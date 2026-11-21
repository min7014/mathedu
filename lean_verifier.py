# -*- coding: utf-8 -*-
"""
lean_verifier.py
================
Machine-checked Lean 4 (v4.36.0) formal proof verifier, catalog builder,
and Telegram briefing helper for the MathEdu platform (Policy 82).

Uses pure Lean 4 core (no external Mathlib dependency) so every theorem
compiles sub-second locally AND runs identically in live.lean-lang.org.
"""

from __future__ import annotations

import silent_subprocess  # noqa: F401

import collections
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent
LEAN_DIR = ROOT_DIR / "lean_proofs"
LEAN_MAIN_FILE = LEAN_DIR / "MatheduFormalProofs.lean"
SCRIPTS_DIR = ROOT_DIR / "video_lectures" / "scripts"
CATALOG_PATH = ROOT_DIR / "assets" / "lean_formal_proofs.json"

KST = dt.timezone(dt.timedelta(hours=9))

THEOREM_SPECS: list[dict[str, str]] = [
    {
        "slug": "2017090101",
        "theorem_name": "pythagorean_square_dissection",
        "precondition_ko": "직각을 낀 두 변 a, b와 빗변 c에 대해 한 변이 a+b인 정사각형을 4개 직각삼각형과 넓이 c^2인 중앙 정사각형으로 분할한 넓이 등식 조건에서 a^2 + b^2 = c^2 을 형식 증명합니다.",
        "precondition_en": "Given the outer square area partition (a + b)^2 = c^2 + 2ab formed by four right triangles with legs a, b and hypotenuse c, prove a^2 + b^2 = c^2 over Int.",
    },
    {
        "slug": "2014111902",
        "theorem_name": "ceva_area_ratio_concurrency",
        "precondition_ko": "양수 넓이 sA, sB, sC > 0를 갖는 삼각형 내부 분할에서 밑변비와 넓이비 비례식(bd*sC = dc*sB 등 3식)이 성립하면 체바 곱 등식 bd*ce*af = dc*ea*fb 가 필연적으로 성립함을 형식 증명합니다.",
        "precondition_en": "Given positive sub-triangle areas sA, sB, sC > 0 and shared-altitude area proportions along sides BC, CA, AB, cancel positive area factors in Lean 4 to prove bd * ce * af = dc * ea * fb.",
    },
    {
        "slug": "2014111901",
        "theorem_name": "menelaus_parallel_ratio_product",
        "precondition_ko": "평행 보조선 선분 길이 ck > 0와 닮음 보조 선분 p, q > 0에 대한 3개의 닮음 비례식으로부터 메넬라우스 곱 등식 bd*ce*af = dc*ea*fb 를 약분 소거로 형식 증명합니다.",
        "precondition_en": "Using positive parallel-auxiliary segment measures ck, p, q > 0 and three similarity proportions across a transversal, formally prove bd * ce * af = dc * ea * fb.",
    },
    {
        "slug": "2014080601",
        "theorem_name": "cauchy_schwarz_lagrange_r2",
        "precondition_ko": "2차원 정수 벡터 (a1, a2), (b1, b2)에 대해 라그랑주 항등식과 완전제곱의 비음수성((a1*b2 - a2*b1)^2 >= 0)을 결합해 코시-슈바르츠 부등식을 논리 공백 없이 증명합니다.",
        "precondition_en": "Combine the 2D Lagrange identity with non-negativity of a square over Int to formally prove (a1*b1 + a2*b2)^2 <= (a1^2 + a2^2)*(b1^2 + b2^2).",
    },
    {
        "slug": "2020062702",
        "theorem_name": "arithmetic_mean_and_square_inequality",
        "precondition_ko": "등차중항 조건 2*m = a + b 로부터 대칭 간격 m - a = b - m 과 완전제곱 항등식 (a+b)^2 >= 4ab 를 동시에 형식 증명합니다.",
        "precondition_en": "From the arithmetic mean relation 2*m = a + b, formally prove equal deviation m - a = b - m together with 4*(a*b) <= (a + b)^2.",
    },
    {
        "slug": "2017091805",
        "theorem_name": "circumcenter_perpendicular_bisectors_concurrency",
        "precondition_ko": "변 AB의 수직이등분선 조건 dOA = dOB와 변 BC의 수직이등분선 조건 dOB = dOC가 만나면 세 꼭짓점까지의 거리가 모두 같음(dOA = dOC)을 전이성으로 증명합니다.",
        "precondition_en": "From perpendicular bisector equidistance dOA = dOB and dOB = dOC, formally prove concurrency equidistance dOA = dOC to all three vertices.",
    },
    {
        "slug": "2017091809",
        "theorem_name": "incenter_angle_bisectors_and_inradius_area",
        "precondition_ko": "내각의 이등분선 교점의 세 변까지 거리 일치(dAB = dBC = dCA)와 내접원 반지름 r에 의한 세 삼각형 2배 넓이 합 2*(S1+S2+S3) = r*(a+b+c)를 동시 증명합니다.",
        "precondition_en": "Prove triple-distance equality from two angle bisectors alongside the doubled triangle area partition 2*(areaBC + areaCA + areaAB) = r*(a + b + c).",
    },
    {
        "slug": "2019111301",
        "theorem_name": "perpendicular_bisector_equidistance",
        "precondition_ko": "좌표평면에서 선분 AB의 중점 M(2*mx = ax+bx, 2*my = ay+by_)과 수직 내적 조건 PM·AB = 0이 주어지면 |PA|^2 = |PB|^2 임을 직접 항등식으로 증명합니다.",
        "precondition_en": "Given Cartesian midpoint 2*mx = ax + bx, 2*my = ay + by_ and dot-product orthogonality to AB, prove squared distance equality distSq(P, A) = distSq(P, B).",
    },
    {
        "slug": "2017091820",
        "theorem_name": "space_diagonal_6_3_5_prism",
        "precondition_ko": "밑면 대각선 제곱 dBaseSq = a^2 + b^2 와 높이 c의 직각관계로부터 공간대각선 제곱 dSpaceSq = a^2 + b^2 + c^2 및 6-3-5 직육면체의 제곱값 70을 형식 검증합니다.",
        "precondition_en": "From base diagonal dBaseSq = a^2 + b^2 and prism height c, prove dSpaceSq = a^2 + b^2 + c^2 and machine-verify 6^2 + 3^2 + 5^2 = 70.",
    },
    {
        "slug": "2017090405",
        "theorem_name": "isosceles_base_angles_sum",
        "precondition_ko": "삼각형 내각의 합 apex + b1 + b2 = 180도와 두 밑각 합동 b1 = b2 조건으로부터 꼭지각과 두 밑각의 일반 관계식 apex + 2*b1 = 180을 증명합니다.",
        "precondition_en": "Combine the triangle angle sum apex + b1 + b2 = 180 with congruent base angles b1 = b2 to prove apex + 2*b1 = 180 and 2*b2 = 180 - apex.",
    },
    {
        "slug": "2017032702",
        "theorem_name": "conjugate_rationalization_identity",
        "precondition_ko": "제곱 성질 sA^2 = a, sB^2 = b를 만족하는 두 근호 항의 켤레 곱 (sA + sB)*(sA - sB)가 유리식 a - b로 정확히 소거됨을 형식 증명합니다.",
        "precondition_en": "When sA^2 = a and sB^2 = b, formally prove that the conjugate product (sA + sB)*(sA - sB) collapses to the rationalized difference a - b.",
    },
    {
        "slug": "math20250130001",
        "theorem_name": "pythagoras_tree_area_conservation",
        "precondition_ko": "매 분기마다 부모 정사각형 넓이가 두 자식 정사각형 넓이의 합과 같을 때(g0 = b1 + b2, b1 = c1 + c2, b2 = c3 + c4), 2세대 4개 정사각형의 넓이 총합이 뿌리 넓이 g0로 보존됨을 증명합니다.",
        "precondition_en": "Assuming each Pythagorean branching step preserves square area (g0 = b1 + b2, b1 = c1 + c2, b2 = c3 + c4), prove total second-generation area equals root area g0.",
    },
    {
        "slug": "2012093001",
        "theorem_name": "inscribed_angle_double_central",
        "precondition_ko": "원의 중심을 지나는 지름으로 분할된 두 이등변삼각형의 외각 성질(ext1 = a1+b1, ext2 = a2+b2, a1=b1, a2=b2)로부터 중심각이 원주각의 정확히 2배임을 증명합니다.",
        "precondition_en": "Splitting an inscribed angle by a diameter into two isosceles triangles (a1 = b1, a2 = b2) with exterior angles ext1, ext2 proves central angle = 2 * (a1 + a2).",
    },
    {
        "slug": "2012100304",
        "theorem_name": "alternate_segment_tangent_chord",
        "precondition_ko": "접선-반지름 수직(tangentAngle + compAngle = 90)과 지름 위 원주각 직각(inscribedAngle + compAngle = 90)을 결합해 접선과 현이 이루는 각이 원주각과 같음을 증명합니다.",
        "precondition_en": "Combine tangent-radius perpendicularity (tangentAngle + compAngle = 90) and the diameter right-angle relation (inscribedAngle + compAngle = 90) to prove tangentAngle = inscribedAngle.",
    },
]


