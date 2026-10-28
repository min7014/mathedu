# -*- coding: utf-8 -*-
"""a33ab59b (쌍곡선 PF'-PF=2 문제) 수식 LaTeX 교정 + 정교화(자동 업그레이드) 재생성.
- 기존: 수식을 $...$ 없이 일반 텍스트(d2^2 등)로 저장 → MathJax 미렌더
- 수정: 모든 수식에 $...$ LaTeX 래핑. 같은 slug 로 덮어쓰기.
- 정교화: 5단계 → 17단계 원자 분해, 단계 간 재료 연결 명시, 기호(닮음비) 추가.
- 로컬 LLM 미사용. 에이전트 직접 작성.
"""
import os, sys, importlib.util
if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
import generator

# 검증기(자체 교정+경고) — 모든 문제 생성 시 필수 통과
_spec = importlib.util.spec_from_file_location("verify_quiz", "verify_quiz.py")
verify_quiz = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(verify_quiz)

SLUG = "a33ab59b"
OUT = os.path.join("board", f"{SLUG}.html")

data = {
  "slug": SLUG,
  "title": "쌍곡선 PF' - PF = 2 조건의 점 P좌표와 삼각형 넓이 (기초→심화)",
  "title_en": "Hyperbola Condition PF' - PF = 2 · Coordinates of Point P and Triangle Area",
  "symbols": [
    {"sym": r"쌍곡선", "desc": "두 초점에서의 거리 차이가 일정한 점들의 자취. $|PF'-PF|=2a$", "desc_en": r"Locus of points with a constant difference of distances to two foci: $|PF'-PF|=2a$."},
    {"sym": r"초점거리 $2c$", "desc": "두 초점 F, F' 사이 거리. $c^2=a^2+b^2$", "desc_en": r"Distance between foci $F$ and $F'$, where $c^2=a^2+b^2$."},
    {"sym": r"거리 $d_1,d_2$", "desc": r"$d_1=PF,\ d_2=PF'$ (두 초점까지의 거리)", "desc_en": r"Distances $d_1=PF$ and $d_2=PF'$ to the two foci."},
    {"sym": r"닮음비", "desc": r"$\triangle QFF'\sim\triangle PFF'$일 때 대응변 비율. 여기선 $\frac{d_1+d_2}{12}=\frac{12}{d_2}$", "desc_en": r"Ratio of corresponding sides in similar triangles $\triangle QFF'\sim\triangle PFF'$."},
    {"sym": r"넓이(행렬식)", "desc": r"꼭짓점 F를 기준으로 $\tfrac12\left|\det(\overrightarrow{FP},\overrightarrow{FQ})\right|$", "desc_en": r"Triangle area via determinant with respect to vertex $F$: $\tfrac12\left|\det(\overrightarrow{FP},\overrightarrow{FQ})\right|$."},
  ],
  "levels": [
    {
      "stage": "level1",
      "title": "🔰 제1단계 · [초등 뺄셈과 수직선 거리 연계] 쌍곡선의 정의와 거리 차 (가장 기초)",
      "title_en": "🔰 Step 1 · [Elementary Subtraction & Distance Link] Definition of a Hyperbola",
      "knowledge": "초등학교 사칙연산에서 두 수의 '차(뺄셈)'가 항상 일정한 규칙을 떠올려 봅시다. 쌍곡선은 '두 초점까지 거리의 차(뺄셈)'가 항상 일정한 점들의 모임이고, 거리는 늘 양수입니다.",
      "knowledge_en": "Recall elementary subtraction where the difference between two lengths remains constant. A hyperbola is the set of points whose distance difference to two fixed foci is constant.",
      "questions": [
        {"stem": r"초등학교 뺄셈과 거리 규칙: 쌍곡선에서 한 점 P의 두 초점 F, F'까지 거리를 각각 $d_1=PF,\ d_2=PF'$라 할 때, 쌍곡선의 정의로 항상 성립하는 것은?",
         "stem_en": r"Elementary subtraction & distance rule: For a point $P$ on a hyperbola with focal distances $d_1=PF$ and $d_2=PF'$, which relation always holds by definition?",
         "options": [r"$|d_2-d_1|=2a$ (거리 차가 일정)",
                     r"$d_1+d_2=2a$ (거리 합이 일정)",
                     r"$d_1=d_2$ (거리 같음)",
                     r"$d_1\cdot d_2=2a$",
                     r"$d_1/d_2=2a$"],
         "answer": 1,
         "exp": r"쌍곡선의 정의: 두 초점까지 거리의 차 $|PF'-PF|$ 가 상수 $2a$ 입니다. 즉 $|d_2-d_1|=2a$.",
         "exp_en": r"By definition of a hyperbola, the absolute difference of focal distances $|PF'-PF|$ is constant ($2a$), i.e., $|d_2-d_1|=2a$."},
      ],
    },
    {
      "stage": "level2",
      "title": "제2단계 · $a^2$ 알아내기",
      "knowledge": r"쌍곡선 표준형은 $\dfrac{x^2}{a^2}-\dfrac{y^2}{b^2}=1$ 꼴입니다. 주어진 식에서 $a^2$를 읽어냅니다.",
      "questions": [
        {"stem": r"방정식 $\dfrac{x^2}{a^2}-\dfrac{y^2}{b^2}=1$에서, $\dfrac{x^2}{1}-\dfrac{y^2}{35}=1$이라면 $a^2$은?",
         "options": ["$a^2=1$", "$a^2=35$", "$a^2=36$", "$a^2=0$", "$a^2=-1$"],
         "answer": 1,
         "exp": r"$\dfrac{x^2}{a^2}$ 의 분모가 $a^2$ 이므로 $a^2=1$."},
      ],
    },
    {
      "stage": "level3",
      "title": "제3단계 · $c$ 구하기 (1): $c^2$",
      "knowledge": r"쌍곡선에서 초점거리와 관련된 식은 $c^2=a^2+b^2$ 입니다. $a^2=1,\ b^2=35$예요.",
      "questions": [
        {"stem": r"$c^2=a^2+b^2$ 이고 $a^2=1,\ b^2=35$ 일 때 $c^2$는?",
         "options": ["$c^2=36$", "$c^2=1$", "$c^2=35$", "$c^2=6$", "$c^2=30$"],
         "answer": 1,
         "exp": r"$c^2=a^2+b^2=1+35=36$."},
      ],
    },
    {
      "stage": "level4",
      "title": "제4단계 · $c$ 구하기 (2): $c=6$",
      "knowledge": r"제3단계에서 $c^2=36$ 이므로 $c=6$ 입니다.",
      "questions": [
        {"stem": r"$c^2=36$ 일 때 $c$는? (거리는 양수)",
         "options": ["$c=6$", "$c=1$", "$c=5$", r"$c=\sqrt{35}$", "$c=36$"],
         "answer": 1,
         "exp": r"$c^2=36$ 이므로 양수 $c=6$."},
      ],
    },
    {
      "stage": "level5",
      "title": "제5단계 · 초점 좌표",
      "knowledge": r"초점은 x축 위에 있고 $c=6$ 이므로 $F(6,0),\ F'(-6,0)$ 입니다. 초점거리 $2c=12$예요.",
      "questions": [
        {"stem": r"초점이 x축 위에 있고 $c=6$ 이므로 두 초점의 좌표로 옳은 것은?",
         "options": [r"$F(6,0),\ F'(-6,0)$",
                     r"$F(0,6),\ F'(0,-6)$",
                     r"$F(1,0),\ F'(-1,0)$",
                     r"$F(6,6),\ F'(-6,-6)$",
                     r"$F(3,0),\ F'(-3,0)$"],
         "answer": 1,
         "exp": r"x축 위 초점, $c=6$ 이므로 $F(c,0)=(6,0),\ F'(-c,0)=(-6,0)$."},
      ],
    },
    {
      "stage": "level6",
      "title": "제6단계 · 거리차 관계",
      "knowledge": r"문제 조건 '$PF'-PF=2$' 이고 $2a=2$ 입니다. $d_1=PF,\ d_2=PF'$로 둡니다.",
      "questions": [
        {"stem": r"$2a=2$ 이고 $PF'-PF=2$ 라면, $d_2-d_1$ 의 값은? ($d_2=PF',\ d_1=PF$)",
         "options": [r"$d_2-d_1=2$",
                     r"$d_2-d_1=1$",
                     r"$d_2+d_1=2$",
                     r"$d_2-d_1=6$",
                     r"$d_1-d_2=2$"],
         "answer": 1,
         "exp": r"$PF'=d_2,\ PF=d_1$ 이므로 $d_2-d_1=2$."},
      ],
    },
    {
      "stage": "level7",
      "title": "제7단계 · P의 위치",
      "knowledge": r"제6단계 결과 $d_2-d_1=2>0$ 이므로 $d_2>d_1$ 입니다. 즉 P는 어느 초점에 더 가까울까요?",
      "questions": [
        {"stem": r"$d_2>d_1$ 이므로 P의 위치에 대한 설명으로 가장 적절한 것은?",
         "options": [r"P는 F 에 더 가까운 쪽 (우측 가지)",
                     r"P는 F' 에 더 가까운 쪽",
                     r"$d_1=d_2$ 인 수선의 발",
                     r"P는 두 초점의 중점",
                     r"P는 원점"],
         "answer": 1,
         "exp": r"$d_2>d_1$ 이므로 P는 F' 보다 F 에 더 가깝습니다(우측 가지)."},
      ],
    },
    {
      "stage": "level8",
      "title": "제8단계 · 닮음의 공통각",
      "knowledge": r"$\triangle QFF'$ 와 $\triangle PFF'$ 가 닮음일 때, 두 삼각형이 공유하는 꼭짓점을 찾습니다.",
      "questions": [
        {"stem": r"$\triangle QFF'$ 와 $\triangle PFF'$ 가 공유하는 꼭짓점각은?",
         "options": [r"$\angle QF'F = \angle PF'F$ (공통각)",
                     r"$\angle QFF' = \angle PFF'$",
                     r"$\angle FQF' = \angle FPF'$",
                     r"직각",
                     r"$60^{\circ}$"],
         "answer": 1,
         "exp": r"두 삼각형이 꼭짓점 $F'$ 을 공유하므로 $\angle QF'F = \angle PF'F$ 가 공통각입니다."},
      ],
    },
    {
      "stage": "level9",
      "title": "제9단계 · 닮음비 식 세우기",
      "knowledge": r"닮음비는 대응변의 길이 비입니다. 한 변의 길이는 $d_1+d_2=PF+PF'$, 다른 쪽 빗변은 $FF'=12$예요.",
      "questions": [
        {"stem": r"닮음비 조건 $\dfrac{PF+PF'}{FF'}=\dfrac{FF'}{PF'}$ 에서, $d_1+d_2$ 와 $FF'=12$ 를 넣으면 성립하는 식은?",
         "options": [r"$\dfrac{d_1+d_2}{12}=\dfrac{12}{d_2}$",
                     r"$\dfrac{d_1+d_2}{d_2}=12$",
                     r"$\dfrac{12}{d_1+d_2}=\dfrac{d_2}{12}$",
                     r"$\dfrac{d_1+d_2}{12}=\dfrac{d_2}{12}$",
                     r"$\dfrac{d_1+d_2}{d_2}=\dfrac{12}{12}$"],
         "answer": 1,
         "exp": r"$\dfrac{d_1+d_2}{FF'}=\dfrac{FF'}{d_2}$ 에 $FF'=12$ 를 넣으면 $\dfrac{d_1+d_2}{12}=\dfrac{12}{d_2}$."},
      ],
    },
    {
      "stage": "level10",
      "title": "제10단계 · 양변 정리",
      "knowledge": r"제9단계 식 $\dfrac{d_1+d_2}{12}=\dfrac{12}{d_2}$ 의 양변에 $12d_2$ 를 곱해 정리합니다.",
      "questions": [
        {"stem": r"$\dfrac{d_1+d_2}{12}=\dfrac{12}{d_2}$ 양변에 $12d_2$를 곱해 정리한 식은?",
         "options": [r"$d_2(d_1+d_2)=144$",
                     r"$d_2(d_1+d_2)=12$",
                     r"$d_1+d_2=12d_2$",
                     r"$d_2^2=144$",
                     r"$(d_1+d_2)d_2=12$"],
         "answer": 1,
         "exp": r"양변에 $12d_2$ 를 곱하면 $d_2(d_1+d_2)=144$."},
      ],
    },
    {
      "stage": "level11",
      "title": "제11단계 · $d_1$ 대입 → 이차방정식",
      "knowledge": r"제6단계에서 $d_1=d_2-2$ 였습니다. 이를 제10단계 식에 대입해 $d_2$ 의 이차방정식을 만듭니다.",
      "questions": [
        {"stem": r"$d_1=d_2-2$ 를 $d_2(d_1+d_2)=144$ 에 대입해 얻는 $d_2$ 의 이차방정식은? (양변 2로 나눈 꼴)",
         "options": [r"$d_2^2-d_2-72=0$",
                     r"$d_2^2+d_2-72=0$",
                     r"$d_2^2-2d_2-72=0$",
                     r"$d_2^2-d_2+72=0$",
                     r"$2d_2^2-d_2-72=0$"],
         "answer": 1,
         "exp": r"$d_2\big((d_2-2)+d_2\big)=d_2(2d_2-2)=144$ → $2d_2^2-2d_2-144=0$ → 양변 2로 나눠 $d_2^2-d_2-72=0$."},
      ],
    },
    {
      "stage": "level12",
      "title": "제12단계 · $d_2$ 풀기",
      "knowledge": r"제11단계 이차방정식을 인수분해합니다. 거리는 양수만 취해요.",
      "questions": [
        {"stem": r"$d_2^2-d_2-72=0$ 의 양의해 $d_2(=PF')$ 는?",
         "options": ["$9$", "$8$", "$12$", "$-8$", "$6$"],
         "answer": 1,
         "exp": r"$(d_2-9)(d_2+8)=0$ 이므로 양의해 $d_2=9$."},
      ],
    },
    {
      "stage": "level13",
      "title": "제13단계 · $d_1$ 구하기",
      "knowledge": r"제6단계 관계 $d_1=d_2-2$ 에 제12단계 $d_2=9$ 를 넣습니다.",
      "questions": [
        {"stem": r"$d_1=d_2-2$ 이고 $d_2=9$ 이므로 $d_1(=PF)$ 는?",
         "options": ["$7$", "$9$", "$11$", "$5$", "$2$"],
         "answer": 1,
         "exp": r"$d_1=9-2=7$."},
      ],
    },
    {
      "stage": "level14",
      "title": "제14단계 · P의 x좌표",
      "knowledge": r"문제가 주는 관계 $d_2^2-d_1^2=24x$ 에 제12·13단계 값을 넣습니다.",
      "questions": [
        {"stem": r"$d_2^2-d_1^2=24x$ 일 때, $d_2=9,\ d_1=7$ 을 넣어 구한 $x$ 는?",
         "options": [r"$x=\tfrac{4}{3}$",
                     "$x=32$",
                     "$x=24$",
                     r"$x=\tfrac{3}{4}$",
                     "$x=1$"],
         "answer": 1,
         "exp": r"$d_2^2-d_1^2=81-49=32$ 이므로 $24x=32$ → $x=\tfrac{32}{24}=\tfrac{4}{3}$."},
      ],
    },
    {
      "stage": "level15",
      "title": "제15단계 · 넓이 공식",
      "knowledge": r"꼭짓점 F를 기준으로 한 $\triangle FPQ$ 의 넓이는 벡터 FP, FQ의 행렬식 절반입니다.",
      "questions": [
        {"stem": r"꼭짓점 F를 기준으로 한 $\triangle FPQ$ 의 넓이 공식으로 옳은 것은?",
         "options": [r"$\tfrac12\left|\det(\overrightarrow{FP},\overrightarrow{FQ})\right|$",
                     r"$\tfrac12\,PF\cdot FQ$",
                     r"$\tfrac12\,d_1d_2$",
                     r"$\det(\overrightarrow{FP},\overrightarrow{FQ})$",
                     r"$\sqrt{d_1^2+d_2^2}$"],
         "answer": 1,
         "exp": r"원점 대신 F를 기준으로 하므로 넓이 $=\tfrac12\left|\det(\overrightarrow{FP},\overrightarrow{FQ})\right|$."},
      ],
    },
    {
      "stage": "level16",
      "title": "제16단계 · 넓이 약분",
      "knowledge": r"행렬식을 풀어 얻은 넓이 $\dfrac{882\sqrt{581}}{81}$ 을 기약분수로 약분합니다.",
      "questions": [
        {"stem": r"넓이 $\dfrac{882\sqrt{581}}{81}$ 을 약분한 값은? ($882=9\times98,\ 81=9\times9$)",
         "options": [r"$\dfrac{98\sqrt{581}}{9}$",
                     r"$\dfrac{882\sqrt{581}}{9}$",
                     r"$98\sqrt{581}$",
                     r"$\dfrac{98}{9}$",
                     r"$\dfrac{882\sqrt{581}}{81}$"],
         "answer": 1,
         "exp": r"$\dfrac{882\sqrt{581}}{81}=\dfrac{882\div9}{81\div9}\sqrt{581}=\dfrac{98\sqrt{581}}{9}$."},
      ],
    },
    {
      "stage": "level17",
      "title": "제17단계 · $p+q$",
      "knowledge": r"넓이를 기약분수 $\dfrac{p}{q}\sqrt{581}$ ($p,q$ 서로소)로 나타냈을 때 $p,q$를 세어 더합니다.",
      "questions": [
        {"stem": r"넓이를 기약분수 $\dfrac{p}{q}\sqrt{581}$ ($p,q$ 서로소)라 할 때 $p+q$ 는?",
         "options": ["$107$", "$98$", "$9$", "$105$", "$117$"],
         "answer": 1,
         "exp": r"$p=98,\ q=9$ (서로소) 이므로 $p+q=107$."},
      ],
    },
  ],
  "final": {
    "stem": (r"쌍곡선 $\dfrac{x^2}{1}-\dfrac{y^2}{35}=1$ 위의 점 P에 대하여 $PF'-PF=2$ 라 하자. "
             r"$\triangle QFF'$ 와 $\triangle PFF'$ 가 닮음이고 $\dfrac{PF+PF'}{FF'}=\dfrac{FF'}{PF'}$ 일 때, "
             r"점 P의 x좌표와 $\triangle FPQ$ 의 넓이를 기약분수 $\dfrac{p}{q}\sqrt{581}$ ($p,q$ 서로소)로 나타냈을 때 "
             r"$p+q$ 의 값을 구하시오."),
    "stem_en": (r"For a point $P$ on the hyperbola $\dfrac{x^2}{1}-\dfrac{y^2}{35}=1$ satisfying $PF'-PF=2$, "
                r"suppose $\triangle QFF' \sim \triangle PFF'$ and $\dfrac{PF+PF'}{FF'}=\dfrac{FF'}{PF'}$. "
                r"When the area of $\triangle FPQ$ is expressed as an irreducible fraction $\dfrac{p}{q}\sqrt{581}$ ($\gcd(p,q)=1$), "
                r"find the value of $p+q$."),
    "options": ["$107$", "$98$", "$105$", "$117$", "$9$"],
    "answer": 1,
    "exp": (r"$a^2=1,\ b^2=35$ 에서 $c=6$, 초점 $F(6,0),F'(-6,0)$. $PF'-PF=2$ 이므로 $d_2-d_1=2$. "
            r"닮음에서 $d_2(d_1+d_2)=144$ → $d_2^2-d_2-72=0$ → $d_2=9,\ d_1=7$. "
            r"$d_2^2-d_1^2=24x$ 에서 $x=4/3$. 넓이 $=\tfrac{98\sqrt{581}}{9}$ 이므로 $p+q=98+9=107$."),
    "exp_en": (r"From $a^2=1, b^2=35$, we have $c=6$ and $FF'=12$. Similarity yields $d_2(d_1+d_2)=144$ with $d_1=d_2-2$, giving $d_2=9, d_1=7$. "
               r"The area of $\triangle FPQ$ is $\dfrac{98\sqrt{581}}{9}$, so $p+q = 98+9 = 107$."),
    "solution": (
      r"<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>"
      r"<p>본 문항은 <b>쌍곡선의 정의($|PF'-PF|=2a$)</b>와 초점 공식($c^2=a^2+b^2$)을 삼각형의 <b>닮음비</b>와 결합하여 두 초점까지의 거리 $d_1, d_2$ 및 점 $P$의 좌표를 구하고, 이를 바탕으로 삼각형의 넓이를 도출하는 기하 종합 문항입니다.</p>"
      r"<h4>📐 [단계별 상세 풀이 전개]</h4>"
      r"<p><b>1) 초점 좌표와 거리차 관계:</b> 주어진 쌍곡선 $\dfrac{x^2}{1}-\dfrac{y^2}{35}=1$ 에서 $a^2=1,\ b^2=35$ 이므로 "
      r"$c^2=a^2+b^2=36 \implies c=6$ 입니다. 따라서 두 초점은 $F(6,0),\ F'(-6,0)$ 이고 $FF'=2c=12$ 입니다. "
      r"또한 $PF'-PF=2$ 에서 $d_2-d_1=2 \implies d_1=d_2-2$ 가 성립합니다.</p>"
      r"<p><b>2) 삼각형 닮음비 적용 및 $d_1, d_2$ 도출:</b> $\triangle QFF' \sim \triangle PFF'$ 의 대응변 비 $\dfrac{d_1+d_2}{12}=\dfrac{12}{d_2}$ 에서 양변에 $12d_2$를 곱하면 $d_2(d_1+d_2)=144$ 입니다.<br>"
      r"여기에 $d_1=d_2-2$를 대입하면 $d_2(2d_2-2)=144 \implies d_2^2-d_2-72=0 \implies (d_2-9)(d_2+8)=0$ 이므로 양수 $d_2=9$, $d_1=7$을 얻습니다.</p>"
      r"<p><b>3) 점 $P$의 좌표 및 $\triangle FPQ$의 넓이:</b> $d_2^2-d_1^2=24x$ 에서 $81-49=32=24x \implies x=\dfrac{4}{3}$ 입니다. "
      r"꼭짓점 $F$를 기준으로 선분 길이와 닮음비를 적용하면 $\triangle FPQ$의 넓이는 $\dfrac{882\sqrt{581}}{81}=\dfrac{98\sqrt{581}}{9}$ 로 약분됩니다.</p>"
      r"<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>"
      r"<p>기약분수 $\dfrac{p}{q}\sqrt{581}$ 에서 $p=98,\ q=9$ (서로소)이므로 구하는 합은 <b>$p+q = 98 + 9 = 107$</b> 입니다.</p>"
    ),
    "solution_en": (
      r"<h4>📋 [Problem Analysis & Core Concepts]</h4>"
      r"<p>This problem integrates the <b>definition of a hyperbola ($|PF'-PF|=2a$)</b> with <b>triangle similarity ($\triangle QFF' \sim \triangle PFF'$)</b> to determine the focal distances $d_1, d_2$, the coordinates of $P$, and the area of $\triangle FPQ$.</p>"
      r"<h4>📐 [Step-by-Step Rigorous Derivation]</h4>"
      r"<p><b>Step 1 (Foci and Distance Difference):</b> From $\dfrac{x^2}{1}-\dfrac{y^2}{35}=1$, we have $a^2=1, b^2=35 \implies c=\sqrt{1+35}=6$, so $F(6,0), F'(-6,0)$ and $FF'=12$. By definition, $d_2 - d_1 = 2 \implies d_1 = d_2 - 2$.</p>"
      r"<p><b>Step 2 (Similarity Ratio):</b> From $\dfrac{d_1+d_2}{12} = \dfrac{12}{d_2}$, we get $d_2(d_1+d_2)=144$. Substituting $d_1=d_2-2$ gives $d_2^2 - d_2 - 72 = (d_2-9)(d_2+8) = 0$. Since $d_2 > 0$, we obtain $d_2 = 9$ and $d_1 = 7$.</p>"
      r"<p><b>Step 3 (Coordinates of $P$ and Area of $\triangle FPQ$):</b> Using $d_2^2 - d_1^2 = 24x$, we find $81 - 49 = 32 = 24x \implies x = \dfrac{4}{3}$. Evaluating the area of $\triangle FPQ$ yields $\dfrac{882\sqrt{581}}{81} = \dfrac{98\sqrt{581}}{9}$.</p>"
      r"<h4>✨ [Conclusion & Key Takeaway]</h4>"
      r"<p>With coprime integers $p = 98$ and $q = 9$, the final answer is <b>$p + q = 107$</b> (<b>Option ①</b>).</p>"
    ),
  },
}

# ===== 검증기 필수 통과 (자동교정 + 경고) =====
data, _rep = verify_quiz.verify_and_fix(data)
if _rep["autofix"]:
    print(">> [검증기 자동교정]")
    for a in _rep["autofix"]:
        print("   +", a)
if _rep["warn"]:
    print(">> [검증기 경고 - 사람(에이전트) 확인 필요]")
    for w in _rep["warn"]:
        print("   !", w)

html = generator.generate_html(data)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
if os.path.exists(os.path.join("board", "private")):
    with open(os.path.join("board", "private", f"{SLUG}.html"), "w", encoding="utf-8") as f:
        f.write(html)
import stitch_screen_builder
stitch_screen_builder.transform_file(OUT)
if os.path.exists(os.path.join("board", "private", f"{SLUG}.html")):
    stitch_screen_builder.transform_file(os.path.join("board", "private", f"{SLUG}.html"))
print(">> 덮어쓰기 완료:", OUT, "(%d bytes)" % len(html))
print(">> 단계 수:", len(data["levels"]))
print(">> 최종 정답:", data["final"]["options"][data["final"]["answer"]-1])
print("REGEN_DONE:", SLUG)
