"""min7014.github.io 수학자료실 연계 추가 학습 자료 추천 및 HTML 생성 모듈"""
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

KEYWORD_WEIGHTS = {
    '삼차함수': 12, '사차함수': 12, '이차함수': 10, '일차함수': 8,
    '미분가능': 12, '미분': 8, '도함수': 8, '접선': 9, '극값': 9, '변곡점': 10,
    '적분': 8, '정적분': 9, '연속': 8, '극한': 7,
    '단델린': 15, '원뿔곡선': 14, '이차곡선': 12, '타원': 11, '쌍곡선': 11, '포물선': 11,
    '삼각함수': 10, '사인': 8, '코사인': 8, '탄젠트': 8, '삼각비': 8,
    '수열': 9, '등차수열': 10, '등비수열': 10, '점화식': 11, '급수': 9,
    '경우의 수': 10, '순열': 10, '조합': 10, '확률': 9, '통계': 9, '정규분포': 11,
    '피타고라스': 10, '외심': 9, '내심': 9, '무게중심': 9, '작도': 8, '원': 6
}

def match_materials(text, limit=3):
    materials = get_materials()
    if not materials:
        return []

    text_lower = text.lower()
    
    # 1. 문제 텍스트에서 주요 키워드 추출
    found_keywords = []
    for kw, w in KEYWORD_WEIGHTS.items():
        if kw in text:
            found_keywords.append((kw, w))
            
    scored = []
    for item in materials:
        title = item.get("title", "")
        tags = item.get("tags", [])
        score = 0
        
        # 키워드 매칭 점수
        for kw, w in found_keywords:
            if kw in title:
                score += w * 3
            elif any(kw in tag for tag in tags):
                score += w
                
        # 일반 텍스트 내 부분 일치
        words = re.findall(r'[가-힣a-zA-Z0-9]{2,}', title)
        for w in words:
            if len(w) >= 2 and w in text:
                score += 2
                
        # 조작 가능한 GeoGebra 인터랙티브 앱렛이 있으면 가산점
        if item.get("geogebra"):
            score += 3
        if item.get("pdf"):
            score += 1
        if item.get("youtube"):
            score += 1
            
        if score > 0:
            scored.append((score, item))
            
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # 상위 N개 선택
    results = [item for _, item in scored[:limit]]
    
    # 매칭 결과가 부족할 경우 대표적 추천 자료 추가
    if len(results) < limit:
        defaults = [
            it for it in materials 
            if any(k in it['title'] for k in ['타원', '삼차함수', '미분', '접선', '원뿔곡선']) and it.get('geogebra')
        ]
        for d in defaults:
            if d not in results:
                results.append(d)
            if len(results) >= limit:
                break
                
    return results[:limit]

def generate_addon_card_html(materials, problem_title=""):
    """퀴즈 화면에 삽입되는 min7014 추가 자료 카드 HTML 생성"""
    if not materials:
        materials = match_materials(problem_title, limit=3)
        
    query = re.sub(r'[^가-힣a-zA-Z0-9\s]', ' ', problem_title).strip()
    query_first = query.split()[0] if query else "수학"

    items_html = ""
    for it in materials:
        raw_title = it.get("title", "")
        # 영문 부제가 괄호/대괄호로 붙은 경우 분리 (내부 수식/괄호 포함 지원)
        m = re.match(r'^(.*?)\s*[\(\[]([A-Za-z][^가-힣]*?)[\)\]]\s*$', raw_title)
        if m:
            ko_part = m.group(1).strip()
            en_part = m.group(2).strip()
        else:
            ko_part = raw_title
            en_part = ""
            
        url = html.escape(it.get("url", "https://min7014.github.io/"))
        pdf = it.get("pdf", "")
        yt = it.get("youtube", "")
        ggb = it.get("geogebra", "")
        
        actions = []
        if ggb:
            actions.append(f'<a href="{html.escape(ggb)}" target="_blank" rel="noopener" class="min-btn min-btn-ggb" title="GeoGebra 인터랙티브 탐구">📐 GeoGebra 조작</a>')
        if pdf:
            actions.append(f'<a href="{html.escape(pdf)}" target="_blank" rel="noopener" class="min-btn min-btn-pdf" title="원리 증명 및 정리 PDF">📄 PDF 정리</a>')
        if yt:
            actions.append(f'<a href="{html.escape(yt)}" target="_blank" rel="noopener" class="min-btn min-btn-yt" title="시각적 애니메이션 해설 영상">▶️ 영상 해설</a>')
            
        actions_str = " ".join(actions)
        sub_html = f'<span class="min-item-sub">{html.escape(en_part)}</span>' if en_part else ""
        
        items_html += f"""
        <div class="min-item">
          <div class="min-item-main">
            <a href="{url}" target="_blank" rel="noopener" class="min-item-title">
              <span class="min-bullet">📌</span> {html.escape(ko_part)}
              {sub_html}
            </a>
          </div>
          <div class="min-item-actions">
            {actions_str}
            <a href="{url}" target="_blank" rel="noopener" class="min-btn min-btn-detail">상세 탐구 ➔</a>
          </div>
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
    <span class="min-tag">GeoGebra & 개념 증명</span>
  </div>
  <p class="min-lead">이 문제와 관련된 수학적 원리를 <b>민은기 선생님의 수학자료실(min7014)</b>의 시각적 GeoGebra 조작 및 정리 자료와 함께 더 깊이 탐구해보세요.</p>
  
  <div class="min-list">
    {items_html}
  </div>

  <div class="min-footer">
    <a href="https://min7014.github.io/" target="_blank" rel="noopener" class="min-footer-link">
      🌐 민은기 선생님의 수학자료실 메인 바로가기 (3,000+ GeoGebra & PDF) ➔
    </a>
  </div>
</div>
"""
