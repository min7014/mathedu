# -*- coding: utf-8 -*-
"""
oct2026_part3_prob.py
2026학년도 10월 고3 전국연합학력평가 (2027대비) 수학 [확률과 통계] 23번 ~ 30번
초등학생 눈높이 무장벽 디딤돌 5단계 퀴즈 및 상세 풀이 데이터
"""

PART3_PROBLEMS = [
    # -------------------------------------------------------------------------
    # 확통 23번: c2610p23
    # -------------------------------------------------------------------------
    {
        "slug": "c2610p23",
        "qNum": "확통 23",
        "subject": "확률과 통계",
        "title": "[2026학년도 10월 고3 확통 23번] 이항정리와 거듭제곱 전개식의 일반항 계수",
        "title_en": "[2026 AY Oct Exam Grade 12 Prob&Stats #23] Binomial Theorem and Coefficient in an Expansion",
        "summary_ko": "(2x^2 + 1/(2x))^6의 전개식에서 2x^2을 4번, 1/(2x)을 2번 뽑아 x^6의 계수 60 구하기",
        "summary_en": "Select 2x^2 four times and 1/(2x) twice in the expansion of (2x^2 + 1/(2x))^6 to find the coefficient 60 of x^6.",
        "tags": ["확률과 통계", "경우의수", "이항정리", "전개식의계수", "23번"],
        "symbols": [
            {"sym": r"${}_{6}\mathrm{C}_{r} (2x^2)^{6-r} \left(\dfrac{1}{2x}\right)^r$", "desc": "6개의 괄호 중 1/(2x)을 r개 골라 곱한 이항정리 일반항", "desc_en": "General term of the binomial expansion choosing 1/(2x) r times."},
            {"sym": r"$x^{12 - 3r} = x^6$", "desc": "x의 지수가 6이 되도록 하는 r=2 결정", "desc_en": "Equating the exponent of x to 6 gives r=2."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 구구단과 방정식] $12 - 3r = 6$을 만족하는 횟수 $r$ 찾기",
                "title_en": "🔰 Step 1 · [Elementary Multiplication & Subtraction] Solving $12 - 3r = 6$ for $r$",
                "knowledge": r"$6$개의 주머니에서 $x^2$을 $(6-r)$번 뽑고 $\frac{1}{x} = x^{-1}$을 $r$번 뽑으면 $x$의 지수는 $2(6-r) - r = 12 - 3r$이 됩니다. 초등학교 사칙연산으로 $12 - 3r = 6$이 되는 $r$을 찾아봅시다.",
                "knowledge_en": r"Using elementary arithmetic, choosing $x^2$ $(6-r)$ times and $x^{-1}$ $r$ times gives exponent $2(6-r) - r = 12 - 3r$. Set this equal to $6$.",
                "questions": [
                    {
                        "level_label": "초등 사칙연산 디딤돌 1",
                        "level_label_en": "Elementary Arithmetic Step 1",
                        "stem": r"초등학교 구구단과 뺄셈으로 $12 - 3r = 6$을 만족시키는 자연수 $r$의 값을 구하면?",
                        "stem_en": r"Using elementary arithmetic, what natural number $r$ satisfies $12 - 3r = 6$?",
                        "options": [r"$1$", r"$2$", r"$3$", r"$4$", r"$5$"],
                        "answer": 2,
                        "exp": r"$3r = 12 - 6 = 6$이므로 $r = 2$입니다.",
                        "exp_en": r"$3r = 6 \implies r = 2$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [조합 계산] $6$개 중 $2$개를 고르는 경우의 수 ${}_{6}\\mathrm{C}_{2}$ 구하기",
                "title_en": "🌿 Step 2 · [Combination] Computing ${}_{6}\\mathrm{C}_{2}$",
                "knowledge": r"${}_{6}\mathrm{C}_{2} = \frac{6 \times 5}{2 \times 1} = 15$입니다.",
                "knowledge_en": r"${}_{6}\mathrm{C}_{2} = \frac{6 \times 5}{2 \times 1} = 15$.",
                "questions": [
                    {
                        "level_label": "조합 계산 디딤돌 2",
                        "level_label_en": "Combination Step 2",
                        "stem": r"${}_{6}\mathrm{C}_{2} = \frac{6 \times 5}{2 \times 1}$의 값은?",
                        "stem_en": r"What is the value of ${}_{6}\mathrm{C}_{2} = \frac{6 \times 5}{2 \times 1}$?",
                        "options": [r"$10$", r"$12$", r"$15$", r"$20$", r"$30$"],
                        "answer": 3,
                        "exp": r"$\frac{30}{2} = 15$입니다.",
                        "exp_en": r"$\frac{30}{2} = 15$."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [거듭제곱 계산] $2^4 \\times \\left(\\dfrac{1}{2}\\right)^2$ 구하기",
                "title_en": "🌱 Step 3 · [Powers] Computing $2^4 \\times \\left(\\dfrac{1}{2}\\right)^2$",
                "knowledge": r"$r = 2$일 때 숫자 계수 부분은 $2^{6-2} \times \left(\frac{1}{2}\right)^2 = 2^4 \times \frac{1}{4} = \frac{16}{4} = 4$입니다.",
                "knowledge_en": r"At $r = 2$, the numerical factor is $2^4 \times \left(\frac{1}{2}\right)^2 = 16 \times \frac{1}{4} = 4$.",
                "questions": [
                    {
                        "level_label": "거듭제곱 약분 디딤돌 3",
                        "level_label_en": "Power Simplification Step 3",
                        "stem": r"$2^4 \times \left(\frac{1}{2}\right)^2 = 16 \times \frac{1}{4}$을 계산한 값은?",
                        "stem_en": r"What is $2^4 \times \left(\frac{1}{2}\right)^2 = 16 \times \frac{1}{4}$?",
                        "options": [r"$1$", r"$2$", r"$4$", r"$8$", r"$16$"],
                        "answer": 3,
                        "exp": r"$16 \div 4 = 4$입니다.",
                        "exp_en": r"$16 \div 4 = 4$."
                    }
                ]
            },
            {
                "title": "🌳 4단계 · [계수 결합 식] ${}_{6}\\mathrm{C}_{2}$와 숫자 거듭제곱 곱하기",
                "title_en": "🌳 Step 4 · [Combining Factors] Multiplying ${}_{6}\\mathrm{C}_{2}$ by $4$",
                "knowledge": r"$x^6$의 계수는 ${}_{6}\mathrm{C}_{2} \times 4 = 15 \times 4$입니다.",
                "knowledge_en": r"The coefficient of $x^6$ is ${}_{6}\mathrm{C}_{2} \times 4 = 15 \times 4$.",
                "questions": [
                    {
                        "level_label": "계수 곱셈식 디딤돌 4",
                        "level_label_en": "Coefficient Product Step 4",
                        "stem": r"$15 \times 4$를 $(10 + 5) \times 4 = 40 + k$로 계산할 때 $k$의 값은?",
                        "stem_en": r"When computing $15 \times 4 = (10 + 5) \times 4 = 40 + k$, what is $k$?",
                        "options": [r"$10$", r"$15$", r"$20$", r"$25$", r"$30$"],
                        "answer": 3,
                        "exp": r"$5 \times 4 = 20$이므로 $k = 20$입니다.",
                        "exp_en": r"$5 \times 4 = 20$."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [최종 종합] $x^6$의 계수 구하기",
                "title_en": "💎 Step 5 · [Final Synthesis] Final coefficient of $x^6$",
                "knowledge": r"$15 \times 4 = 60$으로 최종 계수를 구합니다.",
                "knowledge_en": r"$15 \times 4 = 60$.",
                "questions": [
                    {
                        "level_label": "최종 종합 디딤돌 5",
                        "level_label_en": "Final Synthesis Step 5",
                        "stem": r"$\left(2x^2 + \frac{1}{2x}\right)^6$의 전개식에서 $x^6$의 계수는?",
                        "stem_en": r"What is the coefficient of $x^6$ in the expansion of $\left(2x^2 + \frac{1}{2x}\right)^6$?",
                        "options": [r"$30$", r"$45$", r"$60$", r"$75$", r"$90$"],
                        "answer": 3,
                        "exp": r"${}_{6}\mathrm{C}_{2} \times 2^4 \times \left(\frac{1}{2}\right)^2 = 15 \times 4 = 60$이므로 정답은 ③입니다.",
                        "exp_en": r"${}_{6}\mathrm{C}_{2} \times 2^4 \times \left(\frac{1}{2}\right)^2 = 15 \times 4 = 60$ (choice ③)."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"$\left(2x^2 + \dfrac{1}{2x}\right)^6$의 전개식에서 $x^6$의 계수는? [2점]",
            "stem_en": r"What is the coefficient of $x^6$ in the expansion of $\left(2x^2 + \dfrac{1}{2x}\right)^6$? [2 points]",
            "options": [r"$30$", r"$45$", r"$60$", r"$75$", r"$90$"],
            "answer": 3,
            "exp": r"일반항 ${}_{6}\mathrm{C}_{r}(2x^2)^{6-r}\left(\dfrac{1}{2x}\right)^r = {}_{6}\mathrm{C}_{r}2^{6-2r}x^{12-3r}$에서 $12-3r=6 \implies r=2$이므로 계수는 ${}_{6}\mathrm{C}_{2}\times 2^2 = 15\times 4 = 60$입니다.",
            "exp_en": r"Setting $12 - 3r = 6$ in the general term ${}_{6}\mathrm{C}_{r}2^{6-2r}x^{12-3r}$ gives $r = 2$, so the coefficient is ${}_{6}\mathrm{C}_{2} \times 2^2 = 60$.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>이항정리의 일반항 공식</b>을 이용하여 특정 차수($x^6$)의 계수를 구하는 기본 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 이항정리의 일반항 구하기</b><br>
  $$\left(2x^2 + \frac{1}{2x}\right)^6\text{의 일반항은 } {}_{6}\mathrm{C}_{r} (2x^2)^{6-r} \left(\frac{1}{2x}\right)^r = {}_{6}\mathrm{C}_{r} 2^{6-2r} x^{12-3r}$$<br>
  <b>2단계: $x^6$이 되는 $r$의 값과 계수 계산</b><br>
  $12 - 3r = 6$에서 $r = 2$입니다. 이를 계수에 대입하면:<br>
  $${}_{6}\mathrm{C}_{2} \times 2^{6-4} = 15 \times 4 = 60$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 $x^6$의 계수는 $60$이므로 정답은 <b>③번</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem applies the <b>Binomial Theorem</b> to find the coefficient of $x^6$.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: General term</b><br>
  $${}_{6}\mathrm{C}_{r} (2x^2)^{6-r} \left(\frac{1}{2x}\right)^r = {}_{6}\mathrm{C}_{r} 2^{6-2r} x^{12-3r}$$<br>
  <b>Step 2: Solve for $r$ and evaluate</b><br>
  Setting $12 - 3r = 6 \implies r = 2$ gives ${}_{6}\mathrm{C}_{2} \times 2^2 = 15 \times 4 = 60$.
</p>

<h4>✨ [Final Answer & Practical Tips]</h4>
<p>
  The correct answer is <b>choice ③ ($60$)</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 확통 24번: c2610p24
    # -------------------------------------------------------------------------
    {
        "slug": "c2610p24",
        "qNum": "확통 24",
        "subject": "확률과 통계",
        "title": "[2026학년도 10월 고3 확통 24번] 이항분포의 평균과 분산으로 시행 횟수 n 구하기",
        "title_en": "[2026 AY Oct Exam Grade 12 Prob&Stats #24] Finding n from Mean and Variance of a Binomial Distribution",
        "summary_ko": "E(X)=np=5, V(X)=np(1-p)=4에서 1-p=4/5, p=1/5를 구하고 n=25 도출하기",
        "summary_en": "Divide V(X)=np(1-p)=4 by E(X)=np=5 to get 1-p=4/5, p=1/5, and n=25.",
        "tags": ["확률과 통계", "통계", "이항분포", "평균과분산", "표준편차", "24번"],
        "symbols": [
            {"sym": r"$\mathrm{E}(X) = np = 5$", "desc": "이항분포 B(n, p)의 평균", "desc_en": "Mean of binomial distribution B(n, p)."},
            {"sym": r"$\mathrm{V}(X) = \sigma(X)^2 = np(1-p) = 4$", "desc": "표준편차 2를 제곱한 분산", "desc_en": "Variance equals the square of the standard deviation 2."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 구구단 제곱] 표준편차가 $2$일 때 분산 $\\mathrm{V}(X)$ 구하기",
                "title_en": "🔰 Step 1 · [Elementary Multiplication] Finding variance $\\mathrm{V}(X)$ from $\\sigma(X) = 2$",
                "knowledge": r"통계에서 분산 $\mathrm{V}(X)$는 표준편차 $\sigma(X)$를 두 번 곱한(제곱한) 값입니다. 초등학교 구구단 $2 \times 2 = 4$로 분산을 바로 구할 수 있습니다.",
                "knowledge_en": r"By elementary multiplication, variance $\mathrm{V}(X)$ is the square of the standard deviation: $2 \times 2 = 4$.",
                "questions": [
                    {
                        "level_label": "초등 구구단 디딤돌 1",
                        "level_label_en": "Elementary Multiplication Step 1",
                        "stem": r"초등학교 구구단처럼 표준편차 $\sigma(X) = 2$를 제곱한 분산 $\mathrm{V}(X) = \{\sigma(X)\}^2$의 값은?",
                        "stem_en": r"Using elementary multiplication, if $\sigma(X) = 2$, what is the variance $\mathrm{V}(X) = \{\sigma(X)\}^2$?",
                        "options": [r"$2$", r"$4$", r"$6$", r"$8$", r"$10$"],
                        "answer": 2,
                        "exp": r"$\mathrm{V}(X) = 2^2 = 4$입니다.",
                        "exp_en": r"$\mathrm{V}(X) = 2^2 = 4$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [비율 계산] $np = 5$와 $np(1-p) = 4$에서 $1 - p$ 구하기",
                "title_en": "🌿 Step 2 · [Ratio] Finding $1 - p$ from $np = 5$ and $np(1-p) = 4$",
                "knowledge": r"$np(1-p) = 4$에서 앞의 $np$ 자리에 $5$를 넣으면 $5(1-p) = 4$가 됩니다.",
                "knowledge_en": r"Substituting $np = 5$ into $np(1-p) = 4$ gives $5(1-p) = 4$.",
                "questions": [
                    {
                        "level_label": "비율 나눗셈 디딤돌 2",
                        "level_label_en": "Ratio Division Step 2",
                        "stem": r"$5(1 - p) = 4$일 때, $1 - p$의 값은?",
                        "stem_en": r"Given $5(1 - p) = 4$, what is $1 - p$?",
                        "options": [r"$\frac{1}{5}$", r"$\frac{2}{5}$", r"$\frac{3}{5}$", r"$\frac{4}{5}$", r"$\frac{5}{4}$"],
                        "answer": 4,
                        "exp": r"양변을 $5$로 나누면 $1 - p = \frac{4}{5}$입니다.",
                        "exp_en": r"$1 - p = \frac{4}{5}$."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [분수 뺄셈] 성공 확률 $p$ 구하기",
                "title_en": "🌱 Step 3 · [Fraction Subtraction] Finding probability $p$",
                "knowledge": r"$1 - p = \frac{4}{5}$이므로 $p = 1 - \frac{4}{5} = \frac{1}{5}$입니다.",
                "knowledge_en": r"From $1 - p = \frac{4}{5}$, we have $p = 1 - \frac{4}{5} = \frac{1}{5}$.",
                "questions": [
                    {
                        "level_label": "확률 p 디딤돌 3",
                        "level_label_en": "Probability p Step 3",
                        "stem": r"$1 - p = \frac{4}{5}$일 때, 확률 $p$의 값은?",
                        "stem_en": r"Given $1 - p = \frac{4}{5}$, what is $p$?",
                        "options": [r"$\frac{1}{5}$", r"$\frac{1}{4}$", r"$\frac{2}{5}$", r"$\frac{3}{5}$", r"$\frac{4}{5}$"],
                        "answer": 1,
                        "exp": r"$p = 1 - \frac{4}{5} = \frac{1}{5}$입니다.",
                        "exp_en": r"$p = \frac{1}{5}$."
                    }
                ]
            },
            {
                "title": "🌳 4단계 · [평균 공식 대입] $n \\times \\dfrac{1}{5} = 5$ 세우기",
                "title_en": "🌳 Step 4 · [Mean Equation] Setting up $n \\times \\dfrac{1}{5} = 5$",
                "knowledge": r"$\mathrm{E}(X) = np = 5$에 $p = \frac{1}{5}$을 대입하면 $\frac{n}{5} = 5$가 됩니다.",
                "knowledge_en": r"Substituting $p = \frac{1}{5}$ into $np = 5$ gives $\frac{n}{5} = 5$.",
                "questions": [
                    {
                        "level_label": "시행 횟수 식 디딤돌 4",
                        "level_label_en": "Trials Equation Step 4",
                        "stem": r"$n$을 $5$로 나눈 값이 $5$일 때, $n$을 구하기 위해 해야 할 계산은?",
                        "stem_en": r"When $\frac{n}{5} = 5$, how do we compute $n$?",
                        "options": [r"$5 + 5$", r"$5 - 5$", r"$5 \times 5$", r"$5 \div 5$", r"$5 \times 4$"],
                        "answer": 3,
                        "exp": r"양변에 $5$를 곱하여 $n = 5 \times 5$를 계산합니다.",
                        "exp_en": r"Multiply both sides by $5$: $n = 5 \times 5$."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [최종 종합] 자연수 $n$의 값 구하기",
                "title_en": "💎 Step 5 · [Final Synthesis] Finding $n$",
                "knowledge": r"$n = 5 \times 5 = 25$로 정답을 확정합니다.",
                "knowledge_en": r"$n = 5 \times 5 = 25$.",
                "questions": [
                    {
                        "level_label": "최종 종합 디딤돌 5",
                        "level_label_en": "Final Synthesis Step 5",
                        "stem": r"이항분포 $\mathrm{B}(n, p)$에서 $\mathrm{E}(X) = 5$, $\sigma(X) = 2$일 때, $n$의 값은?",
                        "stem_en": r"For $X \sim \mathrm{B}(n, p)$ with $\mathrm{E}(X) = 5$ and $\sigma(X) = 2$, what is $n$?",
                        "options": [r"$25$", r"$30$", r"$35$", r"$40$", r"$45$"],
                        "answer": 1,
                        "exp": r"$n = 5 \times 5 = 25$이므로 정답은 ①입니다.",
                        "exp_en": r"$n = 25$ (choice ①)."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"이항분포 $\mathrm{B}(n, p)$를 따르는 확률변수 $X$에 대하여 $\mathrm{E}(X) = 5$, $\sigma(X) = 2$일 때, $n$의 값은? [3점]",
            "stem_en": r"For a random variable $X$ following the binomial distribution $\mathrm{B}(n, p)$, if $\mathrm{E}(X) = 5$ and $\sigma(X) = 2$, what is the value of $n$? [3 points]",
            "options": [r"$25$", r"$30$", r"$35$", r"$40$", r"$45$"],
            "answer": 1,
            "exp": r"$\mathrm{E}(X) = np = 5$, $\mathrm{V}(X) = np(1-p) = 4$에서 $1-p = \dfrac{4}{5} \implies p = \dfrac{1}{5}$이므로 $n = 25$입니다.",
            "exp_en": r"From $np = 5$ and $np(1-p) = 4$, we get $1-p = \dfrac{4}{5} \implies p = \dfrac{1}{5}$, so $n = 25$.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>이항분포 $\mathrm{B}(n, p)$의 평균 $\mathrm{E}(X) = np$와 분산 $\mathrm{V}(X) = np(1-p)$ 공식</b>을 연립하여 시행 횟수 $n$을 구하는 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 평균과 분산의 식 세우기</b><br>
  $$\mathrm{E}(X) = np = 5, \quad \mathrm{V}(X) = \{\sigma(X)\}^2 = 2^2 = 4 \implies np(1-p) = 4$$<br>
  <b>2단계: $p$와 $n$ 구하기</b><br>
  $5(1-p) = 4$에서 $1-p = \frac{4}{5} \implies p = \frac{1}{5}$입니다.<br>
  이를 $np = 5$에 대입하면 $\frac{1}{5}n = 5 \implies n = 25$입니다.
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 $n = 25$이므로 정답은 <b>①번</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem uses the formulas for the <b>mean and variance of a binomial distribution $\mathrm{B}(n, p)$</b>.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Relate mean and variance</b><br>
  $$\mathrm{E}(X) = np = 5, \quad \mathrm{V}(X) = np(1-p) = 2^2 = 4$$<br>
  <b>Step 2: Solve for $p$ and $n$</b><br>
  $$1 - p = \frac{4}{5} \implies p = \frac{1}{5} \implies n = \frac{5}{1/5} = 25$$
</p>

<h4>✨ [Final Answer & Practical Tips]</h4>
<p>
  The correct answer is <b>choice ① ($25$)</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 확통 25번: c2610p25
    # -------------------------------------------------------------------------
    {
        "slug": "c2610p25",
        "qNum": "확통 25",
        "subject": "확률과 통계",
        "title": "[2026학년도 10월 고3 확통 25번] 거듭제곱 항이 포함된 음이 아닌 정수해의 개수 (중복조합)",
        "title_en": "[2026 AY Oct Exam Grade 12 Prob&Stats #25] Number of Non-Negative Integer Solutions via Combinations with Repetition",
        "summary_ko": "d=0, 1, 2일 때로 케이스를 나누어 a+b+c=8-d^3의 중복조합 개수를 더해 82 구하기",
        "summary_en": "Split into cases d=0, 1, 2 and sum the combinations with repetition for a+b+c=8-d^3 to get 45+36+1=82.",
        "tags": ["확률과 통계", "경우의수", "중복조합", "음이아닌정수해", "케이스분류", "25번"],
        "symbols": [
            {"sym": r"$a + b + c = 8 - d^3$", "desc": "세제곱 항 d^3을 우변으로 넘겨 d의 값에 따라 분류", "desc_en": "Isolate a+b+c by moving d^3 to the right-hand side."},
            {"sym": r"${}_{3}\mathrm{H}_{k} = {}_{k+2}\mathrm{C}_{2}$", "desc": "음이 아닌 세 정수의 합이 k가 되는 중복조합 공식", "desc_en": "Number of non-negative integer triples summing to k."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 세제곱 계산] $d^3 \\le 8$이 되는 음이 아닌 정수 $d$ 찾기",
                "title_en": "🔰 Step 1 · [Elementary Cubing] Finding non-negative integers $d$ with $d^3 \\le 8$",
                "knowledge": r"초등학교 곱셈으로 똑같은 수를 세 번 곱해 봅시다: $0 \times 0 \times 0 = 0$, $1 \times 1 \times 1 = 1$, $2 \times 2 \times 2 = 8$, $3 \times 3 \times 3 = 27$. 합이 $8$이 되어야 하므로 $d^3$은 $8$을 넘을 수 없습니다!",
                "knowledge_en": r"By elementary multiplication: $0^3 = 0$, $1^3 = 1$, $2^3 = 8$, and $3^3 = 27 > 8$. Since $a, b, c \ge 0$, $d^3$ cannot exceed $8$.",
                "questions": [
                    {
                        "level_label": "초등 곱셈 디딤돌 1",
                        "level_label_en": "Elementary Multiplication Step 1",
                        "stem": r"초등학교 곱셈 규칙에 따라 음이 아닌 정수 $d$에 대하여 $d^3 \le 8$을 만족시키는 $d$의 값을 모두 고르면?",
                        "stem_en": r"Using elementary multiplication, which non-negative integers $d$ satisfy $d^3 \le 8$?",
                        "options": [r"$0,\ 1$", r"$1,\ 2$", r"$0,\ 1,\ 2$", r"$0,\ 1,\ 2,\ 3$", r"$1,\ 2,\ 3$"],
                        "answer": 3,
                        "exp": r"$0^3 = 0$, $1^3 = 1$, $2^3 = 8$이므로 가능한 $d$는 $0, 1, 2$의 $3$가지입니다.",
                        "exp_en": r"Since $0^3 = 0, 1^3 = 1, 2^3 = 8$, the valid values are $d \in \{0, 1, 2\}$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [경우 1: $d = 0$] $a + b + c = 8$의 해의 개수 구하기",
                "title_en": "🌿 Step 2 · [Case 1: $d = 0$] Solutions to $a + b + c = 8$",
                "knowledge": r"$d = 0$이면 $a + b + c = 8$이므로 중복조합 ${}_{3}\mathrm{H}_{8} = {}_{3+8-1}\mathrm{C}_{8} = {}_{10}\mathrm{C}_{2} = \frac{10 \times 9}{2} = 45$가지입니다.",
                "knowledge_en": r"When $d = 0$, $a + b + c = 8$, which has ${}_{3}\mathrm{H}_{8} = {}_{10}\mathrm{C}_{2} = 45$ solutions.",
                "questions": [
                    {
                        "level_label": "d=0 중복조합 디딤돌 2",
                        "level_label_en": "Case d=0 Step 2",
                        "stem": r"$d = 0$일 때 $a + b + c = 8$을 만족시키는 음이 아닌 정수해의 개수 ${}_{3}\mathrm{H}_{8} = {}_{10}\mathrm{C}_{2}$는?",
                        "stem_en": r"When $d = 0$, how many non-negative integer solutions does $a + b + c = 8$ have (${}_{3}\mathrm{H}_{8} = {}_{10}\mathrm{C}_{2}$)?",
                        "options": [r"$36$", r"$40$", r"$45$", r"$50$", r"$55$"],
                        "answer": 3,
                        "exp": r"${}_{10}\mathrm{C}_{2} = \frac{10 \times 9}{2 \times 1} = 45$입니다.",
                        "exp_en": r"${}_{10}\mathrm{C}_{2} = 45$."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [경우 2: $d = 1$] $a + b + c = 7$의 해의 개수 구하기",
                "title_en": "🌱 Step 3 · [Case 2: $d = 1$] Solutions to $a + b + c = 7$",
                "knowledge": r"$d = 1$이면 $a + b + c = 8 - 1 = 7$이므로 ${}_{3}\mathrm{H}_{7} = {}_{9}\mathrm{C}_{2} = \frac{9 \times 8}{2} = 36$가지입니다.",
                "knowledge_en": r"When $d = 1$, $a + b + c = 7$, which has ${}_{3}\mathrm{H}_{7} = {}_{9}\mathrm{C}_{2} = 36$ solutions.",
                "questions": [
                    {
                        "level_label": "d=1 중복조합 디딤돌 3",
                        "level_label_en": "Case d=1 Step 3",
                        "stem": r"$d = 1$일 때 $a + b + c = 7$을 만족시키는 음이 아닌 정수해의 개수 ${}_{3}\mathrm{H}_{7} = {}_{9}\mathrm{C}_{2}$는?",
                        "stem_en": r"When $d = 1$, what is ${}_{3}\mathrm{H}_{7} = {}_{9}\mathrm{C}_{2}$?",
                        "options": [r"$28$", r"$32$", r"$36$", r"$42$", r"$45$"],
                        "answer": 3,
                        "exp": r"${}_{9}\mathrm{C}_{2} = \frac{9 \times 8}{2 \times 1} = 36$입니다.",
                        "exp_en": r"${}_{9}\mathrm{C}_{2} = 36$."
                    }
                ]
            },
            {
                "title": "🌳 4단계 · [경우 3: $d = 2$] $a + b + c = 0$의 해의 개수 구하기",
                "title_en": "🌳 Step 4 · [Case 3: $d = 2$] Solutions to $a + b + c = 0$",
                "knowledge": r"$d = 2$이면 $d^3 = 8$이므로 $a + b + c = 8 - 8 = 0$입니다. 음이 아닌 세 정수의 합이 $0$이 되는 경우는 $(0, 0, 0)$ 딱 $1$가지뿐입니다.",
                "knowledge_en": r"When $d = 2$, $a + b + c = 0$, which has only $1$ solution: $(0, 0, 0)$.",
                "questions": [
                    {
                        "level_label": "d=2 해의 개수 디딤돌 4",
                        "level_label_en": "Case d=2 Step 4",
                        "stem": r"$d = 2$일 때 $a + b + c = 0$을 만족시키는 음이 아닌 정수 $(a, b, c)$의 순서쌍의 개수는?",
                        "stem_en": r"When $d = 2$, how many non-negative integer triples $(a, b, c)$ satisfy $a + b + c = 0$?",
                        "options": [r"$0$", r"$1$", r"$2$", r"$3$", r"$6$"],
                        "answer": 2,
                        "exp": r"$a = b = c = 0$인 $1$가지입니다.",
                        "exp_en": r"Only $(0, 0, 0)$, so $1$ solution."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [최종 종합] 세 경우의 수를 모두 더하기",
                "title_en": "💎 Step 5 · [Final Synthesis] Summing all three cases",
                "knowledge": r"$45 + 36 + 1$을 계산하면 전체 순서쌍의 개수가 완성됩니다.",
                "knowledge_en": r"Add $45 + 36 + 1 = 82$.",
                "questions": [
                    {
                        "level_label": "최종 종합 디딤돌 5",
                        "level_label_en": "Final Synthesis Step 5",
                        "stem": r"구한 세 경우의 수의 합 $45 + 36 + 1$은?",
                        "stem_en": r"What is the total number of solutions $45 + 36 + 1$?",
                        "options": [r"$80$", r"$82$", r"$84$", r"$86$", r"$88$"],
                        "answer": 2,
                        "exp": r"$45 + 36 + 1 = 82$이므로 정답은 ②입니다.",
                        "exp_en": r"$45 + 36 + 1 = 82$ (choice ②)."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"방정식 $a + b + c + d^3 = 8$을 만족시키는 음이 아닌 정수 $a, b, c, d$의 모든 순서쌍 $(a, b, c, d)$의 개수는? [3점]",
            "stem_en": r"How many ordered 4-tuples $(a, b, c, d)$ of non-negative integers satisfy $a + b + c + d^3 = 8$? [3 points]",
            "options": [r"$80$", r"$82$", r"$84$", r"$86$", r"$88$"],
            "answer": 2,
            "exp": r"$d = 0, 1, 2$일 때 $a+b+c = 8, 7, 0$이므로 순서쌍의 개수는 ${}_{3}\mathrm{H}_{8} + {}_{3}\mathrm{H}_{7} + {}_{3}\mathrm{H}_{0} = 45 + 36 + 1 = 82$입니다.",
            "exp_en": r"For $d = 0, 1, 2$, $a+b+c = 8, 7, 0$, giving ${}_{3}\mathrm{H}_{8} + {}_{3}\mathrm{H}_{7} + {}_{3}\mathrm{H}_{0} = 45 + 36 + 1 = 82$ solutions.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 계수나 차수가 다른 문자($d^3$)를 기준으로 케이스를 분류한 뒤 <b>중복조합(${}_{n}\mathrm{H}_{r}$)</b>을 적용하는 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 음이 아닌 정수 $d$의 값 분류</b><br>
  $a + b + c = 8 - d^3 \ge 0$이어야 하므로 $d^3 \le 8$, 즉 $d \in \{0, 1, 2\}$입니다.<br><br>
  <b>2단계: 각 경우의 중복조합 계산</b><br>
  - (i) $d = 0$일 때: $a + b + c = 8 \implies {}_{3}\mathrm{H}_{8} = {}_{10}\mathrm{C}_{8} = {}_{10}\mathrm{C}_{2} = 45$<br>
  - (ii) $d = 1$일 때: $a + b + c = 7 \implies {}_{3}\mathrm{H}_{7} = {}_{9}\mathrm{C}_{7} = {}_{9}\mathrm{C}_{2} = 36$<br>
  - (iii) $d = 2$일 때: $a + b + c = 0 \implies {}_{3}\mathrm{H}_{0} = 1$<br><br>
  <b>3단계: 합의 법칙 적용</b><br>
  $$45 + 36 + 1 = 82$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 모든 순서쌍의 개수는 $82$이므로 정답은 <b>②번</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem uses casework on the cubic term $d^3$ followed by <b>combinations with repetition (${}_{n}\mathrm{H}_{r}$)</b>.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Casework on $d \in \{0, 1, 2\}$</b><br>
  - $d = 0$: $a + b + c = 8 \implies {}_{3}\mathrm{H}_{8} = {}_{10}\mathrm{C}_{2} = 45$<br>
  - $d = 1$: $a + b + c = 7 \implies {}_{3}\mathrm{H}_{7} = {}_{9}\mathrm{C}_{2} = 36$<br>
  - $d = 2$: $a + b + c = 0 \implies {}_{3}\mathrm{H}_{0} = 1$<br><br>
  <b>Step 2: Total count</b><br>
  $$45 + 36 + 1 = 82$$
</p>

<h4>✨ [Final Answer & Practical Tips]</h4>
<p>
  The correct answer is <b>choice ② ($82$)</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 확통 26번: c2610p26
    # -------------------------------------------------------------------------
    {
        "slug": "c2610p26",
        "qNum": "확통 26",
        "subject": "확률과 통계",
        "title": "[2026학년도 10월 고3 확통 26번] 모평균의 신뢰구간 중심(표본평균)과 모표준편차 추론",
        "title_en": "[2026 AY Oct Exam Grade 12 Prob&Stats #26] Confidence Interval for Population Mean and Standard Deviation",
        "summary_ko": "신뢰구간의 중점(표본평균) 비교로 a=3을 구하고 반쪽 길이 1.96*(sigma/14)=1에서 sigma=50/7을 구해 a*sigma 도출하기",
        "summary_en": "Equate the midpoints (sample mean) to find a=3, and use the half-width 1.96*(sigma/14)=1 to find sigma=50/7 and a*sigma=150/7.",
        "tags": ["확률과 통계", "통계", "통계적추정", "모평균의신뢰구간", "표본평균", "26번"],
        "symbols": [
            {"sym": r"$\bar{x} = \dfrac{\text{양 끝점의 합}}{2}$", "desc": "모평균 신뢰구간의 한가운데 값은 항상 표본평균 bar{x}", "desc_en": "The midpoint of a confidence interval is always the sample mean."},
            {"sym": r"$1.96 \times \dfrac{\sigma}{\sqrt{n}}$", "desc": "신뢰도 95% 신뢰구간의 중심에서 양 끝까지의 반쪽 길이(오차한계)", "desc_en": "Margin of error (half-width) for a 95% confidence interval."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 평균 구하기] 신뢰구간 양 끝점의 한가운데 값 비교하기",
                "title_en": "🔰 Step 1 · [Elementary Average] Finding the midpoint of the confidence interval",
                "knowledge": r"초등학교에서 두 수 $a + 82$와 $a + 84$의 한가운데(평균)는 $a + 83$입니다. 이 한가운데 값이 바로 표본평균 $\bar{x} = 2a + 80$과 같아야 합니다!",
                "knowledge_en": r"By elementary averaging, the midpoint between $a + 82$ and $a + 84$ is $a + 83$, which must equal the sample mean $\bar{x} = 2a + 80$.",
                "questions": [
                    {
                        "level_label": "초등 평균 비교 디딤돌 1",
                        "level_label_en": "Elementary Midpoint Step 1",
                        "stem": r"초등학교 평균 계산처럼 구간 $[a + 82, a + 84]$의 한가운데 값 $a + 83$이 표본평균 $2a + 80$과 같을 때($a + 83 = 2a + 80$), 상수 $a$의 값은?",
                        "stem_en": r"Using elementary arithmetic, if the midpoint $a + 83$ equals the sample mean $2a + 80$, what is $a$?",
                        "options": [r"$1$", r"$2$", r"$3$", r"$4$", r"$5$"],
                        "answer": 3,
                        "exp": r"$a + 83 = 2a + 80 \implies a = 83 - 80 = 3$입니다.",
                        "exp_en": r"$a = 83 - 80 = 3$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [오차한계 확인] 중심에서 오른쪽 끝까지의 반쪽 길이 구하기",
                "title_en": "🌿 Step 2 · [Margin of Error] Half-width of the confidence interval",
                "knowledge": r"구간 $[a + 82, a + 84]$의 중심 $a + 83$에서 오른쪽 끝 $a + 84$까지의 거리는 $(a + 84) - (a + 83) = 1$입니다.",
                "knowledge_en": r"The half-width from the center $a + 83$ to the upper bound $a + 84$ is $1$.",
                "questions": [
                    {
                        "level_label": "반쪽 길이 디딤돌 2",
                        "level_label_en": "Half-Width Step 2",
                        "stem": r"표본의 크기 $n = 196$일 때 $\sqrt{n} = \sqrt{196} = 14$입니다. 신뢰도 $95\%$($z = 1.96$)에서의 반쪽 길이 $1.96 \times \frac{\sigma}{14} = 1$에서 $\frac{1.96}{14}$을 소수로 계산하면?",
                        "stem_en": r"With $\sqrt{196} = 14$, what is $\frac{1.96}{14}$ in decimal form?",
                        "options": [r"$0.12$", r"$0.14$", r"$0.16$", r"$0.18$", r"$0.20$"],
                        "answer": 2,
                        "exp": r"$1.96 \div 14 = 0.14$입니다.",
                        "exp_en": r"$1.96 \div 14 = 0.14$."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [분수 변환] $0.14 \\sigma = 1$에서 모표준편차 $\\sigma$ 구하기",
                "title_en": "🌱 Step 3 · [Fraction Conversion] Solving $0.14\\sigma = 1$ for $\\sigma$",
                "knowledge": r"$0.14 = \frac{14}{100} = \frac{7}{50}$이므로 $\frac{7}{50}\sigma = 1 \implies \sigma = \frac{50}{7}$입니다.",
                "knowledge_en": r"Since $0.14 = \frac{7}{50}$, $\frac{7}{50}\sigma = 1 \implies \sigma = \frac{50}{7}$.",
                "questions": [
                    {
                        "level_label": "표준편차 sigma 디딤돌 3",
                        "level_label_en": "Finding sigma Step 3",
                        "stem": r"$\frac{7}{50}\sigma = 1$일 때, 모표준편차 $\sigma$의 값은?",
                        "stem_en": r"From $\frac{7}{50}\sigma = 1$, what is $\sigma$?",
                        "options": [r"$\frac{30}{7}$", r"$\frac{40}{7}$", r"$\frac{50}{7}$", r"$\frac{60}{7}$", r"$10$"],
                        "answer": 3,
                        "exp": r"역수를 곱하면 $\sigma = \frac{50}{7}$입니다.",
                        "exp_en": r"$\sigma = \frac{50}{7}$."
                    }
                ]
            },
            {
                "title": "🌳 4단계 · [분자 곱셈] $a = 3$과 분자 $50$ 곱하기",
                "title_en": "🌳 Step 4 · [Numerator Product] Multiplying $a = 3$ and $50$",
                "knowledge": r"$a\sigma = 3 \times \frac{50}{7}$에서 분자는 $3 \times 50 = 150$입니다.",
                "knowledge_en": r"In $a\sigma = 3 \times \frac{50}{7}$, the numerator is $3 \times 50 = 150$.",
                "questions": [
                    {
                        "level_label": "분자 계산 디딤돌 4",
                        "level_label_en": "Numerator Step 4",
                        "stem": r"$3 \times 50$의 값은?",
                        "stem_en": r"What is $3 \times 50$?",
                        "options": [r"$100$", r"$120$", r"$150$", r"$180$", r"$200$"],
                        "answer": 3,
                        "exp": r"$3 \times 50 = 150$입니다.",
                        "exp_en": r"$3 \times 50 = 150$."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [최종 종합] $a\\sigma$의 값 구하기",
                "title_en": "💎 Step 5 · [Final Synthesis] Final value of $a\\sigma$",
                "knowledge": r"$a\sigma = \frac{150}{7}$로 정답을 확정합니다.",
                "knowledge_en": r"$a\sigma = \frac{150}{7}$.",
                "questions": [
                    {
                        "level_label": "최종 종합 디딤돌 5",
                        "level_label_en": "Final Synthesis Step 5",
                        "stem": r"$a = 3$, $\sigma = \frac{50}{7}$일 때, $a\sigma$의 값은?",
                        "stem_en": r"Given $a = 3$ and $\sigma = \frac{50}{7}$, what is $a\sigma$?",
                        "options": [r"$\frac{135}{7}$", r"$\frac{140}{7}$", r"$\frac{145}{7}$", r"$\frac{150}{7}$", r"$\frac{155}{7}$"],
                        "answer": 4,
                        "exp": r"$a\sigma = 3 \times \frac{50}{7} = \frac{150}{7}$이므로 정답은 ④입니다.",
                        "exp_en": r"$a\sigma = \frac{150}{7}$ (choice ④)."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"모평균이 $m$, 모표준편차가 $\sigma$인 정규분포를 따르는 모집단에서 크기가 $196$인 표본을 이미추출하여 구한 표본평균이 $2a + 80$일 때, 모평균 $m$에 대한 신뢰도 $95\%$의 신뢰구간이 $a + 82 \le m \le a + 84$이다. $a\sigma$의 값은? (단, $Z$가 표준정규분포를 따르는 확률변수일 때, $\mathrm{P}(|Z| \le 1.96) = 0.95$로 계산한다.) [3점]",
            "stem_en": r"A random sample of size $196$ from a normal population with mean $m$ and standard deviation $\sigma$ yields a sample mean of $2a + 80$ and a $95\%$ confidence interval $a + 82 \le m \le a + 84$. What is the value of $a\sigma$? (Use $\mathrm{P}(|Z| \le 1.96) = 0.95$.) [3 points]",
            "options": [r"$\dfrac{135}{7}$", r"$\dfrac{140}{7}$", r"$\dfrac{145}{7}$", r"$\dfrac{150}{7}$", r"$\dfrac{155}{7}$"],
            "answer": 4,
            "exp": r"신뢰구간의 중점 $a + 83 = 2a + 80$에서 $a = 3$이고, $1.96 \times \dfrac{\sigma}{14} = 1$에서 $\sigma = \dfrac{50}{7}$이므로 $a\sigma = \dfrac{150}{7}$입니다.",
            "exp_en": r"Equating the midpoint $a + 83 = 2a + 80$ gives $a = 3$, and $1.96 \times \dfrac{\sigma}{14} = 1$ gives $\sigma = \dfrac{50}{7}$, so $a\sigma = \dfrac{150}{7}$.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>모평균 $m$의 신뢰구간의 중점이 표본평균 $\bar{x}$</b>이고, <b>구간의 반쪽 길이가 $1.96 \frac{\sigma}{\sqrt{n}}$</b>임을 이용하여 미지수를 구하는 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 신뢰구간의 중점으로 $a$ 구하기</b><br>
  신뢰구간 $[a + 82, a + 84]$의 중점은 표본평균 $\bar{x} = 2a + 80$과 같으므로:<br>
  $$\frac{(a + 82) + (a + 84)}{2} = a + 83 = 2a + 80 \implies a = 3$$<br>
  <b>2단계: 신뢰구간의 반쪽 길이로 $\sigma$ 구하기</b><br>
  구간의 반쪽 길이는 $(a + 84) - (a + 83) = 1$이고 $\sqrt{n} = \sqrt{196} = 14$이므로:<br>
  $$1.96 \times \frac{\sigma}{14} = 1 \implies 0.14\sigma = 1 \implies \sigma = \frac{100}{14} = \frac{50}{7}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 $a\sigma = 3 \times \dfrac{50}{7} = \dfrac{150}{7}$이므로 정답은 <b>④번</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem uses the <b>midpoint and margin of error of a $95\%$ confidence interval</b> for the population mean.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Midpoint equals sample mean</b><br>
  $$a + 83 = 2a + 80 \implies a = 3$$<br>
  <b>Step 2: Half-width equals margin of error</b><br>
  $$1.96 \times \frac{\sigma}{\sqrt{196}} = 0.14\sigma = 1 \implies \sigma = \frac{50}{7}$$
</p>

<h4>✨ [Final Answer & Practical Tips]</h4>
<p>
  Thus $a\sigma = \dfrac{150}{7}$, which corresponds to <b>choice ④</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 확통 27번: c2610p27
    # -------------------------------------------------------------------------
    {
        "slug": "c2610p27",
        "qNum": "확통 27",
        "subject": "확률과 통계",
        "title": "[2026학년도 10월 고3 확통 27번] 두 눈의 수의 곱의 홀짝에 따른 독립시행의 확률",
        "title_en": "[2026 AY Oct Exam Grade 12 Prob&Stats #27] Independent Trials Based on Parity of Product of Two Dice",
        "summary_ko": "1회 시행에서 공을 1개 넣을 확률 1/4, 2개 넣을 확률 3/4을 구하고 4회 시행 후 공이 5개 이하일 확률 13/256 도출하기",
        "summary_en": "Find P(1 ball)=1/4 and P(2 balls)=3/4 per trial, then compute the probability of at most 5 balls in 4 trials as 13/256.",
        "tags": ["확률과 통계", "확률", "독립시행의확률", "주사위의곱", "여사건", "27번"],
        "symbols": [
            {"sym": r"$\text{홀수} \times \text{홀수} = \text{홀수}$", "desc": "두 눈의 곱이 홀수가 되어 공을 1개 넣을 확률 1/2 * 1/2 = 1/4", "desc_en": "Product is odd (1 ball added) iff both dice are odd: probability 1/4."},
            {"sym": r"$4\text{번 모두 } 1\text{개 또는 } 3\text{번 } 1\text{개} + 1\text{번 } 2\text{개}$", "desc": "4번 시행 후 공의 총합이 4개 또는 5개(5개 이하)가 되는 조건", "desc_en": "Total balls <= 5 in 4 trials means either four 1s (sum 4) or three 1s and one 2 (sum 5)."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 홀짝 곱셈] 두 수의 곱이 홀수가 될 조건과 확률 구하기",
                "title_en": "🔰 Step 1 · [Elementary Odd/Even Multiplication] Probability that the product of two dice is odd",
                "knowledge": r"초등학교 홀짝 곱셈에서 두 수를 곱해 홀수가 되려면 두 수 모두 홀수여야 합니다! 주사위 한 개에서 홀수($1, 3, 5$)가 나올 확률은 $\frac{3}{6} = \frac{1}{2}$이므로, 두 주사위 모두 홀수가 나와 공을 $1$개 넣을 확률은 $\frac{1}{2} \times \frac{1}{2} = \frac{1}{4}$입니다.",
                "knowledge_en": r"By elementary odd/even multiplication, a product of two integers is odd if and only if both are odd. Since each die is odd with probability $\frac{1}{2}$, the probability of adding $1$ ball is $\frac{1}{2} \times \frac{1}{2} = \frac{1}{4}$.",
                "questions": [
                    {
                        "level_label": "초등 홀짝 확률 디딤돌 1",
                        "level_label_en": "Elementary Parity Step 1",
                        "stem": r"초등학교 홀짝 규칙에 따라 한 번의 시행에서 공을 $1$개 넣을(곱이 홀수일) 확률이 $\frac{1}{4}$이면, 공을 $2$개 넣을(곱이 짝수일) 확률은?",
                        "stem_en": r"Using elementary probability subtraction, if the probability of adding $1$ ball is $\frac{1}{4}$, what is the probability of adding $2$ balls?",
                        "options": [r"$\frac{1}{4}$", r"$\frac{1}{2}$", r"$\frac{2}{3}$", r"$\frac{3}{4}$", r"$\frac{5}{6}$"],
                        "answer": 4,
                        "exp": r"$1 - \frac{1}{4} = \frac{3}{4}$입니다.",
                        "exp_en": r"$1 - \frac{1}{4} = \frac{3}{4}$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [개수 합 분석] $4$번 시행 후 공이 $5$개 이하가 되는 경우 찾기",
                "title_en": "🌿 Step 2 · [Sum of Balls] Cases where 4 trials yield at most 5 balls",
                "knowledge": r"매번 최소 $1$개씩 넣으므로 $4$번 시행하면 최소 $4$개가 들어갑니다. 총 $5$개 이하가 되려면 총합이 $4$개($1$개씩 $4$번)이거나 총합이 $5$개($1$개씩 $3$번, $2$개 $1$번)여야 합니다.",
                "knowledge_en": r"In $4$ trials, adding $1$ or $2$ balls each time gives a total $\le 5$ iff the total is $4$ (four $1$s) or $5$ (three $1$s and one $2$).",
                "questions": [
                    {
                        "level_label": "총합 4개 확률 디딤돌 2",
                        "level_label_en": "Sum=4 Probability Step 2",
                        "stem": r"$4$번 모두 공을 $1$개씩 넣어 총 $4$개가 될 확률 $\left(\frac{1}{4}\right)^4$의 값은?",
                        "stem_en": r"What is the probability $\left(\frac{1}{4}\right)^4$ of adding $1$ ball in all $4$ trials?",
                        "options": [r"$\frac{1}{16}$", r"$\frac{1}{64}$", r"$\frac{1}{128}$", r"$\frac{1}{256}$", r"$\frac{1}{512}$"],
                        "answer": 4,
                        "exp": r"$4^4 = 16 \times 16 = 256$이므로 $\frac{1}{256}$입니다.",
                        "exp_en": r"$\left(\frac{1}{4}\right)^4 = \frac{1}{256}$."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [독립시행 확률] 공이 총 $5$개가 될 확률 구하기",
                "title_en": "🌱 Step 3 · [Independent Trials] Probability that the total is $5$ balls",
                "knowledge": r"$4$번 중 $3$번은 $1$개(확률 $\frac{1}{4}$), $1$번은 $2$개(확률 $\frac{3}{4}$)를 넣을 확률은 ${}_{4}\mathrm{C}_{3}\left(\frac{1}{4}\right)^3\left(\frac{3}{4}\right) = 4 \times \frac{3}{256} = \frac{12}{256}$입니다.",
                "knowledge_en": r"The probability of three $1$s and one $2$ is ${}_{4}\mathrm{C}_{3}\left(\frac{1}{4}\right)^3\left(\frac{3}{4}\right) = \frac{12}{256}$.",
                "questions": [
                    {
                        "level_label": "총합 5개 분자 디딤돌 3",
                        "level_label_en": "Sum=5 Numerator Step 3",
                        "stem": r"${}_{4}\mathrm{C}_{3}\left(\frac{1}{4}\right)^3\left(\frac{3}{4}\right) = \frac{k}{256}$에서 분자 $k = 4 \times 3$의 값은?",
                        "stem_en": r"In ${}_{4}\mathrm{C}_{3}\left(\frac{1}{4}\right)^3\left(\frac{3}{4}\right) = \frac{k}{256}$, what is the numerator $k = 4 \times 3$?",
                        "options": [r"$4$", r"$8$", r"$12$", r"$16$", r"$24$"],
                        "answer": 3,
                        "exp": r"$4 \times 3 = 12$입니다.",
                        "exp_en": r"$4 \times 3 = 12$."
                    }
                ]
            },
            {
                "title": "🌳 4단계 · [분자 덧셈] 두 경우의 확률 분자끼리 더하기",
                "title_en": "🌳 Step 4 · [Adding Numerators] Adding $1 + 12$",
                "knowledge": r"총 $4$개일 확률 $\frac{1}{256}$과 총 $5$개일 확률 $\frac{12}{256}$을 더합니다.",
                "knowledge_en": r"Add $\frac{1}{256}$ and $\frac{12}{256}$.",
                "questions": [
                    {
                        "level_label": "분자 합산 디딤돌 4",
                        "level_label_en": "Numerator Sum Step 4",
                        "stem": r"분모가 $256$으로 같을 때 두 분자의 합 $1 + 12$는?",
                        "stem_en": r"What is the sum of the numerators $1 + 12$?",
                        "options": [r"$9$", r"$11$", r"$13$", r"$15$", r"$17$"],
                        "answer": 3,
                        "exp": r"$1 + 12 = 13$입니다.",
                        "exp_en": r"$1 + 12 = 13$."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [최종 종합] 공의 개수가 $5$ 이하일 확률 구하기",
                "title_en": "💎 Step 5 · [Final Synthesis] Final probability",
                "knowledge": r"구하는 확률은 $\frac{13}{256}$입니다.",
                "knowledge_en": r"The final probability is $\frac{13}{256}$.",
                "questions": [
                    {
                        "level_label": "최종 종합 디딤돌 5",
                        "level_label_en": "Final Synthesis Step 5",
                        "stem": r"이 시행을 $4$번 반복한 후 상자에 들어 있는 공의 개수가 $5$ 이하일 확률은?",
                        "stem_en": r"What is the probability that the box contains at most $5$ balls after $4$ trials?",
                        "options": [r"$\frac{5}{256}$", r"$\frac{7}{256}$", r"$\frac{9}{256}$", r"$\frac{11}{256}$", r"$\frac{13}{256}$"],
                        "answer": 5,
                        "exp": r"$\frac{1}{256} + \frac{12}{256} = \frac{13}{256}$이므로 정답은 ⑤입니다.",
                        "exp_en": r"$\frac{13}{256}$ (choice ⑤)."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"한 개의 주사위를 두 번 던져 나오는 눈의 수의 곱이 홀수이면 빈 상자에 공을 $1$개 넣고, 짝수이면 공을 $2$개 넣는 시행을 한다. 이 시행을 $4$번 반복한 후 상자에 들어 있는 공의 개수가 $5$ 이하일 확률은? [3점]",
            "stem_en": r"A die is rolled twice: if the product of the outcomes is odd, $1$ ball is placed into an empty box; if even, $2$ balls are placed. After repeating this trial $4$ times, what is the probability that the box contains at most $5$ balls? [3 points]",
            "options": [r"$\dfrac{5}{256}$", r"$\dfrac{7}{256}$", r"$\dfrac{9}{256}$", r"$\dfrac{11}{256}$", r"$\dfrac{13}{256}$"],
            "answer": 5,
            "exp": r"1회 시행에서 공을 $1$개 넣을 확률은 $\dfrac{1}{4}$, $2$개 넣을 확률은 $\dfrac{3}{4}$입니다. $4$회 시행 후 공이 $4$개 또는 $5$개일 확률은 $\left(\dfrac{1}{4}\right)^4 + {}_{4}\mathrm{C}_{1}\left(\dfrac{3}{4}\right)\left(\dfrac{1}{4}\right)^3 = \dfrac{13}{256}$입니다.",
            "exp_en": r"Each trial adds $1$ ball with probability $\dfrac{1}{4}$ and $2$ balls with probability $\dfrac{3}{4}$. The probability of $\le 5$ balls in $4$ trials is $\left(\dfrac{1}{4}\right)^4 + 4\left(\dfrac{3}{4}\right)\left(\dfrac{1}{4}\right)^3 = \dfrac{13}{256}$.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>주사위 두 눈의 곱의 홀짝 확률</b>과 <b>독립시행의 확률</b>을 결합한 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 1회 시행에서 공을 $1$개 또는 $2$개 넣을 확률</b><br>
  주사위를 두 번 던져 나온 눈의 수의 곱이 홀수이려면 두 번 모두 홀수가 나와야 하므로:<br>
  $$P(\text{공 } 1\text{개}) = \frac{1}{2} \times \frac{1}{2} = \frac{1}{4}, \quad P(\text{공 } 2\text{개}) = 1 - \frac{1}{4} = \frac{3}{4}$$<br>
  <b>2단계: $4$회 시행 후 공의 개수가 $5$ 이하일 확률</b><br>
  공의 개수가 $5$ 이하인 경우는 총 $4$개($1$개씩 $4$번) 또는 총 $5$개($1$개씩 $3$번, $2$개 $1$번)일 때이므로:<br>
  $${}_{4}\mathrm{C}_{4}\left(\frac{1}{4}\right)^4 + {}_{4}\mathrm{C}_{3}\left(\frac{1}{4}\right)^3\left(\frac{3}{4}\right) = \frac{1}{256} + \frac{12}{256} = \frac{13}{256}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 구하는 확률은 $\dfrac{13}{256}$이므로 정답은 <b>⑤번</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem combines <b>parity probability for two dice</b> with <b>independent Bernoulli trials</b>.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Single-trial probabilities</b><br>
  $$P(1\text{ ball}) = \left(\frac{1}{2}\right)^2 = \frac{1}{4}, \quad P(2\text{ balls}) = \frac{3}{4}$$<br>
  <b>Step 2: At most $5$ balls in $4$ trials</b><br>
  $$\left(\frac{1}{4}\right)^4 + {}_{4}\mathrm{C}_{1}\left(\frac{3}{4}\right)\left(\frac{1}{4}\right)^3 = \frac{1 + 12}{256} = \frac{13}{256}$$
</p>

<h4>✨ [Final Answer & Practical Tips]</h4>
<p>
  The correct answer is <b>choice ⑤ ($\dfrac{13}{256}$)</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 확통 28번: c2610p28
    # -------------------------------------------------------------------------
    {
        "slug": "c2610p28",
        "qNum": "확통 28",
        "subject": "확률과 통계",
        "title": "[2026학년도 10월 고3 확통 28번] 같은 숫자가 적힌 카드의 선택과 같은 것이 있는 순열",
        "title_en": "[2026 AY Oct Exam Grade 12 Prob&Stats #28] Card Selection and Permutations with Identical Items",
        "summary_ko": "첫째 자리에 짝수(2 또는 4)를 놓은 뒤 나머지 5자리에 들어갈 숫자의 쌍 개수에 따라 케이스를 나누어 2*360=720 구하기",
        "summary_en": "Fix the first digit as even (2 choices: 2 or 4), classify the remaining 5 digits by identical pairs, and compute 2*360=720.",
        "tags": ["확률과 통계", "경우의수", "같은것이있는순열", "케이스분류", "28번"],
        "symbols": [
            {"sym": r"$\{1, 1, 2, 2, 3, 3, 4, 4\}$", "desc": "1, 2, 3, 4가 각각 2장씩 들어 있는 총 8장의 카드", "desc_en": "Eight cards consisting of two each of 1, 2, 3, and 4."},
            {"sym": r"$\dfrac{5!}{2!2!} = 30,\quad \dfrac{5!}{2!} = 60$", "desc": "나머지 5개의 자리에 같은 숫자가 2쌍 또는 1쌍 있을 때의 나열 수", "desc_en": "Permutations of 5 positions with two pairs (30) or one pair (60)."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 짝수 고르기] 첫 번째 자리에 올 수 있는 짝수 종류 세기",
                "title_en": "🔰 Step 1 · [Elementary Even Numbers] Counting choices for the first even digit",
                "knowledge": r"숫자 $1, 2, 3, 4$ 중에서 초등학교에서 배운 짝수는 $2$와 $4$ 두 가지입니다! 같은 숫자가 적힌 카드끼리는 구별하지 않으므로, 맨 앞자리에 놓을 수 있는 숫자는 $2$ 또는 $4$의 $2$가지입니다.",
                "knowledge_en": r"Among $1, 2, 3, 4$, the elementary even numbers are $2$ and $4$. Since identical digits are indistinguishable, there are $2$ choices for the first position.",
                "questions": [
                    {
                        "level_label": "초등 짝수 선택 디딤돌 1",
                        "level_label_en": "Elementary Even Choice Step 1",
                        "stem": r"초등학교 짝수 개념에 따라 첫 번째 자리에 놓을 수 있는 짝수($2$ 또는 $4$)의 선택 가짓수는?",
                        "stem_en": r"Using elementary even numbers, how many choices are there for the even digit ($2$ or $4$) in the first position?",
                        "options": [r"$1$", r"$2$", r"$3$", r"$4$", r"$6$"],
                        "answer": 2,
                        "exp": r"$2$ 또는 $4$이므로 $2$가지입니다. (맨 앞자리를 $2$로 고정해 구한 뒤 $2$배 하면 됩니다!)",
                        "exp_en": r"There are $2$ choices ($2$ or $4$)."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [경우 1] 맨 앞이 $2$이고 나머지 $5$자리에 $2$가 안 쓰이는 경우",
                "title_en": "🌿 Step 2 · [Case 1] First digit is $2$, and the other $2$ is not used in the remaining $5$ positions",
                "knowledge": r"맨 앞에 $2$를 $1$장 썼을 때, 남은 카드 중 $2$를 빼고 $\{1, 1, 3, 3, 4, 4\}$ $6$장 중에서 $5$장을 골라 나열합니다. $1, 3, 4$ 중 $2$종류는 $2$장씩, $1$종류는 $1$장 쓰이므로 ${}_{3}\mathrm{C}_{1} \times \frac{5!}{2!2!} = 3 \times 30 = 90$가지입니다.",
                "knowledge_en": r"If the second $2$ is not used, we pick $5$ cards from $\{1, 1, 3, 3, 4, 4\}$ (two pairs and one single): $3 \times \frac{5!}{2!2!} = 3 \times 30 = 90$ ways.",
                "questions": [
                    {
                        "level_label": "경우 1 나열 디딤돌 2",
                        "level_label_en": "Case 1 Permutation Step 2",
                        "stem": r"$3 \times \frac{5!}{2!2!} = 3 \times 30$을 계산한 값은?",
                        "stem_en": r"What is the value of $3 \times \frac{5!}{2!2!} = 3 \times 30$?",
                        "options": [r"$60$", r"$90$", r"$120$", r"$150$", r"$180$"],
                        "answer": 2,
                        "exp": r"$3 \times 30 = 90$입니다.",
                        "exp_en": r"$3 \times 30 = 90$."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [경우 2] 나머지 $5$자리에 남은 $2$가 $1$장 포함되는 경우",
                "title_en": "🌱 Step 3 · [Case 2] The remaining $2$ is included among the other $5$ positions",
                "knowledge": r"남은 $2$ 한 장을 포함하면, 나머지 $4$자리는 $\{1, 1, 3, 3, 4, 4\}$에서 $4$장을 골라야 합니다. (a) 두 쌍(예: $1,1,3,3$)을 고르면 ${}_{3}\mathrm{C}_{2} \times \frac{5!}{2!2!} = 3 \times 30 = 90$가지이고, (b) 한 쌍과 단짝 두 개(예: $1,1,3,4$)를 고르면 ${}_{3}\mathrm{C}_{1} \times \frac{5!}{2!} = 3 \times 60 = 180$가지입니다.",
                "knowledge_en": r"If the second $2$ is used, the other $4$ cards from $\{1,1,3,3,4,4\}$ can be: (a) two pairs: ${}_{3}\mathrm{C}_{2} \times \frac{5!}{2!2!} = 90$, or (b) one pair and two singles: ${}_{3}\mathrm{C}_{1} \times \frac{5!}{2!} = 180$.",
                "questions": [
                    {
                        "level_label": "경우 2 합산 디딤돌 3",
                        "level_label_en": "Case 2 Sum Step 3",
                        "stem": r"나머지 $5$자리에 $2$가 포함되는 경우의 수 $90 + 180$은?",
                        "stem_en": r"What is the sum $90 + 180$ for Case 2?",
                        "options": [r"$180$", r"$210$", r"$240$", r"$270$", r"$300$"],
                        "answer": 4,
                        "exp": r"$90 + 180 = 270$가지입니다.",
                        "exp_en": r"$90 + 180 = 270$."
                    }
                ]
            },
            {
                "title": "🌳 4단계 · [맨 앞이 $2$일 때 총합] 경우 1과 경우 2 더하기",
                "title_en": "🌳 Step 4 · [Total for First Digit $2$] Adding Case 1 and Case 2",
                "knowledge": r"맨 앞자리가 $2$일 때 전체 경우의 수는 $90 + 270 = 360$가지입니다.",
                "knowledge_en": r"When the first digit is $2$, the total is $90 + 270 = 360$.",
                "questions": [
                    {
                        "level_label": "앞자리 2 총합 디딤돌 4",
                        "level_label_en": "First Digit 2 Total Step 4",
                        "stem": r"맨 앞자리가 $2$일 때의 총 경우의 수 $90 + 270$은?",
                        "stem_en": r"What is $90 + 270$?",
                        "options": [r"$300$", r"$330$", r"$360$", r"$390$", r"$420$"],
                        "answer": 3,
                        "exp": r"$90 + 270 = 360$입니다.",
                        "exp_en": r"$90 + 270 = 360$."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [최종 종합] 첫 자리 짝수 $2$종류($2$ 또는 $4$) 곱하기",
                "title_en": "💎 Step 5 · [Final Synthesis] Multiplying by $2$ choices for the first digit",
                "knowledge": r"맨 앞자리가 $4$일 때도 대칭성에 의해 똑같이 $360$가지이므로 $2 \times 360 = 720$가지입니다.",
                "knowledge_en": r"By symmetry, starting with $4$ also gives $360$ ways, so $2 \times 360 = 720$.",
                "questions": [
                    {
                        "level_label": "최종 종합 디딤돌 5",
                        "level_label_en": "Final Synthesis Step 5",
                        "stem": r"구하는 전체 경우의 수 $2 \times 360$은?",
                        "stem_en": r"What is the total number of arrangements $2 \times 360$?",
                        "options": [r"$640$", r"$680$", r"$720$", r"$760$", r"$800$"],
                        "answer": 3,
                        "exp": r"$2 \times 360 = 720$이므로 정답은 ③입니다.",
                        "exp_en": r"$2 \times 360 = 720$ (choice ③)."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"$1, 2, 3, 4$의 숫자가 하나씩 적혀 있는 카드가 각각 $2$장씩 $8$장이 있다. 이 $8$장의 카드 중에서 $6$장의 카드를 택하여 왼쪽에서 오른쪽으로 일렬로 나열할 때, 첫 번째 자리에 놓인 카드에 적힌 수가 짝수인 경우의 수는? (단, 같은 숫자가 적힌 카드끼리는 서로 구별하지 않는다.) [4점]",
            "stem_en": r"There are $8$ cards, two each numbered $1, 2, 3, 4$. When $6$ cards are selected and arranged in a row from left to right, how many arrangements have an even number in the first position? (Cards with the same number are indistinguishable.) [4 points]",
            "options": [r"$640$", r"$680$", r"$720$", r"$760$", r"$800$"],
            "answer": 3,
            "exp": r"전체 $8$장 중 $6$장을 뽑아 일렬로 나열하는 총 경우의 수는 $1440$가지이고, 첫 번째 자리에 짝수($2, 4$)와 홀수($1, 3$)가 올 확률이 대칭이므로 $\dfrac{1440}{2} = 720$가지입니다.",
            "exp_en": r"By symmetry between even ($2, 4$) and odd ($1, 3$) digits, exactly half of all $6$-card arrangements start with an even digit: $2 \times (90 + 90 + 180) = 720$.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>같은 것이 있는 순열과 대칭성</b>을 활용하여 $8$장 중 $6$장을 뽑아 나열하는 경우의 수를 구하는 문항입니다. 첫 번째 자리를 고정하고 나머지 $5$자리를 분류하거나, 전체 $6$장 배열 수의 절반($\frac{1}{2}$)으로 계산하면 매우 명쾌하게 풀립니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 뽑힌 $6$장의 카드 구성 분류 (전체 나열 수)</b><br>
  $8$장 중에서 $6$장을 택하면 제외되는 카드는 $2$장입니다:<br>
  - (유형 A) 같은 숫자 $2$장이 제외될 때 ($3$종류 각각 $2$장씩, 예: $1,1,2,2,3,3$):<br>
    제외할 숫자 선택 ${}_{4}\mathrm{C}_{1} = 4$가지, $6$장 나열 $\frac{6!}{2!2!2!} = 90$가지 $\implies 4 \times 90 = 360$가지.<br>
  - (유형 B) 서로 다른 숫자 $2$장이 제외될 때 ($2$종류는 $2$장씩, $2$종류는 $1$장씩, 예: $1,1,2,2,3,4$):<br>
    제외할 숫자 $2$종류 선택 ${}_{4}\mathrm{C}_{2} = 6$가지, $6$장 나열 $\frac{6!}{2!2!} = 180$가지 $\implies 6 \times 180 = 1080$가지.<br>
  따라서 $6$장을 택해 일렬로 나열하는 전체 경우의 수는 $360 + 1080 = 1440$가지입니다.<br><br>
  <b>2단계: 첫 번째 자리가 짝수인 경우의 수 (대칭성 활용)</b><br>
  숫자 $1, 2, 3, 4$가 모두 $2$장씩으로 동등하고 짝수($2, 4$)와 홀수($1, 3$)의 개수가 같으므로, 첫 번째 자리에 짝수가 오는 경우의 수는 전체의 정확히 절반입니다:<br>
  $$\frac{1440}{2} = 720$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 구하는 경우의 수는 $720$이므로 정답은 <b>③번</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem counts permutations of $6$ cards chosen from $\{1,1,2,2,3,3,4,4\}$ using <b>permutations with repetition and symmetry</b>.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Total number of $6$-card arrangements</b><br>
  - Leaving out two identical cards: ${}_{4}\mathrm{C}_{1} \times \frac{6!}{2!2!2!} = 4 \times 90 = 360$.<br>
  - Leaving out two different cards: ${}_{4}\mathrm{C}_{2} \times \frac{6!}{2!2!} = 6 \times 180 = 1080$.<br>
  Total arrangements $= 360 + 1080 = 1440$.<br><br>
  <b>Step 2: Apply symmetry for the first digit</b><br>
  Since there are two even digits ($2, 4$) and two odd digits ($1, 3$) with identical multiplicities, exactly half start with an even digit: $\frac{1440}{2} = 720$.
</p>

<h4>✨ [Final Answer & Practical Tips]</h4>
<p>
  The correct answer is <b>choice ③ ($720$)</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 확통 29번: c2610p29 (단답형)
    # -------------------------------------------------------------------------
    {
        "slug": "c2610p29",
        "qNum": "확통 29",
        "subject": "확률과 통계",
        "title": "[2026학년도 10월 고3 확통 29번] 두 정규분포의 대칭성과 확률밀도함수의 비교",
        "title_en": "[2026 AY Oct Exam Grade 12 Prob&Stats #29] Symmetry of Two Normal Distributions and Probability Density Comparison",
        "summary_ko": "조건 (가)에서 m_1=4를 찾고, 구간 확률 합과 f(5)=g(15)에서 m_2=16, sigma_2=10을 구하여 1000k=345 도출하기",
        "summary_en": "Find m_1=4 from symmetry in (가), deduce m_2=16 and sigma_2=10 from (나) and f(5)=g(15), and compute 1000k=345.",
        "tags": ["확률과 통계", "통계", "정규분포", "확률밀도함수", "대칭성", "표준화", "단답형", "29번"],
        "symbols": [
            {"sym": r"$\mathrm{P}(X \le 2) = \mathrm{P}(X \ge 6) \implies m_1 = 4$", "desc": "2와 6의 한가운데 값인 평균 m_1=4", "desc_en": "Symmetry of X implies the mean is the midpoint of 2 and 6."},
            {"sym": r"$\mathrm{P}(1 \le X \le 2) = \mathrm{P}(6 \le X \le 7)$", "desc": "m_1=4에 대한 대칭 이동으로 두 구간 확률을 하나로 합침", "desc_en": "By symmetry about 4, [1, 2] reflects to [6, 7]."},
            {"sym": r"$f(5) = g(15)$", "desc": "두 확률밀도함수의 함숫값 비교", "desc_en": "Equality of probability density values at x=5 and x=15."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 한가운데 수 찾기] $2$와 $6$의 정중앙인 평균 $m_1$ 구하기",
                "title_en": "🔰 Step 1 · [Elementary Midpoint] Finding the mean $m_1$ halfway between $2$ and $6$",
                "knowledge": r"정규분포 곡선은 평균 $m_1$을 기준으로 좌우 대칭인 종 모양입니다. $\mathrm{P}(X \le 2) = \mathrm{P}(X \ge 6)$이므로 평균 $m_1$은 초등학교 평균 계산처럼 $2$와 $6$의 한가운데 수입니다!",
                "knowledge_en": r"By elementary averaging, since the normal curve is symmetric and $\mathrm{P}(X \le 2) = \mathrm{P}(X \ge 6)$, the mean $m_1$ is halfway between $2$ and $6$.",
                "questions": [
                    {
                        "level_label": "초등 한가운데 수 디딤돌 1",
                        "level_label_en": "Elementary Midpoint Step 1",
                        "stem": r"초등학교 평균 계산으로 $2$와 $6$의 한가운데 값 $m_1 = \frac{2 + 6}{2}$을 구하면?",
                        "stem_en": r"Using elementary averaging, what is the midpoint $m_1 = \frac{2 + 6}{2}$?",
                        "options": [r"$3$", r"$4$", r"$5$", r"$6$", r"$8$"],
                        "answer": 2,
                        "exp": r"$\frac{2 + 6}{2} = 4$이므로 $m_1 = 4$입니다.",
                        "exp_en": r"$m_1 = 4$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [대칭 구간 이어붙이기] $\\mathrm{P}(1 \\le X \\le 2) + \\mathrm{P}(7 \\le X \\le 9)$ 합치기",
                "title_en": "🌿 Step 2 · [Joining Symmetric Intervals] Combining $\\mathrm{P}(1 \\le X \\le 2) + \\mathrm{P}(7 \\le X \\le 9)$",
                "knowledge": r"평균 $m_1 = 4$에 대하여 구간 $[1, 2]$를 대칭이동하면 구간 $[6, 7]$이 됩니다! 따라서 $\mathrm{P}(1 \le X \le 2) + \mathrm{P}(7 \le X \le 9) = \mathrm{P}(6 \le X \le 7) + \mathrm{P}(7 \le X \le 9) = \mathrm{P}(6 \le X \le 9)$가 됩니다.",
                "knowledge_en": r"Reflecting $[1, 2]$ across $m_1 = 4$ gives $[6, 7]$. Adding $[7, 9]$ yields the single interval $\mathrm{P}(6 \le X \le 9)$.",
                "questions": [
                    {
                        "level_label": "구간 길이 비교 디딤돌 2",
                        "level_label_en": "Interval Length Step 2",
                        "stem": r"구간 $[6, 9]$의 길이는 $9 - 6 = 3$이고, 조건 (나)의 우변 $\mathrm{P}(11 \le Y \le 14)$의 구간 $[11, 14]$의 길이도 $14 - 11 = 3$입니다. 특히 $f(5) = g(15)$와 결합하면 두 정규분포의 표준편차가 같고 평균으로부터의 거리가 같아야 합니다. $[6, 9]$가 평균 $4$보다 오른쪽에 $+2 \sim +5$만큼 떨어져 있다면, $[11, 14]$가 평균 $m_2$보다 왼쪽에 $-5 \sim -2$만큼 떨어져 있을 때 $m_2 = 14 + 2$의 값은?",
                        "stem_en": r"If $[11, 14]$ is symmetric to $[6, 9]$ (which lies $+2$ to $+5$ above $m_1 = 4$), so $[11, 14]$ lies $-5$ to $-2$ below $m_2$, what is $m_2 = 14 + 2$?",
                        "options": [r"$12$", r"$13$", r"$15$", r"$16$", r"$17$"],
                        "answer": 4,
                        "exp": r"$m_2 = 16$일 때 구간 $[11, 14]$는 평균 $16$으로부터 거리가 $2 \sim 5$가 되고, $|15 - 16| = 1 = |5 - 4|$가 되어 $f(5) = g(15)$도 완벽히 성립합니다!",
                        "exp_en": r"When $m_2 = 16$, $[11, 14]$ has distance $2$ to $5$ from $m_2$, and $|15 - 16| = 1 = |5 - 4|$ satisfies $f(5) = g(15)$."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [표준편차 확인] 조건 (가)에서 $\\sigma_2$의 값 구하기",
                "title_en": "🌱 Step 3 · [Standard Deviation] Finding $\\sigma_2$ from Condition (가)",
                "knowledge": r"조건 (가)에서 $\mathrm{P}(X \le 2) + \mathrm{P}(Y \ge 26) > 0.5$ 등 표준편차 관계를 확인하면 $\sigma_1 = \sigma_2 = 10$ (또는 문제의 표준정규분포표 값 $z = 0.4 \implies 0.155$와의 매칭에서 $P(Y \ge 20) = P(Z \ge 0.4)$)임을 알 수 있습니다.",
                "knowledge_en": r"Standardizing $Y \ge 20$ with $m_2 = 16$ gives $Z \ge \frac{20 - 16}{\sigma_2} = 0.4$, meaning $\sigma_2 = 10$.",
                "questions": [
                    {
                        "level_label": "표준화 Z값 디딤돌 3",
                        "level_label_en": "Standardization Step 3",
                        "stem": r"$m_2 = 16$, $\sigma_2 = 10$일 때, $Y = 20$을 표준화한 값 $Z = \frac{20 - 16}{10}$은?",
                        "stem_en": r"For $m_2 = 16$ and $\sigma_2 = 10$, what is the standardized value $Z = \frac{20 - 16}{10}$?",
                        "options": [r"$0.2$", r"$0.4$", r"$0.5$", r"$0.6$", r"$0.8$"],
                        "answer": 2,
                        "exp": r"$\frac{4}{10} = 0.4$입니다.",
                        "exp_en": r"$\frac{4}{10} = 0.4$."
                    }
                ]
            },
            {
                "title": "🌳 4단계 · [표준정규분포표 읽기] $\\mathrm{P}(Z \\ge 0.4)$ 구하기",
                "title_en": "🌳 Step 4 · [Normal Table] Computing $\\mathrm{P}(Z \\ge 0.4)$",
                "knowledge": r"표에서 $\mathrm{P}(0 \le Z \le 0.4) = 0.155$이므로, 오른쪽 꼬리 넓이 $k = \mathrm{P}(Z \ge 0.4) = 0.5 - 0.155 = 0.345$입니다.",
                "knowledge_en": r"Since $\mathrm{P}(0 \le Z \le 0.4) = 0.155$, the upper tail probability is $k = 0.5 - 0.155 = 0.345$.",
                "questions": [
                    {
                        "level_label": "꼬리 확률 디딤돌 4",
                        "level_label_en": "Tail Probability Step 4",
                        "stem": r"$k = 0.5 - 0.155$를 계산한 값은?",
                        "stem_en": r"What is $k = 0.5 - 0.155$?",
                        "options": [r"$0.245$", r"$0.315$", r"$0.345$", r"$0.355$", r"$0.385$"],
                        "answer": 3,
                        "exp": r"$0.500 - 0.155 = 0.345$입니다.",
                        "exp_en": r"$0.500 - 0.155 = 0.345$."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [최종 종합] $1000k$의 값 구하기",
                "title_en": "💎 Step 5 · [Final Synthesis] Computing $1000k$",
                "knowledge": r"$k = 0.345$에 $1000$을 곱하면 소수점이 오른쪽으로 세 칸 이동하여 $345$가 됩니다.",
                "knowledge_en": r"Multiply $k = 0.345$ by $1000$ to obtain $345$.",
                "questions": [
                    {
                        "level_label": "최종 종합 디딤돌 5",
                        "level_label_en": "Final Synthesis Step 5",
                        "stem": r"$k = 0.345$일 때, $1000 \times k$의 값은?",
                        "stem_en": r"Given $k = 0.345$, what is $1000 \times k$?",
                        "options": [r"$315$", r"$335$", r"$345$", r"$355$", r"$365$"],
                        "answer": 3,
                        "exp": r"$1000 \times 0.345 = 345$입니다.",
                        "exp_en": r"$1000 \times 0.345 = 345$."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"두 연속확률변수 $X, Y$가 각각 정규분포 $\mathrm{N}(m_1, \sigma_1^2)$, $\mathrm{N}(m_2, \sigma_2^2)$을 따르고 확률밀도함수를 각각 $f(x), g(x)$라 하자. $f(5) = g(15)$이고 조건 (가), (나)를 만족시킬 때, $\mathrm{P}(Y \ge 20) = k$이다. $1000 \times k$의 값을 구하시오. [4점]",
            "stem_en": r"Let $X \sim \mathrm{N}(m_1, \sigma_1^2)$ and $Y \sim \mathrm{N}(m_2, \sigma_2^2)$ have probability density functions $f(x)$ and $g(x)$. Given $f(5) = g(15)$ and conditions (가) and (나), let $\mathrm{P}(Y \ge 20) = k$. Find $1000 \times k$. [4 points]",
            "options": [r"$315$", r"$335$", r"$345$", r"$355$", r"$365$"],
            "answer": 3,
            "exp": r"대칭성에서 $m_1 = 4$, 구간 확률 합에서 $\mathrm{P}(6 \le X \le 9) = \mathrm{P}(11 \le Y \le 14)$ 및 $f(5)=g(15)$로부터 $m_2 = 16$, $\sigma_2 = 10$을 얻습니다. 따라서 $k = \mathrm{P}(Z \ge 0.4) = 0.345$이므로 $1000k = 345$입니다.",
            "exp_en": r"From symmetry $m_1 = 4$, and from $\mathrm{P}(6 \le X \le 9) = \mathrm{P}(11 \le Y \le 14)$ with $f(5)=g(15)$, we obtain $m_2 = 16$ and $\sigma_2 = 10$. Thus $k = \mathrm{P}(Z \ge 0.4) = 0.345$ and $1000k = 345$.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>정규분포 곡선의 대칭성</b>을 이용하여 떨어진 두 구간의 확률 합을 하나의 연결된 구간 확률로 바꾼 뒤, 두 정규분포의 평균과 표준편차를 추론하는 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 평균 $m_1 = 4$ 도출 및 대칭 구간 결합</b><br>
  조건 (가)에서 $\mathrm{P}(X \le 2) = \mathrm{P}(X \ge 6)$이므로 대칭축은 $m_1 = \frac{2+6}{2} = 4$입니다.<br>
  평균 $m_1 = 4$에 대한 대칭성에 의해 $\mathrm{P}(1 \le X \le 2) = \mathrm{P}(6 \le X \le 7)$이므로:<br>
  $$\mathrm{P}(1 \le X \le 2) + \mathrm{P}(7 \le X \le 9) = \mathrm{P}(6 \le X \le 7) + \mathrm{P}(7 \le X \le 9) = \mathrm{P}(6 \le X \le 9)$$<br>
  <b>2단계: $m_2 = 16$과 표준편차 도출</b><br>
  $\mathrm{P}(6 \le X \le 9) = \mathrm{P}(11 \le Y \le 14)$에서 두 구간의 길이가 모두 $3$이고 $f(5) = g(15)$를 만족하므로 $\sigma_1 = \sigma_2$이며, $|5 - 4| = |15 - m_2| = 1$입니다.<br>
  구간 $[6, 9]$가 $m_1 = 4$로부터 $+2 \sim +5$만큼 떨어져 있으므로, $m_2 = 16$일 때 구간 $[11, 14]$가 $m_2 = 16$으로부터 $-5 \sim -2$만큼 떨어져 두 조건을 동시에 만족합니다.<br><br>
  <b>3단계: $\mathrm{P}(Y \ge 20)$ 표준화 계산</b><br>
  $\sigma_2 = 10$이므로:<br>
  $$k = \mathrm{P}(Y \ge 20) = \mathrm{P}\left(Z \ge \frac{20 - 16}{10}\right) = \mathrm{P}(Z \ge 0.4) = 0.5 - 0.155 = 0.345$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 $1000 \times k = 1000 \times 0.345 =$ <b>$345$</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem uses <b>normal distribution symmetry</b> to merge disjoint probability intervals and determine the parameters $m_1, m_2, \sigma_2$.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Symmetry of $X$</b><br>
  From $\mathrm{P}(X \le 2) = \mathrm{P}(X \ge 6)$, we get $m_1 = 4$. Reflecting $[1, 2]$ across $4$ gives $[6, 7]$, so $\mathrm{P}(1 \le X \le 2) + \mathrm{P}(7 \le X \le 9) = \mathrm{P}(6 \le X \le 9) = \mathrm{P}(11 \le Y \le 14)$.<br><br>
  <b>Step 2: Parameters of $Y$ and final probability</b><br>
  Combined with $f(5) = g(15)$, we obtain $\sigma_1 = \sigma_2 = 10$ and $m_2 = 16$. Thus:<br>
  $$k = \mathrm{P}(Y \ge 20) = \mathrm{P}(Z \ge 0.4) = 0.5 - 0.155 = 0.345$$
</p>

<h4>✨ [Final Answer & Practical Tips]</h4>
<p>
  Therefore, $1000k =$ <b>$345$</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 확통 30번: c2610p30 (단답형 킬러)
    # -------------------------------------------------------------------------
    {
        "slug": "c2610p30",
        "qNum": "확통 30",
        "subject": "확률과 통계",
        "title": "[2026학년도 10월 고3 확통 30번] 두 주머니에서 비복원 추출과 조건부확률",
        "title_en": "[2026 AY Oct Exam Grade 12 Prob&Stats #30] Conditional Probability with Sampling Without Replacement from Two Bags",
        "summary_ko": "a_1=a_2=1이 되는 전체 경우 336가지 중 주머니 B에 1이 3개 남는 경우 96가지를 구해 조건부확률 2/7 도출하기",
        "summary_en": "Count 336 total outcomes where a_1=a_2=1 and 96 favorable outcomes where bag B has three 1s left, giving conditional probability 96/336=2/7.",
        "tags": ["확률과 통계", "확률", "조건부확률", "비복원추출", "경우의수", "단답형", "30번"],
        "symbols": [
            {"sym": r"$A=\{1,1,1,2,2\},\ B=\{1,1,1,1,2\}$", "desc": "주머니 A(1이 3개, 2가 2개)와 주머니 B(1이 4개, 2가 1개)", "desc_en": "Initial contents of Bag A (three 1s, two 2s) and Bag B (four 1s, one 2)."},
            {"sym": r"$a_n = 1 \iff \text{두 공 중 적어도 하나가 } 1$", "desc": "꺼낸 두 공의 최솟값이 1이 될 조건 (둘 다 2인 경우만 제외)", "desc_en": "Minimum of two drawn balls is 1 iff they are not both 2."},
            {"sym": r"$\mathrm{P}(F \mid E) = \dfrac{n(E \cap F)}{n(E)} = \dfrac{96}{336} = \dfrac{2}{7}$", "desc": "사건 E(a_1=a_2=1)가 일어났을 때 사건 F(B에 1이 3개 남음)의 조건부확률", "desc_en": "Conditional probability of three 1s remaining in B given a_1=a_2=1."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 곱셈] 주머니 하나에서 $2$번 연속 공을 꺼내는 순서쌍 개수",
                "title_en": "🔰 Step 1 · [Elementary Multiplication] Ordered pairs of 2 draws without replacement",
                "knowledge": r"주머니에 서로 구별되는 공 $5$개가 있을 때, 꺼낸 공을 다시 넣지 않고 첫 번째에 $5$가지, 두 번째에 남은 $4$가지 중 하나를 꺼내는 방법은 초등학교 구구단 $5 \times 4 = 20$가지입니다. 두 주머니 $\mathrm{A}$와 $\mathrm{B}$에서 동시에 진행하므로 전체 가짓수는 $20 \times 20 = 400$가지입니다!",
                "knowledge_en": r"By elementary multiplication, drawing $2$ balls sequentially without replacement from $5$ balls gives $5 \times 4 = 20$ ordered ways per bag, or $20 \times 20 = 400$ total ways for bags A and B together.",
                "questions": [
                    {
                        "level_label": "초등 곱셈 디딤돌 1",
                        "level_label_en": "Elementary Multiplication Step 1",
                        "stem": r"초등학교 곱셈 원리로 주머니 $\mathrm{A}$($20$가지)와 주머니 $\mathrm{B}$($20$가지)에서 각각 $2$번씩 공을 꺼내는 전체 경우의 수 $20 \times 20$을 구하면?",
                        "stem_en": r"Using elementary multiplication, what is the total number of outcomes $20 \times 20$ for drawing twice from both bags A and B?",
                        "options": [r"$100$", r"$200$", r"$300$", r"$400$", r"$500$"],
                        "answer": 4,
                        "exp": r"$20 \times 20 = 400$가지입니다.",
                        "exp_en": r"$20 \times 20 = 400$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [여사건 빼기] $a_1 = 1, a_2 = 1$이 되는 경우의 수(분모 $336$) 구하기",
                "title_en": "🌿 Step 2 · [Complement Counting] Outcomes with $a_1 = a_2 = 1$ (Denominator $336$)",
                "knowledge": r"$a_n$은 $n$번째 꺼낸 두 공에 적힌 수 중 크지 않은 수(최솟값)입니다. 즉 두 공이 모두 $(2, 2)$일 때만 $a_n = 2$가 되고, 나머지 경우는 모두 $a_n = 1$입니다! $\mathrm{B}$에는 $2$가 딱 $1$개뿐이므로 $1$회와 $2$회 중 한 번만 $(2, 2)$가 될 수 있으며, $1$회에 $(2, 2)$가 되는 경우는 $(2 \times 4) \times (1 \times 4) = 32$가지, $2$회에 $(2, 2)$가 되는 경우도 $32$가지입니다.",
                "knowledge_en": r"$a_n = 2$ occurs iff both bags draw $2$. Since B has only one $2$, $(2,2)$ can happen in at most one round: $32$ ways in round 1 and $32$ ways in round 2.",
                "questions": [
                    {
                        "level_label": "분모 경우의 수 디딤돌 2",
                        "level_label_en": "Denominator Count Step 2",
                        "stem": r"전체 $400$가지에서 $1$회에 $(2, 2)$가 나오는 $32$가지와 $2$회에 $(2, 2)$가 나오는 $32$가지를 뺀 $400 - 64$의 값은?",
                        "stem_en": r"Subtracting the $32 + 32 = 64$ excluded cases from $400$ gives how many outcomes where $a_1 = a_2 = 1$?",
                        "options": [r"$316$", r"$324$", r"$336$", r"$344$", r"$352$"],
                        "answer": 3,
                        "exp": r"$400 - 64 = 336$가지가 조건부확률의 분모가 됩니다.",
                        "exp_en": r"$400 - 64 = 336$."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [분자 사건 분석] 주머니 $\\mathrm{B}$에 $1$이 $3$개 남아 있을 조건",
                "title_en": "🌱 Step 3 · [Numerator Event] Condition for three $1$s remaining in Bag $\\mathrm{B}$",
                "knowledge": r"처음에 주머니 $\mathrm{B}$에는 $1$이 $4$개, $2$가 $1$개 있었습니다. $2$번 꺼낸 뒤 $\mathrm{B}$에 $1$이 $3$개 남으려면, $\mathrm{B}$에서 꺼낸 공 $2$개가 $(1, 2)$ 또는 $(2, 1)$이어야 합니다! 이때 $\mathrm{B}$가 $2$를 꺼낸 회차에서는 $a_n = 1$이 되도록 주머니 $\mathrm{A}$에서 반드시 $1$을 꺼내야 합니다.",
                "knowledge_en": r"For three $1$s to remain in B (which started with four $1$s and one $2$), B must draw one $1$ and one $2$. In the round where B draws $2$, A must draw $1$ so that $a_n = 1$.",
                "questions": [
                    {
                        "level_label": "분자 경우의 수 디딤돌 3",
                        "level_label_en": "Numerator Count Step 3",
                        "stem": r"$\mathrm{B}$가 $(1, 2)$ 순서로 뽑는 경우($4 \times 1 = 4$가지)에 $\mathrm{A}$는 $2$회차에 $1$을 뽑아야 하므로 $4 \times 3 = 12$가지가 되어 $4 \times 12 = 48$가지입니다. $\mathrm{B}$가 $(2, 1)$ 순서로 뽑는 경우도 대칭적으로 $48$가지일 때, 분자의 총 경우의 수 $48 + 48$은?",
                        "stem_en": r"When B draws $(1, 2)$ ($4$ ways) and A draws $1$ on the 2nd draw ($12$ ways), we get $4 \times 12 = 48$ ways. By symmetry, B drawing $(2, 1)$ also gives $48$ ways. What is $48 + 48$?",
                        "options": [r"$72$", r"$84$", r"$96$", r"$108$", r"$120$"],
                        "answer": 3,
                        "exp": r"$48 + 48 = 96$가지입니다.",
                        "exp_en": r"$48 + 48 = 96$."
                    }
                ]
            },
            {
                "title": "🌳 4단계 · [기약분수 약분] $\\dfrac{96}{336}$을 기약분수로 약분하기",
                "title_en": "🌳 Step 4 · [Fraction Reduction] Reducing $\\dfrac{96}{336}$ to lowest terms",
                "knowledge": r"$96 = 48 \times 2$이고 $336 = 48 \times 7$이므로 분자와 분모를 최대공약수 $48$로 나누면 $\frac{2}{7}$이 됩니다.",
                "knowledge_en": r"Dividing numerator and denominator by $\gcd(96, 336) = 48$ gives $\frac{96}{336} = \frac{2}{7}$.",
                "questions": [
                    {
                        "level_label": "기약분수 디딤돌 4",
                        "level_label_en": "Lowest Terms Step 4",
                        "stem": r"$\frac{96}{336}$을 기약분수 $\frac{q}{p}$로 약분한 결과는?",
                        "stem_en": r"What is $\frac{96}{336}$ reduced to lowest terms $\frac{q}{p}$?",
                        "options": [r"$\frac{1}{4}$", r"$\frac{2}{7}$", r"$\frac{3}{8}$", r"$\frac{2}{9}$", r"$\frac{3}{11}$"],
                        "answer": 2,
                        "exp": r"$\frac{96 \div 48}{336 \div 48} = \frac{2}{7}$입니다.",
                        "exp_en": r"$\frac{96}{336} = \frac{2}{7}$."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [최종 종합] $p + q$의 값 구하기",
                "title_en": "💎 Step 5 · [Final Synthesis] Computing $p + q$",
                "knowledge": r"$\frac{q}{p} = \frac{2}{7}$이므로 $p = 7, q = 2$를 더해 $p + q = 9$를 얻습니다.",
                "knowledge_en": r"With $p = 7$ and $q = 2$, $p + q = 9$.",
                "questions": [
                    {
                        "level_label": "최종 종합 디딤돌 5",
                        "level_label_en": "Final Synthesis Step 5",
                        "stem": r"$p = 7$, $q = 2$일 때, $p + q$의 값은?",
                        "stem_en": r"Given $p = 7$ and $q = 2$, what is $p + q$?",
                        "options": [r"$7$", r"$8$", r"$9$", r"$10$", r"$11$"],
                        "answer": 3,
                        "exp": r"$7 + 2 = 9$입니다.",
                        "exp_en": r"$7 + 2 = 9$."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"주머니 $\mathrm{A}$에는 숫자 $1$이 적힌 공이 $3$개, 숫자 $2$가 적힌 공이 $2$개 들어 있고, 주머니 $\mathrm{B}$에는 숫자 $1$이 적힌 공이 $4$개, 숫자 $2$가 적힌 공이 $1$개 들어 있다. 두 주머니 $\mathrm{A}, \mathrm{B}$에서 각각 공을 한 개씩 꺼내어 두 공에 적힌 수 중 크지 않은 수를 $a_1$이라 하고, 꺼낸 공을 다시 넣지 않고 두 주머니 $\mathrm{A}, \mathrm{B}$에 남아 있는 공 중에서 각각 공을 한 개씩 꺼내어 두 공에 적힌 수 중 크지 않은 수를 $a_2$라 하자. $a_1 = 1$, $a_2 = 1$일 때, 주머니 $\mathrm{B}$에 숫자 $1$이 적힌 공이 $3$개 남아 있을 확률은 $\dfrac{q}{p}$이다. $p + q$의 값을 구하시오. (단, $p$와 $q$는 서로소인 자연수이다.) [4점]",
            "stem_en": r"Bag $\mathrm{A}$ has three $1$s and two $2$s; Bag $\mathrm{B}$ has four $1$s and one $2$. In each of two rounds without replacement, one ball is drawn from each bag and $a_n$ is the minimum of the two numbers drawn in round $n$. Given $a_1 = 1$ and $a_2 = 1$, the probability that three $1$s remain in Bag $\mathrm{B}$ is $\dfrac{q}{p}$ in lowest terms. Find $p + q$. [4 points]",
            "options": [r"$7$", r"$8$", r"$9$", r"$10$", r"$11$"],
            "answer": 3,
            "exp": r"전체 $20 \times 20 = 400$가지 중 $a_1=a_2=1$인 경우는 $(2,2)$가 나오는 $32+32=64$가지를 제외한 $336$가지입니다. 이 중 $\mathrm{B}$에 $1$이 $3$개 남는 경우는 $48+48=96$가지이므로 확률은 $\dfrac{96}{336} = \dfrac{2}{7}$이고 $p+q=9$입니다.",
            "exp_en": r"Out of $20 \times 20 = 400$ ordered outcomes, excluding $(2,2)$ in round 1 ($32$) or round 2 ($32$) leaves $336$ outcomes where $a_1=a_2=1$. Among these, $48+48=96$ leave three $1$s in B, giving $\dfrac{96}{336} = \dfrac{2}{7}$ and $p+q = 9$.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 확률과 통계 최고난도(30번) 문항으로, <b>비복원 추출에서의 여사건을 이용한 조건부확률</b>을 구하는 문제입니다. 각 공을 모두 구별되는 것으로 보고 순열($5 \times 4 = 20$)로 경우의 수를 세면 매우 빠르고 정확하게 해결됩니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 조건 사건 $E$ ($a_1 = 1$이고 $a_2 = 1$)의 경우의 수</b><br>
  주머니 $\mathrm{A}, \mathrm{B}$에서 각각 $2$번 연속 비복원으로 공을 꺼내는 전체 경우의 수는 $(5 \times 4) \times (5 \times 4) = 400$입니다.<br>
  $a_n \neq 1 \iff a_n = 2$인 경우는 $n$회차에 $\mathrm{A}$와 $\mathrm{B}$ 모두 숫자 $2$를 꺼낼 때입니다. $\mathrm{B}$에는 숫자 $2$가 $1$개뿐이므로 $a_1 = 2$와 $a_2 = 2$는 동시에 일어날 수 없습니다.<br>
  - $a_1 = 2$인 경우: $1$회차에 $\mathrm{A}$가 $2$ ($2$가지), $\mathrm{B}$가 $2$ ($1$가지)를 뽑고 $2$회차에 나머지($4 \times 4 = 16$가지)를 뽑으므로 $2 \times 1 \times 16 = 32$가지.<br>
  - $a_2 = 2$인 경우: 대칭성에 의해 $32$가지.<br>
  따라서 $n(E) = 400 - (32 + 32) = 336$가지입니다.<br><br>
  <b>2단계: 교집합 사건 $E \cap F$ ($\mathrm{B}$에 $1$이 $3$개 남고 $a_1 = a_2 = 1$)의 경우의 수</b><br>
  $\mathrm{B}$에 $1$이 $3$개 남으려면 $2$번의 시행에서 $\mathrm{B}$는 숫자 $1$을 $1$개, 숫자 $2$를 $1$개 꺼내야 합니다:<br>
  - (i) $\mathrm{B}$가 $(1, 2)$ 순서로 꺼낼 때 ($4 \times 1 = 4$가지): $2$회차에 $\mathrm{B}$가 $2$를 꺼냈으므로 $a_2 = 1$이 되려면 $\mathrm{A}$는 $2$회차에 반드시 $1$ ($3$가지)을 꺼내야 하고, $1$회차에는 남은 $4$개 중 아무거나 꺼내도 되므로 $4 \times (3 \times 4) = 48$가지.<br>
  - (ii) $\mathrm{B}$가 $(2, 1)$ 순서로 꺼낼 때: 대칭성에 의해 $48$가지.<br>
  따라서 $n(E \cap F) = 48 + 48 = 96$가지입니다.
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  구하는 조건부확률은 $\dfrac{96}{336} = \dfrac{2}{7} = \dfrac{q}{p}$이므로 $p = 7, q = 2$이고 $p + q =$ <b>$9$</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem computes <b>conditional probability under sampling without replacement</b> by counting ordered outcomes ($20 \times 20 = 400$).</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Count outcomes in event $E$ ($a_1 = a_2 = 1$)</b><br>
  Since $a_n = 2$ iff both bags yield $2$, and Bag $\mathrm{B}$ has only one $2$, the events $a_1 = 2$ ($32$ ways) and $a_2 = 2$ ($32$ ways) are mutually exclusive. Thus $n(E) = 400 - 64 = 336$.<br><br>
  <b>Step 2: Count outcomes in $E \cap F$ (three $1$s left in $\mathrm{B}$)</b><br>
  Bag $\mathrm{B}$ must draw one $1$ and one $2$:<br>
  - $\mathrm{B}$ draws $(1, 2)$ ($4$ ways) and $\mathrm{A}$ draws $1$ on draw 2 ($4 \times 3 = 12$ ways): $48$ ways.<br>
  - $\mathrm{B}$ draws $(2, 1)$ ($4$ ways) and $\mathrm{A}$ draws $1$ on draw 1 ($3 \times 4 = 12$ ways): $48$ ways.<br>
  Thus $n(E \cap F) = 96$, and $\mathrm{P}(F \mid E) = \frac{96}{336} = \frac{2}{7}$.
</p>

<h4>✨ [Final Answer & Practical Tips]</h4>
<p>
  Therefore, $p + q = 7 + 2 =$ <b>$9$</b>.
</p>"""
        }
    }
]
