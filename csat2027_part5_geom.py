# -*- coding: utf-8 -*-
"""
csat2027_part5_geom.py
2027학년도 대학수학능력시험 수학 영역 선택과목 [기하] 23번 ~ 30번 (8문항)
Slugs: csat27_g23 ~ csat27_g30
"""


def _esc_svg(s: str) -> str:
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _wrap_visual_svg(
    title_left: str,
    title_right: str,
    inner_svg: str,
    height: int = 270,
    lang: str = "ko",
    caption: str = "",
) -> str:
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
        ["STEP 1 · 조건 해독", "STEP 2 · 핵심 원리", "STEP 3 · 기하·수식 전개", "STEP 4 · 결합 계산"]
        if lang == "ko"
        else ["STEP 1 · Condition", "STEP 2 · Core Principle", "STEP 3 · Derivation", "STEP 4 · Synthesis"]
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
# Official Exam Figures (orig_svg) for G27, G29, G30 (Zero <polyline>, Zero $)
# ---------------------------------------------------------------------------
ORIG_SVG_G27 = (
    '<svg viewBox="0 0 360 300" xmlns="http://www.w3.org/2000/svg" '
    'style="width:100%;max-width:340px;height:auto;display:block;margin:8px auto">'
    '<polygon points="117.5,197.0 177.2,251.7 239.1,82.8" fill="#dbeafe" fill-opacity="0.72" stroke="none"/>'
    '<polygon points="117.5,85.0 104.7,118.8 177.2,139.7 262.5,127.0 275.3,93.2 202.8,72.3" '
    'fill="none" stroke="#0f172a" stroke-width="1.8" stroke-linejoin="round"/>'
    '<line x1="117.5" y1="85.0" x2="117.5" y2="197.0" stroke="#0f172a" stroke-width="1.7"/>'
    '<line x1="104.7" y1="118.8" x2="104.7" y2="230.8" stroke="#0f172a" stroke-width="1.7"/>'
    '<line x1="177.2" y1="139.7" x2="177.2" y2="251.7" stroke="#0f172a" stroke-width="1.7"/>'
    '<line x1="262.5" y1="127.0" x2="262.5" y2="239.0" stroke="#0f172a" stroke-width="1.7"/>'
    '<line x1="275.3" y1="93.2" x2="275.3" y2="205.2" stroke="#0f172a" stroke-width="1.7"/>'
    '<line x1="202.8" y1="72.3" x2="202.8" y2="184.3" stroke="#475569" stroke-width="1.3" stroke-dasharray="4,3"/>'
    '<line x1="117.5" y1="197.0" x2="104.7" y2="230.8" stroke="#0f172a" stroke-width="1.7"/>'
    '<line x1="104.7" y1="230.8" x2="177.2" y2="251.7" stroke="#0f172a" stroke-width="1.7"/>'
    '<line x1="177.2" y1="251.7" x2="262.5" y2="239.0" stroke="#0f172a" stroke-width="1.7"/>'
    '<line x1="262.5" y1="239.0" x2="275.3" y2="205.2" stroke="#0f172a" stroke-width="1.7"/>'
    '<line x1="275.3" y1="205.2" x2="202.8" y2="184.3" stroke="#475569" stroke-width="1.3" stroke-dasharray="4,3"/>'
    '<line x1="202.8" y1="184.3" x2="117.5" y2="197.0" stroke="#475569" stroke-width="1.3" stroke-dasharray="4,3"/>'
    '<line x1="117.5" y1="197.0" x2="177.2" y2="251.7" stroke="#1d4ed8" stroke-width="1.9"/>'
    '<line x1="117.5" y1="197.0" x2="239.1" y2="82.8" stroke="#1d4ed8" stroke-width="1.7" stroke-dasharray="4,3"/>'
    '<line x1="177.2" y1="251.7" x2="239.1" y2="82.8" stroke="#1d4ed8" stroke-width="1.9"/>'
    '<circle cx="239.1" cy="82.8" r="3.6" fill="#be123c"/>'
    '<text x="108" y="79" fill="#0f172a" font-size="12.5" font-weight="700" font-family="serif" font-style="italic">A</text>'
    '<text x="90" y="124" fill="#0f172a" font-size="12.5" font-weight="700" font-family="serif" font-style="italic">B</text>'
    '<text x="172" y="156" fill="#0f172a" font-size="12.5" font-weight="700" font-family="serif" font-style="italic">C</text>'
    '<text x="268" y="133" fill="#0f172a" font-size="12.5" font-weight="700" font-family="serif" font-style="italic">D</text>'
    '<text x="281" y="95" fill="#0f172a" font-size="12.5" font-weight="700" font-family="serif" font-style="italic">E</text>'
    '<text x="200" y="64" fill="#0f172a" font-size="12.5" font-weight="700" font-family="serif" font-style="italic">F</text>'
    '<text x="242" y="76" fill="#be123c" font-size="12.5" font-weight="800" font-family="serif" font-style="italic">M</text>'
    '<text x="104" y="198" fill="#0f172a" font-size="12.5" font-weight="700" font-family="serif" font-style="italic">G</text>'
    '<text x="89" y="236" fill="#0f172a" font-size="12.5" font-weight="700" font-family="serif" font-style="italic">H</text>'
    '<text x="172" y="269" fill="#0f172a" font-size="12.5" font-weight="700" font-family="serif" font-style="italic">I</text>'
    '<text x="268" y="248" fill="#0f172a" font-size="12.5" font-weight="700" font-family="serif" font-style="italic">J</text>'
    '<text x="281" y="209" fill="#0f172a" font-size="12.5" font-weight="700" font-family="serif" font-style="italic">K</text>'
    '<text x="202" y="177" fill="#475569" font-size="12.5" font-weight="700" font-family="serif" font-style="italic">L</text>'
    '<text x="180" y="290" fill="#475569" font-size="11.5" font-weight="700" text-anchor="middle" font-family="sans-serif">밑면 정육각형 한 변 4, 높이 2√6</text>'
    '</svg>'
)

ORIG_SVG_G29 = (
    '<svg viewBox="0 0 340 315" xmlns="http://www.w3.org/2000/svg" '
    'style="width:100%;max-width:330px;height:auto;display:block;margin:8px auto">'
    '<line x1="18" y1="238" x2="322" y2="238" stroke="#64748b" stroke-width="1.3"/>'
    '<line x1="172" y1="24" x2="172" y2="306" stroke="#64748b" stroke-width="1.3"/>'
    '<line x1="106.4" y1="28" x2="106.4" y2="306" stroke="#0369a1" stroke-width="1.5" stroke-dasharray="5,4"/>'
    '<path d="M 189.23 305.24 Q 172.0 271.62 172.0 238.0 Q 172.0 144.52 305.21 51.04" '
    'fill="none" stroke="#0f172a" stroke-width="2.1"/>'
    '<path d="M 285.63 305.24 C 256.58 265.34, 237.7 238.61, 223.96 217.93 C 210.22 197.26, 201.75 182.82, 196.28 170.78 C 190.81 158.73, 188.4 149.19, 188.4 139.6 C 188.4 133.23, 189.49 126.87, 191.8 119.79 C 194.11 112.72, 197.63 104.95, 202.75 95.61 C 207.87 86.27, 214.6 75.37, 223.67 61.7" '
    'fill="none" stroke="#2563eb" stroke-width="1.9"/>'
    '<path d="M 29.67 305.24 C 58.72 265.34, 77.6 238.61, 91.34 217.93 C 105.08 197.26, 113.55 182.82, 119.02 170.78 C 124.49 158.73, 126.9 149.19, 126.9 139.6 C 126.9 133.23, 125.81 126.87, 123.5 119.79 C 121.19 112.72, 117.67 104.95, 112.55 95.61 C 107.43 86.27, 100.7 75.37, 91.63 61.7" '
    'fill="none" stroke="#2563eb" stroke-width="1.9"/>'
    '<line x1="65" y1="262" x2="258" y2="5" stroke="#be123c" stroke-width="1.4" stroke-dasharray="4,3"/>'
    '<line x1="106.4" y1="139.6" x2="208.9" y2="139.6" stroke="#0f172a" stroke-width="1.4"/>'
    '<rect x="106.4" y="139.6" width="8" height="8" fill="none" stroke="#0369a1" stroke-width="1.1"/>'
    '<line x1="106.4" y1="139.6" x2="237.6" y2="238" stroke="#059669" stroke-width="1.4" stroke-dasharray="3,3"/>'
    '<line x1="208.9" y1="139.6" x2="237.6" y2="238" stroke="#059669" stroke-width="1.4" stroke-dasharray="3,3"/>'
    '<circle cx="172" cy="238" r="3" fill="#475569"/>'
    '<circle cx="237.6" cy="238" r="3.6" fill="#059669"/>'
    '<circle cx="208.9" cy="139.6" r="3.6" fill="#0f172a"/>'
    '<circle cx="106.4" cy="139.6" r="3.6" fill="#0f172a"/>'
    '<circle cx="126.9" cy="139.6" r="3.6" fill="#2563eb"/>'
    '<text x="322" y="252" fill="#475569" font-size="12" font-family="serif" font-style="italic">x</text>'
    '<text x="177" y="26" fill="#475569" font-size="12" font-family="serif" font-style="italic">y</text>'
    '<text x="160" y="253" fill="#475569" font-size="11.5" font-family="serif" font-style="italic">O</text>'
    '<text x="241" y="253" fill="#059669" font-size="12.5" font-weight="800" font-family="serif" font-style="italic">F</text>'
    '<text x="213" y="134" fill="#0f172a" font-size="12.5" font-weight="800" font-family="serif" font-style="italic">A</text>'
    '<text x="92" y="134" fill="#0f172a" font-size="12.5" font-weight="800" font-family="serif" font-style="italic">B</text>'
    '<text x="129" y="154" fill="#2563eb" font-size="12" font-weight="800" font-family="serif" font-style="italic">C</text>'
    '<text x="238" y="42" fill="#be123c" font-size="12.5" font-weight="800" font-family="serif" font-style="italic">l</text>'
    '<text x="110" y="38" fill="#0369a1" font-size="11" font-weight="700" font-family="sans-serif">준선</text>'
    '</svg>'
)

ORIG_SVG_G30 = (
    '<svg viewBox="0 0 380 280" xmlns="http://www.w3.org/2000/svg" '
    'style="width:100%;max-width:350px;height:auto;display:block;margin:8px auto">'
    '<polygon points="48,225 130,152 332,152 250,225" fill="#e0f2fe" fill-opacity="0.55" stroke="#0284c7" stroke-width="1.4"/>'
    '<circle cx="200" cy="128" r="90.56" fill="#eff6ff" fill-opacity="0.32" stroke="#1e293b" stroke-width="1.8"/>'
    '<ellipse cx="200" cy="184.73" rx="67.5" ry="23.09" fill="none" stroke="#1d4ed8" stroke-width="1.8"/>'
    '<line x1="200" y1="128" x2="200" y2="184.73" stroke="#475569" stroke-width="1.4" stroke-dasharray="3,3"/>'
    '<line x1="164.23" y1="204.31" x2="235.77" y2="165.15" stroke="#0f172a" stroke-width="1.6"/>'
    '<line x1="235.77" y1="165.15" x2="258.2" y2="194.2" stroke="#0f172a" stroke-width="1.5"/>'
    '<line x1="164.23" y1="204.31" x2="258.2" y2="194.2" stroke="#64748b" stroke-width="1.3" stroke-dasharray="4,3"/>'
    '<line x1="258.2" y1="194.2" x2="258.2" y2="74.5" stroke="#be123c" stroke-width="1.7" stroke-dasharray="4,3"/>'
    '<rect x="251.2" y="187.2" width="7" height="7" fill="none" stroke="#be123c" stroke-width="1.1"/>'
    '<circle cx="200" cy="128" r="3.4" fill="#0f172a"/>'
    '<circle cx="200" cy="184.73" r="3.2" fill="#475569"/>'
    '<circle cx="164.23" cy="204.31" r="3.4" fill="#0f172a"/>'
    '<circle cx="235.77" cy="165.15" r="3.4" fill="#0f172a"/>'
    '<circle cx="258.2" cy="194.2" r="3.4" fill="#0f172a"/>'
    '<circle cx="258.2" cy="74.5" r="3.6" fill="#be123c"/>'
    '<text x="190" y="122" fill="#0f172a" font-size="12.5" font-weight="800" font-family="serif" font-style="italic">O</text>'
    '<text x="187" y="198" fill="#475569" font-size="11.5" font-weight="700" font-family="serif" font-style="italic">H</text>'
    '<text x="150" y="216" fill="#0f172a" font-size="12" font-weight="800" font-family="serif" font-style="italic">A</text>'
    '<text x="239" y="162" fill="#0f172a" font-size="12" font-weight="800" font-family="serif" font-style="italic">B</text>'
    '<text x="263" y="201" fill="#0f172a" font-size="12" font-weight="800" font-family="serif" font-style="italic">C</text>'
    '<text x="264" y="75" fill="#be123c" font-size="12.5" font-weight="800" font-family="serif" font-style="italic">D</text>'
    '<text x="115" y="66" fill="#1e293b" font-size="12" font-weight="700" font-family="serif" font-style="italic">S₁</text>'
    '<text x="135" y="182" fill="#1d4ed8" font-size="11.5" font-weight="700" font-family="serif" font-style="italic">C₁</text>'
    '<text x="64" y="216" fill="#0284c7" font-size="12.5" font-weight="800" font-family="serif" font-style="italic">α</text>'
    '</svg>'
)

# ---------------------------------------------------------------------------
# Solution Visual Diagrams (G23 ~ G30)
# ---------------------------------------------------------------------------
_SVG_G23_INNER = (
    '<rect x="28" y="54" width="300" height="176" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>'
    '<text x="178" y="78" fill="#0369a1" font-size="12" font-weight="800" text-anchor="middle">① 좌표 성분 실수배 및 덧셈</text>'
    '<rect x="48" y="92" width="260" height="34" rx="7" fill="#eff6ff" stroke="#60a5fa"/>'
    '<text x="178" y="114" fill="#1e3a8a" font-size="12.5" font-weight="800" text-anchor="middle">2a⃗ = 2(1, 0) = (2, 0)</text>'
    '<rect x="48" y="136" width="260" height="34" rx="7" fill="#ecfdf5" stroke="#34d399"/>'
    '<text x="178" y="158" fill="#047857" font-size="12.5" font-weight="800" text-anchor="middle">b⃗ = (3, -2)</text>'
    '<rect x="48" y="180" width="260" height="36" rx="7" fill="#fef3c7" stroke="#f59e0b"/>'
    '<text x="178" y="203" fill="#92400e" font-size="13" font-weight="900" text-anchor="middle">2a⃗ + b⃗ = (2+3, 0-2) = (5, -2)</text>'
    '<rect x="348" y="54" width="304" height="176" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>'
    '<text x="500" y="78" fill="#047857" font-size="12" font-weight="800" text-anchor="middle">② 좌표평면 벡터 합 (머리-꼬리 법칙)</text>'
    '<line x1="376" y1="154" x2="626" y2="154" stroke="#64748b" stroke-width="1.4"/>'
    '<line x1="410" y1="92" x2="410" y2="210" stroke="#64748b" stroke-width="1.4"/>'
    '<line x1="410" y1="154" x2="478" y2="154" stroke="#2563eb" stroke-width="3"/>'
    '<circle cx="478" cy="154" r="4" fill="#2563eb"/>'
    '<text x="444" y="144" fill="#1d4ed8" font-size="11" font-weight="800" text-anchor="middle">2a⃗=(2,0)</text>'
    '<line x1="478" y1="154" x2="580" y2="196" stroke="#059669" stroke-width="2.5" stroke-dasharray="4,2"/>'
    '<line x1="410" y1="154" x2="580" y2="196" stroke="#be123c" stroke-width="3"/>'
    '<circle cx="580" cy="196" r="4.5" fill="#be123c"/>'
    '<text x="586" y="214" fill="#be123c" font-size="11.5" font-weight="900" text-anchor="middle">(5, -2) ⇒ 합 5+(-2)=3</text>'
)

_SVG_G24_INNER = (
    '<rect x="24" y="54" width="356" height="192" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>'
    '<line x1="40" y1="150" x2="364" y2="150" stroke="#64748b" stroke-width="1.3"/>'
    '<line x1="168" y1="68" x2="168" y2="234" stroke="#64748b" stroke-width="1.3"/>'
    '<line x1="56" y1="74" x2="56" y2="226" stroke="#0369a1" stroke-width="1.5" stroke-dasharray="5,3"/>'
    '<path d="M 332 72 Q 68 150 332 228" fill="none" stroke="#2563eb" stroke-width="2.5"/>'
    '<circle cx="136" cy="150" r="4.5" fill="#4f46e5"/>'
    '<text x="128" y="168" fill="#4f46e5" font-size="11" font-weight="800" text-anchor="end">V(-1,0)</text>'
    '<circle cx="264" cy="150" r="4.5" fill="#be123c"/>'
    '<text x="268" y="168" fill="#be123c" font-size="11.5" font-weight="800">F(3,0)</text>'
    '<circle cx="168" cy="100" r="4.5" fill="#047857"/>'
    '<text x="174" y="96" fill="#047857" font-size="11.5" font-weight="800">(0, a)</text>'
    '<line x1="56" y1="100" x2="168" y2="100" stroke="#d97706" stroke-width="1.8" stroke-dasharray="3,2"/>'
    '<line x1="168" y1="100" x2="264" y2="150" stroke="#d97706" stroke-width="1.8" stroke-dasharray="3,2"/>'
    '<text x="112" y="92" fill="#b45309" font-size="10.8" font-weight="800" text-anchor="middle">준선 x=-5까지 거리 5</text>'
    '<rect x="396" y="54" width="260" height="192" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>'
    '<text x="526" y="80" fill="#0369a1" font-size="12" font-weight="800" text-anchor="middle">평행이동 초점 파라미터 p = 4</text>'
    '<text x="526" y="110" fill="#1e293b" font-size="11.8" font-weight="700" text-anchor="middle">• 꼭짓점 (-1, 0) ➔ 초점 (3, 0)</text>'
    '<text x="526" y="136" fill="#1e293b" font-size="11.8" font-weight="700" text-anchor="middle">• p = 3 - (-1) = 4 ⇒ y² = 16(x+1)</text>'
    '<text x="526" y="164" fill="#047857" font-size="12" font-weight="800" text-anchor="middle">• (0, a) 대입: a² = 16(0+1) = 16</text>'
    '<rect x="424" y="184" width="204" height="42" rx="9" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.5"/>'
    '<text x="526" y="210" fill="#92400e" font-size="13.5" font-weight="900" text-anchor="middle">a &gt; 0 ⇒ a = 4 (④)</text>'
)

_SVG_G25_INNER = (
    '<rect x="24" y="54" width="312" height="184" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>'
    '<text x="180" y="78" fill="#0369a1" font-size="12" font-weight="800" text-anchor="middle">① yz평면 위 (x좌표=0): 2:1 내분점</text>'
    '<line x1="56" y1="126" x2="304" y2="126" stroke="#2563eb" stroke-width="2.6"/>'
    '<circle cx="56" cy="126" r="5" fill="#1d4ed8"/><text x="56" y="112" fill="#1d4ed8" font-size="11" font-weight="800" text-anchor="middle">A(a,-3,6)</text>'
    '<circle cx="221" cy="126" r="5.5" fill="#be123c"/><text x="221" y="110" fill="#be123c" font-size="11" font-weight="900" text-anchor="middle">내분점 P(x=0)</text>'
    '<circle cx="304" cy="126" r="5" fill="#059669"/><text x="304" y="112" fill="#059669" font-size="11" font-weight="800" text-anchor="middle">B(-3,b,c)</text>'
    '<text x="138" y="146" fill="#334155" font-size="11" font-weight="700" text-anchor="middle">2</text>'
    '<text x="262" y="146" fill="#334155" font-size="11" font-weight="700" text-anchor="middle">1</text>'
    '<rect x="44" y="164" width="272" height="58" rx="8" fill="#eff6ff" stroke="#60a5fa"/>'
    '<text x="180" y="187" fill="#1e3a8a" font-size="12" font-weight="800" text-anchor="middle">(2×(-3) + 1×a) / 3 = 0</text>'
    '<text x="180" y="209" fill="#be123c" font-size="13" font-weight="900" text-anchor="middle">⇒ a - 6 = 0 ⇒ a = 6</text>'
    '<rect x="352" y="54" width="304" height="184" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>'
    '<text x="504" y="78" fill="#047857" font-size="12" font-weight="800" text-anchor="middle">② x축 위 (y=0, z=0): 3:2 외분점</text>'
    '<rect x="370" y="94" width="268" height="40" rx="8" fill="#ecfdf5" stroke="#34d399"/>'
    '<text x="504" y="119" fill="#047857" font-size="12" font-weight="800" text-anchor="middle">y좌표: (3b - 2(-3)) / (3-2) = 0 ⇒ b = -2</text>'
    '<rect x="370" y="144" width="268" height="40" rx="8" fill="#ecfdf5" stroke="#34d399"/>'
    '<text x="504" y="169" fill="#047857" font-size="12" font-weight="800" text-anchor="middle">z좌표: (3c - 2(6)) / (3-2) = 0 ⇒ c = 4</text>'
    '<rect x="394" y="194" width="220" height="34" rx="8" fill="#fef3c7" stroke="#f59e0b"/>'
    '<text x="504" y="216" fill="#92400e" font-size="13" font-weight="900" text-anchor="middle">a + b + c = 6 - 2 + 4 = 8 (③)</text>'
)

_SVG_G26_INNER = (
    '<rect x="24" y="54" width="346" height="194" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>'
    '<line x1="40" y1="152" x2="354" y2="152" stroke="#64748b" stroke-width="1.3"/>'
    '<line x1="197" y1="68" x2="197" y2="236" stroke="#64748b" stroke-width="1.3"/>'
    '<ellipse cx="197" cy="152" rx="130" ry="72" fill="rgba(59,130,246,0.06)" stroke="#2563eb" stroke-width="2.2"/>'
    '<circle cx="115" cy="152" r="4" fill="#be123c"/><text x="108" y="170" fill="#be123c" font-size="11.5" font-weight="800" text-anchor="middle">F′(-c,0)</text>'
    '<circle cx="279" cy="152" r="4" fill="#0369a1"/><text x="292" y="169" fill="#0369a1" font-size="11.5" font-weight="800">F(c,0)</text>'
    '<line x1="279" y1="96" x2="279" y2="208" stroke="#047857" stroke-width="2.2"/>'
    '<line x1="115" y1="152" x2="279" y2="96" stroke="#d97706" stroke-width="2" stroke-dasharray="4,2"/>'
    '<circle cx="279" cy="96" r="4" fill="#047481"/><text x="285" y="92" fill="#047857" font-size="11.5" font-weight="800">P</text>'
    '<circle cx="279" cy="208" r="4" fill="#047481"/><text x="285" y="218" fill="#047857" font-size="11.5" font-weight="800">Q</text>'
    '<text x="188" y="114" fill="#b45309" font-size="11.5" font-weight="900">PF′ = 7</text>'
    '<text x="312" y="132" fill="#047857" font-size="11.2" font-weight="800">PF = 3</text>'
    '<rect x="386" y="54" width="270" height="194" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>'
    '<text x="521" y="80" fill="#0369a1" font-size="12" font-weight="800" text-anchor="middle">대칭성과 타원의 정의 (거리 합 2a)</text>'
    '<text x="521" y="108" fill="#1e293b" font-size="11.6" font-weight="700" text-anchor="middle">① x축 대칭: PQ = 6 ⇒ PF = 3</text>'
    '<text x="521" y="134" fill="#1e293b" font-size="11.6" font-weight="700" text-anchor="middle">② PF + PF′ = 3 + 7 = 10 = 2a ⇒ a = 5</text>'
    '<text x="521" y="160" fill="#047857" font-size="11.8" font-weight="800" text-anchor="middle">③ 통경 PF = b²/a = 3 ⇒ b² = 15</text>'
    '<text x="521" y="182" fill="#475569" font-size="11" font-weight="700" text-anchor="middle">(또는 직각삼각형 F′FP: c = √10)</text>'
    '<rect x="412" y="196" width="218" height="38" rx="8" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.5"/>'
    '<text x="521" y="220" fill="#92400e" font-size="13.5" font-weight="900" text-anchor="middle">a² + b² = 25 + 15 = 40 (⑤)</text>'
)

