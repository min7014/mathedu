# -*- coding: utf-8 -*-
"""
mathteacher.py
==============
mathedu 수석 수학 교사 에이전트 (MathTeacher) CLI 및 코어 수학교육학 엔진 (v2.5 Continuous Evolution).
- 16,548개 전 연도·전 학년 수학 기출 및 디딤돌 퀴즈 조회·검색·해설·검증 수행
- 초등학생 눈높이 무장벽 디딤돌(0단계 기호 번역 + 1~5단계 수식 유도) 및 시각적 SVG 도식화 해설 생성
- 4대 수학교육 발전 모듈 상시 진화 엔진 (assets/mathteacher_pedagogy_engine.json 연동):
  1) 🌳 초·중·고 수직 계통성 개념 계보 트리 (Vertical Concept Genealogy Map)
  2) 🧭 폴리아(Pólya) '조건 ➔ 제1보조선·발상' 1초 번역 사전 (Heuristic Dictionary)
  3) 🔬 오개념 백신 & 반례 실험실 (Misconception Vaccine & Counterexample Lab)
  4) 👩‍🏫 교사용 5분 탐구 수업 시나리오 & 발문 런처 (5-Minute Inquiry Lesson Launcher)
"""

import os
import sys
import re
import json
import subprocess
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOARD_DIR = os.path.join(BASE_DIR, "board")
SHARDS_DIR = os.path.join(BOARD_DIR, "archive_shards")
INDEX_JSON = os.path.join(BOARD_DIR, "index.json")
CATALOG_JSON = os.path.join(BOARD_DIR, "archive_catalog.json")
PEDAGOGY_JSON = os.path.join(BASE_DIR, "assets", "mathteacher_pedagogy_engine.json")
MIN7014_DEEP_JSON = os.path.join(BASE_DIR, "assets", "min7014_deep_knowledge.json")
VIDEO_CATALOG_JSON = os.path.join(BASE_DIR, "video_lectures", "catalog.json")


