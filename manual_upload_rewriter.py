#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
manual_upload_rewriter.py — [Policy 89] 수동 업로드 무인 재작성 · 0-바이트 대기 허브 엔진
=========================================================================================
1. YouTube Studio 웹에서 드래그 앤 드롭으로 수동 업로드(API 업로드 쿼터 0유닛)하면,
   제목·전체 설명란(챕터·원문 링크)·태그·다국어 localizations·커스텀 썸네일·
   고정 첫 댓글(5초 유레카 퀴즈·본편 연결·?sub_confirmation=1)·홈페이지 URL 바인딩까지
   100~150유닛(단일 토큰 풀로 일 65~95편)으로 Priority #0 자동 재작성합니다.
2. youtube_uploads/ready_for_manual_upload/ 폴더에는 NTFS 하드링크(추가 디스크 0바이트)로
   아직 유튜브에 올라가지 않은 MP4만 우선순위별 4개 폴더에 유지합니다.
"""

from __future__ import annotations

import silent_subprocess  # noqa: F401 — Rule 48 windowless child processes

import argparse
from datetime import datetime
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = ROOT_DIR / "video_lectures" / "scripts"
YT_PKG_DIR = ROOT_DIR / "video_lectures" / "youtube_packages"
YT_UPLOADS_DIR = ROOT_DIR / "youtube_uploads"
MASTERCLASS_DIR = YT_UPLOADS_DIR / "masterclasses"
EXAM_HYBRID_DIR = YT_UPLOADS_DIR / "exam_hybrid"
QUESTION_DIR = ROOT_DIR / "video_lectures" / "question_classroom"
SHORTS_MAIN_DIR = YT_UPLOADS_DIR / "shorts"
SHORTS_ALT_DIR = ROOT_DIR / "video_lectures" / "shorts"
READY_MANUAL_DIR = YT_UPLOADS_DIR / "ready_for_manual_upload"
STATE_FILE = ROOT_DIR / ".agents" / "manual_upload_rewrite_state.json"

CHANNEL_ID = "UCSlqQfOEtRfJuMPyGMLgFYA"
UPLOADS_PLAYLIST_ID = "UU" + CHANNEL_ID[2:]
YOUTUBE_RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
SUB_CONFIRM_URL = "https://www.youtube.com/@min7014_ai?sub_confirmation=1"
RULE28_CUTOFF_TS = datetime(2026, 11, 8, 20, 0, 0).timestamp()

KIND_PRIORITY = {"mc": 0, "hyb": 1, "std": 2, "qcl": 3, "hybs": 4, "qsh": 5, "sh": 6}
SUBFOLDER_NAMES = (
    "01_장편_마스터클래스",
    "02_기하통찰_하이브리드",
    "03_1080p_시각증명_본편",
    "04_시각증명_쇼츠",
)

HIGH_SEARCH_TERMS = (
    "피타고라스", "원주각", "접선", "이등변", "외심", "내심", "무게중심", "닮음", "메넬라우스", "체바",
    "포물선", "타원", "쌍곡선", "코사인법칙", "사인법칙", "삼수선", "평균값", "중간값", "산술", "코시",
    "극한", "미분", "정적분", "수열", "등차", "등비", "귀납법", "이차함수", "근의 공식",
)

TAG_PATTERNS = (
    ("mc", re.compile(r"\[MC__([A-Za-z0-9_]+)\]")),
    ("hyb", re.compile(r"\[HYB__([A-Za-z0-9]+)_(ko|en)\]", re.IGNORECASE)),
    ("hybs", re.compile(r"\[HYBS__([A-Za-z0-9]+)_(ko|en)\]", re.IGNORECASE)),
    ("std", re.compile(r"\[STD__([A-Za-z0-9]+)_(ko|en)\]", re.IGNORECASE)),
    ("qcl", re.compile(r"\[QCL__([A-Za-z0-9]+)_(ko|en)\]", re.IGNORECASE)),
    ("sh", re.compile(r"\[SH__([A-Za-z0-9]+)_(ko|en)\]", re.IGNORECASE)),
    ("qsh", re.compile(r"\[QSH__([A-Za-z0-9]+)_(ko|en)\]", re.IGNORECASE)),
)
LEGACY_SHORT_TAG_RE = re.compile(r"\[([A-Za-z0-9]+)_SHORT_(KO|EN)\]")
LEGACY_STD_TAG_RE = re.compile(r"\[([A-Za-z0-9]+)_(KO|EN)\]")

STEM_MC_RE = re.compile(r"^(masterclass_[A-Za-z0-9_]+)$")
STEM_PATTERNS = (
    ("hyb", re.compile(r"^([A-Za-z0-9]+)_exam_(ko|en)$", re.IGNORECASE)),
    ("hybs", re.compile(r"^([A-Za-z0-9]+)_exam_short_(ko|en)$", re.IGNORECASE)),
    ("qcl", re.compile(r"^([A-Za-z0-9]+)_q_(ko|en)$", re.IGNORECASE)),
    ("qsh", re.compile(r"^([A-Za-z0-9]+)_short_q_(ko|en)$", re.IGNORECASE)),
    ("sh", re.compile(r"^([A-Za-z0-9]+)_short_(ko|en)$", re.IGNORECASE)),
    ("std", re.compile(r"^([A-Za-z0-9]+)_(ko|en)$", re.IGNORECASE)),
)
STRIP_BRACKET_TAG_RE = re.compile(
    r"\s*\[(?:(?:MC|HYB|HYBS|STD|QCL|SH|QSH)__[^\]]+|[A-Za-z0-9]+_(?:SHORT_)?(?:KO|EN))\]",
    re.IGNORECASE,
)


def _read_json(path: Path, default=None):
    if not path.exists():
        return {} if default is None else default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {} if default is None else default


def _write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _extract_yt_id(url_or_id: str) -> str:
    txt = str(url_or_id or "").strip()
    m = re.search(r"(?:youtu\.be/|shorts/|v=)([A-Za-z0-9_-]{11})", txt)
    if m:
        return m.group(1)
    return txt if re.fullmatch(r"[A-Za-z0-9_-]{11}", txt) else ""


def _spec_key(spec: dict) -> str:
    kind = spec.get("kind", "")
    if kind == "mc":
        return f"mc:{spec.get('mc_slug', '')}"
    return f"{kind}:{spec.get('slug', '')}:{spec.get('lang', 'ko')}"


def load_rewrite_state() -> dict:
    st = _read_json(STATE_FILE, {})
    if not isinstance(st, dict):
        st = {}
    st.setdefault("pending_rewrites", {})
    st.setdefault("completed_rewrites", [])
    st.setdefault("updated_at", "")
    return st


def save_rewrite_state(st: dict) -> None:
    st["updated_at"] = datetime.now().isoformat(timespec="seconds")
    comp = list(dict.fromkeys(str(x) for x in st.get("completed_rewrites", []) if x))
    if len(comp) > 2000:
        comp = comp[-2000:]
    st["completed_rewrites"] = comp
    _write_json(STATE_FILE, st)


def _safe_stem_filename(idx: int, raw_title: str, tag: str) -> str:
    clean = re.sub(r'[\\/:*?"<>|\r\n\t]+', " ", str(raw_title or "math"))
    clean = re.sub(r"\s+", " ", clean).strip(" .")
    prefix = f"{idx:03d}_"
    suffix_stem = f" [{tag}]"
    max_title = max(8, 90 - len(prefix) - len(suffix_stem))
    clipped = clean[:max_title].rstrip(" .")
    stem = f"{prefix}{clipped}{suffix_stem}"
    if len(stem) > 90:
        stem = stem[: 90 - len(suffix_stem)].rstrip(" .") + suffix_stem
    return f"{stem}.mp4"


def _ensure_hardlink(src: Path, dst: Path) -> bool:
    if not src.exists():
        return False
    if dst.exists():
        try:
            if os.path.samefile(src, dst):
                return True
        except OSError:
            pass
        try:
            dst.unlink()
        except OSError:
            return False
    try:
        os.link(src, dst)
        return True
    except OSError:
        return False


def _find_short_mp4(slug: str, lc: str, question: bool = False) -> Path | None:
    fname = f"{slug}_short_q_{lc}.mp4" if question else f"{slug}_short_{lc}.mp4"
    for folder in (SHORTS_MAIN_DIR, SHORTS_ALT_DIR):
        p = folder / fname
        if p.exists() and p.stat().st_mtime >= RULE28_CUTOFF_TS:
            return p
    return None


def _queued_spec_keys(state: dict) -> set[str]:
    keys = set()
    for entry in (state.get("pending_rewrites") or {}).values():
        if isinstance(entry, dict) and isinstance(entry.get("spec"), dict):
            keys.add(_spec_key(entry["spec"]))
    return keys


def _ranked_script_paths() -> list[tuple[dict, Path]]:
    try:
        import youtube_self_evolving_engine as ysee
    except Exception:
        ysee = None
    ranked = []
    for sp in sorted(SCRIPTS_DIR.glob("*.json")):
        sdoc = _read_json(sp)
        if not sdoc:
            continue
        pdf_u = str(sdoc.get("pdf_url") or "").lower()
        if not (pdf_u.endswith(".pdf") and "min7014.github.io" in pdf_u):
            continue
        title = str(sdoc.get("title") or "")
        title_en = str(sdoc.get("title_en") or "")
        hot = 1 if any(term in title for term in HIGH_SEARCH_TERMS) else 0
        c_boost = float(ysee.get_slug_cluster_boost(f"{title} {title_en}")) if ysee else 1.0
        pages = int(sdoc.get("page_count") or len(sdoc.get("pages") or []))
        ranked.append((-round((1 + hot) * c_boost, 2), -c_boost, -pages, sp.stem, sdoc, sp))
    ranked.sort(key=lambda item: (item[0], item[1], item[2], item[3]))
    return [(item[4], item[5]) for item in ranked]


def _mc_sort_key(meta_p: Path, mdoc: dict) -> tuple:
    stem = meta_p.stem.replace("_meta", "")
    dur = float(mdoc.get("duration_sec") or 0.0)
    if stem.startswith("masterclass_original_pdf_"):
        tier = 0
    elif stem.startswith("masterclass_euclidean_geometry_"):
        tier = 1
    elif stem.startswith("masterclass_question_"):
        tier = 2
    else:
        tier = 3
    c_boost = 1.0
    try:
        import youtube_self_evolving_engine as ysee
        t_blob = f"{mdoc.get('title_ko', '')} {mdoc.get('title_en', '')}"
        c_boost = float(ysee.get_slug_cluster_boost(t_blob))
    except Exception:
        pass
    return (tier, -round(c_boost, 2), -dur, stem)


def _sync_manual_subfolder(folder: Path, entries: list[tuple[Path, str]]) -> dict:
    folder.mkdir(parents=True, exist_ok=True)
    active_names = {fname for _, fname in entries}
    linked = 0
    removed = 0
    errors = 0

    for existing in list(folder.glob("*.mp4")):
        if existing.name not in active_names:
            try:
                existing.unlink()
                removed += 1
            except OSError:
                pass

    for src, fname in entries:
        if _ensure_hardlink(src, folder / fname):
            linked += 1
        else:
            errors += 1

    return {"count": len(entries), "linked": linked, "removed": removed, "errors": errors}


def _write_readme(counts: dict[str, int]) -> None:
    lines = [
        "[@min7014_ai 유튜브 스튜디오 수동 업로드 대기 폴더 — Policy 89 자동 재작성]",
        "",
        "■ 사용 방법 (YouTube Data API 업로드 쿼터 0유닛 소모):",
        "  1) https://studio.youtube.com/channel/UCSlqQfOEtRfJuMPyGMLgFYA 에 접속 후 [만들기 -> 동영상 업로드]를 엽니다.",
        "  2) 아래 우선순위 폴더에서 한 번에 최대 15개씩 MP4를 드래그 & 드롭합니다.",
        "     - 제목·설명·태그·썸네일·댓글은 전혀 입력하실 필요 없습니다.",
        "     - [다음 -> 공개(Public) -> 게시]만 누르시면 됩니다.",
        "  3) 게시 직후 0유닛 RSS가 감지하여 이 대기 폴더에서 자동 제거하고,",
        "     매일 17:00 KST 쿼터 리셋(또는 텔레그램 '!재작성') 시 신규 업로드보다 최우선(0순위)으로",
        "     제목·설명·챕터·태그·다국어·커스텀 썸네일·첫 댓글(5초 퀴즈/본편 링크)·홈페이지 등록을 자동 완성합니다.",
        "",
        "■ 권장 업로드 순서 & 현재 미업로드 대기 수량:",
        f"  1. 01_장편_마스터클래스     : {counts.get('01_장편_마스터클래스', 0)}편 (시청시간 4,000h 최단 돌파)",
        f"  2. 02_기하통찰_하이브리드  : {counts.get('02_기하통찰_하이브리드', 0)}편 (구독 전환 부스터)",
        f"  3. 03_1080p_시각증명_본편  : {counts.get('03_1080p_시각증명_본편', 0)}편 (검색 유입 본편 · 상위 200편)",
        f"  4. 04_시각증명_쇼츠        : {counts.get('04_시각증명_쇼츠', 0)}편 (노출 훅 쇼츠 · 상위 200편)",
        "",
        "※ 파일명 끝의 [MC__...], [HYB__...] 등 식별 태그가 유지되므로 제목은 절대 수동 편집하지 마세요.",
    ]
    READY_MANUAL_DIR.mkdir(parents=True, exist_ok=True)
    (READY_MANUAL_DIR / "README_수동업로드_안내.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def prepare_manual_upload_folders() -> dict:
    """아직 유튜브에 업로드되지 않은 MP4만 0-바이트 하드링크로 4대 우선순위 폴더에 동기화합니다."""
    state = load_rewrite_state()
    queued_keys = _queued_spec_keys(state)
    READY_MANUAL_DIR.mkdir(parents=True, exist_ok=True)

    # 1. 01_장편_마스터클래스
    mc_candidates = []
    for mp in sorted(MASTERCLASS_DIR.glob("*_meta.json")):
        mdoc = _read_json(mp)
        if not mdoc or (mdoc.get("youtube_url") or "").strip():
            continue
        mc_slug = str(mdoc.get("mc_slug") or mp.stem.replace("_meta", "")).strip()
        if f"mc:{mc_slug}" in queued_keys:
            continue
        mp4_p = ROOT_DIR / str(mdoc.get("mp4_path") or "")
        if not mp4_p.exists() or mp4_p.stat().st_mtime < RULE28_CUTOFF_TS:
            continue
        lc = str(mdoc.get("lang") or ("en" if mc_slug.endswith("_en") else "ko")).lower()
        raw_t = str(mdoc.get("title_en" if lc == "en" else "title_ko") or mc_slug)
        mc_candidates.append((_mc_sort_key(mp, mdoc), mp4_p, raw_t, f"MC__{mc_slug}"))
    mc_candidates.sort(key=lambda item: item[0])
    mc_entries = [(mp4_p, _safe_stem_filename(i, raw_t, tag)) for i, (_, mp4_p, raw_t, tag) in enumerate(mc_candidates, 1)]

    # 2. 02_기하통찰_하이브리드
    hyb_raw = []
    try:
        import exam_hybrid_creator as ehc
        blueprints = ehc.get_all_ranked_exam_blueprints()
    except Exception:
        blueprints = []
    for bp in blueprints:
        slug = str(bp.get("slug") or "").strip()
        if not slug:
            continue
        sdoc = _read_json(SCRIPTS_DIR / f"{slug}.json")
        ex_urls = sdoc.get("exam_hybrid_urls") or {}
        ex_sh_urls = sdoc.get("exam_hybrid_shorts_urls") or {}
        for lc in ("ko", "en"):
            if not (ex_urls.get(lc) or "").strip() and f"hyb:{slug}:{lc}" not in queued_keys:
                mp4_l = EXAM_HYBRID_DIR / f"{slug}_exam_{lc}.mp4"
                if mp4_l.exists() and mp4_l.stat().st_mtime >= RULE28_CUTOFF_TS:
                    hyb_raw.append((0, mp4_l, str(bp.get(f"title_{lc}") or slug), f"HYB__{slug}_{lc}"))
            if not (ex_sh_urls.get(lc) or "").strip() and f"hybs:{slug}:{lc}" not in queued_keys:
                mp4_s = EXAM_HYBRID_DIR / f"{slug}_exam_short_{lc}.mp4"
                if mp4_s.exists() and mp4_s.stat().st_mtime >= RULE28_CUTOFF_TS:
                    hyb_raw.append((1, mp4_s, str(bp.get(f"short_title_{lc}") or slug), f"HYBS__{slug}_{lc}"))
    hyb_raw.sort(key=lambda item: item[0])
    hyb_entries = [(mp4_p, _safe_stem_filename(i, raw_t, tag)) for i, (_, mp4_p, raw_t, tag) in enumerate(hyb_raw, 1)]

    # 3 & 4. 03_1080p_시각증명_본편 & 04_시각증명_쇼츠 (각 상위 200편)
    ranked_scripts = _ranked_script_paths()
    std_entries: list[tuple[Path, str]] = []
    sh_entries: list[tuple[Path, str]] = []
    for sdoc, sp in ranked_scripts:
        slug = str(sdoc.get("slug") or sp.stem)
        base_ko = str(sdoc.get("title") or slug).split("(")[0].strip()
        base_en = str(sdoc.get("title_en") or base_ko)
        yt_u = sdoc.get("youtube_urls") or {}
        q_yt_u = sdoc.get("question_youtube_urls") or {}
        sh_u = sdoc.get("shorts_urls") or {}
        qsh_u = sdoc.get("question_shorts_urls") or {}

        if len(std_entries) < 200:
            for lc in ("ko", "en"):
                if len(std_entries) >= 200:
                    break
                title_t = base_en if lc == "en" else base_ko
                if not (yt_u.get(lc) or "").strip() and f"std:{slug}:{lc}" not in queued_keys:
                    mp4_p = YT_UPLOADS_DIR / slug / f"{slug}_{lc}.mp4"
                    if mp4_p.exists() and mp4_p.stat().st_mtime >= RULE28_CUTOFF_TS:
                        std_entries.append((mp4_p, _safe_stem_filename(len(std_entries) + 1, title_t, f"STD__{slug}_{lc}")))
                if len(std_entries) >= 200:
                    break
                if not (q_yt_u.get(lc) or "").strip() and f"qcl:{slug}:{lc}" not in queued_keys:
                    q_mp4 = QUESTION_DIR / f"{slug}_q_{lc}.mp4"
                    if q_mp4.exists() and q_mp4.stat().st_mtime >= RULE28_CUTOFF_TS:
                        std_entries.append((q_mp4, _safe_stem_filename(len(std_entries) + 1, title_t, f"QCL__{slug}_{lc}")))

        if len(sh_entries) < 200:
            for lc in ("ko", "en"):
                if len(sh_entries) >= 200:
                    break
                title_t = base_en if lc == "en" else base_ko
                if not (qsh_u.get(lc) or "").strip() and f"qsh:{slug}:{lc}" not in queued_keys:
                    qsh_mp4 = _find_short_mp4(slug, lc, question=True)
                    if qsh_mp4:
                        sh_entries.append((qsh_mp4, _safe_stem_filename(len(sh_entries) + 1, title_t, f"QSH__{slug}_{lc}")))
                if len(sh_entries) >= 200:
                    break
                if not (sh_u.get(lc) or "").strip() and f"sh:{slug}:{lc}" not in queued_keys:
                    sh_mp4 = _find_short_mp4(slug, lc, question=False)
                    if sh_mp4:
                        sh_entries.append((sh_mp4, _safe_stem_filename(len(sh_entries) + 1, title_t, f"SH__{slug}_{lc}")))

        if len(std_entries) >= 200 and len(sh_entries) >= 200:
            break

    results = {
        "01_장편_마스터클래스": _sync_manual_subfolder(READY_MANUAL_DIR / "01_장편_마스터클래스", mc_entries),
        "02_기하통찰_하이브리드": _sync_manual_subfolder(READY_MANUAL_DIR / "02_기하통찰_하이브리드", hyb_entries),
        "03_1080p_시각증명_본편": _sync_manual_subfolder(READY_MANUAL_DIR / "03_1080p_시각증명_본편", std_entries),
        "04_시각증명_쇼츠": _sync_manual_subfolder(READY_MANUAL_DIR / "04_시각증명_쇼츠", sh_entries),
    }
    counts = {k: v["count"] for k, v in results.items()}
    _write_readme(counts)
    return {
        "ready_dir": str(READY_MANUAL_DIR),
        "folders": results,
        "total_ready": sum(counts.values()),
    }


def _spec_from_match(kind: str, ident: str, lang: str = "ko") -> dict | None:
    lc = (lang or "ko").lower()
    if kind == "mc":
        meta_p = MASTERCLASS_DIR / f"{ident}_meta.json"
        if not meta_p.exists() and ident.endswith("_ko"):
            alt = MASTERCLASS_DIR / f"{ident[:-3]}_meta.json"
            if alt.exists():
                meta_p = alt
                ident = ident[:-3]
        if not meta_p.exists():
            return None
        mdoc = _read_json(meta_p)
        mc_lc = str(mdoc.get("lang") or ("en" if ident.endswith("_en") else "ko")).lower()
        return {"kind": "mc", "mc_slug": ident, "slug": ident, "lang": mc_lc, "is_short": False}

    sp = SCRIPTS_DIR / f"{ident}.json"
    if not sp.exists():
        return None
    if kind in ("hyb", "hybs"):
        try:
            import exam_hybrid_creator as ehc
            if not any(str(bp.get("slug")) == ident for bp in ehc.get_all_ranked_exam_blueprints()):
                return None
        except Exception:
            return None
    return {
        "kind": kind,
        "slug": ident,
        "lang": lc,
        "is_short": kind in ("hybs", "sh", "qsh"),
    }


def match_channel_video_to_local_spec(
    video_id: str,
    raw_title: str,
    raw_desc: str,
    pending_map: dict | None = None,
    completed_ids: set[str] | None = None,
) -> dict | None:
    """채널에 올라온 수동 업로드 영상을 로컬 메타 스펙과 1:1 매칭합니다."""
    if video_id in (completed_ids or ()):
        return None
    if pending_map and video_id in pending_map:
        return pending_map[video_id].get("spec")

    title_s = str(raw_title or "").strip()
    desc_s = str(raw_desc or "").strip()
    blob = f"{title_s}\n{desc_s}"

    for kind, pat in TAG_PATTERNS:
        m = pat.search(blob)
        if m:
            ident = m.group(1)
            lc = m.group(2) if m.lastindex and m.lastindex >= 2 else "ko"
            spec = _spec_from_match(kind, ident, lc)
            if spec:
                return spec

    looks_unwritten = ("[" in title_s) or (len(desc_s) < 100)
    if looks_unwritten:
        m_ls = LEGACY_SHORT_TAG_RE.search(blob)
        if m_ls:
            spec = _spec_from_match("sh", m_ls.group(1), m_ls.group(2).lower())
            if spec:
                return spec
        m_ld = LEGACY_STD_TAG_RE.search(blob)
        if m_ld:
            spec = _spec_from_match("std", m_ld.group(1), m_ld.group(2).lower())
            if spec:
                return spec

        stem_candidate = re.sub(r"\.mp4$", "", title_s, flags=re.IGNORECASE).strip()
        m_mc = STEM_MC_RE.match(stem_candidate)
        if m_mc:
            spec = _spec_from_match("mc", m_mc.group(1), "ko")
            if spec:
                return spec
        for kind, pat in STEM_PATTERNS:
            m_st = pat.match(stem_candidate)
            if m_st:
                spec = _spec_from_match(kind, m_st.group(1), m_st.group(2).lower())
                if spec:
                    return spec

    return None


def _spec_already_bound_id(spec: dict) -> str:
    kind = spec["kind"]
    if kind == "mc":
        mdoc = _read_json(MASTERCLASS_DIR / f"{spec['mc_slug']}_meta.json")
        return _extract_yt_id(mdoc.get("youtube_url") or "")
    sdoc = _read_json(SCRIPTS_DIR / f"{spec['slug']}.json")
    field_map = {
        "hyb": "exam_hybrid_urls",
        "hybs": "exam_hybrid_shorts_urls",
        "std": "youtube_urls",
        "qcl": "question_youtube_urls",
        "sh": "shorts_urls",
        "qsh": "question_shorts_urls",
    }
    return _extract_yt_id((sdoc.get(field_map[kind]) or {}).get(spec["lang"]) or "")


def _bind_spec_url_to_local_json(spec: dict, video_id: str) -> str:
    kind = spec["kind"]
    lc = spec["lang"]
    url = f"https://youtube.com/shorts/{video_id}" if spec.get("is_short") else f"https://youtu.be/{video_id}"

    if kind == "mc":
        meta_p = MASTERCLASS_DIR / f"{spec['mc_slug']}_meta.json"
        mdoc = _read_json(meta_p)
        if mdoc:
            mdoc["youtube_url"] = url
            mdoc["uploaded_video_id"] = video_id
            mdoc["manual_upload"] = True
            _write_json(meta_p, mdoc)
        return url

    sp = SCRIPTS_DIR / f"{spec['slug']}.json"
    sdoc = _read_json(sp)
    if not sdoc:
        return url

    if kind == "hyb":
        sdoc.setdefault("exam_hybrid_urls", {})[lc] = url
    elif kind == "hybs":
        sdoc.setdefault("exam_hybrid_shorts_urls", {})[lc] = url
    elif kind == "std":
        sdoc.setdefault("youtube_urls", {})[lc] = url
        pkg = (sdoc.get("youtube_packages") or {}).get(lc)
        if isinstance(pkg, dict):
            pkg["needs_youtube_upload"] = False
            pkg["uploaded_video_id"] = video_id
    elif kind == "qcl":
        sdoc.setdefault("question_youtube_urls", {})[lc] = url
        pkg = (sdoc.get("question_classroom_packages") or {}).get(lc)
        if isinstance(pkg, dict):
            pkg["needs_youtube_upload"] = False
            pkg["uploaded_video_id"] = video_id
    elif kind == "sh":
        sdoc.setdefault("shorts_urls", {})[lc] = url
        pkg = (sdoc.get("shorts_packages") or {}).get(lc)
        if isinstance(pkg, dict):
            pkg["needs_youtube_upload"] = False
            pkg["uploaded_video_id"] = video_id
    elif kind == "qsh":
        sdoc.setdefault("question_shorts_urls", {})[lc] = url
        pkg = (sdoc.get("question_shorts_packages") or {}).get(lc)
        if isinstance(pkg, dict):
            pkg["needs_youtube_upload"] = False
            pkg["uploaded_video_id"] = video_id

    _write_json(sp, sdoc)
    return url


def _finalize_payload(
    vmaker,
    raw_title: str,
    raw_desc: str,
    raw_tags: list[str],
    lang_code: str,
    localizations: dict | None,
    thumb_path: Path | None,
    top_comment: str,
    bound_url: str,
) -> dict:
    import auditor

    cleaned_raw_title = STRIP_BRACKET_TAG_RE.sub("", str(raw_title or "")).strip()
    gated = auditor.sanitize_and_gate_upload_payload(cleaned_raw_title, raw_desc, raw_tags)
    title = vmaker.sanitize_youtube_title(gated["title"], 96)
    desc = vmaker.sanitize_youtube_description(gated["description"])[:4900]

    clean_locs = {}
    for loc_lc, loc_obj in (localizations or {}).items():
        if not isinstance(loc_obj, dict):
            continue
        lt = STRIP_BRACKET_TAG_RE.sub("", str(loc_obj.get("title") or "")).strip()
        ld = str(loc_obj.get("description") or "")
        lg = auditor.sanitize_and_gate_upload_payload(lt or title, ld or desc, [])
        clean_locs[loc_lc] = {
            "title": vmaker.sanitize_youtube_title(lg["title"], 96),
            "description": vmaker.sanitize_youtube_description(lg["description"])[:4900],
        }

    cmt_gated = auditor.sanitize_and_gate_upload_payload("", top_comment, [])
    return {
        "title": title,
        "description": desc,
        "tags": gated["tags"][:25],
        "categoryId": "27",
        "defaultLanguage": lang_code,
        "defaultAudioLanguage": lang_code,
        "localizations": clean_locs,
        "thumb_path": str(thumb_path) if (thumb_path and thumb_path.exists()) else "",
        "top_comment": cmt_gated["description"],
        "bound_url": bound_url,
    }


def build_rewrite_payload(spec: dict, video_id: str) -> dict | None:
    """7개 영상 유형 모두에 대해 제목·설명·태그·다국어·썸네일·첫 댓글 페이로드를 생성합니다."""
    import finance
    import min7014_video_maker as vmaker

    kind = spec["kind"]
    lc = spec["lang"]
    is_en = lc == "en"
    bound_url = f"https://youtube.com/shorts/{video_id}" if spec.get("is_short") else f"https://youtu.be/{video_id}"

    if kind == "mc":
        mdoc = _read_json(MASTERCLASS_DIR / f"{spec['mc_slug']}_meta.json")
        if not mdoc:
            return None
        raw_t = str(mdoc.get("title_en" if is_en else "title_ko") or spec["mc_slug"])
        raw_d = str(mdoc.get("description_en" if is_en else "description_ko") or "")
        tags = list(finance.HIGH_RPM_KEYWORDS_EN if is_en else finance.HIGH_RPM_KEYWORDS_KO)
        ch_lines = "\n".join(mdoc.get("chapters") or [])
        comment = (
            f"💬 Which part of this Masterclass gave you the biggest 'Aha!' moment? Drop the timestamp below! 🤩\n"
            f"▶️ Full Continuous Marathon Playlist: https://www.youtube.com/watch?v={video_id}&list={UPLOADS_PLAYLIST_ID}\n\n"
            f"⏱️ [00:00 | Masterclass Chapter Timestamps — Jump to Any Proof!]\n{ch_lines}\n\n"
            f"🔔 Subscribe to @min7014_ai in 1 Click: {SUB_CONFIRM_URL}\n"
            f"📐 Interactive GeoGebra & 1,113 Visual Proofs: https://min7014.github.io/mathedu/video_board.html?lang=en"
            if is_en
            else f"💬 오늘 마스터클래스 단원 중 가장 명쾌하게 이해된 주제는 몇 강이었나요? 타임스탬프와 함께 댓글로 남겨주세요! 🤩\n"
            f"▶️ 전체 마스터클래스 무중단 연속재생: https://www.youtube.com/watch?v={video_id}&list={UPLOADS_PLAYLIST_ID}\n\n"
            f"⏱️ [00:00 | 마스터클래스 챕터 타임스탬프 — 원하는 단원을 눌러 바로 이동하세요!]\n{ch_lines}\n\n"
            f"🔔 @min7014_ai 1초 무료 구독하기: {SUB_CONFIRM_URL}\n"
            f"📐 전체 1,113개 설명영상 & 무료 GeoGebra 실습 게시판: https://min7014.github.io/mathedu/video_board.html"
        )
        thumb_rel = str(mdoc.get("thumb_path") or "").strip()
        thumb_p = ROOT_DIR / thumb_rel if thumb_rel else None
        if not (thumb_p and thumb_p.exists()):
            for lead_slug in (mdoc.get("slugs") or []):
                cand = YT_PKG_DIR / f"{lead_slug}_{lc}_thumb.png"
                if not cand.exists():
                    cand = YT_PKG_DIR / f"{lead_slug}_ko_thumb.png"
                if cand.exists():
                    thumb_p = cand
                    break
        locs = {
            "ko": {"title": str(mdoc.get("title_ko") or raw_t), "description": str(mdoc.get("description_ko") or raw_d)},
            "en": {"title": str(mdoc.get("title_en") or raw_t), "description": str(mdoc.get("description_en") or raw_d)},
        }
        return _finalize_payload(vmaker, raw_t, raw_d, tags, lc, locs, thumb_p, comment, bound_url)

    slug = spec["slug"]
    sdoc = _read_json(SCRIPTS_DIR / f"{slug}.json")
    if not sdoc:
        return None
    pdf_url = str(sdoc.get("pdf_url") or "https://min7014.github.io/")
    web_url = str(sdoc.get("web_url") or "https://min7014.github.io/")

    if kind in ("hyb", "hybs"):
        import exam_hybrid_creator as ehc
        bp = next((b for b in ehc.get_all_ranked_exam_blueprints() if str(b.get("slug")) == slug), None)
        if not bp:
            return None
        if kind == "hyb":
            raw_t = str(bp["title_en"] if is_en else bp["title_ko"])
            raw_d = (
                f"✨ See why this timeless geometry & algebra theorem holds through pure visual intuition!\n"
                f"📐 100% Original Visual Proof PDF: {pdf_url}\n"
                f"🌐 Interactive Math Lab & Step-by-Step Archive: https://min7014.github.io/mathedu/?lang=en\n"
                f"🔔 Subscribe to @min7014_ai: {SUB_CONFIRM_URL}\n\n"
                f"[ID: {slug}_HYB_{lc.upper()}] #VisualProof #EuclideanGeometry #MathIntuition #GeometryProof"
                if is_en
                else f"✨ 공식 암기 대신 보조선 한 줄과 기하 불변량으로 원리의 필연성을 눈으로 증명합니다!\n"
                f"📐 100% 자체 제작 단계별 시각 증명 PDF: {pdf_url}\n"
                f"🌐 단계별 디딤돌 & 자체 제작 MathLab 실습: https://min7014.github.io/mathedu/\n"
                f"🔔 @min7014_ai 무료 구독하기: {SUB_CONFIRM_URL}\n\n"
                f"[ID: {slug}_HYB_{lc.upper()}] #시각적증명 #도형보조선 #기하학원리 #수학직관 #고등수학"
            )
            tags = ["Visual Math Proof", "Geometry Proof", "Euclidean Geometry"] if is_en else ["시각적증명", "도형보조선", "기하학증명", "수학원리"]
            thumb_p = EXAM_HYBRID_DIR / f"{slug}_exam_{lc}_thumb.png"
            comment = str(bp["comment_quiz_en"] if is_en else bp["comment_quiz_ko"]) + f"\n\n🔔 {SUB_CONFIRM_URL}"
            locs = {
                "ko": {"title": str(bp["title_ko"]), "description": raw_d},
                "en": {"title": str(bp["title_en"]), "description": raw_d},
            }
            return _finalize_payload(vmaker, raw_t, raw_d, tags, lc, locs, thumb_p, comment, bound_url)

        raw_t = str(bp["short_title_en"] if is_en else bp["short_title_ko"])
        long_u = str((sdoc.get("exam_hybrid_urls") or {}).get(lc) or (sdoc.get("youtube_urls") or {}).get(lc) or f"https://www.youtube.com/@min7014_ai")
        raw_d = (
            f"🎬 Watch Full 1080p Visual Proof Breakdown: {long_u}\n"
            f"📐 Interactive Proof Archive: https://min7014.github.io/mathedu/video_board.html?slug={slug}&lang=en\n"
            f"🔔 Subscribe @min7014_ai: {SUB_CONFIRM_URL}\n"
            f"[ID: {slug}_HYBS_{lc.upper()}] #Shorts #VisualProof #GeometryProof #MathPuzzle"
            if is_en
            else f"🎬 1080p 보조선 해체 풀버전 바로 보기: {long_u}\n"
            f"📐 동적 기하 실험실 & 원문 PDF: https://min7014.github.io/mathedu/video_board.html?slug={slug}\n"
            f"🔔 도형 직관 채널 @min7014_ai 구독: {SUB_CONFIRM_URL}\n"
            f"[ID: {slug}_HYBS_{lc.upper()}] #Shorts #시각적증명 #도형보조선 #수학퀴즈"
        )
        tags = ["Shorts", "Math Puzzle", "Visual Math", "Geometry Proof"] if is_en else ["Shorts", "수학쇼츠", "시각적증명", "보조선"]
        comment = (
            f"{bp['comment_quiz_en'] if is_en else bp['comment_quiz_ko']}\n\n"
            f"🎬 1080p Full Video: {long_u}\n🔔 {SUB_CONFIRM_URL}"
            if is_en
            else f"{bp['comment_quiz_ko']}\n\n🎬 1080p 풀버전: {long_u}\n🔔 {SUB_CONFIRM_URL}"
        )
        locs = {
            "ko": {"title": str(bp["short_title_ko"]), "description": raw_d},
            "en": {"title": str(bp["short_title_en"]), "description": raw_d},
        }
        return _finalize_payload(vmaker, raw_t, raw_d, tags, lc, locs, None, comment, bound_url)

    if kind == "std":
        meta_all = _read_json(YT_PKG_DIR / f"{slug}_youtube_meta.json")
        meta = meta_all.get(lc) or meta_all.get("ko") or ((sdoc.get("youtube_packages") or {}).get(lc) or {})
        raw_t = str(meta.get("title") or sdoc.get("title_en" if is_en else "title") or slug)
        raw_d = str(meta.get("description") or f"📐 Visual Math Proof ({slug})\n📄 PDF: {pdf_url}\n🔔 {SUB_CONFIRM_URL}")
        tags = list(meta.get("tags") or (finance.HIGH_RPM_KEYWORDS_EN if is_en else finance.HIGH_RPM_KEYWORDS_KO))
        locs = {}
        for loc_lc in ("ko", "en", "ja", "zh-CN", "es", "fr", "de", "vi"):
            m_loc = meta_all.get(loc_lc)
            if isinstance(m_loc, dict) and m_loc.get("title"):
                locs[loc_lc] = {"title": str(m_loc["title"]), "description": str(m_loc.get("description") or raw_d)}
        quiz_line = str(meta.get("quiz_comment") or (sdoc.get("viral_hooks") or {}).get("quiz_en" if is_en else "quiz_ko") or "")
        board_u = f"https://min7014.github.io/mathedu/video_board.html?slug={slug}&from=yt_comment"
        marathon_u = f"https://www.youtube.com/watch?v={video_id}&list={UPLOADS_PLAYLIST_ID}"
        comment = (
            f"{quiz_line}\n\n"
            f"▶️ Continuous Full-Course Marathon Playlist: {marathon_u}\n"
            f"🔔 Subscribe in 1 Click: {SUB_CONFIRM_URL}\n"
            f"📐 Interactive GeoGebra & Original PDF: {board_u}&lang=en"
            if is_en
            else f"{quiz_line}\n\n"
            f"▶️ 전 강의 무중단 연속 정주행: {marathon_u}\n"
            f"🔔 @min7014_ai 1초 무료 구독하기: {SUB_CONFIRM_URL}\n"
            f"📐 원본 PDF & 동적 기하 직접 조작: {board_u}"
        )
        thumb_p = YT_PKG_DIR / f"{slug}_{lc}_thumb.png"
        return _finalize_payload(vmaker, raw_t, raw_d, tags, lc, locs, thumb_p, comment, bound_url)

    ko_t, en_t = vmaker.split_bilingual_title(str(sdoc.get("title") or slug))
    title_base = (sdoc.get("title_en") or en_t or ko_t) if is_en else ko_t
    clean_t = vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(title_base), max_len=38 if is_en else 34, lang=lc)
    board_u = f"https://min7014.github.io/mathedu/video_board.html?slug={slug}"
    std_yt_u = str((sdoc.get("youtube_urls") or {}).get(lc) or (sdoc.get("youtube_urls") or {}).get("ko") or SUB_CONFIRM_URL)
    if "youtu.be/" in std_yt_u:
        _fid = _extract_yt_id(std_yt_u)
        if _fid:
            std_yt_u = f"https://www.youtube.com/watch?v={_fid}&list={UPLOADS_PLAYLIST_ID}"

    if kind == "qcl":
        raw_t = (
            f"❓ [Question-Asking Math] {clean_t} — Socratic Visual Proof! | @min7014_ai"
            if is_en
            else f"❓ [질문하는 수학 수업] {clean_t} — 스스로 발문하고 발견하는 시각적 증명! | @min7014_ai"
        )
        raw_d = (
            f"❓ [Question-Asking Classroom Edition] {vmaker.latex_to_unicode_title(title_base)} [ID: {slug}_Q_{lc.upper()}]\n\n"
            f"Phase 1: Pause and hypothesize the invariant & auxiliary line before revealing the proof.\n"
            f"Phase 2: Verify visually with step-by-step dynamic spotlights.\n\n"
            f"🎬 Full 1080p Proof: {std_yt_u}\n"
            f"👉 Interactive Question Lab: {board_u}&mode=question&lang=en\n"
            f"📄 Original Resource: {web_url}\n🔔 Subscribe: {SUB_CONFIRM_URL}\n"
            f"#VisualProof #SocraticMath #Geometry #mathedu"
            if is_en
            else f"❓ [질문하는 수학 수업 (Question-Asking Classroom Edition)]\n"
            f"주제: {vmaker.latex_to_unicode_title(title_base)} [ID: {slug}_Q_{lc.upper()}]\n\n"
            f"1단계(Phase 1): 핵심 발문과 사고 멈춤 시간(Thinking Pause)을 통해 먼저 스스로 원리와 불변량을 추론합니다.\n"
            f"2단계(Phase 2): 동적 시각 스포트라이트와 함께 왜 정리가 성립하는지 눈으로 확인합니다.\n\n"
            f"🎬 [일반 설명 본편(1080p) 바로 보기]: {std_yt_u}\n"
            f"👉 [질문하는 수업 실험실]: {board_u}&mode=question\n"
            f"📄 [수학자료실 원문]: {web_url}\n🔔 무료 구독: {SUB_CONFIRM_URL}\n"
            f"#질문하는수업 #수학증명 #기하학 #시각적증명 #mathedu"
        )
        tags = ["Socratic Math", "Visual Proof", "Geometry"] if is_en else ["질문하는수업", "수학증명", "기하학", "소크라테스발문", "시각적증명"]
        comment = (
            f"🙋 [Socratic Inquiry] Pause at Phase 1: which auxiliary line or invariant did you spot first? Share below!\n\n"
            f"🔔 Subscribe in 1 Click: {SUB_CONFIRM_URL}\n📐 GeoGebra Lab: {board_u}&mode=question&lang=en"
            if is_en
            else f"🙋 [오늘의 질문하는 수업] 영상을 멈추고 가장 먼저 떠올린 보조선이나 불변량은 무엇이었나요? 댓글로 나눠보세요!\n\n"
            f"🔔 @min7014_ai 1초 구독: {SUB_CONFIRM_URL}\n📐 GeoGebra 실험실: {board_u}&mode=question"
        )
        thumb_p = YT_PKG_DIR / f"{slug}_q_{lc}_thumb.png"
        return _finalize_payload(vmaker, raw_t, raw_d, tags, lc, None, thumb_p, comment, bound_url)

    if kind == "sh":
        smeta_all = _read_json(YT_PKG_DIR / f"{slug}_shorts_meta.json")
        smeta = smeta_all.get(lc) or smeta_all.get("ko") or {}
        raw_t = str(smeta.get("title") or (f"🔥 {clean_t} — 45s Visual Proof #Shorts #Math" if is_en else f"🔥 보조선의 통찰! {clean_t} #Shorts #수학"))
        raw_d = str(smeta.get("description") or f"🎬 Full 1080p: {std_yt_u}\n📐 {board_u}\n🔔 {SUB_CONFIRM_URL}\n[ID: {slug}_SHORT_{lc.upper()}] #Shorts")
        tags = list(smeta.get("tags") or (["Shorts", "VisualProof", "Math"] if is_en else ["Shorts", "수학쇼츠", "시각적증명", "기하학"]))
        quiz_line = str((sdoc.get("viral_hooks") or {}).get("quiz_en" if is_en else "quiz_ko") or "")
        comment = (
            f"{quiz_line}\n\n"
            f"🎬 Watch Full 1080p Visual Proof: {std_yt_u}\n"
            f"🔔 Subscribe @min7014_ai: {SUB_CONFIRM_URL}\n"
            f"📐 Interactive GeoGebra: {board_u}&from=yt_shorts"
            if is_en
            else f"{quiz_line}\n\n"
            f"🎬 1080p 전체 단계별 증명 풀버전 보기:\n👉 {std_yt_u}\n"
            f"🔔 @min7014_ai 1초 무료 구독: {SUB_CONFIRM_URL}\n"
            f"📐 도형 직접 움직여보기 (GeoGebra): {board_u}&from=yt_shorts"
        )
        locs = {}
        for loc_lc in ("ko", "en"):
            if isinstance(smeta_all.get(loc_lc), dict) and smeta_all[loc_lc].get("title"):
                locs[loc_lc] = {"title": str(smeta_all[loc_lc]["title"]), "description": str(smeta_all[loc_lc].get("description") or raw_d)}
        return _finalize_payload(vmaker, raw_t, raw_d, tags, lc, locs, None, comment, bound_url)

    # qsh
    q_yt_u = str((sdoc.get("question_youtube_urls") or {}).get(lc) or std_yt_u)
    qpkg = (sdoc.get("question_shorts_packages") or {}).get(lc) or {}
    raw_t = str(qpkg.get("title") or (
        f"❓ [Question #Shorts] {clean_t} — Spot the Hidden Line! #Shorts"
        if is_en
        else f"❓ [질문형 숏폼] {clean_t} — 어디에 보조선을 그어야 할까? #Shorts"
    ))
    raw_d = (
        f"❓ [Question-Asking #Shorts] [ID: {slug}_SHORT_Q_{lc.upper()}]\n"
        f"🎬 Full 1080p Socratic Proof: {q_yt_u}\n"
        f"👉 GeoGebra Lab: {board_u}&lang=en\n🔔 Subscribe: {SUB_CONFIRM_URL}\n"
        f"#Shorts #VisualProof #SocraticMath #Geometry"
        if is_en
        else f"❓ [질문하는 수학 수업 숏폼] [ID: {slug}_SHORT_Q_{lc.upper()}]\n"
        f"주제: {vmaker.latex_to_unicode_title(title_base)}\n\n"
        f"❓ [1080p 질문하는 수업 풀버전]: {q_yt_u}\n"
        f"🎬 [1080p 일반 설명 본편]: {std_yt_u}\n"
        f"👉 [GeoGebra 실험실]: {board_u}\n🔔 구독: {SUB_CONFIRM_URL}\n"
        f"#Shorts #질문하는수업 #수학숏폼 #기하학 #시각적증명 #mathedu"
    )
    tags = ["Shorts", "QuestionMath", "VisualProof"] if is_en else ["Shorts", "질문하는수업", "수학숏폼", "기하학", "시각적증명"]
    comment = (
        f"🙋 [Socratic Inquiry Challenge] Which auxiliary line did you spot first?\n\n"
        f"❓ Full 1080p Lesson: {q_yt_u}\n🔔 Subscribe: {SUB_CONFIRM_URL}\n📐 Lab: {board_u}&lang=en"
        if is_en
        else f"🙋 [오늘의 발문 챌린지] 여러분은 어떤 보조선이나 원리를 먼저 떠올리셨나요? 댓글로 남겨보세요!\n\n"
        f"❓ 1080p 질문하는 수업 풀버전:\n👉 {q_yt_u}\n"
        f"🔔 @min7014_ai 1초 구독: {SUB_CONFIRM_URL}\n📐 GeoGebra 실험실: {board_u}"
    )
    return _finalize_payload(vmaker, raw_t, raw_d, tags, lc, None, None, comment, bound_url)


def _fetch_rss_entries() -> list[dict]:
    import xml.etree.ElementTree as ET
    entries = []
    req = urllib.request.Request(YOUTUBE_RSS_URL, headers={"User-Agent": "Mozilla/5.0"})
    raw = urllib.request.urlopen(req, timeout=15).read()
    root = ET.fromstring(raw)
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "yt": "http://www.youtube.com/xml/schemas/2015",
        "media": "http://search.yahoo.com/mrss/",
    }
    for entry in root.findall("atom:entry", ns):
        vid_el = entry.find("yt:videoId", ns)
        t_el = entry.find("atom:title", ns)
        d_el = entry.find("media:group/media:description", ns)
        if vid_el is not None and t_el is not None:
            vid_id = str(vid_el.text or "").strip()
            if vid_id:
                entries.append({
                    "video_id": vid_id,
                    "title": str(t_el.text or "").strip(),
                    "description": str(d_el.text or "").strip() if d_el is not None else "",
                })
    return entries


def _enqueue_detected_entries(entries: list[dict], state: dict, vmaker) -> int:
    blocked_ids = set()
    try:
        blocked_ids = set(vmaker.get_deleted_video_ids_set())
    except Exception:
        pass
    completed = set(state.get("completed_rewrites") or [])
    pending = state.setdefault("pending_rewrites", {})
    newly_queued = 0

    for ent in entries:
        vid = ent["video_id"]
        if not vid or vid in blocked_ids or vid in completed or vid in pending:
            continue
        spec = match_channel_video_to_local_spec(
            vid, ent["title"], ent["description"], pending_map=pending, completed_ids=completed
        )
        if not spec:
            continue
        _bind_spec_url_to_local_json(spec, vid)
        pending[vid] = {
            "spec": spec,
            "title_raw": ent["title"][:120],
            "snippet_done": False,
            "thumb_done": bool(spec.get("is_short")),
            "comment_done": False,
            "detected_at": datetime.now().isoformat(timespec="seconds"),
        }
        newly_queued += 1
        print(f"📥 [Manual Upload Detected -> Queued] {vid} | {spec['kind']} | {ent['title'][:55]}", flush=True)
    return newly_queued


def _is_quota_error(exc: Exception) -> bool:
    s = str(exc)
    return any(tok in s for tok in ("quotaExceeded", "rateLimitExceeded", "uploadLimitExceeded"))


def _apply_pending_rewrite(yt, tok_path, vid: str, entry: dict, vmaker) -> tuple[bool, bool]:
    """단일 대기 영상을 재작성합니다. 반환값: (completed_all, quota_hit)"""
    from googleapiclient.http import MediaFileUpload

    spec = entry["spec"]
    payload = build_rewrite_payload(spec, vid)
    if not payload:
        entry["snippet_done"] = entry["thumb_done"] = entry["comment_done"] = True
        return True, False

    if not entry.get("snippet_done"):
        body = {
            "id": vid,
            "snippet": {
                "title": payload["title"],
                "description": payload["description"],
                "tags": payload["tags"],
                "categoryId": payload["categoryId"],
                "defaultLanguage": payload["defaultLanguage"],
                "defaultAudioLanguage": payload["defaultAudioLanguage"],
            },
        }
        parts = "snippet"
        if payload.get("localizations"):
            body["localizations"] = payload["localizations"]
            parts = "snippet,localizations"
        try:
            yt.videos().update(part=parts, body=body).execute()
            entry["snippet_done"] = True
        except Exception as exc:
            if _is_quota_error(exc):
                if tok_path:
                    vmaker.mark_token_quota_exhausted(tok_path, 900)
                vmaker._LAST_UPLOAD_QUOTA_BLOCKED = True
                return False, True
            if parts != "snippet":
                try:
                    body.pop("localizations", None)
                    yt.videos().update(part="snippet", body=body).execute()
                    entry["snippet_done"] = True
                except Exception as exc2:
                    if _is_quota_error(exc2):
                        if tok_path:
                            vmaker.mark_token_quota_exhausted(tok_path, 900)
                        vmaker._LAST_UPLOAD_QUOTA_BLOCKED = True
                        return False, True
                    return False, False
            else:
                return False, False

    if not entry.get("thumb_done"):
        th_str = str(payload.get("thumb_path") or "").strip()
        if th_str and Path(th_str).exists() and not spec.get("is_short"):
            try:
                yt.thumbnails().set(
                    videoId=vid,
                    media_body=MediaFileUpload(th_str, mimetype="image/png", resumable=False),
                ).execute()
                entry["thumb_done"] = True
            except Exception as exc:
                if _is_quota_error(exc):
                    if tok_path:
                        vmaker.mark_token_quota_exhausted(tok_path, 900)
                    vmaker._LAST_UPLOAD_QUOTA_BLOCKED = True
                    return False, True
                entry["thumb_done"] = True
        else:
            entry["thumb_done"] = True

    if not entry.get("comment_done"):
        cmt = str(payload.get("top_comment") or "").strip()
        if not cmt:
            entry["comment_done"] = True
        else:
            try:
                yt.commentThreads().insert(
                    part="snippet",
                    body={"snippet": {"videoId": vid, "topLevelComment": {"snippet": {"textOriginal": cmt}}}},
                ).execute()
                entry["comment_done"] = True
            except Exception as exc:
                if _is_quota_error(exc):
                    if tok_path:
                        vmaker.mark_token_quota_exhausted(tok_path, 900)
                    vmaker._LAST_UPLOAD_QUOTA_BLOCKED = True
                    return False, True
                entry["comment_done"] = True

    done = bool(entry.get("snippet_done") and entry.get("thumb_done") and entry.get("comment_done"))
    return done, False


def _send_telegram_summary(completed_items: list[dict], pending_left: int) -> None:
    if not completed_items:
        return
    lines = [
        f"✨ [Policy 89 수동 업로드 자동 재작성 완료: {len(completed_items)}편]",
        "• 제목 · 전체 설명란 · 챕터 · 태그 · 썸네일 · 첫 댓글(5초 퀴즈) · 홈페이지 연결 완료",
    ]
    for it in completed_items[:6]:
        lines.append(f"  - [{it['kind'].upper()}] {it['title'][:38]} ➔ {it['url']}")
    if pending_left > 0:
        lines.append(f"• 잔여 재작성 대기: {pending_left}편 (다음 웨이브/쿼터 리셋 즉시 자동 처리)")
    msg = "\n".join(lines)
    try:
        subprocess.run(
            [sys.executable, "-X", "utf8", str(ROOT_DIR / "mathedu_telegram_bridge.py"), "--reply", msg],
            cwd=str(ROOT_DIR),
            capture_output=True,
            timeout=30,
        )
    except Exception:
        pass


def sync_and_rewrite_manual_uploads(max_rewrites: int = 40, notify_telegram: bool = True) -> dict:
    """
    [Stage A] 0-쿼터 RSS 스캔으로 수동 업로드를 감지·바인딩하고 대기 폴더에서 즉시 정리합니다.
    [Stage B] API 가용 시 최근 업로드 목록(최대 150편) 추가 스캔 후 Priority #0로 일괄 재작성합니다.
    """
    import min7014_video_maker as vmaker

    state = load_rewrite_state()
    pending = state["pending_rewrites"]
    rss_detected = 0

    try:
        rss_entries = _fetch_rss_entries()
        rss_detected = _enqueue_detected_entries(rss_entries, state, vmaker)
    except Exception as exc:
        print(f"⚠️ [Manual Rewrite RSS Notice] {exc}", flush=True)

    api_detected = 0
    yt, tok_path = vmaker.get_available_youtube_upload_service()
    if yt is None:
        save_rewrite_state(state)
        if rss_detected > 0:
            try:
                vmaker.update_video_catalog()
            except Exception:
                pass
            prepare_manual_upload_folders()
        return {
            "status": "queued_for_quota_reset" if pending else "no_quota_no_pending",
            "rss_detected": rss_detected,
            "api_detected": 0,
            "rewritten_count": 0,
            "pending_count": len(pending),
            "completed_total": len(state["completed_rewrites"]),
        }

    # Stage B-1: API 업로드 재생목록 최대 3페이지(150개) 스캔 (수동 15~50개 동시 업로드 포착)
    try:
        page_token = None
        api_entries = []
        for _ in range(3):
            resp = yt.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=UPLOADS_PLAYLIST_ID,
                maxResults=50,
                pageToken=page_token,
            ).execute()
            for item in resp.get("items", []):
                vid = str((item.get("contentDetails") or {}).get("videoId") or "").strip()
                sn = item.get("snippet") or {}
                if vid:
                    api_entries.append({
                        "video_id": vid,
                        "title": str(sn.get("title") or ""),
                        "description": str(sn.get("description") or ""),
                    })
            page_token = resp.get("nextPageToken")
            if not page_token:
                break
        api_detected = _enqueue_detected_entries(api_entries, state, vmaker)
    except Exception as exc:
        if _is_quota_error(exc):
            if tok_path:
                vmaker.mark_token_quota_exhausted(tok_path, 900)
            vmaker._LAST_UPLOAD_QUOTA_BLOCKED = True
            save_rewrite_state(state)
            if rss_detected > 0:
                prepare_manual_upload_folders()
            return {
                "status": "queued_for_quota_reset",
                "rss_detected": rss_detected,
                "api_detected": 0,
                "rewritten_count": 0,
                "pending_count": len(pending),
                "completed_total": len(state["completed_rewrites"]),
            }

    # Stage B-2: 우선순위별 재작성 (MC -> HYB -> STD -> QCL -> HYBS -> QSH -> SH)
    ordered_pending = sorted(
        list(pending.items()),
        key=lambda kv: (KIND_PRIORITY.get(kv[1].get("spec", {}).get("kind", "sh"), 9), kv[0]),
    )
    newly_completed = []
    quota_hit = False

    for vid, entry in ordered_pending[: max(1, int(max_rewrites))]:
        done, q_hit = _apply_pending_rewrite(yt, tok_path, vid, entry, vmaker)
        if q_hit:
            quota_hit = True
            break
        if done:
            spec = entry["spec"]
            url = _bind_spec_url_to_local_json(spec, vid)
            state["completed_rewrites"].append(vid)
            pending.pop(vid, None)
            newly_completed.append({
                "video_id": vid,
                "kind": spec["kind"],
                "title": entry.get("title_raw") or vid,
                "url": url,
            })
            print(f"✅ [Policy 89 Rewrite Complete] {vid} ({spec['kind']}) -> {url}", flush=True)

    save_rewrite_state(state)
    if rss_detected > 0 or api_detected > 0 or newly_completed:
        try:
            vmaker.update_video_catalog()
        except Exception:
            pass
        prepare_manual_upload_folders()

    if notify_telegram and newly_completed:
        _send_telegram_summary(newly_completed, len(pending))

    return {
        "status": "quota_exhausted_partial" if quota_hit else "ok",
        "rss_detected": rss_detected,
        "api_detected": api_detected,
        "rewritten_count": len(newly_completed),
        "pending_count": len(pending),
        "completed_total": len(state["completed_rewrites"]),
        "rewritten_items": newly_completed,
    }


def get_manual_upload_status() -> dict:
    st = load_rewrite_state()
    folder_counts = {}
    for sub in SUBFOLDER_NAMES:
        p = READY_MANUAL_DIR / sub
        folder_counts[sub] = len(list(p.glob("*.mp4"))) if p.exists() else 0
    return {
        "ready_dir": str(READY_MANUAL_DIR),
        "folder_counts": folder_counts,
        "total_ready": sum(folder_counts.values()),
        "pending_rewrites": len(st.get("pending_rewrites") or {}),
        "completed_rewrites": len(st.get("completed_rewrites") or []),
        "updated_at": st.get("updated_at") or "",
    }


def format_status_message(res: dict | None = None) -> str:
    st = get_manual_upload_status()
    fc = st["folder_counts"]
    lines = [
        "📂 [Policy 89 수동 업로드 & 자동 재작성 현황]",
        f"• 대기 폴더: `{st['ready_dir']}` (총 {st['total_ready']}편 · 추가 디스크 0바이트)",
        f"  - ① 장편 마스터클래스: {fc['01_장편_마스터클래스']}편",
        f"  - ② 기하통찰 하이브리드: {fc['02_기하통찰_하이브리드']}편",
        f"  - ③ 1080p 시각증명 본편: {fc['03_1080p_시각증명_본편']}편",
        f"  - ④ 시각증명 쇼츠: {fc['04_시각증명_쇼츠']}편",
        f"• 재작성 대기 큐: {st['pending_rewrites']}편 | 누적 자동 재작성 완료: {st['completed_rewrites']}편",
    ]
    if isinstance(res, dict):
        lines.append(
            f"• 이번 동기화: status={res.get('status')} | RSS감지={res.get('rss_detected', 0)} | "
            f"API감지={res.get('api_detected', 0)} | 재작성완료={res.get('rewritten_count', 0)}"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Policy 89 Manual Upload Folder & Priority-0 Rewriter")
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("prepare")
    sub.add_parser("status")
    p_sync = sub.add_parser("sync")
    p_sync.add_argument("--max-rewrites", type=int, default=40)
    p_sync.add_argument("--no-telegram", action="store_true")

    args = parser.parse_args()
    if args.cmd == "prepare":
        out = prepare_manual_upload_folders()
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    if args.cmd == "sync":
        out = sync_and_rewrite_manual_uploads(
            max_rewrites=args.max_rewrites,
            notify_telegram=not args.no_telegram,
        )
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    print(format_status_message())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
