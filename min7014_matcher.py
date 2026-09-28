"""min7014.github.io 수학자료실 연계 정밀 분석, 추천 및 인터랙티브 HTML 생성 모듈"""
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

def get_visual_tip(problem_title, matched_items=None):
    """문제 주제에 맞는 민은기 선생님의 시각적 원리 디딤돌 팁 생성"""
    if not matched_items:
        matched_items = match_materials(problem_title, limit=4)
    
    t = problem_title.lower()
    
    if any(k in t for k in ['사인법칙', '코사인법칙', '사인 법칙', '코사인 법칙']):
        return (
            "💡 <b>민은기 선생님의 시각적 기하 팁</b>: 각도가 예각에서 직각($90^\\circ$), 둔각으로 변함에 따라 "
            "피타고라스 정리가 어떻게 코사인법칙($c^2=a^2+b^2-2ab\\cos C$)으로 자연스럽게 일반화되는지, "
            "하단의 <b>min7014 동적 기하 앱렛</b>에서 삼각형 꼭짓점을 직접 드래그하며 시각적으로 체험해 보세요."
        )
    elif any(k in t for k in ['미분계수', '접선', '도함수', '미분가능']):
        return (
            "💡 <b>민은기 선생님의 시각적 미적분 팁</b>: 곡선 위의 한 고정점과 움직이는 점을 잇는 할선이 "
            "두 점 사이의 거리가 0에 가까워질 때 접선에 수렴하는 '미분계수의 기하학적 극한 과정'을 "
            "하단의 <b>min7014 GeoGebra 모델</b>을 통해 직접 관찰해 보세요."
        )
    elif any(k in t for k in ['삼차함수', '사차함수', '극값', '극대', '극소', '변곡점']):
        return (
            "💡 <b>민은기 선생님의 시각적 다항함수 팁</b>: 삼차함수 그래프에서 극대점, 변곡점, 극소점, 접선이 이루는 "
            "황금 비율 관계($1:\\sqrt{3}$ 및 $1:2$ 비율)와 대칭성을 하단의 <b>min7014 시각적 기하 자료</b>를 통해 "
            "직관적으로 체득할 수 있습니다."
        )
    elif any(k in t for k in ['삼각함수', '사인', '코사인', '탄젠트', '주기']):
        return (
            "💡 <b>민은기 선생님의 시각적 대수 팁</b>: 단위원 위를 회전하는 동점의 회전각과 좌표 $(x, y)=(\\cos\\theta, \\sin\\theta)$가 "
            "파동 형태의 주기함수 곡선으로 전개되는 시각적 원리를 하단의 <b>min7014 동적 앱렛</b>에서 확인해 보세요."
        )
    elif any(k in t for k in ['적분', '정적분', '넓이', '구분구적법']):
        return (
            "💡 <b>민은기 선생님의 시각적 해석학 팁</b>: 곡선과 축 사이의 복잡한 영역을 무수히 많은 직사각형의 합으로 근사하는 "
            "구분구적법과 정적분의 미적분학 기본정리를 하단의 <b>min7014 인터랙티브 모델</b>로 조작해 보세요."
        )
    elif any(k in t for k in ['수열', '등차', '등비', '급수', '시그마']):
        return (
            "💡 <b>민은기 선생님의 시각적 수열 팁</b>: 수열의 각 항이 수직선과 좌표평면에서 찍히는 규칙과, "
            "무한등비급수가 정사각형 면적을 채워나가는 프랙탈 기하학적 원리를 하단의 <b>min7014 자료실</b>에서 시각적으로 확인해 보세요."
        )
    elif any(k in t for k in ['거듭제곱근', '지수법칙', '로그']):
        return (
            "💡 <b>민은기 선생님의 시각적 대수 팁</b>: 지수가 정수에서 유리수, 실수로 확장됨에 따라 나타나는 "
            "지수함수의 지수적 폭발과 거듭제곱근의 기하학적 성질을 하단의 <b>min7014 개념 정리 자료</b>를 통해 깊이 있게 탐구해 보세요."
        )
    elif any(k in t for k in ['원의 방정식', '원과 직선', '원의 접선']):
        return (
            "💡 <b>민은기 선생님의 시각적 해석기하 팁</b>: 원의 중심과 직선 사이의 거리 공식 $d$와 반지름 $r$의 대소 관계($d < r, d=r, d > r$)에 따른 "
            "원의 위치 관계와 접선의 성질을 하단의 <b>min7014 인터랙티브 도구</b>로 직관적으로 확인해 보세요."
        )
    elif any(k in t for k in ['포물선', '타원', '쌍곡선', '원뿔곡선', '단델린']):
        return (
            "💡 <b>민은기 선생님의 시각적 공간기하 팁</b>: 원뿔을 자르는 단면과 내접하는 구(단델린 구)의 접점이 "
            "어떻게 이차곡선의 두 초점이 되는지 보여주는 3D 동적 입체 모델을 하단의 <b>min7014 GeoGebra 3D</b>로 직접 회전시켜 보세요."
        )
    elif any(k in t for k in ['외심', '내심', '무게중심', '피타고라스']):
        return (
            "💡 <b>민은기 선생님의 시각적 평면기하 팁</b>: 삼각형의 오심(외심, 내심, 무게중심, 수심, 방심)의 기하학적 작도 원리와 "
            "피타고라스 정리의 다양한 시각적 증명(유클리드, 바스카라)을 하단의 <b>min7014 동적 작도기</b>로 탐험해 보세요."
        )
    elif any(k in t for k in ['확률', '순열', '조합', '독립', '정규분포']):
        return (
            "💡 <b>민은기 선생님의 시각적 확률통계 팁</b>: 독립시행의 반복과 이항분포가 표본의 크기가 커짐에 따라 "
            "종 모양의 매끄러운 정규분포 곡선으로 수렴하는 중심극한정리의 원리를 하단의 <b>min7014 시각화 모델</b>로 탐색해 보세요."
        )
    else:
        return (
            "💡 <b>민은기 선생님의 시각적 수학 팁</b>: 복잡한 수식과 기호 뒤에 숨겨진 직관적인 기하학적 원리와 시각적 모델을 "
            "하단의 <b>민은기 선생님 수학자료실(min7014)</b>의 GeoGebra 조작 및 개념 증명 자료를 통해 깊이 있게 탐구해 보세요."
        )

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
            actions.append(f'<a href="{html.escape(pdf)}" target="_blank" rel="noopener" class="min-btn min-btn-pdf" title="민은기 선생님의 시각적 증명 및 개념 정리 PDF">📄 PDF 증명</a>')
        if yt:
            actions.append(f'<a href="{html.escape(yt)}" target="_blank" rel="noopener" class="min-btn min-btn-yt" title="민은기 선생님의 유튜브 개념 해설 강의">🎥 해설 강의</a>')
            
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
    <span class="min-tag">GeoGebra · AlgeoMath · 증명 PDF</span>
  </div>
  <p class="min-lead">이 문제와 관련된 수학적 원리를 <b>민은기 선생님의 수학자료실(min7014)</b>의 시각적 동적 기하 조작 및 원리 증명 자료와 함께 더 깊이 탐구해보세요.</p>
  
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
