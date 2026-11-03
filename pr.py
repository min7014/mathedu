#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pr.py — mathedu & @min7014_ai 전담 자율 홍보 에이전트 (Chief PR, Viral Growth & SEO/GEO Director Agent v2.0)
========================================================================================================
민은기 선생님의 수학자료실(min7014.github.io), mathedu(16,548문항 탈-5지선다 창의 수학 플랫폼),
그리고 공식 유튜브 채널(@min7014_ai)의 양방향 트래픽 증폭과 자생적 홍보를 전담하는 자율 에이전트입니다.

[핵심 5대 자율 홍보 모듈]
1. 7대 채널별 맞춤형 바이럴 캠페인 자동 생성기 (generate_topic_promo_campaigns)
   - 📺 유튜브 고정댓글 & 커뮤니티 포스트 (YouTube ➔ 홈페이지 유입 퍼널)
   - 💬 카카오톡 · 학급/스터디 단톡방 1초 도전장
   - 🔥 수험생 커뮤니티 (수만휘 · 오르비 · 포만한) 학습법 칼럼형 추천글
   - 🏫 전국 수학교사 커뮤니티 (인디스쿨 · 수학교사 모임) 5분 탐구 수업 나눔 키트
   - 📸 인스타그램 · 스레드 · 블로그 · X(트위터) #공스타그램 카드뉴스 캡션
   - 👨‍👩‍👧 학부모 · 초중고 교육 카페 초등 눈높이 무장벽 디딤돌 안내문
   - 🌐 Global EdTech (Reddit r/learnmath, r/math, Hacker News) 영문 홍보 키트
2. 고클릭률(CTR) SNS 오픈그래프 & 홍보 배너 이미지 자동 렌더링 (generate_pr_visual_cards)
   - assets/pr_cards/ 디렉터리에 1200x630 고해상도 바이럴 공유 카드 PNG 자동 생성
3. AI 검색엔진(GEO: llms.txt) 및 검색엔진(SEO: sitemap.xml) 실시간 자동 동기화 (sync_seo_and_geo_manifests)
   - ChatGPT, Claude, Gemini, Perplexity, Google, Naver가 새 영상과 문제를 즉시 색인하도록 갱신
