#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
edu_news_material_engine.py
===============================================================================
📰 학술 수학교육 뉴스 레이더 × min7014.github.io 수학 본질 번역 엔진

[핵심 철학 — Policy 64 & Policy 75]:
  - 민감한 사회적 논란·사건사고 소재를 철저히 배제하고(Policy 75),
    **불변의 수학적 본질(min7014.github.io 1,113+ 원문 증명·작도)**을 뿌리에 두어
    **순수 학술 수학교육 화두(서술형·수행평가 확대, 디지털 탐구교실, 고교학점제 기하·미적분,
    수리논술 정당화 등)**와 원문 시각 증명을 연결합니다.

주요 기능:
  1. 0-크레딧 실시간 학술 수학교육 RSS 스캔 (`scan_live_edu_news`) 및 민감 이슈·상표권·비수학 필터링(auditor 연동)
  2. 순수 수학교육 화두 → 수학적 본질 & min7014.github.io 원문 자산 매핑 (`assets/edu_news_materials_db.json`)
===============================================================================
"""

import silent_subprocess  # noqa: F401 — Rule 48 완전 무창 실행 강제

import datetime
import json
import re
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

EDU_NEWS_RSS_FEEDS = [
    (
        "kr_edu_assessment",
        "https://news.google.com/rss/search?q=%EC%84%9C%EC%88%A0%ED%98%95+%EC%88%98%ED%95%99+OR+%EC%88%98%ED%96%89%ED%8F%89%EA%B0%80+%EC%88%98%ED%95%99+OR+%EC%88%98%ED%95%99+%ED%83%90%EA%B5%AC+%EC%88%98%EC%97%85&hl=ko&gl=KR&ceid=KR:ko",
    ),
    (
        "kr_math_classroom",
        "https://news.google.com/rss/search?q=%EC%88%98%ED%95%99%EA%B5%90%EC%9C%A1+OR+%EC%88%98%EB%A6%AC%EB%85%BC%EC%88%A0+OR+%EA%B3%A0%EA%B5%90%ED%95%99%EC%A0%90%EC%A0%9C+%EA%B8%B0%ED%95%98+%EB%AF%B8%EC%A0%81%EB%B6%84+OR+%EC%88%98%ED%95%99+%EB%AC%B8%ED%95%B4%EB%A0%A5&hl=ko&gl=KR&ceid=KR:ko",
    ),
    (
        "global_math_ed",
        "https://news.google.com/rss/search?q=%22mathematics+education%22+OR+%22visual+proof%22+OR+%22geometry+curriculum%22+OR+%22calculus+education%22&hl=en-US&gl=US&ceid=US:en",
    ),
]

CURATED_EDU_NEWS_TRACKS = [
    {
        "track_id": "edunews02",
        "news_theme_ko": "첨단 우주망원경·광학 렌즈 시대의 기하 교육과 이차곡선 본질",
        "news_theme_en": "Space Telescope Optics Era vs. Formula-Only Conic Section Classrooms",
        "pedagogical_response_ko": "판별식 D=0 기계적 암기 대신, 광원의 빛이 이차곡선 거울에서 반사되어 다른 초점으로 모이는 '타원·포물선 빛 반사 최단거리 대칭 원리'를 수식 0줄로 체득",
        "pedagogical_response_en": "Replace discriminant rote drills with zero-formula mirror-symmetry proofs of focal light reflection in ellipses and parabolas",
        "vault_slug": "2022051507",
        "vault_pdf_url": "https://min7014.github.io/math2022051507/2022051507.pdf",
        "related_youtube_url": "https://youtu.be/hgb_73tr-jQ",
        "lesson_slug": "edunews02",
        "lesson_title_ko": "[수학교육×원문탐구 02] 광학 거울 속 빛은 왜 한 점으로 모일까? 타원 초점 반사 시각 증명",
        "lesson_title_en": "🧭 [Math-Ed × Original Proof #02] Why Do Reflected Rays Converge? Visual Proof of Ellipse Focal Reflection",
        "keywords": ["광학", "렌즈", "반사", "타원", "이차곡선", "기하", "작도", "포물선", "optical", "reflection", "ellipse", "geometry"],
    },
    {
        "track_id": "edunews03",
        "news_theme_ko": "초고속 계산 도구 시대와 '인간 고유의 미적분 구조 문해력' 함양",
        "news_theme_en": "Instant Symbolic Calculation vs. Human Structural Calculus Literacy",
        "pedagogical_response_ko": "단순 미분공식 반복 훈련을 넘어, 포물선의 대칭성 때문에 구간 [a, b]의 평균변화율과 정확히 중점 (a+b)/2의 순간변화율이 일치할 수밖에 없는 기하 구조 통찰",
        "pedagogical_response_en": "Move beyond power-rule drills to see why parabolic symmetry locks the secant slope on [a, b] to the exact midpoint tangent at (a+b)/2",
        "vault_slug": "2019072401",
        "vault_pdf_url": "https://min7014.github.io/math2019072401/2019072401.pdf",
        "related_youtube_url": "https://www.youtube.com/@min7014_ai/videos",
        "lesson_slug": "edunews03",
        "lesson_title_ko": "[수학교육×원문탐구 03] 미분 공식 너머의 직관 — 포물선 중점 접선의 기하학적 필연성",
        "lesson_title_en": "🧭 [Math-Ed × Original Proof #03] Calculus Beyond Power-Rule Drills: Midpoint Tangent Symmetry of a Parabola",
        "keywords": ["인공지능", "디지털교과서", "미분", "평균변화율", "접선", "문해력", "미적분", "ai", "calculus", "derivative"],
    },
    {
        "track_id": "edunews04",
        "news_theme_ko": "서술형·수리논술 평가 확대와 '엄밀한 정의·시각적 정당화' 교육",
        "news_theme_en": "Expansion of Proof-Based Essays & Visual Justification of Theorems",
        "pedagogical_response_ko": "전제 조건 확인 없이 편법 미분만 쓰는 습관을 교정하고, 매개변수 곡선 (g(t), f(t)) 위의 평행 접선 그림 한 장으로 코시의 평균값 정리를 엄밀히 정당화",
        "pedagogical_response_en": "Cure blind shortcut misuse by visualizing Cauchy's Mean Value Theorem as a parallel tangent on a parametric curve (g(t), f(t))",
        "vault_slug": "2016012801",
        "vault_pdf_url": "https://min7014.github.io/math2016012801/2016012801.pdf",
        "related_youtube_url": "https://www.youtube.com/@min7014_ai/videos",
        "lesson_slug": "edunews04",
        "lesson_title_ko": "[수학교육×원문탐구 04] 서술형·논술의 핵심 논리! 매개변수 곡선으로 보는 코시의 평균값 정리",
        "lesson_title_en": "🧭 [Math-Ed × Original Proof #04] Proof Literacy: Seeing Cauchy's Mean Value Theorem via Parametric Curves",
        "keywords": ["서술형", "논술", "수리논술", "수행평가", "평균값", "극한", "정당화", "증명", "essay", "proof"],
    },
]

# Policy 75: 비교육·정치·연예뿐만 아니라 시험 부정행위·커닝·사건사고·소송 등 민감한 사회적 논란 키워드 원천 차단
NON_EDU_NOISE_RE = re.compile(
    r"연예|정치|선거|프로야구|범죄|드라마|아이돌|부정행위|커닝|컨닝|스마트\s*안경|AI\s*안경|웨어러블|"
    r"소송|법원|고소|수사|경찰|적발|단속|검거|자백|논란|비상|오해받기|복장\s*검사|스티커|"
    r"cheat|bounties|scandal|arrest|lawsuit|glasses",
    re.IGNORECASE,
)


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
        "philosophy": "뿌리는 불변의 수학 원문(min7014.github.io), 입구는 순수 학술 수학교육 화두 (Policy 64 & Policy 75)",
        "live_edu_news_signals_count": len(signals),
        "live_edu_news_signals": signals,
        "curated_response_tracks": tracks_out,
    }
    EDU_NEWS_DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    EDU_NEWS_DB_FILE.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")
    return db


def format_edu_news_summary() -> str:
    db = sync_edu_news_db(timeout=6)
    lines = [
        "📰 [크레딧 0원 · 학술 수학교육 뉴스 레이더 × 수학 본질 매핑 현황]",
        f"• 스캔 시각: {db['updated_at']} (포착된 순수 수학교육 시그널 {db['live_edu_news_signals_count']}건)",
        "• 핵심 원칙: 불변의 원문 수학 증명(min7014.github.io) 뿌리 × 순수 학술 수학교육 화두 연결 (민감 사회논란 원천 차단)",
        "",
        "📚 [매핑된 수학교육 원문 탐구 트랙]",
    ]
    for tr in db["curated_response_tracks"]:
        status_icon = "✅ 라이브 배포됨" if tr["website_lesson_ready"] else "📖 원문 증명 직결"
        lines.append(f"• [{tr['track_id']}] {tr['news_theme_ko']} ({status_icon})")
        lines.append(f"  → 원문 증명: {tr['vault_slug']} ({tr['vault_pdf_url']})")
    sigs = db.get("live_edu_news_signals") or []
    if sigs:
        lines.append("")
        lines.append("📡 [최근 포착된 순수 학술 수학교육 헤드라인 Top 4]")
        for s in sigs[:4]:
            lines.append(f"  - ({s['matched_track_id']}) {s['abstracted_topic']}")
    return "\n".join(lines)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "sync":
        db = sync_edu_news_db(timeout=6)
        print(json.dumps(db, ensure_ascii=False, indent=2))
    else:
        print(format_edu_news_summary())
