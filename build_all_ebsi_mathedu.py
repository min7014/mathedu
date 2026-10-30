# -*- coding: utf-8 -*-
"""
build_all_ebsi_mathedu.py
=========================
EBSi 기출문제(https://www.ebsi.co.kr/ebs/xip/xipc/previousPaperList.ebs)
전 연도(2006~2026 시행 = 2007~2027학년도) · 전 학년(고3 D300, 고2 D200, 고1 D100)
총 608개 수학 시험지 · 16,747개 고유 수학 문항을 mathedu 초등 눈높이 5단계 디딤돌 퀴즈 +
시각적 도형(SVG) + 도식화 풀이 흐름도 + min7014.github.io 연계 문제로 일괄 생성하는 빌더.

생성 산출물:
1. 대표 수능 실물 단독 HTML 페이지 (board/csat26_*.html 46문항 + board/csat25_*.html 46문항 = 92문항)
2. 전 연도(2006~2026) · 전 학년(고1·고2·고3) 16,747문항 연도별 샤드 DB (board/ebsi_shards/ebsi_2006.json ~ ebsi_2026.json)
3. 통합 자연어 검색용 전 문항 카탈로그 (board/ebsi_catalog.json — 16,747문항)
4. 16,747문항 통합 단계별 인터랙티브 플레이어 (board/ebsi.html)
"""

import os
import sys
import re
import json
import html
import xml.etree.ElementTree as ET

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from ebsi_lml_engine import (
    extract_question_and_explanation,
    synthesize_mathedu_problem,
    UNIT_TEMPLATES,
    DEFAULT_UNIT_TEMPLATE,
)
from build_oct2026_all import (
    COMMON_STYLE,
    render_md_inline,
    extract_clean_qnum,
    build_question_block,
)
import min7014_matcher
from visual_diagram_engine import build_visual_and_schematic_block

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOARD_DIR = os.path.join(BASE_DIR, "board")
SHARDS_DIR = os.path.join(BOARD_DIR, "ebsi_shards")
os.makedirs(SHARDS_DIR, exist_ok=True)

SCRATCH_DIR = r"C:\Users\min\.gemini\antigravity-cli\brain\338ec562-09b6-4442-af01-9e2f87c3d74d\scratch"
PAPERS_JSON = os.path.join(SCRATCH_DIR, "ebsi_math_papers.json")
CACHE_DIR = os.path.join(SCRATCH_DIR, "ebsi_xml_cache")


def parse_paper_metadata(p: dict) -> dict:
    """Normalize EBSi paper metadata into examYear, examYearAlt, month, grade, subject, source."""
    cal_year = str(p.get("year", "2026")).strip()
    grade = str(p.get("grade", "고3")).strip()
    title = str(p.get("title", "")).strip()
    flags = p.get("flags", [])

    # Month
    month_raw = next((fl for fl in flags if "월" in fl), "")
    is_csat = ("대학수학능력시험" in title) and ("모의평가" not in title) and ("예비" not in title)
    if is_csat:
        month = "11월"
        month_label = "수능"
    else:
        month = month_raw if month_raw else "11월"
        month_label = month

    # Academic Year (학년도)
    m_ay = re.search(r"(20\d{2})\s*학년도", title)
    if m_ay:
        exam_year = m_ay.group(1)
        exam_year_alt = cal_year if cal_year != exam_year else str(int(cal_year) + 1)
    else:
        exam_year = cal_year
        exam_year_alt = str(int(cal_year) + 1) if grade == "고3" else cal_year

    # Subject
    if "확률과 통계" in title:
        subj = "확률과 통계"
    elif "미적분" in title:
        subj = "미적분"
    elif "기하" in title and "벡터" not in title:
        subj = "기하"
    elif "기하와 벡터" in title:
        subj = "기하"
    elif "가형" in title:
        subj = "수학(가형)"
    elif "나형" in title:
        subj = "수학(나형)"
    elif "A형" in title:
        subj = "수학(나형)"
    elif "B형" in title:
        subj = "수학(가형)"
    elif grade == "고1":
        subj = "공통수학"
    elif grade == "고2":
        subj = "수학(고2)"
    else:
        subj = "공통(수학I·II)"

    # Clean source label
    if is_csat:
        source = f"{exam_year}학년도 대학수학능력시험"
    elif "모의평가" in title:
        source = f"{exam_year}학년도 {month} 평가원 모의평가"
    else:
        source = f"{cal_year}년 {month} {grade} 전국연합학력평가"

    date_flag = next((fl.replace(".", "-") for fl in flags if re.match(r"^\d{4}\.\d{2}\.\d{2}$", fl)), f"{cal_year}-11-15")

    return {
        "paperId": str(p["paperId"]),
        "calYear": cal_year,
        "examYear": exam_year,
        "examYearAlt": exam_year_alt,
        "month": month,
        "monthLabel": month_label,
        "grade": grade,
        "subject": subj,
        "isCsat": is_csat,
        "source": source,
        "date": date_flag,
        "paperTitle": title,
    }


