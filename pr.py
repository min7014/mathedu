#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pr.py — mathedu & 민은기 선생님(MIN EUN GI) 전담 품격 아카이브 홍보 에이전트 (v3.0)
====================================================================================================
수학교사 민은기 선생님이 20여 년의 교단 연구와 현장 수업을 통해 한 땀 한 땀 빚어낸 주옥 같은
수학교육자료(min7014.github.io 1,132+ 주제 · 865+ 단계별 시각 증명 PDF · GeoGebra · AlgeoMath ·
자체 개발 MathLab · 저서 《수학교사와 학생을 위한 GeoGebra와 수학의 시각화》 ISBN 979-11-87541-13-4 ·
16,594+ 탈-5지선다 창의 수학 디딤돌)를 통해 교육자 민은기 선생님의 철학과 업적을 고급스럽게 조명합니다.

[핵심 5대 품격 홍보 아키텍처]
1. 8대 품격 채널 맞춤형 아카이브 홍보 생성기 (build_8channel_messages_for_topic)
   - educator_tribute  : 🏛️ 교육자·명작 아카이브 헌정 소개 (명품 서사·언론·학회 칼럼)
   - teacher_indischool: 🏫 전국 수학교사 연구·수업 나눔 (교단 연구·탐구 수업 키트)
   - student_community : ✒️ 수험생·탐구 학습 정통 칼럼 (원리 중심 사고 에세이)
   - parent_cafe       : 🌿 학부모·수학교육 철학 편지 (무광고·100% 무료 교육 철학)
   - insta_blog        : 🖼️ 인스타·블로그 아틀리에 노트 (기하학의 미학과 지성 아카이브)
   - kakao_challenge   : ✉️ 학급·스터디 품격 수학 초대장 (1초 도전장 딥링크)
   - youtube_pinned    : 📺 유튜브 고정댓글·원문 아카이브 안내 (Rule 13.1/Rule 38 완벽 조화)
   - global_reddit     : 🌐 Global Math Educators & OER Showcase (EN)
2. 박물관 도록급 '플라톤의 사색 서재(Atelier Monograph)' 1200×630 PNG 홍보 배너 렌더링
   - 마스터 헌정 카드(pr_card_min7014_master.png) + 5대 대표 명작 도판 카드 자동 렌더링
