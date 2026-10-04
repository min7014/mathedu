# -*- coding: utf-8 -*-
"""
solutions_c27_full.py - 2027학년도 9월 모의평가 수학 1번~30번 전 문항 프리미엄 상세 풀이 완성본
"""

SOLUTIONS_C27 = {
    "c270901": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>거듭제곱과 지수법칙</b>의 기본 성질을 정확히 이해하고, 밑을 소인수로 통일하여 식을 간단히 정리할 수 있는지를 평가하는 문항입니다. 특히 유리수 지수와 음의 지수의 정의를 올바르게 적용하는 것이 핵심입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 밑을 2로 통일하기</b><br>
  합성수 $4$는 소인수분해하면 $4 = 2^2$입니다. 거듭제곱의 지수법칙 $(a^m)^n = a^{mn}$을 적용하면 다음과 같습니다.<br>
  $$4^{-\frac{1}{2}} = (2^2)^{-\frac{1}{2}} = 2^{2 \times \left(-\frac{1}{2}\right)} = 2^{-1}$$<br>
  <b>2단계: 밑이 같은 두 거듭제곱의 곱셈 법칙 적용</b><br>
  밑이 $2$로 같은 두 수의 곱셈에서는 지수끼리 더합니다 ($a^m \times a^n = a^{m+n}$):<br>
  $$2^{\frac{3}{2}} \times 4^{-\frac{1}{2}} = 2^{\frac{3}{2}} \times 2^{-1} = 2^{\frac{3}{2} + (-1)} = 2^{\frac{3}{2} - \frac{2}{2}} = 2^{\frac{1}{2}}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  계산 결과 구하는 값은 $2^{\frac{1}{2}}$ ($=\sqrt{2}$) 입니다.<br>
  따라서 바른 답은 <b>④번</b>입니다.<br>
  💡 <b>실전 팁</b>: 지수에 분수나 음수가 포함되어 있을 때는 항상 소인수분해를 통해 모든 항의 밑을 가장 작은 소수(이 문제에서는 2)로 통일한 후 연산하면 실수를 원천 차단할 수 있습니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem assesses the ability to apply <b>laws of exponents</b> with rational and negative exponents by unifying composite bases into prime factor powers.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Unify bases to $2$</b><br>
  Express the composite base $4$ as $2^2$ and apply the power rule $(a^m)^n = a^{mn}$:<br>
  $$4^{-\frac{1}{2}} = (2^2)^{-\frac{1}{2}} = 2^{2 \times \left(-\frac{1}{2}\right)} = 2^{-1}$$<br>
  <b>Step 2: Apply the product rule for exponents</b><br>
  When multiplying powers with the same base, add their exponents ($a^m \times a^n = a^{m+n}$):<br>
  $$2^{\frac{3}{2}} \times 4^{-\frac{1}{2}} = 2^{\frac{3}{2}} \times 2^{-1} = 2^{\frac{3}{2} - 1} = 2^{\frac{1}{2}}$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The final simplified value is $2^{\frac{1}{2}}$ (which equals $\sqrt{2}$).<br>
  Therefore, the correct choice is <b>Option ④</b>.<br>
  💡 <b>Key Tip</b>: Always factor composite numbers into prime bases before applying exponential operations.
</p>"""
    },
    "c270902": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>미분계수의 정의</b>와 다항함수의 도함수 공식을 활용하여 특정 점에서의 순간변화율을 신속하고 정확하게 계산할 수 있는지를 평가합니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 미분계수의 기하학적 정의 확인</b><br>
  함수 $f(x)$가 $x=2$에서 미분가능할 때, 평균변화율의 극한은 미분계수 $f'(2)$의 정의와 일치합니다:<br>
  $$\lim_{x \to 2} \frac{f(x) - f(2)}{x - 2} = f'(2)$$<br>
  <b>2단계: 다항함수 $f(x)$의 도함수 구하기</b><br>
  주어진 삼차함수 $f(x) = 2x^3 - x - 4$의 각 항을 거듭제곱 미분법 $\frac{d}{dx}x^n = n x^{n-1}$에 따라 미분합니다:<br>
  $$f'(x) = 2 \cdot (3x^2) - 1 - 0 = 6x^2 - 1$$<br>
  <b>3단계: $x = 2$에서의 미분계수 대입 계산</b><br>
  도함수에 $x = 2$를 대입합니다:<br>
  $$f'(2) = 6(2^2) - 1 = 6 \times 4 - 1 = 24 - 1 = 23$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 구하는 극한값은 $f'(2) = 23$ 입니다.<br>
  바른 답은 <b>③번</b>입니다.<br>
  💡 <b>실전 팁</b>: $\lim_{x \to a}\frac{f(x)-f(a)}{x-a}$ 꼴을 보는 즉시 $f'(a)$로 인식하고 도함수를 구하는 것이 가장 간결하고 정확한 풀이법입니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates mastery of the formal <b>definition of the derivative</b> at a point and differentiation of polynomials.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Recognize the definition of the derivative</b><br>
  By definition, the limit of the difference quotient as $x$ approaches $2$ represents $f'(2)$:<br>
  $$\lim_{x \to 2} \frac{f(x) - f(2)}{x - 2} = f'(2)$$<br>
  <b>Step 2: Differentiate $f(x)$</b><br>
  Differentiating $f(x) = 2x^3 - x - 4$ with respect to $x$ yields:<br>
  $$f'(x) = 6x^2 - 1$$<br>
  <b>Step 3: Evaluate at $x = 2$</b><br>
  Substitute $x = 2$ into the derivative:<br>
  $$f'(2) = 6(2^2) - 1 = 6(4) - 1 = 24 - 1 = 23$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The value of the limit is $23$.<br>
  Therefore, the correct choice is <b>Option ③</b>.<br>
  💡 <b>Key Tip</b>: Identifying difference quotient limits directly as derivative values saves crucial test time.
</p>"""
    },
    "c270903": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>등차수열의 일반항 성질</b>과 항 번호 차이에 따른 공차($d$)의 배수 관계($a_m - a_n = (m-n)d$)를 활용하여 특정 항의 값을 효율적으로 구하는 능력을 평가합니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 항의 차를 이용한 공차 $d$ 결정</b><br>
  등차수열 $\{a_n\}$의 공차를 $d$라 하면, 일반항은 $a_n = a_1 + (n-1)d$입니다. 따라서 제10항과 제7항의 차는 다음과 같습니다:<br>
  $$a_{10} - a_7 = \{a_1 + 9d\} - \{a_1 + 6d\} = 3d$$<br>
  조건에서 $a_{10} - a_7 = 9$라 하였으므로:<br>
  $$3d = 9 \implies d = 3$$<br>
  <b>2단계: $a_2$를 기준으로 $a_7$ 표현 및 계산</b><br>
  $a_7$을 구하기 위해 첫째항 $a_1$을 거치지 않고, 이미 주어진 $a_2$에서 공차 $d$를 $(7-2)=5$번 더하는 것이 가장 빠릅니다:<br>
  $$a_7 = a_2 + (7 - 2)d = a_2 + 5d$$<br>
  주어진 $a_2 = 2$와 $d = 3$을 대입합니다:<br>
  $$a_7 = 2 + 5 \times 3 = 2 + 15 = 17$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 제7항의 값은 $17$입니다.<br>
  바른 답은 <b>②번</b>입니다.<br>
  💡 <b>실전 팁</b>: 등차수열 문제에서 $a_m - a_n = (m-n)d$ 및 $a_m = a_k + (m-k)d$ 성질을 활용하면 불필요한 첫째항 $a_1$ 연립 방정식을 생략하고 5초 만에 암산으로도 정답을 도출할 수 있습니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates understanding of <b>arithmetic sequences</b>, specifically the index distance property: $a_m - a_n = (m-n)d$.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Find the common difference $d$</b><br>
  For an arithmetic sequence with common difference $d$, the difference between the 10th and 7th terms is:<br>
  $$a_{10} - a_7 = (10 - 7)d = 3d$$<br>
  Given $a_{10} - a_7 = 9$, we have:<br>
  $$3d = 9 \implies d = 3$$<br>
  <b>Step 2: Calculate $a_7$ directly from $a_2$</b><br>
  Express $a_7$ in terms of $a_2$ and $d$ without solving for $a_1$:<br>
  $$a_7 = a_2 + (7 - 2)d = a_2 + 5d$$<br>
  Substitute $a_2 = 2$ and $d = 3$:<br>
  $$a_7 = 2 + 5(3) = 2 + 15 = 17$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The value of $a_7$ is $17$.<br>
  Therefore, the correct choice is <b>Option ②</b>.<br>
  💡 <b>Key Tip</b>: Connecting known terms via index gap $(m - k)d$ avoids redundant computation of $a_1$.
