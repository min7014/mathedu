# -*- coding: utf-8 -*-
"""
csat2027_part3_prob.py
2027학년도 대학수학능력시험 수학 영역 선택과목 [확률과 통계] 23번 ~ 30번 (8문항)
Slugs: csat27_p23 ~ csat27_p30
"""


def _esc_svg(s: str) -> str:
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _wrap_visual_svg(title_left: str, title_right: str, inner_svg: str, height: int = 270, lang: str = "ko", caption: str = "") -> str:
    hdr = (
        "🎨 [그림으로 이해하는 시각적 도형·개념 다이어그램]"
        if lang == "ko"
        else "🎨 [Visual Geometric &amp; Conceptual Diagram]"
    )
    svg = (
        f'<svg class="mathedu-bespoke-svg" viewBox="0 0 680 {height}" xmlns="http://www.w3.org/2000/svg" '
        f'style="width:100%;max-width:680px;height:auto;display:block;margin:0 auto;border-radius:12px;'
        f'background:linear-gradient(145deg,#ffffff 0%,#f8fafc 100%);border:1.5px solid #cbd5e1;'
        f'box-shadow:0 4px 14px rgba(15,23,42,0.06)">'
        f'<rect x="12" y="10" width="656" height="32" rx="8" fill="#e0f2fe" stroke="#7dd3fc"/>'
        f'<text x="24" y="31" fill="#0369a1" font-size="11.8" font-weight="800" font-family="sans-serif">{_esc_svg(title_left)}</text>'
        f'<text x="656" y="31" fill="#047857" font-size="11.8" font-weight="800" text-anchor="end" font-family="sans-serif">{_esc_svg(title_right)}</text>'
        f'{inner_svg}'
        f'</svg>'
    )
    return (
        f'<h4>{hdr}</h4>\n'
        f'<figure class="math-visual-diagram" style="margin:12px 0 18px;padding:14px;background:#f8fafc;border:1.5px solid #cbd5e1;border-radius:14px;text-align:center">'
        f'{svg}'
        f'<figcaption style="margin-top:10px;font-size:0.85rem;color:#475569;line-height:1.55">{caption}</figcaption>'
        f'</figure>'
    )


def _wrap_schematic_flow(steps_4: list, ans_tex: str, lang: str = "ko") -> str:
    hdr = (
        "🗺️ [한눈에 보는 도식화 풀이 흐름도 (Schematic Solution Flowchart)]"
        if lang == "ko"
        else "🗺️ [At-a-Glance Schematic Solution Flowchart]"
    )
    badges = (
        ["STEP 1 · 조건 해독", "STEP 2 · 핵심 원리", "STEP 3 · 수식 전개", "STEP 4 · 결합 계산"]
        if lang == "ko"
        else ["STEP 1 · Condition", "STEP 2 · Core Rule", "STEP 3 · Derivation", "STEP 4 · Synthesis"]
    )
    ans_lbl = "🎯 최종 정답" if lang == "ko" else "🎯 Final Answer"
    cells = []
    for idx, txt in enumerate(steps_4):
        cells.append(
            f'<td style="background:#ffffff;border:1px solid #cbd5e1;border-radius:10px;padding:10px 11px;vertical-align:top;width:20%">'
            f'<b style="color:#0369a1;font-size:0.77rem;display:block;margin-bottom:4px">{badges[idx]}</b>'
            f'<span style="color:#1e293b;font-size:0.85rem;line-height:1.45">{txt}</span>'
            f'</td>'
        )
        if idx < len(steps_4) - 1:
            cells.append(
                '<td style="text-align:center;vertical-align:middle;color:#d97706;font-weight:900;font-size:1.05rem;padding:0 3px">➔</td>'
            )
    cells.append(
        '<td style="text-align:center;vertical-align:middle;color:#059669;font-weight:900;font-size:1.05rem;padding:0 3px">⇒</td>'
        f'<td style="background:#ecfdf5;border:1.5px solid #10b981;border-radius:10px;padding:10px 11px;vertical-align:middle;text-align:center;width:15%">'
        f'<b style="color:#047857;font-size:0.77rem;display:block;margin-bottom:4px">{ans_lbl}</b>'
        f'<b style="color:#065f46;font-size:0.96rem">{ans_tex}</b>'
        f'</td>'
    )
    return (
        f'<h4>{hdr}</h4>\n'
        f'<section class="math-schematic-flow" style="margin:12px 0 18px;padding:14px;background:#f8fafc;border:1px solid #cbd5e1;border-radius:14px">'
        f'<table style="width:100%;border-collapse:separate;border-spacing:4px"><tr>{"".join(cells)}</tr></table>'
        f'</section>'
    )


# ---------------------------------------------------------------------------
# Official Exam Illustrations (orig_svg) for P28 (9 Cards) and P30 (Pouch)
# ---------------------------------------------------------------------------
ORIG_SVG_P28 = (
    '<svg viewBox="0 0 560 92" xmlns="http://www.w3.org/2000/svg" '
    'style="width:100%;max-width:540px;height:auto;display:block;margin:12px auto">'
    '<defs><style>'
    '.c-back{fill:#cbd5e1;stroke:#475569;stroke-width:1.2}'
    '.c-front{fill:#ffffff;stroke:#1e293b;stroke-width:1.5}'
    '.c-num{fill:#0f172a;font-family:Georgia,serif;font-size:18px;font-weight:700;text-anchor:middle}'
    '.c-frac{fill:#0f172a;font-family:Georgia,serif;font-size:14px;font-weight:700;text-anchor:middle}'
    '</style></defs>'
    + "".join(
        f'<g transform="translate({16 + idx * 59}, 14) rotate({-3 if idx % 2 == 0 else 2.5}, 22, 31)">'
        f'<rect x="3" y="3" width="42" height="58" rx="4" class="c-back"/>'
        f'<rect x="0" y="0" width="42" height="58" rx="4" class="c-front"/>'
        + (
            '<text x="21" y="23" class="c-frac">1</text>'
            '<line x1="12" y1="29" x2="30" y2="29" stroke="#0f172a" stroke-width="1.5"/>'
            '<text x="21" y="46" class="c-frac">2</text>'
            if lbl == "1/2"
            else f'<text x="21" y="36" class="c-num">{lbl}</text>'
        )
        + "</g>"
        for idx, lbl in enumerate(["1/2", "1/2", "1", "1", "1", "2", "2", "2", "4"])
    )
    + "</svg>"
)

ORIG_SVG_P30 = (
    '<svg viewBox="0 0 280 232" xmlns="http://www.w3.org/2000/svg" '
    'style="width:100%;max-width:260px;height:auto;display:block;margin:12px auto">'
    # Pouch top ruffle
    '<path d="M 106 24 Q 140 16 174 24 L 160 54 L 120 54 Z" fill="#f1f5f9" stroke="#334155" stroke-width="1.6"/>'
    '<path d="M 122 24 L 130 52 M 140 21 L 140 52 M 158 24 L 150 52" stroke="#64748b" stroke-width="1.1"/>'
    # Pouch body
    '<path d="M 120 54 C 66 78, 48 138, 66 184 C 80 214, 200 214, 214 184 C 232 138, 214 78, 160 54 Z" '
    'fill="#f8fafc" stroke="#1e293b" stroke-width="1.8"/>'
    # Subtle cloth crease lines
    '<path d="M 122 57 C 96 76, 84 96, 80 112" fill="none" stroke="#94a3b8" stroke-width="1.1"/>'
    '<path d="M 158 57 C 184 76, 196 96, 200 112" fill="none" stroke="#94a3b8" stroke-width="1.1"/>'
    # Drawstring tie
    '<rect x="116" y="50" width="48" height="7" rx="3.5" fill="#cbd5e1" stroke="#334155" stroke-width="1.4"/>'
    # 6 cards inside pouch (2 rows x 3 cols)
    + "".join(
        f'<g transform="translate({86 + (n - 1) % 3 * 39}, {104 + ((n - 1) // 3) * 48})">'
        f'<rect x="2" y="2" width="30" height="38" rx="3" fill="#cbd5e1" stroke="#475569" stroke-width="1"/>'
        f'<rect x="0" y="0" width="30" height="38" rx="3" fill="#ffffff" stroke="#1e293b" stroke-width="1.5"/>'
        f'<text x="15" y="25" fill="#0f172a" font-family="Georgia,serif" font-size="16" font-weight="700" text-anchor="middle">{n}</text>'
        f'</g>'
        for n in range(1, 7)
    )
    + "</svg>"
)

# Clean HTML probability distribution tables for P29 (no <div> tags!)
P29_TABLE_KO = (
    '<table style="width:100%;max-width:560px;margin:12px auto;border-collapse:collapse;text-align:center;font-size:0.94rem;background:#ffffff;border:1.5px solid #334155">'
    '<thead><tr style="background:#f1f5f9;border-bottom:1.5px solid #334155">'
    '<th style="padding:7px 8px;border:1px solid #64748b">$X$</th>'
    '<th style="padding:7px 8px;border:1px solid #64748b">$-3k$</th>'
    '<th style="padding:7px 8px;border:1px solid #64748b">$-2k$</th>'
    '<th style="padding:7px 8px;border:1px solid #64748b">$-k$</th>'
    '<th style="padding:7px 8px;border:1px solid #64748b">$k$</th>'
    '<th style="padding:7px 8px;border:1px solid #64748b">$2k$</th>'
    '<th style="padding:7px 8px;border:1px solid #64748b">$3k$</th>'
    '<th style="padding:7px 8px;border:1px solid #64748b">합계</th>'
    '</tr></thead>'
    '<tbody><tr>'
    '<td style="padding:8px;border:1px solid #64748b;background:#f8fafc;font-weight:700">$\\mathrm{P}(X=x)$</td>'
    '<td style="padding:8px;border:1px solid #64748b">$a^2$</td>'
    '<td style="padding:8px;border:1px solid #64748b">$b$</td>'
    '<td style="padding:8px;border:1px solid #64748b">$a$</td>'
    '<td style="padding:8px;border:1px solid #64748b">$a$</td>'
    '<td style="padding:8px;border:1px solid #64748b">$b$</td>'
    '<td style="padding:8px;border:1px solid #64748b">$a^2$</td>'
    '<td style="padding:8px;border:1px solid #64748b">$1$</td>'
    '</tr></tbody></table>'
)

P29_TABLE_EN = P29_TABLE_KO.replace(">합계<", ">Total<")

# ---------------------------------------------------------------------------
# Bespoke Visual Solution Diagrams for P23 ~ P30
# ---------------------------------------------------------------------------
_SVG_P23_INNER = (
    "".join(
        f'<rect x="{22 + i * 91}" y="62" width="76" height="86" rx="10" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.6"/>'
        f'<text x="{60 + i * 91}" y="83" fill="#1d4ed8" font-size="11.5" font-weight="800" text-anchor="middle">{i+1}번째 자리</text>'
        f'<rect x="{30 + i * 91}" y="92" width="26" height="24" rx="5" fill="#ffffff" stroke="#60a5fa"/>'
        f'<text x="{43 + i * 91}" y="109" fill="#0f172a" font-size="12" font-weight="700" text-anchor="middle">a</text>'
        f'<rect x="{64 + i * 91}" y="92" width="26" height="24" rx="5" fill="#ffffff" stroke="#60a5fa"/>'
        f'<text x="{77 + i * 91}" y="109" fill="#0f172a" font-size="12" font-weight="700" text-anchor="middle">b</text>'
        f'<text x="{60 + i * 91}" y="137" fill="#047857" font-size="11.5" font-weight="800" text-anchor="middle">2가지</text>'
        + (f'<text x="{105 + i * 91}" y="110" fill="#d97706" font-size="15" font-weight="900" text-anchor="middle">×</text>' if i < 6 else "")
        for i in range(7)
    )
    + '<rect x="90" y="168" width="500" height="48" rx="10" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.6"/>'
    + '<text x="340" y="197" fill="#92400e" font-size="14" font-weight="900" text-anchor="middle">중복순열 ₂Π₇ = 2 × 2 × 2 × 2 × 2 × 2 × 2 = 2⁷ = 128</text>'
)

_SVG_P24_INNER = (
    '<rect x="28" y="54" width="330" height="190" rx="12" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>'
    '<text x="44" y="75" fill="#334155" font-size="12" font-weight="800">표본공간 S (통분 기준: 분모 12)</text>'
    '<circle cx="152" cy="152" r="66" fill="rgba(59,130,246,0.16)" stroke="#2563eb" stroke-width="2"/>'
    '<circle cx="232" cy="152" r="62" fill="rgba(16,185,129,0.16)" stroke="#059669" stroke-width="2"/>'
    '<text x="116" y="146" fill="#1d4ed8" font-size="12" font-weight="800" text-anchor="middle">A만</text>'
    '<text x="116" y="166" fill="#1e293b" font-size="12" font-weight="700" text-anchor="middle">4/12</text>'
    '<text x="193" y="146" fill="#be123c" font-size="12.5" font-weight="900" text-anchor="middle">A ∩ B</text>'
    '<text x="193" y="166" fill="#be123c" font-size="13" font-weight="900" text-anchor="middle">2/12 = 1/6</text>'
    '<text x="268" y="146" fill="#047857" font-size="12" font-weight="800" text-anchor="middle">B만</text>'
    '<text x="268" y="166" fill="#1e293b" font-size="12" font-weight="700" text-anchor="middle">3/12</text>'
    '<rect x="380" y="54" width="276" height="190" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>'
    '<text x="518" y="80" fill="#0369a1" font-size="12.5" font-weight="800" text-anchor="middle">확률의 덧셈정리 포함·배제 원리</text>'
    '<text x="518" y="110" fill="#1e293b" font-size="12" font-weight="700" text-anchor="middle">P(A) = 1/2 = 6/12,  P(B) = 5/12</text>'
    '<text x="518" y="136" fill="#1e293b" font-size="12" font-weight="700" text-anchor="middle">P(A ∪ B) = 3/4 = 9/12</text>'
    '<text x="518" y="166" fill="#4f46e5" font-size="12" font-weight="800" text-anchor="middle">P(A ∩ B) = P(A) + P(B) - P(A ∪ B)</text>'
    '<rect x="404" y="184" width="228" height="42" rx="8" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.5"/>'
    '<text x="518" y="210" fill="#92400e" font-size="13" font-weight="900" text-anchor="middle">(6 + 5 - 9)/12 = 2/12 = 1/6</text>'
)

_SVG_P25_INNER = (
    '<rect x="24" y="58" width="194" height="168" rx="12" fill="#eff6ff" stroke="#60a5fa" stroke-width="1.6"/>'
    '<text x="121" y="84" fill="#1d4ed8" font-size="12.5" font-weight="800" text-anchor="middle">① 분산으로 시행 횟수 n 구하기</text>'
    '<text x="121" y="114" fill="#1e293b" font-size="12" font-weight="700" text-anchor="middle">σ(X) = 4 ⇒ V(X) = 16</text>'
    '<text x="121" y="142" fill="#1e293b" font-size="12" font-weight="700" text-anchor="middle">npq = n × (2/3) × (1/3) = 2n/9</text>'
    '<text x="121" y="174" fill="#0369a1" font-size="13" font-weight="900" text-anchor="middle">2n/9 = 16 ⇒ n = 72</text>'
    '<text x="233" y="146" fill="#d97706" font-size="20" font-weight="900" text-anchor="middle">➔</text>'
    '<rect x="248" y="58" width="184" height="168" rx="12" fill="#ecfdf5" stroke="#34d399" stroke-width="1.6"/>'
    '<text x="340" y="84" fill="#047857" font-size="12.5" font-weight="800" text-anchor="middle">② 평균 E(X) 구하기</text>'
    '<text x="340" y="118" fill="#1e293b" font-size="12" font-weight="700" text-anchor="middle">E(X) = np</text>'
    '<text x="340" y="146" fill="#1e293b" font-size="12" font-weight="700" text-anchor="middle">= 72 × (2/3)</text>'
    '<text x="340" y="176" fill="#047857" font-size="13.5" font-weight="900" text-anchor="middle">E(X) = 48</text>'
    '<text x="447" y="146" fill="#059669" font-size="20" font-weight="900" text-anchor="middle">⇒</text>'
    '<rect x="462" y="58" width="194" height="168" rx="12" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.8"/>'
    '<text x="559" y="88" fill="#b45309" font-size="12.5" font-weight="800" text-anchor="middle">③ 최종 합계 n + E(X)</text>'
    '<text x="559" y="130" fill="#1e293b" font-size="13" font-weight="800" text-anchor="middle">72 + 48</text>'
    '<text x="559" y="174" fill="#92400e" font-size="18" font-weight="900" text-anchor="middle">= 120</text>'
)

_SVG_P26_CELLS = []
for _r in range(1, 7):
    _SVG_P26_CELLS.append(
        f'<text x="40" y="{88 + (_r - 1) * 28}" fill="#334155" font-size="11.5" font-weight="800" text-anchor="middle">a={_r}</text>'
        f'<text x="{88 + (_r - 1) * 44}" y="64" fill="#334155" font-size="11.5" font-weight="800" text-anchor="middle">b={_r}</text>'
    )
    for _c in range(1, 7):
        _p = _r * _c
        if _p <= 4:
            _bg, _bd, _fg = "#ffe4e6", "#fb7185", "#be123c"
        elif _p >= 29:
            _bg, _bd, _fg = "#fef3c7", "#f59e0b", "#b45309"
        else:
            _bg, _bd, _fg = "#dcfce7", "#34d399", "#065f46"
        _SVG_P26_CELLS.append(
            f'<rect x="{68 + (_c - 1) * 44}" y="{70 + (_r - 1) * 28}" width="40" height="24" rx="4" fill="{_bg}" stroke="{_bd}" stroke-width="1.2"/>'
            f'<text x="{88 + (_c - 1) * 44}" y="{86 + (_r - 1) * 28}" fill="{_fg}" font-size="11" font-weight="800" text-anchor="middle">{_p}</text>'
        )

_SVG_P26_INNER = (
    "".join(_SVG_P26_CELLS)
    + '<rect x="356" y="64" width="300" height="176" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>'
    + '<text x="506" y="88" fill="#0369a1" font-size="12.5" font-weight="800" text-anchor="middle">여사건 격자 분할 (전체 36칸)</text>'
    + '<text x="506" y="116" fill="#be123c" font-size="11.8" font-weight="700" text-anchor="middle">• 분홍 (a×b ≤ 4): 4 + 2 + 1 + 1 = 8칸 제외</text>'
    + '<text x="506" y="142" fill="#b45309" font-size="11.8" font-weight="700" text-anchor="middle">• 노랑 (a×b ≥ 29): 30, 30, 36 = 3칸 제외</text>'
    + '<text x="506" y="168" fill="#047857" font-size="12" font-weight="800" text-anchor="middle">• 초록 (5 ≤ a×b ≤ 28): 36 - 11 = 25칸!</text>'
    + '<rect x="386" y="184" width="240" height="40" rx="8" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5"/>'
    + '<text x="506" y="209" fill="#065f46" font-size="13.5" font-weight="900" text-anchor="middle">구하는 확률 = 25 / 36</text>'
)

_SVG_P27_INNER = (
    # Bell curve & confidence interval on left
    '<path d="M 40 192 Q 110 190 150 132 Q 190 62 220 62 Q 250 62 290 132 Q 330 190 400 192" fill="rgba(56,189,248,0.15)" stroke="#0284c7" stroke-width="2.2"/>'
    '<line x1="28" y1="192" x2="412" y2="192" stroke="#334155" stroke-width="1.6"/>'
    '<line x1="124" y1="118" x2="124" y2="198" stroke="#be123c" stroke-width="1.8" stroke-dasharray="4,3"/>'
    '<line x1="220" y1="62" x2="220" y2="198" stroke="#0369a1" stroke-width="2"/>'
    '<line x1="316" y1="118" x2="316" y2="198" stroke="#be123c" stroke-width="1.8" stroke-dasharray="4,3"/>'
    '<text x="124" y="216" fill="#be123c" font-size="11.5" font-weight="800" text-anchor="middle">252.16</text>'
    '<text x="220" y="216" fill="#0369a1" font-size="12" font-weight="900" text-anchor="middle">x̄ = 260</text>'
    '<text x="316" y="216" fill="#be123c" font-size="11.5" font-weight="800" text-anchor="middle">267.84</text>'
    '<line x1="222" y1="156" x2="314" y2="156" stroke="#d97706" stroke-width="2"/>'
    '<text x="268" y="148" fill="#b45309" font-size="11" font-weight="800" text-anchor="middle">+7.84 = 1.96×(σ/8)</text>'
    # Right summary box
    '<rect x="426" y="56" width="234" height="176" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>'
    '<text x="543" y="82" fill="#0369a1" font-size="12" font-weight="800" text-anchor="middle">모평균 95% 신뢰구간 대칭성</text>'
    '<text x="543" y="110" fill="#1e293b" font-size="11.5" font-weight="700" text-anchor="middle">① 중점 x̄ = (252.16+267.84)/2 = 260</text>'
    '<text x="543" y="138" fill="#1e293b" font-size="11.5" font-weight="700" text-anchor="middle">② 1.96 × (σ/√64) = 7.84</text>'
    '<text x="543" y="164" fill="#047857" font-size="12" font-weight="800" text-anchor="middle">⇒ σ/8 = 4 ⇒ σ = 32</text>'
    '<rect x="444" y="180" width="198" height="38" rx="8" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.5"/>'
    '<text x="543" y="204" fill="#92400e" font-size="13" font-weight="900" text-anchor="middle">x̄ + σ = 260 + 32 = 292</text>'
)

_SVG_P28_INNER = (
    # 4 Even Barrier Cards + 5 Gap Slots
    '<text x="340" y="66" fill="#0f172a" font-size="12" font-weight="800" text-anchor="middle">'
    '핵심 번역: 1/2과 1만 이웃 금지! ➔ 짝수 장벽 {2, 2, 2, 4} 나열 (4!/3! = 4가지) 후 5개 빈칸 분리 배치'
    '</text>'
    + "".join(
        f'<rect x="{38 + i * 130}" y="82" width="54" height="44" rx="8" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.6" stroke-dasharray="4,2"/>'
        f'<text x="{65 + i * 130}" y="109" fill="#b45309" font-size="12" font-weight="800" text-anchor="middle">빈칸 {i+1}</text>'
        + (
            f'<rect x="{104 + i * 130}" y="80" width="46" height="48" rx="7" fill="#dbeafe" stroke="#2563eb" stroke-width="1.8"/>'
            f'<text x="{127 + i * 130}" y="109" fill="#1e3a8a" font-size="13.5" font-weight="900" text-anchor="middle">{"2" if i < 3 else "4"}</text>'
            if i < 4
            else ""
        )
        for i in range(5)
    )
    + '<rect x="28" y="144" width="302" height="96" rx="10" fill="#eff6ff" stroke="#60a5fa" stroke-width="1.5"/>'
    + '<text x="179" y="168" fill="#1d4ed8" font-size="12" font-weight="800" text-anchor="middle">케이스 (i) 1/2 두 장이 같은 빈칸</text>'
    + '<text x="179" y="192" fill="#1e293b" font-size="11.5" font-weight="700" text-anchor="middle">빈칸 택1 (₅C₁=5) × 남은 4칸에 1 세 장 (₄H₃=20)</text>'
    + '<text x="179" y="218" fill="#0369a1" font-size="12.5" font-weight="900" text-anchor="middle">짝수 나열 4 × 5 × 20 = 400가지</text>'
    + '<rect x="350" y="144" width="302" height="96" rx="10" fill="#ecfdf5" stroke="#34d399" stroke-width="1.5"/>'
    + '<text x="501" y="168" fill="#047857" font-size="12" font-weight="800" text-anchor="middle">케이스 (ii) 1/2 두 장이 서로 다른 빈칸</text>'
    + '<text x="501" y="192" fill="#1e293b" font-size="11.5" font-weight="700" text-anchor="middle">빈칸 택2 (₅C₂=10) × 남은 3칸에 1 세 장 (₃H₃=10)</text>'
    + '<text x="501" y="218" fill="#065f46" font-size="12.5" font-weight="900" text-anchor="middle">짝수 나열 4 × 10 × 10 = 400가지 (합 800)</text>'
)

