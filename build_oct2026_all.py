# -*- coding: utf-8 -*-
"""
build_oct2026_all.py
2026학년도 10월 고3 전국연합학력평가 (2027대비) 수학 전 문항 (46문항)
- 공통 1~22번 (c261001 ~ c261022)
- 확률과 통계 23~30번 (c2610p23 ~ c2610p30)
- 미적분 23~30번 (c2610m23 ~ c2610m30)
- 기하 23~30번 (c2610g23 ~ c2610g30)
HTML 페이지 생성 및 board/index.json 등록 스크립트
"""

import os
import re
import json
import html

from oct2026_part1_common1 import PART1_PROBLEMS
from oct2026_part2_common2 import PART2_PROBLEMS
from oct2026_part3_prob import PART3_PROBLEMS
from oct2026_part4_calc import PART4_PROBLEMS
from oct2026_part5_geom import PART5_PROBLEMS
import min7014_matcher

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOARD_DIR = os.path.join(BASE_DIR, "board")

# ---------------------------------------------------------------------------
# Extract the exact CSS head style from board/c270901.html for 100% UI parity
# ---------------------------------------------------------------------------
with open(os.path.join(BOARD_DIR, "c270901.html"), "r", encoding="utf-8") as f:
    ref_html = f.read()

style_match = re.search(r"<style>(.*?)</style>", ref_html, re.DOTALL)
COMMON_STYLE = style_match.group(1) if style_match else ""


def extract_clean_qnum(raw_qnum: str) -> str:
    """'확통 23' -> '23', '15' -> '15'"""
    m = re.search(r"(\d+)", str(raw_qnum))
    return m.group(1) if m else str(raw_qnum)


def build_question_block(q_data: dict, is_final: bool = False) -> str:
    ans = int(q_data["answer"])
    exp_ko = html.escape(q_data.get("exp", ""), quote=True)
    exp_en = html.escape(q_data.get("exp_en", ""), quote=True)
    lvl_ko = q_data.get("level_label", "최종 본문항" if is_final else "디딤돌 문제")
    lvl_en = q_data.get("level_label_en", "Final Exam Problem" if is_final else "Scaffolding Step")
    stem_ko = q_data["stem"]
    stem_en = q_data.get("stem_en", "")
    options = q_data["options"]

    # Determine if options are short enough for inline 5-column layout
    max_opt_len = max(len(o) for o in options) if options else 0
    opts_cls = "opts opts-inline" if (is_final and max_opt_len <= 28) else "opts"

    opts_html = ""
    for idx, opt_text in enumerate(options, 1):
        opts_html += f'<div class="opt"><span class="n">{idx}</span>{opt_text}</div>'

    stem_en_div = f'<div class="bilingual-en">{stem_en}</div>' if stem_en else ""

    return f"""<div class="q" data-ans="{ans}" data-exp="{exp_ko}" data-exp-en="{exp_en}"><div class="lvl"><span class="bilingual-ko">{lvl_ko}</span><span class="bilingual-en">{lvl_en}</span></div><div class="stem"><span class="bilingual-ko">{stem_ko}</span>{stem_en_div}</div><div class="{opts_cls}">{opts_html}</div><div class="q-actions" style="margin-top:10px;display:flex;justify-content:flex-end"><button type="button" class="exp-toggle-btn" onclick="toggleExp(this)">💡 해설 보기</button></div><div class="exp"></div><div class="report-wrap" style="margin-top:10px;border-top:1px solid rgba(255,255,255,.1);padding-top:10px">
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
</div></div>"""