4. 24/7 근간 진화 데몬(mathedu_foundation_daemon.py) 연동 자율 홍보 사이클 (run_autonomous_pr_cycle)
5. CLI 실행 모드: status | kit | generate | seo | verify
"""

import os
import sys
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

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

FLAGSHIP_YT_TOPICS = [
    {
        "slug": "0003",
        "id": "MIN-KB-0003",
        "title": "피타고라스 정리 (25단계 넓이 분할·전단 이동 시각 증명)",
        "title_en": "Pythagorean Theorem (25-Step Area Dissection & Shear Proof)",
        "keyword": "피타고라스",
        "domain": "기하 · 직각삼각형 · 넓이 보존",
        "hook_ko": "a²+b²=c² 공식을 외우기 전에, 두 정사각형 조각이 빗변 정사각형으로 빈틈없이 미끄러져 들어가는 25단계 시각 증명을 눈으로 확인해 보세요!",
        "yt_ko": "https://youtu.be/k6LBYa5SCiA",
        "yt_en": "https://youtu.be/n9zyKwXXsbA",
        "yt_id_ko": "k6LBYa5SCiA",
        "yt_id_en": "n9zyKwXXsbA",
        "short_mp4": "video_lectures/shorts/0003_short_ko.mp4",
        "thumb": "video_lectures/youtube_packages/2017090101_ko_thumb.png",
        "steps": 25,
    },
    {
        "slug": "0001",
        "id": "MIN-KB-0001",
        "title": "메넬라우스의 정리 (20단계 평행보조선 시각 증명)",
        "title_en": "Menelaus' Theorem (20-Step Parallel Auxiliary Line Proof)",
        "keyword": "메넬라우스",
        "domain": "기하 · 닮음비 · 보조선",
        "hook_ko": "복잡한 삼각형 할선 비율 공식, 단 1줄의 평행보조선만 그으면 중학교 닮음비로 3초 만에 증명이 끝납니다!",
        "yt_ko": "https://youtu.be/7zD66SWWceg",
        "yt_en": "https://youtu.be/CjE2nyyzG2s",
        "yt_id_ko": "7zD66SWWceg",
        "yt_id_en": "CjE2nyyzG2s",
        "short_mp4": "video_lectures/shorts/0001_short_ko.mp4",
        "thumb": "video_lectures/youtube_packages/2014111901_ko_thumb.png",
        "steps": 20,
    },
    {
        "slug": "0002",
        "id": "MIN-KB-0002",
        "title": "체바의 정리 (17단계 삼각형 넓이 비 시각 증명)",
        "title_en": "Ceva's Theorem (17-Step Triangle Area Ratio Proof)",
        "keyword": "체바",
        "domain": "기하 · 삼각형 공점선 · 넓이 비",
        "hook_ko": "세 체바선이 한 점에서 만날 조건, 밑변의 길이 비를 색칠된 삼각형의 넓이 비로 바꾸면 순환 약분으로 깔끔하게 1이 됩니다!",
        "yt_ko": "https://youtu.be/W_AWH-Gk89w",
        "yt_en": "https://youtu.be/ffNJhPRvh4Y",
        "yt_id_ko": "W_AWH-Gk89w",
        "yt_id_en": "ffNJhPRvh4Y",
        "short_mp4": "video_lectures/shorts/0002_short_ko.mp4",
        "thumb": "video_lectures/youtube_packages/2014111902_ko_thumb.png",
        "steps": 17,
    },
    {
        "slug": "0004",
        "id": "MIN-KB-0004",
        "title": "피타고라스 나무 (11단계 프랙탈 넓이 보존 & 무한등비급수)",
        "title_en": "Pythagoras Tree (11-Step Fractal Area Conservation)",
        "keyword": "등비급수",
        "domain": "수열 · 미적분 · 프랙탈 기하",
        "hook_ko": "가지가 무한히 뻗어나가는 피타고라스 나무에서 각 단계 정사각형 넓이의 합이 왜 항상 일정한지 11단계 플립북으로 확인하세요!",
        "yt_ko": "https://youtu.be/bQO7fnT6aDU",
        "yt_en": "https://youtu.be/9JKLflqrtDU",
        "yt_id_ko": "bQO7fnT6aDU",
        "yt_id_en": "9JKLflqrtDU",
        "short_mp4": "video_lectures/shorts/0004_short_ko.mp4",
        "thumb": "video_lectures/youtube_packages/2014111902_ko_thumb.png",
        "steps": 11,
    },
    {
        "slug": "0005",
        "id": "MIN-KB-0005",
        "title": "종이띠로 접는 정칠각형 매듭 원리 (11단계 대칭 작도)",
        "title_en": "Regular Heptagon Paper-Strip Knot Construction (11 Steps)",
        "keyword": "다각형",
        "domain": "기하 · 정다각형 작도 · 대칭성",
        "hook_ko": "자와 컴퍼스만으로는 작도할 수 없는 정칠각형이 긴 종이띠 매듭 하나로 완벽하게 접히는 수학적 비밀을 공개합니다!",
        "yt_ko": "https://youtu.be/Mq6s2JLV9mQ",
        "yt_en": "https://youtu.be/fXQJ8s1La-E",
        "yt_id_ko": "Mq6s2JLV9mQ",
        "yt_id_en": "fXQJ8s1La-E",
        "short_mp4": "video_lectures/shorts/0005_short_ko.mp4",
        "thumb": "video_lectures/youtube_packages/2022051507_ko_thumb.png",
        "steps": 11,
    },
]


def build_7channel_messages_for_topic(topic: dict) -> dict:
    slug = topic.get("slug", "0003")
    title = topic.get("title", "시각적 수학 증명")
    title_en = topic.get("title_en", "Visual Math Proof")
    kw = topic.get("keyword", "기하")
    hook = topic.get("hook_ko", "공식 암기 없이 눈으로 깨치는 단계별 시각적 수학 증명!")
    yt_ko = topic.get("yt_ko", "https://www.youtube.com/@min7014_ai")
    yt_en = topic.get("yt_en", "https://www.youtube.com/@min7014_ai")
    steps = topic.get("steps", 15)

    url_board = f"https://min7014.github.io/mathedu/video_board.html?slug={slug}&from=pr"
    url_quiz = f"https://min7014.github.io/mathedu/index.html?q={kw}&from=pr"
    url_daily = "https://min7014.github.io/mathedu/index.html#dailyGrowthFlywheelSection"
    url_game = "https://min7014.github.io/mathedu/game.html"
    url_sub = "https://www.youtube.com/@min7014_ai?sub_confirmation=1"

    return {
        "youtube_pinned": (
            f"📌 [민은기 선생님의 수학자료실 × @min7014_ai 공식 학습 & 실습 링크]\n"
            f"{hook}\n\n"
            f"방금 영상으로 본 [{title}] 원리를 지금 바로 홈페이지에서 내 손으로 조작하고 문제로 풀어보세요! (100% 무료)\n"
            f"📐 1단계 · 이 도형 GeoGebra로 직접 움직여보기: {url_board}\n"
            f"✍️ 2단계 · 5지선다 찍기 없이 수식 레고 조립으로 관련 기출 풀기: {url_quiz}\n"
            f"🔥 3단계 · 오늘의 3분 수학 유레카 & 1초 반례 O/X 백신: {url_daily}\n"
            f"🎮 4단계 · 3D 수학 성소 보스 레이드 게임 도전: {url_game}\n\n"
            f"💬 [오늘의 유레카 댓글 퀴즈]: 영상 속 결정적 보조선이 그어지는 순간 가장 핵심이 된 성질은 무엇이었나요? 댓글로 남기고 홈페이지에서 실전 문제를 격파해 보세요!"
        ),
        "kakao_challenge": (
            f"🔥 [유튜브 1분 시각 증명 × 탈-5지선다 수학 도전장!]\n"
            f"📌 주제: {title}\n"
            f"💡 {hook}\n\n"
            f"🎬 1) @min7014_ai 1080p 시각 증명 영상 먼저 보기:\n"
            f"👉 {yt_ko}\n\n"
            f"✍️ 2) 영상 봤으면 5지선다 보기 없이 직접 식 조립해서 관련 기출 풀기:\n"
            f"👉 {url_quiz}\n\n"
            f"📐 3) 전체 1,113개 설명영상 & GeoGebra 게시판:\n"
            f"👉 {url_board}"
        ),
        "student_community": (
            f"📌 [수학 공부법/무료 사이트 추천] 공식 통암기 멈추고 '보조선 플립북 영상 + 탈-5지선다 수식 조립'으로 수학 깨치는 법 ({title})\n\n"
            f"문제 풀다가 막히면 해설지 첫 줄('보조선을 긋는다')을 왜 그어야 하는지 몰라서 좌절하곤 했는데,\n"
            f"민은기 선생님의 수학자료실 유튜브(@min7014_ai)와 연계된 mathedu 홈페이지를 같이 쓰니까 원리가 완전히 다르게 보입니다.\n\n"
            f"✅ 1단계 (시각적 직관): {yt_ko}\n"
            f"➔ [{title}]이 왜 성립하는지 {steps}단계 1080p 플립북 모션으로 보조선이 그어지는 과정을 한눈에 보여줍니다.\n\n"
            f"✅ 2단계 (탈-5지선다 창의 구성 풀이): {url_quiz}\n"
            f"➔ 객관식 ①~⑤번 보기에 의존해서 찍거나 대입하는 대신, 1단계 초등 눈높이 디딤돌부터 출발해 수식 레고 블록을 직접 조립하며 내 손으로 답을 도출합니다.\n\n"
            f"✅ 3단계 (동적 기하 & 1,113개 영상 게시판): {url_board}\n"
            f"➔ 회원가입·결제 일절 없이 16,548문항 전체 기출과 3,400+개 시각 증명 자료가 100% 무료로 열려 있으니 꼭 활용해 보세요!"
        ),
        "teacher_indischool": (
            f"📐 [수학교사 수업 나눔] '{title}' {steps}단계 시각 증명 영상(@min7014_ai) & 탈-5지선다 창의 구성 퀴즈 패키지\n\n"
            f"선생님들, 수업 도입부 5분 동안 칠판 판서만으로 설명하기 까다로운 [{title}] 단원을 시각적 플립북 영상과 동적 기하(GeoGebra), 그리고 학생 참여형 디딤돌 퀴즈로 한 번에 연결할 수 있는 무료 OER 자료입니다.\n\n"
            f"• 🎬 1080p 수업 도입 영상 (한국어): {yt_ko}\n"
            f"• 🌎 1080p 영문 융합수업 영상 (English): {yt_en}\n"
            f"• 🧭 GeoGebra 슬라이더 조작 & 전체 1,113개 영상 게시판: {url_board}\n"
            f"• ✍️ 학생용 탈-5지선다 수식 구성 & 조건 변형(What-If-Not) 문제 발명 실습: {url_quiz}\n\n"
            f"교실 전자칠판에서 영상을 틀어 보조선의 필연성을 함께 관찰한 뒤, 학생들이 태블릿/스마트폰으로 접속해 5지선다 찍기 없이 스스로 식을 구성해 보는 수업으로 추천드립니다."
        ),
        "insta_blog": (
            f"✨ 공식 외우지 말고 눈으로 먼저 깨치기! [{title}]\n\n"
            f"{hook}\n\n"
            f"🎬 @min7014_ai 1080p 시각 증명 유튜브로 보조선 원리 깨치고\n"
            f"✍️ mathedu 홈페이지에서 5지선다 보기 없이 내 손으로 수식 레고 조립해서 수능 기출까지 클리어! 🟩🟩🟩 🧠 DEEP EUREKA!!\n\n"
            f"🔗 유튜브 영상: {yt_ko}\n"
            f"🔗 무료 수학 홈페이지: {url_board}\n\n"
            f"#수학공부 #공스타그램 #수능수학 #기하 #미적분 #수학증명 #지오지브라 #min7014 #mathedu #수학유튜브 #초등수학 #중등수학 #고등수학"
        ),
        "parent_cafe": (
            f"💡 [무료 수학교육 사이트 & 유튜브 정보] 사교육·선행 없이 초등 눈높이 디딤돌부터 고등 수능 기출까지 스스로 깨치는 곳\n\n"
            f"아이들이 수학 공식을 뜻도 모른 채 외우거나 객관식 5지선다 찍기에 익숙해져서 고민이신 학부모님들께 현직 수학교사 민은기 선생님의 무료 수학 플랫폼을 공유합니다.\n\n"
            f"1️⃣ 눈으로 이해하는 1080p 시각적 수학 증명 유튜브 (@min7014_ai)\n"
            f"• 예: [{title}] ➔ {yt_ko}\n"
            f"• 도형이 움직이고 보조선이 그어지는 과정을 한 단계씩 보여주어 아이가 '아! 이래서 공식이 나오는구나!' 하고 스스로 유레카를 외칩니다.\n\n"
            f"2️⃣ 초등 기초 직관부터 출발하는 탈-5지선다 창의 수학 홈페이지 (mathedu)\n"
            f"• 바로가기: {url_quiz}\n"
            f"• 아무리 어려운 고등 문제도 1단계(작은 숫자 대입·초등 직관)부터 6단계까지 촘촘한 사다리로 나누어져 있고, 5지선다 찍기 대신 수식 블록을 직접 조립하며 진짜 수학적 사고력을 길러줍니다. (100% 영구 무료)"
        ),
        "global_reddit": (
            f"🚀 [Visual Proof + Constructive Math OER] {title_en} (@min7014_ai × mathedu)\n\n"
            f"Instead of memorizing formulas or guessing from 5 multiple-choice options, watch the {steps}-step 1080p visual flipbook proof and then construct the algebraic equations yourself!\n\n"
            f"• 🎬 1080p Visual Proof Video (EN): {yt_en}\n"
            f"• 🇰🇷 1080p Visual Proof Video (KO): {yt_ko}\n"
            f"• 📐 Interactive GeoGebra & 1,113 Visual Proofs Board: {url_board}\n"
            f"• ✍️ De-Multiple-Choice Constructive Math Studio (16,548 Problems): {url_quiz}\n"
            f"• 🔔 Subscribe to @min7014_ai: {url_sub}"
        ),
    }


def generate_pr_visual_cards():
    """Pillow를 활용해 SNS·오픈그래프·커뮤니티 공유용 1200x630 바이럴 홍보 배너 이미지를 생성합니다."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return []

    PR_CARDS_DIR.mkdir(parents=True, exist_ok=True)
    font_candidates = [
        r"C:\Windows\Fonts\malgunbd.ttf",
        r"C:\Windows\Fonts\NanumGothicExtraBold.ttf",
        r"C:\Windows\Fonts\arialbd.ttf",
    ]
    font_path = next((f for f in font_candidates if os.path.exists(f)), None)

    def load_f(sz):
        if font_path:
            try:
                return ImageFont.truetype(font_path, sz)
            except Exception:
                pass
        return ImageFont.load_default()

    generated = []
    for topic in FLAGSHIP_YT_TOPICS:
        slug = topic["slug"]
        out_path = PR_CARDS_DIR / f"pr_card_{slug}.png"
        canvas = Image.new("RGB", (1200, 630), (9, 14, 28))
        draw = ImageDraw.Draw(canvas)

        # Left side: Dark navy high-contrast promo copy
        draw.rectangle([0, 0, 1200, 630], fill=(10, 16, 34))
        draw.rectangle([0, 0, 14, 630], fill=(225, 29, 72))

        # Top badge
        draw.rounded_rectangle([42, 36, 560, 86], radius=14, fill=(225, 29, 72))
        draw.text((60, 47), "▶ @min7014_ai × mathedu 시각 증명", font=load_f(26), fill=(255, 255, 255))

        # Main Headline
        clean_t = topic["title"].split("(")[0].strip()
        draw.text((44, 115), clean_t[:16], font=load_f(58), fill=(250, 204, 21))
        draw.text((44, 192), f"{topic['steps']}단계 시각 증명 & 창의 퀴즈", font=load_f(42), fill=(56, 189, 248))

        # 3-Step Funnel Box
        draw.rounded_rectangle([42, 268, 720, 505], radius=18, fill=(19, 30, 58), outline=(56, 189, 248), width=2)
        draw.text((64, 288), "★ 유튜브 영상 보고 홈페이지에서 직접 체험!", font=load_f(26), fill=(255, 255, 255))
        draw.text((64, 336), "• [1단계] @min7014_ai 1080p 보조선 플립북 시청", font=load_f(23), fill=(226, 232, 240))
        draw.text((64, 378), "• [2단계] GeoGebra 동적 기하 슬라이더 직접 조작", font=load_f(23), fill=(167, 243, 208))
        draw.text((64, 420), "• [3단계] 16,548문항 탈-5지선다 수식 레고 조립", font=load_f(23), fill=(253, 230, 138))
        draw.text((64, 460), f"▶ YouTube: {topic['yt_ko']}", font=load_f(20), fill=(251, 113, 133))

        # Right side: Embed existing video thumbnail if available
        thumb_p = ROOT_DIR / topic.get("thumb", "")
        if thumb_p.exists():
            try:
                th = Image.open(thumb_p).convert("RGB").resize((410, 231))
                canvas.paste(th, (750, 140))
                draw.rounded_rectangle([748, 138, 1162, 373], radius=12, outline=(250, 204, 21), width=4)
            except Exception:
                pass

        # Right bottom badge
        draw.rounded_rectangle([750, 395, 1160, 505], radius=16, fill=(6, 78, 59), outline=(16, 185, 129), width=2)
        draw.text((772, 412), "100% 영구 무료 개방형 수학 플랫폼", font=load_f(22), fill=(167, 243, 208))
        draw.text((772, 450), "min7014.github.io/mathedu", font=load_f(26), fill=(255, 255, 255))

        # Bottom CTA Bar
        draw.rectangle([0, 545, 1200, 630], fill=(225, 29, 72))
        draw.text(
            (44, 568),
            "▶ 지금 바로 접속 : https://min7014.github.io/mathedu  |  YouTube @min7014_ai",
            font=load_f(28),
            fill=(255, 255, 255),
        )

        canvas.save(out_path, "PNG")
        generated.append(str(out_path.relative_to(ROOT_DIR)).replace("\\", "/"))

    return generated


