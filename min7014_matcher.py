"""min7014.github.io 수학자료실 연계 정밀 분석, 추천 및 인터랙티브 HTML 생성 모듈
- 민은기 선생님의 평생 교육 철학: '모든 과정이 다 드러나게 하는 단계별 시각적 플립북 증명' 전수 반영
"""
import json
import os
import re
import html

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MATERIALS_PATH = os.path.join(BASE_DIR, "assets", "min7014_materials.json")

_CACHED_MATERIALS = None

def get_materials():
    global _CACHED_MATERIALS
    if _CACHED_MATERIALS is None:
        if os.path.exists(MATERIALS_PATH):
            with open(MATERIALS_PATH, "r", encoding="utf-8") as f:
                _CACHED_MATERIALS = json.load(f)
        else:
            _CACHED_MATERIALS = []
    return _CACHED_MATERIALS

def match_materials(text, limit=4):
    materials = get_materials()
    if not materials:
        return []

    text_lower = text.lower()
    scored = []

    is_circle = ('원의 방정식' in text_lower) or ('원' in text_lower and any(k in text_lower for k in ['거리', '직선', '접선', '중심', '반지름']))
    is_trig = any(k in text_lower for k in ['삼각함수', '삼각비', '단위원', '호도법', '주기'])
    is_law = any(k in text_lower for k in ['사인법칙', '코사인법칙', '사인 법칙', '코사인 법칙'])
    is_diff = any(k in text_lower for k in ['미분', '접선', '도함수', '할선', '미분계수', '미분가능', '변곡점', '극대', '극소'])
    is_poly = any(k in text_lower for k in ['삼차함수', '사차함수', '다항함수'])
    is_integral = any(k in text_lower for k in ['적분', '정적분', '부정적분', '구분구적법', '넓이'])
    is_seq = any(k in text_lower for k in ['수열', '등차', '등비', '시그마', '점화식', '급수'])
    is_exp = any(k in text_lower for k in ['지수', '거듭제곱', '로그', '밑'])
    is_prob = any(k in text_lower for k in ['확률', '독립', '통계', '정규분포', '순열', '조합'])
    is_conic = any(k in text_lower for k in ['포물선', '타원', '쌍곡선', '원뿔곡선', '단델린', '초점', '준선'])
    is_geom = any(k in text_lower for k in ['피타고라스', '외심', '내심', '무게중심', '수심', '방심', '작도'])

    for item in materials:
        title = item.get("title", "")
        item_text = f"{title} {' '.join(item.get('tags', []))} {item.get('category', '')}".lower()
        score = 0

        # 1. 원의 방정식
        if is_circle:
            if any(k in item_text for k in ['타원', '쌍곡선', '포물선', '원뿔']):
                score -= 100
            elif '원의 방정식' in item_text:
                score += 220
            elif '원의 접선' in item_text or '원과 직선' in item_text:
                score += 180
            elif '원 위의 점' in item_text and '접선' in item_text:
                score += 170
            elif '원의' in item_text and not any(k in item_text for k in ['타원', '외심', '내심']):
                score += 120

        # 2. 삼각함수 & 주기
        if is_trig:
            if '삼각함수' in item_text: score += 180
            if '주기' in item_text: score += 150
            if '호도법' in item_text or '단위원' in item_text: score += 140
            if any(k in item_text for k in ['사인', '코사인', '탄젠트']): score += 100

        # 3. 사인/코사인법칙
        if is_law:
            if '코사인법칙' in item_text or '코사인 법칙' in item_text: score += 200
            if '사인법칙' in item_text or '사인 법칙' in item_text: score += 200

        # 4. 미분 / 접선 / 미분가능성
        if is_diff:
            if '미분가능' in text_lower and '미분가능' in item_text: score += 220
            if '접선' in text_lower and '접선' in item_text: score += 160
            if '할선' in item_text: score += 150
            if '도함수' in item_text or '미분계수' in item_text: score += 140
            if '미분' in item_text: score += 110

        # 5. 다항함수 / 삼차함수
        if is_poly:
            if '삼차함수' in item_text: score += 180
            if '사차함수' in item_text: score += 180
            if '접선' in item_text or '도함수' in item_text: score += 80

        # 6. 적분
        if is_integral:
            if '정적분' in text_lower and '정적분' in item_text: score += 200
            elif '부정적분' in text_lower and '부정적분' in item_text: score += 200
            elif '적분' in item_text: score += 150
            if '구분구적법' in item_text: score += 140

        # 7. 수열 & 급수
        if is_seq:
            if '등차수열' in text_lower and '등차수열' in item_text: score += 200
            elif '등비수열' in text_lower and '등비수열' in item_text: score += 200
            elif '수열의 극한' in text_lower and '수열' in item_text and '극한' in item_text: score += 200
            elif '수열' in item_text: score += 140

        # 8. 지수와 로그
        if is_exp:
            if '지수법칙' in item_text: score += 200
            if '거듭제곱근' in item_text: score += 190
            if '로그' in text_lower and '로그' in item_text: score += 180

        # 9. 확률과 통계
        if is_prob:
            if '정규분포' in text_lower and '정규분포' in item_text: score += 200
            elif '확률분포' in item_text or '정규분포' in item_text: score += 160
            elif '확률' in item_text: score += 120

        # 10. 이차곡선 & 원뿔곡선
        if is_conic:
            if '단델린' in text_lower and '단델린' in item_text: score += 220
            if '포물선' in text_lower and '포물선' in item_text: score += 200
            if '타원' in text_lower and '타원' in item_text: score += 200
            if '쌍곡선' in text_lower and '쌍곡선' in item_text: score += 200
            if '원뿔곡선' in item_text or '이차곡선' in item_text: score += 150

        # 11. 평면기하 & 삼각형
        if is_geom:
            if '피타고라스' in text_lower and '피타고라스' in item_text: score += 180
            if '무게중심' in text_lower and '무게중심' in item_text: score += 180
            if '외심' in text_lower and '외심' in item_text: score += 180
            if '내심' in text_lower and '내심' in item_text: score += 180

        # 인터랙티브 공학도구 가산점
        if item.get("geogebra"): score += 18
        if item.get("algeomath"): score += 14
        if item.get("pdf"): score += 6
        if item.get("youtube"): score += 4

        if score > 0:
            scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)
    
    results = []
    seen_urls = set()
    seen_titles = set()
    for _, it in scored:
        u = it.get('url')
        raw_t = it.get('title', '')
        t_clean = re.sub(r'[\(\[].*?[\)\]]', '', raw_t).strip()
        if u not in seen_urls and t_clean not in seen_titles:
            seen_urls.add(u)
            seen_titles.add(t_clean)
            results.append(it)
        if len(results) >= limit:
            break

    # 매칭 부족 시 대표 핵심 인터랙티브 자료로 보충
    if len(results) < limit:
        defaults = [
            it for it in materials 
            if any(k in it['title'] for k in ['접선에 접근하는 할선', '포물선의 정의', '직각에 대한 코사인법칙', '단위원', '단델린'])
            and (it.get('geogebra') or it.get('algeomath'))
        ]
        for d in defaults:
            raw_t = d.get('title', '')
            t_clean = re.sub(r'[\(\[].*?[\)\]]', '', raw_t).strip()
            if d.get('url') not in seen_urls and t_clean not in seen_titles:
                seen_urls.add(d.get('url'))
                seen_titles.add(t_clean)
                results.append(d)
            if len(results) >= limit:
                break

    return results[:limit]

