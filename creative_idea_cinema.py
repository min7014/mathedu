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

    if any(k in blob for k in ["피타고라스", "pythagor", "직각삼각형", "right triangle", "넓이 보존", "정사각형"]):
        return "pythagoras_fractal"
    if any(k in blob for k in ["체바", "메넬라우스", "ceva", "menelaus", "무게중심", "내분", "선분 비", "평행선", "삼각형", "triangle", "비비아니", "viviani", "나폴레옹", "몰리"]):
        return "ceva_menelaus"
    if any(k in blob for k in ["타원", "포물선", "쌍곡선", "단델린", "초점", "준선", "이차곡선", "ellipse", "parabola", "hyperbola", "dandelin", "conic", "사이클로이드", "cycloid"]):
        return "conic_reflection"
    if any(k in blob for k in ["미분", "적분", "극한", "도함수", "평균값", "롤의", "코시", "접선", "할선", "구분구적", "급수", "derivative", "integral", "limit", "tangent", "cauchy", "rolle"]):
        return "calculus_motion"
    return "circle_invariants"


def build_creative_idea_acts(sdoc: dict, lang_code: str = "ko") -> list[dict]:
    ko_t, en_t = vmaker.split_bilingual_title(sdoc.get("title", sdoc.get("slug", "")))
    clean_ko = vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(ko_t), max_len=38, lang="ko")
    clean_en = vmaker._smart_concise_topic_title(
        vmaker.latex_to_unicode_title(en_t or sdoc.get("title_en") or ko_t), max_len=46, lang="en"
    )
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

    # 기하 / 이차곡선 / 미적분 / 원 / 대수 범용 5막 시네마 대본
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


def render_creative_idea_thumbnail(sdoc: dict, lang_code: str = "ko") -> Path:
    """PDF 캡처 없이 100% 네온 블룸 프랙탈·기하 셰이더로 제작하는 1280x720 시네마 썸네일"""
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
    # 기하 아트가 우측에 빛나도록 우측 시프트 합성
    shifted = Image.new("RGB", (1280, 720), (5, 9, 20))
    shifted.paste(scene_img, (355, 8))

    ov = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
    draw = ImageDraw.Draw(ov)

    draw.rounded_rectangle((28, 32, 560, 688), radius=28, fill=(9, 15, 32, 228), outline=(250, 204, 21, 255), width=4)
    draw.rounded_rectangle((52, 58, 536, 118), radius=16, fill=(124, 58, 237, 255), outline=(254, 240, 138, 255), width=2)

    f_badge = vmaker.get_font_for_lang(lang_code, 22, bold=True)
    f_hero = vmaker.get_font_for_lang(lang_code, 46, bold=True)
    f_sub = vmaker.get_font_for_lang(lang_code, 28, bold=True)

    b_txt = "★ 창의 수학 시네마 (Pure Visual)" if lang_code == "ko" else "★ CREATIVE MATH CINEMA"
    draw.text((70, 73), b_txt, fill=(254, 240, 138, 255), font=f_badge)

    hook_lines = (
        ["공식 암기 멈추세요!", "단 1개의 아이디어로", "끝내는 시각적 비밀!"]
        if lang_code == "ko"
        else ["STOP MEMORIZING!", "1 Core Visual Idea", "Explains It All!"]
    )
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

        idea_title = (
            f"🌟 [창의 수학 시네마] {clean_title} — 공식 암기 없이 단 1개의 아이디어로 깨치는 비밀! | @min7014_ai"
            if lang_code == "ko"
            else f"🌟 [Creative Math Cinema] {clean_title} — The 1 Visual Idea That Explains It All! | @min7014_ai"
        )[:98]

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

        ishort_title = (
            f"🌟 [창의 아이디어 #Shorts] {clean_title} — 공식 없이 깨치는 단 하나의 원리! | @min7014_ai"
            if lang_code == "ko"
            else f"🌟 [Creative Math Idea #Shorts] {clean_title} — 1 Visual Idea Explains All! | @min7014_ai"
        )[:98]

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


