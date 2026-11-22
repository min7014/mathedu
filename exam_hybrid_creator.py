import silent_subprocess  # noqa: F401 — Rule 48 windowless enforcement
import json
import math
import re
import shutil
import subprocess
import tempfile
import textwrap
from datetime import datetime
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw

ROOT_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = ROOT_DIR / "video_lectures" / "scripts"
EXAM_HYBRID_DIR = ROOT_DIR / "youtube_uploads" / "exam_hybrid"
EXAM_HYBRID_DIR.mkdir(parents=True, exist_ok=True)

# ==============================================================================
# [Strategy 4 · Rule 49 & Rule 51] 100% 자체 창작 수치 문제 → min7014 보조선 1줄 5초 해체 블루프린트
# - 저작권·상표권 100% 무결성 보장: 외부 기관 상표(SAT, AP, AMC, IB, Olympiad 등) 및 타 저작물 문항 복제 ZERO!
# - Act 1 수치 예제와 도형은 100% 자체 창작이며, Act 2 시각 증명은 100% 자체 보유 IP(https://min7014.github.io/)입니다.
# ==============================================================================
EXAM_TRAP_BLUEPRINTS = [
    {
        "slug": "2012093001",
        "diagram_kind": "circle_inscribed",
        "exam_badge_ko": "◆ 기하의 불변량 · 원주각과 중심각",
        "exam_badge_en": "◆ Circle Invariant · Inscribed Angle",
        "thumb_hook_ko": ["왜 식 없이 보일까?", "보조선 한 줄의 통찰"],
        "thumb_hook_en": ["WHY NO ALGEBRA?", "ONE HIDDEN LINE"],
        "problem_label_ko": "중심각 ∠AOB = 84°일 때, 원 위를 움직이는 점 P에 대하여 x = ∠APB는?",
        "problem_label_en": "Given central angle ∠AOB = 84°, find x = ∠APB for point P on the circle!",
        "figure_caption_ko": "∠AOB = 84°,  ∠APB = x = ?",
        "figure_caption_en": "∠AOB = 84°,  ∠APB = x = ?",
        "answer_label_ko": "지름 보조선 PO 한 줄 → 이등변삼각형 2개!  x = 84° ÷ 2 = 42°",
        "answer_label_en": "1 Diameter Line PO → Two Isosceles Triangles!  x = 84° ÷ 2 = 42°",
        "title_ko": "✨ 왜 방정식 없이 풀릴까? 원주각을 단번에 여는 보조선 한 줄의 통찰 | 원주각과 중심각 시각적 증명",
        "title_en": "✨ Why One Hidden Diameter Replaces Algebra | Inscribed Angle Visual Proof",
        "short_title_ko": "❓ 중심각 84°일 때 원주각 x는? 지름 보조선 한 줄의 통찰! #Shorts",
        "short_title_en": "❓ Central Angle 84°—See Why One Diameter Reveals Angle x! #Shorts",
        "act1_ko": "잠깐! 중심각이 84도일 때 비스듬히 꺾인 원주각 x를 복잡한 연립방정식으로 푸는 대신, 지름 보조선 딱 한 줄로 그 이유가 한눈에 보이시나요?",
        "act1_en": "Wait! Instead of setting up tedious algebra for angle x when the central angle is 84 degrees, can you see why a single diameter reveals x visually?",
        "act3_ko": "이제 원래 문제로 돌아와 볼까요? 점 P와 중심 O를 잇는 지름 보조선 한 줄이면 두 이등변삼각형의 외각이 되어 x는 84도의 절반, 정답 42도가 명쾌하게 드러납니다! 공식 암기 대신 눈으로 원리를 꿰뚫는 시각적 증명, 지금 바로 채널 구독을 눌러 다음 기하 통찰도 함께해 보세요!",
        "act3_en": "Now back to our geometry problem! Drawing the single diameter through P and O splits angle x into two isosceles exterior halves—so x is half of 84, or 42 degrees directly! Subscribe right now to explore daily visual math insights!",
        "comment_quiz_ko": "🧩 [시각 암산 퀴즈] 만약 중심각 ∠AOB = 116°라면 원주각 x는 몇 도일까요? 암산한 정답을 댓글로 남겨보세요! 👇",
        "comment_quiz_en": "🧩 [Visual Check] If central angle ∠AOB = 116°, what is inscribed angle x? Drop your answer in the comments! 👇",
    },
    {
        "slug": "2012100304",
        "diagram_kind": "tangent_chord",
        "exam_badge_ko": "◆ 원과 접선의 대칭 · 접현각의 원리",
        "exam_badge_en": "◆ Circle & Tangent Symmetry Proof",
        "thumb_hook_ko": ["왜 식 없이 보일까?", "보조선 한 줄의 통찰"],
        "thumb_hook_en": ["WHY NO ALGEBRA?", "ONE HIDDEN LINE"],
        "problem_label_ko": "접선 AT와 현 AB가 이루는 각이 58°일 때, 원주 위 ∠ACB = x는?",
        "problem_label_en": "Tangent AT and chord AB form 58°. Find inscribed angle ∠ACB = x!",
        "figure_caption_ko": "접선각 ∠BAT = 58°,  ∠ACB = x = ?",
        "figure_caption_en": "Tangent ∠BAT = 58°,  ∠ACB = x = ?",
        "answer_label_ko": "지름 보조선 AD 한 줄 → 90° 직각 대칭!  x = 58° 그대로 일치!",
        "answer_label_en": "1 Diameter Line AD → Right-Angle Match!  x = 58° Instantly!",
        "title_ko": "✨ 접선과 현이 만날 때 숨은 대칭! 지름 보조선 한 줄의 증명 | 접현각의 정리(예각) 시각적 증명",
        "title_en": "✨ Hidden Symmetry of Tangent & Chord—Proved by One Diameter! | Alternate Segment Visual Proof",
        "short_title_ko": "❓ 예각 접선이 58°일 때 호 반대편 각 x는? 지름 보조선 한 줄의 통찰! #Shorts",
        "short_title_en": "❓ Acute Tangent Is 58°—Spot Angle x Across the Circle Visually! #Shorts",
        "act1_ko": "원과 접선이 만나 이루는 각이 58도일 때, 멀리 떨어진 원주 위의 각 x는 몇 도일까요? 공식을 외우지 않아도 지름 보조선 딱 한 줄이면 원리가 투명하게 보입니다!",
        "act1_en": "When a tangent and chord meet at 58 degrees, what is angle x across the circle? Even without memorizing formulas, one diameter line makes the symmetry clear!",
        "act3_ko": "접점을 지나는 지름 보조선 한 줄을 그으면 직각 90도에서 같은 여각을 빼 주므로, 복잡해 보이는 원과 접선 문제에서도 x는 58도와 정확히 일치합니다! 도형의 본질을 눈으로 읽는 시각적 증명, 지금 바로 구독 버튼을 눌러 두세요!",
        "act3_en": "Drawing that diameter line in this circle-tangent configuration subtracts the exact same complement from 90 degrees—so x equals 58 degrees at once! Hit Subscribe to build lasting geometric intuition!",
        "comment_quiz_ko": "🧩 [시각 암산 퀴즈] 접선과 현이 이루는 각이 67°라면 호 반대편 원주각 x는 몇 도일까요? 댓글로 남겨보세요! 👇",
        "comment_quiz_en": "🧩 [Visual Check] If the tangent-chord angle is 67°, what is angle x across the chord? Comment below! 👇",
    },
    {
        "slug": "2017090101",
        "diagram_kind": "pythagoras_squares",
        "exam_badge_ko": "◆ 유클리드 넓이 보존 · 직각삼각형",
        "exam_badge_en": "◆ Pythagorean Area Invariance",
        "thumb_hook_ko": ["수식은 내려놓고,", "도형의 눈을 뜨다"],
        "thumb_hook_en": ["BEYOND FORMULAS,", "SEE THE SYMMETRY"],
        "problem_label_ko": "직각삼각형 두 변 위 정사각형 넓이가 9와 16일 때, 빗변 정사각형 넓이 x는?",
        "problem_label_en": "Two leg squares have areas 9 and 16. Find hypotenuse square area x!",
        "figure_caption_ko": "넓이 S₁ = 9, S₂ = 16  →  빗변 정사각형 S₃ = x = ?",
        "figure_caption_en": "Areas S₁ = 9, S₂ = 16  →  Hypotenuse Square x = ?",
        "answer_label_ko": "제곱근 계산 없이! 합동 직각삼각형 4개 넓이 보존(c²=a²+b²) → x = 9 + 16 = 25!",
        "answer_label_en": "Zero Square Roots! Four-Triangle Square Proof (c²=a²+b²) → x = 9 + 16 = 25!",
        "title_ko": "✨ 제곱근 계산 없이 한눈에 보인다! 넓이 보존으로 읽는 빗변 정사각형 | 피타고라스 정리 시각적 증명",
        "title_en": "✨ Zero Square Roots Needed—See Area Conservation Directly! | Pythagorean Theorem Visual Proof",
        "short_title_ko": "❓ 제곱근 없이 넓이 x가 한눈에 보이시나요? 피타고라스 넓이 보존 원리! #Shorts",
        "short_title_en": "❓ Can You Spot Area x Without Square Roots? Pure Visual Proof! #Shorts",
        "act1_ko": "잠깐! 직각삼각형에서 변의 길이를 제곱근으로 구한 뒤 다시 제곱할 필요가 있을까요? 큰 정사각형의 넓이 보존 원리를 알면 계산 없이 그림만으로 투명하게 보입니다!",
        "act1_en": "Wait! Why compute irrational side lengths only to square them back? With four-triangle area conservation, area x reveals itself directly without square roots!",
        "act3_ko": "큰 정사각형 테두리에서 합동인 직각삼각형 네 개를 덜어내면 두 작은 정사각형 넓이 9와 16의 합이 곧 빗변 정사각형 넓이가 되므로 x는 9 더하기 16, 정답 25입니다! 공식 너머의 깊은 직관, 지금 바로 구독하고 매일 만나보세요!",
        "act3_en": "Removing four congruent right triangles around the border leaves c squared equal to a squared plus b squared—so x is simply 9 plus 16 equals 25! Subscribe now for daily visual math discoveries!",
        "comment_quiz_ko": "🧩 [시각 암산 퀴즈] 빗변 정사각형 넓이가 40이고 한쪽 작은 정사각형 넓이가 13이면 나머지 정사각형 넓이는? 댓글로 남겨보세요! 👇",
        "comment_quiz_en": "🧩 [Visual Check] If the hypotenuse square has area 40 and one leg square is 13, what is the other leg square's area? 👇",
    },
    {
        "slug": "2017090405",
        "diagram_kind": "isosceles_bisector",
        "exam_badge_ko": "◆ 대칭과 합동의 미학 · 황금삼각형",
        "exam_badge_en": "◆ Mirror Symmetry · Isosceles Triangle",
        "thumb_hook_ko": ["수식은 내려놓고,", "도형의 눈을 뜨다"],
        "thumb_hook_en": ["BEYOND FORMULAS,", "SEE THE SYMMETRY"],
        "problem_label_ko": "AB = AC인 삼각형에서 꼭지각 ∠A = 36°일 때, 밑각 ∠B = x는?",
        "problem_label_en": "In triangle ABC with AB = AC and ∠A = 36°, find base angle x = ∠B!",
        "figure_caption_ko": "AB = AC,  ∠A = 36°  →  ∠B = x = ?",
        "figure_caption_en": "AB = AC,  ∠A = 36°  →  ∠B = x = ?",
        "answer_label_ko": "꼭지각 이등분선 한 줄 → 완벽 대칭 합동!  x = (180°-36°)÷2 = 72°!",
        "answer_label_en": "1 Angle Bisector → Mirror SAS Congruence!  x = (180°-36°)÷2 = 72°!",
        "title_ko": "✨ 이등변삼각형의 본질을 여는 대칭선 한 줄! 황금삼각형 72°의 조화 | 시각적 증명",
        "title_en": "✨ The One Symmetry Line Behind Every Isosceles Triangle! | Base Angles Visual Proof",
        "short_title_ko": "❓ 꼭지각 36°일 때 밑각 x와 숨은 대칭선 한 줄이 보이시나요? #Shorts",
        "short_title_en": "❓ Vertex Angle 36°—Spot Base Angle x & the Hidden Symmetry Line! #Shorts",
        "act1_ko": "이등변삼각형의 성질을 가장 직관적으로 열어 주는 단 한 줄의 대칭선은 어디일까요? 꼭지각이 36도인 황금삼각형으로 완벽한 좌우 합동을 직접 확인해 보세요!",
        "act1_en": "Where does the single symmetry line lie that illuminates every isosceles triangle property? Discover it directly on this 36-degree golden triangle!",
        "act3_ko": "꼭지각 36도를 반으로 가르는 이등분선 한 줄이면 좌우 삼각형이 완벽히 포개져 두 밑각 x는 144도의 절반인 72도가 즉시 도출됩니다! 보조선 감각을 깨우는 시각적 증명, 지금 구독 눌러 매일 챙겨 보세요!",
        "act3_en": "Bisecting the 36-degree vertex folds the triangle into exact mirror halves, giving base angle x equals 72 degrees immediately! Hit Subscribe to build lasting geometric intuition!",
        "comment_quiz_ko": "🧩 [시각 암산 퀴즈] 이등변삼각형의 한 외각(꼭지각 바깥쪽 각)이 130°일 때 한 밑각 x는 몇 도일까요? 👇",
        "comment_quiz_en": "🧩 [Visual Check] If the exterior angle at the vertex of an isosceles triangle is 130°, what is each base angle x? 👇",
    },
    {
        "slug": "2014111902",
        "diagram_kind": "ceva_ratios",
        "exam_badge_ko": "◆ 공점과 넓이 비의 조화 · 체바 정리",
        "exam_badge_en": "◆ Ceva's Theorem · Area Ratio Balance",
        "thumb_hook_ko": ["수식은 내려놓고,", "도형의 눈을 뜨다"],
        "thumb_hook_en": ["BEYOND FORMULAS,", "SEE THE SYMMETRY"],
        "problem_label_ko": "세 체바선이 한 점 P에서 만나고 BD:DC=2:3, CE:EA=3:4일 때 AF:FB = x : y는?",
        "problem_label_en": "Three cevians concur at P with BD:DC=2:3 and CE:EA=3:4. Find AF:FB!",
        "figure_caption_ko": "BD:DC = 2:3, CE:EA = 3:4  →  AF:FB = x:y = ?",
        "figure_caption_en": "BD:DC = 2:3, CE:EA = 3:4  →  AF:FB = x:y = ?",
        "answer_label_ko": "삼각형 넓이 비 순환 곱 = 1 → (2/3)×(3/4)×(AF/FB)=1 → AF:FB = 2:1",
        "answer_label_en": "Cyclic Area Ratio = 1 → (2/3)×(3/4)×(AF/FB)=1 → AF:FB = 2:1!",
        "title_ko": "✨ 좌표 없이 넓이 비 하나로 약분된다! 삼각형 공점의 기하학 | 체바의 정리 시각적 증명",
        "title_en": "✨ How Triangle Area Ratios Cancel Cleanly to 1 | Ceva's Theorem Visual Proof",
        "short_title_ko": "❓ AF:FB 비율, 좌표 없이 넓이 비만으로 보이시나요? 체바의 정리 시각 증명! #Shorts",
        "short_title_en": "❓ Can You Spot Ratio AF:FB via Pure Area Balance? Ceva Visual Proof! #Shorts",
        "act1_ko": "삼각형 내부 한 점에서 세 직선이 만날 때, 복잡한 연립방정식이나 좌표 없이 AF 대 FB의 비율을 넓이의 균형만으로 읽어낼 수 있을까요?",
        "act1_en": "When three lines concur inside a triangle, can you read the missing side ratio AF to FB using pure area balance without coordinates?",
        "act3_ko": "밑변의 비가 곧 내부 삼각형 넓이의 비라는 원리로 3분의 2 곱하기 4분의 3 곱하기 AF 대 FB가 1이 되므로, 3이 약분되어 정답 2 대 1이 명쾌하게 완성됩니다! 깊이 있는 도형 통찰, 지금 바로 구독해 두세요!",
        "act3_en": "Because base ratios equal interior area ratios around point P, two-thirds times three-fourths times AF over FB equals 1—canceling 3 gives AF to FB equals 2 to 1! Subscribe now for more visual geometry insights!",
        "comment_quiz_ko": "🧩 [시각 암산 퀴즈] BD:DC = 1:2, CE:EA = 2:5일 때 한 점에서 만나려면 AF:FB는 몇 대 몇일까요? 댓글로 도전! 👇",
        "comment_quiz_en": "🧩 [Visual Check] If BD:DC = 1:2 and CE:EA = 2:5, what ratio AF:FB makes the three lines concurrent? 👇",
    },
    {
        "slug": "2014111901",
        "diagram_kind": "menelaus_line",
        "exam_badge_ko": "◆ 할선과 평행 닮음의 고리 · 메넬라우스",
        "exam_badge_en": "◆ Menelaus' Theorem · Parallel Proof",
        "thumb_hook_ko": ["왜 식 없이 보일까?", "보조선 한 줄의 통찰"],
        "thumb_hook_en": ["WHY NO ALGEBRA?", "ONE HIDDEN LINE"],
        "problem_label_ko": "할선이 연장선 D(BC:CD=1:1)와 변 위 E(CE:EA=1:3)를 지날 때 AF:FB는?",
        "problem_label_en": "A line cuts BC extended at D (BC=CD) and AC at E (CE:EA=1:3). Find AF:FB!",
        "figure_caption_ko": "BD:DC = 2:1, CE:EA = 1:3  →  AF:FB = ?",
        "figure_caption_en": "BD:DC = 2:1, CE:EA = 1:3  →  AF:FB = ?",
        "answer_label_ko": "평행보조선 한 줄 닮음 고리! (2/1)×(1/3)×(AF/FB)=1 → AF:FB = 3:2!",
        "answer_label_en": "1 Parallel Line Similarity Loop! (2/1)×(1/3)×(AF/FB)=1 → AF:FB = 3:2!",
        "title_ko": "✨ 외분점 비례가 한눈에 정렬된다! 평행보조선 한 줄의 닮음 원리 | 메넬라우스 정리 시각 증명",
        "title_en": "✨ Never Mix Up Ratio Order Again! One Parallel Line Proves It | Menelaus' Theorem Visualized",
        "short_title_ko": "❓ 삼각형을 가로지르는 직선의 비율, 평행선 한 줄의 원리! #Shorts",
        "short_title_en": "❓ A Line Across a Triangle—One Parallel Line Proves the Ratio! #Shorts",
        "act1_ko": "직선이 삼각형을 비스듬히 뚫고 지나갈 때 외분점 비례의 순서가 헷갈리신 적이 있나요? 꼭짓점을 지나는 평행선 딱 한 줄이면 원리가 절대 흔들리지 않습니다!",
        "act1_en": "Ever wonder why those three segment ratios along a transversal line always multiply to 1? One parallel auxiliary line makes the proportion unforgettable!",
        "act3_ko": "꼭짓점 점프 순환 고리에 그대로 넣으면 1분의 2 곱하기 3분의 1 곱하기 FB분의 AF가 1이 되어 AF 대 FB는 3 대 2로 단번에 정렬됩니다! 지금 채널을 구독하고 흔들리지 않는 도형 직관을 세워 보세요!",
        "act3_en": "Following the vertex-to-intersection loop gives 2 over 1 times 1 over 3 times AF over FB equals 1—so AF to FB is 3 to 2! Hit Subscribe for daily visual proof mastery!",
        "comment_quiz_ko": "🧩 [시각 암산 퀴즈] BD:DC = 3:1, CE:EA = 1:3이면 AF:FB는 몇 대 몇이 될까요? 암산 결과를 댓글로! 👇",
        "comment_quiz_en": "🧩 [Visual Check] If BD:DC = 3:1 and CE:EA = 1:3, what is AF:FB? Drop your answer below! 👇",
    },
]


