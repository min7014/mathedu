# -*- coding: utf-8 -*-
"""
csat2027_part2_common2.py
2027학년도 대학수학능력시험 수학 영역 공통 12~22번 (csat27_12 ~ csat27_22)
"""

Q14_ORIG_SVG = (
    '<svg viewBox="0 0 340 250" xmlns="http://www.w3.org/2000/svg" '
    'style="display:block;max-width:340px;width:100%;height:auto;margin:12px auto;'
    'background:#ffffff;border:1px solid #cbd5e1;border-radius:10px;padding:4px">'
    '<defs>'
    '<marker id="csat27_14_arr" viewBox="0 0 8 8" refX="7" refY="4" '
    'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
    '<path d="M 0 1.2 L 7.2 4 L 0 6.8 z" fill="#1e293b"/>'
    '</marker>'
    '</defs>'
    '<!-- Coordinate Axes -->'
    '<line x1="26" y1="210" x2="326" y2="210" stroke="#1e293b" stroke-width="1.2" marker-end="url(#csat27_14_arr)"/>'
    '<line x1="82" y1="242" x2="82" y2="16" stroke="#1e293b" stroke-width="1.2" marker-end="url(#csat27_14_arr)"/>'
    '<!-- Two Straight Lines through P(5, 1) -->'
    '<line x1="31.30" y1="182.80" x2="319.90" y2="212.40" stroke="#334155" stroke-width="1.25"/>'
    '<line x1="46.90" y1="34.80" x2="213.62" y2="240.00" stroke="#334155" stroke-width="1.25"/>'
    '<!-- Smooth Cubic Bezier Curve y = g(x) = log_a(x+2) + 2 -->'
    '<path d="M 50.60 240.12 C 51.64 232.26, 52.69 225.93, 53.73 220.36 '
    'C 55.03 213.39, 56.33 207.64, 57.62 202.53 '
    'C 59.25 196.15, 60.88 190.79, 62.50 186.00 '
    'C 66.40 174.51, 70.30 166.17, 74.20 158.99 '
    'C 79.40 149.41, 84.60 142.07, 89.80 135.68 '
    'C 96.95 126.90, 104.10 120.02, 111.25 114.00 '
    'C 124.25 103.05, 137.25 94.99, 150.25 88.02 '
    'C 169.75 77.57, 189.25 69.77, 208.75 63.00 '
    'C 244.50 50.61, 280.25 41.85, 316.00 34.33" '
    'fill="none" stroke="#0f172a" stroke-width="1.6" stroke-linecap="round"/>'
    '<!-- Smooth Cubic Bezier Curve y = f(x) = log_a(x-4) + 1 -->'
    '<path d="M 169.36 240.18 C 170.66 232.20, 171.96 225.80, 173.26 220.17 '
    'C 175.34 211.15, 177.42 204.13, 179.50 198.00 '
    'C 183.40 186.51, 187.30 178.17, 191.20 170.99 '
    'C 199.00 156.62, 206.80 147.04, 214.60 138.82 '
    'C 228.90 123.77, 243.20 113.93, 257.50 105.50 '
    'C 277.00 94.01, 296.50 85.67, 316.00 78.49" '
    'fill="none" stroke="#0f172a" stroke-width="1.6" stroke-linecap="round"/>'
    '<!-- Intersection Points P, Q, R -->'
    '<circle cx="179.50" cy="198.00" r="2.5" fill="#0f172a"/>'
    '<circle cx="62.50" cy="186.00" r="2.5" fill="#0f172a"/>'
    '<circle cx="111.25" cy="114.00" r="2.5" fill="#0f172a"/>'
    '<!-- Typography Labels -->'
    '<text x="86" y="223" font-family="Times New Roman, serif" font-size="12" fill="#0f172a">O</text>'
    '<text x="319" y="224" font-family="Times New Roman, serif" font-style="italic" font-size="12.5" fill="#0f172a">x</text>'
    '<text x="69" y="24" font-family="Times New Roman, serif" font-style="italic" font-size="12.5" fill="#0f172a">y</text>'
    '<text x="48" y="179" font-family="Times New Roman, serif" font-size="12.5" fill="#0f172a">Q</text>'
    '<text x="119" y="118" font-family="Times New Roman, serif" font-size="12.5" fill="#0f172a">R</text>'
    '<text x="186" y="193" font-family="Times New Roman, serif" font-size="12.5" fill="#0f172a">P</text>'
    '<text x="208" y="45" font-family="Times New Roman, serif" font-style="italic" font-size="12.5" fill="#0f172a">'
    'y<tspan font-style="normal"> = </tspan>g<tspan font-style="normal">(</tspan>x<tspan font-style="normal">)</tspan></text>'
    '<text x="256" y="112" font-family="Times New Roman, serif" font-style="italic" font-size="12.5" fill="#0f172a">'
    'y<tspan font-style="normal"> = </tspan>f<tspan font-style="normal">(</tspan>x<tspan font-style="normal">)</tspan></text>'
    '</svg>'
)