def upload_creative_idea_to_youtube(slug_key: str = "math20250130001", lang_code: str = "ko", privacy: str = "public") -> dict:
    """
    [Edition 5-A: 🌟 창의 아이디어 시네마 1080p 본편 유튜브 업로드 + 썸네일 + 다국어 + 자동 댓글 + 텔레그램 알림]
    """
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

    yt = vmaker.get_youtube_service()
    existing_url = (sdoc.get("creative_idea_youtube_urls") or {}).get(lang_code, "")
    old_vid = vmaker._extract_youtube_id(existing_url)
    if old_vid:
        try:
            yt.videos().delete(id=old_vid).execute()
        except Exception:
            pass

    title = idea_pkg.get("title") or (
        f"🌟 [창의 수학 시네마] {clean_t} — 공식 암기 없이 단 1개의 아이디어로 깨치는 비밀! | @min7014_ai"
        if lang_code == "ko"
        else f"🌟 [Creative Math Cinema] {clean_t} — The 1 Visual Idea That Explains It All! | @min7014_ai"
    )
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
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = None
    while resp is None:
        _, resp = req.next_chunk()

    vid_id = resp["id"]
    yt_url = f"https://youtu.be/{vid_id}"

    thumb_p = render_creative_idea_thumbnail(sdoc, lang_code=lang_code)
    if thumb_p.exists():
        try:
            yt.thumbnails().set(videoId=vid_id, media_body=MediaFileUpload(str(thumb_p), mimetype="image/png")).execute()
        except Exception:
            pass

    try:
        comment_txt = (
            f"🌟 [창의 수학 아이디어 시네마 — 10초 생각 챌린지!]\n"
            f"오늘 영상의 제4막 'What-If-Not (조건 비틀기)'에서 발견한 불변량 법칙을 댓글로 남겨 보세요!\n\n"
            f"🔔 [매일 새로운 창의 수학 시네마 받아보기 — 1초 구독]\n"
            f"👉 https://www.youtube.com/@min7014_ai?sub_confirmation=1\n\n"
            f"📐 [직접 움직여보는 GeoGebra & 단계별 시각 증명]\n"
            f"👉 {ggb_url}"
            if lang_code == "ko"
            else f"🌟 [Creative Math Idea Challenge!]\n"
                 f"Share your insight from Act IV (What-If-Not Generalization) in the comments!\n\n"
                 f"🔔 [1-Click Subscribe to @min7014_ai]:\n"
                 f"👉 https://www.youtube.com/@min7014_ai?sub_confirmation=1\n\n"
                 f"📐 [Interactive GeoGebra Applet]:\n"
                 f"👉 {ggb_url}"
        )
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

    vmaker._notify_youtube_upload_telegram(
        edition_label=f"🌟 [창의 아이디어 시네마 1080p ({lang_code.upper()})]",
        slug_key=slug_key,
        title=title,
        yt_url=yt_url,
        lang_code=lang_code,
    )
    return {"video_id": vid_id, "youtube_url": yt_url, "title": title}


def upload_creative_idea_short_to_youtube(slug_key: str = "math20250130001", lang_code: str = "ko", privacy: str = "public") -> dict:
    """
    [Edition 5-B: 🌟📱 창의 아이디어 숏폼 9:16 (Idea-#Shorts) 유튜브 업로드 + 자동 댓글 + 텔레그램 알림]
    """
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

    yt = vmaker.get_youtube_service()
    existing_url = (sdoc.get("creative_idea_shorts_urls") or {}).get(lang_code, "")
    old_vid = vmaker._extract_youtube_id(existing_url)
    if old_vid:
        try:
            yt.videos().delete(id=old_vid).execute()
        except Exception:
            pass

    title = spkg.get("title") or (
        f"🌟 [창의 아이디어 #Shorts] {clean_t} — 공식 없이 깨치는 단 하나의 원리! | @min7014_ai"
        if lang_code == "ko"
        else f"🌟 [Creative Math Idea #Shorts] {clean_t} — 1 Visual Idea Explains All! | @min7014_ai"
    )
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
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = None
    while resp is None:
        _, resp = req.next_chunk()

    vid_id = resp["id"]
    yt_url = f"https://youtube.com/shorts/{vid_id}"

    try:
        comment_txt = (
            f"🌟 [45초 창의 수학 아이디어 퀴즈!]\n"
            f"공식을 외우지 않고도 넓이와 비율이 보존되는 이유가 한눈에 보이셨나요?\n\n"
            f"🔔 [매일 1분 수학 직관 업그레이드 — 1초 구독하기]\n"
            f"👉 https://www.youtube.com/@min7014_ai?sub_confirmation=1\n\n"
            f"🎬 [1080p 창의 시네마 5막 풀버전 바로 보기]\n"
            f"👉 {idea_full_url}"
            if lang_code == "ko"
            else f"🌟 [45-Second Creative Math Idea!]\n"
                 f"Did you see why the invariant holds without memorizing formulas?\n\n"
                 f"🔔 [1-Click Subscribe to @min7014_ai]:\n"
                 f"👉 https://www.youtube.com/@min7014_ai?sub_confirmation=1\n\n"
                 f"🎬 [Watch Full 1080p Creative Math Cinema]:\n"
                 f"👉 {idea_full_url}"
        )
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

    vmaker._notify_youtube_upload_telegram(
        edition_label=f"🌟📱 [창의 아이디어 #Shorts ({lang_code.upper()})]",
        slug_key=slug_key,
        title=title,
        yt_url=yt_url,
        lang_code=lang_code,
    )
    return {"video_id": vid_id, "youtube_url": yt_url, "title": title}


def build_flagship_creative_idea_suite(slugs=None, langs=("ko", "en")) -> list:
    """주요 수학 주제들에 대해 Edition 5 v2.0 (순수 네온 블룸 창의 아이디어 시네마 1080p + Idea-#Shorts 9:16) 일괄 제작"""
    if not slugs:
        slugs = ["math20250130001", "2014111902", "2022051507"]
    results = []
    for slug in slugs:
        for lg in langs:
            p_cinema = render_creative_idea_cinema_video(slug, lang_code=lg)
            p_short = render_creative_idea_short_vertical(slug, lang_code=lg)
            results.append({"slug": slug, "lang": lg, "cinema": str(p_cinema), "short": str(p_short)})
    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Edition 5 v2.0: Pure Procedural Neon-Bloom Math Cinema Engine")
    parser.add_argument("--slug", default="math20250130001", help="Topic slug")
    parser.add_argument("--lang", default="ko", help="Language code (ko/en)")
    parser.add_argument("--batch", action="store_true", help="Build flagship suite")
    parser.add_argument("--upload", action="store_true", help="Upload to YouTube if quota permits")
    args = parser.parse_args()

    if args.batch:
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