# 지속 확장용 심층 수학교육학 큐레이션 뱅크 (min7014.github.io 16대 영역 기반)
CONTINUOUS_PEDAGOGY_EXPANSION_POOL = {
    "verticalGenealogy": [
        {
            "id": "genealogy-circle-inscribed",
            "category": "원의 성질과 원주각 (Circle Geometry)",
            "title": "피자 조각 중심각에서 원주각 불변량과 프톨레마이오스 정리까지",
            "badge": "중3·고1·수능 도형 필수",
            "elem": {
                "grade": "초등 3~6학년",
                "concept": "원의 중심과 반지름 · 부채꼴 각도 재기 · 이등변삼각형의 두 밑각",
                "intuition": "원의 중심에서 원 위의 두 점으로 그은 선분은 반지름으로 길이가 무조건 같다(이등변삼각형)!",
                "bridgeQuestion": "원의 중심에 있던 꼭짓점을 원둘레 끝까지 뒤로 물러나게 하면 각도는 몇 분의 1로 줄어들까?"
            },
            "middle": {
                "grade": "중등 3학년",
                "concept": "중심각과 원주각(1/2배) · 내접사각형 대각의 합 180° · 접선과 현이 이루는 각",
                "intuition": "원 위의 점을 어디로 옮겨도 같은 호를 바라보는 원주각의 크기는 단 1도도 변하지 않는다!",
                "min7014Title": "원주각과 중심각의 크기 관계 & 톨레미(Ptolemy)의 정리 시각적 증명",
                "min7014Query": "해석기하·원의 방정식",
                "min7014Url": "https://min7014.github.io/2025020101.pdf"
            },
            "high": {
                "grade": "고등 수학I · 미적분 도형극한",
                "concept": "원주각 불변량 ➔ 사인법칙(2R) ➔ 원에 내접하는 사각형의 코사인법칙 연립",
                "killerPoint": "원에 내접하는 사각형에서 마주 보는 각이 θ와 π-θ이므로 cos(π-θ) = -cosθ로 대각선 길이를 즉시 구한다",
                "searchKeyword": "원에 내접하는 사각형 코사인법칙"
            }
        },
        {
            "id": "genealogy-ceva-area",
            "category": "삼각형의 넓이 비와 닮음 (Area Ratios)",
            "title": "밑변 쪼개기에서 무게중심·체바·메넬라우스와 벡터 내분까지",
            "badge": "기하·벡터 1등급 핵심",
            "elem": {
                "grade": "초등 5학년",
                "concept": "삼각형의 넓이 (밑변 × 높이 ÷ 2) · 평행선 사이의 거리(높이)",
                "intuition": "꼭짓점을 공유하는 두 삼각형은 높이가 똑같아서 밑변의 길이 비율이 곧 넓이의 비율이다!",
                "bridgeQuestion": "삼각형의 세 중선은 왜 한 점(무게중심)에서 만나고 넓이를 똑같이 6등분할까?"
            },
            "middle": {
                "grade": "중등 2학년",
                "concept": "평행선과 선분의 길이 비 · 삼각형의 무게중심(2:1) · 체바와 메넬라우스 정리",
                "intuition": "평행보조선 딱 한 줄을 긋거나 밑변 비를 넓이 비로 바꾸면 세 분수의 곱이 도미노처럼 약분되어 1이 된다!",
                "min7014Title": "체바의 정리(2017090101) & 메넬라우스의 정리(2014111901) 단계별 시각 증명",
                "min7014Query": "유클리드 평면기하",
                "min7014Url": "https://min7014.github.io/2017090101.pdf"
            },
            "high": {
                "grade": "고등 기하 · 벡터",
                "concept": "위치벡터의 내분점 공식 ➔ p·PA + q·PB + r·PC = 0 삼각형 내부 점의 넓이 비(p:q:r)",
                "killerPoint": "계수의 비 p : q : r 가 곧 마주 보는 세 소삼각형 △PBC : △PCA : △PAB 의 넓이 비와 일치한다",
                "searchKeyword": "무게중심 내분 삼각형의 넓이"
            }
        },
        {
            "id": "genealogy-poly-factor",
            "category": "다항식과 인수정리 (Polynomials & Roots)",
            "title": "나눗셈 검산식에서 나머지정리·인수정리와 삼·사차함수 식 작성까지",
            "badge": "수II 다항함수 추론 근간",
            "elem": {
                "grade": "초등 3~4학년",
                "concept": "나눗셈의 몫과 나머지 · 검산식 (나누어지는 수 = 나누는 수 × 몫 + 나머지)",
                "intuition": "17 ÷ 5 = 몫 3, 나머지 2 ➔ 17 = 5 × 3 + 2 (나머지가 0이면 나누어떨어진다 = 약수와 배수!)",
                "bridgeQuestion": "숫자 대신 x가 들어간 다항식 f(x)를 (x-2)로 나눈 나머지를 나눗셈 안 하고 1초 만에 구할 수 있을까?"
            },
            "middle": {
                "grade": "중등 3학년",
                "concept": "곱셈공식과 인수분해 · 이차방정식 (x-α)(x-β)=0의 해와 그래프 x절편",
                "intuition": "방정식의 실근 α는 곧 그래프가 x축과 만나는 교점의 x좌표이고, 식에서는 (x-α) 인수이다!",
                "min7014Title": "곱셈공식과 인수분해의 도형 넓이 퍼즐 시각적 증명",
                "min7014Query": "다항식·방정식·수체계",
                "min7014Url": "https://min7014.github.io/2019080802.html"
            },
            "high": {
                "grade": "고등 수학(상) · 수학II",
                "concept": "나머지정리 f(α)=R ➔ 인수정리 ➔ 접선과의 차함수 f(x)-g(x) = a(x-α)²(x-β)",
                "killerPoint": "관통하는 교점은 1차 인수 (x-α), 스치듯 접하는 교점은 2차 인수 (x-α)², 변곡접선은 3차 인수 (x-α)³으로 즉시 식을 세운다",
                "searchKeyword": "삼차함수 사차함수 최고차항의 계수"
            }
        },
        {
            "id": "genealogy-mvt-rolle",
            "category": "연속성과 평균값 정리 (Continuity & MVT)",
            "title": "끊어지지 않은 선 긋기에서 사잇값·롤·평균값 정리까지",
            "badge": "기억·니은·디귿 합답형 단골",
            "elem": {
                "grade": "초등 4학년",
                "concept": "꺾은선그래프 변화 관찰 · 어제 키가 130cm, 오늘 132cm면 중간에 131cm인 순간이 있었다!",
                "intuition": "연필을 종이에서 떼지 않고 지하 1층에서 지상 3층까지 그리면 반드시 0층(땅바닥)을 최소 한 번은 지나간다!",
                "bridgeQuestion": "출발점과 도착점의 높이가 같도록 부드러운 산 모양 곡선을 그리면 꼭대기(수평 접선)가 반드시 존재할까?"
            },
            "middle": {
                "grade": "중등 2~3학년",
                "concept": "두 점을 잇는 직선의 기울기 · 평행선의 성질(기울기가 같다)",
                "intuition": "곡선 양 끝점을 이은 직선(할선)을 그대로 평행이동시키면 곡선의 볼록한 부분과 딱 접하는 순간이 생긴다!",
                "min7014Title": "롤의 정리와 평균값 정리의 기하학적 의미 동적 탐구",
                "min7014Query": "미분·도함수",
                "min7014Url": "https://min7014.github.io/2019080802.html"
            },
            "high": {
                "grade": "고등 수학II · 미적분",
                "concept": "사잇값 정리(실근 존재) ➔ 롤의 정리 f'(c)=0 ➔ 평균값 정리 [f(b)-f(a)]/(b-a) = f'(c)",
                "killerPoint": "문제에 두 함숫값의 차 f(b)-f(a)와 도함수 f'(x)의 범위가 동시에 등장하면 100% 평균값 정리 부등식 문제이다",
                "searchKeyword": "평균값 정리 사잇값 정리"
            }
        }
    ],
    "polyaHeuristics": [
        {
            "id": "polya-13",
            "domain": "기하·삼각함수",
            "condition": "원에 내접하는 사각형 ABCD가 등장할 때",
            "firstAction": "마주 보는 두 내각에 [θ와 (π - θ)]를 표시하고, 대각선 AC 또는 BD를 보조선으로 그어 코사인법칙을 두 번 쓴다!",
            "visualIntuition": "내접사각형의 마주 보는 각의 합은 180°이므로 cos(π-θ) = -cosθ가 되어 미지수 두 개를 한 번에 연립할 수 있습니다.",
            "formulaBridge": "AC² = a²+b²-2ab cosθ = c²+d²+2cd cosθ",
            "min7014Query": "해석기하·원의 방정식",
            "searchKeyword": "원에 내접하는 사각형"
        },
        {
            "id": "polya-14",
            "domain": "기하·도형",
            "condition": "삼각형의 내접원(내심 I)과 반지름 r이 주어질 때",
            "firstAction": "내심 I에서 세 변에 [수선의 발(반지름 r)]을 내리고, 넓이 공식 [S = (1/2)r(a+b+c)]와 접선 길이 같음을 표시한다!",
            "visualIntuition": "삼각형을 내심 기준으로 3개의 작은 삼각형으로 쪼개면 높이가 모두 내접원 반지름 r로 똑같습니다.",
            "formulaBridge": "S = ½r(a+b+c), 꼭짓점에서 접점까지의 거리를 x, y, z로 두면 a=y+z, b=z+x, c=x+y",
            "min7014Query": "유클리드 평면기하",
            "searchKeyword": "내접원 반지름 삼각형"
        },
        {
            "id": "polya-15",
            "domain": "수학II·미분",
            "condition": "곡선 밖의 한 점 (a, b)에서 곡선 y=f(x)에 그은 접선의 개수를 물어볼 때",
            "firstAction": "접점의 x좌표를 [미지수 t로 먼저 선언: 접점 (t, f(t))]하고, 접선의 방정식에 (a, b)를 대입해 t에 대한 방정식 실근 개수로 바꾼다!",
            "visualIntuition": "곡선 밖의 점은 기울기도 접점도 모르므로, 무조건 '접점의 x좌표 = t'를 주인공으로 세우는 것이 제1원칙입니다.",
            "formulaBridge": "b - f(t) = f'(t)(a - t) 의 서로 다른 실근 t의 개수 = 그을 수 있는 접선의 개수",
            "min7014Query": "미분·도함수",
            "searchKeyword": "접선의 방정식 곡선 밖"
        },
        {
            "id": "polya-16",
            "domain": "수학I·수열",
            "condition": "수열의 귀납적 정의 a_{n+1} = (조건부 분기식)에서 a_1의 값을 모두 구하라고 할 때",
            "firstAction": "a_1을 미지수로 두고 정방향으로 전개하지 말고, 알고 있는 뒤쪽 항(예: a_5, a_6)에서 거꾸로 [역추적 나뭇가지 트리(Tree)]를 그린다!",
            "visualIntuition": "홀수/짝수나 대소 조건으로 갈라지는 점화식은 역방향으로 거슬러 올라가며 조건에 맞지 않는 가지를 쳐내는(Pruning) 것이 가장 빠릅니다.",
            "formulaBridge": "역추적 시 구한 이전 항 a_n이 해당 분기 조건(예: a_n < 0 또는 자연수 조건)을 실제로 만족하는지 매 단계 검산 필수!",
            "min7014Query": "수열·시그마",
            "searchKeyword": "모든 a_1의 값의 합 수열"
        }
    ],
    "misconceptionLab": [
        {
            "id": "vaccine-09",
            "subject": "수학I · 로그의 성질",
            "myth": "log_a(x²) = 2 log_a(x) 는 정의역 안에서 언제나 성립하는 항등식이다?",
            "verdict": "❌ 거짓 (False!)",
            "counterexample": "x = -2일 때 log₂((-2)²) = log₂(4) = 2는 정의되지만, 우변 2 log₂(-2)는 진수가 음수라 존재하지 않는다!",
            "explanation": "짝수 제곱(x²)을 앞으로 내릴 때 x가 음수일 가능성을 잊으면 진수 조건(x > 0)이 깨져 실근의 개수가 절반으로 줄어드는 대형 사고가 납니다.",
            "correctRule": "짝수 지수를 로그 밖으로 내릴 때는 반드시 절댓값을 씌워 log_a(x²) = 2 log_a|x| (단, x ≠ 0)로 변형해야 양수·음수 해를 모두 지킬 수 있습니다.",
            "searchKeyword": "로그방정식 진수 조건"
        },
        {
            "id": "vaccine-10",
            "subject": "수학II · 연속함수의 곱",
            "myth": "불연속함수 f(x)와 연속함수 g(x)를 곱한 f(x)g(x)가 x=a에서 연속이려면 g(a)=0이어야만 한다?",
            "verdict": "⚠️ 반쪽짜리 진실 (예외 존재!)",
            "counterexample": "f(x)가 x=a 좌극한 -1, 우극한 1이고 g(x)가 아니라 f(x)·f(x)처럼 불연속끼리 곱하거나 좌우 절댓값이 같은 경우",
            "explanation": "대부분의 수능 문항(f(x)가 좌우극한이 다른 유한 확정값이고 g(x)가 다항함수일 때)에서는 g(a)=0이 맞지만, f(x)가 무한대로 발산(분모=0)하면 g(a)=0만으로는 부족하고 약분될 인수 (x-a)²이 필요할 수 있습니다.",
            "correctRule": "① f(x)가 x=a에서 유한한 점프 불연속이면 연속함수 g(a)=0으로 0을 곱해 덮어준다. ② f(x)가 1/(x-a) 꼴 발산이면 g(x)가 (x-a) 이상의 인수를 가져 극한값과 함숫값까지 일치시켜야 합니다.",
            "searchKeyword": "실수 전체의 집합에서 연속"
        },
        {
            "id": "vaccine-11",
            "subject": "확률과 통계 · 독립과 배반",
            "myth": "두 사건 A와 B가 서로 배반사건(동시에 일어나지 않음, P(A∩B)=0)이면 서로 독립이다?",
            "verdict": "❌ 거짓 (정반대! 100% 종속)",
            "counterexample": "주사위 1개를 던질 때 짝수 눈 사건 A={2,4,6}와 홀수 눈 사건 B={1,3,5}",
            "explanation": "사건 A가 일어났다는 소식을 듣는 순간 사건 B가 일어날 확률이 원래 1/2에서 0으로 확 바뀌어 버리므로, 배반사건은 서로에게 가장 강력한 영향을 주는 '종속사건'입니다!",
            "correctRule": "P(A)>0, P(B)>0인 두 사건이 배반(P(A∩B)=0)이면 P(A)P(B) ≠ 0이므로 절대 독립(P(A∩B)=P(A)P(B))이 될 수 없습니다.",
            "searchKeyword": "배반사건 독립 사건"
        }
    ],
    "teacherLessonScenarios": [
        {
            "id": "lesson-heptagon-knot",
            "gradeTarget": "중1~고1 기하 · 수학동아리 · 영재학급",
            "topic": "눈금 없는 종이띠 한 장을 묶어 당기면 왜 완벽한 정오각형·정칠각형이 접힐까?",
            "hookQuestion": "자와 컴퍼스로도 작도하기 까다로운 정다각형을, 긴 종이테이프 한 장으로 매듭을 지어 살짝 당기는 것만으로 오차 0%로 만들 수 있는 비밀은 무엇일까?",
            "interactiveMission": "@min7014_ai의 '정칠각형의 매듭 원리(2025020401)' 1080p 설명영상을 재생하고 대칭 사다리꼴과 등변사다리꼴의 각도 관계를 따라가 보자!",
            "groupDiscussion": "종이띠의 폭이 일정하기 때문에 평행사변형과 마름모(이등변삼각형)가 자동 생성되는 원리를 종이테이프로 직접 접으며 증명해 보자.",
            "min7014Query": "__CONSTRUCTION__",
            "videoSlug": "2025020401",
            "quizKeyword": "정다각형 대각선"
        },
        {
            "id": "lesson-viviani",
            "gradeTarget": "중2~고1 기하 · 수행평가 탐구",
            "topic": "정삼각형 공원 어디에 분수대를 세워도 세 산책로까지의 거리 합이 똑같다?! (비비아니 정리)",
            "hookQuestion": "정삼각형 모양의 섬 내부 아무 곳에나 집을 지었을 때, 세 해안선까지 수직으로 걸어가는 세 길의 합을 가장 짧게 하려면 어디에 지어야 할까?",
            "interactiveMission": "@min7014_ai의 '비비아니 정리(2025012901)' 1080p 시각적 증명 영상을 보고, 정삼각형을 세 개의 작은 삼각형으로 쪼개거나 평행선으로 회전시키는 장면을 관찰하자!",
            "groupDiscussion": "전체 정삼각형 넓이 S = ½a(h₁+h₂+h₃) = ½aH 식을 보며, 만약 정삼각형이 아니라 직사각형이나 정육각형이면 어떤 불변량이 성립할지 확장해 보자.",
            "min7014Query": "유클리드 평면기하",
            "videoSlug": "2025012901",
            "quizKeyword": "정삼각형 수선의 발 넓이"
        }
    ]
}