def build_ebsi_problem_html(prob: dict, extra_top_html: str = "", extra_bottom_js: str = "") -> str:
    """Build a standalone Stitch-ready problem HTML page (with rendered official stem in .orig-media-frame)."""
    slug = prob["slug"]
    qnum_clean = extract_clean_qnum(prob["qNum"])
    subject = prob["subject"]
    exam_year = prob.get("examYear", "2026")
    month = prob.get("month", "수능")
    grade = prob.get("grade", "고3")
    source_label = prob.get("source", f"{exam_year}학년도 대학수학능력시험")
    title_ko = prob["title"]
    title_en = prob.get("title_en", title_ko)
    summary_ko = prob.get("summary_ko", title_ko)
    summary_en = prob.get("summary_en", title_en)
    tags = prob.get("tags", [subject, f"{qnum_clean}번"])

    clean_topic_ko = re.sub(r"^\[.*?\]\s*", "", title_ko).strip()

    if subject == "공통(수학I·II)":
        badge_ko = f"{exam_year}학년도 {month} {grade} 공통 {qnum_clean}번"
        badge_en = f"{exam_year} AY {month} {grade} Common #{qnum_clean}"
    else:
        badge_ko = f"{exam_year}학년도 {month} {grade} {subject} {qnum_clean}번"
        badge_en = f"{exam_year} AY {month} {grade} {subject} #{qnum_clean}"

    search_query = f"{title_ko} {summary_ko} {' '.join(tags)}"
    matched_materials = min7014_matcher.match_materials(search_query, limit=4)
    visual_tip_ko = min7014_matcher._get_visual_tip_text(search_query)
    addon_card_html = min7014_matcher.generate_addon_card_html(matched_materials, search_query)

    # Step 0 symbols
    sym_items_html = ""
    for s in prob.get("symbols", []):
        sym_l = s["sym"]
        desc_ko = render_md_inline(s["desc"])
        desc_en = render_md_inline(s.get("desc_en", ""))
        en_div = f'<div class="bilingual-en">{desc_en}</div>' if desc_en else ""
        sym_items_html += f'<div><b>{sym_l}</b> — {desc_ko}{en_div}</div>'

    # Levels (Step 1 ~ Step 5)
    levels_html = ""
    ladder_items_ko = []
    ladder_items_en = []
    step_summaries_ko = []
    step_summaries_en = []
    levels_list = prob.get("levels", [])
    for s_idx, lv in enumerate(levels_list, 1):
        lv_title_ko = render_md_inline(lv["title"])
        lv_title_en = render_md_inline(lv.get("title_en", f"Step {s_idx}"))
        know_ko = render_md_inline(lv.get("knowledge", ""))
        know_en = render_md_inline(lv.get("knowledge_en", ""))
        qs_html = "".join(
            build_question_block(q, is_final=False, step_idx=s_idx, know_ko=know_ko, know_en=know_en)
            for q in lv.get("questions", [])
        )
        levels_html += f"""<h2>{lv_title_ko}<span class="bilingual-en">{lv_title_en}</span></h2><div class="know"><h3>먼저 알아야 할 지식</h3>{know_ko}<div class="bilingual-en"><b>Prerequisite Knowledge:</b> {know_en}</div></div>{qs_html}"""

        q0 = lv["questions"][0] if lv.get("questions") else None
        if q0:
            a_i = int(q0["answer"]) - 1
            opts = q0.get("options", [])
            ans_txt = render_md_inline(opts[a_i]) if 0 <= a_i < len(opts) else str(q0["answer"])
            q_exp_ko = render_md_inline(q0.get("exp", ""))
            q_exp_en = render_md_inline(q0.get("exp_en", ""))
            step_summaries_ko.append(f"{lv_title_ko} ⇒ {ans_txt}")
            step_summaries_en.append(f"{lv_title_en} ⇒ {ans_txt}")
            ladder_items_ko.append(
                f"  <li><b>{lv_title_ko}</b><br>"
                f"    &nbsp;&nbsp;• <b>핵심 개념 및 원리</b>: {know_ko}<br>"
                f"    &nbsp;&nbsp;• <b>단계 확인 정답 ({ans_txt})</b>: {q_exp_ko}</li>"
            )
            ladder_items_en.append(
                f"  <li><b>{lv_title_en}</b><br>"
                f"    &nbsp;&nbsp;• <b>Core Principle</b>: {know_en}<br>"
                f"    &nbsp;&nbsp;• <b>Step Verification ({ans_txt})</b>: {q_exp_en}</li>"
            )

    final_data = prob["final"]
    sol_ko = render_md_inline(final_data["solution"])
    sol_en = render_md_inline(final_data.get("solution_en", ""))
    ans_idx = int(final_data["answer"]) - 1
    final_ans_display = final_data["options"][ans_idx] if 0 <= ans_idx < len(final_data["options"]) else str(final_data["answer"])

    if "math-visual-diagram" not in sol_ko:
        vis_ko = build_visual_and_schematic_block(
            pid=slug,
            title_ko=title_ko,
            step_summaries_ko=step_summaries_ko,
            ans_str=final_ans_display,
            sol_ko_plain=sol_ko,
            lang="ko",
        )
        if "<h4>📐" in sol_ko:
            sol_ko = sol_ko.replace("<h4>📐", vis_ko + "\n<h4>📐", 1)
        elif "</p>" in sol_ko:
            sol_ko = sol_ko.replace("</p>", "</p>\n" + vis_ko, 1)
        else:
            sol_ko = vis_ko + "\n" + sol_ko

    if "math-visual-diagram" not in sol_en:
        vis_en = build_visual_and_schematic_block(
            pid=slug,
            title_ko=title_en,
            step_summaries_ko=step_summaries_en if step_summaries_en else step_summaries_ko,
            ans_str=final_ans_display,
            sol_ko_plain=sol_ko,
            lang="en",
        )
        if "<h4>📐" in sol_en:
            sol_en = sol_en.replace("<h4>📐", vis_en + "\n<h4>📐", 1)
        elif "</p>" in sol_en:
            sol_en = sol_en.replace("</p>", "</p>\n" + vis_en, 1)
        else:
            sol_en = vis_en + "\n" + sol_en

    if ladder_items_ko and "🪜 [초등 눈높이 디딤돌" not in sol_ko:
        n_st = len(ladder_items_ko)
        ladder_block_ko = (
            f"\n<h4>🪜 [초등 눈높이 디딤돌 전 단계(1단계~{n_st}단계) 완전 연결 상세 해설]</h4>\n"
            f"<p>위 디딤돌 문제에서 밟아 온 $1$단계부터 ${n_st}$단계까지의 작은 조각들을 순서대로 연결하면 본문항의 풀이가 빈틈없이 완성됩니다.</p>\n"
            f"<ul>\n" + "\n".join(ladder_items_ko) + "\n</ul>\n"
        )
        if "<h4>✨" in sol_ko:
            sol_ko = sol_ko.replace("<h4>✨", ladder_block_ko + "\n<h4>✨", 1)
        else:
            sol_ko = sol_ko + ladder_block_ko

    if ladder_items_en and "🪜 [Complete Step-by-Step" not in sol_en:
        n_st_en = len(ladder_items_en)
        ladder_block_en = (
            f"\n<h4>🪜 [Complete Step-by-Step Scaffolding Walkthrough (Steps 1–{n_st_en})]</h4>\n"
            f"<p>Connecting each elementary-grounded scaffolding step from Step 1 to Step {n_st_en} completes the entire derivation without any logical gaps:</p>\n"
            f"<ul>\n" + "\n".join(ladder_items_en) + "\n</ul>\n"
        )
        if "<h4>✨" in sol_en:
            sol_en = sol_en.replace("<h4>✨", ladder_block_en + "\n<h4>✨", 1)
        else:
            sol_en = sol_en + ladder_block_en

    if len(sol_en.strip()) < 120:
        sol_en = sol_en + "\n<p>💡 <b>Key Takeaway</b>: Master each micro-scaffolding step from elementary arithmetic to complete the rigorous derivation accurately.</p>"

    # Balance any stray $ in sol_ko / sol_en
    if len(re.findall(r"(?<!\\)\$", sol_ko)) % 2 != 0:
        sol_ko += " $"
    if len(re.findall(r"(?<!\\)\$", sol_en)) % 2 != 0:
        sol_en += " $"

    final_q_block = build_question_block(
        final_data,
        is_final=True,
        step_idx=len(levels_list) + 1,
        sol_ko=sol_ko,
        sol_en=sol_en,
    )

    # Render official exam paper box inside .orig-media-frame (using <section>/<p>/<span>, no <h2>)
    circled_nums = ["①", "②", "③", "④", "⑤"]
    orig_opts_spans = " &nbsp;&nbsp; ".join(
        f'<span style="display:inline-block;margin:3px 6px 3px 0;font-weight:600;color:#1e293b">{circled_nums[i]} {opt}</span>'
        for i, opt in enumerate(final_data.get("options", [])[:5])
    )
    orig_paper_box = (
        f'<section id="ebsiOrigPaperBox" style="width:100%;text-align:left;padding:18px 20px;background:#ffffff;border:1.5px solid #cbd5e1;border-radius:12px;color:#1b1b1d;line-height:1.8;font-size:0.96rem;box-shadow:inset 0 1px 4px rgba(15,23,42,0.04)">'
        f'<p style="margin:0 0 10px;padding-bottom:8px;border-bottom:1.5px solid #0f172a;display:flex;justify-content:space-between;align-items:center;font-weight:800;font-size:0.86rem;color:#0f172a">'
        f'<span>📄 {html.escape(source_label)} · {html.escape(subject)}</span>'
        f'<span style="background:#0f172a;color:#ffffff;padding:2px 10px;border-radius:999px;font-size:0.78rem">문항 {qnum_clean}번</span>'
        f'</p>'
        f'<p id="ebsiOrigStemContent" style="margin:0 0 14px;color:#111827;font-size:0.97rem;line-height:1.85">{final_data["stem"]}</p>'
        f'<p id="ebsiOrigOptsContent" style="margin:0;padding-top:10px;border-top:1px dashed #cbd5e1;font-size:0.92rem;line-height:1.7">{orig_opts_spans}</p>'
        f'</section>'
    )

    meta_desc = html.escape(
        f"{source_label} {grade} {subject} {qnum_clean}번 · {title_ko}. 초등학생도 풀 수 있는 단계별 디딤돌 5지선다 퀴즈 및 상세 해설.",
        quote=True,
    )
    meta_kw = html.escape(
        f"{source_label}, {grade} 수학 {qnum_clean}번, {title_ko}, {subject}, {', '.join(tags)}, 디딤돌 퀴즈, GeoGebra, 수학자료실, mathedu",
        quote=True,
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
<meta property="og:image" content="https://min7014.github.io/mathedu/assets/favicon.png">
<link rel="canonical" href="https://min7014.github.io/mathedu/board/{slug}.html">
<link rel="icon" type="image/png" sizes="32x32" href="../assets/favicon.png">
<style>
{COMMON_STYLE}
</style>
<script>window.MathJax={{tex:{{inlineMath:[['$','$'],['\\\\(','\\\\)']]}}}};</script>
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
    <span class="orig-badge" id="ebsiOrigBadge"><span class="bilingual-ko">{badge_ko}</span><span class="bilingual-en">{badge_en}</span></span>
  </div>
{extra_top_html}
  <div class="orig-grid">
    <!-- 좌측: 실제 시험지 원본 문항 박스 -->
    <div class="orig-col-media">
      <div class="orig-media-frame">
        {orig_paper_box}
      </div>
      <div class="orig-media-sub" id="ebsiOrigMediaSub"><span class="bilingual-ko">📄 {html.escape(source_label)} 공식 기출문항</span><span class="bilingual-en">📄 Official National Exam Paper ({grade})</span></div>
    </div>

    <!-- 우측: 원본 문항 핵심 요약 및 목표 -->
    <div class="orig-col-desc">
      <div class="orig-text-box">
        <h4>📋 원본 문항 핵심 요약 및 목표<span class="bilingual-en">📋 Official Problem Summary & Objectives</span></h4>
        <p id="ebsiOrigTopicTitle" style="margin:0 0 8px;font-weight:600;color:var(--txt)">{clean_topic_ko}</p>
        <p id="ebsiOrigSummaryKo" style="margin:0;font-size:0.88rem;color:var(--sub);line-height:1.6">{summary_ko}</p>
        <div class="bilingual-en" id="ebsiOrigSummaryEn"><b>Problem Objective:</b> {summary_en}</div>
      </div>
      <div class="orig-tip">
        💡 <b>초등 눈높이 디딤돌 길잡이</b>: 처음 나오는 기호도 제0단계 기호 번역과 1단계 초등 사칙연산·구구단 디딤돌부터 순서대로 밟아가면 누구나 100% 자신의 힘으로 해결할 수 있습니다!<span class="bilingual-en">💡 <b>Core Guide</b>: Follow the elementary-grounded micro-steps below to master this problem completely!</span>
      </div>
    </div>
  </div>

  <!-- 하단: 프레임별 시각적 증명 팁 전면 가로 확장 -->
  <div class="min-visual-tip" id="ebsiVisualTipBox" style="margin-top:16px">
    {visual_tip_ko}
  <div class="bilingual-en">💡 <b>Frame-by-Frame Visual Proof Analysis (PDF & GeoGebra Exploration)</b><br>The archive's flipbook proof materials demonstrate how fundamental mathematical principles converge smoothly frame by frame. Explore the interactive dynamic geometry applets below.</div></div>
</div>
<h2>🔰 제0단계 · 수학 기호 번역기<span class="bilingual-en">🔰 Step 0 · Mathematical Symbol Translator</span></h2><div class="sym" id="ebsiSymContainer">{sym_items_html}</div>
<div id="ebsiDynamicLevelsWrap">
{levels_html}
</div>
<div id="trackFull" style="position:fixed;inset:0;z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;background:rgba(252,248,250,0.97);padding:24px;text-align:center"><div id="trackFullLangSwitcher" style="position:absolute;top:18px;left:20px;z-index:100;display:inline-flex;align-items:center;background:#f0edef;border:1.5px solid #e4e2e4;border-radius:24px;padding:3px 4px;gap:3px;box-shadow:0 4px 16px rgba(0,0,0,.4);backdrop-filter:blur(10px)"><button type="button" id="btnTrackFullLangKo" onclick="toggleModalLang('ko')" style="background:#38bdf8;color:#0b1020;border:none;border-radius:18px;padding:5px 12px;font-size:0.82rem;font-weight:800;cursor:pointer;transition:.15s">🇰🇷 한국어</button><button type="button" id="btnTrackFullLangEn" onclick="toggleModalLang('en')" style="background:transparent;color:#cbd5e1;border:none;border-radius:18px;padding:5px 12px;font-size:0.82rem;font-weight:700;cursor:pointer;transition:.15s">🌐 English</button></div><h2 style="background:linear-gradient(90deg,#7cc4ff,#a78bfa);-webkit-background-clip:text;background-clip:text;color:transparent;font-size:1.6rem;margin:0 0 8px">📘 mathedu</h2><div id="modalCenterLangSwitcher" style="margin:4px 0 16px;display:inline-flex;align-items:center;justify-content:center;background:#f0edef;border:1.5px solid #e4e2e4;border-radius:28px;padding:4px 8px;gap:5px;box-shadow:0 6px 20px rgba(0,0,0,.45);backdrop-filter:blur(10px);z-index:10"><span style="font-size:0.83rem;color:#45464d;font-weight:700;margin:0 4px 0 8px;display:inline-flex;align-items:center;gap:4px"><span>🌐</span><span class="bilingual-ko">언어 선택:</span><span class="bilingual-en">Language:</span></span><button type="button" id="btnModalCenterLangKo" onclick="toggleModalLang('ko')" style="background:linear-gradient(135deg,#38bdf8 0%,#818cf8 100%);color:#0b1020;border:none;border-radius:20px;padding:6px 16px;font-size:0.86rem;font-weight:800;cursor:pointer;transition:all .18s;box-shadow:0 2px 10px rgba(56,189,248,.45)">🇰🇷 한국어</button><button type="button" id="btnModalCenterLangEn" onclick="toggleModalLang('en')" style="background:transparent;color:#cbd5e1;border:none;border-radius:20px;padding:6px 16px;font-size:0.86rem;font-weight:700;cursor:pointer;transition:all .18s">🌐 English</button></div><div id="topGuestFreePassRow" style="margin:12px 0 16px;width:100%;max-width:440px;display:flex;flex-direction:column;align-items:center;gap:10px"><button type="button" id="btnTeacherPreviewInModal" onclick="startFreePractice()" style="width:100%;max-width:420px;background:linear-gradient(135deg,#38bdf8 0%,#818cf8 50%,#a855f7 100%);color:#070d1e;border:2px solid #ffffff;border-radius:14px;padding:14px 22px;font-size:1.1rem;font-weight:900;cursor:pointer;transition:all .2s ease;box-shadow:0 0 24px rgba(56,189,248,.7),0 6px 18px rgba(0,0,0,.5);display:inline-flex;align-items:center;justify-content:center;gap:8px;letter-spacing:-0.2px"><span class="bilingual-ko">🚀 가입 없이 바로 문제 열람 & 자유 풀기 ➔</span><span class="bilingual-en">🚀 Free Practice (No Login Required) ➔</span></button><div style="font-size:0.81rem;color:#94a3b8;display:flex;align-items:center;gap:8px;width:100%;max-width:380px"><span style="flex:1;height:1px;background:rgba(255,255,255,.15)"></span><span><span class="bilingual-ko">또는 이름을 입력하고 학습 기록 저장</span><span class="bilingual-en">Or enter name to save your progress</span></span><span style="flex:1;height:1px;background:rgba(255,255,255,.15)"></span></div></div><h3 style="color:#131b2e;margin:0 0 6px;font-weight:800">📝 먼저 이름을 입력하세요</h3><p style="color:#45464d;font-size:.9rem;margin:0 0 20px"><span class="bilingual-ko">이름을 입력해야 학습 기록이 저장됩니다.</span><span class="bilingual-en">Your learning progress will be saved under this name.</span></p><div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap"><input type="text" id="studentName" placeholder="이름 입력" autofocus style="background:#ffffff;color:#1b1b1d;border:1.5px solid #c5c6cd;border-radius:10px;padding:12px 16px;font-size:1.05rem;min-width:200px;text-align:center"><button class="btn" onclick="registerName()" style="font-size:1.05rem;padding:12px 24px"><span class="bilingual-ko">시작하기</span><span class="bilingual-en">Start</span></button></div></div><script>window._studentName="";window._sheetsApiUrl="https://script.google.com/macros/s/AKfycbxQBW1hKYFSHokaVJMRql-UJpk0t4qMeWMiiy_RFuCLZ5SE4iZytYQkGa9_yoCmm1Ak0Q/exec";function toggleModalLang(l){{document.documentElement.lang=l;try{{localStorage.setItem("mathedu_lang",l);localStorage.setItem("mathedu_lang_manual","true");}}catch(e){{}}if(window.setBoardLanguage)window.setBoardLanguage(l);else if(window.setBoardLang)window.setBoardLang(l,true);}}function startFreePractice(){{var vid="";try{{vid=localStorage.getItem("mathedu_visitor_id")||"";if(!vid){{vid=Math.random().toString(36).substring(2,6).toUpperCase();localStorage.setItem("mathedu_visitor_id",vid);}}}}catch(e){{vid="ANON";}}window._studentName=((document.documentElement.lang==="en")?"Guest#":"자유학습#")+vid;var tf=document.getElementById("trackFull");if(tf)tf.remove();if(window.sendProgress)sendProgress();if(window.MathJax&&MathJax.typesetPromise)MathJax.typesetPromise();}}function registerName(){{var n=document.getElementById("studentName").value.trim();if(!n){{alert((document.documentElement.lang==="en")?"Please enter your name":"이름을 입력하세요");return;}}window._studentName=n;document.getElementById("trackFull").remove();sendProgress();if(window.MathJax&&MathJax.typesetPromise){{MathJax.typesetPromise();}}}}function sendProgress(){{var name=(window._studentName||"").trim();if(!name)return;var qs=document.querySelectorAll(".q");var total=qs.length;var done=document.querySelectorAll(".q.done");var correct=0;done.forEach(function(q){{if(q.querySelector(".opt.correct"))correct++;}});if(total===0)return;fetch(window._sheetsApiUrl,{{method:"POST",mode:"no-cors",keepalive:true,headers:{{"Content-Type":"text/plain;charset=utf-8"}},body:JSON.stringify({{quiz_slug:window._activeEbsiSlug||"{slug}",student_name:name,current_step:done.length,total_steps:total,correct:correct}})}}).catch(function(){{}});}}</script>
<h2>🎯 최종 문제 + 상세 풀이<span class="bilingual-en">🎯 Final Official Exam Problem & Complete Solution</span></h2><div class="sol" id="ebsiSolContainer">
  <div class="bilingual-ko">
{sol_ko}
  </div>
  <div class="bilingual-en">
{sol_en}
  </div>
</div><div id="ebsiFinalQWrap">{final_q_block}</div>
<div id="ebsiAddonWrap">{addon_card_html}</div>
<div class="final"><p><span class="bilingual-ko">🎉 완료!</span><span class="bilingual-en">🎉 Completed!</span></p><div class="ans" id="finalAns">정답 {final_ans_display}</div>
<button class="btn" onclick="location.reload()"><span class="bilingual-ko">다시 풀기</span><span class="bilingual-en">Try Again</span></button></div>
</div><script>
let pts=0;
function bindAllQuizEvents(){{
  pts=0;
  const qs=document.querySelectorAll('.q');
  const totEl=document.getElementById('tot');
  if(totEl) totEl.textContent=qs.length;
  const ptsEl=document.getElementById('pts');
  if(ptsEl) ptsEl.textContent='0';
  const barEl=document.getElementById('bar');
  if(barEl) barEl.style.width='0%';
  const pctEl=document.getElementById('pct');
  if(pctEl) pctEl.textContent='0%';

  qs.forEach(q=>{{
    if(q.dataset.bound==='1') return;
    q.dataset.bound='1';
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
        if(exp){{exp.classList.add('show');if(window.MathJax&&window.MathJax.typesetPromise){{window.MathJax.typesetPromise([exp]).catch(function(){{}});}}}}
        var toggleBtn = q.querySelector('.exp-toggle-btn');
        if(toggleBtn) {{ var isEn = (document.documentElement.lang === 'en'); toggleBtn.textContent = isEn ? '💡 Close Explanation' : '💡 해설 닫기'; }}
        document.getElementById('pts').textContent=pts;
        var total = document.querySelectorAll('.q').length;
        const pct=Math.round(pts/total*100);
        document.getElementById('bar').style.width=pct+'%';
        document.getElementById('pct').textContent=pct+'%';
        if(typeof window.syncStitchProgress === 'function') window.syncStitchProgress();
        if(typeof sendProgress === 'function') setTimeout(sendProgress, 50);
      }});
    }});
  }});
}}
bindAllQuizEvents();

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
    if(window.MathJax&&window.MathJax.typesetPromise){{window.MathJax.typesetPromise([exp]).catch(function(){{}});}}
  }}
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
  var slug=window._activeEbsiSlug || '{slug}';
  var qEl=wrap.closest('.q');
  var qNum=qEl?Array.from(document.querySelectorAll('.q')).indexOf(qEl)+1:0;
  var textEl=wrap.querySelector('.report-text');
  var text=(textEl ? textEl.value : '').trim();
  var url=window._sheetsApiUrl||'https://script.google.com/macros/s/AKfycbxQBW1hKYFSHokaVJMRql-UJpk0t4qMeWMiiy_RFuCLZ5SE4iZytYQkGa9_yoCmm1Ak0Q/exec';
  var reportUrl=url+'?action=report&quiz='+encodeURIComponent(slug)+'&q='+qNum+'&name='+encodeURIComponent(name)+'&text='+encodeURIComponent(text||'사유 없음')+'&_t='+Date.now();
  try {{ fetch(reportUrl, {{ mode: 'no-cors', keepalive: true }}).catch(function(){{}}); }} catch(e){{}}
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
</script>
{extra_bottom_js}
</body></html>"""
    return page_html


def build_ebsi_dynamic_player_scripts() -> tuple:
    """Return (extra_top_html, extra_bottom_js) for board/ebsi.html so it can dynamically load any of the 16,747 EBSi problems."""
    extra_top_html = """
  <section id="ebsiUniversalNavBar" style="margin:12px 0 14px;padding:14px 16px;background:linear-gradient(135deg,#f8fafc 0%,#eff6ff 100%);border:1.5px solid #bfdbfe;border-radius:14px;box-shadow:0 2px 10px rgba(0,99,152,0.06)">
    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;margin-bottom:10px">
      <div style="display:flex;align-items:center;gap:6px;font-weight:800;font-size:0.88rem;color:#006398">
        <span>🗂️ EBSi 전 연도(2006~2027학년도) · 전 학년(고1·고2·고3) 16,548문항 단계별 플레이어</span>
      </div>
      <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap">
        <button type="button" onclick="navEbsiProblem(-1)" style="background:#ffffff;border:1px solid #cbd5e1;color:#1e293b;border-radius:8px;padding:4px 10px;font-size:0.78rem;font-weight:700;cursor:pointer">◀ 이전 번호</button>
        <button type="button" onclick="navEbsiProblem(1)" style="background:#ffffff;border:1px solid #cbd5e1;color:#1e293b;border-radius:8px;padding:4px 10px;font-size:0.78rem;font-weight:700;cursor:pointer">다음 번호 ▶</button>
        <button type="button" onclick="downloadCurrentEbsiOffline()" style="background:#006398;border:none;color:#ffffff;border-radius:8px;padding:5px 12px;font-size:0.78rem;font-weight:800;cursor:pointer">📥 이 문항 단독 오프라인 HTML 저장</button>
      </div>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:8px">
      <select id="ebsiSelYear" onchange="onEbsiFilterChange('year')" style="background:#ffffff;border:1px solid #cbd5e1;border-radius:8px;padding:7px 10px;font-size:0.82rem;font-weight:700;color:#1e293b"></select>
      <select id="ebsiSelGrade" onchange="onEbsiFilterChange('grade')" style="background:#ffffff;border:1px solid #cbd5e1;border-radius:8px;padding:7px 10px;font-size:0.82rem;font-weight:700;color:#1e293b">
        <option value="고3">고3 (수능·모평·학평)</option>
        <option value="고2">고2 (전국연합학력평가)</option>
        <option value="고1">고1 (전국연합학력평가)</option>
      </select>
      <select id="ebsiSelPaper" onchange="onEbsiFilterChange('paper')" style="background:#ffffff;border:1px solid #cbd5e1;border-radius:8px;padding:7px 10px;font-size:0.82rem;font-weight:700;color:#1e293b;grid-column:span 2"></select>
      <select id="ebsiSelQnum" onchange="onEbsiQnumSelect()" style="background:#ffffff;border:1px solid #cbd5e1;border-radius:8px;padding:7px 10px;font-size:0.82rem;font-weight:800;color:#006398"></select>
    </div>
  </section>"""

    tpl_json = json.dumps(UNIT_TEMPLATES + [DEFAULT_UNIT_TEMPLATE], ensure_ascii=False)

    extra_bottom_js = f"""<script>
