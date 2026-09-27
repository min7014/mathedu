"""
build_offline_quizzes.py — 모든 수학 문제를 100% 독립 실행 가능한 오프라인 HTML 파일로 일괄 빌드
- 원본 이미지 Base64 인라인 변환 (외부 의존성 제로)
- 온라인 원본 문제 주소(https://min7014.github.io/mathedu/board/{slug}.html) 필수 배너 삽입
- 오프라인 단독 퀴즈 상호작용(채점, 정답, 해설, 점수바) 완벽 보장
- offline/ 디렉토리에 {slug}.html 및 오프라인 전체 목차(index.html) 자동 생성
"""
import os
import sys
import re
import base64
import json
import glob

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOARD_DIR = os.path.join(BASE_DIR, 'board')
OFFLINE_DIR = os.path.join(BASE_DIR, 'offline')
ONLINE_BASE_URL = 'https://min7014.github.io/mathedu'

os.makedirs(OFFLINE_DIR, exist_ok=True)

def image_to_base64(img_path):
    if not os.path.isfile(img_path):
        return None
    ext = os.path.splitext(img_path)[1].lower().replace('.', '')
    if ext == 'jpg': ext = 'jpeg'
    mime = f'image/{ext}' if ext in ['png', 'jpeg', 'gif', 'svg', 'webp'] else 'image/png'
    with open(img_path, 'rb') as f:
        encoded = base64.b64encode(f.read()).decode('utf-8')
    return f'data:{mime};base64,{encoded}'

def extract_title(html_content, slug):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html_content, re.DOTALL)
    if m:
        t = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        t = re.sub(r'^[📘📙📕📝]\s*', '', t)
        return t
    m_title = re.search(r'<title>(.*?)</title>', html_content, re.DOTALL)
    if m_title:
        return m_title.group(1).split('·')[0].split('—')[0].strip()
    return slug