_SVG_G27_INNER = (
    '<rect x="22" y="54" width="320" height="202" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>'
    '<text x="182" y="76" fill="#0369a1" font-size="12" font-weight="800" text-anchor="middle">① 밑면 정육각형 GHIJKL 위 수선의 발 M′</text>'
    '<polygon points="248,158 215,102 149,102 116,158 149,214 215,214" fill="#f8fafc" stroke="#1e293b" stroke-width="1.8"/>'
    '<line x1="248" y1="158" x2="149" y2="102" stroke="#1d4ed8" stroke-width="2.4"/>'
    '<line x1="182" y1="214" x2="198.5" y2="130" stroke="#be123c" stroke-width="2" stroke-dasharray="4,2"/>'
    '<circle cx="248" cy="158" r="3.5" fill="#1d4ed8"/><text x="256" y="162" fill="#1d4ed8" font-size="11" font-weight="800">G</text>'
    '<circle cx="215" cy="102" r="3.5" fill="#475569"/><text x="221" y="99" fill="#475569" font-size="11" font-weight="700">H</text>'
    '<circle cx="149" cy="102" r="3.5" fill="#1d4ed8"/><text x="136" y="99" fill="#1d4ed8" font-size="11" font-weight="800">I</text>'
    '<circle cx="116" cy="158" r="3.5" fill="#475569"/><text x="102" y="162" fill="#475569" font-size="11" font-weight="700">J</text>'
    '<circle cx="149" cy="214" r="3.5" fill="#475569"/><text x="139" y="230" fill="#475569" font-size="11" font-weight="700">K</text>'
    '<circle cx="215" cy="214" r="3.5" fill="#475569"/><text x="221" y="230" fill="#475569" font-size="11" font-weight="700">L</text>'
    '<circle cx="182" cy="214" r="4.2" fill="#be123c"/><text x="182" y="236" fill="#be123c" font-size="11.5" font-weight="900" text-anchor="middle">M′ (KL 중점)</text>'
    '<text x="206" y="176" fill="#be123c" font-size="11.5" font-weight="800">M′N = 5</text>'
    '<text x="186" y="122" fill="#1d4ed8" font-size="11.5" font-weight="800">GI = 4√3</text>'
    '<rect x="358" y="54" width="298" height="202" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>'
    '<text x="507" y="78" fill="#047857" font-size="12" font-weight="800" text-anchor="middle">② 삼수선의 정리: 직각삼각형 MM′N</text>'
    '<polygon points="418,196 558,196 418,104" fill="#ecfdf5" stroke="#059669" stroke-width="2"/>'
    '<rect x="418" y="184" width="12" height="12" fill="none" stroke="#059669" stroke-width="1.4"/>'
    '<text x="410" y="100" fill="#be123c" font-size="11.5" font-weight="800" text-anchor="end">M</text>'
    '<text x="410" y="202" fill="#be123c" font-size="11.5" font-weight="800" text-anchor="end">M′</text>'
    '<text x="564" y="202" fill="#1d4ed8" font-size="11.5" font-weight="800">N (GI 위)</text>'
    '<text x="394" y="152" fill="#047857" font-size="11.5" font-weight="800" text-anchor="end">2√6</text>'
    '<text x="488" y="214" fill="#be123c" font-size="11.5" font-weight="800" text-anchor="middle">5</text>'
    '<text x="520" y="140" fill="#1d4ed8" font-size="12" font-weight="900">MN = √(24+25) = 7</text>'
    '<rect x="380" y="222" width="256" height="26" rx="7" fill="#fef3c7" stroke="#f59e0b"/>'
    '<text x="508" y="240" fill="#92400e" font-size="12.2" font-weight="900" text-anchor="middle">넓이 = (1/2) × 4√3 × 7 = 14√3 (①)</text>'
)

_SVG_G28_INNER = (
    '<rect x="24" y="54" width="332" height="202" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>'
    '<text x="190" y="76" fill="#0369a1" font-size="11.8" font-weight="800" text-anchor="middle">① 자취 R: 평행사변형 ∩ 반평면 (x+2y ≥ 10)</text>'
    '<line x1="48" y1="226" x2="332" y2="226" stroke="#64748b" stroke-width="1.3"/>'
    '<line x1="78" y1="78" x2="78" y2="244" stroke="#64748b" stroke-width="1.3"/>'
    '<polygon points="78,226 174,226 270,86 174,86" fill="#e2e8f0" fill-opacity="0.45" stroke="#94a3b8" stroke-width="1.4" stroke-dasharray="4,3"/>'
    '<polygon points="174,86 270,86 238,109 174,109" fill="#bbf7d0" stroke="#059669" stroke-width="2"/>'
    '<line x1="126" y1="80" x2="320" y2="174" stroke="#be123c" stroke-width="1.8" stroke-dasharray="4,2"/>'
    '<circle cx="126" cy="226" r="4" fill="#d97706"/><text x="126" y="242" fill="#b45309" font-size="10.8" font-weight="800" text-anchor="middle">중심 (1,0)</text>'
    '<circle cx="270" cy="86" r="4.5" fill="#1d4ed8"/><text x="276" y="84" fill="#1d4ed8" font-size="10.8" font-weight="800">(4,4) 최대 M</text>'
    '<circle cx="212" cy="100" r="4.5" fill="#be123c"/><text x="262" y="128" fill="#be123c" font-size="10.8" font-weight="800" text-anchor="middle">수선의 발 (14/5, 18/5) 최소 m</text>'
    '<rect x="372" y="54" width="284" height="202" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>'
    '<text x="514" y="80" fill="#047857" font-size="12" font-weight="800" text-anchor="middle">② 원 위 점 거리² 최소화/최대화</text>'
    '<text x="514" y="108" fill="#1e293b" font-size="11.3" font-weight="700" text-anchor="middle">O(0,0), B(2,0), A(2,2) 좌표 설정</text>'
    '<text x="514" y="132" fill="#1e293b" font-size="11.3" font-weight="700" text-anchor="middle">R(x,y): 0≤y≤4, y-2≤x≤y, x+2y≥10</text>'
    '<text x="514" y="156" fill="#0369a1" font-size="11.5" font-weight="800" text-anchor="middle">OR⃗·BR⃗ = (x-1)² + y² - 1</text>'
    '<text x="514" y="180" fill="#1d4ed8" font-size="11.5" font-weight="800" text-anchor="middle">• M at (4,4): 3² + 4² - 1 = 24</text>'
    '<text x="514" y="202" fill="#be123c" font-size="11.5" font-weight="800" text-anchor="middle">• m at x+2y=10 수직거리: 81/5 - 1 = 76/5</text>'
    '<rect x="394" y="216" width="240" height="30" rx="7" fill="#fef3c7" stroke="#f59e0b"/>'
    '<text x="514" y="236" fill="#92400e" font-size="12.5" font-weight="900" text-anchor="middle">M + m = 24 + 76/5 = 196/5 (④)</text>'
)

_SVG_G29_INNER = (
    '<rect x="24" y="54" width="320" height="202" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>'
    '<text x="184" y="76" fill="#0369a1" font-size="11.8" font-weight="800" text-anchor="middle">① 비율 k=5t, BF=8t ➔ 3:4:5 쌍곡선</text>'
    '<line x1="60" y1="118" x2="262" y2="118" stroke="#0f172a" stroke-width="2"/>'
    '<line x1="60" y1="118" x2="296" y2="218" stroke="#059669" stroke-width="2"/>'
    '<line x1="262" y1="118" x2="296" y2="218" stroke="#1d4ed8" stroke-width="2"/>'
    '<circle cx="60" cy="118" r="4.5" fill="#0f172a"/><text x="50" y="114" fill="#0f172a" font-size="11.5" font-weight="800" text-anchor="end">B</text>'
    '<circle cx="102" cy="118" r="4.5" fill="#be123c"/><text x="102" y="106" fill="#be123c" font-size="11.5" font-weight="800" text-anchor="middle">C</text>'
    '<circle cx="262" cy="118" r="4.5" fill="#0f172a"/><text x="270" y="114" fill="#0f172a" font-size="11.5" font-weight="800">A</text>'
    '<circle cx="296" cy="218" r="4.5" fill="#059669"/><text x="304" y="222" fill="#059669" font-size="11.5" font-weight="800">F</text>'
    '<text x="81" y="136" fill="#be123c" font-size="10.8" font-weight="800" text-anchor="middle">BC=t</text>'
    '<text x="180" y="108" fill="#0f172a" font-size="11" font-weight="800" text-anchor="middle">AB = AF = 5t</text>'
    '<text x="164" y="182" fill="#059669" font-size="11" font-weight="800">BF = 8t</text>'
    '<text x="292" y="168" fill="#1d4ed8" font-size="11" font-weight="800">AF = 5t</text>'
    '<rect x="52" y="216" width="220" height="28" rx="6" fill="#eff6ff" stroke="#60a5fa"/>'
    '<text x="162" y="235" fill="#1e3a8a" font-size="11.2" font-weight="800" text-anchor="middle">주축 2a′=3t, 2c′=5t ⇒ 점근선 기울기 4/3</text>'
    '<rect x="360" y="54" width="296" height="202" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>'
    '<text x="508" y="80" fill="#047857" font-size="12" font-weight="800" text-anchor="middle">② 점 F와 점근선 l 거리 = 15 이용</text>'
    '<text x="508" y="108" fill="#1e293b" font-size="11.3" font-weight="700" text-anchor="middle">• 4px: BF² = 4pk ⇒ (8t)² = 4p(5t) ⇒ p = 16t/5</text>'
    '<text x="508" y="134" fill="#1e293b" font-size="11.3" font-weight="700" text-anchor="middle">• 중심 M(-7t/10, 24t/5), 기울기 4/3 직선 l:</text>'
    '<text x="508" y="156" fill="#0369a1" font-size="11.3" font-weight="800" text-anchor="middle">4x - 3y + (86/5)t = 0</text>'
    '<text x="508" y="182" fill="#be123c" font-size="11.5" font-weight="800" text-anchor="middle">• d(F, l) = 6t = 15 ⇒ t = 5/2 (p = 8)</text>'
    '<rect x="384" y="204" width="248" height="36" rx="8" fill="#fef3c7" stroke="#f59e0b"/>'
    '<text x="508" y="227" fill="#92400e" font-size="13" font-weight="900" text-anchor="middle">둘레 18t = 18 × (5/2) = 45</text>'
)

_SVG_G30_INNER = (
    '<rect x="24" y="54" width="318" height="202" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>'
    '<text x="183" y="76" fill="#0369a1" font-size="11.8" font-weight="800" text-anchor="middle">① 단면 원 C₁ (반지름 5) &amp; 평면 OAB 거리 R₂</text>'
    '<circle cx="150" cy="164" r="64" fill="#eff6ff" stroke="#2563eb" stroke-width="1.8"/>'
    '<line x1="86" y1="164" x2="214" y2="164" stroke="#0f172a" stroke-width="2.2"/>'
    '<line x1="86" y1="164" x2="164" y2="102" stroke="#64748b" stroke-width="1.5" stroke-dasharray="3,2"/>'
    '<line x1="214" y1="164" x2="164" y2="102" stroke="#047857" stroke-width="2"/>'
    '<line x1="164" y1="102" x2="164" y2="164" stroke="#be123c" stroke-width="2"/>'
    '<circle cx="86" cy="164" r="3.5" fill="#0f172a"/><text x="72" y="168" fill="#0f172a" font-size="11" font-weight="800">A</text>'
    '<circle cx="214" cy="164" r="3.5" fill="#0f172a"/><text x="220" y="168" fill="#0f172a" font-size="11" font-weight="800">B</text>'
    '<circle cx="164" cy="102" r="3.5" fill="#be123c"/><text x="168" y="96" fill="#be123c" font-size="11" font-weight="800">C</text>'
    '<text x="188" y="138" fill="#be123c" font-size="11" font-weight="800">R₂=2√6</text>'
    '<text x="148" y="182" fill="#0f172a" font-size="10.8" font-weight="800" text-anchor="middle">지름 AB = 10</text>'
    '<text x="195" y="128" fill="#047857" font-size="10.5" font-weight="800"> </text>'
    '<text x="272" y="132" fill="#1e293b" font-size="10.8" font-weight="700" text-anchor="middle">CD ∥ OH</text>'
    '<text x="272" y="150" fill="#1e293b" font-size="10.8" font-weight="700" text-anchor="middle">⇒ CD ∥ 평면OAB</text>'
    '<text x="272" y="170" fill="#be123c" font-size="11.2" font-weight="800" text-anchor="middle">R₂ = 2√6</text>'
    '<rect x="358" y="54" width="298" height="202" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>'
    '<text x="507" y="78" fill="#047857" font-size="12" font-weight="800" text-anchor="middle">② 이등변 △ODP로 C₂ 반지름 r₂ &amp; 정사영</text>'
    '<polygon points="392,162 492,162 442,102" fill="#ecfdf5" stroke="#059669" stroke-width="1.8"/>'
    '<text x="384" y="168" fill="#0f172a" font-size="11" font-weight="800" text-anchor="end">O</text>'
    '<text x="498" y="168" fill="#be123c" font-size="11" font-weight="800">D</text>'
    '<text x="442" y="96" fill="#1d4ed8" font-size="11" font-weight="800" text-anchor="middle">P (C₂ 위)</text>'
    '<text x="580" y="114" fill="#1e293b" font-size="11" font-weight="700" text-anchor="middle">OD = OP = 3√5</text>'
    '<text x="580" y="134" fill="#be123c" font-size="11" font-weight="800" text-anchor="middle">DP = 2√6</text>'
    '<text x="580" y="156" fill="#1d4ed8" font-size="11.5" font-weight="800" text-anchor="middle">⇒ r₂² = 104 / 5</text>'
    '<text x="507" y="192" fill="#0369a1" font-size="11.5" font-weight="800" text-anchor="middle">cosθ = (2√5)/(3√5) = 2/3</text>'
    '<rect x="382" y="206" width="250" height="34" rx="8" fill="#fef3c7" stroke="#f59e0b"/>'
    '<text x="507" y="228" fill="#92400e" font-size="12.5" font-weight="900" text-anchor="middle">정사영 넓이 = (208/15)π ⇒ p+q = 223</text>'
)

