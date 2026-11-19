"""수학자료실 연계 정밀 분석, 추천 및 인터랙티브 HTML 생성 모듈
- 수학자료실의 교육 철학: '모든 과정이 다 드러나게 하는 단계별 시각적 플립북 증명' 전수 반영
"""
import html
import json
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MATERIALS_PATH = os.path.join(BASE_DIR, "assets", "min7014_materials.json")
DEEP_KNOWLEDGE_PATH = os.path.join(BASE_DIR, "assets", "min7014_deep_knowledge.json")

_CACHED_MATERIALS = None
_CACHED_BY_ID = None
_CACHED_DEEP_KNOWLEDGE = None


# 2027학년도 수능 전 46문항 핵심 원리 기반 정밀 큐레이션 매핑 (min7014.github.io 실존 자료 ID)
CSAT27_CURATED_PRIORITY_IDS = {
    # 공통 1~22번
    "csat27_01": ["MIN-KB-0277", "MIN-KB-0278", "MIN-KB-0281", "MIN-KB-0282"],
    "csat27_02": ["MIN-KB-0663", "MIN-KB-0664", "MIN-KB-0642", "MIN-KB-0665"],
    "csat27_03": ["MIN-KB-0496", "MIN-KB-0497", "MIN-KB-0498", "MIN-KB-0499"],
    "csat27_04": ["MIN-KB-0518", "MIN-KB-1111", "MIN-KB-0504", "MIN-KB-1104"],
    "csat27_05": ["MIN-KB-0525", "MIN-KB-0692", "MIN-KB-0641", "MIN-KB-1062"],
    "csat27_06": ["MIN-KB-0434", "MIN-KB-0429", "MIN-KB-0463", "MIN-KB-0427"],
    "csat27_07": ["MIN-KB-0674", "MIN-KB-0675", "MIN-KB-0703", "MIN-KB-1006"],
    "csat27_08": ["MIN-KB-0413", "MIN-KB-0414", "MIN-KB-1000", "MIN-KB-0416"],
    "csat27_09": ["MIN-KB-0643", "MIN-KB-0692", "MIN-KB-0664", "MIN-KB-0641"],
    "csat27_10": ["MIN-KB-0459", "MIN-KB-0460", "MIN-KB-0456", "MIN-KB-0453"],
    "csat27_11": ["MIN-KB-0655", "MIN-KB-0642", "MIN-KB-0668", "MIN-KB-0665"],
    "csat27_12": ["MIN-KB-0494", "MIN-KB-0495", "MIN-KB-0492", "MIN-KB-0493"],
    "csat27_13": ["MIN-KB-0692", "MIN-KB-0525", "MIN-KB-0641", "MIN-KB-1006"],
    "csat27_14": ["MIN-KB-0421", "MIN-KB-0419", "MIN-KB-0343", "MIN-KB-0342"],
    "csat27_15": ["MIN-KB-0795", "MIN-KB-0796", "MIN-KB-0518", "MIN-KB-1110"],
    "csat27_16": ["MIN-KB-0407", "MIN-KB-0408", "MIN-KB-0275", "MIN-KB-0276"],
    "csat27_17": ["MIN-KB-0525", "MIN-KB-0692", "MIN-KB-0668", "MIN-KB-0665"],
    "csat27_18": ["MIN-KB-0500", "MIN-KB-0501", "MIN-KB-0502", "MIN-KB-0503"],
    "csat27_19": ["MIN-KB-0674", "MIN-KB-0675", "MIN-KB-0703", "MIN-KB-0313"],
    "csat27_20": ["MIN-KB-0434", "MIN-KB-0463", "MIN-KB-0664", "MIN-KB-0642"],
    "csat27_21": ["MIN-KB-0663", "MIN-KB-0674", "MIN-KB-0703", "MIN-KB-0666"],
    "csat27_22": ["MIN-KB-0490", "MIN-KB-0501", "MIN-KB-0495", "MIN-KB-0414"],
    # 확률과 통계 23~30번
    "csat27_p23": ["MIN-KB-0467", "MIN-KB-0939", "MIN-KB-0014", "MIN-KB-0475"],
    "csat27_p24": ["MIN-KB-0467", "MIN-KB-0475", "MIN-KB-0939", "MIN-KB-0014"],
    "csat27_p25": ["MIN-KB-0475", "MIN-KB-0469", "MIN-KB-0481", "MIN-KB-0482"],
    "csat27_p26": ["MIN-KB-0467", "MIN-KB-0053", "MIN-KB-0054", "MIN-KB-0939"],
    "csat27_p27": ["MIN-KB-0487", "MIN-KB-0485", "MIN-KB-0484", "MIN-KB-0477"],
    "csat27_p28": ["MIN-KB-0467", "MIN-KB-0481", "MIN-KB-0939", "MIN-KB-0014"],
    "csat27_p29": ["MIN-KB-0475", "MIN-KB-0469", "MIN-KB-0473", "MIN-KB-0476"],
    "csat27_p30": ["MIN-KB-0467", "MIN-KB-0475", "MIN-KB-0939", "MIN-KB-0053"],
    # 미적분 23~30번
    "csat27_m23": ["MIN-KB-0716", "MIN-KB-0504", "MIN-KB-0523", "MIN-KB-0413"],
    "csat27_m24": ["MIN-KB-1062", "MIN-KB-1061", "MIN-KB-0692", "MIN-KB-0672"],
    "csat27_m25": ["MIN-KB-0818", "MIN-KB-0644", "MIN-KB-0497", "MIN-KB-0499"],
    "csat27_m26": ["MIN-KB-0692", "MIN-KB-0641", "MIN-KB-1062", "MIN-KB-0719"],
    "csat27_m27": ["MIN-KB-0707", "MIN-KB-0722", "MIN-KB-0642", "MIN-KB-0673"],
    "csat27_m28": ["MIN-KB-0706", "MIN-KB-0716", "MIN-KB-0717", "MIN-KB-0673"],
    "csat27_m29": ["MIN-KB-0818", "MIN-KB-0497", "MIN-KB-0513", "MIN-KB-0644"],
    "csat27_m30": ["MIN-KB-0663", "MIN-KB-0434", "MIN-KB-1061", "MIN-KB-0692"],
    # 기하 23~30번
    "csat27_g23": ["MIN-KB-0583", "MIN-KB-0581", "MIN-KB-0593", "MIN-KB-0579"],
    "csat27_g24": ["MIN-KB-0526", "MIN-KB-0527", "MIN-KB-0536", "MIN-KB-0539"],
    "csat27_g25": ["MIN-KB-0631", "MIN-KB-0341", "MIN-KB-0586", "MIN-KB-0632"],
    "csat27_g26": ["MIN-KB-0544", "MIN-KB-0551", "MIN-KB-0545", "MIN-KB-0552"],
    "csat27_g27": ["MIN-KB-1026", "MIN-KB-0620", "MIN-KB-0621", "MIN-KB-0838"],
    "csat27_g28": ["MIN-KB-0599", "MIN-KB-0591", "MIN-KB-0590", "MIN-KB-0589"],
    "csat27_g29": ["MIN-KB-0564", "MIN-KB-0565", "MIN-KB-0526", "MIN-KB-0566"],
    "csat27_g30": ["MIN-KB-0634", "MIN-KB-0630", "MIN-KB-0610", "MIN-KB-0013"],
}


