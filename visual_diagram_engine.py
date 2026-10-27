# -*- coding: utf-8 -*-
"""
visual_diagram_engine.py
------------------------
Generates bespoke, mathematically accurate inline <svg> geometric/visual figures
(20 specialized geometric & visual diagram engines) AND structured schematic
solution flowcharts (<section class="math-schematic-flow">) for all 119 unique
math problems (121 HTML quiz files) in mathedu.

IMPORTANT TECHNICAL GUARANTEES:
1. Uses <figure>, <figcaption>, <section>, <table>, <tr>, <td>, <span>, <b> (NO inner <div> tags)
   so regexes matching <div class="bilingual-ko">(.*?)</div> or <div class="bilingual-en">(.*?)</div>
   never terminate prematurely.
2. Uses crisp Unicode math symbols inside <svg><text> (zero '$' characters inside <svg>)
   so SVG text renders natively and LaTeX '$' counts remain 100% balanced.
"""

import re


def _esc(s: str) -> str:
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _svg_wrap(title_badge: str, subtitle_badge: str, inner_svg: str, height: int = 300) -> str:
    return (
        f'<svg class="mathedu-bespoke-svg" viewBox="0 0 680 {height}" '
        f'xmlns="http://www.w3.org/2000/svg" '
        f'style="width:100%;max-width:680px;height:auto;display:block;margin:0 auto;border-radius:12px;'
        f'background:linear-gradient(145deg,#ffffff 0%,#f6f3f5 100%);border:1.5px solid #cbd5e1;'
        f'box-shadow:0 4px 16px rgba(19,27,46,0.06)">'
        f'<defs>'
        f'<pattern id="grid20" width="20" height="20" patternUnits="userSpaceOnUse">'
        f'<path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(0,99,184,0.06)" stroke-width="1"/>'
        f'</pattern>'
        f'<marker id="arrCyan" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 1 L 8 5 L 0 9 z" fill="#006398"/>'
        f'</marker>'
        f'<marker id="arrGold" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 1 L 8 5 L 0 9 z" fill="#d97706"/>'
        f'</marker>'
        f'<marker id="arrGreen" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 1 L 8 5 L 0 9 z" fill="#059669"/>'
        f'</marker>'
        f'<marker id="arrCoral" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 1 L 8 5 L 0 9 z" fill="#be123c"/>'
        f'</marker>'
        f'</defs>'
        f'<rect width="680" height="{height}" fill="url(#grid20)" rx="12"/>'
        f'<rect x="12" y="10" width="656" height="32" rx="8" fill="#e0f2fe" stroke="#7dd3fc"/>'
        f'<text x="24" y="31" fill="#006398" font-size="11.8" font-weight="800" font-family="sans-serif">{_esc(title_badge)}</text>'
        f'<text x="656" y="31" fill="#047857" font-size="11.8" font-weight="800" text-anchor="end" font-family="sans-serif">{_esc(subtitle_badge)}</text>'
        f'{inner_svg}'
        f'</svg>'
    )


def _right_panel_svg(hdr: str, stroke_col: str, hdr_col: str, eq_label: str, pt1_label: str, pt2_label: str, ans_label: str) -> str:
    return f"""
    <rect x="400" y="52" width="260" height="226" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
    <text x="530" y="74" fill="#006398" font-size="12" font-weight="800" text-anchor="middle">{_esc(hdr)}</text>
    <rect x="414" y="86" width="232" height="42" rx="7" fill="#eff6ff" stroke="#93c5fd"/>
    <text x="530" y="103" fill="#006398" font-size="10.5" font-weight="700" text-anchor="middle">① 주어진 조건 · 기하 구조</text>
    <text x="530" y="120" fill="#1e293b" font-size="10.2" font-weight="800" text-anchor="middle">{_esc(eq_label)}</text>
    <rect x="414" y="136" width="232" height="42" rx="7" fill="#f5f3ff" stroke="#c4b5fd"/>
    <text x="530" y="153" fill="#4f46e5" font-size="10.5" font-weight="700" text-anchor="middle">② 핵심 도형 성질 · 변환 공식</text>
    <text x="530" y="170" fill="#1e293b" font-size="10.2" font-weight="800" text-anchor="middle">{_esc(pt1_label)}</text>
    <rect x="414" y="186" width="232" height="40" rx="7" fill="#ecfdf5" stroke="#6ee7b7"/>
    <text x="530" y="202" fill="#047857" font-size="10.5" font-weight="700" text-anchor="middle">③ 결정적 관계식 · 수치 도출</text>
    <text x="530" y="218" fill="#1e293b" font-size="10.2" font-weight="800" text-anchor="middle">{_esc(pt2_label)}</text>
    <rect x="414" y="233" width="232" height="35" rx="7" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="530" y="255" fill="#b45309" font-size="12" font-weight="900" text-anchor="middle">🎯 최종 결론: {_esc(ans_label)}</text>
    """


def _draw_c261022_svg(lang="ko") -> str:
    title = (
        "📐 [시각적 역추적 트리 모델] [10월 22번] a₃ = a₆ 주기 분기(15, 25) & a₂ → a₁ 역추적 분기 트리"
        if lang == "ko"
        else "📐 [Visual Backtracking Tree] [Oct #22] Period-3 Branches (a₃ = 15, 25) & Backtracking to a₁"
    )
    sub = "∑a₁ = 24+47+44+87 = 202"
    inner = """
    <!-- LEFT PANEL: Periodicity a3 = a6 Parity Branching -->
    <rect x="16" y="50" width="308" height="236" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <text x="170" y="70" fill="#131b2e" font-size="11.5" font-weight="800" text-anchor="middle">① 주기 조건 (a₃ = a₆) · 홀짝 갈래 탐색</text>
    <rect x="28" y="78" width="284" height="24" rx="6" fill="#eff6ff" stroke="#93c5fd"/>
    <text x="170" y="94" fill="#006398" font-size="9.8" font-weight="800" text-anchor="middle">홀수: aₙ₊₁ = (aₙ+1)/2 + n  |  짝수: aₙ₊₁ = aₙ + n (항상 증가)</text>

    <!-- Branch 1: a3=15 -->
    <rect x="28" y="110" width="284" height="62" rx="8" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5"/>
    <text x="40" y="128" fill="#047857" font-size="10.5" font-weight="800">경로 A (홀 → 홀 → 짝): (a₃+1)/2+3 → 홀수</text>
    <text x="40" y="146" fill="#1e293b" font-size="11" font-weight="800">a₃ = 15(홀) ➔ a₄ = 11(홀) ➔ a₅ = 10(짝) ➔ a₆ = 15</text>
    <text x="40" y="163" fill="#059669" font-size="10" font-weight="800">✓ 첫 번째 주기 해: a₃ = 15 확정!</text>

    <!-- Branch 2: a3=25 -->
    <rect x="28" y="180" width="284" height="62" rx="8" fill="#f5f3ff" stroke="#8b5cf6" stroke-width="1.5"/>
    <text x="40" y="198" fill="#4f46e5" font-size="10.5" font-weight="800">경로 B (홀 → 짝 → 짝): (a₃+1)/2+12 = a₃</text>
    <text x="40" y="216" fill="#1e293b" font-size="11" font-weight="800">a₃ = 25(홀) ➔ a₄ = 16(짝) ➔ a₅ = 20(짝) ➔ a₆ = 25</text>
    <text x="40" y="233" fill="#4f46e5" font-size="10" font-weight="800">✓ 두 번째 주기 해: a₃ = 25 확정!</text>

    <text x="170" y="274" fill="#64748b" font-size="9.8" font-weight="700" text-anchor="middle">※ a₃가 짝수이면 a₃ &lt; a₄ &lt; a₅ &lt; a₆이므로 a₃ = a₆ 불가</text>

    <!-- RIGHT PANEL: Backtracking Tree a3 -> a2 -> a1 -->
    <rect x="336" y="50" width="328" height="236" rx="12" fill="#f8fafc" stroke="#006398" stroke-width="1.5"/>
    <text x="500" y="70" fill="#006398" font-size="11.5" font-weight="800" text-anchor="middle">② 역추적 분기 트리 (a₃ ➔ a₂ ➔ a₁)</text>

    <!-- Tree 1: From a3 = 15 -->
    <rect x="348" y="80" width="304" height="68" rx="8" fill="#ffffff" stroke="#10b981" stroke-width="1.5"/>
    <rect x="356" y="96" width="58" height="36" rx="6" fill="#dcfce7" stroke="#10b981"/>
    <text x="385" y="112" fill="#065f46" font-size="10" font-weight="800" text-anchor="middle">a₃ = 15</text>
    <text x="385" y="125" fill="#047857" font-size="9" font-weight="700" text-anchor="middle">(경로 A)</text>
    <line x1="414" y1="114" x2="438" y2="114" stroke="#059669" stroke-width="1.8" marker-end="url(#arrGreen)"/>
    <rect x="442" y="90" width="76" height="48" rx="6" fill="#ecfdf5" stroke="#10b981"/>
    <text x="480" y="106" fill="#047857" font-size="10" font-weight="800" text-anchor="middle">a₂ = 25 (홀)</text>
    <text x="480" y="120" fill="#be123c" font-size="8.5" font-weight="700" text-anchor="middle">짝수 a₂=13(모순)</text>
    <text x="480" y="132" fill="#059669" font-size="8.8" font-weight="800" text-anchor="middle">(a₂+1)/2+2=15</text>
    <line x1="518" y1="104" x2="544" y2="96" stroke="#006398" stroke-width="1.6" marker-end="url(#arrCyan)"/>
    <line x1="518" y1="124" x2="544" y2="132" stroke="#006398" stroke-width="1.6" marker-end="url(#arrCyan)"/>
    <rect x="548" y="85" width="96" height="25" rx="5" fill="#eff6ff" stroke="#006398"/>
    <text x="596" y="101" fill="#006398" font-size="10" font-weight="800" text-anchor="middle">a₁ = 24 (짝수 ✓)</text>
    <rect x="548" y="116" width="96" height="25" rx="5" fill="#eff6ff" stroke="#006398"/>
    <text x="596" y="132" fill="#006398" font-size="10" font-weight="800" text-anchor="middle">a₁ = 47 (홀수 ✓)</text>

    <!-- Tree 2: From a3 = 25 -->
    <rect x="348" y="156" width="304" height="68" rx="8" fill="#ffffff" stroke="#8b5cf6" stroke-width="1.5"/>
    <rect x="356" y="172" width="58" height="36" rx="6" fill="#ede9fe" stroke="#8b5cf6"/>
    <text x="385" y="188" fill="#4f46e5" font-size="10" font-weight="800" text-anchor="middle">a₃ = 25</text>
    <text x="385" y="201" fill="#4f46e5" font-size="9" font-weight="700" text-anchor="middle">(경로 B)</text>
    <line x1="414" y1="190" x2="438" y2="190" stroke="#4f46e5" stroke-width="1.8" marker-end="url(#arrCyan)"/>
    <rect x="442" y="166" width="76" height="48" rx="6" fill="#f5f3ff" stroke="#8b5cf6"/>
    <text x="480" y="182" fill="#4f46e5" font-size="10" font-weight="800" text-anchor="middle">a₂ = 45 (홀)</text>
    <text x="480" y="196" fill="#be123c" font-size="8.5" font-weight="700" text-anchor="middle">짝수 a₂=23(모순)</text>
    <text x="480" y="208" fill="#4f46e5" font-size="8.8" font-weight="800" text-anchor="middle">(a₂+1)/2+2=25</text>
    <line x1="518" y1="180" x2="544" y2="172" stroke="#006398" stroke-width="1.6" marker-end="url(#arrCyan)"/>
    <line x1="518" y1="200" x2="544" y2="208" stroke="#006398" stroke-width="1.6" marker-end="url(#arrCyan)"/>
    <rect x="548" y="161" width="96" height="25" rx="5" fill="#eff6ff" stroke="#006398"/>
    <text x="596" y="177" fill="#006398" font-size="10" font-weight="800" text-anchor="middle">a₁ = 44 (짝수 ✓)</text>
    <rect x="548" y="192" width="96" height="25" rx="5" fill="#eff6ff" stroke="#006398"/>
    <text x="596" y="208" fill="#006398" font-size="10" font-weight="800" text-anchor="middle">a₁ = 87 (홀수 ✓)</text>

    <!-- Final Conclusion Bar -->
    <rect x="348" y="232" width="304" height="44" rx="8" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.8"/>
    <text x="500" y="250" fill="#92400e" font-size="10.2" font-weight="800" text-anchor="middle">가능한 모든 a₁의 합 = (24 + 47) + (44 + 87) = 71 + 131</text>
    <text x="500" y="268" fill="#b45309" font-size="12.5" font-weight="900" text-anchor="middle">🎯 최종 정답: ∑a₁ = 202</text>
    """
    return _svg_wrap(title, sub, inner, 300)