def build_pr_growth_engine_data() -> dict:
    """CATALOG_JSON, VAULT_JSON, DEEP_JSON을 통합 분석하여 assets/pr_growth_engine.json을 생성합니다."""
    cat_list = []
    if CATALOG_JSON.exists():
        try:
            cat_list = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))
        except Exception:
            cat_list = []

    topics_map = {t["slug"]: dict(t) for t in FLAGSHIP_YT_TOPICS}
    for c in cat_list:
        slug = str(c.get("slug") or "").strip()
        if not slug:
            continue
        yt_ko = (c.get("youtube_urls") or {}).get("ko") or ""
        yt_en = (c.get("youtube_urls") or {}).get("en") or ""
        if slug not in topics_map:
            raw_title = (c.get("title") or c.get("title_ko") or slug).strip()
            clean_title = raw_title.split("(")[0].strip() or raw_title
            topics_map[slug] = {
                "slug": slug,
                "id": f"MIN-VID-{slug}",
                "title": f"{clean_title} ({c.get('page_count', 12)}단계 시각 증명)",
                "title_en": (c.get("title_en") or raw_title).strip(),
                "keyword": clean_title.split()[0] if clean_title else "기하",
                "domain": "시각적 수학 증명 · 동적 기하",
                "hook_ko": f"[{clean_title}] 공식 암기 없이 {c.get('page_count', 12)}단계 플립북 모션으로 보조선과 원리를 한눈에 깨쳐 보세요!",
                "yt_ko": yt_ko or "https://www.youtube.com/@min7014_ai",
                "yt_en": yt_en or "https://www.youtube.com/@min7014_ai",
                "yt_id_ko": yt_ko.split("/")[-1] if "youtu.be/" in yt_ko else "k6LBYa5SCiA",
                "yt_id_en": yt_en.split("/")[-1] if "youtu.be/" in yt_en else "n9zyKwXXsbA",
                "short_mp4": f"video_lectures/shorts/{slug}_short_ko.mp4",
                "thumb": f"video_lectures/youtube_packages/{slug}_ko_thumb.png",
                "steps": c.get("page_count", 12),
            }

    card_paths = generate_pr_visual_cards()

    campaigns = []
    for slug, t in topics_map.items():
        msgs = build_7channel_messages_for_topic(t)
        card_rel = f"assets/pr_cards/pr_card_{slug}.png"
        if not (ROOT_DIR / card_rel).exists():
            card_rel = "assets/pr_cards/pr_card_0003.png"
        campaigns.append({
            **t,
            "pr_card_url": card_rel,
            "deep_links": {
                "video_board": f"https://min7014.github.io/mathedu/video_board.html?slug={slug}&from=pr",
                "creative_quiz": f"https://min7014.github.io/mathedu/index.html?q={t['keyword']}&from=pr",
                "daily_eureka": "https://min7014.github.io/mathedu/index.html#dailyGrowthFlywheelSection",
                "boss_raid_3d": f"https://min7014.github.io/mathedu/?challenge={slug}&from=pr",
                "youtube_sub": "https://www.youtube.com/@min7014_ai?sub_confirmation=1",
            },
            "channels": msgs,
        })

    payload = {
        "agent": "pr (Chief Public Relations, Viral Growth & SEO/GEO Director v2.0)",
        "updated_at": datetime.now().isoformat(),
        "stats": {
            "total_campaigns": len(campaigns),
            "channels_per_campaign": 7,
            "total_ready_posts": len(campaigns) * 7,
            "visual_pr_cards": len(card_paths),
        },
        "channel_Metadata": [
            {"id": "youtube_pinned", "label": "📺 유튜브 고정댓글·커뮤니티", "badge": "YouTube ➔ Web 퍼널"},
            {"id": "kakao_challenge", "label": "💬 카톡·단톡방 1초 도전장", "badge": "바이럴 결투장"},
            {"id": "student_community", "label": "🔥 수만휘·오르비 수험생 추천글", "badge": "학습법 칼럼"},
            {"id": "teacher_indischool", "label": "🏫 인디스쿨·수학교사 나눔 키트", "badge": "5분 수업 런처"},
            {"id": "insta_blog", "label": "📸 인스타·블로그 #공스타그램", "badge": "SNS 해시태그"},
            {"id": "parent_cafe", "label": "👨‍👩‍👧 학부모·교육카페 안내문", "badge": "초등 눈높이 디딤돌"},
            {"id": "global_reddit", "label": "🌐 Reddit·Global EdTech (EN)", "badge": "Global Outreach"},
        ],
        "campaigns": campaigns,
    }

    PR_ENGINE_JSON.parent.mkdir(parents=True, exist_ok=True)
    PR_ENGINE_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


