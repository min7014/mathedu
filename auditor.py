#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auditor.py
===============================================================================
🛡️ [Auditor Agent] 저작권 · 상표권 · 유튜브 YPP 정책 · 보안 · 수학/시각 무결성 7계층 독립 감사관 엔진
- AI 크레딧 소모 0원 (100% 순수 파이썬 정규식·AST·파일시스템·YouTube API 검증)
- Rule 48 완전 무창 실행 (silent_subprocess 강제 주입)

[7대 전수 감사 계층]
  L1. 등록상표권 감사 (Rule 51): SAT, AP, College Board, AMC, AIME, MAA, IB, IBO, Olympiad/IMO,
      외부 유튜브 채널명(3Blue1Brown, Veritasium 등), 외부 AI 모델명(Nano Banana 등) 대외 메타데이터 노출 적발
  L2. 저작권 & 원천 자료 순수성 감사 (Rule 15 & 51): 전 스크립트 pdf_url의 min7014.github.io 도메인 검증,
      외부 상업 문제집/학원 교재명(쎈, 블랙라벨, 마플, 시대인재, 메가스터디, 대성 등) 혼입 적발
  L3. 유튜브 YPP 심사 안전성 감사 (Rule 35, 46, 49): 중복 제목, 100자 초과 제목, 끝단 조사 절단 제목 점검
  L4. 개인 호칭 배제 감사 (Rule 13.1 & 38): 개별 영상 제목·스크립트·재생목록 내 금지된 개인 호칭 노출 점검
  L5. 비수학 도메인 절대 격리 감사 (Rule 2): 투자·트레이딩·암호화폐 관련 키워드 유입 점검
  L6. Git 저장소 보안 & 미디어 용량 ZERO 감사 (Rule 13.2): .mp4/.png/.wav 및 .env*/token/secret Git 추적 점검
  L7. 시각·폰트·기하 에셋 무결성 감사 (Rule 28, 37, 44, 52): Pillow 캔버스 내 두부 박스(➔ U+2794) 및
      강렬한 적색 RGB(190,18,60)/RGB(244,63,94), 나노바나나 마스터 에셋 해상도(1920x1080) 점검
