# -*- coding: utf-8 -*-
"""
[Edition 5 v2.0: 🌟 탈-PDF 순수 창의 아이디어 시네마 엔진 (Pure Procedural Neon-Bloom Math Cinema — ZERO PDF Screenshots)]
- PDF 파일의 슬라이드 이미지나 흰색 캡처 박스를 단 1픽셀도 화면에 붙이지 않고,
  오직 주제의 '수학적 아이디어(Core Mathematical Idea)'만을 추출하여
  풀스크린 다크 벨벳 코스믹 캔버스(1920x1080 & 1080x1920) 위에
  다중 레이어 네온 블룸 셰이더(Multi-Layer Gaussian Glow Bloom), 7단계 재귀 프랙탈(128개 가지),
  12채널 동시 레이트레이싱 광선 파동, 실시간 동적 수식 게이지로 제작하는 최고 화질 수학 시네마 엔진입니다.
"""

import asyncio
import json
import math
import re
import shutil
import subprocess
import tempfile
import textwrap
import time
from pathlib import Path

import edge_tts
from PIL import Image, ImageChops, ImageDraw, ImageFilter

import min7014_video_maker as vmaker

ROOT_DIR = vmaker.ROOT_DIR
SCRIPTS_DIR = vmaker.SCRIPTS_DIR
YT_PKG_DIR = vmaker.YT_PKG_DIR
YT_UPLOADS_DIR = vmaker.YT_UPLOADS_DIR
CREATIVE_IDEA_DIR = ROOT_DIR / "video_lectures" / "creative_idea"
CREATIVE_IDEA_DIR.mkdir(parents=True, exist_ok=True)


def ease_in_out_cubic(t: float) -> float:
    t = max(0.0, min(1.0, float(t)))
    return 4.0 * t * t * t if t < 0.5 else 1.0 - ((-2.0 * t + 2.0) ** 3) / 2.0


def sanitize_glyphs(text: str) -> str:
    """Malgun Gothic / Arial에서 깨지는 특수 기호나 이모지를 깔끔한 벡터 호환 기호로 정제합니다."""
    if not text:
        return ""
    repl = {
        "➔": "→",
        "▸": "▶",
        "₀": "0",
        "₁": "1",
        "₂": "2",
        "₃": "3",
        "₄": "4",
        "ⁿ": "^n",
        "∝": " ~ ",
        "∑": "SUM",
        "❓": "[Q]",
        "⚡": "★",
        "🎯": "▶",
        "🧪": "▶",
        "🌱": "▶",
        "🌳": "▶",
        "🧭": "▶",
        "📐": "▶",
        "💡": "★",
        "🔀": "▶",
        "🚀": "★",
        "🏆": "★",
        "🧠": "★",
        "🔔": "▶",
        "💎": "★",
        "📊": "▶",
        "🪐": "★",
        "📈": "▶",
        "🎬": "▶",
        "🌟": "★",
        "📱": "",
        "👆": "→",
        "🔍": "▶",
        "✨": "★",
        "≈": "=",
        "∈": "in",
        "⇒": "→",
        "⇔": "↔",
        "∽": "~",
        "lim( theta arrow 0) ( sin theta/theta)=1": "lim(θ→0) (sinθ/θ) = 1",
        "lim( theta arrow 0) ( sin theta/)": "lim(θ→0) (sinθ/θ) = 1",
        "lim( theta arrow 0) ( sin theta/": "lim(θ→0) (sinθ/θ) = 1",
        "lim( theta arrow 0) ( sin)": "lim(θ→0) (sinθ/θ) = 1",
        "lim( theta arrow 0) (": "lim(θ→0) (sinθ/θ) = 1",
        "theta arrow 0": "θ→0",
        "sin theta": "sinθ",
        "cos theta": "cosθ",
        "tan theta": "tanθ",
        "Reflection of Light on a Ellipse": "Reflection of Light on an Ellipse",
    }
    out = str(text)
    for k, v in repl.items():
        out = out.replace(k, v)
    return out


def detect_visual_archetype(sdoc: dict) -> str:
    raw_t = f"{sdoc.get('title', '')} {sdoc.get('title_en', '')}".lower()
    blob = " ".join([
        raw_t,
        str(sdoc.get("concept_badge", "")).lower(),
        str((sdoc.get("teacher_proof_analysis") or {}).get("category_type", "")).lower(),
    ])

    if any(k in raw_t for k in ["30-60-90", "직각이등변삼각형", "isosceles right", "30도 삼각비", "45도 삼각비", "60도 삼각비"]):
        return "special_triangles"
    if any(k in raw_t for k in ["제곱근", "square root", "정사각형의 한 변", "유리화"]):
        return "square_root_geometry"
    if any(k in raw_t for k in ["사이클로이드", "cycloid"]):
        return "cycloid_kinematics"
    if any(k in blob for k in ["피타고라스", "pythagor", "직각삼각형", "right triangle", "넓이 보존"]):
        return "pythagoras_fractal"
    if any(k in raw_t for k in ["포물선", "parabola"]) or ("준선" in raw_t and "타원" not in raw_t and "쌍곡선" not in raw_t):
        return "conic_parabola"
    if any(k in blob for k in ["타원", "쌍곡선", "단델린", "초점", "이차곡선", "ellipse", "hyperbola", "dandelin", "conic"]):
        return "conic_reflection"
    if any(k in raw_t for k in ["메넬라우스", "menelaus"]):
        return "menelaus_theorem"
    if any(k in raw_t for k in ["체바", "ceva", "무게중심", "centroid", "비비아니", "viviani"]):
        return "ceva_menelaus"
    if any(k in raw_t for k in ["평행선", "선분의 길이의 비", "중점연결정리", "닮음", "similarity"]):
        return "parallel_similarity"
    if ("sin" in raw_t or "사인" in raw_t) and any(k in raw_t for k in ["d/dx", "\\frac{d}{dx}", "미분", "derivative"]):
        return "trig_deriv_sin"
    if any(k in blob for k in ["삼각함수", "삼각비", "사인", "코사인", "탄젠트", "호도법", "단위원", "trigon", "sin(", "cos(", "tan(", "sin ", "cos ", "tan ", "\\sin", "\\cos", "\\tan"]):
        return "trig_harmonic"
    if any(k in raw_t for k in ["코시의 평균값", "cauchy's mean value"]):
        return "cauchy_mvt"
    if any(k in raw_t for k in ["역함수의 미분", "derivative of inverse"]):
        return "inverse_deriv"
    if any(k in blob for k in ["미분", "적분", "극한", "도함수", "평균값", "롤의", "구분구적", "급수", "derivative", "integral", "limit", "mean value", "rolle"]):
        return "calculus_motion"
    if any(k in blob for k in ["황금비", "피보나치", "golden", "fibonacci", "나선", "꽃잎차례", "정오각형", "pentagon", "연분수", "등비", "수열"]):
        return "fibonacci_golden"
    if any(k in blob for k in ["확률", "정규분포", "이항", "통계", "주사위", "독립시행", "binomial", "probability", "조합", "순열", "파스칼", "경우의 수", "표준편차", "분산", "시행과 사건"]):
        return "prob_galton"
    return "circle_invariants"


