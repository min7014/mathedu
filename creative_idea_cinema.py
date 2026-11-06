# -*- coding: utf-8 -*-
"""
[Edition 5: ★ 창의 아이디어 확장 시네마 (Creative Idea & Storytelling Math Cinema — Beyond PDF)]
- 기존 PDF 파일을 한 장씩 넘기며 설명하는 플립북 방식(Edition 1~4)을 넘어,
  해당 주제의 '핵심 수학적 내용과 아이디어(Core Idea & Invariant)'만을 추출해
  3Blue1Brown 스타일의 다크 블루프린트 절차적 벡터 애니메이션(Procedural Vector Animation)과
  5막 스토리텔링(① 직관 역설·일상 미스터리 → ② 라이브 수치·도형 실험 → ③ 결정적 보조선·아이디어 탄생
  → ④ What-If-Not 조건 변형·일반화 확장 → ⑤ 수능·경시 10초 통찰)으로 새롭게 제작하는 모듈입니다.
- 제작 결과물:
  1) Edition 5-A (1080p 16:9 창의 아이디어 시네마 본편):
     video_lectures/creative_idea/{slug}_idea_{lc}.mp4
     video_lectures/youtube_packages/{slug}_idea_{lc}_thumb.png
  2) Edition 5-B (9:16 1080x1920 창의 아이디어 숏폼 Idea-#Shorts):
     video_lectures/shorts/{slug}_short_idea_{lc}.mp4
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
import pymupdf
from PIL import Image, ImageDraw, ImageOps

import min7014_video_maker as vmaker

ROOT_DIR = vmaker.ROOT_DIR
SCRIPTS_DIR = vmaker.SCRIPTS_DIR
YT_PKG_DIR = vmaker.YT_PKG_DIR
YT_UPLOADS_DIR = vmaker.YT_UPLOADS_DIR
CREATIVE_IDEA_DIR = ROOT_DIR / "video_lectures" / "creative_idea"
CREATIVE_IDEA_DIR.mkdir(parents=True, exist_ok=True)


def detect_visual_archetype(sdoc: dict) -> str:
    """주제의 제목·개념·카테고리를 분석하여 최적의 절차적 애니메이션 아키타입을 결정합니다."""
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
    if any(k in blob for k in ["원주각", "중심각", "현", "원", "내접", "외접", "톨레미", "구점원", "접선", "circle", "inscribed", "chord", "ptolemy", "thales", "탈레스", "정칠각형", "정오각형", "다각형", "테셀레이션"]):
        return "circle_invariants"
    return "algebra_visual_blocks"


def build_creative_idea_acts(sdoc: dict, lang_code: str = "ko") -> list[dict]:
    """
    PDF 페이지별 낭독이 아니라, 주제의 핵심 수학적 아이디어(Core Idea)를 바탕으로
    5막 구성의 창의 확장 시네마 대본(Acts 1~5)을 생성합니다.
    """
    ko_t, en_t = vmaker.split_bilingual_title(sdoc.get("title", sdoc.get("slug", "")))
    clean_ko = vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(ko_t), max_len=38, lang="ko")
    clean_en = vmaker._smart_concise_topic_title(
        vmaker.latex_to_unicode_title(en_t or sdoc.get("title_en") or ko_t), max_len=46, lang="en"
    )
    t_title = clean_ko if lang_code == "ko" else clean_en

    tpa = sdoc.get("teacher_proof_analysis") or {}
    qcd = sdoc.get("question_classroom_design") or {}
    archetype = detect_visual_archetype(sdoc)

    inv_ko = vmaker.latex_to_unicode_title(tpa.get("core_invariant") or "도형이 변해도 흔들리지 않는 넓이와 비율의 등식 관계")
    polya_ko = vmaker.latex_to_unicode_title(tpa.get("polya_bridge") or "숨겨진 대칭성과 보조선을 연결해 복잡한 식을 단번에 단순화하는 발상")
    whatif_ko = vmaker.latex_to_unicode_title(tpa.get("what_if_extension") or "특수한 각도와 평면 도형의 성질을 일반 삼각형과 3차원 공간으로 넓히는 확장")

    if archetype == "pythagoras_fractal":
        if lang_code == "ko":
            return [
                {
                    "act": 1,
                    "badge": "ACT 1 · 직관을 깨는 수학 미스터리",
                    "headline": f"가지가 무한히 갈라져도 넓이 합이 똑같다?! ({t_title})",
                    "key_formula": "S1 + S2 = S0  (무한 프랙탈 넓이 보존)",
                    "narration": (
                        f"만약 나무의 줄기에서 두 개의 가지가 뻗어나가고, 그 가지마다 다시 수백, 수천 개의 작은 가지가 끝없이 갈라진다면 과연 무슨 일이 벌어질까요? "
                        f"상식적으로는 나뭇가지가 무한히 많아지면 넓이의 합도 끝없이 커질 것처럼 보입니다. "
                        f"하지만 놀랍게도 [{t_title}]의 세계에서는, 수천 개의 가지가 새로 돋아나도 각 단계의 정사각형 넓이 합이 맨 아래 뿌리 기둥 단 한 개의 넓이와 단 1밀리미터의 오차도 없이 영원히 똑같습니다! 왜 이런 마법 같은 일이 일어나는지 핵심 아이디어를 파헤쳐 봅시다."
                    ),
                    "bullets": [
                        "[Q] 상식의 역설: 가지 개수는 1 → 2 → 4 → 8 → 2ⁿ개로 폭발!",
                        "★ 수학적 진실: 각 단계 정사각형 넓이 합은 언제나 뿌리 넓이(c²)로 일정!",
                        "[핵심] 핵심 질문: 개수와 모양이 바뀌는데 무엇이 넓이를 완벽히 지켜줄까?",
                    ],
                },
                {
                    "act": 2,
                    "badge": "ACT 2 · 공식 없이 눈으로 보는 숫자 실험실",
                    "headline": "초등학생도 5초 만에 발견하는 3 · 4 · 5 넓이 블록 실험",
                    "key_formula": "3² (9) + 4² (16) = 5² (25)",
                    "narration": (
                        f"복잡한 문자는 잠시 잊고, 가장 친숙한 숫자 3, 4, 5로 직접 실험해 볼까요? "
                        f"가로세로가 5인 뿌리 정사각형의 넓이는 25칸입니다. 그 위에 밑변 3, 높이 4인 직각삼각형을 올리고 양쪽에 정사각형 가지를 띄우면, 왼쪽 가지는 9칸, 오른쪽 가지는 16칸이 됩니다. "
                        f"9 더하기 16은 정확히 25! 줄기 하나가 두 갈래로 쪼개졌을 뿐, 넓이의 총량은 단 한 칸도 사라지거나 늘어나지 않았습니다."
                    ),
                    "bullets": [
                        "[실험] 뿌리 정사각형 1개 넓이: 5 × 5 = 25칸",
                        "[1단계] 1단계 두 가지 넓이 합: 3²(9칸) + 4²(16칸) = 25칸 (100% 일치!)",
                        "[확장] 2단계 네 가지 넓이 합: (9의 두 갈래) + (16의 두 갈래) = 여전히 25칸!",
                    ],
                },
                {
                    "act": 3,
                    "badge": "ACT 3 · 천재들의 단 한 줄 보조선 아이디어",
                    "headline": "도형을 자르고 회전시키는 넓이 이동(Area Shear & Rotation)의 마법",
                    "key_formula": "a² + b² = c²  (직각삼각형 합동과 평행이동)",
                    "narration": (
                        f"이 현상을 지탱하는 단 하나의 핵심 아이디어는 바로 직각삼각형을 둘러싼 넓이의 분할과 보존입니다. "
                        f"직각 꼭짓점에서 빗변 정사각형으로 수선을 내려 보조선을 긋는 순간, 큰 정사각형은 왼쪽 직사각형과 오른쪽 직사각형 두 조각으로 정확히 나뉩니다. "
                        f"이 두 조각이 각각 위쪽의 두 작은 정사각형과 합동인 삼각형을 공유하기 때문에, 가지가 몇 단계로 뻗어나가든 넓이 총합은 도미노처럼 아랫단계로 고스란히 전달됩니다."
                    ),
                    "bullets": [
                        f"[원리] 핵심 불변량: {inv_ko[:46]}",
                        f"[도형] 결정적 보조선: {polya_ko[:46]}",
                        "[통찰] 깨달음: 식을 전개하는 대신 넓이 조각의 이동 경로를 추적하라!",
                    ],
                },
                {
                    "act": 4,
                    "badge": "ACT 4 · PDF 너머의 상상 (What-If-Not 조건 변형)",
                    "headline": "만약 정사각형 대신 반원이나 정삼각형을 붙인다면? 직각이 아니라면?",
                    "key_formula": "S(닮음도형) ∝ 변의 길이²  →  반원·정삼각형도 성립!",
                    "narration": (
                        f"이제 원래 자료를 넘어 한 걸음 더 대담한 질문을 던져 봅시다. "
                        f"만약 직각삼각형의 세 변 위에 정사각형이 아니라 반원을 그리거나 정삼각형을 붙인다면, 그때도 두 작은 도형의 넓이 합이 가장 큰 도형의 넓이와 같을까요? "
                        f"정답은 무조건 예스입니다! 모든 닮음 도형의 넓이는 변의 길이의 제곱에 비례하기 때문입니다. 반대로 사잇각이 90도가 아니라 예각이나 둔각으로 바뀌면, 그 어긋난 넓이 차이만큼을 보정해 주는 식이 바로 고등학교의 코사인법칙이 됩니다."
                    ),
                    "bullets": [
                        "[변형] 확장 1 (모양 변경): 세 변에 반원·정삼각형·정오각형을 붙여도 S1 + S2 = S3!",
                        "[변형] 확장 2 (각도 변경): 90°가 무너지면? → c² = a² + b² - 2ab·cosθ (코사인법칙!)",
                        f"[심화] 심화 연결: {whatif_ko[:44]}",
                    ],
                },
                {
                    "act": 5,
                    "badge": "ACT 5 · 수능·경시 킬러 10초 통찰 & 유레카 정리",
                    "headline": "개별 넓이를 따로 구하지 말고 '뿌리 불변량' 하나로 10초 만에 끝내라!",
                    "key_formula": "∑ (n단계 모든 조각 넓이) = 오직 출발 도형 1개의 넓이!",
                    "narration": (
                        f"수능과 수학 경시대회에서 도형이 수없이 쪼개지거나 반복되는 프랙탈 문제가 나오면, 학생들은 조각 하나하나의 길이를 구하느라 시간을 다 써버립니다. "
                        f"하지만 오늘 깨달은 아이디어를 기억하세요! 복잡한 5단계, 10단계 조각들의 합을 구하라는 문제는 반드시 1단계 출발 도형과 넓이가 보존되는 불변 구조를 숨겨두고 있습니다. "
                        f"매일 새롭게 펼쳐지는 창의 수학 시네마를 놓치지 않으려면 지금 바로 구독과 좋아요를 눌러주세요!"
                    ),
                    "bullets": [
                        "[실전] 실전 치트키: 복잡한 n단계 도형 합 = 0단계 뿌리 도형에서 바로 암산!",
                        "[유레카] 오늘의 한 줄 통찰: '공식은 외우는 것이 아니라 넓이의 이동을 눈으로 보는 것이다!'",
                        "▶ 지금 [@min7014_ai 구독] 누르고 1,113개 창의 수학 아이디어를 정복하세요!",
                    ],
                },
            ]
        else:
            return [
                {
                    "act": 1,
                    "badge": "ACT 1 · THE GEOMETRIC PARADOX",
                    "headline": f"Infinite Branches, Yet Exact Same Area?! ({t_title})",
                    "key_formula": "S1 + S2 = S0  (Fractal Area Conservation)",
                    "narration": (
                        f"Imagine a tree where every trunk splits into two branches, and those branches split again hundreds of times. "
                        f"Intuition tells us that as the number of branches explodes, the total area should grow indefinitely. "
                        f"Yet in [{t_title}], every single generation of squares adds up to the exact same area as the single starting trunk! Let's uncover the visual idea behind this geometric miracle."
                    ),
                    "bullets": [
                        "[Q] The Paradox: Branch count explodes 1 → 2 → 4 → 2ⁿ!",
                        "★ The Invariant: Total area of each level stays locked at c²!",
                        "[핵심] Core Question: What geometric law preserves the exact area?",
                    ],
                },
                {
                    "act": 2,
                    "badge": "ACT 2 · LIVE NUMERICAL LAB",
                    "headline": "Testing the 3 - 4 - 5 Area Conservation in 5 Seconds",
                    "key_formula": "3² (9) + 4² (16) = 5² (25)",
                    "narration": (
                        f"Before writing any abstract equations, let's test this with simple numbers: 3, 4, and 5. "
                        f"A trunk square of side 5 has 25 unit tiles. Place a 3-4-5 right triangle on top, and the two branch squares have 9 tiles and 16 tiles. "
                        f"9 plus 16 equals 25! Not a single tile of area is lost or created as the tree branches upward."
                    ),
                    "bullets": [
                        "[실험] Root Trunk Square: 5 × 5 = 25 unit tiles",
                        "[1단계] Level 1 Branches: 3² (9) + 4² (16) = 25 unit tiles!",
                        "[확장] Level N Branches: Every split preserves 100% of its parent area!",
                    ],
                },
                {
                    "act": 3,
                    "badge": "ACT 3 · THE ONE-LINE VISUAL IDEA",
                    "headline": "Auxiliary Altitude & Area Shear Transformation",
                    "key_formula": "a² + b² = c²  (Congruent Triangle Partition)",
                    "narration": (
                        f"The entire proof rests on one brilliant auxiliary line: drop a perpendicular altitude from the right angle straight through the hypotenuse square. "
                        f"This single line slices the trunk square into two rectangles whose areas exactly match the two upper squares through congruent triangles. "
                        f"Instead of algebraic expansion, we literally watch the area flow from the trunk into the branches!"
                    ),
                    "bullets": [
                        "[원리] Core Invariant: Area is conserved across every right-triangle split",
                        "[도형] Key Auxiliary Line: Altitude from the right-angle vertex to the hypotenuse",
                        "[통찰] Visual Insight: Follow the moving area blocks instead of memorizing formulas!",
                    ],
                },
                {
                    "act": 4,
                    "badge": "ACT 4 · WHAT-IF-NOT EXPANSION",
                    "headline": "What If We Attach Semicircles Instead of Squares? Or Change 90°?",
                    "key_formula": "Area ∝ (Length)²  →  Works for Semicircles & Polygons!",
                    "narration": (
                        f"Now let's go beyond the original diagram! What if we replace the squares on the three sides with semicircles, equilateral triangles, or any similar shapes? "
                        f"Because the area of any similar figure scales with the square of its side length, the two smaller semicircles still equal the largest semicircle! "
                        f"And what if the angle is no longer 90 degrees? The exact area deficit or surplus gives birth to the Law of Cosines!"
                    ),
                    "bullets": [
                        "[변형] What-If 1: Semicircles or equilateral triangles on the 3 sides still sum equally!",
                        "[변형] What-If 2: Change 90° to θ → c² = a² + b² - 2ab·cosθ (Law of Cosines!)",
                        "[심화] One concept connects elementary area to high school trigonometry!",
                    ],
                },
                {
                    "act": 5,
                    "badge": "ACT 5 · OLYMPIAD & EXAM TAKEAWAY",
                    "headline": "Solve Multi-Step Fractal & Geometry Problems in 10 Seconds!",
                    "key_formula": "∑ (All Level-N Branches) = Area of Root Trunk!",
                    "narration": (
                        f"When an exam asks for the sum of 16 or 32 tiny squares in a repeating geometric figure, never calculate each branch one by one. "
                        f"Collapse the entire tree back to the root trunk using area conservation and solve it in 10 seconds! "
                        f"Hit Subscribe right now for daily visual math cinema on @min7014_ai!"
                    ),
                    "bullets": [
                        "[실전] 10-Sec Exam Hack: Collapse level-N sums back to the level-0 invariant!",
                        "[유레카] Golden Rule: See the invariant structure before touching algebra.",
                        "▶ Subscribe to @min7014_ai & try the interactive GeoGebra lab in the description!",
                    ],
                },
            ]

    # 일반/기하/미적분/원/이차곡선/대수 전 영역 범용 5막 창의 스토리텔링 생성
    if lang_code == "ko":
        return [
            {
                "act": 1,
                "badge": "ACT 1 · 직관을 깨는 수학 미스터리",
                "headline": f"모양과 위치가 계속 바뀌는데 왜 이 값은 절대 변하지 않을까? ({t_title})",
                "key_formula": f"핵심 테제 · {t_title}",
                "narration": (
                    f"도형 위의 점을 이리저리 움직이거나 숫자를 바꾸면 모든 길이와 각도가 복잡하게 요동칩니다. "
                    f"그런데 참 이상합니다! [{t_title}]에서는 점을 어디로 옮겨 놓아도 특정한 비율이나 관계식이 마치 자석에 고정된 것처럼 단 1의 오차도 없이 일정하게 유지됩니다. "
                    f"단순히 책에 적힌 결과를 한 줄씩 따라 읽는 것을 넘어, 도대체 어떤 숨겨진 아이디어가 이 완벽한 질서를 만들어내는지 근본 원리부터 새롭게 파헤쳐 봅시다!"
                ),
                "bullets": [
                    f"[Q] 직관의 의문: 점과 선이 움직이는데 왜 [{t_title}]은 항상 성립할까?",
                    f"🔍 숨겨진 불변량: {inv_ko[:48]}",
                    "[핵심] 오늘의 목표: PDF 페이지 암기가 아닌 '단 하나의 핵심 아이디어' 완전 체득!",
                ],
            },
            {
                "act": 2,
                "badge": "ACT 2 · 공식 없이 눈으로 보는 실험실",
                "headline": "가장 단순한 대칭 상태와 구체적 수치로 핵심 규칙 발견하기",
                "key_formula": "극단적 대칭 상태(Symmetry Test) → 불변량 즉시 포착!",
                "narration": (
                    f"수학자들이 새로운 정리를 발견할 때는 결코 처음부터 복잡한 문자로 식을 전개하지 않습니다. "
                    f"가장 먼저 도형을 완벽히 대칭인 한가운데에 놓거나, 1, 2, 3처럼 아주 간단한 숫자를 넣어 실험해 봅니다. "
                    f"화면의 시뮬레이션처럼 대칭 상태에서 성립하는 명쾌한 비율과 넓이 균형을 먼저 눈으로 확인하면, 일반화된 정리의 결론이 왜 그런 모양을 가질 수밖에 없는지 공식 없이도 단번에 예측할 수 있습니다."
                ),
                "bullets": [
                    "[실험] 1단계 실험: 정중앙 대칭 위치에서 비율·넓이 균형점 즉시 확인",
                    "▶ 2단계 실험: 점을 이동시켜도 상쇄 구조 덕분에 최종 결과값 유지!",
                    "[통찰] 초등 눈높이 직관: 복잡한 기호도 결국은 '같은 넓이와 비례 묶기'의 약속!",
                ],
            },
            {
                "act": 3,
                "badge": "ACT 3 · 천재들의 단 한 줄 보조선 아이디어",
                "headline": "보조선 딱 한 줄이 흩어진 조건들을 도미노처럼 연결하는 순간!",
                "key_formula": "결정적 보조선 1줄 → 닮음·넓이 비·대칭 연쇄 약분!",
                "narration": (
                    f"그렇다면 대칭이 아닌 일반적인 위치에서도 왜 이 성질이 흔들리지 않을까요? 비밀은 바로 지금 화면에 그어지는 결정적 보조선 한 줄에 있습니다! "
                    f"{polya_ko} "
                    f"서로 아무 관련 없어 보이던 선분과 각도들이 이 보조선 하나를 매개체로 만나면서, 높이가 같은 삼각형의 넓이 비나 평행선 닮음비를 통해 도미노처럼 연쇄적으로 맞물려 증명됩니다."
                ),
                "bullets": [
                    f"[도형] 핵심 보조선 발상: {polya_ko[:48]}",
                    f"★ 구조적 원리: {inv_ko[:48]}",
                    "✨ 한 줄의 보조선이 복잡한 방정식 10줄을 단숨에 대체합니다!",
                ],
            },
            {
                "act": 4,
                "badge": "ACT 4 · PDF 너머의 상상 (What-If-Not 조건 변형)",
                "headline": "만약 점이 도형 밖으로 나가거나 극한의 순간에 도달한다면?",
                "key_formula": "내부 → 외부 → 접선 극한 → 3차원 공간으로의 무한 확장!",
                "narration": (
                    f"이제 원본 자료의 경계를 넘어 생각의 근육을 넓혀 봅시다. "
                    f"만약 도형 내부에 있던 점이 경계선 밖으로 빠져나가면 이 정리는 깨질까요, 아니면 외분점과 부호 대칭을 통해 그대로 유지될까요? "
                    f"또 두 점이 한없이 가까워져 할선이 접선이 되는 극한의 순간에는 어떤 새로운 정리로 변신할까요? {whatif_ko} "
                    f"이렇게 조건 하나를 비틀어 보는 순간, 단편적인 공식 하나가 중학교 기하부터 고등학교 미적분까지 하나의 거대한 뿌리로 연결됩니다."
                ),
                "bullets": [
                    "[변형] 조건 변형 1: 내부의 점을 외부(연장선)로 옮기면? → 외분·연장선 정리로 그대로 성립!",
                    "[변형] 조건 변형 2: 두 점을 한 점으로 합치면? → 할선이 접선(미분 기울기)으로 진화!",
                    f"[확장] 계통성 확장: {whatif_ko[:46]}",
                ],
            },
            {
                "act": 5,
                "badge": "ACT 5 · 수능·경시 킬러 10초 통찰 & 유레카 정리",
                "headline": "실전 문제에서 이 아이디어 하나를 1초 만에 꺼내 쓰는 법!",
                "key_formula": "조건 포착 → 제1보조선 작동 → 10초 만에 킬러 문항 격파!",
                "narration": (
                    f"오늘 우리가 탐구한 [{t_title}]의 진짜 가치는 결과 공식의 암기가 아니라, 막막한 도형이나 식을 만났을 때 어디에 첫 번째 보조선을 그어야 하는지 알려주는 나침반이라는 점입니다. "
                    f"설명란과 고정댓글의 링크를 누르시면 지오지브라로 이 도형을 직접 움직여 보고, 5지선다 찍기 없이 내 손으로 식을 조립하는 실전 문제까지 무료로 체험하실 수 있습니다. "
                    f"지금 바로 채널 구독과 좋아요를 누르고 매일 새로운 수학적 유레카를 만나보세요!"
                ),
                "bullets": [
                    f"[실전] 실전 제1발상: [{t_title}] 조건이 보이면 지체 없이 대칭·보조선부터 연결!",
                    "[도형] 설명란·고정댓글 링크에서 무료 GeoGebra 조작 & 수능 기출 디딤돌 즉시 체험",
                    "▶ 지금 [@min7014_ai 구독] 누르고 눈으로 깨치는 수학 시리즈를 정주행하세요!",
                ],
            },
        ]
    else:
        return [
            {
                "act": 1,
                "badge": "ACT 1 · THE MATHEMATICAL MYSTERY",
                "headline": f"Everything Moves, Yet This Stays Locked?! ({t_title})",
                "key_formula": f"Core Invariant · {t_title}",
                "narration": (
                    f"When you drag points and lines across a geometric figure, lengths and angles change wildly. "
                    f"Yet inside [{t_title}], a hidden mathematical invariant stays completely unchanged no matter how you deform the configuration! "
                    f"Instead of just flipping through static pages, let's build the core idea from the ground up through dynamic visual intuition."
                ),
                "bullets": [
                    f"[Q] The Mystery: Why does [{t_title}] hold true in every configuration?",
                    "🔍 Hidden Invariant: A structural balance of ratios, angles, or areas",
                    "[핵심] Goal: Master the single core idea behind the theorem without rote memorization!",
                ],
            },
            {
                "act": 2,
                "badge": "ACT 2 · LIVE VISUAL EXPERIMENT",
                "headline": "Discovering the Pattern Through Symmetry & Simple Numbers",
                "key_formula": "Symmetric Case → Instant Pattern Recognition!",
                "narration": (
                    f"Great mathematicians never start with messy equations—they test the most symmetric case and simple whole numbers first! "
                    f"Watch how placing the figure in a balanced, symmetric state immediately reveals why the ratios and areas lock into place. "
                    f"Once your eyes see this balance in the simplest case, the general formula becomes completely natural."
                ),
                "bullets": [
                    "[실험] Step 1: Test the symmetric center case with simple whole numbers",
                    "▶ Step 2: Perturb the figure and watch opposing changes cancel out!",
                    "[통찰] Intuition First: Equations are just a shorthand for visual balance.",
                ],
            },
            {
                "act": 3,
                "badge": "ACT 3 · THE ONE-LINE AUXILIARY IDEA",
                "headline": "How One Auxiliary Line Connects Every Clue Like Dominoes",
                "key_formula": "1 Auxiliary Line → Area / Similarity Domino Cancellation!",
                "narration": (
                    f"Why does the invariant survive even when symmetry is broken? The secret lies in a single auxiliary construction! "
                    f"By drawing one strategic line—a parallel line, an altitude, or a shared radius—disconnected segments suddenly share a common triangle height or similar ratio, causing every complex term to cancel out like dominoes."
                ),
                "bullets": [
                    "[도형] Strategic Auxiliary Line: Bridges disconnected lengths and angles",
                    "★ Domino Cancellation: Shared heights and similar triangles simplify the proof",
                    "✨ One visual line replaces ten lines of tedious algebra!",
                ],
            },
            {
                "act": 4,
                "badge": "ACT 4 · WHAT-IF-NOT IDEA EXPANSION",
                "headline": "What If the Point Moves Outside or Reaches the Limit?",
                "key_formula": "Interior → Exterior → Tangent Limit → 3D Generalization!",
                "narration": (
                    f"Now let's push beyond the textbook! What happens if we move the point outside the figure, or slide two points infinitely close together until a secant line becomes a tangent? "
                    f"Remarkably, the exact same core idea generalizes to exterior divisions, limiting tangent derivatives, and even higher-dimensional geometry!"
                ),
                "bullets": [
                    "[변형] What-If 1: Move the point outside → External division preserves the theorem!",
                    "[변형] What-If 2: Merge two points together → Secants smoothly become tangents!",
                    "[확장] One core idea unifies geometry, algebra, and calculus!",
                ],
            },
            {
                "act": 5,
                "badge": "ACT 5 · 10-SECOND EXAM INSIGHT & TAKEAWAY",
                "headline": "Turning Visual Intuition Into Instant Problem-Solving Power",
                "key_formula": "Spot the Cue → Draw the Auxiliary Line → 10-Sec Solution!",
                "narration": (
                    f"The true power of [{t_title}] is knowing exactly which auxiliary line to draw the moment you see a hard problem. "
                    f"Click the link in the description and pinned comment to manipulate this figure yourself in GeoGebra and solve constructive math challenges. "
                    f"Subscribe to @min7014_ai right now for daily visual math breakthroughs!"
                ),
                "bullets": [
                    f"[실전] Instant Trigger: Spot the [{t_title}] pattern and apply the invariant directly!",
                    "[도형] Free interactive GeoGebra & constructive problem lab in the description",
                    "▶ Subscribe to @min7014_ai for daily visual proofs and masterclasses!",
                ],
            },
        ]


def _extract_Inverted_blueprint_crop(doc, page_idx: int, target_w: int, target_h: int) -> Image.Image:
    """원본 PDF에서 핵심 도형 영역을 추출해 다크 시네마 블루프린트 스타일 카드 이미지로 변환합니다."""
    p_i = max(0, min(len(doc) - 1, page_idx))
    pix = doc[p_i].get_pixmap(dpi=180)
    pil_img = vmaker._mask_pdf_bottom_author_bar(Image.frombytes("RGB", [pix.width, pix.height], pix.samples))
    sw, sh = pil_img.size
    scale = min(target_w / max(1, sw), target_h / max(1, sh))
    nw, nh = max(1, int(sw * scale)), max(1, int(sh * scale))
    resized = pil_img.resize((nw, nh), Image.Resampling.LANCZOS)
    card = Image.new("RGB", (target_w, target_h), (255, 255, 255))
    card.paste(resized, ((target_w - nw) // 2, (target_h - nh) // 2))
    return card


def draw_procedural_math_stage(
    draw: ImageDraw.ImageDraw,
    canvas: Image.Image,
    archetype: str,
    act_num: int,
    t: float,
    box: tuple[int, int, int, int],
    doc,
    lang_code: str = "ko",
):
    """
    box = (x0, y0, x1, y1) 영역 내부에 3Blue1Brown 스타일 다크 블루프린트 배경과
    t ∈ [0.0, 1.0]에 따라 살아 움직이는 절차적 기하·대수 애니메이션을 작도합니다.
    """
    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0
    cx = x0 + int(w * 0.42)
    cy = y0 + int(h * 0.54)

    # 1. 다크 코스믹 블루프린트 스테이지 배경 및 은은한 모눈 그리드
    draw.rounded_rectangle(box, radius=24, fill=(8, 15, 32), outline=(56, 189, 248), width=3)
    grid_step = 48
    for gx in range(x0 + grid_step, x1, grid_step):
        draw.line([(gx, y0 + 6), (gx, y1 - 6)], fill=(17, 29, 58), width=1)
    for gy in range(y0 + grid_step, y1, grid_step):
        draw.line([(x0 + 6, gy), (x1 - 6, gy)], fill=(17, 29, 58), width=1)

    font_lbl = vmaker.get_font_for_lang(lang_code, 19, bold=True)
    font_big = vmaker.get_font_for_lang(lang_code, 26, bold=True)
    font_sm = vmaker.get_font_for_lang(lang_code, 16, bold=True)

    # 2. 아키타입별 살아 움직이는 절차적 벡터 애니메이션 (t: 0.0 -> 1.0)
    if archetype == "pythagoras_fractal":
        # 직각삼각형 + 정사각형 / 프랙탈 가지 / Act 4 반원 확장 동적 애니메이션
        base_s = min(w, h) * 0.22
        # 직각삼각형 세 꼭짓점 (A: 왼쪽 아래, B: 오른쪽 아래, C: 위쪽 직각 꼭짓점)
        angle_rot = 0.6435  # 3-4-5 triangle angle
        A = (cx - base_s * 0.5, cy + base_s * 0.25)
        B = (cx + base_s * 0.5, cy + base_s * 0.25)
        C = (
            A[0] + base_s * math.cos(angle_rot) * math.cos(angle_rot),
            A[1] - base_s * math.cos(angle_rot) * math.sin(angle_rot),
        )
        # 아래 뿌리 정사각형 (c^2)
        S0 = [A, B, (B[0], B[1] + base_s), (A[0], A[1] + base_s)]
        draw.polygon(S0, fill=(30, 64, 175), outline=(56, 189, 248), width=3)
        draw.text((int(cx - 58), int(B[1] + base_s * 0.42)), "c² = 25", fill=(254, 240, 138), font=font_big)

        # 직각삼각형 본체
        draw.polygon([A, B, C], fill=(15, 118, 110), outline=(45, 212, 191), width=4)

        # 왼쪽 정사각형 (a^2 = 16) & 오른쪽 정사각형 (b^2 = 9) 성장 애니메이션
        grow = min(1.0, 0.35 + 0.65 * t)
        vx_ac, vy_ac = C[0] - A[0], C[1] - A[1]
        nx_ac, ny_ac = vy_ac * grow, -vx_ac * grow
        S1 = [A, C, (C[0] + nx_ac, C[1] + ny_ac), (A[0] + nx_ac, A[1] + ny_ac)]

        vx_cb, vy_cb = B[0] - C[0], B[1] - C[1]
        nx_cb, ny_cb = vy_cb * grow, -vx_cb * grow
        S2 = [C, B, (B[0] + nx_cb, B[1] + ny_cb), (C[0] + nx_cb, C[1] + ny_cb)]

        if act_num == 4:
            # Act 4: What-If-Not (정사각형 -> 반원·정삼각형 일반화 시연)
            for p_start, p_end, col in [(A, C, (244, 63, 94)), (C, B, (16, 185, 129)), (A, B, (56, 189, 248))]:
                mx, my = (p_start[0] + p_end[0]) / 2, (p_start[1] + p_end[1]) / 2
                rad = int(math.hypot(p_end[0] - p_start[0], p_end[1] - p_start[1]) / 2 * grow)
                if rad > 6:
                    draw.ellipse((mx - rad, my - rad, mx + rad, my + rad), outline=col, width=4)
        else:
            draw.polygon(S1, fill=(136, 19, 55), outline=(251, 113, 133), width=3)
            draw.polygon(S2, fill=(6, 78, 59), outline=(52, 211, 153), width=3)

        # Act 3: 직각 꼭짓점 C에서 빗변 정사각형으로 내려긋는 결정적 수선(보조선) 애니메이션
        if act_num in (3, 5):
            alt_end_y = A[1] + base_s * t
            draw.line([(C[0], C[1]), (C[0], alt_end_y)], fill=(250, 204, 21), width=5)
            draw.ellipse((C[0] - 7, alt_end_y - 7, C[0] + 7, alt_end_y + 7), fill=(225, 29, 72), outline=(255, 255, 255), width=2)

        # 우측 상단 실시간 넓이 보존 게이지 바
        gx0 = x0 + int(w * 0.53)
        gy0 = y0 + 28
        draw.rounded_rectangle((gx0, gy0, x1 - 22, gy0 + 158), radius=16, fill=(15, 23, 42), outline=(251, 191, 36), width=2)
        g_hdr = "▶ 실시간 넓이 불변량 모니터" if lang_code == "ko" else "▶ Live Area Invariant Meter"
        draw.text((gx0 + 16, gy0 + 12), g_hdr, fill=(254, 240, 138), font=font_sm)
        draw.text((gx0 + 16, gy0 + 46), "a² (16.0) + b² (9.0) = 25.0", fill=(52, 211, 153), font=font_lbl)
        draw.text((gx0 + 16, gy0 + 82), "Root Trunk c²       = 25.0", fill=(56, 189, 248), font=font_lbl)
        bar_w = max(20, int((x1 - gx0 - 54) * min(1.0, 0.25 + 0.75 * t)))
        draw.rounded_rectangle((gx0 + 16, gy0 + 118, gx0 + 16 + bar_w, gy0 + 140), radius=8, fill=(250, 204, 21))

    elif archetype == "ceva_menelaus":
        # 삼각형 ABC + 동적 내부 교점 P(t) + 세 체바 선분 & 넓이 비 도미노 약분 애니메이션
        R = min(w, h) * 0.34
        A = (cx, cy - R * 0.92)
        B = (cx - R * 1.05, cy + R * 0.72)
        C = (cx + R * 1.05, cy + R * 0.72)
        # 내부 교점 P가 시간에 따라 부드럽게 이동해도 비율 곱은 항상 1.000!
        angle_t = t * math.pi * 2
        P = (cx + math.cos(angle_t) * R * 0.18, cy + R * 0.12 + math.sin(angle_t) * R * 0.12)

        # 세 내부 분할 삼각형 색칠
        draw.polygon([P, A, B], fill=(30, 58, 138), outline=(56, 189, 248), width=2)
        draw.polygon([P, B, C], fill=(6, 78, 59), outline=(52, 211, 153), width=2)
        draw.polygon([P, C, A], fill=(136, 19, 55), outline=(251, 113, 133), width=2)
        draw.polygon([A, B, C], outline=(255, 255, 255), width=4)

        # 꼭짓점 A, B, C에서 P를 지나는 연장선(체바 선분) 작도
        for V, col in [(A, (250, 204, 21)), (B, (56, 189, 248)), (C, (251, 113, 133))]:
            dx, dy = P[0] - V[0], P[1] - V[1]
            end_pt = (V[0] + dx * 1.55, V[1] + dy * 1.55)
            draw.line([V, end_pt], fill=col, width=4)
        draw.ellipse((P[0] - 9, P[1] - 9, P[0] + 9, P[1] + 9), fill=(250, 204, 21), outline=(255, 255, 255), width=3)

        # 우측 상단 실시간 비율 곱 도미노 약분 모니터
        gx0 = x0 + int(w * 0.53)
        gy0 = y0 + 28
        draw.rounded_rectangle((gx0, gy0, x1 - 22, gy0 + 162), radius=16, fill=(15, 23, 42), outline=(251, 191, 36), width=2)
        g_hdr = "★ 실시간 비율 곱(Invariant) 실험" if lang_code == "ko" else "★ Live Ratio Product Meter"
        draw.text((gx0 + 16, gy0 + 12), g_hdr, fill=(254, 240, 138), font=font_sm)
        draw.text((gx0 + 16, gy0 + 48), "(S1/S2) × (S2/S3) × (S3/S1)", fill=(56, 189, 248), font=font_lbl)
        if t > 0.35:
            # 분모·분자 연쇄 약분 사선 연출
            draw.line([(gx0 + 24, gy0 + 74), (gx0 + 290, gy0 + 48)], fill=(244, 63, 94), width=3)
        draw.text((gx0 + 16, gy0 + 96), "👉 곱 불변량 = 1.000 (항상 일정!)", fill=(52, 211, 153), font=font_lbl)

    elif archetype == "conic_reflection":
        # 타원/포물선 초점 F1에서 발사된 빛이 곡면에 반사되어 초점 F2로 정확히 수렴하는 레이트레이싱 애니메이션
        rx, ry = int(min(w, h) * 0.38), int(min(w, h) * 0.26)
        draw.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(15, 23, 42), outline=(56, 189, 248), width=4)
        c_dist = int(math.sqrt(max(1, rx * rx - ry * ry)))
        F1 = (cx - c_dist, cy)
        F2 = (cx + c_dist, cy)

        theta = (0.25 + 0.55 * t) * math.pi
        P = (cx + int(rx * math.cos(theta)), cy - int(ry * math.sin(theta)))

        # 접선 보조선 작도
        tx, ty = -rx * math.sin(theta), ry * math.cos(theta)
        draw.line([(P[0] - tx * 0.5, P[1] - ty * 0.5), (P[0] + tx * 0.5, P[1] + ty * 0.5)], fill=(148, 163, 184), width=3)

        # F1 -> P -> F2 빛의 반사 경로
        draw.line([F1, P], fill=(250, 204, 21), width=5)
        draw.line([P, F2], fill=(244, 63, 94), width=5)
        for F, lbl in [(F1, "F1"), (F2, "F2")]:
            draw.ellipse((F[0] - 9, F[1] - 9, F[0] + 9, F[1] + 9), fill=(225, 29, 72), outline=(255, 255, 255), width=2)
            draw.text((F[0] - 12, F[1] + 14), lbl, fill=(254, 240, 138), font=font_lbl)
        draw.ellipse((P[0] - 8, P[1] - 8, P[0] + 8, P[1] + 8), fill=(52, 211, 153), outline=(255, 255, 255), width=2)

        gx0 = x0 + int(w * 0.53)
        gy0 = y0 + 28
        draw.rounded_rectangle((gx0, gy0, x1 - 22, gy0 + 150), radius=16, fill=(15, 23, 42), outline=(251, 191, 36), width=2)
        draw.text((gx0 + 16, gy0 + 14), "★ 초점 거리 합 & 반사각 불변량", fill=(254, 240, 138), font=font_sm)
        draw.text((gx0 + 16, gy0 + 52), "|PF1| + |PF2| = 2a (일정!)", fill=(56, 189, 248), font=font_lbl)
        draw.text((gx0 + 16, gy0 + 92), "입사각 α = 반사각 β (100% 수렴)", fill=(52, 211, 153), font=font_lbl)

    elif archetype == "calculus_motion":
        # 곡선 y=f(x) 위의 할선(Secant)이 접선(Tangent)으로 수렴하고 리만 직사각형이 넓이를 채우는 애니메이션
        ax0, ay0 = x0 + 54, cy + int(h * 0.28)
        ax1, ay1 = cx + int(w * 0.18), y0 + 54
        draw.line([(ax0, ay0), (ax1, ay0)], fill=(148, 163, 184), width=3)
        draw.line([(ax0, ay0), (ax0, ay1)], fill=(148, 163, 184), width=3)

        def f_curve(u):
            return 0.18 + 0.62 * (u ** 1.7)

        # 리만 적분 직사각형 (N이 t에 따라 점점 촘촘해짐)
        n_rects = 4 if t < 0.33 else (8 if t < 0.66 else 16)
        span_w = ax1 - ax0 - 40
        span_h = ay0 - ay1 - 30
        for ri in range(n_rects):
            u0 = ri / n_rects
            u1 = (ri + 1) / n_rects
            rx0 = ax0 + 20 + int(u0 * span_w)
            rx1 = ax0 + 20 + int(u1 * span_w)
            rh = int(f_curve((u0 + u1) / 2) * span_h)
            draw.rectangle((rx0, ay0 - rh, rx1 - 2, ay0), fill=(30, 58, 138), outline=(56, 189, 248), width=1)

        # 부드러운 함수 곡선 플롯
        pts = []
        for k in range(61):
            u = k / 60.0
            px = ax0 + 20 + int(u * span_w)
            py = ay0 - int(f_curve(u) * span_h)
            pts.append((px, py))
        draw.line(pts, fill=(52, 211, 153), width=5)

        # 할선 -> 접선 수렴 애니메이션 (Δx -> 0)
        u_a = 0.35
        u_b = max(u_a + 0.04, 0.88 - 0.50 * t)
        pa = (ax0 + 20 + int(u_a * span_w), ay0 - int(f_curve(u_a) * span_h))
        pb = (ax0 + 20 + int(u_b * span_w), ay0 - int(f_curve(u_b) * span_h))
        dx_s, dy_s = pb[0] - pa[0], pb[1] - pa[1]
        draw.line([(pa[0] - dx_s * 0.6, pa[1] - dy_s * 0.6), (pb[0] + dx_s * 0.6, pb[1] + dy_s * 0.6)], fill=(250, 204, 21), width=4)
        draw.ellipse((pa[0] - 8, pa[1] - 8, pa[0] + 8, pa[1] + 8), fill=(225, 29, 72), outline=(255, 255, 255), width=2)
        draw.ellipse((pb[0] - 8, pb[1] - 8, pb[0] + 8, pb[1] + 8), fill=(250, 204, 21), outline=(255, 255, 255), width=2)

        gx0 = x0 + int(w * 0.53)
        gy0 = y0 + 28
        draw.rounded_rectangle((gx0, gy0, x1 - 22, gy0 + 150), radius=16, fill=(15, 23, 42), outline=(251, 191, 36), width=2)
        draw.text((gx0 + 16, gy0 + 14), "▶ 극한(Δx→0) & 미적분 모니터", fill=(254, 240, 138), font=font_sm)
        draw.text((gx0 + 16, gy0 + 52), f"Δx 간격: {max(0.01, round(u_b - u_a, 2))}  →  접선 수렴!", fill=(250, 204, 21), font=font_lbl)
        draw.text((gx0 + 16, gy0 + 92), f"구분구적 분할: N = {n_rects}조각", fill=(56, 189, 248), font=font_lbl)

    else:
        # 원주각·중심각·다각형 대칭 불변량 & 보조선 반지름 동적 애니메이션
        R = int(min(w, h) * 0.33)
        draw.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(12, 22, 46), outline=(56, 189, 248), width=4)
        A = (cx - int(R * 0.78), cy + int(R * 0.62))
        B = (cx + int(R * 0.78), cy + int(R * 0.62))
        ang_p = (-0.75 + 0.55 * math.sin(t * math.pi)) * math.pi
        P = (cx + int(R * math.cos(ang_p)), cy + int(R * math.sin(ang_p)))

        # 중심 O와 연결한 보조선 반지름 (Act 3 이상에서 선명하게 강조)
        draw.line([(cx, cy), A], fill=(244, 63, 94), width=3)
        draw.line([(cx, cy), B], fill=(244, 63, 94), width=3)
        draw.line([(cx, cy), P], fill=(250, 204, 21), width=3)

        # 원주각 삼각형 PAB
        draw.polygon([P, A, B], outline=(52, 211, 153), width=4)
        draw.line([A, B], fill=(250, 204, 21), width=5)
        for pt in [A, B, P, (cx, cy)]:
            draw.ellipse((pt[0] - 7, pt[1] - 7, pt[0] + 7, pt[1] + 7), fill=(250, 204, 21), outline=(255, 255, 255), width=2)

        gx0 = x0 + int(w * 0.53)
        gy0 = y0 + 28
        draw.rounded_rectangle((gx0, gy0, x1 - 22, gy0 + 150), radius=16, fill=(15, 23, 42), outline=(251, 191, 36), width=2)
        draw.text((gx0 + 16, gy0 + 14), "[원리] 원과 대칭 불변량 레이더", fill=(254, 240, 138), font=font_sm)
        draw.text((gx0 + 16, gy0 + 52), "점 P 위치 이동 중... (동적 추적)", fill=(56, 189, 248), font=font_lbl)
        draw.text((gx0 + 16, gy0 + 92), "원주각 ∠APB = ½ ∠AOB (불변!)", fill=(52, 211, 153), font=font_lbl)

    # 3. 우측 하단: 원본 수학자료실 핵심 도형 블루프린트 PiP 참조 카드 (단순 페이지 넘김이 아닌 '핵심 착안 도형' 대조용)
    if doc and len(doc) > 0:
        pip_w = min(360, int(w * 0.32))
        pip_h = min(220, int(h * 0.42))
        px0 = x1 - pip_w - 22
        py0 = y1 - pip_h - 22
        ref_idx = min(len(doc) - 1, max(0, int((act_num - 1) / 4.0 * (len(doc) - 1))))
        crop_im = _extract_Inverted_blueprint_crop(doc, ref_idx, pip_w - 8, pip_h - 36)
        draw.rounded_rectangle((px0, py0, px0 + pip_w, py0 + pip_h), radius=14, fill=(15, 23, 42), outline=(56, 189, 248), width=2)
        pip_lbl = f"[도형] 핵심 착안 도형 (Core Idea #{act_num})" if lang_code == "ko" else f"[도형] Core Idea Blueprint #{act_num}"
        draw.text((px0 + 12, py0 + 6), pip_lbl, fill=(125, 211, 252), font=font_sm)
        canvas.paste(crop_im, (px0 + 4, py0 + 32))


def render_creative_idea_thumbnail(sdoc: dict, lang_code: str = "ko") -> Path:
    """Edition 5: 창의 아이디어 확장 시네마 전용 1280x720 다크 네온 블루프린트 썸네일을 생성합니다."""
    slug_key = sdoc["slug"]
    out_thumb = YT_PKG_DIR / f"{slug_key}_idea_{lang_code}_thumb.png"
    ko_t, en_t = vmaker.split_bilingual_title(sdoc.get("title", slug_key))
    clean_t = (
        vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(ko_t), max_len=24, lang="ko")
        if lang_code == "ko"
        else vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(en_t or sdoc.get("title_en") or ko_t), max_len=30, lang="en")
    )
    archetype = detect_visual_archetype(sdoc)

    pdf_bytes, _ = vmaker.load_or_build_topic_pdf_bytes(sdoc.get("pdf_url", ""), slug_key)
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")

    canvas = Image.new("RGB", (1280, 720), (6, 11, 25))
    draw = ImageDraw.Draw(canvas)

    # 우측 절차적 기하 스테이지 미리보기
    draw_procedural_math_stage(draw, canvas, archetype, 3, 0.78, (540, 36, 1248, 684), doc, lang_code=lang_code)

    # 좌측 강렬한 타이포그래피 후킹 패널
    draw.rounded_rectangle((28, 36, 522, 684), radius=26, fill=(15, 23, 42), outline=(250, 204, 21), width=4)
    draw.rounded_rectangle((52, 62, 496, 122), radius=16, fill=(124, 58, 237), outline=(254, 240, 138), width=2)
    f_badge = vmaker.get_font_for_lang(lang_code, 22, bold=True)
    f_hero = vmaker.get_font_for_lang(lang_code, 46, bold=True)
    f_sub = vmaker.get_font_for_lang(lang_code, 28, bold=True)

    b_txt = "★ 창의 아이디어 시네마 (Beyond PDF)" if lang_code == "ko" else "★ CREATIVE MATH CINEMA"
    draw.text((70, 76), b_txt, fill=(254, 240, 138), font=f_badge)

    hook_lines = (
        ["공식 암기 멈추세요!", "단 1개의 아이디어로", "끝내는 시각적 비밀!"]
        if lang_code == "ko"
        else ["STOP MEMORIZING!", "1 Core Visual Idea", "Explains It All!"]
    )
    for i, hl in enumerate(hook_lines):
        col = (250, 204, 21) if i == 1 else (255, 255, 255)
        draw.text((54, 155 + i * 68), hl, fill=col, font=f_hero)

    t_lines = textwrap.wrap(clean_t, width=14 if lang_code == "ko" else 20)[:2]
    for j, tl in enumerate(t_lines):
        draw.text((54, 395 + j * 42), tl, fill=(125, 211, 252), font=f_sub)

    draw.rounded_rectangle((52, 588, 496, 654), radius=16, fill=(225, 29, 72))
    draw.text(
        (72, 606),
        "▶ 5막 스토리텔링 · @min7014_ai" if lang_code == "ko" else "▶ 5-Act Visual Story · @min7014_ai",
        fill=(255, 255, 255),
        font=f_badge,
    )
    canvas.save(out_thumb)
    return out_thumb


def render_creative_idea_cinema_video(slug_key: str = "math20250130001", lang_code: str = "ko") -> Path:
    """
    [Edition 5-A: ★ 1080p 16:9 창의 아이디어 확장 시네마 본편 제작기]
    - PDF 페이지를 한 장씩 넘기는 대신, 5막 스토리텔링과 3Blue1Brown 스타일 절차적 동적 벡터 애니메이션으로
      주제의 핵심 아이디어와 조건 변형(What-If-Not), 실전 통찰을 시각화합니다.
    """
    script_path = SCRIPTS_DIR / f"{slug_key}.json"
    if not script_path.exists():
        vmaker.generate_or_update_script(slug_key, target_langs=["ko", "en"])
    sdoc = json.loads(script_path.read_text(encoding="utf-8"))

    acts = build_creative_idea_acts(sdoc, lang_code=lang_code)
    archetype = detect_visual_archetype(sdoc)
    pdf_bytes, _ = vmaker.load_or_build_topic_pdf_bytes(sdoc.get("pdf_url", ""), slug_key)
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")

    voice_name = vmaker.GLOBAL_VOICE_MAP.get(lang_code, vmaker.GLOBAL_VOICE_MAP["en"])["voice"]
    ffmpeg_exe = shutil.which("ffmpeg")
    ffprobe_exe = shutil.which("ffprobe")

    tmp_dir = Path(tempfile.mkdtemp(prefix=f"min7014_idea_{slug_key}_{lang_code}_"))
    segs = []

    f_badge = vmaker.get_font_for_lang(lang_code, 24, bold=True)
    f_head = vmaker.get_font_for_lang(lang_code, 34, bold=True)
    f_formula = vmaker.get_font_for_lang(lang_code, 26, bold=True)
    f_bul = vmaker.get_font_for_lang(lang_code, 22, bold=True)
    f_sub = vmaker.get_font_for_lang(lang_code, 27, bold=True)

    ko_t, en_t = vmaker.split_bilingual_title(sdoc.get("title", slug_key))
    clean_title = (
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

            num_frames = 14
            per_f_dur = dur_s / num_frames
            f_lines = []
            last_fp = None
            cap_lines = textwrap.wrap(narr, width=48 if lang_code == "ko" else 74)[:3]

            for fi in range(num_frames):
                t = fi / max(1, num_frames - 1)
                canvas = Image.new("RGB", (1920, 1080), (6, 10, 22))
                draw = ImageDraw.Draw(canvas)

                # 상단 헤더 바
                draw.rounded_rectangle((32, 22, 1888, 132), radius=20, fill=(15, 23, 42), outline=(124, 58, 237), width=3)
                draw.rounded_rectangle((52, 38, 520, 82), radius=12, fill=(124, 58, 237))
                draw.text((68, 46), act_info["badge"], fill=(254, 240, 138), font=f_badge)

                # 우측 상단 구독 유도 배지
                draw.rounded_rectangle((1560, 38, 1864, 84), radius=14, fill=(225, 29, 72), outline=(254, 240, 138), width=2)
                draw.text(
                    (1582, 48),
                    "▶ 구독 @min7014_ai" if lang_code == "ko" else "▶ SUBSCRIBE @min7014_ai",
                    fill=(255, 255, 255),
                    font=f_badge,
                )
                draw.text((540, 44), act_info["headline"][:46], fill=(255, 255, 255), font=f_head)

                # 연속 진행 게이지
                overall_p = ((act_num - 1) + (fi + 1) / num_frames) / len(acts)
                draw.rounded_rectangle((52, 102, 1864, 116), radius=6, fill=(30, 41, 59))
                draw.rounded_rectangle((52, 102, 52 + max(24, int(1812 * overall_p)), 116), radius=6, fill=(250, 204, 21))

                # 좌측 중앙: 3Blue1Brown 스타일 절차적 동적 벡터 스테이지 (x=32..1230, y=148..856)
                draw_procedural_math_stage(
                    draw, canvas, archetype, act_num, t, (32, 148, 1230, 856), doc, lang_code=lang_code
                )

                # 우측 중앙: 핵심 아이디어 수식 & 3단계 사고 노트 패널 (x=1248..1888, y=148..856)
                draw.rounded_rectangle((1248, 148, 1888, 856), radius=24, fill=(13, 21, 38), outline=(250, 204, 21), width=3)
                draw.rounded_rectangle((1272, 174, 1864, 258), radius=16, fill=(30, 58, 138), outline=(56, 189, 248), width=2)
                draw.text((1292, 186), "★ CORE IDEA & INVARIANT", fill=(125, 211, 252), font=f_bul)
                draw.text((1292, 218), act_info["key_formula"][:34], fill=(254, 240, 138), font=f_formula)

                for bi, b_txt in enumerate(act_info["bullets"][:3]):
                    by0 = 286 + bi * 176
                    is_active_b = (fi >= int(bi * (num_frames / 3)))
                    b_fill = (30, 41, 59) if is_active_b else (15, 23, 42)
                    b_out = (52, 211, 153) if is_active_b else (51, 65, 85)
                    draw.rounded_rectangle((1272, by0, 1864, by0 + 154), radius=16, fill=b_fill, outline=b_out, width=2)
                    b_wrapped = textwrap.wrap(b_txt, width=24 if lang_code == "ko" else 34)[:3]
                    for wl_i, wl in enumerate(b_wrapped):
                        draw.text((1294, by0 + 20 + wl_i * 40), wl, fill=(255, 255, 255) if is_active_b else (148, 163, 184), font=f_bul)

                # 하단 키네틱 자막 바 (y=874..1056)
                draw.rounded_rectangle((32, 874, 1888, 1056), radius=20, fill=(15, 23, 42), outline=(56, 189, 248), width=3)
                active_ci = min(len(cap_lines) - 1, int(t * len(cap_lines))) if cap_lines else 0
                for ci, cl in enumerate(cap_lines):
                    c_col = (254, 240, 138) if ci == active_ci else (203, 213, 225)
                    draw.text((64, 896 + ci * 48), cl, fill=c_col, font=f_sub)

                fp = tmp_dir / f"idea_a{act_num:02d}_f{fi:02d}.png"
                canvas.save(fp)
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
                "-c:v", "libx264", "-profile:v", "high", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30",
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

        try:
            vmaker.queue_and_delete_existing_youtube_videos_for_slug(
                slug_key, editions=("idea_cinema",), langs=(lang_code,), execute_delete_now=True
            )
            sdoc = json.loads(script_path.read_text(encoding="utf-8"))
        except Exception:
            pass

        idea_title = (
            f"★ [창의 수학 시네마] {clean_title} — 공식 암기 없이 단 1개의 아이디어로 깨치는 비밀! | @min7014_ai"
            if lang_code == "ko"
            else f"★ [Creative Math Cinema] {clean_title} — The 1 Visual Idea That Explains It All! | @min7014_ai"
        )[:98]

        sdoc.setdefault("creative_idea_packages", {})[lang_code] = {
            "title": idea_title,
            "local_mp4_path": f"video_lectures/creative_idea/{slug_key}_idea_{lang_code}.mp4",
            "thumbnail_path": f"video_lectures/youtube_packages/{thumb_path.name}",
            "duration_sec": round(dur, 2),
            "edition_mode": "5-Act Creative Idea Storytelling & Procedural Vector Animation (Beyond PDF)",
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "needs_youtube_upload": True,
        }
        sdoc.setdefault("creative_idea_youtube_urls", {"ko": "", "en": ""})
        script_path.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
        vmaker.update_video_catalog()
        print(f"★▶ [Edition 5-A: Creative Idea 1080p Cinema Generated] {out_mp4} ({round(dur, 1)}s)")
        return out_mp4
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def render_creative_idea_short_vertical(slug_key: str = "math20250130001", lang_code: str = "ko") -> Path:
    """
    [Edition 5-B: ★ 9:16 (1080x1920) 창의 아이디어 숏폼 (Idea-#Shorts, 38~46초) 제작기]
    - PDF 페이지를 넘기는 대신 다크 블루프린트 절차적 애니메이션으로
      ① 직관 역설 훅 → ② 라이브 숫자·도형 실험 → ③ 단 한 줄 보조선 아이디어 → ④ 조건 변형 확장을 44초 안에 압축합니다.
    """
    script_path = SCRIPTS_DIR / f"{slug_key}.json"
    if not script_path.exists():
        vmaker.generate_or_update_script(slug_key, target_langs=["ko", "en"])
    sdoc = json.loads(script_path.read_text(encoding="utf-8"))

    acts = build_creative_idea_acts(sdoc, lang_code=lang_code)[:4]
    archetype = detect_visual_archetype(sdoc)
    pdf_bytes, _ = vmaker.load_or_build_topic_pdf_bytes(sdoc.get("pdf_url", ""), slug_key)
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")

    voice_name = vmaker.GLOBAL_VOICE_MAP.get(lang_code, vmaker.GLOBAL_VOICE_MAP["en"])["voice"]
    ffmpeg_exe = shutil.which("ffmpeg")
    ffprobe_exe = shutil.which("ffprobe")

    pub_short_dir = ROOT_DIR / "video_lectures" / "shorts"
    pub_short_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir = Path(tempfile.mkdtemp(prefix=f"min7014_ideashort_{slug_key}_{lang_code}_"))
    segs = []

    f_top = vmaker.get_font_for_lang(lang_code, 40, bold=True)
    f_sub = vmaker.get_font_for_lang(lang_code, 26, bold=True)
    f_cap = vmaker.get_font_for_lang(lang_code, 32, bold=True)

    ko_t, en_t = vmaker.split_bilingual_title(sdoc.get("title", slug_key))
    clean_title = (
        vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(ko_t), max_len=30, lang="ko")
        if lang_code == "ko"
        else vmaker._smart_concise_topic_title(vmaker.latex_to_unicode_title(en_t or sdoc.get("title_en") or ko_t), max_len=38, lang="en")
    )

    try:
        for idx, act_info in enumerate(acts, 1):
            # 숏폼용 초압축 2문장 대본
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

            num_frames = 8
            per_f_dur = seg_dur / num_frames
            f_lines = []
            last_fp = None
            cap_lines = textwrap.wrap(short_narr, width=22 if lang_code == "ko" else 34)[:5]

            for fi in range(num_frames):
                t = fi / max(1, num_frames - 1)
                canvas = Image.new("RGB", (1080, 1920), (6, 10, 22))
                draw = ImageDraw.Draw(canvas)

                # 상단 헤더
                draw.rounded_rectangle((40, 56, 1040, 286), radius=26, fill=(15, 23, 42), outline=(124, 58, 237), width=3)
                draw.rounded_rectangle((68, 76, 680, 126), radius=16, fill=(124, 58, 237))
                draw.text((86, 85), act_info["badge"][:30], fill=(254, 240, 138), font=f_sub)
                draw.text((830, 85), f"IDEA {idx}/{len(acts)}", fill=(250, 204, 21), font=f_sub)

                t_lines = textwrap.wrap(clean_title, width=20 if lang_code == "ko" else 28)[:2]
                for li, tl in enumerate(t_lines):
                    draw.text((72, 142 + li * 50), tl, fill=(255, 255, 255), font=f_top)

                overall_p = ((idx - 1) + (fi + 1) / num_frames) / len(acts)
                draw.rounded_rectangle((68, 254, 1012, 268), radius=6, fill=(30, 41, 59))
                draw.rounded_rectangle((68, 254, 68 + max(24, int(944 * overall_p)), 268), radius=6, fill=(250, 204, 21))

                # 중앙 절차적 벡터 애니메이션 스테이지 (y=310..1310)
                draw_procedural_math_stage(
                    draw, canvas, archetype, act_info["act"], t, (40, 310, 1040, 1310), doc, lang_code=lang_code
                )

                # 하단 자막 카드 & 구독 유도 배지 (y=1335..1795)
                draw.rounded_rectangle((40, 1335, 1040, 1795), radius=26, fill=(15, 23, 42), outline=(250, 204, 21), width=3)
                draw.text((70, 1362), act_info["key_formula"][:34], fill=(56, 189, 248), font=f_sub)
                draw.rounded_rectangle((748, 1352, 1016, 1404), radius=16, fill=(225, 29, 72), outline=(254, 240, 138), width=2)
                draw.text(
                    (768, 1363),
                    "▶ 구독 @min7014_ai" if lang_code == "ko" else "▶ SUBSCRIBE",
                    fill=(255, 255, 255),
                    font=vmaker.get_font_for_lang("ko", 22, bold=True),
                )

                active_ci = min(len(cap_lines) - 1, int(t * len(cap_lines))) if cap_lines else 0
                for ci, cl in enumerate(cap_lines):
                    c_col = (254, 240, 138) if ci == active_ci else (203, 213, 225)
                    draw.text((72, 1432 + ci * 60), cl, fill=c_col, font=f_cap)

                draw.rounded_rectangle((40, 1810, 1040, 1892), radius=20, fill=(88, 28, 135), outline=(250, 204, 21), width=3)
                cta_txt = (
                    "▶ [구독] 누르고 매일 창의 수학 아이디어 받기! → 고정댓글에 1080p 본편"
                    if lang_code == "ko"
                    else "▶ Tap [SUBSCRIBE] for Daily Math Ideas! → Full 1080p in Pinned Comment"
                )
                draw.text((64, 1834), cta_txt, fill=(254, 240, 138), font=vmaker.get_font_for_lang("ko", 23, bold=True))

                fp = tmp_dir / f"ishort_{idx:02d}_f{fi:02d}.png"
                canvas.save(fp)
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
                "-c:v", "libx264", "-profile:v", "high", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30",
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
            f"★ [창의 아이디어 #Shorts] {clean_title} — 공식 없이 깨치는 단 하나의 원리! | @min7014_ai"
            if lang_code == "ko"
            else f"★ [Creative Math Idea #Shorts] {clean_title} — 1 Visual Idea Explains All! | @min7014_ai"
        )[:98]

        sdoc = json.loads(script_path.read_text(encoding="utf-8"))
        sdoc.setdefault("creative_idea_shorts_packages", {})[lang_code] = {
            "title": ishort_title,
            "local_mp4_path": f"video_lectures/shorts/{slug_key}_short_idea_{lang_code}.mp4",
            "duration_sec": round(dur, 2),
            "aspect_ratio": "9:16 (1080x1920)",
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "needs_youtube_upload": True,
        }
        sdoc.setdefault("creative_idea_shorts_urls", {"ko": "", "en": ""})
        script_path.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
        vmaker.update_video_catalog()
        print(f"★ [Edition 5-B: Creative Idea YouTube Shorts (<58s) Generated] {out_short} ({round(dur, 1)}s)")
        return out_short
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def upload_creative_idea_to_youtube(slug_key: str, langs=("ko",), privacy="public", replace_existing=False) -> dict:
    """Edition 5-A (1080p 창의 아이디어 시네마 본편)를 @min7014_ai 채널에 업로드하고 텔레그램으로 알립니다."""
    from googleapiclient.http import MediaFileUpload

    script_path = SCRIPTS_DIR / f"{slug_key}.json"
    if not script_path.exists():
        vmaker.generate_or_update_script(slug_key)
    sdoc = json.loads(script_path.read_text(encoding="utf-8"))

    uploaded = {}
    missing = []
    for lc in langs:
        u = (sdoc.get("creative_idea_youtube_urls") or {}).get(lc, "").strip()
        if u and not replace_existing:
            uploaded[lc] = u
        else:
            missing.append(lc)
    if not missing:
        return uploaded

    youtube, active_token_path = vmaker.get_available_youtube_upload_service()
    if youtube is None:
        return uploaded

    for lc in missing:
        mp4_p = CREATIVE_IDEA_DIR / f"{slug_key}_idea_{lc}.mp4"
        if not mp4_p.exists():
            render_creative_idea_cinema_video(slug_key, lang_code=lc)
        sdoc = json.loads(script_path.read_text(encoding="utf-8"))
        pkg = (sdoc.get("creative_idea_packages") or {}).get(lc) or {}
        v_title = pkg.get("title") or f"★ [창의 수학 시네마] {slug_key} | @min7014_ai"
        sub_link = "https://www.youtube.com/@min7014_ai?sub_confirmation=1"
        board_link = f"https://min7014.github.io/mathedu/video_board.html?slug={slug_key}&mode=idea"
        std_yt = (sdoc.get("youtube_urls") or {}).get(lc) or "https://www.youtube.com/@min7014_ai"

        v_desc = (
            f"★ [창의 아이디어 수학 시네마 (Beyond PDF · 5-Act Storytelling Edition)] [ID: {slug_key}_IDEA_{lc.upper()}]\n\n"
            f"단순히 교재를 한 페이지씩 넘기며 공식을 암기하는 방식을 넘어, 단 하나의 핵심 수학적 아이디어와 동적 시뮬레이션으로 원리를 깨치는 창의 수학 시네마입니다!\n"
            f"• ACT 1: 직관을 깨는 수학 미스터리 & 출발 질문\n"
            f"• ACT 2: 공식 없이 눈으로 확인하는 라이브 수치·도형 실험실\n"
            f"• ACT 3: 천재들의 단 한 줄 보조선과 불변량 탄생\n"
            f"• ACT 4: 만약 조건을 바꾼다면? (What-If-Not 일반화 확장)\n"
            f"• ACT 5: 수능·경시 킬러 10초 통찰 & 유레카 정리\n\n"
            f"▶ [@min7014_ai 1초 무료 구독하기]: {sub_link}\n"
            f"📄 [원본 PDF 단계별 증명 영상 보기]: {std_yt}\n"
            f"[도형] [무료 GeoGebra 직접 조작 & 창의 수학 실험실]: {board_link}\n"
            f"#창의수학 #시각적증명 #수학아이디어 #기하학 #수능수학 #mathedu"
        )
        body = {
            "snippet": {
                "title": vmaker._balance_parentheses(v_title),
                "description": v_desc,
                "tags": ["창의수학", "수학아이디어", "시각적증명", "3Blue1Brown스타일", "기하학", "수능수학", "mathedu", slug_key],
                "categoryId": "27",
                "defaultLanguage": lc,
                "defaultAudioLanguage": lc,
            },
            "status": {"privacyStatus": privacy, "selfDeclaredMadeForKids": False},
        }
        try:
            media = MediaFileUpload(str(mp4_p), chunksize=-1, resumable=True, mimetype="video/mp4")
            resp = youtube.videos().insert(part="snippet,status", body=body, media_body=media).execute()
            vid_id = resp["id"]
            yt_u = f"https://youtu.be/{vid_id}"
            uploaded[lc] = yt_u

            thumb_p = YT_PKG_DIR / f"{slug_key}_idea_{lc}_thumb.png"
            if thumb_p.exists():
                try:
                    youtube.thumbnails().set(
                        videoId=vid_id,
                        media_body=MediaFileUpload(str(thumb_p), mimetype="image/png", resumable=False),
                    ).execute()
                except Exception:
                    pass

            sdoc = json.loads(script_path.read_text(encoding="utf-8"))
            sdoc.setdefault("creative_idea_youtube_urls", {"ko": "", "en": ""})[lc] = yt_u
            if isinstance((sdoc.get("creative_idea_packages") or {}).get(lc), dict):
                sdoc["creative_idea_packages"][lc]["needs_youtube_upload"] = False
                sdoc["creative_idea_packages"][lc]["uploaded_video_id"] = vid_id
            script_path.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
            vmaker.update_video_catalog()
            vmaker.notify_telegram_youtube_upload(
                slug_key=slug_key,
                edition_label=f"★ 1080p 창의 아이디어 시네마 본편 ({lc.upper()})",
                video_title=v_title,
                youtube_url=yt_u,
            )
            try:
                c_txt = (
                    f"★ [창의 아이디어 퀴즈] 오늘 5막 시네마에서 가장 인상 깊었던 장면(Act 1~5)이나 조건 변형 아이디어는 무엇이었나요? 댓글로 남겨주세요!\n\n"
                    f"▶ 공식 암기 없는 창의 수학 시네마! @min7014_ai 1초 무료 구독하기:\n👉 {sub_link}\n"
                    f"[도형] 직접 움직여보는 무료 GeoGebra 실험실: {board_link}"
                )
                youtube.commentThreads().insert(
                    part="snippet",
                    body={"snippet": {"videoId": vid_id, "topLevelComment": {"snippet": {"textOriginal": c_txt}}}},
                ).execute()
            except Exception:
                pass
        except Exception as e:
            err_s = str(e)
            if "quotaExceeded" in err_s or "rateLimitExceeded" in err_s or "uploadLimitExceeded" in err_s:
                vmaker.mark_token_quota_exhausted(active_token_path, 900)
            break
    return uploaded


def upload_creative_idea_short_to_youtube(slug_key: str, langs=("ko",), privacy="public", replace_existing=False) -> dict:
    """Edition 5-B (9:16 창의 아이디어 숏폼 Idea-#Shorts)를 @min7014_ai 채널에 업로드하고 텔레그램으로 알립니다."""
    from googleapiclient.http import MediaFileUpload

    script_path = SCRIPTS_DIR / f"{slug_key}.json"
    if not script_path.exists():
        vmaker.generate_or_update_script(slug_key)
    sdoc = json.loads(script_path.read_text(encoding="utf-8"))

    uploaded = {}
    missing = []
    for lc in langs:
        u = (sdoc.get("creative_idea_shorts_urls") or {}).get(lc, "").strip()
        if u and not replace_existing:
            uploaded[lc] = u
        else:
            missing.append(lc)
    if not missing:
        return uploaded

    youtube, active_token_path = vmaker.get_available_youtube_upload_service()
    if youtube is None:
        return uploaded

    for lc in missing:
        mp4_p = ROOT_DIR / "video_lectures" / "shorts" / f"{slug_key}_short_idea_{lc}.mp4"
        if not mp4_p.exists():
            render_creative_idea_short_vertical(slug_key, lang_code=lc)
        sdoc = json.loads(script_path.read_text(encoding="utf-8"))
        pkg = (sdoc.get("creative_idea_shorts_packages") or {}).get(lc) or {}
        v_title = pkg.get("title") or f"★ [창의 아이디어 #Shorts] {slug_key} | @min7014_ai"
        sub_link = "https://www.youtube.com/@min7014_ai?sub_confirmation=1"
        board_link = f"https://min7014.github.io/mathedu/video_board.html?slug={slug_key}&mode=idea"
        idea_yt = (sdoc.get("creative_idea_youtube_urls") or {}).get(lc) or (sdoc.get("youtube_urls") or {}).get(lc) or "https://www.youtube.com/@min7014_ai"

        v_desc = (
            f"★ [창의 아이디어 숏폼 (Beyond PDF · Procedural Math #Shorts)] [ID: {slug_key}_SHORT_IDEA_{lc.upper()}]\n\n"
            f"교재를 한 장씩 넘기는 대신, 단 하나의 핵심 수학적 아이디어와 실시간 수치·도형 시뮬레이션으로 깨치는 45초 창의 수학 #Shorts!\n"
            f"▶ [@min7014_ai 1초 무료 구독하기]: {sub_link}\n"
            f"★ [1080p 창의 수학 시네마 5막 풀버전]: {idea_yt}\n"
            f"[도형] [무료 GeoGebra 직접 조작 & 창의 수학 실험실]: {board_link}\n"
            f"#Shorts #창의수학 #시각적증명 #수학아이디어 #기하학 #mathedu"
        )
        body = {
            "snippet": {
                "title": v_title,
                "description": v_desc,
                "tags": ["Shorts", "창의수학", "수학아이디어", "시각적증명", "기하학", "mathedu", slug_key],
                "categoryId": "27",
                "defaultLanguage": lc,
                "defaultAudioLanguage": lc,
            },
            "status": {"privacyStatus": privacy, "selfDeclaredMadeForKids": False},
        }
        try:
            media = MediaFileUpload(str(mp4_p), chunksize=-1, resumable=True, mimetype="video/mp4")
            resp = youtube.videos().insert(part="snippet,status", body=body, media_body=media).execute()
            vid_id = resp["id"]
            yt_u = f"https://youtube.com/shorts/{vid_id}"
            uploaded[lc] = yt_u

            sdoc = json.loads(script_path.read_text(encoding="utf-8"))
            sdoc.setdefault("creative_idea_shorts_urls", {"ko": "", "en": ""})[lc] = yt_u
            if isinstance((sdoc.get("creative_idea_shorts_packages") or {}).get(lc), dict):
                sdoc["creative_idea_shorts_packages"][lc]["needs_youtube_upload"] = False
                sdoc["creative_idea_shorts_packages"][lc]["uploaded_video_id"] = vid_id
            script_path.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
            vmaker.update_video_catalog()
            vmaker.notify_telegram_youtube_upload(
                slug_key=slug_key,
                edition_label=f"★ 9:16 창의 아이디어 숏폼 Idea-#Shorts ({lc.upper()})",
                video_title=v_title,
                youtube_url=yt_u,
            )
            try:
                c_txt = (
                    f"★ [창의 아이디어 10초 퀴즈] 만약 이 도형에서 조건을 살짝 바꾼다면(What-If-Not) 어떤 일이 벌어질까요?\n\n"
                    f"▶ 공식 암기 없는 창의 수학! @min7014_ai 1초 무료 구독하기:\n👉 {sub_link}\n"
                    f"▶ 1080p 창의 수학 시네마 풀버전 보기:\n👉 {idea_yt}\n"
                    f"[도형] 무료 GeoGebra 실험실: {board_link}"
                )
                youtube.commentThreads().insert(
                    part="snippet",
                    body={"snippet": {"videoId": vid_id, "topLevelComment": {"snippet": {"textOriginal": c_txt}}}},
                ).execute()
            except Exception:
                pass
        except Exception as e:
            err_s = str(e)
            if "quotaExceeded" in err_s or "rateLimitExceeded" in err_s or "uploadLimitExceeded" in err_s:
                vmaker.mark_token_quota_exhausted(active_token_path, 900)
            break
    return uploaded


def build_flagship_creative_idea_suite(slug_key: str = "math20250130001", langs=("ko", "en"), upload: bool = False):
    """특정 주제에 대해 Edition 5-A(1080p 본편) 및 Edition 5-B(9:16 숏폼)를 일괄 생성하고 선택적으로 업로드합니다."""
    results = {"slug": slug_key, "cinema_1080p": {}, "shorts_916": {}}
    for lc in langs:
        p1080 = render_creative_idea_cinema_video(slug_key, lang_code=lc)
        p916 = render_creative_idea_short_vertical(slug_key, lang_code=lc)
        results["cinema_1080p"][lc] = str(p1080)
        results["shorts_916"][lc] = str(p916)
    if upload:
        upload_creative_idea_to_youtube(slug_key, langs=langs)
        upload_creative_idea_short_to_youtube(slug_key, langs=langs)
    return results


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Edition 5: Creative Idea & Storytelling Math Cinema (Beyond PDF)")
    ap.add_argument("--slug", default="math20250130001")
    ap.add_argument("--langs", default="ko,en")
    ap.add_argument("--upload", action="store_true")
    args = ap.parse_args()
    l_list = [x.strip() for x in args.langs.split(",") if x.strip()]
    build_flagship_creative_idea_suite(args.slug, langs=tuple(l_list), upload=args.upload)
