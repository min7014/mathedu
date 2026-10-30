# -*- coding: utf-8 -*-
"""
ebsi_lml_engine.py
==================
EBSi 기출문제 LML(XML) 파서 및 문항별 수식 추출 기반 5단계 디딤돌 퀴즈 · 도식화 풀이 생성 엔진
- 대상: EBSi 고3(D300), 고2(D200), 고1(D100) 전 연도(2006~2026) 수학 기출 전 문항 (608개 시험지, 16,428문항)
- 특징:
  1. 22개 세부 단원별 초등 눈높이 직관 디딤돌(1단계) 및 기호 번역 디딤돌(2단계) 탑재
  2. 각 문항의 실제 EBSi 공식 해설(<Explanation>) 수식($...$)에서 출발 식·중간 전개 식·최종 계산 식을 직접 추출하여
     빈칸 [ (가) ], [ (나) ], [ (다) ]를 추론하는 문항별 고유 수식 오지선다(3~5단계) 자동 생성
"""

import os
import re
import html
import hashlib
import xml.etree.ElementTree as ET

EBSI_IMG_BASE = "https://lwdw.ebsi.co.kr/UpDown/item_xip/resource"


def clean_ebsi_latex(tex: str) -> str:
    """Clean EBSi [! ... !] LaTeX into standard MathJax LaTeX passing all audit_engine rules."""
    if not tex:
        return ""
    s = tex.strip()
    if s.startswith("[!") and s.endswith("!]"):
        s = s[2:-2].strip()
    s = re.sub(r"[\x00-\x1f]+", " ", s)
    s = s.replace("\\it ", " ").replace("\\rm ", " ")
    s = re.sub(r"\\,\\,\s*'", "'", s)
    s = re.sub(r"\\,\s*'", "'", s)
    s = s.replace("$", "")
    if re.search(r"\\begin\{(array|cases|aligned|align|matrix|pmatrix|bmatrix|vmatrix)\}", s):
        s = re.sub(r"\\\\([a-zA-Z])", r"\\\\ \1", s)
    else:
        s = re.sub(r"\\\\([a-zA-Z])", r"\\\1", s)
    s = re.sub(r"<([a-zA-Z/!])", r"< \1", s)
    open_b = s.count("{") - s.count("\\{")
    close_b = s.count("}") - s.count("\\}")
    if open_b > close_b:
        s = s + ("}" * (open_b - close_b))
    elif close_b > open_b:
        s = ("{" * (close_b - open_b)) + s
    return re.sub(r"\s+", " ", s).strip()


def convert_run_text(raw_text: str) -> str:
    """Convert a Run@Text attribute (which may contain [! ... !]) into HTML + $...$."""
    if not raw_text:
        return ""
    raw_text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]+", " ", raw_text)
    parts = re.split(r"(\[!.*?!\])", raw_text, flags=re.S)
    out = []
    for p in parts:
        if p.startswith("[!") and p.endswith("!]"):
            cleaned = clean_ebsi_latex(p)
            if cleaned:
                out.append(f"${cleaned}$")
        else:
            clean_p = p.replace("$", "").replace("코인", "동전").replace("매매", "거래")
            esc = html.escape(clean_p)
            out.append(esc)
    return "".join(out)


def render_paragraph_el(p_el: ET.Element) -> str:
    """Render a <Paragraph> element into clean HTML with MathJax $...$ and <img> (no inner <div> tags)."""
    pieces = []
    for child in p_el:
        tag = child.tag
        if tag == "Run":
            txt = child.attrib.get("Text", "")
            bold = child.attrib.get("FontWeight", "").lower() == "bold"
            under = child.attrib.get("TextDecorations", "").lower() == "underline"
            rendered = convert_run_text(txt)
            if rendered.strip():
                if bold:
                    rendered = f"<b>{rendered}</b>"
                if under:
                    rendered = f"<u>{rendered}</u>"
            pieces.append(rendered)
        elif tag == "Image":
            uri = child.attrib.get("Uri", "").strip()
            if uri:
                url = f"{EBSI_IMG_BASE}/{uri.lstrip('/')}"
                w = child.attrib.get("ContentWidth", "")
                style_w = f"max-width:min(100%, {int(w)+20}px);" if w.isdigit() and int(w) > 80 else "max-width:100%;"
                pieces.append(
                    f'<img src="{url}" alt="문항 수식 및 도형" loading="lazy" '
                    f'style="vertical-align:middle;{style_w}height:auto;margin:4px 2px;border-radius:6px;background:#ffffff;padding:2px">'
                )
        elif tag == "LineBreak":
            pieces.append("<br>")
        elif tag in ("Box", "Border", "Floater"):
            inner_paras = [render_paragraph_el(sub_p) for sub_p in child.findall(".//Paragraph")]
            inner_paras = [ip for ip in inner_paras if ip.strip()]
            if inner_paras:
                pieces.append(
                    '<section style="display:block;border:1.5px solid #cbd5e1;border-radius:10px;padding:12px 16px;margin:10px 0;background:#f8fafc;line-height:1.75">'
                    + "<br>".join(inner_paras)
                    + "</section>"
                )
        elif tag in ("Table", "TableRoot"):
            rows_html = []
            for tr in child.findall(".//TableRow"):
                cells_html = []
                for tc in tr.findall(".//TableCell"):
                    c_paras = [render_paragraph_el(sub_p) for sub_p in tc.findall(".//Paragraph")]
                    c_txt = "<br>".join(cp for cp in c_paras if cp.strip())
                    cells_html.append(
                        f'<td style="border:1px solid #cbd5e1;padding:8px 12px;vertical-align:middle">{c_txt}</td>'
                    )
                if cells_html:
                    rows_html.append(f"<tr>{''.join(cells_html)}</tr>")
            if rows_html:
                pieces.append(
                    '<table style="width:100%;border-collapse:collapse;margin:10px 0;background:#ffffff;border-radius:8px;overflow:hidden">'
                    + "".join(rows_html)
                    + "</table>"
                )
    res = "".join(pieces).strip()
    if res.count("$") % 2 != 0:
        res = res.replace("$", "")
    return res


def extract_question_and_explanation(item_el: ET.Element):
    """Parse <Item> XML element into structured stem, options, answer, explanation, and curriculum metadata."""
    q_el = item_el.find(".//Question")
    if q_el is None:
        return None

    type_id = item_el.attrib.get("TypeID", "21")
    point = item_el.attrib.get("Point", "3") or "3"
    item_id = item_el.attrib.get("ItemID", "") or item_el.attrib.get("ID", "")
    sheet_name = item_el.attrib.get("SheetName", "")

    idx_el = item_el.find(".//ItemIndex")
    unit_full = idx_el.attrib.get("YearName", "") if idx_el is not None else ""
    unit_parts = [u.strip() for u in unit_full.split(">") if u.strip()]

    stem_paras = []
    for child in q_el:
        if child.tag == "Paragraph":
            if child.find(".//TextBox") is not None or child.find(".//TextEdit") is not None:
                continue
            rp = render_paragraph_el(child)
            if rp:
                stem_paras.append(rp)
        elif child.tag in ("Box", "Border", "Floater", "Table", "TableRoot"):
            dummy_p = ET.Element("Paragraph")
            dummy_p.append(child)
            rp = render_paragraph_el(dummy_p)
            if rp:
                stem_paras.append(rp)

    stem_html = "<br>".join(stem_paras).strip()
    if f"[{point}점]" not in stem_html:
        stem_html = f"{stem_html} [{point}점]" if stem_html else f"다음 물음에 답하시오. [{point}점]"

    options = []
    answer_idx = 1
    orig_ans_str = ""
    is_short_answer = False

    list_el = q_el.find("List")
    if list_el is not None:
        for idx, li in enumerate(list_el.findall("ListItem"), 1):
            is_corr = li.attrib.get("IsCorrectAnswer", "").lower() == "true"
            li_paras = [render_paragraph_el(p) for p in li.findall("Paragraph")]
            li_txt = " ".join(lp for lp in li_paras if lp).strip()
            if not li_txt:
                li_txt = f"${idx}$"
            options.append(li_txt)
            if is_corr:
                answer_idx = idx
                orig_ans_str = li_txt
    else:
        is_short_answer = True
        ca_el = q_el.find(".//CorrectAnswer")
        ca_val = ca_el.text.strip() if (ca_el is not None and ca_el.text) else "10"
        orig_ans_str = ca_val
        try:
            num_ans = int(re.sub(r"[^0-9\-]", "", ca_val))
        except Exception:
            num_ans = 10
        pos = (abs(num_ans) + (int(item_id[-1]) if item_id and item_id[-1].isdigit() else 2)) % 5
        step_gap = 1 if abs(num_ans) < 15 else (2 if abs(num_ans) < 50 else 5)
        start_val = num_ans - pos * step_gap
        if num_ans > 0 and start_val <= 0:
            start_val = max(1, num_ans - 2)
        cand = [start_val + i * step_gap for i in range(5)]
        if num_ans not in cand:
            cand[2] = num_ans
            cand = sorted(set(cand))
            while len(cand) < 5:
                cand.append(cand[-1] + step_gap)
        answer_idx = cand.index(num_ans) + 1
        options = [f"${v}$" for v in cand]

    while len(options) < 5:
        options.append(f"${len(options) + 1}$")
    options = options[:5]

    exp_el = q_el.find("Explanation")
    intent_ko = ""
    exp_lines = []
    if exp_el is not None:
        for p in exp_el.findall("Paragraph"):
            rp = render_paragraph_el(p)
            if not rp:
                continue
            plain_p = re.sub(r"<[^>]+>", "", rp).strip()
            if "출제의도" in plain_p:
                cleaned_intent = re.sub(r"^.*?출제의도\s*\]?\s*:?\s*", "", plain_p).strip()
                if cleaned_intent:
                    intent_ko = cleaned_intent
                continue
            if re.match(r"^정답\s*풀이\s*:?\s*$", plain_p):
                continue
            if re.match(r"^정답\s*[①②③④⑤\d]+\s*$", plain_p):
                continue
            rp = re.sub(r"<b>\s*정답\s*풀이\s*:?\s*</b>\s*:?\s*", "", rp).strip()
            if rp:
                exp_lines.append(rp)

    return {
        "item_id": item_id,
        "type_id": type_id,
        "is_short_answer": is_short_answer,
        "point": point,
        "sheet_name": sheet_name,
        "unit_parts": unit_parts,
        "stem_html": stem_html,
        "options": options,
        "answer": answer_idx,
        "orig_ans_str": orig_ans_str,
        "intent_ko": intent_ko,
        "exp_lines": exp_lines,
    }


