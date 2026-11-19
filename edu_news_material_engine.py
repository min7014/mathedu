#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
edu_news_material_engine.py
===============================================================================
📰 교육 관련 뉴스 레이더 × min7014.github.io 수학 본질 번역 · 수업자료 제작 엔진

[핵심 철학 — Policy 64]:
  "시류를 쫓아가는 것으로 보이기는 하나 인생은 대응이지."
  - 가벼운 시류 영합이 아니라, **불변의 수학적 본질(min7014.github.io 1,113+ 원문 증명·작도)**을
    뿌리에 두고 **오늘의 교육 현장 뉴스(AI 스마트 안경 시험 논란, 서술형·수행평가 확대, AI 디지털교과서,
    고교학점제 기하·미적분, 수리논술 정당화 등)**라는 살아있는 입구로 학생과 교사를 초대합니다.

주요 기능:
  1. 0-크레딧 실시간 교육 뉴스 RSS 스캔 (`scan_live_edu_news`) 및 상표권·비수학 필터링(auditor 연동)
  2. 교육 뉴스 현상 → 수학적 본질 & min7014.github.io 원문 자산 매핑 (`assets/edu_news_materials_db.json`)
  3. 홈페이지 인터랙티브 6단계 디딤돌 수업자료(`board/edunews*.html` + `offline/edunews*.html`) 및
     @min7014_ai 시사×수학교육 통찰 영상 블루프린트(`math_issue_insight_creator.py`) 투트랙 동기화