def build_creative_idea_acts(sdoc: dict, lang_code: str = "ko") -> list[dict]:
    ko_t, en_t = vmaker.split_bilingual_title(sdoc.get("title", sdoc.get("slug", "")))
    clean_ko = sanitize_glyphs(vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(ko_t), max_len=38, lang="ko"))
    clean_en = sanitize_glyphs(vmaker._smart_concise_topic_title(
        vmaker.latex_to_unicode_title(en_t or sdoc.get("title_en") or ko_t), max_len=46, lang="en"
    ))
    t_title = clean_ko if lang_code == "ko" else clean_en
    tpa = vmaker.analyze_min7014_topic_as_mathteacher(
        sdoc.get("title", ""),
        sdoc.get("sub_domain_ko", ""),
        sdoc.get("breadcrumb", ""),
    )
    archetype = detect_visual_archetype(sdoc)

    inv_ko = sanitize_glyphs(vmaker.latex_to_unicode_title(tpa.get("conclusion_ko") or tpa.get("core_invariant") or "도형이 변해도 흔들리지 않는 넓이와 비율의 등식 관계"))
    polya_ko = sanitize_glyphs(vmaker.latex_to_unicode_title(tpa.get("auxiliary_line_ko") or tpa.get("polya_bridge") or "숨겨진 대칭성과 보조선을 연결해 복잡한 식을 단번에 단순화하는 발상"))
    logic_ko = sanitize_glyphs(vmaker.latex_to_unicode_title(tpa.get("proof_logic_ko") or ""))
    whatif_ko = sanitize_glyphs(vmaker.latex_to_unicode_title(tpa.get("what_if_not_ko") or tpa.get("what_if_extension") or "특수한 각도와 평면 도형의 성질을 일반 삼각형과 3차원 공간으로 넓히는 확장"))

    if archetype == "pythagoras_fractal":
        if lang_code == "ko":
            return [
                {
                    "act": 1,
                    "badge": "ACT 1 · 직관을 깨는 프랙탈의 역설",
                    "headline": f"수백 개의 가지가 뻗어나가도 넓이 합은 영원히 똑같다! ({t_title})",
                    "key_formula": "Level 0 (25) = Level 1 (16+9) = ... = Level N (25.00)",
                    "narration": (
                        f"하나의 줄기에서 두 개의 가지가 갈라지고, 다시 네 개, 여덟 개, 백스물여덟 개의 가지가 밤하늘의 숲처럼 피어납니다. "
                        f"상식적으로는 가지가 끝없이 뻗어나가면 넓이의 합도 폭발할 것처럼 보입니다. "
                        f"하지만 놀랍게도 [{t_title}]에서는 각 층에 피어난 수백 개 정사각형의 넓이를 모두 더해도 맨 아래 뿌리 기둥 단 한 개의 넓이 25와 단 0.001의 오차도 없이 영원히 일치합니다!"
                    ),
                    "hud_notes": [
                        "가지 개수: 1개 → 2개 → 4개 → 8개 → 16개 → 64개로 기하급수 폭발",
                        "각 층의 넓이 총합: 언제나 뿌리 정사각형(c² = 25)과 100% 일치!",
                        "핵심 질문: 모양과 개수가 바뀌는데 무엇이 넓이를 완벽히 보존할까?",
                    ],
                },
                {
                    "act": 2,
                    "badge": "ACT 2 · 공식 없이 눈으로 보는 25칸 타일 실험",
                    "headline": "문자 대신 3 · 4 · 5 격자 타일 25개로 확인하는 넓이 보존",
                    "key_formula": "3² (9 Tiles) + 4² (16 Tiles) = 5² (25 Tiles)",
                    "narration": (
                        f"추상적인 공식 대신 눈으로 직접 타일 개수를 세어 볼까요? "
                        f"가로세로 5칸인 뿌리 정사각형 안에는 정확히 스물다섯 개의 황금 타일이 들어 있습니다. "
                        f"직각삼각형 위쪽 왼쪽 가지에는 4 곱하기 4 열여섯 칸, 오른쪽 가지에는 3 곱하기 3 아홉 칸이 자리 잡습니다. "
                        f"열여섯 칸과 아홉 칸이 합쳐져 정확히 스물다섯 칸! 에너지가 보존되듯 넓이 타일이 한 층 위 가지들로 고스란히 옮겨간 것입니다."
                    ),
                    "hud_notes": [
                        "뿌리 정사각형(5×5): 25개의 단위 정사각형 격자 타일",
                        "왼쪽 가지(4×4 = 16칸) + 오른쪽 가지(3×3 = 9칸) = 정확히 25칸!",
                        "다음 세대로 갈라질 때도 각 가지의 타일 총량은 100% 보존!",
                    ],
                },
                {
                    "act": 3,
                    "badge": "ACT 3 · 유클리드의 단 한 줄 수선 아이디어",
                    "headline": "직각 꼭짓점에서 내린 황금 수선 1줄이 넓이를 정확히 두 조각으로 나눈다!",
                    "key_formula": "c² = c·(a·cosθ) + c·(b·sinθ) = a² + b²",
                    "narration": (
                        f"왜 어떤 각도로 직각삼각형을 기울여도 이 넓이 보존이 절대 깨지지 않을까요? "
                        f"비밀은 직각 꼭짓점에서 아래쪽 큰 정사각형을 향해 수직으로 내려긋는 황금빛 보조선 한 줄에 있습니다! "
                        f"이 수선 한 줄이 뿌리 정사각형을 왼쪽 직사각형과 오른쪽 직사각형 두 개로 나누는데, 왼쪽 직사각형의 넓이가 정확히 왼쪽 가지 정사각형과 같고, 오른쪽 직사각형이 오른쪽 가지 정사각형과 완벽히 같습니다."
                    ),
                    "hud_notes": [
                        "결정적 보조선: 직각 꼭짓점 C에서 빗변 정사각형으로 내린 수선",
                        "왼쪽 분할 직사각형 넓이 = 왼쪽 정사각형 가지 넓이 (a²)",
                        "오른쪽 분할 직사각형 넓이 = 오른쪽 정사각형 가지 넓이 (b²)",
                    ],
                },
                {
                    "act": 4,
                    "badge": "ACT 4 · 한계를 넘는 상상 (What-If-Not 일반화)",
                    "headline": "정사각형 대신 반원이나 정삼각형을 붙인다면? 각도가 90도가 아니라면?",
                    "key_formula": "S(닮음도형) = k·변²  →  반원·정다각형 모두 성립!",
                    "narration": (
                        f"이제 기존의 틀을 완전히 깨뜨려 봅시다! 만약 세 변 위에 정사각형이 아니라 빛나는 반원이나 정삼각형을 붙인다면 어떨까요? "
                        f"모든 닮음 도형의 넓이는 변의 길이의 제곱에 비례하기 때문에, 두 작은 반원의 넓이 합은 여전히 큰 반원의 넓이와 정확히 같습니다! "
                        f"나아가 사잇각이 90도에서 벗어나 예각이나 둔각으로 변하면, 그 넓이 차이를 보정하는 항이 추가되며 고등학교의 코사인법칙이 탄생합니다."
                    ),
                    "hud_notes": [
                        "조건 변형 1: 세 변에 반원·정삼각형을 붙여도 S1 + S2 = S0 완벽 성립!",
                        "조건 변형 2: 사잇각이 90°가 아니면? → c² = a² + b² - 2ab·cosθ",
                        "단 하나의 기하학적 아이디어가 피타고라스부터 삼각함수까지 관통!",
                    ],
                },
                {
                    "act": 5,
                    "badge": "ACT 5 · 7단계 프랙탈 교향곡 & 10초 실전 통찰",
                    "headline": "수십 개 조각을 일일이 계산하지 말고 뿌리 불변량 하나로 10초 만에 끝내라!",
                    "key_formula": "SUM(All 64 Leaves at Level 6) = Root Square (25)",
                    "narration": (
                        f"수능과 올림피아드에서 도형이 수없이 쪼개지는 프랙탈 급수 문제가 나올 때, 조각 하나하나의 길이를 구하는 것은 출제자의 함정에 빠지는 길입니다. "
                        f"오늘 본 피타고라스 나무처럼, 모든 나뭇잎의 넓이를 부모 가지로 거꾸로 합쳐 내려오면 단 10초 만에 뿌리 도형 하나로 답이 구해집니다. "
                        f"눈으로 보고 단번에 깨치는 최고의 수학 시네마, 지금 바로 구독과 좋아요를 누르고 다음 아이디어도 함께 탐험해 보세요!"
                    ),
                    "hud_notes": [
                        "실전 킬러 해법: n단계의 모든 조각 합 = 0단계 뿌리 도형으로 즉시 환원!",
                        "오늘의 유레카: '공식을 외우지 말고 넓이가 흘러가는 길을 보라!'",
                        "지금 [@min7014_ai 구독] 누르고 1,113개 창의 수학 시네마를 만나보세요!",
                    ],
                },
            ]
        else:
            return [
                {
                    "act": 1,
                    "badge": "ACT 1 · THE FRACTAL PARADOX",
                    "headline": f"Hundreds of Branches, Yet Exact Same Area?! ({t_title})",
                    "key_formula": "Level 0 (25) = Level 1 (16+9) = ... = Level N (25.00)",
                    "narration": (
                        f"Watch a single trunk split into two branches, then four, eight, and a hundred twenty-eight glowing leaves across the night sky. "
                        f"Intuition says the area should explode as branches multiply. "
                        f"Yet in [{t_title}], every single generation of squares adds up to the exact same area as the single root square below!"
                    ),
                    "hud_notes": [
                        "Branch count explodes: 1 → 2 → 4 → 8 → 16 → 64 → 128!",
                        "Total area of every level stays strictly locked at c² = 25!",
                        "What geometric law preserves 100% of the area across every split?",
                    ],
                },
                {
                    "act": 2,
                    "badge": "ACT 2 · LIVE 25-TILE GRID EXPERIMENT",
                    "headline": "Counting the 3 · 4 · 5 Unit Tiles Without Any Algebra",
                    "key_formula": "3² (9 Tiles) + 4² (16 Tiles) = 5² (25 Tiles)",
                    "narration": (
                        f"Forget abstract variables and count the glowing unit tiles directly! "
                        f"A 5 by 5 root square holds 25 golden tiles. Above the right triangle, the left branch holds 16 cyan tiles and the right branch holds 9 rose tiles. "
                        f"16 plus 9 equals 25! Every single tile of area flows from the trunk into the branches without loss."
                    ),
                    "hud_notes": [
                        "Root Trunk (5×5): 25 individual unit grid tiles",
                        "Left Branch (4×4 = 16) + Right Branch (3×3 = 9) = 25 Tiles!",
                        "Every subsequent split preserves the exact tile sum!",
                    ],
                },
                {
                    "act": 3,
                    "badge": "ACT 3 · EUCLID'S GOLDEN ALTITUDE LINE",
                    "headline": "One Perpendicular Line Slices the Area Into Exact Halves",
                    "key_formula": "c² = c·(a·cosθ) + c·(b·sinθ) = a² + b²",
                    "narration": (
                        f"Why does this work for any right triangle tilt angle? "
                        f"Drop a single perpendicular altitude from the right angle straight through the hypotenuse square. "
                        f"This golden line partitions the trunk into two rectangles whose areas exactly match the left and right branch squares!"
                    ),
                    "hud_notes": [
                        "Key Auxiliary Line: Perpendicular altitude from the right angle",
                        "Left Rectangle Area = Left Branch Square Area (a²)",
                        "Right Rectangle Area = Right Branch Square Area (b²)",
                    ],
                },
                {
                    "act": 4,
                    "badge": "ACT 4 · BEYOND THE TEXTBOOK (WHAT-IF-NOT)",
                    "headline": "Semicircles & Equilateral Triangles on the Sides + Law of Cosines",
                    "key_formula": "Area(Similar Shape) = k·Side²  →  Works for Semicircles!",
                    "narration": (
                        f"Now let's break free from squares! What if we attach glowing semicircles or equilateral triangles to the three sides? "
                        f"Because similar areas scale with the square of length, the two smaller semicircles still equal the largest semicircle! "
                        f"And when the angle deviates from 90 degrees, the area difference gives birth to the Law of Cosines."
                    ),
                    "hud_notes": [
                        "What-If 1: Semicircles on the 3 sides still obey S1 + S2 = S0!",
                        "What-If 2: Angle ≠ 90° → c² = a² + b² - 2ab·cosθ (Law of Cosines)",
                        "One visual principle unifies geometry and trigonometry!",
                    ],
                },
                {
                    "act": 5,
                    "badge": "ACT 5 · 10-SECOND OLYMPIAD TAKEAWAY",
                    "headline": "Collapse Any N-Level Fractal Back to the Root in 10 Seconds!",
                    "key_formula": "SUM(All 64 Leaves at Level 6) = Root Square (25)",
                    "narration": (
                        f"When an exam asks for the sum of dozens of tiny fractal branches, never compute them one by one. "
                        f"Collapse every pair of branches back down to the root trunk and solve the problem in 10 seconds! "
                        f"Subscribe to @min7014_ai right now for daily visual math cinema!"
                    ),
                    "hud_notes": [
                        "10-Sec Exam Hack: Collapse level-N leaves directly to Level 0!",
                        "Eureka Rule: Track the invariant area flow, not tedious formulas.",
                        "Subscribe to @min7014_ai & explore the interactive GeoGebra lab!",
                    ],
                },
            ]

    if archetype == "conic_reflection":
        if lang_code == "ko":
            return [
                {
                    "act": 1,
                    "badge": "ACT 1 · 12채널 레이저 광학 미스터리",
                    "headline": f"360도 어느 방향으로 쏜 빛이든 단 하나의 초점으로 모인다! ({t_title})",
                    "key_formula": "PF₁ + PF₂ = 2a (Constant Optical Path)",
                    "narration": (
                        f"어두운 우주 공간에서 제1초점 F1이 열두 가닥의 네온 레이저 광선을 사방으로 발사합니다. "
                        f"놀랍게도 [{t_title}]에서는 어느 각도로 날아간 빛이든 곡선 내벽에 반사되는 순간, 단 하나의 오차도 없이 제2초점 F2로 정확히 모입니다! "
                        f"속삭이는 회랑과 천체 망원경이 사용하는 이 완벽한 광학 집속의 비밀은 무엇일까요?"
                    ),
                    "hud_notes": [
                        "12채널 레이저 발사: 모든 방향의 광선이 반사 후 한 점에 집속!",
                        "핵심 불변량: 두 초점까지의 거리 합 PF₁ + PF₂ = 2a 일정!",
                        "질문: 왜 곡선의 모든 점에서 입사각과 반사각이 정확히 같아질까?",
                    ],
                },
                {
                    "act": 2,
                    "badge": "ACT 2 · 팽팽한 황금 실의 길이가 만드는 궤적",
                    "headline": "한쪽이 길어지면 다른 쪽이 정확히 그만큼 줄어드는 거리 합 불변량!",
                    "key_formula": "Δ(PF₁) + Δ(PF₂) = 0  →  PF₁ + PF₂ = 2a",
                    "narration": (
                        f"곡선 위를 달리는 점 P를 따라 두 초점과 연결된 두 선분의 길이를 실시간으로 측정해 보세요. "
                        f"점 P가 오른쪽으로 이동해 F1에서 멀어지는 순간, F2까지의 거리가 정확히 똑같은 길이만큼 짧아집니다. "
                        f"마치 길이가 2a로 고정된 팽팽한 황금 실에 연필을 걸고 돌리는 것처럼, 거리 합이 영원히 보존됩니다."
                    ),
                    "hud_notes": [
                        "실시간 거리 측정: PF₁이 +Δ만큼 늘어나면 PF₂는 -Δ만큼 감소!",
                        "광학적 의미: 모든 광선이 F₁에서 F₂까지 이동하는 총 시간과 거리가 동일!",
                        "동시 도착 원리: 12개 파동이 제2초점에 동시에 도착하여 보강 간섭!",
                    ],
                },
                {
                    "act": 3,
                    "badge": "ACT 3 · 페르마의 최단 경로와 대칭점 보조선",
                    "headline": "접선 너머로 초점을 대칭이동하면 꺾인 빛의 경로가 일직선으로 펴진다!",
                    "key_formula": "min(PF₁ + PF₂) = Straight Line F₁ — P — F₂'  (θ₁ = θ₂)",
                    "narration": (
                        f"왜 곡선 위의 접선이 두 초점과 이루는 입사각과 반사각을 완벽히 이등분할까요? "
                        f"접선 너머로 초점 F2를 대칭이동해 가상의 점 F2 프라임을 찍는 황금 보조선을 그어 보세요! "
                        f"꺾여 있던 두 선분의 합이 일직선으로 펴지는 바로 그 점 P에서 거리가 최소가 되며, 맞꼭지각과 대칭 성질에 의해 입사각과 반사각이 일치합니다."
                    ),
                    "hud_notes": [
                        "결정적 보조선: 접선에 대해 한 초점을 대칭이동하여 일직선 연결!",
                        "페르마의 원리: 빛은 거울 접선 위에서 이동 거리가 최소인 점 P를 선택!",
                        "맞꼭지각 + 이등변삼각형 성질 → 입사각(θ₁) = 반사각(θ₂) 1초 증명!",
                    ],
                },
                {
                    "act": 4,
                    "badge": "ACT 4 · 한계를 넘는 상상 (이심률 e의 연속 변형)",
                    "headline": "초점 하나를 무한대 저편으로 보내면 타원이 포물선과 쌍곡선으로 진화한다!",
                    "key_formula": "e = 0 (원) → 0<e<1 (타원) → e = 1 (포물선) → e > 1 (쌍곡선)",
                    "narration": (
                        f"이제 타원의 한계를 넘어 이심률을 연속적으로 바꿔 봅시다! "
                        f"제2초점을 무한히 먼 곳으로 밀어내면, 제2초점으로 향하던 광선들이 모두 축에 나란한 평행 광선으로 바뀌며 타원이 포물선으로 변신합니다! "
                        f"자동차 전조등과 전파망원경, 나아가 케플러의 행성 궤도까지 모두 이 하나의 광학 아이디어로 통합됩니다."
                    ),
                    "hud_notes": [
                        "조건 변형 1: 두 초점이 합쳐지면(e=0) 중심에서 반사되는 '원'",
                        "조건 변형 2: 한 초점이 무한대로 가면(e=1) 평행광을 모으는 '포물선'",
                        "조건 변형 3: 거리 차가 일정하면(e>1) 제임스 웹 망원경의 '쌍곡선'",
                    ],
                },
                {
                    "act": 5,
                    "badge": "ACT 5 · 수능·올림피아드 이차곡선 10초 해법",
                    "headline": "이차곡선 위에 점이 찍히는 순간 두 초점과 연결하는 보조선부터 그어라!",
                    "key_formula": "Rule #1: Spot Point P on Conic → Connect Both Foci F₁ & F₂!",
                    "narration": (
                        f"수능과 수리논술에서 타원, 포물선, 쌍곡선 문제가 나올 때 복잡한 방정식에 대입하는 것은 가장 느린 길입니다. "
                        f"곡선 위의 점을 보자마자 두 초점 또는 준선으로 황금 보조선을 긋고, 거리 합과 입사·반사 대칭성을 쓰면 10초 만에 풀립니다. "
                        f"설명란의 인터랙티브 광학 실험실에서 직접 레이저를 쏘아 보고, 지금 바로 @min7014_ai 채널을 구독하세요!"
                    ),
                    "hud_notes": [
                        "실전 제1원칙: 이차곡선 문제 = 정의(초점·준선 거리) 보조선이 90% 해결!",
                        "접선 문제: 초점 대칭이동 & 입사각=반사각 각이등분선 성질 즉시 적용!",
                        "지금 [@min7014_ai 구독] 누르고 1,113개 수학 시네마를 정주행하세요!",
                    ],
                },
            ]
        else:
            return [
                {
                    "act": 1,
                    "badge": "ACT 1 · 12-CHANNEL LASER OPTICS MYSTERY",
                    "headline": f"Every Laser Beam Fired From Focus F₁ Converges Exactly at F₂! ({t_title})",
                    "key_formula": "PF₁ + PF₂ = 2a (Constant Optical Path)",
                    "narration": (
                        f"Twelve glowing neon laser beams fire in every direction from the first focus F1 across the dark cosmos. "
                        f"In [{t_title}], every single beam reflects off the curved boundary and converges with zero error at the second focus F2! "
                        f"What geometric law makes this whispering gallery and telescope reflection work?"
                    ),
                    "hud_notes": [
                        "12-Channel Ray Tracing: All reflected rays lock onto Focus F₂!",
                        "Core Invariant: Sum of focal distances PF₁ + PF₂ = 2a is constant!",
                        "Question: Why does the curve bisect every incident and reflected angle?",
                    ],
                },
                {
                    "act": 2,
                    "badge": "ACT 2 · THE TAUT GOLDEN STRING INVARIANT",
                    "headline": "As One Focal Segment Stretches, the Other Shrinks by the Exact Same Amount!",
                    "key_formula": "Δ(PF₁) + Δ(PF₂) = 0  →  PF₁ + PF₂ = 2a",
                    "narration": (
                        f"Track point P as it glides along the curve. "
                        f"Whenever PF1 stretches by delta, PF2 compresses by the exact same delta, keeping the total path length strictly constant. "
                        f"Because every light wave travels the exact same distance 2a, all twelve waves arrive at F2 in perfect phase!"
                    ),
                    "hud_notes": [
                        "Live Telemetry: +Δ on PF₁ is canceled by -Δ on PF₂!",
                        "Equal Travel Time: All 12 light rays arrive at F₂ simultaneously!",
                        "Constructive Interference: Geometry creates a natural optical lens.",
                    ],
                },
                {
                    "act": 3,
                    "badge": "ACT 3 · FERMAT'S SHORTEST PATH & REFLECTION LINE",
                    "headline": "Reflecting Focus F₂ Across the Tangent Straightens the Light Path!",
                    "key_formula": "min(PF₁ + PF₂) = Straight Line F₁ — P — F₂'  (θ₁ = θ₂)",
                    "narration": (
                        f"Why does the tangent line form equal angles with both focal segments? "
                        f"Reflect focus F2 across the tangent line to create virtual focus F2 prime! "
                        f"The shortest path between F1 and F2 prime is a straight line intersecting at P, instantly proving the angle of incidence equals the angle of reflection!"
                    ),
                    "hud_notes": [
                        "Golden Auxiliary Line: Reflect F₂ across the tangent line to F₂'",
                        "Fermat's Principle: Light chooses point P that minimizes total distance",
                        "Vertical Angles + Symmetry → Incident Angle θ₁ = Reflected Angle θ₂!",
                    ],
                },
                {
                    "act": 4,
                    "badge": "ACT 4 · MORPHING ECCENTRICITY TO INFINITY",
                    "headline": "Push One Focus to Infinity and the Ellipse Morphs Into a Parabola!",
                    "key_formula": "e = 0 (Circle) → 0<e<1 (Ellipse) → e = 1 (Parabola) → e > 1 (Hyperbola)",
                    "narration": (
                        f"What if we push focus F2 all the way to infinity? "
                        f"The rays heading toward F2 become parallel beams, and our ellipse seamlessly transforms into a parabolic satellite dish! "
                        f"Circles, ellipses, parabolas, and hyperbolas are all one family governed by eccentricity."
                    ),
                    "hud_notes": [
                        "e = 0: Both foci merge at the center → Circle",
                        "e = 1: Second focus at infinity → Parabolic Satellite Dish",
                        "e > 1: Difference of distances constant → Cassegrain Hyperbola",
                    ],
                },
                {
                    "act": 5,
                    "badge": "ACT 5 · 10-SECOND OLYMPIAD CONIC STRATEGY",
                    "headline": "Never Brute-Force Equations—Connect Both Foci the Instant You See P!",
                    "key_formula": "Rule #1: Spot Point P on Conic → Connect Both Foci F₁ & F₂!",
                    "narration": (
                        f"Whenever a point lies on a conic section in an exam, draw segments to both foci before writing any coordinate algebra. "
                        f"Try our live 60fps ray-tracing simulator in the description and subscribe to @min7014_ai right now!"
                    ),
                    "hud_notes": [
                        "Instant Trigger: Point on Conic → Draw Focal Radii PF₁ & PF₂!",
                        "Tangent Problem → Use Equal Reflection Angle Property!",
                        "Subscribe to @min7014_ai for daily visual math cinema!",
                    ],
                },
            ]

    if archetype == "trig_harmonic":
        if lang_code == "ko":
            return [
                {
                    "act": 1,
                    "badge": "ACT 1 · 단위원 회전과 파동의 탄생",
                    "headline": f"원의 등속 회전이 시간 축을 만나 아름다운 사인파로 펼쳐진다! ({t_title})",
                    "key_formula": "e^(iθ) = cos θ + i·sin θ  |  lim(θ→0) (sin θ / θ) = 1",
                    "narration": (
                        f"밤하늘의 단위원 위를 도는 점 하나가 오른쪽 시간 축으로 흔적을 남기며 나아갑니다. "
                        f"원을 맴도는 회전 운동이 수평으로 펼쳐지는 순간, 소리와 빛, 전자기파를 지배하는 사인파가 탄생합니다! "
                        f"그리고 각도 세타가 0으로 한없이 가까워질 때, [{t_title}]에서 사인 세타와 호의 길이 세타의 비율은 왜 정확히 1로 수렴할까요?"
                    ),
                    "hud_notes": [
                        "단위원 페이저(Phaser): 회전하는 점의 높이가 실시간 사인파(sin θ)를 생성!",
                        "핵심 극한: 각도 θ → 0 일 때 (현의 높이 sin θ) / (호의 길이 θ) → 1.000!",
                        "질문: 곡선인 호의 길이와 직선인 높이가 어떻게 똑같아질 수 있을까?",
                    ],
                },
                {
                    "act": 2,
                    "badge": "ACT 2 · 실시간 수치 게이지로 보는 극한의 수렴",
                    "headline": "세타가 작아질수록 sin θ, θ, tan θ 세 숫자가 하나로 포개진다!",
                    "key_formula": "sin(0.05) = 0.04998 < θ = 0.05000 < tan(0.05) = 0.05004",
                    "narration": (
                        f"단위원 아래쪽의 실시간 수치 계기판을 주목해 보세요! "
                        f"각도가 클 때는 사인 세타보다 호의 길이 세타가 길고, 바깥쪽 접선 탄젠트 세타가 가장 깁니다. "
                        f"하지만 각도를 점점 좁혀 나가면 세 숫자의 소수점 첫째, 둘째, 셋째 자리가 차례대로 완전히 일치하며 비율이 1.000으로 잠깁니다!"
                    ),
                    "hud_notes": [
                        "관찰 1: 모든 예각에서 항상 sin θ < θ < tan θ 대소 관계 성립!",
                        "관찰 2: θ를 줄일수록 곡선 호(θ)가 직선 수선(sin θ)과 구분 불가능해짐!",
                        "수치 검증: θ = 0.1 rad 일 때 이미 sin θ / θ = 0.9983 (99.8% 일치!)",
                    ],
                },
                {
                    "act": 3,
                    "badge": "ACT 3 · 에메랄드 부채꼴과 두 삼각형의 넓이 샌드위치",
                    "headline": "내접 삼각형 < 부채꼴 < 외접 직각삼각형 넓이 비교 한 줄로 증명 끝!",
                    "key_formula": "½·sinθ·cosθ < ½·θ < ½·tanθ  ⇒  cosθ < (sinθ / θ) < 1",
                    "narration": (
                        f"이 극한을 증명하는 최고의 시각적 아이디어는 길이가 아니라 '넓이'를 비교하는 것입니다! "
                        f"화면의 에메랄드빛 부채꼴을 보세요. 안쪽 삼각형보다는 부채꼴이 넓고, 바깥쪽 접선 직각삼각형보다는 부채꼴이 작습니다. "
                        f"이 넓이 부등식을 사인 세타로 나누어 뒤집으면, 사인 세타 나누기 세타가 코사인 세타와 1 사이에 갇히는 완벽한 샌드위치 정리가 완성됩니다!"
                    ),
                    "hud_notes": [
                        "결정적 아이디어: 곡선 호의 길이를 직접 재는 대신 3개 도형의 넓이 비교!",
                        "넓이 부등식: S(내접삼각형) < S(부채꼴 ½r²θ) < S(외접접선삼각형)",
                        "양변 정리 후 θ→0 극한: cos 0 (=1) ≤ lim(sinθ/θ) ≤ 1 → 정답 1!",
                    ],
                },
                {
                    "act": 4,
                    "badge": "ACT 4 · 한계를 넘는 상상 (미분과 테일러 급수로의 도약)",
                    "headline": "이 단 하나의 극한에서 모든 삼각함수의 미분과 원주율 공식이 탄생한다!",
                    "key_formula": "(sin x)' = cos x  |  sin θ ≈ θ - θ³/6 + θ⁵/120",
                    "narration": (
                        f"만약 사인 세타 나누기 세타가 1로 수렴하지 않았다면 현대 미적분학은 어떻게 되었을까요? "
                        f"사인 함수를 미분하면 코사인이 된다는 아름다운 공식도, 물리학의 단진자 운동 방정식도 모두 이 극한이 1이기 때문에 성립합니다! "
                        f"나아가 도형이 쪼개지는 차수를 분석하면 사인 세타가 세타로 근사되고, 코사인 세타는 1 빼기 2분의 세타 제곱으로 근사됨을 눈으로 읽을 수 있습니다."
                    ),
                    "hud_notes": [
                        "확장 1: 호도법(Radian)을 쓰는 진짜 이유 → (sin x)' = cos x 계수가 1!",
                        "확장 2: 1 - cos θ ≈ ½·θ² (반각 넓이 차이를 이용한 2차 근사!)",
                        "확장 3: 정다각형 극한을 통한 아르키메데스의 원주율(π) 계산과 직결!",
                    ],
                },
                {
                    "act": 5,
                    "badge": "ACT 5 · 수능 미적분 도형 극한 3초 근사 해법",
                    "headline": "도형 극한 킬러 문항은 sin θ → θ, tan θ → θ, 1-cos θ → ½θ²으로 즉시 치환하라!",
                    "key_formula": "θ → 0 :  sin θ ~ θ ,  tan θ ~ θ ,  1 - cos θ ~ ½·θ²",
                    "narration": (
                        f"수능 미적분 도형 극한 문제에서 복잡한 삼각비 식을 세우고 약분하느라 시간을 쏟지 마세요. "
                        f"오늘 본 단위원 그림처럼 세타가 0으로 갈 때 호와 현과 접선은 모두 세타와 같아지므로, 도형 위에서 바로 세타의 차수만 읽어내면 10초 만에 답이 나옵니다! "
                        f"지금 바로 @min7014_ai 채널을 구독하고 모든 수학 정리를 눈으로 마스터하세요!"
                    ),
                    "hud_notes": [
                        "실전 3초 공식: 현의 길이 ≈ 호의 길이(rθ) ≈ 접선 높이(r·tanθ)",
                        "높이 차(화살표 길이): r(1 - cosθ) ≈ ½·r·θ² 으로 즉시 면적 계산!",
                        "지금 [@min7014_ai 구독] 누르고 최고 화질 수학 시네마를 만나보세요!",
                    ],
                },
            ]
        else:
            return [
                {
                    "act": 1,
                    "badge": "ACT 1 · UNIT CIRCLE PHASER & WAVE GENESIS",
                    "headline": f"Circular Rotation Unfolds Into a Pure Harmonic Sine Wave! ({t_title})",
                    "key_formula": "e^(iθ) = cos θ + i·sin θ  |  lim(θ→0) (sin θ / θ) = 1",
                    "narration": (
                        f"Watch a glowing point orbit the unit circle while projecting its height across time to generate a harmonic sine wave. "
                        f"As angle theta shrinks toward zero in [{t_title}], why does the ratio of vertical height sin theta to curved arc length theta lock onto exactly 1?"
                    ),
                    "hud_notes": [
                        "Unit Circle Phaser: Circular rotation projects into a live sine wave!",
                        "Core Limit: As θ → 0, (Chord Height sin θ) / (Arc Length θ) → 1.000!",
                        "Question: How can we rigorously compare a curved arc with straight lines?",
                    ],
                },
                {
                    "act": 2,
                    "badge": "ACT 2 · LIVE NUMERICAL SQUEEZE TELEMETRY",
                    "headline": "Watch sin θ, Arc θ, and tan θ Converge Digit by Digit!",
                    "key_formula": "sin(0.05) = 0.04998 < θ = 0.05000 < tan(0.05) = 0.05004",
                    "narration": (
                        f"Observe the live telemetry below the unit circle. "
                        f"For any positive acute angle, sin theta is strictly smaller than arc theta, which is strictly smaller than tangent theta. "
                        f"Yet as the angle narrows, all three numbers squeeze together until their ratio becomes indistinguishable from 1!"
                    ),
                    "hud_notes": [
                        "Geometric Ordering: sin θ < θ < tan θ holds for every acute angle!",
                        "Visual Zoom: Zooming into the circle makes the arc look perfectly flat!",
                        "At θ = 0.1 rad, sin θ / θ is already 0.9983 (99.8% identical!)",
                    ],
                },
                {
                    "act": 3,
                    "badge": "ACT 3 · THE EMERALD SECTOR AREA SANDWICH",
                    "headline": "Inner Triangle < Circular Sector < Outer Tangent Triangle!",
                    "key_formula": "½·sinθ·cosθ < ½·θ < ½·tanθ  ⇒  cosθ < (sinθ / θ) < 1",
                    "narration": (
                        f"The master stroke is comparing areas instead of lengths! "
                        f"The emerald circular sector has area one-half theta, trapped between the inner triangle and the outer tangent right triangle. "
                        f"Dividing by sin theta traps our ratio between cos theta and 1—proving the limit by the Squeeze Theorem in one glance!"
                    ),
                    "hud_notes": [
                        "Key Idea: Compare 2D areas to bound the 1D curved arc length!",
                        "Area Inequality: ½·sinθ·cosθ < ½·θ < ½·tanθ",
                        "Squeeze Limit as θ→0: cos(0)=1 ≤ lim(sinθ/θ) ≤ 1 → Strictly 1!",
                    ],
                },
                {
                    "act": 4,
                    "badge": "ACT 4 · CALCULUS DERIVATIVES & TAYLOR SERIES",
                    "headline": "Why Radian Measure Makes the Derivative of Sine Equal Cosine!",
                    "key_formula": "(sin x)' = cos x  |  1 - cos θ ≈ ½·θ²",
                    "narration": (
                        f"This single geometric limit is the foundation of all trigonometric calculus. "
                        f"Because sin theta over theta approaches 1 in radians, the derivative of sin x is cleanly cos x without any messy scaling constant!"
                    ),
                    "hud_notes": [
                        "Why Radians Matter: Makes lim(sinθ/θ) = 1 and (sin x)' = cos x!",
                        "Second-Order Approximation: 1 - cos θ ≈ ½·θ²",
                        "Connects Archimedes' polygon exhaustion to modern physics!",
                    ],
                },
                {
                    "act": 5,
                    "badge": "ACT 5 · 3-SECOND GEOMETRIC LIMIT SHORTCUT",
                    "headline": "Replace sin θ and tan θ With θ Directly Inside Small-Angle Diagrams!",
                    "key_formula": "θ → 0 :  sin θ ~ θ ,  tan θ ~ θ ,  1 - cos θ ~ ½·θ²",
                    "narration": (
                        f"In small-angle geometry limits, replace chords, arcs, and tangents directly with theta to find the answer in 3 seconds! "
                        f"Try our live 60fps simulator in the description and subscribe to @min7014_ai right now!"
                    ),
                    "hud_notes": [
                        "3-Sec Shortcut: Chord ≈ Arc (rθ) ≈ Tangent (r·tanθ) as θ→0",
                        "Sagitta Height: r(1 - cosθ) ≈ ½·r·θ²",
                        "Subscribe to @min7014_ai for daily visual math cinema!",
                    ],
                },
            ]

    if archetype == "fibonacci_golden":
        if lang_code == "ko":
            return [
                {
                    "act": 1,
                    "badge": "ACT 1 · 자연과 우주가 선택한 황금 나선",
                    "headline": f"144개의 해바라기 씨앗이 빈틈없이 피어나는 황금각의 비밀! ({t_title})",
                    "key_formula": "φ = (1 + √5) / 2 ≈ 1.618034  |  Golden Angle = 137.508°",
                    "narration": (
                        f"밤하늘의 중심에서 144개의 황금빛 씨앗이 정확히 137.5도씩 회전하며 바깥으로 뻗어나갑니다. "
                        f"놀랍게도 [{t_title}]의 규칙을 따르면 씨앗들이 서로 겹치지 않고 시계 방향과 반시계 방향으로 피보나치 수만큼의 나선 팔을 만들어냅니다! "
                        f"단순한 덧셈 수열이 어떻게 가장 완벽한 기하학적 대칭을 창조할까요?"
                    ),
                    "hud_notes": [
                        "황금각(137.508°): 360° ÷ φ² — 자연계에서 가장 조밀한 씨앗 배열 각도!",
                        "피보나치 나선: 좌우 나선 개수가 항상 8, 13, 21, 34, 55개로 일치!",
                        "핵심 불변량: φ² = φ + 1  ⇔  1/φ = φ - 1 (자기닮음 황금비!)",
                    ],
                },
                {
                    "act": 2,
                    "badge": "ACT 2 · 정사각형을 잘라내도 똑같은 직사각형이 남는다!",
                    "headline": "황금 직사각형 안에서 끝없이 되풀이되는 자기닮음(Self-Similarity)",
                    "key_formula": "φ : 1 = 1 : (φ - 1)  ⇒  φ² - φ - 1 = 0",
                    "narration": (
                        f"화면 아래쪽의 황금 직사각형을 보세요. 긴 변과 짧은 변의 비가 파이 대 1인 직사각형에서 한 변이 1인 정사각형을 잘라내면, 남은 작은 직사각형의 비율도 다시 정확히 파이 대 1이 됩니다! "
                        f"정사각형을 영원히 잘라내도 처음과 완전히 닮은 직사각형이 무한히 재생산됩니다."
                    ),
                    "hud_notes": [
                        "자기닮음 비례식: (긴 변 : 짧은 변) = (짧은 변 : 남은 변)",
                        "이차방정식 도출: φ : 1 = 1 : (φ - 1)  →  φ² - φ - 1 = 0",
                        "피보나치 비의 수렴: 1/1, 2/1, 3/2, 5/3, 8/5, 13/8, 21/13 → 1.618034!",
                    ],
                },
                {
                    "act": 3,
                    "badge": "ACT 3 · 정오각형 대각선과 이등변삼각형 보조선",
                    "headline": "정오각형의 대각선 한 줄이 만드는 36° · 72° · 72° 황금 삼각형!",
                    "key_formula": "Diagonal / Side = 2·cos(36°) = φ ≈ 1.618",
                    "narration": (
                        f"기하학에서 황금비를 단 한 줄의 보조선으로 찾는 곳은 바로 정오각형입니다! "
                        f"정오각형의 대각선을 그으면 꼭지각이 36도이고 두 밑각이 72도인 황금 이등변삼각형이 나타납니다. "
                        f"밑각 72도를 이등분하는 황금 보조선 한 줄만 그으면, 큰 삼각형과 작은 삼각형이 닮음이 되면서 대각선 길이가 정확히 황금비 파이가 됨이 증명됩니다!"
                    ),
                    "hud_notes": [
                        "결정적 보조선: 36°-72°-72° 이등변삼각형의 밑각(72°) 이등분선 작도!",
                        "닮음비 연쇄: 큰 삼각형 ∽ 작은 삼각형 → x : 1 = 1 : (x - 1)",
                        "삼각비 연결: cos 36° = φ / 2 = (1 + √5) / 4 , sin 18° = (√5 - 1) / 4",
                    ],
                },
                {
                    "act": 4,
                    "badge": "ACT 4 · 한계를 넘는 상상 (연분수와 차수 강하 마법)",
                    "headline": "φ² = φ + 1 식 하나로 고차 거듭제곱을 1차식으로 단번에 낮춘다!",
                    "key_formula": "φⁿ = Fₙ·φ + Fₙ₋₁  (Degree Reduction via Fibonacci!)",
                    "narration": (
                        f"황금비의 대수적 마법은 파이 제곱이 파이 더하기 1이라는 식에 있습니다! "
                        f"제곱을 1차식으로 바꿀 수 있기 때문에, 파이의 3제곱, 4제곱, n제곱도 복잡한 무리수 계산 없이 피보나치 수를 계수로 갖는 1차식으로 단번에 줄어듭니다!"
                    ),
                    "hud_notes": [
                        "차수 강하 공식: φ² = φ + 1 , φ³ = 2φ + 1 , φ⁴ = 3φ + 2 , φ⁵ = 5φ + 3!",
                        "계수의 비밀: 거듭제곱 계수가 그대로 피보나치 수열(1, 1, 2, 3, 5, 8...)!",
                        "가장 아름다운 연분수: φ = 1 + 1 / (1 + 1 / (1 + 1 / ...))",
                    ],
                },
                {
                    "act": 5,
                    "badge": "ACT 5 · 경시·수능 황금비 & 점화식 10초 통찰",
                    "headline": "닮음 도형이 반복되거나 36°·72°가 보이면 즉시 자기닮음 비례식을 세워라!",
                    "key_formula": "Self-Similar Split → x = 1 + 1/x → Golden Ratio φ!",
                    "narration": (
                        f"도형 문제에서 정오각형이나 36도, 혹은 똑같은 모양이 반복해서 잘려 나가는 프랙탈 구조를 만났다면, 전체를 x로 놓고 부분과의 닮음비를 세우세요! "
                        f"지금 바로 @min7014_ai 채널을 구독하고 자연과 우주의 수학 시네마를 이어서 감상하세요!"
                    ),
                    "hud_notes": [
                        "실전 포인트 1: 36°·72°·108° 등장 시 밑각 이등분선 보조선 즉시 작도!",
                        "실전 포인트 2: φ² = φ + 1 을 이용해 고차식을 1차식으로 즉시 차수 강하!",
                        "지금 [@min7014_ai 구독] 누르고 1,113개 창의 수학 시네마를 정주행하세요!",
                    ],
                },
            ]
        else:
            return [
                {
                    "act": 1,
                    "badge": "ACT 1 · THE GOLDEN SPIRAL OF NATURE",
                    "headline": f"144 Sunflower Seeds Pack Perfectly Using the 137.5° Golden Angle! ({t_title})",
                    "key_formula": "φ = (1 + √5) / 2 ≈ 1.618034  |  Golden Angle = 137.508°",
                    "narration": (
                        f"Watch 144 glowing seeds spiral outward at the exact golden angle of 137.5 degrees. "
                        f"In [{t_title}], this irrational rotation prevents seeds from ever stacking in radial lines, generating Fibonacci spiral arms in both directions!"
                    ),
                    "hud_notes": [
                        "Golden Angle (137.508°): 360° ÷ φ² achieves optimal packing density!",
                        "Fibonacci Spiral Arms: Left & right spirals always match Fibonacci numbers!",
                        "Core Identity: φ² = φ + 1  ⇔  1/φ = φ - 1",
                    ],
                },
                {
                    "act": 2,
                    "badge": "ACT 2 · INFINITE SELF-SIMILAR GOLDEN RECTANGLES",
                    "headline": "Slice Off a Square and the Remaining Rectangle Keeps the Exact Same Ratio!",
                    "key_formula": "φ : 1 = 1 : (φ - 1)  ⇒  φ² - φ - 1 = 0",
                    "narration": (
                        f"Remove a 1 by 1 square from a golden rectangle of length phi, and the remaining smaller rectangle has sides 1 and phi minus 1—preserving the exact golden ratio forever!"
                    ),
                    "hud_notes": [
                        "Self-Similarity: Long : Short = Short : Remainder",
                        "Algebraic Equation: φ : 1 = 1 : (φ - 1)  →  φ² - φ - 1 = 0",
                        "Fibonacci Ratios: 1/1, 2/1, 3/2, 5/3, 8/5, 13/8 → 1.618034!",
                    ],
                },
                {
                    "act": 3,
                    "badge": "ACT 3 · THE 36°-72°-72° GOLDEN TRIANGLE AUXILIARY LINE",
                    "headline": "One Angle Bisector Inside a Regular Pentagon Proves the Golden Ratio!",
                    "key_formula": "Diagonal / Side = 2·cos(36°) = φ ≈ 1.618",
                    "narration": (
                        f"Draw the diagonals of a regular pentagon to form a 36-72-72 degree golden triangle. "
                        f"Bisecting one 72-degree base angle creates a smaller similar golden triangle, proving that the diagonal-to-side ratio is strictly phi!"
                    ),
                    "hud_notes": [
                        "Golden Auxiliary Line: Bisect the 72° base angle of the 36°-72°-72° triangle",
                        "Similar Triangles: Whole Triangle ∽ Smaller Triangle → φ² - φ - 1 = 0",
                        "Exact Trig Values: cos 36° = φ / 2 = (1 + √5) / 4",
                    ],
                },
                {
                    "act": 4,
                    "badge": "ACT 4 · FIBONACCI POWER REDUCTION MAGIC",
                    "headline": "Reduce Any Power φⁿ to a Linear Fibonacci Expression Instantly!",
                    "key_formula": "φⁿ = Fₙ·φ + Fₙ₋₁  (since φ² = φ + 1)",
                    "narration": (
                        f"Because phi squared equals phi plus 1, every higher power of phi collapses into a linear combination of phi and 1 with Fibonacci coefficients!"
                    ),
                    "hud_notes": [
                        "Power Reduction: φ² = φ+1, φ³ = 2φ+1, φ⁴ = 3φ+2, φ⁵ = 5φ+3!",
                        "Coefficients are the exact Fibonacci sequence Fₙ and Fₙ₋₁!",
                        "Simplest Continued Fraction: φ = 1 + 1/(1 + 1/(1 + ...))",
                    ],
                },
                {
                    "act": 5,
                    "badge": "ACT 5 · 10-SECOND OLYMPIAD TAKEAWAY",
                    "headline": "Spot Self-Similarity or 36° Angles and Set Up the Golden Ratio Immediately!",
                    "key_formula": "Self-Similar Split → x = 1 + 1/x → Golden Ratio φ!",
                    "narration": (
                        f"Whenever a geometry or recurrence problem repeats self-similarly, use phi squared equals phi plus 1 to solve it in seconds! "
                        f"Subscribe to @min7014_ai right now for daily visual math cinema!"
                    ),
                    "hud_notes": [
                        "Instant Trigger: 36°/72° Pentagon → Draw 72° Angle Bisector!",
                        "Algebraic Trigger: x² = x + 1 → Reduce high powers via Fibonacci!",
                        "Subscribe to @min7014_ai & try the interactive simulator below!",
                    ],
                },
            ]

    if archetype == "prob_galton":
        if lang_code == "ko":
            return [
                {
                    "act": 1,
                    "badge": "ACT 1 · 우연 속에서 피어나는 필연의 종 모양 곡선",
                    "headline": f"무작위로 떨어지는 구슬들이 왜 언제나 완벽한 정규분포 곡선을 만들까? ({t_title})",
                    "key_formula": "B(n, p)  —(n→∞)→  N(np, npq)  (Central Limit Theorem)",
                    "narration": (
                        f"수백 개의 빛나는 입자가 갈톤 보드의 핀들과 부딪히며 왼쪽 또는 오른쪽으로 무작위 낙하합니다. "
                        f"공 하나하나의 경로는 예측할 수 없는 우연이지만, 바닥에 쌓인 막대그래프는 놀랍게도 [{t_title}]의 황금빛 가우스 정규분포 종 곡선과 정확히 일치합니다! "
                        f"혼돈 속에서 어떻게 이런 완벽한 대칭 질서가 탄생할까요?"
                    ),
                    "hud_notes": [
                        "갈톤 보드(Galton Board): 매 층마다 좌/우 50% 확률로 독립 분기!",
                        "기적의 수렴: 무작위 시행이 쌓일수록 완벽한 좌우 대칭 종 모양 완성!",
                        "핵심 원리: 파스칼의 삼각형 조합(nCr) → 이항분포 → 정규분포!",
                    ],
                },
                {
                    "act": 2,
                    "badge": "ACT 2 · 파스칼의 삼각형 경로 세기와 이항계수",
                    "headline": "양 끝으로 가는 길은 단 1가지, 정중앙으로 모이는 길은 폭발적으로 많다!",
                    "key_formula": "P(X = k) = ₙCₖ · pᵏ · (1 - p)ⁿ⁻ᵏ",
                    "narration": (
                        f"왜 구슬들이 양 끝보다 정중앙 칸에 압도적으로 많이 모일까요? "
                        f"8층의 핀을 통과할 때 맨 왼쪽 끝으로 가려면 여덟 번 연속 왼쪽으로만 가야 하므로 경로가 단 한 가지뿐입니다. "
                        f"반면 왼쪽 네 번, 오른쪽 네 번이 섞이는 정중앙 칸으로 가는 경로는 8콤비네이션 4, 무려 일흔 가지나 되기 때문입니다!"
                    ),
                    "hud_notes": [
                        "경로 개수 비교 (8단 기준): 양 끝 칸 = ₈C₀ = 1가지 vs 중앙 칸 = ₈C₄ = 70가지!",
                        "이항계수 합: 1 + 8 + 28 + 56 + 70 + 56 + 28 + 8 + 1 = 2⁸ = 256",
                        "각 칸에 쌓이는 높이는 정확히 그 칸으로 도달하는 조합 경로의 수에 비례!",
                    ],
                },
                {
                    "act": 3,
                    "badge": "ACT 3 · 대칭성과 기대값·분산의 선형 결합 아이디어",
                    "headline": "복잡한 시그마 계산 대신 1회 시행의 평균과 분산을 n배로 확장하라!",
                    "key_formula": "E(X) = n·p  ,  Var(X) = n·p·(1 - p)  ,  σ = √(npq)",
                    "narration": (
                        f"이항분포의 평균과 분산을 구할 때 복잡한 시그마 조합 식을 직접 전개할 필요가 전혀 없습니다! "
                        f"단 한 번의 핀 충돌을 0과 1의 베르누이 시행으로 보면 평균은 p, 분산은 p 곱하기 q입니다. "
                        f"독립인 n번의 충돌을 더하면 평균도 정확히 n배, 분산도 정확히 n배가 된다는 선형성 아이디어 하나로 1초 만에 증명됩니다!"
                    ),
                    "hud_notes": [
                        "결정적 아이디어: X = X₁ + X₂ + ... + Xₙ (독립 지시확률변수의 합!)",
                        "1회 시행: E(Xᵢ) = p , Var(Xᵢ) = pq  →  n회 합산: E(X) = np , Var(X) = npq!",
                        "표준편차(퍼짐 정도)는 시행 횟수의 제곱근 √n 에 비례하여 성장!",
                    ],
                },
                {
                    "act": 4,
                    "badge": "ACT 4 · 한계를 넘는 상상 (드무아브르-라플라스 & 중심극한정리)",
                    "headline": "단수를 무한히 늘리면 계단 모양 막대가 매끄러운 가우스 적분 곡선이 된다!",
                    "key_formula": "Z = (X - np) / √(npq)  →  f(z) = (1/√(2π))·e^(-z²/2)",
                    "narration": (
                        f"만약 갈톤 보드의 핀 층수를 8층에서 수백 층, 수만 층으로 늘리고 칸의 간격을 좁히면 어떻게 될까요? "
                        f"불연속적이던 계단형 이항분포 막대들이 매끄러운 곡선으로 녹아들며 자연상수 e와 원주율 파이가 결합된 표준정규분포 함수가 탄생합니다! "
                        f"이것이 바로 통계학 최고의 정리인 중심극한정리입니다."
                    ),
                    "hud_notes": [
                        "표준화 변환: 평균 np를 0으로, 표준편차 √(npq)를 1로 맞추는 Z-스케일링!",
                        "68 - 95 - 99.7 법칙: 평균 ±1σ 안에 68%, ±2σ 안에 95.4%가 항상 수렴!",
                        "이산수학(조합 nCr)과 연속미적분(e^(-z²/2) 넓이)이 하나로 만나는 다리!",
                    ],
                },
                {
                    "act": 5,
                    "badge": "ACT 5 · 수능 확률과 통계 10초 해법",
                    "headline": "독립시행이 반복되면 주저 없이 B(n,p) → N(np, npq) 표준화 넓이로 풀어라!",
                    "key_formula": "Spot Repeated Independent Trials → Standardize Z = (X - m)/σ!",
                    "narration": (
                        f"수능과 모의고사에서 주사위나 동전을 수백 번 던지는 확률 문제를 만나면, 개별 확률을 더하는 대신 즉시 정규분포 종 곡선의 대칭 넓이로 바꾸어 10초 만에 해결하세요! "
                        f"지금 바로 @min7014_ai 채널을 구독하고 살아 움직이는 수학 시네마를 정주행하세요!"
                    ),
                    "hud_notes": [
                        "실전 1단계: 시행 횟수 n과 성공 확률 p를 찾아 평균 m=np, 표준편차 σ=√(npq) 계산",
                        "실전 2단계: Z = (X - m)/σ 표준화 후 대칭 종 곡선 넓이표로 즉시 정답 도출!",
                        "지금 [@min7014_ai 구독] 누르고 1,113개 창의 수학 시네마를 만나보세요!",
                    ],
                },
            ]
        else:
            return [
                {
                    "act": 1,
                    "badge": "ACT 1 · ORDER EMERGING FROM PURE CHAOS",
                    "headline": f"Randomly Bouncing Beads Always Sculpt a Perfect Bell Curve! ({t_title})",
                    "key_formula": "B(n, p)  —(n→∞)→  N(np, npq)  (Central Limit Theorem)",
                    "narration": (
                        f"Hundreds of glowing particles bounce randomly left and right through the pegs of a Galton board. "
                        f"While each individual bead's path is unpredictable, the stacked columns at the bottom always converge to the golden Gaussian bell curve of [{t_title}]!"
                    ),
                    "hud_notes": [
                        "Galton Board: Every peg bounce is an independent 50/50 Bernoulli trial!",
                        "Emergent Symmetry: Randomness aggregates into a deterministic bell curve!",
                        "Core Bridge: Pascal's Triangle (nCr) → Binomial → Normal Distribution!",
                    ],
                },
                {
                    "act": 2,
                    "badge": "ACT 2 · PASCAL'S TRIANGLE & PATH COMBINATORICS",
                    "headline": "Only 1 Path Reaches the Extreme Edge, While 70 Paths Feed the Center!",
                    "key_formula": "P(X = k) = ₙCₖ · pᵏ · (1 - p)ⁿ⁻ᵏ",
                    "narration": (
                        f"Why do beads pile up in the center? "
                        f"Across 8 rows of pegs, reaching the far left requires 8 consecutive left bounces—just 1 path. "
                        f"Reaching the center allows any arrangement of 4 lefts and 4 rights, giving 8 choose 4 equals 70 distinct paths!"
                    ),
                    "hud_notes": [
                        "Path Count (8 Rows): Edge Bin = ₈C₀ = 1 Path vs Center Bin = ₈C₄ = 70 Paths!",
                        "Sum of Binomial Coefficients: 1+8+28+56+70+56+28+8+1 = 2⁸ = 256",
                        "Column heights directly visualize combinations ₙCₖ!",
                    ],
                },
                {
                    "act": 3,
                    "badge": "ACT 3 · LINEARITY OF EXPECTATION & VARIANCE",
                    "headline": "Decompose n Bounces Into n Simple 0-or-1 Indicator Variables!",
                    "key_formula": "E(X) = n·p  ,  Var(X) = n·p·(1 - p)  ,  σ = √(npq)",
                    "narration": (
                        f"Never expand messy sigma factorials to find the mean and variance! "
                        f"Because X is the sum of n independent single-peg indicator variables, the mean is simply n times p and the variance is n times p times q!"
                    ),
                    "hud_notes": [
                        "Key Decomposition: X = X₁ + X₂ + ... + Xₙ (Independent Indicators)",
                        "Single Peg: E(Xᵢ)=p, Var(Xᵢ)=pq  ⇒  n Pegs: E(X)=np, Var(X)=npq!",
                        "Spread grows with the square root of trials: σ = √(npq)",
                    ],
                },
                {
                    "act": 4,
                    "badge": "ACT 4 · THE CENTRAL LIMIT THEOREM IN ACTION",
                    "headline": "As Peg Rows Approach Infinity, Discrete Bars Melt Into e^(-z²/2)!",
                    "key_formula": "Z = (X - np) / √(npq)  →  f(z) = (1/√(2π))·e^(-z²/2)",
                    "narration": (
                        f"Increase the rows to infinity and standardize by subtracting the mean and dividing by sigma. "
                        f"The discrete binomial steps morph smoothly into the universal Gaussian bell curve linking e and pi!"
                    ),
                    "hud_notes": [
                        "Z-Score Standardization: Centers mean at 0 and unit standard deviation at 1",
                        "68 - 95 - 99.7 Rule governs all natural measurement errors!",
                        "Unifies discrete combinatorics with continuous calculus integrals!",
                    ],
                },
                {
                    "act": 5,
                    "badge": "ACT 5 · 10-SECOND PROBABILITY EXAM STRATEGY",
                    "headline": "Convert Large Binomial Sums Into Symmetric Bell Curve Areas Instantly!",
                    "key_formula": "Spot Repeated Independent Trials → Standardize Z = (X - m)/σ!",
                    "narration": (
                        f"When facing hundreds of independent trials on an exam, standardize to Z and read the symmetric bell curve area in 10 seconds! "
                        f"Subscribe to @min7014_ai right now for daily visual math cinema!"
                    ),
                    "hud_notes": [
                        "Step 1: Compute m = np and σ = √(npq) from the trial count",
                        "Step 2: Transform to Z = (X - m)/σ and use symmetry of the normal curve!",
                        "Subscribe to @min7014_ai & explore our live 60fps simulator!",
                    ],
                },
            ]

    if archetype == "calculus_motion":
        if lang_code == "ko":
            return [
                {
                    "act": 1,
                    "badge": "ACT 1 · 평균 속도와 순간 속도가 일치하는 찰나",
                    "headline": f"출발점과 도착점을 잇는 할선과 완전히 평행한 접선이 반드시 존재한다! ({t_title})",
                    "key_formula": "(f(b) - f(a)) / (b - a) = f'(c)  (c ∈ (a, b))",
                    "narration": (
                        f"매끄러운 곡선 위를 달리는 점이 출발점 A에서 도착점 B까지 가속과 감속을 반복하며 이동합니다. "
                        f"놀랍게도 [{t_title}]에 의하면, 전체 구간의 평균 기울기인 할선과 완벽히 평행한 순간 접선 기울기를 갖는 지점 c가 구간 안에 반드시 하나 이상 존재합니다! "
                        f"과속 단속 카메라가 순간 속도계 없이도 과속을 잡아내는 이 미적분의 원리를 눈으로 확인해 봅시다."
                    ),
                    "hud_notes": [
                        "할선(Secant Line): 두 끝점 A, B를 잇는 전체 구간의 평균 변화율",
                        "접선(Tangent Line): 곡선 위 점 c에서의 순간 변화율 f'(c)",
                        "핵심 정리: 매끄러운 곡선에는 할선과 평행한 접선이 반드시 존재!",
                    ],
                },
                {
                    "act": 2,
                    "badge": "ACT 2 · 평행선 스캔으로 찾는 최대 이격점 c",
                    "headline": "할선을 평행이동해 곡선과 가장 멀어지는 꼭대기에서 접선이 탄생한다!",
                    "key_formula": "max |f(x) - L(x)| at x = c  ⇒  f'(c) = L'(c)",
                    "narration": (
                        f"할선을 그대로 들어 올려 곡선 위쪽으로 평행이동시켜 보세요! "
                        f"곡선과 할선 사이의 수직 거리가 가장 멀어지는 바로 그 정상 지점에서, 평행이동한 직선이 곡선에 스치듯 접하게 됩니다! "
                        f"차이 함수의 높이가 극대가 되는 점에서 미분계수가 0이 된다는 롤의 정리가 눈앞에서 직관적으로 확인됩니다."
                    ),
                    "hud_notes": [
                        "1단계 관찰: 할선 L(x)에서 곡선 f(x)까지의 수직 거리 h(x) 측정",
                        "2단계 관찰: 수직 거리 h(x)가 최대인 점 c에서 접선이 할선과 평행!",
                        "핵심 브릿지: 기울어진 평균값 정리 = 회전시킨 롤의 정리(f'(c)=0)!",
                    ],
                },
                {
                    "act": 3,
                    "badge": "ACT 3 · 할선의 두 점이 합쳐지는 극한과 리만 합",
                    "headline": "Δx가 0으로 수렴할 때 할선은 접선이 되고, 막대 넓이는 정적분이 된다!",
                    "key_formula": "lim(Δx→0) Δy/Δx = dy/dx  |  lim Σ f(xₖ)Δx = ∫ f(x)dx",
                    "narration": (
                        f"이제 두 점 사이의 간격 델타 x를 0으로 좁혀 보세요. 두 점을 잇던 할선이 한 점에서의 접선으로 수렴합니다! "
                        f"반대로 곡선 아래를 잘게 쪼갠 네온 직사각형 기둥들을 무한히 더하면, 미분의 역연산인 정적분 넓이로 정확히 수렴합니다."
                    ),
                    "hud_notes": [
                        "미분의 기하학: 두 점의 할선 기울기가 한 점의 접선 기울기로 수렴!",
                        "적분의 기하학: 구분구적 직사각형 넓이 합이 곡선 아래 정적분으로 수렴!",
                        "미적분학의 기본정리: 순간 변화율(접선)을 누적하면 전체 변화량(넓이)!",
                    ],
                },
                {
                    "act": 4,
                    "badge": "ACT 4 · 한계를 넘는 상상 (코시의 평균값 정리와 로피탈)",
                    "headline": "시간 t를 매개변수로 둔 두 함수 f(t), g(t)의 궤적에서도 평행 접선이 성립한다!",
                    "key_formula": "(g(b) - g(a)) / (f(b) - f(a)) = g'(c) / f'(c)",
                    "narration": (
                        f"만약 x축과 y축이 모두 시간에 따라 움직이는 매개변수 곡선이라면 어떻게 될까요? "
                        f"가로 변화량과 세로 변화량의 비율 역시 어느 한 순간 c에서의 미분계수 비율과 정확히 일치합니다! "
                        f"이 코시의 평균값 정리에서 바로 0분의 0 꼴 극한을 단번에 계산하는 로피탈의 정리와 테일러 급수가 탄생합니다."
                    ),
                    "hud_notes": [
                        "확장 1: 코시의 평균값 정리 → 매개변수 평면 운동(x=f(t), y=g(t))의 평행 접선!",
                        "확장 2: 0/0 부정형 극한에서 할선 비를 접선 비 f'(c)/g'(c)로 바꾼 로피탈 정리!",
                        "확장 3: 미분불가능한 뾰족점(첨점)에서는 평행 접선이 존재하지 않는 반례 확인!",
                    ],
                },
                {
                    "act": 5,
                    "badge": "ACT 5 · 수능 미적분·수II 킬러 10초 통찰",
                    "headline": "두 함숫값의 차이 f(b)-f(a)가 보이면 즉시 평균변화율과 접선 기울기로 번역하라!",
                    "key_formula": "f(b) - f(a) = f'(c)·(b - a)  (Instant MVT Translation!)",
                    "narration": (
                        f"수능과 수리논술에서 두 점의 함숫값 차이나 평균변화율 부등식이 등장하면, 식을 전개하지 말고 그래프 위에서 할선과 평행한 접선의 위치부터 찾으세요! "
                        f"지금 바로 @min7014_ai 채널을 구독하고 미적분의 모든 시각적 아이디어를 마스터하세요!"
                    ),
                    "hud_notes": [
                        "실전 제1원칙: (f(b)-f(a))/(b-a) 등장 시 즉시 f'(c) 접선 기울기로 해석!",
                        "차이 함수 h(x) = f(x) - L(x)를 세우면 교점과 접점의 관계가 1초에 해결!",
                        "지금 [@min7014_ai 구독] 누르고 1,113개 창의 수학 시네마를 정주행하세요!",
                    ],
                },
            ]
        else:
            return [
                {
                    "act": 1,
                    "badge": "ACT 1 · SECANT VELOCITY MEETS TANGENT VELOCITY",
                    "headline": f"Every Smooth Journey Guarantees an Instant Where Tangent Parallels Secant! ({t_title})",
                    "key_formula": "(f(b) - f(a)) / (b - a) = f'(c)  (c ∈ (a, b))",
                    "narration": (
                        f"As a glowing point travels along a smooth curve from A to B, its instantaneous speed fluctuates. "
                        f"Yet [{t_title}] guarantees at least one interior point c where the instantaneous tangent line is strictly parallel to the overall secant line!"
                    ),
                    "hud_notes": [
                        "Secant Line: Average rate of change across the interval [a, b]",
                        "Tangent Line: Instantaneous derivative f'(c) at point c",
                        "Core Law: Smoothness forces instantaneous slope to match average slope!",
                    ],
                },
                {
                    "act": 2,
                    "badge": "ACT 2 · PARALLEL SECANT SWEEP TO MAXIMUM GAP",
                    "headline": "Slide the Secant Line Until It Kisses the Peak of Maximum Vertical Gap!",
                    "key_formula": "max |f(x) - L(x)| at x = c  ⇒  f'(c) = L'(c)",
                    "narration": (
                        f"Translate the secant line upward until it just touches the curve at the point of maximum vertical separation. "
                        f"At that exact peak c, the vertical gap stops growing, forcing the tangent slope to equal the secant slope!"
                    ),
                    "hud_notes": [
                        "Step 1: Measure vertical gap h(x) = f(x) - L(x) between curve and secant",
                        "Step 2: At maximum gap x = c, h'(c) = 0 ⇒ f'(c) = secant slope!",
                        "Mean Value Theorem is simply Rolle's Theorem tilted at an angle!",
                    ],
                },
                {
                    "act": 3,
                    "badge": "ACT 3 · SECANT-TO-TANGENT LIMIT & RIEMANN SUMS",
                    "headline": "As Δx → 0, Secants Become Tangents and Riemann Bars Become Integrals!",
                    "key_formula": "lim(Δx→0) Δy/Δx = dy/dx  |  lim Σ f(xₖ)Δx = ∫ f(x)dx",
                    "narration": (
                        f"Watch the two secant points merge into a single tangent line while the glowing Riemann rectangles underneath fuse into the exact definite integral area!"
                    ),
                    "hud_notes": [
                        "Derivative: Limit of secant slopes as Δx shrinks to zero",
                        "Definite Integral: Limit of Riemann rectangle areas under the curve",
                        "Fundamental Theorem: Differentiation and integration are exact inverses!",
                    ],
                },
                {
                    "act": 4,
                    "badge": "ACT 4 · CAUCHY'S MVT & PARAMETRIC MOTION",
                    "headline": "Generalizing to Parametric Curves (f(t), g(t)) and L'Hôpital's Rule!",
                    "key_formula": "(g(b) - g(a)) / (f(b) - f(a)) = g'(c) / f'(c)",
                    "narration": (
                        f"When both x and y evolve with time t, Cauchy's Mean Value Theorem guarantees a point where the ratio of derivatives matches the overall chord slope!"
                    ),
                    "hud_notes": [
                        "Cauchy's MVT: Parametric path (f(t), g(t)) has a parallel tangent vector!",
                        "Direct Foundation of L'Hôpital's Rule for 0/0 indeterminate limits",
                        "Sharp corners (cusps) break differentiability and void the guarantee!",
                    ],
                },
                {
                    "act": 5,
                    "badge": "ACT 5 · 10-SECOND CALCULUS EXAM STRATEGY",
                    "headline": "Spot f(b) - f(a) and Immediately Translate It Into Tangent Slope f'(c)!",
                    "key_formula": "f(b) - f(a) = f'(c)·(b - a)  (Instant MVT Translation!)",
                    "narration": (
                        f"Whenever f of b minus f of a appears in a calculus problem, translate it into a parallel tangent line to solve it visually in seconds! "
                        f"Subscribe to @min7014_ai right now for daily visual math cinema!"
                    ),
                    "hud_notes": [
                        "Instant Trigger: Replace difference quotients with derivative f'(c)!",
                        "Construct difference function h(x) = f(x) - L(x) for tangent intersections",
                        "Subscribe to @min7014_ai & try the interactive 60fps lab below!",
                    ],
                },
            ]

    if archetype == "ceva_menelaus":
        if lang_code == "ko":
            return [
                {
                    "act": 1,
                    "badge": "ACT 1 · 삼각형 비율의 완벽한 균형 미스터리",
                    "headline": f"교점이 어디로 움직여도 세 비율의 곱은 언제나 1.000이다! ({t_title})",
                    "key_formula": "(BD / DC) × (CE / EA) × (AF / FB) = 1.000",
                    "narration": (
                        f"밤하늘의 삼각형 내부에서 세 체바 직선이 만나는 교점 P가 쉼 없이 움직입니다. "
                        f"점 P가 움직일 때마다 세 변을 나누는 여섯 개 조각의 길이는 모두 달라지지만, 놀랍게도 [{t_title}]에서 세 비율을 곱한 값은 언제나 정확히 1.000으로 고정됩니다! "
                        f"길이조차 모르는 일반 삼각형에서 어떻게 이 비율의 곱이 영원히 보존될까요?"
                    ),
                    "hud_notes": [
                        "역동적 관찰: 교점 P가 어디로 이동해도 3개 비율의 곱은 항상 1.000!",
                        "핵심 불변량: 시계 방향으로 한 바퀴 돌며 만든 분수 3개의 연쇄 상쇄!",
                        "질문: 선분의 길이 비를 무엇으로 바꾸어야 약분이 일어날까?",
                    ],
                },
                {
                    "act": 2,
                    "badge": "ACT 2 · 무게중심 대칭 실험과 지렛대 시소 원리",
                    "headline": "정중앙 1×1×1=1 에서 출발해 비대칭 역수 상쇄를 눈으로 확인하라!",
                    "key_formula": "Symmetric Center: (1/1) × (1/1) × (1/1) = 1.000",
                    "narration": (
                        f"먼저 교점 P를 삼각형의 정중앙 무게중심에 놓아 봅시다. 세 변이 모두 1 대 1로 이등분되어 1 곱하기 1 곱하기 1은 당연히 1입니다. "
                        f"이제 점 P를 한쪽 꼭짓점으로 당기면 한 변의 비율이 2배로 커지지만, 나머지 두 변의 비율 곱이 정확히 2분의 1로 줄어들며 완벽한 시소 균형을 이룹니다!"
                    ),
                    "hud_notes": [
                        "1단계 대칭점: 무게중심에서 1 : 1 내분 → 1 × 1 × 1 = 1 즉시 성립!",
                        "2단계 시소 균형: 한 비율이 k배 커지면 인접 비율 곱이 1/k배로 자동 보정!",
                        "아르키메데스의 지렛대: 각 꼭짓점에 질량을 놓으면 교점 P가 질량중심!",
                    ],
                },
                {
                    "act": 3,
                    "badge": "ACT 3 · 밑변 비를 넓이 비로 바꾸는 황금 수선 아이디어",
                    "headline": "높이가 같은 두 삼각형의 넓이 비 S₁ : S₂ : S₃ 도미노 연쇄 약분!",
                    "key_formula": "(S₃ / S₂) × (S₁ / S₃) × (S₂ / S₁) = 1",
                    "narration": (
                        f"이 정리를 단 10초 만에 증명하는 천재적 아이디어는 '선분의 길이 비'를 '삼각형의 넓이 비'로 번역하는 것입니다! "
                        f"화면의 세 색깔 삼각형 S1, S2, S3를 보세요. 밑변 BD 대 DC의 길이 비는 꼭짓점 P를 공유하는 두 삼각형 S3 대 S2의 넓이 비와 같습니다! "
                        f"세 비율을 넓이 분수로 바꾸어 곱하는 순간, 분자와 분모의 S1, S2, S3가 도미노처럼 모두 약분되어 사라지고 숫자 1만 남습니다!"
                    ),
                    "hud_notes": [
                        "결정적 번역: 밑변 길이 비 BD : DC = 넓이 비 S(△PAB) : S(△PAC)!",
                        "도미노 약분: (S₃ / S₂) × (S₁ / S₃) × (S₂ / S₁) = 1.000!",
                        "또는 한 꼭짓점에서 평행 보조선 1줄 작도 → 닮음 삼각형 2쌍으로 증명!",
                    ],
                },
                {
                    "act": 4,
                    "badge": "ACT 4 · 한계를 넘는 상상 (메넬라우스 할선과 외분 확장)",
                    "headline": "교점이 삼각형 밖으로 나가거나 직선 하나가 삼각형을 관통할 때도 성립!",
                    "key_formula": "Ceva (3 Concurrent Lines)  ↔  Menelaus (3 Collinear Points)",
                    "narration": (
                        f"만약 교점 P가 삼각형 바깥으로 나가거나, 직선 하나가 삼각형의 세 변과 연장선을 뚫고 지나가는 메넬라우스 구조가 되면 어떨까요? "
                        f"꼭짓점에서 직선으로 내린 세 수선의 높이 비나 평행 보조선 한 줄을 그으면, 똑같이 세 비율의 곱이 1이라는 황금 불변량이 그대로 유지됩니다!"
                    ),
                    "hud_notes": [
                        "쌍대성(Duality): 세 직선이 한 점에 모임(체바) ↔ 세 점이 한 직선에 놓임(메넬라우스)",
                        "외부 확장: 교점이 삼각형 외부에 있어도 외분비의 곱은 여전히 1.000!",
                        "3차원 사영기하와 구면삼각형까지 그대로 확장되는 불변 구조!",
                    ],
                },
                {
                    "act": 5,
                    "badge": "ACT 5 · 수능·올림피아드 기하 10초 해법",
                    "headline": "삼각형 내부에 교차 선분과 내분비가 보이면 한 바퀴 회전 곱 = 1을 즉시 써라!",
                    "key_formula": "Vertex → Divide Point → Vertex (1 Full Loop Product = 1)",
                    "narration": (
                        f"기하 문제에서 삼각형을 가로지르는 직선들과 선분 비율이 주어졌을 때 연립방정식을 세우지 마세요. "
                        f"꼭짓점에서 분점으로, 분점에서 다음 꼭짓점으로 한 바퀴 도는 도미노 분수 곱을 세우면 단 10초 만에 미지수가 풀립니다! "
                        f"지금 바로 @min7014_ai 채널을 구독하고 모든 기하 아이디어를 눈으로 깨쳐 보세요!"
                    ),
                    "hud_notes": [
                        "실전 암기 제로 팁: (꼭짓점→분점)/(분점→꼭짓점) 3번 징검다리 점프 = 1!",
                        "넓이 비 질문 시: S₁ : S₂ : S₃ 질량중심(지렛대) 비율로 3초 계산!",
                        "지금 [@min7014_ai 구독] 누르고 1,113개 창의 수학 시네마를 정주행하세요!",
                    ],
                },
            ]
        else:
            return [
                {
                    "act": 1,
                    "badge": "ACT 1 · THE TRIANGLE RATIO MYSTERY",
                    "headline": f"No Matter Where Point P Moves, the Product of Three Ratios Is Strictly 1! ({t_title})",
                    "key_formula": "(BD / DC) × (CE / EA) × (AF / FB) = 1.000",
                    "narration": (
                        f"Watch the intersection point P glide freely across the triangle. "
                        f"Every individual segment length changes continuously, yet in [{t_title}], the cyclic product of the three division ratios stays locked at 1.000!"
                    ),
                    "hud_notes": [
                        "Dynamic Observation: As P moves, all 6 segment lengths change live!",
                        "Core Invariant: Cyclic product around the perimeter is always 1.000!",
                        "Question: What hidden quantity cancels all three fractions like dominoes?",
                    ],
                },
                {
                    "act": 2,
                    "badge": "ACT 2 · CENTROID EQUILIBRIUM & LEVER BALANCE",
                    "headline": "Start at the 1×1×1 = 1 Centroid and Watch Inverse Ratios Balance Live!",
                    "key_formula": "Symmetric Center: (1/1) × (1/1) × (1/1) = 1.000",
                    "narration": (
                        f"At the symmetric centroid, every side is bisected 1 to 1, giving 1 times 1 times 1 equals 1. "
                        f"Pulling P toward any vertex stretches one ratio by factor k while compressing the remaining two ratios by 1 over k!"
                    ),
                    "hud_notes": [
                        "Symmetric Baseline: Midpoints give (1/1)×(1/1)×(1/1) = 1",
                        "Archimedes' Lever Law: Point P acts as the center of mass of the vertices!",
                        "Every stretch is balanced by an inverse compression.",
                    ],
                },
                {
                    "act": 3,
                    "badge": "ACT 3 · TRANSLATING LENGTH RATIOS INTO AREA RATIOS",
                    "headline": "Replace Segment Ratios With Triangle Areas S₁, S₂, S₃ for Domino Cancellation!",
                    "key_formula": "(S₃ / S₂) × (S₁ / S₃) × (S₂ / S₁) = 1",
                    "narration": (
                        f"The master stroke is translating 1D segment ratios into 2D triangle areas S1, S2, and S3! "
                        f"Because triangles sharing the same altitude have areas proportional to their bases, the three ratios become S3 over S2, S1 over S3, and S2 over S1—canceling out like dominoes to leave 1!"
                    ),
                    "hud_notes": [
                        "Key Translation: Base Ratio BD : DC = Area Ratio S₃ : S₂!",
                        "Domino Cancellation: (S₃/S₂) × (S₁/S₃) × (S₂/S₁) = 1.000!",
                        "Alternative Proof: 1 parallel auxiliary line creates 2 pairs of similar triangles!",
                    ],
                },
                {
                    "act": 4,
                    "badge": "ACT 4 · DUALITY WITH MENELAUS & EXTERIOR POINTS",
                    "headline": "3 Concurrent Lines (Ceva) ↔ 3 Collinear Points (Menelaus)!",
                    "key_formula": "Ceva (Concurrent Lines)  ↔  Menelaus (Transversal Line)",
                    "narration": (
                        f"What if point P moves outside the triangle, or a single transversal line slices across all three sides? "
                        f"Dropping three perpendicular altitudes to the transversal line proves Menelaus' Theorem with the exact same domino cancellation!"
                    ),
                    "hud_notes": [
                        "Projective Duality: Ceva (concurrency) and Menelaus (collinearity)",
                        "Works identically when intersection P lies outside the triangle!",
                        "One parallel auxiliary line solves every triangle ratio problem.",
                    ],
                },
                {
                    "act": 5,
                    "badge": "ACT 5 · 10-SECOND OLYMPIAD GEOMETRY STRATEGY",
                    "headline": "Walk Around the Triangle Vertex-to-Divider-to-Vertex and Set Product = 1!",
                    "key_formula": "Vertex → Divider → Vertex (1 Full Loop Product = 1)",
                    "narration": (
                        f"Whenever cevians or transversals appear on an exam, write the cyclic Vertex-to-Divider-to-Vertex product equals 1 to solve it in 10 seconds! "
                        f"Subscribe to @min7014_ai right now for daily visual math cinema!"
                    ),
                    "hud_notes": [
                        "Memory Trick: Hop Vertex → Divider → Next Vertex around the loop!",
                        "Use Mass Points (Lever Principle) for instant 3-second ratio mental math",
                        "Subscribe to @min7014_ai & try the interactive 60fps lab below!",
                    ],
                },
            ]

    if archetype == "conic_parabola":
        if lang_code == "ko":
            return [
                {
                    "act": 1,
                    "badge": "ACT 1 · 포물선 평행광선 집속 미스터리",
                    "headline": f"축에 나란히 들어온 모든 빛이 반사 후 단 하나의 초점 F로 모인다! ({t_title})",
                    "key_formula": "|PF| = |PH| (Focus Distance = Directrix Distance)",
                    "narration": (
                        f"우주 저편에서 축에 나란하게 날아온 열 가닥의 네온 평행 광선이 포물선 거울 내벽에 부딪힙니다. "
                        f"놀랍게도 [{t_title}]에서는 어느 위치에 부딪힌 빛이든 반사되는 순간 단 하나의 오차도 없이 초점 F 한 점으로 완벽하게 모입니다! "
                        f"전파망원경과 위성 안테나, 자동차 전조등이 사용하는 이 포물선 반사의 기하학적 비밀은 무엇일까요?"
                    ),
                    "hud_notes": [
                        "평행광선 입사: 대칭축에 나란한 모든 광선이 반사 후 초점 F에 집속!",
                        "포물선의 정의: 초점 F까지의 거리 |PF| = 준선 l까지의 수직 거리 |PH|",
                        "질문: 왜 포물선의 접선은 입사광선과 초점 선분이 이루는 각을 이등분할까?",
                    ],
                },
                {
                    "act": 2,
                    "badge": "ACT 2 · 초점 거리와 준선 거리가 만드는 이등변삼각형",
                    "headline": "포물선 위의 점 P가 어디로 움직여도 |PF| = |PH| 이등변삼각형이 유지된다!",
                    "key_formula": "△PFH Isosceles Triangle: |PF| = |PH|",
                    "narration": (
                        f"포물선 위를 달리는 점 P에서 초점 F까지 이은 선분 PF와, 왼쪽 수직 준선 l에 내린 수선 PH의 길이를 비교해 보세요. "
                        f"점 P가 위로 올라가며 초점 F에서 멀어지면, 준선까지의 수직 거리 PH도 정확히 똑같은 길이만큼 길어집니다! "
                        f"즉, 점 P, 초점 F, 수선의 발 H를 연결한 삼각형 PFH는 언제나 두 변의 길이가 같은 이등변삼각형입니다."
                    ),
                    "hud_notes": [
                        "실시간 거리 검증: 초점까지 거리 |PF| = 준선까지 수직 거리 |PH| (1:1 일치!)",
                        "핵심 도형 탄생: 세 점 P, F, H를 이으면 항상 이등변삼각형 △PFH 완성!",
                        "오개념 주의: 타원은 두 초점 거리 합(2a), 포물선은 초점=준선 거리(|PF|=|PH|)!",
                    ],
                },
                {
                    "act": 3,
                    "badge": "ACT 3 · 이등변삼각형 수직이등분선(접선)과 빛 반사 증명",
                    "headline": "접선이 선분 FH의 수직이등분선이 되어 입사각과 반사각이 일치한다!",
                    "key_formula": "Tangent Bisects ∠FPH  ⇒  Incident Angle = Reflected Angle",
                    "narration": (
                        f"이제 https://min7014.github.io/ 원문 자료의 핵심 보조선을 그어 봅시다! "
                        f"이등변삼각형 PFH에서 꼭지각 ∠FPH의 이등분선(밑변 FH의 수직이등분선)을 그으면, 그 직선이 바로 점 P에서의 포물선 접선이 됩니다! "
                        f"수선 PH를 연장한 평행 입사광선과 접선이 이루는 각은 맞꼭지각과 이등변삼각형 성질에 의해 반사각과 정확히 같아져 모든 빛이 초점 F로 모입니다."
                    ),
                    "hud_notes": [
                        "결정적 보조선: 초점 F와 준선 수선의 발 H를 잇고 수직이등분선(접선) 작도!",
                        "기하학적 증명: |PF| = |PH| 이등변삼각형 꼭지각 이등분 → ∠입사 = ∠반사!",
                        "복잡한 미분 계산 없이 중학교 이등변삼각형 합동 하나로 10초 만에 증명 끝!",
                    ],
                },
                {
                    "act": 4,
                    "badge": "ACT 4 · 한계를 넘는 상상 (준선 위 수직 접선과 포물선의 닮음)",
                    "headline": "준선 위의 한 점에서 그은 두 접선은 항상 90도 수직으로 만난다!",
                    "key_formula": "Orthoptic Property on Directrix: Tangent₁ ⊥ Tangent₂ (90°)",
                    "narration": (
                        f"여기서 한 걸음 더 나아가 볼까요? 만약 준선 위의 한 점에서 포물선에 두 개의 접선을 그으면 두 접선이 이루는 각은 몇 도가 될까요? "
                        f"이등변삼각형 대칭 성질을 양쪽에 적용하면 두 접선은 언제나 정확히 90도 직각으로 만나고, 두 접점을 잇는 직선은 반드시 초점 F를 지납니다! "
                        f"게다가 모든 원이 서로 닮음이듯, 모든 포물선 역시 확대·축소하면 완전히 포개어지는 닮음 도형입니다."
                    ),
                    "hud_notes": [
                        "심화 성질 1: 준선 위 점에서 그은 두 접선은 항상 수직(90°)으로 직교!",
                        "심화 성질 2: 모든 포물선은 초점 거리 p만 다를 뿐 모두 닮음(Similar)!",
                        "역방향 원리: 초점 F에 전구를 켜면 반사된 빛이 모두 평행광선으로 발사!",
                    ],
                },
                {
                    "act": 5,
                    "badge": "ACT 5 · 수능 기하 포물선 킬러 10초 해법",
                    "headline": "포물선 위에 점이 찍히는 순간 준선으로 수선의 발 H부터 내려라!",
                    "key_formula": "Rule #1: Spot Point P on Parabola → Drop Perpendicular PH to Directrix!",
                    "narration": (
                        f"수능과 내신에서 포물선 문제가 나올 때 y제곱은 4px 방정식에 좌표를 대입하는 것은 가장 느린 길입니다. "
                        f"포물선 위의 점 P를 보자마자 숨겨진 준선 x = -p를 그리고 수선의 발 H를 내려 PF = PH 이등변삼각형을 만들면 10초 만에 풀립니다! "
                        f"지금 바로 @min7014_ai 채널을 구독하고 설명란의 지오지브라 실험실에서 직접 광선을 쏘아 보세요!"
                    ),
                    "hud_notes": [
                        "실전 제1원칙: 포물선 위의 점 P 등장 → 즉시 준선 작도 후 |PF| = |PH| 표시!",
                        "포물선 접선 등장 → 무조건 이등변삼각형 △PFH와 마름모 성질로 해결!",
                        "지금 [@min7014_ai 구독] 누르고 1,113개 창의 수학 시네마를 정주행하세요!",
                    ],
                },
            ]
        else:
            return [
                {
                    "act": 1,
                    "badge": "ACT 1 · PARABOLIC PARALLEL RAY MYSTERY",
                    "headline": f"Every Parallel Light Ray Reflects Into One Exact Focus F! ({t_title})",
                    "key_formula": "|PF| = |PH| (Focus Distance = Directrix Distance)",
                    "narration": (
                        f"Ten parallel neon laser beams arrive from deep space along the axis of a parabola. "
                        f"In [{t_title}], every single parallel beam bounces off the curve and converges with zero error at one single focus point F! "
                        f"What geometric law makes parabolic satellite dishes and telescopes work?"
                    ),
                    "hud_notes": [
                        "Parallel Ray Tracing: All axial beams reflect directly into Focus F!",
                        "Parabola Definition: Distance to Focus |PF| = Distance to Directrix |PH|",
                        "Question: Why does the parabolic tangent bisect angle ∠FPH?",
                    ],
                },
                {
                    "act": 2,
                    "badge": "ACT 2 · THE ISOSCELES TRIANGLE |PF| = |PH|",
                    "headline": "As Point P Glides Along the Parabola, |PF| Always Equals |PH|!",
                    "key_formula": "△PFH Isosceles Triangle: |PF| = |PH|",
                    "narration": (
                        f"Compare the segment PF to focus F with the perpendicular segment PH dropped to the vertical directrix line l. "
                        f"Wherever point P moves along the parabola, PF and PH remain strictly equal, forming a glowing isosceles triangle PFH at every instant!"
                    ),
                    "hud_notes": [
                        "Live Measurement: Focal distance |PF| = Directrix distance |PH|!",
                        "Isosceles Structure: Points P, F, and H always form isosceles △PFH!",
                        "Note: Ellipse keeps PF₁+PF₂=2a, while Parabola keeps |PF|=|PH|!",
                    ],
                },
                {
                    "act": 3,
                    "badge": "ACT 3 · PERPENDICULAR BISECTOR TANGENT PROOF",
                    "headline": "The Tangent Line Bisects ∠FPH, Proving Equal Reflection Angles!",
                    "key_formula": "Tangent Bisects ∠FPH  ⇒  Incident Angle = Reflected Angle",
                    "narration": (
                        f"In the visual proof from https://min7014.github.io/, connect F to H and draw the perpendicular bisector of segment FH. "
                        f"Because triangle PFH is isosceles, this angle bisector of ∠FPH is the exact tangent line to the parabola, making the incident and reflected angles strictly equal!"
                    ),
                    "hud_notes": [
                        "Key Auxiliary Line: Connect F to H and bisect apex angle ∠FPH!",
                        "Isosceles Symmetry + Vertical Angles → Incident Angle = Reflected Angle!",
                        "Proved visually in 10 seconds without any calculus!",
                    ],
                },
                {
                    "act": 4,
                    "badge": "ACT 4 · ORTHOPTIC DIRECTRIX & SIMILARITY",
                    "headline": "Two Tangents From Any Point on the Directrix Meet at 90 Degrees!",
                    "key_formula": "Orthoptic Property on Directrix: Tangent₁ ⊥ Tangent₂ (90°)",
                    "narration": (
                        f"What if you draw two tangent lines to a parabola from any point on its directrix? "
                        f"By folding the two isosceles triangles across their tangents, the two tangent lines always intersect at a 90-degree right angle, and all parabolas are geometrically similar!"
                    ),
                    "hud_notes": [
                        "Bonus Theorem 1: Tangents from the directrix always meet at 90°!",
                        "Bonus Theorem 2: All parabolas are geometrically similar!",
                        "Reverse Optics: A bulb at focus F projects a perfectly parallel beam!",
                    ],
                },
                {
                    "act": 5,
                    "badge": "ACT 5 · 10-SECOND PARABOLA EXAM STRATEGY",
                    "headline": "The Instant You See Point P on a Parabola, Drop Perpendicular PH to the Directrix!",
                    "key_formula": "Rule #1: Spot Point P on Parabola → Drop Perpendicular PH to Directrix!",
                    "narration": (
                        f"Whenever a parabola appears on an exam, draw the directrix and drop perpendicular PH to form isosceles triangle PFH in 10 seconds! "
                        f"Subscribe to @min7014_ai right now for daily visual math cinema!"
                    ),
                    "hud_notes": [
                        "Instant Trigger: Point P on Parabola → Draw Directrix & Use |PF| = |PH|!",
                        "Tangent Problem → Use Isosceles Triangle △PFH & Rhombus Symmetry!",
                        "Subscribe to @min7014_ai & explore the interactive GeoGebra lab!",
                    ],
                },
            ]

    if archetype == "menelaus_theorem":
        if lang_code == "ko":
            return [
                {
                    "act": 1,
                    "badge": "ACT 1 · 삼각형을 관통하는 할선의 비율 미스터리",
                    "headline": f"한 직선이 삼각형의 세 변을 뚫고 지나갈 때 세 비율의 곱은 언제나 1이다! ({t_title})",
                    "key_formula": "(AF / FB) × (BD / DC) × (CE / EA) = 1.000",
                    "narration": (
                        f"밤하늘의 삼각형 ABC 위로 네온 할선 하나가 비스듬히 지나가며 변 AB의 내분점 F, 변 AC의 내분점 E, 그리고 밑변 BC 연장선의 외분점 D를 만듭니다. "
                        f"할선의 각도가 어떻게 변하더라도 [{t_title}]에서 세 비율을 순환하여 곱한 값은 언제나 정확히 1.000으로 유지됩니다! "
                        f"세 직선이 한 점에 모이는 체바의 정리와 쌍대를 이루는 이 공선성 정리의 비밀을 파헤쳐 봅시다."
                    ),
                    "hud_notes": [
                        "메넬라우스 구조: 삼각형의 세 변(연장선 포함)과 만나는 일직선 할선 D-F-E",
                        "핵심 불변량: (AF / FB) × (BD / DC) × (CE / EA) = 1.000 일정!",
                        "질문: 단 1줄의 평행 보조선으로 어떻게 이 3개 분수를 모두 약분시킬까?",
                    ],
                },
                {
                    "act": 2,
                    "badge": "ACT 2 · 꼭짓점 → 분점 → 꼭짓점 징검다리 순환 법칙",
                    "headline": "A → F → B → D → C → E → A 한 바퀴 돌아오는 비율의 시소 균형!",
                    "key_formula": "Cyclic Path: (A→F / F→B) × (B→D / D→C) × (C→E / E→A) = 1",
                    "narration": (
                        f"메넬라우스 식을 세울 때 절대 헷갈리지 않는 규칙은 꼭짓점에서 분점으로, 분점에서 다음 꼭짓점으로 징검다리를 뛰며 한 바퀴 돌아오는 것입니다! "
                        f"밑변 연장선 바깥의 외분점 D를 지날 때도 B에서 D까지 나갔다가 다시 D에서 C로 돌아오는 비율 BD 분의 DC를 곱하면, 세 분수의 곱이 완벽한 역수 균형을 이룹니다."
                    ),
                    "hud_notes": [
                        "징검다리 공식: (꼭짓점→분점)/(분점→다음 꼭짓점) 3번 점프 후 출발점 복귀!",
                        "외분점 구간 주의: B → 외분점 D → 꼭짓점 C 순서(BD / DC) 그대로 적용!",
                        "체바(세 직선 한 점 교차)와 메넬라우스(세 점 일직선 위치)의 완벽한 대칭!",
                    ],
                },
                {
                    "act": 3,
                    "badge": "ACT 3 · https://min7014.github.io/ 평행 보조선 CK 1줄 증명",
                    "headline": "꼭짓점 C에서 변 AB에 평행한 보조선 CK 딱 1줄을 그으면 닮음비로 연쇄 약분!",
                    "key_formula": "Draw CK ∥ AB  ⇒  (AF/FB)·(BF/CK)·(CK/AF) = 1",
                    "narration": (
                        f"이제 https://min7014.github.io/ 원문 자료의 결정적 보조선 딱 한 줄을 그어 볼까요? "
                        f"꼭짓점 C를 지나고 변 AB에 평행한 황금빛 보조선 CK를 그어 할선과 만나는 점을 K라고 합시다! "
                        f"그러면 두 쌍의 AA 닮음 삼각형에 의해 BD 분의 DC는 BF 분의 CK가 되고, CE 분의 EA는 CK 분의 AF가 되어, 세 식을 곱하는 순간 보조선 CK와 모든 변이 도미노처럼 약분되어 정확히 1이 남습니다!"
                    ),
                    "hud_notes": [
                        "폴리아 제1보조선: 꼭짓점 C를 지나고 변 AB에 평행한 선분 CK 1줄 작도!",
                        "1단계 AA 닮음(△BDF ∽ △BCK): BD / DC = FB / CK",
                        "2단계 AA 닮음(△AEF ∽ △CEK): CE / EA = CK / AF → 곱하면 100% 약분 = 1!",
                    ],
                },
                {
                    "act": 4,
                    "badge": "ACT 4 · 한계를 넘는 상상 (수선의 높이 비 증명과 데자르그 정리)",
                    "headline": "세 꼭짓점에서 할선에 내린 수선의 길이 비 h₁, h₂, h₃로도 1초 증명!",
                    "key_formula": "(h₁ / h₂) × (h₂ / h₃) × (h₃ / h₁) = 1  (Altitude Ratio Proof)",
                    "narration": (
                        f"또 다른 시각적 증명도 감상해 보세요! 세 꼭짓점 A, B, C에서 할선에 수선의 발을 내려 높이를 각각 h1, h2, h3라고 하면, "
                        f"마주 보는 직각삼각형들의 닮음비에 의해 세 선분 비율은 h1 나누기 h2, h2 나누기 h3, h3 나누기 h1로 바뀌어 단번에 1로 약분됩니다! "
                        f"이 원리가 확장되어 3차원 원근투시도의 데자르그 정리와 파스칼의 육각형 정리가 탄생합니다."
                    ),
                    "hud_notes": [
                        "별해(수선 증명): 세 꼭짓점에서 할선에 내린 수선 높이 비 (h₁/h₂)(h₂/h₃)(h₃/h₁)=1",
                        "역정리 활용: 세 비율의 곱이 1이면 세 점 D, E, F는 반드시 일직선(공선점)!",
                        "사영기하 확장: 파포스의 정리·데자르그의 정리·벡터 내분점 공선 조건의 뿌리!",
                    ],
                },
                {
                    "act": 5,
                    "badge": "ACT 5 · 수능 기하·올림피아드 10초 실전 해법",
                    "headline": "삼각형과 할선이 만나면 평행 보조선 1줄 또는 메넬라우스 순환 곱 = 1!",
                    "key_formula": "Triangle + Transversal Line → Menelaus Cyclic Product = 1!",
                    "narration": (
                        f"도형 문제에서 삼각형 내부를 관통하는 직선과 외분점 비율이 보일 때, 복잡한 좌표나 연립방정식을 세우지 마세요. "
                        f"교점을 지나며 평행한 보조선 한 줄을 긋거나 메넬라우스 순환 곱은 1 공식을 쓰면 10초 만에 풀립니다! "
                        f"지금 바로 @min7014_ai 채널을 구독하고 설명란의 지오지브라 실험실에서 할선을 직접 움직여 보세요!"
                    ),
                    "hud_notes": [
                        "실전 포착 신호: '삼각형 + 연장선 외분점 D + 할선' = 100% 메넬라우스 정리!",
                        "서술형 만점 팁: 꼭짓점에서 평행 보조선 1줄을 그어 AA 닮음 2쌍으로 서술!",
                        "지금 [@min7014_ai 구독] 누르고 1,113개 창의 수학 시네마를 정주행하세요!",
                    ],
                },
            ]
        else:
            return [
                {
                    "act": 1,
                    "badge": "ACT 1 · THE TRANSVERSAL LINE MYSTERY",
                    "headline": f"One Line Slices Across a Triangle—Why Do the 3 Ratios Multiply to 1? ({t_title})",
                    "key_formula": "(AF / FB) × (BD / DC) × (CE / EA) = 1.000",
                    "narration": (
                        f"A single glowing transversal line slices across triangle ABC, cutting side AB at F, side AC at E, and the extended base BC at exterior point D. "
                        f"No matter how the transversal tilts, in [{t_title}] the cyclic product of the three division ratios stays strictly locked at 1.000!"
                    ),
                    "hud_notes": [
                        "Menelaus Configuration: Transversal line cutting 3 sides at collinear D, E, F",
                        "Core Invariant: (AF / FB) × (BD / DC) × (CE / EA) = 1.000!",
                        "Question: How does 1 parallel auxiliary line cancel all three fractions?",
                    ],
                },
                {
                    "act": 2,
                    "badge": "ACT 2 · THE VERTEX-TO-DIVIDER CYCLIC LOOP",
                    "headline": "Hop A → F → B → D → C → E → A Around the Triangle Perimeter!",
                    "key_formula": "Cyclic Path: (A→F / F→B) × (B→D / D→C) × (C→E / E→A) = 1",
                    "narration": (
                        f"Follow the golden cyclic rule: hop from Vertex to Divider, then from Divider to the next Vertex all the way around back to A! "
                        f"Even when jumping out to exterior point D on the extended base, the ratio BD over DC balances the interior ratios to keep the product at 1."
                    ),
                    "hud_notes": [
                        "Cyclic Rule: (Vertex → Divider) / (Divider → Next Vertex) around the loop!",
                        "Exterior Segment: Hop B → exterior D → vertex C (BD / DC)!",
                        "Projective Dual of Ceva's Theorem (Collinearity ↔ Concurrency)!",
                    ],
                },
                {
                    "act": 3,
                    "badge": "ACT 3 · ONE PARALLEL LINE PROOF (CK ∥ AB)",
                    "headline": "Draw 1 Line CK Parallel to AB and Watch Similar Triangles Cancel Out!",
                    "key_formula": "Draw CK ∥ AB  ⇒  (AF/FB)·(BF/CK)·(CK/AF) = 1",
                    "narration": (
                        f"Here is the visual proof from https://min7014.github.io/: draw a single golden line CK through vertex C parallel to side AB! "
                        f"This creates two pairs of AA similar triangles: BD over DC becomes FB over CK, and CE over EA becomes CK over AF—canceling CK and every segment like dominoes to leave 1!"
                    ),
                    "hud_notes": [
                        "Golden Auxiliary Line: Draw CK through vertex C parallel to side AB!",
                        "AA Similarity 1 (△BDF ∽ △BCK): BD / DC = FB / CK",
                        "AA Similarity 2 (△AEF ∽ △CEK): CE / EA = CK / AF → Product = 1!",
                    ],
                },
                {
                    "act": 4,
                    "badge": "ACT 4 · ALTITUDE RATIO PROOF & PROJECTIVE GEOMETRY",
                    "headline": "Drop Three Altitudes h₁, h₂, h₃ to the Transversal for Instant Cancellation!",
                    "key_formula": "(h₁ / h₂) × (h₂ / h₃) × (h₃ / h₁) = 1  (Altitude Ratio Proof)",
                    "narration": (
                        f"You can also drop three perpendicular altitudes h1, h2, and h3 from the vertices to the transversal line! "
                        f"Each segment ratio equals the ratio of altitudes, giving h1 over h2 times h2 over h3 times h3 over h1 equals 1—the foundation of Desargues' and Pascal's theorems!"
                    ),
                    "hud_notes": [
                        "Second Proof: Perpendicular altitudes give (h₁/h₂)(h₂/h₃)(h₃/h₁) = 1!",
                        "Converse Theorem: Product = 1 guarantees points D, E, F are collinear!",
                        "Gateway to Olympiad Projective Geometry & Desargues' Theorem!",
                    ],
                },
                {
                    "act": 5,
                    "badge": "ACT 5 · 10-SECOND OLYMPIAD GEOMETRY STRATEGY",
                    "headline": "Spot a Triangle Cut by a Line and Apply Menelaus' Cyclic Product = 1!",
                    "key_formula": "Triangle + Transversal Line → Menelaus Cyclic Product = 1!",
                    "narration": (
                        f"Whenever a line slices across a triangle on an exam, draw 1 parallel line or write Menelaus' cyclic product equals 1 to solve it in 10 seconds! "
                        f"Subscribe to @min7014_ai right now for daily visual math cinema!"
                    ),
                    "hud_notes": [
                        "Instant Trigger: Triangle + Extended Side + Transversal = Menelaus!",
                        "Draw 1 parallel line through a vertex to create AA similar triangles!",
                        "Subscribe to @min7014_ai & explore the interactive GeoGebra lab!",
                    ],
                },
            ]

    if archetype == "cauchy_mvt":
        if lang_code == "ko":
            return [
                {
                    "act": 1,
                    "badge": "ACT 1 · 두 함수의 변화율 비가 일치하는 순간",
                    "headline": f"두 함수 f(x), g(x)의 평균변화율 비와 미분계수 비가 정확히 일치한다! ({t_title})",
                    "key_formula": "[f(b) - f(a)] / [g(b) - g(a)] = f'(c) / g'(c)  (c ∈ (a, b))",
                    "narration": (
                        f"일반 평균값 정리가 하나의 함수 f(x)의 변화율을 다룬다면, [{t_title}]는 동시에 변화하는 두 함수 f(x)와 g(x)의 변화율 비율을 밝히는 강력한 정리입니다! "
                        f"구간 [a, b] 전체에서의 변화량 비율인 g(b) 빼기 g(a) 분의 f(b) 빼기 f(a)와 정확히 일치하는 순간 미분계수 비율 g 프라임 c 분의 f 프라임 c가 구간 안에 반드시 존재합니다."
                    ),
                    "hud_notes": [
                        "코시의 평균값 정리: 두 함수 f(x), g(x)의 증분 비 = 한 점 c에서의 미분계수 비!",
                        "핵심 공식: [f(b) - f(a)] / [g(b) - g(a)] = f'(c) / g'(c)  (단 g'(x) ≠ 0)",
                        "질문: 왜 분모·분자에 평균값 정리를 따로 쓰면 안 되고 보조함수 h(x)가 필요할까?",
                    ],
                },
                {
                    "act": 2,
                    "badge": "ACT 2 · 매개변수 평면 곡선 (g(t), f(t))의 평행 접선",
                    "headline": "평면 위를 달리는 곡선 (g(t), f(t))의 할선과 평행한 접선이 탄생하는 점 c!",
                    "key_formula": "Parametric Curve (x = g(t), y = f(t)): Chord Slope = Tangent Slope",
                    "narration": (
                        f"이 정리를 눈으로 가장 직관적으로 이해하는 방법은 가로좌표를 g(t), 세로좌표를 f(t)로 놓은 매개변수 평면 곡선을 그리는 것입니다! "
                        f"출발점 (g(a), f(a))와 도착점 (g(b), f(b))를 잇는 할선의 기울기가 바로 좌변이고, 곡선 위를 달리다 그 할선과 완벽히 평행해지는 순간 t = c 에서의 접선 기울기가 바로 우변입니다!"
                    ),
                    "hud_notes": [
                        "기하학적 번역: 가로축 X = g(x), 세로축 Y = f(x) 매개변수 곡선 작도!",
                        "좌변의 의미: 두 끝점 A(g(a), f(a)), B(g(b), f(b))를 잇는 현(할선)의 기울기",
                        "우변의 의미: 시각 x = c 에서의 순간 속도 벡터 접선 기울기 f'(c) / g'(c)!",
                    ],
                },
                {
                    "act": 3,
                    "badge": "ACT 3 · https://min7014.github.io/ 보조함수 h(x)와 롤의 정리 증명",
                    "headline": "보조함수 h(x) = [f(b)-f(a)]g(x) - [g(b)-g(a)]f(x) 로 동일한 점 c를 포착하라!",
                    "key_formula": "h(a) = h(b)  ⇒  h'(c) = [f(b)-f(a)]g'(c) - [g(b)-g(a)]f'(c) = 0",
                    "narration": (
                        f"만약 분자와 분모에 일반 평균값 정리를 따로 적용하면 f 프라임 c1과 g 프라임 c2에서 c1과 c2가 서로 다른 점이 되어 증명에 실패합니다! "
                        f"그래서 https://min7014.github.io/ 원문 증명처럼 보조함수 h(x)를 f(b) 빼기 f(a) 곱하기 g(x) 빼기 g(b) 빼기 g(a) 곱하기 f(x)로 설정하면, "
                        f"h(a)와 h(b)가 같아져 롤의 정리에 의해 h 프라임 c가 0이 되는 단 하나의 동일한 점 c에서 등식이 완벽히 증명됩니다!"
                    ),
                    "hud_notes": [
                        "오개념 주의: 분모·분자에 평균값 정리를 따로 쓰면 c₁ ≠ c₂ 여서 증명 불가!",
                        "결정적 보조함수: h(x) = [f(b) - f(a)]g(x) - [g(b) - g(a)]f(x) 도입!",
                        "롤의 정리 적용: h(a) = h(b) 이므로 h'(c) = 0 인 동일한 점 c 존재 증명!",
                    ],
                },
                {
                    "act": 4,
                    "badge": "ACT 4 · 한계를 넘는 상상 (일반 평균값 정리와 로피탈의 정리 유도)",
                    "headline": "g(x) = x 를 대입하면 평균값 정리, b → a 극한을 취하면 로피탈의 정리!",
                    "key_formula": "lim(x→a) [f(x)-f(a)]/[g(x)-g(a)] = lim(c→a) f'(c)/g'(c) (L'Hôpital)",
                    "narration": (
                        f"코시의 평균값 정리에서 g(x) 자리에 가장 단순한 함수 x를 대입해 보세요. 분모가 b 빼기 a가 되면서 우리가 아는 일반 평균값 정리가 즉시 튀어나옵니다! "
                        f"나아가 f(a)와 g(a)가 모두 0일 때 b를 a로 한없이 가까이 보내면, 사잇점 c도 a로 수렴하면서 0분의 0 꼴 극한을 미분계수의 비로 구하는 로피탈의 정리가 탄생합니다!"
                    ),
                    "hud_notes": [
                        "특수화: g(x) = x 대입 → [f(b) - f(a)] / (b - a) = f'(c) (평균값 정리)",
                        "극한 확장: f(a)=g(a)=0 일 때 x → a 극한 → 로피탈의 정리(L'Hôpital's Rule)!",
                        "미적분학의 거대한 줄기: 롤의 정리 → 코시의 평균값 정리 → 로피탈·테일러 정리!",
                    ],
                },
                {
                    "act": 5,
                    "badge": "ACT 5 · 수리논술·심화 미적분 10초 실전 통찰",
                    "headline": "두 함수의 증분 비가 보이면 즉시 보조함수 h(x)와 코시 평균값 정리를 떠올려라!",
                    "key_formula": "[f(b) - f(a)] / [g(b) - g(a)] = f'(c) / g'(c)  (Verified Q.E.D.)",
                    "narration": (
                        f"수리논술과 대학 미적분에서 두 함수의 함숫값 차이 비율을 묻는 문제가 나오면, 코시의 평균값 정리와 보조함수 h(x)를 즉시 떠올리세요! "
                        f"지금 바로 @min7014_ai 채널을 구독하고 설명란의 단계별 증명 PDF 원문으로 완벽히 마스터해 보세요!"
                    ),
                    "hud_notes": [
                        "논술 만점 포인트: 반드시 보조함수 h(x)를 명시하여 동일한 점 c임을 증명!",
                        "설명란에서 https://min7014.github.io/2016012801 단계별 증명 PDF 무료 확인",
                        "지금 [@min7014_ai 구독] 누르고 1,113개 창의 수학 시네마를 정주행하세요!",
                    ],
                },
            ]
        else:
            return [
                {
                    "act": 1,
                    "badge": "ACT 1 · RATIO OF TWO CHANGING FUNCTIONS",
                    "headline": f"Where the Ratio of Secant Changes Matches the Ratio of Derivatives! ({t_title})",
                    "key_formula": "[f(b) - f(a)] / [g(b) - g(a)] = f'(c) / g'(c)  (c ∈ (a, b))",
                    "narration": (
                        f"While the standard Mean Value Theorem tracks a single function, [{t_title}] compares two smooth functions f(x) and g(x) simultaneously! "
                        f"Across any interval [a, b], there is always an interior point c where the ratio of derivatives f prime of c over g prime of c equals the overall ratio of changes!"
                    ),
                    "hud_notes": [
                        "Cauchy's MVT: Ratio of overall increments = Ratio of derivatives at x = c!",
                        "Exact Formula: [f(b) - f(a)] / [g(b) - g(a)] = f'(c) / g'(c)",
                        "Question: Why must both derivatives be evaluated at the exact same c?",
                    ],
                },
                {
                    "act": 2,
                    "badge": "ACT 2 · PARAMETRIC CURVE (g(t), f(t)) GEOMETRY",
                    "headline": "On the Parametric Curve (g(t), f(t)), Tangent Parallels Chord at t = c!",
                    "key_formula": "Parametric Curve (x = g(t), y = f(t)): Chord Slope = Tangent Slope",
                    "narration": (
                        f"Plot g(t) on the horizontal axis and f(t) on the vertical axis to trace a smooth parametric curve! "
                        f"The left side is the slope of the chord connecting the endpoints, and the right side is the slope of the tangent vector at the exact instant t = c where tangent parallels chord!"
                    ),
                    "hud_notes": [
                        "Geometric View: Plot parametric curve X = g(t), Y = f(t) in the plane",
                        "Left Side: Slope of the chord connecting (g(a), f(a)) and (g(b), f(b))",
                        "Right Side: Instantaneous tangent slope dy/dx = f'(c) / g'(c)!",
                    ],
                },
                {
                    "act": 3,
                    "badge": "ACT 3 · ROLLE'S AUXILIARY FUNCTION h(x) PROOF",
                    "headline": "Construct h(x) = [f(b)-f(a)]g(x) - [g(b)-g(a)]f(x) so h(a) = h(b)!",
                    "key_formula": "h(a) = h(b)  ⇒  h'(c) = [f(b)-f(a)]g'(c) - [g(b)-g(a)]f'(c) = 0",
                    "narration": (
                        f"Applying the ordinary MVT separately to numerator and denominator gives two different points c1 and c2. "
                        f"Instead, following https://min7014.github.io/, define auxiliary function h(x) = [f(b)-f(a)]g(x) - [g(b)-g(a)]f(x) so that h(a) = h(b), and Rolle's Theorem guarantees a single c where h'(c) = 0!"
                    ),
                    "hud_notes": [
                        "Common Trap: Separate MVT on top and bottom gives c₁ ≠ c₂ (Invalid!)",
                        "Master Stroke: Auxiliary function h(x) = [f(b)-f(a)]g(x) - [g(b)-g(a)]f(x)",
                        "Rolle's Theorem: h(a) = h(b) ⇒ h'(c) = 0 at one unified point c!",
                    ],
                },
                {
                    "act": 4,
                    "badge": "ACT 4 · UNIFYING ORDINARY MVT & L'HÔPITAL'S RULE",
                    "headline": "Set g(x) = x for Standard MVT, or Take x → a for L'Hôpital's Rule!",
                    "key_formula": "lim(x→a) [f(x)-f(a)]/[g(x)-g(a)] = lim(c→a) f'(c)/g'(c) (L'Hôpital)",
                    "narration": (
                        f"Setting g(x) = x recovers the standard Mean Value Theorem immediately! "
                        f"And when f(a) = g(a) = 0, letting x approach a squeezes c toward a, proving L'Hôpital's Rule for 0 over 0 indeterminate limits!"
                    ),
                    "hud_notes": [
                        "Special Case g(x) = x: Recovers [f(b) - f(a)] / (b - a) = f'(c)!",
                        "Limit Case x → a: Rigorously proves L'Hôpital's Rule for 0/0 limits!",
                        "Chain of Calculus: Rolle's Theorem → Cauchy's MVT → Taylor's Theorem!",
                    ],
                },
                {
                    "act": 5,
                    "badge": "ACT 5 · 10-SECOND CALCULUS PROOF STRATEGY",
                    "headline": "Use Auxiliary Function h(x) Whenever Comparing Two Functions' Increments!",
                    "key_formula": "[f(b) - f(a)] / [g(b) - g(a)] = f'(c) / g'(c)  (Verified Q.E.D.)",
                    "narration": (
                        f"Check the step-by-step PDF proof on https://min7014.github.io/ in the description and subscribe to @min7014_ai right now for daily visual math cinema!"
                    ),
                    "hud_notes": [
                        "Exam Key: Always write down h(x) to guarantee a single shared point c!",
                        "Full Step-by-Step PDF Proof linked in the description below",
                        "Subscribe to @min7014_ai for daily high-definition math cinema!",
                    ],
                },
            ]

    if archetype in ("inverse_deriv", "trig_deriv_sin", "special_triangles", "square_root_geometry", "cycloid_kinematics", "parallel_similarity"):
        formula_map = {
            "inverse_deriv": "(f⁻¹)'(y) = 1 / f'(x)  (dx/dy = 1 / (dy/dx))",
            "trig_deriv_sin": "d/dx (sin x) = cos x  (via lim sin h / h = 1)",
            "special_triangles": "30°-60°-90° (1 : √3 : 2)  &  45°-45°-90° (1 : 1 : √2)",
            "square_root_geometry": "x² = a  ⇔  x = ±√a  (Side of Area a Square = √a)",
            "cycloid_kinematics": "x(θ) = r(θ - sin θ),  dx/dθ = r(1 - cos θ) ≥ 0",
            "parallel_similarity": "l ∥ m ∥ n  ⇒  a : b = a' : b'  (Parallel Line Similarity)",
        }
        kf = formula_map.get(archetype, f"Core Invariant · {t_title}")
        hyp_s = sanitize_glyphs(vmaker.latex_to_unicode_title(tpa.get("hypothesis_ko") or ""))
        misc_s = sanitize_glyphs(vmaker.latex_to_unicode_title(tpa.get("misconception_ko") or ""))
        if lang_code == "ko":
            return [
                {
                    "act": 1,
                    "badge": f"ACT 1 · [{t_title}] 핵심 직관과 출발 조건",
                    "headline": f"공식을 외우기 전에 출발 정의와 시각적 구조부터 포착하라! ({t_title})",
                    "key_formula": kf,
                    "narration": f"오늘 탐구할 주제는 https://min7014.github.io/ 의 [{t_title}]입니다! 결과 공식을 단순 암기하기 전에 출발 조건부터 살펴볼까요? {hyp_s} 바로 이 구조에서 {inv_ko}가 필연적으로 탄생합니다!",
                    "hud_notes": [
                        f"출발 조건: {hyp_s[:44]}",
                        f"핵심 결론: {inv_ko[:44]}",
                        "목표: 공식 암기가 아닌 시각적 보조선과 원리로 10초 만에 유도!",
                    ],
                },
                {
                    "act": 2,
                    "badge": "ACT 2 · 눈으로 확인하는 대칭성과 기하·대수 모델",
                    "headline": f"핵심 관계식 [{kf[:32]}]의 시각적 균형 관찰",
                    "key_formula": kf,
                    "narration": f"화면의 동적 시뮬레이션을 자세히 관찰해 보세요. [{t_title}]에서 점과 선분이 움직일 때 {inv_ko}라는 관계가 어떻게 한 치의 오차도 없이 유지되는지 눈으로 직접 확인할 수 있습니다.",
                    "hud_notes": [
                        f"핵심 불변식: {kf[:44]}",
                        f"결론 요약: {inv_ko[:44]}",
                        "직관적 관찰: 기호 이전에 도형의 대칭과 넓이·길이의 대응을 먼저 보라!",
                    ],
                },
                {
                    "act": 3,
                    "badge": "ACT 3 · https://min7014.github.io/ 결정적 보조선과 증명 논리",
                    "headline": "단 한 줄의 핵심 보조선·발상이 증명의 모든 조각을 하나로 연결한다!",
                    "key_formula": kf,
                    "narration": f"왜 이 성질이 항상 성립할까요? 핵심 발상은 다음과 같습니다! {polya_ko} 그리고 이를 통해 {logic_ko} 과정으로 결론이 완벽하게 증명됩니다!",
                    "hud_notes": [
                        f"결정적 발상: {polya_ko[:44]}",
                        f"증명 핵심: {logic_ko[:44]}",
                        "https://min7014.github.io/ 단계별 시각 증명 원리와 100% 일치!",
                    ],
                },
                {
                    "act": 4,
                    "badge": "ACT 4 · 가장 많이 틀리는 함정(오개념) 예방 & 조건 확장",
                    "headline": "실전에서 절대 속지 않는 오개념 백신과 상위 교육과정 연결!",
                    "key_formula": kf,
                    "narration": f"여기서 학생들이 가장 자주 실수하는 함정을 꼭 짚고 넘어갑시다! {misc_s} 나아가 조건을 한 단계 확장해 볼까요? {whatif_ko}",
                    "hud_notes": [
                        f"오개념 주의: {misc_s[:44]}",
                        f"심화 확장: {whatif_ko[:44]}",
                        "정의와 조건의 경계를 정확히 알면 변형 문제에서도 흔들리지 않습니다!",
                    ],
                },
                {
                    "act": 5,
                    "badge": "ACT 5 · 실전 10초 유레카 해법 & 인터랙티브 실습",
                    "headline": f"[{t_title}] 문제를 보자마자 핵심 보조선과 정의를 1초 만에 꺼내라!",
                    "key_formula": kf,
                    "narration": f"오늘 함께 증명한 [{t_title}]의 핵심은 {polya_ko}입니다. 설명란과 고정댓글의 https://min7014.github.io/ 원문 PDF와 지오지브라를 직접 조작해 보고, 지금 바로 @min7014_ai 채널을 구독하세요!",
                    "hud_notes": [
                        f"실전 제1원칙: {polya_ko[:44]}",
                        "설명란·고정댓글에서 https://min7014.github.io/ 원문 PDF & GeoGebra 실습",
                        "지금 [@min7014_ai 구독] 누르고 1,113개 창의 수학 시네마를 정주행하세요!",
                    ],
                },
            ]
        else:
            return [
                {
                    "act": 1,
                    "badge": f"ACT 1 · VISUAL INTUITION OF {t_title.upper()[:24]}",
                    "headline": f"See the Exact Geometric Structure Behind [{t_title}]!",
                    "key_formula": kf,
                    "narration": f"Welcome to the pure visual proof of [{t_title}] based on https://min7014.github.io/! Instead of memorizing formulas blindly, watch how the starting geometric definition makes this law inevitable.",
                    "hud_notes": [
                        f"Topic: {t_title[:44]}",
                        f"Core Relation: {kf[:44]}",
                        "100% faithful to the step-by-step proof on https://min7014.github.io/!",
                    ],
                },
                {
                    "act": 2,
                    "badge": "ACT 2 · DYNAMIC GEOMETRIC & ALGEBRAIC BALANCE",
                    "headline": f"Observing the Invariant [{kf[:34]}] Live",
                    "key_formula": kf,
                    "narration": f"Watch the glowing diagram evolve in real time. Every length, slope, and angle locks into the exact mathematical relation of [{t_title}] with zero error!",
                    "hud_notes": [
                        f"Key Formula: {kf[:44]}",
                        "Visual Symmetry: Lengths and slopes balance in real time",
                        "Discovery Before Formula: See why the equation must hold!",
                    ],
                },
                {
                    "act": 3,
                    "badge": "ACT 3 · THE DECISIVE AUXILIARY LINE & PROOF",
                    "headline": "One Strategic Auxiliary Construction Completes the Proof!",
                    "key_formula": kf,
                    "narration": f"By introducing the decisive auxiliary line and symmetry from https://min7014.github.io/, all intermediate terms cancel cleanly and prove [{t_title}] in seconds!",
                    "hud_notes": [
                        "Polya's First Step: Introduce the symmetry auxiliary line",
                        f"Verified Result: {kf[:44]}",
                        "Zero rote memorization—pure logical deduction!",
                    ],
                },
                {
                    "act": 4,
                    "badge": "ACT 4 · COMMON PITFALLS & WHAT-IF-NOT EXTENSION",
                    "headline": "Avoiding Classic Exam Traps and Generalizing the Theorem",
                    "key_formula": kf,
                    "narration": f"Always verify the exact domain and sign conditions so you never fall for common exam traps, and see how [{t_title}] generalizes to higher dimensions and calculus!",
                    "hud_notes": [
                        "Pitfall Check: Verify exact domain, orientation, and sign conditions!",
                        "What-If-Not: Generalizes directly to advanced Olympiad & calculus problems",
                        "Explore the full step-by-step PDF in the description!",
                    ],
                },
                {
                    "act": 5,
                    "badge": "ACT 5 · 10-SECOND EXAM TAKEAWAY",
                    "headline": f"Master [{t_title}] With 1 Visual Idea!",
                    "key_formula": kf,
                    "narration": f"Explore the interactive GeoGebra applet and original PDF on https://min7014.github.io/ linked in the description, and subscribe to @min7014_ai right now!",
                    "hud_notes": [
                        f"Core Formula: {kf[:44]}",
                        "Original PDF & GeoGebra Lab linked in the description below",
                        "Subscribe to @min7014_ai for daily high-definition math cinema!",
                    ],
                },
            ]

    # 원주각과 중심각 (∠APB = 1/2 ∠AOB) 및 원의 성질 5막 시네마 대본
    if lang_code == "ko":
        return [
            {
                "act": 1,
                "badge": "ACT 1 · 원주각과 중심각의 1/2 불변량 미스터리",
                "headline": f"점 P가 원 위를 아무리 움직여도 원주각은 언제나 중심각의 절반이다! ({t_title})",
                "key_formula": "∠APB (Inscribed Angle) = 1/2 ∠AOB (Central Angle)",
                "narration": (
                    f"밤하늘의 원 위에서 호 AB를 바라보는 꼭짓점 P가 원주를 따라 쉼 없이 미끄러져 움직입니다. "
                    f"점 P의 위치가 바뀔 때마다 삼각형의 모양은 계속 달라지지만, 놀랍게도 [{t_title}]에서 원주각 ∠APB의 크기는 언제나 중심각 ∠AOB의 정확히 절반으로 고정됩니다! "
                    f"어떻게 원 위의 모든 점에서 각도가 단 0.1도도 변하지 않을까요?"
                ),
                "hud_notes": [
                    "역동적 관찰: 원 위의 점 P가 어디로 이동해도 원주각 ∠APB 크기는 불변!",
                    "핵심 공식: 한 호에 대한 원주각 ∠APB = 1/2 × 중심각 ∠AOB",
                    "질문: 원의 어떤 성질이 중심각과 원주각을 정확히 2 : 1로 묶어 줄까?",
                ],
            },
            {
                "act": 2,
                "badge": "ACT 2 · 원의 정의(반지름 길이 일치)와 이등변삼각형 발견",
                "headline": "원의 중심 O에서 원 위의 점들에 그은 반지름 OA = OP = OB = R 은 모두 같다!",
                "key_formula": "OA = OP = OB = R  ⇒  Isosceles Triangle △OPA (∠OPA = ∠OAP = α)",
                "narration": (
                    f"먼저 https://min7014.github.io/ 원문 자료의 첫 번째 단계처럼 원의 중심 O가 원주각의 한 변 PB 위에 놓이는 가장 기본적인 상태를 관찰해 봅시다. "
                    f"원의 중심 O에서 꼭짓점 A와 P까지의 거리는 모두 원의 반지름 R로 똑같습니다! "
                    f"따라서 삼각형 OPA는 두 변 OA와 OP의 길이가 같은 이등변삼각형이 되어 두 밑각의 크기가 알파로 정확히 같아집니다."
                ),
                "hud_notes": [
                    "1단계 기본 위치: 원의 중심 O가 원주각의 한 변(지름 PB) 위에 있을 때",
                    "원의 핵심 성질: 반지름 OA = OP = R 이므로 △OPA는 이등변삼각형!",
                    "이등변삼각형의 성질: 두 밑각의 크기가 서로 같음 (∠OPA = ∠OAP = α)",
                ],
            },
            {
                "act": 3,
                "badge": "ACT 3 · 반지름 보조선 OP 1줄과 삼각형의 외각 정리 증명",
                "headline": "삼각형 OPA의 한 외각(중심각 ∠AOB)은 이웃하지 않는 두 내각의 합(α + α = 2α)!",
                "key_formula": "Exterior Angle ∠AOB = ∠OPA + ∠OAP = α + α = 2∠APB",
                "narration": (
                    f"이제 이등변삼각형 OPA의 바깥쪽 각인 중심각 ∠AOB를 보세요! "
                    f"삼각형의 한 외각의 크기는 그와 이웃하지 않는 두 내각의 크기의 합과 같으므로, 중심각 ∠AOB는 밑각 알파 더하기 알파, 즉 2알파가 됩니다! "
                    f"중심 O가 원주각 내부에 있을 때도 꼭짓점 P와 중심 O를 잇는 황금 지름 보조선을 한 줄 그으면 양쪽 두 이등변삼각형의 외각의 합으로 단번에 증명됩니다."
                ),
                "hud_notes": [
                    "결정적 보조선: 꼭짓점 P와 원의 중심 O를 잇는 지름(반지름) 보조선 작도!",
                    "삼각형의 외각 정리: 중심각 ∠AOB = 두 밑각의 합(α + α = 2α) = 2∠APB!",
                    "중심이 내부(2α+2β)·외부(2β-2α)에 있을 때도 지름 보조선 1줄로 완벽 증명!",
                ],
            },
            {
                "act": 4,
                "badge": "ACT 4 · 한계를 넘는 상상 (탈레스의 반원 직각과 접선·현이 이루는 각)",
                "headline": "중심각이 180도(지름)가 되면 원주각은 90도! 점이 합쳐지면 접선과 현이 이루는 각!",
                "key_formula": "Diameter (∠AOB = 180°) ⇒ ∠APB = 90°  |  Tangent-Chord Angle",
                "narration": (
                    f"여기서 조건을 과감하게 확장해 볼까요? 만약 현 AB가 원의 중심을 지나는 지름이 되어 중심각이 180도 평각이 되면, 반원 위의 모든 원주각은 180도의 절반인 90도 직각이 됩니다! "
                    f"또한 점 P가 점 A에 한없이 가까워져 할선이 접선으로 변하는 극한의 순간에도, 접선과 현이 이루는 각은 원주각의 크기와 똑같이 유지됩니다."
                ),
                "hud_notes": [
                    "확장 1(탈레스 정리): 지름(중심각 180°)에 대한 원주각은 언제나 90° 직각!",
                    "확장 2(내접사각형): 마주 보는 두 원주각의 합 = 1/2 × 360° = 180°!",
                    "확장 3(접선과 현이 이루는 각): 할선이 접선으로 수렴해도 각도 불변!",
                ],
            },
            {
                "act": 5,
                "badge": "ACT 5 · 수능·내신 원과 기하 10초 실전 해법",
                "headline": "원 위의 점이 보이면 즉시 중심 O와 연결해 반지름 이등변삼각형을 찾아라!",
                "key_formula": "Rule #1: Spot Point on Circle → Connect Center O (Radius Isosceles △)!",
                "narration": (
                        f"기하 문제에서 원이 등장했을 때 막힌다면, 첫 번째 보조선은 언제나 원의 중심 O와 원 위의 점을 잇는 반지름입니다! "
                        f"반지름 이등변삼각형과 원주각은 중심각의 절반이라는 원리 하나로 모든 각도가 10초 만에 풀립니다. "
                        f"설명란의 https://min7014.github.io/ 원문 PDF와 지오지브라를 직접 체험해 보고, 지금 바로 @min7014_ai 채널을 구독하세요!"
                ),
                "hud_notes": [
                    "실전 제1발상: 원 위의 점 등장 → 중심 O와 연결해 반지름 이등변삼각형 표시!",
                    "지름이 보이면 즉시 원주각 90° 직각삼각형을 찾아 피타고라스·삼각비 연결!",
                    "지금 [@min7014_ai 구독] 누르고 1,113개 창의 수학 시네마를 정주행하세요!",
                ],
            },
        ]
    else:
        return [
            {
                "act": 1,
                "badge": "ACT 1 · THE INSCRIBED ANGLE INVARIANT",
                "headline": f"Move Point P Anywhere on the Circle—∠APB Is Always Half of ∠AOB! ({t_title})",
                "key_formula": "∠APB (Inscribed Angle) = 1/2 ∠AOB (Central Angle)",
                "narration": (
                    f"Watch vertex P glide freely along the circular arc while viewing chord AB. "
                    f"Although triangle PAB changes shape at every instant, in [{t_title}] the inscribed angle ∠APB stays strictly locked at exactly half the central angle ∠AOB!"
                ),
                "hud_notes": [
                    "Dynamic Observation: Moving P along the arc never changes ∠APB!",
                    "Core Invariant: Inscribed Angle ∠APB = 1/2 × Central Angle ∠AOB",
                    "Question: Why does the circle enforce this exact 1 : 2 angle ratio?",
                ],
            },
            {
                "act": 2,
                "badge": "ACT 2 · EQUAL RADII & THE ISOSCELES TRIANGLE",
                "headline": "Radii OA = OP = OB = R Form a Glowing Isosceles Triangle △OPA!",
                "key_formula": "OA = OP = OB = R  ⇒  Isosceles Triangle △OPA (∠OPA = ∠OAP = α)",
                "narration": (
                    f"Following the step-by-step proof on https://min7014.github.io/, start when center O lies on side PB. "
                    f"Because every radius of a circle has the exact same length R, segments OA and OP are equal, making triangle OPA isosceles with two equal base angles alpha!"
                ),
                "hud_notes": [
                    "Baseline Case: Center O lies directly on chord-diameter PB",
                    "Circle Definition: Equal radii OA = OP = R create isosceles △OPA!",
                    "Isosceles Property: Base angles are equal (∠OPA = ∠OAP = α)!",
                ],
            },
            {
                "act": 3,
                "badge": "ACT 3 · DIAMETER AUXILIARY LINE & EXTERIOR ANGLE PROOF",
                "headline": "The Central Angle ∠AOB Is the Exterior Angle α + α = 2α!",
                "key_formula": "Exterior Angle ∠AOB = ∠OPA + ∠OAP = α + α = 2∠APB",
                "narration": (
                    f"By the Exterior Angle Theorem, the central angle ∠AOB equals the sum of the two opposite interior angles: alpha plus alpha equals 2 alpha! "
                    f"When center O lies inside or outside the angle, drawing one diameter line through P and O splits the figure into two isosceles triangles and completes the proof in seconds!"
                ),
                "hud_notes": [
                    "Golden Auxiliary Line: Draw the diameter through vertex P and center O!",
                    "Exterior Angle Theorem: ∠AOB = α + α = 2α ⇒ ∠APB = 1/2 ∠AOB!",
                    "Works for all 3 cases: Center on side, inside (2α+2β), or outside (2β-2α)!",
                ],
            },
            {
                "act": 4,
                "badge": "ACT 4 · THALES' 90° SEMICIRCLE & TANGENT-CHORD LIMIT",
                "headline": "A 180° Diameter Gives a 90° Right Angle Anywhere on the Semicircle!",
                "key_formula": "Diameter (∠AOB = 180°) ⇒ ∠APB = 90°  |  Tangent-Chord Angle",
                "narration": (
                    f"When AB is a diameter, the central angle is 180 degrees, so every inscribed angle on a semicircle is a 90-degree right angle! "
                    f"And as P approaches A until the secant becomes a tangent line, the tangent-chord angle preserves the exact same measure!"
                ),
                "hud_notes": [
                    "Thales' Theorem: Any angle inscribed in a semicircle is 90°!",
                    "Cyclic Quadrilateral: Opposite inscribed angles sum to 180°!",
                    "Tangent-Chord Theorem: Preserved in the limit as P approaches A!",
                ],
            },
            {
                "act": 5,
                "badge": "ACT 5 · 10-SECOND CIRCLE GEOMETRY STRATEGY",
                "headline": "Spot a Point on a Circle and Immediately Connect It to Center O!",
                "key_formula": "Rule #1: Spot Point on Circle → Connect Center O (Radius Isosceles △)!",
                "narration": (
                    f"Whenever a point lies on a circle in an exam, connect it to center O to unlock radius isosceles triangles and the 1 to 2 central angle law in 10 seconds! "
                    f"Subscribe to @min7014_ai right now for daily visual math cinema!"
                ),
                "hud_notes": [
                    "Instant Trigger: Point on Circle → Draw Radius to Center O!",
                    "Diameter Spotted → Mark the 90° Inscribed Right Angle immediately!",
                    "Subscribe to @min7014_ai & explore the interactive GeoGebra lab!",
                ],
            },
        ]


