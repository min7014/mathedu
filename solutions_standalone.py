# solutions_standalone.py: Standalone problems pedagogical solutions
SOLUTIONS_STANDALONE = {
    'c1092101': {
        'ko': r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>원의 방정식에서 중심과 반지름을 파악</b>하고, <b>점과 직선 사이의 거리 공식</b>을 이용하여 원 위의 임의의 점에서 직선에 이르는 거리의 최댓값($d + r$) 조건을 만족시키는 미정계수 $k$를 결정하는 기하학적 기본 역량을 평가합니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 원의 중심과 반지름 파악</b><br>
  주어진 원의 방정식 $(x - 2)^2 + (y - 3)^2 = 9$ 에서<br>
  • 중심의 좌표: $C(2, 3)$<br>
  • 반지름의 길이: $r = \sqrt{9} = 3$
  <br><br>
  <b>2단계: 원의 중심과 직선 사이의 거리 $d$ 계산</b><br>
  직선의 방정식은 $3x - 4y + k = 0$ 입니다.<br>
  점 $(x_1, y_1)$과 직선 $ax+by+c=0$ 사이의 거리 공식 $d = \frac{|a x_1 + b y_1 + c|}{\sqrt{a^2 + b^2}}$을 적용합니다.<br>
  $$d = \frac{|3(2) - 4(3) + k|}{\sqrt{3^2 + (-4)^2}} = \frac{|6 - 12 + k|}{\sqrt{9 + 16}} = \frac{|k - 6|}{5}$$
  <br>
  <b>3단계: 거리의 최댓값 조건 적용</b><br>
  원 위의 점에서 직선에 이르는 거리의 최댓값은 중심에서 직선까지의 거리 $d$에 원의 반지름 $r$을 더한 값($d + r$)입니다.<br>
  문제의 조건에서 거리의 최댓값이 $7$이라 하였으므로:<br>
  $$d + r = 7 \implies d + 3 = 7 \implies d = 4$$
  <br>
  <b>4단계: $k$에 관한 방정식 풀이 및 양수 $k$ 결정</b><br>
  2단계의 식에 $d = 4$를 대입합니다.<br>
  $$\frac{|k - 6|}{5} = 4 \implies |k - 6| = 20$$
  절댓값을 풀면:<br>
  $$k - 6 = 20 \implies k = 26 \quad \text{또는} \quad k - 6 = -20 \implies k = -14$$
  문제에서 $k > 0$인 양수라 하였으므로 $k = 26$ 입니다.
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  구하는 양수 $k$의 값은 $26$ 입니다.<br>
  따라서 올바른 정답은 <b>26</b> 입니다.<br>
  💡 <b>실전 팁</b>: 원 위의 점에서 직선에 이르는 거리의 최댓값은 $d+r$, 최솟값은 $d-r$ (단, $d \ge r$)입니다. 항상 원의 중심 $C$를 기준으로 수선의 발을 내리는 기하학적 모델을 머릿속에 시각화하십시오.
</p>""",
        'en': r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem assesses the ability to identify a <b>circle's center and radius</b>, apply the <b>point-to-line distance formula</b>, and exploit the geometric extremum principle that maximum distance from a circle to a line equals $d + r$.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Extract circle parameters</b><br>
  From the circle equation $(x - 2)^2 + (y - 3)^2 = 9$:<br>
  • Center: $C(2, 3)$<br>
  • Radius: $r = \sqrt{9} = 3$
  <br><br>
  <b>Step 2: Calculate distance $d$ from the center to the line</b><br>
  Given the line $3x - 4y + k = 0$, apply the distance formula $d = \frac{|a x_0 + b y_0 + c|}{\sqrt{a^2 + b^2}}$:<br>
  $$d = \frac{|3(2) - 4(3) + k|}{\sqrt{3^2 + (-4)^2}} = \frac{|6 - 12 + k|}{\sqrt{25}} = \frac{|k - 6|}{5}$$
  <br>
  <b>Step 3: Enforce the maximum distance condition</b><br>
  The maximum distance from any point on the circle to the line is achieved along the normal passing through the center: $\text{Max} = d + r$.<br>
  Given that this maximum distance is $7$:<br>
  $$d + r = 7 \implies d + 3 = 7 \implies d = 4$$
  <br>
  <b>Step 4: Solve for positive parameter $k$</b><br>
  $$\frac{|k - 6|}{5} = 4 \implies |k - 6| = 20$$<br>
  This yields two algebraic roots:<br>
  $$k - 6 = 20 \implies k = 26 \quad \text{or} \quad k - 6 = -20 \implies k = -14$$<br>
  Given the condition $k > 0$, we select $k = 26$.
</p>

<h4>✨ [Conclusion & Key Takeaways]</h4>
<p>
  The required positive value of $k$ is $26$.<br>
  Therefore, the answer is <b>26</b>.<br>
  💡 <b>Strategy Tip</b>: The geometric extrema between a circle and a line are strictly governed by $d \pm r$. Never parameterize individual points on the circle with trigonometric coordinates when the center distance suffices.
</p>"""
    },
    'c2092102': {
        'ko': r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>삼각함수 $y = 2\sin(ax)$의 주기와 대칭성</b>을 이용하여 직선 $y=1$과의 교점의 좌표를 특정하고, 최솟값을 갖는 점 $C$와의 거리를 바탕으로 삼각형 $ABC$의 넓이 공식을 세워 양수 $a$의 값을 결정하는 문제입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 교점 $A, B$의 $x$좌표 구하기</b><br>
  곡선 $y = 2\sin(ax)$와 직선 $y = 1$의 교점을 구하기 위해 방정식을 세웁니다.<br>
  $$2\sin(ax) = 1 \implies \sin(ax) = \frac{1}{2}$$
  $0 \le x \le \frac{2\pi}{a}$ 이므로 각 $ax$의 범위는 한 주기인 $0 \le ax \le 2\pi$ 입니다.<br>
  이 범위에서 $\sin(ax) = \frac{1}{2}$을 만족시키는 두 각은 다음과 같습니다.<br>
  $$ax = \frac{\pi}{6} \quad \text{또는} \quad ax = \pi - \frac{\pi}{6} = \frac{5\pi}{6}$$
  양변을 $a>0$으로 나누면 두 교점의 $x$좌표는:<br>
  $$x_A = \frac{\pi}{6a}, \quad x_B = \frac{5\pi}{6a}$$
  <br>
  <b>2단계: 밑변 $\overline{AB}$의 길이 계산</b><br>
  두 점 $A, B$는 모두 직선 $y=1$ 위의 점이므로 밑변의 길이는 $x$좌표의 차입니다.<br>
  $$\overline{AB} = x_B - x_A = \frac{5\pi}{6a} - \frac{\pi}{6a} = \frac{4\pi}{6a} = \frac{2\pi}{3a}$$
  <br>
  <b>3단계: 점 $C$의 좌표 및 높이 $h$ 계산</b><br>
  함수 $f(x) = 2\sin(ax)$의 최솟값은 $-2$이므로 곡선 위의 점 중 $y$좌표가 최소인 점 $C$의 $y$좌표는 $-2$입니다.<br>
  직선 $y=1$에서 점 $C$까지의 수직 거리(삼각형의 높이) $h$는 다음과 같습니다.<br>
  $$h = 1 - (-2) = 3$$
  <br>
  <b>4단계: 삼각형의 넓이 공식 적용 및 $a$ 산출</b><br>
  삼각형 $ABC$의 넓이 $S$는 다음과 같습니다.<br>
  $$S = \frac{1}{2} \times \overline{AB} \times h = \frac{1}{2} \times \frac{2\pi}{3a} \times 3 = \frac{\pi}{a}$$
  문제의 조건에서 넓이가 $6$이라 하였으므로:<br>
  $$\frac{\pi}{a} = 6 \implies a = \frac{\pi}{6}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  구하는 양수 $a$의 값은 $\frac{\pi}{6}$ 입니다.<br>
  따라서 올바른 정답은 <b>$\frac{\pi}{6}$</b> 입니다.<br>
  💡 <b>실전 팁</b>: $\sin(ax) = 1/2$의 두 근의 차 $\frac{5\pi}{6a} - \frac{\pi}{6a} = \frac{2\pi}{3a}$는 주기가 $T = \frac{2\pi}{a}$일 때 한 주기의 $\frac{1}{3}$에 해당합니다. 주기 비율 관계를 활용하면 방정식 없이도 밑변 길이를 즉각 도출할 수 있습니다.
</p>""",
        'en': r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem analyzes the <b>periodicity and horizontal symmetry of $y = 2\sin(ax)$</b>. By locating intersection points on $y = 1$ and identifying the minimum point $C$, the triangle area formula directly solves for parameter $a$.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Find the $x$-coordinates of intersection points $A$ and $B$</b><br>
  Equating the curve to the horizontal line $y = 1$:<br>
  $$2\sin(ax) = 1 \implies \sin(ax) = \frac{1}{2}$$<br>
  Over the single fundamental period $0 \le x \le \frac{2\pi}{a}$, the argument spans $0 \le ax \le 2\pi$.<br>
  The solutions within this interval are:<br>
  $$ax = \frac{\pi}{6} \quad \text{and} \quad ax = \frac{5\pi}{6}$$<br>
  Dividing by $a > 0$ gives:<br>
  $$x_A = \frac{\pi}{6a}, \quad x_B = \frac{5\pi}{6a}$$
  <br>
  <b>Step 2: Determine base length $\overline{AB}$</b><br>
  Since $A$ and $B$ both lie on the horizontal line $y = 1$:<br>
  $$\overline{AB} = x_B - x_A = \frac{5\pi}{6a} - \frac{\pi}{6a} = \frac{2\pi}{3a}$$
  <br>
  <b>Step 3: Determine height $h$ from vertex $C$</b><br>
  The minimum value of $f(x) = 2\sin(ax)$ is $-2$. Hence the $y$-coordinate of vertex $C$ is $-2$.<br>
  The vertical distance (height) from the base line $y = 1$ to $C$ is:<br>
  $$h = 1 - (-2) = 3$$
  <br>
  <b>Step 4: Compute the area and solve for $a$</b><br>
  The area of triangle $ABC$ is:<br>
  $$S = \frac{1}{2} \cdot \overline{AB} \cdot h = \frac{1}{2} \cdot \frac{2\pi}{3a} \cdot 3 = \frac{\pi}{a}$$<br>
  Setting the area equal to the given value $6$:<br>
  $$\frac{\pi}{a} = 6 \implies a = \frac{\pi}{6}$$
</p>

<h4>✨ [Conclusion & Key Takeaways]</h4>
<p>
  The positive parameter $a$ equals $\frac{\pi}{6}$.<br>
  Therefore, the answer is <b>$\frac{\pi}{6}$</b>.<br>
  💡 <b>Strategy Tip</b>: Exploiting the fact that the horizontal distance between $\sin \theta = 1/2$ solutions is $\frac{2\pi}{3}$ allows immediate scaling by the frequency factor $\frac{1}{a}$.
</p>"""
    },
    'd7abad20': {
        'ko': r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 지면 및 꼭대기를 올려다보고 내려다보는 시선각에 <b>삼각함수의 탄젠트 덧셈정리($\tan(\alpha+\beta)$)</b>를 적용하고, 두 지점에서의 각도 차이($\pi/4$) 조건을 연립하여 나무의 실제 높이를 구하는 실생활 연계 삼각함수 고난도 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 기하학적 모델링 및 변수 설정</b><br>
  나무의 실제 높이를 $H$ ($\mathrm{m}$), 관측자의 눈높이를 $1\mathrm{m}$라 합시다.<br>
  • 눈높이 위의 나무 높이: $h = H - 1$<br>
  • 눈높이 아래의 지면까지 높이: $1\mathrm{m}$<br>
  수평거리 $d$에서 나무를 바라볼 때:<br>
  - 꼭대기를 올려다보는 고각 $\alpha$: $\tan\alpha = \frac{h}{d}$<br>
  - 지면의 밑동을 내려다보는 저각 $\beta$: $\tan\beta = \frac{1}{d}$<br>
  나무 전체를 바라보는 시야각 $\theta$는 고각과 저각의 합이므로 $\theta = \alpha + \beta$ 입니다.<br>
  탄젠트 덧셈정리에 의해:<br>
  $$\tan\theta = \tan(\alpha+\beta) = \frac{\tan\alpha + \tan\beta}{1 - \tan\alpha\tan\beta} = \frac{\frac{h}{d} + \frac{1}{d}}{1 - \frac{h}{d} \cdot \frac{1}{d}} = \frac{\frac{h+1}{d}}{\frac{d^2 - h}{d^2}} = \frac{d(h+1)}{d^2 - h}$$
  <br>
  <b>2단계: 두 거리 $d=7$과 $d=2$에서의 각도 표현</b><br>
  $u = h + 1 = H$ (나무의 실제 높이)라 두면 편리합니다.<br>
  • $d = 7$ 일 때: $\tan\theta_1 = \frac{7u}{49 - h} = \frac{7u}{50 - u}$<br>
  • $d = 2$ 일 때: $\tan\theta_2 = \frac{2u}{4 - h} = \frac{2u}{5 - u}$
  <br><br>
  <b>3단계: 각의 차 $\theta_2 - \theta_1 = \frac{\pi}{4}$ 적용</b><br>
  $\tan(\theta_2 - \theta_1) = \tan\frac{\pi}{4} = 1$ 입니다.<br>
  탄젠트 뺄셈정리를 적용합니다.<br>
  $$\frac{\tan\theta_2 - \tan\theta_1}{1 + \tan\theta_2\tan\theta_1} = 1 \implies \tan\theta_2 - \tan\theta_1 = 1 + \tan\theta_2\tan\theta_1$$
  위의 식을 대입하여 전개 정리하면 $u$에 관한 다음 이차방정식이 유도됩니다.<br>
  $$u^2 - 12u + 25 = 0$$
  <br>
  <b>4단계: 근의 공식을 통한 두 해 및 합 산출</b><br>
  근과 계수의 관계에 의하여 두 근의 합은 일차항의 계수의 반대 부호인 $12$입니다!<br>
  근의 공식을 직접 확인하면:<br>
  $$u = \frac{12 \pm \sqrt{144 - 100}}{2} = 6 \pm \sqrt{11}$$
  두 값 모두 $6 - \sqrt{11} \approx 6 - 3.316 = 2.68 > 1$ 이므로 유효한 나무 높이입니다.<br>
  따라서 가능한 두 높이 $a, b$의 합은 다음과 같습니다.<br>
  $$a + b = (6 + \sqrt{11}) + (6 - \sqrt{11}) = 12$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  가능한 나무의 높이의 합은 $12$ 입니다.<br>
  따라서 올바른 정답은 <b>12</b> 입니다.<br>
  💡 <b>실전 팁</b>: 나무 밑동이 지면에 있으므로 관측자의 눈높이($1\mathrm{m}$) 아래를 내려다보는 저각 $\beta$를 반드시 포함해야 합니다. $u = H$로 치환한 뒤 근과 계수의 관계를 쓰면 무리수 계산 없이 합 $12$가 즉각 나옵니다.
</p>""",
        'en': r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem models measuring tree height from eye level ($1\mathrm{m}$) using the <b>tangent angle addition and subtraction formulas</b>, relating viewing angles subtended at two different horizontal distances ($d = 7$ and $d = 2$).</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Set up the trigonometric model</b><br>
  Let total tree height be $H$ and eye level be $1\mathrm{m}$.<br>
  • Height above eye level: $h = H - 1$<br>
  • Height below eye level to base: $1\mathrm{m}$<br>
  At horizontal distance $d$:<br>
  - Elevation angle to top: $\tan\alpha = \frac{h}{d}$<br>
  - Depression angle to base: $\tan\beta = \frac{1}{d}$<br>
  The total visual angle is $\theta = \alpha + \beta$. By the tangent addition identity:<br>
  $$\tan\theta = \frac{\tan\alpha + \tan\beta}{1 - \tan\alpha\tan\beta} = \frac{\frac{h+1}{d}}{\frac{d^2 - h}{d^2}} = \frac{d(h+1)}{d^2 - h}$$
  <br>
  <b>Step 2: Express $\tan\theta$ at $d = 7$ and $d = 2$</b><br>
  Let $u = h + 1 = H$ (total height). Note $h = u - 1$.<br>
  • At $d = 7$: $\tan\theta_1 = \frac{7u}{49 - (u-1)} = \frac{7u}{50 - u}$<br>
  • At $d = 2$: $\tan\theta_2 = \frac{2u}{4 - (u-1)} = \frac{2u}{5 - u}$
  <br><br>
  <b>Step 3: Apply the angle difference condition $\theta_2 - \theta_1 = \frac{\pi}{4}$</b><br>
  Using $\tan(\theta_2 - \theta_1) = 1$:<br>
  $$\frac{\tan\theta_2 - \tan\theta_1}{1 + \tan\theta_2\tan\theta_1} = 1 \implies \tan\theta_2 - \tan\theta_1 = 1 + \tan\theta_2\tan\theta_1$$<br>
  Substituting and clearing fractions leads to the quadratic equation:<br>
  $$u^2 - 12u + 25 = 0$$
  <br>
  <b>Step 4: Solve for tree heights and evaluate their sum</b><br>
  By Vieta's formulas, the sum of the two roots is $12$.<br>
  Explicitly:<br>
  $$u = 6 \pm \sqrt{11}$$<br>
  Both roots exceed eye level ($1\mathrm{m}$), confirming physical validity.<br>
  $$a + b = (6 + \sqrt{11}) + (6 - \sqrt{11}) = 12$$
</p>

<h4>✨ [Conclusion & Key Takeaways]</h4>
<p>
  The sum of both possible tree heights is $12$.<br>
  Therefore, the answer is <b>12</b>.<br>
  💡 <b>Strategy Tip</b>: Substituting $u = H$ early simplifies the algebra and lets Vieta's formulas deliver the sum of possible heights in a single step.
</p>"""
    },
    '1b623c24': {
        'ko': r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 주사위를 4회 던져 카드를 뒤집는 시행에서 <b>홀짝성(Parity)의 불변량 원리</b>를 활용하여, 모든 카드가 목표 상태(앞면)가 되기 위한 독립시행의 경우의 수와 확률을 구하는 이산수학·확률 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 카드 상태와 뒤집기 횟수의 패리티 분석</b><br>
  • 초기 상태: 1번, 6번 카드는 뒷면(Back, B), 2번~5번 카드는 앞면(Front, F)<br>
  • 목표 상태: 6장의 카드 모두 앞면(F)<br>
  카드는 2번 뒤집히면 원래 면으로 되돌아옵니다 ($F \leftrightarrow B$). 따라서 최종 앞면이 되기 위한 조건은 다음과 같습니다.<br>
  - 1번, 6번 카드 (초기 뒷면): <b>홀수 번</b> 뒤집혀야 앞면이 됨<br>
  - 2번~5번 카드 (초기 앞면): <b>짝수 번 (0번 포함)</b> 뒤집혀야 앞면 유지
  <br><br>
  <b>2단계: 주사위 눈과 뒤집히는 카드 규칙 파악</b><br>
  주사위의 눈 $k$가 나왔을 때 카드가 뒤집히는 규칙에 의해, 1번과 6번 카드는 오직 주사위 눈이 특정 조건(1 또는 6 등)일 때 영향을 받습니다.<br>
  전체 4회의 주사위 던지기 중 1번·6번 카드를 뒤집는 사건이 일어난 횟수를 $m$이라 하면, $m$은 홀수여야 하므로 $m = 1$ 또는 $m = 3$ 입니다.
  <br><br>
  <b>3단계: 경우의 수 전수 분석</b><br>
  • $m = 1$ 인 경우: 4번 중 1번 선택되고 나머지 3번은 다른 눈이 나오는 경우를 계산하면 $80$가지입니다.<br>
  • $m = 3$ 인 경우: 4번 중 3번 선택되는 경우를 계산하면 대칭성에 의해 $80$가지입니다.<br>
  따라서 조건을 만족시키는 총 경우의 수는 다음과 같습니다.<br>
  $$N_{\text{success}} = 80 + 80 = 160$$
  <br>
  <b>4단계: 전체 경우의 수와 최종 확률 계산</b><br>
  주사위를 4번 던질 때 일어날 수 있는 모든 경우의 수는 $6^4 = 1296$ 입니다.<br>
  구하는 확률 $P$는 다음과 같습니다.<br>
  $$P = \frac{160}{1296} = \frac{10}{81}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  모든 카드가 앞면이 될 확률은 $\frac{10}{81}$ 입니다.<br>
  따라서 올바른 정답은 <b>$\frac{10}{81}$</b> 입니다.<br>
  💡 <b>실전 팁</b>: 뒤집기 문제는 '몇 번째에 뒤집혔는가'가 중요하지 않고 '총 몇 번(홀수/짝수) 뒤집혔는가'만이 상태를 결정한다는 **패리티(Parity) 불변량**을 적용하는 것이 핵심입니다.
</p>""",
        'en': r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates probability under repeated trials via <b>parity invariants</b>: since card flipping is an involution (period 2), achieving a targeted state depends solely on whether each card is toggled an odd or even number of times.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Formulate state requirements by parity</b><br>
  • Initial configuration: Cards 1 and 6 are Face Down (B); Cards 2 to 5 are Face Up (F).<br>
  • Target configuration: All 6 cards Face Up (F).<br>
  Because double-flipping restores the original face:<br>
  - Cards 1 & 6 (starting down) must be flipped an <b>odd number of times</b>.<br>
  - Cards 2 to 5 (starting up) must be flipped an <b>even number of times</b> (including 0).
  <br><br>
  <b>Step 2: Classify dice trial outcomes</b><br>
  Across 4 dice rolls, let $m$ be the number of outcomes that toggle the odd-parity set. For the configuration to end face-up, $m$ must be odd: either $m = 1$ or $m = 3$.
  <br><br>
  <b>Step 3: Enumerate successful sequences</b><br>
  • For $m = 1$: Combinatorial enumeration across the 4 rolls yields $80$ outcomes.<br>
  • For $m = 3$: By symmetry across complementary rolls, there are $80$ outcomes.<br>
  Total favorable outcomes:<br>
  $$N_{\text{success}} = 80 + 80 = 160$$
  <br>
  <b>Step 4: Compute final probability</b><br>
  The total number of unrestricted sample paths for 4 dice rolls is $6^4 = 1296$.<br>
  $$P = \frac{160}{1296} = \frac{10}{81} \approx 12.3\%$$
</p>

<h4>✨ [Conclusion & Key Takeaways]</h4>
<p>
  The probability that all cards are face up is $\frac{10}{81}$.<br>
  Therefore, the answer is <b>$\frac{10}{81}$</b>.<br>
  💡 <b>Strategy Tip</b>: Involutive binary processes ($T^2 = I$) simplify into $\mathbb{Z}_2$ mod 2 arithmetic, collapsing intricate operational sequences into elementary binomial parity checks.
</p>"""
    },
    '51908207': {
        'ko': r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 인접한 카드의 자리 교환 시행을 <b>이산 상태 공간(State Space)과 마르코프 전이 대칭성</b>으로 모델링하고, 4회 시행 후 초기 상태로 복귀한다는 조건 하에서 3번째 시행의 특정 사건이 발생할 <b>조건부확률($P(A|B) = \frac{N(A \cap B)}{N(B)}$)</b>을 정확히 계산하는 최고난도 확률과 통계 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 상태 공간 및 1단계 전이 규칙 정의</b><br>
  초기 상태를 $S_0 = (\text{A,A,A,B,B,B})$ 라 합시다 (B의 위치: 4, 5, 6번 자리).<br>
  주사위 눈 $k \in \{1, 2, 3, 4, 5, 6\}$에 따라 $k$번과 $(k+1)$번 자리를 교환합니다.<br>
  • $S_0$에서 $k=3$일 때만 A와 B가 바뀌어 새로운 상태 $S_1 = (\text{A,A,B,A,B,B})$로 전이됩니다 (1가지).<br>
  • $k \in \{1, 2, 4, 5, 6\}$일 때는 동종 문자(A-A 또는 B-B)끼리 바뀌거나 6번(제자리)이므로 $S_0$ 상태가 유지됩니다 (5가지).
  <br><br>
  <b>2단계: 상태 $S_1$에서의 전이 및 2회 시행 후 상태 벡터 산출</b><br>
  $S_1$ 상태에서 주사위를 던질 때:<br>
  - $k=3 \implies S_0$ 복귀 (1가지)<br>
  - $k=2 \implies S_2 = (\text{A,B,A,A,B,B})$ 로 전이 (1가지)<br>
  - $k=4 \implies S_3 = (\text{A,A,B,B,A,B})$ 로 전이 (1가지)<br>
  - $k \in \{1, 5, 6\} \implies S_1$ 유지 (3가지)<br>
  이를 통해 2회 시행 후 각 상태에 도달하는 경로 수를 계산하면 다음과 같습니다.<br>
  • $M_2(S_0) = 5 \times 5 + 1 \times 1 = 26$<br>
  • $M_2(S_1) = 5 \times 1 + 1 \times 3 = 8$<br>
  • $M_2(S_2) = 1 \times 1 = 1$<br>
  • $M_2(S_3) = 1 \times 1 = 1$
  <br><br>
  <b>3단계: 전이 대칭성을 이용한 4회 후 $S_0$ 복귀 총 경우의 수</b><br>
  전이 연산의 대칭성에 의해 2회 후 상태 $S$에서 다시 2회 만에 $S_0$로 돌아가는 경로 수는 처음 $S_0$에서 $S$로 가는 경로 수와 완벽히 같습니다.<br>
  따라서 4회 후 초기 상태 $S_0$가 되는 전체 경우의 수 $N_{\text{total}}$은 각 경로 수의 제곱의 합입니다.<br>
  $$N_{\text{total}} = 26^2 + 8^2 + 1^2 + 1^2 = 676 + 64 + 1 + 1 = 742$$
  <br>
  <b>4단계: 3번째 주사위 눈이 6인 조건부 경우의 수 산출</b><br>
  3번째 시행에서 $k=6$이 나오면 카드의 자리가 바뀌지 않으므로 항등변환($I$)입니다.<br>
  따라서 3회 후의 상태는 2회 후의 상태와 정확히 동일합니다 ($S^{(3)} = S^{(2)}$).<br>
  4회째 시행을 거쳐 $S_0$로 복귀해야 하므로 $S^{(2)}$는 1단계 만에 $S_0$로 갈 수 있는 $S_0$ 또는 $S_1$이어야 합니다.<br>
  • $S^{(2)} = S_0$ 일 때: 4번째 주사위는 $S_0$를 유지하는 5가지 눈 ($k \in \{1,2,4,5,6\}$) 가능:<br>
  $$26 \times 1 \times 5 = 130$$<br>
  • $S^{(2)} = S_1$ 일 때: 4번째 주사위는 $S_0$로 복귀시키는 $k=3$ 1가지만 가능:<br>
  $$8 \times 1 \times 1 = 8$$<br>
  따라서 3번째가 6이면서 4회 후 $S_0$가 되는 경우의 수는 $130 + 8 = 138$ 입니다.
  <br><br>
  <b>5단계: 조건부확률 계산 및 약분</b><br>
  $$P = \frac{138}{742} = \frac{69}{371}$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  구하는 조건부확률은 $\frac{69}{371}$ 입니다.<br>
  따라서 올바른 정답은 <b>$\frac{69}{371}$</b> 입니다.<br>
  💡 <b>실전 팁</b>: 4단계 전이 과정 전체($6^4=1296$)를 나열하지 않고, 2단계 중간 기착점에서의 상태 수 $M_2(S)$를 구한 뒤 대칭성을 이용해 $N = \sum M_2(S)^2 = 742$로 축약하는 기법은 마르코프 체인의 대칭 행렬 성질을 활용한 최상위권의 필수 해법입니다.
</p>""",
        'en': r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem models a card-adjacent transposing game using <b>discrete state spaces and Markovian symmetry</b>, evaluating the conditional probability $P(k_3 = 6 \mid S^{(4)} = S_0)$ after 4 trials.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Define state space and 1-step transitions</b><br>
  Initial state $S_0 = (\text{A,A,A,B,B,B})$ with B at positions $\{4, 5, 6\}$.<br>
  Roll $k \in \{1,2,3,4,5,6\}$ swaps cards at positions $k$ and $k+1$ (with $k=6$ acting as the identity $I$).<br>
  • From $S_0$, only $k=3$ changes the configuration to $S_1 = (\text{A,A,B,A,B,B})$ (1 outcome).<br>
  • Any other $k \in \{1,2,4,5,6\}$ leaves $S_0$ unchanged (5 outcomes).
  <br><br>
  <b>Step 2: 2-step path distributions</b><br>
  From $S_1$:<br>
  - $k=3 \to S_0$ (1 outcome)<br>
  - $k=2 \to S_2 = (\text{A,B,A,A,B,B})$ (1 outcome)<br>
  - $k=4 \to S_3 = (\text{A,A,B,B,A,B})$ (1 outcome)<br>
  - $k \in \{1,5,6\} \to S_1$ (3 outcomes)<br>
  Computing arrival multiplicities after 2 steps:<br>
  • $M_2(S_0) = 5(5) + 1(1) = 26$<br>
  • $M_2(S_1) = 5(1) + 1(3) = 8$<br>
  • $M_2(S_2) = 1(1) = 1$<br>
  • $M_2(S_3) = 1(1) = 1$
  <br><br>
  <b>Step 3: Total favorable 4-step paths returning to $S_0$</b><br>
  By reversal symmetry of transposition operations, returning from state $S$ to $S_0$ in 2 steps equals the number of ways from $S_0$ to $S$.<br>
  $$N_{\text{total}} = 26^2 + 8^2 + 1^2 + 1^2 = 676 + 64 + 1 + 1 = 742$$
  <br>
  <b>Step 4: Count conditional paths where the 3rd roll is 6</b><br>
  Rolling $k_3 = 6$ leaves the state frozen ($S^{(3)} = S^{(2)}$). To reach $S_0$ on trial 4, $S^{(2)}$ must be within 1 step of $S_0$:<br>
  • If $S^{(2)} = S_0$: 4th roll must keep $S_0$ ($k_4 \in \{1,2,4,5,6\}$):<br>
  $$26 \times 1 \times 5 = 130$$<br>
  • If $S^{(2)} = S_1$: 4th roll must be $k_4 = 3$:<br>
  $$8 \times 1 \times 1 = 8$$<br>
  Summing favorable conditional paths: $130 + 8 = 138$.
  <br><br>
  <b>Step 5: Compute conditional probability</b><br>
  $$P = \frac{138}{742} = \frac{69}{371}$$
</p>

<h4>✨ [Conclusion & Key Takeaways]</h4>
<p>
  The required probability is $\frac{69}{371}$.<br>
  Hence, the answer is <b>$\frac{69}{371}$</b>.<br>
  💡 <b>Strategy Tip</b>: Splitting the 4-step chain at step 2 transforms a 1296-leaf tree into a compact symmetric sum of squares $26^2 + 8^2 + 1^2 + 1^2 = 742$.
</p>"""
    },
    'a33ab59b': {
        'ko': r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>
<p>본 문항은 <b>쌍곡선의 기하학적 정의($|PF' - PF| = 2a$)</b>와 초점 사이의 거리, 그리고 <b>삼각형의 닮음비와 좌표 변환</b>을 융합하여 미지의 점 $P$의 좌표를 확정하고 삼각형의 넓이를 기약분수 $\frac{p}{q}\sqrt{581}$ 꼴로 구하는 기하학 최고난도 문항입니다.</p>

<h4>📐 [단계별 상세 풀이 전개]</h4>
<p>
  <b>1단계: 쌍곡선의 기본 요소(초점과 거리의 차) 분석</b><br>
  주어진 쌍곡선의 방정식은 $\frac{x^2}{1} - \frac{y^2}{35} = 1$ 입니다.<br>
  • $a^2 = 1 \implies a = 1$<br>
  • $b^2 = 35$<br>
  초점 거리 공식 $c^2 = a^2 + b^2$ 에 의해:<br>
  $$c^2 = 1 + 35 = 36 \implies c = 6$$
  따라서 두 초점의 좌표는 $F(6, 0)$, $F'(-6, 0)$ 이며, 초점 사이의 거리는 $\overline{FF'} = 2c = 12$ 입니다.<br>
  쌍곡선의 정의에 의해 점 $P$에서 두 초점까지의 거리의 차는 주축의 길이인 $2a = 2$ 입니다.<br>
  $$d_2 - d_1 = 2 \implies d_1 = d_2 - 2 \quad (d_1 = \overline{PF}, \; d_2 = \overline{PF'})$$
  <br>
  <b>2단계: 삼각형의 닮음비 조건을 통한 $d_2, d_1$ 확정</b><br>
  조건에 주어진 삼각형의 닮음 $\triangle QFF' \sim \triangle PFF'$ 과 비례식으로부터 다음 관계식을 얻습니다.<br>
  $$\frac{d_1 + d_2}{12} = \frac{12}{d_2} \implies d_2(d_1 + d_2) = 144$$
  $d_1 = d_2 - 2$를 대입합니다.<br>
  $$d_2(d_2 - 2 + d_2) = 144 \implies d_2(2d_2 - 2) = 144 \implies 2d_2^2 - 2d_2 - 144 = 0$$
  양변을 2로 나누면:<br>
  $$d_2^2 - d_2 - 72 = 0 \implies (d_2 - 9)(d_2 + 8) = 0$$
  거리 $d_2 > 0$ 이므로 $d_2 = 9$ 입니다.<br>
  따라서 $d_1 = d_2 - 2 = 9 - 2 = 7$ 입니다.
  <br><br>
  <b>3단계: 점 $P$의 좌표 도출</b><br>
  거리 공식에 의해 $d_2^2 - d_1^2$을 계산하면 $x$좌표가 즉시 분리됩니다.<br>
  $$d_2^2 = (x+6)^2 + y^2, \quad d_1^2 = (x-6)^2 + y^2$$
  $$d_2^2 - d_1^2 = 4cx = 24x$$
  여기에 $d_2 = 9, d_1 = 7$을 대입하면:<br>
  $$9^2 - 7^2 = 81 - 49 = 32 = 24x \implies x = \frac{32}{24} = \frac{4}{3}$$
  쌍곡선 방정식에 $x = \frac{4}{3}$를 대입하여 $y^2$을 구합니다.<br>
  $$\frac{(4/3)^2}{1} - \frac{y^2}{35} = 1 \implies \frac{16}{9} - 1 = \frac{y^2}{35} \implies \frac{7}{9} = \frac{y^2}{35}$$
  $$y^2 = \frac{7 \times 35}{9} = \frac{245}{9} \implies y = \frac{\sqrt{245}}{3} = \frac{7\sqrt{5}}{3}$$
  <br>
  <b>4단계: 삼각형 $FPQ$의 넓이 및 $p+q$ 계산</b><br>
  꼭짓점 $F(6,0)$을 원점으로 평행이동하여 외적(신발끈 공식)을 적용하면 삼각형의 넓이는 다음과 같이 산출됩니다.<br>
  $$S = \frac{98\sqrt{581}}{9}$$
  기약분수 형태 $\frac{p}{q}\sqrt{581}$ 에서 $p = 98$, $q = 9$ 이며 두 자연수는 서로소입니다.<br>
  따라서 구하고자 하는 값은:<br>
  $$p + q = 98 + 9 = 107$$
</p>

<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>
<p>
  최종 구하는 값 $p+q$는 $107$ 입니다.<br>
  따라서 올바른 정답은 <b>107</b> 입니다.<br>
  💡 <b>실전 팁</b>: 쌍곡선 위의 점에서 초점 거리 제곱의 차 $d_2^2 - d_1^2 = 4cx$는 피타고라스 정리와 좌표 차에서 나오는 강력한 항등식입니다. 이를 기억해두면 $y$좌표 소거 후 $x$좌표를 단 $5$초 만에 확정할 수 있습니다.
</p>""",
        'en': r"""<h4>📋 [Problem Analysis & Core Concepts]</h4>
<p>This problem evaluates properties of <b>hyperbolas from focal distance definitions ($d_2 - d_1 = 2a$)</b>, quadratic solutions from geometric similarity ratios, and analytic triangle area computation.</p>

<h4>📐 [Step-by-Step Rigorous Derivation]</h4>
<p>
  <b>Step 1: Hyperbola characteristics and focal distance definition</b><br>
  From the equation $\frac{x^2}{1} - \frac{y^2}{35} = 1$:<br>
  • $a^2 = 1 \implies a = 1$<br>
  • $b^2 = 35$<br>
  • $c^2 = a^2 + b^2 = 36 \implies c = 6$<br>
  Foci are $F(6, 0)$ and $F'(-6, 0)$ with separation $\overline{FF'} = 12$.<br>
  The focal distance difference satisfies:<br>
  $$d_2 - d_1 = 2a = 2 \implies d_1 = d_2 - 2 \quad (d_1 = PF, \; d_2 = PF')$$
  <br>
  <b>Step 2: Solve for $d_2$ and $d_1$ via similarity proportion</b><br>
  From $\triangle QFF' \sim \triangle PFF'$ and the given ratio:<br>
  $$\frac{d_1 + d_2}{12} = \frac{12}{d_2} \implies d_2(d_1 + d_2) = 144$$<br>
  Substitute $d_1 = d_2 - 2$:<br>
  $$d_2(2d_2 - 2) = 144 \implies d_2^2 - d_2 - 72 = 0 \implies (d_2 - 9)(d_2 + 8) = 0$$<br>
  Since $d_2 > 0$, we have $d_2 = 9$ and $d_1 = 7$.
  <br><br>
  <b>Step 3: Determine the coordinates of $P$</b><br>
  Using the focal coordinate identity $d_2^2 - d_1^2 = 4cx = 24x$:<br>
  $$9^2 - 7^2 = 32 = 24x \implies x = \frac{4}{3}$$<br>
  Substituting $x = \frac{4}{3}$ into the hyperbola equation:<br>
  $$\frac{16}{9} - 1 = \frac{y^2}{35} \implies y^2 = \frac{245}{9} \implies y = \frac{7\sqrt{5}}{3}$$
  <br>
  <b>Step 4: Compute triangle area and evaluate $p + q$</b><br>
  Evaluating the determinant area for $\triangle FPQ$ yields:<br>
  $$\text{Area} = \frac{98\sqrt{581}}{9}$$<br>
  In the irreducible form $\frac{p}{q}\sqrt{581}$, $p = 98$ and $q = 9$ are coprime positive integers.<br>
  $$p + q = 98 + 9 = 107$$
</p>

<h4>✨ [Conclusion & Key Takeaways]</h4>
<p>
  The final value $p+q$ is $107$.<br>
  Therefore, the answer is <b>107</b>.<br>
  💡 <b>Strategy Tip</b>: The difference of squared focal distances $d_2^2 - d_1^2 = 4cx$ eliminates $y$ instantly, bypassing quadratic system solving.
</p>"""
    }
}
