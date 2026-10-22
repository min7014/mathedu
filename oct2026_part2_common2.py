# -*- coding: utf-8 -*-

PART2_PROBLEMS = [{'slug': 'c261012',
  'qNum': '12',
  'subject': '공통(수학I·II)',
  'title': '[2026학년도 10월 고3 12번] 평행이동한 두 지수함수의 그래프와 사다리꼴 변의 길이',
  'title_en': '[2026 AY Oct Exam Grade 12 #12] Translated Exponential Graphs and Segment Lengths',
  'summary_ko': '점 $\\mathrm{A}$와 점 $\\mathrm{D}$의 $y$좌표가 같음을 발견해 $\\overline{\\mathrm{AD}}=2$를 구하고 지수법칙으로 $a$와 $k$ '
                '도출하기',
  'summary_en': 'Identify that $\\mathrm{A}$ and $\\mathrm{D}$ share the same $y$-coordinate to find '
                '$\\overline{\\mathrm{AD}}=2$, then solve for $a$ and $k$ using exponent rules.',
  'tags': ['공통(수학I·II)', '수학I', '지수함수', '평행이동', '좌표와길이', '12번'],
  'symbols': [{'sym': '$y = a^{x-2}$',
               'desc': '함수 $y=a^x$의 그래프를 $x$축 방향으로 $2$만큼 이동한 식',
               'desc_en': 'Graph of $y=a^x$ translated by $+2$ along the $x$-axis.'},
              {'sym': '$\\overline{AD} = (k+2) - k = 2$',
               'desc': '높이(y좌표)가 같은 두 점 사이의 가로 거리',
               'desc_en': 'Horizontal distance between two points sharing the same y-coordinate.'},
              {'sym': '$a^{k+2} - a^k = a^2(a^k - a^{k-2})$',
               'desc': '공통인수 $a^2$으로 묶어 세로 길이의 비율 찾기',
               'desc_en': 'Factoring out $a^2$ to find the ratio of vertical segments.'}],
  'levels': [{'title': '🔰 1단계 · [초등 수직선 거리] 가로선이 같을 때 두 점 사이의 거리 구하기',
              'title_en': '🔰 Step 1 · [Elementary Number Line] Distance between two points at the same height',
              'knowledge': '초등학교 수직선에서 왼쪽 눈금이 $k$이고 오른쪽 눈금이 $k+2$이면, 두 눈금 사이의 거리는 오른쪽에서 왼쪽을 뺀 $(k+2) - k = 2$입니다.',
              'knowledge_en': 'On an elementary number line, the distance between $k$ and $k+2$ is $(k+2) - k = 2$.',
              'questions': [{'level_label': '초등 수직선 디딤돌 1',
                             'level_label_en': 'Elementary Number Line Step 1',
                             'stem': '초등학교 수직선 계산처럼 점 $\\mathrm{A}(k, a^k)$와 점 $\\mathrm{D}(k+2, a^k)$는 높이($y$좌표)가 '
                                     '$a^k$으로 똑같습니다. 이때 가로 선분 $\\overline{\\mathrm{AD}}$의 길이는?',
                             'stem_en': 'Using elementary number line subtraction, points $\\mathrm{A}(k, a^k)$ and '
                                        '$\\mathrm{D}(k+2, a^k)$ have the same $y$-coordinate $a^k$. What is the '
                                        'length of $\\overline{\\mathrm{AD}}$?',
                             'options': ['$1$', '$2$', '$3$', '$4$', '$6$'],
                             'answer': 2,
                             'exp': '두 점의 $y$좌표가 $a^k$으로 같으므로 $\\overline{\\mathrm{AD}}$는 $x$좌표의 차 $(k+2) - k = 2$입니다.',
                             'exp_en': 'Since both points have $y = a^k$, $\\overline{\\mathrm{AD}} = (k+2) - k = '
                                       '2$.'}]},
             {'title': '🌿 2단계 · [초등 뺄셈 활용] 세로 선분 $\\overline{\\mathrm{AC}}$와 $\\overline{\\mathrm{BD}}$의 길이 찾기',
              'title_en': '🌿 Step 2 · [Elementary Subtraction] Finding the vertical lengths $\\overline{\\mathrm{AC}}$ '
                          'and $\\overline{\\mathrm{BD}}$',
              'knowledge': '문제에서 $\\overline{\\mathrm{AC}} = \\overline{\\mathrm{AD}}$라고 했으므로 '
                           '$\\overline{\\mathrm{AC}} = 2$입니다. 또 $\\overline{\\mathrm{AC}} + \\overline{\\mathrm{BD}} '
                           '= 6$이므로 $\\overline{\\mathrm{BD}} = 6 - 2 = 4$가 됩니다.',
              'knowledge_en': 'Since $\\overline{\\mathrm{AC}} = \\overline{\\mathrm{AD}} = 2$ and '
                              '$\\overline{\\mathrm{AC}} + \\overline{\\mathrm{BD}} = 6$, we get '
                              '$\\overline{\\mathrm{BD}} = 6 - 2 = 4$.',
              'questions': [{'level_label': '초등 뺄셈 디딤돌 2',
                             'level_label_en': 'Elementary Subtraction Step 2',
                             'stem': '$\\overline{\\mathrm{AD}} = 2$이고 조건에서 $\\overline{\\mathrm{AC}} = '
                                     '\\overline{\\mathrm{AD}}$, $\\overline{\\mathrm{AC}} + \\overline{\\mathrm{BD}} '
                                     '= 6$일 때, 선분 $\\overline{\\mathrm{BD}}$의 길이는?',
                             'stem_en': 'Given $\\overline{\\mathrm{AD}} = 2$, $\\overline{\\mathrm{AC}} = '
                                        '\\overline{\\mathrm{AD}}$, and $\\overline{\\mathrm{AC}} + '
                                        '\\overline{\\mathrm{BD}} = 6$, what is $\\overline{\\mathrm{BD}}$?',
                             'options': ['$1$', '$2$', '$3$', '$4$', '$5$'],
                             'answer': 4,
                             'exp': '$\\overline{\\mathrm{AC}} = 2$이므로 $2 + \\overline{\\mathrm{BD}} = 6 \\implies '
                                    '\\overline{\\mathrm{BD}} = 4$입니다.',
                             'exp_en': 'Since $\\overline{\\mathrm{AC}} = 2$, $\\overline{\\mathrm{BD}} = 6 - 2 = '
                                       '4$.'}]},
             {'title': '🌱 3단계 · [비율 비교] 세로 길이의 비율로 밑 $a$ 구하기',
              'title_en': '🌱 Step 3 · [Ratio Comparison] Finding base $a$ from the ratio of vertical lengths',
              'knowledge': '$\\overline{\\mathrm{AC}} = a^k - a^{k-2} = 2$이고, $\\overline{\\mathrm{BD}} = a^{k+2} - '
                           'a^k = a^2(a^k - a^{k-2}) = 4$입니다. 즉 $\\overline{\\mathrm{BD}}$는 '
                           '$\\overline{\\mathrm{AC}}$의 $a^2$배입니다.',
              'knowledge_en': '$\\overline{\\mathrm{AC}} = a^k - a^{k-2} = 2$ and $\\overline{\\mathrm{BD}} = a^{k+2} '
                              '- a^k = a^2(a^k - a^{k-2}) = 4$, so $a^2 \\times 2 = 4$.',
              'questions': [{'level_label': '지수 묶어내기 디딤돌 3',
                             'level_label_en': 'Factoring Exponents Step 3',
                             'stem': '$a^2 \\times \\overline{\\mathrm{AC}} = \\overline{\\mathrm{BD}}$에서 $2a^2 = 4$가 '
                                     '성립합니다. $a > 1$일 때 양수 $a$의 값은?',
                             'stem_en': 'From $2a^2 = 4$ with $a > 1$, what is the value of $a$?',
                             'options': ['$\\sqrt{2}$', '$\\sqrt{3}$', '$2$', '$2\\sqrt{2}$', '$4$'],
                             'answer': 1,
                             'exp': '$a^2 = 2$이고 $a > 1$이므로 $a = \\sqrt{2}$입니다.',
                             'exp_en': 'Since $a^2 = 2$ and $a > 1$, $a = \\sqrt{2}$.'}]},
             {'title': '🌳 4단계 · [거듭제곱 계산] $a^k$의 값으로부터 $k$ 구하기',
              'title_en': '🌳 Step 4 · [Power Calculation] Finding $k$ from $a^k$',
              'knowledge': '$\\overline{\\mathrm{BD}} = a^{k+2} - a^k = a^k(a^2 - 1) = 4$에 $a^2 = 2$를 대입하면 $a^k(2 - 1) '
                           '= 4$, 즉 $a^k = 4$입니다.',
              'knowledge_en': 'Substituting $a^2 = 2$ into $a^k(a^2 - 1) = 4$ gives $a^k = 4$.',
              'questions': [{'level_label': '지수 방정식 디딤돌 4',
                             'level_label_en': 'Exponential Equation Step 4',
                             'stem': '$a = \\sqrt{2}$일 때 $(\\sqrt{2})^k = 4$를 만족시키는 상수 $k$의 값은?',
                             'stem_en': 'When $a = \\sqrt{2}$, what is the value of $k$ satisfying $(\\sqrt{2})^k = '
                                        '4$?',
                             'options': ['$1$', '$2$', '$3$', '$4$', '$6$'],
                             'answer': 4,
                             'exp': '$(\\sqrt{2})^2 = 2$이므로 $(\\sqrt{2})^4 = 2^2 = 4$, 따라서 $k = 4$입니다.',
                             'exp_en': 'Since $(\\sqrt{2})^2 = 2$, raising both sides to the 2nd power gives '
                                       '$(\\sqrt{2})^4 = 4$, so $k = 4$.'}]},
             {'title': '💎 5단계 · [최종 종합] $a \\times k$의 값 구하기',
              'title_en': '💎 Step 5 · [Final Synthesis] Calculating $a \\times k$',
              'knowledge': '앞 단계에서 구한 $a = \\sqrt{2}$와 $k = 4$를 곱하면 최종 정답을 얻습니다.',
              'knowledge_en': 'Multiply $a = \\sqrt{2}$ and $k = 4$ found in the previous steps.',
              'questions': [{'level_label': '최종 종합 디딤돌 5',
                             'level_label_en': 'Final Synthesis Step 5',
                             'stem': '$a = \\sqrt{2}$, $k = 4$일 때, $a \\times k$의 값은?',
                             'stem_en': 'Given $a = \\sqrt{2}$ and $k = 4$, what is $a \\times k$?',
                             'options': ['$2\\sqrt{2}$',
                                         '$3\\sqrt{2}$',
                                         '$3\\sqrt{3}$',
                                         '$4\\sqrt{2}$',
                                         '$4\\sqrt{3}$'],
                             'answer': 4,
                             'exp': '$a \\times k = \\sqrt{2} \\times 4 = 4\\sqrt{2}$입니다.',
                             'exp_en': '$a \\times k = \\sqrt{2} \\times 4 = 4\\sqrt{2}$.'}]}],
  'final': {'stem': '두 상수 $a$ $(a > 1)$, $k$에 대하여 직선 $x = k$가 두 함수 $y = a^x$, $y = a^{x-2}$의 그래프와 만나는 점을 각각 '
                    '$\\mathrm{A}$, $\\mathrm{C}$라 하고, 직선 $x = k+2$가 두 함수 $y = a^x$, $y = a^{x-2}$의 그래프와 만나는 점을 각각 '
                    '$\\mathrm{B}$, $\\mathrm{D}$라 하자. $\\overline{\\mathrm{AC}} = \\overline{\\mathrm{AD}}$, '
                    '$\\overline{\\mathrm{AC}} + \\overline{\\mathrm{BD}} = 6$일 때, $a \\times k$의 값은? [4점]',
            'stem_en': 'For constants $a > 1$ and $k$, the line $x = k$ meets $y = a^x$ and $y = a^{x-2}$ at '
                       '$\\mathrm{A}$ and $\\mathrm{C}$, and the line $x = k+2$ meets $y = a^x$ and $y = a^{x-2}$ at '
                       '$\\mathrm{B}$ and $\\mathrm{D}$. When $\\overline{\\mathrm{AC}} = \\overline{\\mathrm{AD}}$ '
                       'and $\\overline{\\mathrm{AC}} + \\overline{\\mathrm{BD}} = 6$, what is $a \\times k$? [4 '
                       'points]',
            'options': ['$2\\sqrt{2}$', '$3\\sqrt{2}$', '$3\\sqrt{3}$', '$4\\sqrt{2}$', '$4\\sqrt{3}$'],
            'answer': 4,
            'exp': '$\\mathrm{A}(k, a^k)$, $\\mathrm{D}(k+2, a^k)$이므로 $\\overline{\\mathrm{AD}} = 2 = '
                   '\\overline{\\mathrm{AC}}$, $\\overline{\\mathrm{BD}} = 4$입니다. $a^2 = '
                   '\\dfrac{\\overline{\\mathrm{BD}}}{\\overline{\\mathrm{AC}}} = 2 \\implies a = \\sqrt{2}$이고, '
                   '$a^k(a^2-1) = 4 \\implies a^k = 4 \\implies k = 4$이므로 $a \\times k = 4\\sqrt{2}$입니다.',
            'exp_en': 'Since $\\mathrm{A}(k, a^k)$ and $\\mathrm{D}(k+2, a^k)$ share the same $y$-coordinate, '
                      '$\\overline{\\mathrm{AD}} = 2 = \\overline{\\mathrm{AC}}$ and $\\overline{\\mathrm{BD}} = 4$. '
                      'Thus $a^2 = 2 \\implies a = \\sqrt{2}$ and $a^k = 4 \\implies k = 4$, giving $a \\times k = '
                      '4\\sqrt{2}$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>지수함수의 평행이동과 네 교점의 좌표 관계</b>를 파악하는 문제입니다. 함수 $y = a^{x-2}$에 $x = k+2$를 대입한 점 '
                        '$\\mathrm{D}$의 $y$좌표가 점 $\\mathrm{A}$의 $y$좌표($a^k$)와 일치한다는 대칭적 특징을 발견하는 것이 핵심입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 네 점 $\\mathrm{A}, \\mathrm{B}, \\mathrm{C}, \\mathrm{D}$의 좌표 구하기</b><br>\n'
                        '  주어진 직선의 방정식을 각 지수함수에 대입하면:<br>\n'
                        '  $$\\mathrm{A}(k, a^k), \\quad \\mathrm{C}(k, a^{k-2}), \\quad \\mathrm{B}(k+2, a^{k+2}), '
                        '\\quad \\mathrm{D}(k+2, a^k)$$<br>\n'
                        '  <b>2단계: 선분 $\\overline{\\mathrm{AD}}, \\overline{\\mathrm{AC}}, \\overline{\\mathrm{BD}}$의 '
                        '길이 결정</b><br>\n'
                        '  점 $\\mathrm{A}$와 점 $\\mathrm{D}$의 $y$좌표가 $a^k$으로 같으므로 선분 $\\mathrm{AD}$는 $x$축에 평행하며:<br>\n'
                        '  $$\\overline{\\mathrm{AD}} = (k+2) - k = 2$$\n'
                        '  조건에서 $\\overline{\\mathrm{AC}} = \\overline{\\mathrm{AD}}$이므로 $\\overline{\\mathrm{AC}} = '
                        '2$이고, $\\overline{\\mathrm{AC}} + \\overline{\\mathrm{BD}} = 6$에서 $\\overline{\\mathrm{BD}} = '
                        '4$입니다.<br><br>\n'
                        '  <b>3단계: 지수법칙으로 $a$와 $k$ 구하기</b><br>\n'
                        '  $$\\overline{\\mathrm{AC}} = a^k - a^{k-2} = 2, \\quad \\overline{\\mathrm{BD}} = a^{k+2} - '
                        'a^k = a^2(a^k - a^{k-2}) = 4$$\n'
                        '  두 식을 나누면 $a^2 = 2$이고 $a > 1$이므로 $a = \\sqrt{2}$입니다.<br>\n'
                        '  이를 $\\overline{\\mathrm{BD}} = a^k(a^2 - 1) = 4$에 대입하면 $a^k(2 - 1) = 4 \\implies '
                        '(\\sqrt{2})^k = 4 \\implies k = 4$입니다.\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 $a \\times k = \\sqrt{2} \\times 4 = 4\\sqrt{2}$이므로 정답은 <b>④번</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem tests understanding of <b>horizontal translation of exponential '
                           'functions</b>. Recognizing that $\\mathrm{A}(k, a^k)$ and $\\mathrm{D}(k+2, a^k)$ have the '
                           'same $y$-coordinate immediately yields $\\overline{\\mathrm{AD}} = 2$.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Coordinates and segment lengths</b><br>\n'
                           '  $$\\mathrm{A}(k, a^k), \\quad \\mathrm{C}(k, a^{k-2}), \\quad \\mathrm{B}(k+2, a^{k+2}), '
                           '\\quad \\mathrm{D}(k+2, a^k)$$\n'
                           '  Thus $\\overline{\\mathrm{AD}} = (k+2) - k = 2 = \\overline{\\mathrm{AC}}$, and '
                           '$\\overline{\\mathrm{BD}} = 6 - 2 = 4$.<br><br>\n'
                           '  <b>Step 2: Solve for $a$ and $k$</b><br>\n'
                           '  $$\\frac{\\overline{\\mathrm{BD}}}{\\overline{\\mathrm{AC}}} = \\frac{a^{k+2} - a^k}{a^k '
                           '- a^{k-2}} = a^2 = \\frac{4}{2} = 2 \\implies a = \\sqrt{2}$$\n'
                           '  From $a^k(a^2 - 1) = 4$, we obtain $a^k = 4 \\implies (\\sqrt{2})^k = 4 \\implies k = '
                           '4$.\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  Therefore, $a \\times k = 4\\sqrt{2}$, which corresponds to <b>choice ④</b>.\n'
                           '</p>'}},
 {'slug': 'c261013',
  'qNum': '13',
  'subject': '공통(수학I·II)',
  'title': '[2026학년도 10월 고3 13번] 다항함수의 차수 결정과 도함수 항등식',
  'title_en': '[2026 AY Oct Exam Grade 12 #13] Degree Determination of a Polynomial and Derivative Identity',
  'summary_ko': '양변의 차수와 최고차항 계수를 비교하여 이차함수 $f(x)$를 결정하고 $f(4)$ 구하기',
  'summary_en': 'Compare degrees and leading coefficients on both sides to determine quadratic $f(x)$ and evaluate '
                '$f(4)$.',
  'tags': ['공통(수학I·II)', '수학II', '미분', '다항함수의차수', '항등식', '13번'],
  'symbols': [{'sym': '$\\deg(f) = n$',
               'desc': '다항함수 $f(x)$의 가장 높은 차수',
               'desc_en': 'Degree (highest power) of polynomial $f(x)$.'},
              {'sym': "$\\deg(f') = n - 1$",
               'desc': '미분하면 차수가 1만큼 줄어듦',
               'desc_en': 'Differentiating reduces the polynomial degree by 1.'},
              {'sym': "$f(x) = \\{f'(x)\\}^2 - 4$",
               'desc': '함수값은 도함수를 제곱한 뒤 4를 뺀 것과 항상 같음',
               'desc_en': 'Identity relating $f(x)$ directly to the square of its derivative.'}],
  'levels': [{'title': '🔰 1단계 · [초등 방정식 규칙] $n = 2(n - 1)$을 만족하는 차수 $n$ 찾기',
              'title_en': '🔰 Step 1 · [Elementary Equation Rule] Finding degree $n$ satisfying $n = 2(n - 1)$',
              'knowledge': '$n$차 다항식을 미분하면 $(n-1)$차가 되고, 그것을 제곱하면 차수가 $2$배인 $2(n-1)$차가 됩니다. 초등학교 숫자 넣기처럼 좌변과 우변의 차수가 '
                           '같으려면 $n = 2(n-1)$이어야 합니다.',
              'knowledge_en': "Using elementary arithmetic, if a degree-$n$ polynomial's derivative (degree $n-1$) is "
                              'squared, its degree becomes $2(n-1)$. Equating degrees gives $n = 2(n-1)$.',
              'questions': [{'level_label': '초등 규칙 찾기 디딤돌 1',
                             'level_label_en': 'Elementary Number Rule Step 1',
                             'stem': '초등학교 숫자 대입으로 $n = 2(n - 1)$을 만족시키는 자연수 $n$(다항함수 $f(x)$의 차수)을 구하면?',
                             'stem_en': 'Using elementary arithmetic, which natural number $n$ satisfies $n = 2(n - '
                                        '1)$?',
                             'options': ['$1$', '$2$', '$3$', '$4$', '$5$'],
                             'answer': 2,
                             'exp': '$n = 2n - 2$에서 $n = 2$입니다. 즉 $f(x)$는 이차함수입니다.',
                             'exp_en': 'Solving $n = 2n - 2$ gives $n = 2$, so $f(x)$ is a quadratic function.'}]},
             {'title': "🌿 2단계 · [계수 비교] 일차함수 $f'(x) = ax + b$의 기울기 $a$ 구하기",
              'title_en': "🌿 Step 2 · [Coefficient Comparison] Finding the slope $a$ of $f'(x) = ax + b$",
              'knowledge': "$f(x)$가 이차함수이므로 미분한 $f'(x)$는 일차함수 $f'(x) = ax + b$입니다. 적분(거꾸로 미분)을 생각하면 $f(x)$의 $x^2$항은 "
                           "$\\frac{a}{2}x^2$이고, 우변 $\\{f'(x)\\}^2$의 $x^2$항은 $a^2x^2$입니다.",
              'knowledge_en': "Since $f'(x) = ax + b$, the leading term of $f(x)$ is $\\frac{a}{2}x^2$, while the "
                              "leading term of $\\{f'(x)\\}^2$ is $a^2x^2$.",
              'questions': [{'level_label': '최고차항 비교 디딤돌 2',
                             'level_label_en': 'Leading Coefficient Step 2',
                             'stem': '$x^2$의 계수를 비교한 식 $\\frac{a}{2} = a^2$ ($a \\neq 0$)을 만족시키는 상수 $a$의 값은?',
                             'stem_en': 'For $a \\neq 0$, what value of $a$ satisfies $\\frac{a}{2} = a^2$?',
                             'options': ['$\\frac{1}{4}$', '$\\frac{1}{2}$', '$1$', '$2$', '$4$'],
                             'answer': 2,
                             'exp': '양변을 $a$로 나누면 $a = \\frac{1}{2}$입니다.',
                             'exp_en': 'Dividing both sides by $a \\neq 0$ yields $a = \\frac{1}{2}$.'}]},
             {'title': "🌱 3단계 · [초기 조건 대입] $f'(0) = 1$로 도함수 $f'(x)$ 완성하기",
              'title_en': "🌱 Step 3 · [Initial Condition] Completing $f'(x)$ using $f'(0) = 1$",
              'knowledge': "$f'(x) = \\frac{1}{2}x + b$에 $x = 0$을 대입하면 $f'(0) = b$입니다. 문제에서 $f'(0) = 1$이라고 주어졌습니다.",
              'knowledge_en': "Substituting $x = 0$ into $f'(x) = \\frac{1}{2}x + b$ gives $f'(0) = b = 1$.",
              'questions': [{'level_label': '도함수 완성 디딤돌 3',
                             'level_label_en': 'Derivative Completion Step 3',
                             'stem': "$f'(x) = \\frac{1}{2}x + 1$일 때, $x = 4$에서의 미분계수 $f'(4)$의 값은?",
                             'stem_en': "When $f'(x) = \\frac{1}{2}x + 1$, what is the value of $f'(4)$?",
                             'options': ['$1$', '$2$', '$3$', '$4$', '$5$'],
                             'answer': 3,
                             'exp': "$f'(4) = \\frac{1}{2} \\times 4 + 1 = 2 + 1 = 3$입니다.",
                             'exp_en': "$f'(4) = \\frac{1}{2}(4) + 1 = 3$."}]},
             {'title': "🌳 4단계 · [제곱 계산] $\\{f'(4)\\}^2$의 값 구하기",
              'title_en': "🌳 Step 4 · [Squaring] Calculating $\\{f'(4)\\}^2$",
              'knowledge': "굳이 $f(x)$의 상수항을 따로 구하지 않아도, 문제에 주어진 관계식 $f(4) = \\{f'(4)\\}^2 - 4$에 $f'(4) = 3$을 바로 대입할 수 "
                           '있습니다!',
              'knowledge_en': "We can directly substitute $f'(4) = 3$ into the given identity $f(4) = \\{f'(4)\\}^2 - "
                              '4$.',
              'questions': [{'level_label': '제곱 계산 디딤돌 4',
                             'level_label_en': 'Squaring Calculation Step 4',
                             'stem': "$f'(4) = 3$일 때, $\\{f'(4)\\}^2$의 값은?",
                             'stem_en': "Given $f'(4) = 3$, what is $\\{f'(4)\\}^2$?",
                             'options': ['$3$', '$6$', '$9$', '$12$', '$16$'],
                             'answer': 3,
                             'exp': '$3^2 = 3 \\times 3 = 9$입니다.',
                             'exp_en': '$3^2 = 9$.'}]},
             {'title': "💎 5단계 · [최종 종합] $f(4) = \\{f'(4)\\}^2 - 4$ 계산하기",
              'title_en': "💎 Step 5 · [Final Synthesis] Evaluating $f(4) = \\{f'(4)\\}^2 - 4$",
              'knowledge': '$9$에서 $4$를 빼면 $f(4)$의 값이 완성됩니다.',
              'knowledge_en': 'Subtract $4$ from $9$ to obtain $f(4)$.',
              'questions': [{'level_label': '최종 종합 디딤돌 5',
                             'level_label_en': 'Final Synthesis Step 5',
                             'stem': "$f(4) = \\{f'(4)\\}^2 - 4 = 9 - 4$를 계산한 최종 정답은?",
                             'stem_en': 'What is the final value of $f(4) = 9 - 4$?',
                             'options': ['$1$', '$3$', '$5$', '$7$', '$9$'],
                             'answer': 3,
                             'exp': '$f(4) = 9 - 4 = 5$이므로 정답은 ③입니다.',
                             'exp_en': '$f(4) = 9 - 4 = 5$ (choice ③).'}]}],
  'final': {'stem': "다항함수 $f(x)$가 모든 실수 $x$에 대하여 $f(x) = \\{f'(x)\\}^2 - 4$를 만족시킨다. $f'(0) = 1$일 때, $f(4)$의 값은? [3점]",
            'stem_en': "A polynomial function $f(x)$ satisfies $f(x) = \\{f'(x)\\}^2 - 4$ for all real $x$. If $f'(0) "
                       '= 1$, what is the value of $f(4)$? [3 points]',
            'options': ['$1$', '$3$', '$5$', '$7$', '$9$'],
            'answer': 3,
            'exp': "차수 비교를 통해 $f(x)$는 이차함수이고 $f'(x) = \\dfrac{1}{2}x + 1$입니다. 따라서 $f'(4) = 3$이므로 $f(4) = 3^2 - 4 = "
                   '5$입니다.',
            'exp_en': "Comparing degrees shows $f(x)$ is quadratic with $f'(x) = \\dfrac{1}{2}x + 1$. Since $f'(4) = "
                      '3$, $f(4) = 3^2 - 4 = 5$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>다항함수와 그 도함수 사이의 항등식에서 차수와 최고차항의 계수를 결정</b>하는 전형적인 수학II 문항입니다. $f(x)$를 구한 뒤 대입해도 '
                        "되지만, $f'(x)$만 구하여 준식에 바로 $x = 4$를 대입하면 훨씬 빠르게 답을 얻을 수 있습니다.</p>\n"
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 다항함수 $f(x)$의 차수 결정</b><br>\n'
                        "  $f(x)$를 $n$차 다항식이라 하면 $f'(x)$는 $(n-1)$차 다항식이고 $\\{f'(x)\\}^2 - 4$는 $2(n-1)$차 다항식입니다.<br>\n"
                        '  양변의 차수가 같아야 하므로 $n = 2(n-1) \\implies n = 2$, 즉 $f(x)$는 이차함수입니다.<br><br>\n'
                        "  <b>2단계: 도함수 $f'(x)$ 결정</b><br>\n"
                        "  $f'(0) = 1$이므로 일차함수인 도함수를 $f'(x) = ax + 1$ ($a \\neq 0$)로 놓을 수 있습니다.<br>\n"
                        "  양변을 미분하면 $f'(x) = 2f'(x)f''(x)$이고, $f'(x) \\neq 0$이므로:<br>\n"
                        "  $$1 = 2f''(x) \\implies f''(x) = a = \\frac{1}{2}$$\n"
                        "  따라서 $f'(x) = \\frac{1}{2}x + 1$입니다.<br><br>\n"
                        '  <b>3단계: $f(4)$의 값 계산</b><br>\n'
                        "  $f'(4) = \\frac{1}{2}(4) + 1 = 3$을 주어진 항등식 $f(4) = \\{f'(4)\\}^2 - 4$에 대입하면:<br>\n"
                        '  $$f(4) = 3^2 - 4 = 9 - 4 = 5$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 $f(4) = 5$이므로 정답은 <b>③번</b>입니다. (참고: $f(x) = \\frac{1}{4}x^2 + x - 3$입니다.)\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem requires finding the <b>degree and derivative of a polynomial function</b> '
                           "from the differential identity $f(x) = \\{f'(x)\\}^2 - 4$.</p>\n"
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Degree comparison</b><br>\n'
                           '  Let $\\deg(f) = n$. Then $n = 2(n-1) \\implies n = 2$.<br><br>\n'
                           '  <b>Step 2: Differentiate both sides</b><br>\n'
                           "  Differentiating $f(x) = \\{f'(x)\\}^2 - 4$ gives $f'(x) = 2f'(x)f''(x) \\implies f''(x) "
                           '= \\frac{1}{2}$.<br>\n'
                           "  Since $f'(0) = 1$, we have $f'(x) = \\frac{1}{2}x + 1$.<br><br>\n"
                           '  <b>Step 3: Evaluate $f(4)$</b><br>\n'
                           "  Since $f'(4) = 3$, substituting $x = 4$ gives $f(4) = 3^2 - 4 = 5$.\n"
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  Therefore, $f(4) = 5$, which is <b>choice ③</b>.\n'
                           '</p>'}},
 {'slug': 'c261014',
  'qNum': '14',
  'subject': '공통(수학I·II)',
  'title': '[2026학년도 10월 고3 14번] 원에 내접하는 사각형에서 사인법칙과 코사인법칙 빈칸 추론',
  'title_en': '[2026 AY Oct Exam Grade 12 #14] Law of Sines and Cosines in a Cyclic Quadrilateral',
  'summary_ko': '삼각형 $\\mathrm{BCD}$의 사인법칙으로 $\\overline{\\mathrm{BD}}=p$를 구하고, 두 삼각형 $\\mathrm{ABD}, \\mathrm{BCD}$의 '
                '코사인법칙으로 $q, r$ 구하기',
  'summary_en': 'Find $\\overline{\\mathrm{BD}}=p$ via the Law of Sines in $\\triangle\\mathrm{BCD}$, then determine '
                '$q$ and $r$ using the Law of Cosines in $\\triangle\\mathrm{ABD}$ and $\\triangle\\mathrm{BCD}$.',
  'tags': ['공통(수학I·II)', '수학I', '삼각함수', '사인법칙', '코사인법칙', '빈칸추론', '14번'],
  'symbols': [{'sym': '$\\dfrac{\\overline{BD}}{\\sin(\\angle DCB)} = 2R$',
               'desc': '외접원의 반지름 $R=3$을 이용한 사인법칙',
               'desc_en': 'Law of Sines using circumradius $R=3$.'},
              {'sym': '$\\angle DAB + \\angle DCB = \\pi$',
               'desc': '원에 내접하는 사각형의 마주 보는 각의 합은 180도',
               'desc_en': 'Opposite angles of a cyclic quadrilateral sum to $\\pi$.'},
              {'sym': '$c^2 = a^2 + b^2 - 2ab\\cos C$',
               'desc': '두 변과 끼인각으로 나머지 한 변을 구하는 코사인법칙',
               'desc_en': 'Law of Cosines relating three sides and one angle.'}],
  'levels': [{'title': '🔰 1단계 · [초등 곱셈과 피타고라스] $\\sin(\\angle\\mathrm{DCB})$와 외접원의 지름 $2R$ 구하기',
              'title_en': '🔰 Step 1 · [Elementary Multiplication & Pythagoras] Finding $\\sin(\\angle\\mathrm{DCB})$ '
                          'and diameter $2R$',
              'knowledge': '초등학교에서 원의 지름은 반지름($3$)의 $2$배이므로 $2 \\times 3 = 6$입니다. 또한 $\\cos(\\angle\\mathrm{DCB}) = '
                           '\\frac{1}{3}$이면 $\\sin^2\\theta + \\cos^2\\theta = 1$에서 $\\sin(\\angle\\mathrm{DCB}) = '
                           '\\sqrt{1 - \\frac{1}{9}} = \\frac{2\\sqrt{2}}{3}$입니다.',
              'knowledge_en': 'By elementary multiplication, the diameter of a circle with radius $3$ is $2 \\times 3 '
                              '= 6$. Also $\\sin(\\angle\\mathrm{DCB}) = \\sqrt{1 - (1/3)^2} = \\frac{2\\sqrt{2}}{3}$.',
              'questions': [{'level_label': '초등 지름과 사인법칙 디딤돌 1',
                             'level_label_en': 'Elementary Diameter & Sine Law Step 1',
                             'stem': '초등학교 원의 지름 계산처럼 반지름이 $3$인 원의 지름은 $2R = 6$입니다. 사인법칙 $\\overline{\\mathrm{BD}} = '
                                     '2R \\sin(\\angle\\mathrm{DCB}) = 6 \\times \\frac{2\\sqrt{2}}{3}$를 계산한 빈칸 (가)의 값 '
                                     '$p$는?',
                             'stem_en': 'Using elementary multiplication for diameter $2R = 6$, what is $p = '
                                        '\\overline{\\mathrm{BD}} = 6 \\times \\frac{2\\sqrt{2}}{3}$ in blank (가)?',
                             'options': ['$2\\sqrt{2}$',
                                         '$3\\sqrt{2}$',
                                         '$4\\sqrt{2}$',
                                         '$5\\sqrt{2}$',
                                         '$6\\sqrt{2}$'],
                             'answer': 3,
                             'exp': '$6 \\times \\frac{2\\sqrt{2}}{3} = 2 \\times 2\\sqrt{2} = 4\\sqrt{2}$이므로 $p = '
                                    '4\\sqrt{2}$입니다.',
                             'exp_en': '$6 \\times \\frac{2\\sqrt{2}}{3} = 4\\sqrt{2}$, so $p = 4\\sqrt{2}$.'}]},
             {'title': '🌿 2단계 · [내접사각형 성질] 마주 보는 각 $\\cos(\\angle\\mathrm{DAB})$의 값 구하기',
              'title_en': '🌿 Step 2 · [Cyclic Quadrilateral] Finding $\\cos(\\angle\\mathrm{DAB})$',
              'knowledge': '원에 내접하는 사각형에서 마주 보는 두 각의 합은 $\\pi$ ($180^\\circ$)입니다. 따라서 $\\cos(\\angle\\mathrm{DAB}) = '
                           '\\cos(\\pi - \\angle\\mathrm{DCB}) = -\\cos(\\angle\\mathrm{DCB}) = -\\frac{1}{3}$입니다.',
              'knowledge_en': 'Since $\\angle\\mathrm{DAB} = \\pi - \\angle\\mathrm{DCB}$, we have '
                              '$\\cos(\\angle\\mathrm{DAB}) = -\\cos(\\angle\\mathrm{DCB}) = -\\frac{1}{3}$.',
              'questions': [{'level_label': '코사인법칙 식 세우기 디딤돌 2',
                             'level_label_en': 'Law of Cosines Setup Step 2',
                             'stem': '삼각형 $\\mathrm{ABD}$에서 $\\overline{\\mathrm{AD}} = k$, $\\overline{\\mathrm{AB}} '
                                     '= 3k$, $\\cos(\\angle\\mathrm{DAB}) = -\\frac{1}{3}$일 때, $k^2 + (3k)^2 - 2 '
                                     '\\cdot k \\cdot 3k \\cdot \\left(-\\frac{1}{3}\\right)$을 간단히 하면?',
                             'stem_en': 'In $\\triangle\\mathrm{ABD}$ with $\\overline{\\mathrm{AD}} = k$, '
                                        '$\\overline{\\mathrm{AB}} = 3k$, and $\\cos(\\angle\\mathrm{DAB}) = '
                                        '-\\frac{1}{3}$, simplify $k^2 + 9k^2 - 6k^2\\left(-\\frac{1}{3}\\right)$.',
                             'options': ['$8k^2$', '$10k^2$', '$12k^2$', '$14k^2$', '$16k^2$'],
                             'answer': 3,
                             'exp': '$k^2 + 9k^2 + 2k^2 = 12k^2$입니다.',
                             'exp_en': '$k^2 + 9k^2 + 2k^2 = 12k^2$.'}]},
             {'title': '🌱 3단계 · [빈칸 (나) 구하기] $12k^2 = (4\\sqrt{2})^2 = 32$에서 $q = \\overline{\\mathrm{AD}}$ 찾기',
              'title_en': '🌱 Step 3 · [Blank (나)] Finding $q = \\overline{\\mathrm{AD}}$ from $12k^2 = 32$',
              'knowledge': '$\\overline{\\mathrm{BD}}^2 = (4\\sqrt{2})^2 = 32$이므로 $12k^2 = 32 \\implies k^2 = '
                           '\\frac{32}{12} = \\frac{8}{3}$입니다.',
              'knowledge_en': 'Since $\\overline{\\mathrm{BD}}^2 = 32$, $12k^2 = 32 \\implies k^2 = \\frac{8}{3}$.',
              'questions': [{'level_label': '빈칸 (나) 도출 디딤돌 3',
                             'level_label_en': 'Blank (나) Step 3',
                             'stem': '$k^2 = \\frac{8}{3}$일 때, 양수 $k = \\overline{\\mathrm{AD}}$의 값인 빈칸 (나)의 수 $q$는?',
                             'stem_en': 'Given $k^2 = \\frac{8}{3}$ ($k > 0$), what is $q = k$ in blank (나)?',
                             'options': ['$\\frac{\\sqrt{6}}{3}$',
                                         '$\\frac{2\\sqrt{6}}{3}$',
                                         '$\\sqrt{6}$',
                                         '$\\frac{4\\sqrt{6}}{3}$',
                                         '$2\\sqrt{6}$'],
                             'answer': 2,
                             'exp': '$k = \\sqrt{\\frac{8}{3}} = \\frac{2\\sqrt{2}}{\\sqrt{3}} = '
                                    '\\frac{2\\sqrt{6}}{3}$이므로 $q = \\frac{2\\sqrt{6}}{3}$입니다.',
                             'exp_en': '$k = \\sqrt{\\frac{8}{3}} = \\frac{2\\sqrt{6}}{3}$, so $q = '
                                       '\\frac{2\\sqrt{6}}{3}$.'}]},
             {'title': '🌳 4단계 · [빈칸 (다) 구하기] 이등변삼각형 $\\mathrm{BCD}$에서 $r = \\overline{\\mathrm{CD}}$ 찾기',
              'title_en': '🌳 Step 4 · [Blank (다)] Finding $r = \\overline{\\mathrm{CD}}$ in isosceles '
                          '$\\triangle\\mathrm{BCD}$',
              'knowledge': '삼각형 $\\mathrm{BCD}$에서 $\\overline{\\mathrm{CB}} = \\overline{\\mathrm{CD}} = r$로 놓으면 '
                           '코사인법칙에 의해 $32 = r^2 + r^2 - 2r^2 \\cdot \\frac{1}{3} = \\frac{4}{3}r^2$입니다.',
              'knowledge_en': 'In $\\triangle\\mathrm{BCD}$ with $\\overline{\\mathrm{CB}} = \\overline{\\mathrm{CD}} '
                              '= r$, the Law of Cosines gives $32 = 2r^2(1 - 1/3) = \\frac{4}{3}r^2$.',
              'questions': [{'level_label': '빈칸 (다) 도출 디딤돌 4',
                             'level_label_en': 'Blank (다) Step 4',
                             'stem': '$\\frac{4}{3}r^2 = 32$에서 $r^2 = 24$입니다. 빈칸 (다)에 알맞은 양수 $r$의 값은?',
                             'stem_en': 'From $\\frac{4}{3}r^2 = 32$, we have $r^2 = 24$. What is the positive value '
                                        '$r$ in blank (다)?',
                             'options': ['$\\sqrt{6}$', '$2\\sqrt{3}$', '$2\\sqrt{6}$', '$3\\sqrt{6}$', '$4\\sqrt{6}$'],
                             'answer': 3,
                             'exp': '$r = \\sqrt{24} = 2\\sqrt{6}$입니다.',
                             'exp_en': '$r = \\sqrt{24} = 2\\sqrt{6}$.'}]},
             {'title': '💎 5단계 · [최종 종합] $\\dfrac{q \\times r}{p}$의 값 계산하기',
              'title_en': '💎 Step 5 · [Final Synthesis] Calculating $\\dfrac{q \\times r}{p}$',
              'knowledge': '$p = 4\\sqrt{2}$, $q = \\frac{2\\sqrt{6}}{3}$, $r = 2\\sqrt{6}$을 $\\frac{q \\times r}{p}$에 '
                           '대입하여 약분합니다.',
              'knowledge_en': 'Substitute $p = 4\\sqrt{2}$, $q = \\frac{2\\sqrt{6}}{3}$, and $r = 2\\sqrt{6}$ into '
                              '$\\frac{q \\times r}{p}$.',
              'questions': [{'level_label': '최종 종합 디딤돌 5',
                             'level_label_en': 'Final Synthesis Step 5',
                             'stem': '$q \\times r = \\frac{2\\sqrt{6}}{3} \\times 2\\sqrt{6} = 8$이고 $p = 4\\sqrt{2}$일 '
                                     '때, $\\frac{q \\times r}{p}$의 값은?',
                             'stem_en': 'Since $q \\times r = 8$ and $p = 4\\sqrt{2}$, what is $\\frac{q \\times '
                                        'r}{p}$?',
                             'options': ['$\\sqrt{2}$', '$\\sqrt{3}$', '$2$', '$\\sqrt{6}$', '$2\\sqrt{2}$'],
                             'answer': 1,
                             'exp': '$\\frac{8}{4\\sqrt{2}} = \\frac{2}{\\sqrt{2}} = \\sqrt{2}$이므로 정답은 ①입니다.',
                             'exp_en': '$\\frac{8}{4\\sqrt{2}} = \\frac{2}{\\sqrt{2}} = \\sqrt{2}$ (choice ①).'}]}],
  'final': {'stem': '반지름의 길이가 $3$인 원에 내접하는 사각형 $\\mathrm{ABCD}$가 $\\overline{\\mathrm{AB}} = '
                    '3\\overline{\\mathrm{AD}}$, $\\overline{\\mathrm{CB}} = \\overline{\\mathrm{CD}}$, '
                    '$\\cos(\\angle\\mathrm{DCB}) = \\dfrac{1}{3}$을 만족시킬 때, 사각형 $\\mathrm{ABCD}$의 둘레의 길이를 구하는 과정에서 '
                    '(가), (나), (다)에 알맞은 수를 각각 $p, q, r$이라 하자. $\\dfrac{q \\times r}{p}$의 값은? [4점]',
            'stem_en': 'A cyclic quadrilateral $\\mathrm{ABCD}$ inscribed in a circle of radius $3$ satisfies '
                       '$\\overline{\\mathrm{AB}} = 3\\overline{\\mathrm{AD}}$, $\\overline{\\mathrm{CB}} = '
                       '\\overline{\\mathrm{CD}}$, and $\\cos(\\angle\\mathrm{DCB}) = \\dfrac{1}{3}$. Let $p, q, r$ be '
                       'the numbers in blanks (가), (나), (다) representing $\\overline{\\mathrm{BD}}$, '
                       '$\\overline{\\mathrm{AD}}$, and $\\overline{\\mathrm{CD}}$, respectively. What is $\\dfrac{q '
                       '\\times r}{p}$? [4 points]',
            'options': ['$\\sqrt{2}$', '$\\sqrt{3}$', '$2$', '$\\sqrt{6}$', '$2\\sqrt{2}$'],
            'answer': 1,
            'exp': '$p = 4\\sqrt{2}$, $q = \\dfrac{2\\sqrt{6}}{3}$, $r = 2\\sqrt{6}$이므로 $\\dfrac{q \\times r}{p} = '
                   '\\dfrac{8}{4\\sqrt{2}} = \\sqrt{2}$입니다.',
            'exp_en': 'With $p = 4\\sqrt{2}$, $q = \\dfrac{2\\sqrt{6}}{3}$, and $r = 2\\sqrt{6}$, we get $\\dfrac{q '
                      '\\times r}{p} = \\dfrac{8}{4\\sqrt{2}} = \\sqrt{2}$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>원에 내접하는 사각형의 성질과 사인법칙·코사인법칙</b>을 결합한 빈칸 추론 문항입니다. 공통 대각선 '
                        '$\\overline{\\mathrm{BD}}$의 길이를 외접원의 반지름 $R = 3$과 사인법칙으로 먼저 구한 뒤, 양쪽 삼각형 $\\mathrm{ABD}$와 '
                        '$\\mathrm{BCD}$에서 각각 코사인법칙을 적용합니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 빈칸 (가) $p = \\overline{\\mathrm{BD}}$ 구하기</b><br>\n'
                        '  $\\cos(\\angle\\mathrm{DCB}) = \\frac{1}{3}$이고 $0 < \\angle\\mathrm{DCB} < \\pi$이므로 '
                        '$\\sin(\\angle\\mathrm{DCB}) = \\sqrt{1 - \\left(\\frac{1}{3}\\right)^2} = '
                        '\\frac{2\\sqrt{2}}{3}$입니다.<br>\n'
                        '  삼각형 $\\mathrm{BCD}$에서 사인법칙에 의하여:<br>\n'
                        '  $$\\overline{\\mathrm{BD}} = 2R\\sin(\\angle\\mathrm{DCB}) = 6 \\times '
                        '\\frac{2\\sqrt{2}}{3} = 4\\sqrt{2} \\implies p = 4\\sqrt{2}$$<br>\n'
                        '  <b>2단계: 빈칸 (나) $q = \\overline{\\mathrm{AD}}$ 구하기</b><br>\n'
                        '  $\\angle\\mathrm{DAB} = \\pi - \\angle\\mathrm{DCB}$이므로 $\\cos(\\angle\\mathrm{DAB}) = '
                        '-\\frac{1}{3}$입니다. $\\overline{\\mathrm{AD}} = q$, $\\overline{\\mathrm{AB}} = 3q$라 하고 삼각형 '
                        '$\\mathrm{ABD}$에서 코사인법칙을 적용하면:<br>\n'
                        '  $$(4\\sqrt{2})^2 = q^2 + (3q)^2 - 2 \\cdot q \\cdot 3q \\cdot \\left(-\\frac{1}{3}\\right) '
                        '\\implies 32 = 12q^2 \\implies q^2 = \\frac{8}{3} \\implies q = \\frac{2\\sqrt{6}}{3}$$<br>\n'
                        '  <b>3단계: 빈칸 (다) $r = \\overline{\\mathrm{CD}}$ 구하기</b><br>\n'
                        '  삼각형 $\\mathrm{BCD}$에서 $\\overline{\\mathrm{CB}} = \\overline{\\mathrm{CD}} = r$이므로 코사인법칙에 '
                        '의하여:<br>\n'
                        '  $$32 = r^2 + r^2 - 2r^2 \\cdot \\frac{1}{3} = \\frac{4}{3}r^2 \\implies r^2 = 24 \\implies '
                        'r = 2\\sqrt{6}$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 $\\dfrac{q \\times r}{p} = \\dfrac{\\frac{2\\sqrt{6}}{3} \\times '
                        '2\\sqrt{6}}{4\\sqrt{2}} = \\dfrac{8}{4\\sqrt{2}} = \\sqrt{2}$이므로 정답은 <b>①번</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem applies the <b>Law of Sines and Law of Cosines</b> to a cyclic '
                           'quadrilateral inscribed in a circle of radius $R = 3$.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Blank (가) $p = \\overline{\\mathrm{BD}}$</b><br>\n'
                           '  Since $\\sin(\\angle\\mathrm{DCB}) = \\frac{2\\sqrt{2}}{3}$, by the Law of Sines: $p = '
                           '2(3)\\left(\\frac{2\\sqrt{2}}{3}\\right) = 4\\sqrt{2}$.<br><br>\n'
                           '  <b>Step 2: Blank (나) $q = \\overline{\\mathrm{AD}}$</b><br>\n'
                           '  In $\\triangle\\mathrm{ABD}$ with $\\cos(\\angle\\mathrm{DAB}) = -\\frac{1}{3}$, $32 = '
                           'q^2 + 9q^2 + 2q^2 = 12q^2 \\implies q = \\frac{2\\sqrt{6}}{3}$.<br><br>\n'
                           '  <b>Step 3: Blank (다) $r = \\overline{\\mathrm{CD}}$</b><br>\n'
                           '  In $\\triangle\\mathrm{BCD}$, $32 = \\frac{4}{3}r^2 \\implies r = 2\\sqrt{6}$.\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  Thus $\\dfrac{q \\times r}{p} = \\dfrac{8}{4\\sqrt{2}} = \\sqrt{2}$, corresponding to '
                           '<b>choice ①</b>.\n'
                           '</p>'}},
 {'slug': 'c261015',
  'qNum': '15',
  'subject': '공통(수학I·II)',
  'title': '[2026학년도 10월 고3 15번] 사차함수의 이중접선 항등식과 원점을 지나는 직선의 교점 개수',
  'title_en': '[2026 AY Oct Exam Grade 12 #15] Quartic Function Bitangent Identity and Intersection Count with Lines '
              'Through the Origin',
  'summary_ko': '조건 (가)에서 $x=1, 4$에서의 이중접선을 파악하고 조건 (나)의 접선 조건으로 $f(x)=x(x-3)^2(x-4)$ 결정하기',
  'summary_en': 'Deduce the bitangent at $x=1, 4$ from (가) and use the tangency condition at $k=0$ from (나) to find '
                '$f(x)=x(x-3)^2(x-4)$.',
  'tags': ['공통(수학I·II)', '수학II', '미분', '사차함수', '이중접선', '교점의개수', '15번'],
  'symbols': [{'sym': "$f'(1) = f'(4) = \\dfrac{f(4)-f(1)}{3}$",
               'desc': '조건 (가)가 모든 $x$에서 성립할 조건 ($x=1, 4$에서 동시에 접하는 직선)',
               'desc_en': 'Condition (가) implies a common tangent line at $x=1$ and $x=4$.'},
              {'sym': '$g(0) = 0$',
               'desc': '원점을 지나는 직선 $y=kx$와 $y=f(x)$의 교점 개수가 $k=0$에서 불연속',
               'desc_en': 'Number of intersections with $y=kx$ jumps at slope $k=0$, meaning $y=0$ is tangent to '
                          '$y=f(x)$.'},
              {'sym': '$f(x) = x(x-3)^2(x-4)$',
               'desc': '원점을 지나고 $x=3$에서 $x$축에 접하며 $x=1, 4$에서 이중접선을 갖는 사차함수',
               'desc_en': 'Quartic function passing through $(0,0)$ and tangent to $y=0$ at $x=3$.'}],
  'levels': [{'title': '🔰 1단계 · [초등 영(0) 만들기 규칙] 모든 $x$에 대해 $Ax + B = C$가 성립할 조건',
              'title_en': '🔰 Step 1 · [Elementary Zero Rule] Condition for $Ax + B = C$ to hold for all $x$',
              'knowledge': '초등학교에서 어떤 수 $x$를 넣어도 $A \\times x + B$의 값이 항상 일정하려면, $x$에 곱해지는 수 $A$가 반드시 $0$이어야 합니다!',
              'knowledge_en': 'By elementary arithmetic, for $A \\times x + B$ to remain constant regardless of $x$, '
                              'the multiplier $A$ must be $0$.',
              'questions': [{'level_label': '초등 항등식 디딤돌 1',
                             'level_label_en': 'Elementary Identity Step 1',
                             'stem': "모든 실수 $x$에 대하여 $\\{f'(1) - f'(4)\\}x - f'(1) + 4f'(4) = f(4) - f(1)$이 성립하려면 $x$ "
                                     "앞의 계수 $f'(1) - f'(4)$의 값은 얼마여야 할까요?",
                             'stem_en': "For $\\{f'(1) - f'(4)\\}x - f'(1) + 4f'(4) = f(4) - f(1)$ to hold for all "
                                        "real $x$, what must the coefficient $f'(1) - f'(4)$ be?",
                             'options': ['$-2$', '$-1$', '$0$', '$1$', '$2$'],
                             'answer': 3,
                             'exp': "$x$의 값에 관계없이 등식이 성립하려면 $x$의 계수가 $0$이어야 하므로 $f'(1) - f'(4) = 0$, 즉 $f'(1) = "
                                    "f'(4)$입니다.",
                             'exp_en': "The coefficient of $x$ must vanish, so $f'(1) - f'(4) = 0$."}]},
             {'title': "🌿 2단계 · [기울기 비교와 이중접선] $f'(1) = f'(4) = m$일 때 상수항 비교하기",
              'title_en': "🌿 Step 2 · [Bitangent Slope] Comparing constant terms when $f'(1) = f'(4) = m$",
              'knowledge': "1단계에서 $f'(1) = f'(4) = m$이라 놓으면, 조건 (가)의 우변은 $0 \\cdot x - m + 4m = 3m$이 됩니다! 즉 $f(4) - "
                           "f(1) = 3m \\implies \\dfrac{f(4) - f(1)}{4 - 1} = f'(1) = f'(4) = m$이므로, 두 점 $(1, f(1))$과 "
                           '$(4, f(4))$를 잇는 직선 $L(x)$는 $x = 1$과 $x = 4$에서 곡선 $y = f(x)$에 <b>동시에 접하는 이중접선</b>입니다!',
              'knowledge_en': "Setting $f'(1) = f'(4) = m$ reduces (가) to $f(4) - f(1) = 3m$, so the secant line "
                              "through $x=1$ and $x=4$ has slope $m = f'(1) = f'(4)$ and is a bitangent line $L(x)$!",
              'questions': [{'level_label': '이중접선 식 세우기 디딤돌 2',
                             'level_label_en': 'Bitangent Equation Step 2',
                             'stem': '최고차항의 계수가 $1$인 사차함수 $f(x)$가 일차함수 $L(x)$와 $x = 1, x = 4$에서 동시에 접할 때, $f(x) - '
                                     'L(x)$를 인수분해한 식은?',
                             'stem_en': 'When a monic quartic $f(x)$ is tangent to a linear function $L(x)$ at both $x '
                                        '= 1$ and $x = 4$, what is $f(x) - L(x)$?',
                             'options': ['$(x-1)(x-4)$',
                                         '$(x-1)^2(x-4)$',
                                         '$(x-1)(x-4)^2$',
                                         '$(x-1)^2(x-4)^2$',
                                         '$(x-1)^3(x-4)$'],
                             'answer': 4,
                             'exp': '$x = 1$과 $x = 4$에서 각각 접하므로 $(x-1)^2$과 $(x-4)^2$을 인수로 가져 $f(x) - L(x) = '
                                    '(x-1)^2(x-4)^2$입니다.',
                             'exp_en': 'Tangency at both points gives double roots at $1$ and $4$: '
                                       '$(x-1)^2(x-4)^2$.'}]},
             {'title': '🌱 3단계 · [다항식 전개와 $f(0) = 0$ 적용] $f(x) = x(x^3 - 10x^2 + 33x + b)$ 꼴 유도하기',
              'title_en': '🌱 Step 3 · [Expanding & Using $f(0) = 0$] Writing $f(x) = x(x^3 - 10x^2 + 33x + b)$',
              'knowledge': '$(x-1)(x-4) = x^2 - 5x + 4$를 제곱하면:$$(x^2 - 5x + 4)^2 = x^4 - 10x^3 + 33x^2 - 40x + 16$$여기에 '
                           '일차함수 $L(x)$를 더하고 $f(0) = 0$ 조건(상수항이 $0$)을 적용하면 일차항의 계수만 미지수 $b$로 남아 $f(x) = x^4 - 10x^3 + '
                           '33x^2 + bx = x(x^3 - 10x^2 + 33x + b)$가 됩니다!',
              'knowledge_en': 'Expanding $(x^2 - 5x + 4)^2 = x^4 - 10x^3 + 33x^2 - 40x + 16$ and adding the linear '
                              'function $L(x)$ with $f(0) = 0$ leaves $f(x) = x^4 - 10x^3 + 33x^2 + bx = x(x^3 - 10x^2 '
                              '+ 33x + b)$.',
              'questions': [{'level_label': '삼차식 묶어내기 디딤돌 3',
                             'level_label_en': 'Factoring out x Step 3',
                             'stem': '원점을 지나는 직선 $y = kx$와 곡선 $y = f(x) = x(x^3 - 10x^2 + 33x + b)$의 교점을 구하는 방정식 $f(x) '
                                     '= kx$에서, 원점($x = 0$)이 아닌 교점들은 삼차함수 $P(x) = x^3 - 10x^2 + 33x + b$가 얼마가 되는 점들인가요?',
                             'stem_en': 'In solving $f(x) = kx \\iff x(x^3 - 10x^2 + 33x + b - k) = 0$, non-zero '
                                        'intersections satisfy $P(x) = x^3 - 10x^2 + 33x + b =$ what value?',
                             'options': ['$0$', '$1$', '$k$', '$b$', '$-k$'],
                             'answer': 3,
                             'exp': '$x \\neq 0$일 때 $x^3 - 10x^2 + 33x + b = k$, 즉 삼차함수 $y = P(x)$와 가로선 $y = k$의 교점이 '
                                    '됩니다!',
                             'exp_en': 'For $x \\neq 0$, $P(x) = k$.'}]},
             {'title': "🌱 4단계 · [삼차함수 $P(x)$의 극점 찾기] $P'(x) = 3x^2 - 20x + 33 = 0$ 인수분해하기",
              'title_en': "🌱 Step 4 · [Extrema of $P(x)$] Factoring $P'(x) = 3x^2 - 20x + 33 = 0$",
              'knowledge': '가로선 $y = k$를 위아래로 움직일 때 삼차함수 $y = P(x) = x^3 - 10x^2 + 33x + b$와의 교점 개수가 갑자기 바뀌는(불연속이 되는) '
                           "순간은 바로 $y = k$가 <b>$P(x)$의 극대점 또는 극소점을 지날 때</b>입니다! 이를 위해 $P'(x) = 3x^2 - 20x + 33$을 인수분해해 "
                           '봅시다.',
              'knowledge_en': 'The number of intersections between $y = P(x)$ and the horizontal line $y = k$ jumps '
                              "when $k$ equals a local extremum of $P(x)$. Differentiating gives $P'(x) = 3x^2 - 20x + "
                              '33$.',
              'questions': [{'level_label': '도함수 인수분해 디딤돌 4',
                             'level_label_en': 'Factoring Derivative Step 4',
                             'stem': "$P'(x) = 3x^2 - 20x + 33 = (3x - 11)(x - c) = 0$으로 인수분해할 때, 자연수인 극대점의 $x$좌표 $c$의 "
                                     '값은?',
                             'stem_en': 'Factoring $3x^2 - 20x + 33 = (3x - 11)(x - c) = 0$, what is the integer root '
                                        '$c$?',
                             'options': ['$1$', '$2$', '$3$', '$4$', '$5$'],
                             'answer': 3,
                             'exp': '$3x^2 - 20x + 33 = (3x - 11)(x - 3) = 0$이므로 $x = 3$(극대)과 $x = '
                                    '\\frac{11}{3}$(극소)에서 극값을 가집니다.',
                             'exp_en': '$3x^2 - 20x + 33 = (3x - 11)(x - 3)$, so $c = 3$.'}]},
             {'title': '🌳 5단계 · [조건 (나) $g(0) = 0$과 부호 조건] $P(3) = 0$으로 상수 $b$ 구하기',
              'title_en': '🌳 Step 5 · [Condition (나) & Sign Check] Using $P(3) = 0$ to find $b = -36$',
              'knowledge': '문제에서 $f\\left(\\dfrac{7}{2}\\right) < 0$이라고 했습니다. $\\dfrac{7}{2} = 3.5$는 $3$과 '
                           '$\\dfrac{11}{3} \\approx 3.67$ 사이의 수입니다!<ul><li>만약 극솟값 $P\\left(\\frac{11}{3}\\right) = '
                           '0$이면, 모든 $x > 0$에서 $P(x) \\ge 0$이 되어 $f\\left(\\frac{7}{2}\\right) > 0$이 되므로 '
                           '모순입니다!</li><li>따라서 <b>극댓값 $P(3) = 0$</b>이어야 하며, 이때 $k = 0$($g(0) = 0$)에서 접선이 되어 불연속이 되고 '
                           '$f\\left(\\frac{7}{2}\\right) < 0$도 완벽히 성립합니다!</li></ul>',
              'knowledge_en': 'Since $\\frac{7}{2} = 3.5 \\in \\left(3, \\frac{11}{3}\\right)$ and '
                              '$f\\left(\\frac{7}{2}\\right) < 0$, the local minimum $P\\left(\\frac{11}{3}\\right)$ '
                              'must be negative, so the local maximum must satisfy $P(3) = 0$ (making $g(0) = 0$).',
              'questions': [{'level_label': '상수 b 결정 디딤돌 5',
                             'level_label_en': 'Finding Constant b Step 5',
                             'stem': '$P(x) = x^3 - 10x^2 + 33x + b$에서 $P(3) = 3^3 - 10(3^2) + 33(3) + b = 27 - 90 + '
                                     '99 + b = 0$일 때, 상수 $b$의 값은?',
                             'stem_en': 'From $P(3) = 27 - 90 + 99 + b = 0$, what is the value of $b$?',
                             'options': ['$-40$', '$-36$', '$-32$', '$-28$', '$-24$'],
                             'answer': 2,
                             'exp': '$27 - 90 + 99 = 36$이므로 $36 + b = 0 \\implies b = -36$입니다.',
                             'exp_en': '$36 + b = 0 \\implies b = -36$.'}]},
             {'title': '🌳 6단계 · [$f(x)$ 인수분해 완성] $f(x) = x(x-3)^2(x-4)$로 나타내기',
              'title_en': '🌳 Step 6 · [Factoring $f(x)$] Writing $f(x) = x(x-3)^2(x-4)$',
              'knowledge': '$b = -36$일 때 $P(x) = x^3 - 10x^2 + 33x - 36$은 $x = 3$에서 극대이자 $0$이므로 $(x - 3)^2$을 인수로 가집니다! '
                           '최고차항과 상수항($-36 = 9 \\times (-4)$)을 비교하면 $P(x) = (x - 3)^2(x - 4)$가 되어, 드디어 사차함수 $f(x)$가 '
                           '완성됩니다:$$f(x) = x(x - 3)^2(x - 4)$$',
              'knowledge_en': "Since $P(3) = P'(3) = 0$, $(x-3)^2$ divides $P(x) = x^3 - 10x^2 + 33x - 36$, giving "
                              '$P(x) = (x-3)^2(x-4)$ and $f(x) = x(x-3)^2(x-4)$.',
              'questions': [{'level_label': '부호 조건 검산 디딤돌 6',
                             'level_label_en': 'Sign Verification Step 6',
                             'stem': '완성된 $f(x) = x(x - 3)^2(x - 4)$에 $x = \\dfrac{7}{2}$을 대입하여 검산할 때, 마지막 인수 '
                                     '$\\left(\\dfrac{7}{2} - 4\\right)$의 값은?',
                             'stem_en': 'When checking $x = \\dfrac{7}{2}$ in $f(x) = x(x-3)^2(x-4)$, what is the last '
                                        'factor $\\left(\\dfrac{7}{2} - 4\\right)$?',
                             'options': ['$-\\frac{3}{2}$', '$-1$', '$-\\frac{1}{2}$', '$\\frac{1}{2}$', '$1$'],
                             'answer': 3,
                             'exp': '$\\frac{7}{2} - \\frac{8}{2} = -\\frac{1}{2} < 0$이므로 '
                                    '$f\\left(\\frac{7}{2}\\right) = \\frac{7}{2} \\times \\frac{1}{4} \\times '
                                    '\\left(-\\frac{1}{2}\\right) = -\\frac{7}{16} < 0$이 성립합니다!',
                             'exp_en': '$\\frac{7}{2} - 4 = -\\frac{1}{2} < 0$, confirming $f(7/2) < 0$.'}]},
             {'title': '💎 7단계 · [$x = 5$ 대입 준비] $(5 - 3)^2$과 $(5 - 4)$ 계산하기',
              'title_en': '💎 Step 7 · [Substituting $x = 5$] Computing $(5 - 3)^2$ and $(5 - 4)$',
              'knowledge': '이제 $f(x) = x(x - 3)^2(x - 4)$에 $x = 5$를 대입하여 각 인수의 값을 구합니다.',
              'knowledge_en': 'Substitute $x = 5$ into each factor of $f(x) = x(x - 3)^2(x - 4)$.',
              'questions': [{'level_label': '인수 계산 디딤돌 7',
                             'level_label_en': 'Factor Evaluation Step 7',
                             'stem': '$x = 5$일 때, $(x - 3)^2 \\times (x - 4) = (5 - 3)^2 \\times (5 - 4)$의 값은?',
                             'stem_en': 'For $x = 5$, what is $(5 - 3)^2 \\times (5 - 4)$?',
                             'options': ['$1$', '$2$', '$4$', '$8$', '$9$'],
                             'answer': 3,
                             'exp': '$(5 - 3)^2 \\times (5 - 4) = 2^2 \\times 1 = 4$입니다.',
                             'exp_en': '$2^2 \\times 1 = 4$.'}]},
             {'title': '🏆 8단계 · [최종 정답 완성] $f(5) = 5 \\times 4$ 계산하기',
              'title_en': '🏆 Step 8 · [Final Synthesis] Evaluating $f(5) = 5 \\times 4$',
              'knowledge': '앞의 $x = 5$와 7단계에서 구한 $4$를 곱하면 최종 정답 $f(5) = 20$이 완성됩니다.',
              'knowledge_en': 'Multiply $x = 5$ by $4$ to obtain $f(5) = 20$.',
              'questions': [{'level_label': '최종 종합 디딤돌 8',
                             'level_label_en': 'Final Synthesis Step 8',
                             'stem': '$f(x) = x(x - 3)^2(x - 4)$일 때, $f(5)$의 값은?',
                             'stem_en': 'For $f(x) = x(x - 3)^2(x - 4)$, what is the value of $f(5)$?',
                             'options': ['$14$', '$16$', '$18$', '$20$', '$22$'],
                             'answer': 4,
                             'exp': '$f(5) = 5 \\times (5-3)^2 \\times (5-4) = 5 \\times 4 \\times 1 = 20$이므로 정답은 '
                                    '④입니다.',
                             'exp_en': '$f(5) = 20$ (choice ④).'}]}],
  'final': {'stem': '최고차항의 계수가 $1$이고 $f(0) = 0$, $f\\left(\\dfrac{7}{2}\\right) < 0$인 사차함수 $f(x)$가 다음 조건을 만족시킬 때, '
                    "$f(5)$의 값은? [4점]<br><br>(가) 모든 실수 $x$에 대하여 $f(4) - f(1) = \\{f'(1) - f'(4)\\}x - f'(1) + 4f'(4)$ "
                    '이다.<br>(나) 실수 $t$에 대하여 곡선 $y = f(x)$와 직선 $y = kx$의 교점의 개수를 $h(k)$라 할 때, $\\lim_{k \\to t-} h(k) '
                    '\\neq \\lim_{k \\to t+} h(k)$를 만족시키는 모든 실수 $t$를 작은 수부터 크기순으로 나열한 것을 $g(0), g(1), \\cdots, g(m)$ '
                    '($m$은 자연수)라 하면 $g(0) = 0$이다.',
            'stem_en': 'A monic quartic function $f(x)$ with $f(0) = 0$ and $f\\left(\\dfrac{7}{2}\\right) < 0$ '
                       "satisfies:<br>(가) $f(4) - f(1) = \\{f'(1) - f'(4)\\}x - f'(1) + 4f'(4)$ for all real "
                       '$x$.<br>(나) Let $h(k)$ be the number of intersections between $y = f(x)$ and $y = kx$. Listing '
                       'all $t$ where $\\lim_{k \\to t-} h(k) \\neq \\lim_{k \\to t+} h(k)$ in increasing order as '
                       '$g(0), g(1), \\dots, g(m)$ gives $g(0) = 0$.<br>What is the value of $f(5)$? [4 points]',
            'options': ['$14$', '$16$', '$18$', '$20$', '$22$'],
            'answer': 4,
            'exp': '조건 (가)에서 $x=1, 4$에서의 이중접선을 이용해 $f(x) = x(x^3 - 10x^2 + 33x + b)$를 얻고, 조건 (나)와 $f(7/2) < 0$에서 '
                   '$x=3$이 중근임을 얻어 $f(x) = x(x-3)^2(x-4)$입니다. 따라서 $f(5) = 20$입니다.',
            'exp_en': 'Condition (가) yields a bitangent at $x=1, 4$, giving $f(x) = x(x^3 - 10x^2 + 33x + b)$. '
                      'Condition (나) and $f(7/2) < 0$ imply a double root at $x=3$, so $f(x) = x(x-3)^2(x-4)$ and '
                      '$f(5) = 20$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 공통 객관식 킬러(15번) 문항으로, <b>항등식을 통한 사차함수의 이중접선 추론</b>과 <b>원점을 지나는 직선과의 교점 개수 불연속점(접선의 '
                        '기울기)</b>을 결합한 고난도 문제입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 조건 (가)의 항등식 해석 (이중접선)</b><br>\n'
                        '  조건 (가)가 모든 실수 $x$에 대하여 성립하므로 $x$의 계수는 $0$이어야 합니다:<br>\n'
                        "  $$f'(1) - f'(4) = 0 \\implies f'(1) = f'(4) = m$$\n"
                        "  이를 상수항에 대입하면 $f(4) - f(1) = 3m \\implies \\frac{f(4) - f(1)}{4 - 1} = f'(1) = f'(4) = "
                        'm$입니다.<br>\n'
                        '  즉, 직선 $L(x) = m(x-1) + f(1)$은 곡선 $y = f(x)$에 $x = 1$과 $x = 4$에서 동시에 접하는 이중접선입니다.<br>\n'
                        '  따라서 최고차항의 계수가 $1$이고 $f(0) = 0$이므로:<br>\n'
                        '  $$f(x) = (x-1)^2(x-4)^2 + mx - 16 = x^4 - 10x^3 + 33x^2 + bx = x(x^3 - 10x^2 + 33x + '
                        'b)$$<br>\n'
                        '  <b>2단계: 조건 (나)의 불연속 기울기 해석</b><br>\n'
                        '  원점을 지나는 직선 $y = kx$와 $y = f(x)$의 교점의 개수 $h(k)$는 $x(x^3 - 10x^2 + 33x + b - k) = 0$의 서로 다른 '
                        '실근의 개수입니다.<br>\n'
                        "  $P(x) = x^3 - 10x^2 + 33x + b$라 하면 $P'(x) = 3x^2 - 20x + 33 = (3x - 11)(x - 3) = 0$에서 극댓값은 "
                        '$P(3)$, 극솟값은 $P\\left(\\frac{11}{3}\\right)$입니다.<br>\n'
                        '  $f\\left(\\frac{7}{2}\\right) < 0$을 만족하면서 $k = 0$에서 불연속이 되려면 $P(3) = 0$이어야 하므로 $b = -36$이고 '
                        '$f(x) = x(x-3)^2(x-4)$입니다.\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 $f(x) = x(x-3)^2(x-4)$이므로:<br>\n'
                        '  $$f(5) = 5 \\times (5-3)^2 \\times (5-4) = 5 \\times 4 \\times 1 = 20$$\n'
                        '  정답은 <b>④번</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem combines <b>bitangent properties of quartic functions</b> with '
                           '<b>discontinuities in the number of intersections with lines through the origin</b>.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Bitangent from Condition (가)</b><br>\n'
                           "  Since (가) holds for all $x$, $f'(1) = f'(4) = \\frac{f(4)-f(1)}{3}$, meaning $y=f(x)$ "
                           'has a bitangent at $x=1$ and $x=4$. Using $f(0)=0$:\n'
                           '  $$f(x) = (x-1)^2(x-4)^2 + mx - 16 = x(x^3 - 10x^2 + 33x + b)$$<br>\n'
                           '  <b>Step 2: Tangency at $k = 0$ from Condition (나)</b><br>\n'
                           '  For $h(k)$ to jump at $k=0$, $P(x) = x^3 - 10x^2 + 33x + b = 0$ must have a double root '
                           "at an extremum. Since $P'(x) = (3x-11)(x-3)$ and $f(7/2) < 0$, the double root is at $x = "
                           '3$, giving $b = -36$ and $f(x) = x(x-3)^2(x-4)$.\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  Evaluating at $x = 5$ gives $f(5) = 5(2)^2(1) = 20$, which is <b>choice ④</b>.\n'
                           '</p>'}},
 {'slug': 'c261016',
  'qNum': '16',
  'subject': '공통(수학I·II)',
  'title': '[2026학년도 10월 고3 16번] 합의 기호 시그마(Σ)의 선형성과 상수의 합',
  'title_en': '[2026 AY Oct Exam Grade 12 #16] Linearity of Sigma Notation and Sum of Constants',
  'summary_ko': '$1$이 $7$번 더해진 값을 먼저 빼서 $a_k$의 합을 구하고 $3$배하여 정답 도출하기',
  'summary_en': 'Subtract the sum of seven $1$s to find the sum of $a_k$, then multiply by $3$.',
  'tags': ['공통(수학I·II)', '수학I', '수열', '시그마의성질', '단답형', '16번'],
  'symbols': [{'sym': '$\\sum_{k=1}^{7} 1 = 7$',
               'desc': '1을 첫째항부터 7번째항까지 7번 더하면 7',
               'desc_en': 'Adding 1 seven times equals 7.'},
              {'sym': '$\\sum_{k=1}^{7} 3a_k = 3\\sum_{k=1}^{7} a_k$',
               'desc': '각 항에 곱해진 3은 시그마 밖으로 묶어낼 수 있음',
               'desc_en': 'Constant factor 3 can be factored out of the summation.'}],
  'levels': [{'title': '🔰 1단계 · [초등 덧셈] $1$을 $7$번 더하면 얼마일까?',
              'title_en': '🔰 Step 1 · [Elementary Addition] Adding $1$ seven times',
              'knowledge': "초등학교 덧셈에서 $1 + 1 + 1 + 1 + 1 + 1 + 1 = 7$입니다. 시그마 기호 $\\sum_{k=1}^{7} 1$은 바로 '$1$을 $7$번 "
                           "더하라'는 뜻입니다.",
              'knowledge_en': 'In elementary addition, adding $1$ seven times gives $7$. That is exactly what '
                              '$\\sum_{k=1}^{7} 1$ means.',
              'questions': [{'level_label': '초등 덧셈 디딤돌 1',
                             'level_label_en': 'Elementary Addition Step 1',
                             'stem': '초등학교 덧셈 원리에 따라 $1$을 $7$번 더한 값 $\\sum_{k=1}^{7} 1$은 얼마인가요?',
                             'stem_en': 'Using elementary addition, what is $\\sum_{k=1}^{7} 1$ (adding $1$ seven '
                                        'times)?',
                             'options': ['$1$', '$3$', '$5$', '$7$', '$10$'],
                             'answer': 4,
                             'exp': '$1 \\times 7 = 7$입니다. (주의: $1$이 아니라 $7$입니다!)',
                             'exp_en': '$1 \\times 7 = 7$.'}]},
             {'title': '🌿 2단계 · [시그마 분리] $\\sum_{k=1}^{7} a_k$의 값 구하기',
              'title_en': '🌿 Step 2 · [Splitting Sigma] Finding $\\sum_{k=1}^{7} a_k$',
              'knowledge': '$\\sum_{k=1}^{7} (a_k + 1) = \\sum_{k=1}^{7} a_k + \\sum_{k=1}^{7} 1 = 30$이므로, '
                           '$\\sum_{k=1}^{7} a_k + 7 = 30$입니다.',
              'knowledge_en': 'Since $\\sum_{k=1}^{7} a_k + 7 = 30$, subtract $7$ from $30$.',
              'questions': [{'level_label': '뺄셈 디딤돌 2',
                             'level_label_en': 'Subtraction Step 2',
                             'stem': '$\\sum_{k=1}^{7} a_k + 7 = 30$일 때, $\\sum_{k=1}^{7} a_k$의 값은?',
                             'stem_en': 'Given $\\sum_{k=1}^{7} a_k + 7 = 30$, what is $\\sum_{k=1}^{7} a_k$?',
                             'options': ['$21$', '$22$', '$23$', '$24$', '$29$'],
                             'answer': 3,
                             'exp': '$30 - 7 = 23$입니다.',
                             'exp_en': '$30 - 7 = 23$.'}]},
             {'title': '🌱 3단계 · [실수배 성질] 상수 $3$을 시그마 밖으로 꺼내기',
              'title_en': '🌱 Step 3 · [Constant Multiple Rule] Factoring $3$ out of the sum',
              'knowledge': '$3a_1 + 3a_2 + \\cdots + 3a_7 = 3(a_1 + a_2 + \\cdots + a_7)$이므로 $\\sum_{k=1}^{7} 3a_k = 3 '
                           '\\sum_{k=1}^{7} a_k$입니다.',
              'knowledge_en': 'By the distributive property, $\\sum_{k=1}^{7} 3a_k = 3 \\sum_{k=1}^{7} a_k$.',
              'questions': [{'level_label': '실수배 공식 디딤돌 3',
                             'level_label_en': 'Constant Multiple Step 3',
                             'stem': '$\\sum_{k=1}^{7} a_k = 23$일 때, $\\sum_{k=1}^{7} 3a_k$를 구하기 위해 해야 할 계산은?',
                             'stem_en': 'Given $\\sum_{k=1}^{7} a_k = 23$, which expression equals $\\sum_{k=1}^{7} '
                                        '3a_k$?',
                             'options': ['$23 + 3$', '$23 - 3$', '$3 \\times 23$', '$7 \\times 23$', '$21 \\times 23$'],
                             'answer': 3,
                             'exp': '시그마의 실수배 성질에 의해 $3 \\times 23$을 계산하면 됩니다.',
                             'exp_en': 'By linearity, multiply $23$ by $3$.'}]},
             {'title': '🌳 4단계 · [자리수 곱셈] $3 \\times 20$과 $3 \\times 3$ 계산하기',
              'title_en': '🌳 Step 4 · [Place Value Multiplication] Computing $3 \\times 20$ and $3 \\times 3$',
              'knowledge': '$3 \\times 23$은 십의 자리 $3 \\times 20 = 60$과 일의 자리 $3 \\times 3 = 9$를 더하여 계산합니다.',
              'knowledge_en': 'Break $3 \\times 23$ into $3 \\times 20 = 60$ plus $3 \\times 3 = 9$.',
              'questions': [{'level_label': '곱셈 확인 디딤돌 4',
                             'level_label_en': 'Multiplication Check Step 4',
                             'stem': '$3 \\times 20 + 3 \\times 3$에서 일의 자리 숫자 $3 \\times 3$은 얼마인가요?',
                             'stem_en': 'In $3 \\times 20 + 3 \\times 3$, what is the ones digit $3 \\times 3$?',
                             'options': ['$3$', '$6$', '$7$', '$8$', '$9$'],
                             'answer': 5,
                             'exp': '$3 \\times 3 = 9$입니다.',
                             'exp_en': '$3 \\times 3 = 9$.'}]},
             {'title': '💎 5단계 · [최종 종합] $\\sum_{k=1}^{7} 3a_k$의 최종 값 구하기',
              'title_en': '💎 Step 5 · [Final Synthesis] Final value of $\\sum_{k=1}^{7} 3a_k$',
              'knowledge': '$60 + 9 = 69$로 단답형 정답을 구합니다.',
              'knowledge_en': 'Add $60 + 9 = 69$ to get the final answer.',
              'questions': [{'level_label': '최종 종합 디딤돌 5',
                             'level_label_en': 'Final Synthesis Step 5',
                             'stem': '$\\sum_{k=1}^{7} 3a_k = 3 \\times 23$의 값은?',
                             'stem_en': 'What is the value of $\\sum_{k=1}^{7} 3a_k = 3 \\times 23$?',
                             'options': ['$63$', '$66$', '$69$', '$72$', '$87$'],
                             'answer': 3,
                             'exp': '$3 \\times 23 = 69$입니다.',
                             'exp_en': '$3 \\times 23 = 69$.'}]}],
  'final': {'stem': '수열 $\\{a_n\\}$에 대하여 $\\sum_{k=1}^{7} (a_k + 1) = 30$일 때, $\\sum_{k=1}^{7} 3a_k$의 값을 구하시오. [3점]',
            'stem_en': 'For a sequence $\\{a_n\\}$, when $\\sum_{k=1}^{7} (a_k + 1) = 30$, find the value of '
                       '$\\sum_{k=1}^{7} 3a_k$. [3 points]',
            'options': ['$63$', '$66$', '$69$', '$72$', '$87$'],
            'answer': 3,
            'exp': '$\\sum_{k=1}^{7} a_k + 7 = 30 \\implies \\sum_{k=1}^{7} a_k = 23$이므로 $\\sum_{k=1}^{7} 3a_k = 3 '
                   '\\times 23 = 69$입니다.',
            'exp_en': 'Since $\\sum_{k=1}^{7} a_k = 30 - 7 = 23$, we have $\\sum_{k=1}^{7} 3a_k = 3 \\times 23 = 69$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>합의 기호 $\\sum$의 기본 성질(선형성과 상수합 공식)</b>을 정확히 적용할 수 있는지를 묻는 단답형 첫 문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 시그마를 분리하여 $\\sum_{k=1}^{7} a_k$ 구하기</b><br>\n'
                        '  $$\\sum_{k=1}^{7} (a_k + 1) = \\sum_{k=1}^{7} a_k + \\sum_{k=1}^{7} 1 = \\sum_{k=1}^{7} a_k '
                        '+ 7 = 30$$\n'
                        '  따라서 $\\sum_{k=1}^{7} a_k = 30 - 7 = 23$입니다.<br><br>\n'
                        '  <b>2단계: 실수배 성질 적용하기</b><br>\n'
                        '  $$\\sum_{k=1}^{7} 3a_k = 3 \\sum_{k=1}^{7} a_k = 3 \\times 23 = 69$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 구하는 값은 <b>$69$</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This short-answer problem tests the <b>linearity of summation notation '
                           '($\\sum$)</b>.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Isolate $\\sum_{k=1}^{7} a_k$</b><br>\n'
                           '  $$\\sum_{k=1}^{7} a_k = 30 - \\sum_{k=1}^{7} 1 = 30 - 7 = 23$$<br>\n'
                           '  <b>Step 2: Multiply by $3$</b><br>\n'
                           '  $$\\sum_{k=1}^{7} 3a_k = 3 \\times 23 = 69$$\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  The final answer is <b>$69$</b>.\n'
                           '</p>'}},
 {'slug': 'c261017',
  'qNum': '17',
  'subject': '공통(수학I·II)',
  'title': '[2026학년도 10월 고3 17번] 다항함수의 부정적분과 적분상수의 결정',
  'title_en': '[2026 AY Oct Exam Grade 12 #17] Indefinite Integral of a Polynomial and Constant of Integration',
  'summary_ko': '$f(x)=3x^2+4x-1$을 적분하고 $F(0)=1$을 이용해 $F(x)$를 완성한 뒤 $F(2)$ 구하기',
  'summary_en': 'Integrate $f(x)=3x^2+4x-1$, use $F(0)=1$ to find the integration constant, and evaluate $F(2)$.',
  'tags': ['공통(수학I·II)', '수학II', '적분', '부정적분', '적분상수', '단답형', '17번'],
  'symbols': [{'sym': '$\\int x^n dx = \\dfrac{1}{n+1}x^{n+1} + C$',
               'desc': '차수를 1 늘리고 그 차수로 나누는 부정적분 공식',
               'desc_en': 'Power rule for indefinite integration.'},
              {'sym': '$F(0) = C = 1$',
               'desc': '$x=0$을 대입했을 때 남는 상수항(적분상수)',
               'desc_en': 'Evaluating at $x=0$ directly gives the constant term $C$.'}],
  'levels': [{'title': '🔰 1단계 · [초등 거꾸로 셈] 미분해서 $3x^2$이 되는 식 찾기',
              'title_en': '🔰 Step 1 · [Elementary Reverse Operation] Finding what differentiates to $3x^2$',
              'knowledge': '초등학교에서 덧셈의 반대가 뺄셈이듯, 미분의 반대는 적분입니다. $x^3$을 미분하면 지수 $3$이 앞으로 내려와 $3x^2$이 되므로, 거꾸로 $3x^2$을 '
                           '적분하면 $x^3$이 됩니다.',
              'knowledge_en': 'Just as subtraction reverses addition in elementary math, integration reverses '
                              "differentiation. Since $(x^3)' = 3x^2$, the antiderivative of $3x^2$ is $x^3$.",
              'questions': [{'level_label': '초등 거꾸로 연산 디딤돌 1',
                             'level_label_en': 'Elementary Reverse Rule Step 1',
                             'stem': "초등학교 거꾸로 계산하기처럼 미분해서 $4x$가 되는 이차항을 찾으면? (힌트: $(x^2)' = 2x$입니다.)",
                             'stem_en': 'Using elementary reverse reasoning, which quadratic term differentiates to '
                                        '$4x$?',
                             'options': ['$x^2$', '$2x^2$', '$3x^2$', '$4x^2$', '$8x^2$'],
                             'answer': 2,
                             'exp': "$(2x^2)' = 2 \\times 2x = 4x$이므로 $4x$를 적분하면 $2x^2$이 됩니다.",
                             'exp_en': "Since $(2x^2)' = 4x$, integrating $4x$ gives $2x^2$."}]},
             {'title': '🌿 2단계 · [부정적분 식 세우기] $F(x) = x^3 + 2x^2 - x + C$에서 적분상수 $C$ 찾기',
              'title_en': '🌿 Step 2 · [Integration Constant] Finding $C$ in $F(x) = x^3 + 2x^2 - x + C$',
              'knowledge': '$f(x) = 3x^2 + 4x - 1$의 한 부정적분은 $F(x) = x^3 + 2x^2 - x + C$입니다. 여기에 $x = 0$을 넣으면 $F(0) = '
                           'C$가 됩니다.',
              'knowledge_en': 'Substituting $x = 0$ into $F(x) = x^3 + 2x^2 - x + C$ gives $F(0) = C$.',
              'questions': [{'level_label': '적분상수 결정 디딤돌 2',
                             'level_label_en': 'Integration Constant Step 2',
                             'stem': '조건에서 $F(0) = 1$일 때, 적분상수 $C$의 값은?',
                             'stem_en': 'Given $F(0) = 1$, what is the constant of integration $C$?',
                             'options': ['$-1$', '$0$', '$1$', '$2$', '$3$'],
                             'answer': 3,
                             'exp': '$F(0) = 0 + 0 - 0 + C = 1$이므로 $C = 1$입니다.',
                             'exp_en': '$F(0) = C = 1$.'}]},
             {'title': '🌱 3단계 · [거듭제곱 대입] $x = 2$일 때 $x^3 + 2x^2$ 계산하기',
              'title_en': '🌱 Step 3 · [Power Substitution] Computing $x^3 + 2x^2$ at $x = 2$',
              'knowledge': '$x = 2$를 대입하면 $2^3 = 8$이고 $2 \\times 2^2 = 2 \\times 4 = 8$입니다.',
              'knowledge_en': 'At $x = 2$, $2^3 = 8$ and $2(2^2) = 8$.',
              'questions': [{'level_label': '거듭제곱 합 디딤돌 3',
                             'level_label_en': 'Sum of Powers Step 3',
                             'stem': '$x = 2$일 때 $x^3 + 2x^2 = 8 + 8$을 계산한 값은?',
                             'stem_en': 'At $x = 2$, what is $x^3 + 2x^2 = 8 + 8$?',
                             'options': ['$12$', '$14$', '$16$', '$18$', '$20$'],
                             'answer': 3,
                             'exp': '$8 + 8 = 16$입니다.',
                             'exp_en': '$8 + 8 = 16$.'}]},
             {'title': '🌳 4단계 · [일차항과 상수항 계산] $-x + 1$에 $x = 2$ 대입하기',
              'title_en': '🌳 Step 4 · [Linear & Constant Terms] Evaluating $-x + 1$ at $x = 2$',
              'knowledge': '$-x + 1$에 $x = 2$를 대입하면 $-2 + 1 = -1$입니다.',
              'knowledge_en': 'Substituting $x = 2$ into $-x + 1$ gives $-2 + 1 = -1$.',
              'questions': [{'level_label': '일차항 대입 디딤돌 4',
                             'level_label_en': 'Linear Substitution Step 4',
                             'stem': '$x = 2$일 때 $-x + 1$의 값은?',
                             'stem_en': 'At $x = 2$, what is the value of $-x + 1$?',
                             'options': ['$-3$', '$-2$', '$-1$', '$0$', '$1$'],
                             'answer': 3,
                             'exp': '$-2 + 1 = -1$입니다.',
                             'exp_en': '$-2 + 1 = -1$.'}]},
             {'title': '💎 5단계 · [최종 종합] $F(2)$의 값 완성하기',
              'title_en': '💎 Step 5 · [Final Synthesis] Completing $F(2)$',
              'knowledge': '앞에서 구한 $16$과 $-1$을 더하면 $F(2)$가 완성됩니다.',
              'knowledge_en': 'Combine $16$ and $-1$ to get $F(2)$.',
              'questions': [{'level_label': '최종 종합 디딤돌 5',
                             'level_label_en': 'Final Synthesis Step 5',
                             'stem': '$F(2) = 8 + 8 - 2 + 1$의 최종 값은?',
                             'stem_en': 'What is the final value of $F(2) = 8 + 8 - 2 + 1$?',
                             'options': ['$13$', '$14$', '$15$', '$16$', '$17$'],
                             'answer': 3,
                             'exp': '$16 - 1 = 15$입니다.',
                             'exp_en': '$16 - 1 = 15$.'}]}],
  'final': {'stem': '함수 $f(x) = 3x^2 + 4x - 1$에 대하여 $f(x)$의 한 부정적분을 $F(x)$라 하자. $F(0) = 1$일 때, $F(2)$의 값을 구하시오. [3점]',
            'stem_en': 'Let $F(x)$ be an indefinite integral of $f(x) = 3x^2 + 4x - 1$. Given $F(0) = 1$, find the '
                       'value of $F(2)$. [3 points]',
            'options': ['$13$', '$14$', '$15$', '$16$', '$17$'],
            'answer': 3,
            'exp': '$F(x) = x^3 + 2x^2 - x + 1$이므로 $F(2) = 8 + 8 - 2 + 1 = 15$입니다.',
            'exp_en': 'Since $F(x) = x^3 + 2x^2 - x + 1$, evaluating at $x = 2$ gives $F(2) = 8 + 8 - 2 + 1 = 15$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>다항함수의 부정적분 공식</b>을 적용하고 초기 조건 $F(0) = 1$로부터 적분상수 $C$를 구하는 기본 문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 부정적분 $F(x)$ 구하기</b><br>\n'
                        '  $$F(x) = \\int (3x^2 + 4x - 1)dx = x^3 + 2x^2 - x + C \\quad (\\text{단, } C\\text{는 '
                        '적분상수})$$\n'
                        '  $F(0) = 1$이므로 $C = 1$이고, $F(x) = x^3 + 2x^2 - x + 1$입니다.<br><br>\n'
                        '  <b>2단계: $F(2)$ 계산하기</b><br>\n'
                        '  $$F(2) = 2^3 + 2(2^2) - 2 + 1 = 8 + 8 - 2 + 1 = 15$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 구하는 값은 <b>$15$</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem evaluates the <b>indefinite integral of a polynomial function</b> given an '
                           'initial value $F(0) = 1$.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Find $F(x)$</b><br>\n'
                           '  $$F(x) = x^3 + 2x^2 - x + C$$\n'
                           '  Using $F(0) = 1$ gives $C = 1$.<br><br>\n'
                           '  <b>Step 2: Evaluate $F(2)$</b><br>\n'
                           '  $$F(2) = 8 + 8 - 2 + 1 = 15$$\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  The final answer is <b>$15$</b>.\n'
                           '</p>'}},
 {'slug': 'c261018',
  'qNum': '18',
  'subject': '공통(수학I·II)',
  'title': '[2026학년도 10월 고3 18번] 사인함수의 최솟값과 삼각함수의 함숫값 계산',
  'title_en': '[2026 AY Oct Exam Grade 12 #18] Minimum Value of a Sine Function and Function Evaluation',
  'summary_ko': '사인함수의 최솟값 $-4+a=1$에서 $a=5$를 구하고 $x=\\dfrac{\\pi}{2}$를 대입하여 함숫값 $7$ 구하기',
  'summary_en': 'Use the minimum value $-4+a=1$ to find $a=5$, then substitute $x=\\dfrac{\\pi}{2}$ to obtain '
                '$f\\!\\left(\\dfrac{\\pi}{2}\\right)=7$.',
  'tags': ['공통(수학I·II)', '수학I', '삼각함수', '삼각함수의그래프', '최솟값', '단답형', '18번'],
  'symbols': [{'sym': '$-1 \\le \\sin\\theta \\le 1$',
               'desc': '사인값은 항상 가장 작을 때 -1, 가장 클 때 1',
               'desc_en': 'The sine function always ranges between $-1$ and $1$.'},
              {'sym': '$\\sin\\left(\\dfrac{\\pi}{6}\\right) = \\dfrac{1}{2}$',
               'desc': '$30^\\circ\\left(\\dfrac{\\pi}{6}\\right)$의 사인값은 $\\dfrac{1}{2}$',
               'desc_en': 'Sine of $\\dfrac{\\pi}{6}$ ($30^\\circ$) is $\\dfrac{1}{2}$.'}],
  'levels': [{'title': '🔰 1단계 · [초등 덧셈·뺄셈] $-4 + a = 1$을 만족하는 수 $a$ 구하기',
              'title_en': '🔰 Step 1 · [Elementary Addition] Solving $-4 + a = 1$ for $a$',
              'knowledge': '사인($\\sin$) 값은 가장 작을 때 $-1$입니다. 여기에 $4$를 곱하면 $-4$가 되고, $a$를 더한 최솟값이 $1$이므로 초등학교 덧셈식 $-4 + '
                           'a = 1$이 성립합니다.',
              'knowledge_en': 'The minimum of $\\sin$ is $-1$. Multiplying by $4$ and adding $a$ gives $-4 + a = 1$, '
                              'which is a simple elementary addition equation.',
              'questions': [{'level_label': '초등 덧셈 디딤돌 1',
                             'level_label_en': 'Elementary Addition Step 1',
                             'stem': '초등학교 덧셈·뺄셈 원리로 $-4 + a = 1$을 만족시키는 상수 $a$의 값을 구하면?',
                             'stem_en': 'Using elementary arithmetic, what value of $a$ satisfies $-4 + a = 1$?',
                             'options': ['$3$', '$4$', '$5$', '$6$', '$7$'],
                             'answer': 3,
                             'exp': '$a = 1 + 4 = 5$입니다.',
                             'exp_en': '$a = 1 + 4 = 5$.'}]},
             {'title': '🌿 2단계 · [초등 분수 통분] $\\dfrac{\\pi}{2} - \\dfrac{\\pi}{3}$ 계산하기',
              'title_en': '🌿 Step 2 · [Elementary Fraction Subtraction] Computing $\\dfrac{\\pi}{2} - '
                          '\\dfrac{\\pi}{3}$',
              'knowledge': '$x = \\frac{\\pi}{2}$를 대입하면 괄호 안의 각은 $\\frac{\\pi}{2} - \\frac{\\pi}{3}$가 됩니다. 분모 $2$와 '
                           '$3$을 $6$으로 통분하면 $\\frac{3\\pi}{6} - \\frac{2\\pi}{6} = \\frac{\\pi}{6}$입니다.',
              'knowledge_en': 'With common denominator $6$, $\\frac{\\pi}{2} - \\frac{\\pi}{3} = \\frac{3\\pi - '
                              '2\\pi}{6} = \\frac{\\pi}{6}$.',
              'questions': [{'level_label': '분수 뺄셈 디딤돌 2',
                             'level_label_en': 'Fraction Subtraction Step 2',
                             'stem': '$\\frac{1}{2} - \\frac{1}{3}$을 통분하여 계산한 결과는?',
                             'stem_en': 'What is the result of $\\frac{1}{2} - \\frac{1}{3}$?',
                             'options': ['$\\frac{1}{12}$',
                                         '$\\frac{1}{6}$',
                                         '$\\frac{1}{5}$',
                                         '$\\frac{1}{3}$',
                                         '$\\frac{1}{2}$'],
                             'answer': 2,
                             'exp': '$\\frac{3}{6} - \\frac{2}{6} = \\frac{1}{6}$입니다.',
                             'exp_en': '$\\frac{3}{6} - \\frac{2}{6} = \\frac{1}{6}$.'}]},
             {'title': '🌱 3단계 · [특수각의 삼각비] $\\sin\\left(\\dfrac{\\pi}{6}\\right)$의 값 찾기',
              'title_en': '🌱 Step 3 · [Special Angle] Value of $\\sin\\left(\\dfrac{\\pi}{6}\\right)$',
              'knowledge': '라디안 각 $\\frac{\\pi}{6}$는 $180^\\circ \\div 6 = 30^\\circ$입니다. $\\sin 30^\\circ = '
                           '\\frac{1}{2}$입니다.',
              'knowledge_en': 'Since $\\frac{\\pi}{6} = 30^\\circ$, we have $\\sin\\left(\\frac{\\pi}{6}\\right) = '
                              '\\frac{1}{2}$.',
              'questions': [{'level_label': '특수각 사인값 디딤돌 3',
                             'level_label_en': 'Special Sine Value Step 3',
                             'stem': '$\\sin\\left(\\frac{\\pi}{6}\\right)$의 값은?',
                             'stem_en': 'What is the value of $\\sin\\left(\\frac{\\pi}{6}\\right)$?',
                             'options': ['$0$',
                                         '$\\frac{1}{2}$',
                                         '$\\frac{\\sqrt{2}}{2}$',
                                         '$\\frac{\\sqrt{3}}{2}$',
                                         '$1$'],
                             'answer': 2,
                             'exp': '$\\sin\\left(\\frac{\\pi}{6}\\right) = \\sin 30^\\circ = \\frac{1}{2}$입니다.',
                             'exp_en': '$\\sin\\left(\\frac{\\pi}{6}\\right) = \\frac{1}{2}$.'}]},
             {'title': '🌳 4단계 · [앞부분 곱셈] $4 \\times \\sin\\left(\\dfrac{\\pi}{6}\\right)$ 계산하기',
              'title_en': '🌳 Step 4 · [Multiplication] Computing $4 \\times \\sin\\left(\\dfrac{\\pi}{6}\\right)$',
              'knowledge': '$4 \\times \\frac{1}{2} = 2$입니다.',
              'knowledge_en': '$4 \\times \\frac{1}{2} = 2$.',
              'questions': [{'level_label': '분수 곱셈 디딤돌 4',
                             'level_label_en': 'Fraction Product Step 4',
                             'stem': '$4 \\sin\\left(\\frac{\\pi}{6}\\right) = 4 \\times \\frac{1}{2}$의 값은?',
                             'stem_en': 'What is $4 \\sin\\left(\\frac{\\pi}{6}\\right) = 4 \\times \\frac{1}{2}$?',
                             'options': ['$1$', '$2$', '$3$', '$4$', '$5$'],
                             'answer': 2,
                             'exp': '$4 \\times \\frac{1}{2} = 2$입니다.',
                             'exp_en': '$4 \\times \\frac{1}{2} = 2$.'}]},
             {'title': '💎 5단계 · [최종 종합] $f\\left(\\dfrac{\\pi}{2}\\right) = 2 + a$ 완성하기',
              'title_en': '💎 Step 5 · [Final Synthesis] Completing $f\\left(\\dfrac{\\pi}{2}\\right) = 2 + a$',
              'knowledge': '$4\\sin\\left(\\frac{\\pi}{6}\\right) = 2$와 1단계에서 구한 $a = 5$를 더합니다.',
              'knowledge_en': 'Add $2$ and $a = 5$ to find $f(\\pi/2)$.',
              'questions': [{'level_label': '최종 종합 디딤돌 5',
                             'level_label_en': 'Final Synthesis Step 5',
                             'stem': '$a = 5$일 때, $f\\left(\\frac{\\pi}{2}\\right) = 2 + 5$의 값은?',
                             'stem_en': 'With $a = 5$, what is $f\\left(\\frac{\\pi}{2}\\right) = 2 + 5$?',
                             'options': ['$5$', '$6$', '$7$', '$8$', '$9$'],
                             'answer': 3,
                             'exp': '$2 + 5 = 7$입니다.',
                             'exp_en': '$2 + 5 = 7$.'}]}],
  'final': {'stem': '함수 $f(x) = 4\\sin\\left(x - \\dfrac{\\pi}{3}\\right) + a$의 최솟값이 $1$일 때, '
                    '$f\\left(\\dfrac{\\pi}{2}\\right)$의 값을 구하시오. (단, $a$는 상수이다.) [3점]',
            'stem_en': 'When the minimum value of $f(x) = 4\\sin\\left(x - \\dfrac{\\pi}{3}\\right) + a$ is $1$ ($a$ '
                       'is a constant), find the value of $f\\left(\\dfrac{\\pi}{2}\\right)$. [3 points]',
            'options': ['$5$', '$6$', '$7$', '$8$', '$9$'],
            'answer': 3,
            'exp': '최솟값은 $-4 + a = 1$이므로 $a = 5$입니다. 따라서 $f\\left(\\dfrac{\\pi}{2}\\right) = '
                   '4\\sin\\left(\\dfrac{\\pi}{6}\\right) + 5 = 2 + 5 = 7$입니다.',
            'exp_en': 'The minimum value is $-4 + a = 1 \\implies a = 5$. Thus $f\\left(\\dfrac{\\pi}{2}\\right) = '
                      '4\\sin\\left(\\dfrac{\\pi}{6}\\right) + 5 = 2 + 5 = 7$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>삼각함수의 최대·최소 성질</b>과 특수각의 삼각비를 결합한 문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 최솟값 조건으로 상수 $a$ 구하기</b><br>\n'
                        '  모든 실수 $x$에 대하여 $-1 \\le \\sin\\left(x - \\frac{\\pi}{3}\\right) \\le 1$이므로 $f(x)$의 '
                        '최솟값은:<br>\n'
                        '  $$-4 + a = 1 \\implies a = 5$$<br>\n'
                        '  <b>2단계: $f\\left(\\frac{\\pi}{2}\\right)$ 계산하기</b><br>\n'
                        '  $$f\\left(\\frac{\\pi}{2}\\right) = 4\\sin\\left(\\frac{\\pi}{2} - \\frac{\\pi}{3}\\right) '
                        '+ 5 = 4\\sin\\left(\\frac{\\pi}{6}\\right) + 5 = 4 \\times \\frac{1}{2} + 5 = 7$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 구하는 값은 <b>$7$</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem uses the <b>minimum value of a sine function</b> to determine the vertical '
                           'shift $a$.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Find $a$</b><br>\n'
                           '  Since $\\min \\sin\\left(x - \\frac{\\pi}{3}\\right) = -1$, the minimum of $f(x)$ is $-4 '
                           '+ a = 1 \\implies a = 5$.<br><br>\n'
                           '  <b>Step 2: Evaluate $f(\\pi/2)$</b><br>\n'
                           '  $$f\\left(\\frac{\\pi}{2}\\right) = 4\\sin\\left(\\frac{\\pi}{6}\\right) + 5 = 2 + 5 = '
                           '7$$\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  The final answer is <b>$7$</b>.\n'
                           '</p>'}},
 {'slug': 'c261019',
  'qNum': '19',
  'subject': '공통(수학I·II)',
  'title': '[2026학년도 10월 고3 19번] 닫힌구간에서 삼차함수의 최댓값과 최솟값',
  'title_en': '[2026 AY Oct Exam Grade 12 #19] Maximum and Minimum of a Cubic Function on a Closed Interval',
  'summary_ko': '구간 $[0, 2]$에서 극점 $x=0, 1$과 끝점 $x=2$의 함숫값을 비교해 $a=-2$를 구하고 $f(-2)$ 도출하기',
  'summary_en': 'Compare values at critical points $x=0, 1$ and endpoint $x=2$ on $[0, 2]$ to find $a=-2$, then '
                'compute $f(-2)$.',
  'tags': ['공통(수학I·II)', '수학II', '미분', '최대와최소', '삼차함수', '단답형', '19번'],
  'symbols': [{'sym': "$f'(x) = 6ax(x - 1)$",
               'desc': '미분하여 기울기가 $0$이 되는 극점 $x=0, 1$ 찾기',
               'desc_en': 'Derivative factored to locate critical points at $x=0$ and $x=1$.'},
              {'sym': '$f(0)=6,\\ f(1)=6-a,\\ f(2)=4a+6$',
               'desc': '닫힌구간 [0, 2]의 양 끝점과 극점에서의 후보 함숫값',
               'desc_en': 'Candidate values at critical points and endpoints on [0, 2].'}],
  'levels': [{'title': '🔰 1단계 · [초등 대소 비교] $f(0) = 6$과 최댓값 $8$, 최솟값 $-2$ 비교하기',
              'title_en': '🔰 Step 1 · [Elementary Comparison] Comparing $f(0) = 6$ with max $8$ and min $-2$',
              'knowledge': '$f(x) = 2ax^3 - 3ax^2 + 6$에 $x = 0$을 넣으면 $a$의 값에 상관없이 $f(0) = 6$입니다. 초등학교 숫자 크기 비교에서 $6$은 '
                           '최솟값 $-2$와 최댓값 $8$ 사이의 수이므로, 나머지 두 후보값 $f(1) = 6 - a$와 $f(2) = 4a + 6$이 각각 $8$과 $-2$가 되어야 '
                           '합니다!',
              'knowledge_en': 'By elementary number comparison, $f(0) = 6$ lies strictly between the minimum $-2$ and '
                              'maximum $8$. Thus the other two candidates $f(1) = 6 - a$ and $f(2) = 4a + 6$ must be '
                              '$8$ and $-2$.',
              'questions': [{'level_label': '초등 숫자 비교 디딤돌 1',
                             'level_label_en': 'Elementary Comparison Step 1',
                             'stem': '초등학교 미지수 찾기처럼 $6 - a = 8$이고 동시에 $4a + 6 = -2$를 만족시키는 정수 $a$의 값은?',
                             'stem_en': 'Using elementary arithmetic, which integer $a$ satisfies both $6 - a = 8$ and '
                                        '$4a + 6 = -2$?',
                             'options': ['$-3$', '$-2$', '$-1$', '$1$', '$2$'],
                             'answer': 2,
                             'exp': '$a = -2$를 넣으면 $6 - (-2) = 8$ (최댓값), $4(-2) + 6 = -2$ (최솟값)가 동시에 성립합니다!',
                             'exp_en': 'Substituting $a = -2$ gives $6 - (-2) = 8$ and $4(-2) + 6 = -2$ '
                                       'simultaneously.'}]},
             {'title': '🌿 2단계 · [함수식 완성] $a = -2$를 대입하여 $f(x)$ 적기',
              'title_en': '🌿 Step 2 · [Completing $f(x)$] Writing $f(x)$ with $a = -2$',
              'knowledge': '$f(x) = 2ax^3 - 3ax^2 + 6$에 $a = -2$를 대입하면 $f(x) = -4x^3 + 6x^2 + 6$이 됩니다.',
              'knowledge_en': 'Substituting $a = -2$ into $f(x) = 2ax^3 - 3ax^2 + 6$ gives $f(x) = -4x^3 + 6x^2 + 6$.',
              'questions': [{'level_label': '계수 확인 디딤돌 2',
                             'level_label_en': 'Coefficient Check Step 2',
                             'stem': '$a = -2$일 때 $f(x) = 2ax^3 - 3ax^2 + 6$의 $x^3$의 계수 $2a$와 $x^2$의 계수 $-3a$를 순서대로 '
                                     '바르게 짝지은 것은?',
                             'stem_en': 'When $a = -2$, what are the coefficients $2a$ and $-3a$ of $x^3$ and $x^2$?',
                             'options': ['$-4,\\ -6$', '$-4,\\ 6$', '$4,\\ -6$', '$4,\\ 6$', '$-2,\\ 6$'],
                             'answer': 2,
                             'exp': '$2a = 2(-2) = -4$이고 $-3a = -3(-2) = 6$입니다.',
                             'exp_en': '$2a = -4$ and $-3a = 6$.'}]},
             {'title': '🌱 3단계 · [음수의 세제곱] $x = -2$일 때 $-4x^3$ 계산하기',
              'title_en': '🌱 Step 3 · [Cube of Negative Number] Computing $-4x^3$ at $x = -2$',
              'knowledge': '$(-2)^3 = -8$이므로 $-4 \\times (-8) = +32$입니다.',
              'knowledge_en': 'Since $(-2)^3 = -8$, we have $-4(-8) = 32$.',
              'questions': [{'level_label': '세제곱 항 계산 디딤돌 3',
                             'level_label_en': 'Cubic Term Step 3',
                             'stem': '$x = -2$일 때 $-4x^3 = -4 \\times (-8)$의 값은?',
                             'stem_en': 'At $x = -2$, what is $-4x^3 = -4 \\times (-8)$?',
                             'options': ['$-32$', '$-16$', '$16$', '$24$', '$32$'],
                             'answer': 5,
                             'exp': '음수끼리의 곱셈이므로 $-4 \\times (-8) = 32$입니다.',
                             'exp_en': '$-4 \\times (-8) = 32$.'}]},
             {'title': '🌳 4단계 · [음수의 제곱] $x = -2$일 때 $6x^2$ 계산하기',
              'title_en': '🌳 Step 4 · [Square of Negative Number] Computing $6x^2$ at $x = -2$',
              'knowledge': '$(-2)^2 = 4$이므로 $6 \\times 4 = 24$입니다.',
              'knowledge_en': 'Since $(-2)^2 = 4$, we have $6 \\times 4 = 24$.',
              'questions': [{'level_label': '제곱 항 계산 디딤돌 4',
                             'level_label_en': 'Quadratic Term Step 4',
                             'stem': '$x = -2$일 때 $6x^2 = 6 \\times 4$의 값은?',
                             'stem_en': 'At $x = -2$, what is $6x^2 = 6 \\times 4$?',
                             'options': ['$-24$', '$-12$', '$12$', '$24$', '$36$'],
                             'answer': 4,
                             'exp': '$6 \\times 4 = 24$입니다.',
                             'exp_en': '$6 \\times 4 = 24$.'}]},
             {'title': '💎 5단계 · [최종 종합] $f(-2) = 32 + 24 + 6$ 계산하기',
              'title_en': '💎 Step 5 · [Final Synthesis] Computing $f(-2) = 32 + 24 + 6$',
              'knowledge': '구한 세 항 $32, 24, 6$을 모두 더하면 $f(-2)$의 값이 완성됩니다.',
              'knowledge_en': 'Sum the three terms $32 + 24 + 6$ to find $f(-2)$.',
              'questions': [{'level_label': '최종 종합 디딤돌 5',
                             'level_label_en': 'Final Synthesis Step 5',
                             'stem': '$f(-2) = 32 + 24 + 6$의 값은?',
                             'stem_en': 'What is the value of $f(-2) = 32 + 24 + 6$?',
                             'options': ['$56$', '$58$', '$60$', '$62$', '$64$'],
                             'answer': 4,
                             'exp': '$32 + 24 + 6 = 62$입니다.',
                             'exp_en': '$32 + 24 + 6 = 62$.'}]}],
  'final': {'stem': '닫힌구간 $[0, 2]$에서 함수 $f(x) = 2ax^3 - 3ax^2 + 6$의 최댓값은 $8$이고 최솟값은 $-2$이다. $f(-2)$의 값을 구하시오. (단, $a$는 '
                    '$0$이 아닌 상수이다.) [3점]',
            'stem_en': 'On the closed interval $[0, 2]$, the function $f(x) = 2ax^3 - 3ax^2 + 6$ has a maximum value '
                       'of $8$ and a minimum value of $-2$ ($a \\neq 0$). Find the value of $f(-2)$. [3 points]',
            'options': ['$56$', '$58$', '$60$', '$62$', '$64$'],
            'answer': 4,
            'exp': "$f'(x) = 6ax(x-1)$에서 $f(0)=6$, $f(1)=6-a$, $f(2)=4a+6$입니다. 최댓값 $8$, 최솟값 $-2$를 만족하려면 $a = -2$이므로 "
                   '$f(x) = -4x^3 + 6x^2 + 6$이고 $f(-2) = 32 + 24 + 6 = 62$입니다.',
            'exp_en': 'Checking $f(0)=6$, $f(1)=6-a$, and $f(2)=4a+6$ against max $8$ and min $-2$ gives $a = -2$. '
                      'Thus $f(x) = -4x^3 + 6x^2 + 6$ and $f(-2) = 62$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>닫힌구간에서 삼차함수의 최댓값과 최솟값</b>을 이용해 미정계수 $a$의 부호와 값을 결정하는 문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 도함수와 구간 $[0, 2]$에서의 함숫값 후보 구하기</b><br>\n'
                        "  $$f'(x) = 6ax^2 - 6ax = 6ax(x - 1)$$\n"
                        '  구간 $[0, 2]$에서 극점과 양 끝점의 함숫값은 다음과 같습니다:<br>\n'
                        '  $$f(0) = 6, \\quad f(1) = 6 - a, \\quad f(2) = 4a + 6$$<br>\n'
                        '  <b>2단계: 최댓값 $8$, 최솟값 $-2$와 비교하여 $a$ 구하기</b><br>\n'
                        '  $f(0) = 6$은 $-2$와 $8$ 사이의 값이므로, $6 - a$와 $4a + 6$이 각각 $8$과 $-2$가 되어야 합니다.<br>\n'
                        '  $a < 0$일 때 $6 - a > 6 > 4a + 6$이므로:<br>\n'
                        '  $$6 - a = 8 \\implies a = -2, \\quad 4(-2) + 6 = -2 \\quad (\\text{성립})$$<br>\n'
                        '  <b>3단계: $f(-2)$의 값 계산</b><br>\n'
                        '  $f(x) = -4x^3 + 6x^2 + 6$이므로:<br>\n'
                        '  $$f(-2) = -4(-8) + 6(4) + 6 = 32 + 24 + 6 = 62$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 구하는 값은 <b>$62$</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem determines the parameter $a$ from the <b>extrema of a cubic function on '
                           '$[0, 2]$</b>.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Candidate values on $[0, 2]$</b><br>\n'
                           "  Since $f'(x) = 6ax(x-1)$, the candidates are $f(0) = 6$, $f(1) = 6 - a$, and $f(2) = 4a "
                           '+ 6$.<br><br>\n'
                           '  <b>Step 2: Determine $a$</b><br>\n'
                           '  For the maximum to be $8$ and minimum to be $-2$, we need $6 - a = 8$ and $4a + 6 = -2$, '
                           'which both yield $a = -2$.<br><br>\n'
                           '  <b>Step 3: Evaluate $f(-2)$</b><br>\n'
                           '  $$f(-2) = -4(-2)^3 + 6(-2)^2 + 6 = 32 + 24 + 6 = 62$$\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  The final answer is <b>$62$</b>.\n'
                           '</p>'}},
 {'slug': 'c261020',
  'qNum': '20',
  'subject': '공통(수학I·II)',
  'title': '[2026학년도 10월 고3 20번] 역함수 관계인 지수·로그함수와 직각삼각형의 닮음',
  'title_en': '[2026 AY Oct Exam Grade 12 #20] Inverse Exponential-Logarithmic Functions and Similar Right Triangles',
  'summary_ko': '평행한 두 직선 사이의 동위각·동측내각 관계로 $\\angle\\mathrm{BAD}=90^\\circ$를 밝히고 닮음비로 점 $\\mathrm{A}\\!\\left(-1, '
                '\\dfrac{1}{3}\\right)$을 찾아 $a^2=27$ 구하기',
  'summary_en': 'Prove $\\angle\\mathrm{BAD}=90^\\circ$ using parallel lines and similar triangles, find '
                '$\\mathrm{A}\\!\\left(-1, \\dfrac{1}{3}\\right)$, and deduce $a^2=27$.',
  'tags': ['공통(수학I·II)', '수학I', '지수함수와로그함수', '역함수', '삼각형의닮음', '단답형', '20번'],
  'symbols': [{'sym': '$f^{-1}(x) = g(x)$',
               'desc': '$y=\\sqrt{3}a^x$와 $y=\\log_a\\!\\left(\\dfrac{x}{\\sqrt{3}}\\right)$는 직선 $y=x$에 대칭인 역함수',
               'desc_en': '$f(x)$ and $g(x)$ are inverse functions symmetric across $y=x$.'},
              {'sym': '$\\triangle CBA \\sim \\triangle BAD$',
               'desc': '평행선 사이의 두 삼각형이 닮음이므로 끼인각이 모두 90도',
               'desc_en': 'Similarity between parallel lines forces angles CBA and BAD to be 90 degrees.'},
              {'sym': '$\\overline{BA} = \\dfrac{2\\sqrt{2}}{3}$',
               'desc': '기울기가 $-1$인 두 평행선 $y=-x-\\dfrac{2}{3}$과 $y=-x+\\dfrac{2}{3}$ 사이의 수직 거리',
               'desc_en': 'Perpendicular distance between the two parallel lines of slope $-1$.'}],
  'levels': [{'title': '🔰 1단계 · [초등 각도 합] 평행선 사이의 두 각이 같을 때 한 각의 크기 구하기',
              'title_en': '🔰 Step 1 · [Elementary Angle Sum] Finding equal supplementary angles between parallel lines',
              'knowledge': '초등학교 도형에서 평행한 두 직선 안쪽의 두 각(동측내각)을 더하면 $180^\\circ$입니다. 삼각형 $\\mathrm{CBA}$와 삼각형 '
                           '$\\mathrm{BAD}$가 닮음이어서 $\\angle\\mathrm{CBA} = \\angle\\mathrm{BAD}$이고 두 각의 합이 '
                           '$180^\\circ$라면, 각 하나는 $180^\\circ \\div 2 = 90^\\circ$(직각)입니다!',
              'knowledge_en': 'In elementary geometry, interior angles on the same side of a transversal between '
                              'parallel lines sum to $180^\\circ$. Since $\\triangle\\mathrm{CBA} \\sim '
                              '\\triangle\\mathrm{BAD}$ gives $\\angle\\mathrm{CBA} = \\angle\\mathrm{BAD}$, each '
                              'angle is $180^\\circ \\div 2 = 90^\\circ$.',
              'questions': [{'level_label': '초등 각도 나눗셈 디딤돌 1',
                             'level_label_en': 'Elementary Angle Division Step 1',
                             'stem': '초등학교 각도 계산처럼 크기가 같은 두 각 $\\angle\\mathrm{CBA}$와 $\\angle\\mathrm{BAD}$의 합이 '
                                     '$180^\\circ$일 때, $\\angle\\mathrm{BAD}$의 크기는?',
                             'stem_en': 'By elementary angle division, if two equal angles $\\angle\\mathrm{CBA}$ and '
                                        '$\\angle\\mathrm{BAD}$ sum to $180^\\circ$, what is $\\angle\\mathrm{BAD}$?',
                             'options': ['$45^\\circ$', '$60^\\circ$', '$90^\\circ$', '$120^\\circ$', '$135^\\circ$'],
                             'answer': 3,
                             'exp': '$180^\\circ \\div 2 = 90^\\circ$이므로 직선 $\\mathrm{AB}$는 두 평행선 $L_1, L_2$에 수직(기울기 '
                                    '$1$)입니다!',
                             'exp_en': '$180^\\circ \\div 2 = 90^\\circ$, meaning segment $\\mathrm{AB}$ is '
                                       'perpendicular to both parallel lines.'}]},
             {'title': '🌿 2단계 · [평행선 거리와 닮음비] $\\overline{\\mathrm{BA}}$와 $\\overline{\\mathrm{AD}}$의 길이 구하기',
              'title_en': '🌿 Step 2 · [Parallel Distance & Similarity] Finding lengths $\\overline{\\mathrm{BA}}$ and '
                          '$\\overline{\\mathrm{AD}}$',
              'knowledge': '두 평행선 $y = -x - \\frac{2}{3}$와 $y = -x + \\frac{2}{3}$ 사이의 수직 거리는 '
                           '$\\overline{\\mathrm{BA}} = \\frac{4/3}{\\sqrt{2}} = \\frac{2\\sqrt{2}}{3}$입니다. 또 넓이의 비가 '
                           '$4 : 1$이므로 닮음비는 $2 : 1$이어서 $\\overline{\\mathrm{BA}} : \\overline{\\mathrm{AD}} = 2 : '
                           '1$입니다.',
              'knowledge_en': 'The perpendicular distance between the two lines is $\\overline{\\mathrm{BA}} = '
                              '\\frac{2\\sqrt{2}}{3}$. Since the area ratio is $4:1$, the similarity ratio is $2:1$, '
                              'so $\\overline{\\mathrm{AD}} = \\frac{1}{2}\\overline{\\mathrm{BA}}$.',
              'questions': [{'level_label': '닮음비 길이 디딤돌 2',
                             'level_label_en': 'Similarity Length Step 2',
                             'stem': '$\\overline{\\mathrm{BA}} = \\frac{2\\sqrt{2}}{3}$이고 $\\overline{\\mathrm{AD}} = '
                                     '\\frac{1}{2}\\overline{\\mathrm{BA}}$일 때, 선분 $\\overline{\\mathrm{AD}}$의 길이는?',
                             'stem_en': 'Given $\\overline{\\mathrm{BA}} = \\frac{2\\sqrt{2}}{3}$ and '
                                        '$\\overline{\\mathrm{AD}} = \\frac{1}{2}\\overline{\\mathrm{BA}}$, what is '
                                        '$\\overline{\\mathrm{AD}}$?',
                             'options': ['$\\frac{\\sqrt{2}}{6}$',
                                         '$\\frac{\\sqrt{2}}{3}$',
                                         '$\\frac{2\\sqrt{2}}{3}$',
                                         '$\\sqrt{2}$',
                                         '$\\frac{4\\sqrt{2}}{3}$'],
                             'answer': 2,
                             'exp': '$\\overline{\\mathrm{AD}} = \\frac{1}{2} \\times \\frac{2\\sqrt{2}}{3} = '
                                    '\\frac{\\sqrt{2}}{3}$입니다.',
                             'exp_en': '$\\overline{\\mathrm{AD}} = \\frac{\\sqrt{2}}{3}$.'}]},
             {'title': '🌱 3단계 · [점 $\\mathrm{A}$의 좌표 찾기] $\\mathrm{D}\\left(-\\dfrac{2}{3}, 0\\right)$에서 왼쪽 위로 이동하기',
              'title_en': '🌱 Step 3 · [Coordinates of $\\mathrm{A}$] Moving from $\\mathrm{D}\\left(-\\dfrac{2}{3}, '
                          '0\\right)$ along slope $-1$',
              'knowledge': '직선 $y = -x - \\frac{2}{3}$의 $x$절편은 $\\mathrm{D}\\left(-\\frac{2}{3}, 0\\right)$입니다. 기울기가 '
                           '$-1$인 직선 위에서 거리가 $\\frac{\\sqrt{2}}{3}$만큼 왼쪽 위로 가면 $x$좌표는 $\\frac{1}{3}$만큼 작아지고 $y$좌표는 '
                           '$\\frac{1}{3}$만큼 커집니다.',
              'knowledge_en': 'Moving distance $\\frac{\\sqrt{2}}{3}$ up-left along a line of slope $-1$ from '
                              '$\\mathrm{D}\\left(-\\frac{2}{3}, 0\\right)$ changes coordinates by '
                              '$\\left(-\\frac{1}{3}, +\\frac{1}{3}\\right)$.',
              'questions': [{'level_label': '점 A 좌표 디딤돌 3',
                             'level_label_en': 'Point A Coordinates Step 3',
                             'stem': '점 $\\mathrm{D}\\left(-\\frac{2}{3}, 0\\right)$에서 $x$좌표에 $-\\frac{1}{3}$, $y$좌표에 '
                                     '$+\\frac{1}{3}$을 더한 점 $\\mathrm{A}$의 좌표는?',
                             'stem_en': 'Adding $\\left(-\\frac{1}{3}, \\frac{1}{3}\\right)$ to '
                                        '$\\mathrm{D}\\left(-\\frac{2}{3}, 0\\right)$ gives which coordinates for '
                                        '$\\mathrm{A}$?',
                             'options': ['$\\left(-1, \\frac{1}{3}\\right)$',
                                         '$\\left(-\\frac{1}{3}, 1\\right)$',
                                         '$\\left(-1, 1\\right)$',
                                         '$\\left(-\\frac{4}{3}, \\frac{2}{3}\\right)$',
                                         '$\\left(-\\frac{1}{3}, \\frac{1}{3}\\right)$'],
                             'answer': 1,
                             'exp': '$-\\frac{2}{3} - \\frac{1}{3} = -1$, $0 + \\frac{1}{3} = \\frac{1}{3}$이므로 '
                                    '$\\mathrm{A}\\left(-1, \\frac{1}{3}\\right)$입니다.',
                             'exp_en': '$\\mathrm{A} = \\left(-\\frac{2}{3} - \\frac{1}{3}, 0 + \\frac{1}{3}\\right) = '
                                       '\\left(-1, \\frac{1}{3}\\right)$.'}]},
             {'title': '🌳 4단계 · [함수 대입] $\\mathrm{A}\\left(-1, \\dfrac{1}{3}\\right)$을 $f(x) = \\sqrt{3}a^x$에 대입하기',
              'title_en': '🌳 Step 4 · [Function Substitution] Substituting $\\mathrm{A}\\left(-1, '
                          '\\dfrac{1}{3}\\right)$ into $f(x) = \\sqrt{3}a^x$',
              'knowledge': '점 $\\mathrm{A}\\left(-1, \\frac{1}{3}\\right)$은 곡선 $y = \\sqrt{3}a^x$ 위의 점이므로 $f(-1) = '
                           '\\frac{\\sqrt{3}}{a} = \\frac{1}{3}$이 성립합니다.',
              'knowledge_en': 'Since $\\mathrm{A}\\left(-1, \\frac{1}{3}\\right)$ lies on $y = \\sqrt{3}a^x$, we have '
                              '$\\frac{\\sqrt{3}}{a} = \\frac{1}{3}$.',
              'questions': [{'level_label': '밑 a 구하기 디딤돌 4',
                             'level_label_en': 'Base a Step 4',
                             'stem': '$\\frac{\\sqrt{3}}{a} = \\frac{1}{3}$에서 양수 $a$의 값은?',
                             'stem_en': 'From $\\frac{\\sqrt{3}}{a} = \\frac{1}{3}$, what is the value of $a$?',
                             'options': ['$\\sqrt{3}$', '$2\\sqrt{3}$', '$3$', '$3\\sqrt{3}$', '$9$'],
                             'answer': 4,
                             'exp': '양변에 $3a$를 곱하면 $a = 3\\sqrt{3}$입니다.',
                             'exp_en': 'Cross-multiplying gives $a = 3\\sqrt{3}$.'}]},
             {'title': '💎 5단계 · [최종 종합] $a^2$의 값 계산하기',
              'title_en': '💎 Step 5 · [Final Synthesis] Computing $a^2$',
              'knowledge': '$a = 3\\sqrt{3}$을 제곱하여 $a^2$의 값을 구합니다.',
              'knowledge_en': 'Square $a = 3\\sqrt{3}$ to obtain $a^2$.',
              'questions': [{'level_label': '최종 종합 디딤돌 5',
                             'level_label_en': 'Final Synthesis Step 5',
                             'stem': '$a = 3\\sqrt{3}$일 때, $a^2 = (3\\sqrt{3})^2$의 값은?',
                             'stem_en': 'Given $a = 3\\sqrt{3}$, what is the value of $a^2$?',
                             'options': ['$9$', '$18$', '$27$', '$36$', '$81$'],
                             'answer': 3,
                             'exp': '$(3\\sqrt{3})^2 = 9 \\times 3 = 27$입니다.',
                             'exp_en': '$(3\\sqrt{3})^2 = 9 \\times 3 = 27$.'}]}],
  'final': {'stem': '$1$보다 큰 상수 $a$에 대하여 두 함수 $f(x) = \\sqrt{3}a^x$, $g(x) = \\log_a \\dfrac{x}{\\sqrt{3}}$의 그래프가 직선 '
                    '$y = -x - \\dfrac{2}{3}$와 만나는 점을 각각 $\\mathrm{A}$, $\\mathrm{E}$라 하고, 직선 $y = -x + '
                    '\\dfrac{2}{3}$와 만나는 점을 각각 $\\mathrm{B}$, $\\mathrm{C}$라 하자. 직선 $y = -x - \\dfrac{2}{3}$가 $x$축과 '
                    '만나는 점을 $\\mathrm{D}$라 할 때, 삼각형 $\\mathrm{CBA}$는 삼각형 $\\mathrm{BAD}$와 닮음이고 넓이가 삼각형 '
                    '$\\mathrm{BAD}$의 넓이의 $4$배이다. $a^2$의 값을 구하시오. (단, $\\angle\\mathrm{CBA} = \\angle\\mathrm{BAD}$, '
                    '$\\angle\\mathrm{BAC} = \\angle\\mathrm{ADB}$이다.) [4점]',
            'stem_en': 'For $a > 1$, the graphs of $f(x) = \\sqrt{3}a^x$ and $g(x) = \\log_a \\dfrac{x}{\\sqrt{3}}$ '
                       'meet $y = -x - \\dfrac{2}{3}$ at $\\mathrm{A}$ and $\\mathrm{E}$, and meet $y = -x + '
                       '\\dfrac{2}{3}$ at $\\mathrm{B}$ and $\\mathrm{C}$. Let $\\mathrm{D}$ be the $x$-intercept of '
                       '$y = -x - \\dfrac{2}{3}$. Given $\\triangle\\mathrm{CBA} \\sim \\triangle\\mathrm{BAD}$ with '
                       '$\\angle\\mathrm{CBA} = \\angle\\mathrm{BAD}$, $\\angle\\mathrm{BAC} = \\angle\\mathrm{ADB}$, '
                       'and $\\text{Area}(\\triangle\\mathrm{CBA}) = 4\\text{Area}(\\triangle\\mathrm{BAD})$, find '
                       '$a^2$. [4 points]',
            'options': ['$9$', '$18$', '$27$', '$36$', '$81$'],
            'answer': 3,
            'exp': '평행선과 닮음 조건에서 $\\angle\\mathrm{CBA} = \\angle\\mathrm{BAD} = 90^\\circ$이고 $\\overline{\\mathrm{BA}} '
                   '= \\dfrac{2\\sqrt{2}}{3}$, $\\overline{\\mathrm{AD}} = \\dfrac{\\sqrt{2}}{3}$이므로 '
                   '$\\mathrm{A}\\left(-1, \\dfrac{1}{3}\\right)$입니다. $f(-1) = \\dfrac{\\sqrt{3}}{a} = '
                   '\\dfrac{1}{3}$에서 $a = 3\\sqrt{3}$이므로 $a^2 = 27$입니다.',
            'exp_en': 'Parallel lines and similarity give $\\angle\\mathrm{CBA} = \\angle\\mathrm{BAD} = 90^\\circ$, '
                      '$\\overline{\\mathrm{BA}} = \\dfrac{2\\sqrt{2}}{3}$, and $\\overline{\\mathrm{AD}} = '
                      '\\dfrac{\\sqrt{2}}{3}$, so $\\mathrm{A}\\left(-1, \\dfrac{1}{3}\\right)$. From $f(-1) = '
                      '\\dfrac{\\sqrt{3}}{a} = \\dfrac{1}{3}$, we get $a = 3\\sqrt{3}$ and $a^2 = 27$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>역함수 관계($y = x$ 대칭)인 지수·로그함수</b>와 기울기가 $-1$인 두 평행선 위에서 만들어지는 <b>닮음 직각삼각형의 기하학적 '
                        '성질</b>을 결합한 문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 평행선의 동측내각과 닮음으로 직각($90^\\circ$) 밝히기</b><br>\n'
                        '  두 직선 $L_1: y = -x - \\frac{2}{3}$와 $L_2: y = -x + \\frac{2}{3}$는 서로 평행하며, 반직선 '
                        '$\\mathrm{AD}$와 반직선 $\\mathrm{BC}$는 모두 오른쪽 아래를 향합니다.<br>\n'
                        '  따라서 동측내각의 합은 $\\angle\\mathrm{CBA} + \\angle\\mathrm{BAD} = 180^\\circ$인데, 문제 조건에서 '
                        '$\\angle\\mathrm{CBA} = \\angle\\mathrm{BAD}$이므로:<br>\n'
                        '  $$\\angle\\mathrm{CBA} = \\angle\\mathrm{BAD} = 90^\\circ$$\n'
                        '  즉, 직선 $\\mathrm{AB}$는 두 평행선에 수직인 기울기 $1$인 직선입니다.<br><br>\n'
                        '  <b>2단계: 닮음비 $2 : 1$을 이용하여 점 $\\mathrm{A}$의 좌표 구하기</b><br>\n'
                        '  두 평행선 $L_1, L_2$ 사이의 거리는 $\\overline{\\mathrm{BA}} = \\frac{4/3}{\\sqrt{2}} = '
                        '\\frac{2\\sqrt{2}}{3}$입니다.<br>\n'
                        '  $\\triangle\\mathrm{CBA}$의 넓이가 $\\triangle\\mathrm{BAD}$의 넓이의 $4$배이므로 닮음비는 $2 : 1$이고:<br>\n'
                        '  $$\\overline{\\mathrm{BA}} : \\overline{\\mathrm{AD}} = 2 : 1 \\implies '
                        '\\overline{\\mathrm{AD}} = \\frac{1}{2}\\overline{\\mathrm{BA}} = \\frac{\\sqrt{2}}{3}$$\n'
                        '  점 $\\mathrm{D}\\left(-\\frac{2}{3}, 0\\right)$에서 직선 $L_1$을 따라 왼쪽 위로 '
                        '$\\frac{\\sqrt{2}}{3}$만큼 이동한 점 $\\mathrm{A}$의 좌표는:<br>\n'
                        '  $$\\mathrm{A}\\left(-\\frac{2}{3} - \\frac{1}{3}, 0 + \\frac{1}{3}\\right) = \\left(-1, '
                        '\\frac{1}{3}\\right)$$\n'
                        '  (참고: 이때 $\\mathrm{B}\\left(-\\frac{1}{3}, 1\\right)$, $\\mathrm{C}\\left(1, '
                        '-\\frac{1}{3}\\right)$가 되어 $\\overline{\\mathrm{CB}} = \\frac{4\\sqrt{2}}{3}$ 및 $g(1) = '
                        '-\\frac{1}{3}$도 완벽히 일치합니다.)<br><br>\n'
                        '  <b>3단계: 지수함수에 대입하여 $a^2$ 구하기</b><br>\n'
                        '  점 $\\mathrm{A}\\left(-1, \\frac{1}{3}\\right)$을 $f(x) = \\sqrt{3}a^x$에 대입하면:<br>\n'
                        '  $$\\sqrt{3}a^{-1} = \\frac{1}{3} \\implies a = 3\\sqrt{3} \\implies a^2 = 27$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 구하는 값은 <b>$27$</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem utilizes <b>inverse symmetry across $y=x$</b> and <b>similar right '
                           'triangles between parallel lines of slope $-1$</b>.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Right angle deduction</b><br>\n'
                           '  Since rays $\\mathrm{BC}$ and $\\mathrm{AD}$ point in the same direction along parallel '
                           'lines, $\\angle\\mathrm{CBA} + \\angle\\mathrm{BAD} = 180^\\circ$. Combined with '
                           '$\\angle\\mathrm{CBA} = \\angle\\mathrm{BAD}$, both angles are $90^\\circ$.<br><br>\n'
                           '  <b>Step 2: Lengths and coordinates of $\\mathrm{A}$</b><br>\n'
                           '  The distance between the parallel lines is $\\overline{\\mathrm{BA}} = '
                           '\\frac{2\\sqrt{2}}{3}$. With similarity ratio $2:1$, $\\overline{\\mathrm{AD}} = '
                           '\\frac{\\sqrt{2}}{3}$. Moving up-left from $\\mathrm{D}\\left(-\\frac{2}{3}, 0\\right)$ '
                           'gives $\\mathrm{A}\\left(-1, \\frac{1}{3}\\right)$.<br><br>\n'
                           '  <b>Step 3: Solve for $a^2$</b><br>\n'
                           '  $$f(-1) = \\frac{\\sqrt{3}}{a} = \\frac{1}{3} \\implies a = 3\\sqrt{3} \\implies a^2 = '
                           '27$$\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  The final answer is <b>$27$</b>.\n'
                           '</p>'}},
 {'slug': 'c261021',
  'qNum': '21',
  'subject': '공통(수학I·II)',
  'title': '[2026학년도 10월 고3 21번] 도함수의 절댓값 정적분과 삼차함수의 극값 차 공식',
  'title_en': '[2026 AY Oct Exam Grade 12 #21] Definite Integral of Absolute Derivative and Cubic Extrema Difference',
  'summary_ko': "구간 $[0, t]$에서 $|f'(x)|$의 정적분을 부호별로 쪼개어 $f(\\alpha)-f(0)=f(2)=\\dfrac{5}{2}$를 도출하고 "
                '$f(0)=\\dfrac{1}{2}$ 구하기',
  'summary_en': "Split the integral of $|f'(x)|$ on $[0, t]$ by sign to derive $f(\\alpha)-f(0)=f(2)=\\dfrac{5}{2}$ "
                'and find $f(0)=\\dfrac{1}{2}$.',
  'tags': ['공통(수학I·II)', '수학II', '적분', '정적분과미분', '절댓값적분', '삼차함수', '단답형', '21번'],
  'symbols': [{'sym': "$\\int_a^b |f'(x)|dx$",
               'desc': '구간 $[a, b]$에서 함수 $f(x)$가 위아래로 움직인 총 변화량',
               'desc_en': 'Total vertical distance traveled by $f(x)$ over $[a, b]$.'},
              {'sym': "$f'(x) = 3(x-\\alpha)(x-2)$",
               'desc': '극대점 $x=\\alpha$ ($0 < \\alpha < 2$)와 극소점 $x=2$를 갖는 도함수',
               'desc_en': 'Derivative with local max at $x=\\alpha$ and local min at $x=2$.'},
              {'sym': '$f(\\alpha) - f(2) = \\dfrac{1}{2}(2-\\alpha)^3$',
               'desc': '최고차항 계수가 $1$인 삼차함수의 극댓값과 극솟값의 차 공식',
               'desc_en': 'Difference between local max and min of a monic cubic function.'}],
  'levels': [{'title': '🔰 1단계 · [초등 엘리베이터 이동거리] 올라간 거리와 내려간 거리 각각 구하기',
              'title_en': '🔰 Step 1 · [Elementary Elevator Distance] Upward and downward travel segments',
              'knowledge': "정적분 $\\int_0^t |f'(x)|dx$는 엘리베이터가 $x = 0$부터 $x = t$까지 <b>위아래로 움직인 총 이동 거리</b>입니다! $0 < "
                           '\\alpha < 2 < t$일 때 세 구간으로 나누어 봅시다.<ul><li>$[0, \\alpha]$ (증가): $f(0)$층에서 $f(\\alpha)$층으로 '
                           '올라간 거리 $= f(\\alpha) - f(0)$</li><li>$[\\alpha, 2]$ (감소): $f(\\alpha)$층에서 $f(2)$층으로 내려간 거리 '
                           '$= f(\\alpha) - f(2)$</li><li>$[2, t]$ (증가): $f(2)$층에서 $f(t)$층으로 올라간 거리 $= f(t) - '
                           'f(2)$</li></ul>',
              'knowledge_en': "The integral $\\int_0^t |f'(x)|dx$ measures total vertical travel: going up $f(\\alpha) "
                              '- f(0)$ on $[0, \\alpha]$, going down $f(\\alpha) - f(2)$ on $[\\alpha, 2]$, and going '
                              'up $f(t) - f(2)$ on $[2, t]$.',
              'questions': [{'level_label': '초등 구간별 이동거리 디딤돌 1',
                             'level_label_en': 'Segment Distance Step 1',
                             'stem': '세 구간의 이동 거리 $(f(\\alpha) - f(0)) + (f(\\alpha) - f(2)) + (f(t) - f(2))$를 모두 더하여 '
                                     '간단히 정리한 식은?',
                             'stem_en': 'What is the sum $(f(\\alpha) - f(0)) + (f(\\alpha) - f(2)) + (f(t) - f(2))$ '
                                        'simplified?',
                             'options': ['$f(\\alpha) - f(2) + f(t) - f(0)$',
                                         '$2f(\\alpha) - 2f(2) - f(0) + f(t)$',
                                         '$2f(\\alpha) - f(2) + f(t)$',
                                         '$f(t) - f(0)$',
                                         '$2f(\\alpha) + 2f(2) - f(t)$'],
                             'answer': 2,
                             'exp': '$f(\\alpha)$가 $2$번 더해지고 $f(2)$가 $2$번 빼지므로 $2f(\\alpha) - 2f(2) - f(0) + f(t)$입니다.',
                             'exp_en': '$2f(\\alpha) - 2f(2) - f(0) + f(t)$.'}]},
             {'title': '🌿 2단계 · [양변 비교와 소거] $f(\\alpha) - f(0) = f(2) = \\dfrac{5}{2}$ 이끌어내기',
              'title_en': '🌿 Step 2 · [Canceling $f(t)$] Deriving $f(\\alpha) - f(0) = f(2) = \\dfrac{5}{2}$',
              'knowledge': '1단계에서 구한 좌변 $2f(\\alpha) - 2f(2) - f(0) + f(t)$가 조건 (나)의 우변 $f(t) + f(0)$과 같습니다! 양변에서 똑같은 '
                           '$f(t)$를 지우면:$$2f(\\alpha) - 2f(2) - f(0) = f(0) \\implies 2f(\\alpha) - 2f(0) = 2f(2) '
                           '\\implies f(\\alpha) - f(0) = f(2)$$',
              'knowledge_en': 'Equating $2f(\\alpha) - 2f(2) - f(0) + f(t) = f(t) + f(0)$ and canceling $f(t)$ gives '
                              '$f(\\alpha) - f(0) = f(2)$.',
              'questions': [{'level_label': '등식 정리 디딤돌 2',
                             'level_label_en': 'Equation Simplification Step 2',
                             'stem': '조건 (가)에서 극솟값 $f(2) = \\dfrac{5}{2}$이므로, 방금 유도한 $f(\\alpha) - f(0) = f(2)$에 의해 '
                                     '$f(\\alpha) - f(0)$의 값은 얼마인가요?',
                             'stem_en': 'Since $f(2) = \\dfrac{5}{2}$ by Condition (가), what is $f(\\alpha) - f(0)$?',
                             'options': ['$\\frac{1}{2}$', '$1$', '$\\frac{3}{2}$', '$2$', '$\\frac{5}{2}$'],
                             'answer': 5,
                             'exp': '$f(\\alpha) - f(0) = f(2) = \\dfrac{5}{2}$입니다.',
                             'exp_en': '$f(\\alpha) - f(0) = \\dfrac{5}{2}$.'}]},
             {'title': "🌱 3단계 · [도함수 식 세우기] 최고차항 계수가 $1$이고 $x = \\alpha, 2$에서 극값을 갖는 $f'(x)$",
              'title_en': "🌱 Step 3 · [Derivative Formula] Writing $f'(x) = 3(x-\\alpha)(x-2)$",
              'knowledge': '최고차항의 계수가 $1$인 삼차함수 $f(x) = x^3 + \\cdots$를 미분하면 최고차항의 계수가 $3$인 이차함수가 됩니다. 극대점 $x = '
                           "\\alpha$와 극소점 $x = 2$에서 미분계수가 $0$이므로:$$f'(x) = 3(x - \\alpha)(x - 2) = 3x^2 - 3(\\alpha + "
                           '2)x + 6\\alpha$$',
              'knowledge_en': 'Since $f(x)$ is monic cubic with extrema at $x = \\alpha$ and $x = 2$, its derivative '
                              "is $f'(x) = 3(x-\\alpha)(x-2) = 3x^2 - 3(\\alpha+2)x + 6\\alpha$.",
              'questions': [{'level_label': '정적분으로 표현 디딤돌 3',
                             'level_label_en': 'Integral Expression Step 3',
                             'stem': "$f(\\alpha) - f(0) = \\int_0^\\alpha f'(x)dx = \\left[x^3 - \\frac{3}{2}(\\alpha "
                                     '+ 2)x^2 + 6\\alpha x\\right]_0^\\alpha$에 $x = \\alpha$를 대입하여 정리한 식은?',
                             'stem_en': 'Evaluating $\\int_0^\\alpha \\left(3x^2 - 3(\\alpha+2)x + 6\\alpha\\right)dx$ '
                                        'gives what expression in $\\alpha$?',
                             'options': ['$-\\frac{1}{2}\\alpha^3 + 3\\alpha^2$',
                                         '$\\frac{1}{2}\\alpha^3 + 3\\alpha^2$',
                                         '$-\\alpha^3 + 3\\alpha^2$',
                                         '$-\\frac{1}{2}\\alpha^3 + 6\\alpha^2$',
                                         '$\\alpha^3 - 3\\alpha^2$'],
                             'answer': 1,
                             'exp': '$\\alpha^3 - \\frac{3}{2}\\alpha^3 - 3\\alpha^2 + 6\\alpha^2 = '
                                    '-\\frac{1}{2}\\alpha^3 + 3\\alpha^2$입니다.',
                             'exp_en': '$-\\frac{1}{2}\\alpha^3 + 3\\alpha^2$.'}]},
             {'title': '🌱 4단계 · [극대점 $\\alpha$ 결정] $-\\dfrac{1}{2}\\alpha^3 + 3\\alpha^2 = \\dfrac{5}{2}$ 풀어 $\\alpha '
                       '= 1$ 찾기',
              'title_en': '🌱 Step 4 · [Solving for $\\alpha$] Finding $\\alpha = 1$ from $\\alpha^3 - 6\\alpha^2 + 5 = '
                          '0$',
              'knowledge': '2단계와 3단계 결과를 합치면 $-\\dfrac{1}{2}\\alpha^3 + 3\\alpha^2 = \\dfrac{5}{2}$입니다. 양변에 $-2$를 곱해 '
                           '이항하면:$$\\alpha^3 - 6\\alpha^2 + 5 = 0$$여기에 $\\alpha = 1$을 대입하면 $1 - 6 + 5 = 0$이 되어 조립제법으로 '
                           '$(\\alpha - 1)(\\alpha^2 - 5\\alpha - 5) = 0$으로 인수분해됩니다!',
              'knowledge_en': 'Multiplying $-\\frac{1}{2}\\alpha^3 + 3\\alpha^2 = \\frac{5}{2}$ by $-2$ gives '
                              '$\\alpha^3 - 6\\alpha^2 + 5 = (\\alpha - 1)(\\alpha^2 - 5\\alpha - 5) = 0$.',
              'questions': [{'level_label': '극대점 위치 디딤돌 4',
                             'level_label_en': 'Locating Local Max Step 4',
                             'stem': '$(\\alpha - 1)(\\alpha^2 - 5\\alpha - 5) = 0$의 실근 중에서 $0 < \\alpha < 2$를 만족시키는 '
                                     '극대점의 $x$좌표 $\\alpha$는?',
                             'stem_en': 'Which root of $(\\alpha - 1)(\\alpha^2 - 5\\alpha - 5) = 0$ lies in the '
                                        'interval $0 < \\alpha < 2$?',
                             'options': ['$\\frac{1}{2}$', '$1$', '$\\frac{4}{3}$', '$\\frac{3}{2}$', '$\\frac{5}{3}$'],
                             'answer': 2,
                             'exp': '$0 < \\alpha < 2$인 실근은 $\\alpha = 1$뿐입니다.',
                             'exp_en': '$\\alpha = 1$.'}]},
             {'title': '🌳 5단계 · [극값의 차 공식] $f(1) - f(2) = \\dfrac{1}{2}(2 - 1)^3$으로 극댓값 $f(1)$ 구하기',
              'title_en': '🌳 Step 5 · [Extrema Difference Formula] Finding local maximum $f(1)$',
              'knowledge': "$\\alpha = 1$일 때 $f'(x) = 3(x - 1)(x - 2)$이므로:$$f(1) - f(2) = \\int_2^1 3(x-1)(x-2)dx = "
                           '\\frac{3}{6}(2 - 1)^3 = \\frac{1}{2}$$조건 (가)에서 극솟값 $f(2) = \\dfrac{5}{2}$이므로 극댓값 $f(1)$을 '
                           '바로 구할 수 있습니다!',
              'knowledge_en': 'By the cubic extrema difference formula, $f(1) - f(2) = \\frac{3}{6}(2 - 1)^3 = '
                              '\\frac{1}{2}$. Since $f(2) = \\frac{5}{2}$, we immediately find $f(1)$.',
              'questions': [{'level_label': '극댓값 $f(1)$ 디딤돌 5',
                             'level_label_en': 'Local Maximum $f(1)$ Step 5',
                             'stem': '$f(2) = \\dfrac{5}{2}$이고 $f(1) - f(2) = \\dfrac{1}{2}$일 때, 극댓값 $f(1) = '
                                     '\\dfrac{5}{2} + \\dfrac{1}{2}$의 값은?',
                             'stem_en': 'Given $f(2) = \\dfrac{5}{2}$ and $f(1) - f(2) = \\dfrac{1}{2}$, what is '
                                        '$f(1)$?',
                             'options': ['$2$', '$\\frac{5}{2}$', '$3$', '$\\frac{7}{2}$', '$4$'],
                             'answer': 3,
                             'exp': '$\\dfrac{5}{2} + \\dfrac{1}{2} = \\dfrac{6}{2} = 3$이므로 $f(1) = 3$입니다.',
                             'exp_en': '$f(1) = 3$.'}]},
             {'title': '🌳 6단계 · [$f(0)$ 도출] $f(1) - f(0) = \\dfrac{5}{2}$에 $f(1) = 3$ 대입하기',
              'title_en': '🌳 Step 6 · [Finding $f(0)$] Using $f(1) - f(0) = \\dfrac{5}{2}$ with $f(1) = 3$',
              'knowledge': '2단계에서 $f(\\alpha) - f(0) = \\dfrac{5}{2}$, 즉 $f(1) - f(0) = \\dfrac{5}{2}$였습니다! 방금 5단계에서 '
                           '$f(1) = 3$을 구했으므로 $3 - f(0) = \\dfrac{5}{2}$입니다.',
              'knowledge_en': 'From Step 2, $f(1) - f(0) = \\frac{5}{2}$. Substituting $f(1) = 3$ gives $3 - f(0) = '
                              '\\frac{5}{2}$.',
              'questions': [{'level_label': '$f(0)$ 계산 디딤돌 6',
                             'level_label_en': 'Evaluating $f(0)$ Step 6',
                             'stem': '$3 - f(0) = \\dfrac{5}{2}$에서 $f(0) = 3 - \\dfrac{5}{2}$의 값을 기약분수 '
                                     '$\\dfrac{q}{p}$로 나타내면?',
                             'stem_en': 'From $3 - f(0) = \\dfrac{5}{2}$, what is $f(0) = \\dfrac{q}{p}$?',
                             'options': ['$\\frac{1}{4}$',
                                         '$\\frac{1}{3}$',
                                         '$\\frac{1}{2}$',
                                         '$\\frac{2}{3}$',
                                         '$\\frac{3}{2}$'],
                             'answer': 3,
                             'exp': '$3 - \\dfrac{5}{2} = \\dfrac{6 - 5}{2} = \\dfrac{1}{2}$입니다.',
                             'exp_en': '$f(0) = \\dfrac{1}{2}$.'}]},
             {'title': '💎 7단계 · [함숫값 검산] $f(x) = x^3 - \\dfrac{9}{2}x^2 + 6x + \\dfrac{1}{2}$에서 $f(2)$ 확인하기',
              'title_en': '💎 Step 7 · [Verification] Checking $f(2)$ in $f(x) = x^3 - \\dfrac{9}{2}x^2 + 6x + '
                          '\\dfrac{1}{2}$',
              'knowledge': "$f'(x) = 3(x-1)(x-2) = 3x^2 - 9x + 6$을 적분하고 $f(0) = \\dfrac{1}{2}$을 넣으면 $f(x) = x^3 - "
                           '\\dfrac{9}{2}x^2 + 6x + \\dfrac{1}{2}$입니다. 여기에 $x = 2$를 대입해 문제의 조건 $f(2) = \\dfrac{5}{2}$가 '
                           '맞는지 검산해 봅시다!',
              'knowledge_en': 'Verify that $f(x) = x^3 - \\frac{9}{2}x^2 + 6x + \\frac{1}{2}$ satisfies $f(2) = '
                              '\\frac{5}{2}$.',
              'questions': [{'level_label': '극솟값 검산 디딤돌 7',
                             'level_label_en': 'Minimum Verification Step 7',
                             'stem': '$f(2) = 2^3 - \\dfrac{9}{2}(2^2) + 6(2) + \\dfrac{1}{2} = 8 - 18 + 12 + '
                                     '\\dfrac{1}{2}$을 계산한 값은?',
                             'stem_en': 'What is $8 - 18 + 12 + \\dfrac{1}{2}$?',
                             'options': ['$\\frac{3}{2}$', '$2$', '$\\frac{5}{2}$', '$3$', '$\\frac{7}{2}$'],
                             'answer': 3,
                             'exp': '$2 + \\dfrac{1}{2} = \\dfrac{5}{2}$로 조건 (가)와 정확히 일치합니다!',
                             'exp_en': '$2 + \\dfrac{1}{2} = \\dfrac{5}{2}$.'}]},
             {'title': '🏆 8단계 · [최종 정답 완성] 서로소인 자연수 $p + q$ 구하기',
              'title_en': '🏆 Step 8 · [Final Synthesis] Computing $p + q$',
              'knowledge': '$f(0) = \\dfrac{1}{2} = \\dfrac{q}{p}$에서 $p = 2, q = 1$이므로 $p + q = 3$입니다.',
              'knowledge_en': 'From $\\dfrac{q}{p} = \\dfrac{1}{2}$, we have $p = 2, q = 1$, so $p + q = 3$.',
              'questions': [{'level_label': '최종 종합 디딤돌 8',
                             'level_label_en': 'Final Synthesis Step 8',
                             'stem': '$p = 2$, $q = 1$일 때, 최종 정답 $p + q$의 값은?',
                             'stem_en': 'With $p = 2$ and $q = 1$, what is $p + q$?',
                             'options': ['$2$', '$3$', '$4$', '$5$', '$7$'],
                             'answer': 2,
                             'exp': '$p + q = 2 + 1 = 3$입니다.',
                             'exp_en': '$p + q = 2 + 1 = 3$.'}]}],
  'final': {'stem': '최고차항의 계수가 $1$인 삼차함수 $f(x)$가 다음 조건을 만족시킬 때, $f(0) = \\dfrac{q}{p}$이다. $p + q$의 값을 구하시오. (단, $p$와 '
                    '$q$는 서로소인 자연수이다.) [4점]<br><br>(가) 함수 $f(x)$는 $x = 2$에서 극솟값 $\\dfrac{5}{2}$를 갖는다.<br>(나) $t > 2$인 '
                    "모든 실수 $t$에 대하여 $\\int_0^t |f'(x)|dx = f(t) + f(0)$ 이다.",
            'stem_en': 'A monic cubic function $f(x)$ satisfies:<br>(가) $f(x)$ has a local minimum of $\\dfrac{5}{2}$ '
                       "at $x = 2$.<br>(나) For all real $t > 2$, $\\int_0^t |f'(x)|dx = f(t) + f(0)$.<br>If $f(0) = "
                       '\\dfrac{q}{p}$ in lowest terms, find $p + q$. [4 points]',
            'options': ['$2$', '$3$', '$4$', '$5$', '$7$'],
            'answer': 2,
            'exp': '극대점의 $x$좌표를 $\\alpha$ ($0 < \\alpha < 2$)라 하면 조건 (나)에서 $f(\\alpha) - f(0) = f(2) = '
                   '\\dfrac{5}{2}$이고 $\\alpha = 1$입니다. 따라서 $f(x) = x^3 - \\dfrac{9}{2}x^2 + 6x + \\dfrac{1}{2}$이므로 '
                   '$f(0) = \\dfrac{1}{2}$, $p + q = 3$입니다.',
            'exp_en': 'Letting $x = \\alpha \\in (0, 2)$ be the local maximum point, Condition (나) gives $f(\\alpha) - '
                      'f(0) = f(2) = \\dfrac{5}{2}$, which yields $\\alpha = 1$ and $f(0) = \\dfrac{1}{2}$, so $p + q '
                      '= 3$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        "<p>본 문항은 <b>도함수의 절댓값 정적분 $\\int_0^t |f'(x)|dx$의 기하학적 의미(함숫값의 총 변화량)</b>를 분석하여 극대점의 위치를 결정하는 "
                        '수학II 준킬러 문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 구간 $[0, \\alpha], [\\alpha, 2], [2, t]$로 나누어 적분 정리</b><br>\n'
                        '  $0 < \\alpha < 2 < t$일 때:<br>\n'
                        "  $$\\int_0^t |f'(x)|dx = (f(\\alpha) - f(0)) + (f(\\alpha) - f(2)) + (f(t) - f(2)) = "
                        '2f(\\alpha) - 2f(2) - f(0) + f(t)$$\n'
                        '  이 식이 $f(t) + f(0)$과 같으므로:<br>\n'
                        '  $$2f(\\alpha) - 2f(2) - f(0) = f(0) \\implies f(\\alpha) - f(0) = f(2) = '
                        '\\frac{5}{2}$$<br>\n'
                        '  <b>2단계: $\\alpha$와 $f(0)$ 구하기</b><br>\n'
                        '  $$f(\\alpha) - f(0) = \\int_0^\\alpha 3(x - \\alpha)(x - 2)dx = -\\frac{1}{2}\\alpha^3 + '
                        '3\\alpha^2 = \\frac{5}{2}$$\n'
                        '  $$\\alpha^3 - 6\\alpha^2 + 5 = (\\alpha - 1)(\\alpha^2 - 5\\alpha - 5) = 0$$\n'
                        '  $0 < \\alpha < 2$이므로 $\\alpha = 1$입니다.<br>\n'
                        '  극댓값과 극솟값의 차 공식에 의해 $f(1) - f(2) = \\frac{1}{2}(2 - 1)^3 = \\frac{1}{2}$이므로 $f(1) = '
                        '\\frac{5}{2} + \\frac{1}{2} = 3$이고:<br>\n'
                        '  $$f(0) = f(1) - \\frac{5}{2} = 3 - \\frac{5}{2} = \\frac{1}{2}$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 $f(0) = \\dfrac{1}{2} = \\dfrac{q}{p}$에서 $p = 2, q = 1$이므로 $p + q =$ <b>$3$</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           "<p>This problem uses the <b>total variation integral $\\int_0^t |f'(x)|dx$</b> to locate "
                           'the local maximum $x = \\alpha$ of a monic cubic function.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           "  <b>Step 1: Split the integral by the sign of $f'(x)$</b><br>\n"
                           "  For $0 < \\alpha < 2 < t$, $f'(x) = 3(x-\\alpha)(x-2)$ is positive on $(0, \\alpha)$, "
                           'negative on $(\\alpha, 2)$, and positive on $(2, t)$:<br>\n'
                           "  $$\\int_0^t |f'(x)|dx = 2f(\\alpha) - 2f(2) - f(0) + f(t) = f(t) + f(0) \\implies "
                           'f(\\alpha) - f(0) = f(2) = \\frac{5}{2}$$<br>\n'
                           '  <b>Step 2: Solve for $\\alpha$ and $f(0)$</b><br>\n'
                           '  $$f(\\alpha) - f(0) = -\\frac{1}{2}\\alpha^3 + 3\\alpha^2 = \\frac{5}{2} \\implies '
                           '(\\alpha - 1)(\\alpha^2 - 5\\alpha - 5) = 0 \\implies \\alpha = 1$$\n'
                           '  Since $f(1) - f(2) = \\frac{1}{2}(2-1)^3 = \\frac{1}{2}$, we get $f(1) = 3$ and $f(0) = '
                           '3 - \\frac{5}{2} = \\frac{1}{2}$.\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  Thus $p = 2, q = 1$ and $p + q =$ <b>$3$</b>.\n'
                           '</p>'}},
 {'slug': 'c261022',
  'qNum': '22',
  'subject': '공통(수학I·II)',
  'title': '[2026학년도 10월 고3 22번] 홀짝에 따라 분기하는 귀납적 수열의 역추적',
  'title_en': '[2026 AY Oct Exam Grade 12 #22] Backtracking an Inductively Defined Sequence with Parity Branching',
  'summary_ko': '$a_3=a_6$ 조건에서 홀짝 갈래를 분석해 $a_3=15, 25$를 찾고 거꾸로 역추적하여 가능한 네 개의 $a_1$의 합 $202$ 구하기',
  'summary_en': 'Analyze parity branches for $a_3=a_6$ to find $a_3 \\in \\{15, 25\\}$, then backtrack to $a_1$ to '
                'obtain the sum $24+47+44+87=202$.',
  'tags': ['공통(수학I·II)', '수학I', '수열', '수학적귀납법', '수열의역추적', '단답형', '22번'],
  'symbols': [{'sym': '$a_{n+1} = \\dfrac{1}{2}(a_n + 1) + n$',
               'desc': '$a_n$이 홀수인 경우 다음 항을 만드는 규칙',
               'desc_en': 'Rule for the next term when $a_n$ is odd.'},
              {'sym': '$a_{n+1} = a_n + n$',
               'desc': '$a_n$이 짝수인 경우 다음 항을 만드는 규칙',
               'desc_en': 'Rule for the next term when $a_n$ is even.'},
              {'sym': '$a_3 = a_6$',
               'desc': '세 번째 항에서 세 번 규칙을 거치면 다시 자기 자신으로 돌아옴',
               'desc_en': 'Period-3 return condition from the 3rd term to the 6th term.'}],
  'levels': [{'title': '🔰 1단계 · [초등 홀짝 규칙 연습] $a_3 = 15$(홀수)일 때 $a_4, a_5, a_6$ 순서대로 구해보기',
              'title_en': '🔰 Step 1 · [Elementary Parity Rules] Computing $a_4, a_5, a_6$ starting from $a_3 = 15$ '
                          '(odd)',
              'knowledge': '조건 (가)의 규칙은 아주 간단합니다!<ul><li><b>$a_n$이 홀수일 때</b>: $a_n$에 $1$을 더해 반으로 나눈 뒤 번호 $n$을 더합니다 '
                           '$\\implies a_{n+1} = \\dfrac{1}{2}(a_n + 1) + n$</li><li><b>$a_n$이 짝수일 때</b>: $a_n$에 그냥 번호 '
                           '$n$을 더합니다 $\\implies a_{n+1} = a_n + n$</li></ul>먼저 $a_3 = 15$(홀수, $n=3$)에서 출발해 '
                           '볼까요?<ul><li>$a_4 = \\dfrac{1}{2}(15 + 1) + 3 = 8 + 3 = 11$ (홀수, $n=4$)</li><li>$a_5 = '
                           '\\dfrac{1}{2}(11 + 1) + 4 = 6 + 4 = 10$ (짝수, $n=5$)</li></ul>이제 $a_5 = 10$은 짝수이므로 짝수 '
                           '규칙($a_6 = a_5 + 5$)을 적용합니다!',
              'knowledge_en': 'By Condition (가), when $a_n$ is odd, $a_{n+1} = \\frac{1}{2}(a_n + 1) + n$; when $a_n$ '
                              'is even, $a_{n+1} = a_n + n$. Starting with $a_3 = 15$ (odd, $n=3$): $a_4 = '
                              '\\frac{1}{2}(16) + 3 = 11$ (odd, $n=4$), and $a_5 = \\frac{1}{2}(12) + 4 = 10$ (even, '
                              '$n=5$).',
              'questions': [{'level_label': '초등 짝수 규칙 디딤돌 1',
                             'level_label_en': 'Elementary Even Rule Step 1',
                             'stem': '초등학교 덧셈 규칙으로, $a_5 = 10$(짝수, $n = 5$)일 때 짝수 규칙 $a_6 = a_5 + 5$로 계산한 $a_6$의 값은?',
                             'stem_en': 'Using elementary addition, when $a_5 = 10$ (even, $n = 5$), what is $a_6 = '
                                        'a_5 + 5$?',
                             'options': ['$12$', '$14$', '$15$', '$16$', '$20$'],
                             'answer': 3,
                             'exp': '$a_6 = 10 + 5 = 15$가 되어 $a_3 = a_6 = 15$가 정확히 성립합니다! (즉, 홀 $\\to$ 홀 $\\to$ 짝 갈래에서 '
                                    '$a_3 = 15$가 첫 번째 해입니다.)',
                             'exp_en': '$a_6 = 10 + 5 = 15 = a_3$.'}]},
             {'title': '🌿 2단계 · [두 번째 주기 해 찾기] (홀 $\\to$ 짝 $\\to$ 짝) 갈래에서 $a_3 = 25$ 확인하기',
              'title_en': '🌿 Step 2 · [Second Periodic Solution] Verifying $a_3 = 25$ along (Odd $\\to$ Even $\\to$ '
                          'Even)',
              'knowledge': '$a_3$가 짝수이면 $a_4 = a_3 + 3 > a_3$이고 계속 커져서 $a_6 = a_3$가 될 수 없습니다. 따라서 $a_3$는 반드시 홀수여서 첫 '
                           '단계에 작아져야 합니다! $a_3$(홀수) $\\to a_4$(짝수) $\\to a_5$(짝수) 갈래를 식으로 세워 봅시다.<ul><li>$a_4 = '
                           '\\dfrac{1}{2}(a_3 + 1) + 3$ (짝수)</li><li>$a_5 = a_4 + 4$ (짝수이므로 자동으로 $a_5$도 '
                           '짝수!)</li><li>$a_6 = a_5 + 5 = a_4 + 9 = \\dfrac{1}{2}(a_3 + 1) + 12$</li></ul>이 식이 $a_3$와 '
                           '같다고 놓으면 $\\dfrac{1}{2}(a_3 + 1) + 12 = a_3$입니다!',
              'knowledge_en': 'Along the branch $a_3$ (odd) $\\to a_4$ (even) $\\to a_5$ (even): $a_4 = '
                              '\\frac{1}{2}(a_3 + 1) + 3$, $a_5 = a_4 + 4$, and $a_6 = a_5 + 5 = \\frac{1}{2}(a_3 + 1) '
                              '+ 12 = a_3$.',
              'questions': [{'level_label': '두 번째 해 a3 디딤돌 2',
                             'level_label_en': 'Second Solution a3 Step 2',
                             'stem': '방정식 $\\dfrac{1}{2}(a_3 + 1) + 12 = a_3$의 양변에 $2$를 곱하면 $a_3 + 1 + 24 = 2a_3$입니다. '
                                     '이때 홀수 $a_3$의 값은?',
                             'stem_en': 'Solving $a_3 + 25 = 2a_3$, what is the value of $a_3$?',
                             'options': ['$19$', '$21$', '$23$', '$25$', '$27$'],
                             'answer': 4,
                             'exp': '$a_3 = 25$(홀수)일 때 $a_4 = 16$(짝수) $\\to a_5 = 20$(짝수) $\\to a_6 = 25$가 되어 완벽히 '
                                    '성립합니다!',
                             'exp_en': '$a_3 = 25$ gives $25 \\to 16 \\to 20 \\to 25$.'}]},
             {'title': '🌱 3단계 · [한 칸 역추적 ①] $a_3 = 15$가 되도록 하는 자연수 $a_2$ 구하기',
              'title_en': '🌱 Step 3 · [Backtracking Part 1] Finding valid $a_2$ when $a_3 = 15$',
              'knowledge': '이제 $n = 2$일 때의 규칙으로 $a_3 = 15$에서 $a_2$를 거꾸로 찾아봅시다!<ul><li>만약 <b>$a_2$가 짝수</b>라면: $a_3 = '
                           "a_2 + 2 = 15 \\implies a_2 = 13$인데, $13$은 홀수이므로 '짝수' 가정에 모순입니다(탈락!).</li><li>만약 <b>$a_2$가 "
                           '홀수</b>라면: $a_3 = \\dfrac{1}{2}(a_2 + 1) + 2 = 15$입니다.</li></ul>',
              'knowledge_en': 'Backtracking from $a_3 = 15$ ($n = 2$): if $a_2$ were even, $a_2 + 2 = 15 \\implies a_2 '
                              '= 13$ (odd, contradiction!). If $a_2$ is odd, $\\frac{1}{2}(a_2 + 1) + 2 = 15$.',
              'questions': [{'level_label': 'a2 역추적 ① 디딤돌 3',
                             'level_label_en': 'Backtracking a2 (Case 1) Step 3',
                             'stem': '$\\dfrac{1}{2}(a_2 + 1) + 2 = 15$에서 $\\dfrac{1}{2}(a_2 + 1) = 13$입니다. 이를 만족시키는 '
                                     '홀수 $a_2$의 값은?',
                             'stem_en': 'From $\\dfrac{1}{2}(a_2 + 1) = 13$, what is the odd integer $a_2$?',
                             'options': ['$21$', '$23$', '$25$', '$27$', '$29$'],
                             'answer': 3,
                             'exp': '$a_2 + 1 = 26 \\implies a_2 = 25$(홀수)이므로 성립합니다.',
                             'exp_en': '$a_2 = 25$ (odd).'}]},
             {'title': '🌱 4단계 · [첫째항 역추적 ①] $a_2 = 25$에서 가능한 두 개의 $a_1$ 구하기',
              'title_en': '🌱 Step 4 · [Backtracking to $a_1$ (Case 1)] Finding the two values of $a_1$ from $a_2 = 25$',
              'knowledge': '방금 구한 $a_2 = 25$에서 $n = 1$일 때의 규칙으로 첫째항 $a_1$을 역추적해 봅시다!<ul><li><b>$a_1$이 짝수인 경우</b>: $a_2 '
                           '= a_1 + 1 = 25 \\implies a_1 = 24$ ($24$는 짝수이므로 합격!)</li><li><b>$a_1$이 홀수인 경우</b>: $a_2 = '
                           '\\dfrac{1}{2}(a_1 + 1) + 1 = 25 \\implies \\dfrac{1}{2}(a_1 + 1) = 24 \\implies a_1 = 47$ '
                           '($47$은 홀수이므로 합격!)</li></ul>',
              'knowledge_en': 'From $a_2 = 25$ ($n = 1$): if $a_1$ is even, $a_1 + 1 = 25 \\implies a_1 = 24$ (even, '
                              'valid!); if $a_1$ is odd, $\\frac{1}{2}(a_1 + 1) + 1 = 25 \\implies a_1 = 47$ (odd, '
                              'valid!).',
              'questions': [{'level_label': '첫째항 후보 ① 디딤돌 4',
                             'level_label_en': 'First Term Candidates 1 Step 4',
                             'stem': '$a_2 = 25$일 때 나오는 두 개의 첫째항 $a_1 = 24$(짝수)와 $a_1 = 47$(홀수)의 합 $24 + 47$은?',
                             'stem_en': 'What is the sum $24 + 47$ of the two valid values of $a_1$ obtained from $a_2 '
                                        '= 25$?',
                             'options': ['$61$', '$67$', '$71$', '$75$', '$81$'],
                             'answer': 3,
                             'exp': '$24 + 47 = 71$입니다.',
                             'exp_en': '$24 + 47 = 71$.'}]},
             {'title': '🌳 5단계 · [한 칸 역추적 ②] $a_3 = 25$가 되도록 하는 자연수 $a_2$ 구하기',
              'title_en': '🌳 Step 5 · [Backtracking Part 2] Finding valid $a_2$ when $a_3 = 25$',
              'knowledge': '이제 두 번째 주기 해인 $a_3 = 25$에서 $n = 2$일 때의 규칙으로 $a_2$를 역추적해 봅시다!<ul><li>만약 <b>$a_2$가 짝수</b>라면: '
                           "$a_3 = a_2 + 2 = 25 \\implies a_2 = 23$인데, $23$은 홀수이므로 '짝수' 가정에 모순입니다(탈락!).</li><li>만약 "
                           '<b>$a_2$가 홀수</b>라면: $a_3 = \\dfrac{1}{2}(a_2 + 1) + 2 = 25$입니다.</li></ul>',
              'knowledge_en': 'Backtracking from $a_3 = 25$ ($n = 2$): if $a_2$ were even, $a_2 + 2 = 25 \\implies a_2 '
                              '= 23$ (odd, contradiction!). If $a_2$ is odd, $\\frac{1}{2}(a_2 + 1) + 2 = 25$.',
              'questions': [{'level_label': 'a2 역추적 ② 디딤돌 5',
                             'level_label_en': 'Backtracking a2 (Case 2) Step 5',
                             'stem': '$\\dfrac{1}{2}(a_2 + 1) + 2 = 25$에서 $\\dfrac{1}{2}(a_2 + 1) = 23$입니다. 이를 만족시키는 '
                                     '홀수 $a_2$의 값은?',
                             'stem_en': 'From $\\dfrac{1}{2}(a_2 + 1) = 23$, what is the odd integer $a_2$?',
                             'options': ['$41$', '$43$', '$45$', '$47$', '$49$'],
                             'answer': 3,
                             'exp': '$a_2 + 1 = 46 \\implies a_2 = 45$(홀수)이므로 성립합니다.',
                             'exp_en': '$a_2 = 45$ (odd).'}]},
             {'title': '🌳 6단계 · [첫째항 역추적 ②: 짝수] $a_2 = 45$에서 짝수인 $a_1$ 구하기',
              'title_en': '🌳 Step 6 · [Backtracking to Even $a_1$ (Case 2)] Finding even $a_1$ from $a_2 = 45$',
              'knowledge': '$a_2 = 45$에서 $n = 1$일 때 $a_1$이 짝수이면 짝수 규칙 $a_2 = a_1 + 1 = 45$가 적용됩니다.',
              'knowledge_en': 'From $a_2 = 45$ ($n = 1$), if $a_1$ is even, then $a_2 = a_1 + 1 = 45$.',
              'questions': [{'level_label': '짝수 a1 디딤돌 6',
                             'level_label_en': 'Even a1 Step 6',
                             'stem': '$a_1 + 1 = 45$를 만족시키는 짝수 $a_1$의 값은?',
                             'stem_en': 'What is the even integer $a_1$ satisfying $a_1 + 1 = 45$?',
                             'options': ['$40$', '$42$', '$44$', '$46$', '$48$'],
                             'answer': 3,
                             'exp': '$a_1 = 44$는 짝수이므로 조건을 만족합니다.',
                             'exp_en': '$a_1 = 44$.'}]},
             {'title': '💎 7단계 · [첫째항 역추적 ②: 홀수] $a_2 = 45$에서 홀수인 $a_1$ 구하기',
              'title_en': '💎 Step 7 · [Backtracking to Odd $a_1$ (Case 2)] Finding odd $a_1$ from $a_2 = 45$',
              'knowledge': '$a_2 = 45$에서 $n = 1$일 때 $a_1$이 홀수이면 홀수 규칙 $\\dfrac{1}{2}(a_1 + 1) + 1 = 45$가 적용됩니다.',
              'knowledge_en': 'From $a_2 = 45$ ($n = 1$), if $a_1$ is odd, then $\\frac{1}{2}(a_1 + 1) + 1 = 45$.',
              'questions': [{'level_label': '홀수 a1 디딤돌 7',
                             'level_label_en': 'Odd a1 Step 7',
                             'stem': '$\\dfrac{1}{2}(a_1 + 1) + 1 = 45 \\implies \\dfrac{1}{2}(a_1 + 1) = 44$를 만족시키는 '
                                     '홀수 $a_1$의 값은?',
                             'stem_en': 'From $\\dfrac{1}{2}(a_1 + 1) = 44$, what is the odd integer $a_1$?',
                             'options': ['$83$', '$85$', '$87$', '$89$', '$91$'],
                             'answer': 3,
                             'exp': '$a_1 + 1 = 88 \\implies a_1 = 87$(홀수)이므로 조건을 만족합니다.',
                             'exp_en': '$a_1 = 87$.'}]},
             {'title': '🏆 8단계 · [최종 정답 완성] 네 개의 $a_1 \\in \\{24, 47, 44, 87\\}$의 총합 구하기',
              'title_en': '🏆 Step 8 · [Final Synthesis] Total sum $24 + 47 + 44 + 87$',
              'knowledge': '4단계에서 구한 $24 + 47 = 71$과 6·7단계에서 구한 $44 + 87 = 131$을 더하면 모든 $a_1$의 값의 합이 완성됩니다!',
              'knowledge_en': 'Add $24 + 47 = 71$ and $44 + 87 = 131$ to obtain the sum of all possible values of '
                              '$a_1$.',
              'questions': [{'level_label': '최종 종합 디딤돌 8',
                             'level_label_en': 'Final Synthesis Step 8',
                             'stem': '가능한 모든 $a_1$의 값의 합 $(24 + 47) + (44 + 87) = 71 + 131$을 계산한 최종 정답은?',
                             'stem_en': 'What is the total sum $(24 + 47) + (44 + 87) = 71 + 131$?',
                             'options': ['$192$', '$198$', '$202$', '$206$', '$212$'],
                             'answer': 3,
                             'exp': '$71 + 131 = 202$입니다.',
                             'exp_en': '$71 + 131 = 202$.'}]}],
  'final': {'stem': '모든 항이 자연수이고 다음 조건을 만족시키는 모든 수열 $\\{a_n\\}$에 대하여 $a_1$의 값의 합을 구하시오. [4점]<br><br>(가) 모든 자연수 $n$에 '
                    '대하여<br>$$a_{n+1} = \\begin{cases} \\dfrac{1}{2}(a_n + 1) + n & (a_n\\text{이 홀수인 경우}) \\\\ a_n + n '
                    '& (a_n\\text{이 짝수인 경우}) \\end{cases}$$<br>(나) $a_3 = a_6$',
            'stem_en': 'For all sequences of natural numbers $\\{a_n\\}$ satisfying:<br>(가) $a_{n+1} = '
                       '\\dfrac{1}{2}(a_n + 1) + n$ if $a_n$ is odd, and $a_{n+1} = a_n + n$ if $a_n$ is even;<br>(나) '
                       '$a_3 = a_6$,<br>find the sum of all possible values of $a_1$. [4 points]',
            'options': ['$192$', '$198$', '$202$', '$206$', '$212$'],
            'answer': 3,
            'exp': '$a_3 = a_6$을 만족하는 홀수 $a_3$는 $15$ ($15\\to 11\\to 10\\to 15$)와 $25$ ($25\\to 16\\to 20\\to 25$)이고, '
                   '이를 역추적하면 $a_2 \\in \\{25, 45\\}$, 다시 역추적하면 $a_1 \\in \\{24, 47, 44, 87\\}$이므로 합은 $202$입니다.',
            'exp_en': 'Solving $a_3 = a_6$ yields $a_3 \\in \\{15, 25\\}$, backtracking to $a_2 \\in \\{25, 45\\}$ and '
                      '$a_1 \\in \\{24, 47, 44, 87\\}$, whose sum is $202$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 공통 영역 최고난도(22번) 문항으로, <b>홀짝 분기 귀납적 정의에서 $a_3 = a_6$이 되는 주기 해를 찾고 첫째항 $a_1$까지 '
                        '역추적</b>하는 문제입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: $a_3 = a_6$을 만족하는 자연수 $a_3$ 구하기</b><br>\n'
                        '  짝수 규칙은 항상 항이 커지므로($a_{n+1} = a_n + n > a_n$), $a_3 = a_6$이 되려면 $a_3$는 반드시 홀수여야 합니다.<br>\n'
                        '  - <b>(경우 1) $a_3$(홀) $\\to a_4$(홀) $\\to a_5$(짝)</b>:<br>\n'
                        '    $$a_4 = \\frac{a_3+1}{2} + 3,\\quad a_5 = \\frac{a_4+1}{2} + 4,\\quad a_6 = a_5 + 5 = '
                        'a_3$$\n'
                        '    이를 풀면 $a_3 = 15$이며, 실제로 $15\\text{(홀)} \\to 11\\text{(홀)} \\to 10\\text{(짝)} \\to 15$가 '
                        '성립합니다.<br>\n'
                        '  - <b>(경우 2) $a_3$(홀) $\\to a_4$(짝) $\\to a_5$(짝)</b>:<br>\n'
                        '    $$a_4 = \\frac{a_3+1}{2} + 3,\\quad a_5 = a_4 + 4,\\quad a_6 = a_5 + 5 = \\frac{a_3+1}{2} '
                        '+ 12 = a_3$$\n'
                        '    이를 풀면 $a_3 = 25$이며, 실제로 $25\\text{(홀)} \\to 16\\text{(짝)} \\to 20\\text{(짝)} \\to 25$가 '
                        '성립합니다.<br><br>\n'
                        '  <b>2단계: $a_2$와 $a_1$ 역추적하기</b><br>\n'
                        '  - $a_3 = 15$일 때: $a_2$가 짝수이면 $a_2 + 2 = 15 \\implies a_2 = 13$(모순), 홀수이면 $\\frac{a_2+1}{2} '
                        '+ 2 = 15 \\implies a_2 = 25$(성립). 다시 $a_2 = 25$에서 $a_1$을 구하면 $a_1 + 1 = 25 \\implies a_1 = '
                        '24$(짝수 성립), $\\frac{a_1+1}{2} + 1 = 25 \\implies a_1 = 47$(홀수 성립).<br>\n'
                        '  - $a_3 = 25$일 때: $a_2$가 짝수이면 $a_2 + 2 = 25 \\implies a_2 = 23$(모순), 홀수이면 $\\frac{a_2+1}{2} '
                        '+ 2 = 25 \\implies a_2 = 45$(성립). 다시 $a_2 = 45$에서 $a_1$을 구하면 $a_1 + 1 = 45 \\implies a_1 = '
                        '44$(짝수 성립), $\\frac{a_1+1}{2} + 1 = 45 \\implies a_1 = 87$(홀수 성립).\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 조건을 만족시키는 모든 $a_1$의 값의 합은:<br>\n'
                        '  $$24 + 47 + 44 + 87 = 202$$\n'
                        '  정답은 <b>$202$</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem requires finding the periodic points satisfying $a_3 = a_6$ under a '
                           'parity-branching recurrence, then backtracking to $a_1$.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Determine valid values of $a_3$</b><br>\n'
                           '  Testing parity trajectories $a_3 \\to a_4 \\to a_5 \\to a_6$ yields two valid '
                           'cycles:<br>\n'
                           '  - $15 \\to 11 \\to 10 \\to 15$<br>\n'
                           '  - $25 \\to 16 \\to 20 \\to 25$<br><br>\n'
                           '  <b>Step 2: Backtrack to $a_2$ and $a_1$</b><br>\n'
                           '  - From $a_3 = 15$, only $a_2 = 25$ (odd) is valid, which gives $a_1 \\in \\{24, '
                           '47\\}$.<br>\n'
                           '  - From $a_3 = 25$, only $a_2 = 45$ (odd) is valid, which gives $a_1 \\in \\{44, 87\\}$.\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  Summing all valid values of $a_1$ gives $24 + 47 + 44 + 87 =$ <b>$202$</b>.\n'
                           '</p>'}}]