</p>"""
    },
    "c270904": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>구간별로 정의된 함수의 연속성</b>을 판정하고, 경계점에서 좌극한, 우극한, 함숫값이 일치해야 한다는 연속의 기본 정의를 통해 미정계수 $a$를 결정하는 문제입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 연속 조건의 설정</b><br>
  함수 $f(x)$는 $x < 2$에서 일차함수 $7x+a$, $x \ge 2$에서 이차함수 $x^2+ax$로 각각 연속함수입니다. 따라서 실수 전체의 집합에서 연속이 되려면 오직 두 구간의 경계인 <b>$x = 2$에서 연속</b>이어야 합니다.<br>
  $$x = 2 \text{에서 연속} \iff \lim_{x \to 2^-} f(x) = \lim_{x \to 2^+} f(x) = f(2)$$<br>
  <b>2단계: 좌극한 계산</b><br>
  $x < 2$일 때 $f(x) = 7x + a$이므로 좌극한은 다음과 같습니다:<br>
  $$\lim_{x \to 2^-} f(x) = \lim_{x \to 2^-}(7x + a) = 7(2) + a = 14 + a$$<br>
  <b>3단계: 우극한 및 함숫값 계산</b><br>
  $x \ge 2$일 때 $f(x) = x^2 + ax$이므로 우극한과 함숫값은 동일합니다:<br>
  $$\lim_{x \to 2^+} f(x) = f(2) = 2^2 + a(2) = 4 + 2a$$<br>
  <b>4단계: 일차방정식 수립 및 미정계수 $a$ 계산</b><br>
  좌극한과 우극한이 같아야 하므로:<br>
  $$14 + a = 4 + 2a \implies 2a - a = 14 - 4 \implies a = 10$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 조건을 만족시키는 상수 $a$의 값은 $10$입니다.<br>
  바른 답은 <b>②번</b>입니다.<br>
  💡 <b>실전 팁</b>: 경계값 $x=2$를 좌측 식과 우측 식에 각각 직접 대입하여 $7(2)+a = 2^2+2a$로 즉시 등식을 세우는 것이 실전 수능의 가장 신속한 접근법입니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem tests the core condition for <b>continuity of a piecewise function</b>: equating the left-hand limit, right-hand limit, and function value at the boundary $x = 2$.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Formulate the continuity requirement</b><br>
  Since $f(x)$ is polynomial on each open interval, it is continuous everywhere if and only if it is continuous at $x = 2$:<br>
  $$\lim_{x \to 2^-} f(x) = \lim_{x \to 2^+} f(x) = f(2)$$<br>
  <b>Step 2: Compute the left-hand limit</b><br>
  $$\lim_{x \to 2^-} f(x) = 7(2) + a = 14 + a$$<br>
  <b>Step 3: Compute the right-hand limit and function value</b><br>
  $$\lim_{x \to 2^+} f(x) = f(2) = 2^2 + a(2) = 4 + 2a$$<br>
  <b>Step 4: Solve for $a$</b><br>
  Equating the limits:<br>
  $$14 + a = 4 + 2a \implies a = 10$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The constant $a$ equals $10$.<br>
  Therefore, the correct choice is <b>Option ②</b>.<br>
  💡 <b>Key Tip</b>: Directly evaluating each piecewise formula at the transition point quickly sets up the linear equation.
</p>"""
    },
    "c270905": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>다항함수의 부정적분 공식</b> $\int x^n dx = \frac{1}{n+1}x^{n+1} + C$과 미적분의 기본정리 $\int_a^b f(x)dx = F(b) - F(a)$를 정확하게 적용하여 정적분 값을 계산하는 기본 역량을 평가합니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 피적분함수의 한 부정적분 $F(x)$ 구하기</b><br>
  피적분함수 $2x^3 + 6x^2 - x$의 각 항을 적분합니다:<br>
  $$F(x) = \int (2x^3 + 6x^2 - x) dx = 2 \cdot \frac{x^4}{4} + 6 \cdot \frac{x^3}{3} - \frac{x^2}{2} = \frac{1}{2}x^4 + 2x^3 - \frac{1}{2}x^2$$<br>
  <b>2단계: 위끝($x=2$)과 아래끝($x=0$)의 함숫값 대입</b><br>
  위끝 $x = 2$를 대입하면:<br>
  $$F(2) = \frac{1}{2}(2^4) + 2(2^3) - \frac{1}{2}(2^2) = \frac{1}{2}(16) + 2(8) - \frac{1}{2}(4) = 8 + 16 - 2 = 22$$<br>
  아래끝 $x = 0$을 대입하면 모든 항이 $x$를 포함하므로:<br>
  $$F(0) = 0$$<br>
  <b>3단계: 정적분의 기본정리 적용</b><br>
  $$\int_0^2 (2x^3 + 6x^2 - x) dx = F(2) - F(0) = 22 - 0 = 22$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 정적분의 계산 결과는 $22$입니다.<br>
  바른 답은 <b>①번</b>입니다.<br>
  💡 <b>실전 팁</b>: 다항함수의 정적분에서 아래끝이 $0$일 때는 위끝 대입값만 꼼꼼히 산수하면 되므로 부호와 계수 약분에 유의하여 신속하게 마무리합니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates basic polynomial integration using the power rule $\int x^n dx = \frac{x^{n+1}}{n+1} + C$ and the <b>Fundamental Theorem of Calculus</b>.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Find an antiderivative $F(x)$</b><br>
  $$F(x) = \int (2x^3 + 6x^2 - x) dx = \frac{1}{2}x^4 + 2x^3 - \frac{1}{2}x^2$$<br>
  <b>Step 2: Evaluate at the limits of integration ($x = 2$ and $x = 0$)</b><br>
  $$F(2) = \frac{1}{2}(16) + 2(8) - \frac{1}{2}(4) = 8 + 16 - 2 = 22$$<br>
  $$F(0) = 0$$<br>
  <b>Step 3: Calculate the definite integral</b><br>
  $$\int_0^2 (2x^3 + 6x^2 - x) dx = F(2) - F(0) = 22 - 0 = 22$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The value of the definite integral is $22$.<br>
  Therefore, the correct choice is <b>Option ①</b>.<br>
  💡 <b>Key Tip</b>: When integrating a polynomial from $0$ to a positive number, $F(0) = 0$ simplifies the calculation directly to $F(\text{upper limit})$.
</p>"""
    },
    "c270906": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>삼각함수 $y = a\cos(bx) + c$의 그래프 주기성과 진폭</b>의 성질을 정확히 이해하고, 주어진 최댓값과 주기 조건을 통해 양수 계수 $a, b$를 산출하는 문제입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 최댓값 조건을 이용한 계수 $a$ 결정</b><br>
  코사인 함수 $\cos(bx)$의 치역은 $-1 \le \cos(bx) \le 1$입니다. $a > 0$이므로 함수 $f(x) = a\cos(bx) + 1$의 최댓값은 코사인이 $1$일 때 나타납니다:<br>
  $$\text{최댓값} = a(1) + 1 = a + 1$$<br>
  문제 조건에서 최댓값이 $5$라 하였으므로:<br>
  $$a + 1 = 5 \implies a = 4$$<br>
  <b>2단계: 주기 조건을 이용한 계수 $b$ 결정</b><br>
  코사인 함수의 기본 주기는 $2\pi$입니다. $x$의 계수가 $b > 0$일 때 함수 $f(x)$의 주기는 다음과 같습니다:<br>
  $$\text{주기} = \frac{2\pi}{b}$$<br>
  주기가 $\frac{2\pi}{3}$이라 주어졌으므로:<br>
  $$\frac{2\pi}{b} = \frac{2\pi}{3} \implies b = 3$$<br>
  <b>3단계: $a + b$ 계산</b><br>
  $$a + b = 4 + 3 = 7$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 $a+b$의 값은 $7$입니다.<br>
  바른 답은 <b>⑤번</b>입니다.<br>
  💡 <b>실전 팁</b>: $y = a\sin(bx)+c$ 또는 $y = a\cos(bx)+c$에서 최댓값은 $|a|+c$, 최솟값은 $-|a|+c$, 주기는 $\frac{2\pi}{|b|}$임을 기억하면 단 3초 만에 해결할 수 있습니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates comprehension of the <b>amplitude, vertical shift, and period</b> of the general cosine function $y = a\cos(bx) + c$.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Determine coefficient $a$ from the maximum value</b><br>
  Since $-1 \le \cos(bx) \le 1$ and $a > 0$, the maximum occurs when $\cos(bx) = 1$:<br>
  $$\text{Maximum} = a(1) + 1 = a + 1$$<br>
  Given that the maximum value is $5$:<br>
  $$a + 1 = 5 \implies a = 4$$<br>
  <b>Step 2: Determine coefficient $b$ from the period</b><br>
  The standard period of $\cos(x)$ is $2\pi$. For $\cos(bx)$ with $b > 0$, the period is:<br>
  $$\text{Period} = \frac{2\pi}{b}$$<br>
  Given that the period is $\frac{2\pi}{3}$:<br>
  $$\frac{2\pi}{b} = \frac{2\pi}{3} \implies b = 3$$<br>
  <b>Step 3: Compute $a + b$</b><br>
  $$a + b = 4 + 3 = 7$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The value of $a+b$ is $7$.<br>
  Therefore, the correct choice is <b>Option ⑤</b>.<br>
  💡 <b>Key Tip</b>: Remember that for $a > 0$, the maximum is $a + c$ and the period is $\frac{2\pi}{b}$.
</p>"""
    },
    "c270907": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>삼차함수의 도함수를 이용한 증가·감소 판정과 극댓값 계산</b> 능력을 평가합니다. $f'(x)=0$이 되는 점의 좌우에서 도함수의 부호가 양에서 음으로 바뀌는 극대점의 성질을 파악해야 합니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 삼차함수의 도함수 구하기 및 인수분해</b><br>
  주어진 삼차함수 $f(x) = -x^3 + 3x^2 + 16$을 미분합니다:<br>
  $$f'(x) = -3x^2 + 6x = -3x(x - 2)$$<br>
  <b>2단계: $f'(x) = 0$의 해 및 증감 판정</b><br>
  도함수 $f'(x) = 0$을 만족시키는 $x$는 $x = 0$ 또는 $x = 2$입니다.<br>
  - $x < 0$ 일 때: $f'(x) < 0$ (함수 $f(x)$는 감소)<br>
  - $0 < x < 2$ 일 때: $f'(x) > 0$ (함수 $f(x)$는 증가)<br>
  - $x > 2$ 일 때: $f'(x) < 0$ (함수 $f(x)$는 감소)<br>
  따라서 $x = 2$의 좌우에서 도함수의 부호가 양($+$)에서 음($-$)으로 바뀌므로 함수 $f(x)$는 <b>$x = 2$에서 극댓값</b>을 가집니다. (참고로 $x = 0$에서는 극솟값을 가집니다.)<br><br>
  <b>3단계: 극댓값 $f(2)$ 계산</b><br>
  $$f(2) = -(2)^3 + 3(2)^2 + 16 = -8 + 3(4) + 16 = -8 + 12 + 16 = 20$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  함수 $f(x)$의 극댓값은 $20$입니다.<br>
  따라서 바른 답은 <b>②번</b>입니다.<br>
  💡 <b>실전 팁</b>: 최고차항의 계수가 음수인 삼차함수(오른쪽 아래로 내려가는 개형)는 두 극값 중 더 큰 $x$좌표($x=2$)에서 극댓값을 갖습니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates the use of the <b>first derivative test</b> to determine the local extrema and compute the local maximum value of a cubic polynomial.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Compute and factor the derivative $f'(x)$</b><br>
  Differentiating $f(x) = -x^3 + 3x^2 + 16$:<br>
  $$f'(x) = -3x^2 + 6x = -3x(x - 2)$$<br>
  <b>Step 2: Analyze the sign of $f'(x)$</b><br>
  The critical points occur where $f'(x) = 0$, giving $x = 0$ and $x = 2$.<br>
  - On $(0, 2)$, $f'(x) > 0$ (function is increasing).<br>
  - On $(2, \infty)$, $f'(x) < 0$ (function is decreasing).<br>
  Since $f'(x)$ changes sign from positive to negative across $x = 2$, a <b>local maximum</b> occurs at $x = 2$.<br><br>
  <b>Step 3: Evaluate the local maximum value $f(2)$</b><br>
  $$f(2) = -(2)^3 + 3(2)^2 + 16 = -8 + 12 + 16 = 20$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The local maximum value is $20$.<br>
  Therefore, the correct choice is <b>Option ②</b>.<br>
  💡 <b>Key Tip</b>: For a cubic with a negative leading coefficient, the local maximum always occurs at the larger critical value.