===============================================================================
"""

import silent_subprocess  # noqa: F401 — Rule 48 완전 무창 실행 강제

import datetime
import html
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent
EDU_NEWS_DB_FILE = ROOT_DIR / "assets" / "edu_news_materials_db.json"
BOARD_DIR = ROOT_DIR / "board"
BOARD_INDEX_FILE = BOARD_DIR / "index.json"

EDU_NEWS_RSS_FEEDS = [
    (
        "kr_edu_assessment",
        "https://news.google.com/rss/search?q=%EA%B5%90%EC%9C%A1+%ED%8F%89%EA%B0%80+OR+%EC%8A%A4%EB%A7%88%ED%8A%B8+%EC%95%88%EA%B2%BD+%EC%8B%9C%ED%97%98+OR+%EC%84%9C%EC%88%A0%ED%98%95+%EC%88%98%ED%95%99+OR+%EC%88%98%ED%96%89%ED%8F%89%EA%B0%80+%EC%88%98%ED%95%99&hl=ko&gl=KR&ceid=KR:ko",
    ),
    (
        "kr_math_classroom",
        "https://news.google.com/rss/search?q=%EC%88%98%ED%95%99%EA%B5%90%EC%9C%A1+OR+%EC%88%98%EB%A6%AC%EB%85%BC%EC%88%A0+OR+%EA%B3%A0%EA%B5%90%ED%95%99%EC%A0%90%EC%A0%9C+%EA%B8%B0%ED%95%98+%EB%AF%B8%EC%A0%81%EB%B6%84+OR+%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5+%EC%88%98%ED%95%99&hl=ko&gl=KR&ceid=KR:ko",
    ),
    (
        "global_math_ed",
        "https://news.google.com/rss/search?q=%22math+education%22+OR+%22AI+exam%22+OR+%22geometry+curriculum%22+OR+%22calculus+education%22&hl=en-US&gl=US&ceid=US:en",
    ),
]

CURATED_EDU_NEWS_TRACKS = [
    {
        "track_id": "edunews01",
        "news_theme_ko": "웨어러블 스마트 안경 시험 부정행위 논란과 5지선다 평가의 한계",
        "news_theme_en": "Wearable Smart-Glasses Exam Controversy & Limits of Multiple-Choice Testing",
        "pedagogical_response_ko": "카메라로 수식을 찍어 번호를 듣는 시험 대신, 수식·좌표·보기가 없는 순수 곡선 하나에서 평행현과 대칭 원리로 초점·준선을 복원하는 동적 기하 작도 평가로 전환",
        "pedagogical_response_en": "Shift from equation plug-in choices to hands-on geometric construction: recovering axis, focus, and directrix from a bare parabola via parallel chords",
        "vault_slug": "2022040501",
        "vault_pdf_url": "https://min7014.github.io/math2022040501/2022040501.pdf",
        "related_youtube_url": "https://youtu.be/hgb_73tr-jQ",
        "lesson_slug": "edunews01",
        "lesson_title_ko": "[교육이슈×수학본질 01] 식도 좌표도 없는 포물선 하나에서 대칭축·초점·준선 작도하기",
        "lesson_title_en": "🧭 [Edu-Issue × Math Essence #01] Constructing Axis, Focus & Directrix from a Bare Parabola",
        "keywords": ["안경", "웨어러블", "부정행위", "객관식", "5지선다", "작도", "포물선", "초점", "준선", "glasses", "cheating"],
    },
    {
        "track_id": "edunews02",
        "news_theme_ko": "첨단 광학·웨어러블 디스플레이 시대의 기하 교육 소외 현상",
        "news_theme_en": "Modern Optical Display Era vs. Formula-Only Conic Section Classrooms",
        "pedagogical_response_ko": "판별식 D=0 기계적 암기 대신, 초소형 광원의 빛이 렌즈에서 반사되어 눈동자 초점으로 모이는 '타원·포물선 빛 반사 최단거리 대칭 원리'를 수식 0줄로 체득",
        "pedagogical_response_en": "Replace discriminant rote drills with zero-formula mirror-symmetry proofs of focal light reflection in ellipses and parabolas",
        "vault_slug": "2022051507",
        "vault_pdf_url": "https://min7014.github.io/math2022051507/2022051507.pdf",
        "related_youtube_url": "https://youtu.be/hgb_73tr-jQ",
        "lesson_slug": "edunews02",
        "lesson_title_ko": "[교육이슈×수학본질 02] 스마트 광학 렌즈 속 빛은 왜 한 점으로 모일까? 타원 초점 반사 시각 증명",
        "lesson_title_en": "🧭 [Edu-Issue × Math Essence #02] Why Do Reflected Rays Converge? Visual Proof of Ellipse Focal Reflection",
        "keywords": ["광학", "렌즈", "반사", "타원", "이차곡선", "기하", "optical", "reflection", "ellipse"],
    },
    {
        "track_id": "edunews03",
        "news_theme_ko": "생성형 AI의 초고속 미분 계산 시대와 '인간 고유의 미적분 문해력' 논쟁",
        "news_theme_en": "Instant AI Differentiation vs. Human Structural Calculus Literacy",
        "pedagogical_response_ko": "단순 미분공식 반복 훈련을 넘어, 포물선의 대칭성 때문에 구간 [a, b]의 평균변화율과 정확히 중점 (a+b)/2의 순간변화율이 일치할 수밖에 없는 기하 구조 통찰",
        "pedagogical_response_en": "Move beyond power-rule drills to see why parabolic symmetry locks the secant slope on [a, b] to the exact midpoint tangent at (a+b)/2",
        "vault_slug": "2019072401",
        "vault_pdf_url": "https://min7014.github.io/math2019072401/2019072401.pdf",
        "related_youtube_url": "https://www.youtube.com/@min7014_ai/videos",
        "lesson_slug": "edunews03",
        "lesson_title_ko": "[교육이슈×수학본질 03] AI가 0.1초 만에 미분하는 시대 — 포물선 중점 접선의 기하학적 필연성",
        "lesson_title_en": "🧭 [Edu-Issue × Math Essence #03] Calculus Beyond AI Drills: Midpoint Tangent Symmetry of a Parabola",
        "keywords": ["인공지능", "디지털교과서", "미분", "평균변화율", "접선", "문해력", "ai", "calculus", "derivative"],
    },
    {
        "track_id": "edunews04",
        "news_theme_ko": "서술형·수리논술 평가 확대와 '무비판적 극한 편법 공식 남용' 감점 이슈",
        "news_theme_en": "Expansion of Proof-Based Essays & Pitfalls of Blind Limit Shortcuts",
        "pedagogical_response_ko": "전제 조건 확인 없이 편법 미분만 쓰는 습관을 교정하고, 매개변수 곡선 (g(t), f(t)) 위의 평행 접선 그림 한 장으로 코시의 평균값 정리를 엄밀히 정당화",
        "pedagogical_response_en": "Cure blind shortcut misuse by visualizing Cauchy's Mean Value Theorem as a parallel tangent on a parametric curve (g(t), f(t))",
        "vault_slug": "2016012801",
        "vault_pdf_url": "https://min7014.github.io/math2016012801/2016012801.pdf",
        "related_youtube_url": "https://www.youtube.com/@min7014_ai/videos",
        "lesson_slug": "edunews04",
        "lesson_title_ko": "[교육이슈×수학본질 04] 서술형·논술 감점 1순위 편법 탈피! 매개변수 곡선으로 보는 코시의 평균값 정리",
        "lesson_title_en": "🧭 [Edu-Issue × Math Essence #04] Proof Literacy: Seeing Cauchy's Mean Value Theorem via Parametric Curves",
        "keywords": ["서술형", "논술", "수리논술", "수행평가", "평균값", "극한", "정당화", "essay", "proof"],
    },
]

NON_EDU_NOISE_RE = re.compile(r"연예|정치|선거|프로야구|범죄|드라마|아이돌", re.IGNORECASE)


def _sanitize_signal_text(raw: str) -> str:
    import auditor

    t = re.sub(r"\s+-\s+[^-]+$", "", str(raw or "").strip())
    t = re.sub(r"<[^>]+>", "", t).strip()
    t = auditor.sanitize_and_gate_upload_payload(t, "", [])["title"]
    return t[:100]


def scan_live_edu_news(timeout: int = 8) -> list[dict]:
    import auditor

    signals: list[dict] = []
    seen: set[str] = set()
    for src_id, url in EDU_NEWS_RSS_FEEDS:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                xml_bytes = resp.read()
            root = ET.fromstring(xml_bytes)
            for it in root.findall(".//item")[:8]:
                raw_t = (it.findtext("title") or "").strip()
                clean_t = _sanitize_signal_text(raw_t)
                if not clean_t or clean_t in seen:
                    continue
                if NON_EDU_NOISE_RE.search(clean_t) or auditor.FORBIDDEN_TRADING_DOMAIN_RE.search(clean_t):
                    continue
                seen.add(clean_t)

                low_t = clean_t.lower()
                matched_track = CURATED_EDU_NEWS_TRACKS[0]["track_id"]
                best_hits = 0
                for tr in CURATED_EDU_NEWS_TRACKS:
                    hits = sum(1 for kw in tr["keywords"] if kw in low_t)
                    if hits > best_hits:
                        best_hits = hits
                        matched_track = tr["track_id"]

                signals.append(
                    {
                        "source": src_id,
                        "abstracted_topic": clean_t,
                        "matched_track_id": matched_track,
                        "detected_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    }
                )
                if len(signals) >= 12:
                    break
        except Exception:
            continue
    return signals


def sync_edu_news_db(timeout: int = 6) -> dict:
    signals = scan_live_edu_news(timeout=timeout)
    tracks_out = []
    for tr in CURATED_EDU_NEWS_TRACKS:
        html_path = BOARD_DIR / f"{tr['lesson_slug']}.html"
        tracks_out.append(
            {
                **tr,
                "website_lesson_ready": html_path.exists(),
                "website_lesson_url": f"https://min7014.github.io/mathedu/board/{tr['lesson_slug']}.html" if html_path.exists() else "",
            }
        )

    db = {
        "updated_at": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "philosophy": "뿌리는 불변의 수학 원문(min7014.github.io), 입구는 살아있는 교육 뉴스 대응 (Policy 64)",
        "live_edu_news_signals_count": len(signals),
        "live_edu_news_signals": signals,
        "curated_response_tracks": tracks_out,
    }
    EDU_NEWS_DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    EDU_NEWS_DB_FILE.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")
    return db


def _extract_stitch_shell_from_template() -> tuple[str, str, str]:
    """기존 검증된 Stitch 수업 페이지(board/c30923.html)에서 공통 CSS 스타일과 상·하단 프레임 추출"""
    tpl_path = BOARD_DIR / "c30923.html"
    raw = tpl_path.read_text(encoding="utf-8")
    m_style = re.search(r"(<style>.*?</style>)", raw, flags=re.S)
    style_block = m_style.group(1) if m_style else ""
    m_gw = re.search(r"(<!-- STITCH_EXPLORER_START -->.*?</div>\s*</div>\s*</div>)", raw, flags=re.S)
    _ = m_gw
    return style_block, "", ""


def build_flagship_edunews01_lesson() -> Path:
    """
    [Flagship #01] AI 스마트 안경 시험 논란에 대한 수학교육의 본질적 응답 수업자료:
    `board/edunews01.html` — 식도 좌표도 없는 포물선 곡선 하나에서 대칭축·초점·준선 작도하기
    - Rule 6: 초등 대칭 접기 직관 → 중점 → 평행현 자취 → 수직이등분선 꼭짓점 → 45° 4등분 초점·준선 6단계 디딤돌
    - Rule 7: 정교한 인라인 <svg> 작도 다이어그램 + 한눈에 보는 도식화 풀이 흐름도
    - Rule 11: 탈-5지선다 MatheduCreativeSolver 자동 연동
    - Rule 58: 100% KO/EN 양방향 번역 완비
    - Rule 61: 영상은 인라인 임베드 없이 오직 @min7014_ai 유튜브 직결 링크로만 연결
    """
    tpl = (BOARD_DIR / "c30923.html").read_text(encoding="utf-8")
    style_match = re.search(r"<style>.*?</style>", tpl, flags=re.S)
    if not style_match:
        raise RuntimeError("Could not extract Stitch <style> block from c30923.html")
    stitch_style = style_match.group(0)

    slug = "edunews01"
    title_ko = "[교육이슈×수학본질 01] 식도 좌표도 없는 포물선 하나에서 대칭축·초점·준선 작도하기"
    title_en = "🧭 [Edu-Issue × Math Essence #01] Constructing Axis, Focus & Directrix from a Bare Parabola"

    svg_ko = """<svg class="mathedu-bespoke-svg" viewBox="0 0 700 320" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:700px;height:auto;display:block;margin:0 auto;border-radius:12px;background:linear-gradient(145deg,#ffffff 0%,#f8fafc 100%);border:1.5px solid #cbd5e1;box-shadow:0 4px 16px rgba(19,27,46,0.06)">
  <defs>
    <pattern id="gridEdu01" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(0,99,152,0.06)" stroke-width="1"/>
    </pattern>
  </defs>
  <rect width="700" height="320" fill="url(#gridEdu01)" rx="12"/>
  <rect x="14" y="10" width="672" height="32" rx="8" fill="#e0f2fe" stroke="#7dd3fc"/>
  <text x="26" y="31" fill="#006398" font-size="12" font-weight="800" font-family="sans-serif">📐 [순수 기하 작도 원리] 방정식·좌표축 ZERO 포물선 → 대칭축 · 꼭짓점 · 초점 · 준선 복원</text>

  <!-- 좌측 작도 캔버스: 정확한 포물선 (180 - y)² = 88(x - 110), 꼭짓점 V(110,180), p=22, 4p=88 -->
  <rect x="18" y="50" width="402" height="256" rx="10" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
  <!-- 준선 d (x = 88 = x_V - p) -->
  <line x1="88" y1="60" x2="88" y2="278" stroke="#7c3aed" stroke-width="2.2" stroke-dasharray="6,4"/>
  <text x="58" y="76" fill="#6d28d9" font-size="11" font-weight="800" text-anchor="middle">준선 d</text>
  <!-- 대칭축 l (y = 180) -->
  <line x1="48" y1="180" x2="404" y2="180" stroke="#059669" stroke-width="2.3"/>
  <rect x="88" y="172" width="8" height="8" fill="none" stroke="#64748b" stroke-width="1.2"/>
  <text x="378" y="172" fill="#047857" font-size="11" font-weight="800" text-anchor="middle">대칭축 ℓ</text>

  <!-- Step 1: 평행한 두 현(기울기 1)과 정확한 중점 M₁(140.9, 224), M₂(178.5, 224) 연결선 M₁M₂ ∥ ℓ -->
  <line x1="112.9" y1="196" x2="168.9" y2="252" stroke="#94a3b8" stroke-width="1.8"/>
  <line x1="114.5" y1="160" x2="242.5" y2="288" stroke="#94a3b8" stroke-width="1.8"/>
  <line x1="122" y1="224" x2="366" y2="224" stroke="#f59e0b" stroke-width="2" stroke-dasharray="5,3"/>
  <circle cx="140.9" cy="224" r="4.2" fill="#f59e0b" stroke="#ffffff" stroke-width="1.2"/>
  <circle cx="178.5" cy="224" r="4.2" fill="#f59e0b" stroke="#ffffff" stroke-width="1.2"/>
  <text x="278" y="217" fill="#b45309" font-size="10.5" font-weight="800" text-anchor="middle">평행현 중점 직선 M₁M₂ ∥ ℓ</text>

  <!-- Step 3: 꼭짓점 V(110,180)에서 정확한 45° 반직선 → 교점 Q(198,92), 수선의 발 H(198,180) [VH = QH = 4p = 88] -->
  <polygon points="110,180 198,180 198,92" fill="rgba(13,148,136,0.08)" stroke="none"/>
  <path d="M 128 180 A 18 18 0 0 0 122.7 167.3" fill="none" stroke="#0d9488" stroke-width="1.5"/>
  <text x="140" y="174" fill="#0f766e" font-size="9.5" font-weight="800">45°</text>
  <line x1="110" y1="180" x2="212" y2="78" stroke="#0d9488" stroke-width="1.9" stroke-dasharray="4,3"/>
  <line x1="198" y1="92" x2="198" y2="180" stroke="#64748b" stroke-width="1.5" stroke-dasharray="3,3"/>
  <rect x="190" y="172" width="8" height="8" fill="none" stroke="#64748b" stroke-width="1.2"/>
  <!-- VH 4등분 눈금 (p=22 간격: 132, 154, 176, 198) -->
  <line x1="154" y1="176" x2="154" y2="184" stroke="#047857" stroke-width="1.6"/>
  <line x1="176" y1="176" x2="176" y2="184" stroke="#047857" stroke-width="1.6"/>

  <!-- 해석학적으로 100% 정확한 2차 베지어 포물선: (180 - y)² = 88(x - 110) -->
  <path d="M 279.14 58 Q 110 119 110 180 Q 110 234 242.55 288" fill="none" stroke="#0284c7" stroke-width="3.4" stroke-linecap="round"/>

  <!-- 주요 점 V, F(p), H(4p), Q(4p,4p) 마커 및 라벨 -->
  <circle cx="110" cy="180" r="5.2" fill="#059669" stroke="#ffffff" stroke-width="1.5"/>
  <text x="100" y="197" fill="#047857" font-size="11.5" font-weight="900" text-anchor="middle" paint-order="stroke" stroke="#ffffff" stroke-width="3.2" stroke-linejoin="round">V</text>
  <circle cx="132" cy="180" r="5.6" fill="#d97706" stroke="#ffffff" stroke-width="1.5"/>
  <text x="142" y="199" fill="#b45309" font-size="10.8" font-weight="900" text-anchor="middle" paint-order="stroke" stroke="#ffffff" stroke-width="3.4" stroke-linejoin="round">초점 F(p)</text>
  <circle cx="198" cy="180" r="4.5" fill="#334155"/>
  <text x="206" y="198" fill="#334155" font-size="10.8" font-weight="800" text-anchor="middle" paint-order="stroke" stroke="#ffffff" stroke-width="3.2" stroke-linejoin="round">H(4p)</text>
  <circle cx="198" cy="92" r="5.2" fill="#0284c7" stroke="#ffffff" stroke-width="1.4"/>
  <text x="208" y="94" fill="#0369a1" font-size="11" font-weight="800">Q(45° 교점)</text>
  <text x="219" y="299" fill="#0f172a" font-size="10.6" font-weight="800" text-anchor="middle">VH = 4p ⇒ 4등분 시 VF = p, 초점~준선 거리 = 2p</text>

  <!-- 우측 4단계 핵심 요약 -->
  <rect x="434" y="50" width="250" height="256" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="559" y="73" fill="#006398" font-size="12" font-weight="800" text-anchor="middle">작도 4단계 핵심 불변 원리</text>
  <rect x="448" y="84" width="222" height="46" rx="7" fill="#eff6ff" stroke="#93c5fd"/>
  <text x="559" y="102" fill="#006398" font-size="10.5" font-weight="800" text-anchor="middle">① 평행한 두 현의 중점 M₁, M₂ 연결</text>
  <text x="559" y="120" fill="#1e293b" font-size="10.2" font-weight="700" text-anchor="middle">직선 M₁M₂ 는 항상 대칭축과 평행!</text>
  <rect x="448" y="138" width="222" height="46" rx="7" fill="#ecfdf5" stroke="#6ee7b7"/>
  <text x="559" y="156" fill="#047857" font-size="10.5" font-weight="800" text-anchor="middle">② 수직인 현 AB 의 수직이등분선</text>
  <text x="559" y="174" fill="#1e293b" font-size="10.2" font-weight="700" text-anchor="middle">대칭축 ℓ 과 꼭짓점 V 완벽 복원!</text>
  <rect x="448" y="192" width="222" height="46" rx="7" fill="#f5f3ff" stroke="#c4b5fd"/>
  <text x="559" y="210" fill="#4f46e5" font-size="10.5" font-weight="800" text-anchor="middle">③ 꼭짓점 V 에서 45° 반직선 교점 Q</text>
  <text x="559" y="228" fill="#1e293b" font-size="10.2" font-weight="700" text-anchor="middle">y=x 와 y²=4px 교점 ⇒ VH = 4p</text>
  <rect x="448" y="246" width="222" height="46" rx="7" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="559" y="265" fill="#b45309" font-size="11" font-weight="900" text-anchor="middle">④ VH = 12 일 때 p = 3</text>
  <text x="559" y="283" fill="#92400e" font-size="11.2" font-weight="900" text-anchor="middle">🎯 초점 F ~ 준선 d 거리 2p = 6</text>
</svg>"""

    svg_en = """<svg class="mathedu-bespoke-svg" viewBox="0 0 700 320" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:700px;height:auto;display:block;margin:0 auto;border-radius:12px;background:linear-gradient(145deg,#ffffff 0%,#f8fafc 100%);border:1.5px solid #cbd5e1;box-shadow:0 4px 16px rgba(19,27,46,0.06)">
  <rect width="700" height="320" fill="#f8fafc" rx="12"/>
  <rect x="14" y="10" width="672" height="32" rx="8" fill="#e0f2fe" stroke="#7dd3fc"/>
  <text x="26" y="31" fill="#006398" font-size="12" font-weight="800" font-family="sans-serif">📐 [Pure Geometric Construction] Bare Parabola → Axis · Vertex · Focus · Directrix</text>
  <rect x="18" y="50" width="402" height="256" rx="10" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
  <line x1="88" y1="60" x2="88" y2="278" stroke="#7c3aed" stroke-width="2.2" stroke-dasharray="6,4"/>
  <text x="56" y="76" fill="#6d28d9" font-size="10.2" font-weight="800" text-anchor="middle">Directrix d</text>
  <line x1="48" y1="180" x2="404" y2="180" stroke="#059669" stroke-width="2.3"/>
  <rect x="88" y="172" width="8" height="8" fill="none" stroke="#64748b" stroke-width="1.2"/>
  <text x="380" y="172" fill="#047857" font-size="11" font-weight="800" text-anchor="middle">Axis ℓ</text>
  <line x1="112.9" y1="196" x2="168.9" y2="252" stroke="#94a3b8" stroke-width="1.8"/>
  <line x1="114.5" y1="160" x2="242.5" y2="288" stroke="#94a3b8" stroke-width="1.8"/>
  <line x1="122" y1="224" x2="366" y2="224" stroke="#f59e0b" stroke-width="2" stroke-dasharray="5,3"/>
  <circle cx="140.9" cy="224" r="4.2" fill="#f59e0b" stroke="#ffffff" stroke-width="1.2"/>
  <circle cx="178.5" cy="224" r="4.2" fill="#f59e0b" stroke="#ffffff" stroke-width="1.2"/>
  <text x="278" y="217" fill="#b45309" font-size="10.2" font-weight="800" text-anchor="middle">Midpoints M₁M₂ ∥ Axis ℓ</text>
  <polygon points="110,180 198,180 198,92" fill="rgba(13,148,136,0.08)" stroke="none"/>
  <path d="M 128 180 A 18 18 0 0 0 122.7 167.3" fill="none" stroke="#0d9488" stroke-width="1.5"/>
  <text x="140" y="174" fill="#0f766e" font-size="9.5" font-weight="800">45°</text>
  <line x1="110" y1="180" x2="212" y2="78" stroke="#0d9488" stroke-width="1.9" stroke-dasharray="4,3"/>
  <line x1="198" y1="92" x2="198" y2="180" stroke="#64748b" stroke-width="1.5" stroke-dasharray="3,3"/>
  <rect x="190" y="172" width="8" height="8" fill="none" stroke="#64748b" stroke-width="1.2"/>
  <line x1="154" y1="176" x2="154" y2="184" stroke="#047857" stroke-width="1.6"/>
  <line x1="176" y1="176" x2="176" y2="184" stroke="#047857" stroke-width="1.6"/>
  <path d="M 279.14 58 Q 110 119 110 180 Q 110 234 242.55 288" fill="none" stroke="#0284c7" stroke-width="3.4" stroke-linecap="round"/>
  <circle cx="110" cy="180" r="5.2" fill="#059669" stroke="#ffffff" stroke-width="1.5"/>
  <text x="100" y="197" fill="#047857" font-size="11.5" font-weight="900" text-anchor="middle" paint-order="stroke" stroke="#ffffff" stroke-width="3.2" stroke-linejoin="round">V</text>
  <circle cx="132" cy="180" r="5.6" fill="#d97706" stroke="#ffffff" stroke-width="1.5"/>
  <text x="145" y="199" fill="#b45309" font-size="10.5" font-weight="900" text-anchor="middle" paint-order="stroke" stroke="#ffffff" stroke-width="3.4" stroke-linejoin="round">Focus F(p)</text>
  <circle cx="198" cy="180" r="4.5" fill="#334155"/>
  <text x="206" y="198" fill="#334155" font-size="10.8" font-weight="800" text-anchor="middle" paint-order="stroke" stroke="#ffffff" stroke-width="3.2" stroke-linejoin="round">H(4p)</text>
  <circle cx="198" cy="92" r="5.2" fill="#0284c7" stroke="#ffffff" stroke-width="1.4"/>
  <text x="208" y="94" fill="#0369a1" font-size="10.5" font-weight="800">Q(45° Ray)</text>
  <text x="219" y="299" fill="#0f172a" font-size="10.5" font-weight="800" text-anchor="middle">VH = 4p ⇒ Quartering gives VF = p, Focus-Directrix = 2p</text>
  <rect x="434" y="50" width="250" height="256" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="559" y="73" fill="#006398" font-size="11.5" font-weight="800" text-anchor="middle">4-Step Construction Invariants</text>
  <rect x="448" y="84" width="222" height="46" rx="7" fill="#eff6ff" stroke="#93c5fd"/>
  <text x="559" y="102" fill="#006398" font-size="10.2" font-weight="800" text-anchor="middle">1. Midpoints M₁, M₂ of Parallel Chords</text>
  <text x="559" y="120" fill="#1e293b" font-size="10" font-weight="700" text-anchor="middle">Line M₁M₂ is always parallel to Axis ℓ</text>
  <rect x="448" y="138" width="222" height="46" rx="7" fill="#ecfdf5" stroke="#6ee7b7"/>
  <text x="559" y="156" fill="#047857" font-size="10.2" font-weight="800" text-anchor="middle">2. Perpendicular Bisector of Chord AB</text>
  <text x="559" y="174" fill="#1e293b" font-size="10" font-weight="700" text-anchor="middle">Recovers exact Axis ℓ &amp; Vertex V</text>
  <rect x="448" y="192" width="222" height="46" rx="7" fill="#f5f3ff" stroke="#c4b5fd"/>
  <text x="559" y="210" fill="#4f46e5" font-size="10.2" font-weight="800" text-anchor="middle">3. 45° Ray from Vertex V Meets at Q</text>
  <text x="559" y="228" fill="#1e293b" font-size="10" font-weight="700" text-anchor="middle">y = x &amp; y² = 4px ⇒ VH = 4p</text>
  <rect x="448" y="246" width="222" height="46" rx="7" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="559" y="265" fill="#b45309" font-size="10.8" font-weight="900" text-anchor="middle">4. Given VH = 12 ⇒ p = 3</text>
  <text x="559" y="283" fill="#92400e" font-size="11" font-weight="900" text-anchor="middle">🎯 Focus-to-Directrix 2p = 6</text>
</svg>"""

    flow_ko = r"""<section class="math-schematic-flow" style="margin:12px 0 18px;padding:14px;background:#f8fafc;border:1px solid #cbd5e1;border-radius:14px">
  <table style="width:100%;border-collapse:separate;border-spacing:4px">
    <tr>
      <td style="background:#ffffff;border:1px solid #cbd5e1;border-radius:10px;padding:10px;width:22%">
        <b style="color:#006398;font-size:0.78rem;display:block;margin-bottom:4px">STEP 1 · 평행현 중점</b>
        <span style="color:#1e293b;font-size:0.84rem">평행한 두 현의 중점 $M_1, M_2$ 연결 $\Rightarrow$ 대칭축 방향 획득</span>
      </td>
      <td style="text-align:center;color:#d97706;font-weight:900">→</td>
      <td style="background:#ffffff;border:1px solid #cbd5e1;border-radius:10px;padding:10px;width:22%">
        <b style="color:#006398;font-size:0.78rem;display:block;margin-bottom:4px">STEP 2 · 대칭축·꼭짓점</b>
        <span style="color:#1e293b;font-size:0.84rem">$M_1M_2 \perp AB$ 현의 수직이등분선 $\Rightarrow$ 대칭축 $\ell$과 꼭짓점 $V$</span>
      </td>
      <td style="text-align:center;color:#d97706;font-weight:900">→</td>
      <td style="background:#ffffff;border:1px solid #cbd5e1;border-radius:10px;padding:10px;width:22%">
        <b style="color:#006398;font-size:0.78rem;display:block;margin-bottom:4px">STEP 3 · 45° 교점 4등분</b>
        <span style="color:#1e293b;font-size:0.84rem">$y=x$ 교점 $Q(4p,4p) \Rightarrow \overline{VH}=4p=12 \Rightarrow p=3$</span>
      </td>
      <td style="text-align:center;color:#059669;font-weight:900">⇒</td>
      <td style="background:#ecfdf5;border:1.5px solid #10b981;border-radius:10px;padding:10px;text-align:center;width:18%">
        <b style="color:#047857;font-size:0.78rem;display:block;margin-bottom:4px">🎯 초점~준선 거리</b>
        <b style="color:#065f46;font-size:1.02rem">$2p = 6$</b>
      </td>
    </tr>
  </table>
</section>"""

    flow_en = r"""<section class="math-schematic-flow" style="margin:12px 0 18px;padding:14px;background:#f8fafc;border:1px solid #cbd5e1;border-radius:14px">
  <table style="width:100%;border-collapse:separate;border-spacing:4px">
    <tr>
      <td style="background:#ffffff;border:1px solid #cbd5e1;border-radius:10px;padding:10px;width:22%">
        <b style="color:#006398;font-size:0.78rem;display:block;margin-bottom:4px">STEP 1 · Parallel Chords</b>
        <span style="color:#1e293b;font-size:0.84rem">Join midpoints $M_1, M_2$ $\Rightarrow$ Direction of Axis $\ell$</span>
      </td>
      <td style="text-align:center;color:#d97706;font-weight:900">→</td>
      <td style="background:#ffffff;border:1px solid #cbd5e1;border-radius:10px;padding:10px;width:22%">
        <b style="color:#006398;font-size:0.78rem;display:block;margin-bottom:4px">STEP 2 · Axis &amp; Vertex</b>
        <span style="color:#1e293b;font-size:0.84rem">Perpendicular bisector of $AB \perp M_1M_2 \Rightarrow \ell$ &amp; $V$</span>
      </td>
      <td style="text-align:center;color:#d97706;font-weight:900">→</td>
      <td style="background:#ffffff;border:1px solid #cbd5e1;border-radius:10px;padding:10px;width:22%">
        <b style="color:#006398;font-size:0.78rem;display:block;margin-bottom:4px">STEP 3 · 45° Ray Quartering</b>
        <span style="color:#1e293b;font-size:0.84rem">$Q(4p,4p)$ gives $\overline{VH}=4p=12 \Rightarrow p=3$</span>
      </td>
      <td style="text-align:center;color:#059669;font-weight:900">⇒</td>
      <td style="background:#ecfdf5;border:1.5px solid #10b981;border-radius:10px;padding:10px;text-align:center;width:18%">
        <b style="color:#047857;font-size:0.78rem;display:block;margin-bottom:4px">🎯 Focus to Directrix</b>
        <b style="color:#065f46;font-size:1.02rem">$2p = 6$</b>
      </td>
    </tr>
  </table>
</section>"""

    steps_data = [
        {
            "lvl_ko": r"🔰 1단계 · [초등 대칭 직관] 데칼코마니 반 접기와 한가운데 중점",
            "lvl_en": r"🔰 Step 1 · [Elementary Symmetry Intuition] Folding in Half & the Exact Midpoint",
            "stem_ko": r"양쪽 모양이 똑같은 데칼코마니 도형을 접는 선(대칭축)을 따라 반으로 접으면 완전히 포개집니다. 접는 선과 <b>수직</b>으로 그린 선분의 길이가 $10$일 때, 접는 선은 이 선분을 각각 얼마의 길이로 나눌까요?",
            "stem_en": r"When a symmetric figure is folded along its line of symmetry, both halves match exactly. If a segment drawn <b>perpendicular</b> to the fold line has length $10$, into what two lengths does the fold line divide it?",
            "opts": [
                (r"$2$와 $8$", r"$2$ and $8$"),
                (r"$5$와 $5$ (정확히 반씩, 중점!)", r"$5$ and $5$ (exact midpoint!)"),
                (r"$3$과 $7$", r"$3$ and $7$"),
                (r"$4$와 $6$", r"$4$ and $6$"),
                (r"$1$과 $9$", r"$1$ and $9$"),
            ],
            "ans": 2,
            "exp_ko": r"대칭축에 수직인 선분은 대칭축에 의해 항상 똑같은 길이($10 \div 2 = 5$)로 수직이등분됩니다. 거꾸로 말하면, 대칭인 두 점을 이은 선분의 <b>수직이등분선</b>이 곧 대칭축이 됩니다!",
            "exp_en": r"Any segment perpendicular to the axis of symmetry is bisected into two equal parts ($10 \div 2 = 5$). Conversely, the perpendicular bisector of a symmetric chord IS the axis of symmetry!",
        },
        {
            "lvl_ko": r"🔰 2단계 · [구체적 수치 관찰] 포물선에서 수평 평행선 두 개의 중점 잇기",
            "lvl_en": r"🔰 Step 2 · [Concrete Coordinate Check] Connecting Midpoints of Two Horizontal Chords",
            "stem_ko": r"가장 친숙한 포물선 $y = x^2$에 두 수평선 $y = 4$와 $y = 9$를 그어 봅시다. $y = 4$와 만나는 두 점 $(-2, 4), (2, 4)$의 중점은 $(0, 4)$이고, $y = 9$와 만나는 두 점 $(-3, 9), (3, 9)$의 중점은 $(0, 9)$입니다. 이 두 중점 $(0, 4)$와 $(0, 9)$를 이은 직선은 무엇과 일치합니까?",
            "stem_en": r"On the parabola $y = x^2$, the horizontal line $y = 4$ meets the curve at $(-2, 4)$ and $(2, 4)$ with midpoint $(0, 4)$, while $y = 9$ meets it at $(-3, 9)$ and $(3, 9)$ with midpoint $(0, 9)$. What line is formed by joining $(0, 4)$ and $(0, 9)$?",
            "opts": [
                (r"$x$축 ($y = 0$)", r"The $x$-axis ($y = 0$)"),
                (r"직선 $y = x$", r"The line $y = x$"),
                (r"포물선의 대칭축 ($y$축, $x = 0$)", r"The parabola's axis of symmetry ($y$-axis, $x = 0$)"),
                (r"직선 $y = 4$", r"The line $y = 4$"),
                (r"원점을 지나지 않는 사선", r"An oblique line missing the origin"),
            ],
            "ans": 3,
            "exp_ko": r"대칭축에 수직인 평행현들의 중점은 모두 $(0, 4), (0, 9)$처럼 포물선의 대칭축($x = 0$) 위에 나란히 놓입니다.",
            "exp_en": r"Midpoints of chords perpendicular to the axis all lie directly on the parabola's axis of symmetry ($x = 0$).",
        },
        {
            "lvl_ko": r"🧭 3단계 · [제1보조선 발견!] 비스듬히 평행한 두 현의 중점을 이으면?",
            "lvl_en": r"🧭 Step 3 · [First Auxiliary Insight!] Joining Midpoints of Oblique Parallel Chords",
            "stem_ko": r"식도 좌표축도 없는 백지 위 포물선에서는 처음에 어느 방향이 대칭축인지 모릅니다! 포물선 $y^2 = 4px$ 위에 기울기가 $m(\neq 0)$으로 서로 <b>평행한 임의의 두 현</b>을 그어 두 교점의 $y$좌표를 $y_1, y_2$라 하면, $y_1^2 - y_2^2 = 4p(x_1 - x_2)$에서 $\frac{y_1 - y_2}{x_1 - x_2} = m$이므로 중점의 $y$좌표 $\frac{y_1 + y_2}{2} = \frac{2p}{m}$로 항상 일정합니다! 즉, 평행한 두 현의 중점 $M_1, M_2$를 이은 직선은 항상 무엇과 평행합니까?",
            "stem_en": r"On a bare parabola with no axes drawn, we do not initially know the axis direction! For any two chords of slope $m(\neq 0)$ on $y^2 = 4px$, subtracting $y_1^2 - y_2^2 = 4p(x_1 - x_2)$ yields $\frac{y_1 + y_2}{2} = \frac{2p}{m}$ (a constant!). Therefore, the line $M_1M_2$ joining the midpoints of two parallel chords is ALWAYS parallel to what?",
            "opts": [
                (r"포물선의 대칭축", r"The axis of symmetry of the parabola"),
                (r"포물선의 준선", r"The directrix of the parabola"),
                ("꼭짓점에서의 접선", "The tangent at the vertex"),
                (r"기울기가 $m$인 원래 현", r"The original chords of slope $m$"),
                (r"일정한 방향이 없다", r"No fixed direction exists"),
            ],
            "ans": 1,
            "exp_ko": r"놀라운 성질입니다! 어떤 기울기 $m$으로 그어도 평행한 두 현의 중점 $M_1, M_2$는 $y$좌표가 $\frac{2p}{m}$로 똑같으므로, 직선 $M_1M_2$는 $x$축(즉, <b>포물선의 대칭축</b>)과 언제나 평행합니다!",
            "exp_en": r"Regardless of the chosen slope $m \neq 0$, both midpoints share the exact same ordinate $\frac{2p}{m}$, meaning line $M_1M_2$ is ALWAYS parallel to the parabola's axis of symmetry!",
        },
        {
            "lvl_ko": r"📐 4단계 · [대칭축 $\ell$과 꼭짓점 $V$ 작도] 수직인 현과 수직이등분선",
            "lvl_en": r"📐 Step 4 · [Recovering Axis $\ell$ & Vertex $V$] Perpendicular Chord & Bisector",
            "stem_ko": r"3단계에서 찾은 직선 $M_1M_2$는 대칭축과 평행합니다. 이제 $M_1M_2$와 <b>수직</b>이 되도록 포물선에 새로운 현 $AB$를 긋고, 선분 $AB$의 <b>수직이등분선 $\ell$</b>을 작도하면 이 직선 $\ell$과 포물선의 교점 $V$는 무엇이 됩니까?",
            "stem_en": r"Line $M_1M_2$ from Step 3 is parallel to the axis. If we now draw a chord $AB$ <b>perpendicular</b> to $M_1M_2$ and construct the <b>perpendicular bisector $\ell$</b> of segment $AB$, what are line $\ell$ and its intersection $V$ with the parabola?",
            "opts": [
                (r"준선 $\ell$과 초점 $V$", r"Directrix $\ell$ and Focus $V$"),
                (r"임의의 할선 $\ell$과 변곡점 $V$", r"Secant line $\ell$ and inflection point $V$"),
                (r"접선 $\ell$과 초점 $V$", r"Tangent line $\ell$ and Focus $V$"),
                (r"포물선의 대칭축 $\ell$과 꼭짓점 $V$", r"The exact Axis of Symmetry $\ell$ and Vertex $V$"),
                (r"점근선 $\ell$과 중심 $V$", r"Asymptote $\ell$ and center $V$"),
            ],
            "ans": 4,
            "exp_ko": r"현 $AB$가 대칭축 방향($M_1M_2$)과 수직이므로, 포물선의 대칭성에 의해 선분 $AB$의 수직이등분선 $\ell$이 곧 <b>진짜 대칭축</b>이 되며, 대칭축이 포물선과 만나는 유일한 점 $V$가 바로 <b>꼭짓점(Vertex)</b>입니다!",
            "exp_en": r"Because chord $AB$ is perpendicular to the axis direction, its perpendicular bisector $\ell$ is the true <b>Axis of Symmetry</b>, meeting the parabola at its <b>Vertex $V$</b>!",
        },
        {
            "lvl_ko": r"✨ 5단계 · [초점 $F$ 복원 마법] 꼭짓점 $45^\circ$ 반직선과 $4$등분 원리",
            "lvl_en": r"✨ Step 5 · [Locating Focus $F$] The $45^\circ$ Ray from Vertex $V$ & Quartering",
            "stem_ko": r"이제 꼭짓점 $V$를 원점 $(0, 0)$, 대칭축 $\ell$을 양의 $x$축이라 두면 포물선은 $y^2 = 4px$입니다. 꼭짓점 $V$에서 대칭축과 $45^\circ$ 각도(즉, $y = x$)로 그은 반직선이 포물선과 다시 만나는 점 $Q$에서 대칭축에 내린 수선의 발을 $H$라 합시다. $x^2 = 4px$ ($x > 0$)에서 $\overline{VH}$는 $p$의 몇 배이며, $\overline{VH}$를 몇 등분하면 초점 $F(p, 0)$을 작도할 수 있습니까?",
            "stem_en": r"Taking Vertex $V$ as $(0, 0)$ and Axis $\ell$ as the positive $x$-axis ($y^2 = 4px$), draw a $45^\circ$ ray ($y = x$) from $V$ meeting the parabola at $Q$, and drop perpendicular $QH$ onto the axis. From $x^2 = 4px$ ($x > 0$), how many times $p$ is $\overline{VH}$, and into how many equal parts do we divide $\overline{VH}$ to locate Focus $F(p, 0)$?",
            "opts": [
                (r"$\overline{VH} = p$, 등분 필요 없음", r"$\overline{VH} = p$, no division needed"),
                (r"$\overline{VH} = 2p$, $2$등분", r"$\overline{VH} = 2p$, divide into $2$ equal parts"),
                (r"$\overline{VH} = 3p$, $3$등분", r"$\overline{VH} = 3p$, divide into $3$ equal parts"),
                (r"$\overline{VH} = 4p$, 반씩 두 번 접어 $4$등분!", r"$\overline{VH} = 4p$, bisect twice into $4$ equal parts!"),
                (r"$\overline{VH} = 8p$, $8$등분", r"$\overline{VH} = 8p$, divide into $8$ equal parts"),
            ],
            "ans": 4,
            "exp_ko": r"$y = x$를 $y^2 = 4px$에 대입하면 $x^2 = 4px \Rightarrow x = 4p$이므로 $Q(4p, 4p)$, 수선의 발 $H(4p, 0)$입니다! 따라서 $\overline{VH} = 4p$를 컴퍼스로 두 번 이등분($4$등분)하면 $\overline{VF} = p$인 <b>초점 $F$</b>가 정확히 작도되며, 반대쪽으로 $p$만큼 가면 <b>준선 $d$</b>까지 완성됩니다!",
            "exp_en": r"Substituting $y = x$ into $y^2 = 4px$ gives $x = 4p$, so $H = (4p, 0)$ and $\overline{VH} = 4p$. Bisecting $\overline{VH}$ twice ($\frac{1}{4}\overline{VH} = p$) locates Focus $F(p, 0)$, and stepping $p$ behind $V$ gives Directrix $x = -p$!",
        },
        {
            "lvl_ko": r"🏆 최종 본문항 · [AI 안경 무력화 실전 작도 추론] 초점과 준선 사이의 거리",
            "lvl_en": r"🏆 Final Synthesis · [AI-Proof Geometric Construction] Distance from Focus to Directrix",
            "stem_ko": r"식도 좌표축도 없는 순수 포물선 곡선 하나에 대하여 위 작도법으로 대칭축 $\ell$과 꼭짓점 $V$를 찾고, $V$에서 대칭축과 $45^\circ$를 이루는 반직선이 포물선과 만나는 점 $Q$에서 대칭축에 내린 수선의 발 $H$까지의 길이를 재었더니 $\overline{VH} = 12$였다. 이 포물선의 <b>초점 $F$에서 준선 $d$까지의 거리</b>는?",
            "stem_en": r"On a bare parabola with no equations or axes, you construct its axis $\ell$ and vertex $V$, draw a $45^\circ$ ray from $V$ meeting the parabola at $Q$, and drop perpendicular $QH$ to $\ell$. Given $\overline{VH} = 12$, what is the <b>distance from Focus $F$ to Directrix $d$</b>?",
            "opts": [
                (r"$3$", r"$3$"),
                (r"$4$", r"$4$"),
                (r"$6$", r"$6$"),
                (r"$8$", r"$8$"),
                (r"$12$", r"$12$"),
            ],
            "ans": 3,
            "exp_ko": rf"<b>[최종 본문항 도식화·시각화 완벽 해설]</b><br><h4>🎨 [그림으로 이해하는 시각적 도형·개념 다이어그램]</h4><figure class='math-visual-diagram' style='margin:12px 0;padding:12px;background:#f8fafc;border:1.5px solid #cbd5e1;border-radius:14px'>{svg_ko}</figure><h4>🗺️ [한눈에 보는 도식화 풀이 흐름도]</h4>{flow_ko}<p>꼭짓점 $V(0,0)$에서 $45^\circ$ 반직선($y=x$)과 포물선 $y^2=4px$의 교점은 $Q(4p, 4p)$이므로 $\overline{{VH}} = 4p = 12 \Rightarrow p = 3$입니다. 초점 $F(3, 0)$과 준선 $x = -3$ 사이의 거리는 $2p = 2 \times 3 = 6$입니다!</p>",
            "exp_en": rf"<b>[Complete Visual &amp; Schematic Solution]</b><br><h4>🎨 [Visual Geometric Diagram]</h4><figure class='math-visual-diagram' style='margin:12px 0;padding:12px;background:#f8fafc;border:1.5px solid #cbd5e1;border-radius:14px'>{svg_en}</figure><h4>🗺️ [Schematic Solution Flowchart]</h4>{flow_en}<p>From $y = x$ and $y^2 = 4px$, the intersection is $Q(4p, 4p)$, so $\overline{{VH}} = 4p = 12 \Rightarrow p = 3$. Because Focus $F$ is at $(p, 0)$ and Directrix $d$ is $x = -p$, the distance between Focus $F$ and Directrix $d$ is $2p = 6$!</p>",
        },
    ]

    q_blocks_html = []
    for st in steps_data:
        opts_html = "".join(
            f'<div class="opt"><span class="n">{i}</span><span class="opt-txt"><span class="bilingual-ko">{ko_o}</span><span class="bilingual-en">{en_o}</span></span></div>'
            for i, (ko_o, en_o) in enumerate(st["opts"], 1)
        )
        esc_ko = html.escape(st["exp_ko"], quote=True)
        esc_en = html.escape(st["exp_en"], quote=True)
        q_blocks_html.append(
            f'<div class="q" data-ans="{st["ans"]}" data-exp="{esc_ko}" data-exp-en="{esc_en}">'
            f'<div class="lvl"><span class="bilingual-ko">{st["lvl_ko"]}</span><span class="bilingual-en">{st["lvl_en"]}</span></div>'
            f'<div class="stem"><span class="bilingual-ko">{st["stem_ko"]}</span><div class="bilingual-en">{st["stem_en"]}</div></div>'
            f'<div class="opts">{opts_html}</div>'
            f'<div class="q-actions" style="margin-top:10px;display:flex;justify-content:flex-end">'
            f'<button type="button" class="exp-toggle-btn" onclick="toggleExp(this)">💡 해설 보기</button>'
            f'</div>'
            f'<div class="exp"></div>'
            f'<div class="report-wrap" style="margin-top:10px;border-top:1px solid #e4e2e4;padding-top:10px">'
            f'<button class="report-btn" onclick="toggleReport(this)" style="background:transparent;color:#64748b;border:1px solid #cbd5e1;border-radius:8px;padding:4px 12px;font-size:.75rem;cursor:pointer">🚨 이 문제에 이상이 있어요</button>'
            f'<div class="report-form" style="display:none;margin-top:10px;text-align:left">'
            f'<textarea class="report-text" rows="3" placeholder="이상한 점이나 개선 의견을 적어주세요." style="width:100%;background:#ffffff;color:#1b1b1d;border:1px solid #c5c6cd;border-radius:8px;padding:8px;font-size:.85rem;box-sizing:border-box"></textarea>'
            f'<div style="display:flex;gap:6px;margin-top:6px;justify-content:flex-end">'
            f'<button class="report-cancel" onclick="toggleReport(this)" style="background:transparent;color:#64748b;border:1px solid #cbd5e1;border-radius:8px;padding:4px 10px;font-size:.75rem;cursor:pointer">취소</button>'
            f'<button class="report-submit" onclick="submitReport(this)" style="background:#006398;color:#fff;border:none;border-radius:8px;padding:4px 12px;font-size:.75rem;cursor:pointer">신고 접수</button>'
            f'</div></div>'
            f'<div class="report-msg" style="display:none;color:#059669;font-size:.75rem;margin-top:6px;text-align:right">✅ 신고가 접수되었어요. 확인 후 고칠게요!</div>'
            f'</div></div>'
        )

    page_html = rf"""<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title_ko} · mathedu 수학자료실</title>
<meta name="description" content="교육 현장의 스마트 안경 평가 논란에 수학의 본질로 답하다: 방정식도 좌표축도 없는 순수 포물선 하나에서 평행현과 대칭 원리로 대칭축·초점·준선을 복원하는 6단계 디딤돌 수업">
<meta property="og:site_name" content="mathedu 수학자료실">
<meta property="og:type" content="article">
<meta property="og:title" content="{title_ko} | mathedu">
<meta property="og:description" content="불변의 수학 원문(min7014.github.io) × 살아있는 교육 뉴스 대응 6단계 인터랙티브 디딤돌 수업">
<meta property="og:url" content="https://min7014.github.io/mathedu/board/{slug}.html">
<meta property="og:image" content="https://min7014.github.io/mathedu/assets/og-image.png">
<link rel="canonical" href="https://min7014.github.io/mathedu/board/{slug}.html">
<link rel="icon" type="image/png" sizes="32x32" href="../assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
{stitch_style}
<script>window.MathJax={{tex:{{inlineMath:[['$','$'],['\\(','\\)']]}}}};</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml-full.js"></script>
<script src="../mathedu-i18n.js?v=20261115_en"></script>
</head><body><div class="wrap">
<script>
(function() {{
  try {{
    if (localStorage.getItem('mathedu_site_theme') === 'dark') {{
      document.documentElement.classList.add('dark-theme');
    }}
  }} catch (e) {{}}
}})();
window.syncSiteThemeUI = function() {{
  var isDark = document.documentElement.classList.contains('dark-theme');
  var iconEl = document.getElementById('themeToggleGlobalIcon');
  if (iconEl) iconEl.textContent = isDark ? '☀️' : '🌙';
}};
window.toggleSiteDarkMode = function() {{
  var isDark = document.documentElement.classList.toggle('dark-theme');
  try {{ localStorage.setItem('mathedu_site_theme', isDark ? 'dark' : 'light'); }} catch (e) {{}}
  window.syncSiteThemeUI();
}};
document.addEventListener('DOMContentLoaded', window.syncSiteThemeUI);
</script>
<header class="stitch-app-header">
  <div class="stitch-app-header-inner">
    <a href="/mathedu/" class="stitch-brand-link">
      <img src="../assets/favicon.png" alt="mathedu" class="stitch-brand-logo">
      <div class="stitch-brand-text">
        <span class="stitch-brand-title">mathedu · 수학자료실</span>
        <div class="stitch-brand-sub">
          <span class="stitch-brand-pill"><span class="bilingual-ko">교육이슈 × 수학본질</span><span class="bilingual-en">Edu-Issue × Math Essence</span></span>
          <span class="stitch-brand-code">EDUNEWS01</span>
        </div>
      </div>
    </a>
    <div class="stitch-header-actions">
      <button type="button" id="themeToggleGlobalBtn" class="stitch-lang-toggle" onclick="toggleSiteDarkMode()" title="Toggle Dark/Light Theme"><span id="themeToggleGlobalIcon">🌙</span></button>
      <button type="button" id="langToggleSingleBtn" class="stitch-lang-toggle" onclick="var nextL=(document.documentElement.lang==='en')?'ko':'en';setBoardLang(nextL,true);this.textContent=nextL.toUpperCase();">KO</button>
      <div class="lang-group" style="display:none">
        <button type="button" class="lang-btn active" data-lang-btn="ko" onclick="setBoardLang('ko', true)">한국어</button>
        <button type="button" class="lang-btn" data-lang-btn="en" onclick="setBoardLang('en', true)">English</button>
      </div>
    </div>
  </div>
</header>

<div class="stitch-hero-card">
  <div class="stitch-hero-top">
    <div class="stitch-hero-brand">
      <span class="material-symbols-outlined" style="font-size:20px;color:#006398">explore</span>
      <span><span class="bilingual-ko">교육 뉴스 대응 특별 수업 · 수학자료실</span><span class="bilingual-en">Timely Edu-Issue Lesson · Math Archive</span></span>
    </div>
    <span class="stitch-free-pill"><span class="bilingual-ko">100% 영구 무료</span><span class="bilingual-en">100% Forever Free</span></span>
  </div>
  <h1>
    <span class="bilingual-ko">
      <span class="stitch-h1-main">교육이슈 × 수학본질 01</span>
      <span class="stitch-h1-accent">식도 좌표도 없는 포물선에서 초점·준선 작도하기</span>
    </span>
    <span class="bilingual-en">{title_en}</span>
  </h1>
  <p class="lead">
    <span class="bilingual-ko">카메라로 수식을 찍어 번호를 듣는 웨어러블 기기 논란의 시대 — 읽을 방정식도 객관식 번호도 없는 순수 곡선 하나에서 대칭과 평행현 원리만으로 초점과 준선을 복원해 봅니다.</span>
    <span class="bilingual-en">In an era where wearable cameras read formula plug-in tests in seconds, discover how pure geometric symmetry reconstructs the axis, focus, and directrix from a bare parabola with zero equations.</span>
  </p>
  <div class="stitch-chip-scroll">
    <button type="button" class="stitch-feature-chip" onclick="scrollToQuizStep(0)">
      <span class="material-symbols-outlined" style="font-size:14px;color:#F59E0B">bolt</span>
      <span class="bilingual-ko">1~6단계 초등 눈높이 디딤돌</span><span class="bilingual-en">6-Step Micro-Scaffolding</span>
    </button>
    <a href="../mathlab.html" class="stitch-feature-chip" style="text-decoration:none">
      <span class="material-symbols-outlined" style="font-size:14px;color:#006398">draw</span>
      <span class="bilingual-ko">MathLab 동적 작도 실습</span><span class="bilingual-en">MathLab Dynamic Canvas</span>
    </a>
    <button type="button" class="stitch-feature-chip" onclick="if(window.openClassCreatorModal)openClassCreatorModal('{slug}')">
      <span class="material-symbols-outlined" style="font-size:14px;color:#4F46E5">qr_code_2</span>
      <span class="bilingual-ko">3초 교실 수업 QR</span><span class="bilingual-en">3-Sec Class QR</span>
    </button>
    <button type="button" class="stitch-feature-chip" id="copyBtn" onclick="copyLink()">
      <span class="material-symbols-outlined" style="font-size:14px;color:#10B981">share</span>
      <span class="bilingual-ko">링크 복사 · 공유</span><span class="bilingual-en">Copy Link</span>
    </button>
  </div>
  <div class="stitch-bento-stats">
    <div class="stitch-bento-item">
      <span class="stitch-bento-val" style="color:#1b1b1d">26p</span>
      <span class="stitch-bento-lbl"><span class="bilingual-ko">원문 시각 증명</span><span class="bilingual-en">Original PDF</span></span>
    </div>
    <div class="stitch-bento-item">
      <span class="stitch-bento-val" style="color:#006398"><b id="pts">0</b> / <b id="tot">6</b></span>
      <span class="stitch-bento-lbl"><span class="bilingual-ko">디딤돌 성취</span><span class="bilingual-en">Steps Solved</span></span>
    </div>
    <div class="stitch-bento-item">
      <span class="stitch-bento-val" style="color:#F59E0B" id="pct">0%</span>
      <span class="stitch-bento-lbl"><span class="bilingual-ko">완주율</span><span class="bilingual-en">Progress</span></span>
    </div>
    <div class="stitch-bento-item">
      <span class="stitch-bento-val" style="color:#10B981">KO/EN</span>
      <span class="stitch-bento-lbl"><span class="bilingual-ko">양방향 지원</span><span class="bilingual-en">Bilingual</span></span>
    </div>
    <div class="stitch-progress-wrap">
      <span class="bar"><i id="bar"></i></span>
    </div>
  </div>
</div>

<div class="orig-card">
  <div class="orig-header">
    <div class="orig-tag"><span class="bilingual-ko">🧭 왜 지금 이 수학 탐구인가? (교육 현장의 화두 → 수학의 본질)</span><span class="bilingual-en">🧭 Why This Inquiry Now? (Educational Issue → Mathematical Essence)</span></div>
    <span class="orig-badge"><span class="bilingual-ko">원문 2022040501 · 기하/이차곡선</span><span class="bilingual-en">Archive #2022040501 · Conics</span></span>
  </div>
  <div class="orig-grid">
    <div class="orig-col-media">
      <div class="orig-media-frame">
        <div class="bilingual-ko">{svg_ko}</div>
        <div class="bilingual-en">{svg_en}</div>
      </div>
      <div class="orig-media-sub"><span class="bilingual-ko">▲ 수식 없는 순수 포물선에서 평행현 중점·수직이등분선·45° 반직선으로 초점과 준선을 찾는 작도 모델</span><span class="bilingual-en">▲ Geometric construction recovering axis, vertex, focus, and directrix from a bare parabola</span></div>
    </div>
    <div class="orig-col-desc">
      <div class="orig-text-box">
        <h4><span class="bilingual-ko">📰 현실의 질문과 수학교육의 대응</span><span class="bilingual-en">📰 Real-World Question &amp; Math Education's Response</span></h4>
        <p style="margin:0 0 8px;font-size:0.9rem;line-height:1.65">
          <span class="bilingual-ko">최근 스마트 안경 등 웨어러블 기기를 이용한 시험 부정행위가 사회적 화두가 된 이유는, 기존 시험이 <b>$y^2=8x$에 숫자를 대입해 번호를 고르는 문항</b>에 머물러 있었기 때문입니다. 하지만 <b>방정식도 좌표축도 없는 순수 포물선 곡선 하나</b>만 주어지고 직접 보조선을 작도해 초점과 준선을 복원하라고 하면, 오직 원리를 꿰뚫어 보는 사람의 손끝에서만 해답이 열립니다.</span>
          <span class="bilingual-en">Wearable smart-glasses controversies highlight how easily equation plug-in tests can be read by a camera. Yet when given only a <b>bare parabola curve with zero equations or coordinates</b>, only genuine geometric reasoning—parallel chords, perpendicular bisectors, and symmetry—can unlock its focus and directrix.</span>
        </p>
      </div>
      <div class="orig-tip">
        <span class="bilingual-ko">💡 <b>수업 활용 팁</b>: 교실에서는 종이에 포물선 곡선만 인쇄해 나누어 주거나 <b>MathLab</b> 동적 작도 창을 열어 학생 스스로 대칭축과 초점을 찾아보게 한 뒤, 아래 1~6단계 디딤돌로 대수적 정당화까지 연결해 보세요!</span>
        <span class="bilingual-en">💡 <b>Classroom Tip</b>: Hand out a sheet with only a printed parabola or open <b>MathLab</b> so students construct the axis and focus first, then justify every step algebraically through Steps 1–6 below!</span>
      </div>
    </div>
  </div>
</div>

{"".join(q_blocks_html)}

<div class="sol" id="solSection">
  <div class="bilingual-ko">
    <h3>🏆 [교육이슈×수학본질 01] 전 과정 시각 도형 &amp; 도식화 종합 해설</h3>
    <h4>🎨 [그림으로 이해하는 시각적 도형·개념 다이어그램]</h4>
    <figure class="math-visual-diagram" style="margin:12px 0 18px;padding:14px;background:#f8fafc;border:1.5px solid #cbd5e1;border-radius:14px;text-align:center">{svg_ko}</figure>
    <h4>🗺️ [한눈에 보는 도식화 풀이 흐름도]</h4>
    {flow_ko}
    <h4>🪜 [초등 눈높이 1~6단계 완전 연결 정리]</h4>
    <p>1) 기울기가 같은 두 평행현의 중점 $M_1, M_2$를 이으면 항상 대칭축과 평행합니다($\frac{{y_1+y_2}}{{2}}=\frac{{2p}}{{m}}$).<br>
    2) $M_1M_2$에 수직인 현 $AB$의 수직이등분선을 그으면 곧 <b>대칭축 $\ell$</b>과 <b>꼭짓점 $V$</b>가 복원됩니다.<br>
    3) 꼭짓점 $V$에서 대칭축과 $45^\circ$ 반직선($y=x$)을 그어 포물선과 만나는 점 $Q(4p, 4p)$의 수선의 발 $H(4p, 0)$을 찾고 $\overline{{VH}}$를 $4$등분하면 <b>초점 $F(p,0)$</b>과 <b>준선 $x=-p$</b>가 완벽히 작도됩니다!</p>
  </div>
  <div class="bilingual-en">
    <h3>🏆 [Edu-Issue × Math Essence #01] Complete Visual &amp; Schematic Synthesis</h3>
    <h4>🎨 [Visual Geometric Construction Diagram]</h4>
    <figure class="math-visual-diagram" style="margin:12px 0 18px;padding:14px;background:#f8fafc;border:1.5px solid #cbd5e1;border-radius:14px;text-align:center">{svg_en}</figure>
    <h4>🗺️ [At-a-Glance Schematic Solution Flowchart]</h4>
    {flow_en}
    <h4>🪜 [Complete 6-Step Synthesis]</h4>
    <p>1) Joining midpoints $M_1, M_2$ of any two parallel chords gives a line parallel to the axis of symmetry ($\frac{{y_1+y_2}}{{2}}=\frac{{2p}}{{m}}$).<br>
    2) Constructing the perpendicular bisector of a chord $AB \perp M_1M_2$ recovers the exact <b>Axis $\ell$</b> and <b>Vertex $V$</b>.<br>
    3) Drawing a $45^\circ$ ray ($y=x$) from $V$ meets $y^2=4px$ at $Q(4p,4p)$; quartering $\overline{{VH}}=4p$ locates <b>Focus $F(p,0)$</b> and <b>Directrix $x=-p$</b>, yielding Focus-to-Directrix distance $2p = 6$ when $\overline{{VH}} = 12$.</p>
  </div>
