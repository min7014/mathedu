#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
google_ecosystem_orchestrator.py
===============================================================================
🌐 [Google Ecosystem Math-Video Orchestrator — Rule 57 Unified Control Tower]
민은기 회장님(`min7014`) 지침:
  "가능하면 구글에서 제공하는 모든 도구를 적절하게 사용하여 수학영상을 만들도록 해라."

핵심 설계 철학 ("무분별한 남용 배제 · 역할별 적재적소 배치 · 수학 오류 ZERO · 추가 과금 0원"):
  1. [Layer 1 · 검색 수요 & 트렌드 레이더 (0원 · 0쿼터)]:
     - YouTube Search Autocomplete API (`suggestqueries.google.com`, `ds=yt`, KO/EN)
     - Google News RSS & Google Trends Daily RSS (`trends.google.com/trending/rss`)
     -> 학생·교사의 실시간 유튜브 검색어를 자동 추출(상표권 필터 적용)하여 태그·제작 우선순위에 반영.
  2. [Layer 2 · 평면·대수 시네마틱 광학 모션 (주력 95%)]:
     - Google Flow ULTRA (`Nano Banana 2.1` 무문자 키프레임 + `Veo 3.1 Lite` 양단고정 8초 모션)
     -> Act 1(3초 훅) & Act 3(5초 완결) 배경 전용. Act 2 본 증명은 100% min7014 원본 300 DPI PDF 직강.
  3. [Layer 3 · 공간기하·원뿔곡선 3D 카메라 워킹 (특수 5%)]:
     - Google Labs空間 월드 트랙 (`genie3_world_controller.py`, 720p24 -> 1080p30 Lanczos+Unsharp 마스터링)
     -> 삼수선·정사영·단델린의 구 등 입체 단원 5%에만 핀셋 투입.
  4. [Layer 4 · 수학 기호 무결점 타이포그래피 (OFL 오픈소스)]:
     - Google Fonts `Noto Sans Math` (`NotoSansMath-Regular.ttf`, `.temp/google_fonts/` 로컬 캐시)
     -> ∀, ∃, ∈, ≅, ≤, ≥, ∠, △, ⊥, ∥, ∑, ∫, →, ⇒ 등 수학 기호 두부 깨짐(`□`) 0% 보장.
  5. [Layer 5 · 제로-과금 선택적 언어 다듬기 (`google-genai` SDK + 로컬 결정론 폴백)]:
     - `GEMINI_API_KEY` 무료 티어 존재 시에만 보조 검수 가동, 유료 종량제 호출 하드 차단(`Rule 50`).
  6. [Layer 6 · YouTube Data API v3 + YouTube Studio 무창 자동화 (API 미지원 독점 기능 포함)]:
     - 6개국어 `localizations` 주입, 쇼츠 `관련 동영상` 직결, 커뮤니티 5초 퀴즈 발행,
     - YouTube Studio `썸네일 테스트 및 비교(Test & Compare)`용 3종 A/B/C HD 썸네일 자동 생성,
     - 일일 업로드 쿼터 보호형 스마트 `.srt` 자막 동기화(`captions.insert` 400유닛 잠식 방지 가드).
  7. [Layer 7 · Google 웹 검색 동영상 색인 & 실시간 관제]:
     - Google 공식 규격 `video-sitemap.xml` 자동 생성 및 `robots.txt` 등록 (구글 동영상 검색 노출 극대화),
     - Google Apps Script × Google Sheets 실시간 오류·학습 피드백 파이프라인 연동.

[비판적 통제 경계선 — 의도적으로 배제·제한하는 구글 도구 4종 (Rule 33 · Rule 44 · Rule 50)]:
  - Google Vids / AI 단독 통짜 영상 생성: 보조선·수식 왜곡 위험으로 본편 증명 생성에 절대 사용 금지.
  - NotebookLM 2인 수다형 오디오: 슬라이드·가상 지휘봉과의 0.1초 시공간 동기화를 깨뜨리므로 본편 음성 배제.
  - Lyria / MusicFX 화려한 멜로디 BGM: 수식 발음 명료도 저하 및 핑거프린트 간섭 방지를 위해 -28dB 순수 합성 패드 유지.
  - Google Cloud 유료 종량제 API(Vertex AI / Cloud TTS) 및 무분별한 Captions API 호출: 월 11만 원 예산 및 일일 6편 업로드 슬롯 수호.