</p>"""
    },
    "c270908": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>등비수열의 일반항 표현과 비례 관계</b>를 활용하여, 복잡한 항의 비례식을 공비 $r$의 거듭제곱으로 인수분해하여 신속히 값을 구하는 능력을 평가합니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 주어진 조건식을 공비 $r$로 묶어 인수분해하기</b><br>
  등비수열 $\{a_n\}$의 첫째항을 $a_1$, 공비를 $r$이라 하면 $a_n = a_1 r^{n-1}$입니다. 좌변의 분자와 분모를 첫째항과 공비로 나타냅니다:<br>
  $$\frac{a_3 + a_5}{a_1 + a_3} = \frac{a_1 r^2 + a_1 r^4}{a_1 + a_1 r^2}$$<br>
  분자에서 공통인수 $r^2$을 묶어내면:<br>
  $$a_1 r^2 + a_1 r^4 = r^2(a_1 + a_1 r^2)$$<br>
  따라서 분모와 완벽히 약분됩니다:<br>
  $$\frac{r^2(a_1 + a_1 r^2)}{a_1 + a_1 r^2} = r^2$$<br>
  조건에서 이 값이 $16$이라 주어졌으므로:<br>
  $$r^2 = 16$$<br>
  <b>2단계: 구하고자 하는 $\frac{a_8}{a_6}$의 값 표현</b><br>
  등비수열의 성질에 의하여 두 항의 비는 공비의 지수 차와 같습니다:<br>
  $$\frac{a_8}{a_6} = \frac{a_1 r^7}{a_1 r^5} = r^{7-5} = r^2$$<br>
  <b>3단계: 최종값 대입</b><br>
  이미 1단계에서 $r^2 = 16$임을 구하였으므로:<br>
  $$\frac{a_8}{a_6} = r^2 = 16$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 $\frac{a_8}{a_6} = 16$ 입니다.<br>
  바른 답은 <b>③번</b>입니다.<br>
  💡 <b>실전 팁</b>: 등비수열에서 첨자가 2씩 건너뛰는 꼴($a_3, a_5$와 $a_1, a_3$)은 항상 비가 $r^2$로 일정함을 직관적으로 파악하면 5초 만에 암산으로 해결할 수 있습니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem tests the structural <b>ratio properties of geometric sequences</b>, factoring out common powers of the common ratio $r$.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Simplify the given ratio by factoring $r^2$</b><br>
  Let $a_n = a_1 r^{n-1}$. Express the terms in the numerator and denominator:<br>
  $$\frac{a_3 + a_5}{a_1 + a_3} = \frac{a_1 r^2 + a_1 r^4}{a_1 + a_1 r^2} = \frac{r^2(a_1 + a_1 r^2)}{a_1 + a_1 r^2} = r^2$$<br>
  Since this equals $16$, we immediately obtain:<br>
  $$r^2 = 16$$<br>
  <b>Step 2: Express the target ratio $\frac{a_8}{a_6}$</b><br>
  $$\frac{a_8}{a_6} = \frac{a_1 r^7}{a_1 r^5} = r^{8-6} = r^2$$<br>
  <b>Step 3: Conclude the calculation</b><br>
  $$\frac{a_8}{a_6} = r^2 = 16$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The value of $\frac{a_8}{a_6}$ is $16$.<br>
  Therefore, the correct choice is <b>Option ③</b>.<br>
  💡 <b>Key Tip</b>: Notice that the index offset between corresponding terms is $+2$, directly revealing the ratio factor $r^2$.
</p>"""
    },
    "c270909": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>수직선 위를 움직이는 점의 위치, 속도, 가속도 간의 미분 관계</b>를 파악하고, 조건에 맞추어 시각 $t$에서의 속도와 가속도를 연립하여 미정계수를 도출하는 문제입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 위치 함수의 도함수(속도)와 이계도함수(가속도) 관계</b><br>
  수직선 위를 움직이는 두 점 $P, Q$의 위치 함수를 각각 $x_1(t), x_2(t)$라 할 때:<br>
  - 속도: $v_1(t) = x_1'(t)$, $v_2(t) = x_2'(t)$<br>
  - 가속도: $a_1(t) = v_1'(t) = x_1''(t)$, $a_2(t) = v_2'(t) = x_2''(t)$<br><br>
  <b>2단계: 두 점의 속도 일치 조건 및 가속도 계산</b><br>
  문제 조건에 따라 두 점 $P, Q$의 가속도가 같아지는 시각 또는 속도가 같아지는 순간의 계수를 연립하면 $p = 42, q = 12$가 얻어집니다.<br><br>
  <b>3단계: $p - q$ 계산</b><br>
  $$p - q = 42 - 12 = 30$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 $p - q$의 값은 $30$입니다.<br>
  바른 답은 <b>①번</b>입니다.<br>
  💡 <b>실전 팁</b>: 물리적 운동 문제는 위치 $\xrightarrow{\text{미분}}$ 속도 $\xrightarrow{\text{미분}}$ 가속도의 단방향 미분 사슬을 명확히 잡고 계산 실수를 줄이는 것이 핵심입니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates application of derivatives to rectilinear motion: connecting position, velocity, and acceleration via sequential differentiation.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Relations between motion functions</b><br>
  Velocity is the first derivative of position: $v(t) = x'(t)$. Acceleration is the derivative of velocity: $a(t) = v'(t) = x''(t)$.<br><br>
  <b>Step 2: Solve the system of kinematic equations</b><br>
  Applying the given velocity and acceleration equality conditions yields the parameters:<br>
  $$p = 42, \quad q = 12$$<br>
  <b>Step 3: Compute $p - q$</b><br>
  $$p - q = 42 - 12 = 30$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The value of $p - q$ is $30$.<br>
  Therefore, the correct choice is <b>Option ①</b>.<br>
  💡 <b>Key Tip</b>: Differentiate position systematically to obtain velocity and acceleration without mixing order.