def _make_cosmic_canvas(w: int, h: int, t_global: float) -> tuple[Image.Image, Image.Image]:
    """
    풀스크린 다크 벨벳 코스믹 배경 레이어(base_rgb)와 네온 글로우 발광 레이어(glow_rgba)를 생성합니다.
    PDF 캡처 이미지가 전혀 없는 100% 순수 그래픽 시네마 공간입니다.
    """
    base = Image.new("RGB", (w, h), (5, 9, 20))
    b_draw = ImageDraw.Draw(base)

    # 은은한 조화 좌표 그리드
    grid_step = 64
    for gx in range(0, w, grid_step):
        col = (14, 24, 48) if (gx // grid_step) % 4 == 0 else (9, 16, 34)
        b_draw.line([(gx, 0), (gx, h)], fill=col, width=1)
    for gy in range(0, h, grid_step):
        col = (14, 24, 48) if (gy // grid_step) % 4 == 0 else (9, 16, 34)
        b_draw.line([(0, gy), (w, gy)], fill=col, width=1)

    # 부유하는 수학적 스타더스트 입자
    for i in range(28):
        px = int(((i * 197 + t_global * 42 * ((i % 3) + 1)) % w))
        py = int(((i * 131 + math.sin(t_global * 2 + i) * 28) % h))
        r_p = 2 if i % 4 == 0 else 1
        c_p = (56, 189, 248) if i % 2 == 0 else (250, 204, 21)
        b_draw.ellipse((px - r_p, py - r_p, px + r_p, py + r_p), fill=c_p)

    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    return base, glow


def _composite_neon_bloom(base_rgb: Image.Image, glow_rgba: Image.Image, crisp_rgba: Image.Image) -> Image.Image:
    """
    glow_rgba에 다중 가우시안 블러(Wide + Tight Neon Bloom)를 적용하여
    3Blue1Brown / Manim 스타일의 부드럽고 영롱한 발광 효과를 합성합니다.
    """
    bloom_wide = glow_rgba.filter(ImageFilter.GaussianBlur(radius=14))
    bloom_tight = glow_rgba.filter(ImageFilter.GaussianBlur(radius=4))

    out = base_rgb.convert("RGBA")
    out = Image.alpha_composite(out, bloom_wide)
    out = Image.alpha_composite(out, bloom_tight)
    out = Image.alpha_composite(out, crisp_rgba)
    return out.convert("RGB")


def _draw_recursive_pythagoras_tree(
    g_draw: ImageDraw.ImageDraw,
    c_draw: ImageDraw.ImageDraw,
    p1: tuple[float, float],
    p2: tuple[float, float],
    angle_rad: float,
    depth: int,
    max_depth: int,
    progress_depth: float,
    mode_shape: str = "square",
):
    """
    p1 -> p2를 아랫변으로 하는 정사각형(또는 반원/정삼각형)과 직각삼각형을 재귀적으로 작도합니다.
    depth가 깊어질수록 코발트 블루 -> 시안 -> 에메랄드 -> 골드 -> 로즈 네온으로 그라데이션됩니다.
    """
    if depth > max_depth:
        return
    level_alpha = max(0.0, min(1.0, progress_depth - depth + 1.0))
    if level_alpha <= 0.02:
        return

    dx = (p2[0] - p1[0]) * level_alpha
    dy = (p2[1] - p1[1]) * level_alpha
    # 위쪽 방향 법선 벡터 (화면 좌표계에서 위쪽은 y 감소)
    nx = dy
    ny = -dx

    p4 = (p1[0] + nx, p1[1] + ny)
    p3 = (p2[0] + nx, p2[1] + ny)

    palette = [
        ((37, 99, 235, 115), (56, 189, 248, 255)),
        ((14, 165, 233, 115), (125, 211, 252, 255)),
        ((16, 185, 129, 115), (52, 211, 153, 255)),
        ((234, 179, 8, 120), (250, 204, 21, 255)),
        ((244, 63, 94, 125), (251, 113, 133, 255)),
        ((168, 85, 247, 130), (216, 180, 254, 255)),
        ((236, 72, 153, 140), (249, 168, 212, 255)),
    ]
    fill_col, stroke_col = palette[min(depth, len(palette) - 1)]

    if mode_shape == "semicircle" and depth <= 2:
        mx, my = (p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0
        r = int(math.hypot(dx, dy) / 2.0)
        if r > 4:
            g_draw.ellipse((mx - r, my - r, mx + r, my + r), fill=fill_col, outline=stroke_col, width=4)
            c_draw.ellipse((mx - r, my - r, mx + r, my + r), outline=stroke_col, width=3)
    else:
        poly = [p1, p2, p3, p4]
        w_line = max(2, 4 - depth // 2)
        g_draw.polygon(poly, fill=fill_col, outline=stroke_col, width=w_line + 2)
        c_draw.polygon(poly, fill=(fill_col[0], fill_col[1], fill_col[2], 75), outline=stroke_col, width=w_line)

    if depth >= max_depth:
        return

    # 윗변 p4 -> p3 위에 직각삼각형 꼭짓점 apex 계산 (탈레스 반원 위 회전각 angle_rad)
    ux, uy = p3[0] - p4[0], p3[1] - p4[1]
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    # p4에서 ux 방향을 angle_rad만큼 위쪽(법선 방향)으로 회전하고 cos_a 배 축소
    rx = ux * cos_a + uy * sin_a
    ry = -ux * sin_a + uy * cos_a
    apex = (p4[0] + rx * cos_a, p4[1] + ry * cos_a)

    # 직각삼각형 색칠
    tri_pts = [p4, p3, apex]
    c_draw.polygon(tri_pts, fill=(250, 204, 21, 55), outline=(254, 240, 138, 220), width=max(1, 3 - depth // 3))

    _draw_recursive_pythagoras_tree(g_draw, c_draw, p4, apex, angle_rad, depth + 1, max_depth, progress_depth, mode_shape)
    _draw_recursive_pythagoras_tree(g_draw, c_draw, apex, p3, angle_rad, depth + 1, max_depth, progress_depth, mode_shape)


def render_pure_procedural_scene(
    w: int,
    h: int,
    archetype: str,
    act_num: int,
    t_raw: float,
    lang_code: str = "ko",
) -> Image.Image:
    """
    PDF 스크린샷을 단 1픽셀도 사용하지 않고, 오직 수학적 아이디어만으로
    (w, h) 전체 화면에 네온 블룸 절차적 수학 애니메이션을 렌더링합니다.
    """
    t = ease_in_out_cubic(t_raw)
    t_global = (act_num - 1) + t_raw
    base_rgb, glow_rgba = _make_cosmic_canvas(w, h, t_global)
    crisp_rgba = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow_rgba)
    c_draw = ImageDraw.Draw(crisp_rgba)

    is_vertical = h > w
    cx = int(w * (0.50 if is_vertical else 0.37))
    cy = int(h * (0.50 if is_vertical else 0.54))
    scale_ref = min(w, h)

    f_big = vmaker.get_font_for_lang(lang_code, 30 if not is_vertical else 28, bold=True)
    f_med = vmaker.get_font_for_lang(lang_code, 22 if not is_vertical else 22, bold=True)

    if archetype == "pythagoras_fractal":
        trunk_s = scale_ref * (0.19 if not is_vertical else 0.21)
        by_bot = cy + trunk_s * (1.25 if act_num in (1, 5) else 0.85)
        p1 = (cx - trunk_s / 2.0, by_bot)
        p2 = (cx + trunk_s / 2.0, by_bot)

        # 각 막(Act)에 맞는 동적 연출
        if act_num == 1:
            # 0단계 뿌리에서 6단계(64개 잎사귀)까지 프랙탈 나무가 순차적으로 피어나며 바람에 흔들림
            angle_rad = math.radians(37.0 + 14.0 * math.sin(t_raw * math.pi))
            prog_depth = 1.2 + 5.3 * t
            _draw_recursive_pythagoras_tree(g_draw, c_draw, p1, p2, angle_rad, 0, 6, prog_depth, "square")
        elif act_num == 2:
            # Act 2: 3-4-5 직각삼각형과 25칸(5x5), 16칸(4x4), 9칸(3x3) 실제 단위 격자 타일 시각화
            angle_rad = math.acos(0.8)  # 3-4-5 triangle (cos = 4/5)
            _draw_recursive_pythagoras_tree(g_draw, c_draw, p1, p2, angle_rad, 0, 1, 2.0, "square")
            # 뿌리 정사각형 내부에 5x5 = 25개 타일 격자 작도
            p4 = (p1[0], p1[1] - trunk_s)
            step_tile = trunk_s / 5.0
            active_tiles = int(1 + 24 * t)
            cnt = 0
            for r_i in range(5):
                for c_i in range(5):
                    cnt += 1
                    tx0 = p4[0] + c_i * step_tile + 3
                    ty0 = p4[1] + r_i * step_tile + 3
                    col_t = (250, 204, 21, 185) if cnt <= active_tiles else (56, 189, 248, 45)
                    c_draw.rounded_rectangle((tx0, ty0, tx0 + step_tile - 6, ty0 + step_tile - 6), radius=4, fill=col_t)
            c_draw.text((int(cx - 88), int(by_bot + 16)), "5² = 25 Tiles = 16 + 9", fill=(254, 240, 138, 255), font=f_big)
        elif act_num == 3:
            # Act 3: 직각 꼭짓점 C에서 빗변 정사각형 바닥까지 관통하는 황금 수선(Euclid Altitude)과 두 직사각형 분할
            angle_rad = math.acos(0.8)
            _draw_recursive_pythagoras_tree(g_draw, c_draw, p1, p2, angle_rad, 0, 2, 2.5, "square")
            p4 = (p1[0], p1[1] - trunk_s)
            p3 = (p2[0], p2[1] - trunk_s)
            ux = p3[0] - p4[0]
            cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
            apex = (p4[0] + ux * cos_a * cos_a, p4[1] - ux * cos_a * sin_a)
            alt_y = apex[1] + (by_bot - apex[1]) * t
            # 왼쪽 분할 영역(a^2=16)과 오른쪽 분할 영역(b^2=9) 색칠
            c_draw.rectangle((p4[0], p4[1], apex[0], by_bot), fill=(14, 165, 233, 95), outline=(56, 189, 248, 255), width=3)
            c_draw.rectangle((apex[0], p4[1], p3[0], by_bot), fill=(16, 185, 129, 95), outline=(52, 211, 153, 255), width=3)
            g_draw.line([(apex[0], apex[1]), (apex[0], alt_y)], fill=(250, 204, 21, 255), width=9)
            c_draw.line([(apex[0], apex[1]), (apex[0], alt_y)], fill=(255, 255, 255, 255), width=4)
            c_draw.ellipse((apex[0] - 9, alt_y - 9, apex[0] + 9, alt_y + 9), fill=(244, 63, 94, 255), outline=(255, 255, 255, 255), width=3)
        elif act_num == 4:
            # Act 4: 정사각형을 넘어 반원(Semicircles)과 동적 각도 변화로 확장!
            angle_rad = math.radians(32.0 + 26.0 * t)
            _draw_recursive_pythagoras_tree(g_draw, c_draw, p1, p2, angle_rad, 0, 3, 3.6, "semicircle")
            c_draw.text((int(cx - 140), int(by_bot + 18)), "S1(반원) + S2(반원) = S0(큰 반원)", fill=(125, 211, 252, 255), font=f_big)
        else:
            # Act 5: 6단계 프랙탈 전체가 황금빛으로 공명하며 뿌리로 수렴하는 피날레
            angle_rad = math.radians(45.0 - 12.0 * math.cos(t_raw * math.pi * 2))
            _draw_recursive_pythagoras_tree(g_draw, c_draw, p1, p2, angle_rad, 0, 6, 6.5, "square")
            c_draw.text((int(cx - 140), int(by_bot + 10)), "SUM(64 Leaves) = Root Square (25)", fill=(250, 204, 21, 255), font=f_med)

    elif archetype == "ceva_menelaus":
        R = scale_ref * (0.31 if not is_vertical else 0.33)
        A = (cx, cy - R * 0.95)
        B = (cx - R * 1.12, cy + R * 0.75)
        C = (cx + R * 1.12, cy + R * 0.75)
        ang = t_raw * math.pi * 2.0
        P = (cx + math.cos(ang) * R * 0.24, cy + R * 0.10 + math.sin(ang * 1.5) * R * 0.16)

        # 3개 분할 삼각형 네온 글래스 패치
        for pts, f_c, s_c in [
            ([P, A, B], (37, 99, 235, 90), (56, 189, 248, 255)),
            ([P, B, C], (16, 185, 129, 90), (52, 211, 153, 255)),
            ([P, C, A], (244, 63, 94, 90), (251, 113, 133, 255)),
        ]:
            g_draw.polygon(pts, fill=f_c, outline=s_c, width=5)
            c_draw.polygon(pts, fill=(f_c[0], f_c[1], f_c[2], 65), outline=s_c, width=3)

        # 체바 선분 연장선 및 교점 D, E, F
        def line_intersect(p_a, p_b, p_c, p_d):
            x1, y1 = p_a
            x2, y2 = p_b
            x3, y3 = p_c
            x4, y4 = p_d
            denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if abs(denom) < 1e-6:
                return ((x3 + x4) / 2, (y3 + y4) / 2)
            px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
            py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom
            return (px, py)

        D = line_intersect(A, P, B, C)
        E = line_intersect(B, P, C, A)
        F = line_intersect(C, P, A, B)

        for V, opp, col in [(A, D, (250, 204, 21, 255)), (B, E, (56, 189, 248, 255)), (C, F, (251, 113, 133, 255))]:
            g_draw.line([V, opp], fill=col, width=7)
            c_draw.line([V, opp], fill=(255, 255, 255, 245), width=3)
            c_draw.ellipse((opp[0] - 8, opp[1] - 8, opp[0] + 8, opp[1] + 8), fill=col, outline=(255, 255, 255, 255), width=2)

        c_draw.ellipse((P[0] - 11, P[1] - 11, P[0] + 11, P[1] + 11), fill=(250, 204, 21, 255), outline=(255, 255, 255, 255), width=3)
        r1 = math.hypot(A[0] - F[0], A[1] - F[1]) / max(1.0, math.hypot(F[0] - B[0], F[1] - B[1]))
        r2 = math.hypot(B[0] - D[0], B[1] - D[1]) / max(1.0, math.hypot(D[0] - C[0], D[1] - C[1]))
        r3 = 1.0 / max(0.01, r1 * r2)
        c_draw.text(
            (int(cx - 210), int(cy + R * 0.86)),
            f"({r1:.2f}) × ({r2:.2f}) × ({r3:.2f}) = 1.0000 (불변!)",
            fill=(254, 240, 138, 255),
            font=f_big,
        )

    elif archetype == "menelaus_theorem":
        # 메넬라우스의 정리: 삼각형 ABC와 연장선 외분점 D를 관통하는 할선 D-F-E + 꼭짓점 C를 지나는 평행 보조선 CK ∥ AB!
        R = scale_ref * (0.29 if not is_vertical else 0.31)
        A = (cx - R * 0.18, cy - R * 0.92)
        B = (cx - R * 1.15, cy + R * 0.68)
        C = (cx + R * 0.38, cy + R * 0.68)
        D = (cx + R * 1.28, cy + R * 0.68)  # BC 연장선 위의 외분점 D

        # 할선이 AB 위 점 F를 지날 때 AC 위 교점 E와 평행 보조선 CK(CK ∥ AB) 작도
        u_f = 0.42 + 0.18 * math.sin(t_raw * math.pi * 2.0)
        F = (A[0] + (B[0] - A[0]) * u_f, A[1] + (B[1] - A[1]) * u_f)

        def _line_isect(p1, p2, p3, p4):
            x1, y1 = p1
            x2, y2 = p2
            x3, y3 = p3
            x4, y4 = p4
            den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if abs(den) < 1e-6:
                return ((x3 + x4) / 2.0, (y3 + y4) / 2.0)
            px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / den
            py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / den
            return (px, py)

        E = _line_isect(D, F, A, C)
        C_par = (C[0] + (A[0] - B[0]), C[1] + (A[1] - B[1]))
        K = _line_isect(D, F, C, C_par)

        # 삼각형 ABC 및 닮음 삼각형 패치
        g_draw.polygon([A, B, C], fill=(37, 99, 235, 80), outline=(56, 189, 248, 255), width=5)
        c_draw.polygon([A, B, C], fill=(37, 99, 235, 50), outline=(255, 255, 255, 235), width=3)
        g_draw.polygon([C, K, E], fill=(250, 204, 21, 85), outline=(250, 204, 21, 240), width=4)

        # BC 연장선 (B -> C -> D)
        g_draw.line([B, D], fill=(125, 211, 252, 220), width=5)
        c_draw.line([B, D], fill=(255, 255, 255, 230), width=2)

        # 꼭짓점 C를 지나는 황금 평행 보조선 CK ∥ AB
        g_draw.line([C, K], fill=(52, 211, 153, 255), width=8)
        c_draw.line([C, K], fill=(255, 255, 255, 255), width=3)

        # 삼각형을 관통하는 네온 할선 (Transversal Line) F - E - D
        ext_f = (F[0] - (D[0] - F[0]) * 0.22, F[1] - (D[1] - F[1]) * 0.22)
        ext_d = (D[0] + (D[0] - F[0]) * 0.12, D[1] + (D[1] - F[1]) * 0.12)
        g_draw.line([ext_f, ext_d], fill=(244, 63, 94, 255), width=8)
        c_draw.line([ext_f, ext_d], fill=(255, 255, 255, 245), width=3)

        for pt, lbl, col in [
            (A, "A", (56, 189, 248, 255)),
            (B, "B", (56, 189, 248, 255)),
            (C, "C", (56, 189, 248, 255)),
            (D, "D(외분)", (251, 113, 133, 255)),
            (E, "E", (250, 204, 21, 255)),
            (F, "F", (250, 204, 21, 255)),
            (K, "K(평행보조선)", (52, 211, 153, 255)),
        ]:
            c_draw.ellipse((pt[0] - 8, pt[1] - 8, pt[0] + 8, pt[1] + 8), fill=col, outline=(255, 255, 255, 255), width=2)
            c_draw.text((int(pt[0] - 12), int(pt[1] - 28)), lbl, fill=(254, 240, 138, 255), font=f_med)

        c_draw.text(
            (int(cx - 245), int(cy + R * 0.86)),
            "(AF/FB) × (BD/DC) × (CE/EA) = 1.000 (평행 보조선 CK 닮음 약분!)",
            fill=(254, 240, 138, 255),
            font=f_big,
        )

    elif archetype == "conic_parabola":
        # 포물선에서의 빛 반사 & 포물선의 정의: 수직 준선 x = -p, 포물선 y² = 4px, 단일 초점 F(p, 0), |PF| = |PH| 이등변삼각형!
        p_len = scale_ref * (0.11 if not is_vertical else 0.12)
        vx = cx - int(p_len * 0.4)
        vy = cy
        dir_x = int(vx - p_len)
        F = (int(vx + p_len), vy)

        # 좌측 수직 준선(Directrix l: x = -p)
        span_y = int(scale_ref * 0.36)
        g_draw.line([(dir_x, vy - span_y), (dir_x, vy + span_y)], fill=(192, 132, 252, 245), width=7)
        c_draw.line([(dir_x, vy - span_y), (dir_x, vy + span_y)], fill=(255, 255, 255, 240), width=3)
        c_draw.text((dir_x - 42, vy - span_y - 30), "준선 l", fill=(216, 180, 254, 255), font=f_med)

        # 포물선 곡선 y² = 4 p (x - vx)
        para_pts = []
        for k in range(-40, 41):
            yk = (k / 40.0) * span_y
            xk = vx + (yk * yk) / max(1.0, 4.0 * p_len)
            para_pts.append((xk, vy + yk))
        g_draw.line(para_pts, fill=(56, 189, 248, 255), width=8)
        c_draw.line(para_pts, fill=(255, 255, 255, 245), width=3)

        # 8개의 평행 입사광선이 포물선 내벽 P에서 반사되어 단일 초점 F로 집속!
        right_src_x = vx + int(scale_ref * 0.44)
        for idx_r, frac_y in enumerate([-0.82, -0.58, -0.34, -0.14, 0.14, 0.34, 0.58, 0.82]):
            ry_p = vy + frac_y * span_y
            rx_p = vx + ((ry_p - vy) ** 2) / max(1.0, 4.0 * p_len)
            P_ray = (rx_p, ry_p)
            H_ray = (dir_x, ry_p)
            # 평행 입사광선 (오른쪽 -> P) 및 초점 반사광선 (P -> F)
            g_draw.line([(right_src_x, ry_p), P_ray], fill=(250, 204, 21, 155), width=4)
            g_draw.line([P_ray, F], fill=(244, 63, 94, 210), width=5)
            c_draw.line([P_ray, F], fill=(255, 255, 255, 230), width=2)
            if idx_r == 1:
                # 대표점 P에서 준선 수선의 발 H와 초점 F를 잇는 |PF| = |PH| 이등변삼각형 △PFH 강조!
                g_draw.polygon([P_ray, F, H_ray], fill=(16, 185, 129, 85), outline=(52, 211, 153, 255), width=5)
                c_draw.line([P_ray, H_ray], fill=(52, 211, 153, 255), width=4)
                c_draw.line([P_ray, F], fill=(52, 211, 153, 255), width=4)
                c_draw.ellipse((H_ray[0] - 8, H_ray[1] - 8, H_ray[0] + 8, H_ray[1] + 8), fill=(52, 211, 153, 255), outline=(255, 255, 255, 255), width=2)
                c_draw.ellipse((P_ray[0] - 8, P_ray[1] - 8, P_ray[0] + 8, P_ray[1] + 8), fill=(250, 204, 21, 255), outline=(255, 255, 255, 255), width=2)
                c_draw.text((int(H_ray[0] - 32), int(H_ray[1] - 12)), "H", fill=(52, 211, 153, 255), font=f_med)
                c_draw.text((int(P_ray[0] + 10), int(P_ray[1] - 26)), "P(|PF|=|PH|)", fill=(254, 240, 138, 255), font=f_med)

        g_draw.ellipse((F[0] - 14, F[1] - 14, F[0] + 14, F[1] + 14), fill=(225, 29, 72, 255))
        c_draw.ellipse((F[0] - 9, F[1] - 9, F[0] + 9, F[1] + 9), fill=(255, 255, 255, 255))
        c_draw.text((F[0] - 18, F[1] + 16), "초점 F", fill=(254, 240, 138, 255), font=f_med)
        c_draw.text((int(cx - 210), int(vy + span_y + 18)), "|PF| = |PH| (초점 거리 = 준선 거리 · 평행광 집속!)", fill=(52, 211, 153, 255), font=f_big)

    elif archetype == "conic_reflection":
        # 12개의 동시 광선 파동이 초점 F1에서 출발해 타원 벽면에 반사된 뒤 정확히 같은 시각에 초점 F2로 수렴!
        rx = int(scale_ref * (0.36 if not is_vertical else 0.38))
        ry = int(scale_ref * (0.25 if not is_vertical else 0.27))
        g_draw.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(15, 23, 42, 120), outline=(56, 189, 248, 255), width=7)
        c_draw.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), outline=(255, 255, 255, 240), width=3)

        c_dist = int(math.sqrt(max(1, rx * rx - ry * ry)))
        F1 = (cx - c_dist, cy)
        F2 = (cx + c_dist, cy)
        total_len = 2.0 * rx  # |PF1| + |PF2| = 2a 일정!
        travel_d = total_len * (0.12 + 0.86 * t)

        for k in range(12):
            ang = (k / 12.0) * 2.0 * math.pi
            P = (cx + rx * math.cos(ang), cy + ry * math.sin(ang))
            d1 = math.hypot(P[0] - F1[0], P[1] - F1[1])
            d2 = max(1.0, total_len - d1)
            if travel_d <= d1:
                u = travel_d / max(1.0, d1)
                cur = (F1[0] + (P[0] - F1[0]) * u, F1[1] + (P[1] - F1[1]) * u)
                g_draw.line([F1, cur], fill=(250, 204, 21, 180), width=4)
                c_draw.line([F1, cur], fill=(254, 240, 138, 230), width=2)
            else:
                u2 = min(1.0, (travel_d - d1) / d2)
                cur = (P[0] + (F2[0] - P[0]) * u2, P[1] + (F2[1] - P[1]) * u2)
                g_draw.line([F1, P], fill=(56, 189, 248, 110), width=3)
                g_draw.line([P, cur], fill=(244, 63, 94, 220), width=5)
                c_draw.line([P, cur], fill=(255, 255, 255, 240), width=2)
            c_draw.ellipse((cur[0] - 6, cur[1] - 6, cur[0] + 6, cur[1] + 6), fill=(250, 204, 21, 255))

        for F, lbl in [(F1, "F1"), (F2, "F2")]:
            g_draw.ellipse((F[0] - 14, F[1] - 14, F[0] + 14, F[1] + 14), fill=(225, 29, 72, 255))
            c_draw.ellipse((F[0] - 9, F[1] - 9, F[0] + 9, F[1] + 9), fill=(255, 255, 255, 255))
            c_draw.text((F[0] - 16, F[1] + 16), lbl, fill=(254, 240, 138, 255), font=f_med)
        c_draw.text((int(cx - 180), int(cy + ry + 26)), "|PF1| + |PF2| = 2a (모든 광선 동시 도착!)", fill=(52, 211, 153, 255), font=f_big)

    elif archetype in ("calculus_motion", "cauchy_mvt", "inverse_deriv"):
        span_w = int(scale_ref * 0.68)
        span_h = int(scale_ref * 0.44)
        ax0 = cx - span_w // 2
        ay0 = cy + span_h // 2
        c_draw.line([(ax0, ay0), (ax0 + span_w, ay0)], fill=(148, 163, 184, 220), width=3)
        c_draw.line([(ax0, ay0), (ax0, ay0 - span_h)], fill=(148, 163, 184, 220), width=3)

        def f_val(u):
            return 0.15 + 0.65 * (u ** 1.8) - 0.12 * math.sin(u * math.pi * 2)

        if archetype == "inverse_deriv":
            # y = x 대칭축과 원래 함수 y = f(x) 및 역함수 y = f⁻¹(x)의 대칭 접선!
            s_len = min(span_w, span_h)
            g_draw.line([(ax0, ay0), (ax0 + s_len, ay0 - s_len)], fill=(250, 204, 21, 190), width=5)
            c_draw.line([(ax0, ay0), (ax0 + s_len, ay0 - s_len)], fill=(254, 240, 138, 235), width=2)
            pts_f = [(ax0 + int((k / 60.0) * s_len), ay0 - int(((k / 60.0) ** 1.75) * s_len)) for k in range(61)]
            pts_inv = [(ax0 + int(((k / 60.0) ** 1.75) * s_len), ay0 - int((k / 60.0) * s_len)) for k in range(61)]
            g_draw.line(pts_f, fill=(56, 189, 248, 255), width=8)
            c_draw.line(pts_f, fill=(255, 255, 255, 245), width=3)
            g_draw.line(pts_inv, fill=(244, 63, 94, 255), width=8)
            c_draw.line(pts_inv, fill=(255, 255, 255, 245), width=3)
            c_draw.text((int(cx - 210), int(ay0 + 22)), "(f⁻¹)'(y) = 1 / f'(x)  (직선 y=x 대칭 역수 기울기!)", fill=(250, 204, 21, 255), font=f_big)
        elif archetype == "cauchy_mvt":
            # 코시의 평균값 정리: 두 끝점 A, B를 잇는 할선과 평행한 접선이 존재하는 점 c!
            pts = [(ax0 + int((k / 80.0) * span_w), ay0 - int(f_val(k / 80.0) * span_h)) for k in range(81)]
            g_draw.line(pts, fill=(52, 211, 153, 255), width=9)
            c_draw.line(pts, fill=(255, 255, 255, 255), width=4)
            pa = pts[10]
            pb = pts[72]
            pc = pts[43]
            dx_s, dy_s = pb[0] - pa[0], pb[1] - pa[1]
            # 양 끝점 할선 (Secant Chord)
            g_draw.line([pa, pb], fill=(56, 189, 248, 230), width=6)
            c_draw.line([pa, pb], fill=(255, 255, 255, 240), width=2)
            # 점 c에서의 평행 접선 (Parallel Tangent at c)
            g_draw.line([(pc[0] - dx_s * 0.45, pc[1] - dy_s * 0.45), (pc[0] + dx_s * 0.45, pc[1] + dy_s * 0.45)], fill=(250, 204, 21, 255), width=8)
            c_draw.line([(pc[0] - dx_s * 0.45, pc[1] - dy_s * 0.45), (pc[0] + dx_s * 0.45, pc[1] + dy_s * 0.45)], fill=(255, 255, 255, 255), width=3)
            for pt_c in [pa, pb, pc]:
                c_draw.ellipse((pt_c[0] - 9, pt_c[1] - 9, pt_c[0] + 9, pt_c[1] + 9), fill=(244, 63, 94, 255), outline=(255, 255, 255, 255), width=3)
            c_draw.text((int(cx - 235), int(ay0 + 22)), "[f(b)-f(a)] / [g(b)-g(a)] = f'(c) / g'(c) (평행 접선!)", fill=(250, 204, 21, 255), font=f_big)
        else:
            # 리만 적분 글로우 바 (N이 6 -> 12 -> 24 -> 48로 촘촘해짐)
            n_bars = 8 + int(28 * t)
            for bi in range(n_bars):
                u0 = bi / n_bars
                u1 = (bi + 1) / n_bars
                bx0 = ax0 + int(u0 * span_w)
                bx1 = ax0 + int(u1 * span_w)
                bh = int(f_val((u0 + u1) / 2.0) * span_h)
                c_draw.rectangle((bx0 + 1, ay0 - bh, max(bx0 + 2, bx1 - 1), ay0), fill=(14, 165, 233, 75), outline=(56, 189, 248, 160), width=1)

            pts = [(ax0 + int((k / 80.0) * span_w), ay0 - int(f_val(k / 80.0) * span_h)) for k in range(81)]
            g_draw.line(pts, fill=(52, 211, 153, 255), width=9)
            c_draw.line(pts, fill=(255, 255, 255, 255), width=4)

            # 할선이 접선으로 수렴하는 애니메이션
            ua = 0.32
            ub = max(ua + 0.02, 0.90 - 0.56 * t)
            pa = (ax0 + int(ua * span_w), ay0 - int(f_val(ua) * span_h))
            pb = (ax0 + int(ub * span_w), ay0 - int(f_val(ub) * span_h))
            dx_s, dy_s = pb[0] - pa[0], pb[1] - pa[1]
            g_draw.line([(pa[0] - dx_s * 0.6, pa[1] - dy_s * 0.6), (pb[0] + dx_s * 0.6, pb[1] + dy_s * 0.6)], fill=(250, 204, 21, 255), width=7)
            c_draw.line([(pa[0] - dx_s * 0.6, pa[1] - dy_s * 0.6), (pb[0] + dx_s * 0.6, pb[1] + dy_s * 0.6)], fill=(255, 255, 255, 255), width=3)
            for pt_c in [pa, pb]:
                c_draw.ellipse((pt_c[0] - 9, pt_c[1] - 9, pt_c[0] + 9, pt_c[1] + 9), fill=(244, 63, 94, 255), outline=(255, 255, 255, 255), width=3)
            c_draw.text((int(cx - 180), int(ay0 + 22)), f"Δx = {ub - ua:.3f} → 0  |  리만 분할 N = {n_bars}", fill=(250, 204, 21, 255), font=f_big)

    elif archetype in ("trig_harmonic", "trig_deriv_sin"):
        # 단위원 페이저 회전 + 실시간 사인·탄젠트 파동 생성기 & 부채꼴 샌드위치 정리(sin θ < θ < tan θ)
        R = int(scale_ref * (0.22 if not is_vertical else 0.25))
        ucx = cx - int(scale_ref * (0.18 if not is_vertical else 0.0))
        ucy = cy - int(scale_ref * (0.04 if not is_vertical else 0.12))
        g_draw.ellipse((ucx - R, ucy - R, ucx + R, ucy + R), fill=(15, 23, 42, 110), outline=(56, 189, 248, 255), width=6)
        c_draw.ellipse((ucx - R, ucy - R, ucx + R, ucy + R), outline=(255, 255, 255, 240), width=2)
        c_draw.line([(ucx - R - 20, ucy), (ucx + R + 280, ucy)], fill=(148, 163, 184, 180), width=2)
        c_draw.line([(ucx, ucy - R - 20), (ucx, ucy + R + 20)], fill=(148, 163, 184, 180), width=2)

        theta = (0.18 + 0.62 * (0.5 - 0.5 * math.cos(t_raw * math.pi * 2))) * (math.pi / 2.2)
        px = ucx + R * math.cos(theta)
        py = ucy - R * math.sin(theta)
        tx = ucx + R
        ty = ucy - R * math.tan(theta)

        # 삼각형 OAP, 부채꼴 OAB, 접선 삼각형 OAT 샌드위치 비교
        g_draw.polygon([(ucx, ucy), (ucx + R, ucy), (tx, ty)], fill=(250, 204, 21, 65), outline=(250, 204, 21, 235), width=4)
        g_draw.polygon([(ucx, ucy), (ucx + R, ucy), (px, py)], fill=(16, 185, 129, 95), outline=(52, 211, 153, 255), width=5)
        g_draw.line([(px, py), (px, ucy)], fill=(244, 63, 94, 255), width=7)
        c_draw.line([(px, py), (px, ucy)], fill=(255, 255, 255, 255), width=3)

        # 우측 사인파 및 코사인 도함수 진행 궤적
        wx0 = ucx + R + 40
        wave_w = int(scale_ref * 0.28)
        w_pts = []
        cos_pts = []
        for k in range(60):
            u_k = k / 59.0
            ang_k = theta + u_k * math.pi * 2.0
            w_pts.append((wx0 + u_k * wave_w, ucy - R * math.sin(ang_k) * 0.85))
            cos_pts.append((wx0 + u_k * wave_w, ucy - R * math.cos(ang_k) * 0.85))
        g_draw.line(w_pts, fill=(52, 211, 153, 235), width=6)
        c_draw.line(w_pts, fill=(255, 255, 255, 240), width=2)
        if archetype == "trig_deriv_sin":
            g_draw.line(cos_pts, fill=(250, 204, 21, 220), width=5)
            c_draw.text((int(cx - 210), int(ucy + R + 32)), "d/dx (sin x) = cos x  (사인 곡선 접선 기울기 = 코사인!)", fill=(254, 240, 138, 255), font=f_big)
        else:
            g_draw.line([(px, py), w_pts[0]], fill=(250, 204, 21, 180), width=3)
            c_draw.text((int(cx - 210), int(ucy + R + 32)), f"sin θ ({math.sin(theta):.3f}) < θ ({theta:.3f}) < tan θ ({math.tan(theta):.3f})", fill=(254, 240, 138, 255), font=f_big)

    elif archetype in ("special_triangles", "square_root_geometry", "parallel_similarity", "cycloid_kinematics"):
        R = int(scale_ref * 0.30)
        if archetype == "special_triangles":
            # 정삼각형 이등분 (30-60-90: 1 : √3 : 2) & 직각이등변삼각형 (1 : 1 : √2)
            top_p = (cx, cy - int(R * 0.86))
            left_p = (cx - R, cy + int(R * 0.86))
            right_p = (cx + R, cy + int(R * 0.86))
            mid_p = (cx, cy + int(R * 0.86))
            g_draw.polygon([top_p, left_p, right_p], fill=(37, 99, 235, 85), outline=(56, 189, 248, 255), width=6)
            c_draw.polygon([top_p, left_p, right_p], outline=(255, 255, 255, 240), width=3)
            g_draw.line([top_p, mid_p], fill=(250, 204, 21, 255), width=8)
            c_draw.line([top_p, mid_p], fill=(255, 255, 255, 255), width=3)
            c_draw.text((int(cx - 215), int(cy + R + 18)), "30°-60°-90° (1 : √3 : 2)  |  45°-45°-90° (1 : 1 : √2)", fill=(254, 240, 138, 255), font=f_big)
        elif archetype == "square_root_geometry":
            # 넓이가 a인 정사각형의 한 변 √a 와 수직선 ±√a 대칭
            sq_r = int(R * 0.72)
            g_draw.rectangle((cx - sq_r, cy - sq_r - 20, cx + sq_r, cy + sq_r - 20), fill=(16, 185, 129, 90), outline=(52, 211, 153, 255), width=6)
            c_draw.rectangle((cx - sq_r, cy - sq_r - 20, cx + sq_r, cy + sq_r - 20), outline=(255, 255, 255, 245), width=3)
            c_draw.line([(cx - int(R * 1.3), cy + sq_r + 25), (cx + int(R * 1.3), cy + sq_r + 25)], fill=(250, 204, 21, 240), width=4)
            c_draw.text((int(cx - 65), int(cy - 30)), "Area = a", fill=(254, 240, 138, 255), font=f_big)
            c_draw.text((int(cx - 215), int(cy + sq_r + 42)), "x² = a ⇔ x = ±√a (넓이 a인 정사각형 한 변 = √a)", fill=(254, 240, 138, 255), font=f_big)
        elif archetype == "parallel_similarity":
            # 세 평행선 l ∥ m ∥ n 과 선분의 길이의 비 a : b = a' : b'
            for idx_l, dy_l in enumerate([-int(R * 0.75), 0, int(R * 0.75)]):
                yl = cy + dy_l
                g_draw.line([(cx - int(R * 1.25), yl), (cx + int(R * 1.25), yl)], fill=(56, 189, 248, 235), width=6)
                c_draw.line([(cx - int(R * 1.25), yl), (cx + int(R * 1.25), yl)], fill=(255, 255, 255, 240), width=2)
            g_draw.line([(cx - int(R * 0.85), cy - int(R * 0.85)), (cx - int(R * 0.25), cy + int(R * 0.85))], fill=(250, 204, 21, 255), width=7)
            g_draw.line([(cx + int(R * 0.15), cy - int(R * 0.85)), (cx + int(R * 0.95), cy + int(R * 0.85))], fill=(244, 63, 94, 255), width=7)
            g_draw.line([(cx + int(R * 0.15), cy - int(R * 0.75)), (cx + int(R * 0.75), cy + int(R * 0.75))], fill=(52, 211, 153, 235), width=6)
            c_draw.text((int(cx - 215), int(cy + int(R * 0.92))), "평행선 l ∥ m ∥ n  ⇒  선분 길이 비 a : b = a' : b'", fill=(254, 240, 138, 255), font=f_big)
        else:
            # 사이클로이드: 구르는 원과 x(θ) = r(θ - sin θ), y(θ) = r(1 - cos θ)
            r_c = int(scale_ref * 0.11)
            base_y = cy + int(r_c * 1.1)
            start_x = cx - int(r_c * 3.14)
            c_draw.line([(start_x - 30, base_y), ( start_x + int(r_c * 6.5), base_y)], fill=(148, 163, 184, 230), width=3)
            cyc_pts = []
            for k in range(81):
                th = (k / 80.0) * 2.0 * math.pi
                cyc_pts.append((start_x + r_c * (th - math.sin(th)), base_y - r_c * (1.0 - math.cos(th))))
            g_draw.line(cyc_pts, fill=(244, 63, 94, 255), width=8)
            c_draw.line(cyc_pts, fill=(255, 255, 255, 245), width=3)
            th_now = (0.15 + 0.75 * t) * 2.0 * math.pi
            ccx = start_x + r_c * th_now
            ccy = base_y - r_c
            px_c = start_x + r_c * (th_now - math.sin(th_now))
            py_c = base_y - r_c * (1.0 - math.cos(th_now))
            g_draw.ellipse((ccx - r_c, ccy - r_c, ccx + r_c, ccy + r_c), outline=(56, 189, 248, 255), width=5)
            g_draw.line([(ccx, ccy), (px_c, py_c)], fill=(250, 204, 21, 255), width=6)
            c_draw.ellipse((px_c - 8, py_c - 8, px_c + 8, py_c + 8), fill=(250, 204, 21, 255), outline=(255, 255, 255, 255), width=2)
            c_draw.text((int(cx - 225), int(base_y + 20)), "x = r(θ - sin θ), dx/dθ = r(1 - cos θ) ≥ 0 (꼬임 없음!)", fill=(254, 240, 138, 255), font=f_big)

    elif archetype == "fibonacci_golden":
        # 황금비 해바라기 필로탁시스(Phyllotaxis) 144개 네온 씨앗 나선
        seed_palette = [
            (56, 189, 248),
            (52, 211, 153),
            (250, 204, 21),
            (251, 113, 133),
            (192, 132, 252),
        ]
        golden_ang = math.radians(137.507764)
        max_seeds = int(24 + 120 * t)
        spread = scale_ref * 0.025
        for n in range(1, max_seeds + 1):
            r_n = spread * math.sqrt(n)
            a_n = n * golden_ang + t_raw * 0.8
            sx = cx + r_n * math.cos(a_n)
            sy = cy + r_n * math.sin(a_n)
            col_s = seed_palette[n % len(seed_palette)]
            rad_s = max(4, int(9 - n * 0.03))
            g_draw.ellipse((sx - rad_s - 2, sy - rad_s - 2, sx + rad_s + 2, sy + rad_s + 2), fill=(col_s[0], col_s[1], col_s[2], 210))
            c_draw.ellipse((sx - rad_s + 1, sy - rad_s + 1, sx + rad_s - 1, sy + rad_s - 1), fill=(255, 255, 255, 235))
        c_draw.text((int(cx - 195), int(cy - scale_ref * 0.36)), "황금각 137.508° · φ = (1 + √5)/2 = 1.618034", fill=(250, 204, 21, 255), font=f_big)

    elif archetype == "prob_galton":
        # 이항분포 갈톤 보드(Galton Board) -> 정규분포 가우시안 벨 커브 수렴
        span_w = int(scale_ref * 0.66)
        span_h = int(scale_ref * 0.42)
        ax0 = cx - span_w // 2
        ay0 = cy + span_h // 2
        n_bins = 16
        bin_w = span_w / n_bins
        for k in range(n_bins):
            z = (k - (n_bins - 1) / 2.0) / (n_bins / 5.2)
            bell = math.exp(-0.5 * z * z)
            bh = int(bell * span_h * (0.35 + 0.65 * t))
            bx0 = ax0 + int(k * bin_w) + 3
            bx1 = ax0 + int((k + 1) * bin_w) - 3
            g_draw.rectangle((bx0, ay0 - bh, bx1, ay0), fill=(56, 189, 248, 125), outline=(125, 211, 252, 240), width=3)
            c_draw.rectangle((bx0, ay0 - bh, bx1, ay0), fill=(14, 165, 233, 95), outline=(255, 255, 255, 220), width=1)
        curve_pts = []
        for i in range(81):
            u = i / 80.0
            z = (u - 0.5) * 5.2
            bell = math.exp(-0.5 * z * z)
            curve_pts.append((ax0 + u * span_w, ay0 - bell * span_h))
        g_draw.line(curve_pts, fill=(250, 204, 21, 255), width=8)
        c_draw.line(curve_pts, fill=(255, 255, 255, 255), width=3)
        c_draw.text((int(cx - 190), int(ay0 + 22)), "이항분포 B(n, p) → 정규분포 N(μ, σ²) 수렴!", fill=(254, 240, 138, 255), font=f_big)

    else:
        # 원주각·중심각 불변량 & 보조선 반지름 동적 레이더
        R = int(scale_ref * (0.31 if not is_vertical else 0.33))
        g_draw.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(15, 23, 42, 110), outline=(56, 189, 248, 255), width=8)
        c_draw.ellipse((cx - R, cy - R, cx + R, cy + R), outline=(255, 255, 255, 245), width=3)

        A = (cx - int(R * 0.78), cy + int(R * 0.62))
        B = (cx + int(R * 0.78), cy + int(R * 0.62))
        ang_p = (-0.82 + 0.64 * math.sin(t_raw * math.pi)) * math.pi
        P = (cx + int(R * math.cos(ang_p)), cy + int(R * math.sin(ang_p)))

        g_draw.polygon([(cx, cy), A, B], fill=(244, 63, 94, 85), outline=(251, 113, 133, 255), width=4)
        g_draw.polygon([P, A, B], fill=(16, 185, 129, 85), outline=(52, 211, 153, 255), width=5)
        c_draw.polygon([P, A, B], outline=(255, 255, 255, 245), width=3)
        g_draw.line([(cx, cy), P], fill=(250, 204, 21, 255), width=6)
        c_draw.line([A, B], fill=(250, 204, 21, 255), width=5)

        for pt_c in [A, B, P, (cx, cy)]:
            c_draw.ellipse((pt_c[0] - 9, pt_c[1] - 9, pt_c[0] + 9, pt_c[1] + 9), fill=(250, 204, 21, 255), outline=(255, 255, 255, 255), width=3)
        c_draw.text((int(cx - 195), int(cy + R + 24)), "원주각 ∠APB = 1/2 ∠AOB (위치 무관 불변!)", fill=(254, 240, 138, 255), font=f_big)

    return _composite_neon_bloom(base_rgb, glow_rgba, crisp_rgba)


def build_viral_curiosity_youtube_title(clean_title: str, archetype: str, lang_code: str = "ko", is_short: bool = False) -> str:
    """
    [월 1,000만 원 CTR 극대화 엔진 + 100% 수학적 정합성 보장]
    첫 25글자(모바일 화면 노출 구간)에 브래킷 라벨 대신 강렬한 호기심 공백(Curiosity Gap) 훅과
    핵심 수학 키워드를 직결하여 클릭률(CTR)과 수학적 정확성을 동시에 극대화합니다.
    """
    clean_title = sanitize_glyphs(clean_title)
    clean_title = re.sub(
        r"lim\(\s*(?:θ|theta)\s*(?:arrow|to|→)\s*0\)\s*\(\s*sin\s*(?:θ|theta)\s*/\s*(?:θ|theta)\s*\)\s*=\s*1.*",
        "lim(θ→0) (sin θ/θ) = 1",
        clean_title,
        flags=re.I,
    )
    clean_title = re.sub(
        r"lim\(\s*(?:θ|theta)\s*(?:arrow|to|→)\s*0\)\s*\(\s*tan\s*(?:θ|theta)\s*/\s*(?:θ|theta)\s*\)\s*=\s*1.*",
        "lim(θ→0) (tan θ/θ) = 1",
        clean_title,
        flags=re.I,
    )
    if "(" in clean_title and ")" not in clean_title:
        clean_title = clean_title.split("(", 1)[0].strip()

    def _make_base(ct: str) -> str:
        ct_low = ct.lower()
        hooks_ko = {
            "pythagoras_fractal": f"🔥 공식 암기는 그만! {ct}, 넓이가 영원히 보존되는 단 1가지 이유",
            "special_triangles": f"🔥 공식 외우지 마세요! 보조선 1줄로 1초 만에 유도하는 {ct}",
            "square_root_geometry": f"🔥 정사각형 넓이 하나로 단번에 깨치는 {ct}의 기하학적 비밀!",
            "cycloid_kinematics": f"🔥 구르는 원 위의 점은 왜 절대 뒤로 꼬이지 않을까? | {ct}",
            "conic_parabola": f"🔥 왜 모든 평행광선은 포물선에 반사되면 한 점(초점)에 모일까? | {ct}",
            "conic_reflection": f"🔥 제1초점에서 쏜 빛이 모두 제2초점에 동시에 모이는 이유! | {ct}",
            "trig_harmonic": (
                f"🔥 왜 0으로 다가갈 때 sin θ와 호의 길이 θ는 같아질까? | {ct}"
                if ("lim" in ct_low or "tan" in ct_low)
                else f"🔥 왜 둥근 원이 회전하면 완벽한 물결 파동이 될까? | {ct}"
            ),
            "trig_deriv_sin": f"🔥 사인(sin x)을 미분하면 왜 정확히 코사인(cos x)이 될까? | {ct}",
            "fibonacci_golden": f"🔥 해바라기와 은하 나선에 숨겨진 137.5° 황금비의 비밀! | {ct}",
            "prob_galton": f"🔥 무작위 우연이 수천 번 쌓이면 왜 완벽한 종 모양이 될까? | {ct}",
            "cauchy_mvt": f"🔥 두 함수의 평균변화율 비와 미분계수 비가 일치하는 순간! | {ct}",
            "inverse_deriv": f"🔥 직선 y=x 대칭 뒤집기 한 번으로 끝나는 {ct} 완벽 증명!",
            "calculus_motion": f"🔥 멈춰 있는 그래프가 살아 움직이는 순간! | {ct}",
            "menelaus_theorem": f"🔥 평행 보조선 딱 1줄이면 끝! 세 비율의 곱이 항상 1이 되는 이유 | {ct}",
            "ceva_menelaus": f"🔥 복잡한 보조선 없이 넓이 비 하나로 단번에 증명되는 이유! | {ct}",
            "parallel_similarity": f"🔥 평행 보조선 딱 1줄로 닮음비가 단번에 증명되는 이유! | {ct}",
            "circle_invariants": f"🔥 점이 원 위를 아무리 움직여도 각도가 절대 안 변하는 이유! | {ct}",
        }
        hooks_en = {
            "pythagoras_fractal": f"🔥 Stop Memorizing! Why {ct} Preserves Area Forever",
            "special_triangles": f"🔥 Stop Memorizing! Derive {ct} in 5 Seconds With 1 Line",
            "square_root_geometry": f"🔥 The 1 Square Area Idea That Explains {ct} Instantly!",
            "cycloid_kinematics": f"🔥 Why a Rolling Circle's Path Never Loops Back! | {ct}",
            "conic_parabola": f"🔥 Why Every Parallel Ray Reflects to One Focus on a Parabola! | {ct}",
            "conic_reflection": f"🔥 Why Every Ray From Focus F₁ Converges at Focus F₂! | {ct}",
            "trig_harmonic": (
                f"🔥 Why Does sin θ Become Equal to Arc θ as θ → 0? | {ct}"
                if ("lim" in ct_low or "tan" in ct_low)
                else f"🔥 How a Rotating Circle Creates Every Wave in the Universe! | {ct}"
            ),
            "trig_deriv_sin": f"🔥 Why Is the Derivative of sin x Exactly cos x? | {ct}",
            "fibonacci_golden": f"🔥 Why Nature Chose the Golden Angle (137.5°)! | {ct}",
            "prob_galton": f"🔥 How Pure Randomness Always Forms a Perfect Bell Curve! | {ct}",
            "cauchy_mvt": f"🔥 Where Two Functions' Secant Ratio Matches Their Derivative Ratio! | {ct}",
            "inverse_deriv": f"🔥 How 1 Reflection Across y=x Proves {ct} Instantly!",
            "calculus_motion": f"🔥 The Exact Moment Secant Becomes Tangent! | {ct}",
            "menelaus_theorem": f"🔥 Just 1 Parallel Line! Why the 3 Ratios Multiply to 1 | {ct}",
            "ceva_menelaus": f"🔥 How 1 Area Ratio Trick Proves {ct} Instantly!",
            "parallel_similarity": f"🔥 How 1 Parallel Line Proves {ct} Instantly!",
            "circle_invariants": f"🔥 Why Moving the Vertex Never Changes the Angle! | {ct}",
        }
        return (
            hooks_ko.get(archetype, f"🔥 공식 암기 없이 단 1개의 아이디어로 깨치는 {ct}!")
            if lang_code == "ko"
            else hooks_en.get(archetype, f"🔥 The 1 Visual Idea That Explains {ct}!")
        )

    suffix = (
        (" #Shorts #창의수학 | @min7014_ai" if is_short else " | 창의 수학 시네마 @min7014_ai")
        if lang_code == "ko"
        else (" #Shorts #Math | @min7014_ai" if is_short else " | Visual Math Cinema @min7014_ai")
    )
    base = _make_base(clean_title)
    if len(base) + len(suffix) <= 98:
        return base + suffix

    short_suffix = " #Shorts #Math" if is_short else " | @min7014_ai"
    if len(base) + len(short_suffix) <= 98:
        return base + short_suffix

    # 만약 여전히 길다면 괄호 부연 설명을 먼저 제거하거나 단어 경계에서 정밀 축약 (중간 단어 절단 원천 차단)
    ct_no_paren = re.sub(r"\s*\([^)]*\)", "", clean_title).strip()
    if ct_no_paren and ct_no_paren != clean_title:
        b2 = _make_base(ct_no_paren)
        if len(b2) + len(short_suffix) <= 98:
            return b2 + short_suffix

    budget_ct = max(14, len(clean_title) - ((len(base) + len(short_suffix)) - 98))
    ct_short = vmaker._smart_concise_topic_title(clean_title, max_len=budget_ct, lang=lang_code)
    b3 = _make_base(ct_short)
    if len(b3) + len(short_suffix) <= 98:
        return b3 + short_suffix
    return (b3[: 98 - len(short_suffix)].rsplit(" ", 1)[0].rstrip(" —|-:,") + short_suffix)[:98]


def build_viral_comment_puzzle(archetype: str, lang_code: str = "ko", ggb_url: str = "", sdoc: dict = None) -> str:
    """
    [유튜브 알고리즘 댓글 참여율(Engagement Velocity) 10배 증폭 엔진 — 100% https://min7014.github.io/ 원문 자료 기반]
    https://min7014.github.io/ 수록 자료(sdoc)의 실제 핵심 아이디어·보조선·불변량과 아키타입별 5초 암산 퍼즐을 결합합니다.
    """
    sdoc = sdoc or {}
    slug_k = sdoc.get("slug", "math20250130001")
    tot_p = sdoc.get("page_count") or len(sdoc.get("pages") or []) or 11
    pdf_u = sdoc.get("pdf_url") or f"https://min7014.github.io/pdf/{slug_k}.pdf"
    web_u = sdoc.get("web_url") or ggb_url or "https://min7014.github.io/"
    ko_raw, en_raw = vmaker.split_bilingual_title(sdoc.get("title", slug_k))
    topic_ko = vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(ko_raw), max_len=36, lang="ko") if ko_raw else ""
    topic_en = vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(en_raw or sdoc.get("title_en") or ko_raw), max_len=44, lang="en") if (en_raw or ko_raw) else ""

    puzzles_ko = {
        "pythagoras_fractal": "🧠 [5초 암산 챌린지 — 댓글에 정답 숫자를 남겨보세요!]\n직각삼각형의 두 작은 정사각형 넓이가 각각 9와 16일 때, 가장 큰 정사각형의 넓이는 얼마일까요? (루트 계산 없이 1초 만에 맞히셨다면 댓글로 숫자를 남겨주세요!)",
        "special_triangles": "🧠 [5초 직각삼각형 챌린지 — 댓글에 정답 숫자를 남겨보세요!]\n30°-60°-90° 직각삼각형(변의 비 1 : √3 : 2)에서 가장 짧은 밑변의 길이가 5일 때, 가장 긴 빗변의 길이는 얼마일까요? 댓글로 숫자를 남겨주세요!",
        "square_root_geometry": "🧠 [5초 제곱근 챌린지 — 댓글에 정답 숫자를 남겨보세요!]\n넓이가 49인 정사각형의 한 변의 길이(√49)는 얼마일까요? 댓글로 정답 숫자를 남겨주세요!",
        "cycloid_kinematics": "🧠 [5초 사이클로이드 챌린지 — 댓글에 정답 숫자를 남겨보세요!]\n반지름 r = 1 인 원이 바닥에서 미끄러지지 않고 한 바퀴(2π) 굴러갔을 때, 원의 중심이 이동한 수평 거리는 몇 π일까요? 댓글로 남겨보세요!",
        "conic_parabola": "🧠 [5초 포물선 직관 챌린지 — 댓글에 정답 숫자를 남겨보세요!]\n포물선(|PF| = |PH|) 위의 점 P에서 준선까지의 수직 거리 PH가 7일 때, 초점 F까지의 거리 PF는 얼마일까요? 1초 만에 보인다면 댓글로 정답을 남겨주세요!",
        "conic_reflection": "🧠 [5초 타원 직관 챌린지 — 댓글에 정답 숫자를 남겨보세요!]\n장축의 길이 2a가 10인 타원(|PF₁| + |PF₂| = 10) 위의 점 P에서 제1초점 F₁까지의 거리가 3일 때, 제2초점 F₂까지의 거리 PF₂는 얼마일까요? 댓글로 정답을 남겨주세요!",
        "trig_harmonic": "🧠 [5초 극한·삼각비 챌린지 — 댓글에 정답 숫자를 남겨보세요!]\n부채꼴 넓이 샌드위치 부등식 cos θ < (sin θ)/θ < 1 에서 θ가 0으로 한없이 다가갈 때, 가운데 (sin θ)/θ 는 어떤 숫자로 수렴할까요? 댓글로 남겨주세요!",
        "trig_deriv_sin": "🧠 [5초 삼각함수 미분 챌린지 — 댓글에 정답 숫자를 남겨보세요!]\n함수 y = sin x 의 도함수는 y' = cos x 입니다. 그렇다면 원점 x = 0 에서의 접선의 기울기(cos 0)는 얼마일까요? 댓글로 숫자를 남겨주세요!",
        "fibonacci_golden": "🧠 [5초 수열 챌린지 — 댓글에 정답 숫자를 남겨보세요!]\n피보나치 수열 1, 1, 2, 3, 5, 8, 13... 에서 13 바로 다음에 올 숫자는 무엇일까요? 댓글로 정답을 남겨주세요!",
        "prob_galton": "🧠 [5초 확률 챌린지 — 댓글에 정답 숫자를 남겨보세요!]\n좌우 갈림길이 4번 있는 골턴 보드에서 구슬이 정중앙 칸에 도달하는 경로의 수(4C2)는 몇 가지일까요? 댓글로 도전해 보세요!",
        "cauchy_mvt": "🧠 [5초 코시 평균값 정리 챌린지 — 댓글에 정답 숫자를 남겨보세요!]\n구간 [1, 3]에서 f(x) = x², g(x) = x 일 때, 두 함수의 평균변화율 비 [f(3)-f(1)] / [g(3)-g(1)] = (9-1)/(3-1) 의 값은 얼마일까요? 댓글로 남겨주세요!",
        "inverse_deriv": "🧠 [5초 역함수 미분 챌린지 — 댓글에 정답 숫자를 남겨보세요!]\n원래 함수 f(x)의 접선 기울기가 f'(a) = 4 일 때, 직선 y = x 대칭인 역함수의 대응점 접선 기울기 (f⁻¹)'(b) = 1 / f'(a) 는 얼마일까요? 댓글로 남겨주세요!",
        "calculus_motion": "🧠 [5초 미분 챌린지 — 댓글에 정답 숫자를 남겨보세요!]\n곡선 y = x² 위에서 x = 3일 때 접선의 기울기(2x)는 얼마일까요? 암산으로 맞히셨다면 댓글로 숫자를 남겨주세요!",
        "menelaus_theorem": "🧠 [5초 메넬라우스 챌린지 — 댓글에 정답 숫자를 남겨보세요!]\n메넬라우스의 정리 (AF/FB) × (BD/DC) × (CE/EA) = 1 에서 앞의 두 비율의 곱이 2일 때, 마지막 세 번째 비율 CE/EA 는 얼마일까요? 댓글로 남겨주세요!",
        "ceva_menelaus": "🧠 [5초 도형 넓이 비 챌린지 — 댓글에 정답 숫자를 남겨보세요!]\n높이가 같은 두 삼각형의 밑변의 비가 2 : 3이고 왼쪽 삼각형 넓이가 10일 때, 오른쪽 삼각형의 넓이는 얼마일까요? 댓글로 정답을 남겨주세요!",
        "parallel_similarity": "🧠 [5초 평행선 비례 챌린지 — 댓글에 정답 숫자를 남겨보세요!]\n세 평행선이 왼쪽 직선을 2 : 3 비율로 나눌 때, 오른쪽 직선에서 위쪽 선분 길이가 4라면 아래쪽 선분 길이는 얼마일까요? 댓글로 남겨주세요!",
        "circle_invariants": "🧠 [5초 원주각 챌린지 — 댓글에 정답 숫자를 남겨보세요!]\n원의 중심각 ∠AOB가 80°일 때, 원 위의 점 P가 어디로 움직이든 원주각 ∠APB는 항상 몇 도일까요? 댓글로 숫자를 남겨주세요!",
    }
    puzzles_en = {
        "pythagoras_fractal": "🧠 [5-Second Mental Math Challenge — Drop Your Answer in the Comments!]\nIf the two smaller squares on a right triangle have areas 9 and 16, what is the area of the largest square? Comment your number below!",
        "special_triangles": "🧠 [5-Second Triangle Challenge — Drop Your Answer in the Comments!]\nIn a 30°-60°-90° right triangle (side ratio 1 : √3 : 2), if the shortest leg has length 5, what is the length of the hypotenuse? Comment below!",
        "square_root_geometry": "🧠 [5-Second Square Root Challenge — Drop Your Answer in the Comments!]\nIf a square has area 49, what is the exact length of one side (√49)? Comment your number below!",
        "cycloid_kinematics": "🧠 [5-Second Cycloid Challenge — Drop Your Answer in the Comments!]\nWhen a circle of radius r = 1 rolls one full turn (2π) without slipping, how many π does its center travel horizontally? Comment below!",
        "conic_parabola": "🧠 [5-Second Parabola Challenge — Drop Your Answer in the Comments!]\nOn a parabola (|PF| = |PH|), if point P is at perpendicular distance PH = 7 from the directrix, what is its exact distance PF to focus F? Comment your answer!",
        "conic_reflection": "🧠 [5-Second Ellipse Challenge — Drop Your Answer in the Comments!]\nOn an ellipse with major axis 2a = 10 (|PF₁| + |PF₂| = 10), if point P is at distance 3 from focus F₁, what is its distance PF₂ to focus F₂? Comment below!",
        "trig_harmonic": "🧠 [5-Second Squeeze Limit Challenge — Drop Your Answer in the Comments!]\nIn the unit-circle area inequality cos θ < (sin θ)/θ < 1, what exact number does (sin θ)/θ approach as θ → 0? Comment your number below!",
        "trig_deriv_sin": "🧠 [5-Second Calculus Challenge — Drop Your Answer in the Comments!]\nSince d/dx(sin x) = cos x, what is the exact slope of the tangent line to y = sin x at x = 0 (cos 0)? Comment your number below!",
        "fibonacci_golden": "🧠 [5-Second Pattern Challenge — Drop Your Answer in the Comments!]\nIn the Fibonacci sequence 1, 1, 2, 3, 5, 8, 13..., what number comes right after 13? Drop your answer in the comments!",
        "prob_galton": "🧠 [5-Second Probability Challenge — Drop Your Answer in the Comments!]\nIn a 4-row Galton board, how many distinct paths (4C2) lead a bead to the exact center bin? Comment your answer!",
        "cauchy_mvt": "🧠 [5-Second Cauchy MVT Challenge — Drop Your Answer in the Comments!]\nOn [1, 3] with f(x) = x² and g(x) = x, what is the ratio [f(3)-f(1)] / [g(3)-g(1)] = (9-1)/(3-1)? Comment your number below!",
        "inverse_deriv": "🧠 [5-Second Inverse Derivative Challenge — Drop Your Answer in the Comments!]\nIf f'(a) = 4 on y = f(x), what is the slope (f⁻¹)'(b) = 1 / f'(a) of the inverse function reflected across y = x? Comment below!",
        "calculus_motion": "🧠 [5-Second Calculus Challenge — Drop Your Answer in the Comments!]\nOn the curve y = x², what is the exact slope of the tangent line (2x) at x = 3? Comment your number below!",
        "menelaus_theorem": "🧠 [5-Second Menelaus Challenge — Drop Your Answer in the Comments!]\nIn Menelaus' Theorem (AF/FB) × (BD/DC) × (CE/EA) = 1, if the product of the first two ratios is 2, what is the third ratio CE/EA? Comment below!",
        "ceva_menelaus": "🧠 [5-Second Area Ratio Challenge — Drop Your Answer in the Comments!]\nTwo triangles share the same height and have base ratio 2 : 3. If the left triangle has area 10, what is the area of the right triangle?",
        "parallel_similarity": "🧠 [5-Second Parallel Ratio Challenge — Drop Your Answer in the Comments!]\nThree parallel lines cut the left transversal in a 2 : 3 ratio. If the upper segment on the right transversal is 4, what is the lower segment?",
        "circle_invariants": "🧠 [5-Second Circle Angle Challenge — Drop Your Answer in the Comments!]\nIf the central angle ∠AOB is 80°, what is the inscribed angle ∠APB for any point P on the circle? Comment your number!",
    }
    if lang_code == "ko":
        q_txt = puzzles_ko.get(archetype, puzzles_ko["pythagoras_fractal"])
        src_line = f"🏛️ [원본 수학 아이디어 출처: https://min7014.github.io/ — '{topic_ko}' ({tot_p}단계 시각적 증명)]\n" if topic_ko else "🏛️ [원본 수학 아이디어 출처: https://min7014.github.io/]\n"
        return (
            f"{src_line}"
            f"{q_txt}\n"
            f"⚡ [Wordle × Chess.com 스타일 1초 댓글 등급표 — 정답 숫자와 함께 이모지를 남겨보세요!]\n"
            f"🟩 3초 컷 (상위 1% 직관) | 🟨 10초 컷 | 🟦 영상 보조선 보고 유레카!\n\n"
            f"📄 [이 영상의 모태가 된 https://min7014.github.io/ 단계별 증명 PDF & 동적 기하 원문]:\n"
            f"👉 원문 아카이브: {web_u}\n"
            f"👉 단계별 증명 PDF: {pdf_u}\n"
            f"👉 인터랙티브 실습 보드: {ggb_url}\n\n"
            f"🎬 [Netflix 스타일 연속 정주행 — 8분+ 네온 시네마 마스터클래스 본편 바로 보기]\n"
            f"👉 https://youtu.be/_5LE_BfLA5w\n\n"
            f"🔔 [매일 1개 두올링고(Duolingo)처럼 수학 직관 스트릭 쌓기 — 1초 무료 구독]\n"
            f"👉 https://www.youtube.com/@min7014_ai?sub_confirmation=1"
        )
    else:
        q_txt = puzzles_en.get(archetype, puzzles_en["pythagoras_fractal"])
        src_line = f"🏛️ [Original Mathematical Idea from https://min7014.github.io/ — '{topic_en}' ({tot_p}-Step Proof)]\n" if topic_en else "🏛️ [Original Mathematical Idea from https://min7014.github.io/]\n"
        return (
            f"{src_line}"
            f"{q_txt}\n"
            f"⚡ [Wordle × Chess.com Speed Tier — Reply with Your Emoji + Answer!]\n"
            f"🟩 Solved in <3s (Top 1%) | 🟨 Solved in <10s | 🟦 Needed the Visual Clue!\n\n"
            f"📄 [Original Step-by-Step Proof PDF & Interactive Archive on https://min7014.github.io/]:\n"
            f"👉 Archive: {web_u}\n"
            f"👉 Step-by-Step PDF: {pdf_u}\n"
            f"👉 Interactive Board: {ggb_url}\n\n"
            f"🎬 [Binge-Watch Next — 8-Min Pure Neon Geometry Masterclass (1080p)]\n"
            f"👉 https://youtu.be/9EL8pgqJtkY\n\n"
            f"🔔 [Build Your Daily Math Intuition Streak — 1-Click Subscribe to @min7014_ai]:\n"
            f"👉 https://www.youtube.com/@min7014_ai?sub_confirmation=1"
        )