def process_file(html_path):
    filename = os.path.basename(html_path)
    slug = os.path.splitext(filename)[0]

    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    title = extract_title(content, slug)
    original_online_url = f"{ONLINE_BASE_URL}/board/{slug}.html"

    # 1. 이미지 Base64 인라인화
    def replace_img(match):
        img_tag = match.group(0)
        src_match = re.search(r'src=["\']([^"\']+)["\']', img_tag)
        if not src_match:
            return img_tag
        src = src_match.group(1)
        if src.startswith('data:'):
            return img_tag

        # 로컬 경로 찾기
        candidate_paths = [
            os.path.join(BOARD_DIR, src),
            os.path.join(BASE_DIR, src),
            os.path.join(BOARD_DIR, os.path.basename(src)),
            os.path.join(BASE_DIR, 'assets', os.path.basename(src))
        ]
        for p in candidate_paths:
            if os.path.isfile(p):
                b64 = image_to_base64(p)
                if b64:
                    return re.sub(r'src=["\'][^"\']+["\']', f'src="{b64}"', img_tag)
        return img_tag

    content = re.sub(r'<img[^>]+>', replace_img, content)

    # 1-1. MathJax 스크립트: 오프라인 로컬 우선 + CDN 폴백
    content = re.sub(
        r'<script id="mj"[^>]*></script>',
        r'<script id="mj" async src="mathjax/tex-mml-chtml.js" onerror="this.onerror=null;this.src=\'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js\'"></script>',
        content
    )

    # 1-2. 네비게이션 바 링크를 오프라인 환경에 맞게 보정
    content = content.replace('href="/board/6wol_mopyung.html"', 'href="index.html"')
    content = content.replace('href="/"', 'href="https://min7014.github.io/mathedu/" target="_blank" rel="noopener"')

    # 1-3. 파비콘 Base64 인라인화
    fav_path = os.path.join(BASE_DIR, 'assets', 'favicon.png')
    fav_b64 = image_to_base64(fav_path)
    if fav_b64:
        content = re.sub(r'href=["\'][^"\']*favicon\.png["\']', f'href="{fav_b64}"', content)

    # 1-4. 온라인 전용 교실 스크립트 제거 (오프라인 환경 404 방지)
    content = re.sub(r'<script[^>]*src=["\'][^"\']*mathedu-room\.js["\'][^>]*></script>', '', content)

    # 2. 오프라인 메타 태그 삽입
    meta_tags = f"""
<link rel="canonical" href="{original_online_url}">
<meta name="original-problem-url" content="{original_online_url}">
<meta name="mathedu-offline-version" content="true">
"""
    if '</head>' in content:
        content = content.replace('</head>', f'{meta_tags}\n</head>')

    # 3. 오프라인 단독 실행 배너 & 원본 주소 링크 카드 생성
    offline_banner = f"""
<!-- 🌐 오프라인 단독 학습 배너 & 온라인 원본 문제 링크 안내 -->
<div class="mathedu-offline-banner" style="background:linear-gradient(135deg,rgba(56,189,248,.18),rgba(129,140,248,.18));border:2px solid #38bdf8;border-radius:16px;padding:18px 22px;margin:16px 0 24px;box-shadow:0 8px 30px rgba(0,0,0,.45);color:#fff;font-family:system-ui,sans-serif">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:10px">
    <div style="display:inline-flex;align-items:center;gap:6px;background:rgba(56,189,248,.25);border:1px solid #38bdf8;color:#38bdf8;border-radius:20px;padding:4px 14px;font-size:0.82rem;font-weight:800">
      📦 오프라인 단독 실행 파일 (인터넷 접속 없이 풀이 가능)
    </div>
    <span style="font-size:0.78rem;color:#94a3b8">min7014 mathedu</span>
  </div>
  <div style="font-size:1.15rem;font-weight:800;color:#ffffff;margin-bottom:6px">{title}</div>
  <div style="font-size:0.86rem;color:#cbd5e1;line-height:1.5;margin-bottom:14px">
    이 파일은 인터넷 연결 없이 웹 브라우저에서 언제든 풀 수 있는 <b>단독 오프라인 인터랙티브 수학 퀴즈</b>입니다.<br>
    보기를 클릭하면 채점과 단계별 상세 해설이 열리며, 점수가 자동 계산됩니다.
  </div>
  <div style="background:rgba(15,23,42,.7);border:1px solid rgba(255,255,255,.14);border-radius:12px;padding:12px 16px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px">
    <div style="font-size:0.85rem;color:#e2e8f0;word-break:break-all">
      <span style="color:#7cc4ff;font-weight:700">🌐 온라인 원본 문제 주소:</span><br>
      <a href="{original_online_url}" target="_blank" rel="noopener" style="color:#38bdf8;font-weight:700;text-decoration:underline;font-family:monospace">
        {original_online_url}
      </a>
    </div>
    <div style="display:flex;gap:8px">
      <a href="{original_online_url}" target="_blank" rel="noopener" style="background:linear-gradient(90deg,#38bdf8,#818cf8);color:#0b1020;padding:8px 16px;border-radius:8px;font-size:0.82rem;font-weight:800;text-decoration:none;display:inline-flex;align-items:center;gap:4px">
        🌐 온라인 원본 열기 ➔
      </a>
      <a href="https://min7014.github.io/" target="_blank" rel="noopener" style="background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);color:#eef2ff;padding:8px 14px;border-radius:8px;font-size:0.82rem;font-weight:700;text-decoration:none">
        🏛️ min7014 자료실
      </a>
    </div>
  </div>
</div>
"""
    # wrap 다음 또는 body 다음에 배너 삽입
    if '<div class="wrap">' in content:
        content = content.replace('<div class="wrap">', f'<div class="wrap">\n{offline_banner}')
    elif '<body>' in content:
        content = content.replace('<body>', f'<body>\n{offline_banner}')

    # 4. #trackFull 시작 모달에 "오프라인 바로 시작" 버튼 보강
    offline_start_script = """
<script>
// 오프라인 실행 보장 스크립트
window._isOfflineFile = true;
window._originalUrl = '""" + original_online_url + """';
document.addEventListener("DOMContentLoaded", function() {
  var tf = document.getElementById("trackFull");
  if (tf) {
    var quickBtn = document.createElement("button");
    quickBtn.type = "button";
    quickBtn.className = "btn";
    quickBtn.style.cssText = "background:rgba(56,189,248,.2);border:1px solid #38bdf8;color:#38bdf8;font-size:.9rem;padding:8px 16px;border-radius:10px;cursor:pointer;margin-top:10px;font-weight:700;";
    quickBtn.innerHTML = "⚡ 오프라인 바로 시작하기";
    quickBtn.onclick = function() {
      window._studentName = "오프라인 학습자";
      tf.remove();
      if (window.sendProgress) sendProgress();
      if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise();
    };
    tf.appendChild(quickBtn);
  }
});
</script>
"""
    if '</body>' in content:
        content = content.replace('</body>', f'{offline_start_script}\n</body>')

    out_path = os.path.join(OFFLINE_DIR, filename)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return {
        'slug': slug,
        'title': title,
        'filename': filename,
        'original_online_url': original_online_url,
        'size': len(content)
    }

