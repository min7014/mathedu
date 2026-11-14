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
# [Strategy 4 · Rule 49] 실전 내신·수능/SAT 함정 1문제 ➔ min7014 보조선 1줄 10초 해체 블루프린트
# - 모든 증명의 수학적 원리는 100% https://min7014.github.io/ 원문 PDF 슬라이드(Act 2)에 기반합니다.
# - Act 1(실전 수치 함정 문제 제시) ➔ Act 2(원문 플립북 시각 증명) ➔ Act 3(5초 암산 완결 & 구독 유도)
# ==============================================================================
EXAM_TRAP_BLUEPRINTS = [
    {
        "slug": "2012093001",
        "diagram_kind": "circle_inscribed",
        "exam_badge_ko": "🚨 내신·수능 도형 4점 단골 함정",
        "exam_badge_en": "🚨 SAT & Geometry Exam Trap",
        "problem_label_ko": "중심각 ∠AOB = 84°일 때, 원 위를 움직이는 점 P에 대하여 x = ∠APB는?",
        "problem_label_en": "Given central angle ∠AOB = 84°, find x = ∠APB for point P on the circle!",
        "figure_caption_ko": "∠AOB = 84°,  ∠APB = x = ?",
        "figure_caption_en": "∠AOB = 84°,  ∠APB = x = ?",
        "answer_label_ko": "보조선 PO 1줄 ➔ 이등변삼각형 2개!  x = 84° ÷ 2 = 42° (5초 컷!)",
        "answer_label_en": "1 Line PO ➔ Two Isosceles Triangles!  x = 84° ÷ 2 = 42° (5s Solve!)",
        "title_ko": "🔥 시험장 90%가 3분 헤매는 원주각 함정, 보조선 1줄로 5초 컷! | 원주각과 중심각 시각적 증명",
        "title_en": "🔥 90% Waste 3 Minutes on This Circle Angle Trap—Solve x in 5 Seconds! | Inscribed Angle Proof",
        "short_title_ko": "❓ x가 몇 도인지 3초 만에 보이시나요? 원주각 함정 보조선 1줄 해법! #Shorts",
        "short_title_en": "❓ Can You Find Angle x in 3 Seconds? One Hidden Radius Trick! #Shorts",
        "act1_ko": "잠깐! 시험장에서 중심각이 84도일 때 비스듬히 꺾인 이 각 x를 연립방정식으로 풀면 3분이 날아갑니다. 공식 암기 없이 보조선 딱 한 줄로 5초 만에 보이시나요?",
        "act1_en": "Stop! In an exam, setting up algebra for angle x when the central angle is 84 degrees wastes three minutes. Can you see why one hidden line solves x in five seconds?",
        "act3_ko": "이제 처음 시험 문제로 돌아와 볼까요? 점 P와 중심 O를 잇는 지름 보조선 한 줄이면 두 이등변삼각형의 외각이 되어 x는 84도의 절반, 정답 42도가 5초 만에 튀어나옵니다! 내신과 수능 도형 4점 문항을 10초 눈풀이로 바꾸는 시각 증명, 지금 바로 채널 구독을 눌러 다음 실전 해법도 놓치지 마세요!",
        "act3_en": "Now back to our exam problem! Drawing the single diameter through P and O splits angle x into two isosceles exterior halves—so x is half of 84, which is 42 degrees in five seconds flat! Subscribe right now so you never miss our daily 10-second visual exam hacks!",
        "comment_quiz_ko": "🧩 [5초 실전 암산 테스트] 만약 중심각 ∠AOB = 116°라면 원주각 x는 몇 도일까요? 암산한 정답을 댓글로 남겨보세요! 👇",
        "comment_quiz_en": "🧩 [5-Sec Exam Check] If central angle ∠AOB = 116°, what is angle x? Drop your mental-math answer in the comments! 👇",
    },
    {
        "slug": "2012100303",
        "diagram_kind": "tangent_chord",
        "exam_badge_ko": "🚨 고1·수능 원과 접선 킬러 함정",
        "exam_badge_en": "🚨 High-Yield Circle Tangent Trap",
        "problem_label_ko": "접선 AT와 현 AB가 이루는 각이 58°일 때, 원주 위 ∠ACB = x는?",
        "problem_label_en": "Tangent AT and chord AB form 58°. Find inscribed angle ∠ACB = x!",
        "figure_caption_ko": "접선각 ∠BAT = 58°,  ∠ACB = x = ?",
        "figure_caption_en": "Tangent ∠BAT = 58°,  ∠ACB = x = ?",
        "answer_label_ko": "지름 보조선 AD 1줄 ➔ 90° 직각 대칭!  x = 58° 그대로 일치!",
        "answer_label_en": "1 Diameter Line AD ➔ Right-Angle Match!  x = 58° Instantly!",
        "title_ko": "⚡ 접선만 나오면 막히는 이유! 지름 보조선 1줄로 x=58° 5초 해체 | 접현각의 정리 시각적 증명",
        "title_en": "⚡ Stuck on Circle Tangents? One Diameter Solves x in 5 Seconds! | Alternate Segment Theorem",
        "short_title_ko": "❓ 접선 각도가 58°일 때 저 위쪽 각 x는? 보조선 1줄 3초 해법! #Shorts",
        "short_title_en": "❓ Tangent Angle Is 58°—What Is x? 3-Second Diameter Trick! #Shorts",
        "act1_ko": "원과 접선이 만나 이루는 각이 58도일 때, 멀리 떨어진 원주 위의 각 x는 몇 도일까요? 공식을 깜빡해도 지름 보조선 딱 한 줄이면 5초 만에 끝납니다!",
        "act1_en": "When a tangent and chord meet at 58 degrees, what is angle x across the circle? Even if you forget the formula, one diameter line solves it in five seconds!",
        "act3_ko": "실전 문제에 그대로 적용하면 접점을 지나는 지름 보조선 한 줄로 직각 90도에서 같은 여각을 빼 주므로 x는 58도와 정확히 일치합니다! 시험장 도형 킬러를 눈으로 푸는 시각 증명, 지금 바로 구독 버튼을 눌러 두세요!",
        "act3_en": "Applying that diameter line to our exam trap subtracts the exact same complement from 90 degrees—so x equals 58 degrees immediately! Hit Subscribe right now to master visual geometry for every exam!",
        "comment_quiz_ko": "🧩 [5초 실전 암산] 접선과 현이 이루는 각이 67°라면 호 반대편 원주각 x는 몇 도일까요? 댓글로 남겨보세요! 👇",
        "comment_quiz_en": "🧩 [5-Sec Check] If the tangent-chord angle is 67°, what is angle x across the chord? Comment below! 👇",
    },
    {
        "slug": "2017090101",
        "diagram_kind": "pythagoras_squares",
        "exam_badge_ko": "🚨 중·고등 도형 넓이 단골 함정",
        "exam_badge_en": "🚨 Classic Exam Area Trap",
        "problem_label_ko": "직각삼각형 두 변 위 정사각형 넓이가 9와 16일 때, 빗변 정사각형 넓이 x는?",
        "problem_label_en": "Two leg squares have areas 9 and 16. Find hypotenuse square area x!",
        "figure_caption_ko": "넓이 S₁ = 9, S₂ = 16  ➔  빗변 정사각형 S₃ = x = ?",
        "figure_caption_en": "Areas S₁ = 9, S₂ = 16  ➔  Hypotenuse Square x = ?",
        "answer_label_ko": "루트 계산 ZERO! 등적변형 넓이 이동으로 x = 9 + 16 = 25 (3초 컷!)",
        "answer_label_en": "Zero Square Roots Needed! Shear Area Shift ➔ x = 9 + 16 = 25!",
        "title_ko": "🔥 루트 계산 쓰면 하수! 넓이 이동만으로 빗변 넓이 3초 암산법 | 피타고라스 정리 시각적 증명",
        "title_en": "🔥 Stop Taking Square Roots! 3-Second Area Shift Trick | Pythagorean Theorem Visual Proof",
        "short_title_ko": "❓ 루트 없이 3초 만에 넓이 x가 보이시나요? 피타고라스 넓이 이동 해법! #Shorts",
        "short_title_en": "❓ Can You Find Area x in 3 Seconds Without Roots? Visual Proof! #Shorts",
        "act1_ko": "잠깐! 이 문제에서 변의 길이를 루트로 구한 뒤 다시 제곱하고 계신가요? 유클리드의 넓이 미끄럼틀 원리를 알면 루트 계산 없이 3초 만에 끝납니다!",
        "act1_en": "Wait! Are you still computing side lengths and squaring them back? With Euclid's area-shearing proof, you can spot x in three seconds with zero square roots!",
        "act3_ko": "두 작은 정사각형 넓이 9와 16이 수선을 기준으로 빗변 정사각형의 왼쪽과 오른쪽 직사각형으로 그대로 흘러 들어가므로 x는 9 더하기 16, 정답 25입니다! 공식 너머의 진짜 직관, 지금 바로 구독하고 매일 받아보세요!",
        "act3_en": "Areas 9 and 16 shear directly into the two rectangles of the hypotenuse square—so x is simply 9 plus 16 equals 25! Subscribe now for daily visual math breakthroughs!",
        "comment_quiz_ko": "🧩 [3초 암산] 빗변 정사각형 넓이가 40이고 한쪽 작은 정사각형 넓이가 13이면 나머지 정사각형 넓이는? 댓글로 남겨보세요! 👇",
        "comment_quiz_en": "🧩 [3-Sec Check] If the hypotenuse square has area 40 and one leg square is 13, what is the other leg square's area? 👇",
    },
    {
        "slug": "2017090405",
        "diagram_kind": "isosceles_bisector",
        "exam_badge_ko": "🚨 중2·수능 기하 각도 추론 단골",
        "exam_badge_en": "🚨 Exam Triangle Angle Trap",
        "problem_label_ko": "AB = AC인 삼각형에서 꼭지각 ∠A = 36°일 때, 밑각 ∠B = x는?",
        "problem_label_en": "In triangle ABC with AB = AC and ∠A = 36°, find base angle x = ∠B!",
        "figure_caption_ko": "AB = AC,  ∠A = 36°  ➔  ∠B = x = ?",
        "figure_caption_en": "AB = AC,  ∠A = 36°  ➔  ∠B = x = ?",
        "answer_label_ko": "꼭지각 이등분선 1줄 ➔ 완벽 대칭 합동!  x = (180°-36°)÷2 = 72°!",
        "answer_label_en": "1 Angle Bisector ➔ Mirror SAS Congruence!  x = (180°-36°)÷2 = 72°!",
        "title_ko": "⚡ 이등변삼각형 문제마다 쓰이는 '보조선 1줄'의 비밀! 황금삼각형 72° 5초 해법 | 시각적 증명",
        "title_en": "⚡ The One Auxiliary Line Behind Every Isosceles Exam Problem! | Base Angles Visual Proof",
        "short_title_ko": "❓ 꼭지각 36°일 때 밑각 x와 숨은 대칭선 1줄, 3초 만에 보이시나요? #Shorts",
        "short_title_en": "❓ Vertex Angle 36°—Spot Base Angle x & the Hidden Mirror Line in 3s! #Shorts",
        "act1_ko": "이등변삼각형 응용 문제에서 막힐 때 1순위로 그어야 할 단 한 줄의 보조선은 어디일까요? 꼭지각이 36도인 황금삼각형 예제로 5초 만에 확인해 보세요!",
        "act1_en": "Whenever an isosceles triangle problem blocks you on an exam, what is the number-one auxiliary line to draw first? Let's unlock it in five seconds!",
        "act3_ko": "꼭지각 36도를 반으로 가르는 이등분선 한 줄이면 좌우 삼각형이 완벽히 포개져 두 밑각 x는 144도의 절반인 72도가 즉시 도출됩니다! 보조선 감각을 깨우는 시각 증명, 지금 구독 눌러 매일 챙겨 보세요!",
        "act3_en": "Bisecting the 36-degree vertex folds the triangle into exact mirror halves, giving base angle x equals 72 degrees immediately! Hit Subscribe to build unstoppable geometry intuition!",
        "comment_quiz_ko": "🧩 [5초 암산] 이등변삼각형의 한 외각(꼭지각 바깥쪽 각)이 130°일 때 한 밑각 x는 몇 도일까요? (반으로 나누기만 하면 끝!) 👇",
        "comment_quiz_en": "🧩 [5-Sec Check] If the exterior angle at the vertex of an isosceles triangle is 130°, what is each base angle x? 👇",
    },
    {
        "slug": "2014111902",
        "diagram_kind": "ceva_ratios",
        "exam_badge_ko": "🚨 경시·특목·수능 도형 비율 킬러",
        "exam_badge_en": "🚨 Olympiad & AMC Ratio Killer",
        "problem_label_ko": "세 체바선이 한 점 P에서 만나고 BD:DC=2:3, CE:EA=3:4일 때 AF:FB = x : y는?",
        "problem_label_en": "Three cevians concur at P with BD:DC=2:3 and CE:EA=3:4. Find AF:FB!",
        "figure_caption_ko": "BD:DC = 2:3, CE:EA = 3:4  ➔  AF:FB = ?",
        "figure_caption_en": "BD:DC = 2:3, CE:EA = 3:4  ➔  AF:FB = ?",
        "answer_label_ko": "삼각형 넓이비 순환 곱 = 1 ➔ (2/3)×(3/4)×(AF/FB)=1 ➔ AF:FB = 2:1 (5초 컷!)",
        "answer_label_en": "Cyclic Area Ratio = 1 ➔ (2/3)×(3/4)×(AF/FB)=1 ➔ AF:FB = 2:1!",
        "title_ko": "🔥 보조평행선 없이 5초 컷! 삼각형 선분비 킬러를 순식간에 끝내는 넓이비 원리 | 체바의 정리 시각 증명",
        "title_en": "🔥 Solve Triangle Ratio Killers in 5 Seconds via Area Ratios! | Ceva's Theorem Visual Proof",
        "short_title_ko": "❓ AF:FB 비율, 좌표 안 쓰고 5초 만에 암산되시나요? 체바 넓이비 해법! #Shorts",
        "short_title_en": "❓ Can You Find Ratio AF:FB in 5 Seconds Without Coordinates? Ceva Visual Trick! #Shorts",
        "act1_ko": "삼각형 내부 한 점에서 세 직선이 만날 때, 복잡한 연립방정식이나 좌표 없이 AF 대 FB의 비율을 단 5초 만에 암산할 수 있을까요?",
        "act1_en": "When three lines meet inside a triangle, can you find the missing side ratio AF to FB in five seconds flat without coordinates or messy algebra?",
        "act3_ko": "밑변의 비가 곧 내부 삼각형 넓이의 비라는 원리로 3분의 2 곱하기 4분의 3 곱하기 AF 대 FB가 1이 되므로, 3이 약분되어 정답 2 대 1이 5초 만에 완성됩니다! 상위 1% 도형 통찰, 지금 바로 구독해 두세요!",
        "act3_en": "Since base ratios match area ratios around point P, two-thirds times three-fourths times AF over FB equals 1—canceling 3 gives AF to FB equals 2 to 1 in five seconds! Subscribe now for more Olympiad-grade visual shortcuts!",
        "comment_quiz_ko": "🧩 [5초 암산] BD:DC = 1:2, CE:EA = 2:5일 때 한 점에서 만나려면 AF:FB는 몇 대 몇일까요? 댓글로 도전! 👇",
        "comment_quiz_en": "🧩 [5-Sec Check] If BD:DC = 1:2 and CE:EA = 2:5, what ratio AF:FB makes the three lines concurrent? 👇",
    },
    {
        "slug": "2014111901",
        "diagram_kind": "menelaus_line",
        "exam_badge_ko": "🚨 내신 심화·수능 벡터/기하 필수",
        "exam_badge_en": "🚨 Geometry & Vector Ratio Essential",
        "problem_label_ko": "할선이 연장선 D(BC:CD=1:1)와 변 위 E(CE:EA=1:3)를 지날 때 AF:FB는?",
        "problem_label_en": "A line cuts BC extended at D (BC=CD) and AC at E (CE:EA=1:3). Find AF:FB!",
        "figure_caption_ko": "BD:DC = 2:1, CE:EA = 1:3  ➔  AF:FB = ?",
        "figure_caption_en": "BD:DC = 2:1, CE:EA = 1:3  ➔  AF:FB = ?",
        "answer_label_ko": "평행보조선 1줄 닮음 고리! (2/1)×(1/3)×(AF/FB)=1 ➔ AF:FB = 3:2!",
        "answer_label_en": "1 Parallel Line Similarity Loop! (2/1)×(1/3)×(AF/FB)=1 ➔ AF:FB = 3:2!",
        "title_ko": "⚡ 헷갈리는 외분점 순서 실수 끝! 평행보조선 1줄로 꿰뚫는 5초 비율 해법 | 메넬라우스 정리 시각 증명",
        "title_en": "⚡ Never Mix Up Ratio Order Again! One Parallel Line Proves It | Menelaus' Theorem Visualized",
        "short_title_ko": "❓ 삼각형 가로지르는 직선 비율 문제, 평행선 1줄로 5초 컷! #Shorts",
        "short_title_en": "❓ Transversal Line Ratio Trap—One Parallel Line Solves It in 5s! #Shorts",
        "act1_ko": "직선이 삼각형을 비스듬히 뚫고 지나갈 때 외분점 순서를 헷갈려 틀려 본 적 있으신가요? 꼭짓점 평행선 딱 한 줄이면 절대 틀리지 않습니다!",
        "act1_en": "Ever lose exam points mixing up segment order when a line slices across a triangle? One parallel auxiliary line makes the ratio unforgettable!",
        "act3_ko": "꼭짓점 점프 순환 고리에 그대로 넣으면 1분의 2 곱하기 3분의 1 곱하기 FB분의 AF가 1이 되어 AF 대 FB는 3 대 2로 단번에 해결됩니다! 지금 채널을 구독하고 흔들리지 않는 도형 무기를 장착하세요!",
        "act3_en": "Following the vertex-to-intersection loop gives 2 over 1 times 1 over 3 times AF over FB equals 1—so AF to FB is 3 to 2! Hit Subscribe for daily visual proof mastery!",
        "comment_quiz_ko": "🧩 [5초 체크] BD:DC = 3:1, CE:EA = 1:3이면 AF:FB는 몇 대 몇이 될까요? 암산 결과를 댓글로! 👇",
        "comment_quiz_en": "🧩 [5-Sec Check] If BD:DC = 3:1 and CE:EA = 1:3, what is AF:FB? Drop your answer below! 👇",
    },
]


