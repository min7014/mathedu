"""퀴즈 dict → 단일 HTML 파일 생성. 저장: board/<slug>.html"""
import json, html, os, hashlib, time, re

TEMPLATE = r"""<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
:root{{--bg:#0d1020;--card:rgba(255,255,255,.10);--card2:rgba(255,255,255,.14);--line:rgba(255,255,255,.20);
--txt:#eef2ff;--sub:#aab4d4;--accent:#7cc4ff;--accent2:#a78bfa;--good:#5eead4;--bad:#fb7185;--gold:#fde68a;
--glass-blur:22px;--glass-shadow:0 8px 32px rgba(0,0,0,.40);--radius:16px}}
*{{box-sizing:border-box}}
body{{margin:0;color:var(--txt);line-height:1.7;
font-family:"Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;
background:
 radial-gradient(circle at 12% 8%, rgba(124,196,255,.35), transparent 42%),
 radial-gradient(circle at 88% 12%, rgba(167,139,250,.32), transparent 40%),
 radial-gradient(circle at 50% 55%, rgba(94,234,212,.18), transparent 45%),
 radial-gradient(circle at 20% 90%, rgba(253,230,138,.15), transparent 40%),
 linear-gradient(160deg,#0a0d1a 0%,#141833 50%,#0a0d1a 100%);
background-attachment:fixed;min-height:100vh}}
.wrap{{max-width:820px;margin:0 auto;padding:24px 18px 80px}}
h1{{font-size:1.55rem;margin:0 0 4px;
background:linear-gradient(90deg,var(--accent),var(--accent2));-webkit-background-clip:text;background-clip:text;color:transparent}}
h2{{font-size:1.2rem;margin:34px 0 10px;color:var(--accent);
border-left:4px solid transparent;border-image:linear-gradient(var(--accent),var(--accent2)) 1;padding-left:10px}}
.lead{{color:var(--sub);font-size:.95rem;margin:0 0 8px}}
.sym{{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:10px 0}}
.sym div{{background:var(--card2);border:1px solid var(--line);border-radius:12px;padding:8px 10px;
font-size:.9rem;backdrop-filter:blur(var(--glass-blur));-webkit-backdrop-filter:blur(var(--glass-blur))}}
.sym b{{color:var(--gold)}}
.q{{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:16px;margin:14px 0;
backdrop-filter:blur(var(--glass-blur));-webkit-backdrop-filter:blur(var(--glass-blur));
box-shadow:var(--glass-shadow);transition:.2s}}
.q:hover{{border-color:rgba(124,196,255,.4)}}
.q .lvl{{font-size:.75rem;color:var(--sub)}}
.q .stem{{font-size:1.02rem;margin:6px 0 12px;font-weight:600}}
.opts{{display:grid;gap:8px}}
.opt{{display:flex;align-items:center;gap:10px;background:var(--card2);border:1px solid var(--line);
border-radius:12px;padding:10px 12px;cursor:pointer;transition:.15s;font-size:.95rem;
backdrop-filter:blur(var(--glass-blur));-webkit-backdrop-filter:blur(var(--glass-blur))}}
.opt:hover{{border-color:var(--accent);transform:translateY(-1px)}}
.opt .n{{width:24px;height:24px;flex:0 0 24px;border-radius:50%;background:rgba(124,196,255,.25);
display:flex;align-items:center;justify-content:center;font-size:.8rem;color:var(--accent)}}
.opt.correct{{background:rgba(94,234,212,.16);border-color:var(--good)}}
.opt.wrong{{background:rgba(251,113,133,.16);border-color:var(--bad)}}
.opt.locked{{cursor:default}}
.exp{{margin-top:12px;padding:10px 12px;border-radius:12px;background:rgba(124,196,255,.1);
border:1px solid var(--line);font-size:.9rem;display:none;backdrop-filter:blur(var(--glass-blur));-webkit-backdrop-filter:blur(var(--glass-blur))}}
.exp.show{{display:block}}
.exp b{{color:var(--gold)}}
.score{{position:sticky;top:0;z-index:50;background:rgba(13,16,32,.7);padding:12px 0;border-bottom:1px solid var(--line);
display:flex;justify-content:space-between;align-items:center;font-size:.95rem;
backdrop-filter:blur(var(--glass-blur));-webkit-backdrop-filter:blur(var(--glass-blur))}}
.score b{{color:var(--gold)}}
.bar{{height:8px;background:rgba(255,255,255,.1);border-radius:6px;overflow:hidden;flex:1;margin:0 12px}}
.bar > i{{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--accent),var(--good));transition:.3s}}
.know{{background:var(--card);border:1px dashed var(--accent);border-radius:14px;padding:14px;margin:12px 0;font-size:.92rem;
backdrop-filter:blur(var(--glass-blur));-webkit-backdrop-filter:blur(var(--glass-blur))}}
.know h3{{margin:0 0 6px;color:var(--accent);font-size:1rem}}
.cards{{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:14px 0}}
.card{{width:64px;height:92px;border-radius:10px;display:flex;flex-direction:column;
align-items:center;justify-content:center;font-weight:700;border:2px solid rgba(255,255,255,.25)}}
.card .num{{font-size:1.3rem}}
.card .face{{font-size:.7rem;margin-top:4px;opacity:.85}}
.card.front{{background:rgba(244,247,255,.85);color:#1b2436;border-color:#cfd8ee;backdrop-filter:blur(var(--glass-blur));-webkit-backdrop-filter:blur(var(--glass-blur))}}
.card.back{{background:rgba(57,67,95,.85);color:#fff;border-color:#56638c;backdrop-filter:blur(var(--glass-blur));-webkit-backdrop-filter:blur(var(--glass-blur))}}
.sol{{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:18px;margin:14px 0;
backdrop-filter:blur(var(--glass-blur));-webkit-backdrop-filter:blur(var(--glass-blur));box-shadow:var(--glass-shadow)}}
.diagram{{background:rgba(255,255,255,.92);color:#1b2436;border:1px solid var(--line);border-radius:12px;padding:14px;margin:14px 0;text-align:center;backdrop-filter:blur(var(--glass-blur));-webkit-backdrop-filter:blur(var(--glass-blur))}}
.diagram svg,.diagram img{{max-width:100%;height:auto}}
.btn{{background:linear-gradient(90deg,var(--accent),var(--accent2));color:#0b1020;border:none;border-radius:10px;
padding:10px 18px;font-weight:700;cursor:pointer;box-shadow:0 4px 14px rgba(124,196,255,.3);transition:.15s}}
.btn:hover{{transform:translateY(-1px);box-shadow:0 6px 20px rgba(124,196,255,.45)}}
.final{{text-align:center;margin:30px 0;font-size:1.05rem}}
.final .ans{{font-size:1.6rem;color:var(--good);font-weight:800;margin:8px 0}}
code{{background:rgba(255,255,255,.08);padding:1px 6px;border-radius:6px;color:var(--gold)}}
.topbar{{display:flex;gap:8px;margin-bottom:14px;flex-wrap:wrap}}
.tbtn{{background:var(--card2);color:var(--txt);border:1px solid var(--line);border-radius:10px;
padding:8px 14px;font-weight:700;cursor:pointer;text-decoration:none;font-size:.9rem;display:inline-flex;align-items:center;
backdrop-filter:blur(var(--glass-blur));-webkit-backdrop-filter:blur(var(--glass-blur));transition:.15s}}
.tbtn:hover{{border-color:var(--accent);color:var(--accent)}}
#trackSubmit{{max-width:820px;margin:30px auto;padding:20px;background:rgba(110,168,254,.08);border:1px solid rgba(110,168,254,.3);border-radius:14px;text-align:center}}
#trackSubmit h3{{color:#6ea8fe;margin:0 0 10px}}
#trackSubmit p{{color:#9aa6c0;font-size:.88rem;margin:0 0 12px}}
#trackSubmit input{{background:#222a3d;color:#e8ecf5;border:1px solid #2e3850;border-radius:8px;padding:10px 14px;font-size:.95rem;min-width:160px}}
#trackSubmit button{{background:#6ea8fe;color:#0b1020;border:none;border-radius:8px;padding:10px 20px;font-weight:700;cursor:pointer}}
#trackResult{{display:none;padding:10px;border-radius:10px;font-weight:700}}
</style>
<script>window.MathJax={{tex:{{inlineMath:[['$','$'],['\\(','\\)']]}}}};</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml-full.js"></script>
</head><body><div class="wrap">
<div class="topbar">
<a class="tbtn" href="/mathedu/">← 게시판</a>
<button class="tbtn" id="copyBtn" onclick="copyLink()">🔗 링크 복사</a>
</div>
<div class="score"><span>점수 <b id="pts">0</b> / <b id="tot">0</b></span>
<span class="bar"><i id="bar"></i></span><span id="pct">0%</span></div>
<h1>📘 {title}</h1>
<p class="lead">기초→심화 단계별 5지선다 퀴즈. 정답 고르면 바로 채점+해설이 열립니다.</p>
{symbols_block}
{levels_block}
{tracking_block}
{solution_block}
<div class="final"><p>🎉 완료!</p><div class="ans" id="finalAns">정답 {final_ans}</div>
<button class="btn" onclick="location.reload()">다시 풀기</button></div>
</div><script>
const qs=document.querySelectorAll('.q');let pts=0;
document.getElementById('tot').textContent=qs.length;
qs.forEach(q=>{{const ans=+q.dataset.ans;const exp=q.querySelector('.exp');
exp.innerHTML=q.dataset.exp;const opts=q.querySelectorAll('.opt');
opts.forEach((o,i)=>{{o.addEventListener('click',()=>{{if(q.classList.contains('done'))return;
q.classList.add('done');opts.forEach((oo,j)=>{{oo.classList.add('locked');if(j+1==ans)oo.classList.add('correct');}});
if(i+1==ans){{o.classList.add('correct');pts++;}}else{{o.classList.add('wrong');}}
exp.classList.add('show');document.getElementById('pts').textContent=pts;
const pct=Math.round(pts/qs.length*100);document.getElementById('bar').style.width=pct+'%';
document.getElementById('pct').textContent=pct+'%';}});}});}});
function sendProgress(){{
  var name = (window._studentName || '').trim();
  if (!name) return;
  var qs = document.querySelectorAll('.q');
  var total = qs.length;
  var done = document.querySelectorAll('.q.done');
  var correct = 0;
  document.querySelectorAll('.q.done').forEach(function(q){{
    var c = q.querySelector('.opt.correct');
    if (c) correct++;
  }});
  var current = done.length;
  if (current === 0) return;
  var url = window._sheetsApiUrl || '/api/progress';
  fetch(url, {{
    method: 'POST',
    headers: {{'Content-Type': 'application/json'}},
    body: JSON.stringify({{
      quiz_slug: '{slug_js}',
      student_name: name,
      current_step: current,
      total_steps: total,
      correct: correct
    }})
  }}).catch(()=>{{}});
}}
function copyLink(){{const b=document.getElementById('copyBtn');const t=b.textContent;
navigator.clipboard.writeText(location.href).then(()=>{{b.textContent='✅ 복사됨';setTimeout(()=>b.textContent=t,1500);}})
.catch(()=>{{prompt('아래 링크를 복사하세요',location.href);}}}}
function toggleReport(el){{
  if(!el) return;
  var wrap=el.closest ? el.closest('.report-wrap') : el.parentElement;
  if(!wrap) return;
  var btn=wrap.querySelector('.report-btn');
  var form=wrap.querySelector('.report-form');
  if(!btn||!form) return;
  if(form.style.display==='none'){{
    form.style.display='block';
    btn.style.display='none';
  }} else {{
    form.style.display='none';
    btn.style.display='block';
  }}
}}
function submitReport(btn){{
  var wrap=btn.closest('.report-wrap');
  var name=(window._studentName||'익명').trim();
  var slug=window.location.pathname.split('/').pop().replace('.html','');
  var qEl=wrap.closest('.q');
  var qNum=qEl?Array.from(document.querySelectorAll('.q')).indexOf(qEl)+1:0;
  var text=wrap.querySelector('.report-text').value.trim();
  var url=window._sheetsApiUrl||'https://script.google.com/macros/s/AKfycbxQBW1hKYFSHokaVJMRql-UJpk0t4qMeWMiiy_RFuCLZ5SE4iZytYQkGa9_yoCmm1Ak0Q/exec';
  if(url){{
    var img=new Image();
    img.src=url+'?action=report&quiz='+encodeURIComponent(slug)+'&q='+qNum+'&name='+encodeURIComponent(name)+'&text='+encodeURIComponent(text||'사유 없음')+'&_t='+Date.now();
  }}
  wrap.querySelector('.report-form').style.display='none';
  wrap.querySelector('.report-msg').style.display='block';
  setTimeout(function(){{
    wrap.querySelector('.report-msg').style.display='none';
    wrap.querySelector('.report-btn').style.display='block';
  }},4000);
}}
</script></body></html>"""