PART2_PROBLEMS = [
    # =========================================================================
    # 12번 (csat27_12)
    # =========================================================================
    {
        'slug': 'csat27_12',
        'qNum': '12',
        'points': 4,
        'is_short_answer': False,
        'official_ans_str': '',
        'subject': '공통(수학I·II)',
        'title': '[2027학년도 수능 고3 공통 12번] 등차수열의 부분합의 차와 절댓값 부호 판정',
        'title_en': '[2027 CSAT Math Common #12] Difference of Partial Sums and Sign Analysis in an Arithmetic Sequence',
        'summary_ko': '$S_8 - S_3 = 5a_6 = -15$에서 $a_6 = -3$을 구하고, $a_3 = |a_8| \\ge 0$으로부터 공차 $d = -6$과 $S_4 = 72$ 도출하기',
        'summary_en': 'Use $S_8 - S_3 = 5a_6 = -15$ to find $a_6 = -3$, deduce $d = -6$ from $a_3 = |a_8| \\ge 0$, and compute $S_4 = 72$.',
        'tags': ['2027학년도수능', '공통(수학I·II)', '수학I', '수열', '등차수열의합', '등차중항', '절댓값', '12번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': '$S_8 - S_3 = a_4 + a_5 + a_6 + a_7 + a_8 = 5a_6$',
                'desc': '연속한 5개 등차수열 항의 합은 한가운데 항 $a_6$의 5배',
                'desc_en': 'The sum of five consecutive arithmetic terms equals 5 times the middle term $a_6$.',
            },
            {
                'sym': '$a_3 = |a_8| \\ge 0$',
                'desc': '절댓값은 항상 0 이상이므로 $a_3 \\ge 0$이고 $a_6 = -3 < 0$에서 공차 $d < 0$',
                'desc_en': 'Since $|a_8| \\ge 0$, $a_3 \\ge 0 > a_6 = -3$, forcing the common difference $d < 0$.',
            },
            {
                'sym': '$a_3 + a_8 = 2a_6 - d = 0$',
                'desc': '$a_8 < 0$이므로 $a_3 = -a_8$, 즉 두 항의 합이 0임을 이용해 공차 결정',
                'desc_en': 'Since $a_8 < 0$, $a_3 + a_8 = 0$, determining $d = 2a_6 = -6$.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 규칙과 평균] 간격이 일정한 다섯 수의 합에서 한가운데 수 찾기',
                'title_en': '🔰 Step 1 · [Elementary Average Rule] Finding the middle number from the sum of 5 evenly spaced numbers',
                'knowledge': '초등학교 규칙 찾기에서 간격이 똑같은 다섯 수의 합은 언제나 **한가운데 수의 $5$배**입니다. 문제의 $S_3 = S_8 + 15$에서 $S_8 - S_3 = -15$이고, $S_8 - S_3 = a_4 + a_5 + a_6 + a_7 + a_8 = 5a_6$입니다.',
                'knowledge_en': 'For five evenly spaced numbers, their sum is always $5$ times the middle number. From $S_3 = S_8 + 15$, we get $S_8 - S_3 = a_4 + a_5 + a_6 + a_7 + a_8 = 5a_6 = -15$.',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '간격이 일정한 다섯 항의 합 $a_4 + a_5 + a_6 + a_7 + a_8 = 5a_6 = -15$일 때, 한가운데 항 $a_6$의 값은?',
                        'stem_en': 'When the sum of five arithmetic terms satisfies $5a_6 = -15$, what is the middle term $a_6$?',
                        'options': ['$-5$', '$-4$', '$-3$', '$3$', '$5$'],
                        'answer': 3,
                        'exp': '$5a_6 = -15$의 양변을 $5$로 나누면 $a_6 = -3$입니다.',
                        'exp_en': 'Dividing $5a_6 = -15$ by $5$ gives $a_6 = -3$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [부호 판정] $a_3 = |a_8|$과 $a_6 = -3$으로 공차 $d$와 $a_8$의 부호 알아내기',
                'title_en': '🌿 Step 2 · [Sign Determination] Finding the signs of $d$ and $a_8$ from $a_3 = |a_8|$ and $a_6 = -3$',
                'knowledge': '절댓값 $|a_8|$은 항상 $0$ 이상이므로 $a_3 = |a_8| \\ge 0$입니다. $3$번째 항은 $0$ 이상인데 $6$번째 항 $a_6 = -3$은 음수이므로 항이 갈수록 작아집니다($d < 0$). 따라서 $8$번째 항 $a_8$은 $a_6 = -3$보다 더 작은 음수입니다!',
                'knowledge_en': 'Since $a_3 = |a_8| \\ge 0$ while $a_6 = -3 < 0$, the sequence is decreasing ($d < 0$). Thus $a_8 = a_6 + 2d < -3 < 0$.',
                'questions': [
                    {
                        'level_label': '절댓값 부호 판정 디딤돌 2',
                        'level_label_en': 'Absolute Value Sign Step 2',
                        'stem': '$a_8 < 0$이므로 $|a_8| = -a_8$입니다. 이를 조건 $a_3 = |a_8|$에 대입했을 때 성립하는 관계식은?',
                        'stem_en': 'Since $a_8 < 0$, we have $|a_8| = -a_8$. Substituting this into $a_3 = |a_8|$ gives which relation?',
                        'options': ['$a_3 - a_8 = 0$', '$a_3 + a_8 = 0$', '$a_3 + a_8 = -3$', '$a_3 + a_8 = 3$', '$2a_3 + a_8 = 0$'],
                        'answer': 2,
                        'exp': '$a_3 = -a_8$에서 이항하면 $a_3 + a_8 = 0$입니다.',
                        'exp_en': '$a_3 = -a_8$ rearranges to $a_3 + a_8 = 0$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [공차 도출] $a_6 = -3$을 기준으로 $a_3 + a_8 = 0$을 풀어 공차 $d$ 구하기',
                'title_en': '🌱 Step 3 · [Common Difference] Solving $a_3 + a_8 = 0$ using $a_6 = -3$ to find $d$',
                'knowledge': '$a_6$을 기준으로 쓰면 $a_3 = a_6 - 3d$이고 $a_8 = a_6 + 2d$입니다. 두 식을 더하면 $a_3 + a_8 = 2a_6 - d = 0$이 됩니다.',
                'knowledge_en': 'Writing $a_3 = a_6 - 3d$ and $a_8 = a_6 + 2d$ gives $a_3 + a_8 = 2a_6 - d = 0$.',
                'questions': [
                    {
                        'level_label': '공차 계산 디딤돌 3',
                        'level_label_en': 'Common Difference Step 3',
                        'stem': '$a_6 = -3$일 때, $2a_6 - d = 0$을 만족시키는 등차수열의 공차 $d$의 값은?',
                        'stem_en': 'Given $a_6 = -3$ and $2a_6 - d = 0$, what is the common difference $d$?',
                        'options': ['$-8$', '$-6$', '$-4$', '$-3$', '$-2$'],
                        'answer': 2,
                        'exp': '$2(-3) - d = 0 \\implies -6 - d = 0 \\implies d = -6$입니다.',
                        'exp_en': '$d = 2a_6 = 2(-3) = -6$.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [일반항 역추적] 첫째항 $a_1$과 넷째항 $a_4$ 구하기',
                'title_en': '🌳 Step 4 · [Finding Terms] Computing $a_1$ and $a_4$',
                'knowledge': '$a_6 = -3$이고 공차 $d = -6$이므로 $a_1 = a_6 - 5d = -3 - 5(-6) = 27$이고, $a_4 = a_6 - 2d = -3 - 2(-6) = 9$입니다.',
                'knowledge_en': 'From $a_6 = -3$ and $d = -6$, we get $a_1 = a_6 - 5d = 27$ and $a_4 = a_6 - 2d = 9$.',
                'questions': [
                    {
                        'level_label': '항의 값 확인 디딤돌 4',
                        'level_label_en': 'Term Evaluation Step 4',
                        'stem': '$a_6 = -3$, $d = -6$인 등차수열에서 첫째항 $a_1$과 넷째항 $a_4$를 순서대로 바르게 구한 것은?',
                        'stem_en': 'For the arithmetic sequence with $a_6 = -3$ and $d = -6$, what is $(a_1, a_4)$?',
                        'options': ['$(21, 3)$', '$(24, 6)$', '$(27, 9)$', '$(30, 12)$', '$(33, 15)$'],
                        'answer': 3,
                        'exp': '$a_1 = -3 - (-30) = 27$, $a_4 = -3 - (-12) = 9$입니다.',
                        'exp_en': '$a_1 = 27$ and $a_4 = 9$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 종합] 첫째항부터 제$4$항까지의 합 $S_4$ 구하기',
                'title_en': '💎 Step 5 · [Final Synthesis] Evaluating the partial sum $S_4$',
                'knowledge': '등차수열의 합 공식 $S_4 = \\dfrac{4(a_1 + a_4)}{2} = 2(a_1 + a_4)$에 $a_1 = 27$, $a_4 = 9$를 대입하거나 $27 + 21 + 15 + 9$를 직접 더합니다.',
                'knowledge_en': 'Use $S_4 = \\dfrac{4(a_1 + a_4)}{2} = 2(27 + 9)$ or add $27 + 21 + 15 + 9$ directly.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': '$a_1 = 27$, $a_2 = 21$, $a_3 = 15$, $a_4 = 9$일 때, $S_4$의 값은?',
                        'stem_en': 'Given $a_1 = 27, a_2 = 21, a_3 = 15, a_4 = 9$, what is $S_4$?',
                        'options': ['$66$', '$69$', '$72$', '$75$', '$78$'],
                        'answer': 3,
                        'exp': '$S_4 = 2 \\times (27 + 9) = 2 \\times 36 = 72$이므로 정답은 ③입니다.',
                        'exp_en': '$S_4 = 2(27 + 9) = 72$ (choice ③).',
                    }
                ],
            },
        ],
        'final': {
            'stem': (
                '등차수열 $\\{a_n\\}$의 첫째항부터 제$n$항까지의 합을 $S_n$이라 하자.<br>'
                '$$a_3 = |a_8|, \\quad S_3 = S_8 + 15$$'
                '일 때, $S_4$의 값은? [4점]'
            ),
            'stem_en': (
                'Let $S_n$ be the sum of the first $n$ terms of an arithmetic sequence $\\{a_n\\}$. When<br>'
                '$$a_3 = |a_8|, \\quad S_3 = S_8 + 15,$$'
                'what is the value of $S_4$? [4 points]'
            ),
            'options': ['$66$', '$69$', '$72$', '$75$', '$78$'],
            'answer': 3,
            'exp': '$S_8 - S_3 = 5a_6 = -15$에서 $a_6 = -3$이고, $a_3 = |a_8| \\ge 0 > a_6$이므로 $d < 0$, $a_8 < 0$입니다. $a_3 + a_8 = 2a_6 - d = 0$에서 $d = -6$, $a_1 = 27$이므로 $S_4 = 72$입니다.',
            'exp_en': 'From $S_8 - S_3 = 5a_6 = -15$, we get $a_6 = -3$. Since $a_3 = |a_8| \\ge 0 > a_6$, $d < 0$ and $a_8 < 0$, giving $a_3 + a_8 = 2a_6 - d = 0 \\implies d = -6$, $a_1 = 27$, and $S_4 = 72$.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 <b>등차수열의 부분합의 차($S_8 - S_3$)와 등차중항 성질</b>을 이용해 특정 항($a_6$)을 즉시 구하고, 절댓값 조건 $a_3 = |a_8|$로부터 수열의 증감(공차의 부호)을 판별하는 문제입니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: 부분합의 차로 $a_6$ 구하기</b><br>\n'
                '  $S_3 = S_8 + 15$에서 $S_8 - S_3 = -15$이므로 등차중항의 성질에 의하여:<br>\n'
                '  $$S_8 - S_3 = a_4 + a_5 + a_6 + a_7 + a_8 = 5a_6 = -15 \\implies a_6 = -3$$<br>\n'
                '  <b>2단계: 공차 $d$의 부호 판정 및 값 도출</b><br>\n'
                '  $a_3 = |a_8| \\ge 0$이고 $a_6 = -3 < 0$이므로 $3d = a_6 - a_3 \\le -3 < 0$, 즉 공차 $d < 0$입니다.<br>\n'
                '  따라서 $a_8 = a_6 + 2d < -3 < 0$이므로 $|a_8| = -a_8$이고:<br>\n'
                '  $$a_3 + a_8 = (a_6 - 3d) + (a_6 + 2d) = 2a_6 - d = -6 - d = 0 \\implies d = -6$$<br>\n'
                '  <b>3단계: $S_4$의 값 계산</b><br>\n'
                '  $a_1 = a_6 - 5d = -3 - 5(-6) = 27$, $a_4 = a_6 - 2d = -3 - 2(-6) = 9$이므로:<br>\n'
                '  $$S_4 = \\frac{4(a_1 + a_4)}{2} = 2(27 + 9) = 72$$\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>검산: $a_3 = 15, a_8 = -15 \\implies a_3 = |a_8|$ 성립, $S_3 = 63, S_8 = 48 \\implies S_3 = S_8 + 15$ 성립. 정답은 <b>③번($72$)</b>입니다.</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                '<p>This problem uses the <b>arithmetic mean property on $S_8 - S_3$</b> and sign analysis of $a_3 = |a_8|$.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Find $a_6$</b><br>\n'
                '  $$S_8 - S_3 = a_4 + a_5 + a_6 + a_7 + a_8 = 5a_6 = -15 \\implies a_6 = -3$$<br>\n'
                '  <b>Step 2: Determine $d$</b><br>\n'
                '  Since $a_3 = |a_8| \\ge 0 > a_6 = -3$, the common difference satisfies $d < 0$, so $a_8 < 0$ and $a_3 + a_8 = 0$.<br>\n'
                '  $$2a_6 - d = -6 - d = 0 \\implies d = -6, \\quad a_1 = -3 - 5(-6) = 27, \\quad a_4 = 9$$<br>\n'
                '  <b>Step 3: Compute $S_4$</b><br>\n'
                '  $$S_4 = \\frac{4(27 + 9)}{2} = 72$$\n'
                '</p>\n\n'
                '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                '<p>Therefore, $S_4 = 72$, corresponding to <b>choice ③</b>.</p>'
            ),
        },
    },

    # =========================================================================
    # 13번 (csat27_13)
    # =========================================================================
    {
        'slug': 'csat27_13',
        'qNum': '13',
        'points': 4,
        'is_short_answer': False,
        'official_ans_str': '',
        'subject': '공통(수학I·II)',
        'title': '[2027학년도 수능 고3 공통 13번] 절댓값 정적분으로 정의된 함수의 성질과 진위 판정',
        'title_en': '[2027 CSAT Math Common #13] Properties of a Function Defined by an Absolute-Value Definite Integral',
        'summary_ko': '구간 $[0, 2]$에서 감소하는 함수 $f(x)$에 대해 $t = f(1)$일 때 상수 $t$의 적분이 상쇄됨을 이용해 ㄱ(참), ㄴ(참), ㄷ(거짓: $\\alpha = f(1)$) 판정하기',
        'summary_en': 'Use midpoint cancellation at $t = f(1)$ for decreasing $f(x)$ on $[0, 2]$ to verify ㄱ (True), ㄴ (True), and disprove ㄷ ($\\alpha = f(1) = -3$).',
        'tags': ['2027학년도수능', '공통(수학I·II)', '수학II', '적분', '절댓값정적분', '진위판정', '13번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': '$g(t) = \\int_0^2 |f(x) - t|\\,dx$',
                'desc': '구간 $[0, 2]$에서 곡선 $y=f(x)$와 가로선 $y=t$ 사이의 넓이',
                'desc_en': 'Area bounded between $y=f(x)$ and the horizontal line $y=t$ over $[0, 2]$.',
            },
            {
                'sym': '$\\int_0^1 (-t)\\,dx + \\int_1^2 t\\,dx = 0$',
                'desc': '구간 $[0,1]$과 $[1,2]$의 길이가 $1$로 같아 상수 $t$가 정확히 상쇄됨',
                'desc_en': 'Since $[0,1]$ and $[1,2]$ both have length $1$, the $-t$ and $+t$ terms cancel out.',
            },
            {
                'sym': '$t = f(1) = -3$',
                'desc': '$[0, 2]$에서 감소하는 함수에서 $g(t)$가 최소가 되고 상수항이 소거되는 기준값',
                'desc_en': 'At $t = f(1) = -3$, $f(x) - t$ changes sign at the midpoint $x = 1$.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 삼각형 넓이] ㄱ의 $g(0) = \\int_0^2 |-x+1|\\,dx$ 넓이로 구하기',
                'title_en': '🔰 Step 1 · [Elementary Triangle Area] Finding $g(0) = \\int_0^2 |-x+1|\\,dx$ via two right triangles',
                'knowledge': '초등학교 도형의 넓이에서 밑변이 $1$, 높이가 $1$인 직각삼각형의 넓이는 $\\dfrac{1 \\times 1}{2} = \\dfrac{1}{2}$입니다. $y = |-x+1|$의 그래프는 $x = 0$부터 $x = 2$까지 밑변 $1$, 높이 $1$인 직각삼각형 $2$개로 이루어져 있습니다.',
                'knowledge_en': 'By elementary geometry, a right triangle of base $1$ and height $1$ has area $\\frac{1}{2}$. Over $[0, 2]$, $y = |-x+1|$ forms two such right triangles meeting at $x = 1$.',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '밑변이 $1$, 높이가 $1$인 직각삼각형 두 개의 넓이의 합으로 구한 보기 ㄱ의 $g(0) = \\displaystyle\\int_0^2 |-x+1|\\,dx$의 값은?',
                        'stem_en': 'Adding the areas of the two right triangles of base $1$ and height $1$, what is $g(0) = \\int_0^2 |-x+1|\\,dx$ in statement ㄱ?',
                        'options': ['$\\dfrac{1}{2}$', '$1$', '$\\dfrac{3}{2}$', '$2$', '$4$'],
                        'answer': 2,
                        'exp': '$\\dfrac{1}{2} + \\dfrac{1}{2} = 1$이므로 보기 ㄱ은 **참**입니다.',
                        'exp_en': '$\\frac{1}{2} + \\frac{1}{2} = 1$, so statement ㄱ is **True**.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [중점 상쇄 원리] $x = 1$을 기준으로 절댓값이 나뉠 때 상수 $t$ 소거 확인하기',
                'title_en': '🌿 Step 2 · [Midpoint Cancellation] Canceling $t$ when sign flips at $x = 1$',
                'knowledge': '만약 구간 $[0, 1]$에서 $f(x) \\ge t$이고 구간 $[1, 2]$에서 $f(x) \\le t$이면, $g(t) = \\int_0^1 \\{f(x) - t\\}\\,dx + \\int_1^2 \\{t - f(x)\\}\\,dx$가 됩니다. 이때 구간 $[0, 1]$과 $[1, 2]$의 길이가 모두 $1$이므로 $-t \\times 1 + t \\times 1 = 0$이 되어 $t$가 깔끔하게 사라집니다!',
                'knowledge_en': 'If $f(x) \\ge t$ on $[0, 1]$ and $f(x) \\le t$ on $[1, 2]$, then $\\int_0^1 (f(x)-t)\\,dx + \\int_1^2 (t-f(x))\\,dx$ simplifies because $-t(1) + t(1) = 0$!',
                'questions': [
                    {
                        'level_label': '중점 적분 상쇄 디딤돌 2',
                        'level_label_en': 'Midpoint Cancellation Step 2',
                        'stem': '$[0, 1]$에서 $f(x) \\ge t$이고 $[1, 2]$에서 $f(x) \\le t$일 때, $\\displaystyle\\int_0^1 (f(x)-t)\\,dx + \\int_1^2 (t-f(x))\\,dx$를 정리한 식은?',
                        'stem_en': 'Simplify $\\int_0^1 (f(x)-t)\\,dx + \\int_1^2 (t-f(x))\\,dx$ using midpoint cancellation.',
                        'options': [
                            '$\\displaystyle\\int_0^2 f(x)\\,dx$',
                            '$\\displaystyle\\int_0^1 f(x)\\,dx - \\int_1^2 f(x)\\,dx$',
                            '$\\displaystyle\\int_1^2 f(x)\\,dx - \\int_0^1 f(x)\\,dx$',
                            '$\\displaystyle\\int_0^1 f(x)\\,dx - \\int_1^2 f(x)\\,dx - 2t$',
                            '$\\displaystyle\\int_0^1 f(x)\\,dx - \\int_1^2 f(x)\\,dx + 2t$',
                        ],
                        'answer': 2,
                        'exp': '$-\\int_0^1 t\\,dx + \\int_1^2 t\\,dx = -t + t = 0$이므로 $\\int_0^1 f(x)\\,dx - \\int_1^2 f(x)\\,dx$가 됩니다.',
                        'exp_en': 'Since $-t + t = 0$, the integral simplifies to $\\int_0^1 f(x)\\,dx - \\int_1^2 f(x)\\,dx$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [보기 ㄴ 검증] $f(x) = x^2 - 4x$에서 $f(1) = -3$ 확인하기',
                'title_en': '🌱 Step 3 · [Statement ㄴ Check] Verifying $f(1) = -3$ for $f(x) = x^2 - 4x$',
                'knowledge': '이차함수 $f(x) = x^2 - 4x = (x-2)^2 - 4$는 대칭축이 $x = 2$이므로 구간 $[0, 2]$에서 계속 감소합니다. 따라서 $t = f(1)$을 대입하면 정확히 2단계의 조건($[0,1]$에서 $f(x) \\ge t$, $[1,2]$에서 $f(x) \\le t$)을 만족합니다!',
                'knowledge_en': 'Since $f(x) = (x-2)^2 - 4$ decreases strictly on $[0, 2]$, choosing $t = f(1)$ satisfies $f(x) \\ge t$ on $[0, 1]$ and $f(x) \\le t$ on $[1, 2]$.',
                'questions': [
                    {
                        'level_label': '보기 ㄴ 판정 디딤돌 3',
                        'level_label_en': 'Statement ㄴ Step 3',
                        'stem': '$f(x) = x^2 - 4x$일 때 $f(1)$의 값과 보기 ㄴ의 참·거짓을 바르게 짝지은 것은?',
                        'stem_en': 'For $f(x) = x^2 - 4x$, what is $f(1)$ and is statement ㄴ True or False?',
                        'options': [
                            '$f(1) = -3$, 참',
                            '$f(1) = -3$, 거짓',
                            '$f(1) = -4$, 참',
                            '$f(1) = -4$, 거짓',
                            '$f(1) = 3$, 거짓',
                        ],
                        'answer': 1,
                        'exp': '$f(1) = 1 - 4 = -3$이므로 $t = -3$일 때 2단계 공식이 그대로 성립하여 보기 ㄴ은 **참**입니다.',
                        'exp_en': '$f(1) = -3$, so $g(-3) = \\int_0^1 f(x)\\,dx - \\int_1^2 f(x)\\,dx$ holds and statement ㄴ is **True**.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [보기 ㄷ 반례 포착] $f(x) = x^2(x-4)$도 $[0, 2]$에서 감소함을 이용해 $\\alpha = f(1)$ 대입하기',
                'title_en': '🌳 Step 4 · [Statement ㄷ Counterexample] Testing $\\alpha = f(1)$ for $f(x) = x^2(x-4)$',
                'knowledge': '$f(x) = x^2(x-4) = x^3 - 4x^2$을 미분하면 $f\'(x) = 3x^2 - 8x = x(3x - 8) \\le 0$ ($0 \\le x \\le 2$)이므로 **이 함수 역시 $[0, 2]$에서 계속 감소**합니다! 따라서 $\\alpha = f(1) = -3$일 때 $g(\\alpha) = \\int_0^1 f(x)\\,dx - \\int_1^2 f(x)\\,dx$가 성립합니다.',
                'knowledge_en': 'For $f(x) = x^3 - 4x^2$, $f\'(x) = x(3x-8) \\le 0$ on $[0, 2]$, so $f$ also decreases on $[0, 2]$! Thus $\\alpha = f(1) = -3$ directly satisfies the integral equation in ㄷ.',
                'questions': [
                    {
                        'level_label': '보기 ㄷ 판정 디딤돌 4',
                        'level_label_en': 'Statement ㄷ Step 4',
                        'stem': '$f(x) = x^2(x-4)$일 때 $\\alpha = f(1) = -3$이면 $g(\\alpha) = \\displaystyle\\int_0^1 f(x)\\,dx - \\int_1^2 f(x)\\,dx$가 성립합니다. 이때 $\\alpha < f(1)$이라는 보기 ㄷ의 주장은 참인가요, 거짓인가요?',
                        'stem_en': 'Since $\\alpha = f(1) = -3$ satisfies $g(\\alpha) = \\int_0^1 f(x)\\,dx - \\int_1^2 f(x)\\,dx$, is the claim $\\alpha < f(1)$ in statement ㄷ True or False?',
                        'options': [
                            '참 ($\\alpha < -3$이다)',
                            '거짓 ($\\alpha = f(1) = -3$일 때 등식이 성립하므로 $\\alpha < f(1)$이 아니다)',
                            '참 ($f(x)$가 증가함수이다)',
                            '참 ($g(-3) = 0$이다)',
                            '알 수 없다',
                        ],
                        'answer': 2,
                        'exp': '$\\alpha = f(1) = -3$이 등식을 만족시키므로 $\\alpha < f(1)$이라는 주장은 **거짓**입니다. (실제로 $g(t)$는 $t = f(1) = -3$에서 유일한 최솟값을 가지므로 $\\alpha = -3$뿐입니다.)',
                        'exp_en': 'Since $\\alpha = f(1) = -3$ satisfies the equation (and is in fact the unique minimizer of $g$), $\\alpha < f(1)$ is **False**.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 종합] 옳은 보기만 있는 대로 고르기',
                'title_en': '💎 Step 5 · [Final Synthesis] Selecting all true statements',
                'knowledge': '지금까지 검증한 결과 ㄱ(참), ㄴ(참), ㄷ(거짓)입니다.',
                'knowledge_en': 'Combining our results: ㄱ is True, ㄴ is True, and ㄷ is False.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': '<보기>의 ㄱ, ㄴ, ㄷ 중 옳은 것만을 있는 대로 고른 것은?',
                        'stem_en': 'Which option lists all true statements among ㄱ, ㄴ, and ㄷ?',
                        'options': ['ㄱ', 'ㄱ, ㄴ', 'ㄱ, ㄷ', 'ㄴ, ㄷ', 'ㄱ, ㄴ, ㄷ'],
                        'answer': 2,
                        'exp': '옳은 것은 ㄱ, ㄴ이므로 정답은 ②입니다.',
                        'exp_en': 'Only ㄱ and ㄴ are true (choice ②).',
                    }
                ],
            },
        ],
        'final': {
            'stem': (
                '실수 $t$와 다항함수 $f(x)$에 대하여 함수 $g(t)$를<br>'
                '$$g(t) = \\int_0^2 |f(x) - t|\\,dx$$'
                '라 하자. &lt;보기&gt;에서 옳은 것만을 있는 대로 고른 것은? [4점]'
                '<div style="margin:10px 0;padding:12px 14px;border:1.5px solid #475569;border-radius:8px;background:#f8fafc">'
                '<div style="color:#1e293b;line-height:1.8">'
                '<div style="text-align:center;font-weight:700;margin-bottom:4px">&lt;보 기&gt;</div>'
                'ㄱ. $f(x) = -x + 1$일 때, $g(0) = 1$이다.<br>'
                'ㄴ. $f(x) = x^2 - 4x$일 때,<br>'
                '&nbsp;&nbsp;&nbsp;&nbsp;$g(-3) = \\displaystyle\\int_0^1 f(x)\\,dx - \\int_1^2 f(x)\\,dx$ 이다.<br>'
                'ㄷ. $f(x) = x^2(x - 4)$일 때,<br>'
                '&nbsp;&nbsp;&nbsp;&nbsp;$g(\\alpha) = \\displaystyle\\int_0^1 f(x)\\,dx - \\int_1^2 f(x)\\,dx$ 이면 $\\alpha &lt; f(1)$이다.<br>'
                '&nbsp;&nbsp;&nbsp;&nbsp;(단, $\\alpha$는 실수이다.)'
                '</div></div>'
            ),
            'stem_en': (
                'For a real number $t$ and a polynomial function $f(x)$, define<br>'
                '$$g(t) = \\int_0^2 |f(x) - t|\\,dx.$$'
                'Which of the following statements in the box are true? [4 points]'
                '<div style="margin:10px 0;padding:12px 14px;border:1.5px solid #475569;border-radius:8px;background:#f8fafc">'
                '<div style="color:#1e293b;line-height:1.8">'
                '<div style="text-align:center;font-weight:700;margin-bottom:4px">&lt;Statements&gt;</div>'
                'ㄱ. When $f(x) = -x + 1$, $g(0) = 1$.<br>'
                'ㄴ. When $f(x) = x^2 - 4x$, $g(-3) = \\displaystyle\\int_0^1 f(x)\\,dx - \\int_1^2 f(x)\\,dx$.<br>'
                'ㄷ. When $f(x) = x^2(x - 4)$, if $g(\\alpha) = \\displaystyle\\int_0^1 f(x)\\,dx - \\int_1^2 f(x)\\,dx$, then $\\alpha &lt; f(1)$ (where $\\alpha \\in \\mathbb{R}$).'
                '</div></div>'
            ),
            'options': ['ㄱ', 'ㄱ, ㄴ', 'ㄱ, ㄷ', 'ㄴ, ㄷ', 'ㄱ, ㄴ, ㄷ'],
            'answer': 2,
            'exp': 'ㄱ: $g(0) = \\frac{1}{2} + \\frac{1}{2} = 1$ (참). ㄴ: $f(x) = x^2-4x$는 $[0,2]$에서 감소하고 $f(1)=-3$이므로 참. ㄷ: $f(x) = x^2(x-4)$도 $[0,2]$에서 감소하며 $\\alpha = f(1) = -3$일 때 등식이 성립하므로 거짓입니다.',
            'exp_en': 'ㄱ is True ($g(0)=1$). ㄴ is True because $f(x)=x^2-4x$ decreases on $[0,2]$ with $f(1)=-3$. ㄷ is False because $f(x)=x^2(x-4)$ also decreases on $[0,2]$ and satisfies the equation at $\\alpha = f(1) = -3$.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 <b>구간 $[0, 2]$에서 단조감소하는 함수 $f(x)$에 대하여 중점 $x = 1$에서의 함숫값 $t = f(1)$을 기준으로 절댓값 정적분을 분리할 때 상수 $t$가 상쇄되는 원리</b>를 묻는 정적분 진위 판정 문항입니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>ㄱ. (참)</b> $f(x) = -x + 1$일 때:<br>\n'
                '  $$g(0) = \\int_0^2 |-x + 1|\\,dx = \\int_0^1 (-x + 1)\\,dx + \\int_1^2 (x - 1)\\,dx = \\frac{1}{2} + \\frac{1}{2} = 1$$<br>\n'
                '  <b>ㄴ. (참)</b> $f(x) = x^2 - 4x$는 $[0, 2]$에서 $f\'(x) = 2x - 4 \\le 0$이므로 감소하며 $f(1) = -3$입니다.<br>\n'
                '  따라서 $[0, 1]$에서 $f(x) \\ge -3$, $[1, 2]$에서 $f(x) \\le -3$이므로:<br>\n'
                '  $$g(-3) = \\int_0^1 \\{f(x) + 3\\}\\,dx + \\int_1^2 \\{-3 - f(x)\\}\\,dx = \\int_0^1 f(x)\\,dx + 3 - 3 - \\int_1^2 f(x)\\,dx = \\int_0^1 f(x)\\,dx - \\int_1^2 f(x)\\,dx$$<br>\n'
                '  <b>ㄷ. (거짓)</b> $f(x) = x^2(x - 4) = x^3 - 4x^2$에 대하여 $f\'(x) = 3x^2 - 8x = x(3x - 8) \\le 0$ ($0 \\le x \\le 2$)이므로 $[0, 2]$에서 감소하며 $f(1) = -3$입니다.<br>\n'
                '  ㄴ과 완전히 동일한 원리로 $\\alpha = -3 = f(1)$일 때:<br>\n'
                '  $$g(-3) = \\int_0^1 f(x)\\,dx - \\int_1^2 f(x)\\,dx \\quad \\left(= \\frac{9}{2}\\right)$$\n'
                '  가 성립하므로 $\\alpha = f(1)$이 되어 $\\alpha < f(1)$은 성립하지 않습니다.\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>따라서 옳은 것은 ㄱ, ㄴ이므로 정답은 <b>②번</b>입니다.</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                '<p>When $f(x)$ is decreasing on $[0, 2]$, setting $t = f(1)$ splits $[0, 2]$ at its midpoint $x = 1$ into two intervals of equal length $1$, canceling the constant $t$ in $g(t)$.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>ㄱ (True):</b> $g(0) = \\int_0^1 (1-x)\\,dx + \\int_1^2 (x-1)\\,dx = \\frac{1}{2} + \\frac{1}{2} = 1$.<br><br>\n'
                '  <b>ㄴ (True):</b> $f(x) = x^2 - 4x$ decreases on $[0, 2]$ and $f(1) = -3$, so $g(-3) = \\int_0^1 (f(x)+3)\\,dx + \\int_1^2 (-3-f(x))\\,dx = \\int_0^1 f(x)\\,dx - \\int_1^2 f(x)\\,dx$.<br><br>\n'
                '  <b>ㄷ (False):</b> $f(x) = x^3 - 4x^2$ has $f\'(x) = x(3x-8) \\le 0$ on $[0, 2]$ and $f(1) = -3$. By the exact same calculation, $\\alpha = -3 = f(1)$ satisfies the equation (and is the unique minimizer of $g$), contradicting $\\alpha < f(1)$.\n'
                '</p>\n\n'
                '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                '<p>Thus only ㄱ and ㄴ are true, giving <b>choice ②</b>.</p>'
            ),
        },
    },

    # =========================================================================
    # 14번 (csat27_14)
    # =========================================================================
    {
        'slug': 'csat27_14',
        'qNum': '14',
        'points': 4,
        'is_short_answer': False,
        'official_ans_str': '',
        'subject': '공통(수학I·II)',
        'title': '[2027학년도 수능 고3 공통 14번] 로그함수의 평행이동 벡터와 삼각형의 무게중심',
        'title_en': '[2027 CSAT Math Common #14] Translation Vector of Logarithmic Curves and Centroid of a Triangle',
        'summary_ko': '평행이동 $(-6, 1)$과 기울기 $-\\dfrac{1}{6}$의 일치로 $\\mathrm{Q}(-1, 2)$를 찾고, 무게중심이 $y=2x$ 위에 있음으로 $\\mathrm{R}\\left(\\dfrac{3}{2}, 8\\right)$ 및 $a^6 = \\dfrac{7}{2}$ 도출하기',
        'summary_en': 'Match translation $(-6, 1)$ with slope $-\\frac{1}{6}$ to locate $\\mathrm{Q}(-1, 2)$, use the centroid on $y = 2x$ to find $\\mathrm{R}(\\frac{3}{2}, 8)$, and deduce $a^6 = \\frac{7}{2}$.',
        'tags': ['2027학년도수능', '공통(수학I·II)', '수학I', '로그함수', '평행이동', '삼각형의무게중심', '14번'],
        'orig_svg': Q14_ORIG_SVG,
        'symbols': [
            {
                'sym': '$g(x) = f(x + 6) + 1$',
                'desc': '곡선 $y=f(x)$를 $x$축으로 $-6$, $y$축으로 $+1$만큼 평행이동하면 $y=g(x)$와 겹침',
                'desc_en': 'Translating $y=f(x)$ by $(-6, +1)$ produces $y=g(x)$.',
            },
            {
                'sym': '$\\mathrm{Q}(5 - 6, 1 + 1) = (-1, 2)$',
                'desc': '평행이동 기울기가 $\\dfrac{1}{-6} = -\\dfrac{1}{6}$이므로 점 $\\mathrm{P}(5, 1)$의 대응점이 곧 교점 $\\mathrm{Q}$',
                'desc_en': 'Since the translation slope is $-\\frac{1}{6}$, translating $\\mathrm{P}(5,1)$ lands directly on $\\mathrm{Q}(-1,2)$.',
            },
            {
                'sym': '$\\mathrm{G}\\left(\\dfrac{x_P + x_Q + x_R}{3}, \\dfrac{y_P + y_Q + y_R}{3}\\right)$',
                'desc': '삼각형 $\\mathrm{PQR}$의 세 꼭짓점 좌표의 평균인 무게중심',
                'desc_en': 'Centroid coordinates given by the average of vertices $\\mathrm{P}, \\mathrm{Q}, \\mathrm{R}$.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 좌표 이동] 점 $(5, 1)$을 왼쪽으로 $6$칸, 위로 $1$칸 옮긴 점 찾기',
                'title_en': '🔰 Step 1 · [Elementary Grid Shift] Moving $(5, 1)$ left by $6$ units and up by $1$ unit',
                'knowledge': '초등학교 모눈종이 좌표 이동처럼 점 $(5, 1)$을 왼쪽($x$축 음의 방향)으로 $6$칸, 위쪽($y$축 양의 방향)으로 $1$칸 옮기면 $(5 - 6, 1 + 1)$이 됩니다.',
                'knowledge_en': 'Shifting $(5, 1)$ by $-6$ horizontally and $+1$ vertically gives $(5 - 6, 1 + 1)$.',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '점 $\\mathrm{P}(5, 1)$을 $x$축 방향으로 $-6$만큼, $y$축 방향으로 $+1$만큼 옮긴 점의 좌표는?',
                        'stem_en': 'What are the coordinates of $\\mathrm{P}(5, 1)$ after shifting by $(-6, +1)$?',
                        'options': ['$(-2, 2)$', '$(-1, 2)$', '$(-1, 3)$', '$(1, 2)$', '$(11, 2)$'],
                        'answer': 2,
                        'exp': '$(5 - 6, 1 + 1) = (-1, 2)$입니다.',
                        'exp_en': '$(5 - 6, 1 + 1) = (-1, 2)$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [평행이동과 기울기 일치] 교점 $\\mathrm{Q}$가 바로 $(-1, 2)$임을 확인하기',
                'title_en': '🌿 Step 2 · [Translation-Slope Match] Confirming $\\mathrm{Q} = (-1, 2)$',
                'knowledge': '$f(x) = \\log_a(x-4)+1$의 $x$ 자리에 $x+6$을 넣고 $1$을 더하면 $\\log_a(x+2)+2 = g(x)$입니다! 이때 이동 비율이 $\\dfrac{+1}{-6} = -\\dfrac{1}{6}$로 문제의 직선 기울기와 똑같고, 증가함수 $y=g(x)$와 감소직선의 교점은 유일하므로 $\\mathrm{Q}(-1, 2)$가 확정됩니다.',
                'knowledge_en': 'Since $g(x) = f(x+6)+1$ and the shift $(-6, 1)$ has slope $-\\frac{1}{6}$, $(-1, 2)$ lies on both $y=g(x)$ and the line of slope $-\\frac{1}{6}$ through $\\mathrm{P}(5,1)$.',
                'questions': [
                    {
                        'level_label': '교점 Q 확정 디딤돌 2',
                        'level_label_en': 'Point Q Verification Step 2',
                        'stem': '함수 $g(x) = \\log_a(x + 2) + 2$에 $x = -1$을 대입했을 때 밑 $a$의 값에 관계없이 항상 지나는 함숫값 $g(-1)$은?',
                        'stem_en': 'Regardless of $a > 1$, what is $g(-1)$ for $g(x) = \\log_a(x + 2) + 2$?',
                        'options': ['$0$', '$1$', '$2$', '$3$', '$4$'],
                        'answer': 3,
                        'exp': '$g(-1) = \\log_a(1) + 2 = 0 + 2 = 2$이므로 점 $\\mathrm{Q}(-1, 2)$를 항상 지납니다.',
                        'exp_en': '$g(-1) = \\log_a 1 + 2 = 2$, confirming $\\mathrm{Q}(-1, 2)$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [무게중심 표현] 점 $\\mathrm{R}(r, -2r+11)$로 삼각형 $\\mathrm{PQR}$의 무게중심 세우기',
                'title_en': '🌱 Step 3 · [Centroid Formula] Expressing the centroid of $\\triangle\\mathrm{PQR}$ using $\\mathrm{R}(r, -2r+11)$',
                'knowledge': '점 $\\mathrm{R}$은 직선 $y = -2x + 11$ 위의 점이므로 $\\mathrm{R}(r, -2r + 11)$로 놓을 수 있습니다. 세 꼭짓점 $\\mathrm{P}(5, 1)$, $\\mathrm{Q}(-1, 2)$, $\\mathrm{R}(r, -2r + 11)$의 좌표를 각각 더해 $3$으로 나누면 무게중심이 됩니다.',
                'knowledge_en': 'Let $\\mathrm{R}(r, -2r+11)$ on $y = -2x+11$. Average the coordinates of $\\mathrm{P}(5,1)$, $\\mathrm{Q}(-1,2)$, and $\\mathrm{R}(r, -2r+11)$.',
                'questions': [
                    {
                        'level_label': '무게중심 식 세우기 디딤돌 3',
                        'level_label_en': 'Centroid Coordinates Step 3',
                        'stem': '세 점 $\\mathrm{P}(5, 1)$, $\\mathrm{Q}(-1, 2)$, $\\mathrm{R}(r, -2r + 11)$을 꼭짓점으로 하는 삼각형 $\\mathrm{PQR}$의 무게중심의 좌표는?',
                        'stem_en': 'What is the centroid of $\\triangle\\mathrm{PQR}$ with $\\mathrm{P}(5,1)$, $\\mathrm{Q}(-1,2)$, and $\\mathrm{R}(r, -2r+11)$?',
                        'options': [
                            '$\\left(\\dfrac{r+4}{3}, \\dfrac{14-2r}{3}\\right)$',
                            '$\\left(\\dfrac{r+6}{3}, \\dfrac{14-2r}{3}\\right)$',
                            '$\\left(\\dfrac{r+4}{3}, \\dfrac{12-2r}{3}\\right)$',
                            '$\\left(\\dfrac{r+4}{2}, \\dfrac{14-2r}{2}\\right)$',
                            '$\\left(\\dfrac{r-4}{3}, \\dfrac{14+2r}{3}\\right)$',
                        ],
                        'answer': 1,
                        'exp': '$x$좌표의 합은 $5 + (-1) + r = r + 4$, $y$좌표의 합은 $1 + 2 + (-2r + 11) = 14 - 2r$이므로 $3$으로 나누면 $\\left(\\dfrac{r+4}{3}, \\dfrac{14-2r}{3}\\right)$입니다.',
                        'exp_en': 'Averaging gives $\\left(\\dfrac{r+4}{3}, \\dfrac{14-2r}{3}\\right)$.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [점 $\\mathrm{R}$ 확정] 무게중심이 직선 $y = 2x$ 위에 있음을 이용해 $\\mathrm{R}$ 구하기',
                'title_en': '🌳 Step 4 · [Finding Point R] Using the centroid on $y = 2x$ to determine $\\mathrm{R}$',
                'knowledge': '무게중심 $\\left(\\dfrac{r+4}{3}, \\dfrac{14-2r}{3}\\right)$을 직선 $y = 2x$에 대입하면 $\\dfrac{14 - 2r}{3} = 2 \\times \\dfrac{r + 4}{3} \\implies 14 - 2r = 2r + 8$입니다.',
                'knowledge_en': 'Substituting the centroid into $y = 2x$ yields $14 - 2r = 2(r + 4) = 2r + 8$.',
                'questions': [
                    {
                        'level_label': '점 R의 좌표 도출 디딤돌 4',
                        'level_label_en': 'Coordinates of R Step 4',
                        'stem': '$14 - 2r = 2r + 8$을 풀어 구한 점 $\\mathrm{R}(r, -2r + 11)$의 좌표는?',
                        'stem_en': 'Solving $14 - 2r = 2r + 8$, what are the coordinates of $\\mathrm{R}(r, -2r+11)$?',
                        'options': [
                            '$\\left(1, 9\\right)$',
                            '$\\left(\\dfrac{3}{2}, 8\\right)$',
                            '$\\left(2, 7\\right)$',
                            '$\\left(\\dfrac{5}{2}, 6\\right)$',
                            '$\\left(3, 5\\right)$',
                        ],
                        'answer': 2,
                        'exp': '$4r = 6 \\implies r = \\dfrac{3}{2}$이고, $y_R = -2 \\times \\dfrac{3}{2} + 11 = 8$이므로 $\\mathrm{R}\\left(\\dfrac{3}{2}, 8\\right)$입니다.',
                        'exp_en': '$4r = 6 \\implies r = \\frac{3}{2}$ and $y_R = -3 + 11 = 8$, so $\\mathrm{R}\\left(\\frac{3}{2}, 8\\right)$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 종합] 점 $\\mathrm{R}\\left(\\dfrac{3}{2}, 8\\right)$을 $y = g(x)$에 대입하여 $a^6$ 구하기',
                'title_en': '💎 Step 5 · [Final Synthesis] Substituting $\\mathrm{R}\\left(\\dfrac{3}{2}, 8\\right)$ into $y = g(x)$ to find $a^6$',
                'knowledge': '점 $\\mathrm{R}\\left(\\dfrac{3}{2}, 8\\right)$은 곡선 $y = g(x) = \\log_a(x + 2) + 2$ 위의 점이므로 $8 = \\log_a\\left(\\dfrac{3}{2} + 2\\right) + 2 \\implies \\log_a\\left(\\dfrac{7}{2}\\right) = 6$입니다.',
                'knowledge_en': 'Substituting $\\mathrm{R}\\left(\\frac{3}{2}, 8\\right)$ into $y = \\log_a(x+2)+2$ gives $\\log_a\\left(\\frac{7}{2}\\right) = 6$.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': '$\\log_a\\left(\\dfrac{7}{2}\\right) = 6$일 때, 로그의 정의에 따른 $a^6$의 값은?',
                        'stem_en': 'From $\\log_a\\left(\\dfrac{7}{2}\\right) = 6$, what is the value of $a^6$?',
                        'options': ['$\\dfrac{11}{4}$', '$3$', '$\\dfrac{13}{4}$', '$\\dfrac{7}{2}$', '$\\dfrac{15}{4}$'],
                        'answer': 4,
                        'exp': '$\\log_a\\left(\\dfrac{7}{2}\\right) = 6 \\iff a^6 = \\dfrac{7}{2}$이므로 정답은 ④입니다.',
                        'exp_en': 'By definition of logarithms, $a^6 = \\dfrac{7}{2}$ (choice ④).',
                    }
                ],
            },
        ],
        'final': {
            'stem': (
                '상수 $a\\,(a > 1)$에 대하여 두 함수<br>'
                '$$f(x) = \\log_a(x - 4) + 1, \\quad g(x) = \\log_a(x + 2) + 2$$'
                '가 있다. 곡선 $y = f(x)$ 위의 점 $\\mathrm{P}(5, 1)$을 지나고 기울기가 $-\\dfrac{1}{6}$인 직선이 곡선 $y = g(x)$와 만나는 점을 $\\mathrm{Q}$라 하고, '
                '점 $\\mathrm{P}$를 지나는 직선 $y = -2x + 11$이 곡선 $y = g(x)$와 만나는 점을 $\\mathrm{R}$이라 하자. '
                '삼각형 $\\mathrm{PQR}$의 무게중심이 직선 $y = 2x$ 위에 있을 때, $a^6$의 값은? [4점]'
            ),
            'stem_en': (
                'For a constant $a > 1$, let<br>'
                '$$f(x) = \\log_a(x - 4) + 1, \\quad g(x) = \\log_a(x + 2) + 2.$$'
                'Let $\\mathrm{Q}$ be the intersection of $y = g(x)$ with the line of slope $-\\dfrac{1}{6}$ passing through $\\mathrm{P}(5, 1)$ on $y = f(x)$, '
                'and let $\\mathrm{R}$ be the intersection of $y = g(x)$ with the line $y = -2x + 11$ passing through $\\mathrm{P}$. '
                'When the centroid of $\\triangle\\mathrm{PQR}$ lies on the line $y = 2x$, what is the value of $a^6$? [4 points]'
            ),
            'options': ['$\\dfrac{11}{4}$', '$3$', '$\\dfrac{13}{4}$', '$\\dfrac{7}{2}$', '$\\dfrac{15}{4}$'],
            'answer': 4,
            'exp': '$g(x) = f(x+6)+1$이므로 $\\mathrm{P}(5,1)$을 $(-6, 1)$만큼 평행이동한 점 $\\mathrm{Q}(-1, 2)$가 교점입니다. 무게중심 $\\left(\\frac{r+4}{3}, \\frac{14-2r}{3}\\right)$이 $y=2x$ 위에 있으므로 $r = \\frac{3}{2}$, $\\mathrm{R}\\left(\\frac{3}{2}, 8\\right)$이고 $g\\left(\\frac{3}{2}\\right) = 8$에서 $a^6 = \\dfrac{7}{2}$입니다.',
            'exp_en': 'Since $g(x) = f(x+6)+1$, $\\mathrm{Q} = (-1, 2)$. Setting the centroid $\\left(\\frac{r+4}{3}, \\frac{14-2r}{3}\\right)$ on $y = 2x$ gives $\\mathrm{R}\\left(\\frac{3}{2}, 8\\right)$, and $g\\left(\\frac{3}{2}\\right) = 8 \\implies a^6 = \\dfrac{7}{2}$.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 <b>로그함수의 평행이동 벡터 $(-6, 1)$과 직선의 기울기 $-\\dfrac{1}{6}$ 사이의 기하적 일치성</b>을 발견하여 교점 $\\mathrm{Q}$의 좌표를 구하고, 삼각형의 무게중심 조건으로 점 $\\mathrm{R}$을 결정하는 문제입니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: 평행이동 관계를 이용한 점 $\\mathrm{Q}$의 좌표 결정</b><br>\n'
                '  $g(x) = \\log_a(x + 2) + 2 = f(x + 6) + 1$이므로 곡선 $y = g(x)$는 곡선 $y = f(x)$를 $x$축 방향으로 $-6$, $y$축 방향으로 $+1$만큼 평행이동한 그래프입니다.<br>\n'
                '  점 $\\mathrm{P}(5, 1)$을 $(-6, 1)$만큼 평행이동한 점 $(-1, 2)$는 곡선 $y = g(x)$ 위에 있고, 두 점 $(5, 1)$과 $(-1, 2)$를 잇는 직선의 기울기가 $\\dfrac{2 - 1}{-1 - 5} = -\\dfrac{1}{6}$이므로 $\\mathrm{Q}(-1, 2)$입니다.<br><br>\n'
                '  <b>2단계: 무게중심 조건으로 점 $\\mathrm{R}$의 좌표 결정</b><br>\n'
                '  직선 $y = -2x + 11$ 위의 점 $\\mathrm{R}$을 $\\mathrm{R}(r, -2r + 11)$이라 하면 삼각형 $\\mathrm{PQR}$의 무게중심 $\\mathrm{G}$는:<br>\n'
                '  $$\\mathrm{G}\\left(\\frac{5 - 1 + r}{3},\\; \\frac{1 + 2 + 11 - 2r}{3}\\right) = \\left(\\frac{r + 4}{3},\\; \\frac{14 - 2r}{3}\\right)$$\n'
                '  점 $\\mathrm{G}$가 직선 $y = 2x$ 위에 있으므로:<br>\n'
                '  $$\\frac{14 - 2r}{3} = 2 \\cdot \\frac{r + 4}{3} \\implies 14 - 2r = 2r + 8 \\implies r = \\frac{3}{2}, \\quad \\mathrm{R}\\left(\\frac{3}{2}, 8\\right)$$<br>\n'
                '  <b>3단계: $a^6$의 값 계산</b><br>\n'
                '  점 $\\mathrm{R}\\left(\\dfrac{3}{2}, 8\\right)$이 곡선 $y = g(x)$ 위에 있으므로:<br>\n'
                '  $$8 = \\log_a\\left(\\frac{3}{2} + 2\\right) + 2 \\implies \\log_a\\left(\\frac{7}{2}\\right) = 6 \\implies a^6 = \\frac{7}{2}$$\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>따라서 $a^6 = \\dfrac{7}{2}$이므로 정답은 <b>④번</b>입니다.</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                '<p>This problem connects <b>horizontal/vertical translation $(-6, 1)$ of logarithmic functions</b> with the line of slope $-\\frac{1}{6}$ and triangle centroid properties.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Find $\\mathrm{Q}$ via translation</b><br>\n'
                '  Since $g(x) = f(x+6) + 1$, shifting $\\mathrm{P}(5, 1)$ by $(-6, 1)$ gives $(-1, 2)$, which lies on both $y = g(x)$ and the line of slope $-\\frac{1}{6}$ through $\\mathrm{P}$. Since $g$ is strictly increasing and the line is decreasing, $\\mathrm{Q} = (-1, 2)$ is unique.<br><br>\n'
                '  <b>Step 2: Find $\\mathrm{R}$ via the centroid on $y = 2x$</b><br>\n'
                '  Let $\\mathrm{R}(r, -2r + 11)$. The centroid $\\left(\\frac{r+4}{3}, \\frac{14-2r}{3}\\right)$ lies on $y = 2x$, so $14 - 2r = 2r + 8 \\implies r = \\frac{3}{2}$ and $\\mathrm{R} = \\left(\\frac{3}{2}, 8\\right)$.<br><br>\n'
                '  <b>Step 3: Compute $a^6$</b><br>\n'
                '  $$g\\left(\\frac{3}{2}\\right) = \\log_a\\left(\\frac{7}{2}\\right) + 2 = 8 \\implies a^6 = \\frac{7}{2}$$\n'
                '</p>\n\n'
                '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                '<p>Therefore, $a^6 = \\dfrac{7}{2}$, corresponding to <b>choice ④</b>.</p>'
            ),
        },
    },

    # =========================================================================
    # 15번 (csat27_15)
    # =========================================================================
    {
        'slug': 'csat27_15',
        'qNum': '15',
        'points': 4,
        'is_short_answer': False,
        'official_ans_str': '',
        'subject': '공통(수학I·II)',
        'title': '[2027학년도 수능 고3 공통 15번] 우극한 부호 함수로 정의된 합성함수 $g(x^2)$의 불연속점',
        'title_en': '[2027 CSAT Math Common #15] Discontinuities of $g(x^2)$ Defined via a Right-Hand Sign Limit',
        'summary_ko': '$x \\to 0$일 때 $x^2 \\to 0+$이고 $g$가 $0$에서 우연속이므로 $x=0$은 연속임을 간파하고, 불연속점 $\\pm 2, \\pm 1$ ($n=4$)과 $g(1) = 4$로부터 $8$ 도출하기',
        'summary_en': 'Observe that $x^2 \\to 0+$ as $x \\to 0$ makes $g(x^2)$ continuous at $x = 0$, leaving $4$ discontinuities $\\{-2, -1, 1, 2\\}$ and $n + g(1) = 4 + 4 = 8$.',
        'tags': ['2027학년도수능', '공통(수학I·II)', '수학II', '함수의연속', '합성함수의극한', '우연속', '15번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': '$\\lim_{t \\to x+} \\dfrac{f(t)}{|f(t)|}$',
                'desc': '$x$보다 아주 조금 오른쪽($x+$)에서 $f(t)$가 양수이면 $+1$, 음수이면 $-1$',
                'desc_en': 'Right-hand sign of $f(t)$: equals $+1$ if $f(t) > 0$ on $(x, x+\\delta)$, and $-1$ if $f(t) < 0$.',
            },
            {
                'sym': '$x \\to 0 \\implies x^2 \\to 0+$',
                'desc': '$x$가 $0$의 왼쪽에서 오든 오른쪽에서 오든 제곱한 $x^2$은 항상 양수 쪽($0+$)에서 $0$에 다가감',
                'desc_en': 'As $x \\to 0$ from either side, $x^2 \\ge 0$ approaches $0$ strictly from the right ($0+$).',
            },
            {
                'sym': '$a_1 = -2,\\; a_2 = -1,\\; a_3 = 1,\\; a_4 = 2$',
                'desc': '$x^2 = 1$ 또는 $x^2 = 4$가 되어 $g(x^2)$이 불연속이 되는 $4$개의 실수',
                'desc_en': 'The $n = 4$ real points where $x^2 \\in \\{1, 4\\}$ causes $g(x^2)$ to jump.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 부호 규칙] 어떤 수를 자기 자신의 절댓값으로 나눈 값 $\\dfrac{k}{|k|}$ 구하기',
                'title_en': '🔰 Step 1 · [Elementary Sign Rule] Dividing a nonzero number $k$ by its magnitude $|k|$',
                'knowledge': '초등학교 나눗셈에서 $0$이 아닌 양수(예: $5$)를 크기 $5$로 나누면 $+1$이고, 음수(예: $-5$)를 크기 $5$로 나누면 $-1$입니다. 즉 $\\dfrac{f(t)}{|f(t)|}$는 함숫값의 **부호($+1$ 또는 $-1$)**만 뽑아내는 장치입니다!',
                'knowledge_en': 'Dividing any positive number by its magnitude gives $+1$, while dividing any negative number by its magnitude gives $-1$.',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '두 식 $\\dfrac{7}{|7|}$과 $\\dfrac{-7}{|-7|}$의 값을 순서대로 바르게 구한 것은?',
                        'stem_en': 'What are the values of $\\dfrac{7}{|7|}$ and $\\dfrac{-7}{|-7|}$, respectively?',
                        'options': ['$1, 1$', '$1, -1$', '$-1, 1$', '$-1, -1$', '$7, -7$'],
                        'answer': 2,
                        'exp': '$\\dfrac{7}{7} = 1$이고 $\\dfrac{-7}{7} = -1$입니다.',
                        'exp_en': '$\\frac{7}{7} = 1$ and $\\frac{-7}{7} = -1$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [인수분해와 우극한 부호] $f(x) = x(x-1)(x-4)$의 구간별 부호와 $g(u)$ ($u \\ge 0$) 구하기',
                'title_en': '🌿 Step 2 · [Factoring & Right-Sign] Finding $g(u)$ for $u \\ge 0$ using $f(t) = t(t-1)(t-4)$',
                'knowledge': '$f(t) = t^3 - 5t^2 + 4t = t(t - 1)(t - 4)$이므로 $0 < t < 1$에서 $f(t) > 0$, $1 < t < 4$에서 $f(t) < 0$, $t > 4$에서 $f(t) > 0$입니다. 특히 $t \\to u+$ (오른쪽에서 접근)이므로 $u = 0, 1, 4$에서의 함숫값은 **바로 오른쪽 구간의 부호**를 따릅니다!',
                'knowledge_en': 'Since $f(t) = t(t-1)(t-4)$ has sign $+$ on $(0,1)$, $-$ on $(1,4)$, and $+$ on $(4,\\infty)$, the right-hand limit $\\lim_{t\\to u+} \\frac{f(t)}{|f(t)|}$ equals $+1$ on $[0,1)$, $-1$ on $[1,4)$, and $+1$ on $[4,\\infty)$.',
                'questions': [
                    {
                        'level_label': '우극한 부호 계산 디딤돌 2',
                        'level_label_en': 'Right-Limit Sign Step 2',
                        'stem': '$1 < t < 4$에서 $f(t) < 0$이므로 $\\lim_{t \\to 1+} \\dfrac{f(t)}{|f(t)|} = -1$입니다. 이때 $g(1) = (2 \\cdot 1 - 6) \\times \\lim_{t \\to 1+} \\dfrac{f(t)}{|f(t)|}$의 값은?',
                        'stem_en': 'Since $\\lim_{t \\to 1+} \\frac{f(t)}{|f(t)|} = -1$, what is $g(1) = (2(1) - 6) \\times (-1)$?',
                        'options': ['$-6$', '$-4$', '$0$', '$4$', '$6$'],
                        'answer': 4,
                        'exp': '$g(1) = (-4) \\times (-1) = 4$입니다.',
                        'exp_en': '$g(1) = (-4)(-1) = 4$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [최고난도 함정 돌파] $x = 0$에서 $g(x^2)$이 연속인지 확인하기',
                'title_en': '🌱 Step 3 · [Crucial Trap Check] Checking continuity of $g(x^2)$ at $x = 0$',
                'knowledge': '$u = x^2$은 $x \\neq 0$일 때 항상 양수($0 < x^2 < 1$)입니다! 따라서 $x \\to 0-$이든 $x \\to 0+$이든 $x^2$은 $0$보다 큰 쪽에서 다가오므로 $0 \\le x^2 < 1$ 구간 식 $g(x^2) = 2x^2 - 6$을 그대로 따릅니다.',
                'knowledge_en': 'For every $x \\in (-1, 1)$, we have $0 \\le x^2 < 1$, where $g(u) = 2u - 6$! Thus $g(x^2) = 2x^2 - 6$ across the entire open interval $(-1, 1)$, including $x = 0$!',
                'questions': [
                    {
                        'level_label': 'x=0 연속성 판정 디딤돌 3',
                        'level_label_en': 'Continuity at x=0 Step 3',
                        'stem': '구간 $(-1, 1)$의 모든 실수 $x$에 대하여 $0 \\le x^2 < 1$이므로 $g(x^2) = 2x^2 - 6$입니다. 이때 $x = 0$에서 함수 $g(x^2)$은 연속인가요?',
                        'stem_en': 'Since $g(x^2) = 2x^2 - 6$ for all $x \\in (-1, 1)$, is $g(x^2)$ continuous at $x = 0$?',
                        'options': [
                            '불연속이다 (좌극한이 $6$이고 우극한이 $-6$이다)',
                            '연속이다 ($\\lim_{x \\to 0} g(x^2) = g(0) = -6$으로 일치한다)',
                            '불연속이다 ($g(0)$이 정의되지 않는다)',
                            '연속이다 ($g(0) = 0$이다)',
                            '불연속이다 (우극한이 존재하지 않는다)',
                        ],
                        'answer': 2,
                        'exp': '$g(u)$ 자체는 $u=0$에서 불연속이지만 **우연속**($\\lim_{u\\to 0+}g(u)=g(0)=-6$)이고 $x^2 \\ge 0$이므로, $g(x^2)$은 $x=0$에서 극한값과 함숫값이 모두 $-6$으로 **연속**입니다!',
                        'exp_en': 'Because $x^2 \\ge 0$ and $g$ is right-continuous at $0$, $\\lim_{x\\to 0} g(x^2) = g(0) = -6$, so $g(x^2)$ is **continuous** at $x = 0$!',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [불연속점 나열] $x^2 = 1$과 $x^2 = 4$에서 불연속점 $a_1, a_2, a_3, a_4$ 구하기',
                'title_en': '🌳 Step 4 · [Listing Discontinuities] Finding $a_1, a_2, a_3, a_4$ where $x^2 \\in \\{1, 4\\}$',
                'knowledge': '$u \\ge 0$에서 $g(u)$는 $u = 1$ (값 $-4 \\leftrightarrow +4$)과 $u = 4$ (값 $-2 \\leftrightarrow +2$, $2(4)-6 = 2 \\neq 0$!)에서만 불연속입니다. 따라서 $x^2 = 1$ 또는 $x^2 = 4$인 $x = -2, -1, 1, 2$에서 $g(x^2)$이 불연속입니다.',
                'knowledge_en': 'For $u > 0$, $g(u)$ jumps at $u = 1$ ($-4$ vs $+4$) and $u = 4$ ($-2$ vs $+2$). Thus $g(x^2)$ is discontinuous precisely where $x^2 = 1$ or $x^2 = 4$.',
                'questions': [
                    {
                        'level_label': '불연속점 정렬 디딤돌 4',
                        'level_label_en': 'Sorting Discontinuities Step 4',
                        'stem': '$g(x^2)$이 불연속인 모든 실수를 작은 수부터 크기순으로 나열한 $a_1, a_2, \\cdots, a_n$에 대하여 $(n, a_3)$를 바르게 구한 것은?',
                        'stem_en': 'Listing all discontinuities of $g(x^2)$ in increasing order as $a_1 < \\dots < a_n$, what is $(n, a_3)$?',
                        'options': ['$(3, 1)$', '$(4, 1)$', '$(4, 2)$', '$(5, 0)$', '$(5, 1)$'],
                        'answer': 2,
                        'exp': '불연속점은 $-2, -1, 1, 2$의 총 $4$개($n = 4$)이며, 세 번째 수 $a_3 = 1$입니다.',
                        'exp_en': 'The discontinuities are $-2, -1, 1, 2$, so $n = 4$ and $a_3 = 1$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 종합] $n + g(a_3)$의 값 완성하기',
                'title_en': '💎 Step 5 · [Final Synthesis] Computing $n + g(a_3)$',
                'knowledge': '4단계에서 $n = 4$, $a_3 = 1$을 구했고, 2단계에서 $g(1) = 4$를 구했습니다.',
                'knowledge_en': 'Combine $n = 4$, $a_3 = 1$, and $g(1) = 4$.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': '$n = 4$, $a_3 = 1$, $g(1) = 4$일 때, $n + g(a_3)$의 값은?',
                        'stem_en': 'Given $n = 4$, $a_3 = 1$, and $g(1) = 4$, what is $n + g(a_3)$?',
                        'options': ['$4$', '$6$', '$8$', '$10$', '$12$'],
                        'answer': 3,
                        'exp': '$n + g(a_3) = 4 + g(1) = 4 + 4 = 8$이므로 정답은 ③입니다.',
                        'exp_en': '$n + g(1) = 4 + 4 = 8$ (choice ③).',
                    }
                ],
            },
        ],
        'final': {
            'stem': (
                '함수 $f(x) = x^3 - 5x^2 + 4x$에 대하여 함수 $g(x)$를<br>'
                '$$g(x) = (2x - 6) \\times \\lim_{t \\to x+} \\frac{f(t)}{|f(t)|}$$'
                '라 하자. 실수 전체의 집합에서 정의된 함수 $g(x^2)$이 $x = a$에서 불연속인 모든 $a$의 값을 작은 수부터 크기순으로 나열한 것을 '
                '$a_1, a_2, \\cdots, a_n\\,(n\\text{은 자연수})$라 할 때, $n + g(a_3)$의 값은? [4점]'
            ),
            'stem_en': (
                'For $f(x) = x^3 - 5x^2 + 4x$, define the function $g(x)$ by<br>'
                '$$g(x) = (2x - 6) \\times \\lim_{t \\to x+} \\frac{f(t)}{|f(t)|}.$$'
                'Let $a_1, a_2, \\dots, a_n$ ($n \\in \\mathbb{N}$) be all real values of $a$, listed in increasing order, '
                'at which $g(x^2)$ is discontinuous. What is the value of $n + g(a_3)$? [4 points]'
            ),
            'options': ['$4$', '$6$', '$8$', '$10$', '$12$'],
            'answer': 3,
            'exp': '$f(x) = x(x-1)(x-4)$이고 $u \\ge 0$에서 $g(u)$는 $u=0$에서 우연속이므로 $g(x^2)$은 $x=0$에서 연속입니다. 불연속점은 $x^2 = 1, 4$인 $-2, -1, 1, 2$로 $n=4$, $a_3=1$이고 $g(1) = (-4)(-1) = 4$이므로 $n + g(a_3) = 8$입니다.',
            'exp_en': 'Since $f(x) = x(x-1)(x-4)$ makes $g(u)$ right-continuous at $u = 0$ and $x^2 \\ge 0$, $g(x^2)$ is continuous at $x = 0$. Its discontinuities are $x \\in \\{-2, -1, 1, 2\\}$ ($n = 4, a_3 = 1$), and $g(1) = 4$, giving $n + g(a_3) = 8$.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 객관식 최고난도(15번) 문항으로, <b>우극한으로 정의된 조각함수 $g(u)$의 우연속성</b>과 <b>짝수차 합성 $u = x^2 \\ge 0$이 $x = 0$ 근방에서 우극한($0+$)만 참조한다는 성질</b>을 정확히 결합할 수 있는지 평가합니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: $u \\ge 0$에서 함수 $g(u)$의 식 구하기</b><br>\n'
                '  $f(t) = t^3 - 5t^2 + 4t = t(t - 1)(t - 4)$이므로 우극한 부호 $\\lim_{t \\to u+} \\dfrac{f(t)}{|f(t)|}$는:<br>\n'
                '  $$g(u) = \\begin{cases} 2u - 6 & (0 \\le u < 1) \\\\ -2u + 6 & (1 \\le u < 4) \\\\ 2u - 6 & (u \\ge 4) \\end{cases}$$<br>\n'
                '  <b>2단계: 합성함수 $g(x^2)$의 불연속점 판별</b><br>\n'
                '  • <b>$x = 0$ 근방</b>: $-1 < x < 1$인 모든 실수 $x$에 대하여 $0 \\le x^2 < 1$이므로 $g(x^2) = 2x^2 - 6$입니다. 따라서 $x = 0$에서 <b>연속</b>입니다!<br>\n'
                '  • <b>$x^2 = 1$ ($x = \\pm 1$)</b>: $|x| \\to 1-$일 때 $g(x^2) \\to -4$이고, $|x| \\to 1+$일 때 및 $|x|=1$에서 $g(x^2) \\to +4$이므로 $x = -1, 1$에서 불연속입니다.<br>\n'
                '  • <b>$x^2 = 4$ ($x = \\pm 2$)</b>: $|x| \\to 2-$일 때 $g(x^2) \\to -2$이고, $|x| \\to 2+$일 때 및 $|x|=2$에서 $g(x^2) \\to +2$이므로 $x = -2, 2$에서 불연속입니다.<br>\n'
                '  따라서 불연속점을 작은 수부터 나열하면 $a_1 = -2,\\; a_2 = -1,\\; a_3 = 1,\\; a_4 = 2$이므로 $n = 4$, $a_3 = 1$입니다.<br><br>\n'
                '  <b>3단계: $n + g(a_3)$ 계산</b><br>\n'
                '  $g(a_3) = g(1) = -2(1) + 6 = 4$이므로 $n + g(a_3) = 4 + 4 = 8$입니다.\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>$x = 0$을 불연속점으로 착각하는 함정과 $2x - 6 = 0$ ($x = 3$)의 위치를 정확히 구분하면 깔끔하게 해결됩니다. 정답은 <b>③번($8$)</b>입니다.</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                '<p>Because $g(u)$ uses the right-hand limit $t \\to u+$, $g(u)$ is right-continuous everywhere, and since $x^2 \\ge 0$ approaches $0$ from the right as $x \\to 0$, $g(x^2)$ is continuous at $x = 0$.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Piecewise formula of $g(u)$ on $u \\ge 0$</b><br>\n'
                '  Factoring $f(t) = t(t-1)(t-4)$ yields $g(u) = 2u - 6$ on $[0, 1) \\cup [4, \\infty)$ and $g(u) = -2u + 6$ on $[1, 4)$.<br><br>\n'
                '  <b>Step 2: Discontinuities of $g(x^2)$</b><br>\n'
                '  On $(-1, 1)$, $0 \\le x^2 < 1$, so $g(x^2) = 2x^2 - 6$ is continuous at $x = 0$. Jumps occur only where $x^2 = 1$ ($-4 \\neq 4$) and $x^2 = 4$ ($-2 \\neq 2$), giving $a_1 = -2, a_2 = -1, a_3 = 1, a_4 = 2$ ($n = 4$).<br><br>\n'
                '  <b>Step 3: Evaluate $n + g(a_3)$</b><br>\n'
                '  Since $g(1) = -2(1) + 6 = 4$, we obtain $n + g(a_3) = 4 + 4 = 8$.\n'
                '</p>\n\n'
                '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                '<p>Therefore, $n + g(a_3) = 8$, which corresponds to <b>choice ③</b>.</p>'
            ),
        },
    },

    # =========================================================================
    # 16번 (csat27_16) - 단답형 3점
    # =========================================================================
    {
        'slug': 'csat27_16',
        'qNum': '16',
        'points': 3,
        'is_short_answer': True,
        'official_ans_str': '2',
        'subject': '공통(수학I·II)',
        'title': '[2027학년도 수능 고3 공통 16번] 밑을 통일하여 푸는 지수방정식',
        'title_en': '[2027 CSAT Math Common #16] Solving an Exponential Equation by Unifying the Base',
        'summary_ko': '$\\dfrac{1}{25} = 5^{-2}$임을 이용해 우변을 $5^{-2x+6}$으로 바꾸고 지수를 비교하여 $x = 2$ 구하기',
        'summary_en': 'Rewrite $\\frac{1}{25} = 5^{-2}$ to express the RHS as $5^{-2x+6}$, then equate exponents to find $x = 2$.',
        'tags': ['2027학년도수능', '공통(수학I·II)', '수학I', '지수함수', '지수방정식', '단답형', '16번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': '$\\dfrac{1}{25} = \\dfrac{1}{5^2} = 5^{-2}$',
                'desc': '25는 5의 제곱이고 역수는 음수 지수로 나타냄',
                'desc_en': 'Since $25 = 5^2$, its reciprocal is $5^{-2}$.',
            },
            {
                'sym': '$(5^{-2})^{x-3} = 5^{-2(x-3)}$',
                'desc': '거듭제곱의 거듭제곱은 두 지수를 서로 곱함',
                'desc_en': 'Power of a power rule multiplies the exponents.',
            },
            {
                'sym': '$5^A = 5^B \\iff A = B$',
                'desc': '밑이 $5$로 같으면 지수끼리 서로 같음',
                'desc_en': 'Injectivity of $5^x$ allows equating exponents.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 곱셈] $25$는 $5$를 몇 번 곱한 수인가요?',
                'title_en': '🔰 Step 1 · [Elementary Multiplication] Expressing $25$ as repeated multiplication of $5$',
                'knowledge': '초등학교 구구단 $5$단에서 $5 \\times 5 = 25$이므로 $25 = 5^2$입니다.',
                'knowledge_en': 'From multiplication tables, $5 \\times 5 = 25 = 5^2$.',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '$25 = 5^2$일 때, 역수 $\\dfrac{1}{25}$을 밑이 $5$인 거듭제곱으로 바르게 나타낸 것은?',
                        'stem_en': 'Since $25 = 5^2$, how is $\\dfrac{1}{25}$ written as a power of $5$?',
                        'options': ['$5^{-3}$', '$5^{-2}$', '$5^{-1}$', '$5^2$', '$5^5$'],
                        'answer': 2,
                        'exp': '$\\dfrac{1}{25} = \\dfrac{1}{5^2} = 5^{-2}$입니다.',
                        'exp_en': '$\\frac{1}{25} = 5^{-2}$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [지수법칙] $(5^{-2})^{x-3}$의 지수 전개하기',
                'title_en': '🌿 Step 2 · [Exponent Rule] Expanding the exponent in $(5^{-2})^{x-3}$',
                'knowledge': '지수법칙 $(a^m)^n = a^{mn}$에 따라 지수 $-2$와 $(x - 3)$을 곱하면 $-2(x - 3) = -2x + 6$입니다.',
                'knowledge_en': 'By $(a^m)^n = a^{mn}$, multiply $-2$ by $(x - 3)$ to get $-2x + 6$.',
                'questions': [
                    {
                        'level_label': '지수 분배법칙 디딤돌 2',
                        'level_label_en': 'Distributive Exponent Step 2',
                        'stem': '$-2(x - 3)$의 괄호를 분배법칙으로 바르게 전개한 식은?',
                        'stem_en': 'Expand $-2(x - 3)$ using the distributive law.',
                        'options': ['$-2x - 6$', '$-2x - 3$', '$-2x + 3$', '$-2x + 6$', '$2x - 6$'],
                        'answer': 4,
                        'exp': '$-2 \\times x + (-2) \\times (-3) = -2x + 6$입니다.',
                        'exp_en': '$-2(x - 3) = -2x + 6$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [지수 비교] 밑이 $5$로 같아진 양변의 지수끼리 등식 세우기',
                'title_en': '🌱 Step 3 · [Equating Exponents] Setting the exponents equal in $5^x = 5^{-2x+6}$',
                'knowledge': '$5^x = 5^{-2x + 6}$에서 밑이 $5$ ($5 \\neq 1, 5 > 0$)로 같으므로 지수끼리 같아야 합니다: $x = -2x + 6$.',
                'knowledge_en': 'From $5^x = 5^{-2x+6}$, equate the exponents: $x = -2x + 6$.',
                'questions': [
                    {
                        'level_label': '일차방정식 정리 디딤돌 3',
                        'level_label_en': 'Linear Equation Step 3',
                        'stem': '$x = -2x + 6$에서 $-2x$를 좌변으로 이항하여 정리한 식은?',
                        'stem_en': 'Rearranging $x = -2x + 6$ by moving $-2x$ to the left side gives:',
                        'options': ['$-x = 6$', '$x = 6$', '$2x = 6$', '$3x = 6$', '$3x = -6$'],
                        'answer': 4,
                        'exp': '$x + 2x = 6$이므로 $3x = 6$입니다.',
                        'exp_en': '$x + 2x = 3x = 6$.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [해 구하기 및 검산] $3x = 6$을 풀고 양변에 대입해 확인하기',
                'title_en': '🌳 Step 4 · [Solving & Checking] Solving $3x = 6$ and checking both sides',
                'knowledge': '$3x = 6$에서 $x = 2$입니다. 준식에 $x = 2$를 넣어 검산하면 좌변은 $5^2 = 25$, 우변은 $\\left(\\dfrac{1}{25}\\right)^{-1} = 25$로 일치합니다.',
                'knowledge_en': 'From $3x = 6$, $x = 2$. Checking: $5^2 = 25$ and $(1/25)^{2-3} = (1/25)^{-1} = 25$.',
                'questions': [
                    {
                        'level_label': '검산 확인 디딤돌 4',
                        'level_label_en': 'Verification Step 4',
                        'stem': '$x = 2$일 때 방정식 $5^x = \\left(\\dfrac{1}{25}\\right)^{x-3}$의 좌변과 우변이 같아지는 공통 값은?',
                        'stem_en': 'When $x = 2$, what common value do both sides of $5^x = (1/25)^{x-3}$ equal?',
                        'options': ['$1$', '$5$', '$10$', '$25$', '$125$'],
                        'answer': 4,
                        'exp': '$5^2 = 25$이고 $\\left(\\dfrac{1}{25}\\right)^{-1} = 25$로 일치합니다.',
                        'exp_en': 'Both sides equal $25$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 종합] 실수 $x$의 값 답하기',
                'title_en': '💎 Step 5 · [Final Synthesis] Final value of $x$',
                'knowledge': '따라서 구하는 실수 $x$의 값은 $2$입니다.',
                'knowledge_en': 'The required real number $x$ is $2$.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': '방정식 $5^x = \\left(\\dfrac{1}{25}\\right)^{x-3}$을 만족시키는 실수 $x$의 값은?',
                        'stem_en': 'What real number $x$ satisfies $5^x = \\left(\\dfrac{1}{25}\\right)^{x-3}$?',
                        'options': ['$1$', '$2$', '$3$', '$4$', '$6$'],
                        'answer': 2,
                        'exp': '$x = 2$입니다.',
                        'exp_en': '$x = 2$.',
                    }
                ],
            },
        ],
        'final': {
            'stem': '방정식 $5^x = \\left(\\dfrac{1}{25}\\right)^{x-3}$ 을 만족시키는 실수 $x$의 값을 구하시오. [3점]',
            'stem_en': 'Find the real number $x$ satisfying the equation $5^x = \\left(\\dfrac{1}{25}\\right)^{x-3}$. [3 points]',
            'options': ['$1$', '$2$', '$3$', '$4$', '$6$'],
            'answer': 2,
            'exp': '$\\left(\\dfrac{1}{25}\\right)^{x-3} = (5^{-2})^{x-3} = 5^{-2x+6}$이므로 $x = -2x + 6 \\implies 3x = 6 \\implies x = 2$입니다.',
            'exp_en': 'Since $\\left(\\dfrac{1}{25}\\right)^{x-3} = 5^{-2x+6}$, equating exponents gives $x = -2x + 6 \\implies x = 2$.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 단답형 첫 문항(16번)으로, <b>음수 지수와 지수법칙을 이용해 밑을 $5$로 통일한 뒤 지수방정식을 해결</b>하는 기본 문항입니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  $$\\frac{1}{25} = 5^{-2} \\implies \\left(\\frac{1}{25}\\right)^{x-3} = (5^{-2})^{x-3} = 5^{-2x + 6}$$\n'
                '  따라서 $5^x = 5^{-2x + 6}$에서 지수끼리 비교하면:<br>\n'
                '  $$x = -2x + 6 \\implies 3x = 6 \\implies x = 2$$\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>따라서 구하는 실수 $x$의 값은 <b>$2$</b>입니다.</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                '<p>This short-answer problem tests <b>exponent laws and solving exponential equations by unifying bases</b>.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  $$5^x = (5^{-2})^{x-3} = 5^{-2x + 6} \\implies x = -2x + 6 \\implies 3x = 6 \\implies x = 2$$\n'
                '</p>\n\n'
                '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                '<p>The exact short-answer value is <b>$2$</b>.</p>'
            ),
        },
    },

    # =========================================================================
    # 17번 (csat27_17) - 단답형 3점
    # =========================================================================
    {
        'slug': 'csat27_17',
        'qNum': '17',
        'points': 3,
        'is_short_answer': True,
        'official_ans_str': '20',
        'subject': '공통(수학I·II)',
        'title': '[2027학년도 수능 고3 공통 17번] 도함수로부터 부정적분과 적분상수 결정',
        'title_en': '[2027 CSAT Math Common #17] Finding a Polynomial via Indefinite Integration and Initial Value',
        'summary_ko': '$f\'(x) = 6x^2 + 1$을 적분하여 $f(x) = 2x^3 + x + C$를 구하고 $f(1) = 5$에서 $C = 2$, $f(2) = 20$ 도출하기',
        'summary_en': 'Integrate $f\'(x) = 6x^2 + 1$ to get $f(x) = 2x^3 + x + C$, find $C = 2$ from $f(1) = 5$, and compute $f(2) = 20$.',
        'tags': ['2027학년도수능', '공통(수학I·II)', '수학II', '적분', '부정적분', '적분상수', '단답형', '17번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': '$\\int x^n\\,dx = \\dfrac{1}{n+1}x^{n+1} + C$',
                'desc': '차수를 $1$ 올리고 그 차수로 나누는 다항함수의 부정적분 공식',
                'desc_en': 'Power rule for antiderivatives: increase exponent by $1$ and divide by the new exponent.',
            },
            {
                'sym': '$f(x) = 2x^3 + x + C$',
                'desc': '미분했을 때 $6x^2 + 1$이 되는 삼차함수',
                'desc_en': 'General cubic antiderivative of $6x^2 + 1$.',
            },
            {
                'sym': '$f(1) = 5 \\implies C = 2$',
                'desc': '초기조건 $x = 1$을 대입하여 적분상수 $C$ 확정',
                'desc_en': 'Initial condition $f(1) = 5$ determines the constant of integration $C = 2$.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 세제곱 계산] $2$를 세 번 곱한 값 $2^3$ 계산하기',
                'title_en': '🔰 Step 1 · [Elementary Multiplication] Computing $2^3 = 2 \\times 2 \\times 2$',
                'knowledge': '초등학교 곱셈에서 $2 \\times 2 \\times 2 = 8$이며, 여기에 $2$를 한 번 더 곱한 $2 \\times 2^3$은 $16$입니다.',
                'knowledge_en': 'By elementary multiplication, $2^3 = 8$ and $2 \\times 2^3 = 16$.',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '초등학교 곱셈으로 $2 \\times (2 \\times 2 \\times 2) = 2 \\times 2^3$을 계산한 값은?',
                        'stem_en': 'Using elementary multiplication, what is $2 \\times (2 \\times 2 \\times 2)$?',
                        'options': ['$8$', '$12$', '$16$', '$18$', '$24$'],
                        'answer': 3,
                        'exp': '$2 \\times 8 = 16$입니다.',
                        'exp_en': '$2 \\times 8 = 16$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [부정적분 구하기] 미분해서 $6x^2 + 1$이 되는 함수 $f(x)$ 세우기',
                'title_en': '🌿 Step 2 · [Indefinite Integral] Integrating $f\'(x) = 6x^2 + 1$',
                'knowledge': '$6x^2$을 적분하면 $\\dfrac{6}{3}x^3 = 2x^3$이고, 상수 $1$을 적분하면 $x$이므로 적분상수 $C$를 붙여 $f(x) = 2x^3 + x + C$입니다.',
                'knowledge_en': 'Integrating $6x^2 + 1$ term by term gives $f(x) = 2x^3 + x + C$.',
                'questions': [
                    {
                        'level_label': '부정적분 공식 디딤돌 2',
                        'level_label_en': 'Antiderivative Step 2',
                        'stem': '$f\'(x) = 6x^2 + 1$을 부정적분한 $f(x)$의 식($C$는 적분상수)으로 옳은 것은?',
                        'stem_en': 'Which is the correct antiderivative $f(x)$ of $f\'(x) = 6x^2 + 1$?',
                        'options': [
                            '$f(x) = 6x^3 + x + C$',
                            '$f(x) = 3x^3 + x + C$',
                            '$f(x) = 2x^3 + x + C$',
                            '$f(x) = 2x^3 + C$',
                            '$f(x) = 12x + C$',
                        ],
                        'answer': 3,
                        'exp': '$\\int (6x^2 + 1)\\,dx = 2x^3 + x + C$입니다.',
                        'exp_en': '$\\int (6x^2 + 1)\\,dx = 2x^3 + x + C$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [적분상수 결정] $f(1) = 5$를 대입하여 $C$ 구하기',
                'title_en': '🌱 Step 3 · [Constant of Integration] Finding $C$ from $f(1) = 5$',
                'knowledge': '$f(x) = 2x^3 + x + C$에 $x = 1$을 대입하면 $f(1) = 2(1)^3 + 1 + C = 3 + C = 5$입니다.',
                'knowledge_en': 'Substituting $x = 1$ gives $f(1) = 2 + 1 + C = 3 + C = 5$.',
                'questions': [
                    {
                        'level_label': '적분상수 도출 디딤돌 3',
                        'level_label_en': 'Finding C Step 3',
                        'stem': '$3 + C = 5$를 만족시키는 적분상수 $C$의 값은?',
                        'stem_en': 'What value of $C$ satisfies $3 + C = 5$?',
                        'options': ['$0$', '$1$', '$2$', '$3$', '$4$'],
                        'answer': 3,
                        'exp': '$C = 5 - 3 = 2$이므로 $f(x) = 2x^3 + x + 2$입니다.',
                        'exp_en': '$C = 2$, completing $f(x) = 2x^3 + x + 2$.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [$x = 2$ 대입] 완성된 $f(x) = 2x^3 + x + 2$의 각 항 계산하기',
                'title_en': '🌳 Step 4 · [Substitution] Evaluating each term of $f(2)$',
                'knowledge': '$x = 2$를 대입하면 첫째 항은 1단계에서 구한 $2 \\times 2^3 = 16$이고, 나머지 $x + 2 = 2 + 2 = 4$입니다.',
                'knowledge_en': 'At $x = 2$, $2(2)^3 = 16$ and $x + 2 = 4$.',
                'questions': [
                    {
                        'level_label': '항별 합산 준비 디딤돌 4',
                        'level_label_en': 'Term Evaluation Step 4',
                        'stem': '$f(x) = 2x^3 + x + 2$에 $x = 2$를 대입했을 때 일차항과 상수항의 합 $(x + 2)$의 값은?',
                        'stem_en': 'When $x = 2$, what is the sum of the linear and constant terms $(x + 2)$?',
                        'options': ['$2$', '$3$', '$4$', '$5$', '$6$'],
                        'answer': 3,
                        'exp': '$2 + 2 = 4$입니다.',
                        'exp_en': '$2 + 2 = 4$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 종합] $f(2)$의 최종 값 완성하기',
                'title_en': '💎 Step 5 · [Final Synthesis] Computing $f(2)$',
                'knowledge': '$16 + 4 = 20$을 더하여 최종 정답을 얻습니다. (정적분 $f(2) = f(1) + \\int_1^2 (6x^2 + 1)\\,dx = 5 + 15 = 20$으로도 일치합니다!)',
                'knowledge_en': 'Adding $16 + 4 = 20$ completes the answer.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': '$f(x) = 2x^3 + x + 2$일 때, $f(2)$의 값은?',
                        'stem_en': 'For $f(x) = 2x^3 + x + 2$, what is $f(2)$?',
                        'options': ['$16$', '$18$', '$20$', '$22$', '$24$'],
                        'answer': 3,
                        'exp': '$f(2) = 2(8) + 2 + 2 = 20$입니다.',
                        'exp_en': '$f(2) = 16 + 2 + 2 = 20$.',
                    }
                ],
            },
        ],
        'final': {
            'stem': (
                '다항함수 $f(x)$에 대하여<br>'
                '$$f\'(x) = 6x^2 + 1, \\quad f(1) = 5$$'
                '가 성립할 때, $f(2)$의 값을 구하시오. [3점]'
            ),
            'stem_en': (
                'For a polynomial function $f(x)$ satisfying<br>'
                '$$f\'(x) = 6x^2 + 1, \\quad f(1) = 5,$$'
                'find the value of $f(2)$. [3 points]'
            ),
            'options': ['$16$', '$18$', '$20$', '$22$', '$24$'],
            'answer': 3,
            'exp': '$f(x) = 2x^3 + x + C$에서 $f(1) = 3 + C = 5 \\implies C = 2$이므로 $f(2) = 16 + 2 + 2 = 20$입니다.',
            'exp_en': 'Integrating gives $f(x) = 2x^3 + x + C$. Using $f(1) = 5$ gives $C = 2$, so $f(2) = 16 + 2 + 2 = 20$.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 <b>다항함수의 부정적분과 초기조건을 이용한 함숫값 계산</b>을 평가하는 기본 문항입니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  $f\'(x) = 6x^2 + 1$을 부정적분하면 적분상수 $C$에 대하여:<br>\n'
                '  $$f(x) = \\int (6x^2 + 1)\\,dx = 2x^3 + x + C$$\n'
                '  $f(1) = 5$이므로 $2(1)^3 + 1 + C = 5 \\implies C = 2$입니다.<br>\n'
                '  따라서 $f(x) = 2x^3 + x + 2$이므로 $f(2) = 2(2)^3 + 2 + 2 = 20$입니다.\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>정적분 $f(2) = f(1) + \\int_1^2 (6x^2+1)\\,dx = 5 + [2x^3+x]_1^2 = 5 + (18 - 3) = 20$으로도 검산됩니다. 정답은 <b>$20$</b>입니다.</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                '<p>This problem applies the <b>Fundamental Theorem of Calculus / power rule for antiderivatives</b>.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  $$f(x) = \\int (6x^2 + 1)\\,dx = 2x^3 + x + C$$\n'
                '  From $f(1) = 3 + C = 5$, we get $C = 2$, hence $f(2) = 2(8) + 2 + 2 = 20$.\n'
                '</p>\n\n'
                '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                '<p>The exact short-answer value is <b>$20$</b>.</p>'
            ),
        },
    },

    # =========================================================================
    # 18번 (csat27_18) - 단답형 3점
    # =========================================================================
    {
        'slug': 'csat27_18',
        'qNum': '18',
        'points': 3,
        'is_short_answer': True,
        'official_ans_str': '5',
        'subject': '공통(수학I·II)',
        'title': '[2027학년도 수능 고3 공통 18번] 합의 기호 시그마(Σ)의 성질과 거듭제곱의 합',
        'title_en': '[2027 CSAT Math Common #18] Linearity of Sigma Notation and Sum of Squares',
        'summary_ko': '좌변 $30 + 5a$와 우변 $1^2+2^2+3^2+4^2+5^2 = 55$를 비교하여 상수 $a = 5$ 도출하기',
        'summary_en': 'Equate the LHS $30 + 5a$ with the RHS $\\sum_{k=1}^5 k^2 = 55$ to find $a = 5$.',
        'tags': ['2027학년도수능', '공통(수학I·II)', '수학I', '수열', '시그마의성질', '자연수거듭제곱의합', '단답형', '18번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': '$\\sum_{k=1}^{5} k = 1 + 2 + 3 + 4 + 5 = 15$',
                'desc': '1부터 5까지 자연수의 합',
                'desc_en': 'Sum of the first 5 positive integers.',
            },
            {
                'sym': '$\\sum_{k=1}^{5} a = 5a$',
                'desc': '상수 $a$를 $5$번 더하면 $5a$가 됨 ($a$가 아님에 주의!)',
                'desc_en': 'Adding constant $a$ five times equals $5a$.',
            },
            {
                'sym': '$\\sum_{k=1}^{5} k^2 = \\dfrac{5 \\cdot 6 \\cdot 11}{6} = 55$',
                'desc': '1부터 5까지 제곱수의 합 ($1 + 4 + 9 + 16 + 25 = 55$)',
                'desc_en': 'Sum of squares from $1^2$ to $5^2$ equals $55$.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 덧셈] $1 + 2 + 3 + 4 + 5$ 계산하기',
                'title_en': '🔰 Step 1 · [Elementary Addition] Adding $1 + 2 + 3 + 4 + 5$',
                'knowledge': '초등학교 덧셈에서 양 끝끼리 짝지어 $(1 + 5) + (2 + 4) + 3 = 6 + 6 + 3 = 15$를 쉽게 구할 수 있습니다.',
                'knowledge_en': 'Pairing numbers gives $(1 + 5) + (2 + 4) + 3 = 15$.',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '$1 + 2 + 3 + 4 + 5 = 15$에 $2$를 곱한 값 $2 \\displaystyle\\sum_{k=1}^{5} k$는 얼마인가요?',
                        'stem_en': 'Given $1 + 2 + 3 + 4 + 5 = 15$, what is $2\\sum_{k=1}^5 k$?',
                        'options': ['$15$', '$20$', '$25$', '$30$', '$35$'],
                        'answer': 4,
                        'exp': '$2 \\times 15 = 30$입니다.',
                        'exp_en': '$2 \\times 15 = 30$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [제곱수의 합] 우변 $1^2 + 2^2 + 3^2 + 4^2 + 5^2$ 계산하기',
                'title_en': '🌿 Step 2 · [Sum of Squares] Computing $1^2 + 2^2 + 3^2 + 4^2 + 5^2$',
                'knowledge': '$\\sum_{k=1}^{5} k^2 = 1 + 4 + 9 + 16 + 25$를 직접 더하거나 공식 $\\dfrac{5 \\times 6 \\times 11}{6}$을 사용합니다.',
                'knowledge_en': 'Add $1 + 4 + 9 + 16 + 25$ directly or use $\\frac{5 \\cdot 6 \\cdot 11}{6}$.',
                'questions': [
                    {
                        'level_label': '제곱수 합산 디딤돌 2',
                        'level_label_en': 'Sum of Squares Step 2',
                        'stem': '$\\displaystyle\\sum_{k=1}^{5} k^2 = 1 + 4 + 9 + 16 + 25$의 값은?',
                        'stem_en': 'What is the value of $\\sum_{k=1}^5 k^2 = 1 + 4 + 9 + 16 + 25$?',
                        'options': ['$45$', '$50$', '$55$', '$60$', '$65$'],
                        'answer': 3,
                        'exp': '$(1 + 9) + (4 + 16) + 25 = 10 + 20 + 25 = 55$입니다.',
                        'exp_en': '$10 + 20 + 25 = 55$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [상수의 시그마] $\\sum_{k=1}^{5} a$를 바르게 나타내기',
                'title_en': '🌱 Step 3 · [Sum of a Constant] Expressing $\\sum_{k=1}^5 a$',
                'knowledge': '$\\sum_{k=1}^{5} a = a + a + a + a + a = 5a$입니다. 좌변 전체는 $2\\sum_{k=1}^{5} k + \\sum_{k=1}^{5} a = 30 + 5a$가 됩니다.',
                'knowledge_en': '$\\sum_{k=1}^5 a = 5a$, so the LHS equals $30 + 5a$.',
                'questions': [
                    {
                        'level_label': '좌변 정리 디딤돌 3',
                        'level_label_en': 'LHS Simplification Step 3',
                        'stem': '좌변 $\\displaystyle\\sum_{k=1}^{5}(2k + a)$를 정리한 식으로 옳은 것은?',
                        'stem_en': 'Which expression simplifies $\\sum_{k=1}^5 (2k + a)$?',
                        'options': ['$15 + a$', '$30 + a$', '$15 + 5a$', '$30 + 5a$', '$30 + 10a$'],
                        'answer': 4,
                        'exp': '$2(15) + 5a = 30 + 5a$입니다.',
                        'exp_en': '$2(15) + 5a = 30 + 5a$.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [일차방정식 정리] $30 + 5a = 55$에서 $5a$ 구하기',
                'title_en': '🌳 Step 4 · [Linear Equation] Finding $5a$ from $30 + 5a = 55$',
                'knowledge': '좌변 $30 + 5a$와 우변 $55$가 같으므로 양변에서 $30$을 빼면 $5a = 25$입니다.',
                'knowledge_en': 'Subtracting $30$ from both sides of $30 + 5a = 55$ gives $5a = 25$.',
                'questions': [
                    {
                        'level_label': '이항 뺄셈 디딤돌 4',
                        'level_label_en': 'Subtraction Step 4',
                        'stem': '$30 + 5a = 55$일 때, $5a$의 값은?',
                        'stem_en': 'Given $30 + 5a = 55$, what is $5a$?',
                        'options': ['$15$', '$20$', '$25$', '$30$', '$35$'],
                        'answer': 3,
                        'exp': '$55 - 30 = 25$입니다.',
                        'exp_en': '$5a = 55 - 30 = 25$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 종합] 상수 $a$의 값 완성하기',
                'title_en': '💎 Step 5 · [Final Synthesis] Finding constant $a$',
                'knowledge': '$5a = 25$의 양변을 $5$로 나누면 $a = 5$입니다.',
                'knowledge_en': 'Dividing $5a = 25$ by $5$ yields $a = 5$.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': '$\\displaystyle\\sum_{k=1}^{5}(2k + a) = \\sum_{k=1}^{5} k^2$일 때, 상수 $a$의 값은?',
                        'stem_en': 'When $\\sum_{k=1}^5 (2k + a) = \\sum_{k=1}^5 k^2$, what is the constant $a$?',
                        'options': ['$3$', '$4$', '$5$', '$6$', '$7$'],
                        'answer': 3,
                        'exp': '$5a = 25$이므로 $a = 5$입니다.',
                        'exp_en': '$a = 5$.',
                    }
                ],
            },
        ],
        'final': {
            'stem': '$\\displaystyle\\sum_{k=1}^{5}(2k + a) = \\sum_{k=1}^{5} k^2$ 일 때, 상수 $a$의 값을 구하시오. [3점]',
            'stem_en': 'When $\\displaystyle\\sum_{k=1}^{5}(2k + a) = \\sum_{k=1}^{5} k^2$, find the value of the constant $a$. [3 points]',
            'options': ['$3$', '$4$', '$5$', '$6$', '$7$'],
            'answer': 3,
            'exp': '$2 \\cdot \\dfrac{5 \\cdot 6}{2} + 5a = \\dfrac{5 \\cdot 6 \\cdot 11}{6}$에서 $30 + 5a = 55 \\implies 5a = 25 \\implies a = 5$입니다.',
            'exp_en': 'From $2(15) + 5a = 55$, we get $5a = 25 \\implies a = 5$.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 <b>합의 기호 $\\sum$의 선형성과 자연수의 거듭제곱의 합 공식</b>을 정확히 적용하는지 평가하는 문항입니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  $$\\sum_{k=1}^{5}(2k + a) = 2\\sum_{k=1}^{5} k + \\sum_{k=1}^{5} a = 2 \\times \\frac{5 \\times 6}{2} + 5a = 30 + 5a$$\n'
                '  $$\\sum_{k=1}^{5} k^2 = \\frac{5 \\times 6 \\times 11}{6} = 55$$\n'
                '  따라서 $30 + 5a = 55 \\implies 5a = 25 \\implies a = 5$입니다.\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>$\\sum_{k=1}^5 a = 5a$를 $a$로 쓰지 않도록 주의합니다. 정답은 <b>$5$</b>입니다.</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                '<p>This problem tests <b>linearity of summation and standard power-sum formulas</b>.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  $$2\\sum_{k=1}^5 k + 5a = 30 + 5a = \\sum_{k=1}^5 k^2 = 55 \\implies 5a = 25 \\implies a = 5$$\n'
                '</p>\n\n'
                '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                '<p>The exact short-answer value is <b>$5$</b>.</p>'
            ),
        },
    },

    # =========================================================================
    # 19번 (csat27_19) - 단답형 3점
    # =========================================================================
    {
        'slug': 'csat27_19',
        'qNum': '19',
        'points': 3,
        'is_short_answer': True,
        'official_ans_str': '31',
        'subject': '공통(수학I·II)',
        'title': '[2027학년도 수능 고3 공통 19번] 삼차함수 그래프와 직선 $y = k$의 교점 개수(극값)',
        'title_en': '[2027 CSAT Math Common #19] Number of Intersections Between a Cubic Curve and $y = k$',
        'summary_ko': '$f\'(x) = 3(x+2)(x-4) = 0$에서 극댓값 $f(-2) = 31$과 극솟값 $f(4) = -77$을 구해 양수 $k = 31$ 도출하기',
        'summary_en': 'Solve $f\'(x) = 3(x+2)(x-4) = 0$ to find extrema $f(-2) = 31$ and $f(4) = -77$, selecting the positive value $k = 31$.',
        'tags': ['2027학년도수능', '공통(수학I·II)', '수학II', '미분', '방정식의활용', '삼차함수의극값', '단답형', '19번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': '$f\'(x) = 3x^2 - 6x - 24 = 3(x+2)(x-4)$',
                'desc': '삼차함수의 극대점($x=-2$)과 극소점($x=4$)을 찾는 도함수 인수분해',
                'desc_en': 'Factored derivative locating the local maximum ($x=-2$) and local minimum ($x=4$).',
            },
            {
                'sym': '교점 개수 $= 2 \\iff k = \\text{극댓값 또는 극솟값}$',
                'desc': '가로선 $y=k$가 삼차함수 그래프와 정확히 두 점에서 만나려면 극점에 접해야 함',
                'desc_en': 'A horizontal line $y=k$ meets a cubic with two extrema at exactly 2 points iff $k$ is a local extremum.',
            },
            {
                'sym': '$k = f(-2) = 31 > 0$',
                'desc': '두 극값 $31$과 $-77$ 중 문제에서 요구하는 양수 $k$',
                'desc_en': 'Positive extremum among $f(-2) = 31$ and $f(4) = -77$.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 그래프 관찰] 오르락내리락하는 곡선과 가로선이 딱 $2$번 만나는 위치 찾기',
                'title_en': '🔰 Step 1 · [Elementary Graph Intuition] Where a horizontal line meets an N-shaped curve twice',
                'knowledge': '올라갔다가 내려가고 다시 올라가는 N자 모양의 곡선에 가로선 $y = k$를 그었을 때, 만나는 점이 정확히 $2$개가 되는 순간은 가로선이 **가장 높은 봉우리(극대점)나 가장 낮은 골짜기(극소점)를 스치듯 지날 때**뿐입니다!',
                'knowledge_en': 'A horizontal line meets an N-shaped curve at exactly $2$ points precisely when it touches the peak (local maximum) or valley (local minimum).',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '봉우리의 높이가 $31$이고 골짜기의 높이가 $-77$인 N자 모양 곡선과 가로선 $y = k$가 정확히 $2$개의 점에서 만나도록 하는 **양수** $k$는?',
                        'stem_en': 'If an N-shaped curve has peak height $31$ and valley height $-77$, what **positive** value of $k$ makes $y = k$ meet the curve at exactly $2$ points?',
                        'options': ['$3$', '$24$', '$31$', '$48$', '$77$'],
                        'answer': 3,
                        'exp': '$k = 31$ 또는 $k = -77$일 때 두 점에서 만나며, 양수인 값은 $31$입니다.',
                        'exp_en': 'The horizontal line touches an extremum at $k = 31$ or $k = -77$; the positive value is $31$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [도함수 구하기] $f(x) = x^3 - 3x^2 - 24x + 3$을 미분하고 $3$으로 묶기',
                'title_en': '🌿 Step 2 · [Derivative] Differentiating $f(x)$ and factoring out $3$',
                'knowledge': '$f(x) = x^3 - 3x^2 - 24x + 3$을 미분하면 $f\'(x) = 3x^2 - 6x - 24 = 3(x^2 - 2x - 8)$입니다.',
                'knowledge_en': 'Differentiating gives $f\'(x) = 3x^2 - 6x - 24 = 3(x^2 - 2x - 8)$.',
                'questions': [
                    {
                        'level_label': '도함수 식 세우기 디딤돌 2',
                        'level_label_en': 'Derivative Setup Step 2',
                        'stem': '$f(x) = x^3 - 3x^2 - 24x + 3$의 도함수 $f\'(x)$를 $3$으로 묶은 식은?',
                        'stem_en': 'Factoring $3$ out of $f\'(x)$ for $f(x) = x^3 - 3x^2 - 24x + 3$ gives:',
                        'options': [
                            '$3(x^2 - x - 8)$',
                            '$3(x^2 - 2x - 8)$',
                            '$3(x^2 + 2x - 8)$',
                            '$3(x^2 - 3x - 24)$',
                            '$3(x^2 - 2x + 8)$',
                        ],
                        'answer': 2,
                        'exp': '$3x^2 - 6x - 24 = 3(x^2 - 2x - 8)$입니다.',
                        'exp_en': '$3(x^2 - 2x - 8)$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [극점의 $x$좌표 찾기] $x^2 - 2x - 8 = 0$ 인수분해하기',
                'title_en': '🌱 Step 3 · [Critical Points] Solving $x^2 - 2x - 8 = 0$',
                'knowledge': '곱해서 $-8$, 더해서 $-2$가 되는 두 정수는 $2$와 $-4$이므로 $x^2 - 2x - 8 = (x + 2)(x - 4) = 0$입니다.',
                'knowledge_en': 'Factoring gives $(x + 2)(x - 4) = 0$, so $x = -2$ or $x = 4$.',
                'questions': [
                    {
                        'level_label': '극점 도출 디딤돌 3',
                        'level_label_en': 'Critical Points Step 3',
                        'stem': '최고차항 계수가 양수($1$)인 삼차함수 $f(x)$에서 $f\'(x) = 3(x + 2)(x - 4) = 0$일 때, 극댓값을 갖는 $x$의 값은?',
                        'stem_en': 'For the cubic $f(x)$ with positive leading coefficient and $f\'(x) = 3(x+2)(x-4)$, at which $x$ does the local maximum occur?',
                        'options': ['$-4$', '$-2$', '$0$', '$2$', '$4$'],
                        'answer': 2,
                        'exp': '최고차항 계수가 양수인 삼차함수는 왼쪽 근 $x = -2$에서 극대, 오른쪽 근 $x = 4$에서 극소를 가집니다.',
                        'exp_en': 'The local maximum occurs at the smaller critical point $x = -2$.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [극값 계산 및 부호 확인] $f(-2)$와 $f(4)$ 계산하기',
                'title_en': '🌳 Step 4 · [Evaluating Extrema] Computing $f(-2)$ and $f(4)$',
                'knowledge': '$f(-2) = (-2)^3 - 3(-2)^2 - 24(-2) + 3 = -8 - 12 + 48 + 3$을 계산하고, $f(4) = 64 - 48 - 96 + 3 = -77 < 0$임을 확인합니다.',
                'knowledge_en': '$f(-2) = -8 - 12 + 48 + 3 = 31 > 0$, while $f(4) = 64 - 48 - 96 + 3 = -77 < 0$.',
                'questions': [
                    {
                        'level_label': '극댓값 계산 디딤돌 4',
                        'level_label_en': 'Local Maximum Step 4',
                        'stem': '$f(x) = x^3 - 3x^2 - 24x + 3$에 $x = -2$를 대입한 극댓값 $f(-2)$는?',
                        'stem_en': 'Evaluate $f(-2)$ for $f(x) = x^3 - 3x^2 - 24x + 3$.',
                        'options': ['$25$', '$27$', '$29$', '$31$', '$35$'],
                        'answer': 4,
                        'exp': '$-8 - 12 + 48 + 3 = -20 + 51 = 31$입니다.',
                        'exp_en': '$-8 - 12 + 48 + 3 = 31$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 종합] 양수 $k$의 값 확정하기',
                'title_en': '💎 Step 5 · [Final Synthesis] Determining the positive constant $k$',
                'knowledge': '두 극값 $31$과 $-77$ 중 양수인 값은 $k = 31$입니다.',
                'knowledge_en': 'Between $31$ and $-77$, the positive value is $k = 31$.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': '곡선 $y = x^3 - 3x^2 - 24x + 3$과 직선 $y = k$가 만나는 점의 개수가 $2$가 되도록 하는 양수 $k$의 값은?',
                        'stem_en': 'Find the positive number $k$ for which $y = x^3 - 3x^2 - 24x + 3$ and $y = k$ meet at exactly $2$ points.',
                        'options': ['$27$', '$29$', '$31$', '$33$', '$35$'],
                        'answer': 3,
                        'exp': '양수인 극값은 $f(-2) = 31$이므로 $k = 31$입니다.',
                        'exp_en': '$k = f(-2) = 31$.',
                    }
                ],
            },
        ],
        'final': {
            'stem': '곡선 $y = x^3 - 3x^2 - 24x + 3$과 직선 $y = k$가 만나는 점의 개수가 $2$가 되도록 하는 양수 $k$의 값을 구하시오. [3점]',
            'stem_en': 'Find the positive constant $k$ such that the curve $y = x^3 - 3x^2 - 24x + 3$ and the line $y = k$ intersect at exactly $2$ points. [3 points]',
            'options': ['$27$', '$29$', '$31$', '$33$', '$35$'],
            'answer': 3,
            'exp': '$f(x) = x^3 - 3x^2 - 24x + 3$에서 $f\'(x) = 3(x+2)(x-4) = 0$이므로 극값은 $f(-2) = 31$, $f(4) = -77$입니다. 양수 $k$의 값은 $31$입니다.',
            'exp_en': 'Differentiating gives $f\'(x) = 3(x+2)(x-4) = 0$, yielding extrema $f(-2) = 31$ and $f(4) = -77$. Since $k > 0$, $k = 31$.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 <b>삼차함수의 그래프와 상수함수 $y = k$의 교점의 개수가 $2$가 될 필요충분조건이 $k$가 극댓값 또는 극솟값임</b>을 활용하는 전형적인 미분 활용 문항입니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  $f(x) = x^3 - 3x^2 - 24x + 3$이라 하면:<br>\n'
                '  $$f\'(x) = 3x^2 - 6x - 24 = 3(x + 2)(x - 4) = 0 \\implies x = -2 \\;\\text{또는}\\; x = 4$$\n'
                '  극댓값과 극솟값을 각각 계산하면:<br>\n'
                '  $$f(-2) = -8 - 12 + 48 + 3 = 31, \\quad f(4) = 64 - 48 - 96 + 3 = -77$$\n'
                '  $k > 0$이므로 $k = 31$입니다.\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>따라서 구하는 양수 $k$의 값은 <b>$31$</b>입니다.</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                '<p>A cubic curve with two local extrema intersects $y = k$ at exactly $2$ points if and only if $k$ equals one of its local extreme values.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  $$f\'(x) = 3(x + 2)(x - 4) = 0 \\implies f(-2) = 31, \\quad f(4) = -77$$\n'
                '  Choosing the positive value gives $k = 31$.\n'
                '</p>\n\n'
                '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                '<p>The exact short-answer value is <b>$31$</b>.</p>'
            ),
        },
    },

    # =========================================================================
    # 20번 (csat27_20) - 단답형 4점 (빈칸 추론)
    # =========================================================================
    {
        'slug': 'csat27_20',
        'qNum': '20',
        'points': 4,
        'is_short_answer': True,
        'official_ans_str': '169',
        'subject': '공통(수학I·II)',
        'title': '[2027학년도 수능 고3 공통 20번] 사인함수의 점대칭성과 이차함수의 할선 기울기 빈칸 추론',
        'title_en': '[2027 CSAT Math Common #20] Point Symmetry of a Sine Curve and Secant Slope Proof Completion',
        'summary_ko': '사인곡선의 점대칭성 $x_1 + x_2 = 2b$로 (가) $p = -2$, 이차방정식 인수분해로 (나) $q = \\dfrac{1}{6}$, 교점 대입으로 (다) $h(b) = \\dfrac{10}{3}b$를 구해 $169$ 도출하기',
        'summary_en': 'Find (가) $p = -2$ from $x_1 + x_2 = 2b$, (나) $q = \\frac{1}{6}$ by factoring $36x_1^2 - 72bx_1 + 11b^2 = 0$, and (다) $h(b) = \\frac{10}{3}b$ to compute $6(p + q + h(9)) = 169$.',
        'tags': ['2027학년도수능', '공통(수학I·II)', '수학I', '삼각함수', '사인함수의대칭성', '빈칸추론', '단답형', '20번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': '$x_1 + x_2 = 2b,\\; y_1 + y_2 = 0$',
                'desc': '곡선 $y = a\\sin\\dfrac{\\pi x}{b}$가 점 $(b, 0)$에 대하여 점대칭이므로 두 교점의 중점이 $(b, 0)$',
                'desc_en': 'Point symmetry of $y = a\\sin(\\pi x/b)$ about $(b, 0)$ implies $(b, 0)$ is the midpoint of $\\overline{\\mathrm{AB}}$.',
            },
            {
                'sym': '$(x_1 + x_2) - 2(b + 1) = -2$',
                'desc': '이차함수 $g(x)$ 위의 두 점 $\\mathrm{A}, \\mathrm{B}$를 잇는 직선 $l$의 기울기 (가)',
                'desc_en': 'Secant slope of $g(x) = x^2 - 2(b+1)x + c$ across $x_1$ and $x_2$ with $x_1 + x_2 = 2b$.',
            },
            {
                'sym': '$(6x_1 - b)(6x_1 - 11b) = 0$',
                'desc': '$x_1 < b$ 조건과 함께 점 $\\mathrm{A}$의 $x$좌표 $x_1 = \\dfrac{1}{6}b$를 결정하는 인수분해',
                'desc_en': 'Factoring $36x_1^2 - 72bx_1 + 11b^2 = 0$ with $x_1 < b$ yields $x_1 = \\frac{1}{6}b$.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 평균과 중점] 한가운데 수가 $b$인 두 수 $x_1, x_2$의 합 구하기',
                'title_en': '🔰 Step 1 · [Elementary Midpoint] Sum of two numbers whose average is $b$',
                'knowledge': '초등학교 평균 계산에서 두 수 $x_1, x_2$의 한가운데(평균)가 $b$이면 $\\dfrac{x_1 + x_2}{2} = b$이므로 두 수의 합은 $x_1 + x_2 = 2b$입니다.',
                'knowledge_en': 'If the average of $x_1$ and $x_2$ is $b$, their sum is $x_1 + x_2 = 2b$.',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '두 수 $x_1, x_2$의 합이 $x_1 + x_2 = 2b$일 때, $(x_1 + x_2) - 2(b + 1)$을 간단히 계산한 값은?',
                        'stem_en': 'When $x_1 + x_2 = 2b$, what does $(x_1 + x_2) - 2(b + 1)$ simplify to?',
                        'options': ['$-4$', '$-2$', '$-1$', '$1$', '$2$'],
                        'answer': 2,
                        'exp': '$2b - (2b + 2) = -2$입니다.',
                        'exp_en': '$2b - 2b - 2 = -2$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [빈칸 (가) 도출] 합차공식으로 직선 $l$의 기울기 $p$ 확정하기',
                'title_en': '🌿 Step 2 · [Blank (가)] Finding slope $p$ via difference of squares',
                'knowledge': '분자의 $x_2{}^2 - x_1{}^2 = (x_2 - x_1)(x_2 + x_1)$을 $(x_2 - x_1)$으로 약분하면 $\\dfrac{\\{x_2{}^2 - 2(b+1)x_2 + c\\} - \\{x_1{}^2 - 2(b+1)x_1 + c\\}}{x_2 - x_1} = (x_1 + x_2) - 2(b + 1) = -2$가 되어 빈칸 (가)의 수 $p = -2$입니다!',
                'knowledge_en': 'Dividing $(x_2^2 - x_1^2) - 2(b+1)(x_2 - x_1)$ by $(x_2 - x_1)$ gives $(x_1 + x_2) - 2(b + 1) = -2$, so $p = -2$.',
                'questions': [
                    {
                        'level_label': '빈칸 (가) 결정 디딤돌 2',
                        'level_label_en': 'Blank (가) Step 2',
                        'stem': '빈칸 (가)에 들어갈 수 $p = -2$일 때, 직선 $l$의 방정식 ㉠ $y = p \\times (x - b)$는?',
                        'stem_en': 'With $p = -2$ in blank (가), what is equation ㉠ of line $l$?',
                        'options': [
                            '$y = -2(x + b)$',
                            '$y = -2(x - b)$',
                            '$y = -(x - b)$',
                            '$y = 2(x - b)$',
                            '$y = 2(x + b)$',
                        ],
                        'answer': 2,
                        'exp': '빈칸 (가)에 $-2$를 대입하면 직선 $l$의 방정식은 $y = -2(x - b)$입니다.',
                        'exp_en': 'Substituting $p = -2$ gives $y = -2(x - b)$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [빈칸 (나) 도출] $36x_1{}^2 - 72bx_1 + 11b^2 = 0$ ($x_1 < b$) 인수분해하기',
                'title_en': '🌱 Step 3 · [Blank (나)] Factoring $36x_1^2 - 72bx_1 + 11b^2 = 0$ ($x_1 < b$)',
                'knowledge': '$36 = 6 \\times 6$, $11 = 1 \\times 11$이고 $-6 - 66 = -72$이므로 $(6x_1 - b)(6x_1 - 11b) = 0$으로 인수분해됩니다! 이때 $x_1 < b$ ($b > 1$)이므로 $x_1 = \\dfrac{1}{6}b$입니다.',
                'knowledge_en': 'Factoring gives $(6x_1 - b)(6x_1 - 11b) = 0$. Since $x_1 < b$ and $b > 1$, we select $x_1 = \\frac{1}{6}b$.',
                'questions': [
                    {
                        'level_label': '빈칸 (나) 결정 디딤돌 3',
                        'level_label_en': 'Blank (나) Step 3',
                        'stem': '$36x_1{}^2 - 72bx_1 + 11b^2 = 0\\;(x_1 < b)$을 만족하는 점 $\\mathrm{A}$의 $x$좌표가 $q \\times b$일 때, 빈칸 (나)의 수 $q$는?',
                        'stem_en': 'From $(6x_1 - b)(6x_1 - 11b) = 0$ with $x_1 < b$, what is $q$ in $x_1 = q \\times b$?',
                        'options': ['$\\dfrac{1}{12}$', '$\\dfrac{1}{6}$', '$\\dfrac{1}{3}$', '$\\dfrac{5}{6}$', '$\\dfrac{11}{6}$'],
                        'answer': 2,
                        'exp': '$x_1 = \\dfrac{1}{6}b$와 $x_1 = \\dfrac{11}{6}b$ 중 $x_1 < b$인 것은 $\\dfrac{1}{6}b$이므로 $q = \\dfrac{1}{6}$입니다.',
                        'exp_en': 'Since $\\frac{11}{6}b > b$, we must have $x_1 = \\frac{1}{6}b$, so $q = \\frac{1}{6}$.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [빈칸 (다) 도출] 점 $\\mathrm{A}$에서 $f(x_1) = y_1$을 이용해 $h(b)$ 구하기',
                'title_en': '🌳 Step 4 · [Blank (다)] Equating $f(x_1) = y_1$ at point $\\mathrm{A}$ to find $h(b)$',
                'knowledge': '$x_1 = \\dfrac{1}{6}b$를 직선 $l$의 식 $y = -2(x - b)$에 대입하면 $y_1 = -2\\left(\\dfrac{1}{6}b - b\\right) = \\dfrac{5}{3}b$이고, $f(x) = a\\sin\\dfrac{\\pi x}{b}$에 대입하면 $f\\left(\\dfrac{1}{6}b\\right) = a\\sin\\dfrac{\\pi}{6} = \\dfrac{1}{2}a$입니다.',
                'knowledge_en': 'At $x_1 = \\frac{1}{6}b$, line $l$ gives $y_1 = -2\\left(-\\frac{5}{6}b\\right) = \\frac{5}{3}b$, while $f(x_1) = a\\sin\\frac{\\pi}{6} = \\frac{1}{2}a$.',
                'questions': [
                    {
                        'level_label': '빈칸 (다) 결정 디딤돌 4',
                        'level_label_en': 'Blank (다) Step 4',
                        'stem': '$\\dfrac{1}{2}a = \\dfrac{5}{3}b$에서 빈칸 (다)의 식 $a = h(b)$를 구하고, $b = 9$를 대입한 $h(9)$의 값은?',
                        'stem_en': 'From $\\frac{1}{2}a = \\frac{5}{3}b$, find $h(b) = a$ and evaluate $h(9)$.',
                        'options': ['$15$', '$20$', '$25$', '$30$', '$36$'],
                        'answer': 4,
                        'exp': '$h(b) = \\dfrac{10}{3}b$이므로 $h(9) = \\dfrac{10}{3} \\times 9 = 30$입니다.',
                        'exp_en': '$h(b) = \\frac{10}{3}b$, so $h(9) = 30$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 종합] $6 \\times (p + q + h(9))$의 값 계산하기',
                'title_en': '💎 Step 5 · [Final Synthesis] Evaluating $6 \\times (p + q + h(9))$',
                'knowledge': '$p = -2$, $q = \\dfrac{1}{6}$, $h(9) = 30$을 대입하여 분배법칙으로 계산합니다: $6 \\times \\left(-2 + \\dfrac{1}{6} + 30\\right) = 6 \\times 28 + 1$.',
                'knowledge_en': 'Substitute $p = -2$, $q = \\frac{1}{6}$, and $h(9) = 30$ into $6(p + q + h(9))$.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': '$p = -2$, $q = \\dfrac{1}{6}$, $h(9) = 30$일 때, $6 \\times (p + q + h(9))$의 값은?',
                        'stem_en': 'Given $p = -2$, $q = \\frac{1}{6}$, and $h(9) = 30$, what is $6 \\times (p + q + h(9))$?',
                        'options': ['$163$', '$166$', '$169$', '$172$', '$175$'],
                        'answer': 3,
                        'exp': '$6 \\times \\left(28 + \\dfrac{1}{6}\\right) = 168 + 1 = 169$입니다.',
                        'exp_en': '$6(28) + 1 = 169$.',
                    }
                ],
            },
        ],
        'final': {
            'stem': (
                '세 상수 $a\\,(a > 0)$, $b\\,(b > 1)$, $c$에 대하여 닫힌구간 $[0, 2b]$에서 정의된 두 함수<br>'
                '$$f(x) = a\\sin\\frac{\\pi x}{b}, \\quad g(x) = x^2 - 2(b + 1)x + c$$'
                '가 있다. 두 곡선 $y = f(x)$와 $y = g(x)$의 서로 다른 두 교점 $\\mathrm{A}(x_1, y_1)$, $\\mathrm{B}(x_2, y_2)\\,(x_1 &lt; b &lt; x_2)$가 존재하고, '
                '$y_2(x_1 - b) = y_1(x_2 - b)$가 성립한다고 하자.<br>'
                '다음은 직선 $\\mathrm{OA}$와 직선 $\\mathrm{OB}$의 기울기의 합이 $\\dfrac{100}{11}$일 때, $a$를 $b$에 대한 식으로 나타내는 과정이다. (단, $\\mathrm{O}$는 원점이다.)'
                '<div style="margin:10px 0;padding:12px 14px;border:1.5px solid #475569;border-radius:8px;background:#f8fafc">'
                '<div style="color:#1e293b;line-height:1.85">'
                '두 점 $\\mathrm{A}$, $\\mathrm{B}$를 지나는 직선을 $l$이라 하자.<br>'
                '주어진 조건으로부터 $\\dfrac{y_1}{x_1 - b} = \\dfrac{y_2}{x_2 - b}$ 이므로<br>'
                '직선 $l$이 점 $(b, 0)$을 지난다.<br>'
                '함수 $y = f(x)$의 그래프의 성질로부터 선분 $\\mathrm{AB}$의 중점의 좌표가 $(b, 0)$이므로 $x_1 + x_2 = 2b$, $y_1 + y_2 = 0$이다.<br>'
                '또한 두 점 $\\mathrm{A}$, $\\mathrm{B}$는 함수 $y = g(x)$의 그래프와 직선 $l$이 만나는 점이므로 직선 $l$의 기울기는'
                '$$\\frac{\\{x_2{}^2 - 2(b + 1)x_2 + c\\} - \\{x_1{}^2 - 2(b + 1)x_1 + c\\}}{x_2 - x_1} = \\boxed{\\text{ (가) }}$$'
                '이고, 직선 $l$의 방정식은'
                '$$y = \\boxed{\\text{ (가) }} \\times (x - b) \\quad \\cdots\\cdots \\text{ ㉠}$$'
                '이다. $\\dfrac{y_1}{x_1} - \\dfrac{y_1}{2b - x_1} = \\dfrac{100}{11}$ 이므로 ㉠을 이용하여 정리하면'
                '$$36x_1{}^2 - 72bx_1 + 11b^2 = 0 \\;\\;(x_1 &lt; b)$$'
                '이고, 점 $\\mathrm{A}$의 $x$좌표는 $\\boxed{\\text{ (나) }} \\times b$이다.<br>'
                '점 $\\mathrm{A}$는 곡선 $y = f(x)$와 직선 $l$의 교점이므로 $a$를 $b$에 대한 식으로 나타내면'
                '$$a = \\boxed{\\text{ (다) }}$$'
                '이다.'
                '</div></div>'
                '위의 (가), (나)에 알맞은 수를 각각 $p$, $q$라 하고, (다)에 알맞은 식을 $h(b)$라 하자. $6 \\times (p + q + h(9))$의 값을 구하시오. [4점]'
            ),
            'stem_en': (
                'For constants $a > 0$, $b > 1$, and $c$, define on $[0, 2b]$:<br>'
                '$$f(x) = a\\sin\\frac{\\pi x}{b}, \\quad g(x) = x^2 - 2(b + 1)x + c.$$'
                'Suppose $y = f(x)$ and $y = g(x)$ intersect at $\\mathrm{A}(x_1, y_1)$ and $\\mathrm{B}(x_2, y_2)$ with $x_1 &lt; b &lt; x_2$ and $y_2(x_1 - b) = y_1(x_2 - b)$. '
                'Below is the derivation expressing $a$ in terms of $b$ when the sum of the slopes of $\\mathrm{OA}$ and $\\mathrm{OB}$ is $\\dfrac{100}{11}$ ($\\mathrm{O}$ is the origin).'
                '<div style="margin:10px 0;padding:12px 14px;border:1.5px solid #475569;border-radius:8px;background:#f8fafc">'
                '<div style="color:#1e293b;line-height:1.85">'
                'Let $l$ be the line through $\\mathrm{A}$ and $\\mathrm{B}$. Since $\\dfrac{y_1}{x_1 - b} = \\dfrac{y_2}{x_2 - b}$, $l$ passes through $(b, 0)$.<br>'
                'By the point symmetry of $y = f(x)$ about $(b, 0)$, the midpoint of $\\overline{\\mathrm{AB}}$ is $(b, 0)$, so $x_1 + x_2 = 2b$ and $y_1 + y_2 = 0$.<br>'
                'Since $\\mathrm{A}$ and $\\mathrm{B}$ also lie on $y = g(x)$, the slope of $l$ is'
                '$$\\frac{\\{x_2{}^2 - 2(b + 1)x_2 + c\\} - \\{x_1{}^2 - 2(b + 1)x_1 + c\\}}{x_2 - x_1} = \\boxed{\\text{ (가) }},$$'
                'giving equation ㉠: $y = \\boxed{\\text{ (가) }} \\times (x - b)$.<br>'
                'Substituting ㉠ into $\\dfrac{y_1}{x_1} - \\dfrac{y_1}{2b - x_1} = \\dfrac{100}{11}$ yields $36x_1{}^2 - 72bx_1 + 11b^2 = 0\\;(x_1 &lt; b)$, '
                'so the $x$-coordinate of $\\mathrm{A}$ is $\\boxed{\\text{ (나) }} \\times b$.<br>'
                'Since $\\mathrm{A}$ lies on both $y = f(x)$ and $l$, expressing $a$ in terms of $b$ gives $a = \\boxed{\\text{ (다) }}$.'
                '</div></div>'
                'Let $p$ and $q$ be the numbers in (가) and (나), and let $h(b)$ be the expression in (다). Find $6 \\times (p + q + h(9))$. [4 points]'
            ),
            'options': ['$163$', '$166$', '$169$', '$172$', '$175$'],
            'answer': 3,
            'exp': '$p = (x_1+x_2) - 2(b+1) = -2$, $(6x_1-b)(6x_1-11b)=0\\;(x_1<b)$에서 $q = \\dfrac{1}{6}$, $\\dfrac{1}{2}a = \\dfrac{5}{3}b$에서 $h(b) = \\dfrac{10}{3}b$이므로 $6 \\times \\left(-2 + \\dfrac{1}{6} + 30\\right) = 169$입니다.',
            'exp_en': 'We find $p = -2$, $q = \\dfrac{1}{6}$, and $h(b) = \\dfrac{10}{3}b$, so $h(9) = 30$ and $6 \\times \\left(-2 + \\dfrac{1}{6} + 30\\right) = 169$.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 <b>삼각함수 $y = a\\sin\\dfrac{\\pi x}{b}$의 점 $(b, 0)$ 대칭성과 이차함수의 할선의 기울기 성질</b>을 결합한 추론 완성형 단답형 문항입니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: 빈칸 (가)의 값 $p$ 구하기</b><br>\n'
                '  $x_1 + x_2 = 2b$이므로 직선 $l$의 기울기는:<br>\n'
                '  $$\\frac{(x_2{}^2 - x_1{}^2) - 2(b + 1)(x_2 - x_1)}{x_2 - x_1} = (x_1 + x_2) - 2(b + 1) = 2b - 2b - 2 = -2 \\implies p = -2$$<br>\n'
                '  <b>2단계: 빈칸 (나)의 값 $q$ 구하기</b><br>\n'
                '  $36x_1{}^2 - 72bx_1 + 11b^2 = (6x_1 - b)(6x_1 - 11b) = 0$이고 $x_1 < b$ ($b > 1$)이므로:<br>\n'
                '  $$x_1 = \\frac{1}{6}b \\implies q = \\frac{1}{6}$$<br>\n'
                '  <b>3단계: 빈칸 (다)의 식 $h(b)$ 및 최종 답 계산</b><br>\n'
                '  점 $\\mathrm{A}$의 $y$좌표는 ㉠에 의해 $y_1 = -2\\left(\\dfrac{1}{6}b - b\\right) = \\dfrac{5}{3}b$이고, 곡선 $y = f(x)$ 위에서 $y_1 = a\\sin\\dfrac{\\pi}{6} = \\dfrac{1}{2}a$이므로:<br>\n'
                '  $$\\frac{1}{2}a = \\frac{5}{3}b \\implies a = h(b) = \\frac{10}{3}b \\implies h(9) = 30$$\n'
                '  따라서 $6 \\times (p + q + h(9)) = 6 \\times \\left(-2 + \\dfrac{1}{6} + 30\\right) = 168 + 1 = 169$입니다.\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>따라서 구하는 값은 <b>$169$</b>입니다.</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                '<p>This proof-completion problem combines <b>point symmetry of $y = a\\sin(\\pi x/b)$ about $(b, 0)$</b> with the secant slope formula on a parabola.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Blank (가)</b>: $(x_1 + x_2) - 2(b + 1) = 2b - 2b - 2 = -2 \\implies p = -2$.<br><br>\n'
                '  <b>Step 2: Blank (나)</b>: $(6x_1 - b)(6x_1 - 11b) = 0$ with $x_1 < b$ gives $x_1 = \\frac{1}{6}b \\implies q = \\frac{1}{6}$.<br><br>\n'
                '  <b>Step 3: Blank (다)</b>: Equating $f(b/6) = a\\sin(\\pi/6) = \\frac{1}{2}a$ with $-2(b/6 - b) = \\frac{5}{3}b$ yields $h(b) = \\frac{10}{3}b$ and $h(9) = 30$.<br>\n'
                '  Finally, $6 \\times \\left(-2 + \\frac{1}{6} + 30\\right) = 169$.\n'
                '</p>\n\n'
                '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                '<p>The exact short-answer value is <b>$169$</b>.</p>'
            ),
        },
    },

    # =========================================================================
    # 21번 (csat27_21) - 단답형 4점
    # =========================================================================
    {
        'slug': 'csat27_21',
        'qNum': '21',
        'points': 4,
        'is_short_answer': True,
        'official_ans_str': '135',
        'subject': '공통(수학I·II)',
        'title': '[2027학년도 수능 고3 공통 21번] 반직선 구간의 최댓값·최솟값의 곱 함수 $g(t)$와 미분가능성',
        'title_en': '[2027 CSAT Math Common #21] Product of Half-Line Maximum and Minimum of a Monic Cubic Function',
        'summary_ko': '극댓값 $M_0 = f(-1) < 0$과 $f(2) = 0$을 파악하고, $f(a) = M_0$인 양수 $a = 1$에서의 좌·우미분계수 차 $-M_0 f\'(a) = 36$으로부터 $f(x) = x^3+x^2-x-10$ 및 $f(5) = 135$ 도출하기',
        'summary_en': 'Deduce local max $M_0 = f(-1) < 0$ and root $f(2) = 0$ from (나), use $-M_0 f\'(a) = 36$ at $a = 1 > 0$ from (가) to obtain $f(x) = x^3+x^2-x-10$, and evaluate $f(5) = 135$.',
        'tags': ['2027학년도수능', '공통(수학I·II)', '수학II', '미분', '삼차함수비율관계', '좌우미분계수', '최대최소함수', '21번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': '$M(t) = \\max_{( -\\infty, t ]} f(x),\\; m(t) = \\min_{[ t, \\infty )} f(x)$',
                'desc': '$t$ 왼쪽에서의 가장 높은 값 $M(t)$와 $t$ 오른쪽에서의 가장 낮은 값 $m(t)$',
                'desc_en': 'Running maximum $M(t)$ up to $t$ and running minimum $m(t)$ from $t$ onward.',
            },
            {
                'sym': '$t \\in [\\alpha, \\beta] \\implies g(t) = M_0 m_0 \\;(\\text{상수})$',
                'desc': '극대점 $\\alpha$와 극소점 $\\beta$ 사이에서는 $M(t)=M_0$, $m(t)=m_0$으로 고정되어 $g\'(t)=0$',
                'desc_en': 'Between local max $\\alpha$ and local min $\\beta$, $g(t) = M_0 m_0$ is constant so $g\'(t) = 0$.',
            },
            {
                'sym': '$g\'_-(a) - g\'_+(a) = -M_0 f\'(a) = 36$',
                'desc': '$f(a) = M_0 < 0$인 점 $a > \\beta$에서 $M(t)$가 상수 $M_0$에서 $f(t)$로 바뀌며 생기는 미분계수 차',
                'desc_en': 'Derivative jump at $a > \\beta$ where $f(a) = M_0 < 0$ transitions $g(t)$ from $M_0 f(t)$ to $\\{f(t)\\}^2$.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 높낮이 직관] 산봉우리($\\alpha$)와 골짜기($\\beta$) 사이에서 최댓값과 최솟값 관찰하기',
                'title_en': '🔰 Step 1 · [Elementary Height Intuition] Running max and min between peak $\\alpha$ and valley $\\beta$',
                'knowledge': '왼쪽에서 산봉우리(높이 $M_0$)를 넘어 골짜기(높이 $m_0$)로 내려가는 길 위의 점 $t$ ($\\alpha \\le t \\le \\beta$)에 서 있다고 상상해 봅시다! 지나온 왼쪽 길에서 가장 높았던 곳은 언제나 봉우리 높이 $M_0$이고, 앞으로 갈 오른쪽 길에서 가장 낮은 곳은 언제나 골짜기 높이 $m_0$입니다.',
                'knowledge_en': 'Standing anywhere at $t \\in [\\alpha, \\beta]$ between the peak (height $M_0$) and valley (height $m_0$), the highest point behind you is fixed at $M_0$ and the lowest point ahead is fixed at $m_0$.',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '구간 $[\\alpha, \\beta]$에서 왼쪽 최댓값이 $M_0$, 오른쪽 최솟값이 $m_0$으로 일정할 때, 두 값의 곱 $g(t) = M_0 m_0$의 변화율(기울기) $g\'(t)$는 얼마인가요?',
                        'stem_en': 'Since $g(t) = M_0 m_0$ stays completely constant on $[\\alpha, \\beta]$, what is its rate of change $g\'(t)$ on $[\\alpha, \\beta]$?',
                        'options': ['$-1$', '$0$', '$1$', '$M_0$', '$M_0 m_0$'],
                        'answer': 2,
                        'exp': '값이 변하지 않는 상수구간이므로 기울기(도함수) $g\'(t) = 0$입니다! (양 끝점에서도 $f\'(\\alpha)=f\'(\\beta)=0$이므로 $g\'(\\alpha)=g\'(\\beta)=0$입니다.)',
                        'exp_en': 'The derivative of a constant is $0$, so $g\'(t) = 0$ across $[\\alpha, \\beta]$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [꺾이는 점 분석] 조건 (가)와 (나)로부터 $\\alpha = -1$, 실근 $r = 2$, $M_0 < 0$ 확정하기',
                'title_en': '🌿 Step 2 · [Corner & Sign Analysis] Deducing $\\alpha = -1$, root $r = 2$, and $M_0 < 0$',
                'knowledge': '$f(x)$가 다시 봉우리 높이 $M_0$과 같아지는 점 $\\gamma$ ($f(\\gamma) = M_0$)에서 $g(t)$는 왼쪽 $M_0 f(t)$에서 오른쪽 $\\{f(t)\\}^2$으로 바뀝니다. 따라서 좌미분계수 빼기 우미분계수는 $M_0 f\'(\\gamma) - 2M_0 f\'(\\gamma) = -M_0 f\'(\\gamma) = 36 > 0$이므로 **$M_0 < 0$**이고 $a = \\gamma > 0$입니다! 또한 $M_0 < 0$이면 $x > a$에서 $f(r) = 0$인 유일한 실근 $r$이 존재하여 $g\'(b) = 0$인 집합은 $[\\alpha, \\beta] \\cup \\{r\\}$이 됩니다.',
                'knowledge_en': 'At $a = \\gamma$ where $f(\\gamma) = M_0$, $g\'_-(\\gamma) - g\'_+(\\gamma) = -M_0 f\'(\\gamma) = 36 > 0$, forcing $M_0 < 0$! Then $f$ has a unique real root $r > a$, so $\\{b : g\'(b)=0\\} = [\\alpha, \\beta] \\cup \\{r\\}$.',
                'questions': [
                    {
                        'level_label': '최대·최소 지점 매칭 디딤돌 2',
                        'level_label_en': 'Matching Bounds Step 2',
                        'stem': '$\\{b : g\'(b) = 0\\} = [\\alpha, \\beta] \\cup \\{r\\}$ ($\\alpha < \\beta < a < r$)이고 조건 (나)에서 $b$의 최솟값이 $-1$, 최댓값이 $2$일 때, $(\\alpha, r)$의 값은?',
                        'stem_en': 'Given $\\{b : g\'(b) = 0\\} = [\\alpha, \\beta] \\cup \\{r\\}$ with $\\alpha < \\beta < a < r$, and condition (나) giving min $-1$ and max $2$, what is $(\\alpha, r)$?',
                        'options': ['$(-1, 1)$', '$(-1, 2)$', '$(0, 2)$', '$(-2, 1)$', '$(-2, 2)$'],
                        'answer': 2,
                        'exp': '가장 작은 값은 극대점 $\\alpha = -1$이고, 가장 큰 값은 $f(r) = 0$인 실근 $r = 2$입니다.',
                        'exp_en': 'The minimum is $\\alpha = -1$ and the maximum is $r = 2$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [삼차함수 식 세우기] $f(-1) = f(a) = M_0$과 $f(2) = 0$ 연결하기',
                'title_en': '🌱 Step 3 · [Cubic Equation Setup] Using $f(-1) = f(a) = M_0$ and $f(2) = 0$',
                'knowledge': '최고차항 계수가 $1$인 삼차함수 $f(x)$가 $x = -1$에서 가로선 $y = M_0$에 접하고 $x = a$에서 만나므로 **$f(x) = (x + 1)^2(x - a) + M_0$**으로 놓을 수 있습니다! 여기에 $f(2) = 0$을 대입하면 $M_0$을 $a$로 나타낼 수 있습니다.',
                'knowledge_en': 'Since $y = f(x)$ is tangent to $y = M_0$ at $x = -1$ and crosses it at $x = a$, write $f(x) = (x + 1)^2(x - a) + M_0$ and apply $f(2) = 0$.',
                'questions': [
                    {
                        'level_label': 'M0 관계식 도출 디딤돌 3',
                        'level_label_en': 'Expressing M0 Step 3',
                        'stem': '$f(x) = (x + 1)^2(x - a) + M_0$에 $f(2) = 0$을 대입하여 $M_0$을 $a$에 대한 식으로 바르게 나타낸 것은?',
                        'stem_en': 'Substituting $f(2) = 0$ into $f(x) = (x + 1)^2(x - a) + M_0$, what is $M_0$ in terms of $a$?',
                        'options': ['$-3(2 - a)$', '$-6(2 - a)$', '$-9(2 - a)$', '$9(2 - a)$', '$-9(a + 1)$'],
                        'answer': 3,
                        'exp': '$f(2) = 3^2(2 - a) + M_0 = 9(2 - a) + M_0 = 0$이므로 $M_0 = -9(2 - a)$입니다.',
                        'exp_en': '$9(2 - a) + M_0 = 0 \\implies M_0 = -9(2 - a)$.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [양수 $a$ 결정] $-M_0 f\'(a) = 36$으로부터 $a = 1$과 $M_0 = -9$ 구하기',
                'title_en': '🌳 Step 4 · [Finding Positive a] Solving $-M_0 f\'(a) = 36$ for $a = 1$',
                'knowledge': '$f(x) = (x + 1)^2(x - a) + M_0$을 미분하여 $x = a$를 대입하면 $f\'(a) = (a + 1)^2$입니다. 이를 $-M_0 f\'(a) = 36$에 대입하면 $9(2 - a)(a + 1)^2 = 36 \\implies (2 - a)(a + 1)^2 = 4$가 됩니다.',
                'knowledge_en': 'Since $f\'(a) = (a + 1)^2$, $-M_0 f\'(a) = 36$ becomes $9(2 - a)(a + 1)^2 = 36 \\implies (2 - a)(a + 1)^2 = 4$.',
                'questions': [
                    {
                        'level_label': '양수 a 결정 디딤돌 4',
                        'level_label_en': 'Solving for a Step 4',
                        'stem': '$0 < a < 2$인 양수 $a$에 대하여 $(2 - a)(a + 1)^2 = 4$를 만족시키는 $a$와 그때의 $M_0 = -9(2 - a)$를 바르게 구한 것은?',
                        'stem_en': 'For $0 < a < 2$, solve $(2 - a)(a + 1)^2 = 4$ to find $(a, M_0)$.',
                        'options': [
                            '$a = \\dfrac{1}{2},\\; M_0 = -\\dfrac{27}{2}$',
                            '$a = 1,\\; M_0 = -9$',
                            '$a = 1,\\; M_0 = -4$',
                            '$a = \\dfrac{3}{2},\\; M_0 = -\\dfrac{9}{2}$',
                            '$a = 2,\\; M_0 = 0$',
                        ],
                        'answer': 2,
                        'exp': '$a = 1$일 때 $(2 - 1)(1 + 1)^2 = 1 \\times 4 = 4$가 정확히 성립합니다! (인수분해하면 $(a + 2)(a - 1)^2 = 0$이므로 양수 해는 $a = 1$뿐입니다.) 이때 $M_0 = -9(2 - 1) = -9$입니다.',
                        'exp_en': 'Expanding gives $(a + 2)(a - 1)^2 = 0$, so for $a > 0$, $a = 1$ and $M_0 = -9$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 종합] 완성된 $f(x) = (x + 1)^2(x - 1) - 9$에 $x = 5$ 대입하기',
                'title_en': '💎 Step 5 · [Final Synthesis] Evaluating $f(5)$',
                'knowledge': '완성된 삼차함수 $f(x) = (x + 1)^2(x - 1) - 9$ (전개하면 $x^3 + x^2 - x - 10$)에 $x = 5$를 대입합니다.',
                'knowledge_en': 'Substitute $x = 5$ into $f(x) = (x + 1)^2(x - 1) - 9$.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': '$f(x) = (x + 1)^2(x - 1) - 9$일 때, $f(5)$의 값은?',
                        'stem_en': 'For $f(x) = (x + 1)^2(x - 1) - 9$, what is the value of $f(5)$?',
                        'options': ['$125$', '$130$', '$135$', '$140$', '$145$'],
                        'answer': 3,
                        'exp': '$f(5) = 6^2 \\times 4 - 9 = 144 - 9 = 135$입니다.',
                        'exp_en': '$f(5) = 36 \\times 4 - 9 = 135$.',
                    }
                ],
            },
        ],
        'final': {
            'stem': (
                '최고차항의 계수가 $1$인 삼차함수 $f(x)$가 있다. 실수 $t$에 대하여 구간 $(-\\infty, t]$에서 $f(x)$의 최댓값과 구간 $[t, \\infty)$에서 $f(x)$의 최솟값의 곱을 $g(t)$라 할 때, 다음 조건이 성립한다.'
                '<div style="margin:10px 0;padding:12px 14px;border:1.5px solid #475569;border-radius:8px;background:#f8fafc">'
                '<div style="color:#1e293b;line-height:1.85">'
                '(가) 어떤 양수 $a$에 대하여'
                '$$\\lim_{t \\to a-} \\frac{g(t) - g(a)}{t - a} - \\lim_{t \\to a+} \\frac{g(t) - g(a)}{t - a} = 36 \\text{ 이다.}$$'
                '(나) $g\'(b) = 0$인 실수 $b$의 최댓값은 $2$이고,<br>'
                '&nbsp;&nbsp;&nbsp;&nbsp;최솟값은 $-1$이다.'
                '</div></div>'
                '$f(5)$의 값을 구하시오. [4점]'
            ),
            'stem_en': (
                'Let $f(x)$ be a monic cubic function. For each real $t$, let $g(t)$ be the product of the maximum of $f(x)$ on $(-\\infty, t]$ and the minimum of $f(x)$ on $[t, \\infty)$. Suppose $g(t)$ satisfies:'
                '<div style="margin:10px 0;padding:12px 14px;border:1.5px solid #475569;border-radius:8px;background:#f8fafc">'
                '<div style="color:#1e293b;line-height:1.85">'
                '(가) For some positive real number $a > 0$,'
                '$$\\lim_{t \\to a-} \\frac{g(t) - g(a)}{t - a} - \\lim_{t \\to a+} \\frac{g(t) - g(a)}{t - a} = 36.$$'
                '(나) Among all real numbers $b$ such that $g\'(b) = 0$, the maximum is $2$ and the minimum is $-1$.'
                '</div></div>'
                'Find the value of $f(5)$. [4 points]'
            ),
            'options': ['$125$', '$130$', '$135$', '$140$', '$145$'],
            'answer': 3,
            'exp': '극대점 $\\alpha=-1$, 유일한 실근 $r=2$이고 $f(-1)=f(a)=M_0<0$인 양수 $a$에서 $-M_0 f\'(a)=36$입니다. $f(x)=(x+1)^2(x-a)-9(2-a)$에서 $(2-a)(a+1)^2=4 \\implies a=1, M_0=-9$이므로 $f(5)=36\\times 4-9=135$입니다.',
            'exp_en': 'With local max $\\alpha = -1$, root $r = 2$, and $f(-1) = f(a) = M_0 < 0$ ($a > 0$), $-M_0 f\'(a) = 36$ yields $9(2-a)(a+1)^2 = 36 \\implies a = 1$ and $M_0 = -9$. Thus $f(x) = (x+1)^2(x-1) - 9$ and $f(5) = 135$.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 단답형 준킬러·킬러(21번) 문항으로, 반직선 위의 최댓값 함수 $M(t)$와 최솟값 함수 $m(t)$의 곱 $g(t) = M(t)m(t)$의 <b>미분불가능점에서의 좌·우미분계수 차</b>와 <b>도함수가 $0$이 되는 구간의 양 끝</b>을 정밀하게 추론하는 문제입니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: $M(t), m(t)$의 구조와 미분불가능점 분석</b><br>\n'
                '  $f(x)$가 극값을 갖지 않으면 $g(t) = \\{f(t)\\}^2$으로 실수 전체에서 미분가능하므로 모순입니다. 따라서 $f(x)$는 $x = \\alpha$에서 극댓값 $M_0$, $x = \\beta$에서 극솟값 $m_0$을 가집니다.<br>\n'
                '  $f(\\delta) = m_0$ ($\\delta < \\alpha$), $f(\\gamma) = M_0$ ($\\gamma > \\beta$)라 하면 $\\delta < \\alpha < \\beta < \\gamma$이고:<br>\n'
                '  • $[\\alpha, \\beta]$에서 $g(t) = M_0 m_0$ (상수)이며 $f\'(\\alpha) = f\'(\\beta) = 0$이므로 $[\\alpha, \\beta]$ 전체에서 $g\'(t) = 0$입니다.<br>\n'
                '  • 미분불가능 후보점은 $t = \\delta$ (좌·우미분계수 차 $+m_0 f\'(\\delta)$)와 $t = \\gamma$ (좌·우미분계수 차 $-M_0 f\'(\\gamma)$)뿐입니다.<br><br>\n'
                '  <b>2단계: 두 부호 케이스 검증 및 $a = 1$ 도출</b><br>\n'
                '  ① 만약 $m_0 > 0$ ($a = \\delta > 0$)이면 $f(-1) = 0$, $\\beta = 2$이고 $f(x) = (x - \\delta)(x - 2)^2 + m_0$에서 $m_0 = 9(1 + \\delta)$, $f\'(\\delta) = (2 - \\delta)^2$입니다. 이때 $m_0 f\'(\\delta) = 9(1 + \\delta)(2 - \\delta)^2 = 36 \\iff \\delta^3 - 3\\delta^2 = 0$은 $0 < \\delta < 2$에서 해가 없어($\\delta = 0$은 양수가 아님!) 모순입니다.<br>\n'
                '  ② 따라서 <b>$M_0 < 0$이고 $a = \\gamma > 0$</b>입니다! 이때 $\\{b : g\'(b) = 0\\} = [\\alpha, \\beta] \\cup \\{r\\}$ ($f(r) = 0, r > a$)이므로 조건 (나)에 의해 <b>$\\alpha = -1$, $r = 2$</b>입니다.<br>\n'
                '  $f(x) = (x + 1)^2(x - a) + M_0$에서 $f(2) = 9(2 - a) + M_0 = 0 \\implies M_0 = -9(2 - a)$이고, $f\'(a) = (a + 1)^2$이므로:<br>\n'
                '  $$-M_0 f\'(a) = 9(2 - a)(a + 1)^2 = 36 \\implies (a + 2)(a - 1)^2 = 0$$\n'
                '  $a > 0$이므로 $a = 1$, $M_0 = -9$이고 $f(x) = (x + 1)^2(x - 1) - 9 = x^3 + x^2 - x - 10$입니다.<br><br>\n'
                '  <b>3단계: $f(5)$ 계산</b><br>\n'
                '  $$f(5) = (5 + 1)^2(5 - 1) - 9 = 36 \\times 4 - 9 = 135$$\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>조건 (가)의 "양수 $a$" 조건이 $\\delta = 0$ 케이스를 정확히 배제하는 핵심 장치임을 확인했습니다. 정답은 <b>$135$</b>입니다.</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                '<p>This problem analyzes the piecewise structure and corner derivatives of $g(t) = \\left(\\max_{(-\\infty, t]} f\\right)\\left(\\min_{[t, \\infty)} f\\right)$ for a monic cubic $f(x)$.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Corner derivative analysis</b><br>\n'
                '  Let $\\alpha < \\beta$ be the local max and min of $f$, with $f(\\delta) = m_0 = f(\\beta)$ ($\\delta < \\alpha$) and $f(\\gamma) = M_0 = f(\\alpha)$ ($\\gamma > \\beta$). Always $[\\alpha, \\beta] \\subset \\{b : g\'(b) = 0\\}$.<br>\n'
                '  The jump $g\'_-(a) - g\'_+(a) = 36 > 0$ occurs either at $a = \\delta > 0$ with $m_0 > 0$ (which yields $9(1+\\delta)(2-\\delta)^2 = 36 \\implies \\delta = 0$, contradicting $a > 0$) or at $a = \\gamma > 0$ with $M_0 < 0$.<br><br>\n'
                '  <b>Step 2: Solve for $f(x)$ when $M_0 < 0$</b><br>\n'
                '  Here $\\{b : g\'(b) = 0\\} = [\\alpha, \\beta] \\cup \\{r\\}$ where $f(r) = 0$, giving $\\alpha = -1$ and $r = 2$.<br>\n'
                '  Writing $f(x) = (x+1)^2(x-a) + M_0$ with $f(2) = 0$ gives $M_0 = -9(2-a)$, and $-M_0 f\'(a) = 9(2-a)(a+1)^2 = 36 \\implies (a+2)(a-1)^2 = 0 \\implies a = 1$, $M_0 = -9$.<br><br>\n'
                '  <b>Step 3: Evaluate $f(5)$</b><br>\n'
                '  $$f(5) = (5 + 1)^2(5 - 1) - 9 = 144 - 9 = 135$$\n'
                '</p>\n\n'
                '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                '<p>The exact short-answer value is <b>$135$</b>.</p>'
            ),
        },
    },

    # =========================================================================
    # 22번 (csat27_22) - 단답형 4점
    # =========================================================================
    {
        'slug': 'csat27_22',
        'qNum': '22',
        'points': 4,
        'is_short_answer': True,
        'official_ans_str': '98',
        'subject': '공통(수학I·II)',
        'title': '[2027학년도 수능 고3 공통 22번] 주기 $3$인 수열의 대칭식 연립과 분수 급수의 합',
        'title_en': '[2027 CSAT Math Common #22] Periodic Sequence of Period 3, Symmetric Relations, and Reciprocal Product Sum',
        'summary_ko': '$a_n = a_{n+6} = a_{n+9}$에서 주기 $3$ ($a_{n+3} = a_n$)을 증명하고, $a_1+a_2 = \\dfrac{7}{2}$, $a_3 = \\dfrac{1}{4}$, $a_1 a_2 = 2$로부터 한 주기 합 $\\dfrac{15}{2}$ 및 최종 합 $98$ 도출하기',
        'summary_en': 'Prove period $3$ ($a_{n+3} = a_n$) for all $n \\ge 1$, deduce $a_1+a_2 = \\frac{7}{2}$, $a_3 = \\frac{1}{4}$, and $a_1 a_2 = 2$, and compute $\\sum_{k=1}^{40} \\frac{1}{a_k a_{k+1}} = 13 \\times \\frac{15}{2} + \\frac{1}{2} = 98$.',
        'tags': ['2027학년도수능', '공통(수학I·II)', '수학I', '수열', '주기수열', '로그의성질', '시그마', '22번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': '$a_{n+3} = a_{(n+3)+6} = a_{n+9} = a_n$',
                'desc': '모든 자연수 $n$에 대해 성립하는 두 주기의 차($9 - 6 = 3$)로부터 첫째항부터 바로 주기 $3$이 성립함',
                'desc_en': 'Replacing $n$ with $n+3$ in $a_n = a_{n+6}$ gives $a_{n+3} = a_{n+9} = a_n$ for every $n \\ge 1$.',
            },
            {
                'sym': '$x + y = \\dfrac{7}{2},\\; z = \\dfrac{1}{4},\\; xy = 2$',
                'desc': '$a_1=x, a_2=y, a_3=z$의 개별 값을 구하지 않고도 대칭식($x+y, xy, z$)만으로 완벽히 풀림',
                'desc_en': 'Symmetric quantities $x+y, xy, z$ determine the target sum without solving for $x, y$ individually.',
            },
            {
                'sym': '$\\dfrac{1}{xy} + \\dfrac{1}{yz} + \\dfrac{1}{zx} = \\dfrac{1}{xy} + \\dfrac{x+y}{xyz} = \\dfrac{15}{2}$',
                'desc': '주기 $3$인 분수 수열 $\\dfrac{1}{a_k a_{k+1}}$의 한 묶음($3$개 항)의 합',
                'desc_en': 'Sum of one full period of 3 consecutive terms of $\\frac{1}{a_k a_{k+1}}$.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 규칙 점프] $6$칸 뒤의 수와 $9$칸 뒤의 수가 항상 같을 때 반복 마디(주기) 찾기',
                'title_en': '🔰 Step 1 · [Elementary Pattern Jump] Finding the repeating block length from $+6$ and $+9$ jumps',
                'knowledge': '모든 자연수 $n$에서 $a_n = a_{n+6}$이므로 $n$ 대신 $n+3$을 넣으면 $a_{n+3} = a_{n+9}$입니다! 그런데 문제에서 $a_n = a_{n+9}$라고 했으므로 **$a_{n+3} = a_n$**, 즉 첫째항부터 예외 없이 **$3$칸마다 똑같은 세 수 $(a_1, a_2, a_3)$가 계속 반복**됩니다!',
                'knowledge_en': 'Substituting $n+3$ into $a_n = a_{n+6}$ gives $a_{n+3} = a_{n+9} = a_n$ for every $n \\ge 1$, meaning $(a_1, a_2, a_3)$ repeats every $3$ terms!',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '세 수 $(a_1, a_2, a_3)$이 계속 반복되는 수열($a_{n+3} = a_n$)에서 $(a_5, a_6, a_{10})$과 각각 같은 항을 순서대로 짝지은 것은?',
                        'stem_en': 'In a sequence repeating $(a_1, a_2, a_3)$ with period $3$, which terms equal $(a_5, a_6, a_{10})$?',
                        'options': [
                            '$(a_1, a_2, a_3)$',
                            '$(a_2, a_3, a_1)$',
                            '$(a_2, a_1, a_3)$',
                            '$(a_3, a_1, a_2)$',
                            '$(a_3, a_2, a_1)$',
                        ],
                        'answer': 2,
                        'exp': '$5, 6, 10$을 $3$으로 나눈 나머지를 보면 $a_5 = a_2$, $a_6 = a_3$, $a_{10} = a_1$입니다.',
                        'exp_en': 'Reducing indices modulo $3$ gives $a_5 = a_2$, $a_6 = a_3$, and $a_{10} = a_1$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [연립방정식] $x = a_1, y = a_2, z = a_3$으로 놓고 $x + y$와 $z$ 구하기',
                'title_en': '🌿 Step 2 · [Linear System] Solving for $x + y$ and $z$ from (가) and $\\sum_{k=1}^{20} a_k = 26$',
                'knowledge': '조건 (가)는 $3y + 2z + 3x = 3(x + y) + 2z = 11$입니다. 또 $20 = 3 \\times 6 + 2$이므로 $\\sum_{k=1}^{20} a_k = 6(x + y + z) + (x + y) = 7(x + y) + 6z = 26$입니다.',
                'knowledge_en': 'Condition (가) gives $3(x+y) + 2z = 11$, and since $20 = 3(6) + 2$, $\\sum_{k=1}^{20} a_k = 7(x+y) + 6z = 26$.',
                'questions': [
                    {
                        'level_label': '연립방정식 풀이 디딤돌 2',
                        'level_label_en': 'Linear System Step 2',
                        'stem': '두 식 $3(x + y) + 2z = 11$과 $7(x + y) + 6z = 26$을 연립하여 구한 $(x + y,\\; z)$의 값은?',
                        'stem_en': 'Solving $3(x+y) + 2z = 11$ and $7(x+y) + 6z = 26$, what is $(x + y,\\; z)$?',
                        'options': [
                            '$\\left(3,\\; 1\\right)$',
                            '$\\left(\\dfrac{7}{2},\\; \\dfrac{1}{4}\\right)$',
                            '$\\left(\\dfrac{7}{2},\\; \\dfrac{1}{2}\\right)$',
                            '$\\left(\\dfrac{5}{2},\\; \\dfrac{7}{4}\\right)$',
                            '$\\left(4,\\; -\\dfrac{1}{2}\\right)$',
                        ],
                        'answer': 2,
                        'exp': '첫 식에 $3$을 곱한 $9(x+y) + 6z = 33$에서 둘째 식을 빼면 $2(x+y) = 7 \\implies x+y = \\dfrac{7}{2}$이고, 대입하면 $2z = 11 - \\dfrac{21}{2} = \\dfrac{1}{2} \\implies z = \\dfrac{1}{4}$입니다.',
                        'exp_en': '$9(x+y)+6z - (7(x+y)+6z) = 33 - 26 \\implies x+y = \\frac{7}{2}$ and $z = \\frac{1}{4}$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [로그 합의 성질] $\\sum_{k=1}^{35} \\log_2 a_k = -10$에서 두 항의 곱 $xy$ 구하기',
                'title_en': '🌱 Step 3 · [Logarithmic Sum] Finding $xy$ from $\\sum_{k=1}^{35} \\log_2 a_k = -10$',
                'knowledge': '$35 = 3 \\times 11 + 2$이므로 $1$항부터 $35$항까지 $x$와 $y$는 $12$번씩, $z = \\dfrac{1}{4}$은 $11$번 등장합니다! 따라서 $12(\\log_2 x + \\log_2 y) + 11\\log_2\\left(\\dfrac{1}{4}\\right) = 12\\log_2(xy) + 11(-2) = -10$입니다.',
                'knowledge_en': 'Since $35 = 3(11) + 2$, $x$ and $y$ each appear $12$ times and $z = \\frac{1}{4}$ appears $11$ times: $12\\log_2(xy) + 11(-2) = -10$.',
                'questions': [
                    {
                        'level_label': '곱 xy 도출 디딤돌 3',
                        'level_label_en': 'Product xy Step 3',
                        'stem': '$12\\log_2(xy) - 22 = -10$을 만족시키는 $xy = a_1 a_2$의 값은?',
                        'stem_en': 'From $12\\log_2(xy) - 22 = -10$, what is the product $xy = a_1 a_2$?',
                        'options': ['$\\dfrac{1}{2}$', '$1$', '$2$', '$4$', '$8$'],
                        'answer': 3,
                        'exp': '$12\\log_2(xy) = 12 \\implies \\log_2(xy) = 1 \\implies xy = 2$입니다.',
                        'exp_en': '$\\log_2(xy) = 1 \\implies xy = 2$.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [한 주기 분수 합] $\\dfrac{1}{xy} + \\dfrac{1}{yz} + \\dfrac{1}{zx}$ 계산하기',
                'title_en': '🌳 Step 4 · [One-Period Sum] Computing $\\dfrac{1}{xy} + \\dfrac{1}{yz} + \\dfrac{1}{zx}$',
                'knowledge': '$b_k = \\dfrac{1}{a_k a_{k+1}}$이라 하면 $b_1 + b_2 + b_3 = \\dfrac{1}{xy} + \\dfrac{1}{yz} + \\dfrac{1}{zx} = \\dfrac{1}{xy} + \\dfrac{x + y}{xyz}$입니다! $xy = 2$, $z = \\dfrac{1}{4}$이므로 $xyz = \\dfrac{1}{2}$이고 $x + y = \\dfrac{7}{2}$입니다.',
                'knowledge_en': 'For one period ($k = 1, 2, 3$), $\\frac{1}{xy} + \\frac{1}{yz} + \\frac{1}{zx} = \\frac{1}{xy} + \\frac{x+y}{xyz}$ with $xy = 2$, $x+y = \\frac{7}{2}$, and $xyz = \\frac{1}{2}$.',
                'questions': [
                    {
                        'level_label': '한 주기 합 계산 디딤돌 4',
                        'level_label_en': 'One-Period Sum Step 4',
                        'stem': '$xy = 2$, $x + y = \\dfrac{7}{2}$, $xyz = \\dfrac{1}{2}$일 때, 한 주기의 합 $\\dfrac{1}{xy} + \\dfrac{x + y}{xyz}$의 값은?',
                        'stem_en': 'Given $xy = 2$, $x+y = \\frac{7}{2}$, and $xyz = \\frac{1}{2}$, what is $\\frac{1}{xy} + \\frac{x+y}{xyz}$?',
                        'options': ['$\\dfrac{11}{2}$', '$\\dfrac{13}{2}$', '$7$', '$\\dfrac{15}{2}$', '$8$'],
                        'answer': 4,
                        'exp': '$\\dfrac{1}{2} + \\dfrac{7/2}{1/2} = \\dfrac{1}{2} + 7 = \\dfrac{15}{2}$입니다.',
                        'exp_en': '$\\frac{1}{2} + 7 = \\frac{15}{2}$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 종합] $40 = 3 \\times 13 + 1$을 이용해 $\\sum_{k=1}^{40} \\dfrac{1}{a_k a_{k+1}}$ 완성하기',
                'title_en': '💎 Step 5 · [Final Synthesis] Evaluating $\\sum_{k=1}^{40} \\dfrac{1}{a_k a_{k+1}}$ using $40 = 3 \\times 13 + 1$',
                'knowledge': '$40$개의 항은 $3$개씩 $13$묶음($39$항)과 마지막 $40$번째 항 $\\dfrac{1}{a_{40} a_{41}} = \\dfrac{1}{a_1 a_2} = \\dfrac{1}{xy} = \\dfrac{1}{2}$로 이루어집니다!',
                'knowledge_en': 'Since $40 = 3 \\times 13 + 1$, there are $13$ full periods of sum $\\frac{15}{2}$ plus the $40$th term $\\frac{1}{a_1 a_2} = \\frac{1}{2}$.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': '$13 \\times \\dfrac{15}{2} + \\dfrac{1}{2}$을 계산한 $\\displaystyle\\sum_{k=1}^{40} \\frac{1}{a_k a_{k+1}}$의 최종 값은?',
                        'stem_en': 'What is the final value of $\\sum_{k=1}^{40} \\frac{1}{a_k a_{k+1}} = 13 \\times \\frac{15}{2} + \\frac{1}{2}$?',
                        'options': ['$94$', '$96$', '$98$', '$100$', '$102$'],
                        'answer': 3,
                        'exp': '$\\dfrac{195}{2} + \\dfrac{1}{2} = \\dfrac{196}{2} = 98$입니다.',
                        'exp_en': '$\\frac{195 + 1}{2} = 98$.',
                    }
                ],
            },
        ],
        'final': {
            'stem': (
                '모든 항이 양수인 수열 $\\{a_n\\}$이 있다. 모든 자연수 $n$에 대하여<br>'
                '$$a_n = a_{n+6} = a_{n+9}$$'
                '이고, 다음 조건이 성립한다.'
                '<div style="margin:10px 0;padding:12px 14px;border:1.5px solid #475569;border-radius:8px;background:#f8fafc">'
                '<div style="color:#1e293b;line-height:1.9">'
                '(가) $3a_5 + 2a_6 + 3a_{10} = 11$<br>'
                '(나) $\\displaystyle\\sum_{k=1}^{20} a_k = 26, \\quad \\sum_{k=1}^{35} \\log_2 a_k = -10$'
                '</div></div>'
                '$\\displaystyle\\sum_{k=1}^{40} \\frac{1}{a_k a_{k+1}}$ 의 값을 구하시오. [4점]'
            ),
            'stem_en': (
                'Let $\\{a_n\\}$ be a sequence of positive real numbers such that for every natural number $n$,<br>'
                '$$a_n = a_{n+6} = a_{n+9},$$'
                'and the following conditions hold:'
                '<div style="margin:10px 0;padding:12px 14px;border:1.5px solid #475569;border-radius:8px;background:#f8fafc">'
                '<div style="color:#1e293b;line-height:1.9">'
                '(가) $3a_5 + 2a_6 + 3a_{10} = 11$<br>'
                '(나) $\\displaystyle\\sum_{k=1}^{20} a_k = 26, \\quad \\sum_{k=1}^{35} \\log_2 a_k = -10$'
                '</div></div>'
                'Find the value of $\\displaystyle\\sum_{k=1}^{40} \\frac{1}{a_k a_{k+1}}$. [4 points]'
            ),
            'options': ['$94$', '$96$', '$98$', '$100$', '$102$'],
            'answer': 3,
            'exp': '$a_{n+3} = a_{n+9} = a_n$이므로 주기 $3$입니다. $a_1+a_2=\\frac{7}{2}$, $a_3=\\frac{1}{4}$, $a_1 a_2 = 2$에서 한 주기 합은 $\\frac{1}{2}+7=\\frac{15}{2}$이므로 $13\\times\\frac{15}{2}+\\frac{1}{2}=98$입니다.',
            'exp_en': 'Since $a_{n+3} = a_{n+9} = a_n$, the period is $3$. Solving gives $a_1+a_2 = \\frac{7}{2}$, $a_3 = \\frac{1}{4}$, and $a_1 a_2 = 2$. One period sums to $\\frac{15}{2}$, giving $13 \\times \\frac{15}{2} + \\frac{1}{2} = 98$.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 공통 영역 최고난도(22번) 문항으로, <b>두 주기 관계식 $a_n = a_{n+6} = a_{n+9}$로부터 모든 자연수 $n$에 대해 최소 주기 $3$이 성립함을 논증</b>하고, 개별 항을 무리수로 구할 필요 없이 대칭식($x+y, xy, z$)만으로 급수를 계산하는 문제입니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: 모든 자연수 $n$에 대한 주기 $3$ 증명</b><br>\n'
                '  모든 자연수 $m$에 대하여 $a_m = a_{m+6}$이므로 $m = n + 3$을 대입하면 $a_{n+3} = a_{n+9}$입니다.<br>\n'
                '  그런데 모든 자연수 $n$에 대하여 $a_{n+9} = a_n$이므로:<br>\n'
                '  $$a_{n+3} = a_n \\quad (\\text{모든 자연수 } n)$$<br>\n'
                '  <b>2단계: $a_1 = x, a_2 = y, a_3 = z$의 대칭식 결정</b><br>\n'
                '  • 조건 (가): $3a_2 + 2a_3 + 3a_1 = 3(x + y) + 2z = 11$<br>\n'
                '  • 조건 (나)의 첫 식 ($20 = 3 \\times 6 + 2$): $6(x + y + z) + (x + y) = 7(x + y) + 6z = 26$<br>\n'
                '  두 식을 연립하면 $x + y = \\dfrac{7}{2}$, $z = \\dfrac{1}{4}$입니다.<br>\n'
                '  • 조건 (나)의 둘째 식 ($35 = 3 \\times 11 + 2$):<br>\n'
                '  $$12\\log_2(xy) + 11\\log_2\\left(\\frac{1}{4}\\right) = -10 \\implies 12\\log_2(xy) - 22 = -10 \\implies xy = 2$$<br>\n'
                '  <b>3단계: $\\sum_{k=1}^{40} \\dfrac{1}{a_k a_{k+1}}$ 계산</b><br>\n'
                '  한 주기($3$개 항)의 합은 $xyz = 2 \\times \\dfrac{1}{4} = \\dfrac{1}{2}$이므로:<br>\n'
                '  $$\\frac{1}{xy} + \\frac{1}{yz} + \\frac{1}{zx} = \\frac{1}{xy} + \\frac{x + y}{xyz} = \\frac{1}{2} + \\frac{7/2}{1/2} = \\frac{15}{2}$$\n'
                '  $40 = 3 \\times 13 + 1$이므로:<br>\n'
                '  $$\\sum_{k=1}^{40} \\frac{1}{a_k a_{k+1}} = 13 \\times \\frac{15}{2} + \\frac{1}{a_1 a_2} = \\frac{195}{2} + \\frac{1}{2} = 98$$\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>(참고: $t^2 - \\frac{7}{2}t + 2 = 0$의 판별식 $D = \\frac{17}{4} > 0$이므로 양수 $x, y$가 실제로 존재합니다.) 정답은 <b>$98$</b>입니다.</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                '<p>This common-section finale (#22) combines <b>periodicity deduction ($\\gcd(6, 9) = 3$)</b> with <b>symmetric algebraic relations and logarithmic sums</b>.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Period $3$ for all $n \\ge 1$</b><br>\n'
                '  Applying $a_m = a_{m+6}$ at $m = n + 3$ gives $a_{n+3} = a_{n+9} = a_n$ for every $n \\ge 1$.<br><br>\n'
                '  <b>Step 2: Find $x+y$, $z$, and $xy$</b><br>\n'
                '  With $(a_1, a_2, a_3) = (x, y, z)$, solving $3(x+y) + 2z = 11$ and $7(x+y) + 6z = 26$ gives $x+y = \\frac{7}{2}$ and $z = \\frac{1}{4}$.<br>\n'
                '  From $12\\log_2(xy) + 11\\log_2(1/4) = -10$, we get $12\\log_2(xy) = 12 \\implies xy = 2$.<br><br>\n'
                '  <b>Step 3: Evaluate the 40-term sum</b><br>\n'
                '  One period sums to $\\frac{1}{xy} + \\frac{x+y}{xyz} = \\frac{1}{2} + \\frac{7/2}{1/2} = \\frac{15}{2}$. Since $40 = 3(13) + 1$:<br>\n'
                '  $$\\sum_{k=1}^{40} \\frac{1}{a_k a_{k+1}} = 13 \\times \\frac{15}{2} + \\frac{1}{2} = 98$$\n'
                '</p>\n\n'
                '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                '<p>The exact short-answer value is <b>$98$</b>.</p>'
            ),
        },
    },
]