def _draw_exam_problem_diagram(draw: ImageDraw.ImageDraw, box: tuple, kind: str, solved: bool = False, canvas_img: Image.Image | None = None, pdf_doc=None):
    """Act 1(문제 제시) 및 Act 3(보조선 해체 완료)용 선명한 기하 다이어그램 렌더링 (원문 PDF 슬라이드 직접 매핑 지원)"""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    draw.rounded_rectangle(box, radius=24, fill=(12, 20, 42), outline=(56, 189, 248), width=3)

    if kind == "pdf_native" and canvas_img is not None and pdf_doc is not None and len(pdf_doc) >= 1:
        import min7014_video_maker as vmaker
        idx_p = max(0, len(pdf_doc) - 2) if solved else 0
        pix = pdf_doc[idx_p].get_pixmap(dpi=220)
        sl = vmaker._mask_pdf_bottom_author_bar(Image.frombytes("RGB", [pix.width, pix.height], pix.samples))
        sc = min((w - 36) / sl.width, (h - 36) / sl.height)
        nw, nh = int(sl.width * sc), int(sl.height * sc)
        px, py = x0 + (w - nw) // 2, y0 + (h - nh) // 2
        canvas_img.paste(sl.resize((nw, nh), Image.Resampling.LANCZOS), (px, py))
        return

    cyan = (56, 189, 248)
    gold = (250, 204, 21)
    red_aux = (244, 63, 94)
    white = (248, 250, 252)
    green = (52, 211, 153)

    r = int(min(w, h) * 0.34)
    if kind == "circle_inscribed":
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=cyan, width=5)
        pa = (cx - int(r * 0.78), cy + int(r * 0.62))
        pb = (cx + int(r * 0.82), cy + int(r * 0.57))
        pp = (cx + int(r * 0.18), cy - int(r * 0.98))
        draw.line([pa, (cx, cy), pb], fill=gold, width=5)
        draw.line([pa, pp, pb], fill=white, width=5)
        if solved:
            pd = (cx - int(r * 0.18), cy + int(r * 0.98))
            draw.line([pp, (cx, cy), pd], fill=red_aux, width=6)
        for pt in (pa, pb, pp, (cx, cy)):
            draw.ellipse((pt[0] - 7, pt[1] - 7, pt[0] + 7, pt[1] + 7), fill=gold)
    elif kind == "tangent_chord":
        draw.ellipse((cx - r, cy - r - 12, cx + r, cy + r - 12), outline=cyan, width=5)
        occ_y = cy + r - 12
        draw.line([(cx - int(r * 1.25), occ_y), (cx + int(r * 1.25), occ_y)], fill=gold, width=5)
        pa = (cx, occ_y)
        pb = (cx + int(r * 0.86), cy - 12 + int(r * 0.5))
        pc = (cx - int(r * 0.72), cy - 12 - int(r * 0.68))
        draw.polygon([pa, pb, pc], outline=white, width=4)
        if solved:
            pd = (cx, cy - r - 12)
            draw.line([pa, pd, pb], fill=red_aux, width=6)
    elif kind == "pythagoras_squares":
        s = int(min(w, h) * 0.16)
        p1 = (cx - s, cy + int(s * 0.8))
        p2 = (cx + int(s * 1.3), cy + int(s * 0.8))
        p3 = (cx - s, cy - int(s * 0.9))
        draw.polygon([p1, p2, p3], outline=white, width=5)
        draw.rectangle((p3[0] - int(s * 1.7), p3[1], p1[0], p1[1]), outline=cyan, width=4)
        draw.rectangle((p1[0], p1[1], p2[0], p1[1] + int(s * 1.5)), outline=green, width=4)
        if solved:
            draw.line([p3, (cx + int(s * 0.3), cy + int(s * 2.3))], fill=red_aux, width=6)
    elif kind == "isosceles_bisector":
        top = (cx, cy - int(r * 0.95))
        left = (cx - int(r * 0.82), cy + int(r * 0.85))
        right = (cx + int(r * 0.82), cy + int(r * 0.85))
        draw.polygon([top, left, right], outline=cyan, width=5)
        if solved:
            mid = (cx, cy + int(r * 0.85))
            draw.line([top, mid], fill=red_aux, width=6)
    else:
        top = (cx, cy - int(r * 0.92))
        left = (cx - int(r * 0.95), cy + int(r * 0.82))
        right = (cx + int(r * 0.95), cy + int(r * 0.82))
        draw.polygon([top, left, right], outline=cyan, width=5)
        d_pt = (cx - int(r * 0.15), cy + int(r * 0.82))
        e_pt = (cx + int(r * 0.48), cy - int(r * 0.05))
        f_pt = (cx - int(r * 0.52), cy - int(r * 0.12))
        draw.line([top, d_pt], fill=gold, width=4)
        draw.line([left, e_pt], fill=gold, width=4)
        draw.line([right, f_pt], fill=red_aux if solved else white, width=5)


