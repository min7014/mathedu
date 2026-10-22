# -*- coding: utf-8 -*-
# Auto-upgraded with Elementary-to-Advanced Micro-Scaffolding

PART4_PROBLEMS = [{'slug': 'c2610m23',
  'qNum': '미적 23',
  'subject': '미적분',
  'title': '[2026학년도 10월 고3 미적 23번] 자연로그 함수의 극한과 계수 비 규칙',
  'title_en': '[2026 AY Oct Exam Grade 12 Calculus #23] Limit of Natural Logarithm Function and Coefficient Ratio',
  'summary_ko': '$\\lim_{x \\to 0} \\dfrac{\\ln(1+5x^2)}{2x^2}$에서 분모·분자의 $x^2$ 계수 비 $\\dfrac{5}{2}$ 구하기',
  'summary_en': 'Evaluate $\\lim_{x \\to 0} \\dfrac{\\ln(1+5x^2)}{2x^2}$ using the standard logarithmic limit to get '
                '$\\dfrac{5}{2}$.',
  'tags': ['미적분', '미분법', '지수로그함수의극한', '자연로그', '23번'],
  'symbols': [{'sym': '$\\lim_{t \\to 0} \\dfrac{\\ln(1+t)}{t} = 1$',
               'desc': '$t$가 $0$에 가까워질 때 $\\ln(1+t)$는 $t$와 거의 같아지는 극한 약속',
               'desc_en': 'Fundamental limit of the natural logarithm near 0.'},
              {'sym': '$\\dfrac{5x^2}{2x^2} = \\dfrac{5}{2}$',
               'desc': '$\\ln(1+5x^2)$을 $5x^2$으로 바꾸어 약분한 비율',
               'desc_en': 'Ratio of coefficients of $x^2$ in numerator and denominator.'}],
  'levels': [{'title': '🔰 1단계 · [초등 분수 약분] $\\dfrac{5 \\times \\square}{2 \\times \\square}$에서 똑같은 네모 지우기',
              'title_en': '🔰 Step 1 · [Elementary Fraction Cancellation] Canceling common factors in $\\dfrac{5 '
                          '\\times \\square}{2 \\times \\square}$',
              'knowledge': '초등학교 분수 약분에서 분자와 분모에 똑같이 곱해진 수($\\square = x^2$)는 지울 수 있습니다! $x$가 $0$에 아주 가까워질 때 $\\ln(1 + '
                           '5x^2)$은 $5x^2$과 거의 같아지므로 $\\frac{5x^2}{2x^2}$을 약분하는 것과 같습니다.',
              'knowledge_en': 'By elementary fraction cancellation, common factors in the numerator and denominator '
                              'cancel out. Since $\\ln(1+5x^2) \\approx 5x^2$ near $x=0$, the ratio reduces to '
                              '$\\frac{5x^2}{2x^2}$.',
              'questions': [{'level_label': '초등 분수 약분 디딤돌 1',
                             'level_label_en': 'Elementary Fraction Step 1',
                             'stem': '초등학교 분수 약분 원리에 따라 $\\frac{5 \\times x^2}{2 \\times x^2}$에서 분자·분모의 $x^2$을 약분하고 남는 '
                                     '분수는?',
                             'stem_en': 'Using elementary fraction cancellation, what remains after canceling $x^2$ in '
                                        '$\\frac{5x^2}{2x^2}$?',
                             'options': ['$\\frac{1}{2}$', '$1$', '$\\frac{3}{2}$', '$2$', '$\\frac{5}{2}$'],
                             'answer': 5,
                             'exp': '$x^2$을 약분하면 계수의 비 $\\frac{5}{2}$만 남습니다.',
                             'exp_en': 'Canceling $x^2$ leaves $\\frac{5}{2}$.'}]},
             {'title': '🌿 2단계 · [기본 공식 확인] $\\lim_{t \\to 0} \\dfrac{\\ln(1+t)}{t}$의 값',
              'title_en': '🌿 Step 2 · [Standard Limit] Value of $\\lim_{t \\to 0} \\dfrac{\\ln(1+t)}{t}$',
              'knowledge': '자연로그의 정의에 의하여 $\\lim_{t \\to 0} \\frac{\\ln(1+t)}{t} = 1$입니다.',
              'knowledge_en': 'By the definition of $e$, $\\lim_{t \\to 0} \\frac{\\ln(1+t)}{t} = 1$.',
              'questions': [{'level_label': '로그 극한 공식 디딤돌 2',
                             'level_label_en': 'Log Limit Formula Step 2',
                             'stem': '$t = 5x^2$이라 할 때, $\\lim_{x \\to 0} \\frac{\\ln(1 + 5x^2)}{5x^2}$의 극한값은?',
                             'stem_en': 'Letting $t = 5x^2$, what is $\\lim_{x \\to 0} \\frac{\\ln(1 + 5x^2)}{5x^2}$?',
                             'options': ['$0$', '$\\frac{1}{5}$', '$1$', '$2$', '$5$'],
                             'answer': 3,
                             'exp': '괄호 안의 $5x^2$과 분모의 $5x^2$이 정확히 일치하므로 극한값은 $1$입니다.',
                             'exp_en': 'Since the argument $5x^2$ matches the denominator, the limit is $1$.'}]},
             {'title': '🌱 3단계 · [식 변형] 분모 맞춰주기',
              'title_en': '🌱 Step 3 · [Algebraic Manipulation] Matching the denominator',
              'knowledge': '$\\frac{\\ln(1+5x^2)}{2x^2} = \\frac{\\ln(1+5x^2)}{5x^2} \\times \\frac{5x^2}{2x^2}$로 나누어 '
                           '쓸 수 있습니다.',
              'knowledge_en': 'Rewrite $\\frac{\\ln(1+5x^2)}{2x^2} = \\frac{\\ln(1+5x^2)}{5x^2} \\times \\frac{5}{2}$.',
              'questions': [{'level_label': '분모 맞추기 디딤돌 3',
                             'level_label_en': 'Denominator Match Step 3',
                             'stem': '$\\frac{\\ln(1+5x^2)}{2x^2} = \\frac{\\ln(1+5x^2)}{5x^2} \\times k$가 성립하도록 하는 상수 '
                                     '$k$의 값은?',
                             'stem_en': 'For $\\frac{\\ln(1+5x^2)}{2x^2} = \\frac{\\ln(1+5x^2)}{5x^2} \\times k$ to '
                                        'hold, what is $k$?',
                             'options': ['$\\frac{1}{2}$', '$\\frac{2}{5}$', '$1$', '$\\frac{5}{2}$', '$5$'],
                             'answer': 4,
                             'exp': '약분하여 원래 분모 $2x^2$이 되려면 $k = \\frac{5}{2}$여야 합니다.',
                             'exp_en': '$k = \\frac{5}{2}$.'}]},
             {'title': '🌳 4단계 · [극한 곱셈] $1 \\times \\dfrac{5}{2}$ 계산하기',
              'title_en': '🌳 Step 4 · [Limit Product] Computing $1 \\times \\dfrac{5}{2}$',
              'knowledge': '앞부분의 극한값 $1$과 뒷부분의 상수 $\\frac{5}{2}$를 곱합니다.',
              'knowledge_en': 'Multiply the limit $1$ by $\\frac{5}{2}$.',
              'questions': [{'level_label': '극한 곱셈 디딤돌 4',
                             'level_label_en': 'Limit Product Step 4',
                             'stem': '$1 \\times \\frac{5}{2}$의 값은?',
                             'stem_en': 'What is $1 \\times \\frac{5}{2}$?',
                             'options': ['$\\frac{1}{2}$', '$1$', '$\\frac{3}{2}$', '$2$', '$\\frac{5}{2}$'],
                             'answer': 5,
                             'exp': '$1 \\times \\frac{5}{2} = \\frac{5}{2}$입니다.',
                             'exp_en': '$1 \\times \\frac{5}{2} = \\frac{5}{2}$.'}]},
             {'title': '💎 5단계 · [최종 종합] 주어진 극한값 확정하기',
              'title_en': '💎 Step 5 · [Final Synthesis] Final limit value',
              'knowledge': '따라서 구하는 극한값은 $\\frac{5}{2}$입니다.',
              'knowledge_en': 'The final limit is $\\frac{5}{2}$.',
              'questions': [{'level_label': '최종 종합 디딤돌 5',
                             'level_label_en': 'Final Synthesis Step 5',
                             'stem': '$\\lim_{x \\to 0} \\frac{\\ln(1+5x^2)}{2x^2}$의 값은?',
                             'stem_en': 'What is the value of $\\lim_{x \\to 0} \\frac{\\ln(1+5x^2)}{2x^2}$?',
                             'options': ['$\\frac{1}{2}$', '$1$', '$\\frac{3}{2}$', '$2$', '$\\frac{5}{2}$'],
                             'answer': 5,
                             'exp': '$\\lim_{x \\to 0} \\frac{\\ln(1+5x^2)}{5x^2} \\times \\frac{5}{2} = '
                                    '\\frac{5}{2}$이므로 정답은 ⑤입니다.',
                             'exp_en': '$\\frac{5}{2}$ (choice ⑤).'}]}],
  'final': {'stem': '$\\lim_{x \\to 0} \\dfrac{\\ln(1+5x^2)}{2x^2}$의 값은? [2점]',
            'stem_en': 'What is the value of $\\lim_{x \\to 0} \\dfrac{\\ln(1+5x^2)}{2x^2}$? [2 points]',
            'options': ['$\\dfrac{1}{2}$', '$1$', '$\\dfrac{3}{2}$', '$2$', '$\\dfrac{5}{2}$'],
            'answer': 5,
            'exp': '$\\lim_{x \\to 0} \\dfrac{\\ln(1+5x^2)}{2x^2} = \\lim_{x \\to 0} \\dfrac{\\ln(1+5x^2)}{5x^2} '
                   '\\times \\dfrac{5}{2} = 1 \\times \\dfrac{5}{2} = \\dfrac{5}{2}$이므로 정답은 ⑤입니다.',
            'exp_en': '$\\lim_{x \\to 0} \\dfrac{\\ln(1+5x^2)}{5x^2} \\times \\dfrac{5}{2} = \\dfrac{5}{2}$. The '
                      'correct answer is ⑤.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>자연로그 함수의 기본 극한 $\\lim_{t \\to 0} \\frac{\\ln(1+t)}{t} = 1$</b>을 이용하여 극한값을 계산하는 '
                        '문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  $$\\lim_{x \\to 0} \\frac{\\ln(1+5x^2)}{2x^2} = \\lim_{x \\to 0} '
                        '\\left\\{\\frac{\\ln(1+5x^2)}{5x^2} \\times \\frac{5}{2}\\right\\} = 1 \\times \\frac{5}{2} = '
                        '\\frac{5}{2}$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 구하는 값은 $\\dfrac{5}{2}$이므로 정답은 <b>⑤번</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem evaluates a logarithmic limit using $\\lim_{t \\to 0} \\frac{\\ln(1+t)}{t} '
                           '= 1$.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  $$\\lim_{x \\to 0} \\frac{\\ln(1+5x^2)}{2x^2} = \\frac{5}{2} \\lim_{x \\to 0} '
                           '\\frac{\\ln(1+5x^2)}{5x^2} = \\frac{5}{2}$$\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  The correct answer is <b>choice ⑤ ($\\dfrac{5}{2}$)</b>.\n'
                           '</p>'}},
 {'slug': 'c2610m24',
  'qNum': '미적 24',
  'subject': '미적분',
  'title': '[2026학년도 10월 고3 미적 24번] 분수함수의 분리를 통한 정적분 계산',
  'title_en': '[2026 AY Oct Exam Grade 12 Calculus #24] Definite Integral of a Rational Function via Termwise Division',
  'summary_ko': '$\\dfrac{x+1}{x^2}$을 $\\dfrac{1}{x} + \\dfrac{1}{x^2}$으로 쪼개어 $\\left[\\ln x - '
                '\\dfrac{1}{x}\\right]_1^2 = \\ln 2 + \\dfrac{1}{2}$ 구하기',
  'summary_en': 'Split $\\dfrac{x+1}{x^2}$ into $\\dfrac{1}{x} + \\dfrac{1}{x^2}$ and integrate from $1$ to $2$ to '
                'obtain $\\ln 2 + \\dfrac{1}{2}$.',
  'tags': ['미적분', '적분법', '여러가지함수의정적분', '분수함수의적분', '24번'],
  'symbols': [{'sym': '$\\dfrac{x+1}{x^2} = \\dfrac{1}{x} + \\dfrac{1}{x^2}$',
               'desc': '분자를 분모 $x^2$으로 각각 나누어 두 분수로 분리',
               'desc_en': 'Splitting a fraction into two simpler terms.'},
              {'sym': '$\\int \\dfrac{1}{x}dx = \\ln|x| + C,\\quad \\int \\dfrac{1}{x^2}dx = -\\dfrac{1}{x} + C$',
               'desc': '$\\dfrac{1}{x}$과 $\\dfrac{1}{x^2}$의 부정적분 공식',
               'desc_en': 'Antiderivatives of $\\dfrac{1}{x}$ and $\\dfrac{1}{x^2}$.'}],
  'levels': [{'title': '🔰 1단계 · [초등 분수 쪼개기] $\\dfrac{x + 1}{x^2}$을 두 분수의 합으로 나누기',
              'title_en': '🔰 Step 1 · [Elementary Fraction Splitting] Splitting $\\dfrac{x + 1}{x^2}$ into two '
                          'fractions',
              'knowledge': '초등학교 분수 덧셈에서 $\\frac{a + b}{c} = \\frac{a}{c} + \\frac{b}{c}$로 쪼갤 수 있듯이, $\\frac{x + '
                           '1}{x^2} = \\frac{x}{x^2} + \\frac{1}{x^2} = \\frac{1}{x} + \\frac{1}{x^2}$로 나누어 씁니다.',
              'knowledge_en': 'Just as $\\frac{a+b}{c} = \\frac{a}{c} + \\frac{b}{c}$ in elementary fractions, '
                              '$\\frac{x+1}{x^2} = \\frac{x}{x^2} + \\frac{1}{x^2} = \\frac{1}{x} + \\frac{1}{x^2}$.',
              'questions': [{'level_label': '초등 분수 분리 디딤돌 1',
                             'level_label_en': 'Elementary Fraction Split Step 1',
                             'stem': '초등학교 분수 약분과 덧셈 원리로 $\\frac{x + 1}{x^2}$을 두 분수의 합으로 바르게 쪼갠 것은?',
                             'stem_en': 'Using elementary fraction splitting, how is $\\frac{x + 1}{x^2}$ written as a '
                                        'sum of two simpler fractions?',
                             'options': ['$1 + \\frac{1}{x}$',
                                         '$\\frac{1}{x} + \\frac{1}{x^2}$',
                                         '$\\frac{1}{x^2} + \\frac{1}{x^3}$',
                                         '$x + \\frac{1}{x^2}$',
                                         '$\\frac{2}{x}$'],
                             'answer': 2,
                             'exp': '$\\frac{x}{x^2} + \\frac{1}{x^2} = \\frac{1}{x} + \\frac{1}{x^2}$입니다.',
                             'exp_en': '$\\frac{x}{x^2} + \\frac{1}{x^2} = \\frac{1}{x} + \\frac{1}{x^2}$.'}]},
             {'title': '🌿 2단계 · [앞부분 적분] $\\int_1^2 \\dfrac{1}{x}dx$ 계산하기',
              'title_en': '🌿 Step 2 · [First Integral] Computing $\\int_1^2 \\dfrac{1}{x}dx$',
              'knowledge': '$\\frac{1}{x}$의 부정적분은 $\\ln|x|$이고 $\\ln 1 = 0$이므로 $\\left[\\ln x\\right]_1^2 = \\ln 2 - '
                           '\\ln 1 = \\ln 2$입니다.',
              'knowledge_en': '$\\int_1^2 \\frac{1}{x}dx = [\\ln x]_1^2 = \\ln 2 - 0 = \\ln 2$.',
              'questions': [{'level_label': '로그 정적분 디딤돌 2',
                             'level_label_en': 'Log Integral Step 2',
                             'stem': '$\\int_1^2 \\frac{1}{x}dx = [\\ln x]_1^2$의 값은?',
                             'stem_en': 'What is the value of $\\int_1^2 \\frac{1}{x}dx = [\\ln x]_1^2$?',
                             'options': ['$0$', '$\\ln 2$', '$1$', '$2\\ln 2$', '$\\ln 2 + 1$'],
                             'answer': 2,
                             'exp': '$\\ln 2 - \\ln 1 = \\ln 2 - 0 = \\ln 2$입니다.',
                             'exp_en': '$\\ln 2 - \\ln 1 = \\ln 2$.'}]},
             {'title': '🌱 3단계 · [뒷부분 부정적분] $\\dfrac{1}{x^2} = x^{-2}$의 부정적분 구하기',
              'title_en': '🌱 Step 3 · [Second Antiderivative] Antiderivative of $\\dfrac{1}{x^2} = x^{-2}$',
              'knowledge': "$\\left(-\\frac{1}{x}\\right)' = \\frac{1}{x^2}$이므로 $\\frac{1}{x^2}$의 부정적분은 "
                           '$-\\frac{1}{x}$입니다.',
              'knowledge_en': "Since $\\left(-\\frac{1}{x}\\right)' = \\frac{1}{x^2}$, the antiderivative of "
                              '$\\frac{1}{x^2}$ is $-\\frac{1}{x}$.',
              'questions': [{'level_label': '분수 부정적분 디딤돌 3',
                             'level_label_en': 'Power Antiderivative Step 3',
                             'stem': '미분하여 $\\frac{1}{x^2}$이 되는 함수(부정적분, 적분상수 제외)는?',
                             'stem_en': 'Which function differentiates to $\\frac{1}{x^2}$?',
                             'options': ['$\\frac{1}{x}$',
                                         '$-\\frac{1}{x}$',
                                         '$\\frac{2}{x}$',
                                         '$-\\frac{2}{x}$',
                                         '$\\ln(x^2)$'],
                             'answer': 2,
                             'exp': "$(x^{-1})' = -x^{-2}$이므로 $\\left(-\\frac{1}{x}\\right)' = \\frac{1}{x^2}$입니다.",
                             'exp_en': "$\\left(-\\frac{1}{x}\\right)' = \\frac{1}{x^2}$."}]},
             {'title': '🌳 4단계 · [뒷부분 정적분] $\\left[-\\dfrac{1}{x}\\right]_1^2$ 계산하기',
              'title_en': '🌳 Step 4 · [Second Definite Integral] Evaluating $\\left[-\\dfrac{1}{x}\\right]_1^2$',
              'knowledge': '위끝 $2$와 아래끝 $1$을 대입하면 $\\left(-\\frac{1}{2}\\right) - (-1) = -\\frac{1}{2} + 1 = '
                           '\\frac{1}{2}$입니다.',
              'knowledge_en': '$\\left[-\\frac{1}{x}\\right]_1^2 = -\\frac{1}{2} - (-1) = \\frac{1}{2}$.',
              'questions': [{'level_label': '분수 정적분 디딤돌 4',
                             'level_label_en': 'Definite Evaluation Step 4',
                             'stem': '$\\left[-\\frac{1}{x}\\right]_1^2 = -\\frac{1}{2} - (-1)$을 계산한 값은?',
                             'stem_en': 'What is $\\left[-\\frac{1}{x}\\right]_1^2 = -\\frac{1}{2} - (-1)$?',
                             'options': ['$-\\frac{3}{2}$',
                                         '$-\\frac{1}{2}$',
                                         '$\\frac{1}{2}$',
                                         '$1$',
                                         '$\\frac{3}{2}$'],
                             'answer': 3,
                             'exp': '$-\\frac{1}{2} + 1 = \\frac{1}{2}$입니다.',
                             'exp_en': '$-\\frac{1}{2} + 1 = \\frac{1}{2}$.'}]},
             {'title': '💎 5단계 · [최종 종합] 두 정적분 결과 더하기',
              'title_en': '💎 Step 5 · [Final Synthesis] Combining both parts',
              'knowledge': '앞부분 $\\ln 2$와 뒷부분 $\\frac{1}{2}$을 더하면 $\\ln 2 + \\frac{1}{2}$이 됩니다.',
              'knowledge_en': 'Combine $\\ln 2$ and $\\frac{1}{2}$ to get $\\ln 2 + \\frac{1}{2}$.',
              'questions': [{'level_label': '최종 종합 디딤돌 5',
                             'level_label_en': 'Final Synthesis Step 5',
                             'stem': '$\\int_1^2 \\frac{x+1}{x^2}dx$의 값은?',
                             'stem_en': 'What is the value of $\\int_1^2 \\frac{x+1}{x^2}dx$?',
                             'options': ['$\\ln 2 + \\frac{1}{2}$',
                                         '$\\ln 2 + 1$',
                                         '$2\\ln 2 + \\frac{1}{2}$',
                                         '$2\\ln 2 + 1$',
                                         '$2\\ln 2 + \\frac{3}{2}$'],
                             'answer': 1,
                             'exp': '$\\left[\\ln x - \\frac{1}{x}\\right]_1^2 = \\ln 2 + \\frac{1}{2}$이므로 정답은 ①입니다.',
                             'exp_en': '$\\ln 2 + \\frac{1}{2}$ (choice ①).'}]}],
  'final': {'stem': '$\\int_1^2 \\dfrac{x+1}{x^2}dx$의 값은? [3점]',
            'stem_en': 'What is the value of $\\int_1^2 \\dfrac{x+1}{x^2}dx$? [3 points]',
            'options': ['$\\ln 2 + \\dfrac{1}{2}$',
                        '$\\ln 2 + 1$',
                        '$2\\ln 2 + \\dfrac{1}{2}$',
                        '$2\\ln 2 + 1$',
                        '$2\\ln 2 + \\dfrac{3}{2}$'],
            'answer': 1,
            'exp': '$\\int_1^2 \\left(\\dfrac{1}{x} + \\dfrac{1}{x^2}\\right)dx = \\left[\\ln x - '
                   '\\dfrac{1}{x}\\right]_1^2 = \\left(\\ln 2 - \\dfrac{1}{2}\\right) - (0 - 1) = \\ln 2 + '
                   '\\dfrac{1}{2}$입니다.',
            'exp_en': '$\\int_1^2 \\left(\\dfrac{1}{x} + \\dfrac{1}{x^2}\\right)dx = \\left[\\ln x - '
                      '\\dfrac{1}{x}\\right]_1^2 = \\ln 2 + \\dfrac{1}{2}$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 분수식 $\\frac{x+1}{x^2}$을 $\\frac{1}{x} + \\frac{1}{x^2}$으로 분리하여 <b>로그함수와 유리함수의 '
                        '정적분</b>을 계산하는 문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  $$\\int_1^2 \\frac{x+1}{x^2}dx = \\int_1^2 \\left(\\frac{1}{x} + \\frac{1}{x^2}\\right)dx = '
                        '\\left[\\ln x - \\frac{1}{x}\\right]_1^2 = \\left(\\ln 2 - \\frac{1}{2}\\right) - (\\ln 1 - '
                        '1) = \\ln 2 + \\frac{1}{2}$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 구하는 값은 $\\ln 2 + \\dfrac{1}{2}$이므로 정답은 <b>①번</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem evaluates a definite integral by splitting the integrand into '
                           '$\\frac{1}{x} + x^{-2}$.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  $$\\int_1^2 \\left(\\frac{1}{x} + \\frac{1}{x^2}\\right)dx = \\left[\\ln x - '
                           '\\frac{1}{x}\\right]_1^2 = \\ln 2 - \\frac{1}{2} + 1 = \\ln 2 + \\frac{1}{2}$$\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  The correct answer is <b>choice ① ($\\ln 2 + \\dfrac{1}{2}$)</b>.\n'
                           '</p>'}},
 {'slug': 'c2610m25',
  'qNum': '미적 25',
  'subject': '미적분',
  'title': '[2026학년도 10월 고3 미적 25번] 이차부등식과 수열의 극한의 대소 관계 (샌드위치 정리)',
  'title_en': '[2026 AY Oct Exam Grade 12 Calculus #25] Quadratic Inequality and Squeeze Theorem for Sequence Limits',
  'summary_ko': '이차부등식을 풀어 $\\dfrac{n^2-n}{k} < a_n < \\dfrac{n^2+n}{k}$를 얻고 샌드위치 정리로 $\\dfrac{1}{4k}=k$에서 '
                '$k=\\dfrac{1}{2}$ 구하기',
  'summary_en': 'Factor the quadratic inequality to bound $a_n$ between $\\dfrac{n^2-n}{k}$ and $\\dfrac{n^2+n}{k}$, '
                'then apply the Squeeze Theorem to get $\\dfrac{1}{4k}=k$ and $k=\\dfrac{1}{2}$.',
  'tags': ['미적분', '수열의극한', '극한의대소관계', '샌드위치정리', '이차부등식', '25번'],
  'symbols': [{'sym': '$(ka_n - n^2 + n)(ka_n - n^2 - n) < 0$',
               'desc': '합차공식 $X^2 - n^2 < 0$으로 인수분해한 이차부등식',
               'desc_en': 'Factoring the quadratic inequality via difference of squares.'},
              {'sym': '$\\dfrac{n^2 - n}{k} < a_n < \\dfrac{n^2 + n}{k}$',
               'desc': '양수 $k$로 나누어 구한 수열 $a_n$의 양쪽 범위',
               'desc_en': 'Sandwich bounds on $a_n$ after dividing by $k > 0$.'}],
  'levels': [{'title': '🔰 1단계 · [초등 곱셈과 제곱] $4k^2 = 1$을 만족하는 양수 $k$ 구하기',
              'title_en': '🔰 Step 1 · [Elementary Multiplication] Finding positive $k$ satisfying $4k^2 = 1$',
              'knowledge': '초등학교 분수 곱셈에서 $\\frac{1}{2} \\times \\frac{1}{2} = \\frac{1}{4}$이고 여기에 $4$를 곱하면 $1$이 됩니다! 이 '
                           '문제의 마지막 단계에서 나오는 방정식 $\\frac{1}{4k} = k \\iff 4k^2 = 1$을 먼저 초등 분수 곱셈으로 확인해 봅시다.',
              'knowledge_en': 'By elementary fraction multiplication, $\\left(\\frac{1}{2}\\right)^2 = \\frac{1}{4}$, '
                              'so $4 \\times \\left(\\frac{1}{2}\\right)^2 = 1$.',
              'questions': [{'level_label': '초등 분수 곱셈 디딤돌 1',
                             'level_label_en': 'Elementary Fraction Product Step 1',
                             'stem': '초등학교 분수 곱셈 원리에 따라 $4 \\times k \\times k = 1$ ($k > 0$)을 만족시키는 분수 $k$는?',
                             'stem_en': 'Using elementary fraction multiplication, which positive fraction $k$ '
                                        'satisfies $4 \\times k \\times k = 1$?',
                             'options': ['$\\frac{1}{4}$', '$\\frac{1}{2}$', '$\\frac{3}{4}$', '$1$', '$\\frac{5}{4}$'],
                             'answer': 2,
                             'exp': '$k^2 = \\frac{1}{4}$이고 $k > 0$이므로 $k = \\frac{1}{2}$입니다.',
                             'exp_en': '$k^2 = \\frac{1}{4} \\implies k = \\frac{1}{2}$.'}]},
             {'title': '🌿 2단계 · [완전제곱식 변형] 부등식 $(ka_n - n^2)^2 < n^2$으로 바꾸기',
              'title_en': '🌿 Step 2 · [Completing the Square] Rewriting as $(ka_n - n^2)^2 < n^2$',
              'knowledge': '$k^2a_n^2 - 2kn^2a_n + n^4 - n^2 < 0$에서 앞의 세 항은 $(ka_n - n^2)^2$입니다! 따라서 $(ka_n - n^2)^2 < '
                           'n^2 \\implies -n < ka_n - n^2 < n$이 됩니다.',
              'knowledge_en': 'The first three terms form $(ka_n - n^2)^2$, so $(ka_n - n^2)^2 < n^2 \\implies -n < '
                              'ka_n - n^2 < n$.',
              'questions': [{'level_label': '부등식 정리 디딤돌 2',
                             'level_label_en': 'Inequality Bounds Step 2',
                             'stem': '$-n < ka_n - n^2 < n$의 각 변에 $n^2$을 더하고 양수 $k$로 나누었을 때, $a_n$의 범위는?',
                             'stem_en': 'Adding $n^2$ and dividing by $k > 0$ in $-n < ka_n - n^2 < n$ gives which '
                                        'bounds for $a_n$?',
                             'options': ['$\\frac{n^2 - n}{k} < a_n < \\frac{n^2 + n}{k}$',
                                         '$k(n^2 - n) < a_n < k(n^2 + n)$',
                                         '$\\frac{n - 1}{k} < a_n < \\frac{n + 1}{k}$',
                                         '$\\frac{n^2}{k} < a_n < \\frac{2n^2}{k}$',
                                         '$-n < a_n < n$'],
                             'answer': 1,
                             'exp': '$n^2 - n < ka_n < n^2 + n$을 양수 $k$로 나누면 $\\frac{n^2 - n}{k} < a_n < \\frac{n^2 + '
                                    'n}{k}$입니다.',
                             'exp_en': '$\\frac{n^2 - n}{k} < a_n < \\frac{n^2 + n}{k}$.'}]},
             {'title': '🌱 3단계 · [최고차항 계수 비] $\\lim_{n \\to \\infty} \\dfrac{n^2 \\pm n}{k(4n^2 + 1)}$ 구하기',
              'title_en': '🌱 Step 3 · [Leading Coefficient Ratio] Evaluating $\\lim_{n \\to \\infty} \\dfrac{n^2 \\pm '
                          'n}{k(4n^2 + 1)}$',
              'knowledge': '각 변을 $4n^2 + 1$로 나누고 $n \\to \\infty$ 극한을 취하면, 분모·분자의 최고차항($n^2$)의 계수 비인 $\\frac{1}{4k}$로 '
                           '수렴합니다.',
              'knowledge_en': 'Dividing by $4n^2 + 1$ and taking $n \\to \\infty$, both bounds converge to the ratio '
                              'of the $n^2$ coefficients: $\\frac{1}{4k}$.',
              'questions': [{'level_label': '샌드위치 극한 디딤돌 3',
                             'level_label_en': 'Squeeze Limit Step 3',
                             'stem': '극한의 대소 관계(샌드위치 정리)에 의하여 $\\lim_{n \\to \\infty} \\frac{a_n}{4n^2 + 1}$을 $k$에 대한 '
                                     '식으로 나타내면?',
                             'stem_en': 'By the Squeeze Theorem, what is $\\lim_{n \\to \\infty} \\frac{a_n}{4n^2 + '
                                        '1}$ in terms of $k$?',
                             'options': ['$\\frac{1}{k}$',
                                         '$\\frac{1}{2k}$',
                                         '$\\frac{1}{4k}$',
                                         '$\\frac{k}{4}$',
                                         '$4k$'],
                             'answer': 3,
                             'exp': '분자의 $n^2$ 계수는 $1$, 분모의 $n^2$ 계수는 $4k$이므로 $\\frac{1}{4k}$입니다.',
                             'exp_en': 'The ratio of leading coefficients is $\\frac{1}{4k}$.'}]},
             {'title': '🌳 4단계 · [방정식 세우기] $\\dfrac{1}{4k} = k$ 정리하기',
              'title_en': '🌳 Step 4 · [Setting Up Equation] Solving $\\dfrac{1}{4k} = k$',
              'knowledge': '문제에서 극한값이 $k$라고 했으므로 $\\frac{1}{4k} = k \\implies k^2 = \\frac{1}{4}$입니다.',
              'knowledge_en': 'Equating the limit to $k$ gives $\\frac{1}{4k} = k \\implies k^2 = \\frac{1}{4}$.',
              'questions': [{'level_label': '$k^2$ 구하기 디딤돌 4',
                             'level_label_en': 'Finding $k^2$ Step 4',
                             'stem': '$\\frac{1}{4k} = k$에서 $k^2$의 값은?',
                             'stem_en': 'From $\\frac{1}{4k} = k$, what is $k^2$?',
                             'options': ['$\\frac{1}{16}$',
                                         '$\\frac{1}{8}$',
                                         '$\\frac{1}{4}$',
                                         '$\\frac{1}{2}$',
                                         '$1$'],
                             'answer': 3,
                             'exp': '양변에 $k$를 곱하면 $k^2 = \\frac{1}{4}$입니다.',
                             'exp_en': '$k^2 = \\frac{1}{4}$.'}]},
             {'title': '💎 5단계 · [최종 종합] 양수 $k$의 값 확정하기',
              'title_en': '💎 Step 5 · [Final Synthesis] Final value of $k > 0$',
              'knowledge': '$k > 0$이므로 $k = \\frac{1}{2}$입니다.',
              'knowledge_en': 'Since $k > 0$, $k = \\frac{1}{2}$.',
              'questions': [{'level_label': '최종 종합 디딤돌 5',
                             'level_label_en': 'Final Synthesis Step 5',
                             'stem': '양수 $k$의 값은?',
                             'stem_en': 'What is the value of the positive constant $k$?',
                             'options': ['$\\frac{1}{4}$', '$\\frac{1}{2}$', '$\\frac{3}{4}$', '$1$', '$\\frac{5}{4}$'],
                             'answer': 2,
                             'exp': '$k = \\frac{1}{2}$이므로 정답은 ②입니다.',
                             'exp_en': '$k = \\frac{1}{2}$ (choice ②).'}]}],
  'final': {'stem': '수열 $\\{a_n\\}$이 모든 자연수 $n$에 대하여 부등식 $k^2a_n^2 - 2kn^2a_n + n^4 - n^2 < 0$을 만족시킨다. $\\lim_{n \\to '
                    '\\infty} \\dfrac{a_n}{4n^2 + 1} = k$일 때, 양수 $k$의 값은? [3점]',
            'stem_en': 'A sequence $\\{a_n\\}$ satisfies $k^2a_n^2 - 2kn^2a_n + n^4 - n^2 < 0$ for all natural numbers '
                       '$n$. When $\\lim_{n \\to \\infty} \\dfrac{a_n}{4n^2 + 1} = k$, what is the positive constant '
                       '$k$? [3 points]',
            'options': ['$\\dfrac{1}{4}$', '$\\dfrac{1}{2}$', '$\\dfrac{3}{4}$', '$1$', '$\\dfrac{5}{4}$'],
            'answer': 2,
            'exp': '$(ka_n - n^2)^2 < n^2$에서 $\\dfrac{n^2-n}{k} < a_n < \\dfrac{n^2+n}{k}$이므로 '
                   '$\\lim_{n\\to\\infty}\\dfrac{a_n}{4n^2+1} = \\dfrac{1}{4k} = k$에서 $k = \\dfrac{1}{2}$입니다.',
            'exp_en': 'From $(ka_n - n^2)^2 < n^2$, we get $\\dfrac{n^2-n}{k} < a_n < \\dfrac{n^2+n}{k}$. By the '
                      'Squeeze Theorem, $\\dfrac{1}{4k} = k \\implies k = \\dfrac{1}{2}$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>이차부등식을 풀어 수열 $a_n$의 범위를 구한 뒤 수열의 극한의 대소 관계(샌드위치 정리)</b>를 적용하는 문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 이차부등식 풀기</b><br>\n'
                        '  $$(ka_n - n^2)^2 - n^2 < 0 \\iff (ka_n - n^2 + n)(ka_n - n^2 - n) < 0$$\n'
                        '  $k > 0$이므로 양변을 $k$로 나누면:<br>\n'
                        '  $$\\frac{n^2 - n}{k} < a_n < \\frac{n^2 + n}{k}$$<br>\n'
                        '  <b>2단계: 샌드위치 정리 적용</b><br>\n'
                        '  각 변을 $4n^2 + 1 > 0$으로 나누고 $n \\to \\infty$ 극한을 취하면:<br>\n'
                        '  $$\\lim_{n \\to \\infty} \\frac{a_n}{4n^2 + 1} = \\frac{1}{4k} = k \\implies k^2 = '
                        '\\frac{1}{4}$$\n'
                        '  $k > 0$이므로 $k = \\frac{1}{2}$입니다.\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 양수 $k$의 값은 $\\dfrac{1}{2}$이므로 정답은 <b>②번</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem applies the <b>Squeeze Theorem</b> after solving a quadratic inequality '
                           'for $a_n$.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Bound $a_n$</b><br>\n'
                           '  $$(ka_n - n^2)^2 < n^2 \\implies \\frac{n^2 - n}{k} < a_n < \\frac{n^2 + n}{k}$$<br>\n'
                           '  <b>Step 2: Apply the Squeeze Theorem</b><br>\n'
                           '  $$\\lim_{n \\to \\infty} \\frac{a_n}{4n^2 + 1} = \\frac{1}{4k} = k \\implies k = '
                           '\\frac{1}{2}$$\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  The correct answer is <b>choice ② ($\\dfrac{1}{2}$)</b>.\n'
                           '</p>'}},
 {'slug': 'c2610m26',
  'qNum': '미적 26',
  'subject': '미적분',
  'title': '[2026학년도 10월 고3 미적 26번] 반원을 단면으로 하는 입체도형의 부피와 부분적분',
  'title_en': '[2026 AY Oct Exam Grade 12 Calculus #26] Volume of a Solid with Semicircular Cross-Sections',
  'summary_ko': '지름이 $\\sqrt{1+(\\ln x)^2}$인 반원의 넓이 $S(x)=\\dfrac{\\pi}{8}\\{1+(\\ln x)^2\\}$을 $1$부터 $e$까지 정적분하여 '
                '$\\dfrac{2e-3}{8}\\pi$ 구하기',
  'summary_en': 'Integrate the semicircular cross-sectional area $S(x)=\\dfrac{\\pi}{8}\\{1+(\\ln x)^2\\}$ from $1$ to '
                '$e$ to obtain $\\dfrac{2e-3}{8}\\pi$.',
  'tags': ['미적분', '적분법', '정적분의활용', '입체도형의부피', '부분적분', '26번'],
  'symbols': [{'sym': '$S(x) = \\dfrac{1}{2}\\pi r^2 = \\dfrac{\\pi}{8}D^2$',
               'desc': '지름의 길이가 $D$일 때 반원의 넓이는 $\\dfrac{\\pi}{8}D^2$',
               'desc_en': 'Area of a semicircle with diameter $D$ is $\\dfrac{\\pi}{8}D^2$.'},
              {'sym': '$\\int_1^e (\\ln x)^2 dx = \\left[x(\\ln x)^2 - 2x\\ln x + 2x\\right]_1^e = e - 2$',
               'desc': '부분적분을 이용한 $(\\ln x)^2$의 정적분',
               'desc_en': 'Definite integral of $(\\ln x)^2$ evaluated via integration by parts.'}],
  'levels': [{'title': '🔰 1단계 · [초등 원의 넓이] 지름이 $D$일 때 반원의 넓이 식 구하기',
              'title_en': '🔰 Step 1 · [Elementary Circle Area] Area of a semicircle with diameter $D$',
              'knowledge': '초등학교에서 반지름 $r$은 지름 $D$의 절반인 $\\frac{D}{2}$입니다. 원의 넓이 $\\pi r^2$의 절반인 반원의 넓이는 $\\frac{1}{2} '
                           '\\times \\pi \\times \\left(\\frac{D}{2}\\right)^2 = \\frac{\\pi}{8}D^2$입니다!',
              'knowledge_en': 'In elementary geometry, radius $r = \\frac{D}{2}$, so the area of a semicircle is '
                              '$\\frac{1}{2}\\pi r^2 = \\frac{1}{2}\\pi\\left(\\frac{D}{2}\\right)^2 = '
                              '\\frac{\\pi}{8}D^2$.',
              'questions': [{'level_label': '초등 반원 넓이 디딤돌 1',
                             'level_label_en': 'Elementary Semicircle Area Step 1',
                             'stem': '초등학교 원의 넓이 원리에 따라 지름의 길이가 $D = \\sqrt{1 + (\\ln x)^2}$인 반원의 단면 넓이 $S(x) = '
                                     '\\frac{\\pi}{8}D^2$은?',
                             'stem_en': 'Using elementary circle area, what is the area $S(x) = \\frac{\\pi}{8}D^2$ of '
                                        'a semicircle with diameter $D = \\sqrt{1 + (\\ln x)^2}$?',
                             'options': ['$\\frac{\\pi}{2}\\{1 + (\\ln x)^2\\}$',
                                         '$\\frac{\\pi}{4}\\{1 + (\\ln x)^2\\}$',
                                         '$\\frac{\\pi}{8}\\{1 + (\\ln x)^2\\}$',
                                         '$\\pi\\{1 + (\\ln x)^2\\}$',
                                         '$\\frac{\\pi}{16}\\{1 + (\\ln x)^2\\}$'],
                             'answer': 3,
                             'exp': '근호가 제곱으로 벗겨지므로 $S(x) = \\frac{\\pi}{8}\\{1 + (\\ln x)^2\\}$입니다.',
                             'exp_en': '$S(x) = \\frac{\\pi}{8}\\{1 + (\\ln x)^2\\}$.'}]},
             {'title': '🌿 2단계 · [상수항 적분] $\\int_1^e 1\\\\,dx$ 계산하기',
              'title_en': '🌿 Step 2 · [Constant Integral] Evaluating $\\int_1^e 1\\\\,dx$',
              'knowledge': '$1$을 $1$부터 $e$까지 정적분하면 구간의 길이 $e - 1$입니다.',
              'knowledge_en': '$\\int_1^e 1\\,dx = e - 1$.',
              'questions': [{'level_label': '상수 적분 디딤돌 2',
                             'level_label_en': 'Constant Integral Step 2',
                             'stem': '$\\int_1^e 1\\,dx = [x]_1^e$의 값은?',
                             'stem_en': 'What is $\\int_1^e 1\\,dx = [x]_1^e$?',
                             'options': ['$1$', '$e - 2$', '$e - 1$', '$e$', '$e + 1$'],
                             'answer': 3,
                             'exp': '$e - 1$입니다.',
                             'exp_en': '$e - 1$.'}]},
             {'title': '🌱 3단계 · [부분적분] $\\int_1^e (\\ln x)^2 dx$ 계산하기',
              'title_en': '🌱 Step 3 · [Integration by Parts] Evaluating $\\int_1^e (\\ln x)^2 dx$',
              'knowledge': '부분적분을 적용하면 $\\int (\\ln x)^2 dx = x(\\ln x)^2 - 2\\int \\ln x\\,dx = x(\\ln x)^2 - 2x\\ln '
                           'x + 2x + C$입니다. 위끝 $e$와 아래끝 $1$을 대입하면 $(e - 2e + 2e) - (0 - 0 + 2) = e - 2$입니다.',
              'knowledge_en': 'Using integration by parts, $\\int_1^e (\\ln x)^2 dx = \\left[x(\\ln x)^2 - 2x\\ln x + '
                              '2x\\right]_1^e = e - 2$.',
              'questions': [{'level_label': '로그제곱 정적분 디딤돌 3',
                             'level_label_en': 'Log Squared Integral Step 3',
                             'stem': '$\\int_1^e (\\ln x)^2 dx = \\left[x(\\ln x)^2 - 2x\\ln x + 2x\\right]_1^e$를 계산한 '
                                     '값은?',
                             'stem_en': 'What is the value of $\\int_1^e (\\ln x)^2 dx$?',
                             'options': ['$e - 3$', '$e - 2$', '$e - 1$', '$2e - 3$', '$2e - 2$'],
                             'answer': 2,
                             'exp': '$x = e$일 때 $e(1) - 2e(1) + 2e = e$이고, $x = 1$일 때 $2$이므로 $e - 2$입니다.',
                             'exp_en': '$e - 2$.'}]},
             {'title': '🌳 4단계 · [적분 합산] $(e - 1) + (e - 2)$ 계산하기',
              'title_en': '🌳 Step 4 · [Summing Integrals] Computing $(e - 1) + (e - 2)$',
              'knowledge': '$\\int_1^e \\{1 + (\\ln x)^2\\}dx = (e - 1) + (e - 2) = 2e - 3$입니다.',
              'knowledge_en': '$(e - 1) + (e - 2) = 2e - 3$.',
              'questions': [{'level_label': '적분 합산 디딤돌 4',
                             'level_label_en': 'Integral Sum Step 4',
                             'stem': '$(e - 1) + (e - 2)$를 간단히 한 식은?',
                             'stem_en': 'Simplify $(e - 1) + (e - 2)$.',
                             'options': ['$2e - 1$', '$2e - 2$', '$2e - 3$', '$2e - 4$', '$e - 3$'],
                             'answer': 3,
                             'exp': '$2e - 3$입니다.',
                             'exp_en': '$2e - 3$.'}]},
             {'title': '💎 5단계 · [최종 종합] 입체도형의 부피 $V$ 확정하기',
              'title_en': '💎 Step 5 · [Final Synthesis] Final volume $V$',
              'knowledge': '앞의 상수 $\\frac{\\pi}{8}$을 곱하면 부피 $V = \\frac{(2e - 3)\\pi}{8}$가 완성됩니다.',
              'knowledge_en': 'Multiply by $\\frac{\\pi}{8}$ to get $V = \\frac{(2e - 3)\\pi}{8}$.',
              'questions': [{'level_label': '최종 종합 디딤돌 5',
                             'level_label_en': 'Final Synthesis Step 5',
                             'stem': '구하는 입체도형의 부피 $V = \\int_1^e S(x)dx$는?',
                             'stem_en': 'What is the volume $V = \\int_1^e S(x)dx$ of the solid?',
                             'options': ['$\\frac{(2e - 1)\\pi}{8}$',
                                         '$\\frac{(e - 1)\\pi}{4}$',
                                         '$\\frac{(2e - 3)\\pi}{8}$',
                                         '$\\frac{(e - 2)\\pi}{4}$',
                                         '$\\frac{(2e - 5)\\pi}{8}$'],
                             'answer': 3,
                             'exp': '$V = \\frac{\\pi}{8}(2e - 3) = \\frac{(2e - 3)\\pi}{8}$이므로 정답은 ③입니다.',
                             'exp_en': '$\\frac{(2e - 3)\\pi}{8}$ (choice ③).'}]}],
  'final': {'stem': '그림과 같이 곡선 $y = \\sqrt{1 + (\\ln x)^2}$ ($1 \\le x \\le e$)와 $x$축 및 두 직선 $x = 1, x = e$로 둘러싸인 도형을 '
                    '밑면으로 하는 입체도형이 있다. 이 입체도형을 $x$축에 수직인 평면으로 자른 단면이 모두 반원일 때, 이 입체도형의 부피는? [3점]',
            'stem_en': 'The base of a solid is bounded by $y = \\sqrt{1 + (\\ln x)^2}$ ($1 \\le x \\le e$), the '
                       '$x$-axis, $x = 1$, and $x = e$. Every cross-section perpendicular to the $x$-axis is a '
                       'semicircle. What is the volume of this solid? [3 points]',
            'options': ['$\\dfrac{(2e - 1)\\pi}{8}$',
                        '$\\dfrac{(e - 1)\\pi}{4}$',
                        '$\\dfrac{(2e - 3)\\pi}{8}$',
                        '$\\dfrac{(e - 2)\\pi}{4}$',
                        '$\\dfrac{(2e - 5)\\pi}{8}$'],
            'answer': 3,
            'exp': '단면인 반원의 넓이는 $S(x) = \\dfrac{\\pi}{8}\\{1 + (\\ln x)^2\\}$이므로 부피는 $\\int_1^e S(x)dx = '
                   '\\dfrac{\\pi}{8}\\{(e-1) + (e-2)\\} = \\dfrac{(2e-3)\\pi}{8}$입니다.',
            'exp_en': 'The semicircular cross-section has area $S(x) = \\dfrac{\\pi}{8}\\{1 + (\\ln x)^2\\}$, so $V = '
                      '\\int_1^e S(x)dx = \\dfrac{\\pi}{8}\\{(e-1) + (e-2)\\} = \\dfrac{(2e-3)\\pi}{8}$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>단면의 넓이 $S(x)$를 정적분하여 입체도형의 부피를 구하는 공식</b>과 <b>$(\\ln x)^2$의 부분적분</b>을 결합한 '
                        '문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 단면의 넓이 $S(x)$ 구하기</b><br>\n'
                        '  지름의 길이가 $y = \\sqrt{1 + (\\ln x)^2}$인 반원의 반지름은 $r = \\frac{1}{2}\\sqrt{1 + (\\ln x)^2}$이므로 '
                        '단면의 넓이는:<br>\n'
                        '  $$S(x) = \\frac{1}{2}\\pi r^2 = \\frac{\\pi}{8}\\left\\{1 + (\\ln x)^2\\right\\}$$<br>\n'
                        '  <b>2단계: 정적분으로 부피 $V$ 계산</b><br>\n'
                        '  $$V = \\int_1^e \\frac{\\pi}{8}\\left\\{1 + (\\ln x)^2\\right\\}dx = '
                        '\\frac{\\pi}{8}\\left[x + x(\\ln x)^2 - 2x\\ln x + 2x\\right]_1^e = '
                        '\\frac{\\pi}{8}\\left\\{(e + e) - (1 + 2)\\right\\} = \\frac{(2e - 3)\\pi}{8}$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 입체도형의 부피는 $\\dfrac{(2e - 3)\\pi}{8}$이므로 정답은 <b>③번</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem computes the <b>volume of a solid by integrating semicircular '
                           'cross-sectional areas</b>.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Cross-sectional area</b><br>\n'
                           '  $$S(x) = \\frac{\\pi}{8}\\left\\{1 + (\\ln x)^2\\right\\}$$<br>\n'
                           '  <b>Step 2: Integrate from $1$ to $e$</b><br>\n'
                           '  $$V = \\frac{\\pi}{8}\\int_1^e \\left\\{1 + (\\ln x)^2\\right\\}dx = '
                           '\\frac{\\pi}{8}\\left[(e - 1) + (e - 2)\\right] = \\frac{(2e - 3)\\pi}{8}$$\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  The correct answer is <b>choice ③ ($\\dfrac{(2e - 3)\\pi}{8}$)</b>.\n'
                           '</p>'}},
 {'slug': 'c2610m27',
  'qNum': '미적 27',
  'subject': '미적분',
  'title': '[2026학년도 10월 고3 미적 27번] 구간별 정의된 지수함수의 미분가능성과 역함수의 미분법',
  'title_en': '[2026 AY Oct Exam Grade 12 Calculus #27] Differentiability of Piecewise Exponential Function and '
              'Derivative of Inverse',
  'summary_ko': "$x=b$에서의 연속·미분가능 조건으로 $e^b=2,\\ a=2$를 구하고 $f(x)=8$을 만족하는 $e^x=4$에서 $g'(8)=\\dfrac{1}{10}$ 도출하기",
  'summary_en': 'Use continuity and differentiability at $x=b$ to find $e^b=2$ and $a=2$, solve $f(x)=8$ to get '
                "$e^x=4$, and compute $g'(8)=\\dfrac{1}{f'(\\ln 4)}=\\dfrac{1}{10}$.",
  'tags': ['미적분', '미분법', '미분가능성', '역함수의미분법', '지수함수', '27번'],
  'symbols': [{'sym': "$f(b-) = f(b+),\\quad f'(b-) = f'(b+)$",
               'desc': '경계점 $x=b$에서 미분가능하기 위한 함숫값 일치(연속)와 미분계수 일치 조건',
               'desc_en': 'Continuity and matching left and right derivatives at $x=b$.'},
              {'sym': "$g'(8) = \\dfrac{1}{f'(c)} \\quad (f(c) = 8)$",
               'desc': '역함수의 미분법 공식',
               'desc_en': 'Formula for the derivative of the inverse function at $y=8$.'}],
  'levels': [{'title': '🔰 1단계 · [초등 역수 약속] 역함수의 기울기는 원래 기울기를 뒤집은 역수!',
              'title_en': '🔰 Step 1 · [Elementary Reciprocal] Slope of the inverse is the reciprocal of the original '
                          'slope',
              'knowledge': "가로와 세로를 바꾼 역함수 $g(x)$의 미분계수 $g'(8)$은, $f(c) = 8$인 점에서 원래 함수의 미분계수 $f'(c)$를 초등학교 분수 "
                           "뒤집기(역수)한 $\\frac{1}{f'(c)}$입니다!",
              'knowledge_en': 'By elementary reciprocals, swapping $x$ and $y$ inverts the slope: if $f(c) = 8$ and '
                              "$f'(c) = 10$, then $g'(8) = \\frac{1}{10}$.",
              'questions': [{'level_label': '초등 역수 디딤돌 1',
                             'level_label_en': 'Elementary Reciprocal Step 1',
                             'stem': "초등학교 역수 구하기처럼 $f(c) = 8$이고 $f'(c) = 10$일 때, 역함수의 미분계수 $g'(8) = "
                                     "\\frac{1}{f'(c)}$의 값은?",
                             'stem_en': "Using elementary reciprocals, if $f(c) = 8$ and $f'(c) = 10$, what is $g'(8) "
                                        "= \\frac{1}{f'(c)}$?",
                             'options': ['$\\frac{1}{16}$',
                                         '$\\frac{1}{14}$',
                                         '$\\frac{1}{12}$',
                                         '$\\frac{1}{10}$',
                                         '$\\frac{1}{8}$'],
                             'answer': 4,
                             'exp': "$10$의 역수는 $\\frac{1}{10}$입니다. 이제 왜 $f'(c) = 10$이 되는지 차근차근 확인해 봅시다!",
                             'exp_en': 'The reciprocal of $10$ is $\\frac{1}{10}$.'}]},
             {'title': '🌿 2단계 · [미분가능 조건] $x = b$에서 좌미분계수와 우미분계수 같다고 놓기',
              'title_en': '🌿 Step 2 · [Differentiability] Equating left and right derivatives at $x = b$',
              'knowledge': "$x < b$에서 $f'(x) = 2e^{2x}$이고, $x > b$에서 $f'(x) = 2e^x + 8e^{-x}$입니다. $x = b$에서 미분가능하므로 "
                           '$2e^{2b} = 2e^b + 8e^{-b}$입니다. $t = e^b > 0$이라 하고 양변에 $\\frac{t}{2}$를 곱하면 $t^3 - t^2 - 4 = '
                           '(t - 2)(t^2 + t + 2) = 0$이 됩니다.',
              'knowledge_en': 'Equating derivatives at $x=b$ gives $2e^{2b} = 2e^b + 8e^{-b}$. Letting $t = e^b > 0$, '
                              'we get $t^3 - t^2 - 4 = (t-2)(t^2+t+2) = 0$.',
              'questions': [{'level_label': '$e^b$ 값 구하기 디딤돌 2',
                             'level_label_en': 'Finding $e^b$ Step 2',
                             'stem': '$(t - 2)(t^2 + t + 2) = 0$에서 양수 $t = e^b$의 값은?',
                             'stem_en': 'What is the positive real root $t = e^b$ of $(t - 2)(t^2 + t + 2) = 0$?',
                             'options': ['$1$', '$2$', '$3$', '$4$', '$8$'],
                             'answer': 2,
                             'exp': '$t^2 + t + 2 > 0$이므로 실근은 $t = e^b = 2$ ($b = \\ln 2$)입니다.',
                             'exp_en': '$t = e^b = 2$.'}]},
             {'title': '🌱 3단계 · [연속 조건] $x = b$에서 함숫값 같다고 놓아 상수 $a$ 구하기',
              'title_en': '🌱 Step 3 · [Continuity] Finding $a$ from continuity at $x = b$',
              'knowledge': '$e^b = 2$를 양쪽 함숫값 $e^{2b} - 2 = 2e^b - 8e^{-b} + a$에 대입하면 $4 - 2 = 4 - 4 + a$가 됩니다.',
              'knowledge_en': 'Substituting $e^b = 2$ into $e^{2b} - 2 = 2e^b - 8e^{-b} + a$ gives $4 - 2 = 4 - 4 + '
                              'a$.',
              'questions': [{'level_label': '상수 a 구하기 디딤돌 3',
                             'level_label_en': 'Finding a Step 3',
                             'stem': '$4 - 2 = 4 - 4 + a$에서 상수 $a$의 값은?',
                             'stem_en': 'From $4 - 2 = 4 - 4 + a$, what is $a$?',
                             'options': ['$0$', '$1$', '$2$', '$3$', '$4$'],
                             'answer': 3,
                             'exp': '$a = 2$입니다.',
                             'exp_en': '$a = 2$.'}]},
             {'title': '🌳 4단계 · [$f(c) = 8$ 풀기] $2e^c - 8e^{-c} + 2 = 8$을 만족하는 $e^c$ 찾기',
              'title_en': '🌳 Step 4 · [Solving $f(c) = 8$] Finding $e^c$ such that $f(c) = 8$',
              'knowledge': '$x = b$일 때 $f(b) = 2 < 8$이므로 $f(c) = 8$인 $c$는 $c > b$ 범위에 있습니다. $2e^c - 8e^{-c} + 2 = 8 '
                           '\\implies e^c - 4e^{-c} - 3 = 0 \\implies (e^c - 4)(e^c + 1) = 0$입니다.',
              'knowledge_en': 'Since $f(b) = 2 < 8$, $c > b$. Solving $2e^c - 8e^{-c} + 2 = 8$ gives $(e^c - 4)(e^c + '
                              '1) = 0$.',
              'questions': [{'level_label': '$e^c$ 값과 미분계수 디딤돌 4',
                             'level_label_en': "Derivative $f'(c)$ Step 4",
                             'stem': "$e^c = 4$일 때, $f'(c) = 2e^c + 8e^{-c} = 2(4) + 8\\left(\\frac{1}{4}\\right)$의 "
                                     '값은?',
                             'stem_en': "When $e^c = 4$, what is $f'(c) = 2e^c + 8e^{-c} = 2(4) + "
                                        '8\\left(\\frac{1}{4}\\right)$?',
                             'options': ['$6$', '$8$', '$10$', '$12$', '$14$'],
                             'answer': 3,
                             'exp': '$8 + 2 = 10$입니다.',
                             'exp_en': '$8 + 2 = 10$.'}]},
             {'title': "💎 5단계 · [최종 종합] $g'(8) = \\dfrac{1}{f'(c)}$ 확정하기",
              'title_en': "💎 Step 5 · [Final Synthesis] Final value of $g'(8)$",
              'knowledge': "$f'(c) = 10$이므로 $g'(8) = \\frac{1}{10}$입니다.",
              'knowledge_en': "Since $f'(c) = 10$, $g'(8) = \\frac{1}{10}$.",
              'questions': [{'level_label': '최종 종합 디딤돌 5',
                             'level_label_en': 'Final Synthesis Step 5',
                             'stem': "역함수 $g(x)$에 대하여 $g'(8)$의 값은?",
                             'stem_en': "What is the value of $g'(8)$?",
                             'options': ['$\\frac{1}{16}$',
                                         '$\\frac{1}{14}$',
                                         '$\\frac{1}{12}$',
                                         '$\\frac{1}{10}$',
                                         '$\\frac{1}{8}$'],
                             'answer': 4,
                             'exp': "$g'(8) = \\frac{1}{10}$이므로 정답은 ④입니다.",
                             'exp_en': '$\\frac{1}{10}$ (choice ④).'}]}],
  'final': {'stem': '두 상수 $a, b$에 대하여 실수 전체의 집합에서 미분가능한 함수 $f(x)$가 $x < b$일 때 $f(x) = e^{2x} - 2$, $x \\ge b$일 때 $f(x) '
                    "= 2e^x - 8e^{-x} + a$이다. 함수 $f(x)$의 역함수를 $g(x)$라 할 때, $g'(8)$의 값은? [3점]",
            'stem_en': 'A function $f(x)$ differentiable on $\\mathbb{R}$ is defined by $f(x) = e^{2x} - 2$ for $x < '
                       'b$ and $f(x) = 2e^x - 8e^{-x} + a$ for $x \\ge b$. Let $g(x)$ be the inverse function of '
                       "$f(x)$. What is the value of $g'(8)$? [3 points]",
            'options': ['$\\dfrac{1}{16}$',
                        '$\\dfrac{1}{14}$',
                        '$\\dfrac{1}{12}$',
                        '$\\dfrac{1}{10}$',
                        '$\\dfrac{1}{8}$'],
            'answer': 4,
            'exp': "$x = b$에서의 미분가능성으로 $e^b = 2$, $a = 2$를 얻고, $f(c) = 8$ ($c \\ge \\ln 2$)에서 $e^c = 4$이므로 $g'(8) = "
                   "\\dfrac{1}{f'(\\ln 4)} = \\dfrac{1}{2(4) + 8(1/4)} = \\dfrac{1}{10}$입니다.",
            'exp_en': 'Differentiability at $x = b$ gives $e^b = 2$ and $a = 2$. Solving $f(c) = 8$ gives $e^c = 4$, '
                      "so $g'(8) = \\dfrac{1}{f'(\\ln 4)} = \\dfrac{1}{10}$.",
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>구간별로 정의된 지수함수의 미분가능성</b>과 <b>역함수의 미분법</b>을 결합한 문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: $x = b$에서의 미분가능 조건으로 $e^b$와 $a$ 구하기</b><br>\n'
                        '  미분계수가 일치해야 하므로 $2e^{2b} = 2e^b + 8e^{-b}$입니다. $t = e^b > 0$이라 하면:<br>\n'
                        '  $$t^3 - t^2 - 4 = (t - 2)(t^2 + t + 2) = 0 \\implies t = e^b = 2$$\n'
                        '  연속 조건 $e^{2b} - 2 = 2e^b - 8e^{-b} + a$에 $e^b = 2$를 대입하면 $4 - 2 = 4 - 4 + a \\implies a = '
                        '2$입니다.<br><br>\n'
                        "  <b>2단계: 역함수의 미분법으로 $g'(8)$ 구하기</b><br>\n"
                        '  $f(b) = 2 < 8$이므로 $f(c) = 8$인 $c$는 $c > b$에 존재합니다:<br>\n'
                        '  $$2e^c - 8e^{-c} + 2 = 8 \\implies (e^c - 4)(e^c + 1) = 0 \\implies e^c = 4$$\n'
                        "  따라서 $f'(c) = 2e^c + 8e^{-c} = 2(4) + 8\\left(\\frac{1}{4}\\right) = 10$이므로:<br>\n"
                        "  $$g'(8) = \\frac{1}{f'(c)} = \\frac{1}{10}$$\n"
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        "  따라서 $g'(8) = \\dfrac{1}{10}$이므로 정답은 <b>④번</b>입니다.\n"
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem combines <b>differentiability at a boundary point</b> with the <b>Inverse '
                           'Function Theorem</b>.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Continuity and differentiability at $x = b$</b><br>\n'
                           '  $$2e^{2b} = 2e^b + 8e^{-b} \\implies e^b = 2, \\quad e^{2b} - 2 = 2e^b - 8e^{-b} + a '
                           '\\implies a = 2$$<br>\n'
                           '  <b>Step 2: Derivative of the inverse at $y = 8$</b><br>\n'
                           "  From $2e^c - 8e^{-c} + 2 = 8$, we get $e^c = 4$. Thus $f'(c) = 2(4) + 8(1/4) = 10$ and "
                           "$g'(8) = \\frac{1}{10}$.\n"
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  The correct answer is <b>choice ④ ($\\dfrac{1}{10}$)</b>.\n'
                           '</p>'}},
 {'slug': 'c2610m28',
  'qNum': '미적 28',
  'subject': '미적분',
  'title': '[2026학년도 10월 고3 미적 28번] 곡선과 직선의 접점 매개변수화 및 음함수·합성함수 미분법',
  'title_en': '[2026 AY Oct Exam Grade 12 Calculus #28] Tangent Parameterization and Implicit Differentiation',
  'summary_ko': "$f'(s)=s\\sec^2 s=\\dfrac{s}{t}$에서 $t=\\cos^2 s$를 얻고 $g(t)=f(s)-\\dfrac{s^2}{t}$를 미분하여 "
                "$g'\\!\\left(\\dfrac{1}{2}\\right)=\\dfrac{\\pi^2+2\\pi}{4}$ 구하기",
  'summary_en': "From $f'(s)=s\\sec^2 s=\\dfrac{s}{t}$ deduce $t=\\cos^2 s$, differentiate $g(t)=f(s)-\\dfrac{s^2}{t}$ "
                "with respect to $t$, and evaluate $g'\\!\\left(\\dfrac{1}{2}\\right)=\\dfrac{\\pi^2+2\\pi}{4}$.",
  'tags': ['미적분', '미분법', '접선의방정식', '매개변수미분법', '삼각함수의미분', '28번'],
  'symbols': [{'sym': "$f'(s) = s\\sec^2 s$",
               'desc': '$f(x)=x\\tan x - \\ln(\\sec x)$를 미분하여 간단히 정리한 도함수',
               'desc_en': 'Simplified derivative of $f(x)=x\\tan x - \\ln(\\sec x)$.'},
              {'sym': '$t = \\cos^2 s$',
               'desc': "접점의 $x$좌표 $s$에서 $f'(s) = \\dfrac{s}{t}$가 성립할 조건",
               'desc_en': 'Relation between parameter $t$ and point of tangency $s$.'},
              {'sym': "$g'(t) = -\\dfrac{s}{t}\\dfrac{ds}{dt} + \\dfrac{s^2}{t^2}$",
               'desc': '접선의 $y$절편 $g(t) = f(s) - \\dfrac{s^2}{t}$를 $t$에 대해 미분한 도함수',
               'desc_en': 'Derivative of the $y$-intercept $g(t)$ with respect to $t$.'}],
  'levels': [{'title': "🔰 1단계 · [초등 소거 규칙과 로그 미분] $(\\ln(\\sec x))' = \\tan x$를 이용해 $f'(x)$ 간단히 하기",
              'title_en': "🔰 Step 1 · [Elementary Cancellation & Log Derivative] Simplifying $f'(x)$ using "
                          "$(\\ln(\\sec x))' = \\tan x$",
              'knowledge': '함수 $f(x) = x\\tan x - \\ln(\\sec x)$를 미분해 봅시다!<ul><li>앞부분 $x\\tan x$를 곱의 미분법으로 미분하면: '
                           '$1\\cdot\\tan x + x\\sec^2 x$</li><li>뒷부분 $\\ln(\\sec x)$를 합성함수 미분법으로 미분하면: '
                           "$\\dfrac{(\\sec x)'}{\\sec x} = \\dfrac{\\sec x \\tan x}{\\sec x} = \\tan x$</li></ul>따라서 "
                           '두 식을 빼면 초등학교 덧셈·뺄셈 소거처럼 $\\tan x - \\tan x = 0$이 지워집니다!',
              'knowledge_en': "Differentiating $f(x) = x\\tan x - \\ln(\\sec x)$: the product rule gives $(x\\tan x)' "
                              "= \\tan x + x\\sec^2 x$, and the chain rule gives $(\\ln(\\sec x))' = \\frac{\\sec "
                              'x\\tan x}{\\sec x} = \\tan x$. Subtracting cancels $\\tan x - \\tan x = 0$!',
              'questions': [{'level_label': '초등 항 소거 디딤돌 1',
                             'level_label_en': 'Elementary Cancellation Step 1',
                             'stem': "$f'(x) = (\\tan x + x\\sec^2 x) - \\tan x$에서 $\\tan x - \\tan x = 0$을 소거하고 남는 "
                                     "도함수 $f'(x)$는?",
                             'stem_en': "After canceling $\\tan x - \\tan x = 0$ in $f'(x) = (\\tan x + x\\sec^2 x) - "
                                        "\\tan x$, what remains for $f'(x)$?",
                             'options': ['$\\tan x$', '$x\\sec^2 x$', '$2\\tan x$', '$\\sec^2 x$', '$x\\tan x$'],
                             'answer': 2,
                             'exp': "$\\tan x$가 소거되어 $f'(x) = x\\sec^2 x = \\dfrac{x}{\\cos^2 x}$만 깔끔하게 남습니다.",
                             'exp_en': "$f'(x) = x\\sec^2 x$."}]},
             {'title': "🌿 2단계 · [접선의 기울기 조건] $f'(s) = \\dfrac{s}{t}$에서 $t$와 $s$의 관계식 찾기",
              'title_en': "🌿 Step 2 · [Tangent Slope Condition] Relating $t$ and $s$ from $f'(s) = \\dfrac{s}{t}$",
              'knowledge': "점 $(s, f(s))$에서의 접선 $l$의 기울기는 $f'(s) = s\\sec^2 s = \\dfrac{s}{\\cos^2 s}$입니다. 문제에서 이 기울기가 "
                           '$\\dfrac{s}{t}$라고 했고 $0 < s < \\dfrac{\\pi}{2}$이므로 양변의 $s$를 약분하면 $\\dfrac{1}{\\cos^2 s} = '
                           '\\dfrac{1}{t}$, 즉 $t = \\cos^2 s$를 얻습니다!',
              'knowledge_en': "Equating $f'(s) = \\frac{s}{\\cos^2 s} = \\frac{s}{t}$ for $s \\in \\left(0, "
                              '\\frac{\\pi}{2}\\right)$ yields $t = \\cos^2 s$.',
              'questions': [{'level_label': '매개변수 관계식 디딤돌 2',
                             'level_label_en': 'Parameter Relation Step 2',
                             'stem': '$\\dfrac{s}{\\cos^2 s} = \\dfrac{s}{t}$ ($s > 0$)에서 분모끼리 비교하여 얻는 $t$를 $s$로 나타낸 '
                                     '식은?',
                             'stem_en': 'Comparing denominators in $\\dfrac{s}{\\cos^2 s} = \\dfrac{s}{t}$, what is '
                                        '$t$ in terms of $s$?',
                             'options': ['$\\sin^2 s$', '$\\cos^2 s$', '$\\tan^2 s$', '$\\sec^2 s$', '$\\cos s$'],
                             'answer': 2,
                             'exp': '$t = \\cos^2 s$입니다.',
                             'exp_en': '$t = \\cos^2 s$.'}]},
             {'title': '🌱 3단계 · [특수각 대입] $t = \\dfrac{1}{2}$일 때 접점의 $x$좌표 $s$ 구하기',
              'title_en': '🌱 Step 3 · [Special Angle] Finding $s$ when $t = \\dfrac{1}{2}$',
              'knowledge': "구하려는 값은 $g'\\!\\left(\\dfrac{1}{2}\\right)$, 즉 $t = \\dfrac{1}{2}$일 때입니다. $t = \\cos^2 s = "
                           '\\dfrac{1}{2}$이고 $0 < s < \\dfrac{\\pi}{2}$이므로 $\\cos s = \\dfrac{\\sqrt{2}}{2}$입니다.',
              'knowledge_en': 'When $t = \\cos^2 s = \\frac{1}{2}$ with $0 < s < \\frac{\\pi}{2}$, we have $\\cos s = '
                              '\\frac{\\sqrt{2}}{2}$.',
              'questions': [{'level_label': '접점 좌표 s 디딤돌 3',
                             'level_label_en': 'Point of Tangency s Step 3',
                             'stem': '열린구간 $\\left(0, \\dfrac{\\pi}{2}\\right)$에서 $\\cos s = \\dfrac{\\sqrt{2}}{2}$를 '
                                     '만족시키는 $s$의 값은?',
                             'stem_en': 'Which $s \\in \\left(0, \\dfrac{\\pi}{2}\\right)$ satisfies $\\cos s = '
                                        '\\dfrac{\\sqrt{2}}{2}$?',
                             'options': ['$\\frac{\\pi}{6}$',
                                         '$\\frac{\\pi}{4}$',
                                         '$\\frac{\\pi}{3}$',
                                         '$\\frac{\\pi}{2}$',
                                         '$\\frac{\\pi}{8}$'],
                             'answer': 2,
                             'exp': '$\\cos\\left(\\dfrac{\\pi}{4}\\right) = \\dfrac{\\sqrt{2}}{2}$이므로 $s = '
                                    '\\dfrac{\\pi}{4}$입니다.',
                             'exp_en': '$s = \\dfrac{\\pi}{4}$.'}]},
             {'title': '🌱 4단계 · [음함수 미분법] $t = \\cos^2 s$를 미분하여 $\\dfrac{ds}{dt}$ 구하기',
              'title_en': '🌱 Step 4 · [Implicit Differentiation] Differentiating $t = \\cos^2 s$ to find '
                          '$\\dfrac{ds}{dt}$',
              'knowledge': '$t = \\cos^2 s$의 양변을 $s$에 대하여 미분하면:$$\\frac{dt}{ds} = 2\\cos s(-\\sin s) = -\\sin(2s)$$여기에 '
                           '$s = \\dfrac{\\pi}{4}$를 대입하면 $\\dfrac{dt}{ds}$와 그 역수인 $\\dfrac{ds}{dt}$를 구할 수 있습니다.',
              'knowledge_en': 'Differentiating $t = \\cos^2 s$ gives $\\frac{dt}{ds} = -2\\cos s\\sin s = -\\sin(2s)$.',
              'questions': [{'level_label': '미분계수 $\\dfrac{\\mathrm{d}s}{\\mathrm{d}t}$ 디딤돌 4',
                             'level_label_en': 'Derivative $\\dfrac{\\mathrm{d}s}{\\mathrm{d}t}$ Step 4',
                             'stem': '$s = \\dfrac{\\pi}{4}$일 때, $\\dfrac{dt}{ds} = -\\sin\\left(2 \\times '
                                     '\\dfrac{\\pi}{4}\\right) = -\\sin\\left(\\dfrac{\\pi}{2}\\right)$의 값은?',
                             'stem_en': 'At $s = \\dfrac{\\pi}{4}$, what is $\\dfrac{dt}{ds} = '
                                        '-\\sin\\left(\\dfrac{\\pi}{2}\\right)$?',
                             'options': ['$-2$', '$-1$', '$0$', '$1$', '$2$'],
                             'answer': 2,
                             'exp': '$-\\sin\\left(\\dfrac{\\pi}{2}\\right) = -1$이므로 역수인 $\\dfrac{ds}{dt}$도 $-1$입니다.',
                             'exp_en': '$\\dfrac{dt}{ds} = -1 \\implies \\dfrac{ds}{dt} = -1$.'}]},
             {'title': '🌳 5단계 · [접선의 $y$절편 $g(t)$ 식 세우기] 접점 $(s, f(s))$와 기울기 $\\dfrac{s}{t}$로 $g(t)$ 나타내기',
              'title_en': '🌳 Step 5 · [Formula for $y$-Intercept $g(t)$] Writing $g(t) = f(s) - \\dfrac{s^2}{t}$',
              'knowledge': '점 $(s, f(s))$를 지나고 기울기가 $\\dfrac{s}{t}$인 접선 $l$의 방정식은:$$y = \\frac{s}{t}(x - s) + f(s) = '
                           '\\frac{s}{t}x + \\left\\{f(s) - \\frac{s^2}{t}\\right\\}$$따라서 직선 $l$의 $y$절편($x = 0$일 때의 '
                           '$y$값) $g(t)$는 $f(s) - \\dfrac{s^2}{t}$입니다!',
              'knowledge_en': 'The tangent line at $(s, f(s))$ with slope $\\frac{s}{t}$ is $y = \\frac{s}{t}(x - s) + '
                              'f(s) = \\frac{s}{t}x + f(s) - \\frac{s^2}{t}$, so its $y$-intercept is $g(t) = f(s) - '
                              '\\frac{s^2}{t}$.',
              'questions': [{'level_label': 'y절편 식 도출 디딤돌 5',
                             'level_label_en': 'y-Intercept Formula Step 5',
                             'stem': '접선 $y - f(s) = \\dfrac{s}{t}(x - s)$에 $x = 0$을 대입하여 구한 $y$절편 $g(t)$의 식은?',
                             'stem_en': 'Substituting $x = 0$ into $y - f(s) = \\dfrac{s}{t}(x - s)$, what is the '
                                        '$y$-intercept $g(t)$?',
                             'options': ['$f(s) + \\frac{s^2}{t}$',
                                         '$f(s) - \\frac{s^2}{t}$',
                                         '$f(s) - \\frac{s}{t}$',
                                         '$\\frac{s^2}{t} - f(s)$',
                                         '$s f(s) - \\frac{s}{t}$'],
                             'answer': 2,
                             'exp': '$x = 0$을 대입하면 $g(t) = f(s) - \\dfrac{s^2}{t}$입니다.',
                             'exp_en': '$g(t) = f(s) - \\dfrac{s^2}{t}$.'}]},
             {'title': '🌳 6단계 · [$g(t)$ 미분 정리] $g(t) = f(s) - \\dfrac{s^2}{t}$를 $t$에 대해 미분하기',
              'title_en': "🌳 Step 6 · [Differentiating $g(t)$] Simplifying $g'(t) = -\\dfrac{s}{t}\\dfrac{ds}{dt} + "
                          '\\dfrac{s^2}{t^2}$',
              'knowledge': '$g(t) = f(s) - s^2 \\cdot t^{-1}$의 양변을 $t$에 대하여 미분해 봅시다 ($s$도 $t$에 따라 변하는 함수임에 '
                           "주의!):$$g'(t) = f'(s)\\frac{ds}{dt} - \\frac{2s}{t}\\frac{ds}{dt} + \\frac{s^2}{t^2}$$그런데 "
                           "$f'(s) = \\dfrac{s}{t}$이므로, 앞의 두 항을 합치면 $\\left(\\dfrac{s}{t} - "
                           '\\dfrac{2s}{t}\\right)\\dfrac{ds}{dt} = -\\dfrac{s}{t}\\dfrac{ds}{dt}$로 간단해집니다!',
              'knowledge_en': "Differentiating $g(t) = f(s) - s^2 t^{-1}$ with respect to $t$ and substituting $f'(s) "
                              "= \\frac{s}{t}$ gives $g'(t) = \\left(\\frac{s}{t} - "
                              '\\frac{2s}{t}\\right)\\frac{ds}{dt} + \\frac{s^2}{t^2} = -\\frac{s}{t}\\frac{ds}{dt} + '
                              '\\frac{s^2}{t^2}$.',
              'questions': [{'level_label': '첫째 항 계산 디딤돌 6',
                             'level_label_en': 'First Term Evaluation Step 6',
                             'stem': "$t = \\dfrac{1}{2}$, $s = \\dfrac{\\pi}{4}$, $\\dfrac{ds}{dt} = -1$일 때, $g'(t)$의 "
                                     '첫째 항 $-\\dfrac{s}{t}\\dfrac{ds}{dt}$의 값은?',
                             'stem_en': 'For $t = \\dfrac{1}{2}$, $s = \\dfrac{\\pi}{4}$, and $\\dfrac{ds}{dt} = -1$, '
                                        'what is $-\\dfrac{s}{t}\\dfrac{ds}{dt}$?',
                             'options': ['$\\frac{\\pi}{4}$',
                                         '$\\frac{\\pi}{2}$',
                                         '$\\pi$',
                                         '$-\\frac{\\pi}{2}$',
                                         '$-\\frac{\\pi}{4}$'],
                             'answer': 2,
                             'exp': '$-\\dfrac{\\pi/4}{1/2} \\times (-1) = \\dfrac{\\pi}{2}$입니다.',
                             'exp_en': '$\\dfrac{\\pi}{2}$.'}]},
             {'title': '💎 7단계 · [둘째 항 계산] $t = \\dfrac{1}{2}, s = \\dfrac{\\pi}{4}$일 때 $\\dfrac{s^2}{t^2}$ 구하기',
              'title_en': '💎 Step 7 · [Second Term Evaluation] Computing $\\dfrac{s^2}{t^2}$ at $t = \\dfrac{1}{2}, s '
                          '= \\dfrac{\\pi}{4}$',
              'knowledge': "이제 $g'(t)$의 둘째 항 $\\dfrac{s^2}{t^2} = \\left(\\dfrac{s}{t}\\right)^2$을 계산합니다. "
                           '$\\dfrac{s}{t} = \\dfrac{\\pi/4}{1/2} = \\dfrac{\\pi}{2}$이므로 이를 제곱하면 됩니다!',
              'knowledge_en': 'Since $\\frac{s}{t} = \\frac{\\pi/4}{1/2} = \\frac{\\pi}{2}$, its square is '
                              '$\\left(\\frac{s}{t}\\right)^2 = \\frac{\\pi^2}{4}$.',
              'questions': [{'level_label': '둘째 항 제곱 디딤돌 7',
                             'level_label_en': 'Second Term Square Step 7',
                             'stem': '$\\dfrac{s}{t} = \\dfrac{\\pi}{2}$일 때, $\\dfrac{s^2}{t^2} = '
                                     '\\left(\\dfrac{\\pi}{2}\\right)^2$의 값은?',
                             'stem_en': 'When $\\dfrac{s}{t} = \\dfrac{\\pi}{2}$, what is $\\dfrac{s^2}{t^2}$?',
                             'options': ['$\\frac{\\pi^2}{16}$',
                                         '$\\frac{\\pi^2}{8}$',
                                         '$\\frac{\\pi^2}{4}$',
                                         '$\\frac{\\pi^2}{2}$',
                                         '$\\pi^2$'],
                             'answer': 3,
                             'exp': '$\\left(\\dfrac{\\pi}{2}\\right)^2 = \\dfrac{\\pi^2}{4}$입니다.',
                             'exp_en': '$\\dfrac{\\pi^2}{4}$.'}]},
             {'title': "🏆 8단계 · [최종 정답 완성] $g'\\!\\left(\\dfrac{1}{2}\\right) = \\dfrac{\\pi}{2} + \\dfrac{\\pi^2}{4}$ "
                       '통분하여 더하기',
              'title_en': '🏆 Step 8 · [Final Synthesis] Combining $\\dfrac{\\pi}{2} + \\dfrac{\\pi^2}{4}$',
              'knowledge': '6단계에서 구한 $\\dfrac{\\pi}{2}$와 7단계에서 구한 $\\dfrac{\\pi^2}{4}$를 분모 $4$로 통분하여 더하면 최종 정답이 완성됩니다!',
              'knowledge_en': 'Combine $\\frac{\\pi}{2} + \\frac{\\pi^2}{4} = \\frac{\\pi^2 + 2\\pi}{4}$.',
              'questions': [{'level_label': '최종 종합 디딤돌 8',
                             'level_label_en': 'Final Synthesis Step 8',
                             'stem': "$g'\\!\\left(\\dfrac{1}{2}\\right) = \\dfrac{\\pi}{2} + \\dfrac{\\pi^2}{4}$를 계산한 "
                                     '최종 정답은?',
                             'stem_en': "What is the value of $g'\\!\\left(\\dfrac{1}{2}\\right) = \\dfrac{\\pi}{2} + "
                                        '\\dfrac{\\pi^2}{4}$?',
                             'options': ['$\\frac{\\pi^2 + 2\\pi}{8}$',
                                         '$\\frac{\\pi^2 + \\pi}{4}$',
                                         '$\\frac{\\pi^2 + 2\\pi}{4}$',
                                         '$\\frac{\\pi^2 + \\pi}{2}$',
                                         '$\\frac{\\pi^2 + 2\\pi}{2}$'],
                             'answer': 3,
                             'exp': '$\\dfrac{2\\pi}{4} + \\dfrac{\\pi^2}{4} = \\dfrac{\\pi^2 + 2\\pi}{4}$이므로 정답은 '
                                    '③입니다.',
                             'exp_en': '$\\dfrac{\\pi^2 + 2\\pi}{4}$ (choice ③).'}]}],
  'final': {'stem': '열린구간 $\\left(0, \\dfrac{\\pi}{2}\\right)$에서 정의된 함수 $f(x) = x\\tan x - \\ln(\\sec x)$가 있다. $0 < t '
                    '< 1$인 실수 $t$에 대하여 곡선 $y = f(x)$ 위의 점 $(s, f(s))$에서의 접선 $l$의 기울기가 $\\dfrac{s}{t}$가 되도록 하는 직선 $l$의 '
                    "$y$절편을 $g(t)$라 하자. $g'\\!\\left(\\dfrac{1}{2}\\right)$의 값은? [4점]",
            'stem_en': 'Consider $f(x) = x\\tan x - \\ln(\\sec x)$ on $\\left(0, \\dfrac{\\pi}{2}\\right)$. For $0 < t '
                       '< 1$, let $g(t)$ be the $y$-intercept of the tangent line $l$ to $y = f(x)$ at $(s, f(s))$ '
                       "whose slope is $\\dfrac{s}{t}$. What is the value of $g'\\!\\left(\\dfrac{1}{2}\\right)$? [4 "
                       'points]',
            'options': ['$\\dfrac{\\pi^2 + 2\\pi}{8}$',
                        '$\\dfrac{\\pi^2 + \\pi}{4}$',
                        '$\\dfrac{\\pi^2 + 2\\pi}{4}$',
                        '$\\dfrac{\\pi^2 + \\pi}{2}$',
                        '$\\dfrac{\\pi^2 + 2\\pi}{2}$'],
            'answer': 3,
            'exp': "$f'(s) = s\\sec^2 s = \\dfrac{s}{t}$에서 $t = \\cos^2 s$이고, $g(t) = f(s) - \\dfrac{s^2}{t}$를 미분하면 "
                   "$g'(t) = -\\dfrac{s}{t}\\dfrac{ds}{dt} + \\dfrac{s^2}{t^2}$입니다. $t = \\dfrac{1}{2}$일 때 $s = "
                   "\\dfrac{\\pi}{4}, \\dfrac{ds}{dt} = -1$이므로 $g'\\!\\left(\\dfrac{1}{2}\\right) = \\dfrac{\\pi^2 + "
                   '2\\pi}{4}$입니다.',
            'exp_en': "From $f'(s) = s\\sec^2 s = \\dfrac{s}{t}$, we get $t = \\cos^2 s$. Differentiating $g(t) = f(s) "
                      "- \\dfrac{s^2}{t}$ gives $g'(t) = -\\dfrac{s}{t}\\dfrac{ds}{dt} + \\dfrac{s^2}{t^2}$. "
                      'Evaluating at $t = \\dfrac{1}{2}$ ($s = \\dfrac{\\pi}{4}, \\dfrac{ds}{dt} = -1$) yields '
                      '$\\dfrac{\\pi^2 + 2\\pi}{4}$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>접점의 좌표 $s$와 매개변수 $t$ 사이의 관계식을 도출하고 합성함수(음함수) 미분법</b>을 적용하는 미적분 4점 문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        "  <b>1단계: 도함수 $f'(x)$와 $t = \\cos^2 s$ 도출</b><br>\n"
                        "  $$f'(x) = (\\tan x + x\\sec^2 x) - \\frac{\\sec x \\tan x}{\\sec x} = x\\sec^2 x$$\n"
                        '  점 $(s, f(s))$에서의 접선의 기울기가 $\\frac{s}{t}$이므로:<br>\n'
                        '  $$s\\sec^2 s = \\frac{s}{t} \\implies t = \\cos^2 s$$<br>\n'
                        '  <b>2단계: $g(t)$의 도함수 구하기</b><br>\n'
                        '  접선 $y = \\frac{s}{t}(x - s) + f(s)$의 $y$절편은 $g(t) = f(s) - \\frac{s^2}{t}$입니다. 양변을 $t$에 대하여 '
                        "미분하고 $f'(s) = \\frac{s}{t}$를 대입하면:<br>\n"
                        "  $$g'(t) = f'(s)\\frac{ds}{dt} - \\frac{2s}{t}\\frac{ds}{dt} + \\frac{s^2}{t^2} = "
                        '-\\frac{s}{t}\\frac{ds}{dt} + \\frac{s^2}{t^2}$$<br>\n'
                        '  <b>3단계: $t = \\frac{1}{2}$에서의 미분계수 계산</b><br>\n'
                        '  $t = \\cos^2 s = \\frac{1}{2}$ ($0 < s < \\frac{\\pi}{2}$)에서 $s = \\frac{\\pi}{4}$이고, '
                        '$\\frac{dt}{ds} = -\\sin(2s) = -1 \\implies \\frac{ds}{dt} = -1$입니다.<br>\n'
                        "  $$g'\\!\\left(\\frac{1}{2}\\right) = -\\frac{\\pi/4}{1/2}(-1) + \\frac{\\pi^2/16}{1/4} = "
                        '\\frac{\\pi}{2} + \\frac{\\pi^2}{4} = \\frac{\\pi^2 + 2\\pi}{4}$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        "  따라서 $g'\\!\\left(\\dfrac{1}{2}\\right) = \\dfrac{\\pi^2 + 2\\pi}{4}$이므로 정답은 <b>③번</b>입니다.\n"
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem applies <b>implicit and parametric differentiation</b> to the '
                           '$y$-intercept $g(t)$ of a tangent line.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Relate $t$ and $s$</b><br>\n'
                           "  $$f'(s) = s\\sec^2 s = \\frac{s}{t} \\implies t = \\cos^2 s$$<br>\n"
                           '  <b>Step 2: Differentiate $g(t) = f(s) - \\frac{s^2}{t}$</b><br>\n'
                           "  $$g'(t) = \\left(f'(s) - \\frac{2s}{t}\\right)\\frac{ds}{dt} + \\frac{s^2}{t^2} = "
                           '-\\frac{s}{t}\\frac{ds}{dt} + \\frac{s^2}{t^2}$$\n'
                           '  At $t = \\frac{1}{2}$, $s = \\frac{\\pi}{4}$ and $\\frac{dt}{ds} = '
                           "-\\sin\\left(\\frac{\\pi}{2}\\right) = -1$, giving $g'\\!\\left(\\frac{1}{2}\\right) = "
                           '\\frac{\\pi}{2} + \\frac{\\pi^2}{4} = \\frac{\\pi^2 + 2\\pi}{4}$.\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  The correct answer is <b>choice ③ ($\\dfrac{\\pi^2 + 2\\pi}{4}$)</b>.\n'
                           '</p>'}},
 {'slug': 'c2610m29',
  'qNum': '미적 29',
  'subject': '미적분',
  'title': '[2026학년도 10월 고3 미적 29번] 등차수열과 등비수열의 결합 및 등비급수의 합',
  'title_en': '[2026 AY Oct Exam Grade 12 Calculus #29] Arithmetic and Geometric Sequences and Infinite Geometric '
              'Series',
  'summary_ko': '정수 조건과 $a_{k+27}-a_k=b_4-b_3=27d$에서 $r=-\\dfrac{1}{2},\\ d=-1,\\ k=5$를 도출해 급수의 합 $\\dfrac{144}{11}$ '
                '구하기',
  'summary_en': 'From integer constraints and $b_4-b_3=27d$, deduce $r=-\\dfrac{1}{2},\\ d=-1,\\ k=5$ and evaluate the '
                'infinite series to $\\dfrac{144}{11}$ ($p+q=155$).',
  'tags': ['미적분', '수열의극한', '등비급수', '등차수열', '등비수열', '단답형', '29번'],
  'symbols': [{'sym': '$-1 < r < 1 \\quad (r \\neq 0)$',
               'desc': '조건 (나)의 등비급수 $\\sum_{n=k}^\\infty b_n$이 수렴하기 위한 공비 $r$의 범위',
               'desc_en': 'Convergence condition for the infinite geometric series in (나).'},
              {'sym': '$b_4 - b_3 = 72r^2(r - 1) = 27d$',
               'desc': '조건 (가) $a_k=b_3,\\ a_{k+27}=b_4$와 정수 공차 $d$를 연결하는 핵심 등식',
               'desc_en': 'Relation connecting geometric terms $b_3, b_4$ with integer common difference $d$.'},
              {'sym': '$\\sum_{n=k}^{\\infty} b_n = \\dfrac{b_k}{1 - r} = a_{k+15}$',
               'desc': '$k$번째 항부터 시작하는 등비급수의 합 공식',
               'desc_en': 'Sum of the geometric series starting from the $k$-th term.'}],
  'levels': [{'title': '🔰 1단계 · [초등 등간격 건너뛰기] $a_{k+27} - a_k$를 공차 $d$로 나타내기',
              'title_en': '🔰 Step 1 · [Elementary Equal Steps] Expressing $a_{k+27} - a_k$ in terms of $d$',
              'knowledge': '등차수열 $\\{a_n\\}$은 한 칸 갈 때마다 공차 $d$씩 더해지는 수열입니다. 따라서 $k$번째 항 $a_k$에서 $27$칸 뒤의 항 '
                           '$a_{k+27}$까지는 공차 $d$가 정확히 $27$번 더해집니다!',
              'knowledge_en': 'In an arithmetic sequence $\\{a_n\\}$ with common difference $d$, moving $27$ steps '
                              'from $a_k$ to $a_{k+27}$ adds $27d$.',
              'questions': [{'level_label': '초등 간격 계산 디딤돌 1',
                             'level_label_en': 'Elementary Step Difference Step 1',
                             'stem': '조건 (가)에서 $a_k = b_3$, $a_{k+27} = b_4$이고 등차수열 $\\{a_n\\}$의 공차가 정수 $d$일 때, $b_4 - '
                                     'b_3 = a_{k+27} - a_k$는 $d$의 몇 배인가요?',
                             'stem_en': 'Given $a_k = b_3$ and $a_{k+27} = b_4$, $b_4 - b_3 = a_{k+27} - a_k$ is what '
                                        'multiple of $d$?',
                             'options': ['$12d$', '$15d$', '$18d$', '$24d$', '$27d$'],
                             'answer': 5,
                             'exp': '$(k + 27) - k = 27$칸 차이므로 $b_4 - b_3 = 27d$입니다.',
                             'exp_en': '$b_4 - b_3 = 27d$.'}]},
             {'title': '🌿 2단계 · [정수 조건과 공비 $r$ 찾기] $b_3 = 72r^2, b_4 = 72r^3$이 정수이고 차가 $27$의 배수가 되는 공비 $r$',
              'title_en': '🌿 Step 2 · [Integer Condition & Common Ratio $r$] Finding $r \\in (-1, 1)$ such that $b_4 - '
                          'b_3 = 27d$',
              'knowledge': '조건 (나)에서 무한등비급수 $\\sum_{n=k}^\\infty b_n$이 수렴하므로 공비 $r$의 범위는 $-1 < r < 1$ ($r \\neq '
                           '0$)입니다! 또한 $\\{a_n\\}$의 모든 항은 정수이므로 $b_3 = 72r^2$과 $b_4 = 72r^3$도 모두 정수여야 하고, 그 차 $b_4 - '
                           'b_3 = 72r^2(r - 1) = 27d$는 **$27$의 배수**여야 합니다!<ul><li>$r = -\\dfrac{1}{2}$을 대입해 볼까요? $b_3 '
                           '= 72 \\times \\dfrac{1}{4} = 18$, $b_4 = 72 \\times \\left(-\\dfrac{1}{8}\\right) = -9$가 '
                           '되어 $b_4 - b_3 = -9 - 18 = -27$ (정확히 $27 \\times (-1)$!)이 됩니다!</li></ul>',
              'knowledge_en': 'Since $\\sum_{n=k}^\\infty b_n$ converges, $-1 < r < 1$. Also $b_3 = 72r^2$ and $b_4 = '
                              '72r^3$ must be integers whose difference $72r^2(r-1) = 27d$ is a multiple of $27$. '
                              'Testing $r = -\\frac{1}{2}$ gives $b_3 = 18$ and $b_4 = -9$, so $b_4 - b_3 = -27 = '
                              '27(-1)$!',
              'questions': [{'level_label': '공비와 공차 결정 디딤돌 2',
                             'level_label_en': 'Finding r and d Step 2',
                             'stem': '$b_1 = 72$, 공비 $r = -\\dfrac{1}{2}$일 때 $a_k = b_3 = 18$, $a_{k+27} = b_4 = '
                                     '-9$입니다. $27d = -9 - 18 = -27$에서 등차수열 $\\{a_n\\}$의 공차 $d$는?',
                             'stem_en': 'When $r = -\\dfrac{1}{2}$, we have $b_3 = 18$ and $b_4 = -9$. From $27d = '
                                        '-27$, what is the integer common difference $d$?',
                             'options': ['$-3$', '$-2$', '$-1$', '$1$', '$2$'],
                             'answer': 3,
                             'exp': '$27d = -27 \\implies d = -1$입니다.',
                             'exp_en': '$d = -1$.'}]},
             {'title': '🌱 3단계 · [조건 (나)의 우변 계산] $a_{k+15} = a_k + 15d$의 값 구하기',
              'title_en': '🌱 Step 3 · [RHS of Condition (나)] Computing $a_{k+15} = a_k + 15d$',
              'knowledge': '$a_k = 18$이고 공차 $d = -1$이므로, $k$번째 항에서 $15$칸 뒤의 항 $a_{k+15}$는 $18$에서 $1$씩 $15$번 줄어든 값입니다.',
              'knowledge_en': 'With $a_k = 18$ and $d = -1$, moving $15$ steps gives $a_{k+15} = 18 + 15(-1)$.',
              'questions': [{'level_label': '$a_{k+15}$ 함숫값 디딤돌 3',
                             'level_label_en': 'Evaluating $a_{k+15}$ Step 3',
                             'stem': '$a_k = 18$, $d = -1$일 때, 조건 (나)의 우변 $a_{k+15} = a_k + 15d$의 값은?',
                             'stem_en': 'Given $a_k = 18$ and $d = -1$, what is $a_{k+15} = 18 + 15(-1)$?',
                             'options': ['$1$', '$2$', '$3$', '$4$', '$5$'],
                             'answer': 3,
                             'exp': '$18 - 15 = 3$입니다.',
                             'exp_en': '$18 - 15 = 3$.'}]},
             {'title': '🌱 4단계 · [조건 (나)의 좌변 등비급수] $\\sum_{n=k}^{\\infty} b_n = \\dfrac{b_k}{1 - r} = 3$에서 $b_k$ 구하기',
              'title_en': '🌱 Step 4 · [LHS Infinite Series] Finding $b_k$ from $\\dfrac{b_k}{1 - (-1/2)} = 3$',
              'knowledge': '$n = k$부터 시작하는 등비급수 $\\sum_{n=k}^{\\infty} b_n$은 **첫째항이 $b_k$**이고 공비가 $r = '
                           '-\\dfrac{1}{2}$입니다! 따라서 등비급수의 합 공식에 의해:$$\\sum_{n=k}^{\\infty} b_n = \\frac{b_k}{1 - '
                           '\\left(-\\frac{1}{2}\\right)} = \\frac{b_k}{\\frac{3}{2}} = \\frac{2}{3}b_k = 3$$',
              'knowledge_en': 'The series $\\sum_{n=k}^\\infty b_n$ starts at $b_k$ with ratio $r = -\\frac{1}{2}$, so '
                              'its sum is $\\frac{b_k}{1 - (-1/2)} = \\frac{2}{3}b_k = 3$.',
              'questions': [{'level_label': '$b_k$ 값 도출 디딤돌 4',
                             'level_label_en': 'Finding $b_k$ Step 4',
                             'stem': '$\\dfrac{2}{3}b_k = 3$의 양변에 $\\dfrac{3}{2}$을 곱하여 구한 $b_k$의 값은?',
                             'stem_en': 'Solving $\\dfrac{2}{3}b_k = 3$, what is $b_k$?',
                             'options': ['$\\frac{3}{2}$', '$3$', '$\\frac{9}{2}$', '$6$', '$9$'],
                             'answer': 3,
                             'exp': '$b_k = 3 \\times \\dfrac{3}{2} = \\dfrac{9}{2}$입니다.',
                             'exp_en': '$b_k = \\dfrac{9}{2}$.'}]},
             {'title': '🌳 5단계 · [자연수 $k$ 확정] $b_k = \\dfrac{9}{2}$이 되는 항 번호 $k$ 찾기',
              'title_en': '🌳 Step 5 · [Determining $k$] Finding $k$ such that $b_k = \\dfrac{9}{2}$',
              'knowledge': '등비수열 $\\{b_n\\}$의 항들을 차례대로 적어 봅시다:<ul><li>$b_1 = 72$</li><li>$b_2 = -36$</li><li>$b_3 = '
                           '18$</li><li>$b_4 = -9$</li><li>$b_5 = (-9) \\times \\left(-\\dfrac{1}{2}\\right) = '
                           '\\dfrac{9}{2}$</li></ul>',
              'knowledge_en': 'Listing the terms of $b_n = 72(-1/2)^{n-1}$: $b_1 = 72, b_2 = -36, b_3 = 18, b_4 = -9, '
                              'b_5 = \\frac{9}{2}$.',
              'questions': [{'level_label': '항 번호 k 디딤돌 5',
                             'level_label_en': 'Finding Index k Step 5',
                             'stem': '$b_n = 72\\left(-\\dfrac{1}{2}\\right)^{n-1}$에서 $b_k = \\dfrac{9}{2}$을 만족시키는 자연수 '
                                     '$k$의 값은?',
                             'stem_en': 'Which natural number $k$ satisfies $b_k = \\dfrac{9}{2}$?',
                             'options': ['$3$', '$4$', '$5$', '$6$', '$7$'],
                             'answer': 3,
                             'exp': '$b_5 = 72 \\times \\dfrac{1}{16} = \\dfrac{9}{2}$이므로 $k = 5$입니다.',
                             'exp_en': '$k = 5$.'}]},
             {'title': '🌳 6단계 · [새로운 등비급수 분석] 수열 $\\left\\{\\dfrac{b_n}{5^n}\\right\\}$의 첫째항과 공비 구하기',
              'title_en': '🌳 Step 6 · [New Geometric Series] First term and ratio of '
                          '$\\left\\{\\dfrac{b_n}{5^n}\\right\\}$',
              'knowledge': '$k = 5$를 대입하면 우리가 구해야 할 급수는 $\\sum_{n=1}^{\\infty} \\dfrac{b_n}{5^n}$입니다!<ul><li>**첫째항 ($n '
                           '= 1$)**: $\\dfrac{b_1}{5^1} = \\dfrac{72}{5}$</li><li>**공비 ($R$)**: $b_n$의 공비 '
                           '$-\\dfrac{1}{2}$을 $5$로 나눈 값 $\\implies R = \\dfrac{-1/2}{5} = -\\dfrac{1}{10}$</li></ul>',
              'knowledge_en': 'For $\\sum_{n=1}^\\infty \\frac{b_n}{5^n}$, the first term ($n=1$) is $\\frac{b_1}{5} = '
                              '\\frac{72}{5}$, and the common ratio is $R = \\frac{-1/2}{5} = -\\frac{1}{10}$.',
              'questions': [{'level_label': '새 등비수열 공비 디딤돌 6',
                             'level_label_en': 'New Common Ratio Step 6',
                             'stem': '등비수열 $\\left\\{\\dfrac{b_n}{5^n}\\right\\}$의 첫째항이 $\\dfrac{72}{5}$일 때, 공비 $R = '
                                     '\\dfrac{r}{5} = \\dfrac{-1/2}{5}$의 값은?',
                             'stem_en': 'What is the common ratio $R = \\dfrac{-1/2}{5}$ of the sequence '
                                        '$\\left\\{\\dfrac{b_n}{5^n}\\right\\}$?',
                             'options': ['$-\\frac{1}{5}$',
                                         '$-\\frac{1}{10}$',
                                         '$\\frac{1}{10}$',
                                         '$-\\frac{2}{5}$',
                                         '$-\\frac{1}{20}$'],
                             'answer': 2,
                             'exp': '$-\\dfrac{1}{2} \\div 5 = -\\dfrac{1}{10}$입니다.',
                             'exp_en': '$R = -\\dfrac{1}{10}$.'}]},
             {'title': '💎 7단계 · [등비급수 합 계산] $\\dfrac{72/5}{1 - (-1/10)}$을 기약분수로 정리하기',
              'title_en': '💎 Step 7 · [Evaluating the Infinite Series] Simplifying $\\dfrac{72/5}{1 - (-1/10)}$',
              'knowledge': '무한등비급수의 합 공식 $\\dfrac{\\text{첫째항}}{1 - \\text{공비}}$에 대입하면:$$\\sum_{n=1}^{\\infty} '
                           '\\frac{b_n}{5^n} = \\frac{\\frac{72}{5}}{1 - \\left(-\\frac{1}{10}\\right)} = '
                           '\\frac{\\frac{72}{5}}{\\frac{11}{10}}$$분모와 분자에 $10$을 곱하면 기약분수 $\\dfrac{q}{p}$가 바로 나옵니다!',
              'knowledge_en': 'Multiplying numerator and denominator of $\\frac{72/5}{11/10}$ by $10$ gives '
                              '$\\frac{144}{11}$.',
              'questions': [{'level_label': '번분수 정리 디딤돌 7',
                             'level_label_en': 'Complex Fraction Step 7',
                             'stem': '$\\dfrac{72/5}{11/10}$의 분모와 분자에 $10$을 곱하여 정리한 기약분수 $\\dfrac{q}{p}$는?',
                             'stem_en': 'What is $\\dfrac{72/5}{11/10}$ in lowest terms $\\dfrac{q}{p}$?',
                             'options': ['$\\frac{72}{11}$',
                                         '$\\frac{144}{11}$',
                                         '$\\frac{72}{9}$',
                                         '$\\frac{144}{9}$',
                                         '$\\frac{120}{11}$'],
                             'answer': 2,
                             'exp': '$\\dfrac{72 \\times 2}{11} = \\dfrac{144}{11}$입니다.',
                             'exp_en': '$\\dfrac{144}{11}$.'}]},
             {'title': '🏆 8단계 · [최종 정답 완성] 서로소인 자연수 $p + q$ 구하기',
              'title_en': '🏆 Step 8 · [Final Synthesis] Computing $p + q$',
              'knowledge': '$\\dfrac{q}{p} = \\dfrac{144}{11}$에서 $p = 11, q = 144$이므로 두 수를 더하면 최종 정답 $155$가 완성됩니다.',
              'knowledge_en': 'With $p = 11$ and $q = 144$, $p + q = 155$.',
              'questions': [{'level_label': '최종 종합 디딤돌 8',
                             'level_label_en': 'Final Synthesis Step 8',
                             'stem': '$p = 11$, $q = 144$일 때, 최종 정답 $p + q$의 값은?',
                             'stem_en': 'Given $p = 11$ and $q = 144$, what is $p + q$?',
                             'options': ['$145$', '$150$', '$155$', '$160$', '$165$'],
                             'answer': 3,
                             'exp': '$11 + 144 = 155$입니다.',
                             'exp_en': '$11 + 144 = 155$.'}]}],
  'final': {'stem': '어떤 자연수 $k$에 대하여 첫째항과 공차가 모두 정수인 등차수열 $\\{a_n\\}$과 첫째항이 $72$이고 공비가 $r$ ($r \\neq 0$)인 등비수열 '
                    '$\\{b_n\\}$이 다음 조건을 만족시킨다.<br><br>(가) $a_k = b_3,\\quad a_{k+27} = b_4$<br>(나) '
                    '$\\sum_{n=k}^{\\infty} b_n = a_{k+15}$<br><br>$\\sum_{n=1}^{\\infty} \\dfrac{b_n}{k^n} = '
                    '\\dfrac{q}{p}$일 때, $p + q$의 값을 구하시오. (단, $p$와 $q$는 서로소인 자연수이다.) [4점]',
            'stem_en': 'For a natural number $k$, an arithmetic sequence $\\{a_n\\}$ with integer first term and '
                       'integer common difference, and a geometric sequence $\\{b_n\\}$ with first term $72$ and '
                       'common ratio $r \\neq 0$, satisfy:<br>(가) $a_k = b_3,\\quad a_{k+27} = b_4$<br>(나) '
                       '$\\sum_{n=k}^{\\infty} b_n = a_{k+15}$<br>If $\\sum_{n=1}^{\\infty} \\dfrac{b_n}{k^n} = '
                       '\\dfrac{q}{p}$ in lowest terms, find $p + q$. [4 points]',
            'options': ['$145$', '$150$', '$155$', '$160$', '$165$'],
            'answer': 3,
            'exp': '수렴 조건 $-1 < r < 1$과 정수 조건 $b_4-b_3=72r^2(r-1)=27d$에서 $r = -\\dfrac{1}{2}$, $d = -1$, $k = 5$입니다. '
                   '따라서 $\\sum_{n=1}^{\\infty} \\dfrac{b_n}{5^n} = \\dfrac{72/5}{1 - (-1/10)} = \\dfrac{144}{11}$이므로 '
                   '$p + q = 155$입니다.',
            'exp_en': 'From $-1 < r < 1$ and $b_4-b_3=72r^2(r-1)=27d$, we find $r = -\\dfrac{1}{2}$, $d = -1$, and $k '
                      '= 5$. Thus $\\sum_{n=1}^{\\infty} \\dfrac{b_n}{5^n} = \\dfrac{72/5}{1 + 1/10} = '
                      '\\dfrac{144}{11}$ and $p + q = 155$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 <b>등비급수의 수렴 조건과 합 공식</b>을 등차수열의 정수 조건과 결합하여 공비 $r$, 공차 $d$, 자연수 $k$를 추론하는 '
                        '문항입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 정수 조건으로부터 공비 $r = -\\frac{1}{2}$과 공차 $d = -1$ 도출</b><br>\n'
                        '  조건 (나)에서 등비급수가 수렴하므로 $-1 < r < 1$ ($r \\neq 0$)입니다.<br>\n'
                        '  조건 (가)에서 $a_k = b_3 = 72r^2$, $a_{k+27} = b_4 = 72r^3$은 모두 정수이고:<br>\n'
                        '  $$a_{k+27} - a_k = 27d \\implies 72r^2(r - 1) = 27d \\implies 8r^2(r - 1) = 3d$$\n'
                        '  이를 만족하는 유리수 공비는 $r = -\\frac{1}{2}$이며, 이때 $b_3 = 18$, $b_4 = -9$, $d = -1$입니다.<br><br>\n'
                        '  <b>2단계: 자연수 $k = 5$ 결정</b><br>\n'
                        '  $$a_{k+15} = a_k + 15d = 18 - 15 = 3$$\n'
                        '  $$\\sum_{n=k}^{\\infty} b_n = \\frac{b_k}{1 - (-1/2)} = \\frac{2}{3}b_k = 3 \\implies b_k = '
                        '\\frac{9}{2}$$\n'
                        '  $b_k = 72\\left(-\\frac{1}{2}\\right)^{k-1} = \\frac{9}{2}$에서 '
                        '$\\left(-\\frac{1}{2}\\right)^{k-1} = \\frac{1}{16}$이므로 $k = 5$입니다.<br><br>\n'
                        '  <b>3단계: 구하는 등비급수의 합 계산</b><br>\n'
                        '  $$\\sum_{n=1}^{\\infty} \\frac{b_n}{5^n} = \\frac{72/5}{1 - (-1/10)} = \\frac{72/5}{11/10} '
                        '= \\frac{144}{11}$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 $p = 11, q = 144$이므로 $p + q =$ <b>$155$</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem combines <b>integer arithmetic sequences and geometric sequences</b> with '
                           'the <b>sum of an infinite geometric series</b>.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Determine parameters</b><br>\n'
                           '  From $72r^2(r-1) = 27d$ with $-1 < r < 1$ and integer terms, we get $r = -\\frac{1}{2}$, '
                           '$b_3 = 18$, $b_4 = -9$, and $d = -1$.<br>\n'
                           '  Then $a_{k+15} = 3 = \\frac{b_k}{3/2} \\implies b_k = \\frac{9}{2} \\implies k = '
                           '5$.<br><br>\n'
                           '  <b>Step 2: Sum the infinite series</b><br>\n'
                           '  $$\\sum_{n=1}^{\\infty} \\frac{b_n}{5^n} = \\frac{72/5}{1 - (-1/10)} = '
                           '\\frac{144}{11}$$\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  Thus $p + q = 11 + 144 =$ <b>$155$</b>.\n'
                           '</p>'}},
 {'slug': 'c2610m30',
  'qNum': '미적 30',
  'subject': '미적분',
  'title': '[2026학년도 10월 고3 미적 30번] 합성함수의 치환적분과 절댓값 정적분(총변화량)',
  'title_en': '[2026 AY Oct Exam Grade 12 Calculus #30] Composite Substitution and Total Variation Integral',
  'summary_ko': '두 번째 치환적분에서 $b+1=\\dfrac{1}{a}$를 구하고 첫 번째 절댓값 정적분(총변화량)에서 $\\sin(2\\pi a)=\\dfrac{1}{2},\\ '
                'a=\\dfrac{5}{12}$를 도출하여 $f(2\\pi)=\\dfrac{19}{10}$ 구하기',
  'summary_en': 'Use substitution $u=g(x)$ on the second integral to find $b+1=\\dfrac{1}{a}$, and analyze the total '
                'variation of $g(f(x))=\\{1-\\sin(ax)\\}^2$ on $[0, 2\\pi]$ to find $a=\\dfrac{5}{12}$ and '
                '$f(2\\pi)=\\dfrac{19}{10}$ ($p+q=29$).',
  'tags': ['미적분', '적분법', '치환적분법', '절댓값정적분', '합성함수', '단답형', '30번'],
  'symbols': [{'sym': "$u = g(x) = (x - b)^2 \\implies du = g'(x)dx$",
               'desc': "두 번째 적분 $\\int_b^{b+1} f(g(x))g'(x)dx$를 $\\int_0^1 f(u)du$로 바꾸는 치환적분",
               'desc_en': 'Substitution $u = g(x)$ transforming the second integral into $\\int_0^1 f(u)du$.'},
              {'sym': '$H(x) = g(f(x)) = \\{1 - \\sin(ax)\\}^2$',
               'desc': "미분하면 $H'(x) = g'(f(x))f'(x)$가 되는 합성함수",
               'desc_en': "Composite function whose derivative is $g'(f(x))f'(x)$."},
              {'sym': "$\\int_0^{2\\pi} |H'(x)|dx = \\dfrac{5}{4}$",
               'desc': '구간 $[0, 2\\pi]$에서 합성함수 $H(x)$가 위아래로 움직인 총 변화량',
               'desc_en': 'Total vertical variation of $H(x) = g(f(x))$ over $[0, 2\\pi]$.'}],
  'levels': [{'title': '🔰 1단계 · [두 번째 적분 치환하기] $u = g(x) = (x - b)^2$일 때 적분 구간 $[b, b+1]$ 바꾸기',
              'title_en': '🔰 Step 1 · [Substituting $u = g(x)$] Changing limits $[b, b+1]$ for $u = (x - b)^2$',
              'knowledge': "두 번째 조건식 $\\int_b^{b+1} f(g(x))g'(x)dx = \\dfrac{\\cos a}{a}$에서 $u = g(x) = (x - b)^2$으로 "
                           '치환해 봅시다!<ul><li>$x = b$일 때: $u = g(b) = (b - b)^2 = 0$</li><li>$x = b + 1$일 때: $u = g(b + '
                           "1) = (b + 1 - b)^2 = 1^2 = 1$</li><li>$g'(x)dx = du$이므로 적분식은 아주 간단한 $\\int_0^1 f(u)du$가 "
                           '됩니다!</li></ul>',
              'knowledge_en': "In $\\int_b^{b+1} f(g(x))g'(x)dx$, let $u = g(x) = (x - b)^2$. At $x = b$, $u = 0$; at "
                              "$x = b + 1$, $u = 1$. Since $g'(x)dx = du$, the integral becomes $\\int_0^1 f(u)du$.",
              'questions': [{'level_label': '초등 치환 구간 디딤돌 1',
                             'level_label_en': 'Substitution Limits Step 1',
                             'stem': '초등학교 제곱 계산으로 $g(x) = (x - b)^2$에 아래끝 $x = b$와 위끝 $x = b + 1$을 대입했을 때, 새로운 적분 구간 '
                                     '$[g(b), g(b+1)]$은?',
                             'stem_en': 'Using elementary squaring on $g(x) = (x - b)^2$, what is the new interval '
                                        '$[g(b), g(b+1)]$?',
                             'options': ['$[0, 1]$', '$[0, b]$', '$[1, 2]$', '$[b, b+1]$', '$[-1, 1]$'],
                             'answer': 1,
                             'exp': '$g(b) = 0^2 = 0$, $g(b+1) = 1^2 = 1$이므로 적분 구간은 $[0, 1]$이 됩니다.',
                             'exp_en': '$[0, 1]$.'}]},
             {'title': '🌿 2단계 · [정적분 계산으로 관계식 도출] $\\int_0^1 \\{-\\sin(au) + b + 1\\}du = \\dfrac{\\cos a}{a}$에서 $b + '
                       '1$ 구하기',
              'title_en': '🌿 Step 2 · [Evaluating $\\int_0^1 f(u)du$] Deriving $b + 1 = \\dfrac{1}{a}$',
              'knowledge': '$f(u) = -\\sin(au) + b + 1$을 $0$부터 $1$까지 적분하면:$$\\left[\\frac{\\cos(au)}{a} + (b + '
                           '1)u\\right]_0^1 = \\left(\\frac{\\cos a}{a} + b + 1\\right) - \\frac{1}{a} = \\frac{\\cos '
                           'a}{a} + b + 1 - \\frac{1}{a}$$이 값이 우변 $\\dfrac{\\cos a}{a}$와 같으므로 양변에서 $\\dfrac{\\cos '
                           'a}{a}$를 지우면 $b + 1 = \\dfrac{1}{a}$을 얻습니다!',
              'knowledge_en': 'Integrating $f(u) = -\\sin(au) + b + 1$ on $[0, 1]$ gives $\\frac{\\cos a - 1}{a} + b + '
                              '1 = \\frac{\\cos a}{a}$, which simplifies to $b + 1 = \\frac{1}{a}$.',
              'questions': [{'level_label': '$b+1$과 $a$의 관계 디딤돌 2',
                             'level_label_en': 'Relating $b+1$ and $a$ Step 2',
                             'stem': '$\\dfrac{\\cos a}{a} + b + 1 - \\dfrac{1}{a} = \\dfrac{\\cos a}{a}$의 양변에서 '
                                     '$\\dfrac{\\cos a}{a}$를 소거하여 정리한 $b + 1$의 식은?',
                             'stem_en': 'Canceling $\\dfrac{\\cos a}{a}$ from both sides gives what expression for $b '
                                        '+ 1$?',
                             'options': ['$a$', '$2a$', '$\\frac{1}{a}$', '$\\frac{2}{a}$', '$-\\frac{1}{a}$'],
                             'answer': 3,
                             'exp': '$b + 1 - \\dfrac{1}{a} = 0 \\implies b + 1 = \\dfrac{1}{a}$입니다.',
                             'exp_en': '$b + 1 = \\dfrac{1}{a}$.'}]},
             {'title': '🌱 3단계 · [첫 번째 적분의 합성함수 해석] $H(x) = g(f(x)) = \\{1 - \\sin(ax)\\}^2$ 만들기',
              'title_en': '🌱 Step 3 · [Composite Function $H(x)$] Writing $H(x) = g(f(x)) = \\{1 - \\sin(ax)\\}^2$',
              'knowledge': "첫 번째 적분식 $\\int_0^{2\\pi} |g'(f(x))f'(x)|dx = \\dfrac{5}{4}$을 자세히 보세요!<ul><li>합성함수의 미분법에 "
                           "의해 $g'(f(x))f'(x)$는 바로 합성함수 $H(x) = g(f(x))$를 미분한 도함수 $H'(x)$입니다!</li><li>$g(x) = (x - "
                           'b)^2$에 $f(x) = -\\sin(ax) + b + 1$을 대입하면 $b$가 지워져서:$$H(x) = \\{f(x) - b\\}^2 = \\{1 - '
                           '\\sin(ax)\\}^2$$이 됩니다!</li></ul>',
              'knowledge_en': "By the Chain Rule, $g'(f(x))f'(x)$ is the derivative of $H(x) = g(f(x)) = \\{f(x) - "
                              'b\\}^2 = \\{1 - \\sin(ax)\\}^2$.',
              'questions': [{'level_label': '합성함수 시작값 $H(0)$ 디딤돌 3',
                             'level_label_en': 'Initial Value $H(0)$ Step 3',
                             'stem': '합성함수 $H(x) = \\{1 - \\sin(ax)\\}^2$에 출발점 $x = 0$을 대입한 함숫값 $H(0)$과, $\\sin(ax) = '
                                     '1$일 때의 최솟값은 각각 얼마인가요?',
                             'stem_en': 'For $H(x) = \\{1 - \\sin(ax)\\}^2$, what is the starting value $H(0)$ and the '
                                        'minimum value when $\\sin(ax) = 1$?',
                             'options': ['$H(0) = 1$, 최솟값 $= 0$',
                                         '$H(0) = 0$, 최솟값 $= 0$',
                                         '$H(0) = 1$, 최솟값 $= 1$',
                                         '$H(0) = 2$, 최솟값 $= 0$',
                                         '$H(0) = 4$, 최솟값 $= 1$'],
                             'answer': 1,
                             'exp': '$x = 0$일 때 $\\sin 0 = 0$이므로 $H(0) = 1^2 = 1$이고, $\\sin(ax) = 1$일 때 $H(x) = (1 - '
                                    '1)^2 = 0$(최솟값)입니다.',
                             'exp_en': '$H(0) = 1$ and minimum $= 0$.'}]},
             {'title': '🌱 4단계 · [총 이동 거리(절댓값 적분) 계산] $1 + \\{1 - \\sin(2\\pi a)\\}^2 = \\dfrac{5}{4}$ 풀기',
              'title_en': '🌱 Step 4 · [Total Variation Distance] Solving $1 + \\{1 - \\sin(2\\pi a)\\}^2 = '
                          '\\dfrac{5}{4}$',
              'knowledge': "$\\int_0^{2\\pi} |H'(x)|dx = \\dfrac{5}{4}$는 $x = 0$부터 $x = 2\\pi$까지 **$H(x)$가 움직인 총 이동 "
                           '거리**가 $\\dfrac{5}{4}$라는 뜻입니다!<ul><li>$H(x)$는 $H(0) = 1$에서 출발하여 $ax = \\dfrac{\\pi}{2}$일 때 '
                           '최솟값 $0$까지 내려갑니다 ($\\implies$ 내려간 거리 $= 1 - 0 = 1$).</li><li>총 이동 거리가 $\\dfrac{5}{4} = 1 + '
                           '\\dfrac{1}{4}$이 되려면, 최솟값 $0$을 찍은 뒤 $x = 2\\pi$에서의 값 $H(2\\pi) = \\{1 - \\sin(2\\pi '
                           'a)\\}^2$이 정확히 $\\dfrac{1}{4}$만큼만 다시 올라가야 합니다!</li></ul>',
              'knowledge_en': 'Since $H(x)$ starts at $H(0) = 1$ and drops to $0$ at $ax = \\frac{\\pi}{2}$ (distance '
                              '$1$), a total travel distance of $\\frac{5}{4}$ means it must rise from $0$ to '
                              '$H(2\\pi) = \\{1 - \\sin(2\\pi a)\\}^2 = \\frac{5}{4} - 1 = \\frac{1}{4}$.',
              'questions': [{'level_label': '삼각방정식 값 디딤돌 4',
                             'level_label_en': 'Trigonometric Value Step 4',
                             'stem': '$\\{1 - \\sin(2\\pi a)\\}^2 = \\dfrac{1}{4}$이고 $1 - \\sin(2\\pi a) \\ge 0$이므로 $1 '
                                     '- \\sin(2\\pi a) = \\dfrac{1}{2}$입니다. 이때 $\\sin(2\\pi a)$의 값은?',
                             'stem_en': 'From $\\{1 - \\sin(2\\pi a)\\}^2 = \\dfrac{1}{4}$ with $1 - \\sin(2\\pi a) '
                                        '\\ge 0$, what is $\\sin(2\\pi a)$?',
                             'options': ['$\\frac{1}{4}$',
                                         '$\\frac{1}{2}$',
                                         '$\\frac{\\sqrt{2}}{2}$',
                                         '$\\frac{\\sqrt{3}}{2}$',
                                         '$1$'],
                             'answer': 2,
                             'exp': '$1 - \\sin(2\\pi a) = \\dfrac{1}{2} \\implies \\sin(2\\pi a) = \\dfrac{1}{2}$입니다.',
                             'exp_en': '$\\sin(2\\pi a) = \\dfrac{1}{2}$.'}]},
             {'title': '🌳 5단계 · [각 $2\\pi a$와 상수 $a$ 결정] $\\dfrac{\\pi}{2} < 2\\pi a < \\dfrac{3\\pi}{2}$에서 $a = '
                       '\\dfrac{5}{12}$ 구하기',
              'title_en': '🌳 Step 5 · [Determining $a$] Finding $2\\pi a = \\dfrac{5\\pi}{6}$ and $a = \\dfrac{5}{12}$',
              'knowledge': '$H(x)$가 $ax = \\dfrac{\\pi}{2}$에서 최솟값 $0$을 찍고 난 뒤 단조증가하는 구간($\\dfrac{\\pi}{2} < ax < '
                           '\\dfrac{3\\pi}{2}$) 안에 끝점 $2\\pi a$가 있어야 합니다!<ul><li>$\\dfrac{\\pi}{2} < 2\\pi a < '
                           '\\dfrac{3\\pi}{2}$에서 $\\sin(2\\pi a) = \\dfrac{1}{2}$을 만족시키는 각은 제2사분면의 각 **$2\\pi a = '
                           '\\dfrac{5\\pi}{6}$**입니다!</li></ul>',
              'knowledge_en': 'Since $2\\pi a$ must lie after the minimum at $\\frac{\\pi}{2}$ and before '
                              '$\\frac{3\\pi}{2}$, $\\sin(2\\pi a) = \\frac{1}{2}$ gives $2\\pi a = \\frac{5\\pi}{6}$.',
              'questions': [{'level_label': '상수 a 구하기 디딤돌 5',
                             'level_label_en': 'Finding Constant a Step 5',
                             'stem': '$2\\pi a = \\dfrac{5\\pi}{6}$의 양변을 $2\\pi$로 나누어 구한 상수 $a$의 값은?',
                             'stem_en': 'Dividing $2\\pi a = \\dfrac{5\\pi}{6}$ by $2\\pi$, what is the constant $a$?',
                             'options': ['$\\frac{1}{6}$',
                                         '$\\frac{1}{4}$',
                                         '$\\frac{5}{12}$',
                                         '$\\frac{7}{12}$',
                                         '$\\frac{5}{6}$'],
                             'answer': 3,
                             'exp': '$a = \\dfrac{5\\pi}{6 \\times 2\\pi} = \\dfrac{5}{12}$입니다.',
                             'exp_en': '$a = \\dfrac{5}{12}$.'}]},
             {'title': '🌳 6단계 · [$b + 1$ 값 확정] $a = \\dfrac{5}{12}$일 때 $b + 1 = \\dfrac{1}{a}$ 구하기',
              'title_en': '🌳 Step 6 · [Evaluating $b + 1$] Computing $b + 1 = \\dfrac{1}{a}$ for $a = \\dfrac{5}{12}$',
              'knowledge': '2단계에서 $b + 1 = \\dfrac{1}{a}$을 구했으므로, 5단계의 $a = \\dfrac{5}{12}$의 역수를 취하면 $b + 1$의 값이 바로 '
                           '나옵니다!',
              'knowledge_en': 'Taking the reciprocal of $a = \\frac{5}{12}$ gives $b + 1 = \\frac{1}{a} = '
                              '\\frac{12}{5}$.',
              'questions': [{'level_label': '역수 계산 디딤돌 6',
                             'level_label_en': 'Reciprocal Step 6',
                             'stem': '$a = \\dfrac{5}{12}$일 때, $b + 1 = \\dfrac{1}{a}$의 값은?',
                             'stem_en': 'When $a = \\dfrac{5}{12}$, what is $b + 1 = \\dfrac{1}{a}$?',
                             'options': ['$\\frac{5}{12}$',
                                         '$\\frac{7}{5}$',
                                         '$\\frac{12}{5}$',
                                         '$\\frac{17}{5}$',
                                         '$\\frac{12}{7}$'],
                             'answer': 3,
                             'exp': '$b + 1 = \\dfrac{12}{5}$입니다.',
                             'exp_en': '$b + 1 = \\dfrac{12}{5}$.'}]},
             {'title': '💎 7단계 · [$f(2\\pi)$ 함숫값 계산] $f(2\\pi) = -\\sin(2\\pi a) + (b + 1)$ 통분하기',
              'title_en': '💎 Step 7 · [Evaluating $f(2\\pi)$] Computing $f(2\\pi) = -\\sin(2\\pi a) + (b + 1)$',
              'knowledge': '$f(x) = -\\sin(ax) + b + 1$에 $x = 2\\pi$를 대입하면:$$f(2\\pi) = -\\sin(2\\pi a) + (b + 1) = '
                           '-\\frac{1}{2} + \\frac{12}{5}$$',
              'knowledge_en': 'Substitute $\\sin(2\\pi a) = \\frac{1}{2}$ and $b + 1 = \\frac{12}{5}$ into $f(2\\pi) = '
                              '-\\sin(2\\pi a) + b + 1$.',
              'questions': [{'level_label': '분수 통분 디딤돌 7',
                             'level_label_en': 'Fraction Addition Step 7',
                             'stem': '$f(2\\pi) = -\\dfrac{1}{2} + \\dfrac{12}{5}$를 분모 $10$으로 통분하여 계산한 기약분수 '
                                     '$\\dfrac{q}{p}$는?',
                             'stem_en': 'What is $-\\dfrac{1}{2} + \\dfrac{12}{5}$ in lowest terms $\\dfrac{q}{p}$?',
                             'options': ['$\\frac{17}{10}$',
                                         '$\\frac{19}{10}$',
                                         '$\\frac{21}{10}$',
                                         '$\\frac{23}{10}$',
                                         '$\\frac{29}{10}$'],
                             'answer': 2,
                             'exp': '$\\dfrac{-5 + 24}{10} = \\dfrac{19}{10}$입니다.',
                             'exp_en': '$\\dfrac{19}{10}$.'}]},
             {'title': '🏆 8단계 · [최종 정답 완성] 서로소인 자연수 $p + q$ 구하기',
              'title_en': '🏆 Step 8 · [Final Synthesis] Computing $p + q$',
              'knowledge': '$\\dfrac{q}{p} = \\dfrac{19}{10}$에서 $p = 10, q = 19$이므로 $p + q = 29$입니다.',
              'knowledge_en': 'With $p = 10$ and $q = 19$, $p + q = 29$.',
              'questions': [{'level_label': '최종 종합 디딤돌 8',
                             'level_label_en': 'Final Synthesis Step 8',
                             'stem': '$p = 10$, $q = 19$일 때, 최종 정답 $p + q$의 값은?',
                             'stem_en': 'Given $p = 10$ and $q = 19$, what is $p + q$?',
                             'options': ['$25$', '$27$', '$29$', '$31$', '$33$'],
                             'answer': 3,
                             'exp': '$10 + 19 = 29$입니다.',
                             'exp_en': '$10 + 19 = 29$.'}]}],
  'final': {'stem': '두 상수 $a$ ($a > 0$), $b$에 대하여 두 함수 $f(x) = -\\sin(ax) + b + 1$, $g(x) = (x - '
                    "b)^2$이<br>$$\\int_0^{2\\pi} |g'(f(x))f'(x)|dx = \\dfrac{5}{4},\\qquad \\int_b^{b+1} "
                    "f(g(x))g'(x)dx = \\dfrac{\\cos a}{a}$$<br>를 만족시킨다. $f(2\\pi) = \\dfrac{q}{p}$일 때, $p + q$의 값을 "
                    '구하시오. (단, $p$와 $q$는 서로소인 자연수이다.) [4점]',
            'stem_en': 'For constants $a > 0$ and $b$, the functions $f(x) = -\\sin(ax) + b + 1$ and $g(x) = (x - '
                       "b)^2$ satisfy $\\int_0^{2\\pi} |g'(f(x))f'(x)|dx = \\dfrac{5}{4}$ and $\\int_b^{b+1} "
                       "f(g(x))g'(x)dx = \\dfrac{\\cos a}{a}$. If $f(2\\pi) = \\dfrac{q}{p}$ in lowest terms, find $p "
                       '+ q$. [4 points]',
            'options': ['$25$', '$27$', '$29$', '$31$', '$33$'],
            'answer': 3,
            'exp': '두 번째 조건에서 $u=g(x)$로 치환하면 $\\int_0^1 f(u)du = \\dfrac{\\cos a - 1}{a} + b + 1 = \\dfrac{\\cos a}{a} '
                   '\\implies b + 1 = \\dfrac{1}{a}$를 얻고, 첫 번째 절댓값 적분에서 $g(f(x)) = \\{1 - \\sin(ax)\\}^2$의 총변화량이 $1 + '
                   '\\{1 - \\sin(2\\pi a)\\}^2 = \\dfrac{5}{4} \\implies \\sin(2\\pi a) = \\dfrac{1}{2}$ ($2\\pi a = '
                   '\\dfrac{5\\pi}{6}$)이므로 $a = \\dfrac{5}{12}$입니다. 따라서 $f(2\\pi) = -\\dfrac{1}{2} + \\dfrac{12}{5} = '
                   '\\dfrac{19}{10}$이고 $p + q = 29$입니다.',
            'exp_en': 'Substituting $u=g(x)$ in the second integral yields $b + 1 = \\dfrac{1}{a}$, and the total '
                      'variation of $g(f(x)) = \\{1 - \\sin(ax)\\}^2$ gives $1 + \\{1 - \\sin(2\\pi a)\\}^2 = '
                      '\\dfrac{5}{4} \\implies 2\\pi a = \\dfrac{5\\pi}{6} \\implies a = \\dfrac{5}{12}$. Thus '
                      '$f(2\\pi) = -\\dfrac{1}{2} + \\dfrac{12}{5} = \\dfrac{19}{10}$ and $p + q = 29$.',
            'solution': '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                        '<p>본 문항은 미적분 최고난도(30번) 문항으로, <b>치환적분법</b>과 <b>절댓값이 포함된 합성함수의 정적분(총변화량)</b>을 결합하여 상수 $a, b$를 '
                        '결정하는 문제입니다.</p>\n'
                        '\n'
                        '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                        '<p>\n'
                        '  <b>1단계: 두 번째 정적분 조건 해석 ($u = g(x)$ 치환)</b><br>\n'
                        "  두 번째 적분에서 $u = g(x) = (x - b)^2$으로 치환하면 $g'(x)dx = du$이고 적분 구간은 $[0, 1]$이 됩니다:<br>\n"
                        '  $$\\int_0^1 \\{-\\sin(au) + b + 1\\}du = \\left[\\frac{\\cos(au)}{a} + (b+1)u\\right]_0^1 = '
                        '\\frac{\\cos a - 1}{a} + b + 1 = \\frac{\\cos a}{a} \\implies b + 1 = \\frac{1}{a}$$<br>\n'
                        '  <b>2단계: 첫 번째 절댓값 정적분 조건 해석</b><br>\n'
                        "  $H(x) = g(f(x)) = \\{1 - \\sin(ax)\\}^2$이라 하면 $H'(x) = g'(f(x))f'(x)$입니다.<br>\n"
                        "  따라서 첫 번째 조건 $\\int_0^{2\\pi} |H'(x)|dx = \\frac{5}{4}$는 구간 $[0, 2\\pi]$에서 $H(x)$의 총변화량이 "
                        '$\\frac{5}{4}$임을 뜻합니다.<br>\n'
                        '  $H(0) = 1$에서 출발하여 $ax = \\frac{\\pi}{2}$에서 최솟값 $0$을 찍고 다시 $H(2\\pi) = \\{1 - \\sin(2\\pi '
                        'a)\\}^2$으로 증가하므로 ($\\frac{\\pi}{2} < 2\\pi a < \\frac{3\\pi}{2}$):<br>\n'
                        '  $$(1 - 0) + \\{1 - \\sin(2\\pi a)\\}^2 = \\frac{5}{4} \\implies \\{1 - \\sin(2\\pi a)\\}^2 '
                        '= \\frac{1}{4} \\implies \\sin(2\\pi a) = \\frac{1}{2}$$\n'
                        '  $\\frac{\\pi}{2} < 2\\pi a < \\frac{3\\pi}{2}$이므로 $2\\pi a = \\frac{5\\pi}{6} \\implies a = '
                        '\\frac{5}{12}$입니다.<br><br>\n'
                        '  <b>3단계: $f(2\\pi)$의 값 도출</b><br>\n'
                        '  $$f(2\\pi) = -\\sin\\left(\\frac{5\\pi}{6}\\right) + \\frac{1}{a} = -\\frac{1}{2} + '
                        '\\frac{12}{5} = \\frac{19}{10}$$\n'
                        '</p>\n'
                        '\n'
                        '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                        '<p>\n'
                        '  따라서 $p = 10, q = 19$이므로 $p + q =$ <b>$29$</b>입니다.\n'
                        '</p>',
            'solution_en': '<h4>📋 [Problem Analysis & Core Concepts]</h4>\n'
                           '<p>This problem combines <b>$u$-substitution</b> with the <b>total variation of a '
                           'composite function $H(x) = g(f(x))$</b>.</p>\n'
                           '\n'
                           '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                           '<p>\n'
                           '  <b>Step 1: Second integral via $u = g(x)$</b><br>\n'
                           '  $$\\int_0^1 f(u)du = \\frac{\\cos a - 1}{a} + b + 1 = \\frac{\\cos a}{a} \\implies b + 1 '
                           '= \\frac{1}{a}$$<br>\n'
                           '  <b>Step 2: First integral via total variation of $H(x) = \\{1 - \\sin(ax)\\}^2$</b><br>\n'
                           '  $$(1 - 0) + \\{1 - \\sin(2\\pi a)\\}^2 = \\frac{5}{4} \\implies \\sin(2\\pi a) = '
                           '\\frac{1}{2} \\implies 2\\pi a = \\frac{5\\pi}{6} \\implies a = \\frac{5}{12}$$\n'
                           '  Thus $f(2\\pi) = -\\frac{1}{2} + \\frac{12}{5} = \\frac{19}{10}$ and $p + q = 29$.\n'
                           '</p>\n'
                           '\n'
                           '<h4>✨ [Final Answer & Practical Tips]</h4>\n'
                           '<p>\n'
                           '  Therefore, $p + q = 10 + 19 =$ <b>$29$</b>.\n'
                           '</p>'}}]