def get_materials():
    global _CACHED_MATERIALS, _CACHED_BY_ID
    if _CACHED_MATERIALS is None:
        if os.path.exists(MATERIALS_PATH):
            with open(MATERIALS_PATH, "r", encoding="utf-8") as f:
                _CACHED_MATERIALS = json.load(f)
        else:
            _CACHED_MATERIALS = []
        _CACHED_BY_ID = {it.get("id"): it for it in _CACHED_MATERIALS if it.get("id")}
    return _CACHED_MATERIALS


def _get_materials_by_id():
    if _CACHED_BY_ID is None:
        get_materials()
    return _CACHED_BY_ID or {}


def get_deep_knowledge():
    global _CACHED_DEEP_KNOWLEDGE
    if _CACHED_DEEP_KNOWLEDGE is None:
        if os.path.exists(DEEP_KNOWLEDGE_PATH):
            with open(DEEP_KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
                _CACHED_DEEP_KNOWLEDGE = json.load(f)
        else:
            _CACHED_DEEP_KNOWLEDGE = []
    return _CACHED_DEEP_KNOWLEDGE


def match_deep_knowledge(text, limit=3):
    """주어진 문항 텍스트나 수학 개념에 가장 적합한 심층 수학 지식 및 초등 디딤돌 발문 아이디어 반환"""
    items = get_deep_knowledge()
    if not items:
        return []

    text_lower = text.lower()
    scored = []

    for item in items:
        t = item.get("title", "").lower()
        cat = item.get("category", "").lower()
        score = 0

        for word in text_lower.split():
            if len(word) >= 2 and (word in t or word in cat):
                score += 15

        if score > 0:
            scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [x[1] for x in scored[:limit]]


def match_materials(text, limit=4):
    materials = get_materials()
    if not materials:
        return []

    text_lower = text.lower()
    text_no_pdf = text_lower.replace("확률밀도함수", "확률밀도")
    scored = []

    is_circle = ("원의 방정식" in text_lower) or (
        "원" in text_lower
        and any(k in text_lower for k in ["거리", "직선", "접선", "중심", "반지름"])
        and not any(k in text_lower for k in ["단면 원", "교선 원", "구 s", "두 구", "단위원"])
    )
    is_trig = any(k in text_lower for k in ["삼각함수", "삼각비", "단위원", "호도법", "사인함수", "코사인함수"])
    is_law = any(k in text_lower for k in ["사인법칙", "코사인법칙", "사인 법칙", "코사인 법칙"])
    is_limit_cont = any(
        k in text_lower
        for k in ["좌극한", "우극한", "함수의 극한", "극한값", "연속", "불연속", "우연속", "함수의극한", "함수의연속"]
    )
    is_diff = any(
        k in text_no_pdf
        for k in [
            "미분",
            "접선",
            "도함수",
            "할선",
            "미분계수",
            "미분가능",
            "변곡점",
            "극대",
            "극소",
            "역함수",
            "음함수",
            "매개변수",
            "속도",
        ]
    )
    is_poly = any(k in text_lower for k in ["삼차함수", "사차함수", "다항함수"])
    is_space = any(
        k in text_lower
        for k in [
            "좌표공간",
            "공간도형",
            "삼수선",
            "정사영",
            "이면각",
            "법선",
            "육각기둥",
            "정사면체",
            "사면체",
            "직선과 평면",
            "두 구",
            "구 s",
            "공간좌표",
        ]
    )
    is_vector = any(k in text_lower for k in ["벡터", "내적", "실수배", "위치벡터", "평면벡터", "공간벡터"])
    is_coord_div = any(k in text_lower for k in ["내분", "외분", "무게중심"])
    is_conic = any(
        k in text_lower
        for k in ["포물선", "타원", "쌍곡선", "원뿔곡선", "단델린", "준선"]
    )
    is_geom = any(
        k in text_lower
        for k in ["피타고라스", "외심", "내심", "무게중심", "수심", "방심", "작도"]
    )
    is_seq = any(
        k in text_lower
        for k in ["수열", "등차", "등비", "부분합", "시그마", "급수", "귀납", "공차", "공비"]
    )
    is_exp = any(
        k in text_lower
        for k in ["지수법칙", "거듭제곱근", "유리수 지수", "지수함수", "지수방정식", "지수부등식", "지수와로그"]
    )
    is_log = any(k in text_lower for k in ["로그", "자연로그", "밑의 변환", "밑의변환", "log", "\\ln"])
    is_prob = any(
        k in text_lower
        for k in [
            "확률",
            "독립",
            "통계",
            "정규분포",
            "이항분포",
            "이산확률",
            "분산",
            "신뢰구간",
            "표본평균",
            "순열",
            "조합",
            "경우의수",
            "경우의 수",
            "여사건",
        ]
    )

    is_integral_geom_block = is_space or is_conic or is_vector or is_law
    has_integral_area = ("넓이" in text_lower) and any(
        k in text_lower for k in ["곡선", "둘러싸인", "이차함수", "삼차함수", "적분"]
    )
    is_integral = (not is_integral_geom_block) and (
        any(
            k in text_lower
            for k in ["적분", "정적분", "부정적분", "구분구적", "입체도형의부피", "입체도형의 부피", "회전체"]
        )
        or has_integral_area
    )

    want_polar = ("극좌표" in text_lower) or ("중적분" in text_lower)

    for item in materials:
        title = item.get("title", "")
        cat = item.get("category", "")
        tags_str = " ".join(item.get("tags", []))
        item_text = f"{title} {tags_str} {cat}".lower()
        score = 0

        title_l = title.lower()
        cat_l = cat.lower()

        # Non-math admin workshops / polar double-integral / string-art craft noise guard
        if any(w in item_text for w in ["워크숍", "현장연구", "영재교육원"]) and not (
            item.get("pdf") or item.get("geogebra") or item.get("algeomath")
        ):
            score -= 300
        if "극좌표계에서의 중적분" in item_text and not want_polar:
            score -= 250
        if any(w in title_l for w in ["compound", "스트링 아트", "매듭"]) and not any(
            w in text_lower for w in ["다면체", "매듭", "스트링"]
        ):
            score -= 120

        # 1. 공간도형 / 정사영 / 삼수선 / 이면각 / 구
        if is_space:
            if "공간도형" in cat or "공간좌표" in cat:
                score += 180
            if "삼수선" in text_lower and "삼수선" in title_l:
                score += 240
            if ("정사영" in text_lower or "이면각" in text_lower) and (
                "정사영" in title_l or "이면각" in title_l or "법선 벡터" in title_l
            ):
                score += 240
            if "직선과 평면" in text_lower or "평행" in text_lower or "접하는" in text_lower:
                if "직선과 평면" in title_l or "평행" in title_l or "평면과 수직" in title_l:
                    score += 150
            if ("구" in text_lower) and ("구(" in title_l or "구의 " in title_l or "구 위" in title_l):
                score += 160

        # 2. 벡터 / 내적 / 자취 영역
        if is_vector:
            if "벡터(" in cat or "벡터 " in cat:
                score += 220
            if any(k in text_lower for k in ["실수배", "성분", "덧셈"]) and any(
                k in title_l for k in ["실수배", "벡터의 합", "성분을 이용한 내적"]
            ):
                score += 180
            if "내적" in text_lower and "내적" in title_l:
                score += 160
            if any(k in text_lower for k in ["평행사변형", "영역", "자취", "최댓값", "최솟값"]) and any(
                k in title_l for k in ["평행사변형의 내부영역", "내적의 범위", "시점과 종점"]
            ):
                score += 190

        # 3. 좌표공간의 내분점 / 외분점 / 무게중심
        if is_coord_div:
            if "내분점과 외분점" in title_l or "내분점의 위치벡터" in title_l:
                score += 250
            if "무게중심" in text_lower and "무게중심" in title_l:
                score += 220
                if "작도" in title_l and "작도" not in text_lower:
                    score -= 60

        # 4. 원의 방정식
        if is_circle:
            if any(k in item_text for k in ["타원", "쌍곡선", "포물선", "원뿔"]):
                score -= 100
            elif "원의 방정식" in item_text:
                score += 220
            elif "원의 접선" in item_text or "원과 직선" in item_text:
                score += 180
            elif "원 위의 점" in item_text and "접선" in item_text:
                score += 170
            elif "원의" in item_text and not any(k in item_text for k in ["타원", "외심", "내심"]):
                score += 120

        # 5. 사인법칙 / 코사인법칙 & 삼각함수
        if is_law:
            if "코사인법칙" in item_text or "코사인 법칙" in item_text:
                score += 240
            if "사인법칙" in item_text or "사인 법칙" in item_text:
                score += 240

        if is_trig:
            if "삼각함수" in item_text:
                score += 180
            if any(k in text_lower for k in ["주기", "대칭", "최댓값"]) and (
                "그래프" in item_text or "주기" in item_text or "sin(" in item_text
            ):
                score += 170
            if "호도법" in item_text or "단위원" in item_text:
                score += 130
            if any(k in item_text for k in ["사인", "코사인", "탄젠트"]):
                score += 90

        # 6. 함수의 극한 & 연속
        if is_limit_cont:
            if any(k in text_lower for k in ["좌극한", "우극한"]) and any(
                k in item_text for k in ["좌극한", "우극한"]
            ):
                score += 280
            if any(k in text_lower for k in ["연속", "불연속", "우연속"]) and any(
                k in item_text for k in ["연속", "불연속"]
            ):
                score += 280
            if "함수의 수렴" in item_text or "함수의 극한" in cat:
                score += 220

        # 7. 미분 / 역함수 / 음함수 / 속도 / 다항함수
        if is_diff:
            if "역함수" in text_lower and "역함수의 미분" in item_text:
                score += 300
            if any(k in text_lower for k in ["음함수", "매개변수"]) and "매개변수" in item_text:
                score += 270
            if "속도" in text_lower and "속도" in item_text:
                score += 290
            if "미분가능" in text_lower and ("미분가능" in item_text or "a$ 에서 함수 $f$의 미분" in item_text):
                score += 230
            if any(k in text_lower for k in ["미분계수", "할선", "도함수"]) and any(
                k in item_text for k in ["접선에 접근하는 할선", "평균 변화율과 순간 변화율", "도함수"]
            ):
                score += 240
            if any(k in text_lower for k in ["극대", "극소", "극값", "최댓값", "변곡"]) and any(
                k in item_text for k in ["최댓값과 최솟값", "극값정리", "미분의 응용", "오목 검사"]
            ):
                score += 240
            if "접선" in text_lower and "접선" in item_text:
                score += 170
            if "미분" in item_text:
                score += 90

        if is_poly:
            if "삼차함수" in item_text or "사차함수" in item_text:
                score += 170
            elif "미분의 응용" in cat or "도함수" in cat:
                score += 90

        # 8. 적분 / 정적분 / 부정적분 / 부피
        if is_integral:
            if "정적분" in text_lower and "정적분" in item_text:
                score += 240
            elif "부정적분" in text_lower and "부정적분" in item_text:
                score += 240
            elif "상합과 하합" in item_text or "사다리꼴 근사법" in item_text or "적분의 기술" in item_text:
                score += 200
            elif "적분과 초월함수" in item_text or "적분" in item_text:
                score += 160

        # 9. 수열 & 급수
        if is_seq:
            if "등차" in text_lower and "등차" in item_text:
                score += 260
            elif "등비" in text_lower and "등비" in item_text:
                score += 260
            elif "시그마" in text_lower and "\\sum" in item_text:
                score += 250
            elif "수열" in cat or "수열" in item_text:
                score += 200
            if any(k in text_lower for k in ["극한", "급수", "수렴", "발산"]) and (
                "수열" in item_text and "극한" in item_text
            ):
                score += 260

        # 10. 지수와 로그
        if is_exp:
            if any(k in text_lower for k in ["지수함수", "지수방정식"]) and any(
                k in item_text for k in ["y=2^x", "y=a^x", "y=2^{x-a}+b"]
            ):
                score += 260
            if any(k in item_text for k in ["유리수인 지수", "지수가 유리수", "영 또는 음의 정수", "지수법칙"]):
                score += 250
            if "거듭제곱근" in text_lower and any(
                k in item_text for k in ["거듭제곱근", "제곱근(radical", "제곱근(n", "제곱근(square"]
            ):
                score += 230

        if is_log:
            if any(k in text_lower for k in ["로그함수", "평행이동", "점근선", "교점"]) and (
                "\\log_2" in item_text or "\\log_a" in item_text
            ):
                score += 280
            if "자연로그" in text_lower and "\\ln x" in item_text:
                score += 270
            if "로그의 정의" in item_text or "로그의 성질" in item_text or "로그의 뜻과 성질" in item_text:
                score += 250

        # 11. 확률과 통계
        if is_prob:
            if any(k in text_lower for k in ["신뢰구간", "모평균", "표본평균"]):
                if "표본평균" in item_text or "모집단" in item_text:
                    score += 270
                elif "표준정규분포" in item_text or "정규분포" in item_text:
                    score += 200
            elif any(k in text_lower for k in ["정규분포", "표준정규", "확률밀도"]):
                if "정규분포(normal" in item_text or "표준정규분포(standard" in item_text:
                    score += 280
                elif "확률분포(probability" in item_text:
                    score += 240
            elif any(k in text_lower for k in ["이항분포", "이산확률", "분산", "표준편차"]):
                if "확률분포" in item_text or "평균, 분산" in item_text or "평균과 분산" in item_text or "_n \\mathrm{c}_r" in item_text:
                    score += 250
            elif any(
                k in text_lower
                for k in ["조건부확률", "주사위", "동전", "카드", "주머니", "시행", "여사건", "순열", "조합", "중복조합", "중복순열", "경우의수"]
            ):
                if "시행과 사건" in item_text or "확률수업" in item_text:
                    score += 240
                elif "주사위" in text_lower and "주사위" in item_text:
                    score += 230
                elif "카드" in text_lower and "카드" in item_text:
                    score += 210
                elif "확률분포" in item_text or "_n \\mathrm{c}_r" in item_text:
                    score += 180

        # 12. 이차곡선 & 원뿔곡선
        if is_conic:
            if "단델린" in text_lower and "단델린" in item_text:
                score += 220
            if "포물선" in text_lower and "포물선" in item_text:
                score += 220
            if "타원" in text_lower and "타원" in item_text:
                score += 230
            if "쌍곡선" in text_lower and "쌍곡선" in item_text:
                score += 240
            if "점근선" in text_lower and "점근선" in item_text:
                score += 220
            if "이차곡선" in cat:
                score += 80

        # 13. 평면기하 & 삼각형
        if is_geom:
            if "피타고라스" in text_lower and "피타고라스" in title_l:
                score += 180
            if "외심" in text_lower and "외심" in title_l:
                score += 180
            if "내심" in text_lower and "내심" in title_l:
                score += 180

        # 도메인 점수가 0보다 큰 경우에만 인터랙티브 공학도구 가산점 부여 (오매칭 방지!)
        if score > 0:
            if item.get("geogebra"):
                score += 18
            if item.get("algeomath"):
                score += 14
            if item.get("pdf"):
                score += 8
            if item.get("youtube"):
                score += 5
            scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)

    results = []
    seen_urls = set()
    seen_titles = set()
    for _, it in scored:
        u = it.get("url")
        raw_t = it.get("title", "")
        t_clean = re.sub(r"[\(\[].*?[\)\]]", "", raw_t).strip()
        if u not in seen_urls and t_clean not in seen_titles:
            seen_urls.add(u)
            seen_titles.add(t_clean)
            results.append(it)
        if len(results) >= limit:
            break

    # 매칭 부족 시 대표 핵심 인터랙티브 자료로 보충
    if len(results) < limit:
        defaults = [
            it
            for it in materials
            if any(
                k in it["title"]
                for k in ["접선에 접근하는 할선", "포물선의 정의", "직각에 대한 코사인법칙", "단위원", "단델린"]
            )
            and (it.get("geogebra") or it.get("algeomath"))
        ]
        for d in defaults:
            raw_t = d.get("title", "")
            t_clean = re.sub(r"[\(\[].*?[\)\]]", "", raw_t).strip()
            if d.get("url") not in seen_urls and t_clean not in seen_titles:
                seen_urls.add(d.get("url"))
                seen_titles.add(t_clean)
                results.append(d)
            if len(results) >= limit:
                break

    return results[:limit]


