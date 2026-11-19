# -*- coding: utf-8 -*-
"""
csat2027_part4_calc.py
======================
2027학년도 대학수학능력시험 수학 영역 선택과목 미적분 23~30번 (8문항: csat27_m23 ~ csat27_m30)
- 한국교육과정평가원(KICE) 홀수형 원본 문제지 13~16쪽 문장·수식·보기·도형 100% 대조 검증 완료
- 공식 정답표 검증:
  23: ① (-3) | 24: ④ (-π/4) | 25: ① (12) | 26: ⑤ (√3(3e²+1)/4)
  27: ③ (25/6) | 28: ④ ((e+1)(e-2)/(2(e-1))) | 29: 12 | 30: 75
"""

M26_ORIG_SVG = (
    '<svg viewBox="0 0 340 240" xmlns="http://www.w3.org/2000/svg" '
    'style="width:100%;max-width:340px;height:auto;display:block;margin:0 auto">'
    '<defs>'
    '<marker id="m26Arr" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse">'
    '<path d="M 0 1.5 L 8.5 5 L 0 8.5 z" fill="#111827"/>'
    '</marker>'
    '<linearGradient id="m26SideGrad" x1="0%" y1="0%" x2="100%" y2="85%">'
    '<stop offset="0%" stop-color="#e5e7eb"/>'
    '<stop offset="100%" stop-color="#cbd5e1"/>'
    '</linearGradient>'
    '<linearGradient id="m26FaceGrad" x1="15%" y1="0%" x2="85%" y2="100%">'
    '<stop offset="0%" stop-color="#d1d5db"/>'
    '<stop offset="100%" stop-color="#b6c0ce"/>'
    '</linearGradient>'
    '</defs>'
    # y-axis visible extensions (bottom-left of O and top-right emerging behind ridge)
    '<line x1="40" y1="205" x2="54" y2="194" stroke="#111827" stroke-width="1.15"/>'
    '<line x1="54" y1="194" x2="127" y2="136" stroke="#475569" stroke-width="1.05" stroke-dasharray="3.2,2.6"/>'
    '<line x1="171" y1="101" x2="216" y2="65" stroke="#111827" stroke-width="1.2" marker-end="url(#m26Arr)"/>'
    '<text x="205" y="63" fill="#111827" font-size="11.5" font-style="italic" font-family="serif">y</text>'
    # Swept front-left curved surface of the solid (0 <= x <= 2)
    '<path d="M 54 194 L 118 202 L 154 24 Q 112 108 62 162 Z" fill="url(#m26SideGrad)" stroke="none"/>'
    # Highlighted intermediate equilateral cross-section at x ≈ 0.9
    '<polygon points="83,197.6 121,167 101,116" fill="#9ca3af" fill-opacity="0.52" stroke="none"/>'
    '<line x1="83" y1="197.6" x2="121" y2="167" stroke="#374151" stroke-width="1.0" stroke-dasharray="3,2.4"/>'
    '<line x1="121" y1="167" x2="101" y2="116" stroke="#374151" stroke-width="1.05"/>'
    '<line x1="83" y1="197.6" x2="101" y2="116" stroke="#111827" stroke-width="1.2"/>'
    # Hidden base curve y = sqrt((2x+1)e^x + sin(pi x)) for 0 <= x <= 2
    '<path d="M 71 180.5 C 90 176, 104 173, 121 167 C 145 158, 168 150, 194 141" '
    'fill="none" stroke="#374151" stroke-width="1.15" stroke-dasharray="3.2,2.5"/>'
    # Initial cross-section edge at x = 0
    '<line x1="54" y1="194" x2="71" y2="180.5" stroke="#374151" stroke-width="1.0" stroke-dasharray="2.8,2.2"/>'
    '<line x1="71" y1="180.5" x2="62" y2="162" stroke="#374151" stroke-width="1.05"/>'
    '<line x1="54" y1="194" x2="62" y2="162" stroke="#111827" stroke-width="1.25"/>'
    # Right boundary equilateral triangle cross-section at x = 2
    '<polygon points="118,202 194,141 154,24" fill="url(#m26FaceGrad)" stroke="#111827" stroke-width="1.35" stroke-linejoin="round"/>'
    # Top ridge curve connecting apexes from x = 0 through intermediate slice to x = 2
    '<path d="M 62 162 Q 112 108 154 24" fill="none" stroke="#111827" stroke-width="1.35"/>'
    # Visible curve y = sqrt((2x+1)e^x + sin(pi x)) for x >= 2
    '<path d="M 194 141 C 224 126, 258 104, 294 75" fill="none" stroke="#111827" stroke-width="1.45"/>'
    # Line x = 2 extending below x-axis and beyond curve
    '<line x1="106" y1="211.5" x2="118" y2="202" stroke="#111827" stroke-width="1.15"/>'
    '<line x1="194" y1="141" x2="262" y2="86.5" stroke="#111827" stroke-width="1.15"/>'
    '<text x="108" y="222" fill="#111827" font-size="10.8" font-family="serif" text-anchor="middle">'
    '<tspan font-style="italic">x</tspan> = 2</text>'
    # x-axis along front base
    '<line x1="42" y1="192.5" x2="156" y2="206.8" stroke="#111827" stroke-width="1.25" marker-end="url(#m26Arr)"/>'
    '<text x="55" y="206" fill="#111827" font-size="11" font-family="serif">O</text>'
    '<text x="153" y="218" fill="#111827" font-size="11.5" font-style="italic" font-family="serif">x</text>'
    # Formula label with crisp radical bar pointing to the curve
    '<line x1="252" y1="108" x2="263" y2="124" stroke="#475569" stroke-width="0.9"/>'
    '<text x="216" y="137" fill="#111827" font-size="10.5" font-family="serif">'
    '<tspan font-style="italic">y</tspan> = </text>'
    '<path d="M 233 132 L 235.5 137.5 L 239.5 123.5 L 328 123.5" fill="none" stroke="#111827" stroke-width="1.05"/>'
    '<text x="241" y="137" fill="#111827" font-size="10.2" font-family="serif">'
    '(2<tspan font-style="italic">x</tspan>+1)<tspan font-style="italic">e</tspan>'
    '<tspan dy="-4.5" font-size="7.6" font-style="italic">x</tspan>'
    '<tspan dy="4.5"> + sin π</tspan><tspan font-style="italic">x</tspan></text>'
    '</svg>'
)


