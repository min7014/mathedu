# -*- coding: utf-8 -*-
# Auto-upgraded with Elementary-to-Advanced Micro-Scaffolding

PART3_PROBLEMS = [{'slug': 'c2610p23',
  'qNum': '확통 23',
  'subject': '확률과 통계',
  'title': '[2026학년도 10월 고3 확통 23번] 이항정리와 거듭제곱 전개식의 일반항 계수',
  'title_en': '[2026 AY Oct Exam Grade 12 Prob&Stats #23] Binomial Theorem and Coefficient in an Expansion',
  'summary_ko': '$\\left(2x^2 + \\dfrac{1}{2x}\\right)^6$의 전개식에서 $2x^2$을 $4$번, $\\dfrac{1}{2x}$을 $2$번 뽑아 $x^6$의 계수 '
                '$60$ 구하기',
  'summary_en': 'Select $2x^2$ four times and $\\dfrac{1}{2x}$ twice in the expansion of $\\left(2x^2 + '
                '\\dfrac{1}{2x}\\right)^6$ to find the coefficient $60$ of $x^6$.',
  'tags': ['확률과 통계', '경우의수', '이항정리', '전개식의계수', '23번'],
  'symbols': [{'sym': '${}_{6}\\mathrm{C}_{r} (2x^2)^{6-r} \\left(\\dfrac{1}{2x}\\right)^r$',
               'desc': '$6$개의 괄호 중 $\\dfrac{1}{2x}$을 $r$개 골라 곱한 이항정리 일반항',
               'desc_en': 'General term of the binomial expansion choosing $\\dfrac{1}{2x}$ $r$ times.'},
              {'sym': '$x^{12 - 3r} = x^6$',
               'desc': '$x$의 지수가 $6$이 되도록 하는 $r=2$ 결정',
               'desc_en': 'Equating the exponent of $x$ to $6$ gives $r=2$.'}],
  'levels': [{'title': '🔰 1단계 · [초등 구구단과 방정식] $12 - 3r = 6$을 만족하는 횟수 $r$ 찾기',
              'title_en': '🔰 Step 1 · [Elementary Multiplication & Subtraction] Solving $12 - 3r = 6$ for $r$',
              'knowledge': '$6$개의 주머니에서 $x^2$을 $(6-r)$번 뽑고 $\\frac{1}{x} = x^{-1}$을 $r$번 뽑으면 $x$의 지수는 $2(6-r) - r = 12 '
                           '- 3r$이 됩니다. 초등학교 사칙연산으로 $12 - 3r = 6$이 되는 $r$을 찾아봅시다.',
              'knowledge_en': 'Using elementary arithmetic, choosing $x^2$ $(6-r)$ times and $x^{-1}$ $r$ times gives '
                              'exponent $2(6-r) - r = 12 - 3r$. Set this equal to $6$.',
              'questions': [{'level_label': '초등 사칙연산 디딤돌 1',
                             'level_label_en': 'Elementary Arithmetic Step 1',
                             'stem': '초등학교 구구단과 뺄셈으로 $12 - 3r = 6$을 만족시키는 자연수 $r$의 값을 구하면?',
                             'stem_en': 'Using elementary arithmetic, what natural number $r$ satisfies $12 - 3r = 6$?',
                             'options': ['$1$', '$2$', '$3$', '$4$', '$5$'],
                             'answer': 2,
                             'exp': '$3r = 12 - 6 = 6$이므로 $r = 2$입니다.',
                             'exp_en': '$3r = 6 \\implies r = 2$.'}]},
             {'title': '🌿 2단계 · [조합 계산] $6$개 중 $2$개를 고르는 경우의 수 ${}_{6}\\mathrm{C}_{2}$ 구하기',
              'title_en': '🌿 Step 2 · [Combination] Computing ${}_{6}\\mathrm{C}_{2}$',
              'knowledge': '${}_{6}\\mathrm{C}_{2} = \\frac{6 \\times 5}{2 \\times 1} = 15$입니다.',
              'knowledge_en': '${}_{6}\\mathrm{C}_{2} = \\frac{6 \\times 5}{2 \\times 1} = 15$.',
              'questions': [{'level_label': '조합 계산 디딤돌 2',
                             'level_label_en': 'Combination Step 2',
                             'stem': '${}_{6}\\mathrm{C}_{2} = \\frac{6 \\times 5}{2 \\times 1}$의 값은?',
                             'stem_en': 'What is the value of ${}_{6}\\mathrm{C}_{2} = \\frac{6 \\times 5}{2 \\times '
                                        '1}$?',
                             'options': ['$10$', '$12$', '$15$', '$20$', '$30$'],
                             'answer': 3,
                             'exp': '$\\frac{30}{2} = 15$입니다.',
                             'exp_en': '$\\frac{30}{2} = 15$.'}]},
             {'title': '🌱 3단계 · [거듭제곱 계산] $2^4 \\times \\left(\\dfrac{1}{2}\\right)^2$ 구하기',
              'title_en': '🌱 Step 3 · [Powers] Computing $2^4 \\times \\left(\\dfrac{1}{2}\\right)^2$',
              'knowledge': '$r = 2$일 때 숫자 계수 부분은 $2^{6-2} \\times \\left(\\frac{1}{2}\\right)^2 = 2^4 \\times '
                           '\\frac{1}{4} = \\frac{16}{4} = 4$입니다.',
              'knowledge_en': 'At $r = 2$, the numerical factor is $2^4 \\times \\left(\\frac{1}{2}\\right)^2 = 16 '
                              '\\times \\frac{1}{4} = 4$.',
              'questions': [{'level_label': '거듭제곱 약분 디딤돌 3',
                             'level_label_en': 'Power Simplification Step 3',
                             'stem': '$2^4 \\times \\left(\\frac{1}{2}\\right)^2 = 16 \\times \\frac{1}{4}$을 계산한 값은?',
                             'stem_en': 'What is $2^4 \\times \\left(\\frac{1}{2}\\right)^2 = 16 \\times '
                                        '\\frac{1}{4}$?',
                             'options': ['$1$', '$2$', '$4$', '$8$', '$16$'],
                             'answer': 3,
                             'exp': '$16 \\div 4 = 4$입니다.',
                             'exp_en': '$16 \\div 4 = 4$.'}]},
             {'title': '🌳 4단계 · [계수 결합 식] ${}_{6}\\mathrm{C}_{2}$와 숫자 거듭제곱 곱하기',
              'title_en': '🌳 Step 4 · [Combining Factors] Multiplying ${}_{6}\\mathrm{C}_{2}$ by $4$',
              'knowledge': '$x^6$의 계수는 ${}_{6}\\mathrm{C}_{2} \\times 4 = 15 \\times 4$입니다.',
              'knowledge_en': 'The coefficient of $x^6$ is ${}_{6}\\mathrm{C}_{2} \\times 4 = 15 \\times 4$.',
              'questions': [{'level_label': '계수 곱셈식 디딤돌 4',
                             'level_label_en': 'Coefficient Product Step 4',
                             'stem': '$15 \\times 4$를 $(10 + 5) \\times 4 = 40 + k$로 계산할 때 $k$의 값은?',
                             'stem_en': 'When computing $15 \\times 4 = (10 + 5) \\times 4 = 40 + k$, what is $k$?',
                             'options': ['$10$', '$15$', '$20$', '$25$', '$30$'],
                             'answer': 3,
                             'exp': '$5 \\times 4 = 20$이므로 $k = 20$입니다.',
                             'exp_en': '$5 \\times 4 = 20$.'}]},
             {'title': '💎 5단계 · [최종 종합] $x^6$의 계수 구하기',
              'title_en': '💎 Step 5 · [Final Synthesis] Final coefficient of $x^6$',
              'knowledge': '$15 \\times 4 = 60$으로 최종 계수를 구합니다.',
              'knowledge_en': '$15 \\times 4 = 60$.',
              'questions': [{'level_label': '최종 종합 디딤돌 5',
                             'level_label_en': 'Final Synthesis Step 5',
                             'stem': '$\\left(2x^2 + \\frac{1}{2x}\\right)^6$의 전개식에서 $x^6$의 계수는?',
                             'stem_en': 'What is the coefficient of $x^6$ in the expansion of $\\left(2x^2 + '
                                        '\\frac{1}{2x}\\right)^6$?',
                             'options': ['$30$', '$45$', '$60$', '$75$', '$90$'],
                             'answer': 3,
                             'exp': '${}_{6}\\mathrm{C}_{2} \\times 2^4 \\times \\left(\\frac{1}{2}\\right)^2 = 15 '
                                    '\\times 4 = 60$이므로 정답은 ③입니다.',
                             'exp_en': '${}_{6}\\mathrm{C}_{2} \\times 2^4 \\times \\left(\\frac{1}{2}\\right)^2 = 15 '
                                       '\\times 4 = 60$ (choice ③).'}]}],
  'final': {'stem': '$\\left(2x^2 + \\dfrac{1}{2x}\\right)^6$의 전개식에서 $x^6$의 계수는? [2점]',
            'stem_en': 'What is the coefficient of $x^6$ in the expansion of $\\left(2x^2 + \\dfrac{1}{2x}\\right)^6$? '
                       '[2 points]',
            'options': ['$30$', '$45$', '$60$', '$75$', '$90$'],
            'answer': 3,
            'exp': '일반항 ${}_{6}\\mathrm{C}_{r}(2x^2)^{6-r}\\left(\\dfrac{1}{2x}\\right)^r = '
                   '{}_{6}\\mathrm{C}_{r}2^{6-2r}x^{12-3r}$에서 $12-3r=6 \\implies r=2$이므로 계수는 '
                   '${}_{6}\\mathrm{C}_{2}\\times 2^2 = 15\\times 4 = 60$입니다.',
            'exp_en': 'Setting $12 - 3r = 6$ in the general term ${}_{6}\\mathrm{C}_{r}2^{6-2r}x^{12-3r}$ gives $r = '
                      '2$, so the coefficient is ${}_{6}\\mathrm{C}_{2} \\times 2^2 = 60$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>이항정리의 일반항 공식</b>을 이용하여 특정 차수($x^6$)의 계수를 구하는 기본 문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 이항정리의 일반항 구하기</b><br>\n'
                        '  $$\\left(2x^2 + \\frac{1}{2x}\\right)^6\\text{의 일반항은 } {}_{6}\\mathrm{C}_{r} (2x^2)^{6-r} '
                        '\\left(\\frac{1}{2x}\\right)^r = {}_{6}\\mathrm{C}_{r} 2^{6-2r} x^{12-3r}$$<br>\n'
                        '  <b>2단계: $x^6$이 되는 $r$의 값과 계수 계산</b><br>\n'
                        '  $12 - 3r = 6$에서 $r = 2$입니다. 이를 계수에 대입하면:<br>\n'
                        '  $${}_{6}\\mathrm{C}_{2} \\times 2^{6-4} = 15 \\times 4 = 60$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 $x^6$의 계수는 $60$이므로 정답은 <b>③번</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem applies the <b>Binomial Theorem</b> to find the coefficient of $x^6$.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: General term</b><br>\n'
                           '  $${}_{6}\\mathrm{C}_{r} (2x^2)^{6-r} \\left(\\frac{1}{2x}\\right)^r = '
                           '{}_{6}\\mathrm{C}_{r} 2^{6-2r} x^{12-3r}$$<br>\n'
                           '  <b>Step 2: Solve for $r$ and evaluate</b><br>\n'
                           '  Setting $12 - 3r = 6 \\implies r = 2$ gives ${}_{6}\\mathrm{C}_{2} \\times 2^2 = 15 '
                           '\\times 4 = 60$.\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  The correct answer is <b>choice ③ ($60$)</b>.\n'
                           '</p>'}},
 {'slug': 'c2610p24',
  'qNum': '확통 24',
  'subject': '확률과 통계',
  'title': '[2026학년도 10월 고3 확통 24번] 이항분포의 평균과 분산으로 시행 횟수 n 구하기',
  'title_en': '[2026 AY Oct Exam Grade 12 Prob&Stats #24] Finding n from Mean and Variance of a Binomial Distribution',
  'summary_ko': '$\\mathrm{E}(X)=np=5,\\ \\mathrm{V}(X)=np(1-p)=4$에서 $1-p=\\dfrac{4}{5},\\ p=\\dfrac{1}{5}$를 구하고 '
                '$n=25$ 도출하기',
  'summary_en': 'Divide $\\mathrm{V}(X)=np(1-p)=4$ by $\\mathrm{E}(X)=np=5$ to get $1-p=\\dfrac{4}{5}$, '
                '$p=\\dfrac{1}{5}$, and $n=25$.',
  'tags': ['확률과 통계', '통계', '이항분포', '평균과분산', '표준편차', '24번'],
  'symbols': [{'sym': '$\\mathrm{E}(X) = np = 5$',
               'desc': '이항분포 $\\mathrm{B}(n, p)$의 평균',
               'desc_en': 'Mean of binomial distribution $\\mathrm{B}(n, p)$.'},
              {'sym': '$\\mathrm{V}(X) = \\sigma(X)^2 = np(1-p) = 4$',
               'desc': '표준편차 2를 제곱한 분산',
               'desc_en': 'Variance equals the square of the standard deviation 2.'}],
  'levels': [{'title': '🔰 1단계 · [초등 구구단 제곱] 표준편차가 $2$일 때 분산 $\\mathrm{V}(X)$ 구하기',
              'title_en': '🔰 Step 1 · [Elementary Multiplication] Finding variance $\\mathrm{V}(X)$ from $\\sigma(X) = '
                          '2$',
              'knowledge': '통계에서 분산 $\\mathrm{V}(X)$는 표준편차 $\\sigma(X)$를 두 번 곱한(제곱한) 값입니다. 초등학교 구구단 $2 \\times 2 = 4$로 '
                           '분산을 바로 구할 수 있습니다.',
              'knowledge_en': 'By elementary multiplication, variance $\\mathrm{V}(X)$ is the square of the standard '
                              'deviation: $2 \\times 2 = 4$.',
              'questions': [{'level_label': '초등 구구단 디딤돌 1',
                             'level_label_en': 'Elementary Multiplication Step 1',
                             'stem': '초등학교 구구단처럼 표준편차 $\\sigma(X) = 2$를 제곱한 분산 $\\mathrm{V}(X) = \\{\\sigma(X)\\}^2$의 '
                                     '값은?',
                             'stem_en': 'Using elementary multiplication, if $\\sigma(X) = 2$, what is the variance '
                                        '$\\mathrm{V}(X) = \\{\\sigma(X)\\}^2$?',
                             'options': ['$2$', '$4$', '$6$', '$8$', '$10$'],
                             'answer': 2,
                             'exp': '$\\mathrm{V}(X) = 2^2 = 4$입니다.',
                             'exp_en': '$\\mathrm{V}(X) = 2^2 = 4$.'}]},
             {'title': '🌿 2단계 · [비율 계산] $np = 5$와 $np(1-p) = 4$에서 $1 - p$ 구하기',
              'title_en': '🌿 Step 2 · [Ratio] Finding $1 - p$ from $np = 5$ and $np(1-p) = 4$',
              'knowledge': '$np(1-p) = 4$에서 앞의 $np$ 자리에 $5$를 넣으면 $5(1-p) = 4$가 됩니다.',
              'knowledge_en': 'Substituting $np = 5$ into $np(1-p) = 4$ gives $5(1-p) = 4$.',
              'questions': [{'level_label': '비율 나눗셈 디딤돌 2',
                             'level_label_en': 'Ratio Division Step 2',
                             'stem': '$5(1 - p) = 4$일 때, $1 - p$의 값은?',
                             'stem_en': 'Given $5(1 - p) = 4$, what is $1 - p$?',
                             'options': ['$\\frac{1}{5}$',
                                         '$\\frac{2}{5}$',
                                         '$\\frac{3}{5}$',
                                         '$\\frac{4}{5}$',
                                         '$\\frac{5}{4}$'],
                             'answer': 4,
                             'exp': '양변을 $5$로 나누면 $1 - p = \\frac{4}{5}$입니다.',
                             'exp_en': '$1 - p = \\frac{4}{5}$.'}]},
             {'title': '🌱 3단계 · [분수 뺄셈] 성공 확률 $p$ 구하기',
              'title_en': '🌱 Step 3 · [Fraction Subtraction] Finding probability $p$',
              'knowledge': '$1 - p = \\frac{4}{5}$이므로 $p = 1 - \\frac{4}{5} = \\frac{1}{5}$입니다.',
              'knowledge_en': 'From $1 - p = \\frac{4}{5}$, we have $p = 1 - \\frac{4}{5} = \\frac{1}{5}$.',
              'questions': [{'level_label': '확률 p 디딤돌 3',
                             'level_label_en': 'Probability p Step 3',
                             'stem': '$1 - p = \\frac{4}{5}$일 때, 확률 $p$의 값은?',
                             'stem_en': 'Given $1 - p = \\frac{4}{5}$, what is $p$?',
                             'options': ['$\\frac{1}{5}$',
                                         '$\\frac{1}{4}$',
                                         '$\\frac{2}{5}$',
                                         '$\\frac{3}{5}$',
                                         '$\\frac{4}{5}$'],
                             'answer': 1,
                             'exp': '$p = 1 - \\frac{4}{5} = \\frac{1}{5}$입니다.',
                             'exp_en': '$p = \\frac{1}{5}$.'}]},
             {'title': '🌳 4단계 · [평균 공식 대입] $n \\times \\dfrac{1}{5} = 5$ 세우기',
              'title_en': '🌳 Step 4 · [Mean Equation] Setting up $n \\times \\dfrac{1}{5} = 5$',
              'knowledge': '$\\mathrm{E}(X) = np = 5$에 $p = \\frac{1}{5}$을 대입하면 $\\frac{n}{5} = 5$가 됩니다.',
              'knowledge_en': 'Substituting $p = \\frac{1}{5}$ into $np = 5$ gives $\\frac{n}{5} = 5$.',
              'questions': [{'level_label': '시행 횟수 식 디딤돌 4',
                             'level_label_en': 'Trials Equation Step 4',
                             'stem': '$n$을 $5$로 나눈 값이 $5$일 때, $n$을 구하기 위해 해야 할 계산은?',
                             'stem_en': 'When $\\frac{n}{5} = 5$, how do we compute $n$?',
                             'options': ['$5 + 5$', '$5 - 5$', '$5 \\times 5$', '$5 \\div 5$', '$5 \\times 4$'],
                             'answer': 3,
                             'exp': '양변에 $5$를 곱하여 $n = 5 \\times 5$를 계산합니다.',
                             'exp_en': 'Multiply both sides by $5$: $n = 5 \\times 5$.'}]},
             {'title': '💎 5단계 · [최종 종합] 자연수 $n$의 값 구하기',
              'title_en': '💎 Step 5 · [Final Synthesis] Finding $n$',
              'knowledge': '$n = 5 \\times 5 = 25$로 정답을 확정합니다.',
              'knowledge_en': '$n = 5 \\times 5 = 25$.',
              'questions': [{'level_label': '최종 종합 디딤돌 5',
                             'level_label_en': 'Final Synthesis Step 5',
                             'stem': '이항분포 $\\mathrm{B}(n, p)$에서 $\\mathrm{E}(X) = 5$, $\\sigma(X) = 2$일 때, $n$의 값은?',
                             'stem_en': 'For $X \\sim \\mathrm{B}(n, p)$ with $\\mathrm{E}(X) = 5$ and $\\sigma(X) = '
                                        '2$, what is $n$?',
                             'options': ['$25$', '$30$', '$35$', '$40$', '$45$'],
                             'answer': 1,
                             'exp': '$n = 5 \\times 5 = 25$이므로 정답은 ①입니다.',
                             'exp_en': '$n = 25$ (choice ①).'}]}],
  'final': {'stem': '이항분포 $\\mathrm{B}(n, p)$를 따르는 확률변수 $X$에 대하여 $\\mathrm{E}(X) = 5$, $\\sigma(X) = 2$일 때, $n$의 값은? '
                    '[3점]',
            'stem_en': 'For a random variable $X$ following the binomial distribution $\\mathrm{B}(n, p)$, if '
                       '$\\mathrm{E}(X) = 5$ and $\\sigma(X) = 2$, what is the value of $n$? [3 points]',
            'options': ['$25$', '$30$', '$35$', '$40$', '$45$'],
            'answer': 1,
            'exp': '$\\mathrm{E}(X) = np = 5$, $\\mathrm{V}(X) = np(1-p) = 4$에서 $1-p = \\dfrac{4}{5} \\implies p = '
                   '\\dfrac{1}{5}$이므로 $n = 25$입니다.',
            'exp_en': 'From $np = 5$ and $np(1-p) = 4$, we get $1-p = \\dfrac{4}{5} \\implies p = \\dfrac{1}{5}$, so '
                      '$n = 25$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>이항분포 $\\mathrm{B}(n, p)$의 평균 $\\mathrm{E}(X) = np$와 분산 $\\mathrm{V}(X) = np(1-p)$ '
                        '공식</b>을 연립하여 시행 횟수 $n$을 구하는 문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 평균과 분산의 식 세우기</b><br>\n'
                        '  $$\\mathrm{E}(X) = np = 5, \\quad \\mathrm{V}(X) = \\{\\sigma(X)\\}^2 = 2^2 = 4 \\implies '
                        'np(1-p) = 4$$<br>\n'
                        '  <b>2단계: $p$와 $n$ 구하기</b><br>\n'
                        '  $5(1-p) = 4$에서 $1-p = \\frac{4}{5} \\implies p = \\frac{1}{5}$입니다.<br>\n'
                        '  이를 $np = 5$에 대입하면 $\\frac{1}{5}n = 5 \\implies n = 25$입니다.\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 $n = 25$이므로 정답은 <b>①번</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem uses the formulas for the <b>mean and variance of a binomial distribution '
                           '$\\mathrm{B}(n, p)$</b>.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Relate mean and variance</b><br>\n'
                           '  $$\\mathrm{E}(X) = np = 5, \\quad \\mathrm{V}(X) = np(1-p) = 2^2 = 4$$<br>\n'
                           '  <b>Step 2: Solve for $p$ and $n$</b><br>\n'
                           '  $$1 - p = \\frac{4}{5} \\implies p = \\frac{1}{5} \\implies n = \\frac{5}{1/5} = 25$$\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  The correct answer is <b>choice ① ($25$)</b>.\n'
                           '</p>'}},
 {'slug': 'c2610p25',
  'qNum': '확통 25',
  'subject': '확률과 통계',
  'title': '[2026학년도 10월 고3 확통 25번] 거듭제곱 항이 포함된 음이 아닌 정수해의 개수 (중복조합)',
  'title_en': '[2026 AY Oct Exam Grade 12 Prob&Stats #25] Number of Non-Negative Integer Solutions via Combinations '
              'with Repetition',
  'summary_ko': '$d=0, 1, 2$일 때로 케이스를 나누어 $a+b+c=8-d^3$의 중복조합 개수를 더해 $82$ 구하기',
  'summary_en': 'Split into cases $d=0, 1, 2$ and sum the combinations with repetition for $a+b+c=8-d^3$ to get '
                '$45+36+1=82$.',
  'tags': ['확률과 통계', '경우의수', '중복조합', '음이아닌정수해', '케이스분류', '25번'],
  'symbols': [{'sym': '$a + b + c = 8 - d^3$',
               'desc': '세제곱 항 $d^3$을 우변으로 넘겨 $d$의 값에 따라 분류',
               'desc_en': 'Isolate $a+b+c$ by moving $d^3$ to the right-hand side.'},
              {'sym': '${}_{3}\\mathrm{H}_{k} = {}_{k+2}\\mathrm{C}_{2}$',
               'desc': '음이 아닌 세 정수의 합이 k가 되는 중복조합 공식',
               'desc_en': 'Number of non-negative integer triples summing to k.'}],
  'levels': [{'title': '🔰 1단계 · [초등 세제곱 계산] $d^3 \\le 8$이 되는 음이 아닌 정수 $d$ 찾기',
              'title_en': '🔰 Step 1 · [Elementary Cubing] Finding non-negative integers $d$ with $d^3 \\le 8$',
              'knowledge': '초등학교 곱셈으로 똑같은 수를 세 번 곱해 봅시다: $0 \\times 0 \\times 0 = 0$, $1 \\times 1 \\times 1 = 1$, $2 '
                           '\\times 2 \\times 2 = 8$, $3 \\times 3 \\times 3 = 27$. 합이 $8$이 되어야 하므로 $d^3$은 $8$을 넘을 수 '
                           '없습니다!',
              'knowledge_en': 'By elementary multiplication: $0^3 = 0$, $1^3 = 1$, $2^3 = 8$, and $3^3 = 27 > 8$. '
                              'Since $a, b, c \\ge 0$, $d^3$ cannot exceed $8$.',
              'questions': [{'level_label': '초등 곱셈 디딤돌 1',
                             'level_label_en': 'Elementary Multiplication Step 1',
                             'stem': '초등학교 곱셈 규칙에 따라 음이 아닌 정수 $d$에 대하여 $d^3 \\le 8$을 만족시키는 $d$의 값을 모두 고르면?',
                             'stem_en': 'Using elementary multiplication, which non-negative integers $d$ satisfy $d^3 '
                                        '\\le 8$?',
                             'options': ['$0,\\ 1$',
                                         '$1,\\ 2$',
                                         '$0,\\ 1,\\ 2$',
                                         '$0,\\ 1,\\ 2,\\ 3$',
                                         '$1,\\ 2,\\ 3$'],
                             'answer': 3,
                             'exp': '$0^3 = 0$, $1^3 = 1$, $2^3 = 8$이므로 가능한 $d$는 $0, 1, 2$의 $3$가지입니다.',
                             'exp_en': 'Since $0^3 = 0, 1^3 = 1, 2^3 = 8$, the valid values are $d \\in \\{0, 1, '
                                       '2\\}$.'}]},
             {'title': '🌿 2단계 · [경우 1: $d = 0$] $a + b + c = 8$의 해의 개수 구하기',
              'title_en': '🌿 Step 2 · [Case 1: $d = 0$] Solutions to $a + b + c = 8$',
              'knowledge': '$d = 0$이면 $a + b + c = 8$이므로 중복조합 ${}_{3}\\mathrm{H}_{8} = {}_{3+8-1}\\mathrm{C}_{8} = '
                           '{}_{10}\\mathrm{C}_{2} = \\frac{10 \\times 9}{2} = 45$가지입니다.',
              'knowledge_en': 'When $d = 0$, $a + b + c = 8$, which has ${}_{3}\\mathrm{H}_{8} = '
                              '{}_{10}\\mathrm{C}_{2} = 45$ solutions.',
              'questions': [{'level_label': '$d=0$ 중복조합 디딤돌 2',
                             'level_label_en': 'Case $d=0$ Step 2',
                             'stem': '$d = 0$일 때 $a + b + c = 8$을 만족시키는 음이 아닌 정수해의 개수 ${}_{3}\\mathrm{H}_{8} = '
                                     '{}_{10}\\mathrm{C}_{2}$는?',
                             'stem_en': 'When $d = 0$, how many non-negative integer solutions does $a + b + c = 8$ '
                                        'have (${}_{3}\\mathrm{H}_{8} = {}_{10}\\mathrm{C}_{2}$)?',
                             'options': ['$36$', '$40$', '$45$', '$50$', '$55$'],
                             'answer': 3,
                             'exp': '${}_{10}\\mathrm{C}_{2} = \\frac{10 \\times 9}{2 \\times 1} = 45$입니다.',
                             'exp_en': '${}_{10}\\mathrm{C}_{2} = 45$.'}]},
             {'title': '🌱 3단계 · [경우 2: $d = 1$] $a + b + c = 7$의 해의 개수 구하기',
              'title_en': '🌱 Step 3 · [Case 2: $d = 1$] Solutions to $a + b + c = 7$',
              'knowledge': '$d = 1$이면 $a + b + c = 8 - 1 = 7$이므로 ${}_{3}\\mathrm{H}_{7} = {}_{9}\\mathrm{C}_{2} = '
                           '\\frac{9 \\times 8}{2} = 36$가지입니다.',
              'knowledge_en': 'When $d = 1$, $a + b + c = 7$, which has ${}_{3}\\mathrm{H}_{7} = {}_{9}\\mathrm{C}_{2} '
                              '= 36$ solutions.',
              'questions': [{'level_label': '$d=1$ 중복조합 디딤돌 3',
                             'level_label_en': 'Case $d=1$ Step 3',
                             'stem': '$d = 1$일 때 $a + b + c = 7$을 만족시키는 음이 아닌 정수해의 개수 ${}_{3}\\mathrm{H}_{7} = '
                                     '{}_{9}\\mathrm{C}_{2}$는?',
                             'stem_en': 'When $d = 1$, what is ${}_{3}\\mathrm{H}_{7} = {}_{9}\\mathrm{C}_{2}$?',
                             'options': ['$28$', '$32$', '$36$', '$42$', '$45$'],
                             'answer': 3,
                             'exp': '${}_{9}\\mathrm{C}_{2} = \\frac{9 \\times 8}{2 \\times 1} = 36$입니다.',
                             'exp_en': '${}_{9}\\mathrm{C}_{2} = 36$.'}]},
             {'title': '🌳 4단계 · [경우 3: $d = 2$] $a + b + c = 0$의 해의 개수 구하기',
              'title_en': '🌳 Step 4 · [Case 3: $d = 2$] Solutions to $a + b + c = 0$',
              'knowledge': '$d = 2$이면 $d^3 = 8$이므로 $a + b + c = 8 - 8 = 0$입니다. 음이 아닌 세 정수의 합이 $0$이 되는 경우는 $(0, 0, 0)$ '
                           '딱 $1$가지뿐입니다.',
              'knowledge_en': 'When $d = 2$, $a + b + c = 0$, which has only $1$ solution: $(0, 0, 0)$.',
              'questions': [{'level_label': '$d=2$ 해의 개수 디딤돌 4',
                             'level_label_en': 'Case $d=2$ Step 4',
                             'stem': '$d = 2$일 때 $a + b + c = 0$을 만족시키는 음이 아닌 정수 $(a, b, c)$의 순서쌍의 개수는?',
                             'stem_en': 'When $d = 2$, how many non-negative integer triples $(a, b, c)$ satisfy $a + '
                                        'b + c = 0$?',
                             'options': ['$0$', '$1$', '$2$', '$3$', '$6$'],
                             'answer': 2,
                             'exp': '$a = b = c = 0$인 $1$가지입니다.',
                             'exp_en': 'Only $(0, 0, 0)$, so $1$ solution.'}]},
             {'title': '💎 5단계 · [최종 종합] 세 경우의 수를 모두 더하기',
              'title_en': '💎 Step 5 · [Final Synthesis] Summing all three cases',
              'knowledge': '$45 + 36 + 1$을 계산하면 전체 순서쌍의 개수가 완성됩니다.',
              'knowledge_en': 'Add $45 + 36 + 1 = 82$.',
              'questions': [{'level_label': '최종 종합 디딤돌 5',
                             'level_label_en': 'Final Synthesis Step 5',
                             'stem': '구한 세 경우의 수의 합 $45 + 36 + 1$은?',
                             'stem_en': 'What is the total number of solutions $45 + 36 + 1$?',
                             'options': ['$80$', '$82$', '$84$', '$86$', '$88$'],
                             'answer': 2,
                             'exp': '$45 + 36 + 1 = 82$이므로 정답은 ②입니다.',
                             'exp_en': '$45 + 36 + 1 = 82$ (choice ②).'}]}],
  'final': {'stem': '방정식 $a + b + c + d^3 = 8$을 만족시키는 음이 아닌 정수 $a, b, c, d$의 모든 순서쌍 $(a, b, c, d)$의 개수는? [3점]',
            'stem_en': 'How many ordered 4-tuples $(a, b, c, d)$ of non-negative integers satisfy $a + b + c + d^3 = '
                       '8$? [3 points]',
            'options': ['$80$', '$82$', '$84$', '$86$', '$88$'],
            'answer': 2,
            'exp': '$d = 0, 1, 2$일 때 $a+b+c = 8, 7, 0$이므로 순서쌍의 개수는 ${}_{3}\\mathrm{H}_{8} + {}_{3}\\mathrm{H}_{7} + '
                   '{}_{3}\\mathrm{H}_{0} = 45 + 36 + 1 = 82$입니다.',
            'exp_en': 'For $d = 0, 1, 2$, $a+b+c = 8, 7, 0$, giving ${}_{3}\\mathrm{H}_{8} + {}_{3}\\mathrm{H}_{7} + '
                      '{}_{3}\\mathrm{H}_{0} = 45 + 36 + 1 = 82$ solutions.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 계수나 차수가 다른 문자($d^3$)를 기준으로 케이스를 분류한 뒤 <b>중복조합(${}_{n}\\mathrm{H}_{r}$)</b>을 적용하는 '
                        '문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 음이 아닌 정수 $d$의 값 분류</b><br>\n'
                        '  $a + b + c = 8 - d^3 \\ge 0$이어야 하므로 $d^3 \\le 8$, 즉 $d \\in \\{0, 1, 2\\}$입니다.<br><br>\n'
                        '  <b>2단계: 각 경우의 중복조합 계산</b><br>\n'
                        '  - (i) $d = 0$일 때: $a + b + c = 8 \\implies {}_{3}\\mathrm{H}_{8} = {}_{10}\\mathrm{C}_{8} = '
                        '{}_{10}\\mathrm{C}_{2} = 45$<br>\n'
                        '  - (ii) $d = 1$일 때: $a + b + c = 7 \\implies {}_{3}\\mathrm{H}_{7} = {}_{9}\\mathrm{C}_{7} = '
                        '{}_{9}\\mathrm{C}_{2} = 36$<br>\n'
                        '  - (iii) $d = 2$일 때: $a + b + c = 0 \\implies {}_{3}\\mathrm{H}_{0} = 1$<br><br>\n'
                        '  <b>3단계: 합의 법칙 적용</b><br>\n'
                        '  $$45 + 36 + 1 = 82$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 모든 순서쌍의 개수는 $82$이므로 정답은 <b>②번</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem uses casework on the cubic term $d^3$ followed by <b>combinations with '
                           'repetition (${}_{n}\\mathrm{H}_{r}$)</b>.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Casework on $d \\in \\{0, 1, 2\\}$</b><br>\n'
                           '  - $d = 0$: $a + b + c = 8 \\implies {}_{3}\\mathrm{H}_{8} = {}_{10}\\mathrm{C}_{2} = '
                           '45$<br>\n'
                           '  - $d = 1$: $a + b + c = 7 \\implies {}_{3}\\mathrm{H}_{7} = {}_{9}\\mathrm{C}_{2} = '
                           '36$<br>\n'
                           '  - $d = 2$: $a + b + c = 0 \\implies {}_{3}\\mathrm{H}_{0} = 1$<br><br>\n'
                           '  <b>Step 2: Total count</b><br>\n'
                           '  $$45 + 36 + 1 = 82$$\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  The correct answer is <b>choice ② ($82$)</b>.\n'
                           '</p>'}},
 {'slug': 'c2610p26',
  'qNum': '확통 26',
  'subject': '확률과 통계',
  'title': '[2026학년도 10월 고3 확통 26번] 모평균의 신뢰구간 중심(표본평균)과 모표준편차 추론',
  'title_en': '[2026 AY Oct Exam Grade 12 Prob&Stats #26] Confidence Interval for Population Mean and Standard '
              'Deviation',
  'summary_ko': '신뢰구간의 중점(표본평균) 비교로 $a=3$을 구하고 반쪽 길이 $1.96 \\times \\dfrac{\\sigma}{14}=1$에서 $\\sigma=\\dfrac{50}{7}$을 '
                '구해 $a\\sigma$ 도출하기',
  'summary_en': 'Equate the midpoints (sample mean) to find $a=3$, and use the half-width $1.96 \\times '
                '\\dfrac{\\sigma}{14}=1$ to find $\\sigma=\\dfrac{50}{7}$ and $a\\sigma=\\dfrac{150}{7}$.',
  'tags': ['확률과 통계', '통계', '통계적추정', '모평균의신뢰구간', '표본평균', '26번'],
  'symbols': [{'sym': '$\\bar{x} = \\dfrac{\\text{양 끝점의 합}}{2}$',
               'desc': '모평균 신뢰구간의 한가운데 값은 항상 표본평균 $\\bar{x}$',
               'desc_en': 'The midpoint of a confidence interval is always the sample mean.'},
              {'sym': '$1.96 \\times \\dfrac{\\sigma}{\\sqrt{n}}$',
               'desc': '신뢰도 95% 신뢰구간의 중심에서 양 끝까지의 반쪽 길이(오차한계)',
               'desc_en': 'Margin of error (half-width) for a 95% confidence interval.'}],
  'levels': [{'title': '🔰 1단계 · [초등 평균 구하기] 신뢰구간 양 끝점의 한가운데 값 비교하기',
              'title_en': '🔰 Step 1 · [Elementary Average] Finding the midpoint of the confidence interval',
              'knowledge': '초등학교에서 두 수 $a + 82$와 $a + 84$의 한가운데(평균)는 $a + 83$입니다. 이 한가운데 값이 바로 표본평균 $\\bar{x} = 2a + '
                           '80$과 같아야 합니다!',
              'knowledge_en': 'By elementary averaging, the midpoint between $a + 82$ and $a + 84$ is $a + 83$, which '
                              'must equal the sample mean $\\bar{x} = 2a + 80$.',
              'questions': [{'level_label': '초등 평균 비교 디딤돌 1',
                             'level_label_en': 'Elementary Midpoint Step 1',
                             'stem': '초등학교 평균 계산처럼 구간 $[a + 82, a + 84]$의 한가운데 값 $a + 83$이 표본평균 $2a + 80$과 같을 때($a + '
                                     '83 = 2a + 80$), 상수 $a$의 값은?',
                             'stem_en': 'Using elementary arithmetic, if the midpoint $a + 83$ equals the sample mean '
                                        '$2a + 80$, what is $a$?',
                             'options': ['$1$', '$2$', '$3$', '$4$', '$5$'],
                             'answer': 3,
                             'exp': '$a + 83 = 2a + 80 \\implies a = 83 - 80 = 3$입니다.',
                             'exp_en': '$a = 83 - 80 = 3$.'}]},
             {'title': '🌿 2단계 · [오차한계 확인] 중심에서 오른쪽 끝까지의 반쪽 길이 구하기',
              'title_en': '🌿 Step 2 · [Margin of Error] Half-width of the confidence interval',
              'knowledge': '구간 $[a + 82, a + 84]$의 중심 $a + 83$에서 오른쪽 끝 $a + 84$까지의 거리는 $(a + 84) - (a + 83) = 1$입니다.',
              'knowledge_en': 'The half-width from the center $a + 83$ to the upper bound $a + 84$ is $1$.',
              'questions': [{'level_label': '반쪽 길이 디딤돌 2',
                             'level_label_en': 'Half-Width Step 2',
                             'stem': '표본의 크기 $n = 196$일 때 $\\sqrt{n} = \\sqrt{196} = 14$입니다. 신뢰도 $95\\%$($z = '
                                     '1.96$)에서의 반쪽 길이 $1.96 \\times \\frac{\\sigma}{14} = 1$에서 $\\frac{1.96}{14}$을 소수로 '
                                     '계산하면?',
                             'stem_en': 'With $\\sqrt{196} = 14$, what is $\\frac{1.96}{14}$ in decimal form?',
                             'options': ['$0.12$', '$0.14$', '$0.16$', '$0.18$', '$0.20$'],
                             'answer': 2,
                             'exp': '$1.96 \\div 14 = 0.14$입니다.',
                             'exp_en': '$1.96 \\div 14 = 0.14$.'}]},
             {'title': '🌱 3단계 · [분수 변환] $0.14 \\sigma = 1$에서 모표준편차 $\\sigma$ 구하기',
              'title_en': '🌱 Step 3 · [Fraction Conversion] Solving $0.14\\sigma = 1$ for $\\sigma$',
              'knowledge': '$0.14 = \\frac{14}{100} = \\frac{7}{50}$이므로 $\\frac{7}{50}\\sigma = 1 \\implies \\sigma = '
                           '\\frac{50}{7}$입니다.',
              'knowledge_en': 'Since $0.14 = \\frac{7}{50}$, $\\frac{7}{50}\\sigma = 1 \\implies \\sigma = '
                              '\\frac{50}{7}$.',
              'questions': [{'level_label': '표준편차 sigma 디딤돌 3',
                             'level_label_en': 'Finding sigma Step 3',
                             'stem': '$\\frac{7}{50}\\sigma = 1$일 때, 모표준편차 $\\sigma$의 값은?',
                             'stem_en': 'From $\\frac{7}{50}\\sigma = 1$, what is $\\sigma$?',
                             'options': ['$\\frac{30}{7}$',
                                         '$\\frac{40}{7}$',
                                         '$\\frac{50}{7}$',
                                         '$\\frac{60}{7}$',
                                         '$10$'],
                             'answer': 3,
                             'exp': '역수를 곱하면 $\\sigma = \\frac{50}{7}$입니다.',
                             'exp_en': '$\\sigma = \\frac{50}{7}$.'}]},
             {'title': '🌳 4단계 · [분자 곱셈] $a = 3$과 분자 $50$ 곱하기',
              'title_en': '🌳 Step 4 · [Numerator Product] Multiplying $a = 3$ and $50$',
              'knowledge': '$a\\sigma = 3 \\times \\frac{50}{7}$에서 분자는 $3 \\times 50 = 150$입니다.',
              'knowledge_en': 'In $a\\sigma = 3 \\times \\frac{50}{7}$, the numerator is $3 \\times 50 = 150$.',
              'questions': [{'level_label': '분자 계산 디딤돌 4',
                             'level_label_en': 'Numerator Step 4',
                             'stem': '$3 \\times 50$의 값은?',
                             'stem_en': 'What is $3 \\times 50$?',
                             'options': ['$100$', '$120$', '$150$', '$180$', '$200$'],
                             'answer': 3,
                             'exp': '$3 \\times 50 = 150$입니다.',
                             'exp_en': '$3 \\times 50 = 150$.'}]},
             {'title': '💎 5단계 · [최종 종합] $a\\sigma$의 값 구하기',
              'title_en': '💎 Step 5 · [Final Synthesis] Final value of $a\\sigma$',
              'knowledge': '$a\\sigma = \\frac{150}{7}$로 정답을 확정합니다.',
              'knowledge_en': '$a\\sigma = \\frac{150}{7}$.',
              'questions': [{'level_label': '최종 종합 디딤돌 5',
                             'level_label_en': 'Final Synthesis Step 5',
                             'stem': '$a = 3$, $\\sigma = \\frac{50}{7}$일 때, $a\\sigma$의 값은?',
                             'stem_en': 'Given $a = 3$ and $\\sigma = \\frac{50}{7}$, what is $a\\sigma$?',
                             'options': ['$\\frac{135}{7}$',
                                         '$\\frac{140}{7}$',
                                         '$\\frac{145}{7}$',
                                         '$\\frac{150}{7}$',
                                         '$\\frac{155}{7}$'],
                             'answer': 4,
                             'exp': '$a\\sigma = 3 \\times \\frac{50}{7} = \\frac{150}{7}$이므로 정답은 ④입니다.',
                             'exp_en': '$a\\sigma = \\frac{150}{7}$ (choice ④).'}]}],
  'final': {'stem': '모평균이 $m$, 모표준편차가 $\\sigma$인 정규분포를 따르는 모집단에서 크기가 $196$인 표본을 이미추출하여 구한 표본평균이 $2a + 80$일 때, 모평균 $m$에 '
                    '대한 신뢰도 $95\\%$의 신뢰구간이 $a + 82 \\le m \\le a + 84$이다. $a\\sigma$의 값은? (단, $Z$가 표준정규분포를 따르는 확률변수일 '
                    '때, $\\mathrm{P}(|Z| \\le 1.96) = 0.95$로 계산한다.) [3점]',
            'stem_en': 'A random sample of size $196$ from a normal population with mean $m$ and standard deviation '
                       '$\\sigma$ yields a sample mean of $2a + 80$ and a $95\\%$ confidence interval $a + 82 \\le m '
                       '\\le a + 84$. What is the value of $a\\sigma$? (Use $\\mathrm{P}(|Z| \\le 1.96) = 0.95$.) [3 '
                       'points]',
            'options': ['$\\dfrac{135}{7}$',
                        '$\\dfrac{140}{7}$',
                        '$\\dfrac{145}{7}$',
                        '$\\dfrac{150}{7}$',
                        '$\\dfrac{155}{7}$'],
            'answer': 4,
            'exp': '신뢰구간의 중점 $a + 83 = 2a + 80$에서 $a = 3$이고, $1.96 \\times \\dfrac{\\sigma}{14} = 1$에서 $\\sigma = '
                   '\\dfrac{50}{7}$이므로 $a\\sigma = \\dfrac{150}{7}$입니다.',
            'exp_en': 'Equating the midpoint $a + 83 = 2a + 80$ gives $a = 3$, and $1.96 \\times \\dfrac{\\sigma}{14} '
                      '= 1$ gives $\\sigma = \\dfrac{50}{7}$, so $a\\sigma = \\dfrac{150}{7}$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>모평균 $m$의 신뢰구간의 중점이 표본평균 $\\bar{x}$</b>이고, <b>구간의 반쪽 길이가 $1.96 '
                        '\\frac{\\sigma}{\\sqrt{n}}$</b>임을 이용하여 미지수를 구하는 문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 신뢰구간의 중점으로 $a$ 구하기</b><br>\n'
                        '  신뢰구간 $[a + 82, a + 84]$의 중점은 표본평균 $\\bar{x} = 2a + 80$과 같으므로:<br>\n'
                        '  $$\\frac{(a + 82) + (a + 84)}{2} = a + 83 = 2a + 80 \\implies a = 3$$<br>\n'
                        '  <b>2단계: 신뢰구간의 반쪽 길이로 $\\sigma$ 구하기</b><br>\n'
                        '  구간의 반쪽 길이는 $(a + 84) - (a + 83) = 1$이고 $\\sqrt{n} = \\sqrt{196} = 14$이므로:<br>\n'
                        '  $$1.96 \\times \\frac{\\sigma}{14} = 1 \\implies 0.14\\sigma = 1 \\implies \\sigma = '
                        '\\frac{100}{14} = \\frac{50}{7}$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 $a\\sigma = 3 \\times \\dfrac{50}{7} = \\dfrac{150}{7}$이므로 정답은 <b>④번</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem uses the <b>midpoint and margin of error of a $95\\%$ confidence '
                           'interval</b> for the population mean.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Midpoint equals sample mean</b><br>\n'
                           '  $$a + 83 = 2a + 80 \\implies a = 3$$<br>\n'
                           '  <b>Step 2: Half-width equals margin of error</b><br>\n'
                           '  $$1.96 \\times \\frac{\\sigma}{\\sqrt{196}} = 0.14\\sigma = 1 \\implies \\sigma = '
                           '\\frac{50}{7}$$\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  Thus $a\\sigma = \\dfrac{150}{7}$, which corresponds to <b>choice ④</b>.\n'
                           '</p>'}},
 {'slug': 'c2610p27',
  'qNum': '확통 27',
  'subject': '확률과 통계',
  'title': '[2026학년도 10월 고3 확통 27번] 두 눈의 수의 곱의 홀짝에 따른 독립시행의 확률',
  'title_en': '[2026 AY Oct Exam Grade 12 Prob&Stats #27] Independent Trials Based on Parity of Product of Two Dice',
  'summary_ko': '$1$회 시행에서 공을 $1$개 넣을 확률 $\\dfrac{1}{4}$, $2$개 넣을 확률 $\\dfrac{3}{4}$을 구하고 $4$회 시행 후 공이 $5$개 이하일 확률 '
                '$\\dfrac{13}{256}$ 도출하기',
  'summary_en': 'Find $\\mathrm{P}(1\\text{ ball})=\\dfrac{1}{4}$ and $\\mathrm{P}(2\\text{ balls})=\\dfrac{3}{4}$ per '
                'trial, then compute the probability of at most $5$ balls in $4$ trials as $\\dfrac{13}{256}$.',
  'tags': ['확률과 통계', '확률', '독립시행의확률', '주사위의곱', '여사건', '27번'],
  'symbols': [{'sym': '$\\text{홀수} \\times \\text{홀수} = \\text{홀수}$',
               'desc': '두 눈의 곱이 홀수가 되어 공을 $1$개 넣을 확률 $\\dfrac{1}{2} \\times \\dfrac{1}{2} = \\dfrac{1}{4}$',
               'desc_en': 'Product is odd ($1$ ball added) iff both dice are odd: probability $\\dfrac{1}{4}$.'},
              {'sym': '$4\\text{번 모두 } 1\\text{개 또는 } 3\\text{번 } 1\\text{개} + 1\\text{번 } 2\\text{개}$',
               'desc': '4번 시행 후 공의 총합이 4개 또는 5개(5개 이하)가 되는 조건',
               'desc_en': 'Total balls $\\le 5$ in $4$ trials means either four $1$s (sum $4$) or three $1$s and one '
                          '$2$ (sum $5$).'}],
  'levels': [{'title': '🔰 1단계 · [초등 홀짝 곱셈] 두 수의 곱이 홀수가 될 조건과 확률 구하기',
              'title_en': '🔰 Step 1 · [Elementary Odd/Even Multiplication] Probability that the product of two dice is '
                          'odd',
              'knowledge': '초등학교 홀짝 곱셈에서 두 수를 곱해 홀수가 되려면 두 수 모두 홀수여야 합니다! 주사위 한 개에서 홀수($1, 3, 5$)가 나올 확률은 '
                           '$\\frac{3}{6} = \\frac{1}{2}$이므로, 두 주사위 모두 홀수가 나와 공을 $1$개 넣을 확률은 $\\frac{1}{2} \\times '
                           '\\frac{1}{2} = \\frac{1}{4}$입니다.',
              'knowledge_en': 'By elementary odd/even multiplication, a product of two integers is odd if and only if '
                              'both are odd. Since each die is odd with probability $\\frac{1}{2}$, the probability of '
                              'adding $1$ ball is $\\frac{1}{2} \\times \\frac{1}{2} = \\frac{1}{4}$.',
              'questions': [{'level_label': '초등 홀짝 확률 디딤돌 1',
                             'level_label_en': 'Elementary Parity Step 1',
                             'stem': '초등학교 홀짝 규칙에 따라 한 번의 시행에서 공을 $1$개 넣을(곱이 홀수일) 확률이 $\\frac{1}{4}$이면, 공을 $2$개 넣을(곱이 '
                                     '짝수일) 확률은?',
                             'stem_en': 'Using elementary probability subtraction, if the probability of adding $1$ '
                                        'ball is $\\frac{1}{4}$, what is the probability of adding $2$ balls?',
                             'options': ['$\\frac{1}{4}$',
                                         '$\\frac{1}{2}$',
                                         '$\\frac{2}{3}$',
                                         '$\\frac{3}{4}$',
                                         '$\\frac{5}{6}$'],
                             'answer': 4,
                             'exp': '$1 - \\frac{1}{4} = \\frac{3}{4}$입니다.',
                             'exp_en': '$1 - \\frac{1}{4} = \\frac{3}{4}$.'}]},
             {'title': '🌿 2단계 · [개수 합 분석] $4$번 시행 후 공이 $5$개 이하가 되는 경우 찾기',
              'title_en': '🌿 Step 2 · [Sum of Balls] Cases where 4 trials yield at most 5 balls',
              'knowledge': '매번 최소 $1$개씩 넣으므로 $4$번 시행하면 최소 $4$개가 들어갑니다. 총 $5$개 이하가 되려면 총합이 $4$개($1$개씩 $4$번)이거나 총합이 '
                           '$5$개($1$개씩 $3$번, $2$개 $1$번)여야 합니다.',
              'knowledge_en': 'In $4$ trials, adding $1$ or $2$ balls each time gives a total $\\le 5$ iff the total '
                              'is $4$ (four $1$s) or $5$ (three $1$s and one $2$).',
              'questions': [{'level_label': '총합 4개 확률 디딤돌 2',
                             'level_label_en': 'Sum $4$ Probability Step 2',
                             'stem': '$4$번 모두 공을 $1$개씩 넣어 총 $4$개가 될 확률 $\\left(\\frac{1}{4}\\right)^4$의 값은?',
                             'stem_en': 'What is the probability $\\left(\\frac{1}{4}\\right)^4$ of adding $1$ ball in '
                                        'all $4$ trials?',
                             'options': ['$\\frac{1}{16}$',
                                         '$\\frac{1}{64}$',
                                         '$\\frac{1}{128}$',
                                         '$\\frac{1}{256}$',
                                         '$\\frac{1}{512}$'],
                             'answer': 4,
                             'exp': '$4^4 = 16 \\times 16 = 256$이므로 $\\frac{1}{256}$입니다.',
                             'exp_en': '$\\left(\\frac{1}{4}\\right)^4 = \\frac{1}{256}$.'}]},
             {'title': '🌱 3단계 · [독립시행 확률] 공이 총 $5$개가 될 확률 구하기',
              'title_en': '🌱 Step 3 · [Independent Trials] Probability that the total is $5$ balls',
              'knowledge': '$4$번 중 $3$번은 $1$개(확률 $\\frac{1}{4}$), $1$번은 $2$개(확률 $\\frac{3}{4}$)를 넣을 확률은 '
                           '${}_{4}\\mathrm{C}_{3}\\left(\\frac{1}{4}\\right)^3\\left(\\frac{3}{4}\\right) = 4 \\times '
                           '\\frac{3}{256} = \\frac{12}{256}$입니다.',
              'knowledge_en': 'The probability of three $1$s and one $2$ is '
                              '${}_{4}\\mathrm{C}_{3}\\left(\\frac{1}{4}\\right)^3\\left(\\frac{3}{4}\\right) = '
                              '\\frac{12}{256}$.',
              'questions': [{'level_label': '총합 5개 분자 디딤돌 3',
                             'level_label_en': 'Sum $5$ Numerator Step 3',
                             'stem': '${}_{4}\\mathrm{C}_{3}\\left(\\frac{1}{4}\\right)^3\\left(\\frac{3}{4}\\right) = '
                                     '\\frac{k}{256}$에서 분자 $k = 4 \\times 3$의 값은?',
                             'stem_en': 'In '
                                        '${}_{4}\\mathrm{C}_{3}\\left(\\frac{1}{4}\\right)^3\\left(\\frac{3}{4}\\right) '
                                        '= \\frac{k}{256}$, what is the numerator $k = 4 \\times 3$?',
                             'options': ['$4$', '$8$', '$12$', '$16$', '$24$'],
                             'answer': 3,
                             'exp': '$4 \\times 3 = 12$입니다.',
                             'exp_en': '$4 \\times 3 = 12$.'}]},
             {'title': '🌳 4단계 · [분자 덧셈] 두 경우의 확률 분자끼리 더하기',
              'title_en': '🌳 Step 4 · [Adding Numerators] Adding $1 + 12$',
              'knowledge': '총 $4$개일 확률 $\\frac{1}{256}$과 총 $5$개일 확률 $\\frac{12}{256}$을 더합니다.',
              'knowledge_en': 'Add $\\frac{1}{256}$ and $\\frac{12}{256}$.',
              'questions': [{'level_label': '분자 합산 디딤돌 4',
                             'level_label_en': 'Numerator Sum Step 4',
                             'stem': '분모가 $256$으로 같을 때 두 분자의 합 $1 + 12$는?',
                             'stem_en': 'What is the sum of the numerators $1 + 12$?',
                             'options': ['$9$', '$11$', '$13$', '$15$', '$17$'],
                             'answer': 3,
                             'exp': '$1 + 12 = 13$입니다.',
                             'exp_en': '$1 + 12 = 13$.'}]},
             {'title': '💎 5단계 · [최종 종합] 공의 개수가 $5$ 이하일 확률 구하기',
              'title_en': '💎 Step 5 · [Final Synthesis] Final probability',
              'knowledge': '구하는 확률은 $\\frac{13}{256}$입니다.',
              'knowledge_en': 'The final probability is $\\frac{13}{256}$.',
              'questions': [{'level_label': '최종 종합 디딤돌 5',
                             'level_label_en': 'Final Synthesis Step 5',
                             'stem': '이 시행을 $4$번 반복한 후 상자에 들어 있는 공의 개수가 $5$ 이하일 확률은?',
                             'stem_en': 'What is the probability that the box contains at most $5$ balls after $4$ '
                                        'trials?',
                             'options': ['$\\frac{5}{256}$',
                                         '$\\frac{7}{256}$',
                                         '$\\frac{9}{256}$',
                                         '$\\frac{11}{256}$',
                                         '$\\frac{13}{256}$'],
                             'answer': 5,
                             'exp': '$\\frac{1}{256} + \\frac{12}{256} = \\frac{13}{256}$이므로 정답은 ⑤입니다.',
                             'exp_en': '$\\frac{13}{256}$ (choice ⑤).'}]}],
  'final': {'stem': '한 개의 주사위를 두 번 던져 나오는 눈의 수의 곱이 홀수이면 빈 상자에 공을 $1$개 넣고, 짝수이면 공을 $2$개 넣는 시행을 한다. 이 시행을 $4$번 반복한 후 상자에 '
                    '들어 있는 공의 개수가 $5$ 이하일 확률은? [3점]',
            'stem_en': 'A die is rolled twice: if the product of the outcomes is odd, $1$ ball is placed into an empty '
                       'box; if even, $2$ balls are placed. After repeating this trial $4$ times, what is the '
                       'probability that the box contains at most $5$ balls? [3 points]',
            'options': ['$\\dfrac{5}{256}$',
                        '$\\dfrac{7}{256}$',
                        '$\\dfrac{9}{256}$',
                        '$\\dfrac{11}{256}$',
                        '$\\dfrac{13}{256}$'],
            'answer': 5,
            'exp': '1회 시행에서 공을 $1$개 넣을 확률은 $\\dfrac{1}{4}$, $2$개 넣을 확률은 $\\dfrac{3}{4}$입니다. $4$회 시행 후 공이 $4$개 또는 $5$개일 '
                   '확률은 $\\left(\\dfrac{1}{4}\\right)^4 + '
                   '{}_{4}\\mathrm{C}_{1}\\left(\\dfrac{3}{4}\\right)\\left(\\dfrac{1}{4}\\right)^3 = '
                   '\\dfrac{13}{256}$입니다.',
            'exp_en': 'Each trial adds $1$ ball with probability $\\dfrac{1}{4}$ and $2$ balls with probability '
                      '$\\dfrac{3}{4}$. The probability of $\\le 5$ balls in $4$ trials is '
                      '$\\left(\\dfrac{1}{4}\\right)^4 + 4\\left(\\dfrac{3}{4}\\right)\\left(\\dfrac{1}{4}\\right)^3 = '
                      '\\dfrac{13}{256}$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>주사위 두 눈의 곱의 홀짝 확률</b>과 <b>독립시행의 확률</b>을 결합한 문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 1회 시행에서 공을 $1$개 또는 $2$개 넣을 확률</b><br>\n'
                        '  주사위를 두 번 던져 나온 눈의 수의 곱이 홀수이려면 두 번 모두 홀수가 나와야 하므로:<br>\n'
                        '  $$P(\\text{공 } 1\\text{개}) = \\frac{1}{2} \\times \\frac{1}{2} = \\frac{1}{4}, \\quad '
                        'P(\\text{공 } 2\\text{개}) = 1 - \\frac{1}{4} = \\frac{3}{4}$$<br>\n'
                        '  <b>2단계: $4$회 시행 후 공의 개수가 $5$ 이하일 확률</b><br>\n'
                        '  공의 개수가 $5$ 이하인 경우는 총 $4$개($1$개씩 $4$번) 또는 총 $5$개($1$개씩 $3$번, $2$개 $1$번)일 때이므로:<br>\n'
                        '  $${}_{4}\\mathrm{C}_{4}\\left(\\frac{1}{4}\\right)^4 + '
                        '{}_{4}\\mathrm{C}_{3}\\left(\\frac{1}{4}\\right)^3\\left(\\frac{3}{4}\\right) = '
                        '\\frac{1}{256} + \\frac{12}{256} = \\frac{13}{256}$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 구하는 확률은 $\\dfrac{13}{256}$이므로 정답은 <b>⑤번</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem combines <b>parity probability for two dice</b> with <b>independent '
                           'Bernoulli trials</b>.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Single-trial probabilities</b><br>\n'
                           '  $$P(1\\text{ ball}) = \\left(\\frac{1}{2}\\right)^2 = \\frac{1}{4}, \\quad P(2\\text{ '
                           'balls}) = \\frac{3}{4}$$<br>\n'
                           '  <b>Step 2: At most $5$ balls in $4$ trials</b><br>\n'
                           '  $$\\left(\\frac{1}{4}\\right)^4 + '
                           '{}_{4}\\mathrm{C}_{1}\\left(\\frac{3}{4}\\right)\\left(\\frac{1}{4}\\right)^3 = \\frac{1 + '
                           '12}{256} = \\frac{13}{256}$$\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  The correct answer is <b>choice ⑤ ($\\dfrac{13}{256}$)</b>.\n'
                           '</p>'}},
 {'slug': 'c2610p28',
  'qNum': '확통 28',
  'subject': '확률과 통계',
  'title': '[2026학년도 10월 고3 확통 28번] 같은 숫자가 적힌 카드의 선택과 같은 것이 있는 순열',
  'title_en': '[2026 AY Oct Exam Grade 12 Prob&Stats #28] Card Selection and Permutations with Identical Items',
  'summary_ko': '첫째 자리에 짝수($2$ 또는 $4$)를 놓은 뒤 나머지 $5$자리에 들어갈 숫자의 쌍 개수에 따라 케이스를 나누어 $2 \\times 360 = 720$ 구하기',
  'summary_en': 'Fix the first digit as even ($2$ choices: $2$ or $4$), classify the remaining $5$ digits by identical '
                'pairs, and compute $2 \\times 360 = 720$.',
  'tags': ['확률과 통계', '경우의수', '같은것이있는순열', '케이스분류', '28번'],
  'symbols': [{'sym': '$\\{1, 1, 2, 2, 3, 3, 4, 4\\}$',
               'desc': '1, 2, 3, 4가 각각 2장씩 들어 있는 총 8장의 카드',
               'desc_en': 'Eight cards consisting of two each of 1, 2, 3, and 4.'},
              {'sym': '$\\dfrac{5!}{2!2!} = 30,\\quad \\dfrac{5!}{2!} = 60$',
               'desc': '나머지 5개의 자리에 같은 숫자가 2쌍 또는 1쌍 있을 때의 나열 수',
               'desc_en': 'Permutations of 5 positions with two pairs (30) or one pair (60).'}],
  'levels': [{'title': '🔰 1단계 · [초등 짝수 고르기] 첫 번째 자리에 올 수 있는 짝수 종류 세기',
              'title_en': '🔰 Step 1 · [Elementary Even Numbers] Counting choices for the first even digit',
              'knowledge': '숫자 $1, 2, 3, 4$ 중에서 초등학교에서 배운 짝수는 $2$와 $4$ 두 가지입니다! 같은 숫자가 적힌 카드끼리는 구별하지 않으므로, 맨 앞자리에 놓을 수 '
                           '있는 숫자는 $2$ 또는 $4$의 $2$가지입니다.',
              'knowledge_en': 'Among $1, 2, 3, 4$, the elementary even numbers are $2$ and $4$. Since identical digits '
                              'are indistinguishable, there are $2$ choices for the first position.',
              'questions': [{'level_label': '초등 짝수 선택 디딤돌 1',
                             'level_label_en': 'Elementary Even Choice Step 1',
                             'stem': '초등학교 짝수 개념에 따라 첫 번째 자리에 놓을 수 있는 짝수($2$ 또는 $4$)의 선택 가짓수는?',
                             'stem_en': 'Using elementary even numbers, how many choices are there for the even digit '
                                        '($2$ or $4$) in the first position?',
                             'options': ['$1$', '$2$', '$3$', '$4$', '$6$'],
                             'answer': 2,
                             'exp': '$2$ 또는 $4$이므로 $2$가지입니다. (맨 앞자리를 $2$로 고정해 구한 뒤 $2$배 하면 됩니다!)',
                             'exp_en': 'There are $2$ choices ($2$ or $4$).'}]},
             {'title': '🌿 2단계 · [경우 1] 맨 앞이 $2$이고 나머지 $5$자리에 $2$가 안 쓰이는 경우',
              'title_en': '🌿 Step 2 · [Case 1] First digit is $2$, and the other $2$ is not used in the remaining $5$ '
                          'positions',
              'knowledge': '맨 앞에 $2$를 $1$장 썼을 때, 남은 카드 중 $2$를 빼고 $\\{1, 1, 3, 3, 4, 4\\}$ $6$장 중에서 $5$장을 골라 나열합니다. $1, '
                           '3, 4$ 중 $2$종류는 $2$장씩, $1$종류는 $1$장 쓰이므로 ${}_{3}\\mathrm{C}_{1} \\times \\frac{5!}{2!2!} = 3 '
                           '\\times 30 = 90$가지입니다.',
              'knowledge_en': 'If the second $2$ is not used, we pick $5$ cards from $\\{1, 1, 3, 3, 4, 4\\}$ (two '
                              'pairs and one single): $3 \\times \\frac{5!}{2!2!} = 3 \\times 30 = 90$ ways.',
              'questions': [{'level_label': '경우 1 나열 디딤돌 2',
                             'level_label_en': 'Case 1 Permutation Step 2',
                             'stem': '$3 \\times \\frac{5!}{2!2!} = 3 \\times 30$을 계산한 값은?',
                             'stem_en': 'What is the value of $3 \\times \\frac{5!}{2!2!} = 3 \\times 30$?',
                             'options': ['$60$', '$90$', '$120$', '$150$', '$180$'],
                             'answer': 2,
                             'exp': '$3 \\times 30 = 90$입니다.',
                             'exp_en': '$3 \\times 30 = 90$.'}]},
             {'title': '🌱 3단계 · [경우 2] 나머지 $5$자리에 남은 $2$가 $1$장 포함되는 경우',
              'title_en': '🌱 Step 3 · [Case 2] The remaining $2$ is included among the other $5$ positions',
              'knowledge': '남은 $2$ 한 장을 포함하면, 나머지 $4$자리는 $\\{1, 1, 3, 3, 4, 4\\}$에서 $4$장을 골라야 합니다. (a) 두 쌍(예: '
                           '$1,1,3,3$)을 고르면 ${}_{3}\\mathrm{C}_{2} \\times \\frac{5!}{2!2!} = 3 \\times 30 = 90$가지이고, '
                           '(b) 한 쌍과 단짝 두 개(예: $1,1,3,4$)를 고르면 ${}_{3}\\mathrm{C}_{1} \\times \\frac{5!}{2!} = 3 '
                           '\\times 60 = 180$가지입니다.',
              'knowledge_en': 'If the second $2$ is used, the other $4$ cards from $\\{1,1,3,3,4,4\\}$ can be: (a) two '
                              'pairs: ${}_{3}\\mathrm{C}_{2} \\times \\frac{5!}{2!2!} = 90$, or (b) one pair and two '
                              'singles: ${}_{3}\\mathrm{C}_{1} \\times \\frac{5!}{2!} = 180$.',
              'questions': [{'level_label': '경우 2 합산 디딤돌 3',
                             'level_label_en': 'Case 2 Sum Step 3',
                             'stem': '나머지 $5$자리에 $2$가 포함되는 경우의 수 $90 + 180$은?',
                             'stem_en': 'What is the sum $90 + 180$ for Case 2?',
                             'options': ['$180$', '$210$', '$240$', '$270$', '$300$'],
                             'answer': 4,
                             'exp': '$90 + 180 = 270$가지입니다.',
                             'exp_en': '$90 + 180 = 270$.'}]},
             {'title': '🌳 4단계 · [맨 앞이 $2$일 때 총합] 경우 1과 경우 2 더하기',
              'title_en': '🌳 Step 4 · [Total for First Digit $2$] Adding Case 1 and Case 2',
              'knowledge': '맨 앞자리가 $2$일 때 전체 경우의 수는 $90 + 270 = 360$가지입니다.',
              'knowledge_en': 'When the first digit is $2$, the total is $90 + 270 = 360$.',
              'questions': [{'level_label': '앞자리 2 총합 디딤돌 4',
                             'level_label_en': 'First Digit 2 Total Step 4',
                             'stem': '맨 앞자리가 $2$일 때의 총 경우의 수 $90 + 270$은?',
                             'stem_en': 'What is $90 + 270$?',
                             'options': ['$300$', '$330$', '$360$', '$390$', '$420$'],
                             'answer': 3,
                             'exp': '$90 + 270 = 360$입니다.',
                             'exp_en': '$90 + 270 = 360$.'}]},
             {'title': '💎 5단계 · [최종 종합] 첫 자리 짝수 $2$종류($2$ 또는 $4$) 곱하기',
              'title_en': '💎 Step 5 · [Final Synthesis] Multiplying by $2$ choices for the first digit',
              'knowledge': '맨 앞자리가 $4$일 때도 대칭성에 의해 똑같이 $360$가지이므로 $2 \\times 360 = 720$가지입니다.',
              'knowledge_en': 'By symmetry, starting with $4$ also gives $360$ ways, so $2 \\times 360 = 720$.',
              'questions': [{'level_label': '최종 종합 디딤돌 5',
                             'level_label_en': 'Final Synthesis Step 5',
                             'stem': '구하는 전체 경우의 수 $2 \\times 360$은?',
                             'stem_en': 'What is the total number of arrangements $2 \\times 360$?',
                             'options': ['$640$', '$680$', '$720$', '$760$', '$800$'],
                             'answer': 3,
                             'exp': '$2 \\times 360 = 720$이므로 정답은 ③입니다.',
                             'exp_en': '$2 \\times 360 = 720$ (choice ③).'}]}],
  'final': {'stem': '$1, 2, 3, 4$의 숫자가 하나씩 적혀 있는 카드가 각각 $2$장씩 $8$장이 있다. 이 $8$장의 카드 중에서 $6$장의 카드를 택하여 왼쪽에서 오른쪽으로 일렬로 '
                    '나열할 때, 첫 번째 자리에 놓인 카드에 적힌 수가 짝수인 경우의 수는? (단, 같은 숫자가 적힌 카드끼리는 서로 구별하지 않는다.) [4점]',
            'stem_en': 'There are $8$ cards, two each numbered $1, 2, 3, 4$. When $6$ cards are selected and arranged '
                       'in a row from left to right, how many arrangements have an even number in the first position? '
                       '(Cards with the same number are indistinguishable.) [4 points]',
            'options': ['$640$', '$680$', '$720$', '$760$', '$800$'],
            'answer': 3,
            'exp': '전체 $8$장 중 $6$장을 뽑아 일렬로 나열하는 총 경우의 수는 $1440$가지이고, 첫 번째 자리에 짝수($2, 4$)와 홀수($1, 3$)가 올 확률이 대칭이므로 '
                   '$\\dfrac{1440}{2} = 720$가지입니다.',
            'exp_en': 'By symmetry between even ($2, 4$) and odd ($1, 3$) digits, exactly half of all $6$-card '
                      'arrangements start with an even digit: $2 \\times (90 + 90 + 180) = 720$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>같은 것이 있는 순열과 대칭성</b>을 활용하여 $8$장 중 $6$장을 뽑아 나열하는 경우의 수를 구하는 문항입니다. 첫 번째 자리를 고정하고 '
                        '나머지 $5$자리를 분류하거나, 전체 $6$장 배열 수의 절반($\\frac{1}{2}$)으로 계산하면 매우 명쾌하게 풀립니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 뽑힌 $6$장의 카드 구성 분류 (전체 나열 수)</b><br>\n'
                        '  $8$장 중에서 $6$장을 택하면 제외되는 카드는 $2$장입니다:<br>\n'
                        '  - (유형 A) 같은 숫자 $2$장이 제외될 때 ($3$종류 각각 $2$장씩, 예: $1,1,2,2,3,3$):<br>\n'
                        '    제외할 숫자 선택 ${}_{4}\\mathrm{C}_{1} = 4$가지, $6$장 나열 $\\frac{6!}{2!2!2!} = 90$가지 $\\implies 4 '
                        '\\times 90 = 360$가지.<br>\n'
                        '  - (유형 B) 서로 다른 숫자 $2$장이 제외될 때 ($2$종류는 $2$장씩, $2$종류는 $1$장씩, 예: $1,1,2,2,3,4$):<br>\n'
                        '    제외할 숫자 $2$종류 선택 ${}_{4}\\mathrm{C}_{2} = 6$가지, $6$장 나열 $\\frac{6!}{2!2!} = 180$가지 '
                        '$\\implies 6 \\times 180 = 1080$가지.<br>\n'
                        '  따라서 $6$장을 택해 일렬로 나열하는 전체 경우의 수는 $360 + 1080 = 1440$가지입니다.<br><br>\n'
                        '  <b>2단계: 첫 번째 자리가 짝수인 경우의 수 (대칭성 활용)</b><br>\n'
                        '  숫자 $1, 2, 3, 4$가 모두 $2$장씩으로 동등하고 짝수($2, 4$)와 홀수($1, 3$)의 개수가 같으므로, 첫 번째 자리에 짝수가 오는 경우의 수는 '
                        '전체의 정확히 절반입니다:<br>\n'
                        '  $$\\frac{1440}{2} = 720$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 구하는 경우의 수는 $720$이므로 정답은 <b>③번</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem counts permutations of $6$ cards chosen from $\\{1,1,2,2,3,3,4,4\\}$ using '
                           '<b>permutations with repetition and symmetry</b>.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Total number of $6$-card arrangements</b><br>\n'
                           '  - Leaving out two identical cards: ${}_{4}\\mathrm{C}_{1} \\times \\frac{6!}{2!2!2!} = 4 '
                           '\\times 90 = 360$.<br>\n'
                           '  - Leaving out two different cards: ${}_{4}\\mathrm{C}_{2} \\times \\frac{6!}{2!2!} = 6 '
                           '\\times 180 = 1080$.<br>\n'
                           '  Total arrangements $= 360 + 1080 = 1440$.<br><br>\n'
                           '  <b>Step 2: Apply symmetry for the first digit</b><br>\n'
                           '  Since there are two even digits ($2, 4$) and two odd digits ($1, 3$) with identical '
                           'multiplicities, exactly half start with an even digit: $\\frac{1440}{2} = 720$.\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  The correct answer is <b>choice ③ ($720$)</b>.\n'
                           '</p>'}},
 {'slug': 'c2610p29',
  'qNum': '확통 29',
  'subject': '확률과 통계',
  'title': '[2026학년도 10월 고3 확통 29번] 두 정규분포의 대칭성과 확률밀도함수의 비교',
  'title_en': '[2026 AY Oct Exam Grade 12 Prob&Stats #29] Symmetry of Two Normal Distributions and Probability Density '
              'Comparison',
  'summary_ko': '조건 (가) $f(x)\\le f(4)$에서 $m_1=4$를 찾고, 대칭 구간 합 $\\mathrm{P}(6\\le X\\le 9)=\\mathrm{P}(11\\le Y\\le '
                '14)$와 조건 (나) $f(5)=g(15)$에서 $m_2=16$을 구하여 $1000k=345$ 도출하기',
  'summary_en': 'Find $m_1=4$ from $f(x)\\le f(4)$ in (가), merge symmetric intervals into $\\mathrm{P}(6\\le X\\le '
                '9)=\\mathrm{P}(11\\le Y\\le 14)$ and combine with $f(5)=g(15)$ to get $m_2=16$, yielding $1000k=345$.',
  'tags': ['확률과 통계', '통계', '정규분포', '확률밀도함수', '대칭성', '표준화', '단답형', '29번'],
  'symbols': [{'sym': '$f(x) \\le f(4) \\implies m_1 = 4$',
               'desc': '정규분포 곡선의 가장 높은 봉우리(최댓값)가 $x=4$이므로 평균 $m_1=4$',
               'desc_en': 'The peak of the normal density $f(x)$ is at $x=4$, so the mean is $m_1=4$.'},
              {'sym': '$\\mathrm{P}(1 \\le X \\le 2) = \\mathrm{P}(6 \\le X \\le 7)$',
               'desc': '평균 $m_1=4$에 대한 좌우 대칭으로 $[1, 2]$를 $[6, 7]$로 옮겨 $[7, 9]$와 이어붙임',
               'desc_en': 'By symmetry about $m_1=4$, $[1, 2]$ reflects to $[6, 7]$ and joins $[7, 9]$.'},
              {'sym': '$f(5) = g(15) \\iff |5 - 4| = |15 - m_2| = 1$',
               'desc': '표준편차가 $10$으로 같은 두 정규분포에서 함숫값이 같으려면 평균으로부터 떨어진 거리가 같아야 함',
               'desc_en': 'With equal standard deviations $\\sigma=10$, equal density values mean equal distances from '
                          'the mean.'}],
  'levels': [{'title': '🔰 1단계 · [초등 산봉우리 꼭대기 찾기] 조건 (가) $f(x) \\le f(4)$에서 평균 $m_1$ 구하기',
              'title_en': '🔰 Step 1 · [Elementary Peak Finding] Finding the mean $m_1$ from $f(x) \\le f(4)$',
              'knowledge': '초등학교 그래프 읽기처럼 정규분포의 확률밀도함수 $f(x)$는 **평균 $x = m_1$에서 가장 높은 산봉우리(최댓값)**를 가지는 좌우 대칭 종 모양 '
                           "곡선입니다! 조건 (가)에서 '모든 실수 $x$에 대하여 $f(x) \\le f(4)$'라는 뜻은 $x = 4$에서의 높이가 가장 높다는 뜻입니다.",
              'knowledge_en': 'Like reading the highest peak of a hill in elementary math, a normal density curve '
                              '$f(x)$ reaches its maximum at the mean $x = m_1$. Condition (가) $f(x) \\le f(4)$ tells '
                              'us the highest peak is at $x = 4$.',
              'questions': [{'level_label': '초등 최댓값 봉우리 디딤돌 1',
                             'level_label_en': 'Elementary Peak Step 1',
                             'stem': '초등학교 그래프에서 가장 높은 곳을 찾듯이, 모든 실수 $x$에 대하여 $f(x) \\le f(4)$일 때 정규분포 '
                                     '$\\mathrm{N}(m_1, 10^2)$의 평균 $m_1$의 값은?',
                             'stem_en': 'Since $f(x) \\le f(4)$ for all real $x$, what is the mean $m_1$ of $X \\sim '
                                        '\\mathrm{N}(m_1, 10^2)$?',
                             'options': ['$2$', '$3$', '$4$', '$5$', '$6$'],
                             'answer': 3,
                             'exp': '$x = 4$에서 함숫값이 최대이므로 대칭축인 평균은 $m_1 = 4$입니다.',
                             'exp_en': 'The maximum occurs at the mean, so $m_1 = 4$.'}]},
             {'title': '🌿 2단계 · [초등 수직선 거울 대칭] 평균 $m_1 = 4$를 기준으로 구간 $[1, 2]$를 반대쪽으로 접기',
              'title_en': '🌿 Step 2 · [Mirror Symmetry on a Number Line] Reflecting $[1, 2]$ across $m_1 = 4$',
              'knowledge': '수직선에서 중심 $4$를 거울 삼아 왼쪽의 숫자를 오른쪽으로 똑같은 거리만큼 옮겨 봅시다.<ul><li>$2$는 $4$보다 왼쪽으로 $2$칸($4 - 2 = '
                           '2$) 떨어져 있으므로, 오른쪽으로 $2$칸 가면 $4 + 2 = 6$입니다.</li><li>$1$은 $4$보다 왼쪽으로 $3$칸($4 - 1 = 3$) 떨어져 '
                           '있으므로, 오른쪽으로 $3$칸 가면 $4 + 3 = 7$입니다.</li></ul>따라서 좌우 대칭에 의해 $\\mathrm{P}(1 \\le X \\le 2) = '
                           '\\mathrm{P}(6 \\le X \\le 7)$입니다!',
              'knowledge_en': 'Reflecting across $m_1 = 4$: $2$ ($2$ units left of $4$) maps to $4 + 2 = 6$, and $1$ '
                              '($3$ units left of $4$) maps to $4 + 3 = 7$. Thus $\\mathrm{P}(1 \\le X \\le 2) = '
                              '\\mathrm{P}(6 \\le X \\le 7)$.',
              'questions': [{'level_label': '수직선 대칭 이동 디딤돌 2',
                             'level_label_en': 'Symmetric Reflection Step 2',
                             'stem': '평균 $m_1 = 4$에 대하여 구간 $1 \\le X \\le 2$와 넓이(확률)가 똑같은 오른쪽 대칭 구간은?',
                             'stem_en': 'By symmetry about $m_1 = 4$, which interval on the right has the exact same '
                                        'probability as $1 \\le X \\le 2$?',
                             'options': ['$4 \\le X \\le 5$',
                                         '$5 \\le X \\le 6$',
                                         '$6 \\le X \\le 7$',
                                         '$7 \\le X \\le 8$',
                                         '$8 \\le X \\le 9$'],
                             'answer': 3,
                             'exp': '$4 + (4 - 2) = 6$, $4 + (4 - 1) = 7$이므로 구간 $6 \\le X \\le 7$과 확률이 같습니다.',
                             'exp_en': 'Reflecting $[1, 2]$ across $4$ gives $[6, 7]$.'}]},
             {'title': '🌱 3단계 · [구간 이어붙이기] $\\mathrm{P}(6 \\le X \\le 7) + \\mathrm{P}(7 \\le X \\le 9)$를 하나의 구간으로 합치기',
              'title_en': '🌱 Step 3 · [Joining Intervals] Merging $\\mathrm{P}(6 \\le X \\le 7) + \\mathrm{P}(7 \\le X '
                          '\\le 9)$',
              'knowledge': '2단계 덕분에 문제의 좌변 $\\mathrm{P}(1 \\le X \\le 2) + \\mathrm{P}(7 \\le X \\le 9)$는 '
                           '$\\mathrm{P}(6 \\le X \\le 7) + \\mathrm{P}(7 \\le X \\le 9)$가 되었습니다! $6$부터 $7$까지의 넓이와 '
                           '$7$부터 $9$까지의 넓이를 이어붙이면 바로 $6$부터 $9$까지의 하나의 연결된 구간 넓이가 됩니다.',
              'knowledge_en': 'Since $[6, 7]$ and $[7, 9]$ meet at $7$, their probabilities add up to a single '
                              'continuous interval $\\mathrm{P}(6 \\le X \\le 9)$.',
              'questions': [{'level_label': '구간 결합 디딤돌 3',
                             'level_label_en': 'Interval Merge Step 3',
                             'stem': '$\\mathrm{P}(6 \\le X \\le 7) + \\mathrm{P}(7 \\le X \\le 9)$를 하나의 구간 확률 '
                                     '$\\mathrm{P}(6 \\le X \\le 9)$로 합쳤을 때, 이 구간 $[6, 9]$는 평균 $m_1 = 4$로부터 오른쪽으로 몇 '
                                     '칸에서 몇 칸까지 떨어진 구간인가요?',
                             'stem_en': 'When merged into $\\mathrm{P}(6 \\le X \\le 9)$, how many units to the right '
                                        'of the mean $m_1 = 4$ does the interval $[6, 9]$ lie?',
                             'options': ['$1$칸 ~ $3$칸', '$1$칸 ~ $4$칸', '$2$칸 ~ $5$칸', '$3$칸 ~ $6$칸', '$4$칸 ~ $7$칸'],
                             'answer': 3,
                             'exp': '$6 - 4 = 2$칸, $9 - 4 = 5$칸이므로 평균 $4$로부터 거리가 $2$ 이상 $5$ 이하인 구간입니다!',
                             'exp_en': '$6 - 4 = 2$ and $9 - 4 = 5$, so it lies from $2$ to $5$ units from the '
                                       'mean.'}]},
             {'title': '🌱 4단계 · [조건 (나) $f(5) = g(15)$ 해석] $m_2$의 후보 두 개 찾기',
              'title_en': '🌱 Step 4 · [Condition (나) $f(5) = g(15)$] Finding the two candidates for $m_2$',
              'knowledge': '두 확률변수 $X \\sim \\mathrm{N}(4, 10^2)$과 $Y \\sim \\mathrm{N}(m_2, 10^2)$는 **표준편차가 $10$으로 '
                           '똑같기 때문에** 종 모양 곡선의 생김새가 완전히 합동입니다! 따라서 두 곡선의 높이가 같으려면($f(5) = g(15)$), 각각의 평균으로부터 떨어진 거리가 '
                           '같아야 합니다:$$|15 - m_2| = |5 - 4| = 1$$',
              'knowledge_en': 'Because $X$ and $Y$ share the same standard deviation $\\sigma = 10$, their density '
                              'curves are congruent. Thus $f(5) = g(15)$ holds iff $15$ is the same distance from '
                              '$m_2$ as $5$ is from $m_1 = 4$: $|15 - m_2| = |5 - 4| = 1$.',
              'questions': [{'level_label': '평균으로부터의 거리 디딤돌 4',
                             'level_label_en': 'Distance from Mean Step 4',
                             'stem': '$15$와의 거리가 $1$인 수, 즉 $|15 - m_2| = 1$을 만족시키는 $m_2$의 두 후보 값은?',
                             'stem_en': 'Which two values of $m_2$ satisfy $|15 - m_2| = 1$?',
                             'options': ['$12$ 또는 $14$',
                                         '$13$ 또는 $15$',
                                         '$14$ 또는 $16$',
                                         '$15$ 또는 $17$',
                                         '$16$ 또는 $18$'],
                             'answer': 3,
                             'exp': '$15 - 1 = 14$ 또는 $15 + 1 = 16$이므로 $m_2$의 후보는 $14$ 또는 $16$입니다.',
                             'exp_en': '$m_2 = 14$ or $m_2 = 16$.'}]},
             {'title': '🌳 5단계 · [평균 $m_2$ 확정] $\\mathrm{P}(6 \\le X \\le 9) = \\mathrm{P}(11 \\le Y \\le 14)$로 $m_2 = '
                       '16$ 결정하기',
              'title_en': '🌳 Step 5 · [Determining $m_2$] Using $\\mathrm{P}(6 \\le X \\le 9) = \\mathrm{P}(11 \\le Y '
                          '\\le 14)$ to fix $m_2 = 16$',
              'knowledge': '3단계에서 좌변의 구간 $[6, 9]$는 평균 $m_1 = 4$로부터 **거리가 $2 \\sim 5$만큼 떨어진 구간**이었습니다. 모양이 똑같은 $Y$에서도 '
                           '우변 $\\mathrm{P}(11 \\le Y \\le 14)$의 넓이가 같으려면, 구간 $[11, 14]$ 역시 평균 $m_2$로부터 **거리가 $2 \\sim '
                           '5$만큼 떨어진 구간**이어야 합니다!<ul><li>만약 $m_2 = 14$이면 구간 $[11, 14]$는 평균 $14$로부터 거리가 $0 \\sim 3$이어서 '
                           '넓이가 다릅니다(탈락!).</li><li>만약 $m_2 = 16$이면 $16 - 14 = 2$, $16 - 11 = 5$이므로 평균 $16$으로부터 거리가 정확히 '
                           '$2 \\sim 5$가 되어 일치합니다!</li></ul>',
              'knowledge_en': 'For $\\mathrm{P}(6 \\le X \\le 9) = \\mathrm{P}(11 \\le Y \\le 14)$ to hold, $[11, 14]$ '
                              'must also lie at distance $2$ to $5$ from $m_2$. Testing the candidates: $m_2 = 14$ '
                              'gives distance $0$ to $3$ (invalid), whereas $m_2 = 16$ gives distance $16 - 14 = 2$ to '
                              '$16 - 11 = 5$ (valid!).',
              'questions': [{'level_label': '평균 m2 확정 디딤돌 5',
                             'level_label_en': 'Confirming m2 Step 5',
                             'stem': '구간 $[11, 14]$의 오른쪽 끝점 $14$가 평균 $m_2$보다 왼쪽으로 $2$칸 떨어져 있도록($m_2 - 14 = 2$) 하는 '
                                     '$m_2$의 값은?',
                             'stem_en': 'Which value of $m_2$ places the endpoint $14$ at distance $2$ below $m_2$ '
                                        '($m_2 - 14 = 2$)?',
                             'options': ['$13$', '$14$', '$15$', '$16$', '$17$'],
                             'answer': 4,
                             'exp': '$m_2 = 14 + 2 = 16$일 때 구간 $[11, 14]$는 평균 $16$으로부터 거리가 $2 \\sim 5$가 되어 좌변과 넓이가 완전히 '
                                    '같아집니다.',
                             'exp_en': '$m_2 = 16$.'}]},
             {'title': '🌳 6단계 · [표준화 $Z$ 변환] $Y \\sim \\mathrm{N}(16, 10^2)$에서 $\\mathrm{P}(Y \\ge 20)$을 표준정규분포로 바꾸기',
              'title_en': '🌳 Step 6 · [Standardization] Converting $\\mathrm{P}(Y \\ge 20)$ using $Z = \\dfrac{Y - '
                          '16}{10}$',
              'knowledge': '이제 $Y$의 평균 $m_2 = 16$과 표준편차 $\\sigma_2 = 10$을 모두 알았습니다! 구하려는 확률 $\\mathrm{P}(Y \\ge 20)$을 '
                           '표준정규분포표로 읽으려면 $Y$에서 평균 $16$을 빼고 표준편차 $10$으로 나눈 표준화 변수 $Z = \\dfrac{Y - 16}{10}$으로 바꿉니다.',
              'knowledge_en': 'With $m_2 = 16$ and $\\sigma_2 = 10$, standardize $Y = 20$ via $Z = \\dfrac{20 - '
                              '16}{10}$.',
              'questions': [{'level_label': '표준화 Z값 디딤돌 6',
                             'level_label_en': 'Standardization Step 6',
                             'stem': '$Y = 20$일 때, 표준화 공식 $Z = \\dfrac{20 - 16}{10}$으로 계산한 $z$의 값은?',
                             'stem_en': 'What is the standardized value $z = \\dfrac{20 - 16}{10}$ when $Y = 20$?',
                             'options': ['$0.2$', '$0.3$', '$0.4$', '$0.5$', '$0.6$'],
                             'answer': 3,
                             'exp': '$\\dfrac{20 - 16}{10} = \\dfrac{4}{10} = 0.4$이므로 $\\mathrm{P}(Y \\ge 20) = '
                                    '\\mathrm{P}(Z \\ge 0.4)$입니다.',
                             'exp_en': '$\\dfrac{4}{10} = 0.4$.'}]},
             {'title': '💎 7단계 · [표준정규분포표 읽기] 오른쪽 꼬리 확률 $k = \\mathrm{P}(Z \\ge 0.4)$ 구하기',
              'title_en': '💎 Step 7 · [Reading the Normal Table] Computing the upper tail $k = \\mathrm{P}(Z \\ge '
                          '0.4)$',
              'knowledge': '표준정규분포 곡선에서 $Z \\ge 0$인 오른쪽 반쪽 전체의 넓이는 $0.5$입니다. 문제의 표에서 가운데 부분 넓이 $\\mathrm{P}(0 \\le Z '
                           '\\le 0.4) = 0.155$이므로, $0.4$보다 오른쪽 꼬리 부분의 넓이 $k = \\mathrm{P}(Z \\ge 0.4)$는 $0.5$에서 '
                           '$0.155$를 빼면 됩니다!',
              'knowledge_en': 'Since $\\mathrm{P}(Z \\ge 0) = 0.5$ and the table gives $\\mathrm{P}(0 \\le Z \\le 0.4) '
                              '= 0.155$, the tail probability is $k = 0.5 - 0.155$.',
              'questions': [{'level_label': '꼬리 확률 계산 디딤돌 7',
                             'level_label_en': 'Tail Probability Step 7',
                             'stem': '$k = \\mathrm{P}(Z \\ge 0.4) = 0.5 - 0.155$를 계산한 값은?',
                             'stem_en': 'What is $k = 0.5 - 0.155$?',
                             'options': ['$0.245$', '$0.315$', '$0.345$', '$0.355$', '$0.385$'],
                             'answer': 3,
                             'exp': '$0.500 - 0.155 = 0.345$입니다.',
                             'exp_en': '$0.500 - 0.155 = 0.345$.'}]},
             {'title': '🏆 8단계 · [최종 정답 완성] $1000 \\times k$의 값 구하기',
              'title_en': '🏆 Step 8 · [Final Synthesis] Computing $1000 \\times k$',
              'knowledge': '$k = 0.345$에 $1000$을 곱하면 소수점이 오른쪽으로 세 칸 이동하여 자연수 $345$가 완성됩니다.',
              'knowledge_en': 'Multiply $k = 0.345$ by $1000$ to obtain the final answer $345$.',
              'questions': [{'level_label': '최종 종합 디딤돌 8',
                             'level_label_en': 'Final Synthesis Step 8',
                             'stem': '$k = 0.345$일 때, $1000 \\times k$의 값은?',
                             'stem_en': 'Given $k = 0.345$, what is $1000 \\times k$?',
                             'options': ['$315$', '$335$', '$345$', '$355$', '$365$'],
                             'answer': 3,
                             'exp': '$1000 \\times 0.345 = 345$입니다.',
                             'exp_en': '$1000 \\times 0.345 = 345$.'}]}],
  'final': {'stem': '확률변수 $X$는 정규분포 $\\mathrm{N}(m_1, 10^2)$을 따르고, 확률변수 $Y$는 정규분포 $\\mathrm{N}(m_2, 10^2)$을 따른다. 확률변수 '
                    '$X$의 확률밀도함수 $f(x)$와 확률변수 $Y$의 확률밀도함수 $g(x)$가 다음 조건을 만족시킨다.<br><br>(가) 모든 실수 $x$에 대하여 $f(x) \\le '
                    'f(4)$이다.<br>(나) $f(5) = g(15)$<br><br>$\\mathrm{P}(1 \\le X \\le 2) + \\mathrm{P}(7 \\le X \\le '
                    '9) = \\mathrm{P}(11 \\le Y \\le 14)$일 때, $\\mathrm{P}(Y \\ge 20)$의 값을 표준정규분포표를 이용하여 구한 값이 $k$이다. '
                    '$1000 \\times k$의 값을 구하시오. (단, $\\mathrm{P}(0 \\le Z \\le 0.4) = 0.155$) [4점]',
            'stem_en': 'Random variables $X \\sim \\mathrm{N}(m_1, 10^2)$ and $Y \\sim \\mathrm{N}(m_2, 10^2)$ have '
                       'probability density functions $f(x)$ and $g(x)$ satisfying:<br>(가) $f(x) \\le f(4)$ for all '
                       'real $x$.<br>(나) $f(5) = g(15)$.<br>Given $\\mathrm{P}(1 \\le X \\le 2) + \\mathrm{P}(7 \\le X '
                       '\\le 9) = \\mathrm{P}(11 \\le Y \\le 14)$, let $k = \\mathrm{P}(Y \\ge 20)$ using '
                       '$\\mathrm{P}(0 \\le Z \\le 0.4) = 0.155$. Find $1000 \\times k$. [4 points]',
            'options': ['$315$', '$335$', '$345$', '$355$', '$365$'],
            'answer': 3,
            'exp': '조건 (가)에서 $m_1 = 4$이고, 대칭성에 의해 $\\mathrm{P}(1 \\le X \\le 2) + \\mathrm{P}(7 \\le X \\le 9) = '
                   '\\mathrm{P}(6 \\le X \\le 9) = \\mathrm{P}(11 \\le Y \\le 14)$입니다. 조건 (나) $f(5)=g(15)$에서 '
                   '$|15-m_2|=1 \\implies m_2 \\in \\{14, 16\\}$이며 구간 거리 비교로 $m_2 = 16$이 확정됩니다. 따라서 $k = \\mathrm{P}(Z '
                   '\\ge 0.4) = 0.5 - 0.155 = 0.345$이고 $1000k = 345$입니다.',
            'exp_en': 'From (가) $m_1 = 4$, and by symmetry $\\mathrm{P}(1 \\le X \\le 2) + \\mathrm{P}(7 \\le X \\le '
                      '9) = \\mathrm{P}(6 \\le X \\le 9) = \\mathrm{P}(11 \\le Y \\le 14)$. Combining with '
                      '$f(5)=g(15)$ fixes $m_2 = 16$, so $k = \\mathrm{P}(Z \\ge 0.4) = 0.345$ and $1000k = 345$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>정규분포 곡선의 최댓값(평균)과 대칭성</b>을 이용하여 떨어진 두 구간의 확률 합을 하나의 연결된 구간 확률로 바꾼 뒤, 표준편차가 같은 두 '
                        '정규분포의 평행이동 관계를 추론하는 문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 조건 (가)에서 평균 $m_1 = 4$ 도출 및 대칭 구간 결합</b><br>\n'
                        '  조건 (가)에서 모든 실수 $x$에 대하여 $f(x) \\le f(4)$이므로 정규분포 $\\mathrm{N}(m_1, 10^2)$의 대칭축(평균)은 $m_1 = '
                        '4$입니다.<br>\n'
                        '  평균 $m_1 = 4$에 대한 대칭성에 의해 구간 $[1, 2]$를 $x = 4$에 대칭이동하면 $[6, 7]$이 되므로 $\\mathrm{P}(1 \\le X '
                        '\\le 2) = \\mathrm{P}(6 \\le X \\le 7)$입니다. 따라서:<br>\n'
                        '  $$\\mathrm{P}(1 \\le X \\le 2) + \\mathrm{P}(7 \\le X \\le 9) = \\mathrm{P}(6 \\le X \\le '
                        '7) + \\mathrm{P}(7 \\le X \\le 9) = \\mathrm{P}(6 \\le X \\le 9)$$<br>\n'
                        '  <b>2단계: 조건 (나)와 구간 비교로 $m_2 = 16$ 확정</b><br>\n'
                        '  두 정규분포의 표준편차가 모두 $10$으로 같으므로, 조건 (나) $f(5) = g(15)$에서:<br>\n'
                        '  $$|15 - m_2| = |5 - 4| = 1 \\implies m_2 = 14 \\text{ 또는 } m_2 = 16$$\n'
                        '  또한 $\\mathrm{P}(6 \\le X \\le 9) = \\mathrm{P}(11 \\le Y \\le 14)$에서 좌변의 구간 $[6, 9]$는 평균 '
                        '$m_1 = 4$로부터 거리가 $2$ 이상 $5$ 이하인 구간입니다. 우변의 구간 $[11, 14]$도 평균 $m_2$로부터 거리가 $2$ 이상 $5$ 이하가 되려면 '
                        '$m_2 = 16$이어야 합니다.<br><br>\n'
                        '  <b>3단계: $\\mathrm{P}(Y \\ge 20)$ 표준화 계산</b><br>\n'
                        '  $Y \\sim \\mathrm{N}(16, 10^2)$이므로:<br>\n'
                        '  $$k = \\mathrm{P}(Y \\ge 20) = \\mathrm{P}\\left(Z \\ge \\frac{20 - 16}{10}\\right) = '
                        '\\mathrm{P}(Z \\ge 0.4) = 0.5 - 0.155 = 0.345$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 $1000 \\times k = 1000 \\times 0.345 =$ <b>$345$</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem uses the <b>peak and symmetry of normal density curves</b> with equal '
                           'standard deviations ($\\sigma = 10$) to merge disjoint probability intervals and determine '
                           '$m_1$ and $m_2$.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Symmetry of $X$</b><br>\n'
                           '  From $f(x) \\le f(4)$, the mean is $m_1 = 4$. Reflecting $[1, 2]$ across $4$ gives $[6, '
                           '7]$, so $\\mathrm{P}(1 \\le X \\le 2) + \\mathrm{P}(7 \\le X \\le 9) = \\mathrm{P}(6 \\le '
                           'X \\le 9) = \\mathrm{P}(11 \\le Y \\le 14)$.<br><br>\n'
                           '  <b>Step 2: Mean $m_2$ of $Y$ and final probability</b><br>\n'
                           '  From $f(5) = g(15)$ with $\\sigma_1 = \\sigma_2 = 10$, we have $|15 - m_2| = |5 - 4| = 1 '
                           '\\implies m_2 \\in \\{14, 16\\}$. Since $[6, 9]$ is at distance $2$ to $5$ from $4$, $[11, '
                           '14]$ must be at distance $2$ to $5$ from $m_2$, fixing $m_2 = 16$. Thus:<br>\n'
                           '  $$k = \\mathrm{P}(Y \\ge 20) = \\mathrm{P}\\left(Z \\ge \\frac{20-16}{10}\\right) = '
                           '\\mathrm{P}(Z \\ge 0.4) = 0.5 - 0.155 = 0.345$$\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  Therefore, $1000k =$ <b>$345$</b>.\n'
                           '</p>'}},
 {'slug': 'c2610p30',
  'qNum': '확통 30',
  'subject': '확률과 통계',
  'title': '[2026학년도 10월 고3 확통 30번] 두 주머니에서 비복원 추출과 조건부확률',
  'title_en': '[2026 AY Oct Exam Grade 12 Prob&Stats #30] Conditional Probability with Sampling Without Replacement '
              'from Two Bags',
  'summary_ko': '전체 $400$가지에서 $a_1=2$($32$가지)·$a_2=2$($32$가지)를 빼 분모 $336$가지를 구하고, $\\mathrm{B}$에서 $(1,2)$ 또는 $(2,1)$을 '
                '뽑는 분자 $48+48=96$가지를 구해 조건부확률 $\\dfrac{96}{336}=\\dfrac{2}{7}$ 도출하기',
  'summary_en': 'Subtract $a_1=2$ ($32$ ways) and $a_2=2$ ($32$ ways) from $400$ total outcomes to get denominator '
                '$336$, count $48+48=96$ numerator outcomes where $\\mathrm{B}$ draws $(1,2)$ or $(2,1)$ with '
                '$a_1=a_2=1$, and reduce $\\dfrac{96}{336}=\\dfrac{2}{7}$ ($p+q=9$).',
  'tags': ['확률과 통계', '확률', '조건부확률', '비복원추출', '여사건', '경우의수', '단답형', '30번'],
  'symbols': [{'sym': '$\\mathrm{A}=\\{1_a,1_b,1_c,2_a,2_b\\},\\ \\mathrm{B}=\\{1_p,1_q,1_r,1_s,2_p\\}$',
               'desc': '주머니 $\\mathrm{A}$($1$이 $3$개, $2$가 $2$개)와 주머니 $\\mathrm{B}$($1$이 $4$개, $2$가 $1$개)의 서로 구별되는 공 '
                       '$5$개씩',
               'desc_en': 'Five distinguishable balls in Bag $\\mathrm{A}$ (three $1$s, two $2$s) and Bag '
                          '$\\mathrm{B}$ (four $1$s, one $2$).'},
              {'sym': '$a_n = 1 \\iff \\text{꺼낸 두 공이 } (2, 2)\\text{가 아님}$',
               'desc': '두 수 중 크지 않은 수($\\min$)가 $1$이 될 조건: 적어도 한 주머니에서 $1$이 나오면 무조건 $a_n=1$!',
               'desc_en': 'The minimum of two drawn numbers is $1$ unless both bags draw $2$.'},
              {'sym': '$\\mathrm{P}(F \\mid E) = \\dfrac{n(E \\cap F)}{n(E)} = \\dfrac{48 + 48}{400 - (32 + 32)} = '
                      '\\dfrac{96}{336} = \\dfrac{2}{7}$',
               'desc': '사건 $E(a_1=a_2=1)$가 일어났을 때 사건 $F(\\mathrm{B}\\text{에 }1\\text{이 }3\\text{개 남음})$의 조건부확률',
               'desc_en': 'Conditional probability of three $1$s remaining in $\\mathrm{B}$ given $a_1=a_2=1$.'}],
  'levels': [{'title': "🔰 1단계 · [초등 수 비교와 규칙 번역] '두 수 중 크지 않은 수($a_n$)'가 언제 $1$이 되고 언제 $2$가 될까?",
              'title_en': "🔰 Step 1 · [Elementary Comparison] When is the 'number not larger ($a_n$)' equal to $1$ vs. "
                          '$2$?',
              'knowledge': "문제에서 **'두 수 중 크지 않은 수'**란 두 숫자를 비교했을 때 **더 작거나 같은 수**를 뜻합니다! 주머니 속 공에는 숫자 $1$ 아니면 $2$만 적혀 "
                           '있으므로 네 가지 경우를 직접 비교해 봅시다.<ul><li>$(\\mathrm{A}=1,\\ \\mathrm{B}=1) \\implies$ 크지 않은 수는 '
                           '**$1$**</li><li>$(\\mathrm{A}=1,\\ \\mathrm{B}=2) \\implies 1$과 $2$ 중 크지 않은 수는 '
                           '**$1$**</li><li>$(\\mathrm{A}=2,\\ \\mathrm{B}=1) \\implies 2$와 $1$ 중 크지 않은 수는 '
                           '**$1$**</li><li>$(\\mathrm{A}=2,\\ \\mathrm{B}=2) \\implies$ 둘 다 $2$이므로 이때만 크지 않은 수가 '
                           '**$2$**!</li></ul>즉, **둘 중 하나라도 $1$이 나오면 무조건 $a_n = 1$**이고, 오직 **두 주머니 모두 $2$를 꺼낸 $(2, '
                           '2)$일 때만 $a_n = 2$**가 됩니다!',
              'knowledge_en': "'The number not larger' simply means the smaller (or equal) of the two numbers drawn. "
                              'Since balls only have $1$ or $2$: $(1,1)\\to 1$, $(1,2)\\to 1$, $(2,1)\\to 1$, and ONLY '
                              '$(2,2)\\to 2$. Thus $a_n = 1$ whenever at least one bag draws $1$, and $a_n = 2$ only '
                              'when both bags draw $2$!',
              'questions': [{'level_label': '초등 숫자 비교 디딤돌 1',
                             'level_label_en': 'Elementary Comparison Step 1',
                             'stem': '초등학교 숫자 비교 규칙으로, 한 시행에서 주머니 $\\mathrm{A}$와 주머니 $\\mathrm{B}$에서 꺼낸 두 공의 숫자가 $(1, '
                                     "2)$일 때 '두 수 중 크지 않은 수'는 얼마이고, 반대로 크지 않은 수가 $2$가 되려면 두 공의 숫자가 무엇이어야 할까요?",
                             'stem_en': 'Using elementary number comparison, if the drawn pair is $(1, 2)$, what is '
                                        "the 'number not larger', and which pair is the ONLY one that makes it $2$?",
                             'options': ['$(1, 2)$일 때는 $1$이고, 오직 $(2, 2)$일 때만 $2$가 된다.',
                                         '$(1, 2)$일 때는 $2$이고, 오직 $(1, 1)$일 때만 $1$이 된다.',
                                         '$(1, 2)$일 때는 $1$이고, $(1, 2)$나 $(2, 1)$이어도 $2$가 된다.',
                                         '$(1, 2)$일 때는 $2$이고, 오직 $(2, 2)$일 때만 $2$가 된다.',
                                         '모든 경우에서 항상 $1$이 된다.'],
                             'answer': 1,
                             'exp': '$1$과 $2$ 중 크지 않은(작거나 같은) 수는 $1$입니다. 크지 않은 수가 $2$가 되는 경우는 두 주머니 모두 $2$를 뽑은 $(2, '
                                    '2)$ 한 가지뿐입니다!',
                             'exp_en': 'The minimum of $(1, 2)$ is $1$, and the minimum is $2$ if and only if the pair '
                                       'is $(2, 2)$.'}]},
             {'title': '🌿 2단계 · [초등 곱셈과 전체 가짓수] 두 주머니에서 각각 $2$번 연속 공을 꺼내는 전체 경우의 수($400$가지)',
              'title_en': '🌿 Step 2 · [Elementary Multiplication] Total outcomes ($400$) for drawing $2$ balls without '
                          'replacement from both bags',
              'knowledge': '확률을 정확히 계산하려면 같은 숫자가 적힌 공이라도 서로 다른 공(예: $1_a, 1_b, 1_c, 2_a, 2_b$)으로 번호표를 붙여 구별해서 세어야 모든 '
                           '경우가 똑같은 가능성을 가집니다.<ul><li>**주머니 $\\mathrm{A}$ (공 $5$개)**: $1$회차에 꺼낼 수 있는 공 $5$가지 $\\times$ '
                           '다시 넣지 않고 $2$회차에 남은 $4$개 중 꺼내는 공 $4$가지 $= 5 \\times 4 = 20$가지</li><li>**주머니 $\\mathrm{B}$ '
                           '(공 $5$개)**: 마찬가지로 $1$회차 $5$가지 $\\times$ $2$회차 $4$가지 $= 5 \\times 4 = 20$가지</li><li>**두 주머니 '
                           '동시 진행**: 주머니 $\\mathrm{A}$의 $20$가지 각각에 대하여 주머니 $\\mathrm{B}$의 $20$가지가 짝지어지므로 전체 경우의 수는 $20 '
                           '\\times 20 = 400$가지입니다!</li></ul>',
              'knowledge_en': 'Treating all $5$ balls in each bag as distinct: Bag A has $5 \\times 4 = 20$ ordered '
                              'pairs of draws without replacement, and Bag B also has $5 \\times 4 = 20$ ordered '
                              'pairs. Together there are $20 \\times 20 = 400$ equally likely total outcomes.',
              'questions': [{'level_label': '초등 곱셈 법칙 디딤돌 2',
                             'level_label_en': 'Elementary Multiplication Step 2',
                             'stem': '공 $5$개가 든 주머니 하나에서 다시 넣지 않고 $2$번 연속 꺼내는 가짓수는 $5 \\times 4 = 20$가지입니다. 두 주머니 '
                                     '$\\mathrm{A}, \\mathrm{B}$에서 동시에 $2$번씩 시행할 때 가능한 전체 경우의 수 $20 \\times 20$은?',
                             'stem_en': 'Each bag has $5 \\times 4 = 20$ ordered pairs of draws. What is the total '
                                        'number of outcomes $20 \\times 20$ for both bags together?',
                             'options': ['$100$', '$200$', '$300$', '$400$', '$500$'],
                             'answer': 4,
                             'exp': '$20 \\times 20 = 400$가지가 아무 조건 없을 때의 전체 근원사건 개수입니다.',
                             'exp_en': '$20 \\times 20 = 400$ total outcomes.'}]},
             {'title': '🌱 3단계 · [여사건 쪼개기 ①: 1회차 탈락] $1$회차에 $a_1 = 2$가 되어 탈락하는 경우의 수($32$가지) 직접 유도하기',
              'title_en': '🌱 Step 3 · [Complement Part 1: Round 1 Failure] Counting the $32$ outcomes where $a_1 = 2$',
              'knowledge': '조건부확률의 분모는 **$a_1 = 1$이고 $a_2 = 1$인 사건 $E$의 경우의 수 $n(E)$**입니다. 이를 직접 세는 것보다, 전체 $400$가지에서 '
                           '**탈락하는 경우($a_1 = 2$ 또는 $a_2 = 2$)**를 빼는 여사건 방법이 훨씬 쉽습니다! 먼저 **$1$회차에 $a_1 = 2$가 되는 경우(즉 '
                           '$1$회차에 $\\mathrm{A}, \\mathrm{B}$ 모두 $2$를 꺼내는 경우)**를 차근차근 세어 봅시다.<ul><li>**주머니 '
                           '$\\mathrm{A}$ ($1$이 $3$개, $2$가 $2$개)**: $1$회차에 숫자 $2$인 공을 꺼내는 방법 **$2$가지** $\\times$ '
                           '$2$회차에 남은 공 $4$개 중 아무거나 꺼내는 방법 **$4$가지** $\\implies 2 \\times 4 = 8$가지</li><li>**주머니 '
                           '$\\mathrm{B}$ ($1$이 $4$개, $2$가 $1$개)**: $1$회차에 유일한 숫자 $2$인 공을 꺼내는 방법 **$1$가지** $\\times$ '
                           '$2$회차에 남은 공 $4$개 중 아무거나 꺼내는 방법 **$4$가지** $\\implies 1 \\times 4 = 4$가지</li></ul>따라서 $1$회차에 '
                           '$a_1 = 2$가 되는 경우의 수는 두 가짓수를 곱한 $8 \\times 4$입니다!',
              'knowledge_en': "Let's count how many of the $400$ outcomes fail in Round 1 ($a_1 = 2$, meaning both A "
                              'and B draw $2$ in Round 1):<ul><li><b>Bag A (three $1$s, two $2$s)</b>: $2$ choices for '
                              "a '$2$' in Round 1 $\\times$ $4$ remaining balls for Round 2 $= 2 \\times 4 = 8$ "
                              "ways.</li><li><b>Bag B (four $1$s, one $2$)</b>: $1$ choice for the single '$2$' in "
                              'Round 1 $\\times$ $4$ remaining balls for Round 2 $= 1 \\times 4 = 4$ '
                              'ways.</li></ul>Multiplying gives $8 \\times 4$ ways where $a_1 = 2$.',
              'questions': [{'level_label': '1회차 탈락 가짓수 디딤돌 3',
                             'level_label_en': 'Round 1 Failure Count Step 3',
                             'stem': '$1$회차에 두 주머니 모두 $2$를 꺼내어 $a_1 = 2$가 되는 경우의 수(주머니 $\\mathrm{A}$의 $2 \\times 4 = '
                                     '8$가지와 주머니 $\\mathrm{B}$의 $1 \\times 4 = 4$가지의 곱 $8 \\times 4$)는?',
                             'stem_en': "Multiplying Bag A's $2 \\times 4 = 8$ ways and Bag B's $1 \\times 4 = 4$ "
                                        'ways, how many outcomes give $a_1 = 2$ in Round 1?',
                             'options': ['$16$', '$24$', '$32$', '$40$', '$48$'],
                             'answer': 3,
                             'exp': '주머니 $\\mathrm{A}$에서 $8$가지, 주머니 $\\mathrm{B}$에서 $4$가지이므로 동시에 일어나는 경우의 수는 $8 '
                                    '\\times 4 = 32$가지입니다.',
                             'exp_en': '$8 \\times 4 = 32$ outcomes.'}]},
             {'title': '🌱 4단계 · [여사건 쪼개기 ②: 2회차 탈락과 분모 확정] $a_1 = a_2 = 1$인 분모 $n(E) = 336$ 구하기',
              'title_en': '🌱 Step 4 · [Complement Part 2 & Denominator] Confirming zero overlap and finding $n(E) = '
                          '336$',
              'knowledge': '이제 **$2$회차에 $a_2 = 2$가 되어 탈락하는 경우**를 세어 봅시다.<ul><li>$1$회차와 $2$회차의 역할만 바뀐 대칭 구조이므로, $2$회차에 '
                           '$\\mathrm{A}$가 $2$를 꺼내고($2 \\times 4 = 8$가지) $\\mathrm{B}$도 $2$를 꺼내는($1 \\times 4 = 4$가지) '
                           '경우의 수 역시 똑같이 **$8 \\times 4 = 32$가지**입니다.</li><li>**핵심 체크 (중복 여부)**: 혹시 $1$회차에도 $a_1 = '
                           '2$이고 $2$회차에도 $a_2 = 2$인(두 번 모두 탈락하는) 겹치는 경우가 있을까요? **절대 없습니다($0$가지)!** 왜냐하면 주머니 '
                           '$\\mathrm{B}$에는 숫자 $2$가 적힌 공이 **딱 $1$개뿐**이고 꺼낸 공을 다시 넣지 않으므로, $\\mathrm{B}$에서 $1$회차와 '
                           '$2$회차에 연속으로 $2$를 꺼내는 것은 불가능하기 때문입니다!</li></ul>따라서 탈락하는 전체 가짓수는 $32 + 32 = 64$가지이고, 조건 $a_1 '
                           '= a_2 = 1$을 만족하는 **분모의 경우의 수 $n(E)$**는 $400 - 64$입니다!',
              'knowledge_en': 'By symmetry between Round 1 and Round 2, $a_2 = 2$ also occurs in $8 \\times 4 = 32$ '
                              'ways. Can $a_1 = 2$ and $a_2 = 2$ happen simultaneously? <b>Impossible ($0$ ways)</b>, '
                              'because Bag B contains only ONE ball labeled $2$ and draws are without replacement! '
                              'Thus the denominator is $n(E) = 400 - (32 + 32)$.',
              'questions': [{'level_label': '분모 경우의 수 확정 디딤돌 4',
                             'level_label_en': 'Denominator Count Step 4',
                             'stem': '전체 $400$가지에서 $a_1 = 2$인 $32$가지와 $a_2 = 2$인 $32$가지(중복 $0$가지)를 뺀, $a_1 = a_2 = 1$을 '
                                     '만족하는 조건부확률의 분모 $n(E) = 400 - (32 + 32)$의 값은?',
                             'stem_en': 'Subtracting the $32 + 32 = 64$ mutually exclusive failure cases from $400$, '
                                        'what is the denominator $n(E) = 400 - 64$?',
                             'options': ['$316$', '$324$', '$336$', '$344$', '$352$'],
                             'answer': 3,
                             'exp': '$400 - 64 = 336$가지가 조건부확률의 분모 $n(E)$가 됩니다.',
                             'exp_en': '$400 - 64 = 336$.'}]},
             {'title': '🌳 5단계 · [분자 사건 번역] 주머니 $\\mathrm{B}$에 숫자 $1$인 공이 $3$개 남아 있으려면 $\\mathrm{B}$에서 무엇을 꺼내야 할까?',
              'title_en': '🌳 Step 5 · [Translating the Target Event] What must Bag $\\mathrm{B}$ draw so that three '
                          '$1$s remain in $\\mathrm{B}$?',
              'knowledge': "이제 조건부확률의 **분자 $n(E \\cap F)$**, 즉 **'$a_1 = a_2 = 1$이면서 동시에 $2$번째 시행 후 주머니 $\\mathrm{B}$에 "
                           "숫자 $1$이 적힌 공이 $3$개 남아 있는 경우'**를 구할 차례입니다!<ul><li>처음에 주머니 $\\mathrm{B}$에는 **숫자 $1$이 $4$개, "
                           '숫자 $2$가 $1$개** 들어 있었습니다.</li><li>$2$번 시행 후 주머니 $\\mathrm{B}$에 **숫자 $1$이 $3$개** 남았다는 것은, '
                           '$2$번의 시행 동안 주머니 $\\mathrm{B}$에서 빠져나간 공 $2$개가 **숫자 $1$ 한 개($4 - 3 = 1$)와 숫자 $2$ 한 개**라는 '
                           '뜻입니다!</li><li>즉, 주머니 $\\mathrm{B}$가 $(1\\text{회차}, 2\\text{회차})$에 꺼낸 공의 숫자는 반드시 **케이스 ① '
                           '$\\mathrm{B}: (1, 2)$** 이거나 **케이스 ② $\\mathrm{B}: (2, 1)$** 두 가지뿐입니다!</li></ul>먼저 케이스 ①에서 '
                           '주머니 $\\mathrm{B}$가 $1$회차에 $1$($4$개 중 하나), $2$회차에 $2$($1$개 중 하나)를 꺼내는 가짓수를 구해 봅시다.',
              'knowledge_en': 'Bag B starts with four $1$s and one $2$. For three $1$s to remain in Bag B after $2$ '
                              "draws, Bag B must have lost exactly one '$1$' ($4 - 3 = 1$) and its single '$2$'. Thus "
                              "Bag B's $(1\\text{st}, 2\\text{nd})$ draws must be either <b>Case 1: $\\mathrm{B}=(1, "
                              '2)$</b> or <b>Case 2: $\\mathrm{B}=(2, 1)$</b>!',
              'questions': [{'level_label': '주머니 B 추출 가짓수 디딤돌 5',
                             'level_label_en': 'Bag B Draw Count Step 5',
                             'stem': '주머니 $\\mathrm{B}$($1$이 $4$개, $2$가 $1$개)에서 $1$회차에 숫자 $1$인 공을 꺼내고($4$가지), $2$회차에 '
                                     '숫자 $2$인 공을 꺼내는($1$가지) 케이스 ① $\\mathrm{B}: (1, 2)$의 경우의 수 $4 \\times 1$은?',
                             'stem_en': 'In Bag B (four $1$s, one $2$), how many ways can Bag B draw $1$ in Round 1 '
                                        '($4$ choices) and $2$ in Round 2 ($1$ choice)?',
                             'options': ['$2$', '$3$', '$4$', '$6$', '$8$'],
                             'answer': 3,
                             'exp': '$1$회차에 $4$개의 $1$ 중 하나를 뽑고($4$가지), $2$회차에 $1$개의 $2$를 뽑으므로($1$가지) $4 \\times 1 = '
                                    '4$가지입니다.',
                             'exp_en': '$4 \\times 1 = 4$ ways.'}]},
             {'title': '🌳 6단계 · [분자 케이스 ①: 주머니 A의 조건] $\\mathrm{B}$가 $(1, 2)$를 꺼낼 때 $a_1 = a_2 = 1$이 되도록 '
                       '$\\mathrm{A}$에서 꺼내는 가짓수($12$가지)',
              'title_en': '🌳 Step 6 · [Numerator Case 1: Condition on Bag A] Counting the $12$ ways for Bag '
                          '$\\mathrm{A}$ when $\\mathrm{B}$ draws $(1, 2)$',
              'knowledge': '케이스 ①처럼 **주머니 $\\mathrm{B}$가 $1$회차에 $1$, $2$회차에 $2$를 꺼냈을 때($\\mathrm{B}: (1, 2)$)**, $a_1 '
                           '= 1$이고 $a_2 = 1$이 되려면 주머니 $\\mathrm{A}$는 어떤 공을 꺼내야 할까요?<ul><li>**$1$회차 확인**: '
                           '$\\mathrm{B}$가 이미 $1$을 꺼냈으므로, $\\mathrm{A}$가 $1$을 꺼내든 $2$를 꺼내든 크지 않은 수 $a_1$은 무조건 $1$이 '
                           '됩니다! (즉, $1$회차에는 $\\mathrm{A}$에 제한이 없습니다.)</li><li>**$2$회차 확인**: $\\mathrm{B}$가 $2$회차에 '
                           '**$2$**를 꺼냈습니다! 만약 $\\mathrm{A}$도 $2$회차에 $2$를 꺼내면 $a_2 = 2$가 되어 탈락하므로, **주머니 '
                           '$\\mathrm{A}$는 $2$회차에 반드시 숫자 $1$을 꺼내야만 합니다!**</li></ul>그럼 주머니 $\\mathrm{A}$($1$이 $3$개, '
                           '$2$가 $2$개, 총 $5$개)에서 **$2$회차에 반드시 $1$을 꺼내는 경우의 수**를 두 가지 방법으로 세어 볼까요?<ul><li>**방법 1 ($2$회차 '
                           '먼저 고르기)**: $2$회차에 꺼낼 숫자 $1$인 공을 먼저 고르는 방법 **$3$가지** $\\times$ $1$회차에는 방금 고른 공을 제외한 나머지 '
                           '$4$개의 공 중 아무거나 꺼내는 방법 **$4$가지** $= 3 \\times 4 = 12$가지!</li><li>**방법 2 ($1$회차 숫자 나누기)**: '
                           '$\\mathrm{A}$가 $(1, 1)$을 꺼내는 경우($3 \\times 2 = 6$가지) $+$ $\\mathrm{A}$가 $(2, 1)$을 꺼내는 '
                           '경우($2 \\times 3 = 6$가지) $= 6 + 6 = 12$가지!</li></ul>',
              'knowledge_en': 'When Bag B draws $(1, 2)$: in Round 1, B already drew $1$, so $a_1 = 1$ automatically; '
                              'in Round 2, B drew $2$, so <b>Bag A MUST draw $1$ in Round 2</b> to make $a_2 = 1$! In '
                              'Bag A (three $1$s, two $2$s):<ul><li><b>Method 1</b>: Pick which of the three $1$s A '
                              'draws in Round 2 ($3$ ways) $\\times$ pick any of the remaining $4$ balls for Round 1 '
                              '($4$ ways) $= 3 \\times 4 = 12$ ways.</li><li><b>Method 2</b>: A draws $(1, 1)$ in $3 '
                              '\\times 2 = 6$ ways, or A draws $(2, 1)$ in $2 \\times 3 = 6$ ways $\\implies 6 + 6 = '
                              '12$ ways!</li></ul>',
              'questions': [{'level_label': '주머니 A 추출 가짓수 디딤돌 6',
                             'level_label_en': 'Bag A Draw Count Step 6',
                             'stem': '주머니 $\\mathrm{B}$가 $(1, 2)$를 꺼냈을 때 $a_2 = 1$이 되려면 주머니 $\\mathrm{A}$($1$이 $3$개, '
                                     '$2$가 $2$개)는 $2$회차에 반드시 $1$을 꺼내야 합니다. $2$회차에 $1$을 고르는 $3$가지와 $1$회차에 남은 $4$개 중 하나를 '
                                     '고르는 $4$가지를 곱한 주머니 $\\mathrm{A}$의 경우의 수 $3 \\times 4$는?',
                             'stem_en': 'For Bag A (three $1$s, two $2$s) to draw $1$ in Round 2 ($3$ choices) and any '
                                        'of the remaining $4$ balls in Round 1 ($4$ choices), how many ways $3 \\times '
                                        '4$ are there for Bag A?',
                             'options': ['$6$', '$8$', '$10$', '$12$', '$15$'],
                             'answer': 4,
                             'exp': '$2$회차에 $1$을 뽑는 $3$가지 각각에 대하여 $1$회차에 남은 $4$개 중 아무 공이나 뽑을 수 있으므로 $3 \\times 4 = '
                                    '12$가지입니다.',
                             'exp_en': '$3 \\times 4 = 12$ ways for Bag A.'}]},
             {'title': '🌳 7단계 · [분자 케이스 ① 결합] 주머니 $\\mathrm{B}$가 $(1, 2)$를 꺼낼 때 조건을 만족하는 전체 가짓수($48$가지)',
              'title_en': '🌳 Step 7 · [Combining Case 1] Total outcomes ($48$) when Bag $\\mathrm{B}$ draws $(1, 2)$',
              'knowledge': '5단계와 6단계에서 구한 두 조각을 레고 블록처럼 곱셈 법칙으로 결합해 봅시다!<ul><li>주머니 $\\mathrm{B}$가 $(1, 2)$ 순서로 꺼내는 '
                           '경우의 수: **$4$가지**</li><li>그 각각에 대하여 주머니 $\\mathrm{A}$가 $2$회차에 $1$을 꺼내어 $a_1 = a_2 = 1$을 만드는 '
                           '경우의 수: **$12$가지**</li></ul>따라서 케이스 ①($\\mathrm{B}$가 $(1, 2)$를 꺼내는 경우)의 전체 가짓수는 $4 \\times '
                           '12$입니다!',
              'knowledge_en': 'Combining Step 5 and Step 6 by multiplication: Bag B draws $(1, 2)$ in $4$ ways, and '
                              'Bag A satisfies $a_1 = a_2 = 1$ in $12$ ways, giving $4 \\times 12$ outcomes for Case '
                              '1.',
              'questions': [{'level_label': '케이스 ① 결합 디딤돌 7',
                             'level_label_en': 'Case 1 Product Step 7',
                             'stem': '주머니 $\\mathrm{B}$가 $(1, 2)$를 꺼내는 $4$가지와 주머니 $\\mathrm{A}$가 조건을 만족하도록 꺼내는 $12$가지를 '
                                     '곱한 케이스 ①의 경우의 수 $4 \\times 12$는?',
                             'stem_en': "Multiplying Bag B's $4$ ways and Bag A's $12$ ways, how many outcomes belong "
                                        'to Case 1?',
                             'options': ['$24$', '$36$', '$48$', '$60$', '$72$'],
                             'answer': 3,
                             'exp': '$4 \\times 12 = 48$가지입니다.',
                             'exp_en': '$4 \\times 12 = 48$ outcomes.'}]},
             {'title': '🌳 8단계 · [분자 케이스 ②와 분자 확정] 주머니 $\\mathrm{B}$가 $(2, 1)$을 꺼내는 경우까지 더해 분자 $n(E \\cap F) = 96$ 구하기',
              'title_en': '🌳 Step 8 · [Case 2 & Numerator Total] Adding Case 2 where Bag $\\mathrm{B}$ draws $(2, 1)$ '
                          'to get $n(E \\cap F) = 96$',
              'knowledge': '이제 두 번째 케이스인 **주머니 $\\mathrm{B}$가 $1$회차에 $2$, $2$회차에 $1$을 꺼내는 경우($\\mathrm{B}: (2, 1)$)**를 '
                           '봅시다!<ul><li>주머니 $\\mathrm{B}$가 $1$회차에 $2$($1$가지), $2$회차에 $1$($4$가지)을 꺼내는 가짓수: $1 \\times 4 '
                           '= 4$가지</li><li>이번에는 $\\mathrm{B}$가 $1$회차에 $2$를 꺼냈으므로, $a_1 = 1$이 되려면 **주머니 $\\mathrm{A}$가 '
                           '$1$회차에 반드시 $1$($3$가지)**을 꺼내고 $2$회차에 남은 공($4$가지)을 꺼내야 하므로: $3 \\times 4 = 12$가지</li><li>따라서 '
                           '케이스 ②($\\mathrm{B}$가 $(2, 1)$을 꺼내는 경우)의 가짓수도 정확히 대칭적으로 **$4 \\times 12 = '
                           '48$가지**입니다!</li></ul>케이스 ①($48$가지)과 케이스 ②($48$가지)를 더하면 조건부확률의 **분자 $n(E \\cap F)$**가 '
                           '완성됩니다!',
              'knowledge_en': 'In Case 2, Bag B draws $(2, 1)$ in $1 \\times 4 = 4$ ways, and since B drew $2$ in '
                              'Round 1, Bag A must draw $1$ in Round 1 ($3 \\times 4 = 12$ ways), giving another $4 '
                              '\\times 12 = 48$ ways. Adding Case 1 and Case 2 gives the numerator $n(E \\cap F) = 48 '
                              '+ 48$.',
              'questions': [{'level_label': '분자 경우의 수 확정 디딤돌 8',
                             'level_label_en': 'Numerator Total Step 8',
                             'stem': '케이스 ①($\\mathrm{B}$가 $(1, 2)$를 뽑는 $48$가지)과 케이스 ②($\\mathrm{B}$가 $(2, 1)$을 뽑는 '
                                     '$48$가지)를 합친 조건부확률의 분자 $n(E \\cap F) = 48 + 48$의 값은?',
                             'stem_en': 'Adding Case 1 ($48$ ways) and Case 2 ($48$ ways), what is the numerator $n(E '
                                        '\\cap F) = 48 + 48$?',
                             'options': ['$72$', '$84$', '$96$', '$108$', '$120$'],
                             'answer': 3,
                             'exp': '$48 + 48 = 96$가지가 조건부확률의 분자 $n(E \\cap F)$입니다.',
                             'exp_en': '$48 + 48 = 96$.'}]},
             {'title': '💎 9단계 · [조건부확률 식 세우기와 약분] $\\mathrm{P}(F \\mid E) = \\dfrac{96}{336}$을 기약분수로 약분하기',
              'title_en': '💎 Step 9 · [Conditional Probability & Reduction] Reducing $\\mathrm{P}(F \\mid E) = '
                          '\\dfrac{96}{336}$ to lowest terms',
              'knowledge': '드디어 조건부확률의 분모 $n(E) = 336$과 분자 $n(E \\cap F) = 96$을 모두 구했습니다!$$\\mathrm{P}(F \\mid E) = '
                           '\\frac{n(E \\cap F)}{n(E)} = \\frac{96}{336}$$차근차근 약분해 볼까요?<ul><li>먼저 분자와 분모를 $16$으로 나누면: '
                           '$96 \\div 16 = 6$, $336 \\div 16 = 21$이므로 $\\dfrac{6}{21}$이 됩니다.</li><li>다시 분자와 분모를 $3$으로 '
                           '나누면: $6 \\div 3 = 2$, $21 \\div 3 = 7$이므로 기약분수 **$\\dfrac{2}{7}$**이 됩니다! (즉, 최대공약수 $48$로 한 '
                           '번에 나누면 $96 = 48 \\times 2$, $336 = 48 \\times 7$입니다.)</li></ul>',
              'knowledge_en': 'Combining the numerator $96$ and denominator $336$:$$\\mathrm{P}(F \\mid E) = '
                              '\\frac{96}{336}$$Dividing by $16$ gives $\\frac{6}{21}$, and dividing by $3$ gives '
                              '$\\frac{2}{7}$ (since $96 = 48 \\times 2$ and $336 = 48 \\times 7$).',
              'questions': [{'level_label': '기약분수 약분 디딤돌 9',
                             'level_label_en': 'Lowest Terms Step 9',
                             'stem': '구하는 조건부확률 $\\dfrac{96}{336}$의 분자와 분모를 $48$로 약분하여 기약분수 $\\dfrac{q}{p}$로 나타내면?',
                             'stem_en': 'Reducing $\\dfrac{96}{336}$ by dividing numerator and denominator by $48$, '
                                        'what is the fraction $\\dfrac{q}{p}$ in lowest terms?',
                             'options': ['$\\frac{1}{4}$',
                                         '$\\frac{2}{7}$',
                                         '$\\frac{3}{8}$',
                                         '$\\frac{2}{9}$',
                                         '$\\frac{3}{11}$'],
                             'answer': 2,
                             'exp': '$\\dfrac{96 \\div 48}{336 \\div 48} = \\dfrac{2}{7}$이므로 $p = 7, q = 2$입니다.',
                             'exp_en': '$\\dfrac{96}{336} = \\dfrac{2}{7}$.'}]},
             {'title': '🏆 10단계 · [최종 정답 완성] 서로소인 자연수 $p + q$의 값 구하기',
              'title_en': '🏆 Step 10 · [Final Synthesis] Computing $p + q$',
              'knowledge': '9단계에서 구한 기약분수 $\\dfrac{q}{p} = \\dfrac{2}{7}$에서 분모 $p = 7$, 분자 $q = 2$ ($7$과 $2$는 서로소인 '
                           '자연수)입니다. 이제 두 수를 더하면 최종 정답이 완성됩니다!',
              'knowledge_en': 'From $\\dfrac{q}{p} = \\dfrac{2}{7}$ in lowest terms, $p = 7$ and $q = 2$, so $p + q = '
                              '7 + 2 = 9$.',
              'questions': [{'level_label': '최종 종합 디딤돌 10',
                             'level_label_en': 'Final Synthesis Step 10',
                             'stem': '$p = 7$, $q = 2$일 때, 문제에서 구하라는 최종 정답 $p + q$의 값은?',
                             'stem_en': 'Given $p = 7$ and $q = 2$, what is the final answer $p + q$?',
                             'options': ['$7$', '$8$', '$9$', '$10$', '$11$'],
                             'answer': 3,
                             'exp': '$p + q = 7 + 2 = 9$입니다.',
                             'exp_en': '$7 + 2 = 9$.'}]}],
  'final': {'stem': '주머니 $\\mathrm{A}$에는 숫자 $1$이 적힌 공 $3$개, 숫자 $2$가 적힌 공 $2$개가 들어 있고, 주머니 $\\mathrm{B}$에는 숫자 $1$이 적힌 공 '
                    '$4$개, 숫자 $2$가 적힌 공 $1$개가 들어 있다. 두 주머니 $\\mathrm{A}, \\mathrm{B}$에서 각각 공을 임의로 한 개씩 꺼내어 꺼낸 두 개의 공에 '
                    '적힌 수를 확인한 후 다시 넣지 않는다. 이 시행을 $2$번 반복할 때, 첫 번째 시행에서 확인한 두 수 중 크지 않은 수를 $a_1$, 두 번째 시행에서 확인한 두 수 중 '
                    '크지 않은 수를 $a_2$라 하자. $a_1 = a_2 = 1$일 때, 두 번째 시행 후 주머니 $\\mathrm{B}$에 숫자 $1$이 적힌 공 $3$개가 들어 있을 확률은 '
                    '$\\dfrac{q}{p}$이다. $p + q$의 값을 구하시오. (단, $p$와 $q$는 서로소인 자연수이다.) [4점]',
            'stem_en': 'Bag $\\mathrm{A}$ has three $1$s and two $2$s; Bag $\\mathrm{B}$ has four $1$s and one $2$. In '
                       'each of two rounds without replacement, one ball is drawn at random from each bag and $a_n$ is '
                       'the number not larger (the minimum) of the two numbers drawn in round $n$. Given $a_1 = a_2 = '
                       '1$, the probability that three $1$s remain in Bag $\\mathrm{B}$ after the second round is '
                       '$\\dfrac{q}{p}$ in lowest terms. Find $p + q$. [4 points]',
            'options': ['$7$', '$8$', '$9$', '$10$', '$11$'],
            'answer': 3,
            'exp': '전체 $(5\\times 4)\\times(5\\times 4) = 400$가지 중 $a_1=2$인 경우($(2\\times 4)\\times(1\\times '
                   '4)=32$가지)와 $a_2=2$인 경우($32$가지, 중복 $0$가지)를 제외한 분모는 $400 - 64 = 336$가지입니다. 이 중 $\\mathrm{B}$에 $1$이 '
                   '$3$개 남으려면 $\\mathrm{B}$가 $(1,2)$ 또는 $(2,1)$을 뽑아야 하며, 각 경우 $(4\\times 1)\\times(3\\times 4) = '
                   '48$가지씩 총 $96$가지이므로 확률은 $\\dfrac{96}{336} = \\dfrac{2}{7}$이고 $p+q=9$입니다.',
            'exp_en': 'Out of $20 \\times 20 = 400$ ordered outcomes, excluding $a_1=2$ ($8 \\times 4 = 32$) and '
                      '$a_2=2$ ($32$, zero overlap) leaves $336$ outcomes where $a_1=a_2=1$. Among these, leaving '
                      'three $1$s in B requires B to draw $(1,2)$ or $(2,1)$, giving $4 \\times 12 + 4 \\times 12 = '
                      '96$ outcomes. Thus $\\dfrac{96}{336} = \\dfrac{2}{7}$ and $p+q = 9$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 확률과 통계 최고난도(30번) 문항으로, <b>비복원 추출에서의 여사건을 이용한 조건부확률 $\\mathrm{P}(F \\mid E) = '
                        '\\dfrac{n(E \\cap F)}{n(E)}$</b>을 구하는 문제입니다. 같은 숫자가 적힌 공이라도 모두 구별되는 $5$개의 공으로 보고 <b>순열($5 '
                        '\\times 4 = 20$)</b>로 근원사건의 개수를 세면 분모와 분자를 매우 직관적이고 오차 없이 구할 수 있습니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 전체 근원사건의 개수 ($400$가지)</b><br>\n'
                        '  주머니 $\\mathrm{A}$($5$개)에서 비복원으로 $2$번 꺼내는 경우의 수는 $5 \\times 4 = 20$가지, 주머니 '
                        '$\\mathrm{B}$($5$개)에서 비복원으로 $2$번 꺼내는 경우의 수도 $5 \\times 4 = 20$가지이므로 전체 경우의 수는:<br>\n'
                        '  $$20 \\times 20 = 400\\text{가지}$$<br>\n'
                        '  <b>2단계: 조건 사건 $E$ ($a_1 = 1$이고 $a_2 = 1$)의 경우의 수 $n(E) = 336$</b><br>\n'
                        '  두 수 중 크지 않은 수 $a_n$이 $1$이 아닌 경우($a_n = 2$)는 $n$번째 시행에서 $\\mathrm{A}$와 $\\mathrm{B}$ 모두 숫자 '
                        '$2$를 꺼낼 때뿐입니다.<br>\n'
                        '  - <b>$a_1 = 2$인 경우 ($1$회차에 둘 다 $2$)</b>:<br>\n'
                        '    &nbsp;&nbsp;• 주머니 $\\mathrm{A}$ ($1$이 $3$개, $2$가 $2$개): $1$회차에 $2$ ($2$가지) $\\times$ '
                        '$2$회차에 남은 공 ($4$가지) $= 8$가지<br>\n'
                        '    &nbsp;&nbsp;• 주머니 $\\mathrm{B}$ ($1$이 $4$개, $2$가 $1$개): $1$회차에 $2$ ($1$가지) $\\times$ '
                        '$2$회차에 남은 공 ($4$가지) $= 4$가지<br>\n'
                        '    &nbsp;&nbsp;• 곱하면 $8 \\times 4 = 32$가지입니다.<br>\n'
                        '  - <b>$a_2 = 2$인 경우 ($2$회차에 둘 다 $2$)</b>:<br>\n'
                        '    &nbsp;&nbsp;• $1$회차와 $2$회차의 대칭성에 의해 똑같이 $8 \\times 4 = 32$가지입니다.<br>\n'
                        '  - <b>교집합 ($a_1 = 2$이고 $a_2 = 2$)</b>:<br>\n'
                        '    &nbsp;&nbsp;• 주머니 $\\mathrm{B}$에는 숫자 $2$가 적힌 공이 단 $1$개뿐이므로 $1, 2$회차 연속으로 $2$를 뽑을 수 없어 '
                        '$0$가지입니다.<br>\n'
                        '  따라서 여사건에 의해 분모의 경우의 수는:<br>\n'
                        '  $$n(E) = 400 - (32 + 32) = 336\\text{가지}$$<br>\n'
                        '  <b>3단계: 교집합 사건 $E \\cap F$ ($\\mathrm{B}$에 $1$이 $3$개 남고 $a_1 = a_2 = 1$)의 경우의 수 $n(E \\cap '
                        'F) = 96$</b><br>\n'
                        '  처음에 $\\mathrm{B}$에는 $1$이 $4$개, $2$가 $1$개 있으므로, $2$번 시행 후 $\\mathrm{B}$에 $1$이 $3$개 남으려면 '
                        '$\\mathrm{B}$에서 꺼낸 두 공이 <b>$1$ 한 개와 $2$ 한 개</b>여야 합니다.<br>\n'
                        '  - <b>(케이스 ①) $\\mathrm{B}$가 $1$회차에 $1$, $2$회차에 $2$를 꺼내는 경우</b>:<br>\n'
                        '    &nbsp;&nbsp;• 주머니 $\\mathrm{B}$의 가짓수: $4 \\times 1 = 4$가지<br>\n'
                        '    &nbsp;&nbsp;• 주머니 $\\mathrm{A}$의 조건: $1$회차에는 $\\mathrm{B}$가 이미 $1$을 뽑았으므로 $a_1 = 1$이 자동 '
                        '성립하고, $2$회차에는 $\\mathrm{B}$가 $2$를 뽑았으므로 $a_2 = 1$이 되려면 <b>$\\mathrm{A}$가 $2$회차에 반드시 $1$을 뽑아야 '
                        '합니다.</b><br>\n'
                        '    &nbsp;&nbsp;• 주머니 $\\mathrm{A}$의 가짓수: $2$회차에 $1$을 먼저 고르는 방법($3$가지) $\\times$ $1$회차에 남은 '
                        '$4$개 중 하나를 고르는 방법($4$가지) $= 3 \\times 4 = 12$가지<br>\n'
                        '    &nbsp;&nbsp;• 따라서 케이스 ①의 가짓수는 $4 \\times 12 = 48$가지입니다.<br>\n'
                        '  - <b>(케이스 ②) $\\mathrm{B}$가 $1$회차에 $2$, $2$회차에 $1$을 꺼내는 경우</b>:<br>\n'
                        '    &nbsp;&nbsp;• 주머니 $\\mathrm{B}$의 가짓수: $1 \\times 4 = 4$가지<br>\n'
                        '    &nbsp;&nbsp;• 주머니 $\\mathrm{A}$의 가짓수: 이번에는 $\\mathrm{A}$가 $1$회차에 반드시 $1$($3$가지)을 뽑고 '
                        '$2$회차에 남은 공($4$가지)을 뽑아야 하므로 $3 \\times 4 = 12$가지<br>\n'
                        '    &nbsp;&nbsp;• 따라서 케이스 ②의 가짓수도 $4 \\times 12 = 48$가지입니다.<br>\n'
                        '  그러므로 분자의 경우의 수는:<br>\n'
                        '  $$n(E \\cap F) = 48 + 48 = 96\\text{가지}$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  구하는 조건부확률은:<br>\n'
                        '  $$\\mathrm{P}(F \\mid E) = \\frac{n(E \\cap F)}{n(E)} = \\frac{96}{336} = \\frac{48 \\times '
                        '2}{48 \\times 7} = \\frac{2}{7}$$\n'
                        '  따라서 $p = 7, q = 2$이므로 $p + q = 7 + 2 =$ <b>$9$</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem is the #30 killer question in Probability & Statistics, asking for the '
                           '<b>conditional probability $\\mathrm{P}(F \\mid E) = \\dfrac{n(E \\cap F)}{n(E)}$ under '
                           'sampling without replacement</b>. Treating all $5$ balls in each bag as distinct makes '
                           'every ordered pair of draws equally likely.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Total outcomes and Denominator $n(E)$ ($a_1 = 1$ and $a_2 = 1$)</b><br>\n'
                           '  Total ordered outcomes across both bags: $(5 \\times 4) \\times (5 \\times 4) = '
                           '400$.<br>\n'
                           '  Since $a_n = 2$ occurs iff both bags draw $2$ in round $n$:<br>\n'
                           '  - $a_1 = 2$: Bag A draws $2$ first ($2 \\times 4 = 8$ ways) and Bag B draws $2$ first '
                           '($1 \\times 4 = 4$ ways) $\\implies 8 \\times 4 = 32$ ways.<br>\n'
                           '  - $a_2 = 2$: By symmetry, $8 \\times 4 = 32$ ways.<br>\n'
                           "  - $a_1 = 2$ and $a_2 = 2$: Impossible ($0$ ways) because Bag B has only one '$2$'.<br>\n"
                           '  Thus $n(E) = 400 - (32 + 32) = 336$.<br><br>\n'
                           '  <b>Step 2: Numerator $n(E \\cap F)$ (Three $1$s remain in B and $a_1 = a_2 = '
                           '1$)</b><br>\n'
                           "  For three $1$s to remain in B (out of four $1$s and one $2$), B must draw one '$1$' and "
                           "one '$2$':<br>\n"
                           '  - <b>Case 1: B draws $(1, 2)$</b> ($4 \\times 1 = 4$ ways). Then A must draw $1$ in '
                           'Round 2 ($3$ choices for Round 2 $\\times$ $4$ remaining balls for Round 1 $= 12$ ways) '
                           '$\\implies 4 \\times 12 = 48$ ways.<br>\n'
                           '  - <b>Case 2: B draws $(2, 1)$</b> ($1 \\times 4 = 4$ ways). Then A must draw $1$ in '
                           'Round 1 ($3 \\times 4 = 12$ ways) $\\implies 4 \\times 12 = 48$ ways.<br>\n'
                           '  Thus $n(E \\cap F) = 48 + 48 = 96$.\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  $$\\mathrm{P}(F \\mid E) = \\frac{96}{336} = \\frac{2}{7} \\implies p = 7,\\ q = 2 '
                           '\\implies p + q = \\mathbf{9}$$\n'
                           '</p>'}}]
