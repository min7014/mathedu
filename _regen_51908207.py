# -*- coding: utf-8 -*-
"""51908207 (카드 교환 주사위 게임) 수식 LaTeX 교정 + 정교화(자동 업그레이드) 재생성.
- cards: A 3장, B 3장, 초기 A,A,A,B,B,B (자리 1~6)
- 규칙: 주사위 눈 k → k≤5 이면 k번째와 (k+1)번째 교환, k=6 이면 변화 없음
- 4회 반복 후 초기 상태일 때, 3번째 시행 눈이 6일 조건부 확률 = 69/371
- 로컬 LLM 미사용. 에이전트 직접 작성.
"""
import os, importlib.util
import generator

# 검증기(자체 교정+경고) — 모든 문제 생성 시 필수 통과
_spec = importlib.util.spec_from_file_location("verify_quiz", "verify_quiz.py")
verify_quiz = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(verify_quiz)

SLUG = "51908207"
OUT = os.path.join("board", f"{SLUG}.html")

data = {
  "title": "카드 교환 주사위 게임 · 4회 후 초기 상태일 때 3번째가 6일 확률 (기초→심화)",
  "symbols": [
    {"sym": r"카드 교환", "desc": "인접한 두 카드의 위치를 서로 바꾸는 연산. $k$번째와 $(k+1)$번째 카드를 맞바꿈."},
    {"sym": r"주사위 눈 $k$", "desc": r"주사위를 던져 나온 눈. $k \in \{1,2,3,4,5,6\}$. $k \le 5$ 이면 교환, $k=6$ 이면 변화 없음(항등변환)."},
    {"sym": r"상태 $S$", "desc": r"6장 카드의 배치. 초기 상태 $S_0$: A,A,A,B,B,B (자리 1~6). B의 위치로 상태를 표현하기도 함."},
    {"sym": r"조건부 확률 $P(A|B)$", "desc": r"사건 $B$가 일어났을 때 사건 $A$가 일어날 확률. $P(A|B) = \frac{P(A \cap B)}{P(B)} = \frac{n(A \cap B)}{n(B)}$ (동등 가능성일 때)."},
    {"sym": r"대칭성", "desc": r"그래프가 무향(대칭)이면 $N(s \to t,\; m) = N(t \to s,\; m)$. 왕복 경우의 수가 같음."},
  ],
  "levels": [
    {
      "stage": "level1",
      "title": "제1단계 · 초기 상태와 교환 규칙 (가장 기초)",
      "knowledge": r"초기에는 자리 1~3이 A, 자리 4~6이 B입니다. 주사위 눈 $k$에 따라 $k$번째와 $(k+1)$번째 카드를 교환합니다. $k=6$이면 아무 교환도 하지 않습니다.",
      "questions": [
        {"stem": r"초기 상태(A,A,A,B,B,B, 자리 1~6)에서 $k=1$일 때 교환 후 상태는?",
         "options": [r"A,A,A,B,B,B (변화 없음)",
                     r"A,A,B,A,B,B",
                     r"A,B,A,A,B,B",
                     r"B,A,A,A,B,B",
                     r"A,A,A,B,B,B (카드 소멸)"],
         "answer": 1,
         "exp": r"$k=1$은 1번과 2번 카드를 교환하는데, 둘 다 A이므로 변화 없음."},
        {"stem": r"초기 상태에서 $k=3$일 때 교환 후 상태는?",
         "options": [r"A,A,A,B,B,B",
                     r"A,A,B,A,B,B",
                     r"A,B,A,A,B,B",
                     r"B,A,A,A,B,B",
                     r"A,A,A,B,B,A"],
         "answer": 2,
         "exp": r"3번(A)과 4번(B)이 교환되어 A,A,B,A,B,B가 됨. 이것이 $S_1$."},
        {"stem": r"초기 상태에서 $k=6$일 때 교환 후 상태는?",
         "options": [r"A,A,A,B,B,B (변화 없음)",
                     r"A,A,B,A,B,B",
                     r"A,B,A,A,B,B",
                     r"A,A,A,B,B,A",
                     r"카드가 소멸"],
         "answer": 1,
         "exp": r"$k=6$이면 교환 없이 그대로. 즉 $T_6 = \text{id}$ (항등변환)."},
      ],
    },
    {
      "stage": "level2",
      "title": "제2단계 · 상태 변화 분석",
      "knowledge": r"초기 상태 $S_0$(A,A,A,B,B,B)에서 $k=1,2,4,5,6$은 변화 없고(5가지), $k=3$만 상태가 변합니다(1가지). $k=3$일 때 $S_1$(A,A,B,A,B,B)이 됩니다.",
      "questions": [
        {"stem": r"초기 상태 $S_0$에서 상태를 바꾸는 $k$는?",
         "options": [r"$k=1$", r"$k=3$", r"$k=5$", r"$k=6$", r"$k=2$"],
         "answer": 2,
         "exp": r"$k=3$일 때만 3번(A)과 4번(B)이 교환되어 상태가 변함."},
        {"stem": r"$S_0$(A,A,A,B,B,B)에서 한 번 시행으로 $S_1$(A,A,B,A,B,B)이 되는 $k$는?",
         "options": [r"$k=1$", r"$k=2$", r"$k=3$", r"$k=4$", r"$k=6$"],
         "answer": 3,
         "exp": r"$k=3$으로 3번(A)과 4번(B) 교환 → A,A,B,A,B,B ($S_1$)."},
        {"stem": r"$S_0$에서 한 번 시행으로 $S_0$에 머무는 경우의 수는?",
         "options": ["1", "3", "5", "6", "2"],
         "answer": 3,
         "exp": r"$k=1,2,4,5,6$의 5가지 경우 상태 유지."},
      ],
    },
    {
      "stage": "level3",
      "title": "제3단계 · $S_1$에서의 상태 전이",
      "knowledge": r"$S_1$(A,A,B,A,B,B)에서 $k=3$으로 다시 $S_0$로 돌아갑니다. $k=2$는 $S_2$(A,B,A,A,B,B)로, $k=4$는 $S_3$(A,A,B,B,A,B)로 갑니다. $k=1,5,6$은 $S_1$ 유지.",
      "questions": [
        {"stem": r"$S_1$(A,A,B,A,B,B)에서 $S_0$로 돌아가는 $k$는?",
         "options": [r"$k=1$", r"$k=2$", r"$k=3$", r"$k=4$", r"$k=6$"],
         "answer": 3,
         "exp": r"$k=3$으로 3번(B)과 4번(A) 교환 → 다시 A,A,A,B,B,B ($S_0$)."},
        {"stem": r"$S_1$에서 $k=2$일 때 도달하는 상태 $S_2$는?",
         "options": [r"A,A,A,B,B,B",
                     r"A,A,B,A,B,B",
                     r"A,B,A,A,B,B",
                     r"A,A,B,B,A,B",
                     r"B,A,A,A,B,B"],
         "answer": 3,
         "exp": r"2번(A)과 3번(B) 교환 → A,B,A,A,B,B ($S_2$)."},
        {"stem": r"$S_1$에서 $k=4$일 때 도달하는 상태 $S_3$는?",
         "options": [r"A,A,A,B,B,B",
                     r"A,A,B,A,B,B",
                     r"A,B,A,A,B,B",
                     r"A,A,B,B,A,B",
                     r"A,A,B,B,B,A"],
         "answer": 4,
         "exp": r"4번(A)과 5번(B) 교환 → A,A,B,B,A,B ($S_3$)."},
      ],
    },
    {
      "stage": "level4",
      "title": "제4단계 · 2회 시행 후 상태별 경우의 수",
      "knowledge": r"2회 시행 후 $S_0$ 도달: $S_0 \to S_0 \to S_0$ ($5 \times 5 = 25$가지), $S_0 \to S_1 \to S_0$ ($1 \times 1 = 1$가지). 총 $M_2(S_0) = 26$가지. $S_1$ 도달: $S_0 \to S_0 \to S_1$ ($5 \times 1 = 5$), $S_0 \to S_1 \to S_1$ ($1 \times 3 = 3$). 총 $M_2(S_1) = 8$가지.",
      "questions": [
        {"stem": r"2회 시행 후 $S_0$로 돌아오는 경우의 수는?",
         "options": ["25", "26", "30", "36", "1"],
         "answer": 2,
         "exp": r"$S_0 \to S_0 \to S_0$: $5 \times 5 = 25$, $S_0 \to S_1 \to S_0$: $1 \times 1 = 1$, 합계 $26$."},
        {"stem": r"2회 시행 후 $S_1$에 도달하는 경우의 수는?",
         "options": ["5", "8", "1", "26", "0"],
         "answer": 2,
         "exp": r"$S_0 \to S_0 \to S_1$: $5 \times 1 = 5$, $S_0 \to S_1 \to S_1$: $1 \times 3 = 3$, 합계 $8$."},
        {"stem": r"2회 시행 후 $S_2$ 또는 $S_3$에 도달하는 경우의 수는 각각?",
         "options": ["각각 1", "각각 2", "각각 5", "0", "각각 8"],
         "answer": 1,
         "exp": r"$S_0 \to S_1 \to S_2$: $1 \times 1 = 1$, $S_0 \to S_1 \to S_3$: $1 \times 1 = 1$."},
      ],
    },
    {
      "stage": "level5",
      "title": "제5단계 · 4회 시행 후 $S_0$ 도달 총 경우의 수",
      "knowledge": r"4회 후 $S_0$ 도달 경우의 수 = $\sum_s M_2(s) \times N(s \to S_0,\; 2)$. 그래프가 무향(대칭)이므로 $N(s \to S_0,\; 2) = M_2(s)$. 따라서 $N_{\text{total}} = 26^2 + 8^2 + 1^2 + 1^2 = 676 + 64 + 1 + 1 = 742$.",
      "questions": [
        {"stem": r"4회 시행 후 $S_0$로 돌아오는 총 경우의 수는?",
         "options": ["742", "676", "720", "1296", "36"],
         "answer": 1,
         "exp": r"$26^2 + 8^2 + 1^2 + 1^2 = 676 + 64 + 1 + 1 = 742$."},
        {"stem": r"$26^2 + 8^2$ 은?",
         "options": ["676 + 64 = 740", "676 + 64 = 740", "676 + 16 = 692", "52 + 16 = 68", "26 + 8 = 34"],
         "answer": 1,
         "exp": r"$26^2 = 676$, $8^2 = 64$, 합 $740$."},
        {"stem": r"대칭성에 의해 $N(S_1 \to S_0,\; 2) = M_2(S_1)$ 인 이유는?",
         "options": [r"그래프가 무향(대칭)이므로 왕복 경우의 수가 같음",
                     r"항상 성립함",
                     r"$S_1$이 특별해서",
                     r"경우의 수가 무한해서",
                     r"모름"],
         "answer": 1,
         "exp": r"인접 교환은 서로 역변환. $S_1 \to S_0$ 경로 하나마다 $S_0 \to S_1$ 경로가 대응되므로 개수가 같음."},
      ],
    },
    {
      "stage": "level6",
      "title": "제6단계 · 3번째 시행이 6인 조건부 경우의 수",
      "knowledge": r"3번째 시행이 $k=6$이면 $T_6 = \text{id}$ 이므로, 3회 후 상태 = 2회 후 상태 = $S_2$. 4회 만에 $S_0$가 되려면, $S_2$에서 4번째 시행으로 $S_0$에 도달해야 함. 가능한 $S_2$는 $S_0$ (4번째 $k \in \{1,2,4,5,6\}$, 5가지) 또는 $S_1$ (4번째 $k=3$, 1가지).",
      "questions": [
        {"stem": r"3번째 시행이 6이고 4회 후 $S_0$가 되는 경우의 수는?",
         "options": ["138", "26", "8", "130", "742"],
         "answer": 1,
         "exp": r"$S_2=S_0$: $26 \times 5 = 130$, $S_2=S_1$: $8 \times 1 = 8$, 합계 $138$."},
        {"stem": r"$S_2 = S_0$ 일 때, 4번째 시행으로 $S_0$ 유지하는 $k$는 몇 가지?",
         "options": ["1", "3", "5", "6", "2"],
         "answer": 3,
         "exp": r"$k=1,2,4,5,6$의 5가지."},
        {"stem": r"$S_2 = S_1$ 일 때, 4번째 시행으로 $S_0$가 되는 $k$는?",
         "options": ["$k=1$", "$k=2$", "$k=3$", "$k=4$", "$k=6$"],
         "answer": 3,
         "exp": r"$k=3$으로 3번(B)과 4번(A) 교환 → $S_0$ 복귀. 1가지."},
      ],
    },
  ],
  "final": {
    "stem": (r"문자 'A'가 적힌 카드 3장과 문자 'B'가 적힌 카드 3장을 준비하여 "
             r"1번째부터 6번째 자리까지 차례로 A, A, A, B, B, B가 되도록 놓는다. "
             r"한 개의 주사위를 던져 나온 눈의 수를 $k$라 할 때, "
             r"$k \le 5$ 이면 $k$번째 자리의 카드와 $(k+1)$번째 자리의 카드를 교환하고, "
             r"$k = 6$ 이면 카드의 위치를 그대로 둔다. "
             r"이 시행을 4회 반복한 결과 카드가 다시 초기 상태인 A, A, A, B, B, B 순서로 놓여 있을 때, "
             r"3번째 시행에서 나온 눈의 수가 6일 확률을 구하시오."),
    "options": [r"$\dfrac{69}{371}$", r"$\dfrac{1}{6}$", r"$\dfrac{5}{36}$", r"$\dfrac{1}{4}$", r"$\dfrac{1}{3}$"],
    "answer": 1,
    "exp": (r"4회 후 $S_0$ 도달 총 $742$가지 중 3번째가 6인 경우 $138$가지 → "
            r"$\dfrac{138}{742} = \dfrac{69}{371}$."),
    "solution": (
      r"<p><b>풀이.</b></p>"
      r"<p><b>① 상태 정의.</b> 초기 상태 $S_0$: A,A,A,B,B,B (B의 위치: 4,5,6). "
      r"$k=1,2,4,5,6$ 이면 $S_0$ 유지(5가지), $k=3$ 이면 $S_1$(A,A,B,A,B,B)로 변화(1가지).</p>"
      r"<p><b>② $S_1$에서의 전이.</b> $S_1$에서 $k=3$ → $S_0$ 복귀(1가지), "
      r"$k=2$ → $S_2$(A,B,A,A,B,B)(1가지), $k=4$ → $S_3$(A,A,B,B,A,B)(1가지), "
      r"$k=1,5,6$ → $S_1$ 유지(3가지).</p>"
      r"<p><b>③ 2회 후 상태별 도달 수.</b> "
      r"$M_2(S_0) = 5 \times 5 + 1 \times 1 = 26$, "
      r"$M_2(S_1) = 5 \times 1 + 1 \times 3 = 8$, "
      r"$M_2(S_2) = 1 \times 1 = 1$, "
      r"$M_2(S_3) = 1 \times 1 = 1$.</p>"
      r"<p><b>④ 4회 후 $S_0$ 총 경우의 수.</b> 대칭성으로 "
      r"$N_{\text{total}} = 26^2 + 8^2 + 1^2 + 1^2 = 676 + 64 + 1 + 1 = 742$.</p>"
      r"<p><b>⑤ 3번째가 6인 조건부 경우의 수.</b> "
      r"3번째 $k=6$이면 $T_6$은 항등변환. 2회 후 상태 = 3회 후 상태 = $S_2$. "
      r"$S_2 = S_0$ 이면 4번째 $k \in \{1,2,4,5,6\}$(5가지): $26 \times 5 = 130$. "
      r"$S_2 = S_1$ 이면 4번째 $k=3$(1가지): $8 \times 1 = 8$. "
      r"합계 $130 + 8 = 138$.</p>"
      r"<p><b>⑥ 확률.</b> $P = \dfrac{138}{742} = \dfrac{69}{371}$.</p>"
      r"<p><b>정답: $\dfrac{69}{371}$</b></p>"
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
print(">> 덮어쓰기 완료:", OUT, "(%d bytes)" % len(html))
print(">> 단계 수:", len(data["levels"]))
print(">> 최종 정답:", data["final"]["options"][data["final"]["answer"]-1])
print("REGEN_DONE:", SLUG)