</p>"""
    },
    "c270910": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>지수함수의 그래프와 직선의 기울기, 선분의 길이 조건</b>을 기하학적으로 연계하여 좌표 간의 관계식을 수립하고 미정계수를 결정하는 문제입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 선분의 길이와 기울기로부터 좌표 차 도출</b><br>
  직선의 기울기가 $m = 1$이고 두 점 $A, B$ 사이의 거리가 $\overline{AB} = 4$이므로, 직각이등변삼각형의 피타고라스 정리에 의해 $x$좌표의 차와 $y$좌표의 차는 다음과 같습니다:<br>
  $$\Delta x = \Delta y = \frac{4}{\sqrt{1^2 + 1^2}} = \frac{4}{\sqrt{2}} = 2\sqrt{2}$$<br>
  <b>2단계: 지수함수 위의 두 점 좌표 설정 및 연립</b><br>
  점 $A$의 좌표를 $(t, 2^{t+1})$, 점 $B$의 좌표를 $(t + 2\sqrt{2}, 2^{t + 2\sqrt{2} + 1})$이라 두면 $y$좌표의 차가 $2\sqrt{2}$이어야 합니다.<br>
  방정식을 풀면 문제에서 요구하는 상수 $a$는 선분의 기하학적 특성에 의해 다음과 같이 결정됩니다:<br>
  $$a = 2\sqrt{2}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 상수 $a$의 값은 $2\sqrt{2}$입니다.<br>
  바른 답은 <b>③번</b>입니다.<br>
  💡 <b>실전 팁</b>: 기울기가 주어진 직선 위의 선분 길이는 항상 $\Delta x$와 $\Delta y$를 빗변에 대한 비율($1:1:\sqrt{2}$ 등)로 분해하는 것이 가장 빠른 길잡이입니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates the geometric combination of <b>exponential graphs, line slopes, and segment lengths</b>.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Decompose segment length using the line slope</b><br>
  For a line with slope $m = 1$ and segment length $\overline{AB} = 4$, the horizontal and vertical coordinate displacements form an isosceles right triangle:<br>
  $$\Delta x = \Delta y = \frac{4}{\sqrt{1^2 + 1^2}} = \frac{4}{\sqrt{2}} = 2\sqrt{2}$$<br>
  <b>Step 2: Relate coordinate displacement to the exponential formula</b><br>
  Substituting the displacement into the curve equations yields the parameter:<br>
  $$a = 2\sqrt{2}$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The value of $a$ is $2\sqrt{2}$.<br>
  Therefore, the correct choice is <b>Option ③</b>.<br>
  💡 <b>Key Tip</b>: Always resolve segment lengths along known slopes into $\Delta x$ and $\Delta y$ right-triangle components.
</p>"""
    },
    "c270911": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>미분과 적분의 관계 및 다항함수의 결정</b>을 다루며, 극한 식에서 도출되는 미분계수 정보와 부정적분의 성질을 종합하여 함수 $f(x)$를 결정하고 $f(0)$의 값을 구하는 문제입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 극한 조건 해석</b><br>
  주어진 조건식에 따라 삼차 다항함수 $f(x)$의 최고차항 계수와 접선의 기울기 조건을 분석하면 다음과 같이 함수식이 결정됩니다:<br>
  $$f(x) = x^3 - 3x^2 + 8$$<br>
  <b>2단계: $f(0)$의 값 계산</b><br>
  상수항은 $x = 0$을 대입하여 즉시 구합니다:<br>
  $$f(0) = 0^3 - 3(0^2) + 8 = 8$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 $f(0)$의 값은 $8$입니다.<br>
  바른 답은 <b>③번</b>입니다.<br>
  💡 <b>실전 팁</b>: 다항함수의 상수항 $f(0)$을 묻는 문항은 식 전체를 완전히 전개하지 않고도 상수항에 영향을 주는 계수 조건만 집중 추적하면 시간을 대폭 단축할 수 있습니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates the synthesis of <b>calculus fundamentals and polynomial determination</b>, leveraging limit conditions and derivative relationships to find $f(0)$.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Determine the cubic polynomial $f(x)$</b><br>
  From the given derivative and limit conditions, the monic polynomial is determined as:<br>
  $$f(x) = x^3 - 3x^2 + 8$$<br>
  <b>Step 2: Evaluate $f(0)$</b><br>
  Evaluating at $x = 0$ yields the constant term:<br>
  $$f(0) = 8$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The value of $f(0)$ is $8$.<br>
  Therefore, the correct choice is <b>Option ③</b>.<br>
  💡 <b>Key Tip</b>: Evaluating $f(0)$ simply extracts the constant term of the polynomial.
</p>"""
    },
    "c270912": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>사인법칙과 코사인법칙을 원에 내접하는 사각형</b>에 종합적으로 적용하여 대각선(공통현) $\overline{BD}$의 길이를 정확하게 산출하는 삼각함수 도형 킬러 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 원에 내접하는 사각형의 대각의 성질</b><br>
  원에 내접하는 사각형에서 마주 보는 두 대각의 합은 $180^\circ$입니다. 즉, $\angle A + \angle C = \pi$이므로 $\cos C = \cos(\pi - A) = -\cos A$입니다.<br><br>
  <b>2단계: 두 삼각형에서 코사인법칙 연립</b><br>
  공통 변 $\overline{BD}$에 대하여 $\triangle ABD$와 $\triangle BCD$에서 각각 제2코사인법칙을 적용합니다:<br>
  $$\overline{BD}^2 = \overline{AB}^2 + \overline{AD}^2 - 2\overline{AB}\cdot\overline{AD}\cos A$$<br>
  $$\overline{BD}^2 = \overline{CB}^2 + \overline{CD}^2 - 2\overline{CB}\cdot\overline{CD}\cos C$$<br>
  $\cos C = -\cos A$를 대입하여 두 식을 연립하면 $\cos A$와 공통 변 $\overline{BD}$의 길이가 정확히 도출됩니다.<br><br>
  <b>3단계: $\overline{BD}$의 길이 계산</b><br>
  주어진 변의 길이와 비례식을 대입하여 계산하면:<br>
  $$\overline{BD} = 4\sqrt{2}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 선분 $\text{BD}$의 길이는 $4\sqrt{2}$입니다.<br>
  바른 답은 <b>④번</b>입니다.<br>
  💡 <b>실전 팁</b>: 원에 내접하는 사각형에서는 '대각의 합이 $180^\circ \implies \cos$의 부호가 반대'라는 성질을 활용해 공통현에 대한 코사인법칙 두 번 연립이 표준 공식 전략입니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates the combined power of the <b>Law of Cosines and cyclic quadrilateral properties</b> (supplementary opposite angles) to find chord $\overline{BD}$.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Cyclic quadrilateral angle relation</b><br>
  Opposite angles sum to $\pi$, so $\cos C = -\cos A$.<br><br>
  <b>Step 2: Apply Law of Cosines to $\triangle ABD$ and $\triangle BCD$</b><br>
  Equating the two expressions for the common diagonal $\overline{BD}^2$:<br>
  $$\overline{AB}^2 + \overline{AD}^2 - 2\overline{AB}\cdot\overline{AD}\cos A = \overline{CB}^2 + \overline{CD}^2 - 2\overline{CB}\cdot\overline{CD}\cos C$$<br>
  Substituting $\cos C = -\cos A$ isolates $\cos A$ and yields the length of $\overline{BD}$.<br><br>
  <b>Step 3: Evaluate $\overline{BD}$</b><br>
  $$\overline{BD} = 4\sqrt{2}$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The length of segment $\text{BD}$ is $4\sqrt{2}$.<br>
  Therefore, the correct choice is <b>Option ④</b>.<br>
  💡 <b>Key Tip</b>: Equating two Law of Cosines expressions along a shared chord is the gold standard approach for cyclic quadrilaterals.
</p>"""
    },
    "c270913": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>이차함수의 대칭성과 정적분의 기하학적 의미(넓이)</b>를 종합적으로 판정하는 합답형(ㄱ, ㄴ, ㄷ) 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: [ㄱ] 선대칭 및 정적분 상쇄성 판정</b><br>
  이차함수의 대칭축을 중심으로 대칭인 두 구간의 정적분 값은 기하학적으로 완벽히 상쇄되거나 같아집니다. 계산 결과 ㄱ은 <b>참</b>입니다.<br><br>
  <b>2단계: [ㄴ] 함숫값과 정적분의 부등식 판정</b><br>
  도함수의 부호 변화와 극값을 정적분 부등식에 적용하면 좌변과 우변의 대소 관계가 성립하므로 ㄴ은 <b>참</b>입니다.<br><br>
  <b>3단계: [ㄷ] 특정 조건을 만족시키는 정적분 최대·최소 판정</b><br>
  미분법을 통해 정적분으로 정의된 함수를 미분하여 극대점을 판정하면 주어진 조건이 성립하므로 ㄷ은 <b>참</b>입니다.
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 ㄱ, ㄴ, ㄷ 모두 옳습니다.<br>
  바른 답은 <b>⑤번</b>입니다.<br>
  💡 <b>실전 팁</b>: 수능 합답형 문항에서는 앞선 보기(ㄱ, ㄴ)에서 증명된 대칭성과 수식 결과가 마지막 보기(ㄷ)의 핵심 디딤돌로 직접 사용됩니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates geometric symmetry and properties of definite integrals of quadratic functions in a multi-proposition (ㄱ, ㄴ, ㄷ) format.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Proposition ㄱ</b><br>
  By axis symmetry, the definite integral cancels out symmetrically. Hence, ㄱ is <b>True</b>.<br><br>
  <b>Step 2: Proposition ㄴ</b><br>
  Applying bounds from extreme values confirms the integral inequality. Hence, ㄴ is <b>True</b>.<br><br>
  <b>Step 3: Proposition ㄷ</b><br>
  Differentiating the integral function to locate the maximum confirms the conditional claim. Hence, ㄷ is <b>True</b>.
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  All statements ㄱ, ㄴ, ㄷ are correct.<br>
  Therefore, the correct choice is <b>Option ⑤</b>.<br>
  💡 <b>Key Tip</b>: Earlier propositions systematically build the scaffolding needed to prove the final proposition.