def match_materials_for_problem(slug, query_text="", limit=4):
    """문항 고유 slug(예: csat27_g30)에 대한 정밀 큐레이션 우선 ID와 시맨틱 매칭을 결합 반환"""
    get_materials()
    by_id = _get_materials_by_id()
    results = []
    seen_urls = set()
    seen_titles = set()

    for cid in CSAT27_CURATED_PRIORITY_IDS.get(slug, []):
        it = by_id.get(cid)
        if not it:
            continue
        u = it.get("url", "")
        raw_t = it.get("title", "")
        t_clean = re.sub(r"[\(\[].*?[\)\]]", "", raw_t).strip()
        if u and u not in seen_urls and t_clean not in seen_titles:
            seen_urls.add(u)
            seen_titles.add(t_clean)
            results.append(it)
        if len(results) >= limit:
            return results[:limit]

    if query_text and len(results) < limit:
        for it in match_materials(query_text, limit=limit + 4):
            u = it.get("url", "")
            raw_t = it.get("title", "")
            t_clean = re.sub(r"[\(\[].*?[\)\]]", "", raw_t).strip()
            if u and u not in seen_urls and t_clean not in seen_titles:
                seen_urls.add(u)
                seen_titles.add(t_clean)
                results.append(it)
            if len(results) >= limit:
                break

    return results[:limit]