def _clean_canvas_text(text: str) -> str:
    """Pillow Malgun Gothic 캔버스에서 두부 박스(□)를 유발하는 이모지·특수문자를 네이티브 기호로 정화"""
    repl = [
        ("⏱️", "◆"), ("⏱", "◆"),
        ("🚨", "◆"), ("📐", "■"),
        ("💡", "◆"), ("🎯", "◆"),
        ("✨", "◆"),
        ("🔔", "▶"), ("👇", "▶"),
        ("📝", "■"), ("⚡", "◆"),
        ("✅", "◆"), ("\u2794", "→"),
    ]
    out = str(text or "")
    for src, dst in repl:
        out = out.replace(src, dst)
    return re.sub(r"\s{2,}", " ", out).strip()


def _line_intersection_exact(p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float], p4: tuple[float, float]) -> tuple[float, float]:
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(den) < 1e-9:
        return ((x3 + x4) * 0.5, (y3 + y4) * 0.5)
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / den
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / den
    return (px, py)


def _draw_centered_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    fill,
    font,
    pill_bg=None,
    pill_outline=None,
    pad_x: int = 10,
    pad_y: int = 5,
):
    cx_t, cy_t = float(xy[0]), float(xy[1])
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    if pill_bg is not None or pill_outline is not None:
        draw.rounded_rectangle(
            (cx_t - tw * 0.5 - pad_x, cy_t - th * 0.5 - pad_y, cx_t + tw * 0.5 + pad_x, cy_t + th * 0.5 + pad_y),
            radius=10,
            fill=pill_bg,
            outline=pill_outline,
            width=2 if pill_outline else 0,
        )
    tx = cx_t - (bbox[0] + bbox[2]) * 0.5
    ty = cy_t - (bbox[1] + bbox[3]) * 0.5
    draw.text((tx, ty), text, fill=fill, font=font)


def _draw_outward_ratio_arc(
    draw: ImageDraw.ImageDraw,
    p1: tuple[float, float],
    p2: tuple[float, float],
    outward_normal: tuple[float, float],
    bow_px: float,
    label: str,
    color,
    font,
    pill_bg=(12, 20, 42),
):
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    seg_len = math.hypot(dx, dy)
    if seg_len < 1e-6:
        return
    nlen = math.hypot(outward_normal[0], outward_normal[1])
    if nlen < 1e-6:
        return
    nx, ny = outward_normal[0] / nlen, outward_normal[1] / nlen
    ux, uy = dx / seg_len, dy / seg_len
    trim = min(10.0, seg_len * 0.12)
    q0 = (p1[0] + ux * trim, p1[1] + uy * trim)
    q2 = (p2[0] - ux * trim, p2[1] - uy * trim)
    mid_x, mid_y = (p1[0] + p2[0]) * 0.5, (p1[1] + p2[1]) * 0.5
    q1 = (mid_x + nx * (2.0 * bow_px), mid_y + ny * (2.0 * bow_px))

    pts = []
    n_seg = 16
    for i in range(n_seg + 1):
        t = i / n_seg
        mt = 1.0 - t
        bx = mt * mt * q0[0] + 2.0 * mt * t * q1[0] + t * t * q2[0]
        by = mt * mt * q0[1] + 2.0 * mt * t * q1[1] + t * t * q2[1]
        pts.append((bx, by))
    for i in range(0, n_seg, 2):
        draw.line([pts[i], pts[i + 1]], fill=color, width=3)

    if label:
        lx = mid_x + nx * (bow_px + 20.0)
        ly = mid_y + ny * (bow_px + 20.0)
        _draw_centered_text(draw, (lx, ly), label, fill=color, font=font, pill_bg=pill_bg, pad_x=6, pad_y=3)


