#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_csat2027_all.py
===============================================================================
2027학년도 대학수학능력시험 수학 영역 전 문항 (46문항) 인터랙티브 디딤돌 빌더
- 원문 PDF: https://cdn.kice.re.kr/27dae-suneung/27DaeSuneung_2.pdf
- 공식 정답표: https://cdn2.kice.re.kr/27dae-suneung/27DaeSuneung_2a.pdf
- 구성:
  * 공통 1~22번 (csat27_01 ~ csat27_22)
  * 확률과 통계 23~30번 (csat27_p23 ~ csat27_p30)
  * 미적분 23~30번 (csat27_m23 ~ csat27_m30)
  * 기하 23~30번 (csat27_g23 ~ csat27_g30)
===============================================================================
"""

import html
import json
import os
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

import silent_subprocess  # noqa: F401
import min7014_matcher
import stitch_screen_builder
from visual_diagram_engine import build_visual_and_schematic_block

from csat2027_part1_common1 import PART1_PROBLEMS
from csat2027_part2_common2 import PART2_PROBLEMS
from csat2027_part3_prob import PART3_PROBLEMS
from csat2027_part4_calc import PART4_PROBLEMS
from csat2027_part5_geom import PART5_PROBLEMS

BOARD_DIR = BASE_DIR / "board"
MANIFEST_PATH = BASE_DIR / "assets" / "csat2027_manifest.json"

# 한국교육과정평가원(KICE) 2027학년도 수능 수학 홀수형 공식 정답표 (100% 대조 검증용)
OFFICIAL_KICE_ANSWERS = {
    # 공통 1~22
    "csat27_01": ("mc", 2, "②"),
    "csat27_02": ("mc", 5, "⑤"),
    "csat27_03": ("mc", 3, "③"),
    "csat27_04": ("mc", 4, "④"),
    "csat27_05": ("mc", 1, "①"),
    "csat27_06": ("mc", 1, "①"),
    "csat27_07": ("mc", 2, "②"),
    "csat27_08": ("mc", 3, "③"),
    "csat27_09": ("mc", 4, "④"),
    "csat27_10": ("mc", 2, "②"),
    "csat27_11": ("mc", 5, "⑤"),
    "csat27_12": ("mc", 3, "③"),
    "csat27_13": ("mc", 2, "②"),
    "csat27_14": ("mc", 4, "④"),
    "csat27_15": ("mc", 3, "③"),
    "csat27_16": ("sa", "2", "2"),
    "csat27_17": ("sa", "20", "20"),
    "csat27_18": ("sa", "5", "5"),
    "csat27_19": ("sa", "31", "31"),
    "csat27_20": ("sa", "169", "169"),
    "csat27_21": ("sa", "135", "135"),
    "csat27_22": ("sa", "98", "98"),
    # 확률과 통계 23~30
    "csat27_p23": ("mc", 3, "③"),
    "csat27_p24": ("mc", 2, "②"),
    "csat27_p25": ("mc", 5, "⑤"),
    "csat27_p26": ("mc", 5, "⑤"),
    "csat27_p27": ("mc", 1, "①"),
    "csat27_p28": ("mc", 3, "③"),
    "csat27_p29": ("sa", "41", "41"),
    "csat27_p30": ("sa", "15", "15"),
    # 미적분 23~30
    "csat27_m23": ("mc", 1, "①"),
    "csat27_m24": ("mc", 4, "④"),
    "csat27_m25": ("mc", 1, "①"),
    "csat27_m26": ("mc", 5, "⑤"),
    "csat27_m27": ("mc", 3, "③"),
    "csat27_m28": ("mc", 4, "④"),
    "csat27_m29": ("sa", "12", "12"),
    "csat27_m30": ("sa", "75", "75"),
    # 기하 23~30
    "csat27_g23": ("mc", 3, "③"),
    "csat27_g24": ("mc", 4, "④"),
    "csat27_g25": ("mc", 3, "③"),
    "csat27_g26": ("mc", 5, "⑤"),
    "csat27_g27": ("mc", 1, "①"),
    "csat27_g28": ("mc", 4, "④"),
    "csat27_g29": ("sa", "45", "45"),
    "csat27_g30": ("sa", "223", "223"),
}

CIRCLED_NUMS = ["①", "②", "③", "④", "⑤"]

ref_html = (BOARD_DIR / "csat26_01.html").read_text(encoding="utf-8")
style_match = re.search(r"<style>(.*?)</style>", ref_html, re.DOTALL)
COMMON_STYLE = style_match.group(1) if style_match else ""


def render_md_inline(s: str) -> str:
    if not s:
        return ""
    s = re.sub(r"\*\*([^*<\n]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"`([^`<\n]+)`", r"<code>\1</code>", s)
    return s


def extract_clean_qnum(raw_qnum: str) -> str:
    m = re.search(r"(\d+)", str(raw_qnum))
    return m.group(1) if m else str(raw_qnum)


def verify_official_answer(prob: dict) -> str:
    slug = prob["slug"]
    assert slug in OFFICIAL_KICE_ANSWERS, f"Unknown slug {slug}"
    kind, expected, disp = OFFICIAL_KICE_ANSWERS[slug]
    fin = prob["final"]
    ans_idx = int(fin["answer"])
    opts = fin["options"]
    assert len(opts) == 5, f"{slug}: final must have 5 options, got {len(opts)}"
    assert len(set(opts)) == 5, f"{slug}: duplicate options in final: {opts}"
    assert 1 <= ans_idx <= 5, f"{slug}: invalid answer index {ans_idx}"
    if kind == "mc":
        assert ans_idx == expected, f"{slug}: KICE answer is {expected}, got {ans_idx}!"
    else:
        chosen = opts[ans_idx - 1].replace("$", "").strip()
        assert chosen == expected, f"{slug}: KICE short answer is {expected}, got '{chosen}' in options {opts}!"

    # Also verify all scaffolding steps have 5 distinct options and valid 1..5 answer
    levels = prob.get("levels", [])
    assert len(levels) >= 5, f"{slug}: must have >= 5 scaffolding steps, got {len(levels)}"
    first_lbl = levels[0]["questions"][0].get("level_label", "")
    assert "초등" in first_lbl, f"{slug}: Step 1 level_label must contain '초등', got '{first_lbl}'"
    for s_i, lv in enumerate(levels, 1):
        for q in lv.get("questions", []):
            q_opts = q.get("options", [])
            q_ans = int(q.get("answer", 0))
            assert len(q_opts) == 5 and len(set(q_opts)) == 5, f"{slug} step {s_i}: invalid options {q_opts}"
            assert 1 <= q_ans <= 5, f"{slug} step {s_i}: invalid answer {q_ans}"
    return disp


def build_question_block(
    q_data: dict,
    is_final: bool = False,
    step_idx: int = 0,
    know_ko: str = "",
    know_en: str = "",
    sol_ko: str = "",
    sol_en: str = "",
) -> str:
    ans = int(q_data["answer"])
    raw_exp_ko = render_md_inline(q_data.get("exp", ""))
    raw_exp_en = render_md_inline(q_data.get("exp_en", ""))

    if is_final:
        if sol_ko:
            raw_exp_ko = (
                f"<b>📌 [최종 본문항 핵심 요약]</b><br>{raw_exp_ko}"
                f'<hr style="border:none;border-top:1px dashed rgba(0,99,152,.28);margin:12px 0">'
                f"{sol_ko}"
            )
        if sol_en:
            raw_exp_en = (
                f"<b>📌 [Final Problem Core Summary]</b><br>{raw_exp_en}"
                f'<hr style="border:none;border-top:1px dashed rgba(0,99,152,.28);margin:12px 0">'
                f"{sol_en}"
            )
    else:
        if know_ko and know_ko not in raw_exp_ko:
            raw_exp_ko = (
                f"<b>✅ [제{step_idx}단계 정답 및 핵심 해설]</b><br>{raw_exp_ko}"
                f"<br><br><b>📖 [제{step_idx}단계 핵심 원리 및 유도 과정]</b><br>{know_ko}"
            )
        if know_en and know_en not in raw_exp_en:
            raw_exp_en = (
                f"<b>✅ [Step {step_idx} Answer &amp; Explanation]</b><br>{raw_exp_en}"
                f"<br><br><b>📖 [Step {step_idx} Core Principle &amp; Derivation]</b><br>{know_en}"
            )

    exp_ko = html.escape(raw_exp_ko, quote=True)
    exp_en = html.escape(raw_exp_en, quote=True)
    lvl_ko = q_data.get("level_label", "최종 본문항" if is_final else "디딤돌 문제")
    lvl_en = q_data.get("level_label_en", "Final Exam Problem" if is_final else "Scaffolding Step")
    stem_ko = render_md_inline(q_data["stem"])
    stem_en = render_md_inline(q_data.get("stem_en", ""))
    options = q_data["options"]

    max_opt_len = max(len(o) for o in options) if options else 0
    opts_cls = "opts opts-inline" if (is_final and max_opt_len <= 28) else "opts"

    opts_html = ""
    for idx, opt_text in enumerate(options, 1):
        opts_html += f'<div class="opt"><span class="n">{idx}</span><span class="opt-txt">{render_md_inline(opt_text)}</span></div>'

    stem_en_div = f'<div class="bilingual-en">{stem_en}</div>' if stem_en else ""

    return f"""<div class="q" data-ans="{ans}" data-exp="{exp_ko}" data-exp-en="{exp_en}"><div class="lvl"><span class="bilingual-ko">{lvl_ko}</span><span class="bilingual-en">{lvl_en}</span></div><div class="stem"><span class="bilingual-ko">{stem_ko}</span>{stem_en_div}</div><div class="{opts_cls}">{opts_html}</div><div class="q-actions" style="margin-top:10px;display:flex;justify-content:flex-end"><button type="button" class="exp-toggle-btn" onclick="toggleExp(this)">💡 해설 보기</button></div><div class="exp"></div><div class="report-wrap" style="margin-top:10px;border-top:1px solid #e4e2e4;padding-top:10px">