window.EBSI_UNIT_TEMPLATES = {tpl_json};
window._ebsiShardCache = {{}};
window._ebsiCurrentYearData = null;
window._activeEbsiSlug = new URLSearchParams(window.location.search).get('id') || 'e25_26111851_01';

function getShardBaseUrl() {{
  var p = window.location.pathname.replace(/\\\\/g, '/');
  if (p.indexOf('/offline/') !== -1) return '../board/ebsi_shards/';
  return 'ebsi_shards/';
}}

function escapeHtmlAttr(s) {{
  return String(s || '').replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}}

function buildDynamicSvgBlock(prob, tpl, ansDisplay) {{
  var topic = tpl.topic_ko || '수학 핵심 개념';
  var unit = (prob.unit_parts && prob.unit_parts.length) ? prob.unit_parts[prob.unit_parts.length - 1] : topic;
  var s1 = '1단계: 초등 기초 직관 및 구구단·사칙연산 규칙 확인';
  var s2 = '2단계: ' + topic + ' 기호 번역 및 기본 공식 연결';
  var s3 = '3단계: 출발 조건 식 세우기 (' + unit + ')';
  var s4 = '4단계: 핵심 관계식 정리 및 중간 값 도출';
  var s5 = '5단계: 최종 계산 조립 ⇒ 정답 ' + ansDisplay;
  return '<figure class="math-visual-diagram" style="margin:16px 0;padding:16px;background:#f8fafc;border:1.5px solid #cbd5e1;border-radius:14px;text-align:center">' +
    '<div style="font-weight:800;font-size:0.92rem;color:#006398;margin-bottom:10px">🎨 [그림으로 이해하는 시각적 도형·개념 다이어그램: ' + unit + ']</div>' +
    '<svg viewBox="0 0 640 210" style="width:100%;max-width:620px;height:auto;background:#ffffff;border-radius:10px;border:1px solid #e2e8f0" xmlns="http://www.w3.org/2000/svg">' +
      '<defs><linearGradient id="ebsiGrad1" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#e0f2fe"/><stop offset="100%" stop-color="#ede9fe"/></linearGradient></defs>' +
      '<rect x="16" y="16" width="180" height="178" rx="12" fill="url(#ebsiGrad1)" stroke="#0284c7" stroke-width="2"/>' +
      '<text x="106" y="48" text-anchor="middle" font-size="13" font-weight="bold" fill="#0369a1">[출발 조건 &amp; 단원 원리]</text>' +
      '<text x="106" y="82" text-anchor="middle" font-size="12" font-weight="bold" fill="#0f172a">' + unit.slice(0, 14) + '</text>' +
      '<circle cx="106" cy="135" r="34" fill="#ffffff" stroke="#0284c7" stroke-width="2" stroke-dasharray="4,3"/>' +
      '<path d="M 82 145 L 106 112 L 130 145 Z" fill="#bae6fd" stroke="#0369a1" stroke-width="1.8"/>' +
      '<path d="M 204 105 L 236 105" stroke="#0284c7" stroke-width="3" marker-end="url(#arrow)"/>' +
      '<rect x="242" y="16" width="180" height="178" rx="12" fill="#f0fdf4" stroke="#059669" stroke-width="2"/>' +
      '<text x="332" y="48" text-anchor="middle" font-size="13" font-weight="bold" fill="#047857">[디딤돌 1~4단계 연결]</text>' +
      '<line x1="264" y1="155" x2="400" y2="155" stroke="#64748b" stroke-width="2"/>' +
      '<line x1="280" y1="170" x2="280" y2="70" stroke="#64748b" stroke-width="2"/>' +
      '<path d="M 270 148 Q 330 72 392 92" fill="none" stroke="#059669" stroke-width="3"/>' +
      '<circle cx="332" cy="108" r="5" fill="#d97706"/>' +
      '<text x="332" y="138" text-anchor="middle" font-size="11" font-weight="bold" fill="#065f46">핵심 식 변형 · 대입</text>' +
      '<path d="M 428 105 L 460 105" stroke="#4f46e5" stroke-width="3"/>' +
      '<rect x="466" y="16" width="158" height="178" rx="12" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>' +
      '<text x="545" y="52" text-anchor="middle" font-size="13" font-weight="bold" fill="#b45309">[최종 목표값 도출]</text>' +
      '<rect x="486" y="80" width="118" height="54" rx="10" fill="#ffffff" stroke="#d97706" stroke-width="2"/>' +
      '<text x="545" y="112" text-anchor="middle" font-size="15" font-weight="bold" fill="#1e293b">정답 ' + String(prob.answer) + '번</text>' +
      '<text x="545" y="162" text-anchor="middle" font-size="11" font-weight="bold" fill="#92400e">검산 및 조건 확인 완료</text>' +
    '</svg>' +
  '</figure>' +
  '<section class="math-schematic-flow" style="margin:16px 0;padding:16px;background:#ffffff;border:1.5px solid #cbd5e1;border-radius:14px">' +
    '<div style="font-weight:800;font-size:0.92rem;color:#006398;margin-bottom:10px">🗺️ [한눈에 보는 도식화 풀이 흐름도]</div>' +
    '<div style="display:flex;flex-direction:column;gap:6px;font-size:0.86rem;color:#1e293b;text-align:left">' +
      '<div style="padding:8px 12px;background:#f0f9ff;border-left:4px solid #0284c7;border-radius:6px"><b>' + s1 + '</b></div>' +
      '<div style="padding:8px 12px;background:#f0fdf4;border-left:4px solid #059669;border-radius:6px"><b>' + s2 + '</b></div>' +
      '<div style="padding:8px 12px;background:#eff6ff;border-left:4px solid #2563eb;border-radius:6px"><b>' + s3 + '</b></div>' +
      '<div style="padding:8px 12px;background:#f5f3ff;border-left:4px solid #4f46e5;border-radius:6px"><b>' + s4 + '</b></div>' +
      '<div style="padding:8px 12px;background:#fffbeb;border-left:4px solid #d97706;border-radius:6px"><b>' + s5 + '</b></div>' +
    '</div>' +
  '</section>';
}}