def find_lean_toolchain_binaries() -> tuple[str, str]:
    """Locate lean.exe and lake.exe without assuming PATH."""
    elan_bin = Path.home() / ".elan" / "bin"
    lean_bin = shutil.which("lean") or (
        str(elan_bin / "lean.exe") if (elan_bin / "lean.exe").exists() else str(elan_bin / "lean")
    )
    lake_bin = shutil.which("lake") or (
        str(elan_bin / "lake.exe") if (elan_bin / "lake.exe").exists() else str(elan_bin / "lake")
    )
    if not Path(lean_bin).exists():
        raise FileNotFoundError(f"Lean compiler not found at {lean_bin}")
    return lean_bin, lake_bin


def _run_tool(cmd: list[str], cwd: Path | None = None, timeout: int = 90) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=timeout,
    )


def _extract_theorem_blocks(source_text: str) -> dict[str, str]:
    """Extract self-contained theorem blocks keyed by theorem_name from MatheduFormalProofs.lean."""
    blocks: dict[str, str] = {}
    lines = source_text.splitlines()
    marker_indices: list[tuple[int, str]] = []
    for idx, line in enumerate(lines):
        m = re.match(r"^theorem\s+([A-Za-z0-9_']+)", line)
        if m:
            # Include the single header comment directly above if present
            start_idx = idx
            if idx > 0 and lines[idx - 1].startswith("-- "):
                start_idx = idx - 1
            marker_indices.append((start_idx, m.group(1)))

    for pos, (start_idx, thm_name) in enumerate(marker_indices):
        end_idx = marker_indices[pos + 1][0] if pos + 1 < len(marker_indices) else len(lines)
        snippet = "\n".join(lines[start_idx:end_idx]).strip()
        blocks[thm_name] = snippet
    return blocks


