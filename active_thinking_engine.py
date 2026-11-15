#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
active_thinking_engine.py
=========================
[능동적 수학 사고(Active Mathematical Thinking) 4단계 시네마 & 코칭 엔진 — 0 LLM Credit]

핵심 철학 (Chairman min7014 수학교육 비전):
"어렵겠지만, 영상을 보고 수학교육에서 중요한 능동적인 사고가 될 수 있게 해주면 좋겠다."

수학교육학 & 인지과학적 해법 (유창한 설명의 착각[Illusion of Competence] 타파):
1. [1단계 · 사전 직관 예측 선택 (Prediction Commitment: A vs B)]:
   - 증명을 보기 전에 흔히 빠지는 통념(A)과 수학적 구조(B) 중 하나를 3.2초 동안 스스로 예측·선택하게 하여,
     수동적 구경꾼이 아닌 '자신의 가설을 검증하는 탐구자' 상태로 전환합니다 (Derek Muller 효과).
2. [2단계 · 제1보조선 등장 직전 '백지 도형' 4초 발상 정지 (Pre-Crux Blank-Figure Pause)]:
   - 가장 중요한 결정적 보조선·대칭·식변형이 등장하기 '직전 페이지'(보조선이 아직 그어지지 않은 순수 가정 도형)에서
     화면을 4.0초 멈추고 폴리아(Pólya) 발문을 던져 시청자가 눈으로 먼저 보조선을 그어 보게 합니다 (Generation Effect).
   - Rule 28.1 절대 준수: 중앙 오리지널 PDF 슬라이드(y: 86~810)는 단 1픽셀도 가리지 않고, 상·하단 여백 바에만
     차분한 골드·에메랄드 사고 타이머 게이지(Rule 37)를 표시합니다.
3. [3단계 · 결론 직전 '왜 성립할까?' 3초 근거 추론 (Self-Explanation Micro-Check)]:
   - 최종 결론(Q.E.D.) 직전 단계에서 어떤 불변량·합동·대칭 때문에 등식이 필연적으로 성립하는지 3.0초 스스로 이유를 말하게 합니다.
4. [4단계 · 라카토스 반례·경계 실험 & What-If-Not 조건 변형 전이 (Post-Proof Transfer)]:
   - 증명이 끝난 순간 사고가 멈추지 않도록, 조건 하나를 극단으로 보내거나 바꿨을 때(예: 이차→삼차, 타원→포물선)
     명제가 유지되는지 깨지는지 추론하게 하고 video_board.html 능동적 사고 실험실(?mode=active) 실습으로 직결합니다.