def _esc(s): return html.escape(str(s))

REPORT_WRAP_HTML = '''<div class="report-wrap" style="margin-top:10px;border-top:1px solid rgba(255,255,255,.1);padding-top:10px">
<button class="report-btn" onclick="toggleReport(this)" style="background:transparent;color:#9aa6c0;border:1px solid #2e3850;border-radius:8px;padding:4px 12px;font-size:.75rem;cursor:pointer;transition:.15s" onmouseover="this.style.borderColor='#ff6b6b';this.style.color='#ff6b6b'" onmouseout="this.style.borderColor='#2e3850';this.style.color='#9aa6c0'">🚨 이 문제에 이상이 있어요</button>
<div class="report-form" style="display:none;margin-top:10px;text-align:left">
<div style="color:#9aa6c0;font-size:.75rem;margin-bottom:6px">어떤 부분이 이상한가요? 자세히 적어주세요.</div>
<textarea class="report-text" rows="3" placeholder="예: 보기 3번이 정답이 아닌 것 같습니다. / 문제의 조건이 모호합니다. / 계산 오류가 있습니다." style="width:100%;background:rgba(13,16,32,.6);color:#eef2ff;border:1px solid #2e3850;border-radius:8px;padding:8px;font-size:.85rem;resize:vertical;box-sizing:border-box"></textarea>
<div style="display:flex;gap:6px;margin-top:6px;justify-content:flex-end">
<button class="report-cancel" onclick="toggleReport(this)" style="background:transparent;color:#9aa6c0;border:1px solid #2e3850;border-radius:8px;padding:4px 10px;font-size:.75rem;cursor:pointer">취소</button>
<button class="report-submit" onclick="submitReport(this)" style="background:linear-gradient(90deg,#ff6b6b,#ee5a5a);color:#fff;border:none;border-radius:8px;padding:4px 12px;font-size:.75rem;cursor:pointer">신고 접수</button>
</div>
</div>
<div class="report-msg" style="display:none;color:#3ddc97;font-size:.75rem;margin-top:6px;text-align:right">✅ 신고가 접수되었어요. 확인 후 고칠게요!</div>
</div>'''