def _get_visual_tip_text(problem_title):
    t = problem_title.lower().replace("확률밀도함수", "확률밀도")

    if any(k in t for k in ["삼수선", "정사영", "이면각", "공간도형", "공간좌표", "구 s", "두 구", "육각기둥"]):
        return (
            "💡 <b>프레임별 시각적 증명 분석 (공간도형 · PDF &amp; GeoGebra 3D 탐구)</b><br>"
            "수학자료실의 공간도형·정사영 자료는 3차원 입체 속에서 <b>수직 조건과 이면각이 평면 삼각형으로 환원되는 과정</b>을 입체적으로 보여줍니다.<br>"
            "• <b>[삼수선의 정리]</b> 평면 밖 한 점에서 평면에 내린 수선의 발과, 그 발에서 평면 위 직선에 내린 수선이 어떻게 공간의 빗변 수직을 결정하는지 3D 회전으로 관찰<br>"
            "• <b>[정사영과 법선벡터]</b> 두 평면 사이의 이면각 $\\theta$가 두 평면의 법선벡터가 이루는 각과 일치하므로 $\\cos\\theta$만으로 정사영 넓이 $S'=S\\cos\\theta$가 즉시 계산되는 원리<br>"
            "• <b>[핵심 연결]</b> 하단 GeoGebra 3D·증명 PDF를 직접 돌려가며 입체 보조선의 수직 구조를 체득해 보세요."
        )
    elif any(k in t for k in ["벡터", "평면벡터", "내적", "실수배", "위치벡터"]):
        return (
            "💡 <b>프레임별 시각적 증명 분석 (벡터 연산 · 내적 기하 PDF &amp; GeoGebra 탐구)</b><br>"
            "수학자료실의 벡터 자료는 식을 넘어 <b>화살표의 이동·평행사변형 영역(자취)·정사영 내적</b>을 동적 기하로 한눈에 드러냅니다.<br>"
            "• <b>[벡터의 실수배와 자취]</b> 두 독립 변수 $t, s \\in [0, 1]$이 결합한 $\\overrightarrow{\\mathrm{OR}} = 2\\overrightarrow{\\mathrm{OP}} - \\overrightarrow{\\mathrm{OQ}}$가 평행사변형 영역 전체를 쓸어내는 원리<br>"
            "• <b>[내적의 기하적 최대·최소]</b> 내적 $\\overrightarrow{\\mathrm{OR}}\\cdot\\overrightarrow{\\mathrm{BR}}$을 기준 중점으로부터의 거리 제곱이나 정사영 길이로 변환하여 최적점을 1초 만에 포착하는 시각화<br>"
            "• <b>[핵심 연결]</b> 하단 자료의 벡터 평행사변형 영역·내적 범위 앱렛으로 직관적 의미를 확인해 보세요."
        )
    elif any(k in t for k in ["좌극한", "우극한", "함수의 극한", "연속", "불연속", "함수의극한", "함수의연속"]):
        return (
            "💡 <b>프레임별 시각적 증명 분석 (함수의 극한·연속 PDF &amp; GeoGebra 탐구)</b><br>"
            "수학자료실의 극한·연속 자료는 $x \\to a-$와 $x \\to a+$일 때 점 $(x, f(x))$가 그래프를 타고 <b>목표 높이를 향해 좌우에서 접근하는 순간</b>을 프레임별로 보여줍니다.<br>"
            "• <b>[좌극한과 우극한의 분리]</b> 그래프가 끊어진 지점에서 왼쪽에서 다가갈 때의 y값과 오른쪽에서 다가갈 때의 y값이 어떻게 달라지는지 동점 애니메이션으로 확인<br>"
            "• <b>[연속의 3조건]</b> 함숫값 $f(a)$, 극한값 $\\lim_{x\\to a}f(x)$의 존재, 그리고 두 값의 일치가 곱함수·합성함수의 연속 판정에 어떻게 결합되는지 하단 자료로 탐구해 보세요."
        )
    elif any(k in t for k in ["로그", "로그함수", "자연로그"]):
        return (
            "💡 <b>프레임별 시각적 증명 분석 (로그의 성질 · 로그함수 평행이동 PDF &amp; AlgeoMath 탐구)</b><br>"
            "수학자료실의 로그·로그함수 자료는 지수의 역함수로서의 대칭성과 <b>$y=\\log_2(x-a)+b$의 점근선·평행이동</b>을 눈앞에 펼쳐 보여줍니다.<br>"
            "• <b>[밑 변환과 대수 법칙]</b> $\\log_a b = \\frac{\\log_c b}{\\log_c a}$가 왜 지수법칙과 완벽히 맞물리는지 단계별 플립북으로 증명<br>"
            "• <b>[평행이동과 좌표 기하]</b> 곡선 $y=\\log_2 x$를 $(a, b)$만큼 평행이동할 때 점근선 $x=a$와 교점·무게중심이 함께 이동하는 모습을 하단 자료와 AlgeoMath로 확인해 보세요."
        )
    elif any(k in t for k in ["사인법칙", "코사인법칙", "사인 법칙", "코사인 법칙"]):
        return (
            "💡 <b>프레임별 시각적 증명 분석 (PDF &amp; GeoGebra 탐구)</b><br>"
            "수학자료실의 PDF 자료는 페이지를 한 장씩 넘길 때마다 <b>기하학적 사고의 전 과정이 애니메이션처럼 펼쳐집니다.</b><br>"
            "• <b>[기초 설정]</b> 삼각형 $\\triangle\\mathrm{ABC}$에서 대변 $a, b, c$를 지정합니다.<br>"
            "• <b>[보조선의 탄생]</b> 꼭짓점 $\\mathrm{A}$에서 대변에 수선 $\\mathrm{AD}$를 내려 두 직각삼각형으로 분할하고 각 삼각비를 투영합니다.<br>"
            "• <b>[각도에 따른 동적 변화]</b> <b>예각일 때</b>($a = \\overline{\\mathrm{BD}} + \\overline{\\mathrm{CD}}$)와 <b>둔각일 때</b>(수선의 발 $\\mathrm{D}$가 바깥으로 나가 $a = \\overline{\\mathrm{BD}} - \\overline{\\mathrm{CD}}$)의 외견상 차이가, "
            "보각 공식 $\\cos(\\pi - \\mathrm{C}) = -\\cos\\mathrm{C}$에 의해 음수가 양수로 상쇄되며 동일한 법칙 $a = c\\cos\\mathrm{B} + b\\cos\\mathrm{C}$로 수렴합니다.<br>"
            "• <b>[수학적 의미]</b> 단순 암기가 아닌, 각이 회전함에 따라 삼각함수가 기하학적 부호를 스스로 조율하는 연속성의 아름다움을 하단 PDF와 앱렛에서 확인해 보세요."
        )
    elif any(k in t for k in ["미분계수", "접선", "도함수", "미분가능", "역함수의미분", "음함수의미분"]):
        return (
            "💡 <b>프레임별 시각적 증명 분석 (PDF &amp; GeoGebra 탐구)</b><br>"
            "수학자료실의 PDF 자료는 페이지를 넘길 때마다 <b>미분계수가 탄생하는 극한의 전 과정이 생생하게 드러납니다.</b><br>"
            "• <b>[초기 상태]</b> 곡선 $y=f(x)$ 위의 고정점 $\\mathrm{P}(a, f(a))$와 멀리 떨어진 동점 $\\mathrm{Q}(x, f(x))$를 잇는 초록색 할선(Secant)의 평균변화율 $\\frac{f(x)-f(a)}{x-a}$을 그립니다.<br>"
            "• <b>[프레임의 연속 이동]</b> $x \\to a$로 접근함에 따라, 곡선을 타고 미끄러지는 동점 $\\mathrm{Q}$와 함께 초록색 할선이 연속적으로 회전합니다.<br>"
            "• <b>[극한의 합일]</b> 마지막 순간, 초록색 할선이 빨간색 접선(Tangent)과 일치하며 순간변화율 $m = \\lim_{x\\to a}\\frac{f(x)-f(a)}{x-a}$에 도달합니다.<br>"
            "• <b>[수학적 의미]</b> 미분은 형식적인 수식 연산이 아니라, 두 점 사이의 할선이 한 점에서의 접선으로 녹아드는 기하학적 수렴 과정임을 하단 자료로 확인해 보세요."
        )
    elif any(k in t for k in ["삼차함수", "사차함수", "극값", "극대", "극소", "변곡점"]):
        return (
            "💡 <b>프레임별 시각적 증명 분석 (PDF &amp; GeoGebra 탐구)</b><br>"
            "수학자료실의 PDF 자료는 삼차·사차함수 그래프의 <b>숨겨진 대칭성과 비율 관계</b>를 단계별로 명쾌하게 드러냅니다.<br>"
            "• <b>[도함수의 뿌리]</b> 도함수 $f'(x)=0$의 두 실근에서 원래 함수 $f(x)$의 극대와 극소가 형성되는 역학적 관계를 추적합니다.<br>"
            "• <b>[변곡점과 대칭]</b> 극대점과 극소점의 정중앙에 위치한 변곡점을 중심으로 점대칭을 이루는 프레임별 도형 관찰<br>"
            "• <b>[비율의 기하학]</b> 극값을 지나는 접선과 곡선이 다시 만나는 점 사이의 $1 : 2$ 및 $1 : \\sqrt{3}$ 비율 관계가 왜 필연적으로 성립하는지 하단 자료의 시각적 분할로 확인해 보세요."
        )
    elif any(k in t for k in ["삼각함수", "사인함수", "코사인함수", "탄젠트", "주기"]):
        return (
            "💡 <b>프레임별 시각적 증명 분석 (PDF &amp; GeoGebra 탐구)</b><br>"
            "수학자료실의 PDF 자료는 원운동이 파동 곡선으로 풀려나가는 <b>기하학적 전개 과정</b>을 한 프레임씩 보여줍니다.<br>"
            "• <b>[단위원의 동점]</b> 반지름 $1$인 원 위를 반시계 방향으로 회전하는 동점 $\\mathrm{P}$의 회전각 $\\theta$와 수직 투영 $y=\\sin\\theta$, 수평 투영 $x=\\cos\\theta$ 설정<br>"
            "• <b>[주기의 필연성]</b> 한 바퀴($2\\pi$) 회전하면 원점으로 귀환하는 원의 닫힌 궤적이 파동 함수의 무한 반복 주기성과 대칭성으로 승화되는 원리를 하단 자료에서 체득해 보세요."
        )
    elif any(k in t for k in ["적분", "정적분", "부정적분", "구분구적법", "입체도형의부피"]):
        return (
            "💡 <b>프레임별 시각적 증명 분석 (PDF &amp; GeoGebra 탐구)</b><br>"
            "수학자료실의 PDF 자료는 곡선 아래의 불규칙한 넓이가 <b>직사각형들의 무한 분할로 채워지는 과정</b>을 단계별로 보여줍니다.<br>"
            "• <b>[균등 분할]</b> 구간 $[a, b]$를 $n$개의 미세 구간으로 나누고, 각 구간에서 세운 직사각형의 넓이 합(상합·하합)을 구성합니다.<br>"
            "• <b>[미적분학의 기본정리]</b> 무한히 쪼갠 직사각형의 극한합이 부정적분의 함숫값 차이 $F(b)-F(a)$와 정확히 일치하는 연결을 하단 자료의 프레임 넘김으로 확인해 보세요."
        )
    elif any(k in t for k in ["수열", "등차", "등비", "급수", "시그마"]):
        return (
            "💡 <b>프레임별 시각적 증명 분석 (PDF &amp; GeoGebra 탐구)</b><br>"
            "수학자료실의 PDF 자료는 수열의 추상적 항들이 <b>규칙적인 도형 합과 극한의 면적으로 실체화되는 과정</b>을 한 장씩 보여줍니다.<br>"
            "• <b>[수열의 규칙과 합]</b> 등차·등비수열과 시그마($\\sum k, \\sum k^2, \\sum k^3$) 공식이 기하학적 블록 결합으로 증명되는 단계별 전개<br>"
            "• <b>[등비급수와 수렴]</b> 무한등비수열이 공비 조건 $|r| < 1$에서 목표값으로 수렴하는 궤적을 하단 자료에서 확인해 보세요."
        )
    elif any(k in t for k in ["거듭제곱근", "지수법칙", "지수함수", "지수방정식"]):
        return (
            "💡 <b>프레임별 시각적 증명 분석 (PDF &amp; GeoGebra 탐구)</b><br>"
            "수학자료실의 PDF 자료는 지수가 자연수에서 정수, 유리수, 실수로 <b>수체계가 확장될 때 규칙이 어떻게 보존되는지</b>를 단계별로 증명합니다.<br>"
            "• <b>[유리수 지수의 확장]</b> $a^m \\times a^n = a^{m+n}$의 지수법칙이 $a^0 = 1$, $a^{-n} = \\frac{1}{a^n}$, $\\sqrt[n]{a^m}=a^{\\frac{m}{n}}$으로 확장되는 논리적 필연성<br>"
            "• <b>[거듭제곱근의 기하학]</b> $x^n = a$의 실근 개수가 지수 $n$의 홀·짝성과 부호에 따라 그래프 교점으로 갈라지는 구조를 하단 자료에서 확인해 보세요."
        )
    elif any(k in t for k in ["원의 방정식", "원과 직선", "원의 접선"]):
        return (
            "💡 <b>프레임별 시각적 증명 분석 (PDF &amp; GeoGebra 탐구)</b><br>"
            "수학자료실의 PDF 자료는 원의 완벽한 대칭성과 <b>직선 사이의 위치 관계</b>를 기하학적 보조선으로 증명합니다.<br>"
            "• <b>[거리의 정의]</b> 중심 $(a, b)$에서 일정한 거리 $r$만큼 떨어진 점들의 자취로부터 원의 방정식 유도<br>"
            "• <b>[접선과 직각]</b> 중심에서 접점에 내린 반지름은 접선과 언제나 수직($90^\\circ$)을 이룬다는 대원칙을 하단 자료에서 확인해 보세요."
        )
    elif any(k in t for k in ["포물선", "타원", "쌍곡선", "원뿔곡선", "단델린"]):
        return (
            "💡 <b>프레임별 시각적 증명 분석 (PDF &amp; GeoGebra 탐구)</b><br>"
            "수학자료실의 PDF 자료는 <b>원뿔곡선(포물선·타원·쌍곡선)의 초점·준선·점근선 작도 원리</b>를 단계별로 증명합니다.<br>"
            "• <b>[정의의 직접 시각화]</b> 초점까지의 거리와 준선 거리(포물선), 거리 합(타원), 거리 차와 점근선(쌍곡선)이 움직이는 동점과 함께 실시간 보존되는 원리<br>"
            "• <b>[핵심 연결]</b> 하단의 GeoGebra·AlgeoMath·증명 PDF에서 직접 초점과 준선을 움직이며 불변량을 체험해 보세요."
        )
    elif any(k in t for k in ["정규분포", "표준정규", "확률밀도", "신뢰구간", "모평균", "표본평균"]):
        return (
            "💡 <b>프레임별 시각적 증명 분석 (PDF &amp; GeoGebra 탐구)</b><br>"
            "수학자료실의 정규분포·표본분포 자료는 <b>종 모양 곡선의 대칭성과 표준화($Z$)·모평균 추정 원리</b>를 동적 기하로 한눈에 보여줍니다.<br>"
            "• <b>[표준화와 신뢰구간]</b> 모평균 $m$과 표본평균 $\\bar{X}$의 분포를 $\\sigma / \\sqrt{n}$ 폭과 $Z$ 변환으로 연결해 하단 GeoGebra 앱렛과 증명 PDF로 확인해 보세요."
        )
    elif any(k in t for k in ["확률", "이항분포", "조합", "순열", "중복", "경우의", "조건부확률"]):
        return (
            "💡 <b>프레임별 시각적 증명 분석 (PDF &amp; GeoGebra 탐구)</b><br>"
            "수학자료실의 확률·통계 자료는 <b>표본공간의 구조적 분할, 확률분포표, 기대값·분산($E(aX+b), V(aX+b)$)의 원리</b>를 투명하게 시각화합니다.<br>"
            "하단의 관련 자료에서 단계별 플립북 증명과 시뮬레이션 도구를 직접 탐색해 보세요."
        )
    else:
        return (
            "💡 <b>프레임별 시각적 증명 분석 (PDF &amp; GeoGebra 탐구)</b><br>"
            "수학자료실의 PDF 자료는 단순 결과가 아닌 <b>처음부터 끝까지 생각의 모든 과정이 투명하게 드러나는 단계별 시각적 증명</b>입니다.<br>"
            "하단의 <b>수학자료실</b> PDF 문서와 공학도구를 넘겨가며, 각 프레임마다 변하는 요소와 보존되는 불변량을 깊이 있게 음미해 보세요."
        )