_SVG_P29_INNER = (
    # Left: Symmetric bars & V(X)=1
    '<rect x="22" y="54" width="304" height="192" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>'
    '<text x="174" y="76" fill="#0369a1" font-size="12" font-weight="800" text-anchor="middle">① 원점 대칭 분포 (E(X)=0) &amp; 1 ≤ V(X) ≤ σ(X)</text>'
    '<line x1="42" y1="176" x2="306" y2="176" stroke="#334155" stroke-width="1.5"/>'
    '<rect x="56" y="150" width="22" height="26" rx="3" fill="#93c5fd"/><text x="67" y="192" fill="#334155" font-size="10" font-weight="700" text-anchor="middle">-3k</text>'
    '<rect x="92" y="140" width="22" height="36" rx="3" fill="#6ee7b7"/><text x="103" y="192" fill="#334155" font-size="10" font-weight="700" text-anchor="middle">-2k</text>'
    '<rect x="128" y="106" width="22" height="70" rx="3" fill="#fcd34d"/><text x="139" y="192" fill="#334155" font-size="10" font-weight="700" text-anchor="middle">-k</text>'
    '<line x1="174" y1="94" x2="174" y2="184" stroke="#be123c" stroke-width="1.5" stroke-dasharray="3,3"/>'
    '<rect x="198" y="106" width="22" height="70" rx="3" fill="#fcd34d"/><text x="209" y="192" fill="#334155" font-size="10" font-weight="700" text-anchor="middle">k</text>'
    '<rect x="234" y="140" width="22" height="36" rx="3" fill="#6ee7b7"/><text x="245" y="192" fill="#334155" font-size="10" font-weight="700" text-anchor="middle">2k</text>'
    '<rect x="270" y="150" width="22" height="26" rx="3" fill="#93c5fd"/><text x="281" y="192" fill="#334155" font-size="10" font-weight="700" text-anchor="middle">3k</text>'
    '<text x="174" y="218" fill="#be123c" font-size="11.5" font-weight="800" text-anchor="middle">1 ≤ s² ≤ s (s≥0) ⇔ s = 1 ⇔ V(X) = 1</text>'
    '<text x="174" y="236" fill="#475569" font-size="11" font-weight="700" text-anchor="middle">2a² + 2a + 2b = 1 ⇒ 8b = 4 - 8a - 8a²</text>'
    # Right: Smooth quadratic curve f(a) = 10(a - 3/10)^2 + 31/10
    '<rect x="344" y="54" width="314" height="192" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>'
    '<text x="501" y="76" fill="#047857" font-size="12" font-weight="800" text-anchor="middle">② f(a) = 10a² - 6a + 4 최솟값 ➔ k² 최댓값</text>'
    '<path d="M 390 100 Q 485 218 580 100" fill="none" stroke="#4f46e5" stroke-width="2.4"/>'
    '<circle cx="485" cy="159" r="5" fill="#be123c"/>'
    '<text x="485" y="182" fill="#be123c" font-size="11.5" font-weight="800" text-anchor="middle">꼭짓점 a = 3/10, 최솟값 31/10 (b=11/100&gt;0)</text>'
    '<rect x="372" y="196" width="258" height="38" rx="8" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.5"/>'
    '<text x="501" y="220" fill="#92400e" font-size="12.5" font-weight="900" text-anchor="middle">max(k²) = 10 / 31 ⇒ p + q = 31 + 10 = 41</text>'
)

_SVG_P30_INNER = (
    # Left: 20 subsets partitioned by score X_i = I_A + I_B
    '<rect x="20" y="54" width="308" height="192" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>'
    '<text x="174" y="76" fill="#0369a1" font-size="12" font-weight="800" text-anchor="middle">① 1회 시행 ₆C₃ = 20가지의 점수 Xᵢ 분할</text>'
    '<rect x="34" y="88" width="280" height="44" rx="7" fill="#eff6ff" stroke="#60a5fa"/>'
    '<text x="174" y="106" fill="#1d4ed8" font-size="11.5" font-weight="800" text-anchor="middle">Xᵢ = 2점 (A ∩ B): 총 6가지</text>'
    '<text x="174" y="124" fill="#1e293b" font-size="10.8" font-weight="700" text-anchor="middle">★ 6 포함: (1,2,6),(1,5,6),(2,4,6),(4,5,6) ➔ 4가지</text>'
    '<rect x="34" y="140" width="280" height="44" rx="7" fill="#ecfdf5" stroke="#34d399"/>'
    '<text x="174" y="158" fill="#047857" font-size="11.5" font-weight="800" text-anchor="middle">Xᵢ = 1점 (A만 또는 B만): 총 12가지</text>'
    '<text x="174" y="176" fill="#1e293b" font-size="10.8" font-weight="700" text-anchor="middle">★ 6 포함: 전체 ₅C₂=10 중 Xᵢ=2인 4개 제외 ➔ 6가지</text>'
    '<rect x="34" y="192" width="280" height="42" rx="7" fill="#ffe4e6" stroke="#fb7185"/>'
    '<text x="174" y="210" fill="#be123c" font-size="11.5" font-weight="800" text-anchor="middle">Xᵢ = 0점 (Aᶜ ∩ Bᶜ): (1,2,4),(1,3,4) 총 2가지</text>'
    '<text x="174" y="226" fill="#9f1239" font-size="10.8" font-weight="700" text-anchor="middle">★ 최댓값 ≤ 4이므로 6 포함: 0가지!</text>'
    # Right: 3-trial sum a+b=4 conditional probability
    '<rect x="344" y="54" width="316" height="192" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>'
    '<text x="502" y="76" fill="#4f46e5" font-size="12" font-weight="800" text-anchor="middle">② 3회 합 a+b = X₁+X₂+X₃ = 4 조건부확률</text>'
    '<text x="502" y="104" fill="#1e293b" font-size="11.5" font-weight="700" text-anchor="middle">• (2,2,0)형: 전체 3×6²×2 = 216 (모두 6 포함: 0)</text>'
    '<text x="502" y="130" fill="#1e293b" font-size="11.5" font-weight="700" text-anchor="middle">• (2,1,1)형: 전체 3×6×12² = 2592 = 216×12</text>'
    '<text x="502" y="154" fill="#047857" font-size="11.5" font-weight="800" text-anchor="middle">• (2,1,1)형 중 3회 모두 6 포함: 3×4×6² = 432 = 216×2</text>'
    '<rect x="366" y="172" width="272" height="60" rx="8" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.6"/>'
    '<text x="502" y="196" fill="#92400e" font-size="12.5" font-weight="900" text-anchor="middle">확률 = 432 / (216 + 2592) = 432 / 2808 = 2 / 13</text>'
    '<text x="502" y="220" fill="#b45309" font-size="13" font-weight="900" text-anchor="middle">∴ p + q = 13 + 2 = 15</text>'
)