def load_pedagogy_engine():
    if os.path.exists(PEDAGOGY_JSON):
        with open(PEDAGOGY_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def expand_pedagogy_from_min7014_vault(max_add_per_category=2):
    """
    [지속적 수학교육 발전 엔진]
    1) CONTINUOUS_PEDAGOGY_EXPANSION_POOL 및 min7014_deep_knowledge.json / video_lectures/catalog.json의 최신 주제를 스캔하여
       아직 등록되지 않은 수직 계통성 계보, 폴리아 보조선 사전, 오개념 백신, 5분 탐구 수업 시나리오를 지속적으로 확장합니다.
    2) 새로 제작된 @min7014_ai 영상(catalog.json)이 있으면 자동으로 교사용 5분 탐구 수업 시나리오와 연동합니다.
    """
    ped = load_pedagogy_engine()
    if not ped:
        return False

    changed = False
    for section_key in ["verticalGenealogy", "polyaHeuristics", "misconceptionLab", "teacherLessonScenarios", "creativeConstructiveLab"]:
        existing_list = ped.setdefault(section_key, [])
        existing_ids = {x.get("id") for x in existing_list}
        added = 0
        for candidate in CONTINUOUS_PEDAGOGY_EXPANSION_POOL.get(section_key, []):
            if candidate["id"] not in existing_ids:
                existing_list.append(candidate)
                existing_ids.add(candidate["id"])
                added += 1
                changed = True
                print(f"✨ [mathteacher Pedagogy Expanded -> {section_key}] +{candidate['id']}: {candidate.get('title') or candidate.get('condition') or candidate.get('myth') or candidate.get('topic')}")
                if added >= max_add_per_category:
                    break

    # 새로 렌더링된 @min7014_ai 영상 중 아직 teacherLessonScenarios에 없는 주제를 자동 탐구 수업 시나리오로 등록
    if os.path.exists(VIDEO_CATALOG_JSON):
        try:
            vcat = json.load(open(VIDEO_CATALOG_JSON, "r", encoding="utf-8"))
            scenarios = ped.setdefault("teacherLessonScenarios", [])
            existing_vslugs = {s.get("videoSlug") for s in scenarios if s.get("videoSlug")}
            for v in vcat:
                vslug = v.get("slug", "")
                if not vslug or vslug in existing_vslugs:
                    continue
                vtitle = re.sub(r"\$[^\$]*\$", "", v.get("title", "")).strip()
                sub_dom = v.get("sub_domain_ko") or "기하·대수 시각적 증명"
                new_scen = {
                    "id": f"lesson-auto-{vslug}",
                    "gradeTarget": f"중·고등 {sub_dom} 연계",
                    "topic": f"[시각적 증명 탐구] {vtitle}",
                    "hookQuestion": f"공식을 외우지 않고 보조선과 도형의 이동만으로 '{vtitle}'이(가) 왜 언제나 성립하는지 단 1분 만에 설명할 수 있을까?",
                    "interactiveMission": f"@min7014_ai의 '{vtitle} ({vslug})' 1080p 단계별 설명영상 및 9:16 숏폼을 칠판에 재생하고 결정적 보조선이 등장하는 단계를 찾아보자!",
                    "groupDiscussion": "영상에서 새롭게 등장한 보조선이나 색칠된 도형 영역이 전체 증명 과정을 어떻게 단축시켰는지 모둠별로 토의해 보자.",
                    "min7014Query": sub_dom.split("(")[0].strip(),
                    "videoSlug": vslug,
                    "quizKeyword": sub_dom.split("·")[0].strip()
                }
                scenarios.append(new_scen)
                existing_vslugs.add(vslug)
                changed = True
                print(f"🎬 [mathteacher Auto-Linked New Video to 5-Min Lesson Scenario] {vslug} -> {vtitle}")
        except Exception as e:
            print(f"[Video Catalog Lesson Sync Notice] {e}")

    if changed:
        with open(PEDAGOGY_JSON, "w", encoding="utf-8") as f:
            json.dump(ped, f, ensure_ascii=False, indent=2)
        print(f"✅ [Saved Expanded Pedagogy Engine] {PEDAGOGY_JSON}")
    return changed


def load_all_catalog():
    items = []
    if os.path.exists(INDEX_JSON):
        with open(INDEX_JSON, "r", encoding="utf-8") as f:
            items.extend(json.load(f))
    if os.path.exists(CATALOG_JSON):
        with open(CATALOG_JSON, "r", encoding="utf-8") as f:
            cat = json.load(f)
            existing = {it.get("slug") for it in items}
            for c in cat:
                if c.get("s") in existing:
                    continue
                items.append({
                    "slug": c["s"],
                    "title": c["t"],
                    "examYear": c["y"],
                    "examYearAlt": c.get("ya", ""),
                    "month": c["m"],
                    "grade": c["g"],
                    "subject": c["sub"],
                    "qNum": c["q"],
                    "source": c["src"],
                    "tags": c.get("tg", []),
                    "url": f"board/archive.html?id={c['s']}",
                })
    return items


def cmd_status():
    items = load_all_catalog()
    standalone_cnt = len(json.load(open(INDEX_JSON, "r", encoding="utf-8"))) if os.path.exists(INDEX_JSON) else 0
    shard_files = sorted(os.listdir(SHARDS_DIR)) if os.path.exists(SHARDS_DIR) else []
    ped = load_pedagogy_engine()
    min_cnt = len(json.load(open(MIN7014_DEEP_JSON, "r", encoding="utf-8"))) if os.path.exists(MIN7014_DEEP_JSON) else 0
    print("=" * 76)
    print("👩‍🏫 [mathteacher v2.5] 수석 수학 교사 에이전트 상태 및 수학교육 발전 모듈 보고")
    print("=" * 76)
    print(f"• 전체 등록된 단계별 수학 문항 수      : {len(items):,}문항")
    print(f"• 단독 HTML 퀴즈 페이지 (board/)       : {standalone_cnt:,}개")
    print(f"• 연도별 기출 샤드 DB (2006~2026)      : {len(shard_files)}개 연도 샤드")
    print(f"• min7014.github.io 심층 시각자료 연동 : {min_cnt:,}개 주제 (16대 영역 · 165개 세부 단원)")
    print(f"• 🌳 초·중·고 수직 계통성 계보 트리     : {len(ped.get('verticalGenealogy', []))}대 핵심 수능 킬러 계보")
    print(f"• 🧭 폴리아 조건➔보조선 1초 번역 사전  : {len(ped.get('polyaHeuristics', []))}대 실전 보조선·발상 규칙")
    print(f"• 🔬 오개념 백신 & 반례 실험실         : {len(ped.get('misconceptionLab', []))}대 빈출 오개념·반례 진단")
    print(f"• 👩‍🏫 교사용 5분 탐구 수업 런처        : {len(ped.get('teacherLessonScenarios', []))}종 교실 도입 발문 시나리오")
    print(f"• ✍️ 탈-5지선다 창의 구성 & 조건 변형 : {len(ped.get('creativeConstructiveLab', []))}대 열린 발상·What-If-Not 실험실")
    print(f"• ❓ 질문하는 수학 수업 프레임워크     : {len(ped.get('questionAskingClassrooms', []))}대 학생 질문 생성(Notice&Wonder·QFT·What-If-Not) 모델")
    print(f"• 🏛️ 수학교육 철학 & 호기심 도감       : {len(ped.get('educationalPhilosophy', []))}대 교육철학 강령 · {len(ped.get('curiosityRealWorldAtlas', []))}대 자연·우주·AI 호기심 도감")
    print("• 교육 설계 기준                       : 제0단계 기호 번역 + 1~5단계 초등 눈높이 디딤돌 + SVG 도형 + 도식화 흐름도 + min7014.github.io 상시 진화")
    print("=" * 76)


def cmd_genealogy(keyword: str = ""):
    ped = load_pedagogy_engine()
    items = ped.get("verticalGenealogy", [])
    print("=" * 76)
    print("🌳 [mathteacher] 초등 직관 ➔ 중등 기하·대수 ➔ 고등 수능 100점 수직 계통성 트리")
    print("=" * 76)
    for g in items:
        blob = json.dumps(g, ensure_ascii=False).lower()
        if keyword and keyword.lower() not in blob:
            continue
        print(f"■ [{g['category']}] {g['title']} ({g['badge']})")
        print(f"  🌱 [초등 뿌리 ({g['elem']['grade']})] {g['elem']['concept']} ➔ \"{g['elem']['intuition']}\"")
        print(f"  🌿 [중등 다리 ({g['middle']['grade']})] {g['middle']['concept']} ➔ min7014: {g['middle']['min7014Title']}")
        print(f"  🌳 [고등 완성 ({g['high']['grade']})] {g['high']['concept']}")
        print(f"     💡 킬러 핵심: {g['high']['killerPoint']} | 실전 기출 검색: '{g['high']['searchKeyword']}'")
        print("-" * 76)


def cmd_polya(keyword: str = ""):
    ped = load_pedagogy_engine()
    items = ped.get("polyaHeuristics", [])
    print("=" * 76)
    print("🧭 [mathteacher] 폴리아(Pólya) '조건 ➔ 제1보조선·발상' 1초 번역 사전")
    print("=" * 76)
    for p in items:
        blob = json.dumps(p, ensure_ascii=False).lower()
        if keyword and keyword.lower() not in blob:
            continue
        print(f"■ [{p['domain']}] 조건: {p['condition']}")
        print(f"  ⚡ 제1보조선/발상 : {p['firstAction']}")
        print(f"  🎨 시각적 직관   : {p['visualIntuition']}")
        print(f"  📐 수식 브릿지   : {p['formulaBridge']} | 실전 기출 검색: '{p['searchKeyword']}'")
        print("-" * 76)


def cmd_vaccine(keyword: str = ""):
    ped = load_pedagogy_engine()
    items = ped.get("misconceptionLab", [])
    print("=" * 76)
    print("🔬 [mathteacher] 오개념 백신 & 1초 반례 실험실 (Lakatos Counterexample Lab)")
    print("=" * 76)
    for v in items:
        blob = json.dumps(v, ensure_ascii=False).lower()
        if keyword and keyword.lower() not in blob:
            continue
        print(f"■ [{v['subject']}] 흔한 착각: \"{v['myth']}\" ➔ {v['verdict']}")
        print(f"  💥 1초 결정적 반례 : {v['counterexample']}")
        print(f"  🔍 왜 틀렸을까?    : {v['explanation']}")
        print(f"  ✅ 올바른 판정 기준: {v['correctRule']}")
        print("-" * 76)


def cmd_lesson(keyword: str = ""):
    ped = load_pedagogy_engine()
    items = ped.get("teacherLessonScenarios", [])
    print("=" * 76)
    print("👩‍🏫 [mathteacher] 교사용 5분 탐구 수업 시나리오 & 발문 런처")
    print("=" * 76)
    for l in items:
        blob = json.dumps(l, ensure_ascii=False).lower()
        if keyword and keyword.lower() not in blob:
            continue
        print(f"■ [{l['gradeTarget']}] {l['topic']}")
        print(f"  ❓ 호기심 발문 (Why?) : {l['hookQuestion']}")
        print(f"  🧭 시각적 실험 미션   : {l['interactiveMission']}")
        print(f"  💬 모둠 토의 주제     : {l['groupDiscussion']}")
        print("-" * 76)






def cmd_philosophy(keyword: str = ""):
    ped = load_pedagogy_engine()
    phils = ped.get("educationalPhilosophy", [])
    atlas = ped.get("curiosityRealWorldAtlas", [])
    print("=" * 84)
    print("🏛️ [mathteacher] 민은기 선생님의 mathedu 5대 수학교육 철학 & 학생 호기심 점화 도감")
    print("=" * 84)
    for p_item in phils:
        print(f"■ {p_item['title']}")
        print(f"  ✨ 철학 모토 : \"{p_item['motto']}\"")
        print(f"  🎓 사상 배경 : {p_item['thinkers']}")
        print(f"  🚀 실제 구현 : {p_item['matheduPractice']}")
        print("-" * 84)
    print("🌍 [왜 이 수학을 배울까? — 자연·우주·AI·일상 속 수학 호기심 도감]")
    print("-" * 84)
    for c_item in atlas:
        if keyword and keyword.lower() not in str(c_item).lower():
            continue
        print(f"■ [{c_item['domain']}] {c_item['studentWonderQuestion']}")
        print(f"  📐 핵심 원리 : {c_item['mathCorePrinciple']}")
        print(f"  🤔 사고 실험 : {c_item['miniThoughtExperiment']}")
        print("-" * 84)


def cmd_question(keyword: str = ""):
    ped = load_pedagogy_engine()
    items = ped.get("questionAskingClassrooms", [])
    print("=" * 76)
    print("❓ [mathteacher] 트렌드 핵심: '질문하는 수학 수업 (Question-Asking Classroom)' 5대 프레임워크")
    print("=" * 76)
    for qm in items:
        blob = json.dumps(qm, ensure_ascii=False).lower()
        if keyword and keyword.lower() not in blob:
            continue
        print(f"■ {qm['framework']}")
        print(f"  💡 핵심 원리: {qm['corePrinciple']}")
        for tp in qm.get("teacherPrompts", []):
            print(f"  👩‍🏫 교사 촉진 발문: {tp}")
        for sq in qm.get("studentQuestionExamples", []):
            print(f"  🙋 학생 생성 질문: \"{sq}\"")
        print(f"  🔗 mathedu 연동 : {qm['min7014Integration']}")
        print("-" * 76)


def cmd_creative(keyword: str = ""):
    ped = load_pedagogy_engine()
    items = ped.get("creativeConstructiveLab", [])
    print("=" * 76)
    print("✍️ [mathteacher] 탈-5지선다 창의적 구성주의 & 조건 변형(What-If-Not) 실험실")
    print("=" * 76)
    for c in items:
        blob = json.dumps(c, ensure_ascii=False).lower()
        if keyword and keyword.lower() not in blob:
            continue
        print(f"■ [{c['domain']}] {c['title']}")
        print(f"  📌 원문 명제       : {c['originalProblem']}")
        print(f"  ✍️ 탈-5지선다 미션 : {c['constructivePrompt']}")
        for mp in c.get("multiPathApproaches", []):
            print(f"     • {mp}")
        print(f"  🔀 What-If-Not 발명: {c['whatIfNotMutation']}")
        print("-" * 76)


def cmd_search(query: str):
    items = load_all_catalog()
    tokens = [t.strip() for t in query.split() if t.strip()]
    results = []
    for it in items:
        hay = f"{it.get('title','')} {it.get('examYear','')}학년도 {it.get('month','')} {it.get('grade','')} {it.get('subject','')} {it.get('qNum','')}번 {it.get('source','')} {' '.join(it.get('tags',[]))}".lower()
        if all(tok.lower() in hay for tok in tokens):
            results.append(it)
    print(f"🔍 [mathteacher 검색 결과] '{query}' ➔ 총 {len(results):,}문항 매칭 (상위 15건 표시)")
    print("-" * 72)
    for idx, r in enumerate(results[:15], 1):
        url = r.get("url") or f"board/{r['slug']}.html"
        print(f"{idx:2d}. [{r.get('slug')}] {r.get('title')}  ➔  {url}")


def cmd_explain(slug: str):
    m = re.match(r"^e(\d{2})_", slug)
    if m:
        yr = "20" + m.group(1)
        shard_path = os.path.join(SHARDS_DIR, f"exam_{yr}.json")
        if os.path.exists(shard_path):
            d = json.load(open(shard_path, "r", encoding="utf-8"))
            prob = d.get("problems", {}).get(slug)
            if prob:
                print("=" * 72)
                print(f"👩‍🏫 [mathteacher 단계별 해설] {prob['title']}")
                print("=" * 72)
                print(f"• 출처: {prob['source']} ({prob['grade']} {prob['subject']} {prob['qNum']}번, {prob.get('point','3')}점)")
                print(f"• 단원: {' > '.join(prob.get('unit_parts', []))}")
                print(f"• 발문: {re.sub(r'<[^>]+>', '', prob['stem'])}")
                print("-" * 72)
                if prob.get("s3_q"):
                    print(f"🌱 [3단계 출발 조건 식 세우기] 정답 {prob['s3_q']['answer']}번 ➔ {prob['s3_q']['options'][prob['s3_q']['answer']-1]}")
                if prob.get("s4_q"):
                    print(f"🌳 [4단계 중간 관계식 유도]   정답 {prob['s4_q']['answer']}번 ➔ {prob['s4_q']['options'][prob['s3_q']['answer']-1]}")
                ans_i = int(prob.get("answer", 1))
                opts = prob.get("options", [])
                ans_str = opts[ans_i - 1] if 1 <= ans_i <= len(opts) else str(ans_i)
                print(f"💎 [최종 정답] {ans_i}번 ({ans_str})")
                print("=" * 72)
                return
    print(f"문항 슬러그 '{slug}'는 board/{slug}.html 단독 페이지 또는 board/archive.html?id={slug}에서 열람할 수 있습니다.")


def cmd_audit():
    subprocess.run([sys.executable, os.path.join(BASE_DIR, "audit_engine.py")], check=True)
    subprocess.run([sys.executable, os.path.join(BASE_DIR, "audit_full_mathedu.py")], check=True)


def main():
    if len(sys.argv) < 2 or sys.argv[1] == "status":
        cmd_status()
    elif sys.argv[1] == "search":
        q = " ".join(sys.argv[2:])
        cmd_search(q)
    elif sys.argv[1] == "explain" and len(sys.argv) >= 3:
        cmd_explain(sys.argv[2])
    elif sys.argv[1] == "genealogy":
        cmd_genealogy(" ".join(sys.argv[2:]))
    elif sys.argv[1] == "polya":
        cmd_polya(" ".join(sys.argv[2:]))
    elif sys.argv[1] == "vaccine":
        cmd_vaccine(" ".join(sys.argv[2:]))
    elif sys.argv[1] == "lesson":
        cmd_lesson(" ".join(sys.argv[2:]))
    elif sys.argv[1] == "creative":
        cmd_creative(" ".join(sys.argv[2:]))
    elif sys.argv[1] == "question":
        cmd_question(" ".join(sys.argv[2:]))
    elif sys.argv[1] == "philosophy":
        cmd_philosophy(" ".join(sys.argv[2:]))
    elif sys.argv[1] == "expand":
        expand_pedagogy_from_min7014_vault(max_add_per_category=10)
        cmd_status()
    elif sys.argv[1] == "audit":
        cmd_audit()
    else:
        cmd_status()


if __name__ == "__main__":
    main()