def _clean_pdf_url(url_val):
    if not url_val:
        return ""
    base = re.sub(r"(#toolbar=0.*)+$", "", url_val)
    return f"{base}#toolbar=0&view=Fit&scrollbar=0"


def _clean_algeo_url(url_val):
    if not url_val:
        return ""
    return re.sub(r"#toolbar=0.*$", "", url_val)


def _append_visual_links(tip_html, matched_items):
    """시각적 팁 박스 내부에 직접 조작 가능한 GeoGebra 및 PDF/영상 링크 바 결합"""
    if not matched_items:
        return tip_html

    links_html = '<div class="min-visual-links" style="margin-top:14px;padding-top:12px;border-top:1px dashed rgba(0,99,152,.3);display:flex;flex-direction:column;gap:10px;">'
    links_html += '<div style="font-weight:700;color:#006398;font-size:.85rem;display:flex;align-items:center;gap:6px"><span>🔗 위 시각적 증명과 직결된 핵심 자료:</span></div>'
    for it in matched_items[:2]:
        t_name = html.escape(it.get("title", "관련 자료"))
        sub = it.get("sub", "")
        u = html.escape(it.get("url", ""))
        pdf = _clean_pdf_url(it.get("pdf", ""))
        ggb = it.get("geogebra", "")
        algeo = _clean_algeo_url(it.get("algeomath", ""))
        yt = it.get("youtube", "")

        links_html += '<div class="min-tip-item" style="background:#ffffff;border:1px solid rgba(0,99,152,0.22);border-radius:10px;padding:10px 14px;display:flex;flex-direction:column;gap:8px">'
        links_html += '<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:6px">'
        sub_text = (
            f' <span style="font-size:.76rem;color:#64748b;font-weight:400">({html.escape(sub)})</span>'
            if (sub and sub not in it.get("title", ""))
            else ""
        )
        links_html += f'<a href="{u}" target="_blank" rel="noopener" style="font-weight:700;color:#006398;text-decoration:none;font-size:.88rem;display:inline-flex;align-items:center;gap:6px"><span style="font-size:1rem">📌</span> {t_name}{sub_text}</a>'
        links_html += '<span style="font-size:.72rem;background:#e0f2fe;color:#0369a1;padding:2px 8px;border-radius:6px;border:1px solid #bae6fd;font-weight:700">시각적 탐구</span></div>'

        actions = '<div class="min-item-actions" style="display:flex;gap:6px;flex-wrap:wrap;align-items:center">'
        if ggb:
            ggb_e = html.escape(ggb, quote=True)
            actions += f'<button type="button" class="min-btn min-btn-ggb" onclick="toggleMinGgb(this, \'{ggb_e}\')" title="페이지 내에서 GeoGebra 직접 조작">📐 GeoGebra 조작 ▾</button>'
            actions += f'<a href="{ggb_e}" target="_blank" rel="noopener" class="min-btn min-btn-ggb" style="opacity:.9" title="GeoGebra Tube 새 창 열기">Tube ↗</a>'
        if algeo:
            actions += f'<a href="{html.escape(algeo, quote=True)}" target="_blank" rel="noopener" class="min-btn min-btn-algeo" title="AlgeoMath 공학도구 열기">🔢 AlgeoMath</a>'
        if pdf:
            actions += f'<a href="{html.escape(pdf, quote=True)}" target="_blank" rel="noopener" class="min-btn min-btn-pdf" title="단계별 플립북 시각적 증명 PDF">📄 단계별 증명 PDF</a>'
        if yt:
            actions += f'<a href="{html.escape(yt, quote=True)}" target="_blank" rel="noopener" class="min-btn min-btn-yt" title="동적 기하 해설 영상">🎥 해설 강의</a>'
        if u:
            actions += f'<a href="{u}" target="_blank" rel="noopener" class="min-btn min-btn-detail">웹 상세 탐구 ➔</a>'
        actions += "</div>"
        links_html += actions
        if ggb:
            links_html += '<div class="min-ggb-frame-wrap"></div>'
        links_html += "</div>"

    links_html += '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;padding-top:4px">'
    links_html += '<a href="#min7014-addon" style="color:#006398;font-size:.82rem;font-weight:700;text-decoration:none;display:inline-flex;align-items:center;gap:4px"><span>👇</span> 하단 연계 심층 탐구 자료실 전체 보기 ➔</a>'
    links_html += '<a href="https://min7014.github.io/" target="_blank" rel="noopener" style="color:#4f46e5;font-size:.82rem;font-weight:700;text-decoration:none;display:inline-flex;align-items:center;gap:4px"><span>🌐</span> 수학자료실 메인 (3,400+ 주제) ↗</a>'
    links_html += "</div></div>"
    return tip_html + "\n" + links_html