<button class="report-btn" onclick="toggleReport(this)" style="background:transparent;color:#64748b;border:1px solid #cbd5e1;border-radius:8px;padding:4px 12px;font-size:.75rem;cursor:pointer;transition:.15s" onmouseover="this.style.borderColor='#ff6b6b';this.style.color='#ff6b6b'" onmouseout="this.style.borderColor='#cbd5e1';this.style.color='#64748b'">🚨 이 문제에 이상이 있어요</button>
<div class="report-form" style="display:none;margin-top:10px;text-align:left">
<div style="color:#64748b;font-size:.75rem;margin-bottom:6px">어떤 부분이 이상한가요? 자세히 적어주세요.</div>
<textarea class="report-text" rows="3" placeholder="예: 보기 3번이 정답이 아닌 것 같습니다. / 문제의 조건이 모호합니다. / 계산 오류가 있습니다." style="width:100%;background:#ffffff;color:#1b1b1d;border:1px solid #c5c6cd;border-radius:8px;padding:8px;font-size:.85rem;resize:vertical;box-sizing:border-box"></textarea>
<div style="display:flex;gap:6px;margin-top:6px;justify-content:flex-end">
<button class="report-cancel" onclick="toggleReport(this)" style="background:transparent;color:#64748b;border:1px solid #cbd5e1;border-radius:8px;padding:4px 10px;font-size:.75rem;cursor:pointer">취소</button>
<button class="report-submit" onclick="submitReport(this)" style="background:linear-gradient(90deg,#ff6b6b,#ee5a5a);color:#fff;border:none;border-radius:8px;padding:4px 12px;font-size:.75rem;cursor:pointer">신고 접수</button>
</div>
</div>
<div class="report-msg" style="display:none;color:#3ddc97;font-size:.75rem;margin-top:6px;text-align:right">✅ 신고가 접수되었어요. 확인 후 고칠게요!</div>
</div></div>"""


def build_orig_paper_box(prob: dict, qnum_clean: str) -> str:
    subject = prob["subject"]
    pts = prob.get("points", 4)
    is_sa = bool(prob.get("is_short_answer", False))
    fin = prob["final"]
    stem_ko = render_md_inline(fin["stem"])
    stem_en = render_md_inline(fin.get("stem_en", ""))
    orig_svg = (prob.get("orig_svg") or "").strip()

    svg_block = (
        f'<div style="margin:12px auto;text-align:center">{orig_svg}</div>'
        if orig_svg
        else ""
    )

    if is_sa:
        opts_row = (
            '<p id="examOrigOptsContent" style="margin:0;padding-top:10px;border-top:1px dashed #cbd5e1;font-size:0.86rem;color:#475569;font-weight:700">'
            '<span class="bilingual-ko">✏️ [단답형 주관식 문항] · 아래 디딤돌 퀴즈에서는 직접 수식을 입력하거나 선택지로 검산할 수 있습니다.</span>'
            '<span class="bilingual-en">✏️ [Short-Answer Official Item] · Solve directly with constructive input or verify via choices below.</span>'
            '</p>'
        )
    else:
        spans = []
        for idx, opt_t in enumerate(fin["options"]):
            spans.append(
                f'<span style="display:inline-block;margin:3px 8px 3px 0;font-weight:600;color:#1e293b">{CIRCLED_NUMS[idx]} {render_md_inline(opt_t)}</span>'
            )
        opts_row = (
            f'<p id="examOrigOptsContent" style="margin:0;padding-top:10px;border-top:1px dashed #cbd5e1;font-size:0.92rem;line-height:1.7">'
            + " &nbsp;&nbsp; ".join(spans)
            + "</p>"
        )

    en_stem_div = f'<div class="bilingual-en" style="margin-top:8px;color:#334155;font-size:0.92rem">{stem_en}</div>' if stem_en else ""

    return (
        f'<section id="examOrigPaperBox" style="width:100%;text-align:left;padding:18px 20px;background:#ffffff;border:1.5px solid #cbd5e1;border-radius:12px;color:#1b1b1d;line-height:1.8;font-size:0.96rem;box-shadow:inset 0 1px 4px rgba(15,23,42,0.04)">'
        f'<p style="margin:0 0 10px;padding-bottom:8px;border-bottom:1.5px solid #0f172a;display:flex;justify-content:space-between;align-items:center;font-weight:800;font-size:0.86rem;color:#0f172a;gap:8px;flex-wrap:wrap">'
        f'<span>📄 2027학년도 대학수학능력시험 · {subject}</span>'
        f'<span style="background:#0f172a;color:#ffffff;padding:2px 10px;border-radius:999px;font-size:0.78rem">문항 {qnum_clean}번 · {pts}점</span>'
        f'</p>'
        f'<div id="examOrigStemContent" style="margin:0 0 14px;color:#111827;font-size:0.97rem;line-height:1.85"><span class="bilingual-ko">{stem_ko}</span>{en_stem_div}</div>'
        f'{svg_block}'
        f'{opts_row}'
        f'</section>'
    )


def build_problem_html(prob: dict) -> tuple[str, list[dict]]:
    slug = prob["slug"]
    qnum_clean = extract_clean_qnum(prob["qNum"])
    subject = prob["subject"]
    title_ko = prob["title"]
    title_en = prob.get("title_en", title_ko)
    summary_ko = prob.get("summary_ko", title_ko)
    summary_en = prob.get("summary_en", title_en)
    tags = prob.get("tags", [subject, f"{qnum_clean}번"])
    clean_topic_ko = re.sub(r"^\[.*?\]\s*", "", title_ko).strip()

    subj_en_map = {
        "공통(수학I·II)": "Common (Math I·II)",
        "확률과 통계": "Prob & Stat",
        "미적분": "Calculus",
        "기하": "Geometry",
    }
    subj_en = subj_en_map.get(subject, subject)
    if subject == "공통(수학I·II)":
        badge_ko = f"2027학년도 수능 고3 공통 {qnum_clean}번"
    else:
        badge_ko = f"2027학년도 수능 고3 {subject} {qnum_clean}번"
    badge_en = f"2027 CSAT Math {subj_en} #{qnum_clean}"

    search_query = f"{title_ko} {summary_ko} {' '.join(tags)}"
    matched_materials = min7014_matcher.match_materials_for_problem(slug, search_query, limit=4)
    visual_tip_ko = min7014_matcher.get_visual_tip(search_query, matched_materials)
    addon_card_html = min7014_matcher.generate_addon_card_html(matched_materials, search_query)

    sym_items_html = ""
    for s in prob.get("symbols", []):
        sym_l = s["sym"]
        desc_ko = render_md_inline(s["desc"])
        desc_en = render_md_inline(s.get("desc_en", ""))
        en_div = f'<div class="bilingual-en">{desc_en}</div>' if desc_en else ""
        sym_items_html += f'<div><b>{sym_l}</b> — {desc_ko}{en_div}</div>'

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
    final_ans_display = (
        final_data["options"][ans_idx]
        if 0 <= ans_idx < len(final_data["options"])
        else str(final_data["answer"])
    )

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

    if len(sol_en.strip()) < 150:
        sol_en += "\n<p>💡 <b>Key Takeaway</b>: Follow each micro-scaffolding step from elementary foundations to complete the rigorous mathematical proof.</p>"

    sol_ko += min7014_matcher.build_solution_material_links_html(matched_materials, lang="ko")
    sol_en += min7014_matcher.build_solution_material_links_html(matched_materials, lang="en")

    final_q_block = build_question_block(
        final_data,
        is_final=True,
        step_idx=len(levels_list) + 1,
        sol_ko=sol_ko,
        sol_en=sol_en,
    )

    orig_paper_box = build_orig_paper_box(prob, qnum_clean)

    meta_desc = html.escape(
        f"2027학년도 대학수학능력시험 고3 {subject} {qnum_clean}번 · {title_ko}. 초등학생도 풀 수 있는 단계별 디딤돌 퀴즈 및 시각적 도식화 해설.",
        quote=True,
    )
    meta_kw = html.escape(
        f"2027학년도 대학수학능력시험, 2027 수능 수학, 고3 수학 {qnum_clean}번, {title_ko}, {subject}, {', '.join(tags)}, 디딤돌 퀴즈, GeoGebra, 수학자료실, mathedu",
        quote=True,
    )

    seo_schema = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": ["Quiz", "LearningResource"],
            "@id": f"https://min7014.github.io/mathedu/board/{slug}.html",
            "name": f"{title_ko} · mathedu 수학자료실",
            "description": f"2027학년도 대학수학능력시험 수학 영역 {subject} {qnum_clean}번 단계별 디딤돌 퀴즈 및 시각 증명 해설",
            "url": f"https://min7014.github.io/mathedu/board/{slug}.html",
            "isAccessibleForFree": True,
            "inLanguage": ["ko", "en"],
            "learningResourceType": ["Quiz", "Interactive Step-by-Step Problem", "Visual Proof"],
            "educationalLevel": ["Elementary School", "Middle School", "High School"],
            "assesses": f"2027학년도 대학수학능력시험 수학 {subject} {qnum_clean}번",
            "teaches": subject,
            "author": {"@type": "Organization", "name": "mathedu · 수학자료실 (min7014)", "url": "https://min7014.github.io/mathedu/"},
        },
        ensure_ascii=False,
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
<script type="application/ld+json" id="mathedu-seo-schema">{seo_schema}</script>
<style>
{COMMON_STYLE}
</style>
<script>window.MathJax={{tex:{{inlineMath:[['$','$'],['\\\\(','\\\\)']]}}}};</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml-full.js"></script>
<script src="../mathedu-i18n.js?v=20261119_csat27"></script>
</head><body><div class="wrap">
<div class="topbar">
<a class="tbtn brand-btn" href="/mathedu/" style="display:inline-flex;align-items:center;gap:8px">
<img src="../assets/favicon.png" alt="mathedu" style="width:20px;height:20px;border-radius:5px;background:#fff;padding:1px">
<span><b>mathedu</b></span>
</a>
<a class="tbtn" href="../csat2027.html" style="font-weight:800;color:#006398">🎯 2027 수능 전 문항 특별관</a>
<button class="tbtn" id="copyBtn" onclick="copyLink()"><span class="bilingual-ko">🔗 링크 복사</span><span class="bilingual-en">🔗 Copy Link</span></button>
<div class="lang-group">
  <button type="button" class="lang-btn active" data-lang-btn="ko" onclick="setBoardLang('ko', true)">한국어</button>
  <button type="button" class="lang-btn" data-lang-btn="en" onclick="setBoardLang('en', true)">English (Bilingual)</button>
</div>
</div>
<div class="score"><span><span class="bilingual-ko">점수</span><span class="bilingual-en">Score</span> <b id="pts">0</b> / <b id="tot">0</b></span>
<span class="bar"><i id="bar"></i></span><span id="pct">0%</span></div>
<h1><span class="bilingual-ko">📘 {title_ko}</span><span class="bilingual-en">📘 {title_en}</span></h1>
<p class="lead">초등학생도 1단계부터 차근차근 따라가면 2027학년도 대학수학능력시험 본문항까지 스스로 풀 수 있는 100% 무료 단계별 디딤돌 퀴즈입니다.<span class="bilingual-en">Elementary-to-advanced step-by-step scaffolding quiz for the Official 2027 CSAT Math Exam.</span></p>
<!-- ★ 원본 문제 카드: 가로 2열 대조 배치 -->
<div class="orig-card">
  <div class="orig-header">
    <div class="orig-tag">📌 원본 문제 (오늘의 목표)<span class="bilingual-en">📌 Official 2027 CSAT Problem (Today's Goal)</span></div>
    <span class="orig-badge" id="examOrigBadge"><span class="bilingual-ko">{badge_ko}</span><span class="bilingual-en">{badge_en}</span></span>
  </div>

  <div class="orig-grid">
    <div class="orig-col-media">
      <div class="orig-media-frame">
        {orig_paper_box}
      </div>
      <div class="orig-media-sub" id="examOrigMediaSub"><span class="bilingual-ko">📄 2027학년도 대학수학능력시험 공식 기출문항 · <a href="../csat2027.html" style="color:#006398;font-weight:700">2027 수능 전체 46문항 보기 ➔</a></span><span class="bilingual-en">📄 Official 2027 CSAT Mathematics Paper · <a href="../csat2027.html" style="color:#006398;font-weight:700">View All 46 Problems ➔</a></span></div>
    </div>

    <div class="orig-col-desc">
      <div class="orig-text-box">
        <h4>📋 원본 문항 핵심 요약 및 목표<span class="bilingual-en">📋 Official Problem Summary &amp; Objectives</span></h4>
        <p id="examOrigTopicTitle" style="margin:0 0 8px;font-weight:600;color:var(--txt)">{clean_topic_ko}</p>
        <p id="examOrigSummaryKo" style="margin:0;font-size:0.88rem;color:var(--sub);line-height:1.6">{summary_ko}</p>
        <div class="bilingual-en" id="examOrigSummaryEn"><b>Problem Objective:</b> {summary_en}</div>
      </div>
      <div class="orig-tip">
        💡 <b>초등 눈높이 디딤돌 길잡이</b>: 처음 나오는 기호도 제0단계 기호 번역과 1단계 초등 기초 직관 디딤돌부터 순서대로 밟아가면 누구나 100% 자신의 힘으로 해결할 수 있습니다!<span class="bilingual-en">💡 <b>Core Guide</b>: Follow the elementary-grounded micro-steps below to master this problem completely!</span>
      </div>
    </div>
  </div>

  <div class="min-visual-tip" id="examVisualTipBox" style="margin-top:16px">
    {visual_tip_ko}
  <div class="bilingual-en">💡 <b>Frame-by-Frame Visual Proof Analysis (PDF &amp; GeoGebra Exploration)</b><br>The archive's flipbook proof materials demonstrate how fundamental mathematical principles converge smoothly frame by frame. Explore the interactive dynamic geometry applets below.</div></div>
</div>
<h2>🔰 제0단계 · 수학 기호 번역기<span class="bilingual-en">🔰 Step 0 · Mathematical Symbol Translator</span></h2><div class="sym" id="examSymContainer">{sym_items_html}</div>
<div id="examDynamicLevelsWrap">
{levels_html}
</div>
<div id="trackFull" style="position:fixed;inset:0;z-index:9999;display:none;flex-direction:column;align-items:center;justify-content:center;background:rgba(252,248,250,0.97);padding:24px;text-align:center"><h3 style="color:#131b2e;margin:0 0 6px;font-weight:800">📝 학습자 이름 등록 (선택)</h3><div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap"><input type="text" id="studentName" placeholder="이름 입력" style="background:#ffffff;color:#1b1b1d;border:1.5px solid #c5c6cd;border-radius:10px;padding:12px 16px;font-size:1.05rem;min-width:200px;text-align:center"><button class="btn" onclick="registerName()" style="font-size:1.05rem;padding:12px 24px"><span class="bilingual-ko">시작하기</span><span class="bilingual-en">Start</span></button></div></div>
<h2>🎯 최종 문제 + 상세 풀이<span class="bilingual-en">🎯 Final Official Exam Problem &amp; Complete Solution</span></h2><div class="sol" id="examSolContainer">
  <div class="bilingual-ko">
{sol_ko}
  </div>
  <div class="bilingual-en">
{sol_en}
  </div>
</div>{final_q_block}
{addon_card_html}
<div class="final"><p><span class="bilingual-ko">🎉 완료!</span><span class="bilingual-en">🎉 Completed!</span></p><div class="ans" id="finalAns">정답 {final_ans_display}</div>
<div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:10px"><button class="btn" onclick="location.reload()"><span class="bilingual-ko">다시 풀기</span><span class="bilingual-en">Try Again</span></button><a class="btn" href="../csat2027.html" style="text-decoration:none;display:inline-flex;align-items:center"><span class="bilingual-ko">🎯 2027 수능 전체 문항 목록 ➔</span><span class="bilingual-en">🎯 All 2027 CSAT Problems ➔</span></a></div></div>
</div><script>
window._studentName="";window._sheetsApiUrl="https://script.google.com/macros/s/AKfycbxQBW1hKYFSHokaVJMRql-UJpk0t4qMeWMiiy_RFuCLZ5SE4iZytYQkGa9_yoCmm1Ak0Q/exec";
function registerName(){{var n=document.getElementById("studentName").value.trim();if(!n)return;window._studentName=n;var tf=document.getElementById("trackFull");if(tf)tf.remove();sendProgress();}}
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
    if(window.MathJax&&window.MathJax.typesetPromise){{window.MathJax.typesetPromise([exp]).catch(function(){{}});}}
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
      if(exp){{exp.classList.add('show');if(window.MathJax&&window.MathJax.typesetPromise){{window.MathJax.typesetPromise([exp]).catch(function(){{}});}}}}
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
function copyLink(){{const b=document.getElementById('copyBtn');const t=b?b.textContent:'';
navigator.clipboard.writeText(location.href).then(()=>{{if(b){{b.textContent='✅ 복사됨';setTimeout(()=>b.textContent=t,1500);}}}})
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
  var slug='{slug}';
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
      }}
    }}
  }} catch(e){{ saved = 'ko'; }}
  setBoardLang(saved, false);
}})();
</script>
</body></html>"""
    return page_html, matched_materials