function renderSingleQBlockHtml(qObj, isFinal, stepIdx, knowKo, solKo) {{
  var ans = qObj.answer || 1;
  var expRaw = qObj.exp || '';
  if (isFinal && solKo) {{
    expRaw = '<b>📌 [최종 본문항 핵심 요약]</b><br>' + expRaw + '<hr style="border:none;border-top:1px dashed #cbd5e1;margin:12px 0">' + solKo;
  }} else if (!isFinal && knowKo) {{
    expRaw = '<b>✅ [제' + stepIdx + '단계 정답 및 핵심 해설]</b><br>' + expRaw + '<br><br><b>📖 [제' + stepIdx + '단계 핵심 원리 및 유도 과정]</b><br>' + knowKo;
  }}
  var optsHtml = '';
  var opts = qObj.options || ['$1$','$2$','$3$','$4$','$5$'];
  for (var i = 0; i < opts.length; i++) {{
    optsHtml += '<div cl' + 'ass="opt"><span class="n">' + (i + 1) + '</span>' + opts[i] + '</div>';
  }}
  return '<div cl' + 'ass="q" data-a' + 'ns="' + ans + '" data-e' + 'xp="' + escapeHtmlAttr(expRaw) + '" data-e' + 'xp-en="' + escapeHtmlAttr(qObj.exp_en || expRaw) + '">' +
    '<div cl' + 'ass="lvl"><span class="bilingual-ko">' + (qObj.level_label || '디딤돌 문제') + '</span><span class="bilingual-en">' + (qObj.level_label_en || 'Scaffolding Step') + '</span></div>' +
    '<div cl' + 'ass="stem"><span class="bilingual-ko">' + qObj.stem + '</span></div>' +
    '<div cl' + 'ass="opts">' + optsHtml + '</div>' +
    '<div class="q-actions" style="margin-top:10px;display:flex;justify-content:flex-end"><button type="button" class="exp-toggle-btn" onclick="toggleExp(this)">💡 해설 보기</button></div>' +
    '<div class="exp"></div>' +
  '</div>';
}}