</div>

<div id="min7014-addon" class="min7014-addon-card" style="margin-top:22px;padding:20px;border-radius:16px;background:#ffffff">
  <div class="min-header" style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:12px">
    <div style="display:flex;align-items:center;gap:8px;font-weight:800;font-size:1.02rem">
      <img src="../assets/favicon.png" alt="수학자료실" style="width:24px;height:24px;border-radius:6px">
      <span><span class="bilingual-ko">📚 수학자료실 원문 PDF · 동적 작도 · @min7014_ai 유튜브 채널 직결</span><span class="bilingual-en">📚 Original Archive PDF · Dynamic Geometry · @min7014_ai YouTube</span></span>
    </div>
  </div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px">
    <a class="stitch-collection-card" href="https://min7014.github.io/math2022040501/2022040501.pdf" target="_blank" rel="noopener noreferrer" style="text-decoration:none">
      <div class="stitch-col-left">
        <div class="stitch-col-icon" style="background:rgba(0,99,152,0.10)">
          <span class="material-symbols-outlined" style="font-size:24px;color:#006398">picture_as_pdf</span>
        </div>
        <div>
          <span class="stitch-col-title"><span class="bilingual-ko">원문 26p 단계별 작도 증명 PDF</span><span class="bilingual-en">Original 26-Page Construction PDF</span></span>
          <span class="stitch-col-sub"><span class="bilingual-ko">포물선이 주어졌을 때 대칭축·초점·준선 작도 (min7014.github.io)</span><span class="bilingual-en">Constructing Axis, Focus &amp; Directrix of a Given Parabola</span></span>
        </div>
      </div>
      <span class="material-symbols-outlined" style="font-size:20px;color:#45464d">open_in_new</span>
    </a>
    <a class="stitch-collection-card" href="https://youtu.be/hgb_73tr-jQ" target="_blank" rel="noopener noreferrer" style="text-decoration:none">
      <div class="stitch-col-left">
        <div class="stitch-col-icon" style="background:rgba(245,158,11,0.12)">
          <span class="material-symbols-outlined" style="font-size:24px;color:#D97706">smart_display</span>
        </div>
        <div>
          <span class="stitch-col-title"><span class="bilingual-ko">@min7014_ai 유튜브 시각 증명 열기</span><span class="bilingual-en">Watch on @min7014_ai YouTube Channel</span></span>
          <span class="stitch-col-sub"><span class="bilingual-ko">포물선의 정의와 대칭 원리 1080p 해설 (유튜브 채널 새 탭)</span><span class="bilingual-en">Definition &amp; Symmetry of Parabola (Opens on YouTube)</span></span>
        </div>
      </div>
      <span class="material-symbols-outlined" style="font-size:20px;color:#45464d">open_in_new</span>
    </a>
    <a class="stitch-collection-card" href="../mathlab.html" style="text-decoration:none">
      <div class="stitch-col-left">
        <div class="stitch-col-icon" style="background:rgba(16,185,129,0.12)">
          <span class="material-symbols-outlined" style="font-size:24px;color:#059669">architecture</span>
        </div>
        <div>
          <span class="stitch-col-title"><span class="bilingual-ko">MathLab 동적 기하 실험실</span><span class="bilingual-en">MathLab Dynamic Geometry Studio</span></span>
          <span class="stitch-col-sub"><span class="bilingual-ko">내 손으로 직접 점·평행현·수직이등분선 작도하기</span><span class="bilingual-en">Construct Chords &amp; Perpendicular Bisectors Yourself</span></span>
        </div>
      </div>
      <span class="material-symbols-outlined" style="font-size:20px;color:#45464d">arrow_forward</span>
    </a>
  </div>