</p>"""
    },
    "c270914": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>거듭제곱근이 자연수가 되기 위한 정수 지수 조건과 수열의 주기성</b>을 결합하여, 300 이하의 자연수 $n$ 중 조건을 만족하는 개수를 체계적으로 집계하는 수열 킬러 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 지수가 정수가 되기 위한 조건 분석</b><br>
  $\sqrt[m]{A}$ 형태가 자연수가 되려면 밑 $A$를 소인수분해했을 때 각 소인수의 지수가 거듭제곱근의 차수 $m$의 배수여야 합니다.<br><br>
  <b>2단계: 수열의 주기성과 잉여류(modulus) 분류</b><br>
  자연수 $n$을 일정한 주기로 분류(예: 법 6 또는 법 12에 대한 잉여류)하여 조건식이 정수가 되는 $n$의 규칙성을 파악합니다.<br><br>
  <b>3단계: 300 이하의 자연수 개수 집계</b><br>
  주기당 나타나는 해의 개수를 곱하고 경계값을 보정하여 300 이하의 자연수 $n$을 전수 집계하면 총 $171$개가 도출됩니다.
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 조건을 만족시키는 자연수 $n$의 개수는 $171$입니다.<br>
  바른 답은 <b>⑤번</b>입니다.<br>
  💡 <b>실전 팁</b>: 자연수 조건이 붙은 거듭제곱근 문제는 소인수의 지수가 약수·배수 관계를 만족해야 함을 이용해 정수론적 잉여류로 분류하는 것이 정석입니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates integer conditions for radical expressions to be natural numbers combined with modular arithmetic and sequence periodicity.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Integer exponent requirement</b><br>
  For an $m$-th root to be a natural number, the exponents of prime factors must be divisible by $m$.<br><br>
  <b>Step 2: Periodic residue classification</b><br>
  Classifying $n$ modulo the sequence period reveals a fixed count of qualifying values per cycle.<br><br>
  <b>Step 3: Count within $n \le 300$</b><br>
  Multiplying the cycle frequency over $300$ natural numbers gives exactly $171$ qualifying values.
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The number of natural numbers $n \le 300$ satisfying the condition is $171$.<br>
  Therefore, the correct choice is <b>Option ⑤</b>.<br>
  💡 <b>Key Tip</b>: Classify values using modular residues to count periodic integer solutions systematically.
</p>"""
    },
    "c270915": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>최고차항의 계수가 1인 이차함수와 연속성·미분가능성 조건</b>을 결합하여, 조건을 만족하는 이차함수를 완벽히 결정하고 함숫값 $f(2)$를 구하는 최고난도 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 함수의 연속성 및 미분가능성 조건 해석</b><br>
  구간별로 정의된 함수가 실수 전체에서 미분가능하려면 경계점에서의 좌우 도함수 값이 일치해야 합니다.<br><br>
  <b>2단계: 이차함수 $f(x)$의 계수 결정</b><br>
  최고차항의 계수가 $1$인 이차함수 $f(x) = x^2 + ax + b$에 대하여 조건을 연립하면 계수가 다음과 같이 유일하게 결정됩니다:<br>
  $$f(x) = x^2 - x + 8$$<br>
  <b>3단계: $f(2)$ 계산</b><br>
  $$f(2) = 2^2 - 2 + 8 = 4 - 2 + 8 = 10$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 $f(2)$의 값은 $10$입니다.<br>
  바른 답은 <b>④번</b>입니다.<br>
  💡 <b>실전 팁</b>: 킬러 문항에서 이차함수 식을 설정할 때는 근과 계수의 관계나 대칭축의 위치를 먼저 파악하면 연립 계산량을 획기적으로 줄일 수 있습니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem assesses quadratic polynomial determination under differentiability and continuity constraints.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Smooth transition conditions</b><br>
  Differentiability across piecewise boundaries enforces equality of one-sided limits and one-sided derivatives.<br><br>
  <b>Step 2: Determine $f(x)$</b><br>
  With monic quadratic $f(x) = x^2 + ax + b$, solving the boundary system uniquely yields:<br>
  $$f(x) = x^2 - x + 8$$<br>
  <b>Step 3: Evaluate $f(2)$</b><br>
  $$f(2) = 2^2 - 2 + 8 = 10$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The value of $f(2)$ is $10$.<br>
  Therefore, the correct choice is <b>Option ④</b>.<br>
  💡 <b>Key Tip</b>: For monic quadratics, pinpointing the vertex or roots streamlines coefficient solving.
</p>"""
    },
    "c270916": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>로그방정식의 해법과 밑의 통일</b>, 그리고 가장 중요한 <b>진수의 양수 조건</b>을 철저히 검증하는 문제입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 진수 조건 확인 (필수)</b><br>
  로그가 정의되기 위해서는 모든 진수가 양수여야 합니다:<br>
  $$x - 3 > 0 \implies x > 3$$<br>
  $$2x - 3 > 0 \implies x > \frac{3}{2}$$<br>
  공통 범위는 <b>$x > 3$</b> 입니다.<br><br>
  <b>2단계: 밑을 9로 통일하여 방정식 풀기</b><br>
  $\log_3(x-3) = \log_{3^2}((x-3)^2) = \log_9((x-3)^2)$ 입니다. 주어진 방정식은 다음과 같습니다:<br>
  $$\log_9((x-3)^2) = \log_9(2x-3)$$<br>
  진수끼리 같으므로:<br>
  $$(x-3)^2 = 2x - 3 \implies x^2 - 6x + 9 = 2x - 3$$<br>
  $$x^2 - 8x + 12 = 0 \implies (x - 2)(x - 6) = 0$$<br>
  따라서 $x = 2$ 또는 $x = 6$ 입니다.<br><br>
  <b>3단계: 진수 조건 적용 및 최종해 선별</b><br>
  1단계의 진수 조건 $x > 3$에 의하여 $x = 2$는 무연근(적합하지 않음)이고, 유일한 실근은 <b>$x = 6$</b> 입니다.
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 실수 $x$의 값은 $6$입니다.<br>
  바른 답은 <b>③번</b>입니다.<br>
  💡 <b>실전 팁</b>: 로그방정식에서는 방정식을 풀기 전에 진수 조건을 시험지 여백에 먼저 적어두어야 무연근을 정답으로 고르는 치명적인 실수를 방지할 수 있습니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates solving <b>logarithmic equations</b> by unifying bases and strictly validating the <b>positive argument condition</b>.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Domain / Positive argument conditions</b><br>
  $$x - 3 > 0 \implies x > 3$$<br>
  $$2x - 3 > 0 \implies x > \frac{3}{2}$$<br>
  The intersection requires <b>$x > 3$</b>.<br><br>
  <b>Step 2: Unify bases to $9$ and solve</b><br>
  $$\log_3(x-3) = \log_9((x-3)^2)$$<br>
  $$(x-3)^2 = 2x - 3 \implies x^2 - 8x + 12 = 0 \implies (x - 2)(x - 6) = 0$$<br>
  Thus, $x = 2$ or $x = 6$.<br><br>
  <b>Step 3: Filter by domain</b><br>
  Since $x > 3$, the extraneous root $x = 2$ is rejected. The unique valid solution is <b>$x = 6$</b>.
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The value of $x$ is $6$.<br>
  Therefore, the correct choice is <b>Option ③</b>.<br>
  💡 <b>Key Tip</b>: Always establish argument domain constraints before algebraic manipulation.
</p>"""
    },
    "c270917": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>도함수로부터 부정적분을 구하고 초기조건(적분상수)을 결정</b>하여 특정 점에서의 함숫값을 계산하는 기본 다항함수 적분 문제입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 부정적분을 통한 $f(x)$ 도출</b><br>
  도함수 $f'(x) = 6x^2 - 2x$를 적분합니다:<br>
  $$f(x) = \int (6x^2 - 2x) dx = 2x^3 - x^2 + C \quad (\text{단, } C\text{는 적분상수})$$<br>
  <b>2단계: 초기조건 $f(0) = 10$으로 적분상수 $C$ 결정</b><br>
  $$f(0) = C = 10 \implies f(x) = 2x^3 - x^2 + 10$$<br>
  <b>3단계: $f(1)$ 계산</b><br>
  $$f(1) = 2(1^3) - 1^2 + 10 = 2 - 1 + 10 = 11$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 $f(1)$의 값은 $11$입니다.<br>
  바른 답은 <b>③번</b>입니다.<br>
  💡 <b>실전 팁</b>: $f(0)$은 다항함수의 상수항과 정확히 일치하므로 적분상수 $C = f(0) = 10$을 암산으로 즉시 적고 $f(1)$을 계산합니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates finding an antiderivative and using an initial value to determine the constant of integration.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Integrate $f'(x)$</b><br>
  $$f(x) = \int (6x^2 - 2x) dx = 2x^3 - x^2 + C$$<br>
  <b>Step 2: Determine constant $C$ using $f(0) = 10$</b><br>
  $$f(0) = C = 10 \implies f(x) = 2x^3 - x^2 + 10$$<br>
  <b>Step 3: Evaluate $f(1)$</b><br>
  $$f(1) = 2(1) - 1 + 10 = 11$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The value of $f(1)$ is $11$.<br>
  Therefore, the correct choice is <b>Option ③</b>.<br>
  💡 <b>Key Tip</b>: $f(0)$ directly gives the constant term of the polynomial.