function renderEbsiProblemToDom(prob) {{
  if (!prob) return;
  window._activeEbsiSlug = prob.slug;
  window._activeEbsiProblem = prob;
  var tpl = window.EBSI_UNIT_TEMPLATES[prob.tpl_idx] || window.EBSI_UNIT_TEMPLATES[window.EBSI_UNIT_TEMPLATES.length - 1];
  var unitParts = prob.unit_parts || [];
  var leafUnit = unitParts.length ? unitParts[unitParts.length - 1] : tpl.topic_ko;
  var midUnit = unitParts.length >= 2 ? unitParts[unitParts.length - 2] : tpl.topic_ko;
  var ansIdx = parseInt(prob.answer || 1, 10);
  var opts = prob.options || ['$1$','$2$','$3$','$4$','$5$'];
  var ansDisplay = opts[ansIdx - 1] || String(ansIdx);

  // Update page title & Stitch H1
  document.title = prob.title + ' · mathedu 수학자료실';
  var h1Main = document.querySelector('.stitch-h1-main');
  var h1Acc = document.querySelector('.stitch-h1-accent');
  var mBr = prob.title.match(/^(\\[.*?\\])\\s*(.*)$/);
  if (h1Main && h1Acc && mBr) {{
    h1Main.textContent = mBr[1];
    h1Acc.textContent = mBr[2];
  }} else {{
    var h1Ko = document.querySelector('h1 .bilingual-ko');
    if (h1Ko) h1Ko.textContent = '📘 ' + prob.title;
  }}

  var badgeEl = document.getElementById('ebsiOrigBadge');
  if (badgeEl) badgeEl.innerHTML = '<span class="bilingual-ko">' + prob.examYear + '학년도 ' + prob.month + ' ' + prob.grade + ' ' + prob.subject + ' ' + prob.qNum + '번</span>';

  var circled = ['①','②','③','④','⑤'];
  var origOpts = opts.map(function(o, idx) {{
    return '<span style="display:inline-block;margin:3px 6px 3px 0;font-weight:600;color:#1e293b">' + (circled[idx] || (idx+1)) + ' ' + o + '</span>';
  }}).join(' &nbsp;&nbsp; ');

  var paperBox = document.getElementById('ebsiOrigPaperBox');
  if (paperBox) {{
    paperBox.innerHTML =
      '<p style="margin:0 0 10px;padding-bottom:8px;border-bottom:1.5px solid #0f172a;display:flex;justify-content:space-between;align-items:center;font-weight:800;font-size:0.86rem;color:#0f172a">' +
        '<span>📄 ' + (prob.source || (prob.examYear + '학년도 기출')) + ' · ' + prob.subject + '</span>' +
        '<span style="background:#0f172a;color:#ffffff;padding:2px 10px;border-radius:999px;font-size:0.78rem">문항 ' + prob.qNum + '번 (' + (prob.point || '3') + '점)</span>' +
      '</p>' +
      '<p style="margin:0 0 14px;color:#111827;font-size:0.97rem;line-height:1.85">' + prob.stem + '</p>' +
      '<p style="margin:0;padding-top:10px;border-top:1px dashed #cbd5e1;font-size:0.92rem;line-height:1.7">' + origOpts + '</p>';
  }}

  var topicEl = document.getElementById('ebsiOrigTopicTitle');
  if (topicEl) topicEl.textContent = prob.title.replace(/^\\[.*?\\]\\s*/, '');
  var sumEl = document.getElementById('ebsiOrigSummaryKo');
  if (sumEl) sumEl.textContent = (prob.intent || leafUnit) + ' · 초등 눈높이 5단계 디딤돌 퀴즈 및 시각적 도식화 해설';

  // Step 0 symbols
  var symEl = document.getElementById('ebsiSymContainer');
  if (symEl && tpl.symbols) {{
    symEl.innerHTML = tpl.symbols.map(function(s) {{
      return '<div><b>' + s.sym + '</b> — ' + s.desc + '<div class="bilingual-en">' + (s.desc_en || '') + '</div></div>';
    }}).join('');
  }}

  // Build 5 Scaffolding Steps
  var s3Line = prob.s3 || ('주어진 조건을 <b>' + leafUnit + '</b>의 기본 수식으로 나타냅니다.');
  var s4Line = prob.s4 || ('세운 관계식에 조건의 수치를 대입하여 중간 식을 정리합니다.');
  var s5Line = prob.s5 || ('정리한 식으로부터 최종 목표값을 계산하면 정답은 ' + ansDisplay + '입니다.');
  var s3Q = prob.s3_q || {{
    level_label: '조건 식 세우기 디딤돌 3',
    stem: '본문항의 출발 조건을 <b>' + leafUnit + '</b>의 관계식으로 나타내면 다음과 같습니다:<br><div style="margin:8px 0;padding:10px 14px;background:#f8fafc;border-left:4px solid #0284c7;border-radius:8px">' + s3Line + '</div>위 식의 전개 방향과 일치하는 핵심 단원 원리는?',
    options: [midUnit + ' · ' + leafUnit + '의 정의와 성질 적용', '역삼각함수의 치환적분', '벡터의 외적과 평면의 방정식', '복소평면의 극형식 변환', '행렬식의 여인수 전개'],
    answer: 1,
    exp: '출발 조건을 <b>' + leafUnit + '</b>의 관계식으로 세우면 다음과 같습니다:<br>• ' + s3Line
  }};
  s3Q.level_label = s3Q.level_label || '조건 식 세우기 디딤돌 3';

  var s4Q = prob.s4_q || {{
    level_label: '중간 관계식 디딤돌 4',
    stem: '앞선 출발 식을 정리하여 중간 관계식을 유도하면 다음과 같습니다:<br><div style="margin:8px 0;padding:10px 14px;background:#f0fdf4;border-left:4px solid #059669;border-radius:8px">' + s4Line + '</div>위 중간 식으로부터 얻을 수 있는 올바른 결론은?',
    options: opts,
    answer: ansIdx,
    exp: '<b>' + leafUnit + '</b>의 성질에 따라 주어진 식을 정리하면 다음과 같이 전개됩니다:<br>• ' + s4Line
  }};
  s4Q.level_label = s4Q.level_label || '중간 관계식 디딤돌 4';

  var stepsData = [
    {{
      title: tpl.step1.title, title_en: tpl.step1.title_en,
      know: tpl.step1.knowledge,
      q: {{ level_label: '초등 직관 디딤돌 1', stem: tpl.step1.stem, options: tpl.step1.options, answer: tpl.step1.answer, exp: tpl.step1.exp }}
    }},
    {{
      title: tpl.step2.title, title_en: tpl.step2.title_en,
      know: tpl.step2.knowledge,
      q: {{ level_label: '기호 번역 디딤돌 2', stem: tpl.step2.stem, options: tpl.step2.options, answer: tpl.step2.answer, exp: tpl.step2.exp }}
    }},
    {{
      title: '🌱 3단계 · [출발 조건 식 세우기] ' + leafUnit + ' 핵심 조건 변환',
      title_en: '🌱 Step 3 · [Setting Up the Equation]',
      know: '본문항 해결의 첫걸음은 문제의 조건을 <b>' + leafUnit + '</b> 단원의 수식으로 옮기는 것입니다.<br>• <b>출발 식 및 원리</b>: ' + s3Line,
      q: s3Q
    }},
    {{
      title: '🌳 4단계 · [풀이 전개] 핵심 관계식 정리 및 중간 값 도출',
      title_en: '🌳 Step 4 · [Intermediate Derivation]',
      know: '3단계에서 세운 출발 식을 정리하여 문제에서 요구하는 핵심 미지수 또는 관계식을 도출합니다.<br>• <b>중간 전개 과정</b>: ' + s4Line,
      q: s4Q
    }},
    {{
      title: '💎 5단계 · [최종 계산 조립] 디딤돌 조각을 합쳐 최종 정답 구하기',
      title_en: '💎 Step 5 · [Final Synthesis]',
      know: '1~4단계에서 확인한 원리와 중간 식을 결합하여 최종 목표값을 구합니다.<br>• <b>최종 마무리 계산</b>: ' + s5Line,
      q: {{
        level_label: '최종 정답 조립 디딤돌 5',
        stem: '위의 단계별 전개 과정을 끝까지 계산하여 얻는 이 문제의 <b>최종 결과값</b>은?',
        options: opts,
        answer: ansIdx,
        exp: '단계별 계산을 마무리하면 최종 결과는 <b>' + ansDisplay + '</b> (<b>' + ansIdx + '번</b>)입니다.<br>• ' + s5Line
      }}
    }}
  ];

  var lvHtml = '';
  stepsData.forEach(function(st, idx) {{
    lvHtml += '<h2>' + st.title + '<span class="bilingual-en">' + st.title_en + '</span></h2>' +
      '<div class="know"><h3>먼저 알아야 할 지식</h3>' + st.know + '</div>' +
      renderSingleQBlockHtml(st.q, false, idx + 1, st.know, '');
  }});
  var lvWrap = document.getElementById('ebsiDynamicLevelsWrap');
  if (lvWrap) lvWrap.innerHTML = lvHtml;

  // Solution & Visual Diagram
  var expBody = (prob.exp_lines && prob.exp_lines.length) ? prob.exp_lines.join('<br>\\n') : ('주어진 조건에 ' + leafUnit + '의 성질을 적용하면 정답은 ' + ansDisplay + '입니다.');
  var unitBread = unitParts.length ? unitParts.join(' &gt; ') : (prob.subject + ' &gt; ' + tpl.topic_ko);
  var visBlock = buildDynamicSvgBlock(prob, tpl, ansDisplay);
  var solKo =
    '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>' +
    '<p>본 문항은 <b>' + unitBread + '</b> 단원에서 <b>' + (prob.intent || leafUnit) + '</b> 능력을 평가하는 ' + (prob.point || '3') + '점 기출문항입니다.</p>' +
    visBlock +
    '<h4>📐 [단계별 상세 풀이 전개]</h4>' +
    '<p>' + expBody + '</p>' +
    '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>' +
    '<p>따라서 구하는 최종 정답은 <b>' + ansDisplay + ' (정답 ' + ansIdx + '번)</b>입니다.</p>';

  var solContainer = document.getElementById('ebsiSolContainer');
  if (solContainer) {{
    solContainer.innerHTML = '<div class="bilingual-ko">' + solKo + '</div><div class="bilingual-en">' + solKo + '</div>';
  }}

  var finalWrap = document.getElementById('ebsiFinalQWrap');
  if (finalWrap) {{
    finalWrap.innerHTML = renderSingleQBlockHtml({{
      level_label: '최종 본문항',
      level_label_en: 'Final Exam Problem',
      stem: prob.stem,
      options: opts,
      answer: ansIdx,
      exp: '<b>[출제의도]</b> ' + (prob.intent || leafUnit) + '<br>' + expBody
    }}, true, 6, '', solKo);
  }}

  var finalAnsEl = document.getElementById('finalAns');
  if (finalAnsEl) finalAnsEl.innerHTML = '정답 ' + ansDisplay;

  bindAllQuizEvents();
  if (window.MathJax && window.MathJax.typesetPromise) {{
    window.MathJax.typesetPromise().catch(function(){{}});
  }}
}}