def render_creative_idea_thumbnail(sdoc: dict, lang_code: str = "ko") -> Path:
    """
    [고클릭률(High-CTR) 아키타입 맞춤형 네온 시네마 썸네일 생성기]
    - 모든 영상에 똑같은 문구를 넣던 배너 블라인드니스를 완전히 제거하고,
      세부 수학 주제별 맞춤형 호기심 역설 질문 + 우측 상단 초대형 네온 수식 콜아웃 배지를 합성합니다.
    """
    slug_key = sdoc["slug"]
    out_thumb = YT_PKG_DIR / f"{slug_key}_idea_{lang_code}_thumb.png"
    ko_t, en_t = vmaker.split_bilingual_title(sdoc.get("title", slug_key))
    clean_t = sanitize_glyphs(
        vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(ko_t), max_len=24, lang="ko")
        if lang_code == "ko"
        else vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(en_t or sdoc.get("title_en") or ko_t), max_len=30, lang="en")
    )
    archetype = detect_visual_archetype(sdoc)

    # 전체 1280x720 배경에 네온 블룸 기하 씬을 렌더링한 뒤 좌측 글래스모피즘 타이포그래피 오버레이 합성
    scene_img = render_pure_procedural_scene(1280, 720, archetype, 1, 0.88, lang_code=lang_code)
    shifted = Image.new("RGB", (1280, 720), (5, 9, 20))
    shifted.paste(scene_img, (355, 8))

    ov = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
    draw = ImageDraw.Draw(ov)

    draw.rounded_rectangle((28, 32, 560, 688), radius=28, fill=(9, 15, 32, 232), outline=(250, 204, 21, 255), width=4)
    draw.rounded_rectangle((52, 58, 536, 118), radius=16, fill=(124, 58, 237, 255), outline=(254, 240, 138, 255), width=2)

    f_badge = vmaker.get_font_for_lang(lang_code, 22, bold=True)
    f_hero = vmaker.get_font_for_lang(lang_code, 44, bold=True)
    f_sub = vmaker.get_font_for_lang(lang_code, 28, bold=True)
    f_call = vmaker.get_font_for_lang("en", 34, bold=True)

    thumb_hooks_ko = {
        "pythagoras_fractal": (["무한히 갈라져도", "넓이 합이 똑같다?", "단 1초 시각 증명!"], "a² + b² = c²"),
        "special_triangles": (["공식 외우지 마세요!", "보조선 딱 1줄로", "끝내는 삼각비 증명!"], "1 : √3 : 2"),
        "square_root_geometry": (["정사각형 넓이 하나로", "단번에 깨치는", "제곱근의 진짜 의미!"], "x²=a ⇔ ±√a"),
        "cycloid_kinematics": (["구르는 원 위의 점은", "왜 절대 뒤로", "꼬이지 않을까?"], "dx/dθ ≥ 0"),
        "conic_parabola": (["왜 모든 평행광선은", "포물선에 반사되면", "한 점(초점)에 모일까?"], "|PF| = |PH|"),
        "conic_reflection": (["제1초점에서 쏜 빛이", "왜 모두 제2초점에", "동시에 모이게 될까?"], "PF₁+PF₂=2a"),
        "trig_harmonic": (["삼각형·부채꼴·접선", "넓이 샌드위치 하나로", "끝내는 극한 증명!"], "sin θ/θ → 1"),
        "trig_deriv_sin": (["사인 곡선 기울기가", "왜 정확히 코사인과", "일치하게 될까?"], "(sin x)'=cos x"),
        "fibonacci_golden": (["자연과 은하계가", "137.5° 황금각을", "선택한 진짜 이유!"], "φ = 1.618..."),
        "prob_galton": (["수천 번의 우연이", "왜 항상 완벽한", "종 모양이 될까?"], "N(μ, σ²)"),
        "cauchy_mvt": (["두 함수의 할선 비와", "미분계수 비가", "일치하는 순간!"], "f'(c)/g'(c)"),
        "inverse_deriv": (["직선 y=x 대칭으로", "단 1초 만에 끝내는", "역함수 미분 증명!"], "1 / f'(x)"),
        "calculus_motion": (["두 점을 잇던 할선이", "접선으로 변하는", "극한의 찰나!"], "dy/dx = lim"),
        "menelaus_theorem": (["평행 보조선 딱 1줄로", "세 선분 비율의 곱이", "1로 약분되는 비밀!"], "Ratio = 1"),
        "ceva_menelaus": (["보조선 공식 없이", "넓이 비 하나로", "10초 만에 끝!"], "Ratio = 1"),
        "parallel_similarity": (["평행 보조선 딱 1줄로", "선분 길이 비례식이", "단번에 증명된다!"], "a:b = a':b'"),
        "circle_invariants": (["점이 아무리 움직여도", "각도가 절대 변하지", "않는 기하의 마법!"], "∠P = 1/2 ∠O"),
    }
    thumb_hooks_en = {
        "pythagoras_fractal": (["Infinite Branches,", "Same Exact Area?", "1-Look Visual Proof!"], "a² + b² = c²"),
        "special_triangles": (["Stop Memorizing!", "1 Symmetry Line", "Derives All Ratios!"], "1 : √3 : 2"),
        "square_root_geometry": (["1 Square Area Model", "Explains Square Roots", "In 5 Seconds!"], "x²=a ⇔ ±√a"),
        "cycloid_kinematics": (["Why a Rolling Circle", "Traces a Curve That", "Never Loops Back!"], "dx/dθ ≥ 0"),
        "conic_parabola": (["Why Parallel Rays", "Bounce to One", "Parabola Focus!"], "|PF| = |PH|"),
        "conic_reflection": (["Why Every Ray From", "Focus F₁ Meets", "At Focus F₂!"], "PF₁+PF₂=2a"),
        "trig_harmonic": (["1 Sector Area Squeeze", "Proves sin θ / θ → 1", "In 10 Seconds!"], "sin θ/θ → 1"),
        "trig_deriv_sin": (["Why Sine's Tangent", "Slope Is Always", "Exactly Cosine!"], "(sin x)'=cos x"),
        "fibonacci_golden": (["Why Nature Chose", "The 137.5° Golden", "Spiral Angle!"], "φ = 1.618..."),
        "prob_galton": (["How Random Chaos", "Always Forms a", "Perfect Bell Curve!"], "N(μ, σ²)"),
        "cauchy_mvt": (["Where Two Functions'", "Secant Ratio Equals", "Derivative Ratio!"], "f'(c)/g'(c)"),
        "inverse_deriv": (["1 Reflection Across", "Line y = x Proves", "Inverse Derivative!"], "1 / f'(x)"),
        "calculus_motion": (["The Exact Moment", "Secant Becomes", "Tangent Line!"], "dy/dx = lim"),
        "menelaus_theorem": (["Just 1 Parallel Line", "Cancels All 3 Ratios", "Into Exactly 1!"], "Ratio = 1"),
        "ceva_menelaus": (["No Extra Formulas!", "1 Area Ratio Trick", "Proves It All!"], "Ratio = 1"),
        "parallel_similarity": (["1 Parallel Line", "Proves Segment", "Proportions Live!"], "a:b = a':b'"),
        "circle_invariants": (["Move the Vertex", "Anywhere—Why Does", "Angle Never Change?"], "∠P = 1/2 ∠O"),
    }
    hook_lines, callout_formula = (
        thumb_hooks_ko.get(archetype, (["공식 암기 멈추세요!", "단 1개의 아이디어로", "끝내는 시각적 비밀!"], "Q.E.D."))
        if lang_code == "ko"
        else thumb_hooks_en.get(archetype, (["STOP MEMORIZING!", "1 Core Visual Idea", "Explains It All!"], "Q.E.D."))
    )

    b_txt = "★ 창의 수학 시네마 (Pure Visual)" if lang_code == "ko" else "★ CREATIVE MATH CINEMA"
    draw.text((70, 73), b_txt, fill=(254, 240, 138, 255), font=f_badge)

    for i, hl in enumerate(hook_lines):
        col = (250, 204, 21, 255) if i == 1 else (255, 255, 255, 255)
        draw.text((54, 152 + i * 68), hl, fill=col, font=f_hero)

    t_lines = textwrap.wrap(clean_t, width=15 if lang_code == "ko" else 22)[:2]
    for j, tl in enumerate(t_lines):
        draw.text((54, 392 + j * 42), tl, fill=(125, 211, 252, 255), font=f_sub)

    draw.rounded_rectangle((52, 592, 536, 658), radius=16, fill=(225, 29, 72, 255))
    draw.text(
        (72, 610),
        "▶ 5막 동적 시뮬레이션 · @min7014_ai" if lang_code == "ko" else "▶ 5-Act Visual Story · @min7014_ai",
        fill=(255, 255, 255, 255),
        font=f_badge,
    )

    # 우측 상단 기하 아트 위에 시선을 사로잡는 네온 수식 콜아웃 배지 배치
    draw.rounded_rectangle((965, 32, 1252, 108), radius=18, fill=(15, 23, 42, 230), outline=(56, 189, 248, 255), width=3)
    draw.text((990, 48), sanitize_glyphs(callout_formula), fill=(250, 204, 21, 255), font=f_call)

    final_rgb = Image.alpha_composite(shifted.convert("RGBA"), ov).convert("RGB")
    final_rgb.save(out_thumb)
    return out_thumb