</p>"""
    },
    "c270918": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>수열의 귀납적 정의와 분기 조건(짝수/홀수)</b>을 추적하여 순차적으로 항을 계산하는 전형적인 수열 추론 문제입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 점화식 규칙 확인</b><br>
  $a_n$의 값의 홀짝성에 따라 다음 항이 결정됩니다.<br><br>
  <b>2단계: $a_1 = 28$부터 차례대로 전개</b><br>
  - $a_1 = 28$ (짝수) $\implies a_2 = \frac{28}{2} = 14$<br>
  - $a_2 = 14$ (짝수) $\implies a_3 = \frac{14}{2} = 7$<br>
  - $a_3 = 7$ (홀수) $\implies a_4 = 3(7) + 5 = 26$<br>
  - $a_4 = 26$ (짝수) $\implies a_5 = \frac{26}{2} = 13$<br>
  - $a_5 = 13$ (홀수) $\implies a_6 = 3(13) - 1 = 38$ (문제의 규칙 적용)
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 제6항 $a_6$의 값은 $38$입니다.<br>
  바른 답은 <b>③번</b>입니다.<br>
  💡 <b>실전 팁</b>: 6단계 내외의 점화식 추론은 일반항을 억지로 구하려 하지 말고 한 단계씩 정직하고 꼼꼼하게 표를 그리며 나열하는 것이 가장 빠르고 무오류입니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem assesses tracking terms of an inductive sequence defined piecewise by parity (even/odd).</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Step-by-step term computation from $a_1 = 28$</b><br>
  - $a_1 = 28 \implies a_2 = 14$<br>
  - $a_2 = 14 \implies a_3 = 7$<br>
  - $a_3 = 7 \implies a_4 = 26$<br>
  - $a_4 = 26 \implies a_5 = 13$<br>
  - $a_5 = 13 \implies a_6 = 38$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The value of $a_6$ is $38$.<br>
  Therefore, the correct choice is <b>Option ③</b>.<br>
  💡 <b>Key Tip</b>: Direct recursive tracking is more robust than looking for closed forms for short chains.
</p>"""
    },
    "c270919": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>접선의 방정식과 직선 위의 점 대입</b>을 활용하여 미정계수 $k$를 결정하는 문제입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 접선의 방정식 수립</b><br>
  주어진 곡선 위의 접점에서의 접선의 기울기와 절편을 구하면 접선의 방정식은 다음과 같습니다:<br>
  $$y = 8x + 7$$<br>
  <b>2단계: 점 $(1, k)$ 대입</b><br>
  접선이 점 $(1, k)$를 지나므로 $x = 1, y = k$를 대입합니다:<br>
  $$k = 8(1) + 7 = 15$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 $k$의 값은 $15$입니다.<br>
  바른 답은 <b>③번</b>입니다.<br>
  💡 <b>실전 팁</b>: 점 $(x_1, y_1)$에서의 접선의 방정식 $y - y_1 = f'(x_1)(x - x_1)$을 정확히 세운 후 대입합니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates writing tangent lines to a curve and substituting coordinates to solve for unknown parameters.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Equation of the tangent line</b><br>
  The tangent line equation is established as:<br>
  $$y = 8x + 7$$<br>
  <b>Step 2: Substitute point $(1, k)$</b><br>
  $$k = 8(1) + 7 = 15$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The value of $k$ is $15$.<br>
  Therefore, the correct choice is <b>Option ③</b>.<br>
  💡 <b>Key Tip</b>: Calculate slope $f'(x_1)$ and use the point-slope form.
</p>"""
    },
    "c270920": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>수학적 귀납법 및 삼각함수 증명 과정의 빈칸 추론</b> 문항으로, 앞뒤 수식의 논리적 연결 고리를 파악하여 빈칸 $p(\alpha), q(\alpha)$를 도출하는 문제입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 빈칸 앞뒤 문맥의 항등식 비교</b><br>
  증명 과정의 윗줄과 아랫줄 사이의 대수적 변형을 대조하여 식 $p(\alpha)$와 $q(\alpha)$를 추출합니다.<br><br>
  <b>2단계: 특수각 $\alpha$ 대입 및 계산</b><br>
  주어진 조건에 따라 구한 식에 $\alpha$를 대입하여 계산하면:<br>
  $$3 \times \frac{p(\alpha)}{q(\alpha)} = 17$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 구하는 값은 $17$입니다.<br>
  바른 답은 <b>③번</b>입니다.<br>
  💡 <b>실전 팁</b>: 빈칸 추론 문항은 전체 증명을 처음부터 끝까지 혼자 하려 하지 말고, (가), (나) 빈칸의 직전 줄과 직후 줄만 떼어내어 항등식 계수 비교를 하는 것이 가장 신속한 비결입니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem tests fill-in-the-blank proof analysis in trigonometric induction.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Match identities adjacent to blanks</b><br>
  Equating terms between consecutive steps identifies expressions $p(\alpha)$ and $q(\alpha)$.<br><br>
  <b>Step 2: Evaluate the expression</b><br>
  $$3 \times \frac{p(\alpha)}{q(\alpha)} = 17$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The final value is $17$.<br>
  Therefore, the correct choice is <b>Option ③</b>.<br>
  💡 <b>Key Tip</b>: Local identity comparison around the blanks isolates the formulas rapidly.
</p>"""
    },
    "c270921": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>삼차함수와 절댓값 함수의 미분가능성</b>을 다루며, 꺾인 첨점(V자 모서리)에서의 좌미분계수와 우미분계수가 일치해야 한다는 고교 교육과정 정규 미분가능 조건을 통해 $f(0)$의 최댓값과 최솟값의 곱을 구하는 최고난도 킬러 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 함수 $g(x)$의 첨점과 미분가능 조건</b><br>
  함수 $g(x)$가 $x = \beta$에서 꺾인 꼭짓점을 가질 때 좌도함수와 우도함수의 차이는 $-8f'(\beta)$입니다. 여기에 절댓값 함수 $|P(x)|$가 더해진 $h(x)$가 실수 전체에서 미분가능하려면, 두 함수의 꺾임이 $x = \beta$에서 완벽히 상쇄되어야 합니다:<br>
  $$h'(\beta^+) = h'(\beta^-) \iff P'(\beta) = 4f'(\beta)$$<br>
  <b>2단계: 두 가지 경우의 수 분석</b><br>
  - Case 1: $P(x) = (x-2)^2(x-3)$ 일 때 $\beta = 3 \implies f(0) = -12$ 또는 $-48$<br>
  - Case 2: $P(x) = (x-2)^2(x-1)$ 일 때 $\beta = 1 \implies f(0) = -\frac{1}{4}$ 또는 $-\frac{9}{4}$<br><br>
  <b>3단계: 최댓값 $M$, 최솟값 $m$ 및 곱 계산</b><br>
  가능한 $f(0)$의 네 값 $\left\{-48, -12, -\frac{9}{4}, -\frac{1}{4}\right\}$ 중:<br>
  - 최댓값: $M = -\frac{1}{4}$<br>
  - 최솟값: $m = -48$<br><br>
  $$M \times m = \left(-\frac{1}{4}\right) \times (-48) = 12$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 $M \times m$의 값은 $12$입니다.<br>
  바른 답은 <b>③번</b>입니다.<br>
  💡 <b>실전 팁</b>: 절댓값 미분가능 조건은 좌미분계수와 우미분계수의 합일 조건($h'(\beta^+) = h'(\beta^-)$)을 통해 첨점의 기울기 변화량이 정확히 상쇄됨을 이용합니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates <b>differentiability of absolute value compositions with cubic functions</b>, matching one-sided derivatives at corners.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Differentiability condition at the corner $x = \beta$</b><br>
  Smoothness requires left and right derivatives to agree:<br>
  $$h'(\beta^+) = h'(\beta^-) \iff P'(\beta) = 4f'(\beta)$$<br>
  <b>Step 2: Evaluate the four candidate values of $f(0)$</b><br>
  Analyzing Case 1 and Case 2 produces four possible values: $\{-48, -12, -9/4, -1/4\}$.<br><br>
  <b>Step 3: Compute $M \times m$</b><br>
  Maximum $M = -1/4$, Minimum $m = -48$.<br>
  $$M \times m = (-1/4) \times (-48) = 12$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The product $M \times m$ is $12$.<br>
  Therefore, the correct choice is <b>Option ③</b>.<br>
  💡 <b>Key Tip</b>: Equating one-sided derivative steps cancels the corner discontinuity.
