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
        "lim( theta arrow 0) ( sin theta/": "lim(θ→0) (sinθ/θ) = 1",
        "theta arrow 0": "θ→0",
        "sin theta": "sinθ",
        "cos theta": "cosθ",
        "tan theta": "tanθ",
    }
    out = str(text)
    for k, v in repl.items():
        out = out.replace(k, v)
    return out


def detect_visual_archetype(sdoc: dict) -> str:
    blob = " ".join([
        str(sdoc.get("title", "")),
        str(sdoc.get("title_en", "")),
        str(sdoc.get("concept_badge", "")),
        str((sdoc.get("teacher_proof_analysis") or {}).get("category_type", "")),
    ]).lower()

    if any(k in blob for k in ["피타고라스", "pythagor", "직각삼각형", "right triangle", "넓이 보존", "정사각형의 한 변"]):
        return "pythagoras_fractal"
    if any(k in blob for k in ["타원", "포물선", "쌍곡선", "단델린", "초점", "준선", "이차곡선", "ellipse", "parabola", "hyperbola", "dandelin", "conic", "사이클로이드", "cycloid"]):
        return "conic_reflection"
    if any(k in blob for k in ["황금비", "피보나치", "golden", "fibonacci", "나선", "정오각형", "pentagon", "연분수", "등비", "수열", "제곱근", "무리수"]):
        return "fibonacci_golden"
    if any(k in blob for k in ["확률", "정규분포", "이항", "통계", "주사위", "독립시행", "binomial", "probability", "조합", "순열", "파스칼", "경우의 수", "표준편차", "분산"]):
        return "prob_galton"
    if any(k in blob for k in ["삼각함수", "삼각비", "사인", "코사인", "탄젠트", "호도법", "단위원", "trigon", "sin(", "cos(", "tan(", "sin ", "cos ", "tan ", "\\sin", "\\cos", "\\tan"]):
        return "trig_harmonic"
    if any(k in blob for k in ["미분", "적분", "극한", "도함수", "평균값", "롤의", "구분구적", "급수", "derivative", "integral", "limit", "mean value", "rolle"]):
        return "calculus_motion"
    if any(k in blob for k in ["체바", "메넬라우스", "ceva", "menelaus", "무게중심", "내분", "외분", "선분의 길이의 비", "평행선", "비비아니", "viviani", "나폴레옹", "몰리", "삼각형", "triangle"]):
        return "ceva_menelaus"
    return "circle_invariants"