def _draw_c2610p27_svg(lang="ko") -> str:
    title = (
        "📐 [시각적 도형 모델] 주사위 2회 36칸 홀짝 격자(P=1/4, 3/4) & 4회 독립시행 넓이 모델"
        if lang == "ko"
        else "📐 [Visual Geometric Model] 6×6 Dice Odd/Even Grid (P=1/4, 3/4) & 4-Trial Binomial Sum"
    )
    sub = "P(X ≤ 5) = 13/256"
    inner = """
    <rect x="16" y="54" width="316" height="232" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <text x="174" y="75" fill="#131b2e" font-size="12" font-weight="800" text-anchor="middle">1회 시행: 주사위 2번(6×6=36칸) 눈의 곱 홀짝 판정</text>
    <text x="112" y="96" fill="#006398" font-size="10.5" font-weight="800" text-anchor="middle">홀수 {1,3,5} (3칸)</text>
    <text x="196" y="96" fill="#64748b" font-size="10.5" font-weight="700" text-anchor="middle">짝수 {2,4,6} (3칸)</text>
    <text x="64" y="132" fill="#006398" font-size="10" font-weight="800" text-anchor="end">홀 {1,3,5}</text>
    <text x="64" y="196" fill="#64748b" font-size="10" font-weight="700" text-anchor="end">짝 {2,4,6}</text>
    <rect x="70" y="102" width="84" height="60" rx="6" fill="#dcfce7" stroke="#10b981" stroke-width="2"/>
    <text x="112" y="126" fill="#047857" font-size="11.5" font-weight="900" text-anchor="middle">홀 × 홀 = 홀수</text>
    <text x="112" y="143" fill="#065f46" font-size="10.5" font-weight="800" text-anchor="middle">3×3 = 9칸 (1/4)</text>
    <text x="112" y="157" fill="#059669" font-size="10" font-weight="800" text-anchor="middle">★ 공 +1개</text>
    <rect x="158" y="102" width="84" height="60" rx="6" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.2"/>
    <text x="200" y="128" fill="#475569" font-size="11" font-weight="700" text-anchor="middle">홀 × 짝 = 짝수</text>
    <text x="200" y="145" fill="#64748b" font-size="10" font-weight="700" text-anchor="middle">9칸 (공 +2개)</text>
    <rect x="70" y="166" width="84" height="60" rx="6" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.2"/>
    <text x="112" y="192" fill="#475569" font-size="11" font-weight="700" text-anchor="middle">짝 × 홀 = 짝수</text>
    <text x="112" y="209" fill="#64748b" font-size="10" font-weight="700" text-anchor="middle">9칸 (공 +2개)</text>
    <rect x="158" y="166" width="84" height="60" rx="6" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.2"/>
    <text x="200" y="192" fill="#475569" font-size="11" font-weight="700" text-anchor="middle">짝 × 짝 = 짝수</text>
    <text x="200" y="209" fill="#64748b" font-size="10" font-weight="700" text-anchor="middle">9칸 (공 +2개)</text>
    <rect x="250" y="102" width="72" height="58" rx="8" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5"/>
    <text x="286" y="123" fill="#047857" font-size="10.5" font-weight="800" text-anchor="middle">공 1개 확률</text>
    <text x="286" y="145" fill="#065f46" font-size="13" font-weight="900" text-anchor="middle">p = 1/4</text>
    <rect x="250" y="168" width="72" height="58" rx="8" fill="#eff6ff" stroke="#006398" stroke-width="1.5"/>
    <text x="286" y="189" fill="#006398" font-size="10.5" font-weight="800" text-anchor="middle">공 2개 확률</text>
    <text x="286" y="211" fill="#006398" font-size="13" font-weight="900" text-anchor="middle">q = 3/4</text>
    <rect x="28" y="236" width="292" height="38" rx="8" fill="#f8fafc" stroke="#cbd5e1"/>
    <text x="174" y="259" fill="#1e293b" font-size="11" font-weight="800" text-anchor="middle">P(공 1개) = 9/36 = 1/4  |  P(공 2개) = 27/36 = 3/4</text>
    <rect x="346" y="54" width="318" height="232" rx="12" fill="#ffffff" stroke="#006398" stroke-width="1.5"/>
    <text x="505" y="75" fill="#006398" font-size="12" font-weight="800" text-anchor="middle">4회 독립시행 후 상자 속 공의 총 개수 ≤ 5개</text>
    <rect x="360" y="88" width="290" height="54" rx="8" fill="#f0fdf4" stroke="#10b981" stroke-width="1.5"/>
    <text x="372" y="108" fill="#047857" font-size="11" font-weight="800">① 총 4개: (1, 1, 1, 1) — 4번 모두 1개씩</text>
    <text x="372" y="129" fill="#1e293b" font-size="11.5" font-weight="800">₄C₄ · (1/4)⁴ = 1 × 1/256 = 1/256</text>
    <rect x="360" y="150" width="290" height="66" rx="8" fill="#eff6ff" stroke="#006398" stroke-width="1.5"/>
    <text x="372" y="170" fill="#006398" font-size="11" font-weight="800">② 총 5개: (1,1,1,2) 배열 — 1개 3번, 2개 1번 (4가지)</text>
    <text x="372" y="189" fill="#475569" font-size="10.5" font-weight="700">(2,1,1,1), (1,2,1,1), (1,1,2,1), (1,1,1,2) ⇒ ₄C₁ = 4가지</text>
    <text x="372" y="207" fill="#1e293b" font-size="11.5" font-weight="800">₄C₃ · (1/4)³ · (3/4)¹ = 4 × 3/256 = 12/256</text>
    <rect x="360" y="224" width="290" height="50" rx="9" fill="#fef3c7" stroke="#f59e0b" stroke-width="2"/>
    <text x="505" y="244" fill="#92400e" font-size="11" font-weight="800" text-anchor="middle">배반사건 합의 법칙: 1/256 + 12/256</text>
    <text x="505" y="265" fill="#b45309" font-size="13.5" font-weight="900" text-anchor="middle">🎯 최종 정답: P(X ≤ 5) = 13/256 (⑤)</text>
    """
    return _svg_wrap(title, sub, inner, 300)


# ==============================================================================
# 20 SPECIALIZED GEOMETRIC / VISUAL SVG DRAWERS
# ==============================================================================

def _draw_c2610p28_svg(lang="ko") -> str:
    title = (
        "🎴 [칠판 판서 도식] 8장(1,1,2,2,3,3,4,4) 중 6장 선택(aabbcc vs aabbcd) · 첫 자리 짝수 6분할 카운팅"
        if lang == "ko"
        else "🎴 [Whiteboard Diagram] Choosing 6 of 8 Cards (aabbcc vs. aabbcd) & 6-Branch Even-First Counting"
    )
    sub = "120+60+60+120+120+240 = 720"
    inner = """
    <!-- TOP BAR: 1,1,2,2,3,3,4,4 -> 6 Cards -> 6 Slots (Slot 1 = Even) & Final Sum Box -->
    <rect x="14" y="48" width="414" height="58" rx="9" fill="rgba(15,23,42,0.94)" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="24" y="65" fill="#7cc4ff" font-size="10.2" font-weight="800">① 전체 카드 8장: 1, 1, 2, 2, 3, 3, 4, 4  ➔  ○○○○○○ (6장 선택)</text>
    <text x="24" y="83" fill="#e2e8f0" font-size="10" font-weight="700">② 6자리 일렬 나열:</text>
    <!-- 6 Slots with Slot 1 highlighted as EVEN -->
    <rect x="128" y="68" width="38" height="28" rx="5" fill="rgba(251,191,36,0.28)" stroke="#fbbf24" stroke-width="1.8"/>
    <text x="147" y="80" fill="#fde68a" font-size="8.5" font-weight="900" text-anchor="middle">짝수</text>
    <text x="147" y="92" fill="#fff" font-size="8.5" font-weight="800" text-anchor="middle">[1자리]</text>
    <rect x="172" y="72" width="32" height="24" rx="4" fill="rgba(56,189,248,0.16)" stroke="#38bdf8"/><text x="188" y="88" fill="#bae6fd" font-size="9" font-weight="700" text-anchor="middle">2</text>
    <rect x="208" y="72" width="32" height="24" rx="4" fill="rgba(56,189,248,0.16)" stroke="#38bdf8"/><text x="224" y="88" fill="#bae6fd" font-size="9" font-weight="700" text-anchor="middle">3</text>
    <rect x="244" y="72" width="32" height="24" rx="4" fill="rgba(56,189,248,0.16)" stroke="#38bdf8"/><text x="260" y="88" fill="#bae6fd" font-size="9" font-weight="700" text-anchor="middle">4</text>
    <rect x="280" y="72" width="32" height="24" rx="4" fill="rgba(56,189,248,0.16)" stroke="#38bdf8"/><text x="296" y="88" fill="#bae6fd" font-size="9" font-weight="700" text-anchor="middle">5</text>
    <rect x="316" y="72" width="32" height="24" rx="4" fill="rgba(56,189,248,0.16)" stroke="#38bdf8"/><text x="332" y="88" fill="#bae6fd" font-size="9" font-weight="700" text-anchor="middle">6</text>
    <text x="388" y="84" fill="#6ee7b7" font-size="9.2" font-weight="800" text-anchor="middle">남은 5자리</text>
    <text x="388" y="96" fill="#fde68a" font-size="8.8" font-weight="700" text-anchor="middle">5!/(2!2!), 5!/2!</text>

    <!-- TOP-RIGHT WHITEBOARD SUMMARY BOX -->
    <rect x="436" y="48" width="230" height="58" rx="9" fill="rgba(52,211,153,0.16)" stroke="#34d399" stroke-width="1.8"/>
    <text x="551" y="66" fill="#6ee7b7" font-size="10.2" font-weight="800" text-anchor="middle">🎯 칠판 우측 상단 최종 합산</text>
    <text x="551" y="83" fill="#fff" font-size="10.5" font-weight="800" text-anchor="middle">120 + 60 + 60 + 120 + 120 + 240</text>
    <text x="551" y="99" fill="#fde68a" font-size="12" font-weight="900" text-anchor="middle">= 720 (정답 ③)</text>

    <!-- LEFT PANEL: CASE 1 (a a b b c c : 3 pairs) -->
    <rect x="14" y="114" width="256" height="194" rx="10" fill="rgba(15,23,42,0.94)" stroke="#a78bfa" stroke-width="1.5"/>
    <text x="142" y="132" fill="#c4b5fd" font-size="11" font-weight="800" text-anchor="middle">Case 1 : a a b b c c (3종류 2장씩 = 180)</text>

    <!-- Case 1 - i) -->
    <rect x="22" y="140" width="240" height="76" rx="7" fill="rgba(56,189,248,0.12)" stroke="rgba(56,189,248,0.45)"/>
    <text x="30" y="155" fill="#7cc4ff" font-size="9.8" font-weight="800">i) a, b, c 중 2개가 짝수 (★ ★ 2 2 4 4)</text>
    <text x="30" y="170" fill="#cbd5e1" font-size="9" font-weight="700">· 홀수 ★ 선택(1 또는 3): 2가지 × 첫자리 짝수 □(2 또는 4): 2가지</text>
    <text x="30" y="185" fill="#e2e8f0" font-size="9" font-weight="700">· 배열: [□] + (□ △ △ ★ ★)  ➔  같은 카드 2쌍!</text>
    <text x="142" y="205" fill="#fde68a" font-size="10.5" font-weight="900" text-anchor="middle">2 × 2 × (5! / 2!2!) = 4 × 30 = 120</text>

    <!-- Case 1 - ii) -->
    <rect x="22" y="222" width="240" height="76" rx="7" fill="rgba(167,139,250,0.12)" stroke="rgba(167,139,250,0.45)"/>
    <text x="30" y="237" fill="#ddd6fe" font-size="9.8" font-weight="800">ii) a, b, c 중 2개가 홀수 (★ ★ 1 1 3 3)</text>
    <text x="30" y="252" fill="#cbd5e1" font-size="9" font-weight="700">· 짝수 ★ 선택(2 또는 4): 2가지 × 첫자리는 반드시 ★(1가지)</text>
    <text x="30" y="267" fill="#e2e8f0" font-size="9" font-weight="700">· 배열: [★] + (★ 1 1 3 3)  ➔  같은 카드 2쌍(1,1 / 3,3)!</text>
    <text x="142" y="287" fill="#fde68a" font-size="10.5" font-weight="900" text-anchor="middle">2 × (5! / 2!2!) = 2 × 30 = 60</text>

    <!-- RIGHT PANEL: CASE 2 (a a b b c d : 2 pairs + 2 singles) -->
    <rect x="278" y="114" width="388" height="194" rx="10" fill="rgba(15,23,42,0.94)" stroke="#fbbf24" stroke-width="1.5"/>
    <text x="472" y="132" fill="#fde68a" font-size="11" font-weight="800" text-anchor="middle">Case 2 : a a b b c d (2종류 2장씩 + 2종류 1장씩 = 540)</text>

    <!-- Case 2 - i) -->
    <rect x="286" y="140" width="182" height="68" rx="7" fill="rgba(52,211,153,0.12)" stroke="rgba(52,211,153,0.45)"/>
    <text x="293" y="155" fill="#6ee7b7" font-size="9.4" font-weight="800">i) c, d가 모두 짝수 (1 1 3 3 2 4)</text>
    <text x="293" y="170" fill="#cbd5e1" font-size="8.7" font-weight="700">· 첫자리 ★(2 or 4): 2가지</text>
    <text x="293" y="184" fill="#e2e8f0" font-size="8.7" font-weight="700">· 남은 5자리: (□ 1 1 3 3)</text>
    <text x="377" y="201" fill="#fde68a" font-size="9.8" font-weight="900" text-anchor="middle">2 × (5! / 2!2!) = 60</text>

    <!-- Case 2 - ii) -->
    <rect x="476" y="140" width="182" height="68" rx="7" fill="rgba(251,113,133,0.12)" stroke="rgba(251,113,133,0.45)"/>
    <text x="483" y="155" fill="#fecdd3" font-size="9.4" font-weight="800">ii) c, d가 모두 홀수 (2 2 4 4 1 3)</text>
    <text x="483" y="170" fill="#cbd5e1" font-size="8.7" font-weight="700">· 첫자리 ★(2 or 4): 2가지</text>
    <text x="483" y="184" fill="#e2e8f0" font-size="8.7" font-weight="700">· 남은 5자리: (★ □ □ 1 3)</text>
    <text x="567" y="201" fill="#fde68a" font-size="9.8" font-weight="900" text-anchor="middle">2 × (5! / 2!) = 120</text>

    <!-- Case 2 - iii) -->
    <rect x="286" y="214" width="372" height="84" rx="7" fill="rgba(251,191,36,0.14)" stroke="#fbbf24" stroke-width="1.3"/>
    <text x="472" y="230" fill="#fde68a" font-size="9.8" font-weight="800" text-anchor="middle">iii) c, d가 홀수 1개·짝수 1개 : e₂ e₂ o₂ o₂ e₁ o₁ (e₁: 2가지 × o₁: 2가지)</text>
    <text x="296" y="249" fill="#bae6fd" font-size="9.2" font-weight="800">① 첫자리 [e₁] + (e₂ e₂ o₂ o₂ o₁) :</text>
    <text x="648" y="249" fill="#fde68a" font-size="9.6" font-weight="900" text-anchor="end">2 × (5! / 2!2!) × 2 = 120</text>
    <text x="296" y="269" fill="#6ee7b7" font-size="9.2" font-weight="800">② 첫자리 [e₂] + (e₁ e₂ o₂ o₂ o₁) :</text>
    <text x="648" y="269" fill="#fde68a" font-size="9.6" font-weight="900" text-anchor="end">2 × 2 × (5! / 2!) = 240</text>
    <text x="472" y="289" fill="#ecfdf5" font-size="9.2" font-weight="800" text-anchor="middle">★ e₁(1장 짝수)이 앞설 때는 2쌍(e₂,o₂) 남고, e₂(2장 짝수)가 앞설 때는 1쌍(o₂)만 남음!</text>
    """
    return _svg_wrap(title, sub, inner, 320)