def _question_html(q):
    opts = "".join(
        f'<div class="opt"><span class="n">{i+1}</span>{_esc(o)}</div>'
        for i, o in enumerate(q.get("options", [])))
    exp = _esc(q.get("exp", "")).replace("\n", "<br>")
    return (f'<div class="q" data-ans="{q.get("answer",1)}" data-exp="{exp}">'
            f'<div class="lvl">문항</div>'
            f'<div class="stem">{_esc(q.get("stem","") )}</div>'
            f'<div class="opts">{opts}</div>'
            f'<div class="exp"></div>'
            f'{REPORT_WRAP_HTML}</div>')

def _level_html(lvl):
    know = ""
    if lvl.get("knowledge"):
        know = (f'<div class="know"><h3>먼저 알아야 할 지식</h3>{_esc(lvl["knowledge"])}</div>')
    qs = "".join(_question_html(q) for q in lvl.get("questions", []))
    return f'<h2>{_esc(lvl.get("title",""))}</h2>{know}{qs}'

def _tracking_html(quiz_slug, sheets_api_url=''):
    """Full-screen name gate."""
    slug_js = quiz_slug.replace("'", "\\'")
    html = '<div id="trackFull" style="position:fixed;inset:0;z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;background:linear-gradient(160deg,#0a0d1a 0%,#141833 50%,#0a0d1a 100%);padding:24px;text-align:center">'
    html += '<h2 style="background:linear-gradient(90deg,#7cc4ff,#a78bfa);-webkit-background-clip:text;background-clip:text;color:transparent;font-size:1.6rem;margin:0 0 8px">📘 mathedu</h2>'
    html += '<h3 style="color:#e8ecf5;margin:0 0 6px">📝 먼저 이름을 입력하세요</h3>'
    html += '<p style="color:#9aa6c0;font-size:.9rem;margin:0 0 20px">이름을 입력해야 학습 기록이 저장됩니다.</p>'
    html += '<div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap">'
    html += '<input type="text" id="studentName" placeholder="이름 입력" autofocus style="background:#222a3d;color:#e8ecf5;border:1px solid #2e3850;border-radius:10px;padding:12px 16px;font-size:1.05rem;min-width:200px;text-align:center">'
    html += '<button class="btn" onclick="registerName()" style="font-size:1.05rem;padding:12px 24px">시작하기</button>'
    html += '</div></div>'
    html += '<script>'
    html += 'window._studentName="";'
    html += 'window._sheetsApiUrl="' + sheets_api_url + '";'
    html += 'function registerName(){'
    html += 'var n=document.getElementById("studentName").value.trim();'
    html += 'if(!n){alert("이름을 입력하세요");return;}'
    html += 'window._studentName=n;'
    html += 'document.getElementById("trackFull").remove();'
    html += 'sendProgress();'
    html += 'if(window.MathJax&&MathJax.typesetPromise){MathJax.typesetPromise();}'
    html += '}'
    html += 'function sendProgress(){'
    html += 'var name=(window._studentName||"").trim();'
    html += 'if(!name)return;'
    html += 'var qs=document.querySelectorAll(".q");'
    html += 'var total=qs.length;'
    html += 'var done=document.querySelectorAll(".q.done");'
    html += 'var correct=0;'
    html += 'done.forEach(function(q){if(q.querySelector(".opt.correct"))correct++;});'
    html += 'if(total===0)return;'
    html += 'fetch(window._sheetsApiUrl,{'
    html += 'method:"POST",headers:{"Content-Type":"application/json"},'
    html += 'body:JSON.stringify({quiz_slug:"' + slug_js + '",student_name:name,current_step:done.length,total_steps:total,correct:correct})'
    html += '}).catch(function(){});'
    html += '}'
    # Answer selection triggers sendProgress after done is set
    html += 'document.querySelectorAll(".q").forEach(function(q){'
    html += 'q.addEventListener("click",function(e){'
    html += 'var opt=e.target.closest(".opt");'
    html += 'if(opt){setTimeout(sendProgress,50);}'
    html += '});'
    html += '});'
    html += 'document.getElementById("studentName").addEventListener("keydown",function(e){if(e.key==="Enter")registerName();});'
    html += '</script>'
    return html