def get_visual_tip(problem_title, matched_items=None):
    """문제 주제에 맞는 '프레임별 시각적 증명' 심층 분석 디딤돌 팁 (관련 자료 바로가기 링크 포함)"""
    if not matched_items:
        matched_items = match_materials(problem_title, limit=4)
    tip_text = _get_visual_tip_text(problem_title)
    return _append_visual_links(tip_text, matched_items)


def build_solution_material_links_html(matched_items, lang="ko"):
    """상세 해설 내부에 삽입되는 문항별 수학자료실 원문·PDF·GeoGebra·AlgeoMath·유튜브 직결 블록"""
    if not matched_items:
        return ""
    is_en = lang == "en"
    hdr = (
        "🔗 [Direct Visual Proofs &amp; Interactive Tools from Math Archive]"
        if is_en
        else "🔗 [이 문항과 직결된 수학자료실 시각 증명 · 공학도구 바로가기]"
    )
    items_li = []
    for it in matched_items[:3]:
        title_esc = html.escape(it.get("title", ""))
        u = html.escape(it.get("url", "https://min7014.github.io/"))
        pdf = _clean_pdf_url(it.get("pdf", ""))
        ggb = it.get("geogebra", "")
        algeo = _clean_algeo_url(it.get("algeomath", ""))
        yt = it.get("youtube", "")
        chips = [
            f'<a href="{u}" target="_blank" rel="noopener" style="color:#0369a1;font-weight:700;text-decoration:underline">{"Web Lesson ↗" if is_en else "웹 원문 ↗"}</a>'
        ]
        if pdf:
            chips.append(
                f'<a href="{html.escape(pdf, quote=True)}" target="_blank" rel="noopener" style="color:#b45309;font-weight:700;text-decoration:underline">{"PDF Proof ↗" if is_en else "단계별 증명 PDF ↗"}</a>'
            )
        if ggb:
            chips.append(
                f'<a href="{html.escape(ggb, quote=True)}" target="_blank" rel="noopener" style="color:#047857;font-weight:700;text-decoration:underline">GeoGebra ↗</a>'
            )
        if algeo:
            chips.append(
                f'<a href="{html.escape(algeo, quote=True)}" target="_blank" rel="noopener" style="color:#6d28d9;font-weight:700;text-decoration:underline">AlgeoMath ↗</a>'
            )
        if yt:
            chips.append(
                f'<a href="{html.escape(yt, quote=True)}" target="_blank" rel="noopener" style="color:#be123c;font-weight:700;text-decoration:underline">{"YouTube ↗" if is_en else "유튜브 해설 ↗"}</a>'
            )
        items_li.append(f'  <li><b>{title_esc}</b> — {" · ".join(chips)}</li>')
    return (
        f'\n<div class="sol-archive-links" style="margin-top:12px;padding:12px 14px;border-radius:10px;background:#f0f9ff;border:1px solid #bae6fd">'
        f'<div style="font-weight:800;color:#0369a1;margin-bottom:6px;font-size:0.9rem">{hdr}</div>'
        f'<ul style="margin:0;padding-left:18px;line-height:1.75;font-size:0.87rem">\n'
        + "\n".join(items_li)
        + "\n</ul>\n</div>\n"
    )


