# -*- coding: utf-8 -*-
"""
oct2026_part4_calc.py
2026학년도 10월 고3 전국연합학력평가 (2027대비) 수학 [미적분] 23번 ~ 30번
초등학생 눈높이 무장벽 디딤돌 5단계 퀴즈 및 상세 풀이 데이터
"""

PART4_PROBLEMS = [
    # -------------------------------------------------------------------------
    # 미적 23번: c2610m23
    # -------------------------------------------------------------------------
    {
        "slug": "c2610m23",
        "qNum": "미적 23",
        "subject": "미적분",
        "title": "[2026학년도 10월 고3 미적 23번] 자연로그 함수의 극한과 계수 비 규칙",
        "title_en": "[2026 AY Oct Exam Grade 12 Calculus #23] Limit of Natural Logarithm Function and Coefficient Ratio",
        "summary_ko": "lim (x->0) ln(1+5x^2)/(2x^2)에서 분모·분자의 x^2 계수 비 5/2 구하기",
        "summary_en": "Evaluate lim_{x->0} ln(1+5x^2)/(2x^2) using the standard logarithmic limit to get 5/2.",
        "tags": ["미적분", "미분법", "지수로그함수의극한", "자연로그", "23번"],
        "symbols": [
            {"sym": r"$\lim_{t \to 0} \dfrac{\ln(1+t)}{t} = 1$", "desc": "t가 0에 가까워질 때 ln(1+t)는 t와 거의 같아지는 극한 약속", "desc_en": "Fundamental limit of the natural logarithm near 0."},
            {"sym": r"$\dfrac{5x^2}{2x^2} = \dfrac{5}{2}$", "desc": "ln(1+5x^2)을 5x^2으로 바꾸어 약분한 비율", "desc_en": "Ratio of coefficients of x^2 in numerator and denominator."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 분수 약분] $\\dfrac{5 \\times \\square}{2 \\times \\square}$에서 똑같은 네모 지우기",
                "title_en": "🔰 Step 1 · [Elementary Fraction Cancellation] Canceling common factors in $\\dfrac{5 \\times \\square}{2 \\times \\square}$",
                "knowledge": r"초등학교 분수 약분에서 분자와 분모에 똑같이 곱해진 수($\square = x^2$)는 지울 수 있습니다! $x$가 $0$에 아주 가까워질 때 $\ln(1 + 5x^2)$은 $5x^2$과 거의 같아지므로 $\frac{5x^2}{2x^2}$을 약분하는 것과 같습니다.",
                "knowledge_en": r"By elementary fraction cancellation, common factors in the numerator and denominator cancel out. Since $\ln(1+5x^2) \approx 5x^2$ near $x=0$, the ratio reduces to $\frac{5x^2}{2x^2}$.",
                "questions": [
                    {
                        "level_label": "초등 분수 약분 디딤돌 1",
                        "level_label_en": "Elementary Fraction Step 1",
                        "stem": r"초등학교 분수 약분 원리에 따라 $\frac{5 \times x^2}{2 \times x^2}$에서 분자·분모의 $x^2$을 약분하고 남는 분수는?",
                        "stem_en": r"Using elementary fraction cancellation, what remains after canceling $x^2$ in $\frac{5x^2}{2x^2}$?",
                        "options": [r"$\frac{1}{2}$", r"$1$", r"$\frac{3}{2}$", r"$2$", r"$\frac{5}{2}$"],
                        "answer": 5,
                        "exp": r"$x^2$을 약분하면 계수의 비 $\frac{5}{2}$만 남습니다.",
                        "exp_en": r"Canceling $x^2$ leaves $\frac{5}{2}$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [기본 공식 확인] $\\lim_{t \\to 0} \\dfrac{\\ln(1+t)}{t}$의 값",
                "title_en": "🌿 Step 2 · [Standard Limit] Value of $\\lim_{t \\to 0} \\dfrac{\\ln(1+t)}{t}$",
                "knowledge": r"자연로그의 정의에 의하여 $\lim_{t \to 0} \frac{\ln(1+t)}{t} = 1$입니다.",
                "knowledge_en": r"By the definition of $e$, $\lim_{t \to 0} \frac{\ln(1+t)}{t} = 1$.",
                "questions": [
                    {
                        "level_label": "로그 극한 공식 디딤돌 2",
                        "level_label_en": "Log Limit Formula Step 2",
                        "stem": r"$t = 5x^2$이라 할 때, $\lim_{x \to 0} \frac{\ln(1 + 5x^2)}{5x^2}$의 극한값은?",
                        "stem_en": r"Letting $t = 5x^2$, what is $\lim_{x \to 0} \frac{\ln(1 + 5x^2)}{5x^2}$?",
                        "options": [r"$0$", r"$\frac{1}{5}$", r"$1$", r"$2$", r"$5$"],
                        "answer": 3,
                        "exp": r"괄호 안의 $5x^2$과 분모의 $5x^2$이 정확히 일치하므로 극한값은 $1$입니다.",
                        "exp_en": r"Since the argument $5x^2$ matches the denominator, the limit is $1$."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [식 변형] 분모 맞춰주기",
                "title_en": "🌱 Step 3 · [Algebraic Manipulation] Matching the denominator",
                "knowledge": r"$\frac{\ln(1+5x^2)}{2x^2} = \frac{\ln(1+5x^2)}{5x^2} \times \frac{5x^2}{2x^2}$로 나누어 쓸 수 있습니다.",
                "knowledge_en": r"Rewrite $\frac{\ln(1+5x^2)}{2x^2} = \frac{\ln(1+5x^2)}{5x^2} \times \frac{5}{2}$.",
                "questions": [
                    {
                        "level_label": "분모 맞추기 디딤돌 3",
                        "level_label_en": "Denominator Match Step 3",
                        "stem": r"$\frac{\ln(1+5x^2)}{2x^2} = \frac{\ln(1+5x^2)}{5x^2} \times k$가 성립하도록 하는 상수 $k$의 값은?",
                        "stem_en": r"For $\frac{\ln(1+5x^2)}{2x^2} = \frac{\ln(1+5x^2)}{5x^2} \times k$ to hold, what is $k$?",
                        "options": [r"$\frac{1}{2}$", r"$\frac{2}{5}$", r"$1$", r"$\frac{5}{2}$", r"$5$"],
                        "answer": 4,
                        "exp": r"약분하여 원래 분모 $2x^2$이 되려면 $k = \frac{5}{2}$여야 합니다.",
                        "exp_en": r"$k = \frac{5}{2}$."
                    }
                ]
            },
            {
                "title": "🌳 4단계 · [극한 곱셈] $1 \\times \\dfrac{5}{2}$ 계산하기",
                "title_en": "🌳 Step 4 · [Limit Product] Computing $1 \\times \\dfrac{5}{2}$",
                "knowledge": r"앞부분의 극한값 $1$과 뒷부분의 상수 $\frac{5}{2}$를 곱합니다.",
                "knowledge_en": r"Multiply the limit $1$ by $\frac{5}{2}$.",
                "questions": [
                    {
                        "level_label": "극한 곱셈 디딤돌 4",
                        "level_label_en": "Limit Product Step 4",
                        "stem": r"$1 \times \frac{5}{2}$의 값은?",
                        "stem_en": r"What is $1 \times \frac{5}{2}$?",
                        "options": [r"$\frac{1}{2}$", r"$1$", r"$\frac{3}{2}$", r"$2$", r"$\frac{5}{2}$"],
                        "answer": 5,
                        "exp": r"$1 \times \frac{5}{2} = \frac{5}{2}$입니다.",
                        "exp_en": r"$1 \times \frac{5}{2} = \frac{5}{2}$."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [최종 종합] 주어진 극한값 확정하기",
                "title_en": "💎 Step 5 · [Final Synthesis] Final limit value",
                "knowledge": r"따라서 구하는 극한값은 $\frac{5}{2}$입니다.",
                "knowledge_en": r"The final limit is $\frac{5}{2}$.",
                "questions": [
                    {
                        "level_label": "최종 종합 디딤돌 5",
                        "level_label_en": "Final Synthesis Step 5",
                        "stem": r"$\lim_{x \to 0} \frac{\ln(1+5x^2)}{2x^2}$의 값은?",
                        "stem_en": r"What is the value of $\lim_{x \to 0} \frac{\ln(1+5x^2)}{2x^2}$?",
                        "options": [r"$\frac{1}{2}$", r"$1$", r"$\frac{3}{2}$", r"$2$", r"$\frac{5}{2}$"],
                        "answer": 5,
                        "exp": r"$\lim_{x \to 0} \frac{\ln(1+5x^2)}{5x^2} \times \frac{5}{2} = \frac{5}{2}$이므로 정답은 ⑤입니다.",
                        "exp_en": r"$\frac{5}{2}$ (choice ⑤)."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"$\lim_{x \to 0} \dfrac{\ln(1+5x^2)}{2x^2}$의 값은? [2점]",
            "stem_en": r"What is the value of $\lim_{x \to 0} \dfrac{\ln(1+5x^2)}{2x^2}$? [2 points]",
            "options": [r"$\dfrac{1}{2}$", r"$1$", r"$\dfrac{3}{2}$", r"$2$", r"$\dfrac{5}{2}$"],
            "answer": 5,
            "exp": r"$\lim_{x \to 0} \dfrac{\ln(1+5x^2)}{2x^2} = \lim_{x \to 0} \dfrac{\ln(1+5x^2)}{5x^2} \times \dfrac{5}{2} = 1 \times \dfrac{5}{2} = \dfrac{5}{2}$이므로 정답은 ⑤입니다.",
            "exp_en": r"$\lim_{x \to 0} \dfrac{\ln(1+5x^2)}{5x^2} \times \dfrac{5}{2} = \dfrac{5}{2}$. The correct answer is ⑤.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>자연로그 함수의 기본 극한 $\lim_{t \to 0} \frac{\ln(1+t)}{t} = 1$</b>을 이용하여 극한값을 계산하는 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  $$\lim_{x \to 0} \frac{\ln(1+5x^2)}{2x^2} = \lim_{x \to 0} \left\{\frac{\ln(1+5x^2)}{5x^2} \times \frac{5}{2}\right\} = 1 \times \frac{5}{2} = \frac{5}{2}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 구하는 값은 $\dfrac{5}{2}$이므로 정답은 <b>⑤번</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates a logarithmic limit using $\lim_{t \to 0} \frac{\ln(1+t)}{t} = 1$.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  $$\lim_{x \to 0} \frac{\ln(1+5x^2)}{2x^2} = \frac{5}{2} \lim_{x \to 0} \frac{\ln(1+5x^2)}{5x^2} = \frac{5}{2}$$
</p>

<h4>✨ [Final Answer & Practical Tips]</h4>
<p>
  The correct answer is <b>choice ⑤ ($\dfrac{5}{2}$)</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 미적 24번: c2610m24
    # -------------------------------------------------------------------------
    {
        "slug": "c2610m24",
        "qNum": "미적 24",
        "subject": "미적분",
        "title": "[2026학년도 10월 고3 미적 24번] 분수함수의 분리를 통한 정적분 계산",
        "title_en": "[2026 AY Oct Exam Grade 12 Calculus #24] Definite Integral of a Rational Function via Termwise Division",
        "summary_ko": "(x+1)/x^2을 1/x + 1/x^2으로 쪼개어 [ln x - 1/x]_1^2 = ln 2 + 1/2 구하기",
        "summary_en": "Split (x+1)/x^2 into 1/x + 1/x^2 and integrate from 1 to 2 to obtain ln 2 + 1/2.",
        "tags": ["미적분", "적분법", "여러가지함수의정적분", "분수함수의적분", "24번"],
        "symbols": [
            {"sym": r"$\dfrac{x+1}{x^2} = \dfrac{1}{x} + \dfrac{1}{x^2}$", "desc": "분자를 분모 x^2으로 각각 나누어 두 분수로 분리", "desc_en": "Splitting a fraction into two simpler terms."},
            {"sym": r"$\int \dfrac{1}{x}dx = \ln|x| + C,\quad \int \dfrac{1}{x^2}dx = -\dfrac{1}{x} + C$", "desc": "1/x과 1/x^2의 부정적분 공식", "desc_en": "Antiderivatives of 1/x and 1/x^2."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 분수 쪼개기] $\\dfrac{x + 1}{x^2}$을 두 분수의 합으로 나누기",
                "title_en": "🔰 Step 1 · [Elementary Fraction Splitting] Splitting $\\dfrac{x + 1}{x^2}$ into two fractions",
                "knowledge": r"초등학교 분수 덧셈에서 $\frac{a + b}{c} = \frac{a}{c} + \frac{b}{c}$로 쪼갤 수 있듯이, $\frac{x + 1}{x^2} = \frac{x}{x^2} + \frac{1}{x^2} = \frac{1}{x} + \frac{1}{x^2}$로 나누어 씁니다.",
                "knowledge_en": r"Just as $\frac{a+b}{c} = \frac{a}{c} + \frac{b}{c}$ in elementary fractions, $\frac{x+1}{x^2} = \frac{x}{x^2} + \frac{1}{x^2} = \frac{1}{x} + \frac{1}{x^2}$.",
                "questions": [
                    {
                        "level_label": "초등 분수 분리 디딤돌 1",
                        "level_label_en": "Elementary Fraction Split Step 1",
                        "stem": r"초등학교 분수 약분과 덧셈 원리로 $\frac{x + 1}{x^2}$을 두 분수의 합으로 바르게 쪼갠 것은?",
                        "stem_en": r"Using elementary fraction splitting, how is $\frac{x + 1}{x^2}$ written as a sum of two simpler fractions?",
                        "options": [r"$1 + \frac{1}{x}$", r"$\frac{1}{x} + \frac{1}{x^2}$", r"$\frac{1}{x^2} + \frac{1}{x^3}$", r"$x + \frac{1}{x^2}$", r"$\frac{2}{x}$"],
                        "answer": 2,
                        "exp": r"$\frac{x}{x^2} + \frac{1}{x^2} = \frac{1}{x} + \frac{1}{x^2}$입니다.",
                        "exp_en": r"$\frac{x}{x^2} + \frac{1}{x^2} = \frac{1}{x} + \frac{1}{x^2}$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [앞부분 적분] $\\int_1^2 \\dfrac{1}{x}dx$ 계산하기",
                "title_en": "🌿 Step 2 · [First Integral] Computing $\\int_1^2 \\dfrac{1}{x}dx$",
                "knowledge": r"$\frac{1}{x}$의 부정적분은 $\ln|x|$이고 $\ln 1 = 0$이므로 $\left[\ln x\right]_1^2 = \ln 2 - \ln 1 = \ln 2$입니다.",
                "knowledge_en": r"$\int_1^2 \frac{1}{x}dx = [\ln x]_1^2 = \ln 2 - 0 = \ln 2$.",
                "questions": [
                    {
                        "level_label": "로그 정적분 디딤돌 2",
                        "level_label_en": "Log Integral Step 2",
                        "stem": r"$\int_1^2 \frac{1}{x}dx = [\ln x]_1^2$의 값은?",
                        "stem_en": r"What is the value of $\int_1^2 \frac{1}{x}dx = [\ln x]_1^2$?",
                        "options": [r"$0$", r"$\ln 2$", r"$1$", r"$2\ln 2$", r"$\ln 2 + 1$"],
                        "answer": 2,
                        "exp": r"$\ln 2 - \ln 1 = \ln 2 - 0 = \ln 2$입니다.",
                        "exp_en": r"$\ln 2 - \ln 1 = \ln 2$."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [뒷부분 부정적분] $\\dfrac{1}{x^2} = x^{-2}$의 부정적분 구하기",
                "title_en": "🌱 Step 3 · [Second Antiderivative] Antiderivative of $\\dfrac{1}{x^2} = x^{-2}$",
                "knowledge": r"$\left(-\frac{1}{x}\right)' = \frac{1}{x^2}$이므로 $\frac{1}{x^2}$의 부정적분은 $-\frac{1}{x}$입니다.",
                "knowledge_en": r"Since $\left(-\frac{1}{x}\right)' = \frac{1}{x^2}$, the antiderivative of $\frac{1}{x^2}$ is $-\frac{1}{x}$.",
                "questions": [
                    {
                        "level_label": "분수 부정적분 디딤돌 3",
                        "level_label_en": "Power Antiderivative Step 3",
                        "stem": r"미분하여 $\frac{1}{x^2}$이 되는 함수(부정적분, 적분상수 제외)는?",
                        "stem_en": r"Which function differentiates to $\frac{1}{x^2}$?",
                        "options": [r"$\frac{1}{x}$", r"$-\frac{1}{x}$", r"$\frac{2}{x}$", r"$-\frac{2}{x}$", r"$\ln(x^2)$"],
                        "answer": 2,
                        "exp": r"$(x^{-1})' = -x^{-2}$이므로 $\left(-\frac{1}{x}\right)' = \frac{1}{x^2}$입니다.",
                        "exp_en": r"$\left(-\frac{1}{x}\right)' = \frac{1}{x^2}$."
                    }
                ]
            },
            {
                "title": "🌳 4단계 · [뒷부분 정적분] $\\left[-\\dfrac{1}{x}\\right]_1^2$ 계산하기",
                "title_en": "🌳 Step 4 · [Second Definite Integral] Evaluating $\\left[-\\dfrac{1}{x}\\right]_1^2$",
                "knowledge": r"위끝 $2$와 아래끝 $1$을 대입하면 $\left(-\frac{1}{2}\right) - (-1) = -\frac{1}{2} + 1 = \frac{1}{2}$입니다.",
                "knowledge_en": r"$\left[-\frac{1}{x}\right]_1^2 = -\frac{1}{2} - (-1) = \frac{1}{2}$.",
                "questions": [
                    {
                        "level_label": "분수 정적분 디딤돌 4",
                        "level_label_en": "Definite Evaluation Step 4",
                        "stem": r"$\left[-\frac{1}{x}\right]_1^2 = -\frac{1}{2} - (-1)$을 계산한 값은?",
                        "stem_en": r"What is $\left[-\frac{1}{x}\right]_1^2 = -\frac{1}{2} - (-1)$?",
                        "options": [r"$-\frac{3}{2}$", r"$-\frac{1}{2}$", r"$\frac{1}{2}$", r"$1$", r"$\frac{3}{2}$"],
                        "answer": 3,
                        "exp": r"$-\frac{1}{2} + 1 = \frac{1}{2}$입니다.",
                        "exp_en": r"$-\frac{1}{2} + 1 = \frac{1}{2}$."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [최종 종합] 두 정적분 결과 더하기",
                "title_en": "💎 Step 5 · [Final Synthesis] Combining both parts",
                "knowledge": r"앞부분 $\ln 2$와 뒷부분 $\frac{1}{2}$을 더하면 $\ln 2 + \frac{1}{2}$이 됩니다.",
                "knowledge_en": r"Combine $\ln 2$ and $\frac{1}{2}$ to get $\ln 2 + \frac{1}{2}$.",
                "questions": [
                    {
                        "level_label": "최종 종합 디딤돌 5",
                        "level_label_en": "Final Synthesis Step 5",
                        "stem": r"$\int_1^2 \frac{x+1}{x^2}dx$의 값은?",
                        "stem_en": r"What is the value of $\int_1^2 \frac{x+1}{x^2}dx$?",
                        "options": [r"$\ln 2 + \frac{1}{2}$", r"$\ln 2 + 1$", r"$2\ln 2 + \frac{1}{2}$", r"$2\ln 2 + 1$", r"$2\ln 2 + \frac{3}{2}$"],
                        "answer": 1,
                        "exp": r"$\left[\ln x - \frac{1}{x}\right]_1^2 = \ln 2 + \frac{1}{2}$이므로 정답은 ①입니다.",
                        "exp_en": r"$\ln 2 + \frac{1}{2}$ (choice ①)."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"$\int_1^2 \dfrac{x+1}{x^2}dx$의 값은? [3점]",
            "stem_en": r"What is the value of $\int_1^2 \dfrac{x+1}{x^2}dx$? [3 points]",
            "options": [r"$\ln 2 + \dfrac{1}{2}$", r"$\ln 2 + 1$", r"$2\ln 2 + \dfrac{1}{2}$", r"$2\ln 2 + 1$", r"$2\ln 2 + \dfrac{3}{2}$"],
            "answer": 1,
            "exp": r"$\int_1^2 \left(\dfrac{1}{x} + \dfrac{1}{x^2}\right)dx = \left[\ln x - \dfrac{1}{x}\right]_1^2 = \left(\ln 2 - \dfrac{1}{2}\right) - (0 - 1) = \ln 2 + \dfrac{1}{2}$입니다.",
            "exp_en": r"$\int_1^2 \left(\dfrac{1}{x} + \dfrac{1}{x^2}\right)dx = \left[\ln x - \dfrac{1}{x}\right]_1^2 = \ln 2 + \dfrac{1}{2}$.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 분수식 $\frac{x+1}{x^2}$을 $\frac{1}{x} + \frac{1}{x^2}$으로 분리하여 <b>로그함수와 유리함수의 정적분</b>을 계산하는 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  $$\int_1^2 \frac{x+1}{x^2}dx = \int_1^2 \left(\frac{1}{x} + \frac{1}{x^2}\right)dx = \left[\ln x - \frac{1}{x}\right]_1^2 = \left(\ln 2 - \frac{1}{2}\right) - (\ln 1 - 1) = \ln 2 + \frac{1}{2}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 구하는 값은 $\ln 2 + \dfrac{1}{2}$이므로 정답은 <b>①번</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates a definite integral by splitting the integrand into $\frac{1}{x} + x^{-2}$.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  $$\int_1^2 \left(\frac{1}{x} + \frac{1}{x^2}\right)dx = \left[\ln x - \frac{1}{x}\right]_1^2 = \ln 2 - \frac{1}{2} + 1 = \ln 2 + \frac{1}{2}$$
</p>

<h4>✨ [Final Answer & Practical Tips]</h4>
<p>
  The correct answer is <b>choice ① ($\ln 2 + \dfrac{1}{2}$)</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 미적 25번: c2610m25
    # -------------------------------------------------------------------------
    {
        "slug": "c2610m25",
        "qNum": "미적 25",
        "subject": "미적분",
        "title": "[2026학년도 10월 고3 미적 25번] 이차부등식과 수열의 극한의 대소 관계 (샌드위치 정리)",
        "title_en": "[2026 AY Oct Exam Grade 12 Calculus #25] Quadratic Inequality and Squeeze Theorem for Sequence Limits",
        "summary_ko": "이차부등식을 풀어 (n^2-n)/k < a_n < (n^2+n)/k를 얻고 샌드위치 정리로 1/(4k)=k에서 k=1/2 구하기",
        "summary_en": "Factor the quadratic inequality to bound a_n between (n^2-n)/k and (n^2+n)/k, then apply the Squeeze Theorem to get 1/(4k)=k and k=1/2.",
        "tags": ["미적분", "수열의극한", "극한의대소관계", "샌드위치정리", "이차부등식", "25번"],
        "symbols": [
            {"sym": r"$(ka_n - n^2 + n)(ka_n - n^2 - n) < 0$", "desc": "합차공식 X^2 - n^2 < 0으로 인수분해한 이차부등식", "desc_en": "Factoring the quadratic inequality via difference of squares."},
            {"sym": r"$\dfrac{n^2 - n}{k} < a_n < \dfrac{n^2 + n}{k}$", "desc": "양수 k로 나누어 구한 수열 a_n의 양쪽 범위", "desc_en": "Sandwich bounds on a_n after dividing by k > 0."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 곱셈과 제곱] $4k^2 = 1$을 만족하는 양수 $k$ 구하기",
                "title_en": "🔰 Step 1 · [Elementary Multiplication] Finding positive $k$ satisfying $4k^2 = 1$",
                "knowledge": r"초등학교 분수 곱셈에서 $\frac{1}{2} \times \frac{1}{2} = \frac{1}{4}$이고 여기에 $4$를 곱하면 $1$이 됩니다! 이 문제의 마지막 단계에서 나오는 방정식 $\frac{1}{4k} = k \iff 4k^2 = 1$을 먼저 초등 분수 곱셈으로 확인해 봅시다.",
                "knowledge_en": r"By elementary fraction multiplication, $\left(\frac{1}{2}\right)^2 = \frac{1}{4}$, so $4 \times \left(\frac{1}{2}\right)^2 = 1$.",
                "questions": [
                    {
                        "level_label": "초등 분수 곱셈 디딤돌 1",
                        "level_label_en": "Elementary Fraction Product Step 1",
                        "stem": r"초등학교 분수 곱셈 원리에 따라 $4 \times k \times k = 1$ ($k > 0$)을 만족시키는 분수 $k$는?",
                        "stem_en": r"Using elementary fraction multiplication, which positive fraction $k$ satisfies $4 \times k \times k = 1$?",
                        "options": [r"$\frac{1}{4}$", r"$\frac{1}{2}$", r"$\frac{3}{4}$", r"$1$", r"$\frac{5}{4}$"],
                        "answer": 2,
                        "exp": r"$k^2 = \frac{1}{4}$이고 $k > 0$이므로 $k = \frac{1}{2}$입니다.",
                        "exp_en": r"$k^2 = \frac{1}{4} \implies k = \frac{1}{2}$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [완전제곱식 변형] 부등식 $(ka_n - n^2)^2 < n^2$으로 바꾸기",
                "title_en": "🌿 Step 2 · [Completing the Square] Rewriting as $(ka_n - n^2)^2 < n^2$",
                "knowledge": r"$k^2a_n^2 - 2kn^2a_n + n^4 - n^2 < 0$에서 앞의 세 항은 $(ka_n - n^2)^2$입니다! 따라서 $(ka_n - n^2)^2 < n^2 \implies -n < ka_n - n^2 < n$이 됩니다.",
                "knowledge_en": r"The first three terms form $(ka_n - n^2)^2$, so $(ka_n - n^2)^2 < n^2 \implies -n < ka_n - n^2 < n$.",
                "questions": [
                    {
                        "level_label": "부등식 정리 디딤돌 2",
                        "level_label_en": "Inequality Bounds Step 2",
                        "stem": r"$-n < ka_n - n^2 < n$의 각 변에 $n^2$을 더하고 양수 $k$로 나누었을 때, $a_n$의 범위는?",
                        "stem_en": r"Adding $n^2$ and dividing by $k > 0$ in $-n < ka_n - n^2 < n$ gives which bounds for $a_n$?",
                        "options": [
                            r"$\frac{n^2 - n}{k} < a_n < \frac{n^2 + n}{k}$",
                            r"$k(n^2 - n) < a_n < k(n^2 + n)$",
                            r"$\frac{n - 1}{k} < a_n < \frac{n + 1}{k}$",
                            r"$\frac{n^2}{k} < a_n < \frac{2n^2}{k}$",
                            r"$-n < a_n < n$"
                        ],
                        "answer": 1,
                        "exp": r"$n^2 - n < ka_n < n^2 + n$을 양수 $k$로 나누면 $\frac{n^2 - n}{k} < a_n < \frac{n^2 + n}{k}$입니다.",
                        "exp_en": r"$\frac{n^2 - n}{k} < a_n < \frac{n^2 + n}{k}$."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [최고차항 계수 비] $\\lim_{n \\to \\infty} \\dfrac{n^2 \\pm n}{k(4n^2 + 1)}$ 구하기",
                "title_en": "🌱 Step 3 · [Leading Coefficient Ratio] Evaluating $\\lim_{n \\to \\infty} \\dfrac{n^2 \\pm n}{k(4n^2 + 1)}$",
                "knowledge": r"각 변을 $4n^2 + 1$로 나누고 $n \to \infty$ 극한을 취하면, 분모·분자의 최고차항($n^2$)의 계수 비인 $\frac{1}{4k}$로 수렴합니다.",
                "knowledge_en": r"Dividing by $4n^2 + 1$ and taking $n \to \infty$, both bounds converge to the ratio of the $n^2$ coefficients: $\frac{1}{4k}$.",
                "questions": [
                    {
                        "level_label": "샌드위치 극한 디딤돌 3",
                        "level_label_en": "Squeeze Limit Step 3",
                        "stem": r"극한의 대소 관계(샌드위치 정리)에 의하여 $\lim_{n \to \infty} \frac{a_n}{4n^2 + 1}$을 $k$에 대한 식으로 나타내면?",
                        "stem_en": r"By the Squeeze Theorem, what is $\lim_{n \to \infty} \frac{a_n}{4n^2 + 1}$ in terms of $k$?",
                        "options": [r"$\frac{1}{k}$", r"$\frac{1}{2k}$", r"$\frac{1}{4k}$", r"$\frac{k}{4}$", r"$4k$"],
                        "answer": 3,
                        "exp": r"분자의 $n^2$ 계수는 $1$, 분모의 $n^2$ 계수는 $4k$이므로 $\frac{1}{4k}$입니다.",
                        "exp_en": r"The ratio of leading coefficients is $\frac{1}{4k}$."
                    }
                ]
            },
            {
                "title": "🌳 4단계 · [방정식 세우기] $\\dfrac{1}{4k} = k$ 정리하기",
                "title_en": "🌳 Step 4 · [Setting Up Equation] Solving $\\dfrac{1}{4k} = k$",
                "knowledge": r"문제에서 극한값이 $k$라고 했으므로 $\frac{1}{4k} = k \implies k^2 = \frac{1}{4}$입니다.",
                "knowledge_en": r"Equating the limit to $k$ gives $\frac{1}{4k} = k \implies k^2 = \frac{1}{4}$.",
                "questions": [
                    {
                        "level_label": "k^2 구하기 디딤돌 4",
                        "level_label_en": "Finding k^2 Step 4",
                        "stem": r"$\frac{1}{4k} = k$에서 $k^2$의 값은?",
                        "stem_en": r"From $\frac{1}{4k} = k$, what is $k^2$?",
                        "options": [r"$\frac{1}{16}$", r"$\frac{1}{8}$", r"$\frac{1}{4}$", r"$\frac{1}{2}$", r"$1$"],
                        "answer": 3,
                        "exp": r"양변에 $k$를 곱하면 $k^2 = \frac{1}{4}$입니다.",
                        "exp_en": r"$k^2 = \frac{1}{4}$."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [최종 종합] 양수 $k$의 값 확정하기",
                "title_en": "💎 Step 5 · [Final Synthesis] Final value of $k > 0$",
                "knowledge": r"$k > 0$이므로 $k = \frac{1}{2}$입니다.",
                "knowledge_en": r"Since $k > 0$, $k = \frac{1}{2}$.",
                "questions": [
                    {
                        "level_label": "최종 종합 디딤돌 5",
                        "level_label_en": "Final Synthesis Step 5",
                        "stem": r"양수 $k$의 값은?",
                        "stem_en": r"What is the value of the positive constant $k$?",
                        "options": [r"$\frac{1}{4}$", r"$\frac{1}{2}$", r"$\frac{3}{4}$", r"$1$", r"$\frac{5}{4}$"],
                        "answer": 2,
                        "exp": r"$k = \frac{1}{2}$이므로 정답은 ②입니다.",
                        "exp_en": r"$k = \frac{1}{2}$ (choice ②)."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"수열 $\{a_n\}$이 모든 자연수 $n$에 대하여 부등식 $k^2a_n^2 - 2kn^2a_n + n^4 - n^2 < 0$을 만족시킨다. $\lim_{n \to \infty} \dfrac{a_n}{4n^2 + 1} = k$일 때, 양수 $k$의 값은? [3점]",
            "stem_en": r"A sequence $\{a_n\}$ satisfies $k^2a_n^2 - 2kn^2a_n + n^4 - n^2 < 0$ for all natural numbers $n$. When $\lim_{n \to \infty} \dfrac{a_n}{4n^2 + 1} = k$, what is the positive constant $k$? [3 points]",
            "options": [r"$\dfrac{1}{4}$", r"$\dfrac{1}{2}$", r"$\dfrac{3}{4}$", r"$1$", r"$\dfrac{5}{4}$"],
            "answer": 2,
            "exp": r"$(ka_n - n^2)^2 < n^2$에서 $\dfrac{n^2-n}{k} < a_n < \dfrac{n^2+n}{k}$이므로 $\lim_{n\to\infty}\dfrac{a_n}{4n^2+1} = \dfrac{1}{4k} = k$에서 $k = \dfrac{1}{2}$입니다.",
            "exp_en": r"From $(ka_n - n^2)^2 < n^2$, we get $\dfrac{n^2-n}{k} < a_n < \dfrac{n^2+n}{k}$. By the Squeeze Theorem, $\dfrac{1}{4k} = k \implies k = \dfrac{1}{2}$.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>이차부등식을 풀어 수열 $a_n$의 범위를 구한 뒤 수열의 극한의 대소 관계(샌드위치 정리)</b>를 적용하는 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 이차부등식 풀기</b><br>
  $$(ka_n - n^2)^2 - n^2 < 0 \iff (ka_n - n^2 + n)(ka_n - n^2 - n) < 0$$
  $k > 0$이므로 양변을 $k$로 나누면:<br>
  $$\frac{n^2 - n}{k} < a_n < \frac{n^2 + n}{k}$$<br>
  <b>2단계: 샌드위치 정리 적용</b><br>
  각 변을 $4n^2 + 1 > 0$으로 나누고 $n \to \infty$ 극한을 취하면:<br>
  $$\lim_{n \to \infty} \frac{a_n}{4n^2 + 1} = \frac{1}{4k} = k \implies k^2 = \frac{1}{4}$$
  $k > 0$이므로 $k = \frac{1}{2}$입니다.
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 양수 $k$의 값은 $\dfrac{1}{2}$이므로 정답은 <b>②번</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem applies the <b>Squeeze Theorem</b> after solving a quadratic inequality for $a_n$.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Bound $a_n$</b><br>
  $$(ka_n - n^2)^2 < n^2 \implies \frac{n^2 - n}{k} < a_n < \frac{n^2 + n}{k}$$<br>
  <b>Step 2: Apply the Squeeze Theorem</b><br>
  $$\lim_{n \to \infty} \frac{a_n}{4n^2 + 1} = \frac{1}{4k} = k \implies k = \frac{1}{2}$$
</p>

<h4>✨ [Final Answer & Practical Tips]</h4>
<p>
  The correct answer is <b>choice ② ($\dfrac{1}{2}$)</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 미적 26번: c2610m26
    # -------------------------------------------------------------------------
    {
        "slug": "c2610m26",
        "qNum": "미적 26",
        "subject": "미적분",
        "title": "[2026학년도 10월 고3 미적 26번] 반원을 단면으로 하는 입체도형의 부피와 부분적분",
        "title_en": "[2026 AY Oct Exam Grade 12 Calculus #26] Volume of a Solid with Semicircular Cross-Sections",
        "summary_ko": "지름이 sqrt(1+(ln x)^2)인 반원의 넓이 S(x)=(pi/8)(1+(ln x)^2)을 1부터 e까지 정적분하여 (2e-3)pi/8 구하기",
        "summary_en": "Integrate the semicircular cross-sectional area S(x)=(pi/8)(1+(ln x)^2) from 1 to e to obtain (2e-3)pi/8.",
        "tags": ["미적분", "적분법", "정적분의활용", "입체도형의부피", "부분적분", "26번"],
        "symbols": [
            {"sym": r"$S(x) = \dfrac{1}{2}\pi r^2 = \dfrac{\pi}{8}D^2$", "desc": "지름의 길이가 D일 때 반원의 넓이는 (pi/8)*D^2", "desc_en": "Area of a semicircle with diameter D is (pi/8)D^2."},
            {"sym": r"$\int_1^e (\ln x)^2 dx = \left[x(\ln x)^2 - 2x\ln x + 2x\right]_1^e = e - 2$", "desc": "부분적분을 이용한 (ln x)^2의 정적분", "desc_en": "Definite integral of (ln x)^2 evaluated via integration by parts."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 원의 넓이] 지름이 $D$일 때 반원의 넓이 식 구하기",
                "title_en": "🔰 Step 1 · [Elementary Circle Area] Area of a semicircle with diameter $D$",
                "knowledge": r"초등학교에서 반지름 $r$은 지름 $D$의 절반인 $\frac{D}{2}$입니다. 원의 넓이 $\pi r^2$의 절반인 반원의 넓이는 $\frac{1}{2} \times \pi \times \left(\frac{D}{2}\right)^2 = \frac{\pi}{8}D^2$입니다!",
                "knowledge_en": r"In elementary geometry, radius $r = \frac{D}{2}$, so the area of a semicircle is $\frac{1}{2}\pi r^2 = \frac{1}{2}\pi\left(\frac{D}{2}\right)^2 = \frac{\pi}{8}D^2$.",
                "questions": [
                    {
                        "level_label": "초등 반원 넓이 디딤돌 1",
                        "level_label_en": "Elementary Semicircle Area Step 1",
                        "stem": r"초등학교 원의 넓이 원리에 따라 지름의 길이가 $D = \sqrt{1 + (\ln x)^2}$인 반원의 단면 넓이 $S(x) = \frac{\pi}{8}D^2$은?",
                        "stem_en": r"Using elementary circle area, what is the area $S(x) = \frac{\pi}{8}D^2$ of a semicircle with diameter $D = \sqrt{1 + (\ln x)^2}$?",
                        "options": [
                            r"$\frac{\pi}{2}\{1 + (\ln x)^2\}$",
                            r"$\frac{\pi}{4}\{1 + (\ln x)^2\}$",
                            r"$\frac{\pi}{8}\{1 + (\ln x)^2\}$",
                            r"$\pi\{1 + (\ln x)^2\}$",
                            r"$\frac{\pi}{16}\{1 + (\ln x)^2\}$"
                        ],
                        "answer": 3,
                        "exp": r"근호가 제곱으로 벗겨지므로 $S(x) = \frac{\pi}{8}\{1 + (\ln x)^2\}$입니다.",
                        "exp_en": r"$S(x) = \frac{\pi}{8}\{1 + (\ln x)^2\}$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [상수항 적분] $\\int_1^e 1\\,dx$ 계산하기",
                "title_en": "🌿 Step 2 · [Constant Integral] Evaluating $\\int_1^e 1\\,dx$",
                "knowledge": r"$1$을 $1$부터 $e$까지 정적분하면 구간의 길이 $e - 1$입니다.",
                "knowledge_en": r"$\int_1^e 1\,dx = e - 1$.",
                "questions": [
                    {
                        "level_label": "상수 적분 디딤돌 2",
                        "level_label_en": "Constant Integral Step 2",
                        "stem": r"$\int_1^e 1\,dx = [x]_1^e$의 값은?",
                        "stem_en": r"What is $\int_1^e 1\,dx = [x]_1^e$?",
                        "options": [r"$1$", r"$e - 2$", r"$e - 1$", r"$e$", r"$e + 1$"],
                        "answer": 3,
                        "exp": r"$e - 1$입니다.",
                        "exp_en": r"$e - 1$."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [부분적분] $\\int_1^e (\\ln x)^2 dx$ 계산하기",
                "title_en": "🌱 Step 3 · [Integration by Parts] Evaluating $\\int_1^e (\\ln x)^2 dx$",
                "knowledge": r"부분적분을 적용하면 $\int (\ln x)^2 dx = x(\ln x)^2 - 2\int \ln x\,dx = x(\ln x)^2 - 2x\ln x + 2x + C$입니다. 위끝 $e$와 아래끝 $1$을 대입하면 $(e - 2e + 2e) - (0 - 0 + 2) = e - 2$입니다.",
                "knowledge_en": r"Using integration by parts, $\int_1^e (\ln x)^2 dx = \left[x(\ln x)^2 - 2x\ln x + 2x\right]_1^e = e - 2$.",
                "questions": [
                    {
                        "level_label": "로그제곱 정적분 디딤돌 3",
                        "level_label_en": "Log Squared Integral Step 3",
                        "stem": r"$\int_1^e (\ln x)^2 dx = \left[x(\ln x)^2 - 2x\ln x + 2x\right]_1^e$를 계산한 값은?",
                        "stem_en": r"What is the value of $\int_1^e (\ln x)^2 dx$?",
                        "options": [r"$e - 3$", r"$e - 2$", r"$e - 1$", r"$2e - 3$", r"$2e - 2$"],
                        "answer": 2,
                        "exp": r"$x = e$일 때 $e(1) - 2e(1) + 2e = e$이고, $x = 1$일 때 $2$이므로 $e - 2$입니다.",
                        "exp_en": r"$e - 2$."
                    }
                ]
            },
            {
                "title": "🌳 4단계 · [적분 합산] $(e - 1) + (e - 2)$ 계산하기",
                "title_en": "🌳 Step 4 · [Summing Integrals] Computing $(e - 1) + (e - 2)$",
                "knowledge": r"$\int_1^e \{1 + (\ln x)^2\}dx = (e - 1) + (e - 2) = 2e - 3$입니다.",
                "knowledge_en": r"$(e - 1) + (e - 2) = 2e - 3$.",
                "questions": [
                    {
                        "level_label": "적분 합산 디딤돌 4",
                        "level_label_en": "Integral Sum Step 4",
                        "stem": r"$(e - 1) + (e - 2)$를 간단히 한 식은?",
                        "stem_en": r"Simplify $(e - 1) + (e - 2)$.",
                        "options": [r"$2e - 1$", r"$2e - 2$", r"$2e - 3$", r"$2e - 4$", r"$e - 3$"],
                        "answer": 3,
                        "exp": r"$2e - 3$입니다.",
                        "exp_en": r"$2e - 3$."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [최종 종합] 입체도형의 부피 $V$ 확정하기",
                "title_en": "💎 Step 5 · [Final Synthesis] Final volume $V$",
                "knowledge": r"앞의 상수 $\frac{\pi}{8}$을 곱하면 부피 $V = \frac{(2e - 3)\pi}{8}$가 완성됩니다.",
                "knowledge_en": r"Multiply by $\frac{\pi}{8}$ to get $V = \frac{(2e - 3)\pi}{8}$.",
                "questions": [
                    {
                        "level_label": "최종 종합 디딤돌 5",
                        "level_label_en": "Final Synthesis Step 5",
                        "stem": r"구하는 입체도형의 부피 $V = \int_1^e S(x)dx$는?",
                        "stem_en": r"What is the volume $V = \int_1^e S(x)dx$ of the solid?",
                        "options": [
                            r"$\frac{(2e - 1)\pi}{8}$",
                            r"$\frac{(e - 1)\pi}{4}$",
                            r"$\frac{(2e - 3)\pi}{8}$",
                            r"$\frac{(e - 2)\pi}{4}$",
                            r"$\frac{(2e - 5)\pi}{8}$"
                        ],
                        "answer": 3,
                        "exp": r"$V = \frac{\pi}{8}(2e - 3) = \frac{(2e - 3)\pi}{8}$이므로 정답은 ③입니다.",
                        "exp_en": r"$\frac{(2e - 3)\pi}{8}$ (choice ③)."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"그림과 같이 곡선 $y = \sqrt{1 + (\ln x)^2}$ ($1 \le x \le e$)와 $x$축 및 두 직선 $x = 1, x = e$로 둘러싸인 도형을 밑면으로 하는 입체도형이 있다. 이 입체도형을 $x$축에 수직인 평면으로 자른 단면이 모두 반원일 때, 이 입체도형의 부피는? [3점]",
            "stem_en": r"The base of a solid is bounded by $y = \sqrt{1 + (\ln x)^2}$ ($1 \le x \le e$), the $x$-axis, $x = 1$, and $x = e$. Every cross-section perpendicular to the $x$-axis is a semicircle. What is the volume of this solid? [3 points]",
            "options": [
                r"$\dfrac{(2e - 1)\pi}{8}$",
                r"$\dfrac{(e - 1)\pi}{4}$",
                r"$\dfrac{(2e - 3)\pi}{8}$",
                r"$\dfrac{(e - 2)\pi}{4}$",
                r"$\dfrac{(2e - 5)\pi}{8}$"
            ],
            "answer": 3,
            "exp": r"단면인 반원의 넓이는 $S(x) = \dfrac{\pi}{8}\{1 + (\ln x)^2\}$이므로 부피는 $\int_1^e S(x)dx = \dfrac{\pi}{8}\{(e-1) + (e-2)\} = \dfrac{(2e-3)\pi}{8}$입니다.",
            "exp_en": r"The semicircular cross-section has area $S(x) = \dfrac{\pi}{8}\{1 + (\ln x)^2\}$, so $V = \int_1^e S(x)dx = \dfrac{\pi}{8}\{(e-1) + (e-2)\} = \dfrac{(2e-3)\pi}{8}$.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>단면의 넓이 $S(x)$를 정적분하여 입체도형의 부피를 구하는 공식</b>과 <b>$(\ln x)^2$의 부분적분</b>을 결합한 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 단면의 넓이 $S(x)$ 구하기</b><br>
  지름의 길이가 $y = \sqrt{1 + (\ln x)^2}$인 반원의 반지름은 $r = \frac{1}{2}\sqrt{1 + (\ln x)^2}$이므로 단면의 넓이는:<br>
  $$S(x) = \frac{1}{2}\pi r^2 = \frac{\pi}{8}\left\{1 + (\ln x)^2\right\}$$<br>
  <b>2단계: 정적분으로 부피 $V$ 계산</b><br>
  $$V = \int_1^e \frac{\pi}{8}\left\{1 + (\ln x)^2\right\}dx = \frac{\pi}{8}\left[x + x(\ln x)^2 - 2x\ln x + 2x\right]_1^e = \frac{\pi}{8}\left\{(e + e) - (1 + 2)\right\} = \frac{(2e - 3)\pi}{8}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 입체도형의 부피는 $\dfrac{(2e - 3)\pi}{8}$이므로 정답은 <b>③번</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem computes the <b>volume of a solid by integrating semicircular cross-sectional areas</b>.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Cross-sectional area</b><br>
  $$S(x) = \frac{\pi}{8}\left\{1 + (\ln x)^2\right\}$$<br>
  <b>Step 2: Integrate from $1$ to $e$</b><br>
  $$V = \frac{\pi}{8}\int_1^e \left\{1 + (\ln x)^2\right\}dx = \frac{\pi}{8}\left[(e - 1) + (e - 2)\right] = \frac{(2e - 3)\pi}{8}$$
</p>

<h4>✨ [Final Answer & Practical Tips]</h4>
<p>
  The correct answer is <b>choice ③ ($\dfrac{(2e - 3)\pi}{8}$)</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 미적 27번: c2610m27
    # -------------------------------------------------------------------------
    {
        "slug": "c2610m27",
        "qNum": "미적 27",
        "subject": "미적분",
        "title": "[2026학년도 10월 고3 미적 27번] 구간별 정의된 지수함수의 미분가능성과 역함수의 미분법",
        "title_en": "[2026 AY Oct Exam Grade 12 Calculus #27] Differentiability of Piecewise Exponential Function and Derivative of Inverse",
        "summary_ko": "x=b에서의 연속·미분가능 조건으로 e^b=2, a=2를 구하고 f(x)=8을 만족하는 e^x=4에서 g'(8)=1/10 도출하기",
        "summary_en": "Use continuity and differentiability at x=b to find e^b=2 and a=2, solve f(x)=8 to get e^x=4, and compute g'(8)=1/f'(ln 4)=1/10.",
        "tags": ["미적분", "미분법", "미분가능성", "역함수의미분법", "지수함수", "27번"],
        "symbols": [
            {"sym": r"$f(b-) = f(b+),\quad f'(b-) = f'(b+)$", "desc": "경계점 x=b에서 미분가능하기 위한 함숫값 일치(연속)와 미분계수 일치 조건", "desc_en": "Continuity and matching left/right derivatives at x=b."},
            {"sym": r"$g'(8) = \dfrac{1}{f'(c)} \quad (f(c) = 8)$", "desc": "역함수의 미분법 공식", "desc_en": "Formula for the derivative of the inverse function at y=8."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 역수 약속] 역함수의 기울기는 원래 기울기를 뒤집은 역수!",
                "title_en": "🔰 Step 1 · [Elementary Reciprocal] Slope of the inverse is the reciprocal of the original slope",
                "knowledge": r"가로와 세로를 바꾼 역함수 $g(x)$의 미분계수 $g'(8)$은, $f(c) = 8$인 점에서 원래 함수의 미분계수 $f'(c)$를 초등학교 분수 뒤집기(역수)한 $\frac{1}{f'(c)}$입니다!",
                "knowledge_en": r"By elementary reciprocals, swapping $x$ and $y$ inverts the slope: if $f(c) = 8$ and $f'(c) = 10$, then $g'(8) = \frac{1}{10}$.",
                "questions": [
                    {
                        "level_label": "초등 역수 디딤돌 1",
                        "level_label_en": "Elementary Reciprocal Step 1",
                        "stem": r"초등학교 역수 구하기처럼 $f(c) = 8$이고 $f'(c) = 10$일 때, 역함수의 미분계수 $g'(8) = \frac{1}{f'(c)}$의 값은?",
                        "stem_en": r"Using elementary reciprocals, if $f(c) = 8$ and $f'(c) = 10$, what is $g'(8) = \frac{1}{f'(c)}$?",
                        "options": [r"$\frac{1}{16}$", r"$\frac{1}{14}$", r"$\frac{1}{12}$", r"$\frac{1}{10}$", r"$\frac{1}{8}$"],
                        "answer": 4,
                        "exp": r"$10$의 역수는 $\frac{1}{10}$입니다. 이제 왜 $f'(c) = 10$이 되는지 차근차근 확인해 봅시다!",
                        "exp_en": r"The reciprocal of $10$ is $\frac{1}{10}$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [미분가능 조건] $x = b$에서 좌미분계수와 우미분계수 같다고 놓기",
                "title_en": "🌿 Step 2 · [Differentiability] Equating left and right derivatives at $x = b$",
                "knowledge": r"$x < b$에서 $f'(x) = 2e^{2x}$이고, $x > b$에서 $f'(x) = 2e^x + 8e^{-x}$입니다. $x = b$에서 미분가능하므로 $2e^{2b} = 2e^b + 8e^{-b}$입니다. $t = e^b > 0$이라 하고 양변에 $\frac{t}{2}$를 곱하면 $t^3 - t^2 - 4 = (t - 2)(t^2 + t + 2) = 0$이 됩니다.",
                "knowledge_en": r"Equating derivatives at $x=b$ gives $2e^{2b} = 2e^b + 8e^{-b}$. Letting $t = e^b > 0$, we get $t^3 - t^2 - 4 = (t-2)(t^2+t+2) = 0$.",
                "questions": [
                    {
                        "level_label": "e^b 값 구하기 디딤돌 2",
                        "level_label_en": "Finding e^b Step 2",
                        "stem": r"$(t - 2)(t^2 + t + 2) = 0$에서 양수 $t = e^b$의 값은?",
                        "stem_en": r"What is the positive real root $t = e^b$ of $(t - 2)(t^2 + t + 2) = 0$?",
                        "options": [r"$1$", r"$2$", r"$3$", r"$4$", r"$8$"],
                        "answer": 2,
                        "exp": r"$t^2 + t + 2 > 0$이므로 실근은 $t = e^b = 2$ ($b = \ln 2$)입니다.",
                        "exp_en": r"$t = e^b = 2$."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [연속 조건] $x = b$에서 함숫값 같다고 놓아 상수 $a$ 구하기",
                "title_en": "🌱 Step 3 · [Continuity] Finding $a$ from continuity at $x = b$",
                "knowledge": r"$e^b = 2$를 양쪽 함숫값 $e^{2b} - 2 = 2e^b - 8e^{-b} + a$에 대입하면 $4 - 2 = 4 - 4 + a$가 됩니다.",
                "knowledge_en": r"Substituting $e^b = 2$ into $e^{2b} - 2 = 2e^b - 8e^{-b} + a$ gives $4 - 2 = 4 - 4 + a$.",
                "questions": [
                    {
                        "level_label": "상수 a 구하기 디딤돌 3",
                        "level_label_en": "Finding a Step 3",
                        "stem": r"$4 - 2 = 4 - 4 + a$에서 상수 $a$의 값은?",
                        "stem_en": r"From $4 - 2 = 4 - 4 + a$, what is $a$?",
                        "options": [r"$0$", r"$1$", r"$2$", r"$3$", r"$4$"],
                        "answer": 3,
                        "exp": r"$a = 2$입니다.",
                        "exp_en": r"$a = 2$."
                    }
                ]
            },
            {
                "title": "🌳 4단계 · [$f(c) = 8$ 풀기] $2e^c - 8e^{-c} + 2 = 8$을 만족하는 $e^c$ 찾기",
                "title_en": "🌳 Step 4 · [Solving $f(c) = 8$] Finding $e^c$ such that $f(c) = 8$",
                "knowledge": r"$x = b$일 때 $f(b) = 2 < 8$이므로 $f(c) = 8$인 $c$는 $c > b$ 범위에 있습니다. $2e^c - 8e^{-c} + 2 = 8 \implies e^c - 4e^{-c} - 3 = 0 \implies (e^c - 4)(e^c + 1) = 0$입니다.",
                "knowledge_en": r"Since $f(b) = 2 < 8$, $c > b$. Solving $2e^c - 8e^{-c} + 2 = 8$ gives $(e^c - 4)(e^c + 1) = 0$.",
                "questions": [
                    {
                        "level_label": "e^c 값과 미분계수 디딤돌 4",
                        "level_label_en": "Derivative f'(c) Step 4",
                        "stem": r"$e^c = 4$일 때, $f'(c) = 2e^c + 8e^{-c} = 2(4) + 8\left(\frac{1}{4}\right)$의 값은?",
                        "stem_en": r"When $e^c = 4$, what is $f'(c) = 2e^c + 8e^{-c} = 2(4) + 8\left(\frac{1}{4}\right)$?",
                        "options": [r"$6$", r"$8$", r"$10$", r"$12$", r"$14$"],
                        "answer": 3,
                        "exp": r"$8 + 2 = 10$입니다.",
                        "exp_en": r"$8 + 2 = 10$."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [최종 종합] $g'(8) = \\dfrac{1}{f'(c)}$ 확정하기",
                "title_en": "💎 Step 5 · [Final Synthesis] Final value of $g'(8)$",
                "knowledge": r"$f'(c) = 10$이므로 $g'(8) = \frac{1}{10}$입니다.",
                "knowledge_en": r"Since $f'(c) = 10$, $g'(8) = \frac{1}{10}$.",
                "questions": [
                    {
                        "level_label": "최종 종합 디딤돌 5",
                        "level_label_en": "Final Synthesis Step 5",
                        "stem": r"역함수 $g(x)$에 대하여 $g'(8)$의 값은?",
                        "stem_en": r"What is the value of $g'(8)$?",
                        "options": [r"$\frac{1}{16}$", r"$\frac{1}{14}$", r"$\frac{1}{12}$", r"$\frac{1}{10}$", r"$\frac{1}{8}$"],
                        "answer": 4,
                        "exp": r"$g'(8) = \frac{1}{10}$이므로 정답은 ④입니다.",
                        "exp_en": r"$\frac{1}{10}$ (choice ④)."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"두 상수 $a, b$에 대하여 실수 전체의 집합에서 미분가능한 함수 $f(x)$가 $x < b$일 때 $f(x) = e^{2x} - 2$, $x \ge b$일 때 $f(x) = 2e^x - 8e^{-x} + a$이다. 함수 $f(x)$의 역함수를 $g(x)$라 할 때, $g'(8)$의 값은? [3점]",
            "stem_en": r"A function $f(x)$ differentiable on $\mathbb{R}$ is defined by $f(x) = e^{2x} - 2$ for $x < b$ and $f(x) = 2e^x - 8e^{-x} + a$ for $x \ge b$. Let $g(x)$ be the inverse function of $f(x)$. What is the value of $g'(8)$? [3 points]",
            "options": [r"$\dfrac{1}{16}$", r"$\dfrac{1}{14}$", r"$\dfrac{1}{12}$", r"$\dfrac{1}{10}$", r"$\dfrac{1}{8}$"],
            "answer": 4,
            "exp": r"$x = b$에서의 미분가능성으로 $e^b = 2$, $a = 2$를 얻고, $f(c) = 8$ ($c \ge \ln 2$)에서 $e^c = 4$이므로 $g'(8) = \dfrac{1}{f'(\ln 4)} = \dfrac{1}{2(4) + 8(1/4)} = \dfrac{1}{10}$입니다.",
            "exp_en": r"Differentiability at $x = b$ gives $e^b = 2$ and $a = 2$. Solving $f(c) = 8$ gives $e^c = 4$, so $g'(8) = \dfrac{1}{f'(\ln 4)} = \dfrac{1}{10}$.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>구간별로 정의된 지수함수의 미분가능성</b>과 <b>역함수의 미분법</b>을 결합한 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: $x = b$에서의 미분가능 조건으로 $e^b$와 $a$ 구하기</b><br>
  미분계수가 일치해야 하므로 $2e^{2b} = 2e^b + 8e^{-b}$입니다. $t = e^b > 0$이라 하면:<br>
  $$t^3 - t^2 - 4 = (t - 2)(t^2 + t + 2) = 0 \implies t = e^b = 2$$
  연속 조건 $e^{2b} - 2 = 2e^b - 8e^{-b} + a$에 $e^b = 2$를 대입하면 $4 - 2 = 4 - 4 + a \implies a = 2$입니다.<br><br>
  <b>2단계: 역함수의 미분법으로 $g'(8)$ 구하기</b><br>
  $f(b) = 2 < 8$이므로 $f(c) = 8$인 $c$는 $c > b$에 존재합니다:<br>
  $$2e^c - 8e^{-c} + 2 = 8 \implies (e^c - 4)(e^c + 1) = 0 \implies e^c = 4$$
  따라서 $f'(c) = 2e^c + 8e^{-c} = 2(4) + 8\left(\frac{1}{4}\right) = 10$이므로:<br>
  $$g'(8) = \frac{1}{f'(c)} = \frac{1}{10}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 $g'(8) = \dfrac{1}{10}$이므로 정답은 <b>④번</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem combines <b>differentiability at a boundary point</b> with the <b>Inverse Function Theorem</b>.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Continuity and differentiability at $x = b$</b><br>
  $$2e^{2b} = 2e^b + 8e^{-b} \implies e^b = 2, \quad e^{2b} - 2 = 2e^b - 8e^{-b} + a \implies a = 2$$<br>
  <b>Step 2: Derivative of the inverse at $y = 8$</b><br>
  From $2e^c - 8e^{-c} + 2 = 8$, we get $e^c = 4$. Thus $f'(c) = 2(4) + 8(1/4) = 10$ and $g'(8) = \frac{1}{10}$.
</p>

<h4>✨ [Final Answer & Practical Tips]</h4>
<p>
  The correct answer is <b>choice ④ ($\dfrac{1}{10}$)</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 미적 28번: c2610m28
    # -------------------------------------------------------------------------
    {
        "slug": "c2610m28",
        "qNum": "미적 28",
        "subject": "미적분",
        "title": "[2026학년도 10월 고3 미적 28번] 곡선과 직선의 접점 매개변수화 및 음함수·합성함수 미분법",
        "title_en": "[2026 AY Oct Exam Grade 12 Calculus #28] Tangent Parameterization and Implicit Differentiation",
        "summary_ko": "f'(s)=s*sec^2(s)=s/t에서 t=cos^2(s)를 얻고 g(t)=f(s)-s^2/t를 미분하여 g'(1/2)=(pi^2+2pi)/4 구하기",
        "summary_en": "From f'(s)=s*sec^2(s)=s/t deduce t=cos^2(s), differentiate g(t)=f(s)-s^2/t with respect to t, and evaluate g'(1/2)=(pi^2+2pi)/4.",
        "tags": ["미적분", "미분법", "접선의방정식", "매개변수미분법", "삼각함수의미분", "28번"],
        "symbols": [
            {"sym": r"$f'(s) = s\sec^2 s$", "desc": "f(x)=x tan x - ln(cos x)를 미분하여 간단히 정리한 도함수", "desc_en": "Simplified derivative of f(x)=x tan x - ln(cos x)."},
            {"sym": r"$t = \cos^2 s$", "desc": "접점의 x좌표 s에서 f'(s) = s/t가 성립할 조건", "desc_en": "Relation between parameter t and point of tangency s."},
            {"sym": r"$g'(t) = \dfrac{s^2}{t^2}$", "desc": "g(t) = f(s) - s*f'(s)를 t에 대해 미분할 때 앞의 항들이 소거되고 남는 도함수!", "desc_en": "Legendre-type cancellation when differentiating the y-intercept g(t)."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 소거 규칙] $(A - A) + B$에서 똑같은 항 지우기",
                "title_en": "🔰 Step 1 · [Elementary Cancellation] Canceling $A - A$ in $(A - A) + B$",
                "knowledge": r"접선의 $y$절편 $g(t) = f(s) - \frac{s^2}{t}$를 미분할 때, $f'(s) = \frac{s}{t}$이므로 앞부분 미분 $\left(f'(s) - \frac{2s}{t}\right)\frac{ds}{dt}$와 뒷부분 미분 $+\frac{s^2}{t^2}$을 합치면 놀라운 소거가 일어납니다! 먼저 초등학교 덧셈·뺄셈처럼 도함수 $f'(x)$에서 똑같은 항이 지워지는지 확인해 봅시다.",
                "knowledge_en": r"By elementary cancellation, identical terms with opposite signs cancel out when differentiating $f(x) = x\tan x - \ln(\cos x)$.",
                "questions": [
                    {
                        "level_label": "초등 항 지우기 디딤돌 1",
                        "level_label_en": "Elementary Cancellation Step 1",
                        "stem": r"초등학교 덧셈·뺄셈 소거처럼 $f(x) = x\tan x - \ln(\cos x)$를 미분한 식 $f'(x) = (1 \cdot \tan x + x\sec^2 x) - (-\tan x)$를 정리할 때, 주의! $-\ln(\cos x)$를 미분하면 $+\frac{\sin x}{\cos x} = +\tan x$일까, $-\tan x$일까? 잠깐! 문제의 함수가 $f(x) = x\tan x + \ln(\cos x)$인지 확인해 봅시다: $(\ln(\cos x))' = -\tan x$이므로 $x\tan x + \ln(\cos x)$를 미분하면 $\tan x - \tan x = 0$이 지워져 남는 항은?",
                        "stem_en": r"Using elementary cancellation, when differentiating $f(x) = x\tan x + \ln(\cos x)$, since $(\ln(\cos x))' = -\tan x$, the $\tan x - \tan x$ terms cancel out, leaving what expression for $f'(x)$?",
                        "options": [r"$\tan x$", r"$x\sec^2 x$", r"$2\tan x$", r"$\sec^2 x$", r"$x\tan x$"],
                        "answer": 2,
                        "exp": r"$(x\tan x + \ln(\cos x))' = \tan x + x\sec^2 x - \tan x = x\sec^2 x$만 깔끔하게 남습니다!",
                        "exp_en": r"$\tan x$ and $-\tan x$ cancel out, leaving $f'(x) = x\sec^2 x$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [접점 조건] $f'(s) = \\dfrac{s}{t}$에서 $t$와 $s$의 관계식 찾기",
                "title_en": "🌿 Step 2 · [Tangency Condition] Relating $t$ and $s$ from $f'(s) = \\dfrac{s}{t}$",
                "knowledge": r"접점의 $x$좌표를 $s$ ($0 < s < \frac{\pi}{2}$)라 하면, 직선의 기울기 $\frac{s}{t}$가 미분계수 $f'(s) = s\sec^2 s = \frac{s}{\cos^2 s}$와 같아야 합니다! 따라서 $t = \cos^2 s$입니다.",
                "knowledge_en": r"Equating the line's slope $\frac{s}{t}$ to $f'(s) = \frac{s}{\cos^2 s}$ gives $t = \cos^2 s$.",
                "questions": [
                    {
                        "level_label": "접점 s 구하기 디딤돌 2",
                        "level_label_en": "Point of Tangency Step 2",
                        "stem": r"$t = \cos^2 s$에서 $t = \frac{1}{2}$일 때, $\cos s = \frac{\sqrt{2}}{2}$를 만족시키는 예각 $s$ ($0 < s < \frac{\pi}{2}$)의 값은?",
                        "stem_en": r"When $t = \cos^2 s = \frac{1}{2}$ with $0 < s < \frac{\pi}{2}$, what is $s$?",
                        "options": [r"$\frac{\pi}{6}$", r"$\frac{\pi}{4}$", r"$\frac{\pi}{3}$", r"$\frac{\pi}{2}$", r"$\frac{\pi}{8}$"],
                        "answer": 2,
                        "exp": r"$\cos\left(\frac{\pi}{4}\right) = \frac{\sqrt{2}}{2}$이므로 $s = \frac{\pi}{4}$입니다.",
                        "exp_en": r"$s = \frac{\pi}{4}$."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [변화율 계산] $t = \\cos^2 s$를 미분하여 $\\dfrac{dt}{ds}$ 구하기",
                "title_en": "🌱 Step 3 · [Rate of Change] Differentiating $t = \\cos^2 s$ to find $\\dfrac{dt}{ds}$",
                "knowledge": r"$t = \cos^2 s$의 양변을 $s$에 대하여 미분하면 $\frac{dt}{ds} = -2\cos s \sin s = -\sin(2s)$입니다.",
                "knowledge_en": r"Differentiating $t = \cos^2 s$ gives $\frac{dt}{ds} = -2\cos s\sin s = -\sin(2s)$.",
                "questions": [
                    {
                        "level_label": "미분계수 dt/ds 디딤돌 3",
                        "level_label_en": "Derivative dt/ds Step 3",
                        "stem": r"$s = \frac{\pi}{4}$일 때, $\frac{dt}{ds} = -\sin\left(2 \times \frac{\pi}{4}\right) = -\sin\left(\frac{\pi}{2}\right)$의 값은?",
                        "stem_en": r"At $s = \frac{\pi}{4}$, what is $\frac{dt}{ds} = -\sin\left(\frac{\pi}{2}\right)$?",
                        "options": [r"$-2$", r"$-1$", r"$0$", r"$1$", r"$2$"],
                        "answer": 2,
                        "exp": r"$-\sin\left(\frac{\pi}{2}\right) = -1$이므로 $\frac{ds}{dt} = -1$입니다.",
                        "exp_en": r"$\frac{dt}{ds} = -1$, so $\frac{ds}{dt} = -1$."
                    }
                ]
            },
            {
                "title": "🌳 4단계 · [$g(t)$ 미분식] $g(t) = f(s) - \\dfrac{s^2}{t}$를 $t$에 대하여 미분하기",
                "title_en": "🌳 Step 4 · [Differentiating $g(t)$] Differentiating $g(t) = f(s) - \\dfrac{s^2}{t}$ with respect to $t$",
                "knowledge": r"접점 $(s, f(s))$가 직선 $y = \frac{s}{t}x + g(t)$ 위에 있으므로 $g(t) = f(s) - \frac{s^2}{t}$입니다. 양변을 $t$에 대해 미분하면 $g'(t) = f'(s)\frac{ds}{dt} - \frac{2s}{t}\frac{ds}{dt} + \frac{s^2}{t^2} = -\frac{s}{t}\frac{ds}{dt} + \frac{s^2}{t^2}$입니다!",
                "knowledge_en": r"Since $g(t) = f(s) - \frac{s^2}{t}$ and $f'(s) = \frac{s}{t}$, differentiating gives $g'(t) = -\frac{s}{t}\frac{ds}{dt} + \frac{s^2}{t^2}$.",
                "questions": [
                    {
                        "level_label": "g'(1/2) 대입 디딤돌 4",
                        "level_label_en": "Evaluating g'(1/2) Step 4",
                        "stem": r"$t = \frac{1}{2}$, $s = \frac{\pi}{4}$, $\frac{ds}{dt} = -1$을 $-\frac{s}{t}\frac{ds}{dt}$에 대입한 값은?",
                        "stem_en": r"Substituting $t = \frac{1}{2}$, $s = \frac{\pi}{4}$, and $\frac{ds}{dt} = -1$ into $-\frac{s}{t}\frac{ds}{dt}$ gives what value?",
                        "options": [r"$\frac{\pi}{4}$", r"$\frac{\pi}{2}$", r"$\pi$", r"$-\frac{\pi}{2}$", r"$-\frac{\pi}{4}$"],
                        "answer": 2,
                        "exp": r"$-\frac{\pi/4}{1/2} \times (-1) = \frac{\pi}{2}$입니다.",
                        "exp_en": r"$-\frac{\pi/4}{1/2}(-1) = \frac{\pi}{2}$."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [최종 종합] $g'\\left(\\dfrac{1}{2}\\right) = \\dfrac{\\pi}{2} + \\dfrac{\\pi^2}{4}$ 통분하기",
                "title_en": "💎 Step 5 · [Final Synthesis] Combining $\\dfrac{\\pi}{2} + \\dfrac{\\pi^2}{4}$",
                "knowledge": r"뒷부분 $\frac{s^2}{t^2} = \frac{\pi^2/16}{1/4} = \frac{\pi^2}{4}$이므로 $\frac{\pi}{2} + \frac{\pi^2}{4} = \frac{\pi^2 + 2\pi}{4}$입니다.",
                "knowledge_en": r"Since $\frac{s^2}{t^2} = \frac{\pi^2}{4}$, we get $g'\left(\frac{1}{2}\right) = \frac{\pi}{2} + \frac{\pi^2}{4} = \frac{\pi^2 + 2\pi}{4}$.",
                "questions": [
                    {
                        "level_label": "최종 종합 디딤돌 5",
                        "level_label_en": "Final Synthesis Step 5",
                        "stem": r"$g'\left(\frac{1}{2}\right)$의 값은?",
                        "stem_en": r"What is the value of $g'\left(\frac{1}{2}\right)$?",
                        "options": [
                            r"$\frac{\pi^2 + \pi}{4}$",
                            r"$\frac{\pi^2 + 2\pi}{8}$",
                            r"$\frac{\pi^2 + 2\pi}{4}$",
                            r"$\frac{\pi^2 + 4\pi}{4}$",
                            r"$\frac{\pi^2 + 2\pi}{2}$"
                        ],
                        "answer": 3,
                        "exp": r"$g'\left(\frac{1}{2}\right) = \frac{\pi^2 + 2\pi}{4}$이므로 정답은 ③입니다.",
                        "exp_en": r"$\frac{\pi^2 + 2\pi}{4}$ (choice ③)."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"열린구간 $\left(0, \dfrac{\pi}{2}\right)$에서 정의된 함수 $f(x) = x\tan x + \ln(\cos x)$가 있다. $0 < t < 1$인 실수 $t$에 대하여 곡선 $y = f(x)$와 직선 $y = \dfrac{s}{t}x + g(t)$가 점 $(s, f(s))$에서 접할 때, $g'\left(\dfrac{1}{2}\right)$의 값은? [4점]",
            "stem_en": r"Consider $f(x) = x\tan x + \ln(\cos x)$ on $\left(0, \dfrac{\pi}{2}\right)$. For $0 < t < 1$, when the line $y = \dfrac{s}{t}x + g(t)$ is tangent to $y = f(x)$ at $(s, f(s))$, what is the value of $g'\left(\dfrac{1}{2}\right)$? [4 points]",
            "options": [
                r"$\dfrac{\pi^2 + \pi}{4}$",
                r"$\dfrac{\pi^2 + 2\pi}{8}$",
                r"$\dfrac{\pi^2 + 2\pi}{4}$",
                r"$\dfrac{\pi^2 + 4\pi}{4}$",
                r"$\dfrac{\pi^2 + 2\pi}{2}$"
            ],
            "answer": 3,
            "exp": r"$f'(s) = s\sec^2 s = \dfrac{s}{t}$에서 $t = \cos^2 s$이고, $g(t) = f(s) - \dfrac{s^2}{t}$를 미분하면 $g'(t) = -\dfrac{s}{t}\dfrac{ds}{dt} + \dfrac{s^2}{t^2}$입니다. $t = \dfrac{1}{2}$일 때 $s = \dfrac{\pi}{4}, \dfrac{ds}{dt} = -1$이므로 $g'\left(\dfrac{1}{2}\right) = \dfrac{\pi^2 + 2\pi}{4}$입니다.",
            "exp_en": r"From $f'(s) = s\sec^2 s = \dfrac{s}{t}$, we get $t = \cos^2 s$. Differentiating $g(t) = f(s) - \dfrac{s^2}{t}$ gives $g'(t) = -\dfrac{s}{t}\dfrac{ds}{dt} + \dfrac{s^2}{t^2}$. Evaluating at $t = \dfrac{1}{2}$ ($s = \dfrac{\pi}{4}, \dfrac{ds}{dt} = -1$) yields $\dfrac{\pi^2 + 2\pi}{4}$.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>접점의 좌표 $s$와 매개변수 $t$ 사이의 관계식을 도출하고 합성함수(음함수) 미분법</b>을 적용하는 미적분 4점 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 도함수 $f'(x)$와 $t = \cos^2 s$ 도출</b><br>
  $$f'(x) = \tan x + x\sec^2 x - \frac{\sin x}{\cos x} = x\sec^2 x$$
  점 $(s, f(s))$에서의 접선의 기울기가 $\frac{s}{t}$이므로:<br>
  $$s\sec^2 s = \frac{s}{t} \implies t = \cos^2 s$$<br>
  <b>2단계: $g(t)$의 도함수 구하기</b><br>
  접점이 직선 위에 있으므로 $g(t) = f(s) - \frac{s^2}{t}$입니다. 양변을 $t$에 대하여 미분하고 $f'(s) = \frac{s}{t}$를 대입하면:<br>
  $$g'(t) = f'(s)\frac{ds}{dt} - \frac{2s}{t}\frac{ds}{dt} + \frac{s^2}{t^2} = -\frac{s}{t}\frac{ds}{dt} + \frac{s^2}{t^2}$$<br>
  <b>3단계: $t = \frac{1}{2}$에서의 미분계수 계산</b><br>
  $t = \cos^2 s = \frac{1}{2}$ ($0 < s < \frac{\pi}{2}$)에서 $s = \frac{\pi}{4}$이고, $\frac{dt}{ds} = -\sin(2s) = -1 \implies \frac{ds}{dt} = -1$입니다.<br>
  $$g'\left(\frac{1}{2}\right) = -\frac{\pi/4}{1/2}(-1) + \frac{\pi^2/16}{1/4} = \frac{\pi}{2} + \frac{\pi^2}{4} = \frac{\pi^2 + 2\pi}{4}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 $g'\left(\dfrac{1}{2}\right) = \dfrac{\pi^2 + 2\pi}{4}$이므로 정답은 <b>③번</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem applies <b>implicit and parametric differentiation</b> to the $y$-intercept $g(t)$ of a tangent line.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Relate $t$ and $s$</b><br>
  $$f'(s) = s\sec^2 s = \frac{s}{t} \implies t = \cos^2 s$$<br>
  <b>Step 2: Differentiate $g(t) = f(s) - \frac{s^2}{t}$</b><br>
  $$g'(t) = \left(f'(s) - \frac{2s}{t}\right)\frac{ds}{dt} + \frac{s^2}{t^2} = -\frac{s}{t}\frac{ds}{dt} + \frac{s^2}{t^2}$$
  At $t = \frac{1}{2}$, $s = \frac{\pi}{4}$ and $\frac{dt}{ds} = -\sin\left(\frac{\pi}{2}\right) = -1$, giving $g'\left(\frac{1}{2}\right) = \frac{\pi}{2} + \frac{\pi^2}{4} = \frac{\pi^2 + 2\pi}{4}$.
</p>

<h4>✨ [Final Answer & Practical Tips]</h4>
<p>
  The correct answer is <b>choice ③ ($\dfrac{\pi^2 + 2\pi}{4}$)</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 미적 29번: c2610m29 (단답형)
    # -------------------------------------------------------------------------
    {
        "slug": "c2610m29",
        "qNum": "미적 29",
        "subject": "미적분",
        "title": "[2026학년도 10월 고3 미적 29번] 등차수열과 등비수열의 결합 및 등비급수의 합",
        "title_en": "[2026 AY Oct Exam Grade 12 Calculus #29] Arithmetic and Geometric Sequences and Infinite Geometric Series",
        "summary_ko": "b_1=72, r=-1/2을 구하고 b_3=18=a_k, b_4=-9=a_{k+27}에서 공차 d=-1, k=5를 도출해 급수의 합 144/11 구하기",
        "summary_en": "Find b_1=72 and r=-1/2, use b_3=18=a_k and b_4=-9=a_{k+27} to get d=-1 and k=5, and evaluate the infinite series to 144/11 (p+q=155).",
        "tags": ["미적분", "수열의극한", "등비급수", "등차수열", "등비수열", "단답형", "29번"],
        "symbols": [
            {"sym": r"$\sum_{n=k}^{\infty} b_n = \dfrac{b_k}{1 - r} = a_{k+15}$", "desc": "k번째 항부터 시작하는 등비급수의 합 공식", "desc_en": "Sum of the geometric series starting from the k-th term."},
            {"sym": r"$S = \dfrac{a}{1 - R}$", "desc": "첫째항이 a이고 공비가 R (-1 < R < 1)인 무한등비급수의 합", "desc_en": "Infinite geometric series sum formula."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 등간격 건너뛰기] $27$칸 건너뛰었을 때 $18$에서 $-9$로 줄어드는 한 칸 간격(공차) 구하기",
                "title_en": "🔰 Step 1 · [Elementary Equal Steps] Finding the step size from $18$ to $-9$ over $27$ steps",
                "knowledge": r"등비수열 $b_n$에서 첫째항 $b_1 = 72$, 공비 $r = -\frac{1}{2}$이면 $b_3 = 18$, $b_4 = -9$입니다. 문제에서 $a_k = b_3 = 18$이고 $a_{k+27} = b_4 = -9$이므로, 초등학교 수직선에서 $27$칸을 가는 동안 $18$에서 $-9$로 총 $27$만큼 줄어든 셈입니다!",
                "knowledge_en": r"With $b_1 = 72$ and $r = -\frac{1}{2}$, we have $b_3 = 18 = a_k$ and $b_4 = -9 = a_{k+27}$. Moving $27$ steps changes the value by $-9 - 18 = -27$.",
                "questions": [
                    {
                        "level_label": "초등 나눗셈 디딤돌 1",
                        "level_label_en": "Elementary Division Step 1",
                        "stem": r"초등학교 나눗셈 원리로 $27$칸 동안 $-27$만큼 변하는 등차수열 $\{a_n\}$의 한 칸 변화량(공차 $d = \frac{-27}{27}$)은?",
                        "stem_en": r"Using elementary division, what is the common difference $d = \frac{-27}{27}$ of the arithmetic sequence $\{a_n\}$?",
                        "options": [r"$-3$", r"$-2$", r"$-1$", r"$1$", r"$2$"],
                        "answer": 3,
                        "exp": r"$27d = -9 - 18 = -27$이므로 공차 $d = -1$입니다.",
                        "exp_en": r"$d = \frac{-27}{27} = -1$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [등차수열 함숫값] $a_{k+15}$의 값 구하기",
                "title_en": "🌿 Step 2 · [Arithmetic Term] Finding $a_{k+15}$",
                "knowledge": r"$a_k = 18$이고 공차 $d = -1$이므로, $15$칸 뒤의 항 $a_{k+15} = a_k + 15d = 18 - 15 = 3$입니다.",
                "knowledge_en": r"Since $a_k = 18$ and $d = -1$, we have $a_{k+15} = 18 + 15(-1) = 3$.",
                "questions": [
                    {
                        "level_label": "등차수열 항 디딤돌 2",
                        "level_label_en": "Arithmetic Term Step 2",
                        "stem": r"$a_k = 18$, $d = -1$일 때, $a_{k+15} = 18 + 15 \times (-1)$의 값은?",
                        "stem_en": r"Given $a_k = 18$ and $d = -1$, what is $a_{k+15} = 18 - 15$?",
                        "options": [r"$1$", r"$2$", r"$3$", r"$4$", r"$5$"],
                        "answer": 3,
                        "exp": r"$18 - 15 = 3$입니다.",
                        "exp_en": r"$18 - 15 = 3$."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [자연수 $k$ 확인] $\\sum_{n=k}^{\\infty} b_n = 3$을 만족하는 $k$ 찾기",
                "title_en": "🌱 Step 3 · [Finding $k$] Solving $\\sum_{n=k}^{\\infty} b_n = 3$ for $k$",
                "knowledge": r"$\sum_{n=k}^{\infty} b_n = \frac{b_k}{1 - (-1/2)} = \frac{2}{3}b_k = 3$에서 $b_k = \frac{9}{2}$입니다. $b_1 = 72, b_2 = -36, b_3 = 18, b_4 = -9, b_5 = \frac{9}{2}$이므로 $k = 5$입니다.",
                "knowledge_en": r"From $\frac{b_k}{1 - (-1/2)} = 3$, we get $b_k = \frac{9}{2}$. Since $b_n = 72(-1/2)^{n-1}$, $b_5 = \frac{9}{2} \implies k = 5$.",
                "questions": [
                    {
                        "level_label": "자연수 k 디딤돌 3",
                        "level_label_en": "Finding k Step 3",
                        "stem": r"$b_n = 72\left(-\frac{1}{2}\right)^{n-1}$에서 $b_k = \frac{9}{2}$이 되도록 하는 자연수 $k$는?",
                        "stem_en": r"For $b_n = 72\left(-\frac{1}{2}\right)^{n-1}$, which natural number $k$ gives $b_k = \frac{9}{2}$?",
                        "options": [r"$3$", r"$4$", r"$5$", r"$6$", r"$7$"],
                        "answer": 3,
                        "exp": r"$72 \times \left(-\frac{1}{2}\right)^4 = \frac{72}{16} = \frac{9}{2}$이므로 $k = 5$입니다.",
                        "exp_en": r"$k = 5$."
                    }
                ]
            },
            {
                "title": "🌳 4단계 · [등비급수의 합] $\\sum_{n=1}^{\\infty} \\dfrac{b_n}{k^n} = \\sum_{n=1}^{\\infty} \\dfrac{b_n}{5^n}$ 구하기",
                "title_en": "🌳 Step 4 · [Infinite Series] Evaluating $\\sum_{n=1}^{\\infty} \\dfrac{b_n}{5^n}$",
                "knowledge": r"수열 $\frac{b_n}{5^n}$은 첫째항이 $\frac{b_1}{5} = \frac{72}{5}$이고 공비가 $R = \frac{-1/2}{5} = -\frac{1}{10}$인 등비수열입니다. 따라서 급수의 합은 $\frac{72/5}{1 - (-1/10)} = \frac{72/5}{11/10} = \frac{144}{11}$입니다.",
                "knowledge_en": r"The series $\sum_{n=1}^\infty \frac{b_n}{5^n}$ has first term $\frac{72}{5}$ and ratio $-\frac{1}{10}$, so its sum is $\frac{72/5}{11/10} = \frac{144}{11}$.",
                "questions": [
                    {
                        "level_label": "등비급수 계산 디딤돌 4",
                        "level_label_en": "Geometric Series Step 4",
                        "stem": r"$\frac{72/5}{1 + 1/10} = \frac{72/5}{11/10}$을 계산한 기약분수 $\frac{q}{p}$는?",
                        "stem_en": r"What is $\frac{72/5}{11/10}$ in lowest terms $\frac{q}{p}$?",
                        "options": [r"$\frac{72}{11}$", r"$\frac{144}{11}$", r"$\frac{72}{9}$", r"$\frac{144}{9}$", r"$\frac{120}{11}$"],
                        "answer": 2,
                        "exp": r"분모·분자에 $10$을 곱하면 $\frac{144}{11}$입니다.",
                        "exp_en": r"$\frac{144}{11}$."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [최종 종합] 서로소인 자연수 $p + q$ 구하기",
                "title_en": "💎 Step 5 · [Final Synthesis] Computing $p + q$",
                "knowledge": r"$\frac{q}{p} = \frac{144}{11}$에서 $p = 11, q = 144$이므로 $p + q = 155$입니다.",
                "knowledge_en": r"With $p = 11$ and $q = 144$, $p + q = 155$.",
                "questions": [
                    {
                        "level_label": "최종 종합 디딤돌 5",
                        "level_label_en": "Final Synthesis Step 5",
                        "stem": r"$p = 11$, $q = 144$일 때, $p + q$의 값은?",
                        "stem_en": r"Given $p = 11$ and $q = 144$, what is $p + q$?",
                        "options": [r"$145$", r"$150$", r"$155$", r"$160$", r"$165$"],
                        "answer": 3,
                        "exp": r"$11 + 144 = 155$입니다.",
                        "exp_en": r"$11 + 144 = 155$."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"등차수열 $\{a_n\}$과 등비수열 $\{b_n\}$이 조건을 만족시킬 때, $\sum_{n=1}^{\infty} \dfrac{b_n}{k^n} = \dfrac{q}{p}$이다. $p + q$의 값을 구하시오. (단, $k$는 자연수이고, $p$와 $q$는 서로소인 자연수이다.) [4점]",
            "stem_en": r"An arithmetic sequence $\{a_n\}$ and a geometric sequence $\{b_n\}$ satisfy the given conditions. If $\sum_{n=1}^{\infty} \dfrac{b_n}{k^n} = \dfrac{q}{p}$ in lowest terms, find $p + q$. [4 points]",
            "options": [r"$145$", r"$150$", r"$155$", r"$160$", r"$165$"],
            "answer": 3,
            "exp": r"$b_1 = 72$, 공비 $r = -\dfrac{1}{2}$이고, $b_3 = 18 = a_k$, $b_4 = -9 = a_{k+27}$에서 등차수열의 공차 $d = -1$, $k = 5$입니다. 따라서 $\sum_{n=1}^{\infty} \dfrac{b_n}{5^n} = \dfrac{72/5}{1 - (-1/10)} = \dfrac{144}{11}$이므로 $p + q = 155$입니다.",
            "exp_en": r"Finding $b_1 = 72$, $r = -\dfrac{1}{2}$, $d = -1$, and $k = 5$ yields $\sum_{n=1}^{\infty} \dfrac{b_n}{5^n} = \dfrac{72/5}{1 + 1/10} = \dfrac{144}{11}$, so $p + q = 155$.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>등비급수의 수렴 조건과 합 공식</b>을 등차수열·등비수열의 일반항과 결합하여 미지수를 추론하는 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 등비수열 $\{b_n\}$과 등차수열 $\{a_n\}$의 관계 파악</b><br>
  조건으로부터 등비수열 $\{b_n\}$의 첫째항 $b_1 = 72$, 공비 $r = -\frac{1}{2}$을 얻으면 $b_3 = 18$, $b_4 = -9$입니다.<br>
  $a_k = b_3 = 18$, $a_{k+27} = b_4 = -9$에서 등차수열 $\{a_n\}$의 공차 $d$는:<br>
  $$27d = -9 - 18 = -27 \implies d = -1$$<br>
  <b>2단계: 자연수 $k$ 결정</b><br>
  $$a_{k+15} = a_k + 15d = 18 - 15 = 3$$
  $$\sum_{n=k}^{\infty} b_n = \frac{b_k}{1 - (-1/2)} = \frac{2}{3}b_k = 3 \implies b_k = \frac{9}{2}$$
  $b_k = 72\left(-\frac{1}{2}\right)^{k-1} = \frac{9}{2}$에서 $\left(-\frac{1}{2}\right)^{k-1} = \frac{1}{16}$이므로 $k = 5$입니다.<br><br>
  <b>3단계: 구하는 등비급수의 합 계산</b><br>
  $$\sum_{n=1}^{\infty} \frac{b_n}{5^n} = \frac{72/5}{1 - (-1/10)} = \frac{72/5}{11/10} = \frac{144}{11}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 $p = 11, q = 144$이므로 $p + q =$ <b>$155$</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem combines <b>arithmetic and geometric sequences</b> with the <b>sum of an infinite geometric series</b>.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Determine parameters</b><br>
  With $b_1 = 72$ and $r = -\frac{1}{2}$, we have $a_k = b_3 = 18$ and $a_{k+27} = b_4 = -9 \implies d = -1$.<br>
  Then $a_{k+15} = 3 = \frac{b_k}{3/2} \implies b_k = \frac{9}{2} \implies k = 5$.<br><br>
  <b>Step 2: Sum the infinite series</b><br>
  $$\sum_{n=1}^{\infty} \frac{b_n}{5^n} = \frac{72/5}{1 - (-1/10)} = \frac{144}{11}$$
</p>

<h4>✨ [Final Answer & Practical Tips]</h4>
<p>
  Thus $p + q = 11 + 144 =$ <b>$155$</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 미적 30번: c2610m30 (단답형 킬러)
    # -------------------------------------------------------------------------
    {
        "slug": "c2610m30",
        "qNum": "미적 30",
        "subject": "미적분",
        "title": "[2026학년도 10월 고3 미적 30번] 삼각함수의 치환적분과 절댓값 정적분(총변화량)",
        "title_en": "[2026 AY Oct Exam Grade 12 Calculus #30] Trigonometric Substitution and Total Variation Integral",
        "summary_ko": "두 번째 치환적분에서 b+1=1/a를 구하고 첫 번째 절댓값 정적분(총변화량)에서 sin(2pi*a)=1/2, a=5/12를 도출하여 f(2pi)=19/10 구하기",
        "summary_en": "Use u-substitution on the second integral to find b+1=1/a, and analyze the total variation of (1-sin(ax))^2 on [0, 2pi] to find a=5/12 and f(2pi)=19/10 (p+q=29).",
        "tags": ["미적분", "적분법", "치환적분법", "절댓값정적분", "삼각함수", "단답형", "30번"],
        "symbols": [
            {"sym": r"$u = \sin x \implies du = \cos x\,dx$", "desc": "두 번째 적분에서 sin x를 u로 바꾸는 치환적분", "desc_en": "Substitution u = sin x in the second integral."},
            {"sym": r"$H(x) = \{1 - \sin(ax)\}^2$", "desc": "미분하면 H'(x) = -2a cos(ax){1 - sin(ax)}가 되는 원시함수", "desc_en": "Antiderivative whose derivative matches the first integrand up to -2a."},
            {"sym": r"$\int_0^{2\pi} |H'(x)|dx = \dfrac{5}{2}a$", "desc": "구간 [0, 2pi]에서 H(x)가 움직인 총 변화량", "desc_en": "Total variation of H(x) over [0, 2pi]."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 분수 덧셈] $1 + \\{1 - \\sin(2\\pi a)\\}^2 = \\dfrac{5}{4}$에서 제곱값 구하기",
                "title_en": "🔰 Step 1 · [Elementary Fraction Subtraction] Solving $1 + \\{1 - \\sin(2\\pi a)\\}^2 = \\dfrac{5}{4}$",
                "knowledge": r"함수 $H(x) = \{1 - \sin(ax)\}^2$은 $x = 0$에서 $H(0) = 1$로 출발하여 최솟값 $0$까지 내려갔다가($1$만큼 이동), 다시 $x = 2\pi$에서의 값 $H(2\pi) = \{1 - \sin(2\pi a)\}^2$까지 올라갑니다. 총 이동 거리가 $\frac{5}{4}$이므로 초등학교 분수 뺄셈 $1 + \{1 - \sin(2\pi a)\}^2 = \frac{5}{4}$이 성립합니다!",
                "knowledge_en": r"By elementary fraction subtraction, $H(x) = \{1 - \sin(ax)\}^2$ decreases from $H(0)=1$ to $0$ (distance $1$) and rises to $H(2\pi) = \{1 - \sin(2\pi a)\}^2$. Total distance $\frac{5}{4}$ gives $1 + \{1 - \sin(2\pi a)\}^2 = \frac{5}{4}$.",
                "questions": [
                    {
                        "level_label": "초등 분수 뺄셈 디딤돌 1",
                        "level_label_en": "Elementary Fraction Step 1",
                        "stem": r"초등학교 분수 뺄셈 원리로 $1 + \{1 - \sin(2\pi a)\}^2 = \frac{5}{4}$에서 $\{1 - \sin(2\pi a)\}^2 = \frac{5}{4} - 1$의 값을 구하면?",
                        "stem_en": r"Using elementary fraction subtraction, what is $\{1 - \sin(2\pi a)\}^2 = \frac{5}{4} - 1$?",
                        "options": [r"$\frac{1}{8}$", r"$\frac{1}{4}$", r"$\frac{1}{2}$", r"$\frac{3}{4}$", r"$1$"],
                        "answer": 2,
                        "exp": r"$\frac{5}{4} - 1 = \frac{1}{4}$이므로 $1 - \sin(2\pi a) = \frac{1}{2} \implies \sin(2\pi a) = \frac{1}{2}$입니다!",
                        "exp_en": r"$\frac{5}{4} - 1 = \frac{1}{4} \implies \sin(2\pi a) = \frac{1}{2}$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [치환적분] 두 번째 적분식에서 $b + 1 = \\dfrac{1}{a}$ 이끌어내기",
                "title_en": "🌿 Step 2 · [u-Substitution] Deriving $b + 1 = \\dfrac{1}{a}$ from the second integral",
                "knowledge": r"$u = \sin x$로 치환하면 $\int_0^{\pi/2} \cos x f(\sin x)dx = \int_0^1 f(u)du = \int_0^1 (\sin(au) + b + 1)du = \frac{1 - \cos a}{a} + b + 1$입니다. 이 값이 $\frac{2 - \cos a}{a}$와 같으므로 $b + 1 = \frac{1}{a}$입니다!",
                "knowledge_en": r"Substituting $u = \sin x$ gives $\int_0^1 f(u)du = \frac{1 - \cos a}{a} + b + 1 = \frac{2 - \cos a}{a}$, which simplifies to $b + 1 = \frac{1}{a}$.",
                "questions": [
                    {
                        "level_label": "b+1 관계식 디딤돌 2",
                        "level_label_en": "Relation for b+1 Step 2",
                        "stem": r"$\frac{1 - \cos a}{a} + b + 1 = \frac{2 - \cos a}{a}$의 양변에서 $\frac{1 - \cos a}{a}$를 빼면 $b + 1$을 $a$로 나타낸 식은?",
                        "stem_en": r"Subtracting $\frac{1 - \cos a}{a}$ from both sides gives what expression for $b + 1$?",
                        "options": [r"$a$", r"$2a$", r"$\frac{1}{a}$", r"$\frac{2}{a}$", r"$-\frac{1}{a}$"],
                        "answer": 3,
                        "exp": r"$b + 1 = \frac{2 - \cos a}{a} - \frac{1 - \cos a}{a} = \frac{1}{a}$입니다.",
                        "exp_en": r"$b + 1 = \frac{1}{a}$."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [상수 $a$ 결정] $\\sin(2\\pi a) = \\dfrac{1}{2}$과 범위 조건으로 $a$ 구하기",
                "title_en": "🌱 Step 3 · [Determining $a$] Finding $a$ from $\\sin(2\\pi a) = \\dfrac{1}{2}$",
                "knowledge": r"$x = 2\pi$가 첫 번째 극소점($ax = \frac{\pi}{2}$)을 지나고 다음 극점($ax = \frac{3\pi}{2}$) 이전이어야 총 이동거리가 $1 + \{1 - \sin(2\pi a)\}^2$이 됩니다. 즉 $\frac{\pi}{2} < 2\pi a < \frac{3\pi}{2}$에서 $\sin(2\pi a) = \frac{1}{2}$을 만족하는 각은 $2\pi a = \frac{5\pi}{6}$입니다.",
                "knowledge_en": r"For $2\pi a \in \left(\frac{\pi}{2}, \frac{3\pi}{2}\right)$, $\sin(2\pi a) = \frac{1}{2}$ yields $2\pi a = \frac{5\pi}{6}$.",
                "questions": [
                    {
                        "level_label": "상수 a 구하기 디딤돌 3",
                        "level_label_en": "Finding a Step 3",
                        "stem": r"$2\pi a = \frac{5\pi}{6}$일 때, 양수 $a$의 값은?",
                        "stem_en": r"From $2\pi a = \frac{5\pi}{6}$, what is $a$?",
                        "options": [r"$\frac{1}{6}$", r"$\frac{1}{4}$", r"$\frac{5}{12}$", r"$\frac{7}{12}$", r"$\frac{5}{6}$"],
                        "answer": 3,
                        "exp": r"양변을 $2\pi$로 나누면 $a = \frac{5}{12}$입니다.",
                        "exp_en": r"$a = \frac{5}{12}$."
                    }
                ]
            },
            {
                "title": "🌳 4단계 · [$f(2\\pi)$ 계산] $f(2\\pi) = -\\sin(2\\pi a) + b + 1$ 구하기",
                "title_en": "🌳 Step 4 · [Evaluating $f(2\\pi)$] Computing $f(2\\pi) = -\\sin(2\\pi a) + b + 1$",
                "knowledge": r"$a = \frac{5}{12}$이므로 $b + 1 = \frac{1}{a} = \frac{12}{5}$이고, $\sin(2\pi a) = \frac{1}{2}$이므로 $f(2\pi) = -\frac{1}{2} + \frac{12}{5}$입니다.",
                "knowledge_en": r"With $b + 1 = \frac{1}{a} = \frac{12}{5}$ and $\sin(2\pi a) = \frac{1}{2}$, we get $f(2\pi) = -\frac{1}{2} + \frac{12}{5}$.",
                "questions": [
                    {
                        "level_label": "분수 통분 디딤돌 4",
                        "level_label_en": "Fraction Addition Step 4",
                        "stem": r"$f(2\pi) = -\frac{1}{2} + \frac{12}{5}$를 분모 $10$으로 통분하여 계산한 기약분수 $\frac{q}{p}$는?",
                        "stem_en": r"What is $-\frac{1}{2} + \frac{12}{5}$ in lowest terms $\frac{q}{p}$?",
                        "options": [r"$\frac{17}{10}$", r"$\frac{19}{10}$", r"$\frac{21}{10}$", r"$\frac{23}{10}$", r"$\frac{29}{10}$"],
                        "answer": 2,
                        "exp": r"$\frac{-5 + 24}{10} = \frac{19}{10}$입니다.",
                        "exp_en": r"$\frac{-5 + 24}{10} = \frac{19}{10}$."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [최종 종합] 서로소인 자연수 $p + q$ 구하기",
                "title_en": "💎 Step 5 · [Final Synthesis] Computing $p + q$",
                "knowledge": r"$\frac{q}{p} = \frac{19}{10}$에서 $p = 10, q = 19$이므로 $p + q = 29$입니다.",
                "knowledge_en": r"With $p = 10$ and $q = 19$, $p + q = 29$.",
                "questions": [
                    {
                        "level_label": "최종 종합 디딤돌 5",
                        "level_label_en": "Final Synthesis Step 5",
                        "stem": r"$p = 10$, $q = 19$일 때, $p + q$의 값은?",
                        "stem_en": r"Given $p = 10$ and $q = 19$, what is $p + q$?",
                        "options": [r"$25$", r"$27$", r"$29$", r"$31$", r"$33$"],
                        "answer": 3,
                        "exp": r"$10 + 19 = 29$입니다.",
                        "exp_en": r"$10 + 19 = 29$."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"두 상수 $a, b$ ($0 < a < 1$)와 함수 $f(x)$가 두 정적분 조건을 만족시킬 때, $f(2\pi) = \dfrac{q}{p}$이다. $p + q$의 값을 구하시오. (단, $p$와 $q$는 서로소인 자연수이다.) [4점]",
            "stem_en": r"For constants $a, b$ ($0 < a < 1$), the trigonometric function $f(x)$ satisfies the two given integral conditions. If $f(2\pi) = \dfrac{q}{p}$ in lowest terms, find $p + q$. [4 points]",
            "options": [r"$25$", r"$27$", r"$29$", r"$31$", r"$33$"],
            "answer": 3,
            "exp": r"두 번째 조건에서 $b + 1 = \dfrac{1}{a}$를 얻고, 첫 번째 절댓값 적분에서 $1 + \{1 - \sin(2\pi a)\}^2 = \dfrac{5}{4} \implies \sin(2\pi a) = \dfrac{1}{2}$ ($2\pi a = \dfrac{5\pi}{6}$)이므로 $a = \dfrac{5}{12}$입니다. 따라서 $f(2\pi) = -\dfrac{1}{2} + \dfrac{12}{5} = \dfrac{19}{10}$이고 $p + q = 29$입니다.",
            "exp_en": r"The second integral yields $b + 1 = \dfrac{1}{a}$, and the first total variation integral gives $1 + \{1 - \sin(2\pi a)\}^2 = \dfrac{5}{4} \implies 2\pi a = \dfrac{5\pi}{6} \implies a = \dfrac{5}{12}$. Thus $f(2\pi) = -\dfrac{1}{2} + \dfrac{12}{5} = \dfrac{19}{10}$ and $p + q = 29$.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 미적분 최고난도(30번) 문항으로, <b>치환적분법</b>과 <b>절댓값이 포함된 삼각함수의 정적분(원시함수의 총변화량)</b>을 결합하여 상수 $a, b$를 결정하는 문제입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 두 번째 정적분 조건 해석 ($u = \sin x$ 치환)</b><br>
  두 번째 적분에서 $u = \sin x$로 치환하면 $\cos x\,dx = du$이고 적분 구간은 $[0, 1]$이 됩니다.<br>
  정적분을 계산하여 우변과 비교하면:<br>
  $$b + 1 = \frac{1}{a}$$<br>
  <b>2단계: 첫 번째 절댓값 정적분 조건 해석</b><br>
  $H(x) = \{1 - \sin(ax)\}^2$이라 하면 $H'(x) = -2a\cos(ax)\{1 - \sin(ax)\}$입니다.<br>
  따라서 첫 번째 조건은 $\int_0^{2\pi} \left|-\frac{1}{2a}H'(x)\right|dx$ 형태가 되어, 구간 $[0, 2\pi]$에서 $H(x)$의 총변화량이 $\frac{5}{4}$임을 뜻합니다.<br>
  $H(0) = 1$에서 출발하여 $ax = \frac{\pi}{2}$에서 최솟값 $0$을 찍고 다시 $H(2\pi) = \{1 - \sin(2\pi a)\}^2$으로 증가하므로 ($\frac{\pi}{2} < 2\pi a < \frac{3\pi}{2}$):<br>
  $$(1 - 0) + \{1 - \sin(2\pi a)\}^2 = \frac{5}{4} \implies \{1 - \sin(2\pi a)\}^2 = \frac{1}{4} \implies \sin(2\pi a) = \frac{1}{2}$$
  $\frac{\pi}{2} < 2\pi a < \frac{3\pi}{2}$이므로 $2\pi a = \frac{5\pi}{6} \implies a = \frac{5}{12}$입니다.<br><br>
  <b>3단계: $f(2\pi)$의 값 도출</b><br>
  $$f(2\pi) = -\sin\left(\frac{5\pi}{6}\right) + \frac{1}{a} = -\frac{1}{2} + \frac{12}{5} = \frac{19}{10}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 $p = 10, q = 19$이므로 $p + q =$ <b>$29$</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem combines <b>trigonometric substitution</b> with <b>total variation integration of $H(x) = \{1 - \sin(ax)\}^2$</b>.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Second integral via $u = \sin x$</b><br>
  Evaluating $\int_0^1 f(u)du$ yields $b + 1 = \frac{1}{a}$.<br><br>
  <b>Step 2: First integral via total variation</b><br>
  With $H(x) = \{1 - \sin(ax)\}^2$, the total variation on $[0, 2\pi]$ is $1 + \{1 - \sin(2\pi a)\}^2 = \frac{5}{4}$, giving $\sin(2\pi a) = \frac{1}{2}$ for $2\pi a \in \left(\frac{\pi}{2}, \frac{3\pi}{2}\right)$. Thus $2\pi a = \frac{5\pi}{6} \implies a = \frac{5}{12}$.<br><br>
  <b>Step 3: Compute $f(2\pi)$</b><br>
  $$f(2\pi) = -\frac{1}{2} + \frac{12}{5} = \frac{19}{10}$$
</p>

<h4>✨ [Final Answer & Practical Tips]</h4>
<p>
  Therefore, $p + q = 10 + 19 =$ <b>$29$</b>.
</p>"""
        }
    }
]
