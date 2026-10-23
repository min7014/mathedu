# -*- coding: utf-8 -*-

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
  'summary_ko': '표준화 변수 $Z_1=\\dfrac{X-m_1}{10},\\ Z_2=\\dfrac{Y-m_2}{10} \\sim \\mathrm{N}(0,1)$을 설정하고, 조건 (가) '
                '$f(x)\\le f(4)$에서 대칭축 $m_1=4$를 찾은 뒤, 좌변을 표준화·대칭 결합하여 $\\mathrm{P}(-0.3\\le Z\\le '
                '-0.2)+\\mathrm{P}(0.3\\le Z\\le 0.5)=(\\cancel{0.118}-0.079)+(0.191-\\cancel{0.118})=0.112$를 구하고, 조건 '
                '(나) $f(5)=g(15)$의 두 대칭 케이스 $\\text{Case 1}(m_2=16)$과 $\\text{Case 2}(m_2=14)$ 중 $\\mathrm{P}(11\\le '
                'Y\\le 14)=0.112$를 만족하는 $m_2=16$을 확정하여 $\\mathrm{P}(Y\\ge 20)=\\mathrm{P}(Z\\ge 0.4)=0.5-0.155=0.345 '
                '\\implies 1000k=345$ 도출하기',
  'summary_en': 'Set $Z_1=\\dfrac{X-m_1}{10},\\ Z_2=\\dfrac{Y-m_2}{10} \\sim \\mathrm{N}(0,1)$. From (가) $f(x)\\le '
                'f(4)$, find the symmetry axis $m_1=4$. Standardize and geometrically merge the left-hand side into '
                '$\\mathrm{P}(-0.3\\le Z\\le -0.2)+\\mathrm{P}(0.3\\le Z\\le '
                '0.5)=(\\cancel{0.118}-0.079)+(0.191-\\cancel{0.118})=0.112$. Test the two symmetric cases of '
                '$f(5)=g(15)$ ($\\text{Case 1}: m_2=16$ vs. $\\text{Case 2}: m_2=14$) against $\\mathrm{P}(11\\le '
                'Y\\le 14)=0.112$ to confirm $m_2=16$, yielding $\\mathrm{P}(Y\\ge 20)=\\mathrm{P}(Z\\ge '
                '0.4)=0.5-0.155=0.345$ and $1000k=345$.',
  'tags': ['확률과 통계', '통계', '정규분포', '확률밀도함수', '대칭성', '표준화', '단답형', '29번'],
  'symbols': [{'sym': '$Z_1 = \\dfrac{X - m_1}{10} \\sim \\mathrm{N}(0,1),\\quad Z_2 = \\dfrac{Y - m_2}{10} \\sim '
                      '\\mathrm{N}(0,1)$',
               'desc': '표준편차가 $\\sigma=10$으로 같은 두 정규분포 $X, Y$는 종 모양 곡선 $f(x), g(x)$가 완전히 합동(평행이동 관계)이며, 평균을 빼고 $10$으로 '
                       '나누면 표준정규분포 $\\mathrm{N}(0,1)$로 통일됨',
               'desc_en': 'Since both $X$ and $Y$ have $\\sigma=10$, their bell curves $f(x)$ and $g(x)$ are congruent '
                          'translations and standardize to $Z_1, Z_2 \\sim \\mathrm{N}(0,1)$.'},
              {'sym': '$f(x) \\le f(4) \\implies m_1 = 4 \\quad \\& \\quad f(5) = g(15) \\implies m_2 = 16 \\text{ 또는 '
                      '} 14$',
               'desc': '곡선 $f$의 가장 높은 산봉우리(대칭축)는 $m_1=4$이고, $x=5$(대칭축에서 거리 $1$)와 높이가 같은 곡선 $g$ 위의 점 $15$는 대칭축 $m_2$의 '
                       '왼쪽($\\text{Case 1}: m_2=16$) 또는 오른쪽($\\text{Case 2}: m_2=14$)에 위치함',
               'desc_en': 'The peak of $f$ is at $m_1=4$. On congruent curve $g$, $g(15)=f(5)$ places $15$ either $1$ '
                          'unit left of $m_2$ ($\\text{Case 1}: m_2=16$) or $1$ unit right of $m_2$ ($\\text{Case 2}: '
                          'm_2=14$).'},
              {'sym': '$\\mathrm{P}(-0.3 \\le Z \\le -0.2) + \\mathrm{P}(0.3 \\le Z \\le 0.5) = \\cancel{0.118} - '
                      '0.079 + 0.191 - \\cancel{0.118} = 0.112$',
               'desc': '기하학적으로 왼쪽 조각 $[-0.3, -0.2]$를 $Z=0$에 대칭이동한 $[0.2, 0.3]$이 $[0.3, 0.5]$와 경계 $Z=0.3$($0.118$)에서 '
                       '맞물려 이어붙여지므로 $0.118$이 상쇄되고 연속 구간 $[0.2, 0.5]$의 넓이 $0.112$가 됨',
               'desc_en': 'Geometrically reflecting $[-0.3, -0.2]$ to $[0.2, 0.3]$ joins $[0.3, 0.5]$ at $Z=0.3$, '
                          'canceling $0.118$ and forming $[0.2, 0.5]$ of area $0.191 - 0.079 = 0.112$.'},
              {'sym': '$\\text{Case 1 }(m_2=16): 0.112\\text{ (O.K.)} \\quad \\text{vs} \\quad \\text{Case 2 '
                      '}(m_2=14): 0.118\\text{ (}\\times\\text{)}$',
               'desc': '$\\mathrm{P}(11\\le Y\\le 14)$를 표준화할 때 $m_2=16$이면 $\\mathrm{P}(-0.5\\le Z\\le '
                       '-0.2)=0.191-0.079=0.112$로 좌변과 합동이지만, $m_2=14$이면 $\\mathrm{P}(-0.3\\le Z\\le 0)=0.118$이 되어 모순!',
               'desc_en': 'Standardizing $\\mathrm{P}(11\\le Y\\le 14)$ gives $\\mathrm{P}(-0.5\\le Z\\le -0.2)=0.112$ '
                          'for $\\text{Case 1 }(m_2=16)$ (valid) vs. $\\mathrm{P}(-0.3\\le Z\\le 0)=0.118$ for '
                          '$\\text{Case 2 }(m_2=14)$ (invalid).'}],
  'levels': [{'title': '🔰 1단계 · [초등 산봉우리 꼭대기 찾기] 조건 (가) $f(x) \\le f(4)$에서 곡선 $f$의 대칭축(평균) $m_1$ 구하기',
              'title_en': '🔰 Step 1 · [Elementary Peak Finding] Finding the symmetry axis (mean) $m_1$ from $f(x) \\le '
                          'f(4)$',
              'knowledge': '초등학교 그래프 읽기처럼 정규분포 $X \\sim \\mathrm{N}(m_1, 10^2)$의 확률밀도함수 $y = f(x)$는 <b>대칭축인 평균 $x = '
                           'm_1$에서 가장 높은 산봉우리 꼭대기(최댓값)</b>를 가지는 좌우 대칭 종 모양 곡선입니다! 조건 (가)에서 '
                           '$\\underline{\\underline{f(x) \\le f(4)}}$라는 뜻은 모든 실수 $x$ 중에서 $x = 4$일 때 곡선의 높이가 가장 높다는 '
                           '뜻이므로, 곡선 $f$의 대칭축(평균)은 <b>$m_1 = 4$</b>이고 표준화 변수는 $Z_1 = \\dfrac{X - 4}{10} \\sim '
                           '\\mathrm{N}(0, 1)$이 됩니다.',
              'knowledge_en': 'Like finding the highest peak of a hill in elementary math, the normal density curve $y '
                              '= f(x)$ of $X \\sim \\mathrm{N}(m_1, 10^2)$ is symmetric and reaches its unique maximum '
                              'at the mean $x = m_1$. Condition (가) $f(x) \\le f(4)$ means the peak is at $x = 4$, so '
                              '$m_1 = 4$ and $Z_1 = \\dfrac{X - 4}{10} \\sim \\mathrm{N}(0, 1)$.',
              'questions': [{'level_label': '초등 산봉우리 대칭축 디딤돌 1',
                             'level_label_en': 'Bell Curve Peak Step 1',
                             'stem': '종 모양 곡선 $y = f(x)$에서 가장 높은 곳을 찾듯이, 모든 실수 $x$에 대하여 $f(x) \\le f(4)$일 때 정규분포 '
                                     '$\\mathrm{N}(m_1, 10^2)$의 대칭축(평균) $m_1$의 값은?',
                             'stem_en': 'Since $f(x) \\le f(4)$ for all real $x$, what is the symmetry axis (mean) '
                                        '$m_1$ of $X \\sim \\mathrm{N}(m_1, 10^2)$?',
                             'options': ['$2$', '$3$', '$4$', '$5$', '$6$'],
                             'answer': 3,
                             'exp': '<b>[1단계 기하학적 해설]</b><br>정규분포 확률밀도함수 $f(x)$는 대칭축 $x = m_1$에서 최댓값을 가집니다. 모든 실수 $x$에 '
                                    '대하여 $f(x) \\le f(4)$이므로 산봉우리 꼭대기(대칭축)는 $m_1 = 4$입니다.',
                             'exp_en': '<b>[Step 1 Geometric Explanation]</b><br>A normal density curve $f(x)$ attains '
                                       'its global maximum at its symmetry axis $x = m_1$. Thus $f(x) \\le f(4)$ '
                                       'implies $m_1 = 4$.'}]},
             {'title': '🌿 2단계 · [두 종 모양 곡선 $f, g$의 합동과 대칭점] 조건 (나) $f(5) = g(15)$에서 $\\text{Case 1}, \\text{Case 2}$ '
                       '나누기',
              'title_en': '🌿 Step 2 · [Congruent Bell Curves $f, g$ & Symmetric Points] Splitting $f(5) = g(15)$ into '
                          'Case 1 and Case 2',
              'knowledge': '두 확률변수 $X \\sim \\mathrm{N}(4, 10^2)$과 $Y \\sim \\mathrm{N}(m_2, 10^2)$는 <b>표준편차가 $\\sigma '
                           '= 10$으로 똑같기 때문에</b> 두 종 모양 곡선 $y = f(x)$와 $y = g(x)$는 평행이동하면 완전히 포개어지는 <b>합동 '
                           '도형</b>입니다!<ul><li>왼쪽 곡선 $f$: 대칭축 $m_1 = 4$에서 오른쪽으로 $1$칸 떨어진 $x = 5$($5 - 4 = 1$)에서의 높이가 '
                           '$f(5)$입니다.</li><li>오른쪽 곡선 $g$: 모양이 똑같은 곡선 $g$에서 높이가 $f(5)$와 같아지는 지점($g(15) = f(5)$)은 대칭축 '
                           '$m_2$로부터 <b>거리가 $1$만큼 떨어진 왼쪽 비탈면과 오른쪽 비탈면 두 곳</b>에 대칭으로 존재합니다!</li><li><b>$\\text{Case 1}$ '
                           '($15$가 대칭축 $m_2$의 왼쪽에 있는 경우)</b>: $15$가 $m_2$보다 $1$칸 작으므로 $m_2 - 1 = 15 \\implies '
                           '\\underline{m_2 = 16}$</li><li><b>$\\text{Case 2}$ ($15$가 대칭축 $m_2$의 오른쪽에 있는 경우)</b>: '
                           '$15$가 $m_2$보다 $1$칸 크므로 $m_2 + 1 = 15 \\implies \\underline{m_2 = 14}$</li></ul>',
              'knowledge_en': 'Because $X$ and $Y$ have the same standard deviation $\\sigma = 10$, the bell curves '
                              '$f(x)$ and $g(x)$ are congruent. On curve $f$, $x = 5$ lies at distance $1$ from the '
                              'peak $m_1 = 4$. On curve $g$, a point at height $g(15) = f(5)$ must also lie at '
                              'distance $1$ from the peak $m_2$: either $15$ is $1$ unit to the left of $m_2$ '
                              '(<b>$\\text{Case 1}: m_2 = 16$</b>) or $1$ unit to the right of $m_2$ (<b>$\\text{Case '
                              '2}: m_2 = 14$</b>).',
              'questions': [{'level_label': '두 곡선 합동과 대칭점 디딤돌 2',
                             'level_label_en': 'Congruent Curves & Cases Step 2',
                             'stem': '합동인 두 종 모양 곡선 $f, g$에서 $f(5) = g(15)$일 때, 점 $15$가 곡선 $g$의 대칭축 $m_2$의 왼쪽 $1$칸에 '
                                     '놓이는 경우($\\text{Case 1}$)와 오른쪽 $1$칸에 놓이는 경우($\\text{Case 2}$)의 평균 $m_2$의 값을 순서대로 '
                                     '짝지은 것은?',
                             'stem_en': 'When $f(5) = g(15)$ on congruent bell curves $f$ and $g$, what are the values '
                                        'of $m_2$ in Case 1 ($15$ is $1$ unit left of $m_2$) and Case 2 ($15$ is $1$ '
                                        'unit right of $m_2$)?',
                             'options': ['$\\text{Case 1}: m_2 = 15,\\ \\ \\text{Case 2}: m_2 = 13$',
                                         '$\\text{Case 1}: m_2 = 14,\\ \\ \\text{Case 2}: m_2 = 16$',
                                         '$\\text{Case 1}: m_2 = 16,\\ \\ \\text{Case 2}: m_2 = 14$',
                                         '$\\text{Case 1}: m_2 = 17,\\ \\ \\text{Case 2}: m_2 = 13$',
                                         '$\\text{Case 1}: m_2 = 16,\\ \\ \\text{Case 2}: m_2 = 15$'],
                             'answer': 3,
                             'exp': '<b>[2단계 기하학적 해설]</b><br>곡선 $f$에서 $x = 5$는 대칭축 $m_1 = 4$에서 거리가 $1$인 점입니다. 곡선 $g$에서 '
                                    '$15$가 대칭축 $m_2$의 왼쪽 $1$칸에 있으면 $m_2 = 15 + 1 = 16$($\\text{Case 1}$)이고, 오른쪽 $1$칸에 '
                                    '있으면 $m_2 = 15 - 1 = 14$($\\text{Case 2}$)입니다.',
                             'exp_en': '<b>[Step 2 Geometric Explanation]</b><br>If $15$ lies $1$ unit to the left of '
                                       '$m_2$, then $m_2 = 15 + 1 = 16$ (Case 1). If $15$ lies $1$ unit to the right '
                                       'of $m_2$, then $m_2 = 15 - 1 = 14$ (Case 2).'}]},
             {'title': '🌱 3단계 · [좌변의 표준화 변환] $Z_1 = \\dfrac{X - 4}{10}$으로 $\\mathrm{P}(1 \\le X \\le 2) + '
                       '\\mathrm{P}(7 \\le X \\le 9)$ 변환하기',
              'title_en': '🌱 Step 3 · [Standardizing the LHS] Converting $\\mathrm{P}(1 \\le X \\le 2) + \\mathrm{P}(7 '
                          '\\le X \\le 9)$ via $Z_1 = \\dfrac{X - 4}{10}$',
              'knowledge': '$X \\sim \\mathrm{N}(4, 10^2)$이므로 표준화 공식 <b>$Z_1 = \\dfrac{X - 4}{10} \\sim \\mathrm{N}(0, '
                           '1)$</b>에 좌변의 양 끝점을 대입해 봅시다!<ul><li>첫째 구간 $1 \\le X \\le 2$: $\\dfrac{1 - 4}{10} \\le Z '
                           '\\le \\dfrac{2 - 4}{10} \\implies \\dfrac{-3}{10} \\le Z \\le \\dfrac{-2}{10} \\implies '
                           '\\mathbf{-0.3 \\le Z \\le -0.2}$</li><li>둘째 구간 $7 \\le X \\le 9$: $\\dfrac{7 - 4}{10} \\le '
                           'Z \\le \\dfrac{9 - 4}{10} \\implies \\dfrac{3}{10} \\le Z \\le \\dfrac{5}{10} \\implies '
                           '\\mathbf{0.3 \\le Z \\le 0.5}$</li></ul>기하학적으로 $Z$의 부호 $(-)$는 대칭축 왼쪽, $(+)$는 대칭축 오른쪽을 뜻하며, '
                           '숫자는 표준편차($10$) 단위로 잰 상대적 거리입니다!',
              'knowledge_en': 'Using $Z_1 = \\dfrac{X - 4}{10} \\sim \\mathrm{N}(0, 1)$:<ul><li>$1 \\le X \\le 2 '
                              '\\implies \\dfrac{-3}{10} \\le Z \\le \\dfrac{-2}{10} \\iff -0.3 \\le Z \\le '
                              '-0.2$</li><li>$7 \\le X \\le 9 \\implies \\dfrac{3}{10} \\le Z \\le \\dfrac{5}{10} '
                              '\\iff 0.3 \\le Z \\le 0.5$</li></ul>',
              'questions': [{'level_label': '좌변 표준화 변환 디딤돌 3',
                             'level_label_en': 'LHS Standardization Step 3',
                             'stem': '$X \\sim \\mathrm{N}(4, 10^2)$에서 $Z = \\dfrac{X - 4}{10}$을 이용하여 좌변 '
                                     '$\\mathrm{P}(1 \\le X \\le 2) + \\mathrm{P}(7 \\le X \\le 9)$를 표준정규분포 $Z$로 올바르게 '
                                     '나타낸 것은?',
                             'stem_en': 'Using $Z = \\dfrac{X - 4}{10}$ for $X \\sim \\mathrm{N}(4, 10^2)$, how is '
                                        '$\\mathrm{P}(1 \\le X \\le 2) + \\mathrm{P}(7 \\le X \\le 9)$ expressed in '
                                        'terms of $Z$?',
                             'options': ['$\\mathrm{P}(-0.2 \\le Z \\le -0.1) + \\mathrm{P}(0.2 \\le Z \\le 0.4)$',
                                         '$\\mathrm{P}(-0.3 \\le Z \\le -0.1) + \\mathrm{P}(0.3 \\le Z \\le 0.4)$',
                                         '$\\mathrm{P}(-0.3 \\le Z \\le -0.2) + \\mathrm{P}(0.3 \\le Z \\le 0.5)$',
                                         '$\\mathrm{P}(-0.4 \\le Z \\le -0.2) + \\mathrm{P}(0.4 \\le Z \\le 0.6)$',
                                         '$\\mathrm{P}(-0.5 \\le Z \\le -0.3) + \\mathrm{P}(0.2 \\le Z \\le 0.5)$'],
                             'answer': 3,
                             'exp': '<b>[3단계 상세 해설]</b><br>$\\mathrm{P}\\left(\\dfrac{-3}{10} \\le Z \\le '
                                    '\\dfrac{-2}{10}\\right) + \\mathrm{P}\\left(\\dfrac{3}{10} \\le Z \\le '
                                    '\\dfrac{5}{10}\\right) = \\mathrm{P}(-0.3 \\le Z \\le -0.2) + \\mathrm{P}(0.3 '
                                    '\\le Z \\le 0.5)$입니다.',
                             'exp_en': '<b>[Step 3 Detailed Explanation]</b><br>$\\mathrm{P}\\left(\\dfrac{-3}{10} '
                                       '\\le Z \\le \\dfrac{-2}{10}\\right) + \\mathrm{P}\\left(\\dfrac{3}{10} \\le Z '
                                       '\\le \\dfrac{5}{10}\\right) = \\mathrm{P}(-0.3 \\le Z \\le -0.2) + '
                                       '\\mathrm{P}(0.3 \\le Z \\le 0.5)$.'}]},
             {'title': '🌱 4단계 · [기하적 대칭 이어붙이기와 $\\cancel{0.118}$ 상쇄] 좌변의 확률 합 $0.112$ 구하기',
              'title_en': '🌱 Step 4 · [Geometric Interval Merging & Cancellation of $0.118$] Evaluating the LHS '
                          'Probability $0.112$',
              'knowledge': '칠판 판서의 핵심 계산과 그 속에 담긴 <b>기하학적 의미</b>를 함께 확인해 봅시다!<ul><li><b>칠판 표준정규분포표 대입 계산</b>:<br>표에서 '
                           '$z=0.2 \\to 0.079$, $z=0.3 \\to 0.118$, $z=0.5 \\to 0.191$이므로<br>$$\\mathrm{P}(-0.3 \\le Z '
                           '\\le -0.2) + \\mathrm{P}(0.3 \\le Z \\le 0.5) = (\\cancel{0.118} - 0.079) + (0.191 - '
                           '\\cancel{0.118}) = 0.191 - 0.079 = \\mathbf{0.112}$$</li><li><b>🎨 [기하학적 설명] 왜 $0.118$이 '
                           '감쪽같이 지워질까?</b><br>대칭축 $Z = 0$($X = 4$)을 거울 삼아 왼쪽 조각 $[-0.3, -0.2]$($X \\in [1, 2]$)를 오른쪽으로 '
                           '접어 옮기면 <b>$[0.2, 0.3]$($X \\in [6, 7]$)</b>이 됩니다. 이 조각을 원래 오른쪽에 있던 <b>$[0.3, 0.5]$($X \\in '
                           '[7, 9]$)</b>와 합치면, 정확히 <b>경계선 $Z = 0.3$($X = 7$, 넓이 $0.118$)에서 빈틈없이 맞물려 하나의 연속된 구간 $[0.2, '
                           '0.5]$($X \\in [6, 9]$)</b>로 이어붙여지기 때문에 경계값 $0.118$이 $+0.118$과 $-0.118$로 상쇄되는 '
                           '것입니다!</li></ul>',
              'knowledge_en': 'From the table ($z=0.2 \\to 0.079,\\ z=0.3 \\to 0.118,\\ z=0.5 \\to 0.191$): '
                              '$\\mathrm{P}(-0.3 \\le Z \\le -0.2) + \\mathrm{P}(0.3 \\le Z \\le 0.5) = '
                              '(\\cancel{0.118} - 0.079) + (0.191 - \\cancel{0.118}) = 0.191 - 0.079 = 0.112$. '
                              'Geometrically, reflecting $[-0.3, -0.2]$ across $Z=0$ gives $[0.2, 0.3]$, which joins '
                              '$[0.3, 0.5]$ seamlessly at the shared boundary $Z = 0.3$ ($0.118$), forming the single '
                              'interval $[0.2, 0.5]$.',
              'questions': [{'level_label': '0.118 상쇄와 넓이 합 디딤돌 4',
                             'level_label_en': 'Cancellation & Area Sum Step 4',
                             'stem': '표준정규분포표에서 $\\mathrm{P}(-0.3 \\le Z \\le -0.2) + \\mathrm{P}(0.3 \\le Z \\le 0.5) '
                                     '= (\\cancel{0.118} - 0.079) + (0.191 - \\cancel{0.118})$을 계산한 좌변의 확률 값은?',
                             'stem_en': 'What is the value of $\\mathrm{P}(-0.3 \\le Z \\le -0.2) + \\mathrm{P}(0.3 '
                                        '\\le Z \\le 0.5) = (\\cancel{0.118} - 0.079) + (0.191 - \\cancel{0.118})$?',
                             'options': ['$0.102$', '$0.112$', '$0.118$', '$0.122$', '$0.155$'],
                             'answer': 2,
                             'exp': '<b>[4단계 기하·대수 해설]</b><br>$0.118$이 $+0.118$과 $-0.118$로 서로 소거되어 $0.191 - 0.079 = '
                                    '0.112$가 됩니다. 기하학적으로도 구간 $[0.2, 0.3]$과 $[0.3, 0.5]$가 경계 $Z = 0.3$에서 합쳐져 $[0.2, '
                                    '0.5]$ 하나의 구간 넓이가 된 것입니다.',
                             'exp_en': '<b>[Step 4 Geometric & Algebraic Explanation]</b><br>The boundary value '
                                       '$0.118$ cancels out, leaving $0.191 - 0.079 = 0.112$, which is the area over '
                                       'the merged interval $[0.2, 0.5]$.'}]},
             {'title': '🌳 5단계 · [$\\text{Case 1}(m_2=16)$ vs $\\text{Case 2}(m_2=14)$ 검증] $\\mathrm{P}(11 \\le Y \\le '
                       '14) = 0.112$를 만족하는 $m_2$ 확정하기',
              'title_en': '🌳 Step 5 · [Testing Case 1 ($m_2=16$) vs Case 2 ($m_2=14$)] Confirming $m_2$ via '
                          '$\\mathrm{P}(11 \\le Y \\le 14) = 0.112$',
              'knowledge': '4단계에서 좌변의 확률이 $0.112$이므로, 우변 $\\mathrm{P}(11 \\le Y \\le 14)$도 <b>$0.112$</b>가 되어야 합니다! 칠판 '
                           '중앙의 두 케이스를 각각 $Z_2 = \\dfrac{Y - m_2}{10}$으로 표준화하여 검증해 봅시다:<ul><li><b>[$\\text{Case 1}$: '
                           '$\\underline{m_2 = 16}$일 때]</b><br>$$\\mathrm{P}(11 \\le Y \\le 14) = '
                           '\\mathrm{P}\\left(\\frac{-5}{10} \\le Z \\le \\frac{-2}{10}\\right) = \\mathrm{P}(-0.5 '
                           '\\le Z \\le -0.2) = 0.191 - 0.079 = \\underline{\\underline{0.112}} \\quad '
                           '(\\mathbf{\\text{O.K.! 성립}})$$&nbsp;&nbsp;👉 <b>기하학적 이유</b>: 구간 $[11, 14]$는 평균 $16$으로부터 '
                           '왼쪽으로 $2\\sim 5$칸 떨어진 구간($Z \\in [-0.5, -0.2]$)이므로, 좌변의 합쳐진 구간 $[6, 9]$($Z \\in [0.2, '
                           '0.5]$, 오른쪽 $2\\sim 5$칸)와 <b>완벽한 거울 대칭(합동)</b>이 되어 넓이가 $0.112$로 '
                           '일치합니다!</li><li><b>[$\\text{Case 2}$: $\\underline{m_2 = 14}$일 때]</b><br>$$\\mathrm{P}(11 '
                           '\\le Y \\le 14) = \\mathrm{P}\\left(\\frac{-3}{10} \\le Z \\le \\frac{0}{10}\\right) = '
                           '\\mathrm{P}(-0.3 \\le Z \\le 0) = 0.118 \\ne 0.112 \\quad (\\mathbf{\\times \\text{ '
                           '탈락!}})$$&nbsp;&nbsp;👉 <b>기하학적 이유</b>: 끝점 $14$가 산봉우리 꼭대기($m_2 = 14, Z = 0$)에 걸치면서 평균으로부터 왼쪽 '
                           '$0\\sim 3$칸인 봉우리 중심부 영역이 되어 넓이가 $0.118$로 달라집니다.</li></ul>',
              'knowledge_en': 'We test both candidates for $\\mathrm{P}(11 \\le Y \\le 14) = 0.112$ using $Z_2 = '
                              '\\dfrac{Y - m_2}{10}$:<ul><li><b>$\\text{Case 1}$ ($m_2 = 16$)</b>: '
                              '$\\mathrm{P}\\left(\\dfrac{-5}{10} \\le Z \\le \\dfrac{-2}{10}\\right) = '
                              '\\mathrm{P}(-0.5 \\le Z \\le -0.2) = 0.191 - 0.079 = 0.112$ (<b>O.K.!</b> Mirrors '
                              '$[0.2, 0.5]$ across $Z=0$).</li><li><b>$\\text{Case 2}$ ($m_2 = 14$)</b>: '
                              '$\\mathrm{P}\\left(\\dfrac{-3}{10} \\le Z \\le \\dfrac{0}{10}\\right) = '
                              '\\mathrm{P}(-0.3 \\le Z \\le 0) = 0.118 \\ne 0.112$ (<b>Invalid!</b> Touches the peak '
                              '$Z=0$).</li></ul>',
              'questions': [{'level_label': 'Case 1 · Case 2 검증 디딤돌 5',
                             'level_label_en': 'Case 1 vs Case 2 Verification Step 5',
                             'stem': '$\\text{Case 1}(m_2 = 16)$과 $\\text{Case 2}(m_2 = 14)$에 대하여 $\\mathrm{P}(11 \\le '
                                     'Y \\le 14)$를 표준화하여 계산한 결과와 올바른 $m_2$의 값을 고르면?',
                             'stem_en': 'Which option correctly states $\\mathrm{P}(11 \\le Y \\le 14)$ for Case 1 '
                                        '($m_2 = 16$) and Case 2 ($m_2 = 14$) and identifies the valid $m_2$?',
                             'options': ['$\\text{Case 1}: 0.118,\\ \\ \\text{Case 2}: 0.112 \\implies m_2 = 14$',
                                         '$\\text{Case 1}: 0.155,\\ \\ \\text{Case 2}: 0.118 \\implies m_2 = 14$',
                                         '$\\text{Case 1}: 0.112,\\ \\ \\text{Case 2}: 0.155 \\implies m_2 = 16$',
                                         '$\\text{Case 1}: 0.112,\\ \\ \\text{Case 2}: 0.118 \\implies m_2 = 16$',
                                         '$\\text{Case 1}: 0.191,\\ \\ \\text{Case 2}: 0.079 \\implies m_2 = 16$'],
                             'answer': 4,
                             'exp': '<b>[5단계 상세 해설]</b><br>$\\text{Case 1}(m_2 = 16)$일 때 $\\mathrm{P}(-0.5 \\le Z \\le '
                                    '-0.2) = 0.191 - 0.079 = 0.112$가 되어 좌변($0.112$)과 일치하므로 $m_2 = 16$이 확정됩니다! '
                                    '($\\text{Case 2}: m_2 = 14$일 때는 $\\mathrm{P}(-0.3 \\le Z \\le 0) = 0.118$로 '
                                    '모순입니다.)',
                             'exp_en': '<b>[Step 5 Detailed Explanation]</b><br>Case 1 ($m_2 = 16$) gives '
                                       '$\\mathrm{P}(-0.5 \\le Z \\le -0.2) = 0.191 - 0.079 = 0.112$, matching the LHS '
                                       '($0.112$), while Case 2 ($m_2 = 14$) gives $0.118$. Thus $m_2 = 16$.'}]},
             {'title': '🌳 6단계 · [최종 목표 확률의 표준화] $Y \\sim \\mathrm{N}(16, 10^2)$에서 $\\mathrm{P}(Y \\ge 20)$을 표준정규분포로 '
                       '바꾸기',
              'title_en': '🌳 Step 6 · [Standardizing the Target Probability] Converting $\\mathrm{P}(Y \\ge 20)$ using '
                          '$Z_2 = \\dfrac{Y - 16}{10}$',
              'knowledge': '5단계에서 $\\text{Case 1}$이 채택되어 $Y \\sim \\mathrm{N}(16, 10^2)$으로 확정되었습니다! 이제 칠판 우측 판서처럼 구하려는 '
                           '확률 $\\mathrm{P}(Y \\ge 20)$을 표준화 공식 $Z = \\dfrac{Y - 16}{10}$으로 변환합니다:$$\\mathrm{P}(Y \\ge '
                           '20) = \\mathrm{P}\\left(Z \\ge \\frac{20 - 16}{10}\\right) = \\mathrm{P}(Z \\ge '
                           '0.4)$$기하학적으로 $Y = 20$은 대칭축 $m_2 = 16$에서 오른쪽으로 $4$칸, 즉 표준편차($10$)의 $0.4$배만큼 떨어진 위치입니다.',
              'knowledge_en': 'With $m_2 = 16$ and $\\sigma = 10$ confirmed from Case 1, standardize $\\mathrm{P}(Y '
                              '\\ge 20)$ via $Z = \\dfrac{Y - 16}{10}$: $\\mathrm{P}(Y \\ge 20) = \\mathrm{P}\\left(Z '
                              '\\ge \\dfrac{20 - 16}{10}\\right) = \\mathrm{P}(Z \\ge 0.4)$.',
              'questions': [{'level_label': '목표 확률 표준화 디딤돌 6',
                             'level_label_en': 'Target Standardization Step 6',
                             'stem': '확정된 평균 $m_2 = 16$을 대입하여 $\\mathrm{P}(Y \\ge 20) = \\mathrm{P}\\left(Z \\ge '
                                     '\\dfrac{20 - 16}{10}\\right) = \\mathrm{P}(Z \\ge z_0)$으로 나타낼 때, 경계값 $z_0$는?',
                             'stem_en': 'With $m_2 = 16$, what is the standardized boundary $z_0 = \\dfrac{20 - '
                                        '16}{10}$ in $\\mathrm{P}(Y \\ge 20) = \\mathrm{P}(Z \\ge z_0)$?',
                             'options': ['$0.2$', '$0.3$', '$0.4$', '$0.5$', '$0.6$'],
                             'answer': 3,
                             'exp': '<b>[6단계 상세 해설]</b><br>$z_0 = \\dfrac{20 - 16}{10} = \\dfrac{4}{10} = 0.4$이므로 '
                                    '$\\mathrm{P}(Y \\ge 20) = \\mathrm{P}(Z \\ge 0.4)$입니다.',
                             'exp_en': '<b>[Step 6 Detailed Explanation]</b><br>$z_0 = \\dfrac{20 - 16}{10} = 0.4$, so '
                                       '$\\mathrm{P}(Y \\ge 20) = \\mathrm{P}(Z \\ge 0.4)$.'}]},
             {'title': '💎 7단계 · [오른쪽 꼬리 넓이 계산] 반쪽 넓이 $0.5$에서 가운데 넓이 $0.155$를 빼서 $k = \\mathrm{P}(Z \\ge 0.4)$ 구하기',
              'title_en': '💎 Step 7 · [Upper Tail Area] Computing $k = \\mathrm{P}(Z \\ge 0.4) = 0.5 - 0.155$',
              'knowledge': '종 모양의 표준정규분포 곡선 아래 전체 넓이는 $1$이고, 대칭축 $Z = 0$을 기준으로 오른쪽 반쪽 전체($Z \\ge 0$)의 넓이는 정확히 '
                           '<b>$0.5$</b>입니다. 표준정규분포표에서 가운데 구간 넓이 $\\mathrm{P}(0 \\le Z \\le 0.4) = 0.155$이므로, 오른쪽 꼬리 '
                           '영역의 넓이 $k = \\mathrm{P}(Z \\ge 0.4)$는:$$k = \\mathrm{P}(Z \\ge 0.4) = 0.5 - 0.155 = '
                           '0.345$$',
              'knowledge_en': 'The total area to the right of the symmetry axis $Z = 0$ is $0.5$. Subtracting the '
                              'central strip $\\mathrm{P}(0 \\le Z \\le 0.4) = 0.155$ leaves the upper tail area $k = '
                              '\\mathrm{P}(Z \\ge 0.4) = 0.5 - 0.155 = 0.345$.',
              'questions': [{'level_label': '꼬리 넓이 계산 디딤돌 7',
                             'level_label_en': 'Tail Area Calculation Step 7',
                             'stem': '오른쪽 반쪽 넓이 $0.5$에서 $\\mathrm{P}(0 \\le Z \\le 0.4) = 0.155$를 뺀 꼬리 확률 $k = '
                                     '\\mathrm{P}(Z \\ge 0.4) = 0.5 - 0.155$의 값은?',
                             'stem_en': 'What is the upper tail probability $k = \\mathrm{P}(Z \\ge 0.4) = 0.5 - '
                                        '0.155$?',
                             'options': ['$0.245$', '$0.315$', '$0.345$', '$0.355$', '$0.385$'],
                             'answer': 3,
                             'exp': '<b>[7단계 기하학적 해설]</b><br>오른쪽 반쪽 전체 넓이 $0.500$에서 가운데 부분 넓이 $0.155$를 잘라내면 오른쪽 꼬리 넓이 '
                                    '$k = 0.500 - 0.155 = 0.345$가 남습니다.',
                             'exp_en': '<b>[Step 7 Geometric Explanation]</b><br>Subtracting the central area $0.155$ '
                                       'from the right half-bell area $0.500$ gives $k = 0.345$.'}]},
             {'title': '🏆 8단계 · [최종 정답 완성] $1000 \\times k$의 값 구하기',
              'title_en': '🏆 Step 8 · [Final Synthesis] Computing $1000 \\times k$',
              'knowledge': '$k = 0.345$에 $1000$을 곱하면 소수점이 오른쪽으로 세 칸 이동하여 최종 정답 <b>$345$</b>가 완성됩니다.',
              'knowledge_en': 'Multiplying $k = 0.345$ by $1000$ shifts the decimal point three places to the right, '
                              'yielding the final answer $345$.',
              'questions': [{'level_label': '최종 종합 디딤돌 8',
                             'level_label_en': 'Final Synthesis Step 8',
                             'stem': '$k = 0.345$일 때, $1000 \\times k$의 값은?',
                             'stem_en': 'Given $k = 0.345$, what is $1000 \\times k$?',
                             'options': ['$315$', '$335$', '$345$', '$355$', '$365$'],
                             'answer': 3,
                             'exp': '<b>[8단계 최종 정답]</b><br>$\\therefore 1000 \\times k = 1000 \\times 0.345 = '
                                    '\\underline{\\underline{345}}$입니다.',
                             'exp_en': '<b>[Step 8 Final Answer]</b><br>$\\therefore 1000 \\times k = 1000 \\times '
                                       '0.345 = 345$.'}]}],
  'final': {'stem': '확률변수 $X$는 정규분포 $\\mathrm{N}(m_1, 10^2)$을 따르고, 확률변수 $Y$는 정규분포 $\\mathrm{N}(m_2, 10^2)$을 따른다. 확률변수 '
                    '$X$의 확률밀도함수 $f(x)$와 확률변수 $Y$의 확률밀도함수 $g(x)$가 다음 조건을 만족시킨다.<br><br>(가) 모든 실수 $x$에 대하여 $f(x) \\le '
                    'f(4)$이다.<br>(나) $f(5) = g(15)$<br><br>$\\mathrm{P}(1 \\le X \\le 2) + \\mathrm{P}(7 \\le X \\le '
                    '9) = \\mathrm{P}(11 \\le Y \\le 14)$일 때, $\\mathrm{P}(Y \\ge 20)$의 값을 표준정규분포표를 이용하여 구한 값이 $k$이다. '
                    '$1000 \\times k$의 값을 구하시오. (단, $\\mathrm{P}(0 \\le Z \\le 0.1)=0.040,\\ \\mathrm{P}(0 \\le Z \\le '
                    '0.2)=0.079,\\ \\mathrm{P}(0 \\le Z \\le 0.3)=0.118,\\ \\mathrm{P}(0 \\le Z \\le 0.4)=0.155,\\ '
                    '\\mathrm{P}(0 \\le Z \\le 0.5)=0.191,\\ \\mathrm{P}(0 \\le Z \\le 0.6)=0.226$) [4점]',
            'stem_en': 'Random variables $X \\sim \\mathrm{N}(m_1, 10^2)$ and $Y \\sim \\mathrm{N}(m_2, 10^2)$ have '
                       'probability density functions $f(x)$ and $g(x)$ satisfying:<br>(가) $f(x) \\le f(4)$ for all '
                       'real $x$.<br>(나) $f(5) = g(15)$.<br>Given $\\mathrm{P}(1 \\le X \\le 2) + \\mathrm{P}(7 \\le X '
                       '\\le 9) = \\mathrm{P}(11 \\le Y \\le 14)$, let $k = \\mathrm{P}(Y \\ge 20)$ using the standard '
                       'normal table ($\\mathrm{P}(0 \\le Z \\le 0.2)=0.079,\\ \\mathrm{P}(0 \\le Z \\le 0.3)=0.118,\\ '
                       '\\mathrm{P}(0 \\le Z \\le 0.4)=0.155,\\ \\mathrm{P}(0 \\le Z \\le 0.5)=0.191$). Find $1000 '
                       '\\times k$. [4 points]',
            'options': ['$315$', '$335$', '$345$', '$355$', '$365$'],
            'answer': 3,
            'exp': '조건 (가) $f(x) \\le f(4)$에서 곡선 $f$의 대칭축(평균)은 $m_1 = 4$이고, 조건 (나) $f(5) = g(15)$에서 합동인 곡선 $g$ 위의 점 '
                   '$15$의 위치에 따라 $\\text{Case 1}(m_2 = 16)$과 $\\text{Case 2}(m_2 = 14)$로 나뉩니다. 좌변을 $Z_1 = '
                   '\\dfrac{X-4}{10}$으로 표준화하면 $\\mathrm{P}(-0.3 \\le Z \\le -0.2) + \\mathrm{P}(0.3 \\le Z \\le 0.5) = '
                   '(\\cancel{0.118} - 0.079) + (0.191 - \\cancel{0.118}) = 0.112$입니다. 우변 $\\mathrm{P}(11 \\le Y \\le '
                   '14)$를 검증하면 $\\text{Case 1}(m_2 = 16)$일 때 $\\mathrm{P}(-0.5 \\le Z \\le -0.2) = 0.191 - 0.079 = '
                   '0.112$로 성립하고($\\text{Case 2}: m_2 = 14$일 때는 $0.118$로 모순), 따라서 $k = \\mathrm{P}(Y \\ge 20) = '
                   '\\mathrm{P}(Z \\ge 0.4) = 0.5 - 0.155 = 0.345 \\implies 1000k = 345$입니다.',
            'exp_en': 'From (가) $f(x) \\le f(4)$, $m_1 = 4$. From (나) $f(5) = g(15)$, congruent curve $g$ yields '
                      '$\\text{Case 1 }(m_2 = 16)$ and $\\text{Case 2 }(m_2 = 14)$. Standardizing the LHS gives '
                      '$\\mathrm{P}(-0.3 \\le Z \\le -0.2) + \\mathrm{P}(0.3 \\le Z \\le 0.5) = (\\cancel{0.118} - '
                      '0.079) + (0.191 - \\cancel{0.118}) = 0.112$. Testing the RHS $\\mathrm{P}(11 \\le Y \\le 14)$ '
                      'confirms $\\text{Case 1 }(m_2 = 16)$ with $\\mathrm{P}(-0.5 \\le Z \\le -0.2) = 0.112$ (while '
                      '$\\text{Case 2}$ gives $0.118$). Thus $k = \\mathrm{P}(Y \\ge 20) = \\mathrm{P}(Z \\ge 0.4) = '
                      '0.5 - 0.155 = 0.345$ and $1000k = 345$.',
            'solution': '<h4>📋 [1. 문제 분석 및 핵심 출제 의도 — 종 모양 곡선의 합동과 대칭성]</h4>\n'
                        '<p>본 문항은 표준편차가 $\\sigma = 10$으로 같은 두 정규분포 $X \\sim \\mathrm{N}(m_1, 10^2)$과 $Y \\sim '
                        '\\mathrm{N}(m_2, 10^2)$에서 <b>두 확률밀도함수 곡선 $y = f(x)$, $y = g(x)$가 평행이동에 의해 완전히 포개어지는 합동 '
                        '도형</b>임을 기하학적으로 이해하고, 표준화 변환 $Z_1 = \\dfrac{X - m_1}{10},\\ Z_2 = \\dfrac{Y - m_2}{10} \\sim '
                        '\\mathrm{N}(0, 1)$을 통해 대칭 구간의 넓이 합과 평균 $m_2$의 위치를 추론하는 문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [2. 칠판 판서 완결 풀이 &amp; 기하학적 원리 상세 전개]</h4>\n'
                        '<p>\n'
                        '  <b>■ 1단계: 표준화 변수 설정과 조건 (가) $f(x) \\le f(4)$의 기하학적 해석 ($m_1 = 4$)</b><br>\n'
                        '  $$X \\sim \\mathrm{N}(m_1, 10^2) \\ (\\text{확률밀도함수 } f(x)), \\qquad Z_1 = \\frac{X - '
                        'm_1}{10} \\sim \\mathrm{N}(0, 1)$$\n'
                        '  $$Y \\sim \\mathrm{N}(m_2, 10^2) \\ (\\text{확률밀도함수 } g(x)), \\qquad Z_2 = \\frac{Y - '
                        'm_2}{10} \\sim \\mathrm{N}(0, 1)$$\n'
                        '  • <b>기하학적 의미</b>: 조건 (가)에서 모든 실수 $x$에 대하여 $\\underline{\\underline{f(x) \\le f(4)}}$라는 것은, '
                        '종 모양 곡선 $y = f(x)$에서 <b>$x = 4$일 때의 높이 $f(4)$가 가장 높은 산봉우리 꼭대기(최댓값)</b>라는 뜻입니다.<br>\n'
                        '  • 정규분포 곡선은 좌우 대칭축인 평균에서 유일한 최댓값을 가지므로 곡선 $f(x)$의 대칭축(평균)은 <b>$m_1 = 4$</b>입니다.<br><br>\n'
                        '  <b>■ 2단계: 조건 (나) $\\underline{\\underline{f(5) = g(15)}}$의 기하학적 작도와 $\\text{Case 1}, '
                        '\\text{Case 2}$ 분류</b><br>\n'
                        '  • 두 정규분포 $X, Y$는 표준편차가 $10$으로 같으므로 두 종 모양 곡선 $f(x)$와 $g(x)$는 폭과 높이가 똑같은 <b>합동 '
                        '곡선</b>입니다.<br>\n'
                        '  • 곡선 $f$에서 $x = 5$는 대칭축 $m_1 = 4$로부터 오른쪽으로 <b>거리가 $1$만큼 떨어진 지점</b>($5 - 4 = 1$)입니다.<br>\n'
                        '  • 따라서 합동인 곡선 $g$에서 높이가 $f(5)$와 똑같은 점($g(15) = f(5)$)은 대칭축 $x = m_2$를 중심으로 <b>왼쪽으로 $1$칸 떨어진 '
                        '비탈면</b>과 <b>오른쪽으로 $1$칸 떨어진 비탈면</b> 두 곳에 대칭으로 나타납니다:<br>\n'
                        '  &nbsp;&nbsp;① <b>$\\text{Case 1}$ ($15$가 대칭축 $m_2$의 왼쪽에 위치할 때)</b>: $m_2 - 1 = 15 \\implies '
                        '\\underline{\\mathbf{m_2 = 16}}$<br>\n'
                        '  &nbsp;&nbsp;② <b>$\\text{Case 2}$ ($15$가 대칭축 $m_2$의 오른쪽에 위치할 때)</b>: $m_2 + 1 = 15 '
                        '\\implies \\underline{\\mathbf{m_2 = 14}}$<br><br>\n'
                        '  <b>■ 3단계: 좌변 $\\mathrm{P}(1 \\le X \\le 2) + \\mathrm{P}(7 \\le X \\le 9)$의 표준화 계산과 '
                        '$\\cancel{0.118}$ 상쇄의 기하학</b><br>\n'
                        '  주어진 확률 등식 $\\mathrm{P}(1 \\le X \\le 2) + \\mathrm{P}(7 \\le X \\le 9) = \\mathrm{P}(11 '
                        '\\le Y \\le 14)$의 좌변을 $Z_1 = \\dfrac{X - 4}{10}$으로 표준화하면:\n'
                        '  $$\\mathrm{P}\\left(\\frac{-3}{10} \\le Z \\le \\frac{-2}{10}\\right) + '
                        '\\mathrm{P}\\left(\\frac{3}{10} \\le Z \\le \\frac{5}{10}\\right)$$\n'
                        '  $$= \\mathrm{P}(-0.3 \\le Z \\le -0.2) + \\mathrm{P}(0.3 \\le Z \\le 0.5)$$\n'
                        '  $$= \\cancel{0.118} - 0.079 + 0.191 - \\cancel{0.118} = \\mathbf{0.112}$$\n'
                        '  • <b>🎨 [기하학적 설명: 왜 $0.118$이 상쇄되고 하나의 구간이 될까?]</b><br>\n'
                        '  &nbsp;&nbsp;- 곡선 $f(x)$에서 왼쪽 조각 $[1, 2]$($Z \\in [-0.3, -0.2]$, 대칭축 $4$에서 왼쪽 $2\\sim 3$칸)를 '
                        '대칭축 $m_1 = 4$($Z = 0$)에 대하여 오른쪽으로 거울 대칭이동하면 <b>$[6, 7]$ ($Z \\in [0.2, 0.3]$, 오른쪽 $2\\sim '
                        '3$칸)</b>에 정확히 포개어집니다.<br>\n'
                        '  &nbsp;&nbsp;- 이 옮겨진 조각 $[6, 7]$($Z \\in [0.2, 0.3]$)이 원래 오른쪽에 있던 조각 $[7, 9]$($Z \\in [0.3, '
                        '0.5]$)와 <b>경계선 $X = 7$($Z = 0.3$, 표준정규분포표 넓이 $0.118$)에서 빈틈없이 맞물려 하나의 연속된 넓이 구간 $[6, 9]$($Z '
                        '\\in [0.2, 0.5]$, 대칭축에서 거리 $2\\sim 5$칸)</b>로 합쳐지기 때문에 중간 경계 넓이 $0.118$이 $+0.118$과 $-0.118$로 '
                        '서로 지워지는 것입니다!<br><br>\n'
                        '  <b>■ 4단계: 우변 $\\mathrm{P}(11 \\le Y \\le 14)$에 대한 $\\text{Case 1}$과 $\\text{Case 2}$ 대조 '
                        '검증</b><br>\n'
                        '  우변 $\\mathrm{P}(11 \\le Y \\le 14)$를 $Z_2 = \\dfrac{Y - m_2}{10}$으로 표준화하여 좌변의 넓이 $0.112$와 '
                        '비교합니다:\n'
                        '</p>\n'
                        '<table style="width:100%;border-collapse:collapse;margin:10px 0 '
                        '16px;font-size:0.88rem;border:1px solid rgba(124,196,255,0.35)">\n'
                        '  <thead>\n'
                        '    <tr style="background:rgba(56,189,248,0.16);color:#fde68a;text-align:center">\n'
                        '      <th style="padding:8px 10px;border:1px solid rgba(148,163,184,0.3);width:20%">구분</th>\n'
                        '      <th style="padding:8px 10px;border:1px solid '
                        'rgba(148,163,184,0.3);width:40%;background:rgba(52,211,153,0.16);color:#6ee7b7">⭕ '
                        '$\\text{Case 1}: \\underline{m_2 = 16}$ ($15$가 $m_2$ 왼쪽 $1$칸)</th>\n'
                        '      <th style="padding:8px 10px;border:1px solid '
                        'rgba(148,163,184,0.3);width:40%;background:rgba(251,113,133,0.14);color:#fecdd3">❌ '
                        '$\\text{Case 2}: \\underline{m_2 = 14}$ ($15$가 $m_2$ 오른쪽 $1$칸)</th>\n'
                        '    </tr>\n'
                        '  </thead>\n'
                        '  <tbody>\n'
                        '    <tr>\n'
                        '      <td style="padding:8px 10px;border:1px solid '
                        'rgba(148,163,184,0.25);font-weight:700;text-align:center;color:#7cc4ff">칠판 표준화 식</td>\n'
                        '      <td style="padding:8px 12px;border:1px solid rgba(148,163,184,0.25)">$$\\mathrm{P}(11 '
                        '\\le Y \\le 14) = \\mathrm{P}\\left(\\frac{-5}{10} \\le Z \\le \\frac{-2}{10}\\right)$$$$= '
                        '\\mathrm{P}(-0.5 \\le Z \\le -0.2)$$</td>\n'
                        '      <td style="padding:8px 12px;border:1px solid rgba(148,163,184,0.25)">$$\\mathrm{P}(11 '
                        '\\le Y \\le 14) = \\mathrm{P}\\left(\\frac{-3}{10} \\le Z \\le \\frac{0}{10}\\right)$$$$= '
                        '\\mathrm{P}(-0.3 \\le Z \\le 0)$$</td>\n'
                        '    </tr>\n'
                        '    <tr>\n'
                        '      <td style="padding:8px 10px;border:1px solid '
                        'rgba(148,163,184,0.25);font-weight:700;text-align:center;color:#7cc4ff">표 대입 계산값</td>\n'
                        '      <td style="padding:8px 12px;border:1px solid '
                        'rgba(148,163,184,0.25);text-align:center;background:rgba(52,211,153,0.10)">$0.191 - 0.079 = '
                        '\\underline{\\underline{\\mathbf{0.112}}}$<br><b style="color:#34d399">O.K.! (좌변 $0.112$와 정확히 '
                        '일치)</b></td>\n'
                        '      <td style="padding:8px 12px;border:1px solid '
                        'rgba(148,163,184,0.25);text-align:center;background:rgba(251,113,133,0.08)">$\\mathbf{0.118} '
                        '\\ne 0.112$<br><b style="color:#fb7185">✕ 탈락! (좌변 $0.112$와 불일치)</b></td>\n'
                        '    </tr>\n'
                        '    <tr>\n'
                        '      <td style="padding:8px 10px;border:1px solid '
                        'rgba(148,163,184,0.25);font-weight:700;text-align:center;color:#7cc4ff">기하학적 위치 해석</td>\n'
                        '      <td style="padding:8px 12px;border:1px solid '
                        'rgba(148,163,184,0.25);line-height:1.55">구간 $[11, 14]$는 대칭축 $m_2=16$으로부터 <b>왼쪽으로 $2\\sim 5$칸 '
                        '떨어진 구간</b>이므로, 좌변의 $[6, 9]$(대칭축 $4$에서 오른쪽 $2\\sim 5$칸)와 <b>완벽한 좌우 대칭(합동)</b>이 되어 넓이가 '
                        '같습니다!</td>\n'
                        '      <td style="padding:8px 12px;border:1px solid '
                        'rgba(148,163,184,0.25);line-height:1.55">구간 $[11, 14]$의 오른쪽 끝점 $14$가 <b>산봉우리 꼭대기($m_2=14$) '
                        '자체</b>에 걸치면서 대칭축에서 왼쪽 $0\\sim 3$칸인 가장 높은 중심부 영역이 되어 넓이가 더 커집니다.</td>\n'
                        '    </tr>\n'
                        '  </tbody>\n'
                        '</table>\n'
                        '<p>\n'
                        '  <b>■ 5단계: 최종 확률 $\\mathrm{P}(Y \\ge 20)$ 및 정답 $1000k$ 도출</b><br>\n'
                        '  $\\text{Case 1}$에 의해 $m_2 = 16$으로 확정되었으므로 $Y \\sim \\mathrm{N}(16, 10^2)$입니다. 구하는 확률 '
                        '$\\mathrm{P}(Y \\ge 20)$을 표준화하면:\n'
                        '  $$\\mathrm{P}(Y \\ge 20) = \\mathrm{P}\\left(Z \\ge \\frac{20 - 16}{10}\\right) = '
                        '\\mathrm{P}(Z \\ge 0.4) = 0.5 - 0.155 = 0.345$$\n'
                        '  • <b>기하학적 의미</b>: 대칭축 $m_2 = 16$($Z = 0$) 오른쪽 반쪽 전체의 넓이 $0.5$에서, $16 \\le Y \\le 20$($0 '
                        '\\le Z \\le 0.4$) 구간의 넓이 $0.155$를 빼낸 오른쪽 꼬리 영역의 넓이가 바로 $k = 0.345$입니다.\n'
                        '</p>\n'
                        '\n'
                        '<h4>🔗 [3. 수학자료실(min7014.github.io) 연계 심층 탐구]</h4>\n'
                        '<ul>\n'
                        '  <li>📌 <b><a href="https://min7014.github.io/math20230602001.html" target="_blank" '
                        'rel="noopener" style="color:#38bdf8">정규분포 (Normal Distribution)</a></b>: 평균 $m$과 표준편차 '
                        '$\\sigma$를 슬라이더로 움직이며 종 모양 확률밀도함수 곡선이 평행이동($m$ 변화)하거나 높낮이가 변하는($\\sigma$ 변화) 기하학적 성질을 <a '
                        'href="https://www.geogebra.org/m/enufqbhp" target="_blank" rel="noopener" '
                        'style="color:#6ee7b7">GeoGebra 앱렛</a>과 <a '
                        'href="https://min7014.github.io/2023/2023060201.pdf#toolbar=0&amp;view=Fit&amp;scrollbar=0" '
                        'target="_blank" rel="noopener" style="color:#fca5a5">단계별 증명 PDF</a>로 직접 확인해 보세요.</li>\n'
                        '  <li>📌 <b><a href="https://min7014.github.io/math20230603001.html" target="_blank" '
                        'rel="noopener" style="color:#38bdf8">표준정규분포 (Standard Normal Distribution)</a></b>: 서로 다른 '
                        '정규분포를 $Z = \\dfrac{X - m}{\\sigma}$으로 표준화할 때 곡선 아래의 색칠된 넓이(확률)가 어떻게 보존되는지 <a '
                        'href="https://www.geogebra.org/m/ewfbgb5b" target="_blank" rel="noopener" '
                        'style="color:#6ee7b7">GeoGebra 조작</a> 및 <a href="https://youtu.be/BZzCy9js8K8" '
                        'target="_blank" rel="noopener" style="color:#fde68a">해설 강의 영상</a>으로 탐구할 수 있습니다.</li>\n'
                        '  <li>📌 <b><a href="https://min7014.github.io/math20230613002.html" target="_blank" '
                        'rel="noopener" style="color:#38bdf8">표준정규분포표 ($z \\to p$) 동적 탐색기</a></b>: $z$값의 구간에 따른 넓이의 합과 '
                        '차($0.191 - 0.079 = 0.112$, $0.5 - 0.155 = 0.345$)를 <a '
                        'href="https://www.geogebra.org/m/pUgrEav5" target="_blank" rel="noopener" '
                        'style="color:#6ee7b7">GeoGebra 인터랙티브 도구</a>로 실험해 보세요.</li>\n'
                        '</ul>\n'
                        '\n'
                        '<h4>✨ [4. 정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 $k = 0.345$이므로 구하는 값은:\n'
                        '  $$\\therefore 1000 \\times k = 1000 \\times 0.345 = '
                        '\\underline{\\underline{\\mathbf{345}}}$$\n'
                        '</p>',
            'solution_en': '<h4>📋 [1. Problem Analysis &amp; Core Geometric Concepts]</h4>\n'
                           '<p>Because $X \\sim \\mathrm{N}(m_1, 10^2)$ and $Y \\sim \\mathrm{N}(m_2, 10^2)$ share the '
                           'same standard deviation $\\sigma = 10$, their probability density curves $y = f(x)$ and $y '
                           '= g(x)$ are <b>geometrically congruent bell curves</b> related by horizontal translation. '
                           'Standardizing via $Z_1 = \\dfrac{X - m_1}{10} \\sim \\mathrm{N}(0, 1)$ and $Z_2 = '
                           '\\dfrac{Y - m_2}{10} \\sim \\mathrm{N}(0, 1)$ lets us compare intervals directly on the '
                           'standard normal curve.</p>\n'
                           '\n'
                           '<h4>📐 [2. Complete Whiteboard Solution &amp; Geometric Explanation]</h4>\n'
                           '<p>\n'
                           '  <b>■ Step 1: Condition (가) $f(x) \\le f(4) \\implies m_1 = 4$</b><br>\n'
                           '  Geometrically, $f(x) \\le f(4)$ for all real $x$ means the bell curve $y = f(x)$ reaches '
                           'its highest peak at $x = 4$. Since the peak of a normal curve is its symmetry axis (mean), '
                           'we have <b>$m_1 = 4$</b>.<br><br>\n'
                           '  <b>■ Step 2: Condition (나) $f(5) = g(15) \\implies \\text{Case 1 }(m_2 = 16)$ vs. '
                           '$\\text{Case 2 }(m_2 = 14)$</b><br>\n'
                           '  On curve $f$, $x = 5$ is $1$ unit to the right of the peak $m_1 = 4$. Since curve $g$ is '
                           'congruent to $f$, a point with the same height $g(15) = f(5)$ must lie at distance $1$ '
                           'from the peak $m_2$ of $g$, giving two symmetric cases:<br>\n'
                           '  • <b>$\\text{Case 1}$ ($15$ is $1$ unit left of $m_2$)</b>: $m_2 - 1 = 15 \\implies '
                           '\\underline{m_2 = 16}$<br>\n'
                           '  • <b>$\\text{Case 2}$ ($15$ is $1$ unit right of $m_2$)</b>: $m_2 + 1 = 15 \\implies '
                           '\\underline{m_2 = 14}$<br><br>\n'
                           '  <b>■ Step 3: Standardizing the LHS &amp; Geometric Meaning of Canceling '
                           '$\\cancel{0.118}$</b><br>\n'
                           '  Standardizing $\\mathrm{P}(1 \\le X \\le 2) + \\mathrm{P}(7 \\le X \\le 9)$ with $Z_1 = '
                           '\\dfrac{X - 4}{10}$:<br>\n'
                           '  $$\\mathrm{P}\\left(\\frac{-3}{10} \\le Z \\le \\frac{-2}{10}\\right) + '
                           '\\mathrm{P}\\left(\\frac{3}{10} \\le Z \\le \\frac{5}{10}\\right) = \\mathrm{P}(-0.3 \\le '
                           'Z \\le -0.2) + \\mathrm{P}(0.3 \\le Z \\le 0.5)$$\n'
                           '  $$= \\cancel{0.118} - 0.079 + 0.191 - \\cancel{0.118} = \\mathbf{0.112}$$\n'
                           '  <i>Geometric insight</i>: Reflecting $[1, 2]$ ($Z \\in [-0.3, -0.2]$) across the '
                           'symmetry axis $m_1 = 4$ ($Z = 0$) maps it onto $[6, 7]$ ($Z \\in [0.2, 0.3]$), which '
                           'shares the boundary $X = 7$ ($Z = 0.3$, where $0.118$ cancels) with $[7, 9]$ ($Z \\in '
                           '[0.3, 0.5]$), forming the single contiguous interval $[6, 9]$ ($Z \\in [0.2, '
                           '0.5]$).<br><br>\n'
                           '  <b>■ Step 4: Testing $\\text{Case 1}$ and $\\text{Case 2}$ on the RHS $\\mathrm{P}(11 '
                           '\\le Y \\le 14)$</b><br>\n'
                           '  • <b>$\\text{Case 1}$ ($m_2 = 16$)</b>: $\\mathrm{P}(11 \\le Y \\le 14) = '
                           '\\mathrm{P}\\left(\\dfrac{-5}{10} \\le Z \\le \\dfrac{-2}{10}\\right) = \\mathrm{P}(-0.5 '
                           '\\le Z \\le -0.2) = 0.191 - 0.079 = \\underline{\\underline{0.112}}$ (<b>O.K.!</b> Mirrors '
                           '$Z \\in [0.2, 0.5]$ across $Z = 0$).<br>\n'
                           '  • <b>$\\text{Case 2}$ ($m_2 = 14$)</b>: $\\mathrm{P}(11 \\le Y \\le 14) = '
                           '\\mathrm{P}\\left(\\dfrac{-3}{10} \\le Z \\le \\dfrac{0}{10}\\right) = \\mathrm{P}(-0.3 '
                           '\\le Z \\le 0) = 0.118 \\ne 0.112$ (<b>Invalid!</b> Right endpoint $14$ sits at the peak '
                           '$Z = 0$).<br><br>\n'
                           '  <b>■ Step 5: Final Tail Probability $\\mathrm{P}(Y \\ge 20)$</b><br>\n'
                           '  With $m_2 = 16$ confirmed:<br>\n'
                           '  $$k = \\mathrm{P}(Y \\ge 20) = \\mathrm{P}\\left(Z \\ge \\frac{20 - 16}{10}\\right) = '
                           '\\mathrm{P}(Z \\ge 0.4) = 0.5 - 0.155 = 0.345$$\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [3. Final Answer &amp; Practical Tips]</h4>\n'
                           '<p>\n'
                           '  Therefore, $1000 \\times k = 1000 \\times 0.345 = '
                           '\\underline{\\underline{\\mathbf{345}}}$.\n'
                           '</p>'}},
 {'slug': 'c2610p30',
  'qNum': '확통 30',
  'subject': '확률과 통계',
  'title': '[2026학년도 10월 고3 확통 30번] 두 주머니에서 비복원 추출과 조건부확률',
  'title_en': '[2026 AY Oct Exam Grade 12 Prob&Stats #30] Conditional Probability with Sampling Without Replacement '
              'from Two Bags',
  'summary_ko': '1시행 $(x_1, y_1)$과 2시행 $(x_2, y_2)$를 순서쌍 $(x_1, y_1, x_2, y_2)$로 놓고, $\\mathrm{I})\\ a_1=a_2=1$의 여사건 '
                '$4$가지($24+8+24+8=64$)를 전체 ${}_5\\mathrm{C}_1 \\times {}_5\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 '
                '\\times {}_4\\mathrm{C}_1 = 400$에서 빼 분모 $336$을 구한 뒤, $\\mathrm{II})\\ \\mathrm{B}_{y_1,y_2}$에 ①이 $3$개 '
                '남는 $(y_1,y_2)=(1,2),(2,1)$의 분자 $48+48=96$을 구해 $\\dfrac{96}{336}=\\dfrac{12}{42}=\\dfrac{2}{7}$ 도출하기',
  'summary_en': 'Represent the two rounds as 4-tuples $(x_1, y_1, x_2, y_2)$. For $\\mathrm{I})\\ a_1=a_2=1$, subtract '
                'the $4$ surviving complement tuples ($24+8+24+8=64$) from ${}_5\\mathrm{C}_1 \\times '
                '{}_5\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 = 400$ to get $336$. For '
                '$\\mathrm{II})$, count $48+48=96$ tuples with $(y_1,y_2)=(1,2),(2,1)$ leaving three ①s in '
                '$\\mathrm{B}_{y_1,y_2}$, giving $\\dfrac{96}{336}=\\dfrac{12}{42}=\\dfrac{2}{7}$ ($p+q=9$).',
  'tags': ['확률과 통계', '확률', '조건부확률', '비복원추출', '여사건', '경우의수', '단답형', '30번'],
  'symbols': [{'sym': '$\\mathrm{A}: \\text{①}\\times 3,\\ \\text{②}\\times 2 \\quad / \\quad \\mathrm{B}: '
                      '\\text{①}\\times 4,\\ \\text{②}\\times 1$',
               'desc': '주머니 $\\mathrm{A}$(숫자 $1$인 공 $3$개, 숫자 $2$인 공 $2$개)와 주머니 $\\mathrm{B}$(숫자 $1$인 공 $4$개, 숫자 $2$인 공 '
                       '$1$개)의 초기 구성',
               'desc_en': 'Initial composition of Bag $\\mathrm{A}$ (three ①s, two ②s) and Bag $\\mathrm{B}$ (four ①s, '
                          'one ②).'},
              {'sym': '$(x_1, y_1, x_2, y_2),\\ \\ a_1=\\min(x_1,y_1),\\ \\ a_2=\\min(x_2,y_2)$',
               'desc': '$1$시행에서 $\\mathrm{A}, \\mathrm{B}$가 꺼낸 수 $x_1, y_1$(남은 주머니 $\\mathrm{A}_{x_1}, '
                       '\\mathrm{B}_{y_1}$)과 $2$시행에서 꺼낸 수 $x_2, y_2$(남은 주머니 $\\mathrm{A}_{x_1,x_2}, '
                       '\\mathrm{B}_{y_1,y_2}$)',
               'desc_en': '$x_1, y_1$ drawn from $\\mathrm{A}, \\mathrm{B}$ in Round 1 (leaving $\\mathrm{A}_{x_1}, '
                          '\\mathrm{B}_{y_1}$) and $x_2, y_2$ drawn in Round 2 (leaving $\\mathrm{A}_{x_1,x_2}, '
                          '\\mathrm{B}_{y_1,y_2}$).'},
              {'sym': '${}_n\\mathrm{C}_1 = n \\quad (\\text{전체: } {}_5\\mathrm{C}_1 \\times {}_5\\mathrm{C}_1 \\times '
                      '{}_4\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 = 400)$',
               'desc': "$n$개의 공 중 $1$개를 뽑는 기호 ${}_n\\mathrm{C}_1$은 초등학교의 '$n$가지 중 하나 고르기($n$)'와 같으며, $(x_1, y_1, x_2, "
                       'y_2)$ 순서 그대로 곱해 계산',
               'desc_en': '${}_n\\mathrm{C}_1 = n$ counts ways to pick $1$ ball out of $n$, multiplied in the exact '
                          'tuple order $(x_1, y_1, x_2, y_2)$.'},
              {'sym': '$\\text{by }\\mathrm{I})\\ \\mathrm{II}):\\ \\dfrac{48+48}{400-(24+8+24+8)} = \\dfrac{96}{336} '
                      '= \\dfrac{12}{42} = \\dfrac{2}{7}$',
               'desc': '분모 $\\mathrm{I})$($a_1=a_2=1$인 $336$가지) 분의 분자 $\\mathrm{II})$($\\mathrm{B}_{y_1,y_2}$에 ①이 $3$개 '
                       '남는 $96$가지)를 $8$과 $6$으로 차례로 약분',
               'desc_en': 'Conditional probability $\\dfrac{\\text{II)}}{\\text{I)}} = \\dfrac{96}{336}$, reduced by '
                          '$8$ to $\\dfrac{12}{42}$ and by $6$ to $\\dfrac{2}{7}$.'}],
  'levels': [{'title': "🔰 1단계 · [초등 기호 번역과 여사건 선택] $a_1=\\min(x_1,y_1)$, $a_2=\\min(x_2,y_2)$에서 '직접 계산'과 '여사건' 중 어느 쪽이 "
                       '편할까?',
              'title_en': '🔰 Step 1 · [Symbol Translation & Complement Choice] Direct calculation vs. Complement for '
                          '$a_1=\\min(x_1,y_1)$ and $a_2=\\min(x_2,y_2)$',
              'knowledge': '먼저 시행 과정을 한눈에 보이도록 기호로 정리해 봅시다!<ul><li><b>$1$시행</b>: 주머니 $\\mathrm{A}$에서 꺼낸 수를 $x_1$(남은 '
                           '주머니 $\\mathrm{A}_{x_1}$), 주머니 $\\mathrm{B}$에서 꺼낸 수를 $y_1$(남은 주머니 $\\mathrm{B}_{y_1}$)이라 '
                           '하면, 두 수 중 크지 않은(더 작거나 같은) 수는 <b>$a_1 = \\min(x_1, y_1)$</b>입니다.</li><li><b>$2$시행</b>: 남은 '
                           '주머니 $\\mathrm{A}_{x_1}$에서 꺼낸 수를 $x_2$(남은 주머니 $\\mathrm{A}_{x_1,x_2}$), 남은 주머니 '
                           '$\\mathrm{B}_{y_1}$에서 꺼낸 수를 $y_2$(남은 주머니 $\\mathrm{B}_{y_1,y_2}$)라 하면, 크지 않은 수는 <b>$a_2 = '
                           '\\min(x_2, y_2)$</b>입니다.</li><li><b>$\\mathrm{I})\\ a_1 = a_2 = 1$의 조건 비교 ("어느 쪽 계산이 '
                           '편할까?")</b>:<br>&nbsp;&nbsp;• <b>직접 세기</b>: $(x_1\\text{ 또는 }y_1\\text{은 }1)$ <b>그리고</b> '
                           "$(x_2\\text{ 또는 }y_2\\text{는 }1)$ $\\to$ '또는'이 겹쳐 있어 가짓수가 너무 많습니다!<br>&nbsp;&nbsp;• "
                           '<b>여사건(반대 경우) 세기</b>: $a_1 = 2\\text{ 또는 }a_2 = 2$가 되려면 두 수 중 작은 수가 $2$여야 하므로, <b>$(x_1 = '
                           'y_1 = 2)\\text{ 또는 }(x_2 = y_2 = 2)$</b>일 때만 찾으면 되어 여사건 계산이 훨씬 편합니다!</li></ul>',
              'knowledge_en': 'Let $x_1, y_1$ be the numbers drawn from $\\mathrm{A}, \\mathrm{B}$ in Round 1 (leaving '
                              '$\\mathrm{A}_{x_1}, \\mathrm{B}_{y_1}$) with $a_1 = \\min(x_1, y_1)$, and let $x_2, '
                              'y_2$ be the numbers drawn in Round 2 (leaving $\\mathrm{A}_{x_1,x_2}, '
                              '\\mathrm{B}_{y_1,y_2}$) with $a_2 = \\min(x_2, y_2)$.<ul><li><b>Direct condition for '
                              '$\\mathrm{I})\\ a_1=a_2=1$</b>: $(x_1=1\\text{ or }y_1=1)$ <b>and</b> $(x_2=1\\text{ or '
                              '}y_2=1)$.</li><li><b>Complement ($a_1=2\\text{ or }a_2=2$)</b>: Since the minimum of '
                              'two numbers in $\\{1,2\\}$ is $2$ iff both are $2$, the complement is simply <b>$(x_1 = '
                              'y_1 = 2)\\text{ or }(x_2 = y_2 = 2)$</b>, which is much easier to count!</li></ul>',
              'questions': [{'level_label': '초등 기호 번역과 여사건 디딤돌 1',
                             'level_label_en': 'Symbol Translation & Complement Step 1',
                             'stem': '초등학교 숫자 비교 규칙으로 $a_1 = \\min(x_1, y_1)$, $a_2 = \\min(x_2, y_2)$라 할 때, 분모 사건 '
                                     '$\\mathrm{I})\\ a_1 = a_2 = 1$을 쉽게 구하기 위한 <b>여사건($a_1 = 2$ 또는 $a_2 = 2$)</b>을 '
                                     '올바르게 나타낸 것은?',
                             'stem_en': 'With $a_1 = \\min(x_1, y_1)$ and $a_2 = \\min(x_2, y_2)$, how is the '
                                        'complement event ($a_1 = 2$ or $a_2 = 2$) of $\\mathrm{I})\\ a_1 = a_2 = 1$ '
                                        'expressed?',
                             'options': ['$(x_1 = y_1 = 2)$ 또는 $(x_2 = y_2 = 2)$',
                                         '$(x_1 = y_1 = 1)$ 또는 $(x_2 = y_2 = 1)$',
                                         '$(x_1 = 2$이고 $x_2 = 2)$',
                                         '$(y_1 = 2$이고 $y_2 = 2)$',
                                         '$(x_1 = y_1 = 2)$ 그리고 $(x_2 = y_2 = 2)$'],
                             'answer': 1,
                             'exp': '<b>[1단계 상세 해설]</b><br>• 주머니 속 공에는 숫자 $1$ 또는 $2$만 적혀 있습니다.<br>• $(1, 2)$를 꺼내면 $1$과 '
                                    '$2$ 중 크지 않은(더 작거나 같은) 수는 <b>$1$</b>입니다.<br>• 네 가지 순서쌍 $(1,1)\\to 1$, $(1,2)\\to '
                                    '1$, $(2,1)\\to 1$, $(2,2)\\to 2$를 모두 비교해 보면, 두 주머니 중 <b>적어도 한 곳에서 $1$이 나오면 무조건 '
                                    '$a_n = 1$</b>이 되고, 오직 <b>두 주머니 모두 $2$를 꺼낸 $(2, 2)$일 때만 $a_n = 2$</b>가 됩니다.',
                             'exp_en': '<b>[Step 1 Detailed Explanation]</b><br>Comparing all four pairs $(1,1)\\to '
                                       '1$, $(1,2)\\to 1$, $(2,1)\\to 1$, and $(2,2)\\to 2$, the minimum is $1$ '
                                       'whenever at least one bag draws $1$, and the minimum is $2$ if and only if '
                                       'both bags draw $2$, i.e., $(2, 2)$.'}]},
             {'title': '🌿 2단계 · [초등 곱셈과 전체 경우의 수] $(x_1, y_1, x_2, y_2)$를 뽑는 전체 가짓수 ${}_5\\mathrm{C}_1 \\times '
                       '{}_5\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 = 400$',
              'title_en': '🌿 Step 2 · [Elementary Multiplication & Total Outcomes] Computing ${}_5\\mathrm{C}_1 '
                          '\\times {}_5\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 = 400$',
              'knowledge': '고등학교 조합 기호 <b>${}_n\\mathrm{C}_1$</b>은 사실 초등학교에서 배운 <b>"서로 다른 $n$개의 공 중에서 꺼낼 공 $1$개를 고르는 '
                           '가짓수($n$가지)"</b>를 뜻하는 약속입니다! (${}_5\\mathrm{C}_1 = 5$, ${}_4\\mathrm{C}_1 = 4$)<br>두 번의 시행 '
                           '결과를 순서쌍 <b>$(x_1, y_1, x_2, y_2)$</b>로 적고, 자리 순서 그대로 전체 경우의 수를 곱해 봅시다:<ul><li><b>$1$시행 '
                           '($x_1, y_1$)</b>: 주머니 $\\mathrm{A}$의 공 $5$개 중 $1$개 선택(${}_5\\mathrm{C}_1 = 5$) $\\times$ '
                           '주머니 $\\mathrm{B}$의 공 $5$개 중 $1$개 선택(${}_5\\mathrm{C}_1 = 5$)</li><li><b>$2$시행 ($x_2, '
                           'y_2$)</b>: 꺼낸 공을 다시 넣지 않으므로, 남은 $\\mathrm{A}_{x_1}$의 공 $4$개 중 $1$개 선택(${}_4\\mathrm{C}_1 = '
                           '4$) $\\times$ 남은 $\\mathrm{B}_{y_1}$의 공 $4$개 중 $1$개 선택(${}_4\\mathrm{C}_1 = '
                           '4$)</li></ul>따라서 전체 경우의 수는 <b>${}_5\\mathrm{C}_1 \\times {}_5\\mathrm{C}_1 \\times '
                           '{}_4\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 = 5 \\times 5 \\times 4 \\times 4$</b>입니다!',
              'knowledge_en': 'The symbol ${}_n\\mathrm{C}_1 = n$ simply means choosing $1$ ball out of $n$ distinct '
                              'balls. Multiplying in the exact order of the 4-tuple $(x_1, y_1, x_2, '
                              'y_2)$:<ul><li><b>Round 1 ($x_1, y_1$)</b>: ${}_5\\mathrm{C}_1 \\times {}_5\\mathrm{C}_1 '
                              '= 5 \\times 5 = 25$ ways.</li><li><b>Round 2 ($x_2, y_2$)</b>: Since balls are not '
                              'replaced, $\\mathrm{A}_{x_1}$ and $\\mathrm{B}_{y_1}$ each have $4$ balls left, giving '
                              '${}_4\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 = 4 \\times 4 = 16$ ways.</li></ul>',
              'questions': [{'level_label': '초등 곱셈과 전체 가짓수 디딤돌 2',
                             'level_label_en': 'Total Outcomes Step 2',
                             'stem': '순서쌍 $(x_1, y_1, x_2, y_2)$의 자리 순서대로 공을 꺼내는 전체 경우의 수 ${}_5\\mathrm{C}_1 \\times '
                                     '{}_5\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 = 5 '
                                     '\\times 5 \\times 4 \\times 4$를 계산하면?',
                             'stem_en': 'What is the total number of outcomes ${}_5\\mathrm{C}_1 \\times '
                                        '{}_5\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 = 5 '
                                        '\\times 5 \\times 4 \\times 4$?',
                             'options': ['$100$', '$200$', '$300$', '$400$', '$500$'],
                             'answer': 4,
                             'exp': '<b>[2단계 상세 해설]</b><br>• 같은 숫자가 적힌 공이라도 서로 다른 '
                                    '공($\\mathrm{A}=\\{1_a,1_b,1_c,2_a,2_b\\}$, '
                                    '$\\mathrm{B}=\\{1_p,1_q,1_r,1_s,2_p\\}$)으로 구별해야 각 경우가 모두 똑같은 확률을 가집니다.<br>• 주머니 '
                                    '$\\mathrm{A}$에서 비복원으로 $2$번 꺼내는 가짓수: $5 \\times 4 = 20$가지<br>• 주머니 $\\mathrm{B}$에서 '
                                    '비복원으로 $2$번 꺼내는 가짓수: $5 \\times 4 = 20$가지<br>• 두 주머니에서 동시에 꺼내므로 곱의 법칙에 의해 전체 근원사건의 '
                                    '개수는 $20 \\times 20 = \\mathbf{400}$가지입니다.',
                             'exp_en': '<b>[Step 2 Detailed Explanation]</b><br>Labeling all $5$ balls in each bag as '
                                       'distinct ensures equally likely outcomes. Bag A has $5 \\times 4 = 20$ ordered '
                                       'pairs and Bag B has $5 \\times 4 = 20$ ordered pairs, giving $20 \\times 20 = '
                                       '\\mathbf{400}$ total outcomes.'}]},
             {'title': '🌱 3단계 · [여사건 순서쌍 소거] $(x_1, y_1, x_2, y_2)$ 후보 중 불가능한 순서쌍 지우기',
              'title_en': '🌱 Step 3 · [Eliminating Impossible Tuples] Crossing out impossible $(x_1, y_1, x_2, y_2)$ '
                          'candidates in the complement',
              'knowledge': '여사건 <b>$(x_1 = y_1 = 2)\\text{ 또는 }(x_2 = y_2 = 2)$</b>를 만족하는 순서쌍 $(x_1, y_1, x_2, y_2)$ '
                           '후보들을 칠판처럼 모두 나열해 보고, 실제로 일어날 수 없는 것을 지워 봅시다!<ul><li><b>$x_1 = y_1 = 2$일 때</b> (뒤의 $x_2, '
                           'y_2$ 자리에 $1, 2$를 넣어 봄):<br>$$\\checkmark\\ (2, 2, 1, 1), \\quad \\cancel{(2, 2, 1, 2)}, '
                           '\\quad \\checkmark\\ (2, 2, 2, 1), \\quad \\cancel{(2, 2, 2, 2)}$$</li><li><b>$x_2 = y_2 = '
                           '2$일 때</b> (앞의 $x_1, y_1$ 자리에 $1, 2$를 넣어 봄):<br>$$\\checkmark\\ (1, 1, 2, 2), \\quad '
                           '\\cancel{(1, 2, 2, 2)}, \\quad \\checkmark\\ (2, 1, 2, 2), \\quad \\cancel{(2, 2, 2, '
                           '2)}$$</li></ul><b>핵심 이유</b>: 주머니 $\\mathrm{B}$($\\text{①}\\times 4,\\ \\text{②}\\times '
                           '1$)에는 숫자 $2$가 적힌 공(`②`)이 <b>오직 $1$개뿐</b>입니다! 따라서 비복원 추출에서 $y_1 = 2$와 $y_2 = 2$가 동시에 들어 있는 '
                           '$\\cancel{(2, 2, 1, 2)}$, $\\cancel{(1, 2, 2, 2)}$, $\\cancel{(2, 2, 2, 2)}$는 절대 일어날 수 없어 '
                           '지워지고, <b>서로 겹치지 않는 $4$가지 순서쌍(`i ~ iv`)</b>만 남습니다!',
              'knowledge_en': 'Listing all candidate 4-tuples $(x_1, y_1, x_2, y_2)$ for $(x_1=y_1=2)\\text{ or '
                              '}(x_2=y_2=2)$:<ul><li>From $x_1=y_1=2$: $\\checkmark\\ (2,2,1,1),\\ '
                              '\\cancel{(2,2,1,2)},\\ \\checkmark\\ (2,2,2,1),\\ \\cancel{(2,2,2,2)}$</li><li>From '
                              '$x_2=y_2=2$: $\\checkmark\\ (1,1,2,2),\\ \\cancel{(1,2,2,2)},\\ \\checkmark\\ '
                              '(2,1,2,2),\\ \\cancel{(2,2,2,2)}$</li></ul>Why are $\\cancel{(2,2,1,2)},\\ '
                              '\\cancel{(1,2,2,2)},\\ \\cancel{(2,2,2,2)}$ crossed out? Because Bag $\\mathrm{B}$ has '
                              'only <b>one</b> ball labeled $2$ ($\\text{②}\\times 1$), so $y_1=2$ and $y_2=2$ cannot '
                              'both occur! Thus exactly $4$ mutually exclusive tuples survive.',
              'questions': [{'level_label': '여사건 순서쌍 소거 디딤돌 3',
                             'level_label_en': 'Complement Tuple Elimination Step 3',
                             'stem': '여사건의 $(x_1, y_1, x_2, y_2)$ 후보들 중에서 $\\cancel{(2, 2, 1, 2)}$, $\\cancel{(1, 2, '
                                     '2, 2)}$, $\\cancel{(2, 2, 2, 2)}$가 모두 지워지고 $\\mathrm{i})\\ (2,2,1,1)$, '
                                     '$\\mathrm{ii})\\ (2,2,2,1)$, $\\mathrm{iii})\\ (1,1,2,2)$, $\\mathrm{iv})\\ '
                                     '(2,1,2,2)$의 $4$가지만 살아남는 이유는?',
                             'stem_en': 'Why are $\\cancel{(2, 2, 1, 2)}$, $\\cancel{(1, 2, 2, 2)}$, and $\\cancel{(2, '
                                        '2, 2, 2)}$ crossed out, leaving only the $4$ tuples '
                                        '$\\mathrm{i})\\sim\\mathrm{iv})$?',
                             'options': ['주머니 $\\mathrm{B}$에 숫자 $2$가 적힌 공이 $1$개뿐이어서 $y_1 = 2$와 $y_2 = 2$가 동시에 나올 수 없기 '
                                         '때문',
                                         '주머니 $\\mathrm{A}$에 숫자 $2$가 적힌 공이 $1$개뿐이어서 $x_1 = 2$와 $x_2 = 2$가 동시에 나올 수 없기 '
                                         '때문',
                                         '주머니 $\\mathrm{A}$에 숫자 $1$이 적힌 공이 $1$개뿐이기 때문',
                                         '주머니 $\\mathrm{B}$에 숫자 $1$이 적힌 공이 $1$개뿐이기 때문',
                                         '꺼낸 공을 다시 주머니에 넣는 복원 추출이기 때문'],
                             'answer': 1,
                             'exp': '<b>[3단계 상세 해설]</b><br>• $a_1 = 2$가 되려면 $1$회차에 주머니 $\\mathrm{A}$와 주머니 '
                                    '$\\mathrm{B}$에서 <b>둘 다 숫자 $2$</b>를 꺼내야 합니다.<br>• <b>주머니 $\\mathrm{A}$ ($1$이 $3$개, '
                                    '$2$가 $2$개)</b>: $1$회차에 $2$를 뽑는 $2$가지 $\\times$ $2$회차에 남은 공 $4$개 중 아무거나 뽑는 $4$가지 '
                                    '$= 2 \\times 4 = 8$가지 (즉, $(2,1)$이 $2\\times 3=6$가지, $(2,2)$가 $2\\times 1=2$가지로 총 '
                                    '$8$가지)<br>• <b>주머니 $\\mathrm{B}$ ($1$이 $4$개, $2$가 $1$개)</b>: $1$회차에 유일한 $2$를 뽑는 '
                                    '$1$가지 $\\times$ $2$회차에 남은 $1$ 네 개 중 하나를 뽑는 $4$가지 $= 1 \\times 4 = 4$가지<br>• 따라서 '
                                    '$n(a_1 = 2) = 8 \\times 4 = \\mathbf{32}$가지입니다.',
                             'exp_en': '<b>[Step 3 Detailed Explanation]</b><br>For $a_1 = 2$, both bags must draw $2$ '
                                       'in Round 1. Bag A has $2 \\times 4 = 8$ ways ($(2,1)$ in $6$ ways + $(2,2)$ in '
                                       '$2$ ways) and Bag B has $1 \\times 4 = 4$ ways ($(2,1)$ in $4$ ways), giving '
                                       '$8 \\times 4 = \\mathbf{32}$ outcomes.'}]},
             {'title': '🌱 4단계 · [여사건 계산 $\\mathrm{i}), \\mathrm{ii})$] $x_1 = y_1 = 2$인 $(2, 2, 1, 1)$과 $(2, 2, 2, '
                       '1)$의 경우의 수($24$와 $8$)',
              'title_en': '🌱 Step 4 · [Complement Cases $\\mathrm{i}), \\mathrm{ii})$] Counting $(2, 2, 1, 1)$ and '
                          '$(2, 2, 2, 1)$ ($24$ and $8$)',
              'knowledge': '살아남은 $4$가지 여사건 순서쌍 중 앞의 두 가지 $\\mathrm{i}), \\mathrm{ii})$를 <b>$(x_1, y_1, x_2, y_2)$ 자리 '
                           '순서 그대로</b> 계산해 봅시다! (주머니 초기 상태: $\\mathrm{A}$는 $\\text{①}\\times 3, \\text{②}\\times 2$ / '
                           '$\\mathrm{B}$는 $\\text{①}\\times 4, \\text{②}\\times 1$)<ul><li><b>$\\mathrm{i})\\ (x_1, '
                           'y_1, x_2, y_2) = (2, 2, 1, 1)$</b>:<br>&nbsp;&nbsp;• $1$시행: $\\mathrm{A}$의 `②` $2$개 중 '
                           '$1$개(${}_2\\mathrm{C}_1$) $\\times$ $\\mathrm{B}$의 `②` $1$개 중 '
                           '$1$개(${}_1\\mathrm{C}_1$)<br>&nbsp;&nbsp;• $2$시행: 남은 $\\mathrm{A}_{x_1}$의 `①` $3$개 중 '
                           '$1$개(${}_3\\mathrm{C}_1$) $\\times$ 남은 $\\mathrm{B}_{y_1}$의 `①` $4$개 중 '
                           '$1$개(${}_4\\mathrm{C}_1$)<br>$$\\implies {}_2\\mathrm{C}_1 \\times {}_1\\mathrm{C}_1 '
                           '\\times {}_3\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 = 2 \\times 1 \\times 3 \\times 4 = '
                           '24$$</li><li><b>$\\mathrm{ii})\\ (x_1, y_1, x_2, y_2) = (2, 2, 2, '
                           '1)$</b>:<br>&nbsp;&nbsp;• $1$시행에 $\\mathrm{A}$에서 이미 `②`를 $1$개 꺼냈으므로, <b>$2$시행에서 '
                           '$\\mathrm{A}_{x_1}$에 남아 있는 `②`는 $1$개뿐(${}_1\\mathrm{C}_1$)</b>입니다!<br>$$\\implies '
                           '{}_2\\mathrm{C}_1 \\times {}_1\\mathrm{C}_1 \\times {}_1\\mathrm{C}_1 \\times '
                           '{}_4\\mathrm{C}_1 = 2 \\times 1 \\times 1 \\times 4 = 8$$</li></ul>',
              'knowledge_en': 'Using $\\mathrm{A}: (\\text{①}\\times 3,\\ \\text{②}\\times 2)$ and $\\mathrm{B}: '
                              '(\\text{①}\\times 4,\\ \\text{②}\\times 1)$, we multiply choices in the order $(x_1, '
                              'y_1, x_2, y_2)$:<ul><li><b>$\\mathrm{i})\\ (2, 2, 1, 1)$</b>: ${}_2\\mathrm{C}_1 '
                              '\\times {}_1\\mathrm{C}_1 \\times {}_3\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 = 2 '
                              '\\times 1 \\times 3 \\times 4 = 24$.</li><li><b>$\\mathrm{ii})\\ (2, 2, 2, 1)$</b>: '
                              'Since one ② was already drawn from $\\mathrm{A}$ in Round 1, only $1$ ball labeled ② '
                              'remains in $\\mathrm{A}_{x_1}$ (${}_1\\mathrm{C}_1$), giving ${}_2\\mathrm{C}_1 \\times '
                              '{}_1\\mathrm{C}_1 \\times {}_1\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 = 2 \\times 1 '
                              '\\times 1 \\times 4 = 8$.</li></ul>',
              'questions': [{'level_label': '여사건 i), ii) 계산 디딤돌 4',
                             'level_label_en': 'Complement Cases i), ii) Step 4',
                             'stem': '여사건 순서쌍 $\\mathrm{i})\\ (2, 2, 1, 1)$의 경우의 수 ${}_2\\mathrm{C}_1 \\times '
                                     '{}_1\\mathrm{C}_1 \\times {}_3\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1$과 '
                                     '$\\mathrm{ii})\\ (2, 2, 2, 1)$의 경우의 수 ${}_2\\mathrm{C}_1 \\times '
                                     '{}_1\\mathrm{C}_1 \\times {}_1\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1$을 바르게 짝지은 '
                                     '것은?',
                             'stem_en': 'What are the counts for $\\mathrm{i})\\ (2, 2, 1, 1)$ and $\\mathrm{ii})\\ '
                                        '(2, 2, 2, 1)$, respectively?',
                             'options': ['$\\mathrm{i})\\ 12,\\quad \\mathrm{ii})\\ 8$',
                                         '$\\mathrm{i})\\ 24,\\quad \\mathrm{ii})\\ 8$',
                                         '$\\mathrm{i})\\ 24,\\quad \\mathrm{ii})\\ 16$',
                                         '$\\mathrm{i})\\ 32,\\quad \\mathrm{ii})\\ 8$',
                                         '$\\mathrm{i})\\ 24,\\quad \\mathrm{ii})\\ 12$'],
                             'answer': 2,
                             'exp': '<b>[4단계 상세 해설]</b><br>• $2$회차에 $a_2 = 2$가 되는 경우: 주머니 $\\mathrm{A}$에서 $2$회차에 $2$를 '
                                    '뽑는 $8$가지($(1,2)$ $6$가지 + $(2,2)$ $2$가지) $\\times$ 주머니 $\\mathrm{B}$에서 $2$회차에 $2$를 '
                                    '뽑는 $4$가지($(1,2)$ $4$가지) $= 8 \\times 4 = 32$가지<br>• $a_1 = 2$이면서 동시에 $a_2 = 2$인 '
                                    '경우: 주머니 $\\mathrm{B}$에 숫자 $2$가 단 $1$개뿐이므로 $1, 2$회차 모두 $2$가 나올 수 없어 '
                                    '<b>$0$가지(배반사건)</b>입니다.<br>• 따라서 여사건에 의해 조건부확률의 분모는 $n(E) = 400 - (32 + 32 - 0) = '
                                    '400 - 64 = \\mathbf{336}$가지입니다.',
                             'exp_en': '<b>[Step 4 Detailed Explanation]</b><br>$a_2 = 2$ also occurs in $8 \\times 4 '
                                       '= 32$ ways, and $a_1 = a_2 = 2$ has $0$ ways because Bag B has only one $2$. '
                                       'Subtracting $32 + 32 = 64$ from $400$ yields $n(E) = \\mathbf{336}$.'}]},
             {'title': '🌱 5단계 · [여사건 계산 $\\mathrm{iii}), \\mathrm{iv})$ 및 분모 $\\mathrm{I})$ 확정] $400 - (24 + 8 + 24 + '
                       '8) = 336$ 구하기',
              'title_en': '🌱 Step 5 · [Complement Cases $\\mathrm{iii}), \\mathrm{iv})$ & Denominator $\\mathrm{I})$] '
                          'Computing $400 - (24 + 8 + 24 + 8) = 336$',
              'knowledge': '마찬가지로 $x_2 = y_2 = 2$인 나머지 두 여사건 순서쌍 $\\mathrm{iii}), \\mathrm{iv})$도 $(x_1, y_1, x_2, '
                           'y_2)$ 순서대로 계산합니다:<ul><li><b>$\\mathrm{iii})\\ (1, 1, 2, 2)$</b>: ${}_3\\mathrm{C}_1 '
                           '\\times {}_4\\mathrm{C}_1 \\times {}_2\\mathrm{C}_1 \\times {}_1\\mathrm{C}_1 = 3 \\times '
                           '4 \\times 2 \\times 1 = 24$</li><li><b>$\\mathrm{iv})\\ (2, 1, 2, 2)$</b>: ($1$시행에 '
                           '$\\mathrm{A}$에서 `②`를 $1$개 뽑았으므로 $2$시행 $\\mathrm{A}_{x_1}$에는 `②`가 $1$개 '
                           '남음)<br>$${}_2\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 \\times {}_1\\mathrm{C}_1 \\times '
                           '{}_1\\mathrm{C}_1 = 2 \\times 4 \\times 1 \\times 1 = 8$$</li></ul>이제 전체 경우의 수에서 여사건 '
                           '$4$가지를 빼면 <b>분모 $\\mathrm{I})\\ a_1 = a_2 = 1$의 경우의 수</b>가 확정됩니다:$${}_5\\mathrm{C}_1 '
                           '\\times {}_5\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 - (24 + 8 + '
                           '24 + 8) = 400 - 64 = 336$$',
              'knowledge_en': 'Counting the remaining two complement tuples in $(x_1, y_1, x_2, y_2)$ '
                              'order:<ul><li><b>$\\mathrm{iii})\\ (1, 1, 2, 2)$</b>: ${}_3\\mathrm{C}_1 \\times '
                              '{}_4\\mathrm{C}_1 \\times {}_2\\mathrm{C}_1 \\times {}_1\\mathrm{C}_1 = '
                              '24$.</li><li><b>$\\mathrm{iv})\\ (2, 1, 2, 2)$</b>: ${}_2\\mathrm{C}_1 \\times '
                              '{}_4\\mathrm{C}_1 \\times {}_1\\mathrm{C}_1 \\times {}_1\\mathrm{C}_1 = '
                              '8$.</li></ul>Subtracting all four from the total gives $\\mathrm{I})$: '
                              '${}_5\\mathrm{C}_1 \\times {}_5\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 \\times '
                              '{}_4\\mathrm{C}_1 - (24 + 8 + 24 + 8) = 400 - 64 = 336$.',
              'questions': [{'level_label': '분모 I) 확정 디딤돌 5',
                             'level_label_en': 'Denominator I) Total Step 5',
                             'stem': '전체 경우의 수 ${}_5\\mathrm{C}_1 \\times {}_5\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 '
                                     '\\times {}_4\\mathrm{C}_1 = 400$에서 여사건 $4$가지의 합 $(24 + 8 + 24 + 8) = 64$를 뺀, 조건 '
                                     '$\\mathrm{I})\\ a_1 = a_2 = 1$을 만족하는 분모의 경우의 수는?',
                             'stem_en': 'Subtracting $(24 + 8 + 24 + 8) = 64$ from ${}_5\\mathrm{C}_1 \\times '
                                        '{}_5\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 = 400$, '
                                        'what is the denominator count for $\\mathrm{I})\\ a_1 = a_2 = 1$?',
                             'options': ['$316$', '$324$', '$336$', '$344$', '$352$'],
                             'answer': 3,
                             'exp': '<b>[5단계 상세 해설]</b><br>• 처음 주머니 $\\mathrm{B}$에는 $1$이 $4$개, $2$가 $1$개 들어 있으므로, $2$번 '
                                    '시행 후 $\\mathrm{B}$에 $1$이 $3$개 남으려면 $\\mathrm{B}$에서 꺼낸 두 공이 <b>$1$ 한 개와 $2$ 한 '
                                    '개</b>여야 합니다.<br>• 그중 케이스 ①($\\mathrm{B}$가 $1$회차에 $1$, $2$회차에 $2$를 꺼내는 경우)은 $1$회차에 '
                                    '$4$개의 $1$ 중 하나를 고르고($4$가지), $2$회차에 유일한 $2$를 고르므로($1$가지) $4 \\times 1 = '
                                    '\\mathbf{4}$가지입니다.',
                             'exp_en': '<b>[Step 5 Detailed Explanation]</b><br>For three $1$s to remain in Bag B, Bag '
                                       'B must draw one $1$ and one $2$. In Case 1 ($\\mathrm{B}=(1, 2)$), there are '
                                       '$4$ choices for $1$ in Round 1 and $1$ choice for $2$ in Round 2, giving $4 '
                                       '\\times 1 = \\mathbf{4}$ ways.'}]},
             {'title': '🌳 6단계 · [분자 사건 $\\mathrm{II})$ 조건 번역] $\\mathrm{B}_{y_1, y_2}$에 ①이 $3$개 남을 조건 $(y_1, y_2) = '
                       '(1, 2),\\ (2, 1)$',
              'title_en': '🌳 Step 6 · [Numerator $\\mathrm{II})$ Condition] Condition on $(y_1, y_2)$ for three ①s to '
                          'remain in $\\mathrm{B}_{y_1, y_2}$',
              'knowledge': '이제 분자 사건 <b>$\\mathrm{II})\\ a_1 = a_2 = 1$ 이고 $2$시행 후 남은 주머니 $\\mathrm{B}_{y_1, y_2}$에 '
                           '`①`이 $3$개 들어 있는 경우</b>를 살펴봅시다!<ul><li>처음 주머니 $\\mathrm{B}$에는 <b>`①`이 $4$개, `②`가 $1$개</b> '
                           '들어 있었습니다.</li><li>$2$번 꺼낸 뒤 남은 주머니 $\\mathrm{B}_{y_1, y_2}$에 <b>`①`이 $3$개</b> 남으려면, 두 번의 '
                           '시행 동안 주머니 $\\mathrm{B}$에서 빠져나간 두 공 $(y_1, y_2)$에 <b>`①`이 $1$개($4 - 3 = 1$), `②`가 $1$개</b> '
                           '있어야 합니다!</li><li>따라서 주머니 $\\mathrm{B}$에서 꺼낸 수의 순서쌍 $(y_1, y_2)$는 반드시 다음 두 '
                           '가지뿐입니다:<br>$$(y_1, y_2) = (1, 2),\\ (2, 1)$$</li></ul>',
              'knowledge_en': 'Bag $\\mathrm{B}$ initially contains four ①s and one ②. For the remaining bag '
                              '$\\mathrm{B}_{y_1, y_2}$ after $2$ rounds to contain exactly three ①s, $\\mathrm{B}$ '
                              'must have drawn one ① and one ② across the two rounds:$$(y_1, y_2) = (1, 2),\\ (2, 1)$$',
              'questions': [{'level_label': '분자 II) 주머니 B 조건 디딤돌 6',
                             'level_label_en': 'Bag B Condition Step 6',
                             'stem': '처음에 `①`이 $4$개, `②`가 $1$개 들어 있던 주머니 $\\mathrm{B}$에서 $2$번 시행 후 남은 주머니 '
                                     '$\\mathrm{B}_{y_1, y_2}$에 `①`이 $3$개 남아 있으려면, $\\mathrm{B}$에서 꺼낸 두 수의 순서쌍 $(y_1, '
                                     'y_2)$는 무엇이어야 할까요?',
                             'stem_en': 'For $\\mathrm{B}_{y_1, y_2}$ to have three ①s remaining out of four ①s and '
                                        'one ②, what must $(y_1, y_2)$ be?',
                             'options': ['$(y_1, y_2) = (1, 1)$',
                                         '$(y_1, y_2) = (2, 2)$',
                                         '$(y_1, y_2) = (1, 2),\\ (2, 1)$',
                                         '$(y_1, y_2) = (1, 1),\\ (1, 2)$',
                                         '$(y_1, y_2) = (1, 1),\\ (2, 1)$'],
                             'answer': 3,
                             'exp': '<b>[6단계 상세 해설]</b><br>• $\\mathrm{B}=(1, 2)$일 때 $1$회차에는 $\\mathrm{B}$가 이미 $1$을 '
                                    '뽑았으므로 $a_1=1$이 자동 성립하고, $2$회차에는 $\\mathrm{B}$가 $2$를 뽑았으므로 $a_2=1$이 되려면 '
                                    '<b>$\\mathrm{A}$는 $2$회차에 반드시 $1$을 뽑아야 합니다.</b><br>• <b>[방법 1: 시행 순서대로 '
                                    '$1\\text{회차}\\to 2\\text{회차}$ 세기]</b> $\\mathrm{A}=(1, 1)$인 경우 $3 \\times 2 = '
                                    '6$가지 $+$ $\\mathrm{A}=(2, 1)$인 경우 $2 \\times 3 = 6$가지 $= 6 + 6 = '
                                    '\\mathbf{12}$가지<br>• <b>[방법 2: 조건이 걸린 $2$회차부터 고정하기]</b> $2$회차에 $1$을 고르는 $3$가지 '
                                    '$\\times$ $1$회차에 나머지 공 $4$개 중 하나를 고르는 $4$가지 $= 3 \\times 4 = \\mathbf{12}$가지',
                             'exp_en': '<b>[Step 6 Detailed Explanation]</b><br>When $\\mathrm{B}=(1, 2)$, Bag A must '
                                       'draw $1$ in Round 2. Method 1 (by Round 1): $\\mathrm{A}=(1, 1)$ gives $3 '
                                       '\\times 2 = 6$ ways and $\\mathrm{A}=(2, 1)$ gives $2 \\times 3 = 6$ ways, '
                                       'totaling $6 + 6 = \\mathbf{12}$ ways. Method 2 (fix Round 2 first): $3$ '
                                       'choices for Round 2 $\\times$ $4$ remaining balls for Round 1 $= \\mathbf{12}$ '
                                       'ways.'}]},
             {'title': '🌳 7단계 · [분자 계산 $\\mathrm{i})$] $(y_1, y_2) = (1, 2)$일 때 $(x_1, y_1, x_2, y_2) = (1, 1, 1, '
                       '2),\\ (2, 1, 1, 2)$의 경우의 수($48$)',
              'title_en': '🌳 Step 7 · [Numerator Case $\\mathrm{i})$] Counting $(1, 1, 1, 2)$ and $(2, 1, 1, 2)$ when '
                          '$(y_1, y_2) = (1, 2)$ ($48$)',
              'knowledge': '분자 $\\mathrm{II})$에서 첫 번째 경우인 <b>$\\mathrm{i})\\ (y_1, y_2) = (1, 2)$</b>일 때를 칠판 풀이 그대로 '
                           '따라가 봅시다!<ul><li>조건 $a_1 = a_2 = 1$은 <b>$(x_1 = 1\\text{ 또는 }y_1 = 1)$ 그리고 $(x_2 = 1\\text{ '
                           '또는 }y_2 = 1)$</b>입니다.</li><li>여기에 $y_1 = 1,\\ y_2 = 2$를 대입하면: $1$시행은 이미 $y_1 = 1$이므로 $x_1 '
                           '= 1, 2$가 모두 가능하지만, $2$시행은 $y_2 = 2$이므로 반드시 <b>$x_2 = 1$</b>이어야 합니다!</li><li>따라서 가능한 순서쌍 '
                           '$(x_1, y_1, x_2, y_2)$는 다음 두 가지입니다:<br>$$(x_1, y_1, x_2, y_2) = (1, 1, 1, 2),\\ (2, 1, 1, '
                           '2)$$</li><li>각 순서쌍의 경우의 수를 $(x_1, y_1, x_2, y_2)$ 자리 순서대로 구해 더하면:<br>&nbsp;&nbsp;• <b>$(1, '
                           '1, 1, 2)$</b>: $1$시행에 $\\mathrm{A}$에서 `①`($3$개)을 뽑았으므로 $2$시행 $\\mathrm{A}_{x_1}$에는 `①`이 '
                           '$2$개 남음 $\\to {}_3\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 \\times {}_2\\mathrm{C}_1 '
                           '\\times {}_1\\mathrm{C}_1 = 24$<br>&nbsp;&nbsp;• <b>$(2, 1, 1, 2)$</b>: $1$시행에 '
                           '$\\mathrm{A}$에서 `②`($2$개)를 뽑았으므로 $2$시행 $\\mathrm{A}_{x_1}$에는 `①`이 $3$개 그대로 남음 $\\to '
                           '{}_2\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 \\times {}_3\\mathrm{C}_1 \\times '
                           '{}_1\\mathrm{C}_1 = 24$<br>$${}_3\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 \\times '
                           '{}_2\\mathrm{C}_1 \\times {}_1\\mathrm{C}_1 + {}_2\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 '
                           '\\times {}_3\\mathrm{C}_1 \\times {}_1\\mathrm{C}_1 = 24 + 24 = '
                           '\\underline{48}$$</li></ul>',
              'knowledge_en': 'When $\\mathrm{i})\\ (y_1, y_2) = (1, 2)$, the condition $(x_1=1\\text{ or }y_1=1)$ and '
                              '$(x_2=1\\text{ or }y_2=1)$ allows $x_1 \\in \\{1, 2\\}$ and forces $x_2 = 1$, giving '
                              'two 4-tuples:$$(x_1, y_1, x_2, y_2) = (1, 1, 1, 2),\\ (2, 1, 1, 2)$$Counting in $(x_1, '
                              'y_1, x_2, y_2)$ order:$${}_3\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 \\times '
                              '{}_2\\mathrm{C}_1 \\times {}_1\\mathrm{C}_1 + {}_2\\mathrm{C}_1 \\times '
                              '{}_4\\mathrm{C}_1 \\times {}_3\\mathrm{C}_1 \\times {}_1\\mathrm{C}_1 = 24 + 24 = '
                              '\\underline{48}$$',
              'questions': [{'level_label': '분자 i) (y1,y2)=(1,2) 디딤돌 7',
                             'level_label_en': 'Numerator Case i) Step 7',
                             'stem': '$\\mathrm{i})\\ (y_1, y_2) = (1, 2)$일 때 가능한 두 순서쌍 $(x_1, y_1, x_2, y_2) = (1, 1, '
                                     '1, 2),\\ (2, 1, 1, 2)$의 경우의 수의 합 ${}_3\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 '
                                     '\\times {}_2\\mathrm{C}_1 \\times {}_1\\mathrm{C}_1 + {}_2\\mathrm{C}_1 \\times '
                                     '{}_4\\mathrm{C}_1 \\times {}_3\\mathrm{C}_1 \\times {}_1\\mathrm{C}_1$은?',
                             'stem_en': 'For $\\mathrm{i})\\ (y_1, y_2) = (1, 2)$, what is the sum of counts for $(1, '
                                        '1, 1, 2)$ and $(2, 1, 1, 2)$: ${}_3\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 '
                                        '\\times {}_2\\mathrm{C}_1 \\times {}_1\\mathrm{C}_1 + {}_2\\mathrm{C}_1 '
                                        '\\times {}_4\\mathrm{C}_1 \\times {}_3\\mathrm{C}_1 \\times '
                                        '{}_1\\mathrm{C}_1$?',
                             'options': ['$24$', '$36$', '$48$', '$60$', '$72$'],
                             'answer': 3,
                             'exp': '<b>[7단계 상세 해설]</b><br>• 주머니 $\\mathrm{B}$가 $(1, 2)$를 꺼내는 $4$가지 각각에 대하여, 주머니 '
                                    '$\\mathrm{A}$가 $(1, 1)$($6$가지) 또는 $(2, 1)$($6$가지)을 꺼내는 $12$가지가 짝지어집니다.<br>• 따라서 '
                                    '곱의 법칙에 의해 케이스 ①의 경우의 수는 $4 \\times 12 = \\mathbf{48}$가지(즉, $4\\times 6 + 4\\times '
                                    '6 = 24 + 24 = 48$가지)입니다.',
                             'exp_en': '<b>[Step 7 Detailed Explanation]</b><br>Each of the $4$ ways for Bag B to draw '
                                       '$(1, 2)$ pairs with $12$ valid ways for Bag A ($6$ ways for $(1,1)$ + $6$ ways '
                                       'for $(2,1)$), giving $4 \\times 12 = \\mathbf{48}$ outcomes.'}]},
             {'title': '🌳 8단계 · [분자 계산 $\\mathrm{ii})$와 분자 확정] $(y_1, y_2) = (2, 1)$일 때 $(1, 2, 1, 1),\\ (1, 2, 2, '
                       '1)$의 경우의 수($48$)와 합($96$)',
              'title_en': '🌳 Step 8 · [Numerator Case $\\mathrm{ii})$ & Total] Counting $(1, 2, 1, 1)$ and $(1, 2, 2, '
                          '1)$ when $(y_1, y_2) = (2, 1)$ ($48$) to get $96$',
              'knowledge': '이제 분자 $\\mathrm{II})$의 두 번째 경우인 <b>$\\mathrm{ii})\\ (y_1, y_2) = (2, 1)$</b>일 때를 계산해 '
                           '봅시다!<ul><li>$y_1 = 2,\\ y_2 = 1$이므로, $(x_1 = 1\\text{ 또는 }y_1 = 1)$이 성립하려면 반드시 <b>$x_1 = '
                           '1$</b>이어야 하고, $2$시행은 이미 $y_2 = 1$이므로 $x_2 = 1, 2$가 모두 가능합니다!</li><li>따라서 가능한 순서쌍 $(x_1, '
                           'y_1, x_2, y_2)$는 다음 두 가지입니다:<br>$$(x_1, y_1, x_2, y_2) = (1, 2, 1, 1),\\ (1, 2, 2, '
                           '1)$$</li><li>각 순서쌍의 경우의 수를 $(x_1, y_1, x_2, y_2)$ 자리 순서대로 구해 더하면:<br>&nbsp;&nbsp;• <b>$(1, '
                           '2, 1, 1)$</b>: $1$시행에 $\\mathrm{A}$에서 `①`($3$개)을 뽑았으므로 $2$시행 $\\mathrm{A}_{x_1}$에는 `①`이 '
                           '$2$개 남음 $\\to {}_3\\mathrm{C}_1 \\times {}_1\\mathrm{C}_1 \\times {}_2\\mathrm{C}_1 '
                           '\\times {}_4\\mathrm{C}_1 = 24$<br>&nbsp;&nbsp;• <b>$(1, 2, 2, 1)$</b>: $1$시행에 '
                           '$\\mathrm{A}$에서 `①`($3$개)을 뽑았으므로 $2$시행 $\\mathrm{A}_{x_1}$에는 `②`가 $2$개 그대로 남음 $\\to '
                           '{}_3\\mathrm{C}_1 \\times {}_1\\mathrm{C}_1 \\times {}_2\\mathrm{C}_1 \\times '
                           '{}_4\\mathrm{C}_1 = 24$<br>$${}_3\\mathrm{C}_1 \\times {}_1\\mathrm{C}_1 \\times '
                           '{}_2\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 + {}_3\\mathrm{C}_1 \\times {}_1\\mathrm{C}_1 '
                           '\\times {}_2\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 = 24 + 24 = '
                           '\\underline{48}$$</li></ul>그러므로 분자 $\\mathrm{II})$의 전체 경우의 수는 $\\mathrm{i})\\ 48 + '
                           '\\mathrm{ii})\\ 48 = 96$입니다!',
              'knowledge_en': 'When $\\mathrm{ii})\\ (y_1, y_2) = (2, 1)$, the condition forces $x_1 = 1$ and allows '
                              '$x_2 \\in \\{1, 2\\}$, giving two 4-tuples:$$(x_1, y_1, x_2, y_2) = (1, 2, 1, 1),\\ (1, '
                              '2, 2, 1)$$Counting in $(x_1, y_1, x_2, y_2)$ order:$${}_3\\mathrm{C}_1 \\times '
                              '{}_1\\mathrm{C}_1 \\times {}_2\\mathrm{C}_1 \\times {}_4\\mathrm{C}_1 + '
                              '{}_3\\mathrm{C}_1 \\times {}_1\\mathrm{C}_1 \\times {}_2\\mathrm{C}_1 \\times '
                              '{}_4\\mathrm{C}_1 = 24 + 24 = \\underline{48}$$Combining $\\mathrm{i})$ and '
                              '$\\mathrm{ii})$ gives the total numerator $48 + 48 = 96$.',
              'questions': [{'level_label': '분자 ii) 및 분자 총합 디딤돌 8',
                             'level_label_en': 'Numerator Case ii) & Total Step 8',
                             'stem': '$\\mathrm{ii})\\ (y_1, y_2) = (2, 1)$일 때 $(1, 2, 1, 1),\\ (1, 2, 2, 1)$의 경우의 수의 '
                                     '합($48$)과 앞선 $\\mathrm{i})$의 경우의 수($48$)를 더한 분자 $\\mathrm{II})$의 총 경우의 수는?',
                             'stem_en': 'Adding $\\mathrm{i})$ ($48$ ways) and $\\mathrm{ii})$ ($48$ ways), what is '
                                        'the total count for the numerator $\\mathrm{II})$?',
                             'options': ['$72$', '$84$', '$96$', '$108$', '$120$'],
                             'answer': 3,
                             'exp': '<b>[8단계 상세 해설]</b><br>• 케이스 ②($\\mathrm{B}=(2, 1)$)에서 주머니 $\\mathrm{B}$의 가짓수는 $1 '
                                    '\\times 4 = 4$가지이고, $1$회차에 $a_1=1$이 되려면 주머니 $\\mathrm{A}$는 $1$회차에 반드시 $1$을 뽑아야 '
                                    '하므로 $\\mathrm{A}=(1, 1)$($6$가지) $+$ $\\mathrm{A}=(1, 2)$($6$가지) $= 12$가지입니다.<br>• '
                                    '따라서 케이스 ②의 가짓수도 $4 \\times 12 = 48$가지이며, 케이스 ①과 케이스 ②는 배반이므로 합의 법칙에 의해 분자는 $n(E '
                                    '\\cap F) = 48 + 48 = \\mathbf{96}$가지입니다.',
                             'exp_en': '<b>[Step 8 Detailed Explanation]</b><br>In Case 2 ($\\mathrm{B}=(2, 1)$, $1 '
                                       '\\times 4 = 4$ ways), Bag A must draw $1$ in Round 1 ($\\mathrm{A}=(1,1)$ in '
                                       '$6$ ways + $\\mathrm{A}=(1,2)$ in $6$ ways $= 12$ ways), giving $4 \\times 12 '
                                       '= 48$ ways. Summing Case 1 and Case 2 gives $n(E \\cap F) = 48 + 48 = '
                                       '\\mathbf{96}$.'}]},
             {'title': '💎 9단계 · [$\\text{by }\\mathrm{I})\\ \\mathrm{II})$ 조건부확률과 단계별 약분] $\\dfrac{96}{336} = '
                       '\\dfrac{12}{42} = \\dfrac{2}{7}$ 구하기',
              'title_en': '💎 Step 9 · [$\\text{by }\\mathrm{I})\\ \\mathrm{II})$ Reduction] Reducing $\\dfrac{96}{336} '
                          '= \\dfrac{12}{42} = \\dfrac{2}{7}$',
              'knowledge': '드디어 $\\mathrm{I})$에서 구한 분모 $336$과 $\\mathrm{II})$에서 구한 분자 $96$을 결합할 차례입니다! 칠판의 약분 과정을 그대로 '
                           '따라가 볼까요?<ul><li>여사건에서 뺀 숫자들을 보면 $24 + 8 + 24 + 8 = 8 \\times (3 + 1 + 3 + 1)$이고, 전체 $400 = '
                           '8 \\times 50$, 분자 $96 = 8 \\times 12$이므로 <b>모든 수가 $8$의 배수</b>입니다!</li><li>먼저 분자와 분모를 '
                           '<b>$8$</b>로 약분하면: $96 \\div 8 = 12$, $336 \\div 8 = 42$이므로 $\\dfrac{12}{42}$가 '
                           '됩니다.</li><li>다시 분자와 분모를 <b>$6$</b>으로 약분하면: $12 \\div 6 = 2$, $42 \\div 6 = 7$이므로 기약분수 '
                           '<b>$\\dfrac{2}{7}$</b>이 됩니다!</li></ul>$$\\text{by }\\mathrm{I})\\ \\mathrm{II}) \\quad '
                           '\\frac{96}{336} = \\frac{12}{42} = \\frac{2}{7}$$',
              'knowledge_en': 'Combining $\\mathrm{I})$ ($336$) and $\\mathrm{II})$ ($96$) and reducing first by $8$ '
                              'and then by $6$:$$\\text{by }\\mathrm{I})\\ \\mathrm{II}) \\quad \\frac{96}{336} = '
                              '\\frac{12}{42} = \\frac{2}{7}$$',
              'questions': [{'level_label': 'by I) II) 약분 디딤돌 9',
                             'level_label_en': 'by I) II) Reduction Step 9',
                             'stem': '$\\text{by }\\mathrm{I})\\ \\mathrm{II})$에 의해 구하는 확률 $\\dfrac{96}{336}$을 먼저 $8$로 '
                                     '약분해 $\\dfrac{12}{42}$로 만든 뒤, 다시 $6$으로 약분하여 기약분수 $\\dfrac{q}{p}$로 나타내면?',
                             'stem_en': 'Reducing $\\dfrac{96}{336}$ by $8$ to $\\dfrac{12}{42}$ and then by $6$, what '
                                        'is the fraction $\\dfrac{q}{p}$ in lowest terms?',
                             'options': ['$\\frac{1}{4}$',
                                         '$\\frac{2}{7}$',
                                         '$\\frac{3}{8}$',
                                         '$\\frac{2}{9}$',
                                         '$\\frac{3}{11}$'],
                             'answer': 2,
                             'exp': '<b>[9단계 상세 해설]</b><br>• 조건부확률 $\\mathrm{P}(F \\mid E) = \\dfrac{n(E \\cap '
                                    'F)}{n(E)} = \\dfrac{96}{336}$입니다.<br>• 분자와 분모를 먼저 $16$으로 나누면 $\\dfrac{96 \\div '
                                    '16}{336 \\div 16} = \\dfrac{6}{21}$이고, 다시 $3$으로 나누면(즉 최대공약수 $48$로 약분하면) 기약분수 '
                                    '<b>$\\dfrac{2}{7}$</b>이 됩니다.<br>• 따라서 서로소인 두 자연수는 $p = 7$, $q = 2$입니다.',
                             'exp_en': '<b>[Step 9 Detailed Explanation]</b><br>$\\mathrm{P}(F \\mid E) = '
                                       '\\dfrac{96}{336} = \\dfrac{96 \\div 16}{336 \\div 16} = \\dfrac{6}{21} = '
                                       '\\mathbf{\\dfrac{2}{7}}$, so $p = 7$ and $q = 2$.'}]},
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
                             'exp': '<b>[10단계 상세 해설]</b><br>• 전체 경우의 수 $n(S) = 20 \\times 20 = 400$가지<br>• 분모 $n(E) = '
                                    '400 - (32 + 32) = 336$가지<br>• 분자 $n(E \\cap F) = 48 + 48 = 96$가지<br>• 조건부확률 '
                                    '$\\dfrac{q}{p} = \\dfrac{96}{336} = \\dfrac{2}{7}$이므로 $p = 7,\\ q = 2$이고, 구하는 값은 '
                                    '$p + q = 7 + 2 = \\mathbf{9}$입니다.',
                             'exp_en': '<b>[Step 10 Detailed Explanation]</b><br>From $n(S) = 400$, $n(E) = 336$, and '
                                       '$n(E \\cap F) = 96$, we obtain $\\dfrac{q}{p} = \\dfrac{96}{336} = '
                                       '\\dfrac{2}{7}$, so $p + q = 7 + 2 = \\mathbf{9}$.'}]}],
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
                   '4)=32$가지)와 $a_2=2$인 경우($32$가지, 중복 $0$가지)를 제외한 분모는 $n(E) = 400 - 64 = 336$가지입니다. 이 중 $\\mathrm{B}$에 '
                   '$1$이 $3$개 남으려면 $\\mathrm{B}$가 $(1,2)$ 또는 $(2,1)$을 뽑아야 하며, 각 경우 $\\mathrm{B}$의 $4$가지에 대하여 '
                   '$\\mathrm{A}$가 $(1,1)$($6$가지) 또는 $(2,1)$·$(1,2)$($6$가지)로 총 $12$가지씩 성립하므로 분자는 $n(E \\cap F) = '
                   '(4\\times 12) + (4\\times 12) = 48 + 48 = 96$가지입니다. 따라서 조건부확률은 $\\dfrac{96}{336} = '
                   '\\dfrac{2}{7}$이고 $p+q=7+2=9$입니다.',
            'exp_en': 'Out of $20 \\times 20 = 400$ equally likely ordered outcomes, excluding $a_1=2$ ($8 \\times 4 = '
                      '32$) and $a_2=2$ ($32$, zero overlap) leaves $n(E) = 336$ outcomes where $a_1=a_2=1$. Leaving '
                      'three $1$s in B requires B to draw $(1,2)$ ($4$ ways) or $(2,1)$ ($4$ ways), each pairing with '
                      '$12$ valid ways in A ($6+6$), giving $n(E \\cap F) = 48 + 48 = 96$. Thus $\\dfrac{96}{336} = '
                      '\\dfrac{2}{7}$ and $p+q = 9$.',
            'solution': '<h4>📋 [1. 문제 조건 완벽 해부 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 확률과 통계 30번 최고난도 문항으로, <b>비복원 추출에서의 여사건을 활용한 조건부확률 $\\mathrm{P}(F \\mid E) = '
                        '\\dfrac{\\mathrm{P}(E \\cap F)}{\\mathrm{P}(E)} = \\dfrac{n(E \\cap F)}{n(E)}$</b>을 정확하게 구하는 '
                        '문제입니다.</p>\n'
                        '<ul>\n'
                        '  <li><b>주머니 초기 상태</b>: 주머니 $\\mathrm{A}$에는 숫자 $1$이 $3$개, 숫자 $2$가 $2$개(총 $5$개), 주머니 '
                        '$\\mathrm{B}$에는 숫자 $1$이 $4$개, 숫자 $2$가 $1$개(총 $5$개) 들어 있습니다.</li>\n'
                        '  <li><b>비복원 $2$회 추출</b>: 꺼낸 공은 다시 넣지 않으므로 $1$회차에 공을 꺼내면 $2$회차에는 남은 $4$개의 공 중에서 $1$개를 꺼내게 '
                        '됩니다.</li>\n'
                        "  <li><b>$a_n$의 의미 번역 ('두 수 중 크지 않은 수')</b>: $n$회차($n=1, 2$)에 주머니 $\\mathrm{A}, "
                        '\\mathrm{B}$에서 꺼낸 공의 숫자를 각각 $\\mathrm{A}_n, \\mathrm{B}_n$이라 하면 $a_n = \\min(\\mathrm{A}_n, '
                        '\\mathrm{B}_n)$입니다.<br>\n'
                        '    &nbsp;&nbsp;• $(1, 1) \\to 1$, &nbsp;$(1, 2) \\to 1$, &nbsp;$(2, 1) \\to 1$, &nbsp;$(2, '
                        '2) \\to 2$<br>\n'
                        '    &nbsp;&nbsp;• 즉, <b>적어도 한 주머니에서 $1$이 나오면 무조건 $a_n = 1$</b>이고, 오직 <b>두 주머니 모두 $2$를 꺼낸 $(2, '
                        '2)$일 때만 $a_n = 2$</b>가 됩니다!</li>\n'
                        '  <li><b>사건 정의</b>:<br>\n'
                        '    &nbsp;&nbsp;• <b>조건 사건 $E$ (분모)</b>: $a_1 = 1$이고 $a_2 = 1$인 사건 (즉, $1$회차에도 $(2, 2)$가 안 '
                        '나오고 $2$회차에도 $(2, 2)$가 안 나오는 사건)<br>\n'
                        '    &nbsp;&nbsp;• <b>목표 사건 $F$</b>: $2$번째 시행 후 주머니 $\\mathrm{B}$에 숫자 $1$이 적힌 공이 $3$개 남아 있는 '
                        '사건</li>\n'
                        '</ul>\n'
                        '\n'
                        '<h4>🔍 [2. 예비 단계: 왜 같은 숫자의 공을 구별해야 하며, 각 주머니의 $20$가지는 어떻게 나뉠까?]</h4>\n'
                        '<p>주머니 안에 $1$과 $2$의 개수가 다르므로, 단순히 숫자 순서쌍 $(1,1), (1,2)$만 세면 각 순서쌍이 일어날 확률이 서로 다릅니다. 모든 근원사건이 '
                        '<b>동등한 가능성($\\dfrac{1}{400}$)</b>을 갖도록 하려면 같은 숫자가 적힌 공이라도 번호표를 붙여 서로 다른 공으로 구별해야 합니다:<br>\n'
                        '$$\\mathrm{A} = \\{1_a,\\ 1_b,\\ 1_c,\\ 2_a,\\ 2_b\\}, \\qquad \\mathrm{B} = \\{1_p,\\ 1_q,\\ '
                        '1_r,\\ 1_s,\\ 2_p\\}$$</p>\n'
                        '<ul>\n'
                        '  <li><b>주머니 $\\mathrm{A}$ ($1$이 $3$개, $2$가 $2$개)에서 $2$번 연속 꺼내는 $5 \\times 4 = 20$가지의 완전 '
                        '분해</b>:\n'
                        '    <ul>\n'
                        '      <li>① $\\mathrm{A} = (1, 1)$ ($1$회차 $1$, $2$회차 $1$): $1$회차에 $3$개의 $1$ 중 하나($3$가지) '
                        '$\\times$ $2$회차에 남은 $2$개의 $1$ 중 하나($2$가지) $= 3 \\times 2 = \\mathbf{6}\\text{가지}$</li>\n'
                        '      <li>② $\\mathrm{A} = (1, 2)$ ($1$회차 $1$, $2$회차 $2$): $1$회차에 $3$개의 $1$ 중 하나($3$가지) '
                        '$\\times$ $2$회차에 $2$개의 $2$ 중 하나($2$가지) $= 3 \\times 2 = \\mathbf{6}\\text{가지}$</li>\n'
                        '      <li>③ $\\mathrm{A} = (2, 1)$ ($1$회차 $2$, $2$회차 $1$): $1$회차에 $2$개의 $2$ 중 하나($2$가지) '
                        '$\\times$ $2$회차에 $3$개의 $1$ 중 하나($3$가지) $= 2 \\times 3 = \\mathbf{6}\\text{가지}$</li>\n'
                        '      <li>④ $\\mathrm{A} = (2, 2)$ ($1$회차 $2$, $2$회차 $2$): $1$회차에 $2$개의 $2$ 중 하나($2$가지) '
                        '$\\times$ $2$회차에 남은 $1$개의 $2$($1$가지) $= 2 \\times 1 = \\mathbf{2}\\text{가지}$</li>\n'
                        '      <li><i>(합계 검산: $6 + 6 + 6 + 2 = 20$가지)</i></li>\n'
                        '    </ul>\n'
                        '  </li>\n'
                        '  <li><b>주머니 $\\mathrm{B}$ ($1$이 $4$개, $2$가 $1$개)에서 $2$번 연속 꺼내는 $5 \\times 4 = 20$가지의 완전 '
                        '분해</b>:\n'
                        '    <ul>\n'
                        '      <li>① $\\mathrm{B} = (1, 1)$ ($1$회차 $1$, $2$회차 $1$): $1$회차에 $4$개의 $1$ 중 하나($4$가지) '
                        '$\\times$ $2$회차에 남은 $3$개의 $1$ 중 하나($3$가지) $= 4 \\times 3 = \\mathbf{12}\\text{가지}$</li>\n'
                        '      <li>② $\\mathrm{B} = (1, 2)$ ($1$회차 $1$, $2$회차 $2$): $1$회차에 $4$개의 $1$ 중 하나($4$가지) '
                        '$\\times$ $2$회차에 유일한 $2$($1$가지) $= 4 \\times 1 = \\mathbf{4}\\text{가지}$</li>\n'
                        '      <li>③ $\\mathrm{B} = (2, 1)$ ($1$회차 $2$, $2$회차 $1$): $1$회차에 유일한 $2$($1$가지) $\\times$ '
                        '$2$회차에 $4$개의 $1$ 중 하나($4$가지) $= 1 \\times 4 = \\mathbf{4}\\text{가지}$</li>\n'
                        '      <li>④ $\\mathrm{B} = (2, 2)$ ($1$회차 $2$, $2$회차 $2$): 주머니 $\\mathrm{B}$에는 $2$가 적힌 공이 '
                        '<b>단 $1$개뿐</b>이므로 비복원 추출에서 두 번 연속 $2$가 나오는 경우는 $\\mathbf{0}\\text{가지(불가능)}$</li>\n'
                        '      <li><i>(합계 검산: $12 + 4 + 4 + 0 = 20$가지)</i></li>\n'
                        '    </ul>\n'
                        '  </li>\n'
                        '  <li><b>전체 근원사건의 수 $n(S)$</b>: 두 주머니에서 동시에 시행하므로 곱의 법칙에 의해\n'
                        '    $$n(S) = 20 \\times 20 = \\mathbf{400}\\text{가지}$$</li>\n'
                        '</ul>\n'
                        '\n'
                        '<h4>📐 [3. 단계별 상세 풀이 ①: 조건부확률의 분모 $n(E) = 336$ 구하기]</h4>\n'
                        '<p>사건 $E$ ($a_1 = 1$이고 $a_2 = 1$)의 경우의 수는 전체 $400$가지에서 <b>여사건 $E^c$ ($a_1 = 2$ 또는 $a_2 = 2$가 '
                        '되어 탈락하는 경우)</b>를 빼서 구합니다.</p>\n'
                        '<ul>\n'
                        '  <li><b>(탈락 1) $1$회차에 $a_1 = 2$인 경우 ($\\mathrm{A}_1 = 2$이고 $\\mathrm{B}_1 = 2$)</b>:\n'
                        '    <ul>\n'
                        '      <li>주머니 $\\mathrm{A}$가 $1$회차에 $2$를 꺼내는 가짓수: 위 분해표에서 $\\mathrm{A}=(2,1)$인 $6$가지 $+$ '
                        '$\\mathrm{A}=(2,2)$인 $2$가지 $= \\mathbf{8}\\text{가지}$<br>\n'
                        '        <i>(또는 $1$회차에 $2$인 공 $2$개 중 택1($2$가지) $\\times$ $2$회차에 남은 공 $4$개 중 택1($4$가지) $= 2 '
                        '\\times 4 = 8$가지)</i></li>\n'
                        '      <li>주머니 $\\mathrm{B}$가 $1$회차에 $2$를 꺼내는 가짓수: 위 분해표에서 $\\mathrm{B}=(2,1)$인 '
                        '$\\mathbf{4}\\text{가지}$<br>\n'
                        '        <i>(또는 $1$회차에 유일한 $2$ 택1($1$가지) $\\times$ $2$회차에 남은 공 $4$개 중 택1($4$가지) $= 1 \\times 4 '
                        '= 4$가지)</i></li>\n'
                        '      <li>따라서 $n(a_1 = 2) = 8 \\times 4 = \\mathbf{32}\\text{가지}$입니다.</li>\n'
                        '    </ul>\n'
                        '  </li>\n'
                        '  <li><b>(탈락 2) $2$회차에 $a_2 = 2$인 경우 ($\\mathrm{A}_2 = 2$이고 $\\mathrm{B}_2 = 2$)</b>:\n'
                        '    <ul>\n'
                        '      <li>주머니 $\\mathrm{A}$가 $2$회차에 $2$를 꺼내는 가짓수: 위 분해표에서 $\\mathrm{A}=(1,2)$인 $6$가지 $+$ '
                        '$\\mathrm{A}=(2,2)$인 $2$가지 $= \\mathbf{8}\\text{가지}$<br>\n'
                        '        <i>(또는 $2$회차에 $2$인 공 $2$개 중 택1($2$가지) $\\times$ $1$회차에 남은 공 $4$개 중 택1($4$가지) $= 2 '
                        '\\times 4 = 8$가지)</i></li>\n'
                        '      <li>주머니 $\\mathrm{B}$가 $2$회차에 $2$를 꺼내는 가짓수: 위 분해표에서 $\\mathrm{B}=(1,2)$인 '
                        '$\\mathbf{4}\\text{가지}$<br>\n'
                        '        <i>(또는 $2$회차에 유일한 $2$ 택1($1$가지) $\\times$ $1$회차에 남은 공 $4$개 중 택1($4$가지) $= 1 \\times 4 '
                        '= 4$가지)</i></li>\n'
                        '      <li>따라서 $n(a_2 = 2) = 8 \\times 4 = \\mathbf{32}\\text{가지}$입니다.</li>\n'
                        '    </ul>\n'
                        '  </li>\n'
                        '  <li><b>(중복 확인) $a_1 = 2$이면서 동시에 $a_2 = 2$인 경우</b>:\n'
                        '    <ul>\n'
                        '      <li>두 회차 모두 $2$가 되려면 주머니 $\\mathrm{B}$에서도 $1, 2$회차 연속으로 $2$를 뽑아야 하지만, 주머니 '
                        '$\\mathrm{B}$에는 $2$가 단 $1$개뿐이므로 $\\mathrm{B}=(2,2)$는 $0$가지입니다.</li>\n'
                        '      <li>즉, $n(a_1 = 2 \\cap a_2 = 2) = \\mathbf{0}$ (두 사건은 배반사건)입니다.</li>\n'
                        '    </ul>\n'
                        '  </li>\n'
                        '</ul>\n'
                        '<p>따라서 조건부확률의 분모 $n(E)$는:\n'
                        '$$n(E) = 400 - (32 + 32 - 0) = 400 - 64 = \\mathbf{336}\\text{가지}$$</p>\n'
                        '\n'
                        '<h4>🎯 [4. 단계별 상세 풀이 ②: 조건부확률의 분자 $n(E \\cap F) = 96$ 구하기]</h4>\n'
                        '<p>사건 $E \\cap F$는 <b>"$a_1 = 1$이고 $a_2 = 1$이면서, 동시에 $2$번 시행 후 주머니 $\\mathrm{B}$에 숫자 $1$이 적힌 '
                        '공이 $3$개 남아 있는 사건"</b>입니다.<br>\n'
                        '처음에 주머니 $\\mathrm{B}$에는 숫자 $1$이 $4$개, 숫자 $2$가 $1$개 있었으므로, $2$번 꺼낸 후 $\\mathrm{B}$에 숫자 $1$이 '
                        '$3$개 남으려면 $2$번의 시행 동안 <b>주머니 $\\mathrm{B}$에서 숫자 $1$이 정확히 $1$개($4-3=1$), 숫자 $2$가 정확히 $1$개 '
                        '빠져나가야 합니다.</b><br>\n'
                        '즉, 주머니 $\\mathrm{B}$의 $(1\\text{회차}, 2\\text{회차})$ 추출 결과는 반드시 <b>[케이스 ①] $\\mathrm{B} = (1, '
                        '2)$</b> 이거나 <b>[케이스 ②] $\\mathrm{B} = (2, 1)$</b> 두 가지뿐입니다.</p>\n'
                        '<ul>\n'
                        '  <li><b>[케이스 ①] 주머니 $\\mathrm{B}$가 $1$회차에 $1$, $2$회차에 $2$를 꺼내는 경우 ($\\mathrm{B} = (1, '
                        '2)$)</b>:\n'
                        '    <ol>\n'
                        '      <li><b>주머니 $\\mathrm{B}$의 가짓수</b>: $1$회차에 $4$개의 $1$ 중 하나($4$가지) $\\times$ $2$회차에 유일한 '
                        '$2$($1$가지) $= 4 \\times 1 = \\mathbf{4}\\text{가지}$</li>\n'
                        '      <li><b>주머니 $\\mathrm{A}$의 조건 해석</b>:\n'
                        '        <br>&nbsp;&nbsp;• <b>$1$회차</b>: 주머니 $\\mathrm{B}$가 이미 $1$을 뽑았으므로($\\mathrm{B}_1 = '
                        '1$), 주머니 $\\mathrm{A}$가 $1$회차에 $1$을 뽑든 $2$를 뽑든 $a_1 = \\min(\\mathrm{A}_1, 1) = 1$이 무조건 '
                        '성립합니다.\n'
                        '        <br>&nbsp;&nbsp;• <b>$2$회차</b>: 주머니 $\\mathrm{B}$가 $2$를 뽑았으므로($\\mathrm{B}_2 = 2$), '
                        '만약 $\\mathrm{A}$도 $2$회차에 $2$를 뽑으면 $a_2 = \\min(2, 2) = 2$가 되어 탈락합니다! 따라서 $a_2 = 1$이 되려면 '
                        '<b>주머니 $\\mathrm{A}$는 $2$회차에 반드시 숫자 $1$을 꺼내야 합니다 ($\\mathrm{A}_2 = 1$)!</b></li>\n'
                        '      <li><b>주머니 $\\mathrm{A}$에서 $\\mathrm{A}_2 = 1$이 되는 가짓수($12$가지)를 구하는 두 가지 방법</b>:\n'
                        '        <br>&nbsp;&nbsp;• <b>[방법 A: 시행 순서대로 $1\\text{회차} \\to 2\\text{회차}$ 나누어 세기]</b>\n'
                        '        <br>&nbsp;&nbsp;&nbsp;&nbsp;- (가) $\\mathrm{A}$가 $1$회차에 $1$, $2$회차에도 $1$을 뽑는 경우 '
                        '$\\mathrm{A} = (1, 1)$: $3 \\times 2 = 6$가지\n'
                        '        <br>&nbsp;&nbsp;&nbsp;&nbsp;- (나) $\\mathrm{A}$가 $1$회차에 $2$, $2$회차에 $1$을 뽑는 경우 '
                        '$\\mathrm{A} = (2, 1)$: $2 \\times 3 = 6$가지\n'
                        '        <br>&nbsp;&nbsp;&nbsp;&nbsp;- 합하면 $6 + 6 = \\mathbf{12}\\text{가지}$!\n'
                        '        <br>&nbsp;&nbsp;• <b>[방법 B: 조건이 걸린 $2$회차를 먼저 고정하고 세기]</b>\n'
                        '        <br>&nbsp;&nbsp;&nbsp;&nbsp;- $2$회차에 들어갈 숫자 $1$인 공($3$개 중 하나)을 먼저 고르는 방법: $3$가지\n'
                        '        <br>&nbsp;&nbsp;&nbsp;&nbsp;- $1$회차에는 방금 고른 공을 제외한 나머지 $4$개의 공 중 아무거나 고르는 방법: $4$가지\n'
                        '        <br>&nbsp;&nbsp;&nbsp;&nbsp;- 곱하면 $3 \\times 4 = \\mathbf{12}\\text{가지}$!</li>\n'
                        '      <li><b>케이스 ①의 경우의 수</b>: $(\\text{주머니 B의 } 4\\text{가지}) \\times (\\text{주머니 A의 } '
                        '12\\text{가지}) = 4 \\times 12 = \\mathbf{48}\\text{가지}$</li>\n'
                        '    </ol>\n'
                        '  </li>\n'
                        '  <li><b>[케이스 ②] 주머니 $\\mathrm{B}$가 $1$회차에 $2$, $2$회차에 $1$을 꺼내는 경우 ($\\mathrm{B} = (2, '
                        '1)$)</b>:\n'
                        '    <ol>\n'
                        '      <li><b>주머니 $\\mathrm{B}$의 가짓수</b>: $1$회차에 유일한 $2$($1$가지) $\\times$ $2$회차에 $4$개의 $1$ 중 '
                        '하나($4$가지) $= 1 \\times 4 = \\mathbf{4}\\text{가지}$</li>\n'
                        '      <li><b>주머니 $\\mathrm{A}$의 조건 해석</b>:\n'
                        '        <br>&nbsp;&nbsp;• <b>$1$회차</b>: 이번에는 주머니 $\\mathrm{B}$가 $1$회차에 $2$를 '
                        '뽑았으므로($\\mathrm{B}_1 = 2$), $a_1 = 1$이 되려면 <b>주머니 $\\mathrm{A}$는 $1$회차에 반드시 숫자 $1$을 꺼내야 합니다 '
                        '($\\mathrm{A}_1 = 1$)!</b>\n'
                        '        <br>&nbsp;&nbsp;• <b>$2$회차</b>: 주머니 $\\mathrm{B}$가 $2$회차에 $1$을 뽑았으므로($\\mathrm{B}_2 = '
                        '1$), $\\mathrm{A}$가 $2$회차에 무엇을 뽑아도 $a_2 = 1$이 자동 성립합니다.</li>\n'
                        '      <li><b>주머니 $\\mathrm{A}$에서 $\\mathrm{A}_1 = 1$이 되는 가짓수($12$가지)</b>:\n'
                        '        <br>&nbsp;&nbsp;• <b>[방법 A: $1\\text{회차} \\to 2\\text{회차}$ 분류]</b> $\\mathrm{A} = (1, '
                        '1)$인 $3 \\times 2 = 6$가지 $+$ $\\mathrm{A} = (1, 2)$인 $3 \\times 2 = 6$가지 $= '
                        '\\mathbf{12}\\text{가지}$\n'
                        '        <br>&nbsp;&nbsp;• <b>[방법 B: $1$회차 고정 $\\to$ $2$회차 선택]</b> $1$회차에 $1$($3$가지) $\\times$ '
                        '$2$회차에 남은 공 아무거나($4$가지) $= 3 \\times 4 = \\mathbf{12}\\text{가지}$</li>\n'
                        '      <li><b>케이스 ②의 경우의 수</b>: $(\\text{주머니 B의 } 4\\text{가지}) \\times (\\text{주머니 A의 } '
                        '12\\text{가지}) = 4 \\times 12 = \\mathbf{48}\\text{가지}$</li>\n'
                        '    </ol>\n'
                        '  </li>\n'
                        '</ul>\n'
                        '<p>따라서 조건부확률의 분자 $n(E \\cap F)$는:\n'
                        '$$n(E \\cap F) = 48 + 48 = \\mathbf{96}\\text{가지}$$</p>\n'
                        '\n'
                        '<h4>📊 [5. 한눈에 보는 $400$가지 전체 경우의 수 완전 해부표 (시각적 전수 검산)]</h4>\n'
                        '<p>주머니 $\\mathrm{A}$의 $4$가지 패턴($6+6+6+2=20$)과 주머니 $\\mathrm{B}$의 $3$가지 패턴($12+4+4=20$)이 만나는 '
                        '$12$개 칸($400$가지)을 표로 정리하면 분모($336$)와 분자($96$)가 한눈에 확인됩니다.</p>\n'
                        '<table style="width:100%;border-collapse:collapse;margin:10px '
                        '0;font-size:0.86rem;text-align:center;border:1px solid rgba(124,196,255,.35)">\n'
                        '  <thead>\n'
                        '    <tr style="background:rgba(124,196,255,.16);color:#7cc4ff">\n'
                        '      <th style="padding:8px;border:1px solid rgba(124,196,255,.25)">$\\mathrm{A} \\backslash '
                        '\\mathrm{B}$</th>\n'
                        '      <th style="padding:8px;border:1px solid rgba(124,196,255,.25)">$\\mathrm{B}=(1,1)$ : '
                        '$12$가지<br><span style="font-size:0.78rem;color:#9aa6c0">($\\mathrm{B}$에 $1$이 $2$개 '
                        '남음)</span></th>\n'
                        '      <th style="padding:8px;border:1px solid '
                        'rgba(124,196,255,.25);background:rgba(94,234,212,.14);color:#5eead4">$\\mathrm{B}=(1,2)$ : '
                        '$4$가지<br><span style="font-size:0.78rem">🎯 $\\mathrm{B}$에 $1$이 $3$개 남음</span></th>\n'
                        '      <th style="padding:8px;border:1px solid '
                        'rgba(124,196,255,.25);background:rgba(94,234,212,.14);color:#5eead4">$\\mathrm{B}=(2,1)$ : '
                        '$4$가지<br><span style="font-size:0.78rem">🎯 $\\mathrm{B}$에 $1$이 $3$개 남음</span></th>\n'
                        '    </tr>\n'
                        '  </thead>\n'
                        '  <tbody>\n'
                        '    <tr>\n'
                        '      <td style="padding:7px;border:1px solid '
                        'rgba(124,196,255,.25);font-weight:700">$\\mathrm{A}=(1,1)$ : $6$가지</td>\n'
                        '      <td style="padding:7px;border:1px solid rgba(124,196,255,.25)">$6\\times 12 = '
                        '72$가지<br><span style="color:#93c5fd">⭕ $a_1=1, a_2=1$ (분모)</span></td>\n'
                        '      <td style="padding:7px;border:1px solid '
                        'rgba(124,196,255,.25);background:rgba(94,234,212,.10)"><b>$6\\times 4 = 24$가지</b><br><span '
                        'style="color:#5eead4">🎯 <b>분자 &amp; 분모</b></span></td>\n'
                        '      <td style="padding:7px;border:1px solid '
                        'rgba(124,196,255,.25);background:rgba(94,234,212,.10)"><b>$6\\times 4 = 24$가지</b><br><span '
                        'style="color:#5eead4">🎯 <b>분자 &amp; 분모</b></span></td>\n'
                        '    </tr>\n'
                        '    <tr>\n'
                        '      <td style="padding:7px;border:1px solid '
                        'rgba(124,196,255,.25);font-weight:700">$\\mathrm{A}=(1,2)$ : $6$가지</td>\n'
                        '      <td style="padding:7px;border:1px solid rgba(124,196,255,.25)">$6\\times 12 = '
                        '72$가지<br><span style="color:#93c5fd">⭕ $a_1=1, a_2=1$ (분모)</span></td>\n'
                        '      <td style="padding:7px;border:1px solid '
                        'rgba(124,196,255,.25);background:rgba(251,113,133,.12)">$6\\times 4 = 24$가지<br><span '
                        'style="color:#fb7185">❌ $a_2=2$ (탈락)</span></td>\n'
                        '      <td style="padding:7px;border:1px solid '
                        'rgba(124,196,255,.25);background:rgba(94,234,212,.10)"><b>$6\\times 4 = 24$가지</b><br><span '
                        'style="color:#5eead4">🎯 <b>분자 &amp; 분모</b></span></td>\n'
                        '    </tr>\n'
                        '    <tr>\n'
                        '      <td style="padding:7px;border:1px solid '
                        'rgba(124,196,255,.25);font-weight:700">$\\mathrm{A}=(2,1)$ : $6$가지</td>\n'
                        '      <td style="padding:7px;border:1px solid rgba(124,196,255,.25)">$6\\times 12 = '
                        '72$가지<br><span style="color:#93c5fd">⭕ $a_1=1, a_2=1$ (분모)</span></td>\n'
                        '      <td style="padding:7px;border:1px solid '
                        'rgba(124,196,255,.25);background:rgba(94,234,212,.10)"><b>$6\\times 4 = 24$가지</b><br><span '
                        'style="color:#5eead4">🎯 <b>분자 &amp; 분모</b></span></td>\n'
                        '      <td style="padding:7px;border:1px solid '
                        'rgba(124,196,255,.25);background:rgba(251,113,133,.12)">$6\\times 4 = 24$가지<br><span '
                        'style="color:#fb7185">❌ $a_1=2$ (탈락)</span></td>\n'
                        '    </tr>\n'
                        '    <tr>\n'
                        '      <td style="padding:7px;border:1px solid '
                        'rgba(124,196,255,.25);font-weight:700">$\\mathrm{A}=(2,2)$ : $2$가지</td>\n'
                        '      <td style="padding:7px;border:1px solid rgba(124,196,255,.25)">$2\\times 12 = '
                        '24$가지<br><span style="color:#93c5fd">⭕ $a_1=1, a_2=1$ (분모)</span></td>\n'
                        '      <td style="padding:7px;border:1px solid '
                        'rgba(124,196,255,.25);background:rgba(251,113,133,.12)">$2\\times 4 = 8$가지<br><span '
                        'style="color:#fb7185">❌ $a_2=2$ (탈락)</span></td>\n'
                        '      <td style="padding:7px;border:1px solid '
                        'rgba(124,196,255,.25);background:rgba(251,113,133,.12)">$2\\times 4 = 8$가지<br><span '
                        'style="color:#fb7185">❌ $a_1=2$ (탈락)</span></td>\n'
                        '    </tr>\n'
                        '    <tr style="background:rgba(255,255,255,.06);font-weight:700">\n'
                        '      <td style="padding:7px;border:1px solid rgba(124,196,255,.25)">열 합계</td>\n'
                        '      <td style="padding:7px;border:1px solid rgba(124,196,255,.25)">분모 $240$가지</td>\n'
                        '      <td style="padding:7px;border:1px solid rgba(124,196,255,.25)">🎯분자 $48$ / ❌탈락 '
                        '$32$</td>\n'
                        '      <td style="padding:7px;border:1px solid rgba(124,196,255,.25)">🎯분자 $48$ / ❌탈락 '
                        '$32$</td>\n'
                        '    </tr>\n'
                        '  </tbody>\n'
                        '</table>\n'
                        '<p>• <b>분모 $n(E)$ 합계</b>: $240 + 48 + 48 = \\mathbf{336}\\text{가지}$ (또는 전체 $400 - \\text{탈락 '
                        '}(32 + 32) = 336$가지)<br>\n'
                        '• <b>분자 $n(E \\cap F)$ 합계</b>: 🎯 초록색 칸 $24 + 24 + 24 + 24 = 48 + 48 = '
                        '\\mathbf{96}\\text{가지}$</p>\n'
                        '\n'
                        '<h4>💡 [6. 별해 (Alternative Solution): 경우의 수 대신 확률의 곱셈정리로 직접 구하기]</h4>\n'
                        '<p>근원사건의 개수를 세지 않고 <b>확률의 덧셈·곱셈정리</b>로도 완전히 동일하게 풀 수 있습니다.</p>\n'
                        '<ul>\n'
                        '  <li><b>분모 $\\mathrm{P}(E)$ 구하기</b>:\n'
                        '    <ul>\n'
                        '      <li>$1$회차에 둘 다 $2$를 뽑을 확률: $\\mathrm{P}(a_1 = 2) = '
                        '\\mathrm{P}(\\mathrm{A}_1=2)\\mathrm{P}(\\mathrm{B}_1=2) = \\dfrac{2}{5} \\times '
                        '\\dfrac{1}{5} = \\dfrac{2}{25}$</li>\n'
                        '      <li>$2$회차에 둘 다 $2$를 뽑을 확률: 비복원 추출에서 매 회차 특정 숫자가 뽑힐 주변확률은 $1$회차와 동일하므로 $\\mathrm{P}(a_2 '
                        '= 2) = \\dfrac{2}{5} \\times \\dfrac{1}{5} = \\dfrac{2}{25}$</li>\n'
                        '      <li>$\\mathrm{B}$에 $2$가 $1$개뿐이므로 $\\mathrm{P}(a_1=2 \\cap a_2=2) = 0$입니다. 따라서:\n'
                        '        $$\\mathrm{P}(E) = 1 - \\left(\\frac{2}{25} + \\frac{2}{25}\\right) = 1 - '
                        '\\frac{4}{25} = \\frac{21}{25}$$</li>\n'
                        '    </ul>\n'
                        '  </li>\n'
                        '  <li><b>분자 $\\mathrm{P}(E \\cap F)$ 구하기</b>:\n'
                        '    <ul>\n'
                        '      <li>케이스 ① ($\\mathrm{B}=(1,2)$이고 $\\mathrm{A}_2=1$): $\\mathrm{P}(\\mathrm{B}=(1,2)) '
                        '\\times \\mathrm{P}(\\mathrm{A}_2=1) = \\left(\\dfrac{4}{5} \\times \\dfrac{1}{4}\\right) '
                        '\\times \\dfrac{3}{5} = \\dfrac{1}{5} \\times \\dfrac{3}{5} = \\dfrac{3}{25}$</li>\n'
                        '      <li>케이스 ② ($\\mathrm{B}=(2,1)$이고 $\\mathrm{A}_1=1$): $\\mathrm{P}(\\mathrm{B}=(2,1)) '
                        '\\times \\mathrm{P}(\\mathrm{A}_1=1) = \\left(\\dfrac{1}{5} \\times \\dfrac{4}{4}\\right) '
                        '\\times \\dfrac{3}{5} = \\dfrac{1}{5} \\times \\dfrac{3}{5} = \\dfrac{3}{25}$</li>\n'
                        '      <li>따라서 $\\mathrm{P}(E \\cap F) = \\dfrac{3}{25} + \\dfrac{3}{25} = '
                        '\\dfrac{6}{25}$입니다.</li>\n'
                        '    </ul>\n'
                        '  </li>\n'
                        '  <li><b>조건부확률 계산</b>:\n'
                        '    $$\\mathrm{P}(F \\mid E) = \\frac{\\mathrm{P}(E \\cap F)}{\\mathrm{P}(E)} = '
                        '\\frac{6/25}{21/25} = \\frac{6}{21} = \\frac{2}{7}$$</li>\n'
                        '</ul>\n'
                        '\n'
                        '<h4>✨ [7. 정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  구하는 조건부확률은:\n'
                        '  $$\\mathrm{P}(F \\mid E) = \\frac{n(E \\cap F)}{n(E)} = \\frac{96}{336} = \\frac{48 \\times '
                        '2}{48 \\times 7} = \\frac{2}{7} = \\frac{q}{p}$$\n'
                        '  따라서 서로소인 두 자연수는 $p = 7,\\ q = 2$이므로 최종 정답은 $p + q = 7 + 2 =$ <b>$9$</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [1. Problem Analysis &amp; Core Concepts]</h4>\n'
                           '<p>This #30 killer question in Probability &amp; Statistics asks for the <b>conditional '
                           'probability $\\mathrm{P}(F \\mid E) = \\dfrac{\\mathrm{P}(E \\cap F)}{\\mathrm{P}(E)} = '
                           '\\dfrac{n(E \\cap F)}{n(E)}$ under sampling without replacement</b>. Labeling the balls as '
                           '$\\mathrm{A} = \\{1_a, 1_b, 1_c, 2_a, 2_b\\}$ and $\\mathrm{B} = \\{1_p, 1_q, 1_r, 1_s, '
                           '2_p\\}$ makes all $20 \\times 20 = 400$ ordered pairs of draws equally likely.</p>\n'
                           '\n'
                           '<h4>🔍 [2. Decomposition of the $20$ Draws in Each Bag]</h4>\n'
                           '<ul>\n'
                           '  <li><b>Bag $\\mathrm{A}$ (three $1$s, two $2$s; $5 \\times 4 = 20$ ordered pairs)</b>: '
                           '$(1,1): 3\\times 2=6$, $(1,2): 3\\times 2=6$, $(2,1): 2\\times 3=6$, $(2,2): 2\\times 1=2$ '
                           '(Total $= 20$).</li>\n'
                           '  <li><b>Bag $\\mathrm{B}$ (four $1$s, one $2$; $5 \\times 4 = 20$ ordered pairs)</b>: '
                           '$(1,1): 4\\times 3=12$, $(1,2): 4\\times 1=4$, $(2,1): 1\\times 4=4$, $(2,2): 0$ (Total $= '
                           '20$).</li>\n'
                           '</ul>\n'
                           '\n'
                           '<h4>📐 [3. Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Denominator $n(E)$ ($a_1 = 1$ and $a_2 = 1$) via Complement</b><br>\n'
                           '  Since $a_n = \\min(\\mathrm{A}_n, \\mathrm{B}_n) = 2$ occurs iff both bags draw $2$ in '
                           'round $n$:<br>\n'
                           '  • $a_1 = 2$: Bag A draws $2$ in Round 1 ($6 + 2 = 8$ ways) $\\times$ Bag B draws $2$ in '
                           'Round 1 ($4$ ways) $= 32$ ways.<br>\n'
                           '  • $a_2 = 2$: Bag A draws $2$ in Round 2 ($6 + 2 = 8$ ways) $\\times$ Bag B draws $2$ in '
                           'Round 2 ($4$ ways) $= 32$ ways.<br>\n'
                           '  • $a_1 = 2$ and $a_2 = 2$: $0$ ways since Bag B has only one ball labeled $2$.<br>\n'
                           '  Thus $n(E) = 400 - (32 + 32 - 0) = \\mathbf{336}$.<br><br>\n'
                           '  <b>Step 2: Numerator $n(E \\cap F)$ (Three $1$s remain in B and $a_1 = a_2 = '
                           '1$)</b><br>\n'
                           '  For three $1$s to remain in B (out of four $1$s and one $2$), B must draw one $1$ and '
                           'one $2$:<br>\n'
                           '  • <b>Case 1: $\\mathrm{B} = (1, 2)$ ($4 \\times 1 = 4$ ways)</b>. Since $\\mathrm{B}_1 = '
                           '1$, $a_1 = 1$ holds automatically. Since $\\mathrm{B}_2 = 2$, Bag A must draw $1$ in Round '
                           '2 ($\\mathrm{A}_2 = 1$), which occurs in $12$ ways (Method A: $\\mathrm{A}=(1,1)$ in $6$ '
                           'ways + $\\mathrm{A}=(2,1)$ in $6$ ways $= 12$; Method B: $3$ choices for Round 2 $\\times$ '
                           '$4$ remaining balls for Round 1 $= 12$). Product: $4 \\times 12 = \\mathbf{48}$ ways.<br>\n'
                           '  • <b>Case 2: $\\mathrm{B} = (2, 1)$ ($1 \\times 4 = 4$ ways)</b>. Since $\\mathrm{B}_1 = '
                           '2$, Bag A must draw $1$ in Round 1 ($\\mathrm{A}_1 = 1$), which occurs in $12$ ways '
                           '($\\mathrm{A}=(1,1)$ in $6$ ways + $\\mathrm{A}=(1,2)$ in $6$ ways $= 12$). Product: $4 '
                           '\\times 12 = \\mathbf{48}$ ways.<br>\n'
                           '  Thus $n(E \\cap F) = 48 + 48 = \\mathbf{96}$.\n'
                           '</p>\n'
                           '\n'
                           '<h4>💡 [4. Alternative Solution via Probability Rules]</h4>\n'
                           '<p>\n'
                           '  • $\\mathrm{P}(E) = 1 - \\left(\\dfrac{2}{5}\\cdot\\dfrac{1}{5} + '
                           '\\dfrac{2}{5}\\cdot\\dfrac{1}{5}\\right) = 1 - \\dfrac{4}{25} = \\dfrac{21}{25}$.<br>\n'
                           '  • $\\mathrm{P}(E \\cap F) = '
                           '\\left(\\dfrac{4}{5}\\cdot\\dfrac{1}{4}\\right)\\cdot\\dfrac{3}{5} + '
                           '\\left(\\dfrac{1}{5}\\cdot\\dfrac{4}{4}\\right)\\cdot\\dfrac{3}{5} = \\dfrac{3}{25} + '
                           '\\dfrac{3}{25} = \\dfrac{6}{25}$.<br>\n'
                           '  • $\\mathrm{P}(F \\mid E) = \\dfrac{6/25}{21/25} = \\dfrac{6}{21} = \\dfrac{2}{7}$.\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [5. Final Answer &amp; Practical Tips]</h4>\n'
                           '<p>\n'
                           '  $$\\mathrm{P}(F \\mid E) = \\frac{96}{336} = \\frac{48 \\times 2}{48 \\times 7} = '
                           '\\frac{2}{7} \\implies p = 7,\\ q = 2 \\implies p + q = \\mathbf{9}$$\n'
                           '</p>'}}]