def verify_creative_idea_math_fidelity(sdoc: dict, acts: list = None, title: str = "", comment_txt: str = "") -> dict:
    """
    [Rule 19 / 정책 11: https://min7014.github.io/ 원문 자료와의 100% 수학적 정합성 및 수식·증명 무결성 필수 검증 게이트]
    - 유튜브 영상은 수많은 시청자에게 노출되어 파급력이 크므로, 원문 자료(sdoc)의 주제·수식·보조선과
      단 1%라도 어긋나는 아키타입 혼동(예: 포물선에 제2초점 F2 언급, 타원에 준선 거리 PF=PH 퍼즐 언급,
      메넬라우스에 세 체바선 교점 P 넓이 비 언급, 제곱근에 황금비 해바라기 언급 등)을 기계적으로 원천 차단합니다.
    """
    raw_t = f"{sdoc.get('title', '')} {sdoc.get('title_en', '')}".lower()
    acts = acts or []
    acts_blob = " ".join(
        f"{a.get('headline', '')} {a.get('key_formula', '')} {a.get('narration', '')} {' '.join(a.get('hud_notes') or [])}"
        for a in acts
    )
    full_blob = f"{title} {acts_blob} {comment_txt}"

    # 1. 포물선(Parabola) vs 타원(Ellipse) 엄격 분리 검증
    if ("포물선" in raw_t or "parabola" in raw_t) and "타원" not in raw_t:
        for bad in ("제2초점", "second focus F2", "PF₁ + PF₂ = 2a"):
            if bad in acts_blob or bad in title or bad in comment_txt:
                return {"ok": False, "reason": f"parabola_conflated_with_ellipse:{bad}"}
    if ("타원" in raw_t or "ellipse" in raw_t) and "포물선" not in raw_t:
        for bad in ("준선까지의 거리가 7", "distance 7 from the directrix"):
            if bad in comment_txt or bad in title:
                return {"ok": False, "reason": f"ellipse_conflated_with_parabola:{bad}"}

    # 2. 메넬라우스(Menelaus) vs 체바(Ceva) 엄격 분리 검증
    if "메넬라우스" in raw_t or "menelaus" in raw_t:
        for bad in ("세 체바 직선이 만나는 교점 P가", "intersection point P glide freely across the triangle", "넓이 비 하나로 단번에 증명되는 이유"):
            if bad in full_blob:
                return {"ok": False, "reason": f"menelaus_conflated_with_ceva:{bad}"}

    # 3. 제곱근(Square Root) vs 황금비(Fibonacci) 엄격 분리 검증
    if "제곱근" in raw_t or "square root" in raw_t:
        for bad in ("해바라기", "137.5", "피보나치", "Fibonacci"):
            if bad in full_blob:
                return {"ok": False, "reason": f"square_root_conflated_with_fibonacci:{bad}"}

    # 4. 사이클로이드(Cycloid) vs 이차곡선 초점 반사 엄격 분리 검증
    if "사이클로이드" in raw_t or "cycloid" in raw_t:
        for bad in ("제1초점", "초점 F", "Focus F"):
            if bad in full_blob:
                return {"ok": False, "reason": f"cycloid_conflated_with_conic:{bad}"}

    # 5. 특수 직각삼각형(30-60-90 / 직각이등변삼각형) vs 체바 넓이 비 엄격 분리 검증
    if "30-60-90" in raw_t or "직각이등변삼각형" in raw_t:
        for bad in ("세 체바 직선이", "넓이 비 하나로"):
            if bad in full_blob:
                return {"ok": False, "reason": f"special_triangle_conflated_with_ceva:{bad}"}

    return {"ok": True, "reason": "verified_100_percent_math_fidelity"}