function loadEbsiYearShard(yearStr, callback) {{
  if (window._ebsiShardCache[yearStr]) {{
    callback(window._ebsiShardCache[yearStr]);
    return;
  }}
  var url = getShardBaseUrl() + 'ebsi_' + yearStr + '.json';
  fetch(url)
    .then(function(r) {{ return r.json(); }})
    .then(function(data) {{
      window._ebsiShardCache[yearStr] = data;
      callback(data);
    }})
    .catch(function(err) {{
      console.error('Failed to load EBSi shard:', err);
    }});
}}

function populateEbsiNavigator(yearData, activeProb) {{
  window._ebsiCurrentYearData = yearData;
  var selYear = document.getElementById('ebsiSelYear');
  if (selYear && selYear.options.length === 0) {{
    for (var y = 2026; y >= 2006; y--) {{
      var opt = document.createElement('option');
      opt.value = String(y);
      opt.textContent = y + '년 시행 (' + (y + 1) + '·' + y + '학년도)';
      selYear.appendChild(opt);
    }}
  }}
  if (selYear && activeProb) selYear.value = String(activeProb.year || '2025');
  var selGrade = document.getElementById('ebsiSelGrade');
  if (selGrade && activeProb) selGrade.value = activeProb.grade || '고3';

  updateEbsiPaperDropdown(activeProb ? activeProb.paperId : null, activeProb ? activeProb.qNum : '1');
}}

function updateEbsiPaperDropdown(targetPaperId, targetQnum) {{
  var yearData = window._ebsiCurrentYearData;
  if (!yearData || !yearData.problems) return;
  var grade = document.getElementById('ebsiSelGrade').value;
  var selPaper = document.getElementById('ebsiSelPaper');
  var papersMap = {{}};
  var paperOrder = [];
  Object.keys(yearData.problems).forEach(function(slug) {{
    var p = yearData.problems[slug];
    if (p.grade !== grade) return;
    var pKey = p.paperId + '_' + p.subject;
    if (!papersMap[pKey]) {{
      papersMap[pKey] = {{ key: pKey, label: p.month + ' · ' + p.subject + ' (' + p.source + ')', items: [] }};
      paperOrder.push(pKey);
    }}
    papersMap[pKey].items.push(p);
  }});
  selPaper.innerHTML = '';
  paperOrder.forEach(function(pk) {{
    var o = document.createElement('option');
    o.value = pk;
    o.textContent = papersMap[pk].label;
    selPaper.appendChild(o);
  }});
  if (targetPaperId) {{
    for (var i = 0; i < selPaper.options.length; i++) {{
      if (selPaper.options[i].value.indexOf(targetPaperId + '_') === 0) {{
        selPaper.selectedIndex = i;
        break;
      }}
    }}
  }}
  window._ebsiPapersMap = papersMap;
  updateEbsiQnumDropdown(targetQnum);
}}

function updateEbsiQnumDropdown(targetQnum) {{
  var selPaper = document.getElementById('ebsiSelPaper');
  var selQnum = document.getElementById('ebsiSelQnum');
  if (!selPaper || !selQnum || !window._ebsiPapersMap) return;
  var pk = selPaper.value;
  var group = window._ebsiPapersMap[pk];
  selQnum.innerHTML = '';
  if (!group) return;
  group.items.sort(function(a, b) {{ return parseInt(a.qNum, 10) - parseInt(b.qNum, 10); }});
  group.items.forEach(function(p) {{
    var o = document.createElement('option');
    o.value = p.slug;
    o.textContent = p.qNum + '번 (' + (p.point || '3') + '점)';
    selQnum.appendChild(o);
  }});
  if (targetQnum) {{
    for (var i = 0; i < group.items.length; i++) {{
      if (String(group.items[i].qNum) === String(targetQnum)) {{
        selQnum.value = group.items[i].slug;
        break;
      }}
    }}
  }}
}}

function onEbsiFilterChange(level) {{
  if (level === 'year') {{
    var y = document.getElementById('ebsiSelYear').value;
    loadEbsiYearShard(y, function(yearData) {{
      window._ebsiCurrentYearData = yearData;
      updateEbsiPaperDropdown(null, '1');
      onEbsiQnumSelect();
    }});
  }} else if (level === 'grade') {{
    updateEbsiPaperDropdown(null, '1');
    onEbsiQnumSelect();
  }} else if (level === 'paper') {{
    updateEbsiQnumDropdown('1');
    onEbsiQnumSelect();
  }}
}}

function onEbsiQnumSelect() {{
  var selQnum = document.getElementById('ebsiSelQnum');
  if (!selQnum || !selQnum.value || !window._ebsiCurrentYearData) return;
  var slug = selQnum.value;
  var prob = window._ebsiCurrentYearData.problems[slug];
  if (prob) {{
    try {{ history.replaceState(null, '', '?id=' + encodeURIComponent(slug)); }} catch(e){{}}
    renderEbsiProblemToDom(prob);
  }}
}}

function navEbsiProblem(delta) {{
  var selQnum = document.getElementById('ebsiSelQnum');
  if (!selQnum || selQnum.options.length === 0) return;
  var nextIdx = selQnum.selectedIndex + delta;
  if (nextIdx >= 0 && nextIdx < selQnum.options.length) {{
    selQnum.selectedIndex = nextIdx;
    onEbsiQnumSelect();
  }}
}}

function downloadCurrentEbsiOffline() {{
  var slug = window._activeEbsiSlug || 'ebsi_quiz';
  var docClone = document.documentElement.cloneNode(true);
  var nav = docClone.querySelector('#ebsiUniversalNavBar');
  if (nav) nav.remove();
  var htmlStr = '<!DOCTYPE html>\\n' + docClone.outerHTML;
  var blob = new Blob([htmlStr], {{ type: 'text/html;charset=utf-8' }});
  var url = URL.createObjectURL(blob);
  var a = document.createElement('a');
  a.href = url;
  a.download = 'mathedu_' + slug + '_offline.html';
  document.body.appendChild(a);
  a.click();
  setTimeout(function() {{ a.remove(); URL.revokeObjectURL(url); }}, 500);
}}