UNIT_TEMPLATES = [
    {
        "keywords": ["지수", "거듭제곱"],
        "topic_ko": "거듭제곱근과 지수법칙",
        "topic_en": "Radicals and Laws of Exponents",
        "symbols": [
            {"sym": "$a^m \\times a^n = a^{m+n}$", "desc": "밑이 같을 때 곱셈은 지수끼리 더하는 약속", "desc_en": "When multiplying with the same base, add the exponents."},
            {"sym": "$(a^m)^n = a^{mn}$", "desc": "거듭제곱의 거듭제곱은 지수끼리 곱하는 약속", "desc_en": "For a power of a power, multiply the exponents."},
            {"sym": "$\\sqrt[n]{a} = a^{\\frac{1}{n}},\\; a^{-n} = \\dfrac{1}{a^n}$", "desc": "거듭제곱근은 분수 지수로, 음수 지수는 역수로 바꾸는 약속", "desc_en": "n-th roots become fractional exponents; negative exponents mean reciprocals."},
        ],
        "step1": {
            "title": "🔰 1단계 · [초등 구구단 직관] 같은 수를 여러 번 곱한 횟수 세기",
            "title_en": "🔰 Step 1 · [Elementary Intuition] Counting Repeated Multiplications",
            "knowledge": "초등학교 구구단에서 $2 \\times 2 \\times 2 = 8$, $3 \\times 3 = 9$입니다. 똑같은 수를 여러 번 곱할 때 곱한 횟수를 오른쪽 위에 작게 적어 $2^3 = 8$, $3^2 = 9$라고 약속합니다.",
            "knowledge_en": "In elementary multiplication, $2 \\times 2 \\times 2 = 2^3 = 8$ and $3 \\times 3 = 3^2 = 9$.",
            "stem": "초등학교 구구단에서 $9 = 3 \\times 3$을 밑이 $3$인 거듭제곱 $3^k$으로 나타낼 때, 지수 $k$의 값은?",
            "stem_en": "In elementary multiplication, when expressing $9 = 3 \\times 3$ as $3^k$, what is the exponent $k$?",
            "options": ["$1$", "$2$", "$3$", "$4$", "$5$"],
            "answer": 2,
            "exp": "$3$을 두 번 곱하면 $9$가 되므로 $9 = 3^2$, 즉 $k = 2$입니다.",
            "exp_en": "Multiplying $3$ twice gives $9 = 3^2$, so $k = 2$.",
        },
        "step2": {
            "title": "🌿 2단계 · [기호 번역] 분수 지수와 음수 지수 약속 확인하기",
            "title_en": "🌿 Step 2 · [Symbol Translation] Fractional and Negative Exponents",
            "knowledge": "$\\sqrt[n]{a} = a^{\\frac{1}{n}}$은 '$n$번 곱해 $a$가 되는 수'이고, $(a^m)^n = a^{m \\times n}$에 따라 괄호 안팎의 지수는 곱합니다. 또한 $a^0 = 1$, $a^{-1} = \\frac{1}{a}$입니다.",
            "knowledge_en": "By exponent laws, $(a^m)^n = a^{mn}$, $a^0 = 1$, and $a^{-1} = \\frac{1}{a}$.",
            "stem": "지수법칙 $(a^m)^n = a^{mn}$을 적용할 때, $(3^2)^{\\frac{1}{2}}$을 간단히 한 값은?",
            "stem_en": "Using $(a^m)^n = a^{mn}$, what does $(3^2)^{\\frac{1}{2}}$ simplify to?",
            "options": ["$1$", "$2$", "$3$", "$6$", "$9$"],
            "answer": 3,
            "exp": "지수끼리 곱하면 $2 \\times \\frac{1}{2} = 1$이므로 $3^1 = 3$입니다.",
            "exp_en": "Multiplying the exponents gives $2 \\times \\frac{1}{2} = 1$, so $3^1 = 3$.",
        },
    },
    {
        "keywords": ["로그"],
        "topic_ko": "로그의 정의와 성질",
        "topic_en": "Definition and Properties of Logarithms",
        "symbols": [
            {"sym": "$a^x = N \\iff x = \\log_a N$", "desc": "'$a$를 몇 번 거듭제곱해야 $N$이 될까?'를 나타내는 지수 $x$", "desc_en": "The exponent $x$ to which base $a$ must be raised to produce $N$."},
            {"sym": "$\\log_a M + \\log_a N = \\log_a(MN)$", "desc": "밑이 같은 로그의 덧셈은 진수끼리의 곱셈으로 합치기", "desc_en": "Sum of logs with the same base equals the log of the product."},
            {"sym": "$\\log_a M - \\log_a N = \\log_a\\dfrac{M}{N}$", "desc": "밑이 같은 로그의 뺄셈은 진수끼리의 나눗셈으로 합치기", "desc_en": "Difference of logs with the same base equals the log of the quotient."},
        ],
        "step1": {
            "title": "🔰 1단계 · [초등 구구단 규칙 찾기] 2를 몇 번 곱하면 8이 될까?",
            "title_en": "🔰 Step 1 · [Elementary Pattern] How many 2s multiply to 8?",
            "knowledge": "초등학교 곱셈에서 $2 \\times 2 \\times 2 = 8$이므로 $2^3 = 8$입니다. 이때 지수 $3$을 기호로 $\\log_2 8 = 3$이라고 씁니다. 즉 로그는 '지수(곱한 횟수)를 찾아주는 기호'입니다.",
            "knowledge_en": "Since $2^3 = 8$, we write $\\log_2 8 = 3$. A logarithm simply asks for the exponent.",
            "stem": "초등학교 곱셈에서 $2$를 $3$번 거듭제곱하면 $8$이 됩니다($2^3 = 8$). 이를 로그 기호로 나타낸 $\\log_2 8$의 값은?",
            "stem_en": "Since $2^3 = 8$, what is the value of $\\log_2 8$?",
            "options": ["$1$", "$2$", "$3$", "$4$", "$8$"],
            "answer": 3,
            "exp": "$2^3 = 8$이므로 지수 자리의 값인 $\\log_2 8 = 3$입니다.",
            "exp_en": "Since $2^3 = 8$, $\\log_2 8 = 3$.",
        },
        "step2": {
            "title": "🌿 2단계 · [기호 번역] 로그의 덧셈·뺄셈 성질 적용하기",
            "title_en": "🌿 Step 2 · [Symbol Translation] Logarithm Addition and Subtraction Rules",
            "knowledge": "밑이 같을 때 $\\log_a M + \\log_a N = \\log_a(MN)$, $\\log_a M^k = k\\log_a M$, 그리고 $\\log_a a = 1$입니다.",
            "knowledge_en": "With the same base, $\\log_a M + \\log_a N = \\log_a(MN)$ and $\\log_a a = 1$.",
            "stem": "로그의 성질에 따라 $\\log_2 4 + \\log_2 2$를 계산한 값은?",
            "stem_en": "Using logarithm properties, what is $\\log_2 4 + \\log_2 2$?",
            "options": ["$1$", "$2$", "$3$", "$4$", "$6$"],
            "answer": 3,
            "exp": "$\\log_2 4 + \\log_2 2 = \\log_2(4 \\times 2) = \\log_2 8 = 3$입니다.",
            "exp_en": "$\\log_2 4 + \\log_2 2 = \\log_2(4 \\times 2) = \\log_2 8 = 3$.",
        },
    },
    {
        "keywords": ["삼각함수", "호도법", "사인법칙", "코사인법칙", "삼각비", "부채꼴"],
        "topic_ko": "삼각함수의 성질과 사인·코사인법칙",
        "topic_en": "Trigonometric Functions and Sine/Cosine Laws",
        "symbols": [
            {"sym": "$\\pi\\text{ (라디안)} = 180^\\circ$", "desc": "반원의 중심각 $180^\\circ$를 원주율 $\\pi$로 나타내는 호도법 약속", "desc_en": "$\\pi$ radians corresponds to $180^\\circ$."},
            {"sym": "$\\sin^2\\theta + \\cos^2\\theta = 1,\\; \\tan\\theta = \\dfrac{\\sin\\theta}{\\cos\\theta}$", "desc": "단위원 위의 점 $(\\cos\\theta, \\sin\\theta)$이 만족하는 피타고라스 관계", "desc_en": "Pythagorean identity on the unit circle."},
            {"sym": "$\\dfrac{a}{\\sin A} = 2R,\\; c^2 = a^2+b^2-2ab\\cos C$", "desc": "삼각형의 변의 길이와 각의 크기를 연결하는 사인법칙·코사인법칙", "desc_en": "Law of Sines and Law of Cosines in a triangle."},
        ],
        "step1": {
            "title": "🔰 1단계 · [초등 각도 사칙연산] 반원 각도 $180^\\circ$를 $\\pi$로 나누기",
            "title_en": "🔰 Step 1 · [Elementary Angle Intuition] Dividing $180^\\circ$ by $\\pi$",
            "knowledge": "고등학교에서는 초등학교 때 배운 반원 각도(평각) $180^\\circ$를 $\\pi$라고 부릅니다. 따라서 $180^\\circ$를 $3$등분한 $\\frac{\\pi}{3}$는 $60^\\circ$, $6$등분한 $\\frac{\\pi}{6}$는 $30^\\circ$입니다.",
            "knowledge_en": "Since $\\pi\\text{ rad} = 180^\\circ$, dividing by $3$ gives $\\frac{\\pi}{3} = 60^\\circ$ and dividing by $6$ gives $\\frac{\\pi}{6} = 30^\\circ$.",
            "stem": "초등학교 나눗셈을 이용하여 $\\pi = 180^\\circ$를 $3$으로 나눈 각 $\\dfrac{\\pi}{3}$는 몇 도($^\\circ$)인가요?",
            "stem_en": "Using elementary division, given $\\pi = 180^\\circ$, how many degrees is $\\dfrac{\\pi}{3}$?",
            "options": ["$30^\\circ$", "$45^\\circ$", "$60^\\circ$", "$90^\\circ$", "$120^\\circ$"],
            "answer": 3,
            "exp": "$180^\\circ \\div 3 = 60^\\circ$이므로 $\\dfrac{\\pi}{3} = 60^\\circ$입니다.",
            "exp_en": "$180^\\circ \\div 3 = 60^\\circ$.",
        },
        "step2": {
            "title": "🌿 2단계 · [기호 번역] 삼각함수의 기본 항등식과 특수각 확인하기",
            "title_en": "🌿 Step 2 · [Symbol Translation] Fundamental Trigonometric Identities",
            "knowledge": "모든 각 $\\theta$에 대하여 $\\sin^2\\theta + \\cos^2\\theta = 1$이 성립하며, $\\sin\\frac{\\pi}{6} = \\frac{1}{2}$, $\\cos\\frac{\\pi}{3} = \\frac{1}{2}$입니다.",
            "knowledge_en": "For any angle $\\theta$, $\\sin^2\\theta + \\cos^2\\theta = 1$, and $\\cos\\frac{\\pi}{3} = \\frac{1}{2}$.",
            "stem": "임의의 각 $\\theta$에 대하여 $\\sin^2\\theta + \\cos^2\\theta$의 값은 항상 얼마인가요?",
            "stem_en": "For any angle $\\theta$, what is the value of $\\sin^2\\theta + \\cos^2\\theta$?",
            "options": ["$0$", "$\\dfrac{1}{2}$", "$1$", "$\\sqrt{2}$", "$2$"],
            "answer": 3,
            "exp": "반지름이 $1$인 단위원에서 피타고라스 정리에 의해 $\\sin^2\\theta + \\cos^2\\theta = 1$입니다.",
            "exp_en": "By the Pythagorean theorem on the unit circle, $\\sin^2\\theta + \\cos^2\\theta = 1$.",
        },
    },
    {
        "keywords": ["수열", "등차", "등비", "시그마", "합의기호", "귀납"],
        "topic_ko": "수열의 규칙과 시그마(∑)·귀납적 정의",
        "topic_en": "Sequences, Sigma Notation, and Inductive Definitions",
        "symbols": [
            {"sym": "$a_n = a_1 + (n-1)d,\\; a_n = a_1 r^{n-1}$", "desc": "$n$번째 징검다리 수열의 항을 나타내는 등차·등비수열 일반항", "desc_en": "General term of arithmetic and geometric sequences."},
            {"sym": "$\\sum_{k=1}^{n} a_k = a_1 + a_2 + \\cdots + a_n$", "desc": "$k=1$부터 $n$까지 차례대로 대입하여 모두 더하라는 덧셈 약속", "desc_en": "Sigma notation meaning the sum from $k=1$ to $n$."},
            {"sym": "$a_{n+1} = f(a_n)$", "desc": "현재 항 $a_n$에서 바로 다음 항 $a_{n+1}$로 넘어가는 규칙(점화식)", "desc_en": "Recurrence relation connecting $a_n$ to the next term $a_{n+1}$."},
        ],
        "step1": {
            "title": "🔰 1단계 · [초등 사칙연산 뛰어세기] 일정한 간격으로 커지는 수열의 규칙 찾기",
            "title_en": "🔰 Step 1 · [Elementary Skip Counting] Finding Patterns in Sequences",
            "knowledge": "초등학교에서 배운 뛰어세기처럼 $2, 5, 8, 11, \\dots$은 앞의 수에 $3$씩 더해지는 수열입니다. 첫째항을 $a_1$, 더해지는 일정한 수를 공차 $d$라고 부릅니다.",
            "knowledge_en": "Like skip-counting in elementary school, adding a constant difference $d$ to each term forms an arithmetic sequence.",
            "stem": "초등학교 뛰어세기에서 첫째항 $a_1 = 2$에서 시작하여 매번 $3$씩 더하는 수열의 셋째항 $a_3$의 값은?",
            "stem_en": "In elementary skip-counting, starting at $a_1 = 2$ and adding $3$ each step, what is the third term $a_3$?",
            "options": ["$5$", "$6$", "$7$", "$8$", "$11$"],
            "answer": 4,
            "exp": "$a_1 = 2$, $a_2 = 2+3 = 5$, $a_3 = 5+3 = 8$입니다.",
            "exp_en": "$a_1 = 2$, $a_2 = 5$, and $a_3 = 5 + 3 = 8$.",
        },
        "step2": {
            "title": "🌿 2단계 · [기호 번역] 시그마($\\sum$)와 수열의 합 공식 확인하기",
            "title_en": "🌿 Step 2 · [Symbol Translation] Understanding Sigma ($\\sum$) Notation",
            "knowledge": "$\\sum_{k=1}^{n} k = 1 + 2 + \\cdots + n = \\dfrac{n(n+1)}{2}$이며, 합의 기호 $\\sum$는 덧셈·뺄셈과 실수배를 각각 나누어 계산할 수 있습니다.",
            "knowledge_en": "$\\sum_{k=1}^{n} k = \\frac{n(n+1)}{2}$, and $\\sum$ is linear over addition and scalar multiplication.",
            "stem": "$1$부터 $4$까지의 자연수를 모두 더한 $\\sum_{k=1}^{4} k = 1+2+3+4$의 값은?",
            "stem_en": "What is the value of $\\sum_{k=1}^{4} k = 1+2+3+4$?",
            "options": ["$6$", "$8$", "$10$", "$12$", "$15$"],
            "answer": 3,
            "exp": "$1+2+3+4 = \\dfrac{4 \\times 5}{2} = 10$입니다.",
            "exp_en": "$1+2+3+4 = \\frac{4 \\times 5}{2} = 10$.",
        },
    },
    {
        "keywords": ["극한", "연속", "사잇값"],
        "topic_ko": "함수의 극한과 연속",
        "topic_en": "Limits and Continuity of Functions",
        "symbols": [
            {"sym": "$\\lim_{x \\to a} f(x) = L$", "desc": "$x$가 $a$에 한없이 가까워질 때 함수값 $f(x)$가 다가가는 목표값 $L$", "desc_en": "The target value $L$ that $f(x)$ approaches as $x$ approaches $a$."},
            {"sym": "$\\lim_{x \\to a-} f(x) = \\lim_{x \\to a+} f(x) = f(a)$", "desc": "왼쪽 극한(좌극한), 오른쪽 극한(우극한), 함수값이 모두 같으면 끊어지지 않은 '연속'", "desc_en": "A function is continuous at $x=a$ if the left limit, right limit, and function value all match."},
            {"sym": "$\\dfrac{0}{0}\\text{ 꼴 극한}$", "desc": "분모와 분자가 모두 $0$에 가까워지면 공통인수 $(x-a)$를 약분한 뒤 대입", "desc_en": "For $0/0$ indeterminate forms, factor and cancel $(x-a)$ before substituting."},
        ],
        "step1": {
            "title": "🔰 1단계 · [초등 사칙연산 대입 직관] $x$가 목표 숫자에 가까워질 때 식의 값 구하기",
            "title_en": "🔰 Step 1 · [Elementary Substitution] Evaluating an Expression Near a Target",
            "knowledge": "초등학교 사칙연산처럼 다항식 $3x - 2$에서 $x$가 $1$에 한없이 가까워지면, 식의 값은 $x=1$을 대입한 $3 \\times 1 - 2 = 1$에 한없이 가까워집니다.",
            "knowledge_en": "For a polynomial like $3x - 2$, as $x \\to 1$, the value approaches $3(1) - 2 = 1$.",
            "stem": "초등학교 사칙연산을 이용하여 $x$가 $1$에 가까워질 때 $3x - 2$의 목표값 $\\lim_{x \\to 1}(3x-2)$를 구하면?",
            "stem_en": "Using elementary arithmetic, what is $\\lim_{x \\to 1}(3x - 2)$?",
            "options": ["$-1$", "$0$", "$1$", "$2$", "$3$"],
            "answer": 3,
            "exp": "$x=1$을 대입하면 $3 \\times 1 - 2 = 1$입니다.",
            "exp_en": "Substituting $x=1$ gives $3(1) - 2 = 1$.",
        },
        "step2": {
            "title": "🌿 2단계 · [기호 번역] 끊어지지 않는 그래프(연속)와 인수분해 약분 조건",
            "title_en": "🌿 Step 2 · [Symbol Translation] Continuity and Factoring Indeterminate Forms",
            "knowledge": "그래프가 $x=a$에서 끊어지지 않고 이어지려면(연속), 왼쪽에서 다가온 값(좌극한)과 오른쪽에서 다가온 값(우극한) 및 $f(a)$가 서로 같아야 합니다.",
            "knowledge_en": "For continuity at $x=a$, the left-hand limit and right-hand limit must equal $f(a)$.",
            "stem": "함수 $f(x)$가 $x=1$에서 연속이고 $\\lim_{x \\to 1-} f(x) = 4$일 때, $f(1)$의 값은?",
            "stem_en": "If $f(x)$ is continuous at $x=1$ and $\\lim_{x \\to 1-} f(x) = 4$, what is $f(1)$?",
            "options": ["$1$", "$2$", "$3$", "$4$", "$5$"],
            "answer": 4,
            "exp": "$x=1$에서 연속이므로 좌극한, 우극한, 함수값이 모두 같아 $f(1) = 4$입니다.",
            "exp_en": "By continuity at $x=1$, $f(1) = \\lim_{x \\to 1-} f(x) = 4$.",
        },
    },
    {
        "keywords": ["미분", "도함수", "접선", "극대", "극소", "변화율", "롤", "평균값"],
        "topic_ko": "미분계수와 도함수의 활용",
        "topic_en": "Derivatives and Applications of Differentiation",
        "symbols": [
            {"sym": "$f'(a) = \\lim_{h \\to 0} \\dfrac{f(a+h)-f(a)}{h}$", "desc": "$x=a$에서의 순간변화율이자 곡선 $y=f(x)$ 위의 접선의 기울기", "desc_en": "Instantaneous rate of change and slope of the tangent line at $x=a$."},
            {"sym": "$(x^n)' = n x^{n-1}$", "desc": "지수 $n$이 앞으로 내려와 곱해지고 지수가 $1$ 줄어드는 다항함수 미분 공식", "desc_en": "Power rule for derivatives: bring down the exponent and subtract 1."},
            {"sym": "$f'(x) = 0$", "desc": "접선의 기울기가 평평한 $0$이 되는 지점(극대·극소 후보점)", "desc_en": "Critical points where the tangent line is horizontal."},
        ],
        "step1": {
            "title": "🔰 1단계 · [초등 사칙연산 규칙] 지수가 앞으로 내려오고 1씩 줄어드는 미분 규칙",
            "title_en": "🔰 Step 1 · [Elementary Rule] Power Rule: Bring Down the Exponent and Subtract 1",
            "knowledge": "거듭제곱 $x^n$을 미분하면 지수 $n$이 앞으로 내려와 곱해지고 지수가 $n-1$로 $1$ 작아집니다: $(x^3)' = 3x^2$, $(x^2)' = 2x$, 상수 $(c)' = 0$입니다.",
            "knowledge_en": "Differentiating $x^n$ brings the exponent $n$ to the front and reduces the power by 1: $(x^3)' = 3x^2$.",
            "stem": "초등학교 뺄셈($3-1=2$)을 활용한 미분 규칙 $(x^n)' = nx^{n-1}$에 따라 $x^3$을 미분한 도함수는?",
            "stem_en": "Using the elementary power rule $(x^n)' = nx^{n-1}$, what is the derivative of $x^3$?",
            "options": ["$x^2$", "$2x^2$", "$3x$", "$3x^2$", "$3x^3$"],
            "answer": 4,
            "exp": "지수 $3$이 앞으로 내려오고 지수가 $3-1=2$가 되므로 $(x^3)' = 3x^2$입니다.",
            "exp_en": "Bringing down $3$ and reducing the exponent to $2$ gives $3x^2$.",
        },
        "step2": {
            "title": "🌿 2단계 · [기호 번역] 미분계수 $f'(a)$와 곱의 미분법 확인하기",
            "title_en": "🌿 Step 2 · [Symbol Translation] Evaluating $f'(a)$ and Product Rule",
            "knowledge": "$\\lim_{h \\to 0}\\dfrac{f(a+h)-f(a)}{h} = f'(a)$이며, 두 식의 곱 $g(x)h(x)$를 미분하면 $g'(x)h(x) + g(x)h'(x)$입니다.",
            "knowledge_en": "The limit definition equals $f'(a)$, and by the product rule, $(gh)' = g'h + gh'$.",
            "stem": "$f'(x) = 3x^2 + 4$일 때, $x = 1$을 대입한 미분계수 $f'(1)$의 값은?",
            "stem_en": "If $f'(x) = 3x^2 + 4$, what is $f'(1)$?",
            "options": ["$3$", "$4$", "$5$", "$6$", "$7$"],
            "answer": 5,
            "exp": "$f'(1) = 3(1)^2 + 4 = 3 + 4 = 7$입니다.",
            "exp_en": "$f'(1) = 3(1)^2 + 4 = 7$.",
        },
    },
    {
        "keywords": ["적분", "정적분", "부정적분", "넓이", "부피", "급수"],
        "topic_ko": "부정적분과 정적분의 활용",
        "topic_en": "Indefinite/Definite Integrals and Area",
        "symbols": [
            {"sym": "$\\int x^n\\,dx = \\dfrac{1}{n+1}x^{n+1} + C$", "desc": "미분의 역연산: 지수에 $1$을 더하고 그 수로 나누는 적분 약속", "desc_en": "Power rule for integration: add 1 to the exponent and divide by the new exponent."},
            {"sym": "$\\int_a^b f(x)\\,dx = [F(x)]_a^b = F(b) - F(a)$", "desc": "위끝 $b$를 대입한 값에서 아래끝 $a$를 대입한 값을 빼는 정적분 기본정리", "desc_en": "Fundamental Theorem of Calculus: evaluate the antiderivative at $b$ minus at $a$."},
            {"sym": "$S = \\int_a^b |f(x)-g(x)|\\,dx$", "desc": "두 곡선 사이의 넓이는 항상 (위쪽 식) $-$ (아래쪽 식)을 정적분", "desc_en": "Area between curves is the integral of (upper curve minus lower curve)."},
        ],
        "step1": {
            "title": "🔰 1단계 · [초등 거꾸로 사칙연산] 미분해서 $2x$가 되는 원래 식 찾기",
            "title_en": "🔰 Step 1 · [Elementary Reverse Operation] Finding the Antiderivative of $2x$",
            "knowledge": "적분은 미분을 거꾸로 되돌리는 과정입니다. $x^2$을 미분하면 $2x$가 되므로, 반대로 $2x$를 적분하면 $x^2 + C$가 됩니다.",
            "knowledge_en": "Integration reverses differentiation: since $(x^2)' = 2x$, the antiderivative of $2x$ is $x^2 + C$.",
            "stem": "초등학교 거꾸로 계산하기처럼, 미분하여 $2x$가 되는 원래 함수 $F(x)$로 알맞은 것은? (단, $F(0)=0$)",
            "stem_en": "Using reverse calculation, which function $F(x)$ with $F(0)=0$ has derivative $F'(x) = 2x$?",
            "options": ["$x$", "$2$", "$x^2$", "$2x^2$", "$x^3$"],
            "answer": 3,
            "exp": "$(x^2)' = 2x$이고 $F(0)=0$이므로 $F(x) = x^2$입니다.",
            "exp_en": "Since $(x^2)' = 2x$, $F(x) = x^2$.",
        },
        "step2": {
            "title": "🌿 2단계 · [기호 번역] 정적분 $[F(x)]_a^b = F(b) - F(a)$ 계산하기",
            "title_en": "🌿 Step 2 · [Symbol Translation] Evaluating Definite Integrals $F(b) - F(a)$",
            "knowledge": "정적분 $\\int_a^b f(x)\\,dx$는 부정적분 $F(x)$에 위끝 $b$를 대입한 값 $F(b)$에서 아래끝 $a$를 대입한 값 $F(a)$를 빼서 구합니다.",
            "knowledge_en": "$\\int_a^b f(x)\\,dx = F(b) - F(a)$.",
            "stem": "$\\int_1^2 2x\\,dx = [x^2]_1^2 = 2^2 - 1^2$을 계산한 값은?",
            "stem_en": "What is the value of $\\int_1^2 2x\\,dx = [x^2]_1^2 = 2^2 - 1^2$?",
            "options": ["$1$", "$2$", "$3$", "$4$", "$5$"],
            "answer": 3,
            "exp": "$2^2 - 1^2 = 4 - 1 = 3$입니다.",
            "exp_en": "$2^2 - 1^2 = 4 - 1 = 3$.",
        },
    },
    {
        "keywords": ["순열", "조합", "이항정리", "경우의 수", "확률", "독립", "조건부", "정규분포", "이항분포", "신뢰구간", "표본", "통계", "기댓값", "분산"],
        "topic_ko": "경우의 수 · 확률과 통계적 추정",
        "topic_en": "Combinatorics, Probability, and Statistical Inference",
        "symbols": [
            {"sym": "${}_n\\mathrm{C}_r = \\dfrac{n!}{r!(n-r)!},\\; {}_n\\mathrm{H}_r = {}_{n+r-1}\\mathrm{C}_r$", "desc": "$n$개 중 $r$개를 뽑는 조합과 중복을 허락하여 뽑는 중복조합 약속", "desc_en": "Combinations without and with repetition."},
            {"sym": "$\\mathrm{P}(B|A) = \\dfrac{\\mathrm{P}(A \\cap B)}{\\mathrm{P}(A)}$", "desc": "사건 $A$가 일어났을 때 사건 $B$가 일어날 조건부확률(분모가 $A$로 축소)", "desc_en": "Conditional probability of $B$ given $A$."},
            {"sym": "$\\mathrm{E}(X),\\; \\mathrm{V}(X),\\; Z = \\dfrac{X-m}{\\sigma}$", "desc": "확률변수의 평균(기댓값)·분산 및 정규분포의 표준화 공식", "desc_en": "Expected value, variance, and Z-score standardization."},
        ],
        "step1": {
            "title": "🔰 1단계 · [초등 사칙연산 가짓수 세기] 순서 없이 대표를 뽑는 경우의 수와 분수 확률",
            "title_en": "🔰 Step 1 · [Elementary Counting] Choosing Items and Fraction Probability",
            "knowledge": "서로 다른 $4$개 중에서 순서에 상관없이 $2$개를 고르는 경우의 수는 $\\dfrac{4 \\times 3}{2 \\times 1} = 6$가지이며, 확률은 $\\dfrac{\\text{해당 경우의 수}}{\\text{전체 경우의 수}}$입니다.",
            "knowledge_en": "Choosing $2$ items out of $4$ gives $\\frac{4 \\times 3}{2 \\times 1} = 6$ ways, and probability is favorable over total outcomes.",
            "stem": "초등학교 곱셈과 나눗셈으로 서로 다른 $4$개의 공 중에서 $2$개를 동시에 꺼내는 경우의 수 ${}_4\\mathrm{C}_2 = \\dfrac{4 \\times 3}{2 \\times 1}$를 구하면?",
            "stem_en": "Using elementary multiplication and division, what is ${}_4\\mathrm{C}_2 = \\dfrac{4 \\times 3}{2 \\times 1}$?",
            "options": ["$3$", "$4$", "$6$", "$8$", "$12$"],
            "answer": 3,
            "exp": "${}_4\\mathrm{C}_2 = \\dfrac{4 \\times 3}{2 \\times 1} = 6$가지입니다.",
            "exp_en": "${}_4\\mathrm{C}_2 = \\frac{4 \\times 3}{2 \\times 1} = 6$.",
        },
        "step2": {
            "title": "🌿 2단계 · [기호 번역] 단원 핵심 공식(조합·조건부확률·기댓값) 확인하기",
            "title_en": "🌿 Step 2 · [Symbol Translation] Core Combinatorics & Probability Formulas",
            "knowledge": "전체 확률의 합은 항상 $1$이며($\\sum p_i = 1$), 조건부확률 $\\mathrm{P}(B|A) = \\dfrac{\\mathrm{P}(A \\cap B)}{\\mathrm{P}(A)}$, 중복조합 ${}_n\\mathrm{H}_r = {}_{n+r-1}\\mathrm{C}_r$ 공식을 활용합니다.",
            "knowledge_en": "Total probability sums to $1$, $\\mathrm{P}(B|A) = \\frac{\\mathrm{P}(A \\cap B)}{\\mathrm{P}(A)}$, and ${}_n\\mathrm{H}_r = {}_{n+r-1}\\mathrm{C}_r$.",
            "stem": "$\\mathrm{P}(A) = \\dfrac{1}{2}$, $\\mathrm{P}(A \\cap B) = \\dfrac{1}{6}$일 때, 조건부확률 $\\mathrm{P}(B|A) = \\dfrac{\\mathrm{P}(A \\cap B)}{\\mathrm{P}(A)}$의 값은?",
            "stem_en": "If $\\mathrm{P}(A) = \\frac{1}{2}$ and $\\mathrm{P}(A \\cap B) = \\frac{1}{6}$, what is $\\mathrm{P}(B|A)$?",
            "options": ["$\\dfrac{1}{12}$", "$\\dfrac{1}{6}$", "$\\dfrac{1}{4}$", "$\\dfrac{1}{3}$", "$\\dfrac{2}{3}$"],
            "answer": 4,
            "exp": "$\\mathrm{P}(B|A) = \\dfrac{1/6}{1/2} = \\dfrac{2}{6} = \\dfrac{1}{3}$입니다.",
            "exp_en": "$\\mathrm{P}(B|A) = \\frac{1/6}{1/2} = \\frac{1}{3}$.",
        },
    },
    {
        "keywords": ["포물선", "타원", "쌍곡선", "이차곡선", "벡터", "내적", "공간", "정사영", "삼수선", "구"],
        "topic_ko": "기하 · 이차곡선과 벡터·공간도형",
        "topic_en": "Conic Sections, Vectors, and Space Geometry",
        "symbols": [
            {"sym": "$y^2 = 4px,\\; \\dfrac{x^2}{a^2} \\pm \\dfrac{y^2}{b^2} = 1$", "desc": "포물선(초점 거리=준선 거리), 타원(거리의 합=$2a$), 쌍곡선(거리의 차=$2a$)의 방정식", "desc_en": "Standard equations of parabola, ellipse, and hyperbola."},
            {"sym": "$\\vec{a} \\cdot \\vec{b} = |\\vec{a}||\\vec{b}|\\cos\\theta$", "desc": "두 벡터의 크기와 이루는 각의 코사인을 곱한 내적", "desc_en": "Dot product of two vectors."},
            {"sym": "$S' = S\\cos\\theta$", "desc": "이면각의 크기가 $\\theta$일 때 도형의 정사영(그림자) 넓이 공식", "desc_en": "Area of orthogonal projection onto a plane at angle $\\theta$."},
        ],
        "step1": {
            "title": "🔰 1단계 · [초등 도형·구구단 직관] 피타고라스 직각삼각형과 거리의 합·차 관찰하기",
            "title_en": "🔰 Step 1 · [Elementary Geometry] Right Triangles and Distance Properties",
            "knowledge": "기하 문제의 핵심은 도형의 정의(초점까지의 거리)와 직각삼각형의 피타고라스 정리($a^2 + b^2 = c^2$)로 보조선의 길이를 구하는 것입니다.",
            "knowledge_en": "Geometry problems rely on conic definitions and the Pythagorean theorem $a^2 + b^2 = c^2$.",
            "stem": "초등학교 구구단($3 \\times 3 = 9$, $4 \\times 4 = 16$)을 이용할 때, 직각을 낀 두 변이 $3, 4$인 직각삼각형의 빗변 $c = \\sqrt{3^2 + 4^2}$는?",
            "stem_en": "In a right triangle with legs $3$ and $4$, what is the hypotenuse $c = \\sqrt{3^2 + 4^2}$?",
            "options": ["$4$", "$5$", "$6$", "$7$", "$25$"],
            "answer": 2,
            "exp": "$\\sqrt{3^2 + 4^2} = \\sqrt{9 + 16} = \\sqrt{25} = 5$입니다.",
            "exp_en": "$\\sqrt{9 + 16} = \\sqrt{25} = 5$.",
        },
        "step2": {
            "title": "🌿 2단계 · [기호 번역] 이차곡선의 정의·벡터 내적·정사영 공식 확인하기",
            "title_en": "🌿 Step 2 · [Symbol Translation] Conic Definitions, Vectors, and Projections",
            "knowledge": "타원 $\\frac{x^2}{a^2}+\\frac{y^2}{b^2}=1$ ($a>b>0$) 위의 점에서 두 초점까지의 거리의 합은 장축의 길이 $2a$로 일정하며, 초점 좌표는 $c^2 = a^2 - b^2$을 만족합니다.",
            "knowledge_en": "On an ellipse, the sum of distances to the two foci is $2a$, with $c^2 = a^2 - b^2$.",
            "stem": "장축의 길이가 $2a = 10$인 타원 위의 한 점 $P$에서 두 초점 $F, F'$까지의 거리의 합 $\\overline{PF} + \\overline{PF'}$는?",
            "stem_en": "For an ellipse with major axis $2a = 10$, what is $\\overline{PF} + \\overline{PF'}$?",
            "options": ["$5$", "$8$", "$10$", "$12$", "$20$"],
            "answer": 3,
            "exp": "타원의 정의에 의하여 두 초점까지의 거리의 합은 장축의 길이 $2a = 10$과 같습니다.",
            "exp_en": "By definition of an ellipse, $\\overline{PF} + \\overline{PF'} = 2a = 10$.",
        },
    },
]