def _draw_exam_problem_diagram(draw: ImageDraw.ImageDraw, box: tuple, kind: str, solved: bool = False, canvas_img: Image.Image | None = None, pdf_doc=None, lang_code: str = "ko"):
    """Act 1(문제 제시) 및 Act 3(보조선 해체 완료)용 100% 해석기하 정밀 작도 다이어그램"""
    import min7014_video_maker as vmaker

    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) * 0.5, (y0 + y1) * 0.5
    draw.rounded_rectangle(box, radius=24, fill=(12, 20, 42), outline=(56, 189, 248), width=3)

    if kind == "pdf_native" and canvas_img is not None and pdf_doc is not None and len(pdf_doc) >= 1:
        idx_p = max(0, len(pdf_doc) - 2) if solved else 0
        pix = pdf_doc[idx_p].get_pixmap(dpi=220)
        sl = vmaker._mask_pdf_bottom_author_bar(Image.frombytes("RGB", [pix.width, pix.height], pix.samples))
        sc = min((w - 36) / sl.width, (h - 36) / sl.height)
        nw, nh = int(sl.width * sc), int(sl.height * sc)
        px, py = int(x0 + (w - nw) // 2), int(y0 + (h - nh) // 2)
        canvas_img.paste(sl.resize((nw, nh), Image.Resampling.LANCZOS), (px, py))
        return

    cyan = (56, 189, 248)
    gold = (250, 204, 21)
    amber_aux = (245, 158, 11)
    white = (248, 250, 252)
    green = (52, 211, 153)
    violet = (167, 139, 250)
    bg_dark = (12, 20, 42)
    is_en = lang_code == "en"

    f_lbl = vmaker.get_font_for_lang("ko", max(22, int(min(w, h) * 0.036)), bold=True)
    f_val = vmaker.get_font_for_lang("ko", max(20, int(min(w, h) * 0.032)), bold=True)
    r = min(w, h) * 0.34

    def _dot(pt: tuple[float, float], color=gold, rad: int = 8):
        px, py = float(pt[0]), float(pt[1])
        draw.ellipse((px - rad, py - rad, px + rad, py + rad), fill=color, outline=white, width=2)

    if kind == "circle_inscribed":
        # 정확히 중심각 ∠AOB = 84° (132° ~ 48°), 원주각 ∠APB = 42°
        rc = r * 0.88
        O = (cx, cy + rc * 0.04)
        A = (O[0] + rc * math.cos(math.radians(132.0)), O[1] + rc * math.sin(math.radians(132.0)))
        B = (O[0] + rc * math.cos(math.radians(48.0)), O[1] + rc * math.sin(math.radians(48.0)))
        P = (O[0] + rc * math.cos(math.radians(-76.0)), O[1] + rc * math.sin(math.radians(-76.0)))
        draw.ellipse((O[0] - rc, O[1] - rc, O[0] + rc, O[1] + rc), outline=cyan, width=5)
        draw.line([A, O, B], fill=gold, width=5)
        draw.line([A, P, B], fill=white, width=5)
        if solved:
            D = (2 * O[0] - P[0], 2 * O[1] - P[1])
            draw.line([P, D], fill=green, width=6)
            _dot(D, green, 7)
            _draw_centered_text(draw, (D[0], D[1] + 26), "D", fill=green, font=f_val, pill_bg=bg_dark, pad_x=4, pad_y=2)
        for pt, lbl, dx, dy in [(A, "A", -26, 18), (B, "B", 26, 18), (P, "P", 18, -24), (O, "O", -24, -14)]:
            _dot(pt, gold if pt != P else cyan, 7)
            _draw_centered_text(draw, (pt[0] + dx, pt[1] + dy), lbl, fill=white, font=f_lbl)
        # ∠APB 내부 각이등분선 방향 배치 (선분 PA, PB, 지름 PD와 비중첩)
        u_pa = ((A[0] - P[0]) / math.hypot(A[0] - P[0], A[1] - P[1]), (A[1] - P[1]) / math.hypot(A[0] - P[0], A[1] - P[1]))
        u_pb = ((B[0] - P[0]) / math.hypot(B[0] - P[0], B[1] - P[1]), (B[1] - P[1]) / math.hypot(B[0] - P[0], B[1] - P[1]))
        bis_x, bis_y = u_pa[0] + u_pb[0], u_pa[1] + u_pb[1]
        blen = math.hypot(bis_x, bis_y)
        bis_x, bis_y = bis_x / blen, bis_y / blen
        ang_dist = max(82.0, r * 0.33)
        if solved:
            _draw_centered_text(draw, (P[0] + bis_x * ang_dist + 34, P[1] + bis_y * ang_dist + 6), "42°", fill=green, font=f_val, pill_bg=bg_dark, pad_x=6, pad_y=3)
            _draw_centered_text(draw, (O[0] + 34, O[1] + 28), "84°", fill=gold, font=f_lbl, pill_bg=bg_dark, pad_x=6, pad_y=3)
        else:
            _draw_centered_text(draw, (P[0] + bis_x * ang_dist, P[1] + bis_y * ang_dist), "x=?", fill=gold, font=f_val, pill_bg=bg_dark, pad_x=6, pad_y=3)
            _draw_centered_text(draw, (O[0], O[1] + max(34.0, r * 0.14)), "84°", fill=gold, font=f_lbl, pill_bg=bg_dark, pad_x=6, pad_y=3)

    elif kind == "tangent_chord":
        # 정확히 접점 A(바닥 90°), 우측 수평 접선 AT와 현 AB 사이 예각 58° -> B는 중심각 -26° 위치
        rc = r * 0.84
        O = (cx, cy - 16)
        A = (O[0], O[1] + rc)
        B = (O[0] + rc * math.cos(math.radians(-26.0)), O[1] + rc * math.sin(math.radians(-26.0)))
        C = (O[0] + rc * math.cos(math.radians(-145.0)), O[1] + rc * math.sin(math.radians(-145.0)))
        draw.ellipse((O[0] - rc, O[1] - rc, O[0] + rc, O[1] + rc), outline=cyan, width=5)
        draw.line([(cx - rc * 1.22, A[1]), (cx + rc * 1.22, A[1])], fill=gold, width=5)
        draw.polygon([A, B, C], outline=white, width=5)
        if solved:
            D = (O[0], O[1] - rc)
            draw.line([A, D], fill=green, width=6)
            draw.line([D, B], fill=amber_aux, width=4)
            _dot(D, green, 7)
            _draw_centered_text(draw, (D[0], D[1] - 28), "D(diam)" if is_en else "D(지름)", fill=green, font=f_val, pill_bg=bg_dark, pad_x=6, pad_y=3)
        for pt, lbl, dx, dy in [(A, "A", -4, 24), (B, "B", 24, 4), (C, "C", -26, -18)]:
            _dot(pt, gold, 7)
            _draw_centered_text(draw, (pt[0] + dx, pt[1] + dy), lbl, fill=white, font=f_lbl)
        _draw_centered_text(draw, (cx + rc * 1.12, A[1] + 24), "T", fill=gold, font=f_lbl)
        _draw_centered_text(draw, (A[0] + max(64.0, r * 0.25), A[1] - max(28.0, r * 0.11)), "58°", fill=gold, font=f_val, pill_bg=bg_dark, pad_x=6, pad_y=3)
        u_ca = ((A[0] - C[0]) / math.hypot(A[0] - C[0], A[1] - C[1]), (A[1] - C[1]) / math.hypot(A[0] - C[0], A[1] - C[1]))
        u_cb = ((B[0] - C[0]) / math.hypot(B[0] - C[0], B[1] - C[1]), (B[1] - C[1]) / math.hypot(B[0] - C[0], B[1] - C[1]))
        cbx, cby = u_ca[0] + u_cb[0], u_ca[1] + u_cb[1]
        cln = math.hypot(cbx, cby)
        cbx, cby = cbx / cln, cby / cln
        cdist = max(66.0, r * 0.27)
        _draw_centered_text(draw, (C[0] + cbx * cdist, C[1] + cby * cdist), "58°" if solved else "x=?", fill=green if solved else gold, font=f_val, pill_bg=bg_dark, pad_x=6, pad_y=3)

    elif kind == "pythagoras_squares":
        # 정확한 3 : 4 : 5 직각삼각형 + 세 변 위의 진짜 1:1 정사각형 3개 (S1=9, S2=16, S3=x=25) — 박스 내부 여백 100% 보장
        u = min(w, h) * 0.068
        C = (cx - 0.95 * u, cy + 1.35 * u)
        A = (C[0], C[1] - 3.0 * u)          # 수직변 길이 3u (넓이 9)
        B = (C[0] + 4.0 * u, C[1])          # 수평변 길이 4u (넓이 16)
        sq1 = [A, C, (C[0] - 3.0 * u, C[1]), (A[0] - 3.0 * u, A[1])]
        sq2 = [C, B, (B[0], B[1] + 4.0 * u), (C[0], C[1] + 4.0 * u)]
        nx, ny = 3.0 * u, -4.0 * u
        sq3 = [A, B, (B[0] + nx, B[1] + ny), (A[0] + nx, A[1] + ny)]

        draw.polygon(sq1, fill=(14, 52, 78), outline=cyan, width=4)
        draw.polygon(sq2, fill=(14, 62, 54), outline=green, width=4)
        draw.polygon(sq3, fill=(58, 44, 18), outline=gold, width=5)
        draw.polygon([A, B, C], fill=(16, 26, 48), outline=white, width=5)
        rk = u * 0.45
        draw.line([(C[0], C[1] - rk), (C[0] + rk, C[1] - rk), (C[0] + rk, C[1])], fill=white, width=3)
        c1x, c1y = sum(p[0] for p in sq1) / 4, sum(p[1] for p in sq1) / 4
        c2x, c2y = sum(p[0] for p in sq2) / 4, sum(p[1] for p in sq2) / 4
        _draw_centered_text(draw, (c1x, c1y), "9", fill=white, font=f_lbl)
        _draw_centered_text(draw, (c2x, c2y), "16", fill=white, font=f_lbl)
        if solved:
            ux, uy = (B[0] - A[0]) / (5.0 * u), (B[1] - A[1]) / (5.0 * u)
            proj = (C[0] - A[0]) * ux + (C[1] - A[1]) * uy
            H_foot = (A[0] + proj * ux, A[1] + proj * uy)
            H_far = (H_foot[0] + nx, H_foot[1] + ny)
            draw.line([C, H_far], fill=amber_aux, width=5)
            right_rect = [H_foot, B, (B[0] + nx, B[1] + ny), H_far]
            c3r_x = sum(p[0] for p in right_rect) / 4
            c3r_y = sum(p[1] for p in right_rect) / 4
            _draw_centered_text(draw, (c3r_x, c3r_y), "x = 25", fill=gold, font=f_lbl, pill_bg=(24, 20, 10), pill_outline=gold, pad_x=10, pad_y=6)
        else:
            c3x, c3y = sum(p[0] for p in sq3) / 4, sum(p[1] for p in sq3) / 4
            _draw_centered_text(draw, (c3x, c3y), "x = ?", fill=gold, font=f_lbl)

    elif kind == "isosceles_bisector":
        # 정확한 꼭지각 36°, 두 밑각 72°인 황금 이등변삼각형 (AB = AC)
        h_tri = r * 1.68
        half_b = h_tri * math.tan(math.radians(18.0))
        A = (cx, cy - h_tri * 0.50)
        B = (cx - half_b, cy + h_tri * 0.50)
        C = (cx + half_b, cy + h_tri * 0.50)
        draw.polygon([A, B, C], outline=cyan, width=5)
        # 등변 표시 눈금
        for P1, P2 in [(A, B), (A, C)]:
            mx, my = (P1[0] + P2[0]) * 0.5, (P1[1] + P2[1]) * 0.5
            dx, dy = P2[0] - P1[0], P2[1] - P1[1]
            ln = math.hypot(dx, dy)
            nx, ny = -dy / ln * 10, dx / ln * 10
            draw.line([(mx - nx, my - ny), (mx + nx, my + ny)], fill=gold, width=4)
        if solved:
            M = (cx, B[1])
            draw.line([A, M], fill=green, width=6)
            draw.rectangle((M[0], M[1] - 16, M[0] + 16, M[1]), outline=white, width=3)
            _dot(M, green, 7)
        for pt, lbl, dx, dy in [(A, "A(36°)", 0, -30), (B, "B", -26, 18), (C, "C", 26, 18)]:
            _dot(pt, gold, 7)
            _draw_centered_text(draw, (pt[0] + dx, pt[1] + dy), lbl, fill=white, font=f_lbl)
        u_ba = ((A[0] - B[0]) / math.hypot(A[0] - B[0], A[1] - B[1]), (A[1] - B[1]) / math.hypot(A[0] - B[0], A[1] - B[1]))
        bbx, bby = u_ba[0] + 1.0, u_ba[1]
        bbl = math.hypot(bbx, bby)
        bbx, bby = bbx / bbl, bby / bbl
        bdist = max(76.0, r * 0.30)
        _draw_centered_text(draw, (B[0] + bbx * bdist, B[1] + bby * bdist), "72°" if solved else "x=?", fill=green if solved else gold, font=f_val, pill_bg=bg_dark, pad_x=6, pad_y=3)

    elif kind == "menelaus_line":
        # 메넬라우스 정리 정밀 작도: BC=CD (BD:DC=2:1), CE:EA=1:3 -> AF:FB=3:2 (D-E-F 100% 일직선 공선점!)
        A = (cx - r * 0.24, cy - r * 0.82)
        B = (cx - r * 1.04, cy + r * 0.72)
        C = (cx + r * 0.02, cy + r * 0.72)
        D = (2.0 * C[0] - B[0], C[1])                    # BC 연장선 외분점 (BC:CD = 1:1 => BD:DC = 2:1)
        E = ((3.0 * C[0] + A[0]) / 4.0, (3.0 * C[1] + A[1]) / 4.0)  # CE:EA = 1:3
        F = _line_intersection_exact(D, E, A, B)         # 할선 DE와 변 AB의 실제 해석기하 교점 (정확히 AF:FB = 3:2!)

        draw.polygon([A, B, C], outline=cyan, width=5)
        draw.line([C, D], fill=cyan, width=4)
        # 할선 연장 (F 바깥 ~ D 바깥까지 정확히 한 직선!)
        vx, vy = D[0] - F[0], D[1] - F[1]
        p_start = (F[0] - vx * 0.14, F[1] - vy * 0.14)
        p_end = (D[0] + vx * 0.08, D[1] + vy * 0.08)
        draw.line([p_start, p_end], fill=gold, width=5)

        if solved:
            # 꼭짓점 C를 지나고 AB에 평행한 보조선 CK ∥ AB
            C_par = (C[0] + (A[0] - B[0]), C[1] + (A[1] - B[1]))
            K = _line_intersection_exact(D, F, C, C_par)
            draw.line([C, K], fill=green, width=6)
            _dot(K, green, 7)
            _draw_centered_text(draw, (K[0] + 48, K[1] + 30), "K(∥AB)" if is_en else "K(평행)", fill=green, font=f_val, pill_bg=bg_dark, pad_x=6, pad_y=3)

        # 변 AB 바깥(좌상) 외분호 & 비율 표기
        ab_dx, ab_dy = B[0] - A[0], B[1] - A[1]
        n_ab = (-ab_dy, ab_dx)
        bow = max(20.0, r * 0.10)
        _draw_outward_ratio_arc(draw, A, F, n_ab, bow, "3" if solved else "x", green if solved else gold, f_val, pill_bg=bg_dark)
        _draw_outward_ratio_arc(draw, F, B, n_ab, bow, "2" if solved else "y", green if solved else gold, f_val, pill_bg=bg_dark)

        pill_txt = "AF : FB = 3 : 2" if solved else "AF : FB = x : y = ?"
        pill_col = green if solved else gold
        pbbox = draw.textbbox((0, 0), pill_txt, font=f_val)
        pill_cx = max(x0 + 138, x0 + 24 + 12 + (pbbox[2] - pbbox[0]) * 0.5)
        _draw_centered_text(draw, (pill_cx, y0 + 42), pill_txt, fill=pill_col, font=f_val, pill_bg=(16, 28, 56), pill_outline=pill_col, pad_x=12, pad_y=6)

        for pt, lbl, dx, dy, col in [
            (A, "A", -6, -30, white),
            (B, "B", -22, 20, white),
            (C, "C", -4, 24, white),
            (D, "D", 14, 22, gold),
            (E, "E", 24, -14, gold),
            (F, "F", 20, 24, green if solved else gold),
        ]:
            _dot(pt, col, 7)
            _draw_centered_text(draw, (pt[0] + dx, pt[1] + dy), lbl, fill=col, font=f_lbl, pill_bg=bg_dark, pad_x=4, pad_y=2)

    else:
        # 체바의 정리(ceva_ratios) 비대칭 부등변 삼각형 + 100% 정밀 무게중심 좌표(질량점 m_A=3, m_B=6, m_C=4) 작도!
        # -> BD:DC = 4:6 = 2:3, CE:EA = 3:4, AF:FB = 6:3 = 2:1 이며 세 직선 AD, BE, CF가 단 0.000px 오차도 없이 정확히 한 점 P에서 만남!
        A = (cx - r * 0.36, cy - r * 0.80)
        B = (cx - r * 0.92, cy + r * 0.68)
        C = (cx + r * 0.98, cy + r * 0.68)

        mA, mB, mC = 3.0, 6.0, 4.0
        D = ((mB * B[0] + mC * C[0]) / (mB + mC), (mB * B[1] + mC * C[1]) / (mB + mC))  # BD:DC = 2:3
        E = ((mC * C[0] + mA * A[0]) / (mC + mA), (mC * C[1] + mA * A[1]) / (mC + mA))  # CE:EA = 3:4
        F = ((mA * A[0] + mB * B[0]) / (mA + mB), (mA * A[1] + mB * B[1]) / (mA + mB))  # AF:FB = 2:1
        P = ((mA * A[0] + mB * B[0] + mC * C[0]) / (mA + mB + mC), (mA * A[1] + mB * B[1] + mC * C[1]) / (mA + mB + mC))

        if solved:
            # 세 내부 삼각형(△PAB, △PBC, △PCA) 넓이 비 분할 시각화
            draw.polygon([P, B, C], fill=(16, 48, 76), outline=cyan, width=2)
            draw.polygon([P, C, A], fill=(20, 56, 54), outline=cyan, width=2)
            draw.polygon([P, A, B], fill=(46, 36, 72), outline=cyan, width=2)

        # 선분 ➔ 외곽 삼각형 ➔ 7개 꼭짓점·분점·공점 도트 순으로 그려 끝점 돌출 ZERO 보장
        cev_cf_col = green if solved else (196, 181, 253)
        draw.line([A, D], fill=gold, width=5)
        draw.line([B, E], fill=gold, width=5)
        draw.line([C, F], fill=cev_cf_col, width=5)
        draw.polygon([A, B, C], outline=cyan, width=5)

        for pt, col, rad in [
            (A, cyan, 7),
            (B, cyan, 7),
            (C, cyan, 7),
            (D, gold, 7),
            (E, violet, 7),
            (F, green if solved else white, 7),
            (P, amber_aux, 9),
        ]:
            _dot(pt, col, rad)

        # 3변 바깥 점선 분할 호 + 비율 수치 (2014111902.pdf 시각 언어 통일)
        bow = r * 0.11
        _draw_outward_ratio_arc(draw, B, D, (0.0, 1.0), bow, "2", gold, f_val, pill_bg=bg_dark)
        _draw_outward_ratio_arc(draw, D, C, (0.0, 1.0), bow, "3", gold, f_val, pill_bg=bg_dark)

        ca_dx, ca_dy = A[0] - C[0], A[1] - C[1]
        ca_len = math.hypot(ca_dx, ca_dy)
        n_ca = (-ca_dy / ca_len, ca_dx / ca_len)
        _draw_outward_ratio_arc(draw, C, E, n_ca, bow, "3", violet, f_val, pill_bg=bg_dark)
        _draw_outward_ratio_arc(draw, E, A, n_ca, bow, "4", violet, f_val, pill_bg=bg_dark)

        ab_dx, ab_dy = B[0] - A[0], B[1] - A[1]
        ab_len = math.hypot(ab_dx, ab_dy)
        n_ab = (-ab_dy / ab_len, ab_dx / ab_len)
        ab_col = green if solved else gold
        _draw_outward_ratio_arc(draw, A, F, n_ab, bow, "2" if solved else "x", ab_col, f_val, pill_bg=bg_dark)
        _draw_outward_ratio_arc(draw, F, B, n_ab, bow, "1" if solved else "y", ab_col, f_val, pill_bg=bg_dark)

        # 좌상단 여백 핵심 질문 배지
        pill_txt = "AF : FB = 2 : 1" if solved else "AF : FB = x : y = ?"
        pill_col = green if solved else gold
        pbbox = draw.textbbox((0, 0), pill_txt, font=f_val)
        pill_cx = max(x0 + 138, x0 + 24 + 12 + (pbbox[2] - pbbox[0]) * 0.5)
        _draw_centered_text(draw, (pill_cx, y0 + 42), pill_txt, fill=pill_col, font=f_val, pill_bg=(16, 28, 56), pill_outline=pill_col, pad_x=12, pad_y=6)

        # 7개 점 라벨 비중첩 배치 (∠APE 73° 열린 섹터 내부에 P 배치)
        for pt, lbl, dx, dy, col, use_pill in [
            (A, "A", -8, -28, white, False),
            (B, "B", -24, 18, white, False),
            (C, "C", 24, 18, white, False),
            (D, "D", 0, 24, gold, True),
            (E, "E", 25 * n_ca[0], 25 * n_ca[1], violet, True),
            (F, "F", 25 * n_ab[0], 25 * n_ab[1], green if solved else white, True),
            (P, "P", r * 0.09, -r * 0.14, amber_aux, True),
        ]:
            _draw_centered_text(
                draw,
                (pt[0] + dx, pt[1] + dy),
                lbl,
                fill=col,
                font=f_lbl,
                pill_bg=bg_dark if use_pill else None,
                pad_x=4,
                pad_y=2,
            )


def _fit_font_to_width(draw: ImageDraw.ImageDraw, vmaker, text: str, max_w: int, start_sz: int, min_sz: int = 18):
    sz = start_sz
    while sz >= min_sz:
        f = vmaker.get_font_for_lang("ko", sz, bold=True)
        bbox = draw.textbbox((0, 0), text, font=f)
        if (bbox[2] - bbox[0]) <= max_w:
            return f
        sz -= 2
    return vmaker.get_font_for_lang("ko", min_sz, bold=True)


def render_exam_hybrid_thumbnail(bp: dict, doc, lang_code: str, out_png: Path) -> Path:
    import min7014_video_maker as vmaker

    W, H = 1280, 720
    # 코스믹 아틀리에 딥 네이비 배경 & 절제된 그리드 (designer × pr)
    img = Image.new("RGB", (W, H), (6, 11, 25))
    draw = ImageDraw.Draw(img)
    for gx in range(0, W, 80):
        draw.line([(gx, 0), (gx, H)], fill=(13, 21, 44), width=1)
    for gy in range(0, H, 80):
        draw.line([(0, gy), (W, gy)], fill=(13, 21, 44), width=1)

    is_en = lang_code == "en"
    # 우측: 원본 min7014.github.io 클라이맥스 슬라이드 무결점 배치 (Rule 28 · 유클리드 슬레이트 베젤 + 샴페인 골드 테두리)
    key_idx = max(0, len(doc) - 2)
    pix = doc[key_idx].get_pixmap(dpi=240)
    slide_img = vmaker._mask_pdf_bottom_author_bar(Image.frombytes("RGB", [pix.width, pix.height], pix.samples))
    scale = min(620 / slide_img.width, 580 / slide_img.height)
    sw, sh = int(slide_img.width * scale), int(slide_img.height * scale)
    sx, sy = W - sw - 34, (H - sh) // 2
    draw.rounded_rectangle((sx - 12, sy - 12, sx + sw + 12, sy + sh + 12), radius=22, fill=(15, 25, 48), outline=(234, 179, 8), width=3)
    img.paste(slide_img.resize((sw, sh), Image.Resampling.LANCZOS), (sx, sy))

    # 좌측 상단 아틀리에 배지 (딥 로열 인디고 + 시안 헤어라인 테두리)
    badge = _clean_canvas_text(bp["exam_badge_en"] if is_en else bp["exam_badge_ko"])
    draw.rounded_rectangle((36, 36, 586, 98), radius=14, fill=(14, 30, 62), outline=(56, 189, 248), width=2)
    f_badge = _fit_font_to_width(draw, vmaker, badge, max_w=516, start_sz=25, min_sz=18)
    draw.text((54, 52), badge, fill=(224, 242, 254), font=f_badge)

    # 좌측 초대형 2줄 시대를 초월한 기하 직관 헤드라인 + 4px 골드 수직 악센트 바
    kind = bp.get("diagram_kind", "pdf_native")
    if bp.get("thumb_hook_ko") and bp.get("thumb_hook_en"):
        h_lines = bp["thumb_hook_en"] if is_en else bp["thumb_hook_ko"]
    elif kind in ("circle_inscribed", "tangent_chord", "menelaus_line"):
        h_lines = ["WHY NO ALGEBRA?", "ONE HIDDEN LINE"] if is_en else ["왜 식 없이 보일까?", "보조선 한 줄의 통찰"]
    elif kind in ("pythagoras_squares", "isosceles_bisector", "ceva_ratios"):
        h_lines = ["BEYOND FORMULAS,", "SEE THE SYMMETRY"] if is_en else ["수식은 내려놓고,", "도형의 눈을 뜨다"]
    else:
        h_lines = ["BEYOND FORMULAS", "ONE VISUAL PROOF"] if is_en else ["공식 너머의 필연성,", "한눈에 읽는 증명"]

    draw.rounded_rectangle((36, 134, 41, 282), radius=2, fill=(250, 204, 21))
    yh = 132
    for idx_l, hl in enumerate(h_lines[:2]):
        f_big = _fit_font_to_width(draw, vmaker, hl, max_w=532, start_sz=(48 if is_en else 54), min_sz=32)
        c_fill = (248, 250, 252) if idx_l == 0 else (250, 204, 21)
        # 부드러운 드롭 섀도 + 절제된 딥 네이비 윤곽
        draw.text((55, yh + 4), hl, fill=(2, 4, 12), font=f_big)
        for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2)):
            draw.text((52 + dx, yh + dy), hl, fill=(4, 8, 20), font=f_big)
        draw.text((52, yh), hl, fill=c_fill, font=f_big)
        yh += 78

    # 좌측 중단 원리·탐구 카드 (문맥 분리: pdf_native = CORE THEOREM, 탐구 수치 = VISUAL INQUIRY)
    draw.rounded_rectangle((36, 316, 586, 496), radius=18, fill=(13, 22, 46), outline=(56, 189, 248), width=2)
    cap_main = _clean_canvas_text(bp["figure_caption_en"] if is_en else bp["figure_caption_ko"])
    if kind == "pdf_native":
        cap_main = re.sub(r"^(?:핵심\s*원리\s*[:：]|Core\s*Principle\s*[:：])\s*", "", cap_main, flags=re.I).strip()
        box_hdr = "CORE THEOREM · 핵심 정리" if not is_en else "CORE THEOREM"
    else:
        box_hdr = "VISUAL INQUIRY · 사유의 질문" if not is_en else "VISUAL INQUIRY"
    draw.text((56, 338), box_hdr, fill=(250, 204, 21), font=vmaker.get_font_for_lang("ko", 24, bold=True))
    has_ko_cap = bool(re.search(r"[가-힣]", cap_main))
    t_sz, t_w = (30, 19) if has_ko_cap else (30, 25)
    wrapped_cap = textwrap.wrap(cap_main, width=t_w)
    if len(wrapped_cap) > 2:
        t_sz, t_w = (25, 24) if has_ko_cap else (25, 30)
        wrapped_cap = textwrap.wrap(cap_main, width=t_w)
    f_tcap = vmaker.get_font_for_lang("ko", t_sz, bold=True)
    yc = 382 if len(wrapped_cap) <= 2 else 374
    t_lh = 44 if len(wrapped_cap) <= 2 else 34
    for cl in wrapped_cap[:3]:
        draw.text((56, yc), cl, fill=(186, 230, 253), font=f_tcap)
        yc += t_lh

    # 하단 아틀리에 브랜드 바 (딥 에메랄드 슬레이트 + 민트 헤어라인)
    draw.rounded_rectangle((36, 540, 586, 656), radius=16, fill=(10, 38, 46), outline=(45, 212, 191), width=2)
    cta1 = "공식 암기 없이, 눈으로 읽는 원리" if not is_en else "See the Logic · Remember Forever"
    cta2 = "▶ @min7014_ai · 시각적 증명 아틀리에" if not is_en else "▶ @min7014_ai · Visual Proof Atelier"
    f_cta1 = _fit_font_to_width(draw, vmaker, cta1, max_w=516, start_sz=24, min_sz=18)
    f_cta2 = _fit_font_to_width(draw, vmaker, cta2, max_w=516, start_sz=24, min_sz=18)
    draw.text((56, 558), cta1, fill=(253, 230, 138), font=f_cta1)
    draw.text((56, 602), cta2, fill=(248, 250, 252), font=f_cta2)

    img.save(out_png, quality=98)
    return out_png


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