def _get_visual_tip_text(problem_title):
    t = problem_title.lower()
    
    if any(k in t for k in ['사인법칙', '코사인법칙', '사인 법칙', '코사인 법칙']):
        return (
            "💡 <b>민은기 선생님의 프레임별 시각적 증명 분석 (PDF & GeoGebra 탐구)</b><br>"
            "선생님의 PDF 자료는 페이지를 한 장씩 넘길 때마다 <b>기하학적 사고의 전 과정이 애니메이션처럼 펼쳐집니다.</b><br>"
            "• <b>[기초 설정]</b> 삼각형 $\\triangle\\mathrm{ABC}$에서 대변 $a, b, c$를 지정합니다.<br>"
            "• <b>[보조선의 탄생]</b> 꼭짓점 $\\mathrm{A}$에서 대변에 수선 $\\mathrm{AD}$를 내려 두 직각삼각형으로 분할하고 각 삼각비를 투영합니다.<br>"
            "• <b>[각도에 따른 동적 변화]</b> <b>예각일 때</b>($a = \\overline{\\mathrm{BD}} + \\overline{\\mathrm{CD}}$)와 <b>둔각일 때</b>(수선의 발 $\\mathrm{D}$가 바깥으로 나가 $a = \\overline{\\mathrm{BD}} - \\overline{\\mathrm{CD}}$)의 외견상 차이가, "
            "보각 공식 $\\cos(\\pi - \\mathrm{C}) = -\\cos\\mathrm{C}$에 의해 음수가 양수로 상쇄되며 동일한 법칙 $a = c\\cos\\mathrm{B} + b\\cos\\mathrm{C}$로 수렴합니다.<br>"
            "• <b>[수학적 의미]</b> 단순 암기가 아닌, 각이 회전함에 따라 삼각함수가 기하학적 부호를 스스로 조율하는 연속성의 아름다움을 하단 PDF와 앱렛에서 확인해 보세요."
        )
    elif any(k in t for k in ['미분계수', '접선', '도함수', '미분가능']):
        return (
            "💡 <b>민은기 선생님의 프레임별 시각적 증명 분석 (PDF & GeoGebra 탐구)</b><br>"
            "선생님의 PDF 자료는 페이지를 넘길 때마다 <b>미분계수가 탄생하는 극한의 전 과정이 생생하게 드러납니다.</b><br>"
            "• <b>[초기 상태]</b> 곡선 $y=f(x)$ 위의 고정점 $\\mathrm{P}(a, f(a))$와 멀리 떨어진 동점 $\\mathrm{Q}(x, f(x))$를 잇는 초록색 할선(Secant)의 평균변화율 $\\frac{f(x)-f(a)}{x-a}$을 그립니다.<br>"
            "• <b>[프레임의 연속 이동]</b> $x \\to a$로 접근함에 따라, 곡선을 타고 미끄러지는 동점 $\\mathrm{Q}$와 함께 초록색 할선이 연속적으로 회전합니다.<br>"
            "• <b>[극한의 합일]</b> 마지막 순간, 초록색 할선이 빨간색 접선(Tangent)과 일치하며 순간변화율 $m = \\lim_{x\\to a}\\frac{f(x)-f(a)}{x-a}$에 도달합니다.<br>"
            "• <b>[수학적 의미]</b> 미분은 형식적인 수식 연산이 아니라, 두 점 사이의 할선이 한 점에서의 접선으로 녹아드는 기하학적 수렴 과정임을 하단 자료로 확인해 보세요."
        )
    elif any(k in t for k in ['삼차함수', '사차함수', '극값', '극대', '극소', '변곡점']):
        return (
            "💡 <b>민은기 선생님의 프레임별 시각적 증명 분석 (PDF & GeoGebra 탐구)</b><br>"
            "선생님의 PDF 자료는 삼차·사차함수 그래프의 <b>숨겨진 대칭성과 황금 비율 관계</b>를 단계별로 명쾌하게 드러냅니다.<br>"
            "• <b>[도함수의 뿌리]</b> 도함수 $f'(x)=0$의 두 실근에서 원래 함수 $f(x)$의 극대와 극소가 형성되는 역학적 관계를 추적합니다.<br>"
            "• <b>[변곡점과 대칭]</b> 극대점과 극소점의 정중앙에 위치한 변곡점 $\\left(-\\frac{b}{3a}, f\\left(-\\frac{b}{3a}\\right)\\right)$을 중심으로 점대칭을 이루는 프레임별 도형 관찰<br>"
            "• <b>[비율의 기하학]</b> 극값을 지나는 접선과 곡선이 다시 만나는 점 사이의 $1 : 2$ 및 $1 : \\sqrt{3}$ 비율 관계가 왜 필연적으로 성립하는지 하단 자료의 시각적 분할로 확인해 보세요."
        )
    elif any(k in t for k in ['삼각함수', '사인', '코사인', '탄젠트', '주기']):
        return (
            "💡 <b>민은기 선생님의 프레임별 시각적 증명 분석 (PDF & GeoGebra 탐구)</b><br>"
            "선생님의 PDF 자료는 원운동이 파동 곡선으로 풀려나가는 <b>기하학적 전개 과정</b>을 한 프레임씩 보여줍니다.<br>"
            "• <b>[단위원의 동점]</b> 반지름 1인 원 위를 반시계 방향으로 회전하는 동점 $\\mathrm{P}$의 회전각 $\\theta$와 수직 투영 $y=\\sin\\theta$, 수평 투영 $x=\\cos\\theta$ 설정<br>"
            "• <b>[파동의 실시간 언래핑]</b> $\\theta$가 증가함에 따라 각 좌표의 높낮이를 오른쪽 직교좌표계로 수평 이동시켜 사인·코사인 곡선의 마루와 골이 직조되는 과정<br>"
            "• <b>[주기의 필연성]</b> 한 바퀴($2\\pi$) 회전하면 원점으로 귀환하는 원의 닫힌 궤적이 파동 함수의 무한 반복 주기성으로 승화되는 원리를 하단 자료에서 체득해 보세요."
        )
    elif any(k in t for k in ['적분', '정적분', '넓이', '구분구적법']):
        return (
            "💡 <b>민은기 선생님의 프레임별 시각적 증명 분석 (PDF & GeoGebra 탐구)</b><br>"
            "선생님의 PDF 자료는 곡선 아래의 불규칙한 넓이가 <b>직사각형들의 무한 분할로 채워지는 과정</b>을 단계별로 보여줍니다.<br>"
            "• <b>[균등 분할]</b> 구간 $[a, b]$를 $n$개의 미세 구간으로 나누고, 각 구간에서 세운 직사각형의 넓이 합(구분구적법)을 구성합니다.<br>"
            "• <b>[오차의 소멸]</b> $n=2, 4, 8, 16, \\dots$으로 분할 수를 늘릴 때마다 곡선과 직사각형 사이의 삐져나온 톱니형 오차가 눈앞에서 사라지는 시각적 장관 관찰<br>"
            "• <b>[미적분학의 기본정리]</b> 무한히 쪼갠 직사각형의 극한합이 부정적분의 함숫값 차이 $F(b)-F(a)$와 정확히 일치하는 기적적인 연결을 하단 자료의 프레임 넘김으로 확인해 보세요."
        )
    elif any(k in t for k in ['수열', '등차', '등비', '급수', '시그마']):
        return (
            "💡 <b>민은기 선생님의 프레임별 시각적 증명 분석 (PDF & GeoGebra 탐구)</b><br>"
            "선생님의 PDF 자료는 수열의 추상적 항들이 <b>좌표평면의 점과 도형의 면적으로 실체화되는 과정</b>을 한 장씩 보여줍니다.<br>"
            "• <b>[수열의 점진적 접근]</b> 항 번호 $n$이 커짐에 따라 수직선과 좌표평면에서 수열 $a_n$의 값들이 목표점(극한값)을 향해 촘촘히 포위해 들어가는 궤적 관찰<br>"
            "• <b>[무한급수의 공간 채우기]</b> 무한등비급수 $\\sum \\left(\\frac{1}{2}\\right)^n$이 정사각형 면적의 반을 채우고, 남은 반의 반을 채워나가며 결국 완전한 1의 넓이를 채워내는 프랙탈 기하학<br>"
            "• <b>[수학적 의미]</b> '무한히 더한다'는 개념이 공허한 상상이 아니라, 공간의 완전한 채움이라는 기하학적 실체임을 하단 자료에서 확인해 보세요."
        )
    elif any(k in t for k in ['거듭제곱근', '지수법칙', '로그']):
        return (
            "💡 <b>민은기 선생님의 프레임별 시각적 증명 분석 (PDF & GeoGebra 탐구)</b><br>"
            "선생님의 PDF 자료는 지수가 자연수에서 정수, 유리수, 실수로 <b>수체계가 확장될 때 규칙이 어떻게 보존되는지</b>를 단계별로 증명합니다.<br>"
            "• <b>[곱셈의 누적]</b> $a^m \\times a^n = a^{m+n}$의 자연수 지수법칙이 $a^0 = 1$, $a^{-n} = \\frac{1}{a^n}$의 역수 구조로 빈틈없이 확장되는 논리적 필연성<br>"
            "• <b>[거듭제곱근의 기하학]</b> $x^n = a$를 만족하는 실근의 개수가 지수 $n$의 홀·짝성과 밑 $a$의 부호에 따라 그래프 교점(1개, 2개, 0개)으로 갈라지는 시각적 대수 구조<br>"
            "• <b>[수학적 의미]</b> 규칙을 깨뜨리지 않고 지평을 넓혀가는 대수학적 확장의 위대함을 하단 자료의 단계별 증명 문서에서 확인해 보세요."
        )
    elif any(k in t for k in ['원의 방정식', '원과 직선', '원의 접선']):
        return (
            "💡 <b>민은기 선생님의 프레임별 시각적 증명 분석 (PDF & GeoGebra 탐구)</b><br>"
            "선생님의 PDF 자료는 원의 완벽한 대칭성과 <b>직선 사이의 위치 관계</b>를 기하학적 보조선으로 증명합니다.<br>"
            "• <b>[거리의 정의]</b> 중심 $(a, b)$에서 일정한 거리 $r$만큼 떨어진 점들의 자취로부터 피타고라스 정리를 통해 원의 방정식 $(x-a)^2 + (y-b)^2 = r^2$ 유도<br>"
            "• <b>[접선과 직각]</b> 원의 중심에서 접점에 내린 반지름은 접선과 언제나 수직($90^\\circ$)을 이룬다는 유클리드 기하의 대원칙 확인<br>"
            "• <b>[판별식과 점과 직선 거리]</b> 대수적 판별식 $D=0$과 기하학적 점과 직선 사이 거리 $d=r$가 동일한 접선의 방정식으로 귀결되는 두 수학적 세계의 일치를 하단 자료에서 확인해 보세요."
        )
    elif any(k in t for k in ['포물선', '타원', '쌍곡선', '원뿔곡선', '단델린']):
        return (
            "💡 <b>민은기 선생님의 프레임별 시각적 증명 분석 (PDF & GeoGebra 탐구)</b><br>"
            "선생님의 PDF 자료는 <b>원뿔을 자르는 3D 입체 공간</b>과 <b>평면 2D 곡선의 초점</b>이 어떻게 만나는지를 단계별로 증명합니다.<br>"
            "• <b>[단델린 구의 내접]</b> 원뿔 내부에서 절단 평면의 위아래에 꼭 맞게 내접하는 두 구(단델린 구)의 접점이 바로 두 초점 $\\mathrm{F}_1, \\mathrm{F}_2$가 되는 기적적인 공간 기하<br>"
            "• <b>[모선의 길이 보존]</b> 원뿔 꼭짓점에서 두 내접구의 접촉 원까지의 모선 길이가 항상 일정하기 때문에, 절단선 위의 임의의 점 $\\mathrm{P}$에 대해 $\\overline{\\mathrm{PF}_1} + \\overline{\\mathrm{PF}_2} = 2a$가 성립<br>"
            "• <b>[수학적 의미]</b> 복잡한 2차 대수방정식이 사실은 3차원 원뿔과 구의 가장 단순한 접촉 기하학에서 태어났음을 하단 3D 모델과 PDF로 체험해 보세요."
        )
    elif any(k in t for k in ['외심', '내심', '무게중심', '피타고라스']):
        return (
            "💡 <b>민은기 선생님의 프레임별 시각적 증명 분석 (PDF & GeoGebra 탐구)</b><br>"
            "선생님의 PDF 자료는 삼각형의 오심(외심, 내심, 무게중심, 수심, 방심)이 <b>세 선분의 만남으로 탄생하는 작도의 과정</b>을 빠짐없이 보여줍니다.<br>"
            "• <b>[작도의 논리]</b> 세 변의 수직이등분선이 왜 반드시 한 점(외심)에서 만날 수밖에 없는지, 각의 이등분선(내심)과 중선(무게중심)의 필연적 수렴 추적<br>"
            "• <b>[면적과 길이의 조화]</b> 무게중심이 세 중선을 $2:1$로 내분하고 삼각형의 넓이를 6개의 동일한 면적으로 분할하는 기하학적 균형미<br>"
            "• <b>[수학적 의미]</b> 눈금 없는 자와 컴퍼스만으로 증명해낸 그리스 기하학의 정수를 하단 인터랙티브 작도기에서 직접 확인해 보세요."
        )
    elif any(k in t for k in ['확률', '순열', '조합', '독립', '정규분포']):
        return (
            "💡 <b>민은기 선생님의 프레임별 시각적 증명 분석 (PDF & GeoGebra 탐구)</b><br>"
            "선생님의 PDF 자료는 독립시행의 무수한 우연이 <b>필연적인 정규분포의 종 모양 곡선으로 수렴하는 과정</b>을 시각화합니다.<br>"
            "• <b>[이항계수의 삼각형]</b> 파스칼 삼각형의 조합 수열이 이항분포 $\\mathrm{B}(n, p)$의 이산 확률기둥들로 쌓여가는 단계별 구축 과정<br>"
            "• <b>[중심극한정리의 출현]</b> 시행 횟수 $n$이 증가함에 따라 거친 계단 모양의 히스토그램이 매끄러운 가우스 정규분포 곡선 $N(\\mu, \\sigma^2)$으로 완벽하게 수렴<br>"
            "• <b>[수학적 의미]</b> 개별 사건은 불확실하지만, 전체의 통계적 집합은 수학의 가장 우아한 대칭 곡선을 따른다는 경이로움을 하단 자료에서 체득해 보세요."
        )
    else:
        return (
            "💡 <b>민은기 선생님의 프레임별 시각적 증명 분석 (PDF & GeoGebra 탐구)</b><br>"
            "선생님의 PDF 자료는 단순 결과가 아닌 <b>처음부터 끝까지 생각의 모든 과정이 투명하게 드러나는 단계별 시각적 증명</b>입니다.<br>"
            "하단의 <b>민은기 선생님 수학자료실(min7014)</b> PDF 문서를 키보드 방향키나 마우스 휠로 넘겨가며, 각 페이지마다 변하는 요소와 보존되는 불변량의 수학적 의미를 깊이 있게 음미해 보세요."
        )