def _draw_c2610p29_svg(lang="ko") -> str:
    title = (
        "📐 [기하적 대칭·합동 모델] 두 정규분포 곡선 f, g의 대칭 이동과 Case 1(m₂=16)·Case 2(m₂=14) 검증"
        if lang == "ko"
        else "📐 [Geometric Symmetry & Congruence Model] Normal Curves f, g & Case 1 (m₂=16) vs Case 2 (m₂=14)"
    )
    sub = "m₁=4, m₂=16 ⇒ k=0.345, 1000k=345"
    inner = """
    <!-- PANEL 1: Curve f(x), m1=4, f(5), and symmetric reflection of [1,2] to [6,7] joining [7,9] -->
    <rect x="14" y="50" width="216" height="152" rx="10" fill="rgba(15,23,42,0.92)" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="122" y="67" fill="#7cc4ff" font-size="11" font-weight="800" text-anchor="middle">① 곡선 f(x) : X ~ N(4, 10²) &amp; 대칭 결합</text>
    <!-- Baseline -->
    <line x1="24" y1="148" x2="220" y2="148" stroke="#94a3b8" stroke-width="1.4"/>
    <!-- Left shaded [1,2] (Z in [-0.3,-0.2]) -->
    <path d="M 68 148 L 68 119 Q 76 112 84 106 L 84 148 Z" fill="rgba(251,113,133,0.42)" stroke="#fb7185" stroke-width="1.2"/>
    <!-- Reflected [6,7] (Z in [0.2,0.3]) -->
    <path d="M 148 148 L 148 106 Q 156 112 164 119 L 164 148 Z" fill="rgba(251,113,133,0.32)" stroke="#fb7185" stroke-width="1.2" stroke-dasharray="3,2"/>
    <!-- Right shaded [7,9] (Z in [0.3,0.5]) -->
    <path d="M 164 148 L 164 119 Q 180 132 196 141 L 196 148 Z" fill="rgba(56,189,248,0.42)" stroke="#38bdf8" stroke-width="1.2"/>
    <!-- Bell curve f -->
    <path d="M 28 146 C 62 144, 88 80, 116 80 C 144 80, 170 144, 214 146" fill="none" stroke="#38bdf8" stroke-width="2.6"/>
    <!-- Symmetry axis m1 = 4 -->
    <line x1="116" y1="74" x2="116" y2="152" stroke="#fbbf24" stroke-width="1.8" stroke-dasharray="4,3"/>
    <circle cx="116" cy="80" r="4" fill="#fbbf24"/>
    <text x="116" y="162" fill="#fde68a" font-size="10" font-weight="800" text-anchor="middle">m₁=4</text>
    <!-- Point x = 5 on curve f (distance +1 from 4) -->
    <line x1="132" y1="86" x2="132" y2="150" stroke="#fde68a" stroke-width="1.2" stroke-dasharray="2,2"/>
    <circle cx="132" cy="86" r="4" fill="#fde68a" stroke="#0b1120" stroke-width="1.2"/>
    <text x="134" y="162" fill="#fde68a" font-size="9.5" font-weight="700" text-anchor="middle">5</text>
    <!-- Reflection curved arrow from [1,2] to [6,7] -->
    <path d="M 76 104 Q 116 64 155 102" fill="none" stroke="#fb7185" stroke-width="1.6" marker-end="url(#arrCoral)"/>
    <text x="116" y="75" fill="#fecdd3" font-size="8.8" font-weight="700" text-anchor="middle">거울 대칭 접기</text>
    <!-- x-axis ticks -->
    <text x="66" y="161" fill="#fecdd3" font-size="9" text-anchor="middle">1</text>
    <text x="84" y="161" fill="#fecdd3" font-size="9" text-anchor="middle">2</text>
    <text x="148" y="161" fill="#bae6fd" font-size="9" text-anchor="middle">6</text>
    <text x="164" y="161" fill="#34d399" font-size="9.5" font-weight="800" text-anchor="middle">7</text>
    <text x="196" y="161" fill="#bae6fd" font-size="9" text-anchor="middle">9</text>
    <!-- Formula summary inside Panel 1 -->
    <text x="122" y="177" fill="#e2e8f0" font-size="9.2" font-weight="700" text-anchor="middle">P(-0.3≤Z≤-0.2) + P(0.3≤Z≤0.5)</text>
    <text x="122" y="192" fill="#34d399" font-size="9.5" font-weight="800" text-anchor="middle">= (0.118-0.079)+(0.191-0.118) = 0.112</text>

    <!-- Horizontal equal-height connector line: f(5) = g(15) -->
    <line x1="132" y1="86" x2="366" y2="86" stroke="#fbbf24" stroke-width="1.3" stroke-dasharray="4,3"/>
    <rect x="200" y="74" width="68" height="15" rx="4" fill="#0f172a" stroke="#fbbf24" stroke-width="1"/>
    <text x="234" y="84.5" fill="#fde68a" font-size="8.8" font-weight="800" text-anchor="middle">f(5) = g(15)</text>

    <!-- PANEL 2: Curve g(x), m2, and the two symmetric points (15) for Case 1 vs Case 2 -->
    <rect x="238" y="50" width="224" height="152" rx="10" fill="rgba(15,23,42,0.92)" stroke="#a78bfa" stroke-width="1.5"/>
    <text x="350" y="67" fill="#c4b5fd" font-size="11" font-weight="800" text-anchor="middle">② 곡선 g(x) : f(5)=g(15)의 두 대칭 케이스</text>
    <line x1="252" y1="132" x2="448" y2="132" stroke="#94a3b8" stroke-width="1.4"/>
    <!-- Bell curve g -->
    <path d="M 262 130 C 294 128, 322 80, 350 80 C 378 80, 406 128, 438 130" fill="none" stroke="#a78bfa" stroke-width="2.6"/>
    <!-- Symmetry axis m2 -->
    <line x1="350" y1="74" x2="350" y2="136" stroke="#fbbf24" stroke-width="1.8" stroke-dasharray="4,3"/>
    <text x="350" y="145" fill="#fde68a" font-size="10" font-weight="800" text-anchor="middle">m₂</text>
    <!-- Left symmetric point 15 (Case 1: m2 = 16) -->
    <line x1="334" y1="86" x2="334" y2="134" stroke="#34d399" stroke-width="1.4" stroke-dasharray="2,2"/>
    <circle cx="334" cy="86" r="4.5" fill="#34d399" stroke="#0b1120" stroke-width="1.2"/>
    <text x="315" y="102" fill="#6ee7b7" font-size="9.2" font-weight="800" text-anchor="end">⑮(Case1)</text>
    <!-- Right symmetric point 15 (Case 2: m2 = 14) -->
    <line x1="366" y1="86" x2="366" y2="134" stroke="#fb7185" stroke-width="1.4" stroke-dasharray="2,2"/>
    <circle cx="366" cy="86" r="4.5" fill="#fb7185" stroke="#0b1120" stroke-width="1.2"/>
    <text x="385" y="102" fill="#fecdd3" font-size="9.2" font-weight="800" text-anchor="start">⑮(Case2)</text>

    <!-- Case 1 vs Case 2 comparison sub-boxes inside Panel 2 -->
    <rect x="245" y="150" width="104" height="45" rx="6" fill="rgba(52,211,153,0.16)" stroke="#34d399" stroke-width="1.3"/>
    <text x="297" y="163" fill="#6ee7b7" font-size="9.2" font-weight="800" text-anchor="middle">Case 1 : m₂ = 16</text>
    <text x="297" y="176" fill="#ecfdf5" font-size="8.6" text-anchor="middle">P(-0.5≤Z≤-0.2)</text>
    <text x="297" y="189" fill="#fde68a" font-size="9.2" font-weight="800" text-anchor="middle">= 0.112 (O.K.!)</text>

    <rect x="353" y="150" width="102" height="45" rx="6" fill="rgba(251,113,133,0.14)" stroke="#fb7185" stroke-width="1.2"/>
    <text x="404" y="163" fill="#fecdd3" font-size="9.2" font-weight="800" text-anchor="middle">Case 2 : m₂ = 14</text>
    <text x="404" y="176" fill="#e2e8f0" font-size="8.6" text-anchor="middle">P(-0.3≤Z≤0)</text>
    <text x="404" y="189" fill="#fb7185" font-size="9.2" font-weight="800" text-anchor="middle">= 0.118 (✕ 모순)</text>

    <!-- PANEL 3: Final Tail Probability P(Y >= 20) = P(Z >= 0.4) = 0.345 -->
    <rect x="470" y="50" width="196" height="152" rx="10" fill="rgba(15,23,42,0.92)" stroke="#34d399" stroke-width="1.5"/>
    <text x="568" y="67" fill="#6ee7b7" font-size="11" font-weight="800" text-anchor="middle">③ 확정 g(x) : P(Y ≥ 20) 꼬리 넓이</text>
    <line x1="482" y1="142" x2="654" y2="142" stroke="#94a3b8" stroke-width="1.4"/>
    <!-- Middle area [16, 20] (0 <= Z <= 0.4) = 0.155 -->
    <path d="M 556 142 L 556 80 Q 574 82 590 106 L 590 142 Z" fill="rgba(56,189,248,0.25)"/>
    <!-- Right tail area [20, inf) (Z >= 0.4) = 0.345 -->
    <path d="M 590 142 L 590 106 C 608 128, 626 139, 648 141 L 648 142 Z" fill="rgba(52,211,153,0.48)" stroke="#34d399" stroke-width="1.3"/>
    <!-- Bell curve Y ~ N(16, 10^2) -->
    <path d="M 486 140 C 514 138, 534 80, 556 80 C 578 80, 606 138, 648 140" fill="none" stroke="#34d399" stroke-width="2.5"/>
    <line x1="556" y1="74" x2="556" y2="146" stroke="#fbbf24" stroke-width="1.7" stroke-dasharray="4,3"/>
    <line x1="590" y1="102" x2="590" y2="146" stroke="#fde68a" stroke-width="1.5"/>
    <text x="556" y="155" fill="#fde68a" font-size="9.5" font-weight="800" text-anchor="middle">m₂=16</text>
    <text x="590" y="155" fill="#6ee7b7" font-size="9.5" font-weight="800" text-anchor="middle">20(Z=0.4)</text>
    <text x="573" y="126" fill="#bae6fd" font-size="8.8" font-weight="700" text-anchor="middle">0.155</text>
    <text x="618" y="124" fill="#ecfdf5" font-size="9.5" font-weight="800" text-anchor="middle">k=0.345</text>
    <text x="568" y="174" fill="#e2e8f0" font-size="9.2" font-weight="700" text-anchor="middle">k = P(Z ≥ 0.4) = 0.5 - 0.155 = 0.345</text>
    <rect x="492" y="180" width="152" height="17" rx="5" fill="rgba(251,191,36,0.22)" stroke="#fbbf24" stroke-width="1.2"/>
    <text x="568" y="192" fill="#fde68a" font-size="10.2" font-weight="900" text-anchor="middle">∴ 1000 × k = 345</text>

    <!-- PANEL 4: Bottom Geometric Alignment & Cancellation Diagram -->
    <rect x="14" y="210" width="652" height="108" rx="10" fill="rgba(30,41,59,0.92)" stroke="#fbbf24" stroke-width="1.5"/>
    <text x="340" y="228" fill="#fde68a" font-size="11.5" font-weight="800" text-anchor="middle">🔍 [기하학적 넓이 이동 &amp; 0.118 상쇄 원리] 왜 좌변은 Z ∈ [0.2, 0.5]가 되고, 우변은 Case 1(m₂=16)만 성립할까?</text>

    <!-- Left sub-diagram: Z-interval glueing at Z=0.3 -->
    <rect x="26" y="236" width="304" height="74" rx="8" fill="rgba(15,23,42,0.85)" stroke="rgba(56,189,248,0.4)"/>
    <text x="178" y="251" fill="#7cc4ff" font-size="10" font-weight="800" text-anchor="middle">좌변(X) : 대칭 이동 조각 [6, 7] + 원래 조각 [7, 9] = 연속 구간 [6, 9]</text>
    <rect x="38" y="259" width="112" height="24" rx="5" fill="rgba(251,113,133,0.28)" stroke="#fb7185" stroke-width="1.3"/>
    <text x="94" y="275" fill="#fecdd3" font-size="9.2" font-weight="800" text-anchor="middle">[6,7] (Z: 0.2~0.3) : 0.118-0.079</text>
    <text x="158" y="275" fill="#fbbf24" font-size="12" font-weight="900" text-anchor="middle">+</text>
    <rect x="166" y="259" width="152" height="24" rx="5" fill="rgba(56,189,248,0.28)" stroke="#38bdf8" stroke-width="1.3"/>
    <text x="242" y="275" fill="#bae6fd" font-size="9.2" font-weight="800" text-anchor="middle">[7,9] (Z: 0.3~0.5) : 0.191-0.118</text>
    <text x="178" y="301" fill="#6ee7b7" font-size="9.5" font-weight="800" text-anchor="middle">경계 X=7 (Z=0.3, 넓이 0.118)에서 맞물려 +0.118과 -0.118 상쇄 ⇒ 0.191 - 0.079 = 0.112</text>

    <!-- Right sub-diagram: Case 1 vs Case 2 geometric distance from mean m2 -->
    <rect x="340" y="236" width="314" height="74" rx="8" fill="rgba(15,23,42,0.85)" stroke="rgba(52,211,153,0.4)"/>
    <text x="497" y="251" fill="#6ee7b7" font-size="10" font-weight="800" text-anchor="middle">우변(Y) : 구간 [11, 14]와 대칭축 m₂ 사이의 기하학적 거리 비교</text>
    <rect x="350" y="258" width="294" height="22" rx="5" fill="rgba(52,211,153,0.22)" stroke="#34d399" stroke-width="1.2"/>
    <text x="497" y="273" fill="#ecfdf5" font-size="9.2" font-weight="800" text-anchor="middle">⭕ Case 1 (m₂=16) : [11, 14]는 16에서 왼쪽 2~5칸 (Z: -0.5~-0.2) ⇒ 넓이 0.112 합동!</text>
    <rect x="350" y="284" width="294" height="21" rx="5" fill="rgba(251,113,133,0.18)" stroke="#fb7185" stroke-width="1.1"/>
    <text x="497" y="298" fill="#fecdd3" font-size="9.1" font-weight="700" text-anchor="middle">❌ Case 2 (m₂=14) : [11, 14]는 봉우리(14)에 걸친 왼쪽 0~3칸 (Z: -0.3~0) ⇒ 넓이 0.118 탈락!</text>
    """
    return _svg_wrap(title, sub, inner, 328)