def _load_script_metadata(slug: str) -> dict[str, Any]:
    sp = SCRIPTS_DIR / f"{slug}.json"
    if not sp.exists():
        return {}
    try:
        return json.loads(sp.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _audit_all_scripts() -> dict[str, Any]:
    if not SCRIPTS_DIR.exists():
        return {"total_scripts": 0, "with_teacher_analysis": 0, "sub_domains": {}}
    total = 0
    with_analysis = 0
    sub_domains: collections.Counter[str] = collections.Counter()
    for p in sorted(SCRIPTS_DIR.glob("*.json")):
        total += 1
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
            if doc.get("teacher_proof_analysis"):
                with_analysis += 1
            sd = (doc.get("sub_domain_ko") or "기타").strip()
            sub_domains[sd] += 1
        except Exception:
            sub_domains["parse_error"] += 1
    return {
        "total_scripts": total,
        "with_teacher_analysis": with_analysis,
        "sub_domains": dict(sub_domains.most_common()),
    }


def _assert_zero_sorry_clean(lean_text: str, label: str) -> None:
    non_comment = "\n".join(
        ln for ln in lean_text.splitlines() if not ln.lstrip().startswith("--")
    )
    if re.search(r"\bsorry\b", non_comment):
        raise ValueError(f"{label}: unfinished placeholder detected")
    if re.search(r"\baxiom\b", non_comment):
        raise ValueError(f"{label}: custom axiom detected")


def verify_all_and_build_catalog(audit_scripts: bool = True) -> dict[str, Any]:
    """
    Compile MatheduFormalProofs.lean via lean.exe & lake build, verify every theorem
    snippet standalone (0 sorry, 0 errors), and write assets/lean_formal_proofs.json.
    """
    if not LEAN_MAIN_FILE.exists():
        raise FileNotFoundError(f"Missing Lean formal proof source: {LEAN_MAIN_FILE}")

    lean_bin, lake_bin = find_lean_toolchain_binaries()
    ver_res = _run_tool([lean_bin, "--version"])
    if ver_res.returncode != 0:
        raise RuntimeError(f"lean --version failed: {ver_res.stderr or ver_res.stdout}")
    lean_version = (ver_res.stdout or "").strip().splitlines()[0]

    main_src = LEAN_MAIN_FILE.read_text(encoding="utf-8")
    _assert_zero_sorry_clean(main_src, LEAN_MAIN_FILE.name)

    main_res = _run_tool([lean_bin, str(LEAN_MAIN_FILE)], timeout=90)
    if main_res.returncode != 0:
        raise RuntimeError(f"Lean file verification failed:\n{main_res.stdout}\n{main_res.stderr}")

    if Path(lake_bin).exists():
        lake_res = _run_tool([lake_bin, "build"], cwd=LEAN_DIR, timeout=120)
        if lake_res.returncode != 0:
            raise RuntimeError(f"lake build failed:\n{lake_res.stdout}\n{lake_res.stderr}")

    blocks = _extract_theorem_blocks(main_src)
    theorems_out: list[dict[str, Any]] = []
    proofs_by_slug: dict[str, dict[str, Any]] = {}

    with tempfile.TemporaryDirectory(prefix="mathedu_lean_chk_") as tmpdir:
        tmp_dir = Path(tmpdir)
        for idx, spec in enumerate(THEOREM_SPECS, start=1):
            slug = spec["slug"]
            thm_name = spec["theorem_name"]
            lean_code = blocks.get(thm_name, "").strip()
            if not lean_code:
                raise KeyError(f"Theorem '{thm_name}' not found in {LEAN_MAIN_FILE.name}")
            _assert_zero_sorry_clean(lean_code, thm_name)

            # Machine-check standalone snippet so live.lean-lang.org runs cleanly with zero imports.
            snippet_file = tmp_dir / f"{idx:02d}_{thm_name}.lean"
            snippet_file.write_text(lean_code + "\n", encoding="utf-8")
            s_res = _run_tool([lean_bin, str(snippet_file)], timeout=60)
            if s_res.returncode != 0:
                raise RuntimeError(
                    f"Standalone Lean verification failed for {thm_name} ({slug}):\n"
                    f"{s_res.stdout}\n{s_res.stderr}"
                )

            meta = _load_script_metadata(slug)
            title_ko = (meta.get("title") or spec.get("title_ko") or slug).strip()
            title_en = (meta.get("title_en") or spec.get("title_en") or thm_name).strip()
            sub_domain_ko = (meta.get("sub_domain_ko") or "유클리드 평면기하").strip()
            live_url = "https://live.lean-lang.org/#code=" + urllib.parse.quote(lean_code, safe="")

            entry = {
                "slug": slug,
                "theorem_name": thm_name,
                "title_ko": title_ko,
                "title_en": title_en,
                "sub_domain_ko": sub_domain_ko,
                "precondition_ko": spec["precondition_ko"],
                "precondition_en": spec["precondition_en"],
                "lean_code": lean_code,
                "live_url": live_url,
                "source_file": "lean_proofs/MatheduFormalProofs.lean",
                "verified": True,
                "zero_sorry": True,
            }
            theorems_out.append(entry)
            proofs_by_slug[slug] = entry

    domain_summary = _audit_all_scripts() if audit_scripts else {"total_scripts": 0}
    verified_at = dt.datetime.now(KST).isoformat(timespec="seconds")

    catalog = {
        "schema_version": "1.0",
        "policy": "Policy 82",
        "lean_version": lean_version,
        "verified_at": verified_at,
        "zero_sorry": True,
        "total_theorems": len(THEOREM_SPECS),
        "verified_count": len(theorems_out),
        "source_file": "lean_proofs/MatheduFormalProofs.lean",
        "domain_audit_summary": domain_summary,
        "theorems": theorems_out,
        "proofs_by_slug": proofs_by_slug,
    }

    CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CATALOG_PATH.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return catalog


def _load_or_build_catalog() -> dict[str, Any]:
    if CATALOG_PATH.exists():
        try:
            data = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
            if data.get("zero_sorry") and int(data.get("verified_count", 0)) > 0:
                return data
        except Exception:
            pass
    return verify_all_and_build_catalog(audit_scripts=True)


def format_telegram_lean_briefing(slug: str = "") -> str:
    """Format Korean Telegram briefing either for the full Lean catalog or one theorem slug."""
    cat = _load_or_build_catalog()
    by_slug = cat.get("proofs_by_slug") or {}

    q = (slug or "").strip()
    if q:
        entry = by_slug.get(q)
        if not entry:
            ql = q.lower()
            for cand in by_slug.values():
                if (
                    ql in str(cand.get("slug", "")).lower()
                    or ql in str(cand.get("theorem_name", "")).lower()
                    or ql in str(cand.get("title_ko", "")).lower()
                    or ql in str(cand.get("title_en", "")).lower()
                ):
                    entry = cand
                    break
        if not entry:
            available = ", ".join(list(by_slug.keys())[:8])
            return (
                f"🔍 [Lean 4 형식 증명 검색] '{q}'에 해당하는 정리를 찾지 못했습니다.\n"
                f"등록된 대표 슬러그: {available} 등 총 {len(by_slug)}종\n"
                f"예시: !린 2014111902"
            )
        return (
            f"✅ [Lean 4 형식 증명 검증 완료 · 0 sorry]\n"
            f"📌 주제: {entry.get('title_ko')} ({entry.get('slug')})\n"
            f"🧩 정리명: {entry.get('theorem_name')}\n"
            f"📐 전제·증명 구조: {entry.get('precondition_ko')}\n"
            f"🔬 웹 컴파일러 실행: {entry.get('live_url')}\n\n"
            f"{entry.get('lean_code')}"
        )

    verified_cnt = int(cat.get("verified_count", 0))
    total_cnt = int(cat.get("total_theorems", verified_cnt))
    lean_ver = str(cat.get("lean_version") or "Lean 4")
    m_ver = re.search(r"version\s+([0-9]+\.[0-9]+\.[0-9]+[^\s,\)]*)", lean_ver)
    short_ver = f"Lean v{m_ver.group(1)}" if m_ver else lean_ver
    scripts_cnt = int((cat.get("domain_audit_summary") or {}).get("total_scripts", 0))
    sample_lines = "\n".join(
        f"  • [{t['slug']}] {t['theorem_name']}"
        for t in (cat.get("theorems") or [])[:5]
    )
    return (
        f"🧪 [Lean 4 형식 증명 검증 리포트 · Policy 82]\n"
        f"⚙️ 컴파일러: {short_ver}\n"
        f"✅ 검증 통과: {verified_cnt}/{total_cnt} 정리 (zero_sorry: {cat.get('zero_sorry')})\n"
        f"📚 연동 대본 감사: {scripts_cnt}개 스크립트 스캔 완료\n"
        f"🌐 웹 연동: video_board.html · /en/proofs/ 라이브 플레이그라운드 연결\n"
        f"🕒 검증 시각: {cat.get('verified_at')}\n\n"
        f"대표 형식 정리:\n{sample_lines}\n"
        f"👉 개별 코드 조회: !린 2014111902"
    )


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    cmd = (args[0].lower() if args else "verify")

    if cmd == "verify":
        rep = verify_all_and_build_catalog(audit_scripts=True)
        print(
            json.dumps(
                {
                    "status": "PASS",
                    "lean_version": rep["lean_version"],
                    "verified_at": rep["verified_at"],
                    "total_theorems": rep["total_theorems"],
                    "verified_count": rep["verified_count"],
                    "zero_sorry": rep["zero_sorry"],
                    "catalog_path": str(CATALOG_PATH),
                    "scripts_audited": (rep.get("domain_audit_summary") or {}).get("total_scripts"),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    if cmd == "status":
        cat = _load_or_build_catalog()
        print(
            json.dumps(
                {
                    "lean_version": cat.get("lean_version"),
                    "verified_at": cat.get("verified_at"),
                    "total_theorems": cat.get("total_theorems"),
                    "verified_count": cat.get("verified_count"),
                    "zero_sorry": cat.get("zero_sorry"),
                    "slugs": list((cat.get("proofs_by_slug") or {}).keys()),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    if cmd == "briefing":
        slug = args[1].strip() if len(args) >= 2 else ""
        print(format_telegram_lean_briefing(slug))
        return 0

    print("Usage: python -X utf8 lean_verifier.py [verify|status|briefing [slug]]")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
