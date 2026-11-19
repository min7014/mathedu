# -*- coding: utf-8 -*-
"""
csat2027_part1_common1.py
2027학년도 대학수학능력시험 수학 영역 공통 1~11번 (csat27_01 ~ csat27_11)
"""

PART1_PROBLEMS = [
    {
        'slug': 'csat27_01',
        'qNum': '1',
        'points': 2,
        'is_short_answer': False,
        'subject': '공통(수학I·II)',
        'title': '[2027학년도 수능 고3 공통 1번] 거듭제곱근과 유리수 지수법칙 계산',
        'title_en': '[2027 CSAT Math Common #1] Radicals and Rational Exponent Rules',
        'summary_ko': '세제곱근 $\\sqrt[3]{32}$와 $4^{-\\frac{1}{3}}$의 밑을 $2$로 통일하여 지수법칙으로 계산하기',
        'summary_en': 'Unify the bases of $\\sqrt[3]{32}$ and $4^{-\\frac{1}{3}}$ to $2$ and evaluate using rational exponent laws.',
        'tags': ['2027학년도 수능', '공통(수학I·II)', '수학I', '지수와로그', '거듭제곱근', '지수법칙', '1번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': '$\\sqrt[3]{a^m} = a^{\\frac{m}{3}}$',
                'desc': '세제곱근 기호는 지수의 분모 $3$으로 바꾸어 분수 지수로 표현',
                'desc_en': 'A cube root converts into a fractional exponent with denominator $3$.',
            },
            {
                'sym': '$32 = 2^5,\\; 4 = 2^2$',
                'desc': '$32$와 $4$를 모두 소수 밑 $2$의 거듭제곱으로 통일',
                'desc_en': 'Express composite numbers $32$ and $4$ as powers of base $2$.',
            },
            {
                'sym': '$(a^m)^n = a^{mn}$',
                'desc': '거듭제곱의 거듭제곱은 괄호 안팎의 지수끼리 곱하기',
                'desc_en': 'Power of a power rule: multiply the inner and outer exponents.',
            },
            {
                'sym': '$a^p \\times a^q = a^{p+q}$',
                'desc': '밑이 같은 거듭제곱의 곱셈은 지수끼리 더하기',
                'desc_en': 'Product of powers with the same base: add the exponents.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 기초 직관] $2$를 몇 번 곱하면 $32$가 될까?',
                'title_en': '🔰 Step 1 · [Elementary Intuition] How many $2$s multiply to $32$?',
                'knowledge': '초등학교 곱셈으로 $2$를 차례대로 곱해 보면 $2 \\times 2 = 4$, $4 \\times 2 = 8$, $8 \\times 2 = 16$, $16 \\times 2 = 32$입니다. 즉 $32$는 $2$를 $5$번 곱한 수($2^5$)입니다.',
                'knowledge_en': 'Multiplying $2$ repeatedly gives $2, 4, 8, 16, 32$. Thus $32$ is the product of five $2$s, written as $2^5$.',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '초등학교 곱셈에서 $2$를 여러 번 곱할 때, $32$가 되려면 $2$를 모두 몇 번 곱해야 할까요? ($32 = 2^k$에서 $k$의 값)',
                        'stem_en': 'How many times must $2$ be multiplied by itself to obtain $32$ (i.e., what is $k$ in $32 = 2^k$)?',
                        'options': ['$3$', '$4$', '$5$', '$6$', '$7$'],
                        'answer': 3,
                        'exp': '$2 \\times 2 \\times 2 \\times 2 \\times 2 = 32$이므로 $32 = 2^5$, 따라서 $k = 5$입니다.',
                        'exp_en': 'Since $2 \\times 2 \\times 2 \\times 2 \\times 2 = 32$, we have $32 = 2^5$, so $k = 5$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [기호 번역] $\\sqrt[3]{32}$를 분수 지수로 바꾸기',
                'title_en': '🌿 Step 2 · [Symbol Translation] Rewriting $\\sqrt[3]{32}$ as a fractional exponent',
                'knowledge': '거듭제곱근 약속 $\\sqrt[3]{2^m} = 2^{\\frac{m}{3}}$에 따라 근호 왼쪽 위의 작은 숫자 $3$은 지수의 분모로 내려갑니다. 앞서 구한 $32 = 2^5$을 대입해 봅시다.',
                'knowledge_en': 'By the rational exponent rule $\\sqrt[3]{2^m} = 2^{\\frac{m}{3}}$, the root index $3$ becomes the denominator of the exponent.',
                'questions': [
                    {
                        'level_label': '기호 번역 디딤돌 2',
                        'level_label_en': 'Symbol Translation Step 2',
                        'stem': '$32 = 2^5$임을 이용하여 $\\sqrt[3]{32}$를 밑이 $2$인 분수 지수 꼴로 바르게 나타낸 것은?',
                        'stem_en': 'Using $32 = 2^5$, which expression correctly represents $\\sqrt[3]{32}$ with base $2$?',
                        'options': ['$2^{\\frac{3}{5}}$', '$2^{\\frac{4}{3}}$', '$2^{\\frac{5}{3}}$', '$2^{\\frac{5}{2}}$', '$2^3$'],
                        'answer': 3,
                        'exp': '$\\sqrt[3]{32} = \\sqrt[3]{2^5} = 2^{\\frac{5}{3}}$입니다.',
                        'exp_en': '$\\sqrt[3]{32} = \\sqrt[3]{2^5} = 2^{\\frac{5}{3}}$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [핵심 관계식 (가)] $4^{-\\frac{1}{3}}$의 밑을 $2$로 바꾸기',
                'title_en': '🌱 Step 3 · [Core Relation A] Converting $4^{-\\frac{1}{3}}$ to base $2$',
                'knowledge': '$4 = 2^2$이므로 $4^{-\\frac{1}{3}} = (2^2)^{-\\frac{1}{3}}$입니다. 거듭제곱의 거듭제곱 법칙 $(a^m)^n = a^{mn}$에 따라 두 지수 $2$와 $-\\frac{1}{3}$을 곱합니다.',
                'knowledge_en': 'Since $4 = 2^2$, we have $4^{-\\frac{1}{3}} = (2^2)^{-\\frac{1}{3}}$. Multiply the exponents $2$ and $-\\frac{1}{3}$.',
                'questions': [
                    {
                        'level_label': '핵심 관계식 (가) 디딤돌 3',
                        'level_label_en': 'Core Relation A Step 3',
                        'stem': '$4 = 2^2$을 이용하여 $4^{-\\frac{1}{3}}$을 밑이 $2$인 거듭제곱으로 바르게 나타낸 것은?',
                        'stem_en': 'Using $4 = 2^2$, how is $4^{-\\frac{1}{3}}$ written as a power of $2$?',
                        'options': ['$2^{-\\frac{1}{6}}$', '$2^{-\\frac{1}{3}}$', '$2^{-\\frac{2}{3}}$', '$2^{\\frac{2}{3}}$', '$2^{-\\frac{4}{3}}$'],
                        'answer': 3,
                        'exp': '$(2^2)^{-\\frac{1}{3}} = 2^{2 \\times \\left(-\\frac{1}{3}\\right)} = 2^{-\\frac{2}{3}}$입니다.',
                        'exp_en': '$(2^2)^{-\\frac{1}{3}} = 2^{2 \\times \\left(-\\frac{1}{3}\\right)} = 2^{-\\frac{2}{3}}$.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [중간 전개 (나)] 지수끼리 더하여 분수 계산하기',
                'title_en': '🌳 Step 4 · [Intermediate Step B] Adding the fractional exponents',
                'knowledge': '밑이 $2$로 같으므로 곱셈 $2^{\\frac{5}{3}} \\times 2^{-\\frac{2}{3}}$에서는 지수끼리 더합니다: $\\frac{5}{3} + \\left(-\\frac{2}{3}\\right) = \\frac{5 - 2}{3}$.',
                'knowledge_en': 'When multiplying powers with the same base $2$, add their exponents: $\\frac{5}{3} + \\left(-\\frac{2}{3}\\right) = \\frac{5 - 2}{3}$.',
                'questions': [
                    {
                        'level_label': '중간 전개 (나) 디딤돌 4',
                        'level_label_en': 'Intermediate Step B Step 4',
                        'stem': '$2^{\\frac{5}{3}} \\times 2^{-\\frac{2}{3}} = 2^p$에서 지수 $p = \\dfrac{5}{3} - \\dfrac{2}{3}$를 계산한 값은?',
                        'stem_en': 'In $2^{\\frac{5}{3}} \\times 2^{-\\frac{2}{3}} = 2^p$, what is the value of $p = \\dfrac{5}{3} - \\dfrac{2}{3}$?',
                        'options': ['$-1$', '$\\dfrac{1}{3}$', '$1$', '$\\dfrac{4}{3}$', '$3$'],
                        'answer': 3,
                        'exp': '분모가 $3$으로 같으므로 $\\dfrac{5 - 2}{3} = \\dfrac{3}{3} = 1$입니다.',
                        'exp_en': 'With common denominator $3$, $\\dfrac{5 - 2}{3} = \\dfrac{3}{3} = 1$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 레고 조립] 최종 거듭제곱 값 확정하기',
                'title_en': '💎 Step 5 · [Final LEGO Assembly] Evaluating the final power',
                'knowledge': '앞선 조각들을 합치면 주어진 식 전체는 $2^1$로 간단히 정리됩니다. 어떤 수의 $1$제곱은 자기 자신과 같습니다.',
                'knowledge_en': 'Combining all previous steps simplifies the entire expression to $2^1$, which equals $2$.',
                'questions': [
                    {
                        'level_label': '최종 레고 조립 디딤돌 5',
                        'level_label_en': 'Final LEGO Assembly Step 5',
                        'stem': '따라서 $\\sqrt[3]{32} \\times 4^{-\\frac{1}{3}} = 2^1$의 최종 값은?',
                        'stem_en': 'What is the final value of $\\sqrt[3]{32} \\times 4^{-\\frac{1}{3}} = 2^1$?',
                        'options': ['$1$', '$2$', '$3$', '$4$', '$5$'],
                        'answer': 2,
                        'exp': '$2^1 = 2$이므로 구하는 값은 $2$입니다.',
                        'exp_en': 'Since $2^1 = 2$, the final value is $2$.',
                    }
                ],
            },
        ],
        'final': {
            'stem': '$\\sqrt[3]{32} \\times 4^{-\\frac{1}{3}}$ 의 값은? [2점]',
            'stem_en': 'What is the value of $\\sqrt[3]{32} \\times 4^{-\\frac{1}{3}}$? [2 points]',
            'options': ['$1$', '$2$', '$3$', '$4$', '$5$'],
            'answer': 2,
            'exp': '$\\sqrt[3]{32} \\times 4^{-\\frac{1}{3}} = 2^{\\frac{5}{3}} \\times (2^2)^{-\\frac{1}{3}} = 2^{\\frac{5}{3} - \\frac{2}{3}} = 2^1 = 2$ 이므로 정답은 ②입니다.',
            'exp_en': '$\\sqrt[3]{32} \\times 4^{-\\frac{1}{3}} = 2^{\\frac{5}{3}} \\times 2^{-\\frac{2}{3}} = 2^1 = 2$. The correct answer is ②.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 <b>거듭제곱근의 성질과 유리수 지수법칙</b>을 활용하여 식의 값을 정확하게 계산할 수 있는지를 평가하는 수학Ⅰ의 대표 기초 문항입니다. '
                '합성수인 $32$와 $4$를 모두 소수 밑 $2$의 거듭제곱으로 통일하면 분수 지수의 덧셈·뺄셈만으로 즉시 해결됩니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: 세제곱근을 밑이 $2$인 분수 지수로 변환하기</b><br>\n'
                '  $32 = 2^5$이므로 거듭제곱근과 유리수 지수의 관계 $\\sqrt[n]{a^m} = a^{\\frac{m}{n}}$에 의하여 다음을 얻습니다:<br>\n'
                '  $$\\sqrt[3]{32} = \\sqrt[3]{2^5} = 2^{\\frac{5}{3}}$$<br>\n'
                '  <b>2단계: $4^{-\\frac{1}{3}}$의 밑을 $2$로 통일하기</b><br>\n'
                '  $4 = 2^2$이므로 지수법칙 $(a^m)^n = a^{mn}$을 적용합니다:<br>\n'
                '  $$4^{-\\frac{1}{3}} = (2^2)^{-\\frac{1}{3}} = 2^{2 \\times \\left(-\\frac{1}{3}\\right)} = 2^{-\\frac{2}{3}}$$<br>\n'
                '  <b>3단계: 밑이 같은 거듭제곱의 곱셈</b><br>\n'
                '  지수법칙 $a^p \\times a^q = a^{p+q}$에 의하여 지수끼리 더합니다:<br>\n'
                '  $$2^{\\frac{5}{3}} \\times 2^{-\\frac{2}{3}} = 2^{\\frac{5}{3} - \\frac{2}{3}} = 2^{\\frac{3}{3}} = 2^1 = 2$$\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>\n'
                '  따라서 주어진 식의 값은 $2$이며, 정답은 <b>②번</b>입니다.<br>\n'
                '  💡 <b>실전 팁</b>: $32 = 2^5$, $64 = 2^6$, $27 = 3^3$, $81 = 3^4$ 등 자주 등장하는 거듭제곱수를 즉시 소수 밑으로 바꾸면 부호 및 약분 실수를 완벽히 예방할 수 있습니다.\n'
                '</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                '<p>This problem evaluates fluency with <b>radicals and rational exponent rules</b>. '
                'By rewriting both composite numbers $32$ and $4$ as powers of the prime base $2$, the product reduces to elementary fraction arithmetic in the exponent.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Convert the cube root into a fractional exponent</b><br>\n'
                '  Since $32 = 2^5$, applying $\\sqrt[n]{a^m} = a^{\\frac{m}{n}}$ yields:<br>\n'
                '  $$\\sqrt[3]{32} = \\sqrt[3]{2^5} = 2^{\\frac{5}{3}}$$<br>\n'
                '  <b>Step 2: Unify the second factor to base $2$</b><br>\n'
                '  Since $4 = 2^2$, the power-of-a-power rule $(a^m)^n = a^{mn}$ gives:<br>\n'
                '  $$4^{-\\frac{1}{3}} = (2^2)^{-\\frac{1}{3}} = 2^{-\\frac{2}{3}}$$<br>\n'
                '  <b>Step 3: Multiply powers with the same base</b><br>\n'
                '  $$2^{\\frac{5}{3}} \\times 2^{-\\frac{2}{3}} = 2^{\\frac{5}{3} - \\frac{2}{3}} = 2^1 = 2$$\n'
                '</p>\n\n'
                '<h4>✨ [Conclusion & Key Takeaway]</h4>\n'
                '<p>\n'
                '  The value of the expression is $2$, which corresponds to <b>Option ②</b>.\n'
                '</p>'
            ),
        },
    },
    {
        'slug': 'csat27_02',
        'qNum': '2',
        'points': 2,
        'is_short_answer': False,
        'subject': '공통(수학I·II)',
        'title': '[2027학년도 수능 고3 공통 2번] 미분계수의 정의와 다항함수의 도함수',
        'title_en': '[2027 CSAT Math Common #2] Definition of Derivative and Polynomial Differentiation',
        'summary_ko': '미분계수의 정의식 $\\lim_{h\\to 0}\\frac{f(1+h)-f(1)}{h}=f\'(1)$을 인식하고 다항함수 미분법으로 계산하기',
        'summary_en': 'Recognize the limit $\\lim_{h\\to 0}\\frac{f(1+h)-f(1)}{h}$ as $f\'(1)$ and evaluate using the power rule.',
        'tags': ['2027학년도 수능', '공통(수학I·II)', '수학II', '미분', '미분계수', '도함수', '2번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': "$f'(1) = \\lim_{h \\to 0} \\dfrac{f(1+h)-f(1)}{h}$",
                'desc': '$x = 1$에서의 순간변화율(미분계수)을 뜻하는 정의식',
                'desc_en': 'Limit definition of the derivative (instantaneous rate of change) at $x = 1$.',
            },
            {
                'sym': "$(x^n)' = nx^{n-1}$",
                'desc': '지수 $n$이 앞으로 내려와 곱해지고 지수가 $1$ 줄어드는 미분 공식',
                'desc_en': 'Power rule for differentiation: bring down the exponent $n$ and subtract $1$ from the power.',
            },
            {
                'sym': "$(cx)' = c$",
                'desc': '일차항 $cx$를 미분하면 $x$ 앞의 계수 $c$만 남음',
                'desc_en': 'The derivative of a linear term $cx$ is its constant coefficient $c$.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 기초 직관] $x = 1$을 식 $8 \\times x \\times x \\times x + 2$에 넣어 계산하기',
                'title_en': '🔰 Step 1 · [Elementary Intuition] Evaluating $8 \\times 1 \\times 1 \\times 1 + 2$',
                'knowledge': '$1$은 몇 번을 곱해도 항상 $1$입니다($1 \\times 1 \\times 1 = 1$). 따라서 $8 \\times 1 + 2$를 초등학교 사칙연산으로 가볍게 계산할 수 있습니다.',
                'knowledge_en': 'Multiplying $1$ by itself any number of times always gives $1$. Thus $8 \\times 1^3 + 2$ reduces to simple addition.',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '초등학교 곱셈과 덧셈에서 $8 \\times 1 \\times 1 \\times 1 + 2$를 계산한 값은?',
                        'stem_en': 'Using elementary multiplication and addition, what is $8 \\times 1 \\times 1 \\times 1 + 2$?',
                        'options': ['$6$', '$7$', '$8$', '$9$', '$10$'],
                        'answer': 5,
                        'exp': '$1 \\times 1 \\times 1 = 1$이므로 $8 \\times 1 + 2 = 8 + 2 = 10$입니다.',
                        'exp_en': 'Since $1 \\times 1 \\times 1 = 1$, we get $8 \\times 1 + 2 = 10$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [기호 번역] 극한식을 미분계수 기호로 번역하기',
                'title_en': '🌿 Step 2 · [Symbol Translation] Translating the limit into derivative notation',
                'knowledge': '평균변화율 $\\dfrac{f(1+h)-f(1)}{h}$에서 간격 $h$를 $0$에 한없이 가깝게 보내는 극한을 $x = 1$에서의 미분계수라 부르고 $f\'(1)$이라고 적습니다.',
                'knowledge_en': 'Taking the limit of the difference quotient $\\dfrac{f(1+h)-f(1)}{h}$ as $h \\to 0$ defines the derivative $f\'(1)$.',
                'questions': [
                    {
                        'level_label': '기호 번역 디딤돌 2',
                        'level_label_en': 'Symbol Translation Step 2',
                        'stem': '극한식 $\\lim_{h \\to 0} \\dfrac{f(1+h)-f(1)}{h}$를 미분계수 기호로 바르게 나타낸 것은?',
                        'stem_en': 'Which derivative symbol equals $\\lim_{h \\to 0} \\dfrac{f(1+h)-f(1)}{h}$?',
                        'options': ['$f(0)$', '$f(1)$', "$f'(0)$", "$f'(1)$", "$2f'(1)$"],
                        'answer': 4,
                        'exp': '미분계수의 정의 $\\lim_{h \\to 0} \\dfrac{f(a+h)-f(a)}{h} = f\'(a)$에서 $a = 1$이므로 $f\'(1)$입니다.',
                        'exp_en': 'By definition $\\lim_{h \\to 0} \\dfrac{f(a+h)-f(a)}{h} = f\'(a)$ with $a = 1$, this equals $f\'(1)$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [핵심 관계식 (가)] 사차항 $2x^4$ 미분하기',
                'title_en': '🌱 Step 3 · [Core Relation A] Differentiating the quartic term $2x^4$',
                'knowledge': '다항함수의 미분법 $(cx^n)\' = c \\cdot n x^{n-1}$에 따라 $2x^4$에서 지수 $4$가 내려와 앞의 계수 $2$와 곱해지고, 지수는 $4 - 1 = 3$이 됩니다.',
                'knowledge_en': 'By $(cx^n)\' = cnx^{n-1}$, bring down the exponent $4$ to multiply $2$, and reduce the exponent to $4 - 1 = 3$.',
                'questions': [
                    {
                        'level_label': '핵심 관계식 (가) 디딤돌 3',
                        'level_label_en': 'Core Relation A Step 3',
                        'stem': '거듭제곱의 미분 공식에 따라 $2x^4$을 $x$에 대하여 미분한 식은?',
                        'stem_en': 'What is the derivative of $2x^4$ with respect to $x$?',
                        'options': ['$4x^3$', '$6x^3$', '$8x^3$', '$8x^4$', '$2x^3$'],
                        'answer': 3,
                        'exp': '$(2x^4)\' = 2 \\times 4x^{4-1} = 8x^3$입니다.',
                        'exp_en': '$(2x^4)\' = 2 \\times 4x^{4-1} = 8x^3$.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [중간 전개 (나)] 도함수 $f\'(x)$ 전체 식 완성하기',
                'title_en': '🌳 Step 4 · [Intermediate Step B] Completing the derivative $f\'(x)$',
                'knowledge': '합의 미분법에 따라 각 항을 따로 미분하여 더합니다. $(2x^4)\' = 8x^3$이고, 일차항 $(2x)\' = 2$입니다.',
                'knowledge_en': 'Differentiate term by term: $(2x^4)\' = 8x^3$ and $(2x)\' = 2$.',
                'questions': [
                    {
                        'level_label': '중간 전개 (나) 디딤돌 4',
                        'level_label_en': 'Intermediate Step B Step 4',
                        'stem': '함수 $f(x) = 2x^4 + 2x$의 도함수 $f\'(x)$를 바르게 구한 것은?',
                        'stem_en': 'What is the derivative $f\'(x)$ of $f(x) = 2x^4 + 2x$?',
                        'options': ['$4x^3 + 2$', '$8x^3 + 1$', '$8x^3 + 2$', '$8x^3 + 2x$', '$6x^3 + 2$'],
                        'answer': 3,
                        'exp': '$f\'(x) = (2x^4)\' + (2x)\' = 8x^3 + 2$입니다.',
                        'exp_en': '$f\'(x) = (2x^4)\' + (2x)\' = 8x^3 + 2$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 레고 조립] $x = 1$을 대입해 $f\'(1)$ 확정하기',
                'title_en': '💎 Step 5 · [Final LEGO Assembly] Substituting $x = 1$ into $f\'(x)$',
                'knowledge': '도함수 $f\'(x) = 8x^3 + 2$에 $x = 1$을 대입하면 문제에서 요구하는 극한값 $f\'(1)$이 도출됩니다.',
                'knowledge_en': 'Substituting $x = 1$ into $f\'(x) = 8x^3 + 2$ gives the desired limit $f\'(1)$.',
                'questions': [
                    {
                        'level_label': '최종 레고 조립 디딤돌 5',
                        'level_label_en': 'Final LEGO Assembly Step 5',
                        'stem': '도함수 $f\'(x) = 8x^3 + 2$에서 $f\'(1)$의 값은?',
                        'stem_en': 'Given $f\'(x) = 8x^3 + 2$, what is the value of $f\'(1)$?',
                        'options': ['$6$', '$7$', '$8$', '$9$', '$10$'],
                        'answer': 5,
                        'exp': '$f\'(1) = 8 \\times 1^3 + 2 = 8 + 2 = 10$입니다.',
                        'exp_en': '$f\'(1) = 8(1)^3 + 2 = 10$.',
                    }
                ],
            },
        ],
        'final': {
            'stem': '함수 $f(x)=2x^4+2x$에 대하여 $\\lim_{h \\to 0} \\dfrac{f(1+h)-f(1)}{h}$ 의 값은? [2점]',
            'stem_en': 'For the function $f(x)=2x^4+2x$, what is the value of $\\lim_{h \\to 0} \\dfrac{f(1+h)-f(1)}{h}$? [2 points]',
            'options': ['$6$', '$7$', '$8$', '$9$', '$10$'],
            'answer': 5,
            'exp': '미분계수의 정의에 의해 주어진 극한값은 $f\'(1)$이고, $f\'(x)=8x^3+2$이므로 $f\'(1)=8+2=10$입니다. 정답은 ⑤입니다.',
            'exp_en': 'By the definition of the derivative, the limit equals $f\'(1)$. Since $f\'(x)=8x^3+2$, we get $f\'(1)=8(1)^3+2=10$. The correct answer is ⑤.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 <b>미분계수의 정의</b>와 <b>다항함수의 미분법</b>을 정확히 연결하여 계산할 수 있는지를 평가합니다. '
                '$h \\to 0$일 때의 평균변화율의 극한을 직접 전개할 필요 없이 $f\'(1)$로 바꾸어 도함수로 해결하는 것이 핵심입니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: 미분계수의 정의 적용</b><br>\n'
                '  함수 $f(x)$는 다항함수이므로 실수 전체에서 미분가능합니다. 따라서 미분계수의 정의에 의하여 다음이 성립합니다:<br>\n'
                '  $$\\lim_{h \\to 0} \\frac{f(1+h)-f(1)}{h} = f\'(1)$$<br>\n'
                '  <b>2단계: 도함수 $f\'(x)$ 구하기</b><br>\n'
                '  $f(x) = 2x^4 + 2x$의 양변을 $x$에 대하여 미분합니다:<br>\n'
                '  $$f\'(x) = 2 \\cdot 4x^3 + 2 = 8x^3 + 2$$<br>\n'
                '  <b>3단계: $x = 1$ 대입</b><br>\n'
                '  $$f\'(1) = 8 \\times 1^3 + 2 = 10$$\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>\n'
                '  따라서 구하는 극한값은 $10$이며, 정답은 <b>⑤번</b>입니다.<br>\n'
                '  💡 <b>실전 팁</b>: 분자의 $1+h$에서 $h$ 앞의 계수가 $1$인지 꼭 확인하세요. 만약 $\\dfrac{f(1+kh)-f(1)}{h}$ 꼴이라면 $k f\'(1)$이 됩니다.\n'
                '</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                '<p>This problem assesses understanding of the <b>limit definition of the derivative</b> together with the <b>power rule for polynomials</b>. '
                'Instead of expanding $(1+h)^4$, we recognize the difference quotient limit directly as $f\'(1)$.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Identify the limit as a derivative at $x = 1$</b><br>\n'
                '  $$\\lim_{h \\to 0} \\frac{f(1+h)-f(1)}{h} = f\'(1)$$<br>\n'
                '  <b>Step 2: Differentiate $f(x) = 2x^4 + 2x$</b><br>\n'
                '  Applying the power rule term by term gives:<br>\n'
                '  $$f\'(x) = 8x^3 + 2$$<br>\n'
                '  <b>Step 3: Evaluate at $x = 1$</b><br>\n'
                '  $$f\'(1) = 8(1)^3 + 2 = 10$$\n'
                '</p>\n\n'
                '<h4>✨ [Conclusion & Key Takeaway]</h4>\n'
                '<p>\n'
                '  The value of the limit is $10$, which corresponds to <b>Option ⑤</b>.\n'
                '</p>'
            ),
        },
    },
    {
        'slug': 'csat27_03',
        'qNum': '3',
        'points': 3,
        'is_short_answer': False,
        'subject': '공통(수학I·II)',
        'title': '[2027학년도 수능 고3 공통 3번] 등비수열의 일반항과 거듭제곱 공비 관계',
        'title_en': '[2027 CSAT Math Common #3] General Term and Common Ratio of a Geometric Sequence',
        'summary_ko': '$a_5=3a_3$에서 두 칸 공비 $r^2=3$을 구하고 $a_7=a_1(r^2)^3$으로 제$7$항 도출하기',
        'summary_en': 'Find $r^2 = 3$ from $a_5 = 3a_3$ and compute $a_7 = a_1 (r^2)^3 = 27$.',
        'tags': ['2027학년도 수능', '공통(수학I·II)', '수학I', '수열', '등비수열', '일반항', '3번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': '$a_n = a_1 r^{n-1}$',
                'desc': '첫째항 $a_1$에 공비 $r$를 $(n-1)$번 곱한 등비수열의 제$n$항',
                'desc_en': 'General term of a geometric sequence with first term $a_1$ and common ratio $r$.',
            },
            {
                'sym': '$a_5 = a_3 \\cdot r^2$',
                'desc': '제$3$항에서 제$5$항까지는 두 칸 차이이므로 공비를 두 번($r^2$) 곱함',
                'desc_en': 'Moving two steps forward from $a_3$ to $a_5$ multiplies by $r^2$.',
            },
            {
                'sym': '$a_7 = a_1 (r^2)^3$',
                'desc': '제$1$항에서 제$7$항까지는 여섯 칸 차이이므로 $r^2$을 세 번 곱함',
                'desc_en': 'Moving six steps from $a_1$ to $a_7$ multiplies by $r^6 = (r^2)^3$.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 기초 직관] 두 칸 갈 때마다 $3$배씩 커지는 징검다리 규칙',
                'title_en': '🔰 Step 1 · [Elementary Intuition] Stepping Stones Multiplying by $3$ Every Two Steps',
                'knowledge': '$1$번 돌의 숫자가 $1$이고, 두 칸 건너갈 때마다 숫자가 $3$배씩 커진다고 상상해 봅시다. $1$번($1$) $\\to$ $3$번($3$) $\\to$ $5$번($9$) $\\to$ $7$번 돌에는 어떤 숫자가 적혀 있을까요?',
                'knowledge_en': 'Start at stone #1 with value $1$. Every jump of $2$ stones multiplies the number by $3$: stone #1 ($1$) $\\to$ #3 ($3$) $\\to$ #5 ($9$) $\\to$ #7 ($?$).',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '$1$에서 출발하여 $3$을 세 번 차례대로 곱한 값 $1 \\times 3 \\times 3 \\times 3$은 얼마인가요?',
                        'stem_en': 'Starting from $1$ and multiplying by $3$ three times, what is $1 \\times 3 \\times 3 \\times 3$?',
                        'options': ['$9$', '$12$', '$18$', '$27$', '$81$'],
                        'answer': 4,
                        'exp': '$1 \\times 3 = 3$, $3 \\times 3 = 9$, $9 \\times 3 = 27$입니다.',
                        'exp_en': '$1 \\times 3 = 3$, $3 \\times 3 = 9$, and $9 \\times 3 = 27$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [기호 번역] $a_5$를 $a_3$과 공비 $r$로 나타내기',
                'title_en': '🌿 Step 2 · [Symbol Translation] Expressing $a_5$ in terms of $a_3$ and $r$',
                'knowledge': '등비수열 $\\{a_n\\}$의 공비를 $r$라 하면 한 칸 갈 때마다 $r$를 곱합니다. 따라서 제$3$항 $a_3$에서 제$5$항 $a_5$까지는 $5 - 3 = 2$칸 차이입니다.',
                'knowledge_en': 'In a geometric sequence with common ratio $r$, advancing from $a_3$ to $a_5$ advances $5 - 3 = 2$ indices.',
                'questions': [
                    {
                        'level_label': '기호 번역 디딤돌 2',
                        'level_label_en': 'Symbol Translation Step 2',
                        'stem': '공비가 $r$인 등비수열 $\\{a_n\\}$에서 $a_5$를 $a_3$을 사용하여 바르게 나타낸 것은?',
                        'stem_en': 'In a geometric sequence with common ratio $r$, how is $a_5$ expressed in terms of $a_3$?',
                        'options': ['$a_3 + 2r$', '$a_3 r$', '$a_3 r^2$', '$a_3 r^3$', '$a_3 r^5$'],
                        'answer': 3,
                        'exp': '$a_5 = a_1 r^4 = (a_1 r^2) \\cdot r^2 = a_3 r^2$입니다.',
                        'exp_en': '$a_5 = a_1 r^4 = (a_1 r^2) r^2 = a_3 r^2$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [핵심 관계식 (가)] $a_5 = 3a_3$에서 $r^2$의 값 구하기',
                'title_en': '🌱 Step 3 · [Core Relation A] Finding $r^2$ from $a_5 = 3a_3$',
                'knowledge': '모든 항이 양수이므로 $a_3 > 0$입니다. 등식 $a_3 r^2 = 3a_3$의 양변을 $a_3$으로 나누면 굳이 $r$ 자체의 근호를 풀지 않고도 $r^2$을 바로 알 수 있습니다.',
                'knowledge_en': 'Since all terms are positive, $a_3 > 0$. Dividing both sides of $a_3 r^2 = 3a_3$ by $a_3$ directly gives $r^2$.',
                'questions': [
                    {
                        'level_label': '핵심 관계식 (가) 디딤돌 3',
                        'level_label_en': 'Core Relation A Step 3',
                        'stem': '모든 항이 양수인 등비수열에서 $a_5 = 3a_3$일 때, 공비의 제곱 $r^2$의 값은?',
                        'stem_en': 'When all terms are positive and $a_5 = 3a_3$, what is the value of $r^2$?',
                        'options': ['$\\sqrt{3}$', '$2$', '$3$', '$6$', '$9$'],
                        'answer': 3,
                        'exp': '$a_3 r^2 = 3a_3$에서 $a_3 > 0$이므로 양변을 $a_3$으로 나누면 $r^2 = 3$입니다.',
                        'exp_en': 'Dividing $a_3 r^2 = 3a_3$ by $a_3 > 0$ gives $r^2 = 3$.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [중간 전개 (나)] $a_7$을 $a_1$과 $r^2$의 거듭제곱으로 묶기',
                'title_en': '🌳 Step 4 · [Intermediate Step B] Rewriting $a_7$ using $a_1$ and $r^2$',
                'knowledge': '일반항 공식에 의해 $a_7 = a_1 r^6$입니다. 지수법칙 $r^6 = (r^2)^3$을 이용하면 $r = \\sqrt{3}$을 직접 대입하는 것보다 훨씬 깔끔합니다.',
                'knowledge_en': 'Since $a_7 = a_1 r^6$ and $r^6 = (r^2)^3$, we can express $a_7$ directly in terms of $r^2$.',
                'questions': [
                    {
                        'level_label': '중간 전개 (나) 디딤돌 4',
                        'level_label_en': 'Intermediate Step B Step 4',
                        'stem': '등비수열의 제$7$항 $a_7 = a_1 r^6$을 $r^2$의 거듭제곱으로 바르게 바꾼 것은?',
                        'stem_en': 'Which expression rewrites $a_7 = a_1 r^6$ in terms of $r^2$?',
                        'options': ['$a_1 (r^2)^2$', '$a_1 (r^2)^3$', '$a_1 (r^2)^4$', '$3 a_1 r^2$', '$a_1 r^2$'],
                        'answer': 2,
                        'exp': '지수법칙에 의해 $r^6 = r^{2 \\times 3} = (r^2)^3$이므로 $a_7 = a_1 (r^2)^3$입니다.',
                        'exp_en': 'By exponent laws, $r^6 = (r^2)^3$, so $a_7 = a_1 (r^2)^3$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 레고 조립] $a_1 = 1$, $r^2 = 3$을 대입하여 $a_7$ 확정하기',
                'title_en': '💎 Step 5 · [Final LEGO Assembly] Computing $a_7$ from $a_1 = 1$ and $r^2 = 3$',
                'knowledge': '이제 $a_7 = a_1 (r^2)^3$에 $a_1 = 1$과 $r^2 = 3$을 대입하면 단번에 정답을 얻습니다.',
                'knowledge_en': 'Substitute $a_1 = 1$ and $r^2 = 3$ into $a_7 = a_1 (r^2)^3$ to obtain $a_7$.',
                'questions': [
                    {
                        'level_label': '최종 레고 조립 디딤돌 5',
                        'level_label_en': 'Final LEGO Assembly Step 5',
                        'stem': '$a_1 = 1$, $r^2 = 3$일 때, $a_7 = a_1 (r^2)^3$의 값은?',
                        'stem_en': 'Given $a_1 = 1$ and $r^2 = 3$, what is $a_7 = a_1 (r^2)^3$?',
                        'options': ['$9$', '$9\\sqrt{3}$', '$27$', '$27\\sqrt{3}$', '$81$'],
                        'answer': 3,
                        'exp': '$a_7 = 1 \\times 3^3 = 27$입니다.',
                        'exp_en': '$a_7 = 1 \\times 3^3 = 27$.',
                    }
                ],
            },
        ],
        'final': {
            'stem': '모든 항이 양수인 등비수열 $\\{a_n\\}$에 대하여 $a_1=1,\\; a_5=3a_3$ 일 때, $a_7$의 값은? [3점]',
            'stem_en': 'For a geometric sequence $\\{a_n\\}$ with all positive terms satisfying $a_1=1$ and $a_5=3a_3$, what is the value of $a_7$? [3 points]',
            'options': ['$9$', '$9\\sqrt{3}$', '$27$', '$27\\sqrt{3}$', '$81$'],
            'answer': 3,
            'exp': '공비를 $r$라 하면 $a_5=3a_3$에서 $r^2=3$이므로 $a_7 = a_1 r^6 = 1 \\times (r^2)^3 = 3^3 = 27$입니다. 정답은 ③입니다.',
            'exp_en': 'Let $r$ be the common ratio. From $a_5 = 3a_3$, we have $r^2 = 3$, so $a_7 = a_1 r^6 = 1 \\cdot (r^2)^3 = 27$. The correct answer is ③.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 <b>등비수열의 일반항과 항 번호 차이에 따른 거듭제곱 비례성</b>을 이해하고 있는지를 평가합니다. '
                '홀수 번째 항들($a_1, a_3, a_5, a_7, \\dots$)끼리는 공비가 $r^2$인 새로운 등비수열을 이룬다는 성질을 활용하면 계산이 매우 간결해집니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: 두 칸 공비 $r^2$ 구하기</b><br>\n'
                '  등비수열 $\\{a_n\\}$의 공비를 $r$ ($r > 0$)라 하면 $a_5 = a_3 r^2$입니다. 조건 $a_5 = 3a_3$에 대입하면:<br>\n'
                '  $$a_3 r^2 = 3a_3$$<br>\n'
                '  모든 항이 양수이므로 $a_3 > 0$이고, 양변을 $a_3$으로 나누면 $r^2 = 3$을 얻습니다.<br>\n'
                '  <b>2단계: 제$7$항 $a_7$ 계산하기</b><br>\n'
                '  $a_1 = 1$이므로 일반항 $a_n = a_1 r^{n-1}$에 $n = 7$을 대입합니다:<br>\n'
                '  $$a_7 = a_1 r^6 = 1 \\times (r^2)^3 = 3^3 = 27$$\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>\n'
                '  따라서 $a_7$의 값은 $27$이며, 정답은 <b>③번</b>입니다.<br>\n'
                '  💡 <b>실전 팁</b>: $a_1, a_3, a_5, a_7$은 두 칸씩 건너뛰는 부분수열이므로 $a_1 = 1 \\xrightarrow{\\times 3} a_3 = 3 \\xrightarrow{\\times 3} a_5 = 9 \\xrightarrow{\\times 3} a_7 = 27$로 3초 만에 암산검산할 수 있습니다.\n'
                '</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                '<p>This problem tests the <b>multiplicative structure of a geometric sequence</b>. '
                'Notice that the odd-indexed terms $a_1, a_3, a_5, a_7$ form a geometric subsequence with common ratio $r^2$.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Determine $r^2$ from $a_5 = 3a_3$</b><br>\n'
                '  Let $r > 0$ be the common ratio. Since $a_5 = a_3 r^2$ and $a_3 > 0$, dividing $a_3 r^2 = 3a_3$ by $a_3$ yields:<br>\n'
                '  $$r^2 = 3$$<br>\n'
                '  <b>Step 2: Compute $a_7$</b><br>\n'
                '  Using $a_1 = 1$ and $r^6 = (r^2)^3$, we obtain:<br>\n'
                '  $$a_7 = a_1 r^6 = 1 \\times 3^3 = 27$$\n'
                '</p>\n\n'
                '<h4>✨ [Conclusion & Key Takeaway]</h4>\n'
                '<p>\n'
                '  The seventh term $a_7$ is $27$, which corresponds to <b>Option ③</b>.\n'
                '</p>'
            ),
        },
    },
    {
        'slug': 'csat27_04',
        'qNum': '4',
        'points': 3,
        'is_short_answer': False,
        'subject': '공통(수학I·II)',
        'title': '[2027학년도 수능 고3 공통 4번] 함수의 그래프에서 좌극한과 우극한 읽기',
        'title_en': '[2027 CSAT Math Common #4] Evaluating One-Sided Limits from a Graph',
        'summary_ko': '조각별로 주어진 $y=f(x)$의 그래프에서 $x \\to 0-$ 좌극한과 $x \\to 1+$ 우극한을 정확히 읽어 합하기',
        'summary_en': 'Read the left-hand limit as $x \\to 0-$ and the right-hand limit as $x \\to 1+$ from the piecewise graph $y=f(x)$.',
        'tags': ['2027학년도 수능', '공통(수학I·II)', '수학II', '함수의극한', '좌극한', '우극한', '4번'],
        'orig_svg': (
            '<svg viewBox="0 0 320 230" xmlns="http://www.w3.org/2000/svg" '
            'style="max-width:340px;width:100%;height:auto;display:block;margin:12px auto;" '
            'role="img" aria-label="함수 y=f(x)의 그래프">'
            '<rect width="320" height="230" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1"/>'
            '<defs>'
            '<marker id="csat27p4-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
            '<path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#1e293b"/>'
            '</marker>'
            '</defs>'
            '<line x1="24" y1="182" x2="298" y2="182" stroke="#1e293b" stroke-width="1.3" marker-end="url(#csat27p4-arr)"/>'
            '<line x1="160" y1="212" x2="160" y2="24" stroke="#1e293b" stroke-width="1.3" marker-end="url(#csat27p4-arr)"/>'
            '<line x1="126" y1="182" x2="126" y2="114" stroke="#64748b" stroke-width="1.1" stroke-dasharray="3,2.5"/>'
            '<line x1="194" y1="182" x2="194" y2="114" stroke="#64748b" stroke-width="1.1" stroke-dasharray="3,2.5"/>'
            '<line x1="126" y1="148" x2="194" y2="148" stroke="#64748b" stroke-width="1.1" stroke-dasharray="3,2.5"/>'
            '<line x1="126" y1="114" x2="194" y2="114" stroke="#64748b" stroke-width="1.1" stroke-dasharray="3,2.5"/>'
            '<line x1="34" y1="56" x2="126" y2="148" stroke="#0f172a" stroke-width="2.1" stroke-linecap="round"/>'
            '<path d="M 126 114 A 34 34 0 0 1 160 80" fill="none" stroke="#0f172a" stroke-width="2.1" stroke-linecap="round"/>'
            '<line x1="160" y1="182" x2="194" y2="114" stroke="#0f172a" stroke-width="2.1" stroke-linecap="round"/>'
            '<line x1="194" y1="148" x2="286" y2="56" stroke="#0f172a" stroke-width="2.1" stroke-linecap="round"/>'
            '<circle cx="126" cy="148" r="3.5" fill="#ffffff" stroke="#0f172a" stroke-width="1.7"/>'
            '<circle cx="126" cy="114" r="3.5" fill="#0f172a"/>'
            '<circle cx="160" cy="80" r="3.5" fill="#ffffff" stroke="#0f172a" stroke-width="1.7"/>'
            '<circle cx="160" cy="182" r="3.5" fill="#0f172a"/>'
            '<circle cx="194" cy="114" r="3.5" fill="#ffffff" stroke="#0f172a" stroke-width="1.7"/>'
            '<circle cx="194" cy="148" r="3.5" fill="#0f172a"/>'
            '<text x="148" y="29" font-family="Times New Roman, Georgia, serif" font-style="italic" font-size="15" fill="#0f172a">y</text>'
            '<text x="296" y="197" font-family="Times New Roman, Georgia, serif" font-style="italic" font-size="15" fill="#0f172a">x</text>'
            '<text x="150" y="197" font-family="Times New Roman, Georgia, serif" font-size="14" fill="#0f172a" text-anchor="middle">O</text>'
            '<text x="124" y="197" font-family="Times New Roman, Georgia, serif" font-size="14" fill="#0f172a" text-anchor="middle">\u22121</text>'
            '<text x="194" y="197" font-family="Times New Roman, Georgia, serif" font-size="14" fill="#0f172a" text-anchor="middle">1</text>'
            '<text x="153" y="144" font-family="Times New Roman, Georgia, serif" font-size="14" fill="#0f172a" text-anchor="end">1</text>'
            '<text x="153" y="110" font-family="Times New Roman, Georgia, serif" font-size="14" fill="#0f172a" text-anchor="end">2</text>'
            '<text x="153" y="76" font-family="Times New Roman, Georgia, serif" font-size="14" fill="#0f172a" text-anchor="end">3</text>'
            '<text x="268" y="48" font-family="Times New Roman, Georgia, serif" font-style="italic" font-size="14.5" fill="#0f172a" text-anchor="middle">y = f(x)</text>'
            '</svg>'
        ),
        'symbols': [
            {
                'sym': '$\\lim_{x \\to 0-} f(x)$',
                'desc': '$x$가 $0$보다 작은 쪽(왼쪽)에서 $0$에 한없이 가까워질 때 그래프가 향하는 $y$ 높이(좌극한)',
                'desc_en': 'Left-hand limit: the $y$-value the curve approaches as $x$ nears $0$ from the left ($x < 0$).',
            },
            {
                'sym': '$\\lim_{x \\to 1+} f(x)$',
                'desc': '$x$가 $1$보다 큰 쪽(오른쪽)에서 $1$에 한없이 가까워질 때 그래프가 향하는 $y$ 높이(우극한)',
                'desc_en': 'Right-hand limit: the $y$-value the curve approaches as $x$ nears $1$ from the right ($x > 1$).',
            },
            {
                'sym': '$\\circ$ 와 $\\bullet$',
                'desc': '빈 동그라미($\\circ$)는 비어 있는 도착 목표점(극한과 관련), 색칠된 점($\\bullet$)은 실제 함숫값',
                'desc_en': 'Open circle ($\\circ$) excludes the endpoint; filled dot ($\\bullet$) indicates the actual function value.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 기초 직관] 길 따라가기 놀이: $0$의 왼쪽 언덕길을 올라가면 눈금 어디에 닿을까?',
                'title_en': '🔰 Step 1 · [Elementary Intuition] Path Tracing on the Hill Left of $0$',
                'knowledge': '가로축의 $-1$과 $0$ 사이에 그려진 둥근 언덕길을 손가락으로 왼쪽($-1$)에서 오른쪽($0$)으로 따라 올라가 보세요. 끝부분의 하얀 동그라미가 세로축 눈금 몇에 있는지 읽으면 됩니다!',
                'knowledge_en': 'Trace your finger along the curved arc between $x = -1$ and $x = 0$ moving rightward toward the $y$-axis. Read the $y$-tick of the open circle at the top.',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '그림에서 가로 눈금 $-1$과 $0$ 사이의 둥근 길을 따라 오른쪽 끝($y$축)까지 올라가면 세로 눈금 얼마에 도착하나요?',
                        'stem_en': 'Tracing the curved path on $(-1, 0)$ rightward up to the $y$-axis, which $y$-tick does the path reach?',
                        'options': ['$0$', '$1$', '$2$', '$3$', '$4$'],
                        'answer': 4,
                        'exp': '$-1$과 $0$ 사이의 곡선은 $( -1, 2 )$에서 출발해 $y$축 위의 $( 0, 3 )$ 빈 동그라미를 향해 올라가므로 눈금 $3$에 도착합니다.',
                        'exp_en': 'The arc starts at $(-1, 2)$ and rises to the open circle on the $y$-axis at height $3$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [기호 번역] $x \\to 0-$와 $x \\to 1+$의 접근 방향 구분하기',
                'title_en': '🌿 Step 2 · [Symbol Translation] Understanding Left ($-$) vs. Right ($+$) Approach',
                'knowledge': '화살표 오른쪽 숫자 뒤의 마이너스($-$)는 수직선의 왼쪽(작은 값)에서 다가온다는 뜻이고, 플러스($+$)는 오른쪽(큰 값)에서 다가온다는 뜻입니다.',
                'knowledge_en': 'A minus superscript ($a-$) means approaching $a$ from the left ($x < a$), while a plus superscript ($a+$) means approaching from the right ($x > a$).',
                'questions': [
                    {
                        'level_label': '기호 번역 디딤돌 2',
                        'level_label_en': 'Symbol Translation Step 2',
                        'stem': '두 기호 $x \\to 0-$와 $x \\to 1+$가 뜻하는 $x$의 접근 방향을 바르게 짝지은 것은?',
                        'stem_en': 'Which option correctly describes the directions of $x \\to 0-$ and $x \\to 1+$?',
                        'options': [
                            '$0$의 왼쪽에서 접근, $1$의 왼쪽에서 접근',
                            '$0$의 왼쪽에서 접근, $1$의 오른쪽에서 접근',
                            '$0$의 오른쪽에서 접근, $1$의 왼쪽에서 접근',
                            '$0$의 오른쪽에서 접근, $1$의 오른쪽에서 접근',
                            '정확히 $x=0$과 $x=1$에서의 함숫값만 확인',
                        ],
                        'answer': 2,
                        'exp': '$0-$는 $0$보다 작은 왼쪽($x < 0$)에서 접근하는 좌극한이고, $1+$는 $1$보다 큰 오른쪽($x > 1$)에서 접근하는 우극한입니다.',
                        'exp_en': '$0-$ approaches $0$ from the left ($x < 0$), and $1+$ approaches $1$ from the right ($x > 1$).',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [핵심 관계식 (가)] 좌극한 $\\lim_{x \\to 0-} f(x)$ 구하기',
                'title_en': '🌱 Step 3 · [Core Relation A] Finding the Left-Hand Limit $\\lim_{x \\to 0-} f(x)$',
                'knowledge': '극한값은 $x = 0$에서의 실제 색칠된 점 $f(0) = 0$이 아니라, $x < 0$ 구간에서 $x$가 $0$에 다가갈 때 그래프의 선이 향하는 목표 높이입니다.',
                'knowledge_en': 'The limit depends on where the path heads as $x \\to 0$ with $x < 0$, NOT on the filled dot $f(0) = 0$.',
                'questions': [
                    {
                        'level_label': '핵심 관계식 (가) 디딤돌 3',
                        'level_label_en': 'Core Relation A Step 3',
                        'stem': '주어진 그래프에서 $\\lim_{x \\to 0-} f(x)$의 값은?',
                        'stem_en': 'From the given graph, what is $\\lim_{x \\to 0-} f(x)$?',
                        'options': ['$0$', '$1$', '$2$', '$3$', '$4$'],
                        'answer': 4,
                        'exp': '$x$가 $0$보다 작은 쪽에서 $0$에 가까워질 때 그래프는 $(0, 3)$을 향하므로 $\\lim_{x \\to 0-} f(x) = 3$입니다.',
                        'exp_en': 'As $x \\to 0$ from the left, the curve approaches $(0, 3)$, so $\\lim_{x \\to 0-} f(x) = 3$.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [중간 전개 (나)] 우극한 $\\lim_{x \\to 1+} f(x)$ 구하기',
                'title_en': '🌳 Step 4 · [Intermediate Step B] Finding the Right-Hand Limit $\\lim_{x \\to 1+} f(x)$',
                'knowledge': '이번에는 $x = 1$의 오른쪽($x > 1$)에 그려진 직선을 따라 왼쪽 아래로 내려오면서 $x = 1$에 도착할 때의 $y$ 높이를 읽습니다.',
                'knowledge_en': 'Follow the ray in the region $x > 1$ leftward toward $x = 1$ and read the $y$-coordinate of its endpoint at $x = 1$.',
                'questions': [
                    {
                        'level_label': '중간 전개 (나) 디딤돌 4',
                        'level_label_en': 'Intermediate Step B Step 4',
                        'stem': '주어진 그래프에서 $\\lim_{x \\to 1+} f(x)$의 값은?',
                        'stem_en': 'From the given graph, what is $\\lim_{x \\to 1+} f(x)$?',
                        'options': ['$0$', '$1$', '$2$', '$3$', '$4$'],
                        'answer': 2,
                        'exp': '$x > 1$인 오른쪽 직선을 따라 $x \\to 1+$로 접근하면 점 $(1, 1)$에 도달하므로 $\\lim_{x \\to 1+} f(x) = 1$입니다.',
                        'exp_en': 'Approaching $x = 1$ from the right ($x > 1$) along the line reaches $(1, 1)$, so $\\lim_{x \\to 1+} f(x) = 1$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 레고 조립] 두 극한값의 합 확정하기',
                'title_en': '💎 Step 5 · [Final LEGO Assembly] Summing the Two One-Sided Limits',
                'knowledge': '이제 앞서 정확히 읽은 좌극한 $3$과 우극한 $1$을 더하면 최종 정답이 완성됩니다.',
                'knowledge_en': 'Add the left-hand limit $3$ and the right-hand limit $1$ to complete the problem.',
                'questions': [
                    {
                        'level_label': '최종 레고 조립 디딤돌 5',
                        'level_label_en': 'Final LEGO Assembly Step 5',
                        'stem': '$\\lim_{x \\to 0-} f(x) = 3$이고 $\\lim_{x \\to 1+} f(x) = 1$일 때, $\\lim_{x \\to 0-} f(x) + \\lim_{x \\to 1+} f(x)$의 값은?',
                        'stem_en': 'Since $\\lim_{x \\to 0-} f(x) = 3$ and $\\lim_{x \\to 1+} f(x) = 1$, what is their sum?',
                        'options': ['$1$', '$2$', '$3$', '$4$', '$5$'],
                        'answer': 4,
                        'exp': '$3 + 1 = 4$입니다.',
                        'exp_en': '$3 + 1 = 4$.',
                    }
                ],
            },
        ],
        'final': {
            'stem': '함수 $y=f(x)$의 그래프가 그림과 같다. $\\lim_{x \\to 0-} f(x) + \\lim_{x \\to 1+} f(x)$의 값은? [3점]',
            'stem_en': 'The graph of $y=f(x)$ is shown in the figure. What is the value of $\\lim_{x \\to 0-} f(x) + \\lim_{x \\to 1+} f(x)$? [3 points]',
            'options': ['$1$', '$2$', '$3$', '$4$', '$5$'],
            'answer': 4,
            'exp': '$\\lim_{x \\to 0-} f(x) = 3$, $\\lim_{x \\to 1+} f(x) = 1$이므로 두 극한값의 합은 $3 + 1 = 4$입니다. 정답은 ④입니다.',
            'exp_en': 'From the graph, $\\lim_{x \\to 0-} f(x) = 3$ and $\\lim_{x \\to 1+} f(x) = 1$, so their sum is $3 + 1 = 4$. The correct answer is ④.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 불연속점이 포함된 함수 $y = f(x)$의 그래프에서 <b>좌극한과 우극한의 기하학적 의미</b>를 함숫값 및 반대 방향 극한값과 혼동하지 않고 정확히 판독할 수 있는지를 평가합니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: $x = 0$에서의 좌극한 $\\lim_{x \\to 0-} f(x)$ 구하기</b><br>\n'
                '  구간 $(-1, 0)$에서 $x$가 $0$보다 작은 값을 가지면서 $0$에 한없이 가까워질 때, 곡선 $y = f(x)$ 위의 점은 빈 동그라미 $(0, 3)$에 한없이 가까워집니다:<br>\n'
                '  $$\\lim_{x \\to 0-} f(x) = 3$$<br>\n'
                '  <b>2단계: $x = 1$에서의 우극한 $\\lim_{x \\to 1+} f(x)$ 구하기</b><br>\n'
                '  구간 $(1, \\infty)$에서 $x$가 $1$보다 큰 값을 가지면서 $1$에 한없이 가까워질 때, 직선 $y = f(x)$ 위의 점은 $(1, 1)$에 한없이 가까워집니다:<br>\n'
                '  $$\\lim_{x \\to 1+} f(x) = 1$$<br>\n'
                '  <b>3단계: 두 극한값의 합 계산</b><br>\n'
                '  $$\\lim_{x \\to 0-} f(x) + \\lim_{x \\to 1+} f(x) = 3 + 1 = 4$$\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>\n'
                '  따라서 구하는 값은 $4$이며, 정답은 <b>④번</b>입니다.<br>\n'
                '  💡 <b>실전 팁</b>: $x = 0$에서의 함숫값 $f(0) = 0$이나 $x = 1$에서의 좌극한 $\\lim_{x \\to 1-} f(x) = 2$를 읽지 않도록 $0-$, $1+$의 부호 방향에 연필로 화살표를 먼저 표시하세요.\n'
                '</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                '<p>This problem tests whether one can accurately read <b>one-sided limits</b> from a piecewise graph without confusing them with point values or opposite-side limits.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Evaluate the left-hand limit at $x = 0$</b><br>\n'
                '  As $x \\to 0$ with $-1 < x < 0$, the circular arc rises toward the open circle at $(0, 3)$:<br>\n'
                '  $$\\lim_{x \\to 0-} f(x) = 3$$<br>\n'
                '  <b>Step 2: Evaluate the right-hand limit at $x = 1$</b><br>\n'
                '  As $x \\to 1$ with $x > 1$, the ray descends leftward toward the point $(1, 1)$:<br>\n'
                '  $$\\lim_{x \\to 1+} f(x) = 1$$<br>\n'
                '  <b>Step 3: Compute the sum</b><br>\n'
                '  $$\\lim_{x \\to 0-} f(x) + \\lim_{x \\to 1+} f(x) = 3 + 1 = 4$$\n'
                '</p>\n\n'
                '<h4>✨ [Conclusion & Key Takeaway]</h4>\n'
                '<p>\n'
                '  The sum of the two limits is $4$, which corresponds to <b>Option ④</b>.\n'
                '</p>'
            ),
        },
    },
    {
        'slug': 'csat27_05',
        'qNum': '5',
        'points': 3,
        'is_short_answer': False,
        'subject': '공통(수학I·II)',
        'title': '[2027학년도 수능 고3 공통 5번] 부정적분과 미적분의 기본정리를 이용한 정적분',
        'title_en': '[2027 CSAT Math Common #5] Definite Integral via Antiderivative and Fundamental Theorem',
        'summary_ko': '$f(x)$의 한 부정적분 $F(x)=x^3-x^2+x$가 주어졌을 때 미적분의 기본정리 $F(2)-F(0)$으로 정적분 구하기',
        'summary_en': 'Use the given antiderivative $F(x)=x^3-x^2+x$ directly in $\\int_0^2 f(x)\\,dx = F(2)-F(0)$.',
        'tags': ['2027학년도 수능', '공통(수학I·II)', '수학II', '적분', '부정적분', '정적분', '5번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': "$F'(x) = f(x)$",
                'desc': '$F(x)$가 $f(x)$의 한 부정적분이라는 것은 $F(x)$를 미분하면 $f(x)$가 된다는 뜻',
                'desc_en': '$F(x)$ being an antiderivative of $f(x)$ means $F\'(x) = f(x)$.',
            },
            {
                'sym': '$\\displaystyle\\int_0^2 f(x)\\,dx = F(2) - F(0)$',
                'desc': '정적분은 부정적분 $F(x)$에 위끝 $2$를 넣은 값에서 아래끝 $0$을 넣은 값을 뺀 것과 같음',
                'desc_en': 'Fundamental Theorem of Calculus: evaluate the antiderivative at the upper limit minus the lower limit.',
            },
            {
                'sym': '$F(0) = 0$',
                'desc': '상수항이 없는 다항식 $x^3 - x^2 + x$에 $x = 0$을 대입하면 $0$이 됨',
                'desc_en': 'Evaluating $F(x) = x^3 - x^2 + x$ at $x = 0$ yields $0$.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 기초 직관] $2 \\times 2 \\times 2 - 2 \\times 2 + 2$ 계산하기',
                'title_en': '🔰 Step 1 · [Elementary Intuition] Computing $2 \\times 2 \\times 2 - 2 \\times 2 + 2$',
                'knowledge': '$2$를 세 번 곱하면 $8$, 두 번 곱하면 $4$입니다. 초등학교 덧셈과 뺄셈으로 $8 - 4 + 2$를 차례대로 계산해 봅시다.',
                'knowledge_en': 'Multiplying $2$ three times gives $8$, and twice gives $4$. Compute $8 - 4 + 2$ step by step.',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '초등학교 곱셈과 덧셈·뺄셈으로 $2 \\times 2 \\times 2 - 2 \\times 2 + 2$를 계산한 값은?',
                        'stem_en': 'What is the value of $2 \\times 2 \\times 2 - 2 \\times 2 + 2$?',
                        'options': ['$4$', '$5$', '$6$', '$7$', '$8$'],
                        'answer': 3,
                        'exp': '$2 \\times 2 \\times 2 = 8$, $2 \\times 2 = 4$이므로 $8 - 4 + 2 = 6$입니다.',
                        'exp_en': '$8 - 4 + 2 = 6$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [기호 번역] 정적분 $\\int_0^2 f(x)\\,dx$를 부정적분 $F(x)$로 나타내기',
                'title_en': '🌿 Step 2 · [Symbol Translation] Expressing $\\int_0^2 f(x)\\,dx$ via $F(x)$',
                'knowledge': '$F(x)$가 이미 $f(x)$를 적분해 놓은 부정적분이므로, 굳이 $F(x)$를 미분해서 $f(x)$를 구한 뒤 다시 적분할 필요가 전혀 없습니다! 미적분의 기본정리를 바로 씁니다.',
                'knowledge_en': 'Because $F(x)$ is already an antiderivative of $f(x)$, there is no need to differentiate and re-integrate; apply the Fundamental Theorem directly.',
                'questions': [
                    {
                        'level_label': '기호 번역 디딤돌 2',
                        'level_label_en': 'Symbol Translation Step 2',
                        'stem': '함수 $f(x)$의 한 부정적분이 $F(x)$일 때, 정적분 $\\displaystyle\\int_0^2 f(x)\\,dx$와 항상 같은 식은?',
                        'stem_en': 'If $F(x)$ is an antiderivative of $f(x)$, which expression equals $\\displaystyle\\int_0^2 f(x)\\,dx$?',
                        'options': ['$F(0) - F(2)$', '$F(2) - F(0)$', '$F(2) + F(0)$', "$F'(2) - F'(0)$", '$2F(2)$'],
                        'answer': 2,
                        'exp': '미적분의 기본정리에 의해 $\\displaystyle\\int_0^2 f(x)\\,dx = \\Big[F(x)\\Big]_0^2 = F(2) - F(0)$입니다.',
                        'exp_en': 'By the Fundamental Theorem of Calculus, $\\displaystyle\\int_0^2 f(x)\\,dx = F(2) - F(0)$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [핵심 관계식 (가)] 위끝을 대입한 $F(2)$ 구하기',
                'title_en': '🌱 Step 3 · [Core Relation A] Evaluating $F(2)$ at the Upper Limit',
                'knowledge': '주어진 부정적분 $F(x) = x^3 - x^2 + x$에 위끝 $x = 2$를 대입합니다.',
                'knowledge_en': 'Substitute the upper limit $x = 2$ into $F(x) = x^3 - x^2 + x$.',
                'questions': [
                    {
                        'level_label': '핵심 관계식 (가) 디딤돌 3',
                        'level_label_en': 'Core Relation A Step 3',
                        'stem': '$F(x) = x^3 - x^2 + x$일 때, $F(2)$의 값은?',
                        'stem_en': 'Given $F(x) = x^3 - x^2 + x$, what is $F(2)$?',
                        'options': ['$4$', '$6$', '$8$', '$10$', '$12$'],
                        'answer': 2,
                        'exp': '$F(2) = 2^3 - 2^2 + 2 = 8 - 4 + 2 = 6$입니다.',
                        'exp_en': '$F(2) = 2^3 - 2^2 + 2 = 8 - 4 + 2 = 6$.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [중간 전개 (나)] 아래끝을 대입한 $F(0)$ 구하기',
                'title_en': '🌳 Step 4 · [Intermediate Step B] Evaluating $F(0)$ at the Lower Limit',
                'knowledge': '$F(x) = x^3 - x^2 + x$에 아래끝 $x = 0$을 대입하여 뺄 값이 있는지 확인합니다.',
                'knowledge_en': 'Substitute the lower limit $x = 0$ into $F(x) = x^3 - x^2 + x$.',
                'questions': [
                    {
                        'level_label': '중간 전개 (나) 디딤돌 4',
                        'level_label_en': 'Intermediate Step B Step 4',
                        'stem': '$F(x) = x^3 - x^2 + x$일 때, $F(0)$의 값은?',
                        'stem_en': 'Given $F(x) = x^3 - x^2 + x$, what is $F(0)$?',
                        'options': ['$-2$', '$-1$', '$0$', '$1$', '$2$'],
                        'answer': 3,
                        'exp': '$F(0) = 0^3 - 0^2 + 0 = 0$입니다.',
                        'exp_en': '$F(0) = 0^3 - 0^2 + 0 = 0$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 레고 조립] $F(2) - F(0)$으로 정적분 확정하기',
                'title_en': '💎 Step 5 · [Final LEGO Assembly] Computing $F(2) - F(0)$',
                'knowledge': '이제 $F(2) = 6$과 $F(0) = 0$을 $\\int_0^2 f(x)\\,dx = F(2) - F(0)$에 대입합니다.',
                'knowledge_en': 'Substitute $F(2) = 6$ and $F(0) = 0$ into $F(2) - F(0)$.',
                'questions': [
                    {
                        'level_label': '최종 레고 조립 디딤돌 5',
                        'level_label_en': 'Final LEGO Assembly Step 5',
                        'stem': '$F(2) = 6$, $F(0) = 0$이므로 $\\displaystyle\\int_0^2 f(x)\\,dx = F(2) - F(0)$의 값은?',
                        'stem_en': 'With $F(2) = 6$ and $F(0) = 0$, what is $\\displaystyle\\int_0^2 f(x)\\,dx$?',
                        'options': ['$6$', '$7$', '$8$', '$9$', '$10$'],
                        'answer': 1,
                        'exp': '$F(2) - F(0) = 6 - 0 = 6$입니다.',
                        'exp_en': '$F(2) - F(0) = 6 - 0 = 6$.',
                    }
                ],
            },
        ],
        'final': {
            'stem': '다항함수 $f(x)$의 한 부정적분이 $F(x)=x^3-x^2+x$일 때, $\\displaystyle\\int_0^2 f(x)\\,dx$의 값은? [3점]',
            'stem_en': 'When an antiderivative of a polynomial function $f(x)$ is $F(x)=x^3-x^2+x$, what is the value of $\\displaystyle\\int_0^2 f(x)\\,dx$? [3 points]',
            'options': ['$6$', '$7$', '$8$', '$9$', '$10$'],
            'answer': 1,
            'exp': '미적분의 기본정리에 의해 $\\displaystyle\\int_0^2 f(x)\\,dx = F(2) - F(0) = (8 - 4 + 2) - 0 = 6$이므로 정답은 ①입니다.',
            'exp_en': 'By the Fundamental Theorem of Calculus, $\\displaystyle\\int_0^2 f(x)\\,dx = F(2) - F(0) = (8 - 4 + 2) - 0 = 6$. The correct answer is ①.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 <b>부정적분의 정의와 정적분의 기본 정리(미적분의 기본정리)</b> 사이의 직결 관계를 이해하고 있는지를 평가합니다. '
                '$F(x)$를 미분하여 $f(x) = 3x^2 - 2x + 1$을 구한 뒤 다시 적분하는 불필요한 우회 없이, 즉시 $F(2) - F(0)$을 계산하는 통찰을 묻습니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: 미적분의 기본정리 적용</b><br>\n'
                '  다항함수 $f(x)$의 한 부정적분이 $F(x)$이므로 정적분의 정의와 기본정리에 의하여 다음이 성립합니다:<br>\n'
                '  $$\\int_0^2 f(x)\\,dx = \\Big[F(x)\\Big]_0^2 = F(2) - F(0)$$<br>\n'
                '  <b>2단계: $F(2)$와 $F(0)$ 대입 계산</b><br>\n'
                '  $F(x) = x^3 - x^2 + x$에 $x = 2$와 $x = 0$을 각각 대입합니다:<br>\n'
                '  $$F(2) = 2^3 - 2^2 + 2 = 8 - 4 + 2 = 6, \\qquad F(0) = 0$$<br>\n'
                '  $$\\therefore \\int_0^2 f(x)\\,dx = 6 - 0 = 6$$\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>\n'
                '  따라서 구하는 정적분의 값은 $6$이며, 정답은 <b>①번</b>입니다.<br>\n'
                '  💡 <b>실전 팁</b>: 부정적분에 상수항 $C$가 붙어 있어도 정적분 계산 $F(b) - F(a)$에서는 상수항이 서로 상쇄됩니다. 다만 주어진 $F(x)$에 상수항이 있는 문제에서는 $F(0) \\ne 0$일 수 있으니 반드시 $F(0)$도 확인하는 습관을 유지하세요.\n'
                '</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                '<p>This problem tests direct application of the <b>Fundamental Theorem of Calculus</b>. '
                'Since $F(x)$ is already an antiderivative of $f(x)$, differentiating $F(x)$ and integrating back is redundant; we directly evaluate $F(2) - F(0)$.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Apply the Fundamental Theorem of Calculus</b><br>\n'
                '  $$\\int_0^2 f(x)\\,dx = \\Big[F(x)\\Big]_0^2 = F(2) - F(0)$$<br>\n'
                '  <b>Step 2: Evaluate $F(x) = x^3 - x^2 + x$ at the bounds</b><br>\n'
                '  $$F(2) = 2^3 - 2^2 + 2 = 8 - 4 + 2 = 6, \\qquad F(0) = 0$$<br>\n'
                '  $$\\int_0^2 f(x)\\,dx = 6 - 0 = 6$$\n'
                '</p>\n\n'
                '<h4>✨ [Conclusion & Key Takeaway]</h4>\n'
                '<p>\n'
                '  The value of the definite integral is $6$, which corresponds to <b>Option ①</b>.\n'
                '</p>'
            ),
        },
    },
    {
        'slug': 'csat27_06',
        'qNum': '6',
        'points': 3,
        'is_short_answer': False,
        'subject': '공통(수학I·II)',
        'title': '[2027학년도 수능 고3 공통 6번] 사인함수의 주기와 최댓값',
        'title_en': '[2027 CSAT Math Common #6] Period and Maximum Value of a Sine Function',
        'summary_ko': '함수 $f(x)=3\\sin\\frac{2\\pi x}{k}+k$ ($k>0$)의 주기가 $8$임을 이용해 $k=8$을 구하고 최댓값 $3+k$ 도출하기',
        'summary_en': 'Determine $k=8$ from the period of $f(x)=3\\sin\\frac{2\\pi x}{k}+k$ ($k>0$), then find its maximum $3+k=11$.',
        'tags': ['2027학년도 수능', '공통(수학I·II)', '수학I', '삼각함수', '삼각함수의그래프', '주기', '최댓값', '6번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': '주기 $T = \\dfrac{2\\pi}{|b|}$',
                'desc': '삼각함수 $y = a\\sin(bx) + c$의 한 물결이 반복되는 가로 간격(주기)',
                'desc_en': 'Period formula for $y = a\\sin(bx) + c$: horizontal length of one complete wave cycle.',
            },
            {
                'sym': '$-1 \\le \\sin\\theta \\le 1$',
                'desc': '사인값은 각도가 아무리 변해도 항상 $-1$ 이상 $1$ 이하에서만 움직임',
                'desc_en': 'Range of the sine function: $\\sin\\theta$ always lies between $-1$ and $1$.',
            },
            {
                'sym': '최댓값 $= |a| + c$',
                'desc': '$y = a\\sin(bx) + c$ ($a > 0$)에서 물결의 가장 높은 꼭대기 값 $a + c$',
                'desc_en': 'Maximum value of $y = a\\sin(bx) + c$ (for $a > 0$) is $a + c$.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 기초 직관] 중심 높이 $8\\text{m}$에서 위아래로 $3\\text{m}$씩 오르내리는 물결의 최고 높이',
                'title_en': '🔰 Step 1 · [Elementary Intuition] Peak Height of a Wave Centered at $8\\text{m}$ with Amplitude $3\\text{m}$',
                'knowledge': '바다의 평균 수면 높이가 $8\\text{m}$인데, 파도가 위아래로 최대 $3\\text{m}$씩 오르내린다고 상상해 보세요. 파도가 가장 높이 올라갔을 때의 높이는 초등학교 덧셈으로 구할 수 있습니다.',
                'knowledge_en': 'Imagine a wave centered at height $8\\text{m}$ that rises and falls by up to $3\\text{m}$. Its highest peak is found by simple addition.',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '기준 높이가 $8$이고 위로 최대 $3$만큼 더 올라갈 수 있을 때, 가장 높은 곳의 높이는 얼마인가요?',
                        'stem_en': 'If the baseline height is $8$ and the wave rises up to $3$ units above it, what is the maximum height?',
                        'options': ['$5$', '$8$', '$11$', '$14$', '$24$'],
                        'answer': 3,
                        'exp': '기준 높이 $8$에서 위로 $3$만큼 더 올라가므로 $8 + 3 = 11$입니다.',
                        'exp_en': 'Adding $3$ to the baseline $8$ gives $8 + 3 = 11$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [기호 번역] $y = a\\sin(bx) + c$에서 주기 공식 확인하기',
                'title_en': '🌿 Step 2 · [Symbol Translation] Identifying the Period Formula for Sine',
                'knowledge': '기본 함수 $y = \\sin x$의 주기는 $2\\pi$입니다. $x$ 앞에 양수 $b$가 곱해진 $y = a\\sin(bx) + c$의 주기는 $2\\pi$를 $b$로 나눈 $\\dfrac{2\\pi}{b}$가 됩니다.',
                'knowledge_en': 'Since $y = \\sin x$ has period $2\\pi$, scaling $x$ by $b > 0$ gives period $T = \\dfrac{2\\pi}{b}$.',
                'questions': [
                    {
                        'level_label': '기호 번역 디딤돌 2',
                        'level_label_en': 'Symbol Translation Step 2',
                        'stem': '양수 $k$에 대하여 함수 $f(x) = 3\\sin\\left(\\dfrac{2\\pi}{k}x\\right) + k$의 주기를 $k$로 바르게 나타낸 것은?',
                        'stem_en': 'For $k > 0$, what is the period of $f(x) = 3\\sin\\left(\\dfrac{2\\pi}{k}x\\right) + k$ in terms of $k$?',
                        'options': ['$\\dfrac{k}{2}$', '$k$', '$2k$', '$2\\pi k$', '$\\dfrac{2\\pi}{k}$'],
                        'answer': 2,
                        'exp': '$x$의 계수가 $b = \\dfrac{2\\pi}{k} > 0$이므로 주기는 $\\dfrac{2\\pi}{\\frac{2\\pi}{k}} = k$입니다.',
                        'exp_en': 'Since the coefficient of $x$ is $b = \\dfrac{2\\pi}{k} > 0$, the period is $\\dfrac{2\\pi}{2\\pi / k} = k$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [핵심 관계식 (가)] 주기가 $8$이라는 조건에서 양수 $k$ 구하기',
                'title_en': '🌱 Step 3 · [Core Relation A] Finding $k$ from Period $= 8$',
                'knowledge': '2단계에서 구한 주기 $k$가 문제에서 주어진 주기 $8$과 같다고 놓으면 상수 $k$가 즉시 결정됩니다.',
                'knowledge_en': 'Equate the period $k$ found in Step 2 to the given period $8$.',
                'questions': [
                    {
                        'level_label': '핵심 관계식 (가) 디딤돌 3',
                        'level_label_en': 'Core Relation A Step 3',
                        'stem': '함수 $f(x) = 3\\sin\\dfrac{2\\pi x}{k} + k$ ($k > 0$)의 주기가 $8$일 때, 양수 $k$의 값은?',
                        'stem_en': 'When the period of $f(x) = 3\\sin\\dfrac{2\\pi x}{k} + k$ ($k > 0$) is $8$, what is $k$?',
                        'options': ['$2$', '$4$', '$6$', '$8$', '$16$'],
                        'answer': 4,
                        'exp': '주기가 $k$이므로 $k = 8$입니다.',
                        'exp_en': 'Since the period equals $k$, we immediately have $k = 8$.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [중간 전개 (나)] 진동 부분 $3\\sin\\dfrac{\\pi x}{4}$의 최댓값 구하기',
                'title_en': '🌳 Step 4 · [Intermediate Step B] Maximum of the Oscillating Term $3\\sin\\dfrac{\\pi x}{4}$',
                'knowledge': '$\\sin$ 값은 언제나 $-1$ 이상 $1$ 이하이므로, 양수 $3$을 곱한 $3\\sin\\left(\\dfrac{\\pi x}{4}\\right)$은 $\\sin$ 값이 $1$일 때 가장 커집니다.',
                'knowledge_en': 'Since $-1 \\le \\sin\\theta \\le 1$, multiplying by $+3$ achieves its maximum when $\\sin\\theta = 1$.',
                'questions': [
                    {
                        'level_label': '중간 전개 (나) 디딤돌 4',
                        'level_label_en': 'Intermediate Step B Step 4',
                        'stem': '실수 전체에서 $3\\sin\\left(\\dfrac{\\pi x}{4}\\right)$이 가질 수 있는 최댓값은?',
                        'stem_en': 'What is the maximum value of $3\\sin\\left(\\dfrac{\\pi x}{4}\\right)$ over all real $x$?',
                        'options': ['$1$', '$2$', '$3$', '$4$', '$6$'],
                        'answer': 3,
                        'exp': '$\\sin\\left(\\dfrac{\\pi x}{4}\\right)$의 최댓값이 $1$이므로 $3 \\times 1 = 3$입니다.',
                        'exp_en': 'The maximum of $\\sin\\left(\\dfrac{\\pi x}{4}\\right)$ is $1$, so $3 \\times 1 = 3$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 레고 조립] 평행이동 $+k$까지 더해 $f(x)$의 최댓값 확정하기',
                'title_en': '💎 Step 5 · [Final LEGO Assembly] Adding Vertical Shift $+k$ for the Final Maximum',
                'knowledge': '$k = 8$을 대입한 $f(x) = 3\\sin\\left(\\dfrac{\\pi x}{4}\\right) + 8$에서 최댓값은 $3 + 8$입니다.',
                'knowledge_en': 'With $k = 8$, the maximum of $f(x) = 3\\sin\\left(\\dfrac{\\pi x}{4}\\right) + 8$ is $3 + 8$.',
                'questions': [
                    {
                        'level_label': '최종 레고 조립 디딤돌 5',
                        'level_label_en': 'Final LEGO Assembly Step 5',
                        'stem': '$k = 8$일 때 함수 $f(x) = 3\\sin\\dfrac{2\\pi x}{8} + 8$의 최댓값은?',
                        'stem_en': 'For $k = 8$, what is the maximum value of $f(x) = 3\\sin\\dfrac{2\\pi x}{8} + 8$?',
                        'options': ['$11$', '$12$', '$13$', '$14$', '$15$'],
                        'answer': 1,
                        'exp': '최댓값은 $3 \\times 1 + 8 = 11$입니다.',
                        'exp_en': 'The maximum value is $3(1) + 8 = 11$.',
                    }
                ],
            },
        ],
        'final': {
            'stem': '양수 $k$에 대하여 함수 $f(x)=3\\sin\\dfrac{2\\pi x}{k}+k$의 주기가 $8$일 때, 함수 $f(x)$의 최댓값은? [3점]',
            'stem_en': 'For a positive constant $k$, when the period of $f(x)=3\\sin\\dfrac{2\\pi x}{k}+k$ is $8$, what is the maximum value of $f(x)$? [3 points]',
            'options': ['$11$', '$12$', '$13$', '$14$', '$15$'],
            'answer': 1,
            'exp': '$k>0$이므로 주기 $\\dfrac{2\\pi}{\\frac{2\\pi}{k}} = k = 8$입니다. 따라서 $f(x)$의 최댓값은 $3 + k = 3 + 8 = 11$이므로 정답은 ①입니다.',
            'exp_en': 'Since $k>0$, the period is $\\dfrac{2\\pi}{2\\pi/k} = k = 8$. Thus the maximum value of $f(x)$ is $3 + k = 3 + 8 = 11$. The correct answer is ①.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 삼각함수 $y = a\\sin(bx) + c$의 <b>주기 공식과 진폭·평행이동에 따른 최댓값</b>을 정확히 이해하고 있는지를 평가합니다. '
                '$k > 0$이라는 부호 조건 덕분에 절댓값 기호 처리가 깔끔하게 이루어집니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: 주기 조건으로부터 양수 $k$ 결정</b><br>\n'
                '  $k > 0$이므로 $x$의 계수 $\\dfrac{2\\pi}{k}$는 양수입니다. 사인함수의 주기 공식에 의하여 $f(x)$의 주기는 다음과 같습니다:<br>\n'
                '  $$\\text{주기} = \\frac{2\\pi}{\\left|\\frac{2\\pi}{k}\\right|} = k$$<br>\n'
                '  주기가 $8$이므로 $k = 8$입니다.<br>\n'
                '  <b>2단계: 함수 $f(x)$의 최댓값 도출</b><br>\n'
                '  $k = 8$을 대입하면 $f(x) = 3\\sin\\dfrac{\\pi x}{4} + 8$이고, 모든 실수 $x$에 대하여 $-1 \\le \\sin\\dfrac{\\pi x}{4} \\le 1$이므로:<br>\n'
                '  $$-3 + 8 \\le 3\\sin\\frac{\\pi x}{4} + 8 \\le 3 + 8 \\implies 5 \\le f(x) \\le 11$$\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>\n'
                '  따라서 함수 $f(x)$의 최댓값은 $11$이며, 정답은 <b>①번</b>입니다.<br>\n'
                '  💡 <b>실전 팁</b>: $\\sin\\left(\\dfrac{2\\pi}{T}x\\right)$ 꼴은 $x = T$를 넣었을 때 각이 정확히 $2\\pi$가 되므로 주기가 바로 $T$라는 사실을 기억해 두면 1초 만에 주기를 읽을 수 있습니다.\n'
                '</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                '<p>This problem evaluates mastery of the <b>period and range of a transformed sine function</b> $y = a\\sin(bx) + c$. '
                'Because $k > 0$, both the period and vertical shift depend linearly on $k$.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Find $k$ using the period formula</b><br>\n'
                '  Since $k > 0$, the period of $f(x) = 3\\sin\\left(\\dfrac{2\\pi}{k}x\\right) + k$ is:<br>\n'
                '  $$T = \\frac{2\\pi}{2\\pi / k} = k = 8$$<br>\n'
                '  <b>Step 2: Determine the maximum value of $f(x)$</b><br>\n'
                '  Since $-1 \\le \\sin\\left(\\dfrac{\\pi x}{4}\\right) \\le 1$ and the amplitude factor $3 > 0$, the maximum value is:<br>\n'
                '  $$M = 3(1) + k = 3 + 8 = 11$$\n'
                '</p>\n\n'
                '<h4>✨ [Conclusion & Key Takeaway]</h4>\n'
                '<p>\n'
                '  The maximum value of $f(x)$ is $11$, which corresponds to <b>Option ①</b>.\n'
                '</p>'
            ),
        },
    },
    {
        'slug': 'csat27_07',
        'qNum': '7',
        'points': 3,
        'is_short_answer': False,
        'subject': '공통(수학I·II)',
        'title': '[2027학년도 수능 고3 공통 7번] 삼차함수의 극소 조건과 극댓값 구하기',
        'title_en': '[2027 CSAT Math Common #7] Local Minimum Condition and Local Maximum of a Cubic Function',
        'summary_ko': '$f\'(1)=0$으로 미정계수 $a=3$을 결정한 뒤 $f\'(x)=3(x+3)(x-1)$에서 극댓값 $f(-3)$ 계산하기',
        'summary_en': 'Use $f\'(1)=0$ to find $a=3$, factor $f\'(x)=3(x+3)(x-1)$, and evaluate the local maximum $f(-3)=28$.',
        'tags': ['2027학년도 수능', '공통(수학I·II)', '수학II', '미분', '함수의극대와극소', '삼차함수', '7번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': "$x=1$에서 극소 $\\implies f'(1)=0$",
                'desc': '미분가능한 함수가 골짜기(극소)나 산봉우리(극대)를 갖는 지점에서는 접선의 기울기가 $0$임',
                'desc_en': 'At a local extremum of a differentiable function, the derivative equals zero.',
            },
            {
                'sym': "$f'(x) = 3(x+3)(x-1)$",
                'desc': '최고차항 계수가 양수인 삼차함수는 왼쪽 근($x=-3$)에서 극대, 오른쪽 근($x=1$)에서 극소',
                'desc_en': 'A cubic with positive leading coefficient has a local maximum at the smaller root of $f\'(x)=0$ and a local minimum at the larger root.',
            },
            {
                'sym': '극댓값 $= f(-3)$',
                'desc': '$f(x)$가 극대가 되는 $x = -3$을 원래 함수 $f(x)$에 대입한 함숫값',
                'desc_en': 'The local maximum value is the function value $f(-3)$ evaluated at $x = -3$.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 기초 직관] 롤러코스터 골짜기와 산봉우리에서의 순간 기울기',
                'title_en': '🔰 Step 1 · [Elementary Intuition] Slope at the Valley Bottom and Hilltop',
                'knowledge': '매끄러운 롤러코스터 레일이 내리막길(기울기 음수)에서 오르막길(기울기 양수)로 바뀌는 가장 낮은 골짜기 바닥에서는 순간적으로 바닥이 평평해집니다. 평평한 수평선의 기울기는 얼마일까요?',
                'knowledge_en': 'At the exact bottom of a smooth valley where a track transitions from going down to going up, the track is momentarily flat (horizontal).',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '매끄러운 곡선의 가장 낮은 골짜기(극소)나 가장 높은 봉우리(극대)에서 평평한 접선의 기울기는 얼마인가요?',
                        'stem_en': 'What is the slope of the horizontal tangent line at a smooth hilltop or valley bottom?',
                        'options': ['$-2$', '$-1$', '$0$', '$1$', '$2$'],
                        'answer': 3,
                        'exp': '오르내림이 없는 수평선의 기울기는 $0$이므로 극점에서의 미분계수는 $0$입니다.',
                        'exp_en': 'A horizontal line has slope $0$, so the derivative at a smooth extremum is $0$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [기호 번역] $f(x) = x^3 + ax^2 - 3ax + 1$의 도함수 $f\'(x)$ 구하기',
                'title_en': '🌿 Step 2 · [Symbol Translation] Differentiating $f(x) = x^3 + ax^2 - 3ax + 1$',
                'knowledge': '상수 $a$는 숫자처럼 그대로 두고 $x$에 대하여 각 항을 미분합니다. 상수항 $+1$은 미분하면 $0$이 됩니다.',
                'knowledge_en': 'Treat $a$ as a constant and differentiate each term with respect to $x$; the constant $+1$ differentiates to $0$.',
                'questions': [
                    {
                        'level_label': '기호 번역 디딤돌 2',
                        'level_label_en': 'Symbol Translation Step 2',
                        'stem': '함수 $f(x) = x^3 + ax^2 - 3ax + 1$을 $x$에 대하여 미분한 도함수 $f\'(x)$는?',
                        'stem_en': 'What is the derivative $f\'(x)$ of $f(x) = x^3 + ax^2 - 3ax + 1$?',
                        'options': [
                            '$3x^2 + ax - 3a$',
                            '$3x^2 + 2ax - 3a$',
                            '$3x^2 + 2ax - 3a + 1$',
                            '$3x^2 + 2ax + 3a$',
                            '$x^2 + 2ax - 3a$',
                        ],
                        'answer': 2,
                        'exp': '$(x^3)\' = 3x^2$, $(ax^2)\' = 2ax$, $(-3ax)\' = -3a$, $(1)\' = 0$이므로 $f\'(x) = 3x^2 + 2ax - 3a$입니다.',
                        'exp_en': 'Differentiating term by term yields $f\'(x) = 3x^2 + 2ax - 3a$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [핵심 관계식 (가)] $f\'(1) = 0$으로부터 상수 $a$ 구하기',
                'title_en': '🌱 Step 3 · [Core Relation A] Solving $f\'(1) = 0$ for Constant $a$',
                'knowledge': '$x = 1$에서 극소이므로 $f\'(1) = 0$이어야 합니다. $f\'(x) = 3x^2 + 2ax - 3a$에 $x = 1$을 넣어 $a$를 구합니다.',
                'knowledge_en': 'Since $f$ has a local minimum at $x = 1$, substitute $x = 1$ into $f\'(x) = 0$ to find $a$.',
                'questions': [
                    {
                        'level_label': '핵심 관계식 (가) 디딤돌 3',
                        'level_label_en': 'Core Relation A Step 3',
                        'stem': '$f\'(1) = 3 + 2a - 3a = 0$을 만족시키는 상수 $a$의 값은?',
                        'stem_en': 'What value of $a$ satisfies $f\'(1) = 3 + 2a - 3a = 0$?',
                        'options': ['$-3$', '$-1$', '$1$', '$2$', '$3$'],
                        'answer': 5,
                        'exp': '$3 - a = 0$이므로 $a = 3$입니다.',
                        'exp_en': 'From $3 - a = 0$, we obtain $a = 3$.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [중간 전개 (나)] $f\'(x) = 0$을 인수분해하여 극대가 되는 $x$ 좌표 찾기',
                'title_en': '🌳 Step 4 · [Intermediate Step B] Factoring $f\'(x) = 0$ to Locate the Local Maximum',
                'knowledge': '$a = 3$을 대입하면 $f\'(x) = 3x^2 + 6x - 9 = 3(x^2 + 2x - 3) = 3(x + 3)(x - 1)$입니다. $f\'(x)$의 부호가 $+$에서 $-$로 바뀌는 지점이 극대입니다.',
                'knowledge_en': 'With $a = 3$, $f\'(x) = 3(x + 3)(x - 1)$. Since $f\'(x)$ changes sign from $+$ to $-$ at $x = -3$, the local maximum occurs at $x = -3$.',
                'questions': [
                    {
                        'level_label': '중간 전개 (나) 디딤돌 4',
                        'level_label_en': 'Intermediate Step B Step 4',
                        'stem': '$f\'(x) = 3(x + 3)(x - 1)$일 때, 함수 $f(x)$가 극대가 되는 $x$의 값은?',
                        'stem_en': 'Given $f\'(x) = 3(x + 3)(x - 1)$, at what value of $x$ does $f(x)$ attain its local maximum?',
                        'options': ['$-3$', '$-2$', '$-1$', '$0$', '$3$'],
                        'answer': 1,
                        'exp': '$x = -3$ 좌우에서 $f\'(x)$의 부호가 양($+$)에서 음($-$)으로 바뀌므로 $x = -3$에서 극대입니다.',
                        'exp_en': '$f\'(x)$ changes sign from positive to negative across $x = -3$, giving a local maximum at $x = -3$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 레고 조립] 원래 함수에 $x = -3$을 대입해 극댓값 $f(-3)$ 확정하기',
                'title_en': '💎 Step 5 · [Final LEGO Assembly] Evaluating the Local Maximum $f(-3)$',
                'knowledge': '$a = 3$이므로 원래 함수는 $f(x) = x^3 + 3x^2 - 9x + 1$입니다. 여기에 $x = -3$을 대입할 때 부호에 유의하여 계산합니다.',
                'knowledge_en': 'Substitute $x = -3$ into $f(x) = x^3 + 3x^2 - 9x + 1$, paying careful attention to negative signs.',
                'questions': [
                    {
                        'level_label': '최종 레고 조립 디딤돌 5',
                        'level_label_en': 'Final LEGO Assembly Step 5',
                        'stem': '함수 $f(x) = x^3 + 3x^2 - 9x + 1$의 극댓값 $f(-3)$은?',
                        'stem_en': 'What is the local maximum value $f(-3)$ of $f(x) = x^3 + 3x^2 - 9x + 1$?',
                        'options': ['$31$', '$28$', '$25$', '$22$', '$19$'],
                        'answer': 2,
                        'exp': '$f(-3) = (-3)^3 + 3(-3)^2 - 9(-3) + 1 = -27 + 27 + 27 + 1 = 28$입니다.',
                        'exp_en': '$f(-3) = (-3)^3 + 3(-3)^2 - 9(-3) + 1 = -27 + 27 + 27 + 1 = 28$.',
                    }
                ],
            },
        ],
        'final': {
            'stem': '함수 $f(x)=x^3+ax^2-3ax+1$이 $x=1$에서 극소일 때, 함수 $f(x)$의 극댓값은? (단, $a$는 상수이다.) [3점]',
            'stem_en': 'When the function $f(x)=x^3+ax^2-3ax+1$ has a local minimum at $x=1$, what is the local maximum value of $f(x)$? (Here, $a$ is a constant.) [3 points]',
            'options': ['$31$', '$28$', '$25$', '$22$', '$19$'],
            'answer': 2,
            'exp': '$f\'(x)=3x^2+2ax-3a$에서 $f\'(1)=3-a=0 \\implies a=3$입니다. $f\'(x)=3(x+3)(x-1)$이므로 극댓값은 $f(-3)=-27+27+27+1=28$입니다. 정답은 ②입니다.',
            'exp_en': 'From $f\'(x)=3x^2+2ax-3a$, $f\'(1)=3-a=0 \\implies a=3$. Then $f\'(x)=3(x+3)(x-1)$, so the local maximum is $f(-3)=-27+27+27+1=28$. The correct answer is ②.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 다항함수의 <b>극값 조건($f\'(x)=0$ 및 부호 변화)</b>을 이용하여 미정계수를 결정하고 다른 극값을 구하는 수학Ⅱ 미분법의 핵심 유형입니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: $x = 1$에서의 극소 조건으로 상수 $a$ 결정</b><br>\n'
                '  $f(x) = x^3 + ax^2 - 3ax + 1$을 미분하면 $f\'(x) = 3x^2 + 2ax - 3a$입니다.<br>\n'
                '  함수 $f(x)$가 $x = 1$에서 극소이므로 $f\'(1) = 0$이어야 합니다:<br>\n'
                '  $$f\'(1) = 3 + 2a - 3a = 3 - a = 0 \\implies a = 3$$<br>\n'
                '  <b>2단계: 도함수의 인수분해 및 극점의 위치 확인</b><br>\n'
                '  $a = 3$을 대입하면 $f(x) = x^3 + 3x^2 - 9x + 1$이고:<br>\n'
                '  $$f\'(x) = 3x^2 + 6x - 9 = 3(x + 3)(x - 1)$$<br>\n'
                '  $x = 1$ 좌우에서 $f\'(x)$의 부호가 음($-$)에서 양($+$)으로 바뀌므로 $x = 1$에서 극소 조건을 만족하며, $x = -3$ 좌우에서는 양($+$)에서 음($-$)으로 바뀌므로 $x = -3$에서 극대가 됩니다.<br>\n'
                '  <b>3단계: 극댓값 $f(-3)$ 계산</b><br>\n'
                '  $$f(-3) = (-3)^3 + 3(-3)^2 - 9(-3) + 1 = -27 + 27 + 27 + 1 = 28$$\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>\n'
                '  따라서 함수 $f(x)$의 극댓값은 $28$이며, 정답은 <b>②번</b>입니다.<br>\n'
                '  💡 <b>실전 팁</b>: 최고차항 계수가 $k$인 삼차함수의 극댓값과 극솟값의 차 공식 $|f(\\beta) - f(\\alpha)| = \\dfrac{|k|}{2}(\\beta - \\alpha)^3$을 쓰면, $f(1) = -4$이므로 극댓값 $= -4 + \\dfrac{1}{2}(1 - (-3))^3 = -4 + 32 = 28$로 빠르게 검산할 수 있습니다.\n'
                '</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                '<p>This problem tests <b>finding local extrema of a cubic polynomial</b> using the first derivative test: setting $f\'(1) = 0$ determines $a$, and factoring $f\'(x)$ identifies the local maximum.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Determine $a$ from $f\'(1) = 0$</b><br>\n'
                '  Differentiating $f(x) = x^3 + ax^2 - 3ax + 1$ gives $f\'(x) = 3x^2 + 2ax - 3a$. Since $x = 1$ is a local minimum:<br>\n'
                '  $$f\'(1) = 3 + 2a - 3a = 3 - a = 0 \\implies a = 3$$<br>\n'
                '  <b>Step 2: Factor $f\'(x)$ and verify sign changes</b><br>\n'
                '  $$f\'(x) = 3x^2 + 6x - 9 = 3(x + 3)(x - 1)$$<br>\n'
                '  $f\'(x)$ changes from $-$ to $+$ at $x = 1$ (local minimum) and from $+$ to $-$ at $x = -3$ (local maximum).<br>\n'
                '  <b>Step 3: Compute the local maximum value $f(-3)$</b><br>\n'
                '  $$f(-3) = (-3)^3 + 3(-3)^2 - 9(-3) + 1 = -27 + 27 + 27 + 1 = 28$$\n'
                '</p>\n\n'
                '<h4>✨ [Conclusion & Key Takeaway]</h4>\n'
                '<p>\n'
                '  The local maximum value of $f(x)$ is $28$, which corresponds to <b>Option ②</b>.\n'
                '</p>'
            ),
        },
    },
    {
        'slug': 'csat27_08',
        'qNum': '8',
        'points': 3,
        'is_short_answer': False,
        'subject': '공통(수학I·II)',
        'title': '[2027학년도 수능 고3 공통 8번] 로그의 밑의 변환 공식과 성질 활용',
        'title_en': '[2027 CSAT Math Common #8] Logarithm Properties and Change-of-Base Formula',
        'summary_ko': '$\\frac{1}{\\log_8 3} = \\log_3 8 = 3\\log_3 2$로 밑을 $3$으로 통일한 뒤 $\\log_2 3 \\times \\log_3 2 = 1$로 곱 계산하기',
        'summary_en': 'Rewrite $\\frac{1}{\\log_8 3} = \\log_3 8 = 3\\log_3 2$ to simplify $b$, then use $\\log_2 3 \\cdot \\log_3 2 = 1$ to evaluate $a \\times b$.',
        'tags': ['2027학년도 수능', '공통(수학I·II)', '수학I', '지수와로그', '로그의성질', '밑의변환', '8번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': '$\\log_a x^n = n\\log_a x$',
                'desc': '진수의 지수 $n$은 로그 앞으로 내려와 곱해지는 성질',
                'desc_en': 'Power rule for logarithms: an exponent inside the argument moves in front as a multiplier.',
            },
            {
                'sym': '$\\dfrac{1}{\\log_8 3} = \\log_3 8$',
                'desc': '로그의 역수는 밑과 진수의 자리를 서로 바꾼 것과 같음 (밑의 변환 공식)',
                'desc_en': 'Reciprocal change-of-base identity: taking the reciprocal swaps the base and argument.',
            },
            {
                'sym': '$\\log_2 3 \\times \\log_3 2 = 1$',
                'desc': '밑과 진수가 서로 뒤바뀐 두 로그를 곱하면 약분되듯 $1$이 됨',
                'desc_en': 'Product of two logarithms with swapped base and argument equals $1$.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 기초 직관] $9$는 $3$을 몇 번, $8$은 $2$를 몇 번 곱한 수일까?',
                'title_en': '🔰 Step 1 · [Elementary Intuition] Counting Repeated Factors in $9$ and $8$',
                'knowledge': '구구단과 곱셈에서 $9 = 3 \\times 3$은 $3$을 $2$번 곱한 수이고, $8 = 2 \\times 2 \\times 2$는 $2$를 $3$번 곱한 수입니다. 이 작은 횟수 숫자($2$와 $3$)가 로그 계산의 핵심 열쇠가 됩니다!',
                'knowledge_en': 'Since $9 = 3 \\times 3 = 3^2$ and $8 = 2 \\times 2 \\times 2 = 2^3$, the repeat counts $2$ and $3$ unlock the entire logarithm calculation.',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '$9 = 3^p$이고 $8 = 2^q$일 때, 두 횟수의 합 $p + q$는 얼마인가요?',
                        'stem_en': 'When $9 = 3^p$ and $8 = 2^q$, what is the sum $p + q$?',
                        'options': ['$3$', '$4$', '$5$', '$6$', '$7$'],
                        'answer': 3,
                        'exp': '$9 = 3^2$이므로 $p = 2$, $8 = 2^3$이므로 $q = 3$이어서 $p + q = 2 + 3 = 5$입니다.',
                        'exp_en': 'From $9 = 3^2$ ($p = 2$) and $8 = 2^3$ ($q = 3$), we get $p + q = 5$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [기호 번역] $a = \\log_2 9$를 $\\log_2 3$으로 간단히 하기',
                'title_en': '🌿 Step 2 · [Symbol Translation] Simplifying $a = \\log_2 9$ in Terms of $\\log_2 3$',
                'knowledge': '로그 성질 $\\log_2(3^2) = 2\\log_2 3$에 의해 진수의 지수 $2$가 로그 앞으로 내려옵니다.',
                'knowledge_en': 'Using $\\log_2(3^2) = 2\\log_2 3$, bring the exponent $2$ out in front of the logarithm.',
                'questions': [
                    {
                        'level_label': '기호 번역 디딤돌 2',
                        'level_label_en': 'Symbol Translation Step 2',
                        'stem': '$9 = 3^2$임을 이용하여 $a = \\log_2 9$를 바르게 변형한 것은?',
                        'stem_en': 'Using $9 = 3^2$, which expression equals $a = \\log_2 9$?',
                        'options': ['$\\log_2 3$', '$2\\log_2 3$', '$3\\log_2 3$', '$\\dfrac{1}{2}\\log_2 3$', '$9\\log_2 3$'],
                        'answer': 2,
                        'exp': '$a = \\log_2 9 = \\log_2 3^2 = 2\\log_2 3$입니다.',
                        'exp_en': '$a = \\log_2(3^2) = 2\\log_2 3$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [핵심 관계식 (가)] 역수 로그 $\\dfrac{1}{\\log_8 3}$의 밑과 진수 뒤집기',
                'title_en': '🌱 Step 3 · [Core Relation A] Simplifying the Reciprocal Term $\\dfrac{1}{\\log_8 3}$',
                'knowledge': '밑의 변환 공식 $\\dfrac{1}{\\log_x y} = \\log_y x$를 쓰면 $\\dfrac{1}{\\log_8 3} = \\log_3 8$이 되어 앞의 항 $\\log_3 2$와 밑이 $3$으로 똑같아집니다!',
                'knowledge_en': 'By $\\dfrac{1}{\\log_8 3} = \\log_3 8$, both terms in $b$ now share the same base $3$.',
                'questions': [
                    {
                        'level_label': '핵심 관계식 (가) 디딤돌 3',
                        'level_label_en': 'Core Relation A Step 3',
                        'stem': '밑의 변환 공식을 이용하여 $\\dfrac{1}{\\log_8 3}$을 밑이 $3$인 로그 $\\log_3 2$로 나타내면?',
                        'stem_en': 'Express $\\dfrac{1}{\\log_8 3}$ in terms of $\\log_3 2$.',
                        'options': ['$\\dfrac{1}{3}\\log_3 2$', '$\\log_3 2$', '$2\\log_3 2$', '$3\\log_3 2$', '$8\\log_3 2$'],
                        'answer': 4,
                        'exp': '$\\dfrac{1}{\\log_8 3} = \\log_3 8 = \\log_3 2^3 = 3\\log_3 2$입니다.',
                        'exp_en': '$\\dfrac{1}{\\log_8 3} = \\log_3 8 = \\log_3(2^3) = 3\\log_3 2$.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [중간 전개 (나)] $b = \\log_3 2 + 3\\log_3 2$ 정리하기',
                'title_en': '🌳 Step 4 · [Intermediate Step B] Combining Like Logarithm Terms in $b$',
                'knowledge': '사과 $1$개에 사과 $3$개를 더하면 사과 $4$개가 되듯이, $\\log_3 2 + 3\\log_3 2$는 $4\\log_3 2$가 됩니다.',
                'knowledge_en': 'Combining like terms $1 \\cdot \\log_3 2 + 3 \\cdot \\log_3 2$ yields $4\\log_3 2$.',
                'questions': [
                    {
                        'level_label': '중간 전개 (나) 디딤돌 4',
                        'level_label_en': 'Intermediate Step B Step 4',
                        'stem': '$b = \\log_3 2 + \\dfrac{1}{\\log_8 3} = \\log_3 2 + 3\\log_3 2$를 간단히 한 식은?',
                        'stem_en': 'Simplify $b = \\log_3 2 + 3\\log_3 2$.',
                        'options': ['$2\\log_3 2$', '$3\\log_3 2$', '$4\\log_3 2$', '$5\\log_3 2$', '$6\\log_3 2$'],
                        'answer': 3,
                        'exp': '$(1 + 3)\\log_3 2 = 4\\log_3 2$입니다.',
                        'exp_en': '$(1 + 3)\\log_3 2 = 4\\log_3 2$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 레고 조립] $a \\times b$에서 역수 관계인 두 로그 소거하기',
                'title_en': '💎 Step 5 · [Final LEGO Assembly] Evaluating $a \\times b$ via Cancellation',
                'knowledge': '$\\log_2 3 \\times \\log_3 2 = \\dfrac{\\ln 3}{\\ln 2} \\times \\dfrac{\\ln 2}{\\ln 3} = 1$이므로 앞의 계수 $2$와 $4$만 곱하면 끝납니다!',
                'knowledge_en': 'Since $\\log_2 3 \\times \\log_3 2 = 1$, only the numerical coefficients $2$ and $4$ remain to multiply.',
                'questions': [
                    {
                        'level_label': '최종 레고 조립 디딤돌 5',
                        'level_label_en': 'Final LEGO Assembly Step 5',
                        'stem': '$a = 2\\log_2 3$, $b = 4\\log_3 2$일 때, $a \\times b$의 값은?',
                        'stem_en': 'Given $a = 2\\log_2 3$ and $b = 4\\log_3 2$, what is $a \\times b$?',
                        'options': ['$6$', '$7$', '$8$', '$9$', '$10$'],
                        'answer': 3,
                        'exp': '$a \\times b = (2\\log_2 3) \\times (4\\log_3 2) = 8 \\times (\\log_2 3 \\cdot \\log_3 2) = 8 \\times 1 = 8$입니다.',
                        'exp_en': '$a \\times b = 2 \\times 4 \\times (\\log_2 3 \\cdot \\log_3 2) = 8 \\times 1 = 8$.',
                    }
                ],
            },
        ],
        'final': {
            'stem': '두 실수 $a=\\log_2 9$, $b=\\log_3 2 + \\dfrac{1}{\\log_8 3}$ 에 대하여 $a \\times b$의 값은? [3점]',
            'stem_en': 'For two real numbers $a=\\log_2 9$ and $b=\\log_3 2 + \\dfrac{1}{\\log_8 3}$, what is the value of $a \\times b$? [3 points]',
            'options': ['$6$', '$7$', '$8$', '$9$', '$10$'],
            'answer': 3,
            'exp': '$a = 2\\log_2 3$이고 $b = \\log_3 2 + \\log_3 8 = 4\\log_3 2$이므로 $a \\times b = 8\\log_2 3 \\cdot \\log_3 2 = 8$입니다. 정답은 ③입니다.',
            'exp_en': 'Since $a = 2\\log_2 3$ and $b = \\log_3 2 + \\log_3 8 = 4\\log_3 2$, we have $a \\times b = 8(\\log_2 3)(\\log_3 2) = 8$. The correct answer is ③.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 <b>로그의 성질과 밑의 변환 공식</b>을 유기적으로 결합하여 로그가 포함된 두 실수의 곱을 간단히 정리할 수 있는지를 평가합니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: $a$를 소수 진수 $3$에 대한 로그로 정리</b><br>\n'
                '  $$a = \\log_2 9 = \\log_2 3^2 = 2\\log_2 3$$<br>\n'
                '  <b>2단계: 밑의 변환 공식으로 $b$의 밑을 $3$으로 통일</b><br>\n'
                '  $\\dfrac{1}{\\log_8 3} = \\log_3 8 = \\log_3 2^3 = 3\\log_3 2$이므로:<br>\n'
                '  $$b = \\log_3 2 + 3\\log_3 2 = 4\\log_3 2$$<br>\n'
                '  <b>3단계: $a \\times b$ 계산</b><br>\n'
                '  밑의 변환 공식에 의해 $\\log_2 3 \\times \\log_3 2 = 1$이므로:<br>\n'
                '  $$a \\times b = (2\\log_2 3) \\times (4\\log_3 2) = 8(\\log_2 3 \\cdot \\log_3 2) = 8$$\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>\n'
                '  따라서 $a \\times b$의 값은 $8$이며, 정답은 <b>③번</b>입니다.<br>\n'
                '  💡 <b>실전 팁</b>: $\\log_{a^m} b^n = \\dfrac{n}{m}\\log_a b$를 기억하면 $\\log_8 3 = \\dfrac{1}{3}\\log_2 3$이므로 역수 $\\dfrac{1}{\\log_8 3} = \\dfrac{3}{\\log_2 3} = 3\\log_3 2$로도 즉시 변환됩니다.\n'
                '</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                '<p>This problem evaluates fluency with <b>logarithm exponent laws and the change-of-base reciprocal identity</b> $\\dfrac{1}{\\log_x y} = \\log_y x$.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Simplify $a$</b><br>\n'
                '  $$a = \\log_2 9 = \\log_2(3^2) = 2\\log_2 3$$<br>\n'
                '  <b>Step 2: Unify the base in $b$ to $3$</b><br>\n'
                '  Using $\\dfrac{1}{\\log_8 3} = \\log_3 8 = \\log_3(2^3) = 3\\log_3 2$, we obtain:<br>\n'
                '  $$b = \\log_3 2 + 3\\log_3 2 = 4\\log_3 2$$<br>\n'
                '  <b>Step 3: Multiply $a$ and $b$</b><br>\n'
                '  Since $\\log_2 3 \\cdot \\log_3 2 = 1$:<br>\n'
                '  $$a \\times b = (2\\log_2 3)(4\\log_3 2) = 8$$\n'
                '</p>\n\n'
                '<h4>✨ [Conclusion & Key Takeaway]</h4>\n'
                '<p>\n'
                '  The product $a \\times b$ equals $8$, which corresponds to <b>Option ③</b>.\n'
                '</p>'
            ),
        },
    },
    {
        'slug': 'csat27_09',
        'qNum': '9',
        'points': 4,
        'is_short_answer': False,
        'subject': '공통(수학I·II)',
        'title': '[2027학년도 수능 고3 공통 9번] 수직선 위를 움직이는 점의 속도와 움직인 거리',
        'title_en': '[2027 CSAT Math Common #9] Velocity and Total Distance Traveled on a Line',
        'summary_ko': '$v(t)=3(t-1)(t-5)$의 운동 방향 전환 시각 $t=1$을 기준으로 구간을 나누어 $\\int_0^2 |v(t)|\\,dt$ 계산하기',
        'summary_en': 'Split $[0, 2]$ at the turning point $t = 1$ where $v(t) = 3(t-1)(t-5) = 0$, and integrate $|v(t)|$ to find total distance.',
        'tags': ['2027학년도 수능', '공통(수학I·II)', '수학II', '적분', '속도와거리', '움직인거리', '9번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': '움직인 거리 $= \\displaystyle\\int_0^2 |v(t)|\\,dt$',
                'desc': '위치의 변화량이 아닌 실제 이동 거리는 속력 $|v(t)|$를 정적분하여 구함',
                'desc_en': 'Total distance traveled is the definite integral of speed $|v(t)|$, not signed velocity.',
            },
            {
                'sym': '$v(t) = 3(t-1)(t-5) = 0$',
                'desc': '속도의 부호가 바뀌며 점 $\\mathrm{P}$가 운동 방향을 바꾸는 시각($t=1, 5$)을 찾는 방정식',
                'desc_en': 'Zeros of velocity identify times where particle $\\mathrm{P}$ reverses direction.',
            },
            {
                'sym': '$[0, 1]$ 전진 $+\\; [1, 2]$ 후진',
                'desc': '$0 \\le t < 1$에서는 양의 방향 이동, $1 < t \\le 2$에서는 음의 방향 이동이므로 두 거리를 모두 양수로 더함',
                'desc_en': 'Add the forward distance on $[0, 1]$ and the backward distance magnitude on $[1, 2]$.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 기초 직관] 앞으로 $7$걸음 갔다가 뒤로 $5$걸음 돌아왔을 때 걸은 총걸음 수',
                'title_en': '🔰 Step 1 · [Elementary Intuition] Total Steps Walked: $7$ Forward Then $5$ Backward',
                'knowledge': '출발선 $0$에서 앞으로 $7$걸음 걸어간 뒤, 뒤돌아서 $5$걸음 걸어오면 현재 서 있는 위치는 $7 - 5 = 2$이지만, 내 다리가 실제로 걸은 총거리는 앞으로 간 거리와 뒤로 간 거리를 모두 더해야 합니다!',
                'knowledge_en': 'Walking $7$ steps forward and $5$ steps backward leaves you at position $2$, but your legs actually walked $7 + 5$ steps in total!',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '수직선 원점 $0$에서 오른쪽으로 $7$칸 이동한 뒤 방향을 바꾸어 왼쪽으로 $5$칸 이동했을 때, 실제로 움직인 총거리는 몇 칸인가요?',
                        'stem_en': 'If a point moves $7$ units right from $0$ and then $5$ units left, what is the total distance traveled?',
                        'options': ['$2$', '$5$', '$7$', '$12$', '$35$'],
                        'answer': 4,
                        'exp': '앞으로 간 거리 $7$칸과 뒤로 간 거리 $5$칸을 모두 더하므로 움직인 총거리는 $7 + 5 = 12$칸입니다.',
                        'exp_en': 'Total distance adds both magnitudes: $7 + 5 = 12$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [기호 번역] $0 \\le t \\le 2$에서 운동 방향이 바뀌는 시각 찾기',
                'title_en': '🌿 Step 2 · [Symbol Translation] Finding Where Velocity Changes Sign on $[0, 2]$',
                'knowledge': '$v(t) = 3t^2 - 18t + 15 = 3(t^2 - 6t + 5) = 3(t - 1)(t - 5)$로 인수분해됩니다. 구간 $[0, 2]$ 안에서 $v(t) = 0$이 되는 시각을 찾아 적분 구간을 나눕니다.',
                'knowledge_en': 'Factor $v(t) = 3(t - 1)(t - 5)$ to find where $v(t) = 0$ inside the interval $[0, 2]$.',
                'questions': [
                    {
                        'level_label': '기호 번역 디딤돌 2',
                        'level_label_en': 'Symbol Translation Step 2',
                        'stem': '속도 $v(t) = 3t^2 - 18t + 15$에 대하여 $0 \\le t \\le 2$에서 점 $\\mathrm{P}$의 운동 방향이 바뀌는 시각 $t$는?',
                        'stem_en': 'At what time $t \\in [0, 2]$ does particle $\\mathrm{P}$ with velocity $v(t) = 3t^2 - 18t + 15$ change direction?',
                        'options': ['$t = \\dfrac{1}{2}$', '$t = 1$', '$t = \\dfrac{3}{2}$', '$t = 2$', '바뀌지 않는다'],
                        'answer': 2,
                        'exp': '$3(t - 1)(t - 5) = 0$에서 $t = 1$ 또는 $t = 5$이고, 구간 $[0, 2]$에 속하며 부호가 $+$에서 $-$로 바뀌는 시각은 $t = 1$입니다.',
                        'exp_en': 'From $3(t - 1)(t - 5) = 0$, the sign change inside $[0, 2]$ occurs at $t = 1$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [핵심 관계식 (가)] $t = 0$부터 $t = 1$까지 앞으로 이동한 거리 구하기',
                'title_en': '🌱 Step 3 · [Core Relation A] Forward Distance on $[0, 1]$',
                'knowledge': '$0 \\le t \\le 1$에서는 $v(t) \\ge 0$이므로 $|v(t)| = 3t^2 - 18t + 15$입니다. 부정적분 $x(t) = t^3 - 9t^2 + 15t$를 이용해 $\\int_0^1 v(t)\\,dt$를 구합니다.',
                'knowledge_en': 'On $[0, 1]$, $v(t) \\ge 0$, so integrate $3t^2 - 18t + 15$ using antiderivative $t^3 - 9t^2 + 15t$.',
                'questions': [
                    {
                        'level_label': '핵심 관계식 (가) 디딤돌 3',
                        'level_label_en': 'Core Relation A Step 3',
                        'stem': '정적분 $\\displaystyle\\int_0^1 (3t^2 - 18t + 15)\\,dt$의 값은?',
                        'stem_en': 'What is the value of $\\displaystyle\\int_0^1 (3t^2 - 18t + 15)\\,dt$?',
                        'options': ['$5$', '$6$', '$7$', '$8$', '$9$'],
                        'answer': 3,
                        'exp': '$\\Big[t^3 - 9t^2 + 15t\\Big]_0^1 = (1 - 9 + 15) - 0 = 7$입니다.',
                        'exp_en': '$\\Big[t^3 - 9t^2 + 15t\\Big]_0^1 = 1 - 9 + 15 = 7$.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [중간 전개 (나)] $t = 1$부터 $t = 2$까지 뒤로 이동한 거리 구하기',
                'title_en': '🌳 Step 4 · [Intermediate Step B] Backward Distance on $[1, 2]$',
                'knowledge': '$1 \\le t \\le 2$에서는 $v(t) \\le 0$이므로 $|v(t)| = -v(t)$입니다. 정적분 $\\int_1^2 v(t)\\,dt$의 절댓값을 구하면 뒤로 이동한 거리가 됩니다.',
                'knowledge_en': 'On $[1, 2]$, $v(t) \\le 0$, so the distance traveled is $-\\int_1^2 v(t)\\,dt = \\left|\\int_1^2 v(t)\\,dt\\right|$.',
                'questions': [
                    {
                        'level_label': '중간 전개 (나) 디딤돌 4',
                        'level_label_en': 'Intermediate Step B Step 4',
                        'stem': '구간 $[1, 2]$에서 점 $\\mathrm{P}$가 움직인 거리 $\\displaystyle\\int_1^2 |3t^2 - 18t + 15|\\,dt$의 값은?',
                        'stem_en': 'What is the distance $\\displaystyle\\int_1^2 |3t^2 - 18t + 15|\\,dt$ traveled on $[1, 2]$?',
                        'options': ['$2$', '$3$', '$4$', '$5$', '$6$'],
                        'answer': 4,
                        'exp': '$F(t) = t^3 - 9t^2 + 15t$라 하면 $F(2) = 8 - 36 + 30 = 2$, $F(1) = 7$이므로 $|F(2) - F(1)| = |2 - 7| = 5$입니다.',
                        'exp_en': 'Let $F(t) = t^3 - 9t^2 + 15t$. Since $F(2) = 2$ and $F(1) = 7$, the distance is $|2 - 7| = 5$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 레고 조립] $t = 0$부터 $t = 2$까지 총 움직인 거리 확정하기',
                'title_en': '💎 Step 5 · [Final LEGO Assembly] Total Distance Traveled on $[0, 2]$',
                'knowledge': '두 구간 $[0, 1]$과 $[1, 2]$에서 각각 움직인 거리 $7$과 $5$를 더하여 최종 정답을 확정합니다.',
                'knowledge_en': 'Sum the distances from $[0, 1]$ and $[1, 2]$ to obtain the total distance traveled.',
                'questions': [
                    {
                        'level_label': '최종 레고 조립 디딤돌 5',
                        'level_label_en': 'Final LEGO Assembly Step 5',
                        'stem': '시각 $t = 0$부터 $t = 2$까지 점 $\\mathrm{P}$가 움직인 총거리는?',
                        'stem_en': 'What is the total distance traveled by particle $\\mathrm{P}$ from $t = 0$ to $t = 2$?',
                        'options': ['$9$', '$10$', '$11$', '$12$', '$13$'],
                        'answer': 4,
                        'exp': '$\\displaystyle\\int_0^2 |v(t)|\\,dt = 7 + 5 = 12$입니다.',
                        'exp_en': '$\\displaystyle\\int_0^2 |v(t)|\\,dt = 7 + 5 = 12$.',
                    }
                ],
            },
        ],
        'final': {
            'stem': '수직선 위를 움직이는 점 $\\mathrm{P}$가 있다. 시각이 $t\\;(t \\ge 0)$일 때 점 $\\mathrm{P}$의 속도 $v(t)$는 $v(t)=3t^2-18t+15$ 이다. 시각 $t=0$부터 $t=2$까지 점 $\\mathrm{P}$가 움직인 거리는? [4점]',
            'stem_en': 'A point $\\mathrm{P}$ moves along a number line with velocity $v(t)=3t^2-18t+15$ at time $t\\;(t \\ge 0)$. What is the total distance traveled by $\\mathrm{P}$ from $t=0$ to $t=2$? [4 points]',
            'options': ['$9$', '$10$', '$11$', '$12$', '$13$'],
            'answer': 4,
            'exp': '$v(t)=3(t-1)(t-5)$이므로 움직인 거리는 $\\displaystyle\\int_0^1 (3t^2-18t+15)\\,dt - \\int_1^2 (3t^2-18t+15)\\,dt = 7 + 5 = 12$입니다. 정답은 ④입니다.',
            'exp_en': 'Since $v(t)=3(t-1)(t-5)$, the total distance is $\\displaystyle\\int_0^1 v(t)\\,dt - \\int_1^2 v(t)\\,dt = 7 + 5 = 12$. The correct answer is ④.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 수직선 위를 움직이는 점의 <b>위치의 변화량($\\int v(t)\\,dt$)과 실제로 움직인 거리($\\int |v(t)|\\,dt$)</b>를 정확히 구분하고, 운동 방향이 바뀌는 시각을 기준으로 절댓값 정적분을 수행할 수 있는지를 평가합니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: 속도 $v(t)$의 부호 조사</b><br>\n'
                '  $$v(t) = 3t^2 - 18t + 15 = 3(t^2 - 6t + 5) = 3(t - 1)(t - 5)$$<br>\n'
                '  구간 $[0, 2]$에서 $0 \\le t \\le 1$일 때 $v(t) \\ge 0$이고, $1 \\le t \\le 2$일 때 $v(t) \\le 0$입니다.<br>\n'
                '  <b>2단계: 구간을 나누어 $|v(t)|$ 정적분하기</b><br>\n'
                '  $F(t) = t^3 - 9t^2 + 15t$로 놓으면 $F(0) = 0$, $F(1) = 1 - 9 + 15 = 7$, $F(2) = 8 - 36 + 30 = 2$이므로:<br>\n'
                '  $$\\int_0^2 |v(t)|\\,dt = \\int_0^1 v(t)\\,dt - \\int_1^2 v(t)\\,dt = \\big(F(1) - F(0)\\big) - \\big(F(2) - F(1)\\big)$$<br>\n'
                '  $$= (7 - 0) - (2 - 7) = 7 + 5 = 12$$\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>\n'
                '  따라서 시각 $t = 0$부터 $t = 2$까지 점 $\\mathrm{P}$가 움직인 거리는 $12$이며, 정답은 <b>④번</b>입니다.<br>\n'
                '  💡 <b>실전 팁</b>: 원점 출발 위치 함수 $x(t) = t^3 - 9t^2 + 15t$를 먼저 구해 $x(0) = 0 \\to x(1) = 7 \\to x(2) = 2$의 꺾임 이동 경로를 적으면 $|7 - 0| + |2 - 7| = 12$로 부호 실수 없이 암산할 수 있습니다.\n'
                '</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                '<p>This problem tests the distinction between net displacement and <b>total distance traveled</b> $\\displaystyle\\int_0^2 |v(t)|\\,dt$ when velocity changes sign within the interval of integration.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Factor $v(t)$ to find direction reversals on $[0, 2]$</b><br>\n'
                '  $$v(t) = 3t^2 - 18t + 15 = 3(t - 1)(t - 5)$$<br>\n'
                '  Thus $v(t) \\ge 0$ on $[0, 1]$ and $v(t) \\le 0$ on $[1, 2]$.<br>\n'
                '  <b>Step 2: Integrate $|v(t)|$ over $[0, 1]$ and $[1, 2]$</b><br>\n'
                '  Let $F(t) = t^3 - 9t^2 + 15t$. Since $F(0) = 0$, $F(1) = 7$, and $F(2) = 2$:<br>\n'
                '  $$\\int_0^2 |v(t)|\\,dt = \\big(F(1) - F(0)\\big) + \\big(F(1) - F(2)\\big) = 7 + 5 = 12$$\n'
                '</p>\n\n'
                '<h4>✨ [Conclusion & Key Takeaway]</h4>\n'
                '<p>\n'
                '  The total distance traveled from $t = 0$ to $t = 2$ is $12$, which corresponds to <b>Option ④</b>.\n'
                '</p>'
            ),
        },
    },
    {
        'slug': 'csat27_10',
        'qNum': '10',
        'points': 4,
        'is_short_answer': False,
        'subject': '공통(수학I·II)',
        'title': '[2027학년도 수능 고3 공통 10번] 사인법칙과 코사인법칙을 결합한 삼각형의 변의 길이',
        'title_en': '[2027 CSAT Math Common #10] Combining Law of Sines and Law of Cosines in a Triangle',
        'summary_ko': '외접원의 넓이 $17\\pi$에서 $R=\\sqrt{17}$, $\\sin A:\\sin B=3:4$에서 $a=3k, b=4k$로 놓고 사인·코사인법칙 연립하기',
        'summary_en': 'Use circumcircle area $17\\pi$ ($R=\\sqrt{17}$), set $a=3k, b=4k$ from $\\sin A:\\sin B=3:4$, and combine the Laws of Sines and Cosines.',
        'tags': ['2027학년도 수능', '공통(수학I·II)', '수학I', '삼각함수', '사인법칙', '코사인법칙', '외접원', '10번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': '$a : b = \\sin A : \\sin B$',
                'desc': '사인법칙에 의해 삼각형의 세 변의 길이의 비는 마주 보는 각의 사인값의 비와 같음',
                'desc_en': 'By the Law of Sines, side lengths are proportional to the sines of their opposite angles.',
            },
            {
                'sym': '$\\dfrac{c}{\\sin C} = 2R$',
                'desc': '변 $c$를 마주 보는 각의 사인값 $\\sin C$로 나누면 외접원의 지름 $2R$이 됨',
                'desc_en': 'Law of Sines relating side $c$, opposite angle $C$, and circumradius $R$.',
            },
            {
                'sym': '$c^2 = a^2 + b^2 - 2ab\\cos C$',
                'desc': '두 변 $a, b$와 끼인각 $C$의 코사인값으로 마주 보는 변 $c$를 구하는 코사인법칙',
                'desc_en': 'Law of Cosines expressing $c^2$ in terms of sides $a, b$ and included angle $C$.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 기초 직관] 원의 넓이가 $17\\pi$일 때 반지름의 제곱 구하기',
                'title_en': '🔰 Step 1 · [Elementary Intuition] Finding $R^2$ When Circle Area Is $17\\pi$',
                'knowledge': '초등학교에서 배운 원의 넓이는 $(\\text{반지름}) \\times (\\text{반지름}) \\times (\\text{원주율 } \\pi)$입니다. 원의 넓이가 $17\\pi$라면 반지름을 두 번 곱한 값은 얼마일까요?',
                'knowledge_en': 'The area of a circle is $\\pi \\times R \\times R$. Comparing $\\pi R^2$ with $17\\pi$ immediately reveals $R^2$.',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '반지름의 길이가 $R$인 외접원의 넓이 $\\pi R^2$이 $17\\pi$일 때, 양수 $R$의 값은?',
                        'stem_en': 'When a circle of radius $R > 0$ has area $\\pi R^2 = 17\\pi$, what is $R$?',
                        'options': ['$\\sqrt{13}$', '$\\sqrt{15}$', '$4$', '$\\sqrt{17}$', '$17$'],
                        'answer': 4,
                        'exp': '$\\pi R^2 = 17\\pi$에서 $R^2 = 17$이고 $R > 0$이므로 $R = \\sqrt{17}$입니다.',
                        'exp_en': 'From $R^2 = 17$ and $R > 0$, we get $R = \\sqrt{17}$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [기호 번역] $\\sin A : \\sin B = 3 : 4$를 두 변 $a, b$의 길이 비로 바꾸기',
                'title_en': '🌿 Step 2 · [Symbol Translation] Translating $\\sin A : \\sin B = 3 : 4$ into Side Ratio $a : b$',
                'knowledge': '사인법칙 $a = 2R\\sin A$, $b = 2R\\sin B$에 의해 $\\overline{\\mathrm{BC}} = a$와 $\\overline{\\mathrm{CA}} = b$의 길이의 비도 $3 : 4$입니다. 따라서 양수 $k$를 도입해 $a = 3k$, $b = 4k$로 놓습니다.',
                'knowledge_en': 'By the Law of Sines, $a : b = \\sin A : \\sin B = 3 : 4$, so we write $a = 3k$ and $b = 4k$ ($k > 0$), where $\\overline{\\mathrm{BC}} = a = 3k$.',
                'questions': [
                    {
                        'level_label': '기호 번역 디딤돌 2',
                        'level_label_en': 'Symbol Translation Step 2',
                        'stem': '삼각형 $\\mathrm{ABC}$에서 $\\sin A : \\sin B = 3 : 4$일 때, $\\overline{\\mathrm{BC}} = a$, $\\overline{\\mathrm{CA}} = b$를 양수 $k$로 바르게 나타낸 것은?',
                        'stem_en': 'Given $\\sin A : \\sin B = 3 : 4$, how can $a = \\overline{\\mathrm{BC}}$ and $b = \\overline{\\mathrm{CA}}$ be parameterized with $k > 0$?',
                        'options': [
                            '$a = 4k,\\; b = 3k$',
                            '$a = 3k,\\; b = 4k$',
                            '$a = 3k,\\; b = 5k$',
                            '$a = 9k,\\; b = 16k$',
                            '$a = \\sqrt{3}k,\\; b = 2k$',
                        ],
                        'answer': 2,
                        'exp': '각 $A$의 대변이 $\\overline{\\mathrm{BC}} = a$, 각 $B$의 대변이 $\\overline{\\mathrm{CA}} = b$이므로 $a : b = 3 : 4 \\implies a = 3k,\\; b = 4k$입니다.',
                        'exp_en': 'Side $a = \\overline{\\mathrm{BC}}$ is opposite $A$ and $b = \\overline{\\mathrm{CA}}$ is opposite $B$, so $a = 3k$ and $b = 4k$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [핵심 관계식 (가)] 코사인법칙으로 변 $c = \\overline{\\mathrm{AB}}$를 $k$로 나타내기',
                'title_en': '🌱 Step 3 · [Core Relation A] Expressing $c$ in Terms of $k$ via Law of Cosines',
                'knowledge': '코사인법칙 $c^2 = a^2 + b^2 - 2ab\\cos C$에 $a = 3k$, $b = 4k$, $\\cos C = \\dfrac{1}{3}$을 대입하면 놀랍게도 $17k^2$이 등장합니다!',
                'knowledge_en': 'Substitute $a = 3k$, $b = 4k$, and $\\cos C = \\dfrac{1}{3}$ into $c^2 = a^2 + b^2 - 2ab\\cos C$.',
                'questions': [
                    {
                        'level_label': '핵심 관계식 (가) 디딤돌 3',
                        'level_label_en': 'Core Relation A Step 3',
                        'stem': '$a = 3k$, $b = 4k$ ($k > 0$), $\\cos C = \\dfrac{1}{3}$을 $c^2 = a^2 + b^2 - 2ab\\cos C$에 대입하여 얻은 $c$의 식은?',
                        'stem_en': 'Substituting $a = 3k$, $b = 4k$, and $\\cos C = \\dfrac{1}{3}$ into the Law of Cosines gives $c = ?$',
                        'options': ['$\\sqrt{13}k$', '$4k$', '$\\sqrt{17}k$', '$\\sqrt{19}k$', '$5k$'],
                        'answer': 3,
                        'exp': '$c^2 = 9k^2 + 16k^2 - 2(3k)(4k) \\cdot \\dfrac{1}{3} = 25k^2 - 8k^2 = 17k^2$이므로 $c = \\sqrt{17}k$입니다.',
                        'exp_en': '$c^2 = 9k^2 + 16k^2 - 8k^2 = 17k^2$, so $c = \\sqrt{17}k$ ($k > 0$).',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [중간 전개 (나)] $\\sin C$를 구하고 사인법칙 $c = 2R\\sin C$ 적용하기',
                'title_en': '🌳 Step 4 · [Intermediate Step B] Finding $\\sin C$ and Applying $c = 2R\\sin C$',
                'knowledge': '삼각형의 내각 $C$에서 $\\sin C > 0$이므로 $\\sin C = \\sqrt{1 - \\cos^2 C} = \\sqrt{1 - \\dfrac{1}{9}} = \\dfrac{2\\sqrt{2}}{3}$입니다. 이제 $c = 2R\\sin C$와 $c = \\sqrt{17}k$를 비교합니다.',
                'knowledge_en': 'Since $0 < C < \\pi$, $\\sin C = \\sqrt{1 - (1/3)^2} = \\dfrac{2\\sqrt{2}}{3}$. Compare $c = \\sqrt{17}k$ with $c = 2R\\sin C$.',
                'questions': [
                    {
                        'level_label': '중간 전개 (나) 디딤돌 4',
                        'level_label_en': 'Intermediate Step B Step 4',
                        'stem': '$R = \\sqrt{17}$, $\\sin C = \\dfrac{2\\sqrt{2}}{3}$일 때, $\\sqrt{17}k = 2R\\sin C$를 만족시키는 양수 $k$의 값은?',
                        'stem_en': 'With $R = \\sqrt{17}$ and $\\sin C = \\dfrac{2\\sqrt{2}}{3}$, solve $\\sqrt{17}k = 2R\\sin C$ for $k$.',
                        'options': ['$\\dfrac{2\\sqrt{2}}{3}$', '$\\sqrt{2}$', '$\\dfrac{4\\sqrt{2}}{3}$', '$\\dfrac{4\\sqrt{3}}{3}$', '$2\\sqrt{2}$'],
                        'answer': 3,
                        'exp': '$\\sqrt{17}k = 2\\sqrt{17} \\times \\dfrac{2\\sqrt{2}}{3}$에서 양변의 $\\sqrt{17}$을 약분하면 $k = \\dfrac{4\\sqrt{2}}{3}$입니다.',
                        'exp_en': 'Dividing $\\sqrt{17}k = 2\\sqrt{17} \\cdot \\dfrac{2\\sqrt{2}}{3}$ by $\\sqrt{17}$ gives $k = \\dfrac{4\\sqrt{2}}{3}$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 레고 조립] 선분 $\\mathrm{BC}$의 길이 $a = 3k$ 확정하기',
                'title_en': '💎 Step 5 · [Final LEGO Assembly] Computing $\\overline{\\mathrm{BC}} = a = 3k$',
                'knowledge': '구하고자 하는 선분 $\\mathrm{BC}$는 각 $A$의 대변 $a = 3k$입니다. $k = \\dfrac{4\\sqrt{2}}{3}$에 $3$을 곱하면 분모 $3$이 깔끔하게 약분됩니다!',
                'knowledge_en': 'Since $\\overline{\\mathrm{BC}} = a = 3k$, multiply $k = \\dfrac{4\\sqrt{2}}{3}$ by $3$.',
                'questions': [
                    {
                        'level_label': '최종 레고 조립 디딤돌 5',
                        'level_label_en': 'Final LEGO Assembly Step 5',
                        'stem': '$k = \\dfrac{4\\sqrt{2}}{3}$일 때, 선분 $\\mathrm{BC}$의 길이 $a = 3k$는?',
                        'stem_en': 'Given $k = \\dfrac{4\\sqrt{2}}{3}$, what is the length $\\overline{\\mathrm{BC}} = 3k$?',
                        'options': ['$3\\sqrt{3}$', '$4\\sqrt{2}$', '$4\\sqrt{3}$', '$5\\sqrt{2}$', '$3\\sqrt{6}$'],
                        'answer': 2,
                        'exp': '$\\overline{\\mathrm{BC}} = 3 \\times \\dfrac{4\\sqrt{2}}{3} = 4\\sqrt{2}$입니다.',
                        'exp_en': '$\\overline{\\mathrm{BC}} = 3 \\times \\dfrac{4\\sqrt{2}}{3} = 4\\sqrt{2}$.',
                    }
                ],
            },
        ],
        'final': {
            'stem': '삼각형 $\\mathrm{ABC}$에서 $\\sin A : \\sin B = 3 : 4$이고 $\\cos C = \\dfrac{1}{3}$이다. 삼각형 $\\mathrm{ABC}$의 외접원의 넓이가 $17\\pi$일 때, 선분 $\\mathrm{BC}$의 길이는? [4점]',
            'stem_en': 'In triangle $\\mathrm{ABC}$, $\\sin A : \\sin B = 3 : 4$ and $\\cos C = \\dfrac{1}{3}$. When the area of the circumcircle of triangle $\\mathrm{ABC}$ is $17\\pi$, what is the length of segment $\\mathrm{BC}$? [4 points]',
            'options': ['$3\\sqrt{3}$', '$4\\sqrt{2}$', '$4\\sqrt{3}$', '$5\\sqrt{2}$', '$3\\sqrt{6}$'],
            'answer': 2,
            'exp': '$R=\\sqrt{17}$, $\\sin C = \\dfrac{2\\sqrt{2}}{3}$이고 $a=3k, b=4k$로 놓으면 코사인법칙에 의해 $c = \\sqrt{17}k$입니다. $c = 2R\\sin C = \\dfrac{4\\sqrt{34}}{3}$에서 $k = \\dfrac{4\\sqrt{2}}{3}$이므로 $\\overline{\\mathrm{BC}} = 3k = 4\\sqrt{2}$입니다. 정답은 ②입니다.',
            'exp_en': 'With $R=\\sqrt{17}$, $\\sin C = \\dfrac{2\\sqrt{2}}{3}$, and $a=3k, b=4k$, the Law of Cosines gives $c = \\sqrt{17}k$. Equating this to $2R\\sin C = 2\\sqrt{17}\\cdot\\dfrac{2\\sqrt{2}}{3}$ yields $k = \\dfrac{4\\sqrt{2}}{3}$, so $\\overline{\\mathrm{BC}} = 3k = 4\\sqrt{2}$. The correct answer is ②.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 삼각형의 외접원 조건과 사인 비례 조건이 함께 주어졌을 때 <b>사인법칙과 코사인법칙을 유기적으로 연립</b>하여 변의 길이를 구하는 수학Ⅰ 도형 영역의 핵심 4점 문항입니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: 외접원의 반지름 $R$과 $\\sin C$ 구하기</b><br>\n'
                '  외접원의 반지름을 $R$이라 하면 $\\pi R^2 = 17\\pi \\implies R = \\sqrt{17}$입니다.<br>\n'
                '  또한 $0 < C < \\pi$이고 $\\cos C = \\dfrac{1}{3}$이므로:<br>\n'
                '  $$\\sin C = \\sqrt{1 - \\cos^2 C} = \\sqrt{1 - \\frac{1}{9}} = \\frac{2\\sqrt{2}}{3}$$<br>\n'
                '  <b>2단계: 사인법칙과 코사인법칙으로 $c$와 비례상수 $k$ 연결</b><br>\n'
                '  사인법칙에 의해 $a : b = \\sin A : \\sin B = 3 : 4$이므로 $a = 3k,\\; b = 4k$ ($k > 0$)라 놓습니다. 코사인법칙에 의하여:<br>\n'
                '  $$c^2 = (3k)^2 + (4k)^2 - 2(3k)(4k)\\cdot\\frac{1}{3} = 9k^2 + 16k^2 - 8k^2 = 17k^2 \\implies c = \\sqrt{17}k$$<br>\n'
                '  한편 사인법칙 $c = 2R\\sin C$에 대입하면:<br>\n'
                '  $$\\sqrt{17}k = 2\\sqrt{17} \\times \\frac{2\\sqrt{2}}{3} \\implies k = \\frac{4\\sqrt{2}}{3}$$<br>\n'
                '  <b>3단계: 선분 $\\mathrm{BC}$의 길이 도출</b><br>\n'
                '  $$\\overline{\\mathrm{BC}} = a = 3k = 3 \\times \\frac{4\\sqrt{2}}{3} = 4\\sqrt{2}$$\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>\n'
                '  따라서 선분 $\\mathrm{BC}$의 길이는 $4\\sqrt{2}$이며, 정답은 <b>②번</b>입니다.<br>\n'
                '  💡 <b>실전 팁</b>: $c^2 = \\dfrac{544}{9}$를 미리 전개하지 않고 $c = \\sqrt{17}k$와 $2R\\sin C = 2\\sqrt{17}\\sin C$에서 양변의 $\\sqrt{17}$을 바로 약분하면 큰 수의 제곱 계산을 통째로 생략할 수 있습니다.\n'
                '</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                '<p>This 4-point problem synthesizes the <b>Law of Sines</b> (for both the circumradius relation and side ratio $a:b$) with the <b>Law of Cosines</b> to determine side $\\overline{\\mathrm{BC}} = a$.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Find circumradius $R$ and $\\sin C$</b><br>\n'
                '  From $\\pi R^2 = 17\\pi$, we have $R = \\sqrt{17}$. Since $0 < C < \\pi$ and $\\cos C = \\dfrac{1}{3}$:<br>\n'
                '  $$\\sin C = \\sqrt{1 - \\frac{1}{9}} = \\frac{2\\sqrt{2}}{3}$$<br>\n'
                '  <b>Step 2: Parameterize $a, b$ and apply the Laws of Cosines and Sines</b><br>\n'
                '  Since $a : b = \\sin A : \\sin B = 3 : 4$, set $a = 3k$ and $b = 4k$ ($k > 0$). By the Law of Cosines:<br>\n'
                '  $$c^2 = 9k^2 + 16k^2 - 2(3k)(4k)\\left(\\frac{1}{3}\\right) = 17k^2 \\implies c = \\sqrt{17}k$$<br>\n'
                '  By the Law of Sines, $c = 2R\\sin C = 2\\sqrt{17} \\cdot \\dfrac{2\\sqrt{2}}{3}$, so canceling $\\sqrt{17}$ yields $k = \\dfrac{4\\sqrt{2}}{3}$.<br>\n'
                '  <b>Step 3: Compute $\\overline{\\mathrm{BC}} = a$</b><br>\n'
                '  $$\\overline{\\mathrm{BC}} = 3k = 4\\sqrt{2}$$\n'
                '</p>\n\n'
                '<h4>✨ [Conclusion & Key Takeaway]</h4>\n'
                '<p>\n'
                '  The length of segment $\\mathrm{BC}$ is $4\\sqrt{2}$, which corresponds to <b>Option ②</b>.\n'
                '</p>'
            ),
        },
    },
    {
        'slug': 'csat27_11',
        'qNum': '11',
        'points': 4,
        'is_short_answer': False,
        'subject': '공통(수학I·II)',
        'title': '[2027학년도 수능 고3 공통 11번] 곱의 미분법과 곡선의 접선의 방정식',
        'title_en': '[2027 CSAT Math Common #11] Product Rule and Tangent Line Equation to $y=x^2 f(x)$',
        'summary_ko': '접선 $y=7x-11$에서 접점의 함숫값 $f(1)=-4$와 기울기 $g\'(1)=2f(1)+f\'(1)=7$을 연립하여 $f\'(1)$ 도출하기',
        'summary_en': 'Extract $f(1)=-4$ and slope $g\'(1)=7$ from the tangent line $y=7x-11$ to $g(x)=x^2 f(x)$, then solve $2f(1)+f\'(1)=7$.',
        'tags': ['2027학년도 수능', '공통(수학I·II)', '수학II', '미분', '접선의방정식', '곱의미분법', '11번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': '접점 $(1, f(1))$은 접선 위의 점',
                'desc': '곡선과 접선은 접점에서 만나므로 접선 $y = 7x - 11$에 $x = 1$을 넣은 값이 바로 $f(1)$임',
                'desc_en': 'Because the curve and tangent share the point of tangency, substituting $x=1$ into $y=7x-11$ gives $f(1)$.',
            },
            {
                'sym': "$g(x) = x^2 f(x) \\implies g'(x) = 2x f(x) + x^2 f'(x)$",
                'desc': '두 함수 $x^2$과 $f(x)$의 곱을 미분하는 곱의 미분법 공식',
                'desc_en': 'Product rule applied to $g(x) = x^2 f(x)$.',
            },
            {
                'sym': "$g'(1) = 7$",
                'desc': '$x = 1$에서의 미분계수 $g\'(1)$은 접선 $y = 7x - 11$의 기울기 $7$과 같음',
                'desc_en': 'The derivative $g\'(1)$ equals the slope $7$ of the tangent line $y = 7x - 11$.',
            },
        ],
        'levels': [
            {
                'title': '🔰 1단계 · [초등 기초 직관] 직선 $y = 7x - 11$에서 $x = 1$일 때 $y$의 값 구하기',
                'title_en': '🔰 Step 1 · [Elementary Intuition] Evaluating $y = 7x - 11$ at $x = 1$',
                'knowledge': '직선 $y = 7 \\times x - 11$에 $x = 1$을 넣으면 $7 - 11$이 됩니다. $7$에서 $11$을 빼면 $0$보다 $4$만큼 작은 음수 $-4$가 됩니다.',
                'knowledge_en': 'Substituting $x = 1$ into $y = 7x - 11$ gives $7 - 11 = -4$.',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': '식 $7 \\times x - 11$에 $x = 1$을 대입하여 계산한 값은?',
                        'stem_en': 'What is the value of $7 \\times x - 11$ when $x = 1$?',
                        'options': ['$-5$', '$-4$', '$-3$', '$3$', '$4$'],
                        'answer': 2,
                        'exp': '$7 \\times 1 - 11 = 7 - 11 = -4$입니다.',
                        'exp_en': '$7(1) - 11 = -4$.',
                    }
                ],
            },
            {
                'title': '🌿 2단계 · [기호 번역] 접선 $y = 7x - 11$에서 두 가지 핵심 단서 뽑아내기',
                'title_en': '🌿 Step 2 · [Symbol Translation] Extracting Two Conditions from Tangent Line $y = 7x - 11$',
                'knowledge': '곡선 $y = g(x)$ 위의 점 $(1, f(1))$에서의 접선이 $y = 7x - 11$이라는 문장 속에는 ① 함숫값 단서 $f(1) = -4$와 ② 접선의 기울기 단서 $g\'(1) = 7$ 두 가지가 숨어 있습니다!',
                'knowledge_en': 'A tangent line $y = 7x - 11$ at $(1, f(1))$ encodes two facts: the point value $f(1) = -4$ and the slope $g\'(1) = 7$.',
                'questions': [
                    {
                        'level_label': '기호 번역 디딤돌 2',
                        'level_label_en': 'Symbol Translation Step 2',
                        'stem': '$g(x) = x^2 f(x)$라 할 때, 점 $(1, f(1))$에서의 접선이 $y = 7x - 11$이라는 조건에서 얻는 $f(1)$과 $g\'(1)$의 값은?',
                        'stem_en': 'Letting $g(x) = x^2 f(x)$, what are $f(1)$ and $g\'(1)$ from the tangent line $y = 7x - 11$ at $x = 1$?',
                        'options': [
                            '$f(1) = 7,\\; g\'(1) = -11$',
                            '$f(1) = -4,\\; g\'(1) = 7$',
                            '$f(1) = 4,\\; g\'(1) = 7$',
                            '$f(1) = -11,\\; g\'(1) = 7$',
                            '$f(1) = -4,\\; g\'(1) = -11$',
                        ],
                        'answer': 2,
                        'exp': '접점 $(1, f(1))$이 직선 $y = 7x - 11$ 위에 있으므로 $f(1) = 7(1) - 11 = -4$이고, 접선의 기울기는 $g\'(1) = 7$입니다.',
                        'exp_en': 'Substituting $x = 1$ gives $f(1) = -4$, and the slope of $y = 7x - 11$ gives $g\'(1) = 7$.',
                    }
                ],
            },
            {
                'title': '🌱 3단계 · [핵심 관계식 (가)] $g(x) = x^2 f(x)$에 곱의 미분법 적용하기',
                'title_en': '🌱 Step 3 · [Core Relation A] Differentiating $g(x) = x^2 f(x)$ via Product Rule',
                'knowledge': '곱의 미분법 $(uv)\' = u\'v + uv\'$에 따라 앞의 $x^2$을 미분해 $2x f(x)$를 만들고, 뒤의 $f(x)$를 미분해 $x^2 f\'(x)$를 만들어 더합니다.',
                'knowledge_en': 'Apply $(uv)\' = u\'v + uv\'$ with $u = x^2$ ($u\' = 2x$) and $v = f(x)$ ($v\' = f\'(x)$).',
                'questions': [
                    {
                        'level_label': '핵심 관계식 (가) 디딤돌 3',
                        'level_label_en': 'Core Relation A Step 3',
                        'stem': '함수 $g(x) = x^2 f(x)$를 $x$에 대하여 미분한 도함수 $g\'(x)$는?',
                        'stem_en': 'What is the derivative $g\'(x)$ of $g(x) = x^2 f(x)$?',
                        'options': [
                            "$2x f'(x)$",
                            "$x^2 f'(x)$",
                            "$2x f(x) + x^2 f'(x)$",
                            "$2x f(x) - x^2 f'(x)$",
                            "$f(x) + 2x f'(x)$",
                        ],
                        'answer': 3,
                        'exp': '곱의 미분법에 의해 $g\'(x) = (x^2)\' f(x) + x^2 f\'(x) = 2x f(x) + x^2 f\'(x)$입니다.',
                        'exp_en': 'By the product rule, $g\'(x) = 2x f(x) + x^2 f\'(x)$.',
                    }
                ],
            },
            {
                'title': '🌳 4단계 · [중간 전개 (나)] $g\'(1) = 7$을 $f(1)$과 $f\'(1)$의 관계식으로 나타내기',
                'title_en': '🌳 Step 4 · [Intermediate Step B] Setting Up $g\'(1) = 7$ at $x = 1$',
                'knowledge': '3단계에서 구한 $g\'(x) = 2x f(x) + x^2 f\'(x)$에 $x = 1$을 대입하고 $g\'(1) = 7$과 같다고 놓습니다.',
                'knowledge_en': 'Evaluate $g\'(x) = 2x f(x) + x^2 f\'(x)$ at $x = 1$ and equate it to $7$.',
                'questions': [
                    {
                        'level_label': '중간 전개 (나) 디딤돌 4',
                        'level_label_en': 'Intermediate Step B Step 4',
                        'stem': '$g\'(x) = 2x f(x) + x^2 f\'(x)$에서 $g\'(1) = 7$을 정리한 관계식은?',
                        'stem_en': 'Which equation follows from $g\'(1) = 7$ when $g\'(x) = 2x f(x) + x^2 f\'(x)$?',
                        'options': [
                            "$f(1) + f'(1) = 7$",
                            "$2f(1) + f'(1) = 7$",
                            "$f(1) + 2f'(1) = 7$",
                            "$2f(1) - f'(1) = 7$",
                            "$2f'(1) = 7$",
                        ],
                        'answer': 2,
                        'exp': '$x = 1$을 대입하면 $g\'(1) = 2(1)f(1) + (1)^2 f\'(1) = 2f(1) + f\'(1) = 7$입니다.',
                        'exp_en': 'Substituting $x = 1$ gives $2f(1) + f\'(1) = 7$.',
                    }
                ],
            },
            {
                'title': '💎 5단계 · [최종 레고 조립] $f(1) = -4$를 대입해 $f\'(1)$ 확정하기',
                'title_en': '💎 Step 5 · [Final LEGO Assembly] Solving $2f(1) + f\'(1) = 7$ for $f\'(1)$',
                'knowledge': '$2f(1) + f\'(1) = 7$에 $f(1) = -4$를 대입하면 $-8 + f\'(1) = 7$이 되어 $f\'(1)$을 바로 얻을 수 있습니다.',
                'knowledge_en': 'Substitute $f(1) = -4$ into $2f(1) + f\'(1) = 7$ to solve for $f\'(1)$.',
                'questions': [
                    {
                        'level_label': '최종 레고 조립 디딤돌 5',
                        'level_label_en': 'Final LEGO Assembly Step 5',
                        'stem': '$f(1) = -4$이고 $2f(1) + f\'(1) = 7$일 때, $f\'(1)$의 값은?',
                        'stem_en': 'Given $f(1) = -4$ and $2f(1) + f\'(1) = 7$, what is $f\'(1)$?',
                        'options': ['$11$', '$12$', '$13$', '$14$', '$15$'],
                        'answer': 5,
                        'exp': '$2(-4) + f\'(1) = 7 \\implies -8 + f\'(1) = 7 \\implies f\'(1) = 15$입니다.',
                        'exp_en': '$-8 + f\'(1) = 7 \\implies f\'(1) = 15$.',
                    }
                ],
            },
        ],
        'final': {
            'stem': '다항함수 $f(x)$에 대하여 곡선 $y=x^2 f(x)$ 위의 점 $(1, f(1))$에서의 접선의 방정식이 $y=7x-11$일 때, $f\'(1)$의 값은? [4점]',
            'stem_en': 'For a polynomial function $f(x)$, when the tangent line to the curve $y=x^2 f(x)$ at the point $(1, f(1))$ is $y=7x-11$, what is the value of $f\'(1)$? [4 points]',
            'options': ['$11$', '$12$', '$13$', '$14$', '$15$'],
            'answer': 5,
            'exp': '점 $(1, f(1))$이 직선 $y=7x-11$ 위의 점이므로 $f(1)=-4$입니다. $g(x)=x^2 f(x)$라 하면 $g\'(x)=2xf(x)+x^2f\'(x)$이고 $g\'(1)=2f(1)+f\'(1)=7$이므로 $-8+f\'(1)=7 \\implies f\'(1)=15$입니다. 정답은 ⑤입니다.',
            'exp_en': 'Since $(1, f(1))$ lies on $y=7x-11$, $f(1)=-4$. Letting $g(x)=x^2 f(x)$, we have $g\'(x)=2xf(x)+x^2f\'(x)$, so $g\'(1)=2f(1)+f\'(1)=7 \\implies -8+f\'(1)=7 \\implies f\'(1)=15$. The correct answer is ⑤.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 두 함수의 곱으로 정의된 곡선 $y = x^2 f(x)$의 접선 정보로부터 <b>함숫값 일치 조건과 미분계수(접선의 기울기) 조건</b> 두 가지를 추출하고 곱의 미분법을 적용할 수 있는지를 평가합니다.</p>\n\n'
                '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: 접점 좌표 조건으로부터 $f(1)$ 구하기</b><br>\n'
                '  접점 $(1, f(1))$은 접선 $y = 7x - 11$ 위의 점이므로 $x = 1$을 대입하면:<br>\n'
                '  $$f(1) = 7 \\times 1 - 11 = -4$$<br>\n'
                '  <b>2단계: 곱의 미분법과 접선의 기울기 조건 적용</b><br>\n'
                '  $g(x) = x^2 f(x)$라 놓으면 곱의 미분법에 의하여:<br>\n'
                '  $$g\'(x) = 2x f(x) + x^2 f\'(x)$$<br>\n'
                '  점 $(1, f(1))$에서의 접선의 기울기가 $7$이므로 $g\'(1) = 7$입니다:<br>\n'
                '  $$g\'(1) = 2f(1) + f\'(1) = 7$$<br>\n'
                '  <b>3단계: $f\'(1)$ 도출</b><br>\n'
                '  $f(1) = -4$를 대입하면:<br>\n'
                '  $$2(-4) + f\'(1) = 7 \\implies -8 + f\'(1) = 7 \\implies f\'(1) = 15$$\n'
                '</p>\n\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>\n'
                '  따라서 $f\'(1)$의 값은 $15$이며, 정답은 <b>⑤번</b>입니다.<br>\n'
                '  💡 <b>실전 팁</b>: 곡선이 $y = f(x)$가 아니라 $y = x^2 f(x)$로 변형되어 있을 때는 반드시 치환 함수 $g(x) = x^2 f(x)$를 한 줄 적어 $f\'(1) = 7$이라고 성급히 놓는 실수를 차단하세요.\n'
                '</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                '<p>This problem tests extracting <b>both function value and derivative information from a tangent line equation</b> and applying the <b>product rule</b> to $g(x) = x^2 f(x)$.</p>\n\n'
                '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Find $f(1)$ using the point of tangency</b><br>\n'
                '  Since $(1, f(1))$ lies on the tangent line $y = 7x - 11$:<br>\n'
                '  $$f(1) = 7(1) - 11 = -4$$<br>\n'
                '  <b>Step 2: Apply the product rule to $g(x) = x^2 f(x)$</b><br>\n'
                '  $$g\'(x) = 2x f(x) + x^2 f\'(x)$$<br>\n'
                '  Matching the slope $7$ of the tangent line at $x = 1$ gives:<br>\n'
                '  $$g\'(1) = 2f(1) + f\'(1) = 7$$<br>\n'
                '  <b>Step 3: Solve for $f\'(1)$</b><br>\n'
                '  $$2(-4) + f\'(1) = 7 \\implies -8 + f\'(1) = 7 \\implies f\'(1) = 15$$\n'
                '</p>\n\n'
                '<h4>✨ [Conclusion & Key Takeaway]</h4>\n'
                '<p>\n'
                '  The value of $f\'(1)$ is $15$, which corresponds to <b>Option ⑤</b>.\n'
                '</p>'
            ),
        },
    },
]