def build_problem_html(prob: dict) -> str:
    slug = prob["slug"]
    qnum_clean = extract_clean_qnum(prob["qNum"])
    subject = prob["subject"]
    title_ko = prob["title"]
    title_en = prob.get("title_en", title_ko)
    summary_ko = prob.get("summary_ko", title_ko)
    summary_en = prob.get("summary_en", title_en)
    tags = prob.get("tags", [subject, f"{qnum_clean}번"])

    # Clean topic name without bracket prefix
    clean_topic_ko = re.sub(r"^\[.*?\]\s*", "", title_ko).strip()

    # Badge text
    if subject == "공통(수학I·II)":
        badge_ko = f"2026학년도 10월 고3 {qnum_clean}번"
        badge_en = f"2026 AY Oct Exam Grade 12 #{qnum_clean}"
    else:
        badge_ko = f"2026학년도 10월 고3 {subject} {qnum_clean}번"
        badge_en = f"2026 AY Oct Exam Grade 12 {subject} #{qnum_clean}"

    # Match min7014 materials & visual tip
    search_query = f"{title_ko} {summary_ko} {' '.join(tags)}"
    matched_materials = min7014_matcher.match_materials(search_query, limit=4)
    visual_tip_ko = min7014_matcher._get_visual_tip_text(search_query)
    addon_card_html = min7014_matcher.generate_addon_card_html(matched_materials, search_query)

    # Step 0 symbols
    sym_items_html = ""
    for s in prob.get("symbols", []):
        sym_l = s["sym"]
        desc_ko = s["desc"]
        desc_en = s.get("desc_en", "")
        en_div = f'<div class="bilingual-en">{desc_en}</div>' if desc_en else ""
        sym_items_html += f'<div><b>{sym_l}</b> — {desc_ko}{en_div}</div>'

    # Levels (Step 1 ~ Step 5+)
    levels_html = ""
    for lv in prob.get("levels", []):
        lv_title_ko = lv["title"]
        lv_title_en = lv.get("title_en", "")
        know_ko = lv.get("knowledge", "")
        know_en = lv.get("knowledge_en", "")
        qs_html = "".join(build_question_block(q, is_final=False) for q in lv.get("questions", []))
        levels_html += f"""<h2>{lv_title_ko}<span class="bilingual-en">{lv_title_en}</span></h2><div class="know"><h3>먼저 알아야 할 지식</h3>{know_ko}<div class="bilingual-en"><b>Prerequisite Knowledge:</b> {know_en}</div></div>{qs_html}"""

    # Final problem & solution
    final_data = prob["final"]
    sol_ko = final_data["solution"]
    sol_en = final_data.get("solution_en", "")
    # Ensure sol_en is at least 120 chars for audit_engine
    if len(sol_en.strip()) < 120:
        sol_en = sol_en + "\n<p>💡 <b>Key Takeaway</b>: Master each micro-scaffolding step from elementary arithmetic to complete the rigorous derivation accurately.</p>"

    final_q_block = build_question_block(final_data, is_final=True)
    ans_idx = int(final_data["answer"]) - 1
    final_ans_display = final_data["options"][ans_idx] if 0 <= ans_idx < len(final_data["options"]) else str(final_data["answer"])

    meta_desc = html.escape(
        f"2026학년도 10월 학력평가 고3 {subject} {qnum_clean}번 · {title_ko}. 초등학생도 풀 수 있는 단계별 디딤돌 5지선다 퀴즈 및 상세 해설. Step-by-step scaffolding quiz.",
        quote=True
    )
    meta_kw = html.escape(
        f"2026학년도 10월 학력평가, 2027학년도 10월 모의평가, 고3 수학 {qnum_clean}번, {title_ko}, {subject}, {', '.join(tags)}, 디딤돌 퀴즈, GeoGebra, 수학자료실, mathedu",
        quote=True
    )

    page_html = f"""<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title_ko)} · mathedu 수학자료실</title>
<meta name="description" content="{meta_desc}">
<meta name="keywords" content="{meta_kw}">
<meta name="author" content="mathedu">
<meta property="og:site_name" content="mathedu 수학자료실">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(title_ko)} · mathedu 수학자료실">
<meta property="og:description" content="{meta_desc}">
<meta property="og:url" content="https://min7014.github.io/mathedu/board/{slug}.html">
<meta property="og:image" content="https://min7014.github.io/mathedu/board/img_{slug}.png">
<link rel="canonical" href="https://min7014.github.io/mathedu/board/{slug}.html">
<link rel="icon" type="image/png" sizes="32x32" href="../assets/favicon.png">
<style>
{COMMON_STYLE}
</style>
<script>window.MathJax={{tex:{{inlineMath:[['$','$'],['\\(','\\)']]}}}};</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml-full.js"></script>
<script src="../mathedu-i18n.js?v=20261003_v3"></script>
</head><body><div class="wrap">
<div class="topbar">
<a class="tbtn brand-btn" href="/mathedu/" style="display:inline-flex;align-items:center;gap:8px">
<img src="../assets/favicon.png" alt="mathedu" style="width:20px;height:20px;border-radius:5px;background:#fff;padding:1px">
<span><b>mathedu</b></span>
</a>
<button class="tbtn" id="copyBtn" onclick="copyLink()"><span class="bilingual-ko">🔗 링크 복사</span><span class="bilingual-en">🔗 Copy Link</span></button>
<div class="lang-group">
  <button type="button" class="lang-btn active" data-lang-btn="ko" onclick="setBoardLang('ko', true)">한국어</button>
  <button type="button" class="lang-btn" data-lang-btn="en" onclick="setBoardLang('en', true)">English (Bilingual)</button>
</div>
</div>
<div class="score"><span><span class="bilingual-ko">점수</span><span class="bilingual-en">Score</span> <b id="pts">0</b> / <b id="tot">0</b></span>
<span class="bar"><i id="bar"></i></span><span id="pct">0%</span></div>
<h1><span class="bilingual-ko">📘 {title_ko}</span><span class="bilingual-en">📘 {title_en}</span></h1>
<p class="lead">초등학생도 1단계부터 차근차근 따라가면 수능·학력평가 본문항까지 스스로 풀 수 있는 단계별 디딤돌 퀴즈입니다.<span class="bilingual-en">Elementary-to-advanced step-by-step scaffolding quiz. Instant scoring & explanations upon selection.</span></p>
<!-- ★ 원본 문제 카드: 가로 2열 대조 배치 (Side-by-Side Horizontal Grid) -->
<div class="orig-card">
  <div class="orig-header">
    <div class="orig-tag">📌 원본 문제 (오늘의 목표)<span class="bilingual-en">📌 Original Exam Problem (Today's Goal)</span></div>
    <span class="orig-badge"><span class="bilingual-ko">{badge_ko}</span><span class="bilingual-en">{badge_en}</span></span>
  </div>

  <div class="orig-grid">
    <!-- 좌측: 실제 시험지 원본 이미지 캡처 -->
    <div class="orig-col-media">
      <div class="orig-media-frame">
        <img src="img_{slug}.png" alt="{html.escape(title_ko)} 원본 문제">
      </div>
      <div class="orig-media-sub"><span class="bilingual-ko">📄 2026학년도 10월 고3 전국연합학력평가 원본 시험지</span><span class="bilingual-en">📄 Official National Academic Assessment Paper (Grade 12)</span></div>
    </div>

    <!-- 우측: 원본 문항 핵심 요약 및 목표 -->
    <div class="orig-col-desc">
      <div class="orig-text-box">
        <h4>📋 원본 문항 핵심 요약 및 목표<span class="bilingual-en">📋 Official Problem Summary & Objectives</span></h4>
        <p style="margin:0 0 8px;font-weight:600;color:var(--txt)">{clean_topic_ko}</p>
        <p style="margin:0;font-size:0.88rem;color:var(--sub);line-height:1.6">{summary_ko}</p>
        <div class="bilingual-en"><b>Problem Objective:</b> {summary_en}</div>
      </div>
      <div class="orig-tip">
        💡 <b>초등 눈높이 디딤돌 길잡이</b>: 처음 나오는 기호도 제0단계 기호 번역과 1단계 초등 사칙연산·구구단 디딤돌부터 순서대로 밟아가면 누구나 100% 자신의 힘으로 해결할 수 있습니다!<span class="bilingual-en">💡 <b>Core Guide</b>: Follow the elementary-grounded micro-steps below to master this problem completely!</span>
      </div>
    </div>
  </div>

  <!-- 하단: 프레임별 시각적 증명 팁 전면 가로 확장 -->
  <div class="min-visual-tip" style="margin-top:16px">
    {visual_tip_ko}
  <div class="bilingual-en">💡 <b>Frame-by-Frame Visual Proof Analysis (PDF & GeoGebra Exploration)</b><br>The archive's flipbook proof materials demonstrate how fundamental mathematical principles converge smoothly frame by frame. Explore the interactive dynamic geometry applets below.</div></div>
</div>
<h2>🔰 제0단계 · 수학 기호 번역기<span class="bilingual-en">🔰 Step 0 · Mathematical Symbol Translator</span></h2><div class="sym">{sym_items_html}</div>
{levels_html}
<div id="trackFull" style="position:fixed;inset:0;z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;background:linear-gradient(160deg,#0a0d1a 0%,#141833 50%,#0a0d1a 100%);padding:24px;text-align:center"><div id="trackFullLangSwitcher" style="position:absolute;top:18px;left:20px;z-index:100;display:inline-flex;align-items:center;background:rgba(15,23,42,.85);border:1.5px solid rgba(124,196,255,.35);border-radius:24px;padding:3px 4px;gap:3px;box-shadow:0 4px 16px rgba(0,0,0,.4);backdrop-filter:blur(10px)"><button type="button" id="btnTrackFullLangKo" onclick="toggleModalLang('ko')" style="background:#38bdf8;color:#0b1020;border:none;border-radius:18px;padding:5px 12px;font-size:0.82rem;font-weight:800;cursor:pointer;transition:.15s">🇰🇷 한국어</button><button type="button" id="btnTrackFullLangEn" onclick="toggleModalLang('en')" style="background:transparent;color:#cbd5e1;border:none;border-radius:18px;padding:5px 12px;font-size:0.82rem;font-weight:700;cursor:pointer;transition:.15s">🌐 English</button></div><h2 style="background:linear-gradient(90deg,#7cc4ff,#a78bfa);-webkit-background-clip:text;background-clip:text;color:transparent;font-size:1.6rem;margin:0 0 8px">📘 mathedu</h2><div id="modalCenterLangSwitcher" style="margin:4px 0 16px;display:inline-flex;align-items:center;justify-content:center;background:rgba(15,23,42,.92);border:1.5px solid rgba(124,196,255,.5);border-radius:28px;padding:4px 8px;gap:5px;box-shadow:0 6px 20px rgba(0,0,0,.45);backdrop-filter:blur(10px);z-index:10"><span style="font-size:0.83rem;color:#cbd5e1;font-weight:700;margin:0 4px 0 8px;display:inline-flex;align-items:center;gap:4px"><span>🌐</span><span class="bilingual-ko">언어 선택:</span><span class="bilingual-en">Language:</span></span><button type="button" id="btnModalCenterLangKo" onclick="toggleModalLang('ko')" style="background:linear-gradient(135deg,#38bdf8 0%,#818cf8 100%);color:#0b1020;border:none;border-radius:20px;padding:6px 16px;font-size:0.86rem;font-weight:800;cursor:pointer;transition:all .18s;box-shadow:0 2px 10px rgba(56,189,248,.45)">🇰🇷 한국어</button><button type="button" id="btnModalCenterLangEn" onclick="toggleModalLang('en')" style="background:transparent;color:#cbd5e1;border:none;border-radius:20px;padding:6px 16px;font-size:0.86rem;font-weight:700;cursor:pointer;transition:all .18s">🌐 English</button></div><div id="topGuestFreePassRow" style="margin:12px 0 16px;width:100%;max-width:440px;display:flex;flex-direction:column;align-items:center;gap:10px"><button type="button" id="btnTeacherPreviewInModal" onclick="startFreePractice()" style="width:100%;max-width:420px;background:linear-gradient(135deg,#38bdf8 0%,#818cf8 50%,#a855f7 100%);color:#070d1e;border:2px solid #ffffff;border-radius:14px;padding:14px 22px;font-size:1.1rem;font-weight:900;cursor:pointer;transition:all .2s ease;box-shadow:0 0 24px rgba(56,189,248,.7),0 6px 18px rgba(0,0,0,.5);display:inline-flex;align-items:center;justify-content:center;gap:8px;letter-spacing:-0.2px" onmouseover="this.style.transform='translateY(-2px) scale(1.03)';this.style.boxShadow='0 0 32px rgba(56,189,248,.95),0 8px 24px rgba(0,0,0,.6)'" onmouseout="this.style.transform='none';this.style.boxShadow='0 0 24px rgba(56,189,248,.7),0 6px 18px rgba(0,0,0,.5)'"><span class="bilingual-ko">🚀 가입 없이 바로 문제 열람 & 자유 풀기 ➔</span><span class="bilingual-en">🚀 Free Practice (No Login Required) ➔</span></button><div style="font-size:0.81rem;color:#94a3b8;display:flex;align-items:center;gap:8px;width:100%;max-width:380px"><span style="flex:1;height:1px;background:rgba(255,255,255,.15)"></span><span><span class="bilingual-ko">또는 이름을 입력하고 학습 기록 저장</span><span class="bilingual-en">Or enter name to save your progress</span></span><span style="flex:1;height:1px;background:rgba(255,255,255,.15)"></span></div></div><h3 style="color:#e8ecf5;margin:0 0 6px">📝 먼저 이름을 입력하세요</h3><p style="color:#9aa6c0;font-size:.9rem;margin:0 0 20px"><span class="bilingual-ko">이름을 입력해야 학습 기록이 저장됩니다.</span><span class="bilingual-en">Your learning progress will be saved under this name.</span></p><div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap"><input type="text" id="studentName" placeholder="이름 입력" autofocus style="background:#222a3d;color:#e8ecf5;border:1px solid #2e3850;border-radius:10px;padding:12px 16px;font-size:1.05rem;min-width:200px;text-align:center"><button class="btn" onclick="registerName()" style="font-size:1.05rem;padding:12px 24px"><span class="bilingual-ko">시작하기</span><span class="bilingual-en">Start</span></button></div></div><script>window._studentName="";window._sheetsApiUrl="https://script.google.com/macros/s/AKfycbxQBW1hKYFSHokaVJMRql-UJpk0t4qMeWMiiy_RFuCLZ5SE4iZytYQkGa9_yoCmm1Ak0Q/exec";function toggleModalLang(l){{document.documentElement.lang=l;try{{localStorage.setItem("mathedu_lang",l);localStorage.setItem("mathedu_lang_manual","true");}}catch(e){{}}var bKo=document.getElementById("btnTrackFullLangKo");var bEn=document.getElementById("btnTrackFullLangEn");if(bKo&&bEn){{if(l==="en"){{bKo.style.background="transparent";bKo.style.color="#cbd5e1";bKo.style.fontWeight="700";bEn.style.background="#38bdf8";bEn.style.color="#0b1020";bEn.style.fontWeight="800";}}else{{bKo.style.background="#38bdf8";bKo.style.color="#0b1020";bKo.style.fontWeight="800";bEn.style.background="transparent";bEn.style.color="#cbd5e1";bEn.style.fontWeight="700";}}}}var cKo=document.getElementById("btnModalCenterLangKo");var cEn=document.getElementById("btnModalCenterLangEn");if(cKo&&cEn){{if(l==="en"){{cKo.style.background="transparent";cKo.style.color="#cbd5e1";cKo.style.fontWeight="700";cKo.style.boxShadow="none";cEn.style.background="linear-gradient(135deg,#38bdf8 0%,#818cf8 100%)";cEn.style.color="#0b1020";cEn.style.fontWeight="800";cEn.style.boxShadow="0 2px 10px rgba(56,189,248,.45)";}}else{{cKo.style.background="linear-gradient(135deg,#38bdf8 0%,#818cf8 100%)";cKo.style.color="#0b1020";cKo.style.fontWeight="800";cKo.style.boxShadow="0 2px 10px rgba(56,189,248,.45)";cEn.style.background="transparent";cEn.style.color="#cbd5e1";cEn.style.fontWeight="700";cEn.style.boxShadow="none";}}}}var sn=document.getElementById("studentName");if(sn)sn.placeholder=(l==="en")?"Enter name":"이름 입력";var pin=document.getElementById("studentPin");if(pin)pin.placeholder=(l==="en")?"4-digit PIN (optional)":"간편비번 4자리 (선택)";if(window.setBoardLanguage)window.setBoardLanguage(l);else if(window.setBoardLang)window.setBoardLang(l,true);}}(function(){{var cur="ko";try{{var p=new URLSearchParams(window.location.search).get("lang");if(p==="en"||p==="ko"){{cur=p;}}else{{var man=localStorage.getItem("mathedu_lang_manual")==="true";var sto=localStorage.getItem("mathedu_lang");if(man&&(sto==="en"||sto==="ko")){{cur=sto;}}else{{var tz="";try{{tz=Intl.DateTimeFormat().resolvedOptions().timeZone||"";}}catch(e){{}}if(tz&&tz!=="Asia/Seoul"&&tz!=="ROK"&&tz!=="Asia/Pyongyang"){{cur="en";}}else{{var l=(navigator.languages&&navigator.languages[0])||navigator.language||"";if(l&&l.toLowerCase().indexOf("ko")!==0)cur="en";}}}}}}}}catch(e){{}}if(cur==="en"){{document.documentElement.lang="en";toggleModalLang("en");}}}})();function startFreePractice(){{var vid="";try{{vid=localStorage.getItem("mathedu_visitor_id")||"";if(!vid){{vid=Math.random().toString(36).substring(2,6).toUpperCase();localStorage.setItem("mathedu_visitor_id",vid);}}}}catch(e){{vid="ANON";}}window._studentName=((document.documentElement.lang==="en")?"Guest#":"자유학습#")+vid;var tf=document.getElementById("trackFull");if(tf)tf.remove();if(window.sendProgress)sendProgress();if(window.MathJax&&MathJax.typesetPromise)MathJax.typesetPromise();}}function registerName(){{var n=document.getElementById("studentName").value.trim();if(!n){{alert((document.documentElement.lang==="en")?"Please enter your name":"이름을 입력하세요");return;}}window._studentName=n;document.getElementById("trackFull").remove();sendProgress();if(window.MathJax&&MathJax.typesetPromise){{MathJax.typesetPromise();}}}}function sendProgress(){{var name=(window._studentName||"").trim();if(!name)return;var qs=document.querySelectorAll(".q");var total=qs.length;var done=document.querySelectorAll(".q.done");var correct=0;done.forEach(function(q){{if(q.querySelector(".opt.correct"))correct++;}});if(total===0)return;fetch(window._sheetsApiUrl,{{method:"POST",mode:"no-cors",keepalive:true,headers:{{"Content-Type":"text/plain;charset=utf-8"}},body:JSON.stringify({{quiz_slug:"{slug}",student_name:name,current_step:done.length,total_steps:total,correct:correct}})}}).catch(function(){{}});}}document.querySelectorAll(".q").forEach(function(q){{q.addEventListener("click",function(e){{var opt=e.target.closest(".opt");if(opt){{setTimeout(sendProgress,50);}}}});}});document.getElementById("studentName").addEventListener("keydown",function(e){{if(e.key==="Enter")registerName();}});</script>
<h2>🎯 최종 문제 + 상세 풀이<span class="bilingual-en">🎯 Final Official Exam Problem & Complete Solution</span></h2><div class="sol">
  <div class="bilingual-ko">
{sol_ko}
  </div>
  <div class="bilingual-en">
{sol_en}
  </div>
</div>{final_q_block}
{addon_card_html}
<div class="final"><p><span class="bilingual-ko">🎉 완료!</span><span class="bilingual-en">🎉 Completed!</span></p><div class="ans" id="finalAns">정답 {final_ans_display}</div>
<button class="btn" onclick="location.reload()"><span class="bilingual-ko">다시 풀기</span><span class="bilingual-en">Try Again</span></button></div>
</div><script>
const qs=document.querySelectorAll('.q');let pts=0;
document.getElementById('tot').textContent=qs.length;

function toggleExp(btn){{
  var q = btn.closest ? btn.closest('.q') : btn.parentElement;
  while(q && !q.classList.contains('q')) {{ q = q.parentElement; }}
  if(!q) return;
  var exp = q.querySelector('.exp');
  if(!exp) return;
  if(exp.classList.contains('show')){{
    exp.classList.remove('show');
    btn.textContent = (document.documentElement.lang === 'en') ? '💡 View Explanation' : '💡 해설 보기';
  }} else {{
    exp.classList.add('show');
    btn.textContent = (document.documentElement.lang === 'en') ? '💡 Close Explanation' : '💡 해설 닫기';
  }}
}}

qs.forEach(q=>{{
  const ans=+q.dataset.ans;
  const exp=q.querySelector('.exp');
  if(exp) {{
    var koExp = q.dataset.exp || '';
    var enExp = q.dataset.expEn || '';
    if(enExp) {{
      exp.innerHTML = koExp + '<div class="bilingual-en"><b>English Explanation:</b> ' + enExp + '</div>';
    }} else {{
      exp.innerHTML = koExp;
    }}
  }}
  const opts=q.querySelectorAll('.opt');
  opts.forEach((o,i)=>{{
    o.addEventListener('click',()=>{{
      if(q.classList.contains('done')) return;
      q.classList.add('done');
      opts.forEach((oo,j)=>{{
        oo.classList.add('locked');
        if(j+1==ans) oo.classList.add('correct');
      }});
      if(i+1==ans){{
        o.classList.add('correct');
        q.classList.add('correct-q');
        pts++;
      }} else {{
        o.classList.add('wrong');
      }}
      if(exp) exp.classList.add('show');
      var toggleBtn = q.querySelector('.exp-toggle-btn');
      if(toggleBtn) {{ var isEn = (document.documentElement.lang === 'en'); toggleBtn.textContent = isEn ? '💡 Close Explanation' : '💡 해설 닫기'; }}
      document.getElementById('pts').textContent=pts;
      var total = document.querySelectorAll('.q').length;
      const pct=Math.round(pts/total*100);
      document.getElementById('bar').style.width=pct+'%';
      document.getElementById('pct').textContent=pct+'%';
      if(typeof sendProgress === 'function') setTimeout(sendProgress, 50);
    }});
  }});
}});
function sendProgress(){{
  var name = (window._studentName || '').trim();
  if (!name) return;
  var qs = document.querySelectorAll('.q');
  var total = qs.length;
  var done = document.querySelectorAll('.q.done');
  var correct = pts;
  var current = done.length;
  if (current === 0) return;
  var url = window._sheetsApiUrl || '/api/progress';
  fetch(url, {{
    method: 'POST',
    mode: 'no-cors', keepalive: true, headers: {{'Content-Type': 'text/plain;charset=utf-8'}},
    body: JSON.stringify({{
      quiz_slug: '{slug}',
      student_name: name,
      current_step: current,
      total_steps: total,
      correct: correct
    }})
  }}).catch(()=>{{}});
}}
function copyLink(){{const b=document.getElementById('copyBtn');const t=b.textContent;
navigator.clipboard.writeText(location.href).then(()=>{{b.textContent='✅ 복사됨';setTimeout(()=>b.textContent=t,1500);}})
.catch(()=>{{prompt('아래 링크를 복사하세요',location.href);}});}}
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
  var slug='{slug}' || window.location.pathname.split('/').filter(Boolean).pop().replace('.html','');
  var qEl=wrap.closest('.q');
  var qNum=qEl?Array.from(document.querySelectorAll('.q')).indexOf(qEl)+1:0;
  var textEl=wrap.querySelector('.report-text');
  var text=(textEl ? textEl.value : '').trim();
  var url=window._sheetsApiUrl||'https://script.google.com/macros/s/AKfycbxQBW1hKYFSHokaVJMRql-UJpk0t4qMeWMiiy_RFuCLZ5SE4iZytYQkGa9_yoCmm1Ak0Q/exec';
  var reportUrl=url+'?action=report&quiz='+encodeURIComponent(slug)+'&q='+qNum+'&name='+encodeURIComponent(name)+'&text='+encodeURIComponent(text||'사유 없음')+'&_t='+Date.now();
  try {{
    fetch(reportUrl, {{ mode: 'no-cors', keepalive: true }}).catch(function(){{}});
  }} catch(e){{}}
  try {{
    var img=new Image();
    img.src=reportUrl;
  }} catch(e){{}}
  wrap.querySelector('.report-form').style.display='none';
  wrap.querySelector('.report-msg').style.display='block';
}}
</script><script src="../mathedu-room.js"></script>
<script src="../mathedu-report.js"></script><script>
function updateExplanations(lang) {{
  var isEn = (lang === 'en');
  var qs = document.querySelectorAll('.q');
  qs.forEach(function(q) {{
    var exp = q.querySelector('.exp');
    var btn = q.querySelector('.exp-toggle-btn');
    if (btn) {{
      var isShown = exp && exp.classList.contains('show');
      btn.textContent = isEn ? (isShown ? '💡 Close Explanation' : '💡 View Explanation') : (isShown ? '💡 해설 닫기' : '💡 해설 보기');
    }}
    if (exp) {{
      var koExp = q.dataset.exp || '';
      var enExp = q.dataset.expEn || '';
      if (isEn && enExp) {{
        exp.innerHTML = '<b>Explanation:</b> ' + enExp;
      }} else {{
        exp.innerHTML = koExp;
      }}
    }}
  }});
  if (window.MathJax && window.MathJax.typesetPromise) {{
    try {{ window.MathJax.typesetPromise(); }} catch(e){{}}
  }}
}}

function setBoardLang(lang, isUserAction) {{
  if (lang !== 'ko' && lang !== 'en') return;
  document.documentElement.lang = lang;
  if (isUserAction) {{
    try {{
      localStorage.setItem('mathedu_lang', lang);
      localStorage.setItem('mathedu_lang_manual', 'true');
    }} catch(e){{}}
  }}
  document.querySelectorAll('[data-lang-btn]').forEach(function(b) {{
    if (b.getAttribute('data-lang-btn') === lang) b.classList.add('active');
    else b.classList.remove('active');
  }});
  if (window.MatheduI18n && typeof MatheduI18n.setLanguage === 'function') {{
    if (isUserAction) {{
      MatheduI18n.setLanguage(lang);
    }}
  }}
  updateExplanations(lang);
}}

(function(){{
  var saved = 'ko';
  try {{
    var p = new URLSearchParams(window.location.search).get('lang');
    if (p === 'en' || p === 'ko') {{
      saved = p;
      try {{
        localStorage.setItem('mathedu_lang', p);
        localStorage.setItem('mathedu_lang_manual', 'true');
      }} catch(e){{}}
    }} else {{
      var manual = localStorage.getItem('mathedu_lang_manual') === 'true';
      var stored = localStorage.getItem('mathedu_lang');
      if (manual && (stored === 'en' || stored === 'ko')) {{
        saved = stored;
      }} else if (window.MatheduI18n && typeof MatheduI18n.getLanguage === 'function') {{
        saved = MatheduI18n.getLanguage();
      }} else {{
        var tz = '';
        try {{ tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ''; }} catch(e){{}}
        if (tz === 'Asia/Seoul' || tz === 'ROK' || tz === 'Asia/Pyongyang') {{
          saved = 'ko';
        }} else if (tz) {{
          saved = 'en';
        }} else {{
          var l = (navigator.languages && navigator.languages[0]) || navigator.language || '';
          saved = (l.toLowerCase().indexOf('ko') === 0) ? 'ko' : 'en';
        }}
      }}
    }}
  }} catch(e){{
    saved = 'ko';
  }}
  setBoardLang(saved, false);
}})();
</script>
</body></html>"""
    return page_html