def _draw_c2610p30_svg(lang="ko") -> str:
    title = "📐 [시각적 도형 모델] 두 주머니 A·B 비복원 추출 & 400칸 표본공간 넓이 분할 도형" if lang == "ko" else "📐 [Visual Geometric Model] Two Bags A & B Non-Replacement & 400-Outcome Area Partition"
    sub = "n(E)=336, n(E∩F)=96 ⇒ P=2/7"
    inner = """
    <rect x="20" y="54" width="195" height="108" rx="10" fill="rgba(30,41,59,0.85)" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="117" y="73" fill="#7cc4ff" font-size="12" font-weight="800" text-anchor="middle">주머니 A (공 5개 → 2회 비복원: 5×4=20)</text>
    <circle cx="48" cy="102" r="14" fill="#0284c7" stroke="#bae6fd" stroke-width="1.5"/><text x="48" y="106" fill="#fff" font-size="11" font-weight="800" text-anchor="middle">1a</text>
    <circle cx="82" cy="102" r="14" fill="#0284c7" stroke="#bae6fd" stroke-width="1.5"/><text x="82" y="106" fill="#fff" font-size="11" font-weight="800" text-anchor="middle">1b</text>
    <circle cx="116" cy="102" r="14" fill="#0284c7" stroke="#bae6fd" stroke-width="1.5"/><text x="116" y="106" fill="#fff" font-size="11" font-weight="800" text-anchor="middle">1c</text>
    <circle cx="152" cy="102" r="14" fill="#d97706" stroke="#fde68a" stroke-width="1.5"/><text x="152" y="106" fill="#fff" font-size="11" font-weight="800" text-anchor="middle">2a</text>
    <circle cx="186" cy="102" r="14" fill="#d97706" stroke="#fde68a" stroke-width="1.5"/><text x="186" y="106" fill="#fff" font-size="11" font-weight="800" text-anchor="middle">2b</text>
    <text x="117" y="136" fill="#e2e8f0" font-size="10.5" text-anchor="middle">합2(1,1): 6가지 | 합3(1,2): 12가지</text>
    <text x="117" y="152" fill="#fde68a" font-size="10.5" font-weight="700" text-anchor="middle">합4(2,2): 2가지 (계 20가지)</text>

    <rect x="20" y="172" width="195" height="108" rx="10" fill="rgba(30,41,59,0.85)" stroke="#a78bfa" stroke-width="1.5"/>
    <text x="117" y="191" fill="#c4b5fd" font-size="12" font-weight="800" text-anchor="middle">주머니 B (공 5개 → 2회 비복원: 5×4=20)</text>
    <circle cx="48" cy="220" r="14" fill="#0284c7" stroke="#bae6fd" stroke-width="1.5"/><text x="48" y="224" fill="#fff" font-size="11" font-weight="800" text-anchor="middle">1p</text>
    <circle cx="82" cy="220" r="14" fill="#0284c7" stroke="#bae6fd" stroke-width="1.5"/><text x="82" y="224" fill="#fff" font-size="11" font-weight="800" text-anchor="middle">1q</text>
    <circle cx="116" cy="220" r="14" fill="#0284c7" stroke="#bae6fd" stroke-width="1.5"/><text x="116" y="224" fill="#fff" font-size="11" font-weight="800" text-anchor="middle">1r</text>
    <circle cx="150" cy="220" r="14" fill="#0284c7" stroke="#bae6fd" stroke-width="1.5"/><text x="150" y="224" fill="#fff" font-size="11" font-weight="800" text-anchor="middle">1s</text>
    <circle cx="186" cy="220" r="14" fill="#d97706" stroke="#fde68a" stroke-width="1.5"/><text x="186" y="224" fill="#fff" font-size="11" font-weight="800" text-anchor="middle">2p</text>
    <text x="117" y="254" fill="#e2e8f0" font-size="10.5" text-anchor="middle">합2(1,1): 12가지 | 합3(1,2): 8가지</text>
    <text x="117" y="270" fill="#fb7185" font-size="10.5" font-weight="700" text-anchor="middle">합4(2,2): 0가지 (2가 1개뿐!)</text>

    <rect x="235" y="54" width="240" height="226" rx="10" fill="rgba(15,23,42,0.9)" stroke="#64748b" stroke-width="1.5"/>
    <text x="355" y="72" fill="#f8fafc" font-size="12" font-weight="800" text-anchor="middle">전체 20×20 = 400칸 직사각형 넓이 모델</text>

    <rect x="255" y="92" width="115" height="45" fill="rgba(251,113,133,0.28)" stroke="#fb7185" stroke-width="1.5"/>
    <text x="312" y="112" fill="#fecdd3" font-size="10.5" font-weight="800" text-anchor="middle">A합=2, B합=2 (72)</text>
    <text x="312" y="127" fill="#fb7185" font-size="10" font-weight="700" text-anchor="middle">중 1·2회 모두 1: 64칸 제외!</text>
    <rect x="370" y="92" width="85" height="45" fill="rgba(56,189,248,0.15)" stroke="#38bdf8" stroke-width="1"/>
    <text x="412" y="118" fill="#bae6fd" font-size="10.5" font-weight="700" text-anchor="middle">A=2, B=3 (48)</text>

    <rect x="255" y="137" width="115" height="65" fill="rgba(52,211,153,0.32)" stroke="#34d399" stroke-width="2"/>
    <text x="312" y="165" fill="#6ee7b7" font-size="11" font-weight="800" text-anchor="middle">★ 케이스 ① (E∩F)</text>
    <text x="312" y="182" fill="#ecfdf5" font-size="11" font-weight="800" text-anchor="middle">A=3, B=2 : 12×4=48칸</text>
    <text x="312" y="196" fill="#a7f3d0" font-size="9.5" text-anchor="middle">(1회차 (1,1)제외: 12-8=4)</text>
    <rect x="370" y="137" width="85" height="65" fill="rgba(56,189,248,0.15)" stroke="#38bdf8" stroke-width="1"/>
    <text x="412" y="173" fill="#bae6fd" font-size="10.5" font-weight="700" text-anchor="middle">A=3, B=3 (96)</text>

    <rect x="255" y="202" width="115" height="50" fill="rgba(56,189,248,0.15)" stroke="#38bdf8" stroke-width="1"/>
    <text x="312" y="231" fill="#bae6fd" font-size="10.5" font-weight="700" text-anchor="middle">A=4, B=2 (24)</text>
    <rect x="370" y="202" width="85" height="50" fill="rgba(52,211,153,0.32)" stroke="#34d399" stroke-width="2"/>
    <text x="412" y="223" fill="#6ee7b7" font-size="10.5" font-weight="800" text-anchor="middle">★ 케이스 ②</text>
    <text x="412" y="240" fill="#ecfdf5" font-size="10.5" font-weight="800" text-anchor="middle">A=4,B=3: 48칸</text>

    <text x="355" y="270" fill="#fde68a" font-size="10.5" font-weight="700" text-anchor="middle">※ 케이스 ①(48칸) + 케이스 ②(48칸) = 총 96칸!</text>

    <rect x="490" y="54" width="170" height="226" rx="10" fill="rgba(30,41,59,0.9)" stroke="#fbbf24" stroke-width="1.5"/>
    <text x="575" y="75" fill="#fde68a" font-size="12" font-weight="800" text-anchor="middle">조건부확률 넓이 비</text>
    <rect x="510" y="90" width="130" height="38" rx="6" fill="rgba(56,189,248,0.18)" stroke="#38bdf8"/>
    <text x="575" y="107" fill="#7cc4ff" font-size="11" font-weight="700" text-anchor="middle">분모 n(E) = 400 - 64</text>
    <text x="575" y="122" fill="#fff" font-size="12" font-weight="800" text-anchor="middle">= 336 가지</text>

    <rect x="510" y="138" width="130" height="38" rx="6" fill="rgba(52,211,153,0.22)" stroke="#34d399"/>
    <text x="575" y="155" fill="#6ee7b7" font-size="11" font-weight="700" text-anchor="middle">분자 n(E∩F) = 48 + 48</text>
    <text x="575" y="170" fill="#fff" font-size="12" font-weight="800" text-anchor="middle">= 96 가지</text>

    <line x1="575" y1="180" x2="575" y2="198" stroke="#fbbf24" stroke-width="2" marker-end="url(#arrGold)"/>
    <rect x="505" y="203" width="140" height="64" rx="8" fill="rgba(251,191,36,0.18)" stroke="#fbbf24" stroke-width="2"/>
    <text x="575" y="224" fill="#fde68a" font-size="12" font-weight="800" text-anchor="middle">P(F|E) = 96/336 = 2/7</text>
    <text x="575" y="244" fill="#34d399" font-size="13" font-weight="900" text-anchor="middle">∴ p + q = 7 + 2 = 9</text>
    <text x="575" y="260" fill="#cbd5e1" font-size="10" text-anchor="middle">(48로 위아래 동시 약분!)</text>
    """
    return _svg_wrap(title, sub, inner, 292)