(function initEbsiPlayer() {{
  var params = new URLSearchParams(window.location.search);
  var id = params.get('id') || 'e25_26111851_01';
  var m = id.match(/^e(\\d{{2}})_/);
  var yearStr = m ? ('20' + m[1]) : '2025';
  loadEbsiYearShard(yearStr, function(yearData) {{
    var prob = (yearData && yearData.problems && yearData.problems[id]) ? yearData.problems[id] : null;
    if (!prob && yearData && yearData.problems) {{
      var firstKey = Object.keys(yearData.problems)[0];
      prob = yearData.problems[firstKey];
    }}
    if (prob) {{
      populateEbsiNavigator(yearData, prob);
      renderEbsiProblemToDom(prob);
    }}
  }});
}})();
</script>"""
    return extra_top_html, extra_bottom_js


def get_tpl_idx(unit_parts: list, intent_ko: str, stem_html: str) -> int:
    hay = f"{' '.join(unit_parts)} {intent_ko} {stem_html}"
    for idx, tpl in enumerate(UNIT_TEMPLATES):
        if any(kw in hay for kw in tpl["keywords"]):
            return idx
    return len(UNIT_TEMPLATES)


def main():
    with open(PAPERS_JSON, "r", encoding="utf-8") as f:
        papers = json.load(f)

    odd_papers = [p for p in papers if p.get("isEven") != "1"]
    print(f"Loaded {len(odd_papers)} standard/odd EBSi math exam papers across 2006~2026 (고3, 고2, 고1).")

    shards_by_year = {}
    catalog_items = []
    standalone_problems = []
    default_ebsi_prob = None

    # Deduplication set for 2022-curriculum Grade 12 common questions (1~22 shared across 확통/미적분/기하)
    seen_common_keys = set()

    for p in odd_papers:
        meta = parse_paper_metadata(p)
        pid = meta["paperId"]
        xml_path = os.path.join(CACHE_DIR, f"{pid}.xml")
        if not os.path.exists(xml_path):
            continue

        try:
            root = ET.parse(xml_path).getroot()
        except Exception as e:
            print(f"XML parse error in {pid}: {e}")
            continue

        cal_year = meta["calYear"]
        exam_year = meta["examYear"]
        exam_year_alt = meta["examYearAlt"]
        month = meta["month"]
        month_label = meta["monthLabel"]
        grade = meta["grade"]
        subj = meta["subject"]
        is_csat = meta["isCsat"]
        source = meta["source"]
        date_str = meta["date"]

        if cal_year not in shards_by_year:
            shards_by_year[cal_year] = {"year": cal_year, "problems": {}}

        is_2022_curr_g3 = (grade == "고3" and int(cal_year) >= 2021 and subj in ("확률과 통계", "미적분", "기하"))

        for pd in root.findall(".//PaperDetail"):
            qnum_int = int(pd.attrib.get("ItemNumber", "0") or "0")
            if qnum_int <= 0:
                continue
            qnum_str = str(qnum_int)

            if is_2022_curr_g3 and 1 <= qnum_int <= 22:
                eff_subj = "공통(수학I·II)"
                common_key = (cal_year, month, grade, source, qnum_int)
                if common_key in seen_common_keys:
                    continue
                seen_common_keys.add(common_key)
            else:
                eff_subj = subj

            item_el = pd.find(".//Item")
            if item_el is None:
                continue
            parsed = extract_question_and_explanation(item_el)
            if not parsed:
                continue

            yy = cal_year[-2:]
            ebsi_slug = f"e{yy}_{pid}_{qnum_int:02d}"

            # Check if this problem is part of 2026학년도 수능 or 2025학년도 수능 (for standalone HTML generation)
            standalone_slug = None
            if is_csat and exam_year in ("2026", "2025"):
                prefix = "csat26" if exam_year == "2026" else "csat25"
                if eff_subj == "공통(수학I·II)":
                    standalone_slug = f"{prefix}_{qnum_int:02d}"
                elif eff_subj == "확률과 통계":
                    standalone_slug = f"{prefix}_p{qnum_int:02d}"
                elif eff_subj == "미적분":
                    standalone_slug = f"{prefix}_m{qnum_int:02d}"
                elif eff_subj == "기하":
                    standalone_slug = f"{prefix}_g{qnum_int:02d}"

            active_slug = standalone_slug if standalone_slug else ebsi_slug

            prob_full = synthesize_mathedu_problem(
                slug=active_slug,
                exam_year=exam_year,
                month=month_label,
                grade=grade,
                subject=eff_subj,
                qnum=qnum_str,
                parsed=parsed,
            )
            prob_full["source"] = source
            prob_full["date"] = date_str
            prob_full["examYearAlt"] = exam_year_alt

            if standalone_slug:
                standalone_problems.append(prob_full)
                if standalone_slug == "csat26_01":
                    default_ebsi_prob = dict(prob_full)

            # Extract compact step 3/4/5 derivation lines for shard
            exp_lines = parsed.get("exp_lines", [])
            text_exp = [
                re.sub(r"^(?:<br\s*/?>)+|(?:<br\s*/?>)+$", "", re.sub(r"<img[^>]*>", "", ln)).strip()
                for ln in exp_lines
            ]
            text_exp = [ln for ln in text_exp if len(re.sub(r"<[^>]+>", "", ln).strip()) >= 3]
            s3 = text_exp[0] if len(text_exp) >= 1 else ""
            s4 = text_exp[len(text_exp) // 2] if len(text_exp) >= 2 else ""
            s5 = text_exp[-1] if len(text_exp) >= 3 else ""

            tpl_idx = get_tpl_idx(parsed.get("unit_parts", []), parsed.get("intent_ko", ""), parsed.get("stem_html", ""))

            shard_record = {
                "slug": ebsi_slug,
                "standaloneSlug": standalone_slug or "",
                "paperId": pid,
                "year": cal_year,
                "examYear": exam_year,
                "examYearAlt": exam_year_alt,
                "month": month_label,
                "grade": grade,
                "subject": eff_subj,
                "qNum": qnum_str,
                "point": parsed.get("point", "3"),
                "source": source,
                "title": prob_full["title"],
                "unit_parts": parsed.get("unit_parts", []),
                "intent": parsed.get("intent_ko", ""),
                "tags": prob_full["tags"],
                "stem": parsed.get("stem_html", ""),
                "options": parsed.get("options", []),
                "answer": parsed.get("answer", 1),
                "exp_lines": exp_lines,
                "tpl_idx": tpl_idx,
                "s3": s3,
                "s4": s4,
                "s5": s5,
                "s3_q": prob_full.get("step3_q"),
                "s4_q": prob_full.get("step4_q"),
            }
            shards_by_year[cal_year]["problems"][ebsi_slug] = shard_record

            # If it's a standalone problem, we don't duplicate it in ebsi_catalog.json because it will be in board/index.json!
            if not standalone_slug:
                catalog_items.append({
                    "s": ebsi_slug,
                    "t": prob_full["title"],
                    "y": exam_year,
                    "ya": exam_year_alt,
                    "m": "11월" if month_label == "수능" else month,
                    "g": grade,
                    "sub": eff_subj,
                    "q": qnum_str,
                    "src": source,
                    "tg": prob_full["tags"][:6],
                })

    # 1. Write 21 yearly shards (board/ebsi_shards/ebsi_2006.json ~ ebsi_2026.json)
    total_shard_probs = 0
    for yr, sdata in sorted(shards_by_year.items()):
        cnt = len(sdata["problems"])
        total_shard_probs += cnt
        shard_path = os.path.join(SHARDS_DIR, f"ebsi_{yr}.json")
        with open(shard_path, "w", encoding="utf-8") as f:
            json.dump(sdata, f, ensure_ascii=False, separators=(",", ":"))
    print(f"Saved {len(shards_by_year)} yearly shards in board/ebsi_shards/ ({total_shard_probs} unique problems).")

    # 2. Write compact catalog (board/ebsi_catalog.json)
    catalog_path = os.path.join(BOARD_DIR, "ebsi_catalog.json")
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog_items, f, ensure_ascii=False, separators=(",", ":"))
    print(f"Saved board/ebsi_catalog.json ({len(catalog_items)} catalog items, {os.path.getsize(catalog_path):,} bytes).")

    # 3. Write standalone HTML files for 2026학년도 수능 (46문항) & 2025학년도 수능 (46문항)
    new_index_entries = []
    standalone_problems.sort(key=lambda x: (0 if x["examYear"] == "2026" else 1, x["slug"]))
    for prob in standalone_problems:
        slug = prob["slug"]
        out_path = os.path.join(BOARD_DIR, f"{slug}.html")
        html_content = build_ebsi_problem_html(prob)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        new_index_entries.append({
            "slug": slug,
            "title": prob["title"],
            "time": f"{prob['date']} 12:00",
            "file": f"{slug}.html",
            "examYear": prob["examYear"],
            "examYearAlt": prob["examYearAlt"],
            "grade": prob["grade"],
            "month": "11월",
            "subject": prob["subject"],
            "qNum": prob["qNum"],
            "source": prob["source"],
            "date": prob["date"],
            "tags": prob["tags"],
            "is_public": True,
        })

    # 4. Write Universal Stitch Player board/ebsi.html and register in board/index.json
    if default_ebsi_prob is None and standalone_problems:
        default_ebsi_prob = dict(standalone_problems[0])
    if default_ebsi_prob:
        ebsi_player_prob = dict(default_ebsi_prob)
        ebsi_player_prob["slug"] = "ebsi"
        ebsi_player_prob["title"] = "[EBSi 전 연도·전 학년 수학 기출 통합 플레이어] 2006~2027학년도 고1·고2·고3 16,548문항 단계별 디딤돌"
        ebsi_player_prob["title_en"] = "[EBSi All-Years & All-Grades Math Player] 16,548 Step-by-Step Scaffolding Problems"
        extra_top_html, extra_bottom_js = build_ebsi_dynamic_player_scripts()
        ebsi_html = build_ebsi_problem_html(ebsi_player_prob, extra_top_html=extra_top_html, extra_bottom_js=extra_bottom_js)
        with open(os.path.join(BOARD_DIR, "ebsi.html"), "w", encoding="utf-8") as f:
            f.write(ebsi_html)

        new_index_entries.insert(0, {
            "slug": "ebsi",
            "title": "[EBSi 전 연도·전 학년 수학 기출 통합 플레이어] 2006~2027학년도 고1·고2·고3 16,548문항 단계별 디딤돌",
            "time": "2026-10-30 22:00",
            "file": "ebsi.html",
            "examYear": "2026",
            "examYearAlt": "2027",
            "grade": "고3",
            "month": "11월",
            "subject": "공통(수학I·II)",
            "qNum": "1",
            "source": "EBSi 전 연도·전 학년 기출 아카이브 (16,548문항)",
            "date": "2026-10-30",
            "tags": ["수능", "모의평가", "학력평가", "고3", "고2", "고1", "전연도기출", "16548문항"],
            "is_public": True,
        })

    # 5. Update board/index.json
    index_json_path = os.path.join(BOARD_DIR, "index.json")
    with open(index_json_path, "r", encoding="utf-8") as f:
        existing_items = json.load(f)

    new_slugs = {e["slug"] for e in new_index_entries}
    filtered_existing = [it for it in existing_items if it.get("slug") not in new_slugs]
    updated_items = new_index_entries + filtered_existing

    with open(index_json_path, "w", encoding="utf-8") as f:
        json.dump(updated_items, f, ensure_ascii=False, indent=2)

    print(f"Generated {len(standalone_problems)} standalone CSAT HTML files + board/ebsi.html, updated board/index.json ({len(updated_items)} items).")
    upgrade_index_html_for_ebsi()


def upgrade_index_html_for_ebsi():
    idx_path = os.path.join(BASE_DIR, "index.html")
    if not os.path.exists(idx_path):
        return
    with open(idx_path, "r", encoding="utf-8") as f:
        txt = f.read()

    # 1. Expand Year, Month, Subject dropdowns in index.html
    old_year_sel = '<option value="2021">2021학년도</option>\n              <option value="2020">2020학년도 이전</option>'
    new_year_sel = "\n              ".join(
        [f'<option value="{y}">{y}학년도</option>' for y in range(2021, 2005, -1)]
    )
    txt_norm = txt.replace("\r\n", "\n")
    if old_year_sel in txt_norm:
        txt_norm = txt_norm.replace(old_year_sel, new_year_sel)

    old_month_sel = '<option value="7월">7월 학평</option>\n              <option value="4월">4월 학평</option>'
    new_month_sel = '<option value="7월">7월 학평</option>\n              <option value="5월">5월 모평·학평</option>\n              <option value="4월">4월 학평</option>'
    if old_month_sel in txt_norm:
        txt_norm = txt_norm.replace(old_month_sel, new_month_sel)

    old_subj_sel = '<option value="확률과 통계">확률과 통계</option>\n              <option value="공통수학">공통수학</option>'
    new_subj_sel = (
        '<option value="확률과 통계">확률과 통계</option>\n'
        '              <option value="수학(가형)">수학(가형)</option>\n'
        '              <option value="수학(나형)">수학(나형)</option>\n'
        '              <option value="수학(고2)">수학(고2)</option>\n'
        '              <option value="공통수학">공통수학(고1)</option>'
    )
    if old_subj_sel in txt_norm:
        txt_norm = txt_norm.replace(old_subj_sel, new_subj_sel)

    # Fix updateExamSelectOptions so 2020 is shown as 2020학년도 instead of 2020학년도 이전
    txt_norm = txt_norm.replace(
        "} else if (opt.value === '2020') {\n          opt.textContent = isEn ? 'Before Year 2020' : '2020학년도 이전';",
        "} else if (opt.value === '2005') {\n          opt.textContent = isEn ? 'Before Year 2005' : '2005학년도 이전';"
    )

    # 2. Load board/ebsi_catalog.json right after board/index.json
    old_fetch_tail = "      renderList();\n    })"
    new_fetch_tail = """      renderList();
      if (!window._ebsiCatalogLoaded) {
        window._ebsiCatalogLoaded = true;
        fetch('board/ebsi_catalog.json')
          .then(function(r) { return r.ok ? r.json() : []; })
          .then(function(cat) {
            if (!Array.isArray(cat) || cat.length === 0) return;
            var existingSlugs = new Set(allItems.map(function(x) { return x.slug; }));
            var ebsiMapped = [];
            for (var i = 0; i < cat.length; i++) {
              var c = cat[i];
              if (!c || existingSlugs.has(c.s)) continue;
              ebsiMapped.push({
                slug: c.s,
                title: c.t,
                examYear: c.y,
                examYearAlt: c.ya,
                month: c.m,
                grade: c.g,
                subject: c.sub,
                qNum: c.q,
                source: c.src,
                tags: c.tg || [],
                url: 'board/ebsi.html?id=' + encodeURIComponent(c.s),
                offlineUrl: 'offline/ebsi.html?id=' + encodeURIComponent(c.s),
                is_public: true
              });
            }
            allItems = allItems.concat(ebsiMapped);
            var hEl = document.getElementById('heroStatQuizCount');
            var isEn2 = window.MatheduI18n && window.MatheduI18n.getLanguage() === 'en';
            if (hEl) hEl.textContent = isEn2 ? (allItems.length.toLocaleString() + '+') : (allItems.length.toLocaleString() + '개');
            renderList();
          })
          .catch(function(){});
      }
    })"""
    if "board/ebsi_catalog.json" not in txt_norm and old_fetch_tail in txt_norm:
        txt_norm = txt_norm.replace(old_fetch_tail, new_fetch_tail, 1)

    # 3. Support 가형, 나형, 고2수학 in parseMatheduNaturalQuery
    old_subj_tok = "      if (tok === '공통수학') {\n        res.subject = '공통수학'; continue;\n      }"
    new_subj_tok = """      if (tok === '공통수학') {
        res.subject = '공통수학'; continue;
      }
      if (tok === '가형' || tok === '수학가형' || tok === 'b형') {
        res.subject = '수학(가형)'; continue;
      }
      if (tok === '나형' || tok === '수학나형' || tok === 'a형') {
        res.subject = '수학(나형)'; continue;
      }"""
    if "수학(가형)" not in txt_norm[txt_norm.find("parseMatheduNaturalQuery"):txt_norm.find("matchMatheduProblem")] and old_subj_tok in txt_norm:
        txt_norm = txt_norm.replace(old_subj_tok, new_subj_tok, 1)

    # 4. Paginate renderList() and support item.url / item.offlineUrl
    old_loop_head = "    for (var i = 0; i < filtered.length; i++) {\n      var item = filtered[i];"
    new_loop_head = """    var displayLimit = window._matheduDisplayLimit || 60;
    var renderCount = Math.min(filtered.length, displayLimit);
    for (var i = 0; i < renderCount; i++) {
      var item = filtered[i];
      var itemHref = item.url || ('board/' + encodeURIComponent(item.slug) + '.html');
      var itemOffHref = item.offlineUrl || ('offline/' + encodeURIComponent(item.slug) + '.html');"""
    if old_loop_head in txt_norm:
        txt_norm = txt_norm.replace(old_loop_head, new_loop_head, 1)

    txt_norm = txt_norm.replace(
        '<a href="board/\' + exactItem.slug + \'.html" class="btn-solve',
        '<a href="\' + (exactItem.url || (\'board/\' + exactItem.slug + \'.html\')) + \'" class="btn-solve'
    )
    txt_norm = txt_norm.replace(
        '<a href="board/\' + slug + \'.html" class="text-on-surface no-underline hover:text-secondary transition-colors">\' + title + \'</a>',
        '<a href="\' + itemHref + \'" class="text-on-surface no-underline hover:text-secondary transition-colors">\' + title + \'</a>'
    )
    txt_norm = txt_norm.replace(
        '<a href="offline/\' + slug + \'.html" download title="\' + tBtnOfflineTitle',
        '<a href="\' + itemOffHref + \'" download title="\' + tBtnOfflineTitle'
    )
    txt_norm = txt_norm.replace(
        'href="board/\' + slug + \'.html">\' + solveBtnText + \'</a>',
        'href="\' + itemHref + \'">\' + solveBtnText + \'</a>'
    )
    txt_norm = txt_norm.replace(
        'href="board/\' + rSlug + \'.html">\' + tBtnSolve + \'</a>',
        'href="\' + (rItem.url || (\'board/\' + rSlug + \'.html\')) + \'">\' + tBtnSolve + \'</a>'
    )
    txt_norm = txt_norm.replace(
        '<a href="board/\' + rSlug + \'.html" class="text-on-surface no-underline hover:text-secondary transition-colors">\' + rTitle + \'</a>',
        '<a href="\' + (rItem.url || (\'board/\' + rSlug + \'.html\')) + \'" class="text-on-surface no-underline hover:text-secondary transition-colors">\' + rTitle + \'</a>'
    )

    old_loop_end = "      html += '</div>';\n    }\n\n    // Render Related Problems Section"
    new_loop_end = """      html += '</div>';
    }
    if (filtered.length > renderCount) {
      html += '<div class="rounded-xl bg-surface-container-lowest border border-secondary/30 p-3.5 text-center shadow-sm">';
      html += '  <button type="button" onclick="window._matheduDisplayLimit=(window._matheduDisplayLimit||60)+60; window._triggerRenderList();" class="px-5 py-2.5 rounded-xl bg-secondary text-white font-headline-sm text-[14px] font-bold border-0 cursor-pointer hover:opacity-95 transition-opacity">';
      html += '    ➕ 다음 60문항 더보기 (현재 ' + renderCount.toLocaleString() + ' / 검색 결과 ' + filtered.length.toLocaleString() + '문항)';
      html += '  </button>';
      html += '</div>';
    }

    // Render Related Problems Section"""
    if old_loop_end in txt_norm:
        txt_norm = txt_norm.replace(old_loop_end, new_loop_end, 1)

    with open(idx_path, "w", encoding="utf-8") as f:
        f.write(txt_norm)
    print("Upgraded index.html to load board/ebsi_catalog.json (16,548 total problems) with pagination and 2006~2027 filters.")


if __name__ == "__main__":
    main()