</div>

<div class="stitch-footer">
  <div class="stitch-footer-links">
    <a href="https://min7014.github.io/"><span class="bilingual-ko">수학자료실 원문</span><span class="bilingual-en">Original Archive</span></a>
    <span>·</span>
    <a href="https://www.youtube.com/@min7014_ai" target="_blank" rel="noopener noreferrer">@min7014_ai YouTube</a>
    <span>·</span>
    <a href="../index.html"><span class="bilingual-ko">홈으로</span><span class="bilingual-en">Home</span></a>
  </div>
  <p class="stitch-footer-copy"><span class="bilingual-ko">© mathedu · 수학자료실. 불변의 수학 원문과 살아있는 교육 현장의 질문이 만나는 공간.</span><span class="bilingual-en">© mathedu · Math Archive. Connecting timeless visual proofs with living educational questions.</span></p>
</div>
</div>
<script>
function scrollToQuizStep(idx) {{
  var qs = document.querySelectorAll('.q');
  if (qs[idx]) qs[idx].scrollIntoView({{ behavior: 'smooth', block: 'center' }});
}}
function scrollToSolSection() {{
  var sol = document.getElementById('solSection');
  if (sol) sol.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
}}
const qs=document.querySelectorAll('.q');let pts=0;
document.getElementById('tot').textContent=qs.length;
qs.forEach(q=>{{const ans=+q.dataset.ans;const exp=q.querySelector('.exp');
exp.innerHTML=q.dataset.exp;const opts=q.querySelectorAll('.opt');
opts.forEach((o,i)=>{{o.addEventListener('click',()=>{{if(q.classList.contains('done'))return;
q.classList.add('done');opts.forEach((oo,j)=>{{oo.classList.add('locked');if(j+1==ans)oo.classList.add('correct');}});
if(i+1==ans){{o.classList.add('correct');pts++;}}else{{o.classList.add('wrong');}}
exp.classList.add('show');var toggleBtn=q.querySelector('.exp-toggle-btn');if(toggleBtn){{var isEn=(document.documentElement.lang==='en');toggleBtn.textContent=isEn?'💡 Close Explanation':'💡 해설 닫기';}}
document.getElementById('pts').textContent=pts;
const pct=Math.round(pts/qs.length*100);document.getElementById('bar').style.width=pct+'%';
document.getElementById('pct').textContent=pct+'%';}});}});}});
function toggleExp(btn){{
  var q=btn.closest('.q');if(!q)return;var exp=q.querySelector('.exp');if(!exp)return;
  if(exp.classList.contains('show')){{exp.classList.remove('show');btn.textContent=(document.documentElement.lang==='en')?'💡 View Explanation':'💡 해설 보기';}}
  else{{exp.classList.add('show');btn.textContent=(document.documentElement.lang==='en')?'💡 Close Explanation':'💡 해설 닫기';}}
}}
function copyLink(){{const b=document.getElementById('copyBtn');const t=b.textContent;
navigator.clipboard.writeText(location.href).then(()=>{{b.textContent='✅ 복사됨';setTimeout(()=>b.textContent=t,1500);}});}}
function toggleReport(el){{
  var wrap=el.closest('.report-wrap');if(!wrap)return;
  var btn=wrap.querySelector('.report-btn'),form=wrap.querySelector('.report-form');
  if(form.style.display==='none'){{form.style.display='block';btn.style.display='none';}}
  else{{form.style.display='none';btn.style.display='block';}}
}}
function submitReport(btn){{
  var wrap=btn.closest('.report-wrap');
  var qEl=wrap.closest('.q');
  var qNum=qEl?Array.from(document.querySelectorAll('.q')).indexOf(qEl)+1:0;
  var text=(wrap.querySelector('.report-text').value||'').trim();
  var url=window._sheetsApiUrl||'https://script.google.com/macros/s/AKfycbxQBW1hKYFSHokaVJMRql-UJpk0t4qMeWMiiy_RFuCLZ5SE4iZytYQkGa9_yoCmm1Ak0Q/exec';
  var reportUrl=url+'?action=report&quiz={slug}&q='+qNum+'&name=익명&text='+encodeURIComponent(text||'사유 없음')+'&_t='+Date.now();
  try{{fetch(reportUrl,{{mode:'no-cors',keepalive:true}});}}catch(e){{}}
  wrap.querySelector('.report-form').style.display='none';
  wrap.querySelector('.report-msg').style.display='block';
}}
</script>
<script src="../mathedu-room.js?v=20261115_en"></script>
<script src="../mathedu-report.js?v=20261115_fix"></script>
<script>
function updateExplanations(lang) {{
  var isEn = (lang === 'en');
  document.querySelectorAll('.q').forEach(function(q) {{
    var exp = q.querySelector('.exp');
    var btn = q.querySelector('.exp-toggle-btn');
    if (btn) {{
      var isShown = exp && exp.classList.contains('show');
      btn.textContent = isEn ? (isShown ? '💡 Close Explanation' : '💡 View Explanation') : (isShown ? '💡 해설 닫기' : '💡 해설 보기');
    }}
    if (exp) {{
      exp.innerHTML = (isEn && q.dataset.expEn) ? q.dataset.expEn : (q.dataset.exp || '');
    }}
  }});
  var lBtn = document.getElementById('langToggleSingleBtn');
  if (lBtn) lBtn.textContent = isEn ? 'EN' : 'KO';
  if (window.MathJax && window.MathJax.typesetPromise) {{
    try {{ window.MathJax.typesetPromise(); }} catch(e){{}}
  }}
}}
function setBoardLang(lang, isUserAction) {{
  if (lang !== 'ko' && lang !== 'en') return;
  document.documentElement.lang = lang;
  if (isUserAction) {{
    try {{
      localStorage.setItem('mathedu_lang', lang);
      localStorage.setItem('mathedu_lang_manual', 'true');
    }} catch(e){{}}
  }}
  if (isUserAction && window.MatheduI18n && typeof MatheduI18n.setLanguage === 'function') {{
    MatheduI18n.setLanguage(lang);
  }}
  updateExplanations(lang);
  if (window.MatheduI18n && window.MatheduI18n.applyDomTranslations) {{
    try {{ window.MatheduI18n.applyDomTranslations(); }} catch(e){{}}
  }}
}}
(function(){{
  var saved = 'ko';
  try {{
    var p = new URLSearchParams(window.location.search).get('lang');
    if (p === 'en' || p === 'ko') saved = p;
    else if (localStorage.getItem('mathedu_lang_manual') === 'true' && localStorage.getItem('mathedu_lang')) saved = localStorage.getItem('mathedu_lang');
  }} catch(e){{}}
  setBoardLang(saved, false);
}})();
</script>
</body></html>"""

    out_path = BOARD_DIR / f"{slug}.html"
    out_path.write_text(page_html, encoding="utf-8")

    # board/index.json 상단(archive 바로 다음)에 등록하여 메인 탐색기에서 즉시 검색·열람 가능하게 연결
    idx_items = json.loads(BOARD_INDEX_FILE.read_text(encoding="utf-8"))
    idx_items = [it for it in idx_items if it.get("slug") != slug]
    entry = {
        "slug": slug,
        "title": title_ko,
        "title_en": title_en,
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "file": f"{slug}.html",
        "examYear": "2027",
        "examYearAlt": "2026",
        "grade": "고2·고3",
        "month": "특별탐구",
        "subject": "기하(이차곡선·작도)",
        "qNum": "1",
        "source": "교육이슈 × 수학본질 특별 탐구 (원문 2022040501)",
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "tags": [
            "교육이슈",
            "작도",
            "포물선",
            "초점",
            "준선",
            "대칭축",
            "평행현",
            "기하",
            "수행평가",
        ],
        "is_public": True,
    }
    insert_pos = 1 if idx_items and idx_items[0].get("slug") == "archive" else 0
    idx_items.insert(insert_pos, entry)
    BOARD_INDEX_FILE.write_text(json.dumps(idx_items, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


def format_edu_news_summary() -> str:
    db = sync_edu_news_db(timeout=6)
    lines = [
        "📰 [크레딧 0원 · 교육 관련 뉴스 레이더 × 수학 본질 대응 자료 현황]",
        f"• 스캔 시각: {db['updated_at']} (포착된 실시간 교육 시그널 {db['live_edu_news_signals_count']}건)",
        "• 핵심 원칙: 불변의 원문 수학 증명(min7014.github.io) 뿌리 × 살아있는 교육 현안 입구",
        "",
        "📚 [구축 및 매핑된 교육이슈 대응 수업 트랙]",
    ]
    for tr in db["curated_response_tracks"]:
        status_icon = "✅ 라이브 배포됨" if tr["website_lesson_ready"] else "⏳ 순차 제작 대기"
        lines.append(f"• [{tr['track_id']}] {tr['news_theme_ko']} ({status_icon})")
        lines.append(f"  → 원문 증명: {tr['vault_slug']} | 수업: {tr['website_lesson_url'] or tr['lesson_title_ko']}")
    sigs = db.get("live_edu_news_signals") or []
    if sigs:
        lines.append("")
        lines.append("📡 [최근 포착된 실시간 교육 관련 뉴스 헤드라인 Top 4]")
        for s in sigs[:4]:
            lines.append(f"  - ({s['matched_track_id']}) {s['abstracted_topic']}")
    return "\n".join(lines)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "build-flagship":
        p = build_flagship_edunews01_lesson()
        db = sync_edu_news_db(timeout=6)
        print(f"Built {p} and synced {EDU_NEWS_DB_FILE} (signals={db['live_edu_news_signals_count']})")
    elif cmd == "sync":
        db = sync_edu_news_db(timeout=6)
        print(json.dumps(db, ensure_ascii=False, indent=2))
    else:
        print(format_edu_news_summary())