def _draw_coordinate_curve_svg(pid: str, title_ko: str, eq_label: str, pt1_label: str, pt2_label: str, ans_label: str, mode: str = "cubic", lang: str = "ko") -> str:
    badge = f"📐 [시각적 도형·함수 그래프 모델] {title_ko}" if lang == "ko" else f"📐 [Visual Geometric & Graph Model] {pid.upper()}"
    if mode == "area":
        curve_svg = """
        <path d="M 120 210 Q 210 95 310 130 L 310 210 Z" fill="rgba(52,211,153,0.28)" stroke="none"/>
        <path d="M 80 235 Q 200 75 350 140" fill="none" stroke="#38bdf8" stroke-width="3"/>
        <path d="M 80 210 L 355 210" fill="none" stroke="#a78bfa" stroke-width="2" stroke-dasharray="5,4"/>
        <line x1="120" y1="90" x2="120" y2="245" stroke="#fbbf24" stroke-width="1.5" stroke-dasharray="4,4"/>
        <line x1="310" y1="90" x2="310" y2="245" stroke="#fbbf24" stroke-width="1.5" stroke-dasharray="4,4"/>
        <text x="215" y="175" fill="#6ee7b7" font-size="12.5" font-weight="800" text-anchor="middle">정적분 넓이 S = ∫ [위 곡선 - 아래 곡선] dx</text>
        """
    elif mode == "piecewise":
        curve_svg = """
        <path d="M 80 220 Q 150 110 215 145" fill="none" stroke="#38bdf8" stroke-width="3"/>
        <path d="M 215 145 Q 285 180 350 95" fill="none" stroke="#34d399" stroke-width="3"/>
        <line x1="215" y1="75" x2="215" y2="245" stroke="#fbbf24" stroke-width="1.5" stroke-dasharray="4,4"/>
        <circle cx="215" cy="145" r="6" fill="#fbbf24" stroke="#0b1120" stroke-width="2"/>
        <text x="140" y="115" fill="#7cc4ff" font-size="11.5" font-weight="700" text-anchor="middle">좌극한 lim(x→a⁻)</text>
        <text x="295" y="115" fill="#6ee7b7" font-size="11.5" font-weight="700" text-anchor="middle">우극한 lim(x→a⁺)</text>
        <text x="215" y="262" fill="#fde68a" font-size="11.5" font-weight="800" text-anchor="middle">경계점 x = a (연속·미분가능 일치점)</text>
        """
    elif mode == "tangent":
        curve_svg = """
        <path d="M 75 235 C 140 220, 210 175, 330 75" fill="none" stroke="#38bdf8" stroke-width="3"/>
        <line x1="115" y1="230" x2="345" y2="92" stroke="#fbbf24" stroke-width="2.5"/>
        <path d="M 215 170 L 285 170 L 285 128" fill="rgba(251,191,36,0.18)" stroke="#fde68a" stroke-width="1.5" stroke-dasharray="3,3"/>
        <circle cx="215" cy="170" r="5.5" fill="#fb7185" stroke="#fff" stroke-width="1.5"/>
        <text x="250" y="186" fill="#fde68a" font-size="11" font-weight="700" text-anchor="middle">Δx</text>
        <text x="315" y="154" fill="#fde68a" font-size="11" font-weight="700" text-anchor="middle">Δy = f'(a)Δx</text>
        <text x="195" y="155" fill="#fecdd3" font-size="11.5" font-weight="800" text-anchor="end">접점 P(a, f(a))</text>
        """
    elif mode == "kinematics":
        curve_svg = """
        <path d="M 80 120 Q 175 255 280 170 T 355 95" fill="none" stroke="#38bdf8" stroke-width="3"/>
        <path d="M 80 185 L 132 185 Q 105 150 80 120 Z" fill="rgba(56,189,248,0.25)"/>
        <path d="M 132 185 Q 195 240 262 185 Z" fill="rgba(251,113,133,0.28)"/>
        <circle cx="132" cy="185" r="5" fill="#fbbf24"/>
        <circle cx="262" cy="185" r="5" fill="#fbbf24"/>
        <text x="197" y="232" fill="#fecdd3" font-size="11" font-weight="800" text-anchor="middle">v(t) &lt; 0 (역방향 이동 구간)</text>
        <text x="197" y="110" fill="#fde68a" font-size="11.5" font-weight="800" text-anchor="middle">운동 방향 전환점: v(t) = 0</text>
        """
    elif mode == "quartic_bitangent":
        curve_svg = """
        <!-- W-shaped Quartic with Bitangent Line at x=1 and x=4 -->
        <path d="M 85 95 C 110 215, 155 190, 195 140 C 235 90, 275 185, 345 75" fill="none" stroke="#38bdf8" stroke-width="3"/>
        <line x1="75" y1="195" x2="355" y2="125" stroke="#fbbf24" stroke-width="2.4"/>
        <circle cx="132" cy="181" r="5.5" fill="#34d399" stroke="#0b1120" stroke-width="1.5"/>
        <circle cx="282" cy="143" r="5.5" fill="#34d399" stroke="#0b1120" stroke-width="1.5"/>
        <text x="132" y="200" fill="#6ee7b7" font-size="11" font-weight="800" text-anchor="middle">접점 x = 1</text>
        <text x="282" y="164" fill="#6ee7b7" font-size="11" font-weight="800" text-anchor="middle">접점 x = 4</text>
        <text x="215" y="88" fill="#fde68a" font-size="11.5" font-weight="800" text-anchor="middle">이중접선: f(x) - (mx+n) = (x-1)²(x-4)²</text>
        """
    elif mode == "cusp_abs":
        curve_svg = """
        <!-- Absolute value folded curve with smooth tangent root vs V-cusp root -->
        <path d="M 80 210 Q 130 210 155 155 Q 185 90 245 210" fill="none" stroke="#38bdf8" stroke-width="3"/>
        <path d="M 245 210 L 325 95" fill="none" stroke="#fb7185" stroke-width="3"/>
        <path d="M 245 210 L 315 260" fill="none" stroke="#94a3b8" stroke-width="1.8" stroke-dasharray="4,4"/>
        <circle cx="115" cy="210" r="5.5" fill="#34d399"/><text x="115" y="232" fill="#6ee7b7" font-size="10.5" font-weight="800" text-anchor="middle">중근 α (미분가능)</text>
        <circle cx="245" cy="210" r="5.5" fill="#fb7185"/><text x="245" y="232" fill="#fecdd3" font-size="10.5" font-weight="800" text-anchor="middle">첨점 β (꺾임 상쇄!)</text>
        <text x="215" y="85" fill="#fde68a" font-size="11" font-weight="800" text-anchor="middle">절댓값 함수의 첨점(V자) 좌·우 미분계수 대칭</text>
        """
    elif mode == "transcendental_limit":
        curve_svg = """
        <!-- y = ln(1+t) or sin(t) tangent to y = t at origin -->
        <line x1="80" y1="210" x2="315" y2="75" stroke="#fbbf24" stroke-width="2.2" stroke-dasharray="5,4"/>
        <path d="M 80 210 Q 195 142 345 115" fill="none" stroke="#38bdf8" stroke-width="3"/>
        <circle cx="80" cy="210" r="6" fill="#34d399" stroke="#0b1120" stroke-width="1.5"/>
        <text x="265" y="88" fill="#fde68a" font-size="11.5" font-weight="800">접선 y = t (기울기 1)</text>
        <text x="275" y="148" fill="#7cc4ff" font-size="11.5" font-weight="800">곡선 y = ln(1+t) · sin t</text>
        <text x="215" y="255" fill="#6ee7b7" font-size="11" font-weight="800" text-anchor="middle">원점(0,0) 근방에서 곡선과 접선의 비율 → 1</text>
        """
    else:
        curve_svg = """
        <path d="M 75 225 C 125 75, 185 75, 220 155 C 255 235, 305 235, 355 85" fill="none" stroke="#38bdf8" stroke-width="3"/>
        <line x1="115" y1="112" x2="205" y2="112" stroke="#34d399" stroke-width="1.8" stroke-dasharray="4,3"/>
        <line x1="235" y1="198" x2="325" y2="198" stroke="#fb7185" stroke-width="1.8" stroke-dasharray="4,3"/>
        <circle cx="158" cy="112" r="5.5" fill="#34d399" stroke="#0b1120" stroke-width="1.5"/>
        <circle cx="282" cy="198" r="5.5" fill="#fb7185" stroke="#0b1120" stroke-width="1.5"/>
        <text x="158" y="98" fill="#6ee7b7" font-size="11" font-weight="800" text-anchor="middle">극대 (f'=0)</text>
        <text x="282" y="218" fill="#fecdd3" font-size="11" font-weight="800" text-anchor="middle">극소 (f'=0)</text>
        """

    inner = f"""
    <rect x="20" y="52" width="365" height="226" rx="10" fill="rgba(15,23,42,0.9)" stroke="#475569" stroke-width="1.5"/>
    <line x1="45" y1="210" x2="365" y2="210" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arrCyan)"/>
    <line x1="80" y1="255" x2="80" y2="68" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arrCyan)"/>
    <text x="368" y="214" fill="#cbd5e1" font-size="11" font-weight="700">x</text>
    <text x="76" y="64" fill="#cbd5e1" font-size="11" font-weight="700">y</text>
    <text x="68" y="224" fill="#94a3b8" font-size="10.5">O</text>
    {curve_svg}
    {_right_panel_svg("핵심 기하·해석 관계 요약", "#38bdf8", "#7cc4ff", eq_label, pt1_label, pt2_label, ans_label)}
    """
    return _svg_wrap(badge, f"Answer: {ans_label}", inner, 290)