def generate_addon_card_html(materials, problem_title=""):
    """퀴즈 화면에 삽입되는 수학자료실 추가 자료 카드 HTML 생성"""
    if not materials:
        materials = match_materials(problem_title, limit=4)

    items_html = ""
    for it in materials:
        raw_title = it.get("title", "")
        m = re.match(r"^(.*?)\s*[\(\[]([A-Za-z][^가-힣]*?)[\)\]]\s*$", raw_title)
        if m:
            ko_part = m.group(1).strip()
            en_part = m.group(2).strip()
        else:
            ko_part = raw_title
            en_part = ""

        url = html.escape(it.get("url", "https://min7014.github.io/"))
        sub_html = f'<span class="min-item-sub">{html.escape(en_part)}</span>' if en_part else ""

        category = it.get("category", "")
        cat_html = f'<div class="min-cat-badge">📂 {html.escape(category)}</div>' if category else ""

        pdf = _clean_pdf_url(it.get("pdf", ""))
        yt = it.get("youtube", "")
        ggb = it.get("geogebra", "")
        algeo = _clean_algeo_url(it.get("algeomath", ""))

        actions = []
        if ggb:
            ggb_e = html.escape(ggb, quote=True)
            actions.append(
                f'<button type="button" class="min-btn min-btn-ggb" onclick="toggleMinGgb(this, \'{ggb_e}\')" title="페이지 내에서 GeoGebra 직접 조작">📐 GeoGebra 조작 ▾</button>'
            )
            actions.append(
                f'<a href="{ggb_e}" target="_blank" rel="noopener" class="min-btn min-btn-ggb" style="opacity:.85" title="GeoGebra Tube 새 창 열기">Tube ↗</a>'
            )
        if algeo:
            actions.append(
                f'<a href="{html.escape(algeo, quote=True)}" target="_blank" rel="noopener" class="min-btn min-btn-algeo" title="AlgeoMath 공학도구 열기">🔢 AlgeoMath</a>'
            )
        if pdf:
            actions.append(
                f'<a href="{html.escape(pdf, quote=True)}" target="_blank" rel="noopener" class="min-btn min-btn-pdf" title="단계별 플립북 시각적 증명 PDF">📄 단계별 증명 PDF</a>'
            )
        if yt:
            actions.append(
                f'<a href="{html.escape(yt, quote=True)}" target="_blank" rel="noopener" class="min-btn min-btn-yt" title="동적 기하 해설 영상">🎥 해설 강의</a>'
            )

        actions.append(
            f'<a href="{url}" target="_blank" rel="noopener" class="min-btn min-btn-detail">웹 상세 탐구 ➔</a>'
        )
        actions_str = " ".join(actions)

        items_html += f"""
        <div class="min-item">
          <div class="min-item-main">
            {cat_html}
            <a href="{url}" target="_blank" rel="noopener" class="min-item-title">
              <span class="min-bullet">📌</span> {html.escape(ko_part)}
              {sub_html}
            </a>
          </div>
          <div class="min-item-actions">
            {actions_str}
          </div>
          <div class="min-ggb-frame-wrap"></div>
        </div>
        """

    return f"""
<!-- 📚 수학자료실 공식 연계 심층 탐구 자료 카드 -->
<div id="min7014-addon" class="min7014-addon-card">
  <div class="min-header">
    <div class="min-header-title">
      <img src="../assets/favicon.png" alt="수학자료실" class="min-logo">
      <span>📚 수학자료실 공식 연계 심층 탐구</span>
    </div>
    <span class="min-tag">GeoGebra · AlgeoMath · 단계별 증명 PDF</span>
  </div>
  <p class="min-lead">이 문제와 관련된 수학적 원리를 <b>수학자료실</b>의 시각적 동적 기하 조작 및 원리 증명 자료와 함께 더 깊이 탐구해보세요.</p>

  <div class="min-guide-banner" style="background:#f0f7ff;border:1px solid rgba(0,99,152,0.22);border-radius:10px;padding:12px 16px;margin-bottom:16px;font-size:.85rem;line-height:1.6;color:#1e293b">
    🎬 <b>자료를 깊이 있게 감상하는 법</b>: 수학자료실의 PDF는 책장을 넘기듯 페이지를 넘겨갈 때마다 <b>도형의 점이 이동하고 보조선이 더해지며 수식이 스스로 완성되는 '단계별 플립북 애니메이션 증명'</b>입니다. 상단 미리보기나 새 창에서 키보드 방향키나 마우스 휠로 페이지를 넘기며, <b>각 프레임마다 변하는 요소와 보존되는 원리의 의미</b>를 곱씹어 보세요.
  </div>

  <div class="min-list">
    {items_html}
  </div>

  <div class="min-footer">
    <a href="https://min7014.github.io/" target="_blank" rel="noopener" class="min-footer-link">
      🌐 수학자료실 메인 바로가기 (3,400+ GeoGebra &amp; 증명 PDF) ➔
    </a>
  </div>
</div>

<script>
if (!window.toggleMinGgb) {{
  window.toggleMinGgb = function(btn, ggbUrl) {{
    var item = btn.closest ? btn.closest('.min-item, .min-tip-item') : btn.parentElement.parentElement;
    if (!item) return;
    var wrap = item.querySelector('.min-ggb-frame-wrap');
    if (!wrap) return;
    if (wrap.classList.contains('active')) {{
      wrap.classList.remove('active');
      wrap.innerHTML = '';
      btn.innerHTML = '📐 GeoGebra 조작 ▾';
    }} else {{
      var m = ggbUrl.match(/geogebra\\.org\\/m\\/([a-zA-Z0-9]+)/);
      var id = m ? m[1] : '';
      var src = id ? ('https://www.geogebra.org/material/iframe/id/' + id + '/width/740/height/480/border/888888/sfsb/true/smb/false/stb/false/stbh/false/ai/false/asb/false/sri/false/rc/false/ld/false/sdz/false/ctl/false') : ggbUrl;
      wrap.innerHTML = '<iframe src="' + src + '" style="width:100%;height:480px;border:0;border-radius:10px;display:block;" allowfullscreen></iframe>';
      wrap.classList.add('active');
      btn.innerHTML = '📐 GeoGebra 조작 닫기 ▴';
    }}
  }};
}}
</script>
"""