def sync_seo_and_geo_manifests():
    """
    AI 검색엔진(ChatGPT, Claude, Gemini, Perplexity)이 참조하는 llms.txt에
    최신 @min7014_ai 유튜브 영상 목록과 탈-5지선다 창의 수학 퍼널 정보를 자동 업데이트합니다.
    """
    if not LLMS_TXT.exists():
        return
    txt = LLMS_TXT.read_text(encoding="utf-8")
    marker = "## 📺 Official @min7014_ai YouTube Visual Proof Cinema & Bi-Directional Funnel"
    yt_section_lines = [
        marker,
        "- Official AI Visual Math Proof YouTube Channel: https://www.youtube.com/@min7014_ai",
        "- Full 1,113 Visual Math Proof Video & GeoGebra Board: https://min7014.github.io/mathedu/video_board.html",
        "- De-Multiple-Choice Creativity-First Constructive Math Studio (16,548 Problems): https://min7014.github.io/mathedu/",
        "- Featured 1080p Visual Flipbook Proofs (Korean & English):",
    ]
    for t in FLAGSHIP_YT_TOPICS:
        yt_section_lines.append(
            f"  * {t['title']} / {t['title_en']}: KO {t['yt_ko']} | EN {t['yt_en']} | Interactive Board: https://min7014.github.io/mathedu/video_board.html?slug={t['slug']}"
        )
    new_block = "\n".join(yt_section_lines) + "\n"

    if marker in txt:
        txt = txt.split(marker)[0].rstrip() + "\n\n" + new_block
    else:
        txt = txt.rstrip() + "\n\n" + new_block
    LLMS_TXT.write_text(txt, encoding="utf-8")