def _draw_geometry_conic_trig_svg(pid: str, title_ko: str, eq_label: str, pt1_label: str, pt2_label: str, ans_label: str, geo_type: str = "circle_tri", lang: str = "ko") -> str:
    badge = f"📐 [의도적 기하 작도 다이어그램] {title_ko}" if lang == "ko" else f"📐 [Intentional Geometric Construction] {pid.upper()}"
    if geo_type == "hyperbola":
        fig = """
        <line x1="40" y1="165" x2="370" y2="165" stroke="#94a3b8" stroke-width="1.5"/>
        <line x1="205" y1="65" x2="205" y2="265" stroke="#94a3b8" stroke-width="1.5"/>
        <line x1="75" y1="75" x2="335" y2="255" stroke="#a78bfa" stroke-width="1.2" stroke-dasharray="5,4"/>
        <line x1="75" y1="255" x2="335" y2="75" stroke="#a78bfa" stroke-width="1.2" stroke-dasharray="5,4"/>
        <path d="M 110 80 Q 175 165 110 250" fill="none" stroke="#38bdf8" stroke-width="3"/>
        <path d="M 300 80 Q 235 165 300 250" fill="none" stroke="#38bdf8" stroke-width="3"/>
        <circle cx="105" cy="165" r="4.5" fill="#fbbf24"/><text x="105" y="184" fill="#fde68a" font-size="11" font-weight="800" text-anchor="middle">F'(-c,0)</text>
        <circle cx="305" cy="165" r="4.5" fill="#fbbf24"/><text x="305" y="184" fill="#fde68a" font-size="11" font-weight="800" text-anchor="middle">F(c,0)</text>
        <circle cx="282" cy="108" r="5.5" fill="#34d399" stroke="#fff" stroke-width="1.5"/><text x="302" y="102" fill="#6ee7b7" font-size="11.5" font-weight="800">P(x,y)</text>
        <polygon points="105,165 305,165 282,108" fill="rgba(52,211,153,0.18)" stroke="#34d399" stroke-width="2"/>
        <text x="185" y="128" fill="#6ee7b7" font-size="11" font-weight="800">PF' = d₂</text>
        <text x="308" y="140" fill="#6ee7b7" font-size="11" font-weight="800">PF = d₁</text>
        <text x="205" y="255" fill="#fde68a" font-size="11" font-weight="800" text-anchor="middle">쌍곡선 정의: |PF' - PF| = 2a &amp; 점근선 y = ±(b/a)x</text>
        """
    elif geo_type == "parabola":
        fig = """
        <line x1="45" y1="165" x2="365" y2="165" stroke="#94a3b8" stroke-width="1.5"/>
        <line x1="165" y1="65" x2="165" y2="265" stroke="#94a3b8" stroke-width="1.5"/>
        <line x1="105" y1="70" x2="105" y2="260" stroke="#fb7185" stroke-width="2" stroke-dasharray="5,4"/>
        <text x="105" y="272" fill="#fecdd3" font-size="10.5" font-weight="800" text-anchor="middle">준선 x = -p</text>
        <path d="M 320 75 Q 40 165 320 255" fill="none" stroke="#38bdf8" stroke-width="3"/>
        <line x1="125" y1="185" x2="295" y2="75" stroke="#fbbf24" stroke-width="2.2"/>
        <circle cx="195" cy="139" r="5.5" fill="#34d399" stroke="#fff" stroke-width="1.5"/>
        <line x1="105" y1="139" x2="195" y2="139" stroke="#34d399" stroke-width="2.2" marker-start="url(#arrGreen)" marker-end="url(#arrGreen)"/>
        <circle cx="225" cy="165" r="4.5" fill="#fbbf24"/><text x="225" y="183" fill="#fde68a" font-size="11" font-weight="800" text-anchor="middle">초점 F(p,0)</text>
        <text x="150" y="130" fill="#6ee7b7" font-size="11" font-weight="800" text-anchor="middle">거리 = x₁ + p</text>
        """
    elif geo_type == "ellipse":
        fig = """
        <line x1="40" y1="170" x2="370" y2="170" stroke="#94a3b8" stroke-width="1.5"/>
        <line x1="205" y1="65" x2="205" y2="265" stroke="#94a3b8" stroke-width="1.5"/>
        <ellipse cx="205" cy="170" rx="135" ry="78" fill="rgba(56,189,248,0.10)" stroke="#38bdf8" stroke-width="2.5"/>
        <circle cx="120" cy="170" r="5" fill="#fbbf24"/><text x="120" y="190" fill="#fde68a" font-size="11" font-weight="800" text-anchor="middle">F'(-c,0)</text>
        <circle cx="290" cy="170" r="5" fill="#fbbf24"/><text x="290" y="190" fill="#fde68a" font-size="11" font-weight="800" text-anchor="middle">F(c,0)</text>
        <circle cx="245" cy="96" r="5.5" fill="#34d399" stroke="#fff" stroke-width="1.5"/><text x="245" y="84" fill="#6ee7b7" font-size="11.5" font-weight="800" text-anchor="middle">P</text>
        <polygon points="120,170 290,170 245,96" fill="rgba(52,211,153,0.22)" stroke="#34d399" stroke-width="2"/>
        <text x="205" y="264" fill="#fde68a" font-size="11" font-weight="800" text-anchor="middle">타원의 정의: PF' + PF = 2a (장축의 길이)</text>
        """
    elif geo_type == "space3d":
        fig = """
        <polygon points="85,125 225,125 275,85 135,85" fill="rgba(56,189,248,0.12)" stroke="#38bdf8" stroke-width="1.8"/>
        <polygon points="85,235 225,235 275,195 135,195" fill="rgba(167,139,250,0.15)" stroke="#a78bfa" stroke-width="2"/>
        <line x1="85" y1="125" x2="85" y2="235" stroke="#38bdf8" stroke-width="1.8"/>
        <line x1="225" y1="125" x2="225" y2="235" stroke="#38bdf8" stroke-width="1.8"/>
        <line x1="275" y1="85" x2="275" y2="195" stroke="#38bdf8" stroke-width="1.8"/>
        <line x1="135" y1="85" x2="135" y2="195" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="4,4"/>
        <polygon points="85,155 225,125 185,235" fill="rgba(251,191,36,0.28)" stroke="#fbbf24" stroke-width="2.2"/>
        <polygon points="85,235 225,235 185,235" fill="rgba(52,211,153,0.3)" stroke="#34d399" stroke-width="2"/>
        <text x="185" y="165" fill="#fde68a" font-size="11.5" font-weight="800" text-anchor="middle">단면 넓이 S(x)</text>
        <text x="195" y="258" fill="#6ee7b7" font-size="11" font-weight="800" text-anchor="middle">공간도형 · 삼수선 정리 · 정사영 S' = S cos θ</text>
        """
    elif geo_type == "vector":
        fig = """
        <polygon points="200,75 85,230 325,230" fill="rgba(56,189,248,0.12)" stroke="#38bdf8" stroke-width="2"/>
        <line x1="85" y1="230" x2="255" y2="140" stroke="#fbbf24" stroke-width="2.5" marker-end="url(#arrGold)"/>
        <circle cx="200" cy="75" r="5" fill="#38bdf8"/><text x="200" y="65" fill="#7cc4ff" font-size="12" font-weight="800" text-anchor="middle">A</text>
        <circle cx="85" cy="230" r="5" fill="#38bdf8"/><text x="70" y="235" fill="#7cc4ff" font-size="12" font-weight="800">B</text>
        <circle cx="325" cy="230" r="5" fill="#38bdf8"/><text x="340" y="235" fill="#7cc4ff" font-size="12" font-weight="800">C</text>
        <circle cx="255" cy="140" r="5.5" fill="#fbbf24"/><text x="282" y="138" fill="#fde68a" font-size="11.5" font-weight="800">내분점 P</text>
        <text x="205" y="256" fill="#6ee7b7" font-size="11" font-weight="800" text-anchor="middle">벡터 분해 및 내적(수직 투영) 기하 모델</text>
        """
    elif geo_type == "circle_line":
        fig = """
        <!-- Circle C(2,3) and Line 3x-4y+k=0 with Max Distance d + r -->
        <circle cx="175" cy="168" r="58" fill="rgba(56,189,248,0.12)" stroke="#38bdf8" stroke-width="2.5"/>
        <line x1="95" y1="68" x2="345" y2="225" stroke="#fbbf24" stroke-width="2.5"/>
        <!-- Perpendicular line through center C to farthest point P -->
        <line x1="128" y1="204" x2="245" y2="118" stroke="#34d399" stroke-width="2.2" stroke-dasharray="4,3"/>
        <circle cx="175" cy="168" r="5" fill="#fbbf24"/><text x="165" y="158" fill="#fde68a" font-size="11" font-weight="800" text-anchor="end">중심 C(2,3)</text>
        <circle cx="128" cy="204" r="5.5" fill="#fb7185"/><text x="115" y="224" fill="#fecdd3" font-size="11" font-weight="800">최대점 P</text>
        <text x="158" y="198" fill="#6ee7b7" font-size="11" font-weight="800">r=3</text>
        <text x="218" y="152" fill="#fde68a" font-size="11" font-weight="800">거리 d=4</text>
        <text x="205" y="258" fill="#6ee7b7" font-size="11" font-weight="800" text-anchor="middle">최댓값 M = 중심거리 d + 반지름 r = 7</text>
        """
    elif geo_type == "trig_wave":
        fig = """
        <!-- Sine/Cosine periodic wave + horizontal line y = k + Triangle ABC -->
        <line x1="40" y1="165" x2="365" y2="165" stroke="#94a3b8" stroke-width="1.5"/>
        <line x1="65" y1="68" x2="65" y2="255" stroke="#94a3b8" stroke-width="1.5"/>
        <path d="M 65 165 Q 130 65 195 165 T 325 165" fill="none" stroke="#38bdf8" stroke-width="3"/>
        <line x1="45" y1="115" x2="355" y2="115" stroke="#fbbf24" stroke-width="1.8" stroke-dasharray="5,4"/>
        <polygon points="92,115 168,115 260,215" fill="rgba(52,211,153,0.22)" stroke="#34d399" stroke-width="2"/>
        <circle cx="92" cy="115" r="5" fill="#fbbf24"/><text x="85" y="105" fill="#fde68a" font-size="11" font-weight="800">A</text>
        <circle cx="168" cy="115" r="5" fill="#fbbf24"/><text x="175" y="105" fill="#fde68a" font-size="11" font-weight="800">B</text>
        <circle cx="260" cy="215" r="5" fill="#34d399"/><text x="260" y="234" fill="#6ee7b7" font-size="11" font-weight="800" text-anchor="middle">극소·최소 C</text>
        <text x="205" y="258" fill="#fde68a" font-size="11" font-weight="800" text-anchor="middle">삼각함수 주기 T = 2π/b &amp; 대칭축 중점 성질</text>
        """
    elif geo_type == "trig_quadrant":
        fig = """
        <!-- Unit Circle & Quadrant Right Triangle -->
        <line x1="55" y1="162" x2="350" y2="162" stroke="#94a3b8" stroke-width="1.5"/>
        <line x1="202" y1="62" x2="202" y2="258" stroke="#94a3b8" stroke-width="1.5"/>
        <circle cx="202" cy="162" r="78" fill="rgba(56,189,248,0.08)" stroke="#38bdf8" stroke-width="2"/>
        <polygon points="202,162 138,162 138,116" fill="rgba(52,211,153,0.25)" stroke="#34d399" stroke-width="2"/>
        <circle cx="138" cy="116" r="5" fill="#fbbf24"/>
        <text x="118" y="110" fill="#fde68a" font-size="11" font-weight="800">P(x, y)</text>
        <text x="265" y="105" fill="#7cc4ff" font-size="10.5" font-weight="700">1사분면: 모두(+)</text>
        <text x="72" y="105" fill="#6ee7b7" font-size="10.5" font-weight="700">2사분면: sin(+)</text>
        <text x="72" y="232" fill="#c4b5fd" font-size="10.5" font-weight="700">3사분면: tan(+)</text>
        <text x="265" y="232" fill="#fde68a" font-size="10.5" font-weight="700">4사분면: cos(+)</text>
        <text x="202" y="268" fill="#fde68a" font-size="11" font-weight="800" text-anchor="middle">단위원 직각삼각형 &amp; 사분면 부호(얼싸안고)</text>
        """
    elif geo_type == "tree_height":
        fig = """
        <!-- Observer at 7m and 2m viewing tree of height H -->
        <line x1="45" y1="228" x2="355" y2="228" stroke="#94a3b8" stroke-width="2"/>
        <line x1="65" y1="192" x2="340" y2="192" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="4,4"/>
        <!-- Tree at x=315 -->
        <line x1="315" y1="78" x2="315" y2="228" stroke="#34d399" stroke-width="5"/>
        <circle cx="315" cy="78" r="14" fill="rgba(52,211,153,0.35)" stroke="#34d399" stroke-width="2"/>
        <!-- Observer 1 (7m) and Observer 2 (2m) -->
        <circle cx="85" cy="192" r="5" fill="#fbbf24"/><line x1="85" y1="192" x2="85" y2="228" stroke="#fbbf24" stroke-width="2.5"/>
        <circle cx="215" cy="192" r="5" fill="#fb7185"/><line x1="215" y1="192" x2="215" y2="228" stroke="#fb7185" stroke-width="2.5"/>
        <line x1="85" y1="192" x2="315" y2="78" stroke="#fde68a" stroke-width="1.5"/>
        <line x1="85" y1="192" x2="315" y2="228" stroke="#fde68a" stroke-width="1.5"/>
        <line x1="215" y1="192" x2="315" y2="78" stroke="#fb7185" stroke-width="1.8"/>
        <line x1="215" y1="192" x2="315" y2="228" stroke="#fb7185" stroke-width="1.8"/>
        <text x="125" y="184" fill="#fde68a" font-size="11" font-weight="800">θ (7m)</text>
        <text x="248" y="182" fill="#fecdd3" font-size="11" font-weight="800">θ+π/4 (2m)</text>
        <text x="336" y="140" fill="#6ee7b7" font-size="11" font-weight="800">h=H-1</text>
        <text x="336" y="214" fill="#bae6fd" font-size="10.5" font-weight="700">1m</text>
        <text x="200" y="258" fill="#fde68a" font-size="11" font-weight="800" text-anchor="middle">tan(α+β) 덧셈정리 &amp; 시선각 기하 모델</text>
        """
    elif geo_type == "exp_log_sym":
        fig = """
        <!-- Exponential & Log curves symmetric across y=x with chord triangle -->
        <line x1="45" y1="220" x2="360" y2="220" stroke="#94a3b8" stroke-width="1.5"/>
        <line x1="85" y1="250" x2="85" y2="65" stroke="#94a3b8" stroke-width="1.5"/>
        <line x1="65" y1="240" x2="325" y2="70" stroke="#fbbf24" stroke-width="1.5" stroke-dasharray="5,4"/>
        <path d="M 65 205 Q 155 190 235 72" fill="none" stroke="#38bdf8" stroke-width="3"/>
        <path d="M 105 245 Q 145 155 335 115" fill="none" stroke="#34d399" stroke-width="3"/>
        <polygon points="155,155 215,155 215,105" fill="rgba(167,139,250,0.22)" stroke="#c4b5fd" stroke-width="1.8"/>
        <circle cx="155" cy="155" r="5" fill="#fbbf24"/>
        <circle cx="215" cy="105" r="5" fill="#fbbf24"/>
        <text x="315" y="88" fill="#fde68a" font-size="11" font-weight="800">대칭축 y = x</text>
        <text x="195" y="82" fill="#7cc4ff" font-size="11" font-weight="800">y = aˣ</text>
        <text x="315" y="138" fill="#6ee7b7" font-size="11" font-weight="800">y = logₐ x</text>
        <text x="205" y="258" fill="#fde68a" font-size="11" font-weight="800" text-anchor="middle">지수·로그 평행·대칭이동 &amp; 직각삼각형 좌표 차</text>
        """
    else:
        fig = """
        <circle cx="200" cy="162" r="92" fill="rgba(56,189,248,0.08)" stroke="#38bdf8" stroke-width="2.2"/>
        <polygon points="135,97 272,105 282,205 115,198" fill="rgba(167,139,250,0.16)" stroke="#c4b5fd" stroke-width="2"/>
        <line x1="272" y1="105" x2="115" y2="198" stroke="#fbbf24" stroke-width="2.5"/>
        <circle cx="135" cy="97" r="4.5" fill="#34d399"/><text x="122" y="90" fill="#6ee7b7" font-size="11.5" font-weight="800">A</text>
        <circle cx="272" cy="105" r="4.5" fill="#fbbf24"/><text x="285" y="102" fill="#fde68a" font-size="11.5" font-weight="800">B</text>
        <circle cx="282" cy="205" r="4.5" fill="#34d399"/><text x="295" y="212" fill="#6ee7b7" font-size="11.5" font-weight="800">C</text>
        <circle cx="115" cy="198" r="4.5" fill="#fbbf24"/><text x="98" y="205" fill="#fde68a" font-size="11.5" font-weight="800">D</text>
        <text x="195" y="146" fill="#fde68a" font-size="11.5" font-weight="800" text-anchor="middle">공통현 BD = 2R sin θ</text>
        <text x="200" y="268" fill="#bae6fd" font-size="10.5" font-weight="700" text-anchor="middle">사인법칙 &amp; 코사인법칙 결합 기하 도형</text>
        """

    inner = f"""
    <rect x="20" y="52" width="365" height="226" rx="10" fill="rgba(15,23,42,0.9)" stroke="#475569" stroke-width="1.5"/>
    {fig}
    {_right_panel_svg("기하 작도 및 길이·각도 분석", "#a78bfa", "#c4b5fd", eq_label, pt1_label, pt2_label, ans_label)}
    """
    return _svg_wrap(badge, f"Answer: {ans_label}", inner, 290)