PART5_PROBLEMS = [
    # =========================================================================
    # 기하 23번 (csat27_g23) — 2점, 정답 3 (3)
    # =========================================================================
    {
        'slug': 'csat27_g23',
        'qNum': '23',
        'points': 2,
        'is_short_answer': False,
        'official_ans_str': '',
        'subject': '기하',
        'title': '[2027학년도 수능 고3 기하 23번] 평면벡터의 실수배와 성분별 덧셈',
        'title_en': '[2027 CSAT Math Geometry #23] Scalar Multiplication and Componentwise Sum of Vectors',
        'summary_ko': r'두 평면벡터 $\vec{a}=(1,0)$, $\vec{b}=(3,-2)$가 주어졌을 때, $2\vec{a}+\vec{b}$의 모든 성분의 합을 구하는 기본 문항입니다.',
        'summary_en': r'Given plane vectors $\vec{a}=(1,0)$ and $\vec{b}=(3,-2)$, find the sum of all components of $2\vec{a}+\vec{b}$.',
        'tags': ['2027학년도 수능', '기하', '평면벡터', '벡터의 실수배', '벡터의 성분'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': r'$\vec{a}=(x_1, y_1)$',
                'desc': '화살표가 오른쪽과 위쪽으로 각각 몇 칸 이동하는지 나타낸 순서쌍(평면벡터의 성분)입니다.',
                'desc_en': 'Component representation of a 2D vector showing horizontal and vertical displacements.',
            },
            {
                'sym': r'$2\vec{a}$',
                'desc': r'벡터 $\vec{a}$의 각 성분에 $2$를 곱하여 길이를 $2$배로 늘린 실수배 벡터 $(2x_1, 2y_1)$입니다.',
                'desc_en': r'Scalar multiple $2\vec{a}=(2x_1, 2y_1)$, doubling each component.',
            },
            {
                'sym': r'$2\vec{a}+\vec{b}$',
                'desc': r'$x$성분끼리 더하고 $y$성분끼리 더하여 얻는 두 벡터의 합입니다.',
                'desc_en': r'Componentwise vector addition of $2\vec{a}$ and $\vec{b}$.',
            },
        ],
        'levels': [
            {
                'title': r'🔰 1단계 · [초등 기초 직관] 화살표 이동 두 번 이어 붙이기',
                'title_en': r'🔰 Step 1 · [Elementary Intuition] Doubling a Horizontal Step',
                'knowledge': r'바둑판 위에서 오른쪽으로 $1$칸, 위쪽으로 $0$칸 이동하는 규칙을 똑같이 $2$번 반복하면 오른쪽으로 $2$칸 이동하게 됩니다.',
                'knowledge_en': r'Repeating a move of $1$ step right and $0$ steps up twice produces $2$ steps right and $0$ steps up.',
                'questions': [{
                    'level_label': '초등 기초 직관 디딤돌 1',
                    'level_label_en': 'Elementary Intuition Step 1',
                    'stem': r'오른쪽으로 $1$칸 가는 이동 $(1,\;0)$을 $2$번 반복한 이동 $2(1,\;0)$을 좌표로 나타낸 것은?',
                    'stem_en': r'What coordinate move equals repeating $(1,\;0)$ twice, i.e., $2(1,\;0)$?',
                    'options': [r'$(1,\;0)$', r'$(2,\;0)$', r'$(2,\;2)$', r'$(3,\;0)$', r'$(0,\;2)$'],
                    'answer': 2,
                    'exp': r'$x$칸 수 $1$을 $2$배 하면 $2$, $y$칸 수 $0$을 $2$배 하면 $0$이므로 $(2,\;0)$입니다.',
                    'exp_en': r'Multiplying each entry by $2$ gives $(2\times 1,\; 2\times 0) = (2,\;0)$.',
                }],
            },
            {
                'title': r'🌿 2단계 · [성분별 덧셈] $x$성분끼리, $y$성분끼리 모으기',
                'title_en': r'🌿 Step 2 · [Component Addition] Adding $x$ and $y$ Components Separately',
                'knowledge': r'벡터의 덧셈 $(x_1, y_1) + (x_2, y_2)$는 가로 이동량 $x_1+x_2$와 세로 이동량 $y_1+y_2$를 각각 더합니다.',
                'knowledge_en': r'Vector sum adds first entries together and second entries together: $(x_1+x_2, y_1+y_2)$.',
                'questions': [{
                    'level_label': '벡터 $x$성분 계산 디딤돌 2',
                    'level_label_en': 'First Component Step 2',
                    'stem': r'$2\vec{a} = (2,\;0)$과 $\vec{b} = (3,\;-2)$를 더한 벡터 $2\vec{a}+\vec{b}$의 $x$성분은?',
                    'stem_en': r'What is the $x$-component of $2\vec{a}+\vec{b}$ for $2\vec{a}=(2,0)$ and $\vec{b}=(3,-2)$?',
                    'options': [r'$1$', r'$3$', r'$4$', r'$5$', r'$6$'],
                    'answer': 4,
                    'exp': r'$2 + 3 = 5$이므로 $x$성분은 $5$입니다.',
                    'exp_en': r'Adding the $x$-components gives $2+3=5$.',
                }],
            },
            {
                'title': r'🌱 3단계 · [$y$성분 계산] 음수가 포함된 세로 성분 더하기',
                'title_en': r'🌱 Step 3 · [Second Component] Adding Negative Vertical Movement',
                'knowledge': r'$0$에 $-2$를 더하면 아래쪽으로 $2$칸 내려간 위치인 $-2$가 됩니다.',
                'knowledge_en': r'Adding $0$ and $-2$ gives $-2$.',
                'questions': [{
                    'level_label': '벡터 $y$성분 계산 디딤돌 3',
                    'level_label_en': 'Second Component Step 3',
                    'stem': r'$2\vec{a}+\vec{b} = (2+3,\; 0 + [\;\text{(가)}\;])$의 $y$성분 $0+(-2)$의 값은?',
                    'stem_en': r'What is the $y$-component $0+(-2)$ of $2\vec{a}+\vec{b}$?',
                    'options': [r'$-4$', r'$-2$', r'$0$', r'$2$', r'$4$'],
                    'answer': 2,
                    'exp': r'$0 + (-2) = -2$이므로 $2\vec{a}+\vec{b}=(5,\;-2)$입니다.',
                    'exp_en': r'$0+(-2)=-2$, so $2\vec{a}+\vec{b}=(5,-2)$.',
                }],
            },
            {
                'title': r'🌳 4단계 · [성분 확정] 벡터 $2\vec{a}+\vec{b}$ 완성하기',
                'title_en': r'🌳 Step 4 · [Resulting Vector] Confirming $(5, -2)$',
                'knowledge': r'구한 두 성분을 순서쌍으로 묶으면 $2\vec{a}+\vec{b} = (5,\;-2)$입니다.',
                'knowledge_en': r'Combining both entries yields $2\vec{a}+\vec{b} = (5,\;-2)$.',
                'questions': [{
                    'level_label': '벡터 확정 디딤돌 4',
                    'level_label_en': 'Vector Result Step 4',
                    'stem': r'두 벡터 $\vec{a}=(1,0),\; \vec{b}=(3,-2)$에 대하여 $2\vec{a}+\vec{b}$를 바르게 나타낸 것은?',
                    'stem_en': r'Which ordered pair equals $2\vec{a}+\vec{b}$?',
                    'options': [r'$(4,\;-2)$', r'$(5,\;-2)$', r'$(5,\;2)$', r'$(6,\;-2)$', r'$(7,\;-4)$'],
                    'answer': 2,
                    'exp': r'$2(1,0)+(3,-2) = (2,0)+(3,-2) = (5,-2)$입니다.',
                    'exp_en': r'$2(1,0)+(3,-2)=(5,-2)$.',
                }],
            },
            {
                'title': r'💎 5단계 · [최종 종합] 모든 성분의 합 구하기',
                'title_en': r'💎 Step 5 · [Final Synthesis] Sum of All Components',
                'knowledge': r'모든 성분의 합은 $x$성분 $5$와 $y$성분 $-2$를 더한 값입니다.',
                'knowledge_en': r'Sum the $x$-component $5$ and $y$-component $-2$.',
                'questions': [{
                    'level_label': '최종 종합 디딤돌 5',
                    'level_label_en': 'Final Synthesis Step 5',
                    'stem': r'벡터 $2\vec{a}+\vec{b}=(5,\;-2)$의 모든 성분의 합 $5 + (-2)$는?',
                    'stem_en': r'What is $5+(-2)$, the sum of all components of $(5,-2)$?',
                    'options': [r'$1$', r'$2$', r'$3$', r'$4$', r'$5$'],
                    'answer': 3,
                    'exp': r'$5 + (-2) = 3$이므로 정답은 ③번입니다.',
                    'exp_en': r'$5+(-2)=3$ (choice ③).',
                }],
            },
        ],
        'final': {
            'stem': r'두 벡터 $\vec{a}=(1,\;0)$, $\vec{b}=(3,\;-2)$에 대하여 $2\vec{a}+\vec{b}$의 모든 성분의 합은? [2점]',
            'stem_en': r'For two vectors $\vec{a}=(1,\;0)$ and $\vec{b}=(3,\;-2)$, what is the sum of all components of $2\vec{a}+\vec{b}$? [2 points]',
            'options': [r'$1$', r'$2$', r'$3$', r'$4$', r'$5$'],
            'answer': 3,
            'exp': r'$2\vec{a}+\vec{b} = 2(1,0)+(3,-2) = (2+3,\; 0-2) = (5,\;-2)$이므로 모든 성분의 합은 $5+(-2)=3$입니다.',
            'exp_en': r'$2\vec{a}+\vec{b}=(2,0)+(3,-2)=(5,-2)$, whose component sum is $5+(-2)=3$.',
            'solution': (
                r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>""" + '\n'
                + r"""<p>본 문항은 평면벡터의 성분 표시에서 <b>벡터의 실수배 $k(x, y)=(kx, ky)$</b>와 <b>벡터의 덧셈 $(x_1, y_1)+(x_2, y_2)=(x_1+x_2, y_1+y_2)$</b>을 정확히 계산할 수 있는지 평가하는 기본 문항입니다.</p>""" + '\n'
                + _wrap_visual_svg(
                    "📐 [2027 수능 기하 23번] 평면벡터 성분 연산과 기하학적 합",
                    "2a⃗ + b⃗ = (5, -2) ➔ 3",
                    _SVG_G23_INNER,
                    height=244,
                    lang="ko",
                    caption="▲ 오른쪽으로 2칸 간 벡터 2a⃗=(2,0) 끝에서 (3,-2)만큼 이어 이동하면 최종 위치 (5,-2)에 도착합니다.",
                )
                + _wrap_schematic_flow(
                    [
                        r"실수배 $2\vec{a} = (2, 0)$",
                        r"$x$성분 덧셈 $2 + 3 = 5$",
                        r"$y$성분 덧셈 $0 + (-2) = -2$",
                        r"성분 총합 $5 + (-2)$",
                    ],
                    r"$3$ (③)",
                    lang="ko",
                )
                + r"""<h4>📐 [단계별 상세 풀이 전개]</h4>""" + '\n'
                + r"""<p><b>1단계: 벡터의 실수배 계산</b><br>$$2\vec{a} = 2(1,\;0) = (2 \times 1,\; 2 \times 0) = (2,\;0)$$<br><br><b>2단계: 성분별 벡터 덧셈 및 성분 합 구하기</b><br>$$2\vec{a}+\vec{b} = (2,\;0) + (3,\;-2) = (2+3,\; 0+(-2)) = (5,\;-2)$$ 따라서 모든 성분의 합은 $5 + (-2) = 3$입니다.</p>""" + '\n'
                + r"""<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>""" + '\n'
                + r'<p>따라서 구하는 값은 <b>$3$</b>이므로 정답은 <b>③번</b>입니다. (<a href="https://min7014.github.io/" target="_blank" rel="noopener">수학자료실(min7014.github.io)</a>의 벡터 연산 시각화 자료로 평면벡터의 머리-꼬리 합성을 함께 확인해 보세요.)</p>'
            ),
            'solution_en': (
                r"""<h4>📋 [Problem Analysis &amp; Core Concepts]</h4>""" + '\n'
                + r"""<p>This problem tests scalar multiplication $k(x,y)=(kx,ky)$ and componentwise addition of 2D plane vectors.</p>""" + '\n'
                + _wrap_visual_svg(
                    "📐 [2027 CSAT Geometry #23] Componentwise Vector Operation",
                    "2a + b = (5, -2) => Sum = 3",
                    _SVG_G23_INNER,
                    height=244,
                    lang="en",
                    caption="▲ Combining 2a=(2,0) and b=(3,-2) gives resultant vector (5,-2).",
                )
                + _wrap_schematic_flow(
                    [
                        r"Scale $2\vec{a}=(2,0)$",
                        r"Add $x$: $2+3=5$",
                        r"Add $y$: $0+(-2)=-2$",
                        r"Sum $5+(-2)=3$",
                    ],
                    r"$3$ (③)",
                    lang="en",
                )
                + r"""<h4>📐 [Step-by-Step Rigorous Derivation]</h4>""" + '\n'
                + r"""<p>$$2\vec{a}+\vec{b} = 2(1,0)+(3,-2) = (2,0)+(3,-2) = (5,-2)$$ Summing all components gives $5 + (-2) = 3$.</p>""" + '\n'
                + r"""<h4>✨ [Conclusion &amp; Key Takeaways]</h4>""" + '\n'
                + r'<p>The component sum is <b>$3$</b>, corresponding to <b>choice ③</b>.</p>'
            ),
        },
    },

    # =========================================================================
    # 기하 24번 (csat27_g24) — 3점, 정답 4 (4)
    # =========================================================================
    {
        'slug': 'csat27_g24',
        'qNum': '24',
        'points': 3,
        'is_short_answer': False,
        'official_ans_str': '',
        'subject': '기하',
        'title': '[2027학년도 수능 고3 기하 24번] 포물선의 평행이동과 방정식',
        'title_en': '[2027 CSAT Math Geometry #24] Translated Parabola Equation from Vertex and Focus',
        'summary_ko': r'초점이 $(3,0)$이고 꼭짓점이 $(-1,0)$인 포물선이 점 $(0,a)$를 지날 때, 양수 $a$의 값을 구하는 문항입니다.',
        'summary_en': r'A parabola with focus $(3,0)$ and vertex $(-1,0)$ passes through $(0,a)$. Find $a>0$.',
        'tags': ['2027학년도 수능', '기하', '이차곡선', '포물선', '평행이동'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': r'$p$',
                'desc': '꼭짓점에서 초점까지 x축 방향으로 떨어진 부호 있는 거리입니다.',
                'desc_en': 'Directed distance from vertex to focus along the axis of symmetry.',
            },
            {
                'sym': r'$y^2 = 4p(x-x_0)$',
                'desc': r'꼭짓점이 $(x_0, 0)$이고 초점이 $(x_0+p, 0)$인 포물선의 표준형 방정식입니다.',
                'desc_en': r'Standard translated parabola with vertex $(x_0,0)$ and focus $(x_0+p,0)$.',
            },
            {
                'sym': r'준선 $x = x_0 - p$',
                'desc': '포물선 위의 모든 점에서 초점까지의 거리와 같아지는 기준 직선입니다.',
                'desc_en': 'Directrix line symmetric to the focus across the vertex.',
            },
        ],
        'levels': [
            {
                'title': r'🔰 1단계 · [초등 기초 직관] 수직선에서 두 점 사이의 거리 구하기',
                'title_en': r'🔰 Step 1 · [Elementary Intuition] Distance Between Two Points on Number Line',
                'knowledge': r'수직선 위의 점 $-1$에서 출발하여 오른쪽으로 이동해 점 $3$에 도착하려면 몇 칸 이동해야 할지 세어 봅니다.',
                'knowledge_en': r'Count steps from $-1$ rightward to $+3$ on the number line.',
                'questions': [{
                    'level_label': '초등 기초 직관 디딤돌 1',
                    'level_label_en': 'Elementary Intuition Step 1',
                    'stem': r'수직선 위에서 꼭짓점 $-1$부터 초점 $3$까지의 칸 수 $3 - (-1)$은 얼마인가요?',
                    'stem_en': r'On the number line, how many units are between $-1$ and $3$ ($3 - (-1)$)?',
                    'options': [r'$1$', r'$2$', r'$3$', r'$4$', r'$5$'],
                    'answer': 4,
                    'exp': r'$-1$에서 $0$까지 $1$칸, $0$에서 $3$까지 $3$칸이므로 총 $3 - (-1) = 4$칸입니다.',
                    'exp_en': r'$-1 \to 0$ is $1$ step and $0 \to 3$ is $3$ steps, totaling $4$.',
                }],
            },
            {
                'title': r'🌿 2단계 · [기호 번역] $p=4$를 이용해 계수 $4p$ 정하기',
                'title_en': r'🌿 Step 2 · [Formula Coefficient] Determining $4p$',
                'knowledge': r'포물선의 꼭짓점이 $(-1,0)$, 초점이 $(3,0)$이므로 $p = 4$입니다. 따라서 $4p$의 값을 계산할 수 있습니다.',
                'knowledge_en': r'Since $p=4$, compute $4p$ for the equation $y^2 = 4p(x-x_0)$.',
                'questions': [{
                    'level_label': '포물선 계수 디딤돌 2',
                    'level_label_en': 'Parabola Coefficient Step 2',
                    'stem': r'꼭짓점이 $(-1,0)$이고 초점이 $(3,0)$인 포물선 $y^2 = 4p(x+1)$에서 $4p$의 값은?',
                    'stem_en': r'For $p=4$, what is the coefficient $4p$ in $y^2 = 4p(x+1)$?',
                    'options': [r'$4$', r'$8$', r'$12$', r'$16$', r'$20$'],
                    'answer': 4,
                    'exp': r'$p = 4$이므로 $4p = 4 \times 4 = 16$, 즉 포물선의 방정식은 $y^2 = 16(x+1)$입니다.',
                    'exp_en': r'$4p = 4 \times 4 = 16$, giving $y^2 = 16(x+1)$.',
                }],
            },
            {
                'title': r'🌱 3단계 · [좌표 대입] 점 $(0, a)$ 대입하여 $a^2$ 구하기',
                'title_en': r'🌱 Step 3 · [Point Substitution] Plugging in $(0, a)$',
                'knowledge': r'곡선이 점 $(0, a)$를 지나면 식에 $x=0$, $y=a$를 대입했을 때 등식이 성립합니다.',
                'knowledge_en': r'Substitute $x=0$ and $y=a$ into $y^2 = 16(x+1)$.',
                'questions': [{
                    'level_label': '좌표 대입 디딤돌 3',
                    'level_label_en': 'Substitution Step 3',
                    'stem': r'$y^2 = 16(x+1)$에 $x=0$, $y=a$를 대입하여 얻은 $a^2$의 값은?',
                    'stem_en': r'Substituting $(0, a)$ into $y^2 = 16(x+1)$ gives what value for $a^2$?',
                    'options': [r'$4$', r'$8$', r'$12$', r'$16$', r'$32$'],
                    'answer': 4,
                    'exp': r'$a^2 = 16(0+1) = 16 \times 1 = 16$입니다.',
                    'exp_en': r'$a^2 = 16(0+1) = 16$.',
                }],
            },
            {
                'title': r'🌳 4단계 · [기하 검증] 포물선의 정의(초점 거리 = 준선 거리)로 교차검증',
                'title_en': r'🌳 Step 4 · [Geometric Check] Focus-Directrix Definition',
                'knowledge': r'꼭짓점이 $(-1,0)$이고 $p=4$이면 준선은 $x = -1 - 4 = -5$입니다. 따라서 $(0, a)$에서 준선 $x=-5$까지의 거리는 $5$입니다.',
                'knowledge_en': r'The directrix is $x=-1-4=-5$, so the distance from $(0,a)$ to the directrix is $5$.',
                'questions': [{
                    'level_label': '포물선 정의 검증 디딤돌 4',
                    'level_label_en': 'Geometric Definition Step 4',
                    'stem': r'점 $(0, a)$에서 초점 $(3, 0)$까지의 거리가 준선까지 거리 $5$와 같으려면 $3^2 + a^2 = [\;\text{(가)}\;]^2$입니다. $[\;\text{(가)}\;]$는?',
                    'stem_en': r'Equating distances from $(0,a)$ to focus $(3,0)$ and directrix $x=-5$ gives $3^2+a^2=[\;\text{(A)}\;]^2$. What is $[\;\text{(A)}\;]$?',
                    'options': [r'$3$', r'$4$', r'$5$', r'$6$', r'$7$'],
                    'answer': 3,
                    'exp': r'$3^2 + a^2 = 5^2 \implies a^2 = 25 - 9 = 16$으로 동일한 결과를 얻습니다!',
                    'exp_en': r'$3^2+a^2=5^2 \implies a^2=16$, matching completely.',
                }],
            },
            {
                'title': r'💎 5단계 · [최종 종합] 양수 $a$ 확정하기',
                'title_en': r'💎 Step 5 · [Final Synthesis] Determining Positive $a$',
                'knowledge': r'$a^2 = 16$을 만족하는 수 중에서 양수인 값을 찾습니다.',
                'knowledge_en': r'Pick the positive square root of $16$.',
                'questions': [{
                    'level_label': '최종 종합 디딤돌 5',
                    'level_label_en': 'Final Synthesis Step 5',
                    'stem': r'$a^2 = 16$을 만족하는 양수 $a$의 값은?',
                    'stem_en': r'What positive number $a$ satisfies $a^2 = 16$?',
                    'options': [r'$1$', r'$2$', r'$3$', r'$4$', r'$5$'],
                    'answer': 4,
                    'exp': r'$4 \times 4 = 16$이고 $a > 0$이므로 $a = 4$(④번)입니다.',
                    'exp_en': r'Since $a>0$ and $a^2=16$, $a=4$ (choice ④).',
                }],
            },
        ],
        'final': {
            'stem': r'초점의 좌표가 $(3,\;0)$, 꼭짓점의 좌표가 $(-1,\;0)$인 포물선이 점 $(0,\;a)$를 지날 때, 양수 $a$의 값은? [3점]',
            'stem_en': r'When a parabola with focus $(3,\;0)$ and vertex $(-1,\;0)$ passes through $(0,\;a)$, what is the value of the positive constant $a$? [3 points]',
            'options': [r'$1$', r'$2$', r'$3$', r'$4$', r'$5$'],
            'answer': 4,
            'exp': r'꼭짓점이 $(-1,0)$이고 초점이 $(3,0)$이므로 $p = 3 - (-1) = 4$이고 포물선은 $y^2 = 16(x+1)$입니다. $(0,a)$를 대입하면 $a^2 = 16 \implies a=4$($a>0$)입니다.',
            'exp_en': r'With vertex $(-1,0)$ and focus $(3,0)$, $p=4$, so $y^2=16(x+1)$. Substituting $(0,a)$ yields $a^2=16 \implies a=4$.',
            'solution': (
                r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>""" + '\n'
                + r"""<p>본 문항은 꼭짓점과 초점의 위치로부터 <b>평행이동된 포물선의 방정식 $y^2 = 4p(x - x_0)$</b>을 세우거나, <b>포물선의 정의(초점까지 거리 = 준선까지 거리)</b>를 적용하여 미정 좌표를 구하는 기본 문항입니다.</p>""" + '\n'
                + _wrap_visual_svg(
                    "📐 [2027 수능 기하 24번] 꼭짓점 (-1,0) &amp; 초점 (3,0) 포물선과 3:4:5 직각삼각형",
                    "p = 4 ⇒ y² = 16(x+1) ⇒ a = 4",
                    _SVG_G24_INNER,
                    height=258,
                    lang="ko",
                    caption="▲ 꼭짓점 (-1,0)에서 초점 (3,0)까지 거리가 4이므로 준선은 x=-5이고, (0,a)와 준선 사이 거리는 5입니다.",
                )
                + _wrap_schematic_flow(
                    [
                        r"거리 $p = 3 - (-1) = 4$",
                        r"방정식 $y^2 = 16(x+1)$",
                        r"$(0,a)$ 대입: $a^2 = 16$",
                        r"양수 $a = \sqrt{16}$",
                    ],
                    r"$4$ (④)",
                    lang="ko",
                )
                + r"""<h4>📐 [단계별 상세 풀이 전개]</h4>""" + '\n'
                + r"""<p><b>1단계: 평행이동된 포물선의 방정식 구하기</b><br>꼭짓점이 $(-1,\;0)$이고 초점이 $(3,\;0)$으로 모두 $x$축 위에 놓여 있으므로 포물선 $y^2 = 4px$를 $x$축 방향으로 $-1$만큼 평행이동한 형태입니다. $$p = 3 - (-1) = 4 \implies y^2 = 4(4)(x + 1) = 16(x + 1)$$<br><br><b>2단계: 점 $(0, a)$ 대입 (또는 포물선의 정의 직관 검증)</b><br>$x=0,\; y=a$를 대입하면 $a^2 = 16(0+1) = 16$이므로 $a > 0$에서 $a = 4$입니다. (정의로 확인: 준선이 $x = -5$이므로 $\sqrt{3^2+a^2} = 0-(-5) = 5$에서 $3:4:5$ 직각삼각형에 의해 곧바로 $a=4$!)</p>""" + '\n'
                + r"""<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>""" + '\n'
                + r'<p>따라서 양수 $a$의 값은 <b>$4$</b>이므로 정답은 <b>④번</b>입니다. (<a href="https://min7014.github.io/" target="_blank" rel="noopener">수학자료실(min7014.github.io)</a>의 포물선 작도·평행이동 앱렛으로 준선 대칭성을 직접 확인해 보세요.)</p>'
            ),
            'solution_en': (
                r"""<h4>📋 [Problem Analysis &amp; Core Concepts]</h4>""" + '\n'
                + r"""<p>Find $p$ from the vertex and focus to write the translated parabola equation $y^2 = 4p(x-x_0)$ and evaluate at $x=0$.</p>""" + '\n'
                + _wrap_visual_svg(
                    "📐 [2027 CSAT Geometry #24] Translated Parabola y^2 = 16(x+1)",
                    "p = 4 => a = 4",
                    _SVG_G24_INNER,
                    height=258,
                    lang="en",
                    caption="▲ Both equation substitution y^2=16(x+1) and the 3-4-5 right triangle with directrix x=-5 yield a=4.",
                )
                + _wrap_schematic_flow(
                    [
                        r"$p = 3 - (-1) = 4$",
                        r"$y^2 = 16(x+1)$",
                        r"Set $x=0 \implies a^2=16$",
                        r"Positive root $a=4$",
                    ],
                    r"$4$ (④)",
                    lang="en",
                )
                + r"""<h4>📐 [Step-by-Step Rigorous Derivation]</h4>""" + '\n'
                + r"""<p>Since vertex is $(-1,0)$ and focus is $(3,0)$, $p = 3-(-1)=4$, giving $y^2 = 16(x+1)$. Setting $x=0, y=a$ yields $a^2=16$, so $a=4$.</p>""" + '\n'
                + r"""<h4>✨ [Conclusion &amp; Key Takeaways]</h4>""" + '\n'
                + r'<p>Therefore, $a = 4$, which is <b>choice ④</b>.</p>'
            ),
        },
    },

    # =========================================================================
    # 기하 25번 (csat27_g25) — 3점, 정답 3 (8)
    # =========================================================================
    {
        'slug': 'csat27_g25',
        'qNum': '25',
        'points': 3,
        'is_short_answer': False,
        'official_ans_str': '',
        'subject': '기하',
        'title': '[2027학년도 수능 고3 기하 25번] 좌표공간 선분의 내분점과 외분점 조건',
        'title_en': '[2027 CSAT Math Geometry #25] Internal and External Division Points in 3D Space',
        'summary_ko': r'좌표공간에서 두 점 $\mathrm{A}(a,-3,6)$, $\mathrm{B}(-3,b,c)$의 $2:1$ 내분점이 $yz$평면 위에 있고 $3:2$ 외분점이 $x$축 위에 있을 때 $a+b+c$를 구하는 문항입니다.',
        'summary_en': r'In 3D space, the $2:1$ internal division point of $\mathrm{AB}$ lies on the $yz$-plane and the $3:2$ external division point lies on the $x$-axis. Find $a+b+c$.',
        'tags': ['2027학년도 수능', '기하', '공간좌표', '내분점과 외분점'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': r'$yz\text{평면 위}$',
                'desc': 'x좌표가 0인 점 (0, y, z)들의 모임입니다.',
                'desc_en': 'The set of points whose x-coordinate is 0.',
            },
            {
                'sym': r'$x\text{축 위}$',
                'desc': 'y좌표와 z좌표가 모두 0인 점 (x, 0, 0)들의 모임입니다.',
                'desc_en': 'The set of points whose y and z coordinates are both 0.',
            },
            {
                'sym': r'$m:n\text{ 내분 / 외분}$',
                'desc': r'각 좌표마다 $\dfrac{mx_B + nx_A}{m+n}$ (내분), $\dfrac{mx_B - nx_A}{m-n}$ (외분)으로 계산합니다.',
                'desc_en': r'Componentwise weighted average formulas for internal (+) and external (-) division.',
            },
        ],
        'levels': [
            {
                'title': r'🔰 1단계 · [초등 기초 직관] 좌표평면과 공간에서 축·평면 위 점의 특징 알기',
                'title_en': r'🔰 Step 1 · [Elementary Intuition] Zero Coordinates on Planes and Axes',
                'knowledge': r'앞뒤(x), 좌우(y), 높이(z) 중에서 yz평면은 x가 0인 벽이고, x축은 y=0, z=0인 바닥 선입니다.',
                'knowledge_en': r'Points on the yz-plane have x=0; points on the x-axis have both y=0 and z=0.',
                'questions': [{
                    'level_label': '초등 기초 직관 디딤돌 1',
                    'level_label_en': 'Elementary Intuition Step 1',
                    'stem': r'좌표공간에서 어떤 점이 $yz$평면 위에 있을 때 반드시 $0$이 되어야 하는 좌표와, $x$축 위에 있을 때 반드시 $0$이 되어야 하는 좌표들을 바르게 짝지은 것은?',
                    'stem_en': r'Which coordinate(s) must be $0$ for a point on the $yz$-plane and on the $x$-axis, respectively?',
                    'options': [
                        r'$x=0$ / $y=0$만',
                        r'$x=0$ / $y=0,\; z=0$',
                        r'$y=0$ / $x=0,\; z=0$',
                        r'$z=0$ / $x=0,\; y=0$',
                        r'$y=0,\; z=0$ / $x=0$',
                    ],
                    'answer': 2,
                    'exp': r'$yz$평면은 $x=0$이고, $x$축은 $y=0$이면서 $z=0$입니다.',
                    'exp_en': r'$yz$-plane means $x=0$; $x$-axis means $y=0$ and $z=0$.',
                }],
            },
            {
                'title': r'🌿 2단계 · [내분점 식 세우기] $2:1$ 내분점의 $x$좌표 $= 0$으로 $a$ 구하기',
                'title_en': r'🌿 Step 2 · [Internal Division] Finding $a$ from $x=0$',
                'knowledge': r'선분 $\mathrm{AB}$를 $2:1$로 내분하는 점의 $x$좌표는 $\dfrac{2(-3) + 1 \cdot a}{2+1}$입니다.',
                'knowledge_en': r'The $x$-coordinate of the $2:1$ internal division point is $\frac{2(-3)+1\cdot a}{2+1}$.',
                'questions': [{
                    'level_label': '내분점 $a$ 구하기 디딤돌 2',
                    'level_label_en': 'Internal Division Step 2',
                    'stem': r'$\dfrac{2(-3) + a}{3} = 0$에서 $a$의 값은?',
                    'stem_en': r'Solving $\dfrac{2(-3)+a}{3}=0$ gives what value for $a$?',
                    'options': [r'$3$', r'$4$', r'$5$', r'$6$', r'$9$'],
                    'answer': 4,
                    'exp': r'$-6 + a = 0 \implies a = 6$입니다.',
                    'exp_en': r'$-6+a=0 \implies a=6$.',
                }],
            },
            {
                'title': r'🌱 3단계 · [외분점 $y$좌표] $3:2$ 외분점의 $y$좌표 $= 0$으로 $b$ 구하기',
                'title_en': r'🌱 Step 3 · [External Division $y$] Finding $b$ from $y=0$',
                'knowledge': r'선분 $\mathrm{AB}$를 $3:2$로 외분하는 점의 $y$좌표는 $\dfrac{3b - 2(-3)}{3-2}$이며, $x$축 위이므로 $0$입니다.',
                'knowledge_en': r'The $y$-coordinate of the $3:2$ external division point is $\frac{3b-2(-3)}{3-2}=0$.',
                'questions': [{
                    'level_label': '외분점 $b$ 구하기 디딤돌 3',
                    'level_label_en': 'External Division $y$ Step 3',
                    'stem': r'$\dfrac{3b - 2(-3)}{3-2} = 0$에서 $b$의 값은?',
                    'stem_en': r'Solving $\dfrac{3b-2(-3)}{3-2}=0$ yields what value for $b$?',
                    'options': [r'$-3$', r'$-2$', r'$-1$', r'$2$', r'$3$'],
                    'answer': 2,
                    'exp': r'$3b + 6 = 0 \implies 3b = -6 \implies b = -2$입니다.',
                    'exp_en': r'$3b+6=0 \implies b=-2$.',
                }],
            },
            {
                'title': r'🌳 4단계 · [외분점 $z$좌표] $3:2$ 외분점의 $z$좌표 $= 0$으로 $c$ 구하기',
                'title_en': r'🌳 Step 4 · [External Division $z$] Finding $c$ from $z=0$',
                'knowledge': r'선분 $\mathrm{AB}$를 $3:2$로 외분하는 점의 $z$좌표는 $\dfrac{3c - 2(6)}{3-2}$이며, 마찬가지로 $0$입니다.',
                'knowledge_en': r'The $z$-coordinate of the $3:2$ external division point is $\frac{3c-2(6)}{3-2}=0$.',
                'questions': [{
                    'level_label': '외분점 $c$ 구하기 디딤돌 4',
                    'level_label_en': 'External Division $z$ Step 4',
                    'stem': r'$\dfrac{3c - 2(6)}{3-2} = 0$에서 $c$의 값은?',
                    'stem_en': r'Solving $\dfrac{3c-12}{1}=0$ gives what value for $c$?',
                    'options': [r'$2$', r'$3$', r'$4$', r'$6$', r'$8$'],
                    'answer': 3,
                    'exp': r'$3c - 12 = 0 \implies c = 4$입니다.',
                    'exp_en': r'$3c-12=0 \implies c=4$.',
                }],
            },
            {
                'title': r'💎 5단계 · [최종 종합] $a + b + c$의 값 구하기',
                'title_en': r'💎 Step 5 · [Final Synthesis] Computing $a+b+c$',
                'knowledge': r'앞서 구한 $a=6$, $b=-2$, $c=4$를 모두 더합니다.',
                'knowledge_en': r'Sum $a=6$, $b=-2$, and $c=4$.',
                'questions': [{
                    'level_label': '최종 종합 디딤돌 5',
                    'level_label_en': 'Final Synthesis Step 5',
                    'stem': r'$a=6$, $b=-2$, $c=4$일 때, $a + b + c$의 값은?',
                    'stem_en': r'What is $a+b+c$ for $a=6, b=-2, c=4$?',
                    'options': [r'$6$', r'$7$', r'$8$', r'$9$', r'$10$'],
                    'answer': 3,
                    'exp': r'$a+b+c = 6 + (-2) + 4 = 8$이므로 정답은 ③번입니다.',
                    'exp_en': r'$6-2+4=8$ (choice ③).',
                }],
            },
        ],
        'final': {
            'stem': r'좌표공간의 서로 다른 두 점 $\mathrm{A}(a,\;-3,\;6)$, $\mathrm{B}(-3,\;b,\;c)$에 대하여 선분 $\mathrm{AB}$를 $2:1$로 내분하는 점이 $yz$평면 위에 있고, 선분 $\mathrm{AB}$를 $3:2$로 외분하는 점이 $x$축 위에 있을 때, $a+b+c$의 값은? [3점]',
            'stem_en': r'In 3D space, for distinct points $\mathrm{A}(a,-3,6)$ and $\mathrm{B}(-3,b,c)$, the point dividing $\mathrm{AB}$ internally in the ratio $2:1$ lies on the $yz$-plane, and the point dividing $\mathrm{AB}$ externally in the ratio $3:2$ lies on the $x$-axis. Find $a+b+c$. [3 points]',
            'options': [r'$6$', r'$7$', r'$8$', r'$9$', r'$10$'],
            'answer': 3,
            'exp': r'$2:1$ 내분점의 $x$좌표 $\frac{-6+a}{3}=0 \implies a=6$, $3:2$ 외분점의 $y, z$좌표 $\frac{3b+6}{1}=0 \implies b=-2$, $\frac{3c-12}{1}=0 \implies c=4$이므로 $a+b+c = 6-2+4 = 8$입니다.',
            'exp_en': r'From $\frac{-6+a}{3}=0 \implies a=6$, $3b+6=0 \implies b=-2$, and $3c-12=0 \implies c=4$, we obtain $a+b+c=8$.',
            'solution': (
                r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>""" + '\n'
                + r"""<p>본 문항은 좌표공간에서 <b>평면($yz$평면: $x=0$)</b>과 <b>좌표축($x$축: $y=0, z=0$)</b>의 방정식을 정확히 알고, 성분별 <b>내분점·외분점 공식</b>을 적용해 미지수를 독립적으로 분리해 내는 문항입니다.</p>""" + '\n'
                + _wrap_visual_svg(
                    "📐 [2027 수능 기하 25번] 좌표공간 내분점(yz평면) &amp; 외분점(x축) 분해",
                    "a=6, b=-2, c=4 ⇒ 8",
                    _SVG_G25_INNER,
                    height=252,
                    lang="ko",
                    caption="▲ x좌표(내분점=0)에서 a=6이 바로 풀리고, y·z좌표(외분점=0)에서 b=-2, c=4가 독립적으로 결정됩니다.",
                )
                + _wrap_schematic_flow(
                    [
                        r"$2:1$ 내분점 $\in yz$평면 ➔ $x=0$",
                        r"$\frac{-6+a}{3}=0 \implies a=6$",
                        r"$3:2$ 외분점 $\in x$축 ➔ $y=z=0$",
                        r"$b=-2, c=4 \implies a+b+c=8$",
                    ],
                    r"$8$ (③)",
                    lang="ko",
                )
                + r"""<h4>📐 [단계별 상세 풀이 전개]</h4>""" + '\n'
                + r"""<p><b>1단계: $2:1$ 내분점의 $x$좌표 조건</b><br>선분 $\mathrm{AB}$를 $2:1$로 내분하는 점은 $yz$평면($x=0$) 위에 있으므로 $x$좌표가 $0$입니다. $$\frac{2 \cdot (-3) + 1 \cdot a}{2+1} = 0 \implies a - 6 = 0 \implies a = 6$$<br><br><b>2단계: $3:2$ 외분점의 $y, z$좌표 조건</b><br>선분 $\mathrm{AB}$를 $3:2$로 외분하는 점은 $x$축($y=0,\; z=0$) 위에 있으므로 $y, z$좌표가 모두 $0$입니다. $$\frac{3b - 2(-3)}{3-2} = 3b + 6 = 0 \implies b = -2, \qquad \frac{3c - 2(6)}{3-2} = 3c - 12 = 0 \implies c = 4$$</p>""" + '\n'
                + r"""<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>""" + '\n'
                + r'<p>따라서 $a+b+c = 6 + (-2) + 4 = 8$이므로 정답은 <b>③번</b>입니다. (덧셈 실수를 막기 위해 내분점과 외분점 비율의 교차 곱셈 순서 $mB \pm nA$를 꼭 검산하고, <a href="https://min7014.github.io/" target="_blank" rel="noopener">수학자료실(min7014.github.io)</a>의 공간좌표 자료도 함께 살펴보세요.)</p>'
            ),
            'solution_en': (
                r"""<h4>📋 [Problem Analysis &amp; Core Concepts]</h4>""" + '\n'
                + r"""<p>Use $x=0$ on the $yz$-plane for the $2:1$ internal division point and $y=z=0$ on the $x$-axis for the $3:2$ external division point.</p>""" + '\n'
                + _wrap_visual_svg(
                    "📐 [2027 CSAT Geometry #25] Decoupled 3D Division Coordinates",
                    "a=6, b=-2, c=4 => 8",
                    _SVG_G25_INNER,
                    height=252,
                    lang="en",
                    caption="▲ Each coordinate equation decouples cleanly to give a=6, b=-2, and c=4.",
                )
                + _wrap_schematic_flow(
                    [
                        r"Internal $2:1 \in yz$-plane ($x=0$)",
                        r"$(-6+a)/3=0 \implies a=6$",
                        r"External $3:2 \in x$-axis ($y=z=0$)",
                        r"$b=-2, c=4 \implies a+b+c=8$",
                    ],
                    r"$8$ (③)",
                    lang="en",
                )
                + r"""<h4>📐 [Step-by-Step Rigorous Derivation]</h4>""" + '\n'
                + r"""<p>Internal $2:1$ $x$-coord: $\frac{-6+a}{3}=0 \implies a=6$. External $3:2$ $y,z$-coords: $3b+6=0 \implies b=-2$ and $3c-12=0 \implies c=4$. Thus $a+b+c=8$.</p>""" + '\n'
                + r"""<h4>✨ [Conclusion &amp; Key Takeaways]</h4>""" + '\n'
                + r'<p>Therefore, $a+b+c = 8$, which corresponds to <b>choice ③</b>.</p>'
            ),
        },
    },

    # =========================================================================
    # 기하 26번 (csat27_g26) — 3점, 정답 5 (40)
    # =========================================================================
    {
        'slug': 'csat27_g26',
        'qNum': '26',
        'points': 3,
        'is_short_answer': False,
        'official_ans_str': '',
        'subject': '기하',
        'title': '[2027학년도 수능 고3 기하 26번] 타원의 정의와 통경의 성질을 이용한 a²+b² 계산',
        'title_en': '[2027 CSAT Math Geometry #26] Ellipse Definition and Focal Chord (Latus Rectum)',
        'summary_ko': r"""타원 $\frac{x^2}{a^2}+\frac{y^2}{b^2}=1\;(a>b>0)$에서 초점 $\mathrm{F}$를 지나고 $x$축에 수직인 직선이 타원과 만나는 두 점 $\mathrm{P}, \mathrm{Q}$에 대해 $\overline{\mathrm{PQ}}=6,\; \overline{\mathrm{PF}'}=7$일 때 $a^2+b^2$을 구하는 문항입니다.""",
        'summary_en': r"""For ellipse $\frac{x^2}{a^2}+\frac{y^2}{b^2}=1\;(a>b>0)$, a vertical line through focus $\mathrm{F}$ meets the ellipse at $\mathrm{P},\mathrm{Q}$ with $\overline{\mathrm{PQ}}=6$ and $\overline{\mathrm{PF}'}=7$. Find $a^2+b^2$.""",
        'tags': ['2027학년도 수능', '기하', '이차곡선', '타원', '타원의 정의'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': r"""$\overline{\mathrm{PF}}+\overline{\mathrm{PF}'}=2a$""",
                'desc': '타원 위의 모든 점 P에서 두 초점 F, F′까지 거리의 합은 항상 장축의 길이 2a로 일정합니다.',
                'desc_en': 'Sum of distances from any point P on the ellipse to foci F and F′ equals the major axis 2a.',
            },
            {
                'sym': r'$x\text{축 대칭}$',
                'desc': 'x축에 수직인 현 PQ는 x축을 기준으로 위아래 길이가 정확히 반씩 같아 PF = PQ / 2 입니다.',
                'desc_en': 'Symmetry across the x-axis splits vertical focal chord PQ equally: PF = PQ / 2.',
            },
            {
                'sym': r'$c^2 = a^2 - b^2$',
                'desc': '장축 반지름 a, 단축 반지름 b, 초점 거리 c 사이의 피타고라스 관계식입니다.',
                'desc_en': 'Fundamental ellipse relation connecting semi-axes a, b and focal distance c.',
            },
        ],
        'levels': [
            {
                'title': r'🔰 1단계 · [초등 기초 직관] 반으로 똑같이 접어 $\overline{\mathrm{PF}}$ 길이 알기',
                'title_en': r'🔰 Step 1 · [Elementary Intuition] Folding Symmetrically to Find $\overline{\mathrm{PF}}$',
                'knowledge': r'타원은 $x$축을 따라 위아래가 거울처럼 똑같이 생겼으므로, 수직선분 $\overline{\mathrm{PQ}}=6$은 점 $\mathrm{F}$에서 위와 아래로 절반씩 나뉩니다.',
                'knowledge_en': r'Symmetry about the $x$-axis splits segment $\mathrm{PQ}=6$ into two equal halves at $\mathrm{F}$.',
                'questions': [{
                    'level_label': '초등 기초 직관 디딤돌 1',
                    'level_label_en': 'Elementary Intuition Step 1',
                    'stem': r'선분 $\mathrm{PQ}$의 길이가 $6$이고 점 $\mathrm{F}$가 $\mathrm{PQ}$의 정중앙에 있을 때, 선분 $\mathrm{PF}$의 길이는?',
                    'stem_en': r'If $\overline{\mathrm{PQ}}=6$ and $\mathrm{F}$ is its midpoint, what is $\overline{\mathrm{PF}}$?',
                    'options': [r'$1$', r'$2$', r'$3$', r'$4$', r'$6$'],
                    'answer': 3,
                    'exp': r'$6 \div 2 = 3$이므로 $\overline{\mathrm{PF}} = 3$입니다.',
                    'exp_en': r'$\overline{\mathrm{PF}} = 6 / 2 = 3$.',
                }],
            },
            {
                'title': r'🌿 2단계 · [타원의 정의] 두 초점까지의 거리 합으로 장축 $2a$ 구하기',
                'title_en': r'🌿 Step 2 · [Ellipse Definition] Finding Major Axis $2a$',
                'knowledge': r"""타원 위의 점 $\mathrm{P}$에 대하여 두 초점 $\mathrm{F}, \mathrm{F}'$까지의 거리의 합 $\overline{\mathrm{PF}} + \overline{\mathrm{PF}'}$는 항상 $2a$와 같습니다.""",
                'knowledge_en': r"""By definition of the ellipse, $\overline{\mathrm{PF}} + \overline{\mathrm{PF}'} = 2a$.""",
                'questions': [{
                    'level_label': '장축 길이 $a$ 구하기 디딤돌 2',
                    'level_label_en': 'Semi-Major Axis Step 2',
                    'stem': r"""$\overline{\mathrm{PF}} = 3$, $\overline{\mathrm{PF}'} = 7$일 때, $2a = 3 + 7$로부터 구한 $a$의 값은?""",
                    'stem_en': r"""From $2a = \overline{\mathrm{PF}} + \overline{\mathrm{PF}'} = 3 + 7$, what is $a$?""",
                    'options': [r'$3$', r'$4$', r'$5$', r'$6$', r'$10$'],
                    'answer': 3,
                    'exp': r'$2a = 10$이므로 $a = 5$이고, $a^2 = 25$입니다.',
                    'exp_en': r'$2a = 10 \implies a = 5$ (and $a^2 = 25$).',
                }],
            },
            {
                'title': r"""🌱 3단계 · [직각삼각형 활용] $\triangle\mathrm{PF}'\mathrm{F}$에서 초점 거리 $2c$ 구하기""",
                'title_en': r'🌱 Step 3 · [Pythagorean Step] Focal Separation $2c$',
                'knowledge': r"""$\overline{\mathrm{PQ}} \perp x\text{축}$이므로 $\angle\mathrm{PFF}' = 90^\circ$입니다! 빗변이 $7$, 높이가 $3$인 직각삼각형에서 밑변 $\overline{\mathrm{FF}'} = 2c$를 구할 수 있습니다.""",
                'knowledge_en': r"""Since $\angle\mathrm{PFF}'=90^\circ$, apply Pythagoras to right triangle $\mathrm{PF}'\mathrm{F}$.""",
                'questions': [{
                    'level_label': '직각삼각형 $c^2$ 디딤돌 3',
                    'level_label_en': 'Right Triangle Step 3',
                    'stem': r"""직각삼각형 $\mathrm{PF}'\mathrm{F}$에서 $(2c)^2 = 7^2 - 3^2 = 40$일 때, $c^2$의 값은?""",
                    'stem_en': r'From $(2c)^2 = 7^2 - 3^2 = 40$, what is $c^2$?',
                    'options': [r'$8$', r'$10$', r'$12$', r'$16$', r'$20$'],
                    'answer': 2,
                    'exp': r'$4c^2 = 49 - 9 = 40$이므로 $c^2 = 10$입니다.',
                    'exp_en': r'$4c^2 = 40 \implies c^2 = 10$.',
                }],
            },
            {
                'title': r'🌳 4단계 · [$b^2$ 도출] $c^2 = a^2 - b^2$ (또는 통경 $\frac{b^2}{a}=3$)로 $b^2$ 구하기',
                'title_en': r'🌳 Step 4 · [Finding $b^2$] Via $b^2 = a^2 - c^2$ or $\frac{b^2}{a}=3$',
                'knowledge': r'$a^2 = 25$이고 $c^2 = 10$이므로 $b^2 = a^2 - c^2$로 구할 수 있으며, 또는 $\mathrm{P}(c, 3)$을 타원 식에 넣으면 바로 $\frac{b^2}{a}=3$을 얻습니다.',
                'knowledge_en': r'Either $b^2 = a^2 - c^2$ or the semi-latus rectum $\frac{b^2}{a}=3$ gives $b^2$.',
                'questions': [{
                    'level_label': '$b^2$ 계산 디딤돌 4',
                    'level_label_en': 'Computing $b^2$ Step 4',
                    'stem': r'$a^2 = 25$, $c^2 = 10$일 때, $b^2 = a^2 - c^2$의 값은?',
                    'stem_en': r'Given $a^2 = 25$ and $c^2 = 10$, what is $b^2 = a^2 - c^2$?',
                    'options': [r'$10$', r'$12$', r'$14$', r'$15$', r'$16$'],
                    'answer': 4,
                    'exp': r'$b^2 = 25 - 10 = 15$입니다. (확인: $\frac{b^2}{a} = \frac{15}{5} = 3 = \overline{\mathrm{PF}}$ 일치!)',
                    'exp_en': r'$b^2 = 25 - 10 = 15$ (matching $b^2/a = 15/5 = 3$).',
                }],
            },
            {
                'title': r'💎 5단계 · [최종 종합] $a^2 + b^2$ 계산 완료하기',
                'title_en': r'💎 Step 5 · [Final Synthesis] Computing $a^2 + b^2$',
                'knowledge': r'앞서 구한 $a^2 = 25$와 $b^2 = 15$를 더합니다.',
                'knowledge_en': r'Sum $a^2 = 25$ and $b^2 = 15$.',
                'questions': [{
                    'level_label': '최종 종합 디딤돌 5',
                    'level_label_en': 'Final Synthesis Step 5',
                    'stem': r'$a^2 = 25$, $b^2 = 15$일 때, $a^2 + b^2$의 값은?',
                    'stem_en': r'What is $a^2 + b^2$ when $a^2 = 25$ and $b^2 = 15$?',
                    'options': [r'$32$', r'$34$', r'$36$', r'$38$', r'$40$'],
                    'answer': 5,
                    'exp': r'$25 + 15 = 40$이므로 정답은 ⑤번입니다.',
                    'exp_en': r'$25+15=40$ (choice ⑤).',
                }],
            },
        ],
        'final': {
            'stem': r"""두 초점이 $\mathrm{F}$, $\mathrm{F}'$인 타원 $\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}=1\;(a>b>0)$이 있다. 점 $\mathrm{F}$를 지나고 $x$축에 수직인 직선이 이 타원과 만나는 두 점을 $\mathrm{P}$, $\mathrm{Q}$라 하자. $\overline{\mathrm{PQ}}=6$, $\overline{\mathrm{PF}'}=7$일 때, $a^2+b^2$의 값은? [3점]""",
            'stem_en': r"""Consider the ellipse $\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}=1\;(a>b>0)$ with foci $\mathrm{F}$ and $\mathrm{F}'$. A line through $\mathrm{F}$ perpendicular to the $x$-axis intersects the ellipse at $\mathrm{P}$ and $\mathrm{Q}$. If $\overline{\mathrm{PQ}}=6$ and $\overline{\mathrm{PF}'}=7$, find $a^2+b^2$. [3 points]""",
            'options': [r'$32$', r'$34$', r'$36$', r'$38$', r'$40$'],
            'answer': 5,
            'exp': r'$x$축 대칭으로 $\overline{\mathrm{PF}}=3$이고 타원의 정의에서 $2a = 3+7 = 10 \implies a=5$입니다. 또한 $\overline{\mathrm{PF}}=\frac{b^2}{a}=3$이므로 $b^2=15$이며, 따라서 $a^2+b^2=25+15=40$입니다.',
            'exp_en': r'By symmetry $\overline{\mathrm{PF}}=3$, so $2a=3+7=10 \implies a=5$. Also $b^2/a = 3 \implies b^2=15$, hence $a^2+b^2=25+15=40$.',
            'solution': (
                r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>""" + '\n'
                + r"""<p>본 문항은 타원의 <b>$x$축 대칭성</b>, <b>거리 합 일정의 정의($\overline{\mathrm{PF}}+\overline{\mathrm{PF}'}=2a$)</b>, 그리고 <b>초점 통경의 반길이 $\overline{\mathrm{PF}}=\frac{b^2}{a}$</b> (또는 직각삼각형 $\mathrm{PF}'\mathrm{F}$)를 결합하여 $a^2+b^2$을 구하는 전형적·핵심 기하 문항입니다.</p>""" + '\n'
                + _wrap_visual_svg(
                    "📐 [2027 수능 기하 26번] 타원 대칭성 + 거리 합 2a=10 + 직각삼각형 F′FP",
                    "a²=25, b²=15 ⇒ 40",
                    _SVG_G26_INNER,
                    height=262,
                    lang="ko",
                    caption="▲ x축 대칭으로 PF = 3을 얻고, 타원의 정의 3+7=2a로 a=5, 직각삼각형(또는 통경 b²/a=3)으로 b²=15를 구합니다.",
                )
                + _wrap_schematic_flow(
                    [
                        r"$x$축 대칭 ➔ $\overline{\mathrm{PF}}=\frac{6}{2}=3$",
                        r"타원 정의: $2a = 3 + 7 = 10 \implies a=5$",
                        r"통경 $\frac{b^2}{a}=3$ (또는 $c^2=10$)",
                        r"$b^2=15 \implies a^2+b^2=40$",
                    ],
                    r"$40$ (⑤)",
                    lang="ko",
                )
                + r"""<h4>📐 [단계별 상세 풀이 전개]</h4>""" + '\n'
                + r"""<p><b>1단계: 타원의 대칭성과 정의로 $a$ 구하기</b><br>선분 $\mathrm{PQ}$는 초점 $\mathrm{F}$를 지나며 $x$축에 수직이므로, 타원의 $x$축 대칭성에 의해 $\overline{\mathrm{PF}} = \frac{1}{2}\overline{\mathrm{PQ}} = 3$입니다. 타원의 정의에 따라 $2a = \overline{\mathrm{PF}} + \overline{\mathrm{PF}'} = 3 + 7 = 10$이므로 $a = 5$, 즉 $a^2 = 25$입니다.<br><br><b>2단계: $b^2$ 계산 (통경 공식 또는 피타고라스 정리)</b><br>직각삼각형 $\mathrm{PF}'\mathrm{F}$에서 $(2c)^2 = 7^2 - 3^2 = 40 \implies c^2 = 10$이므로 $b^2 = a^2 - c^2 = 25 - 10 = 15$입니다. (또는 점 $\mathrm{P}(c, 3)$을 타원 방정식에 대입하면 $\frac{c^2}{a^2}+\frac{9}{b^2}=1 \implies b^2 = 3a = 15$로 즉시 구할 수 있습니다.)</p>""" + '\n'
                + r"""<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>""" + '\n'
                + r'<p>따라서 $a^2 + b^2 = 25 + 15 = 40$이므로 정답은 <b>⑤번</b>입니다. (실전 팁: 초점을 지나는 수직 현의 반길이 $\frac{b^2}{a}$는 수능 빈출 구조이므로 <a href="https://min7014.github.io/" target="_blank" rel="noopener">수학자료실(min7014.github.io)</a>의 타원 통경 시각 자료와 함께 익혀 두면 매우 빠릅니다.)</p>'
            ),
            'solution_en': (
                r"""<h4>📋 [Problem Analysis &amp; Core Concepts]</h4>""" + '\n'
                + r"""<p>Combine $x$-axis symmetry ($\overline{\mathrm{PF}}=3$), the ellipse focal-sum definition ($2a = 3+7$), and either the Pythagorean relation $b^2=a^2-c^2$ or the semi-latus rectum $b^2/a=3$.</p>""" + '\n'
                + _wrap_visual_svg(
                    "📐 [2027 CSAT Geometry #26] Focal Chord &amp; Ellipse Symmetry",
                    "a^2 + b^2 = 25 + 15 = 40",
                    _SVG_G26_INNER,
                    height=262,
                    lang="en",
                    caption="▲ Half the vertical focal chord gives PF=3; then 2a=3+7 gives a=5 and right triangle F′FP gives b^2=15.",
                )
                + _wrap_schematic_flow(
                    [
                        r"Symmetry: $\overline{\mathrm{PF}} = 6/2 = 3$",
                        r"$2a = 3 + 7 = 10 \implies a = 5$",
                        r"$(2c)^2 = 7^2-3^2 \implies c^2 = 10$",
                        r"$b^2 = 25-10=15 \implies 40$",
                    ],
                    r"$40$ (⑤)",
                    lang="en",
                )
                + r"""<h4>📐 [Step-by-Step Rigorous Derivation]</h4>""" + '\n'
                + r"""<p>$\overline{\mathrm{PF}} = \overline{\mathrm{PQ}}/2 = 3$. Then $2a = \overline{\mathrm{PF}}+\overline{\mathrm{PF}'} = 3+7 = 10 \implies a=5, a^2=25$. Using $(2c)^2 = 7^2-3^2 = 40 \implies c^2=10$, we get $b^2 = 25-10 = 15$, so $a^2+b^2 = 40$.</p>""" + '\n'
                + r"""<h4>✨ [Conclusion &amp; Key Takeaways]</h4>""" + '\n'
                + r'<p>Hence $a^2+b^2 = 40$, which matches <b>choice ⑤</b>.</p>'
            ),
        },
    },
    # =========================================================================
    # 기하 27번 (csat27_g27) — 3점, 정답 1 (14√3)
    # =========================================================================
    {
        'slug': 'csat27_g27',
        'qNum': '27',
        'points': 3,
        'is_short_answer': False,
        'official_ans_str': '',
        'subject': '기하',
        'title': '[2027학년도 수능 고3 기하 27번] 정육각기둥에서 삼수선의 정리를 이용한 삼각형 넓이',
        'title_en': '[2027 CSAT Math Geometry #27] Triangle Area in a Hexagonal Prism via Three Perpendiculars Theorem',
        'summary_ko': r'한 변의 길이가 $4$인 정육각형을 밑면으로 하고 높이가 $2\sqrt{6}$인 육각기둥 $\mathrm{ABCDEF-GHIJKL}$에서 선분 $\mathrm{EF}$의 중점 $\mathrm{M}$에 대하여 삼각형 $\mathrm{MGI}$의 넓이를 구하는 문항입니다.',
        'summary_en': r'In a right regular hexagonal prism $\mathrm{ABCDEF-GHIJKL}$ of base edge $4$ and height $2\sqrt{6}$, let $\mathrm{M}$ be the midpoint of $\mathrm{EF}$. Find the area of triangle $\mathrm{MGI}$.',
        'tags': ['2027학년도 수능', '기하', '공간도형', '삼수선의 정리', '정육각기둥'],
        'orig_svg': ORIG_SVG_G27,
        'symbols': [
            {
                'sym': r"""$\mathrm{M}'$""",
                'desc': r'윗면 변 $\mathrm{EF}$의 중점 $\mathrm{M}$에서 아랫면 $\mathrm{GHIJKL}$로 수직으로 내린 수선의 발(변 $\mathrm{KL}$의 중점)입니다.',
                'desc_en': r'Orthogonal projection of midpoint $\mathrm{M}$ of $\mathrm{EF}$ onto the bottom hexagon (midpoint of $\mathrm{KL}$).',
            },
            {
                'sym': r'$\overline{\mathrm{GI}}$',
                'desc': r'한 변의 길이가 $4$인 정육각형에서 한 꼭짓점($\mathrm{H}$)을 건너뛴 대각선의 길이 $4\sqrt{3}$입니다.',
                'desc_en': r'Short diagonal of the regular hexagon of side $4$, equal to $4\sqrt{3}$.',
            },
            {
                'sym': r'$\overline{\mathrm{MN}} \perp \overline{\mathrm{GI}}$',
                'desc': r"""삼수선의 정리: $\overline{\mathrm{MM}'}\perp\text{밑면}$이고 $\overline{\mathrm{M}'\mathrm{N}}\perp\overline{\mathrm{GI}}$이면 공간의 빗변 $\overline{\mathrm{MN}}$도 $\overline{\mathrm{GI}}$에 수직이 됩니다.""",
                'desc_en': r"""Three Perpendiculars Theorem: $\overline{\mathrm{MM}'}\perp\text{base}$ and $\overline{\mathrm{M}'\mathrm{N}}\perp\overline{\mathrm{GI}} \implies \overline{\mathrm{MN}}\perp\overline{\mathrm{GI}}$.""",
            },
        ],
        'levels': [
            {
                'title': r'🔰 1단계 · [초등 기초 직관] 기둥의 윗면 중점을 바닥으로 그대로 내리기',
                'title_en': r'🔰 Step 1 · [Elementary Intuition] Dropping Midpoint Vertically to Bottom Face',
                'knowledge': r"""사각기둥이나 육각기둥처럼 옆면이 수직으로 서 있는 기둥에서 윗면 변 $\mathrm{EF}$의 중점 $\mathrm{M}$을 바닥으로 수직 낙하시키면 아랫면에서 $\mathrm{EF}$와 마주 보는 변 $\mathrm{KL}$의 중점 $\mathrm{M}'$에 닿습니다.""",
                'knowledge_en': r"""Dropping midpoint $\mathrm{M}$ of top edge $\mathrm{EF}$ straight down hits midpoint $\mathrm{M}'$ of bottom edge $\mathrm{KL}$, with vertical drop equal to height $2\sqrt{6}$.""",
                'questions': [{
                    'level_label': '초등 기초 직관 디딤돌 1',
                    'level_label_en': 'Elementary Intuition Step 1',
                    'stem': r"""육각기둥 $\mathrm{ABCDEF-GHIJKL}$에서 윗면 변 $\mathrm{EF}$의 중점 $\mathrm{M}$을 아랫면에 정사영시킨 점 $\mathrm{M}'$의 위치는?""",
                    'stem_en': r'Where does midpoint $\mathrm{M}$ of $\mathrm{EF}$ project orthogonally onto the bottom hexagon $\mathrm{GHIJKL}$?',
                    'options': [
                        r'변 $\mathrm{GH}$의 중점',
                        r'변 $\mathrm{HI}$의 중점',
                        r'변 $\mathrm{IJ}$의 중점',
                        r'변 $\mathrm{JK}$의 중점',
                        r'변 $\mathrm{KL}$의 중점',
                    ],
                    'answer': 5,
                    'exp': r"""옆모서리 $\mathrm{EK}, \mathrm{FL}$이 밑면에 수직이므로 $\mathrm{EF}$의 중점 $\mathrm{M}$은 밑면의 변 $\mathrm{KL}$의 중점 $\mathrm{M}'$ 위로 내려옵니다.""",
                    'exp_en': r'Because lateral edges $\mathrm{EK},\mathrm{FL}$ are vertical, $\mathrm{M}$ projects to the midpoint of $\mathrm{KL}$.',
                }],
            },
            {
                'title': r'🌿 2단계 · [밑변 길이] 정육각형의 대각선 $\overline{\mathrm{GI}}$ 길이 구하기',
                'title_en': r'🌿 Step 2 · [Base Side] Computing Diagonal $\overline{\mathrm{GI}}$',
                'knowledge': r'밑면 정육각형 $\mathrm{GHIJKL}$의 한 변의 길이는 $4$이고 한 내각 $\angle\mathrm{GHI}=120^\circ$입니다. 이등변삼각형 $\mathrm{GHI}$의 밑변 길이는 $1:1:\sqrt{3}$ 비율을 가집니다.',
                'knowledge_en': r'In isosceles triangle $\mathrm{GHI}$ ($4, 4, 120^\circ$), the base has length $4\sqrt{3}$.',
                'questions': [{
                    'level_label': '정육각형 대각선 길이 디딤돌 2',
                    'level_label_en': 'Hexagon Diagonal Step 2',
                    'stem': r'한 변의 길이가 $4$인 정육각형 $\mathrm{GHIJKL}$에서 선분 $\mathrm{GI}$의 길이는?',
                    'stem_en': r'In a regular hexagon $\mathrm{GHIJKL}$ of side length $4$, what is $\overline{\mathrm{GI}}$?',
                    'options': [r'$4$', r'$2\sqrt{6}$', r'$4\sqrt{3}$', r'$6$', r'$8$'],
                    'answer': 3,
                    'exp': r'$\angle\mathrm{GHI}=120^\circ$인 이등변삼각형에서 $\overline{\mathrm{GI}} = 2 \times 4\cos 30^\circ = 4\sqrt{3}$입니다.',
                    'exp_en': r'$\overline{\mathrm{GI}} = 4\sqrt{3}$.',
                }],
            },
            {
                'title': r"""🌱 3단계 · [바닥 거리] 밑면에서 점 $\mathrm{M}'$과 직선 $\mathrm{GI}$ 사이 거리 구하기""",
                'title_en': r"""🌱 Step 3 · [Base Distance] Distance from $\mathrm{M}'$ to Line $\mathrm{GI}$""",
                'knowledge': r"""정육각형에서 대변 $\mathrm{HI}$와 $\mathrm{KL}$ 사이의 평행 거리는 $4\sqrt{3}$이고, 중심에서 $\mathrm{KL}$까지가 $2\sqrt{3}$, 중심에서 $\mathrm{GI}$까지 거리(방향 $\overrightarrow{\mathrm{OH}}$)는 $4 \cdot \frac{\sqrt{3}}{2}$가 아닌 변 $\mathrm{JK}\perp\mathrm{GI}$ 방향 사다리꼴 높이를 씁니다! 변 $\mathrm{GL}$의 정삼각형 높이가 $2\sqrt{3}$일 때, $\mathrm{G}(4,0), \mathrm{I}(-2,2\sqrt{3}), \mathrm{M}'(0,-2\sqrt{3})$를 쓰거나 대칭축 $\mathrm{HJ}$ 방향($\mathrm{HK}$가 아닌 $\mathrm{H}$–중심–$\mathrm{K}$ 길이 $8$)으로 따집니다. 중심 $\mathrm{O}$에서 대각선 $\mathrm{GI}$까지 거리는 $2$? 잠깐: $\angle\mathrm{HGI}=30^\circ$, 정삼각형 $6$개의 높이 $h_0=2\sqrt{3}$과 구분해 정사영하면 $\overline{\mathrm{M}'\mathrm{N}} = 5$입니다!""",
                'knowledge_en': r"""Decomposing the regular hexagon along the altitude perpendicular to $\mathrm{GI}$ shows $d(\mathrm{M}', \mathrm{GI}) = 5$.""",
                'questions': [{
                    'level_label': '바닥 수선 길이 디딤돌 3',
                    'level_label_en': 'Base Perpendicular Step 3',
                    'stem': r"""한 변의 길이가 $4$인 정육각형 $\mathrm{GHIJKL}$에서 변 $\mathrm{KL}$의 중점 $\mathrm{M}'$과 직선 $\mathrm{GI}$ 사이의 거리 $\overline{\mathrm{M}'\mathrm{N}}$은? (힌트: 중심 $\mathrm{O}$에서 $\mathrm{GI}$까지 거리는 $2$? 아니요, $\mathrm{G}(4,0)$, $\mathrm{I}(-2, 2\sqrt{3})$, $\mathrm{M}'(0, -2\sqrt{3})$에서 직선 $\mathrm{GI}: x+\sqrt{3}y=4$까지 거리를 계산하거나 사다리꼴로 분할해 보세요!)""",
                    'stem_en': r"""In regular hexagon $\mathrm{GHIJKL}$ of side $4$, what is the perpendicular distance $\overline{\mathrm{M}'\mathrm{N}}$ from midpoint $\mathrm{M}'$ of $\mathrm{KL}$ to line $\mathrm{GI}$?""",
                    'options': [r'$3$', r'$4$', r'$5$', r'$2\sqrt{3}$', r'$4\sqrt{3}$'],
                    'answer': 3,
                    'exp': r"""중심 $\mathrm{O}(0,0)$, $\mathrm{G}(4,0)$, $\mathrm{I}(-2,2\sqrt{3})$에서 직선 $\mathrm{GI}$는 $x+\sqrt{3}y-4=0$입니다. 점 $\mathrm{M}'(0, -2\sqrt{3})$까지 거리는 $\frac{|0+\sqrt{3}(-2\sqrt{3})-4|}{\sqrt{1+3}} = \frac{10}{2} = 5$입니다!""",
                    'exp_en': r"""Using coordinates with center $(0,0)$, $\mathrm{M}'(0,-2\sqrt{3})$ and line $\mathrm{GI}: x+\sqrt{3}y-4=0$, distance is $|-6-4|/2 = 5$.""",
                }],
            },
            {
                'title': r'🌳 4단계 · [삼수선의 정리] $\triangle\mathrm{MGI}$의 실제 높이 $\overline{\mathrm{MN}}$ 구하기',
                'title_en': r'🌳 Step 4 · [Three Perpendiculars] Slant Height $\overline{\mathrm{MN}}$',
                'knowledge': r"""직각삼각형 $\mathrm{MM}'\mathrm{N}$에서 높이 $\overline{\mathrm{MM}'}=2\sqrt{6}$, 바닥 변 $\overline{\mathrm{M}'\mathrm{N}}=5$이므로 피타고라스 정리로 빗변 $\overline{\mathrm{MN}}$을 구합니다.""",
                'knowledge_en': r"""In right triangle $\mathrm{MM}'\mathrm{N}$, $\overline{\mathrm{MN}} = \sqrt{\overline{\mathrm{MM}'}^2 + \overline{\mathrm{M}'\mathrm{N}}^2}$.""",
                'questions': [{
                    'level_label': '삼수선 높이 구하기 디딤돌 4',
                    'level_label_en': 'Slant Height Step 4',
                    'stem': r"""$\overline{\mathrm{MM}'}=2\sqrt{6}$, $\overline{\mathrm{M}'\mathrm{N}}=5$일 때, 삼각형 $\mathrm{MGI}$의 높이 $\overline{\mathrm{MN}}$은?""",
                    'stem_en': r"""Given $\overline{\mathrm{MM}'}=2\sqrt{6}$ and $\overline{\mathrm{M}'\mathrm{N}}=5$, what is height $\overline{\mathrm{MN}}$ of $\triangle\mathrm{MGI}$?""",
                    'options': [r'$6$', r'$\sqrt{41}$', r'$7$', r'$5\sqrt{2}$', r'$8$'],
                    'answer': 3,
                    'exp': r'$\overline{\mathrm{MN}} = \sqrt{(2\sqrt{6})^2 + 5^2} = \sqrt{24 + 25} = \sqrt{49} = 7$입니다!',
                    'exp_en': r'$\overline{\mathrm{MN}} = \sqrt{24 + 25} = \sqrt{49} = 7$.',
                }],
            },
            {
                'title': r'💎 5단계 · [최종 종합] $\triangle\mathrm{MGI}$의 넓이 계산하기',
                'title_en': r'💎 Step 5 · [Final Synthesis] Area of $\triangle\mathrm{MGI}$',
                'knowledge': r'밑변 $\overline{\mathrm{GI}}=4\sqrt{3}$, 높이 $\overline{\mathrm{MN}}=7$인 삼각형의 넓이를 구합니다.',
                'knowledge_en': r'Compute $\frac{1}{2} \times \overline{\mathrm{GI}} \times \overline{\mathrm{MN}}$.',
                'questions': [{
                    'level_label': '최종 종합 디딤돌 5',
                    'level_label_en': 'Final Synthesis Step 5',
                    'stem': r'밑변 $\overline{\mathrm{GI}}=4\sqrt{3}$, 높이 $\overline{\mathrm{MN}}=7$일 때, $\triangle\mathrm{MGI}$의 넓이는?',
                    'stem_en': r'With base $4\sqrt{3}$ and height $7$, what is $\mathrm{Area}(\triangle\mathrm{MGI})$?',
                    'options': [
                        r'$14\sqrt{3}$',
                        r'$\dfrac{29\sqrt{3}}{2}$',
                        r'$15\sqrt{3}$',
                        r'$\dfrac{31\sqrt{3}}{2}$',
                        r'$16\sqrt{3}$',
                    ],
                    'answer': 1,
                    'exp': r'$\frac{1}{2} \times 4\sqrt{3} \times 7 = 14\sqrt{3}$이므로 정답은 ①번입니다.',
                    'exp_en': r'$\frac{1}{2} \cdot 4\sqrt{3} \cdot 7 = 14\sqrt{3}$ (choice ①).',
                }],
            },
        ],
        'final': {
            'stem': r'그림과 같이 한 변의 길이가 $4$인 정육각형을 밑면으로 하고 높이가 $2\sqrt{6}$인 육각기둥 $\mathrm{ABCDEF-GHIJKL}$이 있다. 선분 $\mathrm{EF}$의 중점 $\mathrm{M}$에 대하여 삼각형 $\mathrm{MGI}$의 넓이는? [3점]',
            'stem_en': r'As shown in the figure, a hexagonal prism $\mathrm{ABCDEF-GHIJKL}$ has a regular hexagon of side length $4$ as its base and height $2\sqrt{6}$. If $\mathrm{M}$ is the midpoint of $\mathrm{EF}$, what is the area of triangle $\mathrm{MGI}$? [3 points]',
            'options': [
                r'$14\sqrt{3}$',
                r'$\dfrac{29\sqrt{3}}{2}$',
                r'$15\sqrt{3}$',
                r'$\dfrac{31\sqrt{3}}{2}$',
                r'$16\sqrt{3}$',
            ],
            'answer': 1,
            'exp': r"""점 $\mathrm{M}$의 밑면 정사영 $\mathrm{M}'$은 변 $\mathrm{KL}$의 중점이고, 정육각형에서 $\overline{\mathrm{GI}}=4\sqrt{3}$이며 점 $\mathrm{M}'$에서 직선 $\mathrm{GI}$까지의 거리는 $5$입니다. 삼수선의 정리에 의해 높이 $\overline{\mathrm{MN}}=\sqrt{(2\sqrt{6})^2+5^2}=7$이므로 넓이는 $\frac{1}{2}\cdot 4\sqrt{3}\cdot 7 = 14\sqrt{3}$입니다.""",
            'exp_en': r"""$\mathrm{M}$ projects to the midpoint $\mathrm{M}'$ of $\mathrm{KL}$. On the base hexagon, $\overline{\mathrm{GI}}=4\sqrt{3}$ and $d(\mathrm{M}',\mathrm{GI})=5$, so by the Three Perpendiculars Theorem the slant height is $\sqrt{24+25}=7$, yielding area $14\sqrt{3}$.""",
            'solution': (
                r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>""" + '\n'
                + r"""<p>본 문항은 정육각기둥 위 비스듬히 놓인 삼각형 $\mathrm{MGI}$의 넓이를 구하기 위해, 윗면의 중점 $\mathrm{M}$을 밑면으로 정사영한 뒤 <b>삼수선의 정리(수직 높이 + 밑면 수선 ➔ 빗변 수선)</b>를 적용하는 핵심 공간도형 문항입니다.</p>""" + '\n'
                + _wrap_visual_svg(
                    "📐 [2027 수능 기하 27번] 밑면 정육각형 거리 M′N=5 + 삼수선 직각삼각형",
                    "넓이 = (1/2) × 4√3 × 7 = 14√3",
                    _SVG_G27_INNER,
                    height=268,
                    lang="ko",
                    caption="▲ 밑면 GHIJKL에서 GI=4√3, KL 중점 M′에서 직선 GI까지 거리 M′N=5를 먼저 구한 뒤 높이 2√6과 피타고라스로 결합하면 빗변 높이 7이 깔끔한 정수로 떨어집니다.",
                )
                + _wrap_schematic_flow(
                    [
                        r"$\mathrm{M}$ 정사영 $\mathrm{M}'$ ($\mathrm{KL}$ 중점)",
                        r"밑면 $\overline{\mathrm{GI}} = 4\sqrt{3}$",
                        r"수선 $\overline{\mathrm{M}'\mathrm{N}} = 5$",
                        r"삼수선 $\overline{\mathrm{MN}}=7 \implies 14\sqrt{3}$",
                    ],
                    r"$14\sqrt{3}$ (①)",
                    lang="ko",
                )
                + r"""<h4>📐 [단계별 상세 풀이 전개]</h4>""" + '\n'
                + r"""<p><b>1단계: 정사영 $\mathrm{M}'$ 설정 및 밑변 $\overline{\mathrm{GI}}$ 구하기</b><br>육각기둥의 옆모서리가 밑면에 수직이므로 $\mathrm{EF}$의 중점 $\mathrm{M}$에서 밑면 $\mathrm{GHIJKL}$에 내린 수선의 발 $\mathrm{M}'$은 변 $\mathrm{KL}$의 중점입니다. 또한 $\angle\mathrm{GHI}=120^\circ$인 이등변삼각형 $\mathrm{GHI}$($\overline{\mathrm{GH}}=\overline{\mathrm{HI}}=4$)에서 $\overline{\mathrm{GI}} = 4\sqrt{3}$입니다.<br><br><b>2단계: 밑면 거리 $\overline{\mathrm{M}'\mathrm{N}}$과 삼수선의 정리 적용</b><br>밑면 정육각형의 중심 $\mathrm{O}$를 원점으로 두고 $\mathrm{G}(4,0)$, $\mathrm{H}(2, 2\sqrt{3})$, $\mathrm{I}(-2, 2\sqrt{3})$, $\mathrm{K}(-2, -2\sqrt{3})$, $\mathrm{L}(2, -2\sqrt{3})$이라 잡으면 $\mathrm{M}'=(0, -2\sqrt{3})$이고 직선 $\mathrm{GI}$의 방정식은 $x+\sqrt{3}y-4=0$입니다.<br>점 $\mathrm{M}'$에서 직선 $\mathrm{GI}$에 내린 수선의 발을 $\mathrm{N}$이라 하면 $$\overline{\mathrm{M}'\mathrm{N}} = \frac{|0 + \sqrt{3}(-2\sqrt{3}) - 4|}{\sqrt{1^2 + (\sqrt{3})^2}} = \frac{10}{2} = 5$$ 삼수선의 정리에 의해 $\overline{\mathrm{MN}} \perp \overline{\mathrm{GI}}$이므로 직각삼각형 $\mathrm{MM}'\mathrm{N}$에서 삼각형 $\mathrm{MGI}$의 높이는 $$\overline{\mathrm{MN}} = \sqrt{\overline{\mathrm{MM}'}^2 + \overline{\mathrm{M}'\mathrm{N}}^2} = \sqrt{(2\sqrt{6})^2 + 5^2} = \sqrt{24 + 25} = 7$$</p>""" + '\n'
                + r"""<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>""" + '\n'
                + r'<p>따라서 $\triangle\mathrm{MGI}$의 넓이는 $\frac{1}{2} \times 4\sqrt{3} \times 7 = 14\sqrt{3}$이므로 정답은 <b>①번</b>입니다. (<a href="https://min7014.github.io/" target="_blank" rel="noopener">수학자료실(min7014.github.io)</a>의 삼수선의 정리 3D 인터랙티브 자료도 함께 탐구해 보세요.)</p>'
            ),
            'solution_en': (
                r"""<h4>📋 [Problem Analysis &amp; Core Concepts]</h4>""" + '\n'
                + r"""<p>Project $\mathrm{M}$ vertically to midpoint $\mathrm{M}'$ of $\mathrm{KL}$, find $d(\mathrm{M}',\mathrm{GI})$ on the base hexagon, and apply the Three Perpendiculars Theorem.</p>""" + '\n'
                + _wrap_visual_svg(
                    "📐 [2027 CSAT Geometry #27] Hexagonal Base Projection &amp; Three Perpendiculars",
                    "Area = (1/2) * 4√3 * 7 = 14√3",
                    _SVG_G27_INNER,
                    height=268,
                    lang="en",
                    caption="▲ Computing base distance M′N = 5 and height MM′ = 2√6 yields an exact integer slant height MN = 7.",
                )
                + _wrap_schematic_flow(
                    [
                        r"Project $\mathrm{M} \to \mathrm{M}'$ (mid $\mathrm{KL}$)",
                        r"Base chord $\overline{\mathrm{GI}}=4\sqrt{3}$",
                        r"Base altitude $d(\mathrm{M}',\mathrm{GI})=5$",
                        r"Height $\sqrt{24+25}=7 \implies 14\sqrt{3}$",
                    ],
                    r"$14\sqrt{3}$ (①)",
                    lang="en",
                )
                + r"""<h4>📐 [Step-by-Step Rigorous Derivation]</h4>""" + '\n'
                + r"""<p>With base hexagon vertices at radius $4$, $\overline{\mathrm{GI}} = 4\sqrt{3}$ and $d(\mathrm{M}',\mathrm{GI}) = 5$. By the Three Perpendiculars Theorem, slant height $\overline{\mathrm{MN}} = \sqrt{(2\sqrt{6})^2+5^2} = 7$. Thus $\mathrm{Area}(\triangle\mathrm{MGI}) = \frac{1}{2}(4\sqrt{3})(7) = 14\sqrt{3}$.</p>""" + '\n'
                + r"""<h4>✨ [Conclusion &amp; Key Takeaways]</h4>""" + '\n'
                + r'<p>Hence the area is <b>$14\sqrt{3}$</b>, which matches <b>choice ①</b>.</p>'
            ),
        },
    },

    # =========================================================================
    # 기하 28번 (csat27_g28) — 4점, 정답 4 (196/5)
    # =========================================================================
    {
        'slug': 'csat27_g28',
        'qNum': '28',
        'points': 4,
        'is_short_answer': False,
        'official_ans_str': '',
        'subject': '기하',
        'title': '[2027학년도 수능 고3 기하 28번] 평면벡터의 자취(평행사변형 영역)와 내적의 최대·최소',
        'title_en': '[2027 CSAT Math Geometry #28] Locus of Vector Sum and Extrema of Dot Product',
        'summary_ko': r'$\overline{\mathrm{OA}}=2\sqrt{2},\; \overline{\mathrm{OB}}=\overline{\mathrm{AB}}=2$인 직각삼각형 $\mathrm{OAB}$에서 선분 $\mathrm{OA}, \mathrm{OB}$ 위의 동점 $\mathrm{P}, \mathrm{Q}$와 조건 (가), (나)를 만족시키는 점 $\mathrm{R}$에 대하여 $\overrightarrow{\mathrm{OR}}\cdot\overrightarrow{\mathrm{BR}}$의 최댓값 $M$과 최솟값 $m$의 합을 구하는 문항입니다.',
        'summary_en': r'In right triangle $\mathrm{OAB}$ ($\overline{\mathrm{OA}}=2\sqrt{2}, \overline{\mathrm{OB}}=\overline{\mathrm{AB}}=2$), $\mathrm{P}\in\overline{\mathrm{OA}}, \mathrm{Q}\in\overline{\mathrm{OB}}$ and point $\mathrm{R}$ satisfy conditions (가) and (나). Find $M+m$ for $\overrightarrow{\mathrm{OR}}\cdot\overrightarrow{\mathrm{BR}}$.',
        'tags': ['2027학년도 수능', '기하', '평면벡터', '벡터의 자취', '벡터의 내적'],
        'orig_svg': '',
        'symbols': [
            {
                'sym': r'$\overrightarrow{\mathrm{OR}} = 2\overrightarrow{\mathrm{OP}} - \overrightarrow{\mathrm{OQ}}$',
                'desc': r'$2\overrightarrow{\mathrm{OP}}$ 자취(길이 $4\sqrt{2}$ 선분)와 $-\overrightarrow{\mathrm{OQ}}$ 자취(길이 $2$ 선분)의 결합으로 점 $\mathrm{R}$의 평행사변형 영역이 결정됩니다.',
                'desc_en': r'Sum of segments traced by $2t\overrightarrow{\mathrm{OA}}$ and $-s\overrightarrow{\mathrm{OB}}$ produces a parallelogram region for $\mathrm{R}$.',
            },
            {
                'sym': r'$\overrightarrow{\mathrm{OR}}\cdot\overrightarrow{\mathrm{BR}}$',
                'desc': r'$\overline{\mathrm{OB}}$의 중점 $\mathrm{M}(1,0)$을 이용하면 $|\overrightarrow{\mathrm{MR}}|^2 - 1$로 바뀌어 거리 제곱의 최대·최소 문제로 번역됩니다!',
                'desc_en': r'Rewrites via midpoint $\mathrm{M}(1,0)$ of $\mathrm{OB}$ as $|\overrightarrow{\mathrm{MR}}|^2 - 1$.',
            },
            {
                'sym': r'$x + 2y \ge 10$',
                'desc': r'조건 (나) $2\overrightarrow{\mathrm{OA}}\cdot\overrightarrow{\mathrm{BR}}-\overrightarrow{\mathrm{OB}}\cdot\overrightarrow{\mathrm{AR}}\ge 16$을 좌표화하여 얻는 직선 경계 부등식입니다.',
                'desc_en': r'Half-plane constraint derived from condition (나).',
            },
        ],
        'levels': [
            {
                'title': r'🔰 1단계 · [초등 기초 직관] 세 변의 길이가 $2, 2, 2\sqrt{2}$인 삼각형 모양 알아보기',
                'title_en': r'🔰 Step 1 · [Elementary Intuition] Identifying the Right Isosceles Triangle',
                'knowledge': r'$2^2 + 2^2 = 4 + 4 = 8 = (2\sqrt{2})^2$이므로 $\triangle\mathrm{OAB}$는 직각이등변삼각형이며, 가장 긴 빗변 $\mathrm{OA}$ 맞은편인 꼭짓점 $\mathrm{B}$가 직각($90^\circ$)입니다.',
                'knowledge_en': r'$2^2+2^2=(2\sqrt{2})^2$ shows $\triangle\mathrm{OAB}$ is a $45^\circ$-$45^\circ$-$90^\circ$ triangle with $\angle\mathrm{B}=90^\circ$.',
                'questions': [{
                    'level_label': '초등 기초 직관 디딤돌 1',
                    'level_label_en': 'Elementary Intuition Step 1',
                    'stem': r'직각삼각형 $\mathrm{OAB}$를 좌표평면에 놓을 때 $\mathrm{O}(0,0)$, $\mathrm{B}(2,0)$으로 잡으면 제$1$사분면 위 점 $\mathrm{A}$의 좌표로 가장 알맞은 것은?',
                    'stem_en': r'Placing $\mathrm{O}(0,0)$ and $\mathrm{B}(2,0)$ in the first quadrant, what is the cleanest coordinate choice for $\mathrm{A}$?',
                    'options': [r'$(0,\; 2)$', r'$(2,\; 2)$', r'$(2,\; 2\sqrt{2})$', r'$(\sqrt{2},\; \sqrt{2})$', r'$(4,\; 2)$'],
                    'answer': 2,
                    'exp': r'$\overline{\mathrm{OB}}=2$이고 $\angle\mathrm{OBA}=90^\circ$, $\overline{\mathrm{BA}}=2$이므로 $\mathrm{A}(2,\;2)$로 두면 $\overline{\mathrm{OA}}=\sqrt{2^2+2^2}=2\sqrt{2}$가 완벽히 성립합니다!',
                    'exp_en': r'With $\mathrm{B}(2,0)$ and $\angle\mathrm{B}=90^\circ$, $\mathrm{A}=(2,2)$ satisfies all edge lengths cleanly.',
                }],
            },
            {
                'title': r'🌿 2단계 · [조건 (가) 해석] 점 $\mathrm{R}(x,y)$가 존재하는 평행사변형 영역 구하기',
                'title_en': r'🌿 Step 2 · [Condition (가)] Determining the Parallelogram Domain of $\mathrm{R}$',
                'knowledge': r'$\overrightarrow{\mathrm{OP}} = t(2,2)\;(0\le t\le 1)$, $\overrightarrow{\mathrm{OQ}} = s(2,0)\;(0\le s\le 1)$로 놓으면 $\overrightarrow{\mathrm{OR}} = (4t-2s,\; 4t)$입니다.',
                'knowledge_en': r'Writing $\overrightarrow{\mathrm{OP}}=t(2,2)$ and $\overrightarrow{\mathrm{OQ}}=s(2,0)$ gives $\mathrm{R}(4t-2s, 4t)$.',
                'questions': [{
                    'level_label': '벡터 자취 영역 디딤돌 2',
                    'level_label_en': 'Vector Locus Step 2',
                    'stem': r'$\mathrm{R}(x,y)=(4t-2s,\; 4t)$ ($0\le t\le 1,\; 0\le s\le 1$)에서 $y$와 $x$가 만족하는 범위는?',
                    'stem_en': r'For $(x,y)=(4t-2s, 4t)$ with $t,s\in[0,1]$, which inequalities characterize $(x,y)$?',
                    'options': [
                        r'$0 \le y \le 2,\; y-2 \le x \le y$',
                        r'$0 \le y \le 4,\; y-2 \le x \le y$',
                        r'$0 \le y \le 4,\; y \le x \le y+2$',
                        r'$0 \le x \le 4,\; 0 \le y \le 4$',
                        r'$0 \le y \le 2\sqrt{2},\; -2 \le x \le 4$',
                    ],
                    'answer': 2,
                    'exp': r'$y = 4t \in [0, 4]$이고, $x = y - 2s$에서 $0 \le 2s \le 2$이므로 $y - 2 \le x \le y$입니다.',
                    'exp_en': r'Since $y=4t\in[0,4]$ and $0\le 2s\le 2$, we get $y-2 \le x \le y$.',
                }],
            },
            {
                'title': r'🌱 3단계 · [조건 (나) 해석] 내적 부등식을 직선 반평면으로 정리하기',
                'title_en': r'🌱 Step 3 · [Condition (나)] Linearizing the Dot Product Inequality',
                'knowledge': r'$\overrightarrow{\mathrm{OA}}=(2,2)$, $\overrightarrow{\mathrm{OB}}=(2,0)$, $\overrightarrow{\mathrm{BR}}=(x-2,y)$, $\overrightarrow{\mathrm{AR}}=(x-2,y-2)$를 대입해 계산합니다.',
                'knowledge_en': r'Expand $2(2,2)\cdot(x-2,y) - (2,0)\cdot(x-2,y-2) \ge 16$.',
                'questions': [{
                    'level_label': '내적 부등식 정리 디딤돌 3',
                    'level_label_en': 'Inequality Expansion Step 3',
                    'stem': r'조건 (나) $2\overrightarrow{\mathrm{OA}}\cdot\overrightarrow{\mathrm{BR}} - \overrightarrow{\mathrm{OB}}\cdot\overrightarrow{\mathrm{AR}} \ge 16$을 좌표 $(x,y)$로 간단히 한 식은?',
                    'stem_en': r'Simplifying condition (나) in coordinates $(x,y)$ yields which linear inequality?',
                    'options': [
                        r'$x + y \ge 5$',
                        r'$x + 2y \ge 8$',
                        r'$x + 2y \ge 10$',
                        r'$2x + y \ge 10$',
                        r'$x + 2y \le 10$',
                    ],
                    'answer': 3,
                    'exp': r'$4(x-2)+4y - 2(x-2) = 2(x-2)+4y = 2x+4y-4 \ge 16 \iff 2x+4y \ge 20 \iff x+2y \ge 10$입니다.',
                    'exp_en': r'$2x+4y-4 \ge 16 \iff x+2y \ge 10$.',
                }],
            },
            {
                'title': r'🌳 4단계 · [최댓값 & 최솟값 원리] $\overrightarrow{\mathrm{OR}}\cdot\overrightarrow{\mathrm{BR}} = (x-1)^2+y^2-1$ 해석',
                'title_en': r'🌳 Step 4 · [Distance Squared] Rewriting $\overrightarrow{\mathrm{OR}}\cdot\overrightarrow{\mathrm{BR}}$',
                'knowledge': r'구하는 값 $\overrightarrow{\mathrm{OR}}\cdot\overrightarrow{\mathrm{BR}} = x(x-2)+y^2 = (x-1)^2+y^2-1$은 점 $\mathrm{R}(x,y)$에서 기준점 $\mathrm{M}(1,0)$까지 거리의 제곱에서 $1$을 뺀 값입니다! 영역 $\{0\le y\le 4,\; y-2\le x\le y,\; x+2y\ge 10\}$의 맨 위 오른쪽 꼭짓점 $(4,4)$에서 최대, 경계선 $x+2y=10$ 위로 내린 수선의 발에서 최소가 됩니다.',
                'knowledge_en': r'Distance from $(1,0)$ is maximized at top-right corner $(4,4)$ and minimized at the foot of the perpendicular onto $x+2y=10$.',
                'questions': [{
                    'level_label': '거리 제곱 최대·최소 디딤돌 4',
                    'level_label_en': 'Distance Extrema Step 4',
                    'stem': r'점 $(1,0)$에서 직선 $x + 2y - 10 = 0$까지의 거리 $d$를 구해 최솟값 $m = d^2 - 1$을 계산하면? (수선의 발 $(\frac{14}{5}, \frac{18}{5})$는 $y-2\le x\le y$ 영역 안에 포함됩니다.)',
                    'stem_en': r'What is $m = d^2 - 1$, where $d$ is the distance from $(1,0)$ to line $x+2y-10=0$?',
                    'options': [r'$\dfrac{71}{5}$', r'$\dfrac{74}{5}$', r'$\dfrac{76}{5}$', r'$16$', r'$\dfrac{81}{5}$'],
                    'answer': 3,
                    'exp': r'$d = \frac{|1+0-10|}{\sqrt{1^2+2^2}} = \frac{9}{\sqrt{5}}$이므로 $d^2 = \frac{81}{5}$이고, 따라서 $m = \frac{81}{5} - 1 = \frac{76}{5}$입니다.',
                    'exp_en': r'$d = 9/\sqrt{5} \implies d^2 = 81/5 \implies m = 81/5 - 1 = 76/5$.',
                }],
            },
            {
                'title': r'💎 5단계 · [최종 종합] 최댓값 $M=24$와 최솟값 $m=\frac{76}{5}$ 더하기',
                'title_en': r'💎 Step 5 · [Final Synthesis] Adding $M=24$ and $m=\frac{76}{5}$',
                'knowledge': r'점 $(4,4)$에서 $(4-1)^2+4^2-1 = 9+16-1 = 24$이므로 $M=24$이고, $m=\frac{76}{5}$와 더합니다.',
                'knowledge_en': r'At $(4,4)$, $M = 3^2+4^2-1 = 24$. Add $m = 76/5$.',
                'questions': [{
                    'level_label': '최종 종합 디딤돌 5',
                    'level_label_en': 'Final Synthesis Step 5',
                    'stem': r'$M = 24$, $m = \dfrac{76}{5}$일 때, $M + m$의 값은?',
                    'stem_en': r'What is $M + m$ when $M=24$ and $m=\frac{76}{5}$?',
                    'options': [
                        r'$\dfrac{193}{5}$',
                        r'$\dfrac{194}{5}$',
                        r'$39$',
                        r'$\dfrac{196}{5}$',
                        r'$\dfrac{197}{5}$',
                    ],
                    'answer': 4,
                    'exp': r'$M + m = \frac{120}{5} + \frac{76}{5} = \frac{196}{5}$이므로 정답은 ④번입니다.',
                    'exp_en': r'$24 + 76/5 = 196/5$ (choice ④).',
                }],
            },
        ],
        'final': {
            'stem': r'좌표평면에 $\overline{\mathrm{OA}}=2\sqrt{2}$, $\overline{\mathrm{OB}}=\overline{\mathrm{AB}}=2$인 직각삼각형 $\mathrm{OAB}$가 있다. 선분 $\mathrm{OA}$ 위를 움직이는 점 $\mathrm{P}$와 선분 $\mathrm{OB}$ 위를 움직이는 점 $\mathrm{Q}$에 대하여 점 $\mathrm{R}$이 다음 조건을 만족시킨다.<br><br>(가) $2\overrightarrow{\mathrm{OP}}=\overrightarrow{\mathrm{OQ}}+\overrightarrow{\mathrm{OR}}$<br>(나) $2\overrightarrow{\mathrm{OA}}\cdot\overrightarrow{\mathrm{BR}}-\overrightarrow{\mathrm{OB}}\cdot\overrightarrow{\mathrm{AR}}\ge 16$<br><br>$\overrightarrow{\mathrm{OR}}\cdot\overrightarrow{\mathrm{BR}}$의 최댓값과 최솟값을 각각 $M$, $m$이라 할 때, $M+m$의 값은? [4점]',
            'stem_en': r'In the coordinate plane, $\mathrm{OAB}$ is a right triangle with $\overline{\mathrm{OA}}=2\sqrt{2}$ and $\overline{\mathrm{OB}}=\overline{\mathrm{AB}}=2$. For points $\mathrm{P}\in\overline{\mathrm{OA}}$ and $\mathrm{Q}\in\overline{\mathrm{OB}}$, point $\mathrm{R}$ satisfies: (가) $2\overrightarrow{\mathrm{OP}}=\overrightarrow{\mathrm{OQ}}+\overrightarrow{\mathrm{OR}}$; (나) $2\overrightarrow{\mathrm{OA}}\cdot\overrightarrow{\mathrm{BR}}-\overrightarrow{\mathrm{OB}}\cdot\overrightarrow{\mathrm{AR}}\ge 16$. If $M$ and $m$ are the maximum and minimum values of $\overrightarrow{\mathrm{OR}}\cdot\overrightarrow{\mathrm{BR}}$, find $M+m$. [4 points]',
            'options': [
                r'$\dfrac{193}{5}$',
                r'$\dfrac{194}{5}$',
                r'$39$',
                r'$\dfrac{196}{5}$',
                r'$\dfrac{197}{5}$',
            ],
            'answer': 4,
            'exp': r'$\mathrm{O}(0,0), \mathrm{B}(2,0), \mathrm{A}(2,2)$로 두면 (가)에서 $\mathrm{R}(x,y)$는 $0\le y\le 4,\; y-2\le x\le y$ 위를 움직이고 (나)는 $x+2y\ge 10$이 됩니다. $\overrightarrow{\mathrm{OR}}\cdot\overrightarrow{\mathrm{BR}}=(x-1)^2+y^2-1$은 $(4,4)$에서 최댓값 $M=24$, $(1,0)$에서 $x+2y=10$에 내린 수선의 발 $(\frac{14}{5},\frac{18}{5})$에서 최솟값 $m=\frac{81}{5}-1=\frac{76}{5}$를 가지므로 $M+m=\frac{196}{5}$입니다.',
            'exp_en': r'Setting $\mathrm{O}(0,0), \mathrm{B}(2,0), \mathrm{A}(2,2)$, condition (가) gives $0\le y\le 4,\; y-2\le x\le y$, and condition (나) gives $x+2y\ge 10$. Optimizing $(x-1)^2+y^2-1$ yields $M=24$ at $(4,4)$ and $m=\frac{81}{5}-1=\frac{76}{5}$ at $(\frac{14}{5},\frac{18}{5})$, summing to $\frac{196}{5}$.',
            'solution': (
                r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>""" + '\n'
                + r"""<p>본 문항은 벡터 관계식으로 주어진 <b>평행사변형 영역(자취)</b>과 <b>내적 일차부등식 반평면</b>의 교집합 위에서, 또 다른 내적 $\overrightarrow{\mathrm{OR}}\cdot\overrightarrow{\mathrm{BR}}$을 <b>한 고정점 $\mathrm{M}(1,0)$으로부터의 거리 제곱 $- 1$</b>로 환원해 최대·최소를 구하는 고난도 핵심 문항입니다.</p>""" + '\n'
                + _wrap_visual_svg(
                    "📐 [2027 수능 기하 28번] 평행사변형 영역 ∩ 반평면(x+2y≥10)과 거리² 최적해",
                    "M = 24, m = 76/5 ⇒ 196/5",
                    _SVG_G28_INNER,
                    height=268,
                    lang="ko",
                    caption="▲ 직각삼각형 OAB를 좌표화하면 R의 영역이 직관적 사다리꼴/삼각형 조각(초록색)으로 드러나며, 중심 (1,0)에서 가장 먼 꼭짓점 (4,4)와 가장 가까운 수선의 발 (14/5, 18/5)이 즉시 보입니다.",
                )
                + _wrap_schematic_flow(
                    [
                        r"좌표 설정 $\mathrm{O}(0,0),\mathrm{B}(2,0),\mathrm{A}(2,2)$",
                        r"(가) $0\le y\le 4,\; y-2\le x\le y$",
                        r"(나) 반평면 $x + 2y \ge 10$",
                        r"$(4,4) \to M=24$, 수선 $\to m=\frac{76}{5}$",
                    ],
                    r"$\dfrac{196}{5}$ (④)",
                    lang="ko",
                )
                + r"""<h4>📐 [단계별 상세 풀이 전개]</h4>""" + '\n'
                + r"""<p><b>1단계: 좌표 설정 및 조건 (가), (나) 번역</b><br>$\overline{\mathrm{OB}}^2+\overline{\mathrm{AB}}^2 = 2^2+2^2 = 8 = \overline{\mathrm{OA}}^2$이므로 $\angle\mathrm{B}=90^\circ$입니다. 좌표평면에 $\mathrm{O}(0,0)$, $\mathrm{B}(2,0)$, $\mathrm{A}(2,2)$를 잡습니다.<br>선분 $\mathrm{OA}, \mathrm{OB}$ 위의 동점을 $\overrightarrow{\mathrm{OP}}=t(2,2)$, $\overrightarrow{\mathrm{OQ}}=s(2,0)\;(0\le t,s\le 1)$이라 하면 (가)에 의해 $\overrightarrow{\mathrm{OR}} = 2\overrightarrow{\mathrm{OP}}-\overrightarrow{\mathrm{OQ}} = (4t-2s,\; 4t)$이므로 점 $\mathrm{R}(x,y)$의 범위는 $$0 \le y \le 4, \qquad y - 2 \le x \le y$$ 또한 $\overrightarrow{\mathrm{BR}}=(x-2, y)$, $\overrightarrow{\mathrm{AR}}=(x-2, y-2)$를 조건 (나)에 대입하면 $$2(2,2)\cdot(x-2,y) - (2,0)\cdot(x-2,y-2) = 2(x-2)+4y \ge 16 \iff x + 2y \ge 10$$<br><br><b>2단계: $\overrightarrow{\mathrm{OR}}\cdot\overrightarrow{\mathrm{BR}}$의 최댓값 $M$과 최솟값 $m$</b><br>$\overrightarrow{\mathrm{OR}}\cdot\overrightarrow{\mathrm{BR}} = x(x-2)+y^2 = (x-1)^2 + y^2 - 1$이므로 중심 $\mathrm{M}(1,0)$으로부터의 거리 제곱에서 $1$을 뺀 값입니다.<br>① <b>최댓값 $M$</b>: 영역 $\{0\le y\le 4,\; y-2\le x\le y,\; x+2y\ge 10\}$의 꼭짓점은 $(2,4), (4,4), (\frac{10}{3}, \frac{10}{3})$입니다. $\mathrm{M}(1,0)$에서 가장 먼 점은 $(4,4)$이므로 $$M = (4-1)^2 + 4^2 - 1 = 9 + 16 - 1 = 24$$ ② <b>최솟값 $m$</b>: $\mathrm{M}(1,0)$에서 경계선 $x+2y=10$에 내린 수선의 발을 구하면 $(1,0)+\lambda(1,2)$를 대입해 $5\lambda=9 \implies \lambda=\frac{9}{5}$, 즉 $(\frac{14}{5}, \frac{18}{5}) = (2.8, 3.6)$입니다. 이때 $y-2 = 1.6 \le 2.8 \le 3.6 = y$이므로 이 수선의 발이 영역 안에 실제로 존재합니다! 따라서 $$m = d^2 - 1 = \left(\frac{|1+0-10|}{\sqrt{5}}\right)^2 - 1 = \frac{81}{5} - 1 = \frac{76}{5}$$</p>""" + '\n'
                + r"""<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>""" + '\n'
                + r'<p>그러므로 $M + m = 24 + \frac{76}{5} = \frac{196}{5}$이고 정답은 <b>④번</b>입니다. (수선의 발이 선분 경계 내부에 포함되는지 확인하는 과정이 핵심! <a href="https://min7014.github.io/" target="_blank" rel="noopener">수학자료실(min7014.github.io)</a>의 벡터 내적과 원 영역 자료도 함께 학습해 보세요.)</p>'
            ),
            'solution_en': (
                r"""<h4>📋 [Problem Analysis &amp; Core Concepts]</h4>""" + '\n'
                + r"""<p>Translate conditions (가) and (나) into a region in the plane and rewrite $\overrightarrow{\mathrm{OR}}\cdot\overrightarrow{\mathrm{BR}}$ as squared distance from $(1,0)$ minus $1$.</p>""" + '\n'
                + _wrap_visual_svg(
                    "📐 [2027 CSAT Geometry #28] Locus Region &amp; Distance Extrema",
                    "M = 24, m = 76/5 => 196/5",
                    _SVG_G28_INNER,
                    height=268,
                    lang="en",
                    caption="▲ Optimizing (x-1)^2+y^2-1 over {0<=y<=4, y-2<=x<=y, x+2y>=10} gives M=24 at (4,4) and m=76/5 at (14/5, 18/5).",
                )
                + _wrap_schematic_flow(
                    [
                        r"Coords: $\mathrm{O}(0,0), \mathrm{B}(2,0), \mathrm{A}(2,2)$",
                        r"(가) $0\le y\le 4,\; y-2\le x\le y$",
                        r"(나) $x + 2y \ge 10$",
                        r"$M=24,\; m=\frac{76}{5} \implies \frac{196}{5}$",
                    ],
                    r"$\dfrac{196}{5}$ (④)",
                    lang="en",
                )
                + r"""<h4>📐 [Step-by-Step Rigorous Derivation]</h4>""" + '\n'
                + r"""<p>Placing $\mathrm{O}(0,0), \mathrm{B}(2,0), \mathrm{A}(2,2)$ gives $0\le y\le 4,\; y-2\le x\le y$ and $x+2y\ge 10$. The target equals $(x-1)^2+y^2-1$. Maximum $M = (4-1)^2+4^2-1 = 24$ occurs at $(4,4)$. The foot from $(1,0)$ onto $x+2y=10$ is $(14/5, 18/5)$, which lies inside $y-2\le x\le y$, yielding $m = 81/5 - 1 = 76/5$. Summing gives $24 + 76/5 = 196/5$.</p>""" + '\n'
                + r"""<h4>✨ [Conclusion &amp; Key Takeaways]</h4>""" + '\n'
                + r'<p>Therefore, $M+m = \frac{196}{5}$, which matches <b>choice ④</b>.</p>'
            ),
        },
    },

    # =========================================================================
    # 기하 29번 (csat27_g29) — 4점 단답형, 정답 45
    # =========================================================================
    {
        'slug': 'csat27_g29',
        'qNum': '29',
        'points': 4,
        'is_short_answer': True,
        'official_ans_str': '45',
        'subject': '기하',
        'title': '[2027학년도 수능 고3 기하 29번] 포물선과 쌍곡선의 정의 및 점근선 거리를 이용한 삼각형 둘레',
        'title_en': '[2027 CSAT Math Geometry #29] Combined Parabola & Hyperbola Definitions and Asymptote Distance',
        'summary_ko': r'포물선 $y^2=4px\;(p>0)$ 위의 점 $\mathrm{A}$에서 준선에 내린 수선의 발 $\mathrm{B}$와 초점 $\mathrm{F}$에 대해, 두 초점이 $\mathrm{A}, \mathrm{B}$이고 $\mathrm{F}$를 지나는 쌍곡선의 꼭짓점 $\mathrm{C}$와 양수 기울기 점근선 $l$이 $8\overline{\mathrm{BC}}=\overline{\mathrm{BF}}$, $d(\mathrm{F},l)=15$를 만족시킬 때 $\triangle\mathrm{ABF}$의 둘레를 구하는 주관식 문항입니다.',
        'summary_en': r'Point $\mathrm{A}$ lies on parabola $y^2=4px$ with focus $\mathrm{F}$ and projection $\mathrm{B}$ on the directrix. A hyperbola with foci $\mathrm{A}, \mathrm{B}$ passing through $\mathrm{F}$ has vertex $\mathrm{C}$ near $\mathrm{B}$ and positive-slope asymptote $l$. If $8\overline{\mathrm{BC}}=\overline{\mathrm{BF}}$ and $d(\mathrm{F},l)=15$ with $\overline{\mathrm{AF}}<2p$, find the perimeter of $\triangle\mathrm{ABF}$.',
        'tags': ['2027학년도 수능', '기하', '이차곡선', '포물선', '쌍곡선', '점근선', '주관식 단답형'],
        'orig_svg': ORIG_SVG_G29,
        'symbols': [
            {
                'sym': r'$\overline{\mathrm{AB}} = \overline{\mathrm{AF}} = k$',
                'desc': '포물선의 정의에 의해 점 A에서 초점 F까지의 거리와 준선 위 수선의 발 B까지의 거리는 항상 같아 △ABF는 이등변삼각형이 됩니다.',
                'desc_en': 'By parabola definition, AB = AF = k, making triangle ABF isosceles.',
            },
            {
                'sym': r"""$2a' = \overline{\mathrm{BF}} - \overline{\mathrm{AF}}$""",
                'desc': '두 초점이 A, B이고 F를 지나는 쌍곡선의 정의에 의해 두 거리의 차가 주축의 길이 2a′가 됩니다.',
                'desc_en': 'Hyperbola focal-difference property gives transverse axis length 2a′.',
            },
            {
                'sym': r"""$\text{기울기 } \dfrac{b'}{a'}$""",
                'desc': r'쌍곡선 중심 $\mathrm{M}$(선분 $\mathrm{AB}$의 중점)을 지나고 기울기가 양수인 점근선 $l$의 기울기입니다.',
                'desc_en': r'Slope b′/a′ of the positive-slope asymptote passing through midpoint M of AB.',
            },
        ],
        'levels': [
            {
                'title': r'🔰 1단계 · [초등 기초 직관] 포물선으로 이등변삼각형 $\triangle\mathrm{ABF}$ 변 같음 찾기',
                'title_en': r'🔰 Step 1 · [Elementary Intuition] Recognizing the Isosceles Triangle from Parabola',
                'knowledge': r'포물선 위의 점 $\mathrm{A}$는 초점 $\mathrm{F}$까지의 거리와 준선($\mathrm{B}$)까지의 거리가 언제나 똑같습니다. 따라서 $\overline{\mathrm{AB}} = \overline{\mathrm{AF}}$입니다.',
                'knowledge_en': r'Every point $\mathrm{A}$ on a parabola is equidistant from focus $\mathrm{F}$ and directrix foot $\mathrm{B}$, so $\overline{\mathrm{AB}}=\overline{\mathrm{AF}}$.',
                'questions': [{
                    'level_label': '초등 기초 직관 디딤돌 1',
                    'level_label_en': 'Elementary Intuition Step 1',
                    'stem': r'점 $\mathrm{A}$가 포물선 $y^2=4px$ 위의 점이고 $\mathrm{B}$가 준선에 내린 수선의 발일 때, $\overline{\mathrm{AB}} = \overline{\mathrm{AF}} = k$라 두면 성립하는 것은?',
                    'stem_en': r'Because $\mathrm{A}$ lies on the parabola with focus $\mathrm{F}$ and directrix foot $\mathrm{B}$, which geometric relation always holds?',
                    'options': [
                        r'$\overline{\mathrm{AB}} = \overline{\mathrm{BF}}$',
                        r'$\overline{\mathrm{AB}} = \overline{\mathrm{AF}}$',
                        r'$\overline{\mathrm{AF}} = \overline{\mathrm{BF}}$',
                        r'$\overline{\mathrm{AC}} = \overline{\mathrm{BF}}$',
                        r'$\overline{\mathrm{BC}} = \overline{\mathrm{AF}}$',
                    ],
                    'answer': 2,
                    'exp': r'포물선의 정의 그 자체로 $\overline{\mathrm{AB}} = \overline{\mathrm{AF}} = k$가 성립합니다.',
                    'exp_en': r'By the focus-directrix definition of a parabola, $\overline{\mathrm{AB}} = \overline{\mathrm{AF}} = k$.',
                }],
            },
            {
                'title': r'🌿 2단계 · [쌍곡선 정의 연결] $8\overline{\mathrm{BC}} = \overline{\mathrm{BF}}$로 세 변의 황금 비율 찾기',
                'title_en': r'🌿 Step 2 · [Hyperbola Ratio] Determining the Exact $5:5:8$ Side Ratios',
                'knowledge': r"""두 초점이 $\mathrm{A}, \mathrm{B}$($2c' = k$)이고 꼭짓점이 $\mathrm{C}$인 쌍곡선의 주축 길이는 $2a' = \overline{\mathrm{BF}} - k$입니다 ($\overline{\mathrm{AF}} < 2p$이므로 $\overline{\mathrm{BF}} > \overline{\mathrm{AF}}$). 따라서 $\overline{\mathrm{BC}} = c' - a' = \frac{k}{2} - \frac{\overline{\mathrm{BF}}-k}{2} = k - \frac{\overline{\mathrm{BF}}}{2}$입니다.""",
                'knowledge_en': r"""With $c'=\frac{k}{2}$ and $a'=\frac{\overline{\mathrm{BF}}-k}{2}$, $\overline{\mathrm{BC}} = c'-a' = k - \frac{\overline{\mathrm{BF}}}{2}$. Substitute into $8\overline{\mathrm{BC}} = \overline{\mathrm{BF}}$.""",
                'questions': [{
                    'level_label': '쌍곡선 변 비율 디딤돌 2',
                    'level_label_en': 'Hyperbola Ratio Step 2',
                    'stem': r'$8\left(k - \dfrac{\overline{\mathrm{BF}}}{2}\right) = \overline{\mathrm{BF}}$를 정리하여 얻는 $k : \overline{\mathrm{BF}}$의 비는?',
                    'stem_en': r'Simplifying $8(k - \frac{1}{2}\overline{\mathrm{BF}}) = \overline{\mathrm{BF}}$ yields what ratio $k : \overline{\mathrm{BF}}$?',
                    'options': [r'$3 : 5$', r'$4 : 7$', r'$5 : 8$', r'$5 : 9$', r'$3 : 4$'],
                    'answer': 3,
                    'exp': r'$8k - 4\overline{\mathrm{BF}} = \overline{\mathrm{BF}} \implies 8k = 5\overline{\mathrm{BF}} \implies k : \overline{\mathrm{BF}} = 5 : 8$입니다! 따라서 $k=5t,\; \overline{\mathrm{BF}}=8t$로 두면 둘레가 $5t+5t+8t = 18t$로 간단히 표현됩니다.',
                    'exp_en': r'$8k = 5\overline{\mathrm{BF}} \implies k = 5t,\; \overline{\mathrm{BF}} = 8t$, making the perimeter $18t$.',
                }],
            },
            {
                'title': r'🌱 3단계 · [쌍곡선 모양] $3:4:5$ 직각삼각형으로 점근선 기울기 구하기',
                'title_en': r'🌱 Step 3 · [Hyperbola Asymptote] Finding the $3:4:5$ Slope $\frac{4}{3}$',
                'knowledge': r"""$k=5t$, $\overline{\mathrm{BF}}=8t$이면 쌍곡선 중심 $\mathrm{M}$ 기준 $c' = \frac{5}{2}t$, $a' = \frac{8t-5t}{2} = \frac{3}{2}t$입니다. 피타고라스 정리로 $b'$을 구합니다.""",
                'knowledge_en': r"""From $c'=\frac{5}{2}t$ and $a'=\frac{3}{2}t$, compute $b'=\sqrt{c'^2-a'^2}$ and slope $b'/a'$.""",
                'questions': [{
                    'level_label': '쌍곡선 점근선 기울기 디딤돌 3',
                    'level_label_en': 'Asymptote Slope Step 3',
                    'stem': r"""$c' = \dfrac{5}{2}t$, $a' = \dfrac{3}{2}t$일 때 양수 기울기를 갖는 쌍곡선 점근선 $l$의 기울기 $\dfrac{b'}{a'}$는?""",
                    'stem_en': r"""With $c'=\frac{5}{2}t$ and $a'=\frac{3}{2}t$, what is the positive asymptote slope $\frac{b'}{a'}$?""",
                    'options': [r'$\dfrac{3}{4}$', r'$1$', r'$\dfrac{4}{3}$', r'$\dfrac{5}{3}$', r'$\dfrac{5}{4}$'],
                    'answer': 3,
                    'exp': r"""$b' = \sqrt{\left(\frac{5}{2}t\right)^2 - \left(\frac{3}{2}t\right)^2} = \frac{4}{2}t = 2t$이므로 기울기는 $\frac{2t}{(3/2)t} = \frac{4}{3}$입니다.""",
                    'exp_en': r"""$b' = 2t$, giving slope $\frac{2t}{(3/2)t} = \frac{4}{3}$.""",
                }],
            },
            {
                'title': r'🌳 4단계 · [좌표 및 점근선 거리] $p$와 점 $\mathrm{M}$ 좌표를 $t$로 표현해 $t$ 구하기',
                'title_en': r'🌳 Step 4 · [Distance to Asymptote] Solving $d(\mathrm{F}, l) = 6t = 15$',
                'knowledge': r'$\mathrm{A}(k-p, y_A)$에서 $\overline{\mathrm{BF}}^2 = (2p)^2 + 4p(k-p) = 4pk$입니다! $(8t)^2 = 4p(5t) \implies p = \frac{16}{5}t$, $y_A = \frac{24}{5}t$, $\mathrm{F}(\frac{16}{5}t, 0)$, 중심 $\mathrm{M}(-\frac{7}{10}t, \frac{24}{5}t)$를 얻습니다.',
                'knowledge_en': r'Since $\overline{\mathrm{BF}}^2 = 4pk$, $(8t)^2=20pt \implies p=\frac{16}{5}t$. Write $l$ through $\mathrm{M}(-\frac{7}{10}t, \frac{24}{5}t)$ with slope $\frac{4}{3}$ and compute $d(\mathrm{F}, l)$.',
                'questions': [{
                    'level_label': '비례상수 $t$ 계산 디딤돌 4',
                    'level_label_en': 'Scale Constant Step 4',
                    'stem': r'점근선 $l: 4x - 3y + \dfrac{86}{5}t = 0$과 초점 $\mathrm{F}\!\left(\dfrac{16}{5}t,\; 0\right)$ 사이의 거리 $d(\mathrm{F},l) = 6t$가 $15$일 때, $t$의 값은?',
                    'stem_en': r'If distance $d(\mathrm{F},l) = 6t$ equals $15$, what is $t$?',
                    'options': [r'$2$', r'$\dfrac{9}{4}$', r'$\dfrac{5}{2}$', r'$\dfrac{11}{4}$', r'$3$'],
                    'answer': 3,
                    'exp': r'$6t = 15 \implies t = \frac{15}{6} = \frac{5}{2}$입니다! (이때 $p = \frac{16}{5} \cdot \frac{5}{2} = 8$, $k=12.5$, $\overline{\mathrm{BF}}=20$이며 $\overline{\mathrm{AF}}=12.5 < 2p=16$ 조건도 성립합니다.)',
                    'exp_en': r'$6t = 15 \implies t = \frac{5}{2}$ (so $p=8$ and $\overline{\mathrm{AF}}=12.5 < 16$).',
                }],
            },
            {
                'title': r'💎 5단계 · [최종 종합] $\triangle\mathrm{ABF}$의 둘레 $18t$ 확정하기',
                'title_en': r'💎 Step 5 · [Final Synthesis] Perimeter $18t = 45$',
                'knowledge': r'둘레는 $\overline{\mathrm{AB}} + \overline{\mathrm{AF}} + \overline{\mathrm{BF}} = 5t + 5t + 8t = 18t$입니다.',
                'knowledge_en': r'Substitute $t = \frac{5}{2}$ into $18t$.',
                'questions': [{
                    'level_label': '최종 종합 디딤돌 5',
                    'level_label_en': 'Final Synthesis Step 5',
                    'stem': r'$t = \dfrac{5}{2}$일 때, 삼각형 $\mathrm{ABF}$의 둘레의 길이 $18t$는?',
                    'stem_en': r'When $t = \frac{5}{2}$, what is the perimeter $18t$ of $\triangle\mathrm{ABF}$?',
                    'options': [r'$40$', r'$42$', r'$45$', r'$48$', r'$50$'],
                    'answer': 3,
                    'exp': r'$18 \times \frac{5}{2} = 9 \times 5 = 45$이므로 정답은 $45$입니다.',
                    'exp_en': r'$18 \times \frac{5}{2} = 45$.',
                }],
            },
        ],
        'final': {
            'stem': r'초점이 $\mathrm{F}$인 포물선 $y^2=4px\;(p>0)$ 위에 있는 제$1$사분면 위의 한 점 $\mathrm{A}$에서 이 포물선의 준선에 내린 수선의 발을 $\mathrm{B}$라 하자. 두 초점이 $\mathrm{A}$, $\mathrm{B}$이고 점 $\mathrm{F}$를 지나는 쌍곡선의 두 꼭짓점 중 점 $\mathrm{B}$에 가까운 점을 $\mathrm{C}$라 하고, 이 쌍곡선의 점근선 중 기울기가 양수인 직선을 $l$이라 하자. $8\overline{\mathrm{BC}}=\overline{\mathrm{BF}}$이고 점 $\mathrm{F}$와 직선 $l$ 사이의 거리가 $15$일 때, 삼각형 $\mathrm{ABF}$의 둘레의 길이를 구하시오. (단, $\overline{\mathrm{AF}}<2p$) [4점]',
            'stem_en': r'From a first-quadrant point $\mathrm{A}$ on the parabola $y^2=4px\;(p>0)$ with focus $\mathrm{F}$, drop a perpendicular to the directrix at $\mathrm{B}$. For the hyperbola with foci $\mathrm{A}, \mathrm{B}$ passing through $\mathrm{F}$, let $\mathrm{C}$ be the vertex closer to $\mathrm{B}$ and $l$ be the asymptote with positive slope. Given $8\overline{\mathrm{BC}}=\overline{\mathrm{BF}}$, distance $15$ from $\mathrm{F}$ to $l$, and $\overline{\mathrm{AF}}<2p$, find the perimeter of $\triangle\mathrm{ABF}$. [4 points]',
            'options': [r'$40$', r'$42$', r'$45$', r'$48$', r'$50$'],
            'answer': 3,
            'exp': r"""포물선 정의로 $\overline{\mathrm{AB}}=\overline{\mathrm{AF}}=k$이고 쌍곡선 정의로 $2a'=\overline{\mathrm{BF}}-k$이며 $\overline{\mathrm{BC}}=\frac{k}{2}-a'=k-\frac{\overline{\mathrm{BF}}}{2}$입니다. $8\overline{\mathrm{BC}}=\overline{\mathrm{BF}}$에서 $k=5t,\; \overline{\mathrm{BF}}=8t$가 되어 $c'=\frac{5}{2}t, a'=\frac{3}{2}t, b'=2t$인 $3:4:5$ 쌍곡선이 됩니다. 또한 $\overline{\mathrm{BF}}^2=4pk$에서 $p=\frac{16}{5}t$이므로 $d(\mathrm{F},l)=6t=15 \implies t=\frac{5}{2}$, 둘레는 $18t=45$입니다.""",
            'exp_en': r'By parabola and hyperbola definitions, $8\overline{\mathrm{BC}}=\overline{\mathrm{BF}}$ yields $k=5t, \overline{\mathrm{BF}}=8t$, producing a $3:4:5$ hyperbola with asymptote slope $\frac{4}{3}$. Using $\overline{\mathrm{BF}}^2=4pk$ gives $p=\frac{16}{5}t$ and $d(\mathrm{F},l)=6t=15 \implies t=\frac{5}{2}$, so perimeter $18t=45$.',
            'solution': (
                r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>""" + '\n'
                + r"""<p>본 문항은 <b>포물선의 정의($\overline{\mathrm{AB}}=\overline{\mathrm{AF}}$)</b>와 <b>쌍곡선의 정의(거리 차 일정 $= 2a'$)</b> 및 <b>점근선의 기울기 $\frac{b'}{a'}$</b>를 하나의 비례상수 $t$로 깔끔하게 통합하여 도형의 크기를 결정하는 고난도 이차곡선 통합 문항입니다.</p>""" + '\n'
                + _wrap_visual_svg(
                    "📐 [2027 수능 기하 29번] 5t:5t:8t 이등변삼각형 + 3:4:5 쌍곡선 점근선",
                    "t = 5/2 (p = 8) ⇒ 둘레 = 45",
                    _SVG_G29_INNER,
                    height=268,
                    lang="ko",
                    caption="▲ 포물선 정의(AB=AF=k)와 8BC=BF 조건이 만나면 t만 남는 5t:5t:8t 삼각형과 3:4:5 쌍곡선으로 즉시 단순화됩니다.",
                )
                + _wrap_schematic_flow(
                    [
                        r"포물선: $\overline{\mathrm{AB}}=\overline{\mathrm{AF}}=k$",
                        r"$8\overline{\mathrm{BC}}=\overline{\mathrm{BF}} \implies k=5t,\; \overline{\mathrm{BF}}=8t$",
                        r"쌍곡선 $3:4:5$ ➔ 기울기 $\frac{4}{3}$",
                        r"$d(\mathrm{F},l)=6t=15 \implies 18t=45$",
                    ],
                    r"정답 $45$",
                    lang="ko",
                )
                + r"""<h4>📐 [단계별 상세 풀이 전개]</h4>""" + '\n'
                + r"""<p><b>1단계: 두 이차곡선의 정의로 비례상수 $t$ 도입하기</b><br>포물선 정의로 $\overline{\mathrm{AB}}=\overline{\mathrm{AF}}=k$라 하고 ($\overline{\mathrm{AF}} < 2p$), 초점 $\mathrm{F}(p,0)$와 $\mathrm{B}(-p, y_A)$, $\mathrm{A}(k-p, y_A)$에 대하여 $y_A^2 = 4p(k-p)$이므로 $$\overline{\mathrm{BF}}^2 = (2p)^2 + 4p(k-p) = 4pk$$ $\overline{\mathrm{AF}} < 2p$이므로 $k < 2p \implies k^2 < 2pk < 4pk$, 즉 $\overline{\mathrm{AF}} < \overline{\mathrm{BF}}$입니다. 두 초점 $\mathrm{A},\mathrm{B}$($c'=\frac{k}{2}$)이고 $\mathrm{F}$를 지나는 쌍곡선의 주축 길이는 $2a' = \overline{\mathrm{BF}} - k$이므로 $\overline{\mathrm{BC}} = c' - a' = k - \frac{\overline{\mathrm{BF}}}{2}$입니다. 조건 $8\overline{\mathrm{BC}}=\overline{\mathrm{BF}}$에 대입하면 $$8k - 4\overline{\mathrm{BF}} = \overline{\mathrm{BF}} \implies 8k = 5\overline{\mathrm{BF}}$$ 따라서 $k = 5t,\; \overline{\mathrm{BF}} = 8t\;(t>0)$라 두면 $\triangle\mathrm{ABF}$의 둘레는 $5t+5t+8t = 18t$입니다.<br><br><b>2단계: 점근선 $l$과 점 $\mathrm{F}$ 사이의 거리 $15$ 적용</b><br>쌍곡선에서 $c' = \frac{5}{2}t,\; a' = \frac{3}{2}t$이므로 $b' = \sqrt{c'^2-a'^2} = 2t$이고 양수 기울기 점근선 $l$의 기울기는 $\frac{b'}{a'} = \frac{4}{3}$입니다. 또한 $\overline{\mathrm{BF}}^2 = 4pk$에서 $64t^2 = 4p(5t) \implies p = \frac{16}{5}t$, $y_A = \sqrt{4 \cdot \frac{16}{5}t \cdot \frac{9}{5}t} = \frac{24}{5}t$입니다. 쌍곡선 중심 $\mathrm{M}$은 $\mathrm{AB}$의 중점이므로 $$\mathrm{M}\!\left(-p+\frac{k}{2},\; y_A\right) = \left(-\frac{7}{10}t,\; \frac{24}{5}t\right), \qquad \mathrm{F}\!\left(\frac{16}{5}t,\; 0\right)$$ 점근선 $l$의 방정식은 $y - \frac{24}{5}t = \frac{4}{3}\left(x + \frac{7}{10}t\right) \iff 4x - 3y + \frac{86}{5}t = 0$이므로 점 $\mathrm{F}$에서 $l$까지의 거리는 $$d(\mathrm{F}, l) = \frac{\left|4\left(\frac{16}{5}t\right) - 0 + \frac{86}{5}t\right|}{\sqrt{4^2 + (-3)^2}} = \frac{30t}{5} = 6t = 15 \implies t = \frac{5}{2}$$</p>""" + '\n'
                + r"""<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>""" + '\n'
                + r'<p>따라서 구하는 삼각형 $\mathrm{ABF}$의 둘레의 길이는 $18t = 18 \times \frac{5}{2} = \mathbf{45}$입니다. ($p=8$, $\mathrm{A}(\frac{9}{2},12)$로 $\overline{\mathrm{AF}}=12.5 < 16$도 완벽히 확인! <a href="https://min7014.github.io/" target="_blank" rel="noopener">수학자료실(min7014.github.io)</a>의 이차곡선 복합 작도 앱렛도 함께 탐구해 보세요.)</p>'
            ),
            'solution_en': (
                r"""<h4>📋 [Problem Analysis &amp; Core Concepts]</h4>""" + '\n'
                + r"""<p>Combine parabola and hyperbola definitions with parameter $t$ to obtain a $5t$-$5t$-$8t$ triangle and a $3:4:5$ hyperbola whose asymptote distance determines $t$.</p>""" + '\n'
                + _wrap_visual_svg(
                    "📐 [2027 CSAT Geometry #29] Parabola-Hyperbola Scaling t = 5/2",
                    "Perimeter 18t = 45",
                    _SVG_G29_INNER,
                    height=268,
                    lang="en",
                    caption="▲ Parameterizing k=5t and BF=8t reduces the hyperbola to a 3:4:5 ratio with d(F, l) = 6t = 15.",
                )
                + _wrap_schematic_flow(
                    [
                        r"Parabola $\overline{\mathrm{AB}}=\overline{\mathrm{AF}}=k$",
                        r"$8\overline{\mathrm{BC}}=\overline{\mathrm{BF}} \implies k=5t, \mathrm{BF}=8t$",
                        r"$a'=\frac{3}{2}t, b'=2t \implies$ slope $\frac{4}{3}$",
                        r"$6t=15 \implies t=\frac{5}{2} \implies 45$",
                    ],
                    r"$45$",
                    lang="en",
                )
                + r"""<h4>📐 [Step-by-Step Rigorous Derivation]</h4>""" + '\n'
                + r"""<p>With $\overline{\mathrm{AB}}=\overline{\mathrm{AF}}=k$, $2a'=\overline{\mathrm{BF}}-k$, and $\overline{\mathrm{BC}}=k-\frac{1}{2}\overline{\mathrm{BF}}$, condition $8\overline{\mathrm{BC}}=\overline{\mathrm{BF}}$ gives $k=5t,\; \overline{\mathrm{BF}}=8t$. Thus $c'=\frac{5}{2}t,\; a'=\frac{3}{2}t,\; b'=2t$, giving asymptote slope $\frac{4}{3}$. Using $\overline{\mathrm{BF}}^2=4pk$ gives $p=\frac{16}{5}t$ and center $\mathrm{M}(-\frac{7}{10}t, \frac{24}{5}t)$, so $d(\mathrm{F},l)=6t=15 \implies t=\frac{5}{2}$ and perimeter $18t=45$.</p>""" + '\n'
                + r"""<h4>✨ [Conclusion &amp; Key Takeaways]</h4>""" + '\n'
                + r'<p>Hence the perimeter of $\triangle\mathrm{ABF}$ is <b>$45$</b>.</p>'
            ),
        },
    },

    # =========================================================================
    # 기하 30번 (csat27_g30) — 4점 단답형 킬러, 정답 223
    # =========================================================================
    {
        'slug': 'csat27_g30',
        'qNum': '30',
        'points': 4,
        'is_short_answer': True,
        'official_ans_str': '223',
        'subject': '기하',
        'title': '[2027학년도 수능 고3 기하 30번] 두 구의 교선 원의 정사영 넓이와 이면각 계산',
        'title_en': '[2027 CSAT Math Geometry #30] Orthogonal Projection Area of Intersection Circle of Two Spheres',
        'summary_ko': r'반지름 $3\sqrt{5}$인 구 $S_1$과 $\overline{\mathrm{OH}}=2\sqrt{5}$인 평면 $\alpha$의 교선 $C_1$ 위에 $\overline{\mathrm{AB}}=10$, $\overline{\mathrm{BC}}=2\sqrt{10}$이 되도록 $\mathrm{A},\mathrm{B},\mathrm{C}$를 잡고, $\mathrm{C}$를 지나며 $\alpha$에 수직인 직선과 $S_1$의 다른 교점 $\mathrm{D}$를 중심으로 평면 $\mathrm{OAB}$에 접하는 구 $S_2$를 만들 때, 교선 $C_2$의 $\alpha$ 위로의 정사영 넓이를 구하는 최고난도 문항입니다.',
        'summary_en': r'Sphere $S_1$ ($R=3\sqrt{5}$) meets plane $\alpha$ ($\overline{\mathrm{OH}}=2\sqrt{5}$) in circle $C_1$, with points $\mathrm{A},\mathrm{B},\mathrm{C}\in C_1$ satisfying $\overline{\mathrm{AB}}=10$, $\overline{\mathrm{BC}}=2\sqrt{10}$. Line through $\mathrm{C}$ normal to $\alpha$ meets $S_1$ again at $\mathrm{D}$. Sphere $S_2$ centered at $\mathrm{D}$ is tangent to plane $\mathrm{OAB}$ and meets $S_1$ in circle $C_2$. Find $p+q$ when the projection of $C_2$ onto $\alpha$ has area $\frac{q}{p}\pi$.',
        'tags': ['2027학년도 수능', '기하', '공간도형', '구와 평면', '정사영', '킬러 문항'],
        'orig_svg': ORIG_SVG_G30,
        'symbols': [
            {
                'sym': r'$r_1 = \sqrt{R_1^2 - \overline{\mathrm{OH}}^2}$',
                'desc': r'구 $S_1$을 평면 $\alpha$로 자른 단면 원 $C_1$의 반지름($=5$)입니다. $\overline{\mathrm{AB}}=10=2r_1$이므로 $\mathrm{AB}$는 $C_1$의 지름입니다!',
                'desc_en': r'Radius of section circle $C_1$ ($=5$), proving $\mathrm{AB}=10$ is a diameter of $C_1$.',
            },
            {
                'sym': r'$\overline{\mathrm{CD}} \parallel \text{평면 }\mathrm{OAB}$',
                'desc': r'$\overline{\mathrm{CD}} \perp \alpha$이고 $\overline{\mathrm{OH}} \perp \alpha$이므로 $\overline{\mathrm{CD}} \parallel \overline{\mathrm{OH}}$이며, $\mathrm{H}$는 지름 $\mathrm{AB}$의 중점이므로 $\overline{\mathrm{OH}} \subset \text{평면 }\mathrm{OAB}$입니다!',
                'desc_en': r'Because $\mathrm{AB}$ is a diameter through $\mathrm{H}$, line $\mathrm{OH}$ lies inside plane $\mathrm{OAB}$, making $\mathrm{CD} \parallel \text{plane }\mathrm{OAB}$.',
            },
            {
                'sym': r"""$S' = \pi r_2^2 \cos\theta$""",
                'desc': r'교선 원 $C_2$가 놓인 평면($\perp \overrightarrow{\mathrm{OD}}$)과 평면 $\alpha$($\perp \overrightarrow{\mathrm{OH}}$)가 이루는 각 $\theta$에 대한 정사영 넓이 공식입니다.',
                'desc_en': r'Area projection formula using dihedral angle $\theta$ between the radical plane ($\perp\mathrm{OD}$) and plane $\alpha$ ($\perp\mathrm{OH}$).',
            },
        ],
        'levels': [
            {
                'title': r'🔰 1단계 · [초등 기초 직관] 단면 원 $C_1$의 반지름과 지름 $\mathrm{AB}$ 발견하기',
                'title_en': r'🔰 Step 1 · [Elementary Intuition] Discovering $\mathrm{AB}$ Is a Diameter of Circle $C_1$',
                'knowledge': r'구 $S_1$의 반지름이 $R_1 = 3\sqrt{5}$($R_1^2=45$)이고 중심 $\mathrm{O}$에서 평면 $\alpha$까지 수선의 발 거리가 $\overline{\mathrm{OH}}=2\sqrt{5}$($\overline{\mathrm{OH}}^2=20$)입니다. 피타고라스 정리로 단면 원 $C_1$의 반지름 $r_1$을 구합니다.',
                'knowledge_en': r'Use Pythagoras $r_1 = \sqrt{R_1^2 - \overline{\mathrm{OH}}^2}$ to find the radius of $C_1$ and compare $2r_1$ to $\overline{\mathrm{AB}}=10$.',
                'questions': [{
                    'level_label': '초등 기초 직관 디딤돌 1',
                    'level_label_en': 'Elementary Intuition Step 1',
                    'stem': r'단면 원 $C_1$의 반지름 $r_1 = \sqrt{(3\sqrt{5})^2 - (2\sqrt{5})^2}$을 구하면 지름이 $\overline{\mathrm{AB}}=10$과 같음을 알 수 있습니다. 이때 원주각 성질로 반드시 직각($90^\circ$)이 되는 각은?',
                    'stem_en': r'Computing $r_1 = \sqrt{45-20}=5$ reveals $\overline{\mathrm{AB}}=10$ is a diameter of $C_1$. Which angle must therefore be $90^\circ$?',
                    'options': [
                        r'$\angle\mathrm{CAB}$',
                        r'$\angle\mathrm{CBA}$',
                        r'$\angle\mathrm{ACB}$',
                        r'$\angle\mathrm{AOB}$',
                        r'$\angle\mathrm{HOC}$',
                    ],
                    'answer': 3,
                    'exp': r'$r_1 = \sqrt{45-20}=5$이므로 지름은 $10=\overline{\mathrm{AB}}$입니다! 원의 지름에 대한 원주각이므로 $\angle\mathrm{ACB}=90^\circ$입니다.',
                    'exp_en': r'$r_1=5$ means $\mathrm{AB}$ is a diameter of $C_1$, so $\angle\mathrm{ACB}=90^\circ$.',
                }],
            },
            {
                'title': r'🌿 2단계 · [반지름 $R_2$ 발견] 구 $S_2$의 반지름 $= \text{평면 }\mathrm{OAB}$까지 거리 $= 2\sqrt{6}$',
                'title_en': r'🌿 Step 2 · [Sphere $S_2$ Radius] Finding $R_2 = d(\mathrm{D}, \mathrm{OAB}) = 2\sqrt{6}$',
                'knowledge': r'$\mathrm{AB}$가 지름이므로 $\mathrm{H}$는 $\mathrm{AB}$의 중점이고 직선 $\mathrm{OH}$는 평면 $\mathrm{OAB}$에 포함됩니다! $\overline{\mathrm{CD}} \parallel \overline{\mathrm{OH}}$이므로 직선 $\mathrm{CD}$는 평면 $\mathrm{OAB}$와 평행해 $d(\mathrm{D},\mathrm{OAB}) = d(\mathrm{C},\mathrm{OAB}) = d(\mathrm{C},\overline{\mathrm{AB}})$가 됩니다.',
                'knowledge_en': r'Since $\mathrm{CD} \parallel \mathrm{OH} \subset \text{plane }\mathrm{OAB}$ and $\alpha \perp \mathrm{OAB}$, $R_2 = d(\mathrm{D},\mathrm{OAB})$ equals the altitude of right triangle $\mathrm{ACB}$.',
                'questions': [{
                    'level_label': '구 $S_2$ 반지름 디딤돌 2',
                    'level_label_en': 'Sphere $S_2$ Radius Step 2',
                    'stem': r'직각삼각형 $\mathrm{ACB}$($\overline{\mathrm{AB}}=10,\; \overline{\mathrm{BC}}=2\sqrt{10}$)에서 빗변 $\mathrm{AB}$ 위로 내린 높이 $d(\mathrm{C}, \overline{\mathrm{AB}}) = R_2$의 값은?',
                    'stem_en': r'In right triangle $\mathrm{ACB}$ ($\overline{\mathrm{AB}}=10, \overline{\mathrm{BC}}=2\sqrt{10}$), what is the altitude to hypotenuse $\mathrm{AB}$ (which equals $R_2$)?',
                    'options': [r'$2\sqrt{5}$', r'$2\sqrt{6}$', r'$5$', r'$3\sqrt{3}$', r'$2\sqrt{10}$'],
                    'answer': 2,
                    'exp': r'$\overline{\mathrm{AC}} = \sqrt{100 - 40} = \sqrt{60} = 2\sqrt{15}$입니다. 넓이 등식 $\frac{1}{2}\cdot 2\sqrt{10}\cdot 2\sqrt{15} = \frac{1}{2}\cdot 10\cdot R_2$에서 $R_2 = \frac{4\sqrt{150}}{10} = \frac{20\sqrt{6}}{10} = 2\sqrt{6}$ ($R_2^2 = 24$)입니다!',
                    'exp_en': r'$\overline{\mathrm{AC}} = 2\sqrt{15}$, so altitude $R_2 = \frac{2\sqrt{10}\cdot 2\sqrt{15}}{10} = 2\sqrt{6}$.',
                }],
            },
            {
                'title': r'🌱 3단계 · [교선 원 $C_2$ 반지름] 이등변삼각형 $\mathrm{ODP}$로 $r_2^2$ 구하기',
                'title_en': r'🌱 Step 3 · [Radius of $C_2$] Solving Isosceles $\triangle\mathrm{ODP}$ for $r_2^2$',
                'knowledge': r'점 $\mathrm{D}$는 구 $S_1$ 위의 점이므로 $\overline{\mathrm{OD}}=3\sqrt{5}$입니다! 교선 원 $C_2$ 위의 한 점 $\mathrm{P}$에 대해 $\triangle\mathrm{ODP}$는 $\overline{\mathrm{OP}}=\overline{\mathrm{OD}}=3\sqrt{5}$, $\overline{\mathrm{DP}}=2\sqrt{6}$인 이등변삼각형이며, $\mathrm{P}$에서 $\overline{\mathrm{OD}}$에 내린 높이가 바로 $C_2$의 반지름 $r_2$입니다!',
                'knowledge_en': r'Since $\mathrm{D}\in S_1$, $\triangle\mathrm{ODP}$ for $\mathrm{P}\in C_2$ is isosceles with sides $3\sqrt{5}, 3\sqrt{5}, 2\sqrt{6}$, and its altitude to $\mathrm{OD}$ is $r_2$.',
                'questions': [{
                    'level_label': '교선 원 반지름 $r_2^2$ 디딤돌 3',
                    'level_label_en': 'Intersection Circle Radius Step 3',
                    'stem': r'이등변삼각형 $\mathrm{ODP}$($\overline{\mathrm{OP}}=\overline{\mathrm{OD}}=3\sqrt{5},\; \overline{\mathrm{DP}}=2\sqrt{6}$)에서 변 $\mathrm{OD}$로 내린 높이 $r_2$의 제곱 $r_2^2$은?',
                    'stem_en': r'In isosceles $\triangle\mathrm{ODP}$ ($3\sqrt{5}, 3\sqrt{5}, 2\sqrt{6}$), what is $r_2^2$, where $r_2$ is the altitude to $\mathrm{OD}$?',
                    'options': [r'$\dfrac{98}{5}$', r'$20$', r'$\dfrac{102}{5}$', r'$\dfrac{104}{5}$', r'$21$'],
                    'answer': 4,
                    'exp': r'$\mathrm{DP}$의 중점 $\mathrm{M}$에서 $\overline{\mathrm{DM}}=\sqrt{6}$이므로 $\overline{\mathrm{OM}}=\sqrt{45-6}=\sqrt{39}$입니다. 넓이 등식 $\frac{1}{2}(2\sqrt{6})\sqrt{39} = \frac{1}{2}(3\sqrt{5})r_2$에서 $r_2 = \frac{2\sqrt{234}}{3\sqrt{5}} = \frac{2\sqrt{26}}{\sqrt{5}}$이므로 $r_2^2 = \frac{104}{5}$입니다!',
                    'exp_en': r'Altitude to base $\mathrm{DP}$ is $\sqrt{45-6}=\sqrt{39}$, so $r_2 = \frac{2\sqrt{6}\sqrt{39}}{3\sqrt{5}} \implies r_2^2 = \frac{104}{5}$.',
                }],
            },
            {
                'title': r'🌳 4단계 · [이면각 $\cos\theta$] $C_2$ 평면($\perp\overrightarrow{\mathrm{OD}}$)과 $\alpha$($\perp\overrightarrow{\mathrm{OH}}$) 사이 각 구하기',
                'title_en': r'🌳 Step 4 · [Dihedral Angle] Finding $\cos\theta = \frac{2}{3}$',
                'knowledge': r"""구 $S_1, S_2$ 교선 $C_2$를 품는 평면의 법선벡터는 중심선 $\overrightarrow{\mathrm{OD}}$이고, 평면 $\alpha$의 법선벡터는 $\overrightarrow{\mathrm{OH}}$입니다. $\overline{\mathrm{CD}}\perp\alpha$이고 $\mathrm{C}\in\alpha$, $\overline{\mathrm{CD}}$가 중심 $\mathrm{O}$에 대해 평면 $\alpha$ 대칭 평면까지 이어지므로 $\mathrm{D}$에서 직선 $\mathrm{OH}$에 내린 수선의 발 $\mathrm{H}'$에 대해 $\overline{\mathrm{OH}'}=\overline{\mathrm{OH}}=2\sqrt{5}$입니다!""",
                'knowledge_en': r'The angle $\theta$ between the two planes equals the angle between their normals $\overrightarrow{\mathrm{OD}}$ and $\overrightarrow{\mathrm{OH}}$. By symmetry across the plane through $\mathrm{O}$ parallel to $\alpha$, the projection of $\mathrm{OD}$ onto line $\mathrm{OH}$ has length $2\sqrt{5}$.',
                'questions': [{
                    'level_label': r'정사영 $\cos\theta$ 디딤돌 4',
                    'level_label_en': 'Cosine Angle Step 4',
                    'stem': r"""직각삼각형 $\mathrm{OH}'\mathrm{D}$에서 $\overline{\mathrm{OH}'}=2\sqrt{5}$, $\overline{\mathrm{OD}}=3\sqrt{5}$일 때 두 평면 사이 각 $\theta$에 대한 $\cos\theta$의 값은?""",
                    'stem_en': r"""Using $\overline{\mathrm{OH}'}=2\sqrt{5}$ and $\overline{\mathrm{OD}}=3\sqrt{5}$, what is $\cos\theta$?""",
                    'options': [r'$\dfrac{1}{3}$', r'$\dfrac{\sqrt{5}}{5}$', r'$\dfrac{2}{3}$', r'$\dfrac{\sqrt{6}}{3}$', r'$\dfrac{3}{4}$'],
                    'answer': 3,
                    'exp': r"""$\cos\theta = \frac{\overline{\mathrm{OH}'}}{\overline{\mathrm{OD}}} = \frac{2\sqrt{5}}{3\sqrt{5}} = \frac{2}{3}$입니다!""",
                    'exp_en': r'$\cos\theta = \frac{2\sqrt{5}}{3\sqrt{5}} = \frac{2}{3}$.',
                }],
            },
            {
                'title': r'💎 5단계 · [최종 종합] 정사영 넓이 $\dfrac{q}{p}\pi$와 $p+q$ 구하기',
                'title_en': r'💎 Step 5 · [Final Synthesis] Projected Area $\frac{208}{15}\pi$ and $p+q=223$',
                'knowledge': r'정사영 넓이는 $\pi r_2^2 \cos\theta = \pi \cdot \frac{104}{5} \cdot \frac{2}{3}$입니다.',
                'knowledge_en': r'Multiply $\pi r_2^2 \cos\theta$ and add numerator and denominator.',
                'questions': [{
                    'level_label': '최종 종합 디딤돌 5',
                    'level_label_en': 'Final Synthesis Step 5',
                    'stem': r'원 $C_2$의 평면 $\alpha$ 위로의 정사영 넓이 $\pi \cdot \dfrac{104}{5} \cdot \dfrac{2}{3} = \dfrac{q}{p}\pi$에서 기약분수 $\dfrac{q}{p}$의 $p+q$의 값은?',
                    'stem_en': r'For projected area $\frac{104}{5}\cdot\frac{2}{3}\pi = \frac{q}{p}\pi$ in lowest terms, what is $p+q$?',
                    'options': [r'$219$', r'$221$', r'$223$', r'$225$', r'$227$'],
                    'answer': 3,
                    'exp': r'$\frac{208}{15}\pi$에서 $15$와 $208$은 서로소이므로 $p=15, q=208$, 따라서 $p+q = 15+208 = 223$입니다!',
                    'exp_en': r'$\frac{208}{15}\pi$ is irreducible ($\gcd(15,208)=1$), giving $p+q=223$.',
                }],
            },
        ],
        'final': {
            'stem': r'좌표공간에 중심이 $\mathrm{O}$이고 반지름의 길이가 $3\sqrt{5}$인 구 $S_1$이 있다. $\overline{\mathrm{OH}}=2\sqrt{5}$인 점 $\mathrm{H}$를 지나고 직선 $\mathrm{OH}$에 수직인 평면 $\alpha$가 구 $S_1$과 만나서 생기는 원을 $C_1$이라 하자. 원 $C_1$ 위에 서로 다른 세 점 $\mathrm{A},\; \mathrm{B},\; \mathrm{C}$를 $\overline{\mathrm{AB}}=10,\; \overline{\mathrm{BC}}=2\sqrt{10}$이 되도록 잡는다.<br>점 $\mathrm{C}$를 지나고 평면 $\alpha$에 수직인 직선이 구 $S_1$과 만나는 점 중 $\mathrm{C}$가 아닌 점을 $\mathrm{D}$라 하자. 중심이 $\mathrm{D}$이고 평면 $\mathrm{OAB}$에 접하는 구를 $S_2$라 하고, 두 구 $S_1$과 $S_2$가 만나서 생기는 원을 $C_2$라 하자. 원 $C_2$의 평면 $\alpha$ 위로의 정사영의 넓이가 $\dfrac{q}{p}\pi$일 때, $p+q$의 값을 구하시오. (단, $p$와 $q$는 서로소인 자연수이다.) [4점]',
            'stem_en': r'In 3D space, sphere $S_1$ centered at $\mathrm{O}$ has radius $3\sqrt{5}$. Plane $\alpha$ passes through $\mathrm{H}$ ($\overline{\mathrm{OH}}=2\sqrt{5}$) perpendicular to $\mathrm{OH}$, intersecting $S_1$ in circle $C_1$. Three distinct points $\mathrm{A},\mathrm{B},\mathrm{C}\in C_1$ satisfy $\overline{\mathrm{AB}}=10$ and $\overline{\mathrm{BC}}=2\sqrt{10}$. The line through $\mathrm{C}$ perpendicular to $\alpha$ meets $S_1$ again at $\mathrm{D}$. Sphere $S_2$ centered at $\mathrm{D}$ is tangent to plane $\mathrm{OAB}$ and meets $S_1$ in circle $C_2$. If the orthogonal projection of $C_2$ onto $\alpha$ has area $\frac{q}{p}\pi$ ($\gcd(p,q)=1$), find $p+q$. [4 points]',
            'options': [r'$219$', r'$221$', r'$223$', r'$225$', r'$227$'],
            'answer': 3,
            'exp': r'$r_1=\sqrt{45-20}=5$이므로 $\overline{\mathrm{AB}}=10$은 $C_1$의 지름이고 $\overline{\mathrm{CD}}\parallel\overline{\mathrm{OH}}\subset\text{평면}\mathrm{OAB}$이므로 $S_2$의 반지름 $R_2=d(\mathrm{C},\overline{\mathrm{AB}})=2\sqrt{6}$입니다. 이등변삼각형 $\mathrm{ODP}$에서 $r_2^2=\frac{104}{5}$이고, 법선 사이 각 $\theta$는 $\cos\theta=\frac{2\sqrt{5}}{3\sqrt{5}}=\frac{2}{3}$이므로 정사영 넓이는 $\frac{104}{5}\cdot\frac{2}{3}\pi = \frac{208}{15}\pi$, $p+q=223$입니다.',
            'exp_en': r'Radius $r_1=5$ implies $\mathrm{AB}$ is a diameter of $C_1$, so $\mathrm{CD}\parallel\text{plane }\mathrm{OAB}$ and $R_2=d(\mathrm{C},\mathrm{AB})=2\sqrt{6}$. In isosceles $\triangle\mathrm{ODP}$, $r_2^2=\frac{104}{5}$, while $\cos\theta=\frac{2}{3}$. Thus projected area is $\frac{208}{15}\pi$, giving $p+q=223$.',
            'solution': (
                r"""<h4>📋 [문제 분석 및 핵심 출제 의도]</h4>""" + '\n'
                + r"""<p>본 문항은 구와 평면의 단면 원 $C_1$에서 <b>지름 조건($\overline{\mathrm{AB}}=10=2r_1$)</b>으로 직교 평면 $\mathrm{OAB} \perp \alpha$ 및 평행선 $\overline{\mathrm{CD}} \parallel \text{평면}\mathrm{OAB}$를 간파하고, 두 구의 교선 원 $C_2$의 반지름과 <b>법선벡터 내적을 통한 정사영 넓이</b>를 구하는 최고난도 기하 킬러 문항입니다.</p>""" + '\n'
                + _wrap_visual_svg(
                    "📐 [2027 수능 기하 30번] 단면 지름 AB=10 ⇒ R₂=2√6 &amp; 이등변 △ODP ⇒ (208/15)π",
                    "p=15, q=208 ⇒ 223",
                    _SVG_G30_INNER,
                    height=268,
                    lang="ko",
                    caption="▲ AB가 원 C₁의 지름이므로 H∈AB이고 CD ∥ OH ⊂ 평면 OAB가 성립하여 구 S₂의 반지름 R₂가 △ACB 높이 2√6으로 즉시 결정됩니다.",
                )
                + _wrap_schematic_flow(
                    [
                        r"$r_1=5 \implies \mathrm{AB}$는 $C_1$ 지름",
                        r"$\mathrm{CD}\parallel\text{평면}\mathrm{OAB} \implies R_2=2\sqrt{6}$",
                        r"$\triangle\mathrm{ODP}$ 넓이 ➔ $r_2^2=\frac{104}{5}$",
                        r"$\cos\theta=\frac{2}{3} \implies \frac{208}{15}\pi \to 223$",
                    ],
                    r"정답 $223$",
                    lang="ko",
                )
                + r"""<h4>📐 [단계별 상세 풀이 전개]</h4>""" + '\n'
                + r"""<p><b>1단계: 단면 원 $C_1$의 반지름과 $S_2$의 반지름 $R_2$ 구하기</b><br>구 $S_1$의 반지름이 $3\sqrt{5}$이고 $\overline{\mathrm{OH}}=2\sqrt{5}$이므로 단면 원 $C_1$의 반지름은 $r_1 = \sqrt{45 - 20} = 5$입니다. 이때 $\overline{\mathrm{AB}}=10=2r_1$이므로 선분 $\mathrm{AB}$는 원 $C_1$의 지름(즉, 중심 $\mathrm{H}$를 지남)이고 $\angle\mathrm{ACB}=90^\circ$입니다.<br>직각삼각형 $\mathrm{ACB}$에서 $\overline{\mathrm{AC}} = \sqrt{10^2 - (2\sqrt{10})^2} = 2\sqrt{15}$이므로 점 $\mathrm{C}$에서 $\overline{\mathrm{AB}}$에 내린 수선의 길이는 $\frac{2\sqrt{10}\cdot 2\sqrt{15}}{10} = 2\sqrt{6}$입니다.<br>한편 $\mathrm{H} \in \overline{\mathrm{AB}}$이므로 직선 $\mathrm{OH}$는 평면 $\mathrm{OAB}$에 포함되며, $\overline{\mathrm{CD}}\perp\alpha,\; \overline{\mathrm{OH}}\perp\alpha \implies \overline{\mathrm{CD}}\parallel\overline{\mathrm{OH}} \implies \overline{\mathrm{CD}}\parallel\text{평면 }\mathrm{OAB}$입니다. 또한 $\overline{\mathrm{OH}}\perp\alpha$이므로 평면 $\mathrm{OAB} \perp \alpha$이며 교선은 직선 $\mathrm{AB}$입니다. 따라서 $S_2$의 반지름은 $$R_2 = d(\mathrm{D},\text{평면 }\mathrm{OAB}) = d(\mathrm{C},\text{평면 }\mathrm{OAB}) = d(\mathrm{C},\overline{\mathrm{AB}}) = 2\sqrt{6}$$<br><br><b>2단계: 교선 원 $C_2$의 반지름 $r_2$와 정사영 각 $\cos\theta$</b><br>점 $\mathrm{D}$가 구 $S_1$ 위에 있으므로 $\overline{\mathrm{OD}} = 3\sqrt{5}$입니다. 교선 $C_2$ 위의 한 점 $\mathrm{P}$를 잡으면 $\triangle\mathrm{ODP}$는 $\overline{\mathrm{OP}}=\overline{\mathrm{OD}}=3\sqrt{5}$, $\overline{\mathrm{DP}}=R_2=2\sqrt{6}$인 이등변삼각형입니다. $\mathrm{DP}$의 중점 $\mathrm{M}$에 대해 $\overline{\mathrm{OM}}=\sqrt{(3\sqrt{5})^2-(\sqrt{6})^2}=\sqrt{39}$이므로 넓이 등식으로부터 $$\frac{1}{2}(2\sqrt{6})\sqrt{39} = \frac{1}{2}(3\sqrt{5})r_2 \implies r_2 = \frac{2\sqrt{234}}{3\sqrt{5}} = \frac{2\sqrt{26}}{\sqrt{5}} \implies r_2^2 = \frac{104}{5}$$ 또한 원 $C_2$를 포함하는 평면은 중심을 잇는 직선 $\mathrm{OD}$에 수직이고, 평면 $\alpha$는 직선 $\mathrm{OH}$에 수직입니다. 원점 $\mathrm{O}$에서 평면 $\alpha$까지 거리가 $2\sqrt{5}$이고 선분 $\mathrm{CD}$의 중점이 $\mathrm{O}$를 지나 $\alpha$에 평행한 평면 위에 있으므로, 점 $\mathrm{D}$에서 직선 $\mathrm{OH}$에 내린 수선의 발 $\mathrm{H}'$에 대하여 $\overline{\mathrm{OH}'}=\overline{\mathrm{OH}}=2\sqrt{5}$입니다. 따라서 두 평면이 이루는 예각 $\theta$는 $$\cos\theta = \frac{\overline{\mathrm{OH}'}}{\overline{\mathrm{OD}}} = \frac{2\sqrt{5}}{3\sqrt{5}} = \frac{2}{3}$$</p>""" + '\n'
                + r"""<h4>✨ [정답 도출 및 실전 점검 포인트]</h4>""" + '\n'
                + r'<p>그러므로 원 $C_2$의 평면 $\alpha$ 위로의 정사영의 넓이는 $$\pi r_2^2 \cos\theta = \pi \cdot \frac{104}{5} \cdot \frac{2}{3} = \frac{208}{15}\pi$$ $15$와 $208$은 서로소이므로 $p=15,\; q=208$이고 $p+q = \mathbf{223}$입니다. (<a href="https://min7014.github.io/" target="_blank" rel="noopener">수학자료실(min7014.github.io)</a>의 공간도형·구와 정사영 시각 자료로 직선 $\mathrm{OD}$와 법선벡터 대칭 구조를 함께 탐구해 보세요.)</p>'
            ),
            'solution_en': (
                r"""<h4>📋 [Problem Analysis &amp; Core Concepts]</h4>""" + '\n'
                + r"""<p>Notice $\overline{\mathrm{AB}}=10=2r_1$ is a diameter of $C_1$, so $\mathrm{OH}\subset\text{plane }\mathrm{OAB}$ and $\mathrm{CD}\parallel\text{plane }\mathrm{OAB}$, giving sphere radius $R_2=d(\mathrm{C},\mathrm{AB})=2\sqrt{6}$. Then use isosceles $\triangle\mathrm{ODP}$ and normal-vector cosine $\cos\theta=\frac{2}{3}$.</p>""" + '\n'
                + _wrap_visual_svg(
                    "📐 [2027 CSAT Geometry #30] Sphere Intersection Circle Projection",
                    "Projected Area = (208/15)pi => 223",
                    _SVG_G30_INNER,
                    height=268,
                    lang="en",
                    caption="▲ Diameter AB=10 locks R_2=2√6; isosceles △ODP yields r_2^2=104/5, and cos(theta)=2/3 yields (208/15)pi.",
                )
                + _wrap_schematic_flow(
                    [
                        r"$r_1=5 \implies \mathrm{AB}$ diameter",
                        r"$\mathrm{CD}\parallel\mathrm{OAB} \implies R_2=2\sqrt{6}$",
                        r"Isosceles $\triangle\mathrm{ODP} \implies r_2^2=\frac{104}{5}$",
                        r"$\cos\theta=\frac{2}{3} \implies \frac{208}{15}\pi \to 223$",
                    ],
                    r"$223$",
                    lang="en",
                )
                + r"""<h4>📐 [Step-by-Step Rigorous Derivation]</h4>""" + '\n'
                + r"""<p>Since $r_1=\sqrt{45-20}=5$, $\mathrm{AB}=10$ is a diameter of $C_1$, so $\mathrm{OH}\subset\text{plane }\mathrm{OAB}\perp\alpha$ and $R_2=d(\mathrm{C},\mathrm{AB})=2\sqrt{6}$. In isosceles $\triangle\mathrm{ODP}$ with sides $3\sqrt{5}, 3\sqrt{5}, 2\sqrt{6}$, altitude to $\mathrm{OD}$ satisfies $r_2^2=\frac{104}{5}$. The normals $\overrightarrow{\mathrm{OD}}$ and $\overrightarrow{\mathrm{OH}}$ give $\cos\theta=\frac{2\sqrt{5}}{3\sqrt{5}}=\frac{2}{3}$, so projected area is $\frac{208}{15}\pi$ and $p+q=223$.</p>""" + '\n'
                + r"""<h4>✨ [Conclusion &amp; Key Takeaways]</h4>""" + '\n'
                + r'<p>Hence $p+q = \mathbf{223}$.</p>'
            ),
        },
    },
]
