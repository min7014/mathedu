"""Quiz generation homepage backend.

Routes:
- '/': upload form + board list
- '/generate': problem(+image) -> pending queue -> I build the quiz manually
- '/board/<slug>': serve quiz HTML
"""
import os, json, time, uuid, re, hashlib, sqlite3
from flask import (Flask, request, render_template_string, redirect,
                   send_from_directory, make_response)
import generator

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, 'results.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_slug TEXT NOT NULL,
        student_name TEXT NOT NULL,
        score INTEGER NOT NULL,
        total INTEGER NOT NULL,
        pct REAL NOT NULL,
        answers TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_slug TEXT NOT NULL,
        student_name TEXT NOT NULL,
        current_step INTEGER NOT NULL DEFAULT 0,
        total_steps INTEGER NOT NULL DEFAULT 0,
        correct INTEGER NOT NULL DEFAULT 0,
        pct REAL NOT NULL DEFAULT 0.0,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(quiz_slug, student_name)
    )''')
    conn.commit()
    conn.close()

DASHBOARD_2_TPL = r"""<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>mathedu · 학습 현황 대시보드</title>
<style>
body{font-family:"Apple SD Gothic Neo","Malgun Gothic",sans-serif;background:#0f1320;color:#e8ecf5;
margin:0;padding:24px} h1{color:#6ea8fe} h2{color:#6ea8fe;font-size:1.1rem;margin:24px 0 10px}
.box{background:#1a2030;border:1px solid #2e3850;border-radius:14px;padding:16px;margin:12px 0}
a{color:#6ea8fe;text-decoration:none} a:hover{text-decoration:underline}
table{width:100%;border-collapse:collapse;font-size:.88rem;margin:8px 0}
th,td{padding:8px 10px;border-bottom:1px solid #2e3850;text-align:left}
th{color:#9aa6c0;font-weight:600}
tr:hover td{background:rgba(110,168,254,.06)}
.pill{display:inline-block;padding:2px 10px;border-radius:20px;font-size:.78rem;font-weight:700}
.pill-high{background:rgba(62,220,151,.15);color:#3ddc97}
.pill-mid{background:rgba(255,209,102,.15);color:#ffd166}
.pill-low{background:rgba(255,107,107,.15);color:#ff6b6b}
.pill-live{background:rgba(110,168,254,.20);color:#6ea8fe;animation:blink 1.5s infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.5}}
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;margin:10px 0}
.stat-card{background:#1a2030;border:1px solid #2e3850;border-radius:12px;padding:14px}
.stat-card .num{font-size:1.6rem;font-weight:800;color:#6ea8fe}
.stat-card .lbl{font-size:.8rem;color:#9aa6c0;margin-top:4px}
.filter-bar{display:flex;gap:8px;margin:10px 0;flex-wrap:wrap;align-items:center}
.filter-bar select,.filter-bar input{background:#222a3d;color:#e8ecf5;border:1px solid #2e3850;border-radius:8px;padding:8px 12px;font-size:.9rem}
.btn{background:#6ea8fe;color:#0b1020;border:none;border-radius:8px;padding:8px 16px;font-weight:700;cursor:pointer}
.btn-live{display:inline-flex;align-items:center;gap:6px;background:#1a2030;color:#6ea8fe;border:1px solid #6ea8fe}
.live-dot{width:8px;height:8px;background:#3ddc97;border-radius:50%;animation:blink 1s infinite}
</style></head><body>
<h1>📊 mathedu · 학습 현황 대시보드</h1>
<p><a href="/">← 게시판으로 돌아가기</a></p>
<div class="filter-bar">
  <select id="quizFilter"><option value="">전체 퀴즈</option></select>
  <button class="btn" onclick="refreshData()">🔄 새로고침</button>
  <label style="display:flex;align-items:center;gap:6px;font-size:.85rem;color:#9aa6c0;cursor:pointer">
  <input type="checkbox" id="liveToggle" checked onchange="toggleLive()">
    <span class="live-dot" id="liveDot"></span> 실시간 갱신
  </label>
</div>
<div class="box">
<h2 style="margin-top:0">📊 현재 학습 현황</h2>
<div id="liveInfo" style="font-size:.85rem;color:#3ddc97;margin-bottom:8px"></div>
<table id="liveTable"><tr><th>학생</th><th>퀴즈</th><th>진행</th><th>정답률</th><th>업데이트</th></tr>
<tr><td colspan="5" style="color:#9aa6c0;text-align:center">불러오는 중...</td></tr></table>
</div>
<div class="box">
<h2 style="margin-top:0">📈 퀴즈별 최종 통계</h2>
<div class="stats-grid" id="statsGrid"><p style="color:#9aa6c0">불러오는 중...</p></div>
</div>
<div class="box">
<h2 style="margin-top:0">📋 최종 제출 기록</h2>
<table id="finalTable"><tr><th>#</th><th>학생</th><th>퀴즈</th><th>점수</th><th>정답률</th><th>제출 시각</th></tr>
<tr><td colspan="6" style="color:#9aa6c0;text-align:center">불러오는 중...</td></tr></table>
</div>
<script>
let liveInterval=null;
function toggleLive(){
  const cb=document.getElementById('liveToggle');
  if(cb.checked){liveInterval=setInterval(refreshData,5000);document.getElementById('liveDot').style.background='#3ddc97';}
  else{clearInterval(liveInterval);document.getElementById('liveDot').style.background='#9aa6c0';}
}
function refreshData(){
  const q=document.getElementById('quizFilter').value;
  const qp=q?('?quiz='+encodeURIComponent(q)):'';
  fetch('/api/progress'+qp).then(r=>r.json()).then(d=>{
    const items=d.items||[];
    document.getElementById('liveInfo').textContent='실시간: '+items.length+'명 학습 중';
    const rows=items.map(p=>{
      const stepTxt=p.current_step>=p.total_steps?'✅ 완료':(p.current_step+' / '+p.total_steps+' 단계');
      const pill=p.current_step>=p.total_steps?
        '<span class="pill pill-high">완료</span>':
        '<span class="pill pill-live">풀이중</span>';
      return '<tr><td>'+p.student_name+'</td><td><a href="/board/'+p.quiz_slug+'">'+p.quiz_slug+'</a></td>'+
        '<td>'+stepTxt+' '+pill+'</td>'+
        '<td>'+p.pct+'%</td><td>'+p.updated_at+'</td></tr>';
    }).join('');
    document.getElementById('liveTable').innerHTML=
      '<tr><th>학생</th><th>퀴즈</th><th>진행</th><th>정답률</th><th>업데이트</th></tr>'+
      (rows||'<tr><td colspan="5" style="color:#9aa6c0;text-align:center">아직 학습 중인 학생이 없습니다.</td></tr>');
  }).catch(()=>{});
  fetch('/api/stats'+qp).then(r=>r.json()).then(d=>{
    const stats=d.stats||[];
    const cards=stats.map(s=>{
      return '<div class="stat-card"><div class="num">'+s.avg_pct+'%</div>'+
        '<div class="lbl">평균 정답률</div>'+
        '<div style="font-size:.8rem;color:#9aa6c0;margin-top:4px">'+s.quiz_slug+' · '+s.n+'명</div>'+
        '<div style="font-size:.78rem;color:#9aa6c0">최고 '+s.best+'% / 최저 '+s.worst+'%</div></div>';
    }).join('');
    document.getElementById('statsGrid').innerHTML=cards||'<p style="color:#9aa6c0">아직 데이터가 없습니다.</p>';
  }).catch(()=>{});
  fetch('/api/results_list'+qp).then(r=>r.json()).then(d=>{
    const rows=(d.items||[]).map(r=>{
      const pill=r.pct>=80?'pill-high':(r.pct>=50?'pill-mid':'pill-low');
      return '<tr><td>'+r.id+'</td><td>'+r.student_name+'</td>'+
        '<td><a href="/board/'+r.quiz_slug+'">'+r.quiz_slug+'</a></td>'+
        '<td>'+r.score+' / '+r.total+'</td>'+
        '<td><span class="pill '+pill+'">'+r.pct+'%</span></td>'+
        '<td>'+r.created_at+'</td></tr>';
    }).join('');
    document.getElementById('finalTable').innerHTML=
      '<tr><th>#</th><th>학생</th><th>퀴즈</th><th>점수</th><th>정답률</th><th>제출 시각</th></tr>'+
      (rows||'<tr><td colspan="6" style="color:#9aa6c0;text-align:center">아직 결과가 없습니다.</td></tr>');
  }).catch(()=>{});
}
function loadQuizFilter(){
  fetch('/api/stats').then(r=>r.json()).then(d=>{
    const sel=document.getElementById('quizFilter');
    const stats=d.stats||[];
    stats.forEach(s=>{
      const opt=document.createElement('option');
      opt.value=s.quiz_slug;opt.textContent=s.quiz_slug+' ('+s.n+'명)';
      sel.appendChild(opt);
    });
  }).catch(()=>{});
}
loadQuizFilter();
refreshData();
liveInterval=setInterval(refreshData,5000);
</script>
</body></html>"""

init_db()

BOARD = os.path.join(BASE, "board")
MATHJAX_DIR = os.path.join(BASE, "mathjax")  # ★ mathjax은 board 밖 루트에 있음
os.makedirs(BOARD, exist_ok=True)
os.makedirs(MATHJAX_DIR, exist_ok=True)
META = os.path.join(BOARD, "index.json")
app = Flask(__name__)

def load_meta():
    try: return json.load(open(META, encoding="utf-8"))
    except: return []

def save_meta(m):
    json.dump(m, open(META, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

INDEX_TPL = r"""<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>mathedu · 퀴즈 생성 게시판</title>
<style>
body{font-family:"Apple SD Gothic Neo","Malgun Gothic",sans-serif;background:#0f1320;color:#e8ecf5;
margin:0;padding:24px} h1{color:#6ea8fe} .box{background:#1a2030;border:1px solid #2e3850;
border-radius:14px;padding:18px;margin:14px 0} textarea,input[type=text]{width:100%;background:#222a3d;
color:#e8ecf5;border:1px solid #2e3850;border-radius:8px;padding:10px;font-size:1rem}
button{background:#6ea8fe;color:#0b1020;border:none;border-radius:10px;padding:10px 18px;
font-weight:700;cursor:pointer;margin-top:10px} .list a{color:#ffd166;text-decoration:none;font-size:1.05rem}
.list div{padding:8px 0;border-bottom:1px solid #2e3850}
.label{font-size:.9rem;color:#9aa6c0} .err{color:#ff6b6b} .ok{color:#3ddc97}
.hint{font-size:.82rem;color:#9aa6c0;margin:4px 0 8px}
.tbtn{background:#222a3d;color:#e8ecf5;border:1px solid #2e3850;border-radius:10px;
padding:8px 14px;font-weight:700;cursor:pointer;text-decoration:none;font-size:.9rem;display:inline-flex;align-items:center}
.tbtn:hover{border-color:#6ea8fe}
#prev{max-width:200px;margin-top:8px;border-radius:10px;display:none;border:1px solid #2e3850}
#pastezone{border:2px dashed #3a4566;border-radius:10px;padding:10px;color:#9aa6c0;font-size:.85rem}
/* 생성 대기 오버레이 */
#loading{position:fixed;inset:0;background:rgba(15,19,32,.96);z-index:9999;display:none;
flex-direction:column;align-items:center;justify-content:center;color:#e8ecf5;text-align:center}
#loading.show{display:flex}
#loading .spin{width:54px;height:54px;border:5px solid #2e3850;border-top-color:#6ea8fe;
border-radius:50%;animation:sp 1s linear infinite;margin-bottom:18px}
@keyframes sp{to{transform:rotate(360deg)}}
#loading .t1{font-size:1.25rem;font-weight:700;color:#6ea8fe}
#loading .t2{font-size:.95rem;color:#9aa6c0;margin-top:8px}
/* 방금 완성 배너: 3개 초과면 스크롤 (동적 제어) */
#doneBox{overflow-y:auto}
#doneList a{color:#ffd166;text-decoration:none}
#doneList div{padding:6px 0;border-bottom:1px solid #2e3850}
</style></head><body>
# Dashboard template is loaded from dashboard_template.html to avoid string escaping issues
def load_dash_template():
    try:
        with open(os.path.join(BASE, "dashboard_template.html"), "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return "<h1>Dashboard template error</h1>"

<div id="loading"><div class="spin"></div>
<div class="t1">⏳ 잠시 기다려 주세요</div>
<div class="t2">문제를 생성하고 있습니다…<br>완성되면 해당 문제로 이동합니다.</div></div>
<div id="dupModal" style="display:none;position:fixed;top:20px;left:50%;transform:translateX(-50%);
z-index:9998;background:#1a2030;border:1px solid #3ddc97;border-radius:14px;padding:16px 22px;
max-width:92%;box-shadow:0 8px 30px rgba(0,0,0,.5);text-align:center">
 <div style="color:#3ddc97;font-weight:700;font-size:1.05rem">📌 같은 문제예요</div>
 <div style="color:#e8ecf5;font-size:.92rem;margin:6px 0">기존 풀이를 최상단에 올려뒀습니다.</div>
 <a id="dupLink" href="#" style="color:#ffd166;font-weight:700;text-decoration:none">기존 풀이 보러가기 →</a>
</div>
<div class="box" id="doneBox" style="display:none;border-color:#3ddc97">
 <h3 style="color:#3ddc97;margin-top:0">✅ 방금 완성된 퀴즈</h3>
 <div id="doneList"></div>
</div>
<h1>📘 mathedu · 퀴즈 생성 게시판</h1>
<div class="box" style="border-color:#6ea8fe;background:#16203a">
 <a href="/board/6wol_mopyung.html" style="color:#ffd166;font-size:1.1rem;font-weight:700;text-decoration:none">📑 2024 6월 고3 모의평가 수학(공통) 전체 풀이 (30문항 단일페이지) →</a>
 <p class="hint" style="margin-top:6px">30개 문항을 한 곳에서 보거나, 각 문항별 개별 단일 파일로 따로 열어볼 수 있습니다.</p>
</div>
<div class="box">
 <h3>새 퀴즈 만들기</h3>
 <form method="post" action="/generate" enctype="multipart/form-data" id="frm">
  <label>문제 제목</label><br>
  <input type="text" name="title" placeholder="예: 2026 6월 모의평가 확통 28번"><br>
  <p class="hint" style="margin-top:6px">어려운 문제를 올리면 쉬운 문제부터 시작하여 단계적으로 문제를 만들어줍니다.<br>제목을 넣지 않아도 이미지 분석하여 제목을 자동 생성합니다.</p><br>
  <label>문제 내용 (텍스트로 붙여넣기)</label><br>
  <div id="pastezone" tabindex="0" style="cursor:pointer">이미지는 <b>Ctrl+V</b> · <b>📋 버튼</b> · <b>여기로 파일 드래그</b> 중 편한 걸로 넣으세요</div><br>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:6px">
    <button type="button" class="tbtn" onclick="pasteFromClipboard()">📋 클립보드에서 이미지 가져오기</button>
  </div>
  <textarea name="problem" id="problem" rows="8" placeholder="문제를 붙여넣으세요..."></textarea><br>
  <label>이미지 (선택, 문제 사진)</label><br>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:6px">
    <button type="button" class="tbtn" onclick="pickImage(false)">🖼️ 갤러리에서 선택</button>
    <button type="button" class="tbtn" onclick="pickImage(true)">📷 카메라로 촬영</button>
  </div>
  <input type="file" name="image" id="image" accept="image/*" style="display:none">
  <img id="prev" alt="선택한 이미지 미리보기">
  <button type="submit">🚀 퀴즈 생성 + 게시</button>
 </form>
 {% if msg and not goto %}<p class="{{'ok' if ok else 'err'}}">{{msg}}</p>{% endif %}
</div>
<div class="box list">
 <h3>📋 게시판 ({{total}}개)</h3>
 {% for it in items %}
  <div>📄 {% if it.pending %}<span style="color:#9aa6c0">{{it.title}}</span>
      {% else %}<a href="/board/{{it.slug}}">{{it.title}}</a>{% endif %}
      <span style="color:#9aa6c0;font-size:.8rem"> — {{it.time}}</span></div>
 {% endfor %}
 {% if total_pages > 1 %}
 <div style="margin-top:14px;display:flex;gap:8px;justify-content:center;align-items:center">
  {% if page > 1 %}<a href="/?page={{page-1}}" style="background:#222a3d;color:#e8ecf5;border:1px solid #2e3850;border-radius:8px;padding:6px 14px;text-decoration:none;font-size:.9rem">◀ 이전</a>{% endif %}
  <span style="color:#9aa6c0;font-size:.9rem">{{page}} / {{total_pages}} 페이지</span>
  {% if page < total_pages %}<a href="/?page={{page+1}}" style="background:#222a3d;color:#e8ecf5;border:1px solid #2e3850;border-radius:8px;padding:6px 14px;text-decoration:none;font-size:.9rem">다음 ▶</a>{% endif %}
 </div>
 {% endif %}
</div>
<script>
const ta=document.getElementById('problem');
const fileInput=document.getElementById('image');
const prev=document.getElementById('prev');
// 이미지 클립보드 → file input 주입 + 미리보기 (공통)
function applyImage(blob){
  if(!blob) return false;
  const file=new File([blob],'pasted_'+Date.now()+'.png',{type:blob.type||'image/png'});
  const dt=new DataTransfer(); dt.items.add(file);
  try{ fileInput.files=dt.files; }catch(err){ /* 일부 브라우저는 files 대입 불가 → 미리보기만 */ }
  const url=URL.createObjectURL(blob);
  prev.src=url; prev.style.display='block';
  const pz=document.getElementById('pastezone');
  pz.textContent='✅ 이미지가 붙여넣어졌어요. 그대로 생성하면 됩니다.';
  pz.style.color='#3ddc97';
  return true;
}
// 경로 1: Ctrl+V (대부분 동작하나 포커스/보안 제약 있음)
document.addEventListener('paste',e=>{
  const cd=(e.clipboardData||window.clipboardData);
  if(!cd) return;
  let blob=null, foundText=false;
  if(cd.items){ for(const it of cd.items){
    if(it.type&&it.type.indexOf('image')===0){ blob=it.getAsFile(); if(blob) break; }
    else if(it.kind==='string') foundText=true;
  }}
  if(!blob&&cd.files&&cd.files.length){ for(const f of cd.files){ if(f.type&&f.type.indexOf('image')===0){ blob=f; break; } } }
  if(blob){ e.preventDefault(); applyImage(blob); }
});
// 경로 2: 📋 버튼 → 공식 Clipboard API (가장 확실, 권한 허용 시)
async function pasteFromClipboard(){
  const pz=document.getElementById('pastezone');
  if(!navigator.clipboard||!navigator.clipboard.read){
    pz.textContent='이 브라우저는 클립보드 읽기를 지원하지 않아요. 대신 🖼️ 갤러리 선택을 쓰세요.';
    pz.style.color='#ff6b6b'; return;
  }
  try{
    const items=await navigator.clipboard.read();
    for(const item of items){
      const type=item.types.find(t=>t.startsWith('image/'));
      if(type){ const blob=await item.getType(type); applyImage(blob); return; }
    }
    pz.textContent='클립보드에 이미지가 없어요. 캡처 후 다시 눌러주세요.';
    pz.style.color='#ffd166';
  }catch(err){
    pz.textContent='클립보드 접근이 차단됐어요. 브라우저가 권한을 물으면 "허용"을 누르세요. (또는 🖼️ 갤러리 선택)';
    pz.style.color='#ff6b6b';
  }
}
// 기존 파일 선택 시에도 미리보기
fileInput.addEventListener('change',()=>{
  if(fileInput.files&&fileInput.files[0]){prev.src=URL.createObjectURL(fileInput.files[0]);prev.style.display='block';}
});
// 경로 3: 드래그앤드롭 (클립보드 의존 없음 — 파일을 직접 끌어다 놓기)
const pz=document.getElementById('pastezone');
['dragover','dragenter'].forEach(ev=>pz.addEventListener(ev,e=>{e.preventDefault();pz.style.borderColor='#3ddc97';}));
['dragleave','drop'].forEach(ev=>pz.addEventListener(ev,e=>{e.preventDefault();pz.style.borderColor='#3a4566';}));
pz.addEventListener('drop',e=>{
  const dt=e.dataTransfer; if(!dt||!dt.files||!dt.files.length) return;
  for(const f of dt.files){ if(f.type.indexOf('image')===0){ applyImage(f); return; } }
});
// 📱 갤러리 / 카메라 선택 버튼
function pickImage(useCamera){
  const fi=document.getElementById('image');
  if(useCamera){ fi.setAttribute('capture','environment'); }
  else { fi.removeAttribute('capture'); }
  fi.value='';  // 같은 파일 재선택 허용
  fi.click();
}
// 생성 버튼 → 대기 오버레이 표시 (실제 제출은 그대로 진행)
document.getElementById('frm').addEventListener('submit',()=>{
  document.getElementById('loading').classList.add('show');
});
// 15초마다 완성된 퀴즈 확인 → 배너 표시 (최근 10분 내 것만)
function checkDone(){
  fetch('/done.json').then(r=>r.json()).then(d=>{
    const items=(d.items||[]).filter(it=>{
      const ts=it.ts||0;
      return (Date.now()/1000 - ts) < 600;  // 10분 이내
    });
    const box=document.getElementById('doneBox');
    const list=document.getElementById('doneList');
    if(items.length){
      box.style.display='block';
      list.innerHTML=items.map(it=>
        `<div>📄 <a href="/board/${it.slug}">${it.title}</a>`+
        ` <span style="color:#9aa6c0;font-size:.8rem"> — ${it.time}</span></div>`).join('');
      // 3개 초과면 스크롤, 3개 이하면 자동 높이
      box.style.maxHeight = items.length > 3 ? '300px' : 'none';
      box.style.overflowY = items.length > 3 ? 'auto' : 'visible';
    } else {
      box.style.display='none';
    }
  }).catch(()=>{});
}
// 중복 안내 팝업: 기존 풀이로 이동
(function(){const p=new URLSearchParams(location.search);const g=p.get('goto');
if(g){const m=document.getElementById('dupModal');document.getElementById('dupLink').href='/board/'+g;
m.style.display='block';setTimeout(()=>{location.href='/board/'+g;},2200);}})();
checkDone(); setInterval(checkDone, 15000);

</script>
</body></html>"""

def make_title(problem, has_image):
    """제목이 없을 때 문제 내용을 분석해 자동 제목 생성 (키워드 기반, 빠름·안정)"""
    # 1) 첫 줄(문단)만 깔끔하게
    first = (problem or "").strip().splitlines()
    first = [l.strip() for l in first if l.strip()]
    snippet = first[0] if first else ""
    # 2) 수학 과목/주제 키워드 매핑
    topic_map = [
        ("확률과통계", ["확률", "조건부", "이항분포", "정규분포", "표본", "상관", "통계", "조합", "순열", "카드", "주사위"]),
        ("미적분", ["미분", "적분", "극한", "도함수", "로그", "지수함수", "미분계수"]),
        ("기하와 벡터", ["벡터", "행렬", "평면", "공간도형", "좌표평면", "행렬식"]),
        ("수학II", ["삼각함수", "수열", "등비", "등차"]),
        ("수학I", ["다항식", "방정식", "부등식", "이차방정식", "근의 공식"]),
        ("수학III", ["허수", "복소수", "극좌표"]),
    ]
    topic = "수학 문제"
    for name, kws in topic_map:
        if any(k in (problem or "") for k in kws):
            topic = name
            break
    # 3) 제목 조합
    if snippet:
        s = snippet if len(snippet) <= 26 else snippet[:26] + "…"
        return f"{topic} · {s}"
    if has_image:
        return f"{topic} · 이미지 문제 ({time.strftime('%H:%M')})"
    return f"{topic} · {time.strftime('%Y-%m-%d %H:%M')}"

def make_sig(problem, image_bytes):
    """중복 판별용 서명: 이미지 문제는 바이트 MD5, 텍스트 문제는 정규화 텍스트 MD5"""
    if image_bytes:
        return "img:" + hashlib.md5(image_bytes).hexdigest()
    norm = re.sub(r"[^\w가-힣]", "", (problem or "").strip().lower())
    norm = re.sub(r"\s+", "", norm)
    return "txt:" + hashlib.md5(norm.encode("utf-8")).hexdigest()

# 수학 관련 키워드/수식 신호 (regex)
_MATH_SIGNALS = [
    r"[0-9]+\s*[+\-*/×÷=]\s*[0-9]",   # 산수식
    r"[0-9]+\s*[+\-*/×÷=]",            # 등호/연산 포함
    r"[a-zA-Z]\s*[=\(]",               # x=, f( 등
    r"[∫∑√πθ∞≤≥±≠≈%]",               # 수학 기호
    r"\b(함수|방정식|부등식|행렬|벡터|미분|적분|극한|확률|조합|순열|통계|기하|삼각|로그|지수|수열|집합|도형|각도|넓이|부피|정답|구하시오|풀이|문제)\b",
    r"[0-9]+개|[0-9]+명|[0-9]+번",      # "~개", "~명", "~번"
    r"[0-9]+%",                        # 퍼센트
    r"\b(점|점수|점수의|평균|합|차|곱|몫)\b",
]
_MATH_RE = re.compile("|".join(_MATH_SIGNALS))
# 비수학 키워드 (한글은 단어경계 \b 가 안 먹히므로 substring 매칭)
_NONMATH_WORDS = ["안녕","반가워","날씨","밥","뭐해","심심","ㅋㅋ","ㅎㅎ","수고",
                  "감사","고마워","사랑","보고싶","어디","언제","누구","재밌","뭐야"]

def is_math_problem(text):
    """텍스트만 있는 경우 1차 수학문제 판별 (로컬 LLM 미사용, 키워드+수식 휴리스틱).
    이미지 문제는 제가 직접 보고 수학 아니면 버리므로 True 반환."""
    if not text or not text.strip():
        return True  # 이미지 등 텍스트 없으면 접수(추후 수동 검토)
    t = text.strip()
    # 비수학 키워드가 포함되면 바로 탈락
    if any(w in t for w in _NONMATH_WORDS):
        return False
    # 수학 신호가 1개 이상 있으면 수학문제로 판단
    return bool(_MATH_RE.search(t))

@app.route("/")
def index():
    msg = request.args.get("msg"); ok = request.args.get("ok")=="1"
    goto = request.args.get("goto")
    all_items = load_meta()
    # 페이지네이션: 페이지당 20개
    page = request.args.get("page", 1, type=int)
    per_page = 20
    total = len(all_items)
    total_pages = max(1, (total + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    items = all_items[start:start + per_page]
    resp = make_response(render_template_string(INDEX_TPL, items=items,
                                   msg=msg, ok=ok, goto=goto,
                                   page=page, total_pages=total_pages,
                                   total=total))
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return resp

@app.route("/generate", methods=["POST"])
def gen():
    raw_title = request.form.get("title","").strip()
    problem = request.form.get("problem","").strip()
    img = request.files.get("image"); img_path = None; img_bytes = None
    if img and img.filename:
        img_bytes = img.read()
        ext = os.path.splitext(img.filename)[1] or ".png"
        if ext.lower() not in (".png",".jpg",".jpeg",".gif",".webp"):
            ext = ".png"
        img_path = os.path.join(BOARD, "img_"+uuid.uuid4().hex+ext)
        with open(img_path, "wb") as fh: fh.write(img_bytes)
    if not problem and not img_path:
        return redirect("/?msg=문제 내용이나 이미지를 넣어주세요.&ok=0")
    # ★ 텍스트만 있는 경우: 수학문제가 아니면 접수하지 않음 (이미지는 제가 직접 검토)
    if problem and not img_path and not is_math_problem(problem):
        return redirect("/?msg=수학 문제만 접수할 수 있어요. 수학 문제를 올려주세요.&ok=0")
    # 제목이 비어있으면 문제 분석해서 자동 생성
    title = raw_title or make_title(problem, bool(img_path))
    # ★ 중복 판별: 같은 문제(이미지 바이트 또는 정규화 텍스트)면 기존 글을 최상단 + 팝업
    sig = make_sig(problem, img_bytes)
    meta = load_meta()
    for i, it in enumerate(meta):
        if it.get("sig") == sig and not it.get("pending"):
            old = meta.pop(i); meta.insert(0, old); save_meta(meta)
            return redirect(f"/?msg=같은 문제예요. 기존 풀이를 최상단에 올려뒀습니다&ok=1&goto={old['slug']}")
    # 로컬 LLM 미사용(M님 지시). 받은 문제를 대기 큐에 접수 → 제가 직접 분석해 퀴즈 제작
    pid = uuid.uuid4().hex[:8]
    pending = {
        "id": pid, "title": title, "problem": problem,
        "image": os.path.basename(img_path) if img_path else None,
        "sig": sig,
        "time": time.strftime("%Y-%m-%d %H:%M")
    }
    os.makedirs(os.path.join(BOARD, "pending"), exist_ok=True)
    json.dump(pending, open(os.path.join(BOARD, "pending", pid+".json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    # ★ 완성 전까지 게시판에 올리지 않음: 대기 큐(pending/)에만 보관
    return redirect(f"/?msg=문제가 접수됐어요. 완성되면 게시합니다.&ok=1")

@app.route("/publish", methods=["POST"])
def publish():
    """제가(허미스) 직접 지은 퀴즈 dict(JSON)를 받아 게시한다.
    pending 접수 → 완성 → 게시 브리지. 원본 캡처 이미지는 게시하지 않음(생성기 안전장치).
    body: JSON {"quiz": {...}, "pid": "pending_id(옵션)", "sig": "중복서명(옵션)"}
    """
    raw = request.get_json(silent=True) or {}
    quiz = raw.get("quiz") or json.loads(request.form.get("quiz", "{}"))
    if not isinstance(quiz, dict) or not quiz.get("title"):
        return {"ok": False, "error": "quiz JSON 필요"}, 400
    # ★ 중복 검사: 같은 sig가 이미 있으면 중복으로 처리
    sig = raw.get("sig") or quiz.get("sig")
    if not sig:
        pid = raw.get("pid") or request.form.get("pid")
        if pid:
            pp = os.path.join(BOARD, "pending", f"{pid}.json")
            if os.path.exists(pp):
                try: sig = json.load(open(pp, encoding="utf-8")).get("sig")
                except Exception: pass
    if not sig:
        sig = make_sig(quiz.get("title", ""), None)
    meta_check = load_meta()
    for it in meta_check:
        if it.get("sig") == sig and not it.get("pending"):
            return {"ok": False, "error": "중복", "existing_slug": it["slug"], "message": "같은 문제가 이미 게시되어 있습니다."}
    # 1) slug 결정 (HTML 생성 전에 설정해야 tracking HTML에 slug가 들어감)
    slug = hashlib.md5((quiz.get("title", "") + str(time.time())).encode()).hexdigest()[:8]
    quiz["slug"] = slug
    # 2) HTML 생성 (안전장치: 원본 img 자동 제거됨)
    html = generator.generate_html(quiz)
    path = os.path.join(BOARD, f"{slug}.html")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    # 2.5) 중복 서명(sig): 호출자가 준 값 우선, 없으면 pending에서 가져오고, 없으면 title 기반 생성
    sig = raw.get("sig") or quiz.get("sig")
    pid = raw.get("pid") or request.form.get("pid")
    if not sig and pid:
        pp = os.path.join(BOARD, "pending", f"{pid}.json")
        if os.path.exists(pp):
            try: sig = json.load(open(pp, encoding="utf-8")).get("sig")
            except Exception: pass
    if not sig:
        sig = make_sig(quiz.get("title", ""), None)
    # 3) index.json 등록 (sig 포함 → 추후 중복 판별 가능)
    meta = load_meta()
    now = time.strftime("%Y-%m-%d %H:%M")
    item = {"slug": slug, "title": quiz.get("title", ""), "time": now,
            "file": f"{slug}.html", "sig": sig}
    meta.insert(0, item)
    save_meta(meta)
    # 4) done.json 등록 (방금 완성 배너용)
    done_p = os.path.join(BOARD, "done.json")
    try:
        done = json.load(open(done_p, encoding="utf-8"))
    except Exception:
        done = []
    if isinstance(done, dict):
        done = done.get("items", [])
    done.insert(0, {"slug": slug, "title": quiz.get("title", ""), "time": now, "ts": int(time.time())})
    json.dump(done, open(done_p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    # 5) 해당 pid의 pending 정리
    if pid and os.path.exists(os.path.join(BOARD, "pending", f"{pid}.json")):
        try: os.remove(os.path.join(BOARD, "pending", f"{pid}.json"))
        except Exception: pass
    return {"ok": True, "slug": slug, "url": f"/board/{slug}"}

@app.route("/done.json")
def done_json():
    p = os.path.join(BOARD, "done.json")
    if not os.path.exists(p): return {"items": []}
    try:
        return {"items": json.load(open(p, encoding="utf-8"))}
    except: return {"items": []}

@app.route("/api/results", methods=["POST"])
def save_result():
    """학생이 퀴즈 완료 후 결과를 전송하는 엔드포인트."""
    data = request.get_json(silent=True) or {}
    quiz_slug = data.get("quiz_slug", "").strip()
    student_name = data.get("student_name", "").strip()
    score = int(data.get("score", 0))
    total = int(data.get("total", 0))
    answers = json.dumps(data.get("answers", []), ensure_ascii=False)
    if not quiz_slug or not student_name or total == 0:
        return {"ok": False, "error": "필수 필드 누락"}, 400
    pct = round(score / total * 100, 1) if total else 0
    conn = get_db()
    conn.execute(
        "INSERT INTO results (quiz_slug, student_name, score, total, pct, answers) VALUES (?, ?, ?, ?, ?, ?)",
        (quiz_slug, student_name, score, total, pct, answers)
    )
    conn.commit()
    conn.close()
    return {"ok": True, "pct": pct}

@app.route("/api/progress", methods=["POST"])
def save_progress():
    """학생이 문제 풀 때마다 진행 상황 실시간 저장."""
    data = request.get_json(silent=True) or {}
    quiz_slug = data.get("quiz_slug", "").strip()
    student_name = data.get("student_name", "").strip()
    current_step = int(data.get("current_step", 0))
    total_steps = int(data.get("total_steps", 0))
    correct = int(data.get("correct", 0))
    if not quiz_slug or not student_name:
        return {"ok": False, "error": "필수 필드 누락"}, 400
    pct = round(correct / total_steps * 100, 1) if total_steps else 0
    conn = get_db()
    conn.execute('''INSERT OR REPLACE INTO progress 
        (quiz_slug, student_name, current_step, total_steps, correct, pct, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, datetime('now'))''',
        (quiz_slug, student_name, current_step, total_steps, correct, pct))
    conn.commit()
    conn.close()
    return {"ok": True, "pct": pct}

@app.route("/api/progress")
def get_progress():
    """대시보드용: 퀴즈별 실시간 진행 목록."""
    quiz_filter = request.args.get("quiz", "").strip()
    conn = get_db()
    if quiz_filter:
        rows = conn.execute(
            "SELECT * FROM progress WHERE quiz_slug=? ORDER BY updated_at DESC LIMIT 200",
            (quiz_filter,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM progress ORDER BY updated_at DESC LIMIT 200"
        ).fetchall()
    conn.close()
    return {"items": [dict(r) for r in rows]}

@app.route("/api/stats")
def get_stats():
    """퀴즈별 통계 (results 기반)."""
    conn = get_db()
    stats = conn.execute(
        "SELECT quiz_slug, COUNT(*) as n, ROUND(AVG(pct),1) as avg_pct, "
        "ROUND(AVG(score),1) as avg_score, MAX(pct) as best, MIN(pct) as worst "
        "FROM results GROUP BY quiz_slug ORDER BY quiz_slug"
    ).fetchall()
    conn.close()
    return {"stats": [dict(s) for s in stats]}

@app.route("/api/results_list")
def get_results_list():
    """최종 제출 목록."""
    quiz_filter = request.args.get("quiz", "").strip()
    conn = get_db()
    if quiz_filter:
        rows = conn.execute(
            "SELECT * FROM results WHERE quiz_slug=? ORDER BY created_at DESC LIMIT 200",
            (quiz_filter,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM results ORDER BY created_at DESC LIMIT 200"
        ).fetchall()
    conn.close()
    return {"items": [dict(r) for r in rows]}

@app.route("/dashboard")
def dashboard():
    """학생 성과 대시보드 (실시간, 회원가입 없음)."""
    return render_template_string(DASHBOARD_2_TPL)

@app.route("/mathjax/<path:filename>")
def board_mathjax(filename):
    return send_from_directory(MATHJAX_DIR, filename)

@app.route("/board/<slug>")
def board_view(slug):
    # 이미지 직접 서빙 (예: /board/img_xxx.png)
    if "." in slug:
        p = os.path.join(BOARD, slug)
        if os.path.exists(p):
            return send_from_directory(BOARD, slug)
        return "없는 파일", 404
    p = os.path.join(BOARD, f"{slug}.html")
    if not os.path.exists(p): return "없는 게시물", 404
    return send_from_directory(BOARD, f"{slug}.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5055, debug=False)