def _encode_single_card_segment(frame_img: Image.Image, mp3_path: Path, out_mp4: Path, ffmpeg_exe: str, ffprobe_exe: str):
    import min7014_video_maker as vmaker

    dur = max(3.5, vmaker.get_media_duration_seconds(mp3_path, ffprobe_exe) + 0.35)
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


def render_exam_hybrid_bundle(bp: dict, lang_code: str = "ko") -> dict:
    """
    단일 블루프린트에 대해:
    1) 1080p 16:9 '실전 문제 → min7014 시각 증명 → 5초 해체' 본편 (3~5분 스윗스팟) + 전용 썸네일
    2) 1080x1920 9:16 '실전 x=? 3초 챌린지 Q-#Shorts' (32~42초 스와이프 방어 포맷)
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

    ffmpeg_exe = shutil.which("ffmpeg")
    ffprobe_exe = shutil.which("ffprobe")
    voice_name = vmaker.GLOBAL_VOICE_MAP.get(lang_code, vmaker.GLOBAL_VOICE_MAP["en"])["voice"]
    is_en = lang_code == "en"

    long_mp4 = EXAM_HYBRID_DIR / f"{slug}_exam_{lang_code}.mp4"
    long_thumb = EXAM_HYBRID_DIR / f"{slug}_exam_{lang_code}_thumb.png"
    short_mp4 = EXAM_HYBRID_DIR / f"{slug}_exam_short_{lang_code}.mp4"

    render_exam_hybrid_thumbnail(bp, doc, lang_code, long_thumb)

    pages = sdoc.get("pages") or []
    n_pages = len(pages)
    # 3~5분 최적 완주 구간을 위해 핵심 6단계 추출
    if n_pages <= 6:
        mid_indices = list(range(n_pages))
    else:
        mid_indices = sorted(list({0, max(1, n_pages // 5), (2 * n_pages) // 5, (3 * n_pages) // 5, (4 * n_pages) // 5, n_pages - 1}))

    tmp_dir = Path(tempfile.mkdtemp(prefix=f"exam_hyb_{slug}_{lang_code}_"))
    try:
        # ---------------- A. 1080p 16:9 Exam-Hybrid 본편 ----------------
        long_segs = []
        # Act 1: 실전 시험 문제 카드 (1920x1080)
        act1_img = Image.new("RGB", (1920, 1080), (8, 13, 28))
        d1 = ImageDraw.Draw(act1_img)
        d1.rounded_rectangle((56, 44, 1864, 156), radius=22, fill=(30, 64, 175), outline=(250, 204, 21), width=4)
        d1.text((88, 74), _clean_canvas_text(bp["exam_badge_en"] if is_en else bp["exam_badge_ko"]), fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 42, bold=True))
        d1.text((1380, 78), "◆ VISUAL INQUIRY" if is_en else "◆ 시각 직관 탐구", fill=(254, 240, 138), font=vmaker.get_font_for_lang(lang_code, 36, bold=True))

        _draw_exam_problem_diagram(d1, (68, 196, 940, 880), bp["diagram_kind"], solved=False, canvas_img=act1_img, pdf_doc=doc, lang_code=lang_code)
        d1.rounded_rectangle((980, 196, 1852, 880), radius=24, fill=(15, 23, 42), outline=(56, 189, 248), width=3)
        p_lbl = _clean_canvas_text(bp["problem_label_en"] if is_en else bp["problem_label_ko"])
        y_txt = 248
        for line in textwrap.wrap(p_lbl, width=28 if is_en else 18)[:4]:
            d1.text((1024, y_txt), line, fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 42, bold=True))
            y_txt += 64
        d1.rounded_rectangle((1024, 560, 1808, 700), radius=18, fill=(30, 41, 59), outline=(250, 204, 21), width=3)
        cap_long = _clean_canvas_text(bp["figure_caption_en"] if is_en else bp["figure_caption_ko"])
        f_cap_long = vmaker.get_font_for_lang(lang_code, 36, bold=True)
        for cap_sz in (36, 32, 29, 26, 23):
            f_cap_cand = vmaker.get_font_for_lang(lang_code, cap_sz, bold=True)
            cb = d1.textbbox((0, 0), cap_long, font=f_cap_cand)
            if cb[2] - cb[0] <= 736:
                f_cap_long = f_cap_cand
                break
        _draw_centered_text(d1, ((1024 + 1808) * 0.5, (560 + 700) * 0.5), cap_long, fill=(250, 204, 21), font=f_cap_long)
        d1.text((1024, 760), "★ Hint: Don't write equations—spot ONE line!" if is_en else "★ 힌트: 방정식을 세우지 말고 보조선 1줄을 찾으세요!", fill=(125, 211, 252), font=vmaker.get_font_for_lang(lang_code, 30, bold=True))

        act1_mp3 = tmp_dir / "long_act1.mp3"
        act1_seg = tmp_dir / "long_act1.mp4"
        vmaker.synthesize_tts_mp3_sync(bp["act1_en"] if is_en else bp["act1_ko"], voice_name, act1_mp3, rate="+8%")
        _encode_single_card_segment(act1_img, act1_mp3, act1_seg, ffmpeg_exe, ffprobe_exe)
        long_segs.append(act1_seg)

        # Act 2: 원본 min7014.github.io PDF 핵심 슬라이드 증명 (Rule 28 100% 준수: 무크롭 원본 비율 유지)
        for idx_s, p_idx in enumerate(mid_indices, 1):
            p_info = pages[p_idx]
            doc_p = min(len(doc) - 1, max(0, int(p_info.get("page", p_idx + 1)) - 1))
            pix = doc[doc_p].get_pixmap(dpi=240)
            s_raw = vmaker._mask_pdf_bottom_author_bar(Image.frombytes("RGB", [pix.width, pix.height], pix.samples))
            frame = Image.new("RGB", (1920, 1080), (10, 16, 34))
            df = ImageDraw.Draw(frame)
            df.rounded_rectangle((48, 26, 1872, 108), radius=16, fill=(15, 23, 42), outline=(56, 189, 248), width=2)
            hdr = f"■ Visual Proof Step {idx_s}/{len(mid_indices)} (min7014.github.io)" if is_en else f"■ 핵심 시각 증명 STEP {idx_s}/{len(mid_indices)} (원리 해체)"
            df.text((76, 46), hdr, fill=(125, 211, 252), font=vmaker.get_font_for_lang(lang_code, 32, bold=True))

            sc = min(1760 / s_raw.width, 880 / s_raw.height)
            nw, nh = int(s_raw.width * sc), int(s_raw.height * sc)
            ox, oy = (1920 - nw) // 2, 128 + (920 - nh) // 2
            df.rounded_rectangle((ox - 8, oy - 8, ox + nw + 8, oy + nh + 8), radius=16, fill=(255, 255, 255), outline=(56, 189, 248), width=3)
            frame.paste(s_raw.resize((nw, nh), Image.Resampling.LANCZOS), (ox, oy))

            raw_n = (p_info.get("narrations") or {}).get(lang_code) or p_info.get("explanation_text") or ""
            raw_n = re.sub(r"안녕하세요[^.?!]*[.?!]\s*", "", raw_n).strip()
            if is_en and re.search(r"[가-힣]", raw_n):
                raw_n = ""
            if not raw_n:
                raw_n = f"Step {idx_s}: Watch how the auxiliary geometry locks the equal quantities together." if is_en else "보조선에 의해 두 도형 요소의 크기가 자연스럽게 연결됩니다."
            s_mp3 = tmp_dir / f"long_step_{idx_s:02d}.mp3"
            s_mp4 = tmp_dir / f"long_step_{idx_s:02d}.mp4"
            vmaker.synthesize_tts_mp3_sync(raw_n, voice_name, s_mp3, rate="+8%")
            _encode_single_card_segment(frame, s_mp3, s_mp4, ffmpeg_exe, ffprobe_exe)
            long_segs.append(s_mp4)

        # Act 3: 실전 문제 5초 암산 완결 + 구독 전환 카드
        act3_img = Image.new("RGB", (1920, 1080), (8, 18, 32))
        d3 = ImageDraw.Draw(act3_img)
        d3.rounded_rectangle((56, 44, 1864, 156), radius=22, fill=(5, 150, 105), outline=(250, 204, 21), width=4)
        d3.text((88, 74), "◆ PROOF IN ONE LINE · GEOMETRIC INSIGHT" if is_en else "◆ 보조선 한 줄로 완성된 기하학적 통찰!", fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 42, bold=True))
        _draw_exam_problem_diagram(d3, (68, 196, 940, 880), bp["diagram_kind"], solved=True, canvas_img=act3_img, pdf_doc=doc, lang_code=lang_code)
        d3.rounded_rectangle((980, 196, 1852, 880), radius=24, fill=(15, 23, 42), outline=(52, 211, 153), width=4)
        ans_lbl = _clean_canvas_text(bp["answer_label_en"] if is_en else bp["answer_label_ko"])
        ya = 256
        for line in textwrap.wrap(ans_lbl, width=28 if is_en else 18)[:4]:
            d3.text((1024, ya), line, fill=(254, 240, 138), font=vmaker.get_font_for_lang(lang_code, 42, bold=True))
            ya += 64
        d3.rounded_rectangle((1024, 590, 1808, 820), radius=20, fill=(2, 132, 199), outline=(255, 255, 255), width=3)
        sub_h1 = "▶ Subscribe to @min7014_ai Right Now!" if is_en else "▶ 지금 바로 @min7014_ai [구독] 누르기!"
        sub_h2 = "See the deep visual logic behind geometry!" if is_en else "도형과 해석의 본질을 시각적 증명으로 만나보세요!"
        d3.text((1056, 636), sub_h1, fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 36, bold=True))
        d3.text((1056, 712), sub_h2, fill=(254, 240, 138), font=vmaker.get_font_for_lang(lang_code, 28, bold=True))

        act3_mp3 = tmp_dir / "long_act3.mp3"
        act3_seg = tmp_dir / "long_act3.mp4"
        vmaker.synthesize_tts_mp3_sync(bp["act3_en"] if is_en else bp["act3_ko"], voice_name, act3_mp3, rate="+8%")
        _encode_single_card_segment(act3_img, act3_mp3, act3_seg, ffmpeg_exe, ffprobe_exe)
        long_segs.append(act3_seg)

        concat_long = tmp_dir / "concat_long.txt"
        concat_long.write_text("\n".join(f"file '{p.as_posix()}'" for p in long_segs), encoding="utf-8")
        raw_long = tmp_dir / "raw_long.mp4"
        subprocess.run([ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_long), "-c", "copy", str(raw_long)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        _mix_ambient_bgm(raw_long, long_mp4, ffmpeg_exe)
        long_dur = vmaker.get_media_duration_seconds(long_mp4, ffprobe_exe)

        # ---------------- B. 1080x1920 9:16 Exam-Hybrid Q-#Shorts (32~42s 스와이프 방어 포맷) ----------------
        # Scene 1 (0~7초): 텍스트 과밀 ZERO! 초대형 실전 도형 + "x = ? 3초 안에 보이시나요?"
        sh_segs = []
        s1 = Image.new("RGB", (1080, 1920), (8, 13, 28))
        ds1 = ImageDraw.Draw(s1)
        ds1.rounded_rectangle((44, 68, 1036, 214), radius=24, fill=(2, 132, 199), outline=(250, 204, 21), width=4)
        if "AF:FB" in bp.get("figure_caption_en", ""):
            sh1_hdr = "★ CAN YOU FIND AF:FB IN 5 SECONDS?" if is_en else "★ 공식 없이 5초 안에 AF:FB가 보이시나요?"
        elif bp["diagram_kind"] == "pdf_native":
            sh1_hdr = "★ CAN YOU SPOT THE CLUE IN 3 SECONDS?" if is_en else "★ 공식 없이 3초 안에 핵심 단서가 보이시나요?"
        else:
            sh1_hdr = "★ CAN YOU FIND x IN 3 SECONDS?" if is_en else "★ 공식 없이 3초 안에 x가 보이시나요?"
        ds1.text((78, 110), sh1_hdr, fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 40 if "AF:FB" in sh1_hdr else 42, bold=True))
        _draw_exam_problem_diagram(ds1, (56, 250, 1024, 1210), bp["diagram_kind"], solved=False, canvas_img=s1, pdf_doc=doc, lang_code=lang_code)
        ds1.rounded_rectangle((56, 1248, 1024, 1600), radius=24, fill=(15, 23, 42), outline=(56, 189, 248), width=4)
        cap_sh = _clean_canvas_text(bp["figure_caption_en"] if is_en else bp["figure_caption_ko"])
        f_cap_sh = vmaker.get_font_for_lang(lang_code, 40, bold=True)
        for csh_sz in (40, 36, 32, 28, 25):
            f_csh_cand = vmaker.get_font_for_lang(lang_code, csh_sz, bold=True)
            cb_sh = ds1.textbbox((0, 0), cap_sh, font=f_csh_cand)
            if cb_sh[2] - cb_sh[0] <= 900:
                f_cap_sh = f_csh_cand
                break
        ds1.text((88, 1286), cap_sh, fill=(250, 204, 21), font=f_cap_sh)
        p_short_lines = textwrap.wrap(_clean_canvas_text(bp["problem_label_en"] if is_en else bp["problem_label_ko"]), width=32 if is_en else 24)[:3]
        for li, pl in enumerate(p_short_lines):
            ds1.text((88, 1368 + li * 56), pl, fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 33, bold=True))

        sh1_mp3 = tmp_dir / "sh1.mp3"
        sh1_seg = tmp_dir / "sh1.mp4"
        vmaker.synthesize_tts_mp3_sync(bp["act1_en"] if is_en else bp["act1_ko"], voice_name, sh1_mp3, rate="+18%")
        _encode_single_card_segment(s1, sh1_mp3, sh1_seg, ffmpeg_exe, ffprobe_exe)
        sh_segs.append(sh1_seg)

        # Scene 2 & 3: 핵심 원본 PDF 슬라이드 2장 (중간 단서 + 클라이맥스)
        pick_sh = [max(0, len(doc) // 2 - 1), max(0, len(doc) - 2)]
        for si, dp_i in enumerate(pick_sh, 2):
            pix_s = doc[dp_i].get_pixmap(dpi=230)
            sl_img = vmaker._mask_pdf_bottom_author_bar(Image.frombytes("RGB", [pix_s.width, pix_s.height], pix_s.samples))
            sc_v = Image.new("RGB", (1080, 1920), (10, 16, 34))
            dsc = ImageDraw.Draw(sc_v)
            dsc.rounded_rectangle((44, 68, 1036, 200), radius=22, fill=(2, 132, 199), outline=(254, 240, 138), width=3)
            dsc.text((78, 108), f"★ VISUAL CLUE {si-1}/2 — Watch the Auxiliary Line!" if is_en else f"★ 핵심 단서 {si-1}/2 — 보조선의 마법을 보세요!", fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 36, bold=True))
            k_scale = min(980 / sl_img.width, 1020 / sl_img.height)
            kw, kh = int(sl_img.width * k_scale), int(sl_img.height * k_scale)
            kx, ky = (1080 - kw) // 2, 260 + (1060 - kh) // 2
            dsc.rounded_rectangle((kx - 8, ky - 8, kx + kw + 8, ky + kh + 8), radius=18, fill=(255, 255, 255), outline=(56, 189, 248), width=4)
            sc_v.paste(sl_img.resize((kw, kh), Image.Resampling.LANCZOS), (kx, ky))

            p_match = pages[min(len(pages) - 1, dp_i)]
            clue_txt = ((p_match.get("narrations") or {}).get(lang_code) or ("" if is_en else p_match.get("explanation_text")) or "").strip()
            if is_en and re.search(r"[가-힣]", clue_txt):
                clue_txt = ""
            sents = [x.strip() for x in re.split(r"(?<=[.?!])\s+", clue_txt) if len(re.findall(r"[A-Za-z가-힣0-9]", x)) >= 8 and "안녕하세요" not in x]
            max_clue_chars = 145 if is_en else 84
            concise = [s for s in sents if len(s) <= max_clue_chars]
            short_clue = concise[-1] if concise else (sents[-1] if sents else ("One auxiliary line locks the equal angles together!" if is_en else "보조선 한 줄이 숨어 있던 합동과 대칭을 즉시 깨웁니다!"))
            cleaned_clue = _clean_canvas_text(short_clue)
            dsc.rounded_rectangle((44, 1356, 1036, 1648), radius=22, fill=(15, 23, 42), outline=(56, 189, 248), width=3)
            wrap_w_try = 33 if is_en else 21
            wrapped_clue = textwrap.wrap(cleaned_clue, width=wrap_w_try)
            if len(wrapped_clue) <= 3:
                font_sz, line_h = 33, 48
            elif len(textwrap.wrap(cleaned_clue, width=39 if is_en else 25)) <= 5:
                font_sz, line_h = 28, 42
                wrapped_clue = textwrap.wrap(cleaned_clue, width=39 if is_en else 25)
            else:
                font_sz, line_h = 24, 36
                wrapped_clue = textwrap.wrap(cleaned_clue, width=45 if is_en else 29)
            f_clue = vmaker.get_font_for_lang(lang_code, font_sz, bold=True)
            total_text_h = len(wrapped_clue) * line_h
            start_y = 1356 + max(24, (1648 - 1356 - total_text_h) // 2)
            for li, cl_l in enumerate(wrapped_clue):
                dsc.text((80, start_y + li * line_h), cl_l, fill=(255, 255, 255), font=f_clue)

            sh_m_mp3 = tmp_dir / f"sh_{si}.mp3"
            sh_m_seg = tmp_dir / f"sh_{si}.mp4"
            vmaker.synthesize_tts_mp3_sync(short_clue, voice_name, sh_m_mp3, rate="+18%")
            _encode_single_card_segment(sc_v, sh_m_mp3, sh_m_seg, ffmpeg_exe, ffprobe_exe)
            sh_segs.append(sh_m_seg)

        # Scene 4: 5초 정답 완결 + 하단 @min7014_ai 구독 & 관련 동영상 클릭 CTA
        s4 = Image.new("RGB", (1080, 1920), (8, 20, 34))
        ds4 = ImageDraw.Draw(s4)
        ds4.rounded_rectangle((44, 68, 1036, 204), radius=24, fill=(5, 150, 105), outline=(250, 204, 21), width=4)
        ds4.text((78, 110), "★ BOOM! 5-SECOND EXAM PAYOFF!" if is_en else "★ 유레카! 보조선 1줄로 5초 암산 끝!", fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 40, bold=True))
        _draw_exam_problem_diagram(ds4, (56, 244, 1024, 1140), bp["diagram_kind"], solved=True, canvas_img=s4, pdf_doc=doc, lang_code=lang_code)
        ds4.rounded_rectangle((44, 1180, 1036, 1590), radius=24, fill=(15, 23, 42), outline=(52, 211, 153), width=4)
        for li, al in enumerate(textwrap.wrap(_clean_canvas_text(bp["answer_label_en"] if is_en else bp["answer_label_ko"]), width=28 if is_en else 19)[:3]):
            ds4.text((80, 1222 + li * 56), al, fill=(254, 240, 138), font=vmaker.get_font_for_lang(lang_code, 38, bold=True))
        ds4.rounded_rectangle((72, 1430, 1008, 1560), radius=18, fill=(2, 132, 199))
        cta_b = "▶ Tap Related Video & Hit [Subscribe] @min7014_ai!" if is_en else "▶ 아래 [관련 동영상] 풀버전 클릭 & [@min7014_ai 구독]!"
        ds4.text((98, 1474), cta_b, fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 31, bold=True))

        sh4_mp3 = tmp_dir / "sh4.mp3"
        sh4_seg = tmp_dir / "sh4.mp4"
        vmaker.synthesize_tts_mp3_sync(bp["act3_en"] if is_en else bp["act3_ko"], voice_name, sh4_mp3, rate="+18%")
        _encode_single_card_segment(s4, sh4_mp3, sh4_seg, ffmpeg_exe, ffprobe_exe)
        sh_segs.append(sh4_seg)

        concat_sh = tmp_dir / "concat_sh.txt"
        concat_sh.write_text("\n".join(f"file '{p.as_posix()}'" for p in sh_segs), encoding="utf-8")
        raw_sh = tmp_dir / "raw_sh.mp4"
        subprocess.run([ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_sh), "-c", "copy", str(raw_sh)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        _mix_ambient_bgm(raw_sh, short_mp4, ffmpeg_exe)
        short_dur = vmaker.get_media_duration_seconds(short_mp4, ffprobe_exe)
        if short_dur >= 46.0:
            spd = min(1.85, round(short_dur / 39.0, 3))
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

        # 스크립트 JSON에 메타데이터 기록
        sdoc.setdefault("exam_hybrid_packages", {})[lang_code] = {
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
        return sdoc["exam_hybrid_packages"][lang_code]
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        doc.close()


def get_all_ranked_exam_blueprints(max_dynamic: int = 120) -> list[dict]:
    """
    [0-크레딧 무한 확장 엔진]:
    수동 설계 6대 블루프린트 완료 후에도 멈추지 않고, min7014.github.io 전체 847개 시각 증명 PDF 중
    youtube_self_evolving_engine의 다윈식 승자 클러스터 가중치가 높은 핵심 주제들을 자동으로 실전 함정 블루프린트로 합성합니다.
    """
    curated_slugs = {b["slug"] for b in EXAM_TRAP_BLUEPRINTS}
    result = list(EXAM_TRAP_BLUEPRINTS)

    try:
        import min7014_video_maker as vm
        import youtube_self_evolving_engine as ysee

        dyn_cands = []
        for sp in sorted(SCRIPTS_DIR.glob("*.json")):
            if sp.stem in curated_slugs:
                continue
            try:
                sdoc = json.loads(sp.read_text(encoding="utf-8"))
            except Exception:
                continue
            pdf_u = str(sdoc.get("pdf_url") or "")
            if not (pdf_u.lower().endswith(".pdf") and "min7014.github.io" in pdf_u.lower()):
                continue
            pages = sdoc.get("pages") or []
            if not (6 <= len(pages) <= 32):
                continue
            raw_t = str(sdoc.get("title") or "")
            if any(skip in raw_t for skip in ("특강", "워크숍", "직무연수", "TikZ", "학년도")):
                continue
            boost = ysee.get_slug_cluster_boost(f"{raw_t} {sdoc.get('title_en', '')}")
            dyn_cands.append((-boost, abs(len(pages) - 14), sp.stem, sdoc))

        dyn_cands.sort(key=lambda x: (x[0], x[1], x[2]))
        for _, _, slug, sdoc in dyn_cands[:max_dynamic]:
            ko_t, en_t = vm.split_bilingual_title(sdoc.get("title", ""))
            ko_c = vm._smart_concise_topic_title(vm.latex_to_unicode_title(ko_t).strip(), max_len=26, lang="ko")
            en_c = vm._smart_concise_topic_title(vm.latex_to_unicode_title((sdoc.get("title_en") or en_t or ko_c).split("—")[0].strip()), max_len=38, lang="en")
            p0 = (sdoc.get("pages") or [{}])[0]
            p_last = (sdoc.get("pages") or [{}])[-1]
            q0_ko = (p0.get("step_question_ko") or f"도형에서 어떤 보조선 한 줄이 {ko_c}을 즉시 증명할까요?").strip()
            q0_en = (p0.get("step_question_en") or f"Which single auxiliary line unlocks {en_c} in seconds?").strip()
            end_ko = re.sub(r"\s+", " ", (p_last.get("narrations") or {}).get("ko") or p_last.get("explanation_text") or "").strip()[:76]
            end_en = re.sub(r"\s+", " ", (p_last.get("narrations") or {}).get("en") or "").strip()[:115]

            result.append({
                "slug": slug,
                "diagram_kind": "pdf_native",
                "exam_badge_ko": "◆ 유클리드 아틀리에 · 시각적 증명",
                "exam_badge_en": "◆ Euclid Visual Proof Archive",
                "problem_label_ko": q0_ko[:68],
                "problem_label_en": q0_en[:96],
                "figure_caption_ko": ko_c,
                "figure_caption_en": en_c,
                "answer_label_ko": end_ko or f"보조선과 기하 불변량으로 [{ko_c}] 원리 완전 증명!",
                "answer_label_en": end_en or f"One visual auxiliary clue illuminates [{en_c}] completely!",
                "title_ko": f"✨ 공식 너머의 필연성! 보조선과 대칭으로 읽는 기하 직관 | {ko_c} 시각적 증명",
                "title_en": f"✨ Beyond Rote Formulas—See Why It Must Hold | {en_c} Visual Proof",
                "short_title_ko": f"❓ 공식 없이 눈으로 보이시나요? {ko_c} 시각적 통찰! #Shorts",
                "short_title_en": f"❓ Can You Spot Why {en_c} Works Visually? #Shorts",
                "act1_ko": f"잠깐! {ko_c} 관련 원리를 공식으로만 외우면 조금만 조건이 달라져도 흐름을 놓치기 쉽습니다. 도형 속 핵심 단서가 눈앞에 보이시나요?",
                "act1_en": f"Wait! Memorizing {en_c} blindly hides why it is true whenever conditions shift. Can you spot the visual invariant directly?",
                "act3_ko": f"결국 이 시각적 원리 하나로 {ko_c}의 필연성이 눈앞에서 명쾌하게 증명됩니다! 수학의 본질을 그림으로 깨치는 시각 증명 아틀리에, 지금 바로 채널 구독을 눌러 두세요!",
                "act3_en": f"That single visual connection illuminates {en_c} effortlessly! Subscribe to @min7014_ai right now for timeless visual proofs!",
                "comment_quiz_ko": f"🧩 [시각 원리 체크] 오늘 본 '{ko_c}' 증명에서 가장 결정적이었던 보조선·성질은 무엇이었나요? 한 줄로 댓글에 남겨 복습해 보세요! 👇",
                "comment_quiz_en": f"🧩 [Visual Recap] Which visual step made '{en_c}' click for you? Share in the comments below! 👇",
            })
    except Exception:
        pass
    return result


def ensure_next_exam_hybrid_rendered(max_bundles: int = 1) -> list[dict]:
    rendered = []
    try:
        import youtube_self_evolving_engine as _ysee
        lang_order = _ysee.preferred_lang_order_for_current_hour()
    except Exception:
        lang_order = ("ko", "en")
    for bp in get_all_ranked_exam_blueprints():
        slug = bp["slug"]
        for lc in lang_order:
            l_mp4 = EXAM_HYBRID_DIR / f"{slug}_exam_{lc}.mp4"
            s_mp4 = EXAM_HYBRID_DIR / f"{slug}_exam_short_{lc}.mp4"
            if not (l_mp4.exists() and s_mp4.exists()):
                pkg = render_exam_hybrid_bundle(bp, lang_code=lc)
                rendered.append({"slug": slug, "lang": lc, **pkg})
                if len(rendered) >= max_bundles:
                    return rendered
    return rendered


def _safe_notify_telegram(kind_label: str, slug: str, lc: str, title: str, url: str):
    try:
        import sys
        subprocess.run(
            [
                sys.executable, "-X", "utf8",
                str(ROOT_DIR / "mathedu_telegram_bridge.py"),
                "--reply",
                f"🎯 [유클리드 아틀리에 하이브리드 자동 발행 완료 ({kind_label} · {lc.upper()})]\n• 주제({slug}): {title}\n• 링크: {url}",
            ],
            cwd=str(ROOT_DIR),
            timeout=20,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass


def sync_pending_policy87_live_assets(yt=None, tok_path=None, max_ops: int = 6) -> dict:
    """
    Policy 87 self-healing sync hook: once daily YouTube Data API quota resets,
    gradually updates any remaining live exam_hybrid titles/thumbnails and BkxSXat12V4
    in-place without deleting videos (Rule 33). Stops cleanly on quota limit or max_ops.
    """
    import re
    import auditor
    import min7014_video_maker as vmaker
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload

    state_path = EXAM_HYBRID_DIR / "_policy87_live_sync_state.json"
    state = {"completed": False, "done_thumbs": [], "done_titles": []}
    if state_path.exists():
        try:
            loaded = json.loads(state_path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                state.update(loaded)
        except Exception:
            pass
    if state.get("completed"):
        return {}

    if yt is None:
        yt, tok_path = vmaker.get_available_youtube_upload_service()
    if yt is None:
        return {}

    done_thumbs = set(state.get("done_thumbs") or [])
    done_titles = set(state.get("done_titles") or [])
    legacy_title_tokens = ("시험장", "함정", "하수", "5초", "Stop Memorizing", "90%", "Trap", "Hack")

    def _has_legacy(text: str) -> bool:
        return any(tok in (text or "") for tok in legacy_title_tokens)

    def _clean_desc(desc: str, is_en: bool) -> str:
        repl = "Beyond Formulas—One Visual Proof" if is_en else "공식 너머의 필연성, 보조선 한 줄의 통찰"
        out = re.sub(
            r"시험장\s*90%\s*(?:함정)?!?|90%\s*함정!?|보조선\s*1줄\s*5초\s*컷!?|90%\s*MISS\s*THIS!?|SOLVE\s+\S+\s+IN\s+5s!?|쓰면\s*하수!?|실\s*전함정|Visual\s*Hack",
            repl,
            desc or "",
            flags=re.IGNORECASE,
        )
        return out

    def _is_quota_exc(exc: Exception) -> bool:
        msg = str(exc)
        return ("quotaExceeded" in msg) or ("uploadLimitExceeded" in msg) or ("dailyLimitExceeded" in msg)

    ops_used = 0
    titles_updated = 0
    thumbs_updated = 0
    stopped_early = False
    quota_hit = False

    # Build candidate queue: BkxSXat12V4 first, then all blueprints with live exam_hybrid_urls
    candidates = [{
        "slug": "2012093001",
        "lang": "ko",
        "vid": "BkxSXat12V4",
        "title": "✨ 왜 방정식 없이 풀릴까? 원주각을 단번에 여는 보조선 한 줄의 통찰 | 원주각과 중심각 시각적 증명",
        "thumb": EXAM_HYBRID_DIR / "2012093001_exam_ko_thumb.png",
    }]
    seen_vids = {"BkxSXat12V4"}
    for bp in get_all_ranked_exam_blueprints(max_dynamic=1000):
        slug = bp["slug"]
        sp = SCRIPTS_DIR / f"{slug}.json"
        if not sp.exists():
            continue
        try:
            sdoc = json.loads(sp.read_text(encoding="utf-8"))
        except Exception:
            continue
        for lc, url in (sdoc.get("exam_hybrid_urls") or {}).items():
            vid = vmaker.extract_youtube_video_id(url)
            if not vid or vid in seen_vids:
                continue
            seen_vids.add(vid)
            is_en = lc == "en"
            candidates.append({
                "slug": slug,
                "lang": lc,
                "vid": vid,
                "title": bp["title_en"] if is_en else bp["title_ko"],
                "thumb": EXAM_HYBRID_DIR / f"{slug}_exam_{lc}_thumb.png",
            })

    need_snippet_ids = [c["vid"] for c in candidates if c["vid"] not in done_titles]
    live_snippets = {}
    for i in range(0, len(need_snippet_ids), 50):
        chunk = need_snippet_ids[i:i + 50]
        try:
            resp = yt.videos().list(part="snippet", id=",".join(chunk)).execute()
            for item in resp.get("items", []):
                live_snippets[item["id"]] = item.get("snippet", {})
        except HttpError as exc:
            if _is_quota_exc(exc):
                if tok_path:
                    vmaker.mark_token_quota_exhausted(tok_path, 3600)
                vmaker._LAST_UPLOAD_QUOTA_BLOCKED = True
                quota_hit = True
                stopped_early = True
                break
        except Exception:
            stopped_early = True

    try:
        for cand in candidates:
            if quota_hit or ops_used >= max_ops:
                stopped_early = True
                break
            vid = cand["vid"]
            is_en = cand["lang"] == "en"

            if vid not in done_titles:
                snip = live_snippets.get(vid)
                if snip is not None:
                    live_t = snip.get("title", "")
                    live_d = snip.get("description", "")
                    if not _has_legacy(live_t) and not _has_legacy(live_d):
                        done_titles.add(vid)
                    else:
                        new_desc = _clean_desc(live_d, is_en)
                        raw_tags = [t for t in (snip.get("tags") or []) if not _has_legacy(t)]
                        try:
                            gated = auditor.sanitize_and_gate_upload_payload(cand["title"], new_desc, raw_tags)
                            final_t = gated.get("title") or cand["title"]
                            final_d = gated.get("description") or new_desc
                            final_tags = gated.get("tags") if gated.get("tags") is not None else raw_tags
                        except Exception:
                            final_t = vmaker.sanitize_youtube_title(cand["title"])
                            final_d = new_desc
                            final_tags = raw_tags
                        body_snip = {
                            "title": final_t[:100].replace("<", "＜").replace(">", "＞"),
                            "description": final_d[:4900],
                            "categoryId": snip.get("categoryId") or "27",
                        }
                        if final_tags:
                            body_snip["tags"] = final_tags
                        if snip.get("defaultLanguage"):
                            body_snip["defaultLanguage"] = snip["defaultLanguage"]
                        if snip.get("defaultAudioLanguage"):
                            body_snip["defaultAudioLanguage"] = snip["defaultAudioLanguage"]
                        try:
                            yt.videos().update(part="snippet", body={"id": vid, "snippet": body_snip}).execute()
                            ops_used += 1
                            titles_updated += 1
                            done_titles.add(vid)
                        except HttpError as exc:
                            if _is_quota_exc(exc):
                                if tok_path:
                                    vmaker.mark_token_quota_exhausted(tok_path, 3600)
                                vmaker._LAST_UPLOAD_QUOTA_BLOCKED = True
                                quota_hit = True
                                stopped_early = True
                                break
                            stopped_early = True

            if quota_hit or ops_used >= max_ops:
                stopped_early = True
                break

            if vid not in done_thumbs:
                tp = cand["thumb"]
                if not tp.exists():
                    continue
                try:
                    yt.thumbnails().set(
                        videoId=vid,
                        media_body=MediaFileUpload(str(tp), mimetype="image/png"),
                    ).execute()
                    ops_used += 1
                    thumbs_updated += 1
                    done_thumbs.add(vid)
                except HttpError as exc:
                    if _is_quota_exc(exc):
                        if tok_path:
                            vmaker.mark_token_quota_exhausted(tok_path, 3600)
                        vmaker._LAST_UPLOAD_QUOTA_BLOCKED = True
                        quota_hit = True
                        stopped_early = True
                        break
                    stopped_early = True

        all_done = (not stopped_early) and (not quota_hit) and all(
            (c["vid"] in done_titles) and (c["vid"] in done_thumbs)
            for c in candidates
            if c["thumb"].exists()
        )
        state["completed"] = bool(all_done)
    finally:
        state["done_thumbs"] = sorted(done_thumbs)
        state["done_titles"] = sorted(done_titles)
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "titles_updated": titles_updated,
        "thumbs_updated": thumbs_updated,
        "ops_used": ops_used,
        "completed": state["completed"],
    }


def try_upload_one_exam_hybrid(kind: str = "long") -> dict | None:
    """
    finance.py 황금비 엔진 연동용 업로더:
    kind == 'long'  : 미업로드 Exam-Hybrid 1080p 본편 1편 업로드 + 5초 암산 고정댓글 등록
    kind == 'short' : 본편이 업로드된 Exam-Hybrid Q-#Shorts 1편 업로드 + 스튜디오 관련 동영상 자동 연결
    """
    import min7014_video_maker as vmaker
    from googleapiclient.http import MediaFileUpload

    if vmaker._LAST_UPLOAD_QUOTA_BLOCKED:
        return None
    yt, tok_path = vmaker.get_available_youtube_upload_service()
    if yt is None:
        return None

    if kind == "long":
        try:
            sync_pending_policy87_live_assets(yt=yt, tok_path=tok_path, max_ops=6)
        except Exception:
            pass
        if vmaker._LAST_UPLOAD_QUOTA_BLOCKED:
            return None

    try:
        import youtube_self_evolving_engine as _ysee
        lang_order = _ysee.preferred_lang_order_for_current_hour()
    except Exception:
        lang_order = ("ko", "en")

    for bp in get_all_ranked_exam_blueprints():
        slug = bp["slug"]
        sp = SCRIPTS_DIR / f"{slug}.json"
        if not sp.exists():
            continue
        sdoc = json.loads(sp.read_text(encoding="utf-8"))
        ex_urls = sdoc.setdefault("exam_hybrid_urls", {})
        ex_sh_urls = sdoc.setdefault("exam_hybrid_shorts_urls", {})

        for lc in lang_order:
            is_en = lc == "en"
            l_mp4 = EXAM_HYBRID_DIR / f"{slug}_exam_{lc}.mp4"
            l_thumb = EXAM_HYBRID_DIR / f"{slug}_exam_{lc}_thumb.png"
            s_mp4 = EXAM_HYBRID_DIR / f"{slug}_exam_short_{lc}.mp4"

            if kind == "long" and not (ex_urls.get(lc) or "").strip():
                if not l_mp4.exists():
                    render_exam_hybrid_bundle(bp, lang_code=lc)
                if not l_mp4.exists():
                    continue
                raw_title = bp["title_en"] if is_en else bp["title_ko"]
                pdf_url = sdoc.get("pdf_url") or "https://min7014.github.io/"
                raw_desc = (
                    f"✨ See why this timeless geometry & algebra theorem holds through pure visual intuition!\n"
                    f"📐 100% Original Visual Proof PDF: {pdf_url}\n"
                    f"🌐 Interactive Math Lab & Step-by-Step Archive: https://min7014.github.io/mathedu/\n"
                    f"🔔 Subscribe to @min7014_ai: https://www.youtube.com/@min7014_ai?sub_confirmation=1\n\n"
                    f"#VisualProof #EuclideanGeometry #MathIntuition #GeometryProof #Mathematics"
                    if is_en
                    else f"✨ 공식 암기 대신 보조선 한 줄과 기하 불변량으로 원리의 필연성을 눈으로 증명합니다!\n"
                    f"📐 100% 자체 제작 단계별 시각 증명 PDF: {pdf_url}\n"
                    f"🌐 단계별 디딤돌 & 자체 제작 MathLab 실습: https://min7014.github.io/mathedu/\n"
                    f"🔔 @min7014_ai 무료 구독하기: https://www.youtube.com/@min7014_ai?sub_confirmation=1\n\n"
                    f"#시각적증명 #도형보조선 #기하학원리 #수학직관 #고등수학"
                )
                raw_tags = ["Visual Math Proof", "Geometry Proof", "Euclidean Geometry", "Math Intuition"] if is_en else ["시각적증명", "도형보조선", "기하학증명", "수학원리", "원주각"]
                import auditor as _aud
                gated = _aud.sanitize_and_gate_upload_payload(raw_title, raw_desc, raw_tags)
                title = vmaker.sanitize_youtube_title(gated["title"])
                desc = gated["description"]
                body = {
                    "snippet": {
                        "title": title,
                        "description": desc,
                        "tags": gated["tags"],
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
                    try:
                        yt.commentThreads().insert(
                            part="snippet",
                            body={"snippet": {"videoId": vid, "topLevelComment": {"snippet": {"textOriginal": bp["comment_quiz_en"] if is_en else bp["comment_quiz_ko"]}}}},
                        ).execute()
                    except Exception:
                        pass
                    url = f"https://youtu.be/{vid}"
                    ex_urls[lc] = url
                    sp.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
                    _safe_notify_telegram("1080p 본편", slug, lc, title, url)
                    return {"type": "exam_hybrid_1080p", "slug": slug, "lang": lc, "url": url, "title": title}
                except Exception as e:
                    if "uploadLimitExceeded" in str(e) or "quotaExceeded" in str(e) or "rateLimitExceeded" in str(e):
                        vmaker.mark_token_quota_exhausted(tok_path, 900)
                    return None

            if kind == "short" and (ex_urls.get(lc) or "").strip() and not (ex_sh_urls.get(lc) or "").strip():
                if not s_mp4.exists():
                    render_exam_hybrid_bundle(bp, lang_code=lc)
                if not s_mp4.exists():
                    continue
                sh_title = vmaker.sanitize_youtube_title(bp["short_title_en"] if is_en else bp["short_title_ko"])
                long_u = ex_urls[lc]
                desc_sh = (
                    f"🎬 Watch Full 5-Sec Visual Proof Breakdown (1080p): {long_u}\n"
                    f"🔔 Subscribe @min7014_ai for daily original visual math proofs!\n#Shorts #VisualProof #GeometryProof #MathPuzzle"
                    if is_en
                    else f"🎬 1080p 5초 보조선 해체 풀버전 바로 보기: {long_u}\n"
                    f"🔔 도형·미적분 10초 눈풀이 @min7014_ai 구독!\n#Shorts #시각적증명 #도형보조선 #수학퀴즈"
                )
                body_sh = {
                    "snippet": {
                        "title": sh_title,
                        "description": desc_sh,
                        "tags": ["Shorts", "Math Puzzle", "Visual Math", "Geometry Proof"] if is_en else ["Shorts", "수학쇼츠", "시각적증명", "보조선"],
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
                    try:
                        yt.commentThreads().insert(
                            part="snippet",
                            body={"snippet": {"videoId": vid, "topLevelComment": {"snippet": {"textOriginal": bp["comment_quiz_en"] if is_en else bp["comment_quiz_ko"]}}}},
                        ).execute()
                    except Exception:
                        pass
                    url = f"https://youtube.com/shorts/{vid}"
                    ex_sh_urls[lc] = url
                    sp.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
                    try:
                        import youtube_community_controller as _ycc
                        _ycc.link_shorts_related_videos_in_studio(max_links=2, headless=True)
                    except Exception:
                        pass
                    _safe_notify_telegram("Q-#Shorts", slug, lc, sh_title, url)
                    return {"type": "exam_hybrid_short", "slug": slug, "lang": lc, "url": url, "title": sh_title}
                except Exception as e:
                    if "uploadLimitExceeded" in str(e) or "quotaExceeded" in str(e) or "rateLimitExceeded" in str(e):
                        vmaker.mark_token_quota_exhausted(tok_path, 900)
                    return None
    return None


if __name__ == "__main__":
    import sys
    cnt = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    out = ensure_next_exam_hybrid_rendered(max_bundles=cnt)
    print(json.dumps(out, ensure_ascii=False, indent=2))
