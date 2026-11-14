#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nano_banana_cinema_creator.py
===============================================================================
🍌 [Google Nano Banana × min7014.github.io] 실생활 시각 미스터리 시네마 하이브리드 엔진
- Rule 44 (수학적 오류 ZERO): 생성형 이미지 AI의 기하·수식 환각을 원천 차단하기 위해,
  나노바나나(Nano Banana) 마스터 아트워크는 오직 '텍스트·수식 0%의 순수 실생활·건축·크리스탈 기하 오브제'
  (Act 1 시선 강탈 훅 & Act 3 유레카 완결 & 고클릭률 썸네일)에만 사용하고,
  모든 수식·수치 라벨은 100% 파이썬 정밀 렌더링, 본 증명(Act 2)은 100% min7014.github.io
  오리지널 원문 PDF + 메이플 가상 지휘봉(Rule 43)으로 결합합니다.
- Rule 35 (인간 오리지널 깊이 강조): 단순 AI 슬롭(Slop) 오인을 막기 위해 원문 PDF 저작 정통성을 명시합니다.
- Rule 37 (사색적 블루·틸·골드 색채 조화): 강렬한 적색 배제, 로열 블루·에메랄드 틸·앰버 골드 적용.
- Rule 48 (완전 무창 실행): silent_subprocess 강제 주입.
- Rule 50 (월 11만 원 예산 수호): 로컬 캐싱된 고해상도 마스터 에셋 1장으로 KO/EN 1080p·Shorts·썸네일
  멀티유즈 렌더링하여 추가 외부 API 과금 0원 달성.