PART4_PROBLEMS = [
    # =========================================================================
    # 23번 (csat27_m23) — 자연로그 함수의 극한 [2점] · 공식 정답 ① (-3)
    # =========================================================================
    {
        'slug': 'csat27_m23',
        'qNum': '23',
        'points': 2,
        'is_short_answer': False,
        'official_ans_str': '',
        'subject': '미적분',
        'title': '[2027학년도 수능 고3 미적분 23번] 자연로그 함수의 극한과 치환 계수 비',
        'title_en': '[2027 CSAT Math Calculus #23] Limit of Natural Logarithm Function via Coefficient Ratio',
        'summary_ko': '자연로그의 기본 극한 $\\lim_{t \\to 0} \\dfrac{\\ln(1+t)}{t} = 1$을 이용하여 $\\lim_{x \\to 0} \\dfrac{\\ln(1-3x)}{x} = -3$ 구하기',
        'summary_en': 'Evaluate $\\lim_{x \\to 0} \\dfrac{\\ln(1-3x)}{x}$ by matching the argument $-3x$ in the denominator to obtain $-3$.',
        'tags': ['미적분', '미분법', '지수로그함수의극한', '자연로그', '2027학년도 수능', '23번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': '$\\ln(1 - 3x)$',
                'desc': '무리수 $e$를 밑으로 하는 자연로그 ($x \\to 0$일 때 진수가 $1$에 가까워져 $\\ln 1 = 0$에 수렴)',
                'desc_en': 'Natural logarithm with base $e$, approaching $\\ln 1 = 0$ as $x \\to 0$.',
            },
            {
                'sym': '$\\lim_{t \\to 0} \\dfrac{\\ln(1+t)}{t} = 1$',
                'desc': '$t$가 $0$에 한없이 가까워질 때 $\\ln(1+t)$와 $t$의 비율이 $1$이 되는 기본 극한 약속',
                'desc_en': 'Fundamental logarithmic limit near $0$: $\\ln(1+t)$ behaves like $t$ as $t \\to 0$.',
            },
            {
                'sym': '$\\dfrac{\\ln(1-3x)}{x} = \\dfrac{\\ln(1-3x)}{-3x} \\times (-3)$',
                'desc': '분모를 로그 안의 변화량 $-3x$와 똑같이 맞춰 주고 $-3$을 곱해 보정하는 식 변형',
                'desc_en': 'Algebraic adjustment matching the denominator to $-3x$ while multiplying by $-3$.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 분수 약분과 부호] $\\dfrac{-3 \\times \\square}{\\square}$에서 공통인 수 지우기',
                'title_en': '🔰 Step 1 · [Elementary Fraction Cancellation] Simplifying $\\dfrac{-3 \\times \\square}{\\square}$',
                'knowledge': '초등학교 분수의 약분 원리에 따라 분자와 분모에 똑같이 곱해진 $0$이 아닌 수($\\square = x$)는 지울 수 있습니다! $x$가 $0$에 아주 가까워질 때 $\\ln(1 - 3x)$는 $-3x$와 거의 같아지므로, 결국 $\\dfrac{-3x}{x}$를 약분하는 것과 같은 이치입니다.',
                'knowledge_en': 'By elementary fraction cancellation, a common nonzero factor $\\square = x$ cancels out. Since $\\ln(1-3x) \\approx -3x$ near $x=0$, the ratio mirrors $\\dfrac{-3x}{x}$.',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '$0$이 아닌 수 $x$에 대하여 분수 $\\dfrac{-3 \\times x}{x}$의 분자와 분모에서 $x$를 약분한 값은?',
                        'stem_en': 'For $x \\neq 0$, what remains after canceling $x$ in the fraction $\\dfrac{-3 \\times x}{x}$?',
                        'options': ['$-3$', '$-1$', '$0$', '$1$', '$3$'],
                        'answer': 1,
                        'exp': '분자와 분모의 $x$를 약분하면 앞의 계수 $-3$만 남습니다.',
                        'exp_en': 'Canceling $x$ from numerator and denominator leaves $-3$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [기호 번역 브릿지] 자연로그의 기본 극한 $\\lim_{t \\to 0} \\dfrac{\\ln(1+t)}{t}$ 확인하기',
                'title_en': '🌿 Step 2 · [Standard Limit Bridge] Verifying $\\lim_{t \\to 0} \\dfrac{\\ln(1+t)}{t}$',
                'knowledge': '자연상수 $e$와 자연로그의 정의로부터 $\\lim_{t \\to 0} \\dfrac{\\ln(1+t)}{t} = 1$입니다. 여기서 $t = -3x$라 놓으면 $x \\to 0$일 때 $t \\to 0$이므로 똑같은 공식이 적용됩니다.',
                'knowledge_en': 'By the definition of $e$, $\\lim_{t \\to 0} \\dfrac{\\ln(1+t)}{t} = 1$. Setting $t = -3x$, we have $t \\to 0$ as $x \\to 0$.',
                'questions': [
                    {
                        'level_label': '기본 공식 확인 디딤돌 2',
                        'level_label_en': 'Fundamental Limit Step 2',
                        'stem': '$t = -3x$로 치환할 때, $\\lim_{x \\to 0} \\dfrac{\\ln(1 - 3x)}{-3x} = \\lim_{t \\to 0} \\dfrac{\\ln(1+t)}{t}$의 극한값은?',
                        'stem_en': 'Letting $t = -3x$, what is the value of $\\lim_{x \\to 0} \\dfrac{\\ln(1 - 3x)}{-3x}$?',
                        'options': ['$-3$', '$-1$', '$0$', '$1$', '$3$'],
                        'answer': 4,
                        'exp': '진수의 $1$ 뒤에 더해진 식 $-3x$와 분모 $-3x$가 정확히 일치하므로 극한값은 $1$입니다.',
                        'exp_en': 'Because the denominator matches $-3x$ exactly, the limit equals $1$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [식 변형 추론] 분모를 $-3x$로 맞추고 상수 보정하기',
                'title_en': '🌱 Step 3 · [Algebraic Matching] Matching $-3x$ in the Denominator',
                'knowledge': '원래 식의 분모는 $x$이므로, 분모를 $-3x$로 바꾸면 원래 식과 똑같아지도록 분자에 $-3$을 곱해 주어야 합니다:$$\\frac{\\ln(1-3x)}{x} = \\frac{\\ln(1-3x)}{-3x} \\times (-3)$$',
                'knowledge_en': 'To keep the expression unchanged when replacing $x$ in the denominator with $-3x$, multiply by $-3$: $\\dfrac{\\ln(1-3x)}{x} = \\dfrac{\\ln(1-3x)}{-3x} \\times (-3)$.',
                'questions': [
                    {
                        'level_label': '수식 변형 추론 디딤돌 3',
                        'level_label_en': 'Algebraic Matching Step 3',
                        'stem': '$0$이 아닌 모든 실수 $x$에 대하여 $\\dfrac{\\ln(1-3x)}{x} = \\dfrac{\\ln(1-3x)}{-3x} \\times [\\;\\text{(가)}\\;]$가 성립할 때, 빈칸 (가)에 알맞은 상수는?',
                        'stem_en': 'For $\\dfrac{\\ln(1-3x)}{x} = \\dfrac{\\ln(1-3x)}{-3x} \\times [\\;\\text{(가)}\\;]$ to hold for $x \\neq 0$, what constant goes in (가)?',
                        'options': ['$-3$', '$-\\dfrac{1}{3}$', '$\\dfrac{1}{3}$', '$1$', '$3$'],
                        'answer': 1,
                        'exp': '$\\dfrac{1}{-3x} \\times (-3) = \\dfrac{1}{x}$이므로 빈칸 (가)에 알맞은 상수는 $-3$입니다.',
                        'exp_en': 'Since $\\dfrac{-3}{-3x} = \\dfrac{1}{x}$, the required constant is $-3$.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [극한의 곱셈 성질] 수렴하는 두 값 곱하기',
                'title_en': '🌳 Step 4 · [Limit Product Law] Multiplying Convergent Factors',
                'knowledge': '극한의 성질에 의하여 수렴하는 함수와 상수의 곱의 극한은 각각의 극한값의 곱과 같습니다: $1 \\times (-3) = -3$.',
                'knowledge_en': 'By the constant multiple rule for limits, the limit is the product $1 \\times (-3) = -3$.',
                'questions': [
                    {
                        'level_label': '극한 곱셈 계산 디딤돌 4',
                        'level_label_en': 'Limit Multiplication Step 4',
                        'stem': '$\\lim_{x \\to 0} \\dfrac{\\ln(1-3x)}{-3x} = 1$일 때, $\\lim_{x \\to 0} \\left\\{\\dfrac{\\ln(1-3x)}{-3x} \\times (-3)\\right\\}$를 계산한 값은?',
                        'stem_en': 'Given $\\lim_{x \\to 0} \\dfrac{\\ln(1-3x)}{-3x} = 1$, what is $\\lim_{x \\to 0} \\left\\{\\dfrac{\\ln(1-3x)}{-3x} \\times (-3)\\right\\}$?',
                        'options': ['$-6$', '$-3$', '$0$', '$3$', '$6$'],
                        'answer': 2,
                        'exp': '$1 \\times (-3) = -3$입니다.',
                        'exp_en': '$1 \\times (-3) = -3$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 레고 조립] 본문항의 극한값 확정하기',
                'title_en': '💎 Step 5 · [Final Synthesis] Confirming the Official Answer',
                'knowledge': '따라서 구하는 극한값은 $-3$이며, 일반 공식 $\\lim_{x \\to 0} \\dfrac{\\ln(1+ax)}{bx} = \\dfrac{a}{b}$에 $a = -3, b = 1$을 대입한 결과와도 일치합니다.',
                'knowledge_en': 'Thus the limit is $-3$, matching $\\lim_{x \\to 0} \\dfrac{\\ln(1+ax)}{bx} = \\dfrac{a}{b}$ with $a=-3, b=1$.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': '$\\lim_{x \\to 0} \\dfrac{\\ln(1-3x)}{x}$의 값은?',
                        'stem_en': 'What is the value of $\\lim_{x \\to 0} \\dfrac{\\ln(1-3x)}{x}$?',
                        'options': ['$-3$', '$-1$', '$0$', '$1$', '$3$'],
                        'answer': 1,
                        'exp': '$\\lim_{x \\to 0} \\dfrac{\\ln(1-3x)}{-3x} \\times (-3) = 1 \\times (-3) = -3$이므로 정답은 ①입니다.',
                        'exp_en': 'The limit evaluates to $-3$ (choice ①).',
                    }
                ],
            },
        ],
        'final': {
            'stem': '$\\lim_{x \\to 0} \\dfrac{\\ln(1-3x)}{x}$의 값은? [2점]',
            'stem_en': 'What is the value of $\\lim_{x \\to 0} \\dfrac{\\ln(1-3x)}{x}$? [2 points]',
            'options': ['$-3$', '$-1$', '$0$', '$1$', '$3$'],
            'answer': 1,
            'exp': '$\\lim_{x \\to 0} \\dfrac{\\ln(1-3x)}{x} = \\lim_{x \\to 0} \\left\\{\\dfrac{\\ln(1-3x)}{-3x} \\times (-3)\\right\\} = 1 \\times (-3) = -3$이므로 정답은 ①입니다.',
            'exp_en': '$\\lim_{x \\to 0} \\dfrac{\\ln(1-3x)}{x} = \\lim_{x \\to 0} \\dfrac{\\ln(1-3x)}{-3x} \\times (-3) = -3$. Correct answer: ①.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 <b>자연로그 함수의 기본 극한 $\\lim_{t \\to 0} \\dfrac{\\ln(1+t)}{t} = 1$</b>을 활용하여 부정형($\\dfrac{0}{0}$ 꼴) 극한값을 정확히 계산하는지를 평가하는 문항입니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  진수 $1 - 3x = 1 + (-3x)$에 맞추어 분모를 $-3x$로 변형한 뒤 $-3$을 곱하면 다음과 같습니다.<br>\n'
                '  $$\\lim_{x \\to 0} \\frac{\\ln(1-3x)}{x} = \\lim_{x \\to 0} \\left\\{\\frac{\\ln(1-3x)}{-3x} \\times (-3)\\right\\}$$\n'
                '  여기서 $t = -3x$라 놓으면 $x \\to 0$일 때 $t \\to 0$이므로 $\\lim_{t \\to 0} \\dfrac{\\ln(1+t)}{t} = 1$에 의하여\n'
                '  $$\\lim_{x \\to 0} \\frac{\\ln(1-3x)}{x} = 1 \\times (-3) = -3$$\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>\n'
                '  부호 실수($+3$과 $-3$ 혼동)만 주의하면 즉시 도출할 수 있으며, 구하는 값은 <b>$-3$ (정답 ①번)</b>입니다.\n'
                '</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis &amp; Core Concepts]</h4>\n'
                '<p>This item tests the fundamental logarithmic limit $\\lim_{t \\to 0} \\dfrac{\\ln(1+t)}{t} = 1$ on a $\\dfrac{0}{0}$ indeterminate form.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  Matching the term $-3x$ inside $\\ln(1 + (-3x))$ with the denominator gives:\n'
                '  $$\\lim_{x \\to 0} \\frac{\\ln(1-3x)}{x} = (-3) \\lim_{x \\to 0} \\frac{\\ln(1-3x)}{-3x} = (-3) \\times 1 = -3.$$\n'
                '</p>\n\n'
                '<h4>✨ [Final Answer &amp; Practical Tips]</h4>\n'
                '<p>\n'
                '  Pay attention to the negative sign on $-3x$. Therefore, the correct answer is <b>choice ① ($-3$)</b>.\n'
                '</p>'
            ),
        },
    },

    # =========================================================================
    # 24번 (csat27_m24) — 부분적분법 정적분 [3점] · 공식 정답 ④ (-π/4)
    # =========================================================================
    {
        'slug': 'csat27_m24',
        'qNum': '24',
        'points': 3,
        'is_short_answer': False,
        'official_ans_str': '',
        'subject': '미적분',
        'title': '[2027학년도 수능 고3 미적분 24번] 다항함수와 삼각함수의 곱의 부분적분법',
        'title_en': '[2027 CSAT Math Calculus #24] Integration by Parts for Product of Polynomial and Sine',
        'summary_ko': '부분적분법으로 $\\displaystyle\\int_0^{\\pi} x \\sin 4x \\, dx = \\left[-\\dfrac{x\\cos 4x}{4}\\right]_0^{\\pi} + \\dfrac{1}{4}\\int_0^{\\pi} \\cos 4x \\, dx = -\\dfrac{\\pi}{4}$ 구하기',
        'summary_en': 'Apply integration by parts with $u=x$ and $v\'=\\sin 4x$ over $[0, \\pi]$ to evaluate $\\displaystyle\\int_0^{\\pi} x \\sin 4x \\, dx = -\\dfrac{\\pi}{4}$.',
        'tags': ['미적분', '적분법', '부분적분법', '삼각함수의정적분', '2027학년도 수능', '24번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': '$\\displaystyle\\int_0^{\\pi} x \\sin 4x \\, dx$',
                'desc': '다항함수 $x$와 삼각함수 $\\sin 4x$의 곱을 구간 $[0, \\pi]$에서 정적분한 값',
                'desc_en': 'Definite integral of the product $x \\sin 4x$ over $[0, \\pi]$.',
            },
            {
                'sym': "$\\displaystyle\\int_a^b u v' dx = \\left[uv\\right]_a^b - \\int_a^b u' v dx$",
                'desc': '미분하면 간단해지는 함수($u=x$)와 적분하기 쉬운 함수($v\'=\\sin 4x$)로 나누는 정적분의 부분적분법',
                'desc_en': 'Definite integration by parts formula reducing $u=x$ to $u\'=1$.',
            },
            {
                'sym': '$\\left(-\\dfrac{1}{4}\\cos 4x\\right)\' = \\sin 4x$',
                'desc': '코사인을 미분하면 $-\\sin$이 되고 속미분 $4$가 나오므로 $-\\dfrac{1}{4}$을 곱해 만든 $\\sin 4x$의 한 부정적분',
                'desc_en': 'Antiderivative of $\\sin 4x$ accounting for the sign flip and inner factor $4$.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 분수 곱셈과 덧셈] $\\pi \\times \\left(-\\dfrac{1}{4}\\right) + 0$ 계산하기',
                'title_en': '🔰 Step 1 · [Elementary Fraction Arithmetic] Computing $\\pi \\times \\left(-\\dfrac{1}{4}\\right) + 0$',
                'knowledge': '부분적분법으로 식을 쪼개면 앞부분에서 $\\pi \\times \\left(-\\dfrac{1}{4}\\right)$, 뒷부분에서 $0$이 나옵니다! 먼저 초등 분수와 음수 곱셈 규칙으로 두 값을 더한 결과를 확인해 봅시다.',
                'knowledge_en': 'Splitting the integral yields $\\pi \\times \\left(-\\dfrac{1}{4}\\right)$ from the boundary term and $0$ from the remaining integral.',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '양수 $\\pi$와 음의 분수 $-\\dfrac{1}{4}$을 곱한 뒤 $0$을 더한 $\\pi \\times \\left(-\\dfrac{1}{4}\\right) + 0$의 값은?',
                        'stem_en': 'What is the value of $\\pi \\times \\left(-\\dfrac{1}{4}\\right) + 0$?',
                        'options': ['$-\\pi$', '$-\\dfrac{3\\pi}{4}$', '$-\\dfrac{\\pi}{2}$', '$-\\dfrac{\\pi}{4}$', '$0$'],
                        'answer': 4,
                        'exp': '$\\pi \\times \\left(-\\dfrac{1}{4}\\right) + 0 = -\\dfrac{\\pi}{4}$입니다.',
                        'exp_en': 'The expression simplifies directly to $-\\dfrac{\\pi}{4}$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [삼각함수 부정적분] $\\sin 4x$를 적분한 함수 $v(x)$ 구하기',
                'title_en': '🌿 Step 2 · [Trigonometric Antiderivative] Finding $v(x)$ with $v\'(x) = \\sin 4x$',
                'knowledge': '$(\\cos 4x)\' = -4\\sin 4x$이므로, 양변을 $-4$로 나누면 $\\left(-\\dfrac{1}{4}\\cos 4x\\right)\' = \\sin 4x$입니다!',
                'knowledge_en': 'Since $(\\cos 4x)\' = -4\\sin 4x$, dividing by $-4$ gives $\\left(-\\dfrac{1}{4}\\cos 4x\\right)\' = \\sin 4x$.',
                'questions': [
                    {
                        'level_label': '삼각함수 적분 디딤돌 2',
                        'level_label_en': 'Trig Antiderivative Step 2',
                        'stem': '미분했을 때 $\\sin 4x$가 되는 함수 $v(x)$ (단, 적분상수는 $0$)로 옳은 것은?',
                        'stem_en': 'Which function $v(x)$ satisfies $v\'(x) = \\sin 4x$?',
                        'options': [
                            '$\\dfrac{1}{4}\\cos 4x$',
                            '$-\\dfrac{1}{4}\\cos 4x$',
                            '$4\\cos 4x$',
                            '$-4\\cos 4x$',
                            '$-\\dfrac{1}{4}\\sin 4x$',
                        ],
                        'answer': 2,
                        'exp': '$\\left(-\\dfrac{1}{4}\\cos 4x\\right)\' = -\\dfrac{1}{4}(-4\\sin 4x) = \\sin 4x$이므로 $v(x) = -\\dfrac{1}{4}\\cos 4x$입니다.',
                        'exp_en': 'Differentiating $-\\dfrac{1}{4}\\cos 4x$ yields $\\sin 4x$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [부분적분법 전개] $u(x) = x$, $v\'(x) = \\sin 4x$ 대입하기',
                'title_en': '🌱 Step 3 · [Applying Integration by Parts] Setting $u(x) = x$ and $v\'(x) = \\sin 4x$',
                'knowledge': '$u(x) = x \\implies u\'(x) = 1$이고 $v(x) = -\\dfrac{1}{4}\\cos 4x$이므로, 부분적분 공식 $\\left[uv\\right]_0^{\\pi} - \\displaystyle\\int_0^{\\pi} u\'v \\, dx$에 대입하면 마이너스 두 개가 만나 뒷부분이 플러스($+$)로 바뀝니다.',
                'knowledge_en': 'With $u(x)=x$, $u\'(x)=1$, and $v(x)=-\\dfrac{1}{4}\\cos 4x$, $\\left[uv\\right]_0^{\\pi} - \\int_0^{\\pi} u\'v \\, dx$ becomes $\\left[-\\dfrac{x\\cos 4x}{4}\\right]_0^{\\pi} + \\dfrac{1}{4}\\int_0^{\\pi} \\cos 4x \\, dx$.',
                'questions': [
                    {
                        'level_label': '부분적분 전개 디딤돌 3',
                        'level_label_en': 'Integration by Parts Step 3',
                        'stem': '$\\displaystyle\\int_0^{\\pi} x \\sin 4x \\, dx = \\Bigl[\\;\\text{(가)}\\;\\Bigr]_0^{\\pi} + \\dfrac{1}{4}\\int_0^{\\pi} \\cos 4x \\, dx$가 성립할 때, 빈칸 (가)에 알맞은 식은?',
                        'stem_en': 'In $\\displaystyle\\int_0^{\\pi} x \\sin 4x \\, dx = \\Bigl[\\;\\text{(가)}\\;\\Bigr]_0^{\\pi} + \\dfrac{1}{4}\\int_0^{\\pi} \\cos 4x \\, dx$, what expression belongs in (가)?',
                        'options': [
                            '$x\\cos 4x$',
                            '$-x\\cos 4x$',
                            '$\\dfrac{x\\cos 4x}{4}$',
                            '$-\\dfrac{x\\cos 4x}{4}$',
                            '$-\\dfrac{x\\sin 4x}{4}$',
                        ],
                        'answer': 4,
                        'exp': '$u(x)v(x) = x \\cdot \\left(-\\dfrac{1}{4}\\cos 4x\\right) = -\\dfrac{x\\cos 4x}{4}$입니다.',
                        'exp_en': 'The product $u(x)v(x)$ is $-\\dfrac{x\\cos 4x}{4}$.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [주기 정적분 확인] 뒷부분 $\\dfrac{1}{4}\\displaystyle\\int_0^{\\pi} \\cos 4x \\, dx$ 계산하기',
                'title_en': '🌳 Step 4 · [Full-Period Integral] Evaluating $\\dfrac{1}{4}\\displaystyle\\int_0^{\\pi} \\cos 4x \\, dx$',
                'knowledge': '앞부분은 $\\cos 4\\pi = 1$이므로 $\\left[-\\dfrac{x\\cos 4x}{4}\\right]_0^{\\pi} = -\\dfrac{\\pi}{4} - 0 = -\\dfrac{\\pi}{4}$입니다. 한편 $\\cos 4x$의 주기는 $\\dfrac{2\\pi}{4} = \\dfrac{\\pi}{2}$이므로 구간 $[0, \\pi]$는 정확히 두 주기이며, $\\left[\\dfrac{\\sin 4x}{16}\\right]_0^{\\pi} = 0$이 됩니다!',
                'knowledge_en': 'The boundary term equals $-\\dfrac{\\pi \\cos 4\\pi}{4} - 0 = -\\dfrac{\\pi}{4}$, while $[0, \\pi]$ spans two full periods of $\\cos 4x$, giving $\\left[\\dfrac{\\sin 4x}{16}\\right]_0^{\\pi} = 0$.',
                'questions': [
                    {
                        'level_label': '나머지 정적분 디딤돌 4',
                        'level_label_en': 'Remaining Integral Step 4',
                        'stem': '$\\sin 4\\pi = 0$, $\\sin 0 = 0$임을 이용할 때, 뒷부분 $\\dfrac{1}{4}\\displaystyle\\int_0^{\\pi} \\cos 4x \\, dx = \\left[\\dfrac{\\sin 4x}{16}\\right]_0^{\\pi}$의 값은?',
                        'stem_en': 'Using $\\sin 4\\pi = 0$ and $\\sin 0 = 0$, what is $\\dfrac{1}{4}\\displaystyle\\int_0^{\\pi} \\cos 4x \\, dx = \\left[\\dfrac{\\sin 4x}{16}\\right]_0^{\\pi}$?',
                        'options': ['$-\\dfrac{\\pi}{2}$', '$-\\dfrac{\\pi}{4}$', '$0$', '$\\dfrac{\\pi}{4}$', '$\\dfrac{\\pi}{2}$'],
                        'answer': 3,
                        'exp': '$\\dfrac{\\sin 4\\pi}{16} - \\dfrac{\\sin 0}{16} = 0 - 0 = 0$입니다.',
                        'exp_en': 'Both endpoints evaluate to $0$, so the integral is $0$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 레고 조립] 두 항을 합쳐 정적분 확정하기',
                'title_en': '💎 Step 5 · [Final Synthesis] Combining Both Parts',
                'knowledge': '앞부분 $-\\dfrac{\\pi}{4}$와 뒷부분 $0$을 더하면 최종 정적분 값 $-\\dfrac{\\pi}{4}$가 완성됩니다.',
                'knowledge_en': 'Adding $-\\dfrac{\\pi}{4}$ and $0$ gives the exact integral $-\\dfrac{\\pi}{4}$.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': '$\\displaystyle\\int_0^{\\pi} x \\sin 4x \\, dx$의 값은?',
                        'stem_en': 'What is the value of $\\displaystyle\\int_0^{\\pi} x \\sin 4x \\, dx$?',
                        'options': ['$-\\pi$', '$-\\dfrac{3\\pi}{4}$', '$-\\dfrac{\\pi}{2}$', '$-\\dfrac{\\pi}{4}$', '$0$'],
                        'answer': 4,
                        'exp': '$\\left[-\\dfrac{x\\cos 4x}{4}\\right]_0^{\\pi} + \\left[\\dfrac{\\sin 4x}{16}\\right]_0^{\\pi} = -\\dfrac{\\pi}{4} + 0 = -\\dfrac{\\pi}{4}$이므로 정답은 ④입니다.',
                        'exp_en': '$-\\dfrac{\\pi}{4} + 0 = -\\dfrac{\\pi}{4}$ (choice ④).',
                    }
                ],
            },
        ],
        'final': {
            'stem': '$\\displaystyle\\int_0^{\\pi} x \\sin 4x \\, dx$의 값은? [3점]',
            'stem_en': 'What is the value of $\\displaystyle\\int_0^{\\pi} x \\sin 4x \\, dx$? [3 points]',
            'options': ['$-\\pi$', '$-\\dfrac{3\\pi}{4}$', '$-\\dfrac{\\pi}{2}$', '$-\\dfrac{\\pi}{4}$', '$0$'],
            'answer': 4,
            'exp': '부분적분법에 의하여 $\\displaystyle\\int_0^{\\pi} x \\sin 4x \\, dx = \\left[-\\dfrac{x\\cos 4x}{4}\\right]_0^{\\pi} + \\int_0^{\\pi} \\dfrac{\\cos 4x}{4} \\, dx = -\\dfrac{\\pi}{4} + \\left[\\dfrac{\\sin 4x}{16}\\right]_0^{\\pi} = -\\dfrac{\\pi}{4}$이므로 정답은 ④입니다.',
            'exp_en': 'By integration by parts, $\\left[-\\dfrac{x\\cos 4x}{4}\\right]_0^{\\pi} + \\left[\\dfrac{\\sin 4x}{16}\\right]_0^{\\pi} = -\\dfrac{\\pi}{4}$. Correct answer: ④.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 다항함수 $x$와 삼각함수 $\\sin 4x$가 곱해진 피적분함수에 <b>정적분의 부분적분법</b>을 적용하여 계산하는 문항입니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                "  $u(x) = x$, $v'(x) = \\sin 4x$로 놓으면 $u'(x) = 1$, $v(x) = -\\dfrac{1}{4}\\cos 4x$이므로 부분적분법에 의하여\n"
                '  $$\\begin{aligned}\n'
                '  \\int_0^{\\pi} x \\sin 4x \\, dx &= \\left[-\\frac{x \\cos 4x}{4}\\right]_0^{\\pi} - \\int_0^{\\pi} \\left(-\\frac{\\cos 4x}{4}\\right) dx \\\\\n'
                '  &= \\left(-\\frac{\\pi \\cos 4\\pi}{4} - 0\\right) + \\left[\\frac{\\sin 4x}{16}\\right]_0^{\\pi} \\\\\n'
                '  &= -\\frac{\\pi}{4} + (0 - 0) = -\\frac{\\pi}{4}\n'
                '  \\end{aligned}$$\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>\n'
                '  $\\sin 4x$를 적분할 때의 음수 부호($-$)와 속미분 역수 $\\dfrac{1}{4}$만 정확히 챙기면 됩니다. 구하는 값은 <b>$-\\dfrac{\\pi}{4}$ (정답 ④번)</b>입니다.\n'
                '</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis &amp; Core Concepts]</h4>\n'
                '<p>This problem applies <b>integration by parts</b> to the product of a linear polynomial $x$ and a trigonometric function $\\sin 4x$.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                "  Let $u(x) = x$ and $v'(x) = \\sin 4x$, so $u'(x) = 1$ and $v(x) = -\\dfrac{1}{4}\\cos 4x$. Integrating by parts over $[0, \\pi]$ gives:\n"
                '  $$\\int_0^{\\pi} x \\sin 4x \\, dx = \\left[-\\frac{x\\cos 4x}{4}\\right]_0^{\\pi} + \\frac{1}{4}\\int_0^{\\pi} \\cos 4x \\, dx = -\\frac{\\pi}{4} + \\left[\\frac{\\sin 4x}{16}\\right]_0^{\\pi} = -\\frac{\\pi}{4}.$$\n'
                '</p>\n\n'
                '<h4>✨ [Final Answer &amp; Practical Tips]</h4>\n'
                '<p>\n'
                '  Since $[0, \\pi]$ covers two full periods of $\\cos 4x$, the remaining integral vanishes cleanly. The correct answer is <b>choice ④ ($-\\dfrac{\\pi}{4}$)</b>.\n'
                '</p>'
            ),
        },
    },

    # =========================================================================
    # 25번 (csat27_m25) — 등비수열의 극한 [3점] · 공식 정답 ① (12)
    # =========================================================================
    {
        'slug': 'csat27_m25',
        'qNum': '25',
        'points': 3,
        'is_short_answer': False,
        'official_ans_str': '',
        'subject': '미적분',
        'title': '[2027학년도 수능 고3 미적분 25번] 등비수열의 극한의 수렴 조건과 공비의 제곱 추론',
        'title_en': '[2027 CSAT Math Calculus #25] Convergence of Geometric Sequence Limit and Common Ratio Squared',
        'summary_ko': '$a_{2n} = a_2 (r^2)^{n-1}$에서 분모 $3 \\times 4^{n-1}$과 밑을 비교하여 $r^2 = 4$, $a_2 = 3$을 구하고 $a_4 = a_2 r^2 = 12$ 도출하기',
        'summary_en': 'Rewrite $a_{2n} = a_2 (r^2)^{n-1}$ and compare bases with $4^{n-1}$ to deduce $r^2 = 4$ and $a_2 = 3$, yielding $a_4 = a_2 r^2 = 12$.',
        'tags': ['미적분', '수열의극한', '등비수열의극한', '수렴조건', '2027학년도 수능', '25번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': '$a_n = a_1 r^{n-1},\\quad a_2 = a_1 r$',
                'desc': '첫째항이 $a_1$, 공비가 $r$인 등비수열의 일반항과 둘째항',
                'desc_en': 'General term and second term of a geometric sequence with first term $a_1$ and ratio $r$.',
            },
            {
                'sym': '$a_{2n} = a_1 r^{2n-1} = a_2 (r^2)^{n-1}$',
                'desc': '짝수 번째 항 $a_{2n}$을 둘째항 $a_2$와 밑 $r^2$의 거듭제곱으로 정리한 식',
                'desc_en': 'Even-indexed term $a_{2n}$ expressed with base $r^2$ and coefficient $a_2 = a_1 r$.',
            },
            {
                'sym': '$r^2 = 4 \\implies |r| = 2 < 4$',
                'desc': '분모의 밑 $4$와 $r^2$이 일치할 때 $\\dfrac{r^{n-1}}{4^{n-1}} \\to 0$이 되어 앞항만 남는 원리',
                'desc_en': 'When $r^2 = 4$, $|r| = 2 < 4$ ensures $a_n / 4^{n-1} \\to 0$.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 규칙 곱셈] 둘째항이 $3$이고 두 칸마다 $4$배가 될 때 넷째항 구하기',
                'title_en': '🔰 Step 1 · [Elementary Pattern Multiplication] Finding the 4th Term from the 2nd Term',
                'knowledge': '등비수열에서 한 칸 갈 때 $r$을 곱하면, 두 칸 건너뛸 때는 $r \\times r = r^2$을 곱합니다! 둘째항 $a_2 = 3$에서 두 칸 건너뛰어 $4$배가 되는 넷째항 $a_4$를 먼저 초등 곱셈으로 구해 봅시다.',
                'knowledge_en': 'Jumping two steps in a geometric sequence multiplies by $r^2$. Starting from $a_2 = 3$ and multiplying by $r^2 = 4$ gives $a_4$.',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '둘째항이 $3$인 수열에서 두 칸 뒤로 갈 때 $4$를 곱한다면, 넷째항 $3 \\times 4$의 값은?',
                        'stem_en': 'If the 2nd term is $3$ and jumping two steps multiplies by $4$, what is the 4th term $3 \\times 4$?',
                        'options': ['$12$', '$14$', '$16$', '$18$', '$20$'],
                        'answer': 1,
                        'exp': '$3 \\times 4 = 12$입니다.',
                        'exp_en': '$3 \\times 4 = 12$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [지수법칙 정리] $a_{2n}$을 $(r^2)^{n-1}$ 꼴로 나타내기',
                'title_en': '🌿 Step 2 · [Exponent Law] Rewriting $a_{2n}$ in Terms of $(r^2)^{n-1}$',
                'knowledge': '첫째항이 $a_1$, 공비가 $r$인 등비수열에서 $2n - 1 = 1 + 2(n - 1)$이므로$$a_{2n} = a_1 r^{2n-1} = (a_1 r) \\cdot r^{2(n-1)} = a_2 (r^2)^{n-1}$$로 깔끔하게 바꿀 수 있습니다.',
                'knowledge_en': 'Using $2n - 1 = 1 + 2(n - 1)$, we rewrite $a_{2n} = a_1 r^{2n-1} = (a_1 r)(r^2)^{n-1} = a_2 (r^2)^{n-1}$.',
                'questions': [
                    {
                        'level_label': '짝수 항 지수 변형 디딤돌 2',
                        'level_label_en': 'Even-Term Exponent Step 2',
                        'stem': '등비수열 $a_n = a_1 r^{n-1}$ ($a_2 = a_1 r$)에서 $a_{2n}$을 분모의 $4^{n-1}$과 지수를 맞추어 $(r^2)^{n-1}$ 꼴로 바르게 나타낸 것은?',
                        'stem_en': 'How is $a_{2n}$ written with exponent $n-1$ to match $4^{n-1}$ in the denominator (where $a_2 = a_1 r$)?',
                        'options': [
                            '$a_1 (r^2)^{n-1}$',
                            '$a_2 (r^2)^{n-1}$',
                            '$a_2 r^{n-1}$',
                            '$a_1 (2r)^{n-1}$',
                            '$a_2 (r^2)^n$',
                        ],
                        'answer': 2,
                        'exp': '$a_{2n} = a_1 r \\cdot r^{2n-2} = a_2 (r^2)^{n-1}$입니다.',
                        'exp_en': '$a_{2n} = a_1 r \\cdot (r^2)^{n-1} = a_2 (r^2)^{n-1}$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [수렴 조건 추론] 분모의 밑 $4$와 분자의 최고 밑 $r^2$ 비교하기',
                'title_en': '🌱 Step 3 · [Convergence Condition] Comparing Base $r^2$ with Denominator Base $4$',
                'knowledge': '$\\lim_{n \\to \\infty} \\dfrac{a_2 (r^2)^{n-1} + a_1 r^{n-1}}{3 \\times 4^{n-1}} = 1$에서:<ul><li>$|r| < 2$ ($r^2 < 4$)이면 분자가 $4^{n-1}$보다 느리게 커져서 극한값이 $0$이 됩니다(모순).</li><li>$|r| > 2$ ($r^2 > 4$)이면 $a_2 \\neq 0$일 때 발산합니다(모순).</li><li>따라서 반드시 <b>$r^2 = 4$</b> ($r = 2$ 또는 $r = -2$)여야 합니다!</li></ul>',
                'knowledge_en': 'If $r^2 < 4$, the limit is $0$; if $r^2 > 4$ (with $a_2 \\neq 0$), the fraction diverges. For a nonzero finite limit $1$, we must have $r^2 = 4$.',
                'questions': [
                    {
                        'level_label': '공비의 제곱 도출 디딤돌 3',
                        'level_label_en': 'Common Ratio Squared Step 3',
                        'stem': '극한 $\\lim_{n \\to \\infty} \\dfrac{a_2 (r^2)^{n-1} + a_1 r^{n-1}}{3 \\times 4^{n-1}}$이 $0$이 아닌 값 $1$로 수렴하기 위한 $r^2$의 값은?',
                        'stem_en': 'For $\\lim_{n \\to \\infty} \\dfrac{a_2 (r^2)^{n-1} + a_1 r^{n-1}}{3 \\times 4^{n-1}} = 1$ to hold, what must $r^2$ equal?',
                        'options': ['$1$', '$2$', '$3$', '$4$', '$16$'],
                        'answer': 4,
                        'exp': '분모의 최고 밑이 $4$이므로 분자의 최고 밑 $r^2$도 $4$와 같아야 $0$이 아닌 상수로 수렴합니다.',
                        'exp_en': 'Matching the dominant exponential base $4$ in the denominator requires $r^2 = 4$.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [계수 비 계산] 극한값 $1$로부터 둘째항 $a_2 = a_1 r$ 구하기',
                'title_en': '🌳 Step 4 · [Leading Ratio] Finding $a_2 = a_1 r$ from the Limit Value $1$',
                'knowledge': '$r^2 = 4$이면 $|r| = 2 < 4$이므로 $\\lim_{n \\to \\infty} \\left(\\dfrac{r}{4}\\right)^{n-1} = 0$입니다. 따라서$$\\lim_{n \\to \\infty} \\frac{a_2 \\cdot 4^{n-1} + a_1 r^{n-1}}{3 \\times 4^{n-1}} = \\frac{a_2 + 0}{3} = 1 \\implies a_2 = 3$$을 얻습니다.',
                'knowledge_en': 'Since $|r| = 2 < 4$, $(r/4)^{n-1} \\to 0$, reducing the limit to $\\dfrac{a_2}{3} = 1 \\implies a_2 = 3$.',
                'questions': [
                    {
                        'level_label': '둘째항 도출 디딤돌 4',
                        'level_label_en': 'Second Term Step 4',
                        'stem': '$r^2 = 4$를 대입하여 얻은 극한식 $\\dfrac{a_2}{3} = 1$에서 둘째항 $a_2 = a_1 r$의 값은?',
                        'stem_en': 'From $\\dfrac{a_2}{3} = 1$, what is the value of the second term $a_2 = a_1 r$?',
                        'options': ['$1$', '$2$', '$3$', '$4$', '$6$'],
                        'answer': 3,
                        'exp': '$\\dfrac{a_2}{3} = 1$의 양변에 $3$을 곱하면 $a_2 = 3$입니다.',
                        'exp_en': 'Multiplying both sides by $3$ gives $a_2 = 3$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 레고 조립] $a_4 = a_2 \\times r^2$ 확정하기',
                'title_en': '💎 Step 5 · [Final Synthesis] Computing $a_4 = a_2 r^2$',
                'knowledge': '$r = 2$이든 $r = -2$이든 관계없이 $a_2 = a_1 r = 3$이고 $r^2 = 4$이므로, 구하는 넷째항은 $a_4 = a_1 r^3 = (a_1 r) \\cdot r^2 = 3 \\times 4 = 12$로 유일하게 결정됩니다!',
                'knowledge_en': 'Regardless of whether $r = 2$ or $r = -2$, $a_4 = a_1 r^3 = (a_1 r)r^2 = 3 \\times 4 = 12$ uniquely.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': '$a_1 r = 3$이고 $r^2 = 4$일 때, 등비수열 $\\{a_n\\}$의 넷째항 $a_4 = a_1 r^3$의 값은?',
                        'stem_en': 'Given $a_1 r = 3$ and $r^2 = 4$, what is the fourth term $a_4 = a_1 r^3$?',
                        'options': ['$12$', '$14$', '$16$', '$18$', '$20$'],
                        'answer': 1,
                        'exp': '$a_4 = (a_1 r) \\times r^2 = 3 \\times 4 = 12$이므로 정답은 ①입니다.',
                        'exp_en': '$a_4 = 3 \\times 4 = 12$ (choice ①).',
                    }
                ],
            },
        ],
        'final': {
            'stem': '등비수열 $\\{a_n\\}$에 대하여 $\\lim_{n \\to \\infty} \\dfrac{a_{2n}+a_n}{3 \\times 4^{n-1}} = 1$일 때, $a_4$의 값은? [3점]',
            'stem_en': 'For a geometric sequence $\\{a_n\\}$, if $\\lim_{n \\to \\infty} \\dfrac{a_{2n}+a_n}{3 \\times 4^{n-1}} = 1$, what is the value of $a_4$? [3 points]',
            'options': ['$12$', '$14$', '$16$', '$18$', '$20$'],
            'answer': 1,
            'exp': '$a_n = a_1 r^{n-1}$이라 하면 $a_{2n} = a_1 r (r^2)^{n-1}$이므로 극한이 $1$로 수렴하려면 $r^2 = 4$ ($|r|=2<4$)이고 $\\dfrac{a_1 r}{3} = 1 \\implies a_1 r = 3$입니다. 따라서 $a_4 = (a_1 r)r^2 = 3 \\times 4 = 12$이므로 정답은 ①입니다.',
            'exp_en': 'Writing $a_n = a_1 r^{n-1}$ gives $a_{2n} = (a_1 r)(r^2)^{n-1}$. Convergence to $1$ forces $r^2 = 4$ and $\\dfrac{a_1 r}{3} = 1 \\implies a_1 r = 3$, so $a_4 = (a_1 r)r^2 = 12$. Correct answer: ①.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 <b>등비수열의 극한의 수렴 조건</b>을 이용하여 짝수 항 $a_{2n}$의 밑 $r^2$과 계수 $a_1 r$을 결정하는 문항입니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  등비수열 $\\{a_n\\}$의 첫째항을 $a_1$, 공비를 $r$이라 하면 $a_n = a_1 r^{n-1}$ ($a_1 \\neq 0, r \\neq 0$)이고,\n'
                '  $$a_{2n} = a_1 r^{2n-1} = (a_1 r)(r^2)^{n-1}$$\n'
                '  입니다. 주어진 극한식에 대입하면\n'
                '  $$\\lim_{n \\to \\infty} \\frac{(a_1 r)(r^2)^{n-1} + a_1 r^{n-1}}{3 \\times 4^{n-1}} = 1$$\n'
                '  입니다.<br>\n'
                '  • $|r| < 2$ ($r^2 < 4$)이면 극한값이 $0$이 되어 모순이고, $|r| > 2$ ($r^2 > 4$)이면 $r^2 > |r| > 4$이므로 발산하여 모순입니다.<br>\n'
                '  • 따라서 <b>$r^2 = 4$</b> ($r = \\pm 2$)이며, 이때 $|r| = 2 < 4$이므로 $\\lim_{n \\to \\infty} \\dfrac{a_1 r^{n-1}}{3 \\times 4^{n-1}} = 0$입니다.<br>\n'
                '  • 그러므로 $\\dfrac{a_1 r}{3} = 1 \\implies a_1 r = 3$이고, 구하는 넷째항은\n'
                '  $$a_4 = a_1 r^3 = (a_1 r) \\cdot r^2 = 3 \\times 4 = 12$$\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>\n'
                '  공비 $r$이 $+2$이든 $-2$이든 $a_2 = a_1 r = 3$과 $r^2 = 4$가 불변이므로 $a_4$는 하나로 결정됩니다. 정답은 <b>$12$ (①번)</b>입니다.\n'
                '</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis &amp; Core Concepts]</h4>\n'
                '<p>This problem uses the <b>convergence of exponential sequences</b> to determine the common ratio squared $r^2$ and second term $a_2 = a_1 r$.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  Let $a_n = a_1 r^{n-1}$. Then $a_{2n} = a_1 r^{2n-1} = (a_1 r)(r^2)^{n-1}$, so\n'
                '  $$\\lim_{n \\to \\infty} \\frac{(a_1 r)(r^2)^{n-1} + a_1 r^{n-1}}{3 \\times 4^{n-1}} = 1.$$\n'
                '  If $|r| < 2$, the limit is $0$; if $|r| > 2$, the numerator dominates $4^{n-1}$ and diverges. Thus $r^2 = 4$ ($r = \\pm 2$). Since $|r| = 2 < 4$, $(r/4)^{n-1} \\to 0$, giving $\\dfrac{a_1 r}{3} = 1 \\implies a_1 r = 3$. Hence:\n'
                '  $$a_4 = a_1 r^3 = (a_1 r)r^2 = 3 \\times 4 = 12.$$\n'
                '</p>\n\n'
                '<h4>✨ [Final Answer &amp; Practical Tips]</h4>\n'
                '<p>\n'
                '  Even though $r = \\pm 2$ has two signs, $a_4 = a_2 r^2$ depends only on $r^2 = 4$. The correct answer is <b>choice ① ($12$)</b>.\n'
                '</p>'
            ),
        },
    },

    # =========================================================================
    # 26번 (csat27_m26) — 입체도형의 부피 [3점] · 공식 정답 ⑤ (√3(3e²+1)/4)
    # =========================================================================
    {
        'slug': 'csat27_m26',
        'qNum': '26',
        'points': 3,
        'is_short_answer': False,
        'official_ans_str': '',
        'subject': '미적분',
        'title': '[2027학년도 수능 고3 미적분 26번] 정삼각형 단면을 갖는 입체도형의 정적분 부피',
        'title_en': '[2027 CSAT Math Calculus #26] Volume of a Solid with Equilateral Triangle Cross-Sections',
        'summary_ko': '단면인 정삼각형의 넓이 $S(x) = \\dfrac{\\sqrt{3}}{4}\\{(2x+1)e^x + \\sin\\pi x\\}$를 $[0, 2]$에서 정적분하여 $\\dfrac{\\sqrt{3}(3e^2+1)}{4}$ 구하기',
        'summary_en': 'Integrate the equilateral cross-sectional area $S(x) = \\dfrac{\\sqrt{3}}{4}\\{(2x+1)e^x + \\sin\\pi x\\}$ over $[0, 2]$ to obtain $\\dfrac{\\sqrt{3}(3e^2+1)}{4}$.',
        'tags': ['미적분', '적분법', '입체도형의부피', '정삼각형단면', '부분적분법', '2027학년도 수능', '26번'],
        'orig_svg': M26_ORIG_SVG,
        'symbols': [
            {
                'sym': '$S(x) = \\dfrac{\\sqrt{3}}{4} y^2$',
                'desc': '한 변의 길이가 $y$인 정삼각형 단면의 넓이 공식',
                'desc_en': 'Area of an equilateral triangle with side length $y$.',
            },
            {
                'sym': '$V = \\displaystyle\\int_0^2 S(x) \\, dx$',
                'desc': '$x = 0$부터 $x = 2$까지 단면 넓이 $S(x)$를 빈틈없이 쌓아 구하는 입체도형의 부피',
                'desc_en': 'Volume of the solid obtained by integrating cross-sectional area $S(x)$ from $0$ to $2$.',
            },
            {
                'sym': "$\\{(2x-1)e^x\\}' = (2x+1)e^x$",
                'desc': '곱의 미분법 역연산(또는 부분적분법)으로 얻는 $(2x+1)e^x$의 부정적분',
                'desc_en': 'Antiderivative identity $\\int (2x+1)e^x dx = (2x-1)e^x + C$.',
            },
            {
                'sym': '$\\displaystyle\\int_0^2 \\sin\\pi x \\, dx = 0$',
                'desc': '주기가 $2$인 $\\sin\\pi x$를 한 주기 $[0, 2]$ 동안 적분하면 양·음 넓이가 상쇄되어 $0$이 됨',
                'desc_en': 'Full-period integral of $\\sin\\pi x$ (period $2$) over $[0, 2]$ cancels to $0$.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 도형 감각과 제곱근] $\\left(\\sqrt{A}\\right)^2$에서 루트 벗기기',
                'title_en': '🔰 Step 1 · [Elementary Square Root Property] Simplifying $\\left(\\sqrt{A}\\right)^2$',
                'knowledge': '식빵 조각의 넓이를 차곡차곡 모으면 식빵 전체의 부피가 되듯이, 단면 정삼각형의 넓이를 구하려면 먼저 밑변의 길이 $y = \\sqrt{A}$를 제곱해야 합니다! 양수 $A$에 대하여 $\\sqrt{A}$를 두 번 곱하면 루트가 깔끔하게 사라집니다.',
                'knowledge_en': 'Just as stacking bread slices gives the loaf volume, finding the triangle area squares the base $y = \\sqrt{A}$, removing the radical cleanly.',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '양수 $A$에 대하여 제곱근의 정의에 따라 $\\left(\\sqrt{A}\\right)^2 = \\sqrt{A} \\times \\sqrt{A}$를 간단히 한 것은?',
                        'stem_en': 'For $A > 0$, what does $\\left(\\sqrt{A}\\right)^2 = \\sqrt{A} \\times \\sqrt{A}$ simplify to?',
                        'options': ['$\\sqrt{A}$', '$A$', '$2A$', '$A^2$', '$\\dfrac{A}{2}$'],
                        'answer': 2,
                        'exp': '제곱하여 $A$가 되는 양수가 $\\sqrt{A}$이므로 $\\left(\\sqrt{A}\\right)^2 = A$입니다.',
                        'exp_en': 'By definition of the square root, $\\left(\\sqrt{A}\\right)^2 = A$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [단면의 넓이 $S(x)$] 정삼각형 넓이 공식 $\\dfrac{\\sqrt{3}}{4}y^2$ 적용하기',
                'title_en': '🌿 Step 2 · [Cross-Sectional Area $S(x)$] Applying $\\dfrac{\\sqrt{3}}{4}y^2$',
                'knowledge': '좌표가 $x$ ($0 \\le x \\le 2$)인 지점에서 $x$축에 수직인 평면으로 자른 단면은 한 변의 길이가 $y = \\sqrt{(2x+1)e^x + \\sin\\pi x}$인 정삼각형이므로 단면의 넓이는 $S(x) = \\dfrac{\\sqrt{3}}{4}y^2$입니다.',
                'knowledge_en': 'At position $x \\in [0, 2]$, the equilateral cross-section has side length $y = \\sqrt{(2x+1)e^x + \\sin\\pi x}$ and area $S(x) = \\dfrac{\\sqrt{3}}{4}y^2$.',
                'questions': [
                    {
                        'level_label': '단면 넓이 식 디딤돌 2',
                        'level_label_en': 'Cross-Section Formula Step 2',
                        'stem': '한 변의 길이가 $y = \\sqrt{(2x+1)e^x + \\sin\\pi x}$인 정삼각형 단면의 넓이 $S(x)$를 바르게 나타낸 것은?',
                        'stem_en': 'What is the area $S(x)$ of the equilateral triangle cross-section with side $y = \\sqrt{(2x+1)e^x + \\sin\\pi x}$?',
                        'options': [
                            '$\\dfrac{1}{2}\\{(2x+1)e^x + \\sin\\pi x\\}$',
                            '$\\dfrac{\\sqrt{3}}{2}\\{(2x+1)e^x + \\sin\\pi x\\}$',
                            '$\\dfrac{\\sqrt{3}}{4}\\{(2x+1)e^x + \\sin\\pi x\\}$',
                            '$\\dfrac{\\sqrt{3}}{8}\\{(2x+1)e^x + \\sin\\pi x\\}$',
                            '$\\sqrt{3}\\{(2x+1)e^x + \\sin\\pi x\\}$',
                        ],
                        'answer': 3,
                        'exp': '한 변의 길이가 $y$인 정삼각형의 넓이는 $\\dfrac{\\sqrt{3}}{4}y^2 = \\dfrac{\\sqrt{3}}{4}\\{(2x+1)e^x + \\sin\\pi x\\}$입니다.',
                        'exp_en': '$S(x) = \\dfrac{\\sqrt{3}}{4}y^2 = \\dfrac{\\sqrt{3}}{4}\\{(2x+1)e^x + \\sin\\pi x\\}$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [삼각함수 주기 대칭] $\\displaystyle\\int_0^2 \\sin\\pi x \\, dx$ 계산하기',
                'title_en': '🌱 Step 3 · [Periodic Symmetry] Evaluating $\\displaystyle\\int_0^2 \\sin\\pi x \\, dx$',
                'knowledge': '$\\sin\\pi x$의 주기는 $\\dfrac{2\\pi}{\\pi} = 2$입니다! $[0, 1]$에서의 양의 넓이와 $[1, 2]$에서의 음의 정적분이 정확히 대칭으로 상쇄되어 $\\left[-\\dfrac{\\cos\\pi x}{\\pi}\\right]_0^2 = -\\dfrac{1}{\\pi} - \\left(-\\dfrac{1}{\\pi}\\right) = 0$이 됩니다.',
                'knowledge_en': 'Since $\\sin\\pi x$ has period $\\dfrac{2\\pi}{\\pi} = 2$, integrating over one full period $[0, 2]$ cancels symmetrically to $0$.',
                'questions': [
                    {
                        'level_label': '한 주기 정적분 디딤돌 3',
                        'level_label_en': 'Full-Period Sine Step 3',
                        'stem': '정적분 $\\displaystyle\\int_0^2 \\sin\\pi x \\, dx = \\left[-\\frac{\\cos\\pi x}{\\pi}\\right]_0^2$의 값은?',
                        'stem_en': 'What is the value of $\\displaystyle\\int_0^2 \\sin\\pi x \\, dx = \\left[-\\frac{\\cos\\pi x}{\\pi}\\right]_0^2$?',
                        'options': ['$-\\dfrac{2}{\\pi}$', '$-\\dfrac{1}{\\pi}$', '$0$', '$\\dfrac{1}{\\pi}$', '$\\dfrac{2}{\\pi}$'],
                        'answer': 3,
                        'exp': '$\\cos 2\\pi = 1$, $\\cos 0 = 1$이므로 $-\\dfrac{1}{\\pi} + \\dfrac{1}{\\pi} = 0$입니다.',
                        'exp_en': '$-\\dfrac{\\cos 2\\pi}{\\pi} + \\dfrac{\\cos 0}{\\pi} = -\\dfrac{1}{\\pi} + \\dfrac{1}{\\pi} = 0$.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [지수함수 부분적분] $\\displaystyle\\int_0^2 (2x+1)e^x \\, dx$ 계산하기',
                'title_en': '🌳 Step 4 · [Exponential Integration by Parts] Evaluating $\\displaystyle\\int_0^2 (2x+1)e^x \\, dx$',
                'knowledge': "부분적분법(또는 $\\{(2x-1)e^x\\}' = 2e^x + (2x-1)e^x = (2x+1)e^x$)을 이용하면$$\\int_0^2 (2x+1)e^x \\, dx = \\left[(2x-1)e^x\\right]_0^2 = 3e^2 - (-1)e^0 = 3e^2 + 1$$입니다!",
                'knowledge_en': 'Since $\\dfrac{d}{dx}[(2x-1)e^x] = (2x+1)e^x$, evaluating from $0$ to $2$ gives $3e^2 - (-1)e^0 = 3e^2 + 1$.',
                'questions': [
                    {
                        'level_label': '지수함수 정적분 디딤돌 4',
                        'level_label_en': 'Exponential Integral Step 4',
                        'stem': '$\\displaystyle\\int_0^2 (2x+1)e^x \\, dx = \\left[(2x-1)e^x\\right]_0^2$를 계산한 값은?',
                        'stem_en': 'What is the value of $\\displaystyle\\int_0^2 (2x+1)e^x \\, dx = \\left[(2x-1)e^x\\right]_0^2$?',
                        'options': ['$3e^2 - 2$', '$3e^2 - 1$', '$3e^2 + 1$', '$3e^2 + 4$', '$5e^2 - 1$'],
                        'answer': 3,
                        'exp': '$x = 2$를 대입하면 $3e^2$, $x = 0$을 대입하면 $-1$이므로 $3e^2 - (-1) = 3e^2 + 1$입니다.',
                        'exp_en': 'At $x=2$ we get $3e^2$, and at $x=0$ we subtract $-1$, giving $3e^2 + 1$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 레고 조립] 입체도형의 부피 $V$ 완성하기',
                'title_en': '💎 Step 5 · [Final Synthesis] Completing the Volume $V$',
                'knowledge': '단면 계수 $\\dfrac{\\sqrt{3}}{4}$에 정적분 결과 $(3e^2 + 1) + 0$을 곱하면 부피 $V = \\dfrac{\\sqrt{3}(3e^2 + 1)}{4}$가 완성됩니다.',
                'knowledge_en': 'Multiplying $\\dfrac{\\sqrt{3}}{4}$ by $(3e^2 + 1) + 0$ gives $V = \\dfrac{\\sqrt{3}(3e^2 + 1)}{4}$.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': '이 입체도형의 부피 $V = \\displaystyle\\int_0^2 \\frac{\\sqrt{3}}{4}\\{(2x+1)e^x + \\sin\\pi x\\} \\, dx$의 값은?',
                        'stem_en': 'What is the volume $V = \\displaystyle\\int_0^2 \\frac{\\sqrt{3}}{4}\\{(2x+1)e^x + \\sin\\pi x\\} \\, dx$ of the solid?',
                        'options': [
                            '$\\dfrac{\\sqrt{3}(3e^2-2)}{8}$',
                            '$\\dfrac{\\sqrt{3}(3e^2+1)}{8}$',
                            '$\\dfrac{\\sqrt{3}(3e^2+4)}{8}$',
                            '$\\dfrac{\\sqrt{3}(3e^2-2)}{4}$',
                            '$\\dfrac{\\sqrt{3}(3e^2+1)}{4}$',
                        ],
                        'answer': 5,
                        'exp': '$V = \\dfrac{\\sqrt{3}}{4}(3e^2 + 1 + 0) = \\dfrac{\\sqrt{3}(3e^2+1)}{4}$이므로 정답은 ⑤입니다.',
                        'exp_en': '$V = \\dfrac{\\sqrt{3}(3e^2+1)}{4}$ (choice ⑤).',
                    }
                ],
            },
        ],
        'final': {
            'stem': '그림과 같이 곡선 $y = \\sqrt{(2x+1)e^x + \\sin\\pi x}\\;(x \\ge 0)$과 $x$축, $y$축 및 직선 $x = 2$로 둘러싸인 부분을 밑면으로 하는 입체도형이 있다. 이 입체도형을 $x$축에 수직인 평면으로 자른 단면이 모두 정삼각형일 때, 이 입체도형의 부피는? [3점]',
            'stem_en': 'As shown in the figure, the base of a solid is the region bounded by the curve $y = \\sqrt{(2x+1)e^x + \\sin\\pi x}\\;(x \\ge 0)$, the $x$-axis, the $y$-axis, and the line $x = 2$. Every cross-section perpendicular to the $x$-axis is an equilateral triangle. What is the volume of this solid? [3 points]',
            'options': [
                '$\\dfrac{\\sqrt{3}(3e^2-2)}{8}$',
                '$\\dfrac{\\sqrt{3}(3e^2+1)}{8}$',
                '$\\dfrac{\\sqrt{3}(3e^2+4)}{8}$',
                '$\\dfrac{\\sqrt{3}(3e^2-2)}{4}$',
                '$\\dfrac{\\sqrt{3}(3e^2+1)}{4}$',
            ],
            'answer': 5,
            'exp': '단면의 넓이 $S(x) = \\dfrac{\\sqrt{3}}{4}y^2 = \\dfrac{\\sqrt{3}}{4}\\{(2x+1)e^x + \\sin\\pi x\\}$이므로 부피는 $\\dfrac{\\sqrt{3}}{4}\\left(\\left[(2x-1)e^x\\right]_0^2 + \\left[-\\dfrac{\\cos\\pi x}{\\pi}\\right]_0^2\\right) = \\dfrac{\\sqrt{3}(3e^2+1)}{4}$입니다. 정답은 ⑤입니다.',
            'exp_en': 'Integrating $S(x) = \\dfrac{\\sqrt{3}}{4}\\{(2x+1)e^x + \\sin\\pi x\\}$ over $[0, 2]$ yields $\\dfrac{\\sqrt{3}}{4}(3e^2 + 1 + 0) = \\dfrac{\\sqrt{3}(3e^2+1)}{4}$. Correct answer: ⑤.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 정적분을 활용한 <b>입체도형의 부피($V = \\int_a^b S(x)dx$)</b>와 <b>지수·삼각함수의 정적분</b>을 결합한 문항입니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: 단면의 넓이 $S(x)$ 구하기</b><br>\n'
                '  구간 $[0, 2]$에 속하는 $x$에서 $x$축에 수직인 평면으로 자른 단면은 한 변의 길이가 $y = \\sqrt{(2x+1)e^x + \\sin\\pi x}$인 정삼각형이므로 단면의 넓이는\n'
                '  $$S(x) = \\frac{\\sqrt{3}}{4}y^2 = \\frac{\\sqrt{3}}{4}\\left\\{(2x+1)e^x + \\sin\\pi x\\right\\}$$\n'
                '  입니다.<br><br>\n'
                '  <b>2단계: 구간 $[0, 2]$에서 정적분하여 부피 계산하기</b><br>\n'
                '  $$\\begin{aligned}\n'
                '  V &= \\int_0^2 S(x) \\, dx = \\frac{\\sqrt{3}}{4} \\int_0^2 \\left\\{(2x+1)e^x + \\sin\\pi x\\right\\} dx \\\\\n'
                '  &= \\frac{\\sqrt{3}}{4} \\left(\\Bigl[(2x-1)e^x\\Bigr]_0^2 + \\left[-\\frac{\\cos\\pi x}{\\pi}\\right]_0^2\\right) \\\\\n'
                '  &= \\frac{\\sqrt{3}}{4} \\left\\{\\bigl(3e^2 - (-1)\\bigr) + \\left(-\\frac{1}{\\pi} + \\frac{1}{\\pi}\\right)\\right\\} = \\frac{\\sqrt{3}(3e^2+1)}{4}\n'
                '  \\end{aligned}$$\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>\n'
                '  $x = 0$을 $(2x-1)e^x$에 대입할 때 $(-1)e^0 = -1$을 빼므로 $+1$이 더해지는 부호만 정확히 처리하면 됩니다. 정답은 <b>⑤번 ($\\dfrac{\\sqrt{3}(3e^2+1)}{4}$)</b>입니다.\n'
                '</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis &amp; Core Concepts]</h4>\n'
                '<p>This item computes the <b>volume of a cross-sectional solid</b> $V = \\int_0^2 S(x)\\,dx$ whose cross-sections perpendicular to the $x$-axis are equilateral triangles.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  At each $x \\in [0, 2]$, the equilateral triangle has side length $y = \\sqrt{(2x+1)e^x + \\sin\\pi x}$, giving cross-sectional area\n'
                '  $$S(x) = \\frac{\\sqrt{3}}{4}y^2 = \\frac{\\sqrt{3}}{4}\\left\\{(2x+1)e^x + \\sin\\pi x\\right\\}.$$\n'
                '  Integrating from $x = 0$ to $x = 2$:\n'
                '  $$V = \\frac{\\sqrt{3}}{4}\\left(\\Bigl[(2x-1)e^x\\Bigr]_0^2 + \\left[-\\frac{\\cos\\pi x}{\\pi}\\right]_0^2\\right) = \\frac{\\sqrt{3}}{4}\\bigl((3e^2 + 1) + 0\\bigr) = \\frac{\\sqrt{3}(3e^2+1)}{4}.$$\n'
                '</p>\n\n'
                '<h4>✨ [Final Answer &amp; Practical Tips]</h4>\n'
                '<p>\n'
                '  Note that $\\sin\\pi x$ integrates to $0$ over its full period $[0, 2]$. The correct answer is <b>choice ⑤ ($\\dfrac{\\sqrt{3}(3e^2+1)}{4}$)</b>.\n'
                '</p>'
            ),
        },
    },

    # =========================================================================
    # 27번 (csat27_m27) — 음함수의 미분법과 두 접선의 교점 [3점] · 공식 정답 ③ (25/6)
    # =========================================================================
    {
        'slug': 'csat27_m27',
        'qNum': '27',
        'points': 3,
        'is_short_answer': False,
        'official_ans_str': '',
        'subject': '미적분',
        'title': '[2027학년도 수능 고3 미적분 27번] 음함수의 미분법과 두 접선이 이루는 삼각형의 넓이',
        'title_en': '[2027 CSAT Math Calculus #27] Implicit Differentiation and Area of Triangle Formed by Two Tangents',
        'summary_ko': '$y=1$과의 교점 $\\mathrm{P}\\left(-\\dfrac{3}{a},1\\right), \\mathrm{Q}\\left(\\dfrac{2}{a},1\\right)$에서 음함수 미분으로 두 접선의 교점 높이 $y_{\\mathrm{R}}-1=\\dfrac{25}{3}$을 구해 $a=\\dfrac{25}{6}$ 도출하기',
        'summary_en': 'Find intersections $\\mathrm{P}(-3/a, 1), \\mathrm{Q}(2/a, 1)$ on $y=1$, apply implicit differentiation to get tangent slopes $-5a$ and $-5a/4$, and use triangle height $25/3$ and area $5$ to find $a = 25/6$.',
        'tags': ['미적분', '미분법', '음함수의미분법', '접선의방정식', '삼각형의넓이', '2027학년도 수능', '27번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': '$C : a^2 x^2 + axy + e^{y^2 - 1} = 7$',
                'desc': '양수 $a$에 대하여 $x$와 $y$의 방정식으로 주어진 음함수 곡선',
                'desc_en': 'Implicit curve $C$ defined for a positive constant $a > 0$.',
            },
            {
                'sym': '$\\overline{\\mathrm{PQ}} = \\dfrac{2}{a} - \\left(-\\dfrac{3}{a}\\right) = \\dfrac{5}{a}$',
                'desc': '직선 $y = 1$을 곡선 식에 대입해 얻은 두 교점 $\\mathrm{P}, \\mathrm{Q}$ 사이의 밑변 길이',
                'desc_en': 'Horizontal base length between intersections $\\mathrm{P}$ and $\\mathrm{Q}$ along $y = 1$.',
            },
            {
                'sym': "$2a^2 x + ay + (ax + 2y e^{y^2 - 1})y' = 0$",
                'desc': '곡선 $C$의 양변을 $x$에 대하여 음함수 미분한 도함수 관계식',
                'desc_en': 'Implicit derivative equation of curve $C$ with respect to $x$.',
            },
            {
                'sym': '$\\triangle\\mathrm{PQR}\\text{ 넓이} = \\dfrac{1}{2} \\times \\overline{\\mathrm{PQ}} \\times |y_{\\mathrm{R}} - 1| = 5$',
                'desc': '수평 밑변 $\\overline{\\mathrm{PQ}}$와 교점 $\\mathrm{R}$의 세로 높이를 곱해 구하는 삼각형 넓이',
                'desc_en': 'Area of $\\triangle\\mathrm{PQR}$ computed from horizontal base $\\overline{\\mathrm{PQ}}$ and vertical height $|y_{\\mathrm{R}} - 1|$.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 삼각형 넓이 공식] $\\dfrac{1}{2} \\times \\dfrac{5}{a} \\times \\dfrac{25}{3} = 5$에서 $a$ 구하기',
                'title_en': '🔰 Step 1 · [Elementary Triangle Area] Solving $\\dfrac{1}{2} \\times \\dfrac{5}{a} \\times \\dfrac{25}{3} = 5$',
                'knowledge': '초등학교에서 배운 삼각형의 넓이는 $\\dfrac{1}{2} \\times (\\text{밑변}) \\times (\\text{높이})$입니다! 밑변이 $\\dfrac{5}{a}$이고 높이가 $\\dfrac{25}{3}$일 때 넓이가 $5$가 되는 양수 $a$를 먼저 초등 분수 계산으로 확인해 봅시다.',
                'knowledge_en': 'Using the elementary formula $\\text{Area} = \\dfrac{1}{2} \\times \\text{base} \\times \\text{height}$, solve $\\dfrac{1}{2} \\times \\dfrac{5}{a} \\times \\dfrac{25}{3} = 5$ for $a$.',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '삼각형의 넓이 식 $\\dfrac{1}{2} \\times \\dfrac{5}{a} \\times \\dfrac{25}{3} = 5$를 만족시키는 양수 $a$의 값은?',
                        'stem_en': 'Which positive fraction $a$ satisfies $\\dfrac{1}{2} \\times \\dfrac{5}{a} \\times \\dfrac{25}{3} = 5$?',
                        'options': ['$\\dfrac{5}{2}$', '$\\dfrac{25}{8}$', '$\\dfrac{25}{6}$', '$\\dfrac{25}{4}$', '$\\dfrac{25}{2}$'],
                        'answer': 3,
                        'exp': '$\\dfrac{125}{6a} = 5 \\implies 6a = 25 \\implies a = \\dfrac{25}{6}$입니다.',
                        'exp_en': '$\\dfrac{125}{6a} = 5 \\implies a = \\dfrac{25}{6}$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [교점과 밑변 길이] $y = 1$을 대입하여 선분 $\\mathrm{PQ}$의 길이 구하기',
                'title_en': '🌿 Step 2 · [Intersections & Base Length] Substituting $y = 1$ to Find $\\overline{\\mathrm{PQ}}$',
                'knowledge': '곡선 $a^2 x^2 + axy + e^{y^2 - 1} = 7$에 $y = 1$을 대입하면 $e^0 = 1$이므로$$(ax)^2 + ax + 1 = 7 \\implies (ax + 3)(ax - 2) = 0$$이 됩니다. 따라서 두 교점의 $x$좌표는 $-\\dfrac{3}{a}$과 $\\dfrac{2}{a}$입니다 ($a > 0$).',
                'knowledge_en': 'Setting $y = 1$ gives $(ax)^2 + ax + 1 = 7 \\implies (ax+3)(ax-2) = 0$, so the $x$-coordinates are $-\\dfrac{3}{a}$ and $\\dfrac{2}{a}$.',
                'questions': [
                    {
                        'level_label': '밑변 길이 도출 디딤돌 2',
                        'level_label_en': 'Base Length Step 2',
                        'stem': '양수 $a$에 대하여 직선 $y = 1$ 위의 두 교점 $\\mathrm{P}\\left(-\\dfrac{3}{a}, 1\\right)$, $\\mathrm{Q}\\left(\\dfrac{2}{a}, 1\\right)$ 사이의 거리 $\\overline{\\mathrm{PQ}}$는?',
                        'stem_en': 'For $a > 0$, what is the distance $\\overline{\\mathrm{PQ}}$ between $\\left(-\\dfrac{3}{a}, 1\\right)$ and $\\left(\\dfrac{2}{a}, 1\\right)$?',
                        'options': ['$\\dfrac{1}{a}$', '$\\dfrac{3}{a}$', '$\\dfrac{4}{a}$', '$\\dfrac{5}{a}$', '$\\dfrac{6}{a}$'],
                        'answer': 4,
                        'exp': '$\\overline{\\mathrm{PQ}} = \\dfrac{2}{a} - \\left(-\\dfrac{3}{a}\\right) = \\dfrac{5}{a}$입니다.',
                        'exp_en': '$\\dfrac{2}{a} - \\left(-\\dfrac{3}{a}\\right) = \\dfrac{5}{a}$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [음함수의 미분법] $y = 1$인 점에서의 접선의 기울기 식 구하기',
                'title_en': '🌱 Step 3 · [Implicit Differentiation] Finding $\\dfrac{dy}{dx}$ Along $y = 1$',
                'knowledge': '$a^2 x^2 + axy + e^{y^2 - 1} = 7$의 양변을 $x$에 대하여 미분하면$$2a^2 x + ay + ax y\' + 2y e^{y^2 - 1} y\' = 0$$이고, 여기에 $y = 1$ ($e^{y^2-1} = 1$)을 대입하면 $(ax + 2)y\' = -a(2ax + 1)$을 얻습니다.',
                'knowledge_en': 'Differentiating with respect to $x$ gives $2a^2 x + ay + (ax + 2y e^{y^2-1})y\' = 0$. Setting $y = 1$ yields $(ax + 2)y\' = -a(2ax + 1)$.',
                'questions': [
                    {
                        'level_label': '음함수 미분 추론 디딤돌 3',
                        'level_label_en': 'Implicit Slope Step 3',
                        'stem': '곡선 $C$ 위의 $y = 1$인 점에서 접선의 기울기 $y\'$을 $ax$에 대한 식으로 바르게 나타낸 것은?',
                        'stem_en': 'At points on $C$ with $y = 1$, which formula gives the tangent slope $y\'$?',
                        'options': [
                            '$-\\dfrac{a(2ax + 1)}{ax + 2}$',
                            '$\\dfrac{a(2ax + 1)}{ax + 2}$',
                            '$-\\dfrac{2ax + 1}{ax + 2}$',
                            '$-\\dfrac{a(ax + 1)}{2ax + 1}$',
                            '$-\\dfrac{a(2ax + 1)}{ax + 1}$',
                        ],
                        'answer': 1,
                        'exp': '$(ax + 2)y\' = -(2a^2 x + a) = -a(2ax + 1)$에서 $y\' = -\\dfrac{a(2ax + 1)}{ax + 2}$입니다.',
                        'exp_en': 'Solving $(ax + 2)y\' = -a(2ax + 1)$ gives $y\' = -\\dfrac{a(2ax + 1)}{ax + 2}$.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [두 접선의 교점 $\\mathrm{R}$] $ax$ 소거로 삼각형의 높이 $y_{\\mathrm{R}} - 1$ 구하기',
                'title_en': '🌳 Step 4 · [Tangent Intersection] Finding Vertical Height $y_{\\mathrm{R}} - 1$',
                'knowledge': '<ul><li>$ax = -3$인 점에서의 기울기: $-\\dfrac{a(-5)}{-1} = -5a \\implies y - 1 = -5(ax + 3) \\implies ax = -3 - \\dfrac{y - 1}{5}$</li><li>$ax = 2$인 점에서의 기울기: $-\\dfrac{a(5)}{4} = -\\dfrac{5a}{4} \\implies y - 1 = -\\dfrac{5}{4}(ax - 2) \\implies ax = 2 - \\dfrac{4(y - 1)}{5}$</li></ul>교점 $\\mathrm{R}$에서 두 $ax$가 같으므로 $a$에 관계없이 높이 $h = y_{\\mathrm{R}} - 1$이 상수로 깔끔하게 떨어집니다!',
                'knowledge_en': 'At $ax = -3$, the slope is $-5a$, giving $ax = -3 - \\dfrac{y-1}{5}$. At $ax = 2$, the slope is $-\\dfrac{5a}{4}$, giving $ax = 2 - \\dfrac{4(y-1)}{5}$. Equating $ax$ determines $y_{\\mathrm{R}} - 1$ independent of $a$.',
                'questions': [
                    {
                        'level_label': '교점 높이 계산 디딤돌 4',
                        'level_label_en': 'Triangle Height Step 4',
                        'stem': '두 접선의 식에서 $ax$를 같다고 놓은 방정식 $-3 - \\dfrac{h}{5} = 2 - \\dfrac{4h}{5}$ ($h = y_{\\mathrm{R}} - 1$)를 풀어 구한 삼각형 $\\mathrm{PQR}$의 높이 $h$는?',
                        'stem_en': 'Solving $-3 - \\dfrac{h}{5} = 2 - \\dfrac{4h}{5}$ for $h = y_{\\mathrm{R}} - 1$, what is the height $h$ of $\\triangle\\mathrm{PQR}$?',
                        'options': ['$5$', '$\\dfrac{20}{3}$', '$\\dfrac{25}{4}$', '$\\dfrac{25}{3}$', '$10$'],
                        'answer': 4,
                        'exp': '$\\dfrac{3h}{5} = 5 \\implies h = \\dfrac{25}{3}$입니다.',
                        'exp_en': '$\\dfrac{3h}{5} = 5 \\implies h = \\dfrac{25}{3}$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 레고 조립] 삼각형 넓이 $5$로부터 양수 $a$ 확정하기',
                'title_en': '💎 Step 5 · [Final Synthesis] Determining $a$ from Area $= 5$',
                'knowledge': '밑변 $\\overline{\\mathrm{PQ}} = \\dfrac{5}{a}$와 높이 $h = \\dfrac{25}{3}$을 결합하면 $\\dfrac{1}{2} \\times \\dfrac{5}{a} \\times \\dfrac{25}{3} = \\dfrac{125}{6a} = 5 \\implies a = \\dfrac{25}{6}$입니다.',
                'knowledge_en': 'Combining base $\\dfrac{5}{a}$ and height $\\dfrac{25}{3}$ gives $\\dfrac{125}{6a} = 5 \\implies a = \\dfrac{25}{6}$.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': '삼각형 $\\mathrm{PQR}$의 넓이가 $5$일 때, 양수 $a$의 값은?',
                        'stem_en': 'When the area of triangle $\\mathrm{PQR}$ is $5$, what is the positive constant $a$?',
                        'options': ['$\\dfrac{5}{2}$', '$\\dfrac{25}{8}$', '$\\dfrac{25}{6}$', '$\\dfrac{25}{4}$', '$\\dfrac{25}{2}$'],
                        'answer': 3,
                        'exp': '$\\dfrac{1}{2} \\times \\dfrac{5}{a} \\times \\dfrac{25}{3} = 5$에서 $a = \\dfrac{25}{6}$이므로 정답은 ③입니다.',
                        'exp_en': '$a = \\dfrac{25}{6}$ (choice ③).',
                    }
                ],
            },
        ],
        'final': {
            'stem': '양수 $a$에 대하여 곡선 $C : a^2 x^2 + axy + e^{y^2 - 1} = 7$과 직선 $y = 1$이 만나는 서로 다른 두 점을 $\\mathrm{P}$, $\\mathrm{Q}$라 하자. 곡선 $C$ 위의 점 $\\mathrm{P}$에서의 접선과 곡선 $C$ 위의 점 $\\mathrm{Q}$에서의 접선이 만나는 점을 $\\mathrm{R}$이라 할 때, 삼각형 $\\mathrm{PQR}$의 넓이는 $5$이다. $a$의 값은? [3점]',
            'stem_en': 'For a positive constant $a$, let $\\mathrm{P}$ and $\\mathrm{Q}$ be the two distinct intersection points of the curve $C : a^2 x^2 + axy + e^{y^2 - 1} = 7$ and the line $y = 1$. Let $\\mathrm{R}$ be the intersection point of the tangent lines to $C$ at $\\mathrm{P}$ and $\\mathrm{Q}$. If the area of triangle $\\mathrm{PQR}$ is $5$, what is the value of $a$? [3 points]',
            'options': ['$\\dfrac{5}{2}$', '$\\dfrac{25}{8}$', '$\\dfrac{25}{6}$', '$\\dfrac{25}{4}$', '$\\dfrac{25}{2}$'],
            'answer': 3,
            'exp': '$y=1$을 대입하면 $(ax)^2 + ax - 6 = 0$이므로 두 교점 사이의 거리는 $\\overline{\\mathrm{PQ}} = \\dfrac{5}{a}$이고, 음함수 미분법으로 구한 두 접선의 기울기 $-5a, -\\dfrac{5}{4}a$로부터 교점 $\\mathrm{R}$의 높이 $y_{\\mathrm{R}} - 1 = \\dfrac{25}{3}$을 얻습니다. 넓이 $\\dfrac{1}{2} \\cdot \\dfrac{5}{a} \\cdot \\dfrac{25}{3} = 5$에서 $a = \\dfrac{25}{6}$이므로 정답은 ③입니다.',
            'exp_en': 'Setting $y=1$ gives $(ax+3)(ax-2)=0$, so $\\overline{\\mathrm{PQ}} = \\dfrac{5}{a}$. Implicit differentiation yields tangent slopes $-5a$ and $-\\dfrac{5}{4}a$, whose intersection has height $y_{\\mathrm{R}}-1 = \\dfrac{25}{3}$. From $\\dfrac{1}{2}\\cdot\\dfrac{5}{a}\\cdot\\dfrac{25}{3} = 5$, we get $a = \\dfrac{25}{6}$. Correct answer: ③.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 <b>음함수의 미분법</b>을 활용하여 곡선 위의 두 교점에서의 접선의 방정식을 세우고, 두 접선과 수평선이 이루는 삼각형의 넓이로부터 미정계수 $a$를 구하는 문항입니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: 직선 $y = 1$과의 교점 $\\mathrm{P}, \\mathrm{Q}$ 및 밑변의 길이</b><br>\n'
                '  곡선 $C$의 방정식에 $y = 1$을 대입하면 $(ax)^2 + ax + 1 = 7 \\implies (ax + 3)(ax - 2) = 0$입니다.<br>\n'
                '  일반성을 잃지 않고 $\\mathrm{P}\\left(-\\dfrac{3}{a}, 1\\right)$, $\\mathrm{Q}\\left(\\dfrac{2}{a}, 1\\right)$라 하면 ($a > 0$), 밑변의 길이는 $\\overline{\\mathrm{PQ}} = \\dfrac{5}{a}$입니다.<br><br>\n'
                '  <b>2단계: 음함수 미분법으로 두 접선의 기울기 도출</b><br>\n'
                '  $a^2 x^2 + axy + e^{y^2 - 1} = 7$의 양변을 $x$에 대하여 미분하면\n'
                "  $$2a^2 x + ay + (ax + 2y e^{y^2 - 1})y' = 0$$\n"
                '  이므로 $y = 1$일 때 $y\' = -\\dfrac{a(2ax + 1)}{ax + 2}$입니다. 따라서:\n'
                '  • 점 $\\mathrm{P}$ ($ax = -3$)에서의 기울기: $y\'_{\\mathrm{P}} = -\\dfrac{a(-5)}{-1} = -5a$<br>\n'
                '  • 점 $\\mathrm{Q}$ ($ax = 2$)에서의 기울기: $y\'_{\\mathrm{Q}} = -\\dfrac{a(5)}{4} = -\\dfrac{5}{4}a$<br><br>\n'
                '  <b>3단계: 두 접선의 교점 $\\mathrm{R}$의 높이 및 $a$ 결정</b><br>\n'
                '  두 접선 $y - 1 = -5(ax + 3)$과 $y - 1 = -\\dfrac{5}{4}(ax - 2)$에서 $ax$를 소거하면\n'
                '  $$-3 - \\frac{y_{\\mathrm{R}} - 1}{5} = 2 - \\frac{4(y_{\\mathrm{R}} - 1)}{5} \\implies \\frac{3(y_{\\mathrm{R}} - 1)}{5} = 5 \\implies y_{\\mathrm{R}} - 1 = \\frac{25}{3}$$\n'
                '  따라서 삼각형 $\\mathrm{PQR}$의 넓이는 $\\dfrac{1}{2} \\times \\dfrac{5}{a} \\times \\dfrac{25}{3} = \\dfrac{125}{6a} = 5$이므로 $a = \\dfrac{25}{6}$입니다.\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>\n'
                '  $ax$를 하나의 묶음 변수로 보고 연립하면 $y_{\\mathrm{R}} - 1$에서 $a$가 완전히 소거되어 계산이 매우 간결해집니다. 정답은 <b>③번 ($\\dfrac{25}{6}$)</b>입니다.\n'
                '</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis &amp; Core Concepts]</h4>\n'
                '<p>This problem combines <b>implicit differentiation</b> with tangent line geometry to compute the area of $\\triangle\\mathrm{PQR}$.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Intersections with $y = 1$</b><br>\n'
                '  Substituting $y = 1$ into $a^2 x^2 + axy + e^{y^2-1} = 7$ gives $(ax)^2 + ax - 6 = 0$, so $x = -\\dfrac{3}{a}$ and $x = \\dfrac{2}{a}$, yielding base $\\overline{\\mathrm{PQ}} = \\dfrac{5}{a}$.<br><br>\n'
                '  <b>Step 2: Implicit differentiation &amp; tangent intersection</b><br>\n'
                "  Differentiating gives $2a^2 x + ay + (ax + 2ye^{y^2-1})y' = 0$. At $y = 1$, $y' = -\\dfrac{a(2ax+1)}{ax+2}$, so the slopes at $\\mathrm{P}$ and $\\mathrm{Q}$ are $-5a$ and $-\\dfrac{5a}{4}$. Eliminating $ax$ between $y - 1 = -5(ax+3)$ and $y - 1 = -\\dfrac{5}{4}(ax-2)$ yields $y_{\\mathrm{R}} - 1 = \\dfrac{25}{3}$.<br><br>\n"
                '  <b>Step 3: Area equation</b><br>\n'
                '  $$\\frac{1}{2} \\cdot \\frac{5}{a} \\cdot \\frac{25}{3} = \\frac{125}{6a} = 5 \\implies a = \\frac{25}{6}.$$\n'
                '</p>\n\n'
                '<h4>✨ [Final Answer &amp; Practical Tips]</h4>\n'
                '<p>\n'
                '  Treating $ax$ as a single variable eliminates $a$ from the vertical height immediately. Correct answer: <b>choice ③ ($\\dfrac{25}{6}$)</b>.\n'
                '</p>'
            ),
        },
    },

    # =========================================================================
    # 28번 (csat27_m28) — 역함수 미분법과 유일근 조건 [4점] · 공식 정답 ④
    # =========================================================================
    {
        'slug': 'csat27_m28',
        'qNum': '28',
        'points': 4,
        'is_short_answer': False,
        'official_ans_str': '',
        'subject': '미적분',
        'title': '[2027학년도 수능 고3 미적분 28번] 역함수 관계식으로 정의된 함수의 유일근 접선 조건과 역함수의 미분법',
        'title_en': '[2027 CSAT Math Calculus #28] Inverse Function Identity, Unique Positive Root Tangency, and Inverse Derivative',
        'summary_ko': '$g(x) = x - f^{-1}(x)$에서 $g(f(t)) = ate^{-bt} = \\dfrac{1}{b}$의 유일 양수 근 조건으로 $a = e,\\; b = \\dfrac{2}{e},\\; k = e$를 결정하고 $g(k) + g\'(k+1) = \\dfrac{(e+1)(e-2)}{2(e-1)}$ 구하기',
        'summary_en': 'Deduce $g(x) = x - f^{-1}(x)$ so $g(f(t)) = ate^{-bt}$. Unique positive root tangency of $bte^{-bt} = 1/a$ gives $a = e, k = 2/b$, and $f(k)=k+1$ gives $b = 2/e, k = e$, yielding $g(k) + g\'(k+1) = \\dfrac{(e+1)(e-2)}{2(e-1)}$.',
        'tags': ['미적분', '미분법', '역함수의미분법', '지수함수의극대극소', '방정식의실근의개수', '2027학년도 수능', '28번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': '$f(x - g(x)) = x \\iff g(x) = x - f^{-1}(x)$',
                'desc': '역함수 $f^{-1}$를 양변에 취하여 얻는 $g(x)$의 명시적 표현',
                'desc_en': 'Applying $f^{-1}$ to Condition (가) expresses $g(x)$ directly via $f^{-1}(x)$.',
            },
            {
                'sym': '$g(f(t)) = f(t) - t = ate^{-bt}$',
                'desc': '$x = f(t)$ ($x > 0 \\iff t > 0$)로 치환할 때 $x$ 항이 소거되어 남는 지수함수',
                'desc_en': 'Substituting $x = f(t)$ simplifies $g(f(t))$ cleanly to $ate^{-bt}$.',
            },
            {
                'sym': '$\\phi(u) = ue^{-u} \\le \\phi(1) = \\dfrac{1}{e}\\quad (u > 0)$',
                'desc': '양수 $u$에서 $u = 1$일 때 유일한 극댓값이자 최댓값 $\\dfrac{1}{e}$을 갖는 곡선',
                'desc_en': 'Function $ue^{-u}$ attains its unique positive maximum $1/e$ at $u = 1$.',
            },
            {
                'sym': "$g'(k+1) = 1 - \\dfrac{1}{f'(k)}$",
                'desc': '$f(k) = k + 1 \\iff f^{-1}(k+1) = k$일 때 역함수의 미분법으로 구한 도함숫값',
                'desc_en': 'Derivative of $g(x) = x - f^{-1}(x)$ at $x = k + 1 = f(k)$ via the inverse function theorem.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 식 묶기와 인수분해] $e^2 - e - 2$를 두 일차식의 곱으로 바꾸기',
                'title_en': '🔰 Step 1 · [Elementary Factoring] Factoring $e^2 - e - 2$ into Linear Factors',
                'knowledge': '이 문제의 마지막 분수 덧셈 $\\dfrac{e}{2} - \\dfrac{1}{e - 1}$을 통분하면 분자에 $e(e - 1) - 2 = e^2 - e - 2$가 나타납니다! 곱해서 $-2$가 되고 더해서 $-1$이 되는 두 정수 $+1$과 $-2$를 먼저 찾아 봅시다.',
                'knowledge_en': 'Combining $\\dfrac{e}{2} - \\dfrac{1}{e-1}$ produces the numerator $e^2 - e - 2$. Find two integers with product $-2$ and sum $-1$.',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '곱해서 $-2$, 더해서 $-1$이 되는 두 정수 $+1, -2$를 이용하여 $e^2 - e - 2$를 바르게 인수분해한 식은?',
                        'stem_en': 'Using two integers whose product is $-2$ and sum is $-1$, how does $e^2 - e - 2$ factor?',
                        'options': [
                            '$(e - 1)(e - 2)$',
                            '$(e + 1)(e - 2)$',
                            '$(e - 1)(e + 2)$',
                            '$(e + 1)(e + 2)$',
                            '$e(e - 2)$',
                        ],
                        'answer': 2,
                        'exp': '$(+1) + (-2) = -1$, $(+1) \\times (-2) = -2$이므로 $(e + 1)(e - 2)$입니다.',
                        'exp_en': '$(e + 1)(e - 2) = e^2 - e - 2$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [조건 (가) 해석] 역함수를 이용하여 $g(f(t))$ 간단히 하기',
                'title_en': '🌿 Step 2 · [Interpreting Condition (가)] Simplifying $g(f(t))$ via $f^{-1}$',
                'knowledge': '역함수를 갖는 함수 $f(x) = axe^{-bx} + x$에 대하여 조건 (가) $f(x - g(x)) = x$의 양변에 $f^{-1}$를 취하면$$x - g(x) = f^{-1}(x) \\implies g(x) = x - f^{-1}(x)$$입니다. 여기에 $x = f(t)$를 대입하면 $f^{-1}(f(t)) = t$이므로 놀랍게도 $t$가 지워집니다!',
                'knowledge_en': 'Applying $f^{-1}$ to $f(x - g(x)) = x$ gives $g(x) = x - f^{-1}(x)$. Substituting $x = f(t)$ yields $g(f(t)) = f(t) - t$.',
                'questions': [
                    {
                        'level_label': '역함수 치환 디딤돌 2',
                        'level_label_en': 'Inverse Substitution Step 2',
                        'stem': '$f(t) = ate^{-bt} + t$이고 $g(x) = x - f^{-1}(x)$일 때, $g(f(t))$를 $t$에 대한 식으로 간단히 나타낸 것은?',
                        'stem_en': 'Given $f(t) = ate^{-bt} + t$ and $g(x) = x - f^{-1}(x)$, what does $g(f(t))$ equal?',
                        'options': ['$t$', '$ate^{-bt}$', '$ate^{-bt} + t$', '$\\dfrac{1}{b}e^{-bt}$', '$abe^{-bt}$'],
                        'answer': 2,
                        'exp': '$g(f(t)) = f(t) - t = (ate^{-bt} + t) - t = ate^{-bt}$입니다.',
                        'exp_en': '$g(f(t)) = f(t) - t = ate^{-bt}$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [조건 (나) 유일근 조건] $(bt)e^{-bt} = \\dfrac{1}{a}$의 극댓값으로 $a$와 $k$ 구하기',
                'title_en': '🌱 Step 3 · [Unique Root in Condition (나)] Finding $a$ and $k$ via Maximum of $ue^{-u}$',
                'knowledge': '$0 < a < e^2$이므로 $f\'(x) = a(1-bx)e^{-bx} + 1 \\ge 1 - ae^{-2} > 0$이고 $f(0) = 0$이어서, 양수 $x > 0$과 양수 $t = f^{-1}(x) > 0$은 일대일 대응합니다! 따라서 조건 (나)는$$ate^{-bt} = \\frac{1}{b} \\iff (bt)e^{-bt} = \\frac{1}{a}$$의 양수 근 $t$가 오직 $1$개라는 뜻입니다. $\\phi(u) = ue^{-u}$ ($u > 0$)는 $u = 1$에서 유일한 최댓값 $\\dfrac{1}{e}$을 가지므로 $\\dfrac{1}{a} = \\dfrac{1}{e} \\implies a = e$이고, 그때 $bt = 1 \\implies t = \\dfrac{1}{b}$입니다!',
                'knowledge_en': 'Since $f(0)=0$ and $f\'(x) > 0$, $x > 0 \\iff t > 0$. Thus $(bt)e^{-bt} = \\dfrac{1}{a}$ has a unique positive root iff $\\dfrac{1}{a}$ equals the maximum $\\dfrac{1}{e}$ of $ue^{-u}$ at $u = bt = 1$, giving $a = e$ and $k = f(1/b)$.',
                'questions': [
                    {
                        'level_label': '유일근 접선 추론 디딤돌 3',
                        'level_label_en': 'Unique Positive Root Step 3',
                        'stem': '조건 (나)로부터 얻은 상수 $a$의 값과, $g(k) = \\dfrac{1}{b}$인 유일한 양수 $k = f\\left(\\dfrac{1}{b}\\right)$를 $b$로 바르게 나타낸 것은?',
                        'stem_en': 'From Condition (나), what are the constant $a$ and the unique positive $k = f(1/b)$ in terms of $b$?',
                        'options': [
                            '$a = 1,\\; k = \\dfrac{1}{b}$',
                            '$a = e,\\; k = \\dfrac{1}{b}$',
                            '$a = e,\\; k = \\dfrac{2}{b}$',
                            '$a = e^2,\\; k = \\dfrac{2}{b}$',
                            '$a = \\dfrac{1}{e},\\; k = \\dfrac{2}{b}$',
                        ],
                        'answer': 3,
                        'exp': '$a = e$이고 $k = f\\left(\\dfrac{1}{b}\\right) = e \\cdot \\dfrac{1}{b} \\cdot e^{-1} + \\dfrac{1}{b} = \\dfrac{2}{b}$입니다.',
                        'exp_en': '$a = e$, and $k = f(1/b) = e \\cdot \\dfrac{1}{b} e^{-1} + \\dfrac{1}{b} = \\dfrac{2}{b}$.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [$b, k$ 결정 및 역함수 미분] $f(k) = k + 1$로부터 $g\'(k+1)$ 구하기',
                'title_en': '🌳 Step 4 · [Inverse Derivative] Determining $b, k$ and Evaluating $g\'(k+1)$',
                'knowledge': '$f(k) = k + 1 \\iff eke^{-bk} = 1$에 $k = \\dfrac{2}{b}$($bk = 2$)를 대입하면$$e \\cdot \\frac{2}{b} \\cdot e^{-2} = 1 \\implies b = \\frac{2}{e},\\quad k = e$$입니다! 또한 $f^{-1}(k+1) = k = e$이고 $f\'(x) = e(1 - bx)e^{-bx} + 1$에서 $f\'(e) = e(1 - 2)e^{-2} + 1 = \\dfrac{e - 1}{e}$이므로 $g\'(k+1) = 1 - \\dfrac{1}{f\'(e)}$를 바로 구할 수 있습니다.',
                'knowledge_en': 'Substituting $k = 2/b$ ($bk = 2$) into $eke^{-bk} = 1$ yields $b = 2/e$ and $k = e$. Since $f^{-1}(k+1) = e$ and $f\'(e) = 1 - 1/e = (e-1)/e$, we compute $g\'(k+1) = 1 - 1/f\'(e)$.',
                'questions': [
                    {
                        'level_label': '역함수 미분계수 디딤돌 4',
                        'level_label_en': 'Inverse Derivative Step 4',
                        'stem': '$f\'(e) = \\dfrac{e - 1}{e}$일 때, $g\'(k + 1) = 1 - \\dfrac{1}{f\'(e)}$의 값은?',
                        'stem_en': 'Given $f\'(e) = \\dfrac{e - 1}{e}$, what is the value of $g\'(k + 1) = 1 - \\dfrac{1}{f\'(e)}$?',
                        'options': [
                            '$-\\dfrac{1}{e + 1}$',
                            '$-\\dfrac{1}{e - 1}$',
                            '$\\dfrac{1}{e - 1}$',
                            '$\\dfrac{e - 2}{e - 1}$',
                            '$-\\dfrac{e}{e - 1}$',
                        ],
                        'answer': 2,
                        'exp': '$1 - \\dfrac{e}{e - 1} = \\dfrac{(e - 1) - e}{e - 1} = -\\dfrac{1}{e - 1}$입니다.',
                        'exp_en': '$1 - \\dfrac{e}{e - 1} = -\\dfrac{1}{e - 1}$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 레고 조립] $g(k) + g\'(k + 1)$ 통분하여 완성하기',
                'title_en': '💎 Step 5 · [Final Synthesis] Combining $g(k) + g\'(k + 1)$',
                'knowledge': '$g(k) = \\dfrac{1}{b} = \\dfrac{e}{2}$과 $g\'(k + 1) = -\\dfrac{1}{e - 1}$을 더하면$$\\frac{e}{2} - \\frac{1}{e - 1} = \\frac{e(e - 1) - 2}{2(e - 1)} = \\frac{e^2 - e - 2}{2(e - 1)} = \\frac{(e + 1)(e - 2)}{2(e - 1)}$$이 완성됩니다.',
                'knowledge_en': 'Adding $g(k) = \\dfrac{e}{2}$ and $g\'(k+1) = -\\dfrac{1}{e-1}$ yields $\\dfrac{e^2 - e - 2}{2(e - 1)} = \\dfrac{(e + 1)(e - 2)}{2(e - 1)}$.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': '$g(k) = \\dfrac{e}{2}$, $g\'(k + 1) = -\\dfrac{1}{e - 1}$일 때, $g(k) + g\'(k + 1)$의 값은?',
                        'stem_en': 'With $g(k) = \\dfrac{e}{2}$ and $g\'(k + 1) = -\\dfrac{1}{e - 1}$, what is $g(k) + g\'(k + 1)$?',
                        'options': [
                            '$\\dfrac{e^2 - e - 1}{2(e + 1)}$',
                            '$\\dfrac{e(e - 1)}{2(e + 1)}$',
                            '$\\dfrac{e^2 - 5}{2(e - 1)}$',
                            '$\\dfrac{(e + 1)(e - 2)}{2(e - 1)}$',
                            '$\\dfrac{e^2 - 3}{2(e - 1)}$',
                        ],
                        'answer': 4,
                        'exp': '$\\dfrac{e}{2} - \\dfrac{1}{e - 1} = \\dfrac{(e + 1)(e - 2)}{2(e - 1)}$이므로 정답은 ④입니다.',
                        'exp_en': '$\\dfrac{(e + 1)(e - 2)}{2(e - 1)}$ (choice ④).',
                    }
                ],
            },
        ],
        'final': {
            'stem': (
                '역함수를 갖는 함수 $f(x) = axe^{-bx} + x\\;(0 < a < e^2,\\; b > 0)$과 실수 전체의 집합에서 미분가능한 함수 $g(x)$에 대하여 다음 조건이 성립한다.'
                '<span style="display:block;margin:10px 0;padding:10px 14px;border:1px solid #cbd5e1;border-radius:8px;background:#f8fafc">'
                '(가) 모든 실수 $x$에 대하여 $f(x - g(x)) = x$이다.<br>'
                '(나) $g(x) = \\dfrac{1}{b}$인 양수 $x$의 개수는 $1$이다.'
                '</span>'
                '$g(k) = \\dfrac{1}{b}$인 양수 $k$에 대하여 $f(k) = k + 1$일 때, $g(k) + g\'(k + 1)$의 값은? '
                '(단, $\\lim_{x \\to \\infty} xe^{-x} = 0$이고, $a$와 $b$는 상수이다.) [4점]'
            ),
            'stem_en': (
                'An invertible function $f(x) = axe^{-bx} + x\\;(0 < a < e^2,\\; b > 0)$ and a function $g(x)$ differentiable on $\\mathbb{R}$ satisfy:'
                '<span style="display:block;margin:10px 0;padding:10px 14px;border:1px solid #cbd5e1;border-radius:8px;background:#f8fafc">'
                '(가) For all real numbers $x$, $f(x - g(x)) = x$.<br>'
                '(나) The number of positive real numbers $x$ such that $g(x) = \\dfrac{1}{b}$ is $1$.'
                '</span>'
                'For the positive number $k$ satisfying $g(k) = \\dfrac{1}{b}$, if $f(k) = k + 1$, what is the value of $g(k) + g\'(k + 1)$? '
                '(Here $\\lim_{x \\to \\infty} xe^{-x} = 0$, and $a, b$ are constants.) [4 points]'
            ),
            'options': [
                '$\\dfrac{e^2 - e - 1}{2(e + 1)}$',
                '$\\dfrac{e(e - 1)}{2(e + 1)}$',
                '$\\dfrac{e^2 - 5}{2(e - 1)}$',
                '$\\dfrac{(e + 1)(e - 2)}{2(e - 1)}$',
                '$\\dfrac{e^2 - 3}{2(e - 1)}$',
            ],
            'answer': 4,
            'exp': '조건 (가)에서 $g(x) = x - f^{-1}(x)$이고 $x = f(t)$ ($t > 0$)로 치환하면 $g(f(t)) = ate^{-bt} = \\dfrac{1}{b}$의 양수 근이 유일하므로 $a = e$, $t = \\dfrac{1}{b}$, $k = f\\left(\\dfrac{1}{b}\\right) = \\dfrac{2}{b}$입니다. $f(k) = k + 1$에서 $b = \\dfrac{2}{e},\\; k = e$를 얻고 $g(k) = \\dfrac{e}{2}$, $g\'(k+1) = 1 - \\dfrac{1}{f\'(e)} = -\\dfrac{1}{e - 1}$이므로 합은 $\\dfrac{(e + 1)(e - 2)}{2(e - 1)}$입니다. 정답은 ④입니다.',
            'exp_en': 'From (가), $g(x) = x - f^{-1}(x)$ and $g(f(t)) = ate^{-bt}$. Unique positive root tangency in (나) yields $a = e$ and $k = f(1/b) = 2/b$. Then $f(k) = k + 1$ gives $b = 2/e, k = e$, so $g(k) + g\'(k+1) = \\dfrac{e}{2} - \\dfrac{1}{e - 1} = \\dfrac{(e + 1)(e - 2)}{2(e - 1)}$. Correct answer: ④.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 미적분 객관식 최고난도(28번) 문항으로, <b>역함수 합성 항등식의 해석($g(x) = x - f^{-1}(x)$)</b>, <b>지수함수 $ue^{-u}$의 극댓값을 이용한 유일근 추론</b>, 그리고 <b>역함수의 미분법</b>을 유기적으로 결합한 문항입니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: 조건 (가)에서 $g(x)$와 $f^{-1}(x)$의 관계식 도출</b><br>\n'
                '  $0 < a < e^2,\\; b > 0$에서 $f\'(x) = a(1 - bx)e^{-bx} + 1 \\ge 1 - ae^{-2} > 0$이므로 $f$는 실수 전체에서 순증가하고 $f(0) = 0$, $\\lim_{x \\to \\infty} f(x) = \\infty$입니다.<br>\n'
                '  조건 (가) $f(x - g(x)) = x$에서 $x - g(x) = f^{-1}(x) \\implies g(x) = x - f^{-1}(x)$입니다.<br><br>\n'
                '  <b>2단계: 조건 (나)의 유일한 양수 실근 조건으로 $a = e$와 $k = \\dfrac{2}{b}$ 결정</b><br>\n'
                '  $x = f(t)$라 놓으면 $x > 0 \\iff t > 0$이 일대일 대응하며, $g(f(t)) = f(t) - t = ate^{-bt}$입니다.<br>\n'
                '  따라서 $g(x) = \\dfrac{1}{b}$인 양수 $x$가 $1$개라는 것은 방정식 $(bt)e^{-bt} = \\dfrac{1}{a}$의 양수 근 $t$가 유일하다는 뜻입니다.<br>\n'
                '  함수 $\\phi(u) = ue^{-u}$ ($u > 0$)는 $u = 1$에서 유일한 극댓값이자 최댓값 $\\dfrac{1}{e}$을 갖고 $\\lim_{u \\to 0^+} \\phi(u) = \\lim_{u \\to \\infty} \\phi(u) = 0$이므로,\n'
                '  $$\\frac{1}{a} = \\frac{1}{e} \\implies a = e, \\qquad bt = 1 \\implies t = \\frac{1}{b}$$\n'
                '  이고, 유일한 양수 근 $x = k$는 $k = f\\left(\\dfrac{1}{b}\\right) = e \\cdot \\dfrac{1}{b} e^{-1} + \\dfrac{1}{b} = \\dfrac{2}{b}$입니다.<br><br>\n'
                '  <b>3단계: $f(k) = k + 1$에서 $b, k$ 확정 및 $g(k) + g\'(k + 1)$ 계산</b><br>\n'
                '  $f(k) - k = eke^{-bk} = 1$에 $k = \\dfrac{2}{b}$ ($bk = 2$)를 대입하면 $e \\cdot \\dfrac{2}{b} e^{-2} = 1 \\implies b = \\dfrac{2}{e},\\; k = e$입니다.<br>\n'
                '  • $g(k) = \\dfrac{1}{b} = \\dfrac{e}{2}$<br>\n'
                '  • $f(e) = k + 1 \\implies f^{-1}(k + 1) = e$이고 $f\'(e) = e(1 - 2)e^{-2} + 1 = \\dfrac{e - 1}{e}$이므로\n'
                '  $$g\'(k + 1) = 1 - \\frac{1}{f\'(e)} = 1 - \\frac{e}{e - 1} = -\\frac{1}{e - 1}$$\n'
                '  따라서 구하는 값은\n'
                '  $$g(k) + g\'(k + 1) = \\frac{e}{2} - \\frac{1}{e - 1} = \\frac{e^2 - e - 2}{2(e - 1)} = \\frac{(e + 1)(e - 2)}{2(e - 1)}$$\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>\n'
                '  $x = f(t)$ 치환 한 줄로 역함수 방정식을 $ate^{-bt} = \\dfrac{1}{b}$로 바꾸는 발상이 핵심 열쇠입니다. 정답은 <b>④번 ($\\dfrac{(e + 1)(e - 2)}{2(e - 1)}$)</b>입니다.\n'
                '</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis &amp; Core Concepts]</h4>\n'
                '<p>This 4-point Calculus problem integrates <b>inverse function identities</b>, <b>tangency for a unique positive root of $ue^{-u}$</b>, and the <b>inverse function derivative formula</b>.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Expressing $g(x)$ via $f^{-1}(x)$</b><br>\n'
                '  Since $0 < a < e^2$, $f\'(x) = a(1-bx)e^{-bx} + 1 \\ge 1 - ae^{-2} > 0$ on $\\mathbb{R}$ with $f(0)=0$, so $t \\mapsto f(t)$ maps $(0, \\infty)$ bijectively onto $(0, \\infty)$. Condition (가) gives $g(x) = x - f^{-1}(x)$, so setting $x = f(t)$ yields $g(f(t)) = ate^{-bt}$.<br><br>\n'
                '  <b>Step 2: Unique positive root condition</b><br>\n'
                '  Condition (나) requires $(bt)e^{-bt} = \\dfrac{1}{a}$ to have a unique root $t > 0$. Since $ue^{-u}$ ($u>0$) achieves its unique maximum $\\dfrac{1}{e}$ at $u = 1$, we obtain $a = e$, $t = \\dfrac{1}{b}$, and $k = f\\left(\\dfrac{1}{b}\\right) = \\dfrac{2}{b}$.<br><br>\n'
                '  <b>Step 3: Finding $b, k$ and $g(k) + g\'(k+1)$</b><br>\n'
                '  From $f(k) - k = eke^{-bk} = 1$ with $k = \\dfrac{2}{b}$, we get $\\dfrac{2}{be} = 1 \\implies b = \\dfrac{2}{e}$ and $k = e$. Then $g(k) = \\dfrac{e}{2}$, $f^{-1}(k+1) = e$, and $f\'(e) = 1 - \\dfrac{1}{e} = \\dfrac{e-1}{e}$, so\n'
                '  $$g\'(k+1) = 1 - \\frac{1}{f\'(e)} = -\\frac{1}{e - 1}, \\qquad g(k) + g\'(k+1) = \\frac{e}{2} - \\frac{1}{e - 1} = \\frac{(e + 1)(e - 2)}{2(e - 1)}.$$\n'
                '</p>\n\n'
                '<h4>✨ [Final Answer &amp; Practical Tips]</h4>\n'
                '<p>\n'
                '  Parametrizing $x = f(t)$ bypasses solving for $f^{-1}(x)$ explicitly. Correct answer: <b>choice ④ ($\\dfrac{(e + 1)(e - 2)}{2(e - 1)}$)</b>.\n'
                '</p>'
            ),
        },
    },

    # =========================================================================
    # 29번 (csat27_m29) — 수열의 극한과 급수의 발산 [4점, 단답형] · 공식 정답 12
    # =========================================================================
    {
        'slug': 'csat27_m29',
        'qNum': '29',
        'points': 4,
        'is_short_answer': True,
        'official_ans_str': '12',
        'subject': '미적분',
        'title': '[2027학년도 수능 고3 미적분 29번] 등비수열을 포함한 분수식 극한과 급수의 발산 조건',
        'title_en': '[2027 CSAT Math Calculus #29] Exponential Rational Sequence Limit and Divergence Condition of Infinite Series',
        'summary_ko': '$8k$와 $k^2+15$의 대소를 나누어 무수히 많은 $n$에서 $(a_n-1)(a_{n+1}+1) < 0$ ($a_n \\in (-1, 1)$)이 되는 자연수 $k = 5, 7$을 찾아 합 $12$ 구하기',
        'summary_en': 'Compare exponential bases $8k$ and $k^2 + 15$ to find all natural numbers $k$ for which $(a_n - 1)(a_{n+1} + 1) < 0$ holds infinitely often, obtaining $k \\in \\{5, 7\\}$ and sum $5 + 7 = 12$.',
        'tags': ['미적분', '급수', '급수의수렴과발산', '등비수열의극한', '단답형', '2027학년도 수능', '29번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': '$a_n = \\dfrac{6 \\times (8k)^n}{(k^2 + 15)^n + 10} + 2k - 15$',
                'desc': '분자의 밑 $8k$와 분모의 밑 $k^2 + 15$의 대소에 따라 극한값이 달라지는 수열',
                'desc_en': 'Sequence whose asymptotic behavior is governed by comparing bases $8k$ and $k^2 + 15$.',
            },
            {
                'sym': '$(a_n - 1) \\times (a_{n+1} + 1) < 0$',
                'desc': '$a_n - 1$과 $a_{n+1} + 1$의 부호가 서로 반대일 때 $b_n = 1$이 되는 판별 조건',
                'desc_en': 'Sign-opposition condition assigning $b_n = 1$ (in particular satisfied whenever $a_n, a_{n+1} \\in (-1, 1)$).',
            },
            {
                'sym': '$\\displaystyle\\sum_{n=1}^{\\infty} b_n\\text{ 발산} \\iff b_n = 1\\text{이 무한히 많음}$',
                'desc': '$b_n \\in \\{0, 1\\}$이므로 급수가 발산하려면 무수히 많은 $n$에서 부등식이 성립해야 함',
                'desc_en': 'Since $b_n \\in \\{0, 1\\}$, $\\sum b_n$ diverges iff $b_n = 1$ for infinitely many $n$.',
            },
            {
                'sym': '$(k^2 + 15) - 8k = (k - 3)(k - 5)$',
                'desc': '두 밑 $k^2 + 15$와 $8k$의 크기가 같아지는 경계 $k = 3, 5$를 찾는 인수분해식',
                'desc_en': 'Difference of exponential bases factoring as $(k - 3)(k - 5)$.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 $0$과 $1$ 더하기] $0$ 또는 $1$만 나오는 급수가 발산할 조건',
                'title_en': '🔰 Step 1 · [Elementary Sum of 0s and 1s] When Does a $0$-$1$ Series Diverge?',
                'knowledge': '수열 $b_n$의 각 항은 $1$ 아니면 $0$입니다! 만약 $1$이 유한 번(예: $8$번)만 나오고 그 뒤로 계속 $0$만 나오면 합은 $8$에서 멈추어 수렴합니다. 합이 멈추지 않고 한없이 커지려면(발산하려면) $b_n = 1$이 끝없이 계속 나와야 합니다!',
                'knowledge_en': 'Each term $b_n$ is either $0$ or $1$. If $1$ appears only finitely many times, the sum is finite; for the series to diverge, $b_n = 1$ must occur infinitely many times.',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '$0$ 또는 $1$의 값만 갖는 수열 $\\{b_n\\}$을 끝없이 더한 급수 $b_1 + b_2 + b_3 + \\cdots$가 발산하려면 $b_n = 1$인 자연수 $n$이 몇 개 있어야 하나요?',
                        'stem_en': 'For $b_1 + b_2 + b_3 + \\cdots$ with $b_n \\in \\{0, 1\\}$ to diverge, how many indices $n$ must satisfy $b_n = 1$?',
                        'options': ['$0$개', '$1$개', '$5$개', '$10$개 이하의 유한 개', '무수히 많음(무한히 계속)'],
                        'answer': 5,
                        'exp': '$b_n = 1$이 무수히 많이 나와야 부분합이 $1$씩 끝없이 커져서 발산합니다.',
                        'exp_en': 'Infinitely many $1$s are required so the partial sums grow without bound.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [밑의 대소 비교] $8k$와 $k^2 + 15$의 크기가 같아지는 자연수 $k$ 찾기',
                'title_en': '🌿 Step 2 · [Comparing Bases] Solving $8k = k^2 + 15$',
                'knowledge': '분수식 $\\dfrac{6 \\times (8k)^n}{(k^2 + 15)^n + 10}$의 극한은 분자의 밑 $8k$와 분모의 밑 $k^2 + 15$ 중 누가 더 큰지에 따라 결정됩니다!$$(k^2 + 15) - 8k = k^2 - 8k + 15 = (k - 3)(k - 5)$$',
                'knowledge_en': 'The limit of $\\dfrac{6 \\times (8k)^n}{(k^2 + 15)^n + 10}$ depends on comparing $8k$ and $k^2 + 15$, where $(k^2 + 15) - 8k = (k - 3)(k - 5)$.',
                'questions': [
                    {
                        'level_label': '밑 비교 경계값 디딤돌 2',
                        'level_label_en': 'Equal-Base Boundary Step 2',
                        'stem': '이차방정식 $k^2 - 8k + 15 = 0$을 풀어 분자의 밑 $8k$와 분모의 밑 $k^2 + 15$가 같아지는 두 자연수 $k$를 구하면?',
                        'stem_en': 'For which two natural numbers $k$ are the bases $8k$ and $k^2 + 15$ equal?',
                        'options': ['$1,\\; 15$', '$2,\\; 6$', '$3,\\; 5$', '$4,\\; 6$', '$5,\\; 7$'],
                        'answer': 3,
                        'exp': '$(k - 3)(k - 5) = 0$이므로 $k = 3$ 또는 $k = 5$입니다.',
                        'exp_en': 'Factoring $(k - 3)(k - 5) = 0$ gives $k = 3$ and $k = 5$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [밑이 같을 때 판정] $k = 3, 5$일 때 $(a_n - 1)(a_{n+1} + 1) < 0$ 조사하기',
                'title_en': '🌱 Step 3 · [Equal Bases Case] Checking $k = 3$ and $k = 5$',
                'knowledge': '<ul><li><b>$k = 3$일 때</b> ($8k = k^2 + 15 = 24$): $a_n = \\dfrac{6 \\cdot 24^n}{24^n + 10} - 9 < -3$이므로 $a_n - 1 < 0$이고 $a_{n+1} + 1 < 0$이어서 곱이 양수($b_n = 0$, 수렴)입니다.</li><li><b>$k = 5$일 때</b> ($8k = k^2 + 15 = 40$): $a_n = \\dfrac{6 \\cdot 40^n}{40^n + 10} - 5 = 1 - \\dfrac{60}{40^n + 10}$입니다! 모든 자연수 $n \\ge 1$에서 $40^n + 10 \\ge 50$이므로 $-\\dfrac{1}{5} \\le a_n < 1$이 되어 $a_n - 1 < 0$, $a_{n+1} + 1 > 0$이 항상 성립합니다!</li></ul>',
                'knowledge_en': 'For $k = 3$, $a_n < -3$ so both factors are negative ($b_n = 0$). For $k = 5$, $a_n = 1 - \\dfrac{60}{40^n + 10} \\in [-1/5, 1)$ for every $n \\ge 1$, making $a_n - 1 < 0$ and $a_{n+1} + 1 > 0$ always!',
                'questions': [
                    {
                        'level_label': '밑 일치 구간 판정 디딤돌 3',
                        'level_label_en': 'Equal-Base Check Step 3',
                        'stem': '$k = 5$일 때 모든 자연수 $n$에 대하여 $-\\dfrac{1}{5} \\le a_n < 1$입니다. 이때 $(a_n - 1)(a_{n+1} + 1)$의 부호와 급수 $\\displaystyle\\sum_{n=1}^{\\infty} b_n$의 수렴·발산으로 옳은 것은?',
                        'stem_en': 'When $k = 5$, $-\\dfrac{1}{5} \\le a_n < 1$ for all $n \\ge 1$. What is the sign of $(a_n - 1)(a_{n+1} + 1)$ and behavior of $\\sum_{n=1}^\\infty b_n$?',
                        'options': [
                            '모든 $n$에서 음수($< 0$)이므로 $b_n = 1$이 되어 급수가 발산한다.',
                            '모든 $n$에서 양수($> 0$)이므로 $b_n = 0$이 되어 급수가 수렴한다.',
                            '모든 $n$에서 $0$이므로 급수가 $0$으로 수렴한다.',
                            '$n = 1$일 때만 음수이므로 급수가 $1$로 수렴한다.',
                            '홀수 $n$에서만 양수이고 유한합으로 수렴한다.',
                        ],
                        'answer': 1,
                        'exp': '$a_n - 1 < 0$이고 $a_{n+1} + 1 \\ge \\dfrac{4}{5} > 0$이므로 모든 $n$에서 곱이 음수가 되어 $b_n = 1$이며 급수는 발산합니다!',
                        'exp_en': 'Since $a_n - 1 < 0$ and $a_{n+1} + 1 > 0$ for all $n$, $b_n = 1$ for all $n$ and the series diverges.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [분모의 밑이 더 클 때 ($8k < k^2 + 15$)] 미세 양수 $+\\epsilon_n$의 방향 분석하기',
                'title_en': '🌳 Step 4 · [Smaller Numerator Base] Analyzing $a_n = (2k - 15) + \\epsilon_n$ ($\\epsilon_n \\to 0^+$)',
                'knowledge': '<ul><li>$k = 4$이면 $8k = 32 > 31 = k^2 + 15$이므로 $a_n \\to +\\infty$가 되어 큰 $n$에서 두 인수가 모두 양수($b_n = 0$, 수렴)입니다.</li><li>$k \\in \\{1, 2\\} \\cup \\{6, 7, 8, \\dots\\}$이면 $8k < k^2 + 15$이므로 $\\epsilon_n = \\dfrac{6 \\times (8k)^n}{(k^2+15)^n + 10} > 0$은 <b>양수를 유지하며 $0$에 수렴($\\epsilon_n \\to 0^+$)</b>합니다!</li><li>따라서 $a_n = (2k - 15) + \\epsilon_n$이 충분히 큰 모든 $n$에서 열린구간 $(-1, 1)$ 안으로 들어오려면 극한값 $2k - 15$가 경계 $-1$이어야 합니다! ($2k - 15 = +1$인 $k = 8$은 $a_n = 1 + \\epsilon_n > 1$이라 $a_n - 1 > 0$이 되어 탈락!)</li></ul>',
                'knowledge_en': 'When $8k < k^2 + 15$, $\\epsilon_n > 0$ approaches $0^+$, so $a_n = (2k - 15) + \\epsilon_n$ approaches $2k - 15$ strictly from above. Thus $a_n \\in (-1, 1)$ for all large $n$ iff $2k - 15 = -1$ ($k = 7$); for $k = 8$, $a_n = 1 + \\epsilon_n > 1$ fails!',
                'questions': [
                    {
                        'level_label': '우극한 경계 판정 디딤돌 4',
                        'level_label_en': 'One-Sided Limit Step 4',
                        'stem': '$8k < k^2 + 15$인 자연수 $k$ 중에서 $2k - 15 = -1$을 만족하여 충분히 큰 모든 $n$에서 $-1 < a_n = -1 + \\epsilon_n < 1$이 되게 하는 자연수 $k$는?',
                        'stem_en': 'Among natural numbers $k$ with $8k < k^2 + 15$, which $k$ gives $2k - 15 = -1$ so that $-1 < a_n < 1$ for all sufficiently large $n$?',
                        'options': ['$k = 4$', '$k = 6$', '$k = 7$', '$k = 8$', '$k = 9$'],
                        'answer': 3,
                        'exp': '$2k - 15 = -1 \\implies 2k = 14 \\implies k = 7$이며, 이때 $a_n = -1 + \\epsilon_n$ ($0 < \\epsilon_n < 2$, 큰 $n$)이므로 $a_n - 1 < 0,\\; a_{n+1} + 1 = \\epsilon_{n+1} > 0$이 되어 발산합니다!',
                        'exp_en': '$2k - 15 = -1 \\implies k = 7$, for which $a_n - 1 < 0$ and $a_{n+1} + 1 = \\epsilon_{n+1} > 0$ for all large $n$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 레고 조립] 조건을 만족하는 모든 자연수 $k$의 합 구하기',
                'title_en': '💎 Step 5 · [Final Synthesis] Sum of All Valid Natural Numbers $k$',
                'knowledge': '따라서 급수 $\\displaystyle\\sum_{n=1}^{\\infty} b_n$이 발산하도록 하는 모든 자연수 $k$는 $5$와 $7$뿐이므로, 합은 $5 + 7 = 12$입니다.',
                'knowledge_en': 'The valid natural numbers are $k = 5$ and $k = 7$, giving a sum of $5 + 7 = 12$.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': '급수 $\\displaystyle\\sum_{n=1}^{\\infty} b_n$이 발산하도록 하는 모든 자연수 $k$의 값의 합은?',
                        'stem_en': 'What is the sum of all natural numbers $k$ for which $\\displaystyle\\sum_{n=1}^{\\infty} b_n$ diverges?',
                        'options': ['$10$', '$11$', '$12$', '$13$', '$14$'],
                        'answer': 3,
                        'exp': '$k = 5$와 $k = 7$의 합은 $5 + 7 = 12$입니다.',
                        'exp_en': '$5 + 7 = 12$.',
                    }
                ],
            },
        ],
        'final': {
            'stem': (
                '자연수 $k$에 대하여 수열 $\\{a_n\\}$의 일반항은<br>'
                '$$a_n = \\dfrac{6 \\times (8k)^n}{(k^2 + 15)^n + 10} + 2k - 15$$'
                '이고, 수열 $\\{b_n\\}$은 모든 자연수 $n$에 대하여<br>'
                '$$b_n = \\begin{cases} 1 & ((a_n - 1) \\times (a_{n+1} + 1) < 0\\text{인 경우}) \\\\ 0 & (\\text{그 외의 경우}) \\end{cases}$$'
                '이다. 급수 $\\displaystyle\\sum_{n=1}^{\\infty} b_n$이 발산하도록 하는 모든 자연수 $k$의 값의 합을 구하시오. [4점]'
            ),
            'stem_en': (
                'For a natural number $k$, let the sequence $\\{a_n\\}$ have general term<br>'
                '$$a_n = \\dfrac{6 \\times (8k)^n}{(k^2 + 15)^n + 10} + 2k - 15,$$'
                'and let the sequence $\\{b_n\\}$ be defined for every natural number $n$ by<br>'
                '$$b_n = \\begin{cases} 1 & (\\text{if } (a_n - 1) \\times (a_{n+1} + 1) < 0) \\\\ 0 & (\\text{otherwise}). \\end{cases}$$'
                'Find the sum of all natural numbers $k$ for which the infinite series $\\displaystyle\\sum_{n=1}^{\\infty} b_n$ diverges. [4 points]'
            ),
            'options': ['$10$', '$11$', '$12$', '$13$', '$14$'],
            'answer': 3,
            'exp': '$b_n \\in \\{0, 1\\}$이므로 급수가 발산하려면 무수히 많은 $n$에서 $(a_n - 1)(a_{n+1} + 1) < 0$이어야 합니다. $(k^2+15)-8k=(k-3)(k-5)$에 따라 조사하면 $k = 5$일 때 $a_n = 1 - \\dfrac{60}{40^n+10} \\in (-1, 1)$로 성립하고, $8k < k^2 + 15$일 때는 $a_n = (2k - 15) + \\epsilon_n$ ($\\epsilon_n \\to 0^+$)이므로 $2k - 15 = -1$인 $k = 7$에서만 충분히 큰 모든 $n$에 대해 $a_n \\in (-1, 1)$이 되어 성립합니다. 따라서 구하는 합은 $5 + 7 = 12$입니다.',
            'exp_en': 'Since $b_n \\in \\{0, 1\\}$, $\\sum b_n$ diverges iff $(a_n - 1)(a_{n+1} + 1) < 0$ holds infinitely often. Case analysis on $(k^2+15) - 8k = (k-3)(k-5)$ yields $k = 5$ ($a_n = 1 - \\dfrac{60}{40^n+10} \\in (-1, 1)$) and $k = 7$ ($a_n = -1 + \\epsilon_n \\in (-1, 1)$ for large $n$ as $\\epsilon_n \\to 0^+$). Their sum is $5 + 7 = 12$.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 <b>등비수열을 포함한 분수식의 극한 분류</b>와 <b>급수의 발산 필요충분조건($b_n \\in \\{0, 1\\}$일 때 무한히 많은 $n$에서 $b_n = 1$)</b>, 그리고 극한값으로 다가가는 미세 부호($+0$ vs $-0$)를 정밀하게 판별하는 문항입니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: 급수의 발산 조건과 밑의 대소 비교</b><br>\n'
                '  $b_n \\in \\{0, 1\\}$이므로 $\\sum_{n=1}^{\\infty} b_n$이 발산할 필요충분조건은 무수히 많은 자연수 $n$에서 $(a_n - 1)(a_{n+1} + 1) < 0$이 성립하는 것입니다.<br>\n'
                '  분모와 분자의 밑의 차는 $(k^2 + 15) - 8k = (k - 3)(k - 5)$입니다.<br><br>\n'
                '  <b>2단계: 세 구간별 $a_n$의 거동 전수 조사</b><br>\n'
                '  ① <b>$8k > k^2 + 15$ ($k = 4$)</b>: $8k = 32 > 31 = k^2 + 15$이므로 $\\lim_{n \\to \\infty} a_n = +\\infty$입니다. 충분히 큰 모든 $n$에서 $a_n - 1 > 0,\\; a_{n+1} + 1 > 0$이므로 $b_n = 0$이 되어 수렴합니다.<br>\n'
                '  ② <b>$8k = k^2 + 15$ ($k = 3$ 또는 $k = 5$)</b>: $M = 8k$라 하면 $a_n = (2k - 9) - \\dfrac{60}{M^n + 10}$입니다.<br>\n'
                '  &nbsp;&nbsp;• $k = 3$: $a_n = -3 - \\dfrac{60}{24^n + 10} < -3$이므로 두 인수가 모두 음수($b_n = 0$, 수렴).<br>\n'
                '  &nbsp;&nbsp;• <b>$k = 5$</b>: $a_n = 1 - \\dfrac{60}{40^n + 10}$이므로 모든 $n \\ge 1$에서 $-\\dfrac{1}{5} \\le a_n < 1$입니다. 따라서 $a_n - 1 < 0,\\; a_{n+1} + 1 > 0$이 항상 성립하여 $b_n = 1$ (<b>발산!</b>).<br>\n'
                '  ③ <b>$8k < k^2 + 15$ ($k \\in \\{1, 2, 6, 7, 8, \\dots\\}$)</b>: $\\epsilon_n = \\dfrac{6 \\times (8k)^n}{(k^2 + 15)^n + 10}$이라 하면 모든 $n$에서 $\\epsilon_n > 0$이고 $\\lim_{n \\to \\infty} \\epsilon_n = 0$입니다. 즉 $a_n = (2k - 15) + \\epsilon_n$입니다.<br>\n'
                '  &nbsp;&nbsp;• $k \\in \\{1, 2, 6\\}$: $2k - 15 \\le -3$이므로 큰 $n$에서 $a_n < -2$가 되어 두 인수 모두 음수($b_n = 0$, 수렴).<br>\n'
                '  &nbsp;&nbsp;• $k \\ge 8$: $2k - 15 \\ge 1$이므로 $a_n = (2k - 15) + \\epsilon_n > 1$이 되어 모든 $n$에서 두 인수 모두 양수($b_n = 0$, 수렴).<br>\n'
                '  &nbsp;&nbsp;• <b>$k = 7$</b>: $a_n = -1 + \\epsilon_n$이고 충분히 큰 모든 $n$에서 $0 < \\epsilon_n < 2$이므로 $-1 < a_n < 1$입니다. 따라서 $a_n - 1 < 0,\\; a_{n+1} + 1 = \\epsilon_{n+1} > 0$이 무수히 많은 $n$에서 성립하여 <b>발산</b>합니다!<br><br>\n'
                '  <b>3단계: 모든 자연수 $k$의 값의 합</b><br>\n'
                '  조건을 만족시키는 자연수는 $k = 5, 7$이므로 구하는 합은 $5 + 7 = 12$입니다.\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>\n'
                '  극한값만 보면 $k = 8$($\\lim a_n = 1$)도 후보처럼 보이지만, $a_n = 1 + \\epsilon_n > 1$이어서 $a_n - 1 > 0$이 되므로 제외된다는 점이 최고의 변별 포인트입니다. 정답은 <b>$12$</b>입니다.\n'
                '</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis &amp; Core Concepts]</h4>\n'
                '<p>This short-answer problem tests <b>asymptotic analysis of exponential rational sequences</b> and <b>one-sided convergence</b> relative to the interval $(-1, 1)$.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  Since $b_n \\in \\{0, 1\\}$, $\\sum_{n=1}^{\\infty} b_n$ diverges iff $(a_n - 1)(a_{n+1} + 1) < 0$ for infinitely many $n$. Note $(k^2 + 15) - 8k = (k - 3)(k - 5)$.<br>\n'
                '  • <b>Case $k = 4$ ($8k > k^2 + 15$)</b>: $a_n \\to +\\infty$, so $b_n = 0$ for large $n$ (converges).<br>\n'
                '  • <b>Case $k = 3, 5$ ($8k = k^2 + 15$)</b>: For $k = 3$, $a_n < -3$ ($b_n = 0$). For <b>$k = 5$</b>, $a_n = 1 - \\dfrac{60}{40^n + 10} \\in [-1/5, 1)$ for all $n \\ge 1$, so $(a_n - 1)(a_{n+1} + 1) < 0$ always (<b>diverges</b>).<br>\n'
                '  • <b>Case $k \\in \\{1, 2, 6, 7, 8, \\dots\\}$ ($8k < k^2 + 15$)</b>: Write $a_n = (2k - 15) + \\epsilon_n$ with $\\epsilon_n > 0$ and $\\epsilon_n \\to 0$. For $k \\in \\{1, 2, 6\\}$, $a_n \\to 2k - 15 \\le -3$; for $k \\ge 8$, $a_n > 1$ for all $n$. Only for <b>$k = 7$</b> do we have $a_n = -1 + \\epsilon_n \\in (-1, 1)$ for all sufficiently large $n$, giving $a_n - 1 < 0$ and $a_{n+1} + 1 = \\epsilon_{n+1} > 0$ (<b>diverges</b>).<br>\n'
                '  Hence $k \\in \\{5, 7\\}$, and their sum is $5 + 7 = 12$.\n'
                '</p>\n\n'
                '<h4>✨ [Final Answer &amp; Practical Tips]</h4>\n'
                '<p>\n'
                '  Checking the strict sign $\\epsilon_n > 0$ rules out $k = 8$ cleanly while confirming $k = 5$ and $k = 7$. Final answer: <b>$12$</b>.\n'
                '</p>'
            ),
        },
    },

    # =========================================================================
    # 30번 (csat27_m30) — 미분가능성과 정적분 [4점, 단답형] · 공식 정답 75
    # =========================================================================
    {
        'slug': 'csat27_m30',
        'qNum': '30',
        'points': 4,
        'is_short_answer': True,
        'official_ans_str': '75',
        'subject': '미적분',
        'title': '[2027학년도 수능 고3 미적분 30번] 절댓값 삼각함수의 실수 전체 미분가능성과 사분면 부호 결정 정적분',
        'title_en': '[2027 CSAT Math Calculus #30] Global Differentiability of Absolute Trigonometric Function and Quadrant Sign Integrals',
        'summary_ko': '$h_0(x)=\\sin x(\\sqrt{1+3\\cos^2 x}-1)$의 영점 미분계수를 분석해 구간별 부호 $(s_1, s_2, s_3) = (1, -1, -1)$을 결정하고, $J = \\dfrac{5}{18}$로부터 $\\alpha = 3J = \\dfrac{5}{6}$, $90\\alpha = 75$ 구하기',
        'summary_en': 'Analyze differentiability of $|f(x)| = |h_0(x)|$ at multiples of $\\pi/2$ to determine interval signs $(s_1, s_2, s_3) = (1, -1, -1)$ via (나), then evaluate $J = 5/18$ by $u = \\cos x$ to get $\\alpha = 3J = 5/6$ and $90\\alpha = 75$.',
        'tags': ['미적분', '적분법', '미분가능성', '치환적분법', '정적분과대칭성', '단답형', '2027학년도 수능', '30번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': '$h_0(x) = \\sin x \\left(\\sqrt{1 + 3\\cos^2 x} - 1\\right)$',
                'desc': '$|f(x)| = |h_0(x)|$를 만족시키는 실수 전체에서 미분가능한 기준 함수',
                'desc_en': 'Smooth reference function satisfying $|f(x)| = |h_0(x)|$ on $\\mathbb{R}$.',
            },
            {
                'sym': '$h_0\'(n\\pi) = (-1)^n \\neq 0,\\quad h_0\'\\left(\\dfrac{\\pi}{2} + n\\pi\\right) = 0$',
                'desc': '$x = n\\pi$에서는 부호가 유지되어야 하고, $x = \\dfrac{\\pi}{2} + n\\pi$에서는 부호 전환이 자유로운 미분가능 조건',
                'desc_en': 'Nonzero slope at $n\\pi$ forbids sign flips, whereas zero slope at $\\pi/2 + n\\pi$ permits free sign selection.',
            },
            {
                'sym': '$(s_1, s_2, s_3) = (1, -1, -1)$',
                'desc': '세 구간 $\\left[0, \\dfrac{\\pi}{2}\\right], \\left[\\dfrac{\\pi}{2}, \\dfrac{3\\pi}{2}\\right], \\left[\\dfrac{3\\pi}{2}, 2\\pi\\right]$에서 조건 (나)로 확정된 $f(x) = s_i h_0(x)$의 부호',
                'desc_en': 'Signs on $[0, \\pi/2]$, $[\\pi/2, 3\\pi/2]$, and $[3\\pi/2, 2\\pi]$ uniquely determined by Condition (나).',
            },
            {
                'sym': '$J = \\displaystyle\\int_0^{\\frac{\\pi}{2}} h_0(x)\\cos x \\, dx = \\dfrac{5}{18}$',
                'desc': '$u = \\cos x$로 치환하여 구하는 제1사분면 정적분 기본 블록',
                'desc_en': 'First-quadrant base integral evaluated via substitution $u = \\cos x$.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 분수 곱셈] 기본 조각 $J = \\dfrac{5}{18}$가 $3$개 모였을 때 $90 \\times \\alpha$ 계산하기',
                'title_en': '🔰 Step 1 · [Elementary Fraction Multiplication] Computing $90 \\times 3J$ for $J = \\dfrac{5}{18}$',
                'knowledge': '이 문제를 사분면 조각퍼즐처럼 쪼개면, 똑같은 크기의 넓이 조각 $J = \\dfrac{5}{18}$가 정확히 $3$개 남아서 $\\alpha = 3J$가 됩니다! 먼저 초등 분수 곱셈과 약분으로 $90 \\times 3 \\times \\dfrac{5}{18}$을 계산해 봅시다.',
                'knowledge_en': 'Breaking $[0, 2\\pi]$ into four congruent quadrant blocks of size $J = \\dfrac{5}{18}$ leaves $\\alpha = 3J$. Compute $90 \\times 3 \\times \\dfrac{5}{18}$ using elementary fraction cancellation.',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '$J = \\dfrac{5}{18}$이고 $\\alpha = 3J = \\dfrac{5}{6}$일 때, $90 \\times \\alpha$를 약분하여 계산한 자연수는?',
                        'stem_en': 'If $J = \\dfrac{5}{18}$ and $\\alpha = 3J = \\dfrac{5}{6}$, what is $90 \\times \\alpha$?',
                        'options': ['$60$', '$65$', '$70$', '$75$', '$80$'],
                        'answer': 4,
                        'exp': '$90 \\times \\dfrac{5}{6} = 15 \\times 5 = 75$입니다.',
                        'exp_en': '$90 \\times \\dfrac{5}{6} = 15 \\times 5 = 75$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [미분가능성과 부호 전환점] $x = n\\pi$ vs $x = \\dfrac{\\pi}{2} + n\\pi$ 비교하기',
                'title_en': '🌿 Step 2 · [Differentiability & Sign-Flip Points] Comparing $x = n\\pi$ and $x = \\dfrac{\\pi}{2} + n\\pi$',
                'knowledge': '기준 함수 $h_0(x) = \\sin x \\left(\\sqrt{1 + 3\\cos^2 x} - 1\\right)$은 $x = \\dfrac{k\\pi}{2}$ ($k \\in \\mathbb{Z}$)에서만 $0$이 됩니다.<ul><li><b>$x = n\\pi$일 때</b>: $\\sqrt{1 + 3\\cos^2(n\\pi)} - 1 = \\sqrt{4} - 1 = 1 \\neq 0$이므로 $h_0\'(n\\pi) = \\cos(n\\pi) \\cdot 1 = (-1)^n \\neq 0$입니다! 미분가능하려면 $x = n\\pi$ 좌우에서 $h_0(x)$ 앞의 부호가 <b>절대 바뀔 수 없습니다</b>.</li><li><b>$x = \\dfrac{\\pi}{2} + n\\pi$일 때</b>: $\\cos x = 0$이므로 $\\sqrt{1 + 3\\cos^2 x} - 1$의 함숫값과 미분계수가 모두 $0$이 되어 $h_0\'\\left(\\dfrac{\\pi}{2} + n\\pi\\right) = 0$입니다! 따라서 좌우 부호를 <b>자유롭게 선택</b>해도 미분가능합니다.</li></ul>',
                'knowledge_en': 'At $x = n\\pi$, $h_0\'(n\\pi) = (-1)^n \\neq 0$, so the sign in $f(x) = \\pm h_0(x)$ cannot change across $n\\pi$. At $x = \\pi/2 + n\\pi$, both $\\sqrt{1+3\\cos^2 x}-1$ and its derivative vanish, so $h_0\' = 0$ and the sign can switch freely!',
                'questions': [
                    {
                        'level_label': '미분가능 부호 전환점 디딤돌 2',
                        'level_label_en': 'Differentiability Check Step 2',
                        'stem': '열린구간 $(0, 2\\pi)$ 안에서 실수 전체 미분가능한 함수 $f(x) = \\pm h_0(x)$의 앞 부호($+$ 또는 $-$)가 바뀔 수 있는 지점만을 있는 대로 고른 것은?',
                        'stem_en': 'Inside $(0, 2\\pi)$, at which points can the sign $\\pm$ in $f(x) = \\pm h_0(x)$ change while preserving differentiability on $\\mathbb{R}$?',
                        'options': [
                            '$x = \\pi$만 가능',
                            '$x = \\dfrac{\\pi}{2},\\; \\dfrac{3\\pi}{2}$만 가능',
                            '$x = \\dfrac{\\pi}{2},\\; \\pi,\\; \\dfrac{3\\pi}{2}$ 모두 가능',
                            '부호가 바뀔 수 있는 점이 없다',
                            '$x = \\dfrac{\\pi}{4},\\; \\dfrac{3\\pi}{4}$만 가능',
                        ],
                        'answer': 2,
                        'exp': '$x = \\pi$에서는 $h_0\'(\\pi) = -1 \\neq 0$이라 부호가 유지되어야 하고, $x = \\dfrac{\\pi}{2}, \\dfrac{3\\pi}{2}$에서는 $h_0\' = 0$이므로 부호가 자유롭게 바뀔 수 있습니다.',
                        'exp_en': 'Only $x = \\dfrac{\\pi}{2}$ and $x = \\dfrac{3\\pi}{2}$ have $h_0\'(x) = 0$, allowing sign switches.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [조건 (나)의 부등식 해석] 세 구간의 부호 $(s_1, s_2, s_3)$ 확정하기',
                'title_en': '🌱 Step 3 · [Condition (나) Sign Deduction] Determining $(s_1, s_2, s_3)$',
                'knowledge': '세 구간 $\\left[0, \\dfrac{\\pi}{2}\\right], \\left[\\dfrac{\\pi}{2}, \\dfrac{3\\pi}{2}\\right], \\left[\\dfrac{3\\pi}{2}, 2\\pi\\right]$에서 $f(x) = s_i h_0(x)$ ($s_i \\in \\{-1, 1\\}$)라 놓고 $I = \\int_0^{\\pi/2} h_0(x)dx > 0$이라 합시다.<ul><li>사분면별 $\\int h_0(x)dx$는 $(+I, +I, -I, -I)$이므로 $\\int_0^{2\\pi} f(x)dx = s_1 I + s_2(I - I) + s_3(-I) = (s_1 - s_3)I > 0 \\implies s_1 = 1,\\; s_3 = -1$!</li><li>구간 $\\left[\\dfrac{\\pi}{2}, \\dfrac{3\\pi}{2}\\right]$에서 $h_0(x)$는 $\\left[\\dfrac{\\pi}{2}, \\pi\\right]$에서 양수, $\\left[\\pi, \\dfrac{3\\pi}{2}\\right]$에서 대칭인 음수인데 가중치 $x$가 뒤쪽 구간에서 더 크므로 $\\int_{\\pi/2}^{3\\pi/2} x h_0(x)dx < 0$입니다! 따라서 $s_2 \\int_{\\pi/2}^{3\\pi/2} x h_0(x)dx > 0 \\implies s_2 = -1$!</li></ul>',
                'knowledge_en': 'With quadrant integrals of $h_0$ equal to $(+I, +I, -I, -I)$, $\\int_0^{2\\pi} f(x)dx = (s_1 - s_3)I > 0$ forces $s_1 = 1, s_3 = -1$. On $[\\pi/2, 3\\pi/2]$, $h_0$ is positive on $[\\pi/2, \\pi]$ and antisymmetric negative on $[\\pi, 3\\pi/2]$ where $x$ is larger, so $\\int_{\\pi/2}^{3\\pi/2} x h_0(x)dx < 0$, forcing $s_2 = -1$.',
                'questions': [
                    {
                        'level_label': '구간 부호 추론 디딤돌 3',
                        'level_label_en': 'Interval Sign Deduction Step 3',
                        'stem': '조건 (나)의 두 부등식 $\\displaystyle\\int_0^{2\\pi} f(x)dx > 0$과 $\\displaystyle\\int_{\\frac{\\pi}{2}}^{\\frac{3\\pi}{2}} x f(x)dx > 0$을 모두 만족시키는 부호 순서쌍 $(s_1, s_2, s_3)$은?',
                        'stem_en': 'Which sign triple $(s_1, s_2, s_3) \\in \\{-1, 1\\}^3$ satisfies both inequalities in Condition (나)?',
                        'options': [
                            '$(1,\\; 1,\\; -1)$',
                            '$(1,\\; -1,\\; -1)$',
                            '$(1,\\; -1,\\; 1)$',
                            '$(-1,\\; -1,\\; 1)$',
                            '$(-1,\\; 1,\\; -1)$',
                        ],
                        'answer': 2,
                        'exp': '$s_1 - s_3 > 0$에서 $s_1 = 1, s_3 = -1$이고, $\\int_{\\pi/2}^{3\\pi/2} x h_0(x)dx < 0$이므로 $s_2 = -1$입니다.',
                        'exp_en': 'We obtain $(s_1, s_2, s_3) = (1, -1, -1)$.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [치환적분 계산] $u = \\cos x$로 기본 블록 $J$의 값 구하기',
                'title_en': '🌳 Step 4 · [Substitution Integral] Computing Base Integral $J$ via $u = \\cos x$',
                'knowledge': '$J = \\displaystyle\\int_0^{\\frac{\\pi}{2}} \\sin x \\cos x \\left(\\sqrt{1 + 3\\cos^2 x} - 1\\right) dx$에서 $u = \\cos x$ ($-\\sin x dx = du$)로 치환하면$$J = \\int_0^1 u\\left(\\sqrt{1 + 3u^2} - 1\\right) du = \\left[\\frac{1}{9}(1 + 3u^2)^{\\frac{3}{2}} - \\frac{1}{2}u^2\\right]_0^1$$입니다!',
                'knowledge_en': 'Substituting $u = \\cos x$ transforms $J$ into $\\int_0^1 u(\\sqrt{1+3u^2} - 1)\\,du = \\left[\\dfrac{1}{9}(1+3u^2)^{3/2} - \\dfrac{1}{2}u^2\\right]_0^1$.',
                'questions': [
                    {
                        'level_label': '치환적분 계산 디딤돌 4',
                        'level_label_en': 'Substitution Evaluation Step 4',
                        'stem': '정적분 $J = \\left[\\dfrac{1}{9}(1 + 3u^2)^{\\frac{3}{2}} - \\dfrac{1}{2}u^2\\right]_0^1$을 계산한 기약분수는?',
                        'stem_en': 'What is the value of $J = \\left[\\dfrac{1}{9}(1 + 3u^2)^{\\frac{3}{2}} - \\dfrac{1}{2}u^2\\right]_0^1$?',
                        'options': ['$\\dfrac{1}{6}$', '$\\dfrac{2}{9}$', '$\\dfrac{5}{18}$', '$\\dfrac{1}{3}$', '$\\dfrac{7}{18}$'],
                        'answer': 3,
                        'exp': '$\\left(\\dfrac{8}{9} - \\dfrac{1}{2}\\right) - \\left(\\dfrac{1}{9} - 0\\right) = \\dfrac{7}{9} - \\dfrac{1}{2} = \\dfrac{5}{18}$입니다.',
                        'exp_en': '$\\dfrac{8 - 1}{9} - \\dfrac{1}{2} = \\dfrac{7}{9} - \\dfrac{1}{2} = \\dfrac{5}{18}$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 레고 조립] 사분면별 부호 합산으로 $\\alpha$와 $90 \\times \\alpha$ 확정하기',
                'title_en': '💎 Step 5 · [Final Synthesis] Quadrant Summation for $\\alpha$ and $90 \\times \\alpha$',
                'knowledge': '$1, 2, 3, 4$사분면에서 $\\sin x \\cos x$의 부호는 $(+, -, +, -)$이므로 $\\int h_0(x)\\cos x \\, dx$는 $(+J, -J, +J, -J)$이고, 여기에 $f$의 부호 $(s_1, s_2, s_2, s_3) = (1, -1, -1, -1)$을 곱하면 사분면별 $\\int f(x)\\cos x \\, dx$는 <b>$(+J, +J, -J, +J)$</b>가 됩니다! 따라서$$\\alpha = (J + J - J + J) + J = 2J + J = 3J = \\frac{5}{6} \\implies 90 \\times \\alpha = 75$$입니다!',
                'knowledge_en': 'Multiplying quadrant integrals $(+J, -J, +J, -J)$ of $h_0(x)\\cos x$ by $(s_1, s_2, s_2, s_3) = (1, -1, -1, -1)$ gives $(+J, +J, -J, +J)$ for $f(x)\\cos x$. Adding the extra second-quadrant integral $+J$ gives $\\alpha = 2J + J = 3J = \\dfrac{5}{6}$ and $90\\alpha = 75$.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': '$\\alpha = \\displaystyle\\int_0^{2\\pi} f(x)\\cos x \\, dx + \\int_{\\frac{\\pi}{2}}^{\\pi} f(x)\\cos x \\, dx = 3J = \\dfrac{5}{6}$일 때, $90 \\times \\alpha$의 값은?',
                        'stem_en': 'Given $\\alpha = 3J = \\dfrac{5}{6}$, what is the value of $90 \\times \\alpha$?',
                        'options': ['$60$', '$65$', '$70$', '$75$', '$80$'],
                        'answer': 4,
                        'exp': '$90 \\times \\dfrac{5}{6} = 75$입니다.',
                        'exp_en': '$90 \\times \\dfrac{5}{6} = 75$.',
                    }
                ],
            },
        ],
        'final': {
            'stem': (
                '실수 전체의 집합에서 미분가능한 함수 $f(x)$에 대하여 다음 조건이 성립한다.'
                '<span style="display:block;margin:10px 0;padding:10px 14px;border:1px solid #cbd5e1;border-radius:8px;background:#f8fafc">'
                '(가) 모든 실수 $x$에 대하여<br>'
                '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$|f(x)| = |\\sin x|\\left(\\sqrt{1 + 3\\cos^2 x} - 1\\right)$<br>'
                '&nbsp;&nbsp;&nbsp;&nbsp;이다.<br>'
                '(나) $\\displaystyle\\int_0^{2\\pi} f(x) \\, dx > 0,\\quad \\int_{\\frac{\\pi}{2}}^{\\frac{3\\pi}{2}} x f(x) \\, dx > 0$'
                '</span>'
                '$\\displaystyle\\int_0^{2\\pi} f(x)\\cos x \\, dx + \\int_{\\frac{\\pi}{2}}^{\\pi} f(x)\\cos x \\, dx = \\alpha$라 할 때, $90 \\times \\alpha$의 값을 구하시오. [4점]'
            ),
            'stem_en': (
                'A function $f(x)$ differentiable on the set of all real numbers satisfies:'
                '<span style="display:block;margin:10px 0;padding:10px 14px;border:1px solid #cbd5e1;border-radius:8px;background:#f8fafc">'
                '(가) For all real numbers $x$, $|f(x)| = |\\sin x|\\left(\\sqrt{1 + 3\\cos^2 x} - 1\\right)$.<br>'
                '(나) $\\displaystyle\\int_0^{2\\pi} f(x) \\, dx > 0,\\quad \\int_{\\frac{\\pi}{2}}^{\\frac{3\\pi}{2}} x f(x) \\, dx > 0$.'
                '</span>'
                'Let $\\displaystyle\\int_0^{2\\pi} f(x)\\cos x \\, dx + \\int_{\\frac{\\pi}{2}}^{\\pi} f(x)\\cos x \\, dx = \\alpha$. Find the value of $90 \\times \\alpha$. [4 points]'
            ),
            'options': ['$60$', '$65$', '$70$', '$75$', '$80$'],
            'answer': 4,
            'exp': '$h_0(x) = \\sin x(\\sqrt{1+3\\cos^2 x}-1)$이라 하면 $h_0\'(n\\pi) \\neq 0$, $h_0\'\\left(\\dfrac{\\pi}{2}+n\\pi\\right) = 0$이므로 $\\left[0,\\dfrac{\\pi}{2}\\right], \\left[\\dfrac{\\pi}{2},\\dfrac{3\\pi}{2}\\right], \\left[\\dfrac{3\\pi}{2},2\\pi\\right]$에서 $f(x) = s_i h_0(x)$ ($s_i \\in \\{-1,1\\}$)입니다. 조건 (나)에서 $(s_1, s_2, s_3) = (1, -1, -1)$을 얻고, $J = \\int_0^{\\pi/2} h_0(x)\\cos x \\, dx = \\dfrac{5}{18}$이므로 $\\alpha = (J + J - J + J) + J = 3J = \\dfrac{5}{6}$, $90\\alpha = 75$입니다.',
            'exp_en': 'Writing $h_0(x) = \\sin x(\\sqrt{1+3\\cos^2 x}-1)$, differentiability fixes constant signs $s_1, s_2, s_3 \\in \\{-1, 1\\}$ on $[0, \\pi/2], [\\pi/2, 3\\pi/2], [3\\pi/2, 2\\pi]$. Condition (나) forces $(s_1, s_2, s_3) = (1, -1, -1)$. With $J = \\int_0^{\\pi/2} h_0(x)\\cos x \\, dx = \\dfrac{5}{18}$, we get $\\alpha = 3J = \\dfrac{5}{6}$ and $90\\alpha = 75$.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 미적분 최고난도(30번) 문항으로, <b>절댓값 방정식 $|f(x)| = |h_0(x)|$의 실수 전체 미분가능성 판정(영점에서의 미분계수 $0$ 여부)</b>과 <b>대칭성·가중 적분 부등식을 통한 구간별 부호 추론</b>, 그리고 <b>삼각 치환적분법</b>을 결합한 문항입니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: 미분가능성을 이용한 구간별 부호 구조 파악</b><br>\n'
                '  $h_0(x) = \\sin x \\left(\\sqrt{1 + 3\\cos^2 x} - 1\\right)$이라 하면 $|f(x)| = |h_0(x)|$이고, $h_0(x) = 0 \\iff x = \\dfrac{k\\pi}{2}$ ($k \\in \\mathbb{Z}$)입니다.<br>\n'
                '  • $x = n\\pi$ ($n \\in \\mathbb{Z}$)에서 $\\sqrt{1 + 3\\cos^2(n\\pi)} - 1 = 1 \\neq 0$이므로 $h_0\'(n\\pi) = (-1)^n \\neq 0$입니다. 따라서 $f$가 $x = n\\pi$에서 미분가능하려면 $x = n\\pi$ 좌우에서 $h_0(x)$ 앞의 부호가 바뀌지 않아야 합니다.<br>\n'
                '  • 반면 $x = \\dfrac{\\pi}{2} + n\\pi$에서는 $\\sqrt{1 + 3\\cos^2 x} - 1 = \\dfrac{3\\cos^2 x}{\\sqrt{1 + 3\\cos^2 x} + 1}$이므로 $h_0\'\\left(\\dfrac{\\pi}{2} + n\\pi\\right) = 0$이 되어 부호가 바뀌어도 항상 미분가능합니다.<br>\n'
                '  그러므로 구간 $\\left[0, \\dfrac{\\pi}{2}\\right], \\left[\\dfrac{\\pi}{2}, \\dfrac{3\\pi}{2}\\right], \\left[\\dfrac{3\\pi}{2}, 2\\pi\\right]$에서 각각 $f(x) = s_1 h_0(x),\\; s_2 h_0(x),\\; s_3 h_0(x)$ ($s_i \\in \\{-1, 1\\}$)로 놓을 수 있습니다.<br><br>\n'
                '  <b>2단계: 조건 (나)를 이용한 부호 $(s_1, s_2, s_3)$ 결정</b><br>\n'
                '  $I = \\displaystyle\\int_0^{\\frac{\\pi}{2}} h_0(x) \\, dx > 0$이라 하면 삼각함수의 대칭성에 의하여\n'
                '  $$\\int_0^{2\\pi} f(x) \\, dx = s_1 I + s_2(I - I) + s_3(-I) = (s_1 - s_3)I > 0 \\implies s_1 = 1,\\quad s_3 = -1$$\n'
                '  또한 $x = \\pi + t$ ($t \\in [-\\pi/2, \\pi/2]$)로 치환하면 $h_0(\\pi + t) = -h_0(t)$ (기함수)이므로\n'
                '  $$\\int_{\\frac{\\pi}{2}}^{\\frac{3\\pi}{2}} x h_0(x) \\, dx = \\int_{-\\frac{\\pi}{2}}^{\\frac{\\pi}{2}} (\\pi + t)\\bigl(-h_0(t)\\bigr) dt = -2\\int_0^{\\frac{\\pi}{2}} t h_0(t) \\, dt < 0$$\n'
                '  입니다. 따라서 $\\displaystyle\\int_{\\frac{\\pi}{2}}^{\\frac{3\\pi}{2}} x f(x) \\, dx = s_2 \\int_{\\frac{\\pi}{2}}^{\\frac{3\\pi}{2}} x h_0(x) \\, dx > 0$에서 <b>$s_2 = -1$</b>입니다.<br><br>\n'
                '  <b>3단계: 기본 정적분 $J$ 계산 및 $90\\alpha$ 도출</b><br>\n'
                '  $u = \\cos x$로 치환하면\n'
                '  $$J = \\int_0^{\\frac{\\pi}{2}} \\sin x \\cos x \\left(\\sqrt{1 + 3\\cos^2 x} - 1\\right) dx = \\int_0^1 u\\left(\\sqrt{1 + 3u^2} - 1\\right) du = \\left[\\frac{(1 + 3u^2)^{\\frac{3}{2}}}{9} - \\frac{u^2}{2}\\right]_0^1 = \\frac{8 - 1}{9} - \\frac{1}{2} = \\frac{5}{18}$$\n'
                '  $1, 2, 3, 4$사분면에서 $\\int h_0(x)\\cos x \\, dx$는 차례로 $(+J, -J, +J, -J)$이고 $(s_1, s_2, s_2, s_3) = (1, -1, -1, -1)$을 곱하면 $\\int f(x)\\cos x \\, dx$는 차례로 $(+J, +J, -J, +J)$입니다. 따라서\n'
                '  $$\\alpha = (J + J - J + J) + J = 3J = 3 \\times \\frac{5}{18} = \\frac{5}{6} \\implies 90 \\times \\alpha = 75$$\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>\n'
                '  $x = n\\pi$에서는 단순 영점($h_0\' \\neq 0$)이라 부호가 고정되고, $x = \\dfrac{\\pi}{2} + n\\pi$에서는 이중 영점($h_0\' = 0$)이라 부호 전환이 가능하다는 관찰이 30번 해결의 핵심입니다. 정답은 <b>$75$</b>입니다.\n'
                '</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis &amp; Core Concepts]</h4>\n'
                '<p>This flagship #30 Calculus item synthesizes <b>global differentiability of $|f(x)| = |h_0(x)|$</b>, <b>symmetry &amp; weighted integral sign deduction</b>, and <b>trigonometric $u$-substitution</b>.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Sign-switching structure</b><br>\n'
                '  Let $h_0(x) = \\sin x (\\sqrt{1 + 3\\cos^2 x} - 1)$. At $x = n\\pi$, $h_0\'(n\\pi) = (-1)^n \\neq 0$, forbidding sign flips; at $x = \\dfrac{\\pi}{2} + n\\pi$, $\\sqrt{1+3\\cos^2 x} - 1 \\sim \\dfrac{3}{2}\\cos^2 x$ gives $h_0\' = 0$, allowing free sign selection. Hence on $[0, \\pi/2]$, $[\\pi/2, 3\\pi/2]$, and $[3\\pi/2, 2\\pi]$, $f(x) = s_i h_0(x)$ with $s_1, s_2, s_3 \\in \\{-1, 1\\}$.<br><br>\n'
                '  <b>Step 2: Determining $(s_1, s_2, s_3)$ from (나)</b><br>\n'
                '  With $I = \\int_0^{\\pi/2} h_0(x)dx > 0$, $\\int_0^{2\\pi} f(x)dx = (s_1 - s_3)I > 0 \\implies s_1 = 1,\\; s_3 = -1$. Substituting $x = \\pi + t$ shows $\\int_{\\pi/2}^{3\\pi/2} x h_0(x)dx = -2\\int_0^{\\pi/2} t h_0(t)dt < 0$, so $\\int_{\\pi/2}^{3\\pi/2} x f(x)dx > 0 \\implies s_2 = -1$.<br><br>\n'
                '  <b>Step 3: Evaluating $J$ and $90\\alpha$</b><br>\n'
                '  Setting $u = \\cos x$ gives $J = \\int_0^1 u(\\sqrt{1+3u^2} - 1)du = \\left[\\dfrac{(1+3u^2)^{3/2}}{9} - \\dfrac{u^2}{2}\\right]_0^1 = \\dfrac{7}{9} - \\dfrac{1}{2} = \\dfrac{5}{18}$. Across the four quadrants, $\\int f(x)\\cos x \\, dx$ equals $(+J, +J, -J, +J)$, whence\n'
                '  $$\\alpha = (J + J - J + J) + J = 3J = \\frac{5}{6} \\implies 90 \\times \\alpha = 75.$$\n'
                '</p>\n\n'
                '<h4>✨ [Final Answer &amp; Practical Tips]</h4>\n'
                '<p>\n'
                '  Distinguishing simple zeros ($x = n\\pi$) from higher-order zeros ($x = \\pi/2 + n\\pi$) immediately unlocks the sign structure. Final answer: <b>$75$</b>.\n'
                '</p>'
            ),
        },
    },
]