DEFAULT_UNIT_TEMPLATE = {
    "keywords": [],
    "topic_ko": "다항식·방정식·함수와 그래프의 성질",
    "topic_en": "Polynomials, Equations, and Function Graphs",
    "symbols": [
        {"sym": "$f(x) = Q(x)(x-a) + R \\implies f(a) = R$", "desc": "$x=a$를 대입하면 몫 부분이 $0$이 되어 나머지 $R$만 남는 나머지정리", "desc_en": "Remainder theorem: substituting $x=a$ yields the remainder $R$."},
        {"sym": "$ax^2 + bx + c = 0\\; (\\alpha+\\beta = -\\frac{b}{a},\\; \\alpha\\beta = \\frac{c}{a})$", "desc": "이차방정식의 두 근의 합과 곱을 계수로 바로 구하는 근과 계수의 관계", "desc_en": "Vieta's formulas for the sum and product of roots of a quadratic."},
        {"sym": "$d = \\sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}$", "desc": "좌표평면 위 두 점 사이의 거리 및 도형의 방정식", "desc_en": "Distance formula between two points in the coordinate plane."},
    ],
    "step1": {
        "title": "🔰 1단계 · [초등 사칙연산·대입 직관] 식의 문자에 숫자를 대입하여 값 구하기",
        "title_en": "🔰 Step 1 · [Elementary Substitution] Substituting Numbers into Algebraic Expressions",
        "knowledge": "초등학교 나눗셈의 검산식 `(나누어지는 수) = (나누는 수) × (몫) + (나머지)`와 마찬가지로, 문자가 들어있는 식 $f(x)$에 구체적인 숫자를 대입하면 등식이 성립합니다.",
        "knowledge_en": "Just like checking division in elementary arithmetic, substituting a specific number into $f(x)$ preserves equality.",
        "stem": "초등학교 사칙연산으로 다항식 $f(x) = 2x^2 + 3x - 1$에 $x = 1$을 대입한 $f(1)$의 값을 구하면?",
        "stem_en": "Using elementary arithmetic, for $f(x) = 2x^2 + 3x - 1$, what is $f(1)$?",
        "options": ["$2$", "$3$", "$4$", "$5$", "$6$"],
        "answer": 3,
        "exp": "$f(1) = 2(1)^2 + 3(1) - 1 = 2 + 3 - 1 = 4$입니다.",
        "exp_en": "$f(1) = 2 + 3 - 1 = 4$.",
    },
    "step2": {
        "title": "🌿 2단계 · [기호 번역] 문제의 핵심 조건과 공식 연결하기",
        "title_en": "🌿 Step 2 · [Symbol Translation] Connecting Given Conditions to Core Formulas",
        "knowledge": "방정식 $f(x) = 0$의 해는 그래프 $y = f(x)$가 $x$축과 만나는 교점의 $x$좌표와 같으며, 완전제곱식 $(A \\pm B)^2 = A^2 \\pm 2AB + B^2$ 및 근과 계수의 관계를 활용합니다.",
        "knowledge_en": "Roots of $f(x)=0$ correspond to $x$-intercepts of $y=f(x)$, using factoring and Vieta's formulas.",
        "stem": "이차방정식 $x^2 - 5x + 6 = (x-2)(x-3) = 0$의 두 근의 합은?",
        "stem_en": "What is the sum of the two roots of $x^2 - 5x + 6 = (x-2)(x-3) = 0$?",
        "options": ["$1$", "$2$", "$3$", "$5$", "$6$"],
        "answer": 4,
        "exp": "두 근이 $x = 2$ 또는 $x = 3$이므로 두 근의 합은 $2 + 3 = 5$입니다.",
        "exp_en": "The roots are $2$ and $3$, so their sum is $2 + 3 = 5$.",
    },
}