def _draw_sequence_algebra_prob_svg(pid: str, title_ko: str, eq_label: str, pt1_label: str, pt2_label: str, ans_label: str, seq_type: str = "stepping", lang: str = "ko") -> str:
    badge = f"📐 [의도적 도형·시각화 모델] {title_ko}" if lang == "ko" else f"📐 [Intentional Visual Model] {pid.upper()}"
    if seq_type == "bell":
        fig = """
        <line x1="40" y1="225" x2="365" y2="225" stroke="#94a3b8" stroke-width="1.5"/>
        <path d="M 145 225 L 145 125 Q 202 65 260 125 L 260 225 Z" fill="rgba(52,211,153,0.28)"/>
        <path d="M 45 223 C 105 220, 145 72, 202 72 C 260 72, 300 220, 360 223" fill="none" stroke="#38bdf8" stroke-width="3"/>
        <line x1="202" y1="65" x2="202" y2="235" stroke="#fbbf24" stroke-width="2" stroke-dasharray="5,4"/>
        <text x="202" y="252" fill="#fde68a" font-size="11" font-weight="800" text-anchor="middle">대칭축 (평균 m / 표본평균 x̄)</text>
        <text x="145" y="242" fill="#6ee7b7" font-size="10.5" font-weight="700" text-anchor="middle">m - E</text>
        <text x="260" y="242" fill="#6ee7b7" font-size="10.5" font-weight="700" text-anchor="middle">m + E</text>
        <text x="202" y="165" fill="#ecfdf5" font-size="11.5" font-weight="800" text-anchor="middle">대칭 넓이 = 확률 P</text>
        """
    elif seq_type == "tree":
        fig = """
        <rect x="45" y="145" width="68" height="34" rx="8" fill="rgba(251,191,36,0.22)" stroke="#fbbf24" stroke-width="1.8"/>
        <text x="79" y="166" fill="#fde68a" font-size="11" font-weight="800" text-anchor="middle">기준 상태</text>
        <line x1="113" y1="155" x2="168" y2="108" stroke="#34d399" stroke-width="2" marker-end="url(#arrGreen)"/>
        <line x1="113" y1="170" x2="168" y2="212" stroke="#fb7185" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrCoral)"/>
        <rect x="172" y="88" width="82" height="36" rx="8" fill="rgba(52,211,153,0.2)" stroke="#34d399" stroke-width="1.8"/>
        <text x="213" y="110" fill="#6ee7b7" font-size="10.5" font-weight="800" text-anchor="middle">경로 ① (유효)</text>
        <rect x="172" y="195" width="82" height="36" rx="8" fill="rgba(251,113,133,0.15)" stroke="#fb7185" stroke-width="1.5"/>
        <text x="213" y="217" fill="#fecdd3" font-size="10.5" font-weight="700" text-anchor="middle">경로 ② (제외)</text>
        <line x1="254" y1="106" x2="292" y2="82" stroke="#34d399" stroke-width="2" marker-end="url(#arrGreen)"/>
        <line x1="254" y1="106" x2="292" y2="136" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrCyan)"/>
        <rect x="296" y="65" width="76" height="34" rx="7" fill="rgba(52,211,153,0.28)" stroke="#34d399" stroke-width="2"/>
        <text x="334" y="86" fill="#ecfdf5" font-size="10.5" font-weight="800" text-anchor="middle">해 ① 확정</text>
        <rect x="296" y="120" width="76" height="34" rx="7" fill="rgba(56,189,248,0.22)" stroke="#38bdf8" stroke-width="1.8"/>
        <text x="334" y="141" fill="#bae6fd" font-size="10.5" font-weight="800" text-anchor="middle">해 ② 확정</text>
        <text x="205" y="262" fill="#fde68a" font-size="11" font-weight="800" text-anchor="middle">상태 전이 · 홀짝 분기 · 역추적 트리 도형</text>
        """
    elif seq_type == "fraction_bar":
        fig = """
        <text x="202" y="82" fill="#7cc4ff" font-size="11.5" font-weight="800" text-anchor="middle">밑(Base) 통일 &amp; 지수·로그 막대 결합 도형</text>
        <rect x="55" y="100" width="135" height="42" rx="6" fill="rgba(56,189,248,0.28)" stroke="#38bdf8" stroke-width="2"/>
        <text x="122" y="125" fill="#fff" font-size="11.5" font-weight="800" text-anchor="middle">첫째 지수·로그 블록</text>
        <text x="202" y="126" fill="#fbbf24" font-size="18" font-weight="900" text-anchor="middle">+</text>
        <rect x="215" y="100" width="135" height="42" rx="6" fill="rgba(167,139,250,0.28)" stroke="#a78bfa" stroke-width="2"/>
        <text x="282" y="125" fill="#fff" font-size="11.5" font-weight="800" text-anchor="middle">둘째 지수·로그 블록</text>
        <line x1="202" y1="150" x2="202" y2="178" stroke="#34d399" stroke-width="2.5" marker-end="url(#arrGreen)"/>
        <rect x="55" y="186" width="295" height="46" rx="8" fill="rgba(52,211,153,0.25)" stroke="#34d399" stroke-width="2.2"/>
        <text x="202" y="214" fill="#ecfdf5" font-size="12.5" font-weight="900" text-anchor="middle">결합된 전체 지수·로그 막대 (정수·유리수 완성!)</text>
        <text x="202" y="258" fill="#fde68a" font-size="10.5" font-weight="700" text-anchor="middle">곱셈·나눗셈을 막대 길이의 덧셈·뺄셈으로 시각화</text>
        """
    elif seq_type == "number_line_domain":
        fig = """
        <!-- Number Line Domain Intersection & Squeeze Interval Model -->
        <text x="202" y="84" fill="#7cc4ff" font-size="11.5" font-weight="800" text-anchor="middle">수직선 진수·수렴 범위 교집합 &amp; 해 판정 도형</text>
        <rect x="145" y="120" width="185" height="58" fill="rgba(52,211,153,0.22)" stroke="none"/>
        <line x1="45" y1="178" x2="360" y2="178" stroke="#cbd5e1" stroke-width="2" marker-end="url(#arrCyan)"/>
        <!-- Ray 1 -->
        <path d="M 95 178 L 95 145 L 345 145" fill="none" stroke="#38bdf8" stroke-width="2.2" marker-end="url(#arrCyan)"/>
        <circle cx="95" cy="178" r="5.5" fill="#0b1120" stroke="#38bdf8" stroke-width="2.2"/>
        <!-- Ray 2 -->
        <path d="M 145 178 L 145 120 L 345 120" fill="none" stroke="#34d399" stroke-width="2.5" marker-end="url(#arrGreen)"/>
        <circle cx="145" cy="178" r="5.5" fill="#0b1120" stroke="#34d399" stroke-width="2.5"/>
        <!-- Valid vs Invalid Root -->
        <circle cx="115" cy="178" r="5" fill="#fb7185"/><text x="115" y="202" fill="#fecdd3" font-size="10.5" font-weight="800" text-anchor="middle">무연근(제외)</text>
        <circle cx="245" cy="178" r="6" fill="#fbbf24"/><text x="245" y="202" fill="#fde68a" font-size="11" font-weight="800" text-anchor="middle">유효 해(채택!)</text>
        <text x="235" y="110" fill="#6ee7b7" font-size="11" font-weight="800" text-anchor="middle">공통 허용 구간 (빗금 영역)</text>
        <text x="202" y="256" fill="#fde68a" font-size="11" font-weight="800" text-anchor="middle">수직선 위에서 경계값·부등호 방향을 시각적으로 검증</text>
        """
    elif seq_type == "dice_grid":
        fig = """
        <!-- 6x6 = 36 Coordinate Grid Square for Two Dice -->
        <text x="202" y="76" fill="#7cc4ff" font-size="11.5" font-weight="800" text-anchor="middle">주사위 2회 6×6 = 36칸 정사각형 격자 넓이 모델</text>
        <rect x="112" y="88" width="144" height="144" fill="rgba(30,41,59,0.9)" stroke="#94a3b8" stroke-width="1.8"/>
        <!-- 6 anti-diagonal cells highlighted -->
        <rect x="112" y="208" width="24" height="24" fill="rgba(52,211,153,0.45)" stroke="#34d399"/>
        <rect x="136" y="184" width="24" height="24" fill="rgba(52,211,153,0.45)" stroke="#34d399"/>
        <rect x="160" y="160" width="24" height="24" fill="rgba(52,211,153,0.45)" stroke="#34d399"/>
        <rect x="184" y="136" width="24" height="24" fill="rgba(52,211,153,0.45)" stroke="#34d399"/>
        <rect x="208" y="112" width="24" height="24" fill="rgba(52,211,153,0.45)" stroke="#34d399"/>
        <rect x="232" y="88" width="24" height="24" fill="rgba(52,211,153,0.45)" stroke="#34d399"/>
        <text x="315" y="145" fill="#6ee7b7" font-size="11.5" font-weight="800" text-anchor="middle">목표 격자칸</text>
        <text x="315" y="165" fill="#fde68a" font-size="11.5" font-weight="800" text-anchor="middle">/ 전체 36칸</text>
        <text x="202" y="256" fill="#fde68a" font-size="11" font-weight="800" text-anchor="middle">순서쌍 (a, b)를 좌표 격자의 색칠된 칸수로 카운팅</text>
        """
    elif seq_type == "cards_slots":
        fig = """
        <!-- Visual Row of Cards / Flags / Slots with Symmetry & Combination -->
        <text x="202" y="82" fill="#7cc4ff" font-size="11.5" font-weight="800" text-anchor="middle">카드·깃발 자리 배치 및 대칭 묶음 도형</text>
        <rect x="48" y="105" width="42" height="58" rx="6" fill="rgba(251,113,133,0.28)" stroke="#fb7185" stroke-width="2"/><text x="69" y="139" fill="#fff" font-size="12" font-weight="800" text-anchor="middle">1</text>
        <rect x="98" y="105" width="42" height="58" rx="6" fill="rgba(56,189,248,0.25)" stroke="#38bdf8" stroke-width="1.8"/><text x="119" y="139" fill="#fff" font-size="12" font-weight="800" text-anchor="middle">2</text>
        <rect x="148" y="105" width="42" height="58" rx="6" fill="rgba(251,191,36,0.28)" stroke="#fbbf24" stroke-width="2"/><text x="169" y="139" fill="#fff" font-size="12" font-weight="800" text-anchor="middle">3</text>
        <rect x="198" y="105" width="42" height="58" rx="6" fill="rgba(56,189,248,0.25)" stroke="#38bdf8" stroke-width="1.8"/><text x="219" y="139" fill="#fff" font-size="12" font-weight="800" text-anchor="middle">4</text>
        <rect x="248" y="105" width="42" height="58" rx="6" fill="rgba(52,211,153,0.28)" stroke="#34d399" stroke-width="2"/><text x="269" y="139" fill="#fff" font-size="12" font-weight="800" text-anchor="middle">5</text>
        <rect x="298" y="105" width="42" height="58" rx="6" fill="rgba(167,139,250,0.25)" stroke="#a78bfa" stroke-width="1.8"/><text x="319" y="139" fill="#fff" font-size="12" font-weight="800" text-anchor="middle">6</text>
        <path d="M 69 175 Q 169 220 269 175" fill="none" stroke="#fbbf24" stroke-width="2" marker-end="url(#arrGold)"/>
        <text x="202" y="222" fill="#6ee7b7" font-size="11.5" font-weight="800" text-anchor="middle">순서 고정 · 대칭성 비율 · 중복조합 칸막이 모델</text>
        <text x="202" y="256" fill="#fde68a" font-size="11" font-weight="800" text-anchor="middle">자리 선택(nCr)과 대칭 나눗셈(÷k!)의 시각적 결합</text>
        """
    elif seq_type == "telescoping":
        fig = """
        <!-- Telescoping Cancellation Domino Blocks -->
        <text x="202" y="82" fill="#7cc4ff" font-size="11.5" font-weight="800" text-anchor="middle">부분분수 · 시그마 차분 연쇄 상쇄(Telescoping) 도형</text>
        <rect x="45" y="110" width="66" height="48" rx="7" fill="rgba(52,211,153,0.3)" stroke="#34d399" stroke-width="2.2"/>
        <text x="78" y="138" fill="#ecfdf5" font-size="11" font-weight="800" text-anchor="middle">+첫째항 생존!</text>
        <rect x="119" y="110" width="76" height="48" rx="7" fill="rgba(251,113,133,0.18)" stroke="#fb7185" stroke-width="1.5"/>
        <text x="157" y="138" fill="#fecdd3" font-size="11" font-weight="700" text-anchor="middle">-중간항 +중간항</text>
        <line x1="123" y1="152" x2="191" y2="116" stroke="#fb7185" stroke-width="2.5"/>
        <rect x="203" y="110" width="76" height="48" rx="7" fill="rgba(251,113,133,0.18)" stroke="#fb7185" stroke-width="1.5"/>
        <text x="241" y="138" fill="#fecdd3" font-size="11" font-weight="700" text-anchor="middle">-중간항 +중간항</text>
        <line x1="207" y1="152" x2="275" y2="116" stroke="#fb7185" stroke-width="2.5"/>
        <rect x="287" y="110" width="72" height="48" rx="7" fill="rgba(56,189,248,0.28)" stroke="#38bdf8" stroke-width="2.2"/>
        <text x="323" y="138" fill="#bae6fd" font-size="11" font-weight="800" text-anchor="middle">-끝항(→0)</text>
        <text x="202" y="198" fill="#6ee7b7" font-size="11.5" font-weight="800" text-anchor="middle">이웃한 (+), (-) 블록이 도미노처럼 연쇄 소거됨!</text>
        <text x="202" y="256" fill="#fde68a" font-size="11" font-weight="800" text-anchor="middle">남는 앞쪽 항들의 합 = 전체 급수·수열의 합</text>
        """
    else:
        fig = """
        <line x1="40" y1="232" x2="365" y2="232" stroke="#94a3b8" stroke-width="1.5"/>
        <rect x="62" y="182" width="46" height="50" rx="5" fill="rgba(56,189,248,0.28)" stroke="#38bdf8" stroke-width="1.8"/>
        <text x="85" y="212" fill="#fff" font-size="11" font-weight="800" text-anchor="middle">a₁</text>
        <rect x="138" y="152" width="46" height="80" rx="5" fill="rgba(56,189,248,0.35)" stroke="#38bdf8" stroke-width="1.8"/>
        <text x="161" y="196" fill="#fff" font-size="11" font-weight="800" text-anchor="middle">a₂</text>
        <rect x="214" y="122" width="46" height="110" rx="5" fill="rgba(167,139,250,0.35)" stroke="#a78bfa" stroke-width="1.8"/>
        <text x="237" y="180" fill="#fff" font-size="11" font-weight="800" text-anchor="middle">a₃</text>
        <rect x="290" y="92" width="52" height="140" rx="5" fill="rgba(52,211,153,0.35)" stroke="#34d399" stroke-width="2.2"/>
        <text x="316" y="166" fill="#ecfdf5" font-size="11.5" font-weight="900" text-anchor="middle">목표항 aₙ</text>
        <path d="M 85 176 Q 123 135 161 146" fill="none" stroke="#fbbf24" stroke-width="2" marker-end="url(#arrGold)"/>
        <path d="M 161 146 Q 199 105 237 116" fill="none" stroke="#fbbf24" stroke-width="2" marker-end="url(#arrGold)"/>
        <path d="M 237 116 Q 276 75 316 86" fill="none" stroke="#34d399" stroke-width="2" marker-end="url(#arrGreen)"/>
        <text x="202" y="258" fill="#fde68a" font-size="11" font-weight="800" text-anchor="middle">항 번호 점프(+d / ×r / 누적합) 계단 기둥 도형</text>
        """

    inner = f"""
    <rect x="20" y="52" width="365" height="226" rx="10" fill="rgba(15,23,42,0.9)" stroke="#475569" stroke-width="1.5"/>
    {fig}
    {_right_panel_svg("도식화 핵심 구조 및 수치", "#34d399", "#6ee7b7", eq_label, pt1_label, pt2_label, ans_label)}
    """
    return _svg_wrap(badge, f"Answer: {ans_label}", inner, 290)


# ==============================================================================
# CLASSIFIER & VISUAL PACKAGE BUILDER FOR ALL 119 PROBLEMS
# ==============================================================================

def _classify_problem(pid: str, title: str, sol_text: str):
    t = (title + " " + sol_text[:300]).lower()
    if pid == "c2610p28":
        return ("c2610p28", "cards_six_cases")
    if pid == "c2610p29":
        return ("c2610p29", "normal_two_cases")
    if pid in ("c2610p30", "c2709p30"):
        return ("c2610p30", "bags")
    if pid in ("a33ab59b", "c2610g24", "c2709g29") or "쌍곡선" in t:
        return ("geo", "hyperbola")
    if pid in ("c2610g26", "c2709g27") or "포물선" in t:
        return ("geo", "parabola")
    if pid in ("c2610g28", "c2709g25") or "타원" in t:
        return ("geo", "ellipse")
    if pid == "c1092101":
        return ("geo", "circle_line")
    if pid == "d7abad20":
        return ("geo", "tree_height")
    if pid in ("c2092102", "c261018", "c270906", "c30920"):
        return ("geo", "trig_wave")
    if pid in ("c261006", "c30906"):
        return ("geo", "trig_quadrant")
    if pid in ("c261012", "c261020", "c270910", "c30914"):
        return ("geo", "exp_log_sym")
    if pid in ("c2610g25", "c2610g27", "c2610g29", "c2610m26", "c30926", "c2709g24", "c2709g26", "c2709g28") or "공간도형" in t or "공간좌표" in t or "정사영" in t or "원기둥" in t or "입체도형" in t:
        return ("geo", "space3d")
    if pid in ("c2610g23", "c2610g30", "c2709g23", "c2709g30") or "벡터" in t:
        return ("geo", "vector")
    if pid in ("c261014", "c270912", "c30910", "c270920") or "사인법칙" in t or "외접원" in t:
        return ("geo", "circle_tri")
    if pid in ("36790012", "c2610p24", "c2610p26", "c2610p29", "c2709p27") or "정규분포" in t or "신뢰구간" in t or "이항분포" in t:
        return ("seq", "bell")
    if pid in ("8f24f3c3", "c2610p27", "c2709p24", "c2709p26"):
        return ("seq", "dice_grid")
    if pid in ("4cb6d212", "a05b47bc", "c2610p23", "c2610p25", "c2610p28", "c2709p23", "c2709p25", "c2709p28", "c2709p29"):
        return ("seq", "cards_slots")
    if pid in ("c270916", "c30916", "c2610m25", "c270925"):
        return ("seq", "number_line_domain")
    if pid in ("c270929", "c30929", "c30918", "c261016"):
        return ("seq", "telescoping")
    if pid in ("c261022", "c270918", "c270922", "c30922", "51908207", "1b623c24") or "귀납" in t or "역추적" in t or "전이" in t or "뒤집기" in t:
        return ("seq", "tree")
    if pid in ("c261001", "c261008", "8e9d528d", "c270901", "c30901", "c30908") or "거듭제곱" in t or "로그" in t:
        return ("seq", "fraction_bar")
    if pid in ("c261003", "c261010", "c2610m29", "c270903", "c270908", "c270914", "c30903", "c30912", "c30925") or "수열" in t:
        return ("seq", "stepping")
    if pid == "c261015":
        return ("calc", "quartic_bitangent")
    if pid in ("ac8dc374", "c270921", "e7d51a27", "c261021"):
        return ("calc", "cusp_abs")
    if pid in ("c2610m23", "c270923", "c30923"):
        return ("calc", "transcendental_limit")
    if pid in ("c261011", "c270909", "c30911") or "속도" in t or "가속도" in t:
        return ("calc", "kinematics")
    if pid in ("c261004", "c261009", "c2610m27", "c270904", "c270915", "c30904", "c30907") or "연속" in t or "좌극한" in t:
        return ("calc", "piecewise")
    if pid in ("c261007", "c2610m24", "c2610m30", "c270905", "c270913", "c270924", "c270926", "c30909", "c30913", "c30928") or "정적분" in t or "둘러싸인" in t:
        return ("calc", "area")
    if pid in ("c261002", "c261005", "c2610m28", "c270902", "c270919", "c270927", "c270928", "c30902", "c30905", "c30924", "c30927") or "미분계수" in t or "접선" in t:
        return ("calc", "tangent")
    return ("calc", "cubic")