def _append_visual_links(tip_html, matched_items):
    """시각적 팁 박스 내부에 직접 조작 가능한 GeoGebra 및 PDF/영상 링크 바 결합"""
    if not matched_items:
        return tip_html
    
    links_html = '<div class="min-visual-links" style="margin-top:14px;padding-top:12px;border-top:1px dashed rgba(124,196,255,.3);display:flex;flex-direction:column;gap:10px;">'
    links_html += '<div style="font-weight:700;color:#93c5fd;font-size:.85rem;display:flex;align-items:center;gap:6px"><span>🔗 위 시각적 증명과 직결된 민은기 선생님 핵심 자료:</span></div>'
    for it in matched_items[:2]:
        t_name = it.get('title', '관련 자료')
        sub = it.get('sub', '')
        u = it.get('url', '')
        pdf = it.get('pdf', '')
        ggb = it.get('geogebra', '')
        algeo = it.get('algeomath', '')
        yt = it.get('youtube', '')
        
        links_html += '<div class="min-tip-item" style="background:rgba(15,23,42,.55);border:1px solid rgba(56,189,248,.35);border-radius:10px;padding:10px 14px;display:flex;flex-direction:column;gap:8px">'
        links_html += '<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:6px">'
        sub_text = f' <span style="font-size:.76rem;color:#94a3b8;font-weight:400">({sub})</span>' if sub else ''
        links_html += f'<a href="{u}" target="_blank" rel="noopener" style="font-weight:700;color:#38bdf8;text-decoration:none;font-size:.88rem;display:inline-flex;align-items:center;gap:6px"><span style="font-size:1rem">📌</span> {t_name}{sub_text}</a>'
        links_html += '<span style="font-size:.72rem;background:rgba(56,189,248,.18);color:#7dd3fc;padding:2px 8px;border-radius:6px;border:1px solid rgba(56,189,248,.35)">시각적 탐구</span></div>'
        
        actions = '<div class="min-item-actions" style="display:flex;gap:6px;flex-wrap:wrap;align-items:center">'
        if ggb:
            actions += f'<button type="button" class="min-btn min-btn-ggb" onclick="toggleMinGgb(this, \'{ggb}\')" title="페이지 내에서 GeoGebra 직접 조작">📐 GeoGebra 조작 ▾</button>'
            actions += f'<a href="{ggb}" target="_blank" rel="noopener" class="min-btn min-btn-ggb" style="opacity:.9" title="GeoGebra Tube 새 창 열기">Tube ↗</a>'
        if algeo:
            actions += f'<a href="{algeo}" target="_blank" rel="noopener" class="min-btn min-btn-algeo" title="AlgeoMath 공학도구 열기">🔢 AlgeoMath</a>'
        if pdf:
            actions += f'<a href="{pdf}#toolbar=0&amp;view=Fit&amp;scrollbar=0" target="_blank" rel="noopener" class="min-btn min-btn-pdf" title="선생님의 단계별 플립북 시각적 증명 PDF">📄 단계별 증명 PDF</a>'
        if yt:
            actions += f'<a href="{yt}" target="_blank" rel="noopener" class="min-btn min-btn-yt" title="선생님의 동적 기하 해설 영상">🎥 해설 강의</a>'
        if u:
            actions += f'<a href="{u}" target="_blank" rel="noopener" class="min-btn min-btn-detail">웹 상세 탐구 ➔</a>'
        actions += '</div>'
        links_html += actions
        if ggb:
            links_html += '<div class="min-ggb-frame-wrap"></div>'
        links_html += '</div>'
        
    links_html += '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;padding-top:4px">'
    links_html += '<a href="#min7014-addon" style="color:#7cc4ff;font-size:.82rem;font-weight:700;text-decoration:none;display:inline-flex;align-items:center;gap:4px"><span>👇</span> 하단 연계 심층 탐구 자료실 전체 보기 ➔</a>'
    links_html += '<a href="https://min7014.github.io/" target="_blank" rel="noopener" style="color:#a78bfa;font-size:.82rem;font-weight:700;text-decoration:none;display:inline-flex;align-items:center;gap:4px"><span>🌐</span> 민은기 선생님의 수학자료실 메인 (3,400+ 주제) ↗</a>'
    links_html += '</div></div>'
    return tip_html + "\n" + links_html

