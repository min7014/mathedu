# -*- coding: utf-8 -*-
"""51908207 (카드 교환 주사위 게임) 원자분해 재설계 + 중복보기 교정.

[교정 이력]
- v1: 6단계 — 설계기준(최소 8단계) 미달 + 제5단계 중복 보기("676 + 64 = 740" 2개)
       → 독립 5지선다 위반(동일 보기 2개).
- v2: 23단계 원자분해 — 한 단계 = 한 번의 개념 적용 OR 한 번의 계산.
       중복 보기 제거(유일 정답 + 그럴듯한 오답 4개).
- 정답 진실값: 브루트포스(product 6^4=1296 전수검사) 검증 → 138/742 = 69/371.

규칙: 주사위 눈 k → k≤5이면 k번째와 (k+1)번째 교환, k=6이면 변화 없음.
4회 반복 후 초기 상태일 때, 3번째 시행 눈이 6일 조건부 확률.

로컬 LLM 미사용. 에이전트 직접 작성(sympy/전수검사 검증).
"""
import os, sys, importlib.util
if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
import generator

# 검증기(자체 교정+경고) — 모든 문제 생성 시 필수 통과
_spec = importlib.util.spec_from_file_location("verify_quiz", "verify_quiz.py")
verify_quiz = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(verify_quiz)

SLUG = "51908207"
OUT = os.path.join("board", f"{SLUG}.html")