"""

import silent_subprocess  # noqa: F401 — Rule 48: 100% 무창(CREATE_NO_WINDOW) 실행 강제

import math
import re
import struct
import subprocess
import textwrap
import wave
from pathlib import Path

from PIL import Image, ImageDraw

ROOT_DIR = Path(__file__).resolve().parent
AUDIO_CACHE_DIR = ROOT_DIR / ".temp" / "active_thinking_audio"
AUDIO_CACHE_DIR.mkdir(parents=True, exist_ok=True)


# ==============================================================================
# 1. 대표 단원 정밀 설계 블루프린트 + 847개 전 주제 도메인별 무오류 자동 생성기 (Rule 44)
# ==============================================================================
CURATED_ACTIVE_BLUEPRINTS: dict[str, dict] = {
    "2022051507": {
        "option_a_ko": "[직관 A] 타원 방정식을 미분해 접선 기울기 공식을 세워야만 반사각을 구할 수 있다",
        "option_b_ko": "[직관 B] 식 계산 0줄! 접선 너머에 초점의 '거울 대칭점' 하나만 찍으면 최단거리 직선으로 즉시 끝난다",
        "option_a_en": "[Intuition A] You must differentiate x²/a² + y²/b² = 1 to prove equal reflection angles",
        "option_b_en": "[Intuition B] Zero calculus! Reflecting one focus across the tangent turns reflection into a straight shortest path",
        "prediction_tts_ko": "증명을 보기 전에 여러분의 수학적 직관을 먼저 선택해 보세요! A, 복잡한 접선 미분식이 꼭 필요할까요? 아니면 B, 거울 대칭점 하나로 계산 없이 끝날까요? 3초 동안 먼저 골라 보세요!",
        "prediction_tts_en": "Before watching the proof, commit to your own prediction! Option A: must we use derivative algebra? Or Option B: can one mirror reflection solve it with zero formulas? Choose in 3 seconds!",
        "crux_prompt_ko": "잠깐! 바로 다음 장에서 이 증명의 결정적 보조선이 등장합니다. 두 초점 거리 합 일정 성질을 쓰려면, 어떤 점을 어디에 대칭이동해 일직선으로 펴야 할까요? 4초 동안 화면 위 도형에 눈으로 먼저 그어 보세요!",
        "crux_prompt_en": "Hold on! The decisive auxiliary construction appears on the very next slide. To use constant focal distance sum, which point would YOU reflect across the tangent line? Trace your idea with your eyes for 4 seconds!",
        "justify_prompt_ko": "결론 직전 핵심 추론입니다! 대칭점으로 만든 두 삼각형이 합동이 되면서, 왜 입사각과 반사각이 정확히 같아질 수밖에 없는지 3초 동안 먼저 이유를 떠올려 보세요!",
        "justify_prompt_en": "Final check before Q.E.D.! From the congruent triangles formed by reflection, articulate in your own words for 3 seconds WHY the incident and reflected angles must be equal!",
        "what_if_ko": "[조건 변형 사고 실험] 만약 타원의 오른쪽 초점을 무한히 멀리 보내면 타원이 '포물선'으로 변합니다! 방금 스스로 찾은 거울 대칭 아이디어를 그대로 쓰면 파라볼라 안테나의 빛 반사도 증명될까요?",
        "what_if_en": "[What-If-Not Transfer] Imagine pushing one focus of the ellipse infinitely far away so it becomes a PARABOLA! Does the exact same mirror-point idea prove parabolic dish reflection too?",
    },
    "2019072401": {
        "preferred_crux_idx": 7,
        "preferred_justify_idx": 11,
        "option_a_ko": "[예측 A] 포물선이 한쪽으로 갈수록 가팔라지므로, 할선 PQ와 평행한 접점 R도 가파른 쪽으로 치우쳐 있다",
        "option_b_ko": "[예측 B] 두 점 P, Q가 어디에 있든 할선 PQ의 '중점 M'에서 준선 l에 수선을 내린 바로 그 위치 R에서 접선이 평행해진다",
        "option_a_en": "[Prediction A] Since the parabola steepens on one side, the parallel tangent point R shifts toward the steeper end",
        "option_b_en": "[Prediction B] Wherever P and Q lie, dropping a perpendicular from chord midpoint M to directrix l hits the exact parallel tangent point R",
        "prediction_tts_ko": "영상을 그냥 보지 말고 먼저 예측해 보세요! 포물선 두 점 P, Q를 이은 할선과 똑같은 기울기를 갖는 접점 위치는 A처럼 가파른 쪽으로 치우칠까요, 아니면 B처럼 언제나 현의 중점 M에서 준선에 수선을 내린 정확한 한가운데일까요? 3초 동안 선택해 보세요!",
        "prediction_tts_en": "Do not watch passively—predict first! Does the tangent parallel to secant PQ shift toward the steeper side (Option A), or land right where the perpendicular from midpoint M to directrix l meets the parabola (Option B)? Decide in 3 seconds!",
        "crux_prompt_ko": "여기서 잠깐 멈춰 능동적으로 생각해 보세요! 미분 공식 2ax+b 없이 순수 기하학만으로 할선 PQ와 평행한 접점을 찾으려면, 선분 PQ 위 어떤 특별한 점에서 준선 l에 수선을 내려야 할까요? 4초 동안 눈으로 먼저 그어 보세요!",
        "crux_prompt_en": "Pause and think geometrically! Without derivative formulas, from WHICH special point on chord PQ should you drop a perpendicular to directrix l to locate the parallel tangent point R? Visualize your line for 4 seconds!",
        "justify_prompt_ko": "결론 직전 능동적 점검입니다! 중점 M에서 준선 l에 내린 수선과 포물선의 대칭 성질 때문에 왜 점 R의 접선이 할선 PQ와 정확히 평행해질 수밖에 없는지 3초 동안 스스로 설명해 보세요!",
        "justify_prompt_en": "Self-explanation check! Using midpoint M, the perpendicular to directrix l, and parabola reflection symmetry, explain to yourself in 3 seconds WHY the tangent at R must be parallel to chord PQ!",
        "what_if_ko": "[반례·전이 실험] 이차 포물선에서는 P, Q를 아무리 움직여도 언제나 '중점 M' 위치에서 접선이 평행했습니다. 만약 곡선을 '삼차함수 y = x³'으로 바꾸면 구간 [-1, 2]에서도 중점에서 평행할까요, 아니면 깨질까요?",
        "what_if_en": "[Counterexample Stress-Test] For any parabola, the midpoint rule never fails as P and Q move. What if we change the curve to a CUBIC y = x³ on [-1, 2]—does the midpoint rule survive or break?",
    },
    "2017031401": {
        "option_a_ko": "[예측 A] 분모가 아주 큰 소수(예: 97)이면 순환하지 않고 불규칙하게 영원히 나아가는 분수도 있을 것이다",
        "option_b_ko": "[예측 B] 나누는 수 q보다 작은 나머지는 최대 q-1개뿐이므로, 늦어도 q번째 안에는 반드시 같은 나머지가 다시 나와 순환한다",
        "option_a_en": "[Prediction A] For tricky prime denominators, a fraction's decimal digits might wander forever without repeating",
        "option_b_en": "[Prediction B] Since remainders mod q have at most q-1 non-zero values, division MUST revisit a remainder and repeat",
        "prediction_tts_ko": "먼저 스스로 추론해 보세요! 어떤 분수를 끝없이 나눗셈할 때 A처럼 규칙 없이 뻗어갈 수 있을까요, 아니면 B처럼 나머지 개수의 한계 때문에 반드시 순환할 수밖에 없을까요? 3초 동안 선택해 보세요!",
        "prediction_tts_en": "Predict before the proof! When dividing integers, could digits wander without pattern (A), or do finite remainders force repetition every time (B)? Commit in 3 seconds!",
        "crux_prompt_ko": "잠깐! 다음 단계를 보기 전에 직접 세어 보세요. 어떤 자연수를 7로 나눌 때, 0이 아닌 나머지로 나올 수 있는 숫자는 모두 몇 종류뿐일까요? 그리고 7번 나눗셈을 계속하면 무슨 일이 벌어질지 4초 동안 추론해 보세요!",
        "crux_prompt_en": "Think first! When dividing by 7, how many distinct non-zero remainders can possibly appear—and what MUST happen by the seventh step? Reason it out for 4 seconds!",
        "justify_prompt_ko": "핵심 연결 점검입니다! 이전에 나왔던 똑같은 나머지가 다시 등장하는 그 순간, 왜 그 뒤의 모든 몫의 숫자열이 처음과 똑같이 되풀이될 수밖에 없는지 3초 동안 스스로 말해 보세요!",
        "justify_prompt_en": "Self-check! The exact moment a previous remainder reappears, why is every subsequent quotient digit forced to repeat identically? Articulate why in 3 seconds!",
        "what_if_ko": "[조건 확장 질문] 십진법이 아니라 컴퓨터가 쓰는 '이진법(0과 1)'으로 분수 1/3을 소수로 나타내면 유한소수가 될까요, 순환소수가 될까요? 방금 깨우친 나머지 원리로 추론해 보세요!",
        "what_if_en": "[What-If-Not Transfer] What if we write 1/3 in binary (base 2) instead of base 10—does it terminate or repeat? Use the remainder principle you just mastered!",
    },
    "2016012801": {
        "option_a_ko": "[시각 A] 코시의 평균값 정리는 h(x)=f(x)-kg(x)라는 인위적 보조함수를 외워야만 증명되는 순수 대수 정리다",
        "option_b_ko": "[시각 B] (g(t), f(t))를 평면 위 점의 이동 경로로 그리면 '양 끝점 할선과 평행한 접선'이라는 한 장의 기하 직관이다",
        "option_a_en": "[View A] Cauchy's Mean Value Theorem is purely algebraic—you just have to memorize an artificial helper function",
        "option_b_en": "[View B] Plotting (g(t), f(t)) as a plane curve turns it into one obvious picture: a tangent parallel to the chord",
        "prediction_tts_ko": "먼저 생각해 보세요! 교과서 속 코시의 평균값 정리는 A처럼 억지로 보조함수를 외워야만 하는 대수 공식일까요, 아니면 B처럼 평면 곡선 한 장으로 당연하게 보이는 기하 원리일까요? 3초 선택해 보세요!",
        "prediction_tts_en": "Predict first! Is Cauchy's Mean Value Theorem just memorized helper-function algebra (A), or a single transparent geometric curve picture (B)? Choose in 3 seconds!",
        "crux_prompt_ko": "잠깐 멈추고 발상해 보세요! 두 함수 g(t)와 f(t)의 변화량 비율 f'(c) 나누기 g'(c)를 기하학적인 '기울기'로 한눈에 보려면 가로축과 세로축에 각각 무엇을 놓아야 할까요? 4초 동안 먼저 설계해 보세요!",
        "crux_prompt_en": "Pause and design the representation yourself! To turn the ratio f'(c)/g'(c) into a visible geometric slope, what should you place on the horizontal and vertical axes? Think for 4 seconds!",
        "justify_prompt_ko": "결정적 점검입니다! 곡선 양 끝점을 이은 직선과 접선이 평행할 때, 왜 교과서에 적힌 분수 등식이 즉시 성립하는지 기울기 정의로 3초 동안 연결해 보세요!",
        "justify_prompt_en": "Key justification! When the curve's tangent is parallel to the secant chord, connect slopes in 3 seconds to see why Cauchy's quotient formula follows immediately!",
        "what_if_ko": "[경계 반례 실험] 만약 분모의 미분값 g'(c)가 구간 중간에서 0이 되는 곡선(첨점·되돌림점)이라면 이 정리가 그대로 성립할까요? 왜 'g'(x) ≠ 0' 조건이 필수인지 반례 곡선을 상상해 보세요!",
        "what_if_en": "[Lakatos Boundary Test] What if g'(c) = 0 somewhere inside the interval (a cusp or turn-back)? Why does the theorem require g'(x) ≠ 0? Picture a counterexample curve!",
    },
    "2017091006": {
        "option_a_ko": "[접근 A] 세 변만 주어졌으니 근호가 복잡하게 겹치는 헤론의 공식을 끝까지 외워서 대입해야 한다",
        "option_b_ko": "[접근 B] 꼭짓점에서 수선 보조선 딱 1줄만 내리면 중학교 피타고라스 정리 두 줄로 높이와 넓이가 스스로 구해진다",
        "option_a_en": "[Approach A] With only three sides given, you are stuck unless you memorized Heron's radical formula",
        "option_b_en": "[Approach B] Dropping ONE altitude splits it into two right triangles solvable by the Pythagorean theorem alone",
        "prediction_tts_ko": "시험장에서 공식이 기억나지 않는 순간입니다! 세 변이 6, 5, 4인 삼각형 넓이를 구할 때 A처럼 복잡한 공식을 외워야만 할까요, 아니면 B처럼 보조선 한 줄로 스스로 공식을 대신할 수 있을까요? 3초 동안 선택해 보세요!",
        "prediction_tts_en": "Imagine blanking out on formulas! For a 6-5-4 triangle, are you stuck without Heron's formula (A), or can one altitude rebuild the area from scratch (B)? Choose in 3 seconds!",
        "crux_prompt_ko": "잠깐! 다음 장면을 보기 전에 여러분이 직접 보조선을 그어 보세요! 세 변 6, 5, 4 중 어느 변을 밑변으로 놓고 수선을 내려야 계산이 가장 간단해질지, 미지수 x를 어디에 둘지 4초 동안 먼저 설계해 보세요!",
        "crux_prompt_en": "Pause and construct it yourself! Onto which side of the 6-5-4 triangle would YOU drop an altitude, and which segment would you label x to set up two Pythagorean equations? Plan for 4 seconds!",
        "justify_prompt_ko": "스스로 확인하는 순간입니다! 왼쪽 직각삼각형과 오른쪽 직각삼각형이 공유하는 '공통 높이 h의 제곱'을 같다고 놓으면 x에 대한 이차항이 어떻게 사라지는지 3초 동안 암산해 보세요!",
        "justify_prompt_en": "Mental check! When you equate h² from the left and right right-triangles, watch what happens to the x² terms—verify in 3 seconds why it reduces to a simple linear equation!",
        "what_if_ko": "[일반화 발명 질문] 방금 6, 5, 4 숫자로 해낸 '수선 내리기 → 공통 높이 h² 연립' 과정을 일반 문자 a, b, c로 그대로 따라가면 어떤 유명한 공식이 우리 손으로 재발명될까요?",
        "what_if_en": "[Guided Reinvention] If you repeat the exact 'drop altitude → equate h²' steps with general side letters a, b, c, which famous theorem have you just reinvented by yourself?",
    },
}


def _clean_canvas_str(text: str, lang_code: str) -> str:
    is_en = lang_code == "en"
    rep_en = {
        "🧭": "[INSIGHT]", "🏛️": "[ARCHIVE]", "🏛": "[ARCHIVE]", "🎓": "[TAKEAWAY]",
        "🔔": "[SUBSCRIBE]", "💡": "[CLUE]", "💬": "[INQUIRY]", "👇": "[WATCH]",
        "⏸️": "[PAUSE]", "⏸": "[PAUSE]", "🧠": "[THINK]", "🔍": "[TRANSFER]",
        "🤩": "", "❓": "[Q]", "🔥": "[KEY]", "⚡": "[KEY]",
    }
    rep_ko = {
        "🧭": "[통찰]", "🏛️": "[원문]", "🏛": "[원문]", "🎓": "[핵심]",
        "🔔": "[구독]", "💡": "[단서]", "💬": "[열린발문]", "👇": "[본편보기]",
        "⏸️": "[사고정지]", "⏸": "[사고정지]", "🧠": "[능동사고]", "🔍": "[조건변형]",
        "🤩": "", "❓": "[질문]", "🔥": "[핵심]", "⚡": "[직관]",
    }
    out = str(text or "")
    for k, v in (rep_en if is_en else rep_ko).items():
        out = out.replace(k, v)
    out = out.replace("\ufe0f", "").replace("\u2794", "→")
    return re.sub(r"\s{2,}", " ", out).strip()


def find_crux_and_justify_indices(pages: list[dict]) -> tuple[int, int]:
    """
    원본 PDF 대본(pages)에서:
    1) 제1보조선·핵심 변환이 처음 등장하는 결정적 페이지(crux_idx >= 1)
    2) 최종 결론 직전 핵심 근거 페이지(justify_idx)
    를 자동 탐색합니다.
    """
    n = len(pages)
    if n <= 2:
        return (min(1, max(0, n - 1)), max(0, n - 1))

    crux_idx = None
    crux_markers = ("초록", "green", "보조선", "대칭", "수선", "평행", "치환", "나머지", "유레카", "열쇠")
    # Beamer PDF 특성상 1p(표지)·2p(여백/초기점)를 건너뛰어 직전 슬라이드(crux_idx-1)가 항상 실제 '순수 가정 도형'이 되도록 보장!
    min_start = 3 if n >= 8 else (2 if n >= 4 else 1)
    max_scan = min(n - 2, max(min_start + 1, int(n * 0.55)))
    for idx in range(min_start, max_scan):
        p = pages[idx]
        blob = f"{p.get('color_tag', '')} {p.get('visual_focus', '')} {p.get('step_title', '')} {p.get('explanation_text', '')}".lower()
        if any(m in blob for m in crux_markers):
            crux_idx = idx
            break

    if crux_idx is None:
        crux_idx = min(max(min_start, n // 3), n - 2) if n >= 4 else 1

    justify_idx = max(crux_idx + 2, n - 3) if n >= 7 else max(crux_idx + 1, n - 2)
    if justify_idx >= n:
        justify_idx = n - 1
    return crux_idx, justify_idx


def build_active_thinking_blueprint(slug: str, script_doc: dict) -> dict:
    """
    모든 주제(847+ PDF)에 대해 단원 무결성(Rule 44)을 100% 준수하는 4단계 능동적 사고 발문 세트를 생성합니다.
    (기하 단원과 대수·수체계·미적분 단원을 엄밀히 구분하여 대수 영상에 기하 보조선 문구가 절대 섞이지 않게 보장)
    """
    pages = script_doc.get("pages") or []
    crux_idx, justify_idx = find_crux_and_justify_indices(pages)

    if slug in CURATED_ACTIVE_BLUEPRINTS:
        out = dict(CURATED_ACTIVE_BLUEPRINTS[slug])
        n_p = len(pages)
        if n_p >= 4 and "preferred_crux_idx" in out:
            crux_idx = min(n_p - 2, max(2, int(out["preferred_crux_idx"])))
        if n_p >= 5 and "preferred_justify_idx" in out:
            justify_idx = min(n_p - 2, max(crux_idx + 1, int(out["preferred_justify_idx"])))
        out["crux_idx"] = crux_idx
        out["justify_idx"] = justify_idx
        return out

    title_ko = re.sub(r"\([^)]*\)", "", str(script_doc.get("title") or slug)).strip()
    title_en = str(script_doc.get("title_en") or title_ko).strip()
    blob = f"{title_ko} {title_en} {script_doc.get('sub_domain_ko', '')}".lower()

    is_number_or_algebra = any(
        w in blob for w in ("유리수", "무리수", "제곱근", "소수", "순환소수", "지수", "로그", "방정식", "인수분해", "항등식", "수열", "급수", "rational", "prime", "radical", "exponent", "sequence", "algebra")
    ) and not any(w in blob for w in ("원", "삼각형", "타원", "포물선", "쌍곡선", "접선", "정사각형", "각"))

    is_calculus = any(
        w in blob for w in ("미분", "적분", "극한", "변화율", "평균값", "연속", "구분구적", "derivative", "integral", "limit", "mean value", "calculus")
    )

    if is_number_or_algebra:
        return {
            "crux_idx": crux_idx,
            "justify_idx": justify_idx,
            "option_a_ko": f"[통념 A] '{title_ko}' 성질은 결과 공식만 외워서 숫자를 대입하는 규칙이다",
            "option_b_ko": "[본질 B] 정의와 수의 구조적 규칙(불변량)을 한 단계씩 풀면 공식이 필연적으로 도출된다",
            "option_a_en": f"[Habit A] '{title_en}' is just an algebraic rule to memorize and plug into",
            "option_b_en": "[Insight B] Unpacking the fundamental definition forces the identity to emerge naturally",
            "prediction_tts_ko": f"영상을 보기 전에 먼저 생각해 보세요! {title_ko}, 결과 공식 암기만으로 충분할까요, 아니면 정의에서 출발해 우리 손으로 직접 식을 이끌어낼 수 있을까요? 3초 동안 어떻게 첫 식을 세울지 예측해 보세요!",
            "prediction_tts_en": f"Think actively before watching! For {title_en}, instead of memorizing the final rule, how would YOU rewrite the starting definition to unlock the first step? Predict for 3 seconds!",
            "crux_prompt_ko": "잠깐 멈추고 스스로 식을 연결해 보세요! 바로 다음 단계에서 핵심 식 변형이 등장합니다. 지금 화면의 출발 식에서 어떤 정의나 묶기 규칙을 적용해야 목표 결론에 다가갈 수 있을지 4초 동안 먼저 떠올려 보세요!",
            "crux_prompt_en": "Pause for 4 seconds! Before the key algebraic step appears next, ask yourself: which definition or structural grouping transforms the current expression toward our target?",
            "justify_prompt_ko": "결론 직전 자기 점검입니다! 방금 변형한 식에서 왜 좌변과 우변이 항상 같아질 수밖에 없는지 핵심 근거를 3초 동안 마음속으로 말해 보세요!",
            "justify_prompt_en": "Self-explanation check! Take 3 seconds to state in your own words WHY the two expressions on screen must be identically equal!",
            "what_if_ko": "[조건 변형 질문] 만약 수의 범위(양수·음수·0)나 지수·항의 조건이 바뀐다면 이 성질은 그대로 유지될까요, 아니면 예외 반례가 생길까요? 아래 능동적 사고 실험실에서 직접 점검해 보세요!",
            "what_if_en": "[What-If-Not Stress-Test] What if the domain (zero, negative values, or boundary cases) changes—does the identity still hold, or does a counterexample appear?",
        }

    if is_calculus:
        return {
            "crux_idx": crux_idx,
            "justify_idx": justify_idx,
            "option_a_ko": f"[통념 A] '{title_ko}'은 미분·적분 계산 공식만 기계적으로 적용하는 단원이다",
            "option_b_ko": "[본질 B] 그래프의 기울기·대칭·넓이 변화 구조를 눈으로 먼저 읽으면 수식의 의미가 투명해진다",
            "option_a_en": f"[Habit A] '{title_en}' is purely mechanical symbol manipulation",
            "option_b_en": "[Insight B] Reading slope, symmetry, and area geometry first makes the calculus inevitable",
            "prediction_tts_ko": f"능동적으로 먼저 예측해 보세요! {title_ko}에서 수식을 전개하기 전에, 그래프의 기울기나 넓이 사이에 어떤 기하학적 관계가 숨어 있을까요? 3초 동안 먼저 상상해 보세요!",
            "prediction_tts_en": f"Predict before the algebra! In {title_en}, what geometric relationship between slopes or areas must hold on the graph? Visualize it for 3 seconds!",
            "crux_prompt_ko": "잠깐! 다음 장면에서 결정적인 기하·해석적 연결고리가 나타납니다. 그래프 위 두 점과 접선, 또는 넓이 조각을 어떻게 연결해야 핵심 관계가 드러날지 4초 동안 먼저 눈으로 설계해 보세요!",
            "crux_prompt_en": "Hold on for 4 seconds! Before the decisive geometric link appears next, how would YOU connect the points, secant/tangent, or area slices on this graph?",
            "justify_prompt_ko": "결론 직전 점검입니다! 극한이나 대칭 조건 때문에 왜 목표 등식이 성립할 수밖에 없는지 3초 동안 스스로 근거를 짚어 보세요!",
            "justify_prompt_en": "Final reasoning check! Take 3 seconds to explain to yourself WHY the limit or symmetry condition locks in the target conclusion!",
            "what_if_ko": "[반례·경계 사고 실험] 만약 함수가 매끄럽지 않은 뾰족점(미분불가능)이나 불연속점을 갖는다면 이 정리가 여전히 성립할까요? 전제 조건의 이유를 반례 그래프와 함께 떠올려 보세요!",
            "what_if_en": "[Lakatos Counterexample Test] What if the curve has a sharp corner or discontinuity—where does the theorem break down? Picture a counterexample graph!",
        }

    # 기하·이차곡선·삼각비·공간기하 표준 능동 사고 세트
    return {
        "crux_idx": crux_idx,
        "justify_idx": justify_idx,
        "option_a_ko": f"[통념 A] '{title_ko}'은 결과 공식을 외워서 변과 각의 숫자를 대입하는 문제다",
        "option_b_ko": "[본질 B] 결정적 보조선·대칭·불변량 하나를 스스로 찾으면 공식이 왜 탄생했는지 눈으로 재발명된다",
        "option_a_en": f"[Habit A] '{title_en}' is just a theorem formula to memorize",
        "option_b_en": "[Insight B] One purposeful auxiliary line reveals the invariant and reinvents the theorem visually",
        "prediction_tts_ko": f"수동적으로 보지 말고 먼저 예측해 보세요! {title_ko}에서 모양이 바뀌어도 끝까지 변하지 않는 핵심 관계는 무엇일까요? 3초 동안 도형을 보며 먼저 추측해 보세요!",
        "prediction_tts_en": f"Engage actively first! Looking at {title_en}, what geometric quantity stays invariant even as the figure moves? Form your conjecture in 3 seconds!",
        "crux_prompt_ko": "잠깐 멈추고 먼저 상상해 보세요! 바로 다음 장에서 증명의 열쇠가 되는 보조선이 등장합니다. 떨어진 가정과 결론을 하나로 잇기 위해 여러분이라면 어디에 선을 긋겠습니까? 4초 동안 화면 위 도형에 눈으로 먼저 그어 보세요!",
        "crux_prompt_en": "Pause for 4 seconds! The decisive auxiliary line appears on the very next slide. Where would YOU draw ONE line or symmetry construction to bridge hypothesis and conclusion? Trace it with your eyes first!",
        "justify_prompt_ko": "결론 직전 능동적 추론입니다! 보조선이 만든 합동·닮음·대칭 관계에서 어떤 두 요소가 같기 때문에 최종 결론이 완성되는지 3초 동안 스스로 이유를 말해 보세요!",
        "justify_prompt_en": "Self-explanation check! From the congruence, similarity, or symmetry on screen, state in 3 seconds WHICH equal parts clinch the final conclusion!",
        "what_if_ko": "[What-If-Not 조건 변형] 만약 점의 위치를 도형 외부로 옮기거나 특수한 극단 각도로 바꾸면 이 성질은 어떻게 변할까요? 아래 능동적 사고 실험실(MathLab)에서 점을 직접 드래그해 확인해 보세요!",
        "what_if_en": "[What-If-Not Transfer] What happens if you drag the key point outside the figure or to an extreme angle? Test your conjecture hands-on in the interactive MathLab link below!",
    }


# ==============================================================================
# 2. 순수 절차적 합성(Rule 24 Content ID 0%) 사색 타이머 사운드 생성기
# ==============================================================================
def ensure_thinking_pulse_wav(duration_sec: float = 4.0) -> Path:
    """
    무음 구간 이탈을 막으면서 깊은 수학적 사고를 돕는 사색 사운드(순수 math.sin 합성):
    - 부드러운 Cmaj9 명상 화음(-29dB) + 1초 간격 은은한 목탁/차임 펄스(528Hz/792Hz) + 종료 직전 유레카 화음
    """
    dur_key = f"{duration_sec:.1f}".replace(".", "p")
    out_wav = AUDIO_CACHE_DIR / f"thinking_pulse_{dur_key}s.wav"
    if out_wav.exists() and out_wav.stat().st_size > 1000:
        return out_wav

    sr = 44100
    n_samples = max(1, int(sr * duration_sec))
    pad_freqs = (261.63, 329.63, 392.00, 493.88)  # C4, E4, G4, B4
    eureka_freqs = (523.25, 659.25, 783.99, 1046.50)  # C5, E5, G5, C6

    buf = bytearray()
    for i in range(n_samples):
        t = i / sr
        # 1) 은은한 앰비언트 패드
        env_pad = min(1.0, t / 0.25) * min(1.0, max(0.0, (duration_sec - t) / 0.25))
        sample = sum(math.sin(2.0 * math.pi * f * t) for f in pad_freqs) * 0.012 * env_pad

        # 2) 매 1.0초 정각 부드러운 사고 펄스 틱
        frac = t % 1.0
        if t < duration_sec - 0.45 and frac < 0.18:
            tick_env = math.exp(-frac * 26.0)
            sample += (0.048 * math.sin(2.0 * math.pi * 528.0 * frac) + 0.024 * math.sin(2.0 * math.pi * 792.0 * frac)) * tick_env

        # 3) 종료 직전 0.42초 유레카 차임
        rem = duration_sec - t
        if 0.0 <= rem <= 0.42:
            eu_t = 0.42 - rem
            eu_env = math.exp(-eu_t * 7.5)
            sample += sum(math.sin(2.0 * math.pi * ef * eu_t) for ef in eureka_freqs) * 0.022 * eu_env

        val = max(-32767, min(32767, int(sample * 32767)))
        buf += struct.pack("<h", val)

    with wave.open(str(out_wav), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        # stereo duplicate
        stereo = bytearray()
        for k in range(0, len(buf), 2):
            pair = buf[k : k + 2]
            stereo += pair + pair
        wf.writeframes(bytes(stereo))
    return out_wav


# ==============================================================================
# 3. Rule 28.1 무가림 100% 보장 '능동적 사고 정지(Active Pause)' 비디오 세그먼트 인코더
# ==============================================================================
def render_active_pause_margin_overlay_1080p(
    base_slide_frame: Image.Image,
    lang_code: str,
    prompt_text: str,
    badge_label: str,
    sec_left: int,
    total_sec: int,
) -> Image.Image:
    """
    중앙 오리지널 PDF 슬라이드 영역(y: 84 ~ 816)은 단 1픽셀도 건드리지 않고(Rule 28.1 100% 준수),
    오직 상단 헤더 배지(y: 12~60)와 하단 자막 리본(y: 826~1026)에만 능동적 사고 발문과
    실시간 카운트다운 게이지 바(Rule 37 블루·에메랄드·골드)를 렌더링합니다.
    """
    import min7014_video_maker as vmaker

    frame = base_slide_frame.copy()
    draw = ImageDraw.Draw(frame)
    W, _ = frame.size
    is_en = lang_code == "en"

    # 상단 우측 사고 배지 (y: 12~60 — PDF 밖)
    clean_badge = _clean_canvas_str(badge_label, lang_code)
    draw.rounded_rectangle([W - 600, 12, W - 22, 60], radius=12, fill=(5, 150, 105), outline=(250, 204, 21), width=2)
    draw.text((W - 580, 22), clean_badge, fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 20, bold=True))

    # 하단 자막·카운트다운 리본 (y: 826~1028 — 중앙 PDF y:86~810 완전 바깥, Rule 49.3 문장 절단 0% 자동 피팅!)
    draw.rounded_rectangle([36, 826, W - 36, 1026], radius=16, fill=(12, 22, 44), outline=(250, 204, 21), width=3)

    clean_p = _clean_canvas_str(prompt_text, lang_code)
    for fsize, w_ch in ((26, 84 if is_en else 54), (24, 92 if is_en else 60), (21, 104 if is_en else 68)):
        lines = textwrap.wrap(clean_p, width=w_ch)
        line_h = int(fsize * 1.34)
        if len(lines) * line_h <= 108 or fsize == 21:
            f_p = vmaker.get_font_for_lang(lang_code, fsize, bold=True)
            yc = 836
            for ln in lines[:3]:
                draw.text((64, yc), ln, fill=(254, 240, 138), font=f_p)
                yc += line_h
            break

    # 하단 사고 진행 게이지 바 (y: 950~994)
    bar_x1, bar_y1, bar_x2, bar_y2 = 64, 950, W - 64, 994
    draw.rounded_rectangle([bar_x1, bar_y1, bar_x2, bar_y2], radius=12, fill=(30, 41, 59), outline=(56, 189, 248), width=2)
    if sec_left > 0 and total_sec > 0:
        ratio = max(0.06, min(1.0, sec_left / float(total_sec)))
        fill_w = int((bar_x2 - bar_x1 - 8) * ratio)
        draw.rounded_rectangle([bar_x1 + 4, bar_y1 + 4, bar_x1 + 4 + fill_w, bar_y2 - 4], radius=9, fill=(5, 150, 105))
        timer_lbl = (
            f"[ACTIVE THINKING PAUSE] Sketch your idea first!  {sec_left}s  (Press SPACE if you need more time)"
            if is_en
            else f"[능동적 사고 시간] 먼저 스스로 떠올려 보세요!  {sec_left}초  (더 생각하려면 일시정지 SPACE)"
        )
    else:
        timer_lbl = (
            "[THINK FIRST] Listen to the question & observe the clean figure carefully..."
            if is_en
            else "[질문 경청] 보조선이 그어지기 전 도형을 보며 스스로 길을 먼저 찾아보세요..."
        )
    draw.text((bar_x1 + 22, bar_y1 + 9), timer_lbl, fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 22, bold=True))
    return frame


def encode_active_pause_segment_1080p(
    base_slide_frame: Image.Image,
    lang_code: str,
    voice_name: str,
    prompt_text: str,
    badge_label: str,
    pause_seconds: int,
    tmp_dir: Path,
    seg_prefix: str,
    ffmpeg_exe: str,
    ffprobe_exe: str,
    fps: int = 24,
    audio_rate: int = 44100,
    h264_high_profile: bool = False,
) -> tuple[Path, float]:
    """
    1) 발문 음성 구간(질문 경청 프레임) + 2) 실제 능동적 사고 카운트다운 구간(N초 -> 1초, 1초 단위 게이지 애니메이션 + 사색 펄스 사운드)을
    하나의 무결점 1080p H.264 세그먼트(.mp4)로 합성하여 반환합니다.
    """
    import min7014_video_maker as vmaker

    q_mp3 = tmp_dir / f"{seg_prefix}_q.mp3"
    vmaker.synthesize_tts_mp3_sync(prompt_text, voice_name, q_mp3, rate="+4%")
    q_dur = max(1.5, vmaker.get_media_duration_seconds(q_mp3, ffprobe_exe) + 0.25)

    v_flags = (
        ["-c:v", "libx264", "-profile:v", "high", "-level:v", "4.2", "-preset", "veryfast", "-tune", "stillimage", "-crf", "16", "-pix_fmt", "yuv420p", "-r", str(fps)]
        if h264_high_profile
        else ["-c:v", "libx264", "-preset", "ultrafast", "-tune", "stillimage", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(fps)]
    )

    # Part A: 질문 발화 세그먼트
    listen_img = render_active_pause_margin_overlay_1080p(
        base_slide_frame, lang_code, prompt_text, badge_label, sec_left=0, total_sec=pause_seconds
    )
    listen_png = tmp_dir / f"{seg_prefix}_listen.png"
    listen_mp4 = tmp_dir / f"{seg_prefix}_partA.mp4"
    listen_img.save(listen_png)
    subprocess.run(
        [
            ffmpeg_exe, "-y",
            "-loop", "1", "-t", f"{q_dur:.3f}", "-i", str(listen_png),
            "-i", str(q_mp3),
            *v_flags,
            "-c:a", "aac", "-b:a", "192k", "-ar", str(audio_rate), "-ac", "2",
            "-shortest", str(listen_mp4),
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    # Part B: 실제 N초 능동적 사고 정지 카운트다운 세그먼트
    pulse_wav = ensure_thinking_pulse_wav(float(pause_seconds))
    concat_lines = []
    last_png = None
    for s_left in range(pause_seconds, 0, -1):
        c_img = render_active_pause_margin_overlay_1080p(
            base_slide_frame, lang_code, prompt_text, badge_label, sec_left=s_left, total_sec=pause_seconds
        )
        c_png = tmp_dir / f"{seg_prefix}_cnt_{s_left}.png"
        c_img.save(c_png)
        concat_lines.append(f"file '{c_png.as_posix()}'\nduration 1.000")
        last_png = c_png
    if last_png is not None:
        concat_lines.append(f"file '{last_png.as_posix()}'")

    cnt_txt = tmp_dir / f"{seg_prefix}_cnt.txt"
    cnt_txt.write_text("\n".join(concat_lines) + "\n", encoding="utf-8")
    pause_mp4 = tmp_dir / f"{seg_prefix}_partB.mp4"
    subprocess.run(
        [
            ffmpeg_exe, "-y",
            "-f", "concat", "-safe", "0", "-i", str(cnt_txt),
            "-i", str(pulse_wav),
            *v_flags,
            "-c:a", "aac", "-b:a", "192k", "-ar", str(audio_rate), "-ac", "2",
            "-t", f"{float(pause_seconds):.3f}",
            str(pause_mp4),
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    # Part A + Part B 무손실 결합
    join_txt = tmp_dir / f"{seg_prefix}_join.txt"
    join_txt.write_text(f"file '{listen_mp4.as_posix()}'\nfile '{pause_mp4.as_posix()}'\n", encoding="utf-8")
    out_mp4 = tmp_dir / f"{seg_prefix}_active.mp4"
    subprocess.run(
        [ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", str(join_txt), "-c", "copy", str(out_mp4)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    tot_dur = vmaker.get_media_duration_seconds(out_mp4, ffprobe_exe)
    return out_mp4, tot_dur