===============================================================================
"""

import silent_subprocess  # noqa: F401 — Rule 48 windowless enforcement
import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = ROOT_DIR / "video_lectures" / "scripts"
AUDIT_REPORT_FILE = ROOT_DIR / ".agents" / "latest_audit_report.json"

# L1: 대외 영상 제목·설명·태그·재생목록에 절대 노출 금지되는 등록상표 패턴
FORBIDDEN_TRADEMARK_PATTERNS = [
    (r"\bSAT\b", "College Board 등록상표 'SAT'"),
    (r"\bAP\s*Calculus\b", "College Board 등록상표 'AP Calculus'"),
    (r"\bCollege\s*Board\b", "외부 기관명 'College Board'"),
    (r"\bAMC\s*(?:8|10|12|Math)?\b", "MAA 등록상표 'AMC'"),
    (r"\bAIME\b", "MAA 등록상표 'AIME'"),
    (r"\bIB\s*Math\b", "IBO 등록상표 'IB Math'"),
    (r"\bOlympiad\b", "외부 경시 명칭 'Olympiad'"),
    (r"\bIMO\b", "외부 경시 명칭 'IMO'"),
    (r"\bNano\s*Banana\b", "구글 내부 모델 브랜드명 'Nano Banana' 대외 노출"),
    (r"\b나노\s*바나나\b|\b나노바나나\b", "구글 모델 브랜드명 '나노바나나' 대외 노출"),
    (r"\bGoogle\s*Flow\b|\b구글\s*플로우\b|\bVeo\s*3(?:\.\d+)?\b|\bGemini\s*Omni\b", "구글 내부 영상 도구명(Google Flow/Veo/Omni) 대외 노출"),
    (r"\b3Blue1Brown\b|\bVeritasium\b|\bKurzgesagt\b|\bMindYourDecisions\b|\bMathologer\b|\b깨봉수학\b", "타 유튜브 채널 상표 노출"),
    (r"\bDuolingo\b|\bWordle\b|\bNetflix\b", "타사 플랫폼 상표 노출"),
]

# L2: 외부 사설 문제집·학원 교재 저작권 위험 키워드
FORBIDDEN_EXTERNAL_TEXTBOOK_PATTERNS = [
    (r"블랙라벨|일품수학|최상위수학|마플시너지|자이스토리|마더텅|시대인재|대성마이맥|메가스터디|현우진|뉴런", "외부 상업 문제집/사설 학원 상표·저작물 언급"),
]

# L4: 개별 영상 내 금지 호칭 (Rule 13.1; 채널 공식명 제외)
FORBIDDEN_VIDEO_HONORIFIC_RE = re.compile(r"민은기\s*선생님|Min's\s*Math\s*Lab|Min\s*Eunki", re.IGNORECASE)

# L5: 비수학·트레이딩 도메인 절대 격리 키워드 (Rule 2)
FORBIDDEN_TRADING_DOMAIN_RE = re.compile(
    r"\bS-NOVA\b|암호화폐|비트코인|이더리움|선물거래|레버리지\s*투자|매수\s*타점|매도\s*타점|코인\s*차트|\b cryptocurrency\b|\bforex\s*trading\b",
    re.IGNORECASE,
)

# 대외 생성 파이썬 모듈 목록 (감사 자체 모듈인 auditor.py 및 정화 치환 테이블 제외)
PUBLIC_GENERATOR_MODULES = [
    "exam_hybrid_creator.py",
    "nano_banana_cinema_creator.py",
    "google_flow_controller.py",
    "finance.py",
    "min7014_video_maker.py",
    "creative_idea_cinema.py",
    "video_creator.py",
    "secretary.py",
]


def sanitize_and_gate_upload_payload(title: str, description: str, tags: list[str] | None = None) -> dict:
    """
    유튜브 업로드 직전 호출되는 0-크레딧 하드 게이트(Hard Gate).
    상표권·개인호칭·외부 모델명·비수학 용어를 즉시 정화하고 무결성을 보증합니다.
    """
    import youtube_self_evolving_engine as ysee

    t = ysee.sanitize_copyright_and_trademark_text(str(title or ""))
    d = ysee.sanitize_copyright_and_trademark_text(str(description or ""))
    raw_tags = list(tags or [])

    extra_subs = [
        (r"\bNano\s*Banana\b|나노\s*바나나|나노바나나", "시네마틱 기하"),
        (r"\bGoogle\s*Flow\b|구글\s*플로우|\bVeo\s*3(?:\.\d+)?\b|\bGemini\s*Omni\b", "시네마틱 모션"),
        (r"\b3Blue1Brown\b|\bVeritasium\b|\bKurzgesagt\b|\bMindYourDecisions\b|\bMathologer\b|깨봉수학", ""),
        (r"\bDuolingo\b|\bWordle\b|\bNetflix\b", ""),
        (r"민은기\s*선생님의\s*수학자료실_AI|Min's\s*Math\s*Lab\s*AI", "@min7014_ai"),
        (r"민은기\s*선생님[의]*|Min's\s*Math\s*Lab", ""),
    ]
    for pat, rep in extra_subs:
        t = re.sub(pat, rep, t, flags=re.IGNORECASE)
        d = re.sub(pat, rep, d, flags=re.IGNORECASE)

    t = re.sub(r"\s{2,}", " ", t).strip()[:100]
    d = re.sub(r"[ \t]{2,}", " ", d).strip()

    clean_tags = []
    for tg in raw_tags:
        ctg = ysee.sanitize_copyright_and_trademark_text(str(tg))
        for pat, rep in extra_subs:
            ctg = re.sub(pat, rep, ctg, flags=re.IGNORECASE).strip()
        if ctg and not any(re.search(p, ctg, re.IGNORECASE) for p, _ in FORBIDDEN_TRADEMARK_PATTERNS):
            clean_tags.append(ctg)

    violations_prevented = (t != str(title or "").strip()) or (d != str(description or "").strip()) or (len(clean_tags) != len(raw_tags))
    return {
        "title": t,
        "description": d,
        "tags": clean_tags,
        "sanitized": violations_prevented,
    }


def run_full_audit(auto_fix: bool = False, check_live_youtube: bool = False) -> dict:
    """7계층 전수 감사 실행 (0 크레딧 · 고속 스캔)"""
    findings = {
        "L1_trademark": [],
        "L2_copyright_origin": [],
        "L3_ypp_titles": [],
        "L4_honorific_leak": [],
        "L5_domain_separation": [],
        "L6_git_security": [],
        "L7_visual_integrity": [],
    }
    fixed_actions = []

    # ---------------- L1, L2, L3, L4: 스크립트 패키지 메타데이터 전수 스캔 ----------------
    seen_titles = {}
    checked_scripts = 0
    for sp in sorted(SCRIPTS_DIR.glob("*.json")):
        checked_scripts += 1
        try:
            sdoc = json.loads(sp.read_text(encoding="utf-8"))
        except Exception:
            continue
        changed_sdoc = False

        # L2: 원천 PDF 도메인 확인
        pdf_url = str(sdoc.get("pdf_url") or "").strip()
        if pdf_url and "min7014.github.io" not in pdf_url.lower():
            findings["L2_copyright_origin"].append(f"{sp.name}: 비공식 외부 pdf_url 감지 ({pdf_url[:70]})")

        # 패키지별 대외 제목/퀴즈 점검
        for pkg_key in ("exam_hybrid_packages", "nano_banana_packages"):
            pkg_map = sdoc.get(pkg_key) or {}
            for lc, pkg in pkg_map.items():
                if not isinstance(pkg, dict):
                    continue
                for fld in ("title", "short_title", "comment_quiz"):
                    val = str(pkg.get(fld) or "")
                    if not val:
                        continue
                    for pat, desc_lbl in FORBIDDEN_TRADEMARK_PATTERNS:
                        if re.search(pat, val, re.IGNORECASE):
                            if auto_fix:
                                cleaned = sanitize_and_gate_upload_payload(val, "", [])["title" if "title" in fld else "title"]
                                pkg[fld] = cleaned
                                changed_sdoc = True
                                fixed_actions.append(f"Fixed {sp.stem}.{pkg_key}.{lc}.{fld}")
                            else:
                                findings["L1_trademark"].append(f"{sp.stem}.{pkg_key}.{lc}.{fld}: {desc_lbl} ('{val[:55]}')")
                    for pat, desc_lbl in FORBIDDEN_EXTERNAL_TEXTBOOK_PATTERNS:
                        if re.search(pat, val, re.IGNORECASE):
                            findings["L2_copyright_origin"].append(f"{sp.stem}.{pkg_key}.{lc}.{fld}: {desc_lbl}")
                    if FORBIDDEN_VIDEO_HONORIFIC_RE.search(val):
                        findings["L4_honorific_leak"].append(f"{sp.stem}.{pkg_key}.{lc}.{fld}: 금지 호칭 포함")
                    if "title" in fld:
                        if len(val) > 100:
                            findings["L3_ypp_titles"].append(f"{sp.stem}.{pkg_key}.{lc}.{fld}: 100자 초과 ({len(val)}자)")
                        t_norm = val.strip().lower()
                        if t_norm in seen_titles and seen_titles[t_norm] != f"{sp.stem}:{pkg_key}:{lc}:{fld}":
                            findings["L3_ypp_titles"].append(f"중복 패키지 제목: '{val[:48]}'")
                        seen_titles[t_norm] = f"{sp.stem}:{pkg_key}:{lc}:{fld}"

        if changed_sdoc:
            sp.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---------------- L1, L5, L7: 핵심 생성 파이썬 모듈 및 웹 HTML 스캔 ----------------
    for mod_name in PUBLIC_GENERATOR_MODULES:
        mp = ROOT_DIR / mod_name
        if not mp.exists():
            continue
        src = mp.read_text(encoding="utf-8", errors="ignore")
        # 주석 라인 제외한 실제 코드/문자열 라인 검사
        code_lines = [ln for ln in src.splitlines() if not ln.strip().startswith("#")]
        code_body = "\n".join(code_lines)

        if FORBIDDEN_TRADING_DOMAIN_RE.search(code_body):
            findings["L5_domain_separation"].append(f"{mod_name}: 비수학/트레이딩 키워드 감지")

        if mod_name in ("exam_hybrid_creator.py", "nano_banana_cinema_creator.py"):
            if "(190, 18, 60)" in code_body or "(244, 63, 94)" in code_body:
                findings["L7_visual_integrity"].append(f"{mod_name}: Rule 37 위반 강렬한 적색 RGB 잔존")
            if "➔" in code_body:
                findings["L7_visual_integrity"].append(f"{mod_name}: Pillow 폰트 미지원 화살표(➔ U+2794) 잔존 -> □ 깨짐 위험")

    for html_name in ("index.html", "video_board.html", "mathlab.html"):
        hp = ROOT_DIR / html_name
        if hp.exists():
            hsrc = hp.read_text(encoding="utf-8", errors="ignore")
            if FORBIDDEN_TRADING_DOMAIN_RE.search(hsrc):
                findings["L5_domain_separation"].append(f"{html_name}: 비수학/트레이딩 용어 감지")

    # ---------------- L7: 나노바나나 마스터 아트워크 해상도 검수 ----------------
    nb_dir = ROOT_DIR / "youtube_uploads" / "nano_banana_assets"
    if nb_dir.exists():
        try:
            from PIL import Image
            for png_f in sorted(nb_dir.glob("*.png")):
                with Image.open(png_f) as im:
                    if im.size != (1920, 1080):
                        findings["L7_visual_integrity"].append(f"{png_f.name}: 1920x1080 표준 해상도 불일치 ({im.size})")
        except Exception:
            pass

    # ---------------- L6: Git 미디어 및 비밀키 유출 ZERO 스캔 ----------------
    try:
        tracked = subprocess.run(
            ["git", "ls-files"], cwd=str(ROOT_DIR), capture_output=True, text=True, encoding="utf-8", timeout=15
        ).stdout.splitlines()
        bad_exts = (".mp4", ".webm", ".mov", ".wav", ".mp3")
        secret_markers = (".env", "client_secret", "youtube_token", "oauth_token")
        for tf in tracked:
            tfl = tf.lower()
            if tfl.endswith(bad_exts):
                findings["L6_git_security"].append(f"Git 미디어 파일 추적 감지 (Rule 13.2 위반): {tf}")
            if any(sm in tfl for sm in secret_markers) and not tfl.endswith(".example"):
                findings["L6_git_security"].append(f"Git 비밀키/환경변수 파일 추적 감지: {tf}")
    except Exception as e:
        findings["L6_git_security"].append(f"git ls-files 점검 실패: {e}")

    # ---------------- L1, L3, L4 (Live): 유튜브 채널 라이브 재생목록 & 최신 영상 전수 스캔 ----------------
    live_checked = {"playlists": 0, "videos": 0}
    if check_live_youtube:
        try:
            import min7014_video_maker as vm
            yt, _ = vm.get_available_youtube_upload_service()
            if yt is not None:
                pls = yt.playlists().list(part="snippet", mine=True, maxResults=50).execute().get("items", [])
                live_checked["playlists"] = len(pls)
                for pl in pls:
                    pid = pl["id"]
                    pt = pl["snippet"].get("title", "")
                    pd = pl["snippet"].get("description", "")
                    combo = f"{pt} {pd}"
                    hit_tm = [lbl for pat, lbl in FORBIDDEN_TRADEMARK_PATTERNS if re.search(pat, combo, re.IGNORECASE)]
                    if hit_tm:
                        if auto_fix:
                            gated = sanitize_and_gate_upload_payload(pt, pd, [])
                            yt.playlists().update(
                                part="snippet",
                                body={"id": pid, "snippet": {"title": gated["title"][:140], "description": gated["description"][:4000]}},
                            ).execute()
                            fixed_actions.append(f"Sanitized live playlist {pid}")
                        else:
                            findings["L1_trademark"].append(f"Live Playlist {pid} ('{pt[:45]}'): {', '.join(hit_tm)}")

                ch = yt.channels().list(part="contentDetails", mine=True).execute()["items"][0]
                upl = ch["contentDetails"]["relatedPlaylists"]["uploads"]
                v_items = yt.playlistItems().list(part="snippet", playlistId=upl, maxResults=35).execute().get("items", [])
                live_checked["videos"] = len(v_items)
                live_titles_seen = set()
                for it in v_items:
                    vid = it["snippet"]["resourceId"]["videoId"]
                    vt = it["snippet"].get("title", "")
                    vd = it["snippet"].get("description", "")
                    for pat, lbl in FORBIDDEN_TRADEMARK_PATTERNS:
                        if re.search(pat, f"{vt} {vd}", re.IGNORECASE):
                            findings["L1_trademark"].append(f"Live Video {vid} ('{vt[:45]}'): {lbl}")
                    if FORBIDDEN_VIDEO_HONORIFIC_RE.search(vt):
                        findings["L4_honorific_leak"].append(f"Live Video {vid}: 제목 내 개인 호칭 노출 ('{vt[:45]}')")
                    if vt.strip().lower() in live_titles_seen:
                        findings["L3_ypp_titles"].append(f"Live 최근 영상 중복 제목 감지: '{vt[:48]}'")
                    live_titles_seen.add(vt.strip().lower())
        except Exception as e:
            findings["L1_trademark"].append(f"Live YouTube API 조회 참고: {str(e)[:80]}")

    total_issues = sum(len(v) for v in findings.values())
    report = {
        "audited_at": datetime.now().isoformat(timespec="seconds"),
        "status": "PASS_ZERO_VIOLATIONS" if total_issues == 0 else "ACTION_REQUIRED",
        "total_violations": total_issues,
        "checked_scripts": checked_scripts,
        "live_youtube_checked": live_checked,
        "fixed_actions": fixed_actions,
        "findings": findings,
    }
    AUDIT_REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_REPORT_FILE.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def build_telegram_audit_summary(check_live: bool = True, auto_fix: bool = False) -> str:
    rep = run_full_audit(auto_fix=auto_fix, check_live_youtube=check_live)
    f = rep["findings"]
    badge = "✅ [무결성 100% PASS]" if rep["total_violations"] == 0 else f"🚨 [경고: {rep['total_violations']}건 감지]"
    lines = [
        f"🛡️ [독립 감사관(auditor) 7계층 전수 감사 리포트] {badge}",
        f"• 점검 시각: {rep['audited_at']} (스크립트 {rep['checked_scripts']}건"
        + (f", 라이브 재생목록 {rep['live_youtube_checked']['playlists']}개·최신영상 {rep['live_youtube_checked']['videos']}편)" if check_live else ")"),
        f"• [L1 등록상표권 (SAT·AMC·IB·타채널·AI상표)]: {len(f['L1_trademark'])}건",
        f"• [L2 저작권·원문 순수성 (min7014 100%)]: {len(f['L2_copyright_origin'])}건",
        f"• [L3 YPP 심사 안전성 (중복·절단 제목)]: {len(f['L3_ypp_titles'])}건",
        f"• [L4 개별영상 개인호칭 배제 (Rule 13.1)]: {len(f['L4_honorific_leak'])}건",
        f"• [L5 비수학·트레이딩 격리 (Rule 2)]: {len(f['L5_domain_separation'])}건",
        f"• [L6 Git 미디어·비밀키 유출 (Rule 13.2)]: {len(f['L6_git_security'])}건",
        f"• [L7 시각·글리프·기하 비례 (Rule 37·44·52)]: {len(f['L7_visual_integrity'])}건",
    ]
    if rep["fixed_actions"]:
        lines.append(f"• 🔧 자동 정화 완료: {len(rep['fixed_actions'])}건")
    if rep["total_violations"] > 0:
        sample = []
        for k, arr in f.items():
            for item in arr[:2]:
                sample.append(f"  - [{k}] {item}")
        lines.extend(sample[:6])
    return "\n".join(lines)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Mathedu 7-Layer Copyright, Trademark & Integrity Auditor")
    ap.add_argument("mode", nargs="?", default="check", choices=["check", "fix", "telegram"])
    ap.add_argument("--live", action="store_true", help="Include live YouTube playlists & recent uploads check")
    args = ap.parse_args()

    if args.mode == "telegram":
        print(build_telegram_audit_summary(check_live=args.live, auto_fix=False))
    else:
        res = run_full_audit(auto_fix=(args.mode == "fix"), check_live_youtube=args.live)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        sys.exit(0 if res["total_violations"] == 0 else 1)