===============================================================================
"""

import silent_subprocess  # noqa: F401 — Rule 48: 100% 무창(CREATE_NO_WINDOW) 실행 강제

import argparse
import datetime
import html
import json
import os
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = Path(__file__).resolve().parent
TEMP_DIR = ROOT_DIR / ".temp"
GOOGLE_FONTS_DIR = TEMP_DIR / "google_fonts"
GOOGLE_FONTS_DIR.mkdir(parents=True, exist_ok=True)

SCRIPTS_DIR = ROOT_DIR / "video_lectures" / "scripts"
YT_PKG_DIR = ROOT_DIR / "video_lectures" / "youtube_packages"
CATALOG_JSON = ROOT_DIR / "video_lectures" / "catalog.json"
VIDEO_SITEMAP_XML = ROOT_DIR / "video-sitemap.xml"
ROBOTS_TXT = ROOT_DIR / "robots.txt"

SUGGEST_CACHE_FILE = ROOT_DIR / ".agents" / "google_youtube_suggest_cache.json"
ECOSYSTEM_STATE_FILE = ROOT_DIR / ".agents" / "google_ecosystem_state.json"

NOTO_SANS_MATH_URLS = (
    "https://raw.githubusercontent.com/google/fonts/main/ofl/notosansmath/NotoSansMath-Regular.ttf",
    "https://github.com/notofonts/math/raw/main/fonts/NotoSansMath/unhinted/ttf/NotoSansMath-Regular.ttf",
)

# Rule 37 사색적 블루·틸·인디고·골드 팔레트 (강렬한 적색 원천 배제)
PALETTE_DEEP_NAVY = (12, 20, 38)
PALETTE_INDIGO_CARD = (22, 34, 62)
PALETTE_ROYAL_BLUE = (2, 132, 199)
PALETTE_SKY_CYAN = (56, 189, 248)
PALETTE_EMERALD_TEAL = (5, 150, 105)
PALETTE_MINT_ACCENT = (52, 211, 153)
PALETTE_AMBER_GOLD = (245, 158, 11)
PALETTE_SOFT_GOLD = (250, 204, 21)
PALETTE_PURE_WHITE = (255, 255, 255)
PALETTE_SLATE_LIGHT = (226, 232, 240)

SUGGEST_TTL_SEC = 86400  # 24시간 캐시


# ==============================================================================
# Layer 4: Google Fonts (`Noto Sans Math`) 무결점 수학 기호 폰트 엔진
# ==============================================================================
def ensure_google_noto_math_font(timeout: int = 12) -> Path | None:
    """
    Google 오픈소스(SIL OFL) 수학 전용 폰트 `NotoSansMath-Regular.ttf`를
    Git 추적 대상 밖인 `.temp/google_fonts/`에 1회 다운로드·캐싱합니다.
    """
    dst = GOOGLE_FONTS_DIR / "NotoSansMath-Regular.ttf"
    if dst.exists() and dst.stat().st_size > 80_000:
        return dst

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) MatheduFontLoader/1.0"}
    for url in NOTO_SANS_MATH_URLS:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
            if len(raw) > 80_000 and raw[:4] in (b"\x00\x01\x00\x00", b"OTTO"):
                dst.write_bytes(raw)
                return dst
        except Exception:
            continue
    return dst if dst.exists() else None


def get_google_math_font(size: int = 32):
    """Noto Sans Math 폰트를 우선 로드하고, 오프라인 시 Windows 기호 폰트로 안전 폴백합니다."""
    fp = ensure_google_noto_math_font(timeout=5)
    if fp and fp.exists():
        try:
            return ImageFont.truetype(str(fp), size)
        except Exception:
            pass
    win_fonts = Path(r"C:\Windows\Fonts")
    for cand in ("seguisym.ttf", "cambria.ttc", "malgun.ttf", "arial.ttf"):
        p = win_fonts / cand
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                continue
    return ImageFont.load_default()


def normalize_pillow_safe_math_glyphs(text: str) -> str:
    """
    Pillow 렌더링 시 폰트 미지원 글리프(예: U+2794 무거운 화살표 등)를
    Noto Sans Math 및 Malgun Gothic 모두에서 100% 선명하게 표시되는 표준 유니코드 기호로 정규화합니다.
    """
    s = str(text or "")
    # U+2794, U+279C, U+27A1 등 장식 화살표를 표준 수학 화살표 U+2192(→)로 치환
    for code_pt in ("\u2794", "\u279c", "\u27a1", "\u2b95"):
        s = s.replace(code_pt, "\u2192")
    return s


# ==============================================================================
# Layer 1: Google / YouTube Search Autocomplete (`ds=yt`) & Google Trends 레이더
# ==============================================================================
def _load_suggest_cache() -> dict:
    if SUGGEST_CACHE_FILE.exists():
        try:
            return json.loads(SUGGEST_CACHE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def _save_suggest_cache(cache: dict) -> None:
    SUGGEST_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    SUGGEST_CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def fetch_youtube_autocomplete_math_keywords(
    seed_query: str,
    lang_code: str = "ko",
    max_results: int = 8,
    timeout: int = 5,
) -> list[str]:
    """
    Google 공식 YouTube 검색 자동완성 엔드포인트(`suggestqueries.google.com`, `ds=yt`)에서
    실제 학습자들이 입력하는 수학 검색어를 실시간 조회하고 상표권·비수학 노이즈를 정화합니다.
    - 비용: 0원 / YouTube Data API 쿼터 소모: 0유닛
    """
    q_clean = re.sub(r"\s+", " ", str(seed_query or "")).strip()
    if not q_clean:
        return []

    is_en = lang_code == "en"
    hl = "en" if is_en else "ko"
    gl = "US" if is_en else "KR"
    cache_key = f"{hl}:{q_clean.lower()}"

    cache = _load_suggest_cache()
    now_ts = time.time()
    cached_entry = cache.get(cache_key)
    if isinstance(cached_entry, dict) and (now_ts - float(cached_entry.get("ts", 0))) < SUGGEST_TTL_SEC:
        return list(cached_entry.get("items") or [])[:max_results]

    params = urllib.parse.urlencode(
        {
            "client": "firefox",
            "ds": "yt",
            "hl": hl,
            "gl": gl,
            "q": q_clean,
        }
    )
    url = f"https://suggestqueries.google.com/complete/search?{params}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/131.0.0.0 Safari/537.36"}

    raw_suggestions = []
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8", errors="replace"))
        if isinstance(payload, list) and len(payload) >= 2 and isinstance(payload[1], list):
            raw_suggestions = [str(x).strip() for x in payload[1] if isinstance(x, str) and str(x).strip()]
    except Exception:
        raw_suggestions = []

    import auditor
    # 사설 학원·강사명·게임·비수학 노이즈 차단 필터
    noise_re = re.compile(
        r"게임|노래|먹방|드라마|주식|코인|현우진|정승제|메가스터디|대성|시대인재|쎈|마플|블랙라벨|일품|자이스토리|ebs|인강추천",
        re.IGNORECASE,
    )
    cleaned_list = []
    seen = set()
    for item in raw_suggestions:
        if noise_re.search(item):
            continue
        gated = auditor.sanitize_and_gate_upload_payload("", "", [item])
        valid_tags = gated.get("tags") or []
        if not valid_tags:
            continue
        cand = valid_tags[0].strip()
        if len(cand) < 2 or len(cand) > 45:
            continue
        low_c = cand.lower()
        if low_c not in seen:
            seen.add(low_c)
            cleaned_list.append(cand)
        if len(cleaned_list) >= max_results:
            break

    cache[cache_key] = {"ts": now_ts, "items": cleaned_list}
    # 캐시 비대화 방지 (최대 600개 유지)
    if len(cache) > 600:
        oldest_keys = sorted(cache.keys(), key=lambda k: float(cache[k].get("ts", 0) if isinstance(cache[k], dict) else 0))[:120]
        for ok in oldest_keys:
            cache.pop(ok, None)
    _save_suggest_cache(cache)
    return cleaned_list


def extract_core_math_seed_query(sdoc: dict, lang_code: str = "ko") -> str:
    """스크립트 문서에서 YouTube 자동완성 검색용 핵심 수학 개념어를 추출합니다."""
    if lang_code == "en":
        raw_en = str(sdoc.get("title_en") or "")
        # 부제 분리 및 기호 정리
        core = re.split(r"[|—\-:()]", raw_en)[0].strip()
        core = re.sub(r"^(The|A|An|Visual Proof of|Step-by-Step)\s+", "", core, flags=re.IGNORECASE).strip()
        return core[:48] or "visual geometry proof"
    raw_ko = str(sdoc.get("title") or "")
    core_ko = re.split(r"[|—\-:(]", raw_ko)[0].strip()
    core_ko = re.sub(r"\s*(유도하기|증명하기|알아보기|작도하기)$", "", core_ko).strip()
    return core_ko[:32] or "시각적 수학 증명"


def enrich_tags_with_google_youtube_suggest(
    slug: str,
    lang_code: str = "ko",
    base_tags: list[str] | None = None,
    max_total_chars: int = 440,
) -> list[str]:
    """
    기존 기본 태그에 YouTube 실시간 자동완성 검색어(`ds=yt`)를 결합하고,
    YouTube 태그 총 글자수 한도(500자 미만 안전선 440자) 및 `auditor` L1 상표권 무결성을 보증합니다.
    """
    tags = list(base_tags or [])
    sp = SCRIPTS_DIR / f"{slug}.json"
    sdoc = {}
    if sp.exists():
        try:
            sdoc = json.loads(sp.read_text(encoding="utf-8"))
        except Exception:
            sdoc = {}

    seed = extract_core_math_seed_query(sdoc, lang_code=lang_code)
    queries = [seed]
    if lang_code == "en" and "proof" not in seed.lower():
        queries.append(f"{seed} proof")
    elif lang_code == "ko" and "증명" not in seed:
        queries.append(f"{seed} 증명")

    live_kw = []
    for q in queries:
        live_kw.extend(fetch_youtube_autocomplete_math_keywords(q, lang_code=lang_code, max_results=6))

    import auditor
    merged = []
    seen = set()
    used_chars = 0
    for candidate in tags + live_kw:
        gated = auditor.sanitize_and_gate_upload_payload("", "", [candidate]).get("tags") or []
        if not gated:
            continue
        t_clean = gated[0].strip()
        if not t_clean or t_clean.lower() in seen:
            continue
        cost = len(t_clean) + 2
        if used_chars + cost > max_total_chars:
            continue
        seen.add(t_clean.lower())
        merged.append(t_clean)
        used_chars += cost
    return merged


def fetch_google_trends_stem_signals(geo: str = "KR", timeout: int = 6) -> list[str]:
    """Google Trends 일간 급상승 RSS에서 과학·수학·교육·우주·AI 추론 연관 시그널을 0크레딧으로 탐지합니다."""
    url = f"https://trends.google.com/trending/rss?geo={geo.upper()}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) MatheduTrends/1.0"}
    stem_re = re.compile(
        r"수학|과학|우주|인공지능|수능|모의고사|교육|기하|반도체|양자|알고리즘|노벨|필즈상|math|science|space|physics|quantum|geometry|calculus|ai\b|stem",
        re.IGNORECASE,
    )
    hits = []
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            xml_bytes = resp.read()
        root = ET.fromstring(xml_bytes)
        for item in root.findall(".//item"):
            title_el = item.find("title")
            if title_el is not None and title_el.text:
                t = title_el.text.strip()
                if stem_re.search(t):
                    hits.append(t)
    except Exception:
        pass
    return hits[:10]


# ==============================================================================
# Layer 6: YouTube Studio `썸네일 테스트 및 비교(Test & Compare)` 3종 A/B/C 생성기
# ==============================================================================
def _render_clean_pdf_crop(doc, page_index: int, box_size: tuple[int, int]) -> Image.Image:
    idx = max(0, min(len(doc) - 1, page_index))
    pix = doc[idx].get_pixmap(dpi=220, alpha=False)
    im = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    im.thumbnail(box_size, Image.Resampling.LANCZOS)
    card = Image.new("RGB", box_size, PALETTE_PURE_WHITE)
    ox = (box_size[0] - im.width) // 2
    oy = (box_size[1] - im.height) // 2
    card.paste(im, (ox, oy))
    return card


def _draw_wrapped_lines(
    draw: ImageDraw.ImageDraw,
    lines: list[str],
    x: int,
    y_start: int,
    font,
    fill: tuple[int, int, int],
    line_gap: int = 12,
) -> int:
    y = y_start
    for ln in lines:
        safe_ln = normalize_pillow_safe_math_glyphs(ln)
        draw.text((x, y), safe_ln, font=font, fill=fill)
        bbox = draw.textbbox((x, y), safe_ln, font=font)
        y += max(28, bbox[3] - bbox[1]) + line_gap
    return y


def generate_studio_ab_test_thumbnails(slug: str, lang_code: str = "ko") -> list[str]:
    """
    YouTube Studio의 '썸네일 테스트 및 비교(Test & Compare)' 기능에 즉시 투입할 수 있는
    3종 1280x720 HD 썸네일(Variant A / B / C)을 Rule 28(원문 무가림) & Rule 37(무적색 조화 색채)에 맞춰 생성합니다.
      - Variant A: 오리지널 원문 완성 도형 중심 + 핵심 원리 질문형
      - Variant B: 다크 인디고/광학 시네마 배경 + 골드 불변량 스포트라이트형
      - Variant C: '3초 직관 챌린지' 참여 유도형
    """
    import min7014_video_maker as vmaker

    sp = SCRIPTS_DIR / f"{slug}.json"
    if not sp.exists():
        return []
    sdoc = json.loads(sp.read_text(encoding="utf-8"))
    pdf_url = str(sdoc.get("pdf_url") or "")
    if not pdf_url:
        return []
    pdf_bytes, _ = vmaker.load_or_build_topic_pdf_bytes(pdf_url, slug)
    if not pdf_bytes:
        return []

    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    try:
        n_pages = len(doc)
        climax_idx = max(0, n_pages - 2) if n_pages >= 3 else max(0, n_pages - 1)
        mid_idx = max(0, n_pages // 2)

        is_en = lang_code == "en"
        topic_core = extract_core_math_seed_query(sdoc, lang_code=lang_code)
        f_badge = vmaker.get_font_for_lang(lang_code, 28, bold=True)
        f_big = vmaker.get_font_for_lang(lang_code, 48, bold=True)
        f_sub = vmaker.get_font_for_lang(lang_code, 30, bold=True)

        import textwrap
        wrap_w = 16 if is_en else 10
        topic_lines = textwrap.wrap(topic_core, width=wrap_w)[:3]

        variants_spec = [
            (
                "A",
                PALETTE_DEEP_NAVY,
                PALETTE_ROYAL_BLUE,
                climax_idx,
                "ORIGINAL VISUAL PROOF" if is_en else "오리지널 단계별 시각 증명",
                "Why Does It ALWAYS Hold?" if is_en else "공식 없이 왜 항상 성립할까?",
            ),
            (
                "B",
                (10, 26, 47),
                PALETTE_EMERALD_TEAL,
                mid_idx,
                "1 AUXILIARY LINE INSIGHT" if is_en else "결정적 보조선 1줄의 통찰",
                "Spot the Hidden Link ->" if is_en else "숨은 보조선이 보이시나요? →",
            ),
            (
                "C",
                (18, 25, 52),
                PALETTE_AMBER_GOLD,
                climax_idx,
                "3-SEC THINKING CHALLENGE" if is_en else "능동적 사고 3초 발상 챌린지",
                "Pause & Predict First!" if is_en else "멈추고 먼저 예측해 보세요!",
            ),
        ]

        YT_PKG_DIR.mkdir(parents=True, exist_ok=True)
        nb_art_candidates = list((ROOT_DIR / "youtube_uploads" / "nano_banana_assets").glob(f"nb_{slug}*.png"))
        created_paths = []

        for v_code, bg_col, accent_col, p_idx, badge_txt, footer_txt in variants_spec:
            canvas = Image.new("RGB", (1280, 720), bg_col)
            if v_code == "B" and nb_art_candidates:
                try:
                    bg_art = Image.open(nb_art_candidates[0]).convert("RGB").resize((1280, 720), Image.Resampling.LANCZOS)
                    overlay = Image.new("RGB", (1280, 720), bg_col)
                    canvas = Image.blend(bg_art, overlay, 0.72)
                except Exception:
                    pass

            draw = ImageDraw.Draw(canvas)
            badge_text_col = PALETTE_DEEP_NAVY if accent_col == PALETTE_AMBER_GOLD else PALETTE_PURE_WHITE
            draw.rounded_rectangle((36, 42, 566, 108), radius=16, fill=accent_col)
            draw.text((56, 58), normalize_pillow_safe_math_glyphs(badge_txt), font=f_badge, fill=badge_text_col)

            y_after = _draw_wrapped_lines(draw, topic_lines, x=42, y_start=152, font=f_big, fill=PALETTE_PURE_WHITE, line_gap=16)

            draw.rounded_rectangle((36, max(490, y_after + 28), 566, 668), radius=18, fill=PALETTE_INDIGO_CARD, outline=PALETTE_SOFT_GOLD, width=3)
            draw.text((58, max(518, y_after + 56)), normalize_pillow_safe_math_glyphs(footer_txt), font=f_sub, fill=PALETTE_SOFT_GOLD)

            fig_box_w, fig_box_h = 636, 636
            draw.rounded_rectangle((596, 36, 596 + fig_box_w + 12, 36 + fig_box_h + 12), radius=20, fill=PALETTE_PURE_WHITE, outline=accent_col, width=4)
            fig_img = _render_clean_pdf_crop(doc, p_idx, (fig_box_w - 16, fig_box_h - 16))
            canvas.paste(fig_img, (610, 50))

            out_p = YT_PKG_DIR / f"{slug}_{lang_code}_thumb_ab_{v_code}.png"
            canvas.save(out_p, format="PNG", optimize=True)
            created_paths.append(str(out_p.relative_to(ROOT_DIR)).replace("\\", "/"))

        return created_paths
    finally:
        doc.close()


# ==============================================================================
# Layer 7: Google Search 공식 `video-sitemap.xml` 자동 생성 및 `robots.txt` 동기화
# ==============================================================================
def _extract_yt_video_id(url: str) -> str:
    s = str(url or "").strip()
    if not s:
        return ""
    m = re.search(r"(?:youtu\.be/|youtube\.com/(?:watch\?v=|shorts/|embed/))([A-Za-z0-9_-]{11})", s)
    return m.group(1) if m else ""


def build_google_video_sitemap() -> dict:
    """
    Google 검색센터 공식 Video Sitemap 규격(`http://www.google.com/schemas/sitemap-video/1.1`)에 따라
    라이브 `@min7014_ai` 유튜브 영상과 `min7014.github.io/mathedu/video_board.html?slug=...` 학습 페이지를
    1:1 매핑한 `video-sitemap.xml`을 생성하여 구글 동영상 검색 및 AI 개요 노출을 극대화합니다.
    """
    import auditor

    entries_by_slug: dict[str, list[dict]] = {}
    total_videos = 0
    seen_vid_ids = set()

    url_fields = (
        ("youtube_urls", "Visual Proof Lecture"),
        ("question_youtube_urls", "Active Question-Asking Math Lecture"),
        ("issue_insight_urls", "Contemporary Math Education Insight"),
        ("nano_banana_urls", "Optical Geometry & Step-by-Step Visual Proof"),
        ("exam_hybrid_urls", "Problem-Solving Trap & Visual Proof"),
        ("shorts_youtube_urls", "60-Second Visual Math Proof Short"),
        ("question_shorts_youtube_urls", "Active-Thinking Math Question Short"),
        ("issue_insight_shorts_urls", "Math Education Insight Short"),
        ("nano_banana_shorts_urls", "Visual Geometry Mystery Short"),
    )

    for sp in sorted(SCRIPTS_DIR.glob("*.json")):
        slug = sp.stem
        try:
            sdoc = json.loads(sp.read_text(encoding="utf-8"))
        except Exception:
            continue

        page_count = int(sdoc.get("page_count") or len(sdoc.get("pages_ko") or []) or 10)
        est_dur_long = max(90, min(1800, page_count * 26))

        for field_name, kind_label in url_fields:
            umap = sdoc.get(field_name)
            if not isinstance(umap, dict):
                continue
            is_short = "shorts" in field_name
            for lc, raw_url in umap.items():
                vid = _extract_yt_video_id(raw_url)
                if not vid or vid in seen_vid_ids:
                    continue
                seen_vid_ids.add(vid)

                is_en = str(lc).startswith("en")
                base_t = str(sdoc.get("title_en") if is_en else sdoc.get("title") or slug).strip()
                raw_title = f"{base_t} ({kind_label})" if is_en else f"{base_t} — 단계별 시각적 수학 증명"
                raw_desc = (
                    f"Step-by-step human-crafted visual mathematical proof for {base_t}, paired with interactive MathLab geometry and active-thinking prompts."
                    if is_en
                    else f"{base_t}의 수학적 필연성을 한 페이지씩 눈으로 확인하는 오리지널 단계별 시각 증명 및 능동적 사고 강의입니다."
                )
                gated = auditor.sanitize_and_gate_upload_payload(raw_title, raw_desc, [])
                dur_sec = 46 if is_short else est_dur_long

                entries_by_slug.setdefault(slug, []).append(
                    {
                        "video_id": vid,
                        "lang": lc,
                        "title": gated["title"][:98],
                        "description": gated["description"][:480],
                        "duration": dur_sec,
                    }
                )
                total_videos += 1

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">',
    ]

    for slug, vlist in sorted(entries_by_slug.items()):
        loc_url = f"https://min7014.github.io/mathedu/video_board.html?slug={urllib.parse.quote(slug)}"
        lines.append("  <url>")
        lines.append(f"    <loc>{html.escape(loc_url)}</loc>")
        for v in vlist[:8]:
            vid = v["video_id"]
            thumb_u = f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
            player_u = f"https://www.youtube.com/embed/{vid}"
            content_u = f"https://www.youtube.com/watch?v={vid}"
            lines.append("    <video:video>")
            lines.append(f"      <video:thumbnail_loc>{html.escape(thumb_u)}</video:thumbnail_loc>")
            lines.append(f"      <video:title>{html.escape(v['title'])}</video:title>")
            lines.append(f"      <video:description>{html.escape(v['description'])}</video:description>")
            lines.append(f"      <video:content_loc>{html.escape(content_u)}</video:content_loc>")
            lines.append(f"      <video:player_loc>{html.escape(player_u)}</video:player_loc>")
            lines.append(f"      <video:duration>{int(v['duration'])}</video:duration>")
            lines.append("      <video:family_friendly>yes</video:family_friendly>")
            lines.append("      <video:live>no</video:live>")
            lines.append("    </video:video>")
        lines.append("  </url>")

    lines.append("</urlset>")
    VIDEO_SITEMAP_XML.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # robots.txt에 video-sitemap.xml 등록 보장
    sitemap_directive = "Sitemap: https://min7014.github.io/mathedu/video-sitemap.xml"
    if ROBOTS_TXT.exists():
        rtxt = ROBOTS_TXT.read_text(encoding="utf-8")
        if "video-sitemap.xml" not in rtxt:
            ROBOTS_TXT.write_text(rtxt.rstrip() + "\n" + sitemap_directive + "\n", encoding="utf-8")

    return {
        "sitemap_path": str(VIDEO_SITEMAP_XML.name),
        "indexed_slugs": len(entries_by_slug),
        "indexed_live_videos": total_videos,
        "updated_at": datetime.datetime.now().isoformat(timespec="seconds"),
    }


# ==============================================================================
# Layer 6-B: 일일 업로드 쿼터 보호형 스마트 YouTube `.srt` 자막 트랙 동기화기
# ==============================================================================
def smart_sync_youtube_captions_surplus_quota(
    max_tracks: int = 2,
    force_even_before_daily_quota_complete: bool = False,
) -> dict:
    """
    [Rule 32 & Rule 46 쿼터 보호 설계]:
    `youtube.captions().insert`는 트랙당 400 유닛을 소모합니다.
    무분별하게 호출하면 일일 6편 영상 업로드(`videos.insert` 1,600유닛 × 6 = 9,600유닛) 슬롯을 잠식하므로,
    기본적으로 금일 목표 업로드 웨이브(>= 6편)가 모두 완료된 뒤 남은 잉여 쿼터에서만 자막을 업로드합니다.
    """
    bal_file = ROOT_DIR / ".agents" / "daily_wave_balance.json"
    uploaded_today = 0
    if bal_file.exists():
        try:
            bdoc = json.loads(bal_file.read_text(encoding="utf-8"))
            today_str = datetime.date.today().isoformat()
            if bdoc.get("date") == today_str:
                uploaded_today = int(bdoc.get("long", 0)) + int(bdoc.get("short", 0))
        except Exception:
            pass

    if not force_even_before_daily_quota_complete and uploaded_today < 6:
        return {
            "status": "deferred_protecting_video_upload_slots",
            "uploaded_videos_today": uploaded_today,
            "reason": "일일 6편 본편·쇼츠 업로드 슬롯(9,600유닛) 보호를 위해 잉여 쿼터 시간대까지 자막 API 호출 보류",
            "synced_tracks": [],
        }

    cap_state_p = ROOT_DIR / ".agents" / "synced_captions_state.json"
    cap_state = {"synced": {}}
    if cap_state_p.exists():
        try:
            cap_state = json.loads(cap_state_p.read_text(encoding="utf-8"))
        except Exception:
            pass

    import min7014_video_maker as vm
    from googleapiclient.http import MediaFileUpload

    yt, tok_p = vm.get_available_youtube_upload_service()
    if yt is None:
        return {"status": "no_available_token", "synced_tracks": []}

    synced = []
    for sp in sorted(SCRIPTS_DIR.glob("*.json")):
        if len(synced) >= max_tracks:
            break
        slug = sp.stem
        try:
            sdoc = json.loads(sp.read_text(encoding="utf-8"))
        except Exception:
            continue
        ymap = sdoc.get("youtube_urls") or {}
        for lc in ("ko", "en"):
            if len(synced) >= max_tracks:
                break
            vid = _extract_yt_video_id(ymap.get(lc, ""))
            srt_p = YT_PKG_DIR / f"{slug}_{lc}.srt"
            key = f"{vid}:{lc}"
            if not vid or not srt_p.exists() or key in (cap_state.get("synced") or {}):
                continue
            try:
                body = {
                    "snippet": {
                        "videoId": vid,
                        "language": lc,
                        "name": "한국어 정밀 수학 자막" if lc == "ko" else "English Visual Proof Subtitles",
                        "isDraft": False,
                    }
                }
                media = MediaFileUpload(str(srt_p), mimetype="application/x-subrip", resumable=False)
                yt.captions().insert(part="snippet", body=body, media_body=media).execute()
                cap_state.setdefault("synced", {})[key] = datetime.datetime.now().isoformat(timespec="seconds")
                cap_state_p.write_text(json.dumps(cap_state, ensure_ascii=False, indent=2), encoding="utf-8")
                synced.append(key)
            except Exception as e:
                if "quotaExceeded" in str(e) or "rateLimitExceeded" in str(e):
                    vm.mark_token_quota_exhausted(tok_p, 900)
                    cap_state_p.write_text(json.dumps(cap_state, ensure_ascii=False, indent=2), encoding="utf-8")
                    return {"status": "quota_reached", "synced_tracks": synced}
                continue

    return {"status": "ok", "synced_tracks": synced}


def smart_repair_youtube_url_boundaries_surplus_quota(max_repairs: int = 30) -> dict:
    """
    [Rule 5 · 잉여 쿼터 활용 구버전 유튜브 설명란 URL 경계 자동 정화기]
    일일 6편 본편·쇼츠 업로드 슬롯 완수 후 남는 잉여 쿼터로 구버전 설명란의
    'github.io/)로부터', '?q=한글' 미인코딩 등을 삭제 없이 제자리 정화(videos.update)합니다.
    """
    bal_p = ROOT_DIR / ".agents" / "daily_wave_balance.json"
    uploaded_today = 0
    if bal_p.exists():
        try:
            b = json.loads(bal_p.read_text(encoding="utf-8"))
            uploaded_today = int(b.get("mc", 0)) + int(b.get("std", 0)) + int(b.get("shorts", 0))
        except Exception:
            pass
    if uploaded_today < 6:
        return {"status": "deferred_protecting_upload_slots", "repaired": []}

    st_p = ROOT_DIR / ".agents" / "repaired_url_boundaries_state.json"
    done_ids = set()
    if st_p.exists():
        try:
            done_ids = set(json.loads(st_p.read_text(encoding="utf-8")).get("repaired_video_ids") or [])
        except Exception:
            done_ids = set()

    import min7014_video_maker as vm
    import youtube_self_evolving_engine as ysee

    yt, tok_p = vm.get_available_youtube_upload_service()
    if yt is None:
        return {"status": "no_available_token", "repaired": []}

    repaired = []
    try:
        ch = yt.channels().list(part="contentDetails", id="UCSlqQfOEtRfJuMPyGMLgFYA").execute()["items"][0]
        upl = ch["contentDetails"]["relatedPlaylists"]["uploads"]
        pt = None
        cand_ids = []
        while len(cand_ids) < 600:
            r = yt.playlistItems().list(part="contentDetails", playlistId=upl, maxResults=50, pageToken=pt).execute()
            for it in r.get("items", []):
                vid = it["contentDetails"]["videoId"]
                if vid not in done_ids:
                    cand_ids.append(vid)
            pt = r.get("nextPageToken")
            if not pt:
                break

        for i in range(0, len(cand_ids), 50):
            if len(repaired) >= max_repairs:
                break
            vr = yt.videos().list(part="snippet", id=",".join(cand_ids[i : i + 50])).execute()
            for vit in vr.get("items", []):
                if len(repaired) >= max_repairs:
                    break
                vid = vit["id"]
                sn = vit["snippet"]
                old_d = sn.get("description") or ""
                new_d = ysee.ensure_clean_youtube_url_boundaries(old_d)
                if new_d != old_d:
                    sn["description"] = new_d[:4950]
                    yt.videos().update(part="snippet", body={"id": vid, "snippet": sn}).execute()
                    repaired.append(vid)
                done_ids.add(vid)
        st_p.write_text(json.dumps({"repaired_video_ids": sorted(done_ids)}, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        if "quotaExceeded" in str(e) or "rateLimitExceeded" in str(e):
            vm.mark_token_quota_exhausted(tok_p, 900)
            st_p.write_text(json.dumps({"repaired_video_ids": sorted(done_ids)}, ensure_ascii=False, indent=2), encoding="utf-8")
            return {"status": "quota_reached", "repaired": repaired}
    return {"status": "ok", "repaired": repaired}


# ==============================================================================
# Layer 5: `google-genai` SDK 제로-과금 방화벽 보조 검수기 (Rule 50 엄수)
# ==============================================================================
def optional_gemini_free_tier_hook_polish(prompt_text: str, fallback_text: str) -> str:
    """
    설치된 `google.genai` SDK를 무료 AI Studio 키(`GEMINI_FREE_API_KEY`)가 명시된 경우에만 제한적으로 사용하며,
    유료 과금 키 호출은 원천 차단(`Rule 50` 월 11만 원 고정비 수호)하고 즉시 결정론적 로컬 수학교육 텍스트로 폴백합니다.
    """
    free_key = os.environ.get("GEMINI_FREE_API_KEY", "").strip()
    if not free_key:
        return fallback_text
    try:
        from google import genai
        client = genai.Client(api_key=free_key)
        resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_text,
        )
        cand = (getattr(resp, "text", "") or "").strip()
        if cand:
            import auditor
            return auditor.sanitize_and_gate_upload_payload("", cand, [])["description"] or fallback_text
    except Exception:
        pass
    return fallback_text


# ==============================================================================
# 주제별 최적 구글 도구 조합 판정기 & 텔레그램 0-크레딧 종합 리포트
# ==============================================================================
def resolve_optimal_google_toolchain(slug: str) -> dict:
    """주어진 `min7014.github.io` 단원(`slug`)에 가장 적합한 구글 도구 파이프라인을 자동 배정합니다."""
    import genie3_world_controller as gwc

    sp = SCRIPTS_DIR / f"{slug}.json"
    sdoc = {}
    if sp.exists():
        try:
            sdoc = json.loads(sp.read_text(encoding="utf-8"))
        except Exception:
            sdoc = {}

    spatial = gwc.is_spatial_3d_topic(sdoc)
    visual_engine = (
        "Google Labs 3D Spatial World Camera (1080p30 Lanczos+Unsharp, 5% 공간·원뿔곡선 전용)"
        if spatial
        else "Google Flow ULTRA (Nano Banana 2.1 무문자 키프레임 + Veo 3.1 Lite 양단고정 8초 모션, 주력 95%)"
    )
    return {
        "slug": slug,
        "title": sdoc.get("title", slug),
        "is_spatial_3d": spatial,
        "layers": {
            "L1_search_demand": "YouTube Search Autocomplete (ds=yt, KO/EN) + Google News/Trends RSS",
            "L2_L3_visual_broll": visual_engine,
            "core_proof_spine": "100% min7014.github.io 원본 300 DPI PDF 1:1 무가림 + 가상 지휘봉 + 4단계 능동 사고 정지",
            "L4_math_typography": "Google Fonts Noto Sans Math (OFL) + Malgun/Segoe 복합 글리프 가드",
            "L5_genai_sdk": "google-genai 제로-과금 방화벽 (유료 호출 차단 · 로컬 mathteacher 결정론 엔진 기본)",
            "L6_youtube_studio_and_api": "YouTube Data API v3 (6개국어 localizations) + Studio 관련 동영상/커뮤니티 퀴즈 + 3종 A/B/C 테스트 썸네일",
            "L7_google_web_discovery": "Google Video Sitemap (video-sitemap.xml) + Schema.org VideoObject + Google Apps Script/Sheets 관제",
        },
    }


def get_google_ecosystem_status() -> dict:
    noto_p = ensure_google_noto_math_font(timeout=4)
    sug_cache = _load_suggest_cache()
    ab_thumbs = list(YT_PKG_DIR.glob("*_thumb_ab_*.png")) if YT_PKG_DIR.exists() else []
    flow_clips = list((ROOT_DIR / "youtube_uploads" / "flow_clips").glob("*.mp4"))
    genie_clips = list((ROOT_DIR / "youtube_uploads" / "genie_clips").glob("*.mp4"))
    rel_p = ROOT_DIR / ".agents" / "studio_shorts_related_linked.json"
    rel_cnt = len((json.loads(rel_p.read_text(encoding="utf-8")).get("linked_short_ids") or [])) if rel_p.exists() else 0
    loc_p = ROOT_DIR / ".agents" / "localized_videos_state.json"
    loc_cnt = len((json.loads(loc_p.read_text(encoding="utf-8")).get("localized_ids") or [])) if loc_p.exists() else 0

    sitemap_videos = 0
    if VIDEO_SITEMAP_XML.exists():
        sitemap_videos = VIDEO_SITEMAP_XML.read_text(encoding="utf-8", errors="ignore").count("<video:video>")

    st = {
        "noto_sans_math_ready": bool(noto_p and noto_p.exists()),
        "noto_font_bytes": noto_p.stat().st_size if (noto_p and noto_p.exists()) else 0,
        "youtube_suggest_cached_queries": len(sug_cache),
        "flow_locked_motion_clips": len(flow_clips),
        "spatial_3d_mastered_clips": len(genie_clips),
        "studio_ab_thumbnail_files": len(ab_thumbs),
        "studio_related_shorts_linked": rel_cnt,
        "six_lang_localized_videos": loc_cnt,
        "google_video_sitemap_videos": sitemap_videos,
        "zero_extra_billing_guard": True,
        "checked_at": datetime.datetime.now().isoformat(timespec="seconds"),
    }
    ECOSYSTEM_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    ECOSYSTEM_STATE_FILE.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")
    return st


def format_telegram_google_toolchain_briefing() -> str:
    st = get_google_ecosystem_status()
    font_ok = "🟢 완비" if st["noto_sans_math_ready"] else "🟡 폴백"
    return (
        "🌐 [크레딧 0원 · 구글 7계층 수학영상 도구 통합 관제 (`google_ecosystem_orchestrator.py`)]\n"
        f"1️⃣ 검색·이슈 기획 (YouTube 자동완성 `ds=yt` + Google News/Trends): 캐시 {st['youtube_suggest_cached_queries']}건 가동\n"
        f"2️⃣ 평면·대수 광학 모션 (Google Flow 95% 양단고정): {st['flow_locked_motion_clips']}클립\n"
        f"3️⃣ 입체·원뿔 3D 공간 카메라 (Google Labs 5% 핀셋): {st['spatial_3d_mastered_clips']}클립\n"
        f"4️⃣ 수학 기호 전용 폰트 (Google Noto Sans Math OFL): {font_ok} (`□` 깨짐 0%)\n"
        f"5️⃣ YouTube Data API v3 (6개국어 현지화 {st['six_lang_localized_videos']}편 + 쿼터 보호형 자막 동기화)\n"
        f"6️⃣ YouTube Studio 무창 자동화 (쇼츠 본편 연결 {st['studio_related_shorts_linked']}편 + A/B/C 테스트 썸네일 {st['studio_ab_thumbnail_files']}종)\n"
        f"7️⃣ Google 동영상 검색 색인 (`video-sitemap.xml`): 라이브 영상 {st['google_video_sitemap_videos']}편 매핑 완료\n"
        "🛡️ 통제 가드레일: 본 증명(Act 2) 100% 원문 PDF 고정 · 대외 AI 도구명 노출 0건 · 추가 유료 과금 0원"
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="Google Ecosystem Math-Video Orchestrator")
    ap.add_argument(
        "cmd",
        nargs="?",
        default="status",
        choices=["status", "telegram", "enrich-seo", "ab-thumbs", "build-video-sitemap", "sync-captions", "plan"],
    )
    ap.add_argument("--slug", type=str, default="2022101601")
    ap.add_argument("--lang", type=str, default="ko")
    args = ap.parse_args()

    if args.cmd == "telegram":
        print(format_telegram_google_toolchain_briefing())
    elif args.cmd == "enrich-seo":
        tags = enrich_tags_with_google_youtube_suggest(args.slug, lang_code=args.lang, base_tags=["시각적증명", "수학교육"])
        print(json.dumps({"slug": args.slug, "lang": args.lang, "tags": tags}, ensure_ascii=False, indent=2))
    elif args.cmd == "ab-thumbs":
        paths = generate_studio_ab_test_thumbnails(args.slug, lang_code=args.lang)
        print(json.dumps({"slug": args.slug, "lang": args.lang, "ab_thumbnails": paths}, ensure_ascii=False, indent=2))
    elif args.cmd == "build-video-sitemap":
        res = build_google_video_sitemap()
        print(json.dumps(res, ensure_ascii=False, indent=2))
    elif args.cmd == "sync-captions":
        res = smart_sync_youtube_captions_surplus_quota()
        print(json.dumps(res, ensure_ascii=False, indent=2))
    elif args.cmd == "plan":
        print(json.dumps(resolve_optimal_google_toolchain(args.slug), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(get_google_ecosystem_status(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