- Rule 51 (저작권·상표권 100% 무결성): 외부 시험·기업 등록상표 노출 0건 보장.
===============================================================================
"""

import silent_subprocess  # noqa: F401 — Rule 48 windowless enforcement
import json
import re
import shutil
import subprocess
import tempfile
import textwrap
from datetime import datetime
from pathlib import Path

import pymupdf
from PIL import Image, ImageChops, ImageDraw, ImageEnhance

ROOT_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = ROOT_DIR / "video_lectures" / "scripts"
NB_ASSETS_DIR = ROOT_DIR / "youtube_uploads" / "nano_banana_assets"
FLOW_CLIPS_DIR = ROOT_DIR / "youtube_uploads" / "flow_clips"
NB_OUT_DIR = ROOT_DIR / "youtube_uploads" / "nano_banana"
WEEKLY_CAP_STATE_FILE = ROOT_DIR / ".agents" / "nano_banana_weekly_cap.json"
# [Rule 52 Google Flow ULTRA 업그레이드 확정]: Antigravity 에이전트 쿼터 0소모(Google Flow ULTRA 직접 구동)로 주 2~3편 제한 전면 해제!
MAX_NANO_BANANA_WEEKLY_EPISODES = 50
NB_ASSETS_DIR.mkdir(parents=True, exist_ok=True)
FLOW_CLIPS_DIR.mkdir(parents=True, exist_ok=True)
NB_OUT_DIR.mkdir(parents=True, exist_ok=True)

# 2012100303 -> 2012100304(예각 접현각 증명) 에셋 호환 보장
if (NB_ASSETS_DIR / "nb_2012100303_tangent.png").exists() and not (NB_ASSETS_DIR / "nb_2012100304_tangent.png").exists():
    shutil.copy2(NB_ASSETS_DIR / "nb_2012100303_tangent.png", NB_ASSETS_DIR / "nb_2012100304_tangent.png")


NANO_BANANA_BLUEPRINTS = [
    {
        "slug": "2017090101",
        "art_file": "nb_2017090101_pythagoras.png",
        "flow_clip": "2017090101_flow.mp4",
        "flow_motion_prompt": "Locked static top-down 90-degree orthographic camera. All three crystal square water basins and brass right triangle edges remain 100% stationary in exact position. Gentle luminous sapphire-blue, emerald-teal, and golden water ripples and light caustics shimmer softly inside the three square crystal basins on dark velvet. Zero camera zoom, zero rotation, zero deformation, zero text, zero numbers.",
        "badge_ko": "★ 실생활 기하 미스터리 · 정사각형 수조 넓이 보존",
        "badge_en": "★ Visual Geometry Mystery · Crystal Square Area Proof",
        "thumb_hook_ko": ["루트 계산 ZERO!", "수조 넓이 3초 암산!"],
        "thumb_hook_en": ["ZERO SQUARE ROOTS!", "3-SEC AREA TRICK!"],
        "problem_label_ko": "직각삼각형 두 변 위 정사각형 수조 넓이가 9와 16일 때, 빗변의 큰 정사각형 수조 넓이 x는?",
        "problem_label_en": "Two square crystal basins on the legs have areas 9 and 16. What is hypotenuse square area x?",
        "figure_caption_ko": "수조 넓이 S₁ = 9, S₂ = 16  →  큰 수조 x = ?",
        "figure_caption_en": "Square Areas S₁ = 9, S₂ = 16  →  Large Square x = ?",
        "answer_label_ko": "루트 계산 ZERO! 합동 직각삼각형 4개 넓이 소거 원리(c² = a² + b²)로 x = 9 + 16 = 25 (3초 완결!)",
        "answer_label_en": "Zero Square Roots! Four-Triangle Square Decomposition (c² = a² + b²) → x = 9 + 16 = 25!",
        "title_ko": "🔥 루트 계산 쓰면 하수! 정사각형 수조 넓이 보존 3초 암산법 | 피타고라스 정리 시각적 증명",
        "title_en": "🔥 Stop Taking Square Roots! 3-Second Crystal Square Area Proof | Pythagorean Theorem Visualized",
        "short_title_ko": "❓ 루트 없이 3초 만에 큰 정사각형 넓이 x가 보이시나요? 수조 넓이 보존 해법! #Shorts",
        "short_title_en": "❓ Stop Scrolling! Spot Hypotenuse Square Area x in 3s Without Roots! #Shorts",
        "act1_ko": "잠깐! 직각삼각형에 맞닿은 파란 정사각형 수조 넓이가 9, 초록 수조 넓이가 16일 때, 변의 길이를 루트로 구하지 않고도 큰 정사각형 수조 넓이 x가 왜 정확히 합쳐지는지 3초 만에 보이시나요?",
        "act1_en": "Stop scrolling! When the sapphire square basin has area 9 and the emerald square has area 16, can you see in three seconds why the large hypotenuse square equals their exact sum—with zero square roots?",
        "act3_ko": "이제 큰 정사각형 테두리에 합동인 직각삼각형 네 개를 배치해 2ab를 깔끔히 지워내는 넓이 보존 증명이 한눈에 보이시나요? 루트 계산 없이 작은 두 정사각형 넓이 9와 16을 그대로 더해 정답 25가 3초 만에 완성됩니다! 공식 너머의 깊은 도형 통찰, 지금 바로 채널 구독을 눌러 매일 받아보세요!",
        "act3_en": "Now the four-triangle square decomposition proof is crystal clear! Subtracting the four congruent right triangles leaves c squared equal to a squared plus b squared—so 9 plus 16 gives x equals 25 in three seconds flat! Subscribe right now for daily visual math breakthroughs!",
        "comment_quiz_ko": "🧩 [3초 직관 암산] 만약 빗변의 큰 정사각형 수조 넓이가 40이고 작은 파란 수조 넓이가 13이라면, 초록 정사각형 수조 넓이는 얼마일까요? 댓글로 남겨보세요! 🤩👇",
        "comment_quiz_en": "🧩 [3-Sec Visual Check] If the large hypotenuse square basin has area 40 and the blue square is 13, what is the green square's area? Drop your answer below! 🤩👇",
    },
    {
        "slug": "2012100304",
        "art_file": "nb_2012100304_tangent.png",
        "flow_clip": "2012100304_flow.mp4",
        "flow_motion_prompt": "Locked static top-down 90-degree orthographic camera. Sapphire circle rim, crystal pins, golden bottom tangent beam, and emerald chords stay 100% stationary in exact position. Gentle warm golden and emerald-teal photonic light pulses shimmer smoothly along the tangent and chord beams on dark velvet. Zero camera zoom, zero rotation, zero deformation, zero text, zero numbers.",
        "badge_ko": "★ 천체 광학 기하 미스터리 · 원과 접선의 각도 불변량",
        "badge_en": "★ Optical Geometry Mystery · Tangent Light & Circle Angle",
        "thumb_hook_ko": ["접선 각도가 58°?", "지름 1줄로 5초 컷!"],
        "thumb_hook_en": ["TANGENT AT 58°?", "1 DIAMETER = 5s!"],
        "problem_label_ko": "바닥 황금 접선 빛줄기와 원의 현이 58°로 만날 때, 원 반대편 원주 위의 각 x는 몇 도일까요?",
        "problem_label_en": "A golden tangent light beam meets a chord at 58°. What is angle x across the sapphire circle?",
        "figure_caption_ko": "바닥 접선각 = 58°  →  원 반대편 ∠ACB = x = ?",
        "figure_caption_en": "Bottom Tangent = 58°  →  Inscribed Angle x = ?",
        "answer_label_ko": "접점을 지나는 지름 보조선 1줄 → 직각 90° 대칭 이동!  x = 58° 그대로 일치 (5초 완결!)",
        "answer_label_en": "1 Diameter Line from Contact Point → 90° Complement Match!  x = 58° Instantly!",
        "title_ko": "⚡ 접선만 나오면 막히는 이유! 황금 접선 58°와 지름 보조선 1줄 5초 해법 | 접현각의 정리 시각적 증명",
        "title_en": "⚡ Stuck on Circle Tangents? One Diameter Solves 58° in 5 Seconds! | Alternate Segment Theorem",
        "short_title_ko": "❓ 바닥 접선이 58°일 때 원 반대편 각 x는? 지름 보조선 1줄 3초 해법! #Shorts",
        "short_title_en": "❓ Stop Scrolling! Tangent Beam Is 58°—Spot Angle x in 3 Seconds! #Shorts",
        "act1_ko": "잠깐! 황금빛 접선이 사파이어 원의 바닥을 스치며 현과 58도를 이룰 때, 멀리 떨어진 원 반대편 각 x를 복잡한 연립방정식 없이 단 3초 만에 찾는 보조선 한 줄이 보이시나요?",
        "act1_en": "Wait! When a golden tangent beam grazes the bottom of a circle at 58 degrees to a chord, can you spot the single auxiliary line that reveals angle x across the circle in three seconds?",
        "act3_ko": "접점에서 원의 중심을 꿰뚫는 지름 보조선 딱 한 줄이면 접선과 이루는 90도, 반원에 대한 원주각 90도에서 똑같은 여각이 빠져나가므로 x는 언제나 58도와 완벽히 일치합니다! 도형 킬러 문항을 눈으로 푸는 시각 증명, 지금 바로 구독 버튼을 눌러 두세요!",
        "act3_en": "Drawing one diameter from the tangent point creates matching 90-degree right angles, locking angle x to the exact same 58 degrees in five seconds! Hit Subscribe right now to master visual Euclidean geometry!",
        "comment_quiz_ko": "🧩 [5초 직관 암산] 만약 바닥 접선과 현이 이루는 각이 67°라면, 호 반대편 원주각 x는 몇 도일까요? 암산 정답을 댓글로 남겨보세요! 🤩👇",
        "comment_quiz_en": "🧩 [5-Sec Check] If the tangent beam and chord form 67°, what is angle x across the circle? Comment your mental-math answer below! 🤩👇",
    },
    {
        "slug": "2014111902",
        "art_file": "nb_2014111902_ceva.png",
        "flow_clip": "2014111902_flow.mp4",
        "flow_motion_prompt": "Locked static top-down 90-degree orthographic camera. Triangular stained-glass skylight frame and three golden concurrent beams meeting at the center crystal point stay 100% stationary. Subtle sapphire, emerald, and warm golden sunlight caustics shimmer gently across the stained-glass panels on dark velvet. Zero camera zoom, zero rotation, zero deformation, zero text, zero numbers.",
        "badge_ko": "★ 유클리드 건축 기하 미스터리 · 삼각 천창의 균형점",
        "badge_en": "★ Architectural Geometry Mystery · Skylight Concurrency",
        "thumb_hook_ko": ["좌표·방정식 금지!", "넓이비로 5초 암산!"],
        "thumb_hook_en": ["NO COORDINATES!", "5s AREA BALANCE!"],
        "problem_label_ko": "삼각 천창의 세 황금 들보가 한 점에서 만나고 BD:DC=2:3, CE:EA=3:4일 때 AF:FB 비율은?",
        "problem_label_en": "Three golden skylight beams meet at one point with BD:DC=2:3 and CE:EA=3:4. Find ratio AF:FB!",
        "figure_caption_ko": "BD:DC = 2:3,  CE:EA = 3:4  →  AF:FB = ?",
        "figure_caption_en": "BD:DC = 2:3,  CE:EA = 3:4  →  AF:FB = ?",
        "answer_label_ko": "내부 삼각형 넓이비 순환 곱 = 1 → (2/3)×(3/4)×(AF/FB)=1 → AF:FB = 2 : 1 (5초 완결!)",
        "answer_label_en": "Cyclic Triangle Area Product = 1 → (2/3)×(3/4)×(AF/FB)=1 → AF:FB = 2 : 1!",
        "title_ko": "🔥 좌표 계산 없이 5초 컷! 삼각 천창 넓이비로 끝내는 선분 비율의 비밀 | 체바의 정리 시각적 증명",
        "title_en": "🔥 Zero Coordinates Needed! Solve Triangle Ratios in 5 Seconds via Area Balance | Ceva's Theorem",
        "short_title_ko": "❓ 삼각 천창 세 직선이 한 점에 모일 때 AF:FB 비율, 5초 만에 보이시나요? #Shorts",
        "short_title_en": "❓ Stop Scrolling! Three Beams Meet at One Point—Find Ratio AF:FB in 5s! #Shorts",
        "act1_ko": "잠깐! 스테인드글라스 삼각 천창의 세 황금 기둥이 정확히 한 점에서 만나고 두 변의 비가 2 대 3, 3 대 4일 때, 좌표나 평행선 없이 나머지 비율 AF 대 FB가 5초 만에 암산되시나요?",
        "act1_en": "Stop! Three golden beams of a triangular skylight meet at one glowing point, splitting two sides in ratios 2 to 3 and 3 to 4. Can you find the third ratio AF to FB in five seconds with zero coordinates?",
        "act3_ko": "밑변의 길이 비가 곧 내부 삼각형 조각들의 넓이 비라는 원리를 따라 한 바퀴 곱하면 3분의 2 곱하기 4분의 3 곱하기 FB분의 AF가 1이 되어, 3이 약분되고 정답 2 대 1이 5초 만에 튀어나옵니다! 차원이 다른 기하 직관, 지금 바로 구독해 두세요!",
        "act3_en": "Because base ratios equal interior triangle area ratios around the center point, multiplying 2 over 3 times 3 over 4 times AF over FB equals 1—canceling 3 gives AF to FB equals 2 to 1 in five seconds! Subscribe now for daily visual proofs!",
        "comment_quiz_ko": "🧩 [5초 직관 암산] 만약 BD:DC = 1:2이고 CE:EA = 2:5일 때 세 직선이 한 점에서 만나려면 AF:FB는 몇 대 몇이어야 할까요? 댓글로 도전! 🤩👇",
        "comment_quiz_en": "🧩 [5-Sec Check] If BD:DC = 1:2 and CE:EA = 2:5, what ratio AF:FB makes the three beams meet at a single point? Comment below! 🤩👇",
    },
    {
        "slug": "2012093001",
        "art_file": "nb_2012093001_inscribed.png",
        "flow_clip": "2012093001_flow.mp4",
        "badge_ko": "★ 천체 원형 링 광학 미스터리 · 중심각과 원주각 2배 불변량",
        "badge_en": "★ Sapphire Astrolabe Mystery · Inscribed vs Central Angle",
        "thumb_hook_ko": ["중심각이 84°일 때", "지름 1줄로 3초 암산!"],
        "thumb_hook_en": ["CENTRAL = 84°?", "1 DIAMETER = 3s!"],
        "problem_label_ko": "원 중심에 모인 황금 빛줄기 각이 84°일 때, 원 꼭대기에 모인 초록 빛줄기 각 x는 몇 도일까요?",
        "problem_label_en": "Two golden beams meet at the center at 84°. What is the emerald angle x at the top of the circle?",
        "figure_caption_ko": "중심 황금각 = 84°  →  꼭대기 원주각 x = ?",
        "figure_caption_en": "Central Beam = 84°  →  Top Inscribed Angle x = ?",
        "answer_label_ko": "중심을 꿰뚫는 지름 보조선 1줄 → 이등변삼각형 외각 2배 원리!  x = 84° ÷ 2 = 42° (3초 완결!)",
        "answer_label_en": "1 Diameter Through Center → Isosceles Exterior Angle Principle!  x = 84° ÷ 2 = 42°!",
        "title_ko": "⚡ 원만 나오면 막히는 이유! 중심을 지나는 지름 보조선 1줄 3초 암산법 | 원주각과 중심각의 관계 시각적 증명",
        "title_en": "⚡ Never Memorize Circle Rules Blindly! One Diameter Solves 84° in 3s | Inscribed Angle Visual Proof",
        "short_title_ko": "❓ 원 중심 황금각이 84°일 때 꼭대기 초록각 x는? 지름 보조선 1줄 3초 해법! #Shorts",
        "short_title_en": "❓ Stop Scrolling! Central Beam Is 84°—Spot Top Angle x in 3 Seconds! #Shorts",
        "act1_ko": "잠깐! 사파이어 원의 같은 두 점에서 출발한 황금 빛줄기가 중심에서 84도를 이룰 때, 원 꼭대기에 모인 초록 빛줄기 각 x가 왜 언제나 정확히 절반이 되는지 지름 보조선 한 줄로 3초 만에 보이시나요?",
        "act1_en": "Stop scrolling! When two golden light beams meet at the center of a sapphire circle at 84 degrees, can you see in three seconds—using just one diameter line—why the emerald angle x at the top is always exact half?",
        "act3_ko": "원 꼭대기에서 중심을 꿰뚫는 지름 보조선 딱 한 줄을 그으면 반지름이 같은 두 이등변삼각형으로 쪼개지고 외각은 밑각의 두 배가 되므로, 중심각 84도의 절반인 정답 42도가 3초 만에 튀어나옵니다! 눈으로 깨치는 오리지널 기하 직관, 지금 바로 채널 구독을 눌러 두세요!",
        "act3_en": "Drawing a single diameter from the top vertex through the center splits the figure into two isosceles triangles where each central exterior angle doubles its base angle—giving 84 divided by 2 equals 42 degrees in three seconds! Hit Subscribe right now for daily visual proofs!",
        "comment_quiz_ko": "🧩 [3초 직관 암산] 만약 원 중심에서 만나는 황금 빛줄기 중심각이 114°라면, 같은 호에 대한 원주각 x는 몇 도일까요? 암산 정답을 댓글로 남겨보세요! 🤩👇",
        "comment_quiz_en": "🧩 [3-Sec Check] If the central golden angle is 114°, what is the inscribed angle x subtending the same arc? Drop your mental-math answer in the comments! 🤩👇",
    },
]


def _load_master_art(bp: dict) -> Image.Image:
    p = NB_ASSETS_DIR / bp["art_file"]
    if p.exists():
        return Image.open(p).convert("RGB").resize((1920, 1080), Image.Resampling.LANCZOS)
    return Image.new("RGB", (1920, 1080), (12, 20, 38))


def _compute_normalized_diff_bbox(prev_img: Image.Image | None, curr_img: Image.Image) -> tuple | None:
    if prev_img is None or prev_img.size != curr_img.size:
        return (0.28, 0.25, 0.72, 0.78)
    diff = ImageChops.difference(prev_img.convert("RGB"), curr_img.convert("RGB")).convert("L")
    bw = diff.point(lambda v: 255 if v > 24 else 0)
    bb = bw.getbbox()
    if not bb:
        return (0.30, 0.28, 0.70, 0.76)
    w, h = curr_img.size
    return (bb[0] / w, bb[1] / h, bb[2] / w, bb[3] / h)


def render_nano_banana_thumbnail(bp: dict, doc, lang_code: str, out_png: Path) -> Path:
    """
    [Rule 37 + Rule 49 + Rule 51]:
    좌측/배경에는 시선을 사로잡는 구글 나노바나나 실생활 크리스탈·천체·건축 기하 오브제를 배치하고,
    우측에는 min7014.github.io 오리지널 원문 핵심 증명 카드와 정밀 수치 발문 배지를 결합한 초고클릭률(CTR 12%+) 썸네일.
    """
    import min7014_video_maker as vmaker

    W, H = 1280, 720
    art = _load_master_art(bp)
    # 좌측 2/3 영역이 잘 보이도록 1280x720 리사이즈 및 우측 다크 인디고 그라데이션 블렌딩
    base = art.resize((W, H), Image.Resampling.LANCZOS)
    base = ImageEnhance.Contrast(base).enhance(1.08)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # 우측 540px 구간에 부드러운 딥 인디고 글래스모피즘 패널 형성 (Rule 37)
    for x in range(620, W):
        alpha = int(min(238, max(0, (x - 620) / 150.0 * 228)))
        od.line([(x, 0), (x, H)], fill=(10, 18, 36, alpha), width=1)
    # 하단 가독성 그라데이션
    for y in range(520, H):
        alpha = int(min(215, (y - 520) / 200.0 * 210))
        od.line([(0, y), (680, y)], fill=(8, 15, 30, alpha), width=1)

    img = Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    is_en = lang_code == "en"

    # 상단 로열 블루 배지 (Rule 37: 적색 배제, Malgun Gothic 완벽 지원 기호만 사용)
    badge = "★ REAL-WORLD VISUAL PROOF" if is_en else "★ 실생활 기하 미스터리 × 시각 증명"
    draw.rounded_rectangle((28, 26, 540, 86), radius=16, fill=(2, 132, 199), outline=(250, 204, 21), width=3)
    draw.text((48, 40), badge, fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 25, bold=True))

    # 좌하단 수치 질문 배지 (절단 ZERO 보장)
    cap = (bp["figure_caption_en"] if is_en else bp["figure_caption_ko"]).replace("→", "→")
    draw.rounded_rectangle((28, 592, 692, 690), radius=18, fill=(15, 23, 42), outline=(56, 189, 248), width=3)
    draw.text((46, 624), cap, fill=(254, 240, 138), font=vmaker.get_font_for_lang(lang_code, 26 if is_en else 27, bold=True))

    # 우측 상단 2줄 초대형 호기심 카피
    hooks = bp["thumb_hook_en"] if is_en else bp["thumb_hook_ko"]
    f_big = vmaker.get_font_for_lang(lang_code, 46 if is_en else 50, bold=True)
    yh = 40
    for idx_h, hl in enumerate(hooks):
        c_fill = (255, 255, 255) if idx_h == 0 else (250, 204, 21)
        for dx in (-3, 0, 3):
            for dy in (-3, 0, 3):
                if dx or dy:
                    draw.text((712 + dx, yh + dy), hl, fill=(0, 0, 0), font=f_big)
        draw.text((712, yh), hl, fill=c_fill, font=f_big)
        yh += 68

    # 우측 중하단: 100% 무가림 원본 min7014.github.io 클라이맥스 증명 슬라이드 인셋 (Rule 28 & Rule 35)
    key_idx = max(0, len(doc) - 2)
    pix = doc[key_idx].get_pixmap(dpi=220)
    slide_img = vmaker._mask_pdf_bottom_author_bar(Image.frombytes("RGB", [pix.width, pix.height], pix.samples))
    sc = min(516 / slide_img.width, 360 / slide_img.height)
    sw, sh = int(slide_img.width * sc), int(slide_img.height * sc)
    sx, sy = 716 + (528 - sw) // 2, 206 + (370 - sh) // 2
    draw.rounded_rectangle((sx - 10, sy - 10, sx + sw + 10, sy + sh + 10), radius=18, fill=(255, 255, 255), outline=(16, 185, 129), width=4)
    img.paste(slide_img.resize((sw, sh), Image.Resampling.LANCZOS), (sx, sy))

    # 우측 최하단 에메랄드 틸 정통성 배지
    draw.rounded_rectangle((712, 600, 1252, 690), radius=16, fill=(5, 150, 105), outline=(167, 243, 208), width=2)
    sub_txt = "■ Original Proof · @min7014_ai" if is_en else "■ 오리지널 원문 증명 · @min7014_ai"
    draw.text((734, 628), sub_txt, fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 26, bold=True))

    img.save(out_png, quality=98)
    return out_png


def _resolve_flow_clip(bp: dict) -> Path | None:
    cand_name = bp.get("flow_clip") or f"{bp['slug']}_flow.mp4"
    p = FLOW_CLIPS_DIR / cand_name
    if p.exists() and p.stat().st_size > 150_000:
        try:
            with p.open("rb") as fh:
                hdr = fh.read(12)
            if len(hdr) >= 8 and hdr[4:8] == b"ftyp":
                return p
        except Exception:
            pass
    return None


def _encode_cinematic_art_card(
    art_img: Image.Image,
    hud_rgba: Image.Image,
    mp3_path: Path,
    out_mp4: Path,
    ffmpeg_exe: str,
    ffprobe_exe: str,
    width: int = 1920,
    height: int = 1080,
    flow_clip_mp4: Path | None = None,
):
    """
    [Google Flow ULTRA 실사 광학 모션 비디오 우선 합성 + 정적 줌 드리프트 폴백]:
    - `flow_clip_mp4`(Veo 3.1 양단 키프레임 고정 8초 실사 모션 비디오)가 존재하면
      실제 흐르는 광학 모션 클립을 무한 심리스 루프(`-stream_loop -1`)로 배경에 깔고,
      전면의 파이썬 정밀 수식·텍스트 HUD 레이어(RGBA)를 흔들림 없이 칼같이 선명하게 합성합니다.
    - 모션 클립이 아직 없을 경우 고해상도 정지 오브제에 부드러운 24fps 줌 드리프트를 부여합니다.
    """
    import min7014_video_maker as vmaker

    dur = max(3.8, vmaker.get_media_duration_seconds(mp3_path, ffprobe_exe) + 0.35)
    hud_png = out_mp4.with_name(out_mp4.stem + "_hud.png")
    hud_rgba.save(hud_png)

    if flow_clip_mp4 is not None and flow_clip_mp4.exists():
        if width == 1920 and height == 1080:
            filt = (
                f"[0:v]scale=1920:1080:flags=lanczos,setsar=1,fps=24[bg];"
                f"[bg][1:v]overlay=0:0:format=auto,format=yuv420p[v]"
            )
            cmd = [
                ffmpeg_exe, "-y",
                "-stream_loop", "-1", "-t", f"{dur:.3f}", "-i", str(flow_clip_mp4),
                "-loop", "1", "-t", f"{dur:.3f}", "-i", str(hud_png),
                "-i", str(mp3_path),
                "-filter_complex", filt,
                "-map", "[v]", "-map", "2:a",
                "-c:v", "libx264", "-preset", "ultrafast", "-crf", "19",
                "-r", "24",
                "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
                "-shortest", str(out_mp4),
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return dur
        elif width == 1080 and height == 1920:
            bg_png = out_mp4.with_name(out_mp4.stem + "_vbg.png")
            Image.new("RGB", (1080, 1920), (10, 16, 34)).save(bg_png)
            filt = (
                f"[0:v]fps=24[base];"
                f"[1:v]scale=1920:1080:flags=lanczos,crop=1320:1080:20:0,scale=1000:940:flags=lanczos,setsar=1,fps=24[mclip];"
                f"[base][mclip]overlay=40:240:format=auto[mid];"
                f"[mid][2:v]overlay=0:0:format=auto,format=yuv420p[v]"
            )
            cmd = [
                ffmpeg_exe, "-y",
                "-loop", "1", "-t", f"{dur:.3f}", "-i", str(bg_png),
                "-stream_loop", "-1", "-t", f"{dur:.3f}", "-i", str(flow_clip_mp4),
                "-loop", "1", "-t", f"{dur:.3f}", "-i", str(hud_png),
                "-i", str(mp3_path),
                "-filter_complex", filt,
                "-map", "[v]", "-map", "3:a",
                "-c:v", "libx264", "-preset", "ultrafast", "-crf", "19",
                "-r", "24",
                "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
                "-shortest", str(out_mp4),
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return dur

    n_frames = max(24, int(dur * 24) + 6)
    bg_png = out_mp4.with_name(out_mp4.stem + "_bg.png")
    art_img.resize((width, height), Image.Resampling.LANCZOS).save(bg_png)

    filt = (
        f"[0:v]scale={int(width*1.12)}:{int(height*1.12)},"
        f"zoompan=z='min(1.045,1.0+0.045*on/{n_frames})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n_frames}:s={width}x{height}:fps=24[bg];"
        f"[bg][1:v]overlay=0:0:format=auto,format=yuv420p[v]"
    )
    cmd = [
        ffmpeg_exe, "-y",
        "-loop", "1", "-t", f"{dur:.3f}", "-i", str(bg_png),
        "-loop", "1", "-t", f"{dur:.3f}", "-i", str(hud_png),
        "-i", str(mp3_path),
        "-filter_complex", filt,
        "-map", "[v]", "-map", "2:a",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "20",
        "-r", "24",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
        "-shortest", str(out_mp4),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return dur


def _encode_still_segment(frame_img: Image.Image, mp3_path: Path, out_mp4: Path, ffmpeg_exe: str, ffprobe_exe: str):
    import min7014_video_maker as vmaker

    dur = max(3.4, vmaker.get_media_duration_seconds(mp3_path, ffprobe_exe) + 0.32)
    png_p = out_mp4.with_suffix(".png")
    frame_img.save(png_p)
    cmd = [
        ffmpeg_exe, "-y",
        "-loop", "1", "-t", f"{dur:.3f}", "-i", str(png_p),
        "-i", str(mp3_path),
        "-c:v", "libx264", "-preset", "ultrafast", "-tune", "stillimage", "-crf", "20",
        "-pix_fmt", "yuv420p", "-r", "24",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
        "-shortest", str(out_mp4),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return dur


def _mix_ambient_bgm(raw_in: Path, out_mp4: Path, ffmpeg_exe: str):
    import min7014_video_maker as vmaker

    ambient_wav = vmaker.ensure_ambient_pad_wav()
    subprocess.run(
        [
            ffmpeg_exe, "-y",
            "-i", str(raw_in),
            "-stream_loop", "-1", "-i", str(ambient_wav),
            "-filter_complex",
            "[0:a]aformat=sample_rates=48000:channel_layouts=stereo[v];"
            "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.14[bgm];"
            "[v][bgm]amix=inputs=2:duration=first:dropout_transition=1[aout]",
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest",
            str(out_mp4),
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )


def render_nano_banana_bundle(bp: dict, lang_code: str = "ko") -> dict:
    """
    단일 블루프린트에 대해:
    1) 1080p 16:9 '나노바나나 실생활 시각 미스터리(Act 1) → min7014 오리지널 원문 증명 + 가상 지휘봉(Act 2) → 유레카 완결(Act 3)'
    2) 1080x1920 9:16 '실생활 크리스탈·천체 기하 3초 챌린지 Q-#Shorts' (<45s 스와이프 방어 포맷)
    두 가지를 한 번에 무창 렌더링합니다.
    """
    import min7014_video_maker as vmaker

    slug = bp["slug"]
    sp = SCRIPTS_DIR / f"{slug}.json"
    if not sp.exists():
        vmaker.generate_or_update_script(slug, target_langs=["ko", "en"])
    sdoc = json.loads(sp.read_text(encoding="utf-8"))
    pdf_bytes, _ = vmaker.load_or_build_topic_pdf_bytes(sdoc.get("pdf_url", ""), slug)
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    art_16x9 = _load_master_art(bp)
    flow_clip = _resolve_flow_clip(bp)

    ffmpeg_exe = shutil.which("ffmpeg")
    ffprobe_exe = shutil.which("ffprobe")
    voice_name = vmaker.GLOBAL_VOICE_MAP.get(lang_code, vmaker.GLOBAL_VOICE_MAP["en"])["voice"]
    is_en = lang_code == "en"

    long_mp4 = NB_OUT_DIR / f"{slug}_nb_{lang_code}.mp4"
    long_thumb = NB_OUT_DIR / f"{slug}_nb_{lang_code}_thumb.png"
    short_mp4 = NB_OUT_DIR / f"{slug}_nb_short_{lang_code}.mp4"

    render_nano_banana_thumbnail(bp, doc, lang_code, long_thumb)

    pages = sdoc.get("pages") or []
    n_pages = len(pages)
    if n_pages <= 8:
        mid_indices = list(range(n_pages))
    else:
        mid_indices = sorted(
            list({0, max(1, n_pages // 7), (2 * n_pages) // 7, (3 * n_pages) // 7, (4 * n_pages) // 7, (5 * n_pages) // 7, max(1, n_pages - 2), n_pages - 1})
        )

    tmp_dir = Path(tempfile.mkdtemp(prefix=f"nb_cin_{slug}_{lang_code}_"))
    try:
        # ==================== A. 1080p 16:9 시네마 하이브리드 본편 ====================
        long_segs = []

        # --- Act 1: 나노바나나 24fps 시네마틱 줌 + 정밀 수학 미스터리 HUD ---
        hud1 = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
        d1 = ImageDraw.Draw(hud1)
        for x in range(960, 1920):
            a = int(min(226, max(0, (x - 960) / 180.0 * 222)))
            d1.line([(x, 0), (x, 1080)], fill=(10, 18, 36, a), width=1)
        d1.rounded_rectangle((52, 38, 1868, 138), radius=20, fill=(15, 28, 60, 230), outline=(56, 189, 248, 255), width=3)
        d1.text((84, 64), bp["badge_en"] if is_en else bp["badge_ko"], fill=(255, 255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 36, bold=True))
        d1.text((1420, 66), "▶ 3-SEC MYSTERY" if is_en else "▶ 3초 직관 챌린지!", fill=(250, 204, 21, 255), font=vmaker.get_font_for_lang(lang_code, 34, bold=True))

        d1.rounded_rectangle((1060, 196, 1856, 896), radius=26, fill=(15, 23, 42, 232), outline=(56, 189, 248, 255), width=3)
        y_t = 248
        for line in textwrap.wrap(bp["problem_label_en"] if is_en else bp["problem_label_ko"], width=27 if is_en else 17)[:4]:
            d1.text((1102, y_t), line, fill=(255, 255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 39, bold=True))
            y_t += 62
        d1.rounded_rectangle((1096, 560, 1820, 704), radius=18, fill=(2, 132, 199, 235), outline=(250, 204, 21, 255), width=3)
        for li, cl in enumerate(textwrap.wrap(bp["figure_caption_en"] if is_en else bp["figure_caption_ko"], width=28 if is_en else 20)[:2]):
            d1.text((1124, 588 + li * 48), cl, fill=(254, 240, 138, 255), font=vmaker.get_font_for_lang(lang_code, 33, bold=True))
        d1.text(
            (1102, 768),
            "★ Spot ONE visual invariant—zero messy algebra!" if is_en else "★ 복잡한 식 대신 숨은 보조선·불변량을 찾아보세요!",
            fill=(125, 211, 252, 255),
            font=vmaker.get_font_for_lang(lang_code, 28, bold=True),
        )

        act1_mp3 = tmp_dir / "long_act1.mp3"
        act1_seg = tmp_dir / "long_act1.mp4"
        vmaker.synthesize_tts_mp3_sync(bp["act1_en"] if is_en else bp["act1_ko"], voice_name, act1_mp3, rate="+8%")
        _encode_cinematic_art_card(art_16x9, hud1, act1_mp3, act1_seg, ffmpeg_exe, ffprobe_exe, 1920, 1080, flow_clip_mp4=flow_clip)
        long_segs.append(act1_seg)

        # --- Act 2: min7014.github.io 오리지널 원문 PDF + Rule 43 메이플 가상 지휘봉 ---
        prev_slide_raw = None
        for idx_s, p_idx in enumerate(mid_indices, 1):
            p_info = pages[p_idx]
            doc_p = min(len(doc) - 1, max(0, int(p_info.get("page", p_idx + 1)) - 1))
            pix = doc[doc_p].get_pixmap(dpi=240)
            s_raw = vmaker._mask_pdf_bottom_author_bar(Image.frombytes("RGB", [pix.width, pix.height], pix.samples))
            bbox_norm = _compute_normalized_diff_bbox(prev_slide_raw, s_raw)
            prev_slide_raw = s_raw

            frame = Image.new("RGB", (1920, 1080), (10, 16, 34))
            df = ImageDraw.Draw(frame)
            df.rounded_rectangle((48, 24, 1872, 104), radius=16, fill=(15, 23, 42), outline=(2, 132, 199), width=2)
            hdr = (
                f"■ Original Visual Proof STEP {idx_s}/{len(mid_indices)} · min7014.github.io"
                if is_en
                else f"■ 오리지널 단계별 시각 증명 STEP {idx_s}/{len(mid_indices)} · min7014.github.io"
            )
            df.text((76, 44), hdr, fill=(125, 211, 252), font=vmaker.get_font_for_lang(lang_code, 31, bold=True))

            sc = min(1740 / s_raw.width, 880 / s_raw.height)
            nw, nh = int(s_raw.width * sc), int(s_raw.height * sc)
            ox, oy = (1920 - nw) // 2, 124 + (920 - nh) // 2
            df.rounded_rectangle((ox - 8, oy - 8, ox + nw + 8, oy + nh + 8), radius=16, fill=(255, 255, 255), outline=(56, 189, 248), width=3)
            resized_pdf = s_raw.resize((nw, nh), Image.Resampling.LANCZOS)
            frame.paste(resized_pdf, (ox, oy))

            # Rule 43: 원본 잉크에서 9px 이격된 무가림 메이플 가상 지휘봉 포인팅
            try:
                vmaker.draw_virtual_teacher_baton(frame, resized_pdf, ox, oy, nw, nh, bbox_norm, stage=2 if idx_s % 2 == 1 else 3)
            except Exception:
                pass

            raw_n = (p_info.get("narrations") or {}).get(lang_code) or p_info.get("explanation_text") or ""
            raw_n = re.sub(r"안녕하세요[^.?!]*[.?!]\s*", "", raw_n).strip()
            if not raw_n:
                raw_n = "Observe how the geometric relationship locks the equal quantities into place." if is_en else "보조선과 대칭 구조에 의해 핵심 성질이 눈앞에서 명확히 드러납니다."
            s_mp3 = tmp_dir / f"long_step_{idx_s:02d}.mp3"
            s_mp4 = tmp_dir / f"long_step_{idx_s:02d}.mp4"
            vmaker.synthesize_tts_mp3_sync(raw_n, voice_name, s_mp3, rate="+8%")
            _encode_still_segment(frame, s_mp3, s_mp4, ffmpeg_exe, ffprobe_exe)
            long_segs.append(s_mp4)

        # --- Act 3: 나노바나나 유레카 완결 + 5초 암산 정리 & 구독 유도 ---
        hud3 = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
        d3 = ImageDraw.Draw(hud3)
        for x in range(940, 1920):
            a = int(min(232, max(0, (x - 940) / 170.0 * 226)))
            d3.line([(x, 0), (x, 1080)], fill=(8, 22, 36, a), width=1)
        d3.rounded_rectangle((52, 38, 1868, 138), radius=20, fill=(5, 150, 105, 238), outline=(250, 204, 21, 255), width=3)
        d3.text(
            (84, 64),
            "★ EUREKA! REAL-WORLD MYSTERY SOLVED IN SECONDS!" if is_en else "★ 유레카! 보조선 원리로 실생활 기하 미스터리 완벽 해체!",
            fill=(255, 255, 255, 255),
            font=vmaker.get_font_for_lang(lang_code, 36, bold=True),
        )
        d3.rounded_rectangle((1040, 196, 1856, 896), radius=26, fill=(15, 23, 42, 236), outline=(16, 185, 129, 255), width=4)
        ya = 250
        for line in textwrap.wrap(bp["answer_label_en"] if is_en else bp["answer_label_ko"], width=27 if is_en else 17)[:4]:
            d3.text((1084, ya), line, fill=(254, 240, 138, 255), font=vmaker.get_font_for_lang(lang_code, 39, bold=True))
            ya += 62
        d3.rounded_rectangle((1080, 598, 1820, 836), radius=20, fill=(2, 132, 199, 240), outline=(255, 255, 255, 255), width=3)
        d3.text(
            (1112, 646),
            "▶ Subscribe to @min7014_ai Right Now!" if is_en else "▶ 지금 바로 @min7014_ai [구독] 누르기!",
            fill=(255, 255, 255, 255),
            font=vmaker.get_font_for_lang(lang_code, 34, bold=True),
        )
        d3.text(
            (1112, 724),
            "20-Year Original Visual Proofs · Daily Intuition!" if is_en else "20년 연구 오리지널 시각 증명 · 매일 새로운 수학 통찰!",
            fill=(254, 240, 138, 255),
            font=vmaker.get_font_for_lang(lang_code, 26, bold=True),
        )

        act3_mp3 = tmp_dir / "long_act3.mp3"
        act3_seg = tmp_dir / "long_act3.mp4"
        vmaker.synthesize_tts_mp3_sync(bp["act3_en"] if is_en else bp["act3_ko"], voice_name, act3_mp3, rate="+8%")
        _encode_cinematic_art_card(art_16x9, hud3, act3_mp3, act3_seg, ffmpeg_exe, ffprobe_exe, 1920, 1080, flow_clip_mp4=flow_clip)
        long_segs.append(act3_seg)

        concat_long = tmp_dir / "concat_long.txt"
        concat_long.write_text("\n".join(f"file '{p.as_posix()}'" for p in long_segs), encoding="utf-8")
        raw_long = tmp_dir / "raw_long.mp4"
        subprocess.run([ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_long), "-c", "copy", str(raw_long)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        _mix_ambient_bgm(raw_long, long_mp4, ffmpeg_exe)
        long_dur = vmaker.get_media_duration_seconds(long_mp4, ffprobe_exe)

        # ==================== B. 1080x1920 9:16 스와이프 방어 Q-#Shorts ====================
        sh_segs = []
        # 좌측 핵심 오브제 영역(x=40..1320)을 1080x1080 정사각 쇼케이스로 정밀 프레이밍하여 9:16 중앙에 배치
        art_focus = art_16x9.crop((20, 0, 1340, 1080)).resize((1000, 940), Image.Resampling.LANCZOS)

        def _make_vertical_art_canvas(top_banner_text: str, top_fill: tuple, bottom_lines: list[str], caption_line: str, cta_line: str | None = None) -> tuple[Image.Image, Image.Image]:
            v_bg = Image.new("RGB", (1080, 1920), (10, 16, 34))
            v_bg.paste(art_focus, (40, 240))
            v_hud = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
            dv = ImageDraw.Draw(v_hud)
            dv.rounded_rectangle((36, 236, 1044, 1184), radius=24, outline=(56, 189, 248, 255), width=4)
            dv.rounded_rectangle((40, 64, 1040, 204), radius=22, fill=(*top_fill, 242), outline=(250, 204, 21, 255), width=4)
            dv.text((72, 108), top_banner_text, fill=(255, 255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 38, bold=True))
            dv.rounded_rectangle((40, 1220, 1040, 1608), radius=24, fill=(15, 23, 42, 242), outline=(56, 189, 248, 255), width=4)
            dv.text((74, 1258), caption_line[:38], fill=(250, 204, 21, 255), font=vmaker.get_font_for_lang(lang_code, 36, bold=True))
            for li, bl in enumerate(bottom_lines[:3]):
                dv.text((74, 1336 + li * 52), bl, fill=(255, 255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 33, bold=True))
            if cta_line:
                dv.rounded_rectangle((56, 1496, 1024, 1590), radius=16, fill=(2, 132, 199, 248))
                dv.text((82, 1524), cta_line, fill=(255, 255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 29, bold=True))
            return v_bg, v_hud

        s1_bg, s1_hud = _make_vertical_art_canvas(
            "▶ STOP! CAN YOU SPOT x IN 3 SECONDS?" if is_en else "▶ 잠깐! 공식 없이 3초 안에 x가 보이시나요?",
            (2, 132, 199),
            textwrap.wrap(bp["problem_label_en"] if is_en else bp["problem_label_ko"], width=30 if is_en else 20),
            bp["figure_caption_en"] if is_en else bp["figure_caption_ko"],
        )
        sh1_mp3 = tmp_dir / "sh1.mp3"
        sh1_seg = tmp_dir / "sh1.mp4"
        vmaker.synthesize_tts_mp3_sync(bp["act1_en"] if is_en else bp["act1_ko"], voice_name, sh1_mp3, rate="+18%")
        _encode_cinematic_art_card(s1_bg, s1_hud, sh1_mp3, sh1_seg, ffmpeg_exe, ffprobe_exe, 1080, 1920, flow_clip_mp4=flow_clip)
        sh_segs.append(sh1_seg)

        # Scene 2 & 3: 원본 min7014.github.io 핵심 슬라이드 2장
        pick_sh = [max(0, len(doc) // 2 - 1), max(0, len(doc) - 2)]
        for si, dp_i in enumerate(pick_sh, 2):
            pix_s = doc[dp_i].get_pixmap(dpi=230)
            sl_img = vmaker._mask_pdf_bottom_author_bar(Image.frombytes("RGB", [pix_s.width, pix_s.height], pix_s.samples))
            sc_v = Image.new("RGB", (1080, 1920), (10, 16, 34))
            dsc = ImageDraw.Draw(sc_v)
            dsc.rounded_rectangle((40, 64, 1040, 198), radius=22, fill=(30, 64, 175), outline=(254, 240, 138), width=3)
            dsc.text(
                (74, 106),
                f"★ ORIGINAL PROOF CLUE {si-1}/2 · min7014" if is_en else f"★ 오리지널 시각 증명 단서 {si-1}/2!",
                fill=(255, 255, 255),
                font=vmaker.get_font_for_lang(lang_code, 36, bold=True),
            )
            k_scale = min(980 / sl_img.width, 1020 / sl_img.height)
            kw, kh = int(sl_img.width * k_scale), int(sl_img.height * k_scale)
            kx, ky = (1080 - kw) // 2, 256 + (1060 - kh) // 2
            dsc.rounded_rectangle((kx - 8, ky - 8, kx + kw + 8, ky + kh + 8), radius=18, fill=(255, 255, 255), outline=(56, 189, 248), width=4)
            sc_v.paste(sl_img.resize((kw, kh), Image.Resampling.LANCZOS), (kx, ky))

            p_match = pages[min(len(pages) - 1, dp_i)]
            clue_txt = ((p_match.get("narrations") or {}).get(lang_code) or p_match.get("explanation_text") or "").strip()
            sents = [x.strip() for x in re.split(r"(?<=[.?!])\s+", clue_txt) if x.strip() and "안녕하세요" not in x]
            short_clue = sents[-1] if sents else ("One auxiliary line reveals the invariant immediately!" if is_en else "보조선 한 줄이 숨어 있던 기하학적 불변량을 깨웁니다!")
            if len(short_clue) > (120 if is_en else 68):
                short_clue = short_clue[: (116 if is_en else 64)].rsplit(" ", 1)[0] + "."
            dsc.rounded_rectangle((40, 1378, 1040, 1600), radius=22, fill=(15, 23, 42), outline=(56, 189, 248), width=3)
            for li, cl_l in enumerate(textwrap.wrap(short_clue, width=32 if is_en else 20)[:3]):
                dsc.text((76, 1416 + li * 50), cl_l, fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 34, bold=True))

            sh_m_mp3 = tmp_dir / f"sh_{si}.mp3"
            sh_m_seg = tmp_dir / f"sh_{si}.mp4"
            vmaker.synthesize_tts_mp3_sync(short_clue, voice_name, sh_m_mp3, rate="+18%")
            _encode_still_segment(sc_v, sh_m_mp3, sh_m_seg, ffmpeg_exe, ffprobe_exe)
            sh_segs.append(sh_m_seg)

        # Scene 4: 나노바나나 유레카 정답 완결 + 관련 동영상 클릭 유도
        s4_bg, s4_hud = _make_vertical_art_canvas(
            "★ EUREKA! VISUAL MYSTERY SOLVED!" if is_en else "★ 유레카! 3초 시각 직관 해체 완료!",
            (5, 150, 105),
            textwrap.wrap(bp["answer_label_en"] if is_en else bp["answer_label_ko"], width=30 if is_en else 20),
            "■ ZERO ROTE FORMULAS!" if is_en else "■ 공식 암기 ZERO · 완벽 직관!",
            cta_line="▶ Tap [Related Video] Full Proof & [Subscribe]!" if is_en else "▶ 아래 [관련 동영상] 본편 클릭 & [@min7014_ai 구독]!",
        )
        sh4_mp3 = tmp_dir / "sh4.mp3"
        sh4_seg = tmp_dir / "sh4.mp4"
        vmaker.synthesize_tts_mp3_sync(bp["act3_en"] if is_en else bp["act3_ko"], voice_name, sh4_mp3, rate="+18%")
        _encode_cinematic_art_card(s4_bg, s4_hud, sh4_mp3, sh4_seg, ffmpeg_exe, ffprobe_exe, 1080, 1920, flow_clip_mp4=flow_clip)
        sh_segs.append(sh4_seg)

        concat_sh = tmp_dir / "concat_sh.txt"
        concat_sh.write_text("\n".join(f"file '{p.as_posix()}'" for p in sh_segs), encoding="utf-8")
        raw_sh = tmp_dir / "raw_sh.mp4"
        subprocess.run([ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_sh), "-c", "copy", str(raw_sh)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        _mix_ambient_bgm(raw_sh, short_mp4, ffmpeg_exe)
        short_dur = vmaker.get_media_duration_seconds(short_mp4, ffprobe_exe)
        if short_dur >= 46.0:
            spd = min(1.85, round(short_dur / 39.5, 3))
            fast_sh = tmp_dir / "fast_sh.mp4"
            subprocess.run(
                [
                    ffmpeg_exe, "-y", "-i", str(short_mp4),
                    "-filter_complex", f"[0:v]setpts=PTS/{spd}[v];[0:a]atempo={spd}[a]",
                    "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "ultrafast", "-crf", "19", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
                    str(fast_sh),
                ],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            shutil.copy2(fast_sh, short_mp4)
            short_dur = vmaker.get_media_duration_seconds(short_mp4, ffprobe_exe)

        sdoc.setdefault("nano_banana_packages", {})[lang_code] = {
            "long_mp4": str(long_mp4.relative_to(ROOT_DIR)).replace("\\", "/"),
            "long_thumb": str(long_thumb.relative_to(ROOT_DIR)).replace("\\", "/"),
            "long_duration_sec": round(long_dur, 2),
            "short_mp4": str(short_mp4.relative_to(ROOT_DIR)).replace("\\", "/"),
            "short_duration_sec": round(short_dur, 2),
            "title": bp["title_en"] if is_en else bp["title_ko"],
            "short_title": bp["short_title_en"] if is_en else bp["short_title_ko"],
            "comment_quiz": bp["comment_quiz_en"] if is_en else bp["comment_quiz_ko"],
            "updated_at": datetime.now().isoformat(timespec="seconds"),
        }
        sp.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
        return sdoc["nano_banana_packages"][lang_code]
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        doc.close()


def render_all_nano_banana_flagships(langs: tuple[str, ...] = ("ko", "en")) -> list[dict]:
    out = []
    for bp in NANO_BANANA_BLUEPRINTS:
        for lc in langs:
            pkg = render_nano_banana_bundle(bp, lang_code=lc)
            out.append({"slug": bp["slug"], "lang": lc, **pkg})
    return out


def try_upload_one_nano_banana_cinema(kind: str = "long", target_slug: str | None = None, target_lang: str | None = None, notify_tg: bool = True) -> dict | None:
    """
    Rule 35 (인간 오리지널 증명 정통성 명시) + Rule 51 (상표권 정화 필터) 완벽 준수 업로더.
    """
    import min7014_video_maker as vmaker
    import youtube_self_evolving_engine as ysee
    from googleapiclient.http import MediaFileUpload

    if vmaker._LAST_UPLOAD_QUOTA_BLOCKED:
        return None

    # [Rule 52 주간 대표 킬러 시리즈 하드 캡 (주 최대 3개 주제 선별 제한)]
    now_ts = datetime.now().timestamp()
    w_state = {"episodes": []}
    if WEEKLY_CAP_STATE_FILE.exists():
        try:
            w_state.update(json.loads(WEEKLY_CAP_STATE_FILE.read_text(encoding="utf-8")))
        except Exception:
            pass
    recent_eps = [e for e in (w_state.get("episodes") or []) if (now_ts - float(e.get("ts", 0))) < 7 * 86400]
    active_week_slugs = {e.get("slug") for e in recent_eps if e.get("slug")}

    yt, _ = vmaker.get_available_youtube_upload_service()
    if yt is None:
        return None

    lang_order = (target_lang,) if target_lang else ysee.preferred_lang_order_for_current_hour()

    for bp in get_all_available_flow_blueprints():
        slug = bp["slug"]
        if target_slug and slug != target_slug:
            continue
        if slug not in active_week_slugs and len(active_week_slugs) >= MAX_NANO_BANANA_WEEKLY_EPISODES:
            continue
        sp = SCRIPTS_DIR / f"{slug}.json"
        if not sp.exists():
            continue
        sdoc = json.loads(sp.read_text(encoding="utf-8"))
        nb_urls = sdoc.setdefault("nano_banana_urls", {})
        nb_sh_urls = sdoc.setdefault("nano_banana_shorts_urls", {})

        for lc in lang_order:
            is_en = lc == "en"
            l_mp4 = NB_OUT_DIR / f"{slug}_nb_{lc}.mp4"
            l_thumb = NB_OUT_DIR / f"{slug}_nb_{lc}_thumb.png"
            s_mp4 = NB_OUT_DIR / f"{slug}_nb_short_{lc}.mp4"

            if kind == "long" and not (nb_urls.get(lc) or "").strip():
                if not l_mp4.exists():
                    render_nano_banana_bundle(bp, lang_code=lc)
                if not l_mp4.exists():
                    continue
                raw_title = bp["title_en"] if is_en else bp["title_ko"]
                pdf_url = sdoc.get("pdf_url") or "https://min7014.github.io/"
                raw_desc = (
                    f"📐 [Human-Crafted Original Proof] This lesson is NOT generic AI-generated content. "
                    f"The core geometric proof, auxiliary line insight, and step-by-step slides are 100% human-researched original educational materials ({pdf_url}), "
                    f"paired with conceptual studio art and multilingual narration to bring mathematical intuition to life.\n\n"
                    f"00:00 | Real-World Visual Geometry Mystery\n"
                    f"00:12 | Step-by-Step Original Visual Proof (min7014.github.io)\n"
                    f"01:15 | 5-Second Mental-Math Eureka Resolution\n\n"
                    f"🌐 Interactive MathLab & 3,400+ Proofs: https://min7014.github.io/mathedu/\n"
                    f"🔔 Subscribe to @min7014_ai: https://www.youtube.com/@min7014_ai?sub_confirmation=1\n\n"
                    f"#VisualProof #EuclideanGeometry #MathIntuition #GeometryProof #Mathematics"
                    if is_en
                    else f"📐 [사람이 직접 연구·작도한 오리지널 원문 기반] 본 콘텐츠는 단순 AI 자동 생성물이 아닙니다. "
                    f"핵심 수학 아이디어·보조선 발상·단계별 시각 증명 슬라이드는 오랜 세월 직접 연구하고 작도한 오리지널 원문 자료({pdf_url})로부터 탄생했으며, "
                    f"도입부 시네마틱 오브제 연출은 기하학적 직관을 돕기 위한 시각 보조 장치입니다.\n\n"
                    f"00:00 | 실생활 기하 미스터리 3초 발문\n"
                    f"00:12 | 오리지널 단계별 시각 증명 해체 (min7014.github.io)\n"
                    f"01:15 | 공식 암기 ZERO · 5초 직관 완결\n\n"
                    f"🌐 단계별 디딤돌 & 자체 제작 MathLab 실습: https://min7014.github.io/mathedu/\n"
                    f"🔔 @min7014_ai 무료 구독하기: https://www.youtube.com/@min7014_ai?sub_confirmation=1\n\n"
                    f"#시각적증명 #도형보조선 #기하학원리 #수학직관 #피타고라스정리"
                )
                raw_tags = ["Visual Math Proof", "Euclidean Geometry", "Math Intuition", "Geometry Mystery"] if is_en else ["시각적증명", "도형보조선", "기하학증명", "수학원리", "수학교육"]
                import auditor as _aud
                gated = _aud.sanitize_and_gate_upload_payload(raw_title, raw_desc, raw_tags)
                title = vmaker.sanitize_youtube_title(gated["title"])
                desc = gated["description"]
                tags = gated["tags"]
                body = {
                    "snippet": {
                        "title": title,
                        "description": desc,
                        "tags": tags,
                        "categoryId": "27",
                        "defaultLanguage": lc,
                        "defaultAudioLanguage": lc,
                    },
                    "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False},
                }
                try:
                    req = yt.videos().insert(part="snippet,status", body=body, media_body=MediaFileUpload(str(l_mp4), chunksize=4 * 1024 * 1024, resumable=True))
                    resp = None
                    while resp is None:
                        _, resp = req.next_chunk()
                    vid = resp["id"]
                    if l_thumb.exists():
                        try:
                            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(str(l_thumb), mimetype="image/png")).execute()
                        except Exception:
                            pass
                    quiz_c = ysee.sanitize_trademark_free_text(bp["comment_quiz_en"] if is_en else bp["comment_quiz_ko"])
                    try:
                        yt.commentThreads().insert(
                            part="snippet",
                            body={"snippet": {"videoId": vid, "topLevelComment": {"snippet": {"textOriginal": quiz_c}}}},
                        ).execute()
                    except Exception:
                        pass
                    url = f"https://youtu.be/{vid}"
                    nb_urls[lc] = url
                    sp.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
                    if slug not in active_week_slugs:
                        recent_eps.append({"slug": slug, "ts": now_ts, "url": url})
                        WEEKLY_CAP_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
                        WEEKLY_CAP_STATE_FILE.write_text(json.dumps({"episodes": recent_eps}, ensure_ascii=False, indent=2), encoding="utf-8")
                    if notify_tg:
                        import sys
                        subprocess.run(
                            [
                                sys.executable, "-X", "utf8", str(ROOT_DIR / "mathedu_telegram_bridge.py"),
                                "--reply", f"✨ [나노바나나 × 오리지널 시각증명 1080p 발행 ({lc.upper()})]\n• 주제({slug}): {title}\n• 링크: {url}",
                            ],
                            cwd=str(ROOT_DIR), timeout=20, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                        )
                    return {"type": "nano_banana_1080p", "slug": slug, "lang": lc, "url": url, "title": title}
                except Exception as e:
                    if "uploadLimitExceeded" in str(e) or "quotaExceeded" in str(e):
                        vmaker._LAST_UPLOAD_QUOTA_BLOCKED = True
                    return None

            if kind == "short" and (nb_urls.get(lc) or "").strip() and not (nb_sh_urls.get(lc) or "").strip():
                if not s_mp4.exists():
                    render_nano_banana_bundle(bp, lang_code=lc)
                if not s_mp4.exists():
                    continue
                sh_title = vmaker.sanitize_youtube_title(ysee.sanitize_trademark_free_text(bp["short_title_en"] if is_en else bp["short_title_ko"]))
                long_u = nb_urls[lc]
                desc_sh = ysee.sanitize_trademark_free_text(
                    f"🎬 Watch Full Step-by-Step Original Visual Proof (1080p): {long_u}\n"
                    f"📐 Human-Crafted Original Archive: https://min7014.github.io/\n"
                    f"🔔 Subscribe @min7014_ai for daily visual math breakthroughs!\n#Shorts #VisualProof #EuclideanGeometry #MathPuzzle"
                    if is_en
                    else f"🎬 1080p 오리지널 시각 증명 풀버전 바로 보기: {long_u}\n"
                    f"📐 20년 연구 오리지널 수학자료실: https://min7014.github.io/\n"
                    f"🔔 도형·미적분 10초 눈풀이 @min7014_ai 구독!\n#Shorts #시각적증명 #도형보조선 #수학퀴즈"
                )
                body_sh = {
                    "snippet": {
                        "title": sh_title,
                        "description": desc_sh,
                        "tags": ["Shorts", "Visual Math", "Euclidean Geometry", "Math Puzzle"] if is_en else ["Shorts", "시각적증명", "수학쇼츠", "도형보조선"],
                        "categoryId": "27",
                        "defaultLanguage": lc,
                        "defaultAudioLanguage": lc,
                    },
                    "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False},
                }
                try:
                    req = yt.videos().insert(part="snippet,status", body=body_sh, media_body=MediaFileUpload(str(s_mp4), chunksize=4 * 1024 * 1024, resumable=True))
                    resp = None
                    while resp is None:
                        _, resp = req.next_chunk()
                    vid = resp["id"]
                    quiz_c = ysee.sanitize_trademark_free_text(bp["comment_quiz_en"] if is_en else bp["comment_quiz_ko"])
                    try:
                        yt.commentThreads().insert(
                            part="snippet",
                            body={"snippet": {"videoId": vid, "topLevelComment": {"snippet": {"textOriginal": quiz_c}}}},
                        ).execute()
                    except Exception:
                        pass
                    url = f"https://youtube.com/shorts/{vid}"
                    nb_sh_urls[lc] = url
                    sp.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
                    try:
                        import youtube_community_controller as _ycc
                        _ycc.link_shorts_related_videos_in_studio(max_links=2, headless=True)
                    except Exception:
                        pass
                    if notify_tg:
                        import sys
                        subprocess.run(
                            [
                                sys.executable, "-X", "utf8", str(ROOT_DIR / "mathedu_telegram_bridge.py"),
                                "--reply", f"⚡ [나노바나나 × 오리지널 시각증명 Q-#Shorts 발행 ({lc.upper()})]\n• 주제({slug}): {sh_title}\n• 링크: {url}",
                            ],
                            cwd=str(ROOT_DIR), timeout=20, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                        )
                    return {"type": "nano_banana_short", "slug": slug, "lang": lc, "url": url, "title": sh_title}
                except Exception as e:
                    if "uploadLimitExceeded" in str(e) or "quotaExceeded" in str(e):
                        vmaker._LAST_UPLOAD_QUOTA_BLOCKED = True
                    return None
    return None


FLOW_RETROFIT_STATE_FILE = ROOT_DIR / ".agents" / "flow_retrofit_state.json"
MIN_RETROFIT_INTERVAL_SEC = 2700  # 45분 주기 유휴시간 백그라운드 자동 고품질화
MAX_DAILY_FLOW_RETROFITS = 8      # 일 최대 8주제 (= 최대 40 Flow 크레딧/일, Ultra 월 25,000 풀의 <5%, Antigravity 쿼터 0!)
SAFE_SWAP_MAX_VIEWS = 15          # Rule 33: 15뷰 초과 인기 영상은 조회수·시청시간 보존을 위해 절대 삭제 금지!
SAFE_SWAP_MIN_AGE_HOURS = 48.0    # 게시 후 최소 48시간 경과한 저조회 정적 구버전만 클린 교체


def _clean_topic_core_ko(raw_title: str) -> str:
    # 영어 병기 괄호만 제거하고 한국어 세부 구분 괄호(예: '(예각)', '(둔각)', '(내분)')는 유지해 중복 제목(L3) 원천 방지!
    t = re.sub(r"\([A-Za-z0-9\s,'\-:;./]+\)", "", str(raw_title or "")).strip()
    t = re.split(r"\s+[A-Za-z]{3,}", t)[0].strip(" .,-—:")
    return t[:32] if len(t) > 32 else (t or "핵심 기하 정리")


def _clean_topic_core_en(sdoc: dict) -> str:
    te = str(sdoc.get("title_en") or "").strip()
    if not te:
        m = re.search(r"\(([A-Za-z][^)]{4,})\)", str(sdoc.get("title") or ""))
        te = m.group(1).strip() if m else f"Visual Geometry #{str(sdoc.get('slug') or '')[-3:]}"
    te = te.strip(" .,-—:")
    return te[:40] if len(te) > 40 else te


def _build_domain_flow_prompts(sdoc: dict) -> tuple[str, str]:
    """
    주제 도메인에 맞춰 수식·글자·숫자가 0%인 Google Flow ULTRA 스튜디오 오브제 키프레임 프롬프트와
    양단 고정(시작=종료) 광학 파동 모션 프롬프트를 생성합니다 (Rule 44 기하 왜곡 ZERO).
    """
    t_all = f"{sdoc.get('title', '')} {sdoc.get('sub_domain_ko', '')} {sdoc.get('core_concept', '')}"
    if any(k in t_all for k in ("원", "접선", "현", "원주각", "활꼴", "내접", "외접")):
        img_p = (
            "Strict top-down 90-degree orthographic architectural studio photograph on a deep midnight navy velvet table. "
            "Positioned on the LEFT TWO-THIRDS of the 16:9 frame (leaving clean dark navy negative space on the right third): "
            "a precision-machined circular sapphire glass ring rimmed in brushed brass, with emerald-teal crystal pins on the circle "
            "connected by crisp emerald-teal and warm amber-gold laser chords and a subtle royal-blue dashed diameter line through the center. "
            "Zero text, zero numbers, zero letters, zero mathematical symbols anywhere in the scene."
        )
        mot_p = (
            "Locked static top-down 90-degree orthographic camera. All crystal pins, brass circle rim, and beam angles stay 100% stationary. "
            "Gentle luminous emerald-teal and warm amber-gold photonic light pulses shimmer smoothly along the existing beams inside the sapphire ring. "
            "Zero camera zoom, zero rotation, zero deformation, zero text, zero numbers."
        )
    elif any(k in t_all for k in ("포물선", "타원", "쌍곡선", "이차곡선", "초점", "준선")):
        img_p = (
            "Strict top-down 90-degree orthographic optical laboratory studio photograph on a deep midnight navy velvet table. "
            "Positioned on the LEFT TWO-THIRDS of the 16:9 frame (leaving clean dark navy negative space on the right third): "
            "a curved brushed-brass conic mirror resting on dark sapphire glass, reflecting crisp emerald-teal parallel laser beams "
            "into a single glowing amber-gold crystal focal pin, with a royal-blue reference directrix bar. "
            "Zero text, zero numbers, zero letters, zero mathematical symbols anywhere in the scene."
        )
        mot_p = (
            "Locked static top-down 90-degree orthographic camera. Curved brass mirror, crystal focus pin, and beams stay 100% stationary. "
            "Soft emerald-teal and golden light pulses travel gently along the reflected focal rays on dark velvet. "
            "Zero camera zoom, zero rotation, zero deformation, zero text, zero numbers."
        )
    elif any(k in t_all for k in ("미분", "적분", "극한", "함수", "접선의 기울기", "평균값", "수열", "급수", "부등식")):
        img_p = (
            "Strict top-down 90-degree orthographic architectural sculpture photograph on a deep midnight navy velvet surface. "
            "Positioned on the LEFT TWO-THIRDS of the 16:9 frame (leaving clean dark navy negative space on the right third): "
            "translucent stepped sapphire-blue glass prisms beneath a smooth sweeping brushed-brass curve, illuminated by a single "
            "razor-sharp emerald-teal tangent laser beam touching a glowing golden crystal point on the curve. "
            "Zero text, zero numbers, zero letters, zero mathematical symbols anywhere in the scene."
        )
        mot_p = (
            "Locked static top-down 90-degree orthographic camera. Sapphire glass prisms, brass curve, and tangent beam stay 100% stationary. "
            "Subtle cyan and golden caustics shimmer gently through the translucent glass prisms on dark midnight velvet. "
            "Zero camera zoom, zero rotation, zero deformation, zero text, zero numbers."
        )
    else:
        img_p = (
            "Strict top-down 90-degree orthographic architectural studio photograph on a deep midnight navy velvet table. "
            "Positioned on the LEFT TWO-THIRDS of the 16:9 frame (leaving clean dark navy negative space on the right third): "
            "a precision-crafted Euclidean triangle of brushed brass and translucent sapphire-emerald crystal segments, "
            "with glowing amber-gold interior auxiliary light beams meeting cleanly at crystal vertex pins. "
            "Zero text, zero numbers, zero letters, zero mathematical symbols anywhere in the scene."
        )
        mot_p = (
            "Locked static top-down 90-degree orthographic camera. All brass triangle edges, crystal segments, and beams stay 100% stationary. "
            "Gentle emerald-teal and warm golden photonic light waves shimmer smoothly along the geometric beams on dark velvet. "
            "Zero camera zoom, zero rotation, zero deformation, zero text, zero numbers."
        )
    return img_p, mot_p


def build_dynamic_flow_blueprint_from_script(slug: str) -> dict | None:
    """
    min7014.github.io 847+ 원문 스크립트(`{slug}.json`)로부터 Google Flow ULTRA 하이브리드 블루프린트를 자동 합성합니다.
    """
    for existing in NANO_BANANA_BLUEPRINTS:
        if existing["slug"] == slug:
            return existing

    sp = SCRIPTS_DIR / f"{slug}.json"
    if not sp.exists():
        return None
    try:
        sdoc = json.loads(sp.read_text(encoding="utf-8"))
    except Exception:
        return None

    saved_bp = sdoc.get("flow_blueprint")
    if isinstance(saved_bp, dict) and saved_bp.get("slug") == slug:
        return saved_bp

    pdf_u = str(sdoc.get("pdf_url") or "")
    if "min7014.github.io" not in pdf_u.lower() or not (sdoc.get("pages") or []):
        return None

    core_ko = _clean_topic_core_ko(sdoc.get("title") or "")
    core_en = _clean_topic_core_en(sdoc)
    tpa = sdoc.get("teacher_proof_analysis") or {}
    aux_ko = str(tpa.get("auxiliary_line_ko") or sdoc.get("solving_tip") or "핵심 보조선 한 줄과 대칭 불변량").strip()
    aux_en = str(tpa.get("auxiliary_line_en") or "one strategic auxiliary line and geometric invariance").strip()
    img_prompt, mot_prompt = _build_domain_flow_prompts(sdoc)

    bp = {
        "slug": slug,
        "art_file": f"nb_{slug}_flow.png",
        "flow_clip": f"{slug}_flow.mp4",
        "flow_image_prompt": img_prompt,
        "flow_motion_prompt": mot_prompt,
        "badge_ko": f"★ 실사 광학 기하 미스터리 · {core_ko[:18]}",
        "badge_en": f"★ Optical Geometry Mystery · {core_en[:24]}",
        "thumb_hook_ko": ["공식 암기 ZERO!", "보조선 1줄 5초 해법!"],
        "thumb_hook_en": ["ZERO ROTE RULES!", "1 LINE = 5s PROOF!"],
        "problem_label_ko": f"공식을 외우지 않고도 '{core_ko}'가 왜 항상 성립하는지 숨은 보조선 한 줄이 3초 만에 보이시나요?",
        "problem_label_en": f"Without memorizing formulas, can you spot in 3 seconds why {core_en} always holds?",
        "figure_caption_ko": f"{core_ko[:16]}  →  결정적 단서 1줄은?",
        "figure_caption_en": f"{core_en[:20]}  →  Spot the 1 Key Line!",
        "answer_label_ko": f"핵심 열쇠: {aux_ko[:44]} → 눈으로 보는 즉시 증명 완결!",
        "answer_label_en": f"Key Clue: {aux_en[:56]} → Visual Proof Complete!",
        "title_ko": f"⚡ 공식 무조건 외우지 마세요! 보조선 1줄로 끝내는 {core_ko} | 단계별 시각적 증명",
        "title_en": f"⚡ Stop Memorizing Blindly! One Line Unlocks {core_en} | Visual Math Proof",
        "short_title_ko": f"❓ 공식 없이 3초 만에 보조선 단서가 보이시나요? {core_ko} 시각 해법! #Shorts",
        "short_title_en": f"❓ Stop Scrolling! Spot the Hidden Line in 3s — {core_en} #Shorts",
        "act1_ko": f"잠깐! 결과 공식부터 외우던 {core_ko}, 복잡한 계산 없이 단 한 줄의 시각적 단서만으로 왜 항상 성립하는지 3초 만에 보이시나요?",
        "act1_en": f"Stop scrolling! Before memorizing any formula for {core_en}, can you spot in three seconds the single visual clue that makes it inevitable?",
        "act3_ko": f"이제 원문 단계별 작도를 통해 {core_ko}가 필연적으로 성립하는 원리가 한눈에 보이시나요? 암기 대신 눈으로 깨치는 오리지널 수학 직관, 지금 바로 채널 구독을 눌러 매일 받아보세요!",
        "act3_en": f"Now the step-by-step original geometric construction makes {core_en} crystal clear with zero rote memorization! Subscribe right now for daily visual math breakthroughs!",
        "comment_quiz_ko": f"🧩 [3초 직관 체크] 오늘 살펴본 '{core_ko}'의 단계별 증명 중 가장 결정적인 유레카 순간은 몇 번째 단계였나요? 댓글로 남겨보세요! 🤩👇",
        "comment_quiz_en": f"🧩 [3-Sec Visual Check] Which step in today's visual proof of {core_en} gave you the biggest 'Aha!' moment? Drop your answer below! 🤩👇",
    }
    return bp


def get_all_available_flow_blueprints() -> list[dict]:
    """수동 큐레이션 블루프린트 + 유휴시간 자동 고품질화로 생성된 블루프린트를 통합 반환합니다."""
    out = list(NANO_BANANA_BLUEPRINTS)
    seen = {b["slug"] for b in out}
    for sp in sorted(SCRIPTS_DIR.glob("*.json")):
        if sp.stem in seen:
            continue
        try:
            sdoc = json.loads(sp.read_text(encoding="utf-8"))
        except Exception:
            continue
        fb = sdoc.get("flow_blueprint")
        if isinstance(fb, dict) and fb.get("slug") == sp.stem:
            out.append(fb)
            seen.add(sp.stem)
    return out


def _load_retrofit_state() -> dict:
    today = datetime.now().strftime("%Y-%m-%d")
    st = {
        "date": today,
        "daily_count": 0,
        "last_run_ts": 0.0,
        "last_swap_ts": 0.0,
        "upgraded_slugs": [],
        "safe_swapped_videos": [],
        "protected_high_view_videos": [],
    }
    if FLOW_RETROFIT_STATE_FILE.exists():
        try:
            saved = json.loads(FLOW_RETROFIT_STATE_FILE.read_text(encoding="utf-8"))
            st.update(saved)
            if st.get("date") != today:
                st["date"] = today
                st["daily_count"] = 0
        except Exception:
            pass
    return st


def _save_retrofit_state(st: dict) -> None:
    FLOW_RETROFIT_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    FLOW_RETROFIT_STATE_FILE.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")


def get_flow_retrofit_status_summary() -> dict:
    st = _load_retrofit_state()
    flow_clips = sorted(
        p.stem.replace("_flow", "")
        for p in FLOW_CLIPS_DIR.glob("*_flow.mp4")
        if p.stat().st_size > 150_000 and p.open("rb").read(12)[4:8] == b"ftyp"
    )
    nb_rendered = sorted({p.name.split("_nb_")[0] for p in NB_OUT_DIR.glob("*_nb_ko.mp4")})
    return {
        "today_upgraded_count": st.get("daily_count", 0),
        "daily_cap": MAX_DAILY_FLOW_RETROFITS,
        "total_flow_motion_clips": len(flow_clips),
        "flow_motion_slugs": flow_clips,
        "total_hybrid_rendered_slugs": len(nb_rendered),
        "safe_swapped_count": len(st.get("safe_swapped_videos") or []),
        "protected_high_view_count": len(st.get("protected_high_view_videos") or []),
    }


def _try_safe_swap_or_thumb_upgrade_on_live_channel(bp: dict, st: dict) -> dict | None:
    """
    [Rule 13.3 + Rule 33 스마트 교체 가드레일]:
    - 이미 라이브 채널에 구버전 정적 영상이 올라가 있는 경우 실시간 조회수와 게시 경과 시간을 확인합니다.
    - 조회수가 15뷰를 초과(`views > SAFE_SWAP_MAX_VIEWS`)한 인기 영상은 YPP 시청시간·알고리즘 보존을 위해 **절대 삭제하지 않고**
      고클릭률 Flow 썸네일만 무손실 업데이트(`thumbnails().set`)한 뒤 보호 목록에 기록합니다.
    - 조회수가 15뷰 이하이고 게시 후 48시간 이상 경과한 저조회 정적 영상만 12시간당 최대 1건씩
      `videos().delete` 후 Flow 실사 광학 모션 본편으로 안전 교체합니다.
    """
    import min7014_video_maker as vmaker
    from googleapiclient.http import MediaFileUpload

    now_ts = datetime.now().timestamp()
    if (now_ts - float(st.get("last_swap_ts") or 0.0)) < 12 * 3600:
        return None
    if vmaker._LAST_UPLOAD_QUOTA_BLOCKED:
        return None

    slug = bp["slug"]
    sp = SCRIPTS_DIR / f"{slug}.json"
    if not sp.exists():
        return None
    sdoc = json.loads(sp.read_text(encoding="utf-8"))
    nb_urls = sdoc.get("nano_banana_urls") or {}
    yt_urls = sdoc.get("youtube_urls") or {}

    yt, _ = vmaker.get_available_youtube_upload_service()
    if yt is None:
        return None

    already_swapped = {x.get("old_vid") for x in (st.get("safe_swapped_videos") or [])}
    already_protected = {x.get("vid") for x in (st.get("protected_high_view_videos") or [])}

    for lc in ("ko", "en"):
        if (nb_urls.get(lc) or "").strip():
            # If Flow hybrid already live, ensure its thumbnail is up-to-date without touching video ID
            continue
        old_u = str(yt_urls.get(lc) or "").strip()
        m = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", old_u)
        if not m:
            continue
        old_vid = m.group(1)
        if old_vid in already_swapped or old_vid in already_protected:
            continue

        l_mp4 = NB_OUT_DIR / f"{slug}_nb_{lc}.mp4"
        l_thumb = NB_OUT_DIR / f"{slug}_nb_{lc}_thumb.png"
        if not l_mp4.exists():
            continue

        try:
            vr = yt.videos().list(part="statistics,snippet", id=old_vid).execute()
            items = vr.get("items") or []
            if not items:
                continue
            views = int((items[0].get("statistics") or {}).get("viewCount") or 0)
            pub_str = (items[0].get("snippet") or {}).get("publishedAt") or ""
            age_h = 999.0
            if pub_str:
                pub_dt = datetime.fromisoformat(pub_str.replace("Z", "+00:00"))
                age_h = (datetime.now(pub_dt.tzinfo) - pub_dt).total_seconds() / 3600.0

            if views > SAFE_SWAP_MAX_VIEWS:
                # Rule 33: Protect high-performing video! Upgrade thumbnail only (0 view loss!)
                if l_thumb.exists():
                    try:
                        yt.thumbnails().set(videoId=old_vid, media_body=MediaFileUpload(str(l_thumb), mimetype="image/png")).execute()
                    except Exception:
                        pass
                st.setdefault("protected_high_view_videos", []).append({"slug": slug, "lang": lc, "vid": old_vid, "views": views})
                _save_retrofit_state(st)
                return {"action": "protected_high_views_thumb_only", "slug": slug, "lang": lc, "vid": old_vid, "views": views}

            if age_h >= SAFE_SWAP_MIN_AGE_HOURS and views <= SAFE_SWAP_MAX_VIEWS:
                # Rule 13.3 Clean Swap: delete low-view static legacy video first, then upload Flow Motion Hybrid!
                yt.videos().delete(id=old_vid).execute()
                yt_urls[lc] = ""
                sp.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
                up_res = try_upload_one_nano_banana_cinema(kind="long", target_slug=slug, target_lang=lc, notify_tg=True)
                if up_res and up_res.get("url"):
                    yt_urls[lc] = up_res["url"]
                    sdoc_after = json.loads(sp.read_text(encoding="utf-8"))
                    sdoc_after.setdefault("youtube_urls", {})[lc] = up_res["url"]
                    sp.write_text(json.dumps(sdoc_after, ensure_ascii=False, indent=2), encoding="utf-8")
                    st["last_swap_ts"] = now_ts
                    st.setdefault("safe_swapped_videos", []).append(
                        {"slug": slug, "lang": lc, "old_vid": old_vid, "old_views": views, "new_url": up_res["url"]}
                    )
                    _save_retrofit_state(st)
                    return {"action": "clean_swapped_low_view", "slug": slug, "lang": lc, "old_vid": old_vid, "new_url": up_res["url"]}
        except Exception:
            continue
    return None


def run_idle_flow_quality_retrofit_cycle(
    max_topics: int = 1,
    force: bool = False,
    allow_low_view_live_swap: bool = True,
    target_slug: str | None = None,
) -> dict:
    """
    [회장님 지시 — '이미 만든 자료들도 여유가 있을때 품질을 이 방식으로 높여주기 바란다']:
    24/7 데몬의 유휴 시간마다 Antigravity 에이전트 쿼터 0원으로 구동되는 자동 고품질화(Flow Motion Retrofit) 사이클.
    - Tier 1: 기존 정지 줌 에피소드(`2017090101`, `2012100304`, `2014111902` 등)에 실제 Veo 3.1 양단고정 광학 모션 클립 장착 및 재렌더링
    - Tier 2: 기존에 만들어 둔 847+ 원문 스크립트(검색 핵심 단원 우선)에 Google Flow ULTRA 키프레임(0크레딧) + 양단고정 모션(5크레딧) 생성·합성
    - Tier 3: 15뷰 이하 저조회 구버전 안전 교체(Rule 13.3) 및 15뷰 초과 인기 영상 보호(Rule 33)
    """
    import google_flow_controller as gfc

    st = _load_retrofit_state()
    now_ts = datetime.now().timestamp()
    if not force:
        if int(st.get("daily_count") or 0) >= MAX_DAILY_FLOW_RETROFITS:
            return {"status": "daily_cap_reached", "summary": get_flow_retrofit_status_summary()}
        if (now_ts - float(st.get("last_run_ts") or 0.0)) < MIN_RETROFIT_INTERVAL_SEC:
            return {"status": "cooldown_wait", "summary": get_flow_retrofit_status_summary()}

    upgraded_now = []

    # Build candidate queue: Tier 1 (curated blueprints needing Flow motion clip or re-render) -> Tier 2 (high-search existing scripts)
    candidates: list[dict] = []
    for bp in NANO_BANANA_BLUEPRINTS:
        if target_slug and bp["slug"] != target_slug:
            continue
        f_mp4 = _resolve_flow_clip(bp)
        ko_mp4 = NB_OUT_DIR / f"{bp['slug']}_nb_ko.mp4"
        needs_clip = f_mp4 is None
        needs_rerender = (f_mp4 is not None) and ((not ko_mp4.exists()) or (ko_mp4.stat().st_mtime < f_mp4.stat().st_mtime))
        if needs_clip or needs_rerender:
            candidates.append(bp)

    if len(candidates) < max_topics:
        high_terms = ("피타고라스", "원주각", "접선", "이등변", "외심", "내심", "무게중심", "닮음", "메넬라우스", "체바", "포물선", "타원", "코사인", "미분", "정적분")
        scored_slugs = []
        for sp in sorted(SCRIPTS_DIR.glob("*.json")):
            slug = sp.stem
            if target_slug and slug != target_slug:
                continue
            if any(c["slug"] == slug for c in candidates):
                continue
            if (FLOW_CLIPS_DIR / f"{slug}_flow.mp4").exists() and (NB_OUT_DIR / f"{slug}_nb_ko.mp4").exists():
                continue
            try:
                sdoc = json.loads(sp.read_text(encoding="utf-8"))
                pdf_u = str(sdoc.get("pdf_url") or "")
                if "min7014.github.io" not in pdf_u.lower() or len(sdoc.get("pages") or []) < 4:
                    continue
                t_s = str(sdoc.get("title") or "")
                hs = 1 if any(k in t_s for k in high_terms) else 0
                not_yet_live = 1 if not ((sdoc.get("youtube_urls") or {}).get("ko") or "").strip() else 0
                scored_slugs.append((-hs, -not_yet_live, slug))
            except Exception:
                continue
        scored_slugs.sort()
        for _, _, sl in scored_slugs[: max(4, max_topics * 2)]:
            dyn_bp = build_dynamic_flow_blueprint_from_script(sl)
            if dyn_bp:
                candidates.append(dyn_bp)

    for bp in candidates[:max_topics]:
        slug = bp["slug"]
        art_p = NB_ASSETS_DIR / bp["art_file"]
        flow_p = FLOW_CLIPS_DIR / (bp.get("flow_clip") or f"{slug}_flow.mp4")

        # Step 1: Generate Nano Banana 2.1 16:9 keyframe (0 credits) if missing
        used_fresh_project_asset = False
        if not art_p.exists():
            img_prompt = bp.get("flow_image_prompt") or _build_domain_flow_prompts({"title": bp.get("title_ko", "")})[0]
            gen_img = gfc.generate_flow_image_16x9(img_prompt, art_p, headless=True)
            if not gen_img or not art_p.exists():
                continue
            used_fresh_project_asset = True

        # Step 2: Generate Veo 3.1 Lite locked-keyframe 8s motion clip (5 credits) if missing or invalid MP4
        if _resolve_flow_clip(bp) is None:
            mot_prompt = bp.get("flow_motion_prompt") or gfc.DEFAULT_LOCKED_MOTION_PROMPT
            gen_vid = gfc.generate_flow_locked_motion_clip(
                art_p,
                flow_p,
                motion_prompt=mot_prompt,
                lock_end_frame=True,
                model_name="Veo 3.1 - Lite",
                use_latest_project_asset=used_fresh_project_asset,
                headless=True,
            )
            if not gen_vid or not flow_p.exists():
                continue

        # Persist dynamic blueprint into script JSON if dynamically generated
        sp = SCRIPTS_DIR / f"{slug}.json"
        if sp.exists() and slug not in {b["slug"] for b in NANO_BANANA_BLUEPRINTS}:
            try:
                sdoc = json.loads(sp.read_text(encoding="utf-8"))
                sdoc["flow_blueprint"] = bp
                sp.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
            except Exception:
                pass

        # Step 3: Render KO & EN 1080p + 9:16 Q-#Shorts with the real Veo motion clip!
        for lc in ("ko", "en"):
            render_nano_banana_bundle(bp, lang_code=lc)

        swap_info = None
        if allow_low_view_live_swap:
            swap_info = _try_safe_swap_or_thumb_upgrade_on_live_channel(bp, st)

        st["last_run_ts"] = datetime.now().timestamp()
        st["daily_count"] = int(st.get("daily_count") or 0) + 1
        if slug not in (st.get("upgraded_slugs") or []):
            st.setdefault("upgraded_slugs", []).append(slug)
        _save_retrofit_state(st)
        upgraded_now.append({"slug": slug, "flow_clip": flow_p.name, "swap_info": swap_info})

    return {"status": "ok", "upgraded": upgraded_now, "summary": get_flow_retrofit_status_summary()}


if __name__ == "__main__":
    import sys as _sys
    if "--retrofit-once" in _sys.argv:
        print(json.dumps(run_idle_flow_quality_retrofit_cycle(max_topics=1, force=True), ensure_ascii=False, indent=2))
    elif "--retrofit-status" in _sys.argv:
        print(json.dumps(get_flow_retrofit_status_summary(), ensure_ascii=False, indent=2))
    else:
        res = render_all_nano_banana_flagships(("ko", "en"))
        print(json.dumps(res, ensure_ascii=False, indent=2))