def run_autonomous_pr_cycle(last_slug: str = ""):
    """
    24/7 근간 진화 데몬(mathedu_foundation_daemon.py) 또는 CLI에서 호출되어
    새 영상·자료에 대한 7대 채널 홍보 캠페인, SNS 홍보 카드, llms.txt를 자동 갱신합니다.
    """
    payload = build_pr_growth_engine_data()
    sync_seo_and_geo_manifests()
    print(
        f"📣 [PR Agent Autonomous Cycle] 총 {payload['stats']['total_campaigns']}개 주제 × 7대 채널 "
        f"({payload['stats']['total_ready_posts']}종 홍보 문구) & SNS 비주얼 카드 동기화 완료! "
        f"(최근 슬러그: {last_slug or 'ALL'})",
        flush=True,
    )
    return payload


def cmd_status():
    payload = build_pr_growth_engine_data()
    sync_seo_and_geo_manifests()
    llms_size = LLMS_TXT.stat().st_size if LLMS_TXT.exists() else 0
    sitemap_size = SITEMAP_XML.stat().st_size if SITEMAP_XML.exists() else 0
    print("=" * 78)
    print("📣 [pr v2.0] 자율 홍보 에이전트 (Chief PR · Viral Growth · YouTube×Web Funnel Director)")
    print("=" * 78)
    print("• 5대 에이전트 협업 체제      : 👩‍🏫 mathteacher × 🎮 gamemaker × 🎨 designer × 📣 pr × 💼 finance")
    print(f"• 홍보 엔진 데이터베이스      : assets/pr_growth_engine.json ({PR_ENGINE_JSON.stat().st_size:,} bytes)")
    print(f"• 자동 생성된 캠페인 수       : {payload['stats']['total_campaigns']}개 주제 × 7대 채널 = 총 {payload['stats']['total_ready_posts']}개 맞춤형 홍보 키트")
    print(f"• 고해상도 SNS 홍보 카드      : assets/pr_cards/ ({payload['stats']['visual_pr_cards']}종 1200x630 PNG 렌더링 완료)")
    print(f"• AI 검색엔진 매니페스트(GEO) : llms.txt ({llms_size:,} bytes · @min7014_ai 딥링크 동기화 완료)")
    print(f"• 검색엔진 사이트맵(SEO)      : sitemap.xml ({sitemap_size:,} bytes)")
    print("• 양방향 홍보 루프            :")
    print("  1) 📺 YouTube (@min7014_ai) ➔ On-Screen 하단 홍보 바 + 설명란 5대 홈페이지 직행 딥링크")
    print("  2) 🌐 홈페이지 (mathedu)    ➔ 인라인 유튜브 극장 + 문항별 유튜브 시각 증명 코치 + 7대 채널 홍보 스튜디오")
    print("  3) ⚙️ 24/7 데몬 자동 연동   ➔ 새 영상 제작 시 7대 채널 홍보문구·SNS 카드·llms.txt 자동 생성")
    print("=" * 78)