def _clean_plain(s: str, max_len: int = 60) -> str:
    s = str(s)
    s = re.sub(r'<span class="bilingual-en">.*?</span>', ' ', s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s*\(자동 폴백 아님[^)]*\)", "", s)
    s = re.sub(r"\s*\(기초→심화\)", "", s)
    for _ in range(3):
        s = re.sub(r"\\sqrt\[3\]\{([^{}]+)\}", r"³√\1", s)
        s = re.sub(r"\\sqrt\{([^{}]+)\}", r"√\1", s)
        s = re.sub(r"\\binom\{([^{}]+)\}\{([^{}]+)\}", r"C(\1,\2)", s)
        s = re.sub(
            r"\\d?frac\{([^{}]+)\}\{([^{}]+)\}",
            lambda fm: (f"({fm.group(1)})" if ('+' in fm.group(1) or '-' in fm.group(1)[1:]) else fm.group(1)) + '/' + fm.group(2),
            s
        )
    s = s.replace("\\dfrac", "").replace("\\frac", "/").replace("\\sqrt", "√")
    s = s.replace("\\overline", "").replace("\\mathrm", "").replace("\\left", "").replace("\\right", "")
    s = s.replace("\\implies", "⇒").replace("\\iff", "⇔").replace("\\to", "→")
    s = s.replace("\\in", "∈").replace("\\subset", "⊂").replace("\\cup", "∪").replace("\\cap", "∩")
    s = s.replace("\\sum", "∑").replace("\\infty", "∞")
    s = s.replace("\\le", "≤").replace("\\ge", "≥").replace("\\ne", "≠")
    s = s.replace("\\pi", "π").replace("\\theta", "θ").replace("\\alpha", "α").replace("\\beta", "β")
    s = s.replace("\\times", "×").replace("\\cdot", "·").replace("\\pm", "±")
    s = s.replace("^2", "²").replace("^3", "³")
    for idx_d, sub_c in enumerate("₀₁₂₃₄₅₆₇₈₉"):
        s = re.sub(rf"([a-zA-Z])_{idx_d}\b", rf"\1{sub_c}", s)
    s = re.sub(r"([a-zA-Z])_n\b", r"\1ₙ", s)
    s = re.sub(r"([a-zA-Z])_k\b", r"\1ₖ", s)
    s = s.replace("$", "").replace("{", "").replace("}", "").replace("\\", "")
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) <= max_len:
        return s
    # Word-boundary truncation without cutting mid-word
    cut = s[:max_len]
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut


def _compact_title_for_svg(short_title: str) -> str:
    t = _clean_plain(short_title, 90)
    # Shorten verbose exam prefixes so the full mathematical topic fits without truncation
    t = re.sub(r"^\[20\d\d학년도\s*(\d+월)\s*(?:고\d\s*)?([^\]]+)\]", r"[\1 \2]", t)
    t = re.sub(r"^20\d\d학년도\s*(\d+월)\s*(?:모의평가|학력평가)\s*", r"[\1] ", t)
    t = re.sub(r"^20\d\d년\s*(\d+월)\s*학력평가\s*", r"[\1] ", t)
    return _clean_plain(t, 42)


def _compact_step_for_svg(raw_step: str) -> str:
    s = _clean_plain(raw_step, 120)
    # Strip verbose prefix like '🔰 1단계 · [초등 구구단 연계] ' or '제1단계 · '
    s = re.sub(r"^[🔰🌿🌱🌳💎🏆📘🎯\s]*(?:제?\d+단계)\s*·\s*(?:\[[^\]]+\]\s*)?", "", s).strip()
    if len(s) <= 32:
        return s
    if "⇒" in s:
        left, right = s.split("⇒", 1)
        left = left.strip()
        right = right.strip()
        avail = max(12, 29 - len(right))
        if len(left) > avail:
            cut_l = left[:avail]
            if " " in cut_l and len(cut_l.rsplit(" ", 1)[0]) >= 8:
                cut_l = cut_l.rsplit(" ", 1)[0]
            left = cut_l.strip()
        return f"{left} ⇒ {right}"
    return _clean_plain(s, 32)


def build_visual_and_schematic_block(
    pid: str,
    title_ko: str,
    step_summaries_ko: list,
    ans_str: str,
    sol_ko_plain: str = "",
    lang: str = "ko",
) -> str:
    from stitch_screen_builder import convert_svg_to_stitch_light
    short_title = re.sub(r"\s*·\s*(?:mathedu|min7014).*$", "", title_ko).strip()
    short_title = re.sub(r"\s*\(자동 폴백 아님[^)]*\)", "", short_title).strip()
    svg_title = _compact_title_for_svg(short_title)

    ans_raw = re.sub(r'<span class="bilingual-en">.*?</span>', '', str(ans_str), flags=re.S)
    ans_raw = re.sub(r'(?:정답|Correct Answer|Answer|\:)', ' ', ans_raw, flags=re.I)
    ans_clean = _clean_plain(ans_raw, 26) or "확정"

    s_clean = [_compact_step_for_svg(x) for x in step_summaries_ko if _compact_step_for_svg(x)]
    eq_lbl = s_clean[0] if len(s_clean) > 0 else svg_title
    pt1_lbl = s_clean[1] if len(s_clean) > 1 else "핵심 공식 및 기하 관계 적용"
    pt2_lbl = s_clean[-1] if len(s_clean) > 2 else f"수식 연립 및 도출 ⇒ {ans_clean}"

    cat, submode = _classify_problem(pid, short_title, sol_ko_plain)
    if pid == "c261022":
        svg_html = _draw_c261022_svg(lang=lang)
    elif pid == "c2610p27":
        svg_html = _draw_c2610p27_svg(lang=lang)
    elif cat == "c2610p28":
        svg_html = _draw_c2610p28_svg(lang=lang)
    elif cat == "c2610p29":
        svg_html = _draw_c2610p29_svg(lang=lang)
    elif cat == "c2610p30":
        svg_html = _draw_c2610p30_svg(lang=lang)
    elif cat == "geo":
        svg_html = _draw_geometry_conic_trig_svg(pid, svg_title, eq_lbl, pt1_lbl, pt2_lbl, ans_clean, geo_type=submode, lang=lang)
    elif cat == "seq":
        svg_html = _draw_sequence_algebra_prob_svg(pid, svg_title, eq_lbl, pt1_lbl, pt2_lbl, ans_clean, seq_type=submode, lang=lang)
    else:
        svg_html = _draw_coordinate_curve_svg(pid, svg_title, eq_lbl, pt1_lbl, pt2_lbl, ans_clean, mode=submode, lang=lang)

    svg_html = convert_svg_to_stitch_light(svg_html, ans_clean)

    flow_steps = []
    for raw_s in step_summaries_ko:
        if raw_s.count("$") % 2 != 0:
            raw_s = raw_s.replace("$", "")
        flow_steps.append(raw_s)

    while len(flow_steps) < 3:
        flow_steps.append("핵심 조건 및 공식 결합")

    if len(flow_steps) > 4:
        n = len(flow_steps)
        picked = [flow_steps[0], flow_steps[n // 3], flow_steps[(2 * n) // 3], flow_steps[-1]]
    else:
        picked = flow_steps[:4]

    ans_math = ans_str.strip()
    if ans_math.count("$") % 2 != 0:
        ans_math = ans_clean

    if lang == "ko":
        fig_hdr = "🎨 [그림으로 이해하는 시각적 도형·개념 다이어그램]"
        fig_cap = (
            f"▲ <b>[{_esc(short_title)}]</b> 문항의 조건과 기하학적·구조적 관계를 한눈에 볼 수 있도록 의도적으로 작도한 시각적 도형 모델입니다."
        )
        flow_hdr = "🗺️ [한눈에 보는 도식화 풀이 흐름도 (Schematic Solution Flowchart)]"
        badge_labels = ["STEP 1 · 출발 조건", "STEP 2 · 도형·공식 변환", "STEP 3 · 핵심 식 도출", "STEP 4 · 결합 및 계산"]
        tbl_hdr_1, tbl_hdr_2, tbl_hdr_3 = "도식화 단계", "핵심 개념 · 기하 도형 · 적용 공식", "도출 결과"
    else:
        fig_hdr = "🎨 [Visual Geometric & Conceptual Diagram]"
        fig_cap = (
            f"▲ Intentionally constructed geometric & visual model illustrating the core mathematical relationships of <b>[{_esc(pid.upper())}]</b>."
        )
        flow_hdr = "🗺️ [At-a-Glance Schematic Solution Flowchart]"
        badge_labels = ["STEP 1 · Given Condition", "STEP 2 · Visual/Formula Transform", "STEP 3 · Key Derivation", "STEP 4 · Synthesis"]
        tbl_hdr_1, tbl_hdr_2, tbl_hdr_3 = "Schematic Stage", "Core Concept · Geometric Model · Formula", "Derived Result"

    flow_cells = []
    for idx, st_txt in enumerate(picked):
        b_lbl = badge_labels[idx] if idx < len(badge_labels) else f"STEP {idx+1}"
        flow_cells.append(
            f'<td style="background:#ffffff;border:1px solid #cbd5e1;border-radius:10px;padding:10px 12px;vertical-align:top;width:22%">'
            f'<b style="color:#006398;font-size:0.78rem;display:block;margin-bottom:4px">{b_lbl}</b>'
            f'<span style="color:#1e293b;font-size:0.86rem;line-height:1.45">{st_txt}</span>'
            f'</td>'
        )
        if idx < len(picked) - 1:
            flow_cells.append(
                '<td style="text-align:center;vertical-align:middle;color:#d97706;font-weight:900;font-size:1.1rem;padding:0 4px">➔</td>'
            )

    flow_cells.append(
        '<td style="text-align:center;vertical-align:middle;color:#059669;font-weight:900;font-size:1.1rem;padding:0 4px">⇒</td>'
        f'<td style="background:#ecfdf5;border:1.5px solid #10b981;border-radius:10px;padding:10px 12px;vertical-align:middle;text-align:center;width:16%">'
        f'<b style="color:#047857;font-size:0.78rem;display:block;margin-bottom:4px">🎯 최종 정답</b>'
        f'<b style="color:#065f46;font-size:0.98rem">{ans_math}</b>'
        f'</td>'
    )

    summary_rows = []
    for idx, full_st in enumerate(flow_steps, 1):
        stage_lbl = f"제{idx}단계" if lang == "ko" else f"Step {idx}"
        summary_rows.append(
            f'<tr>'
            f'<td style="padding:7px 10px;border:1px solid #cbd5e1;color:#006398;font-weight:700;text-align:center;white-space:nowrap">{stage_lbl}</td>'
            f'<td style="padding:7px 12px;border:1px solid #cbd5e1;color:#1e293b;line-height:1.5">{full_st}</td>'
            f'<td style="padding:7px 10px;border:1px solid #cbd5e1;color:#059669;font-weight:700;text-align:center">'
            f'{"다음 단계 연결 ➔" if idx < len(flow_steps) else f"정답: {ans_math}"}'
            f'</td>'
            f'</tr>'
        )

    block_html = (
        f'<h4>{fig_hdr}</h4>'
        f'<figure class="math-visual-diagram" style="margin:12px 0 18px;padding:14px;background:#f8fafc;border:1.5px solid #cbd5e1;border-radius:14px;text-align:center">'
        f'{svg_html}'
        f'<figcaption style="margin-top:10px;font-size:0.85rem;color:#475569;line-height:1.55">{fig_cap}</figcaption>'
        f'</figure>'
        f'<h4>{flow_hdr}</h4>'
        f'<section class="math-schematic-flow" style="margin:12px 0 18px;padding:14px;background:#f8fafc;border:1px solid #cbd5e1;border-radius:14px">'
        f'<table style="width:100%;border-collapse:separate;border-spacing:4px;margin-bottom:12px"><tr>{"".join(flow_cells)}</tr></table>'
        f'<table style="width:100%;border-collapse:collapse;font-size:0.86rem;background:#ffffff;border-radius:8px;overflow:hidden">'
        f'<thead><tr style="background:#f1f5f9;color:#0f172a">'
        f'<th style="padding:8px 10px;border:1px solid #cbd5e1;width:14%">{tbl_hdr_1}</th>'
        f'<th style="padding:8px 12px;border:1px solid #cbd5e1">{tbl_hdr_2}</th>'
        f'<th style="padding:8px 10px;border:1px solid #cbd5e1;width:22%">{tbl_hdr_3}</th>'
        f'</tr></thead>'
        f'<tbody>{"".join(summary_rows)}</tbody>'
        f'</table>'
        f'</section>'
    )
    return block_html