PART3_PROBLEMS = [
    # =========================================================================
    # 확통 23번 (csat27_p23) — 2점, 정답 3 (128)
    # =========================================================================
    {
        'slug': 'csat27_p23',
        'qNum': '23',
        'points': 2,
        'is_short_answer': False,
        'official_ans_str': '',
        'subject': '확률과 통계',
        'title': '[2027학년도 수능 고3 확통 23번] 중복순열을 이용한 문자열 일렬 나열의 경우의 수',
        'title_en': '[2027 CSAT Math Prob & Stat #23] Permutations with Repetition of Two Letters in 7 Positions',
        'summary_ko': r'서로 다른 $2$개의 문자 $a, b$ 중에서 중복을 허용하여 $7$개를 택해 일렬로 나열하는 중복순열 ${}_{2}\Pi_{7} = 2^7 = 128$ 구하기',
        'summary_en': r'Compute the number of permutations with repetition ${}_{2}\Pi_{7} = 2^7 = 128$ when arranging $7$ characters chosen from $\{a, b\}$.',
        'tags': ['확률과 통계', '2027학년도 수능', '경우의수', '중복순열', '거듭제곱', '23번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': r'${}_{n}\Pi_{r} = n^r$',
                'desc': r'서로 다른 $n$개에서 중복을 허용하여 $r$개를 택해 일렬로 나열하는 중복순열의 수 ($n$을 $r$번 곱하기)',
                'desc_en': r'Number of permutations with repetition of $r$ items chosen from $n$ distinct types ($n$ multiplied $r$ times).',
            },
            {
                'sym': r'$a, b$',
                'desc': r'각 자리에 들어갈 수 있는 $2$가지 선택지(문자)',
                'desc_en': r'The $2$ available letter choices for each position.',
            },
            {
                'sym': r'$2^7$',
                'desc': r'$7$개의 자리마다 $2$가지씩 선택하여 곱한 값 ($2 \times 2 \times 2 \times 2 \times 2 \times 2 \times 2$)',
                'desc_en': r'Product of $2$ choices across each of the $7$ positions.',
            },
        ],
        'levels': [
            {
                'title': r'🔰 1단계 · [초등 기초 직관] $2$칸에 $a, b$를 채우는 가짓수 직접 세기',
                'title_en': r'🔰 Step 1 · [Elementary Intuition] Counting ways to fill $2$ slots with $a$ or $b$',
                'knowledge': r'초등학교 곱셈 규칙처럼 빈칸이 $2$개 있을 때 각 칸에 $a$ 또는 $b$를 넣으면 $(a,a), (a,b), (b,a), (b,b)$로 $2 \times 2 = 4$가지가 됩니다.',
                'knowledge_en': r'By elementary multiplication, filling $2$ slots where each slot can be $a$ or $b$ gives $(a,a), (a,b), (b,a), (b,b)$, which is $2 \times 2 = 4$ ways.',
                'questions': [
                    {
                        'level_label': '초등 기초 직관 디딤돌 1',
                        'level_label_en': 'Elementary Intuition Step 1',
                        'stem': r'초등학교 곱셈 규칙으로 $2$개의 빈칸 각각에 문자 $a$ 또는 $b$를 중복을 허용하여 넣는 경우의 수 $2 \times 2$는?',
                        'stem_en': r'Using elementary multiplication, how many ways can $2$ slots each be filled with $a$ or $b$ ($2 \times 2$)?',
                        'options': [r'$2$', r'$4$', r'$6$', r'$8$', r'$10$'],
                        'answer': 2,
                        'exp': r'첫째 칸에 $2$가지, 둘째 칸에 $2$가지이므로 $2 \times 2 = 4$가지입니다.',
                        'exp_en': r'$2$ choices for Slot 1 times $2$ choices for Slot 2 gives $2 \times 2 = 4$ ways.',
                    }
                ],
            },
            {
                'title': r'🌿 2단계 · [기호 번역 브릿지] $7$개의 자리를 채우는 중복순열 기호로 나타내기',
                'title_en': r'🌿 Step 2 · [Symbol Bridge] Expressing $7$ slots as ${}_{2}\Pi_{7} = 2^7$',
                'knowledge': r'일렬로 놓인 $7$개의 자리마다 독립적으로 $a$ 또는 $b$의 $2$가지 선택지가 있으므로 곱의 법칙에 의해 ${}_{2}\Pi_{7} = 2^7$입니다.',
                'knowledge_en': r'Each of the $7$ positions in a row independently has $2$ choices ($a$ or $b$), giving ${}_{2}\Pi_{7} = 2^7$ by the multiplication rule.',
                'questions': [
                    {
                        'level_label': '중복순열 식 세우기 디딤돌 2',
                        'level_label_en': 'Formula Setup Step 2',
                        'stem': r'$2$개의 문자 $a, b$ 중에서 중복을 허용하여 $7$개를 택해 일렬로 나열하는 경우의 수를 거듭제곱으로 바르게 나타낸 것은?',
                        'stem_en': r'Which power correctly represents the number of ways to arrange $7$ letters chosen with repetition from $\{a, b\}$?',
                        'options': [r'$2 \times 7$', r'$7^2$', r'$2^7$', r'$2^6$', r'$7!$'],
                        'answer': 3,
                        'exp': r'각 자리마다 $2$가지씩 총 $7$번 곱하므로 ${}_{2}\Pi_{7} = 2^7$입니다.',
                        'exp_en': r'Multiplying $2$ choices across $7$ positions yields ${}_{2}\Pi_{7} = 2^7$.',
                    }
                ],
            },
            {
                'title': r'🌱 3단계 · [부분 거듭제곱 계산] $2^4$과 $2^3$ 각각 구하기',
                'title_en': r'🌱 Step 3 · [Partial Powers] Computing $2^4$ and $2^3$',
                'knowledge': r'큰 거듭제곱은 지수법칙 $2^7 = 2^4 \times 2^3$으로 쪼개어 계산하면 실수가 없습니다. $2^4 = 16$, $2^3 = 8$입니다.',
                'knowledge_en': r'Splitting $2^7 = 2^4 \times 2^3$ prevents arithmetic errors: $2^4 = 16$ and $2^3 = 8$.',
                'questions': [
                    {
                        'level_label': '거듭제곱 쪼개기 디딤돌 3',
                        'level_label_en': 'Power Splitting Step 3',
                        'stem': r'$2^4$과 $2^3$의 값을 순서대로 바르게 짝지은 것은?',
                        'stem_en': r'What are the values of $2^4$ and $2^3$, respectively?',
                        'options': [r'$8,\; 6$', r'$12,\; 8$', r'$16,\; 6$', r'$16,\; 8$', r'$32,\; 8$'],
                        'answer': 4,
                        'exp': r'$2^4 = 2 \times 2 \times 2 \times 2 = 16$이고 $2^3 = 2 \times 2 \times 2 = 8$입니다.',
                        'exp_en': r'$2^4 = 16$ and $2^3 = 8$.',
                    }
                ],
            },
            {
                'title': r'🌳 4단계 · [곱셈 결합] $16 \times 8$ 계산하기',
                'title_en': r'🌳 Step 4 · [Multiplication] Computing $16 \times 8$',
                'knowledge': r'분배법칙을 쓰면 $16 \times 8 = (10 + 6) \times 8 = 80 + 48$로 암산할 수 있습니다.',
                'knowledge_en': r'Using the distributive law, $16 \times 8 = (10 + 6) \times 8 = 80 + 48$.',
                'questions': [
                    {
                        'level_label': '두 자리 곱셈 디딤돌 4',
                        'level_label_en': 'Distributive Product Step 4',
                        'stem': r'$16 \times 8 = (10 + 6) \times 8 = 80 + [\;\text{(가)}\;]$에서 $[\;\text{(가)}\;]$에 알맞은 수는?',
                        'stem_en': r'In $16 \times 8 = (10 + 6) \times 8 = 80 + [\;\text{(A)}\;]$, what number goes in $[\;\text{(A)}\;]$?',
                        'options': [r'$36$', r'$42$', r'$48$', r'$54$', r'$56$'],
                        'answer': 3,
                        'exp': r'$6 \times 8 = 48$이므로 $[\;\text{(가)}\;] = 48$입니다.',
                        'exp_en': r'Since $6 \times 8 = 48$, $[\;\text{(A)}\;] = 48$.',
                    }
                ],
            },
            {
                'title': r'💎 5단계 · [최종 종합] $2^7$의 값 확정하기',
                'title_en': r'💎 Step 5 · [Final Synthesis] Confirming $2^7 = 128$',
                'knowledge': r'$80 + 48 = 128$이므로 구하는 경우의 수는 $128$입니다.',
                'knowledge_en': r'Adding $80 + 48 = 128$ gives the total number of arrangements.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': r'$2$개의 문자 $a, b$ 중에서 중복을 허용하여 $7$개를 택해 일렬로 나열하는 경우의 수 $2^7$은?',
                        'stem_en': r'What is $2^7$, the number of ways to arrange $7$ letters chosen with repetition from $\{a, b\}$?',
                        'options': [r'$120$', r'$124$', r'$128$', r'$132$', r'$136$'],
                        'answer': 3,
                        'exp': r'${}_{2}\Pi_{7} = 2^7 = 80 + 48 = 128$이므로 정답은 ③번입니다.',
                        'exp_en': r'${}_{2}\Pi_{7} = 2^7 = 128$ (choice ③).',
                    }
                ],
            },
        ],
        'final': {
            'stem': r'$2$개의 문자 $a, b$ 중에서 중복을 허용하여 $7$개를 택해 일렬로 나열하는 경우의 수는? [2점]',
            'stem_en': r'What is the number of ways to choose $7$ letters with repetition from the $2$ letters $a, b$ and arrange them in a row? [2 points]',
            'options': [r'$120$', r'$124$', r'$128$', r'$132$', r'$136$'],
            'answer': 3,
            'exp': r'일렬로 놓인 $7$개의 자리 각각에 문자 $a$ 또는 $b$의 $2$가지 중 하나를 중복을 허용하여 선택할 수 있으므로, 곱의 법칙(중복순열)에 의해 구하는 경우의 수는 ${}_{2}\Pi_{7} = 2^7 = 128$입니다.',
            'exp_en': r'Each of the $7$ positions in the row can independently be filled with either $a$ or $b$ ($2$ choices), so by permutations with repetition the total number of arrangements is ${}_{2}\Pi_{7} = 2^7 = 128$.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 서로 다른 $2$개의 문자 $a, b$에서 중복을 허용하여 $7$개를 뽑아 일렬로 배열하는 <b>중복순열(${}_{n}\\Pi_{r} = n^r$)</b>의 기본 원리를 정확히 이해하고 있는지 확인하는 문항입니다.</p>\n'
                + _wrap_visual_svg(
                    "📐 [2027 수능 확통 23번] 7개 자리에 {a, b} 중복 허용 배치",
                    "₂Π₇ = 2⁷ = 128",
                    _SVG_P23_INNER,
                    height=232,
                    lang="ko",
                    caption="▲ 1번째 자리부터 7번째 자리까지 매번 독립적으로 a 또는 b의 2가지 선택지가 열려 있으므로 2를 7번 곱한 128가지가 됩니다.",
                )
                + _wrap_schematic_flow(
                    [
                        r"선택 문자 $\{a, b\}$ ($n=2$)",
                        r"일렬 나열 자리 수 $r=7$",
                        r"중복순열 공식 ${}_{2}\Pi_{7} = 2^7$",
                        r"$2^4 \times 2^3 = 16 \times 8$",
                    ],
                    r"$128$ (③)",
                    lang="ko",
                )
                + '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: 자리별 선택 가짓수 파악하기</b><br>\n'
                '  일렬로 나열할 $7$개의 빈칸을 왼쪽부터 차례대로 제$1$칸, 제$2$칸, $\\cdots$, 제$7$칸이라 합시다. 중복을 허용하므로 앞 칸에 어떤 문자를 넣었는지와 관계없이 매 칸마다 $a$ 또는 $b$의 <b>$2$가지</b> 중 하나를 넣을 수 있습니다.<br><br>\n'
                '  <b>2단계: 중복순열 공식 적용 및 계산</b><br>\n'
                '  곱의 법칙에 의해 구하는 경우의 수는 서로 다른 $2$개에서 $7$개를 택하는 중복순열의 수와 같습니다.\n'
                '  $${}_{2}\\Pi_{7} = 2^7 = 2^4 \\times 2^3 = 16 \\times 8 = 128$$\n'
                '</p>\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>따라서 구하는 경우의 수는 <b>$128$</b>이므로 정답은 <b>③번</b>입니다. (실전 팁: 중복순열 $n^r$에서 밑 $n$은 <i>선택당하는 후보의 개수($2$개)</i>이고, 지수 $r$은 <i>채워야 할 자리의 개수($7$자리)</i>임을 바뀌지 않게 점검하고, <a href="https://min7014.github.io/" target="_blank" rel="noopener">수학자료실(min7014.github.io)</a>의 경우의 수·순열 시각 자료도 함께 탐구해 보세요.)</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis &amp; Core Concepts]</h4>\n'
                '<p>This problem tests <b>permutations with repetition (${}_{n}\\Pi_{r} = n^r$)</b> when filling $7$ ordered positions using characters from the $2$-element set $\\{a, b\\}$.</p>\n'
                + _wrap_visual_svg(
                    "📐 [2027 CSAT Prob & Stat #23] 7 Ordered Slots with {a, b}",
                    "2^7 = 128",
                    _SVG_P23_INNER,
                    height=232,
                    lang="en",
                    caption="▲ Each of the 7 ordered positions independently admits 2 choices (a or b), yielding 2^7 = 128 arrangements.",
                )
                + _wrap_schematic_flow(
                    [
                        r"Candidate letters $\{a, b\}$ ($n=2$)",
                        r"Ordered positions $r=7$",
                        r"Formula ${}_{2}\Pi_{7} = 2^7$",
                        r"$2^4 \times 2^3 = 16 \times 8$",
                    ],
                    r"$128$ (③)",
                    lang="en",
                )
                + '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Independent choices per slot</b><br>\n'
                '  Because repetition is allowed, each of the $7$ positions in the row has exactly $2$ choices ($a$ or $b$).<br><br>\n'
                '  <b>Step 2: Apply the multiplication principle</b><br>\n'
                '  $${}_{2}\\Pi_{7} = 2^7 = 16 \\times 8 = 128$$\n'
                '</p>\n'
                '<h4>✨ [Conclusion &amp; Key Takeaways]</h4>\n'
                '<p>Therefore, the number of arrangements is <b>$128$</b>, which corresponds to <b>choice ③</b>.</p>'
            ),
        },
    },

    # =========================================================================
    # 확통 24번 (csat27_p24) — 3점, 정답 2 (1/6)
    # =========================================================================
    {
        'slug': 'csat27_p24',
        'qNum': '24',
        'points': 3,
        'is_short_answer': False,
        'official_ans_str': '',
        'subject': '확률과 통계',
        'title': '[2027학년도 수능 고3 확통 24번] 확률의 덧셈정리를 이용한 곱사건의 확률 계산',
        'title_en': '[2027 CSAT Math Prob & Stat #24] Addition Rule of Probability for P(A ∩ B)',
        'summary_ko': r'확률의 덧셈정리 $\mathrm{P}(A \cup B) = \mathrm{P}(A) + \mathrm{P}(B) - \mathrm{P}(A \cap B)$에 대입하여 $\mathrm{P}(A \cap B) = \dfrac{1}{2} + \dfrac{5}{12} - \dfrac{3}{4} = \dfrac{1}{6}$ 구하기',
        'summary_en': r'Apply the addition rule $\mathrm{P}(A \cap B) = \mathrm{P}(A) + \mathrm{P}(B) - \mathrm{P}(A \cup B) = \dfrac{1}{2} + \dfrac{5}{12} - \dfrac{3}{4} = \dfrac{1}{6}$.',
        'tags': ['확률과 통계', '2027학년도 수능', '확률', '확률의덧셈정리', '합사건과곱사건', '24번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': r'$\mathrm{P}(A \cup B)$',
                'desc': r'사건 $A$ 또는 사건 $B$가 일어날 합사건의 확률',
                'desc_en': r'Probability of the union event ($A$ or $B$ occurs).',
            },
            {
                'sym': r'$\mathrm{P}(A \cap B)$',
                'desc': r'사건 $A$와 사건 $B$가 동시에 일어날 곱사건(겹치는 부분)의 확률',
                'desc_en': r'Probability of the intersection event (both $A$ and $B$ occur).',
            },
            {
                'sym': r'$\mathrm{P}(A) + \mathrm{P}(B) - \mathrm{P}(A \cup B)$',
                'desc': r'두 원을 더할 때 두 번 더해진 겹치는 부분 $\mathrm{P}(A \cap B)$를 구하는 식',
                'desc_en': r'Rearranged inclusion-exclusion formula isolating the overlap $\mathrm{P}(A \cap B)$.',
            },
        ],
        'levels': [
            {
                'title': r'🔰 1단계 · [초등 기초 직관] 분모 $2, 4, 12$의 공통분모로 통분하기',
                'title_en': r'🔰 Step 1 · [Elementary Intuition] Converting fractions to common denominator $12$',
                'knowledge': r'초등학교 분수 덧셈·뺄셈처럼 분모가 $4, 2, 12$인 세 분수 $\dfrac{3}{4}, \dfrac{1}{2}, \dfrac{5}{12}$를 모두 분모가 $12$인 분수로 통분하면 계산이 한눈에 보입니다.',
                'knowledge_en': r'Using elementary fraction arithmetic, rewrite $\dfrac{3}{4}, \dfrac{1}{2}, \dfrac{5}{12}$ with common denominator $12$.',
                'questions': [
                    {
                        'level_label': '초등 분수 통분 디딤돌 1',
                        'level_label_en': 'Elementary Fraction Step 1',
                        'stem': r'초등학교 분수 통분 규칙으로 $\dfrac{1}{2}$과 $\dfrac{3}{4}$을 분모가 $12$인 분수로 바르게 고친 것은?',
                        'stem_en': r'Using elementary fractions, how are $\dfrac{1}{2}$ and $\dfrac{3}{4}$ written with denominator $12$?',
                        'options': [
                            r'$\dfrac{4}{12},\; \dfrac{8}{12}$',
                            r'$\dfrac{6}{12},\; \dfrac{8}{12}$',
                            r'$\dfrac{6}{12},\; \dfrac{9}{12}$',
                            r'$\dfrac{5}{12},\; \dfrac{9}{12}$',
                            r'$\dfrac{6}{12},\; \dfrac{10}{12}$',
                        ],
                        'answer': 3,
                        'exp': r'$\dfrac{1}{2} = \dfrac{6}{12}$이고 $\dfrac{3}{4} = \dfrac{9}{12}$입니다.',
                        'exp_en': r'$\dfrac{1}{2} = \dfrac{6}{12}$ and $\dfrac{3}{4} = \dfrac{9}{12}$.',
                    }
                ],
            },
            {
                'title': r'🌿 2단계 · [기호 번역 브릿지] 확률의 덧셈정리 이항하기',
                'title_en': r'🌿 Step 2 · [Symbol Bridge] Rearranging the addition rule for $\mathrm{P}(A \cap B)$',
                'knowledge': r'$\mathrm{P}(A \cup B) = \mathrm{P}(A) + \mathrm{P}(B) - \mathrm{P}(A \cap B)$에서 $\mathrm{P}(A \cap B)$를 좌변으로, $\mathrm{P}(A \cup B)$를 우변으로 이항합니다.',
                'knowledge_en': r'Rearranging $\mathrm{P}(A \cup B) = \mathrm{P}(A) + \mathrm{P}(B) - \mathrm{P}(A \cap B)$ isolates $\mathrm{P}(A \cap B)$.',
                'questions': [
                    {
                        'level_label': '덧셈정리 식 변형 디딤돌 2',
                        'level_label_en': 'Addition Rule Step 2',
                        'stem': r'확률의 덧셈정리에 의해 $\mathrm{P}(A \cap B)$를 바르게 나타낸 식은?',
                        'stem_en': r'Which expression equals $\mathrm{P}(A \cap B)$ by the addition rule of probability?',
                        'options': [
                            r'$\mathrm{P}(A \cup B) - \mathrm{P}(A) - \mathrm{P}(B)$',
                            r'$\mathrm{P}(A) + \mathrm{P}(B) - \mathrm{P}(A \cup B)$',
                            r'$\mathrm{P}(A) \times \mathrm{P}(B)$',
                            r'$\mathrm{P}(A \cup B) - \mathrm{P}(A)$',
                            r'$1 - \mathrm{P}(A \cup B)$',
                        ],
                        'answer': 2,
                        'exp': r'두 확률을 더한 값에서 합사건의 확률을 빼면 겹친 부분 $\mathrm{P}(A \cap B) = \mathrm{P}(A) + \mathrm{P}(B) - \mathrm{P}(A \cup B)$가 됩니다.',
                        'exp_en': r'$\mathrm{P}(A \cap B) = \mathrm{P}(A) + \mathrm{P}(B) - \mathrm{P}(A \cup B)$.',
                    }
                ],
            },
            {
                'title': r'🌱 3단계 · [분수 덧셈] $\mathrm{P}(A) + \mathrm{P}(B)$ 먼저 계산하기',
                'title_en': r'🌱 Step 3 · [Fraction Sum] Computing $\mathrm{P}(A) + \mathrm{P}(B)$',
                'knowledge': r'$\mathrm{P}(A) + \mathrm{P}(B) = \dfrac{6}{12} + \dfrac{5}{12} = \dfrac{11}{12}$입니다.',
                'knowledge_en': r'$\mathrm{P}(A) + \mathrm{P}(B) = \dfrac{6}{12} + \dfrac{5}{12} = \dfrac{11}{12}$.',
                'questions': [
                    {
                        'level_label': '두 확률의 합 디딤돌 3',
                        'level_label_en': 'Sum of Probabilities Step 3',
                        'stem': r'$\mathrm{P}(A) = \dfrac{1}{2} = \dfrac{6}{12}$이고 $\mathrm{P}(B) = \dfrac{5}{12}$일 때, $\mathrm{P}(A) + \mathrm{P}(B)$의 값은?',
                        'stem_en': r'Given $\mathrm{P}(A) = \dfrac{6}{12}$ and $\mathrm{P}(B) = \dfrac{5}{12}$, what is $\mathrm{P}(A) + \mathrm{P}(B)$?',
                        'options': [r'$\dfrac{7}{12}$', r'$\dfrac{9}{12}$', r'$\dfrac{10}{12}$', r'$\dfrac{11}{12}$', r'$1$'],
                        'answer': 4,
                        'exp': r'$\dfrac{6}{12} + \dfrac{5}{12} = \dfrac{11}{12}$입니다.',
                        'exp_en': r'$\dfrac{6}{12} + \dfrac{5}{12} = \dfrac{11}{12}$.',
                    }
                ],
            },
            {
                'title': r'🌳 4단계 · [분수 뺄셈] $\dfrac{11}{12} - \dfrac{9}{12}$ 계산하기',
                'title_en': r'🌳 Step 4 · [Fraction Subtraction] Subtracting $\mathrm{P}(A \cup B) = \dfrac{9}{12}$',
                'knowledge': r'$\mathrm{P}(A \cap B) = \dfrac{11}{12} - \dfrac{9}{12} = \dfrac{2}{12}$입니다.',
                'knowledge_en': r'$\mathrm{P}(A \cap B) = \dfrac{11}{12} - \dfrac{9}{12} = \dfrac{2}{12}$.',
                'questions': [
                    {
                        'level_label': '합사건 빼기 디딤돌 4',
                        'level_label_en': 'Subtracting Union Step 4',
                        'stem': r'$\dfrac{11}{12} - \dfrac{3}{4} = \dfrac{11}{12} - \dfrac{9}{12} = \dfrac{[\;\text{(가)}\;]}{12}$에서 분자 $[\;\text{(가)}\;]$의 값은?',
                        'stem_en': r'In $\dfrac{11}{12} - \dfrac{9}{12} = \dfrac{[\;\text{(A)}\;]}{12}$, what is the numerator $[\;\text{(A)}\;]$?',
                        'options': [r'$1$', r'$2$', r'$3$', r'$4$', r'$5$'],
                        'answer': 2,
                        'exp': r'$11 - 9 = 2$이므로 $[\;\text{(가)}\;] = 2$입니다.',
                        'exp_en': r'$11 - 9 = 2$.',
                    }
                ],
            },
            {
                'title': r'💎 5단계 · [최종 종합] 기약분수로 약분하여 정답 확정하기',
                'title_en': r'💎 Step 5 · [Final Synthesis] Reducing $\dfrac{2}{12}$ to lowest terms',
                'knowledge': r'$\dfrac{2}{12}$의 분자와 분모를 $2$로 약분하면 $\dfrac{1}{6}$이 됩니다.',
                'knowledge_en': r'Dividing numerator and denominator of $\dfrac{2}{12}$ by $2$ gives $\dfrac{1}{6}$.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': r'$\mathrm{P}(A \cup B)=\dfrac{3}{4},\; \mathrm{P}(A)=\dfrac{1}{2},\; \mathrm{P}(B)=\dfrac{5}{12}$일 때, 기약분수로 나타낸 $\mathrm{P}(A \cap B)$의 값은?',
                        'stem_en': r'When $\mathrm{P}(A \cup B)=\dfrac{3}{4},\; \mathrm{P}(A)=\dfrac{1}{2},\; \mathrm{P}(B)=\dfrac{5}{12}$, what is $\mathrm{P}(A \cap B)$ in lowest terms?',
                        'options': [r'$\dfrac{1}{12}$', r'$\dfrac{1}{6}$', r'$\dfrac{1}{4}$', r'$\dfrac{1}{3}$', r'$\dfrac{5}{12}$'],
                        'answer': 2,
                        'exp': r'$\mathrm{P}(A \cap B) = \dfrac{2}{12} = \dfrac{1}{6}$이므로 정답은 ②번입니다.',
                        'exp_en': r'$\mathrm{P}(A \cap B) = \dfrac{2}{12} = \dfrac{1}{6}$ (choice ②).',
                    }
                ],
            },
        ],
        'final': {
            'stem': r'두 사건 $A, B$에 대하여 $$\mathrm{P}(A \cup B)=\dfrac{3}{4}, \quad \mathrm{P}(A)=\dfrac{1}{2}, \quad \mathrm{P}(B)=\dfrac{5}{12}$$일 때, $\mathrm{P}(A \cap B)$의 값은? [3점]',
            'stem_en': r'For two events $A$ and $B$, given that $$\mathrm{P}(A \cup B)=\dfrac{3}{4}, \quad \mathrm{P}(A)=\dfrac{1}{2}, \quad \mathrm{P}(B)=\dfrac{5}{12}$$ what is the value of $\mathrm{P}(A \cap B)$? [3 points]',
            'options': [r'$\dfrac{1}{12}$', r'$\dfrac{1}{6}$', r'$\dfrac{1}{4}$', r'$\dfrac{1}{3}$', r'$\dfrac{5}{12}$'],
            'answer': 2,
            'exp': r'확률의 덧셈정리 $\mathrm{P}(A \cup B) = \mathrm{P}(A) + \mathrm{P}(B) - \mathrm{P}(A \cap B)$에 의해 $\mathrm{P}(A \cap B) = \dfrac{1}{2} + \dfrac{5}{12} - \dfrac{3}{4} = \dfrac{6 + 5 - 9}{12} = \dfrac{2}{12} = \dfrac{1}{6}$입니다.',
            'exp_en': r'By the addition rule of probability, $\mathrm{P}(A \cap B) = \mathrm{P}(A) + \mathrm{P}(B) - \mathrm{P}(A \cup B) = \dfrac{1}{2} + \dfrac{5}{12} - \dfrac{3}{4} = \dfrac{6 + 5 - 9}{12} = \dfrac{1}{6}$.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 두 사건의 확률과 합사건의 확률이 주어졌을 때 <b>확률의 덧셈정리(포함·배제의 원리)</b>를 적용하여 곱사건의 확률 $\\mathrm{P}(A \\cap B)$를 구하는 기본 3점 문항입니다.</p>\n'
                + _wrap_visual_svg(
                    "📐 [2027 수능 확통 24번] 벤다이어그램 포함·배제 원리",
                    "P(A ∩ B) = 1/6",
                    _SVG_P24_INNER,
                    height=260,
                    lang="ko",
                    caption="▲ 분모를 12로 통분하면 P(A)=6/12와 P(B)=5/12의 합(11/12)에서 합사건 P(A∪B)=9/12를 뺀 겹침 영역이 2/12 = 1/6임을 직관적으로 확인할 수 있습니다.",
                )
                + _wrap_schematic_flow(
                    [
                        r"분모 $12$로 통분 ($\frac{9}{12}, \frac{6}{12}, \frac{5}{12}$)",
                        r"덧셈정리 $\mathrm{P}(A \cap B) = \mathrm{P}(A)+\mathrm{P}(B)-\mathrm{P}(A \cup B)$",
                        r"$\dfrac{6+5-9}{12} = \dfrac{2}{12}$",
                        r"기약분수 약분 $\dfrac{1}{6}$",
                    ],
                    r"$\dfrac{1}{6}$ (②)",
                    lang="ko",
                )
                + '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: 확률의 덧셈정리 정리하기</b><br>\n'
                '  두 사건 $A, B$에 대하여 $\\mathrm{P}(A \\cup B) = \\mathrm{P}(A) + \\mathrm{P}(B) - \\mathrm{P}(A \\cap B)$이므로 이를 $\\mathrm{P}(A \\cap B)$에 대하여 정리하면 다음과 같습니다.\n'
                '  $$\\mathrm{P}(A \\cap B) = \\mathrm{P}(A) + \\mathrm{P}(B) - \\mathrm{P}(A \\cup B)$$\n'
                '  <b>2단계: 공통분모 $12$로 통분하여 계산하기</b><br>\n'
                '  주어진 값을 대입하고 분모 $2, 12, 4$의 최소공배수인 $12$로 통분합니다.\n'
                '  $$\\mathrm{P}(A \\cap B) = \\frac{1}{2} + \\frac{5}{12} - \\frac{3}{4} = \\frac{6}{12} + \\frac{5}{12} - \\frac{9}{12} = \\frac{2}{12} = \\frac{1}{6}$$\n'
                '</p>\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>따라서 $\\mathrm{P}(A \\cap B) = \\dfrac{1}{6}$이므로 정답은 <b>②번</b>입니다. (<a href="https://min7014.github.io/" target="_blank" rel="noopener">수학자료실(min7014.github.io)</a>의 집합·벤다이어그램 시각 자료와 함께 복습하면 포함·배제 원리가 더욱 탄탄해집니다.)</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis &amp; Core Concepts]</h4>\n'
                '<p>This problem applies the <b>Addition Rule of Probability</b> to find the intersection probability $\\mathrm{P}(A \\cap B)$ from $\\mathrm{P}(A)$, $\\mathrm{P}(B)$, and $\\mathrm{P}(A \\cup B)$.</p>\n'
                + _wrap_visual_svg(
                    "📐 [2027 CSAT Prob & Stat #24] Venn Diagram Inclusion-Exclusion",
                    "P(A ∩ B) = 1/6",
                    _SVG_P24_INNER,
                    height=260,
                    lang="en",
                    caption="▲ Expressing all probabilities over 12 shows that the overlap equals 6/12 + 5/12 - 9/12 = 2/12 = 1/6.",
                )
                + _wrap_schematic_flow(
                    [
                        r"Common denominator $12$",
                        r"$\mathrm{P}(A \cap B) = \mathrm{P}(A)+\mathrm{P}(B)-\mathrm{P}(A \cup B)$",
                        r"$\dfrac{6+5-9}{12} = \dfrac{2}{12}$",
                        r"Reduce to $\dfrac{1}{6}$",
                    ],
                    r"$\dfrac{1}{6}$ (②)",
                    lang="en",
                )
                + '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Isolate the intersection probability</b><br>\n'
                '  $$\\mathrm{P}(A \\cap B) = \\mathrm{P}(A) + \\mathrm{P}(B) - \\mathrm{P}(A \\cup B)$$\n'
                '  <b>Step 2: Substitute and simplify using denominator $12$</b><br>\n'
                '  $$\\mathrm{P}(A \\cap B) = \\frac{1}{2} + \\frac{5}{12} - \\frac{3}{4} = \\frac{6 + 5 - 9}{12} = \\frac{2}{12} = \\frac{1}{6}$$\n'
                '</p>\n'
                '<h4>✨ [Conclusion &amp; Key Takeaways]</h4>\n'
                '<p>Hence, $\\mathrm{P}(A \\cap B) = \\dfrac{1}{6}$, corresponding to <b>choice ②</b>.</p>'
            ),
        },
    },

    # =========================================================================
    # 확통 25번 (csat27_p25) — 3점, 정답 5 (120)
    # =========================================================================
    {
        'slug': 'csat27_p25',
        'qNum': '25',
        'points': 3,
        'is_short_answer': False,
        'official_ans_str': '',
        'subject': '확률과 통계',
        'title': '[2027학년도 수능 고3 확통 25번] 이항분포의 표준편차와 평균 사이의 관계',
        'title_en': '[2027 CSAT Math Prob & Stat #25] Standard Deviation and Mean of a Binomial Distribution',
        'summary_ko': r'$X \sim \mathrm{B}\left(n, \dfrac{2}{3}\right)$에서 $\mathrm{V}(X) = \dfrac{2}{9}n = 4^2 = 16$으로 $n=72$를 구하고 $\mathrm{E}(X) = 48$을 더해 $n + \mathrm{E}(X) = 120$ 도출하기',
        'summary_en': r'For $X \sim \mathrm{B}\left(n, \dfrac{2}{3}\right)$, solve $\mathrm{V}(X) = \dfrac{2}{9}n = 16 \implies n=72$, find $\mathrm{E}(X)=48$, and obtain $n+\mathrm{E}(X)=120$.',
        'tags': ['확률과 통계', '2027학년도 수능', '통계', '이항분포', '평균과표준편차', '25번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': r'$\mathrm{B}(n, p)$',
                'desc': r'성공 확률이 $p$인 독립시행을 $n$번 반복할 때 성공 횟수가 따르는 이항분포',
                'desc_en': r'Binomial distribution for $n$ independent trials with success probability $p$.',
            },
            {
                'sym': r'$\sigma(X),\; \mathrm{V}(X) = np(1-p)$',
                'desc': r'표준편차 $\sigma(X)$를 제곱하면 분산 $\mathrm{V}(X) = \{\sigma(X)\}^2 = npq$가 됨',
                'desc_en': r'Squaring standard deviation $\sigma(X)$ gives variance $\mathrm{V}(X) = np(1-p)$.',
            },
            {
                'sym': r'$\mathrm{E}(X) = np$',
                'desc': r'이항분포의 평균(기댓값)은 시행 횟수 $n$과 성공 확률 $p$의 곱',
                'desc_en': r'Mean (expected value) of $\mathrm{B}(n, p)$ equals $np$.',
            },
        ],
        'levels': [
            {
                'title': r'🔰 1단계 · [초등 기초 직관] 표준편차 $\sigma(X)=4$를 제곱해 분산 구하기',
                'title_en': r'🔰 Step 1 · [Elementary Intuition] Squaring $\sigma(X)=4$ to find variance $\mathrm{V}(X)$',
                'knowledge': r'분산 $\mathrm{V}(X)$는 표준편차 $\sigma(X)$를 똑같이 두 번 곱한 값입니다. 초등학교 구구단 $4 \times 4 = 16$으로 바로 구합니다.',
                'knowledge_en': r'By elementary multiplication, variance $\mathrm{V}(X)$ is the square of the standard deviation: $4 \times 4 = 16$.',
                'questions': [
                    {
                        'level_label': '초등 구구단 디딤돌 1',
                        'level_label_en': 'Elementary Multiplication Step 1',
                        'stem': r'초등학교 구구단 곱셈으로 표준편차가 $\sigma(X)=4$일 때 분산 $\mathrm{V}(X) = \{\sigma(X)\}^2 = 4 \times 4$의 값은?',
                        'stem_en': r'Using elementary multiplication, when $\sigma(X)=4$, what is the variance $\mathrm{V}(X) = 4 \times 4$?',
                        'options': [r'$8$', r'$12$', r'$16$', r'$20$', r'$24$'],
                        'answer': 3,
                        'exp': r'$4 \times 4 = 16$이므로 $\mathrm{V}(X) = 16$입니다.',
                        'exp_en': r'$4 \times 4 = 16$.',
                    }
                ],
            },
            {
                'title': r'🌿 2단계 · [기호 번역 브릿지] 실패 확률 $q = 1 - p$와 분산 식 $npq$ 세우기',
                'title_en': r'🌿 Step 2 · [Symbol Bridge] Expressing $\mathrm{V}(X) = np(1-p)$ in terms of $n$',
                'knowledge': r'$p = \dfrac{2}{3}$이므로 $q = 1 - \dfrac{2}{3} = \dfrac{1}{3}$이고, 이항분포의 분산은 $\mathrm{V}(X) = n \times \dfrac{2}{3} \times \dfrac{1}{3} = \dfrac{2}{9}n$입니다.',
                'knowledge_en': r'With $p = \dfrac{2}{3}$ and $q = 1 - p = \dfrac{1}{3}$, the variance is $\mathrm{V}(X) = npq = \dfrac{2}{9}n$.',
                'questions': [
                    {
                        'level_label': '이항분포 분산 공식 디딤돌 2',
                        'level_label_en': 'Binomial Variance Step 2',
                        'stem': r'이항분포 $\mathrm{B}\left(n, \dfrac{2}{3}\right)$의 분산 $\mathrm{V}(X) = n \times \dfrac{2}{3} \times \left(1 - \dfrac{2}{3}\right)$을 간단히 하면?',
                        'stem_en': r'What does $\mathrm{V}(X) = n \times \dfrac{2}{3} \times \left(1 - \dfrac{2}{3}\right)$ simplify to?',
                        'options': [r'$\dfrac{1}{9}n$', r'$\dfrac{2}{9}n$', r'$\dfrac{1}{3}n$', r'$\dfrac{4}{9}n$', r'$\dfrac{2}{3}n$'],
                        'answer': 2,
                        'exp': r'$n \times \dfrac{2}{3} \times \dfrac{1}{3} = \dfrac{2}{9}n$입니다.',
                        'exp_en': r'$n \times \dfrac{2}{3} \times \dfrac{1}{3} = \dfrac{2}{9}n$.',
                    }
                ],
            },
            {
                'title': r'🌱 3단계 · [시행 횟수 도출] $\dfrac{2}{9}n = 16$에서 $n$ 구하기',
                'title_en': r'🌱 Step 3 · [Solving for $n$] Finding $n$ from $\dfrac{2}{9}n = 16$',
                'knowledge': r'$\dfrac{2}{9}n = 16$의 양변에 $\dfrac{9}{2}$를 곱하면 $n = 16 \times \dfrac{9}{2} = 8 \times 9 = 72$입니다.',
                'knowledge_en': r'Multiplying $\dfrac{2}{9}n = 16$ by $\dfrac{9}{2}$ gives $n = 8 \times 9 = 72$.',
                'questions': [
                    {
                        'level_label': '시행 횟수 n 계산 디딤돌 3',
                        'level_label_en': 'Number of Trials Step 3',
                        'stem': r'$\dfrac{2}{9}n = 16$을 만족시키는 자연수 $n$의 값은?',
                        'stem_en': r'What natural number $n$ satisfies $\dfrac{2}{9}n = 16$?',
                        'options': [r'$54$', r'$63$', r'$72$', r'$81$', r'$90$'],
                        'answer': 3,
                        'exp': r'$n = 16 \times \dfrac{9}{2} = 8 \times 9 = 72$입니다.',
                        'exp_en': r'$n = 16 \times \dfrac{9}{2} = 72$.',
                    }
                ],
            },
            {
                'title': r'🌳 4단계 · [평균 계산] $\mathrm{E}(X) = np$ 구하기',
                'title_en': r'🌳 Step 4 · [Mean Calculation] Computing $\mathrm{E}(X) = np$',
                'knowledge': r'$n = 72$, $p = \dfrac{2}{3}$이므로 $\mathrm{E}(X) = 72 \times \dfrac{2}{3} = 24 \times 2 = 48$입니다.',
                'knowledge_en': r'With $n = 72$ and $p = \dfrac{2}{3}$, $\mathrm{E}(X) = 72 \times \dfrac{2}{3} = 48$.',
                'questions': [
                    {
                        'level_label': '이항분포 평균 디딤돌 4',
                        'level_label_en': 'Binomial Mean Step 4',
                        'stem': r'$n = 72$일 때 이항분포 $\mathrm{B}\left(72, \dfrac{2}{3}\right)$의 평균 $\mathrm{E}(X) = 72 \times \dfrac{2}{3}$의 값은?',
                        'stem_en': r'For $\mathrm{B}\left(72, \dfrac{2}{3}\right)$, what is the mean $\mathrm{E}(X) = 72 \times \dfrac{2}{3}$?',
                        'options': [r'$36$', r'$42$', r'$48$', r'$54$', r'$60$'],
                        'answer': 3,
                        'exp': r'$72 \div 3 = 24$이고 $24 \times 2 = 48$이므로 $\mathrm{E}(X) = 48$입니다.',
                        'exp_en': r'$72 \times \dfrac{2}{3} = 48$.',
                    }
                ],
            },
            {
                'title': r'💎 5단계 · [최종 종합] $n + \mathrm{E}(X)$의 값 구하기',
                'title_en': r'💎 Step 5 · [Final Synthesis] Computing $n + \mathrm{E}(X)$',
                'knowledge': r'$n = 72$와 $\mathrm{E}(X) = 48$을 더하면 $72 + 48 = 120$으로 완성됩니다.',
                'knowledge_en': r'Adding $n = 72$ and $\mathrm{E}(X) = 48$ gives $72 + 48 = 120$.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': r'$n = 72$이고 $\mathrm{E}(X) = 48$일 때, $n + \mathrm{E}(X)$의 값은?',
                        'stem_en': r'Given $n = 72$ and $\mathrm{E}(X) = 48$, what is $n + \mathrm{E}(X)$?',
                        'options': [r'$100$', r'$105$', r'$110$', r'$115$', r'$120$'],
                        'answer': 5,
                        'exp': r'$72 + 48 = 120$이므로 정답은 ⑤번입니다.',
                        'exp_en': r'$72 + 48 = 120$ (choice ⑤).',
                    }
                ],
            },
        ],
        'final': {
            'stem': r'확률변수 $X$가 이항분포 $\mathrm{B}\left(n, \dfrac{2}{3}\right)$를 따르고 $\sigma(X)=4$일 때, $n+\mathrm{E}(X)$의 값은? [3점]',
            'stem_en': r'When a random variable $X$ follows the binomial distribution $\mathrm{B}\left(n, \dfrac{2}{3}\right)$ and $\sigma(X)=4$, what is the value of $n+\mathrm{E}(X)$? [3 points]',
            'options': [r'$100$', r'$105$', r'$110$', r'$115$', r'$120$'],
            'answer': 5,
            'exp': r'$X \sim \mathrm{B}\left(n, \dfrac{2}{3}\right)$이므로 분산은 $\mathrm{V}(X) = n \times \dfrac{2}{3} \times \dfrac{1}{3} = \dfrac{2}{9}n$입니다. $\sigma(X)=4$에서 $\mathrm{V}(X)=16$이므로 $\dfrac{2}{9}n = 16 \implies n = 72$이고, $\mathrm{E}(X) = 72 \times \dfrac{2}{3} = 48$이므로 $n + \mathrm{E}(X) = 72 + 48 = 120$입니다.',
            'exp_en': r'Since $X \sim \mathrm{B}\left(n, \dfrac{2}{3}\right)$, $\mathrm{V}(X) = n \cdot \dfrac{2}{3} \cdot \dfrac{1}{3} = \dfrac{2}{9}n = 4^2 = 16$, giving $n = 72$. Then $\mathrm{E}(X) = 72 \cdot \dfrac{2}{3} = 48$, so $n + \mathrm{E}(X) = 72 + 48 = 120$.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 <b>이항분포 $\\mathrm{B}(n, p)$의 분산 $\\mathrm{V}(X)=np(1-p)$와 평균 $\\mathrm{E}(X)=np$ 공식</b>을 연결하여 미지수 $n$과 기댓값을 차례대로 구하는 3점 문항입니다.</p>\n'
                + _wrap_visual_svg(
                    "📐 [2027 수능 확통 25번] 이항분포 B(n, 2/3)의 분산·평균 연결",
                    "n + E(X) = 72 + 48 = 120",
                    _SVG_P25_INNER,
                    height=246,
                    lang="ko",
                    caption="▲ 표준편차 4를 제곱한 분산 16에서 n=72를 도출한 뒤 평균 E(X)=48을 구해 더하면 120이 됩니다.",
                )
                + _wrap_schematic_flow(
                    [
                        r"$\sigma(X)=4 \implies \mathrm{V}(X)=16$",
                        r"$\dfrac{2}{9}n = 16 \implies n = 72$",
                        r"$\mathrm{E}(X) = 72 \times \dfrac{2}{3} = 48$",
                        r"$n + \mathrm{E}(X) = 72 + 48$",
                    ],
                    r"$120$ (⑤)",
                    lang="ko",
                )
                + '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: 분산 $\\mathrm{V}(X) = np(1-p)$로 $n$ 구하기</b><br>\n'
                '  확률변수 $X$가 이항분포 $\\mathrm{B}\\left(n, \\dfrac{2}{3}\\right)$를 따르므로 $p = \\dfrac{2}{3}$, $1 - p = \\dfrac{1}{3}$입니다.<br>\n'
                '  $\\sigma(X) = 4$에서 $\\mathrm{V}(X) = \\{\\sigma(X)\\}^2 = 16$이므로\n'
                '  $$n \\times \\frac{2}{3} \\times \\frac{1}{3} = \\frac{2}{9}n = 16 \\implies n = 16 \\times \\frac{9}{2} = 72$$\n'
                '  <b>2단계: 평균 $\\mathrm{E}(X)$ 및 $n + \\mathrm{E}(X)$ 계산하기</b><br>\n'
                '  $$\\mathrm{E}(X) = np = 72 \\times \\frac{2}{3} = 48$$\n'
                '  따라서 구하는 합은 $n + \\mathrm{E}(X) = 72 + 48 = 120$입니다.\n'
                '</p>\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>따라서 정답은 <b>⑤번 ($120$)</b>입니다. (빠른 지름길: $n + \\mathrm{E}(X) = n + \\dfrac{2}{3}n = \\dfrac{5}{3}n = \\dfrac{5}{3} \\times 72 = 120$으로 한 번에 계산할 수도 있습니다. <a href="https://min7014.github.io/" target="_blank" rel="noopener">수학자료실(min7014.github.io)</a>에서 이항분포 시뮬레이션 자료도 함께 확인해 보세요.)</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis &amp; Core Concepts]</h4>\n'
                '<p>This problem uses the variance $\\mathrm{V}(X)=np(1-p)$ and mean $\\mathrm{E}(X)=np$ of a <b>binomial distribution $\\mathrm{B}\\left(n, \\dfrac{2}{3}\\right)$</b>.</p>\n'
                + _wrap_visual_svg(
                    "📐 [2027 CSAT Prob & Stat #25] Binomial B(n, 2/3) Variance & Mean",
                    "n + E(X) = 120",
                    _SVG_P25_INNER,
                    height=246,
                    lang="en",
                    caption="▲ From σ(X)=4 we obtain V(X)=16=(2/9)n ⇒ n=72 and E(X)=48, so n+E(X)=120.",
                )
                + _wrap_schematic_flow(
                    [
                        r"$\sigma(X)=4 \implies \mathrm{V}(X)=16$",
                        r"$\dfrac{2}{9}n = 16 \implies n = 72$",
                        r"$\mathrm{E}(X) = 72 \times \dfrac{2}{3} = 48$",
                        r"$72 + 48 = 120$",
                    ],
                    r"$120$ (⑤)",
                    lang="en",
                )
                + '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Find $n$ from the variance</b><br>\n'
                '  $$\\mathrm{V}(X) = n \\cdot \\frac{2}{3} \\cdot \\left(1 - \\frac{2}{3}\\right) = \\frac{2}{9}n = 4^2 = 16 \\implies n = 72$$\n'
                '  <b>Step 2: Evaluate $\\mathrm{E}(X)$ and $n + \\mathrm{E}(X)$</b><br>\n'
                '  $$\\mathrm{E}(X) = 72 \\times \\frac{2}{3} = 48 \\implies n + \\mathrm{E}(X) = 72 + 48 = 120$$\n'
                '</p>\n'
                '<h4>✨ [Conclusion &amp; Key Takeaways]</h4>\n'
                '<p>Thus, $n + \\mathrm{E}(X) = 120$, corresponding to <b>choice ⑤</b>.</p>'
            ),
        },
    },

    # =========================================================================
    # 확통 26번 (csat27_p26) — 3점, 정답 5 (25/36)
    # =========================================================================
    {
        'slug': 'csat27_p26',
        'qNum': '26',
        'points': 3,
        'is_short_answer': False,
        'official_ans_str': '',
        'subject': '확률과 통계',
        'title': '[2027학년도 수능 고3 확통 26번] 여사건을 활용한 주사위 두 눈의 곱의 범위 확률',
        'title_en': '[2027 CSAT Math Prob & Stat #26] Probability of Dice Product Range via Complement Counting',
        'summary_ko': r'전체 $36$가지 순서쌍 $(a, b)$에서 여사건인 $a \times b \le 4$ ($8$가지)와 $a \times b \ge 29$ ($3$가지)를 제외하여 $\dfrac{36 - 11}{36} = \dfrac{25}{36}$ 구하기',
        'summary_en': r'Out of $36$ ordered pairs $(a, b)$, subtract the complement cases $ab \le 4$ ($8$ pairs) and $ab \ge 29$ ($3$ pairs) to get $\dfrac{25}{36}$.',
        'tags': ['확률과 통계', '2027학년도 수능', '확률', '수학적확률', '여사건의확률', '주사위순서쌍', '26번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': r'$(a, b) \in \{1,2,3,4,5,6\}^2$',
                'desc': r'주사위를 두 번 던져 나오는 눈의 수의 순서쌍 (전체 $6 \times 6 = 36$가지)',
                'desc_en': r'Ordered pair of outcomes from rolling a die twice ($36$ equally likely outcomes).',
            },
            {
                'sym': r'$5 \le a \times b \le 28$',
                'desc': r'두 눈의 곱이 $5$ 이상이고 $28$ 이하인 목표 사건',
                'desc_en': r'Target event where the product of the two rolls lies between $5$ and $28$, inclusive.',
            },
            {
                'sym': r'$a \times b \le 4 \;\text{또는}\; a \times b \ge 29$',
                'desc': r'목표 범위 바깥에 놓이는 여사건 (개수가 적어 세기 훨씬 빠름!)',
                'desc_en': r'Complement event outside $[5, 28]$, which has far fewer cases to count.',
            },
        ],
        'levels': [
            {
                'title': r'🔰 1단계 · [초등 기초 직관] 주사위 두 번 던지기의 전체 가짓수 구하기',
                'title_en': r'🔰 Step 1 · [Elementary Intuition] Total outcomes when rolling a die twice',
                'knowledge': r'$1$부터 $6$까지의 눈이 있는 주사위를 두 번 던지면 첫 번째 $6$가지, 두 번째 $6$가지이므로 초등학교 구구단 $6 \times 6 = 36$가지 순서쌍이 나옵니다.',
                'knowledge_en': r'By elementary multiplication, rolling a $6$-sided die twice produces $6 \times 6 = 36$ equally likely ordered pairs $(a, b)$.',
                'questions': [
                    {
                        'level_label': '초등 구구단 디딤돌 1',
                        'level_label_en': 'Elementary Multiplication Step 1',
                        'stem': r'초등학교 구구단으로 한 개의 주사위를 두 번 던져 나오는 순서쌍 $(a, b)$의 전체 가짓수 $6 \times 6$은?',
                        'stem_en': r'Using elementary multiplication, how many ordered pairs $(a, b)$ are possible when rolling a die twice ($6 \times 6$)?',
                        'options': [r'$12$', r'$18$', r'$24$', r'$30$', r'$36$'],
                        'answer': 5,
                        'exp': r'$6 \times 6 = 36$가지입니다.',
                        'exp_en': r'$6 \times 6 = 36$ ordered pairs.',
                    }
                ],
            },
            {
                'title': r'🌿 2단계 · [작은 쪽 여사건] $a \times b \le 4$인 순서쌍 개수 세기',
                'title_en': r'🌿 Step 2 · [Lower Complement] Counting pairs with $a \times b \le 4$',
                'knowledge': r'$5 \le a \times b \le 28$을 직접 세는 대신 바깥쪽을 셉니다! 곱이 $4$ 이하인 자연수 순서쌍은 $a=1$일 때 $(1,1),(1,2),(1,3),(1,4)$의 $4$개, $a=2$일 때 $(2,1),(2,2)$의 $2$개, $a=3$일 때 $(3,1)$의 $1$개, $a=4$일 때 $(4,1)$의 $1$개입니다.',
                'knowledge_en': r'Pairs with $ab \le 4$: $(1,1),(1,2),(1,3),(1,4)$ ($4$), $(2,1),(2,2)$ ($2$), $(3,1)$ ($1$), and $(4,1)$ ($1$).',
                'questions': [
                    {
                        'level_label': '작은 곱 여사건 디딤돌 2',
                        'level_label_en': 'Small Product Count Step 2',
                        'stem': r'주사위 눈의 곱이 $a \times b \le 4$를 만족시키는 순서쌍 $(a, b)$의 개수는 모두 몇 개인가?',
                        'stem_en': r'How many ordered pairs $(a, b) \in \{1,\dots,6\}^2$ satisfy $a \times b \le 4$?',
                        'options': [r'$6$', r'$7$', r'$8$', r'$9$', r'$10$'],
                        'answer': 3,
                        'exp': r'$4 + 2 + 1 + 1 = 8$개입니다.',
                        'exp_en': r'$4 + 2 + 1 + 1 = 8$ pairs.',
                    }
                ],
            },
            {
                'title': r'🌱 3단계 · [큰 쪽 여사건] $a \times b > 28$인 순서쌍 개수 세기',
                'title_en': r'🌱 Step 3 · [Upper Complement] Counting pairs with $a \times b > 28$',
                'knowledge': r'주사위 두 눈의 곱 중 $28$보다 큰 값은 $30$과 $36$뿐입니다! 즉 $(5, 6), (6, 5), (6, 6)$의 $3$가지입니다 ($5 \times 5 = 25 \le 28$, $4 \times 6 = 24 \le 28$).',
                'knowledge_en': r'Products exceeding $28$ in $\{1,\dots,6\}^2$ are only $30$ and $36$, giving $(5,6), (6,5), (6,6)$ ($3$ pairs).',
                'questions': [
                    {
                        'level_label': '큰 곱 여사건 디딤돌 3',
                        'level_label_en': 'Large Product Count Step 3',
                        'stem': r'주사위 눈의 곱이 $a \times b > 28$을 만족시키는 순서쌍 $(a, b)$의 개수는?',
                        'stem_en': r'How many ordered pairs $(a, b) \in \{1,\dots,6\}^2$ satisfy $a \times b > 28$?',
                        'options': [r'$1$', r'$2$', r'$3$', r'$4$', r'$5$'],
                        'answer': 3,
                        'exp': r'$a \times b = 30$인 $(5,6), (6,5)$와 $a \times b = 36$인 $(6,6)$으로 총 $3$개입니다.',
                        'exp_en': r'Only $(5,6), (6,5), (6,6)$, so $3$ pairs.',
                    }
                ],
            },
            {
                'title': r'🌳 4단계 · [여사건 빼기] 조건을 만족하는 순서쌍의 개수 구하기',
                'title_en': r'🌳 Step 4 · [Complement Subtraction] Valid count $36 - (8 + 3)$',
                'knowledge': r'전체 $36$개에서 두 여사건(서로 겹치지 않는 배반사건)의 개수 $8 + 3 = 11$개를 빼면 $36 - 11 = 25$개가 됩니다.',
                'knowledge_en': r'Subtracting the $8 + 3 = 11$ excluded pairs from $36$ leaves $36 - 11 = 25$ valid pairs.',
                'questions': [
                    {
                        'level_label': '여사건 경우의 수 디딤돌 4',
                        'level_label_en': 'Valid Outcomes Step 4',
                        'stem': r'전체 $36$가지 중에서 $a \times b \le 4$인 $8$가지와 $a \times b > 28$인 $3$가지를 뺀, $5 \le a \times b \le 28$인 순서쌍의 개수는?',
                        'stem_en': r'Subtracting $8 + 3 = 11$ excluded pairs from $36$, how many pairs satisfy $5 \le a \times b \le 28$?',
                        'options': [r'$21$', r'$23$', r'$24$', r'$25$', r'$27$'],
                        'answer': 4,
                        'exp': r'$36 - (8 + 3) = 36 - 11 = 25$개입니다.',
                        'exp_en': r'$36 - 11 = 25$ pairs.',
                    }
                ],
            },
            {
                'title': r'💎 5단계 · [최종 종합] 구하는 확률 확정하기',
                'title_en': r'💎 Step 5 · [Final Synthesis] Final probability $\dfrac{25}{36}$',
                'knowledge': r'전체 $36$가지 근원사건이 모두 같은 정도로 기대되므로 확률은 $\dfrac{25}{36}$입니다.',
                'knowledge_en': r'Dividing $25$ favorable outcomes by $36$ equally likely outcomes gives $\dfrac{25}{36}$.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': r'한 개의 주사위를 두 번 던져 나오는 눈의 수를 차례로 $a, b$라 할 때, $5 \le a \times b \le 28$일 확률은?',
                        'stem_en': r'When rolling a die twice to get $a$ and $b$, what is the probability that $5 \le a \times b \le 28$?',
                        'options': [r'$\dfrac{1}{4}$', r'$\dfrac{13}{36}$', r'$\dfrac{17}{36}$', r'$\dfrac{7}{12}$', r'$\dfrac{25}{36}$'],
                        'answer': 5,
                        'exp': r'$\dfrac{36 - (8 + 3)}{36} = \dfrac{25}{36}$이므로 정답은 ⑤번입니다.',
                        'exp_en': r'$\dfrac{25}{36}$ (choice ⑤).',
                    }
                ],
            },
        ],
        'final': {
            'stem': r'한 개의 주사위를 두 번 던져 나오는 눈의 수를 차례로 $a, b$라 하자. $5 \le a \times b \le 28$일 확률은? [3점]',
            'stem_en': r'A fair die is rolled twice, and the numbers landing face up are denoted in order by $a$ and $b$. What is the probability that $5 \le a \times b \le 28$? [3 points]',
            'options': [r'$\dfrac{1}{4}$', r'$\dfrac{13}{36}$', r'$\dfrac{17}{36}$', r'$\dfrac{7}{12}$', r'$\dfrac{25}{36}$'],
            'answer': 5,
            'exp': r'표본공간의 전체 순서쌍 $36$가지 중에서 여사건인 $a \times b \le 4$를 만족하는 순서쌍은 $(1,1),(1,2),(1,3),(1,4),(2,1),(2,2),(3,1),(4,1)$의 $8$가지이고, $a \times b > 28$을 만족하는 순서쌍은 $(5,6),(6,5),(6,6)$의 $3$가지입니다. 따라서 구하는 확률은 $1 - \dfrac{8+3}{36} = \dfrac{25}{36}$입니다.',
            'exp_en': r'Among all $36$ ordered pairs $(a,b)$, the complement consists of $ab \le 4$ ($8$ pairs: $(1,1),(1,2),(1,3),(1,4),(2,1),(2,2),(3,1),(4,1)$) and $ab > 28$ ($3$ pairs: $(5,6),(6,5),(6,6)$). Thus the probability is $1 - \dfrac{8+3}{36} = \dfrac{25}{36}$.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 주사위 두 번 던지기($36$가지 격자점)에서 부등식 $5 \\le a \\times b \\le 28$을 만족하는 사건의 경우의 수가 많을 때, <b>여사건의 확률 $\\mathrm{P}(E) = 1 - \\mathrm{P}(E^c)$</b>을 활용하여 빠르고 실수 없이 계산하는 능력을 평가합니다.</p>\n'
                + _wrap_visual_svg(
                    "📐 [2027 수능 확통 26번] 6×6 주사위 눈의 곱 격자표와 여사건 분할",
                    "36 - (8 + 3) = 25 ➔ 25/36",
                    _SVG_P26_INNER,
                    height=258,
                    lang="ko",
                    caption="▲ 6×6 구구단 격자표에서 왼쪽 위 분홍색 8칸(ab≤4)과 오른쪽 아래 노란색 3칸(ab≥30)만 걷어내면 초록색 25칸이 한눈에 남습니다.",
                )
                + _wrap_schematic_flow(
                    [
                        r"전체 순서쌍 $6 \times 6 = 36$개",
                        r"$a \times b \le 4$: $8$개",
                        r"$a \times b \ge 29$: $3$개",
                        r"여사건 제외 $36 - 11 = 25$개",
                    ],
                    r"$\dfrac{25}{36}$ (⑤)",
                    lang="ko",
                )
                + '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: 표본공간과 여사건 설정하기</b><br>\n'
                '  한 개의 주사위를 두 번 던져 나오는 순서쌍 $(a, b)$의 전체 가짓수는 $6 \\times 6 = 36$입니다.<br>\n'
                '  사건 $E$를 $5 \\le a \\times b \\le 28$인 사건이라 하면, 여사건 $E^c$는 <b>$a \\times b \\le 4$ 또는 $a \\times b \\ge 29$</b>인 사건입니다.<br><br>\n'
                '  <b>2단계: 여사건 $E^c$의 원소의 개수 세기</b><br>\n'
                '  (i) $a \\times b \\le 4$인 순서쌍:<br>\n'
                '  &nbsp;&nbsp;• $a = 1$: $(1, 1), (1, 2), (1, 3), (1, 4)$ ($4$개)<br>\n'
                '  &nbsp;&nbsp;• $a = 2$: $(2, 1), (2, 2)$ ($2$개)<br>\n'
                '  &nbsp;&nbsp;• $a = 3$: $(3, 1)$ ($1$개), &nbsp;$a = 4$: $(4, 1)$ ($1$개) $\\implies$ 합계 $8$개<br>\n'
                '  (ii) $a \\times b \\ge 29$인 순서쌍:<br>\n'
                '  &nbsp;&nbsp;• $(5, 6), (6, 5), (6, 6)$ $\\implies$ 합계 $3$개<br><br>\n'
                '  <b>3단계: 여사건의 확률로 본사건 확률 구하기</b><br>\n'
                '  $$\\mathrm{P}(E) = 1 - \\mathrm{P}(E^c) = 1 - \\frac{8 + 3}{36} = \\frac{36 - 11}{36} = \\frac{25}{36}$$\n'
                '</p>\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>따라서 구하는 확률은 <b>$\\dfrac{25}{36}$</b>이므로 정답은 <b>⑤번</b>입니다. (<a href="https://min7014.github.io/" target="_blank" rel="noopener">수학자료실(min7014.github.io)</a>의 확률 격자·기하적 확률 탐구 자료도 함께 살펴보세요.)</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis &amp; Core Concepts]</h4>\n'
                '<p>Instead of counting all $25$ valid outcomes directly, we use the <b>Complement Rule $\\mathrm{P}(E) = 1 - \\mathrm{P}(E^c)$</b> on the $6 \\times 6$ sample space.</p>\n'
                + _wrap_visual_svg(
                    "📐 [2027 CSAT Prob & Stat #26] 6×6 Product Grid & Complement",
                    "25 / 36",
                    _SVG_P26_INNER,
                    height=258,
                    lang="en",
                    caption="▲ Excluding 8 pink cells (ab ≤ 4) and 3 amber cells (ab ≥ 30) from the 36-cell multiplication grid leaves 25 valid cells.",
                )
                + _wrap_schematic_flow(
                    [
                        r"Sample space $6 \times 6 = 36$",
                        r"$a \times b \le 4$: $8$ pairs",
                        r"$a \times b \ge 29$: $3$ pairs",
                        r"$36 - (8+3) = 25$ valid pairs",
                    ],
                    r"$\dfrac{25}{36}$ (⑤)",
                    lang="en",
                )
                + '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Count outcomes where $a \\times b \\le 4$</b><br>\n'
                '  $(1,1),(1,2),(1,3),(1,4),(2,1),(2,2),(3,1),(4,1)$ give $4 + 2 + 1 + 1 = 8$ pairs.<br><br>\n'
                '  <b>Step 2: Count outcomes where $a \\times b > 28$</b><br>\n'
                '  Only products $30$ and $36$ exceed $28$: $(5,6),(6,5),(6,6)$ give $3$ pairs.<br><br>\n'
                '  <b>Step 3: Apply the complement probability formula</b><br>\n'
                '  $$\\mathrm{P}(5 \\le a \\times b \\le 28) = 1 - \\frac{8 + 3}{36} = \\frac{25}{36}$$\n'
                '</p>\n'
                '<h4>✨ [Conclusion &amp; Key Takeaways]</h4>\n'
                '<p>Therefore, the required probability is <b>$\\dfrac{25}{36}$</b> (<b>choice ⑤</b>).</p>'
            ),
        },
    },

    # =========================================================================
    # 확통 27번 (csat27_p27) — 3점, 정답 1 (292)
    # =========================================================================
    {
        'slug': 'csat27_p27',
        'qNum': '27',
        'points': 3,
        'is_short_answer': False,
        'official_ans_str': '',
        'subject': '확률과 통계',
        'title': '[2027학년도 수능 고3 확통 27번] 모평균의 95% 신뢰구간을 이용한 표본평균과 모표준편차 구하기',
        'title_en': '[2027 CSAT Math Prob & Stat #27] Sample Mean and Population Standard Deviation from a 95% Confidence Interval',
        'summary_ko': r'신뢰구간 $[252.16,\; 267.84]$의 중점으로 $\bar{x}=260$을 구하고 반쪽 폭 $1.96 \times \dfrac{\sigma}{8} = 7.84$에서 $\sigma=32$를 구해 $\bar{x}+\sigma=292$ 도출하기',
        'summary_en': r'Find the midpoint $\bar{x}=260$ of $[252.16, 267.84]$ and solve the margin of error $1.96 \times \dfrac{\sigma}{8} = 7.84 \implies \sigma=32$ to get $\bar{x}+\sigma=292$.',
        'tags': ['확률과 통계', '2027학년도 수능', '통계적추정', '모평균의추정', '신뢰구간', '표본평균', '27번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': r'$\bar{x} - 1.96\dfrac{\sigma}{\sqrt{n}} \le m \le \bar{x} + 1.96\dfrac{\sigma}{\sqrt{n}}$',
                'desc': r'표본 크기 $n$, 표본평균 $\bar{x}$, 모표준편차 $\sigma$일 때 모평균 $m$의 신뢰도 $95\%$ 신뢰구간',
                'desc_en': r'The $95\%$ confidence interval formula for population mean $m$.',
            },
            {
                'sym': r'$\bar{x} = \dfrac{a + b}{2}$',
                'desc': r'신뢰구간 $[a, b]$의 정가운데(중점)가 바로 표본평균 $\bar{x}$',
                'desc_en': r'Sample mean $\bar{x}$ is the exact midpoint of the confidence interval $[a, b]$.',
            },
            {
                'sym': r'$1.96 \times \dfrac{\sigma}{\sqrt{64}} = b - \bar{x}$',
                'desc': r'구간의 오른쪽 끝에서 중심 $\bar{x}$까지의 거리(오차한계)',
                'desc_en': r'Margin of error (half-width of the confidence interval).',
            },
        ],
        'levels': [
            {
                'title': r'🔰 1단계 · [초등 기초 직관] 수직선 두 끝점 $252.16$과 $267.84$의 한가운데 값 구하기',
                'title_en': r'🔰 Step 1 · [Elementary Intuition] Midpoint of $252.16$ and $267.84$ on a number line',
                'knowledge': r'신뢰구간은 표본평균 $\bar{x}$를 중심으로 왼쪽과 오른쪽으로 똑같은 거리만큼 벌어진 구간입니다. 초등학교 소수 덧셈과 나눗셈으로 두 수를 더해 $2$로 나누면 중심 $\bar{x}$가 나옵니다!',
                'knowledge_en': r'A confidence interval is symmetric around $\bar{x}$. Using elementary decimal addition and division by $2$, find the midpoint.',
                'questions': [
                    {
                        'level_label': '초등 소수 평균 디딤돌 1',
                        'level_label_en': 'Elementary Midpoint Step 1',
                        'stem': r'초등학교 소수의 덧셈과 나눗셈으로 두 수 $252.16$과 $267.84$의 한가운데 값 $\dfrac{252.16 + 267.84}{2}$를 구하면?',
                        'stem_en': r'Using elementary arithmetic, what is the midpoint $\dfrac{252.16 + 267.84}{2}$?',
                        'options': [r'$256$', r'$258$', r'$260$', r'$262$', r'$264$'],
                        'answer': 3,
                        'exp': r'$252.16 + 267.84 = 520$이므로 $520 \div 2 = 260$입니다.',
                        'exp_en': r'$252.16 + 267.84 = 520$, and $520 \div 2 = 260$.',
                    }
                ],
            },
            {
                'title': r'🌿 2단계 · [오차한계 구하기] 중심 $\bar{x}=260$에서 오른쪽 끝 $267.84$까지의 거리',
                'title_en': r'🌿 Step 2 · [Margin of Error] Distance from $\bar{x}=260$ to $267.84$',
                'knowledge': r'오른쪽 끝값 $\bar{x} + 1.96\dfrac{\sigma}{\sqrt{n}} = 267.84$에서 $\bar{x} = 260$을 빼면 반쪽 폭(오차한계)은 $267.84 - 260 = 7.84$입니다.',
                'knowledge_en': r'Subtracting $\bar{x} = 260$ from the upper bound $267.84$ gives the half-width $7.84$.',
                'questions': [
                    {
                        'level_label': '신뢰구간 반쪽 폭 디딤돌 2',
                        'level_label_en': 'Half-Width Step 2',
                        'stem': r'신뢰구간의 오른쪽 끝값 $267.84$에서 중심 $\bar{x} = 260$을 뺀 값 $1.96 \times \dfrac{\sigma}{\sqrt{64}}$는?',
                        'stem_en': r'What is $267.84 - 260$, the value of $1.96 \times \dfrac{\sigma}{\sqrt{64}}$?',
                        'options': [r'$5.88$', r'$6.86$', r'$7.84$', r'$8.82$', r'$9.80$'],
                        'answer': 3,
                        'exp': r'$267.84 - 260 = 7.84$입니다.',
                        'exp_en': r'$267.84 - 260 = 7.84$.',
                    }
                ],
            },
            {
                'title': r'🌱 3단계 · [나눗셈 정리] $1.96 \times \dfrac{\sigma}{8} = 7.84$에서 $\dfrac{\sigma}{8}$ 구하기',
                'title_en': r'🌱 Step 3 · [Standard Error] Solving $1.96 \times \dfrac{\sigma}{8} = 7.84$ for $\dfrac{\sigma}{8}$',
                'knowledge': r'$\sqrt{64} = 8$이고, $1.96 \times 4 = 7.84$이므로 양변을 $1.96$으로 나누면 $\dfrac{\sigma}{8} = 4$가 됩니다.',
                'knowledge_en': r'Since $\sqrt{64} = 8$ and $7.84 \div 1.96 = 4$, we obtain $\dfrac{\sigma}{8} = 4$.',
                'questions': [
                    {
                        'level_label': '표준오차 계산 디딤돌 3',
                        'level_label_en': 'Standard Error Step 3',
                        'stem': r'$1.96 \times \dfrac{\sigma}{8} = 7.84$일 때, $\dfrac{\sigma}{8} = \dfrac{7.84}{1.96}$의 값은?',
                        'stem_en': r'Given $1.96 \times \dfrac{\sigma}{8} = 7.84$, what is $\dfrac{\sigma}{8} = \dfrac{7.84}{1.96}$?',
                        'options': [r'$2$', r'$3$', r'$4$', r'$5$', r'$6$'],
                        'answer': 3,
                        'exp': r'$196 \times 4 = 784$이므로 $7.84 \div 1.96 = 4$입니다.',
                        'exp_en': r'$7.84 \div 1.96 = 4$.',
                    }
                ],
            },
            {
                'title': r'🌳 4단계 · [모표준편차 도출] $\sigma$의 값 구하기',
                'title_en': r'🌳 Step 4 · [Population SD] Finding $\sigma$ from $\dfrac{\sigma}{8} = 4$',
                'knowledge': r'$\dfrac{\sigma}{8} = 4$의 양변에 $8$을 곱하면 $\sigma = 4 \times 8 = 32$입니다.',
                'knowledge_en': r'Multiplying $\dfrac{\sigma}{8} = 4$ by $8$ yields $\sigma = 32$.',
                'questions': [
                    {
                        'level_label': '모표준편차 도출 디딤돌 4',
                        'level_label_en': 'Population SD Step 4',
                        'stem': r'$\dfrac{\sigma}{8} = 4$일 때, 모표준편차 $\sigma$의 값은?',
                        'stem_en': r'When $\dfrac{\sigma}{8} = 4$, what is $\sigma$?',
                        'options': [r'$16$', r'$24$', r'$32$', r'$40$', r'$48$'],
                        'answer': 3,
                        'exp': r'$\sigma = 4 \times 8 = 32$입니다.',
                        'exp_en': r'$\sigma = 4 \times 8 = 32$.',
                    }
                ],
            },
            {
                'title': r'💎 5단계 · [최종 종합] $\bar{x} + \sigma$의 값 확정하기',
                'title_en': r'💎 Step 5 · [Final Synthesis] Computing $\bar{x} + \sigma$',
                'knowledge': r'$\bar{x} = 260$과 $\sigma = 32$를 더하면 $260 + 32 = 292$입니다.',
                'knowledge_en': r'Adding $\bar{x} = 260$ and $\sigma = 32$ gives $292$.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': r'$\bar{x} = 260$이고 $\sigma = 32$일 때, $\bar{x} + \sigma$의 값은?',
                        'stem_en': r'Given $\bar{x} = 260$ and $\sigma = 32$, what is $\bar{x} + \sigma$?',
                        'options': [r'$292$', r'$296$', r'$300$', r'$304$', r'$308$'],
                        'answer': 1,
                        'exp': r'$260 + 32 = 292$이므로 정답은 ①번입니다.',
                        'exp_en': r'$260 + 32 = 292$ (choice ①).',
                    }
                ],
            },
        ],
        'final': {
            'stem': r'어느 농장에서 생산하는 참외 $1$개의 무게는 평균이 $m$이고 표준편차가 $\sigma$인 정규분포를 따른다고 한다. 이 농장에서 생산하는 참외 중에서 $64$개를 임의추출하여 얻은 표본평균의 값이 $\bar{x}$일 때, 이를 이용하여 구한 모평균 $m$에 대한 신뢰도 $95\%$의 신뢰구간이 $252.16 \le m \le 267.84$이다. $\bar{x}+\sigma$의 값은? (단, 무게의 단위는 $\mathrm{g}$이고, $Z$가 표준정규분포를 따르는 확률변수일 때, $\mathrm{P}(|Z| \le 1.96)=0.95$로 계산한다.) [3점]',
            'stem_en': r'The weight of a single oriental melon produced at a farm follows a normal distribution with mean $m$ and standard deviation $\sigma$. Using the sample mean $\bar{x}$ obtained from a random sample of $64$ melons from this farm, the $95\%$ confidence interval for the population mean $m$ is $252.16 \le m \le 267.84$. What is the value of $\bar{x}+\sigma$? (Weights are in $\mathrm{g}$, and $\mathrm{P}(|Z| \le 1.96)=0.95$ for a standard normal random variable $Z$.) [3 points]',
            'options': [r'$292$', r'$296$', r'$300$', r'$304$', r'$308$'],
            'answer': 1,
            'exp': r'표본의 크기 $n=64$이므로 신뢰도 $95\%$의 신뢰구간은 $\bar{x} - 1.96 \times \dfrac{\sigma}{8} \le m \le \bar{x} + 1.96 \times \dfrac{\sigma}{8}$입니다. 양 끝점의 중점에서 $\bar{x} = \dfrac{252.16 + 267.84}{2} = 260$이고, 오차한계 $1.96 \times \dfrac{\sigma}{8} = 267.84 - 260 = 7.84$에서 $\dfrac{\sigma}{8} = 4 \implies \sigma = 32$이므로 $\bar{x} + \sigma = 260 + 32 = 292$입니다.',
            'exp_en': r'With $n=64$, the $95\%$ confidence interval is $\bar{x} \pm 1.96 \cdot \dfrac{\sigma}{8}$. Its midpoint gives $\bar{x} = \dfrac{252.16 + 267.84}{2} = 260$, and its half-width gives $1.96 \cdot \dfrac{\sigma}{8} = 7.84 \implies \dfrac{\sigma}{8} = 4 \implies \sigma = 32$. Hence $\bar{x} + \sigma = 260 + 32 = 292$.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 <b>모평균 $m$의 신뢰구간 $\\left[\\bar{x} - k\\dfrac{\\sigma}{\\sqrt{n}},\\; \\bar{x} + k\\dfrac{\\sigma}{\\sqrt{n}}\\right]$이 표본평균 $\\bar{x}$에 대하여 대칭</b>이라는 기하적 성질을 이용해 $\\bar{x}$와 $\\sigma$를 구하는 통계적 추정 핵심 문항입니다.</p>\n'
                + _wrap_visual_svg(
                    "📐 [2027 수능 확통 27번] 신뢰도 95% 신뢰구간의 대칭 중심과 오차한계",
                    "x̄ = 260, σ = 32 ➔ 292",
                    _SVG_P27_INNER,
                    height=248,
                    lang="ko",
                    caption="▲ 신뢰구간 [252.16, 267.84]의 중점이 x̄ = 260이고 반쪽 길이 7.84가 1.96 × (σ/8)과 같으므로 σ = 32가 즉시 결정됩니다.",
                )
                + _wrap_schematic_flow(
                    [
                        r"표본 크기 $n=64 \implies \sqrt{n}=8$",
                        r"중점 $\bar{x} = \dfrac{252.16+267.84}{2} = 260$",
                        r"반쪽 폭 $1.96 \times \dfrac{\sigma}{8} = 7.84 \implies \sigma = 32$",
                        r"$\bar{x} + \sigma = 260 + 32$",
                    ],
                    r"$292$ (①)",
                    lang="ko",
                )
                + '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: 신뢰구간의 중점으로 표본평균 $\\bar{x}$ 구하기</b><br>\n'
                '  표본의 크기가 $n = 64$($\\sqrt{n} = 8$)이고 $\\mathrm{P}(|Z| \\le 1.96) = 0.95$이므로 모평균 $m$에 대한 신뢰도 $95\\%$의 신뢰구간은\n'
                '  $$\\bar{x} - 1.96 \\times \\frac{\\sigma}{8} \\le m \\le \\bar{x} + 1.96 \\times \\frac{\\sigma}{8}$$\n'
                '  이 구간이 $252.16 \\le m \\le 267.84$와 일치하므로 양 끝값의 산술평균이 곧 $\\bar{x}$입니다.\n'
                '  $$\\bar{x} = \\frac{252.16 + 267.84}{2} = \\frac{520}{2} = 260$$\n'
                '  <b>2단계: 오차한계(반쪽 길이)로 모표준편차 $\\sigma$ 구하기</b><br>\n'
                '  $$1.96 \\times \\frac{\\sigma}{8} = 267.84 - 260 = 7.84$$\n'
                '  $7.84 \\div 1.96 = 4$이므로 $\\dfrac{\\sigma}{8} = 4 \\implies \\sigma = 32$입니다.<br><br>\n'
                '  <b>3단계: $\\bar{x} + \\sigma$ 계산하기</b><br>\n'
                '  $$\\bar{x} + \\sigma = 260 + 32 = 292$$\n'
                '</p>\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>따라서 $\\bar{x} + \\sigma = 292$이므로 정답은 <b>①번</b>입니다. (<a href="https://min7014.github.io/" target="_blank" rel="noopener">수학자료실(min7014.github.io)</a>의 정규분포·신뢰구간 시뮬레이션 앱렛으로 표본추출과 신뢰구간의 의미를 시각적으로 확인해 보세요.)</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis &amp; Core Concepts]</h4>\n'
                '<p>This problem uses the symmetry of a <b>$95\\%$ confidence interval $\\left[\\bar{x} - 1.96\\dfrac{\\sigma}{\\sqrt{n}},\\; \\bar{x} + 1.96\\dfrac{\\sigma}{\\sqrt{n}}\\right]$</b> around the sample mean $\\bar{x}$.</p>\n'
                + _wrap_visual_svg(
                    "📐 [2027 CSAT Prob & Stat #27] 95% Confidence Interval Symmetry",
                    "x̄ + σ = 292",
                    _SVG_P27_INNER,
                    height=248,
                    lang="en",
                    caption="▲ The midpoint of [252.16, 267.84] is x̄ = 260, and the margin of error 7.84 = 1.96 × (σ/8) yields σ = 32.",
                )
                + _wrap_schematic_flow(
                    [
                        r"$n=64 \implies \sqrt{n}=8$",
                        r"Midpoint $\bar{x} = 260$",
                        r"$1.96 \times \dfrac{\sigma}{8} = 7.84 \implies \sigma = 32$",
                        r"$260 + 32 = 292$",
                    ],
                    r"$292$ (①)",
                    lang="en",
                )
                + '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Find $\\bar{x}$ from the midpoint</b><br>\n'
                '  $$\\bar{x} = \\frac{252.16 + 267.84}{2} = 260$$\n'
                '  <b>Step 2: Find $\\sigma$ from the half-width</b><br>\n'
                '  $$1.96 \\times \\frac{\\sigma}{\\sqrt{64}} = 267.84 - 260 = 7.84 \\implies \\frac{\\sigma}{8} = 4 \\implies \\sigma = 32$$\n'
                '  <b>Step 3: Sum $\\bar{x}$ and $\\sigma$</b><br>\n'
                '  $$\\bar{x} + \\sigma = 260 + 32 = 292$$\n'
                '</p>\n'
                '<h4>✨ [Conclusion &amp; Key Takeaways]</h4>\n'
                '<p>Thus, $\\bar{x} + \\sigma = 292$, which is <b>choice ①</b>.</p>'
            ),
        },
    },

    # =========================================================================
    # 확통 28번 (csat27_p28) — 4점, 정답 3 (800)
    # =========================================================================
    {
        'slug': 'csat27_p28',
        'qNum': '28',
        'points': 4,
        'is_short_answer': False,
        'official_ans_str': '',
        'subject': '확률과 통계',
        'title': '[2027학년도 수능 고3 확통 28번] 이웃 조건의 동치 번역과 빈칸 중복조합을 이용한 9장 카드 나열',
        'title_en': '[2027 CSAT Math Prob & Stat #28] Card Arrangements via Non-Adjacency Translation and Gap Stars-and-Bars',
        'summary_ko': r'인접 조건 "$x_k \times x_{k+1} \in \mathbb{N}$ 또는 $x_k = x_{k+1}$"을 "$\dfrac{1}{2}$과 $1$이 이웃하지 않는다"로 번역한 뒤, 짝수 카드 $\{2,2,2,4\}$($4$가지) 사이·양끝 $5$개 빈칸에 $\dfrac{1}{2}$과 $1$을 분리 배치하여 $400 + 400 = 800$ 구하기',
        'summary_en': r'Translate the adjacent-card rule into "no $\frac{1}{2}$ is adjacent to $1$", arrange $\{2,2,2,4\}$ in $4$ ways, and place two $\frac{1}{2}$s and three $1$s into disjoint subsets of the $5$ gaps: $400 + 400 = 800$.',
        'tags': ['확률과 통계', '2027학년도 수능', '경우의수', '같은것이있는순열', '중복조합', '이웃하지않을조건', '28번'],
        'orig_svg': ORIG_SVG_P28,
        'symbols': [
            {
                'sym': r'$x_k \times x_{k+1} \in \mathbb{N} \;\text{또는}\; x_k = x_{k+1}$',
                'desc': r'이웃한 두 카드의 곱이 자연수이거나 두 카드의 숫자가 같아야 한다는 규칙 ($\dfrac{1}{2}$과 $1$만 이웃 불가능!)',
                'desc_en': r'Adjacent cards must have a natural-number product or be equal (forbids ONLY $\frac{1}{2}$ next to $1$).',
            },
            {
                'sym': r'$\dfrac{4!}{3!} = 4$',
                'desc': r'$\dfrac{1}{2}$과 $1$ 사이를 막아 주는 짝수 장벽 카드 $2, 2, 2, 4$를 일렬로 나열하는 경우의 수',
                'desc_en': r'Ways to arrange the four even barrier cards $\{2, 2, 2, 4\}$.',
            },
            {
                'sym': r'${}_{n}\mathrm{H}_{r} = {}_{n+r-1}\mathrm{C}_{r}$',
                'desc': r'남은 $n$개의 서로 다른 빈칸에 똑같은 숫자 $1$ 카드 $r=3$장을 나누어 넣는 중복조합',
                'desc_en': r'Combinations with repetition for distributing $3$ identical $1$-cards into $n$ remaining gaps.',
            },
        ],
        'levels': [
            {
                'title': r'🔰 1단계 · [초등 기초 직관] 네 종류의 수 $\dfrac{1}{2}, 1, 2, 4$ 중 이웃하면 안 되는 짝 찾기',
                'title_en': r'🔰 Step 1 · [Elementary Intuition] Identifying which pair among $\dfrac{1}{2}, 1, 2, 4$ cannot be adjacent',
                'knowledge': r'초등학교 분수 곱셈을 해 봅시다! $\dfrac{1}{2} \times 2 = 1$(자연수), $\dfrac{1}{2} \times 4 = 2$(자연수)이고, $\dfrac{1}{2}$끼리 붙으면 두 수가 같아서($x_k = x_{k+1}$) 통과합니다! 오직 $\dfrac{1}{2} \times 1 = \dfrac{1}{2}$만 자연수도 아니고 두 수도 달라서 탈락합니다!',
                'knowledge_en': r'By elementary fraction multiplication: $\frac{1}{2}\times 2=1 \in \mathbb{N}$, $\frac{1}{2}\times 4=2 \in \mathbb{N}$, and $\left(\frac{1}{2}, \frac{1}{2}\right)$ has $x_k=x_{k+1}$. Only $\frac{1}{2}$ and $1$ give product $\frac{1}{2} \notin \mathbb{N}$ while being unequal!',
                'questions': [
                    {
                        'level_label': '초등 분수 곱셈 관찰 디딤돌 1',
                        'level_label_en': 'Elementary Fraction Product Step 1',
                        'stem': r'초등학교 분수 곱셈으로 확인할 때, 조건 "$x_k \times x_{k+1}$이 자연수이거나 $x_k = x_{k+1}$"을 어기게 되어 절대 이웃할 수 없는 두 수의 짝은?',
                        'stem_en': r'Checking elementary products, which pair of numbers violates "$x_k \times x_{k+1} \in \mathbb{N}$ or $x_k = x_{k+1}$" and can NEVER be adjacent?',
                        'options': [
                            r'$\dfrac{1}{2}$과 $\dfrac{1}{2}$',
                            r'$\dfrac{1}{2}$과 $1$',
                            r'$\dfrac{1}{2}$과 $2$',
                            r'$\dfrac{1}{2}$과 $4$',
                            r'$1$과 $2$',
                        ],
                        'answer': 2,
                        'exp': r'$\dfrac{1}{2} \times 1 = \dfrac{1}{2}$은 자연수가 아니고 $\dfrac{1}{2} \ne 1$이므로, 문제의 전체 조건은 "$\dfrac{1}{2}$과 $1$이 절대 이웃하지 않는다"와 완전히 같습니다!',
                        'exp_en': r'$\frac{1}{2} \times 1 = \frac{1}{2} \notin \mathbb{N}$ and $\frac{1}{2} \ne 1$, so the condition is equivalent to "$\frac{1}{2}$ and $1$ are never adjacent".',
                    }
                ],
            },
            {
                'title': r'🌿 2단계 · [짝수 장벽 배열] 카드 $2, 2, 2, 4$를 먼저 일렬로 나열하기',
                'title_en': r'🌿 Step 2 · [Even Barriers] Arranging the four even cards $\{2, 2, 2, 4\}$',
                'knowledge': r'$2$와 $4$는 $\dfrac{1}{2}$ 옆에도, $1$ 옆에도 자유롭게 올 수 있는 든든한 장벽입니다! $2, 2, 2, 4$ 네 장을 나열하는 가짓수는 $4$가 놓일 자리만 고르면 되므로 $\dfrac{4!}{3!} = 4$가지이며, 양끝과 사이사이에 총 $5$개의 빈칸이 생깁니다.',
                'knowledge_en': r'Cards $2, 2, 2, 4$ act as safe barriers between $\frac{1}{2}$ and $1$. They can be arranged in $\frac{4!}{3!} = 4$ ways, creating $5$ gaps (ends + between).',
                'questions': [
                    {
                        'level_label': '짝수 장벽 나열 디딤돌 2',
                        'level_label_en': 'Barrier Arrangement Step 2',
                        'stem': r'같은 숫자가 적힌 카드를 구별하지 않을 때, 네 장의 짝수 카드 $2, 2, 2, 4$를 일렬로 나열하는 경우의 수와 그때 생기는 빈칸(양끝 포함)의 개수를 순서대로 쓰면?',
                        'stem_en': r'How many ways can $\{2, 2, 2, 4\}$ be arranged in a row, and how many gaps (including both ends) do they form?',
                        'options': [
                            r'$4$가지, $4$개',
                            r'$4$가지, $5$개',
                            r'$6$가지, $5$개',
                            r'$12$가지, $4$개',
                            r'$12$가지, $5$개',
                        ],
                        'answer': 2,
                        'exp': r'$\dfrac{4!}{3!} = 4$가지이고, $\square\; E_1 \;\square\; E_2 \;\square\; E_3 \;\square\; E_4 \;\square$로 빈칸은 $5$개입니다.',
                        'exp_en': r'$\frac{4!}{3!} = 4$ ways and $5$ gaps.',
                    }
                ],
            },
            {
                'title': r'🌱 3단계 · [케이스 (i)] $\dfrac{1}{2}$ 두 장이 같은 빈칸에 들어갈 때 배치 수',
                'title_en': r'🌱 Step 3 · [Case (i)] Both $\dfrac{1}{2}$ cards enter the SAME gap',
                'knowledge': r'$\dfrac{1}{2}$과 $1$이 같은 빈칸에 들어가면 서로 이웃하게 되므로, $\dfrac{1}{2}$이 들어간 빈칸에는 $1$이 절대 들어갈 수 없습니다! $5$개 빈칸 중 $1$곳에 $\left(\dfrac{1}{2}, \dfrac{1}{2}\right)$를 넣으면(${}_{5}\mathrm{C}_{1}=5$가지), 남은 $4$개 빈칸에 $1$ 세 장을 빈칸 허용(중복 허용)으로 나누어 넣는 가짓수는 ${}_{4}\mathrm{H}_{3} = {}_{6}\mathrm{C}_{3} = 20$가지입니다.',
                'knowledge_en': r'Choose $1$ of $5$ gaps for both $\frac{1}{2}$s (${}_{5}\mathrm{C}_{1}=5$), then distribute three identical $1$s into the remaining $4$ gaps in ${}_{4}\mathrm{H}_{3} = {}_{6}\mathrm{C}_{3} = 20$ ways.',
                'questions': [
                    {
                        'level_label': '케이스 (i) 중복조합 디딤돌 3',
                        'level_label_en': 'Case (i) Gap Placement Step 3',
                        'stem': r'고정된 짝수 배열 하나에 대하여, $\dfrac{1}{2}$ 두 장을 $5$개 빈칸 중 한 곳에 함께 넣고(${}_{5}\mathrm{C}_{1}$), 남은 $4$개 빈칸에 $1$ 세 장을 나누어 넣는(${}_{4}\mathrm{H}_{3}$) 경우의 수 ${}_{5}\mathrm{C}_{1} \times {}_{4}\mathrm{H}_{3}$은?',
                        'stem_en': r'For a fixed even-card order, what is ${}_{5}\mathrm{C}_{1} \times {}_{4}\mathrm{H}_{3}$ when both $\frac{1}{2}$s share one gap and three $1$s go into the other $4$ gaps?',
                        'options': [r'$60$', r'$80$', r'$100$', r'$120$', r'$150$'],
                        'answer': 3,
                        'exp': r'${}_{5}\mathrm{C}_{1} \times {}_{4}\mathrm{H}_{3} = 5 \times {}_{6}\mathrm{C}_{3} = 5 \times 20 = 100$가지입니다 (짝수 배열 $4$가지를 곱하면 $400$가지).',
                        'exp_en': r'$5 \times \binom{6}{3} = 5 \times 20 = 100$ ways (and $4 \times 100 = 400$ with even-card orders).',
                    }
                ],
            },
            {
                'title': r'🌳 4단계 · [케이스 (ii)] $\dfrac{1}{2}$ 두 장이 서로 다른 빈칸에 들어갈 때 배치 수',
                'title_en': r'🌳 Step 4 · [Case (ii)] The two $\dfrac{1}{2}$ cards enter TWO DIFFERENT gaps',
                'knowledge': r'$5$개 빈칸 중 서로 다른 $2$곳을 골라 $\dfrac{1}{2}$을 한 장씩 넣으면(${}_{5}\mathrm{C}_{2} = 10$가지), 이제 $1$이 들어갈 수 있는 빈칸은 $3$곳 남습니다. 남은 $3$개 빈칸에 $1$ 세 장을 나누어 넣는 가짓수는 ${}_{3}\mathrm{H}_{3} = {}_{5}\mathrm{C}_{3} = 10$가지입니다.',
                'knowledge_en': r'Choose $2$ of $5$ gaps for the two $\frac{1}{2}$s (${}_{5}\mathrm{C}_{2}=10$), then distribute three $1$s into the remaining $3$ gaps in ${}_{3}\mathrm{H}_{3} = {}_{5}\mathrm{C}_{3} = 10$ ways.',
                'questions': [
                    {
                        'level_label': '케이스 (ii) 중복조합 디딤돌 4',
                        'level_label_en': 'Case (ii) Gap Placement Step 4',
                        'stem': r'고정된 짝수 배열 하나에 대하여, $\dfrac{1}{2}$ 두 장을 서로 다른 두 빈칸에 넣고(${}_{5}\mathrm{C}_{2}$), 남은 $3$개 빈칸에 $1$ 세 장을 나누어 넣는(${}_{3}\mathrm{H}_{3}$) 경우의 수 ${}_{5}\mathrm{C}_{2} \times {}_{3}\mathrm{H}_{3}$은?',
                        'stem_en': r'For a fixed even-card order, what is ${}_{5}\mathrm{C}_{2} \times {}_{3}\mathrm{H}_{3}$ when the two $\frac{1}{2}$s occupy two distinct gaps?',
                        'options': [r'$60$', r'$80$', r'$90$', r'$100$', r'$120$'],
                        'answer': 4,
                        'exp': r'${}_{5}\mathrm{C}_{2} \times {}_{3}\mathrm{H}_{3} = 10 \times {}_{5}\mathrm{C}_{3} = 10 \times 10 = 100$가지입니다 (짝수 배열 $4$가지를 곱하면 $400$가지).',
                        'exp_en': r'$10 \times \binom{5}{3} = 10 \times 10 = 100$ ways (and $4 \times 100 = 400$ with even-card orders).',
                    }
                ],
            },
            {
                'title': r'💎 5단계 · [최종 종합] 짝수 배열 $4$가지를 곱하여 전체 경우의 수 완성하기',
                'title_en': r'💎 Step 5 · [Final Synthesis] Multiplying by $4$ even-card orders',
                'knowledge': r'짝수 배열 $4$가지 각각에 대하여 케이스 (i) $100$가지와 케이스 (ii) $100$가지가 있으므로 전체 경우의 수는 $4 \times (100 + 100) = 400 + 400 = 800$입니다.',
                'knowledge_en': r'Multiplying the $4$ even-card arrangements by $(100 + 100)$ gap placements gives $4 \times 200 = 800$.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': r'짝수 카드 나열 $4$가지에 케이스 (i), (ii)의 빈칸 배치 $(100 + 100)$가지를 곱한 전체 나열의 경우의 수는?',
                        'stem_en': r'What is the total number of valid arrangements $4 \times (100 + 100)$ of all $9$ cards?',
                        'options': [r'$720$', r'$760$', r'$800$', r'$840$', r'$880$'],
                        'answer': 3,
                        'exp': r'$4 \times (5 \times 20 + 10 \times 10) = 400 + 400 = 800$이므로 정답은 ③번입니다.',
                        'exp_en': r'$4 \times (100 + 100) = 800$ (choice ③).',
                    }
                ],
            },
        ],
        'final': {
            'stem': (
                r'숫자 $\dfrac{1}{2}, \dfrac{1}{2}, 1, 1, 1, 2, 2, 2, 4$가 하나씩 적혀 있는 $9$장의 카드를 모두 한 번씩 사용하여 일렬로 나열하려고 한다. 나열된 카드에 적힌 수를 왼쪽에서부터 차례로 $x_1, x_2, \cdots, x_9$라 할 때, $8$ 이하의 모든 자연수 $k$에 대하여 다음 조건이 성립하도록 나열하는 경우의 수는? (단, 같은 수가 적힌 카드끼리는 서로 구별하지 않는다.) [4점]'
                r'<span style="display:block;margin:12px auto;padding:10px 16px;max-width:460px;border:1.5px solid #334155;border-radius:6px;background:#f8fafc;text-align:center;font-weight:600">$x_k \times x_{k+1}$의 값이 자연수이거나 $x_k = x_{k+1}$이다.</span>'
            ),
            'stem_en': (
                r'Nine cards bearing the numbers $\dfrac{1}{2}, \dfrac{1}{2}, 1, 1, 1, 2, 2, 2, 4$ are to be arranged in a row using each card once. Letting $x_1, x_2, \cdots, x_9$ denote the numbers from left to right, how many arrangements satisfy the following condition for every natural number $k \le 8$? (Cards bearing the same number are indistinguishable.) [4 points]'
                r'<span style="display:block;margin:12px auto;padding:10px 16px;max-width:480px;border:1.5px solid #334155;border-radius:6px;background:#f8fafc;text-align:center;font-weight:600">$x_k \times x_{k+1}$ is a natural number, or $x_k = x_{k+1}$.</span>'
            ),
            'options': [r'$720$', r'$760$', r'$800$', r'$840$', r'$880$'],
            'answer': 3,
            'exp': r'이웃한 두 수 $(x_k, x_{k+1})$ 중 조건을 위반하는 경우는 오직 $\dfrac{1}{2}$과 $1$이 이웃할 때뿐입니다($\dfrac{1}{2}\times\dfrac{1}{2}$은 $x_k=x_{k+1}$로 성립, $\dfrac{1}{2}\times 2=1$, $\dfrac{1}{2}\times 4=2$는 자연수로 성립). 먼저 짝수 카드 $\{2,2,2,4\}$를 나열하는 $\dfrac{4!}{3!}=4$가지에 대하여, 양끝과 사이의 $5$개 빈칸 중 (i) $\dfrac{1}{2}$ 두 장이 같은 빈칸에 들어가면 $5 \times {}_{4}\mathrm{H}_{3} = 5 \times 20 = 100$가지, (ii) $\dfrac{1}{2}$ 두 장이 다른 빈칸에 들어가면 ${}_{5}\mathrm{C}_{2} \times {}_{3}\mathrm{H}_{3} = 10 \times 10 = 100$가지이므로 총 $4 \times (100 + 100) = 800$가지입니다.',
            'exp_en': r'The condition fails if and only if $\frac{1}{2}$ and $1$ are adjacent. Arranging the four even barrier cards $\{2,2,2,4\}$ gives $\frac{4!}{3!}=4$ ways and creates $5$ gaps. Placing the two $\frac{1}{2}$s into one gap gives $5 \times {}_{4}\mathrm{H}_{3} = 100$ ways for the three $1$s; placing them into two distinct gaps gives ${}_{5}\mathrm{C}_{2} \times {}_{3}\mathrm{H}_{3} = 100$ ways. Thus the total is $4 \times (100 + 100) = 800$.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 낯설어 보이는 대수적 인접 조건(<i>"$x_k \\times x_{k+1} \\in \\mathbb{N}$ 또는 $x_k = x_{k+1}$"</i>)을 모든 카드 쌍에 대조하여 <b>"$\\dfrac{1}{2}$과 $1$이 서로 이웃하지 않는다"</b>는 순수 조합론적 동치 조건으로 번역한 뒤, <b>짝수 장벽 배열 + 빈칸 중복조합(${}_{n}\\mathrm{H}_{r}$)</b>으로 해결하는 4점 핵심 문항입니다.</p>\n'
                + _wrap_visual_svg(
                    "📐 [2027 수능 확통 28번] 짝수 장벽 {2,2,2,4}와 5개 빈칸 중복조합 분리",
                    "400 + 400 = 800",
                    _SVG_P28_INNER,
                    height=256,
                    lang="ko",
                    caption="▲ 짝수 카드 4장(2, 2, 2, 4)을 먼저 세워 5개의 안전 빈칸을 만든 뒤, 1/2이 들어간 빈칸과 1이 들어간 빈칸이 절대 겹치지 않도록 나누어 넣으면 이웃 금지 조건이 100% 필요충분으로 만족됩니다.",
                )
                + _wrap_schematic_flow(
                    [
                        r"동치 번역: $\frac{1}{2}$과 $1$ 이웃 금지",
                        r"짝수 $\{2,2,2,4\}$ 나열 $\frac{4!}{3!}=4$가지 ($5$빈칸)",
                        r"(i) $\frac{1}{2}$ 합석: $4 \times 5 \times {}_{4}\mathrm{H}_{3} = 400$",
                        r"(ii) $\frac{1}{2}$ 분리: $4 \times {}_{5}\mathrm{C}_{2} \times {}_{3}\mathrm{H}_{3} = 400$",
                    ],
                    r"$800$ (③)",
                    lang="ko",
                )
                + '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: 박스 조건의 완벽한 동치 번역</b><br>\n'
                '  카드에 적힌 수의 종류는 $\\dfrac{1}{2}, 1, 2, 4$의 네 종류입니다.<br>\n'
                '  • $1, 2, 4$끼리는 어떤 두 수를 곱해도 항상 자연수이므로 서로 자유롭게 이웃할 수 있습니다.<br>\n'
                '  • $\\dfrac{1}{2}$과 $2$, 또는 $\\dfrac{1}{2}$과 $4$가 이웃하면 곱이 각각 $1, 2$로 자연수가 되어 성립합니다.<br>\n'
                '  • $\\dfrac{1}{2}$과 $\\dfrac{1}{2}$이 이웃하면 곱은 $\\dfrac{1}{4}$이지만 <b>$x_k = x_{k+1}$ 조건</b>에 의해 성립합니다!<br>\n'
                '  • 오직 <b>$\\dfrac{1}{2}$과 $1$이 이웃할 때</b>만 곱이 $\\dfrac{1}{2}$(자연수 아님)이고 두 수도 서로 달라 조건을 위반합니다.<br>\n'
                '  따라서 주어진 조건은 <b>"$\\dfrac{1}{2}$이 적힌 카드와 $1$이 적힌 카드가 절대 이웃하지 않는다"</b>와 필요충분조건입니다.<br><br>\n'
                '  <b>2단계: 짝수 카드 $\\{2, 2, 2, 4\\}$를 장벽으로 먼저 배열하기</b><br>\n'
                '  짝수 카드 $4$장을 일렬로 나열하는 경우의 수는 $\\dfrac{4!}{3!\\,1!} = 4$가지입니다.<br>\n'
                '  이 $4$장의 카드 양끝과 사이사이에는 총 <b>$5$개의 빈칸</b>이 생깁니다: $\\square\\; E_1 \\;\\square\\; E_2 \\;\\square\\; E_3 \\;\\square\\; E_4 \\;\\square$.<br>\n'
                '  같은 빈칸 안에는 오직 $\\dfrac{1}{2}$들만 들어가거나 $1$들만 들어가야 합니다(한 빈칸에 $\\dfrac{1}{2}$과 $1$이 함께 들어가면 그 빈칸 안에서 반드시 이웃하게 됩니다).<br><br>\n'
                '  <b>3단계: $\\dfrac{1}{2}$ 두 장의 배치 모양에 따른 케이스 분류</b><br>\n'
                '  • <b>[케이스 (i)] $\\dfrac{1}{2}$ 두 장이 같은 빈칸 $1$곳에 함께 들어가는 경우</b>:<br>\n'
                '  &nbsp;&nbsp;1) $5$개 빈칸 중 $\\left(\\dfrac{1}{2}, \\dfrac{1}{2}\\right)$가 들어갈 $1$곳 선택: ${}_{5}\\mathrm{C}_{1} = 5$가지<br>\n'
                '  &nbsp;&nbsp;2) 나머지 $4$개 빈칸에 똑같은 $1$ 카드 $3$장을(빈칸에 $0$장~여러 장 허용) 나누어 넣는 중복조합: ${}_{4}\\mathrm{H}_{3} = {}_{6}\\mathrm{C}_{3} = 20$가지<br>\n'
                '  &nbsp;&nbsp;$\\implies 4 \\times 5 \\times 20 = 400$가지<br>\n'
                '  • <b>[케이스 (ii)] $\\dfrac{1}{2}$ 두 장이 서로 다른 빈칸 $2$곳에 한 장씩 들어가는 경우</b>:<br>\n'
                '  &nbsp;&nbsp;1) $5$개 빈칸 중 $\\dfrac{1}{2}$이 들어갈 $2$곳 선택: ${}_{5}\\mathrm{C}_{2} = 10$가지<br>\n'
                '  &nbsp;&nbsp;2) 나머지 $3$개 빈칸에 똑같은 $1$ 카드 $3$장을 나누어 넣는 중복조합: ${}_{3}\\mathrm{H}_{3} = {}_{5}\\mathrm{C}_{3} = 10$가지<br>\n'
                '  &nbsp;&nbsp;$\\implies 4 \\times 10 \\times 10 = 400$가지<br><br>\n'
                '  <b>4단계: 합의 법칙으로 최종 합산</b><br>\n'
                '  두 케이스는 배반이므로 구하는 경우의 수는 $400 + 400 = 800$입니다.\n'
                '</p>\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>따라서 정답은 <b>③번 ($800$)</b>입니다. (함정 주의: "$x_k = x_{k+1}$" 조건 덕분에 $\\dfrac{1}{2}$끼리는 이웃할 수 있으므로 케이스 (i)을 절대 빠뜨리면 안 됩니다! <a href="https://min7014.github.io/" target="_blank" rel="noopener">수학자료실(min7014.github.io)</a>의 중복조합 칸막이 모델 시각 증명도 함께 탐구해 보세요.)</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis &amp; Core Concepts]</h4>\n'
                '<p>Testing all pairs from $\\left\\{\\dfrac{1}{2}, 1, 2, 4\\right\\}$ reveals that "$x_k \\times x_{k+1} \\in \\mathbb{N}$ or $x_k = x_{k+1}$" holds if and only if <b>no $\\dfrac{1}{2}$ card is adjacent to any $1$ card</b>. We solve this using <b>even-card barriers</b> and <b>combinations with repetition (${}_{n}\\mathrm{H}_{r}$)</b>.</p>\n'
                + _wrap_visual_svg(
                    "📐 [2027 CSAT Prob & Stat #28] Even Barriers {2,2,2,4} & 5 Gaps",
                    "400 + 400 = 800",
                    _SVG_P28_INNER,
                    height=256,
                    lang="en",
                    caption="▲ Arranging {2,2,2,4} in 4 ways creates 5 gaps; keeping 1/2 and 1 in disjoint sets of gaps prevents adjacency.",
                )
                + _wrap_schematic_flow(
                    [
                        r"Forbid $\frac{1}{2}$ adjacent to $1$",
                        r"Arrange $\{2,2,2,4\}$: $\frac{4!}{3!}=4$ ($5$ gaps)",
                        r"Case (i) same gap: $4 \times 5 \times {}_{4}\mathrm{H}_{3} = 400$",
                        r"Case (ii) split gaps: $4 \times {}_{5}\mathrm{C}_{2} \times {}_{3}\mathrm{H}_{3} = 400$",
                    ],
                    r"$800$ (③)",
                    lang="en",
                )
                + '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Equivalent non-adjacency condition</b><br>\n'
                '  Adjacent $\\left(\\frac{1}{2}, \\frac{1}{2}\\right)$ satisfies $x_k = x_{k+1}$, and $\\frac{1}{2} \\times 2 = 1,\\; \\frac{1}{2} \\times 4 = 2 \\in \\mathbb{N}$. Only $\\left\\{\\frac{1}{2}, 1\\right\\}$ gives product $\\frac{1}{2} \\notin \\mathbb{N}$ with $x_k \\ne x_{k+1}$.<br><br>\n'
                '  <b>Step 2: Arrange the $4$ even barrier cards</b><br>\n'
                '  $\\{2, 2, 2, 4\\}$ can be ordered in $\\dfrac{4!}{3!} = 4$ ways, forming $5$ gaps. Any gap may hold $\\frac{1}{2}$s or $1$s, never both.<br><br>\n'
                '  <b>Step 3: Casework on the two $\\frac{1}{2}$ cards</b><br>\n'
                '  • <b>Case (i) Both $\\frac{1}{2}$s in one gap</b>: ${}_{5}\\mathrm{C}_{1} = 5$ choices for that gap, and ${}_{4}\\mathrm{H}_{3} = \\binom{6}{3} = 20$ ways to place three $1$s into the other $4$ gaps $\\implies 4 \\times 5 \\times 20 = 400$.<br>\n'
                '  • <b>Case (ii) Two $\\frac{1}{2}$s in different gaps</b>: ${}_{5}\\mathrm{C}_{2} = 10$ choices for those two gaps, and ${}_{3}\\mathrm{H}_{3} = \\binom{5}{3} = 10$ ways to place three $1$s into the remaining $3$ gaps $\\implies 4 \\times 10 \\times 10 = 400$.<br>\n'
                '  Total valid arrangements $= 400 + 400 = 800$.\n'
                '</p>\n'
                '<h4>✨ [Conclusion &amp; Key Takeaways]</h4>\n'
                '<p>Therefore, the total number of valid arrangements is <b>$800$</b> (<b>choice ③</b>).</p>'
            ),
        },
    },

    # =========================================================================
    # 확통 29번 (csat27_p29) — 4점 단답형, 정답 41
    # =========================================================================
    {
        'slug': 'csat27_p29',
        'qNum': '29',
        'points': 4,
        'is_short_answer': True,
        'official_ans_str': '41',
        'subject': '확률과 통계',
        'title': '[2027학년도 수능 고3 확통 29번] 대칭 이산확률분포의 분산 조건과 이차함수를 이용한 k²의 최댓값',
        'title_en': '[2027 CSAT Math Prob & Stat #29] Maximizing k² in a Symmetric Discrete Probability Distribution with 1 ≤ V(X) ≤ σ(X)',
        'summary_ko': r'$1 \le \mathrm{V}(X) \le \sigma(X)$에서 $\mathrm{V}(X)=1$을 확정하고, 원점 대칭($\mathrm{E}(X)=0$)과 $2a^2+2a+2b=1$로 $\mathrm{V}(X)=k^2(10a^2-6a+4)=1$을 유도한 뒤 $10\left(a-\dfrac{3}{10}\right)^2+\dfrac{31}{10}$의 최솟값으로 $\max(k^2)=\dfrac{10}{31} \implies p+q=41$ 구하기',
        'summary_en': r'Deduce $\mathrm{V}(X)=1$ from $1 \le \mathrm{V}(X) \le \sigma(X)$, use symmetry $\mathrm{E}(X)=0$ and $a^2+a+b=\frac{1}{2}$ to get $k^2 = \dfrac{1}{10(a-3/10)^2 + 31/10} \le \dfrac{10}{31}$, giving $p+q=41$.',
        'tags': ['확률과 통계', '2027학년도 수능', '통계', '이산확률변수', '확률분포표', '분산과표준편차', '이차함수최대최소', '29번'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': r'$1 \le \mathrm{V}(X) \le \sigma(X)$',
                'desc': r'$s = \sigma(X) \ge 0$으로 놓으면 $1 \le s^2 \le s$가 되어 오직 $s = 1$, 즉 $\mathrm{V}(X) = 1$로 하나로 결정됨!',
                'desc_en': r'Letting $s = \sigma(X) \ge 0$ gives $1 \le s^2 \le s$, which uniquely forces $s = 1$ and $\mathrm{V}(X) = 1$.',
            },
            {
                'sym': r'$2a^2 + 2a + 2b = 1$',
                'desc': r'확률분포표의 모든 확률의 합은 $1$이라는 성질 ($8b = 4 - 8a - 8a^2$ 소거용)',
                'desc_en': r'Total probability equals $1$, allowing us to eliminate $b$ via $2b = 1 - 2a - 2a^2$.',
            },
            {
                'sym': r'$\mathrm{V}(X) = k^2(10a^2 - 6a + 4) = 1$',
                'desc': r'원점 대칭($\mathrm{E}(X)=0$)으로 구한 분산을 $a$의 이차식으로 정리한 핵심 등식',
                'desc_en': r'Variance expressed as a quadratic in $a$ using $\mathrm{E}(X) = 0$.',
            },
        ],
        'levels': [
            {
                'title': r'🔰 1단계 · [초등 기초 직관] 제곱해도 커지지 않고 $1$ 이상인 양수 찾기 ($1 \le \mathrm{V}(X) \le \sigma(X)$)',
                'title_en': r'🔰 Step 1 · [Elementary Intuition] Finding the unique number satisfying $1 \le s^2 \le s$',
                'knowledge': r'초등학교 곱셈 감각을 떠올려 봅시다! $1$보다 큰 수(예: $2$)는 두 번 곱하면 $2 \times 2 = 4$로 원래 수보다 커져서 $s^2 \le s$가 깨지고, $1$보다 작은 양수(예: $0.5$)는 두 번 곱하면 $0.25$로 $1$보다 작아져서 $1 \le s^2$이 깨집니다. 따라서 $1 \le s^2 \le s$를 동시에 만족하는 양수 $s = \sigma(X)$는 오직 $1$뿐입니다!',
                'knowledge_en': r'By elementary number sense: if $s > 1$, then $s^2 > s$; if $0 \le s < 1$, then $s^2 < 1$. Hence the only $s \ge 0$ satisfying $1 \le s^2 \le s$ is $s = 1$, so $\mathrm{V}(X) = 1$!',
                'questions': [
                    {
                        'level_label': '초등 수 크기 비교 디딤돌 1',
                        'level_label_en': 'Elementary Number Sense Step 1',
                        'stem': r'초등학교 수의 크기 비교 원리로 볼 때, $\mathrm{V}(X) = \{\sigma(X)\}^2$이면서 $1 \le \mathrm{V}(X) \le \sigma(X)$가 성립하려면 분산 $\mathrm{V}(X)$의 값은 반드시 얼마여야 하는가?',
                        'stem_en': r'Since $\mathrm{V}(X) = \{\sigma(X)\}^2$ and $1 \le \mathrm{V}(X) \le \sigma(X)$, what unique value must $\mathrm{V}(X)$ take?',
                        'options': [r'$\dfrac{1}{2}$', r'$1$', r'$\dfrac{3}{2}$', r'$2$', r'$4$'],
                        'answer': 2,
                        'exp': r'$s = \sigma(X) \ge 0$이라 하면 $1 \le s^2$에서 $s \ge 1$이고 $s^2 \le s$에서 $0 \le s \le 1$이므로 $s = 1$, 즉 $\mathrm{V}(X) = 1$입니다.',
                        'exp_en': r'$1 \le s^2 \le s$ with $s \ge 0$ forces $s = 1$, so $\mathrm{V}(X) = 1$.',
                    }
                ],
            },
            {
                'title': r'🌿 2단계 · [확률 총합과 대칭 평균] $\mathrm{E}(X)=0$과 $2b = 1 - 2a - 2a^2$ 도출하기',
                'title_en': r'🌿 Step 2 · [Total Probability & Symmetry] Deriving $\mathrm{E}(X)=0$ and $2b = 1 - 2a - 2a^2$',
                'knowledge': r'확률변수 값 $-3k, -2k, -k, k, 2k, 3k$와 확률 $a^2, b, a, a, b, a^2$가 $0$을 기준으로 좌우 완벽 대칭이므로 평균은 계산할 필요도 없이 $\mathrm{E}(X) = 0$이고, 확률의 총합에서 $2a^2 + 2a + 2b = 1$입니다.',
                'knowledge_en': r'By symmetry around $0$, $\mathrm{E}(X) = 0$, and summing all probabilities gives $2a^2 + 2a + 2b = 1 \implies 2b = 1 - 2a - 2a^2$.',
                'questions': [
                    {
                        'level_label': '확률 합과 대칭 평균 디딤돌 2',
                        'level_label_en': 'Symmetry & Total Prob Step 2',
                        'stem': r'주어진 확률분포표에서 평균 $\mathrm{E}(X)$의 값과, 확률의 총합 $2a^2 + 2a + 2b = 1$을 이용하여 $8b$를 $a$에 대한 식으로 바르게 나타낸 것은?',
                        'stem_en': r'What is $\mathrm{E}(X)$, and how is $8b$ expressed in terms of $a$ using $2a^2 + 2a + 2b = 1$?',
                        'options': [
                            r'$\mathrm{E}(X)=0,\quad 8b = 4 - 4a - 4a^2$',
                            r'$\mathrm{E}(X)=0,\quad 8b = 4 - 8a - 8a^2$',
                            r'$\mathrm{E}(X)=k,\quad 8b = 4 - 8a - 8a^2$',
                            r'$\mathrm{E}(X)=0,\quad 8b = 2 - 4a - 4a^2$',
                            r'$\mathrm{E}(X)=k,\quad 8b = 1 - 2a - 2a^2$',
                        ],
                        'answer': 2,
                        'exp': r'원점 대칭이므로 $\mathrm{E}(X)=0$이고, $2b = 1 - 2a - 2a^2$의 양변에 $4$를 곱하면 $8b = 4 - 8a - 8a^2$입니다.',
                        'exp_en': r'$\mathrm{E}(X)=0$, and multiplying $2b = 1 - 2a - 2a^2$ by $4$ gives $8b = 4 - 8a - 8a^2$.',
                    }
                ],
            },
            {
                'title': r'🌱 3단계 · [분산 식 정리] $\mathrm{V}(X) = k^2(10a^2 - 6a + 4)$ 유도하기',
                'title_en': r'🌱 Step 3 · [Variance Formula] Simplifying $\mathrm{V}(X)$ into $k^2(10a^2 - 6a + 4)$',
                'knowledge': r'$\mathrm{E}(X)=0$이므로 $\mathrm{V}(X) = \mathrm{E}(X^2) = 2\{(3k)^2 a^2 + (2k)^2 b + k^2 a\} = k^2(18a^2 + 8b + 2a)$입니다. 여기에 $8b = 4 - 8a - 8a^2$을 대입합니다.',
                'knowledge_en': r'Substitute $8b = 4 - 8a - 8a^2$ into $\mathrm{V}(X) = k^2(18a^2 + 8b + 2a)$ to eliminate $b$.',
                'questions': [
                    {
                        'level_label': '분산 이차식 유도 디딤돌 3',
                        'level_label_en': 'Variance Quadratic Step 3',
                        'stem': r'$\mathrm{V}(X) = k^2(18a^2 + 8b + 2a)$에 $8b = 4 - 8a - 8a^2$을 대입하여 정리한 식은?',
                        'stem_en': r'Substituting $8b = 4 - 8a - 8a^2$ into $k^2(18a^2 + 8b + 2a)$ yields which expression?',
                        'options': [
                            r'$k^2(10a^2 - 6a + 4)$',
                            r'$k^2(10a^2 + 6a + 4)$',
                            r'$k^2(10a^2 - 8a + 4)$',
                            r'$k^2(26a^2 - 6a + 4)$',
                            r'$k^2(8a^2 - 6a + 2)$',
                        ],
                        'answer': 1,
                        'exp': r'$18a^2 + (4 - 8a - 8a^2) + 2a = 10a^2 - 6a + 4$이므로 $\mathrm{V}(X) = k^2(10a^2 - 6a + 4)$입니다.',
                        'exp_en': r'$18a^2 + (4 - 8a - 8a^2) + 2a = 10a^2 - 6a + 4$.',
                    }
                ],
            },
            {
                'title': r'🌳 4단계 · [이차함수 최솟값] $10a^2 - 6a + 4$의 최솟값과 확률 양수 조건 확인',
                'title_en': r'🌳 Step 4 · [Quadratic Minimum] Minimum of $10a^2 - 6a + 4$ and valid probability check',
                'knowledge': r'$k^2 = \dfrac{1}{10a^2 - 6a + 4}$이 최대가 되려면 분모 $f(a) = 10a^2 - 6a + 4 = 10\left(a - \dfrac{3}{10}\right)^2 + \dfrac{31}{10}$이 최소가 되어야 합니다. 꼭짓점 $a = \dfrac{3}{10}$일 때 $b = \dfrac{1}{2} - \dfrac{3}{10} - \dfrac{9}{100} = \dfrac{11}{100} > 0$이므로 모든 확률이 $0$ 이상인 조건도 완벽히 통과합니다!',
                'knowledge_en': r'Completing the square gives $10\left(a - \frac{3}{10}\right)^2 + \frac{31}{10}$. At $a = \frac{3}{10}$, $b = \frac{11}{100} > 0$ is a valid probability, so the minimum of the denominator is $\frac{31}{10}$.',
                'questions': [
                    {
                        'level_label': '완전제곱식 최솟값 디딤돌 4',
                        'level_label_en': 'Completing the Square Step 4',
                        'stem': r'확률 조건($a \ge 0,\; b \ge 0$)을 만족하는 범위에서 이차식 $10a^2 - 6a + 4 = 10\left(a - \dfrac{3}{10}\right)^2 + [\;\text{(가)}\;]$의 최솟값 $[\;\text{(가)}\;]$는?',
                        'stem_en': r'What is the minimum value $[\;\text{(A)}\;]$ of $10a^2 - 6a + 4 = 10\left(a - \dfrac{3}{10}\right)^2 + [\;\text{(A)}\;]$ over valid probabilities?',
                        'options': [
                            r'$\dfrac{29}{10}$',
                            r'$3$',
                            r'$\dfrac{31}{10}$',
                            r'$\dfrac{16}{5}$',
                            r'$\dfrac{33}{10}$',
                        ],
                        'answer': 3,
                        'exp': r'$4 - 10 \times \dfrac{9}{100} = 4 - \dfrac{9}{10} = \dfrac{31}{10}$이며, $a=\dfrac{3}{10}$일 때 $b=\dfrac{11}{100}>0$이므로 최솟값은 $\dfrac{31}{10}$입니다.',
                        'exp_en': r'$4 - \dfrac{9}{10} = \dfrac{31}{10}$, achieved at $a = \dfrac{3}{10}$ where $b = \dfrac{11}{100} > 0$.',
                    }
                ],
            },
            {
                'title': r'💎 5단계 · [최종 종합] $k^2$의 최댓값 $\dfrac{q}{p}$와 $p+q$ 구하기',
                'title_en': r'💎 Step 5 · [Final Synthesis] Finding $\max(k^2) = \dfrac{q}{p}$ and $p + q$',
                'knowledge': r'$k^2 = \dfrac{1}{10a^2 - 6a + 4}$의 최댓값은 분모가 최소인 $\dfrac{31}{10}$일 때 $\dfrac{1}{\frac{31}{10}} = \dfrac{10}{31}$입니다. $31$과 $10$은 서로소이므로 $p = 31, q = 10 \implies p + q = 41$입니다.',
                'knowledge_en': r'Taking the reciprocal of $\dfrac{31}{10}$ gives $\max(k^2) = \dfrac{10}{31}$, so $p = 31, q = 10$, and $p + q = 41$.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': r'$k^2$의 최댓값이 $\dfrac{q}{p} = \dfrac{10}{31}$일 때, 서로소인 두 자연수 $p, q$의 합 $p + q$의 값은?',
                        'stem_en': r'When the maximum of $k^2$ is $\dfrac{q}{p} = \dfrac{10}{31}$ in lowest terms, what is $p + q$?',
                        'options': [r'$37$', r'$39$', r'$41$', r'$43$', r'$45$'],
                        'answer': 3,
                        'exp': r'$p = 31,\; q = 10$이므로 $p + q = 31 + 10 = 41$입니다.',
                        'exp_en': r'$p + q = 31 + 10 = 41$.',
                    }
                ],
            },
        ],
        'final': {
            'stem': (
                r'양수 $k$에 대하여 이산확률변수 $X$의 확률분포를 표로 나타내면 다음과 같다.'
                + P29_TABLE_KO
                + r'$1 \le \mathrm{V}(X) \le \sigma(X)$가 성립할 때, $k^2$의 최댓값은 $\dfrac{q}{p}$이다. $p+q$의 값을 구하시오. (단, $p$와 $q$는 서로소인 자연수이다.) [4점]'
            ),
            'stem_en': (
                r'For a positive number $k$, the probability distribution of a discrete random variable $X$ is given by the following table.'
                + P29_TABLE_EN
                + r'When $1 \le \mathrm{V}(X) \le \sigma(X)$ holds, the maximum value of $k^2$ is $\dfrac{q}{p}$. Find the value of $p+q$, where $p$ and $q$ are coprime natural numbers. [4 points]'
            ),
            'options': [r'$37$', r'$39$', r'$41$', r'$43$', r'$45$'],
            'answer': 3,
            'exp': r'$\sigma(X) = \sqrt{\mathrm{V}(X)} \ge 0$이므로 $1 \le \mathrm{V}(X) \le \sqrt{\mathrm{V}(X)}$에서 $\mathrm{V}(X) = 1$입니다. 확률의 합 $2a^2 + 2a + 2b = 1$($8b = 4 - 8a - 8a^2$)과 원점 대칭에 의한 $\mathrm{E}(X) = 0$으로부터 $\mathrm{V}(X) = k^2(18a^2 + 8b + 2a) = k^2(10a^2 - 6a + 4) = 1$을 얻습니다. $10a^2 - 6a + 4 = 10\left(a - \dfrac{3}{10}\right)^2 + \dfrac{31}{10}$은 $a = \dfrac{3}{10}$($b = \dfrac{11}{100} > 0$)에서 최솟값 $\dfrac{31}{10}$을 가지므로 $k^2$의 최댓값은 $\dfrac{10}{31}$이고 $p + q = 31 + 10 = 41$입니다.',
            'exp_en': r'Since $\sigma(X) = \sqrt{\mathrm{V}(X)}$, the inequality $1 \le \mathrm{V}(X) \le \sigma(X)$ forces $\mathrm{V}(X) = 1$. Using symmetry ($\mathrm{E}(X)=0$) and $2a^2+2a+2b=1$, we obtain $1 = \mathrm{V}(X) = k^2(18a^2+8b+2a) = k^2(10a^2-6a+4)$. Since $10a^2-6a+4 = 10\left(a-\frac{3}{10}\right)^2 + \frac{31}{10}$ attains its minimum $\frac{31}{10}$ at $a=\frac{3}{10}$ (with $b=\frac{11}{100}>0$), $\max(k^2) = \frac{10}{31}$ and $p+q = 41$.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 <b>부등식 $1 \\le \\mathrm{V}(X) \\le \\sigma(X)$가 등식 $\\mathrm{V}(X) = 1$로 귀결되는 대수적 통찰</b>, <b>원점 대칭 이산확률분포의 평균($\\mathrm{E}(X)=0$)</b>, 그리고 <b>확률의 합($1$)을 이용한 이차함수 최대·최소</b>를 결합한 완결성 높은 4점 단답형 문항입니다.</p>\n'
                + _wrap_visual_svg(
                    "📐 [2027 수능 확통 29번] 원점 대칭 분포 (V(X)=1) & 이차함수 최솟값",
                    "max(k²) = 10/31 ➔ p+q = 41",
                    _SVG_P29_INNER,
                    height=262,
                    lang="ko",
                    caption="▲ 1 ≤ s² ≤ s에서 V(X)=1을 먼저 확정한 뒤, 분모 10(a - 3/10)² + 31/10이 꼭짓점 a = 3/10 (b = 11/100 > 0)에서 최솟값 31/10을 가짐을 이용해 k²의 최댓값 10/31을 도출합니다.",
                )
                + _wrap_schematic_flow(
                    [
                        r"$1 \le s^2 \le s \implies \mathrm{V}(X)=1$",
                        r"대칭 $\mathrm{E}(X)=0$, $8b=4-8a-8a^2$",
                        r"$\mathrm{V}(X)=k^2(10a^2-6a+4)=1$",
                        r"분모 최솟값 $\frac{31}{10} \implies \max(k^2)=\frac{10}{31}$",
                    ],
                    r"$41$",
                    lang="ko",
                )
                + '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: 부등식 $1 \\le \\mathrm{V}(X) \\le \\sigma(X)$에서 $\\mathrm{V}(X)$ 확정하기</b><br>\n'
                '  표준편차 $s = \\sigma(X) \\ge 0$이라 놓으면 $\\mathrm{V}(X) = s^2$이므로 주어진 부등식은 $1 \\le s^2 \\le s$입니다.<br>\n'
                '  • $1 \\le s^2$이고 $s \\ge 0$이므로 $s \\ge 1$입니다.<br>\n'
                '  • 동시에 $s^2 \\le s \\iff s(s - 1) \\le 0$이므로 $0 \\le s \\le 1$입니다.<br>\n'
                '  따라서 $s = 1$, 즉 <b>$\\mathrm{V}(X) = 1$</b>이 유일하게 성립합니다.<br><br>\n'
                '  <b>2단계: 확률의 총합과 대칭성을 이용한 분산 $\\mathrm{V}(X)$ 정리</b><br>\n'
                '  모든 확률의 합은 $1$이므로\n'
                '  $$2a^2 + 2a + 2b = 1 \\implies a^2 + a + b = \\frac{1}{2} \\implies 8b = 4 - 8a - 8a^2$$\n'
                '  또한 모든 확률은 $0$ 이상이어야 하므로 $a \\ge 0$이고 $b = \\dfrac{1}{2} - a - a^2 \\ge 0$이어야 합니다.<br>\n'
                '  확률분포표가 $X = 0$에 대하여 대칭이므로 기댓값은\n'
                '  $$\\mathrm{E}(X) = (-3k)a^2 + (-2k)b + (-k)a + ka + 2kb + 3ka^2 = 0$$\n'
                '  따라서 분산 $\\mathrm{V}(X) = \\mathrm{E}(X^2) - \\{\\mathrm{E}(X)\\}^2 = \\mathrm{E}(X^2)$를 계산하면:\n'
                '  $$\\mathrm{V}(X) = 2\\left\\{(3k)^2 a^2 + (2k)^2 b + k^2 a\\right\\} = k^2(18a^2 + 8b + 2a)$$\n'
                '  여기에 $8b = 4 - 8a - 8a^2$을 대입하면:\n'
                '  $$\\mathrm{V}(X) = k^2\\left(18a^2 + 4 - 8a - 8a^2 + 2a\\right) = k^2(10a^2 - 6a + 4) = 1$$\n'
                '  <b>3단계: 완전제곱식으로 $k^2$의 최댓값과 유효성 검증하기</b><br>\n'
                '  $$k^2 = \\frac{1}{10a^2 - 6a + 4} = \\frac{1}{10\\left(a - \\dfrac{3}{10}\\right)^2 + \\dfrac{31}{10}}$$\n'
                '  $a = \\dfrac{3}{10}$일 때 $a > 0$, $a^2 = \\dfrac{9}{100} > 0$, 그리고 $b = \\dfrac{1}{2} - \\dfrac{3}{10} - \\dfrac{9}{100} = \\dfrac{11}{100} > 0$이므로 유효한 확률분포 조건을 완벽히 만족합니다!<br>\n'
                '  따라서 분모의 최솟값은 $\\dfrac{31}{10}$이고, $k^2$의 최댓값은 역수인 <b>$\\dfrac{10}{31}$</b>입니다.\n'
                '</p>\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>서로소인 두 자연수는 $p = 31,\\; q = 10$이므로 구하는 값은 $p + q = 31 + 10 = \\mathbf{41}$입니다. (필수 점검: 이차함수의 꼭짓점 $a = \\dfrac{3}{10}$에서 $b \\ge 0$이 실제로 성립하는지 반드시 확인하는 습관을 길러야 하며, <a href="https://min7014.github.io/" target="_blank" rel="noopener">수학자료실(min7014.github.io)</a>의 이차함수 최대·최소 및 통계 단원 시각 증명도 함께 참고해 보세요.)</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis &amp; Core Concepts]</h4>\n'
                '<p>This short-answer problem combines three key ideas: squeezing <b>$1 \\le \\mathrm{V}(X) \\le \\sigma(X)$ to $\\mathrm{V}(X) = 1$</b>, exploiting <b>origin symmetry ($\\mathrm{E}(X) = 0$)</b>, and minimizing a quadratic in $a$ subject to non-negative probabilities.</p>\n'
                + _wrap_visual_svg(
                    "📐 [2027 CSAT Prob & Stat #29] Symmetric Distribution & Quadratic Minimum",
                    "max(k²) = 10/31 ➔ p+q = 41",
                    _SVG_P29_INNER,
                    height=262,
                    lang="en",
                    caption="▲ From 1 ≤ s² ≤ s we get V(X)=1; minimizing 10(a - 3/10)² + 31/10 at a = 3/10 (where b = 11/100 > 0) yields max(k²) = 10/31.",
                )
                + _wrap_schematic_flow(
                    [
                        r"$1 \le s^2 \le s \implies \mathrm{V}(X)=1$",
                        r"Symmetry $\mathrm{E}(X)=0$, $8b=4-8a-8a^2$",
                        r"$k^2(10a^2-6a+4)=1$",
                        r"Min denom $\frac{31}{10} \implies \max(k^2)=\frac{10}{31}$",
                    ],
                    r"$41$",
                    lang="en",
                )
                + '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Deduce $\\mathrm{V}(X) = 1$</b><br>\n'
                '  Let $s = \\sigma(X) \\ge 0$. Then $1 \\le s^2 \\le s$ implies both $s \\ge 1$ and $0 \\le s \\le 1$, so $s = 1$ and $\\mathrm{V}(X) = 1$.<br><br>\n'
                '  <b>Step 2: Express $\\mathrm{V}(X)$ in terms of $k$ and $a$</b><br>\n'
                '  Probabilities sum to $1$: $2a^2 + 2a + 2b = 1 \\implies 8b = 4 - 8a - 8a^2$. By symmetry, $\\mathrm{E}(X) = 0$, so\n'
                '  $$1 = \\mathrm{V}(X) = \\mathrm{E}(X^2) = k^2(18a^2 + 8b + 2a) = k^2(10a^2 - 6a + 4)$$\n'
                '  <b>Step 3: Maximize $k^2$ via completing the square</b><br>\n'
                '  $$10a^2 - 6a + 4 = 10\\left(a - \\frac{3}{10}\\right)^2 + \\frac{31}{10}$$\n'
                '  At $a = \\dfrac{3}{10}$, all probabilities are valid ($b = \\dfrac{1}{2} - \\dfrac{3}{10} - \\dfrac{9}{100} = \\dfrac{11}{100} > 0$), so the minimum of the denominator is $\\dfrac{31}{10}$ and $\\max(k^2) = \\dfrac{10}{31}$.\n'
                '</p>\n'
                '<h4>✨ [Conclusion &amp; Key Takeaways]</h4>\n'
                '<p>Since $p = 31$ and $q = 10$ are coprime natural numbers, $p + q = 31 + 10 = \\mathbf{41}$.</p>'
            ),
        },
    },

    # =========================================================================
    # 확통 30번 (csat27_p30) — 4점 단답형, 정답 15
    # =========================================================================
    {
        'slug': 'csat27_p30',
        'qNum': '30',
        'points': 4,
        'is_short_answer': True,
        'official_ans_str': '15',
        'subject': '확률과 통계',
        'title': '[2027학년도 수능 고3 확통 30번] 1회 시행 점수 치환(Xᵢ ∈ {0,1,2})을 이용한 3회 반복 시행의 조건부확률',
        'title_en': '[2027 CSAT Math Prob & Stat #30] Conditional Probability in 3 Repeated Card Draws via Per-Trial Score Partition',
        'summary_ko': r'$1$회 시행의 ${}_{6}\mathrm{C}_{3}=20$가지를 사건 $A, B$ 발생 횟수 합 $X_i \in \{2, 1, 0\}$으로 분할하면 $6, 12, 2$가지(그중 $6$ 포함은 각각 $4, 6, 0$가지)가 되며, $3$회 합 $a+b=4$인 $(2,2,0)$형($216$가지)과 $(2,1,1)$형($2592$가지) 중 $3$회 모두 $6$이 나오는 조건부확률 $\dfrac{432}{2808}=\dfrac{2}{13}$에서 $p+q=15$ 도출하기',
        'summary_en': r'Partition the $\binom{6}{3}=20$ outcomes per draw by score $X_i = \mathbf{1}_A + \mathbf{1}_B \in \{2,1,0\}$ into $6, 12, 2$ outcomes (with $4, 6, 0$ containing card $6$). Over $3$ draws with $X_1+X_2+X_3=4$, obtain $\dfrac{0 + 432}{216 + 2592} = \dfrac{2}{13} \implies p+q=15$.',
        'tags': ['확률과 통계', '2027학년도 수능', '확률', '조건부확률', '독립시행의확률', '배수판정과여사건', '킬러문항', '30번'],
        'orig_svg': ORIG_SVG_P30,
        'symbols': [
            {
                'sym': r'$A:\; \text{세 수의 합이 } 3\text{의 배수},\quad B:\; \text{최댓값} \ge 5$',
                'desc': r'$1$회 시행(${}_{6}\mathrm{C}_{3}=20$가지)에서 $n(A)=8$, $n(B)=20-{}_{4}\mathrm{C}_{3}=16$',
                'desc_en': r'In one draw of $3$ cards out of $6$ ($20$ ways), $n(A)=8$ and $n(B)=20-4=16$.',
            },
            {
                'sym': r'$X_i \in \{0, 1, 2\} \quad (X_1 + X_2 + X_3 = a + b = 4)$',
                'desc': r'$i$번째 시행에서 사건 $A, B$가 일어난 횟수의 합($2$점, $1$점, $0$점)으로 바꾸어 세는 핵심 치환!',
                'desc_en': r'Number of events among $A, B$ occurring in trial $i$; summing over $3$ trials equals $a + b = 4$.',
            },
            {
                'sym': r'$\mathrm{P}(F \mid E) = \dfrac{n(E \cap F)}{n(E)}$',
                'desc': r'$a+b=4$인 전체 경우의 수 분의 그중 $3$번 모두 숫자 $6$ 카드가 포함되는 경우의 수',
                'desc_en': r'Conditional probability that card $6$ appears in all $3$ trials given $a + b = 4$.',
            },
        ],
        'levels': [
            {
                'title': r'🔰 1단계 · [초등 기초 직관] $1\sim 6$을 $3$으로 나눈 나머지로 묶어 사건 $A, B^c$ 세기',
                'title_en': r'🔰 Step 1 · [Elementary Intuition] Counting $A$ and $B^c$ using remainders mod $3$',
                'knowledge': r'초등학교 나눗셈 나머지로 $1\sim 6$을 묶으면 $\{1, 4\}$(나머지 $1$), $\{2, 5\}$(나머지 $2$), $\{3, 6\}$(나머지 $0$)입니다! 세 수의 합이 $3$의 배수($A$)가 되려면 세 묶음에서 하나씩 뽑아야 하므로 $2 \times 2 \times 2 = 8$가지이고, 가장 큰 수가 $4$ 이하($B^c$)인 경우는 $\{1,2,3,4\}$에서만 $3$장을 뽑는 ${}_{4}\mathrm{C}_{3} = 4$가지입니다.',
                'knowledge_en': r'Grouping $\{1,\dots,6\}$ by remainder mod $3$ gives $\{1,4\}, \{2,5\}, \{3,6\}$. Sum divisible by $3$ ($A$) picks one from each group: $2\times 2\times 2 = 8$ ways. Max $\le 4$ ($B^c$) picks $3$ from $\{1,2,3,4\}$: $4$ ways.',
                'questions': [
                    {
                        'level_label': '초등 나눗셈 나머지 디딤돌 1',
                        'level_label_en': 'Elementary Remainder Step 1',
                        'stem': r'초등학교 나눗셈의 나머지 원리를 이용할 때, $6$장 중 $3$장을 뽑는 ${}_{6}\mathrm{C}_{3}=20$가지 중에서 세 수의 합이 $3$의 배수인 사건 $A$의 가짓수와 가장 큰 수가 $4$ 이하인 여사건 $B^c$의 가짓수를 순서대로 구하면?',
                        'stem_en': r'Among $\binom{6}{3}=20$ triples, how many have sum divisible by $3$ ($n(A)$), and how many have maximum $\le 4$ ($n(B^c)$)?',
                        'options': [
                            r'$6$가지, $4$가지',
                            r'$8$가지, $4$가지',
                            r'$8$가지, $6$가지',
                            r'$9$가지, $4$가지',
                            r'$10$가지, $4$가지',
                        ],
                        'answer': 2,
                        'exp': r'각 나머지 묶음 $\{1,4\}, \{2,5\}, \{3,6\}$에서 $1$장씩 뽑는 $n(A) = 2 \times 2 \times 2 = 8$가지이고, $\{1,2,3,4\}$에서 $3$장을 뽑는 $n(B^c) = {}_{4}\mathrm{C}_{3} = 4$가지입니다.',
                        'exp_en': r'$n(A) = 2^3 = 8$ and $n(B^c) = \binom{4}{3} = 4$.',
                    }
                ],
            },
            {
                'title': r'🌿 2단계 · [1회 시행 점수 분할] $X_i = 2, 1, 0$점인 가짓수 $(6, 12, 2)$ 구하기',
                'title_en': r'🌿 Step 2 · [Score Partition] Counting $X_i = 2, 1, 0$ per trial ($6, 12, 2$)',
                'knowledge': r'$B^c$의 $4$가지 $\{1,2,3\}, \{1,2,4\}, \{1,3,4\}, \{2,3,4\}$ 중에서 합이 $3$의 배수인 것($A \cap B^c$)은 $\{1,2,3\}$(합 $6$)과 $\{2,3,4\}$(합 $9$)의 $2$가지, 합이 $3$의 배수가 아닌 것($A^c \cap B^c$, 즉 **$0$점**)은 $\{1,2,4\}, \{1,3,4\}$의 **$2$가지**입니다! 따라서 $A \cap B$(**$2$점**)는 $8 - 2 = \mathbf{6}$가지이고, 나머지 **$1$점**은 $20 - 6 - 2 = \mathbf{12}$가지입니다.',
                'knowledge_en': r'Among $B^c = \{\{1,2,3\},\{1,2,4\},\{1,3,4\},\{2,3,4\}\}$, two belong to $A$ ($\{1,2,3\},\{2,3,4\}$) and two belong to $A^c \cap B^c$ ($0$ points: $\{1,2,4\},\{1,3,4\}$). Thus $2$ points ($A \cap B$) has $8 - 2 = 6$ ways, and $1$ point has $20 - 6 - 2 = 12$ ways.',
                'questions': [
                    {
                        'level_label': '1회 시행 점수 분할 디딤돌 2',
                        'level_label_en': 'Per-Trial Score Split Step 2',
                        'stem': r'한 번의 시행($20$가지)에서 사건 $A, B$가 동시에 일어나는 가짓수($2$점), 둘 중 하나만 일어나는 가짓수($1$점), 둘 다 일어나지 않는 가짓수($0$점)를 순서대로 바르게 나열한 것은?',
                        'stem_en': r'In one draw ($20$ outcomes), how many outcomes give score $2$ ($A \cap B$), score $1$ (exactly one of $A, B$), and score $0$ ($A^c \cap B^c$), respectively?',
                        'options': [
                            r'$6,\; 10,\; 4$',
                            r'$6,\; 12,\; 2$',
                            r'$7,\; 11,\; 2$',
                            r'$5,\; 13,\; 2$',
                            r'$8,\; 10,\; 2$',
                        ],
                        'answer': 2,
                        'exp': r'$n(A \cap B) = 6$($2$점), $n(A^c \cap B^c) = 2$($0$점), 나머지는 $20 - 6 - 2 = 12$($1$점)입니다.',
                        'exp_en': r'$6$ ways for score $2$, $12$ ways for score $1$, and $2$ ways for score $0$.',
                    }
                ],
            },
            {
                'title': r'🌱 3단계 · [숫자 $6$ 포함 개수] $2$점, $1$점, $0$점 중 $6$이 적힌 카드가 들어 있는 가짓수',
                'title_en': r'🌱 Step 3 · [Card 6 Sub-counts] Outcomes containing card $6$ within each score',
                'knowledge': r'$6$이 적힌 카드를 뽑으면 나머지 $2$장을 고르는 전체 가짓수는 ${}_{5}\mathrm{C}_{2} = 10$가지이며, 가장 큰 수가 $6 \ge 5$이므로 무조건 사건 $B$가 일어납니다! 따라서 $0$점 중에는 $6$ 포함이 **$0$가지**이고, $2$점($A \cap B$) 중 $6$ 포함은 $\{1,4\}$에서 $1$장, $\{2,5\}$에서 $1$장을 뽑아 $6$과 짝짓는 $2 \times 2 = \mathbf{4}$가지이며, $1$점 중 $6$ 포함은 $10 - 4 = \mathbf{6}$가지입니다!',
                'knowledge_en': r'Total triples containing $6$ is $\binom{5}{2} = 10$, all of which satisfy $B$ ($\max = 6 \ge 5$). Thus $0$-point triples with $6$: $0$; $2$-point triples with $6$: $2 \times 2 = 4$ ($\{1,2,6\},\{1,5,6\},\{2,4,6\},\{4,5,6\}$); $1$-point triples with $6$: $10 - 4 = 6$.',
                'questions': [
                    {
                        'level_label': '6 포함 세부분할 디딤돌 3',
                        'level_label_en': 'Card 6 Sub-counts Step 3',
                        'stem': r'$2$점($6$가지), $1$점($12$가지), $0$점($2$가지) 각각에서 숫자 $6$이 적힌 카드가 포함되어 있는 경우의 수를 순서대로 구하면?',
                        'stem_en': r'Among the $2$-point ($6$), $1$-point ($12$), and $0$-point ($2$) outcomes, how many contain card $6$, respectively?',
                        'options': [
                            r'$4,\; 6,\; 0$',
                            r'$3,\; 7,\; 0$',
                            r'$4,\; 5,\; 1$',
                            r'$5,\; 5,\; 0$',
                            r'$4,\; 6,\; 1$',
                        ],
                        'answer': 1,
                        'exp': r'$6$을 포함하면서 합이 $3$의 배수인 경우는 $4$가지($2$점), 나머지 $6$ 포함 경우는 $10 - 4 = 6$가지($1$점), $0$점에는 최댓값이 $4$ 이하이므로 $0$가지입니다.',
                        'exp_en': r'$4$, $6$, and $0$ outcomes, respectively.',
                    }
                ],
            },
            {
                'title': r'🌳 4단계 · [분모와 분자 계산] $3$회 점수 합 $X_1+X_2+X_3=4$인 $(2,2,0)$형과 $(2,1,1)$형',
                'title_en': r'🌳 Step 4 · [3-Trial Totals] Counting $(2,2,0)$ and $(2,1,1)$ patterns for $a + b = 4$',
                'knowledge': r'$3$번의 시행 점수 합이 $4$가 되는 경우는 **$(2, 2, 0)$ 나열형($3$가지)**과 **$(2, 1, 1)$ 나열형($3$가지)** 두 가지뿐입니다!<br>• 분모($a+b=4$ 전체): $3 \times 6^2 \times 2 + 3 \times 6 \times 12^2 = 216 + 2592 = 2808 = 216 \times 13$<br>• 분자($3$번 모두 $6$ 포함): $(2,2,0)$형은 $0$점에 $6$이 없으므로 $0$가지, $(2,1,1)$형은 $3 \times 4 \times 6^2 = 432 = 216 \times 2$가지!',
                'knowledge_en': r'Sum $4$ over $3$ trials occurs via permutations of $(2,2,0)$ ($3$ orders) or $(2,1,1)$ ($3$ orders). Denominator: $3\cdot 6^2\cdot 2 + 3\cdot 6\cdot 12^2 = 216 + 2592 = 2808 = 216 \times 13$. Numerator (all $3$ draws have $6$): $0 + 3\cdot 4\cdot 6^2 = 432 = 216 \times 2$.',
                'questions': [
                    {
                        'level_label': '조건부확률 약분 디딤돌 4',
                        'level_label_en': 'Conditional Ratio Step 4',
                        'stem': r'분모 $216 + 2592 = 2808$($= 216 \times 13$)과 분자 $0 + 432 = 432$($= 216 \times 2$)로부터 구한 조건부확률 $\dfrac{432}{2808}$를 기약분수로 나타내면?',
                        'stem_en': r'Reducing the conditional probability $\dfrac{432}{216 + 2592} = \dfrac{216 \times 2}{216 \times 13}$ to lowest terms gives?',
                        'options': [
                            r'$\dfrac{1}{13}$',
                            r'$\dfrac{2}{13}$',
                            r'$\dfrac{3}{13}$',
                            r'$\dfrac{2}{11}$',
                            r'$\dfrac{3}{14}$',
                        ],
                        'answer': 2,
                        'exp': r'분자와 분모를 최대공약수 $216$으로 약분하면 $\dfrac{216 \times 2}{216 \times (1 + 12)} = \dfrac{2}{13}$입니다.',
                        'exp_en': r'Canceling the common factor $216$ immediately yields $\dfrac{2}{13}$.',
                    }
                ],
            },
            {
                'title': r'💎 5단계 · [최종 종합] 서로소인 두 자연수 $p + q$의 값 구하기',
                'title_en': r'💎 Step 5 · [Final Synthesis] Computing $p + q$',
                'knowledge': r'구하는 확률이 $\dfrac{q}{p} = \dfrac{2}{13}$이고 $13$과 $2$는 서로소인 자연수이므로 $p = 13,\; q = 2 \implies p + q = 15$입니다.',
                'knowledge_en': r'From $\dfrac{q}{p} = \dfrac{2}{13}$ in lowest terms, $p = 13$ and $q = 2$, so $p + q = 15$.',
                'questions': [
                    {
                        'level_label': '최종 종합 디딤돌 5',
                        'level_label_en': 'Final Synthesis Step 5',
                        'stem': r'조건부확률이 $\dfrac{q}{p} = \dfrac{2}{13}$일 때, 서로소인 두 자연수 $p, q$의 합 $p + q$의 값은?',
                        'stem_en': r'Given $\dfrac{q}{p} = \dfrac{2}{13}$ with coprime natural numbers $p$ and $q$, what is $p + q$?',
                        'options': [r'$11$', r'$13$', r'$15$', r'$17$', r'$19$'],
                        'answer': 3,
                        'exp': r'$p = 13,\; q = 2$이므로 $p + q = 13 + 2 = 15$입니다.',
                        'exp_en': r'$p + q = 13 + 2 = 15$.',
                    }
                ],
            },
        ],
        'final': {
            'stem': r'$1$부터 $6$까지의 자연수가 하나씩 적힌 $6$장의 카드가 들어 있는 주머니가 있다. 이 주머니에서 임의로 $3$장의 카드를 동시에 꺼내어 카드에 적힌 수를 확인하고 다시 넣는 시행을 한다. 이 시행에서 꺼낸 $3$장의 카드에 적힌 세 수의 합이 $3$의 배수인 사건을 $A$, 꺼낸 $3$장의 카드에 적힌 세 수 중 가장 큰 수가 $5$ 이상인 사건을 $B$라 하자. 이 시행을 $3$번 반복할 때, 사건 $A$가 일어난 횟수를 $a$, 사건 $B$가 일어난 횟수를 $b$라 하자. $a+b=4$일 때, $3$번의 시행 모두에서 $6$이 적힌 카드가 나올 확률은 $\dfrac{q}{p}$이다. $p+q$의 값을 구하시오. (단, $p$와 $q$는 서로소인 자연수이다.) [4점]',
            'stem_en': r'A pouch contains $6$ cards bearing the natural numbers $1$ through $6$, one on each card. In a single trial, $3$ cards are drawn simultaneously at random, their numbers are recorded, and the cards are returned to the pouch. Let $A$ be the event that the sum of the three numbers drawn is a multiple of $3$, and let $B$ be the event that the largest of the three numbers drawn is at least $5$. When this trial is repeated $3$ times, let $a$ be the number of times event $A$ occurs and $b$ be the number of times event $B$ occurs. Given that $a+b=4$, the probability that the card bearing $6$ is drawn in all $3$ trials is $\dfrac{q}{p}$. Find $p+q$, where $p$ and $q$ are coprime natural numbers. [4 points]',
            'options': [r'$11$', r'$13$', r'$15$', r'$17$', r'$19$'],
            'answer': 3,
            'exp': r'$1$회 시행의 ${}_{6}\mathrm{C}_{3}=20$가지 중 $A$와 $B$가 일어나는 횟수의 합 $X_i \in \{2, 1, 0\}$을 세면 $X_i=2$($A\cap B$)가 $6$가지(그중 $6$ 포함 $4$가지), $X_i=1$이 $12$가지(그중 $6$ 포함 $6$가지), $X_i=0$($A^c\cap B^c$)이 $2$가지($6$ 포함 $0$가지)입니다. $3$회 시행에서 $a+b = X_1+X_2+X_3 = 4$인 경우는 $(2,2,0)$형 $3\times 6^2\times 2 = 216$가지($3$회 모두 $6$ 포함 $0$가지)와 $(2,1,1)$형 $3\times 6\times 12^2 = 2592$가지($3$회 모두 $6$ 포함 $3\times 4\times 6^2 = 432$가지)이므로 조건부확률은 $\dfrac{432}{216+2592} = \dfrac{432}{2808} = \dfrac{2}{13}$이고 $p+q=15$입니다.',
            'exp_en': r'In a single draw ($\binom{6}{3}=20$ outcomes), let $X_i \in \{2,1,0\}$ be the number of events among $A, B$ that occur: $X_i=2$ has $6$ outcomes ($4$ with card $6$), $X_i=1$ has $12$ outcomes ($6$ with card $6$), and $X_i=0$ has $2$ outcomes ($0$ with card $6$). For $a+b = X_1+X_2+X_3 = 4$, pattern $(2,2,0)$ gives $3\cdot 6^2\cdot 2 = 216$ ways ($0$ with card $6$ in all $3$ draws) and pattern $(2,1,1)$ gives $3\cdot 6\cdot 12^2 = 2592$ ways ($3\cdot 4\cdot 6^2 = 432$ with card $6$ in all $3$ draws). Thus the conditional probability is $\dfrac{432}{2808} = \dfrac{2}{13}$, giving $p+q = 15$.',
            'solution': (
                '<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>\n'
                '<p>본 문항은 2027학년도 수능 확률과 통계 30번 최고난도 문항입니다. 만약 두 사건 $A, B$가 서로 종속임에도 $(a, b) = (3,1), (2,2), (1,3)$으로 쪼개어 풀려고 하면 계산이 매우 복잡해지지만, <b>"$a + b$는 곧 각 시행에서 일어난 사건의 개수 $X_i \\in \\{0, 1, 2\\}$의 $3$회 총합 $X_1 + X_2 + X_3 = 4$와 같다"</b>는 발상 전환을 쓰면 놀라울 만큼 간결하고 우아하게 해결됩니다!</p>\n'
                + _wrap_visual_svg(
                    "📐 [2027 수능 확통 30번] 1회 시행 점수 Xᵢ ∈ {2,1,0} 분할 & 조건부확률",
                    "432 / 2808 = 2 / 13 ➔ p+q = 15",
                    _SVG_P30_INNER,
                    height=262,
                    lang="ko",
                    caption="▲ 20가지 근원사건을 1회 점수 Xᵢ = 2점(6개), 1점(12개), 0점(2개)과 '6 포함 여부'(4개, 6개, 0개)로 한 번만 분류해 두면 3회 독립시행의 조건부확률이 공통인수 216 약분으로 단숨에 2/13가 됩니다.",
                )
                + _wrap_schematic_flow(
                    [
                        r"${}_{6}\mathrm{C}_{3}=20$ 중 $n(A)=8, n(B)=16$",
                        r"점수 $X_i = 2,1,0$: $(6, 12, 2)$가지 ($6$포함 $4,6,0$)",
                        r"$X_1+X_2+X_3=4$: $(2,2,0)$형 $216$ + $(2,1,1)$형 $2592$",
                        r"확률 $\dfrac{432}{2808} = \dfrac{2}{13}$",
                    ],
                    r"$15$",
                    lang="ko",
                )
                + '<h4>📐 [단계별 상세 풀이 전개]</h4>\n'
                '<p>\n'
                '  <b>1단계: $1$회 시행(${}_{6}\\mathrm{C}_{3} = 20$가지)에서 사건 $A, B$ 분석하기</b><br>\n'
                '  • <b>사건 $A$ (세 수의 합이 $3$의 배수)</b>: $\\{1, 2, 3, 4, 5, 6\\}$을 $3$으로 나눈 나머지에 따라 $\\{1, 4\\}$, $\\{2, 5\\}$, $\\{3, 6\\}$으로 나누면, 세 수의 합이 $3$의 배수가 되려면 세 집합에서 각각 $1$개씩 뽑아야 합니다(각 집합의 원소가 $2$개뿐이므로 같은 나머지 $3$개를 뽑는 것은 불가능).<br>\n'
                '  $$n(A) = 2 \\times 2 \\times 2 = 8\\text{가지}$$<br>\n'
                '  • <b>여사건 $B^c$ (가장 큰 수가 $4$ 이하)</b>: $\\{1, 2, 3, 4\\}$ 중에서만 $3$장을 뽑는 경우이므로\n'
                '  $$n(B^c) = {}_{4}\\mathrm{C}_{3} = 4\\text{가지} \\quad (\\{1,2,3\\},\\; \\{1,2,4\\},\\; \\{1,3,4\\},\\; \\{2,3,4\\})$$\n'
                '  그중 합이 $3$의 배수인 것($A \\cap B^c$)은 $\\{1,2,3\\}$(합 $6$)과 $\\{2,3,4\\}$(합 $9$)의 <b>$2$가지</b>이고, 합이 $3$의 배수가 아닌 것($A^c \\cap B^c$)은 $\\{1,2,4\\}, \\{1,3,4\\}$의 <b>$2$가지</b>입니다.<br><br>\n'
                '  <b>2단계: $i$번째 시행의 점수 $X_i \\in \\{0, 1, 2\\}$와 숫자 $6$ 포함 가짓수 분류</b><br>\n'
                '  $i$번째 시행($i=1,2,3$)에서 사건 $A$와 사건 $B$가 일어난 횟수의 합을 $X_i$라 하고, $6$이 적힌 카드가 나오는 사건을 $C$($n(C) = {}_{5}\\mathrm{C}_{2} = 10$가지)라 합시다.<br>\n'
                '  1) <b>$X_i = 2$ ($A \\cap B$)</b>: $n(A) - n(A \\cap B^c) = 8 - 2 = \\mathbf{6}\\text{가지}$<br>\n'
                '  &nbsp;&nbsp;• 그중 $6$이 포함된 경우($A \\cap B \\cap C$): $6$을 뽑으면 자동으로 $B$가 성립하고 나머지 두 수를 $\\{1,4\\}$에서 $1$개, $\\{2,5\\}$에서 $1$개 뽑으면 합이 $3$의 배수가 되므로 $2 \\times 2 = \\mathbf{4}\\text{가지}$ ($\\{1,2,6\\}, \\{1,5,6\\}, \\{2,4,6\\}, \\{4,5,6\\}$).<br>\n'
                '  2) <b>$X_i = 0$ ($A^c \\cap B^c$)</b>: $\\{1,2,4\\}, \\{1,3,4\\}$로 $\\mathbf{2}\\text{가지}$<br>\n'
                '  &nbsp;&nbsp;• 최댓값이 $4$ 이하이므로 $6$이 포함된 경우는 $\\mathbf{0}\\text{가지}$!<br>\n'
                '  3) <b>$X_i = 1$ (사건 $A, B$ 중 정확히 하나만 발생)</b>: $20 - 6 - 2 = \\mathbf{12}\\text{가지}$<br>\n'
                '  &nbsp;&nbsp;• $6$이 포함된 전체 $10$가지 중 $X_i = 2$가 $4$가지, $X_i = 0$이 $0$가지이므로, $X_i = 1$이면서 $6$이 포함된 경우는 $10 - 4 = \\mathbf{6}\\text{가지}$!<br><br>\n'
                '  <b>3단계: $3$회 반복 시행에서 $a + b = X_1 + X_2 + X_3 = 4$일 조건부확률</b><br>\n'
                '  전체 표본공간 $20^3$은 분모와 분자에서 똑같이 약분되므로 경우의 수로 바로 계산합니다.<br>\n'
                '  • <b>[유형 1] $(X_1, X_2, X_3)$가 $2, 2, 0$의 순열인 경우 ($3$가지 자리 배치)</b>:<br>\n'
                '  &nbsp;&nbsp;- 전체 가짓수: $3 \\times 6^2 \\times 2 = 216$가지<br>\n'
                '  &nbsp;&nbsp;- $3$회 모두 $6$이 나오는 가짓수: $X_i = 0$인 시행에서 $6$이 나올 수 없으므로 $3 \\times 4^2 \\times 0 = \\mathbf{0}\\text{가지}$<br>\n'
                '  • <b>[유형 2] $(X_1, X_2, X_3)$가 $2, 1, 1$의 순열인 경우 ($3$가지 자리 배치)</b>:<br>\n'
                '  &nbsp;&nbsp;- 전체 가짓수: $3 \\times 6 \\times 12^2 = 3 \\times 6 \\times 144 = 2592 = 216 \\times 12$가지<br>\n'
                '  &nbsp;&nbsp;- $3$회 모두 $6$이 나오는 가짓수: $3 \\times 4 \\times 6^2 = 12 \\times 36 = 432 = 216 \\times 2$가지<br><br>\n'
                '  <b>4단계: 공통인수 $216$으로 약분하여 기약분수 도출</b><br>\n'
                '  $$\\frac{q}{p} = \\frac{0 + 432}{216 + 2592} = \\frac{216 \\times 2}{216 \\times (1 + 12)} = \\frac{2}{13}$$\n'
                '</p>\n'
                '<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>\n'
                '<p>서로소인 두 자연수는 $p = 13,\\; q = 2$이므로 구하는 값은 $p + q = 13 + 2 = \\mathbf{15}$입니다. (핵심 통찰: 여러 사건의 발생 횟수의 합 $a+b$가 조건으로 주어질 때, 각 독립시행에서의 합 $X_i = \\mathbf{1}_A + \\mathbf{1}_B$로 치환하면 종속인 두 사건도 한 번의 시행 안에서 깨끗하게 독립화됩니다! <a href="https://min7014.github.io/" target="_blank" rel="noopener">수학자료실(min7014.github.io)</a>의 조건부확률·독립시행 심화 탐구 자료도 함께 학습해 보세요.)</p>'
            ),
            'solution_en': (
                '<h4>📋 [Problem Analysis &amp; Core Concepts]</h4>\n'
                '<p>Because $A$ and $B$ are dependent within a single draw, the cleanest strategy is to define the <b>per-trial score $X_i = \\mathbf{1}_A + \\mathbf{1}_B \\in \\{0, 1, 2\\}$</b>, turning $a + b = 4$ into $X_1 + X_2 + X_3 = 4$ across $3$ independent trials.</p>\n'
                + _wrap_visual_svg(
                    "📐 [2027 CSAT Prob & Stat #30] Per-Trial Score Partition & Conditional Probability",
                    "432 / 2808 = 2 / 13 ➔ p+q = 15",
                    _SVG_P30_INNER,
                    height=262,
                    lang="en",
                    caption="▲ Partitioning the 20 triples into X_i = 2 (6 ways, 4 with 6), X_i = 1 (12 ways, 6 with 6), and X_i = 0 (2 ways, 0 with 6) yields 432 / 2808 = 2 / 13.",
                )
                + _wrap_schematic_flow(
                    [
                        r"$\binom{6}{3}=20$: $n(A)=8, n(B)=16$",
                        r"$X_i = 2,1,0$: $(6,12,2)$ ways (with $6$: $4,6,0$)",
                        r"$X_1+X_2+X_3=4$: $(2,2,0)$ gives $216$; $(2,1,1)$ gives $2592$",
                        r"Ratio $\dfrac{432}{2808} = \dfrac{2}{13}$",
                    ],
                    r"$15$",
                    lang="en",
                )
                + '<h4>📐 [Step-by-Step Rigorous Derivation]</h4>\n'
                '<p>\n'
                '  <b>Step 1: Analyze a single draw ($\\binom{6}{3} = 20$ outcomes)</b><br>\n'
                '  • Residue classes mod $3$ are $\\{1,4\\}, \\{2,5\\}, \\{3,6\\}$, so $n(A) = 2 \\times 2 \\times 2 = 8$.<br>\n'
                '  • Complement $B^c$ (max $\\le 4$) chooses $3$ from $\\{1,2,3,4\\}$: $n(B^c) = 4$ ($\\{1,2,3\\}, \\{1,2,4\\}, \\{1,3,4\\}, \\{2,3,4\\}$), of which $\\{1,2,3\\}$ and $\\{2,3,4\\}$ lie in $A \\cap B^c$ ($2$ ways) and $\\{1,2,4\\}, \\{1,3,4\\}$ lie in $A^c \\cap B^c$ ($2$ ways).<br><br>\n'
                '  <b>Step 2: Partition by $X_i \\in \\{2, 1, 0\\}$ and presence of card $6$</b><br>\n'
                '  • $X_i = 2$ ($A \\cap B$): $8 - 2 = 6$ ways; those containing $6$ pick one from $\\{1,4\\}$ and one from $\\{2,5\\}$, giving $2 \\times 2 = 4$ ways.<br>\n'
                '  • $X_i = 0$ ($A^c \\cap B^c$): $2$ ways; $0$ ways contain $6$ (since max $\\le 4$).<br>\n'
                '  • $X_i = 1$: $20 - 6 - 2 = 12$ ways; since $\\binom{5}{2} = 10$ triples contain $6$ in total, $10 - 4 = 6$ ways have $X_i = 1$ and contain $6$.<br><br>\n'
                '  <b>Step 3: Conditional probability over $3$ independent trials</b><br>\n'
                '  $X_1 + X_2 + X_3 = 4$ splits into two patterns:<br>\n'
                '  • Permutations of $(2, 2, 0)$: $3 \\times 6^2 \\times 2 = 216$ total ways, and $3 \\times 4^2 \\times 0 = 0$ ways with $6$ in all $3$ draws.<br>\n'
                '  • Permutations of $(2, 1, 1)$: $3 \\times 6 \\times 12^2 = 2592 = 216 \\times 12$ total ways, and $3 \\times 4 \\times 6^2 = 432 = 216 \\times 2$ ways with $6$ in all $3$ draws.<br>\n'
                '  $$\\frac{q}{p} = \\frac{0 + 432}{216 + 2592} = \\frac{216 \\times 2}{216 \\times 13} = \\frac{2}{13}$$\n'
                '</p>\n'
                '<h4>✨ [Conclusion &amp; Key Takeaways]</h4>\n'
                '<p>Since $p = 13$ and $q = 2$ are coprime natural numbers, $p + q = 13 + 2 = \\mathbf{15}$.</p>'
            ),
        },
    },
]