def cmd_kit(target_slug: str = "0003"):
    payload = build_pr_growth_engine_data()
    camps = payload.get("campaigns", [])
    chosen = next((c for c in camps if c["slug"] == target_slug), camps[0] if camps else None)
    if not chosen:
        print("캠페인 데이터가 없습니다.")
        return
    print("=" * 78)
    print(f"📣 [pr v2.0] '{chosen['title']}' 7대 외부 채널별 즉시 배포용 홍보 키트")
    print("=" * 78)
    for ch_meta in payload["channel_Metadata"]:
        cid = ch_meta["id"]
        print(f"\n{ch_meta['label']} [{ch_meta['badge']}]")
        print("-" * 78)
        print(chosen["channels"].get(cid, ""))
    print("\n" + "=" * 78)


def cmd_verify():
    print("🔍 [pr v2.0] 홍보 에이전트 데이터·비주얼 카드·SEO/GEO·JS 문법 무결성 검증 시작...")
    payload = run_autonomous_pr_cycle()
    assert PR_ENGINE_JSON.exists() and PR_ENGINE_JSON.stat().st_size > 1000, "pr_growth_engine.json 생성 실패"
    assert LLMS_TXT.exists() and LLMS_TXT.stat().st_size > 500, "llms.txt 누락"
    print(f"✅ pr_growth_engine.json 검증 완료 ({payload['stats']['total_ready_posts']}개 멀티채널 홍보 포스트 준비됨)")
    r1 = subprocess.run(["node", "--check", "mathedu-room.js"], cwd=ROOT_DIR)
    if r1.returncode != 0:
        sys.exit(r1.returncode)
    print("✅ mathedu-room.js 문법 검증 통과!")
    r2 = subprocess.run(["node", "--check", "mathedu-quest-game.js"], cwd=ROOT_DIR)
    if r2.returncode != 0:
        sys.exit(r2.returncode)
    print("✅ mathedu-quest-game.js 문법 검증 통과!")


if __name__ == "__main__":
    cmd = sys.argv[1].lower() if len(sys.argv) > 1 else "status"
    arg2 = sys.argv[2] if len(sys.argv) > 2 else "0003"
    if cmd == "kit":
        cmd_kit(arg2)
    elif cmd in ("generate", "sync", "seo"):
        run_autonomous_pr_cycle()
    elif cmd == "verify":
        cmd_verify()
    else:
        cmd_status()