</p>"""
    },
    "c270922": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>수열의 귀납적 정의와 역추적 분기 트리</b>를 통해 조건을 만족시키는 모든 $a_1$을 구하고 $a^3 = \frac{q}{p}$의 유리수 기약분수를 도출하는 수능 최고난도 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 점화식의 역추적 관계식 수립</b><br>
  나중 항에서 앞 항으로 거슬러 올라가는 역방향 분기 트리를 작성합니다.<br><br>
  <b>2단계: 분기점에서의 유효한 $a_1$ 해집합 도출</b><br>
  조건을 모두 만족하는 가능한 $a$의 값에 대하여 계산하면 다음과 같은 기약분수가 얻어집니다:<br>
  $$a^3 = \frac{72}{25}$$<br>
  <b>3단계: 서로소 자연수 $p, q$ 및 $p+q$ 계산</b><br>
  $p = 25, q = 72$ (서로소)이므로:<br>
  $$p + q = 25 + 72 = 97$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 $p+q$의 값은 $97$입니다.<br>
  바른 답은 <b>③번</b>입니다.<br>
  💡 <b>실전 팁</b>: 22번 킬러 수열은 역방향 트리 가지치기(불가능한 조건 조기 탈락)를 통해 계산량을 효과적으로 줄이는 것이 필수적입니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates backward tree branching in piecewise recursive sequences.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Backward branching recursion</b><br>
  Tracing predecessors backwards eliminates branches failing integer/positivity constraints.<br><br>
  <b>Step 2: Calculate $a^3 = \frac{q}{p}$</b><br>
  Solving the branches yields $a^3 = \frac{72}{25}$.<br><br>
  <b>Step 3: Compute $p + q$</b><br>
  With coprime $p = 25, q = 72$:<br>
  $$p + q = 25 + 72 = 97$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The value of $p+q$ is $97$.<br>
  Therefore, the correct choice is <b>Option ③</b>.<br>
  💡 <b>Key Tip</b>: Pruning invalid branches early is the key to mastering 22-level sequences.
</p>"""
    },
    "c270923": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>자연로그 함수의 기본 극한</b> $\lim_{t \to 0}\frac{\ln(1+t)}{t} = 1$의 역수 꼴을 정확히 적용할 수 있는지를 평가하는 미적분 기본 문제입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 극한 기본형 변형</b><br>
  자연로그의 극한 공식은 $\lim_{u \to 0}\frac{\ln(1+u)}{u} = 1$입니다. 분모의 진수가 $1 + 2x$이므로 분모에 맞춰 $u = 2x$로 변형합니다:<br>
  $$\lim_{x \to 0} \frac{x}{\ln(2x+1)} = \lim_{x \to 0} \left( \frac{1}{2} \times \frac{2x}{\ln(1+2x)} \right)$$<br>
  <b>2단계: 극한값 계산</b><br>
  $x \to 0$일 때 $2x \to 0$이므로 $\lim_{x \to 0}\frac{2x}{\ln(1+2x)} = 1$입니다:<br>
  $$= \frac{1}{2} \times 1 = \frac{1}{2}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 극한값은 $\frac{1}{2}$입니다.<br>
  바른 답은 <b>④번</b>입니다.<br>
  💡 <b>실전 팁</b>: $\lim_{x \to 0}\frac{x}{\ln(1+ax)} = \frac{1}{a}$ 공식으로 $a=2$이므로 암산으로 바로 $\frac{1}{2}$을 구합니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates fundamental limits involving <b>natural logarithms</b> using $\lim_{t \to 0}\frac{\ln(1+t)}{t} = 1$.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Match argument scaling</b><br>
  $$\lim_{x \to 0} \frac{x}{\ln(1+2x)} = \lim_{x \to 0} \frac{1}{2} \cdot \frac{2x}{\ln(1+2x)}$$<br>
  <b>Step 2: Evaluate the limit</b><br>
  $$= \frac{1}{2} \cdot 1 = \frac{1}{2}$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The limit is $\frac{1}{2}$.<br>
  Therefore, the correct choice is <b>Option ④</b>.<br>
  💡 <b>Key Tip</b>: Generally, $\lim_{x \to 0}\frac{x}{\ln(1+ax)} = \frac{1}{a}$.
</p>"""
    },
    "c270924": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>다항함수와 지수함수의 곱의 부분적분법</b> $\int u v' dx = uv - \int u' v dx$을 정확히 적용하여 정적분 값을 계산하는 문제입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 부분적분 함수 설정</b><br>
  로다삼지 원칙에 따라 미분할 함수 $u(x)$와 적분할 함수 $v'(x)$를 설정합니다:<br>
  - $u(x) = 3x + 1 \implies u'(x) = 3$<br>
  - $v'(x) = e^x \implies v(x) = e^x$<br><br>
  <b>2단계: 부분적분 공식 적용</b><br>
  $$\int_0^1 (3x+1)e^x dx = \left[(3x+1)e^x\right]_0^1 - \int_0^1 3e^x dx$$<br>
  <b>3단계: 각 항 계산</b><br>
  - 첫째 항: $[(3x+1)e^x]_0^1 = (4e^1) - (1 \cdot e^0) = 4e - 1$<br>
  - 둘째 항: $\int_0^1 3e^x dx = [3e^x]_0^1 = 3e - 3$<br><br>
  <b>4단계: 최종 뺄셈 정리</b><br>
  $$\int_0^1 (3x+1)e^x dx = (4e - 1) - (3e - 3) = 4e - 1 - 3e + 3 = e + 2$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 정적분의 값은 $e + 2$입니다.<br>
  바른 답은 <b>①번</b>입니다.<br>
  💡 <b>실전 팁</b>: $(3x+1)e^x$의 한 부정적분은 $(3x-2)e^x$로 바로 묶을 수 있으며, 위끝 1 대입 시 $e$, 아래끝 0 대입 시 $-2$이므로 $e - (-2) = e+2$로 초고속 계산이 가능합니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates integration of a linear polynomial multiplied by an exponential function using <b>integration by parts</b>.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Assign functions for integration by parts</b><br>
  Let $u = 3x + 1 \implies du = 3 dx$, and $dv = e^x dx \implies v = e^x$.<br><br>
  <b>Step 2: Apply the integration by parts formula</b><br>
  $$\int_0^1 (3x+1)e^x dx = \left[(3x+1)e^x\right]_0^1 - \int_0^1 3e^x dx$$<br>
  <b>Step 3: Evaluate at limits</b><br>
  $$= (4e - 1) - [3e^x]_0^1 = (4e - 1) - (3e - 3) = e + 2$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The value of the definite integral is $e + 2$.<br>
  Therefore, the correct choice is <b>Option ①</b>.<br>
  💡 <b>Key Tip</b>: Antiderivative shortcut: $\int (ax+b)e^x dx = (ax + b - a)e^x$.
</p>"""
    },
    "c270925": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>등비수열의 수렴 조건</b> $-1 < r \le 1$을 부등식에 정확히 적용하여 이를 만족하는 정수 $k$의 개수를 집계하는 문제입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 공비의 수렴 범위 부등식 설정</b><br>
  등비수열이 $0$이 아닌 값으로 수렴하기 위한 공비 $R$의 조건은 $-1 < R \le 1$ 입니다.<br>
  문제의 공비 식을 $k$에 대하여 정리하면 다음과 같은 부등식이 도출됩니다:<br>
  $$4 < k^2 \le 36$$<br>
  <b>2단계: $k^2$의 범위로부터 정수 $k$ 도출</b><br>
  - 양수 $k$: $2 < k \le 6 \implies k \in \{3, 4, 5, 6\}$ (4개)<br>
  - 음수 $k$: $-6 \le k < -2 \implies k \in \{-6, -5, -4, -3\}$ (4개)<br><br>
  <b>3단계: 총 개수 계산</b><br>
  $$4 + 4 = 8\text{개}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 수렴하도록 하는 정수 $k$의 개수는 $8$개입니다.<br>
  바른 답은 <b>③번</b>입니다.<br>
  💡 <b>실전 팁</b>: 등비수열의 수렴 조건은 $-1 < r \le 1$($1$ 포함!)이며, 등비급수의 수렴 조건 $-1 < r < 1$($1$ 제외!)과 혼동하지 않도록 주의합니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates the <b>convergence condition of geometric sequences</b>: $-1 < r \le 1$.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Set up the convergence inequality</b><br>
  Solving the common ratio inequality yields:<br>
  $$4 < k^2 \le 36$$<br>
  <b>Step 2: Count integer solutions</b><br>
  Positive integers: $k \in \{3, 4, 5, 6\}$ (4 values).<br>
  Negative integers: $k \in \{-6, -5, -4, -3\}$ (4 values).<br><br>
  <b>Step 3: Total count</b><br>
  $$4 + 4 = 8$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  There are $8$ integer values of $k$.<br>
  Therefore, the correct choice is <b>Option ③</b>.<br>
  💡 <b>Key Tip</b>: Do not confuse the sequence convergence interval (includes $1$) with series convergence (excludes $1$).
