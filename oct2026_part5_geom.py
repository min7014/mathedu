# -*- coding: utf-8 -*-
# Auto-upgraded with Elementary-to-Advanced Micro-Scaffolding

PART5_PROBLEMS = [{'slug': 'c2610g23',
  'qNum': '기하 23',
  'subject': '기하',
  'title': '[2026학년도 10월 고3 기하 23번] 평면벡터의 실수배와 성분 뺄셈 연산',
  'title_en': '[2026 AY Oct Exam Grade 12 Geometry #23] Scalar Multiplication and Component Subtraction of Plane '
              'Vectors',
  'summary_ko': '벡터 $\\vec{a}=(1, 3)$에서 $2\\vec{b}=(-4, 2)$를 성분별로 빼어 $k=1-(-4)=5$ 구하기',
  'summary_en': 'Subtract $2\\vec{b}=(-4, 2)$ from $\\vec{a}=(1, 3)$ componentwise to find $k=1-(-4)=5$.',
  'tags': ['기하', '평면벡터', '벡터의성분', '벡터의연산', '23번'],
  'symbols': [{'sym': '$2\\vec{b} = 2(-2, 1) = (-4, 2)$',
               'desc': '벡터의 각 성분에 2를 곱하는 실수배',
               'desc_en': 'Scalar multiplication multiplies each component by 2.'},
              {'sym': '$\\vec{a} - 2\\vec{b} = (1 - (-4), 3 - 2) = (5, 1)$',
               'desc': 'x성분은 x성분끼리, y성분은 y성분끼리 빼기',
               'desc_en': 'Componentwise subtraction of two plane vectors.'}],
  'levels': [{'title': '🔰 1단계 · [초등 곱셈] $(-2, 1)$의 각 숫자에 $2$ 곱하기',
              'title_en': '🔰 Step 1 · [Elementary Multiplication] Multiplying each number in $(-2, 1)$ by $2$',
              'knowledge': '벡터 $\\vec{b} = (-2, 1)$에 $2$를 곱한 $2\\vec{b}$는 초등학교 곱셈처럼 앞의 숫자와 뒤의 숫자에 각각 $2$를 곱하면 됩니다: $(2 '
                           '\\times (-2), 2 \\times 1) = (-4, 2)$.',
              'knowledge_en': 'By elementary multiplication, $2\\vec{b} = 2(-2, 1) = (2 \\times (-2), 2 \\times 1) = '
                              '(-4, 2)$.',
              'questions': [{'level_label': '초등 곱셈 디딤돌 1',
                             'level_label_en': 'Elementary Multiplication Step 1',
                             'stem': '초등학교 곱셈 원리에 따라 $\\vec{b} = (-2, 1)$의 각 성분에 $2$를 곱한 $2\\vec{b}$를 바르게 구한 것은?',
                             'stem_en': 'Using elementary multiplication, what is $2\\vec{b}$ for $\\vec{b} = (-2, '
                                        '1)$?',
                             'options': ['$(-4, 1)$', '$(-4, 2)$', '$(-2, 2)$', '$(4, 2)$', '$(-4, -2)$'],
                             'answer': 2,
                             'exp': '$(2 \\times (-2), 2 \\times 1) = (-4, 2)$입니다.',
                             'exp_en': '$(-4, 2)$.'}]},
             {'title': '🌿 2단계 · [$y$성분 확인] $\\vec{a} - 2\\vec{b}$의 $y$성분 구하기',
              'title_en': '🌿 Step 2 · [$y$-Component] Checking the $y$-component of $\\vec{a} - 2\\vec{b}$',
              'knowledge': '$\\vec{a} = (1, 3)$과 $2\\vec{b} = (-4, 2)$의 $y$성분끼리 빼면 $3 - 2 = 1$입니다.',
              'knowledge_en': 'Subtracting the $y$-components gives $3 - 2 = 1$.',
              'questions': [{'level_label': 'y성분 뺄셈 디딤돌 2',
                             'level_label_en': 'y-Component Step 2',
                             'stem': '$\\vec{a} = (1, 3)$과 $2\\vec{b} = (-4, 2)$에서 $y$성분끼리의 차 $3 - 2$는?',
                             'stem_en': 'What is the difference of the $y$-components $3 - 2$?',
                             'options': ['$-1$', '$0$', '$1$', '$2$', '$5$'],
                             'answer': 3,
                             'exp': '$3 - 2 = 1$로 문제의 $(k, 1)$의 $y$성분과 일치합니다.',
                             'exp_en': '$3 - 2 = 1$.'}]},
             {'title': '🌱 3단계 · [음수 뺄셈 부호] $1 - (-4)$를 덧셈으로 바꾸기',
              'title_en': '🌱 Step 3 · [Subtracting a Negative] Rewriting $1 - (-4)$ as addition',
              'knowledge': '음수 $-4$를 빼는 것은 양수 $4$를 더하는 것과 같습니다: $1 - (-4) = 1 + 4$.',
              'knowledge_en': 'Subtracting $-4$ is equivalent to adding $4$: $1 - (-4) = 1 + 4$.',
              'questions': [{'level_label': '부호 변환 디딤돌 3',
                             'level_label_en': 'Sign Rule Step 3',
                             'stem': '$x$성분끼리 뺀 식 $1 - (-4)$와 같은 식은?',
                             'stem_en': 'Which expression is equivalent to $1 - (-4)$?',
                             'options': ['$1 - 4$', '$-1 - 4$', '$1 + 4$', '$-1 + 4$', '$4 - 1$'],
                             'answer': 3,
                             'exp': '마이너스와 마이너스가 만나 플러스가 되므로 $1 + 4$입니다.',
                             'exp_en': '$1 - (-4) = 1 + 4$.'}]},
             {'title': '🌳 4단계 · [$x$성분 계산] $1 + 4$ 계산하기',
              'title_en': '🌳 Step 4 · [$x$-Component] Computing $1 + 4$',
              'knowledge': '$1 + 4 = 5$이므로 $\\vec{a} - 2\\vec{b} = (5, 1)$입니다.',
              'knowledge_en': '$1 + 4 = 5$, so $\\vec{a} - 2\\vec{b} = (5, 1)$.',
              'questions': [{'level_label': 'x성분 덧셈 디딤돌 4',
                             'level_label_en': 'x-Component Step 4',
                             'stem': '$\\vec{a} - 2\\vec{b}$를 성분으로 나타낸 결과는?',
                             'stem_en': 'What is $\\vec{a} - 2\\vec{b}$ in component form?',
                             'options': ['$(1, 1)$', '$(2, 1)$', '$(3, 1)$', '$(4, 1)$', '$(5, 1)$'],
                             'answer': 5,
                             'exp': '$(1 - (-4), 3 - 2) = (5, 1)$입니다.',
                             'exp_en': '$(5, 1)$.'}]},
             {'title': '💎 5단계 · [최종 종합] 실수 $k$의 값 구하기',
              'title_en': '💎 Step 5 · [Final Synthesis] Final value of $k$',
              'knowledge': '$(5, 1) = (k, 1)$이므로 $k = 5$입니다.',
              'knowledge_en': 'Comparing $(5, 1) = (k, 1)$ gives $k = 5$.',
              'questions': [{'level_label': '최종 종합 디딤돌 5',
                             'level_label_en': 'Final Synthesis Step 5',
                             'stem': '$\\vec{a} - 2\\vec{b} = (k, 1)$일 때, 실수 $k$의 값은?',
                             'stem_en': 'When $\\vec{a} - 2\\vec{b} = (k, 1)$, what is $k$?',
                             'options': ['$1$', '$2$', '$3$', '$4$', '$5$'],
                             'answer': 5,
                             'exp': '$k = 5$이므로 정답은 ⑤입니다.',
                             'exp_en': '$k = 5$ (choice ⑤).'}]}],
  'final': {'stem': '두 벡터 $\\vec{a} = (1, 3)$, $\\vec{b} = (-2, 1)$에 대하여 $\\vec{a} - 2\\vec{b} = (k, 1)$일 때, 실수 $k$의 '
                    '값은? [2점]',
            'stem_en': 'For vectors $\\vec{a} = (1, 3)$ and $\\vec{b} = (-2, 1)$, if $\\vec{a} - 2\\vec{b} = (k, 1)$, '
                       'what is the real number $k$? [2 points]',
            'options': ['$1$', '$2$', '$3$', '$4$', '$5$'],
            'answer': 5,
            'exp': '$\\vec{a} - 2\\vec{b} = (1, 3) - (-4, 2) = (5, 1) = (k, 1)$이므로 $k = 5$입니다.',
            'exp_en': '$\\vec{a} - 2\\vec{b} = (1, 3) - (-4, 2) = (5, 1)$, so $k = 5$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>평면벡터의 성분 연산(실수배와 뺄셈)</b>을 평가하는 기본 문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  $$\\vec{a} - 2\\vec{b} = (1, 3) - 2(-2, 1) = (1, 3) - (-4, 2) = (1 - (-4), 3 - 2) = (5, '
                        '1)$$\n'
                        '  따라서 $(5, 1) = (k, 1)$에서 $k = 5$입니다.\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 $k = 5$이므로 정답은 <b>⑤번</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem tests <b>componentwise scalar multiplication and subtraction of plane '
                           'vectors</b>.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  $$\\vec{a} - 2\\vec{b} = (1, 3) - (-4, 2) = (5, 1) \\implies k = 5$$\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  The correct answer is <b>choice ⑤ ($5$)</b>.\n'
                           '</p>'}},
 {'slug': 'c2610g24',
  'qNum': '기하 24',
  'subject': '기하',
  'title': '[2026학년도 10월 고3 기하 24번] 쌍곡선의 점근선의 방정식과 기울기',
  'title_en': '[2026 AY Oct Exam Grade 12 Geometry #24] Asymptotes of a Hyperbola and Their Slopes',
  'summary_ko': '쌍곡선 $\\dfrac{x^2}{a^2} - \\dfrac{y^2}{36} = 1$의 점근선 $y = \\pm\\dfrac{6}{a}x$에서 $\\dfrac{6}{a} = 2$를 '
                '풀어 $a=3$ 구하기',
  'summary_en': 'From the hyperbola $\\dfrac{x^2}{a^2} - \\dfrac{y^2}{36} = 1$ with asymptotes $y = '
                '\\pm\\dfrac{6}{a}x$, solve $\\dfrac{6}{a} = 2$ to find $a=3$.',
  'tags': ['기하', '이차곡선', '쌍곡선', '점근선의방정식', '24번'],
  'symbols': [{'sym': '$\\dfrac{x^2}{a^2} - \\dfrac{y^2}{b^2} = 1$',
               'desc': '쌍곡선의 기본 방정식 ($b^2 = 36 \\implies b = 6$)',
               'desc_en': 'Standard equation of a hyperbola with $b^2 = 36$.'},
              {'sym': '$y = \\pm \\dfrac{b}{a}x = \\pm \\dfrac{6}{a}x$',
               'desc': '쌍곡선이 한없이 가까워지는 두 직선(점근선)의 방정식',
               'desc_en': 'Equations of the two asymptotes of the hyperbola.'}],
  'levels': [{'title': '🔰 1단계 · [초등 구구단 제곱] 곱해서 $36$이 되는 양수 $b$ 찾기',
              'title_en': '🔰 Step 1 · [Elementary Multiplication] Finding $b > 0$ such that $b \\times b = 36$',
              'knowledge': '쌍곡선 식 $\\frac{x^2}{a^2} - \\frac{y^2}{36} = 1$에서 $y^2$ 아래의 분모 $36$은 초등학교 구구단 $6 \\times 6 '
                           '= 36$, 즉 $b^2 = 6^2$입니다.',
              'knowledge_en': 'In elementary multiplication, $6 \\times 6 = 36$, so $b^2 = 36 \\implies b = 6$.',
              'questions': [{'level_label': '초등 구구단 디딤돌 1',
                             'level_label_en': 'Elementary Multiplication Step 1',
                             'stem': '초등학교 구구단에서 똑같은 수를 두 번 곱해 $b^2 = 36$이 되는 양수 $b$의 값은?',
                             'stem_en': 'Using elementary multiplication, which positive number $b$ satisfies $b '
                                        '\\times b = 36$?',
                             'options': ['$4$', '$5$', '$6$', '$8$', '$9$'],
                             'answer': 3,
                             'exp': '$6 \\times 6 = 36$이므로 $b = 6$입니다.',
                             'exp_en': '$b = 6$.'}]},
             {'title': '🌿 2단계 · [점근선 공식] 쌍곡선의 점근선 기울기 식 세우기',
              'title_en': "🌿 Step 2 · [Asymptote Formula] Slope of the hyperbola's asymptotes",
              'knowledge': '쌍곡선 $\\frac{x^2}{a^2} - \\frac{y^2}{b^2} = 1$의 점근선의 방정식은 $y = \\pm \\frac{b}{a}x$입니다. 여기서 '
                           '$b = 6$이므로 점근선은 $y = \\pm \\frac{6}{a}x$입니다.',
              'knowledge_en': 'The asymptotes of $\\frac{x^2}{a^2} - \\frac{y^2}{b^2} = 1$ are $y = \\pm \\frac{b}{a}x '
                              '= \\pm \\frac{6}{a}x$.',
              'questions': [{'level_label': '점근선 기울기 디딤돌 2',
                             'level_label_en': 'Asymptote Slope Step 2',
                             'stem': '양수 $a$에 대하여 쌍곡선 $\\frac{x^2}{a^2} - \\frac{y^2}{36} = 1$의 양의 점근선 기울기는?',
                             'stem_en': 'For $a > 0$, what is the positive slope of the asymptote of $\\frac{x^2}{a^2} '
                                        '- \\frac{y^2}{36} = 1$?',
                             'options': ['$\\frac{a}{6}$',
                                         '$\\frac{6}{a}$',
                                         '$\\frac{36}{a}$',
                                         '$\\frac{6}{a^2}$',
                                         '$6a$'],
                             'answer': 2,
                             'exp': '$\\frac{b}{a} = \\frac{6}{a}$입니다.',
                             'exp_en': '$\\frac{6}{a}$.'}]},
             {'title': '🌱 3단계 · [기울기 비교] $\\dfrac{6}{a} = 2$ 식 세우기',
              'title_en': '🌱 Step 3 · [Comparing Slopes] Setting $\\dfrac{6}{a} = 2$',
              'knowledge': '문제에서 한 점근선의 방정식이 $y = 2x$라고 했으므로 기울기 $\\frac{6}{a} = 2$입니다.',
              'knowledge_en': 'Since one asymptote is $y = 2x$, its slope satisfies $\\frac{6}{a} = 2$.',
              'questions': [{'level_label': '방정식 변형 디딤돌 3',
                             'level_label_en': 'Equation Setup Step 3',
                             'stem': '$\\frac{6}{a} = 2$의 양변에 $a$를 곱한 식은?',
                             'stem_en': 'Multiplying both sides of $\\frac{6}{a} = 2$ by $a$ gives which equation?',
                             'options': ['$2a = 6$', '$6a = 2$', '$a = 12$', '$a + 2 = 6$', '$a^2 = 6$'],
                             'answer': 1,
                             'exp': '$2a = 6$입니다.',
                             'exp_en': '$2a = 6$.'}]},
             {'title': '🌳 4단계 · [나눗셈 계산] $2a = 6$에서 $a$ 구하기',
              'title_en': '🌳 Step 4 · [Division] Solving $2a = 6$ for $a$',
              'knowledge': '$6 \\div 2 = 3$입니다.',
              'knowledge_en': '$a = 6 \\div 2 = 3$.',
              'questions': [{'level_label': '나눗셈 디딤돌 4',
                             'level_label_en': 'Division Step 4',
                             'stem': '$2a = 6$을 만족시키는 $a$의 값은?',
                             'stem_en': 'What value of $a$ satisfies $2a = 6$?',
                             'options': ['$1$', '$2$', '$3$', '$4$', '$6$'],
                             'answer': 3,
                             'exp': '$a = 3$입니다.',
                             'exp_en': '$a = 3$.'}]},
             {'title': '💎 5단계 · [최종 종합] 양수 $a$의 값 확정하기',
              'title_en': '💎 Step 5 · [Final Synthesis] Confirming $a = 3$',
              'knowledge': '$a = 3$일 때 점근선은 $y = \\pm \\frac{6}{3}x = \\pm 2x$가 되어 문제 조건을 만족합니다.',
              'knowledge_en': 'When $a = 3$, the asymptotes are $y = \\pm 2x$.',
              'questions': [{'level_label': '최종 종합 디딤돌 5',
                             'level_label_en': 'Final Synthesis Step 5',
                             'stem': '쌍곡선 $\\frac{x^2}{a^2} - \\frac{y^2}{36} = 1$의 한 점근선의 방정식이 $y = 2x$일 때, 양수 $a$의 '
                                     '값은?',
                             'stem_en': 'When one asymptote of $\\frac{x^2}{a^2} - \\frac{y^2}{36} = 1$ is $y = 2x$, '
                                        'what is the positive constant $a$?',
                             'options': ['$1$', '$2$', '$3$', '$4$', '$5$'],
                             'answer': 3,
                             'exp': '$\\frac{6}{a} = 2 \\implies a = 3$이므로 정답은 ③입니다.',
                             'exp_en': '$a = 3$ (choice ③).'}]}],
  'final': {'stem': '쌍곡선 $\\dfrac{x^2}{a^2} - \\dfrac{y^2}{36} = 1$의 한 점근선의 방정식이 $y = 2x$일 때, 양수 $a$의 값은? [3점]',
            'stem_en': 'When one asymptote of the hyperbola $\\dfrac{x^2}{a^2} - \\dfrac{y^2}{36} = 1$ is $y = 2x$, '
                       'what is the positive constant $a$? [3 points]',
            'options': ['$1$', '$2$', '$3$', '$4$', '$5$'],
            'answer': 3,
            'exp': '점근선의 방정식 $y = \\pm \\dfrac{6}{a}x$에서 $\\dfrac{6}{a} = 2$이므로 양수 $a = 3$입니다.',
            'exp_en': 'From the asymptote equation $y = \\pm \\dfrac{6}{a}x$, equating $\\dfrac{6}{a} = 2$ gives $a = '
                      '3$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>쌍곡선의 점근선의 방정식 $y = \\pm \\frac{b}{a}x$</b>를 이용하여 미지수를 구하는 기본 문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  쌍곡선 $\\frac{x^2}{a^2} - \\frac{y^2}{6^2} = 1$ ($a > 0$)의 점근선의 방정식은:<br>\n'
                        '  $$y = \\pm \\frac{6}{a}x$$\n'
                        '  한 점근선의 방정식이 $y = 2x$이므로 $\\frac{6}{a} = 2 \\implies a = 3$입니다.\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 양수 $a$의 값은 $3$이므로 정답은 <b>③번</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem uses the <b>asymptote formula $y = \\pm \\frac{b}{a}x$</b> of a '
                           'hyperbola.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  Since $b = \\sqrt{36} = 6$ and $a > 0$, the positive-slope asymptote is $y = '
                           '\\frac{6}{a}x = 2x \\implies a = 3$.\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  The correct answer is <b>choice ③ ($3$)</b>.\n'
                           '</p>'}},
 {'slug': 'c2610g25',
  'qNum': '기하 25',
  'subject': '기하',
  'title': '[2026학년도 10월 고3 기하 25번] 좌표공간의 대칭이동과 두 점 사이의 거리',
  'title_en': '[2026 AY Oct Exam Grade 12 Geometry #25] Reflections in 3D Coordinate Space and Distance Between Two '
              'Points',
  'summary_ko': '$xy$평면 대칭점 $\\mathrm{B}(1, 2, -k)$에서 $\\overline{\\mathrm{AB}}=2k=4$로 $k=2$를 구하고, $x$축 대칭점 '
                '$\\mathrm{C}(1, -2, -2)$에서 $\\overline{\\mathrm{AC}}=4\\sqrt{2}$ 도출하기',
  'summary_en': 'Reflect $\\mathrm{A}(1, 2, k)$ across the $xy$-plane to $\\mathrm{B}(1, 2, -k)$, use '
                '$\\overline{\\mathrm{AB}}=2k=4$ to get $k=2$, and find $\\overline{\\mathrm{AC}}=4\\sqrt{2}$ where '
                '$\\mathrm{C}(1, -2, -2)$ is the reflection across the $x$-axis.',
  'tags': ['기하', '공간도형과공간좌표', '대칭이동', '두점사이의거리', '25번'],
  'symbols': [{'sym': '$\\mathrm{B}(1, 2, -k)$',
               'desc': '점 $\\mathrm{A}(1, 2, k)$를 $xy$평면에 대하여 대칭이동한 점 ($z$좌표의 부호 반전)',
               'desc_en': 'Reflection of $\\mathrm{A}(1, 2, k)$ across the $xy$-plane negates $z$.'},
              {'sym': '$\\mathrm{C}(1, -2, -k)$',
               'desc': '점 $\\mathrm{A}(1, 2, k)$를 $x$축에 대하여 대칭이동한 점 ($y, z$좌표의 부호 반전)',
               'desc_en': 'Reflection of $\\mathrm{A}(1, 2, k)$ across the $x$-axis negates $y$ and $z$.'}],
  'levels': [{'title': '🔰 1단계 · [초등 거울 대칭 거리] 거울에서 $k$만큼 떨어진 점과 거울 속 점 사이의 거리',
              'title_en': '🔰 Step 1 · [Elementary Mirror Distance] Distance between a point and its mirror image',
              'knowledge': '초등학교 거울 놀이에서 내가 거울($xy$평면) 앞에 $k$만큼 서 있으면 거울 속 내 모습($\\mathrm{B}$)도 거울 뒤로 $k$만큼 떨어져 있어, 나와 '
                           '거울 속 모습 사이의 거리는 $k + k = 2k$입니다!',
              'knowledge_en': 'By elementary mirror symmetry, a point at height $k$ above the $xy$-plane and its '
                              'reflection at $-k$ are separated by $k + k = 2k$.',
              'questions': [{'level_label': '초등 거울 거리 디딤돌 1',
                             'level_label_en': 'Elementary Mirror Step 1',
                             'stem': '초등학교 덧셈·나눗셈 원리로 점 $\\mathrm{A}(1, 2, k)$와 $xy$평면 대칭점 $\\mathrm{B}(1, 2, -k)$ 사이의 '
                                     '거리 $\\overline{\\mathrm{AB}} = 2k = 4$일 때, 양수 $k$의 값은?',
                             'stem_en': 'Using elementary arithmetic, if the distance between $\\mathrm{A}(1, 2, k)$ '
                                        'and its reflection $\\mathrm{B}(1, 2, -k)$ is $\\overline{\\mathrm{AB}} = 2k '
                                        '= 4$, what is $k$?',
                             'options': ['$1$', '$2$', '$3$', '$4$', '$8$'],
                             'answer': 2,
                             'exp': '$2k = 4$이므로 $k = 2$입니다. 즉 $\\mathrm{A}(1, 2, 2)$입니다.',
                             'exp_en': '$2k = 4 \\implies k = 2$, so $\\mathrm{A}(1, 2, 2)$.'}]},
             {'title': '🌿 2단계 · [$x$축 대칭이동] 점 $\\mathrm{A}(1, 2, 2)$를 $x$축에 대칭이동한 점 $\\mathrm{C}$ 구하기',
              'title_en': '🌿 Step 2 · [Reflection Across $x$-Axis] Finding $\\mathrm{C}$ by reflecting $\\mathrm{A}(1, '
                          '2, 2)$ across the $x$-axis',
              'knowledge': '$x$축에 대하여 대칭이동하면 $x$좌표는 그대로 유지되고, 나머지 $y$좌표와 $z$좌표의 부호가 바뀝니다.',
              'knowledge_en': 'Reflecting across the $x$-axis preserves the $x$-coordinate and negates both $y$ and '
                              '$z$.',
              'questions': [{'level_label': 'x축 대칭 좌표 디딤돌 2',
                             'level_label_en': 'x-Axis Reflection Step 2',
                             'stem': '점 $\\mathrm{A}(1, 2, 2)$를 $x$축에 대하여 대칭이동한 점 $\\mathrm{C}$의 좌표는?',
                             'stem_en': 'What are the coordinates of $\\mathrm{C}$, the reflection of $\\mathrm{A}(1, '
                                        '2, 2)$ across the $x$-axis?',
                             'options': ['$(-1, 2, 2)$',
                                         '$(1, -2, 2)$',
                                         '$(1, 2, -2)$',
                                         '$(1, -2, -2)$',
                                         '$(-1, -2, -2)$'],
                             'answer': 4,
                             'exp': '$y, z$좌표의 부호가 바뀌므로 $\\mathrm{C}(1, -2, -2)$입니다.',
                             'exp_en': '$\\mathrm{C}(1, -2, -2)$.'}]},
             {'title': '🌱 3단계 · [좌표 차이 계산] 두 점 $\\mathrm{A}(1, 2, 2)$와 $\\mathrm{C}(1, -2, -2)$의 성분 차 구하기',
              'title_en': '🌱 Step 3 · [Coordinate Differences] Differences between $\\mathrm{A}(1, 2, 2)$ and '
                          '$\\mathrm{C}(1, -2, -2)$',
              'knowledge': '$x$좌표의 차는 $1 - 1 = 0$, $y$좌표의 차는 $2 - (-2) = 4$, $z$좌표의 차는 $2 - (-2) = 4$입니다.',
              'knowledge_en': 'The coordinate differences are $\\Delta x = 0$, $\\Delta y = 4$, and $\\Delta z = 4$.',
              'questions': [{'level_label': '제곱의 합 디딤돌 3',
                             'level_label_en': 'Sum of Squares Step 3',
                             'stem': '$\\overline{\\mathrm{AC}}^2 = 0^2 + 4^2 + 4^2 = 16 + 16$을 계산한 값은?',
                             'stem_en': 'What is $\\overline{\\mathrm{AC}}^2 = 0^2 + 4^2 + 4^2$?',
                             'options': ['$8$', '$16$', '$24$', '$32$', '$64$'],
                             'answer': 4,
                             'exp': '$16 + 16 = 32$입니다.',
                             'exp_en': '$16 + 16 = 32$.'}]},
             {'title': '🌳 4단계 · [근호 간단히 하기] $\\sqrt{32}$를 $a\\sqrt{b}$ 꼴로 나타내기',
              'title_en': '🌳 Step 4 · [Simplifying Radical] Simplifying $\\sqrt{32}$',
              'knowledge': '$32 = 16 \\times 2 = 4^2 \\times 2$이므로 $\\sqrt{32} = 4\\sqrt{2}$입니다.',
              'knowledge_en': 'Since $32 = 16 \\times 2$, $\\sqrt{32} = 4\\sqrt{2}$.',
              'questions': [{'level_label': '제곱근 정리 디딤돌 4',
                             'level_label_en': 'Radical Simplification Step 4',
                             'stem': '$\\sqrt{32} = \\sqrt{16 \\times 2}$를 간단히 한 값은?',
                             'stem_en': 'Simplify $\\sqrt{32} = \\sqrt{16 \\times 2}$.',
                             'options': ['$2\\sqrt{2}$', '$2\\sqrt{6}$', '$4$', '$4\\sqrt{2}$', '$4\\sqrt{3}$'],
                             'answer': 4,
                             'exp': '$\\sqrt{16} = 4$이므로 $4\\sqrt{2}$입니다.',
                             'exp_en': '$4\\sqrt{2}$.'}]},
             {'title': '💎 5단계 · [최종 종합] 선분 $\\overline{\\mathrm{AC}}$의 길이 확정하기',
              'title_en': '💎 Step 5 · [Final Synthesis] Final length of $\\overline{\\mathrm{AC}}$',
              'knowledge': '선분 $\\mathrm{AC}$의 길이는 $4\\sqrt{2}$입니다.',
              'knowledge_en': '$\\overline{\\mathrm{AC}} = 4\\sqrt{2}$.',
              'questions': [{'level_label': '최종 종합 디딤돌 5',
                             'level_label_en': 'Final Synthesis Step 5',
                             'stem': '구하는 선분 $\\mathrm{AC}$의 길이는?',
                             'stem_en': 'What is the length of segment $\\mathrm{AC}$?',
                             'options': ['$2\\sqrt{2}$', '$2\\sqrt{6}$', '$4$', '$4\\sqrt{2}$', '$4\\sqrt{3}$'],
                             'answer': 4,
                             'exp': '$\\overline{\\mathrm{AC}} = 4\\sqrt{2}$이므로 정답은 ④입니다.',
                             'exp_en': '$4\\sqrt{2}$ (choice ④).'}]}],
  'final': {'stem': '좌표공간의 점 $\\mathrm{A}(1, 2, k)$ ($k > 0$)를 $xy$평면에 대하여 대칭이동한 점을 $\\mathrm{B}$라 하고, 점 '
                    '$\\mathrm{A}$를 $x$축에 대하여 대칭이동한 점을 $\\mathrm{C}$라 하자. $\\overline{\\mathrm{AB}} = 4$일 때, 선분 '
                    '$\\mathrm{AC}$의 길이는? [3점]',
            'stem_en': 'In 3D coordinate space, let $\\mathrm{B}$ be the reflection of $\\mathrm{A}(1, 2, k)$ ($k > '
                       '0$) across the $xy$-plane, and let $\\mathrm{C}$ be the reflection of $\\mathrm{A}$ across the '
                       '$x$-axis. If $\\overline{\\mathrm{AB}} = 4$, what is the length of segment $\\mathrm{AC}$? [3 '
                       'points]',
            'options': ['$2\\sqrt{2}$', '$2\\sqrt{6}$', '$4$', '$4\\sqrt{2}$', '$4\\sqrt{3}$'],
            'answer': 4,
            'exp': '$\\mathrm{B}(1, 2, -k)$에서 $\\overline{\\mathrm{AB}} = 2k = 4 \\implies k = 2$이므로 $\\mathrm{A}(1, '
                   '2, 2)$, $\\mathrm{C}(1, -2, -2)$이고 $\\overline{\\mathrm{AC}} = \\sqrt{0 + 16 + 16} = '
                   '4\\sqrt{2}$입니다.',
            'exp_en': 'From $\\mathrm{B}(1, 2, -k)$ and $\\overline{\\mathrm{AB}} = 2k = 4$, we get $k = 2$. Then '
                      '$\\mathrm{A}(1, 2, 2)$ and $\\mathrm{C}(1, -2, -2)$ give $\\overline{\\mathrm{AC}} = \\sqrt{4^2 '
                      '+ 4^2} = 4\\sqrt{2}$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>좌표공간에서의 점의 대칭이동($xy$평면, $x$축)</b>과 두 점 사이의 거리 공식을 평가하는 문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 점 $\\mathrm{B}$의 좌표와 $k$ 구하기</b><br>\n'
                        '  점 $\\mathrm{A}(1, 2, k)$를 $xy$평면에 대칭이동한 점은 $\\mathrm{B}(1, 2, -k)$입니다.<br>\n'
                        '  $$\\overline{\\mathrm{AB}} = 2k = 4 \\implies k = 2 \\implies \\mathrm{A}(1, 2, 2)$$<br>\n'
                        '  <b>2단계: 점 $\\mathrm{C}$의 좌표와 $\\overline{\\mathrm{AC}}$ 구하기</b><br>\n'
                        '  점 $\\mathrm{A}(1, 2, 2)$를 $x$축에 대칭이동한 점은 $\\mathrm{C}(1, -2, -2)$이므로:<br>\n'
                        '  $$\\overline{\\mathrm{AC}} = \\sqrt{(1-1)^2 + \\{2-(-2)\\}^2 + \\{2-(-2)\\}^2} = \\sqrt{0 + '
                        '16 + 16} = 4\\sqrt{2}$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 선분 $\\mathrm{AC}$의 길이는 $4\\sqrt{2}$이므로 정답은 <b>④번</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem uses <b>3D coordinate reflections</b> and the distance formula.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Find $k$</b><br>\n'
                           '  Reflecting $\\mathrm{A}(1, 2, k)$ across the $xy$-plane gives $\\mathrm{B}(1, 2, -k)$, '
                           'so $\\overline{\\mathrm{AB}} = 2k = 4 \\implies k = 2$.<br><br>\n'
                           '  <b>Step 2: Find $\\overline{\\mathrm{AC}}$</b><br>\n'
                           '  Reflecting $\\mathrm{A}(1, 2, 2)$ across the $x$-axis gives $\\mathrm{C}(1, -2, -2)$, so '
                           '$\\overline{\\mathrm{AC}} = \\sqrt{0^2 + 4^2 + 4^2} = 4\\sqrt{2}$.\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  The correct answer is <b>choice ④ ($4\\sqrt{2}$)</b>.\n'
                           '</p>'}},
 {'slug': 'c2610g26',
  'qNum': '기하 26',
  'subject': '기하',
  'title': '[2026학년도 10월 고3 기하 26번] 포물선의 접선의 방정식과 준선까지의 거리',
  'title_en': '[2026 AY Oct Exam Grade 12 Geometry #26] Tangent Line to a Parabola and Distance to Directrix',
  'summary_ko': '포물선 $y^2=4px$의 기울기 $2$인 접선 $y=2x+\\dfrac{p}{2}$와 $y=2x+1$을 비교해 $p=2$, 접점 '
                '$\\mathrm{P}\\!\\left(\\dfrac{1}{2}, 2\\right)$를 구하고 준선 $x=-2$까지의 거리 $\\dfrac{5}{2}$ 도출하기',
  'summary_en': 'Compare $y=2x+\\dfrac{p}{2}$ with $y=2x+1$ to find $p=2$ and tangency point '
                '$\\mathrm{P}\\!\\left(\\dfrac{1}{2}, 2\\right)$, then compute the distance to the directrix $x=-2$ as '
                '$\\dfrac{5}{2}$.',
  'tags': ['기하', '이차곡선', '포물선', '포물선의접선', '포물선의정의', '26번'],
  'symbols': [{'sym': '$y = mx + \\dfrac{p}{m}$',
               'desc': '포물선 $y^2 = 4px$에 접하고 기울기가 $m$인 직선의 방정식',
               'desc_en': 'Tangent line of slope $m$ to the parabola $y^2 = 4px$.'},
              {'sym': '$x = -p = -2$',
               'desc': '초점이 $\\mathrm{F}(p, 0)$인 포물선의 준선의 방정식',
               'desc_en': 'Directrix $x = -p$ of the parabola.'}],
  'levels': [{'title': '🔰 1단계 · [초등 나눗셈] $\\dfrac{p}{2} = 1$을 만족하는 수 $p$ 구하기',
              'title_en': '🔰 Step 1 · [Elementary Division] Solving $\\dfrac{p}{2} = 1$ for $p$',
              'knowledge': '포물선 $y^2 = 4px$에 접하고 기울기가 $m = 2$인 직선의 방정식은 $y = 2x + \\frac{p}{2}$입니다. 이 직선이 $y = 2x + '
                           '1$과 같으려면 초등학교 나눗셈에서 $\\frac{p}{2} = 1$이어야 합니다!',
              'knowledge_en': 'The tangent of slope $m = 2$ to $y^2 = 4px$ is $y = 2x + \\frac{p}{2}$. Comparing with '
                              '$y = 2x + 1$ gives $\\frac{p}{2} = 1$.',
              'questions': [{'level_label': '초등 나눗셈 디딤돌 1',
                             'level_label_en': 'Elementary Division Step 1',
                             'stem': '초등학교 나눗셈·곱셈 원리로 $\\frac{p}{2} = 1$을 만족시키는 양수 $p$의 값을 구하면?',
                             'stem_en': 'Using elementary arithmetic, what value of $p$ satisfies $\\frac{p}{2} = 1$?',
                             'options': ['$1$', '$2$', '$3$', '$4$', '$6$'],
                             'answer': 2,
                             'exp': '$p = 2 \\times 1 = 2$입니다.',
                             'exp_en': '$p = 2$.'}]},
             {'title': '🌿 2단계 · [접점 $\\mathrm{P}$ 구하기] $y^2 = 8x$와 $y = 2x + 1$이 접하는 점 찾기',
              'title_en': '🌿 Step 2 · [Point of Tangency $\\mathrm{P}$] Finding where $y^2 = 8x$ and $y = 2x + 1$ '
                          'touch',
              'knowledge': '$p = 2$이므로 포물선은 $y^2 = 8x$입니다. $4x = 2y - 2$를 대입하면 $y^2 = 4y - 4 \\implies (y - 2)^2 = '
                           '0$이므로 $y = 2$, $x = \\frac{1}{2}$입니다.',
              'knowledge_en': 'Substituting $8x = 4y - 4$ into $y^2 = 8x$ gives $(y - 2)^2 = 0$, so $y = 2$ and $x = '
                              '\\frac{1}{2}$.',
              'questions': [{'level_label': '접점 x좌표 디딤돌 2',
                             'level_label_en': 'Tangency x-Coordinate Step 2',
                             'stem': '접점 $\\mathrm{P}$의 $y$좌표가 $2$이고 직선 $y = 2x + 1$ 위의 점일 때, 점 $\\mathrm{P}$의 $x$좌표는?',
                             'stem_en': 'When $y = 2$ on the line $y = 2x + 1$, what is the $x$-coordinate of '
                                        '$\\mathrm{P}$?',
                             'options': ['$\\frac{1}{4}$', '$\\frac{1}{2}$', '$1$', '$\\frac{3}{2}$', '$2$'],
                             'answer': 2,
                             'exp': '$2 = 2x + 1 \\implies 2x = 1 \\implies x = \\frac{1}{2}$입니다.',
                             'exp_en': '$x = \\frac{1}{2}$.'}]},
             {'title': '🌱 3단계 · [준선의 방정식] $y^2 = 4px$ ($p = 2$)의 준선 찾기',
              'title_en': '🌱 Step 3 · [Directrix] Finding the directrix of $y^2 = 8x$',
              'knowledge': '$y^2 = 4px$에서 초점은 $\\mathrm{F}(p, 0) = (2, 0)$이고, 준선의 방정식은 $x = -p = -2$입니다.',
              'knowledge_en': 'For $y^2 = 4px$ with $p = 2$, the focus is $(2, 0)$ and the directrix is $x = -2$.',
              'questions': [{'level_label': '준선의 방정식 디딤돌 3',
                             'level_label_en': 'Directrix Equation Step 3',
                             'stem': '$p = 2$일 때 포물선 $y^2 = 8x$의 준선의 방정식은?',
                             'stem_en': 'What is the equation of the directrix of $y^2 = 8x$?',
                             'options': ['$x = -4$', '$x = -2$', '$x = -1$', '$x = 2$', '$y = -2$'],
                             'answer': 2,
                             'exp': '준선은 $x = -p = -2$입니다.',
                             'exp_en': '$x = -2$.'}]},
             {'title': '🌳 4단계 · [거리 식 세우기] $x = \\dfrac{1}{2}$과 $x = -2$ 사이의 가로 거리',
              'title_en': '🌳 Step 4 · [Horizontal Distance] Distance between $x = \\dfrac{1}{2}$ and $x = -2$',
              'knowledge': '점 $\\mathrm{P}\\left(\\frac{1}{2}, 2\\right)$와 직선 $x = -2$ 사이의 거리는 오른쪽 $x$좌표에서 왼쪽 $x$좌표를 뺀 '
                           '$\\frac{1}{2} - (-2) = \\frac{1}{2} + 2$입니다. (포물선의 정의에 의해 초점 $\\mathrm{F}(2, 0)$까지의 거리 '
                           '$\\overline{\\mathrm{PF}}$와도 똑같습니다!)',
              'knowledge_en': 'The distance from $\\mathrm{P}\\left(\\frac{1}{2}, 2\\right)$ to $x = -2$ is '
                              '$\\frac{1}{2} - (-2) = \\frac{1}{2} + 2$.',
              'questions': [{'level_label': '분수 덧셈 디딤돌 4',
                             'level_label_en': 'Fraction Addition Step 4',
                             'stem': '$\\frac{1}{2} + 2$를 가분수로 계산한 값은?',
                             'stem_en': 'What is $\\frac{1}{2} + 2$ as an improper fraction?',
                             'options': ['$\\frac{3}{2}$', '$2$', '$\\frac{5}{2}$', '$3$', '$\\frac{7}{2}$'],
                             'answer': 3,
                             'exp': '$\\frac{1}{2} + \\frac{4}{2} = \\frac{5}{2}$입니다.',
                             'exp_en': '$\\frac{5}{2}$.'}]},
             {'title': '💎 5단계 · [최종 종합] 점 $\\mathrm{P}$와 준선 사이의 거리 확정하기',
              'title_en': '💎 Step 5 · [Final Synthesis] Final distance from $\\mathrm{P}$ to the directrix',
              'knowledge': '구하는 거리는 $\\frac{5}{2}$입니다.',
              'knowledge_en': 'The distance is $\\frac{5}{2}$.',
              'questions': [{'level_label': '최종 종합 디딤돌 5',
                             'level_label_en': 'Final Synthesis Step 5',
                             'stem': '점 $\\mathrm{P}$와 포물선의 준선 사이의 거리는?',
                             'stem_en': 'What is the distance between point $\\mathrm{P}$ and the directrix of the '
                                        'parabola?',
                             'options': ['$\\frac{5}{2}$', '$3$', '$\\frac{7}{2}$', '$4$', '$\\frac{9}{2}$'],
                             'answer': 1,
                             'exp': '$\\frac{1}{2} - (-2) = \\frac{5}{2}$이므로 정답은 ①입니다.',
                             'exp_en': '$\\frac{5}{2}$ (choice ①).'}]}],
  'final': {'stem': '포물선 $y^2 = 4px$ ($p > 0$)에 접하는 직선 $y = 2x + 1$이 포물선과 만나는 점을 $\\mathrm{P}$라 할 때, 점 $\\mathrm{P}$와 '
                    '포물선의 준선 사이의 거리는? [3점]',
            'stem_en': 'The line $y = 2x + 1$ is tangent to the parabola $y^2 = 4px$ ($p > 0$) at point $\\mathrm{P}$. '
                       'What is the distance between $\\mathrm{P}$ and the directrix of the parabola? [3 points]',
            'options': ['$\\dfrac{5}{2}$', '$3$', '$\\dfrac{7}{2}$', '$4$', '$\\dfrac{9}{2}$'],
            'answer': 1,
            'exp': '접선 공식 $y = 2x + \\dfrac{p}{2}$에서 $\\dfrac{p}{2} = 1 \\implies p = 2$이고 접점은 '
                   '$\\mathrm{P}\\left(\\dfrac{1}{2}, 2\\right)$입니다. 준선 $x = -2$까지의 거리는 $\\dfrac{1}{2} - (-2) = '
                   '\\dfrac{5}{2}$입니다.',
            'exp_en': 'From $y = 2x + \\dfrac{p}{2} = 2x + 1$, we get $p = 2$ and $\\mathrm{P}\\left(\\dfrac{1}{2}, '
                      '2\\right)$. The distance to the directrix $x = -2$ is $\\dfrac{1}{2} - (-2) = \\dfrac{5}{2}$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>기울기가 주어진 포물선의 접선의 방정식 $y = mx + \\frac{p}{m}$</b>과 포물선의 준선의 정의를 평가하는 문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 접선 공식으로 $p$ 구하기</b><br>\n'
                        '  포물선 $y^2 = 4px$에 접하고 기울기가 $2$인 직선의 방정식은 $y = 2x + \\frac{p}{2}$입니다.<br>\n'
                        '  이 직선이 $y = 2x + 1$이므로 $\\frac{p}{2} = 1 \\implies p = 2$입니다.<br><br>\n'
                        '  <b>2단계: 접점 $\\mathrm{P}$와 준선 사이의 거리 구하기</b><br>\n'
                        '  $y^2 = 8x$와 $y = 2x + 1$을 연립하면 $(y - 2)^2 = 0 \\implies y = 2, x = \\frac{1}{2}$이므로 '
                        '$\\mathrm{P}\\left(\\frac{1}{2}, 2\\right)$입니다.<br>\n'
                        '  준선의 방정식은 $x = -p = -2$이므로 점 $\\mathrm{P}$와 준선 사이의 거리는:<br>\n'
                        '  $$\\frac{1}{2} - (-2) = \\frac{5}{2}$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 구하는 거리는 $\\dfrac{5}{2}$이므로 정답은 <b>①번</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem uses the <b>tangent line formula $y = mx + \\frac{p}{m}$</b> for a '
                           'parabola and the equation of its directrix.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Find $p$ and point $\\mathrm{P}$</b><br>\n'
                           '  Equating $y = 2x + \\frac{p}{2}$ with $y = 2x + 1$ gives $p = 2$. Solving $y^2 = 8x$ '
                           'with $y = 2x + 1$ gives $\\mathrm{P}\\left(\\frac{1}{2}, 2\\right)$.<br><br>\n'
                           '  <b>Step 2: Distance to directrix $x = -2$</b><br>\n'
                           '  $$\\text{Distance} = \\frac{1}{2} - (-2) = \\frac{5}{2}$$\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  The correct answer is <b>choice ① ($\\dfrac{5}{2}$)</b>.\n'
                           '</p>'}},
 {'slug': 'c2610g27',
  'qNum': '기하 27',
  'subject': '기하',
  'title': '[2026학년도 10월 고3 기하 27번] 원기둥의 밑면 원주각과 삼수선의 정리',
  'title_en': '[2026 AY Oct Exam Grade 12 Geometry #27] Cylinder Base Inscribed Angle and Theorem of Three '
              'Perpendiculars',
  'summary_ko': "밑면 $C_2$의 지름 $\\overline{\\mathrm{A'C}}=8$에서 호 $\\mathrm{A'D}=\\dfrac{4}{3}\\pi$에 대한 중심각·원주각으로 "
                "$\\mathrm{D}$에서 $\\mathrm{A'C}$까지의 거리 $2\\sqrt{3}$을 구하고 삼수선의 정리로 높이 $2\\sqrt{6}$ 도출하기",
  'summary_en': "Use diameter $\\overline{\\mathrm{A'C}}=8$ and arc length $\\dfrac{4}{3}\\pi$ on base $C_2$ to find "
                "the perpendicular distance $2\\sqrt{3}$ from $\\mathrm{D}$ to $\\mathrm{A'C}$, then apply the Theorem "
                'of Three Perpendiculars to find cylinder height $2\\sqrt{6}$.',
  'tags': ['기하', '공간도형과공간좌표', '삼수선의정리', '원기둥', '부채꼴의호의길이', '27번'],
  'symbols': [{'sym': "$\\overline{A'C} = 2r = 8$",
               'desc': '밑면 원 $C_2$의 중심을 지나는 지름의 길이',
               'desc_en': 'Diameter of the circular base $C_2$ with radius $4$.'},
              {'sym': '$l = r\\theta \\implies 4\\theta = \\dfrac{4}{3}\\pi \\implies \\theta = \\dfrac{\\pi}{3}$',
               'desc': "중심각을 이용하여 밑면 직각삼각형 $\\mathrm{A'CD}$의 내각 결정",
               'desc_en': 'Central angle formula $l = r\\theta$ on the base circle.'},
              {'sym': "$\\overline{DH}^2 + \\overline{AA'}^2 = \\overline{DM}^2$",
               'desc': '삼수선의 정리에 의한 공간 삼각형 ABD의 높이 제곱',
               'desc_en': 'Pythagorean relation from the Theorem of Three Perpendiculars.'}],
  'levels': [{'title': '🔰 1단계 · [초등 삼각형의 넓이] 밑변이 $8$이고 넓이가 $24$인 삼각형의 높이 구하기',
              'title_en': '🔰 Step 1 · [Elementary Triangle Area] Finding the altitude of a triangle with base $8$ and '
                          'area $24$',
              'knowledge': '삼각형 $\\mathrm{ABD}$에서 밑변 $\\overline{\\mathrm{AB}}$는 반지름이 $4$인 원의 지름이므로 $2 \\times 4 = '
                           '8$입니다! 초등학교 삼각형의 넓이 공식 $\\frac{1}{2} \\times (\\text{밑변}) \\times (\\text{높이}) = 24$로 삼각형 '
                           '$\\mathrm{ABD}$의 높이를 먼저 구해 봅시다.',
              'knowledge_en': 'By elementary geometry, the diameter is $\\overline{\\mathrm{AB}} = 2 \\times 4 = 8$. '
                              'Using $\\text{Area} = \\frac{1}{2} \\times \\text{base} \\times \\text{height} = 24$, '
                              'we can immediately find the altitude of $\\triangle\\mathrm{ABD}$.',
              'questions': [{'level_label': '초등 삼각형 넓이 디딤돌 1',
                             'level_label_en': 'Elementary Triangle Area Step 1',
                             'stem': '초등학교 삼각형의 넓이 공식 $\\frac{1}{2} \\times 8 \\times H = 24$에서 점 $\\mathrm{D}$로부터 직선 '
                                     '$\\mathrm{AB}$까지의 거리(높이 $H$)는?',
                             'stem_en': 'Using the elementary triangle area formula $\\frac{1}{2} \\times 8 \\times H '
                                        '= 24$, what is the altitude $H$ from $\\mathrm{D}$ to $\\mathrm{AB}$?',
                             'options': ['$3$', '$4$', '$6$', '$8$', '$12$'],
                             'answer': 3,
                             'exp': '$4H = 24$이므로 삼각형 $\\mathrm{ABD}$의 높이 $H = 6$입니다!',
                             'exp_en': '$4H = 24 \\implies H = 6$.'}]},
             {'title': "🌿 2단계 · [밑면 중심각과 원주각] 호의 길이 $\\dfrac{4}{3}\\pi$로 직각삼각형 $\\mathrm{A'CD}$ 분석하기",
              'title_en': "🌿 Step 2 · [Base Circle Angles] Analyzing right triangle $\\mathrm{A'CD}$ from arc length "
                          '$\\dfrac{4}{3}\\pi$',
              'knowledge': "점 $\\mathrm{A}, \\mathrm{B}$에서 밑면 $C_2$에 내린 수선의 발을 $\\mathrm{A'}, \\mathrm{C}$라 하면 "
                           "$\\overline{\\mathrm{A'C}} = 8$은 지름입니다. 짧은 호 $\\mathrm{A'D}$(또는 $\\mathrm{CD}$)의 중심각에서 "
                           "직각삼각형 $\\mathrm{A'CD}$의 한 예각은 $\\frac{\\pi}{6}$ ($30^\\circ$)가 되어 "
                           "$\\overline{\\mathrm{A'D}} = 4$, $\\overline{\\mathrm{CD}} = 4\\sqrt{3}$입니다.",
              'knowledge_en': 'Projecting $\\mathrm{A}, \\mathrm{B}$ onto $C_2$ gives diameter '
                              "$\\overline{\\mathrm{A'C}} = 8$. In right triangle $\\mathrm{A'CD}$, the legs are $4$ "
                              'and $4\\sqrt{3}$.',
              'questions': [{'level_label': '밑면 수선의 길이 디딤돌 2',
                             'level_label_en': 'Base Altitude Step 2',
                             'stem': "빗변이 $\\overline{\\mathrm{A'C}} = 8$이고 두 직각변이 $4, 4\\sqrt{3}$인 직각삼각형 "
                                     "$\\mathrm{A'CD}$에서, 꼭짓점 $\\mathrm{D}$에서 지름 $\\mathrm{A'C}$에 내린 수선의 발 "
                                     '$\\mathrm{M}$까지의 길이 $\\overline{\\mathrm{DM}} = \\frac{4 \\times '
                                     '4\\sqrt{3}}{8}$은?',
                             'stem_en': "In right triangle $\\mathrm{A'CD}$ with hypotenuse $8$ and legs $4, "
                                        '4\\sqrt{3}$, what is the altitude $\\overline{\\mathrm{DM}} = \\frac{4 '
                                        "\\times 4\\sqrt{3}}{8}$ to the diameter $\\mathrm{A'C}$?",
                             'options': ['$\\sqrt{3}$', '$2\\sqrt{2}$', '$2\\sqrt{3}$', '$3\\sqrt{3}$', '$4\\sqrt{3}$'],
                             'answer': 3,
                             'exp': '$\\frac{16\\sqrt{3}}{8} = 2\\sqrt{3}$입니다.',
                             'exp_en': '$\\overline{\\mathrm{DM}} = 2\\sqrt{3}$.'}]},
             {'title': '🌱 3단계 · [삼수선의 정리] 원기둥의 높이 $h$와 $H = 6$, $\\overline{\\mathrm{DM}} = 2\\sqrt{3}$ 연결하기',
              'title_en': '🌱 Step 3 · [Three Perpendiculars] Relating cylinder height $h$ with $H = 6$ and '
                          '$\\overline{\\mathrm{DM}} = 2\\sqrt{3}$',
              'knowledge': '삼수선의 정리에 의해 삼각형 $\\mathrm{ABD}$의 높이 $H = 6$은 밑면에서의 수선 $\\overline{\\mathrm{DM}} = '
                           '2\\sqrt{3}$과 원기둥의 높이 $h$를 두 직각변으로 하는 직각삼각형의 빗변입니다! 즉 $(2\\sqrt{3})^2 + h^2 = 6^2$입니다.',
              'knowledge_en': 'By the Theorem of Three Perpendiculars, $\\overline{\\mathrm{DM}}^2 + h^2 = H^2$, so '
                              '$(2\\sqrt{3})^2 + h^2 = 6^2$.',
              'questions': [{'level_label': '피타고라스 정리 디딤돌 3',
                             'level_label_en': 'Pythagorean Theorem Step 3',
                             'stem': '$12 + h^2 = 36$에서 원기둥의 높이의 제곱 $h^2$의 값은?',
                             'stem_en': 'From $12 + h^2 = 36$, what is $h^2$?',
                             'options': ['$16$', '$20$', '$24$', '$28$', '$32$'],
                             'answer': 3,
                             'exp': '$h^2 = 36 - 12 = 24$입니다.',
                             'exp_en': '$h^2 = 36 - 12 = 24$.'}]},
             {'title': '🌳 4단계 · [제곱근 정리] $\\sqrt{24}$ 간단히 하기',
              'title_en': '🌳 Step 4 · [Simplifying Radical] Simplifying $\\sqrt{24}$',
              'knowledge': '$24 = 4 \\times 6 = 2^2 \\times 6$이므로 $h = \\sqrt{24} = 2\\sqrt{6}$입니다.',
              'knowledge_en': 'Since $24 = 4 \\times 6$, $h = \\sqrt{24} = 2\\sqrt{6}$.',
              'questions': [{'level_label': '제곱근 계산 디딤돌 4',
                             'level_label_en': 'Radical Step 4',
                             'stem': '$h^2 = 24$ ($h > 0$)일 때 $h = \\sqrt{24}$를 간단히 한 값은?',
                             'stem_en': 'Simplify $h = \\sqrt{24}$.',
                             'options': ['$2\\sqrt{3}$',
                                         '$2\\sqrt{6}$',
                                         '$3\\sqrt{2}$',
                                         '$4\\sqrt{3}$',
                                         '$4\\sqrt{6}$'],
                             'answer': 2,
                             'exp': '$\\sqrt{4 \\times 6} = 2\\sqrt{6}$입니다.',
                             'exp_en': '$2\\sqrt{6}$.'}]},
             {'title': '💎 5단계 · [최종 종합] 원기둥의 높이 확정하기',
              'title_en': '💎 Step 5 · [Final Synthesis] Final height of the cylinder',
              'knowledge': '구하는 원기둥의 높이는 $2\\sqrt{6}$입니다.',
              'knowledge_en': 'The height of the cylinder is $2\\sqrt{6}$.',
              'questions': [{'level_label': '최종 종합 디딤돌 5',
                             'level_label_en': 'Final Synthesis Step 5',
                             'stem': '이 원기둥의 높이는?',
                             'stem_en': 'What is the height of this cylinder?',
                             'options': ['$2\\sqrt{3}$', '$2\\sqrt{6}$', '$6$', '$4\\sqrt{3}$', '$6\\sqrt{2}$'],
                             'answer': 2,
                             'exp': '$h = 2\\sqrt{6}$이므로 정답은 ②입니다.',
                             'exp_en': '$2\\sqrt{6}$ (choice ②).'}]}],
  'final': {'stem': '밑면의 반지름의 길이가 $4$인 원기둥이 있다. 이 원기둥의 한 밑면의 둘레를 이루는 원을 $C_1$, 다른 밑면의 둘레를 이루는 원을 $C_2$라 하자. 원 $C_1$의 '
                    '중심을 지나는 직선이 원 $C_1$과 만나는 두 점을 $\\mathrm{A}, \\mathrm{B}$라 하고, 점 $\\mathrm{B}$를 지나고 원기둥의 밑면에 수직인 '
                    '직선이 원 $C_2$와 만나는 점을 $\\mathrm{C}$라 하자. 원 $C_2$ 위의 점 $\\mathrm{D}$에 대하여 호 $\\mathrm{CD}$의 길이가 '
                    '$\\dfrac{4}{3}\\pi$이고 삼각형 $\\mathrm{ABD}$의 넓이가 $24$일 때, 이 원기둥의 높이는? [3점]',
            'stem_en': 'A cylinder has base circles $C_1$ and $C_2$ of radius $4$. Points $\\mathrm{A}, \\mathrm{B}$ '
                       'form a diameter of $C_1$, and the line through $\\mathrm{B}$ perpendicular to the bases meets '
                       '$C_2$ at $\\mathrm{C}$. For a point $\\mathrm{D}$ on $C_2$, the arc $\\mathrm{CD}$ has length '
                       '$\\dfrac{4}{3}\\pi$ and $\\text{Area}(\\triangle\\mathrm{ABD}) = 24$. What is the height of '
                       'the cylinder? [3 points]',
            'options': ['$2\\sqrt{3}$', '$2\\sqrt{6}$', '$6$', '$4\\sqrt{3}$', '$6\\sqrt{2}$'],
            'answer': 2,
            'exp': "점 $\\mathrm{A}$의 $C_2$ 위 정사영을 $\\mathrm{A'}$이라 하면 $\\overline{\\mathrm{A'C}} = 8$이고 점 "
                   "$\\mathrm{D}$에서 $\\mathrm{A'C}$에 내린 수선의 길이는 $2\\sqrt{3}$입니다. 삼각형 $\\mathrm{ABD}$의 높이가 "
                   '$\\dfrac{2\\times 24}{8} = 6$이므로 원기둥의 높이는 $\\sqrt{6^2 - (2\\sqrt{3})^2} = 2\\sqrt{6}$입니다.',
            'exp_en': "Projecting $\\mathrm{A}$ to $\\mathrm{A'}$ on $C_2$ gives diameter $\\overline{\\mathrm{A'C}} = "
                      "8$, and the altitude from $\\mathrm{D}$ to $\\mathrm{A'C}$ is $2\\sqrt{3}$. Since the altitude "
                      'of $\\triangle\\mathrm{ABD}$ to $\\mathrm{AB}$ is $6$, the cylinder height is $\\sqrt{6^2 - '
                      '(2\\sqrt{3})^2} = 2\\sqrt{6}$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>원기둥의 밑면에서의 호의 길이($l = r\\theta$)와 삼수선의 정리</b>를 결합하여 원기둥의 높이를 구하는 공간도형 문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 삼각형 $\\mathrm{ABD}$의 높이 구하기</b><br>\n'
                        '  원 $C_1$의 반지름이 $4$이므로 지름 $\\overline{\\mathrm{AB}} = 8$입니다.<br>\n'
                        '  점 $\\mathrm{D}$에서 직선 $\\mathrm{AB}$에 내린 수선의 발을 $\\mathrm{H}$라 하면:<br>\n'
                        '  $$\\text{Area}(\\triangle\\mathrm{ABD}) = \\frac{1}{2} \\times 8 \\times '
                        '\\overline{\\mathrm{DH}} = 24 \\implies \\overline{\\mathrm{DH}} = 6$$<br>\n'
                        "  <b>2단계: 밑면 원 $C_2$에서 점 $\\mathrm{D}$와 지름 $\\mathrm{A'C}$ 사이의 거리 구하기</b><br>\n"
                        "  점 $\\mathrm{A}$에서 밑면 $C_2$에 내린 수선의 발을 $\\mathrm{A'}$이라 하면 $\\overline{\\mathrm{A'C}} = 8$은 "
                        '원 $C_2$의 지름입니다.<br>\n'
                        '  호 $\\mathrm{CD}$의 길이가 $4\\theta = \\frac{4}{3}\\pi$이므로 중심각은 $\\frac{\\pi}{3}$ '
                        "($60^\\circ$)이고, 원주각 $\\angle\\mathrm{CA'D} = \\frac{\\pi}{6}$ ($30^\\circ$)입니다.<br>\n"
                        "  따라서 직각삼각형 $\\mathrm{A'CD}$에서 $\\overline{\\mathrm{CD}} = 4$, $\\overline{\\mathrm{A'D}} = "
                        "4\\sqrt{3}$이고, 점 $\\mathrm{D}$에서 지름 $\\mathrm{A'C}$에 내린 수선의 발 $\\mathrm{M}$까지의 거리는:<br>\n"
                        '  $$\\overline{\\mathrm{DM}} = 4\\sin\\frac{\\pi}{3} = 2\\sqrt{3}$$<br>\n'
                        '  <b>3단계: 삼수선의 정리로 원기둥의 높이 $h$ 구하기</b><br>\n'
                        '  삼수선의 정리에 의하여 $\\overline{\\mathrm{HM}} = h$는 밑면에 수직이므로:<br>\n'
                        '  $$h = \\sqrt{\\overline{\\mathrm{DH}}^2 - \\overline{\\mathrm{DM}}^2} = \\sqrt{6^2 - '
                        '(2\\sqrt{3})^2} = \\sqrt{36 - 12} = \\sqrt{24} = 2\\sqrt{6}$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 원기둥의 높이는 $2\\sqrt{6}$이므로 정답은 <b>②번</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem applies the <b>Theorem of Three Perpendiculars</b> to a cylinder with '
                           'circular base radius $4$.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Altitude of $\\triangle\\mathrm{ABD}$</b><br>\n'
                           '  Since $\\overline{\\mathrm{AB}} = 8$ and $\\text{Area}(\\triangle\\mathrm{ABD}) = 24$, '
                           'the altitude from $\\mathrm{D}$ to $\\mathrm{AB}$ is $\\overline{\\mathrm{DH}} = '
                           '6$.<br><br>\n'
                           '  <b>Step 2: Base projection and Three Perpendiculars</b><br>\n'
                           '  On circle $C_2$, arc $\\mathrm{CD} = \\frac{4}{3}\\pi$ gives central angle '
                           '$\\frac{\\pi}{3}$, so the perpendicular distance from $\\mathrm{D}$ to diameter '
                           "$\\mathrm{A'C}$ is $\\overline{\\mathrm{DM}} = 4\\sin\\frac{\\pi}{3} = 2\\sqrt{3}$.<br>\n"
                           '  By the Theorem of Three Perpendiculars, $h = \\sqrt{6^2 - (2\\sqrt{3})^2} = \\sqrt{24} = '
                           '2\\sqrt{6}$.\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  The correct answer is <b>choice ② ($2\\sqrt{6}$)</b>.\n'
                           '</p>'}},
 {'slug': 'c2610g28',
  'qNum': '기하 28',
  'subject': '기하',
  'title': '[2026학년도 10월 고3 기하 28번] 타원의 정의와 두 이등변삼각형의 닮음',
  'title_en': '[2026 AY Oct Exam Grade 12 Geometry #28] Definition of an Ellipse and Two Similar Isosceles Triangles',
  'summary_ko': "타원의 정의 $\\overline{\\mathrm{F'P}}+\\overline{\\mathrm{PF}}=2a=\\overline{\\mathrm{F'Q}}$에서 "
                '$\\overline{\\mathrm{PF}}=\\overline{\\mathrm{PQ}}$와 '
                "$\\overline{\\mathrm{F'F}}=\\overline{\\mathrm{FQ}}=2c$를 찾고, 기울기 $\\dfrac{\\sqrt{7}}{3}$과 넓이 "
                '$6\\sqrt{7}$로부터 $c=3\\sqrt{2}$, 둘레 $8c=24\\sqrt{2}$ 도출하기',
  'summary_en': "Use $\\overline{\\mathrm{F'P}}+\\overline{\\mathrm{PF}}=2a=\\overline{\\mathrm{F'Q}}$ to deduce "
                '$\\overline{\\mathrm{PF}}=\\overline{\\mathrm{PQ}}$ and '
                "$\\overline{\\mathrm{F'F}}=\\overline{\\mathrm{FQ}}=2c$, find $c=3\\sqrt{2}$ from slope "
                '$\\dfrac{\\sqrt{7}}{3}$ and area $6\\sqrt{7}$, and compute '
                "$\\text{Perimeter}(\\triangle\\mathrm{F'RQ})=8c=24\\sqrt{2}$.",
  'tags': ['기하', '이차곡선', '타원의정의', '이등변삼각형', '닮음', '28번'],
  'symbols': [{'sym': "$\\overline{\\mathrm{F'P}} + \\overline{\\mathrm{PF}} = 2a = \\overline{\\mathrm{F'Q}}$",
               'desc': "타원의 정의(장축의 길이 $2a$)와 $\\overline{\\mathrm{F'Q}}=2a$에서 "
                       '$\\overline{\\mathrm{PF}}=\\overline{\\mathrm{PQ}}$ 도출',
               'desc_en': "Ellipse definition combined with $\\overline{\\mathrm{F'Q}}=2a$ implies "
                          '$\\overline{\\mathrm{PF}}=\\overline{\\mathrm{PQ}}$.'},
              {'sym': "$\\angle\\mathrm{FF'P} = \\angle\\mathrm{QFP} = \\angle\\mathrm{PQF}$",
               'desc': "이등변삼각형 $\\mathrm{PFQ}$의 밑각 성질로부터 큰 삼각형 $\\mathrm{F'FQ}$도 "
                       "$\\overline{\\mathrm{F'F}}=\\overline{\\mathrm{FQ}}=2c$인 이등변삼각형임을 도출",
               'desc_en': "Base angles show $\\triangle\\mathrm{F'FQ}$ is also isosceles with "
                          "$\\overline{\\mathrm{F'F}}=\\overline{\\mathrm{FQ}}=2c$."},
              {'sym': "$\\text{둘레}(\\triangle\\mathrm{F'RQ}) = 4a + 2c = 8c$",
               'desc': "타원의 정의 $\\overline{\\mathrm{F'R}}+\\overline{\\mathrm{FR}}=2a$를 이용한 삼각형 $\\mathrm{F'RQ}$의 둘레의 "
                       '길이',
               'desc_en': "Perimeter of $\\triangle\\mathrm{F'RQ}$ expressed via the ellipse definition."}],
  'levels': [{'title': "🔰 1단계 · [초등 선분 빼기] $\\overline{\\mathrm{F'P}} + \\overline{\\mathrm{PF}} = "
                       "\\overline{\\mathrm{F'P}} + \\overline{\\mathrm{PQ}}$에서 같은 길이 찾기",
              'title_en': '🔰 Step 1 · [Elementary Segment Subtraction] Finding equal segments from '
                          "$\\overline{\\mathrm{F'P}} + \\overline{\\mathrm{PF}} = \\overline{\\mathrm{F'P}} + "
                          '\\overline{\\mathrm{PQ}}$',
              'knowledge': "타원 위의 점 $\\mathrm{P}$에서 두 초점까지의 거리의 합은 장축의 길이 $\\overline{\\mathrm{F'P}} + "
                           "\\overline{\\mathrm{PF}} = 2a$입니다. 문제에서 선분 $\\mathrm{F'Q}$의 길이도 장축의 길이와 같으므로 "
                           "$\\overline{\\mathrm{F'Q}} = \\overline{\\mathrm{F'P}} + \\overline{\\mathrm{PQ}} = "
                           "2a$입니다. 초등학교 양팔저울처럼 양쪽에서 $\\overline{\\mathrm{F'P}}$를 똑같이 빼면 $\\overline{\\mathrm{PF}} = "
                           '\\overline{\\mathrm{PQ}}$가 됩니다!',
              'knowledge_en': "By the ellipse definition $\\overline{\\mathrm{F'P}} + \\overline{\\mathrm{PF}} = 2a$, "
                              "and since $\\overline{\\mathrm{F'Q}} = \\overline{\\mathrm{F'P}} + "
                              "\\overline{\\mathrm{PQ}} = 2a$, subtracting $\\overline{\\mathrm{F'P}}$ gives "
                              '$\\overline{\\mathrm{PF}} = \\overline{\\mathrm{PQ}}$.',
              'questions': [{'level_label': '초등 선분 비교 디딤돌 1',
                             'level_label_en': 'Elementary Segment Step 1',
                             'stem': "$\\overline{\\mathrm{F'P}} + \\overline{\\mathrm{PF}} = 2a$와 "
                                     "$\\overline{\\mathrm{F'P}} + \\overline{\\mathrm{PQ}} = 2a$의 양변에서 "
                                     "$\\overline{\\mathrm{F'P}}$를 빼면 삼각형 $\\mathrm{PFQ}$는 어떤 삼각형이 되나요?",
                             'stem_en': "Subtracting $\\overline{\\mathrm{F'P}}$ from $\\overline{\\mathrm{F'P}} + "
                                        "\\overline{\\mathrm{PF}} = 2a$ and $\\overline{\\mathrm{F'P}} + "
                                        '\\overline{\\mathrm{PQ}} = 2a$, what kind of triangle is '
                                        '$\\triangle\\mathrm{PFQ}$?',
                             'options': ['$\\overline{\\mathrm{PF}} = \\overline{\\mathrm{PQ}}$인 이등변삼각형',
                                         '$\\overline{\\mathrm{PF}} = \\overline{\\mathrm{FQ}}$인 이등변삼각형',
                                         '정삼각형',
                                         '$\\angle\\mathrm{Q} = 90^\\circ$인 직각삼각형',
                                         '세 변의 길이가 모두 다른 삼각형'],
                             'answer': 1,
                             'exp': '$\\overline{\\mathrm{PF}} = \\overline{\\mathrm{PQ}}$이므로 삼각형 $\\mathrm{PFQ}$는 점 '
                                    '$\\mathrm{P}$가 꼭짓점인 이등변삼각형입니다!',
                             'exp_en': 'Since $\\overline{\\mathrm{PF}} = \\overline{\\mathrm{PQ}}$, '
                                       '$\\triangle\\mathrm{PFQ}$ is isosceles.'}]},
             {'title': "🌿 2단계 · [두 번째 이등변삼각형 발견] $\\angle\\mathrm{FF'P} = \\angle\\mathrm{QFP}$로부터 "
                       '$\\overline{\\mathrm{FQ}}$의 길이 구하기',
              'title_en': '🌿 Step 2 · [Second Isosceles Triangle] Finding $\\overline{\\mathrm{FQ}}$ from '
                          "$\\angle\\mathrm{FF'P} = \\angle\\mathrm{QFP}$",
              'knowledge': '1단계에서 $\\overline{\\mathrm{PF}} = \\overline{\\mathrm{PQ}}$이므로 이등변삼각형 $\\mathrm{PFQ}$의 두 '
                           "밑각은 $\\angle\\mathrm{QFP} = \\angle\\mathrm{PQF}$로 같습니다. 그런데 문제에서 $\\angle\\mathrm{FF'P} = "
                           "\\angle\\mathrm{QFP}$라고 했으므로, 큰 삼각형 $\\mathrm{F'FQ}$에서도 두 밑각 $\\angle\\mathrm{FF'Q} = "
                           "\\angle\\mathrm{F'QF}$가 같아집니다! 즉 큰 삼각형 $\\mathrm{F'FQ}$도 $\\overline{\\mathrm{F'F}} = "
                           '\\overline{\\mathrm{FQ}}$인 이등변삼각형입니다.',
              'knowledge_en': 'Since $\\overline{\\mathrm{PF}} = \\overline{\\mathrm{PQ}}$, $\\angle\\mathrm{QFP} = '
                              "\\angle\\mathrm{PQF}$. Combined with $\\angle\\mathrm{FF'P} = \\angle\\mathrm{QFP}$, we "
                              "get $\\angle\\mathrm{FF'Q} = \\angle\\mathrm{F'QF}$, so $\\triangle\\mathrm{F'FQ}$ is "
                              "isosceles with $\\overline{\\mathrm{F'F}} = \\overline{\\mathrm{FQ}}$.",
              'questions': [{'level_label': '이등변삼각형 발견 디딤돌 2',
                             'level_label_en': 'Second Isosceles Step 2',
                             'stem': "두 초점 $\\mathrm{F}(c, 0), \\mathrm{F'}(-c, 0)$ 사이의 거리가 $\\overline{\\mathrm{F'F}} "
                                     "= 2c$이고 큰 삼각형 $\\mathrm{F'FQ}$에서 $\\angle\\mathrm{FF'Q} = "
                                     "\\angle\\mathrm{F'QF}$일 때, 선분 $\\mathrm{FQ}$의 길이는?",
                             'stem_en': "Since $\\overline{\\mathrm{F'F}} = 2c$ and $\\angle\\mathrm{FF'Q} = "
                                        "\\angle\\mathrm{F'QF}$ in $\\triangle\\mathrm{F'FQ}$, what is "
                                        '$\\overline{\\mathrm{FQ}}$?',
                             'options': ['$c$', '$\\dfrac{3}{2}c$', '$2c$', '$\\dfrac{5}{2}c$', '$3c$'],
                             'answer': 3,
                             'exp': "밑각이 같은 이등변삼각형이므로 $\\overline{\\mathrm{FQ}} = \\overline{\\mathrm{F'F}} = 2c$입니다!",
                             'exp_en': "$\\overline{\\mathrm{FQ}} = \\overline{\\mathrm{F'F}} = 2c$."}]},
             {'title': '🌱 3단계 · [기울기와 삼각비] $\\tan\\theta = \\dfrac{\\sqrt{7}}{3}$일 때 $\\cos\\theta$ 구하기',
              'title_en': '🌱 Step 3 · [Slope & Trigonometry] Finding $\\cos\\theta$ when $\\tan\\theta = '
                          '\\dfrac{\\sqrt{7}}{3}$',
              'knowledge': "직선 $\\mathrm{F'P}$가 $x$축과 이루는 각을 $\\theta = \\angle\\mathrm{FF'P}$라 하면, 직선의 기울기는 "
                           '$\\tan\\theta = \\dfrac{\\sqrt{7}}{3}$입니다. 밑변이 $3$, 높이가 $\\sqrt{7}$인 직각삼각형에서 피타고라스 정리로 빗변의 '
                           '길이를 구하면 $\\sqrt{3^2 + (\\sqrt{7})^2} = \\sqrt{9 + 7} = \\sqrt{16} = 4$입니다.',
              'knowledge_en': "Let $\\theta = \\angle\\mathrm{FF'P}$. Since the slope is $\\tan\\theta = "
                              '\\dfrac{\\sqrt{7}}{3}$, a right triangle with legs $3$ and $\\sqrt{7}$ has hypotenuse '
                              '$\\sqrt{9+7} = 4$.',
              'questions': [{'level_label': '삼각비 코사인 디딤돌 3',
                             'level_label_en': 'Cosine Ratio Step 3',
                             'stem': '밑변이 $3$, 높이가 $\\sqrt{7}$, 빗변이 $4$인 직각삼각형에서 $\\cos\\theta = '
                                     '\\dfrac{(\\text{밑변})}{(\\text{빗변})}$의 값은?',
                             'stem_en': 'In a right triangle with base $3$, height $\\sqrt{7}$, and hypotenuse $4$, '
                                        'what is $\\cos\\theta$?',
                             'options': ['$\\dfrac{1}{4}$',
                                         '$\\dfrac{\\sqrt{7}}{4}$',
                                         '$\\dfrac{3}{4}$',
                                         '$\\dfrac{\\sqrt{7}}{3}$',
                                         '$\\dfrac{4}{3}$'],
                             'answer': 3,
                             'exp': '$\\cos\\theta = \\dfrac{3}{4}$입니다.',
                             'exp_en': '$\\cos\\theta = \\dfrac{3}{4}$.'}]},
             {'title': "🌳 4단계 · [장축의 길이 $2a$와 $c$의 관계] 이등변삼각형 $\\mathrm{F'FQ}$에서 $\\overline{\\mathrm{F'Q}} = 2a$를 "
                       '$c$로 나타내기',
              'title_en': "🌳 Step 4 · [Relating $2a$ and $c$] Expressing $\\overline{\\mathrm{F'Q}} = 2a$ in terms of "
                          '$c$',
              'knowledge': "$\\overline{\\mathrm{F'F}} = \\overline{\\mathrm{FQ}} = 2c$인 이등변삼각형 $\\mathrm{F'FQ}$에서 꼭짓점 "
                           "$\\mathrm{F}$에서 밑변 $\\mathrm{F'Q}$에 수선의 발을 내리면 밑변이 반으로 나뉩니다. 한쪽 절반의 길이가 "
                           "$2c\\cos\\theta$이므로, 전체 밑변의 길이는 $\\overline{\\mathrm{F'Q}} = 2a = 2 \\times "
                           '(2c\\cos\\theta) = 4c\\cos\\theta$입니다!',
              'knowledge_en': "Dropping an altitude from $\\mathrm{F}$ to base $\\mathrm{F'Q}$ in isosceles "
                              "$\\triangle\\mathrm{F'FQ}$ bisects $\\mathrm{F'Q}$, so $\\overline{\\mathrm{F'Q}} = 2a "
                              '= 2(2c\\cos\\theta) = 4c\\cos\\theta$.',
              'questions': [{'level_label': '장축과 초점거리 관계 디딤돌 4',
                             'level_label_en': 'Major Axis & Focal Length Step 4',
                             'stem': '$\\cos\\theta = \\dfrac{3}{4}$일 때, 장축의 길이 $2a = 4c\\cos\\theta$를 $c$로 간단히 나타내면?',
                             'stem_en': 'With $\\cos\\theta = \\dfrac{3}{4}$, what is $2a = 4c\\cos\\theta$ in terms '
                                        'of $c$?',
                             'options': ['$2c$', '$\\dfrac{5}{2}c$', '$3c$', '$\\dfrac{7}{2}c$', '$4c$'],
                             'answer': 3,
                             'exp': '$2a = 4c \\times \\dfrac{3}{4} = 3c$입니다.',
                             'exp_en': '$2a = 3c$.'}]},
             {'title': '🏛️ 5단계 · [삼각형 $\\mathrm{PFQ}$의 높이와 넓이] 밑변 $\\overline{\\mathrm{FQ}} = 2c$에 대한 높이와 넓이 식 세우기',
              'title_en': '🏛️ Step 5 · [Height & Area of $\\triangle\\mathrm{PFQ}$] Expressing the area of '
                          '$\\triangle\\mathrm{PFQ}$ in terms of $c$',
              'knowledge': '작은 이등변삼각형 $\\mathrm{PFQ}$ ($\\overline{\\mathrm{PF}} = \\overline{\\mathrm{PQ}}$)에서 밑변은 '
                           '$\\overline{\\mathrm{FQ}} = 2c$이고 양 끝 밑각은 모두 $\\theta$입니다. 꼭짓점 $\\mathrm{P}$에서 밑변 '
                           '$\\mathrm{FQ}$의 중점에 수선을 내리면 반쪽 밑변이 $c$이므로, 높이는 $h = c\\tan\\theta = '
                           '\\dfrac{\\sqrt{7}}{3}c$가 됩니다!',
              'knowledge_en': 'In isosceles $\\triangle\\mathrm{PFQ}$ with base $\\overline{\\mathrm{FQ}} = 2c$ and '
                              'base angles $\\theta$, the altitude to the midpoint of $\\mathrm{FQ}$ is $h = '
                              'c\\tan\\theta = \\dfrac{\\sqrt{7}}{3}c$.',
              'questions': [{'level_label': '삼각형 PFQ 넓이 식 디딤돌 5',
                             'level_label_en': 'Area Formula of PFQ Step 5',
                             'stem': '밑변이 $2c$이고 높이가 $\\dfrac{\\sqrt{7}}{3}c$인 삼각형 $\\mathrm{PFQ}$의 넓이 $\\dfrac{1}{2} '
                                     '\\times 2c \\times \\dfrac{\\sqrt{7}}{3}c$를 정리한 식은?',
                             'stem_en': 'What is the area $\\dfrac{1}{2} \\times 2c \\times \\dfrac{\\sqrt{7}}{3}c$ of '
                                        '$\\triangle\\mathrm{PFQ}$?',
                             'options': ['$\\dfrac{\\sqrt{7}}{6}c^2$',
                                         '$\\dfrac{\\sqrt{7}}{3}c^2$',
                                         '$\\dfrac{2\\sqrt{7}}{3}c^2$',
                                         '$\\sqrt{7}c^2$',
                                         '$\\dfrac{4\\sqrt{7}}{3}c^2$'],
                             'answer': 2,
                             'exp': '$\\dfrac{1}{2} \\times 2c \\times \\dfrac{\\sqrt{7}}{3}c = '
                                    '\\dfrac{\\sqrt{7}}{3}c^2$입니다.',
                             'exp_en': '$\\dfrac{\\sqrt{7}}{3}c^2$.'}]},
             {'title': '⚡ 6단계 · [초점 거리 $c$ 구하기] $\\dfrac{\\sqrt{7}}{3}c^2 = 6\\sqrt{7}$에서 양수 $c$ 확정하기',
              'title_en': '⚡ Step 6 · [Solving for $c$] Finding $c > 0$ from $\\dfrac{\\sqrt{7}}{3}c^2 = 6\\sqrt{7}$',
              'knowledge': '문제에서 삼각형 $\\mathrm{PFQ}$의 넓이가 $6\\sqrt{7}$이므로 $\\dfrac{\\sqrt{7}}{3}c^2 = 6\\sqrt{7}$입니다. '
                           '양변을 $\\sqrt{7}$로 나누고 $3$을 곱하면 $c^2 = 18$을 얻습니다.',
              'knowledge_en': 'Equating $\\dfrac{\\sqrt{7}}{3}c^2 = 6\\sqrt{7}$ gives $c^2 = 18$.',
              'questions': [{'level_label': 'c의 값 확정 디딤돌 6',
                             'level_label_en': 'Confirming c Step 6',
                             'stem': '$c^2 = 18$일 때, 양수 $c = \\sqrt{18}$을 간단히 한 값은?',
                             'stem_en': 'Given $c^2 = 18$ ($c > 0$), simplify $c = \\sqrt{18}$.',
                             'options': ['$2\\sqrt{2}$', '$2\\sqrt{3}$', '$3\\sqrt{2}$', '$3\\sqrt{3}$', '$6$'],
                             'answer': 3,
                             'exp': '$\\sqrt{18} = \\sqrt{9 \\times 2} = 3\\sqrt{2}$입니다.',
                             'exp_en': '$c = 3\\sqrt{2}$.'}]},
             {'title': "🌟 7단계 · [삼각형 $\\mathrm{F'RQ}$의 둘레 식] 타원의 정의로 둘레를 $c$로 나타내기",
              'title_en': "🌟 Step 7 · [Perimeter of $\\triangle\\mathrm{F'RQ}$] Expressing the perimeter in terms of "
                          '$c$',
              'knowledge': '점 $\\mathrm{R}$은 직선 $\\mathrm{FQ}$ 위에 있어 $\\overline{\\mathrm{RQ}} = '
                           '\\overline{\\mathrm{RF}} + \\overline{\\mathrm{FQ}}$이고, 동시에 타원 $C$ 위의 점이므로 타원의 정의에 의해 '
                           "$\\overline{\\mathrm{F'R}} + \\overline{\\mathrm{RF}} = 2a$입니다! 따라서 삼각형 $\\mathrm{F'RQ}$의 "
                           "둘레는 $\\overline{\\mathrm{F'Q}} + \\overline{\\mathrm{F'R}} + \\overline{\\mathrm{RQ}} = 2a "
                           "+ (\\overline{\\mathrm{F'R}} + \\overline{\\mathrm{RF}}) + \\overline{\\mathrm{FQ}} = 2a + "
                           '2a + 2c = 4a + 2c$입니다.',
              'knowledge_en': 'Since $\\overline{\\mathrm{RQ}} = \\overline{\\mathrm{RF}} + \\overline{\\mathrm{FQ}}$ '
                              "and $\\overline{\\mathrm{F'R}} + \\overline{\\mathrm{RF}} = 2a$, the perimeter of "
                              "$\\triangle\\mathrm{F'RQ}$ is $2a + 2a + 2c = 4a + 2c$.",
              'questions': [{'level_label': '둘레 식 정리 디딤돌 7',
                             'level_label_en': 'Perimeter in Terms of c Step 7',
                             'stem': "4단계에서 구한 $2a = 3c$를 대입하면, 삼각형 $\\mathrm{F'RQ}$의 둘레의 길이 $4a + 2c = 2(2a) + 2c$는 "
                                     '$c$의 몇 배인가요?',
                             'stem_en': 'Substituting $2a = 3c$ into $4a + 2c = 2(2a) + 2c$, what multiple of $c$ is '
                                        'the perimeter?',
                             'options': ['$5c$', '$6c$', '$7c$', '$8c$', '$9c$'],
                             'answer': 4,
                             'exp': '$2(3c) + 2c = 6c + 2c = 8c$입니다.',
                             'exp_en': '$8c$.'}]},
             {'title': "💎 8단계 · [최종 종합] 삼각형 $\\mathrm{F'RQ}$의 둘레의 길이 $8c$ 확정하기",
              'title_en': '💎 Step 8 · [Final Synthesis] Computing the final perimeter $8c$',
              'knowledge': '6단계에서 구한 $c = 3\\sqrt{2}$를 7단계의 둘레 식 $8c$에 대입하면 최종 정답이 완성됩니다!',
              'knowledge_en': 'Substituting $c = 3\\sqrt{2}$ into $8c$ gives the final answer.',
              'questions': [{'level_label': '최종 종합 디딤돌 8',
                             'level_label_en': 'Final Synthesis Step 8',
                             'stem': "$c = 3\\sqrt{2}$일 때, 삼각형 $\\mathrm{F'RQ}$의 둘레의 길이 $8c$의 값은?",
                             'stem_en': 'When $c = 3\\sqrt{2}$, what is the perimeter $8c$ of '
                                        "$\\triangle\\mathrm{F'RQ}$?",
                             'options': ['$20\\sqrt{2}$',
                                         '$22\\sqrt{2}$',
                                         '$24\\sqrt{2}$',
                                         '$26\\sqrt{2}$',
                                         '$28\\sqrt{2}$'],
                             'answer': 3,
                             'exp': '$8 \\times 3\\sqrt{2} = 24\\sqrt{2}$이므로 정답은 ③입니다.',
                             'exp_en': '$8 \\times 3\\sqrt{2} = 24\\sqrt{2}$ (choice ③).'}]}],
  'final': {'stem': "두 초점이 $\\mathrm{F}(c, 0), \\mathrm{F'}(-c, 0)$ ($c > 0$)인 타원 $C$가 있다. 타원 $C$ 위에 있는 제$1$사분면 위의 점 "
                    "$\\mathrm{P}$에 대하여 직선 $\\mathrm{F'P}$ 위에 점 $\\mathrm{Q}$를 선분 $\\mathrm{F'Q}$의 길이와 타원 $C$의 장축의 길이가 "
                    '같도록 잡을 때, 직선 $\\mathrm{FQ}$가 타원 $C$와 만나는 점 중 $y$좌표가 음수인 점을 $\\mathrm{R}$이라 하자. 직선 '
                    "$\\mathrm{F'P}$의 기울기가 $\\dfrac{\\sqrt{7}}{3}$이고, $\\angle\\mathrm{FF'P} = "
                    "\\angle\\mathrm{QFP}$이다. 삼각형 $\\mathrm{PFQ}$의 넓이가 $6\\sqrt{7}$일 때, 삼각형 $\\mathrm{F'RQ}$의 둘레의 길이는? "
                    '[4점]',
            'stem_en': "An ellipse $C$ has foci $\\mathrm{F}(c, 0), \\mathrm{F'}(-c, 0)$ ($c > 0$). For a "
                       "first-quadrant point $\\mathrm{P}$ on $C$, point $\\mathrm{Q}$ on ray $\\mathrm{F'P}$ is "
                       "chosen so that $\\overline{\\mathrm{F'Q}}$ equals the major axis length of $C$, and line "
                       '$\\mathrm{FQ}$ meets $C$ at $\\mathrm{R}$ ($y_{\\mathrm{R}} < 0$). The slope of line '
                       "$\\mathrm{F'P}$ is $\\dfrac{\\sqrt{7}}{3}$ and $\\angle\\mathrm{FF'P} = \\angle\\mathrm{QFP}$. "
                       'If $\\text{Area}(\\triangle\\mathrm{PFQ}) = 6\\sqrt{7}$, what is the perimeter of '
                       "$\\triangle\\mathrm{F'RQ}$? [4 points]",
            'options': ['$20\\sqrt{2}$', '$22\\sqrt{2}$', '$24\\sqrt{2}$', '$26\\sqrt{2}$', '$28\\sqrt{2}$'],
            'answer': 3,
            'exp': "타원의 정의에서 $\\overline{\\mathrm{PF}} = \\overline{\\mathrm{PQ}}$이고 $\\angle\\mathrm{FF'P} = "
                   "\\angle\\mathrm{QFP} = \\angle\\mathrm{PQF}$이므로 $\\overline{\\mathrm{F'F}} = "
                   '\\overline{\\mathrm{FQ}} = 2c$입니다. $\\tan\\theta = \\dfrac{\\sqrt{7}}{3} \\implies \\cos\\theta = '
                   '\\dfrac{3}{4}$에서 $2a = 3c$이고, $\\text{Area}(\\triangle\\mathrm{PFQ}) = \\dfrac{\\sqrt{7}}{3}c^2 = '
                   "6\\sqrt{7} \\implies c = 3\\sqrt{2}$입니다. 따라서 $\\triangle\\mathrm{F'RQ}$의 둘레는 $4a + 2c = 8c = "
                   '24\\sqrt{2}$입니다.',
            'exp_en': 'By the ellipse definition, $\\overline{\\mathrm{PF}} = \\overline{\\mathrm{PQ}}$ and '
                      "$\\angle\\mathrm{FF'P} = \\angle\\mathrm{QFP} = \\angle\\mathrm{PQF}$, so "
                      "$\\overline{\\mathrm{F'F}} = \\overline{\\mathrm{FQ}} = 2c$. From $\\tan\\theta = "
                      '\\dfrac{\\sqrt{7}}{3}$ ($\\cos\\theta = \\dfrac{3}{4}$), we get $2a = 3c$ and '
                      '$\\text{Area}(\\triangle\\mathrm{PFQ}) = \\dfrac{\\sqrt{7}}{3}c^2 = 6\\sqrt{7} \\implies c = '
                      "3\\sqrt{2}$. Thus $\\text{Perimeter}(\\triangle\\mathrm{F'RQ}) = 4a + 2c = 8c = 24\\sqrt{2}$.",
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        "<p>본 문항은 <b>타원의 정의($\\overline{\\mathrm{F'P}} + \\overline{\\mathrm{PF}} = 2a$)를 이용하여 숨겨진 두 "
                        "이등변삼각형($\\triangle\\mathrm{PFQ}$, $\\triangle\\mathrm{F'FQ}$)을 발견</b>하는 기하 4점 문항입니다.</p>\n"
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 타원의 정의로 두 이등변삼각형 발견</b><br>\n'
                        "  타원의 장축의 길이를 $2a$라 하면 $\\overline{\\mathrm{F'P}} + \\overline{\\mathrm{PF}} = 2a$이고, 조건에서 "
                        "$\\overline{\\mathrm{F'Q}} = \\overline{\\mathrm{F'P}} + \\overline{\\mathrm{PQ}} = "
                        '2a$이므로:<br>\n'
                        '  $$\\overline{\\mathrm{PF}} = \\overline{\\mathrm{PQ}}$$\n'
                        '  따라서 $\\triangle\\mathrm{PFQ}$는 이등변삼각형이고 $\\angle\\mathrm{QFP} = '
                        '\\angle\\mathrm{PQF}$입니다.<br>\n'
                        "  조건에서 $\\angle\\mathrm{FF'P} = \\angle\\mathrm{QFP}$이므로 $\\angle\\mathrm{FF'Q} = "
                        "\\angle\\mathrm{F'QF}$가 되어 큰 삼각형 $\\mathrm{F'FQ}$도 $\\overline{\\mathrm{F'F}} = "
                        '\\overline{\\mathrm{FQ}} = 2c$인 이등변삼각형입니다.<br><br>\n'
                        '  <b>2단계: 삼각비로 $2a = 3c$와 $c = 3\\sqrt{2}$ 구하기</b><br>\n'
                        "  $\\angle\\mathrm{FF'P} = \\theta$라 하면 $\\tan\\theta = \\dfrac{\\sqrt{7}}{3} \\implies "
                        '\\cos\\theta = \\dfrac{3}{4}$입니다.<br>\n'
                        "  $\\overline{\\mathrm{F'F}} = \\overline{\\mathrm{FQ}} = 2c$인 이등변삼각형 "
                        "$\\mathrm{F'FQ}$에서:<br>\n"
                        "  $$\\overline{\\mathrm{F'Q}} = 2a = 2(2c\\cos\\theta) = 4c \\times \\frac{3}{4} = 3c$$\n"
                        '  또한 이등변삼각형 $\\mathrm{PFQ}$에서 밑변은 $\\overline{\\mathrm{FQ}} = 2c$이고 높이는 $c\\tan\\theta = '
                        '\\dfrac{\\sqrt{7}}{3}c$이므로:<br>\n'
                        '  $$\\text{Area}(\\triangle\\mathrm{PFQ}) = \\frac{1}{2} \\times 2c \\times '
                        '\\frac{\\sqrt{7}}{3}c = \\frac{\\sqrt{7}}{3}c^2 = 6\\sqrt{7} \\implies c^2 = 18 \\implies c = '
                        '3\\sqrt{2}$$<br>\n'
                        "  <b>3단계: 삼각형 $\\mathrm{F'RQ}$의 둘레의 길이 구하기</b><br>\n"
                        "  점 $\\mathrm{R}$도 타원 위의 점이므로 $\\overline{\\mathrm{F'R}} + \\overline{\\mathrm{RF}} = "
                        '2a$입니다.<br>\n'
                        "  $$\\text{둘레}(\\triangle\\mathrm{F'RQ}) = \\overline{\\mathrm{F'Q}} + "
                        "\\overline{\\mathrm{F'R}} + \\overline{\\mathrm{RQ}} = 2a + (\\overline{\\mathrm{F'R}} + "
                        '\\overline{\\mathrm{RF}}) + \\overline{\\mathrm{FQ}} = 4a + 2c = 6c + 2c = 8c = '
                        '24\\sqrt{2}$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        "  따라서 삼각형 $\\mathrm{F'RQ}$의 둘레의 길이는 $24\\sqrt{2}$이므로 정답은 <b>③번</b>입니다.\n"
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem uses the <b>definition of an ellipse</b> to identify two similar isosceles '
                           "triangles $\\triangle\\mathrm{PFQ}$ and $\\triangle\\mathrm{F'FQ}$.</p>\n"
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Isosceles triangles</b><br>\n'
                           "  From $\\overline{\\mathrm{F'P}} + \\overline{\\mathrm{PF}} = 2a = "
                           "\\overline{\\mathrm{F'P}} + \\overline{\\mathrm{PQ}}$, we have $\\overline{\\mathrm{PF}} = "
                           "\\overline{\\mathrm{PQ}}$, so $\\angle\\mathrm{FF'P} = \\angle\\mathrm{QFP} = "
                           "\\angle\\mathrm{PQF}$ and $\\overline{\\mathrm{F'F}} = \\overline{\\mathrm{FQ}} = "
                           '2c$.<br>\n'
                           '  With $\\tan\\theta = \\frac{\\sqrt{7}}{3}$ ($\\cos\\theta = \\frac{3}{4}$), we get $2a = '
                           '4c\\cos\\theta = 3c$.<br><br>\n'
                           '  <b>Step 2: Area and perimeter</b><br>\n'
                           '  $$\\text{Area}(\\triangle\\mathrm{PFQ}) = \\frac{1}{2}(2c)(c\\tan\\theta) = '
                           '\\frac{\\sqrt{7}}{3}c^2 = 6\\sqrt{7} \\implies c = 3\\sqrt{2}$$\n'
                           "  $$\\text{Perimeter}(\\triangle\\mathrm{F'RQ}) = 2a + (\\overline{\\mathrm{F'R}} + "
                           '\\overline{\\mathrm{RF}}) + 2c = 4a + 2c = 8c = 24\\sqrt{2}$$\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  The correct answer is <b>choice ③ ($24\\sqrt{2}$)</b>.\n'
                           '</p>'}},
 {'slug': 'c2610g29',
  'qNum': '기하 29',
  'subject': '기하',
  'title': '[2026학년도 10월 고3 기하 29번] 직육면체에서 두 평면이 이루는 각과 정사영의 넓이',
  'title_en': '[2026 AY Oct Exam Grade 12 Geometry #29] Dihedral Angle and Orthogonal Projection Area in a Rectangular '
              'Box',
  'summary_ko': '직육면체 $\\mathrm{ABCD-EFGH}$에서 내분점 길이 $\\overline{\\mathrm{AP}}=4, \\overline{\\mathrm{AQ}}=2$와 '
                '$\\text{Area}(\\triangle\\mathrm{QRS})=3\\sqrt{10}$으로부터 $\\overline{\\mathrm{ER}}=1$을 구하고, 옆면 단면 벡터로 '
                '이면각 $\\cos\\theta=\\dfrac{4}{5}$를 구해 $S=\\dfrac{8\\sqrt{10}}{5},\\ 25S^2=640$ 도출하기',
  'summary_en': 'In box $\\mathrm{ABCD-EFGH}$, find $\\overline{\\mathrm{AP}}=4, \\overline{\\mathrm{AQ}}=2$, use '
                '$\\text{Area}(\\triangle\\mathrm{QRS})=3\\sqrt{10}$ to get $\\overline{\\mathrm{ER}}=1$, find '
                'dihedral cosine $\\cos\\theta=\\dfrac{4}{5}$, and obtain $S=\\dfrac{8\\sqrt{10}}{5}$ and $25S^2=640$.',
  'tags': ['기하', '공간도형과공간좌표', '정사영', '이면각', '삼수선의정리', '단답형', '29번'],
  'symbols': [{'sym': '$\\overline{\\mathrm{AP}} = 4,\\quad \\overline{\\mathrm{AQ}} = 2$',
               'desc': '선분 $\\mathrm{AB}=6$의 $2:1$ 내분점 $\\mathrm{P}$와 선분 $\\mathrm{AD}=6$의 $1:2$ 내분점 $\\mathrm{Q}$까지의 '
                       '길이',
               'desc_en': 'Internal division lengths $\\overline{\\mathrm{AP}}=4$ and $\\overline{\\mathrm{AQ}}=2$.'},
              {'sym': '$\\overline{\\mathrm{RS}} \\parallel \\overline{\\mathrm{EF}} \\perp (\\text{평면 '
                      '}\\mathrm{AEHD})$',
               'desc': '직선 $\\mathrm{RS}$와 $\\mathrm{AP}$가 모두 옆면 $\\mathrm{AEHD}$에 수직임을 뜻하는 공간도형 성질',
               'desc_en': 'Both $\\mathrm{RS}$ and $\\mathrm{AP}$ are perpendicular to the side face '
                          '$\\mathrm{AEHD}$.'},
              {'sym': '$S = \\text{Area}(\\triangle\\mathrm{ARP})\\cos\\theta$',
               'desc': '두 평면 $\\mathrm{ARP}, \\mathrm{QRS}$가 이루는 각이 $\\theta$일 때 정사영의 넓이 공식',
               'desc_en': 'Orthogonal projection area formula.'}],
  'levels': [{'title': '🔰 1단계 · [초등 비례배분] $\\overline{\\mathrm{AB}} = 6, \\overline{\\mathrm{AD}} = 6$에서 '
                       '$\\overline{\\mathrm{AP}}$와 $\\overline{\\mathrm{AQ}}$의 길이 구하기',
              'title_en': '🔰 Step 1 · [Elementary Proportional Division] Finding $\\overline{\\mathrm{AP}}$ and '
                          '$\\overline{\\mathrm{AQ}}$ from $\\overline{\\mathrm{AB}} = \\overline{\\mathrm{AD}} = 6$',
              'knowledge': '직육면체에서 $\\overline{\\mathrm{AB}} = 6$을 $2 : 1$로 내분하는 점이 $\\mathrm{P}$이고, '
                           '$\\overline{\\mathrm{AD}} = 6$을 $1 : 2$로 내분하는 점이 $\\mathrm{Q}$입니다. 초등학교 비례배분처럼 전체 $2 + 1 = '
                           '3$칸으로 나누어 한 칸의 길이($6 \\div 3 = 2$)를 구해 봅시다!',
              'knowledge_en': 'Point $\\mathrm{P}$ divides $\\overline{\\mathrm{AB}} = 6$ in the ratio $2:1$, and '
                              '$\\mathrm{Q}$ divides $\\overline{\\mathrm{AD}} = 6$ in the ratio $1:2$.',
              'questions': [{'level_label': '초등 비례배분 디딤돌 1',
                             'level_label_en': 'Elementary Ratio Step 1',
                             'stem': '길이 $6$을 $2 : 1$로 나눈 $\\overline{\\mathrm{AP}}$의 길이와 $1 : 2$로 나눈 '
                                     '$\\overline{\\mathrm{AQ}}$의 길이를 순서대로 바르게 짝지은 것은?',
                             'stem_en': 'What are the lengths $\\overline{\\mathrm{AP}}$ ($2:1$ of $6$) and '
                                        '$\\overline{\\mathrm{AQ}}$ ($1:2$ of $6$)?',
                             'options': ['$\\overline{\\mathrm{AP}} = 3,\\ \\overline{\\mathrm{AQ}} = 3$',
                                         '$\\overline{\\mathrm{AP}} = 4,\\ \\overline{\\mathrm{AQ}} = 2$',
                                         '$\\overline{\\mathrm{AP}} = 2,\\ \\overline{\\mathrm{AQ}} = 4$',
                                         '$\\overline{\\mathrm{AP}} = 5,\\ \\overline{\\mathrm{AQ}} = 1$',
                                         '$\\overline{\\mathrm{AP}} = 4,\\ \\overline{\\mathrm{AQ}} = 3$'],
                             'answer': 2,
                             'exp': '$\\overline{\\mathrm{AP}} = 6 \\times \\dfrac{2}{3} = 4$이고, '
                                    '$\\overline{\\mathrm{AQ}} = 6 \\times \\dfrac{1}{3} = 2$입니다.',
                             'exp_en': '$\\overline{\\mathrm{AP}} = 4$ and $\\overline{\\mathrm{AQ}} = 2$.'}]},
             {'title': '🌿 2단계 · [초등 삼각형의 넓이] $\\triangle\\mathrm{QRS}$의 넓이 $3\\sqrt{10}$에서 선분 $\\mathrm{QR}$의 길이 구하기',
              'title_en': '🌿 Step 2 · [Triangle Area] Finding $\\overline{\\mathrm{QR}}$ from '
                          '$\\text{Area}(\\triangle\\mathrm{QRS}) = 3\\sqrt{10}$',
              'knowledge': '선분 $\\mathrm{RS}$는 모서리 $\\mathrm{EF}$와 평행하므로 길이가 $\\overline{\\mathrm{RS}} = '
                           '\\overline{\\mathrm{EF}} = \\overline{\\mathrm{AB}} = 6$이고, 옆면 $\\mathrm{AEHD}$ 전체와 수직입니다! '
                           '따라서 옆면 $\\mathrm{AEHD}$ 위에 있는 선분 $\\mathrm{QR}$과 선분 $\\mathrm{RS}$는 서로 수직($\\mathrm{QR} '
                           '\\perp \\mathrm{RS}$)이어서 $\\triangle\\mathrm{QRS}$는 직각삼각형입니다.',
              'knowledge_en': 'Since $\\mathrm{RS} \\parallel \\mathrm{EF}$ and $\\mathrm{EF} \\perp (\\text{face '
                              '}\\mathrm{AEHD})$, we have $\\overline{\\mathrm{RS}} = 6$ and $\\mathrm{QR} \\perp '
                              '\\mathrm{RS}$.',
              'questions': [{'level_label': '선분 QR 길이 디딤돌 2',
                             'level_label_en': 'Length of QR Step 2',
                             'stem': '밑변이 $\\overline{\\mathrm{RS}} = 6$이고 높이가 $\\overline{\\mathrm{QR}}$인 직각삼각형 '
                                     '$\\mathrm{QRS}$의 넓이 $\\dfrac{1}{2} \\times 6 \\times \\overline{\\mathrm{QR}} = '
                                     '3\\sqrt{10}$일 때, $\\overline{\\mathrm{QR}}$의 길이는?',
                             'stem_en': 'Given $\\text{Area}(\\triangle\\mathrm{QRS}) = \\dfrac{1}{2} \\times 6 '
                                        '\\times \\overline{\\mathrm{QR}} = 3\\sqrt{10}$, what is '
                                        '$\\overline{\\mathrm{QR}}$?',
                             'options': ['$\\sqrt{5}$',
                                         '$\\sqrt{10}$',
                                         '$2\\sqrt{5}$',
                                         '$2\\sqrt{10}$',
                                         '$3\\sqrt{10}$'],
                             'answer': 2,
                             'exp': '$3\\overline{\\mathrm{QR}} = 3\\sqrt{10}$이므로 $\\overline{\\mathrm{QR}} = '
                                    '\\sqrt{10}$입니다.',
                             'exp_en': '$\\overline{\\mathrm{QR}} = \\sqrt{10}$.'}]},
             {'title': '🌱 3단계 · [옆면 피타고라스 정리] $\\overline{\\mathrm{QR}} = \\sqrt{10}$과 $\\overline{\\mathrm{ER}} < 2$로 '
                       '$\\overline{\\mathrm{ER}}$의 길이 확정하기',
              'title_en': '🌱 Step 3 · [Side Face Pythagoras] Finding $\\overline{\\mathrm{ER}}$ from '
                          '$\\overline{\\mathrm{QR}} = \\sqrt{10}$ and $\\overline{\\mathrm{ER}} < 2$',
              'knowledge': '직사각형 모양인 옆면 $\\mathrm{AEHD}$에서 높이는 $\\overline{\\mathrm{AE}} = 3$이고, 위쪽 변에서 '
                           '$\\overline{\\mathrm{AQ}} = 2$, 아래쪽 변에서 $\\overline{\\mathrm{ER}} = r$이라 하면 가로 차이는 $|2 - '
                           'r|$입니다. 피타고라스 정리에 의해 $\\overline{\\mathrm{QR}}^2 = (2 - r)^2 + 3^2 = 10$입니다!',
              'knowledge_en': 'In rectangle $\\mathrm{AEHD}$ with height $\\overline{\\mathrm{AE}} = 3$, let '
                              '$\\overline{\\mathrm{ER}} = r$. Then $\\overline{\\mathrm{QR}}^2 = (2 - r)^2 + 3^2 = '
                              '10$.',
              'questions': [{'level_label': 'ER 길이 확정 디딤돌 3',
                             'level_label_en': 'Finding ER Step 3',
                             'stem': '$(2 - r)^2 + 9 = 10$이고 문제 조건에서 $r = \\overline{\\mathrm{ER}} < 2$일 때, $r$의 값은?',
                             'stem_en': 'From $(2 - r)^2 + 9 = 10$ and $r = \\overline{\\mathrm{ER}} < 2$, what is '
                                        '$r$?',
                             'options': ['$\\dfrac{1}{2}$', '$1$', '$\\dfrac{3}{2}$', '$\\sqrt{2}$', '$\\sqrt{3}$'],
                             'answer': 2,
                             'exp': '$(2 - r)^2 = 1 \\implies 2 - r = \\pm 1$인데 $r < 2$이므로 $r = 1$입니다.',
                             'exp_en': '$r = 1$.'}]},
             {'title': '🌳 4단계 · [삼각형 $\\mathrm{ARP}$의 넓이] 직각삼각형 $\\mathrm{ARP}$의 두 직각변과 넓이 구하기',
              'title_en': '🌳 Step 4 · [Area of $\\triangle\\mathrm{ARP}$] Finding the legs and area of right triangle '
                          '$\\triangle\\mathrm{ARP}$',
              'knowledge': '직각삼각형 $\\mathrm{AER}$에서 $\\overline{\\mathrm{AE}} = 3, \\overline{\\mathrm{ER}} = 1$이므로 빗변 '
                           '$\\overline{\\mathrm{AR}} = \\sqrt{3^2 + 1^2} = \\sqrt{10}$입니다. 또한 모서리 $\\mathrm{AB}$ 위의 '
                           '선분 $\\mathrm{AP}$($\\overline{\\mathrm{AP}} = 4$)는 옆면 $\\mathrm{AEHD}$에 수직이므로 '
                           '$\\mathrm{AP} \\perp \\mathrm{AR}$입니다! 즉 $\\triangle\\mathrm{ARP}$는 $\\angle\\mathrm{PAR} '
                           '= 90^\\circ$인 직각삼각형입니다.',
              'knowledge_en': 'In $\\triangle\\mathrm{AER}$, $\\overline{\\mathrm{AR}} = \\sqrt{3^2+1^2} = '
                              '\\sqrt{10}$. Since $\\mathrm{AP} \\perp (\\text{face }\\mathrm{AEHD})$, $\\mathrm{AP} '
                              '\\perp \\mathrm{AR}$ with $\\overline{\\mathrm{AP}} = 4$.',
              'questions': [{'level_label': '삼각형 ARP 넓이 디딤돌 4',
                             'level_label_en': 'Area of ARP Step 4',
                             'stem': '두 직각변이 $\\overline{\\mathrm{AP}} = 4$, $\\overline{\\mathrm{AR}} = \\sqrt{10}$인 '
                                     '직각삼각형 $\\mathrm{ARP}$의 넓이 $\\dfrac{1}{2} \\times 4 \\times \\sqrt{10}$은?',
                             'stem_en': 'What is the area $\\dfrac{1}{2} \\times 4 \\times \\sqrt{10}$ of right '
                                        'triangle $\\triangle\\mathrm{ARP}$?',
                             'options': ['$\\sqrt{10}$',
                                         '$2\\sqrt{10}$',
                                         '$3\\sqrt{10}$',
                                         '$4\\sqrt{10}$',
                                         '$6\\sqrt{10}$'],
                             'answer': 2,
                             'exp': '$\\dfrac{1}{2} \\times 4 \\times \\sqrt{10} = 2\\sqrt{10}$입니다.',
                             'exp_en': '$2\\sqrt{10}$.'}]},
             {'title': '🏛️ 5단계 · [두 평면의 이면각 구조] 옆면 $\\mathrm{AEHD}$에서 이면각 $\\theta = \\angle\\mathrm{ARQ}$ 찾기',
              'title_en': '🏛️ Step 5 · [Dihedral Angle Structure] Identifying $\\theta = \\angle\\mathrm{ARQ}$ in side '
                          'face $\\mathrm{AEHD}$',
              'knowledge': '평면 $\\mathrm{ARP}$에 포함된 직선 $\\mathrm{AP}$와 평면 $\\mathrm{QRS}$에 포함된 직선 $\\mathrm{RS}$는 모두 '
                           '모서리 $\\mathrm{EF}$에 평행하므로 옆면 $\\mathrm{AEHD}$에 수직입니다. 따라서 두 평면이 이루는 이면각 $\\theta$는 두 평면이 '
                           '옆면 $\\mathrm{AEHD}$와 만나서 이루는 두 선분 $\\mathrm{RA}$와 $\\mathrm{RQ}$ 사이의 각 '
                           '$\\angle\\mathrm{ARQ}$와 정확히 같습니다!',
              'knowledge_en': 'Since both planes $\\mathrm{ARP}$ and $\\mathrm{QRS}$ are perpendicular to face '
                              '$\\mathrm{AEHD}$, their dihedral angle $\\theta$ equals $\\angle\\mathrm{ARQ}$ in face '
                              '$\\mathrm{AEHD}$.',
              'questions': [{'level_label': '평면벡터 성분 디딤돌 5',
                             'level_label_en': 'Side Face Vectors Step 5',
                             'stem': '옆면 $\\mathrm{AEHD}$ 위에서 점 $\\mathrm{E}(0, 0)$을 원점으로 놓으면 $\\mathrm{R}(1, 0), '
                                     '\\mathrm{A}(0, 3), \\mathrm{Q}(2, 3)$입니다. 시점을 $\\mathrm{R}$로 한 두 벡터 '
                                     '$\\overrightarrow{\\mathrm{RA}}$와 $\\overrightarrow{\\mathrm{RQ}}$의 성분은?',
                             'stem_en': 'In face $\\mathrm{AEHD}$ with $\\mathrm{E}(0,0), \\mathrm{R}(1,0), '
                                        '\\mathrm{A}(0,3), \\mathrm{Q}(2,3)$, what are '
                                        '$\\overrightarrow{\\mathrm{RA}}$ and $\\overrightarrow{\\mathrm{RQ}}$?',
                             'options': ['$\\overrightarrow{\\mathrm{RA}} = (-1, 3),\\ \\overrightarrow{\\mathrm{RQ}} '
                                         '= (1, 3)$',
                                         '$\\overrightarrow{\\mathrm{RA}} = (1, 3),\\ \\overrightarrow{\\mathrm{RQ}} = '
                                         '(2, 3)$',
                                         '$\\overrightarrow{\\mathrm{RA}} = (-1, 3),\\ \\overrightarrow{\\mathrm{RQ}} '
                                         '= (2, 3)$',
                                         '$\\overrightarrow{\\mathrm{RA}} = (0, 3),\\ \\overrightarrow{\\mathrm{RQ}} = '
                                         '(1, 3)$',
                                         '$\\overrightarrow{\\mathrm{RA}} = (-1, 2),\\ \\overrightarrow{\\mathrm{RQ}} '
                                         '= (1, 2)$'],
                             'answer': 1,
                             'exp': '$\\overrightarrow{\\mathrm{RA}} = (0 - 1, 3 - 0) = (-1, 3)$이고 '
                                    '$\\overrightarrow{\\mathrm{RQ}} = (2 - 1, 3 - 0) = (1, 3)$입니다.',
                             'exp_en': '$\\overrightarrow{\\mathrm{RA}} = (-1, 3)$ and $\\overrightarrow{\\mathrm{RQ}} '
                                       '= (1, 3)$.'}]},
             {'title': '⚡ 6단계 · [이면각의 코사인] 내적으로 $\\cos\\theta$ 계산하기',
              'title_en': '⚡ Step 6 · [Cosine of Dihedral Angle] Computing $\\cos\\theta$ via dot product',
              'knowledge': '두 벡터 $\\overrightarrow{\\mathrm{RA}} = (-1, 3)$과 $\\overrightarrow{\\mathrm{RQ}} = (1, '
                           '3)$의 크기는 모두 $\\sqrt{1 + 9} = \\sqrt{10}$이고, 내적은 $(-1)\\times 1 + 3\\times 3 = -1 + 9 = '
                           '8$입니다. (또는 삼각형 $\\mathrm{ARQ}$에서 코사인법칙을 써도 똑같습니다!)',
              'knowledge_en': 'With $\\overrightarrow{\\mathrm{RA}} = (-1, 3)$ and $\\overrightarrow{\\mathrm{RQ}} = '
                              '(1, 3)$, both lengths are $\\sqrt{10}$ and their dot product is $-1 + 9 = 8$.',
              'questions': [{'level_label': '이면각 코사인 디딤돌 6',
                             'level_label_en': 'Dihedral Cosine Step 6',
                             'stem': '두 평면이 이루는 각 $\\theta$에 대하여 $\\cos\\theta = '
                                     '\\dfrac{\\overrightarrow{\\mathrm{RA}}\\cdot\\overrightarrow{\\mathrm{RQ}}}{|\\overrightarrow{\\mathrm{RA}}||\\overrightarrow{\\mathrm{RQ}}|} '
                                     '= \\dfrac{8}{\\sqrt{10}\\times\\sqrt{10}}$을 기약분수로 나타내면?',
                             'stem_en': 'What is $\\cos\\theta = \\dfrac{8}{\\sqrt{10}\\times\\sqrt{10}}$ in lowest '
                                        'terms?',
                             'options': ['$\\dfrac{1}{5}$',
                                         '$\\dfrac{2}{5}$',
                                         '$\\dfrac{3}{5}$',
                                         '$\\dfrac{4}{5}$',
                                         '$\\dfrac{9}{10}$'],
                             'answer': 4,
                             'exp': '$\\dfrac{8}{10} = \\dfrac{4}{5}$입니다.',
                             'exp_en': '$\\cos\\theta = \\dfrac{4}{5}$.'}]},
             {'title': '🌟 7단계 · [정사영의 넓이 $S$] $S = \\text{Area}(\\triangle\\mathrm{ARP}) \\times \\cos\\theta$ 구하기',
              'title_en': '🌟 Step 7 · [Projected Area $S$] Computing $S = \\text{Area}(\\triangle\\mathrm{ARP}) '
                          '\\times \\cos\\theta$',
              'knowledge': '정사영의 넓이 공식에 따라 4단계에서 구한 $\\text{Area}(\\triangle\\mathrm{ARP}) = 2\\sqrt{10}$에 6단계에서 구한 '
                           '$\\cos\\theta = \\dfrac{4}{5}$를 곱하면 $S$를 얻습니다.',
              'knowledge_en': 'By the orthogonal projection area formula, $S = '
                              '\\text{Area}(\\triangle\\mathrm{ARP})\\cos\\theta = 2\\sqrt{10} \\times \\dfrac{4}{5}$.',
              'questions': [{'level_label': '정사영 넓이 디딤돌 7',
                             'level_label_en': 'Projected Area Step 7',
                             'stem': '$\\text{Area}(\\triangle\\mathrm{ARP}) = 2\\sqrt{10}$이고 $\\cos\\theta = '
                                     '\\dfrac{4}{5}$일 때, 정사영의 넓이 $S = 2\\sqrt{10} \\times \\dfrac{4}{5}$는?',
                             'stem_en': 'With $\\text{Area}(\\triangle\\mathrm{ARP}) = 2\\sqrt{10}$ and $\\cos\\theta '
                                        '= \\dfrac{4}{5}$, what is $S$?',
                             'options': ['$\\dfrac{4\\sqrt{10}}{5}$',
                                         '$\\dfrac{6\\sqrt{10}}{5}$',
                                         '$\\dfrac{8\\sqrt{10}}{5}$',
                                         '$2\\sqrt{10}$',
                                         '$\\dfrac{12\\sqrt{10}}{5}$'],
                             'answer': 3,
                             'exp': '$S = \\dfrac{8\\sqrt{10}}{5}$입니다.',
                             'exp_en': '$S = \\dfrac{8\\sqrt{10}}{5}$.'}]},
             {'title': '💎 8단계 · [최종 종합] $25S^2$의 값 계산하기',
              'title_en': '💎 Step 8 · [Final Synthesis] Computing $25S^2$',
              'knowledge': '$S = \\dfrac{8\\sqrt{10}}{5}$를 제곱하면 $S^2 = \\dfrac{64 \\times 10}{25} = '
                           '\\dfrac{640}{25}$이므로, 여기에 $25$를 곱하면 분모가 깔끔하게 약분됩니다!',
              'knowledge_en': 'Squaring $S = \\dfrac{8\\sqrt{10}}{5}$ gives $S^2 = \\dfrac{640}{25}$, so $25S^2 = '
                              '640$.',
              'questions': [{'level_label': '최종 종합 디딤돌 8',
                             'level_label_en': 'Final Synthesis Step 8',
                             'stem': '$S = \\dfrac{8\\sqrt{10}}{5}$일 때, $25S^2$의 값은?',
                             'stem_en': 'Given $S = \\dfrac{8\\sqrt{10}}{5}$, what is $25S^2$?',
                             'options': ['$480$', '$540$', '$600$', '$640$', '$720$'],
                             'answer': 4,
                             'exp': '$25 \\times \\dfrac{64 \\times 10}{25} = 640$입니다.',
                             'exp_en': '$25S^2 = 640$.'}]}],
  'final': {'stem': '그림과 같이 $\\overline{\\mathrm{AB}} = 6, \\overline{\\mathrm{AD}} = 6, \\overline{\\mathrm{AE}} = '
                    '3$인 직육면체 $\\mathrm{ABCD-EFGH}$가 있다. 선분 $\\mathrm{AB}$를 $2:1$로 내분하는 점을 $\\mathrm{P}$, 선분 '
                    '$\\mathrm{AD}$를 $1:2$로 내분하는 점을 $\\mathrm{Q}$라 하자. 선분 $\\mathrm{EH}$ 위의 점 $\\mathrm{R}$과 선분 '
                    '$\\mathrm{FG}$ 위의 점 $\\mathrm{S}$에 대하여 두 직선 $\\mathrm{RS}, \\mathrm{EF}$는 서로 평행하다. 삼각형 '
                    '$\\mathrm{QRS}$의 넓이가 $3\\sqrt{10}$이고 $\\overline{\\mathrm{ER}} < 2$일 때, 삼각형 $\\mathrm{ARP}$의 평면 '
                    '$\\mathrm{QRS}$ 위로의 정사영의 넓이를 $S$라 하자. $25S^2$의 값을 구하시오. [4점]',
            'stem_en': 'In rectangular box $\\mathrm{ABCD-EFGH}$ with $\\overline{\\mathrm{AB}} = 6, '
                       '\\overline{\\mathrm{AD}} = 6, \\overline{\\mathrm{AE}} = 3$, point $\\mathrm{P}$ divides '
                       '$\\mathrm{AB}$ internally in $2:1$ and $\\mathrm{Q}$ divides $\\mathrm{AD}$ internally in '
                       '$1:2$. Points $\\mathrm{R}$ on $\\mathrm{EH}$ and $\\mathrm{S}$ on $\\mathrm{FG}$ satisfy '
                       '$\\mathrm{RS} \\parallel \\mathrm{EF}$. Given $\\text{Area}(\\triangle\\mathrm{QRS}) = '
                       '3\\sqrt{10}$ and $\\overline{\\mathrm{ER}} < 2$, let $S$ be the area of the orthogonal '
                       'projection of $\\triangle\\mathrm{ARP}$ onto plane $\\mathrm{QRS}$. Find $25S^2$. [4 points]',
            'options': ['$480$', '$540$', '$600$', '$640$', '$720$'],
            'answer': 4,
            'exp': '$\\overline{\\mathrm{AP}} = 4, \\overline{\\mathrm{AQ}} = 2$이고 '
                   '$\\text{Area}(\\triangle\\mathrm{QRS}) = \\dfrac{1}{2} \\times 6 \\times '
                   '\\sqrt{(2-\\overline{\\mathrm{ER}})^2+9} = 3\\sqrt{10}$에서 $\\overline{\\mathrm{ER}} = 1$입니다. 두 평면 '
                   '$\\mathrm{ARP}$와 $\\mathrm{QRS}$가 이루는 각 $\\theta = \\angle\\mathrm{ARQ}$에 대하여 $\\cos\\theta = '
                   '\\dfrac{4}{5}$이고 $\\text{Area}(\\triangle\\mathrm{ARP}) = 2\\sqrt{10}$이므로 $S = '
                   '\\dfrac{8\\sqrt{10}}{5},\\ 25S^2 = 640$입니다.',
            'exp_en': 'From $\\overline{\\mathrm{AP}} = 4, \\overline{\\mathrm{AQ}} = 2$ and '
                      '$\\text{Area}(\\triangle\\mathrm{QRS}) = 3\\sqrt{10}$, we find $\\overline{\\mathrm{ER}} = 1$. '
                      'The dihedral angle $\\theta = \\angle\\mathrm{ARQ}$ satisfies $\\cos\\theta = \\dfrac{4}{5}$ '
                      'and $\\text{Area}(\\triangle\\mathrm{ARP}) = 2\\sqrt{10}$, giving $S = \\dfrac{8\\sqrt{10}}{5}$ '
                      'and $25S^2 = 640$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>직육면체에서 직선과 평면의 수직 관계 및 두 평면이 이루는 이면각을 통한 정사영의 넓이</b>를 구하는 공간도형 4점 문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 삼각형 $\\mathrm{QRS}$의 넓이로 $\\overline{\\mathrm{ER}} = 1$ 결정</b><br>\n'
                        '  내분비로부터 $\\overline{\\mathrm{AP}} = 4, \\overline{\\mathrm{AQ}} = 2$입니다. $\\mathrm{RS} '
                        '\\parallel \\mathrm{EF}$이고 $\\mathrm{EF} \\perp (\\text{평면 }\\mathrm{AEHD})$이므로 $\\mathrm{RS} '
                        '\\perp \\mathrm{QR}$입니다.<br>\n'
                        '  $\\overline{\\mathrm{ER}} = r$ ($r < 2$)이라 하면 $\\overline{\\mathrm{QR}} = \\sqrt{(2-r)^2 + '
                        '3^2}$이므로:<br>\n'
                        '  $$\\text{Area}(\\triangle\\mathrm{QRS}) = \\frac{1}{2} \\times 6 \\times \\sqrt{(2-r)^2 + '
                        '9} = 3\\sqrt{10} \\implies (2-r)^2 = 1 \\implies r = 1$$<br>\n'
                        '  <b>2단계: 두 평면 $\\mathrm{ARP}$와 $\\mathrm{QRS}$가 이루는 각 $\\theta$ 구하기</b><br>\n'
                        '  두 평면 모두 모서리 $\\mathrm{EF}$에 평행하므로 옆면 $\\mathrm{AEHD}$에 수직입니다. 따라서 이면각 $\\theta$는 옆면 '
                        '$\\mathrm{AEHD}$ 위의 두 벡터 $\\overrightarrow{\\mathrm{RA}} = (-1, 3)$과 '
                        '$\\overrightarrow{\\mathrm{RQ}} = (1, 3)$이 이루는 각 $\\angle\\mathrm{ARQ}$와 같습니다:<br>\n'
                        '  $$\\cos\\theta = \\frac{(-1)(1) + 3(3)}{\\sqrt{10}\\sqrt{10}} = \\frac{8}{10} = '
                        '\\frac{4}{5}$$<br>\n'
                        '  <b>3단계: 정사영의 넓이 $S$와 $25S^2$ 계산</b><br>\n'
                        '  $\\mathrm{AP} \\perp \\mathrm{AR}$이고 $\\overline{\\mathrm{AP}} = 4, '
                        '\\overline{\\mathrm{AR}} = \\sqrt{10}$이므로 $\\text{Area}(\\triangle\\mathrm{ARP}) = '
                        '\\dfrac{1}{2} \\times 4 \\times \\sqrt{10} = 2\\sqrt{10}$입니다.<br>\n'
                        '  $$S = \\text{Area}(\\triangle\\mathrm{ARP})\\cos\\theta = 2\\sqrt{10} \\times \\frac{4}{5} '
                        '= \\frac{8\\sqrt{10}}{5} \\implies 25S^2 = 640$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 구하는 값은 <b>$640$</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem computes the <b>orthogonal projection area</b> between two planes '
                           '$\\mathrm{ARP}$ and $\\mathrm{QRS}$ that are both perpendicular to face $\\mathrm{AEHD}$ '
                           'of the rectangular box.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Determine $\\overline{\\mathrm{ER}} = 1$</b><br>\n'
                           '  $$\\text{Area}(\\triangle\\mathrm{QRS}) = \\frac{1}{2}(6)\\sqrt{(2-r)^2 + 9} = '
                           '3\\sqrt{10} \\implies r = \\overline{\\mathrm{ER}} = 1$$<br>\n'
                           '  <b>Step 2: Dihedral angle and projected area</b><br>\n'
                           '  In face $\\mathrm{AEHD}$, $\\overrightarrow{\\mathrm{RA}} = (-1, 3)$ and '
                           '$\\overrightarrow{\\mathrm{RQ}} = (1, 3)$ give $\\cos\\theta = \\frac{8}{10} = '
                           '\\frac{4}{5}$.<br>\n'
                           '  Since $\\text{Area}(\\triangle\\mathrm{ARP}) = \\frac{1}{2}(4)\\sqrt{10} = 2\\sqrt{10}$, '
                           'we obtain $S = \\frac{8\\sqrt{10}}{5}$ and $25S^2 = 640$.\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  The final answer is <b>$640$</b>.\n'
                           '</p>'}},
 {'slug': 'c2610g30',
  'qNum': '기하 30',
  'subject': '기하',
  'title': '[2026학년도 10월 고3 기하 30번] 평면벡터의 내분점과 내적 등식의 기하학적 해석',
  'title_en': '[2026 AY Oct Exam Grade 12 Geometry #30] Internal Division of Plane Vectors and Geometric '
              'Interpretation of Dot Product',
  'summary_ko': '$5\\overrightarrow{\\mathrm{BP}}=2\\overrightarrow{\\mathrm{BA}}+3\\overrightarrow{\\mathrm{BC}}$에서 점 '
                '$\\mathrm{P}$가 $\\mathrm{AC}$를 $3:2$로 내분함을 찾고, '
                '$\\overrightarrow{\\mathrm{AP}}\\cdot\\overrightarrow{\\mathrm{PQ}}=\\overrightarrow{\\mathrm{CP}}\\cdot\\overrightarrow{\\mathrm{PB}}$에서 '
                '$\\overrightarrow{\\mathrm{PQ}}=\\dfrac{2}{3}\\overrightarrow{\\mathrm{BP}}$와 '
                '$\\overrightarrow{\\mathrm{AB}}\\cdot\\overrightarrow{\\mathrm{AC}}=1$을 구하여 '
                '$\\overrightarrow{\\mathrm{AQ}}\\cdot\\overrightarrow{\\mathrm{BC}}=\\dfrac{40}{3}$ 도출하기',
  'summary_en': 'From '
                '$5\\overrightarrow{\\mathrm{BP}}=2\\overrightarrow{\\mathrm{BA}}+3\\overrightarrow{\\mathrm{BC}}$ '
                'deduce $\\mathrm{P}$ divides $\\mathrm{AC}$ in $3:2$, from '
                '$\\overrightarrow{\\mathrm{AP}}\\cdot\\overrightarrow{\\mathrm{PQ}}=\\overrightarrow{\\mathrm{CP}}\\cdot\\overrightarrow{\\mathrm{PB}}$ '
                'find $\\overrightarrow{\\mathrm{PQ}}=\\dfrac{2}{3}\\overrightarrow{\\mathrm{BP}}$ and '
                '$\\overrightarrow{\\mathrm{AB}}\\cdot\\overrightarrow{\\mathrm{AC}}=1$, and compute '
                '$\\overrightarrow{\\mathrm{AQ}}\\cdot\\overrightarrow{\\mathrm{BC}}=\\dfrac{40}{3}$ ($p+q=43$).',
  'tags': ['기하', '평면벡터', '위치벡터', '내분점', '벡터의내적', '단답형', '30번'],
  'symbols': [{'sym': '$\\overrightarrow{\\mathrm{BP}} = \\dfrac{2\\overrightarrow{\\mathrm{BA}} + '
                      '3\\overrightarrow{\\mathrm{BC}}}{2+3}$',
               'desc': '점 $\\mathrm{P}$가 선분 $\\mathrm{AC}$를 $3:2$로 내분하는 점임을 뜻하는 위치벡터 공식',
               'desc_en': 'Position vector formula showing $\\mathrm{P}$ divides segment $\\mathrm{AC}$ internally in '
                          '$3:2$.'},
              {'sym': '$\\overrightarrow{\\mathrm{AP}}\\cdot\\overrightarrow{\\mathrm{PQ}} = '
                      '\\overrightarrow{\\mathrm{CP}}\\cdot\\overrightarrow{\\mathrm{PB}} \\implies '
                      '\\overrightarrow{\\mathrm{PQ}} = \\dfrac{2}{3}\\overrightarrow{\\mathrm{BP}}$',
               'desc': '$\\overrightarrow{\\mathrm{CP}} = -\\dfrac{2}{3}\\overrightarrow{\\mathrm{AP}}$를 대입하고 '
                       '$\\overrightarrow{\\mathrm{AP}}\\cdot\\overrightarrow{\\mathrm{BP}} > 0$으로 나누어 얻는 선분 비',
               'desc_en': 'Substituting $\\overrightarrow{\\mathrm{CP}} = '
                          '-\\dfrac{2}{3}\\overrightarrow{\\mathrm{AP}}$ yields $\\overrightarrow{\\mathrm{PQ}} = '
                          '\\dfrac{2}{3}\\overrightarrow{\\mathrm{BP}}$.'},
              {'sym': '$\\overrightarrow{\\mathrm{AQ}} = \\overrightarrow{\\mathrm{AC}} - '
                      '\\dfrac{2}{3}\\overrightarrow{\\mathrm{AB}}$',
               'desc': '시점을 $\\mathrm{A}$로 통일하여 나타낸 벡터 $\\overrightarrow{\\mathrm{AQ}}$',
               'desc_en': 'Vector $\\overrightarrow{\\mathrm{AQ}}$ expressed with initial point $\\mathrm{A}$.'}],
  'levels': [{'title': '🔰 1단계 · [초등 비례배분과 내분점] $5\\overrightarrow{\\mathrm{BP}} = 2\\overrightarrow{\\mathrm{BA}} + '
                       '3\\overrightarrow{\\mathrm{BC}}$에서 점 $\\mathrm{P}$의 위치 찾기',
              'title_en': '🔰 Step 1 · [Internal Division Formula] Locating point $\\mathrm{P}$ from '
                          '$5\\overrightarrow{\\mathrm{BP}} = 2\\overrightarrow{\\mathrm{BA}} + '
                          '3\\overrightarrow{\\mathrm{BC}}$',
              'knowledge': '첫 번째 조건 $5\\overrightarrow{\\mathrm{BP}} = 2\\overrightarrow{\\mathrm{BA}} + '
                           '3\\overrightarrow{\\mathrm{BC}}$의 양변을 $5$로 나누면 $\\overrightarrow{\\mathrm{BP}} = '
                           '\\dfrac{2\\overrightarrow{\\mathrm{BA}} + 3\\overrightarrow{\\mathrm{BC}}}{3 + 2}$입니다! 내분점 '
                           '위치벡터 공식에서 대각선으로 곱해지므로 점 $\\mathrm{P}$는 선분 $\\mathrm{AC}$를 $3 : 2$로 내분하는 점입니다.',
              'knowledge_en': 'Dividing $5\\overrightarrow{\\mathrm{BP}} = 2\\overrightarrow{\\mathrm{BA}} + '
                              '3\\overrightarrow{\\mathrm{BC}}$ by $5$ gives $\\overrightarrow{\\mathrm{BP}} = '
                              '\\dfrac{2\\overrightarrow{\\mathrm{BA}} + 3\\overrightarrow{\\mathrm{BC}}}{3 + 2}$, '
                              'meaning $\\mathrm{P}$ divides $\\mathrm{AC}$ internally in the ratio $3:2$.',
              'questions': [{'level_label': '초등 비례배분과 내분비 디딤돌 1',
                             'level_label_en': 'Elementary Internal Division Step 1',
                             'stem': '초등학교 비례배분 원리에 따라 점 $\\mathrm{P}$가 선분 $\\mathrm{AC}$를 $3 : 2$로 내분하는 점일 때, '
                                     '$\\overrightarrow{\\mathrm{AP}}$는 $\\overrightarrow{\\mathrm{AC}}$의 몇 배인가요?',
                             'stem_en': 'Using elementary proportional division, since $\\mathrm{P}$ divides '
                                        '$\\mathrm{AC}$ internally in the ratio $3:2$, what multiple of '
                                        '$\\overrightarrow{\\mathrm{AC}}$ is $\\overrightarrow{\\mathrm{AP}}$?',
                             'options': ['$\\dfrac{1}{5}\\overrightarrow{\\mathrm{AC}}$',
                                         '$\\dfrac{2}{5}\\overrightarrow{\\mathrm{AC}}$',
                                         '$\\dfrac{1}{2}\\overrightarrow{\\mathrm{AC}}$',
                                         '$\\dfrac{3}{5}\\overrightarrow{\\mathrm{AC}}$',
                                         '$\\dfrac{2}{3}\\overrightarrow{\\mathrm{AC}}$'],
                             'answer': 4,
                             'exp': '전체 $3 + 2 = 5$칸 중 $3$칸이므로 $\\overrightarrow{\\mathrm{AP}} = '
                                    '\\dfrac{3}{5}\\overrightarrow{\\mathrm{AC}}$입니다.',
                             'exp_en': '$\\overrightarrow{\\mathrm{AP}} = '
                                       '\\dfrac{3}{5}\\overrightarrow{\\mathrm{AC}}$.'}]},
             {'title': '🌿 2단계 · [내적 등식 해석] $\\overrightarrow{\\mathrm{AP}}\\cdot\\overrightarrow{\\mathrm{PQ}} = '
                       '\\overrightarrow{\\mathrm{CP}}\\cdot\\overrightarrow{\\mathrm{PB}}$에서 '
                       '$\\overrightarrow{\\mathrm{PQ}}$와 $\\overrightarrow{\\mathrm{BP}}$의 비율 찾기',
              'title_en': '🌿 Step 2 · [Dot Product Equation] Finding the ratio between '
                          '$\\overrightarrow{\\mathrm{PQ}}$ and $\\overrightarrow{\\mathrm{BP}}$',
              'knowledge': '1단계에서 $\\overline{\\mathrm{AP}} : \\overline{\\mathrm{PC}} = 3 : 2$이고 '
                           '$\\overrightarrow{\\mathrm{CP}}$는 $\\overrightarrow{\\mathrm{AP}}$와 반대 방향이므로 '
                           '$\\overrightarrow{\\mathrm{CP}} = -\\dfrac{2}{3}\\overrightarrow{\\mathrm{AP}}$입니다. 또한 '
                           '$\\overrightarrow{\\mathrm{PB}} = -\\overrightarrow{\\mathrm{BP}}$이므로 우변은 '
                           '$\\overrightarrow{\\mathrm{CP}}\\cdot\\overrightarrow{\\mathrm{PB}} = '
                           '\\left(-\\dfrac{2}{3}\\overrightarrow{\\mathrm{AP}}\\right)\\cdot(-\\overrightarrow{\\mathrm{BP}}) '
                           '= \\dfrac{2}{3}(\\overrightarrow{\\mathrm{AP}}\\cdot\\overrightarrow{\\mathrm{BP}})$가 됩니다!',
              'knowledge_en': 'Since $\\overrightarrow{\\mathrm{CP}} = -\\dfrac{2}{3}\\overrightarrow{\\mathrm{AP}}$ '
                              'and $\\overrightarrow{\\mathrm{PB}} = -\\overrightarrow{\\mathrm{BP}}$, the right-hand '
                              'side becomes $\\overrightarrow{\\mathrm{CP}}\\cdot\\overrightarrow{\\mathrm{PB}} = '
                              '\\dfrac{2}{3}(\\overrightarrow{\\mathrm{AP}}\\cdot\\overrightarrow{\\mathrm{BP}})$.',
              'questions': [{'level_label': '직선 BP 위의 점 Q 디딤돌 2',
                             'level_label_en': 'Point Q on Line BP Step 2',
                             'stem': '직선 $\\mathrm{BP}$ 위의 점 $\\mathrm{Q}$에 대하여 $\\overrightarrow{\\mathrm{PQ}} = '
                                     'k\\overrightarrow{\\mathrm{BP}}$라 할 때, '
                                     '$k(\\overrightarrow{\\mathrm{AP}}\\cdot\\overrightarrow{\\mathrm{BP}}) = '
                                     '\\dfrac{2}{3}(\\overrightarrow{\\mathrm{AP}}\\cdot\\overrightarrow{\\mathrm{BP}})$와 '
                                     '$\\overrightarrow{\\mathrm{AP}}\\cdot\\overrightarrow{\\mathrm{BP}} > 0$에서 상수 '
                                     '$k$의 값은?',
                             'stem_en': 'Writing $\\overrightarrow{\\mathrm{PQ}} = k\\overrightarrow{\\mathrm{BP}}$ on '
                                        'line $\\mathrm{BP}$, what is $k$ from '
                                        '$k(\\overrightarrow{\\mathrm{AP}}\\cdot\\overrightarrow{\\mathrm{BP}}) = '
                                        '\\dfrac{2}{3}(\\overrightarrow{\\mathrm{AP}}\\cdot\\overrightarrow{\\mathrm{BP}})$ '
                                        '($\\overrightarrow{\\mathrm{AP}}\\cdot\\overrightarrow{\\mathrm{BP}} > 0$)?',
                             'options': ['$\\dfrac{1}{3}$',
                                         '$\\dfrac{1}{2}$',
                                         '$\\dfrac{2}{3}$',
                                         '$\\dfrac{3}{2}$',
                                         '$2$'],
                             'answer': 3,
                             'exp': '$\\overrightarrow{\\mathrm{AP}}\\cdot\\overrightarrow{\\mathrm{BP}} > 0$으로 양변을 '
                                    '나누면 $k = \\dfrac{2}{3}$, 즉 $\\overrightarrow{\\mathrm{PQ}} = '
                                    '\\dfrac{2}{3}\\overrightarrow{\\mathrm{BP}}$입니다!',
                             'exp_en': '$k = \\dfrac{2}{3}$, so $\\overrightarrow{\\mathrm{PQ}} = '
                                       '\\dfrac{2}{3}\\overrightarrow{\\mathrm{BP}}$.'}]},
             {'title': '🌱 3단계 · [삼각형 넓이 비] $\\text{Area}(\\triangle\\mathrm{APQ}) = \\dfrac{4\\sqrt{5}}{5}$로부터 '
                       '$\\text{Area}(\\triangle\\mathrm{ABC})$ 구하기',
              'title_en': '🌱 Step 3 · [Triangle Area Ratios] Finding $\\text{Area}(\\triangle\\mathrm{ABC})$ from '
                          '$\\text{Area}(\\triangle\\mathrm{APQ}) = \\dfrac{4\\sqrt{5}}{5}$',
              'knowledge': '높이가 같은 삼각형들의 넓이는 밑변의 길이에 비례합니다! $\\overline{\\mathrm{BP}} : \\overline{\\mathrm{PQ}} = 3 : '
                           '2$이므로 $\\text{Area}(\\triangle\\mathrm{ABP}) = '
                           '\\dfrac{3}{2}\\text{Area}(\\triangle\\mathrm{APQ})$이고, 다시 $\\overline{\\mathrm{AC}} : '
                           '\\overline{\\mathrm{AP}} = 5 : 3$이므로 $\\text{Area}(\\triangle\\mathrm{ABC}) = '
                           '\\dfrac{5}{3}\\text{Area}(\\triangle\\mathrm{ABP})$입니다.',
              'knowledge_en': 'Using base ratios, $\\text{Area}(\\triangle\\mathrm{ABP}) = '
                              '\\dfrac{3}{2}\\text{Area}(\\triangle\\mathrm{APQ})$ and '
                              '$\\text{Area}(\\triangle\\mathrm{ABC}) = '
                              '\\dfrac{5}{3}\\text{Area}(\\triangle\\mathrm{ABP})$.',
              'questions': [{'level_label': '삼각형 ABC 넓이 디딤돌 3',
                             'level_label_en': 'Area of ABC Step 3',
                             'stem': '$\\text{Area}(\\triangle\\mathrm{APQ}) = \\dfrac{4\\sqrt{5}}{5}$일 때, '
                                     '$\\text{Area}(\\triangle\\mathrm{ABC}) = \\dfrac{5}{3} \\times \\dfrac{3}{2} '
                                     '\\times \\dfrac{4\\sqrt{5}}{5}$를 계산한 값은?',
                             'stem_en': 'What is $\\text{Area}(\\triangle\\mathrm{ABC}) = \\dfrac{5}{3} \\times '
                                        '\\dfrac{3}{2} \\times \\dfrac{4\\sqrt{5}}{5}$?',
                             'options': ['$\\sqrt{5}$',
                                         '$\\dfrac{3\\sqrt{5}}{2}$',
                                         '$2\\sqrt{5}$',
                                         '$\\dfrac{5\\sqrt{5}}{2}$',
                                         '$3\\sqrt{5}$'],
                             'answer': 3,
                             'exp': '$\\dfrac{5}{2} \\times \\dfrac{4\\sqrt{5}}{5} = 2\\sqrt{5}$입니다.',
                             'exp_en': '$\\text{Area}(\\triangle\\mathrm{ABC}) = 2\\sqrt{5}$.'}]},
             {'title': '🌳 4단계 · [삼각비 $\\sin A$와 $\\cos A$] $\\overline{\\mathrm{AB}} = \\overline{\\mathrm{AC}} = 3$과 '
                       '넓이 $2\\sqrt{5}$에서 $\\cos A$ 구하기',
              'title_en': '🌳 Step 4 · [Finding $\\sin A$ and $\\cos A$] Computing $\\cos A$ from '
                          '$\\overline{\\mathrm{AB}} = \\overline{\\mathrm{AC}} = 3$ and area $2\\sqrt{5}$',
              'knowledge': '두 변의 길이가 $\\overline{\\mathrm{AB}} = \\overline{\\mathrm{AC}} = 3$인 삼각형 $\\mathrm{ABC}$의 '
                           '넓이는 $\\dfrac{1}{2} \\times 3 \\times 3 \\times \\sin A = \\dfrac{9}{2}\\sin A = '
                           '2\\sqrt{5}$이므로 $\\sin A = \\dfrac{4\\sqrt{5}}{9}$입니다. $\\triangle\\mathrm{ABC}$는 예각삼각형이므로 '
                           '$\\cos A > 0$입니다!',
              'knowledge_en': 'From $\\dfrac{1}{2}(3)(3)\\sin A = 2\\sqrt{5}$, we get $\\sin A = '
                              '\\dfrac{4\\sqrt{5}}{9}$. Since $\\angle A$ is acute, $\\cos A = \\sqrt{1 - \\sin^2 A}$.',
              'questions': [{'level_label': '코사인 $\\cos A$ 계산 디딤돌 4',
                             'level_label_en': 'Finding $\\cos A$ Step 4',
                             'stem': '예각 $A$에 대하여 $\\sin A = \\dfrac{4\\sqrt{5}}{9}$일 때, $\\cos A = \\sqrt{1 - '
                                     '\\left(\\dfrac{4\\sqrt{5}}{9}\\right)^2} = \\sqrt{1 - \\dfrac{80}{81}}$의 값은?',
                             'stem_en': 'For acute angle $A$ with $\\sin A = \\dfrac{4\\sqrt{5}}{9}$, what is $\\cos A '
                                        '= \\sqrt{1 - \\dfrac{80}{81}}$?',
                             'options': ['$\\dfrac{1}{9}$',
                                         '$\\dfrac{2}{9}$',
                                         '$\\dfrac{1}{3}$',
                                         '$\\dfrac{4}{9}$',
                                         '$\\dfrac{5}{9}$'],
                             'answer': 1,
                             'exp': '$\\sqrt{\\dfrac{1}{81}} = \\dfrac{1}{9}$입니다.',
                             'exp_en': '$\\cos A = \\dfrac{1}{9}$.'}]},
             {'title': '🏛️ 5단계 · [기본 내적 구하기] $\\overrightarrow{\\mathrm{AB}} \\cdot \\overrightarrow{\\mathrm{AC}}$의 값 '
                       '계산하기',
              'title_en': '🏛️ Step 5 · [Base Dot Product] Computing $\\overrightarrow{\\mathrm{AB}} \\cdot '
                          '\\overrightarrow{\\mathrm{AC}}$',
              'knowledge': '두 벡터 $\\overrightarrow{\\mathrm{AB}}$와 $\\overrightarrow{\\mathrm{AC}}$의 내적은 '
                           '$|\\overrightarrow{\\mathrm{AB}}||\\overrightarrow{\\mathrm{AC}}|\\cos A$입니다. '
                           '$|\\overrightarrow{\\mathrm{AB}}| = 3$, $|\\overrightarrow{\\mathrm{AC}}| = 3$, $\\cos A = '
                           '\\dfrac{1}{9}$를 대입해 봅시다.',
              'knowledge_en': 'The dot product is $\\overrightarrow{\\mathrm{AB}} \\cdot '
                              '\\overrightarrow{\\mathrm{AC}} = '
                              '|\\overrightarrow{\\mathrm{AB}}||\\overrightarrow{\\mathrm{AC}}|\\cos A$.',
              'questions': [{'level_label': '기본 내적 디딤돌 5',
                             'level_label_en': 'Base Dot Product Step 5',
                             'stem': '$|\\overrightarrow{\\mathrm{AB}}| = 3$, $|\\overrightarrow{\\mathrm{AC}}| = 3$, '
                                     '$\\cos A = \\dfrac{1}{9}$일 때, 내적 $\\overrightarrow{\\mathrm{AB}} \\cdot '
                                     '\\overrightarrow{\\mathrm{AC}}$의 값은?',
                             'stem_en': 'With $|\\overrightarrow{\\mathrm{AB}}| = |\\overrightarrow{\\mathrm{AC}}| = '
                                        '3$ and $\\cos A = \\dfrac{1}{9}$, what is $\\overrightarrow{\\mathrm{AB}} '
                                        '\\cdot \\overrightarrow{\\mathrm{AC}}$?',
                             'options': ['$0$', '$1$', '$2$', '$3$', '$9$'],
                             'answer': 2,
                             'exp': '$3 \\times 3 \\times \\dfrac{1}{9} = 1$입니다.',
                             'exp_en': '$3 \\times 3 \\times \\dfrac{1}{9} = 1$.'}]},
             {'title': '⚡ 6단계 · [시점 통일] $\\overrightarrow{\\mathrm{AQ}}$와 $\\overrightarrow{\\mathrm{BC}}$를 '
                       '$\\overrightarrow{\\mathrm{AB}}, \\overrightarrow{\\mathrm{AC}}$로 나타내기',
              'title_en': '⚡ Step 6 · [Unifying Initial Point] Expressing $\\overrightarrow{\\mathrm{AQ}}$ and '
                          '$\\overrightarrow{\\mathrm{BC}}$ in terms of $\\overrightarrow{\\mathrm{AB}}$ and '
                          '$\\overrightarrow{\\mathrm{AC}}$',
              'knowledge': '$\\overrightarrow{\\mathrm{AQ}} = \\overrightarrow{\\mathrm{AP}} + '
                           '\\overrightarrow{\\mathrm{PQ}} = \\overrightarrow{\\mathrm{AP}} + '
                           '\\dfrac{2}{3}\\overrightarrow{\\mathrm{BP}} = \\overrightarrow{\\mathrm{AP}} + '
                           '\\dfrac{2}{3}(\\overrightarrow{\\mathrm{AP}} - \\overrightarrow{\\mathrm{AB}}) = '
                           '\\dfrac{5}{3}\\overrightarrow{\\mathrm{AP}} - '
                           '\\dfrac{2}{3}\\overrightarrow{\\mathrm{AB}}$입니다. 여기에 1단계의 $\\overrightarrow{\\mathrm{AP}} '
                           '= \\dfrac{3}{5}\\overrightarrow{\\mathrm{AC}}$를 대입하면 아주 간단해집니다!',
              'knowledge_en': 'Since $\\overrightarrow{\\mathrm{AQ}} = \\overrightarrow{\\mathrm{AP}} + '
                              '\\dfrac{2}{3}(\\overrightarrow{\\mathrm{AP}} - \\overrightarrow{\\mathrm{AB}}) = '
                              '\\dfrac{5}{3}\\overrightarrow{\\mathrm{AP}} - '
                              '\\dfrac{2}{3}\\overrightarrow{\\mathrm{AB}}$ and $\\overrightarrow{\\mathrm{AP}} = '
                              '\\dfrac{3}{5}\\overrightarrow{\\mathrm{AC}}$, we can simplify '
                              '$\\overrightarrow{\\mathrm{AQ}}$.',
              'questions': [{'level_label': '벡터 AQ 정리 디딤돌 6',
                             'level_label_en': 'Simplifying Vector AQ Step 6',
                             'stem': '$\\dfrac{5}{3}\\overrightarrow{\\mathrm{AP}} - '
                                     '\\dfrac{2}{3}\\overrightarrow{\\mathrm{AB}}$에 $\\overrightarrow{\\mathrm{AP}} = '
                                     '\\dfrac{3}{5}\\overrightarrow{\\mathrm{AC}}$를 대입하여 '
                                     '$\\overrightarrow{\\mathrm{AQ}}$를 정리한 식은?',
                             'stem_en': 'Substitute $\\overrightarrow{\\mathrm{AP}} = '
                                        '\\dfrac{3}{5}\\overrightarrow{\\mathrm{AC}}$ into '
                                        '$\\overrightarrow{\\mathrm{AQ}} = \\dfrac{5}{3}\\overrightarrow{\\mathrm{AP}} '
                                        '- \\dfrac{2}{3}\\overrightarrow{\\mathrm{AB}}$.',
                             'options': ['$\\overrightarrow{\\mathrm{AC}} - '
                                         '\\dfrac{1}{3}\\overrightarrow{\\mathrm{AB}}$',
                                         '$\\overrightarrow{\\mathrm{AC}} - '
                                         '\\dfrac{2}{3}\\overrightarrow{\\mathrm{AB}}$',
                                         '$\\dfrac{3}{5}\\overrightarrow{\\mathrm{AC}} - '
                                         '\\dfrac{2}{3}\\overrightarrow{\\mathrm{AB}}$',
                                         '$\\overrightarrow{\\mathrm{AC}} + '
                                         '\\dfrac{2}{3}\\overrightarrow{\\mathrm{AB}}$',
                                         '$\\dfrac{5}{3}\\overrightarrow{\\mathrm{AC}} - '
                                         '\\dfrac{2}{3}\\overrightarrow{\\mathrm{AB}}$'],
                             'answer': 2,
                             'exp': '$\\dfrac{5}{3}\\left(\\dfrac{3}{5}\\overrightarrow{\\mathrm{AC}}\\right) - '
                                    '\\dfrac{2}{3}\\overrightarrow{\\mathrm{AB}} = \\overrightarrow{\\mathrm{AC}} - '
                                    '\\dfrac{2}{3}\\overrightarrow{\\mathrm{AB}}$입니다.',
                             'exp_en': '$\\overrightarrow{\\mathrm{AQ}} = \\overrightarrow{\\mathrm{AC}} - '
                                       '\\dfrac{2}{3}\\overrightarrow{\\mathrm{AB}}$.'}]},
             {'title': '🌟 7단계 · [내적 전개 및 계산] $\\overrightarrow{\\mathrm{AQ}} \\cdot \\overrightarrow{\\mathrm{BC}}$의 값 '
                       '$\\dfrac{q}{p}$ 구하기',
              'title_en': '🌟 Step 7 · [Expanding Dot Product] Computing $\\overrightarrow{\\mathrm{AQ}} \\cdot '
                          '\\overrightarrow{\\mathrm{BC}} = \\dfrac{q}{p}$',
              'knowledge': '$\\overrightarrow{\\mathrm{AQ}} = \\overrightarrow{\\mathrm{AC}} - '
                           '\\dfrac{2}{3}\\overrightarrow{\\mathrm{AB}}$와 $\\overrightarrow{\\mathrm{BC}} = '
                           '\\overrightarrow{\\mathrm{AC}} - \\overrightarrow{\\mathrm{AB}}$를 내적하여 분배법칙으로 전개하면 '
                           '$|\\overrightarrow{\\mathrm{AC}}|^2 - '
                           '\\dfrac{5}{3}(\\overrightarrow{\\mathrm{AB}}\\cdot\\overrightarrow{\\mathrm{AC}}) + '
                           '\\dfrac{2}{3}|\\overrightarrow{\\mathrm{AB}}|^2$이 됩니다.',
              'knowledge_en': 'Expanding $\\left(\\overrightarrow{\\mathrm{AC}} - '
                              '\\dfrac{2}{3}\\overrightarrow{\\mathrm{AB}}\\right)\\cdot(\\overrightarrow{\\mathrm{AC}} '
                              '- \\overrightarrow{\\mathrm{AB}})$ gives $|\\overrightarrow{\\mathrm{AC}}|^2 - '
                              '\\dfrac{5}{3}(\\overrightarrow{\\mathrm{AB}}\\cdot\\overrightarrow{\\mathrm{AC}}) + '
                              '\\dfrac{2}{3}|\\overrightarrow{\\mathrm{AB}}|^2$.',
              'questions': [{'level_label': '내적 값 대입 디딤돌 7',
                             'level_label_en': 'Evaluating Dot Product Step 7',
                             'stem': '$|\\overrightarrow{\\mathrm{AB}}|^2 = |\\overrightarrow{\\mathrm{AC}}|^2 = 9$이고 '
                                     '$\\overrightarrow{\\mathrm{AB}}\\cdot\\overrightarrow{\\mathrm{AC}} = 1$일 때, $9 '
                                     '- \\dfrac{5}{3}(1) + \\dfrac{2}{3}(9) = 15 - \\dfrac{5}{3}$을 계산한 기약분수 '
                                     '$\\dfrac{q}{p}$는?',
                             'stem_en': 'With $|\\overrightarrow{\\mathrm{AB}}|^2 = |\\overrightarrow{\\mathrm{AC}}|^2 '
                                        '= 9$ and $\\overrightarrow{\\mathrm{AB}}\\cdot\\overrightarrow{\\mathrm{AC}} '
                                        '= 1$, what is $9 - \\dfrac{5}{3}(1) + \\dfrac{2}{3}(9) = 15 - \\dfrac{5}{3}$?',
                             'options': ['$\\dfrac{35}{3}$',
                                         '$\\dfrac{38}{3}$',
                                         '$\\dfrac{40}{3}$',
                                         '$\\dfrac{43}{3}$',
                                         '$\\dfrac{46}{3}$'],
                             'answer': 3,
                             'exp': '$15 - \\dfrac{5}{3} = \\dfrac{45 - 5}{3} = \\dfrac{40}{3}$입니다.',
                             'exp_en': '$\\dfrac{40}{3}$.'}]},
             {'title': '💎 8단계 · [최종 종합] 서로소인 자연수 $p + q$ 구하기',
              'title_en': '💎 Step 8 · [Final Synthesis] Computing $p + q$',
              'knowledge': '$\\dfrac{q}{p} = \\dfrac{40}{3}$에서 $3$과 $40$은 서로소인 자연수이므로 $p = 3, q = 40$입니다.',
              'knowledge_en': 'From $\\dfrac{q}{p} = \\dfrac{40}{3}$ with $\\gcd(3, 40) = 1$, we have $p = 3$ and $q = '
                              '40$.',
              'questions': [{'level_label': '최종 종합 디딤돌 8',
                             'level_label_en': 'Final Synthesis Step 8',
                             'stem': '$p = 3$, $q = 40$일 때, $p + q$의 값은?',
                             'stem_en': 'Given $p = 3$ and $q = 40$, what is $p + q$?',
                             'options': ['$39$', '$41$', '$43$', '$45$', '$47$'],
                             'answer': 3,
                             'exp': '$3 + 40 = 43$입니다.',
                             'exp_en': '$3 + 40 = 43$.'}]}],
  'final': {'stem': '좌표평면에서 $\\overline{\\mathrm{AB}} = \\overline{\\mathrm{AC}} = 3$인 예각삼각형 $\\mathrm{ABC}$와 선분 '
                    '$\\mathrm{AC}$ 위의 점 $\\mathrm{P}$, 직선 $\\mathrm{BP}$ 위의 점 '
                    '$\\mathrm{Q}$가<br><br>$$5\\overrightarrow{\\mathrm{BP}} = 2\\overrightarrow{\\mathrm{BA}} + '
                    '3\\overrightarrow{\\mathrm{BC}}, \\quad '
                    '\\overrightarrow{\\mathrm{AP}}\\cdot\\overrightarrow{\\mathrm{PQ}} = '
                    '\\overrightarrow{\\mathrm{CP}}\\cdot\\overrightarrow{\\mathrm{PB}}, \\quad '
                    '\\overrightarrow{\\mathrm{AP}}\\cdot\\overrightarrow{\\mathrm{BP}} > 0$$<br>을 만족시킨다. 삼각형 '
                    '$\\mathrm{APQ}$의 넓이가 $\\dfrac{4\\sqrt{5}}{5}$일 때, $\\overrightarrow{\\mathrm{AQ}} \\cdot '
                    '\\overrightarrow{\\mathrm{BC}} = \\dfrac{q}{p}$이다. $p + q$의 값을 구하시오. (단, $p$와 $q$는 서로소인 자연수이다.) '
                    '[4점]',
            'stem_en': 'In the coordinate plane, an acute isosceles triangle $\\mathrm{ABC}$ with '
                       '$\\overline{\\mathrm{AB}} = \\overline{\\mathrm{AC}} = 3$, a point $\\mathrm{P}$ on segment '
                       '$\\mathrm{AC}$, and a point $\\mathrm{Q}$ on line $\\mathrm{BP}$ '
                       'satisfy<br><br>$$5\\overrightarrow{\\mathrm{BP}} = 2\\overrightarrow{\\mathrm{BA}} + '
                       '3\\overrightarrow{\\mathrm{BC}}, \\quad '
                       '\\overrightarrow{\\mathrm{AP}}\\cdot\\overrightarrow{\\mathrm{PQ}} = '
                       '\\overrightarrow{\\mathrm{CP}}\\cdot\\overrightarrow{\\mathrm{PB}}, \\quad '
                       '\\overrightarrow{\\mathrm{AP}}\\cdot\\overrightarrow{\\mathrm{BP}} > 0.$$<br>When '
                       '$\\text{Area}(\\triangle\\mathrm{APQ}) = \\dfrac{4\\sqrt{5}}{5}$, let '
                       '$\\overrightarrow{\\mathrm{AQ}} \\cdot \\overrightarrow{\\mathrm{BC}} = \\dfrac{q}{p}$ in '
                       'lowest terms. Find $p + q$. [4 points]',
            'options': ['$39$', '$41$', '$43$', '$45$', '$47$'],
            'answer': 3,
            'exp': '점 $\\mathrm{P}$는 선분 $\\mathrm{AC}$를 $3:2$로 내분하고 $\\overrightarrow{\\mathrm{PQ}} = '
                   '\\dfrac{2}{3}\\overrightarrow{\\mathrm{BP}}$이므로 $\\text{Area}(\\triangle\\mathrm{ABC}) = '
                   '2\\sqrt{5} \\implies \\cos A = \\dfrac{1}{9} \\implies '
                   '\\overrightarrow{\\mathrm{AB}}\\cdot\\overrightarrow{\\mathrm{AC}} = 1$입니다. '
                   '$\\overrightarrow{\\mathrm{AQ}} = \\overrightarrow{\\mathrm{AC}} - '
                   '\\dfrac{2}{3}\\overrightarrow{\\mathrm{AB}}$이므로 '
                   '$\\overrightarrow{\\mathrm{AQ}}\\cdot\\overrightarrow{\\mathrm{BC}} = \\dfrac{40}{3}$이고 $p + q = '
                   '43$입니다.',
            'exp_en': 'Point $\\mathrm{P}$ divides $\\mathrm{AC}$ in $3:2$ and $\\overrightarrow{\\mathrm{PQ}} = '
                      '\\dfrac{2}{3}\\overrightarrow{\\mathrm{BP}}$, so $\\text{Area}(\\triangle\\mathrm{ABC}) = '
                      '2\\sqrt{5} \\implies \\cos A = \\dfrac{1}{9} \\implies '
                      '\\overrightarrow{\\mathrm{AB}}\\cdot\\overrightarrow{\\mathrm{AC}} = 1$. Since '
                      '$\\overrightarrow{\\mathrm{AQ}} = \\overrightarrow{\\mathrm{AC}} - '
                      '\\dfrac{2}{3}\\overrightarrow{\\mathrm{AB}}$, we get '
                      '$\\overrightarrow{\\mathrm{AQ}}\\cdot\\overrightarrow{\\mathrm{BC}} = \\dfrac{40}{3}$ and $p + '
                      'q = 43$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>선분의 내분점 위치벡터와 내적 등식을 기하학적으로 해석하여 삼각형의 넓이 비와 시점 통일</b>을 수행하는 기하 30번 킬러 문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 점 $\\mathrm{P}, \\mathrm{Q}$의 위치 관계 파악</b><br>\n'
                        '  $5\\overrightarrow{\\mathrm{BP}} = 2\\overrightarrow{\\mathrm{BA}} + '
                        '3\\overrightarrow{\\mathrm{BC}} \\implies \\overrightarrow{\\mathrm{BP}} = '
                        '\\dfrac{2\\overrightarrow{\\mathrm{BA}} + 3\\overrightarrow{\\mathrm{BC}}}{3 + 2}$이므로 점 '
                        '$\\mathrm{P}$는 선분 $\\mathrm{AC}$를 $3 : 2$로 내분하는 점입니다 ($\\overrightarrow{\\mathrm{AP}} = '
                        '\\dfrac{3}{5}\\overrightarrow{\\mathrm{AC}}, \\overrightarrow{\\mathrm{CP}} = '
                        '-\\dfrac{2}{3}\\overrightarrow{\\mathrm{AP}}$).<br>\n'
                        '  또한 직선 $\\mathrm{BP}$ 위의 점 $\\mathrm{Q}$에 대하여 $\\overrightarrow{\\mathrm{PQ}} = '
                        'k\\overrightarrow{\\mathrm{BP}}$라 하면:<br>\n'
                        '  $$\\overrightarrow{\\mathrm{AP}}\\cdot\\overrightarrow{\\mathrm{PQ}} = '
                        '\\overrightarrow{\\mathrm{CP}}\\cdot\\overrightarrow{\\mathrm{PB}} \\implies '
                        'k(\\overrightarrow{\\mathrm{AP}}\\cdot\\overrightarrow{\\mathrm{BP}}) = '
                        '\\left(-\\frac{2}{3}\\overrightarrow{\\mathrm{AP}}\\right)\\cdot(-\\overrightarrow{\\mathrm{BP}}) '
                        '= \\frac{2}{3}(\\overrightarrow{\\mathrm{AP}}\\cdot\\overrightarrow{\\mathrm{BP}})$$\n'
                        '  $\\overrightarrow{\\mathrm{AP}}\\cdot\\overrightarrow{\\mathrm{BP}} > 0$이므로 $k = '
                        '\\dfrac{2}{3}$, 즉 $\\overrightarrow{\\mathrm{PQ}} = '
                        '\\dfrac{2}{3}\\overrightarrow{\\mathrm{BP}}$입니다.<br><br>\n'
                        '  <b>2단계: 삼각형의 넓이 비로 $\\overrightarrow{\\mathrm{AB}} \\cdot \\overrightarrow{\\mathrm{AC}} = '
                        '1$ 도출</b><br>\n'
                        '  $$\\text{Area}(\\triangle\\mathrm{ABC}) = \\frac{5}{3}\\text{Area}(\\triangle\\mathrm{ABP}) '
                        '= \\frac{5}{3} \\times \\frac{3}{2}\\text{Area}(\\triangle\\mathrm{APQ}) = \\frac{5}{2} '
                        '\\times \\frac{4\\sqrt{5}}{5} = 2\\sqrt{5}$$\n'
                        '  $$\\frac{1}{2} \\times 3 \\times 3 \\times \\sin A = 2\\sqrt{5} \\implies \\sin A = '
                        '\\frac{4\\sqrt{5}}{9} \\implies \\cos A = \\frac{1}{9} \\quad (\\because A\\text{는 예각})$$\n'
                        '  따라서 $\\overrightarrow{\\mathrm{AB}} \\cdot \\overrightarrow{\\mathrm{AC}} = 3 \\times 3 '
                        '\\times \\dfrac{1}{9} = 1$입니다.<br><br>\n'
                        '  <b>3단계: 시점을 $\\mathrm{A}$로 통일하여 $\\overrightarrow{\\mathrm{AQ}} \\cdot '
                        '\\overrightarrow{\\mathrm{BC}}$ 계산</b><br>\n'
                        '  $$\\overrightarrow{\\mathrm{AQ}} = \\overrightarrow{\\mathrm{AP}} + '
                        '\\frac{2}{3}\\overrightarrow{\\mathrm{BP}} = \\frac{5}{3}\\overrightarrow{\\mathrm{AP}} - '
                        '\\frac{2}{3}\\overrightarrow{\\mathrm{AB}} = \\overrightarrow{\\mathrm{AC}} - '
                        '\\frac{2}{3}\\overrightarrow{\\mathrm{AB}}$$\n'
                        '  $$\\overrightarrow{\\mathrm{AQ}} \\cdot \\overrightarrow{\\mathrm{BC}} = '
                        '\\left(\\overrightarrow{\\mathrm{AC}} - \\frac{2}{3}\\overrightarrow{\\mathrm{AB}}\\right) '
                        '\\cdot (\\overrightarrow{\\mathrm{AC}} - \\overrightarrow{\\mathrm{AB}}) = '
                        '|\\overrightarrow{\\mathrm{AC}}|^2 - '
                        '\\frac{5}{3}(\\overrightarrow{\\mathrm{AB}}\\cdot\\overrightarrow{\\mathrm{AC}}) + '
                        '\\frac{2}{3}|\\overrightarrow{\\mathrm{AB}}|^2 = 9 - \\frac{5}{3} + 6 = \\frac{40}{3}$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 $p = 3, q = 40$이므로 $p + q = 3 + 40 = \\mathbf{43}$입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem uses <b>internal division position vectors</b> and <b>dot product '
                           'identities</b> to relate triangle areas and evaluate $\\overrightarrow{\\mathrm{AQ}} '
                           '\\cdot \\overrightarrow{\\mathrm{BC}}$.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Locate $\\mathrm{P}$ and $\\mathrm{Q}$</b><br>\n'
                           '  From $5\\overrightarrow{\\mathrm{BP}} = 2\\overrightarrow{\\mathrm{BA}} + '
                           '3\\overrightarrow{\\mathrm{BC}}$, $\\mathrm{P}$ divides $\\mathrm{AC}$ internally in '
                           '$3:2$, and $\\overrightarrow{\\mathrm{AP}}\\cdot\\overrightarrow{\\mathrm{PQ}} = '
                           '\\overrightarrow{\\mathrm{CP}}\\cdot\\overrightarrow{\\mathrm{PB}}$ with '
                           '$\\overrightarrow{\\mathrm{AP}}\\cdot\\overrightarrow{\\mathrm{BP}} > 0$ gives '
                           '$\\overrightarrow{\\mathrm{PQ}} = \\frac{2}{3}\\overrightarrow{\\mathrm{BP}}$.<br><br>\n'
                           '  <b>Step 2: Find $\\overrightarrow{\\mathrm{AB}} \\cdot \\overrightarrow{\\mathrm{AC}} = '
                           '1$</b><br>\n'
                           '  $$\\text{Area}(\\triangle\\mathrm{ABC}) = \\frac{5}{3} \\cdot '
                           '\\frac{3}{2}\\text{Area}(\\triangle\\mathrm{APQ}) = 2\\sqrt{5} \\implies \\sin A = '
                           '\\frac{4\\sqrt{5}}{9} \\implies \\cos A = \\frac{1}{9}$$\n'
                           '  $$\\overrightarrow{\\mathrm{AB}} \\cdot \\overrightarrow{\\mathrm{AC}} = 3 \\times 3 '
                           '\\times \\frac{1}{9} = 1$$<br>\n'
                           '  <b>Step 3: Compute $\\overrightarrow{\\mathrm{AQ}} \\cdot '
                           '\\overrightarrow{\\mathrm{BC}}$</b><br>\n'
                           '  $$\\overrightarrow{\\mathrm{AQ}} \\cdot \\overrightarrow{\\mathrm{BC}} = '
                           '\\left(\\overrightarrow{\\mathrm{AC}} - \\frac{2}{3}\\overrightarrow{\\mathrm{AB}}\\right) '
                           '\\cdot (\\overrightarrow{\\mathrm{AC}} - \\overrightarrow{\\mathrm{AB}}) = 9 - '
                           '\\frac{5}{3}(1) + \\frac{2}{3}(9) = \\frac{40}{3}$$\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  With $p = 3$ and $q = 40$, $p + q = \\mathbf{43}$.\n'
                           '</p>'}}]