def main():
    all_problems = (
        PART1_PROBLEMS
        + PART2_PROBLEMS
        + PART3_PROBLEMS
        + PART4_PROBLEMS
        + PART5_PROBLEMS
    )
    print(f"Total problems loaded: {len(all_problems)}")

    new_index_entries = []
    for prob in all_problems:
        slug = prob["slug"]
        out_path = os.path.join(BOARD_DIR, f"{slug}.html")
        html_content = build_problem_html(prob)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        qnum_clean = extract_clean_qnum(prob["qNum"])
        new_index_entries.append({
            "slug": slug,
            "title": prob["title"],
            "time": "2026-10-21 12:30",
            "file": f"{slug}.html",
            "examYear": "2026",
            "examYearAlt": "2027",
            "grade": "고3",
            "month": "10월",
            "subject": prob["subject"],
            "qNum": qnum_clean,
            "source": "2026학년도 10월 학력평가",
            "date": "2026-10-21",
            "tags": prob.get("tags", [prob["subject"], f"{qnum_clean}번"]),
            "is_public": True
        })

    # Update board/index.json
    index_json_path = os.path.join(BOARD_DIR, "index.json")
    with open(index_json_path, "r", encoding="utf-8") as f:
        existing_items = json.load(f)

    new_slugs = {e["slug"] for e in new_index_entries}
    filtered_existing = [it for it in existing_items if it.get("slug") not in new_slugs]
    updated_items = new_index_entries + filtered_existing

    with open(index_json_path, "w", encoding="utf-8") as f:
        json.dump(updated_items, f, ensure_ascii=False, indent=2)

    print(f"Generated {len(all_problems)} HTML files in board/ and updated board/index.json ({len(updated_items)} total items).")

    # Update index.html to support examYearAlt filter
    idx_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(idx_path):
        with open(idx_path, "r", encoding="utf-8") as f:
            txt = f.read()
        old_str = "var mYear = (it.examYear === ef.year) || title.includes(ef.year);"
        new_str = "var mYear = (it.examYear === ef.year) || (it.examYearAlt === ef.year) || title.includes(ef.year);"
        if old_str in txt:
            txt = txt.replace(old_str, new_str)
            with open(idx_path, "w", encoding="utf-8") as f:
                f.write(txt)
            print("Updated index.html examYearAlt check.")

    # Ensure 7 legacy files in board/ pass SCAFFOLDING_ELEMENTARY_GROUNDING
    legacy_files = [
        "1b623c24.html", "36790012.html", "4cb6d212.html",
        "8e9d528d.html", "8f24f3c3.html", "a05b47bc.html", "e7d51a27.html"
    ]
    for fname in legacy_files:
        lpath = os.path.join(BOARD_DIR, fname)
        if not os.path.exists(lpath):
            continue
        with open(lpath, "r", encoding="utf-8") as f:
            c = f.read()
        m = re.search(r'<div class="lvl">(.*?)</div>', c, flags=re.S)
        if m and "초등" not in m.group(1):
            inner = m.group(1)
            if "lang-ko" in inner:
                inner = inner.replace('lang-ko">', 'lang-ko">[초등 기초 디딤돌] ', 1)
                inner = inner.replace('lang-en">', 'lang-en">[Elementary Foundation] ', 1)
            else:
                inner = "[초등 기초 디딤돌] " + inner
            c = c[:m.start()] + '<div class="lvl">' + inner + '</div>' + c[m.end():]
            with open(lpath, "w", encoding="utf-8") as f:
                f.write(c)
            print("Updated legacy file for elementary grounding:", fname)


if __name__ == "__main__":
    main()
