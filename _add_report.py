#!/usr/bin/env python3
"""Add 'report issue' button to each board HTML and update sheets-script.gs."""
import re, glob

BOARD = "C:/Users/min/Desktop/mathedu/board"

REPORT_BTN = '''
<div class="report-box" style="margin-top:10px;padding:8px;border-top:1px solid rgba(255,255,255,.1);text-align:right">
<button class="report-btn" onclick="reportIssue(this)" style="background:transparent;color:#9aa6c0;border:1px solid #2e3850;border-radius:8px;padding:4px 12px;font-size:.75rem;cursor:pointer;transition:.15s" onmouseover="this.style.borderColor='#ff6b6b';this.style.color='#ff6b6b'" onmouseout="this.style.borderColor='#2e3850';this.style.color='#9aa6c0'">🚨 이 문제에 이상이 있어요</button>
<div class="report-msg" style="display:none;color:#3ddc97;font-size:.75rem;margin-top:4px">✅ 신고가 접수되었어요. 확인 후 고칠게요!</div>
</div>
<script>
function reportIssue(btn){{
  var name=(window._studentName||'익명').trim();
  var slug=window.location.pathname.split('/').pop().replace('.html','');
  var qEl=btn.closest('.q');
  var qNum=qEl?Array.from(document.querySelectorAll('.q')).indexOf(qEl)+1:0;
  var url=window._sheetsApiUrl;
  if(url){{
    fetch(url+'?action=report&quiz='+encodeURIComponent(slug)+'&q='+qNum&name='+encodeURIComponent(name),{{method:'GET'}}).catch(function(){{}});
  }}
  btn.style.display='none';
  btn.nextElementSibling.style.display='block';
  setTimeout(function(){{btn.style.display='';btn.nextElementSibling.style.display='none';}},3000);
}}
</script>'''

n = 0
for path in sorted(glob.glob(f"{BOARD}/*.html")):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    
    if 'report-btn' in html:
        continue
    
    # Insert after each .exp closing div (inside .q blocks)
    # Find pattern: <div class="exp"></div></div>
    html = html.replace(
        '<div class="exp"></div></div>',
        '<div class="exp"></div>' + REPORT_BTN + '</div>'
    )
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    n += 1

print(f"Done: {n} files updated")