def main() -> None:
    all_problems = (
        PART1_PROBLEMS
        + PART2_PROBLEMS
        + PART3_PROBLEMS
        + PART4_PROBLEMS
        + PART5_PROBLEMS
    )
    assert len(all_problems) == 46, f"Expected 46 problems, got {len(all_problems)}"

    new_index_entries = []
    manifest_items = []

    for prob in all_problems:
        slug = prob["slug"]
        official_disp = verify_official_answer(prob)
        out_path = BOARD_DIR / f"{slug}.html"
        html_content, matched = build_problem_html(prob)
        out_path.write_text(html_content, encoding="utf-8")
        stitch_screen_builder.transform_file(str(out_path))

        qnum_clean = extract_clean_qnum(prob["qNum"])
        pts = int(prob.get("points", 4))
        is_sa = bool(prob.get("is_short_answer", False))
        ans_idx = int(prob["final"]["answer"]) - 1
        ans_val_tex = prob["final"]["options"][ans_idx]

        new_index_entries.append(
            {
                "slug": slug,
                "title": prob["title"],
                "title_en": prob.get("title_en", prob["title"]),
                "time": "2026-11-19 18:00",
                "file": f"{slug}.html",
                "examYear": "2027",
                "examYearAlt": "2026",
                "grade": "고3",
                "month": "11월",
                "subject": prob["subject"],
                "qNum": qnum_clean,
                "source": "2027학년도 대학수학능력시험",
                "date": "2026-11-19",
                "tags": prob.get("tags", [prob["subject"], "2027학년도 수능", f"{qnum_clean}번"]),
                "is_public": True,
            }
        )

        manifest_items.append(
            {
                "slug": slug,
                "qNum": int(qnum_clean),
                "subject": prob["subject"],
                "points": pts,
                "is_short_answer": is_sa,
                "official_answer": official_disp,
                "answer_value_tex": ans_val_tex,
                "title": prob["title"],
                "title_en": prob.get("title_en", prob["title"]),
                "summary_ko": prob.get("summary_ko", ""),
                "summary_en": prob.get("summary_en", ""),
                "tags": prob.get("tags", []),
                "proof_links": [
                    {
                        "id": m.get("id", ""),
                        "title": m.get("title", ""),
                        "category": m.get("category", ""),
                        "url": m.get("url", ""),
                        "pdf": min7014_matcher._clean_pdf_url(m.get("pdf", "")),
                        "geogebra": m.get("geogebra", ""),
                        "algeomath": min7014_matcher._clean_algeo_url(m.get("algeomath", "")),
                        "youtube": m.get("youtube", ""),
                    }
                    for m in (matched or [])[:3]
                ],
            }
        )

    # Update board/index.json (insert right after 'archive' so 2027 CSAT is featured first!)
    index_json_path = BOARD_DIR / "index.json"
    existing_items = json.loads(index_json_path.read_text(encoding="utf-8"))
    new_slugs = {e["slug"] for e in new_index_entries}
    filtered_existing = [it for it in existing_items if it.get("slug") not in new_slugs]

    if filtered_existing and filtered_existing[0].get("slug") == "archive":
        updated_items = [filtered_existing[0]] + new_index_entries + filtered_existing[1:]
    else:
        updated_items = new_index_entries + filtered_existing

    index_json_path.write_text(json.dumps(updated_items, ensure_ascii=False, indent=2), encoding="utf-8")

    manifest_doc = {
        "exam_title_ko": "2027학년도 대학수학능력시험 수학 영역",
        "exam_title_en": "2027 Academic Year College Scholastic Ability Test (CSAT) — Mathematics",
        "exam_date": "2026-11-19",
        "official_pdf_url": "https://cdn.kice.re.kr/27dae-suneung/27DaeSuneung_2.pdf",
        "official_answer_pdf_url": "https://cdn2.kice.re.kr/27dae-suneung/27DaeSuneung_2a.pdf",
        "total_problems": len(manifest_items),
        "items": manifest_items,
    }
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest_doc, ensure_ascii=False, indent=2), encoding="utf-8")

    print(
        f"✅ Built {len(all_problems)} Stitch-transformed 2027 CSAT HTML files in board/, "
        f"updated board/index.json ({len(updated_items)} items), and wrote {MANIFEST_PATH}!"
    )


if __name__ == "__main__":
    main()