data = {
  "slug": SLUG,
  "title": "카드 교환 주사위 게임 · 4회 후 초기 상태일 때 3번째가 6일 확률 (기초→심화)",
  "title_en": "Card Swap Dice Game · Conditional Probability of Rolling 6 on the 3rd Trial Given Return to Initial State After 4 Trials",
  "symbols": [
    {"sym": r"카드 교환", "desc": "인접한 두 카드의 위치를 서로 바꾸는 연산. $k$번째와 $(k+1)$번째 카드를 맞바꿈.", "desc_en": "Swapping two adjacent cards at positions $k$ and $k+1$."},
    {"sym": r"주사위 눈 $k$", "desc": r"주사위를 던져 나온 눈. $k \in \{1,2,3,4,5,6\}$. $k \le 5$ 이면 교환, $k=6$ 이면 변화 없음(항등변환).", "desc_en": r"Dice roll $k \in \{1,2,3,4,5,6\}$. Swap if $k \le 5$; no change (identity) if $k=6$."},
    {"sym": r"상태 $S$", "desc": r"6장 카드의 배치. 초기 상태 $S_0$: A,A,A,B,B,B (자리 1~6). B의 위치로 상태를 표현하기도 함.", "desc_en": r"Arrangement of 6 cards. Initial state $S_0$: A,A,A,B,B,B at positions 1 to 6."},
    {"sym": r"조건부 확률 $P(A|B)$", "desc": r"사건 $B$가 일어났을 때 사건 $A$가 일어날 확률. $P(A|B) = \frac{P(A \cap B)}{P(B)} = \frac{n(A \cap B)}{n(B)}$ (동등 가능성일 때).", "desc_en": r"Conditional probability $P(A|B) = \frac{n(A \cap B)}{n(B)}$ under equally likely outcomes."},
    {"sym": r"경우의 수 $M_2(s)$", "desc": r"초기 상태 $S_0$에서 2회 시행하여 상태 $s$에 도달하는 순서쌍 $(k_1, k_2)$의 개수.", "desc_en": r"Number of 2-step sequences $(k_1, k_2)$ reaching state $s$ from $S_0$."},
    {"sym": r"대칭성", "desc": r"그래프가 무향(대칭)이면 $N(s \to t,\; m) = N(t \to s,\; m)$. 왕복 경우의 수가 같음.", "desc_en": r"By symmetry of adjacent swaps, the number of paths from $s$ to $t$ equals that from $t$ to $s$."},
  ],
  "levels": [
    # ============ 제1~4단계: 교환 규칙의 기본 (한 단계 = 한 개념) ============
    {
      "stage": "level1",
      "title": "🔰 제1단계 · [초등 규칙과 사칙연산 연계] 이웃한 카드 자리 바꾸기 규칙 (가장 기초)",
      "title_en": "🔰 Step 1 · [Elementary Rules & Arithmetic Link] Meaning of the Adjacent Card Swap Rule",
      "knowledge": r"초등학교에서 줄을 설 때 바로 옆 친구와 자리를 바꾸는 놀이를 떠올려 봅시다. 주사위 눈 $k$가 나오면, $k \le 5$ 이면 $k$번째 자리와 $(k+1)$번째 자리의 카드를 맞바꿉니다. $k=6$ 이면 아무것도 하지 않습니다.",
      "knowledge_en": r"Just like swapping places with your neighbor in line in elementary school: when dice roll $k \le 5$, swap the $k$-th and $(k+1)$-th cards. When $k=6$, do nothing.",
      "questions": [
        {"stem": r"초등학교 규칙 찾기: 주사위 눈이 $k \le 5$ 일 때 시행은 무엇을 하는가?",
         "stem_en": r"Elementary rule check: What operation is performed when the dice roll satisfies $k \le 5$?",
         "options": [r"$k$번째와 $(k+1)$번째 카드를 교환",
                     r"$k$번째 카드를 제거",
                     r"$k$번째와 $(k+2)$번째 카드를 교환",
                     r"모든 카드를 뒤집음",
                     r"아무 일도 하지 않음"],
         "answer": 1,
         "exp": r"$k \le 5$ 이면 인접한 $k$번째와 $(k+1)$번째 카드를 맞바꿈.",
         "exp_en": r"When $k \le 5$, swap the adjacent $k$-th and $(k+1)$-th cards."},
        {"stem": r"$k=6$ 일 때 시행은 무엇을 하는가?",
         "options": [r"6번째와 1번째 카드를 교환",
                     r"아무 일도 하지 않음(항등)",
                     r"모든 카드를 제자리로 되돌림",
                     r"5번째와 6번째 카드를 교환",
                     r"주사위를 한 번 더 던짐"],
         "answer": 2,
         "exp": r"$k=6$이면 교환하지 않음. 이를 항등변환 $T_6 = \text{id}$ 라 함."},
        {"stem": r"같은 문자가 적힌 두 카드를 교환하면 상태는 어떻게 되는가?",
         "options": [r"문자가 바뀜",
                     r"상태가 변하지 않음",
                     r"카드가 소멸",
                     r"다른 상태로 이동",
                     r"알 수 없음"],
         "answer": 2,
         "exp": r"A와 A를 맞바꿔도 눈에 보이는 배치는 그대로. 상태 변화 없음."},
      ],
    },
    {
      "stage": "level2",
      "title": "제2단계 · 초기 상태에서 $k=1$일 때",
      "knowledge": r"초기 상태 $S_0$: A,A,A,B,B,B (자리 1~6). $k=1$이면 1번(A)과 2번(A)을 교환합니다.",
      "questions": [
        {"stem": r"초기 상태(A,A,A,B,B,B)에서 $k=1$일 때 교환 후 상태는?",
         "options": [r"A,A,A,B,B,B (변화 없음)",
                     r"A,A,B,A,B,B",
                     r"A,B,A,A,B,B",
                     r"B,A,A,A,B,B",
                     r"A,A,A,B,B,B (카드 소멸)"],
         "answer": 1,
         "exp": r"$k=1$은 1번과 2번 카드를 교환하는데, 둘 다 A이므로 변화 없음."},
        {"stem": r"$k=1$에서 교환되는 두 카드의 문자는?",
         "options": [r"A와 B", r"B와 B", r"A와 A", r"A와 C", r"B와 A"],
         "answer": 3,
         "exp": r"1번 자리 A, 2번 자리 A. 같은 문자끼리라 상태 불변."},
      ],
    },
    {
      "stage": "level3",
      "title": "제3단계 · 초기 상태에서 $k=3$일 때 → $S_1$",
      "knowledge": r"초기 상태에서 $k=3$이면 3번(A)과 4번(B)이 교환되어 A,A,B,A,B,B가 됩니다. 이 상태를 $S_1$이라 합시다.",
      "questions": [
        {"stem": r"초기 상태에서 $k=3$일 때 교환 후 상태는?",
         "options": [r"A,A,A,B,B,B",
                     r"A,A,B,A,B,B",
                     r"A,B,A,A,B,B",
                     r"B,A,A,A,B,B",
                     r"A,A,A,B,B,A"],
         "answer": 2,
         "exp": r"3번(A)과 4번(B)이 교환되어 A,A,B,A,B,B가 됨. 이것이 $S_1$."},
        {"stem": r"$k=3$에서 교환되는 두 카드의 문자는?",
         "options": [r"A와 A", r"B와 B", r"A와 B", r"A와 C", r"B와 C"],
         "answer": 3,
         "exp": r"3번 A, 4번 B. 다른 문자끼리라 상태가 실제로 변함."},
        {"stem": r"초기 상태에서 $k=3$으로 도달한 상태를 무엇이라 부르는가?",
         "options": [r"$S_0$", r"$S_1$", r"$S_2$", r"$S_3$", r"$S_4$"],
         "answer": 2,
         "exp": r"새 상태에 이름 $S_1$ 을 붙임(기호의미 선행)."},
      ],
    },
    {
      "stage": "level4",
      "title": "제4단계 · 초기 상태에서 $k=6$일 때",
      "knowledge": r"$k=6$이면 교환 없이 그대로입니다. 초기 상태 $S_0$는 $k=6$에도 변하지 않습니다.",
      "questions": [
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
    # ============ 제5단계: 초기 상태 전이 정리 (개념 1개) ============
    {
      "stage": "level5",
      "title": "제5단계 · 초기 상태 $S_0$의 전이 정리",
      "knowledge": r"초기 상태 $S_0$에서 $k=1,2,4,5,6$은 변화 없고(5가지), $k=3$만 $S_1$로 상태가 변합니다(1가지).",
      "questions": [
        {"stem": r"초기 상태 $S_0$에서 상태를 바꾸는 $k$는?",
         "options": [r"$k=1$", r"$k=3$", r"$k=5$", r"$k=6$", r"$k=2$"],
         "answer": 2,
         "exp": r"$k=3$일 때만 3번(A)과 4번(B)이 교환되어 상태가 변함."},
        {"stem": r"초기 상태 $S_0$에서 한 번 시행으로 $S_0$에 머무는 경우의 수는?",
         "options": [r"1", r"3", r"5", r"6", r"2"],
         "answer": 3,
         "exp": r"$k=1,2,4,5,6$의 5가지 경우 상태 유지."},
        {"stem": r"초기 상태 $S_0$에서 한 번 시행으로 $S_1$에 도달하는 경우의 수는?",
         "options": [r"1", r"3", r"5", r"6", r"0"],
         "answer": 1,
         "exp": r"$k=3$ 한 가지."},
      ],
    },
    # ============ 제6~9단계: S1 전이 (한 단계 = 한 전이) ============
    {
      "stage": "level6",
      "title": "제6단계 · $S_1$에서 $S_0$로 돌아가기",
      "knowledge": r"$S_1$(A,A,B,A,B,B)에서 $k=3$이면 3번(B)과 4번(A)이 교환되어 다시 $S_0$(A,A,A,B,B,B)가 됩니다.",
      "questions": [
        {"stem": r"$S_1$(A,A,B,A,B,B)에서 $S_0$로 돌아가는 $k$는?",
         "options": [r"$k=1$", r"$k=2$", r"$k=3$", r"$k=4$", r"$k=6$"],
         "answer": 3,
         "exp": r"$k=3$으로 3번(B)과 4번(A) 교환 → 다시 A,A,A,B,B,B ($S_0$)."},
        {"stem": r"$S_1$에서 $S_0$로 가는 경우의 수는?",
         "options": [r"1", r"3", r"5", r"6", r"0"],
         "answer": 1,
         "exp": r"$k=3$ 한 가지뿐."},
      ],
    },
    {
      "stage": "level7",
      "title": "제7단계 · $S_1$에서 $k=2$일 때 → $S_2$",
      "knowledge": r"$S_1$에서 $k=2$이면 2번(A)과 3번(B)이 교환되어 A,B,A,A,B,B가 됩니다. 이 상태를 $S_2$라 합시다.",
      "questions": [
        {"stem": r"$S_1$에서 $k=2$일 때 도달하는 상태 $S_2$는?",
         "options": [r"A,A,A,B,B,B",
                     r"A,A,B,A,B,B",
                     r"A,B,A,A,B,B",
                     r"A,A,B,B,A,B",
                     r"B,A,A,A,B,B"],
         "answer": 3,
         "exp": r"2번(A)과 3번(B) 교환 → A,B,A,A,B,B ($S_2$)."},
        {"stem": r"$S_1$에서 $k=2$로 도달한 상태를 무엇이라 부르는가?",
         "options": [r"$S_0$", r"$S_1$", r"$S_2$", r"$S_3$", r"$S_4$"],
         "answer": 3,
         "exp": r"두 번째로 새로 만나는 상태에 $S_2$ 이름 부여."},
      ],
    },
    {
      "stage": "level8",
      "title": "제8단계 · $S_1$에서 $k=4$일 때 → $S_3$",
      "knowledge": r"$S_1$에서 $k=4$이면 4번(A)과 5번(B)이 교환되어 A,A,B,B,A,B가 됩니다. 이 상태를 $S_3$라 합시다.",
      "questions": [
        {"stem": r"$S_1$에서 $k=4$일 때 도달하는 상태 $S_3$는?",
         "options": [r"A,A,A,B,B,B",
                     r"A,A,B,A,B,B",
                     r"A,B,A,A,B,B",
                     r"A,A,B,B,A,B",
                     r"A,A,B,B,B,A"],
         "answer": 4,
         "exp": r"4번(A)과 5번(B) 교환 → A,A,B,B,A,B ($S_3$)."},
        {"stem": r"$S_1$에서 $k=4$로 도달한 상태를 무엇이라 부르는가?",
         "options": [r"$S_0$", r"$S_1$", r"$S_2$", r"$S_3$", r"$S_4$"],
         "answer": 4,
         "exp": r"세 번째로 새로 만나는 상태에 $S_3$ 이름 부여."},
      ],
    },
    {
      "stage": "level9",
      "title": "제9단계 · $S_1$에서 머무는 경우의 수",
      "knowledge": r"$S_1$에서 $k=1,5,6$은 변화 없어 $S_1$에 머무릅니다(3가지). 정리하면 $S_1$의 한 번 시행 전이는: $S_0$ 1가지, $S_2$ 1가지, $S_3$ 1가지, $S_1$ 유지 3가지.",
      "questions": [
        {"stem": r"$S_1$에서 한 번 시행으로 $S_1$에 머무는 경우의 수는?",
         "options": [r"1", r"3", r"5", r"6", r"2"],
         "answer": 2,
         "exp": r"$k=1,5,6$의 3가지 경우 상태 유지."},
        {"stem": r"$S_1$에서 한 번 시행의 전이 경우의 수를 모두 합하면?",
         "options": [r"3", r"4", r"5", r"6", r"8"],
         "answer": 4,
         "exp": r"$S_0$ 1가지 + $S_2$ 1가지 + $S_3$ 1가지 + $S_1$ 유지 3가지 = 6가지. 주사위 눈은 항상 6가지."},
      ],
    },
    # ============ 제10~13단계: M2(S0) 계산 (한 단계 = 한 계산) ============
    {
      "stage": "level10",
      "title": r"제10단계 · 2회 후 $S_0$ 도달 — 경로 ① ($S_0 \to S_0 \to S_0$)",
      "knowledge": r"2회 시행 후 $S_0$에 도달하는 경로는 두 갈래입니다. 첫 갈래: $S_0 \to S_0 \to S_0$. 첫 시행에 $S_0$ 유지가 5가지, 둘째에도 5가지이므로 $5 \times 5$ 가지.",
      "questions": [
        {"stem": r"$S_0 \to S_0 \to S_0$ 경로의 수 $5 \times 5$ 은?",
         "options": [r"10", r"25", r"5", r"30", r"36"],
         "answer": 2,
         "exp": r"$5 \times 5 = 25$."},
        {"stem": r"2회 시행 후 $S_0$ 도달 경로의 첫 갈래가 $S_0 \to S_0 \to S_0$ 인 이유는?",
         "options": [r"두 시행 모두 상태를 유지하는 눈을 고르면 됨",
                     r"두 시행 모두 $k=3$이어야 함",
                     r"두 시행 모두 $k=6$이어야 함",
                     r"한 시행만 하면 됨",
                     r"경로가 존재하지 않음"],
         "answer": 1,
         "exp": r"2회 내내 $S_0$에 머무르면 2회 후에도 $S_0$. 각 5가지 눈 선택."},
      ],
    },
    {
      "stage": "level11",
      "title": r"제11단계 · 2회 후 $S_0$ 도달 — 경로 ② ($S_0 \to S_1 \to S_0$)",
      "knowledge": r"둘째 갈래: $S_0 \to S_1 \to S_0$. 첫 시행에 $S_1$로 가는 눈은 $k=3$ (1가지), 둘째에 $S_1 \to S_0$ 도 $k=3$ (1가지)이므로 $1 \times 1$ 가지.",
      "questions": [
        {"stem": r"$S_0 \to S_1 \to S_0$ 경로의 수 $1 \times 1$ 은?",
         "options": [r"0", r"1", r"2", r"3", r"5"],
         "answer": 2,
         "exp": r"$1 \times 1 = 1$."},
        {"stem": r"$S_0 \to S_1$ 로 가는 눈과 $S_1 \to S_0$ 로 가는 눈은 각각?",
         "options": [r"둘 다 $k=3$", r"둘 다 $k=1$", r"$k=3$ 과 $k=1$", r"$k=6$ 과 $k=3$", r"둘 다 $k=6$"],
         "answer": 1,
         "exp": r"3번(A)과 4번(B)을 맞바꾸는 교환은 두 방향 모두 $k=3$으로 가능. 역변환이 같은 눈."},
      ],
    },
    {
      "stage": "level12",
      "title": "제12단계 · $M_2(S_0)$ 합산 (계산)",
      "knowledge": r"두 갈래를 더하면 $M_2(S_0) = 25 + 1 = 26$ 가지. 이는 초기 상태에서 2회 시행하여 $S_0$에 도달하는 경우의 수입니다.",
      "questions": [
        {"stem": r"2회 시행 후 $S_0$로 돌아오는 경우의 수 $M_2(S_0)$ 는?",
         "options": [r"25", r"26", r"30", r"36", r"1"],
         "answer": 2,
         "exp": r"$S_0 \to S_0 \to S_0$: $5 \times 5 = 25$, $S_0 \to S_1 \to S_0$: $1 \times 1 = 1$, 합계 $26$."},
        {"stem": r"$25 + 1$ 을 계산하면?",
         "options": [r"24", r"26", r"27", r"30", r"36"],
         "answer": 2,
         "exp": r"$25 + 1 = 26$."},
      ],
    },
    {
      "stage": "level13",
      "title": "제13단계 · $M_2(S_1)$ 계산 (두 갈래 합산)",
      "knowledge": r"2회 후 $S_1$ 도달: $S_0 \to S_0 \to S_1$ ($5 \times 1 = 5$), $S_0 \to S_1 \to S_1$ ($1 \times 3 = 3$). 총 $M_2(S_1) = 8$가지.",
      "questions": [
        {"stem": r"$S_0 \to S_0 \to S_1$ 경로의 수 $5 \times 1$ 은?",
         "options": [r"1", r"5", r"6", r"3", r"8"],
         "answer": 2,
         "exp": r"$5 \times 1 = 5$."},
        {"stem": r"$S_0 \to S_1 \to S_1$ 경로의 수 $1 \times 3$ 은?",
         "options": [r"1", r"3", r"5", r"6", r"8"],
         "answer": 2,
         "exp": r"$1 \times 3 = 3$."},
        {"stem": r"2회 시행 후 $S_1$에 도달하는 경우의 수 $M_2(S_1)$ 는?",
         "options": [r"5", r"8", r"1", r"26", r"0"],
         "answer": 2,
         "exp": r"$S_0 \to S_0 \to S_1$: $5 \times 1 = 5$, $S_0 \to S_1 \to S_1$: $1 \times 3 = 3$, 합계 $8$."},
      ],
    },
    # ============ 제14~15단계: M2(S2), M2(S3) ============
    {
      "stage": "level14",
      "title": "제14단계 · $M_2(S_2)$ 계산",
      "knowledge": r"2회 후 $S_2$에 도달하려면 $S_0 \to S_1 \to S_2$ 밖에 없습니다. 첫 시행 $k=3$ (1가지), 둘째 시행 $k=2$ (1가지).",
      "questions": [
        {"stem": r"2회 시행 후 $S_2$에 도달하는 경우의 수 $M_2(S_2)$ 는?",
         "options": [r"0", r"1", r"2", r"5", r"8"],
         "answer": 2,
         "exp": r"$S_0 \to S_1 \to S_2$: $1 \times 1 = 1$."},
        {"stem": r"$S_0 \to S_1 \to S_2$ 에서 둘째 시행의 눈은?",
         "options": [r"$k=1$", r"$k=2$", r"$k=3$", r"$k=4$", r"$k=6$"],
         "answer": 2,
         "exp": r"$S_1$에서 $k=2$로 $S_2$ 도달."},
      ],
    },
    {
      "stage": "level15",
      "title": "제15단계 · $M_2(S_3)$ 계산",
      "knowledge": r"2회 후 $S_3$에 도달하려면 $S_0 \to S_1 \to S_3$ 밖에 없습니다. 첫 시행 $k=3$ (1가지), 둘째 시행 $k=4$ (1가지).",
      "questions": [
        {"stem": r"2회 시행 후 $S_3$에 도달하는 경우의 수 $M_2(S_3)$ 는?",
         "options": [r"0", r"1", r"2", r"5", r"8"],
         "answer": 2,
         "exp": r"$S_0 \to S_1 \to S_3$: $1 \times 1 = 1$."},
        {"stem": r"$S_0 \to S_1 \to S_3$ 에서 둘째 시행의 눈은?",
         "options": [r"$k=1$", r"$k=2$", r"$k=3$", r"$k=4$", r"$k=6$"],
         "answer": 4,
         "exp": r"$S_1$에서 $k=4$로 $S_3$ 도달."},
      ],
    },
    # ============ 제16단계: 대칭성 개념 ============
    {
      "stage": "level16",
      "title": "제16단계 · 대칭성 — 왕복 경우의 수",
      "knowledge": r"인접 교환은 서로 역변환입니다. $s \to t$ 경로 하나마다 $t \to s$ 경로가 대응하므로, 무향 그래프에서 $N(s \to t,\; 2) = N(t \to s,\; 2) = M_2(s)$.",
      "questions": [
        {"stem": r"대칭성에 의해 $N(S_1 \to S_0,\; 2) = M_2(S_1)$ 인 이유는?",
         "options": [r"그래프가 무향(대칭)이므로 왕복 경우의 수가 같음",
                     r"항상 성립함",
                     r"$S_1$이 특별해서",
                     r"경우의 수가 무한해서",
                     r"우연히 같음"],
         "answer": 1,
         "exp": r"인접 교환은 서로 역변환. $S_1 \to S_0$ 경로 하나마다 $S_0 \to S_1$ 경로가 대응되므로 개수가 같음."},
        {"stem": r"대칭성에 의해 $N(S_0 \to S_0,\; 2)$ 의 값은?",
         "options": [r"5", r"8", r"26", r"1", r"742"],
         "answer": 3,
         "exp": r"$N(S_0 \to S_0,\; 2) = M_2(S_0) = 26$."},
      ],
    },
    # ============ 제17~18단계: 4회 후 S0 총 경우의 수 (한 단계 = 한 계산) ============
    {
      "stage": "level17",
      "title": "제17단계 · 4회 후 $S_0$ 총 경우의 수 — 제곱 계산",
      "knowledge": r"4회 후 $S_0$ 도달 경우의 수 = $\sum_s M_2(s) \times N(s \to S_0,\; 2)$. 대칭성으로 $N(s \to S_0,\; 2) = M_2(s)$ 이므로 각 항은 제곱이 됩니다: $26^2 + 8^2 + 1^2 + 1^2$.",
      "questions": [
        {"stem": r"$26^2$ 은?",
         "options": [r"52", r"676", r"260", r"625", r"729"],
         "answer": 2,
         "exp": r"$26 \times 26 = 676$."},
        {"stem": r"$8^2$ 은?",
         "options": [r"16", r"32", r"64", r"8", r"128"],
         "answer": 3,
         "exp": r"$8 \times 8 = 64$."},
        {"stem": r"$1^2$ 은?",
         "options": [r"0", r"1", r"2", r"11", r"12"],
         "answer": 2,
         "exp": r"$1 \times 1 = 1$."},
      ],
    },
    {
      "stage": "level18",
      "title": "제18단계 · 4회 후 $S_0$ 총 경우의 수 — 합산",
      "knowledge": r"네 제곱을 더합니다: $676 + 64 + 1 + 1$. 두 번 더하면 $740 + 2 = 742$.",
      "questions": [
        {"stem": r"$676 + 64$ 은?",
         "options": [r"730", r"740", r"742", r"720", r"760"],
         "answer": 2,
         "exp": r"$676 + 64 = 740$."},
        {"stem": r"$740 + 1 + 1$ 은?",
         "options": [r"740", r"741", r"742", r"743", r"744"],
         "answer": 3,
         "exp": r"$740 + 1 + 1 = 742$."},
        {"stem": r"4회 시행 후 $S_0$로 돌아오는 총 경우의 수는?",
         "options": [r"742", r"676", r"720", r"1296", r"36"],
         "answer": 1,
         "exp": r"$26^2 + 8^2 + 1^2 + 1^2 = 676 + 64 + 1 + 1 = 742$."},
      ],
    },
    # ============ 제19단계: 3번째가 6이면 항등 (개념) ============
    {
      "stage": "level19",
      "title": "제19단계 · 3번째 시행이 6이면 항등",
      "knowledge": r"3번째 시행이 $k=6$이면 $T_6 = \text{id}$ 이므로, 3회 후 상태 = 2회 후 상태 그대로입니다. 따라서 4회 만에 $S_0$가 되려면, 2회 후 상태에서 4번째 시행으로 $S_0$에 도달해야 합니다.",
      "questions": [
        {"stem": r"3번째 시행이 $k=6$일 때, 3회 후 상태는?",
         "options": [r"2회 후 상태와 같음",
                     r"항상 $S_0$",
                     r"항상 $S_1$",
                     r"2회 후 상태의 역",
                     r"알 수 없음"],
         "answer": 1,
         "exp": r"$T_6 = \text{id}$ 이므로 3회 후 = 2회 후."},
        {"stem": r"3번째가 6이고 4회 후 $S_0$가 되려면, 4번째 시행은 무엇을 만족해야 하는가?",
         "options": [r"2회 후 상태를 $S_0$로 만듦",
                     r"2회 후 상태를 $S_1$로 만듦",
                     r"2회 후 상태를 유지",
                     r"3회 후 상태를 유지",
                     r"아무 조건 없음"],
         "answer": 1,
         "exp": r"4번째가 $S_0$에 도달해야 최종 $S_0$."},
      ],
    },
    # ============ 제20~21단계: 조건부 경우의 수 (한 단계 = 한 계산) ============
    {
      "stage": "level20",
      "title": "제20단계 · 조건부 경우의 수 — 2회 후 $S_0$ 분기",
      "knowledge": r"2회 후 상태가 $S_0$이면 4번째 시행으로 $S_0$을 유지해야 합니다. $S_0$ 유지 눈은 $k \in \{1,2,4,5,6\}$ (5가지). 경우의 수 = $M_2(S_0) \times 5 = 26 \times 5$.",
      "questions": [
        {"stem": r"2회 후 상태가 $S_0$일 때, 4번째 시행으로 $S_0$ 유지하는 $k$는 몇 가지?",
         "options": [r"1", r"3", r"5", r"6", r"2"],
         "answer": 3,
         "exp": r"$k=1,2,4,5,6$의 5가지."},
        {"stem": r"$M_2(S_0) \times 5 = 26 \times 5$ 은?",
         "options": [r"120", r"130", r"138", r"26", r"125"],
         "answer": 2,
         "exp": r"$26 \times 5 = 130$."},
      ],
    },
    {
      "stage": "level21",
      "title": "제21단계 · 조건부 경우의 수 — 2회 후 $S_1$ 분기",
      "knowledge": r"2회 후 상태가 $S_1$이면 4번째 시행으로 $S_0$에 도달해야 합니다. $S_1 \to S_0$ 눈은 $k=3$ (1가지). 경우의 수 = $M_2(S_1) \times 1 = 8 \times 1$.",
      "questions": [
        {"stem": r"2회 후 상태가 $S_1$일 때, 4번째 시행으로 $S_0$가 되는 $k$는?",
         "options": [r"$k=1$", r"$k=2$", r"$k=3$", r"$k=4$", r"$k=6$"],
         "answer": 3,
         "exp": r"$k=3$으로 3번(B)과 4번(A) 교환 → $S_0$ 복귀. 1가지."},
        {"stem": r"$M_2(S_1) \times 1 = 8 \times 1$ 은?",
         "options": [r"5", r"8", r"26", r"1", r"138"],
         "answer": 2,
         "exp": r"$8 \times 1 = 8$."},
        {"stem": r"2회 후 상태가 $S_2$ 또는 $S_3$일 때, 4번째 시행으로 $S_0$에 도달하는 경우의 수는?",
         "options": [r"각각 1", r"각각 5", r"0", r"각각 3", r"각각 8"],
         "answer": 3,
         "exp": r"$S_2$, $S_3$에서 한 번의 교환으로 $S_0$에 도달할 수 없음. 기여 0."},
      ],
    },
    # ============ 제22단계: 조건부 합산 ============
    {
      "stage": "level22",
      "title": "제22단계 · 조건부 경우의 수 합산",
      "knowledge": r"두 분기의 경우의 수를 더합니다: $130 + 8$. 3번째 시행이 6이고 4회 후 $S_0$인 경우의 수가 됩니다.",
      "questions": [
        {"stem": r"3번째 시행이 6이고 4회 후 $S_0$가 되는 경우의 수는?",
         "options": [r"138", r"26", r"8", r"130", r"742"],
         "answer": 1,
         "exp": r"$S_2=S_0$: $26 \times 5 = 130$, $S_2=S_1$: $8 \times 1 = 8$, 합계 $138$."},
        {"stem": r"$130 + 8$ 을 계산하면?",
         "options": [r"128", r"136", r"138", r"140", r"142"],
         "answer": 3,
         "exp": r"$130 + 8 = 138$."},
      ],
    },
    # ============ 제23단계: 조건부 확률 (최종) ============
    {
      "stage": "level23",
      "title": "제23단계 · 조건부 확률 도출 (최종)",
      "knowledge": r"조건부 확률 $P = \dfrac{138}{742}$. 분자·분모를 2로 약분하면 $\dfrac{69}{371}$.",
      "questions": [
        {"stem": r"조건부 확률 $P = \dfrac{138}{742}$ 을 약분하면?",
         "options": [r"$\dfrac{69}{371}$", r"$\dfrac{138}{371}$", r"$\dfrac{69}{742}$", r"$\dfrac{23}{371}$", r"$\dfrac{1}{6}$"],
         "answer": 1,
         "exp": r"$\gcd(138, 742) = 2$ 이므로 $\dfrac{138}{742} = \dfrac{69}{371}$."},
        {"stem": r"$\gcd(138, 742)$ 은?",
         "options": [r"1", r"2", r"3", r"6", r"23"],
         "answer": 2,
         "exp": r"$138 = 2 \times 69$, $742 = 2 \times 371$. $69 = 3 \times 23$, $371 = 7 \times 53$ 으로 더 이상 공약수 없음."},
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
    "stem_en": (r"Three 'A' cards and three 'B' cards are placed in positions 1 to 6 as A, A, A, B, B, B. "
                r"A fair die is rolled to get $k$: if $k \le 5$, the $k$-th and $(k+1)$-th cards are swapped; "
                r"if $k = 6$, the cards remain in place. "
                r"Given that after 4 trials the cards return to the initial state A, A, A, B, B, B, "
                r"find the conditional probability that the 3rd roll was 6."),
    "options": [r"$\dfrac{69}{371}$", r"$\dfrac{1}{6}$", r"$\dfrac{5}{36}$", r"$\dfrac{1}{4}$", r"$\dfrac{1}{3}$"],
    "answer": 1,
    "exp": (r"4회 후 $S_0$ 도달 총 $742$가지 중 3번째가 6인 경우 $138$가지 → "
            r"$\dfrac{138}{742} = \dfrac{69}{371}$."),
    "exp_en": (r"Among $742$ total 4-step paths returning to $S_0$, $138$ have $k_3=6$, giving $\dfrac{138}{742} = \dfrac{69}{371}$."),
    "solution": (
      r"<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>"
      r"<p>본 문항은 주사위 눈에 따른 인접 카드 교환 규칙을 <b>상태 전이 그래프(State Transition Graph)</b>로 모델링하고, 2회 시행 후 도달 가능한 상태별 경우의 수 $M_2(s)$와 대칭성을 활용하여 <b>조건부 확률</b>을 구하는 고난도 확률 문항입니다.</p>"
      r"<h4>📐 [단계별 상세 풀이 전개]</h4>"
      r"<p><b>① 상태 정의 및 1회 전이 분석:</b> 초기 상태 $S_0$: A,A,A,B,B,B (B의 위치: 4,5,6). "
      r"$k=1,2,4,5,6$ 이면 같은 문자끼리 교환하거나 정지하므로 $S_0$ 유지(5가지), $k=3$ 이면 3번(A)과 4번(B)이 교환되어 $S_1$(A,A,B,A,B,B)로 변화(1가지)합니다.</p>"
      r"<p><b>② $S_1$에서의 전이 분석:</b> $S_1$에서 $k=3$ → $S_0$ 복귀(1가지), "
      r"$k=2$ → $S_2$(A,B,A,A,B,B)(1가지), $k=4$ → $S_3$(A,A,B,B,A,B)(1가지), "
      r"$k=1,5,6$ → $S_1$ 유지(3가지)입니다.</p>"
      r"<p><b>③ 2회 시행 후 상태별 도달 경우의 수 $M_2(s)$:</b><br>"
      r"• $M_2(S_0) = 5 \times 5 + 1 \times 1 = 26$<br>"
      r"• $M_2(S_1) = 5 \times 1 + 1 \times 3 = 8$<br>"
      r"• $M_2(S_2) = 1 \times 1 = 1$, $M_2(S_3) = 1 \times 1 = 1$</p>"
      r"<p><b>④ 4회 후 $S_0$ 복귀 총 경우의 수 (분모):</b> 인접 교환의 가역성(대칭성)에 의해 $s \to S_0$의 2회 경로 수도 $M_2(s)$와 같으므로:<br>"
      r"$$n(B) = 26^2 + 8^2 + 1^2 + 1^2 = 676 + 64 + 1 + 1 = 742$$</p>"
      r"<p><b>⑤ 3번째 눈이 6이고 4회 후 $S_0$인 경우의 수 (분자):</b> "
      r"3번째 시행이 $k=6$이면 상태가 그대로 유지되므로(2회 후 상태 = 3회 후 상태), 4번째 시행 한 번으로 $S_0$에 도달해야 합니다.<br>"
      r"• 2회 후 $S_0$일 때: 4번째에 $S_0$ 유지(5가지) $\implies 26 \times 5 = 130$<br>"
      r"• 2회 후 $S_1$일 때: 4번째에 $k=3$으로 복귀(1가지) $\implies 8 \times 1 = 8$<br>"
      r"• 2회 후 $S_2, S_3$일 때: 1회 시행으로 $S_0$ 복귀 불가(0가지)<br>"
      r"따라서 $n(A \cap B) = 130 + 8 = 138$ 입니다.</p>"
      r"<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>"
      r"<p>구하는 조건부 확률은 $P(A|B) = \dfrac{138}{742} = \dfrac{69}{371}$ 이며, 정답은 <b>①번 ($\dfrac{69}{371}$)</b>입니다.</p>"
    ),
    "solution_en": (
      r"<h4>📋 [Problem Analysis & Core Concepts]</h4>"
      r"<p>This problem models adjacent card swaps driven by dice rolls as a <b>symmetric state transition graph</b> and computes the conditional probability using 2-step path counts $M_2(s)$.</p>"
      r"<h4>📐 [Step-by-Step Rigorous Derivation]</h4>"
      r"<p><b>Step 1 (Transitions from $S_0$ and $S_1$):</b> From $S_0$ (A,A,A,B,B,B), $k \in \{1,2,4,5,6\}$ keeps $S_0$ (5 ways), while $k=3$ moves to $S_1$ (A,A,B,A,B,B) (1 way). From $S_1$, $k=3$ returns to $S_0$ (1 way), $k=2 \to S_2$ (1 way), $k=4 \to S_3$ (1 way), and $k \in \{1,5,6\}$ stays at $S_1$ (3 ways).</p>"
      r"<p><b>Step 2 (2-Step Path Counts $M_2(s)$):</b><br>"
      r"$M_2(S_0) = 5^2 + 1^2 = 26$, $M_2(S_1) = 5(1) + 1(3) = 8$, $M_2(S_2) = 1$, $M_2(S_3) = 1$.</p>"
      r"<p><b>Step 3 (Total 4-Step Return Paths & Favorable Paths):</b><br>"
      r"By symmetry, total ways to return to $S_0$ in 4 steps is $26^2 + 8^2 + 1^2 + 1^2 = 742$.<br>"
      r"If the 3rd roll is $k_3=6$ (identity), the 4th roll must transition directly from the 2nd-step state to $S_0$: $26 \times 5 + 8 \times 1 = 130 + 8 = 138$.</p>"
      r"<h4>✨ [Conclusion & Key Takeaway]</h4>"
      r"<p>The conditional probability is $P = \dfrac{138}{742} = \dfrac{69}{371}$ (<b>Option ①</b>).</p>"
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