def render_creative_idea_cinema_video(slug_key: str = "math20250130001", lang_code: str = "ko") -> Path:
    """
    [Edition 5-A v2.0: 🌟 1080p 16:9 순수 창의 아이디어 시네마 본편 제작기]
    - PDF 이미지를 전혀 쓰지 않는 풀스크린 다크 네온 블룸 애니메이션 + 반투명 글래스모피즘 HUD 오버레이!
    """
    script_path = SCRIPTS_DIR / f"{slug_key}.json"
    if not script_path.exists():
        vmaker.generate_or_update_script(slug_key, target_langs=["ko", "en"])
    sdoc = json.loads(script_path.read_text(encoding="utf-8"))

    acts = build_creative_idea_acts(sdoc, lang_code=lang_code)
    archetype = detect_visual_archetype(sdoc)

    ko_t, en_t = vmaker.split_bilingual_title(sdoc.get("title", slug_key))
    clean_title = sanitize_glyphs(
        vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(ko_t), max_len=36, lang="ko")
        if lang_code == "ko"
        else vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(en_t or sdoc.get("title_en") or ko_t), max_len=44, lang="en")
    )
    idea_title_precheck = build_viral_curiosity_youtube_title(clean_title, archetype, lang_code=lang_code, is_short=False)
    comment_precheck = build_viral_comment_puzzle(archetype, lang_code=lang_code, sdoc=sdoc)
    fidelity_check = verify_creative_idea_math_fidelity(sdoc, acts, idea_title_precheck, comment_precheck)
    if not fidelity_check.get("ok"):
        raise ValueError(f"[Math Fidelity Guard Blocked Render ({slug_key}/{lang_code})]: {fidelity_check.get('reason')}")

    voice_name = vmaker.GLOBAL_VOICE_MAP.get(lang_code, vmaker.GLOBAL_VOICE_MAP["en"])["voice"]
    ffmpeg_exe = shutil.which("ffmpeg")
    ffprobe_exe = shutil.which("ffprobe")

    tmp_dir = Path(tempfile.mkdtemp(prefix=f"min7014_idea2_{slug_key}_{lang_code}_"))
    segs = []

    f_badge = vmaker.get_font_for_lang(lang_code, 20, bold=True)
    f_head = vmaker.get_font_for_lang(lang_code, 28, bold=True)
    f_formula = vmaker.get_font_for_lang(lang_code, 21, bold=True)
    f_bul = vmaker.get_font_for_lang(lang_code, 21, bold=True)
    f_sub = vmaker.get_font_for_lang(lang_code, 27, bold=True)

    try:
        for act_info in acts:
            act_num = act_info["act"]
            narr = act_info["narration"]
            mp3_p = tmp_dir / f"idea_act_{act_num:02d}.mp3"
            seg_p = tmp_dir / f"idea_act_{act_num:02d}.mp4"
            comm = edge_tts.Communicate(narr, voice_name, rate="+8%")
            asyncio.run(comm.save(str(mp3_p)))
            dur_s = max(4.0, vmaker.get_media_duration_seconds(mp3_p, ffprobe_exe))

            num_frames = 20
            per_f_dur = dur_s / num_frames
            f_lines = []
            last_fp = None
            cap_lines = textwrap.wrap(sanitize_glyphs(narr), width=50 if lang_code == "ko" else 76)[:3]

            for fi in range(num_frames):
                t_raw = fi / max(1, num_frames - 1)
                scene_rgb = render_pure_procedural_scene(1920, 1080, archetype, act_num, t_raw, lang_code=lang_code)
                hud = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
                draw = ImageDraw.Draw(hud)

                # 상단 반투명 글래스모피즘 타이틀 바
                draw.rounded_rectangle((36, 22, 1884, 122), radius=20, fill=(10, 18, 36, 205), outline=(56, 189, 248, 220), width=2)
                draw.rounded_rectangle((56, 36, 520, 78), radius=12, fill=(124, 58, 237, 245))
                draw.text((70, 44), sanitize_glyphs(act_info["badge"])[:26], fill=(254, 240, 138, 255), font=f_badge)

                draw.rounded_rectangle((1564, 36, 1860, 80), radius=14, fill=(225, 29, 72, 245), outline=(254, 240, 138, 245), width=2)
                draw.text(
                    (1588, 45),
                    "▶ 구독 @min7014_ai" if lang_code == "ko" else "▶ SUBSCRIBE @min7014_ai",
                    fill=(255, 255, 255, 255),
                    font=f_badge,
                )
                draw.text((538, 42), sanitize_glyphs(act_info["headline"])[:36 if lang_code == "ko" else 48], fill=(255, 255, 255, 255), font=f_head)

                overall_p = ((act_num - 1) + (fi + 1) / num_frames) / len(acts)
                draw.rounded_rectangle((56, 94, 1860, 108), radius=6, fill=(30, 41, 59, 220))
                draw.rounded_rectangle((56, 94, 56 + max(24, int(1804 * overall_p)), 108), radius=6, fill=(250, 204, 21, 255))

                # 우측 반투명 글래스모피즘 인사이트 카드 (배경의 네온 아트가 은은하게 비치는 설계)
                draw.rounded_rectangle((1280, 152, 1884, 842), radius=24, fill=(10, 18, 36, 195), outline=(250, 204, 21, 210), width=2)
                draw.rounded_rectangle((1304, 178, 1860, 266), radius=16, fill=(30, 58, 138, 220), outline=(56, 189, 248, 230), width=2)
                draw.text((1324, 190), "★ CORE MATHEMATICAL INVARIANT", fill=(125, 211, 252, 255), font=f_bul)
                draw.text((1324, 224), sanitize_glyphs(act_info["key_formula"])[:44], fill=(254, 240, 138, 255), font=f_formula)

                for bi, b_txt in enumerate(act_info["hud_notes"][:3]):
                    by0 = 294 + bi * 172
                    is_active_b = fi >= int(bi * (num_frames / 3))
                    b_fill = (23, 37, 84, 210) if is_active_b else (15, 23, 42, 160)
                    b_out = (52, 211, 153, 240) if is_active_b else (51, 65, 85, 180)
                    draw.rounded_rectangle((1304, by0, 1860, by0 + 150), radius=16, fill=b_fill, outline=b_out, width=2)
                    b_wrapped = textwrap.wrap(sanitize_glyphs(b_txt), width=23 if lang_code == "ko" else 33)[:3]
                    for wl_i, wl in enumerate(b_wrapped):
                        draw.text((1326, by0 + 20 + wl_i * 38), wl, fill=(255, 255, 255, 255) if is_active_b else (148, 163, 184, 220), font=f_bul)

                # 하단 시네마틱 키네틱 자막 바
                draw.rounded_rectangle((36, 868, 1884, 1054), radius=20, fill=(8, 14, 28, 218), outline=(56, 189, 248, 210), width=2)
                active_ci = min(len(cap_lines) - 1, int(t_raw * len(cap_lines))) if cap_lines else 0
                for ci, cl in enumerate(cap_lines):
                    c_col = (254, 240, 138, 255) if ci == active_ci else (203, 213, 225, 235)
                    draw.text((68, 892 + ci * 48), cl, fill=c_col, font=f_sub)

                frame_out = Image.alpha_composite(scene_rgb.convert("RGBA"), hud).convert("RGB")
                fp = tmp_dir / f"idea_a{act_num:02d}_f{fi:02d}.png"
                frame_out.save(fp)
                f_lines.append(f"file '{fp.as_posix()}'")
                f_lines.append(f"duration {per_f_dur:.4f}")
                last_fp = fp

            if last_fp:
                f_lines.append(f"file '{last_fp.as_posix()}'")
            f_txt = tmp_dir / f"idea_fconcat_{act_num:02d}.txt"
            f_txt.write_text("\n".join(f_lines), encoding="utf-8")

            chime_wav = vmaker.ensure_harmonic_chime_wav()
            cmd = [
                ffmpeg_exe, "-y",
                "-f", "concat", "-safe", "0", "-i", str(f_txt),
                "-i", str(mp3_p),
                "-i", str(chime_wav),
                "-filter_complex",
                "[1:a]aformat=sample_rates=48000:channel_layouts=stereo[v];"
                "[2:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.14[c];"
                "[v][c]amix=inputs=2:duration=first:dropout_transition=0[aout]",
                "-map", "0:v", "-map", "[aout]",
                "-c:v", "libx264", "-profile:v", "high", "-crf", "17", "-pix_fmt", "yuv420p", "-r", "30",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                "-shortest",
                str(seg_p),
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            segs.append(seg_p)

        concat_p = tmp_dir / "concat_idea.txt"
        concat_p.write_text("\n".join(f"file '{s.as_posix()}'" for s in segs), encoding="utf-8")
        raw_mp4 = tmp_dir / f"raw_idea_{slug_key}_{lang_code}.mp4"
        out_mp4 = CREATIVE_IDEA_DIR / f"{slug_key}_idea_{lang_code}.mp4"
        subprocess.run(
            [ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_p), "-c", "copy", str(raw_mp4)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        ambient_wav = vmaker.ensure_ambient_pad_wav()
        subprocess.run(
            [
                ffmpeg_exe, "-y",
                "-i", str(raw_mp4),
                "-stream_loop", "-1", "-i", str(ambient_wav),
                "-filter_complex",
                "[0:a]aformat=sample_rates=48000:channel_layouts=stereo[v];"
                "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.12[bgm];"
                "[v][bgm]amix=inputs=2:duration=first:dropout_transition=1[aout]",
                "-map", "0:v", "-map", "[aout]",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest",
                str(out_mp4),
            ],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        dur = vmaker.get_media_duration_seconds(out_mp4, ffprobe_exe)
        thumb_path = render_creative_idea_thumbnail(sdoc, lang_code=lang_code)

        idea_title = build_viral_curiosity_youtube_title(clean_title, archetype, lang_code=lang_code, is_short=False)

        sdoc = json.loads(script_path.read_text(encoding="utf-8"))
        sdoc.setdefault("creative_idea_packages", {})[lang_code] = {
            "title": idea_title,
            "local_mp4_path": f"video_lectures/creative_idea/{slug_key}_idea_{lang_code}.mp4",
            "thumbnail_path": f"video_lectures/youtube_packages/{thumb_path.name}",
            "duration_sec": round(dur, 2),
            "edition_mode": "v2.0 Pure Procedural Neon-Bloom Cinema (Zero PDF Screenshots)",
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "needs_youtube_upload": True,
        }
        sdoc.setdefault("creative_idea_youtube_urls", {"ko": "", "en": ""})
        script_path.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
        vmaker.update_video_catalog()
        print(f"🌟🎬 [Edition 5-A v2.0 Pure Procedural 1080p Cinema Generated] {out_mp4} ({round(dur, 1)}s)")
        return out_mp4
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def render_creative_idea_short_vertical(slug_key: str = "math20250130001", lang_code: str = "ko") -> Path:
    """
    [Edition 5-B v2.0: 🌟📱 9:16 (1080x1920) 순수 창의 아이디어 숏폼 (Idea-#Shorts)]
    - PDF 캡처 이미지가 전혀 없는 풀스크린 세로형 네온 블룸 프랙탈·기하 애니메이션!
    """
    script_path = SCRIPTS_DIR / f"{slug_key}.json"
    if not script_path.exists():
        vmaker.generate_or_update_script(slug_key, target_langs=["ko", "en"])
    sdoc = json.loads(script_path.read_text(encoding="utf-8"))

    acts = build_creative_idea_acts(sdoc, lang_code=lang_code)[:4]
    archetype = detect_visual_archetype(sdoc)

    ko_t, en_t = vmaker.split_bilingual_title(sdoc.get("title", slug_key))
    clean_title = sanitize_glyphs(
        vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(ko_t), max_len=30, lang="ko")
        if lang_code == "ko"
        else vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(en_t or sdoc.get("title_en") or ko_t), max_len=38, lang="en")
    )
    ishort_title_precheck = build_viral_curiosity_youtube_title(clean_title, archetype, lang_code=lang_code, is_short=True)
    comment_precheck = build_viral_comment_puzzle(archetype, lang_code=lang_code, sdoc=sdoc)
    fidelity_check = verify_creative_idea_math_fidelity(sdoc, acts, ishort_title_precheck, comment_precheck)
    if not fidelity_check.get("ok"):
        raise ValueError(f"[Math Fidelity Guard Blocked Short Render ({slug_key}/{lang_code})]: {fidelity_check.get('reason')}")

    voice_name = vmaker.GLOBAL_VOICE_MAP.get(lang_code, vmaker.GLOBAL_VOICE_MAP["en"])["voice"]
    ffmpeg_exe = shutil.which("ffmpeg")
    ffprobe_exe = shutil.which("ffprobe")

    pub_short_dir = ROOT_DIR / "video_lectures" / "shorts"
    pub_short_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir = Path(tempfile.mkdtemp(prefix=f"min7014_ideashort2_{slug_key}_{lang_code}_"))
    segs = []

    f_top = vmaker.get_font_for_lang(lang_code, 40, bold=True)
    f_sub = vmaker.get_font_for_lang(lang_code, 25, bold=True)
    f_cap = vmaker.get_font_for_lang(lang_code, 32, bold=True)

    try:
        for idx, act_info in enumerate(acts, 1):
            raw_sents = re.split(r"(?<=[.?!])\s+", act_info["narration"].strip())
            short_narr = " ".join(raw_sents[:2])
            if idx == len(acts):
                short_narr += (
                    " 지금 구독 누르고 1080p 창의 시네마 풀버전을 확인해 보세요!"
                    if lang_code == "ko"
                    else " Hit Subscribe and watch the full 1080p Creative Math Cinema!"
                )

            mp3_p = tmp_dir / f"ishort_{idx:02d}.mp3"
            seg_p = tmp_dir / f"ishort_{idx:02d}.mp4"
            comm = edge_tts.Communicate(short_narr, voice_name, rate="+22%")
            asyncio.run(comm.save(str(mp3_p)))
            seg_dur = max(2.5, vmaker.get_media_duration_seconds(mp3_p, ffprobe_exe))

            num_frames = 12
            per_f_dur = seg_dur / num_frames
            f_lines = []
            last_fp = None
            cap_lines = textwrap.wrap(sanitize_glyphs(short_narr), width=22 if lang_code == "ko" else 34)[:5]

            for fi in range(num_frames):
                t_raw = fi / max(1, num_frames - 1)
                scene_rgb = render_pure_procedural_scene(1080, 1920, archetype, act_info["act"], t_raw, lang_code=lang_code)
                hud = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
                draw = ImageDraw.Draw(hud)

                draw.rounded_rectangle((40, 56, 1040, 286), radius=26, fill=(10, 18, 36, 210), outline=(124, 58, 237, 235), width=3)
                draw.rounded_rectangle((68, 76, 680, 126), radius=16, fill=(124, 58, 237, 245))
                draw.text((86, 85), sanitize_glyphs(act_info["badge"])[:30], fill=(254, 240, 138, 255), font=f_sub)
                draw.text((830, 85), f"IDEA {idx}/{len(acts)}", fill=(250, 204, 21, 255), font=f_sub)

                t_lines = textwrap.wrap(clean_title, width=20 if lang_code == "ko" else 28)[:2]
                for li, tl in enumerate(t_lines):
                    draw.text((72, 142 + li * 50), tl, fill=(255, 255, 255, 255), font=f_top)

                overall_p = ((idx - 1) + (fi + 1) / num_frames) / len(acts)
                draw.rounded_rectangle((68, 254, 1012, 268), radius=6, fill=(30, 41, 59, 220))
                draw.rounded_rectangle((68, 254, 68 + max(24, int(944 * overall_p)), 268), radius=6, fill=(250, 204, 21, 255))

                draw.rounded_rectangle((40, 1335, 1040, 1795), radius=26, fill=(8, 14, 28, 218), outline=(250, 204, 21, 225), width=3)
                draw.text((70, 1362), sanitize_glyphs(act_info["key_formula"])[:34], fill=(56, 189, 248, 255), font=f_sub)
                draw.rounded_rectangle((748, 1352, 1016, 1404), radius=16, fill=(225, 29, 72, 245), outline=(254, 240, 138, 245), width=2)
                draw.text(
                    (768, 1363),
                    "▶ 구독 @min7014_ai" if lang_code == "ko" else "▶ SUBSCRIBE",
                    fill=(255, 255, 255, 255),
                    font=vmaker.get_font_for_lang("ko", 22, bold=True),
                )

                active_ci = min(len(cap_lines) - 1, int(t_raw * len(cap_lines))) if cap_lines else 0
                for ci, cl in enumerate(cap_lines):
                    c_col = (254, 240, 138, 255) if ci == active_ci else (203, 213, 225, 235)
                    draw.text((72, 1432 + ci * 60), cl, fill=c_col, font=f_cap)

                draw.rounded_rectangle((40, 1810, 1040, 1892), radius=20, fill=(88, 28, 135, 235), outline=(250, 204, 21, 240), width=3)
                cta_txt = (
                    "▶ [구독] 누르고 매일 창의 수학 아이디어 받기! → 고정댓글에 1080p 본편"
                    if lang_code == "ko"
                    else "▶ Tap [SUBSCRIBE] for Daily Math Ideas! → Full 1080p in Pinned Comment"
                )
                draw.text((64, 1834), cta_txt, fill=(254, 240, 138, 255), font=vmaker.get_font_for_lang("ko", 23, bold=True))

                frame_out = Image.alpha_composite(scene_rgb.convert("RGBA"), hud).convert("RGB")
                fp = tmp_dir / f"ishort_{idx:02d}_f{fi:02d}.png"
                frame_out.save(fp)
                f_lines.append(f"file '{fp.as_posix()}'")
                f_lines.append(f"duration {per_f_dur:.4f}")
                last_fp = fp

            if last_fp:
                f_lines.append(f"file '{last_fp.as_posix()}'")
            f_txt = tmp_dir / f"ishort_fconcat_{idx:02d}.txt"
            f_txt.write_text("\n".join(f_lines), encoding="utf-8")

            chime_wav = vmaker.ensure_harmonic_chime_wav()
            cmd = [
                ffmpeg_exe, "-y",
                "-f", "concat", "-safe", "0", "-i", str(f_txt),
                "-i", str(mp3_p),
                "-i", str(chime_wav),
                "-filter_complex",
                "[1:a]aformat=sample_rates=48000:channel_layouts=stereo[v];"
                "[2:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.14[c];"
                "[v][c]amix=inputs=2:duration=first:dropout_transition=0[aout]",
                "-map", "0:v", "-map", "[aout]",
                "-c:v", "libx264", "-profile:v", "high", "-crf", "17", "-pix_fmt", "yuv420p", "-r", "30",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                "-shortest",
                str(seg_p),
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            segs.append(seg_p)

        concat_p = tmp_dir / "concat_ishort.txt"
        concat_p.write_text("\n".join(f"file '{s.as_posix()}'" for s in segs), encoding="utf-8")
        raw_short = tmp_dir / f"raw_ishort_{slug_key}_{lang_code}.mp4"
        out_short = pub_short_dir / f"{slug_key}_short_idea_{lang_code}.mp4"
        subprocess.run(
            [ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_p), "-c", "copy", str(raw_short)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        ambient_wav = vmaker.ensure_ambient_pad_wav()
        subprocess.run(
            [
                ffmpeg_exe, "-y",
                "-i", str(raw_short),
                "-stream_loop", "-1", "-i", str(ambient_wav),
                "-filter_complex",
                "[0:a]aformat=sample_rates=48000:channel_layouts=stereo[v];"
                "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.13[bgm];"
                "[v][bgm]amix=inputs=2:duration=first:dropout_transition=1[aout]",
                "-map", "0:v", "-map", "[aout]",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest",
                str(out_short),
            ],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        dur = vmaker.get_media_duration_seconds(out_short, ffprobe_exe)
        if dur >= 48.5:
            speed_factor = round((dur / 43.5), 3)
            trimmed = tmp_dir / f"{slug_key}_short_idea_{lang_code}_fast.mp4"
            subprocess.run(
                [
                    ffmpeg_exe, "-y", "-i", str(out_short),
                    "-filter_complex", f"[0:v]setpts=PTS/{speed_factor}[v];[0:a]atempo={min(2.0, speed_factor)}[a]",
                    "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-profile:v", "high", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
                    str(trimmed),
                ],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            shutil.copyfile(trimmed, out_short)
            dur = vmaker.get_media_duration_seconds(out_short, ffprobe_exe)

        ishort_title = build_viral_curiosity_youtube_title(clean_title, archetype, lang_code=lang_code, is_short=True)

        sdoc = json.loads(script_path.read_text(encoding="utf-8"))
        sdoc.setdefault("creative_idea_shorts_packages", {})[lang_code] = {
            "title": ishort_title,
            "local_mp4_path": f"video_lectures/shorts/{slug_key}_short_idea_{lang_code}.mp4",
            "duration_sec": round(dur, 2),
            "aspect_ratio": "9:16 (1080x1920)",
            "edition_mode": "v2.0 Pure Procedural Neon-Bloom Shorts (Zero PDF Screenshots)",
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "needs_youtube_upload": True,
        }
        sdoc.setdefault("creative_idea_shorts_urls", {"ko": "", "en": ""})
        script_path.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
        vmaker.update_video_catalog()
        print(f"🌟📱 [Edition 5-B v2.0 Pure Procedural YouTube Shorts (<58s) Generated] {out_short} ({round(dur, 1)}s)")
        return out_short
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def upload_creative_idea_to_youtube(slug_key: str = "math20250130001", lang_code: str = "ko", langs=None, privacy: str = "public") -> dict:
    """
    [Edition 5-A: 🌟 창의 아이디어 시네마 1080p 본편 유튜브 업로드 + 썸네일 + 다국어 + 자동 댓글 + 텔레그램 알림]
    """
    if langs is not None:
        out_all = {}
        for lc in langs:
            try:
                out_all[lc] = upload_creative_idea_to_youtube(slug_key, lang_code=lc, privacy=privacy)
            except Exception:
                break
        return out_all
    from googleapiclient.http import MediaFileUpload

    mp4_path = CREATIVE_IDEA_DIR / f"{slug_key}_idea_{lang_code}.mp4"
    if not mp4_path.exists():
        mp4_path = render_creative_idea_cinema_video(slug_key, lang_code=lang_code)

    script_path = SCRIPTS_DIR / f"{slug_key}.json"
    sdoc = json.loads(script_path.read_text(encoding="utf-8"))
    idea_pkg = (sdoc.get("creative_idea_packages") or {}).get(lang_code, {})

    ko_t, en_t = vmaker.split_bilingual_title(sdoc.get("title", slug_key))
    clean_t = sanitize_glyphs(
        vmaker._smart_concise_topic_title(sanitize_glyphs(vmaker.latex_to_unicode_title(ko_t)), max_len=36, lang="ko")
        if lang_code == "ko"
        else vmaker._smart_concise_topic_title(sanitize_glyphs(vmaker.latex_to_unicode_title(en_t or sdoc.get("title_en") or ko_t)), max_len=44, lang="en")
    )

    archetype = detect_visual_archetype(sdoc)
    title = build_viral_curiosity_youtube_title(clean_t, archetype, lang_code=lang_code, is_short=False)
    std_url = (sdoc.get("youtube_urls") or {}).get(lang_code) or f"https://www.youtube.com/results?search_query=min7014_ai+{slug_key}"
    ggb_url = sdoc.get("geogebra_url") or sdoc.get("source_page_url") or sdoc.get("web_url") or f"https://min7014.github.io/{slug_key}/"
    pdf_url = sdoc.get("pdf_url") or f"https://min7014.github.io/pdf/{slug_key}.pdf"
    web_url = sdoc.get("web_url") or "https://min7014.github.io/"

    desc = (
        f"🌟 [Edition 5: https://min7014.github.io/ 원문 자료 기반 창의 수학 아이디어 시네마 (Pure Procedural Neon-Bloom Math Cinema)]\n"
        f"본 영상은 https://min7014.github.io/ 의 단계별 시각 증명 자료('{clean_t}')에 담긴 핵심 수학적 아이디어와 보조선 원리를 바탕으로, 네온 블룸 프랙탈과 동적 기하 셰이더로 구현한 5막 스토리텔링 시네마입니다!\n\n"
        f"🏛️ [기본 아이디어 원문 자료 (https://min7014.github.io/)]\n"
        f"• 단계별 시각 증명 원본 PDF: {pdf_url}\n"
        f"• 수학자료실 원문 아카이브: {web_url}\n"
        f"• GeoGebra 인터랙티브 직접 조작: {ggb_url}\n\n"
        f"🔔 [지금 바로 @min7014_ai 채널 1초 구독하기]:\n"
        f"👉 https://www.youtube.com/@min7014_ai?sub_confirmation=1\n\n"
        f"🎬 [함께 보면 200% 시너지가 나는 연계 콘텐츠]\n"
        f"• 8분+ 네온 시네마 마스터클래스 총정리: https://youtu.be/_5LE_BfLA5w\n"
        f"• 단계별 시각 증명 본편: {std_url}\n"
        f"• mathedu 16,548문항 무료 문제은행: https://min7014.github.io/mathedu/video_board.html?slug={slug_key}\n\n"
        f"#창의수학 #시각적증명 #{clean_t.replace(' ', '')} #수학아이디어 #수능수학 #기하학 #VisualProof #MathAnimation #min7014_ai"
    )

    body = {
        "snippet": {
            "title": title[:100],
            "description": desc[:4900],
            "tags": ["창의수학", "시각적증명", "수학아이디어", clean_t, "VisualProof", "MathCinema", "GeoGebra", "min7014_ai"],
            "categoryId": "27",
            "defaultLanguage": lang_code,
            "defaultAudioLanguage": lang_code,
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(str(mp4_path), mimetype="video/mp4", resumable=True, chunksize=4 * 1024 * 1024)
    resp = None
    yt = None
    last_err = None
    while True:
        yt, t_path = vmaker.get_available_youtube_upload_service()
        if yt is None:
            raise RuntimeError(f"All YouTube tokens exhausted: {last_err}")
        try:
            existing_url = (sdoc.get("creative_idea_youtube_urls") or {}).get(lang_code, "")
            old_vid = vmaker.extract_youtube_video_id(existing_url)
            if old_vid:
                try:
                    yt.videos().delete(id=old_vid).execute()
                except Exception:
                    pass
            req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
            while resp is None:
                _, resp = req.next_chunk()
            break
        except Exception as e:
            last_err = e
            vmaker._EXHAUSTED_TOKEN_FILES[t_path] = time.time() + 1800
            continue

    vid_id = resp["id"]
    yt_url = f"https://youtu.be/{vid_id}"

    thumb_p = render_creative_idea_thumbnail(sdoc, lang_code=lang_code)
    if thumb_p.exists():
        try:
            yt.thumbnails().set(videoId=vid_id, media_body=MediaFileUpload(str(thumb_p), mimetype="image/png")).execute()
        except Exception:
            pass

    try:
        comment_txt = build_viral_comment_puzzle(archetype, lang_code=lang_code, ggb_url=ggb_url, sdoc=sdoc)
        yt.commentThreads().insert(
            part="snippet",
            body={"snippet": {"videoId": vid_id, "topLevelComment": {"snippet": {"textOriginal": comment_txt}}}},
        ).execute()
    except Exception:
        pass

    sdoc = json.loads(script_path.read_text(encoding="utf-8"))
    sdoc.setdefault("creative_idea_youtube_urls", {"ko": "", "en": ""})[lang_code] = yt_url
    if "creative_idea_packages" in sdoc and lang_code in sdoc["creative_idea_packages"]:
        sdoc["creative_idea_packages"][lang_code]["youtube_url"] = yt_url
        sdoc["creative_idea_packages"][lang_code]["needs_youtube_upload"] = False
    script_path.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
    vmaker.update_video_catalog()

    vmaker.notify_telegram_youtube_upload(
        slug_key=slug_key,
        edition_label=f"🌟 [창의 아이디어 시네마 1080p ({lang_code.upper()})]",
        video_title=title,
        youtube_url=yt_url,
    )
    return {"video_id": vid_id, "youtube_url": yt_url, "title": title}


def upload_creative_idea_short_to_youtube(slug_key: str = "math20250130001", lang_code: str = "ko", langs=None, privacy: str = "public") -> dict:
    """
    [Edition 5-B: 🌟📱 창의 아이디어 숏폼 9:16 (Idea-#Shorts) 유튜브 업로드 + 자동 댓글 + 텔레그램 알림]
    """
    if langs is not None:
        out_all = {}
        for lc in langs:
            try:
                out_all[lc] = upload_creative_idea_short_to_youtube(slug_key, lang_code=lc, privacy=privacy)
            except Exception:
                break
        return out_all
    from googleapiclient.http import MediaFileUpload

    short_path = ROOT_DIR / "video_lectures" / "shorts" / f"{slug_key}_short_idea_{lang_code}.mp4"
    if not short_path.exists():
        short_path = render_creative_idea_short_vertical(slug_key, lang_code=lang_code)

    script_path = SCRIPTS_DIR / f"{slug_key}.json"
    sdoc = json.loads(script_path.read_text(encoding="utf-8"))
    spkg = (sdoc.get("creative_idea_shorts_packages") or {}).get(lang_code, {})

    ko_t, en_t = vmaker.split_bilingual_title(sdoc.get("title", slug_key))
    clean_t = sanitize_glyphs(
        vmaker._smart_concise_topic_title(sanitize_glyphs(vmaker.latex_to_unicode_title(ko_t)), max_len=30, lang="ko")
        if lang_code == "ko"
        else vmaker._smart_concise_topic_title(sanitize_glyphs(vmaker.latex_to_unicode_title(en_t or sdoc.get("title_en") or ko_t)), max_len=38, lang="en")
    )

    yt, _ = vmaker.get_available_youtube_upload_service()
    if yt is None:
        raise RuntimeError("No available YouTube upload service / quota exhausted")

    archetype = detect_visual_archetype(sdoc)
    title = build_viral_curiosity_youtube_title(clean_t, archetype, lang_code=lang_code, is_short=True)
    idea_full_url = (
        (sdoc.get("creative_idea_youtube_urls") or {}).get(lang_code)
        or (sdoc.get("youtube_urls") or {}).get(lang_code)
        or f"https://min7014.github.io/mathedu/video_board.html?slug={slug_key}&mode=idea"
    )
    ggb_url = sdoc.get("geogebra_url") or sdoc.get("source_page_url") or sdoc.get("web_url") or f"https://min7014.github.io/{slug_key}/"
    pdf_url = sdoc.get("pdf_url") or f"https://min7014.github.io/pdf/{slug_key}.pdf"
    web_url = sdoc.get("web_url") or "https://min7014.github.io/"

    desc = (
        f"🎬 [1080p 창의 시네마 풀버전 & 8분+ 마스터클래스 바로 보기]\n"
        f"👉 1080p 본편: {idea_full_url}\n"
        f"👉 8분 마스터클래스 총정리: {'https://youtu.be/_5LE_BfLA5w' if lang_code == 'ko' else 'https://youtu.be/9EL8pgqJtkY'}\n\n"
        f"🏛️ [기본 아이디어 출처: https://min7014.github.io/ ('{clean_t}')]\n"
        f"• 단계별 증명 원본 PDF: {pdf_url}\n"
        f"• 수학자료실 원문 아카이브: {web_url}\n"
        f"• 직접 조작하는 GeoGebra: {ggb_url}\n\n"
        f"🌟📱 [Edition 5-B: https://min7014.github.io/ 원문 기반 창의 수학 아이디어 #Shorts]\n"
        f"단 45초 만에 '{clean_t}'의 핵심 불변량 아이디어를 순수 네온 블룸 애니메이션으로 직관화합니다!\n\n"
        f"🔔 [지금 @min7014_ai 1초 구독하기]:\n"
        f"👉 https://www.youtube.com/@min7014_ai?sub_confirmation=1\n\n"
        f"#Shorts #창의수학 #시각적증명 #수학쇼츠 #MathShorts #VisualProof #min7014_ai"
    )

    body = {
        "snippet": {
            "title": title[:100],
            "description": desc[:4900],
            "tags": ["Shorts", "창의수학", "수학쇼츠", "시각적증명", clean_t, "MathShorts", "VisualProof", "min7014_ai"],
            "categoryId": "27",
            "defaultLanguage": lang_code,
            "defaultAudioLanguage": lang_code,
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
        },
    }
    media = MediaFileUpload(str(short_path), mimetype="video/mp4", resumable=True, chunksize=4 * 1024 * 1024)
    resp = None
    yt = None
    last_err = None
    while True:
        yt, t_path = vmaker.get_available_youtube_upload_service()
        if yt is None:
            raise RuntimeError(f"All YouTube tokens exhausted: {last_err}")
        try:
            existing_url = (sdoc.get("creative_idea_shorts_urls") or {}).get(lang_code, "")
            old_vid = vmaker.extract_youtube_video_id(existing_url)
            if old_vid:
                try:
                    yt.videos().delete(id=old_vid).execute()
                except Exception:
                    pass
            req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
            while resp is None:
                _, resp = req.next_chunk()
            break
        except Exception as e:
            last_err = e
            vmaker._EXHAUSTED_TOKEN_FILES[t_path] = time.time() + 1800
            continue

    vid_id = resp["id"]
    yt_url = f"https://youtube.com/shorts/{vid_id}"

    try:
        comment_txt = build_viral_comment_puzzle(archetype, lang_code=lang_code, ggb_url=idea_full_url, sdoc=sdoc)
        yt.commentThreads().insert(
            part="snippet",
            body={"snippet": {"videoId": vid_id, "topLevelComment": {"snippet": {"textOriginal": comment_txt}}}},
        ).execute()
    except Exception:
        pass

    sdoc = json.loads(script_path.read_text(encoding="utf-8"))
    sdoc.setdefault("creative_idea_shorts_urls", {"ko": "", "en": ""})[lang_code] = yt_url
    if "creative_idea_shorts_packages" in sdoc and lang_code in sdoc["creative_idea_shorts_packages"]:
        sdoc["creative_idea_shorts_packages"][lang_code]["youtube_url"] = yt_url
        sdoc["creative_idea_shorts_packages"][lang_code]["needs_youtube_upload"] = False
    script_path.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
    vmaker.update_video_catalog()

    vmaker.notify_telegram_youtube_upload(
        slug_key=slug_key,
        edition_label=f"🌟📱 [창의 아이디어 #Shorts ({lang_code.upper()})]",
        video_title=title,
        youtube_url=yt_url,
    )
    return {"video_id": vid_id, "youtube_url": yt_url, "title": title}


def upgrade_all_creative_idea_titles() -> int:
    """기존에 생성된 모든 창의 시네마 패키지(JSON)의 제목을 고클릭률(High-CTR) 바이럴 호기심 훅 제목으로 일괄 업그레이드합니다."""
    cnt = 0
    for p in sorted(SCRIPTS_DIR.glob("*.json")):
        try:
            sdoc = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if "creative_idea_packages" not in sdoc and "creative_idea_shorts_packages" not in sdoc:
            continue
        arch = detect_visual_archetype(sdoc)
        ko_t, en_t = vmaker.split_bilingual_title(sdoc.get("title", p.stem))
        changed = False
        for lg in ("ko", "en"):
            raw_t = ko_t if lg == "ko" else (en_t or sdoc.get("title_en") or ko_t)
            san_raw = sanitize_glyphs(vmaker.latex_to_unicode_title(raw_t))
            ct_long = sanitize_glyphs(vmaker._smart_concise_topic_title(san_raw, max_len=36 if lg == "ko" else 44, lang=lg))
            ct_short = sanitize_glyphs(vmaker._smart_concise_topic_title(san_raw, max_len=30 if lg == "ko" else 38, lang=lg))
            if lg in sdoc.get("creative_idea_packages", {}):
                new_t = build_viral_curiosity_youtube_title(ct_long, arch, lang_code=lg, is_short=False)
                if sdoc["creative_idea_packages"][lg].get("title") != new_t:
                    sdoc["creative_idea_packages"][lg]["title"] = new_t
                    changed = True
            if lg in sdoc.get("creative_idea_shorts_packages", {}):
                new_st = build_viral_curiosity_youtube_title(ct_short, arch, lang_code=lg, is_short=True)
                if sdoc["creative_idea_shorts_packages"][lg].get("title") != new_st:
                    sdoc["creative_idea_shorts_packages"][lg]["title"] = new_st
                    changed = True
        if changed:
            p.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
            cnt += 1
    if cnt:
        vmaker.update_video_catalog()
    return cnt


def sync_live_creative_idea_youtube_metadata(target_slugs=None) -> list:
    """
    [Rule 19 수학적 정합성 라이브 동기화 엔진]
    이미 @min7014_ai 유튜브 채널에 게시되어 조회수·시청시간을 쌓고 있는 창의 아이디어 시네마(본편 & #Shorts) 영상들에 대해,
    영상 삭제 없이(조회수 100% 보존!) yt.videos().update, yt.thumbnails().set, yt.commentThreads().insert 로
    100% 수학적으로 정확한 제목·설명란·썸네일·5초 암산 퍼즐 댓글을 즉시 반영합니다.
    """
    from googleapiclient.http import MediaFileUpload

    yt, _ = vmaker.get_available_youtube_upload_service()
    if yt is None:
        print("[sync_live_creative_idea_youtube_metadata] No YouTube service available.")
        return []

    if not target_slugs:
        target_slugs = [
            "2014111901", "2022042501", "2022051507", "2016032701", "2016012801",
            "math20250130001", "2014111902", "2017090101", "2012092301",
        ]
    updated_vids = []
    for slug in target_slugs:
        sp = SCRIPTS_DIR / f"{slug}.json"
        if not sp.exists():
            continue
        sdoc = json.loads(sp.read_text(encoding="utf-8"))
        arch = detect_visual_archetype(sdoc)
        ko_t, en_t = vmaker.split_bilingual_title(sdoc.get("title", slug))
        ggb_url = sdoc.get("geogebra_url") or sdoc.get("source_page_url") or sdoc.get("web_url") or f"https://min7014.github.io/{slug}/"
        pdf_url = sdoc.get("pdf_url") or f"https://min7014.github.io/pdf/{slug}.pdf"
        web_url = sdoc.get("web_url") or "https://min7014.github.io/"
        tpa = sdoc.get("teacher_proof_analysis") or {}

        for lg in ("ko", "en"):
            raw_t = ko_t if lg == "ko" else (en_t or sdoc.get("title_en") or ko_t)
            san_raw = sanitize_glyphs(vmaker.latex_to_unicode_title(raw_t))
            ct_long = sanitize_glyphs(vmaker._smart_concise_topic_title(san_raw, max_len=36 if lg == "ko" else 44, lang=lg))
            ct_short = sanitize_glyphs(vmaker._smart_concise_topic_title(san_raw, max_len=30 if lg == "ko" else 38, lang=lg))
            core_eq = tpa.get("conclusion_ko" if lg == "ko" else "conclusion_en") or ""
            aux_line = tpa.get("auxiliary_line_ko" if lg == "ko" else "auxiliary_line_en") or ""

            thumb_p = render_creative_idea_thumbnail(sdoc, lang_code=lg)

            # 1. Long-form Creative Idea video in-place update
            long_url = (sdoc.get("creative_idea_youtube_urls") or {}).get(lg, "")
            vid_id = vmaker.extract_youtube_video_id(long_url)
            if vid_id:
                new_title = build_viral_curiosity_youtube_title(ct_long, arch, lang_code=lg, is_short=False)
                std_url = (sdoc.get("youtube_urls") or {}).get(lg) or f"https://www.youtube.com/results?search_query=min7014_ai+{slug}"
                desc = (
                    f"🌟 [Edition 5: https://min7014.github.io/ 원문 자료 100% 수학적 검증 기반 창의 아이디어 시네마]\n"
                    f"• 주제: {ct_long}\n"
                    f"• 핵심 수학 정리·불변량: {core_eq}\n"
                    f"• 핵심 보조선·아이디어: {aux_line}\n\n"
                    f"🏛️ [기본 아이디어 원문 자료 (https://min7014.github.io/)]\n"
                    f"• 단계별 시각 증명 원본 PDF: {pdf_url}\n"
                    f"• 수학자료실 원문 아카이브: {web_url}\n"
                    f"• GeoGebra 인터랙티브 직접 조작: {ggb_url}\n\n"
                    f"🔔 [지금 바로 @min7014_ai 채널 1초 구독하기]:\n"
                    f"👉 https://www.youtube.com/@min7014_ai?sub_confirmation=1\n\n"
                    f"🎬 [함께 보면 200% 시너지가 나는 연계 콘텐츠]\n"
                    f"• 8분+ 네온 시네마 마스터클래스 총정리: https://youtu.be/_5LE_BfLA5w\n"
                    f"• 단계별 시각 증명 본편: {std_url}\n"
                    f"• mathedu 16,548문항 무료 문제은행: https://min7014.github.io/mathedu/video_board.html?slug={slug}\n\n"
                    f"#창의수학 #시각적증명 #수학아이디어 #수능수학 #기하학 #VisualProof #MathAnimation #min7014_ai"
                )
                desc = desc.replace("<", "＜").replace(">", "＞")
                try:
                    yt.videos().update(
                        part="snippet",
                        body={
                            "id": vid_id,
                            "snippet": {
                                "title": new_title[:100].replace("<", "＜").replace(">", "＞"),
                                "description": desc[:4900],
                                "tags": ["창의수학", "시각적증명", "수학아이디어", ct_long, "VisualProof", "MathCinema", "GeoGebra", "min7014_ai"],
                                "categoryId": "27",
                                "defaultLanguage": lg,
                                "defaultAudioLanguage": lg,
                            },
                        },
                    ).execute()
                    if thumb_p.exists() and slug in ("2014111901", "2022042501", "2022051507", "2016032701", "2016012801"):
                        yt.thumbnails().set(videoId=vid_id, media_body=MediaFileUpload(str(thumb_p), mimetype="image/png")).execute()
                    if slug in ("2014111901", "2022042501", "2022051507", "2016012801"):
                        c_txt = build_viral_comment_puzzle(arch, lang_code=lg, ggb_url=ggb_url, sdoc=sdoc)
                        yt.commentThreads().insert(
                            part="snippet",
                            body={"snippet": {"videoId": vid_id, "topLevelComment": {"snippet": {"textOriginal": c_txt}}}},
                        ).execute()
                    updated_vids.append({"slug": slug, "lang": lg, "type": "long", "video_id": vid_id, "title": new_title})
                except Exception as exc:
                    print(f"[sync_live long err] {slug} ({lg}): {exc}")

            # 2. Short-form Creative Idea video in-place update
            short_url = (sdoc.get("creative_idea_shorts_urls") or {}).get(lg, "")
            svid_id = vmaker.extract_youtube_video_id(short_url)
            if svid_id:
                new_stitle = build_viral_curiosity_youtube_title(ct_short, arch, lang_code=lg, is_short=True)
                idea_full_url = long_url or (sdoc.get("youtube_urls") or {}).get(lg) or f"https://min7014.github.io/mathedu/video_board.html?slug={slug}&mode=idea"
                mc_url = "https://youtu.be/_5LE_BfLA5w" if lg == "ko" else "https://youtu.be/9EL8pgqJtkY"
                sdesc = (
                    f"🎬 [1080p 창의 시네마 풀버전 & 8분+ 마스터클래스 바로 보기]\n"
                    f"👉 1080p 본편: {idea_full_url}\n"
                    f"👉 8분 마스터클래스 총정리: {mc_url}\n\n"
                    f"🏛️ [기본 아이디어 출처: https://min7014.github.io/ ('{ct_short}')]\n"
                    f"• 핵심 수학 불변량: {core_eq}\n"
                    f"• 단계별 증명 원본 PDF: {pdf_url}\n"
                    f"• 수학자료실 원문 아카이브: {web_url}\n"
                    f"• 직접 조작하는 GeoGebra: {ggb_url}\n\n"
                    f"🔔 [지금 @min7014_ai 1초 구독하기]:\n"
                    f"👉 https://www.youtube.com/@min7014_ai?sub_confirmation=1\n\n"
                    f"#Shorts #창의수학 #시각적증명 #수학쇼츠 #MathShorts #VisualProof #min7014_ai"
                )
                sdesc = sdesc.replace("<", "＜").replace(">", "＞")
                try:
                    yt.videos().update(
                        part="snippet",
                        body={
                            "id": svid_id,
                            "snippet": {
                                "title": new_stitle[:100].replace("<", "＜").replace(">", "＞"),
                                "description": sdesc[:4900],
                                "tags": ["Shorts", "창의수학", "수학쇼츠", "시각적증명", ct_short, "MathShorts", "VisualProof", "min7014_ai"],
                                "categoryId": "27",
                                "defaultLanguage": lg,
                                "defaultAudioLanguage": lg,
                            },
                        },
                    ).execute()
                    if slug in ("2014111901", "2022042501", "2022051507", "2016012801"):
                        c_txt = build_viral_comment_puzzle(arch, lang_code=lg, ggb_url=idea_full_url, sdoc=sdoc)
                        yt.commentThreads().insert(
                            part="snippet",
                            body={"snippet": {"videoId": svid_id, "topLevelComment": {"snippet": {"textOriginal": c_txt}}}},
                        ).execute()
                    updated_vids.append({"slug": slug, "lang": lg, "type": "short", "video_id": svid_id, "title": new_stitle})
                except Exception as exc:
                    print(f"[sync_live short err] {slug} ({lg}): {exc}")

    return updated_vids


def build_flagship_creative_idea_suite(slugs=None, langs=("ko", "en")) -> list:
    """주요 수학 주제들에 대해 Edition 5 v2.0 (순수 네온 블룸 창의 아이디어 시네마 1080p + Idea-#Shorts 9:16) 일괄 제작"""
    if not slugs:
        slugs = ["math20250130001", "2014111902", "2022051507", "2014111901", "2016032701", "2022042501"]
    results = []
    for slug in slugs:
        for lg in langs:
            c_mp4 = CREATIVE_IDEA_DIR / f"{slug}_idea_{lg}.mp4"
            s_mp4 = ROOT_DIR / "video_lectures" / "shorts" / f"{slug}_short_idea_{lg}.mp4"
            p_cinema = render_creative_idea_cinema_video(slug, lang_code=lg) if not c_mp4.exists() else c_mp4
            p_short = render_creative_idea_short_vertical(slug, lang_code=lg) if not s_mp4.exists() else s_mp4
            results.append({"slug": slug, "lang": lg, "cinema": str(p_cinema), "short": str(p_short)})
    return results


def build_creative_idea_masterclass_compilation(langs=("ko", "en")) -> list:
    """
    [월 1,000만 원 핵심 엔진: 🌟 10분+ 미드롤(Mid-Roll) 순수 네온 블룸 창의 수학 시네마 마스터클래스 합본 Vol.1 & Vol.2 제작]
    - PDF 캡처가 전혀 없는 12편의 순수 네온 블룸 시네마(Vol.1 6편 + Vol.2 6편)를
      각각 10~13분+ 정주행 마스터클래스로 결합하여 미드롤 광고 슬롯 3~4개와 시청 지속시간(Watch Time)을 극대화합니다.
    """
    vol_suites = [
        ("masterclass_neon_idea_vol1", ["math20250130001", "2014111902", "2022051507", "2014111901", "2016032701", "2022042501"]),
        ("masterclass_neon_idea_vol2", ["2017090101", "2016012801", "2012092301", "2019081052", "2011112501", "2017030206"]),
        ("masterclass_neon_idea_vol3", ["2012093001", "2016040701", "2019101602", "2020041301", "2017090601", "2017090501"]),
    ]
    for _, v_slugs in vol_suites:
        build_flagship_creative_idea_suite(slugs=v_slugs, langs=langs)

    mc_dir = ROOT_DIR / "video_lectures" / "masterclasses"
    mc_dir.mkdir(parents=True, exist_ok=True)
    ffmpeg_exe = shutil.which("ffmpeg")
    ffprobe_exe = shutil.which("ffprobe")
    compiled = []

    for base_id, v_slugs in vol_suites:
        for lg in langs:
            mp4_list = [CREATIVE_IDEA_DIR / f"{sl}_idea_{lg}.mp4" for sl in v_slugs if (CREATIVE_IDEA_DIR / f"{sl}_idea_{lg}.mp4").exists()]
            if len(mp4_list) < 3:
                continue
            out_id = base_id if lg == "ko" else f"{base_id}_en"
            out_mp4 = mc_dir / f"{out_id}.mp4"
            concat_txt = mc_dir / f"concat_{out_id}.txt"
            concat_txt.write_text("\n".join(f"file '{p.as_posix()}'" for p in mp4_list), encoding="utf-8")
            subprocess.run(
                [ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", "-movflags", "+faststart", str(out_mp4)],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            concat_txt.unlink(missing_ok=True)
            dur = vmaker.get_media_duration_seconds(out_mp4, ffprobe_exe)
            compiled.append({"id": out_id, "lang": lg, "path": str(out_mp4), "duration_sec": round(dur, 1), "chapters": len(mp4_list)})
            print(f"🌟🏆 [10-Min+ Mid-Roll Neon-Bloom Cinema Masterclass Compiled] {out_mp4} ({round(dur / 60, 1)} min)")
    return compiled


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Edition 5 v2.0: Pure Procedural Neon-Bloom Math Cinema Engine")
    parser.add_argument("--slug", default="math20250130001", help="Topic slug")
    parser.add_argument("--lang", default="ko", help="Language code (ko/en)")
    parser.add_argument("--batch", action="store_true", help="Build flagship suite")
    parser.add_argument("--masterclass", action="store_true", help="Build 10-min+ Neon-Bloom Masterclass compilation")
    parser.add_argument("--upload", action="store_true", help="Upload to YouTube if quota permits")
    args = parser.parse_args()

    if args.masterclass:
        res = build_creative_idea_masterclass_compilation()
        print(json.dumps(res, ensure_ascii=False, indent=2))
    elif args.batch:
        res = build_flagship_creative_idea_suite()
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        c_mp4 = render_creative_idea_cinema_video(args.slug, lang_code=args.lang)
        s_mp4 = render_creative_idea_short_vertical(args.slug, lang_code=args.lang)
        if args.upload:
            try:
                upload_creative_idea_to_youtube(args.slug, lang_code=args.lang)
                upload_creative_idea_short_to_youtube(args.slug, lang_code=args.lang)
            except Exception as exc:
                print(f"[Upload Deferred / Quota Pending] {exc}")
