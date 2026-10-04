# solutions_c30_part1.py: Problems c30901 ~ c30910
SOLUTIONS_PART1 = {
    'c30901': {
        'ko': r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>거듭제곱근의 성질과 유리수 지수의 계산 법칙</b>을 평가합니다. 서로 다른 거듭제곱근 기호($\sqrt[n]{a}$)로 표현된 식을 공통 밑인 소수 $2$의 유리수 지수 꼴 $2^{\frac{m}{n}}$으로 변환하여 나눗셈을 지수의 뺄셈으로 간결하게 정리하는 능력이 핵심입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 분자를 밑이 2인 유리수 지수 형태로 변형</b><br>
  $32 = 2^5$이므로 $n$제곱근의 정의 $\sqrt[n]{a^m} = a^{\frac{m}{n}}$을 적용합니다.<br>
  $$\sqrt[4]{32} = \sqrt[4]{2^5} = 2^{\frac{5}{4}}$$
  <br>
  <b>2단계: 분모를 밑이 2인 유리수 지수 형태로 변형</b><br>
  $4 = 2^2$이므로 거듭제곱근의 기본 성질을 적용합니다.<br>
  $$\sqrt[8]{4} = \sqrt[8]{2^2} = 2^{\frac{2}{8}} = 2^{\frac{1}{4}}$$
  <br>
  <b>3단계: 밑이 같은 두 거듭제곱의 나눗셈 법칙 적용</b><br>
  지수법칙 $\frac{a^m}{a^n} = a^{m-n}$을 적용하여 분수를 계산합니다.<br>
  $$\frac{\sqrt[4]{32}}{\sqrt[8]{4}} = \frac{2^{\frac{5}{4}}}{2^{\frac{1}{4}}} = 2^{\frac{5}{4} - \frac{1}{4}} = 2^{\frac{4}{4}} = 2^1 = 2$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  계산된 최종 값은 $2$ 입니다.<br>
  따라서 올바른 정답은 <b>②번</b>입니다.<br>
  💡 <b>실전 팁</b>: 밑이 소인수분해 가능한 합성수인 거듭제곱근 문제는 가장 먼저 밑을 소수로 통일하고 분수 지수로 전환하면 어떤 복잡한 곱셈/나눗셈도 단순한 덧셈/뺄셈 산수로 귀결됩니다.
</p>""",
        'en': r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem assesses foundational proficiency in <b>radical properties and laws of rational exponents</b>. The key strategy is converting radicals into fractional exponents with a common prime base of $2$, transforming a division of radicals into an elementary subtraction of exponents.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Convert the numerator into base-2 exponential form</b><br>
  Factoring $32 = 2^5$ and applying $\sqrt[n]{a^m} = a^{\frac{m}{n}}$:<br>
  $$\sqrt[4]{32} = \sqrt[4]{2^5} = 2^{\frac{5}{4}}$$
  <br>
  <b>Step 2: Convert the denominator into base-2 exponential form</b><br>
  Factoring $4 = 2^2$ and simplifying the rational exponent:<br>
  $$\sqrt[8]{4} = \sqrt[8]{2^2} = 2^{\frac{2}{8}} = 2^{\frac{1}{4}}$$
  <br>
  <b>Step 3: Apply the quotient rule of exponents</b><br>
  Using the exponent quotient property $\frac{a^m}{a^n} = a^{m-n}$:<br>
  $$\frac{\sqrt[4]{32}}{\sqrt[8]{4}} = \frac{2^{\frac{5}{4}}}{2^{\frac{1}{4}}} = 2^{\frac{5}{4} - \frac{1}{4}} = 2^1 = 2$$
</p>

<h4>✨ [Conclusion & Key Takeaways]</h4>
<p>
  The final simplified value is $2$.<br>
  Therefore, the correct choice is <b>Option ②</b>.<br>
  💡 <b>Strategy Tip</b>: Always factor composite bases into prime factor powers immediately. Fractional exponents streamline radical arithmetic into straightforward linear calculations.
</p>"""
    },
    'c30902': {
        'ko': r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>미분계수의 정의식</b>을 식별하고, 다항함수의 도함수를 구하여 특정 점에서의 순간변화율을 신속 정확하게 계산할 수 있는지를 묻습니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 극한식의 기하학적·해석학적 의미 파악</b><br>
  주어진 극한 $\lim_{h \to 0}\frac{f(1+h)-f(1)}{h}$ 은 평균변화율의 극한으로서 $x=1$에서의 미분계수 $f'(1)$의 엄밀한 정의입니다.<br>
  $$\lim_{h \to 0}\frac{f(1+h)-f(1)}{h} = f'(1)$$
  <br>
  <b>2단계: 다항함수의 거듭제곱 도함수 구하기</b><br>
  $f(x) = x^3 + 3x^2 - 5$ 에 대하여 거듭제곱 미분법 $(x^n)' = n x^{n-1}$ 과 상수 미분법 $(c)' = 0$을 적용합니다.<br>
  $$f'(x) = 3x^2 + 6x$$
  <br>
  <b>3단계: $x=1$ 대입 및 미분계수 산출</b><br>
  도함수에 $x=1$을 대입합니다.<br>
  $$f'(1) = 3(1)^2 + 6(1) = 3 + 6 = 9$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  구하는 극한값은 $9$ 입니다.<br>
  따라서 올바른 정답은 <b>⑤번</b>입니다.<br>
  💡 <b>실전 팁</b>: $\lim_{h \to 0}\frac{f(a+h)-f(a)}{h} = f'(a)$ 형태는 미분계수의 교과서 표준 형식이므로 식 변형 없이 즉각 $f'(1)$로 직결하여 시간을 절약할 수 있습니다.
</p>""",
        'en': r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates direct understanding of the <b>definition of the derivative at a point</b> and basic polynomial differentiation rules.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Identify the derivative from the limit of the difference quotient</b><br>
  The given limit precisely matches the definition of the instantaneous rate of change at $x=1$:<br>
  $$\lim_{h \to 0}\frac{f(1+h)-f(1)}{h} = f'(1)$$
  <br>
  <b>Step 2: Differentiate the polynomial function $f(x)$</b><br>
  Given $f(x) = x^3 + 3x^2 - 5$, apply the power rule term by term:<br>
  $$f'(x) = \frac{d}{dx}(x^3 + 3x^2 - 5) = 3x^2 + 6x$$
  <br>
  <b>Step 3: Evaluate at $x = 1$</b><br>
  Substitute $x = 1$ into $f'(x)$:<br>
  $$f'(1) = 3(1)^2 + 6(1) = 3 + 6 = 9$$
</p>

<h4>✨ [Conclusion & Key Takeaways]</h4>
<p>
  The evaluated limit equals $9$.<br>
  Hence, the correct answer is <b>Option ⑤</b>.<br>
  💡 <b>Strategy Tip</b>: Instantly recognize standard limit forms for derivatives to bypass unnecessary difference quotient expansions.
</p>"""
    },
    'c30903': {
        'ko': r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>등비수열의 일반항 표현($a_n = a r^{n-1}$)</b>과 항들 사이의 곱·나눗셈 관계를 연립방정식으로 해결하여 특정 항의 값을 구하는 능력을 평가합니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 첫째항 $a$와 공비 $r$을 이용한 미지수 설정</b><br>
  등비수열 $\{a_n\}$의 첫째항을 $a$, 공비를 $r$이라 하면 일반항은 $a_n = a r^{n-1}$입니다.<br>
  주어진 조건들을 $a, r$로 표현합니다.<br>
  $$a_2 = ar, \quad a_3 = ar^2, \quad a_4 = ar^3$$
  조건 (1): $a_2 a_3 = (ar)(ar^2) = a^2 r^3 = 2 \quad \cdots\cdots \text{㉠}$<br>
  조건 (2): $a_4 = ar^3 = 4 \quad \cdots\cdots \text{㉡}$
  <br><br>
  <b>2단계: 변변 나눗셈을 통한 첫째항 $a$ 결정</b><br>
  식 ㉠을 식 ㉡으로 나누면 공비 거듭제곱 $r^3$이 소거됩니다.<br>
  $$\frac{a^2 r^3}{ar^3} = a = \frac{2}{4} = \frac{1}{2}$$
  <br>
  <b>3단계: 공비 $r$ 및 제6항 $a_6$ 도출</b><br>
  $a = \frac{1}{2}$을 ㉡에 대입합니다.<br>
  $$\frac{1}{2} r^3 = 4 \implies r^3 = 8 \implies r = 2 \quad (\because \text{실수 수열})$$
  구하고자 하는 제6항 $a_6$은 $a_4$에 $r^2$을 곱하여 쉽게 구할 수 있습니다.<br>
  $$a_6 = a_4 \times r^2 = 4 \times 2^2 = 4 \times 4 = 16$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  제6항의 값은 $16$ 입니다.<br>
  따라서 올바른 정답은 <b>④번</b>입니다.<br>
  💡 <b>실전 팁</b>: 등비수열 문제에서 $a_6$을 구할 때 $a r^5$를 직접 다시 계산하기보다 이미 주어진 $a_4$를 활용하여 $a_6 = a_4 \cdot r^2$으로 계산하면 연산 단계가 획기적으로 줄어듭니다.
</p>""",
        'en': r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This question tests understanding of the <b>general term of a geometric sequence ($a_n = a r^{n-1}$)</b> and the technique of dividing equations to isolate parameters cleanly.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Set up equations in terms of first term $a$ and common ratio $r$</b><br>
  Let $a_n = a r^{n-1}$. Translating the given conditions:<br>
  $$a_2 a_3 = (ar)(ar^2) = a^2 r^3 = 2 \quad \cdots\cdots (1)$$<br>
  $$a_4 = ar^3 = 4 \quad \cdots\cdots (2)$$
  <br>
  <b>Step 2: Eliminate $r^3$ by dividing equation (1) by equation (2)</b><br>
  Dividing equation (1) by equation (2):<br>
  $$\frac{a^2 r^3}{ar^3} = a = \frac{2}{4} = \frac{1}{2}$$
  <br>
  <b>Step 3: Solve for $r$ and compute $a_6$</b><br>
  Substituting $a = \frac{1}{2}$ back into equation (2):<br>
  $$\frac{1}{2} r^3 = 4 \implies r^3 = 8 \implies r = 2$$<br>
  To find $a_6$, advance from the known value $a_4$ by multiplying by $r^2$:<br>
  $$a_6 = a_4 \cdot r^2 = 4 \times 2^2 = 16$$
</p>

<h4>✨ [Conclusion & Key Takeaways]</h4>
<p>
  The value of the 6th term is $16$.<br>
  Therefore, the correct answer is <b>Option ④</b>.<br>
  💡 <b>Strategy Tip</b>: In geometric progressions, indexing jumps via $a_{n+k} = a_n \cdot r^k$ avoids re-evaluating powers from the first term.
</p>"""
    },
    'c30904': {
        'ko': r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 주어진 <b>함수의 불연속 그래프에서 좌극한($x \to a^-$)과 우극한($x \to b^+$)을 정확하게 판독</b>하여 연산하는 기초 해석학 역량을 평가합니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: $x=0$에서의 좌극한 $\lim_{x \to 0^-} f(x)$ 판독</b><br>
  $x$가 $0$보다 작은 음수 쪽($x < 0$)에서 $0$을 향해 한없이 가까워질 때, 그래프 상의 점 $(x, f(x))$의 $y$좌표는 아래쪽의 닫힌 점인 $-2$를 향해 수렴합니다.<br>
  $$\lim_{x \to 0^-} f(x) = -2$$
  <br>
  <b>2단계: $x=1$에서의 우극한 $\lim_{x \to 1^+} f(x)$ 판독</b><br>
  $x$가 $1$보다 큰 양수 쪽($x > 1$)에서 $1$을 향해 한없이 가까워질 때, 그래프 상의 $y$좌표는 직선을 타고 $1$을 향해 수렴합니다.<br>
  $$\lim_{x \to 1^+} f(x) = 1$$
  <br>
  <b>3단계: 두 극한값의 합 계산</b><br>
  구하고자 하는 두 값의 합을 구합니다.<br>
  $$\lim_{x \to 0^-} f(x) + \lim_{x \to 1^+} f(x) = (-2) + 1 = -1$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  구하는 합은 $-1$ 입니다.<br>
  따라서 올바른 정답은 <b>②번</b>입니다.<br>
  💡 <b>실전 팁</b>: 불연속점에서는 함숫값 $f(a)$와 극한값 $\lim_{x \to a^\pm} f(x)$가 다를 수 있습니다. 색칠된 원(함숫값)과 열린 원(극한 도달값)의 방향을 좌/우 부호($-$, $+$)에 맞춰 정확히 추적해야 합니다.
</p>""",
        'en': r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem checks the ability to read <b>one-sided limits (left-hand limit $x \to a^-$ and right-hand limit $x \to b^+$)</b> directly from a piecewise graphical representation.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Read the left-hand limit at $x = 0$</b><br>
  As $x$ approaches $0$ from the left ($x < 0$), the graph follows the lower branch toward $y = -2$:<br>
  $$\lim_{x \to 0^-} f(x) = -2$$
  <br>
  <b>Step 2: Read the right-hand limit at $x = 1$</b><br>
  As $x$ approaches $1$ from the right ($x > 1$), following the corresponding curve indicates the $y$-value approaches $1$:<br>
  $$\lim_{x \to 1^+} f(x) = 1$$
  <br>
  <b>Step 3: Compute the sum of the two one-sided limits</b><br>
  Adding the two obtained limits:<br>
  $$\lim_{x \to 0^-} f(x) + \lim_{x \to 1^+} f(x) = -2 + 1 = -1$$
</p>

<h4>✨ [Conclusion & Key Takeaways]</h4>
<p>
  The resulting sum is $-1$.<br>
  Therefore, the correct choice is <b>Option ②</b>.<br>
  💡 <b>Strategy Tip</b>: Distinguish strictly between one-sided limits and isolated points (function values) at discontinuities.
</p>"""
    },
    'c30905': {
        'ko': r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 두 다항식의 곱으로 정의된 함수의 <b>곱의 미분법(Product Rule)</b>을 적용하고, 미분계수를 정확히 대입하여 산출할 수 있는지를 평가합니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 곱의 미분법 공식 적용</b><br>
  $f(x) = u(x)v(x)$ 에 대하여 $\{u(x)v(x)\}' = u'(x)v(x) + u(x)v'(x)$ 입니다.<br>
  여기서 $u(x) = x+1$, $v(x) = x^2+x-5$ 이므로<br>
  $$u'(x) = 1, \quad v'(x) = 2x+1$$
  도함수 $f'(x)$는 다음과 같습니다.<br>
  $$f'(x) = 1 \cdot (x^2+x-5) + (x+1)(2x+1)$$
  <br>
  <b>2단계: $x=2$ 대입 및 각 인수의 값 계산</b><br>
  전개하기 전 각 인수에 직접 $x=2$를 대입하여 계산을 간소화합니다.<br>
  • $u(2) = 2+1 = 3$<br>
  • $u'(2) = 1$<br>
  • $v(2) = 2^2 + 2 - 5 = 4 + 2 - 5 = 1$<br>
  • $v'(2) = 2(2) + 1 = 5$
  <br>
  <b>3단계: 최종 미분계수 산출</b><br>
  $$f'(2) = u'(2)v(2) + u(2)v'(2) = 1 \cdot 1 + 3 \cdot 5 = 1 + 15 = 16$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  구하는 미분계수는 $16$ 입니다.<br>
  따라서 올바른 정답은 <b>②번</b>입니다.<br>
  💡 <b>실전 팁</b>: 곱의 미분법에서 식 전체를 전개한 후 미분하기보다, 곱의 미분 공식 형태 그대로 $x=2$를 대입하는 것이 계산 오류를 최소화하는 가장 빠르고 안전한 방법입니다.
</p>""",
        'en': r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem verifies the correct application of the <b>Product Rule of differentiation</b> on two polynomial factors and evaluating the derivative at a specified point.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: State and apply the product rule</b><br>
  For $f(x) = (x+1)(x^2+x-5)$, let $u(x) = x+1$ and $v(x) = x^2+x-5$.<br>
  Their respective derivatives are:<br>
  $$u'(x) = 1, \quad v'(x) = 2x+1$$<br>
  Applying $(uv)' = u'v + uv'$:<br>
  $$f'(x) = 1 \cdot (x^2+x-5) + (x+1)(2x+1)$$
  <br>
  <b>Step 2: Evaluate factor values at $x = 2$</b><br>
  Rather than expanding polynomials, evaluate each term at $x=2$ directly:<br>
  • $u(2) = 3$<br>
  • $u'(2) = 1$<br>
  • $v(2) = 2^2 + 2 - 5 = 1$<br>
  • $v'(2) = 2(2) + 1 = 5$
  <br>
  <b>Step 3: Compute the final derivative value</b><br>
  $$f'(2) = (1)(1) + (3)(5) = 1 + 15 = 16$$
</p>

<h4>✨ [Conclusion & Key Takeaways]</h4>
<p>
  The evaluated derivative $f'(2)$ equals $16$.<br>
  Thus, the correct answer is <b>Option ②</b>.<br>
  💡 <b>Strategy Tip</b>: Evaluating component factors before summing drastically reduces algebraic expanding errors under time constraints.
</p>"""
    },
    'c30906': {
        'ko': r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>삼각함수의 각 변환 공식</b>과 사분면에 따른 삼각함수 값의 부호 결정, 그리고 삼각함수의 기본 항등식 $\sin^2\theta + \cos^2\theta = 1$을 유기적으로 활용하는 문제입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 각 변환을 통한 $\cos\theta$ 값 결정</b><br>
  주어진 조건 $\cos(\pi+\theta) = \frac{2\sqrt{5}}{5}$ 에서 각 변환 공식 $\cos(\pi+\theta) = -\cos\theta$ 를 적용합니다.<br>
  $$-\cos\theta = \frac{2\sqrt{5}}{5} \implies \cos\theta = -\frac{2\sqrt{5}}{5}$$
  <br>
  <b>2단계: 사분면 조건 분석 및 $\sin\theta$ 계산</b><br>
  동경 $\theta$의 범위가 $\frac{\pi}{2} < \theta < \pi$ (제2사분면)이므로, $\sin\theta > 0$ 입니다.<br>
  기본 항등식 $\sin^2\theta + \cos^2\theta = 1$을 적용하면 다음과 같습니다.<br>
  $$\sin\theta = \sqrt{1 - \cos^2\theta} = \sqrt{1 - \left(-\frac{2\sqrt{5}}{5}\right)^2} = \sqrt{1 - \frac{20}{25}} = \sqrt{\frac{5}{25}} = \frac{\sqrt{5}}{5}$$
  <br>
  <b>3단계: $\sin\theta + \cos\theta$ 계산</b><br>
  구하고자 하는 두 삼각함수의 합을 계산합니다.<br>
  $$\sin\theta + \cos\theta = \frac{\sqrt{5}}{5} + \left(-\frac{2\sqrt{5}}{5}\right) = -\frac{\sqrt{5}}{5}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  구하는 합은 $-\frac{\sqrt{5}}{5}$ 입니다.<br>
  따라서 올바른 정답은 <b>②번</b>입니다.<br>
  💡 <b>실전 팁</b>: 삼각함수 각 변환 $\cos(\pi+\theta) = -\cos\theta$ 적용 시 부호 실수를 주의하고, 제2사분면에서는 $\sin$만 양수이고 $\cos, \tan$는 음수라는 '올-싸-탄-코(All-Sin-Tan-Cos)' 규칙을 항상 점검하십시오.
</p>""",
        'en': r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem tests the application of <b>trigonometric reduction formulas ($\cos(\pi+\theta) = -\cos\theta$)</b>, quadrant-based sign analysis, and the Pythagorean identity $\sin^2\theta + \cos^2\theta = 1$.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Simplify using trigonometric reduction</b><br>
  Given $\cos(\pi+\theta) = \frac{2\sqrt{5}}{5}$, recall that $\cos(\pi+\theta) = -\cos\theta$.<br>
  $$-\cos\theta = \frac{2\sqrt{5}}{5} \implies \cos\theta = -\frac{2\sqrt{5}}{5}$$
  <br>
  <b>Step 2: Determine $\sin\theta$ considering quadrant constraints</b><br>
  The angle $\theta$ lies in Quadrant II ($\frac{\pi}{2} < \theta < \pi$), where the sine function is strictly positive ($\sin\theta > 0$).<br>
  Using $\sin^2\theta + \cos^2\theta = 1$:<br>
  $$\sin\theta = +\sqrt{1 - \cos^2\theta} = \sqrt{1 - \frac{20}{25}} = \sqrt{\frac{5}{25}} = \frac{\sqrt{5}}{5}$$
  <br>
  <b>Step 3: Calculate the sum $\sin\theta + \cos\theta$</b><br>
  $$\sin\theta + \cos\theta = \frac{\sqrt{5}}{5} - \frac{2\sqrt{5}}{5} = -\frac{\sqrt{5}}{5}$$
</p>

<h4>✨ [Conclusion & Key Takeaways]</h4>
<p>
  The value of $\sin\theta + \cos\theta$ is $-\frac{\sqrt{5}}{5}$.<br>
  Hence, the correct answer is <b>Option ②</b>.<br>
  💡 <b>Strategy Tip</b>: Always verify the signs of trigonometric values against the quadrant of the terminal angle $\theta$.
</p>"""
    },
    'c30907': {
        'ko': r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>구간별로 다르게 정의된 함수의 연속성 조건</b>을 바탕으로, 경계점에서의 좌극한, 우극한, 함숫값이 일치함을 이용하여 미정계수 $a$에 관한 이차방정식을 세우고 모든 해의 곱을 구하는 문제입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 연속성 정의 및 경계점 조건 분석</b><br>
  함수 $f(x)$가 실수 전체의 집합에서 연속이 되기 위해서는 두 규칙이 나뉘는 경계점인 $x=4$에서 연속이어야 합니다.<br>
  즉, 다음 조건이 성립해야 합니다.<br>
  $$\lim_{x \to 4^-} f(x) = \lim_{x \to 4^+} f(x) = f(4)$$
  <br>
  <b>2단계: 좌극한과 우극한(함숫값) 계산</b><br>
  • $x < 4$ 일 때 $f(x) = (x-a)^2$ 이므로 좌극한은:<br>
  $$\lim_{x \to 4^-} f(x) = (4-a)^2 = a^2 - 8a + 16$$
  • $x \ge 4$ 일 때 $f(x) = 2x-4$ 이므로 우극한 및 함숫값은:<br>
  $$\lim_{x \to 4^+} f(x) = f(4) = 2(4) - 4 = 4$$
  <br>
  <b>3단계: 이차방정식 수립 및 $a$의 값의 곱 산출</b><br>
  연속 조건에 따라 좌극한과 우극한이 같아야 합니다.<br>
  $$a^2 - 8a + 16 = 4 \implies a^2 - 8a + 12 = 0$$
  인수분해하면 $(a-2)(a-6) = 0$ 이므로 $a = 2$ 또는 $a = 6$ 입니다.<br>
  근과 계수의 관계에 의해서도 두 근의 곱은 상수항인 $12$임을 바로 확인할 수 있습니다.<br>
  $$2 \times 6 = 12$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  모든 상수 $a$의 값의 곱은 $12$ 입니다.<br>
  따라서 올바른 정답은 <b>③번</b>입니다.<br>
  💡 <b>실전 팁</b>: 이차방정식 $a^2 - 8a + 12 = 0$의 두 실근의 곱을 물었으므로, 판별식 $D/4 = 16 - 12 = 4 > 0$으로 실근 존재를 확인한 후 근과 계수의 관계를 통해 즉시 $12$를 도출하면 연산이 매우 빠릅니다.
</p>""",
        'en': r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates conditions for <b>continuity of a piecewise-defined function</b> at the boundary point $x=4$, translating the continuity requirement into a quadratic equation in parameter $a$.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: State the continuity condition at $x = 4$</b><br>
  For $f(x)$ to be continuous everywhere on $\mathbb{R}$, the left-hand limit, right-hand limit, and function value must agree at $x=4$:<br>
  $$\lim_{x \to 4^-} f(x) = \lim_{x \to 4^+} f(x) = f(4)$$
  <br>
  <b>Step 2: Evaluate one-sided limits</b><br>
  • Left-hand limit ($x < 4$):<br>
  $$\lim_{x \to 4^-} (x-a)^2 = (4-a)^2 = a^2 - 8a + 16$$<br>
  • Right-hand limit and value ($x \ge 4$):<br>
  $$f(4) = 2(4) - 4 = 4$$
  <br>
  <b>Step 3: Solve the quadratic equation for $a$</b><br>
  Equating the two expressions:<br>
  $$a^2 - 8a + 16 = 4 \implies a^2 - 8a + 12 = 0$$<br>
  Factoring gives $(a-2)(a-6) = 0$, yielding $a = 2$ or $a = 6$.<br>
  By Vieta's formulas, the product of all roots is the constant term $12$:<br>
  $$2 \times 6 = 12$$
</p>

<h4>✨ [Conclusion & Key Takeaways]</h4>
<p>
  The product of all possible values of $a$ is $12$.<br>
  Therefore, the correct answer is <b>Option ③</b>.<br>
  💡 <b>Strategy Tip</b>: Vieta's formulas provide instantaneous product solutions once real roots are confirmed via the discriminant ($D > 0$).
</p>"""
    },
    'c30908': {
        'ko': r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>로그의 밑 변환 공식과 역수 관계</b>를 파악하고, 공통 부분을 치환하여 이차방정식을 해결하는 대수적 추론 능력을 평가합니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 로그의 성질을 통한 두 수의 곱 $k$ 결정</b><br>
  밑 변환 공식과 진수의 거듭제곱 성질에 의하여<br>
  $$\log_a 8 = \log_a (2^3) = 3 \log_a 2 = \frac{3}{\log_2 a}$$
  두 수 $\log_2 a$와 $\log_a 8$의 곱 $k$는 다음과 같이 상수로 결정됩니다.<br>
  $$k = (\log_2 a) \times (\log_a 8) = (\log_2 a) \times \frac{3}{\log_2 a} = 3$$
  <br>
  <b>2단계: 합 조건에 치환 적용 및 방정식 풀이</b><br>
  두 수의 합이 $4$이므로 식을 세웁니다.<br>
  $$\log_2 a + \frac{3}{\log_2 a} = 4$$
  $X = \log_2 a$ 라 두면, 문제의 조건 $a > 2$ 에서 $X > \log_2 2 = 1$ 입니다.<br>
  양변에 $X$를 곱하여 정리하면:<br>
  $$X + \frac{3}{X} = 4 \implies X^2 - 4X + 3 = 0 \implies (X-1)(X-3) = 0$$
  <br>
  <b>3단계: 조건에 맞는 $a$ 및 $a+k$ 계산</b><br>
  $X > 1$ 이므로 $X = 3$ 입니다.<br>
  $$\log_2 a = 3 \implies a = 2^3 = 8$$
  따라서 구하고자 하는 값 $a+k$는 다음과 같습니다.<br>
  $$a + k = 8 + 3 = 11$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  최종 구하는 값 $a+k$는 $11$ 입니다.<br>
  따라서 올바른 정답은 <b>①번</b>입니다.<br>
  💡 <b>실전 팁</b>: $\log_a b$와 $\log_b a$는 서로 역수 관계입니다. $\log_a 8 = 3\log_a 2 = \frac{3}{\log_2 a}$임을 간파하면 두 수의 곱 $k=3$이 즉시 나오고, 합이 4이므로 합과 곱을 이용한 $X^2 - 4X + 3 = 0$이 순식간에 도출됩니다.
</p>""",
        'en': r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates proficiency in the <b>change of base formula and reciprocal relationships in logarithms</b>, along with solving algebraic equations via substitution.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Simplify the product $k$ using logarithmic properties</b><br>
  Using $\log_a (2^3) = 3\log_a 2 = \frac{3}{\log_2 a}$:<br>
  $$k = (\log_2 a) \cdot (\log_a 8) = (\log_2 a) \cdot \frac{3}{\log_2 a} = 3$$
  <br>
  <b>Step 2: Solve the sum equation via substitution</b><br>
  The sum of the two numbers is given as $4$:<br>
  $$\log_2 a + \frac{3}{\log_2 a} = 4$$<br>
  Substitute $X = \log_2 a$. Since $a > 2$, we have $X > 1$.<br>
  $$X + \frac{3}{X} = 4 \implies X^2 - 4X + 3 = 0 \implies (X-1)(X-3) = 0$$
  <br>
  <b>Step 3: Determine $a$ and evaluate $a+k$</b><br>
  Given the constraint $X > 1$, we must have $X = 3$.<br>
  $$\log_2 a = 3 \implies a = 2^3 = 8$$<br>
  Thus, compute the required sum:<br>
  $$a + k = 8 + 3 = 11$$
</p>

<h4>✨ [Conclusion & Key Takeaways]</h4>
<p>
  The final value $a+k$ is $11$.<br>
  Hence, the correct answer is <b>Option ①</b>.<br>
  💡 <b>Strategy Tip</b>: Recognizing reciprocal bases ($\log_a b = \frac{1}{\log_b a}$) immediately converts the setup into a symmetric sum-and-product quadratic structure.
</p>"""
    },
    'c30909': {
        'ko': r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>정적분의 선형성(Linearity of Definite Integrals)</b>을 이용하여 여러 개의 적분 기호를 하나의 적분으로 통합하고, 다항함수의 정적분을 효율적으로 계산하는 능력을 평가합니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 정적분의 선형성을 이용한 피적분함수 통합</b><br>
  적분 구간이 $[0, 1]$로 모두 같으므로 정적분의 성질 $\int_a^b \{c f(x) + g(x)\}dx = c\int_a^b f(x)dx + \int_a^b g(x)dx$을 적용하여 식을 하나로 묶습니다.<br>
  $$5\int_0^1 f(x)dx - \int_0^1 (5x+f(x))dx = \int_0^1 \{5f(x) - (5x+f(x))\} dx = \int_0^1 \{4f(x) - 5x\} dx$$
  <br>
  <b>2단계: $f(x) = x^2+x$ 대입 및 피적분함수 정리</b><br>
  주어진 $f(x) = x^2+x$를 피적분함수에 대입합니다.<br>
  $$4f(x) - 5x = 4(x^2+x) - 5x = 4x^2 + 4x - 5x = 4x^2 - x$$
  <br>
  <b>3단계: 다항함수의 정적분 계산</b><br>
  부정적분을 구하고 위끝과 아래끝을 대입합니다.<br>
  $$\int_0^1 (4x^2 - x)dx = \left[ \frac{4}{3}x^3 - \frac{1}{2}x^2 \right]_0^1 = \left(\frac{4}{3} - \frac{1}{2}\right) - 0 = \frac{8 - 3}{6} = \frac{5}{6}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  계산된 정적분 값은 $\frac{5}{6}$ 입니다.<br>
  따라서 올바른 정답은 <b>⑤번</b>입니다.<br>
  💡 <b>실전 팁</b>: 각각의 적분을 따로 계산한 뒤 빼려고 하면 계산 횟수가 늘어나 실수가 발생하기 쉽습니다. 구간이 동일한 적분은 먼저 하나의 기호 $\int$로 통합하여 동류항을 정리한 후 마지막에 한 번만 적분하십시오.
</p>""",
        'en': r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem verifies mastery of the <b>linearity property of definite integrals</b>, combining multiple integrals with identical limits into a single consolidated polynomial integral.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Consolidate the integral expression</b><br>
  Because both terms share the identical interval of integration $[0, 1]$, combine them using linearity:<br>
  $$5\int_0^1 f(x)dx - \int_0^1 (5x+f(x))dx = \int_0^1 [5f(x) - (5x+f(x))] dx = \int_0^1 [4f(x) - 5x] dx$$
  <br>
  <b>Step 2: Substitute $f(x) = x^2+x$ into the integrand</b><br>
  $$4f(x) - 5x = 4(x^2+x) - 5x = 4x^2 - x$$
  <br>
  <b>Step 3: Evaluate the definite integral</b><br>
  Find the antiderivative and apply the Fundamental Theorem of Calculus:<br>
  $$\int_0^1 (4x^2 - x)dx = \left[ \frac{4}{3}x^3 - \frac{1}{2}x^2 \right]_0^1 = \frac{4}{3} - \frac{1}{2} = \frac{5}{6}$$
</p>

<h4>✨ [Conclusion & Key Takeaways]</h4>
<p>
  The computed value is $\frac{5}{6}$.<br>
  Thus, the correct choice is <b>Option ⑤</b>.<br>
  💡 <b>Strategy Tip</b>: Combining integrands over identical integration bounds saves substantial algebra and prevents arithmetic mistakes.
</p>"""
    },
    'c30910': {
        'ko': r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 삼각형의 <b>사인법칙(Law of Sines)</b>과 외접원의 반지름, 그리고 직각삼각형에서의 피타고라스 정리를 종합적으로 연계하여 변의 길이를 추론하는 기하학적 종합 문제입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 외접원의 반지름 $R$ 및 변의 비율 설정</b><br>
  삼각형 $ABC$의 외접원의 넓이가 $50\pi$이므로 외접원 반지름 $R$은 다음과 같습니다.<br>
  $$\pi R^2 = 50\pi \implies R = \sqrt{50} = 5\sqrt{2}$$
  조건 $\overline{AB} : \overline{AC} = \sqrt{2} : 1$ 에서 $\overline{AC} = x$ ($x>0$)라 두면 $\overline{AB} = \sqrt{2}x$ 입니다.
  <br><br>
  <b>2단계: 직각삼각형 $AHC$를 이용한 $\sin C$ 표현 및 사인법칙 적용</b><br>
  점 $A$에서 선분 $BC$에 내린 수선의 발을 $H$라 하면, 직각삼각형 $AHC$에서 $\overline{AH} = 2$ 입니다.<br>
  따라서 각 $C$에 대한 사인값은 다음과 같습니다.<br>
  $$\sin C = \frac{\overline{AH}}{\overline{AC}} = \frac{2}{x}$$
  삼각형 $ABC$에서 사인법칙을 대변 $\overline{AB}$와 각 $C$에 적용하면:<br>
  $$\frac{\overline{AB}}{\sin C} = 2R \implies \overline{AB} = 2R \sin C$$
  대입하면:<br>
  $$\sqrt{2}x = 2(5\sqrt{2}) \cdot \left(\frac{2}{x}\right) = \frac{20\sqrt{2}}{x}$$
  양변을 $\sqrt{2}$로 나누고 $x$를 곱하면:<br>
  $$x^2 = 20 \implies x = \sqrt{20} = 2\sqrt{5}$$
  <br>
  <b>3단계: $\overline{AB}$ 산출 및 직각삼각형 $ABH$에서 피타고라스 정리 적용</b><br>
  $\overline{AB} = \sqrt{2}x = \sqrt{2}(2\sqrt{5}) = 2\sqrt{10}$ 입니다.<br>
  직각삼각형 $ABH$에서 $\angle AHB = 90^\circ$ 이므로 피타고라스 정리를 적용합니다.<br>
  $$\overline{BH} = \sqrt{\overline{AB}^2 - \overline{AH}^2} = \sqrt{(2\sqrt{10})^2 - 2^2} = \sqrt{40 - 4} = \sqrt{36} = 6$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  선분 $BH$의 길이는 $6$ 입니다.<br>
  따라서 올바른 정답은 <b>①번</b>입니다.<br>
  💡 <b>실전 팁</b>: 수선의 발 $H$가 주어지면 높이($\overline{AH}$)를 공통으로 갖는 두 직각삼각형 $AHC$와 $ABH$를 분리하여 보고, 외접원 조건이 나오는 즉시 $2R$과 사인법칙을 결합하는 것이 표준적인 접근법입니다.
</p>""",
        'en': r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem integrates the <b>Law of Sines</b>, circumradius properties, and the Pythagorean theorem on right triangles derived from an altitude dropped to the base.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Determine the circumradius $R$ and parameterize side lengths</b><br>
  Given the circumcircle area $50\pi$, the circumradius is:<br>
  $$\pi R^2 = 50\pi \implies R = 5\sqrt{2}$$<br>
  Given the ratio $\overline{AB} : \overline{AC} = \sqrt{2} : 1$, let $\overline{AC} = x$. Then $\overline{AB} = \sqrt{2}x$.
  <br><br>
  <b>Step 2: Express $\sin C$ from right triangle $AHC$ and apply the Law of Sines</b><br>
  In right triangle $AHC$ with altitude $\overline{AH} = 2$:<br>
  $$\sin C = \frac{\overline{AH}}{\overline{AC}} = \frac{2}{x}$$<br>
  By the Law of Sines on $\triangle ABC$:<br>
  $$\frac{\overline{AB}}{\sin C} = 2R \implies \overline{AB} = 2R \sin C$$<br>
  Substituting our parameterized expressions:<br>
  $$\sqrt{2}x = 2(5\sqrt{2})\left(\frac{2}{x}\right) = \frac{20\sqrt{2}}{x}$$<br>
  Multiplying both sides by $x$ and dividing by $\sqrt{2}$:<br>
  $$x^2 = 20 \implies x = 2\sqrt{5}$$
  <br>
  <b>Step 3: Compute $\overline{AB}$ and determine $\overline{BH}$ via Pythagorean theorem</b><br>
  The length of hypotenuse $\overline{AB}$ is:<br>
  $$\overline{AB} = \sqrt{2}(2\sqrt{5}) = 2\sqrt{10}$$<br>
  In right triangle $ABH$:<br>
  $$\overline{BH} = \sqrt{\overline{AB}^2 - \overline{AH}^2} = \sqrt{40 - 4} = \sqrt{36} = 6$$
</p>

<h4>✨ [Conclusion & Key Takeaways]</h4>
<p>
  The length of segment $BH$ is $6$.<br>
  Hence, the correct option is <b>Option ①</b>.<br>
  💡 <b>Strategy Tip</b>: An altitude naturally divides a general triangle into two right triangles, letting you bridge trigonometric ratios ($\sin C = \frac{h}{b}$) with the circumradius Law of Sines ($\frac{c}{\sin C} = 2R$).
</p>"""
    }
}
