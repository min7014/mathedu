# solutions_c30_part2.py: Problems c30911 ~ c30920
SOLUTIONS_PART2 = {
    'c30911': {
        'ko': r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 수직선 위를 움직이는 두 점의 <b>위치 함수($x(t)$), 속도 함수($v(t) = x'(t)$), 가속도 함수($a(t) = v'(t)$)의 미분 관계</b>를 파악하고, 두 점이 만나는 시각($x_1(t) = x_2(t)$)에서의 가속도의 차를 정확히 구하는 능력을 평가합니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 두 점이 만나는 시각 $t$ 구하기</b><br>
  두 점 $P, Q$의 위치가 같아지는 시각은 $x_1(t) = x_2(t)$를 만족하는 $t \ge 0$입니다.<br>
  $$t^2 + t - 6 = -t^3 + 7t^2 \implies t^3 - 6t^2 + t - 6 = 0$$
  공통인수로 묶어 인수분해하면 다음과 같습니다.<br>
  $$t^2(t-6) + (t-6) = (t-6)(t^2+1) = 0$$
  모든 실수 $t$에 대하여 $t^2 + 1 > 0$ 이므로 두 점이 만나는 유일한 시각은 $t = 6$ 입니다.
  <br><br>
  <b>2단계: 속도 및 가속도 도함수 유도</b><br>
  각 점의 위치 함수를 시간에 대해 두 번 미분하여 가속도 함수를 구합니다.<br>
  • 점 $P$:<br>
  $$v_1(t) = x_1'(t) = 2t + 1 \implies a_1(t) = v_1'(t) = 2$$<br>
  • 점 $Q$:<br>
  $$v_2(t) = x_2'(t) = -3t^2 + 14t \implies a_2(t) = v_2'(t) = -6t + 14$$
  <br>
  <b>3단계: $t=6$에서의 가속도 $p, q$ 및 차 $p-q$ 계산</b><br>
  $t=6$을 대입합니다.<br>
  $$p = a_1(6) = 2$$<br>
  $$q = a_2(6) = -6(6) + 14 = -36 + 14 = -22$$<br>
  따라서 구하는 값은:<br>
  $$p - q = 2 - (-22) = 2 + 22 = 24$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  구하는 값 $p-q$는 $24$ 입니다.<br>
  따라서 올바른 정답은 <b>①번</b>입니다.<br>
  💡 <b>실전 팁</b>: 3차 방정식 인수분해 시 계수의 비율($1:-6 = 1:-6$)을 관찰하면 조립제법 없이도 $t^2(t-6) + (t-6)$으로 순식간에 묶어낼 수 있습니다.
</p>""",
        'en': r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem assesses differential calculus applied to rectilinear kinematics: finding the encounter time ($x_1(t) = x_2(t)$) for two moving particles and evaluating their respective accelerations via second derivatives ($a(t) = x''(t)$).</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Determine the encounter time $t$</b><br>
  The particles $P$ and $Q$ meet when their positions coincide ($x_1(t) = x_2(t)$) for $t \ge 0$:<br>
  $$t^2 + t - 6 = -t^3 + 7t^2 \implies t^3 - 6t^2 + t - 6 = 0$$<br>
  Factor by grouping terms:<br>
  $$t^2(t-6) + (t-6) = (t-6)(t^2+1) = 0$$<br>
  Since $t^2+1 > 0$ for all real $t$, the unique meeting moment is $t = 6$.
  <br><br>
  <b>Step 2: Differentiate positions to obtain acceleration functions</b><br>
  • For particle $P$:<br>
  $$v_1(t) = x_1'(t) = 2t + 1 \implies a_1(t) = 2$$<br>
  • For particle $Q$:<br>
  $$v_2(t) = x_2'(t) = -3t^2 + 14t \implies a_2(t) = -6t + 14$$
  <br>
  <b>Step 3: Evaluate accelerations at $t = 6$ and compute $p - q$</b><br>
  $$p = a_1(6) = 2$$<br>
  $$q = a_2(6) = -6(6) + 14 = -22$$<br>
  Subtracting gives:<br>
  $$p - q = 2 - (-22) = 24$$
</p>

<h4>✨ [Conclusion & Key Takeaways]</h4>
<p>
  The final value $p-q$ is $24$.<br>
  Therefore, the correct choice is <b>Option ①</b>.<br>
  💡 <b>Strategy Tip</b>: Observing proportional coefficients in the cubic polynomial permits instant grouping without relying on synthetic division.
</p>"""
    },
    'c30912': {
        'ko': r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 등차수열 $\{a_n\}$에 대하여 부호가 교대로 바뀌는 누적합으로 정의된 새로운 수열 $\{b_n\}$의 <b>홀수 항과 짝수 항의 주기적·규칙적 특성</b>을 분석하고 합을 구하는 수열 추론 문제입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 공차 $d$의 도출</b><br>
  등차수열 $\{a_n\}$의 첫째항을 $a_1$, 공차를 $d$라 합시다.<br>
  $b_2 = a_1 - a_2$ 이고 등차수열의 정의에 의해 $a_2 - a_1 = d$ 이므로<br>
  $$b_2 = -(a_2 - a_1) = -d = -2 \implies d = 2$$
  <br>
  <b>2단계: $b_3 + b_7 = 0$ 조건을 통한 첫째항 $a_1$ 결정</b><br>
  홀수 번째 항 $b_{2k-1}$의 구조를 관찰하면 인접한 두 항의 차가 $-d$로 묶입니다.<br>
  • $b_3 = (a_1 - a_2) + a_3 = -d + a_3 = a_3 - 2$<br>
  • $b_7 = (a_1 - a_2) + (a_3 - a_4) + (a_5 - a_6) + a_7 = -3d + a_7 = a_7 - 6$<br>
  조건 $b_3 + b_7 = 0$ 에 대입하면:<br>
  $$(a_3 - 2) + (a_7 - 6) = a_3 + a_7 - 8 = 0$$
  $a_3 = a_1 + 2d = a_1 + 4$, $a_7 = a_1 + 6d = a_1 + 12$ 이므로<br>
  $$(a_1 + 4) + (a_1 + 12) - 8 = 2a_1 + 8 = 0 \implies a_1 = -4$$
  따라서 등차수열의 일반항은 $a_n = -4 + 2(n-1) = 2n - 6$ 입니다.
  <br><br>
  <b>3단계: $b_1$부터 $b_9$까지의 총합 계산</b><br>
  • 짝수 항 ($b_{2k} = -kd = -2k$):<br>
  $b_2 = -2,\; b_4 = -4,\; b_6 = -6,\; b_8 = -8$<br>
  $$\sum_{k=1}^4 b_{2k} = -(2 + 4 + 6 + 8) = -20$$<br>
  • 홀수 항 ($b_{2k-1} = -(k-1)d + a_{2k-1} = -2(k-1) + [2(2k-1)-6] = 2k-6$):<br>
  $b_1 = -4,\; b_3 = -2,\; b_5 = 0,\; b_7 = 2,\; b_9 = 4$<br>
  $$\sum_{k=1}^5 b_{2k-1} = (-4) + (-2) + 0 + 2 + 4 = 0$$<br>
  따라서 제1항부터 제9항까지의 합은:<br>
  $$\sum_{n=1}^9 b_n = \sum_{k=1}^5 b_{2k-1} + \sum_{k=1}^4 b_{2k} = 0 + (-20) = -20$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  구하는 합은 $-20$ 입니다.<br>
  따라서 올바른 정답은 <b>②번</b>입니다.<br>
  💡 <b>실전 팁</b>: 부호 교대 수열 $b_n$은 짝수 항에서는 인접한 쌍들이 모두 $-d$로 깔끔하게 묶이고, 홀수 항은 등차수열을 이룹니다. 짝수항과 홀수항을 분리하여 더하면 대칭성에 의해 홀수 항의 합이 $0$이 되어 계산이 대단히 명쾌해집니다.
</p>""",
        'en': r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This sequence problem investigates an arithmetic sequence $\{a_n\}$ coupled with an alternating partial sum sequence $\{b_n\}$. The key strategy is separating even and odd indexed terms to exploit pairwise telescoping cancellations.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Determine the common difference $d$</b><br>
  Let $\{a_n\}$ have first term $a_1$ and common difference $d$.<br>
  By definition, $b_2 = a_1 - a_2 = -d$. Given $b_2 = -2$:<br>
  $$-d = -2 \implies d = 2$$
  <br>
  <b>Step 2: Find $a_1$ using the condition $b_3 + b_7 = 0$</b><br>
  Group consecutive pairs $(a_{2k-1} - a_{2k}) = -d = -2$:<br>
  • $b_3 = (a_1 - a_2) + a_3 = -d + a_3 = a_3 - 2$<br>
  • $b_7 = (a_1 - a_2) + (a_3 - a_4) + (a_5 - a_6) + a_7 = -3d + a_7 = a_7 - 6$<br>
  Substitute into $b_3 + b_7 = 0$:<br>
  $$(a_3 - 2) + (a_7 - 6) = a_3 + a_7 - 8 = 0$$<br>
  Using $a_3 = a_1 + 4$ and $a_7 = a_1 + 12$:<br>
  $$(a_1 + 4) + (a_1 + 12) - 8 = 2a_1 + 8 = 0 \implies a_1 = -4$$<br>
  Thus, $a_n = -4 + 2(n-1) = 2n - 6$.
  <br><br>
  <b>Step 3: Sum the terms from $n = 1$ to $9$</b><br>
  Split into even and odd indices:<br>
  • Even terms ($b_{2k} = -kd = -2k$ for $k=1,2,3,4$):<br>
  $$\sum_{k=1}^4 b_{2k} = -2(1 + 2 + 3 + 4) = -20$$<br>
  • Odd terms ($b_{2k-1} = 2k - 6$ for $k=1,2,3,4,5$):<br>
  $$\sum_{k=1}^5 b_{2k-1} = (-4) + (-2) + 0 + 2 + 4 = 0$$<br>
  Summing both components:<br>
  $$\sum_{n=1}^9 b_n = (-20) + 0 = -20$$
</p>

<h4>✨ [Conclusion & Key Takeaways]</h4>
<p>
  The total sum $\sum_{n=1}^9 b_n$ is $-20$.<br>
  Therefore, the correct answer is <b>Option ②</b>.<br>
  💡 <b>Strategy Tip</b>: Pairing alternating signs as $-d$ reduces alternating series to simple arithmetic steps, revealing useful symmetries around zero.
</p>"""
    },
    'c30913': {
        'ko': r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>이차함수의 축 대칭성과 정적분과 넓이의 기하학적 관계</b>를 묻습니다. 곡선과 선분으로 둘러싸인 넓이의 대칭적 분할을 정적분 $\int_0^k f(x)dx = 0$ 이라는 단일 등식으로 전환하여 빠르게 상수를 결정하는 능력이 핵심입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 대칭성에 의한 넓이 관계 분석</b><br>
  주어진 이차함수 그래프는 축에 대하여 좌우 대칭입니다.<br>
  곡선 $y=f(x)$와 선분 $PQ$로 둘러싸인 윗부분의 총넓이를 $A$라 할 때, 대칭축을 기준으로 양분되므로 $x \ge 0$인 오른쪽 반쪽의 넓이는 $\frac{A}{2}$ 입니다.<br>
  문제의 조건에서 $A = 2B$ 이므로 양변을 2로 나누면 다음을 얻습니다.<br>
  $$\frac{A}{2} = B$$
  <br>
  <b>2단계: 넓이 상쇄와 정적분 값의 관계 파악</b><br>
  $x \ge 0$에서 $x$축 위쪽 영역의 넓이가 $\frac{A}{2}$이고, 곡선이 $x$축 아래로 내려간 영역의 넓이가 $B$입니다.<br>
  $\frac{A}{2} = B$ 이므로 $x=0$부터 $x=k$까지 정적분하면 $x$축 위쪽 영역의 양(+)의 적분값과 $x$축 아래쪽 영역의 음(-)의 적분값이 정확히 상쇄되어 합이 $0$이 됩니다!<br>
  $$\int_0^k (-x^2 + 2x + 6)dx = 0$$
  <br>
  <b>3단계: 정적분 계산 및 $k$의 값 결정</b><br>
  부정적분을 구하여 위끝 $k$와 아래끝 $0$을 대입합니다.<br>
  $$\left[ -\frac{1}{3}x^3 + x^2 + 6x \right]_0^k = -\frac{1}{3}k^3 + k^2 + 6k = 0$$
  양변에 $-3$을 곱하고 공통인수 $k$로 묶으면 ($k > 4$이므로 $k \ne 0$):<br>
  $$k^3 - 3k^2 - 18k = 0 \implies k(k^2 - 3k - 18) = 0$$
  이차식을 인수분해하면 $(k-6)(k+3) = 0$ 입니다.<br>
  조건 $k > 4$에 의해 가능한 값은 $k = 6$ 입니다.
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  상수 $k$의 값은 $6$ 입니다.<br>
  따라서 올바른 정답은 <b>④번</b>입니다.<br>
  💡 <b>실전 팁</b>: 두 영역의 넓이가 같다는 조건(위쪽 넓이 = 아래쪽 넓이)이 나오면 각 넓이를 따로 적분하여 비교하기보다, 시작점부터 끝점까지의 **정적분 결과가 0**이라는 사실($\int_a^b f(x)dx = 0$)을 이용하는 것이 가장 빠른 풀이법입니다.
</p>""",
        'en': r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates the geometric relationship between <b>area and definite integrals under parabolic symmetry</b>. The key insight is translating the area equality ($A/2 = B$) into a net zero definite integral over $[0, k]$.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Exploit symmetry to analyze regional areas</b><br>
  Due to the reflectional symmetry of the parabola across the vertical axis, the upper region of area $A$ bounded by the parabola and horizontal segment $PQ$ is divided equally: each half has area $\frac{A}{2}$.<br>
  Given $A = 2B$, dividing by 2 yields:<br>
  $$\frac{A}{2} = B$$
  <br>
  <b>Step 2: Translate equal opposing areas into a zero definite integral</b><br>
  For $x \ge 0$, the area above the $x$-axis is $\frac{A}{2}$ and the area below the $x$-axis from the root up to $x=k$ is $B$.<br>
  Because $\frac{A}{2} = B$, the positive integral above the axis cancels the negative integral below the axis exactly:<br>
  $$\int_0^k (-x^2 + 2x + 6)dx = 0$$
  <br>
  <b>Step 3: Evaluate the integral and solve for $k$</b><br>
  $$\left[ -\frac{1}{3}x^3 + x^2 + 6x \right]_0^k = -\frac{1}{3}k^3 + k^2 + 6k = 0$$<br>
  Multiply by $-3$ and factor out $k$ (since $k > 4$, $k \ne 0$):<br>
  $$k^2 - 3k - 18 = 0 \implies (k-6)(k+3) = 0$$<br>
  Given the constraint $k > 4$, we conclude $k = 6$.
</p>

<h4>✨ [Conclusion & Key Takeaways]</h4>
<p>
  The required value of constant $k$ is $6$.<br>
  Thus, the correct answer is <b>Option ④</b>.<br>
  💡 <b>Strategy Tip</b>: When equal positive and negative areas meet on an interval, setting the definite integral over the entire range to $0$ bypasses root-finding and piece-by-piece area integration completely.
</p>"""
    },
    'c30914': {
        'ko': r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>지수함수와 로그함수의 역함수 대칭성($y=x$)</b>, 직선의 기울기와 점과 점 사이의 거리 공식, 그리고 원의 대칭성을 융합한 고난도 해석기하·대수 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 두 점 $A_n, B_n$의 좌표 및 기울기·거리 연립</b><br>
  지수함수 $y=2^x$ 위의 두 점을 $A_n(a_n, 2^{a_n})$, $B_n(b_n, 2^{b_n})$ ($a_n < b_n$)이라 합시다.<br>
  조건 (가)에 의해 두 점을 지나는 직선의 기울기는 $3$입니다.<br>
  $$\frac{2^{b_n} - 2^{a_n}}{b_n - a_n} = 3 \implies 2^{b_n} - 2^{a_n} = 3(b_n - a_n) \quad \cdots\cdots \text{㉠}$$
  조건 (나)에 의해 두 점 사이의 거리가 $n\sqrt{10}$입니다.<br>
  $$(b_n - a_n)^2 + (2^{b_n} - 2^{a_n})^2 = (n\sqrt{10})^2 = 10n^2 \quad \cdots\cdots \text{㉡}$$
  ㉠을 ㉡에 대입하면:<br>
  $$(b_n - a_n)^2 + [3(b_n - a_n)]^2 = 10(b_n - a_n)^2 = 10n^2 \implies (b_n - a_n)^2 = n^2$$
  $b_n > a_n$ 이므로 $b_n - a_n = n$ 입니다.<br>
  따라서 $a_n = b_n - n$ 입니다.
  <br><br>
  <b>2단계: $2^{b_n}$의 일반식 유도</b><br>
  $a_n = b_n - n$ 을 식 ㉠에 대입합니다.<br>
  $$2^{b_n} - 2^{b_n - n} = 3n \implies 2^{b_n}(1 - 2^{-n}) = 3n$$
  $$2^{b_n} = \frac{3n}{1 - 2^{-n}} = \frac{3n \cdot 2^n}{2^n - 1}$$
  <br>
  <b>3단계: 원의 대칭성과 로그함수와의 교점 $x_n$ 도출</b><br>
  원의 중심이 직선 $y=x$ 위에 있으므로 원은 직선 $y=x$에 대하여 완벽히 대칭입니다.<br>
  지수함수 $y=2^x$와 로그함수 $y=\log_2 x$ 역시 $y=x$에 대하여 대칭인 역함수 관계입니다.<br>
  따라서 원과 로그함수의 교점은 원과 지수함수의 교점인 $A_n, B_n$을 직선 $y=x$에 대칭이동한 점 $(2^{a_n}, a_n)$과 $(2^{b_n}, b_n)$입니다.<br>
  이 두 점의 $x$좌표 중 더 큰 값 $x_n$은 바로 $2^{b_n}$ 입니다!<br>
  $$x_n = 2^{b_n} = \frac{3n \cdot 2^n}{2^n - 1}$$
  <br>
  <b>4단계: $x_1 + x_2 + x_3$ 계산</b><br>
  $n=1, 2, 3$을 대입합니다.<br>
  • $x_1 = \frac{3(1) \cdot 2^1}{2^1 - 1} = \frac{6}{1} = 6$<br>
  • $x_2 = \frac{3(2) \cdot 2^2}{2^2 - 1} = \frac{24}{3} = 8$<br>
  • $x_3 = \frac{3(3) \cdot 2^3}{2^3 - 1} = \frac{72}{7}$<br>
  구하는 합은:<br>
  $$x_1 + x_2 + x_3 = 6 + 8 + \frac{72}{7} = 14 + \frac{72}{7} = \frac{98 + 72}{7} = \frac{170}{7}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  세 값의 합은 $\frac{170}{7}$ 입니다.<br>
  따라서 올바른 정답은 <b>⑤번</b>입니다.<br>
  💡 <b>실전 팁</b>: 중심이 $y=x$ 위에 있는 원과 역함수 관계인 두 곡선($2^x, \log_2 x$)의 교점은 반드시 $y=x$에 대칭입니다. 따라서 복잡한 원의 방정식을 세울 필요 없이 $(x, y) \leftrightarrow (y, x)$ 대칭 원리만으로 $x_n = 2^{b_n}$을 즉시 간파하는 것이 핵심입니다.
</p>""",
        'en': r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem synthesizes the <b>inverse symmetry of exponential ($2^x$) and logarithmic ($\log_2 x$) functions across $y=x$</b>, geometric line properties (slope and distance), and circle reflectional invariance.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Set up slope and distance equations on $y=2^x$</b><br>
  Let the points on $y=2^x$ be $A_n(a_n, 2^{a_n})$ and $B_n(b_n, 2^{b_n})$ with $a_n < b_n$.<br>
  • Slope $= 3$ gives:<br>
  $$\frac{2^{b_n} - 2^{a_n}}{b_n - a_n} = 3 \implies 2^{b_n} - 2^{a_n} = 3(b_n - a_n) \quad \cdots\cdots (1)$$<br>
  • Distance $= n\sqrt{10}$ gives:<br>
  $$(b_n - a_n)^2 + [3(b_n - a_n)]^2 = 10(b_n - a_n)^2 = 10n^2 \implies b_n - a_n = n$$<br>
  Thus, $a_n = b_n - n$.
  <br><br>
  <b>Step 2: Solve for $2^{b_n}$</b><br>
  Substitute $a_n = b_n - n$ into equation (1):<br>
  $$2^{b_n} - 2^{b_n - n} = 3n \implies 2^{b_n}(1 - 2^{-n}) = 3n \implies 2^{b_n} = \frac{3n \cdot 2^n}{2^n - 1}$$
  <br>
  <b>Step 3: Exploit circle and inverse symmetry across $y = x$</b><br>
  Since the center of the circle lies on $y=x$, the circle is symmetric with respect to $y=x$.<br>
  Because $y = \log_2 x$ is the reflection of $y = 2^x$ across $y = x$, the intersection points of the circle with $y = \log_2 x$ are precisely the reflections $(2^{a_n}, a_n)$ and $(2^{b_n}, b_n)$.<br>
  The larger $x$-coordinate of these two points is $x_n = 2^{b_n}$:<br>
  $$x_n = \frac{3n \cdot 2^n}{2^n - 1}$$
  <br>
  <b>Step 4: Compute the sum $x_1 + x_2 + x_3$</b><br>
  • $x_1 = \frac{3(1)(2)}{1} = 6$<br>
  • $x_2 = \frac{3(2)(4)}{3} = 8$<br>
  • $x_3 = \frac{3(3)(8)}{7} = \frac{72}{7}$<br>
  Summing:<br>
  $$x_1 + x_2 + x_3 = 14 + \frac{72}{7} = \frac{170}{7}$$
</p>

<h4>✨ [Conclusion & Key Takeaways]</h4>
<p>
  The sum of the three values is $\frac{170}{7}$.<br>
  Therefore, the correct option is <b>Option ⑤</b>.<br>
  💡 <b>Strategy Tip</b>: Symmetry across $y=x$ allows direct coordinate swapping $(x, y) \mapsto (y, x)$ without ever constructing the explicit algebraic circle equation.
</p>"""
    },
    'c30915': {
        'ko': r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>정적분으로 정의된 함수의 양변 미분</b>과 <b>곱의 미분법의 역연산(부정적분)</b>을 결합하여 미지의 다항함수 $g(x)$를 특정하고 정적분 값을 계산하는 고난도 해석학 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 조건 (가)의 양변을 $x$에 대하여 미분</b><br>
  주어진 조건 $\int_0^x \{t f(t) + t g(t)\}dt = 3x^4 + 8x^3 - 3x^2$ 의 양변을 $x$에 대하여 미분합니다.<br>
  미적분학의 기본정리에 의해 좌변의 도함수는 피적분함수에 $x$를 대입한 $x f(x) + x g(x)$ 입니다.<br>
  $$x f(x) + x g(x) = 12x^3 + 24x^2 - 6x$$
  양변을 $x$로 나누면 ($x \ne 0$에서 성립하며, 다항함수의 연속성에 의해 모든 실수에서 성립):<br>
  $$f(x) + g(x) = 12x^2 + 24x - 6 \quad \cdots\cdots \text{㉠}$$
  <br>
  <b>2단계: 조건 (나) 대입 및 곱의 미분법 역연산</b><br>
  조건 (나)에서 $f(x) = x g'(x)$ 이므로 이를 식 ㉠에 대입합니다.<br>
  $$x g'(x) + g(x) = 12x^2 + 24x - 6$$
  좌변의 $x g'(x) + g(x)$는 바로 곱의 미분법 $\{x g(x)\}'$의 전개식입니다!<br>
  $$\{x g(x)\}' = 12x^2 + 24x - 6$$
  양변을 부정적분하면 다음과 같습니다.<br>
  $$x g(x) = \int (12x^2 + 24x - 6)dx = 4x^3 + 12x^2 - 6x + C$$
  $g(x)$가 다항함수이므로 $x=0$을 대입할 때 좌변이 $0$이어야 하므로 적분상수 $C = 0$ 입니다.<br>
  따라서 양변을 $x$로 나누면 $g(x)$가 완전히 결정됩니다.<br>
  $$g(x) = 4x^2 + 12x - 6$$
  <br>
  <b>3단계: 정적분 $\int_0^3 g(x)dx$ 계산</b><br>
  구하는 정적분을 계산합니다.<br>
  $$\int_0^3 (4x^2 + 12x - 6)dx = \left[ \frac{4}{3}x^3 + 6x^2 - 6x \right]_0^3$$
  $$= \frac{4}{3}(27) + 6(9) - 6(3) = 36 + 54 - 18 = 72$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  계산된 정적분 값은 $72$ 입니다.<br>
  따라서 올바른 정답은 <b>①번</b>입니다.<br>
  💡 <b>실전 팁</b>: 수능에서 $x g'(x) + g(x)$ 꼴이 보이면 즉시 **곱의 미분법 $\{x g(x)\}'$**으로 한 덩어리로 묶어 적분하는 패턴은 빈출 핵심 킬러 테크닉입니다.
</p>""",
        'en': r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates differentiation of integral-defined functions and recognizes the reverse product rule pattern $\{x g(x)\}' = x g'(x) + g(x)$ to reconstruct a polynomial function.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Differentiate condition (A) with respect to $x$</b><br>
  Differentiating $\int_0^x \{t f(t) + t g(t)\}dt = 3x^4 + 8x^3 - 3x^2$ via the Fundamental Theorem of Calculus:<br>
  $$x f(x) + x g(x) = 12x^3 + 24x^2 - 6x$$<br>
  Dividing both sides by $x$ (valid everywhere by polynomial continuity):<br>
  $$f(x) + g(x) = 12x^2 + 24x - 6 \quad \cdots\cdots (1)$$
  <br>
  <b>Step 2: Recognize the reverse product rule</b><br>
  Condition (B) states $f(x) = x g'(x)$. Substituting into (1):<br>
  $$x g'(x) + g(x) = 12x^2 + 24x - 6$$<br>
  Observe that the left-hand side is the derivative of the product $x g(x)$:<br>
  $$\{x g(x)\}' = 12x^2 + 24x - 6$$<br>
  Integrating both sides:<br>
  $$x g(x) = 4x^3 + 12x^2 - 6x + C$$<br>
  Evaluating at $x = 0$ yields $0 = C \implies C = 0$. Dividing by $x$ gives:<br>
  $$g(x) = 4x^2 + 12x - 6$$
  <br>
  <b>Step 3: Evaluate the definite integral over $[0, 3]$</b><br>
  $$\int_0^3 (4x^2 + 12x - 6)dx = \left[ \frac{4}{3}x^3 + 6x^2 - 6x \right]_0^3$$<br>
  $$= \frac{4}{3}(27) + 6(9) - 6(3) = 36 + 54 - 18 = 72$$
</p>

<h4>✨ [Conclusion & Key Takeaways]</h4>
<p>
  The value of the integral is $72$.<br>
  Hence, the correct answer is <b>Option ①</b>.<br>
  💡 <b>Strategy Tip</b>: Spotting the identity $\frac{d}{dx}[x g(x)] = x g'(x) + g(x)$ instantly unlocks anti-differentiation without having to guess polynomial degrees or undetermined coefficients.
</p>"""
    },
    'c30916': {
        'ko': r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>로그방정식의 해법</b>에서 가장 중요한 <b>진수 조건</b>을 확인하고, 밑 변환 공식을 통해 밑을 3으로 통일한 후 진수의 곱셈을 이용하여 이차방정식을 해결하는 단답형 문제입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 필수 진수 조건 확인</b><br>
  로그가 정의되기 위해서는 모든 진수가 양수여야 합니다.<br>
  • $x + 2 > 0 \implies x > -2$<br>
  • $x - 4 > 0 \implies x > 4$<br>
  두 조건의 공통 범위는 $x > 4$ 입니다.
  <br><br>
  <b>2단계: 밑을 3으로 통일하고 하나의 로그로 합성</b><br>
  $\frac{1}{3} = 3^{-1}$ 이므로 로그의 밑 변환 성질에 의해 다음과 같습니다.<br>
  $$\log_{\frac{1}{3}}(x-4) = \log_{3^{-1}}(x-4) = -\log_3(x-4)$$
  주어진 방정식에 대입하면 마이너스가 플러스로 바뀝니다.<br>
  $$\log_3(x+2) - \{-\log_3(x-4)\} = 3$$
  $$\log_3(x+2) + \log_3(x-4) = 3$$
  로그의 덧셈 성질 $\log_a M + \log_a N = \log_a(MN)$을 적용합니다.<br>
  $$\log_3\{(x+2)(x-4)\} = 3$$
  <br>
  <b>3단계: 이차방정식 풀이 및 해 선별</b><br>
  로그의 정의에 의해 진수는 $3^3 = 27$ 입니다.<br>
  $$(x+2)(x-4) = 27 \implies x^2 - 2x - 8 = 27 \implies x^2 - 2x - 35 = 0$$
  인수분해하면 $(x-7)(x+5) = 0$ 이므로 $x = 7$ 또는 $x = -5$ 입니다.<br>
  1단계의 진수 조건 $x > 4$를 만족해야 하므로 $x = 7$ 만이 유일한 해입니다.
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  구하는 방정식의 해는 $7$ 입니다.<br>
  따라서 올바른 정답은 <b>7</b> 입니다.<br>
  💡 <b>실전 팁</b>: 로그방정식에서 진수 조건을 사전에 적어두지 않으면 무연근(이 문제에서는 $-5$)을 답으로 적어 감점되는 치명적 실수가 발생할 수 있습니다. 항상 **진수 조건($>0$)을 풀이 맨 첫 줄에 적는 습관**을 들이십시오.
</p>""",
        'en': r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem verifies the ability to solve a <b>logarithmic equation</b>, emphasizing domain constraints (argument $> 0$) and base unification via exponent inversion ($\log_{3^{-1}} u = -\log_3 u$).</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Determine the domain constraints (arguments $> 0$)</b><br>
  For real logarithmic expressions, arguments must be strictly positive:<br>
  • $x + 2 > 0 \implies x > -2$<br>
  • $x - 4 > 0 \implies x > 4$<br>
  Their intersection requires $x > 4$.
  <br><br>
  <b>Step 2: Unify bases to $3$ and condense</b><br>
  Using base property $\log_{3^{-1}}(x-4) = -\log_3(x-4)$:<br>
  $$\log_3(x+2) - [-\log_3(x-4)] = 3 \implies \log_3(x+2) + \log_3(x-4) = 3$$<br>
  Applying the product rule of logarithms:<br>
  $$\log_3[(x+2)(x-4)] = 3 \implies (x+2)(x-4) = 3^3 = 27$$
  <br>
  <b>Step 3: Solve the quadratic equation and verify constraints</b><br>
  $$x^2 - 2x - 8 = 27 \implies x^2 - 2x - 35 = 0 \implies (x-7)(x+5) = 0$$<br>
  The algebraic solutions are $x = 7$ and $x = -5$.<br>
  Enforcing the domain restriction $x > 4$, the extraneous root $-5$ is rejected, leaving $x = 7$.
</p>

<h4>✨ [Conclusion & Key Takeaways]</h4>
<p>
  The final solution is $7$.<br>
  Therefore, the answer is <b>7</b>.<br>
  💡 <b>Strategy Tip</b>: Always state the domain restrictions ($x > 4$) before converting to algebraic form to reliably weed out extraneous roots.
</p>"""
    },
    'c30917': {
        'ko': r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>다항함수의 부정적분</b>을 구하고, 주어진 초기조건(함숫값)을 이용하여 적분상수 $C$를 결정한 뒤 특정 점에서의 함숫값을 계산하는 기본 연산 문제입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 부정적분을 통한 일반 형태 구하기</b><br>
  $f'(x) = 6x^2 + 2x + 1$ 에 대하여 각 항의 거듭제곱 적분 공식 $\int x^n dx = \frac{1}{n+1}x^{n+1} + C$를 적용합니다.<br>
  $$f(x) = \int (6x^2 + 2x + 1)dx = 6 \cdot \frac{1}{3}x^3 + 2 \cdot \frac{1}{2}x^2 + x + C = 2x^3 + x^2 + x + C$$
  (단, $C$는 적분상수)
  <br><br>
  <b>2단계: 초기조건을 통한 적분상수 $C$ 결정</b><br>
  주어진 조건 $f(0) = 1$ 을 대입합니다.<br>
  $$f(0) = 2(0)^3 + 0^2 + 0 + C = C = 1$$
  따라서 완성된 함수 $f(x)$는 다음과 같습니다.<br>
  $$f(x) = 2x^3 + x^2 + x + 1$$
  <br>
  <b>3단계: $f(1)$ 계산</b><br>
  $x = 1$을 대입합니다.<br>
  $$f(1) = 2(1)^3 + (1)^2 + (1) + 1 = 2 + 1 + 1 + 1 = 5$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  구하는 값 $f(1)$은 $5$ 입니다.<br>
  따라서 올바른 정답은 <b>5</b> 입니다.<br>
  💡 <b>실전 팁</b>: $f(1) - f(0) = \int_0^1 f'(x)dx$ 임을 이용하면 적분상수 $C$를 따로 구하지 않고도 $f(1) = f(0) + \int_0^1 (6x^2+2x+1)dx = 1 + (2+1+1) = 5$로도 즉각 해결할 수 있습니다.
</p>""",
        'en': r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem verifies procedural fluency with <b>indefinite integration of polynomials</b> and determining the constant of integration from an initial boundary condition.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Compute the antiderivative of $f'(x)$</b><br>
  Given $f'(x) = 6x^2 + 2x + 1$, apply power-rule integration:<br>
  $$f(x) = \int (6x^2 + 2x + 1)dx = 2x^3 + x^2 + x + C$$
  <br>
  <b>Step 2: Determine integration constant $C$</b><br>
  Given initial condition $f(0) = 1$:<br>
  $$f(0) = C = 1 \implies f(x) = 2x^3 + x^2 + x + 1$$
  <br>
  <b>Step 3: Evaluate $f(1)$</b><br>
  $$f(1) = 2(1)^3 + 1^2 + 1 + 1 = 5$$
</p>

<h4>✨ [Conclusion & Key Takeaways]</h4>
<p>
  The value of $f(1)$ is $5$.<br>
  Hence, the answer is <b>5</b>.<br>
  💡 <b>Strategy Tip</b>: Alternatively, evaluate via the Fundamental Theorem of Calculus: $f(1) = f(0) + \int_0^1 f'(x)dx = 1 + (2+1+1) = 5$.
</p>"""
    },
    'c30918': {
        'ko': r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>시그마 기호($\Sigma$)의 전개와 지표 맞추기(인덱스 변환)</b>를 활용하여, 두 수열의 합 식의 차를 통해 원하는 형태인 $\sum_{k=1}^{10} a_k$를 한 번에 유도해내는 대수적 조작 능력을 평가합니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 두 시그마 식을 나열하여 구조 파악</b><br>
  주어진 두 식을 각 항별로 펼쳐 전개합니다.<br>
  • 식 ㉠:<br>
  $$\sum_{k=1}^{10} k a_k = 1a_1 + 2a_2 + 3a_3 + 4a_4 + \cdots + 10a_{10} = 36$$<br>
  • 식 ㉡:<br>
  $$\sum_{k=1}^9 k a_{k+1} = 1a_2 + 2a_3 + 3a_4 + \cdots + 9a_{10} = 7$$
  <br>
  <b>2단계: 변변 뺄셈을 통한 각 항의 계수 통일</b><br>
  식 ㉠에서 식 ㉡을 변끼리 빼면 다음과 같은 놀라운 규칙이 나타납니다.<br>
  $$\left(\sum_{k=1}^{10} k a_k\right) - \left(\sum_{k=1}^9 k a_{k+1}\right)$$
  $$= 1a_1 + (2-1)a_2 + (3-2)a_3 + \cdots + (10-9)a_{10}$$
  $$= a_1 + a_2 + a_3 + \cdots + a_{10}$$
  이는 정확히 우리가 구하고자 하는 $\sum_{k=1}^{10} a_k$ 입니다!
  <br><br>
  <b>3단계: 최종 값 산출</b><br>
  두 우변의 값의 차를 계산합니다.<br>
  $$\sum_{k=1}^{10} a_k = 36 - 7 = 29$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  구하는 값은 $29$ 입니다.<br>
  따라서 올바른 정답은 <b>29</b> 입니다.<br>
  💡 <b>실전 팁</b>: 수열 $a_k$의 일반항을 억지로 구하려 하지 말고, 시그마의 전개 나열식을 상하로 나란히 배치해 빼보십시오. 계수 $k$와 $k-1$의 차가 항상 $1$이 되므로 목표하는 $\sum a_k$가 즉시 나타납니다.
</p>""",
        'en': r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates algebraic manipulation of <b>summation notation ($\Sigma$)</b> by expanding series and shifting indices to isolate $\sum_{k=1}^{10} a_k$ cleanly.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Expand both summations term-by-term</b><br>
  Writing out the terms explicitly:<br>
  • Equation (1):<br>
  $$\sum_{k=1}^{10} k a_k = a_1 + 2a_2 + 3a_3 + \cdots + 10a_{10} = 36$$<br>
  • Equation (2):<br>
  $$\sum_{k=1}^9 k a_{k+1} = a_2 + 2a_3 + 3a_4 + \cdots + 9a_{10} = 7$$
  <br>
  <b>Step 2: Subtract equation (2) from equation (1)</b><br>
  Subtracting term by term:<br>
  $$(a_1 + 2a_2 + 3a_3 + \dots + 10a_{10}) - (a_2 + 2a_3 + \dots + 9a_{10})$$<br>
  $$= a_1 + (2-1)a_2 + (3-2)a_3 + \dots + (10-9)a_{10}$$<br>
  $$= a_1 + a_2 + a_3 + \dots + a_{10} = \sum_{k=1}^{10} a_k$$
  <br>
  <b>Step 3: Compute the numerical difference</b><br>
  $$\sum_{k=1}^{10} a_k = 36 - 7 = 29$$
</p>

<h4>✨ [Conclusion & Key Takeaways]</h4>
<p>
  The evaluated sum is $29$.<br>
  Therefore, the answer is <b>29</b>.<br>
  💡 <b>Strategy Tip</b>: Expanding sigma notation horizontally and subtracting matching columns is often vastly faster than algebraic index re-indexing.
</p>"""
    },
    'c30919': {
        'ko': r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>삼차함수의 극대·극소 조건</b>($f'(x) = 0$)을 바탕으로 미정계수 $a, b$를 차례로 결정하고, 극댓값을 활용하여 계수의 합 $a+b$를 구하는 전형적인 다항함수 미분 문제입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 도함수 유도 및 극소 조건 적용</b><br>
  함수 $f(x) = x^3 + ax^2 - 9x + b$ 의 도함수는 다음과 같습니다.<br>
  $$f'(x) = 3x^2 + 2ax - 9$$
  함수 $f(x)$가 $x=1$에서 극소이므로 미분계수가 $0$이어야 합니다 ($f'(1) = 0$).<br>
  $$f'(1) = 3(1)^2 + 2a(1) - 9 = 2a - 6 = 0 \implies 2a = 6 \implies a = 3$$
  <br>
  <b>2단계: $f'(x) = 0$의 두 근을 통한 극대점의 위치 파악</b><br>
  $a=3$을 도함수에 대입하여 인수분해합니다.<br>
  $$f'(x) = 3x^2 + 6x - 9 = 3(x^2 + 2x - 3) = 3(x+3)(x-1) = 0$$
  최고차항 계수가 $1>0$인 삼차함수의 도함수가 아래로 볼록한 이차함수이므로,<br>
  $x = -3$에서 도함수의 부호가 양에서 음으로 바뀌어 <b>극대</b>를 갖고,<br>
  $x = 1$에서 도함수의 부호가 음에서 양으로 바뀌어 <b>극소</b>를 갖습니다.
  <br><br>
  <b>3단계: 극댓값 28을 이용한 $b$ 결정 및 $a+b$ 계산</b><br>
  극댓값이 $28$이므로 $f(-3) = 28$ 입니다.<br>
  $$f(-3) = (-3)^3 + 3(-3)^2 - 9(-3) + b = -27 + 27 + 27 + b = 27 + b = 28$$
  따라서 $b = 1$ 입니다.<br>
  구하고자 하는 두 계수의 합은 다음과 같습니다.<br>
  $$a + b = 3 + 1 = 4$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  구하는 값 $a+b$는 $4$ 입니다.<br>
  따라서 올바른 정답은 <b>4</b> 입니다.<br>
  💡 <b>실전 팁</b>: 삼차함수에서 극대와 극소의 $x$좌표는 도함수의 두 실근입니다. $x=1$이 극소점이면 더 작은 근인 $x=-3$이 반드시 극대점이 됨을 증감표 없이 개형으로 즉시 판단하십시오.
</p>""",
        'en': r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem verifies ability to determine polynomial coefficients using <b>local extrema conditions ($f'(x) = 0$)</b> of a cubic function and calculating function values at local maximum points.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Differentiate and apply the local minimum condition</b><br>
  For $f(x) = x^3 + ax^2 - 9x + b$:<br>
  $$f'(x) = 3x^2 + 2ax - 9$$<br>
  Since $f(x)$ attains a local minimum at $x = 1$, we have $f'(1) = 0$:<br>
  $$f'(1) = 3(1)^2 + 2a(1) - 9 = 2a - 6 = 0 \implies a = 3$$
  <br>
  <b>Step 2: Factor $f'(x)$ to find the local maximum location</b><br>
  Substituting $a = 3$:<br>
  $$f'(x) = 3x^2 + 6x - 9 = 3(x+3)(x-1) = 0$$<br>
  For a cubic with positive leading coefficient, the graph transitions from increasing to decreasing at the smaller critical value $x = -3$ (local maximum), and from decreasing to increasing at $x = 1$ (local minimum).
  <br><br>
  <b>Step 3: Solve for $b$ using the maximum value $28$</b><br>
  $$f(-3) = (-3)^3 + 3(-3)^2 - 9(-3) + b = 27 + b = 28 \implies b = 1$$<br>
  Then evaluate the required sum:<br>
  $$a + b = 3 + 1 = 4$$
</p>

<h4>✨ [Conclusion & Key Takeaways]</h4>
<p>
  The final value $a+b$ is $4$.<br>
  Hence, the answer is <b>4</b>.<br>
  💡 <b>Strategy Tip</b>: A cubic polynomial's local maximum always precedes its local minimum when the leading coefficient is positive.
</p>"""
    },
    'c30920': {
        'ko': r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>구간별 삼각함수의 그래프</b>를 정확히 작도하고, 수평선 $y=f(t)$와의 교점의 개수가 3개가 되는 모든 $t$의 값을 찾아 합을 구하는 기하학적·해석학적 고난도 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 구간별 함수 $y=f(x)$의 그래프 분석</b><br>
  정의역 $[0, 2\pi]$에서 함수 $f(x)$의 개형을 구간별로 조사합니다.<br>
  • $0 \le x < \pi$ 일 때: $f(x) = \sin x - 1$<br>
  이 구간에서 $\sin x \ge 0$이므로 $-1 \le f(x) \le 0$ 입니다.<br>
  - $x = 0$ 일 때 $f(0) = -1$<br>
  - $x = \frac{\pi}{2}$ 일 때 최댓값 $f(\frac{\pi}{2}) = 0$<br>
  - $x \to \pi^-$ 일 때 $f(x) \to -1$<br>
  • $\pi \le x \le 2\pi$ 일 때: $f(x) = -\sqrt{2}\sin x - 1$<br>
  이 구간에서 $\sin x \le 0$이므로 $-\sqrt{2}\sin x \ge 0$ 입니다.<br>
  - $x = \pi$ 일 때 $f(\pi) = -1$<br>
  - $x = \frac{3\pi}{2}$ 일 때 최댓값 $f(\frac{3\pi}{2}) = -\sqrt{2}(-1) - 1 = \sqrt{2} - 1 \approx 0.414$<br>
  - $x = 2\pi$ 일 때 $f(2\pi) = -1$
  <br><br>
  <b>2단계: 교점 개수가 3개가 되는 수평선 높이 판별</b><br>
  직선 $y = f(t)$와 곡선 $y=f(x)$의 교점 개수가 3개가 되는 $y$-값은 그래프 분석 결과 오직 두 가지입니다.<br>
  (1) $y = -1$: 양쪽 구간의 시작/끝점이 만나는 높이로 교점 3개 발생 ($x = 0, \pi, 2\pi$)<br>
  (2) $y = 0$: 첫 번째 구간의 극댓값이자 두 번째 구간의 곡선과 2번 만나는 높이로 교점 3개 발생 ($x = \frac{\pi}{2}$에서 접하고, $\pi < x < 2\pi$에서 2개 만남)
  <br><br>
  <b>3단계: 각 경우에 해당하는 모든 $t$의 값 도출</b><br>
  • <b>Case 1: $f(t) = -1$</b><br>
  정의역 $[0, 2\pi]$에서 $f(t) = -1$이 되는 $t$는:<br>
  $$t = 0, \quad t = \pi, \quad t = 2\pi$$
  • <b>Case 2: $f(t) = 0$</b><br>
  - $0 \le t < \pi$에서: $\sin t - 1 = 0 \implies \sin t = 1 \implies t = \frac{\pi}{2}$<br>
  - $\pi \le t \le 2\pi$에서: $-\sqrt{2}\sin t - 1 = 0 \implies \sin t = -\frac{1}{\sqrt{2}} = -\frac{\sqrt{2}}{2}$<br>
  이 구간에서 $\sin$ 값이 $-\frac{\sqrt{2}}{2}$가 되는 두 각은 제3, 제4사분면의 각입니다.<br>
  $$t = \pi + \frac{\pi}{4} = \frac{5\pi}{4}, \quad t = 2\pi - \frac{\pi}{4} = \frac{7\pi}{4}$$
  <br>
  <b>4단계: 모든 $t$의 합 및 $p+q$ 계산</b><br>
  구한 모든 $t$의 값을 합산합니다.<br>
  $$\text{합} = (0 + \pi + 2\pi) + \frac{\pi}{2} + \left(\frac{5\pi}{4} + \frac{7\pi}{4}\right)$$
  $$= 3\pi + \frac{\pi}{2} + 3\pi = 6\pi + \frac{\pi}{2} = \frac{13\pi}{2}$$<br>
  따라서 $p = 2, q = 13$ 이며 두 자연수는 서로소입니다.<br>
  $$p + q = 2 + 13 = 15$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  최종 구하는 값 $p+q$는 $15$ 입니다.<br>
  따라서 올바른 정답은 <b>15</b> 입니다.<br>
  💡 <b>실전 팁</b>: 수평선 $y = c$와의 교점 개수 문제는 그래프의 **극값(접선 기울기 0)**과 **경계값(구간 연결점)**에서 개수 변화가 일어납니다. 극댓값 $y=0$과 경계 최솟값 $y=-1$을 빠르게 특정하면 실근의 대칭성을 이용해 합을 신속히 구할 수 있습니다.
</p>""",
        'en': r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem analyzes the graph of a <b>piecewise sinusoidal function</b>, identifying the exact horizontal levels $y = f(t)$ where the equation $f(x) = f(t)$ produces exactly three distinct real solutions, and summing all valid values of $t$.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Sketch and analyze $y = f(x)$ over $[0, 2\pi]$</b><br>
  • Interval $[0, \pi)$: $f(x) = \sin x - 1$.<br>
  Starts at $(0, -1)$, peaks at local maximum $(\frac{\pi}{2}, 0)$, and approaches $(-1)$ as $x \to \pi^-$.<br>
  • Interval $[\pi, 2\pi]$: $f(x) = -\sqrt{2}\sin x - 1$.<br>
  Starts at $(\pi, -1)$, reaches maximum at $x = \frac{3\pi}{2}$ where $f(\frac{3\pi}{2}) = \sqrt{2}-1 \approx 0.414$, and ends at $(2\pi, -1)$.
  <br><br>
  <b>Step 2: Identify horizontal levels yielding exactly 3 intersections</b><br>
  From the visual structure, a horizontal line intersects the graph at exactly 3 points only when:<br>
  (1) $f(t) = -1$: The baseline containing the boundary points.<br>
  (2) $f(t) = 0$: Tangent to the first crest ($x = \pi/2$) and cutting through the second crest twice.
  <br><br>
  <b>Step 3: Solve for all corresponding values of $t$</b><br>
  • For $f(t) = -1$:<br>
  $$t = 0, \quad \pi, \quad 2\pi$$<br>
  • For $f(t) = 0$:<br>
  From $[0, \pi)$: $\sin t = 1 \implies t = \frac{\pi}{2}$.<br>
  From $[\pi, 2\pi]$: $-\sqrt{2}\sin t - 1 = 0 \implies \sin t = -\frac{\sqrt{2}}{2} \implies t = \frac{5\pi}{4}, \frac{7\pi}{4}$.
  <br><br>
  <b>Step 4: Compute the sum of all valid $t$ and evaluate $p + q$</b><br>
  $$\text{Sum} = (0 + \pi + 2\pi) + \frac{\pi}{2} + \left(\frac{5\pi}{4} + \frac{7\pi}{4}\right) = 3\pi + \frac{\pi}{2} + 3\pi = \frac{13\pi}{2}$$<br>
  Here $p = 2$ and $q = 13$, which are coprime positive integers.<br>
  $$p + q = 2 + 13 = 15$$
</p>

<h4>✨ [Conclusion & Key Takeaways]</h4>
<p>
  The final value $p+q$ is $15$.<br>
  Therefore, the answer is <b>15</b>.<br>
  💡 <b>Strategy Tip</b>: Critical horizontal intersection levels occur strictly at local extrema and piecewise stitching endpoints.
</p>"""
    }
}