def build_creative_idea_acts(sdoc: dict, lang_code: str = "ko") -> list[dict]:
    ko_t, en_t = vmaker.split_bilingual_title(sdoc.get("title", sdoc.get("slug", "")))
    clean_ko = sanitize_glyphs(vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(ko_t), max_len=38, lang="ko"))
    clean_en = sanitize_glyphs(vmaker._smart_concise_topic_title(
        vmaker.latex_to_unicode_title(en_t or sdoc.get("title_en") or ko_t), max_len=46, lang="en"
    ))
    t_title = clean_ko if lang_code == "ko" else clean_en
    tpa = sdoc.get("teacher_proof_analysis") or {}
    archetype = detect_visual_archetype(sdoc)

    inv_ko = sanitize_glyphs(vmaker.latex_to_unicode_title(tpa.get("core_invariant") or "도형이 변해도 흔들리지 않는 넓이와 비율의 등식 관계"))
    polya_ko = sanitize_glyphs(vmaker.latex_to_unicode_title(tpa.get("polya_bridge") or "숨겨진 대칭성과 보조선을 연결해 복잡한 식을 단번에 단순화하는 발상"))
    whatif_ko = sanitize_glyphs(vmaker.latex_to_unicode_title(tpa.get("what_if_extension") or "특수한 각도와 평면 도형의 성질을 일반 삼각형과 3차원 공간으로 넓히는 확장"))

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

    # 원주각 / 원의 방멱 / 기하 불변량 5막 시네마 대본
    if lang_code == "ko":
        return [
            {
                "act": 1,
                "badge": "ACT 1 · 직관을 깨는 기하학 미스터리",
                "headline": f"모든 선과 각도가 요동치는데 왜 이 값만은 절대 변하지 않을까? ({t_title})",
                "key_formula": f"Core Invariant · {t_title}",
                "narration": (
                    f"밤하늘의 좌표 공간 위에서 점과 선분이 쉼 없이 움직이며 도형의 모양을 바꿉니다. "
                    f"그런데 놀랍게도 [{t_title}]에서는 점을 어느 위치로 옮겨 놓아도 핵심 비율과 관계식이 마치 중력 법칙처럼 단 0.001의 오차도 없이 일정하게 유지됩니다! "
                    f"정지된 종이 교재를 넘어, 살아 움직이는 시뮬레이션으로 이 불변량의 비밀을 밝혀내 봅시다."
                ),
                "hud_notes": [
                    f"역동적 관찰: 점이 궤적을 따라 움직여도 [{t_title}] 등식은 불변!",
                    f"핵심 불변량: {inv_ko[:46]}",
                    "목표: 공식 암기가 아닌 '살아 움직이는 단 하나의 원리' 완전 체득!",
                ],
            },
            {
                "act": 2,
                "badge": "ACT 2 · 공식 없이 눈으로 보는 대칭·수치 실험",
                "headline": "가장 대칭적인 순간과 실시간 수치 계기판으로 규칙 포착하기",
                "key_formula": "Live Invariant Ratio = 1.000 (100% Constant)",
                "narration": (
                    f"복잡한 기호로 식을 세우기 전에, 가장 완벽한 대칭 위치에서 도형의 균형을 먼저 관찰해 보세요. "
                    f"화면 우측의 실시간 계기판에서 볼 수 있듯, 한쪽 길이가 길어지면 반대쪽 비율이 정확히 반비례하여 상쇄되기 때문에 전체 곱과 합의 균형은 언제나 일정하게 유지됩니다."
                ),
                "hud_notes": [
                    "1단계 실험: 정중앙 대칭 상태에서 비율과 넓이의 완벽한 평형 확인",
                    "2단계 실험: 비대칭으로 이동해도 상호 역수 구조로 완벽히 상쇄!",
                    "직관적 결론: 수식은 눈으로 본 대칭 균형을 짧게 기록한 약속일 뿐이다!",
                ],
            },
            {
                "act": 3,
                "badge": "ACT 3 · 천재들의 단 한 줄 보조선 아이디어",
                "headline": "황금빛 보조선 한 줄이 그어지는 순간 모든 조각이 도미노처럼 맞물린다!",
                "key_formula": "1 Golden Auxiliary Line → Domino Cancellation!",
                "narration": (
                    f"그렇다면 왜 어떤 비대칭 위치에서도 이 상쇄 법칙이 깨지지 않을까요? "
                    f"비밀은 지금 화면 한가운데에 빛나며 그어지는 단 한 줄의 황금 보조선에 있습니다! "
                    f"{polya_ko} "
                    f"이 보조선 하나가 흩어져 있던 선분들을 높이가 같은 삼각형의 넓이 비와 닮음비로 묶어주어, 복잡한 분수들이 도미노처럼 연쇄 약분됩니다."
                ),
                "hud_notes": [
                    f"결정적 보조선: {polya_ko[:46]}",
                    f"연쇄 상쇄 원리: {inv_ko[:46]}",
                    "단 한 줄의 시각적 보조선이 10줄의 대수 계산을 단숨에 끝냅니다!",
                ],
            },
            {
                "act": 4,
                "badge": "ACT 4 · 한계를 넘는 상상 (What-If-Not 일반화)",
                "headline": "점이 도형 밖으로 나가거나 할선이 접선으로 수렴하는 극한의 순간!",
                "key_formula": "Interior → Exterior → Tangent Limit → 3D Space!",
                "narration": (
                    f"여기서 멈추지 않고 조건을 과감하게 확장해 봅시다! "
                    f"만약 내부에 있던 점이 도형 바깥의 연장선 위로 나가거나, 두 점이 한없이 가까워져 할선이 접선이 되는 극한의 순간에 도달하면 어떻게 될까요? "
                    f"{whatif_ko} "
                    f"놀랍게도 우리가 발견한 핵심 아이디어는 외분점과 미분 접선, 나아가 3차원 공간 기하에서도 똑같이 작동합니다."
                ),
                "hud_notes": [
                    "확장 1: 점이 외부(연장선)로 이동해도 외분비 대칭으로 동일하게 성립!",
                    "확장 2: 두 점이 합쳐지는 극한(Δx→0)에서 미분 접선 정리로 진화!",
                    f"심화 계통성: {whatif_ko[:44]}",
                ],
            },
            {
                "act": 5,
                "badge": "ACT 5 · 수능·경시 킬러 10초 통찰 & 유레카",
                "headline": "실전 킬러 문항에서 이 시각적 아이디어를 1초 만에 꺼내 쓰는 법!",
                "key_formula": "Spot the Invariant → Draw 1 Line → 10-Sec Solution!",
                "narration": (
                    f"오늘 경험한 [{t_title}] 시네마의 핵심은 결과 공식이 아니라, 문제를 보자마자 어느 꼭짓점에서 어떤 보조선을 그어야 하는지 눈으로 떠올리는 힘입니다. "
                    f"설명란과 고정댓글의 링크에서 지오지브라 도형을 직접 움직여 보고, 5지선다 보기 없이 스스로 식을 조립하는 실전 문제에 도전해 보세요. "
                    f"지금 바로 구독과 좋아요를 누르고 매일 새로운 수학적 유레카를 만나보세요!"
                ),
                "hud_notes": [
                    f"실전 제1발상: [{t_title}] 구조 포착 즉시 핵심 보조선 1줄 작동!",
                    "설명란·고정댓글에서 무료 GeoGebra & 탈-5지선다 기출 즉시 체험",
                    "지금 [@min7014_ai 구독] 누르고 최고 화질 창의 수학 시네마를 정주행하세요!",
                ],
            },
        ]
    else:
        return [
            {
                "act": 1,
                "badge": "ACT 1 · THE GEOMETRIC MYSTERY",
                "headline": f"Everything Moves, Yet This Stays Strictly Invariant! ({t_title})",
                "key_formula": f"Core Invariant · {t_title}",
                "narration": (
                    f"Across this dark coordinate cosmos, points and lines glide continuously, deforming every angle and length. "
                    f"Yet inside [{t_title}], a profound mathematical invariant remains locked with zero error! "
                    f"Forget static textbook pages—let's witness the living geometry that makes this theorem inevitable."
                ),
                "hud_notes": [
                    f"Dynamic Observation: As points move, [{t_title}] remains locked!",
                    "Hidden Invariant: Structural balance of ratios, angles, and areas",
                    "Goal: See the living visual mechanism instead of memorizing formulas!",
                ],
            },
            {
                "act": 2,
                "badge": "ACT 2 · SYMMETRY & LIVE NUMERICAL LAB",
                "headline": "Capturing the Law Through Symmetry & Real-Time Meters",
                "key_formula": "Live Invariant Ratio = 1.000 (100% Constant)",
                "narration": (
                    f"Before writing a single algebraic symbol, observe the figure in its most symmetric state. "
                    f"As shown on the live telemetry meter, whenever one segment stretches, its partner compresses in exact inverse proportion, keeping the overall product and sum invariant."
                ),
                "hud_notes": [
                    "Step 1: Observe the exact equilibrium in the symmetric center state",
                    "Step 2: Perturb the point and watch inverse ratios cancel out live!",
                    "Visual Rule: Algebra is simply the language of geometric balance.",
                ],
            },
            {
                "act": 3,
                "badge": "ACT 3 · THE GOLDEN AUXILIARY LINE",
                "headline": "One Glowing Auxiliary Line Triggers a Domino Cancellation!",
                "key_formula": "1 Golden Auxiliary Line → Domino Cancellation!",
                "narration": (
                    f"Why does this balance survive even in asymmetric positions? "
                    f"Watch the golden auxiliary line illuminate across the canvas! "
                    f"By introducing a shared altitude, parallel line, or common radius, disconnected ratios lock together and cancel out like dominoes."
                ),
                "hud_notes": [
                    "Strategic Auxiliary Line: Connects isolated lengths and angles",
                    "Domino Cancellation: Shared heights and similar triangles do the work",
                    "One visual line replaces ten lines of algebraic manipulation!",
                ],
            },
            {
                "act": 4,
                "badge": "ACT 4 · WHAT-IF-NOT GENERALIZATION",
                "headline": "Moving to the Exterior, Tangent Limits & Higher Dimensions",
                "key_formula": "Interior → Exterior → Tangent Limit → 3D Space!",
                "narration": (
                    f"Now let's push beyond all boundaries! What if the point moves outside the figure, or two points merge until a secant line becomes a tangent? "
                    f"The exact same visual idea extends seamlessly to external divisions, calculus derivatives, and 3D space!"
                ),
                "hud_notes": [
                    "Extension 1: Exterior points preserve the invariant via signed ratios!",
                    "Extension 2: Merging points (Δx→0) transforms secants into tangents!",
                    "One core idea unifies Euclidean geometry and modern calculus!",
                ],
            },
            {
                "act": 5,
                "badge": "ACT 5 · 10-SECOND OLYMPIAD INSIGHT",
                "headline": "Solving Hard Problems Instantly With Visual Intuition",
                "key_formula": "Spot the Invariant → Draw 1 Line → 10-Sec Solution!",
                "narration": (
                    f"Mastering [{t_title}] means knowing which auxiliary line to draw the instant you see a hard problem. "
                    f"Use the links in the description to explore the interactive GeoGebra lab and constructive challenges. "
                    f"Subscribe to @min7014_ai right now for daily visual math cinema!"
                ),
                "hud_notes": [
                    f"Instant Trigger: Spot [{t_title}] and draw the golden auxiliary line!",
                    "Try the free GeoGebra & constructive problem lab in the description",
                    "Subscribe to @min7014_ai for daily high-definition math cinema!",
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

    elif archetype == "calculus_motion":
        span_w = int(scale_ref * 0.68)
        span_h = int(scale_ref * 0.44)
        ax0 = cx - span_w // 2
        ay0 = cy + span_h // 2
        c_draw.line([(ax0, ay0), (ax0 + span_w, ay0)], fill=(148, 163, 184, 220), width=3)
        c_draw.line([(ax0, ay0), (ax0, ay0 - span_h)], fill=(148, 163, 184, 220), width=3)

        def f_val(u):
            return 0.15 + 0.65 * (u ** 1.8) - 0.12 * math.sin(u * math.pi * 2)

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

    elif archetype == "trig_harmonic":
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

        # 우측 사인파 진행 궤적
        wx0 = ucx + R + 40
        wave_w = int(scale_ref * 0.28)
        w_pts = []
        for k in range(60):
            u_k = k / 59.0
            ang_k = theta + u_k * math.pi * 2.0
            w_pts.append((wx0 + u_k * wave_w, ucy - R * math.sin(ang_k) * 0.85))
        g_draw.line(w_pts, fill=(52, 211, 153, 235), width=6)
        c_draw.line(w_pts, fill=(255, 255, 255, 240), width=2)
        g_draw.line([(px, py), w_pts[0]], fill=(250, 204, 21, 180), width=3)
        c_draw.text((int(cx - 210), int(ucy + R + 32)), f"sin θ ({math.sin(theta):.3f}) < θ ({theta:.3f}) < tan θ ({math.tan(theta):.3f})", fill=(254, 240, 138, 255), font=f_big)

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
    [월 1,000만 원 CTR 극대화 엔진]
    첫 25글자(모바일 화면 노출 구간)에 브래킷 라벨 대신 강렬한 호기심 공백(Curiosity Gap) 훅과
    핵심 수학 키워드를 직결하여 클릭률(CTR)을 극대화합니다.
    """
    hooks_ko = {
        "pythagoras_fractal": f"🔥 공식 암기는 그만! {clean_title}, 넓이가 영원히 보존되는 단 1가지 이유",
        "conic_reflection": f"🔥 왜 모든 빛은 반드시 한 점(초점)에 모일까? | {clean_title}",
        "trig_harmonic": f"🔥 왜 둥근 원이 회전하면 완벽한 물결 파동이 될까? | {clean_title}",
        "fibonacci_golden": f"🔥 해바라기와 은하 나선에 숨겨진 137.5° 황금비의 비밀! | {clean_title}",
        "prob_galton": f"🔥 무작위 우연이 수천 번 쌓이면 왜 완벽한 종 모양이 될까? | {clean_title}",
        "calculus_motion": f"🔥 멈춰 있는 그래프가 살아 움직이는 순간! | {clean_title}",
        "ceva_menelaus": f"🔥 복잡한 보조선 없이 넓이 비 하나로 단번에 증명되는 이유! | {clean_title}",
        "circle_invariants": f"🔥 점이 원 위를 아무리 움직여도 각도가 절대 안 변하는 이유! | {clean_title}",
    }
    hooks_en = {
        "pythagoras_fractal": f"🔥 Stop Memorizing! Why {clean_title} Preserves Area Forever",
        "conic_reflection": f"🔥 Why Every Light Ray Bounces to One Exact Focus! | {clean_title}",
        "trig_harmonic": f"🔥 How a Rotating Circle Creates Every Wave in the Universe! | {clean_title}",
        "fibonacci_golden": f"🔥 Why Nature Chose the Golden Angle (137.5°)! | {clean_title}",
        "prob_galton": f"🔥 How Pure Randomness Always Forms a Perfect Bell Curve! | {clean_title}",
        "calculus_motion": f"🔥 The Exact Moment Secant Becomes Tangent! | {clean_title}",
        "ceva_menelaus": f"🔥 How 1 Area Ratio Trick Proves {clean_title} Instantly!",
        "circle_invariants": f"🔥 Why Moving the Vertex Never Changes the Angle! | {clean_title}",
    }
    if lang_code == "ko":
        base = hooks_ko.get(archetype, f"🔥 공식 암기 없이 단 1개의 아이디어로 깨치는 {clean_title}!")
        suffix = " #Shorts #창의수학 | @min7014_ai" if is_short else " | 창의 수학 시네마 @min7014_ai"
    else:
        base = hooks_en.get(archetype, f"🔥 The 1 Visual Idea That Explains {clean_title}!")
        suffix = " #Shorts #Math | @min7014_ai" if is_short else " | Visual Math Cinema @min7014_ai"

    if len(base) + len(suffix) <= 98:
        return base + suffix
    short_suffix = " #Shorts #Math" if is_short else " | @min7014_ai"
    return (base[: 98 - len(short_suffix)].rstrip(" —|-:") + short_suffix)[:98]


def build_viral_comment_puzzle(archetype: str, lang_code: str = "ko", ggb_url: str = "") -> str:
    """
    [유튜브 알고리즘 댓글 참여율(Engagement Velocity) 10배 증폭 엔진]
    누구나 5초 만에 암산하여 숫자/단어로 즉시 댓글을 달 수 있는 아키타입별 '5초 직관 퀴즈'를 생성합니다.
    """
    puzzles_ko = {
        "pythagoras_fractal": "🧠 [5초 암산 챌린지 — 댓글에 정답 숫자를 남겨보세요!]\n직각삼각형의 두 작은 정사각형 넓이가 각각 9와 16일 때, 가장 큰 정사각형의 넓이는 얼마일까요? (루트 계산 없이 1초 만에 맞히셨다면 댓글로 숫자를 남겨주세요!)",
        "conic_reflection": "🧠 [5초 직관 챌린지 — 댓글에 정답 숫자를 남겨보세요!]\n포물선 위의 점 P에서 준선까지의 거리가 7일 때, 초점 F까지의 거리 PF는 얼마일까요? 1초 만에 보인다면 댓글로 정답을 남겨주세요!",
        "trig_harmonic": "🧠 [5초 파동 챌린지 — 댓글에 정답 숫자를 남겨보세요!]\n반지름이 1인 단위원에서 회전각이 90°(π/2)일 때 사인파의 높이(sin 90°)는 얼마일까요? 댓글로 숫자를 남겨주세요!",
        "fibonacci_golden": "🧠 [5초 수열 챌린지 — 댓글에 정답 숫자를 남겨보세요!]\n피보나치 수열 1, 1, 2, 3, 5, 8, 13... 에서 13 바로 다음에 올 숫자는 무엇일까요? 댓글로 정답을 남겨주세요!",
        "prob_galton": "🧠 [5초 확률 챌린지 — 댓글에 정답 숫자를 남겨보세요!]\n좌우 갈림길이 4번 있는 골턴 보드에서 구슬이 정중앙 칸에 도달하는 경로의 수(4C2)는 몇 가지일까요? 댓글로 도전해 보세요!",
        "calculus_motion": "🧠 [5초 미분 챌린지 — 댓글에 정답 숫자를 남겨보세요!]\n곡선 y = x² 위에서 x = 3일 때 접선의 기울기(2x)는 얼마일까요? 암산으로 맞히셨다면 댓글로 숫자를 남겨주세요!",
        "ceva_menelaus": "🧠 [5초 도형 챌린지 — 댓글에 정답 숫자를 남겨보세요!]\n높이가 같은 두 삼각형의 밑변의 비가 2 : 3이고 왼쪽 삼각형 넓이가 10일 때, 오른쪽 삼각형의 넓이는 얼마일까요? 댓글로 정답을 남겨주세요!",
        "circle_invariants": "🧠 [5초 원주각 챌린지 — 댓글에 정답 숫자를 남겨보세요!]\n원의 중심각 ∠AOB가 80°일 때, 원 위의 점 P가 어디로 움직이든 원주각 ∠APB는 항상 몇 도일까요? 댓글로 숫자를 남겨주세요!",
    }
    puzzles_en = {
        "pythagoras_fractal": "🧠 [5-Second Mental Math Challenge — Drop Your Answer in the Comments!]\nIf the two smaller squares on a right triangle have areas 9 and 16, what is the area of the largest square? Comment your number below!",
        "conic_reflection": "🧠 [5-Second Geometry Challenge — Drop Your Answer in the Comments!]\nIf a point P on a parabola is at distance 7 from the directrix, what is its exact distance PF to the focus F? Comment your answer!",
        "trig_harmonic": "🧠 [5-Second Wave Challenge — Drop Your Answer in the Comments!]\nOn a unit circle of radius 1, what is the exact height of the sine wave at 90° (sin 90°)? Comment your number below!",
        "fibonacci_golden": "🧠 [5-Second Pattern Challenge — Drop Your Answer in the Comments!]\nIn the Fibonacci sequence 1, 1, 2, 3, 5, 8, 13..., what number comes right after 13? Drop your answer in the comments!",
        "prob_galton": "🧠 [5-Second Probability Challenge — Drop Your Answer in the Comments!]\nIn a 4-row Galton board, how many distinct paths (4C2) lead a bead to the exact center bin? Comment your answer!",
        "calculus_motion": "🧠 [5-Second Calculus Challenge — Drop Your Answer in the Comments!]\nOn the curve y = x², what is the exact slope of the tangent line (2x) at x = 3? Comment your number below!",
        "ceva_menelaus": "🧠 [5-Second Area Ratio Challenge — Drop Your Answer in the Comments!]\nTwo triangles share the same height and have base ratio 2 : 3. If the left triangle has area 10, what is the area of the right triangle?",
        "circle_invariants": "🧠 [5-Second Circle Angle Challenge — Drop Your Answer in the Comments!]\nIf the central angle ∠AOB is 80°, what is the inscribed angle ∠APB for any point P on the circle? Comment your number!",
    }
    if lang_code == "ko":
        q_txt = puzzles_ko.get(archetype, puzzles_ko["pythagoras_fractal"])
        return (
            f"{q_txt}\n\n"
            f"🔔 [매일 새로운 창의 수학 시네마 받아보기 — 1초 구독]\n"
            f"👉 https://www.youtube.com/@min7014_ai?sub_confirmation=1\n\n"
            f"📐 [직접 마우스로 움직여보는 60fps 인터랙티브 셰이더 & GeoGebra]\n"
            f"👉 {ggb_url}"
        )
    else:
        q_txt = puzzles_en.get(archetype, puzzles_en["pythagoras_fractal"])
        return (
            f"{q_txt}\n\n"
            f"🔔 [1-Click Subscribe to @min7014_ai for Daily Visual Math]:\n"
            f"👉 https://www.youtube.com/@min7014_ai?sub_confirmation=1\n\n"
            f"📐 [Interactive 60fps Shader & GeoGebra Applet]:\n"
            f"👉 {ggb_url}"
        )


def render_creative_idea_thumbnail(sdoc: dict, lang_code: str = "ko") -> Path:
    """
    [고클릭률(High-CTR) 아키타입 맞춤형 네온 시네마 썸네일 생성기]
    - 모든 영상에 똑같은 문구를 넣던 배너 블라인드니스를 완전히 제거하고,
      8대 수학 아키타입별 맞춤형 호기심 역설 질문 + 우측 상단 초대형 네온 수식 콜아웃 배지를 합성합니다.
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
        "conic_reflection": (["왜 모든 평행광선은", "반드시 한 점(초점)에", "모이게 될까?"], "PF = PH"),
        "trig_harmonic": (["둥근 원이 돌면", "왜 완벽한 파동이", "만들어질까?"], "sin²θ+cos²θ=1"),
        "fibonacci_golden": (["자연과 은하계가", "137.5° 황금각을", "선택한 진짜 이유!"], "φ = 1.618..."),
        "prob_galton": (["수천 번의 우연이", "왜 항상 완벽한", "종 모양이 될까?"], "N(μ, σ²)"),
        "calculus_motion": (["두 점을 잇던 할선이", "접선으로 변하는", "극한의 찰나!"], "dy/dx = lim"),
        "ceva_menelaus": (["보조선 공식 없이", "넓이 비 하나로", "10초 만에 끝!"], "Ratio = 1"),
        "circle_invariants": (["점이 아무리 움직여도", "각도가 절대 변하지", "않는 기하의 마법!"], "∠P = 1/2 ∠O"),
    }
    thumb_hooks_en = {
        "pythagoras_fractal": (["Infinite Branches,", "Same Exact Area?", "1-Look Visual Proof!"], "a² + b² = c²"),
        "conic_reflection": (["Why Every Ray", "Bounces to One", "Exact Focus Point!"], "PF = PH"),
        "trig_harmonic": (["How a Spinning", "Circle Generates", "Every Wave!"], "sin²θ+cos²θ=1"),
        "fibonacci_golden": (["Why Nature Chose", "The 137.5° Golden", "Spiral Angle!"], "φ = 1.618..."),
        "prob_galton": (["How Random Chaos", "Always Forms a", "Perfect Bell Curve!"], "N(μ, σ²)"),
        "calculus_motion": (["The Exact Moment", "Secant Becomes", "Tangent Line!"], "dy/dx = lim"),
        "ceva_menelaus": (["No Extra Formulas!", "1 Area Ratio Trick", "Proves It All!"], "Ratio = 1"),
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

    ko_t, en_t = vmaker.split_bilingual_title(sdoc.get("title", slug_key))
    clean_title = sanitize_glyphs(
        vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(ko_t), max_len=36, lang="ko")
        if lang_code == "ko"
        else vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(en_t or sdoc.get("title_en") or ko_t), max_len=44, lang="en")
    )

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

    ko_t, en_t = vmaker.split_bilingual_title(sdoc.get("title", slug_key))
    clean_title = sanitize_glyphs(
        vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(ko_t), max_len=30, lang="ko")
        if lang_code == "ko"
        else vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(en_t or sdoc.get("title_en") or ko_t), max_len=38, lang="en")
    )

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
    clean_t = (
        vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(ko_t), max_len=36, lang="ko")
        if lang_code == "ko"
        else vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(en_t or sdoc.get("title_en") or ko_t), max_len=44, lang="en")
    )

    archetype = detect_visual_archetype(sdoc)
    title = build_viral_curiosity_youtube_title(clean_t, archetype, lang_code=lang_code, is_short=False)
    std_url = (sdoc.get("youtube_urls") or {}).get(lang_code) or f"https://www.youtube.com/results?search_query=min7014_ai+{slug_key}"
    ggb_url = sdoc.get("geogebra_url") or sdoc.get("source_page_url") or f"https://min7014.github.io/{slug_key}/"

    desc = (
        f"🌟 [Edition 5: 창의 수학 아이디어 시네마 (Pure Procedural Neon-Bloom Math Cinema)]\n"
        f"정적인 슬라이드 캡처를 완전히 벗어나, 수학적 본질 아이디어가 네온 블룸 프랙탈과 동적 기하 셰이더로 살아 움직이는 5막 스토리텔링 시네마입니다!\n\n"
        f"🔔 [지금 바로 @min7014_ai 채널 1초 구독하기]:\n"
        f"👉 https://www.youtube.com/@min7014_ai?sub_confirmation=1\n\n"
        f"🎬 [함께 보면 200% 시너지가 나는 연계 콘텐츠]\n"
        f"• 단계별 시각 증명 본편: {std_url}\n"
        f"• GeoGebra 인터랙티브 직접 조작: {ggb_url}\n"
        f"• mathedu 16,548문항 무료 문제은행: https://min7014.github.io/mathedu/video_board.html\n\n"
        f"#창의수학 #시각적증명 #{clean_t.replace(' ', '')} #수학아이디어 #수능수학 #기하학 #VisualProof #MathAnimation"
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
        comment_txt = build_viral_comment_puzzle(archetype, lang_code=lang_code, ggb_url=ggb_url)
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
    clean_t = (
        vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(ko_t), max_len=30, lang="ko")
        if lang_code == "ko"
        else vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(en_t or sdoc.get("title_en") or ko_t), max_len=38, lang="en")
    )

    yt, _ = vmaker.get_available_youtube_upload_service()
    if yt is None:
        raise RuntimeError("No available YouTube upload service / quota exhausted")
    existing_url = (sdoc.get("creative_idea_shorts_urls") or {}).get(lang_code, "")
    old_vid = vmaker.extract_youtube_video_id(existing_url)
    if old_vid:
        try:
            yt.videos().delete(id=old_vid).execute()
        except Exception:
            pass

    archetype = detect_visual_archetype(sdoc)
    title = build_viral_curiosity_youtube_title(clean_t, archetype, lang_code=lang_code, is_short=True)
    idea_full_url = (
        (sdoc.get("creative_idea_youtube_urls") or {}).get(lang_code)
        or (sdoc.get("youtube_urls") or {}).get(lang_code)
        or f"https://min7014.github.io/mathedu/video_board.html?slug={slug_key}&mode=idea"
    )
    ggb_url = sdoc.get("geogebra_url") or sdoc.get("source_page_url") or f"https://min7014.github.io/{slug_key}/"

    desc = (
        f"🌟📱 [Edition 5-B: 창의 수학 아이디어 #Shorts]\n"
        f"단 45초 만에 '{clean_t}'의 핵심 불변량 아이디어를 순수 네온 블룸 애니메이션으로 직관화합니다!\n\n"
        f"🔔 [지금 @min7014_ai 1초 구독하기]:\n"
        f"👉 https://www.youtube.com/@min7014_ai?sub_confirmation=1\n\n"
        f"🎬 [1080p 창의 아이디어 시네마 풀버전 보기]:\n"
        f"👉 {idea_full_url}\n\n"
        f"📐 [직접 조작하는 GeoGebra]:\n"
        f"👉 {ggb_url}\n\n"
        f"#Shorts #창의수학 #시각적증명 #수학쇼츠 #MathShorts #VisualProof"
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
        comment_txt = build_viral_comment_puzzle(archetype, lang_code=lang_code, ggb_url=idea_full_url)
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
            ct_long = sanitize_glyphs(vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(raw_t), max_len=36 if lg == "ko" else 44, lang=lg))
            ct_short = sanitize_glyphs(vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(raw_t), max_len=30 if lg == "ko" else 38, lang=lg))
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