def generate_html(data):
    sym = "".join(
        f'<div><b>{_esc(s.get("sym","") )}</b> — {_esc(s.get("desc",""))}</div>'
        for s in data.get("symbols", []))
    symbols_block = (f'<h2>🔰 제0단계 · 수학 기호</h2><div class="sym">{sym}</div>' if sym else "")
    levels_block = "".join(_level_html(l) for l in data.get("levels", []))
    f = data.get("final", {})
    fopts = "".join(
        f'<div class="opt"><span class="n">{i+1}</span>{_esc(o)}</div>'
        for i, o in enumerate(f.get("options", [])))
    fexp = _esc(f.get("exp", "")).replace("\n", "<br>")
    fsol = f.get("solution", "")
    if not isinstance(fsol, str): fsol = str(fsol)
    diagram_html = ""
    if f.get("diagram"):
        diagram_html = f'<div class="diagram">{f["diagram"]}</div>'
    figure_html = ""
    if f.get("figure"):
        figure_html = f'<div class="figure"><img src="{_esc(f["figure"])}" alt="문제 그림" style="max-width:100%;border-radius:10px"></div>'
    solution_block = (
        f'<h2>🎯 최종 문제 + 상세 풀이</h2>'
        f'{diagram_html}'
        f'{figure_html}'
        f'<div class="sol">{fsol}</div>'
        f'<div class="q" data-ans="{f.get("answer",1)}" data-exp="{fexp}">'
        f'<div class="lvl">최종 본문항</div>'
        f'<div class="stem">{_esc(f.get("stem","") )}</div>'
        f'<div class="opts">{fopts}</div>'
        f'<div class="exp"></div>'
        f'{REPORT_WRAP_HTML}</div>')
    final_ans = ""
    try: final_ans = f.get("options", [])[int(f.get("answer", 1)) - 1]
    except Exception: final_ans = ""
    # ★ 학습 현황 추적 블록
    _sheets_url = data.get("sheets_api_url", "")
    if not _sheets_url:
        try:
            _url_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "progress-api-url.txt")
            if os.path.exists(_url_path):
                with open(_url_path, "r", encoding="utf-8") as _f:
                    _sheets_url = _f.read().strip()
        except Exception:
            pass
    tracking_block = _tracking_html(data.get("slug", ""), _sheets_url)
    slug_js = data.get("slug", "").replace("'", "\\'")
    html = TEMPLATE.format(
        title=_esc(data.get("title", "퀴즈")),
        symbols_block=symbols_block, levels_block=levels_block,
        solution_block=solution_block, final_ans=_esc(final_ans),
        tracking_block=tracking_block,
        slug_js=slug_js)
    # ★ 안전장치: 원본 캡처 이미지(img_xxx.png 등)가 게시물에 그대로 박이는 것 차단
    html = re.sub(r'<img[^>]*src=["\']?[^\"\']*img_[0-9a-f]+\.[a-z]+["\']?[^>]*>', '', html, flags=re.I)
    return html

def save(data, board_dir="board"):
    os.makedirs(board_dir, exist_ok=True)
    slug = hashlib.md5((data.get("title","quiz")+str(time.time())).encode()).hexdigest()[:8]
    data["slug"] = slug
    html = generate_html(data)
    path = os.path.join(board_dir, f"{slug}.html")
    with open(path, "w", encoding="utf-8") as fh: fh.write(html)
    return slug, path

if __name__ == "__main__":
    import ollama_client
    d = ollama_client._mock()
    slug, path = save(d, "board")
    print("saved", slug, path)