def get_visual_tip(problem_title, matched_items=None):
    """문제 주제에 맞는 민은기 선생님의 '프레임별 시각적 증명' 심층 분석 디딤돌 팁 (관련 자료 바로가기 링크 포함)"""
    if not matched_items:
        matched_items = match_materials(problem_title, limit=4)
    tip_text = _get_visual_tip_text(problem_title)
    return _append_visual_links(tip_text, matched_items)

def generate_addon_card_html(materials, problem_title=""):
    """퀴즈 화면에 삽입되는 min7014 추가 자료 카드 HTML 생성"""
    if not materials:
        materials = match_materials(problem_title, limit=4)

    items_html = ""
    for it in materials:
        raw_title = it.get("title", "")
        # 영문 부제가 괄호/대괄호로 붙은 경우 분리
        m = re.match(r'^(.*?)\s*[\(\[]([A-Za-z][^가-힣]*?)[\)\]]\s*$', raw_title)
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

        pdf = it.get("pdf", "")
        yt = it.get("youtube", "")
        ggb = it.get("geogebra", "")
        algeo = it.get("algeomath", "")
        
        actions = []
        if ggb:
            actions.append(f'<button type="button" class="min-btn min-btn-ggb" onclick="toggleMinGgb(this, \'{html.escape(ggb)}\')" title="페이지 내에서 GeoGebra 직접 조작">📐 GeoGebra 조작 ▾</button>')
            actions.append(f'<a href="{html.escape(ggb)}" target="_blank" rel="noopener" class="min-btn min-btn-ggb" style="opacity:.85" title="GeoGebra Tube 새 창 열기">Tube ↗</a>')
        if algeo:
            actions.append(f'<a href="{html.escape(algeo)}" target="_blank" rel="noopener" class="min-btn min-btn-algeo" title="AlgeoMath 공학도구 열기">🔢 AlgeoMath</a>')
        if pdf:
            actions.append(f'<a href="{html.escape(pdf)}" target="_blank" rel="noopener" class="min-btn min-btn-pdf" title="선생님의 단계별 플립북 시각적 증명 PDF">📄 단계별 증명 PDF</a>')
        if yt:
            actions.append(f'<a href="{html.escape(yt)}" target="_blank" rel="noopener" class="min-btn min-btn-yt" title="선생님의 동적 기하 해설 영상">🎥 해설 강의</a>')
            
        actions.append(f'<a href="{url}" target="_blank" rel="noopener" class="min-btn min-btn-detail">웹 상세 탐구 ➔</a>')
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
<!-- 📚 min7014 수학자료실 공식 연계 심층 탐구 자료 카드 -->
<div class="min7014-addon-card">
  <div class="min-header">
    <div class="min-header-title">
      <img src="../assets/favicon.png" alt="min7014" class="min-logo">
      <span>📚 min7014 수학자료실 공식 연계 심층 탐구</span>
    </div>
    <span class="min-tag">GeoGebra · AlgeoMath · 단계별 증명 PDF</span>
  </div>
  <p class="min-lead">이 문제와 관련된 수학적 원리를 <b>민은기 선생님의 수학자료실(min7014)</b>의 시각적 동적 기하 조작 및 원리 증명 자료와 함께 더 깊이 탐구해보세요.</p>
  
  <div class="min-guide-banner" style="background:rgba(124,196,255,.08);border:1px solid rgba(124,196,255,.25);border-radius:10px;padding:12px 16px;margin-bottom:16px;font-size:.85rem;line-height:1.6;color:#c7d2fe">
    🎬 <b>선생님의 자료를 깊이 있게 감상하는 법</b>: 민은기 선생님의 PDF는 책장을 넘기듯 페이지를 넘겨갈 때마다 <b>도형의 점이 이동하고 보조선이 더해지며 수식이 스스로 완성되는 '단계별 플립북 애니메이션 증명'</b>입니다. 상단 미리보기나 새 창에서 키보드 방향키나 마우스 휠로 페이지를 넘기며, <b>각 프레임마다 변하는 요소와 보존되는 원리의 의미</b>를 곱씹어 보세요.
  </div>

  <div class="min-list">
    {items_html}
  </div>

  <div class="min-footer">
    <a href="https://min7014.github.io/" target="_blank" rel="noopener" class="min-footer-link">
      🌐 민은기 선생님의 수학자료실 메인 바로가기 (3,400+ GeoGebra & 증명 PDF) ➔
    </a>
  </div>
</div>

<script>
if (!window.toggleMinGgb) {{
  window.toggleMinGgb = function(btn, ggbUrl) {{
    var item = btn.closest ? btn.closest('.min-item') : btn.parentElement.parentElement;
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
