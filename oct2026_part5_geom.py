# -*- coding: utf-8 -*-
"""
oct2026_part5_geom.py
2026학년도 10월 고3 전국연합학력평가 (2027대비) 수학 [기하] 23번 ~ 30번
초등학생 눈높이 무장벽 디딤돌 5단계 퀴즈 및 상세 풀이 데이터
"""

PART5_PROBLEMS = [
    # -------------------------------------------------------------------------
    # 기하 23번: c2610g23
    # -------------------------------------------------------------------------
    {
        "slug": "c2610g23",
        "qNum": "기하 23",
        "subject": "기하",
        "title": "[2026학년도 10월 고3 기하 23번] 평면벡터의 실수배와 성분 뺄셈 연산",
        "title_en": "[2026 AY Oct Exam Grade 12 Geometry #23] Scalar Multiplication and Component Subtraction of Plane Vectors",
        "summary_ko": r"벡터 $\vec{a}=(1, 3)$에서 $2\vec{b}=(-4, 2)$를 성분별로 빼어 $k=1-(-4)=5$ 구하기",
        "summary_en": r"Subtract $2\vec{b}=(-4, 2)$ from $\vec{a}=(1, 3)$ componentwise to find $k=1-(-4)=5$.",
        "tags": ["기하", "평면벡터", "벡터의성분", "벡터의연산", "23번"],
        "symbols": [
            {"sym": r"$2\vec{b} = 2(-2, 1) = (-4, 2)$", "desc": "벡터의 각 성분에 2를 곱하는 실수배", "desc_en": "Scalar multiplication multiplies each component by 2."},
            {"sym": r"$\vec{a} - 2\vec{b} = (1 - (-4), 3 - 2) = (5, 1)$", "desc": "x성분은 x성분끼리, y성분은 y성분끼리 빼기", "desc_en": "Componentwise subtraction of two plane vectors."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 곱셈] $(-2, 1)$의 각 숫자에 $2$ 곱하기",
                "title_en": "🔰 Step 1 · [Elementary Multiplication] Multiplying each number in $(-2, 1)$ by $2$",
                "knowledge": r"벡터 $\vec{b} = (-2, 1)$에 $2$를 곱한 $2\vec{b}$는 초등학교 곱셈처럼 앞의 숫자와 뒤의 숫자에 각각 $2$를 곱하면 됩니다: $(2 \times (-2), 2 \times 1) = (-4, 2)$.",
                "knowledge_en": r"By elementary multiplication, $2\vec{b} = 2(-2, 1) = (2 \times (-2), 2 \times 1) = (-4, 2)$.",
                "questions": [
                    {
                        "level_label": "초등 곱셈 디딤돌 1",
                        "level_label_en": "Elementary Multiplication Step 1",
                        "stem": r"초등학교 곱셈 원리에 따라 $\vec{b} = (-2, 1)$의 각 성분에 $2$를 곱한 $2\vec{b}$를 바르게 구한 것은?",
                        "stem_en": r"Using elementary multiplication, what is $2\vec{b}$ for $\vec{b} = (-2, 1)$?",
                        "options": [r"$(-4, 1)$", r"$(-4, 2)$", r"$(-2, 2)$", r"$(4, 2)$", r"$(-4, -2)$"],
                        "answer": 2,
                        "exp": r"$(2 \times (-2), 2 \times 1) = (-4, 2)$입니다.",
                        "exp_en": r"$(-4, 2)$."
                    }
                ]
            },
            {
                "title": r"🌿 2단계 · [$y$성분 확인] $\vec{a} - 2\vec{b}$의 $y$성분 구하기",
                "title_en": r"🌿 Step 2 · [$y$-Component] Checking the $y$-component of $\vec{a} - 2\vec{b}$",
                "knowledge": r"$\vec{a} = (1, 3)$과 $2\vec{b} = (-4, 2)$의 $y$성분끼리 빼면 $3 - 2 = 1$입니다.",
                "knowledge_en": r"Subtracting the $y$-components gives $3 - 2 = 1$.",
                "questions": [
                    {
                        "level_label": "y성분 뺄셈 디딤돌 2",
                        "level_label_en": "y-Component Step 2",
                        "stem": r"$\vec{a} = (1, 3)$과 $2\vec{b} = (-4, 2)$에서 $y$성분끼리의 차 $3 - 2$는?",
                        "stem_en": r"What is the difference of the $y$-components $3 - 2$?",
                        "options": [r"$-1$", r"$0$", r"$1$", r"$2$", r"$5$"],
                        "answer": 3,
                        "exp": r"$3 - 2 = 1$로 문제의 $(k, 1)$의 $y$성분과 일치합니다.",
                        "exp_en": r"$3 - 2 = 1$."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [음수 뺄셈 부호] $1 - (-4)$를 덧셈으로 바꾸기",
                "title_en": "🌱 Step 3 · [Subtracting a Negative] Rewriting $1 - (-4)$ as addition",
                "knowledge": r"음수 $-4$를 빼는 것은 양수 $4$를 더하는 것과 같습니다: $1 - (-4) = 1 + 4$.",
                "knowledge_en": r"Subtracting $-4$ is equivalent to adding $4$: $1 - (-4) = 1 + 4$.",
                "questions": [
                    {
                        "level_label": "부호 변환 디딤돌 3",
                        "level_label_en": "Sign Rule Step 3",
                        "stem": r"$x$성분끼리 뺀 식 $1 - (-4)$와 같은 식은?",
                        "stem_en": r"Which expression is equivalent to $1 - (-4)$?",
                        "options": [r"$1 - 4$", r"$-1 - 4$", r"$1 + 4$", r"$-1 + 4$", r"$4 - 1$"],
                        "answer": 3,
                        "exp": r"마이너스와 마이너스가 만나 플러스가 되므로 $1 + 4$입니다.",
                        "exp_en": r"$1 - (-4) = 1 + 4$."
                    }
                ]
            },
            {
                "title": "🌳 4단계 · [$x$성분 계산] $1 + 4$ 계산하기",
                "title_en": "🌳 Step 4 · [$x$-Component] Computing $1 + 4$",
                "knowledge": r"$1 + 4 = 5$이므로 $\vec{a} - 2\vec{b} = (5, 1)$입니다.",
                "knowledge_en": r"$1 + 4 = 5$, so $\vec{a} - 2\vec{b} = (5, 1)$.",
                "questions": [
                    {
                        "level_label": "x성분 덧셈 디딤돌 4",
                        "level_label_en": "x-Component Step 4",
                        "stem": r"$\vec{a} - 2\vec{b}$를 성분으로 나타낸 결과는?",
                        "stem_en": r"What is $\vec{a} - 2\vec{b}$ in component form?",
                        "options": [r"$(1, 1)$", r"$(2, 1)$", r"$(3, 1)$", r"$(4, 1)$", r"$(5, 1)$"],
                        "answer": 5,
                        "exp": r"$(1 - (-4), 3 - 2) = (5, 1)$입니다.",
                        "exp_en": r"$(5, 1)$."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [최종 종합] 실수 $k$의 값 구하기",
                "title_en": "💎 Step 5 · [Final Synthesis] Final value of $k$",
                "knowledge": r"$(5, 1) = (k, 1)$이므로 $k = 5$입니다.",
                "knowledge_en": r"Comparing $(5, 1) = (k, 1)$ gives $k = 5$.",
                "questions": [
                    {
                        "level_label": "최종 종합 디딤돌 5",
                        "level_label_en": "Final Synthesis Step 5",
                        "stem": r"$\vec{a} - 2\vec{b} = (k, 1)$일 때, 실수 $k$의 값은?",
                        "stem_en": r"When $\vec{a} - 2\vec{b} = (k, 1)$, what is $k$?",
                        "options": [r"$1$", r"$2$", r"$3$", r"$4$", r"$5$"],
                        "answer": 5,
                        "exp": r"$k = 5$이므로 정답은 ⑤입니다.",
                        "exp_en": r"$k = 5$ (choice ⑤)."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"두 벡터 $\vec{a} = (1, 3)$, $\vec{b} = (-2, 1)$에 대하여 $\vec{a} - 2\vec{b} = (k, 1)$일 때, 실수 $k$의 값은? [2점]",
            "stem_en": r"For vectors $\vec{a} = (1, 3)$ and $\vec{b} = (-2, 1)$, if $\vec{a} - 2\vec{b} = (k, 1)$, what is the real number $k$? [2 points]",
            "options": [r"$1$", r"$2$", r"$3$", r"$4$", r"$5$"],
            "answer": 5,
            "exp": r"$\vec{a} - 2\vec{b} = (1, 3) - (-4, 2) = (5, 1) = (k, 1)$이므로 $k = 5$입니다.",
            "exp_en": r"$\vec{a} - 2\vec{b} = (1, 3) - (-4, 2) = (5, 1)$, so $k = 5$.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>평면벡터의 성분 연산(실수배와 뺄셈)</b>을 평가하는 기본 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  $$\vec{a} - 2\vec{b} = (1, 3) - 2(-2, 1) = (1, 3) - (-4, 2) = (1 - (-4), 3 - 2) = (5, 1)$$
  따라서 $(5, 1) = (k, 1)$에서 $k = 5$입니다.
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 $k = 5$이므로 정답은 <b>⑤번</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem tests <b>componentwise scalar multiplication and subtraction of plane vectors</b>.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  $$\vec{a} - 2\vec{b} = (1, 3) - (-4, 2) = (5, 1) \implies k = 5$$
</p>

<h4>✨ [Final Answer & Practical Tips]</h4>
<p>
  The correct answer is <b>choice ⑤ ($5$)</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 기하 24번: c2610g24
    # -------------------------------------------------------------------------
    {
        "slug": "c2610g24",
        "qNum": "기하 24",
        "subject": "기하",
        "title": "[2026학년도 10월 고3 기하 24번] 쌍곡선의 점근선의 방정식과 기울기",
        "title_en": "[2026 AY Oct Exam Grade 12 Geometry #24] Asymptotes of a Hyperbola and Their Slopes",
        "summary_ko": r"쌍곡선 $\dfrac{x^2}{a^2} - \dfrac{y^2}{36} = 1$의 점근선 $y = \pm\dfrac{6}{a}x$에서 $\dfrac{6}{a} = 2$를 풀어 $a=3$ 구하기",
        "summary_en": r"From the hyperbola $\dfrac{x^2}{a^2} - \dfrac{y^2}{36} = 1$ with asymptotes $y = \pm\dfrac{6}{a}x$, solve $\dfrac{6}{a} = 2$ to find $a=3$.",
        "tags": ["기하", "이차곡선", "쌍곡선", "점근선의방정식", "24번"],
        "symbols": [
            {"sym": r"$\dfrac{x^2}{a^2} - \dfrac{y^2}{b^2} = 1$", "desc": r"쌍곡선의 기본 방정식 ($b^2 = 36 \implies b = 6$)", "desc_en": r"Standard equation of a hyperbola with $b^2 = 36$."},
            {"sym": r"$y = \pm \dfrac{b}{a}x = \pm \dfrac{6}{a}x$", "desc": "쌍곡선이 한없이 가까워지는 두 직선(점근선)의 방정식", "desc_en": "Equations of the two asymptotes of the hyperbola."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 구구단 제곱] 곱해서 $36$이 되는 양수 $b$ 찾기",
                "title_en": r"🔰 Step 1 · [Elementary Multiplication] Finding $b > 0$ such that $b \times b = 36$",
                "knowledge": r"쌍곡선 식 $\frac{x^2}{a^2} - \frac{y^2}{36} = 1$에서 $y^2$ 아래의 분모 $36$은 초등학교 구구단 $6 \times 6 = 36$, 즉 $b^2 = 6^2$입니다.",
                "knowledge_en": r"In elementary multiplication, $6 \times 6 = 36$, so $b^2 = 36 \implies b = 6$.",
                "questions": [
                    {
                        "level_label": "초등 구구단 디딤돌 1",
                        "level_label_en": "Elementary Multiplication Step 1",
                        "stem": r"초등학교 구구단에서 똑같은 수를 두 번 곱해 $b^2 = 36$이 되는 양수 $b$의 값은?",
                        "stem_en": r"Using elementary multiplication, which positive number $b$ satisfies $b \times b = 36$?",
                        "options": [r"$4$", r"$5$", r"$6$", r"$8$", r"$9$"],
                        "answer": 3,
                        "exp": r"$6 \times 6 = 36$이므로 $b = 6$입니다.",
                        "exp_en": r"$b = 6$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [점근선 공식] 쌍곡선의 점근선 기울기 식 세우기",
                "title_en": "🌿 Step 2 · [Asymptote Formula] Slope of the hyperbola's asymptotes",
                "knowledge": r"쌍곡선 $\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1$의 점근선의 방정식은 $y = \pm \frac{b}{a}x$입니다. 여기서 $b = 6$이므로 점근선은 $y = \pm \frac{6}{a}x$입니다.",
                "knowledge_en": r"The asymptotes of $\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1$ are $y = \pm \frac{b}{a}x = \pm \frac{6}{a}x$.",
                "questions": [
                    {
                        "level_label": "점근선 기울기 디딤돌 2",
                        "level_label_en": "Asymptote Slope Step 2",
                        "stem": r"양수 $a$에 대하여 쌍곡선 $\frac{x^2}{a^2} - \frac{y^2}{36} = 1$의 양의 점근선 기울기는?",
                        "stem_en": r"For $a > 0$, what is the positive slope of the asymptote of $\frac{x^2}{a^2} - \frac{y^2}{36} = 1$?",
                        "options": [r"$\frac{a}{6}$", r"$\frac{6}{a}$", r"$\frac{36}{a}$", r"$\frac{6}{a^2}$", r"$6a$"],
                        "answer": 2,
                        "exp": r"$\frac{b}{a} = \frac{6}{a}$입니다.",
                        "exp_en": r"$\frac{6}{a}$."
                    }
                ]
            },
            {
                "title": r"🌱 3단계 · [기울기 비교] $\dfrac{6}{a} = 2$ 식 세우기",
                "title_en": r"🌱 Step 3 · [Comparing Slopes] Setting $\dfrac{6}{a} = 2$",
                "knowledge": r"문제에서 한 점근선의 방정식이 $y = 2x$라고 했으므로 기울기 $\frac{6}{a} = 2$입니다.",
                "knowledge_en": r"Since one asymptote is $y = 2x$, its slope satisfies $\frac{6}{a} = 2$.",
                "questions": [
                    {
                        "level_label": "방정식 변형 디딤돌 3",
                        "level_label_en": "Equation Setup Step 3",
                        "stem": r"$\frac{6}{a} = 2$의 양변에 $a$를 곱한 식은?",
                        "stem_en": r"Multiplying both sides of $\frac{6}{a} = 2$ by $a$ gives which equation?",
                        "options": [r"$2a = 6$", r"$6a = 2$", r"$a = 12$", r"$a + 2 = 6$", r"$a^2 = 6$"],
                        "answer": 1,
                        "exp": r"$2a = 6$입니다.",
                        "exp_en": r"$2a = 6$."
                    }
                ]
            },
            {
                "title": "🌳 4단계 · [나눗셈 계산] $2a = 6$에서 $a$ 구하기",
                "title_en": "🌳 Step 4 · [Division] Solving $2a = 6$ for $a$",
                "knowledge": r"$6 \div 2 = 3$입니다.",
                "knowledge_en": r"$a = 6 \div 2 = 3$.",
                "questions": [
                    {
                        "level_label": "나눗셈 디딤돌 4",
                        "level_label_en": "Division Step 4",
                        "stem": r"$2a = 6$을 만족시키는 $a$의 값은?",
                        "stem_en": r"What value of $a$ satisfies $2a = 6$?",
                        "options": [r"$1$", r"$2$", r"$3$", r"$4$", r"$6$"],
                        "answer": 3,
                        "exp": r"$a = 3$입니다.",
                        "exp_en": r"$a = 3$."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [최종 종합] 양수 $a$의 값 확정하기",
                "title_en": "💎 Step 5 · [Final Synthesis] Confirming $a = 3$",
                "knowledge": r"$a = 3$일 때 점근선은 $y = \pm \frac{6}{3}x = \pm 2x$가 되어 문제 조건을 만족합니다.",
                "knowledge_en": r"When $a = 3$, the asymptotes are $y = \pm 2x$.",
                "questions": [
                    {
                        "level_label": "최종 종합 디딤돌 5",
                        "level_label_en": "Final Synthesis Step 5",
                        "stem": r"쌍곡선 $\frac{x^2}{a^2} - \frac{y^2}{36} = 1$의 한 점근선의 방정식이 $y = 2x$일 때, 양수 $a$의 값은?",
                        "stem_en": r"When one asymptote of $\frac{x^2}{a^2} - \frac{y^2}{36} = 1$ is $y = 2x$, what is the positive constant $a$?",
                        "options": [r"$1$", r"$2$", r"$3$", r"$4$", r"$5$"],
                        "answer": 3,
                        "exp": r"$\frac{6}{a} = 2 \implies a = 3$이므로 정답은 ③입니다.",
                        "exp_en": r"$a = 3$ (choice ③)."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"쌍곡선 $\dfrac{x^2}{a^2} - \dfrac{y^2}{36} = 1$의 한 점근선의 방정식이 $y = 2x$일 때, 양수 $a$의 값은? [3점]",
            "stem_en": r"When one asymptote of the hyperbola $\dfrac{x^2}{a^2} - \dfrac{y^2}{36} = 1$ is $y = 2x$, what is the positive constant $a$? [3 points]",
            "options": [r"$1$", r"$2$", r"$3$", r"$4$", r"$5$"],
            "answer": 3,
            "exp": r"점근선의 방정식 $y = \pm \dfrac{6}{a}x$에서 $\dfrac{6}{a} = 2$이므로 양수 $a = 3$입니다.",
            "exp_en": r"From the asymptote equation $y = \pm \dfrac{6}{a}x$, equating $\dfrac{6}{a} = 2$ gives $a = 3$.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>쌍곡선의 점근선의 방정식 $y = \pm \frac{b}{a}x$</b>를 이용하여 미지수를 구하는 기본 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  쌍곡선 $\frac{x^2}{a^2} - \frac{y^2}{6^2} = 1$ ($a > 0$)의 점근선의 방정식은:<br>
  $$y = \pm \frac{6}{a}x$$
  한 점근선의 방정식이 $y = 2x$이므로 $\frac{6}{a} = 2 \implies a = 3$입니다.
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 양수 $a$의 값은 $3$이므로 정답은 <b>③번</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem uses the <b>asymptote formula $y = \pm \frac{b}{a}x$</b> of a hyperbola.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  Since $b = \sqrt{36} = 6$ and $a > 0$, the positive-slope asymptote is $y = \frac{6}{a}x = 2x \implies a = 3$.
</p>

<h4>✨ [Final Answer & Practical Tips]</h4>
<p>
  The correct answer is <b>choice ③ ($3$)</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 기하 25번: c2610g25
    # -------------------------------------------------------------------------
    {
        "slug": "c2610g25",
        "qNum": "기하 25",
        "subject": "기하",
        "title": "[2026학년도 10월 고3 기하 25번] 좌표공간의 대칭이동과 두 점 사이의 거리",
        "title_en": "[2026 AY Oct Exam Grade 12 Geometry #25] Reflections in 3D Coordinate Space and Distance Between Two Points",
        "summary_ko": r"$xy$평면 대칭점 $\mathrm{B}(1, 2, -k)$에서 $\overline{\mathrm{AB}}=2k=4$로 $k=2$를 구하고, $x$축 대칭점 $\mathrm{C}(1, -2, -2)$에서 $\overline{\mathrm{AC}}=4\sqrt{2}$ 도출하기",
        "summary_en": r"Reflect $\mathrm{A}(1, 2, k)$ across the $xy$-plane to $\mathrm{B}(1, 2, -k)$, use $\overline{\mathrm{AB}}=2k=4$ to get $k=2$, and find $\overline{\mathrm{AC}}=4\sqrt{2}$ where $\mathrm{C}(1, -2, -2)$ is the reflection across the $x$-axis.",
        "tags": ["기하", "공간도형과공간좌표", "대칭이동", "두점사이의거리", "25번"],
        "symbols": [
            {"sym": r"$\mathrm{B}(1, 2, -k)$", "desc": r"점 $\mathrm{A}(1, 2, k)$를 $xy$평면에 대하여 대칭이동한 점 ($z$좌표의 부호 반전)", "desc_en": r"Reflection of $\mathrm{A}(1, 2, k)$ across the $xy$-plane negates $z$."},
            {"sym": r"$\mathrm{C}(1, -2, -k)$", "desc": r"점 $\mathrm{A}(1, 2, k)$를 $x$축에 대하여 대칭이동한 점 ($y, z$좌표의 부호 반전)", "desc_en": r"Reflection of $\mathrm{A}(1, 2, k)$ across the $x$-axis negates $y$ and $z$."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 거울 대칭 거리] 거울에서 $k$만큼 떨어진 점과 거울 속 점 사이의 거리",
                "title_en": "🔰 Step 1 · [Elementary Mirror Distance] Distance between a point and its mirror image",
                "knowledge": r"초등학교 거울 놀이에서 내가 거울($xy$평면) 앞에 $k$만큼 서 있으면 거울 속 내 모습($\mathrm{B}$)도 거울 뒤로 $k$만큼 떨어져 있어, 나와 거울 속 모습 사이의 거리는 $k + k = 2k$입니다!",
                "knowledge_en": r"By elementary mirror symmetry, a point at height $k$ above the $xy$-plane and its reflection at $-k$ are separated by $k + k = 2k$.",
                "questions": [
                    {
                        "level_label": "초등 거울 거리 디딤돌 1",
                        "level_label_en": "Elementary Mirror Step 1",
                        "stem": r"초등학교 덧셈·나눗셈 원리로 점 $\mathrm{A}(1, 2, k)$와 $xy$평면 대칭점 $\mathrm{B}(1, 2, -k)$ 사이의 거리 $\overline{\mathrm{AB}} = 2k = 4$일 때, 양수 $k$의 값은?",
                        "stem_en": r"Using elementary arithmetic, if the distance between $\mathrm{A}(1, 2, k)$ and its reflection $\mathrm{B}(1, 2, -k)$ is $\overline{\mathrm{AB}} = 2k = 4$, what is $k$?",
                        "options": [r"$1$", r"$2$", r"$3$", r"$4$", r"$8$"],
                        "answer": 2,
                        "exp": r"$2k = 4$이므로 $k = 2$입니다. 즉 $\mathrm{A}(1, 2, 2)$입니다.",
                        "exp_en": r"$2k = 4 \implies k = 2$, so $\mathrm{A}(1, 2, 2)$."
                    }
                ]
            },
            {
                "title": r"🌿 2단계 · [$x$축 대칭이동] 점 $\mathrm{A}(1, 2, 2)$를 $x$축에 대칭이동한 점 $\mathrm{C}$ 구하기",
                "title_en": r"🌿 Step 2 · [Reflection Across $x$-Axis] Finding $\mathrm{C}$ by reflecting $\mathrm{A}(1, 2, 2)$ across the $x$-axis",
                "knowledge": r"$x$축에 대하여 대칭이동하면 $x$좌표는 그대로 유지되고, 나머지 $y$좌표와 $z$좌표의 부호가 바뀝니다.",
                "knowledge_en": r"Reflecting across the $x$-axis preserves the $x$-coordinate and negates both $y$ and $z$.",
                "questions": [
                    {
                        "level_label": "x축 대칭 좌표 디딤돌 2",
                        "level_label_en": "x-Axis Reflection Step 2",
                        "stem": r"점 $\mathrm{A}(1, 2, 2)$를 $x$축에 대하여 대칭이동한 점 $\mathrm{C}$의 좌표는?",
                        "stem_en": r"What are the coordinates of $\mathrm{C}$, the reflection of $\mathrm{A}(1, 2, 2)$ across the $x$-axis?",
                        "options": [
                            r"$(-1, 2, 2)$",
                            r"$(1, -2, 2)$",
                            r"$(1, 2, -2)$",
                            r"$(1, -2, -2)$",
                            r"$(-1, -2, -2)$"
                        ],
                        "answer": 4,
                        "exp": r"$y, z$좌표의 부호가 바뀌므로 $\mathrm{C}(1, -2, -2)$입니다.",
                        "exp_en": r"$\mathrm{C}(1, -2, -2)$."
                    }
                ]
            },
            {
                "title": r"🌱 3단계 · [좌표 차이 계산] 두 점 $\mathrm{A}(1, 2, 2)$와 $\mathrm{C}(1, -2, -2)$의 성분 차 구하기",
                "title_en": r"🌱 Step 3 · [Coordinate Differences] Differences between $\mathrm{A}(1, 2, 2)$ and $\mathrm{C}(1, -2, -2)$",
                "knowledge": r"$x$좌표의 차는 $1 - 1 = 0$, $y$좌표의 차는 $2 - (-2) = 4$, $z$좌표의 차는 $2 - (-2) = 4$입니다.",
                "knowledge_en": r"The coordinate differences are $\Delta x = 0$, $\Delta y = 4$, and $\Delta z = 4$.",
                "questions": [
                    {
                        "level_label": "제곱의 합 디딤돌 3",
                        "level_label_en": "Sum of Squares Step 3",
                        "stem": r"$\overline{\mathrm{AC}}^2 = 0^2 + 4^2 + 4^2 = 16 + 16$을 계산한 값은?",
                        "stem_en": r"What is $\overline{\mathrm{AC}}^2 = 0^2 + 4^2 + 4^2$?",
                        "options": [r"$8$", r"$16$", r"$24$", r"$32$", r"$64$"],
                        "answer": 4,
                        "exp": r"$16 + 16 = 32$입니다.",
                        "exp_en": r"$16 + 16 = 32$."
                    }
                ]
            },
            {
                "title": r"🌳 4단계 · [근호 간단히 하기] $\sqrt{32}$를 $a\sqrt{b}$ 꼴로 나타내기",
                "title_en": r"🌳 Step 4 · [Simplifying Radical] Simplifying $\sqrt{32}$",
                "knowledge": r"$32 = 16 \times 2 = 4^2 \times 2$이므로 $\sqrt{32} = 4\sqrt{2}$입니다.",
                "knowledge_en": r"Since $32 = 16 \times 2$, $\sqrt{32} = 4\sqrt{2}$.",
                "questions": [
                    {
                        "level_label": "제곱근 정리 디딤돌 4",
                        "level_label_en": "Radical Simplification Step 4",
                        "stem": r"$\sqrt{32} = \sqrt{16 \times 2}$를 간단히 한 값은?",
                        "stem_en": r"Simplify $\sqrt{32} = \sqrt{16 \times 2}$.",
                        "options": [r"$2\sqrt{2}$", r"$2\sqrt{6}$", r"$4$", r"$4\sqrt{2}$", r"$4\sqrt{3}$"],
                        "answer": 4,
                        "exp": r"$\sqrt{16} = 4$이므로 $4\sqrt{2}$입니다.",
                        "exp_en": r"$4\sqrt{2}$."
                    }
                ]
            },
            {
                "title": r"💎 5단계 · [최종 종합] 선분 $\overline{\mathrm{AC}}$의 길이 확정하기",
                "title_en": r"💎 Step 5 · [Final Synthesis] Final length of $\overline{\mathrm{AC}}$",
                "knowledge": r"선분 $\mathrm{AC}$의 길이는 $4\sqrt{2}$입니다.",
                "knowledge_en": r"$\overline{\mathrm{AC}} = 4\sqrt{2}$.",
                "questions": [
                    {
                        "level_label": "최종 종합 디딤돌 5",
                        "level_label_en": "Final Synthesis Step 5",
                        "stem": r"구하는 선분 $\mathrm{AC}$의 길이는?",
                        "stem_en": r"What is the length of segment $\mathrm{AC}$?",
                        "options": [r"$2\sqrt{2}$", r"$2\sqrt{6}$", r"$4$", r"$4\sqrt{2}$", r"$4\sqrt{3}$"],
                        "answer": 4,
                        "exp": r"$\overline{\mathrm{AC}} = 4\sqrt{2}$이므로 정답은 ④입니다.",
                        "exp_en": r"$4\sqrt{2}$ (choice ④)."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"좌표공간의 점 $\mathrm{A}(1, 2, k)$ ($k > 0$)를 $xy$평면에 대하여 대칭이동한 점을 $\mathrm{B}$라 하고, 점 $\mathrm{A}$를 $x$축에 대하여 대칭이동한 점을 $\mathrm{C}$라 하자. $\overline{\mathrm{AB}} = 4$일 때, 선분 $\mathrm{AC}$의 길이는? [3점]",
            "stem_en": r"In 3D coordinate space, let $\mathrm{B}$ be the reflection of $\mathrm{A}(1, 2, k)$ ($k > 0$) across the $xy$-plane, and let $\mathrm{C}$ be the reflection of $\mathrm{A}$ across the $x$-axis. If $\overline{\mathrm{AB}} = 4$, what is the length of segment $\mathrm{AC}$? [3 points]",
            "options": [r"$2\sqrt{2}$", r"$2\sqrt{6}$", r"$4$", r"$4\sqrt{2}$", r"$4\sqrt{3}$"],
            "answer": 4,
            "exp": r"$\mathrm{B}(1, 2, -k)$에서 $\overline{\mathrm{AB}} = 2k = 4 \implies k = 2$이므로 $\mathrm{A}(1, 2, 2)$, $\mathrm{C}(1, -2, -2)$이고 $\overline{\mathrm{AC}} = \sqrt{0 + 16 + 16} = 4\sqrt{2}$입니다.",
            "exp_en": r"From $\mathrm{B}(1, 2, -k)$ and $\overline{\mathrm{AB}} = 2k = 4$, we get $k = 2$. Then $\mathrm{A}(1, 2, 2)$ and $\mathrm{C}(1, -2, -2)$ give $\overline{\mathrm{AC}} = \sqrt{4^2 + 4^2} = 4\sqrt{2}$.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>좌표공간에서의 점의 대칭이동($xy$평면, $x$축)</b>과 두 점 사이의 거리 공식을 평가하는 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 점 $\mathrm{B}$의 좌표와 $k$ 구하기</b><br>
  점 $\mathrm{A}(1, 2, k)$를 $xy$평면에 대칭이동한 점은 $\mathrm{B}(1, 2, -k)$입니다.<br>
  $$\overline{\mathrm{AB}} = 2k = 4 \implies k = 2 \implies \mathrm{A}(1, 2, 2)$$<br>
  <b>2단계: 점 $\mathrm{C}$의 좌표와 $\overline{\mathrm{AC}}$ 구하기</b><br>
  점 $\mathrm{A}(1, 2, 2)$를 $x$축에 대칭이동한 점은 $\mathrm{C}(1, -2, -2)$이므로:<br>
  $$\overline{\mathrm{AC}} = \sqrt{(1-1)^2 + \{2-(-2)\}^2 + \{2-(-2)\}^2} = \sqrt{0 + 16 + 16} = 4\sqrt{2}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 선분 $\mathrm{AC}$의 길이는 $4\sqrt{2}$이므로 정답은 <b>④번</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem uses <b>3D coordinate reflections</b> and the distance formula.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Find $k$</b><br>
  Reflecting $\mathrm{A}(1, 2, k)$ across the $xy$-plane gives $\mathrm{B}(1, 2, -k)$, so $\overline{\mathrm{AB}} = 2k = 4 \implies k = 2$.<br><br>
  <b>Step 2: Find $\overline{\mathrm{AC}}$</b><br>
  Reflecting $\mathrm{A}(1, 2, 2)$ across the $x$-axis gives $\mathrm{C}(1, -2, -2)$, so $\overline{\mathrm{AC}} = \sqrt{0^2 + 4^2 + 4^2} = 4\sqrt{2}$.
</p>

<h4>✨ [Final Answer & Practical Tips]</h4>
<p>
  The correct answer is <b>choice ④ ($4\sqrt{2}$)</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 기하 26번: c2610g26
    # -------------------------------------------------------------------------
    {
        "slug": "c2610g26",
        "qNum": "기하 26",
        "subject": "기하",
        "title": "[2026학년도 10월 고3 기하 26번] 포물선의 접선의 방정식과 준선까지의 거리",
        "title_en": "[2026 AY Oct Exam Grade 12 Geometry #26] Tangent Line to a Parabola and Distance to Directrix",
        "summary_ko": r"포물선 $y^2=4px$의 기울기 $2$인 접선 $y=2x+\dfrac{p}{2}$와 $y=2x+1$을 비교해 $p=2$, 접점 $\mathrm{P}\!\left(\dfrac{1}{2}, 2\right)$를 구하고 준선 $x=-2$까지의 거리 $\dfrac{5}{2}$ 도출하기",
        "summary_en": r"Compare $y=2x+\dfrac{p}{2}$ with $y=2x+1$ to find $p=2$ and tangency point $\mathrm{P}\!\left(\dfrac{1}{2}, 2\right)$, then compute the distance to the directrix $x=-2$ as $\dfrac{5}{2}$.",
        "tags": ["기하", "이차곡선", "포물선", "포물선의접선", "포물선의정의", "26번"],
        "symbols": [
            {"sym": r"$y = mx + \dfrac{p}{m}$", "desc": r"포물선 $y^2 = 4px$에 접하고 기울기가 $m$인 직선의 방정식", "desc_en": r"Tangent line of slope $m$ to the parabola $y^2 = 4px$."},
            {"sym": r"$x = -p = -2$", "desc": r"초점이 $\mathrm{F}(p, 0)$인 포물선의 준선의 방정식", "desc_en": r"Directrix $x = -p$ of the parabola."}
        ],
        "levels": [
            {
                "title": r"🔰 1단계 · [초등 나눗셈] $\dfrac{p}{2} = 1$을 만족하는 수 $p$ 구하기",
                "title_en": r"🔰 Step 1 · [Elementary Division] Solving $\dfrac{p}{2} = 1$ for $p$",
                "knowledge": r"포물선 $y^2 = 4px$에 접하고 기울기가 $m = 2$인 직선의 방정식은 $y = 2x + \frac{p}{2}$입니다. 이 직선이 $y = 2x + 1$과 같으려면 초등학교 나눗셈에서 $\frac{p}{2} = 1$이어야 합니다!",
                "knowledge_en": r"The tangent of slope $m = 2$ to $y^2 = 4px$ is $y = 2x + \frac{p}{2}$. Comparing with $y = 2x + 1$ gives $\frac{p}{2} = 1$.",
                "questions": [
                    {
                        "level_label": "초등 나눗셈 디딤돌 1",
                        "level_label_en": "Elementary Division Step 1",
                        "stem": r"초등학교 나눗셈·곱셈 원리로 $\frac{p}{2} = 1$을 만족시키는 양수 $p$의 값을 구하면?",
                        "stem_en": r"Using elementary arithmetic, what value of $p$ satisfies $\frac{p}{2} = 1$?",
                        "options": [r"$1$", r"$2$", r"$3$", r"$4$", r"$6$"],
                        "answer": 2,
                        "exp": r"$p = 2 \times 1 = 2$입니다.",
                        "exp_en": r"$p = 2$."
                    }
                ]
            },
            {
                "title": r"🌿 2단계 · [접점 $\mathrm{P}$ 구하기] $y^2 = 8x$와 $y = 2x + 1$이 접하는 점 찾기",
                "title_en": r"🌿 Step 2 · [Point of Tangency $\mathrm{P}$] Finding where $y^2 = 8x$ and $y = 2x + 1$ touch",
                "knowledge": r"$p = 2$이므로 포물선은 $y^2 = 8x$입니다. $4x = 2y - 2$를 대입하면 $y^2 = 4y - 4 \implies (y - 2)^2 = 0$이므로 $y = 2$, $x = \frac{1}{2}$입니다.",
                "knowledge_en": r"Substituting $8x = 4y - 4$ into $y^2 = 8x$ gives $(y - 2)^2 = 0$, so $y = 2$ and $x = \frac{1}{2}$.",
                "questions": [
                    {
                        "level_label": "접점 x좌표 디딤돌 2",
                        "level_label_en": "Tangency x-Coordinate Step 2",
                        "stem": r"접점 $\mathrm{P}$의 $y$좌표가 $2$이고 직선 $y = 2x + 1$ 위의 점일 때, 점 $\mathrm{P}$의 $x$좌표는?",
                        "stem_en": r"When $y = 2$ on the line $y = 2x + 1$, what is the $x$-coordinate of $\mathrm{P}$?",
                        "options": [r"$\frac{1}{4}$", r"$\frac{1}{2}$", r"$1$", r"$\frac{3}{2}$", r"$2$"],
                        "answer": 2,
                        "exp": r"$2 = 2x + 1 \implies 2x = 1 \implies x = \frac{1}{2}$입니다.",
                        "exp_en": r"$x = \frac{1}{2}$."
                    }
                ]
            },
            {
                "title": "🌱 3단계 · [준선의 방정식] $y^2 = 4px$ ($p = 2$)의 준선 찾기",
                "title_en": "🌱 Step 3 · [Directrix] Finding the directrix of $y^2 = 8x$",
                "knowledge": r"$y^2 = 4px$에서 초점은 $\mathrm{F}(p, 0) = (2, 0)$이고, 준선의 방정식은 $x = -p = -2$입니다.",
                "knowledge_en": r"For $y^2 = 4px$ with $p = 2$, the focus is $(2, 0)$ and the directrix is $x = -2$.",
                "questions": [
                    {
                        "level_label": "준선의 방정식 디딤돌 3",
                        "level_label_en": "Directrix Equation Step 3",
                        "stem": r"$p = 2$일 때 포물선 $y^2 = 8x$의 준선의 방정식은?",
                        "stem_en": r"What is the equation of the directrix of $y^2 = 8x$?",
                        "options": [r"$x = -4$", r"$x = -2$", r"$x = -1$", r"$x = 2$", r"$y = -2$"],
                        "answer": 2,
                        "exp": r"준선은 $x = -p = -2$입니다.",
                        "exp_en": r"$x = -2$."
                    }
                ]
            },
            {
                "title": r"🌳 4단계 · [거리 식 세우기] $x = \dfrac{1}{2}$과 $x = -2$ 사이의 가로 거리",
                "title_en": r"🌳 Step 4 · [Horizontal Distance] Distance between $x = \dfrac{1}{2}$ and $x = -2$",
                "knowledge": r"점 $\mathrm{P}\left(\frac{1}{2}, 2\right)$와 직선 $x = -2$ 사이의 거리는 오른쪽 $x$좌표에서 왼쪽 $x$좌표를 뺀 $\frac{1}{2} - (-2) = \frac{1}{2} + 2$입니다. (포물선의 정의에 의해 초점 $\mathrm{F}(2, 0)$까지의 거리 $\overline{\mathrm{PF}}$와도 똑같습니다!)",
                "knowledge_en": r"The distance from $\mathrm{P}\left(\frac{1}{2}, 2\right)$ to $x = -2$ is $\frac{1}{2} - (-2) = \frac{1}{2} + 2$.",
                "questions": [
                    {
                        "level_label": "분수 덧셈 디딤돌 4",
                        "level_label_en": "Fraction Addition Step 4",
                        "stem": r"$\frac{1}{2} + 2$를 가분수로 계산한 값은?",
                        "stem_en": r"What is $\frac{1}{2} + 2$ as an improper fraction?",
                        "options": [r"$\frac{3}{2}$", r"$2$", r"$\frac{5}{2}$", r"$3$", r"$\frac{7}{2}$"],
                        "answer": 3,
                        "exp": r"$\frac{1}{2} + \frac{4}{2} = \frac{5}{2}$입니다.",
                        "exp_en": r"$\frac{5}{2}$."
                    }
                ]
            },
            {
                "title": r"💎 5단계 · [최종 종합] 점 $\mathrm{P}$와 준선 사이의 거리 확정하기",
                "title_en": r"💎 Step 5 · [Final Synthesis] Final distance from $\mathrm{P}$ to the directrix",
                "knowledge": r"구하는 거리는 $\frac{5}{2}$입니다.",
                "knowledge_en": r"The distance is $\frac{5}{2}$.",
                "questions": [
                    {
                        "level_label": "최종 종합 디딤돌 5",
                        "level_label_en": "Final Synthesis Step 5",
                        "stem": r"점 $\mathrm{P}$와 포물선의 준선 사이의 거리는?",
                        "stem_en": r"What is the distance between point $\mathrm{P}$ and the directrix of the parabola?",
                        "options": [r"$\frac{5}{2}$", r"$3$", r"$\frac{7}{2}$", r"$4$", r"$\frac{9}{2}$"],
                        "answer": 1,
                        "exp": r"$\frac{1}{2} - (-2) = \frac{5}{2}$이므로 정답은 ①입니다.",
                        "exp_en": r"$\frac{5}{2}$ (choice ①)."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"포물선 $y^2 = 4px$ ($p > 0$)에 접하는 직선 $y = 2x + 1$이 포물선과 만나는 점을 $\mathrm{P}$라 할 때, 점 $\mathrm{P}$와 포물선의 준선 사이의 거리는? [3점]",
            "stem_en": r"The line $y = 2x + 1$ is tangent to the parabola $y^2 = 4px$ ($p > 0$) at point $\mathrm{P}$. What is the distance between $\mathrm{P}$ and the directrix of the parabola? [3 points]",
            "options": [r"$\dfrac{5}{2}$", r"$3$", r"$\dfrac{7}{2}$", r"$4$", r"$\dfrac{9}{2}$"],
            "answer": 1,
            "exp": r"접선 공식 $y = 2x + \dfrac{p}{2}$에서 $\dfrac{p}{2} = 1 \implies p = 2$이고 접점은 $\mathrm{P}\left(\dfrac{1}{2}, 2\right)$입니다. 준선 $x = -2$까지의 거리는 $\dfrac{1}{2} - (-2) = \dfrac{5}{2}$입니다.",
            "exp_en": r"From $y = 2x + \dfrac{p}{2} = 2x + 1$, we get $p = 2$ and $\mathrm{P}\left(\dfrac{1}{2}, 2\right)$. The distance to the directrix $x = -2$ is $\dfrac{1}{2} - (-2) = \dfrac{5}{2}$.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>기울기가 주어진 포물선의 접선의 방정식 $y = mx + \frac{p}{m}$</b>과 포물선의 준선의 정의를 평가하는 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 접선 공식으로 $p$ 구하기</b><br>
  포물선 $y^2 = 4px$에 접하고 기울기가 $2$인 직선의 방정식은 $y = 2x + \frac{p}{2}$입니다.<br>
  이 직선이 $y = 2x + 1$이므로 $\frac{p}{2} = 1 \implies p = 2$입니다.<br><br>
  <b>2단계: 접점 $\mathrm{P}$와 준선 사이의 거리 구하기</b><br>
  $y^2 = 8x$와 $y = 2x + 1$을 연립하면 $(y - 2)^2 = 0 \implies y = 2, x = \frac{1}{2}$이므로 $\mathrm{P}\left(\frac{1}{2}, 2\right)$입니다.<br>
  준선의 방정식은 $x = -p = -2$이므로 점 $\mathrm{P}$와 준선 사이의 거리는:<br>
  $$\frac{1}{2} - (-2) = \frac{5}{2}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 구하는 거리는 $\dfrac{5}{2}$이므로 정답은 <b>①번</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem uses the <b>tangent line formula $y = mx + \frac{p}{m}$</b> for a parabola and the equation of its directrix.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Find $p$ and point $\mathrm{P}$</b><br>
  Equating $y = 2x + \frac{p}{2}$ with $y = 2x + 1$ gives $p = 2$. Solving $y^2 = 8x$ with $y = 2x + 1$ gives $\mathrm{P}\left(\frac{1}{2}, 2\right)$.<br><br>
  <b>Step 2: Distance to directrix $x = -2$</b><br>
  $$\text{Distance} = \frac{1}{2} - (-2) = \frac{5}{2}$$
</p>

<h4>✨ [Final Answer & Practical Tips]</h4>
<p>
  The correct answer is <b>choice ① ($\dfrac{5}{2}$)</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 기하 27번: c2610g27
    # -------------------------------------------------------------------------
    {
        "slug": "c2610g27",
        "qNum": "기하 27",
        "subject": "기하",
        "title": "[2026학년도 10월 고3 기하 27번] 원기둥의 밑면 원주각과 삼수선의 정리",
        "title_en": "[2026 AY Oct Exam Grade 12 Geometry #27] Cylinder Base Inscribed Angle and Theorem of Three Perpendiculars",
        "summary_ko": r"밑면 $C_2$의 지름 $\overline{\mathrm{A'C}}=8$에서 호 $\mathrm{A'D}=\dfrac{4}{3}\pi$에 대한 중심각·원주각으로 $\mathrm{D}$에서 $\mathrm{A'C}$까지의 거리 $2\sqrt{3}$을 구하고 삼수선의 정리로 높이 $2\sqrt{6}$ 도출하기",
        "summary_en": r"Use diameter $\overline{\mathrm{A'C}}=8$ and arc length $\dfrac{4}{3}\pi$ on base $C_2$ to find the perpendicular distance $2\sqrt{3}$ from $\mathrm{D}$ to $\mathrm{A'C}$, then apply the Theorem of Three Perpendiculars to find cylinder height $2\sqrt{6}$.",
        "tags": ["기하", "공간도형과공간좌표", "삼수선의정리", "원기둥", "부채꼴의호의길이", "27번"],
        "symbols": [
            {"sym": r"$\overline{A'C} = 2r = 8$", "desc": r"밑면 원 $C_2$의 중심을 지나는 지름의 길이", "desc_en": r"Diameter of the circular base $C_2$ with radius $4$."},
            {"sym": r"$l = r\theta \implies 4\theta = \dfrac{4}{3}\pi \implies \theta = \dfrac{\pi}{3}$", "desc": r"중심각을 이용하여 밑면 직각삼각형 $\mathrm{A'CD}$의 내각 결정", "desc_en": r"Central angle formula $l = r\theta$ on the base circle."},
            {"sym": r"$\overline{DH}^2 + \overline{AA'}^2 = \overline{DM}^2$", "desc": "삼수선의 정리에 의한 공간 삼각형 ABD의 높이 제곱", "desc_en": "Pythagorean relation from the Theorem of Three Perpendiculars."}
        ],
        "levels": [
            {
                "title": "🔰 1단계 · [초등 삼각형의 넓이] 밑변이 $8$이고 넓이가 $24$인 삼각형의 높이 구하기",
                "title_en": "🔰 Step 1 · [Elementary Triangle Area] Finding the altitude of a triangle with base $8$ and area $24$",
                "knowledge": r"삼각형 $\mathrm{ABD}$에서 밑변 $\overline{\mathrm{AB}}$는 반지름이 $4$인 원의 지름이므로 $2 \times 4 = 8$입니다! 초등학교 삼각형의 넓이 공식 $\frac{1}{2} \times (\text{밑변}) \times (\text{높이}) = 24$로 삼각형 $\mathrm{ABD}$의 높이를 먼저 구해 봅시다.",
                "knowledge_en": r"By elementary geometry, the diameter is $\overline{\mathrm{AB}} = 2 \times 4 = 8$. Using $\text{Area} = \frac{1}{2} \times \text{base} \times \text{height} = 24$, we can immediately find the altitude of $\triangle\mathrm{ABD}$.",
                "questions": [
                    {
                        "level_label": "초등 삼각형 넓이 디딤돌 1",
                        "level_label_en": "Elementary Triangle Area Step 1",
                        "stem": r"초등학교 삼각형의 넓이 공식 $\frac{1}{2} \times 8 \times H = 24$에서 점 $\mathrm{D}$로부터 직선 $\mathrm{AB}$까지의 거리(높이 $H$)는?",
                        "stem_en": r"Using the elementary triangle area formula $\frac{1}{2} \times 8 \times H = 24$, what is the altitude $H$ from $\mathrm{D}$ to $\mathrm{AB}$?",
                        "options": [r"$3$", r"$4$", r"$6$", r"$8$", r"$12$"],
                        "answer": 3,
                        "exp": r"$4H = 24$이므로 삼각형 $\mathrm{ABD}$의 높이 $H = 6$입니다!",
                        "exp_en": r"$4H = 24 \implies H = 6$."
                    }
                ]
            },
            {
                "title": r"🌿 2단계 · [밑면 중심각과 원주각] 호의 길이 $\dfrac{4}{3}\pi$로 직각삼각형 $\mathrm{A'CD}$ 분석하기",
                "title_en": r"🌿 Step 2 · [Base Circle Angles] Analyzing right triangle $\mathrm{A'CD}$ from arc length $\dfrac{4}{3}\pi$",
                "knowledge": r"점 $\mathrm{A}, \mathrm{B}$에서 밑면 $C_2$에 내린 수선의 발을 $\mathrm{A'}, \mathrm{C}$라 하면 $\overline{\mathrm{A'C}} = 8$은 지름입니다. 짧은 호 $\mathrm{A'D}$(또는 $\mathrm{CD}$)의 중심각에서 직각삼각형 $\mathrm{A'CD}$의 한 예각은 $\frac{\pi}{6}$ ($30^\circ$)가 되어 $\overline{\mathrm{A'D}} = 4$, $\overline{\mathrm{CD}} = 4\sqrt{3}$입니다.",
                "knowledge_en": r"Projecting $\mathrm{A}, \mathrm{B}$ onto $C_2$ gives diameter $\overline{\mathrm{A'C}} = 8$. In right triangle $\mathrm{A'CD}$, the legs are $4$ and $4\sqrt{3}$.",
                "questions": [
                    {
                        "level_label": "밑면 수선의 길이 디딤돌 2",
                        "level_label_en": "Base Altitude Step 2",
                        "stem": r"빗변이 $\overline{\mathrm{A'C}} = 8$이고 두 직각변이 $4, 4\sqrt{3}$인 직각삼각형 $\mathrm{A'CD}$에서, 꼭짓점 $\mathrm{D}$에서 지름 $\mathrm{A'C}$에 내린 수선의 발 $\mathrm{M}$까지의 길이 $\overline{\mathrm{DM}} = \frac{4 \times 4\sqrt{3}}{8}$은?",
                        "stem_en": r"In right triangle $\mathrm{A'CD}$ with hypotenuse $8$ and legs $4, 4\sqrt{3}$, what is the altitude $\overline{\mathrm{DM}} = \frac{4 \times 4\sqrt{3}}{8}$ to the diameter $\mathrm{A'C}$?",
                        "options": [r"$\sqrt{3}$", r"$2\sqrt{2}$", r"$2\sqrt{3}$", r"$3\sqrt{3}$", r"$4\sqrt{3}$"],
                        "answer": 3,
                        "exp": r"$\frac{16\sqrt{3}}{8} = 2\sqrt{3}$입니다.",
                        "exp_en": r"$\overline{\mathrm{DM}} = 2\sqrt{3}$."
                    }
                ]
            },
            {
                "title": r"🌱 3단계 · [삼수선의 정리] 원기둥의 높이 $h$와 $H = 6$, $\overline{\mathrm{DM}} = 2\sqrt{3}$ 연결하기",
                "title_en": r"🌱 Step 3 · [Three Perpendiculars] Relating cylinder height $h$ with $H = 6$ and $\overline{\mathrm{DM}} = 2\sqrt{3}$",
                "knowledge": r"삼수선의 정리에 의해 삼각형 $\mathrm{ABD}$의 높이 $H = 6$은 밑면에서의 수선 $\overline{\mathrm{DM}} = 2\sqrt{3}$과 원기둥의 높이 $h$를 두 직각변으로 하는 직각삼각형의 빗변입니다! 즉 $(2\sqrt{3})^2 + h^2 = 6^2$입니다.",
                "knowledge_en": r"By the Theorem of Three Perpendiculars, $\overline{\mathrm{DM}}^2 + h^2 = H^2$, so $(2\sqrt{3})^2 + h^2 = 6^2$.",
                "questions": [
                    {
                        "level_label": "피타고라스 정리 디딤돌 3",
                        "level_label_en": "Pythagorean Theorem Step 3",
                        "stem": r"$12 + h^2 = 36$에서 원기둥의 높이의 제곱 $h^2$의 값은?",
                        "stem_en": r"From $12 + h^2 = 36$, what is $h^2$?",
                        "options": [r"$16$", r"$20$", r"$24$", r"$28$", r"$32$"],
                        "answer": 3,
                        "exp": r"$h^2 = 36 - 12 = 24$입니다.",
                        "exp_en": r"$h^2 = 36 - 12 = 24$."
                    }
                ]
            },
            {
                "title": r"🌳 4단계 · [제곱근 정리] $\sqrt{24}$ 간단히 하기",
                "title_en": r"🌳 Step 4 · [Simplifying Radical] Simplifying $\sqrt{24}$",
                "knowledge": r"$24 = 4 \times 6 = 2^2 \times 6$이므로 $h = \sqrt{24} = 2\sqrt{6}$입니다.",
                "knowledge_en": r"Since $24 = 4 \times 6$, $h = \sqrt{24} = 2\sqrt{6}$.",
                "questions": [
                    {
                        "level_label": "제곱근 계산 디딤돌 4",
                        "level_label_en": "Radical Step 4",
                        "stem": r"$h^2 = 24$ ($h > 0$)일 때 $h = \sqrt{24}$를 간단히 한 값은?",
                        "stem_en": r"Simplify $h = \sqrt{24}$.",
                        "options": [r"$2\sqrt{3}$", r"$2\sqrt{6}$", r"$3\sqrt{2}$", r"$4\sqrt{3}$", r"$4\sqrt{6}$"],
                        "answer": 2,
                        "exp": r"$\sqrt{4 \times 6} = 2\sqrt{6}$입니다.",
                        "exp_en": r"$2\sqrt{6}$."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [최종 종합] 원기둥의 높이 확정하기",
                "title_en": "💎 Step 5 · [Final Synthesis] Final height of the cylinder",
                "knowledge": r"구하는 원기둥의 높이는 $2\sqrt{6}$입니다.",
                "knowledge_en": r"The height of the cylinder is $2\sqrt{6}$.",
                "questions": [
                    {
                        "level_label": "최종 종합 디딤돌 5",
                        "level_label_en": "Final Synthesis Step 5",
                        "stem": r"이 원기둥의 높이는?",
                        "stem_en": r"What is the height of this cylinder?",
                        "options": [r"$2\sqrt{3}$", r"$2\sqrt{6}$", r"$6$", r"$4\sqrt{3}$", r"$6\sqrt{2}$"],
                        "answer": 2,
                        "exp": r"$h = 2\sqrt{6}$이므로 정답은 ②입니다.",
                        "exp_en": r"$2\sqrt{6}$ (choice ②)."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"밑면의 반지름의 길이가 $4$인 원기둥이 있다. 이 원기둥의 한 밑면의 둘레를 이루는 원을 $C_1$, 다른 밑면의 둘레를 이루는 원을 $C_2$라 하자. 원 $C_1$의 중심을 지나는 직선이 원 $C_1$과 만나는 두 점을 $\mathrm{A}, \mathrm{B}$라 하고, 점 $\mathrm{B}$를 지나고 원기둥의 밑면에 수직인 직선이 원 $C_2$와 만나는 점을 $\mathrm{C}$라 하자. 원 $C_2$ 위의 점 $\mathrm{D}$에 대하여 호 $\mathrm{CD}$의 길이가 $\dfrac{4}{3}\pi$이고 삼각형 $\mathrm{ABD}$의 넓이가 $24$일 때, 이 원기둥의 높이는? [3점]",
            "stem_en": r"A cylinder has base circles $C_1$ and $C_2$ of radius $4$. Points $\mathrm{A}, \mathrm{B}$ form a diameter of $C_1$, and the line through $\mathrm{B}$ perpendicular to the bases meets $C_2$ at $\mathrm{C}$. For a point $\mathrm{D}$ on $C_2$, the arc $\mathrm{CD}$ has length $\dfrac{4}{3}\pi$ and $\text{Area}(\triangle\mathrm{ABD}) = 24$. What is the height of the cylinder? [3 points]",
            "options": [r"$2\sqrt{3}$", r"$2\sqrt{6}$", r"$6$", r"$4\sqrt{3}$", r"$6\sqrt{2}$"],
            "answer": 2,
            "exp": r"점 $\mathrm{A}$의 $C_2$ 위 정사영을 $\mathrm{A'}$이라 하면 $\overline{\mathrm{A'C}} = 8$이고 점 $\mathrm{D}$에서 $\mathrm{A'C}$에 내린 수선의 길이는 $2\sqrt{3}$입니다. 삼각형 $\mathrm{ABD}$의 높이가 $\dfrac{2\times 24}{8} = 6$이므로 원기둥의 높이는 $\sqrt{6^2 - (2\sqrt{3})^2} = 2\sqrt{6}$입니다.",
            "exp_en": r"Projecting $\mathrm{A}$ to $\mathrm{A'}$ on $C_2$ gives diameter $\overline{\mathrm{A'C}} = 8$, and the altitude from $\mathrm{D}$ to $\mathrm{A'C}$ is $2\sqrt{3}$. Since the altitude of $\triangle\mathrm{ABD}$ to $\mathrm{AB}$ is $6$, the cylinder height is $\sqrt{6^2 - (2\sqrt{3})^2} = 2\sqrt{6}$.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>원기둥의 밑면에서의 호의 길이($l = r\theta$)와 삼수선의 정리</b>를 결합하여 원기둥의 높이를 구하는 공간도형 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 삼각형 $\mathrm{ABD}$의 높이 구하기</b><br>
  원 $C_1$의 반지름이 $4$이므로 지름 $\overline{\mathrm{AB}} = 8$입니다.<br>
  점 $\mathrm{D}$에서 직선 $\mathrm{AB}$에 내린 수선의 발을 $\mathrm{H}$라 하면:<br>
  $$\text{Area}(\triangle\mathrm{ABD}) = \frac{1}{2} \times 8 \times \overline{\mathrm{DH}} = 24 \implies \overline{\mathrm{DH}} = 6$$<br>
  <b>2단계: 밑면 원 $C_2$에서 점 $\mathrm{D}$와 지름 $\mathrm{A'C}$ 사이의 거리 구하기</b><br>
  점 $\mathrm{A}$에서 밑면 $C_2$에 내린 수선의 발을 $\mathrm{A'}$이라 하면 $\overline{\mathrm{A'C}} = 8$은 원 $C_2$의 지름입니다.<br>
  호 $\mathrm{CD}$의 길이가 $4\theta = \frac{4}{3}\pi$이므로 중심각은 $\frac{\pi}{3}$ ($60^\circ$)이고, 원주각 $\angle\mathrm{CA'D} = \frac{\pi}{6}$ ($30^\circ$)입니다.<br>
  따라서 직각삼각형 $\mathrm{A'CD}$에서 $\overline{\mathrm{CD}} = 4$, $\overline{\mathrm{A'D}} = 4\sqrt{3}$이고, 점 $\mathrm{D}$에서 지름 $\mathrm{A'C}$에 내린 수선의 발 $\mathrm{M}$까지의 거리는:<br>
  $$\overline{\mathrm{DM}} = 4\sin\frac{\pi}{3} = 2\sqrt{3}$$<br>
  <b>3단계: 삼수선의 정리로 원기둥의 높이 $h$ 구하기</b><br>
  삼수선의 정리에 의하여 $\overline{\mathrm{HM}} = h$는 밑면에 수직이므로:<br>
  $$h = \sqrt{\overline{\mathrm{DH}}^2 - \overline{\mathrm{DM}}^2} = \sqrt{6^2 - (2\sqrt{3})^2} = \sqrt{36 - 12} = \sqrt{24} = 2\sqrt{6}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 원기둥의 높이는 $2\sqrt{6}$이므로 정답은 <b>②번</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem applies the <b>Theorem of Three Perpendiculars</b> to a cylinder with circular base radius $4$.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Altitude of $\triangle\mathrm{ABD}$</b><br>
  Since $\overline{\mathrm{AB}} = 8$ and $\text{Area}(\triangle\mathrm{ABD}) = 24$, the altitude from $\mathrm{D}$ to $\mathrm{AB}$ is $\overline{\mathrm{DH}} = 6$.<br><br>
  <b>Step 2: Base projection and Three Perpendiculars</b><br>
  On circle $C_2$, arc $\mathrm{CD} = \frac{4}{3}\pi$ gives central angle $\frac{\pi}{3}$, so the perpendicular distance from $\mathrm{D}$ to diameter $\mathrm{A'C}$ is $\overline{\mathrm{DM}} = 4\sin\frac{\pi}{3} = 2\sqrt{3}$.<br>
  By the Theorem of Three Perpendiculars, $h = \sqrt{6^2 - (2\sqrt{3})^2} = \sqrt{24} = 2\sqrt{6}$.
</p>

<h4>✨ [Final Answer & Practical Tips]</h4>
<p>
  The correct answer is <b>choice ② ($2\sqrt{6}$)</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 기하 28번: c2610g28
    # -------------------------------------------------------------------------
    {
        "slug": "c2610g28",
        "qNum": "기하 28",
        "subject": "기하",
        "title": "[2026학년도 10월 고3 기하 28번] 타원의 정의와 이등변삼각형의 닮음",
        "title_en": "[2026 AY Oct Exam Grade 12 Geometry #28] Definition of an Ellipse and Similar Isosceles Triangles",
        "summary_ko": r"타원의 정의 $\overline{\mathrm{F'P}}+\overline{\mathrm{PF}}=2a=\overline{\mathrm{F'Q}}$에서 $\overline{\mathrm{PF}}=\overline{\mathrm{PQ}}$를 찾고 이등변삼각형의 닮음과 넓이 $6\sqrt{7}$로부터 $c=3\sqrt{2}$, 둘레 $8c=24\sqrt{2}$ 구하기",
        "summary_en": r"Use $\overline{\mathrm{F'P}}+\overline{\mathrm{PF}}=2a=\overline{\mathrm{F'Q}}$ to show $\overline{\mathrm{PF}}=\overline{\mathrm{PQ}}$, apply similarity of isosceles triangles and $\text{Area}(\triangle\mathrm{PFQ})=6\sqrt{7}$ to find $c=3\sqrt{2}$, and compute $\text{Perimeter}(\triangle\mathrm{F'RQ})=8c=24\sqrt{2}$.",
        "tags": ["기하", "이차곡선", "타원의정의", "이등변삼각형", "닮음", "28번"],
        "symbols": [
            {"sym": r"$\overline{F'P} + \overline{PF} = 2a = \overline{F'Q}$", "desc": r"타원의 정의(장축의 길이 $2a$)와 $\overline{\mathrm{F'Q}}=2a$에서 $\overline{\mathrm{PF}}=\overline{\mathrm{PQ}}$ 도출", "desc_en": r"Ellipse definition combined with $\overline{\mathrm{F'Q}}=2a$ implies $\overline{\mathrm{PF}}=\overline{\mathrm{PQ}}$."},
            {"sym": r"$\triangle F'FQ \sim \triangle FPQ$", "desc": r"밑각 $\theta$를 공유하는 두 이등변삼각형의 $\mathrm{AA}$ 닮음", "desc_en": r"Two isosceles triangles sharing base angle $\theta$ are similar."},
            {"sym": r"$\text{둘레}(\triangle F'RQ) = 4a + 2c = 8c$", "desc": r"타원의 정의 $\overline{\mathrm{F'R}}+\overline{\mathrm{FR}}=2a$를 이용한 삼각형 $\mathrm{F'RQ}$의 둘레의 길이", "desc_en": r"Perimeter of $\triangle\mathrm{F'RQ}$ expressed via the ellipse definition."}
        ],
        "levels": [
            {
                "title": r"🔰 1단계 · [초등 선분 빼기] $\overline{\mathrm{F'P}} + \overline{\mathrm{PF}} = \overline{\mathrm{F'P}} + \overline{\mathrm{PQ}}$에서 같은 길이 찾기",
                "title_en": r"🔰 Step 1 · [Elementary Segment Subtraction] Finding equal segments from $\overline{\mathrm{F'P}} + \overline{\mathrm{PF}} = \overline{\mathrm{F'P}} + \overline{\mathrm{PQ}}$",
                "knowledge": r"타원 위의 점 $\mathrm{P}$에서 두 초점까지의 거리의 합은 장축의 길이 $\overline{\mathrm{F'P}} + \overline{\mathrm{PF}} = 2a$입니다. 그런데 점 $\mathrm{P}$를 지나는 선분 $\mathrm{F'Q}$의 길이도 $\overline{\mathrm{F'Q}} = \overline{\mathrm{F'P}} + \overline{\mathrm{PQ}} = 2a$라고 주어졌으므로, 초등학교 양팔저울처럼 양쪽에서 $\overline{\mathrm{F'P}}$를 빼면 $\overline{\mathrm{PF}} = \overline{\mathrm{PQ}}$가 됩니다!",
                "knowledge_en": r"By elementary subtraction, since $\overline{\mathrm{F'P}} + \overline{\mathrm{PF}} = 2a$ (ellipse definition) and $\overline{\mathrm{F'Q}} = \overline{\mathrm{F'P}} + \overline{\mathrm{PQ}} = 2a$, subtracting $\overline{\mathrm{F'P}}$ gives $\overline{\mathrm{PF}} = \overline{\mathrm{PQ}}$.",
                "questions": [
                    {
                        "level_label": "초등 선분 비교 디딤돌 1",
                        "level_label_en": "Elementary Segment Step 1",
                        "stem": r"초등학교 덧셈·뺄셈 원리에 따라 $\overline{\mathrm{F'P}} + \overline{\mathrm{PF}} = 2a$와 $\overline{\mathrm{F'P}} + \overline{\mathrm{PQ}} = 2a$를 비교하면, 삼각형 $\mathrm{PFQ}$는 어떤 삼각형일까요?",
                        "stem_en": r"Using elementary subtraction on $\overline{\mathrm{F'P}} + \overline{\mathrm{PF}} = 2a$ and $\overline{\mathrm{F'P}} + \overline{\mathrm{PQ}} = 2a$, what kind of triangle is $\triangle\mathrm{PFQ}$?",
                        "options": [
                            r"$\overline{\mathrm{PF}} = \overline{\mathrm{PQ}}$인 이등변삼각형",
                            r"$\overline{\mathrm{PF}} = \overline{\mathrm{FQ}}$인 이등변삼각형",
                            r"정삼각형",
                            r"$\angle\mathrm{Q} = 90^\circ$인 직각삼각형",
                            r"세 변의 길이가 모두 다른 삼각형"
                        ],
                        "answer": 1,
                        "exp": r"$\overline{\mathrm{PF}} = \overline{\mathrm{PQ}}$이므로 삼각형 $\mathrm{PFQ}$는 이등변삼각형입니다!",
                        "exp_en": r"Since $\overline{\mathrm{PF}} = \overline{\mathrm{PQ}}$, $\triangle\mathrm{PFQ}$ is isosceles."
                    }
                ]
            },
            {
                "title": r"🌿 2단계 · [삼각비와 닮음] $\tan\theta = \dfrac{\sqrt{7}}{3}$에서 $\cos\theta$와 $2a : c$ 비율 구하기",
                "title_en": r"🌿 Step 2 · [Trigonometry & Similarity] Finding $\cos\theta$ and the ratio $2a : c$",
                "knowledge": r"$\angle\mathrm{F'QF} = \theta$일 때 $\tan\theta = \frac{\sqrt{7}}{3}$이면 직각삼각형 피타고라스 정리로 빗변은 $\sqrt{3^2 + 7} = 4$이므로 $\cos\theta = \frac{3}{4}, \sin\theta = \frac{\sqrt{7}}{4}$입니다. 또한 $\overline{\mathrm{F'F}} = \overline{\mathrm{FQ}} = 2c$인 이등변삼각형 $\mathrm{F'FQ}$에서 $\overline{\mathrm{F'Q}} = 2a = 2(2c\cos\theta) = 3c$가 됩니다!",
                "knowledge_en": r"From $\tan\theta = \frac{\sqrt{7}}{3}$, we have $\cos\theta = \frac{3}{4}$. In isosceles $\triangle\mathrm{F'FQ}$ with $\overline{\mathrm{F'F}} = \overline{\mathrm{FQ}} = 2c$, the base is $\overline{\mathrm{F'Q}} = 2a = 2(2c\cos\theta) = 3c$.",
                "questions": [
                    {
                        "level_label": "이등변삼각형 변의 비 디딤돌 2",
                        "level_label_en": "Isosceles Ratio Step 2",
                        "stem": r"이등변삼각형 $\mathrm{PFQ}$ ($\overline{\mathrm{PF}} = \overline{\mathrm{PQ}}$)에서 밑변이 $\overline{\mathrm{FQ}} = 2c$이고 밑각이 $\theta$ ($\cos\theta = \frac{3}{4}$)일 때, $\overline{\mathrm{PQ}} = \frac{c}{\cos\theta}$를 $c$로 나타내면?",
                        "stem_en": r"In isosceles $\triangle\mathrm{PFQ}$ with base $\overline{\mathrm{FQ}} = 2c$ and base angle $\theta$ ($\cos\theta = \frac{3}{4}$), what is $\overline{\mathrm{PQ}} = \frac{c}{\cos\theta}$?",
                        "options": [r"$\frac{3}{4}c$", r"$c$", r"$\frac{4}{3}c$", r"$\frac{3}{2}c$", r"$2c$"],
                        "answer": 3,
                        "exp": r"$\frac{c}{3/4} = \frac{4}{3}c$입니다.",
                        "exp_en": r"$\overline{\mathrm{PQ}} = \frac{4}{3}c$."
                    }
                ]
            },
            {
                "title": r"🌱 3단계 · [넓이로 $c$ 구하기] 삼각형 $\mathrm{PFQ}$의 넓이 $6\sqrt{7}$ 이용하기",
                "title_en": r"🌱 Step 3 · [Finding $c$ from Area] Using $\text{Area}(\triangle\mathrm{PFQ}) = 6\sqrt{7}$",
                "knowledge": r"삼각형 $\mathrm{PFQ}$에서 밑변은 $\overline{\mathrm{FQ}} = 2c$이고 높이는 $c\tan\theta = \frac{\sqrt{7}}{3}c$이므로, 넓이는 $\frac{1}{2} \times 2c \times \frac{\sqrt{7}}{3}c = \frac{\sqrt{7}}{3}c^2 = 6\sqrt{7}$입니다.",
                "knowledge_en": r"$\text{Area}(\triangle\mathrm{PFQ}) = \frac{1}{2}(2c)(c\tan\theta) = \frac{\sqrt{7}}{3}c^2 = 6\sqrt{7}$.",
                "questions": [
                    {
                        "level_label": "초점 거리 c 디딤돌 3",
                        "level_label_en": "Finding c Step 3",
                        "stem": r"$\frac{\sqrt{7}}{3}c^2 = 6\sqrt{7}$에서 $c^2 = 18$입니다. 양수 $c$의 값은?",
                        "stem_en": r"From $\frac{\sqrt{7}}{3}c^2 = 6\sqrt{7}$, we get $c^2 = 18$. What is $c > 0$?",
                        "options": [r"$2\sqrt{2}$", r"$2\sqrt{3}$", r"$3\sqrt{2}$", r"$3\sqrt{3}$", r"$6$"],
                        "answer": 3,
                        "exp": r"$c = \sqrt{18} = 3\sqrt{2}$입니다.",
                        "exp_en": r"$c = 3\sqrt{2}$."
                    }
                ]
            },
            {
                "title": r"🌳 4단계 · [둘레의 길이 식] 삼각형 $\mathrm{F'RQ}$의 둘레를 $c$로 나타내기",
                "title_en": r"🌳 Step 4 · [Perimeter Formula] Expressing the perimeter of $\triangle\mathrm{F'RQ}$ in terms of $c$",
                "knowledge": r"선분 $\mathrm{FQ}$가 타원과 만나는 점이 $\mathrm{R}$이므로, 삼각형 $\mathrm{F'RQ}$의 둘레는 $\overline{\mathrm{F'Q}} + \overline{\mathrm{F'R}} + \overline{\mathrm{RQ}} = 2a + (\overline{\mathrm{F'R}} + \overline{\mathrm{RF}}) + \overline{\mathrm{FQ}} = 2a + 2a + 2c = 4a + 2c$입니다! $2a = 3c$이므로 $4a + 2c = 6c + 2c = 8c$입니다.",
                "knowledge_en": r"Using $\overline{\mathrm{F'R}} + \overline{\mathrm{RF}} = 2a$ and $\overline{\mathrm{FQ}} = 2c$, the perimeter of $\triangle\mathrm{F'RQ}$ is $2a + 2a + 2c = 4a + 2c = 6c + 2c = 8c$.",
                "questions": [
                    {
                        "level_label": "둘레 식 정리 디딤돌 4",
                        "level_label_en": "Perimeter Expression Step 4",
                        "stem": r"$2a = 3c$일 때, 삼각형 $\mathrm{F'RQ}$의 둘레의 길이 $4a + 2c$를 $c$로 나타내면?",
                        "stem_en": r"Given $2a = 3c$, what is $4a + 2c$ in terms of $c$?",
                        "options": [r"$5c$", r"$6c$", r"$7c$", r"$8c$", r"$9c$"],
                        "answer": 4,
                        "exp": r"$2(3c) + 2c = 6c + 2c = 8c$입니다.",
                        "exp_en": r"$8c$."
                    }
                ]
            },
            {
                "title": r"💎 5단계 · [최종 종합] $8c = 8 \times 3\sqrt{2}$ 계산하기",
                "title_en": r"💎 Step 5 · [Final Synthesis] Computing $8c = 8 \times 3\sqrt{2}$",
                "knowledge": r"$c = 3\sqrt{2}$를 $8c$에 대입하면 $24\sqrt{2}$가 완성됩니다.",
                "knowledge_en": r"$8 \times 3\sqrt{2} = 24\sqrt{2}$.",
                "questions": [
                    {
                        "level_label": "최종 종합 디딤돌 5",
                        "level_label_en": "Final Synthesis Step 5",
                        "stem": r"삼각형 $\mathrm{F'RQ}$의 둘레의 길이 $8c$는?",
                        "stem_en": r"What is the perimeter $8c$ of $\triangle\mathrm{F'RQ}$?",
                        "options": [r"$18\sqrt{2}$", r"$21\sqrt{2}$", r"$24\sqrt{2}$", r"$27\sqrt{2}$", r"$30\sqrt{2}$"],
                        "answer": 3,
                        "exp": r"$8 \times 3\sqrt{2} = 24\sqrt{2}$이므로 정답은 ③입니다.",
                        "exp_en": r"$24\sqrt{2}$ (choice ③)."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"두 초점이 $\mathrm{F}(c, 0), \mathrm{F'}(-c, 0)$ ($c > 0$)이고 장축의 길이가 $2a$인 타원이 있다. 타원 위의 점 $\mathrm{P}$에 대하여 직선 $\mathrm{F'P}$ 위의 점 $\mathrm{Q}$가 $\overline{\mathrm{F'Q}} = 2a$, $\overline{\mathrm{F'F}} = \overline{\mathrm{FQ}}$를 만족시킨다. 선분 $\mathrm{FQ}$가 타원과 만나는 점을 $\mathrm{R}$이라 하자. $\tan(\angle\mathrm{F'QF}) = \dfrac{\sqrt{7}}{3}$이고 삼각형 $\mathrm{PFQ}$의 넓이가 $6\sqrt{7}$일 때, 삼각형 $\mathrm{F'RQ}$의 둘레의 길이는? [4점]",
            "stem_en": r"An ellipse has foci $\mathrm{F}(c, 0), \mathrm{F'}(-c, 0)$ ($c > 0$) and major axis $2a$. For a point $\mathrm{P}$ on the ellipse, point $\mathrm{Q}$ on ray $\mathrm{F'P}$ satisfies $\overline{\mathrm{F'Q}} = 2a$ and $\overline{\mathrm{F'F}} = \overline{\mathrm{FQ}}$. Segment $\mathrm{FQ}$ meets the ellipse at $\mathrm{R}$. Given $\tan(\angle\mathrm{F'QF}) = \dfrac{\sqrt{7}}{3}$ and $\text{Area}(\triangle\mathrm{PFQ}) = 6\sqrt{7}$, what is the perimeter of $\triangle\mathrm{F'RQ}$? [4 points]",
            "options": [r"$18\sqrt{2}$", r"$21\sqrt{2}$", r"$24\sqrt{2}$", r"$27\sqrt{2}$", r"$30\sqrt{2}$"],
            "answer": 3,
            "exp": r"타원의 정의에서 $\overline{\mathrm{PF}} = \overline{\mathrm{PQ}}$이므로 $\triangle\mathrm{PFQ}$는 이등변삼각형입니다. $\tan\theta = \dfrac{\sqrt{7}}{3} \implies \cos\theta = \dfrac{3}{4}$에서 $2a = 3c$이고, $\text{Area}(\triangle\mathrm{PFQ}) = \dfrac{\sqrt{7}}{3}c^2 = 6\sqrt{7} \implies c = 3\sqrt{2}$입니다. 따라서 $\triangle\mathrm{F'RQ}$의 둘레는 $4a + 2c = 8c = 24\sqrt{2}$입니다.",
            "exp_en": r"By the ellipse definition, $\overline{\mathrm{PF}} = \overline{\mathrm{PQ}}$. From $\tan\theta = \dfrac{\sqrt{7}}{3}$ ($\cos\theta = \dfrac{3}{4}$), we get $2a = 3c$ and $\text{Area}(\triangle\mathrm{PFQ}) = \dfrac{\sqrt{7}}{3}c^2 = 6\sqrt{7} \implies c = 3\sqrt{2}$. The perimeter of $\triangle\mathrm{F'RQ}$ is $4a + 2c = 8c = 24\sqrt{2}$.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>타원의 정의($\overline{\mathrm{F'P}} + \overline{\mathrm{PF}} = 2a$)를 이용하여 숨겨진 이등변삼각형($\overline{\mathrm{PF}} = \overline{\mathrm{PQ}}$)을 발견</b>하는 기하 4점 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 타원의 정의로 이등변삼각형 $\mathrm{PFQ}$ 발견</b><br>
  타원의 정의에 의해 $\overline{\mathrm{F'P}} + \overline{\mathrm{PF}} = 2a$이고, 조건에서 $\overline{\mathrm{F'Q}} = \overline{\mathrm{F'P}} + \overline{\mathrm{PQ}} = 2a$이므로:<br>
  $$\overline{\mathrm{PF}} = \overline{\mathrm{PQ}}$$
  따라서 삼각형 $\mathrm{PFQ}$는 $\overline{\mathrm{PF}} = \overline{\mathrm{PQ}}$인 이등변삼각형입니다.<br><br>
  <b>2단계: 삼각비로 $2a = 3c$와 $c = 3\sqrt{2}$ 구하기</b><br>
  $\angle\mathrm{F'QF} = \theta$라 하면 $\tan\theta = \frac{\sqrt{7}}{3} \implies \cos\theta = \frac{3}{4}$입니다.<br>
  $\overline{\mathrm{F'F}} = \overline{\mathrm{FQ}} = 2c$인 이등변삼각형 $\mathrm{F'FQ}$에서:<br>
  $$\overline{\mathrm{F'Q}} = 2a = 2(2c\cos\theta) = 4c \times \frac{3}{4} = 3c$$
  또한 이등변삼각형 $\mathrm{PFQ}$에서 밑변은 $\overline{\mathrm{FQ}} = 2c$이고 높이는 $c\tan\theta = \frac{\sqrt{7}}{3}c$이므로:<br>
  $$\text{Area}(\triangle\mathrm{PFQ}) = \frac{1}{2} \times 2c \times \frac{\sqrt{7}}{3}c = \frac{\sqrt{7}}{3}c^2 = 6\sqrt{7} \implies c^2 = 18 \implies c = 3\sqrt{2}$$<br>
  <b>3단계: 삼각형 $\mathrm{F'RQ}$의 둘레의 길이 구하기</b><br>
  점 $\mathrm{R}$도 타원 위의 점이므로 $\overline{\mathrm{F'R}} + \overline{\mathrm{RF}} = 2a$입니다.<br>
  $$\text{둘레}(\triangle\mathrm{F'RQ}) = \overline{\mathrm{F'Q}} + \overline{\mathrm{F'R}} + \overline{\mathrm{RQ}} = 2a + (\overline{\mathrm{F'R}} + \overline{\mathrm{RF}}) + \overline{\mathrm{FQ}} = 4a + 2c = 6c + 2c = 8c = 24\sqrt{2}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 삼각형 $\mathrm{F'RQ}$의 둘레의 길이는 $24\sqrt{2}$이므로 정답은 <b>③번</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem uses the <b>definition of an ellipse</b> to identify two similar isosceles triangles $\triangle\mathrm{F'FQ}$ and $\triangle\mathrm{FPQ}$.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Isosceles triangles</b><br>
  From $\overline{\mathrm{F'P}} + \overline{\mathrm{PF}} = 2a = \overline{\mathrm{F'P}} + \overline{\mathrm{PQ}}$, we have $\overline{\mathrm{PF}} = \overline{\mathrm{PQ}}$.<br>
  With $\tan\theta = \frac{\sqrt{7}}{3}$ ($\cos\theta = \frac{3}{4}$) and $\overline{\mathrm{F'F}} = \overline{\mathrm{FQ}} = 2c$, we get $2a = 4c\cos\theta = 3c$.<br><br>
  <b>Step 2: Area and perimeter</b><br>
  $$\text{Area}(\triangle\mathrm{PFQ}) = \frac{1}{2}(2c)(c\tan\theta) = \frac{\sqrt{7}}{3}c^2 = 6\sqrt{7} \implies c = 3\sqrt{2}$$
  $$\text{Perimeter}(\triangle\mathrm{F'RQ}) = 2a + (\overline{\mathrm{F'R}} + \overline{\mathrm{RF}}) + 2c = 4a + 2c = 8c = 24\sqrt{2}$$
</p>

<h4>✨ [Final Answer & Practical Tips]</h4>
<p>
  The correct answer is <b>choice ③ ($24\sqrt{2}$)</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 기하 29번: c2610g29 (단답형)
    # -------------------------------------------------------------------------
    {
        "slug": "c2610g29",
        "qNum": "기하 29",
        "subject": "기하",
        "title": "[2026학년도 10월 고3 기하 29번] 구와 평면의 교선 및 두 평면이 이루는 각과 정사영의 넓이",
        "title_en": "[2026 AY Oct Exam Grade 12 Geometry #29] Sphere-Plane Intersection, Dihedral Angle, and Area of Orthogonal Projection",
        "summary_ko": r"삼각형 $\mathrm{QRS}$의 넓이 $3\sqrt{10}$에서 $r=1$을 구하고, $yz$평면 단면 벡터로 이면각의 코사인 $\dfrac{4}{5}$를 구해 정사영 넓이 $S=\dfrac{8\sqrt{10}}{5},\ 25S^2=640$ 도출하기",
        "summary_en": r"Find $r=1$ from $\text{Area}(\triangle\mathrm{QRS})=3\sqrt{10}$, compute $\cos\theta=\dfrac{4}{5}$ between planes via $yz$-plane cross-section, and obtain $S=\dfrac{8\sqrt{10}}{5}$ and $25S^2=640$.",
        "tags": ["기하", "공간도형과공간좌표", "정사영", "이면각", "구의방정식", "단답형", "29번"],
        "symbols": [
            {"sym": r"$S' = S_0 \cos\theta$", "desc": r"두 평면이 이루는 각이 $\theta$일 때 정사영의 넓이 공식", "desc_en": "Orthogonal projection area formula."},
            {"sym": r"$\overrightarrow{RA} = (0, -1, 3),\quad \overrightarrow{RQ} = (0, 1, 3)$", "desc": "교선 PR(x축과 평행)에 수직인 yz평면 위 두 직선의 방향벡터", "desc_en": "Vectors in the yz-plane perpendicular to the line of intersection PR."}
        ],
        "levels": [
            {
                "title": r"🔰 1단계 · [초등 삼각형의 넓이] 밑변이 $6$이고 넓이가 $3\sqrt{10}$인 삼각형의 높이 구하기",
                "title_en": r"🔰 Step 1 · [Elementary Triangle Area] Finding the altitude of $\triangle\mathrm{QRS}$ with base $6$ and area $3\sqrt{10}$",
                "knowledge": r"구 $S_2$와 평면이 만나 생기는 원에서 지름 $\overline{\mathrm{QS}} = 6$을 밑변으로 하는 삼각형 $\mathrm{QRS}$의 넓이가 $3\sqrt{10}$입니다. 초등학교 삼각형 넓이 공식 $\frac{1}{2} \times 6 \times H = 3\sqrt{10}$으로 높이를 바로 구할 수 있습니다!",
                "knowledge_en": r"Using the elementary triangle area formula $\frac{1}{2} \times 6 \times H = 3\sqrt{10}$ with base $\overline{\mathrm{QS}} = 6$, we immediately find the altitude $H$.",
                "questions": [
                    {
                        "level_label": "초등 삼각형 넓이 디딤돌 1",
                        "level_label_en": "Elementary Triangle Area Step 1",
                        "stem": r"초등학교 삼각형 넓이 공식 $\frac{1}{2} \times 6 \times H = 3\sqrt{10}$에서 삼각형 $\mathrm{QRS}$의 높이 $H$는?",
                        "stem_en": r"From $\frac{1}{2} \times 6 \times H = 3\sqrt{10}$, what is the altitude $H$?",
                        "options": [r"$\sqrt{5}$", r"$\sqrt{10}$", r"$2\sqrt{5}$", r"$2\sqrt{10}$", r"$3\sqrt{10}$"],
                        "answer": 2,
                        "exp": r"$3H = 3\sqrt{10}$이므로 $H = \sqrt{10}$입니다.",
                        "exp_en": r"$H = \sqrt{10}$."
                    }
                ]
            },
            {
                "title": "🌿 2단계 · [반지름 $r$ 결정] $H^2 = (2 - r)^2 + 3^2 = 10$에서 $r$ 구하기",
                "title_en": "🌿 Step 2 · [Finding Radius $r$] Solving $(2 - r)^2 + 9 = 10$ for $r < 2$",
                "knowledge": r"단면인 $yz$평면에서 점 $\mathrm{R}(0, r, 0)$과 점 $\mathrm{Q}(0, 2, 3)$ 사이의 거리가 $H = \sqrt{10}$이므로 $(2 - r)^2 + 3^2 = 10$입니다.",
                "knowledge_en": r"In the $yz$-plane cross-section, the distance between $\mathrm{R}(0, r, 0)$ and $\mathrm{Q}(0, 2, 3)$ is $\sqrt{(2-r)^2 + 3^2} = \sqrt{10}$.",
                "questions": [
                    {
                        "level_label": "반지름 r 구하기 디딤돌 2",
                        "level_label_en": "Finding r Step 2",
                        "stem": r"$(2 - r)^2 + 9 = 10$에서 $0 < r < 2$를 만족시키는 상수 $r$의 값은?",
                        "stem_en": r"From $(2 - r)^2 + 9 = 10$ with $0 < r < 2$, what is $r$?",
                        "options": [r"$\frac{1}{2}$", r"$1$", r"$\frac{3}{2}$", r"$\sqrt{2}$", r"$\sqrt{3}$"],
                        "answer": 2,
                        "exp": r"$(2 - r)^2 = 1$이고 $r < 2$이므로 $r = 1$입니다.",
                        "exp_en": r"$r = 1$."
                    }
                ]
            },
            {
                "title": r"🌱 3단계 · [이면각의 코사인] 두 평면이 이루는 각 $\cos\theta$ 구하기",
                "title_en": r"🌱 Step 3 · [Dihedral Angle] Finding $\cos\theta$ between the two planes",
                "knowledge": r"두 평면 $\mathrm{ARP}$와 $\mathrm{PRQ}$의 교선 $\mathrm{PR}$은 $x$축에 평행합니다. 따라서 $yz$평면 위의 두 벡터 $\overrightarrow{\mathrm{RA}} = (-1, 3)$과 $\overrightarrow{\mathrm{RQ}} = (1, 3)$이 이루는 각이 바로 두 평면의 이면각 $\theta$입니다!",
                "knowledge_en": r"Since the intersection line $\mathrm{PR}$ is parallel to the $x$-axis, the dihedral angle $\theta$ is the angle between $\overrightarrow{\mathrm{RA}} = (-1, 3)$ and $\overrightarrow{\mathrm{RQ}} = (1, 3)$ in the $yz$-plane.",
                "questions": [
                    {
                        "level_label": "이면각 코사인 디딤돌 3",
                        "level_label_en": "Dihedral Cosine Step 3",
                        "stem": r"두 벡터 $(-1, 3)$과 $(1, 3)$에 대하여 $\cos\theta = \frac{(-1)(1) + 3(3)}{\sqrt{10}\sqrt{10}}$을 계산한 값은?",
                        "stem_en": r"What is $\cos\theta = \frac{(-1)(1) + 3(3)}{\sqrt{10}\sqrt{10}}$?",
                        "options": [r"$\frac{1}{5}$", r"$\frac{2}{5}$", r"$\frac{3}{5}$", r"$\frac{4}{5}$", r"$\frac{9}{10}$"],
                        "answer": 4,
                        "exp": r"$\frac{-1 + 9}{10} = \frac{8}{10} = \frac{4}{5}$입니다.",
                        "exp_en": r"$\cos\theta = \frac{8}{10} = \frac{4}{5}$."
                    }
                ]
            },
            {
                "title": r"🌳 4단계 · [정사영의 넓이 $S$] $\text{Area}(\triangle\mathrm{ARP}) \times \cos\theta$ 구하기",
                "title_en": r"🌳 Step 4 · [Projected Area $S$] Computing $\text{Area}(\triangle\mathrm{ARP}) \times \cos\theta$",
                "knowledge": r"삼각형 $\mathrm{ARP}$는 밑변 $\overline{\mathrm{PR}} = 4$이고 높이가 $\overline{\mathrm{RA}} = \sqrt{10}$이므로 넓이는 $\frac{1}{2} \times 4 \times \sqrt{10} = 2\sqrt{10}$입니다. 따라서 정사영의 넓이는 $S = 2\sqrt{10} \times \frac{4}{5} = \frac{8\sqrt{10}}{5}$입니다.",
                "knowledge_en": r"$\text{Area}(\triangle\mathrm{ARP}) = \frac{1}{2}(4)(\sqrt{10}) = 2\sqrt{10}$, so $S = 2\sqrt{10} \times \frac{4}{5} = \frac{8\sqrt{10}}{5}$.",
                "questions": [
                    {
                        "level_label": "정사영 넓이 디딤돌 4",
                        "level_label_en": "Projection Area Step 4",
                        "stem": r"$\text{Area}(\triangle\mathrm{ARP}) = 2\sqrt{10}$이고 $\cos\theta = \frac{4}{5}$일 때, 정사영의 넓이 $S = 2\sqrt{10} \times \frac{4}{5}$는?",
                        "stem_en": r"With $\text{Area}(\triangle\mathrm{ARP}) = 2\sqrt{10}$ and $\cos\theta = \frac{4}{5}$, what is $S$?",
                        "options": [
                            r"$\frac{4\sqrt{10}}{5}$",
                            r"$\frac{6\sqrt{10}}{5}$",
                            r"$\frac{8\sqrt{10}}{5}$",
                            r"$2\sqrt{10}$",
                            r"$\frac{12\sqrt{10}}{5}$"
                        ],
                        "answer": 3,
                        "exp": r"$S = \frac{8\sqrt{10}}{5}$입니다.",
                        "exp_en": r"$S = \frac{8\sqrt{10}}{5}$."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [최종 종합] $25S^2$의 값 계산하기",
                "title_en": "💎 Step 5 · [Final Synthesis] Computing $25S^2$",
                "knowledge": r"$S = \frac{8\sqrt{10}}{5}$를 제곱하고 $25$를 곱하면 $25 \times \frac{64 \times 10}{25} = 640$입니다.",
                "knowledge_en": r"$25S^2 = 25 \times \frac{640}{25} = 640$.",
                "questions": [
                    {
                        "level_label": "최종 종합 디딤돌 5",
                        "level_label_en": "Final Synthesis Step 5",
                        "stem": r"$S = \frac{8\sqrt{10}}{5}$일 때, $25S^2$의 값은?",
                        "stem_en": r"Given $S = \frac{8\sqrt{10}}{5}$, what is $25S^2$?",
                        "options": [r"$480$", r"$540$", r"$600$", r"$640$", r"$720$"],
                        "answer": 4,
                        "exp": r"$25 \times \frac{640}{25} = 640$입니다.",
                        "exp_en": r"$25S^2 = 640$."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"좌표공간에서 두 구 $S_1, S_2$와 평면의 교선 위에 놓인 점 $\mathrm{A}, \mathrm{P}, \mathrm{Q}, \mathrm{R}, \mathrm{S}$에 대하여 삼각형 $\mathrm{QRS}$의 넓이가 $3\sqrt{10}$이다. 삼각형 $\mathrm{ARP}$의 평면 $\mathrm{PRQ}$ 위로의 정사영의 넓이를 $S$라 할 때, $25S^2$의 값을 구하시오. [4점]",
            "stem_en": r"In 3D coordinate space, for spheres $S_1, S_2$ and points $\mathrm{A}, \mathrm{P}, \mathrm{Q}, \mathrm{R}, \mathrm{S}$ satisfying the given conditions with $\text{Area}(\triangle\mathrm{QRS}) = 3\sqrt{10}$, let $S$ be the area of the orthogonal projection of $\triangle\mathrm{ARP}$ onto plane $\mathrm{PRQ}$. Find $25S^2$. [4 points]",
            "options": [r"$480$", r"$540$", r"$600$", r"$640$", r"$720$"],
            "answer": 4,
            "exp": r"$\text{Area}(\triangle\mathrm{QRS}) = \dfrac{1}{2} \times 6 \times \sqrt{(2-r)^2+9} = 3\sqrt{10}$에서 $r = 1$이고, 두 평면 $\mathrm{ARP}$와 $\mathrm{PRQ}$가 이루는 각 $\theta$에 대하여 $\cos\theta = \dfrac{4}{5}$입니다. $\text{Area}(\triangle\mathrm{ARP}) = 2\sqrt{10}$이므로 $S = \dfrac{8\sqrt{10}}{5}$이고 $25S^2 = 640$입니다.",
            "exp_en": r"From $\text{Area}(\triangle\mathrm{QRS}) = 3\sqrt{10}$, we find $r = 1$. The dihedral angle $\theta$ satisfies $\cos\theta = \dfrac{4}{5}$, and $\text{Area}(\triangle\mathrm{ARP}) = 2\sqrt{10}$, giving $S = \dfrac{8\sqrt{10}}{5}$ and $25S^2 = 640$.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>구와 평면의 교선(원)의 기하학적 성질과 두 평면이 이루는 이면각을 통한 정사영의 넓이</b>를 구하는 공간좌표·공간도형 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 삼각형 $\mathrm{QRS}$의 넓이로 $r = 1$ 결정</b><br>
  지름 $\overline{\mathrm{QS}} = 6$을 밑변으로 하는 삼각형 $\mathrm{QRS}$에서 높이는 $\sqrt{(2-r)^2 + 3^2}$이므로:<br>
  $$\text{Area}(\triangle\mathrm{QRS}) = \frac{1}{2} \times 6 \times \sqrt{(2-r)^2 + 9} = 3\sqrt{10} \implies (2-r)^2 = 1$$
  $0 < r < 2$이므로 $r = 1$입니다.<br><br>
  <b>2단계: 두 평면 $\mathrm{ARP}$와 $\mathrm{PRQ}$가 이루는 각 $\theta$ 구하기</b><br>
  교선 $\mathrm{PR}$이 $x$축에 평행하므로 $yz$평면으로 자른 단면에서 두 평면의 방향은 $\overrightarrow{\mathrm{RA}} = (0, -1, 3)$과 $\overrightarrow{\mathrm{RQ}} = (0, 1, 3)$입니다:<br>
  $$\cos\theta = \frac{(-1)(1) + 3(3)}{\sqrt{10}\sqrt{10}} = \frac{8}{10} = \frac{4}{5}$$<br>
  <b>3단계: 정사영의 넓이 $S$와 $25S^2$ 계산</b><br>
  $\overline{\mathrm{PR}} = 4$, 높이가 $\overline{\mathrm{RA}} = \sqrt{10}$이므로 $\text{Area}(\triangle\mathrm{ARP}) = \frac{1}{2} \times 4 \times \sqrt{10} = 2\sqrt{10}$입니다.<br>
  $$S = \text{Area}(\triangle\mathrm{ARP})\cos\theta = 2\sqrt{10} \times \frac{4}{5} = \frac{8\sqrt{10}}{5} \implies 25S^2 = 640$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 구하는 값은 <b>$640$</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem computes the <b>orthogonal projection area</b> between two planes intersecting along a line parallel to the $x$-axis.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Determine $r = 1$</b><br>
  $$\text{Area}(\triangle\mathrm{QRS}) = \frac{1}{2}(6)\sqrt{(2-r)^2 + 9} = 3\sqrt{10} \implies r = 1$$<br>
  <b>Step 2: Dihedral angle and projected area</b><br>
  In the $yz$-plane, $\overrightarrow{\mathrm{RA}} = (-1, 3)$ and $\overrightarrow{\mathrm{RQ}} = (1, 3)$ give $\cos\theta = \frac{8}{10} = \frac{4}{5}$.<br>
  Since $\text{Area}(\triangle\mathrm{ARP}) = \frac{1}{2}(4)\sqrt{10} = 2\sqrt{10}$, we obtain $S = \frac{8\sqrt{10}}{5}$ and $25S^2 = 640$.
</p>

<h4>✨ [Final Answer & Practical Tips]</h4>
<p>
  The final answer is <b>$640$</b>.
</p>"""
        }
    },

    # -------------------------------------------------------------------------
    # 기하 30번: c2610g30 (단답형 킬러)
    # -------------------------------------------------------------------------
    {
        "slug": "c2610g30",
        "qNum": "기하 30",
        "subject": "기하",
        "title": "[2026학년도 10월 고3 기하 30번] 평면벡터의 선형결합(내분점)과 내적의 계산",
        "title_en": "[2026 AY Oct Exam Grade 12 Geometry #30] Linear Combination of Plane Vectors, Internal Division, and Dot Product",
        "summary_ko": r"조건 (가)에서 점 $\mathrm{P}$가 $\mathrm{AC}$를 $3:2$로 내분함을 찾고, 조건 (나)와 넓이 $\dfrac{4\sqrt{5}}{5}$로부터 $\overrightarrow{\mathrm{AB}}\cdot\overrightarrow{\mathrm{AC}}=1$을 구하여 $\overrightarrow{\mathrm{AQ}}\cdot\overrightarrow{\mathrm{BC}}=\dfrac{40}{3}$ 도출하기",
        "summary_en": r"Deduce from (가) that $\mathrm{P}$ divides $\mathrm{AC}$ in $3:2$, use (나) and $\text{Area}(\triangle\mathrm{APQ})=\dfrac{4\sqrt{5}}{5}$ to find $\overrightarrow{\mathrm{AB}}\cdot\overrightarrow{\mathrm{AC}}=1$, and compute $\overrightarrow{\mathrm{AQ}}\cdot\overrightarrow{\mathrm{BC}}=\dfrac{40}{3}$ ($p+q=43$).",
        "tags": ["기하", "평면벡터", "위치벡터", "내분점", "벡터의내적", "단답형", "30번"],
        "symbols": [
            {"sym": r"$2\overrightarrow{PA} + 3\overrightarrow{PC} = \vec{0}$", "desc": "점 P가 선분 AC를 3:2로 내분하는 점임을 뜻하는 벡터 등식", "desc_en": "Vector identity showing P divides segment AC internally in the ratio 3:2."},
            {"sym": r"$\overrightarrow{AQ} = \overrightarrow{AC} - \dfrac{2}{3}\overrightarrow{AB}$", "desc": "시점을 A로 통일하여 나타낸 벡터 AQ", "desc_en": "Vector AQ expressed with initial point A."},
            {"sym": r"$\overrightarrow{AB} \cdot \overrightarrow{AC} = |\overrightarrow{AB}||\overrightarrow{AC}|\cos A = 1$", "desc": "삼각형 ABC의 넓이로부터 구한 두 변 벡터의 내적", "desc_en": "Dot product of AB and AC derived from the area of triangle ABC."}
        ],
        "levels": [
            {
                "title": r"🔰 1단계 · [초등 시소 균형과 비례배분] $2\overrightarrow{\mathrm{PA}} + 3\overrightarrow{\mathrm{PC}} = \vec{0}$에서 내분비 찾기",
                "title_en": r"🔰 Step 1 · [Elementary Seesaw Ratio] Finding the internal division ratio from $2\overrightarrow{\mathrm{PA}} + 3\overrightarrow{\mathrm{PC}} = \vec{0}$",
                "knowledge": r"조건 (가)의 $\overrightarrow{\mathrm{AB}} + \overrightarrow{\mathrm{PB}} = 2\overrightarrow{\mathrm{BC}} + 3\overrightarrow{\mathrm{PC}}$에서 $\overrightarrow{\mathrm{AB}} - 2\overrightarrow{\mathrm{BC}}$를 정리하면 $2\overrightarrow{\mathrm{PA}} + 3\overrightarrow{\mathrm{PC}} = \vec{0}$이 됩니다! 초등학교 시소 원리처럼 무게가 $2 : 3$이면 거리의 비는 반대로 $\overline{\mathrm{AP}} : \overline{\mathrm{PC}} = 3 : 2$이므로 $\overline{\mathrm{AP}}$는 전체 $\overline{\mathrm{AC}}$의 $\frac{3}{3 + 2} = \frac{3}{5}$입니다!",
                "knowledge_en": r"Condition (가) simplifies to $2\overrightarrow{\mathrm{PA}} + 3\overrightarrow{\mathrm{PC}} = \vec{0}$. Like an elementary seesaw, $\overline{\mathrm{AP}} : \overline{\mathrm{PC}} = 3 : 2$, so $\overline{\mathrm{AP}} = \frac{3}{5}\overline{\mathrm{AC}}$.",
                "questions": [
                    {
                        "level_label": "초등 비례배분 디딤돌 1",
                        "level_label_en": "Elementary Ratio Step 1",
                        "stem": r"초등학교 비례배분 원리에 따라 점 $\mathrm{P}$가 선분 $\mathrm{AC}$를 $3 : 2$로 나누는 점일 때, $\overline{\mathrm{AP}}$의 길이는 전체 $\overline{\mathrm{AC}}$의 몇 분의 몇인가요?",
                        "stem_en": r"Using elementary proportional division, if $\mathrm{P}$ divides $\mathrm{AC}$ in the ratio $3 : 2$, what fraction of $\overline{\mathrm{AC}}$ is $\overline{\mathrm{AP}}$?",
                        "options": [r"$\frac{1}{5}$", r"$\frac{2}{5}$", r"$\frac{1}{2}$", r"$\frac{3}{5}$", r"$\frac{2}{3}$"],
                        "answer": 4,
                        "exp": r"전체 $3 + 2 = 5$칸 중 $3$칸이므로 $\frac{3}{5}$입니다.",
                        "exp_en": r"$\frac{3}{3 + 2} = \frac{3}{5}$."
                    }
                ]
            },
            {
                "title": r"🌿 2단계 · [삼각형 넓이 비] $\text{Area}(\triangle\mathrm{APQ}) = \dfrac{4\sqrt{5}}{5}$에서 $\text{Area}(\triangle\mathrm{ABC})$ 구하기",
                "title_en": r"🌿 Step 2 · [Area Ratio] Finding $\text{Area}(\triangle\mathrm{ABC})$ from $\text{Area}(\triangle\mathrm{APQ}) = \dfrac{4\sqrt{5}}{5}$",
                "knowledge": r"조건 (나)에서 $\overrightarrow{\mathrm{PQ}} = \frac{2}{3}\overrightarrow{\mathrm{BP}}$이므로 $\text{Area}(\triangle\mathrm{ABP}) = \frac{3}{2}\text{Area}(\triangle\mathrm{APQ})$이고, 다시 $\overline{\mathrm{AC}} = \frac{5}{3}\overline{\mathrm{AP}}$이므로 $\text{Area}(\triangle\mathrm{ABC}) = \frac{5}{3}\text{Area}(\triangle\mathrm{ABP}) = \frac{5}{3} \times \frac{3}{2} \times \frac{4\sqrt{5}}{5} = 2\sqrt{5}$입니다!",
                "knowledge_en": r"Since $\overrightarrow{\mathrm{PQ}} = \frac{2}{3}\overrightarrow{\mathrm{BP}}$ and $\overline{\mathrm{AP}} = \frac{3}{5}\overline{\mathrm{AC}}$, $\text{Area}(\triangle\mathrm{ABC}) = \frac{5}{3} \times \frac{3}{2}\text{Area}(\triangle\mathrm{APQ}) = 2\sqrt{5}$.",
                "questions": [
                    {
                        "level_label": "삼각형 ABC 넓이 디딤돌 2",
                        "level_label_en": "Area of ABC Step 2",
                        "stem": r"$\overline{\mathrm{AB}} = \overline{\mathrm{AC}} = 3$인 삼각형 $\mathrm{ABC}$의 넓이 $\frac{1}{2} \times 3 \times 3 \times \sin A = 2\sqrt{5}$일 때, $\sin A$의 값은?",
                        "stem_en": r"In $\triangle\mathrm{ABC}$ with $\overline{\mathrm{AB}} = \overline{\mathrm{AC}} = 3$ and area $\frac{9}{2}\sin A = 2\sqrt{5}$, what is $\sin A$?",
                        "options": [
                            r"$\frac{\sqrt{5}}{9}$",
                            r"$\frac{2\sqrt{5}}{9}$",
                            r"$\frac{\sqrt{5}}{3}$",
                            r"$\frac{4\sqrt{5}}{9}$",
                            r"$\frac{5\sqrt{5}}{9}$"
                        ],
                        "answer": 4,
                        "exp": r"$\frac{9}{2}\sin A = 2\sqrt{5} \implies \sin A = \frac{4\sqrt{5}}{9}$입니다.",
                        "exp_en": r"$\sin A = \frac{4\sqrt{5}}{9}$."
                    }
                ]
            },
            {
                "title": r"🌱 3단계 · [내적 구하기] $\cos A$와 $\overrightarrow{\mathrm{AB}} \cdot \overrightarrow{\mathrm{AC}}$ 계산하기",
                "title_en": r"🌱 Step 3 · [Dot Product] Computing $\cos A$ and $\overrightarrow{\mathrm{AB}} \cdot \overrightarrow{\mathrm{AC}}$",
                "knowledge": r"예각 $A$에 대하여 $\cos A = \sqrt{1 - \left(\frac{4\sqrt{5}}{9}\right)^2} = \sqrt{1 - \frac{80}{81}} = \frac{1}{9}$입니다. 따라서 내적 $\overrightarrow{\mathrm{AB}} \cdot \overrightarrow{\mathrm{AC}} = 3 \times 3 \times \frac{1}{9} = 1$입니다!",
                "knowledge_en": r"For acute angle $A$, $\cos A = \sqrt{1 - \frac{80}{81}} = \frac{1}{9}$, so $\overrightarrow{\mathrm{AB}} \cdot \overrightarrow{\mathrm{AC}} = 3 \times 3 \times \frac{1}{9} = 1$.",
                "questions": [
                    {
                        "level_label": "기본 내적 디딤돌 3",
                        "level_label_en": "Base Dot Product Step 3",
                        "stem": r"$|\overrightarrow{\mathrm{AB}}| = 3$, $|\overrightarrow{\mathrm{AC}}| = 3$, $\cos A = \frac{1}{9}$일 때, 내적 $\overrightarrow{\mathrm{AB}} \cdot \overrightarrow{\mathrm{AC}}$의 값은?",
                        "stem_en": r"With $|\overrightarrow{\mathrm{AB}}| = |\overrightarrow{\mathrm{AC}}| = 3$ and $\cos A = \frac{1}{9}$, what is $\overrightarrow{\mathrm{AB}} \cdot \overrightarrow{\mathrm{AC}}$?",
                        "options": [r"$0$", r"$1$", r"$2$", r"$3$", r"$9$"],
                        "answer": 2,
                        "exp": r"$3 \times 3 \times \frac{1}{9} = 1$입니다.",
                        "exp_en": r"$3 \times 3 \times \frac{1}{9} = 1$."
                    }
                ]
            },
            {
                "title": r"🌳 4단계 · [벡터 전개] $\overrightarrow{\mathrm{AQ}} \cdot \overrightarrow{\mathrm{BC}}$를 전개하여 계산하기",
                "title_en": r"🌳 Step 4 · [Expanding Dot Product] Evaluating $\overrightarrow{\mathrm{AQ}} \cdot \overrightarrow{\mathrm{BC}}$",
                "knowledge": r"$\overrightarrow{\mathrm{AQ}} = \overrightarrow{\mathrm{AP}} + \overrightarrow{\mathrm{PQ}} = \frac{3}{5}\overrightarrow{\mathrm{AC}} + \frac{2}{3}\left(\frac{3}{5}\overrightarrow{\mathrm{AC}} - \overrightarrow{\mathrm{AB}}\right) = \overrightarrow{\mathrm{AC}} - \frac{2}{3}\overrightarrow{\mathrm{AB}}$이고, $\overrightarrow{\mathrm{BC}} = \overrightarrow{\mathrm{AC}} - \overrightarrow{\mathrm{AB}}$입니다! 두 벡터를 내적하면 $|\overrightarrow{\mathrm{AC}}|^2 - \frac{5}{3}(\overrightarrow{\mathrm{AB}} \cdot \overrightarrow{\mathrm{AC}}) + \frac{2}{3}|\overrightarrow{\mathrm{AB}}|^2$이 됩니다.",
                "knowledge_en": r"Since $\overrightarrow{\mathrm{AQ}} = \overrightarrow{\mathrm{AC}} - \frac{2}{3}\overrightarrow{\mathrm{AB}}$ and $\overrightarrow{\mathrm{BC}} = \overrightarrow{\mathrm{AC}} - \overrightarrow{\mathrm{AB}}$, their dot product is $|\overrightarrow{\mathrm{AC}}|^2 - \frac{5}{3}(\overrightarrow{\mathrm{AB}} \cdot \overrightarrow{\mathrm{AC}}) + \frac{2}{3}|\overrightarrow{\mathrm{AB}}|^2$.",
                "questions": [
                    {
                        "level_label": "내적 값 대입 디딤돌 4",
                        "level_label_en": "Dot Product Evaluation Step 4",
                        "stem": r"$|\overrightarrow{\mathrm{AB}}|^2 = |\overrightarrow{\mathrm{AC}}|^2 = 9$이고 $\overrightarrow{\mathrm{AB}} \cdot \overrightarrow{\mathrm{AC}} = 1$일 때, $9 - \frac{5}{3}(1) + \frac{2}{3}(9) = 15 - \frac{5}{3}$을 계산한 기약분수 $\frac{q}{p}$는?",
                        "stem_en": r"What is $9 - \frac{5}{3}(1) + \frac{2}{3}(9) = 15 - \frac{5}{3}$ in lowest terms $\frac{q}{p}$?",
                        "options": [r"$\frac{35}{3}$", r"$\frac{38}{3}$", r"$\frac{40}{3}$", r"$\frac{43}{3}$", r"$\frac{46}{3}$"],
                        "answer": 3,
                        "exp": r"$15 - \frac{5}{3} = \frac{45 - 5}{3} = \frac{40}{3}$입니다.",
                        "exp_en": r"$\frac{40}{3}$."
                    }
                ]
            },
            {
                "title": "💎 5단계 · [최종 종합] 서로소인 자연수 $p + q$ 구하기",
                "title_en": "💎 Step 5 · [Final Synthesis] Computing $p + q$",
                "knowledge": r"$\frac{q}{p} = \frac{40}{3}$에서 $p = 3, q = 40$이므로 $p + q = 43$입니다.",
                "knowledge_en": r"With $p = 3$ and $q = 40$, $p + q = 43$.",
                "questions": [
                    {
                        "level_label": "최종 종합 디딤돌 5",
                        "level_label_en": "Final Synthesis Step 5",
                        "stem": r"$p = 3$, $q = 40$일 때, $p + q$의 값은?",
                        "stem_en": r"Given $p = 3$ and $q = 40$, what is $p + q$?",
                        "options": [r"$39$", r"$41$", r"$43$", r"$45$", r"$47$"],
                        "answer": 3,
                        "exp": r"$3 + 40 = 43$입니다.",
                        "exp_en": r"$3 + 40 = 43$."
                    }
                ]
            }
        ],
        "final": {
            "stem": r"$\overline{\mathrm{AB}} = \overline{\mathrm{AC}} = 3$이고 $\angle\mathrm{BAC}$가 예각인 삼각형 $\mathrm{ABC}$와 두 점 $\mathrm{P}, \mathrm{Q}$가 조건 (가), (나)를 만족시킨다. 삼각형 $\mathrm{APQ}$의 넓이가 $\dfrac{4\sqrt{5}}{5}$일 때, $\overrightarrow{\mathrm{AQ}} \cdot \overrightarrow{\mathrm{BC}} = \dfrac{q}{p}$이다. $p + q$의 값을 구하시오. (단, $p$와 $q$는 서로소인 자연수이다.) [4점]",
            "stem_en": r"In isosceles $\triangle\mathrm{ABC}$ with $\overline{\mathrm{AB}} = \overline{\mathrm{AC}} = 3$ and acute $\angle\mathrm{BAC}$, points $\mathrm{P}, \mathrm{Q}$ satisfy conditions (가) and (나) and $\text{Area}(\triangle\mathrm{APQ}) = \dfrac{4\sqrt{5}}{5}$. If $\overrightarrow{\mathrm{AQ}} \cdot \overrightarrow{\mathrm{BC}} = \dfrac{q}{p}$ in lowest terms, find $p + q$. [4 points]",
            "options": [r"$39$", r"$41$", r"$43$", r"$45$", r"$47$"],
            "answer": 3,
            "exp": r"점 $\mathrm{P}$는 선분 $\mathrm{AC}$를 $3:2$로 내분하고 $\overrightarrow{\mathrm{PQ}} = \dfrac{2}{3}\overrightarrow{\mathrm{BP}}$이므로 $\text{Area}(\triangle\mathrm{ABC}) = 2\sqrt{5} \implies \cos A = \dfrac{1}{9} \implies \overrightarrow{\mathrm{AB}}\cdot\overrightarrow{\mathrm{AC}} = 1$입니다. $\overrightarrow{\mathrm{AQ}} = \overrightarrow{\mathrm{AC}} - \dfrac{2}{3}\overrightarrow{\mathrm{AB}}$이므로 $\overrightarrow{\mathrm{AQ}}\cdot\overrightarrow{\mathrm{BC}} = \dfrac{40}{3}$이고 $p + q = 43$입니다.",
            "exp_en": r"$\mathrm{P}$ divides $\mathrm{AC}$ in $3:2$ and $\overrightarrow{\mathrm{PQ}} = \dfrac{2}{3}\overrightarrow{\mathrm{BP}}$, giving $\text{Area}(\triangle\mathrm{ABC}) = 2\sqrt{5} \implies \overrightarrow{\mathrm{AB}}\cdot\overrightarrow{\mathrm{AC}} = 1$. Since $\overrightarrow{\mathrm{AQ}} = \overrightarrow{\mathrm{AC}} - \dfrac{2}{3}\overrightarrow{\mathrm{AB}}$, we get $\overrightarrow{\mathrm{AQ}}\cdot\overrightarrow{\mathrm{BC}} = \dfrac{40}{3}$ and $p + q = 43$.",
            "solution": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 기하 최고난도(30번) 문항으로, <b>시점 통일을 통한 위치벡터의 내분점 해석</b>과 <b>삼각형의 넓이 비를 이용한 두 기본 벡터의 내적</b>을 결합한 문제입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 조건 (가), (나)의 벡터 관계식 정리</b><br>
  조건 (가)를 시점 $\mathrm{P}$로 정리하면 $2\overrightarrow{\mathrm{PA}} + 3\overrightarrow{\mathrm{PC}} = \vec{0}$이 되어, 점 $\mathrm{P}$는 선분 $\mathrm{AC}$를 $3 : 2$로 내분하는 점입니다 ($\overrightarrow{\mathrm{AP}} = \frac{3}{5}\overrightarrow{\mathrm{AC}}$).<br>
  조건 (나)에서 $\overrightarrow{\mathrm{PQ}} = \frac{2}{3}\overrightarrow{\mathrm{BP}}$이므로 시점을 $\mathrm{A}$로 통일하면:<br>
  $$\overrightarrow{\mathrm{AQ}} = \overrightarrow{\mathrm{AP}} + \frac{2}{3}(\overrightarrow{\mathrm{AP}} - \overrightarrow{\mathrm{AB}}) = \frac{5}{3}\overrightarrow{\mathrm{AP}} - \frac{2}{3}\overrightarrow{\mathrm{AB}} = \overrightarrow{\mathrm{AC}} - \frac{2}{3}\overrightarrow{\mathrm{AB}}$$<br>
  <b>2단계: 넓이 비로 $\overrightarrow{\mathrm{AB}} \cdot \overrightarrow{\mathrm{AC}}$ 구하기</b><br>
  $$\text{Area}(\triangle\mathrm{ABC}) = \frac{5}{3}\text{Area}(\triangle\mathrm{ABP}) = \frac{5}{3} \times \frac{3}{2}\text{Area}(\triangle\mathrm{APQ}) = \frac{5}{2} \times \frac{4\sqrt{5}}{5} = 2\sqrt{5}$$
  $\frac{1}{2} \times 3 \times 3 \times \sin A = 2\sqrt{5}$에서 $\sin A = \frac{4\sqrt{5}}{9}$이고, $A$가 예각이므로 $\cos A = \frac{1}{9}$입니다.<br>
  따라서 $\overrightarrow{\mathrm{AB}} \cdot \overrightarrow{\mathrm{AC}} = 3 \times 3 \times \frac{1}{9} = 1$입니다.<br><br>
  <b>3단계: $\overrightarrow{\mathrm{AQ}} \cdot \overrightarrow{\mathrm{BC}}$ 계산</b><br>
  $$\overrightarrow{\mathrm{AQ}} \cdot \overrightarrow{\mathrm{BC}} = \left(\overrightarrow{\mathrm{AC}} - \frac{2}{3}\overrightarrow{\mathrm{AB}}\right) \cdot (\overrightarrow{\mathrm{AC}} - \overrightarrow{\mathrm{AB}}) = |\overrightarrow{\mathrm{AC}}|^2 - \frac{5}{3}(\overrightarrow{\mathrm{AB}} \cdot \overrightarrow{\mathrm{AC}}) + \frac{2}{3}|\overrightarrow{\mathrm{AB}}|^2 = 9 - \frac{5}{3} + 6 = \frac{40}{3}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 $p = 3, q = 40$이므로 $p + q =$ <b>$43$</b>입니다.
</p>""",
            "solution_en": r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem simplifies vector equations to locate points $\mathrm{P}$ and $\mathrm{Q}$, uses area ratios to find $\overrightarrow{\mathrm{AB}} \cdot \overrightarrow{\mathrm{AC}}$, and computes $\overrightarrow{\mathrm{AQ}} \cdot \overrightarrow{\mathrm{BC}}$.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Express $\overrightarrow{\mathrm{AP}}$ and $\overrightarrow{\mathrm{AQ}}$</b><br>
  Condition (가) yields $2\overrightarrow{\mathrm{PA}} + 3\overrightarrow{\mathrm{PC}} = \vec{0} \implies \overrightarrow{\mathrm{AP}} = \frac{3}{5}\overrightarrow{\mathrm{AC}}$.<br>
  Condition (나) gives $\overrightarrow{\mathrm{PQ}} = \frac{2}{3}\overrightarrow{\mathrm{BP}} \implies \overrightarrow{\mathrm{AQ}} = \overrightarrow{\mathrm{AC}} - \frac{2}{3}\overrightarrow{\mathrm{AB}}$.<br><br>
  <b>Step 2: Area ratio and dot product</b><br>
  $$\text{Area}(\triangle\mathrm{ABC}) = \frac{5}{2}\text{Area}(\triangle\mathrm{APQ}) = 2\sqrt{5} \implies \sin A = \frac{4\sqrt{5}}{9} \implies \cos A = \frac{1}{9} \implies \overrightarrow{\mathrm{AB}} \cdot \overrightarrow{\mathrm{AC}} = 1$$
  $$\overrightarrow{\mathrm{AQ}} \cdot \overrightarrow{\mathrm{BC}} = 9 - \frac{5}{3}(1) + \frac{2}{3}(9) = \frac{40}{3}$$
</p>

<h4>✨ [Final Answer & Practical Tips]</h4>
<p>
  Therefore, $p + q = 3 + 40 =$ <b>$43$</b>.
</p>"""
        }
    }
]