3. AI 검색엔진(GEO: llms.txt) & 검색엔진(SEO) 교육자 프로필·원문 아카이브 동기화
4. 24/7 근간 진화 데몬(mathedu_foundation_daemon.py) 상시 연동 (run_autonomous_pr_cycle)
5. CLI: status | kit [slug] | generate | seo | verify
"""

import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
from datetime import datetime
from pathlib import Path

import silent_subprocess  # noqa: F401 — Rule 48: 100% 무창 실행 강제

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent
CATALOG_JSON = ROOT_DIR / "video_lectures" / "catalog.json"
VAULT_JSON = ROOT_DIR / "video_lectures" / "vault_index.json"
DEEP_JSON = ROOT_DIR / "assets" / "min7014_deep_knowledge.json"
PEDAGOGY_JSON = ROOT_DIR / "assets" / "mathteacher_pedagogy_engine.json"
PR_ENGINE_JSON = ROOT_DIR / "assets" / "pr_growth_engine.json"
PR_CARDS_DIR = ROOT_DIR / "assets" / "pr_cards"
LLMS_TXT = ROOT_DIR / "llms.txt"
SITEMAP_XML = ROOT_DIR / "sitemap.xml"

LEGACY_CARD_ALIASES = {
    "2014111901": "pr_card_0001.png",
    "2014111902": "pr_card_0002.png",
    "2017090101": "pr_card_0003.png",
    "math20250130001": "pr_card_0004.png",
    "2025020101": "pr_card_0005.png",
}

CHANNEL_METADATA = [
    {"id": "educator_tribute", "label": "🏛️ 교육자·명작 아카이브 헌정 소개", "badge": "명품 서사 칼럼"},
    {"id": "teacher_indischool", "label": "🏫 전국 수학교사 연구·수업 나눔", "badge": "교단 연구 나눔"},
    {"id": "student_community", "label": "✒️ 수험생·탐구 학습 정통 칼럼", "badge": "본질 탐구 에세이"},
    {"id": "parent_cafe", "label": "🌿 학부모·수학교육 철학 편지", "badge": "원리 중심 교육"},
    {"id": "insta_blog", "label": "🖼️ 인스타·블로그 아틀리에 노트", "badge": "지성 아카이브"},
    {"id": "kakao_challenge", "label": "✉️ 학급·스터디 품격 수학 초대장", "badge": "사색 초대장"},
    {"id": "youtube_pinned", "label": "📺 유튜브 고정댓글·원문 아카이브 안내", "badge": "원문 ➔ 실습 퍼널"},
    {"id": "global_reddit", "label": "🌐 Global Math Educators & OER Showcase (EN)", "badge": "Global Heritage"},
]

FORBIDDEN_HYPE_PHRASES = (
    "\ud1b5\uc554\uae30 \uba48\ucd94\uace0",
    "\ubb34\ub8cc \uc0ac\uc774\ud2b8 \ucd94\ucc9c",
    "\uae09\uc2dd\ub3c4 \uba39\uae30 \uc804\uc5d0",
)

FLAGSHIP_YT_TOPICS = [
    {
        "slug": "2017090101",
        "id": "MIN-KB-0185",
        "legacy_id": "MIN-KB-0003",
        "title": "피타고라스 정리 (25단계 넓이 분할·전단 이동 시각 증명)",
        "title_en": "Pythagorean Theorem (25-Step Area Dissection & Shear Proof)",
        "keyword": "피타고라스",
        "domain": "기하 · 직각삼각형 · 넓이 보존 불변성",
        "hook_ko": "a²+b²=c²이라는 한 줄의 등식을 암기로 건네는 대신, 두 정사각형이 전단 변형과 분할 이동을 거쳐 빗변 위 정사각형으로 빈틈없이 포개지는 25장면의 기하학적 필연성을 교단 위 시각 언어로 정교하게 빚어냈습니다.",
        "yt_ko": "https://youtu.be/7RcvUpfGM6s",
        "yt_en": "https://youtu.be/yZER1pGb2J8",
        "yt_q_ko": "https://youtu.be/E7x3OZdC14U",
        "yt_short_ko": "https://youtube.com/shorts/1RKQ4Uxu4Uw",
        "yt_orig": "https://youtu.be/T5NQWOxuXN4",
        "orig_url": "https://min7014.github.io/math20200113001.html",
        "orig_pdf": "https://min7014.github.io/2020/2017090101.pdf",
        "algeomath": "https://www.algeomath.kr/algeo/algeomath/app/view?id=f527dae4f69211eaaa4bd20d1935fd69",
        "thumb": "video_lectures/youtube_packages/2017090101_ko_thumb.png",
        "steps": 25,
    },
    {
        "slug": "2014111901",
        "id": "MIN-KB-0239",
        "legacy_id": "MIN-KB-0001",
        "title": "메넬라우스의 정리 (20단계 평행보조선 시각 증명)",
        "title_en": "Menelaus' Theorem (20-Step Parallel Auxiliary Line Proof)",
        "keyword": "메넬라우스",
        "domain": "논증기하 · 공선점 · 평행보조선과 닮음비",
        "hook_ko": "분자와 분모의 순서마저 혼동하기 쉬운 삼각형 할선의 비율 공식을, 꼭짓점을 지나는 한 줄의 평행보조선과 20단계 순차 도판으로 풀어내어 중등 닮음 직관만으로 정리가 자연스레 떠오르게 합니다.",
        "yt_ko": "https://youtu.be/CshN2d86plg",
        "yt_en": "https://youtu.be/d0yl3hSHDgE",
        "yt_q_ko": "https://youtu.be/pXjyHgxYzGQ",
        "yt_short_ko": "https://youtube.com/shorts/9uWcbayRrgo",
        "yt_orig": "https://youtu.be/4GVwSo1lQsc",
        "orig_url": "https://min7014.github.io/math20200225001.html",
        "orig_pdf": "https://min7014.github.io/2020/2014111901.pdf",
        "algeomath": "https://www.algeomath.kr/algeo/algeomath/app/view?id=21127107571511eab70f020003750001",
        "thumb": "video_lectures/youtube_packages/2014111901_ko_thumb.png",
        "steps": 20,
    },
    {
        "slug": "2014111902",
        "id": "MIN-KB-0240",
        "legacy_id": "MIN-KB-0002",
        "title": "체바의 정리 (17단계 삼각형 넓이 비 시각 증명)",
        "title_en": "Ceva's Theorem (17-Step Triangle Area Ratio Proof)",
        "keyword": "체바",
        "domain": "논증기하 · 공점 체바선 · 넓이 비 순환 소거",
        "hook_ko": "세 체바선이 한 점에서 만나는 기하학적 조건을 밑변의 비에서 내부 삼각형 넓이의 비로 우아하게 번역하여, 17단계의 맑은 도판 흐름 끝에 순환 약분으로 1이 도출되는 순간의 경이로움을 전합니다.",
        "yt_ko": "https://youtu.be/oq_CJWJ-Zrg",
        "yt_en": "https://youtu.be/aKmG-iKoieQ",
        "yt_q_ko": "https://youtu.be/zvRgbIKm0jc",
        "yt_short_ko": "https://youtube.com/shorts/A1DNOkXcL-w",
        "yt_orig": "https://youtu.be/MHnSJy3lFlk",
        "orig_url": "https://min7014.github.io/math20200228001.html",
        "orig_pdf": "https://min7014.github.io/2020/2014111902.pdf",
        "algeomath": "https://www.algeomath.kr/algeo/algeomath/app/view?id=de1bd69559ac11eab70f020003750001",
        "thumb": "video_lectures/youtube_packages/2014111902_ko_thumb.png",
        "steps": 17,
    },
    {
        "slug": "math20250130001",
        "id": "MIN-KB-0004",
        "legacy_id": "MIN-KB-0004",
        "title": "피타고라스 나무 (11단계 프랙탈 넓이 보존 & 무한급수)",
        "title_en": "Pythagoras Tree (11-Step Fractal Area Conservation)",
        "keyword": "등비급수",
        "domain": "기하와 미적분의 만남 · 프랙탈 넓이 보존",
        "hook_ko": "직각삼각형 위에서 세대를 거듭하며 나무처럼 뻗어 나가는 정사각형들이 매 단계마다 정확히 동일한 총넓이를 품고 있다는 사실을 11단계의 절제된 시각 증명과 GeoGebra 탐구로 생생히 펼쳐 보입니다.",
        "yt_ko": "https://youtu.be/DSgUHigl82o",
        "yt_en": "https://youtu.be/3ik6yQ-0fP8",
        "yt_q_ko": "https://youtu.be/GS9Qj-g-oVo",
        "yt_short_ko": "https://youtube.com/shorts/maGFOifE-2E",
        "yt_orig": "https://youtu.be/vks-ZgCfXpw",
        "orig_url": "https://min7014.github.io/math20250130001.html",
        "orig_pdf": "https://min7014.github.io/2025/2025013001.pdf",
        "geogebra": "https://www.geogebra.org/m/xK2WwJtQ",
        "thumb": "video_lectures/youtube_packages/math20250130001_ko_thumb.png",
        "steps": 11,
    },
    {
        "slug": "2025020101",
        "id": "MIN-KB-0001",
        "legacy_id": "MIN-KB-0005",
        "title": "종이띠로 접는 정칠각형 매듭 원리 (11단계 대칭 작도)",
        "title_en": "Regular Heptagon Paper-Strip Knot Construction (11 Steps)",
        "keyword": "정다각형",
        "domain": "작도와 위상 · 정칠각형 대칭성",
        "hook_ko": "눈금 없는 자와 컴퍼스만으로는 작도할 수 없는 정칠각형이 긴 종이띠 한 가닥의 조용한 매듭 속에서 정확한 각도와 대칭으로 탄생하는 순간을 11단계 도판과 동적 기하로 기록한 작품입니다.",
        "yt_ko": "https://youtu.be/AhBxxFFhfEA",
        "yt_en": "https://youtube.com/shorts/iiO39hbWzhs",
        "yt_short_ko": "https://youtube.com/shorts/OiCRDRdOI_g",
        "yt_orig": "https://youtu.be/dWdB6ivDQZM",
        "orig_url": "https://min7014.github.io/math20250201001.html",
        "orig_pdf": "https://min7014.github.io/2025/2025020101.pdf",
        "geogebra": "https://www.geogebra.org/m/egpbt5m2",
        "thumb": "video_lectures/youtube_packages/2025020101_ko_thumb.png",
        "steps": 11,
    },
]


def _clean_pdf_url(raw_pdf: str) -> str:
    return str(raw_pdf or "").split("#")[0].strip()


def _load_deep_knowledge_index() -> dict:
    """DEEP_JSON(1,132개 주제)을 slug·id·pdf stem으로 인덱싱하여 원문 메타데이터를 결합합니다."""
    idx = {}
    if not DEEP_JSON.exists():
        return idx
    try:
        items = json.loads(DEEP_JSON.read_text(encoding="utf-8"))
    except Exception:
        return idx
    for it in items:
        keys = set()
        if it.get("id"):
            keys.add(str(it["id"]).strip())
        u = str(it.get("url") or "").strip()
        if u:
            keys.add(u.split("/")[-1].replace(".html", "").strip())
        p = _clean_pdf_url(it.get("pdf") or "")
        if p:
            keys.add(p.split("/")[-1].replace(".pdf", "").strip())
        for k in keys:
            if k and k not in idx:
                idx[k] = it
    return idx


def build_8channel_messages_for_topic(topic: dict) -> dict:
    """수학교사 민은기 선생님의 교육 철학과 원문 수학교육자료를 중심으로 8대 품격 홍보 문안을 생성합니다."""
    slug = topic.get("slug", "2017090101")
    title = topic.get("title", "시각적 수학 증명")
    title_en = topic.get("title_en", "Visual Math Proof")
    kw = topic.get("keyword", "기하")
    domain = topic.get("domain", "시각적 수학 증명 · 동적 기하")
    hook = topic.get("hook_ko") or f"[{title}] 개념이 보조선과 기하학적 필연성으로 피어나는 단계별 시각 증명 작품입니다."
    yt_ko = topic.get("yt_ko") or "https://www.youtube.com/@min7014_ai"
    yt_en = topic.get("yt_en") or yt_ko
    yt_orig = topic.get("yt_orig") or ""
    orig_url = topic.get("orig_url") or "https://min7014.github.io/"
    orig_pdf = _clean_pdf_url(topic.get("orig_pdf") or "")
    ggb = str(topic.get("geogebra") or "").strip()
    alg = str(topic.get("algeomath") or "").strip()
    steps = topic.get("steps", 12)

    url_board = f"https://min7014.github.io/mathedu/video_board.html?slug={slug}&from=pr"
    url_quiz = f"https://min7014.github.io/mathedu/index.html?q={kw}&from=pr"
    url_csat27 = "https://min7014.github.io/mathedu/csat2027.html?from=pr"
    url_mathlab = "https://min7014.github.io/2025/mathlab.html"
    url_sub = "https://www.youtube.com/@min7014_ai?sub_confirmation=1"

    provenance_lines = [f"• 원문 아카이브 페이지: {orig_url}"]
    if orig_pdf:
        provenance_lines.append(f"• 단계별 시각 증명 PDF ({steps}단계): {orig_pdf}")
    if ggb:
        provenance_lines.append(f"• GeoGebra 동적 기하 탐구: {ggb}")
    if alg:
        provenance_lines.append(f"• AlgeoMath 작도 실습: {alg}")
    if yt_orig:
        provenance_lines.append(f"• 민은기 선생님 교단 원문 강의: {yt_orig}")
    provenance_block = "\n".join(provenance_lines)

    pin_orig_line = orig_pdf or orig_url

    return {
        "educator_tribute": (
            f"🏛️ [수학교사 민은기 선생님의 교단 아카이브] 《{title}》\n\n"
            f"수학교사가 칠판 앞에서 건네는 가장 깊은 선물은 '암기할 공식'이 아니라 '스스로 깨닫는 눈'입니다.\n"
            f"20여 년 동안 교단과 현장 연구를 지키며 수학의 아름다움을 한 땀 한 땀 작도해 온 수학교사 민은기 선생님(MIN EUN GI)의 방대한 교육 자산 가운데, 오늘 한 편의 작품 《{title}》({domain})을 소개합니다.\n\n"
            f"✒️ 작품 해설\n"
            f"{hook}\n\n"
            f"📜 수학교사 민은기 선생님이 일군 주옥 같은 수학교육 아카이브\n"
            f"{provenance_block}\n"
            f"• 865+ 단계별 시각 증명 PDF · 1,132+ 동적 기하(GeoGebra·AlgeoMath) 및 자체 제작 MathLab ({url_mathlab})\n"
            f"• 저서 《수학교사와 학생을 위한 GeoGebra와 수학의 시각화》(ISBN 979-11-87541-13-4) 및 과학고·대학원 탐구 강의록\n"
            f"• 2027 수능 전 문항({url_csat27}) 포함 16,594+ 기출의 초등 눈높이 디딤돌을 광고·과금 없이 100% 무료 개방\n\n"
            f"🎬 공식 채널 영상(KO): {yt_ko}\n"
            f"🌐 통합 시각 증명 극장: {url_board}\n"
            f"✍️ 창의 구성 기출 스튜디오: {url_quiz}"
        ),
        "teacher_indischool": (
            f"🏫 [교단 연구 나눔 · 수학교사 민은기 선생님의 시각 증명 자료] 《{title}》\n\n"
            f"현장에서 아이들에게 개념의 필연성을 전하고자 고민하시는 선생님들께, 20여 년 교단 연구의 결실인 수학교사 민은기 선생님의 시각적 증명 아카이브를 정중히 나눕니다.\n"
            f"{hook}\n\n"
            f"📐 수업 활용 원문 자료 ({steps}단계 플립북 PDF · 동적 기하)\n"
            f"{provenance_block}\n"
            f"• 전자칠판 연동 시각 증명 게시판: {url_board}\n"
            f"• 자체 개발 동적 작도 MathLab: {url_mathlab}\n"
            f"• 5지선다 배제 창의 수식 구성 실습(2027 수능 포함 16,594+문항): {url_quiz}\n\n"
            f"수업 도입부 5분 동안 원문 PDF 도판과 영상을 학생들과 함께 관찰하며 '왜 이 보조선이 자연스러운가'를 발문으로 열어 보시면 깊은 탐구 수업이 펼쳐집니다. 모든 자료는 교실과 학생을 위해 100% 무료·무광고로 개방되어 있습니다."
        ),
        "student_community": (
            f"✒️ [본질로 꿰뚫는 수학의 시선] 수학교사 민은기 선생님의 《{title}》 단계별 시각 증명\n\n"
            f"풀이의 첫 줄을 외우려 하면 수학은 버거워지지만, 도형이 움직이고 넓이가 이동하는 필연적인 장면을 눈으로 확인하면 공식은 자연스럽게 내 것이 됩니다.\n"
            f"수학교사 민은기 선생님께서 20여 년간 학생들을 위해 집대성한 《{title}》 시각 증명 도판을 따라가 보시기 바랍니다.\n\n"
            f"• 💡 핵심 통찰: {hook}\n"
            f"• 📄 원문 단계별 증명 도판({steps}단계): {orig_url}\n"
            f"• 🎬 1080p 시각 증명 해설: {yt_ko}\n"
            f"• 🌐 동적 기하 체험 · 아카이브 게시판: {url_board}\n"
            f"• ✍️ 보기를 가리고 직접 식을 세워 보는 기출 디딤돌(2027 수능 포함): {url_quiz}\n\n"
            f"배움에 들이는 노력을 귀하게 여기는 선생님의 철학에 따라 전 과정이 별도 비용 없이 열려 있습니다."
        ),
        "parent_cafe": (
            f"🌿 [수학교육 에세이] 20년 교단 수학교사 민은기 선생님이 학생들에게 남긴 무광고·무료 시각 수학 아카이브\n\n"
            f"아이가 수학 공식을 외우느라 지쳐 있을 때, 현직에서 오랜 세월 아이들을 가르친 수학교사 민은기 선생님이 직접 설계한 '눈으로 이해하는 수학 아카이브'를 권해 드립니다.\n\n"
            f"• 오늘의 명작 자료: 《{title}》\n"
            f"• 교육적 가치: {hook}\n"
            f"• 원문 아카이브 열람: {orig_url}\n"
            f"• 시각 증명 영상({steps}단계): {yt_ko}\n"
            f"• 초등 직관부터 수능까지 촘촘히 잇는 디딤돌 문제실: {url_quiz}\n\n"
            f"865+편의 단계별 시각 증명 PDF와 1,132+개의 동적 기하 탐구 자료, 16,594+문항의 단계별 디딤돌이 '공부에 참여하는 노력 자체를 응원한다'는 선생님의 뜻 아래 상업 광고 없이 전량 무료로 공개되어 있습니다."
        ),
        "insta_blog": (
            f"🖼️ [Atelier of Mathematics · 수학교사 민은기 선생님의 시각 증명 노트]\n"
            f"《{title}》\n\n"
            f"{hook}\n\n"
            f"수학교사 민은기 선생님(MIN EUN GI)의 20년 교단 아카이브는 단 하나의 질문에서 시작합니다.\n"
            f"'학생이 공식을 외우기 전에, 그 진리를 눈으로 먼저 목격할 수 없을까?'\n\n"
            f"📜 원문 도판 & 자료: {orig_url}\n"
            f"🎬 시각 증명 극장: {yt_ko}\n"
            f"🧭 인터랙티브 보드: {url_board}\n"
            f"🏛️ 수학자료실 전체 1,132+ 컬렉션: https://min7014.github.io/\n\n"
            f"#민은기선생님 #민은기선생님의수학자료실 #시각적수학증명 #수학교육 #기하학 #지오지브라 #알지오매스 #MathLab #mathedu"
        ),
        "kakao_challenge": (
            f"✉️ [함께 사색하는 오늘의 수학 명작 초대장]\n"
            f"🏛️ 수학교사 민은기 선생님의 수학자료실 × mathedu 아카이브\n"
            f"📌 작품: 《{title}》 ({domain})\n\n"
            f"💡 {hook}\n\n"
            f"1) 📜 원문 시각 증명 ({steps}단계): {orig_url}\n"
            f"2) 🎬 1080p 해설 영상: {yt_ko}\n"
            f"3) 🧭 동적 기하 & 영상 극장: {url_board}\n"
            f"4) ✍️ 관련 기출 스스로 식 세우기: {url_quiz}"
        ),
        "youtube_pinned": (
            f"🏛️ [민은기 선생님의 단계별 시각적 수학 증명 (@min7014_ai) · 원문 아카이브 안내]\n"
            f"📐 오리지널 원문 자료 & 시각 증명 PDF (https://min7014.github.io/): {pin_orig_line}\n\n"
            f"오늘 영상으로 만나보신 《{title}》은 교단에서 직접 제작한 {steps}단계 시각 증명 원문을 한 페이지씩 정교하게 짚어 구성했습니다.\n"
            f"• GeoGebra · AlgeoMath 통합 시각 증명 보드: {url_board}\n"
            f"• 자체 개발 동적 기하 도구 MathLab: {url_mathlab}\n"
            f"• 5지선다 없이 식을 직접 구성해 푸는 기출 디딤돌 (16,594+문항): {url_quiz}\n"
            f"• 2027 수능 수학 전 문항(46문항) 특별관: {url_csat27}\n"
            f"🔔 채널 구독하고 매일 새로운 수학적 통찰을 만나보세요: {url_sub}"
        ),
        "global_reddit": (
            f"🏛️ [Archival Visual Mathematics · Works of Educator MIN EUN GI] {title_en}\n\n"
            f"Created over two decades of classroom teaching by Korean mathematics educator MIN EUN GI (민은기), "
            f"this visual monograph decomposes '{title_en}' into {steps} illuminated steps so learners witness geometric necessity before memorizing symbols.\n\n"
            f"• Primary Monograph & PDF ({steps} steps): {orig_pdf or orig_url}\n"
            f"• Archival Topic Page: {orig_url}\n"
            f"• Visual Proof Cinema (EN): {yt_en}\n"
            f"• Bilingual Lecture (KO): {yt_ko}\n"
            f"• Interactive Archive & GeoGebra/AlgeoMath Board (1,132+ works): {url_board}\n"
            f"• Author's Constructive Math Studio (16,594+ scaffolded problems, 100% ad-free & free OER): {url_quiz}\n"
            f"• Reference Book: GeoGebra and Visualization of Mathematics (ISBN 979-11-87541-13-4) | Channel: {url_sub}"
        ),
    }


build_7channel_messages_for_topic = build_8channel_messages_for_topic


def _load_curatorial_font(size: int, bold: bool = True, latin_serif: bool = False):
    from PIL import ImageFont

    cands = (
        [r"C:\Windows\Fonts\georgiab.ttf", r"C:\Windows\Fonts\georgia.ttf", r"C:\Windows\Fonts\timesbd.ttf"]
        if latin_serif
        else [
            r"C:\Windows\Fonts\malgunbd.ttf" if bold else r"C:\Windows\Fonts\malgun.ttf",
            r"C:\Windows\Fonts\malgunbd.ttf",
            r"C:\Windows\Fonts\NanumGothicBold.ttf",
            r"C:\Windows\Fonts\arialbd.ttf",
        ]
    )
    for fp in cands:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _render_original_pdf_plate(pdf_url: str, slug: str, thumb_rel: str, target_w: int, target_h: int):
    """min7014.github.io 원문 PDF의 핵심 증명 도판을 220 DPI로 무왜곡 렌더링합니다."""
    from PIL import Image

    clean_pdf = _clean_pdf_url(pdf_url)
    if clean_pdf and "min7014.github.io" in clean_pdf.lower():
        try:
            import pymupdf
            import min7014_video_maker as vmaker

            pdf_bytes, _ = vmaker.load_or_build_topic_pdf_bytes(clean_pdf, slug)
            if pdf_bytes:
                with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
                    if len(doc) >= 1:
                        key_idx = max(0, len(doc) - 2)
                        pix = doc[key_idx].get_pixmap(dpi=200)
                        im = vmaker._mask_pdf_bottom_author_bar(
                            Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        )
                        sc = min(target_w / im.width, target_h / im.height)
                        nw, nh = max(1, int(im.width * sc)), max(1, int(im.height * sc))
                        return im.resize((nw, nh), Image.Resampling.LANCZOS)
        except Exception:
            pass

    thumb_p = ROOT_DIR / str(thumb_rel or "")
    if thumb_p.exists():
        try:
            im = Image.open(thumb_p).convert("RGB")
            sc = min(target_w / im.width, target_h / im.height)
            return im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.Resampling.LANCZOS)
        except Exception:
            pass
    return None


def _draw_atelier_card_frame(canvas, draw, W: int = 1200, H: int = 630):
    """플라톤의 사색 서재·박물관 도록풍 1200x630 다크 옵시디언 & 앤틱 골드 프레임"""
    obsidian = (10, 16, 30)
    panel = (17, 25, 45)
    gold = (212, 175, 55)
    gold_soft = (140, 118, 52)
    draw.rectangle([0, 0, W, H], fill=obsidian)
    for gx in range(40, W, 80):
        draw.line([(gx, 0), (gx, H)], fill=(15, 23, 42), width=1)
    for gy in range(40, H, 80):
        draw.line([(0, gy), (W, gy)], fill=(15, 23, 42), width=1)
    draw.rounded_rectangle([14, 14, W - 15, H - 15], radius=16, outline=gold, width=2, fill=None)
    draw.rounded_rectangle([22, 22, W - 23, H - 23], radius=12, outline=gold_soft, width=1, fill=None)
    return obsidian, panel, gold


def _draw_fitted_text_lines(draw, x: int, y: int, text: str, max_w: int, start_size: int, wrap_width: int, max_lines: int, fill, bold: bool = True, line_gap: int = 8) -> int:
    font = _load_curatorial_font(start_size, bold=bold)
    lines = textwrap.wrap(text, width=wrap_width)[:max_lines]
    cur_y = y
    for ln in lines:
        f_use = font
        sz = start_size
        while sz > 14:
            f_try = _load_curatorial_font(sz, bold=bold)
            bb = draw.textbbox((0, 0), ln, font=f_try)
            if bb[2] - bb[0] <= max_w:
                f_use = f_try
                break
            sz -= 2
        draw.text((x, cur_y), ln, font=f_use, fill=fill)
        bb = draw.textbbox((0, 0), ln, font=f_use)
        cur_y += (bb[3] - bb[1]) + line_gap
    return cur_y


def generate_pr_visual_cards():
    """플라톤의 사색 서재(Atelier Monograph) 양식의 1200x630 박물관 도록형 홍보 카드를 렌더링합니다."""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return []

    PR_CARDS_DIR.mkdir(parents=True, exist_ok=True)
    generated = []
    ivory = (248, 245, 236)
    slate = (203, 213, 225)
    sky_muted = (125, 211, 252)
    mint_muted = (110, 231, 183)
    f_serif_hdr = _load_curatorial_font(17, bold=True, latin_serif=True)
    f_kicker = _load_curatorial_font(20, bold=True)
    f_meta = _load_curatorial_font(18, bold=False)
    f_foot = _load_curatorial_font(19, bold=True)

    # 1. 주제별 명작 도판 카드 5종 (+ 레거시 0001..0005 동기화)
    plates_for_master = []
    for topic in FLAGSHIP_YT_TOPICS:
        slug = topic["slug"]
        out_path = PR_CARDS_DIR / f"pr_card_{slug}.png"
        canvas = Image.new("RGB", (1200, 630), (10, 16, 30))
        draw = ImageDraw.Draw(canvas)
        _, panel, gold = _draw_atelier_card_frame(canvas, draw)

        draw.text((48, 44), "MIN EUN GI · ARCHIVE MONOGRAPH", font=f_serif_hdr, fill=gold)
        draw.line([(48, 72), (650, 72)], fill=(71, 85, 105), width=1)
        draw.text((48, 86), "수학교사 민은기 선생님의 주옥 같은 시각 증명 작품", font=f_kicker, fill=sky_muted)

        clean_t = topic["title"].split("(")[0].strip()
        next_y = _draw_fitted_text_lines(draw, 48, 128, clean_t, max_w=604, start_size=34 if len(clean_t) > 12 else 44, wrap_width=24, max_lines=2, fill=ivory, bold=True, line_gap=10)
        draw.text((48, next_y + 8), f"{topic.get('domain', '시각적 수학 증명')}  ·  {topic.get('steps', 12)}단계 원문 도판", font=f_kicker, fill=gold)

        hook_y = max(258, next_y + 46)
        draw.rounded_rectangle([48, hook_y, 654, 466], radius=14, fill=panel, outline=(71, 85, 105), width=2)
        draw.rectangle([58, hook_y + 18, 63, hook_y + 106], fill=gold)
        _draw_fitted_text_lines(draw, 80, hook_y + 20, topic["hook_ko"], max_w=556, start_size=20, wrap_width=32, max_lines=4, fill=slate, bold=False, line_gap=7)
        draw.text((80, 424), "저서 ISBN 979-11-87541-13-4  ·  865+ 시각 증명 PDF  ·  MathLab", font=f_meta, fill=mint_muted)

        # 우측: 실제 min7014.github.io 원문 PDF 핵심 도판 (Gallery Plate Frame)
        draw.rounded_rectangle([682, 46, 1154, 526], radius=14, fill=(14, 21, 38), outline=gold, width=2)
        plate = _render_original_pdf_plate(topic.get("orig_pdf", ""), slug, topic.get("thumb", ""), 444, 412)
        if plate is not None:
            px = 682 + (472 - plate.width) // 2
            py = 62 + (420 - plate.height) // 2
            draw.rectangle([px - 4, py - 4, px + plate.width + 4, py + plate.height + 4], outline=(226, 232, 240), width=2, fill=(255, 255, 255))
            canvas.paste(plate, (px, py))
            if slug in ("2017090101", "2014111902", "math20250130001", "2025020101"):
                plates_for_master.append((clean_t, plate))
        draw.text((700, 492), f"Original PDF Plate · {topic.get('id', slug)}", font=f_meta, fill=gold)

        # 하단 아카이브 바
        draw.rectangle([24, 548, 1176, 606], fill=(15, 28, 54))
        draw.line([(24, 548), (1176, 548)], fill=gold, width=1)
        draw.text((48, 566), "민은기 선생님의 수학자료실 (min7014.github.io)  |  1,132+ 동적 기하 · 16,594+ 기출 100% 무료 개방", font=f_foot, fill=ivory)

        canvas.save(out_path, "PNG")
        generated.append(str(out_path.relative_to(ROOT_DIR)).replace("\\", "/"))

        alias_name = LEGACY_CARD_ALIASES.get(slug)
        if alias_name:
            alias_p = PR_CARDS_DIR / alias_name
            shutil.copy2(out_path, alias_p)
            generated.append(str(alias_p.relative_to(ROOT_DIR)).replace("\\", "/"))

    # 2. 교육자 헌정 마스터 전시 카드 (pr_card_min7014_master.png)
    master_path = PR_CARDS_DIR / "pr_card_min7014_master.png"
    m_canvas = Image.new("RGB", (1200, 630), (10, 16, 30))
    m_draw = ImageDraw.Draw(m_canvas)
    _, m_panel, m_gold = _draw_atelier_card_frame(m_canvas, m_draw)

    m_draw.text((48, 44), "EDUCATOR HERITAGE ARCHIVE · MIN EUN GI", font=f_serif_hdr, fill=m_gold)
    m_draw.line([(48, 72), (620, 72)], fill=(71, 85, 105), width=1)
    _draw_fitted_text_lines(m_draw, 48, 92, "수학교사 민은기 선생님의", max_w=560, start_size=36, wrap_width=18, max_lines=1, fill=sky_muted, bold=True)
    _draw_fitted_text_lines(m_draw, 48, 144, "주옥 같은 수학교육 컬렉션", max_w=560, start_size=44, wrap_width=16, max_lines=1, fill=ivory, bold=True)

    m_draw.rounded_rectangle([48, 224, 608, 524], radius=14, fill=m_panel, outline=m_gold, width=2)
    stats_rows = [
        ("1,132+ 심층 주제", "원리 중심 동적 기하·공학 탐구 아카이브"),
        ("865+ 단계별 PDF", "학생의 눈으로 진리를 목격하는 시각 증명"),
        ("16,594+ 기출 디딤돌", "2027 수능 포함 탈-5지선다 창의 구성"),
        ("저서 · MathLab", "저서 ISBN 979-11-87541-13-4 · 자체 MathLab"),
    ]
    ry = 248
    for badge_t, desc_t in stats_rows:
        m_draw.rounded_rectangle([70, ry, 258, ry + 40], radius=8, fill=(24, 38, 68), outline=m_gold, width=1)
        _draw_fitted_text_lines(m_draw, 82, ry + 8, badge_t, max_w=166, start_size=18, wrap_width=40, max_lines=1, fill=m_gold, bold=True, line_gap=2)
        _draw_fitted_text_lines(m_draw, 270, ry + 10, desc_t, max_w=322, start_size=17, wrap_width=80, max_lines=1, fill=ivory, bold=False, line_gap=2)
        ry += 66

    # 우측 2x2 박물관 도판 갤러리
    m_draw.rounded_rectangle([632, 46, 1154, 524], radius=14, fill=(14, 21, 38), outline=m_gold, width=2)
    m_draw.text((656, 62), "Selected Original Proof Plates · min7014.github.io", font=f_serif_hdr, fill=m_gold)
    slots = [(654, 98), (906, 98), (654, 304), (906, 304)]
    for (sx, sy), (pt_title, p_im) in zip(slots, plates_for_master[:4]):
        thumb_tile = p_im.resize((226, 168), Image.Resampling.LANCZOS)
        m_draw.rectangle([sx - 2, sy - 2, sx + 228, sy + 170], outline=(226, 232, 240), width=1, fill=(255, 255, 255))
        m_canvas.paste(thumb_tile, (sx, sy))
        tile_lbl = "정칠각형 매듭 원리" if "정칠각형" in pt_title else pt_title[:16]
        _draw_fitted_text_lines(m_draw, sx + 2, sy + 174, tile_lbl, max_w=222, start_size=15, wrap_width=24, max_lines=1, fill=slate, bold=True, line_gap=2)

    m_draw.rectangle([24, 548, 1176, 606], fill=(15, 28, 54))
    m_draw.line([(24, 548), (1176, 548)], fill=m_gold, width=1)
    m_draw.text((48, 566), "https://min7014.github.io/   ·   mathedu   ·   @min7014_ai   |   광고·과금 ZERO 100% 무료 개방", font=f_foot, fill=ivory)
    m_canvas.save(master_path, "PNG")
    generated.append(str(master_path.relative_to(ROOT_DIR)).replace("\\", "/"))

    return sorted(set(generated))


def build_pr_growth_engine_data() -> dict:
    """CATALOG_JSON, DEEP_JSON(1,132주제)을 통합 분석하여 assets/pr_growth_engine.json을 생성합니다."""
    cat_list = []
    if CATALOG_JSON.exists():
        try:
            cat_list = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))
        except Exception:
            cat_list = []

    deep_idx = _load_deep_knowledge_index()
    topics_map = {}

    for t in FLAGSHIP_YT_TOPICS:
        slug = t["slug"]
        dk = deep_idx.get(slug, {})
        merged = dict(t)
        merged.setdefault("geogebra", dk.get("geogebra", ""))
        merged.setdefault("algeomath", dk.get("algeomath", ""))
        merged["is_lecture"] = bool(dk.get("is_lecture"))
        merged["is_construction"] = bool(dk.get("is_construction"))
        topics_map[slug] = merged

    for c in cat_list:
        slug = str(c.get("slug") or "").strip()
        if not slug or slug in topics_map:
            continue
        dk = deep_idx.get(slug, {})
        yt_ko = (c.get("youtube_urls") or {}).get("ko") or ""
        yt_en = (c.get("youtube_urls") or {}).get("en") or ""
        yt_orig = dk.get("youtube") or (c.get("youtube_urls") or {}).get("orig") or ""
        raw_title = (c.get("title") or c.get("title_ko") or dk.get("title_ko") or slug).strip()
        clean_title = raw_title.split("(")[0].strip() or raw_title
        orig_pdf = _clean_pdf_url(dk.get("pdf") or c.get("pdf_url") or "")
        orig_url = str(dk.get("url") or "https://min7014.github.io/").strip()
        core_c = re.sub(r"\s+", " ", str(dk.get("core_concept") or "")).strip()
        steps = int(c.get("page_count") or 12)
        hook_ko = core_c[:160] if core_c else f"[{clean_title}] 수학교사 민은기 선생님이 {steps}단계 시각 증명과 동적 기하 직관으로 집대성한 교육 자료입니다."

        topics_map[slug] = {
            "slug": slug,
            "id": dk.get("id") or f"MIN-VID-{slug}",
            "title": f"{clean_title} ({steps}단계 시각 증명)",
            "title_en": (c.get("title_en") or dk.get("title_en") or raw_title).strip(),
            "keyword": clean_title.split()[0] if clean_title else "기하",
            "domain": dk.get("category") or "시각적 수학 증명 · 동적 기하",
            "hook_ko": hook_ko,
            "yt_ko": yt_ko or "https://www.youtube.com/@min7014_ai",
            "yt_en": yt_en or "https://www.youtube.com/@min7014_ai",
            "yt_orig": yt_orig,
            "orig_url": orig_url,
            "orig_pdf": orig_pdf,
            "geogebra": dk.get("geogebra", ""),
            "algeomath": dk.get("algeomath", ""),
            "steps": steps,
        }

    card_paths = generate_pr_visual_cards()

    campaigns = []
    for slug, t in topics_map.items():
        msgs = build_8channel_messages_for_topic(t)
        card_rel = f"assets/pr_cards/pr_card_{slug}.png"
        if not (ROOT_DIR / card_rel).exists():
            card_rel = "assets/pr_cards/pr_card_min7014_master.png"
        campaigns.append({
            "slug": t["slug"],
            "id": t["id"],
            "title": t["title"],
            "title_en": t.get("title_en", t["title"]),
            "keyword": t.get("keyword", "기하"),
            "domain": t.get("domain", ""),
            "orig_url": t.get("orig_url", "https://min7014.github.io/"),
            "orig_pdf": _clean_pdf_url(t.get("orig_pdf", "")),
            "yt_ko": t.get("yt_ko", "https://www.youtube.com/@min7014_ai"),
            "yt_en": t.get("yt_en", "https://www.youtube.com/@min7014_ai"),
            "steps": t.get("steps", 12),
            "pr_card_url": card_rel,
            "channels": msgs,
        })

    payload = {
        "agent": "pr (Educator Heritage & Atelier Monograph PR Director v3.0)",
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "stats": {
            "total_campaigns": len(campaigns),
            "channels_per_campaign": len(CHANNEL_METADATA),
            "total_ready_posts": len(campaigns) * len(CHANNEL_METADATA),
            "visual_pr_cards": len(card_paths),
            "deep_archive_topics": len(deep_idx) or 1132,
        },
        "channel_Metadata": CHANNEL_METADATA,
        "campaigns": campaigns,
    }

    PR_ENGINE_JSON.parent.mkdir(parents=True, exist_ok=True)
    # Compact JSON keeps browser fetch under ~7 MB while delivering all 8 enriched channels
    PR_ENGINE_JSON.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return payload


def sync_seo_and_geo_manifests():
    """llms.txt에 수학교사 민은기 선생님(MIN EUN GI)의 교육자 아카이브 프로필 및 대표 시각 증명 작품을 동기화합니다."""
    if not LLMS_TXT.exists():
        return
    txt = LLMS_TXT.read_text(encoding="utf-8")

    # 1. 최상단 소개부 보강 (범용 요약 대신 교육자 민은기 선생님 아카이브 명기)
    lines = txt.splitlines()
    if lines and lines[0].startswith("# mathedu"):
        lines[0] = "# mathedu · 민은기 선생님의 수학자료실 (Mathematics Heritage Archive & Scaffolding Platform)"
        if len(lines) >= 3 and lines[2].startswith("> "):
            lines[2] = (
                "> Authored and curated over 20+ years by Korean mathematics teacher MIN EUN GI (민은기 선생님): "
                "1,132+ dynamic geometry & math engineering explorations, 865+ step-by-step visual proof PDFs, "
                "monograph ISBN 979-11-87541-13-4, custom MathLab software, and 16,594+ CSAT scaffolding problems (100% free & ad-free OER)."
            )
        txt = "\n".join(lines) + "\n"

    # 2. 하단 AI 검색엔진 교육자·영상 아카이브 블록 동기화
    old_marker = "## 📺 Official @min7014_ai YouTube Visual Proof Cinema & Bi-Directional Funnel"
    new_marker = "## 🏛️ Educator Heritage & Visual Proof Archive — MIN EUN GI (수학교사 민은기 선생님)"
    section_lines = [
        new_marker,
        "- Original Author & Educator: MIN EUN GI (민은기 선생님 · Mathematics Teacher & Curriculum Researcher)",
        "- Primary Archive: https://min7014.github.io/ (1,132+ curated deep-knowledge topics · 865+ original visual proof PDFs)",
        "- Published Book: 《수학교사와 학생을 위한 GeoGebra와 수학의 시각화》 (ISBN 979-11-87541-13-4)",
        "- Custom Dynamic Geometry Software: MathLab (https://min7014.github.io/2025/mathlab.html)",
        "- Official YouTube Channel (@min7014_ai — 민은기 선생님의 단계별 시각적 수학 증명): https://www.youtube.com/@min7014_ai",
        "- Interactive Visual Proof Theater: https://min7014.github.io/mathedu/video_board.html",
        "- De-Multiple-Choice Constructive Math Studio (16,594+ Problems, 2027 CSAT Included): https://min7014.github.io/mathedu/csat2027.html",
        "- Flagship Original Visual Proof Monographs & Bilingual Cinema:",
    ]
    for t in FLAGSHIP_YT_TOPICS:
        section_lines.append(
            f"  * {t['title']} / {t['title_en']}: Archive {t.get('orig_url')} | PDF {t.get('orig_pdf')} | KO {t['yt_ko']} | EN {t['yt_en']} | Board https://min7014.github.io/mathedu/video_board.html?slug={t['slug']}"
        )
    new_block = "\n".join(section_lines) + "\n"

    for mk in (new_marker, old_marker):
        if mk in txt:
            txt = txt.split(mk)[0].rstrip() + "\n\n" + new_block
            break
    else:
        txt = txt.rstrip() + "\n\n" + new_block
    LLMS_TXT.write_text(txt, encoding="utf-8")


def run_autonomous_pr_cycle(last_slug: str = ""):
    payload = build_pr_growth_engine_data()
    sync_seo_and_geo_manifests()
    print(
        f"🏛️ [PR Agent v3.0 Heritage Cycle] {payload['stats']['total_campaigns']}개 주제 × {payload['stats']['channels_per_campaign']}대 채널 "
        f"({payload['stats']['total_ready_posts']}종 품격 홍보 문구) & 아틀리에 도록 카드 동기화 완료 (최근: {last_slug or 'ALL'})",
        flush=True,
    )
    return payload


def cmd_status():
    payload = build_pr_growth_engine_data()
    sync_seo_and_geo_manifests()
    llms_size = LLMS_TXT.stat().st_size if LLMS_TXT.exists() else 0
    sitemap_size = SITEMAP_XML.stat().st_size if SITEMAP_XML.exists() else 0
    print("=" * 78)
    print("🏛️ [pr v3.0] 수학교사 민은기 선생님 명작 아카이브 기반 품격 홍보 에이전트")
    print("=" * 78)
    print(f"• 홍보 데이터베이스           : assets/pr_growth_engine.json ({PR_ENGINE_JSON.stat().st_size:,} bytes)")
    print(f"• 구축된 캠페인 규모          : {payload['stats']['total_campaigns']}개 주제 × {payload['stats']['channels_per_campaign']}대 채널 = {payload['stats']['total_ready_posts']}종 맞춤 키트")
    print(f"• 아카이브 보유 원문 규모     : {payload['stats']['deep_archive_topics']}개 심층 주제 · 865+ 시각 증명 PDF · 16,594+ 기출")
    print(f"• 아틀리에 도록 카드(1200x630): assets/pr_cards/ ({payload['stats']['visual_pr_cards']}종 PNG — pr_card_min7014_master.png 포함)")
    print(f"• AI 검색 매니페스트(GEO)     : llms.txt ({llms_size:,} bytes · MIN EUN GI 프로필 동기화)")
    print(f"• 검색엔진 사이트맵(SEO)      : sitemap.xml ({sitemap_size:,} bytes)")
    print("=" * 78)


def cmd_kit(target_slug: str = "2017090101"):
    payload = build_pr_growth_engine_data()
    alias_map = {"0001": "2014111901", "0002": "2014111902", "0003": "2017090101", "0004": "math20250130001", "0005": "2025020101", "master": "2017090101", "min7014": "2017090101"}
    norm_slug = alias_map.get(target_slug, target_slug)
    camps = payload.get("campaigns", [])
    chosen = next((c for c in camps if c["slug"] == norm_slug), camps[0] if camps else None)
    if not chosen:
        print("캠페인 데이터가 없습니다.")
        return
    print("=" * 78)
    print(f"🏛️ [pr v3.0] '{chosen['title']}' 8대 채널 품격 홍보 키트")
    print("=" * 78)
    for ch_meta in payload["channel_Metadata"]:
        cid = ch_meta["id"]
        print(f"\n{ch_meta['label']} [{ch_meta['badge']}]")
        print("-" * 78)
        print(chosen["channels"].get(cid, ""))
    print("\n" + "=" * 78)


def cmd_verify():
    from PIL import Image

    print("🔍 [pr v3.0] 교육자 헌정 홍보 데이터베이스·아틀리에 도판 카드·GEO·JS 무결성 검증 시작...")
    payload = run_autonomous_pr_cycle()
    assert PR_ENGINE_JSON.exists() and 1000 < PR_ENGINE_JSON.stat().st_size < 12 * 1024 * 1024, (
        f"pr_growth_engine.json 크기 범위 이상: {PR_ENGINE_JSON.stat().st_size if PR_ENGINE_JSON.exists() else 0}"
    )

    camps = payload.get("campaigns", [])
    assert len(camps) >= 600, f"캠페인 수 부족: {len(camps)}"
    req_channels = {m["id"] for m in CHANNEL_METADATA}
    for c in camps[:25]:
        assert req_channels.issubset(set((c.get("channels") or {}).keys())), f"누락 채널: {c.get('slug')}"
        all_txt = "\n".join(c["channels"].values())
        for bad in FORBIDDEN_HYPE_PHRASES:
            assert bad not in all_txt, f"품격 저해 과장 문구 감지({c.get('slug')}): {bad}"
        assert "민은기 선생님" in c["channels"]["educator_tribute"], f"교육자 헌정 누락: {c.get('slug')}"

    req_cards = ["pr_card_min7014_master.png"] + [f"pr_card_{t['slug']}.png" for t in FLAGSHIP_YT_TOPICS] + list(LEGACY_CARD_ALIASES.values())
    for cname in req_cards:
        cp = PR_CARDS_DIR / cname
        assert cp.exists(), f"PR 카드 누락: {cname}"
        with Image.open(cp) as im:
            assert im.size == (1200, 630), f"PR 카드 해상도 불일치({cname}): {im.size}"

    assert LLMS_TXT.exists() and "MIN EUN GI" in LLMS_TXT.read_text(encoding="utf-8"), "llms.txt 교육자 프로필 누락"
    print(f"✅ pr_growth_engine.json 검증 완료 ({PR_ENGINE_JSON.stat().st_size:,} bytes, {payload['stats']['total_ready_posts']}개 홍보 포스트)")
    print(f"✅ 1200x630 아틀리에 PR 카드 {len(req_cards)}종 무결성 검증 완료")

    for js_file in ("mathedu-room.js", "mathedu-quest-game.js"):
        r = subprocess.run(["node", "--check", js_file], cwd=ROOT_DIR)
        if r.returncode != 0:
            sys.exit(r.returncode)
        print(f"✅ {js_file} 문법 검증 통과!")


if __name__ == "__main__":
    cmd = sys.argv[1].lower() if len(sys.argv) > 1 else "status"
    arg2 = sys.argv[2] if len(sys.argv) > 2 else "2017090101"
    if cmd == "kit":
        cmd_kit(arg2)
    elif cmd in ("generate", "sync", "seo"):
        run_autonomous_pr_cycle()
    elif cmd == "verify":
        cmd_verify()
    else:
        cmd_status()
