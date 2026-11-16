#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
math_issue_insight_creator.py
=============================
[수학 분야 실시간 이슈 × min7014.github.io 오리지널 자료 연계 — 차별화된 수학교육 통찰 영상 자동 제작 엔진]

핵심 철학 (Chairman min7014 수학교육 비전):
- 단순 입시 요령 암기나 가십성 이슈 요약을 넘어, 오늘날 수학계·과학기술계·교육 현장에서 화두가 되는 이슈를
  민은기 선생님이 직접 연구·작도한 오리지널 시각 증명 자료(https://min7014.github.io/ 847+ PDF)와 정밀 연결하여
  학생·교사·학부모에게 '수학교육의 본질과 차별화된 시각(공식 암기 너머의 기하학적 필연성·반례 사고·조건 변형)'을 제시합니다.

아키텍처 (100% 0-LLM-Credit 상시 자율 가동 · Rule 28/33/35/37/43/44/48/51/53 완전 준수):
1. LiveMathIssueRadar:
   - Google News(KO/EN 수학·수학교육·기하·미적분 RSS) + arXiv(math.HO / math.GM RSS) + 월별 수학교육 학사 화두 레이더 수집
   - 비수학·트레이딩(Rule 2) 및 외부 기관 등록상표(SAT/AMC/IB/Olympiad 등 · Rule 51) 기계적 원천 차단
2. OriginalVaultSemanticMatcher:
   - 실시간 수학 화두 키워드를 min7014.github.io 오리지널 시각 증명 PDF(scripts/*.json & min7014_deep_knowledge.json)와 시맨틱 매칭
3. 3-Act Pedagogical Insight Cinema (KO/EN 1080p 본편 + 9:16 Q-#Shorts 4종 자동 렌더링):
   - Act 1 (수학교육 화두 제기): 왜 지금 이 수학 이슈 앞에서 기존의 '기계적 공식 암기'가 한계에 부딪히는가?
   - Act 2 (오리지널 원문 1:1 무가림 직강): min7014.github.io 원본 PDF 전 페이지(1 Page = 1 Scene) 300 DPI + 메이플 가상 지휘봉(Rule 43)
   - Act 3 (차별화된 수학교육 시각 & 열린 발문): 교실과 학습을 바꾸는 수학교육적 통찰 요약 + 소크라테스 댓글 토론 질문
"""

import silent_subprocess  # noqa: F401 — Rule 48: 100% 무창(CREATE_NO_WINDOW) 실행 강제

import datetime
import json
import re
import shutil
import subprocess
import tempfile
import textwrap
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw

ROOT_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = ROOT_DIR / "video_lectures" / "scripts"
ISSUE_INSIGHT_DIR = ROOT_DIR / "youtube_uploads" / "issue_insight"
ISSUE_INSIGHT_DIR.mkdir(parents=True, exist_ok=True)
RADAR_STATE_FILE = ROOT_DIR / ".agents" / "math_issue_radar_state.json"

# ==============================================================================
# 1. 대표 플래그십 블루프린트 (실시간 핵심 화두 5선 × min7014 오리지널 12~15p 정밀 증명 PDF)
#    * Pillow 캔버스 내 U+2794(➔) 사용 금지(Rule 53 L7) -> 표준 화살표 U+2192(→)만 사용
# ==============================================================================
CURATED_ISSUE_INSIGHT_BLUEPRINTS = [
    {
        "slug": "2022051507",
        "issue_category_ko": "🧭 첨단 광학·우주 기술 이슈 × 기하 교육의 본질",
        "issue_category_en": "🧭 Space Optics & LiDAR Era × True Geometry Education",
        "issue_headline_ko": "우주망원경과 자율주행 광학 센서의 핵심 '타원 초점 반사' — 왜 교실에서는 방정식 대입만 외우게 할까?",
        "issue_headline_en": "From Space Telescopes to Optical Sensors: Why Do Classrooms Reduce Ellipses to Blind Algebra?",
        "old_view_ko": "기존 암기식 시각: x²/a² + y²/b² = 1 접선 공식과 판별식 D=0을 기계적으로 대입·계산",
        "old_view_en": "Rote Formula View: Memorizing x²/a² + y²/b² = 1 tangent equations & mechanical algebra",
        "new_insight_ko": "차별화된 수학교육 시각: 미분·판별식 계산 0줄! '거리 합 일정(PF₁+PF₂=2a)'과 대칭·최단거리 원리만으로 빛이 다른 초점으로 모이는 기하학적 필연성을 눈으로 재발명!",
        "new_insight_en": "Math-Ed Insight: Zero derivatives! Using PF₁+PF₂=2a & mirror shortest-path symmetry reveals WHY light MUST focus—geometry before formula!",
        "title_ko": "🧭 우주망원경의 비밀을 판별식 암기로 가르치시나요? 수식 0줄로 깨우치는 빛 반사 원리 | 타원에서의 빛 반사 시각적 증명",
        "title_en": "🧭 Telescope Optics Beyond Blind Algebra! Zero-Formula Proof | Ellipse Reflection",
        "short_title_ko": "❓ 수식 계산 0줄! 한 초점에서 쏜 빛이 반드시 다른 초점으로 모이는 진짜 이유? #Shorts",
        "short_title_en": "❓ Zero Algebra! Why Must Light from One Focus Hit the Other Focus? #Shorts",
        "act1_ko": "제임스 웹 우주망원경부터 첨단 광학 센서까지, 현대 과학에서 이차곡선의 초점 반사 원리가 끊임없이 주목받고 있습니다. 그런데 우리 수학교실에서는 왜 타원을 복잡한 방정식과 판별식 암기로만 가르칠까요? 미분도, 좌표 계산도 단 한 줄 쓰지 않고 빛이 왜 반드시 다른 초점으로 모이는지 본질을 꿰뚫어 봅니다!",
        "act1_en": "From space telescopes to precision optical sensors, focal reflection in conics powers modern science. Yet why do classrooms reduce ellipses to tedious coordinate algebra? With zero derivatives and zero discriminant calculations, let us discover the pure geometric reason light from one focus must reach the other!",
        "act3_ko": "방금 확인하셨듯 대수 방정식은 기하학적 진실을 사후에 기록한 결과물일 뿐입니다. 공식을 외우기 전에 대칭점 하나와 최단거리 직선이라는 기하학적 필연성을 먼저 눈으로 경험할 때, 학생에게 이차곡선은 암기 과목이 아니라 살아 움직이는 과학의 언어가 됩니다. 수학교육의 새로운 시각, 지금 구독으로 함께해 주세요!",
        "act3_en": "As we just saw, algebraic equations merely record a deeper geometric truth. When students experience mirror symmetry and shortest-path invariance BEFORE memorizing formulas, conic sections transform from rote drills into living mathematical insight. Subscribe now for distinctive perspectives in math education!",
        "comment_quiz_ko": "💬 [수학교육 열린 질문] 만약 빛이 출발하는 점이 초점이 아니라 타원 내부의 다른 점이라면 반사된 빛은 어디를 지날까요? 여러분의 직관을 댓글로 나눠 주세요! 🤩",
        "comment_quiz_en": "💬 [Open Math-Ed Question] What if a light ray starts between the two foci instead of at a focus—where will reflected rays pass? Share your geometric intuition below! 🤩",
    },
    {
        "slug": "2019072401",
        "issue_category_ko": "🧭 AI 추론 시대의 미적분 교육 대전환",
        "issue_category_en": "🧭 Rethinking Calculus Education in the AI Era",
        "issue_headline_ko": "AI가 미분 계산을 0.1초에 끝내는 시대 — 공식 f'(x)=2ax+b 암기 너머 인간이 길러야 할 미적분 통찰은?",
        "issue_headline_en": "When AI Differentiates in 0.1 Seconds: What Calculus Insight Still Belongs Uniquely to Humans?",
        "old_view_ko": "기존 암기식 시각: 지수를 앞으로 내리는 기계적 미분법(2ax+b)만 반복 훈련",
        "old_view_en": "Rote Formula View: Drilling power-rule differentiation without seeing graph symmetry",
        "new_insight_ko": "차별화된 수학교육 시각: 포물선의 대칭 구조 때문에 두 점 [a, b]의 할선 기울기와 '정확히 한가운데 중점 (a+b)/2'의 접선 기울기가 일치하는 구조적 필연성 발견!",
        "new_insight_en": "Math-Ed Insight: Parabolic symmetry forces the secant slope on [a, b] to match the tangent slope at the exact midpoint (a+b)/2!",
        "title_ko": "🧭 AI 시대에도 미분 공식만 외우게 할 건가요? 포물선 대칭이 숨긴 '중점 접선'의 필연성 | 평균변화율과 순간변화율 시각적 증명",
        "title_en": "🧭 Beyond Power-Rule Drills in the AI Era! Midpoint Symmetry | Parabola Tangent Proof",
        "short_title_ko": "❓ 포물선 두 점의 기울기와 정확히 같아지는 접선은 왜 항상 '한가운데 중점'일까? #Shorts",
        "short_title_en": "❓ Why Does a Parabola's Secant Slope Match the Exact Midpoint Tangent? #Shorts",
        "act1_ko": "인공지능이 복잡한 미분 계산을 0.1초 만에 끝내는 오늘날, 수학교육계에서는 인간이 진짜 배워야 할 미적분 문해력이 무엇인지 뜨거운 논의가 이어지고 있습니다. 기계적인 미분 공식을 적용하기 전에, 포물선의 할선과 접선 사이에 숨어 있는 놀라운 중점 대칭의 필연성을 시각적으로 발견해 볼까요?",
        "act1_en": "In an era where AI computes derivatives in milliseconds, math educators worldwide are asking what true calculus literacy means. Beyond mechanical power-rule drills, let us uncover why a parabola's average rate of change always equals its instantaneous rate at the exact midpoint!",
        "act3_ko": "기계적인 미분 계산은 컴퓨터가 더 빠르지만, 그래프의 대칭 구조 속에서 왜 중점의 접선이 할선과 평행할 수밖에 없는지 꿰뚫어 보는 눈은 오직 깊은 시각적 사고에서만 길러집니다. 계산 기술자가 아닌 수학적 구조를 읽는 학습자를 키우는 시각 증명, 지금 구독하고 교실과 학습에 바로 활용해 보세요!",
        "act3_en": "Machines can differentiate faster than any human, but seeing WHY parabolic symmetry locks the midpoint tangent parallel to the secant builds genuine mathematical structure sense. Subscribe right now for visual proofs that elevate math education beyond rote calculation!",
        "comment_quiz_ko": "💬 [수학교육 열린 질문] 이차함수 포물선에서는 항상 '중점'에서 기울기가 일치하는데, 만약 삼차함수라면 여전히 중점에서 항상 일치할까요? 반례나 생각을 댓글로 남겨주세요! 🤩",
        "comment_quiz_en": "💬 [Open Math-Ed Question] The midpoint rule always holds for parabolas—does it still always hold for cubic curves? Share a counterexample or insight below! 🤩",
    },
    {
        "slug": "2017031401",
        "issue_category_ko": "🧭 끊이지 않는 무한소수 논쟁 × 초·중·고 수직 계통성",
        "issue_category_en": "🧭 The Endless Repeating Decimal Debate × Concept Genealogy",
        "issue_headline_ko": "해마다 온라인을 달구는 '0.999... = 1'과 순환소수 논쟁 — 왜 10x 빼기 x 공식만 가르치면 극한에서 흔들릴까?",
        "issue_headline_en": "Why the '0.999... = 1' Debate Never Ends: Moving Past the 10x - x Trick to True Number Sense",
        "old_view_ko": "기존 암기식 시각: 분모에 9와 0을 기계적으로 적는 순환소수 변환 공식 암기",
        "old_view_en": "Rote Formula View: Memorizing 9s-and-0s denominator rules without remainder structure",
        "new_insight_ko": "차별화된 수학교육 시각: 나눗셈 나머지의 유한성(비둘기집 원리)으로 왜 모든 유리수가 유한소수 또는 순환소수가 될 수밖에 없는지 수체계의 뿌리를 직관화!",
        "new_insight_en": "Math-Ed Insight: Finite division remainders (Pigeonhole Principle) explain WHY every rational number must terminate or repeat!",
        "title_ko": "🧭 순환소수 고칠 때 무작정 99만 쓰게 하시나요? 무한소수 논쟁을 끝내는 나눗셈 나머지의 비밀 | 유리수와 순환소수 시각적 증명",
        "title_en": "🧭 Beyond the 99x Trick: Finite Remainders & Repeating Decimals | Visual Math Proof",
        "short_title_ko": "❓ 분수를 소수로 나눌 때 왜 언젠가는 반드시 같은 숫자가 반복될 수밖에 없을까? #Shorts",
        "short_title_en": "❓ Why MUST Long Division of Any Fraction Terminate or Repeat Forever? #Shorts",
        "act1_ko": "온라인 수학 커뮤니티와 교실에서 해마다 끊이지 않는 단골 이슈가 바로 무한소수와 순환소수의 정체입니다. 많은 학생이 분모에 구십구나 구백구십을 적는 변환 요령은 외우지만, 정작 왜 분수를 나눗셈하면 예외 없이 순환마디가 생길 수밖에 없는지는 설명하지 못합니다. 초등 나눗셈의 나머지 원리로 수체계의 본질을 열어 봅니다!",
        "act1_en": "Every year, repeating decimals and infinite decimal debates spark intense discussion online and in classrooms. Students memorize shortcut rules with nines in the denominator, yet rarely see WHY dividing two integers must always repeat. Let us unlock the deeper remainder principle step by step!",
        "act3_ko": "나누는 수보다 작은 나머지의 개수는 유한하기 때문에, 나눗셈이 끝나지 않는다면 언젠가 반드시 같은 나머지를 다시 만나 순환할 수밖에 없습니다. 초등 나눗셈에서 중등 유리수, 고등 무한급수까지 하나로 꿰뚫는 수직 계통성의 시선이야말로 진짜 수학의 힘입니다!",
        "act3_en": "Because there are only finitely many possible non-zero remainders smaller than the divisor, any non-terminating division is mathematically forced to revisit a previous remainder and cycle forever. Connecting elementary division to infinite series is the heart of meaningful math education!",
        "comment_quiz_ko": "💬 [5초 원리 발문] 어떤 기약분수를 7로 나눌 때 생길 수 있는 순환마디의 최대 길이는 몇 자리일까요? 나눗셈 나머지 개수로 추론해 댓글로 남겨주세요! 🤩",
        "comment_quiz_en": "💬 [5-Sec Concept Prompt] When dividing by 7, what is the maximum possible length of the repeating block—and why? Drop your reasoning in the comments! 🤩",
    },
    {
        "slug": "2016012801",
        "issue_category_ko": "🧭 고교-대학 심화 탐구(세특·논술) 화두 × 기하 직관",
        "issue_category_en": "🧭 Advanced Inquiry & Proof Literacy × Geometric Calculus",
        "issue_headline_ko": "심화 수학 탐구에서 단골로 지적되는 '무비판적 공식 남용' — 그 뿌리인 코시의 평균값 정리를 눈으로 본 적 있나요?",
        "issue_headline_en": "Stop Using Limit Shortcuts Blindly: Have You Ever SEEN Cauchy's Mean Value Theorem Geometrically?",
        "old_view_ko": "기존 암기식 시각: 보조함수 h(x)를 외워서 대입하는 무미건조한 대수 증명 암기",
        "old_view_en": "Rote Formula View: Memorizing an artificial auxiliary function h(x) with zero geometric meaning",
        "new_insight_ko": "차별화된 수학교육 시각: 두 함수 (g(t), f(t))를 평면 위 움직이는 점의 매개변수 궤적으로 보면, 코시 평균값 정리는 곧 '양 끝점 할선과 평행한 접선'이라는 한 장의 그림이 됩니다!",
        "new_insight_en": "Math-Ed Insight: Plotting (g(t), f(t)) as a parametric curve turns Cauchy's Mean Value Theorem into a clear parallel-tangent picture!",
        "title_ko": "🧭 보조함수 억지 암기는 그만! 매개변수 곡선 한 장으로 꿰뚫는 미적분 심화 탐구의 정수 | 코시의 평균값 정리 시각적 증명",
        "title_en": "🧭 No More Artificial Helper Functions! Parametric Curve | Cauchy Mean Value Theorem",
        "short_title_ko": "❓ 외우기만 했던 코시의 평균값 정리, 좌표평면 곡선 하나로 단숨에 이해된다면? #Shorts",
        "short_title_en": "❓ Cauchy's Mean Value Theorem Made Obvious by One Parametric Curve! #Shorts",
        "act1_ko": "고등학교 심화 수학 탐구와 대학 미적분학 연결 과정에서 가장 자주 등장하는 화두가 바로 극한 편법 공식의 무비판적 남용과 그 엄밀한 뿌리인 코시의 평균값 정리입니다. 교과서에서 갑자기 튀어나오는 보조함수를 억지로 외우는 대신, 평면 위 곡선의 기하학적 움직임으로 그 필연성을 직접 확인해 보겠습니다!",
        "act1_en": "In advanced high-school inquiry and university calculus transitions, blind formula use often hides the foundational pillar underneath: Cauchy's Mean Value Theorem. Instead of memorizing an artificial helper function, let us see why a single parametric curve makes this theorem geometrically inevitable!",
        "act3_ko": "두 함수를 각각 가로축과 세로축 좌표로 놓는 발상의 전환 하나로, 추상적인 분수 등식이 곡선 위 할선과 평행한 접선이라는 투명한 기하학으로 바뀝니다. 왜 이 보조함수가 탄생했는지 기원을 비춰 주는 것, 그것이 암기를 통찰로 바꾸는 수학교육의 역할입니다!",
        "act3_en": "By viewing the two functions as horizontal and vertical coordinates of a moving point, an abstract quotient equation transforms into a crystal-clear parallel tangent on a curve. Revealing WHY auxiliary functions exist turns memorization into lasting mathematical insight!",
        "comment_quiz_ko": "💬 [심화 탐구 발문] 코시의 평균값 정리에서 만약 g(x) = x로 놓으면 우리가 잘 아는 어떤 정리로 즉시 바뀌게 될까요? 댓글로 남겨보세요! 🤩",
        "comment_quiz_en": "💬 [Inquiry Question] In Cauchy's Mean Value Theorem, what familiar theorem appears immediately when we set g(x) = x? Share below! 🤩",
    },
    {
        "slug": "2017091006",
        "issue_category_ko": "🧭 낯선 문제 앞 공식 붕괴 현상 × 보조선 구성주의",
        "issue_category_en": "🧭 Formula Fragility vs. Constructive Auxiliary Thinking",
        "issue_headline_ko": "시험만 끝나면 반복되는 '공식이 안 떠올랐어요' — 세 변 6·5·4 삼각형 넓이, 복잡한 근호 공식 없이 어떻게 꿰뚫을까?",
        "issue_headline_en": "When Memorized Area Formulas Blank Out: Unlocking a 6-5-4 Triangle with One Structural Altitude",
        "old_view_ko": "기존 암기식 시각: 복잡한 헤론의 공식이나 제2코사인법칙에 숫자를 대입해 기계적 계산",
        "old_view_en": "Rote Formula View: Plugging numbers into Heron's formula without structural decomposition",
        "new_insight_ko": "차별화된 수학교육 시각: 수선 보조선 단 한 줄로 직각삼각형 두 개로 쪼개어 피타고라스 관계만으로 넓이를 스스로 구성해 내는 힘!",
        "new_insight_en": "Math-Ed Insight: Dropping ONE altitude splits the unknown triangle into two right triangles—reconstructing area from first principles!",
        "title_ko": "🧭 헤론의 공식 깜빡하면 포기하실 건가요? 수선 1줄로 공식을 스스로 재발명하는 힘 | 6-5-4 삼각형의 넓이 시각적 증명",
        "title_en": "🧭 Forgot Heron's Formula? Rebuild Area with One Altitude! | 6-5-4 Triangle Proof",
        "short_title_ko": "❓ 세 변이 6, 5, 4인 삼각형 넓이! 어려운 공식 없이 수선 1줄로 구하는 법? #Shorts",
        "short_title_en": "❓ Sides 6, 5, 4—How Do You Find the Area Without Heron's Formula? #Shorts",
        "act1_ko": "큰 시험이 끝날 때마다 교육 현장에서 반복되는 이야기가 있습니다. 조금만 낯선 조건이 나오면 외웠던 공식이 머릿속에서 하얗게 지워진다는 것입니다. 세 변의 길이가 육, 오, 사인 삼각형의 넓이를 구할 때, 복잡한 공식을 외우지 않고도 초중등 피타고라스 원리만으로 스스로 길을 여는 구성적 사고를 살펴봅니다!",
        "act1_en": "After every major mathematics assessment, students say the same thing: under pressure, memorized formulas vanish. Given a triangle with sides 6, 5, and 4, how can you reconstruct its exact area from first principles without Heron's formula? Let us watch one altitude unlock everything!",
        "act3_ko": "공식 백 개를 외운 학생은 백한 번째 낯선 도형 앞에서 멈추지만, 수선 한 줄을 내려 직각삼각형 두 개로 분해할 줄 아는 학생은 언제든 필요한 식을 스스로 만들어 냅니다. 죽은 공식 전달이 아닌 살아있는 문제 해결력을 기르는 수학교육, 구독으로 함께해 주세요!",
        "act3_en": "Memorizing a hundred formulas fails on the hundred-and-first unfamiliar figure, whereas knowing how to drop one altitude empowers students to rebuild formulas anytime. Subscribe to @min7014_ai for math education that builds resilient thinkers!",
        "comment_quiz_ko": "💬 [열린 발문] 세 변이 6, 5, 4인 삼각형에서 가장 큰 각과 가장 작은 각 사이에는 어떤 특별한 배수 관계가 숨어 있을까요? 댓글로 추론해 보세요! 🤩",
        "comment_quiz_en": "💬 [Bonus Discovery] In a 6-5-4 triangle, there is a surprising exact ratio between two of its angles—can you spot or guess it? Comment below! 🤩",
    },
    {
        "slug": "2022040501",
        "issue_category_ko": "🧭 스마트 안경 시험 논란 시대 × AI가 대신할 수 없는 작도 사고력",
        "issue_category_en": "🧭 Wearable AI Exam Era × Irreplaceable Geometric Construction",
        "issue_headline_ko": "카메라로 찍어 3초 만에 객관식 답을 듣는 스마트 안경 논란 — 수식도 보기도 없는 '순수 포물선 곡선' 하나만 주어지면 어떻게 될까?",
        "issue_headline_en": "When Wearable AI Reads Formula Tests in Seconds: What Happens When Only a Pure Curve Is Given with Zero Equations?",
        "old_view_ko": "기존 암기식 평가: y² = 4px 식에 숫자를 대입해 객관식 번호(①~⑤)로 초점 좌표를 찍는 시험",
        "old_view_en": "Rote Formula Exam: Plugging numbers into y² = 4px to pick a multiple-choice focus coordinate",
        "new_insight_ko": "차별화된 수학교육 시각: 방정식도 좌표축도 없는 포물선 위에서 평행현의 중점 자취와 대칭 원리만으로 대칭축·초점·준선을 손수 복원해 내는 동적 작도 역량!",
        "new_insight_en": "Math-Ed Insight: Reconstructing the axis, focus, and directrix from a bare parabola via parallel-chord midpoints and pure geometric symmetry!",
        "title_ko": "🧭 AI 안경도 절대 못 베끼는 진짜 수학 문제! 식 없는 포물선에서 초점·준선 찾아내기 | 포물선 작도 시각적 증명",
        "title_en": "🧭 The Math Test Wearable AI Cannot Cheat! Finding Focus & Directrix from a Bare Parabola",
        "short_title_ko": "❓ 수식도 좌표도 없는 포물선 그림 하나에서 '초점'을 어떻게 작도로 찾아낼까? #Shorts",
        "short_title_en": "❓ Zero Equations, Zero Axes! How Do You Construct a Parabola's Focus by Hand? #Shorts",
        "act1_ko": "최근 카메라로 시험지를 비추어 객관식 정답을 귓속말로 전달받는 스마트 안경 부정행위가 교육계의 큰 화두가 되었습니다. 이 현상은 사실 오지선다와 공식 대입에 머물러 있던 기존 평가 방식에 근본적인 질문을 던지고 있습니다. 만약 수식도, 좌표축도, 객관식 보기도 없이 오직 포물선 곡선 하나만 그려진 종이 위에서 대칭축과 초점, 준선을 직접 작도하라고 하면 어떻게 될까요?",
        "act1_en": "Recent exam controversies involving wearable smart glasses expose a deeper truth: multiple-choice formula drills can be answered by a camera in seconds. What happens instead when an assessment gives zero equations, zero coordinates, and zero answer choices—only a bare parabola curve—and asks you to construct its axis, focus, and directrix from pure geometric principles?",
        "act3_ko": "평행한 두 현의 중점을 이어 대칭축의 방향을 잡고, 직각과 반사 대칭의 성질로 초점과 준선을 한 땀 한 땀 복원하는 과정은 결코 귓속말 숫자 하나로 대신할 수 없습니다. 전파를 막는 단속을 넘어, 학생이 직접 보조선을 긋고 원리를 구성하게 만드는 평가의 전환이야말로 인공지능 시대 수학교육이 나아갈 진짜 해답입니다!",
        "act3_en": "Connecting midpoints of parallel chords and using reflection symmetry to locate the focus and directrix can never be whispered as a multiple-choice number. Moving from rote answer checking to hands-on geometric construction is the true future of mathematics education in the AI era!",
        "comment_quiz_ko": "💬 [수학교육 열린 발문] 만약 포물선이 아니라 '원 둘레의 일부(호)'만 그려져 있다면, 원의 중심은 어떤 두 선을 그어 찾을 수 있을까요? 댓글로 작도 아이디어를 들려주세요! 🤩",
        "comment_quiz_en": "💬 [Open Construction Prompt] If you are given only a circular arc instead of a parabola, which two lines would you construct to find its center? Share your idea below! 🤩",
    },
]

# ==============================================================================
# 2. 실시간 수학·수학교육 이슈 레이더 (0-LLM-Credit RSS + 학사 시즌 캘린더)
# ==============================================================================
LIVE_MATH_RSS_FEEDS = [
    ("google_news_ko_edunews", "https://news.google.com/rss/search?q=%EC%88%98%ED%95%99%EA%B5%90%EC%9C%A1+OR+%EC%84%9C%EC%88%A0%ED%98%95+%EC%88%98%ED%95%99+OR+%EC%8A%A4%EB%A7%88%ED%8A%B8+%EC%95%88%EA%B2%BD+%EC%8B%9C%ED%97%98+OR+%EC%88%98%EB%A6%AC%EB%85%BC%EC%88%A0+OR+%EA%B3%A0%EA%B5%90%ED%95%99%EC%A0%90%EC%A0%9C+%EC%88%98%ED%95%99&hl=ko&gl=KR&ceid=KR:ko"),
    ("google_news_ko_mathedu", "https://news.google.com/rss/search?q=%EC%88%98%ED%95%99+%EC%82%AC%EA%B3%A0%EB%A0%A5+OR+%EA%B8%B0%ED%95%98+%EC%A7%81%EA%B4%80+OR+%EC%88%98%EB%8A%A5+%EC%88%98%ED%95%99+%EB%B3%80%EB%B3%84%EB%A0%A5+OR+%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5+%EC%88%98%ED%95%99%EA%B5%90%EC%8B%A4&hl=ko&gl=KR&ceid=KR:ko"),
    ("google_news_en_mathedu", "https://news.google.com/rss/search?q=%22mathematics+education%22+OR+%22math+assessment%22+OR+%22visual+proof%22+OR+%22AI+in+math+education%22&hl=en-US&gl=US&ceid=US:en"),
    ("arxiv_math_ho", "https://export.arxiv.org/rss/math.HO"),
]

SEASONAL_MATH_ED_ISSUES = {
    1: ("새 학년 수학 선행학습 열풍 vs 개념 뿌리 이해", "선행 진도 속도전보다 직전 학년 기하·수체계 연결고리가 성적을 좌우하는 이유", ["제곱근", "인수분해", "피타고라스", "유리수"]),
    2: ("새 학기 수학 불안감(수포자 예방) 화두", "추상 기호가 두려운 학생에게 도형 넓이와 시각적 모델이 주는 인지적 디딤돌", ["곱셈공식", "정사각형", "방정식", "함수"]),
    3: ("3·14 파이데이(Pi Day) & 첫 학력평가 직관 화두", "원주율 파이와 원의 성질을 단순 수치 3.14 암기가 아닌 동적 기하로 보는 시선", ["원주각", "원의 접선", "부채꼴", "삼각비"]),
    4: ("중간고사 서술형·증명 평가 확대 이슈", "감점 없는 서술형 논리의 핵심 — 결과 공식이 아닌 가정에서 결론으로 가는 시각적 필연성", ["이등변삼각형", "내심", "외심", "미분계수"]),
    5: ("인공지능·데이터 시대의 수학 문해력 화두", "기계가 대신할 수 없는 조건 해석과 반례 추론 능력 기르기", ["평균변화율", "부등식", "극한", "확률"]),
    6: ("상반기 모의평가 이후 킬러·준킬러 기하 추론 화두", "복잡한 계산 늪을 단숨에 건너게 하는 제1보조선 발견의 원리", ["원주각", "사인법칙", "코사인법칙", "접선"]),
    7: ("여름방학 수학 심화 탐구·세특 주제 선정 이슈", "교과서 정리에서 조건 하나를 바꿔 나만의 정리를 재발명하는 What-If-Not 탐구법", ["타원", "포물선", "쌍곡선", "체바"]),
    8: ("2학기 도형·미적분 단원 급격한 체감 난이도 상승 이슈", "수식 전개 이전에 그래프 대칭과 넓이 보존으로 개념 장벽 낮추기", ["정적분", "구분구적", "접선", "닮음"]),
    9: ("하반기 핵심 모의평가 & 수리논술 시즌 화두", "당연해 보이는 직관의 함정을 깨는 엄밀한 정의와 시각적 반례", ["평균값 정리", "연속", "극한", "수열"]),
    10: ("실전 마무리 시즌 — 공식 망각을 이기는 원리 구조화", "시험장 긴장 속에서도 흔들리지 않는 도형 불변량과 대칭 사고", ["내접원", "외접원", "벡터", "정사영"]),
    11: ("11월 대입 시험 직후 '유형 암기 붕괴 vs 본질적 수학 사고력' 대논쟁", "낯선 신유형 앞에서도 무너지지 않는 힘은 유형 암기가 아니라 시각적 원리 재발명에서 나온다", ["원주각", "접선", "타원", "평균변화율", "넓이"]),
    12: ("학년말 학생부 수학 세특·창의 산출물 작성 시즌", "베끼기식 보고서를 넘어 하나의 시각적 증명에서 새 질문을 여는 진짜 수학 탐구", ["피타고라스", "황금비", "코시", "수열의 합"]),
}

CONCEPT_KEYWORD_BRIDGE = [
    (("안경", "웨어러블", "부정행위", "객관식", "오지선다", "5지선다", "wearable", "glasses", "cheating", "multiple choice"), ["작도", "포물선", "타원", "빛 반사", "자취"]),
    (("서술형", "논술", "수행평가", "구술", "면접", "과정중심", "정당화", "essay", "oral", "assessment"), ["평균값 정리", "코시", "원주각", "이등변삼각형", "체바"]),
    (("디지털교과서", "환각", "생성형", "문해력", "기초학력", "고교학점제", "curriculum", "literacy", "edtech"), ["피타고라스", "제곱근", "평균변화율", "순환소수", "삼각비"]),
    (("타원", "초점", "반사", "망원경", "광학", "ellipse", "focus", "optical", "reflection"), ["타원", "초점", "빛 반사", "이차곡선"]),
    (("포물선", "안테나", "투사체", "parabola", "trajectory"), ["포물선", "준선", "평균변화율"]),
    (("미분", "변화율", "최적화", "인공지능", "경사", "derivative", "calculus", "optimization", "ai"), ["미분", "평균변화율", "접선", "평균값 정리"]),
    (("적분", "넓이", "부피", "아르키메데스", "integral", "quadrature", "area"), ["정적분", "넓이", "삼각형의 넓이", "피타고라스"]),
    (("원", "각도", "회전", "대칭", "기하", "circle", "geometry", "symmetry", "angle"), ["원주각", "원의 접선", "이등변삼각형", "체바"]),
    (("소수", "유리수", "무리수", "무한", "수체계", "prime", "rational", "infinite", "number"), ["유리수", "순환소수", "제곱근", "무리수"]),
    (("극한", "수렴", "연속", "반례", "limit", "continuity", "counterexample", "proof"), ["극한", "평균값 정리", "부등식"]),
]

NON_ACADEMIC_NOISE_TOKENS = ("정치", "연예", "스포츠중계", "election", "celebrity", "gossip")


def _is_pure_math_domain_text(text: str) -> bool:
    low = str(text or "").lower()
    if any(tok in low for tok in NON_ACADEMIC_NOISE_TOKENS):
        return False
    try:
        import auditor
        if auditor.FORBIDDEN_TRADING_DOMAIN_RE.search(text):
            return False
    except Exception:
        pass
    return True


def _clean_rss_headline(raw_title: str) -> str:
    t = re.sub(r"\s+-\s+[^-]+$", "", str(raw_title or "").strip())
    t = re.sub(r"<[^>]+>", "", t).strip()
    try:
        import auditor
        t = auditor.sanitize_and_gate_upload_payload(t, "", [])["title"]
    except Exception:
        pass
    return t[:110]


def scan_live_math_issues(timeout: int = 8) -> dict:
    """
    외부 RSS(Google News 수학/수학교육 KO·EN + arXiv math.HO)와 월별 수학교육 화두 캘린더를 스캔하여
    저작권·상표권·도메인 무결성 필터를 통과한 순수 수학/수학교육 화두만 추출합니다 (0 LLM 크레딧).
    """
    month = datetime.datetime.now().month
    s_title, s_insight, s_keywords = SEASONAL_MATH_ED_ISSUES.get(month, SEASONAL_MATH_ED_ISSUES[11])
    discovered = [
        {
            "source": "seasonal_math_ed_calendar",
            "topic_theme": s_title,
            "pedagogical_focus": s_insight,
            "matched_keywords": s_keywords,
        }
    ]

    for feed_id, url in LIVE_MATH_RSS_FEEDS:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                xml_bytes = resp.read()
            root = ET.fromstring(xml_bytes)
            items = root.findall(".//item")[:8]
            for it in items:
                raw_t = (it.findtext("title") or "").strip()
                clean_t = _clean_rss_headline(raw_t)
                if not clean_t or not _is_pure_math_domain_text(clean_t):
                    continue
                low_t = clean_t.lower()
                matched_kws: list[str] = []
                for triggers, vault_kws in CONCEPT_KEYWORD_BRIDGE:
                    if any(tr in low_t for tr in triggers):
                        for vk in vault_kws:
                            if vk not in matched_kws:
                                matched_kws.append(vk)
                if not matched_kws and any(w in low_t for w in ("수학", "기하", "증명", "교육", "평가", "논술", "수업", "math", "geometry", "proof", "calculus", "theorem", "education", "assessment")):
                    matched_kws = list(s_keywords[:3])
                if matched_kws:
                    # 저작권 보호(Rule 51): 외부 기사 문장을 복제하지 않고 순수 수학 키워드 화두로만 추상화 기록
                    discovered.append(
                        {
                            "source": feed_id,
                            "topic_theme": f"실시간 수학·교육 화두 ({', '.join(matched_kws[:2])})",
                            "reference_signal": clean_t[:80],
                            "matched_keywords": matched_kws,
                        }
                    )
                if len(discovered) >= 12:
                    break
        except Exception:
            continue

    state = {
        "scanned_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "seasonal_theme": s_title,
        "discovered_count": len(discovered),
        "signals": discovered[:12],
    }
    RADAR_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    RADAR_STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    return state


def get_ranked_issue_insight_blueprints(max_dynamic: int = 80) -> list[dict]:
    """
    1순위: 정밀 설계된 5대 플래그십 수학 이슈 × 오리지널 증명 블루프린트
    2순위: 실시간 수학 이슈 레이더 키워드와 시맨틱 매칭된 min7014.github.io 847개 오리지널 PDF 동적 확장 블루프린트
    """
    curated_slugs = {b["slug"] for b in CURATED_ISSUE_INSIGHT_BLUEPRINTS}
    result = list(CURATED_ISSUE_INSIGHT_BLUEPRINTS)

    try:
        import min7014_video_maker as vm
        import youtube_self_evolving_engine as ysee

        radar = (
            json.loads(RADAR_STATE_FILE.read_text(encoding="utf-8"))
            if RADAR_STATE_FILE.exists()
            else scan_live_math_issues(timeout=6)
        )
        hot_kws: list[str] = []
        for sig in radar.get("signals") or []:
            for kw in sig.get("matched_keywords") or []:
                if kw not in hot_kws:
                    hot_kws.append(kw)
        seasonal_theme = radar.get("seasonal_theme") or "AI·변혁기 본질적 수학 사고력 화두"

        cands = []
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
            if not (6 <= len(pages) <= 22):
                continue
            raw_t = str(sdoc.get("title") or "")
            if any(skip in raw_t for skip in ("특강", "워크숍", "직무연수", "TikZ", "학년도")):
                continue
            kw_hits = sum(1 for kw in hot_kws if kw in raw_t)
            boost = ysee.get_slug_cluster_boost(f"{raw_t} {sdoc.get('title_en', '')}")
            cands.append((-(kw_hits * 2.0 + boost), abs(len(pages) - 12), sp.stem, sdoc))

        cands.sort(key=lambda x: (x[0], x[1], x[2]))
        for _, _, slug, sdoc in cands[:max_dynamic]:
            ko_t, en_t = vm.split_bilingual_title(sdoc.get("title", ""))
            ko_c = vm._smart_concise_topic_title(vm.latex_to_unicode_title(ko_t).strip(), max_len=26, lang="ko")
            en_c = vm._smart_concise_topic_title(
                vm.latex_to_unicode_title((sdoc.get("title_en") or en_t or ko_c).split("—")[0].strip()),
                max_len=38,
                lang="en",
            )
            result.append(
                {
                    "slug": slug,
                    "issue_category_ko": "🧭 오늘의 수학교육 화두 × 오리지널 시각 증명",
                    "issue_category_en": "🧭 Contemporary Math-Ed Issue × Original Visual Proof",
                    "issue_headline_ko": f"[{seasonal_theme}] 왜 '{ko_c}'을 결과 공식 암기로만 배우면 응용에서 무너질까?",
                    "issue_headline_en": f"Why Memorizing '{en_c}' as a Rote Formula Fails in Real Mathematical Thinking",
                    "old_view_ko": f"기존 암기식 시각: '{ko_c}'의 결과 식만 외워 기계적으로 숫자 대입",
                    "old_view_en": f"Rote View: Memorizing the final statement of '{en_c}' without structural proof",
                    "new_insight_ko": f"차별화된 수학교육 시각: 보조선과 단계별 시각 구조로 '{ko_c}'이 왜 성립할 수밖에 없는지 스스로 재발명!",
                    "new_insight_en": f"Math-Ed Insight: Step-by-step visual structure reveals WHY '{en_c}' is inevitable!",
                    "title_ko": f"🧭 공식만 외우는 수학은 왜 무너질까? 수학교육의 눈으로 다시 보는 {ko_c} | 단계별 시각적 증명",
                    "title_en": f"🧭 Why Rote Formulas Fail: Rediscovering {en_c} Visually | Math Education Insight",
                    "short_title_ko": f"❓ 공식 암기 없이 '{ko_c}'의 진짜 이유가 한눈에 보이시나요? #Shorts",
                    "short_title_en": f"❓ Beyond Formulas: Can You See WHY {en_c} Must Be True? #Shorts",
                    "act1_ko": f"오늘날 수학교육 현장에서 가장 중요하게 떠오른 화두는 결과 공식 암기가 아니라 개념의 탄생 과정을 스스로 재발명하는 힘입니다. 많은 학생이 {ko_c}을 결과 공식으로만 외우고 넘어가지만, 도형과 식의 연결 구조를 눈으로 확인하면 전혀 새로운 수학적 시야가 열립니다!",
                    "act1_en": f"One of the biggest questions in modern mathematics education is how to move students from fragile formula memorization to genuine conceptual discovery. Instead of treating {en_c} as a rule to memorize, let us trace step by step why it must hold!",
                    "act3_ko": f"공식을 수동적으로 암기할 때와 그 필연적 구조를 눈으로 재발명할 때 학생의 수학적 자존감과 응용력은 완전히 달라집니다. {ko_c}을 꿰뚫는 차별화된 수학교육 통찰, 지금 채널 구독으로 매일 만나 보세요!",
                    "act3_en": f"When learners visually reinvent {en_c} instead of memorizing it, fragile test habits turn into resilient mathematical thinking. Subscribe to @min7014_ai for daily visual proofs with deeper educational insight!",
                    "comment_quiz_ko": f"💬 [수학교육 열린 발문] 오늘 살펴본 '{ko_c}' 증명에서 조건 하나를 바꾼다면 어떤 새로운 성질이 만들어질까요? 댓글로 아이디어를 남겨주세요! 🤩",
                    "comment_quiz_en": f"💬 [Open Inquiry] Which visual step in '{en_c}' gave you the clearest 'aha' moment—and what happens if we alter one condition? Comment below! 🤩",
                }
            )
    except Exception:
        pass
    return result


# ==============================================================================
# 3. 고품격 아카데믹 통찰 프레임 & 썸네일 렌더러 (Rule 28 · Rule 37 · Rule 43 · L7 준수)
# ==============================================================================
def _encode_card_segment(frame_img: Image.Image, mp3_path: Path, out_mp4: Path, ffmpeg_exe: str, ffprobe_exe: str) -> float:
    import min7014_video_maker as vmaker

    dur = max(3.6, vmaker.get_media_duration_seconds(mp3_path, ffprobe_exe) + 0.35)
    png_p = out_mp4.with_suffix(".png")
    frame_img.save(png_p)
    subprocess.run(
        [
            ffmpeg_exe, "-y",
            "-loop", "1", "-t", f"{dur:.3f}", "-i", str(png_p),
            "-i", str(mp3_path),
            "-c:v", "libx264", "-preset", "ultrafast", "-tune", "stillimage", "-crf", "20",
            "-pix_fmt", "yuv420p", "-r", "24",
            "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
            "-shortest", str(out_mp4),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return dur


def _mix_calm_bgm(in_mp4: Path, out_mp4: Path, ffmpeg_exe: str) -> None:
    import min7014_video_maker as vmaker

    pad_wav = vmaker.ensure_ambient_pad_wav()
    subprocess.run(
        [
            ffmpeg_exe, "-y",
            "-i", str(in_mp4),
            "-stream_loop", "-1", "-i", str(pad_wav),
            "-filter_complex", "[1:a]volume=0.040[bgm];[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]",
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest",
            str(out_mp4),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _paste_clean_pdf_preview(canvas: Image.Image, pdf_doc: pymupdf.Document, box: tuple[int, int, int, int], page_idx: int) -> None:
    import min7014_video_maker as vmaker

    x1, y1, x2, y2 = box
    bw, bh = x2 - x1, y2 - y1
    p_i = min(len(pdf_doc) - 1, max(0, page_idx))
    pix = pdf_doc[p_i].get_pixmap(dpi=250)
    raw = vmaker._mask_pdf_bottom_author_bar(Image.frombytes("RGB", [pix.width, pix.height], pix.samples))
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((x1, y1, x2, y2), radius=20, fill=(255, 255, 255), outline=(56, 189, 248), width=4)
    pad = 16
    sc = min((bw - pad * 2) / raw.width, (bh - pad * 2) / raw.height)
    nw, nh = int(raw.width * sc), int(raw.height * sc)
    ox, oy = x1 + (bw - nw) // 2, y1 + (bh - nh) // 2
    canvas.paste(raw.resize((nw, nh), Image.Resampling.LANCZOS), (ox, oy))


def _clean_canvas_text(text: str, lang_code: str) -> str:
    """Pillow 캔버스 전용 텍스트 정화: 이모지 두부박스(□) 및 영어 화면 내 한글 태그 혼입을 100% 차단합니다."""
    is_en = lang_code == "en"
    rep_en = {
        "🧭": "[INSIGHT]",
        "🏛️": "[ARCHIVE]",
        "🏛": "[ARCHIVE]",
        "🎓": "[TAKEAWAY]",
        "🔔": "[SUBSCRIBE]",
        "💡": "[CLUE]",
        "💬": "[INQUIRY]",
        "👇": "[WATCH]",
        "🤩": "",
        "❓": "[Q]",
        "🔥": "[KEY]",
        "⚡": "[KEY]",
    }
    rep_ko = {
        "🧭": "[통찰]",
        "🏛️": "[원문]",
        "🏛": "[원문]",
        "🎓": "[핵심]",
        "🔔": "[구독]",
        "💡": "[단서]",
        "💬": "[열린발문]",
        "👇": "[본편보기]",
        "🤩": "",
        "❓": "[질문]",
        "🔥": "[핵심]",
        "⚡": "[직관]",
    }
    out = str(text or "")
    for k, v in (rep_en if is_en else rep_ko).items():
        out = out.replace(k, v)
    out = out.replace("\ufe0f", "").replace("\u2794", "→")
    return re.sub(r"\s{2,}", " ", out).strip()


def _draw_fitted_multiline(
    draw: ImageDraw.ImageDraw,
    text: str,
    lang_code: str,
    x: int,
    y_top: int,
    max_height: int,
    base_size: int = 34,
    fill=(255, 255, 255),
    base_width_ko: int = 18,
    base_width_en: int = 28,
) -> int:
    """문장이 중간에 절대 잘리지 않도록 줄 수와 높이에 맞춰 폰트 크기와 줄바꿈 폭을 자동 조절합니다 (Rule 49.3 절단 ZERO)."""
    import min7014_video_maker as vmaker

    clean_t = _clean_canvas_text(text, lang_code)
    is_en = lang_code == "en"
    for scale in (1.0, 0.88, 0.78, 0.68, 0.60):
        fsize = max(19, int(base_size * scale))
        w_chars = max(12, int((base_width_en if is_en else base_width_ko) / scale))
        lines = textwrap.wrap(clean_t, width=w_chars)
        line_h = int(fsize * 1.40)
        if len(lines) * line_h <= max_height or scale == 0.60:
            font = vmaker.get_font_for_lang(lang_code, fsize, bold=True)
            yc = y_top
            for ln in lines:
                if yc + fsize > y_top + max_height + 10:
                    break
                draw.text((x, yc), ln, fill=fill, font=font)
                yc += line_h
            return yc
    return y_top


def _best_climax_page_idx(pdf_doc: pymupdf.Document) -> int:
    """마지막 페이지가 AlgeoMath/GeoGebra URL 안내 슬라이드인 경우 그 직전 완성 도형 페이지를 자동 선택합니다."""
    n = len(pdf_doc)
    if n <= 1:
        return 0
    for cand in range(n - 1, max(0, n - 4) - 1, -1):
        txt = (pdf_doc[cand].get_text("text") or "").lower()
        if any(k in txt for k in ("algegomath", "algeomath", "geogebra", "click or paste url", "url search bar")):
            continue
        return cand
    return max(0, n - 2)


def render_issue_insight_thumbnail(bp: dict, pdf_doc: pymupdf.Document, lang_code: str, out_png: Path) -> None:
    """
    1280x720 고클릭률 수학교육 통찰 썸네일 (Rule 37 사색적 로열블루·인디고·골드 조화, 적색 0%, 절단 0%)
    좌측: min7014 오리지널 완성 도형 무크롭 배치 | 우측: 수학 이슈 키워드 & 암기 타파 통찰 대비
    """
    import min7014_video_maker as vmaker

    is_en = lang_code == "en"
    thumb = Image.new("RGB", (1280, 720), (9, 15, 32))
    d = ImageDraw.Draw(thumb)

    # 상단 로열 블루-인디고 학술 리본 (영어 썸네일에 한글 [탐구] 혼입 원천 차단)
    d.rounded_rectangle((28, 24, 1252, 108), radius=18, fill=(30, 58, 138), outline=(250, 204, 21), width=3)
    badge_txt = "[INSIGHT] MATH ISSUE × VISUAL PROOF" if is_en else "[수학교육 통찰] 수학 이슈 × 오리지널 시각 증명"
    d.text((54, 46), badge_txt, fill=(254, 240, 138), font=vmaker.get_font_for_lang(lang_code, 34, bold=True))

    # 좌측: 오리지널 클라이맥스 슬라이드
    climax_idx = _best_climax_page_idx(pdf_doc)
    _paste_clean_pdf_preview(thumb, pdf_doc, (32, 132, 650, 684), climax_idx)

    # 우측: 통념 타파 vs 본질 통찰 카드 (문장 절단 ZERO 자동 피팅)
    d.rounded_rectangle((676, 132, 1248, 684), radius=22, fill=(15, 23, 42), outline=(56, 189, 248), width=3)
    hl = bp["issue_headline_en"] if is_en else bp["issue_headline_ko"]
    _draw_fitted_multiline(
        d, hl, lang_code, x=704, y_top=162, max_height=224,
        base_size=33, fill=(255, 255, 255), base_width_ko=16, base_width_en=25,
    )

    d.rounded_rectangle((702, 404, 1222, 520), radius=16, fill=(2, 132, 199), outline=(254, 240, 138), width=2)
    tag1 = "Beyond Rote Formulas →" if is_en else "공식 암기 너머의 진짜 본질 →"
    tag2 = "100% Visual Invariance!" if is_en else "보조선·대칭으로 한눈에 증명!"
    d.text((726, 422), tag1, fill=(254, 240, 138), font=vmaker.get_font_for_lang(lang_code, 26, bold=True))
    d.text((726, 466), tag2, fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 28, bold=True))

    d.rounded_rectangle((702, 548, 1222, 650), radius=16, fill=(5, 150, 105))
    sub_txt = "[PROOF] Original Visual Archive" if is_en else "[증명] 수학교육의 새로운 시선"
    d.text((728, 580), sub_txt, fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 29, bold=True))

    out_png.parent.mkdir(parents=True, exist_ok=True)
    thumb.save(out_png)


def _fmt_mmss(sec: float) -> str:
    s = max(0, int(round(sec)))
    return f"{s // 60:02d}:{s % 60:02d}"


def render_issue_insight_bundle(bp: dict, lang_code: str = "ko") -> dict:
    """
    단일 수학 이슈 × 오리지널 자료 블루프린트에 대해 [능동적 수학 사고 4단계 엔진(active_thinking_engine)]을 결합하여 렌더링:
    1) 1080p 16:9 본편:
       - Act 1: 수학 이슈 화두 제기 + [직관 예측 선택 A vs B] + 3초 예측 선택 카운트다운
       - Act 2: 원본 PDF 전 페이지 1:1 무생략 직강(Rule 28.4) + [결정적 보조선 직전 '백지 도형' 4초 발상 정지] + [결론 직전 3초 근거 추론] + 가상 지휘봉(Rule 43)
       - Act 3: 차별화된 수학교육 통찰 + [라카토스 반례·경계 실험 & What-If-Not 조건 변형 전이]
    2) 1080x1920 9:16 능동 사고형 Q-#Shorts (<46s):
       - Scene 1: 이슈 & 예측 질문 + 2초 사고 타이머 -> Scene 2/3: 오리지널 결정적 단서 2장 -> Scene 4: 조건 변형 통찰 & 본편 유도
    """
    import active_thinking_engine as ate
    import min7014_video_maker as vmaker

    slug = bp["slug"]
    sp = SCRIPTS_DIR / f"{slug}.json"
    regenerated_script = False
    if not sp.exists():
        vmaker.generate_or_update_script(slug, target_langs=["ko", "en"])
        regenerated_script = True
    sdoc = json.loads(sp.read_text(encoding="utf-8"))
    pdf_bytes, _ = vmaker.load_or_build_topic_pdf_bytes(sdoc.get("pdf_url", ""), slug)
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")

    # Rule 28.4: 과거 묶음(축약) 대본 발견 시 즉시 전체 페이지 1:1 정밀 대본으로 자동 복원!
    if len(doc) <= 60 and len(sdoc.get("pages") or []) != len(doc):
        sdoc = vmaker.generate_or_update_script(slug, target_langs=["ko", "en"])
        regenerated_script = True

    if regenerated_script:
        try:
            import auditor
            auditor.run_full_7layer_audit(check_live_youtube=False, auto_fix=True)
            sdoc = json.loads(sp.read_text(encoding="utf-8"))
        except Exception:
            pass

    ffmpeg_exe = shutil.which("ffmpeg")
    ffprobe_exe = shutil.which("ffprobe")
    voice_name = vmaker.GLOBAL_VOICE_MAP.get(lang_code, vmaker.GLOBAL_VOICE_MAP["en"])["voice"]
    is_en = lang_code == "en"

    long_mp4 = ISSUE_INSIGHT_DIR / f"{slug}_issue_{lang_code}.mp4"
    long_thumb = ISSUE_INSIGHT_DIR / f"{slug}_issue_{lang_code}_thumb.png"
    short_mp4 = ISSUE_INSIGHT_DIR / f"{slug}_issue_short_{lang_code}.mp4"

    render_issue_insight_thumbnail(bp, doc, lang_code, long_thumb)

    pages = sdoc.get("pages") or []
    all_indices = list(range(len(pages)))
    act_bp = ate.build_active_thinking_blueprint(slug, sdoc)
    crux_idx = act_bp["crux_idx"]
    justify_idx = act_bp["justify_idx"]
    pre_crux_preview_idx = min(len(doc) - 1, max(1 if len(doc) > 2 else 0, crux_idx - 1))
    climax_preview_idx = _best_climax_page_idx(doc)

    tmp_dir = Path(tempfile.mkdtemp(prefix=f"issue_ins_{slug}_{lang_code}_", dir=str(ROOT_DIR / ".temp") if (ROOT_DIR / ".temp").exists() else None))
    try:
        # ==================== A. 1080p 16:9 능동적 수학 사고 통찰 본편 ====================
        long_segs: list[Path] = []
        cursor_t = 0.0
        chapter_lines: list[str] = [
            f"00:00 | {'Math Issue & Active Prediction (A vs B)' if is_en else '오늘의 수학 화두 & A vs B 직관 예측 선택'}"
        ]

        # [Act 1] 오늘의 수학·교육 이슈 제기 & [능동적 예측 선택 A vs B] + 3초 예측 타이머
        act1_img = Image.new("RGB", (1920, 1080), (9, 14, 28))
        d1 = ImageDraw.Draw(act1_img)
        d1.rounded_rectangle((48, 36, 1872, 138), radius=20, fill=(30, 58, 138), outline=(250, 204, 21), width=3)
        d1.text(
            (80, 66),
            _clean_canvas_text(bp["issue_category_en"] if is_en else bp["issue_category_ko"], lang_code),
            fill=(254, 240, 138),
            font=vmaker.get_font_for_lang(lang_code, 35, bold=True),
        )
        _paste_clean_pdf_preview(act1_img, doc, (56, 174, 900, 920), pre_crux_preview_idx)

        d1.rounded_rectangle((936, 174, 1864, 920), radius=24, fill=(15, 23, 42), outline=(56, 189, 248), width=3)
        hl_txt = bp["issue_headline_en"] if is_en else bp["issue_headline_ko"]
        _draw_fitted_multiline(
            d1, hl_txt, lang_code, x=974, y_top=202, max_height=188,
            base_size=34, fill=(255, 255, 255), base_width_ko=23, base_width_en=35,
        )

        # 예측 선택지 A (흔히 빠지는 통념 · 슬레이트 네이비 Rule 37)
        d1.rounded_rectangle((972, 408, 1828, 578), radius=16, fill=(30, 41, 59), outline=(148, 163, 184), width=2)
        opt_a = act_bp["option_a_en"] if is_en else act_bp["option_a_ko"]
        _draw_fitted_multiline(
            d1, opt_a, lang_code, x=998, y_top=428, max_height=136,
            base_size=27, fill=(226, 232, 240), base_width_ko=26, base_width_en=41,
        )

        # 예측 선택지 B (구조적 불변량/시각 통찰 · 에메랄드 틸 & 골드)
        d1.rounded_rectangle((972, 598, 1828, 804), radius=18, fill=(6, 78, 59), outline=(250, 204, 21), width=3)
        opt_b = act_bp["option_b_en"] if is_en else act_bp["option_b_ko"]
        _draw_fitted_multiline(
            d1, opt_b, lang_code, x=998, y_top=618, max_height=168,
            base_size=28, fill=(254, 240, 138), base_width_ko=25, base_width_en=39,
        )

        d1.rounded_rectangle((972, 822, 1828, 898), radius=14, fill=(2, 132, 199), outline=(254, 240, 138), width=2)
        commit_lbl = (
            "[STEP 1 · COMMIT FIRST] Pick A or B in 3 seconds before the proof starts!"
            if is_en
            else "[능동적 사고 1단계] 증명을 보기 전 A와 B 중 내 예측을 3초 먼저 선택하세요!"
        )
        d1.text((996, 845), commit_lbl, fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 23, bold=True))

        d1.rounded_rectangle((48, 952, 1872, 1044), radius=14, fill=(15, 23, 42), outline=(56, 189, 248), width=2)
        foot1 = (
            "[ARCHIVE] Original Proofs: https://min7014.github.io/  |  Active Thinking Lab: min7014.github.io/mathedu/video_board.html"
            if is_en
            else "[원문] 수학자료실: https://min7014.github.io/  |  능동적 사고 실습실: min7014.github.io/mathedu/video_board.html"
        )
        d1.text((80, 982), foot1, fill=(125, 211, 252), font=vmaker.get_font_for_lang(lang_code, 25, bold=True))

        act1_tts = (
            f"{bp['act1_en']} {act_bp['prediction_tts_en']}"
            if is_en
            else f"{bp['act1_ko']} {act_bp['prediction_tts_ko']}"
        )
        act1_mp3 = tmp_dir / "long_act1.mp3"
        act1_partA = tmp_dir / "long_act1_a.mp4"
        vmaker.synthesize_tts_mp3_sync(act1_tts, voice_name, act1_mp3, rate="+5%")
        dur_a1 = _encode_card_segment(act1_img, act1_mp3, act1_partA, ffmpeg_exe, ffprobe_exe)

        # Act 1 직후 3.0초 실제 예측 선택 사색 구간 추가
        pred_pulse = ate.ensure_thinking_pulse_wav(3.0)
        act1_png = tmp_dir / "act1_hold.png"
        act1_img.save(act1_png)
        act1_partB = tmp_dir / "long_act1_b.mp4"
        subprocess.run(
            [
                ffmpeg_exe, "-y", "-loop", "1", "-t", "3.000", "-i", str(act1_png),
                "-i", str(pred_pulse),
                "-c:v", "libx264", "-preset", "ultrafast", "-tune", "stillimage", "-crf", "20",
                "-pix_fmt", "yuv420p", "-r", "24",
                "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2", "-shortest", str(act1_partB),
            ],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        long_segs.extend([act1_partA, act1_partB])
        cursor_t += dur_a1 + 3.0
        chapter_lines.append(
            f"{_fmt_mmss(cursor_t)} | {'Step-by-Step Original Visual Proof' if is_en else '오리지널 원문 PDF 1페이지부터 직강 시작'}"
        )

        # [Act 2] 오리지널 PDF 1페이지 → 마지막 페이지 100% 무생략 직강 + 능동적 사고 정지 체크포인트 2곳
        for idx_s, p_idx in enumerate(all_indices, 1):
            p_info = pages[p_idx]
            doc_p = min(len(doc) - 1, max(0, int(p_info.get("page", p_idx + 1)) - 1))

            # ★ [능동적 사고 체크포인트 2]: 결정적 제1보조선 등장 '직전 백지 도형'에서 4초 발상 정지!
            if p_idx == crux_idx and len(all_indices) >= 3:
                pre_doc_p = max(0, doc_p - 1)
                pre_info = pages[max(0, p_idx - 1)]
                clean_pre_frame = vmaker.render_slide_frame_1080p(
                    doc[pre_doc_p], pre_info, sdoc, lang_code, show_spotlight=False, stage=1
                )
                chapter_lines.append(
                    f"{_fmt_mmss(cursor_t)} | {'[PAUSE 1] Sketch Your Auxiliary Idea First (4s)' if is_en else '[능동적 사고 1] 보조선 등장 전 먼저 상상하기 (4초)'}"
                )
                crux_seg, crux_dur = ate.encode_active_pause_segment_1080p(
                    base_slide_frame=clean_pre_frame,
                    lang_code=lang_code,
                    voice_name=voice_name,
                    prompt_text=act_bp["crux_prompt_en"] if is_en else act_bp["crux_prompt_ko"],
                    badge_label="[ACTIVE THINKING 1/2] INVENT THE CLUE FIRST" if is_en else "[능동적 사고 1/2] 보조선을 먼저 상상해 보세요!",
                    pause_seconds=4,
                    tmp_dir=tmp_dir,
                    seg_prefix="crux_pause",
                    ffmpeg_exe=ffmpeg_exe,
                    ffprobe_exe=ffprobe_exe,
                )
                long_segs.append(crux_seg)
                cursor_t += crux_dur

            # ★ [능동적 사고 체크포인트 3]: 최종 결론 직전 '왜 성립할까?' 3초 스스로 근거 말하기!
            elif p_idx == justify_idx and len(all_indices) >= 5 and justify_idx > crux_idx:
                pre_j_doc = max(0, doc_p - 1)
                pre_j_info = pages[max(0, p_idx - 1)]
                clean_j_frame = vmaker.render_slide_frame_1080p(
                    doc[pre_j_doc], pre_j_info, sdoc, lang_code, show_spotlight=False, stage=1
                )
                chapter_lines.append(
                    f"{_fmt_mmss(cursor_t)} | {'[PAUSE 2] Justify Why It Must Hold (3s)' if is_en else '[능동적 사고 2] 왜 성립하는지 스스로 말하기 (3초)'}"
                )
                just_seg, just_dur = ate.encode_active_pause_segment_1080p(
                    base_slide_frame=clean_j_frame,
                    lang_code=lang_code,
                    voice_name=voice_name,
                    prompt_text=act_bp["justify_prompt_en"] if is_en else act_bp["justify_prompt_ko"],
                    badge_label="[ACTIVE THINKING 2/2] SELF-EXPLAIN WHY" if is_en else "[능동적 사고 2/2] 성립 근거를 스스로 말해 보세요!",
                    pause_seconds=3,
                    tmp_dir=tmp_dir,
                    seg_prefix="justify_pause",
                    ffmpeg_exe=ffmpeg_exe,
                    ffprobe_exe=ffprobe_exe,
                )
                long_segs.append(just_seg)
                cursor_t += just_dur

            stage_num = 3 if idx_s == len(all_indices) else (1 if idx_s == 1 else 2)
            slide_frame = vmaker.render_slide_frame_1080p(
                doc[doc_p], p_info, sdoc, lang_code, show_spotlight=(idx_s > 1), stage=stage_num
            )
            raw_n = (p_info.get("narrations") or {}).get(lang_code) or p_info.get("explanation_text") or ""
            raw_n = re.sub(r"안녕하세요[^.?!]*[.?!]\s*", "", raw_n).strip()
            if not raw_n:
                raw_n = (
                    "Observe how each step connects hypothesis to conclusion."
                    if is_en
                    else "각 단계가 가정에서 결론으로 필연적으로 이어지는 과정을 살펴보세요."
                )
            s_mp3 = tmp_dir / f"long_p_{idx_s:02d}.mp3"
            s_mp4 = tmp_dir / f"long_p_{idx_s:02d}.mp4"
            vmaker.synthesize_tts_mp3_sync(raw_n, voice_name, s_mp3, rate="+6%")
            seg_d = _encode_card_segment(slide_frame, s_mp3, s_mp4, ffmpeg_exe, ffprobe_exe)
            long_segs.append(s_mp4)
            cursor_t += seg_d

        # [Act 3] 차별화된 수학교육 통찰 종합 & [능동적 사고 체크포인트 4: 라카토스 반례·What-If-Not 조건 변형 전이]
        chapter_lines.append(
            f"{_fmt_mmss(cursor_t)} | {'What-If-Not Counterexample & Hands-On Transfer' if is_en else '조건 변형(What-If-Not) & 반례 전이 사고 실험'}"
        )
        act3_img = Image.new("RGB", (1920, 1080), (8, 18, 34))
        d3 = ImageDraw.Draw(act3_img)
        d3.rounded_rectangle((48, 36, 1872, 138), radius=20, fill=(5, 150, 105), outline=(250, 204, 21), width=3)
        d3.text(
            (80, 66),
            "[ACTIVE TRANSFER] BEYOND THE PROOF: WHAT IF CONDITIONS CHANGE?"
            if is_en
            else "[능동적 사고 확장] 증명 끝이 진짜 시작! 조건을 바꾸면 어떻게 될까?",
            fill=(255, 255, 255),
            font=vmaker.get_font_for_lang(lang_code, 35, bold=True),
        )
        _paste_clean_pdf_preview(act3_img, doc, (56, 174, 900, 920), climax_preview_idx)

        d3.rounded_rectangle((936, 174, 1864, 920), radius=24, fill=(15, 23, 42), outline=(52, 211, 153), width=3)
        _draw_fitted_multiline(
            d3, bp["new_insight_en"] if is_en else bp["new_insight_ko"], lang_code,
            x=974, y_top=198, max_height=226, base_size=31, fill=(254, 240, 138),
            base_width_ko=24, base_width_en=37,
        )

        # 라카토스 반례 & What-If-Not 전이 실험 박스
        d3.rounded_rectangle((972, 444, 1828, 708), radius=18, fill=(30, 58, 138), outline=(250, 204, 21), width=2)
        wif_txt = act_bp["what_if_en"] if is_en else act_bp["what_if_ko"]
        _draw_fitted_multiline(
            d3, wif_txt, lang_code, x=998, y_top=466, max_height=220,
            base_size=26, fill=(255, 255, 255), base_width_ko=26, base_width_en=41,
        )

        d3.rounded_rectangle((972, 728, 1828, 892), radius=18, fill=(2, 132, 199), outline=(255, 255, 255), width=2)
        cta1 = "[HANDS-ON LAB] Try What-If-Not in Link Below!" if is_en else "[직접 실험] 설명란 능동적 사고 실험실 링크에서 직접 움직여 보세요!"
        cta2 = "[SUBSCRIBE] @min7014_ai  |  min7014.github.io" if is_en else "[구독] @min7014_ai  |  원문 아카이브 min7014.github.io"
        d3.text((998, 758), cta1, fill=(254, 240, 138), font=vmaker.get_font_for_lang(lang_code, 25, bold=True))
        d3.text((998, 818), cta2, fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 27, bold=True))

        act3_tts = (
            f"{bp['act3_en']} {act_bp['what_if_en']}"
            if is_en
            else f"{bp['act3_ko']} {act_bp['what_if_ko']}"
        )
        act3_mp3 = tmp_dir / "long_act3.mp3"
        act3_seg = tmp_dir / "long_act3.mp4"
        vmaker.synthesize_tts_mp3_sync(act3_tts, voice_name, act3_mp3, rate="+6%")
        _encode_card_segment(act3_img, act3_mp3, act3_seg, ffmpeg_exe, ffprobe_exe)
        long_segs.append(act3_seg)

        concat_long = tmp_dir / "concat_long.txt"
        concat_long.write_text("\n".join(f"file '{p.as_posix()}'" for p in long_segs), encoding="utf-8")
        raw_long = tmp_dir / "raw_long.mp4"
        subprocess.run(
            [ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_long), "-c", "copy", str(raw_long)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        _mix_calm_bgm(raw_long, long_mp4, ffmpeg_exe)
        long_dur = vmaker.get_media_duration_seconds(long_mp4, ffprobe_exe)

        # ==================== B. 1080x1920 9:16 능동 사고형 통찰 Q-#Shorts (<46s) ====================
        sh_segs: list[Path] = []

        # Scene 1: 이슈 발문 훅 + 오리지널 초기 백지 도형 + 2.0초 능동적 발상 정지!
        s1 = Image.new("RGB", (1080, 1920), (9, 14, 28))
        ds1 = ImageDraw.Draw(s1)
        ds1.rounded_rectangle((40, 64, 1040, 210), radius=24, fill=(30, 58, 138), outline=(250, 204, 21), width=4)
        ds1.text(
            (72, 108),
            "[THINK FIRST] PREDICT THE VISUAL CLUE!" if is_en else "[능동적 사고] 먼저 보조선을 상상해 보세요!",
            fill=(254, 240, 138),
            font=vmaker.get_font_for_lang(lang_code, 38, bold=True),
        )
        _paste_clean_pdf_preview(s1, doc, (48, 248, 1032, 1180), pre_crux_preview_idx)
        ds1.rounded_rectangle((48, 1216, 1032, 1630), radius=24, fill=(15, 23, 42), outline=(56, 189, 248), width=3)
        _draw_fitted_multiline(
            ds1, bp["issue_headline_en"] if is_en else bp["issue_headline_ko"], lang_code,
            x=82, y_top=1246, max_height=270, base_size=34, fill=(255, 255, 255),
            base_width_ko=22, base_width_en=33,
        )
        ds1.rounded_rectangle((76, 1532, 1004, 1606), radius=14, fill=(5, 150, 105), outline=(250, 204, 21), width=2)
        ds1.text(
            (102, 1552),
            "[PAUSE 2s] Where would YOU draw the first line?" if is_en else "[2초 멈춤] 어디에 보조선·단서를 잡으시겠습니까?",
            fill=(255, 255, 255),
            font=vmaker.get_font_for_lang(lang_code, 27, bold=True),
        )

        sh1_mp3 = tmp_dir / "sh1.mp3"
        sh1_seg = tmp_dir / "sh1.mp4"
        sh_hook_tts = (
            bp["issue_headline_en"] + " Pause two seconds—where would YOU draw the key clue?"
            if is_en
            else bp["issue_headline_ko"] + " 정답을 보기 전 2초 동안 어디에 핵심 단서를 잡을지 먼저 상상해 보세요!"
        )
        vmaker.synthesize_tts_mp3_sync(sh_hook_tts, voice_name, sh1_mp3, rate="+18%")
        _encode_card_segment(s1, sh1_mp3, sh1_seg, ffmpeg_exe, ffprobe_exe)
        sh_segs.append(sh1_seg)

        # 2.0초 실제 사색 펄스 세그먼트 (Shorts 리텐션 & 능동적 사고 유도)
        sh_pulse = ate.ensure_thinking_pulse_wav(2.0)
        s1_png = tmp_dir / "sh1_hold.png"
        s1.save(s1_png)
        sh1_wait = tmp_dir / "sh1_wait.mp4"
        subprocess.run(
            [
                ffmpeg_exe, "-y", "-loop", "1", "-t", "2.000", "-i", str(s1_png),
                "-i", str(sh_pulse),
                "-c:v", "libx264", "-preset", "ultrafast", "-tune", "stillimage", "-crf", "20",
                "-pix_fmt", "yuv420p", "-r", "24",
                "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2", "-shortest", str(sh1_wait),
            ],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        sh_segs.append(sh1_wait)

        # Scene 2 & 3: 오리지널 PDF 핵심 전환점 & 클라이맥스 슬라이드 2장
        pick_sh = [min(len(doc) - 1, max(1, crux_idx)), climax_preview_idx]
        for si, dp_i in enumerate(pick_sh, 2):
            sc_v = Image.new("RGB", (1080, 1920), (10, 16, 34))
            dsc = ImageDraw.Draw(sc_v)
            dsc.rounded_rectangle((40, 64, 1040, 196), radius=22, fill=(2, 132, 199), outline=(254, 240, 138), width=3)
            dsc.text(
                (72, 104),
                f"[DISCOVERY {si-1}/2] COMPARE WITH YOUR IDEA!" if is_en else f"[단서 공개 {si-1}/2] 여러분의 발상과 비교해 보세요!",
                fill=(255, 255, 255),
                font=vmaker.get_font_for_lang(lang_code, 35, bold=True),
            )
            _paste_clean_pdf_preview(sc_v, doc, (48, 236, 1032, 1280), dp_i)

            p_match = pages[min(len(pages) - 1, dp_i)]
            clue_txt = ((p_match.get("narrations") or {}).get(lang_code) or p_match.get("explanation_text") or "").strip()
            sents = [x.strip() for x in re.split(r"(?<=[.?!])\s+", clue_txt) if x.strip() and "안녕하세요" not in x]
            short_clue = sents[-1] if sents else ("Visual symmetry connects the core condition directly!" if is_en else "보조선과 대칭 구조가 가정과 결론을 한눈에 연결합니다!")
            if len(short_clue) > (130 if is_en else 76):
                short_clue = short_clue[: (126 if is_en else 72)].rsplit(" ", 1)[0] + "."

            dsc.rounded_rectangle((48, 1320, 1032, 1610), radius=22, fill=(15, 23, 42), outline=(56, 189, 248), width=3)
            _draw_fitted_multiline(
                dsc, short_clue, lang_code, x=80, y_top=1352, max_height=230,
                base_size=33, fill=(255, 255, 255), base_width_ko=23, base_width_en=35,
            )

            sh_m_mp3 = tmp_dir / f"sh_{si}.mp3"
            sh_m_seg = tmp_dir / f"sh_{si}.mp4"
            vmaker.synthesize_tts_mp3_sync(short_clue, voice_name, sh_m_mp3, rate="+18%")
            _encode_card_segment(sc_v, sh_m_mp3, sh_m_seg, ffmpeg_exe, ffprobe_exe)
            sh_segs.append(sh_m_seg)

        # Scene 4: 차별화된 수학교육 통찰 결론 & 관련 동영상 본편 클릭 유도
        s4 = Image.new("RGB", (1080, 1920), (8, 20, 34))
        ds4 = ImageDraw.Draw(s4)
        ds4.rounded_rectangle((40, 64, 1040, 200), radius=24, fill=(5, 150, 105), outline=(250, 204, 21), width=4)
        ds4.text(
            (72, 106),
            "[WHAT-IF-NOT] KEEP THINKING IN FULL VIDEO!" if is_en else "[능동적 통찰] 전체 증명 & 조건 변형 본편 보기!",
            fill=(255, 255, 255),
            font=vmaker.get_font_for_lang(lang_code, 36, bold=True),
        )
        _paste_clean_pdf_preview(s4, doc, (48, 236, 1032, 1120), climax_preview_idx)
        ds4.rounded_rectangle((48, 1156, 1032, 1620), radius=24, fill=(15, 23, 42), outline=(52, 211, 153), width=4)
        _draw_fitted_multiline(
            ds4, bp["new_insight_en"] if is_en else bp["new_insight_ko"], lang_code,
            x=80, y_top=1186, max_height=258, base_size=32, fill=(254, 240, 138),
            base_width_ko=23, base_width_en=35,
        )
        ds4.rounded_rectangle((72, 1464, 1008, 1592), radius=18, fill=(2, 132, 199))
        cta_b = "[WATCH] Tap Related Video (Full Active Proof)!" if is_en else "[본편 보기] 아래 관련 동영상 클릭 & 직접 실험하기!"
        ds4.text((92, 1508), cta_b, fill=(255, 255, 255), font=vmaker.get_font_for_lang(lang_code, 28, bold=True))

        sh4_mp3 = tmp_dir / "sh4.mp3"
        sh4_seg = tmp_dir / "sh4.mp4"
        sh_out_tts = (
            bp["new_insight_en"] + " Tap the related video below for the full active-thinking proof and subscribe!"
            if is_en
            else bp["new_insight_ko"] + " 조건이 바뀌면 어떻게 될지 아래 관련 동영상 본편에서 직접 확인하고 구독해 두세요!"
        )
        vmaker.synthesize_tts_mp3_sync(sh_out_tts, voice_name, sh4_mp3, rate="+18%")
        _encode_card_segment(s4, sh4_mp3, sh4_seg, ffmpeg_exe, ffprobe_exe)
        sh_segs.append(sh4_seg)

        concat_sh = tmp_dir / "concat_sh.txt"
        concat_sh.write_text("\n".join(f"file '{p.as_posix()}'" for p in sh_segs), encoding="utf-8")
        raw_sh = tmp_dir / "raw_sh.mp4"
        subprocess.run(
            [ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_sh), "-c", "copy", str(raw_sh)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        _mix_calm_bgm(raw_sh, short_mp4, ffmpeg_exe)
        short_dur = vmaker.get_media_duration_seconds(short_mp4, ffprobe_exe)
        if short_dur >= 52.0:
            spd = min(1.75, round(short_dur / 44.0, 3))
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

        pkg_meta = {
            "long_mp4": str(long_mp4.relative_to(ROOT_DIR)).replace("\\", "/"),
            "long_thumb": str(long_thumb.relative_to(ROOT_DIR)).replace("\\", "/"),
            "long_duration_sec": round(long_dur, 2),
            "short_mp4": str(short_mp4.relative_to(ROOT_DIR)).replace("\\", "/"),
            "short_duration_sec": round(short_dur, 2),
            "issue_category": bp["issue_category_en"] if is_en else bp["issue_category_ko"],
            "issue_headline": bp["issue_headline_en"] if is_en else bp["issue_headline_ko"],
            "pedagogical_insight": bp["new_insight_en"] if is_en else bp["new_insight_ko"],
            "what_if_transfer": act_bp["what_if_en"] if is_en else act_bp["what_if_ko"],
            "chapters_text": "\n".join(chapter_lines),
            "active_thinking_v1": True,
            "title": bp["title_en"] if is_en else bp["title_ko"],
            "short_title": bp["short_title_en"] if is_en else bp["short_title_ko"],
            "comment_quiz": bp["comment_quiz_en"] if is_en else bp["comment_quiz_ko"],
            "updated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        }
        sdoc.setdefault("issue_insight_packages", {})[lang_code] = pkg_meta
        sp.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
        return pkg_meta
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        doc.close()


def ensure_next_issue_insight_rendered(max_bundles: int = 1) -> list[dict]:
    """
    24/7 데몬 루프 호출용: 실시간 수학 이슈 레이더를 갱신하고 다음 미제작 수학교육 통찰 패키지를 자동 렌더링합니다.
    """
    scan_live_math_issues(timeout=6)
    rendered = []
    try:
        import youtube_self_evolving_engine as _ysee
        lang_order = _ysee.preferred_lang_order_for_current_hour()
    except Exception:
        lang_order = ("ko", "en")

    for bp in get_ranked_issue_insight_blueprints():
        slug = bp["slug"]
        for lc in lang_order:
            l_mp4 = ISSUE_INSIGHT_DIR / f"{slug}_issue_{lc}.mp4"
            s_mp4 = ISSUE_INSIGHT_DIR / f"{slug}_issue_short_{lc}.mp4"
            if not (l_mp4.exists() and s_mp4.exists()):
                pkg = render_issue_insight_bundle(bp, lang_code=lc)
                rendered.append({"slug": slug, "lang": lc, **pkg})
                if len(rendered) >= max_bundles:
                    return rendered
    return rendered


def _notify_telegram_issue_upload(kind_label: str, slug: str, lc: str, title: str, url: str) -> None:
    try:
        import mathedu_telegram_bridge as tg_bridge
        cfg = tg_bridge.load_env_config()
        tk, cid = cfg.get("TELEGRAM_BOT_TOKEN", ""), cfg.get("TELEGRAM_CHAT_ID", "")
        if tk and cid:
            tg_bridge.send_msg(
                tk,
                cid,
                f"🧭 [수학 이슈 × 오리지널 수학교육 통찰 자동 발행 ({kind_label} · {lc.upper()})]\n"
                f"• 주제({slug}): {title}\n"
                f"• 유튜브 링크: {url}",
            )
    except Exception:
        pass


def try_upload_one_issue_insight(kind: str = "long", force_slug: str | None = None, force_lang: str | None = None) -> dict | None:
    """
    finance.py 황금비 엔진 연동용 업로더 (Rule 28.3 원문 링크 최상단 + Rule 35 인간 오리지널 정통성 + Rule 53 Auditor 7계층 검문):
    - kind == 'long'  : 1080p 수학교육 통찰 본편 업로드 + 열린 발문 고정댓글 등록
    - kind == 'short' : 본편이 업로드된 짝꿍 Q-#Shorts 업로드 + 스튜디오 관련 동영상 자동 연결
    """
    import auditor as _aud
    import min7014_video_maker as vmaker
    from googleapiclient.http import MediaFileUpload

    if vmaker._LAST_UPLOAD_QUOTA_BLOCKED:
        return None
    yt, _ = vmaker.get_available_youtube_upload_service()
    if yt is None:
        return None

    try:
        import youtube_self_evolving_engine as _ysee
        lang_order = (force_lang,) if force_lang else _ysee.preferred_lang_order_for_current_hour()
    except Exception:
        lang_order = (force_lang,) if force_lang else ("ko", "en")

    for bp in get_ranked_issue_insight_blueprints():
        slug = bp["slug"]
        if force_slug and slug != force_slug:
            continue
        sp = SCRIPTS_DIR / f"{slug}.json"
        if not sp.exists():
            continue
        sdoc = json.loads(sp.read_text(encoding="utf-8"))
        iss_urls = sdoc.setdefault("issue_insight_urls", {})
        iss_sh_urls = sdoc.setdefault("issue_insight_shorts_urls", {})

        for lc in lang_order:
            is_en = lc == "en"
            l_mp4 = ISSUE_INSIGHT_DIR / f"{slug}_issue_{lc}.mp4"
            l_thumb = ISSUE_INSIGHT_DIR / f"{slug}_issue_{lc}_thumb.png"
            s_mp4 = ISSUE_INSIGHT_DIR / f"{slug}_issue_short_{lc}.mp4"

            if kind == "long" and not (iss_urls.get(lc) or "").strip():
                pkg_meta = (sdoc.get("issue_insight_packages") or {}).get(lc) or {}
                if not l_mp4.exists() or not pkg_meta.get("active_thinking_v1"):
                    render_issue_insight_bundle(bp, lang_code=lc)
                    sdoc = json.loads(sp.read_text(encoding="utf-8"))
                    iss_urls = sdoc.setdefault("issue_insight_urls", {})
                    iss_sh_urls = sdoc.setdefault("issue_insight_shorts_urls", {})
                    pkg_meta = (sdoc.get("issue_insight_packages") or {}).get(lc) or {}
                if not l_mp4.exists():
                    continue
                pdf_url = sdoc.get("pdf_url") or "https://min7014.github.io/"
                web_url = sdoc.get("web_url") or "https://min7014.github.io/"
                chapters_block = pkg_meta.get("chapters_text") or (
                    "00:00 | Contemporary Math Issue & Active Prediction (A vs B)\n"
                    "00:28 | Step-by-Step Original Visual Proof & Active Pause Checkpoints\n"
                    "04:10 | What-If-Not Counterexample & Hands-On Transfer"
                    if is_en
                    else "00:00 | 오늘의 수학 화두 & A vs B 직관 예측 선택\n"
                    "00:28 | 오리지널 원문 PDF 직강 & 보조선 능동 발상 정지\n"
                    "04:10 | 조건 변형(What-If-Not) & 반례 전이 사고 실험"
                )
                wif_line = pkg_meta.get("what_if_transfer") or ""
                raw_title = bp["title_en"] if is_en else bp["title_ko"]
                raw_desc = (
                    f"🏛️ [Original Visual Math Archive (https://min7014.github.io/)]\n"
                    f"• Step-by-Step Original Proof PDF: {pdf_url}\n"
                    f"• 🧠 Active-Thinking 4-Step Workbench (Predict → Sketch → What-If-Not): https://min7014.github.io/mathedu/video_board.html?slug={slug}&mode=active\n"
                    f"• Interactive Dynamic Geometry & MathLab: https://min7014.github.io/mathedu/mathlab.html?slug={slug}\n"
                    f"• Binge Full Visual Proof Playlist: https://www.youtube.com/playlist?list=UUSlqQfOEtRfJuMPyGMLgFYA\n\n"
                    f"🧭 [Active Mathematical Thinking × Differentiated Math-Education Perspective]\n"
                    f"• Issue Focus: {bp['issue_headline_en']}\n"
                    f"• Pedagogical Shift: {bp['new_insight_en']}\n"
                    f"• Post-Proof Transfer: {wif_line}\n\n"
                    f"✍️ [Human-Crafted Original Depth Notice]\n"
                    f"This lecture is NOT generic AI-generated content. Every mathematical idea, auxiliary construction, and step-by-step visual proof slide originates 100% from human-authored research materials ({web_url}), designed with intentional Active-Thinking Pause Checkpoints so learners invent key ideas before seeing the answer.\n\n"
                    f"{chapters_block}\n\n"
                    f"#MathematicsEducation #ActiveThinking #VisualProof #MathematicalThinking #DiscoveryLearning"
                    if is_en
                    else f"🏛️ [오리지널 원문 수학자료실 (https://min7014.github.io/) 바로가기]\n"
                    f"• 오리지널 단계별 시각 증명 PDF 원문: {pdf_url}\n"
                    f"• 🧠 능동적 사고 4단계 워크벤치 (직관 예측 → 보조선 설계 → 조건 변형 실습): https://min7014.github.io/mathedu/video_board.html?slug={slug}&mode=active\n"
                    f"• 자체 제작 MathLab 동적 작도 실습: https://min7014.github.io/mathedu/mathlab.html?slug={slug}\n"
                    f"• 연속재생 전체 증명 플레이리스트: https://www.youtube.com/playlist?list=UUSlqQfOEtRfJuMPyGMLgFYA\n\n"
                    f"🧭 [능동적 수학 사고 × 차별화된 수학교육 통찰]\n"
                    f"• 오늘의 화두: {bp['issue_headline_ko']}\n"
                    f"• 수학교육의 시선: {bp['new_insight_ko']}\n"
                    f"• 증명 이후 확장 질문: {wif_line}\n\n"
                    f"✍️ [오리지널 인간 저작물 정통성 안내]\n"
                    f"본 콘텐츠는 모든 것이 AI에 의해 만들어진 단순 생성물이 아닙니다. 기본 수학 아이디어·보조선 발상·단계별 시각 증명 슬라이드는 사람이 오랜 세월 직접 연구하고 한 땀 한 땀 작도한 깊이 있는 오리지널 원문 자료({web_url})로부터 탄생했으며, 시청자가 수동적으로 듣지 않고 스스로 보조선을 먼저 상상하고 조건을 변형해 보도록 '능동적 사고 정지 체크포인트'를 결합했습니다.\n\n"
                    f"{chapters_block}\n\n"
                    f"#수학교육 #능동적사고 #시각적증명 #수학적사고력 #질문하는수업"
                )
                raw_tags = (
                    ["Mathematics Education", "Active Mathematical Thinking", "Visual Math Proof", "Geometry Intuition", "Discovery Learning"]
                    if is_en
                    else ["수학교육", "능동적사고", "시각적증명", "수학적사고력", "기하직관", "질문하는수학수업"]
                )
                try:
                    import google_ecosystem_orchestrator as _geo
                    raw_tags = _geo.enrich_tags_with_google_youtube_suggest(slug, lang_code=lc, base_tags=raw_tags)
                    _geo.generate_studio_ab_test_thumbnails(slug, lang_code=lc)
                except Exception:
                    pass
                gated = _aud.sanitize_and_gate_upload_payload(raw_title, raw_desc, raw_tags)
                title = vmaker.sanitize_youtube_title(gated["title"])
                body = {
                    "snippet": {
                        "title": title,
                        "description": gated["description"],
                        "tags": gated["tags"],
                        "categoryId": "27",
                        "defaultLanguage": lc,
                        "defaultAudioLanguage": lc,
                    },
                    "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False},
                }
                try:
                    req = yt.videos().insert(
                        part="snippet,status",
                        body=body,
                        media_body=MediaFileUpload(str(l_mp4), chunksize=4 * 1024 * 1024, resumable=True),
                    )
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
                        lab_line = (
                            f"\n🧠 Hands-On Active Thinking Lab: https://min7014.github.io/mathedu/video_board.html?slug={slug}&mode=active"
                            if is_en
                            else f"\n🧠 내 손으로 직접 해보는 능동적 사고 실험실: https://min7014.github.io/mathedu/video_board.html?slug={slug}&mode=active"
                        )
                        c_txt = (bp["comment_quiz_en"] if is_en else bp["comment_quiz_ko"]) + lab_line + f"\n🔗 https://www.youtube.com/watch?v={vid}&list=UUSlqQfOEtRfJuMPyGMLgFYA"
                        yt.commentThreads().insert(
                            part="snippet",
                            body={"snippet": {"videoId": vid, "topLevelComment": {"snippet": {"textOriginal": c_txt}}}},
                        ).execute()
                    except Exception:
                        pass
                    url = f"https://youtu.be/{vid}"
                    iss_urls[lc] = url
                    sp.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
                    _notify_telegram_issue_upload("1080p 수학교육 통찰 본편", slug, lc, title, url)
                    return {"type": "issue_insight_1080p", "slug": slug, "lang": lc, "url": url, "title": title}
                except Exception as e:
                    if "uploadLimitExceeded" in str(e) or "quotaExceeded" in str(e):
                        vmaker._LAST_UPLOAD_QUOTA_BLOCKED = True
                    return None

            if kind == "short" and (iss_urls.get(lc) or "").strip() and not (iss_sh_urls.get(lc) or "").strip():
                if not s_mp4.exists():
                    render_issue_insight_bundle(bp, lang_code=lc)
                if not s_mp4.exists():
                    continue
                raw_sh_title = bp["short_title_en"] if is_en else bp["short_title_ko"]
                long_u = iss_urls[lc]
                long_vid = long_u.rstrip("/").split("/")[-1].split("?")[0]
                watch_pl = f"https://www.youtube.com/watch?v={long_vid}&list=UUSlqQfOEtRfJuMPyGMLgFYA" if long_vid else long_u
                raw_sh_desc = (
                    f"🎬 Watch Full 1080p Active-Thinking Proof & Insight: {watch_pl}\n"
                    f"🧠 Hands-On 4-Step Active Thinking Lab: https://min7014.github.io/mathedu/video_board.html?slug={slug}&mode=active\n"
                    f"🏛️ Original Visual Proof Archive: https://min7014.github.io/\n"
                    f"#Shorts #MathematicsEducation #ActiveThinking #VisualProof"
                    if is_en
                    else f"🎬 1080p 능동적 수학 사고 통찰 & 전체 시각 증명 본편 바로 보기: {watch_pl}\n"
                    f"🧠 내 손으로 직접 해보는 능동적 사고 4단계 워크벤치: https://min7014.github.io/mathedu/video_board.html?slug={slug}&mode=active\n"
                    f"🏛️ 오리지널 원문 수학자료실: https://min7014.github.io/\n"
                    f"#Shorts #수학교육 #능동적사고 #시각적증명 #수학적사고력"
                )
                raw_sh_tags = ["Shorts", "Mathematics Education", "Visual Proof"] if is_en else ["Shorts", "수학교육", "시각적증명", "수학이슈"]
                gated_sh = _aud.sanitize_and_gate_upload_payload(raw_sh_title, raw_sh_desc, raw_sh_tags)
                sh_title = vmaker.sanitize_youtube_title(gated_sh["title"])
                body_sh = {
                    "snippet": {
                        "title": sh_title,
                        "description": gated_sh["description"],
                        "tags": gated_sh["tags"],
                        "categoryId": "27",
                        "defaultLanguage": lc,
                        "defaultAudioLanguage": lc,
                    },
                    "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False},
                }
                try:
                    req = yt.videos().insert(
                        part="snippet,status",
                        body=body_sh,
                        media_body=MediaFileUpload(str(s_mp4), chunksize=4 * 1024 * 1024, resumable=True),
                    )
                    resp = None
                    while resp is None:
                        _, resp = req.next_chunk()
                    vid = resp["id"]
                    url = f"https://youtube.com/shorts/{vid}"
                    iss_sh_urls[lc] = url
                    sp.write_text(json.dumps(sdoc, ensure_ascii=False, indent=2), encoding="utf-8")
                    try:
                        import youtube_community_controller as _ycc
                        _ycc.link_shorts_related_videos_in_studio(max_links=2, headless=True)
                    except Exception:
                        pass
                    _notify_telegram_issue_upload("통찰 Q-#Shorts", slug, lc, sh_title, url)
                    return {"type": "issue_insight_short", "slug": slug, "lang": lc, "url": url, "title": sh_title}
                except Exception as e:
                    if "uploadLimitExceeded" in str(e) or "quotaExceeded" in str(e):
                        vmaker._LAST_UPLOAD_QUOTA_BLOCKED = True
                    return None
    return None


def format_issue_insight_status_summary() -> str:
    radar = scan_live_math_issues(timeout=6)
    mp4s = list(ISSUE_INSIGHT_DIR.glob("*_issue_*.mp4"))
    long_cnt = len([p for p in mp4s if "_short_" not in p.name])
    short_cnt = len([p for p in mp4s if "_short_" in p.name])
    uploaded_long = 0
    uploaded_short = 0
    recent_links: list[str] = []
    for sp in SCRIPTS_DIR.glob("*.json"):
        try:
            d = json.loads(sp.read_text(encoding="utf-8"))
            u_l = d.get("issue_insight_urls") or {}
            u_s = d.get("issue_insight_shorts_urls") or {}
            for lc, u in u_l.items():
                if u:
                    uploaded_long += 1
                    recent_links.append(f"  - [{sp.stem} · {lc.upper()} 본편] {u}")
            for lc, u in u_s.items():
                if u:
                    uploaded_short += 1
        except Exception:
            continue

    lines = [
        "🧭 [크레딧 0원 · 수학 분야 실시간 이슈 × 능동적 수학 사고(Active Thinking) 통찰 엔진 현황]",
        f"• 실시간 레이더 스캔: {radar.get('scanned_at')} (감지 화두 {radar.get('discovered_count', 0)}건)",
        f"• 이달의 핵심 교육 화두: {radar.get('seasonal_theme')}",
        "• 능동 사고 4단계 엔진: A vs B 직관 예측(3초) → 백지 도형 발상 정지(4초) → 결론 정당화(3초) → What-If-Not 전이",
        f"• 렌더링 완비 자산: 1080p 통찰 본편 {long_cnt}편 / 9:16 통찰 Q-#Shorts {short_cnt}편",
        f"• @min7014_ai 라이브 발행: 본편 {uploaded_long}편 / Q-#Shorts {uploaded_short}편",
    ]
    sigs = radar.get("signals") or []
    if sigs:
        lines.append("• 실시간 포착 수학·교육 시그널:")
        for s in sigs[:3]:
            ref = s.get("reference_signal") or s.get("pedagogical_focus") or ""
            kws = ", ".join((s.get("matched_keywords") or [])[:3])
            lines.append(f"  - [{kws}] {ref[:68]}")
    if recent_links:
        lines.append("• 최근 발행 수학교육 통찰 영상:")
        lines.extend(recent_links[-4:])
    return "\n".join(lines)


if __name__ == "__main__":
    import sys

    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "status":
        print(format_issue_insight_status_summary())
    elif cmd == "render":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 2
        res = ensure_next_issue_insight_rendered(max_bundles=n)
        print(json.dumps(res, ensure_ascii=False, indent=2))
    elif cmd == "upload":
        k = sys.argv[2] if len(sys.argv) > 2 else "long"
        print(json.dumps(try_upload_one_issue_insight(kind=k), ensure_ascii=False, indent=2))