def main():
    files = sorted(glob.glob(os.path.join(BOARD_DIR, '*.html')))
    # index.html 등 메인 파일 제외
    quiz_files = [f for f in files if not os.path.basename(f).startswith('index')]

    print(f"총 {len(quiz_files)}개 퀴즈 파일을 오프라인 패키지로 변환 시작...")
    results = []
    for f in quiz_files:
        res = process_file(f)
        results.append(res)

    # 오프라인 인덱스 페이지(offline/index.html) 생성
    index_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>min7014 mathedu · 오프라인 전체 문제 보관함</title>
<style>
:root {{
  --bg: #0d1020; --card: rgba(255,255,255,.10); --line: rgba(255,255,255,.20);
  --txt: #eef2ff; --sub: #aab4d4; --accent: #7cc4ff; --accent2: #a78bfa; --good: #5eead4;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  color: var(--txt); line-height: 1.6;
  font-family: -apple-system, BlinkMacSystemFont, "Pretendard", sans-serif;
  background: linear-gradient(160deg, #0a0d1a 0%, #141833 50%, #0a0d1a 100%);
  min-height: 100vh; padding: 36px 18px 80px;
}}
.wrap {{ max-width: 900px; margin: 0 auto; }}
h1 {{
  font-size: 2rem; background: linear-gradient(90deg, var(--accent), var(--accent2));
  -webkit-background-clip: text; background-clip: text; color: transparent;
  font-weight: 800; margin-bottom: 8px;
}}
.lead {{ color: var(--sub); font-size: 1rem; margin-bottom: 24px; }}
.banner {{
  background: rgba(56,189,248,.14); border: 1px solid rgba(56,189,248,.35);
  border-radius: 14px; padding: 18px 22px; margin-bottom: 28px;
}}
.list {{ display: grid; gap: 12px; }}
.card {{
  background: var(--card); border: 1px solid var(--line); border-radius: 14px;
  padding: 16px 20px; display: flex; align-items: center; justify-content: space-between;
  gap: 16px; flex-wrap: wrap; transition: .15s;
}}
.card:hover {{ border-color: var(--accent); transform: translateY(-1px); }}
.card-title {{ font-size: 1.05rem; font-weight: 700; color: #fff; text-decoration: none; }}
.card-title:hover {{ color: var(--accent); }}
.card-meta {{ font-size: 0.8rem; color: var(--sub); margin-top: 4px; }}
.btn {{
  background: linear-gradient(90deg, var(--accent), var(--accent2)); color: #0b1020;
  padding: 8px 16px; border-radius: 10px; font-weight: 800; font-size: 0.85rem;
  text-decoration: none; display: inline-flex; align-items: center; gap: 6px;
}}
</style>
</head>
<body>
<div class="wrap">
  <h1>📦 min7014 mathedu 오프라인 전체 문제 보관함</h1>
  <p class="lead">인터넷 접속 없이 언제 어디서나 풀이할 수 있는 오프라인 독립 실행형 수학 퀴즈 모음입니다.</p>

  <div class="banner">
    <div style="font-weight:700;color:var(--good);margin-bottom:4px">💡 오프라인 단독 파일 안내</div>
    <div style="font-size:0.88rem;color:#cbd5e1">
      • 각 문제 파일은 이미지와 인터랙티브 채점 로직이 포함된 <b>단일 HTML 파일</b>입니다.<br>
      • 모든 문제에는 온라인 원본 주소(<code>https://min7014.github.io/mathedu/board/...</code>) 및 민은기 선생님 수학자료실 링크가 포함되어 있습니다.<br>
      • 총 <b>{len(results)}개</b>의 문제 파일이 준비되어 있습니다.
    </div>
  </div>

  <div class="list">
"""
    for r in results:
        index_html += f"""    <div class="card">
      <div>
        <a href="{r['filename']}" class="card-title">📘 {r['title']}</a>
        <div class="card-meta">
          <span>고유 슬러그: <code>{r['slug']}</code></span> · 
          <a href="{r['original_online_url']}" target="_blank" rel="noopener" style="color:var(--accent);text-decoration:underline">온라인 원본 링크 ➔</a>
        </div>
      </div>
      <div>
        <a href="{r['filename']}" class="btn" download>📥 다운로드</a>
        <a href="{r['filename']}" class="btn" style="background:rgba(255,255,255,.1);color:#fff;border:1px solid var(--line);margin-left:6px">풀기 ➔</a>
      </div>
    </div>
"""
    index_html += """  </div>
</div>
</body>
</html>
"""
    with open(os.path.join(OFFLINE_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)

    print(f"✅ 총 {len(results)}개 문제의 오프라인 HTML 파일 및 offline/index.html 빌드 완료!")

if __name__ == '__main__':
    main()