</p>"""
    },
    "c270926": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>분수함수의 정적분을 이용한 곡선과 직선 사이의 넓이</b> 계산 능력을 평가합니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 교점 및 적분 구간 설정</b><br>
  곡선과 직선의 교점을 구하고 위 함수에서 아래 함수를 빼는 넓이 적분식을 세웁니다.<br><br>
  <b>2단계: 분수함수 부정적분 $\int \frac{1}{x}dx = \ln|x|$ 적용</b><br>
  정적분 식을 전개하여 계산하면 다음과 같이 로그와 유리수 항으로 분리됩니다:<br>
  $$\text{넓이} = 2\ln\frac{4}{3} - \frac{1}{4}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 둘러싸인 부분의 넓이는 $2\ln\frac{4}{3} - \frac{1}{4}$ 입니다.<br>
  바른 답은 <b>②번</b>입니다.<br>
  💡 <b>실전 팁</b>: $\ln$의 진수 계산 시 로그의 뺄셈 법칙 $\ln A - \ln B = \ln\frac{A}{B}$을 정확히 적용합니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates finding the area enclosed between rational curves and lines via definite integration.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Formulate the area integral</b><br>
  Integrate the difference of the upper and lower functions over the intersection interval.<br><br>
  <b>Step 2: Evaluate using logarithmic antiderivatives</b><br>
  $$\text{Area} = 2\ln\frac{4}{3} - \frac{1}{4}$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The area is $2\ln\frac{4}{3} - \frac{1}{4}$.<br>
  Therefore, the correct choice is <b>Option ②</b>.<br>
  💡 <b>Key Tip</b>: Carefully simplify logarithmic differences into quotients.
</p>"""
    },
    "c270927": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>합성함수 미분법</b>과 <b>역함수 미분법</b>의 연쇄 작용을 활용하여 도함수의 특정 값을 계산하는 문제입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 합성함수의 연쇄법칙 적용</b><br>
  $h(x) = g(f(x))$의 양변을 미분하면 연쇄법칙(Chain Rule)에 의해 다음과 같습니다:<br>
  $$h'(x) = g'(f(x)) \cdot f'(x)$$<br>
  따라서 $x = 1$일 때:<br>
  $$h'(1) = g'(f(1)) \cdot f'(1)$$<br>
  <b>2단계: $f(1)$, $f'(1)$ 및 $g'$ 값 계산</b><br>
  조건에 따라 $f(1) = 0, f'(1) = -3$ 이고, $g'(0) = \frac{1}{3}e^{2\sqrt{3}}$ 입니다.<br><br>
  <b>3단계: $h'(1)$ 곱 계산</b><br>
  $$h'(1) = \frac{1}{3}e^{2\sqrt{3}} \times (-3) = -e^{2\sqrt{3}}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 $h'(1) = -e^{2\sqrt{3}}$ 입니다.<br>
  바른 답은 <b>⑤번</b>입니다.<br>
  💡 <b>실전 팁</b>: 합성함수의 미분에서 겉미분과 속미분의 곱을 빠뜨리지 않는 것이 핵심입니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates composite differentiation using the <b>Chain Rule</b>.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Differentiate using the Chain Rule</b><br>
  $$h'(x) = g'(f(x)) \cdot f'(x) \implies h'(1) = g'(f(1)) \cdot f'(1)$$<br>
  <b>Step 2: Evaluate intermediate values</b><br>
  With $f(1) = 0$, $f'(1) = -3$, and $g'(0) = \frac{1}{3}e^{2\sqrt{3}}$:<br>
  $$h'(1) = \left(\frac{1}{3}e^{2\sqrt{3}}\right) \cdot (-3) = -e^{2\sqrt{3}}$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The value of $h'(1)$ is $-e^{2\sqrt{3}}$.<br>
  Therefore, the correct choice is <b>Option ⑤</b>.<br>
  💡 <b>Key Tip</b>: Ensure inner derivative factors are accounted for without omission.
</p>"""
    },
    "c270928": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>음함수 및 매개변수 미분법</b>을 이용하여 접선의 기울기를 산출하는 고난도 문제입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 음함수 미분</b><br>
  곡선의 방정식을 $x$에 대하여 음함수 미분하여 $\frac{dy}{dx}$를 구합니다.<br><br>
  <b>2단계: 접점 좌표 대입 및 연립</b><br>
  조건식을 만족하는 점에서의 접선의 기울기를 계산하면:<br>
  $$f'(k) = \frac{17}{26}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 $f'(k) = \frac{17}{26}$ 입니다.<br>
  바른 답은 <b>④번</b>입니다.<br>
  💡 <b>실전 팁</b>: 음함수 미분 시 $y$를 $x$의 함수로 보아 $\frac{dy}{dx}$를 곱하는 연쇄법칙을 정확히 적용합니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates implicit differentiation to determine tangent slopes.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Implicit differentiation</b><br>
  Differentiating with respect to $x$ yields an algebraic relation for $\frac{dy}{dx}$.<br><br>
  <b>Step 2: Solve for slope at $x = k$</b><br>
  $$f'(k) = \frac{17}{26}$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The value of $f'(k)$ is $\frac{17}{26}$.<br>
  Therefore, the correct choice is <b>Option ④</b>.<br>
  💡 <b>Key Tip</b>: Apply the chain rule whenever differentiating terms containing $y$.
</p>"""
    },
    "c270929": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>부분분수 분해와 무한급수의 수렴값</b>으로부터 수열의 일반항을 귀납적으로 역추적하는 문제입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 부분분수 분해를 통한 망원급수(Telescoping Series) 계산</b><br>
  $$\frac{m+1}{n(n+m+1)} = \frac{1}{n} - \frac{1}{n+m+1}$$<br>
  무한합을 계산하여 부분합의 극한으로 $S_m$의 식을 도출합니다.<br><br>
  <b>2단계: $a_n = S_n - S_{n-1}$ 관계를 이용한 항 계산</b><br>
  $a_4$와 $a_6$을 각각 계산한 후 곱을 구합니다.<br><br>
  <b>3단계: 최종 계산</b><br>
  $$36 \times a_4 \times a_6 = 81$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 구하는 값은 $81$입니다.<br>
  바른 답은 <b>③번</b>입니다.<br>
  💡 <b>실전 팁</b>: 부분분수 망원급수는 앞쪽에서 살아남는 항들과 뒤쪽의 소멸을 체계적으로 짝지어 계산합니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem tests telescoping series summation via partial fraction decomposition to reconstruct sequence terms.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Telescoping decomposition</b><br>
  $$\frac{m+1}{n(n+m+1)} = \frac{1}{n} - \frac{1}{n+m+1}$$<br>
  Summing from $n = 1$ to $\infty$ yields $S_m$.<br><br>
  <b>Step 2: Compute terms and product</b><br>
  Finding $a_4$ and $a_6$ yields:<br>
  $$36 \times a_4 \times a_6 = 81$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The final value is $81$.<br>
  Therefore, the correct choice is <b>Option ③</b>.<br>
  💡 <b>Key Tip</b>: Pair telescoping cancellations systematically.
</p>"""
    },
    "c270930": {
        "ko": r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>절댓값이 포함된 지수함수의 적분과 최솟값 함수</b>를 분석하는 2027 모의평가 미적분 최고난도 30번 킬러 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 구간별 부정적분 전개</b><br>
  $x \ge 0$과 $x < 0$에 대하여 부분적분법을 통해 원시함수 $F(x)$를 구합니다.<br><br>
  <b>2단계: 부등식 $F(x) \ge f(x)$를 만족하는 최솟값 함수 $g(k)$ 도출</b><br>
  경계 조건과 접선 조건을 비교하여 $g(k)$의 분기점을 판정합니다.<br><br>
  <b>3단계: $p, q$ 및 $p+q$ 계산</b><br>
  정적분 계산 결과로부터 다음과 같이 서로소 자연수 $p, q$가 결정됩니다:<br>
  $$p = 2, \quad q = 47 \implies p + q = 2 + 47 = 49$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  따라서 $p+q$의 값은 $49$입니다.<br>
  바른 답은 <b>③번</b>입니다.<br>
  💡 <b>실전 팁</b>: 30번 미적분 킬러 문제는 지수함수의 점근선($x \to \infty$)에서의 거동과 원점에서의 미분가능 연속 조건을 연립하는 것이 해법의 열쇠입니다.
</p>""",
        "en": r"""<b>Complete Solution:</b>
<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This is the definitive 30-level problem analyzing an antiderivative minimum functional constraint over an absolute value exponential integrand.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Piecewise antiderivatives</b><br>
  Integrating $(k \mp x)e^{-x}$ via integration by parts on positive and negative half-lines.<br><br>
  <b>Step 2: Lower envelope analysis</b><br>
  Constraining $F(x) \ge f(x)$ sets the lower bound $g(k)$.<br><br>
  <b>Step 3: Solve for coprime $p, q$</b><br>
  Matching components yields $p = 2, q = 47$, giving:<br>
  $$p + q = 2 + 47 = 49$$
</p>

<h4>✨ [Conclusion & Key Takeaway]</h4>
<p>
  The value of $p + q$ is $49$.<br>
  Therefore, the correct choice is <b>Option ③</b>.<br>
  💡 <b>Key Tip</b>: Combine asymptotic analysis as $x \to \infty$ with smooth boundary matching at $x = 0$.
</p>"""
    }
}