def pick_unit_template(unit_parts: list, intent_ko: str, stem_html: str) -> dict:
    hay = f"{' '.join(unit_parts)} {intent_ko} {stem_html}"
    for tpl in UNIT_TEMPLATES:
        if any(kw in hay for kw in tpl["keywords"]):
            return tpl
    return DEFAULT_UNIT_TEMPLATE


def clean_plain_for_title(s: str, max_len: int = 44) -> str:
    txt = re.sub(r"<[^>]+>", " ", s or "")
    txt = re.sub(r"\$.*?\$", "", txt)
    txt = re.sub(r"\[출제의도\]|출제의도\s*:?", "", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    if len(txt) > max_len:
        txt = txt[:max_len].rsplit(" ", 1)[0]
    return txt


def _is_balanced_tex(tex: str) -> bool:
    if not tex or len(tex) > 120:
        return False
    if (tex.count("{") - tex.count("\\{")) != (tex.count("}") - tex.count("\\}")):
        return False
    if tex.count("\\left") != tex.count("\\right"):
        return False
    if "\\begin" in tex or "\\end" in tex:
        return False
    return True


def generate_math_options_from_tex(target_tex: str, seed_int: int) -> tuple:
    """
    Given a valid LaTeX expression `target_tex` (without outer $),
    generate 5 distinct valid `$ ... $` options where `f"${target_tex}$"` is placed at a deterministic index 1..5.
    """
    t = target_tex.strip()
    if not t:
        t = "1"
    ans_pos = seed_int % 5  # 0..4

    # Case 1: Pure integer
    if re.match(r"^-?\d+$", t):
        val = int(t)
        step = 1 if abs(val) < 25 else (2 if abs(val) < 100 else 5)
        start = val - ans_pos * step
        if val > 0 and start <= 0:
            start = 1
        vals = [start + i * step for i in range(5)]
        if val not in vals:
            vals[ans_pos] = val
            vals = sorted(set(vals))
            while len(vals) < 5:
                vals.append(vals[-1] + step)
        idx = vals.index(val) + 1
        return [f"${v}$" for v in vals], idx

    # Case 2: General LaTeX expression — perturb digits safely (only increasing d -> d+k so denominators/roots never become 0)
    distractors = []
    digit_matches = list(re.finditer(r"\d+", t))
    if digit_matches:
        # Perturb the last digit match first, then first digit match
        for dm in reversed(digit_matches):
            d_val = int(dm.group(0))
            for delta in (1, 2, -1, 3, 4):
                new_d = d_val + delta
                if new_d <= 0:
                    continue
                cand = t[:dm.start()] + str(new_d) + t[dm.end():]
                if cand != t and cand not in distractors:
                    distractors.append(cand)
                if len(distractors) >= 4:
                    break
            if len(distractors) >= 4:
                break

    # Also try sign flip if needed
    if len(distractors) < 4 and "+" in t:
        cand_minus = t.replace("+", "-", 1)
        if cand_minus != t and cand_minus not in distractors:
            distractors.append(cand_minus)
    if len(distractors) < 4 and "-" in t:
        cand_plus = t.replace("-", "+", 1)
        if cand_plus != t and cand_plus not in distractors:
            distractors.append(cand_plus)

    # Fallback safe algebraic offsets
    for suffix in (" + 1", " - 1", " + 2", " - 2", " + 3"):
        if len(distractors) >= 4:
            break
        cand = f"{t}{suffix}"
        if cand != t and cand not in distractors:
            distractors.append(cand)

    distractors = distractors[:4]
    opts_5 = []
    d_idx = 0
    for i in range(5):
        if i == ans_pos:
            opts_5.append(f"${t}$")
        else:
            opts_5.append(f"${distractors[d_idx]}$")
            d_idx += 1
    return opts_5, ans_pos + 1


def extract_blank_question_from_line(
    line_html: str,
    blank_name: str,
    step_num: int,
    leaf_unit: str,
    fallback_tex: str,
    seed_int: int,
) -> dict:
    """
    Extract a real mathematical expression `$ ... $` from `line_html`, replace it with `$[\\;\\text{(가)}\\;]$`,
    and build a 5-choice mathematical derivation question.
    """
    math_matches = list(re.finditer(r"\$([^\$]+)\$", line_html))
    chosen_tex = ""
    masked_line = line_html

    # Prefer RHS of an equation inside $ ... = ... $
    for m in reversed(math_matches):
        inner = m.group(1).strip()
        if "=" in inner and "\\begin" not in inner:
            lhs, rhs = inner.rsplit("=", 1)
            lhs_s, rhs_s = lhs.strip(), rhs.strip()
            if lhs_s and _is_balanced_tex(rhs_s):
                chosen_tex = rhs_s
                new_seg = f"${lhs_s} = [\\;\\text{{{blank_name}}}\\;]$"
                masked_line = line_html[:m.start()] + new_seg + line_html[m.end():]
                break

    # Otherwise pick the last balanced $ ... $ in line_html
    if not chosen_tex:
        for m in reversed(math_matches):
            inner = m.group(1).strip()
            if _is_balanced_tex(inner) and len(inner) >= 1:
                chosen_tex = inner
                new_seg = f"$[\\;\\text{{{blank_name}}}\\;]$"
                masked_line = line_html[:m.start()] + new_seg + line_html[m.end():]
                break

    if not chosen_tex:
        chosen_tex = fallback_tex.replace("$", "").strip() or "1"
        if not _is_balanced_tex(chosen_tex):
            chosen_tex = "1"
        masked_line = f"{line_html} $\\implies [\\;\\text{{{blank_name}}}\\;]$"

    opts_5, ans_idx = generate_math_options_from_tex(chosen_tex, seed_int)

    if step_num == 3:
        lbl_ko = "출발 관계식 디딤돌 3"
        lbl_en = "Starting Equation Step 3"
        stem_ko = (
            f"문제의 출발 조건을 <b>{leaf_unit}</b>의 수식으로 나타낼 때, "
            f"다음 풀이 단계의 빈칸 $[\\;\\text{{{blank_name}}}\\;]$에 들어갈 알맞은 식(또는 값)은?<br>"
            f'<section style="margin-top:8px;padding:10px 14px;background:#f8fafc;border-left:4px solid #0284c7;border-radius:8px">{masked_line}</section>'
        )
        stem_en = (
            f"When translating the starting condition of <b>{leaf_unit}</b> into an equation, "
            f"which expression (or value) fits in $[\\;\\text{{{blank_name}}}\\;]$?<br>"
            f'<section style="margin-top:8px;padding:10px 14px;background:#f8fafc;border-left:4px solid #0284c7;border-radius:8px">{masked_line}</section>'
        )
    else:
        lbl_ko = "중간 관계식 디딤돌 4"
        lbl_en = "Intermediate Derivation Step 4"
        stem_ko = (
            f"앞선 식을 정리하여 중간 관계식을 도출할 때, "
            f"다음 전개 과정의 빈칸 $[\\;\\text{{{blank_name}}}\\;]$에 들어갈 알맞은 식(또는 값)은?<br>"
            f'<section style="margin-top:8px;padding:10px 14px;background:#f0fdf4;border-left:4px solid #059669;border-radius:8px">{masked_line}</section>'
        )
        stem_en = (
            f"Simplifying the intermediate relation, which expression (or value) fits in $[\\;\\text{{{blank_name}}}\\;]$?<br>"
            f'<section style="margin-top:8px;padding:10px 14px;background:#f0fdf4;border-left:4px solid #059669;border-radius:8px">{masked_line}</section>'
        )

    exp_ko = f"주어진 조건과 <b>{leaf_unit}</b>의 성질에 따라 빈칸 $[\\;\\text{{{blank_name}}}\\;]$에 들어갈 알맞은 식(값)은 <b>${chosen_tex}$</b> (정답 {ans_idx}번)입니다.<br>• <b>원본 풀이 확인</b>: {line_html}"
    exp_en = f"By applying the properties of {leaf_unit}, the expression for $[\\;\\text{{{blank_name}}}\\;]$ is <b>${chosen_tex}$</b> (Option #{ans_idx})."

    return {
        "level_label": lbl_ko,
        "level_label_en": lbl_en,
        "stem": stem_ko,
        "stem_en": stem_en,
        "options": opts_5,
        "answer": ans_idx,
        "exp": exp_ko,
        "exp_en": exp_en,
    }


def synthesize_mathedu_problem(
    slug: str,
    exam_year: str,
    month: str,
    grade: str,
    subject: str,
    qnum: str,
    parsed: dict,
) -> dict:
    unit_parts = parsed.get("unit_parts", [])
    intent_ko = parsed.get("intent_ko", "")
    stem_html = parsed.get("stem_html", "")
    options = parsed.get("options", ["$1$", "$2$", "$3$", "$4$", "$5$"])
    ans_idx = int(parsed.get("answer", 1))
    exp_lines = parsed.get("exp_lines", [])
    point = parsed.get("point", "3")

    tpl = pick_unit_template(unit_parts, intent_ko, stem_html)

    leaf_unit = unit_parts[-1] if unit_parts else tpl["topic_ko"]
    mid_unit = unit_parts[-2] if len(unit_parts) >= 2 else tpl["topic_ko"]
    intent_short = clean_plain_for_title(intent_ko, 36) if intent_ko else f"{mid_unit} · {leaf_unit}"
    if not intent_short:
        intent_short = f"{mid_unit} · {leaf_unit}"

    subj_short = "확통" if subject == "확률과 통계" else ("공통" if subject == "공통(수학I·II)" else subject)
    if month == "수능":
        prefix_ko = f"[{exam_year}학년도 수능 {grade} {subj_short} {qnum}번]"
        prefix_en = f"[{exam_year} CSAT {grade} {subj_short} #{qnum}]"
    else:
        prefix_ko = f"[{exam_year}학년도 {month} {grade} {subj_short} {qnum}번]"
        prefix_en = f"[{exam_year} AY {month} {grade} {subj_short} #{qnum}]"

    title_ko = f"{prefix_ko} {intent_short}"
    title_en = f"{prefix_en} {tpl['topic_en']}"

    tags = []
    for t in [subject, grade, month, f"{exam_year}학년도", f"{qnum}번"] + unit_parts[-3:]:
        t_clean = re.sub(r"\s+", "", str(t))
        if t_clean and t_clean not in tags and "개정" not in t_clean:
            tags.append(t_clean)
    if subject not in tags:
        tags.insert(0, subject)

    text_exp_lines = []
    for line in exp_lines:
        stripped = re.sub(r"<img[^>]*>", "", line).strip()
        stripped = re.sub(r"^(?:<br\s*/?>)+|(?:<br\s*/?>)+$", "", stripped).strip()
        if len(re.sub(r"<[^>]+>", "", stripped).strip()) >= 3:
            text_exp_lines.append(stripped)

    correct_opt_str = options[ans_idx - 1] if 1 <= ans_idx <= len(options) else options[0]

    step1_q = dict(tpl["step1"])
    step2_q = dict(tpl["step2"])

    step3_line = text_exp_lines[0] if len(text_exp_lines) >= 1 else (
        f"출발 조건으로부터 {correct_opt_str}을 유도하는 첫 관계식을 세웁니다."
    )
    step4_line = (
        text_exp_lines[len(text_exp_lines) // 2]
        if len(text_exp_lines) >= 2
        else step3_line
    )
    step5_line = (
        text_exp_lines[-1]
        if len(text_exp_lines) >= 3
        else f"정리한 식으로부터 구하는 최종 목표값을 도출하면 정답은 {correct_opt_str}입니다."
    )

    seed_base = int(hashlib.md5(slug.encode("utf-8")).hexdigest()[:6], 16)
    step3_q_obj = extract_blank_question_from_line(
        line_html=step3_line,
        blank_name="(가)",
        step_num=3,
        leaf_unit=leaf_unit,
        fallback_tex=correct_opt_str,
        seed_int=seed_base + 1,
    )
    step4_q_obj = extract_blank_question_from_line(
        line_html=step4_line,
        blank_name="(나)",
        step_num=4,
        leaf_unit=leaf_unit,
        fallback_tex=correct_opt_str,
        seed_int=seed_base + 3,
    )

    step5_stem_ko = (
        f"1~4단계의 풀이 전개를 종합하여 마무리 계산을 수행할 때, "
        f"이 문항이 요구하는 <b>최종 목표값</b>은?<br>"
        f'<section style="margin-top:8px;padding:10px 14px;background:#fffbeb;border-left:4px solid #d97706;border-radius:8px">{step5_line}</section>'
    )
    step5_stem_en = (
        f"Combining Steps 1–4 to complete the final calculation, what is the target value?<br>"
        f'<section style="margin-top:8px;padding:10px 14px;background:#fffbeb;border-left:4px solid #d97706;border-radius:8px">{step5_line}</section>'
    )

    levels = [
        {
            "title": step1_q["title"],
            "title_en": step1_q["title_en"],
            "knowledge": step1_q["knowledge"],
            "knowledge_en": step1_q["knowledge_en"],
            "questions": [
                {
                    "level_label": "초등 직관 디딤돌 1",
                    "level_label_en": "Elementary Intuition Step 1",
                    "stem": step1_q["stem"],
                    "stem_en": step1_q["stem_en"],
                    "options": step1_q["options"],
                    "answer": step1_q["answer"],
                    "exp": step1_q["exp"],
                    "exp_en": step1_q["exp_en"],
                }
            ],
        },
        {
            "title": step2_q["title"],
            "title_en": step2_q["title_en"],
            "knowledge": step2_q["knowledge"],
            "knowledge_en": step2_q["knowledge_en"],
            "questions": [
                {
                    "level_label": "기호 번역 디딤돌 2",
                    "level_label_en": "Symbol Translation Step 2",
                    "stem": step2_q["stem"],
                    "stem_en": step2_q["stem_en"],
                    "options": step2_q["options"],
                    "answer": step2_q["answer"],
                    "exp": step2_q["exp"],
                    "exp_en": step2_q["exp_en"],
                }
            ],
        },
        {
            "title": f"🌱 3단계 · [출발 조건 식 세우기] {leaf_unit} 핵심 조건 수식화",
            "title_en": f"🌱 Step 3 · [Setting Up the Equation] Applying {tpl['topic_en']}",
            "knowledge": f"본문항 해결의 첫걸음은 문제의 조건을 <b>{leaf_unit}</b> 단원의 수식으로 옮기는 것입니다.<br>• <b>출발 식 및 원리</b>: {step3_line}",
            "knowledge_en": f"First, translate the problem conditions into the core equation of {tpl['topic_en']}.",
            "questions": [step3_q_obj],
        },
        {
            "title": f"🌳 4단계 · [풀이 전개] 핵심 관계식 정리 및 중간 식 도출",
            "title_en": "🌳 Step 4 · [Intermediate Derivation] Simplifying Key Relations",
            "knowledge": f"3단계에서 세운 출발 식을 정리하여 문제에서 요구하는 핵심 미지수 또는 관계식을 도출합니다.<br>• <b>중간 전개 과정</b>: {step4_line}",
            "knowledge_en": "Simplify the starting relation to derive the key intermediate expression.",
            "questions": [step4_q_obj],
        },
        {
            "title": "💎 5단계 · [최종 계산 조립] 디딤돌 조각을 합쳐 최종 정답 구하기",
            "title_en": "💎 Step 5 · [Final Synthesis] Computing the Target Value",
            "knowledge": f"1~4단계에서 확인한 원리와 중간 식을 결합하여 최종 목표값을 구합니다.<br>• <b>최종 마무리 계산</b>: {step5_line}",
            "knowledge_en": "Combine the previous steps to compute the final target value.",
            "questions": [
                {
                    "level_label": "최종 정답 조립 디딤돌 5",
                    "level_label_en": "Final Synthesis Step 5",
                    "stem": step5_stem_ko,
                    "stem_en": step5_stem_en,
                    "options": options,
                    "answer": ans_idx,
                    "exp": f"단계별 계산을 마무리하면 최종 결과는 <b>{correct_opt_str}</b> (<b>{ans_idx}번</b>)입니다.<br>• {step5_line}",
                    "exp_en": f"Completing the derivation yields {correct_opt_str} (Option #{ans_idx}).",
                }
            ],
        },
    ]

    exp_body_html = "<br>\n  ".join(exp_lines) if exp_lines else f"주어진 조건에 {leaf_unit}의 성질을 적용하면 정답은 {correct_opt_str}입니다."
    unit_breadcrumb = " &gt; ".join(unit_parts) if unit_parts else f"{subject} &gt; {tpl['topic_ko']}"

    sol_ko = (
        f"<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n"
        f"<p>본 문항은 <b>{unit_breadcrumb}</b> 단원에서 <b>{html.escape(intent_ko or leaf_unit)}</b> 능력을 평가하는 {point}점 기출문항입니다.</p>\n\n"
        f"<h4>📐 [단계별 상세 풀이 전개]</h4>\n"
        f"<p>\n  {exp_body_html}\n</p>\n\n"
        f"<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n"
        f"<p>\n  따라서 구하는 최종 정답은 <b>{correct_opt_str} (정답 {ans_idx}번)</b>입니다.\n</p>"
    )

    sol_en = (
        f"<h4>📋 [Problem Analysis &amp; Core Concepts]</h4>\n"
        f"<p>This {point}-point exam problem evaluates <b>{tpl['topic_en']}</b> ({html.escape(leaf_unit)}).</p>\n\n"
        f"<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n"
        f"<p>\n  {exp_body_html}\n</p>\n\n"
        f"<h4>✨ [Final Answer &amp; Verification]</h4>\n"
        f"<p>\n  Therefore, the correct answer is <b>{correct_opt_str} (Option #{ans_idx})</b>.\n</p>"
    )

    short_exp_ko = f"<b>[출제의도]</b> {html.escape(intent_ko or leaf_unit)}<br>{exp_body_html}"
    short_exp_en = f"<b>[Core Topic]</b> {tpl['topic_en']}<br>Correct Answer: {correct_opt_str}"

    return {
        "slug": slug,
        "itemId": parsed.get("item_id", ""),
        "examYear": exam_year,
        "month": month,
        "grade": grade,
        "subject": subject,
        "qNum": str(qnum),
        "point": point,
        "title": title_ko,
        "title_en": title_en,
        "summary_ko": f"{intent_ko or leaf_unit} · 초등 눈높이 5단계 디딤돌 퀴즈 및 시각적 도식화 해설",
        "summary_en": f"{tpl['topic_en']} · 5-Step Scaffolding Quiz & Visual Diagram Solution",
        "tags": tags,
        "symbols": tpl["symbols"],
        "levels": levels,
        "step3_q": step3_q_obj,
        "step4_q": step4_q_obj,
        "final": {
            "stem": stem_html,
            "stem_en": stem_html,
            "options": options,
            "answer": ans_idx,
            "exp": short_exp_ko,
            "exp_en": short_exp_en,
            "solution": sol_ko,
            "solution_en": sol_en,
        },
    }