def render_exam_hybrid_thumbnail(bp: dict, doc, lang_code: str, out_png: Path) -> Path:
    import min7014_video_maker as vmaker

    W, H = 1280, 720
    img = Image.new("RGB", (W, H), (8, 13, 28))
    draw = ImageDraw.Draw(img)
    for gx in range(0, W, 80):
        draw.line([(gx, 0), (gx, H)], fill=(16, 26, 52), width=1)
    for gy in range(0, H, 80):
        draw.line([(0, gy), (W, gy)], fill=(16, 26, 52), width=1)

    is_en = lang_code == "en"
    # 우측: 원본 min7014.github.io 클라이맥스 슬라이드 무결점 배치 (Rule 28)
    key_idx = max(0, len(doc) - 2)
    pix = doc[key_idx].get_pixmap(dpi=240)
    slide_img = vmaker._mask_pdf_bottom_author_bar(Image.frombytes("RGB", [pix.width, pix.height], pix.samples))
    scale = min(620 / slide_img.width, 580 / slide_img.height)
    sw, sh = int(slide_img.width * scale), int(slide_img.height * scale)
    sx, sy = W - sw - 34, (H - sh) // 2
    draw.rounded_rectangle((sx - 12, sy - 12, sx + sw + 12, sy + sh + 12), radius=22, fill=(244, 63, 94), outline=(250, 204, 21), width=4)
    img.paste(slide_img.resize((sw, sh), Image.Resampling.LANCZOS), (sx, sy))

    # 좌측 상단 시험 킬러 배지
    badge = bp["exam_badge_en"] if is_en else bp["exam_badge_ko"]
    draw.rounded_rectangle((36, 36, 586, 98), radius=16, fill=(190, 18, 60), outline=(254, 240, 138), width=3)
    draw.text((56, 51), badge, fill=(255, 255, 255), font=vmaker.get_font_for_lang("ko", 26, bold=True))

    # 좌측 초대형 2줄 시험 함정 카피
    h_lines = ["90% MISS THIS!", "SOLVE x IN 5s!"] if is_en else ["시험장 90% 함정!", "보조선 1줄 5초 컷!"]
    f_big = vmaker.get_font_for_lang("ko", 54 if is_en else 60, bold=True)
    yh = 128
    for idx_l, hl in enumerate(h_lines):
        c_fill = (255, 255, 255) if idx_l == 0 else (250, 204, 21)
        for dx in (-4, 0, 4):
            for dy in (-4, 0, 4):
                if dx or dy:
                    draw.text((40 + dx, yh + dy), hl, fill=(0, 0, 0), font=f_big)
        draw.text((40, yh), hl, fill=c_fill, font=f_big)
        yh += 80

    # 좌측 중단 구체적 수치 조건 박스 (x = ?)
    draw.rounded_rectangle((36, 316, 586, 496), radius=18, fill=(15, 25, 52), outline=(56, 189, 248), width=3)
    cap_main = bp["figure_caption_en"] if is_en else bp["figure_caption_ko"]
    draw.text((56, 340), "📝 [실전 문제]" if not is_en else "📝 [EXAM PROBLEM]", fill=(250, 204, 21), font=vmaker.get_font_for_lang("ko", 26, bold=True))
    wrapped_cap = textwrap.wrap(cap_main, width=24 if is_en else 18)[:2]
    yc = 386
    for cl in wrapped_cap:
        draw.text((56, yc), cl, fill=(125, 211, 252), font=vmaker.get_font_for_lang("ko", 32 if is_en else 34, bold=True))
        yc += 46

    # 하단 구독 유도 브랜드 바
    draw.rounded_rectangle((36, 540, 586, 656), radius=16, fill=(15, 118, 110), outline=(110, 231, 183), width=2)
    cta1 = "⚡ 공식 암기 ZERO · 10초 시각 해법" if not is_en else "⚡ Zero Rote Formulas · 10s Visual Hack"
    cta2 = "🔔 @min7014_ai 내신·수능 도형 정복" if not is_en else "🔔 @min7014_ai · Exam Visual Proofs"
    draw.text((56, 558), cta1, fill=(254, 240, 138), font=vmaker.get_font_for_lang("ko", 24, bold=True))
    draw.text((56, 602), cta2, fill=(255, 255, 255), font=vmaker.get_font_for_lang("ko", 24, bold=True))

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
    1) 1080p 16:9 '실전 문제 ➔ min7014 시각 증명 ➔ 5초 해체' 본편 (3~5분 스윗스팟) + 전용 썸네일
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
        d1.rounded_rectangle((56, 44, 1864, 156), radius=22, fill=(190, 18, 60), outline=(250, 204, 21), width=4)
        d1.text((88, 74), bp["exam_badge_en"] if is_en else bp["exam_badge_ko"], fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 42, bold=True))
        d1.text((1380, 78), "⏱️ 5-SEC CHALLENGE" if is_en else "⏱️ 실전 5초 챌린지!", fill=(254, 240, 138), font=vmaker.get_font_for_lang(lang_code, 36, bold=True))

        _draw_exam_problem_diagram(d1, (68, 196, 940, 880), bp["diagram_kind"], solved=False, canvas_img=act1_img, pdf_doc=doc)
        d1.rounded_rectangle((980, 196, 1852, 880), radius=24, fill=(15, 23, 42), outline=(56, 189, 248), width=3)
        p_lbl = bp["problem_label_en"] if is_en else bp["problem_label_ko"]
        y_txt = 248
        for line in textwrap.wrap(p_lbl, width=28 if is_en else 18)[:4]:
            d1.text((1024, y_txt), line, fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 42, bold=True))
            y_txt += 64
        d1.rounded_rectangle((1024, 560, 1808, 700), radius=18, fill=(30, 41, 59), outline=(250, 204, 21), width=3)
        d1.text((1056, 604), bp["figure_caption_en"] if is_en else bp["figure_caption_ko"], fill=(250, 204, 21), font=vmaker.get_font_for_lang(lang_code, 38, bold=True))
        d1.text((1024, 760), "💡 Hint: Don't write equations—spot ONE line!" if is_en else "💡 힌트: 방정식을 세우지 말고 보조선 1줄을 찾으세요!", fill=(125, 211, 252), font=vmaker.get_font_for_lang(lang_code, 30, bold=True))

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
            hdr = f"📐 Visual Proof Step {idx_s}/{len(mid_indices)} (min7014.github.io)" if is_en else f"📐 핵심 시각 증명 STEP {idx_s}/{len(mid_indices)} (원리 해체)"
            df.text((76, 46), hdr, fill=(125, 211, 252), font=vmaker.get_font_for_lang(lang_code, 32, bold=True))

            sc = min(1760 / s_raw.width, 880 / s_raw.height)
            nw, nh = int(s_raw.width * sc), int(s_raw.height * sc)
            ox, oy = (1920 - nw) // 2, 128 + (920 - nh) // 2
            df.rounded_rectangle((ox - 8, oy - 8, ox + nw + 8, oy + nh + 8), radius=16, fill=(255, 255, 255), outline=(56, 189, 248), width=3)
            frame.paste(s_raw.resize((nw, nh), Image.Resampling.LANCZOS), (ox, oy))

            raw_n = (p_info.get("narrations") or {}).get(lang_code) or p_info.get("explanation_text") or ""
            raw_n = re.sub(r"안녕하세요[^.?!]*[.?!]\s*", "", raw_n).strip()
            if not raw_n:
                raw_n = "Watch how the auxiliary geometry locks the two quantities together." if is_en else "보조선에 의해 두 도형 요소의 크기가 자연스럽게 연결됩니다."
            s_mp3 = tmp_dir / f"long_step_{idx_s:02d}.mp3"
            s_mp4 = tmp_dir / f"long_step_{idx_s:02d}.mp4"
            vmaker.synthesize_tts_mp3_sync(raw_n, voice_name, s_mp3, rate="+8%")
            _encode_single_card_segment(frame, s_mp3, s_mp4, ffmpeg_exe, ffprobe_exe)
            long_segs.append(s_mp4)

        # Act 3: 실전 문제 5초 암산 완결 + 구독 전환 카드
        act3_img = Image.new("RGB", (1920, 1080), (8, 18, 32))
        d3 = ImageDraw.Draw(act3_img)
        d3.rounded_rectangle((56, 44, 1864, 156), radius=22, fill=(5, 150, 105), outline=(250, 204, 21), width=4)
        d3.text((88, 74), "✅ SOLVED IN 5 SECONDS! (1-LINE VISUAL HACK)" if is_en else "✅ 보조선 1줄로 단 5초 만에 실전 해체 완료!", fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 42, bold=True))
        _draw_exam_problem_diagram(d3, (68, 196, 940, 880), bp["diagram_kind"], solved=True, canvas_img=act3_img, pdf_doc=doc)
        d3.rounded_rectangle((980, 196, 1852, 880), radius=24, fill=(15, 23, 42), outline=(52, 211, 153), width=4)
        ans_lbl = bp["answer_label_en"] if is_en else bp["answer_label_ko"]
        ya = 256
        for line in textwrap.wrap(ans_lbl, width=28 if is_en else 18)[:4]:
            d3.text((1024, ya), line, fill=(254, 240, 138), font=vmaker.get_font_for_lang(lang_code, 42, bold=True))
            ya += 64
        d3.rounded_rectangle((1024, 590, 1808, 820), radius=20, fill=(2, 132, 199), outline=(255, 255, 255), width=3)
        sub_h1 = "🔔 Subscribe to @min7014_ai Right Now!" if is_en else "🔔 지금 바로 @min7014_ai [구독] 누르기!"
        sub_h2 = "Turn tough exam traps into 10-sec visual solves!" if is_en else "내신·수능 4점 도형·미적분이 10초 눈풀이로 바뀝니다!"
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
        ds1.rounded_rectangle((44, 68, 1036, 214), radius=24, fill=(190, 18, 60), outline=(250, 204, 21), width=4)
        ds1.text((78, 110), "⏱️ CAN YOU FIND x IN 3 SECONDS?" if is_en else "⏱️ 공식 없이 3초 안에 x가 보이시나요?", fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 42, bold=True))
        _draw_exam_problem_diagram(ds1, (56, 256, 1024, 1220), bp["diagram_kind"], solved=False, canvas_img=s1, pdf_doc=doc)
        ds1.rounded_rectangle((56, 1260, 1024, 1520), radius=24, fill=(15, 23, 42), outline=(56, 189, 248), width=4)
        ds1.text((92, 1305), bp["figure_caption_en"] if is_en else bp["figure_caption_ko"], fill=(250, 204, 21), font=vmaker.get_font_for_lang(lang_code, 42, bold=True))
        p_short_lines = textwrap.wrap(bp["problem_label_en"] if is_en else bp["problem_label_ko"], width=30 if is_en else 20)[:2]
        for li, pl in enumerate(p_short_lines):
            ds1.text((92, 1384 + li * 52), pl, fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 34, bold=True))

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
            dsc.text((78, 108), f"💡 VISUAL CLUE {si-1}/2 — Watch the Auxiliary Line!" if is_en else f"💡 핵심 단서 {si-1}/2 — 보조선의 마법을 보세요!", fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 36, bold=True))
            k_scale = min(980 / sl_img.width, 1020 / sl_img.height)
            kw, kh = int(sl_img.width * k_scale), int(sl_img.height * k_scale)
            kx, ky = (1080 - kw) // 2, 260 + (1060 - kh) // 2
            dsc.rounded_rectangle((kx - 8, ky - 8, kx + kw + 8, ky + kh + 8), radius=18, fill=(255, 255, 255), outline=(56, 189, 248), width=4)
            sc_v.paste(sl_img.resize((kw, kh), Image.Resampling.LANCZOS), (kx, ky))

            p_match = pages[min(len(pages) - 1, dp_i)]
            clue_txt = ((p_match.get("narrations") or {}).get(lang_code) or p_match.get("explanation_text") or "").strip()
            sents = [x.strip() for x in re.split(r"(?<=[.?!])\s+", clue_txt) if x.strip() and "안녕하세요" not in x]
            short_clue = sents[-1] if sents else ("One auxiliary line locks the equal angles together!" if is_en else "보조선 한 줄이 숨어 있던 합동과 대칭을 즉시 깨웁니다!")
            if len(short_clue) > (120 if is_en else 68):
                short_clue = short_clue[: (116 if is_en else 64)].rsplit(" ", 1)[0] + "."
            dsc.rounded_rectangle((44, 1380, 1036, 1600), radius=22, fill=(15, 23, 42), outline=(56, 189, 248), width=3)
            for li, cl_l in enumerate(textwrap.wrap(short_clue, width=32 if is_en else 20)[:3]):
                dsc.text((80, 1418 + li * 50), cl_l, fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 34, bold=True))

            sh_m_mp3 = tmp_dir / f"sh_{si}.mp3"
            sh_m_seg = tmp_dir / f"sh_{si}.mp4"
            vmaker.synthesize_tts_mp3_sync(short_clue, voice_name, sh_m_mp3, rate="+18%")
            _encode_single_card_segment(sc_v, sh_m_mp3, sh_m_seg, ffmpeg_exe, ffprobe_exe)
            sh_segs.append(sh_m_seg)

        # Scene 4: 5초 정답 완결 + 하단 @min7014_ai 구독 & 관련 동영상 클릭 CTA
        s4 = Image.new("RGB", (1080, 1920), (8, 20, 34))
        ds4 = ImageDraw.Draw(s4)
        ds4.rounded_rectangle((44, 68, 1036, 204), radius=24, fill=(5, 150, 105), outline=(250, 204, 21), width=4)
        ds4.text((78, 110), "🎯 BOOM! 5-SECOND EXAM PAYOFF!" if is_en else "🎯 유레카! 보조선 1줄로 5초 암산 끝!", fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 40, bold=True))
        _draw_exam_problem_diagram(ds4, (56, 244, 1024, 1140), bp["diagram_kind"], solved=True, canvas_img=s4, pdf_doc=doc)
        ds4.rounded_rectangle((44, 1180, 1036, 1590), radius=24, fill=(15, 23, 42), outline=(52, 211, 153), width=4)
        for li, al in enumerate(textwrap.wrap(bp["answer_label_en"] if is_en else bp["answer_label_ko"], width=28 if is_en else 19)[:3]):
            ds4.text((80, 1222 + li * 56), al, fill=(254, 240, 138), font=vmaker.get_font_for_lang(lang_code, 38, bold=True))
        ds4.rounded_rectangle((72, 1430, 1008, 1560), radius=18, fill=(2, 132, 199))
        cta_b = "👇 Tap Related Video & Hit [Subscribe] @min7014_ai!" if is_en else "👇 아래 [관련 동영상] 풀버전 클릭 & [@min7014_ai 구독]!"
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
                "exam_badge_ko": "🚨 내신·수능 빈출 시각 증명 해법",
                "exam_badge_en": "🚨 High-Yield Exam Visual Hack",
                "problem_label_ko": q0_ko[:68],
                "problem_label_en": q0_en[:96],
                "figure_caption_ko": f"핵심 원리: {ko_c}",
                "figure_caption_en": f"Core Principle: {en_c}",
                "answer_label_ko": end_ko or f"보조선 1줄 시각 불변량으로 [{ko_c}] 5초 완벽 해결!",
                "answer_label_en": end_en or f"One visual auxiliary clue proves [{en_c}] in 5 seconds!",
                "title_ko": f"🔥 공식 암기 금지! 시험장에서 5초 만에 꿰뚫는 보조선 직관 | {ko_c} 시각적 증명",
                "title_en": f"🔥 Stop Memorizing Formulas! 5-Second Visual Exam Proof | {en_c}",
                "short_title_ko": f"❓ 공식 없이 3초 만에 보이시나요? {ko_c} 보조선 해법! #Shorts",
                "short_title_en": f"❓ Can You Spot Why {en_c} Works in 3 Seconds? #Shorts",
                "act1_ko": f"잠깐! 시험장에서 {ko_c} 관련 문제가 나왔을 때 공식만 외우면 조금만 변형되어도 막힙니다. 도형에서 핵심 단서가 3초 만에 보이시나요?",
                "act1_en": f"Stop! Memorizing {en_c} blindly fails whenever an exam twists the figure. Can you spot the visual invariant in three seconds?",
                "act3_ko": f"결국 이 보조선 원리 하나로 {ko_c}이 눈앞에서 명쾌하게 해결됩니다! 내신과 수능 수학을 10초 눈풀이로 바꾸는 시각 증명, 지금 바로 채널 구독을 눌러 두세요!",
                "act3_en": f"That single visual connection proves {en_c} effortlessly! Subscribe to @min7014_ai right now for daily 10-second exam breakthroughs!",
                "comment_quiz_ko": f"🧩 [5초 개념 체크] 오늘 본 '{ko_c}' 증명에서 가장 결정적이었던 보조선·성질은 무엇이었나요? 한 줄로 댓글에 남겨 복습해 보세요! 👇",
                "comment_quiz_en": f"🧩 [5-Sec Recap] Which visual step made '{en_c}' click for you? Share in the comments below! 👇",
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
                f"🎯 [실전 함정 하이브리드 자동 발행 완료 ({kind_label} · {lc.upper()})]\n• 주제({slug}): {title}\n• 링크: {url}",
            ],
            cwd=str(ROOT_DIR),
            timeout=20,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass


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
    yt, _ = vmaker.get_available_youtube_upload_service()
    if yt is None:
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
                title = vmaker.sanitize_youtube_title(bp["title_en"] if is_en else bp["title_ko"])
                pdf_url = sdoc.get("pdf_url") or "https://min7014.github.io/"
                desc = (
                    f"🔥 Solve this high-frequency exam trap in 5 seconds using visual geometry!\n"
                    f"📐 Original Visual Proof PDF: {pdf_url}\n"
                    f"🌐 Interactive Math Lab & 16,548 Problems: https://min7014.github.io/mathedu/\n"
                    f"🔔 Subscribe to @min7014_ai: https://www.youtube.com/@min7014_ai?sub_confirmation=1\n\n"
                    f"#MathTrap #SATMath #VisualProof #GeometryHack #OlympiadMath"
                    if is_en
                    else f"🔥 시험장에서 90%가 방정식 세우다 시간 뺏기는 실전 함정 문항을 보조선 1줄 시각 증명으로 5초 만에 해체합니다!\n"
                    f"📐 원문 단계별 시각 증명 PDF: {pdf_url}\n"
                    f"🌐 16,548문항 기출 디딤돌 & 자체 제작 MathLab 실습: https://min7014.github.io/mathedu/\n"
                    f"🔔 @min7014_ai 무료 구독하기: https://www.youtube.com/@min7014_ai?sub_confirmation=1\n\n"
                    f"#수능수학 #내신도형 #시각적증명 #보조선해법 #수학잘하는법"
                )
                body = {
                    "snippet": {
                        "title": title,
                        "description": desc,
                        "tags": ["SAT Math", "Geometry Proof", "Visual Math", "Math Trick"] if is_en else ["수능수학", "내신수학", "도형보조선", "시각적증명", "원주각"],
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
                    if "uploadLimitExceeded" in str(e) or "quotaExceeded" in str(e):
                        vmaker._LAST_UPLOAD_QUOTA_BLOCKED = True
                    return None

            if kind == "short" and (ex_urls.get(lc) or "").strip() and not (ex_sh_urls.get(lc) or "").strip():
                if not s_mp4.exists():
                    render_exam_hybrid_bundle(bp, lang_code=lc)
                if not s_mp4.exists():
                    continue
                sh_title = vmaker.sanitize_youtube_title(bp["short_title_en"] if is_en else bp["short_title_ko"])
                long_u = ex_urls[lc]
                desc_sh = (
                    f"🎬 Watch Full 5-Sec Exam Breakdown (1080p): {long_u}\n"
                    f"🔔 Subscribe @min7014_ai for daily visual exam hacks!\n#Shorts #SATMath #GeometryTrick #MathPuzzle"
                    if is_en
                    else f"🎬 1080p 실전 5초 해체 풀버전 바로 보기: {long_u}\n"
                    f"🔔 내신·수능 도형 10초 눈풀이 @min7014_ai 구독!\n#Shorts #수능수학 #도형보조선 #수학퀴즈"
                )
                body_sh = {
                    "snippet": {
                        "title": sh_title,
                        "description": desc_sh,
                        "tags": ["Shorts", "Math Puzzle", "SAT Math", "Geometry"] if is_en else ["Shorts", "수학쇼츠", "수능수학", "보조선"],
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
                    if "uploadLimitExceeded" in str(e) or "quotaExceeded" in str(e):
                        vmaker._LAST_UPLOAD_QUOTA_BLOCKED = True
                    return None
    return None


if __name__ == "__main__":
    import sys
    cnt = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    out = ensure_next_exam_hybrid_rendered(max_bundles=cnt)
    print(json.dumps(out, ensure_ascii=False, indent=2))
