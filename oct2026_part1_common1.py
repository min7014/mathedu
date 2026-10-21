# -*- coding: utf-8 -*-
"""
oct2026_part1_common1.py
2026학년도 10월 고3 전국연합학력평가 (2027대비) 수학 공통 1번 ~ 11번
초등학생 눈높이 무장벽 디딤돌 6단계 퀴즈 및 상세 풀이 데이터
"""

PART1_PROBLEMS = [
    # -------------------------------------------------------------------------
    # 1번: c261001
    # -------------------------------------------------------------------------
    {
        "slug": "c261001",
        "qNum": "1",
        "subject": "공통(수학I·II)",
        "title": "[2026학년도 10월 고3 1번] 거듭제곱근과 유리수 지수법칙 계산",
        "title_en": "[2026 AY Oct Exam Grade 12 #1] Radicals and Rational Exponent Rules",
        "summary_ko": "세제곱근을 분수 지수로 바꾸고 밑을 2로 통일하여 지수법칙으로 값을 구하기",
        "summary_en": "Convert cube roots into fractional exponents and unify the base to 2 using exponent rules.",
        "tags": ["공통(수학I·II)", "수학I", "지수", "거듭제곱근", "지수법칙", "1번"],
        "symbols": [
            {"sym": r"$\sqrt[3]{a} = a^{\frac{1}{3}}$", "desc": "세 번 곱해 a가 되는 수 (지수를 1/3로 표현)", "desc_en": "Cube root of a, expressed with fractional exponent 1/3."},
            {"sym": r"$4 = 2^2$", "desc": "4는 2를 두 번 곱한 수 (밑을 2로 통일)", "desc_en": "Express composite number 4 as 2 squared."},
            {"sym": r"$(a^m)^n = a^{m \times n}$", "desc": "거듭제곱의 거듭제곱은 지수끼리 곱하기", "desc_en": "Power of a power rule: multiply the exponents."},
            {"sym": r"$a^{-1} = \dfrac{1}{a}$", "desc": "지수가 -1이면 분모로 내려가는 역수 약속", "desc_en": "Negative exponent -1 represents the reciprocal 1/a."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 구구단 연계] 4는 2를 몇 번 곱한 수일까?",
                "title_en": "🔰 Step 1 · [Elementary Multiplication Link] Expressing 4 as a power of 2",
                "knowledge": r"초등학교 구구단에서 $2 \times 2 = 4$입니다. 수학에서는 같은 수를 여러 번 곱할 때 오른쪽 위에 작게 횟수를 적어 $2^2 = 4$라고 약속합니다.",
                "knowledge_en": r"In elementary multiplication, $2 \times 2 = 4$. Writing the repeat count as a small superscript gives $2^2 = 4$.",
                "questions": [
                    {
                        "level_label": "초등 구구단 디딤돌 1",
                        "level_label_en": "Elementary Multiplication Step 1",
                        "stem": r"초등학교 구구단에서 $2 \times 2 = 4$입니다. $4$를 $2$의 거듭제곱 $2^k$으로 나타낼 때, 지수 $k$에 알맞은 수는?",
                        "stem_en": r"Since $2 \times 2 = 4$ in elementary multiplication, what is the exponent $k$ when writing $4 = 2^k$?",
                        "options": [r"$1$", r"$2$", r"$3$", r"$4$", r"$5$"],
                        "answer": 2,
                        "exp": r"$2$를 $2$번 곱하면 $4$가 되므로 $4 = 2^2$, 따라서 $k = 2$입니다.",
                        "exp_en": r"Multiplying $2$ twice gives $4 = 2^2$, so $k = 2$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [기호 번역] 세제곱근 기호 $\\sqrt[3]{2}$를 분수 지수로 바꾸기",
                "title_en": "🌿 Step 2 · [Symbol Translation] Rewriting $\\sqrt[3]{2}$ as a fractional exponent",
                "knowledge": r"똑같은 수를 $3$번 곱해서 $2$가 되는 수를 $\sqrt[3]{2}$라고 쓰고, 지수로는 '3번 중의 1번'이라는 뜻으로 $2^{\frac{1}{3}}$이라고 바꿀 수 있습니다.",
                "knowledge_en": r"The number that gives $2$ when multiplied $3$ times is written $\sqrt[3]{2}$, which equals $2^{\frac{1}{3}}$ in exponent form.",
                "questions": [
                    {
                        "level_label": "기호 번역 디딤돌 2",
                        "level_label_en": "Symbol Translation Step 2",
                        "stem": r"거듭제곱근 약속 $\sqrt[n]{a} = a^{\frac{1}{n}}$에 따라 $\sqrt[3]{2}$를 밑이 $2$인 거듭제곱으로 바르게 나타낸 것은?",
                        "stem_en": r"Using $\sqrt[n]{a} = a^{\frac{1}{n}}$, how is $\sqrt[3]{2}$ written as a power of $2$?",
                        "options": [r"$2^3$", r"$2^{\frac{1}{2}}$", r"$2^{\frac{1}{3}}$", r"$2^{-\frac{1}{3}}$", r"$2^{\frac{2}{3}}$"],
                        "answer": 3,
                        "exp": r"근호 왼쪽 위의 작은 숫자 $3$이 지수의 분모로 들어가므로 $\sqrt[3]{2} = 2^{\frac{1}{3}}$입니다.",
                        "exp_en": r"The index $3$ becomes the denominator of the exponent: $\sqrt[3]{2} = 2^{\frac{1}{3}}$."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [분수 곱셈] 거듭제곱의 지수끼리 곱하기",
                "title_en": "🌱 Step 3 · [Fraction Multiplication] Multiplying exponents in $(2^2)^{-\\frac{2}{3}}$",
                "knowledge": r"$4^{-\frac{2}{3}}$에서 $4$ 대신 $2^2$을 넣으면 $(2^2)^{-\frac{2}{3}}$이 됩니다. 괄호 안과 밖의 지수는 서로 곱합니다: $2 \times \left(-\frac{2}{3}\right) = -\frac{4}{3}$.",
                "knowledge_en": r"Replacing $4$ with $2^2$ gives $(2^2)^{-\frac{2}{3}}$. Multiply the inner and outer exponents: $2 \times \left(-\frac{2}{3}\right) = -\frac{4}{3}$.",
                "questions": [
                    {
                        "level_label": "분수 곱셈 디딤돌 3",
                        "level_label_en": "Fraction Multiplication Step 3",
                        "stem": r"지수법칙 $(a^m)^n = a^{m \times n}$에 따라 $(2^2)^{-\frac{2}{3}}$의 지수 $2 \times \left(-\frac{2}{3}\right)$를 계산한 값은?",
                        "stem_en": r"By $(a^m)^n = a^{m \times n}$, what is the product of the exponents $2 \times \left(-\frac{2}{3}\right)$ in $(2^2)^{-\frac{2}{3}}$?",
                        "options": [r"$-\frac{1}{3}$", r"$-\frac{2}{3}$", r"$-1$", r"$-\frac{4}{3}$", r"$-\frac{5}{3}$"],
                        "answer": 4,
                        "exp": r"자연수 $2$를 분자 $-2$에 곱하면 $2 \times \left(-\frac{2}{3}\right) = -\frac{4}{3}$입니다.",
                        "exp_en": r"Multiplying the numerator by $2$ gives $2 \times \left(-\frac{2}{3}\right) = -\frac{4}{3}$."
                    }
                ]
            },
            {
                "title": "🌳 4단계 · [초등 분수 뺄셈] 밑이 같은 곱셈은 지수끼리 더하기",
                "title_en": "🌳 Step 4 · [Elementary Fraction Subtraction] Adding exponents with the same base",
                "knowledge": r"밑이 $2$로 같을 때 곱셈은 지수끼리 더합니다: $2^{\frac{1}{3}} \times 2^{-\frac{4}{3}} = 2^{\frac{1}{3} - \frac{4}{3}}$. 분모가 $3$으로 같으므로 분자끼리 $1 - 4 = -3$을 계산합니다.",
                "knowledge_en": r"With the same base $2$, add the exponents: $\frac{1}{3} + \left(-\frac{4}{3}\right) = \frac{1 - 4}{3} = -\frac{3}{3} = -1$.",
                "questions": [
                    {
                        "level_label": "분수 덧셈·뺄셈 디딤돌 4",
                        "level_label_en": "Fraction Addition Step 4",
                        "stem": r"분모가 같은 두 분수의 계산 $\frac{1}{3} - \frac{4}{3}$의 결과는?",
                        "stem_en": r"What is the result of $\frac{1}{3} - \frac{4}{3}$?",
                        "options": [r"$-2$", r"$-1$", r"$0$", r"$1$", r"$2$"],
                        "answer": 2,
                        "exp": r"$\frac{1 - 4}{3} = \frac{-3}{3} = -1$입니다.",
                        "exp_en": r"$\frac{1 - 4}{3} = \frac{-3}{3} = -1$."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [음수 지수 약속] $2^{-1}$을 분수로 바꾸기",
                "title_en": "💎 Step 5 · [Negative Exponent Rule] Converting $2^{-1}$ to a fraction",
                "knowledge": r"지수에 마이너스($-$)가 붙은 $a^{-1}$은 '역수(분모로 내려감)'를 뜻하는 약속입니다. 따라서 $2^{-1} = \frac{1}{2}$입니다.",
                "knowledge_en": r"A negative exponent $a^{-1}$ means the reciprocal $\frac{1}{a}$. Thus $2^{-1} = \frac{1}{2}$.",
                "questions": [
                    {
                        "level_label": "음수 지수 디딤돌 5",
                        "level_label_en": "Negative Exponent Step 5",
                        "stem": r"음의 지수 약속 $a^{-1} = \frac{1}{a}$에 따라 $2^{-1}$의 값을 구하면?",
                        "stem_en": r"Using the negative exponent definition $a^{-1} = \frac{1}{a}$, what is the value of $2^{-1}$?",
                        "options": [r"$-2$", r"$-\frac{1}{2}$", r"$\frac{1}{4}$", r"$\frac{1}{2}$", r"$2$"],
                        "answer": 4,
                        "exp": r"$2^{-1}$은 $2$의 역수이므로 $\frac{1}{2}$입니다. (부호가 음수가 되는 것이 아니라 분모로 내려갑니다!)",
                        "exp_en": r"$2^{-1}$ is the reciprocal of $2$, which is $\frac{1}{2}$."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"$\sqrt[3]{2} \times 4^{-\frac{2}{3}}$ 의 값은? [2점]",
            "stem_en": r"What is the value of $\sqrt[3]{2} \times 4^{-\frac{2}{3}}$? [2 points]",
            "options": [r"$\dfrac{1}{4}$", r"$\dfrac{1}{2}$", r"$1$", r"$2$", r"$4$"],
            "answer": 2,
            "exp": r"$\sqrt[3]{2} \times 4^{-\frac{2}{3}} = 2^{\frac{1}{3}} \times (2^2)^{-\frac{2}{3}} = 2^{\frac{1}{3} - \frac{4}{3}} = 2^{-1} = \dfrac{1}{2}$ 이므로 정답은 ②입니다.",
            "exp_en": r"$\sqrt[3]{2} \times 4^{-\frac{2}{3}} = 2^{\frac{1}{3}} \times 2^{-\frac{4}{3}} = 2^{-1} = \dfrac{1}{2}$. The correct answer is ②.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>거듭제곱근의 성질과 유리수 지수법칙</b>을 활용하여 식을 간단히 계산할 수 있는지를 평가합니다. 근호($\sqrt[3]{\ }$)를 분수 지수로 바꾸고 합성수 밑($4$)을 소수 밑($2$)으로 통일하면 초등학교 분수 연산만으로 쉽게 해결할 수 있습니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 세제곱근을 분수 지수로 변환하기</b><br>
  거듭제곱근과 유리수 지수의 정의 $\sqrt[n]{a} = a^{\frac{1}{n}}$에 의하여 앞의 항을 변환합니다:<br>
  $$\sqrt[3]{2} = 2^{\frac{1}{3}}$$<br>
  <b>2단계: 밑을 $2$로 통일하고 지수 곱하기</b><br>
  $4 = 2^2$이므로 지수법칙 $(a^m)^n = a^{mn}$을 적용합니다:<br>
  $$4^{-\frac{2}{3}} = (2^2)^{-\frac{2}{3}} = 2^{2 \times \left(-\frac{2}{3}\right)} = 2^{-\frac{4}{3}}$$<br>
  <b>3단계: 밑이 같은 거듭제곱의 곱셈</b><br>
  밑이 $2$로 같으므로 지수끼리 더합니다 ($a^p \times a^q = a^{p+q}$):<br>
  $$2^{\frac{1}{3}} \times 2^{-\frac{4}{3}} = 2^{\frac{1}{3} - \frac{4}{3}} = 2^{-\frac{3}{3}} = 2^{-1} = \frac{1}{2}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 구하는 값은 $\dfrac{1}{2}$이며, 정답은 <b>②번</b>입니다.<br>
  💡 <b>실전 팁</b>: 지수에 음수($-1$)가 나왔을 때 값을 음수로 착각하지 말고 항상 역수($\frac{1}{a}$)로 바꾸는 습관을 기르세요.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates the ability to simplify expressions involving <b>radicals and rational exponents</b> by converting radicals into fractional powers and unifying the base to $2$.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Convert the cube root into a fractional exponent</b><br>
  By definition $\sqrt[n]{a} = a^{\frac{1}{n}}$, we have:<br>
  $$\sqrt[3]{2} = 2^{\frac{1}{3}}$$<br>
  <b>Step 2: Unify the base to $2$</b><br>
  Since $4 = 2^2$, applying $(a^m)^n = a^{mn}$ gives:<br>
  $$4^{-\frac{2}{3}} = (2^2)^{-\frac{2}{3}} = 2^{-\frac{4}{3}}$$<br>
  <b>Step 3: Add exponents and evaluate</b><br>
  $$2^{\frac{1}{3}} \times 2^{-\frac{4}{3}} = 2^{\frac{1}{3} - \frac{4}{3}} = 2^{-1} = \frac{1}{2}$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The value of the expression is $\dfrac{1}{2}$, which corresponds to <b>Option ②</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 2번: c261002
    # -------------------------------------------------------------------------
    {
        "slug": "c261002",
        "qNum": "2",
        "subject": "공통(수학I·II)",
        "title": "[2026학년도 10월 고3 2번] 미분계수의 정의와 다항함수의 도함수",
        "title_en": "[2026 AY Oct Exam Grade 12 #2] Definition of Derivative & Polynomial Differentiation",
        "summary_ko": "극한식으로 표현된 미분계수 f'(1)의 의미를 알고 다항함수를 미분하여 값 구하기",
        "summary_en": "Recognize the limit definition of the derivative f'(1) and differentiate the cubic polynomial.",
        "tags": ["공통(수학I·II)", "수학II", "미분계수", "도함수", "극한", "2번"],
        "symbols": [
            {"sym": r"$\lim_{h \to 0}\dfrac{f(1+h)-f(1)}{h}$", "desc": "x=1에서의 순간변화율(미분계수) f'(1)을 뜻하는 약속", "desc_en": "Limit definition of the derivative f'(1) at x=1."},
            {"sym": r"$(x^n)' = n x^{n-1}$", "desc": "지수가 앞으로 내려오고 지수가 1 줄어드는 미분 규칙", "desc_en": "Power rule for differentiation."},
            {"sym": r"$(cx)' = c,\ (c)' = 0$", "desc": "일차항을 미분하면 앞의 숫자만 남고, 상수항은 0이 됨", "desc_en": "Derivative of a linear term is its coefficient; derivative of a constant is 0."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 사칙연산 연계] 거듭제곱과 덧셈 계산하기",
                "title_en": "🔰 Step 1 · [Elementary Arithmetic Link] Basic multiplication and addition",
                "knowledge": r"초등학교 곱셈과 덧셈을 복습해 봅시다. $1$은 몇 번을 곱해도 $1 \times 1 = 1$입니다. 따라서 $3 \times 1^2 + 3 = 3 \times 1 + 3 = 6$입니다.",
                "knowledge_en": r"In elementary arithmetic, multiplying $1$ by itself gives $1 \times 1 = 1$. Thus $3 \times 1^2 + 3 = 3 + 3 = 6$.",
                "questions": [
                    {
                        "level_label": "초등 사칙연산 디딤돌 1",
                        "level_label_en": "Elementary Arithmetic Step 1",
                        "stem": r"초등학교 사칙연산 규칙: $x = 1$일 때, $3 \times x \times x + 3$의 계산 결과는?",
                        "stem_en": r"Elementary arithmetic: When $x = 1$, what is the value of $3 \times x \times x + 3$?",
                        "options": [r"$4$", r"$5$", r"$6$", r"$7$", r"$8$"],
                        "answer": 3,
                        "exp": r"$x = 1$을 넣으면 $3 \times 1 \times 1 + 3 = 3 + 3 = 6$입니다.",
                        "exp_en": r"Substituting $x = 1$ gives $3 \times 1 \times 1 + 3 = 3 + 3 = 6$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [기호 번역] 극한식을 미분계수 $f'(1)$로 번역하기",
                "title_en": "🌿 Step 2 · [Symbol Translation] Translating the limit into $f'(1)$",
                "knowledge": r"$\lim_{h \to 0}\dfrac{f(1+h)-f(1)}{h}$라는 복잡한 기호는 '점 $x=1$에서의 아주 짧은 순간의 변화율(기울기)'을 뜻하며, 이를 간단히 $f'(1)$이라고 줄여 씁니다.",
                "knowledge_en": r"The limit $\lim_{h \to 0}\dfrac{f(1+h)-f(1)}{h}$ represents the instantaneous rate of change at $x=1$, denoted simply as $f'(1)$.",
                "questions": [
                    {
                        "level_label": "기호 번역 디딤돌 2",
                        "level_label_en": "Symbol Translation Step 2",
                        "stem": r"미분계수의 정의에 따라 극한값 $\lim_{h \to 0}\dfrac{f(1+h)-f(1)}{h}$를 기호로 간단히 나타낸 것은?",
                        "stem_en": r"By the definition of the derivative, what symbol represents $\lim_{h \to 0}\dfrac{f(1+h)-f(1)}{h}$?",
                        "options": [r"$f(0)$", r"$f(1)$", r"$f'(0)$", r"$f'(1)$", r"$f'(2)$"],
                        "answer": 4,
                        "exp": r"$1+h$에서 $h$가 $0$으로 갈 때 $1$에서의 순간변화율이므로 $f'(1)$입니다.",
                        "exp_en": r"It is the derivative of $f$ evaluated at $x = 1$, written $f'(1)$."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [미분 규칙 1] $x^3$을 미분하는 규칙",
                "title_en": "🌱 Step 3 · [Differentiation Rule 1] Differentiating $x^3$",
                "knowledge": r"거듭제곱 $x^n$을 미분($'$)할 때는 오른쪽 위의 숫자 $n$이 앞으로 내려와 곱해지고, 위쪽 숫자는 $1$만큼 줄어듭니다: $(x^n)' = n x^{n-1}$.",
                "knowledge_en": r"By the power rule $(x^n)' = n x^{n-1}$, bring the exponent down in front and subtract $1$ from the exponent.",
                "questions": [
                    {
                        "level_label": "거듭제곱 미분 디딤돌 3",
                        "level_label_en": "Power Rule Step 3",
                        "stem": r"미분 규칙 $(x^n)' = n x^{n-1}$에 따라 $x^3$을 미분한 식은?",
                        "stem_en": r"According to $(x^n)' = n x^{n-1}$, what is the derivative of $x^3$?",
                        "options": [r"$x^2$", r"$2x^2$", r"$3x^2$", r"$3x^3$", r"$x^3$"],
                        "answer": 3,
                        "exp": r"지수 $3$이 앞으로 내려오고 지수가 $3-1=2$가 되므로 $(x^3)' = 3x^2$입니다.",
                        "exp_en": r"Bringing $3$ down and reducing the power by $1$ gives $(x^3)' = 3x^2$."
                    }
                ]
            },
            {
                "title": "🌳 4단계 · [미분 규칙 2] $3x + 2$를 미분하고 도함수 $f'(x)$ 완성하기",
                "title_en": "🌳 Step 4 · [Differentiation Rule 2] Differentiating $3x + 2$ to find $f'(x)$",
                "knowledge": r"$3x$처럼 $x$가 한 번 곱해진 항을 미분하면 앞의 숫자 $3$만 남고, $2$처럼 $x$가 없는 숫자(상수)는 변하지 않으므로 미분하면 $0$이 되어 사라집니다.",
                "knowledge_en": r"Differentiating $3x$ leaves its coefficient $3$, while the constant $2$ has rate of change $0$.",
                "questions": [
                    {
                        "level_label": "도함수 완성 디딤돌 4",
                        "level_label_en": "Derivative Function Step 4",
                        "stem": r"함수 $f(x) = x^3 + 3x + 2$의 각 항을 미분하여 도함수 $f'(x)$를 구하면?",
                        "stem_en": r"What is the derivative $f'(x)$ of $f(x) = x^3 + 3x + 2$?",
                        "options": [r"$3x^2 + 3$", r"$3x^2 + 2$", r"$3x^2 + 3x$", r"$x^2 + 3$", r"$3x^2 + 5$"],
                        "answer": 1,
                        "exp": r"$(x^3)' = 3x^2$, $(3x)' = 3$, $(2)' = 0$이므로 $f'(x) = 3x^2 + 3$입니다.",
                        "exp_en": r"Differentiating term by term yields $f'(x) = 3x^2 + 3 + 0 = 3x^2 + 3$."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [최종 대입] $f'(x) = 3x^2 + 3$에 $x = 1$ 대입하기",
                "title_en": "💎 Step 5 · [Final Substitution] Evaluating $f'(1)$",
                "knowledge": r"구한 도함수 $f'(x) = 3x^2 + 3$의 $x$ 자리에 $1$을 대입하면 문제에서 구하는 극한값 $f'(1)$이 완성됩니다.",
                "knowledge_en": r"Substitute $x = 1$ into $f'(x) = 3x^2 + 3$ to obtain $f'(1)$.",
                "questions": [
                    {
                        "level_label": "미분계수 대입 디딤돌 5",
                        "level_label_en": "Derivative Evaluation Step 5",
                        "stem": r"$f'(x) = 3x^2 + 3$일 때, $f'(1)$의 값은?",
                        "stem_en": r"Given $f'(x) = 3x^2 + 3$, what is $f'(1)$?",
                        "options": [r"$6$", r"$7$", r"$8$", r"$9$", r"$10$"],
                        "answer": 1,
                        "exp": r"$f'(1) = 3(1)^2 + 3 = 3 + 3 = 6$입니다.",
                        "exp_en": r"$f'(1) = 3(1)^2 + 3 = 6$."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"함수 $f(x) = x^3 + 3x + 2$에 대하여 $\lim_{h \to 0}\dfrac{f(1+h)-f(1)}{h}$의 값은? [2점]",
            "stem_en": r"For the function $f(x) = x^3 + 3x + 2$, what is the value of $\lim_{h \to 0}\dfrac{f(1+h)-f(1)}{h}$? [2 points]",
            "options": [r"$6$", r"$7$", r"$8$", r"$9$", r"$10$"],
            "answer": 1,
            "exp": r"미분계수의 정의에 의하여 주어진 극한값은 $f'(1)$과 같습니다. $f'(x) = 3x^2 + 3$이므로 $f'(1) = 3 + 3 = 6$, 정답은 ①입니다.",
            "exp_en": r"By definition of the derivative, the limit equals $f'(1)$. Since $f'(x) = 3x^2 + 3$, $f'(1) = 6$. The correct answer is ①.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>미분계수의 정의</b>를 이해하고 다항함수의 미분법을 통해 특정 점에서의 미분계수를 정확히 구할 수 있는지를 평가합니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 미분계수의 정의 적용</b><br>
  다항함수 $f(x)$는 실수 전체에서 미분가능하므로, 주어진 극한값은 $x=1$에서의 미분계수 $f'(1)$의 정의와 일치합니다:<br>
  $$\lim_{h \to 0}\frac{f(1+h)-f(1)}{h} = f'(1)$$<br>
  <b>2단계: 도함수 $f'(x)$ 구하기</b><br>
  $f(x) = x^3 + 3x + 2$의 양변을 $x$에 대하여 미분합니다:<br>
  $$f'(x) = 3x^2 + 3$$<br>
  <b>3단계: $x = 1$ 대입</b><br>
  $$f'(1) = 3 \times 1^2 + 3 = 6$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 구하는 값은 $6$이며, 정답은 <b>①번</b>입니다.<br>
  💡 <b>실전 팁</b>: $\lim_{h \to 0}\frac{f(a+h)-f(a)}{h}$ 꼴의 극한은 직접 $f(1+h)$를 전개하지 말고 즉시 $f'(a)$로 바꾸어 도함수에 대입하세요.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem tests the <b>definition of the derivative</b> at a point and basic differentiation rules for polynomials.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Identify the limit as a derivative</b><br>
  $$\lim_{h \to 0}\frac{f(1+h)-f(1)}{h} = f'(1)$$<br>
  <b>Step 2: Differentiate $f(x) = x^3 + 3x + 2$</b><br>
  $$f'(x) = 3x^2 + 3$$<br>
  <b>Step 3: Substitute $x = 1$</b><br>
  $$f'(1) = 3(1)^2 + 3 = 6$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The value of the limit is $6$, corresponding to <b>Option ①</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 3번: c261003
    # -------------------------------------------------------------------------
    {
        "slug": "c261003",
        "qNum": "3",
        "subject": "공통(수학I·II)",
        "title": "[2026학년도 10월 고3 3번] 등비수열의 성질과 공비 추론",
        "title_en": "[2026 AY Oct Exam Grade 12 #3] Geometric Sequence & Common Ratio",
        "summary_ko": "이웃한 항들의 곱의 비율로부터 공비 r을 구하고 제4항 계산하기",
        "summary_en": "Find the common ratio r from the ratio of products of terms and compute the 4th term.",
        "tags": ["공통(수학I·II)", "수학I", "수열", "등비수열", "공비", "3번"],
        "symbols": [
            {"sym": r"등비수열 $\{a_n\}$", "desc": "일정한 수(공비 r)를 계속 곱해 나가는 숫자 줄", "desc_en": "A sequence where each term is obtained by multiplying the previous term by a constant ratio r."},
            {"sym": r"$a_n = a_1 r^{n-1}$", "desc": "첫째항 a_1에 공비 r을 (n-1)번 곱한 n번째 항", "desc_en": "General term formula of a geometric sequence."},
            {"sym": r"$\dfrac{a_2 a_3}{a_1 a_2} = \dfrac{a_3}{a_1} = r^2$", "desc": "두 식을 나누면 a_2가 약분되어 공비의 제곱만 남음", "desc_en": "Dividing the two products cancels a_2 and leaves r^2."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 분수 나눗셈 연계] $2$ 안에 $\\frac{1}{2}$이 몇 번 들어갈까?",
                "title_en": "🔰 Step 1 · [Elementary Fraction Division Link] Dividing $2$ by $\\frac{1}{2}$",
                "knowledge": r"피자 $2$판을 반 판($\frac{1}{2}$)씩 나누면 총 $4$조각이 나옵니다. 즉 $2 \div \frac{1}{2} = 2 \times 2 = 4$입니다.",
                "knowledge_en": r"Dividing $2$ wholes into halves ($\frac{1}{2}$) gives $2 \div \frac{1}{2} = 2 \times 2 = 4$ pieces.",
                "questions": [
                    {
                        "level_label": "초등 분수 나눗셈 디딤돌 1",
                        "level_label_en": "Elementary Fraction Division Step 1",
                        "stem": r"초등학교 분수의 나눗셈: $2 \div \dfrac{1}{2}$을 계산한 값은?",
                        "stem_en": r"Elementary fraction division: What is the value of $2 \div \dfrac{1}{2}$?",
                        "options": [r"$\frac{1}{4}$", r"$\frac{1}{2}$", r"$1$", r"$2$", r"$4$"],
                        "answer": 5,
                        "exp": r"나누는 분수 $\frac{1}{2}$의 분모와 분자를 뒤집어 곱하면 $2 \times 2 = 4$입니다.",
                        "exp_en": r"Multiplying by the reciprocal gives $2 \times 2 = 4$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [기호 번역] 등비수열과 공비 $r$의 뜻",
                "title_en": "🌿 Step 2 · [Symbol Translation] Meaning of geometric sequence and common ratio $r$",
                "knowledge": r"등비수열은 앞의 수에 일정한 수 $r$(공비)을 곱해서 다음 수를 만드는 규칙입니다. 따라서 $a_1$에서 두 칸 뒤인 $a_3$은 $r$을 두 번 곱한 $a_1 \times r^2$입니다.",
                "knowledge_en": r"In a geometric sequence, each step multiplies by $r$. Moving two steps from $a_1$ to $a_3$ multiplies by $r^2$.",
                "questions": [
                    {
                        "level_label": "등비수열 규칙 디딤돌 2",
                        "level_label_en": "Geometric Sequence Rule Step 2",
                        "stem": r"등비수열에서 첫째항 $a_1$에 공비 $r$을 두 번 곱하면 세 번째 항 $a_3 = a_1 r^2$이 됩니다. 이때 $\dfrac{a_3}{a_1}$을 간단히 하면?",
                        "stem_en": r"Since $a_3 = a_1 r^2$ in a geometric sequence, what does $\dfrac{a_3}{a_1}$ simplify to?",
                        "options": [r"$r$", r"$2r$", r"$r^2$", r"$r^3$", r"$r^4$"],
                        "answer": 3,
                        "exp": r"$\dfrac{a_3}{a_1} = \dfrac{a_1 r^2}{a_1} = r^2$입니다.",
                        "exp_en": r"Canceling $a_1$ leaves $\dfrac{a_3}{a_1} = r^2$."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [공비 구하기] 두 식을 나누어 양수 공비 $r$ 찾기",
                "title_en": "🌱 Step 3 · [Finding Common Ratio] Dividing the two conditions to find $r > 0$",
                "knowledge": r"$a_1 a_2 = \frac{1}{2}$이고 $a_2 a_3 = 2$이므로, 두 식을 나누면 $\dfrac{a_2 a_3}{a_1 a_2} = \dfrac{a_3}{a_1} = r^2 = \dfrac{2}{1/2} = 4$가 됩니다.",
                "knowledge_en": r"Dividing $a_2 a_3 = 2$ by $a_1 a_2 = \frac{1}{2}$ gives $r^2 = 4$. Since all terms are positive, $r > 0$.",
                "questions": [
                    {
                        "level_label": "공비 결정 디딤돌 3",
                        "level_label_en": "Common Ratio Step 3",
                        "stem": r"모든 항이 양수이므로 공비 $r > 0$입니다. $r^2 = 4$를 만족시키는 양수 $r$의 값은?",
                        "stem_en": r"Since all terms are positive ($r > 0$), what is the positive value of $r$ satisfying $r^2 = 4$?",
                        "options": [r"$1$", r"$2$", r"$3$", r"$4$", r"$8$"],
                        "answer": 2,
                        "exp": r"$2 \times 2 = 4$이므로 양수 $r = 2$입니다.",
                        "exp_en": r"Since $2^2 = 4$ and $r > 0$, we have $r = 2$."
                    }
                ]
            },
            {
                "title": "🌳 4단계 · [항 구하기] $a_2$와 $a_3$의 값 알아내기",
                "title_en": "🌳 Step 4 · [Finding Terms] Determining $a_2$ and $a_3$",
                "knowledge": r"공비 $r = 2$이므로 $a_3 = 2 a_2$입니다. 이를 $a_2 a_3 = 2$에 넣으면 $a_2 \times (2 a_2) = 2 \implies a_2^2 = 1$이 되어 양수 $a_2 = 1$을 얻습니다!",
                "knowledge_en": r"Since $r = 2$, $a_3 = 2a_2$. Substituting into $a_2 a_3 = 2$ gives $2a_2^2 = 2 \implies a_2 = 1$.",
                "questions": [
                    {
                        "level_label": "항 계산 디딤돌 4",
                        "level_label_en": "Term Calculation Step 4",
                        "stem": r"양수 $a_2$에 대하여 $a_2^2 = 1$일 때 $a_2 = 1$입니다. 공비 $r = 2$일 때 세 번째 항 $a_3 = a_2 \times r$의 값은?",
                        "stem_en": r"With $a_2 = 1$ and common ratio $r = 2$, what is the third term $a_3 = a_2 \times r$?",
                        "options": [r"$\frac{1}{2}$", r"$1$", r"$2$", r"$4$", r"$8$"],
                        "answer": 3,
                        "exp": r"$a_3 = a_2 \times r = 1 \times 2 = 2$입니다.",
                        "exp_en": r"$a_3 = 1 \times 2 = 2$."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [최종 계산] 네 번째 항 $a_4$ 구하기",
                "title_en": "💎 Step 5 · [Final Step] Finding the 4th term $a_4$",
                "knowledge": r"세 번째 항 $a_3 = 2$에 공비 $r = 2$를 한 번 더 곱하면 네 번째 항 $a_4 = a_3 \times r$이 됩니다.",
                "knowledge_en": r"Multiply the third term $a_3 = 2$ by the common ratio $r = 2$ once more to get $a_4$.",
                "questions": [
                    {
                        "level_label": "제4항 도출 디딤돌 5",
                        "level_label_en": "Fourth Term Step 5",
                        "stem": r"$a_3 = 2$이고 공비 $r = 2$일 때, $a_4 = a_3 \times r$의 값은?",
                        "stem_en": r"Given $a_3 = 2$ and $r = 2$, what is $a_4 = a_3 \times r$?",
                        "options": [r"$2$", r"$4$", r"$6$", r"$8$", r"$10$"],
                        "answer": 2,
                        "exp": r"$a_4 = 2 \times 2 = 4$입니다.",
                        "exp_en": r"$a_4 = 2 \times 2 = 4$."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"모든 항이 양수인 등비수열 $\{a_n\}$에 대하여 $a_1 a_2 = \dfrac{1}{2}$, $a_2 a_3 = 2$일 때, $a_4$의 값은? [3점]",
            "stem_en": r"For a geometric sequence $\{a_n\}$ with all positive terms, if $a_1 a_2 = \dfrac{1}{2}$ and $a_2 a_3 = 2$, what is $a_4$? [3 points]",
            "options": [r"$2$", r"$4$", r"$6$", r"$8$", r"$10$"],
            "answer": 2,
            "exp": r"$\dfrac{a_2 a_3}{a_1 a_2} = r^2 = 4$에서 $r = 2$ ($r>0$). $a_2 \cdot 2a_2 = 2$에서 $a_2 = 1$이므로 $a_4 = a_2 r^2 = 1 \times 4 = 4$. 정답은 ②입니다.",
            "exp_en": r"From $\dfrac{a_2 a_3}{a_1 a_2} = r^2 = 4$, we get $r = 2$. Then $2a_2^2 = 2 \implies a_2 = 1$, so $a_4 = a_2 r^2 = 4$. The correct answer is ②.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>등비수열의 일반항과 인접한 항들 사이의 비례 관계</b>를 이해하고 있는지를 평가합니다. 두 조건식의 비를 구하면 $a_2$가 약분되어 공비 $r$을 즉시 구할 수 있습니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 두 식을 나누어 공비 $r$ 구하기</b><br>
  등비수열 $\{a_n\}$의 공비를 $r$ ($r > 0$)이라 하면, 주어진 두 식의 비는 다음과 같습니다:<br>
  $$\frac{a_2 a_3}{a_1 a_2} = \frac{a_3}{a_1} = r^2 = \frac{2}{\frac{1}{2}} = 4$$<br>
  모든 항이 양수이므로 $r = 2$입니다.<br><br>
  <b>2단계: $a_2$ 및 $a_4$ 구하기</b><br>
  $a_3 = a_2 r = 2a_2$를 두 번째 식 $a_2 a_3 = 2$에 대입하면:<br>
  $$2a_2^2 = 2 \implies a_2^2 = 1 \implies a_2 = 1 \quad (a_2 > 0)$$<br>
  따라서 구하는 네 번째 항 $a_4$는 다음과 같습니다:<br>
  $$a_4 = a_2 r^2 = 1 \times 2^2 = 4$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 $a_4 = 4$이며, 정답은 <b>②번</b>입니다.<br>
  💡 <b>실전 팁</b>: 등비수열에서 항들의 곱이 주어질 때는 나눗셈을 통해 공통 항을 소거하고 공비의 거듭제곱($r^k$)을 먼저 찾는 것이 가장 빠릅니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem assesses understanding of <b>geometric sequences</b> by extracting the common ratio from products of consecutive terms.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Divide the two given equations to find the common ratio $r$</b><br>
  $$\frac{a_2 a_3}{a_1 a_2} = \frac{a_3}{a_1} = r^2 = \frac{2}{1/2} = 4 \implies r = 2 \quad (r > 0)$$<br>
  <b>Step 2: Find $a_2$ and $a_4$</b><br>
  Since $a_3 = 2a_2$, the equation $a_2 a_3 = 2$ gives $2a_2^2 = 2 \implies a_2 = 1$.<br>
  Therefore:<br>
  $$a_4 = a_2 r^2 = 1 \times 2^2 = 4$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The value of $a_4$ is $4$, which corresponds to <b>Option ②</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 4번: c261004
    # -------------------------------------------------------------------------
    {
        "slug": "c261004",
        "qNum": "4",
        "subject": "공통(수학I·II)",
        "title": "[2026학년도 10월 고3 4번] 구간별 정의된 함수의 연속성과 완전제곱식",
        "title_en": "[2026 AY Oct Exam Grade 12 #4] Continuity of Piecewise Function & Perfect Square",
        "summary_ko": "경계점 x=a에서 두 식의 값이 같아야 함을 이용해 이차방정식 (a-2)^2=0 풀기",
        "summary_en": "Equate the left-hand limit and right-hand value at boundary x=a to solve (a-2)^2=0.",
        "tags": ["공통(수학I·II)", "수학II", "함수의연속", "이차방정식", "4번"],
        "symbols": [
            {"sym": r"실수 전체에서 연속", "desc": "그래프가 끊어지지 않고 매끄럽게 이어져 있음", "desc_en": "The graph is connected everywhere without any breaks."},
            {"sym": r"$\lim_{x \to a^-} f(x) = f(a)$", "desc": "경계점 x=a 왼쪽 식에 a를 넣은 값과 오른쪽 식에 a를 넣은 값이 같음", "desc_en": "Left-hand limit equals the function value at boundary x=a."},
            {"sym": r"$(a-2)^2 = a^2 - 4a + 4$", "desc": "똑같은 식 (a-2)를 두 번 곱한 완전제곱식", "desc_en": "Perfect square trinomial expansion."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 사칙연산 연계] $x = 2$일 때 두 식의 값 비교하기",
                "title_en": "🔰 Step 1 · [Elementary Arithmetic Link] Comparing two expressions at $x = 2$",
                "knowledge": r"초등학교 뺄셈과 곱셈을 해 봅시다. $x = 2$일 때 $x - 4 = 2 - 4 = -2$이고, $x \times x - 3 \times x = 4 - 6 = -2$로 두 값이 정확히 같아집니다!",
                "knowledge_en": r"When $x = 2$, $x - 4 = 2 - 4 = -2$ and $x^2 - 3x = 4 - 6 = -2$. Both expressions yield the exact same value $-2$!",
                "questions": [
                    {
                        "level_label": "초등 사칙연산 디딤돌 1",
                        "level_label_en": "Elementary Arithmetic Step 1",
                        "stem": r"초등학교 곱셈과 뺄셈: $a = 2$일 때, $a \times a - 3 \times a$를 계산한 값은?",
                        "stem_en": r"Elementary arithmetic: When $a = 2$, what is the value of $a \times a - 3 \times a$?",
                        "options": [r"$-4$", r"$-2$", r"$0$", r"$2$", r"$4$"],
                        "answer": 2,
                        "exp": r"$2 \times 2 - 3 \times 2 = 4 - 6 = -2$입니다.",
                        "exp_en": r"$2 \times 2 - 3 \times 2 = 4 - 6 = -2$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [기호 번역] '연속'이란 경계점 $x = a$에서 두 길이 만나는 것!",
                "title_en": "🌿 Step 2 · [Symbol Translation] Continuity means the two pieces meet at $x = a$",
                "knowledge": r"$x < a$일 때는 위쪽 식 $x^2 - 3x$를 따라가고, $x \ge a$일 때는 아래쪽 식 $x - 4$를 따라갑니다. 그래프가 끊어지지 않으려면(연속이려면) 경계 $x = a$를 두 식에 넣은 값이 서로 같아야 합니다.",
                "knowledge_en": r"For the piecewise graph to be continuous without a break at $x = a$, substituting $x = a$ into both formulas must give the same value.",
                "questions": [
                    {
                        "level_label": "연속 조건 디딤돌 2",
                        "level_label_en": "Continuity Condition Step 2",
                        "stem": r"함수 $f(x) = \begin{cases} x^2 - 3x & (x < a) \\ x - 4 & (x \ge a) \end{cases}$가 $x = a$에서 연속이기 위한 조건식은?",
                        "stem_en": r"What equation must hold for $f(x)$ to be continuous at $x = a$?",
                        "options": [
                            r"$a^2 - 3a = a - 4$",
                            r"$a^2 - 3a = 0$",
                            r"$a - 4 = 0$",
                            r"$2a - 3 = 1$",
                            r"$a^2 + 3a = a + 4$"
                        ],
                        "answer": 1,
                        "exp": r"위쪽 식에 $x=a$를 넣은 좌극한 $a^2 - 3a$와 아래쪽 식에 $x=a$를 넣은 함숫값 $a - 4$가 같아야 합니다.",
                        "exp_en": r"The left-hand limit $a^2 - 3a$ must equal the right-hand value $a - 4$."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [이항 정리] 우변의 항을 좌변으로 옮겨 $= 0$ 만들기",
                "title_en": "🌱 Step 3 · [Rearranging Terms] Moving all terms to the left side",
                "knowledge": r"등식 $a^2 - 3a = a - 4$에서 우변의 $a - 4$를 좌변으로 옮기면 부호가 반대로 바뀌어 $a^2 - 3a - a + 4 = 0$이 됩니다.",
                "knowledge_en": r"Subtracting $a$ and adding $4$ to both sides of $a^2 - 3a = a - 4$ gives $a^2 - 4a + 4 = 0$.",
                "questions": [
                    {
                        "level_label": "방정식 정리 디딤돌 3",
                        "level_label_en": "Equation Rearrangement Step 3",
                        "stem": r"등식 $a^2 - 3a = a - 4$의 모든 항을 좌변으로 이항하여 정리한 식은?",
                        "stem_en": r"What do we get when we move all terms of $a^2 - 3a = a - 4$ to the left-hand side?",
                        "options": [
                            r"$a^2 - 2a - 4 = 0$",
                            r"$a^2 - 4a - 4 = 0$",
                            r"$a^2 - 4a + 4 = 0$",
                            r"$a^2 + 4a + 4 = 0$",
                            r"$a^2 - 2a + 4 = 0$"
                        ],
                        "answer": 3,
                        "exp": r"$-3a - a = -4a$이고 $-4$가 넘어오면 $+4$가 되므로 $a^2 - 4a + 4 = 0$입니다.",
                        "exp_en": r"Combining $-3a - a = -4a$ and moving $-4$ gives $a^2 - 4a + 4 = 0$."
                    }
                ]
            },
            {
                "title": "🌳 4단계 · [완전제곱식] $a^2 - 4a + 4 = 0$ 인수분해하기",
                "title_en": "🌳 Step 4 · [Perfect Square] Factoring $a^2 - 4a + 4 = 0$",
                "knowledge": r"곱해서 $+4$가 되고 더해서 $-4$가 되는 두 수는 $-2$와 $-2$입니다. 따라서 $a^2 - 4a + 4 = (a - 2)^2$으로 묶입니다.",
                "knowledge_en": r"Two numbers that multiply to $+4$ and add to $-4$ are $-2$ and $-2$, so $a^2 - 4a + 4 = (a - 2)^2$.",
                "questions": [
                    {
                        "level_label": "인수분해 디딤돌 4",
                        "level_label_en": "Factoring Step 4",
                        "stem": r"이차방정식 $a^2 - 4a + 4 = 0$을 완전제곱식으로 바르게 묶은 것은?",
                        "stem_en": r"How does $a^2 - 4a + 4 = 0$ factor as a perfect square?",
                        "options": [
                            r"$(a + 2)^2 = 0$",
                            r"$(a - 1)^2 = 0$",
                            r"$(a - 2)^2 = 0$",
                            r"$(a - 4)^2 = 0$",
                            r"$(a + 4)^2 = 0$"
                        ],
                        "answer": 3,
                        "exp": r"$(a - 2)^2 = a^2 - 4a + 4$이므로 $(a - 2)^2 = 0$입니다.",
                        "exp_en": r"$a^2 - 4a + 4 = (a - 2)^2 = 0$."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [정답 확정] $(a - 2)^2 = 0$을 만족하는 상수 $a$ 구하기",
                "title_en": "💎 Step 5 · [Final Answer] Solving $(a - 2)^2 = 0$ for $a$",
                "knowledge": r"제곱해서 $0$이 되는 수는 $0$뿐이므로 $a - 2 = 0$, 즉 $a = 2$입니다.",
                "knowledge_en": r"Since the square of a number is $0$ only when the number itself is $0$, $a - 2 = 0 \implies a = 2$.",
                "questions": [
                    {
                        "level_label": "상수 a 결정 디딤돌 5",
                        "level_label_en": "Constant Determination Step 5",
                        "stem": r"$(a - 2)^2 = 0$을 만족시키는 실수 $a$의 값은?",
                        "stem_en": r"What is the real number $a$ satisfying $(a - 2)^2 = 0$?",
                        "options": [r"$-2$", r"$-1$", r"$0$", r"$1$", r"$2$"],
                        "answer": 5,
                        "exp": r"$a - 2 = 0$에서 $a = 2$입니다.",
                        "exp_en": r"From $a - 2 = 0$, we obtain $a = 2$."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"함수 $f(x) = \begin{cases} x^2 - 3x & (x < a) \\ x - 4 & (x \ge a) \end{cases}$가 실수 전체의 집합에서 연속일 때, 상수 $a$의 값은? [3점]",
            "stem_en": r"When the function $f(x) = \begin{cases} x^2 - 3x & (x < a) \\ x - 4 & (x \ge a) \end{cases}$ is continuous on the set of all real numbers, what is the constant $a$? [3 points]",
            "options": [r"$-2$", r"$-1$", r"$0$", r"$1$", r"$2$"],
            "answer": 5,
            "exp": r"$x = a$에서 연속이어야 하므로 $a^2 - 3a = a - 4 \implies (a - 2)^2 = 0 \implies a = 2$입니다. 정답은 ⑤입니다.",
            "exp_en": r"Continuity at $x = a$ requires $a^2 - 3a = a - 4 \implies (a - 2)^2 = 0 \implies a = 2$. The correct answer is ⑤.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 구간별로 정의된 다항함수가 <b>실수 전체의 집합에서 연속</b>이기 위한 경계점에서의 극한값과 함숫값 일치 조건을 평가합니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 경계점 $x = a$에서의 연속 조건 수립</b><br>
  $x < a$와 $x > a$에서 $f(x)$는 각각 다항함수이므로 항상 연속입니다. 따라서 실수 전체에서 연속이려면 경계점 $x = a$에서의 좌극한과 우극한(함숫값)이 같아야 합니다:<br>
  $$\lim_{x \to a^-} (x^2 - 3x) = \lim_{x \to a^+} (x - 4)$$<br>
  $$a^2 - 3a = a - 4$$<br>
  <b>2단계: 이차방정식 풀이</b><br>
  우변의 항을 좌변으로 이항하여 인수분해합니다:<br>
  $$a^2 - 4a + 4 = 0 \implies (a - 2)^2 = 0 \implies a = 2$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 상수 $a$의 값은 $2$이며, 정답은 <b>⑤번</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem tests the condition for a piecewise polynomial function to be <b>continuous on $\mathbb{R}$</b> by matching one-sided limits at the boundary $x = a$.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Equate left-hand and right-hand limits at $x = a$</b><br>
  $$\lim_{x \to a^-} (x^2 - 3x) = f(a) \implies a^2 - 3a = a - 4$$<br>
  <b>Step 2: Solve the quadratic equation</b><br>
  $$a^2 - 4a + 4 = 0 \implies (a - 2)^2 = 0 \implies a = 2$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The constant $a$ is $2$, which corresponds to <b>Option ⑤</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 5번: c261005
    # -------------------------------------------------------------------------
    {
        "slug": "c261005",
        "qNum": "5",
        "subject": "공통(수학I·II)",
        "title": "[2026학년도 10월 고3 5번] 곱의 미분법과 미분계수 계산",
        "title_en": "[2026 AY Oct Exam Grade 12 #5] Product Rule for Differentiation",
        "summary_ko": "두 다항식의 곱으로 이루어진 함수를 곱의 미분법으로 미분하고 x=2 대입하기",
        "summary_en": "Apply the product rule (uv)' = u'v + uv' and evaluate the derivative at x=2.",
        "tags": ["공통(수학I·II)", "수학II", "미분법", "곱의미분법", "미분계수", "5번"],
        "symbols": [
            {"sym": r"$\{g(x)h(x)\}' = g'(x)h(x) + g(x)h'(x)$", "desc": "두 식의 곱을 미분할 때는 (앞 미분 × 뒤 그대로) + (앞 그대로 × 뒤 미분)", "desc_en": "Product rule: differentiate the first times the second, plus the first times the derivative of the second."},
            {"sym": r"$f'(2)$", "desc": "도함수 f'(x)에 x=2를 대입한 값", "desc_en": "Value of the derivative f'(x) at x=2."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 사칙연산 연계] $x = 2$일 때 두 괄호의 값 구하기",
                "title_en": "🔰 Step 1 · [Elementary Arithmetic Link] Evaluating the two factors at $x = 2$",
                "knowledge": r"$x = 2$를 두 괄호 $(x+1)$과 $(x^2+3x+1)$에 각각 넣어 봅시다. $2+1 = 3$이고, $2^2 + 3 \times 2 + 1 = 4 + 6 + 1 = 11$입니다.",
                "knowledge_en": r"At $x = 2$, the first factor is $2+1 = 3$ and the second factor is $2^2 + 3(2) + 1 = 4 + 6 + 1 = 11$.",
                "questions": [
                    {
                        "level_label": "초등 사칙연산 디딤돌 1",
                        "level_label_en": "Elementary Arithmetic Step 1",
                        "stem": r"초등학교 사칙연산: $x = 2$일 때, $x \times x + 3 \times x + 1$의 값을 계산하면?",
                        "stem_en": r"Elementary arithmetic: When $x = 2$, what is the value of $x \times x + 3 \times x + 1$?",
                        "options": [r"$9$", r"$10$", r"$11$", r"$12$", r"$13$"],
                        "answer": 3,
                        "exp": r"$2 \times 2 + 3 \times 2 + 1 = 4 + 6 + 1 = 11$입니다.",
                        "exp_en": r"$4 + 6 + 1 = 11$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [기호 번역] 곱의 미분법 규칙 알아보기",
                "title_en": "🌿 Step 2 · [Symbol Translation] Understanding the Product Rule",
                "knowledge": r"두 식 $A$와 $B$가 곱해진 $(A \times B)$를 미분할 때는 사이좋게 한 번씩 번갈아 미분해서 더합니다: $(A \times B)' = A' \times B + A \times B'$.",
                "knowledge_en": r"When differentiating a product $A \times B$, take turns differentiating each factor and add: $(A \times B)' = A' B + A B'$.",
                "questions": [
                    {
                        "level_label": "곱의 미분법 디딤돌 2",
                        "level_label_en": "Product Rule Step 2",
                        "stem": r"곱의 미분법 공식에 따라 $\{g(x)h(x)\}'$을 바르게 전개한 것은?",
                        "stem_en": r"According to the product rule, what is $\{g(x)h(x)\}'$?",
                        "options": [
                            r"$g'(x)h'(x)$",
                            r"$g'(x)h(x) + g(x)h'(x)$",
                            r"$g'(x)h(x) - g(x)h'(x)$",
                            r"$g(x)h(x)$",
                            r"$g'(x) + h'(x)$"
                        ],
                        "answer": 2,
                        "exp": r"(앞 미분 $\times$ 뒤 그대로) $+$ (앞 그대로 $\times$ 뒤 미분)이므로 $g'(x)h(x) + g(x)h'(x)$입니다.",
                        "exp_en": r"By the product rule, $\{g(x)h(x)\}' = g'(x)h(x) + g(x)h'(x)$."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [각 괄호 미분] $(x+1)$과 $(x^2+3x+1)$ 각각 미분하기",
                "title_en": "🌱 Step 3 · [Differentiating Factors] Differentiating each factor separately",
                "knowledge": r"앞의 식 $(x+1)$을 미분하면 $1$이고, 뒤의 식 $(x^2+3x+1)$을 미분하면 $2x + 3$입니다.",
                "knowledge_en": r"The derivative of $(x+1)$ is $1$, and the derivative of $(x^2+3x+1)$ is $2x + 3$.",
                "questions": [
                    {
                        "level_label": "다항식 미분 디딤돌 3",
                        "level_label_en": "Factor Derivative Step 3",
                        "stem": r"이차식 $h(x) = x^2 + 3x + 1$을 미분한 $h'(x)$에 $x = 2$를 대입한 값 $h'(2)$는?",
                        "stem_en": r"For $h(x) = x^2 + 3x + 1$, what is the value of its derivative $h'(2)$ at $x = 2$?",
                        "options": [r"$5$", r"$6$", r"$7$", r"$8$", r"$9$"],
                        "answer": 3,
                        "exp": r"$h'(x) = 2x + 3$이므로 $h'(2) = 2(2) + 3 = 7$입니다.",
                        "exp_en": r"Since $h'(x) = 2x + 3$, $h'(2) = 4 + 3 = 7$."
                    }
                ]
            },
            {
                "title": "🌳 4단계 · [도함수 식 세우기] $f'(x)$ 완성하기",
                "title_en": "🌳 Step 4 · [Assembling Derivative] Writing the expression for $f'(x)$",
                "knowledge": r"곱의 미분법에 넣으면 $f'(x) = 1 \cdot (x^2+3x+1) + (x+1)(2x+3)$이 됩니다.",
                "knowledge_en": r"Combining the pieces gives $f'(x) = 1 \cdot (x^2+3x+1) + (x+1)(2x+3)$.",
                "questions": [
                    {
                        "level_label": "도함수 결합 디딤돌 4",
                        "level_label_en": "Assembling Derivative Step 4",
                        "stem": r"$f'(x) = (x^2+3x+1) + (x+1)(2x+3)$에서 뒤쪽 항 $(x+1)(2x+3)$에 $x = 2$를 대입한 값은?",
                        "stem_en": r"In $f'(x) = (x^2+3x+1) + (x+1)(2x+3)$, what is the value of the second term $(x+1)(2x+3)$ at $x = 2$?",
                        "options": [r"$14$", r"$18$", r"$21$", r"$24$", r"$28$"],
                        "answer": 3,
                        "exp": r"$x = 2$를 대입하면 $(2+1) \times (4+3) = 3 \times 7 = 21$입니다.",
                        "exp_en": r"At $x = 2$, $(2+1)(4+3) = 3 \times 7 = 21$."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [최종 합산] 앞쪽 값 $11$과 뒤쪽 값 $21$ 더하기",
                "title_en": "💎 Step 5 · [Final Addition] Adding $11$ and $21$ to get $f'(2)$",
                "knowledge": r"1단계에서 구한 앞쪽 괄호 값 $11$과 4단계에서 구한 뒤쪽 곱의 값 $21$을 더하면 $f'(2) = 11 + 21 = 32$입니다.",
                "knowledge_en": r"Add the first part $11$ (from Step 1) and the second part $21$ (from Step 4) to get $f'(2) = 11 + 21 = 32$.",
                "questions": [
                    {
                        "level_label": "최종 덧셈 디딤돌 5",
                        "level_label_en": "Final Addition Step 5",
                        "stem": r"$f'(2) = 11 + 21$을 계산한 최종 값은?",
                        "stem_en": r"What is the final value of $f'(2) = 11 + 21$?",
                        "options": [r"$26$", r"$28$", r"$30$", r"$32$", r"$34$"],
                        "answer": 4,
                        "exp": r"$11 + 21 = 32$입니다.",
                        "exp_en": r"$11 + 21 = 32$."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"함수 $f(x) = (x+1)(x^2+3x+1)$에 대하여 $f'(2)$의 값은? [3점]",
            "stem_en": r"For the function $f(x) = (x+1)(x^2+3x+1)$, what is the value of $f'(2)$? [3 points]",
            "options": [r"$26$", r"$28$", r"$30$", r"$32$", r"$34$"],
            "answer": 4,
            "exp": r"$f'(x) = (x^2+3x+1) + (x+1)(2x+3)$이므로 $f'(2) = (4+6+1) + 3 \times 7 = 11 + 21 = 32$입니다. 정답은 ④입니다.",
            "exp_en": r"By the product rule, $f'(x) = (x^2+3x+1) + (x+1)(2x+3)$, so $f'(2) = 11 + 21 = 32$. The correct answer is ④.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 다항함수의 <b>곱의 미분법</b>을 적용하여 미분계수를 정확히 계산할 수 있는지를 평가합니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 곱의 미분법으로 도함수 $f'(x)$ 구하기</b><br>
  $f(x) = (x+1)(x^2+3x+1)$의 양변을 $x$에 대하여 미분하면:<br>
  $$f'(x) = (x+1)'(x^2+3x+1) + (x+1)(x^2+3x+1)'$$<br>
  $$f'(x) = 1 \cdot (x^2+3x+1) + (x+1)(2x+3)$$<br>
  <b>2단계: $x = 2$ 대입 계산</b><br>
  식을 전개할 필요 없이 바로 $x = 2$를 대입합니다:<br>
  $$f'(2) = (2^2 + 3 \times 2 + 1) + (2 + 1)(2 \times 2 + 3) = 11 + 3 \times 7 = 11 + 21 = 32$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 $f'(2) = 32$이며, 정답은 <b>④번</b>입니다.<br>
  💡 <b>실전 팁</b>: 특정 점에서의 미분계수 $f'(a)$를 구할 때는 도함수 식을 굳이 전개하여 정리하지 말고, 곱의 미분법 형태 그대로 $x = a$를 대입하는 것이 훨씬 빠르고 계산 실수가 적습니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem assesses mastery of the <b>product rule for differentiation</b> and evaluating derivatives at a given point.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Apply the product rule</b><br>
  $$f'(x) = (x^2+3x+1) + (x+1)(2x+3)$$<br>
  <b>Step 2: Substitute $x = 2$</b><br>
  $$f'(2) = (4 + 6 + 1) + (3)(4 + 3) = 11 + 21 = 32$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The value of $f'(2)$ is $32$, which corresponds to <b>Option ④</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 6번: c261006
    # -------------------------------------------------------------------------
    {
        "slug": "c261006",
        "qNum": "6",
        "subject": "공통(수학I·II)",
        "title": "[2026학년도 10월 고3 6번] 삼각함수 사이의 관계와 사분면의 부호",
        "title_en": "[2026 AY Oct Exam Grade 12 #6] Trigonometric Identities & Quadrant Signs",
        "summary_ko": "1 + tan^2(θ) = 1/cos^2(θ) 관계식과 제2사분면에서의 코사인 부호(-) 적용하기",
        "summary_en": "Use 1 + tan^2(θ) = 1/cos^2(θ) and the negative sign of cosine in the second quadrant.",
        "tags": ["공통(수학I·II)", "수학I", "삼각함수", "삼각함수사이의관계", "사분면", "6번"],
        "symbols": [
            {"sym": r"$\dfrac{\pi}{2} < \theta < \pi$", "desc": "각도가 90도보다 크고 180도보다 작은 제2사분면(왼쪽 위)", "desc_en": "Angle θ lies in Quadrant II (between 90° and 180°)."},
            {"sym": r"$1 + \tan^2\theta = \dfrac{1}{\cos^2\theta}$", "desc": "피타고라스 정리에서 나온 탄젠트와 코사인의 단짝 공식", "desc_en": "Pythagorean trigonometric identity relating tangent and cosine."},
            {"sym": r"제2사분면 $\cos\theta < 0$", "desc": "코사인은 x좌표이므로 왼쪽(제2사분면)에서는 음수(-)", "desc_en": "Cosine represents the x-coordinate on the unit circle, which is negative in Quadrant II."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 도형·피타고라스 연계] 직각삼각형의 빗변 길이 구하기",
                "title_en": "🔰 Step 1 · [Elementary Geometry Link] Finding the hypotenuse of a right triangle",
                "knowledge": r"초등·중등 도형에서 직각삼각형의 밑변이 $1$이고 높이가 $\sqrt{2}$일 때, (빗변)$^2 = 1^2 + (\sqrt{2})^2 = 1 + 2 = 3$입니다.",
                "knowledge_en": r"In a right triangle with base $1$ and height $\sqrt{2}$, the square of the hypotenuse is $1^2 + (\sqrt{2})^2 = 1 + 2 = 3$.",
                "questions": [
                    {
                        "level_label": "초등 도형·덧셈 디딤돌 1",
                        "level_label_en": "Elementary Geometry Step 1",
                        "stem": r"초등학교 덧셈과 도형 규칙: 밑변의 제곱이 $1$이고 높이의 제곱이 $2$일 때, 두 값을 더한 $1 + 2$는?",
                        "stem_en": r"Elementary addition & geometry: If the square of the base is $1$ and the square of the height is $2$, what is $1 + 2$?",
                        "options": [r"$1$", r"$2$", r"$3$", r"$4$", r"$5$"],
                        "answer": 3,
                        "exp": r"$1 + 2 = 3$이므로 빗변의 제곱은 $3$, 빗변의 길이는 $\sqrt{3}$이 됩니다.",
                        "exp_en": r"$1 + 2 = 3$, so the hypotenuse squared is $3$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [삼각함수 관계식] $\\cos^2\\theta$의 값 구하기",
                "title_en": "🌿 Step 2 · [Trigonometric Identity] Finding $\\cos^2\\theta$",
                "knowledge": r"삼각함수 공식 $1 + \tan^2\theta = \dfrac{1}{\cos^2\theta}$에 $\tan^2\theta = 2$를 넣으면 $1 + 2 = 3 = \dfrac{1}{\cos^2\theta}$이 됩니다. 양변을 뒤집으면 $\cos^2\theta = \dfrac{1}{3}$입니다.",
                "knowledge_en": r"Substituting $\tan^2\theta = 2$ into $1 + \tan^2\theta = \dfrac{1}{\cos^2\theta}$ gives $\dfrac{1}{\cos^2\theta} = 3 \implies \cos^2\theta = \dfrac{1}{3}$.",
                "questions": [
                    {
                        "level_label": "삼각함수 항등식 디딤돌 2",
                        "level_label_en": "Trig Identity Step 2",
                        "stem": r"$\tan^2\theta = 2$일 때, 공식 $\dfrac{1}{\cos^2\theta} = 1 + \tan^2\theta$를 이용하여 구한 $\cos^2\theta$의 값은?",
                        "stem_en": r"Given $\tan^2\theta = 2$, what is $\cos^2\theta$ using $\dfrac{1}{\cos^2\theta} = 1 + \tan^2\theta$?",
                        "options": [r"$\frac{1}{6}$", r"$\frac{1}{3}$", r"$\frac{1}{2}$", r"$\frac{2}{3}$", r"$3$"],
                        "answer": 2,
                        "exp": r"$\dfrac{1}{\cos^2\theta} = 1 + 2 = 3$이므로 역수를 취하면 $\cos^2\theta = \dfrac{1}{3}$입니다.",
                        "exp_en": r"Since $\dfrac{1}{\cos^2\theta} = 3$, taking the reciprocal gives $\cos^2\theta = \dfrac{1}{3}$."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [사분면의 부호] 제2사분면에서 $\\cos\\theta$의 부호 판단하기",
                "title_en": "🌱 Step 3 · [Quadrant Sign] Sign of $\\cos\\theta$ in Quadrant II",
                "knowledge": r"$\dfrac{\pi}{2} < \theta < \pi$ ($90^\circ < \theta < 180^\circ$)는 좌표평면의 왼쪽 위(제2사분면)입니다. 코사인($\cos\theta$)은 단위원 위의 점의 $x$좌표이므로 왼쪽에서는 항상 음수($-$)입니다.",
                "knowledge_en": r"For $\dfrac{\pi}{2} < \theta < \pi$ (Quadrant II, upper-left), $\cos\theta$ corresponds to the $x$-coordinate, which is negative ($-$).",
                "questions": [
                    {
                        "level_label": "사분면 부호 디딤돌 3",
                        "level_label_en": "Quadrant Sign Step 3",
                        "stem": r"$\dfrac{\pi}{2} < \theta < \pi$ (제2사분면)일 때, 삼각함수의 부호로 옳은 것은?",
                        "stem_en": r"When $\dfrac{\pi}{2} < \theta < \pi$ (Quadrant II), which statement about the sign of $\cos\theta$ is true?",
                        "options": [
                            r"$\cos\theta > 0$ (양수)",
                            r"$\cos\theta < 0$ (음수)",
                            r"$\cos\theta = 0$",
                            r"$\cos\theta \ge 1$",
                            r"부호를 알 수 없다"
                        ],
                        "answer": 2,
                        "exp": r"제2사분면에서는 사인($\sin$)만 양수이고 코사인($\cos$)과 탄젠트($\tan$)는 모두 음수($<0$)입니다.",
                        "exp_en": r"In Quadrant II, only sine is positive; cosine is negative ($\cos\theta < 0$)."
                    }
                ]
            },
            {
                "title": "💎 4단계 · [분모의 유리화] $-\\dfrac{1}{\\sqrt{3}}$을 유리화하여 정답 구하기",
                "title_en": "💎 Step 4 · [Rationalizing Denominator] Rewriting $-\\dfrac{1}{\\sqrt{3}}$",
                "knowledge": r"$\cos^2\theta = \dfrac{1}{3}$이고 $\cos\theta < 0$이므로 $\cos\theta = -\dfrac{1}{\sqrt{3}}$입니다. 분모와 분자에 똑같이 $\sqrt{3}$을 곱하면 $-\dfrac{\sqrt{3}}{3}$이 됩니다.",
                "knowledge_en": r"Since $\cos^2\theta = \dfrac{1}{3}$ and $\cos\theta < 0$, $\cos\theta = -\dfrac{1}{\sqrt{3}} = -\dfrac{\sqrt{3}}{3}$.",
                "questions": [
                    {
                        "level_label": "유리화 디딤돌 4",
                        "level_label_en": "Rationalization Step 4",
                        "stem": r"$\cos\theta = -\dfrac{1}{\sqrt{3}}$의 분모를 유리화한 값은?",
                        "stem_en": r"What is $-\dfrac{1}{\sqrt{3}}$ after rationalizing the denominator?",
                        "options": [
                            r"$-\dfrac{\sqrt{3}}{3}$",
                            r"$-\dfrac{1}{3}$",
                            r"$-\dfrac{1}{6}$",
                            r"$\dfrac{1}{3}$",
                            r"$\dfrac{\sqrt{3}}{3}$"
                        ],
                        "answer": 1,
                        "exp": r"분모와 분자에 $\sqrt{3}$을 곱하면 $-\dfrac{1 \times \sqrt{3}}{\sqrt{3} \times \sqrt{3}} = -\dfrac{\sqrt{3}}{3}$입니다.",
                        "exp_en": r"Multiplying numerator and denominator by $\sqrt{3}$ yields $-\dfrac{\sqrt{3}}{3}$."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"$\dfrac{\pi}{2} < \theta < \pi$인 $\theta$에 대하여 $\tan^2\theta = 2$일 때, $\cos\theta$의 값은? [3점]",
            "stem_en": r"For $\dfrac{\pi}{2} < \theta < \pi$, if $\tan^2\theta = 2$, what is the value of $\cos\theta$? [3 points]",
            "options": [
                r"$-\dfrac{\sqrt{3}}{3}$",
                r"$-\dfrac{1}{3}$",
                r"$-\dfrac{1}{6}$",
                r"$\dfrac{1}{3}$",
                r"$\dfrac{\sqrt{3}}{3}$"
            ],
            "answer": 1,
            "exp": r"$1 + \tan^2\theta = \dfrac{1}{\cos^2\theta}$에서 $\cos^2\theta = \dfrac{1}{3}$이고, 제2사분면에서 $\cos\theta < 0$이므로 $\cos\theta = -\dfrac{\sqrt{3}}{3}$입니다. 정답은 ①입니다.",
            "exp_en": r"From $1 + \tan^2\theta = \dfrac{1}{\cos^2\theta} = 3$, $\cos^2\theta = \dfrac{1}{3}$. Since $\theta \in (\frac{\pi}{2}, \pi)$, $\cos\theta = -\dfrac{\sqrt{3}}{3}$. The correct answer is ①.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>삼각함수 사이의 관계식</b>($1 + \tan^2\theta = \sec^2\theta = \frac{1}{\cos^2\theta}$)과 동경이 위치한 사분면에 따른 삼각함수의 부호를 판별할 수 있는지를 평가합니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 삼각함수 사이의 관계식 적용</b><br>
  $\sin^2\theta + \cos^2\theta = 1$의 양변을 $\cos^2\theta$로 나누면 $1 + \tan^2\theta = \dfrac{1}{\cos^2\theta}$이 성립합니다. $\tan^2\theta = 2$를 대입하면:<br>
  $$\frac{1}{\cos^2\theta} = 1 + 2 = 3 \implies \cos^2\theta = \frac{1}{3}$$<br>
  <b>2단계: 사분면의 부호 결정</b><br>
  주어진 각의 범위 $\dfrac{\pi}{2} < \theta < \pi$는 제2사분면이므로 $\cos\theta < 0$입니다. 따라서:<br>
  $$\cos\theta = -\frac{1}{\sqrt{3}} = -\frac{\sqrt{3}}{3}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 $\cos\theta = -\dfrac{\sqrt{3}}{3}$이며, 정답은 <b>①번</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates mastery of <b>Pythagorean trigonometric identities</b> and determining the sign of trigonometric functions by quadrant.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Apply $1 + \tan^2\theta = \dfrac{1}{\cos^2\theta}$</b><br>
  $$\frac{1}{\cos^2\theta} = 1 + 2 = 3 \implies \cos^2\theta = \frac{1}{3}$$<br>
  <b>Step 2: Apply the Quadrant II sign condition</b><br>
  Since $\dfrac{\pi}{2} < \theta < \pi$, $\cos\theta < 0$, which yields:<br>
  $$\cos\theta = -\frac{1}{\sqrt{3}} = -\frac{\sqrt{3}}{3}$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The value of $\cos\theta$ is $-\dfrac{\sqrt{3}}{3}$, corresponding to <b>Option ①</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 7번: c261007
    # -------------------------------------------------------------------------
    {
        "slug": "c261007",
        "qNum": "7",
        "subject": "공통(수학I·II)",
        "title": "[2026학년도 10월 고3 7번] 두 곡선과 두 직선으로 둘러싸인 도형의 넓이",
        "title_en": "[2026 AY Oct Exam Grade 12 #7] Area Bounded by Two Curves and Vertical Lines",
        "summary_ko": "구간 [0, 2]에서 위쪽 곡선 식에서 아래쪽 곡선 식을 빼서 정적분으로 넓이 구하기",
        "summary_en": "Integrate the difference (upper curve minus lower curve) over the interval [0, 2].",
        "tags": ["공통(수학I·II)", "수학II", "정적분", "넓이", "이차함수", "7번"],
        "symbols": [
            {"sym": r"$\int_0^2 (\text{위쪽 식} - \text{아래쪽 식})\,dx$", "desc": "x=0부터 x=2까지 세로 길이를 촘촘히 더해 넓이를 구하는 정적분", "desc_en": "Definite integral of (upper minus lower function) from x=0 to x=2 gives the area."},
            {"sym": r"$\int x^2\,dx = \dfrac{1}{3}x^3 + C$", "desc": "x^2을 적분하면 지수가 3이 되고 앞에 1/3이 곱해짐", "desc_en": "Power rule for integration of x^2."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 분수 덧셈 연계] $\\dfrac{1}{2}$과 $\\dfrac{1}{4}$ 통분하여 더하기",
                "title_en": "🔰 Step 1 · [Elementary Fraction Addition Link] Adding $\\dfrac{1}{2} + \\dfrac{1}{4}$",
                "knowledge": r"초등학교 분수 덧셈에서 $\dfrac{1}{2}$은 분모와 분자에 $2$를 곱하면 $\dfrac{2}{4}$와 같습니다. 따라서 $\dfrac{1}{2} + \dfrac{1}{4} = \dfrac{2}{4} + \dfrac{1}{4} = \dfrac{3}{4}$입니다.",
                "knowledge_en": r"In elementary fractions, $\dfrac{1}{2} = \dfrac{2}{4}$. Adding $\dfrac{1}{4}$ gives $\dfrac{2}{4} + \dfrac{1}{4} = \dfrac{3}{4}$.",
                "questions": [
                    {
                        "level_label": "초등 분수 덧셈 디딤돌 1",
                        "level_label_en": "Elementary Fraction Addition Step 1",
                        "stem": r"초등학교 분수 덧셈: $\dfrac{1}{2} + \dfrac{1}{4}$을 통분하여 계산한 값은?",
                        "stem_en": r"Elementary fraction addition: What is the sum $\dfrac{1}{2} + \dfrac{1}{4}$?",
                        "options": [r"$\frac{1}{4}$", r"$\frac{2}{6}$", r"$\frac{3}{4}$", r"$1$", r"$\frac{5}{4}$"],
                        "answer": 3,
                        "exp": r"$\dfrac{1}{2} = \dfrac{2}{4}$이므로 $\dfrac{2}{4} + \dfrac{1}{4} = \dfrac{3}{4}$입니다.",
                        "exp_en": r"$\dfrac{2}{4} + \dfrac{1}{4} = \dfrac{3}{4}$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [세로 길이 구하기] 위쪽 곡선에서 아래쪽 곡선 빼기",
                "title_en": "🌿 Step 2 · [Vertical Height] Subtracting the lower curve from the upper curve",
                "knowledge": r"그림에서 위쪽 곡선은 $y = \dfrac{1}{2}x^2 + 2$이고 아래쪽 곡선은 $y = -\dfrac{1}{4}x^2 - 1$입니다. 빼기 음수($-(-)$)는 덧셈($+$)이 되므로 두 식의 차는 $\left(\dfrac{1}{2} + \dfrac{1}{4}\right)x^2 + (2 + 1) = \dfrac{3}{4}x^2 + 3$입니다.",
                "knowledge_en": r"Subtracting the lower curve from the upper curve gives $\left(\dfrac{1}{2}x^2 + 2\right) - \left(-\dfrac{1}{4}x^2 - 1\right) = \dfrac{3}{4}x^2 + 3$.",
                "questions": [
                    {
                        "level_label": "식의 뺄셈 디딤돌 2",
                        "level_label_en": "Subtracting Curves Step 2",
                        "stem": r"위쪽 식 $\left(\dfrac{1}{2}x^2 + 2\right)$에서 아래쪽 식 $\left(-\dfrac{1}{4}x^2 - 1\right)$을 뺀 결과는?",
                        "stem_en": r"What is the result of $\left(\dfrac{1}{2}x^2 + 2\right) - \left(-\dfrac{1}{4}x^2 - 1\right)$?",
                        "options": [
                            r"$\dfrac{1}{4}x^2 + 1$",
                            r"$\dfrac{1}{4}x^2 + 3$",
                            r"$\dfrac{3}{4}x^2 + 1$",
                            r"$\dfrac{3}{4}x^2 + 3$",
                            r"$\dfrac{3}{4}x^2 - 3$"
                        ],
                        "answer": 4,
                        "exp": r"$\dfrac{1}{2}x^2 - \left(-\dfrac{1}{4}x^2\right) = \dfrac{3}{4}x^2$이고, $2 - (-1) = 3$이므로 $\dfrac{3}{4}x^2 + 3$입니다.",
                        "exp_en": r"Combining like terms gives $\dfrac{3}{4}x^2 + 3$."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [적분 규칙] $\\dfrac{3}{4}x^2 + 3$을 부정적분하기",
                "title_en": "🌱 Step 3 · [Integration Rule] Finding the antiderivative of $\\dfrac{3}{4}x^2 + 3$",
                "knowledge": r"$x^2$을 적분하면 $\dfrac{1}{3}x^3$이 됩니다. 따라서 $\dfrac{3}{4}x^2$을 적분하면 $\dfrac{3}{4} \times \dfrac{1}{3}x^3 = \dfrac{1}{4}x^3$이 되고, 상수 $3$을 적분하면 $3x$가 됩니다.",
                "knowledge_en": r"Integrating $\dfrac{3}{4}x^2$ gives $\dfrac{3}{4} \cdot \dfrac{1}{3}x^3 = \dfrac{1}{4}x^3$, and integrating $3$ gives $3x$.",
                "questions": [
                    {
                        "level_label": "적분 공식 디딤돌 3",
                        "level_label_en": "Antiderivative Step 3",
                        "stem": r"$\dfrac{3}{4}x^2 + 3$을 적분한 식 $\left[\ \Box\ \right]_0^2$의 빈칸에 알맞은 식은?",
                        "stem_en": r"What is the antiderivative of $\dfrac{3}{4}x^2 + 3$?",
                        "options": [
                            r"$\dfrac{1}{4}x^3 + 3x$",
                            r"$\dfrac{3}{4}x^3 + 3x$",
                            r"$\dfrac{1}{4}x^3 + 3$",
                            r"$\dfrac{3}{2}x + 3$",
                            r"$x^3 + 3x$"
                        ],
                        "answer": 1,
                        "exp": r"$\int \left(\dfrac{3}{4}x^2 + 3\right)dx = \dfrac{1}{4}x^3 + 3x$입니다.",
                        "exp_en": r"The antiderivative is $\dfrac{1}{4}x^3 + 3x$."
                    }
                ]
            },
            {
                "title": "💎 4단계 · [위끝 대입] $x = 2$를 대입하여 넓이 완성하기",
                "title_en": "💎 Step 4 · [Evaluating Definite Integral] Substituting $x = 2$",
                "knowledge": r"$\dfrac{1}{4}x^3 + 3x$에 $x = 2$를 대입하면 $\dfrac{1}{4} \times 8 + 3 \times 2 = 2 + 6 = 8$이고, $x = 0$을 대입하면 $0$이므로 넓이는 $8$입니다.",
                "knowledge_en": r"At $x = 2$, $\dfrac{1}{4}(2^3) + 3(2) = \dfrac{8}{4} + 6 = 2 + 6 = 8$.",
                "questions": [
                    {
                        "level_label": "정적분 값 디딤돌 4",
                        "level_label_en": "Definite Integral Step 4",
                        "stem": r"$\left[\dfrac{1}{4}x^3 + 3x\right]_0^2$를 계산한 넓이의 값은?",
                        "stem_en": r"What is the value of $\left[\dfrac{1}{4}x^3 + 3x\right]_0^2$?",
                        "options": [r"$7$", r"$\dfrac{15}{2}$", r"$8$", r"$\dfrac{17}{2}$", r"$9$"],
                        "answer": 3,
                        "exp": r"$\dfrac{8}{4} + 6 = 2 + 6 = 8$입니다.",
                        "exp_en": r"$2 + 6 = 8$."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"두 곡선 $y = \dfrac{1}{2}x^2 + 2$, $y = -\dfrac{1}{4}x^2 - 1$ 및 두 직선 $x = 0$, $x = 2$로 둘러싸인 부분의 넓이는? [3점]",
            "stem_en": r"What is the area of the region bounded by the two curves $y = \dfrac{1}{2}x^2 + 2$, $y = -\dfrac{1}{4}x^2 - 1$, and the lines $x = 0$, $x = 2$? [3 points]",
            "options": [r"$7$", r"$\dfrac{15}{2}$", r"$8$", r"$\dfrac{17}{2}$", r"$9$"],
            "answer": 3,
            "exp": r"$\int_0^2 \left\{\left(\dfrac{1}{2}x^2+2\right) - \left(-\dfrac{1}{4}x^2-1\right)\right\}dx = \int_0^2 \left(\dfrac{3}{4}x^2 + 3\right)dx = \left[\dfrac{1}{4}x^3 + 3x\right]_0^2 = 2 + 6 = 8$. 정답은 ③입니다.",
            "exp_en": r"$\int_0^2 \left(\dfrac{3}{4}x^2 + 3\right)dx = \left[\dfrac{1}{4}x^3 + 3x\right]_0^2 = 2 + 6 = 8$. The correct answer is ③.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>정적분을 활용하여 두 곡선과 두 직선으로 둘러싸인 도형의 넓이</b>를 구할 수 있는지를 평가합니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 구간 $[0, 2]$에서 두 곡선의 대소 비교 및 정적분 식 세우기</b><br>
  닫힌구간 $[0, 2]$에서 $\dfrac{1}{2}x^2 + 2 > 0 > -\dfrac{1}{4}x^2 - 1$이므로, 둘러싸인 부분의 넓이 $S$는 위쪽 식에서 아래쪽 식을 뺀 함수의 정적분입니다:<br>
  $$S = \int_0^2 \left\{ \left(\frac{1}{2}x^2 + 2\right) - \left(-\frac{1}{4}x^2 - 1\right) \right\} dx = \int_0^2 \left(\frac{3}{4}x^2 + 3\right) dx$$<br>
  <b>2단계: 정적분 계산</b><br>
  $$S = \left[ \frac{1}{4}x^3 + 3x \right]_0^2 = \left(\frac{8}{4} + 6\right) - 0 = 2 + 6 = 8$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 구하는 넓이는 $8$이며, 정답은 <b>③번</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem assesses finding the <b>area between two curves</b> over a closed interval using definite integration.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Set up the definite integral of (upper curve minus lower curve)</b><br>
  $$S = \int_0^2 \left\{ \left(\frac{1}{2}x^2 + 2\right) - \left(-\frac{1}{4}x^2 - 1\right) \right\} dx = \int_0^2 \left(\frac{3}{4}x^2 + 3\right) dx$$<br>
  <b>Step 2: Evaluate the integral</b><br>
  $$S = \left[ \frac{1}{4}x^3 + 3x \right]_0^2 = 2 + 6 = 8$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The area of the region is $8$, corresponding to <b>Option ③</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 8번: c261008
    # -------------------------------------------------------------------------
    {
        "slug": "c261008",
        "qNum": "8",
        "subject": "공통(수학I·II)",
        "title": "[2026학년도 10월 고3 8번] 로그의 정의와 밑의 변환 성질",
        "title_en": "[2026 AY Oct Exam Grade 12 #8] Definition & Base Properties of Logarithms",
        "summary_ko": "log_a(b)=2에서 b=a^2을 이끌어내고 log_4(a^2)=log_2(a) 성질로 a, b 구하기",
        "summary_en": "Use b=a^2 from log_a(b)=2 and simplify log_4(a^2)=log_2(a) to find b/a.",
        "tags": ["공통(수학I·II)", "수학I", "로그", "로그의성질", "밑변환", "8번"],
        "symbols": [
            {"sym": r"$\log_a b = 2 \iff b = a^2$", "desc": "'a를 몇 번 곱해야 b가 될까?'의 답이 2라는 뜻이므로 b = a^2", "desc_en": "Definition of logarithm: log_a(b) = 2 means b = a^2."},
            {"sym": r"$\log_{a^m} b^n = \dfrac{n}{m}\log_a b$", "desc": "밑과 진수에 똑같이 제곱이 있으면 약분되어 처음 로그와 같아짐", "desc_en": "Exponents of the base and argument come out as a ratio n/m."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 거듭제곱 연계] $2$를 $4$번 곱하면 얼마일까?",
                "title_en": "🔰 Step 1 · [Elementary Multiplication Link] Multiplying $2$ four times ($2^4$)",
                "knowledge": r"초등학교 곱셈으로 $2 \times 2 \times 2 \times 2$를 계산해 봅시다. $2 \times 2 = 4$, $4 \times 2 = 8$, $8 \times 2 = 16$입니다.",
                "knowledge_en": r"In elementary multiplication, $2 \times 2 \times 2 \times 2 = 4 \times 4 = 16$.",
                "questions": [
                    {
                        "level_label": "초등 곱셈 디딤돌 1",
                        "level_label_en": "Elementary Multiplication Step 1",
                        "stem": r"초등학교 곱셈 규칙: $2$를 네 번 곱한 값 $2 \times 2 \times 2 \times 2$ ($= 2^4$)는 얼마인가요?",
                        "stem_en": r"Elementary multiplication: What is $2 \times 2 \times 2 \times 2$ ($= 2^4$)?",
                        "options": [r"$4$", r"$8$", r"$12$", r"$16$", r"$32$"],
                        "answer": 4,
                        "exp": r"$2 \times 2 = 4$이고 $4 \times 4 = 16$이므로 $2^4 = 16$입니다.",
                        "exp_en": r"$2^4 = 16$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [기호 번역] $\\log_a b = 2$를 거듭제곱으로 바꾸기",
                "title_en": "🌿 Step 2 · [Symbol Translation] Translating $\\log_a b = 2$ into exponents",
                "knowledge": r"로그 기호 $\log_a b = 2$는 '$a$를 $2$제곱하면 $b$가 된다'는 뜻입니다. 따라서 $b = a^2$이고, 양변을 $a$로 나누면 문제에서 묻는 $\dfrac{b}{a} = \dfrac{a^2}{a} = a$가 됩니다!",
                "knowledge_en": r"$\log_a b = 2$ means $b = a^2$. Therefore, the target ratio $\dfrac{b}{a} = \dfrac{a^2}{a} = a$!",
                "questions": [
                    {
                        "level_label": "로그 정의 디딤돌 2",
                        "level_label_en": "Logarithm Definition Step 2",
                        "stem": r"$\log_a b = 2$일 때 $b = a^2$입니다. 이때 구하고자 하는 $\dfrac{b}{a}$를 $a$로 간단히 나타내면?",
                        "stem_en": r"Since $\log_a b = 2$ means $b = a^2$, what does $\dfrac{b}{a}$ simplify to in terms of $a$?",
                        "options": [r"$1$", r"$2$", r"$a$", r"$2a$", r"$a^2$"],
                        "answer": 3,
                        "exp": r"$\dfrac{b}{a} = \dfrac{a^2}{a} = a$이므로, 결국 $a$의 값만 구하면 바로 정답이 됩니다!",
                        "exp_en": r"$\dfrac{b}{a} = \dfrac{a^2}{a} = a$, so finding $a$ directly gives the final answer."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [로그의 성질] $\\log_4 b = \\log_{2^2}(a^2)$ 간단히 하기",
                "title_en": "🌱 Step 3 · [Logarithm Property] Simplifying $\\log_4(a^2)$",
                "knowledge": r"$4 = 2^2$이고 $b = a^2$이므로 $\log_4 b = \log_{2^2}(a^2)$입니다. 밑의 지수 $2$와 진수의 지수 $2$가 똑같이 앞으로 나가 약분($\frac{2}{2} = 1$)되므로 $\log_2 a$와 같아집니다.",
                "knowledge_en": r"Since $4 = 2^2$ and $b = a^2$, $\log_4 b = \log_{2^2}(a^2) = \dfrac{2}{2}\log_2 a = \log_2 a$.",
                "questions": [
                    {
                        "level_label": "로그 성질 디딤돌 3",
                        "level_label_en": "Logarithm Simplification Step 3",
                        "stem": r"로그의 성질 $\log_{2^2}(a^2) = \dfrac{2}{2}\log_2 a$를 이용하면 $\log_2 a + \log_4 b$는 무엇과 같아지나요?",
                        "stem_en": r"Using $\log_4 b = \log_{2^2}(a^2) = \log_2 a$, what does $\log_2 a + \log_4 b$ simplify to?",
                        "options": [
                            r"$\log_2 a$",
                            r"$2\log_2 a$",
                            r"$3\log_2 a$",
                            r"$4\log_2 a$",
                            r"$(\log_2 a)^2$"
                        ],
                        "answer": 2,
                        "exp": r"$\log_4 b = \log_2 a$이므로 $\log_2 a + \log_4 b = \log_2 a + \log_2 a = 2\log_2 a$입니다.",
                        "exp_en": r"$\log_2 a + \log_2 a = 2\log_2 a$."
                    }
                ]
            },
            {
                "title": "💎 4단계 · [방정식 풀이] $2\\log_2 a = 8$에서 $a$ 구하기",
                "title_en": "💎 Step 4 · [Solving for $a$] Finding $a$ from $2\\log_2 a = 8$",
                "knowledge": r"$2\log_2 a = 8$의 양변을 $2$로 나누면 $\log_2 a = 4$입니다. 즉 '$2$를 $4$제곱하면 $a$가 된다'는 뜻이므로 $a = 2^4 = 16$입니다.",
                "knowledge_en": r"From $2\log_2 a = 8$, we get $\log_2 a = 4 \implies a = 2^4 = 16$.",
                "questions": [
                    {
                        "level_label": "최종 값 도출 디딤돌 4",
                        "level_label_en": "Final Value Step 4",
                        "stem": r"$\log_2 a = 4$일 때, $\dfrac{b}{a} = a = 2^4$의 값은?",
                        "stem_en": r"When $\log_2 a = 4$, what is the value of $\dfrac{b}{a} = a = 2^4$?",
                        "options": [r"$2$", r"$4$", r"$8$", r"$16$", r"$32$"],
                        "answer": 4,
                        "exp": r"1단계에서 계산한 것처럼 $2^4 = 16$이므로 $\dfrac{b}{a} = 16$입니다.",
                        "exp_en": r"$a = 2^4 = 16$, so $\dfrac{b}{a} = 16$."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"두 양수 $a$ ($a \neq 1$), $b$가 $\log_a b = 2$, $\log_2 a + \log_4 b = 8$을 만족시킬 때, $\dfrac{b}{a}$의 값은? [3점]",
            "stem_en": r"When positive numbers $a$ ($a \neq 1$) and $b$ satisfy $\log_a b = 2$ and $\log_2 a + \log_4 b = 8$, what is $\dfrac{b}{a}$? [3 points]",
            "options": [r"$2$", r"$4$", r"$8$", r"$16$", r"$32$"],
            "answer": 4,
            "exp": r"$b = a^2$이므로 $\log_4 b = \log_{2^2}(a^2) = \log_2 a$. 따라서 $2\log_2 a = 8 \implies \log_2 a = 4 \implies a = 16$. $\dfrac{b}{a} = a = 16$이므로 정답은 ④입니다.",
            "exp_en": r"Since $b = a^2$, $\log_4 b = \log_2 a$. Then $2\log_2 a = 8 \implies \log_2 a = 4 \implies a = 16$, so $\dfrac{b}{a} = a = 16$. The correct answer is ④.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>로그의 정의와 밑의 변환 공식</b>($\log_{a^m} b^n = \frac{n}{m}\log_a b$)을 활용하여 미지수 $a, b$의 값을 구할 수 있는지를 평가합니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 첫 번째 조건에서 $a$와 $b$의 관계 도출</b><br>
  로그의 정의에 의하여 $\log_a b = 2 \iff b = a^2$입니다. 이때 구하는 식은 $\dfrac{b}{a} = \dfrac{a^2}{a} = a$가 됩니다.<br><br>
  <b>2단계: 두 번째 조건에 대입하여 밑 통일하기</b><br>
  $4 = 2^2$이고 $b = a^2$이므로:<br>
  $$\log_4 b = \log_{2^2} (a^2) = \frac{2}{2}\log_2 a = \log_2 a$$<br>
  따라서 두 번째 식은 다음과 같이 정리됩니다:<br>
  $$\log_2 a + \log_4 b = 2\log_2 a = 8 \implies \log_2 a = 4 \implies a = 2^4 = 16$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 $\dfrac{b}{a} = a = 16$이며, 정답은 <b>④번</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem tests the <b>definition of logarithms</b> and simplifying logarithmic expressions by unifying the base.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Express $b$ in terms of $a$</b><br>
  $$\log_a b = 2 \implies b = a^2 \implies \frac{b}{a} = a$$<br>
  <b>Step 2: Simplify the second equation</b><br>
  $$\log_4 b = \log_{2^2}(a^2) = \log_2 a \implies 2\log_2 a = 8 \implies \log_2 a = 4 \implies a = 2^4 = 16$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  Therefore, $\dfrac{b}{a} = 16$, which corresponds to <b>Option ④</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 9번: c261009
    # -------------------------------------------------------------------------
    {
        "slug": "c261009",
        "qNum": "9",
        "subject": "공통(수학I·II)",
        "title": "[2026학년도 10월 고3 9번] 분수함수의 극한 수렴 조건과 이차함수의 인수 추론",
        "title_en": "[2026 AY Oct Exam Grade 12 #9] Convergence of Rational Limit & Quadratic Factors",
        "summary_ko": "분모 (x-a)^2을 약분시키기 위해 a=3인 경우와 a≠3인 경우로 나누어 실수 a 구하기",
        "summary_en": "Analyze the two cases (a=3 and a≠3) where the numerator cancels the double root (x-a)^2 in the denominator.",
        "tags": ["공통(수학I·II)", "수학II", "함수의극한", "미정계수", "이차함수", "9번"],
        "symbols": [
            {"sym": r"$\lim_{x \to a}\dfrac{f(x)(x-3)}{(x-a)^2} = 5$", "desc": "분모에 (x-a)가 두 개 있으므로 분자에도 (x-a)가 최소 두 개 있어야 약분되어 5가 됨", "desc_en": "Since the denominator has (x-a)^2 approaching 0, the numerator must also contain (x-a)^2 as a factor."},
            {"sym": r"최고차항의 계수가 $1$인 이차함수", "desc": "f(x) = x^2 + px + q (또는 (x-α)(x-β)) 모양의 식", "desc_en": "A monic quadratic function of the form f(x) = (x - α)(x - β)."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 분수 약분 연계] 분모와 분자의 같은 덩어리 지우기",
                "title_en": "🔰 Step 1 · [Elementary Fraction Cancellation Link] Canceling common factors",
                "knowledge": r"초등학교 분수 약분에서 $\dfrac{7 \times 7 \times 5}{7 \times 7}$는 분모와 분자의 $7 \times 7$을 똑같이 지우면 $5$만 남습니다. 식에서도 분모에 $(x-a)^2$이 있으면 분자에도 $(x-a)^2$이 있어야 약분할 수 있습니다.",
                "knowledge_en": r"Just as $\dfrac{7 \times 7 \times 5}{7 \times 7} = 5$ by canceling $7 \times 7$, the numerator must have $(x-a)^2$ to cancel $(x-a)^2$ in the denominator.",
                "questions": [
                    {
                        "level_label": "초등 약분 디딤돌 1",
                        "level_label_en": "Elementary Cancellation Step 1",
                        "stem": r"초등학교 분수 약분: 분수 $\dfrac{(x-a)^2 \times 5}{(x-a)^2}$에서 분모와 분자의 $(x-a)^2$을 약분하면 남는 값은? (단, $x \neq a$)",
                        "stem_en": r"Elementary fraction cancellation: When canceling $(x-a)^2$ in $\dfrac{(x-a)^2 \times 5}{(x-a)^2}$ ($x \neq a$), what remains?",
                        "options": [r"$1$", r"$3$", r"$5$", r"$a$", r"$x-a$"],
                        "answer": 3,
                        "exp": r"분모와 분자의 $(x-a)^2$을 약분하면 $5$가 남습니다.",
                        "exp_en": r"Canceling $(x-a)^2$ leaves $5$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [첫 번째 경우: $a = 3$] $(x-3)$이 이미 하나 도와줄 때!",
                "title_en": "🌿 Step 2 · [Case 1: $a = 3$] When $(x-3)$ already provides one factor",
                "knowledge": r"만약 $a = 3$이면 분모는 $(x-3)^2$입니다. 이때 분자에는 이미 $(x-3)$이 하나 곱해져 있으므로, 이차함수 $f(x)$가 $(x-3)$을 하나만 가지고 있으면(즉 $f(x) = (x-3)(x-k)$) 분모의 $(x-3)^2$과 완전히 약분됩니다!",
                "knowledge_en": r"If $a = 3$, the denominator is $(x-3)^2$. Since the numerator already has $(x-3)$, $f(x) = (x-3)(x-k)$ provides the second $(x-3)$ factor.",
                "questions": [
                    {
                        "level_label": "첫 번째 경우 디딤돌 2",
                        "level_label_en": "Case 1 Analysis Step 2",
                        "stem": r"$a = 3$이고 $f(x) = (x-3)(x+2)$일 때, $\lim_{x \to 3}\dfrac{f(x)(x-3)}{(x-3)^2} = \lim_{x \to 3}(x+2)$의 값은?",
                        "stem_en": r"When $a = 3$ and $f(x) = (x-3)(x+2)$, what is $\lim_{x \to 3}\dfrac{f(x)(x-3)}{(x-3)^2} = \lim_{x \to 3}(x+2)$?",
                        "options": [r"$1$", r"$2$", r"$3$", r"$4$", r"$5$"],
                        "answer": 5,
                        "exp": r"$x = 3$을 대입하면 $3 + 2 = 5$가 되어 문제의 조건($= 5$)을 완벽히 만족합니다! 따라서 $a = 3$은 가능한 값입니다.",
                        "exp_en": r"Substituting $x = 3$ gives $3 + 2 = 5$, satisfying the condition. Thus $a = 3$ is valid."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [두 번째 경우: $a \\neq 3$] $f(x)$ 혼자서 $(x-a)^2$을 다 책임질 때!",
                "title_en": "🌱 Step 3 · [Case 2: $a \\neq 3$] When $f(x)$ alone must equal $(x-a)^2$",
                "knowledge": r"$a \neq 3$이면 옆에 있는 $(x-3)$은 $(x-a)$ 약분에 도움을 주지 못합니다. 따라서 이차함수 $f(x)$ 혼자서 $(x-a)$를 두 개 모두 가져야 하므로 $f(x) = (x-a)^2$이 됩니다.",
                "knowledge_en": r"If $a \neq 3$, $(x-3)$ does not cancel $(x-a)$. Thus the monic quadratic $f(x)$ must be $f(x) = (x-a)^2$.",
                "questions": [
                    {
                        "level_label": "두 번째 경우 디딤돌 3",
                        "level_label_en": "Case 2 Analysis Step 3",
                        "stem": r"$a \neq 3$일 때 $f(x) = (x-a)^2$을 대입하여 $(x-a)^2$을 약분하면 $\lim_{x \to a}(x-3) = 5$가 됩니다. 이를 만족하는 $a$의 값은?",
                        "stem_en": r"When $f(x) = (x-a)^2$, canceling $(x-a)^2$ leaves $a - 3 = 5$. What is $a$?",
                        "options": [r"$5$", r"$6$", r"$7$", r"$8$", r"$9$"],
                        "answer": 4,
                        "exp": r"$a - 3 = 5$에서 $a = 8$입니다.",
                        "exp_en": r"From $a - 3 = 5$, we get $a = 8$."
                    }
                ]
            },
            {
                "title": "💎 4단계 · [최종 합산] 가능한 모든 실수 $a$의 값 더하기",
                "title_en": "💎 Step 4 · [Final Sum] Adding all possible values of $a$",
                "knowledge": r"2단계에서 구한 $a = 3$과 3단계에서 구한 $a = 8$을 더하면 $3 + 8 = 11$입니다.",
                "knowledge_en": r"Adding the two valid values $a = 3$ and $a = 8$ gives $3 + 8 = 11$.",
                "questions": [
                    {
                        "level_label": "모든 a의 합 디딤돌 4",
                        "level_label_en": "Sum of Values Step 4",
                        "stem": r"조건을 만족시키는 두 실수 $a = 3$과 $a = 8$의 합은?",
                        "stem_en": r"What is the sum of the two valid values $a = 3$ and $a = 8$?",
                        "options": [r"$7$", r"$8$", r"$9$", r"$10$", r"$11$"],
                        "answer": 5,
                        "exp": r"$3 + 8 = 11$입니다.",
                        "exp_en": r"$3 + 8 = 11$."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"$\lim_{x \to a}\dfrac{f(x)(x-3)}{(x-a)^2} = 5$를 만족시키는 최고차항의 계수가 $1$인 이차함수 $f(x)$가 존재하도록 하는 모든 실수 $a$의 값의 합은? [4점]",
            "stem_en": r"What is the sum of all real numbers $a$ for which there exists a monic quadratic function $f(x)$ satisfying $\lim_{x \to a}\dfrac{f(x)(x-3)}{(x-a)^2} = 5$? [4 points]",
            "options": [r"$7$", r"$8$", r"$9$", r"$10$", r"$11$"],
            "answer": 5,
            "exp": r"(i) $a = 3$일 때 $f(x) = (x-3)(x+2)$이면 극한값이 $5$로 존재합니다. (ii) $a \neq 3$일 때 $f(x) = (x-a)^2$이어야 하므로 $a - 3 = 5 \implies a = 8$. 따라서 합은 $3 + 8 = 11$, 정답은 ⑤입니다.",
            "exp_en": r"Case 1: $a = 3$ works with $f(x) = (x-3)(x+2)$. Case 2: $a \neq 3$ requires $f(x) = (x-a)^2$, giving $a - 3 = 5 \implies a = 8$. The sum is $3 + 8 = 11$ (⑤).",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 분모가 $(x-a)^2 \to 0$으로 가는 극한이 $0$이 아닌 상수 $5$로 수렴하기 위해 <b>분자 $f(x)(x-3)$이 $(x-a)^2$을 인수로 가져야 함</b>을 추론하는 4점 문항입니다. 특히 $(x-3)$ 자체가 $(x-a)$가 되는 경우($a=3$)를 놓치지 않고 케이스를 나누는 것이 핵심입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: $a = 3$인 경우</b><br>
  $a = 3$이면 주어진 식은 $\lim_{x \to 3}\dfrac{f(x)(x-3)}{(x-3)^2} = \lim_{x \to 3}\dfrac{f(x)}{x-3} = 5$가 됩니다.<br>
  분모가 $0$으로 가므로 최고차항의 계수가 $1$인 이차함수 $f(x)$가 $f(x) = (x-3)(x-k)$ 꼴이면:<br>
  $$\lim_{x \to 3}\frac{(x-3)(x-k)}{x-3} = 3 - k = 5 \implies k = -2$$<br>
  즉 $f(x) = (x-3)(x+2)$가 존재하므로 <b>$a = 3$</b>은 조건을 만족시킵니다.<br><br>
  <b>2단계: $a \neq 3$인 경우</b><br>
  $a \neq 3$이면 $(x-3)$은 $(x-a)$를 인수로 갖지 않으므로, 이차함수 $f(x)$가 홀로 $(x-a)^2$을 인수로 가져야 합니다. 최고차항의 계수가 $1$이므로 $f(x) = (x-a)^2$입니다. 이를 대입하면:<br>
  $$\lim_{x \to a}\frac{(x-a)^2(x-3)}{(x-a)^2} = \lim_{x \to a}(x-3) = a - 3 = 5 \implies a = 8$$<br>
  즉 $f(x) = (x-8)^2$이 존재하므로 <b>$a = 8$</b>은 조건을 만족시킵니다.
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  조건을 만족시키는 모든 실수 $a$의 값의 합은 $3 + 8 = 11$이며, 정답은 <b>⑤번</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>For the limit $\lim_{x \to a}\dfrac{f(x)(x-3)}{(x-a)^2} = 5$ to converge, the numerator $f(x)(x-3)$ must contain $(x-a)^2$ as a factor. We divide into two cases based on whether $a = 3$ or $a \neq 3$.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Case $a = 3$</b><br>
  The limit simplifies to $\lim_{x \to 3}\dfrac{f(x)}{x-3} = 5$, which is satisfied by the monic quadratic $f(x) = (x-3)(x+2)$. Thus $a = 3$ is valid.<br><br>
  <b>Step 2: Case $a \neq 3$</b><br>
  Since $x - 3 \neq 0$ at $x = a$, $f(x)$ must have a double root at $x = a$, so $f(x) = (x-a)^2$. Then:<br>
  $$\lim_{x \to a}\frac{(x-a)^2(x-3)}{(x-a)^2} = a - 3 = 5 \implies a = 8$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The sum of all possible values of $a$ is $3 + 8 = 11$, which corresponds to <b>Option ⑤</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 10번: c261010
    # -------------------------------------------------------------------------
    {
        "slug": "c261010",
        "qNum": "10",
        "subject": "공통(수학I·II)",
        "title": "[2026학년도 10월 고3 10번] 등차수열의 일반항과 절댓값 합 방정식",
        "title_en": "[2026 AY Oct Exam Grade 12 #10] Arithmetic Sequence Sum & Absolute Value Equation",
        "summary_ko": "a_2 + a_9 = 0에서 공차 d=-4를 구하고 |S_k|=48을 만족하는 k=4, 6, 12 찾기",
        "summary_en": "Find the common difference d=-4 from a_2+a_9=0 and solve |S_k|=48 for natural numbers k.",
        "tags": ["공통(수학I·II)", "수학I", "수열", "등차수열", "등차수열의합", "10번"],
        "symbols": [
            {"sym": r"등차수열 $a_n = a_1 + (n-1)d$", "desc": "첫째항 a_1에 일정한 차이(공차 d)를 (n-1)번 더한 수", "desc_en": "General term of an arithmetic sequence with first term a_1 and common difference d."},
            {"sym": r"$S_k = \dfrac{k(a_1 + a_k)}{2}$", "desc": "첫째항부터 k번째 항까지 모두 더한 합", "desc_en": "Sum of the first k terms of an arithmetic sequence."},
            {"sym": r"$|S_k| = 48$", "desc": "합 S_k가 +48이거나 -48이 되는 두 경우를 모두 찾음", "desc_en": "Absolute value equation meaning S_k = 48 or S_k = -48."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 규칙 찾기 연계] $18$에서 $4$씩 빼 나가는 숫자 줄",
                "title_en": "🔰 Step 1 · [Elementary Pattern Link] Subtracting $4$ repeatedly starting from $18$",
                "knowledge": r"첫 번째 수가 $18$이고 $4$씩 줄어드는 숫자 줄을 적어 봅시다: $18, 14, 10, 6, 2, -2, \dots$ 처음 네 개의 수를 더하면 $18 + 14 + 10 + 6 = 48$입니다!",
                "knowledge_en": r"Starting at $18$ and subtracting $4$ each step gives $18, 14, 10, 6, 2, -2, \dots$ The sum of the first $4$ numbers is $18 + 14 + 10 + 6 = 48$!",
                "questions": [
                    {
                        "level_label": "초등 덧셈·규칙 디딤돌 1",
                        "level_label_en": "Elementary Pattern Step 1",
                        "stem": r"초등학교 덧셈 규칙: $18$부터 $4$씩 작아지는 네 수 $18 + 14 + 10 + 6$을 모두 더한 합은?",
                        "stem_en": r"Elementary addition: What is the sum $18 + 14 + 10 + 6$?",
                        "options": [r"$40$", r"$44$", r"$48$", r"$52$", r"$56$"],
                        "answer": 3,
                        "exp": r"$18 + 14 = 32$이고 $10 + 6 = 16$이므로 $32 + 16 = 48$입니다. 즉 $k = 4$일 때 합이 $48$이 됩니다!",
                        "exp_en": r"$18 + 14 + 10 + 6 = 48$, which already gives our first solution $k = 4$!"
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [공차 구하기] $a_2 + a_9 = 0$에서 공차 $d$ 찾기",
                "title_en": "🌿 Step 2 · [Common Difference] Finding $d$ from $a_2 + a_9 = 0$",
                "knowledge": r"$a_1 = 18$일 때, $a_2 = 18 + d$이고 $a_9 = 18 + 8d$입니다. 두 항을 더하면 $36 + 9d = 0$이므로 $9d = -36 \implies d = -4$입니다.",
                "knowledge_en": r"Since $a_1 = 18$, $a_2 + a_9 = (18+d) + (18+8d) = 36 + 9d = 0 \implies d = -4$.",
                "questions": [
                    {
                        "level_label": "공차 계산 디딤돌 2",
                        "level_label_en": "Common Difference Step 2",
                        "stem": r"$36 + 9d = 0$을 만족시키는 공차 $d$의 값은?",
                        "stem_en": r"What is the common difference $d$ satisfying $36 + 9d = 0$?",
                        "options": [r"$-6$", r"$-5$", r"$-4$", r"$-3$", r"$-2$"],
                        "answer": 3,
                        "exp": r"$9d = -36$의 양변을 $9$로 나누면 $d = -4$입니다.",
                        "exp_en": r"Dividing $-36$ by $9$ gives $d = -4$."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [등차수열의 합] $S_k = 2k(10 - k)$ 식 세우기",
                "title_en": "🌱 Step 3 · [Sum Formula] Expressing $S_k = 2k(10 - k)$",
                "knowledge": r"$a_k = 18 - 4(k-1) = 22 - 4k$이므로, 등차수열의 합 공식에 넣으면 $S_k = \dfrac{k(18 + 22 - 4k)}{2} = k(20 - 2k) = 2k(10 - k)$가 됩니다.",
                "knowledge_en": r"With $a_k = 22 - 4k$, the sum of the first $k$ terms is $S_k = \dfrac{k(18 + 22 - 4k)}{2} = 2k(10 - k)$.",
                "questions": [
                    {
                        "level_label": "합이 +48인 경우 디딤돌 3",
                        "level_label_en": "Positive Sum Step 3",
                        "stem": r"$S_k = 2k(10 - k) = 48$에서 양변을 $2$로 나누면 $k(10 - k) = 24$가 됩니다. 이를 만족하는 두 자연수 $k$는?",
                        "stem_en": r"Solving $k(10 - k) = 24$, what are the two natural numbers $k$?",
                        "options": [
                            r"$2,\ 8$",
                            r"$3,\ 7$",
                            r"$4,\ 6$",
                            r"$5,\ 5$",
                            r"$1,\ 9$"
                        ],
                        "answer": 3,
                        "exp": r"더해서 $10$이 되고 곱해서 $24$가 되는 두 자연수는 $4$와 $6$입니다 ($4 \times 6 = 24$).",
                        "exp_en": r"Since $4 \times 6 = 24$ and $6 \times 4 = 24$, the solutions are $k = 4$ and $k = 6$."
                    }
                ]
            },
            {
                "title": "🌳 4단계 · [절댓값 조건] 합이 음수($S_k = -48$)가 되는 자연수 $k$ 찾기",
                "title_en": "🌳 Step 4 · [Negative Sum Case] Solving $S_k = -48$ for natural number $k$",
                "knowledge": r"$|S_k| = 48$은 $S_k = -48$인 경우도 포함합니다! $2k(10 - k) = -48 \implies k(k - 10) = 24$에서 차이가 $10$이고 곱이 $24$인 두 자연수는 $12$와 $2$ ($12 \times 2 = 24$)이므로 $k = 12$입니다.",
                "knowledge_en": r"$|S_k| = 48$ also includes $S_k = -48 \implies k(k - 10) = 24 \implies (k - 12)(k + 2) = 0 \implies k = 12$.",
                "questions": [
                    {
                        "level_label": "합이 -48인 경우 디딤돌 4",
                        "level_label_en": "Negative Sum Step 4",
                        "stem": r"$S_k = -48$, 즉 $k(k - 10) = 24$를 만족시키는 자연수 $k$의 값은?",
                        "stem_en": r"What natural number $k$ satisfies $k(k - 10) = 24$?",
                        "options": [r"$8$", r"$10$", r"$12$", r"$14$", r"$16$"],
                        "answer": 3,
                        "exp": r"$k = 12$일 때 $12 \times (12 - 10) = 12 \times 2 = 24$가 성립합니다.",
                        "exp_en": r"When $k = 12$, $12 \times (12 - 10) = 24$."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [최종 합산] 구한 세 자연수 $k = 4, 6, 12$ 모두 더하기",
                "title_en": "💎 Step 5 · [Final Sum] Adding all valid natural numbers $k = 4, 6, 12$",
                "knowledge": r"조건을 만족하는 자연수 $k$는 $4, 6, 12$ 세 개입니다. 이를 모두 더하면 $4 + 6 + 12 = 22$입니다.",
                "knowledge_en": r"Summing all valid natural numbers $k \in \{4, 6, 12\}$ gives $4 + 6 + 12 = 22$.",
                "questions": [
                    {
                        "level_label": "최종 덧셈 디딤돌 5",
                        "level_label_en": "Final Sum Step 5",
                        "stem": r"$|S_k| = 48$을 만족시키는 모든 자연수 $k$의 값 $4,\ 6,\ 12$의 합은?",
                        "stem_en": r"What is the sum of $4,\ 6,\ \text{and } 12$?",
                        "options": [r"$16$", r"$19$", r"$22$", r"$25$", r"$28$"],
                        "answer": 3,
                        "exp": r"$4 + 6 + 12 = 22$입니다.",
                        "exp_en": r"$4 + 6 + 12 = 22$."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"첫째항이 $18$인 등차수열 $\{a_n\}$의 첫째항부터 제$n$항까지의 합을 $S_n$이라 하자. $a_2 + a_9 = 0$일 때, $|S_k| = 48$을 만족시키는 모든 자연수 $k$의 값의 합은? [4점]",
            "stem_en": r"Let $S_n$ be the sum of the first $n$ terms of an arithmetic sequence $\{a_n\}$ with $a_1 = 18$. If $a_2 + a_9 = 0$, what is the sum of all natural numbers $k$ satisfying $|S_k| = 48$? [4 points]",
            "options": [r"$16$", r"$19$", r"$22$", r"$25$", r"$28$"],
            "answer": 3,
            "exp": r"$a_2 + a_9 = 36 + 9d = 0 \implies d = -4$. $S_k = 2k(10-k)$에서 $|S_k| = 48 \implies k(10-k) = \pm 24$이므로 자연수 $k = 4, 6, 12$. 합은 $22$ (③)입니다.",
            "exp_en": r"$d = -4$ and $S_k = 2k(10-k)$. Solving $|S_k| = 48$ for natural numbers $k$ yields $k = 4, 6, 12$, whose sum is $22$ (③).",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>등차수열의 일반항과 첫째항부터 제$n$항까지의 합 $S_n$</b>을 구하고, 절댓값이 포함된 방정식 $|S_k| = 48$을 풀어 조건을 만족하는 자연수 항 번호 $k$를 모두 찾는 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 공차 $d$와 일반항 구하기</b><br>
  첫째항 $a_1 = 18$이고 공차를 $d$라 하면:<br>
  $$a_2 + a_9 = (a_1 + d) + (a_1 + 8d) = 2a_1 + 9d = 36 + 9d = 0 \implies d = -4$$<br>
  따라서 $a_n = 18 - 4(n-1) = 22 - 4n$입니다.<br><br>
  <b>2단계: 합 $S_k$의 식 도출</b><br>
  $$S_k = \frac{k(a_1 + a_k)}{2} = \frac{k(18 + 22 - 4k)}{2} = k(20 - 2k) = 2k(10 - k)$$<br>
  <b>3단계: $|S_k| = 48$ 풀이</b><br>
  $|2k(10 - k)| = 48 \iff |k(10 - k)| = 24$에서 두 경우로 나눕니다:<br>
  • (i) $k(10 - k) = 24 \implies k^2 - 10k + 24 = (k-4)(k-6) = 0 \implies k = 4$ 또는 $k = 6$<br>
  • (ii) $k(10 - k) = -24 \implies k^2 - 10k - 24 = (k-12)(k+2) = 0 \implies k = 12$ ($k$는 자연수)
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 모든 자연수 $k$의 값의 합은 $4 + 6 + 12 = 22$이며, 정답은 <b>③번</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates finding the <b>sum of an arithmetic sequence</b> and solving an absolute value quadratic equation $|S_k| = 48$ over natural numbers.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Determine common difference $d$</b><br>
  $$a_2 + a_9 = 2(18) + 9d = 0 \implies d = -4$$<br>
  <b>Step 2: Formula for $S_k$</b><br>
  $$S_k = \frac{k(36 - 4(k-1))}{2} = 2k(10 - k)$$<br>
  <b>Step 3: Solve $|2k(10 - k)| = 48$</b><br>
  • $k(10 - k) = 24 \implies (k-4)(k-6) = 0 \implies k = 4, 6$<br>
  • $k(10 - k) = -24 \implies (k-12)(k+2) = 0 \implies k = 12$ ($k \in \mathbb{N}$)
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The sum of all natural numbers $k$ is $4 + 6 + 12 = 22$, corresponding to <b>Option ③</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 11번: c261011
    # -------------------------------------------------------------------------
    {
        "slug": "c261011",
        "qNum": "11",
        "subject": "공통(수학I·II)",
        "title": "[2026학년도 10월 고3 11번] 수직선 운동의 속도·위치와 이동 거리 합답형 추론",
        "title_en": "[2026 AY Oct Exam Grade 12 #11] Velocity, Position, and Total Distance on a Line",
        "summary_ko": "운동 방향이 바뀌는 시각에서 v(4)=0임을 이용해 a=1을 구하고 위치와 이동 거리 판별하기",
        "summary_en": "Use v(4)=0 at the turning point to find a=1, then evaluate position at t=3 and total distance on [0, 4].",
        "tags": ["공통(수학I·II)", "수학II", "정적분의활용", "속도와거리", "합답형", "11번"],
        "symbols": [
            {"sym": r"운동 방향이 바뀔 때 $v(t) = 0$", "desc": "앞으로 가다가 뒤로(또는 뒤로 가다가 앞으로) 방향을 바꾸는 순간 속도는 0이 됨", "desc_en": "When a particle reverses direction, its instantaneous velocity v(t) is 0."},
            {"sym": r"위치 $x(t) = \int_0^t v(s)\,ds$", "desc": "원점 출발 시 속도를 그대로 적분하면 현재 위치가 됨", "desc_en": "Position starting from the origin is the definite integral of velocity."},
            {"sym": r"움직인 거리 $= \int_0^t |v(s)|\,ds$", "desc": "앞으로 간 거리와 뒤로 간 거리를 모두 양수로 더한 총 걸음 수", "desc_en": "Total distance traveled is the integral of the absolute value of velocity (speed)."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 수직선 걷기 연계] 위치와 움직인 거리의 차이 알기",
                "title_en": "🔰 Step 1 · [Elementary Number Line Walk Link] Position vs. Total Distance",
                "knowledge": r"수직선 원점($0$)에서 오른쪽으로 $7$칸 갔다가 왼쪽으로 $1$칸 돌아오면, 현재 서 있는 '위치'는 $7 - 1 = 6$이지만 실제로 걸은 '움직인 거리'는 $7 + 1 = 8$칸입니다!",
                "knowledge_en": r"If you walk $7$ steps right from $0$ and $1$ step left, your current position is $7 - 1 = 6$, while your total distance walked is $7 + 1 = 8$.",
                "questions": [
                    {
                        "level_label": "초등 수직선 디딤돌 1",
                        "level_label_en": "Elementary Number Line Step 1",
                        "stem": r"초등학교 수직선과 분수 덧셈: 앞으로 $\dfrac{20}{3}$만큼 갔다가 뒤로 $\dfrac{4}{3}$만큼 걸었을 때, 실제로 걸은 총 거리 $\dfrac{20}{3} + \dfrac{4}{3}$는?",
                        "stem_en": r"Elementary fraction addition: If you walk $\dfrac{20}{3}$ forward and $\dfrac{4}{3}$ backward, what is the total distance $\dfrac{20}{3} + \dfrac{4}{3}$?",
                        "options": [r"$6$", r"$7$", r"$8$", r"$9$", r"$10$"],
                        "answer": 3,
                        "exp": r"$\dfrac{20 + 4}{3} = \dfrac{24}{3} = 8$입니다. (따라서 <보기> ㄷ의 10은 틀린 설명이 됩니다!)",
                        "exp_en": r"$\dfrac{20 + 4}{3} = \dfrac{24}{3} = 8$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [<보기> ㄱ 확인] $t = 4$에서 속도가 $0$임을 이용해 $a$ 구하기",
                "title_en": "🌿 Step 2 · [Statement ㄱ] Finding $a$ using $v(4) = 0$",
                "knowledge": r"시각 $t = 4$에서 운동 방향이 바뀌므로 그 순간 멈췄다가 방향을 트는 것입니다. 즉 $v(4) = 4^2 - (a+5) \times 4 + 8 = 0$입니다.",
                "knowledge_en": r"Since the particle changes direction at $t = 4$, $v(4) = 16 - 4(a+5) + 8 = 0$.",
                "questions": [
                    {
                        "level_label": "ㄱ 판별 디딤돌 2",
                        "level_label_en": "Statement ㄱ Step 2",
                        "stem": r"$v(4) = 16 - 4(a+5) + 8 = 0$에서 $24 = 4(a+5)$가 됩니다. 상수 $a$의 값은?",
                        "stem_en": r"From $24 = 4(a+5)$, what is the value of $a$?",
                        "options": [r"$-1$", r"$0$", r"$1$", r"$2$", r"$3$"],
                        "answer": 3,
                        "exp": r"$a + 5 = 6$이므로 $a = 1$입니다. 따라서 <보기> ㄱ은 옳습니다!",
                        "exp_en": r"$a + 5 = 6 \implies a = 1$. Thus statement ㄱ is true."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [<보기> ㄴ 확인] 시각 $t = 3$일 때 점 P의 위치 구하기",
                "title_en": "🌱 Step 3 · [Statement ㄴ] Finding the position at $t = 3$",
                "knowledge": r"$a = 1$이므로 $v(t) = t^2 - 6t + 8$입니다. 원점 출발 시 시각 $t$에서의 위치는 $v(t)$를 적분한 $x(t) = \dfrac{1}{3}t^3 - 3t^2 + 8t$입니다.",
                "knowledge_en": r"Integrating $v(t) = t^2 - 6t + 8$ with $x(0) = 0$ gives the position $x(t) = \dfrac{1}{3}t^3 - 3t^2 + 8t$.",
                "questions": [
                    {
                        "level_label": "ㄴ 판별 디딤돌 3",
                        "level_label_en": "Statement ㄴ Step 3",
                        "stem": r"위치 식 $x(t) = \dfrac{1}{3}t^3 - 3t^2 + 8t$에 $t = 3$을 대입한 위치 $x(3)$의 값은?",
                        "stem_en": r"What is the position $x(3)$ when substituting $t = 3$ into $x(t) = \dfrac{1}{3}t^3 - 3t^2 + 8t$?",
                        "options": [r"$4$", r"$5$", r"$6$", r"$7$", r"$8$"],
                        "answer": 3,
                        "exp": r"$x(3) = \dfrac{1}{3}(27) - 3(9) + 8(3) = 9 - 27 + 24 = 6$입니다. 따라서 <보기> ㄴ도 옳습니다!",
                        "exp_en": r"$x(3) = 9 - 27 + 24 = 6$. Thus statement ㄴ is true."
                    }
                ]
            },
            {
                "title": "💎 4단계 · [<보기> ㄷ 확인] $t = 0$에서 $t = 4$까지 움직인 거리 구하기",
                "title_en": "💎 Step 4 · [Statement ㄷ] Total distance traveled from $t = 0$ to $t = 4$",
                "knowledge": r"$v(t) = (t-2)(t-4)$이므로 $0 \le t \le 2$에서는 앞으로 $\int_0^2 v(t)\,dt = \dfrac{20}{3}$만큼 가고, $2 \le t \le 4$에서는 뒤로 $\int_2^4 (-v(t))\,dt = \dfrac{4}{3}$만큼 갑니다.",
                "knowledge_en": r"Since $v(t) = (t-2)(t-4)$, the particle moves forward $\dfrac{20}{3}$ on $[0, 2]$ and backward $\dfrac{4}{3}$ on $[2, 4]$.",
                "questions": [
                    {
                        "level_label": "ㄷ 판별 및 종합 디딤돌 4",
                        "level_label_en": "Statement ㄷ Step 4",
                        "stem": r"움직인 거리는 $\dfrac{20}{3} + \dfrac{4}{3} = 8$이므로 ㄷ(움직인 거리는 10이다)은 거짓입니다. 따라서 <보기> 중 옳은 것만을 모두 고르면?",
                        "stem_en": r"Since the total distance is $\dfrac{20}{3} + \dfrac{4}{3} = 8 \neq 10$, statement ㄷ is false. Which statements are correct?",
                        "options": [r"ㄱ", r"ㄱ, ㄴ", r"ㄱ, ㄷ", r"ㄴ, ㄷ", r"ㄱ, ㄴ, ㄷ"],
                        "answer": 2,
                        "exp": r"ㄱ($a=1$)과 ㄴ($x(3)=6$)이 참이고 ㄷ(거리 $8 \neq 10$)은 거짓이므로 옳은 것은 ㄱ, ㄴ입니다.",
                        "exp_en": r"Statements ㄱ and ㄴ are true, while ㄷ is false."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"시각 $t = 0$일 때 원점을 출발하여 수직선 위를 움직이는 점 P가 있다. 실수 $a$에 대하여 시각이 $t$ ($t \ge 0$)일 때 점 P의 속도 $v(t)$가 $v(t) = t^2 - (a+5)t + 8$이다. 시각 $t = 4$에서 점 P의 운동 방향이 바뀔 때, <보기>에서 옳은 것만을 있는 대로 고른 것은? [4점]",
            "stem_en": r"A point P starts from the origin at $t = 0$ and moves along a number line with velocity $v(t) = t^2 - (a+5)t + 8$. Given that P changes direction at $t = 4$, which statements in <보기> are correct? [4 points]",
            "options": [r"ㄱ", r"ㄱ, ㄴ", r"ㄱ, ㄷ", r"ㄴ, ㄷ", r"ㄱ, ㄴ, ㄷ"],
            "answer": 2,
            "exp": r"ㄱ. $v(4)=0 \implies a=1$ (참). ㄴ. $x(3) = \int_0^3 (t^2-6t+8)dt = 6$ (참). ㄷ. 이동 거리는 $\int_0^2 v(t)dt - \int_2^4 v(t)dt = \frac{20}{3} + \frac{4}{3} = 8 \neq 10$ (거짓). 정답은 ②입니다.",
            "exp_en": r"ㄱ: $a = 1$ (True). ㄴ: $x(3) = 6$ (True). ㄷ: Total distance on $[0, 4]$ is $\frac{20}{3} + \frac{4}{3} = 8 \neq 10$ (False). The correct answer is ②.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 수직선 위를 움직이는 점의 <b>운동 방향 전환 조건($v(t)=0$ 및 부호 변화), 위치($\int v\,dt$), 움직인 거리($\int |v|\,dt$)</b>를 정확히 구분하여 계산할 수 있는지를 평가합니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>ㄱ. 상수 $a$의 값 결정 (참)</b><br>
  시각 $t = 4$에서 운동 방향이 바뀌므로 $v(4) = 0$이어야 합니다:<br>
  $$v(4) = 16 - 4(a+5) + 8 = 0 \implies 4(a+5) = 24 \implies a = 1$$<br>
  이때 $v(t) = t^2 - 6t + 8 = (t-2)(t-4)$이므로 ㄱ은 <b>참</b>입니다.<br><br>
  <b>ㄴ. 시각 $t = 3$일 때의 위치 (참)</b><br>
  원점 출발이므로 시각 $t$에서의 위치 $x(t)$는 다음과 같습니다:<br>
  $$x(t) = \int_0^t (s^2 - 6s + 8)\,ds = \frac{1}{3}t^3 - 3t^2 + 8t$$<br>
  $$x(3) = 9 - 27 + 24 = 6$$<br>
  따라서 ㄴ은 <b>참</b>입니다.<br><br>
  <b>ㄷ. 시각 $t = 0$에서 $t = 4$까지 움직인 거리 (거짓)</b><br>
  $v(t) = (t-2)(t-4)$는 $[0, 2]$에서 양수($\ge 0$), $[2, 4]$에서 음수($\le 0$)이므로 움직인 거리는:<br>
  $$\int_0^4 |v(t)|\,dt = \int_0^2 (t^2 - 6t + 8)\,dt + \int_2^4 (-t^2 + 6t - 8)\,dt = \frac{20}{3} + \frac{4}{3} = 8 \neq 10$$<br>
  따라서 ㄷ은 <b>거짓</b>입니다.
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  옳은 것은 ㄱ, ㄴ이므로 정답은 <b>②번</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates the distinction between <b>position (displacement) and total distance traveled</b> for a particle moving along a line.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Statement ㄱ (True):</b><br>
  Since P changes direction at $t = 4$, $v(4) = 16 - 4(a+5) + 8 = 0 \implies a = 1$.<br><br>
  <b>Statement ㄴ (True):</b><br>
  $$x(3) = \int_0^3 (t^2 - 6t + 8)\,dt = \left[\frac{1}{3}t^3 - 3t^2 + 8t\right]_0^3 = 9 - 27 + 24 = 6$$<br>
  <b>Statement ㄷ (False):</b><br>
  $$\int_0^4 |v(t)|\,dt = \int_0^2 v(t)\,dt - \int_2^4 v(t)\,dt = \frac{20}{3} + \frac{4}{3} = 8 \neq 10$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  Only statements ㄱ and ㄴ are correct, corresponding to <b>Option ②</b>.
</p>"""
        }
    }
]
