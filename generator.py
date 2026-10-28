"""퀴즈 dict → 단일 HTML 파일 생성. 저장: board/<slug>.html"""
import json, html, os, hashlib, time, re
import min7014_matcher

TEMPLATE = r"""<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · min7014 mathedu</title>
<meta name="description" content="{title} · 초등 눈높이부터 시작하는 단계별 인터랙티브 디딤돌 퀴즈 & GeoGebra 시각적 증명 무료 풀이">
<meta name="keywords" content="{title}, 수능 수학 기출, 모의평가 수학 해설, 디딤돌 퀴즈, GeoGebra, 수학자료실, mathedu, min7014">
<meta name="author" content="mathedu">
<link rel="canonical" href="https://min7014.github.io/mathedu/board/{slug_js}.html">
<link rel="icon" type="image/png" sizes="32x32" href="../assets/favicon.png">
<style>
/* ════════════════════════════════════════════════════════════════════════
   ✨ Google Stitch Design System: "Mathematical Clarity & Dynamic Geometry"
   Academic Modernism Light Palette for Problem & Scaffolding Pages
   ════════════════════════════════════════════════════════════════════════ */
:root {{
  --bg: #fcf8fa;
  --card: #ffffff;
  --card2: #f6f3f5;
  --card3: #f0edef;
  --line: #e4e2e4;
  --line-strong: #c5c6cd;
  --txt: #1b1b1d;
  --sub: #45464d;
  --primary: #131b2e;
  --accent: #006398;
  --accent2: #4f46e5;
  --good: #059669;
  --bad: #ba1a1a;
  --gold: #b45309;
  --glass-blur: 16px;
  --glass-shadow: 0 2px 12px rgba(19, 27, 46, 0.05);
  --radius: 16px;
}}

*, *::before, *::after {{
  box-sizing: border-box;
}}

html, body {{
  overflow-x: hidden !important;
  max-width: 100vw;
  width: 100%;
}}

body {{
  margin: 0;
  color: var(--txt);
  line-height: 1.7;
  font-family: 'Inter', 'Pretendard', -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", system-ui, sans-serif;
  background-color: var(--bg);
  background-image:
    radial-gradient(circle at 12% 8%, rgba(0, 99, 152, 0.05), transparent 40%),
    radial-gradient(circle at 88% 12%, rgba(79, 70, 229, 0.05), transparent 40%),
    radial-gradient(circle at 50% 85%, rgba(16, 185, 129, 0.04), transparent 45%);
  background-attachment: fixed;
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
}}

.wrap {{
  max-width: 860px;
  width: 100%;
  margin: 0 auto;
  padding: 24px 18px 80px;
  overflow-x: hidden;
  box-sizing: border-box;
}}

/* ── Top Navigation Bar ── */
.topbar {{
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  flex-wrap: wrap;
  padding: 10px 14px;
  background: rgba(255, 255, 255, 0.90);
  border: 1px solid var(--line);
  border-radius: 14px;
  box-shadow: 0 2px 8px rgba(19, 27, 46, 0.04);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
}}

.tbtn {{
  background: #ffffff;
  color: var(--txt);
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 7px 13px;
  font-weight: 700;
  cursor: pointer;
  text-decoration: none;
  font-size: .86rem;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all .15s ease;
  box-shadow: 0 1px 2px rgba(19, 27, 46, 0.03);
}}

.tbtn:hover {{
  background: var(--card2);
  border-color: var(--accent);
  color: var(--accent);
  transform: translateY(-1px);
}}

.tbtn.brand-btn {{
  background: var(--primary) !important;
  color: #ffffff !important;
  border-color: var(--primary) !important;
}}

.tbtn.brand-btn:hover {{
  background: #1e293b !important;
  color: #ffffff !important;
}}

.lang-group {{
  display: inline-flex;
  gap: 3px;
  background: var(--card3);
  padding: 3px;
  border-radius: 10px;
  border: 1px solid var(--line);
  margin-left: auto;
}}

.lang-btn {{
  background: transparent;
  color: var(--sub);
  border: none;
  border-radius: 7px;
  padding: 5px 11px;
  font-size: 0.8rem;
  font-weight: 700;
  cursor: pointer;
  transition: 0.15s;
}}

.lang-btn.active {{
  background: #000000;
  color: #ffffff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.12);
}}

/* ── Sticky Score & Progress Bar ── */
.score {{
  position: sticky;
  top: 8px;
  z-index: 50;
  background: rgba(255, 255, 255, 0.92);
  padding: 10px 16px;
  margin-bottom: 18px;
  border: 1px solid var(--line);
  border-radius: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: .92rem;
  color: var(--txt);
  font-weight: 600;
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  box-shadow: 0 4px 14px rgba(19, 27, 46, 0.05);
}}

.score b {{
  color: var(--accent);
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 700;
}}

.bar {{
  height: 8px;
  background: #e4e2e4;
  border-radius: 9999px;
  overflow: hidden;
  flex: 1;
  margin: 0 14px;
}}

.bar > i {{
  display: block;
  height: 100%;
  width: 0;
  background: linear-gradient(90deg, var(--accent), #10b981);
  border-radius: 9999px;
  transition: .3s;
}}

/* ── Headings & Typography ── */
h1 {{
  font-family: 'Plus Jakarta Sans', 'Pretendard', sans-serif;
  font-size: 1.55rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  margin: 0 0 6px;
  color: var(--primary);
  line-height: 1.38;
}}

h2 {{
  font-family: 'Plus Jakarta Sans', 'Pretendard', sans-serif;
  font-size: 1.18rem;
  font-weight: 800;
  letter-spacing: -0.015em;
  margin: 34px 0 12px;
  color: var(--primary);
  border-left: 4px solid var(--accent);
  padding-left: 12px;
  line-height: 1.4;
}}

.lead {{
  color: var(--sub);
  font-size: .95rem;
  margin: 0 0 12px;
  line-height: 1.65;
}}

code {{
  background: var(--card3);
  padding: 2px 6px;
  border-radius: 6px;
  color: var(--accent);
  font-family: 'Space Grotesk', monospace;
  font-size: 0.9em;
}}

/* ── Original Exam Problem Card ── */
.orig-card {{
  background: #ffffff;
  border: 1px solid var(--line);
  border-top: 4px solid var(--primary);
  border-radius: var(--radius);
  padding: 22px 24px;
  margin: 18px 0 26px;
  box-shadow: 0 4px 20px rgba(19, 27, 46, 0.06);
}}

.orig-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
  flex-wrap: wrap;
  gap: 8px;
}}

.orig-tag {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--primary);
  color: #ffffff;
  font-size: .78rem;
  font-weight: 800;
  padding: 5px 14px;
  border-radius: 9999px;
  letter-spacing: .2px;
  box-shadow: 0 2px 6px rgba(19, 27, 46, 0.12);
}}

.orig-badge {{
  font-size: .8rem;
  color: var(--accent);
  font-weight: 700;
  background: rgba(0, 99, 152, 0.08);
  border: 1px solid rgba(0, 99, 152, 0.22);
  padding: 4px 12px;
  border-radius: 9999px;
  font-family: 'Space Grotesk', 'Pretendard', sans-serif;
}}

.orig-grid {{
  display: grid;
  grid-template-columns: 1.05fr 0.95fr;
  gap: 18px;
  align-items: start;
}}

.orig-col-media {{
  display: flex;
  flex-direction: column;
  gap: 8px;
}}

.orig-media-tabs {{
  display: flex;
  gap: 6px;
  margin-bottom: 4px;
}}

.orig-media-tab {{
  flex: 1;
  background: var(--card2);
  border: 1px solid var(--line);
  color: var(--sub);
  border-radius: 8px;
  padding: 6px 10px;
  font-size: .8rem;
  font-weight: 700;
  cursor: pointer;
  transition: .15s;
  text-align: center;
}}

.orig-media-tab:hover {{
  background: var(--card3);
  color: var(--primary);
  border-color: var(--accent);
}}

.orig-media-tab.active {{
  background: var(--primary);
  border-color: var(--primary);
  color: #ffffff;
}}

.orig-media-frame {{
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 12px;
  text-align: center;
  box-shadow: 0 1px 4px rgba(19, 27, 46, 0.04);
}}

.orig-media-frame img, .orig-media-frame video {{
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  display: block;
  margin: 0 auto;
}}

.orig-media-sub {{
  font-size: .76rem;
  color: var(--sub);
  text-align: center;
}}

.orig-col-desc {{
  display: flex;
  flex-direction: column;
  gap: 10px;
}}

.orig-text-box {{
  background: var(--card2);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 14px 16px;
  font-size: .92rem;
  line-height: 1.7;
  color: var(--txt);
}}

.orig-text-box h4 {{
  margin: 0 0 8px;
  color: var(--accent);
  font-size: .96rem;
  font-weight: 800;
}}

.orig-cond-wrap {{
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 10px 12px;
  font-size: .88rem;
  line-height: 1.65;
  margin-top: 8px;
  color: var(--txt);
}}

.orig-stem {{
  font-size: 1.05rem;
  line-height: 1.75;
  font-weight: 600;
  color: var(--txt);
  word-break: keep-all;
  margin: 6px 0;
}}

.orig-media {{
  text-align: center;
  margin: 14px 0;
}}

.orig-media img {{
  max-width: 100%;
  max-height: 360px;
  border-radius: 12px;
  border: 1px solid var(--line);
  box-shadow: 0 2px 12px rgba(19, 27, 46, 0.06);
}}

.orig-tip {{
  font-size: .85rem;
  color: var(--sub);
  background: var(--card2);
  border: 1px dashed rgba(0, 99, 152, 0.35);
  border-radius: 10px;
  padding: 10px 12px;
  line-height: 1.6;
}}

.min-visual-tip {{
  background: #f0f7ff;
  border: 1px solid rgba(0, 99, 152, 0.22);
  border-left: 4px solid var(--accent);
  border-radius: 12px;
  padding: 14px 16px;
  margin: 18px 0;
  font-size: .88rem;
  line-height: 1.65;
  color: #1e293b;
}}

.min-visual-tip b {{
  color: var(--accent);
}}

/* ── Step 0 Symbol Translator & Knowledge Cards ── */
.sym {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin: 12px 0;
}}

.sym div {{
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 10px 14px;
  font-size: .9rem;
  color: var(--txt);
  box-shadow: 0 1px 4px rgba(19, 27, 46, 0.03);
}}

.sym b {{
  color: var(--accent);
}}

.sym-card {{
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 18px 20px;
  box-shadow: var(--glass-shadow);
  transition: .2s;
}}

.sym-card:hover {{
  border-color: rgba(0, 99, 152, 0.45);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(19, 27, 46, 0.08);
}}

.sym-badge {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(0, 99, 152, 0.08);
  border: 1px solid rgba(0, 99, 152, 0.22);
  color: var(--accent);
  font-size: .76rem;
  font-weight: 800;
  padding: 3px 10px;
  border-radius: 12px;
  margin-bottom: 8px;
}}

.sym-title {{
  font-size: 1.05rem;
  color: var(--primary);
  font-weight: 800;
  margin: 0 0 10px;
  line-height: 1.45;
}}

.sym-formula-box {{
  background: var(--card2);
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 10px 14px;
  margin: 8px 0 12px;
  text-align: center;
  font-size: 1.05rem;
  color: var(--txt);
}}

.sym-desc {{
  color: var(--txt);
  font-size: .91rem;
  line-height: 1.75;
}}

.sym-desc b {{
  color: var(--accent);
}}

.step0-visual-box {{
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 20px;
  margin: 20px 0 26px;
  box-shadow: var(--glass-shadow);
}}

.know {{
  background: var(--card2);
  border: 1px dashed rgba(0, 99, 152, 0.40);
  border-radius: 14px;
  padding: 14px 16px;
  margin: 12px 0;
  font-size: .92rem;
  color: var(--txt);
}}

.know h3 {{
  margin: 0 0 6px;
  color: var(--accent);
  font-size: .98rem;
  font-weight: 800;
}}

/* ── Interactive Step Quiz Cards ── */
.q {{
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 18px 20px;
  margin: 14px 0;
  box-shadow: var(--glass-shadow);
  transition: .2s;
}}

.q:hover {{
  border-color: rgba(0, 99, 152, 0.35);
  box-shadow: 0 6px 22px rgba(19, 27, 46, 0.07);
}}

.q .lvl {{
  display: inline-block;
  font-size: .74rem;
  font-weight: 800;
  color: var(--accent);
  background: rgba(0, 99, 152, 0.08);
  border: 1px solid rgba(0, 99, 152, 0.18);
  padding: 2px 10px;
  border-radius: 9999px;
  margin-bottom: 4px;
}}

.q .stem {{
  font-size: 1.02rem;
  margin: 8px 0 14px;
  font-weight: 600;
  color: var(--txt);
  line-height: 1.65;
}}

.opts {{
  display: grid;
  gap: 8px;
}}

.opts.opts-inline {{
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 10px;
}}

.opt {{
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--card2);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 10px 14px;
  cursor: pointer;
  transition: .15s;
  font-size: .95rem;
  color: var(--txt);
}}

.opt:hover {{
  background: var(--card3);
  border-color: var(--accent);
  transform: translateY(-1px);
}}

.opt .n {{
  width: 24px;
  height: 24px;
  flex: 0 0 24px;
  border-radius: 50%;
  background: #ffffff;
  border: 1px solid var(--line-strong);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: .8rem;
  font-weight: 700;
  color: var(--primary);
  font-family: 'Space Grotesk', sans-serif;
}}

.opt.correct {{
  background: rgba(16, 185, 129, 0.12) !important;
  border-color: #10b981 !important;
  color: #065f46 !important;
  font-weight: 600;
}}

.opt.correct .n {{
  background: #10b981 !important;
  border-color: #10b981 !important;
  color: #ffffff !important;
}}

.opt.wrong {{
  background: rgba(239, 68, 68, 0.10) !important;
  border-color: #ef4444 !important;
  color: #991b1b !important;
}}

.opt.wrong .n {{
  background: #ef4444 !important;
  border-color: #ef4444 !important;
  color: #ffffff !important;
}}

.opt.locked {{
  cursor: default;
}}

.exp-toggle-btn {{
  background: var(--card3);
  border: 1px solid var(--line-strong);
  color: var(--primary);
  border-radius: 8px;
  padding: 5px 12px;
  font-size: .82rem;
  font-weight: 700;
  cursor: pointer;
  transition: .15s;
}}

.exp-toggle-btn:hover {{
  background: var(--primary);
  border-color: var(--primary);
  color: #ffffff;
}}

.exp {{
  margin-top: 12px;
  padding: 14px 16px;
  border-radius: 12px;
  background: var(--card2);
  border: 1px solid var(--line);
  border-left: 4px solid var(--accent);
  font-size: .92rem;
  display: none;
  color: var(--txt);
  line-height: 1.7;
}}

.exp.show {{
  display: block;
}}

.exp b {{
  color: var(--primary);
}}

/* ── Solution Card, Visual Diagrams & Schematic Flowcharts ── */
.sol {{
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 20px 22px;
  margin: 14px 0;
  box-shadow: var(--glass-shadow);
  color: var(--txt);
}}

.sol h4 {{
  color: var(--primary);
  margin: 18px 0 8px;
  font-size: 1.02rem;
  font-weight: 800;
}}

.sol-highlight {{
  background: #f0f7ff;
  border-left: 4px solid var(--accent);
  border-radius: 0 8px 8px 0;
  padding: 10px 14px;
  margin: 12px 0;
  color: var(--txt);
}}

.diagram {{
  background: #ffffff;
  color: #1b2436;
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 14px;
  margin: 14px 0;
  text-align: center;
  box-shadow: 0 1px 4px rgba(19, 27, 46, 0.04);
}}

.diagram svg, .diagram img {{
  max-width: 100%;
  height: auto;
}}

.diagram-caption {{
  font-size: .82rem;
  color: var(--sub);
  margin-top: 8px;
}}

figure.math-visual-diagram {{
  background: #f8fafc !important;
  border: 1px solid #cbd5e1 !important;
  border-radius: 14px !important;
  padding: 14px !important;
  margin: 12px 0 18px !important;
  text-align: center !important;
}}

figure.math-visual-diagram figcaption {{
  color: #475569 !important;
  font-size: 0.85rem !important;
  margin-top: 10px !important;
  line-height: 1.55 !important;
}}

section.math-schematic-flow {{
  background: #f8fafc !important;
  border: 1px solid #cbd5e1 !important;
  border-radius: 14px !important;
  padding: 14px !important;
  margin: 12px 0 18px !important;
}}

section.math-schematic-flow table {{
  background: transparent !important;
}}

section.math-schematic-flow td,
section.math-schematic-flow th {{
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
  color: #1e293b !important;
}}

section.math-schematic-flow thead tr,
section.math-schematic-flow thead th {{
  background: #f1f5f9 !important;
  color: #0f172a !important;
}}

section.math-schematic-flow td span,
section.math-schematic-flow td b {{
  color: #1e293b !important;
}}

section.math-schematic-flow td > b:first-child {{
  color: #006398 !important;
}}

/* ── Buttons & Final Score Block ── */
.btn {{
  background: #000000;
  color: #ffffff;
  border: none;
  border-radius: 10px;
  padding: 10px 20px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
  transition: .15s;
}}

.btn:hover {{
  background: #1e293b;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.18);
}}

.final {{
  text-align: center;
  margin: 34px 0;
  padding: 24px;
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  box-shadow: var(--glass-shadow);
  font-size: 1.05rem;
}}

.final .ans {{
  font-size: 1.6rem;
  color: var(--good);
  font-weight: 800;
  margin: 8px 0 14px;
  font-family: 'Plus Jakarta Sans', 'Pretendard', sans-serif;
}}

/* ── Cards (Playing Cards Visual) ── */
.cards {{
  display: flex;
  gap: 8px;
  justify-content: center;
  flex-wrap: wrap;
  margin: 14px 0;
}}

.card {{
  width: 64px;
  height: 92px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  border: 2px solid var(--line-strong);
}}

.card .num {{ font-size: 1.3rem; }}
.card .face {{ font-size: .7rem; margin-top: 4px; opacity: .85; }}
.card.front {{ background: #ffffff; color: #1b2436; border-color: #94a3b8; }}
.card.back {{ background: #334155; color: #ffffff; border-color: #1e293b; }}

/* ── min7014 Deep Exploration Addon Card ── */
.min7014-addon-card {{
  background: #ffffff;
  border: 1px solid var(--line);
  border-top: 4px solid var(--accent);
  border-radius: var(--radius);
  padding: 22px 24px;
  margin: 28px 0;
  box-shadow: 0 4px 20px rgba(19, 27, 46, 0.05);
  transition: .2s;
}}

.min7014-addon-card:hover {{
  border-color: rgba(0, 99, 152, 0.45);
}}

.min-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  flex-wrap: wrap;
  gap: 8px;
}}

.min-header-title {{
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.05rem;
  font-weight: 800;
  color: var(--primary);
  font-family: 'Plus Jakarta Sans', 'Pretendard', sans-serif;
}}

.min-logo {{
  width: 24px;
  height: 24px;
  border-radius: 6px;
  background: #ffffff;
  border: 1px solid var(--line);
  padding: 1px;
}}

.min-tag {{
  background: rgba(0, 99, 152, 0.08);
  border: 1px solid rgba(0, 99, 152, 0.25);
  color: var(--accent);
  padding: 3px 10px;
  border-radius: 9999px;
  font-size: .75rem;
  font-weight: 700;
}}

.min-lead {{
  font-size: .88rem;
  color: var(--sub);
  margin-bottom: 16px;
  line-height: 1.55;
  word-break: keep-all;
}}

.min-guide-banner {{
  background: #f0f7ff !important;
  border: 1px solid rgba(0, 99, 152, 0.22) !important;
  border-radius: 10px !important;
  padding: 12px 16px !important;
  margin-bottom: 16px !important;
  font-size: .85rem !important;
  line-height: 1.6 !important;
  color: #1e293b !important;
}}

.min-list {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
  gap: 14px;
  width: 100%;
  box-sizing: border-box;
}}

.min-item {{
  background: var(--card2);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 10px;
  transition: .15s;
  box-sizing: border-box;
  overflow: hidden;
  width: 100%;
}}

.min-item:hover {{
  background: #ffffff;
  border-color: var(--accent);
  box-shadow: 0 4px 14px rgba(0, 99, 152, 0.08);
  transform: translateY(-1px);
}}

.min-item:has(.min-ggb-frame-wrap.active) {{
  grid-column: 1 / -1;
}}

.min-item-main {{
  width: 100%;
  min-width: 0;
  box-sizing: border-box;
}}

.min-item-title {{
  display: block;
  color: var(--txt);
  font-size: .94rem;
  font-weight: 700;
  text-decoration: none;
  line-height: 1.6;
  word-break: keep-all;
  overflow-wrap: anywhere;
  white-space: normal;
}}

.min-item-title:hover {{
  color: var(--accent);
}}

.min-item-sub {{
  display: block;
  font-size: .8rem;
  font-weight: 400;
  color: var(--sub);
  margin-top: 4px;
  line-height: 1.4;
  word-break: break-word;
}}

.min-bullet {{
  font-size: .85rem;
  margin-right: 4px;
}}

.min-item-actions {{
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  align-items: center;
}}

.min-btn {{
  font-size: .78rem;
  font-weight: 700;
  padding: 5px 12px;
  border-radius: 8px;
  text-decoration: none;
  transition: .15s;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
}}

.min-btn-ggb {{
  background: rgba(2, 132, 199, 0.10);
  border: 1px solid rgba(2, 132, 199, 0.30);
  color: #0369a1;
}}

.min-btn-ggb:hover {{
  background: #0284c7;
  color: #ffffff;
}}

.min-btn-pdf {{
  background: rgba(220, 38, 38, 0.08);
  border: 1px solid rgba(220, 38, 38, 0.25);
  color: #b91c1c;
}}

.min-btn-pdf:hover {{
  background: #dc2626;
  color: #ffffff;
}}

.min-btn-yt {{
  background: rgba(239, 68, 68, 0.08);
  border: 1px solid rgba(239, 68, 68, 0.25);
  color: #dc2626;
}}

.min-btn-yt:hover {{
  background: #ef4444;
  color: #ffffff;
}}

.min-btn-algeo {{
  background: rgba(124, 58, 237, 0.08);
  border: 1px solid rgba(124, 58, 237, 0.25);
  color: #6d28d9;
}}

.min-btn-algeo:hover {{
  background: #7c3aed;
  color: #ffffff;
}}

.min-btn-detail {{
  background: var(--primary);
  border: 1px solid var(--primary);
  color: #ffffff;
}}

.min-btn-detail:hover {{
  background: var(--accent);
  border-color: var(--accent);
  color: #ffffff;
}}

.min-cat-badge {{
  display: inline-block;
  font-size: .72rem;
  padding: 2px 8px;
  border-radius: 6px;
  background: rgba(0, 99, 152, 0.08);
  color: var(--accent);
  border: 1px solid rgba(0, 99, 152, 0.20);
  margin-bottom: 6px;
  font-weight: 600;
}}

.min-ggb-frame-wrap {{
  margin-top: 12px;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--line);
  background: #ffffff;
  display: none;
}}

.min-ggb-frame-wrap.active {{
  display: block;
}}

.min-footer {{
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px dashed var(--line);
  text-align: right;
}}

.min-footer-link {{
  color: var(--accent);
  font-size: .84rem;
  font-weight: 700;
  text-decoration: none;
  transition: .15s;
}}

.min-footer-link:hover {{
  text-decoration: underline;
  color: var(--primary);
}}

.min-tip-item {{
  background: #ffffff !important;
  border: 1px solid rgba(0, 99, 152, 0.22) !important;
  color: var(--txt) !important;
}}

/* ── Report Form Overrides ── */
.report-wrap {{
  margin-top: 10px !important;
  border-top: 1px solid var(--line) !important;
  padding-top: 10px !important;
}}

.report-btn {{
  background: transparent !important;
  color: var(--sub) !important;
  border: 1px solid var(--line) !important;
}}

.report-text {{
  background: #ffffff !important;
  color: var(--txt) !important;
  border: 1px solid var(--line-strong) !important;
}}

.report-cancel {{
  background: #ffffff !important;
  color: var(--sub) !important;
  border: 1px solid var(--line-strong) !important;
}}

/* ── TrackFull Entry Modal Light Academic Styling ── */
#trackFull {{
  background: rgba(252, 248, 250, 0.96) !important;
  backdrop-filter: blur(18px) !important;
  -webkit-backdrop-filter: blur(18px) !important;
  color: var(--txt) !important;
}}

#trackFull h2 {{
  border-left: none !important;
  padding-left: 0 !important;
  color: var(--primary) !important;
  background: none !important;
  -webkit-text-fill-color: var(--primary) !important;
}}

#trackFull h3 {{
  color: var(--primary) !important;
}}

#trackFull p {{
  color: var(--sub) !important;
}}

#trackFull #studentName,
#trackFull #studentPin {{
  background: #ffffff !important;
  color: var(--txt) !important;
  border: 1.5px solid var(--line-strong) !important;
  box-shadow: 0 2px 6px rgba(19, 27, 46, 0.04) !important;
}}

/* ── Bilingual Dual-Display Engine (Light Mode High-Contrast) ── */
.bilingual-en {{ display: none; }}
.bilingual-ko {{ display: inline; }}
div.bilingual-ko, p.bilingual-ko {{ display: block; }}
html[lang="en"] .bilingual-ko {{ display: none !important; }}
html[lang="en"] .bilingual-en {{
  display: block;
  margin-top: 8px;
  color: #006398;
  font-size: 0.92em;
  line-height: 1.6;
  border-left: 3px solid rgba(0, 99, 152, 0.35);
  padding-left: 12px;
  font-weight: 500;
}}
html[lang="en"] span.bilingual-en {{
  display: inline !important;
  border-left: none !important;
  padding-left: 0 !important;
  margin-top: 0 !important;
}}
html[lang="en"] .stem span.bilingual-en {{
  display: inline !important;
  color: var(--txt);
  font-weight: 600;
}}
html[lang="en"] h1 .bilingual-en {{
  font-size: 1.35rem;
  color: var(--primary);
  font-weight: 800;
  border-left: none;
  padding-left: 0;
  margin-top: 2px;
}}
html[lang="en"] h2 .bilingual-en {{
  font-size: 1.05rem;
  color: var(--primary);
  font-weight: 800;
  border-left: none;
  padding-left: 0;
  margin-top: 2px;
}}
html[lang="en"] .lead .bilingual-en {{
  color: var(--sub);
  border-left: none;
  padding-left: 0;
  font-size: 0.92rem;
}}
html[lang="en"] .stem .bilingual-en {{
  color: var(--txt);
  font-weight: 600;
  margin-top: 6px;
}}
html[lang="en"] .orig-tag .bilingual-en {{
  display: inline;
  margin-left: 6px;
  font-weight: 700;
  border: none;
  padding: 0;
  color: #ffffff;
}}
html[lang="en"] .orig-tip .bilingual-en {{
  color: var(--sub);
  margin-top: 4px;
}}
html[lang="en"] .know .bilingual-en {{
  color: #0369a1;
  border-left-color: rgba(3, 105, 161, 0.4);
}}
html[lang="en"] .sol .bilingual-en {{
  color: var(--txt);
  border-left-color: rgba(0, 99, 152, 0.4);
}}
html[lang="en"] .exp .bilingual-en {{
  color: var(--txt);
  border-left-color: rgba(0, 99, 152, 0.4);
}}
html[lang="en"] .sym div .bilingual-en {{
  color: var(--sub);
  font-size: 0.84rem;
  margin-top: 4px;
  border-left: none;
  padding-left: 0;
}}
html[lang="en"] .sym-card .bilingual-en {{
  display: block !important;
  color: var(--sub);
  font-size: .88rem;
  line-height: 1.6;
  margin-top: 10px;
  border-left: 2px solid rgba(0, 99, 152, 0.35);
  padding-left: 10px;
}}
html[lang="en"] .sym-badge .bilingual-en {{
  display: inline !important;
  border: none !important;
  padding: 0 !important;
  margin: 0 !important;
  color: inherit !important;
}}
html[lang="en"] .sym-title .bilingual-en {{
  display: block !important;
  color: var(--primary) !important;
  font-size: .95rem !important;
  border: none !important;
  padding: 0 !important;
  margin-top: 4px !important;
}}

/* ── Mobile-Responsive Mathematical Formula & Layout Overflow Prevention ── */
h1, h2, h3, h4, h5, h6, p, div, span, li, a, label {{
  overflow-wrap: break-word;
  word-break: keep-all;
}}

.lead, .exp, .sol p, .orig-text-box, .min-visual-tip, .sym-desc,
.bilingual-ko, .bilingual-en, .orig-cond-wrap, .orig-tip, .know,
.sol-highlight, .min-item-title, .min-item-sub {{
  overflow-wrap: anywhere !important;
  word-break: normal;
}}

mjx-container {{
  max-width: 100% !important;
  box-sizing: border-box !important;
  -webkit-overflow-scrolling: touch;
}}

mjx-container[display="true"] {{
  display: block !important;
  max-width: 100% !important;
  overflow-x: auto !important;
  overflow-y: hidden !important;
  margin: 0.85em 0 !important;
  padding: 10px 14px !important;
  background: var(--card2) !important;
  border-radius: 10px;
  border: 1px solid var(--line) !important;
  color: var(--txt) !important;
  text-align: center !important;
  scrollbar-width: thin;
}}

mjx-container[display="true"]::-webkit-scrollbar {{ height: 4px; }}
mjx-container[display="true"]::-webkit-scrollbar-track {{ background: transparent; }}
mjx-container[display="true"]::-webkit-scrollbar-thumb {{ background: rgba(0, 99, 152, 0.25); border-radius: 3px; }}

mjx-container:not([display="true"]) {{
  display: inline-flex !important;
  vertical-align: middle !important;
  max-width: 100% !important;
  overflow: visible !important;
  padding: 0 1px !important;
  text-decoration: none !important;
  border-bottom: none !important;
  scrollbar-width: none !important;
}}

mjx-container:not([display="true"])::-webkit-scrollbar {{
  display: none !important;
  height: 0 !important;
  width: 0 !important;
}}

.opt, .opt * {{
  text-decoration: none !important;
  border-bottom: none !important;
}}
.opt mjx-container {{
  overflow: visible !important;
  scrollbar-width: none !important;
}}
.opt mjx-container::-webkit-scrollbar {{
  display: none !important;
  height: 0 !important;
  width: 0 !important;
}}

.orig-grid, .orig-grid > div, .orig-col-media, .orig-col-desc,
.min-list, .min-list > div, .min-item, .min-item-main, .min-item-actions,
.opts, .opt, .sym, .sym > div, .sym-card, .topbar, .score, .score > * {{
  min-width: 0 !important;
  max-width: 100% !important;
}}

.orig-card, .sol, .q, .exp, .know, .min7014-addon-card, .sym-card, .step0-visual-box {{
  max-width: 100% !important;
  overflow-x: hidden !important;
  box-sizing: border-box !important;
}}

@media (max-width: 768px) {{
  .orig-grid {{ grid-template-columns: 1fr !important; gap: 14px !important; }}
  .sym {{ grid-template-columns: 1fr !important; }}
  .min-list {{ grid-template-columns: 1fr !important; }}
}}

@media (max-width: 640px) {{
  .wrap {{ padding: 16px 14px 70px !important; }}
  h1 {{ font-size: 1.3rem !important; line-height: 1.45 !important; }}
  h2 {{ font-size: 1.12rem !important; margin: 26px 0 10px !important; }}
  .lead {{ font-size: 0.9rem !important; }}
  .orig-card {{ padding: 16px 14px !important; margin: 14px 0 20px !important; }}
  .orig-text-box {{ padding: 12px 14px !important; font-size: 0.88rem !important; }}
  .q {{ padding: 16px 14px !important; margin: 14px 0 !important; }}
  .q .stem {{ font-size: 0.98rem !important; }}
  .opts.opts-inline {{ grid-template-columns: repeat(2, 1fr) !important; gap: 8px !important; }}
  .opt {{ padding: 9px 12px !important; font-size: 0.92rem !important; }}
  .sol {{ padding: 18px 14px !important; font-size: 0.9rem !important; }}
  .min7014-addon-card {{ padding: 16px 14px !important; margin: 20px 0 !important; }}
  .min-item {{ padding: 12px 14px !important; }}
  .min-ggb-frame-wrap iframe {{ height: 380px !important; }}
  mjx-container {{ font-size: 92% !important; }}
}}

@media (max-width: 420px) {{
  .wrap {{ padding: 12px 10px 60px !important; }}
  h1 {{ font-size: 1.18rem !important; line-height: 1.4 !important; }}
  h2 {{ font-size: 1.05rem !important; }}
  .orig-header {{ flex-direction: column !important; align-items: flex-start !important; gap: 6px !important; }}
  .orig-tag {{ font-size: 0.75rem !important; padding: 4px 10px !important; }}
  .topbar {{ gap: 6px !important; }}
  .tbtn {{ padding: 6px 10px !important; font-size: 0.8rem !important; }}
  .lang-btn {{ padding: 4px 8px !important; font-size: 0.76rem !important; }}
  .score {{ font-size: 0.86rem !important; padding: 8px 12px !important; }}
  .bar {{ margin: 0 8px !important; }}
  .opts.opts-inline {{ grid-template-columns: 1fr !important; gap: 6px !important; }}
  .opt {{ padding: 8px 10px !important; font-size: 0.88rem !important; gap: 6px !important; }}
  .opt .n {{ width: 22px !important; height: 22px !important; flex: 0 0 22px !important; font-size: 0.76rem !important; }}
  .min-item-actions {{ gap: 4px !important; }}
  .min-btn {{ padding: 4px 8px !important; font-size: 0.74rem !important; }}
  .min-ggb-frame-wrap iframe {{ height: 300px !important; }}
  mjx-container {{ font-size: 85% !important; }}
  #studentName {{ min-width: 0 !important; width: 100% !important; }}
}}

@media (max-width: 360px) {{
  .wrap {{ padding: 10px 8px 50px !important; }}
  h1 {{ font-size: 1.08rem !important; }}
  .q, .sol, .orig-card, .min7014-addon-card, .sym-card, .know {{ padding: 12px 10px !important; border-radius: 12px !important; }}
  mjx-container {{ font-size: 80% !important; }}
}}
</style>
<script>window.MathJax={{tex:{{inlineMath:[['$','$'],['\\(','\\)']]}}}};</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml-full.js"></script>
<script src="../mathedu-i18n.js"></script>
</head><body><div class="wrap">
<div class="topbar">
<a class="tbtn brand-btn" href="/mathedu/" style="display:inline-flex;align-items:center;gap:8px">
<img src="../assets/favicon.png" alt="min7014" style="width:20px;height:20px;border-radius:5px;background:#fff;padding:1px">
<span>min7014 <b>mathedu</b></span>
</a>
<button class="tbtn" id="copyBtn" onclick="copyLink()"><span class="bilingual-ko">🔗 링크 복사</span><span class="bilingual-en">🔗 Copy Link</span></button>
<div class="lang-group">
  <button type="button" class="lang-btn active" data-lang-btn="ko" onclick="setBoardLang('ko', true)">한국어</button>
  <button type="button" class="lang-btn" data-lang-btn="en" onclick="setBoardLang('en', true)">English (Bilingual)</button>
</div>
</div>
<div class="score"><span><span class="bilingual-ko">점수</span><span class="bilingual-en">Score</span> <b id="pts">0</b> / <b id="tot">0</b></span>
<span class="bar"><i id="bar"></i></span><span id="pct">0%</span></div>
<h1>📘 {h1_title}</h1>
<p class="lead">기초→심화 단계별 5지선다 퀴즈. 정답 고르면 바로 채점+해설이 열립니다.<span class="bilingual-en">Step-by-step 5-choice scaffolding quiz from fundamentals to advanced mastery. Instant scoring & explanations upon selection.</span></p>
{original_block}
{symbols_block}
{levels_block}
{tracking_block}
{solution_block}
{min7014_materials_block}
<div class="final"><p><span class="bilingual-ko">🎉 완료!</span><span class="bilingual-en">🎉 Completed!</span></p><div class="ans" id="finalAns"><span class="bilingual-ko">정답</span><span class="bilingual-en">Answer</span> {final_ans}</div>
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
  var isEn = (document.documentElement.lang === 'en');
  if(exp.classList.contains('show')){{
    exp.classList.remove('show');
    btn.textContent = isEn ? '💡 View Explanation' : '💡 해설 보기';
  }} else {{
    exp.classList.add('show');
    btn.textContent = isEn ? '💡 Close Explanation' : '💡 해설 닫기';
  }}
}}

qs.forEach(q=>{{
  const ans=+q.dataset.ans;
  const exp=q.querySelector('.exp');
  if(exp) exp.innerHTML=q.dataset.exp;
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
  if (!name || name === '자유 학습자' || name === 'Guest Learner') {{
    var vid = '';
    try {{ vid = localStorage.getItem('mathedu_visitor_id') || ''; if (!vid) {{ vid = Math.random().toString(36).substring(2, 6).toUpperCase(); localStorage.setItem('mathedu_visitor_id', vid); }} }} catch(e) {{ vid = 'ANON'; }}
    name = ((document.documentElement.lang === 'en') ? 'Guest#' : '자유학습#') + vid;
    window._studentName = name;
  }}
  var qs = document.querySelectorAll('.q');
  var total = qs.length;
  var done = document.querySelectorAll('.q.done');
  var correct = pts;
  var current = done.length;
  if (total === 0) return;
  var url = window._sheetsApiUrl || '/api/progress';
  fetch(url, {{
    method: 'POST',
    mode: 'no-cors',
    keepalive: true,
    headers: {{'Content-Type': 'text/plain;charset=utf-8'}},
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
  var slug='{slug_js}' || window.location.pathname.split('/').filter(Boolean).pop().replace('.html','');
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
</script><script src="../mathedu-room.js"></script><script src="../mathedu-report.js"></script></body></html>"""

def _esc(s): return html.escape(str(s))

REPORT_WRAP_HTML = '''<div class="report-wrap" style="margin-top:10px;border-top:1px solid #e4e2e4;padding-top:10px">
<button class="report-btn" onclick="toggleReport(this)" style="background:transparent;color:#9aa6c0;border:1px solid #2e3850;border-radius:8px;padding:4px 12px;font-size:.75rem;cursor:pointer;transition:.15s" onmouseover="this.style.borderColor='#ff6b6b';this.style.color='#ff6b6b'" onmouseout="this.style.borderColor='#2e3850';this.style.color='#9aa6c0'">🚨 이 문제에 이상이 있어요</button>
<div class="report-form" style="display:none;margin-top:10px;text-align:left">
<div style="color:#9aa6c0;font-size:.75rem;margin-bottom:6px">어떤 부분이 이상한가요? 자세히 적어주세요.</div>
<textarea class="report-text" rows="3" placeholder="예: 보기 3번이 정답이 아닌 것 같습니다. / 문제의 조건이 모호합니다. / 계산 오류가 있습니다." style="width:100%;background:#ffffff;color:#1b1b1d;border:1px solid #c5c6cd;border-radius:8px;padding:8px;font-size:.85rem;resize:vertical;box-sizing:border-box"></textarea>
<div style="display:flex;gap:6px;margin-top:6px;justify-content:flex-end">
<button class="report-cancel" onclick="toggleReport(this)" style="background:transparent;color:#9aa6c0;border:1px solid #2e3850;border-radius:8px;padding:4px 10px;font-size:.75rem;cursor:pointer">취소</button>
<button class="report-submit" onclick="submitReport(this)" style="background:linear-gradient(90deg,#ff6b6b,#ee5a5a);color:#fff;border:none;border-radius:8px;padding:4px 12px;font-size:.75rem;cursor:pointer">신고 접수</button>
</div>
</div>
<div class="report-msg" style="display:none;color:#3ddc97;font-size:.75rem;margin-top:6px;text-align:right">✅ 신고가 접수되었어요. 확인 후 고칠게요!</div>
</div>'''

def _resolve_options_and_ans(opts_list, ans):
    if opts_list and len(opts_list) == 5:
        try:
            ans_idx = int(ans)
        except Exception:
            ans_idx = 1
        return opts_list, ans_idx
    
    try:
        val = int(ans)
    except Exception:
        val = 1
    
    if 1 <= val <= 5:
        options = ["$1$", "$2$", "$3$", "$4$", "$5$"]
        return options, val
    elif val > 5:
        start = max(1, val - 2)
        options = [f"${start + i}$" for i in range(5)]
        ans_idx = (val - start) + 1
        return options, ans_idx
    else:
        start = val - 2
        options = [f"${start + i}$" for i in range(5)]
        return options, 3

def _question_html(q):
    opts_list, ans_idx = _resolve_options_and_ans(q.get("options", []), q.get("answer", 1))
    exp = _esc(q.get("exp", "")).replace("\n", "<br>")
    exp_en = _esc(q.get("exp_en", "")).replace("\n", "<br>")
    exp_en_attr = f' data-exp-en="{exp_en}"' if exp_en else ""
    lvl_label = _esc(q.get("level_label") or "문항")
    lvl_label_en = _esc(q.get("level_label_en") or "Question")
    
    opts_en_list = q.get("options_en", [])
    opts_items = []
    for i, o in enumerate(opts_list):
        if i < len(opts_en_list) and opts_en_list[i]:
            opts_items.append(f'<div class="opt"><span class="n">{i+1}</span><span class="bilingual-ko">{_esc(o)}</span><span class="bilingual-en">{_esc(opts_en_list[i])}</span></div>')
        else:
            opts_items.append(f'<div class="opt"><span class="n">{i+1}</span>{_esc(o)}</div>')
    opts = "".join(opts_items)
    body = f'<div class="opts">{opts}</div>'
    
    stem_ko = _esc(q.get("stem", ""))
    stem_en = _esc(q.get("stem_en", ""))
    if stem_en:
        stem_html = f'<span class="bilingual-ko">{stem_ko}</span><div class="bilingual-en">{stem_en}</div>'
    else:
        stem_html = stem_ko

    return (f'<div class="q" data-ans="{ans_idx}" data-exp="{exp}"{exp_en_attr}>'
            f'<div class="lvl"><span class="bilingual-ko">{lvl_label}</span><span class="bilingual-en">{lvl_label_en}</span></div>'
            f'<div class="stem">{stem_html}</div>'
            f'{body}'
            f'<div class="q-actions" style="margin-top:10px;display:flex;justify-content:flex-end">'
            f'<button type="button" class="exp-toggle-btn" onclick="toggleExp(this)">💡 해설 보기</button>'
            f'</div>'
            f'<div class="exp"></div>'
            f'{REPORT_WRAP_HTML}</div>')

def _level_html(lvl):
    know = ""
    if lvl.get("knowledge"):
        know_en = f'<div class="bilingual-en"><b>Prerequisite Knowledge:</b> {_esc(lvl["knowledge_en"])}</div>' if lvl.get("knowledge_en") else ""
        know = (f'<div class="know"><h3>먼저 알아야 할 지식</h3>{_esc(lvl["knowledge"])}{know_en}</div>')
    q_list = list(lvl.get("questions", []))
    if q_list and str(lvl.get("stage", "")) == "level1":
        q0 = dict(q_list[0])
        if not q0.get("level_label"):
            q0["level_label"] = lvl.get("title") or "🔰 1단계 · [초등 기초 직관·사칙연산 디딤돌]"
            q0["level_label_en"] = lvl.get("title_en") or "🔰 Step 1 · [Elementary Intuition Scaffolding]"
        q_list[0] = q0
    qs = "".join(_question_html(q) for q in q_list)
    t_ko = _esc(lvl.get("title", ""))
    t_en = f'<span class="bilingual-en">{_esc(lvl["title_en"])}</span>' if lvl.get("title_en") else ""
    return f'<h2>{t_ko}{t_en}</h2>{know}{qs}'

def _tracking_html(quiz_slug, sheets_api_url=''):
    """Full-screen name gate with bilingual support and Guest Free Pass."""
    slug_js = quiz_slug.replace("'", "\\'")
    html = (
        '<div id="trackFull" style="position:fixed;inset:0;z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;background:rgba(252,248,250,0.97);padding:24px;text-align:center">'
        '<div id="trackFullLangSwitcher" style="position:absolute;top:18px;left:20px;z-index:100;display:inline-flex;align-items:center;background:#f0edef;border:1.5px solid #e4e2e4;border-radius:24px;padding:3px 4px;gap:3px;box-shadow:0 4px 16px rgba(0,0,0,.4);backdrop-filter:blur(10px)">'
        '<button type="button" id="btnTrackFullLangKo" onclick="toggleModalLang(\'ko\')" style="background:#38bdf8;color:#0b1020;border:none;border-radius:18px;padding:5px 12px;font-size:0.82rem;font-weight:800;cursor:pointer;transition:.15s">🇰🇷 한국어</button>'
        '<button type="button" id="btnTrackFullLangEn" onclick="toggleModalLang(\'en\')" style="background:transparent;color:#cbd5e1;border:none;border-radius:18px;padding:5px 12px;font-size:0.82rem;font-weight:700;cursor:pointer;transition:.15s">🌐 English</button>'
        '</div>'
        '<h2 style="background:linear-gradient(90deg,#7cc4ff,#a78bfa);-webkit-background-clip:text;background-clip:text;color:transparent;font-size:1.6rem;margin:0 0 8px">📘 mathedu</h2>'
        '<div id="modalCenterLangSwitcher" style="margin:4px 0 16px;display:inline-flex;align-items:center;justify-content:center;background:#f0edef;border:1.5px solid #e4e2e4;border-radius:28px;padding:4px 8px;gap:5px;box-shadow:0 6px 20px rgba(0,0,0,.45);backdrop-filter:blur(10px);z-index:10">'
        '<span style="font-size:0.83rem;color:#45464d;font-weight:700;margin:0 4px 0 8px;display:inline-flex;align-items:center;gap:4px"><span>🌐</span><span class="bilingual-ko">언어 선택:</span><span class="bilingual-en">Language:</span></span>'
        '<button type="button" id="btnModalCenterLangKo" onclick="toggleModalLang(\'ko\')" style="background:linear-gradient(135deg,#38bdf8 0%,#818cf8 100%);color:#0b1020;border:none;border-radius:20px;padding:6px 16px;font-size:0.86rem;font-weight:800;cursor:pointer;transition:all .18s;box-shadow:0 2px 10px rgba(56,189,248,.45)">🇰🇷 한국어</button>'
        '<button type="button" id="btnModalCenterLangEn" onclick="toggleModalLang(\'en\')" style="background:transparent;color:#cbd5e1;border:none;border-radius:20px;padding:6px 16px;font-size:0.86rem;font-weight:700;cursor:pointer;transition:all .18s">🌐 English</button>'
        '</div>'
        '<div id="topGuestFreePassRow" style="margin:12px 0 16px;width:100%;max-width:440px;display:flex;flex-direction:column;align-items:center;gap:10px">'
        '<button type="button" id="btnTeacherPreviewInModal" onclick="startFreePractice()" style="width:100%;max-width:420px;background:linear-gradient(135deg,#38bdf8 0%,#818cf8 50%,#a855f7 100%);color:#070d1e;border:2px solid #ffffff;border-radius:14px;padding:14px 22px;font-size:1.1rem;font-weight:900;cursor:pointer;transition:all .2s ease;box-shadow:0 0 24px rgba(56,189,248,.7),0 6px 18px rgba(0,0,0,.5);display:inline-flex;align-items:center;justify-content:center;gap:8px;letter-spacing:-0.2px" onmouseover="this.style.transform=\'translateY(-2px) scale(1.03)\';this.style.boxShadow=\'0 0 32px rgba(56,189,248,.95),0 8px 24px rgba(0,0,0,.6)\'" onmouseout="this.style.transform=\'none\';this.style.boxShadow=\'0 0 24px rgba(56,189,248,.7),0 6px 18px rgba(0,0,0,.5)\'">'
        '<span class="bilingual-ko">🚀 가입 없이 바로 문제 열람 & 자유 풀기 ➔</span><span class="bilingual-en">🚀 Free Practice (No Login Required) ➔</span>'
        '</button>'
        '<div style="font-size:0.81rem;color:#94a3b8;display:flex;align-items:center;gap:8px;width:100%;max-width:380px"><span style="flex:1;height:1px;background:rgba(255,255,255,.15)"></span><span><span class="bilingual-ko">또는 이름을 입력하고 학습 기록 저장</span><span class="bilingual-en">Or enter name to save your progress</span></span><span style="flex:1;height:1px;background:rgba(255,255,255,.15)"></span></div>'
        '</div>'
        '<h3 style="color:#131b2e;margin:0 0 6px;font-weight:800"><span class="bilingual-ko">📝 먼저 이름을 입력하세요</span><span class="bilingual-en">📝 Please enter your name first</span></h3>'
        '<p style="color:#45464d;font-size:.9rem;margin:0 0 20px"><span class="bilingual-ko">이름을 입력해야 학습 기록이 저장됩니다.</span><span class="bilingual-en">Your learning progress will be saved under this name.</span></p>'
        '<div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap">'
        '<input type="text" id="studentName" placeholder="이름 입력" autofocus style="background:#ffffff;color:#1b1b1d;border:1.5px solid #c5c6cd;border-radius:10px;padding:12px 16px;font-size:1.05rem;min-width:200px;text-align:center">'
        '<button class="btn" onclick="registerName()" style="font-size:1.05rem;padding:12px 24px"><span class="bilingual-ko">시작하기</span><span class="bilingual-en">Start</span></button>'
        '</div></div>'
        '<script>'
        'window._studentName="";'
        'window._sheetsApiUrl="' + sheets_api_url + '";'
        'function toggleModalLang(l){'
        'document.documentElement.lang=l;'
        'try{localStorage.setItem("mathedu_lang",l);localStorage.setItem("mathedu_lang_manual","true");}catch(e){}'
        'var bKo=document.getElementById("btnTrackFullLangKo");var bEn=document.getElementById("btnTrackFullLangEn");'
        'if(bKo&&bEn){if(l==="en"){bKo.style.background="transparent";bKo.style.color="#45464d";bKo.style.fontWeight="700";bEn.style.background="#38bdf8";bEn.style.color="#0b1020";bEn.style.fontWeight="800";}else{bKo.style.background="#38bdf8";bKo.style.color="#0b1020";bKo.style.fontWeight="800";bEn.style.background="transparent";bEn.style.color="#45464d";bEn.style.fontWeight="700";}}'
        'var cKo=document.getElementById("btnModalCenterLangKo");var cEn=document.getElementById("btnModalCenterLangEn");'
        'if(cKo&&cEn){if(l==="en"){cKo.style.background="transparent";cKo.style.color="#45464d";cKo.style.fontWeight="700";cKo.style.boxShadow="none";cEn.style.background="linear-gradient(135deg,#38bdf8 0%,#818cf8 100%)";cEn.style.color="#0b1020";cEn.style.fontWeight="800";cEn.style.boxShadow="0 2px 10px rgba(56,189,248,.45)";}else{cKo.style.background="linear-gradient(135deg,#38bdf8 0%,#818cf8 100%)";cKo.style.color="#0b1020";cKo.style.fontWeight="800";cKo.style.boxShadow="0 2px 10px rgba(56,189,248,.45)";cEn.style.background="transparent";cEn.style.color="#45464d";cEn.style.fontWeight="700";cEn.style.boxShadow="none";}}'
        'var sn=document.getElementById("studentName");if(sn)sn.placeholder=(l==="en")?"Enter name":"이름 입력";'
        'if(window.setBoardLanguage)window.setBoardLanguage(l);else if(window.setBoardLang)window.setBoardLang(l,true);'
        '}'
        '(function(){var cur="ko";try{var p=new URLSearchParams(window.location.search).get("lang");if(p==="en"||p==="ko"){cur=p;}else{var man=localStorage.getItem("mathedu_lang_manual")==="true";var sto=localStorage.getItem("mathedu_lang");if(man&&(sto==="en"||sto==="ko")){cur=sto;}else{var tz="";try{tz=Intl.DateTimeFormat().resolvedOptions().timeZone||"";}catch(e){}if(tz&&tz!=="Asia/Seoul"&&tz!=="ROK"&&tz!=="Asia/Pyongyang"){cur="en";}else{var l=(navigator.languages&&navigator.languages[0])||navigator.language||"";if(l&&l.toLowerCase().indexOf("ko")!==0)cur="en";}}}}catch(e){}if(cur==="en"){document.documentElement.lang="en";toggleModalLang("en");}})();'
        'function getAnonVisitorName(){var vid="";try{vid=localStorage.getItem("mathedu_visitor_id")||"";if(!vid){vid=Math.random().toString(36).substring(2,6).toUpperCase();localStorage.setItem("mathedu_visitor_id",vid);}}catch(e){vid="ANON";}return((document.documentElement.lang==="en")?"Guest#":"자유학습#")+vid;}'
        'function startFreePractice(){window._studentName=getAnonVisitorName();var tf=document.getElementById("trackFull");if(tf)tf.remove();if(window.sendProgress)sendProgress();if(window.MathJax&&MathJax.typesetPromise)MathJax.typesetPromise();}'
        'function registerName(){'
        'var n=document.getElementById("studentName").value.trim();'
        'if(!n){alert((document.documentElement.lang==="en")?"Please enter your name":"이름을 입력하세요");return;}'
        'window._studentName=n;'
        'document.getElementById("trackFull").remove();'
        'sendProgress();'
        'if(window.MathJax&&MathJax.typesetPromise){MathJax.typesetPromise();}'
        '}'
        'function sendProgress(){'
        'var name=(window._studentName||"").trim();'
        'if(!name||name==="자유 학습자"||name==="Guest Learner"){name=getAnonVisitorName();window._studentName=name;}'
        'var qs=document.querySelectorAll(".q");'
        'var total=qs.length;'
        'var done=document.querySelectorAll(".q.done");'
        'var correct=0;'
        'done.forEach(function(q){if(q.querySelector(".opt.correct"))correct++;});'
        'if(total===0)return;'
        'fetch(window._sheetsApiUrl,{'
        'method:"POST",mode:"no-cors",keepalive:true,headers:{"Content-Type":"text/plain;charset=utf-8"},'
        'body:JSON.stringify({quiz_slug:"' + slug_js + '",student_name:name,current_step:done.length,total_steps:total,correct:correct})'
        '}).catch(function(){});'
        '}'
        'document.querySelectorAll(".q").forEach(function(q){'
        'q.addEventListener("click",function(e){'
        'var opt=e.target.closest(".opt");'
        'if(opt){setTimeout(sendProgress,50);}'
        '});'
        '});'
        'document.getElementById("studentName").addEventListener("keydown",function(e){if(e.key==="Enter")registerName();});'
        '</script>'
    )
    return html



def generate_html(data):
    sym_items = []
    for s in data.get("symbols", []):
        stxt = str(s.get("sym", "")).strip()
        if stxt and "$" not in stxt and not re.search(r'[가-힣]', stxt):
            stxt = f"${stxt}$"
        stxt = re.sub(r'(?<![a-zA-Z\\])\\frac(?=\{)', r'\\dfrac', stxt)
        desc_txt = _esc(s.get("desc", ""))
        desc_en = f'<div class="bilingual-en">{_esc(s["desc_en"])}</div>' if s.get("desc_en") else ""
        sym_items.append(f'<div><b>{stxt}</b> — {desc_txt}{desc_en}</div>')
    sym = "".join(sym_items)
    symbols_block = (f'<h2>🔰 제0단계 · 수학 기호<span class="bilingual-en">🔰 Step 0 · Mathematical Symbols</span></h2><div class="sym">{sym}</div>' if sym else "")
    levels_block = "".join(_level_html(l) for l in data.get("levels", []))
    f = data.get("final", {})
    fopts_list, fans_idx = _resolve_options_and_ans(f.get("options", []), f.get("answer", 1))
    fexp = _esc(f.get("exp", "")).replace("\n", "<br>")
    fexp_en = _esc(f.get("exp_en", "")).replace("\n", "<br>")
    fexp_en_attr = f' data-exp-en="{fexp_en}"' if fexp_en else ""
    fsol = f.get("solution", "")
    if not isinstance(fsol, str): fsol = str(fsol)
    fsol_en = f.get("solution_en", "")
    if "bilingual-ko" not in fsol:
        if not fsol_en:
            fsol_en = (
                "<h4>📋 [Problem Analysis & Core Concepts]</h4>"
                "<p>This problem evaluates step-by-step mathematical reasoning and conceptual synthesis from fundamental rules to the final derivation.</p>"
                "<h4>📐 [Step-by-Step Rigorous Derivation]</h4>"
                f"<p>{fexp_en or fexp}</p>"
                "<h4>✨ [Conclusion & Key Takeaway]</h4>"
                "<p>By combining the intermediate results derived in the preceding scaffolding steps, we obtain the exact final answer.</p>"
            )
        try:
            if "math-visual-diagram" not in fsol:
                import visual_diagram_engine
                step_summaries_ko = []
                for _lv in data.get("levels", []):
                    _lt = str(_lv.get("title", "")).replace("\x09o", r"\to")
                    _qs = _lv.get("questions") or []
                    if _qs:
                        _q0 = _qs[0]
                        _qo, _qa = _resolve_options_and_ans(_q0.get("options", []), _q0.get("answer", 1))
                        _qat = _qo[int(_qa) - 1] if 1 <= int(_qa) <= len(_qo) else ""
                        step_summaries_ko.append(f"{_lt} ⇒ {_qat}")
                    else:
                        step_summaries_ko.append(_lt)
                _ans_for_vis = fopts_list[int(fans_idx) - 1] if 1 <= int(fans_idx) <= len(fopts_list) else str(f.get("answer", 1))
                _slug_v = str(data.get("slug", "quiz")).strip()
                _vis_ko = visual_diagram_engine.build_visual_and_schematic_block(
                    _slug_v, str(data.get("title", "")), step_summaries_ko, _ans_for_vis, fsol, lang="ko"
                )
                _vis_en = visual_diagram_engine.build_visual_and_schematic_block(
                    _slug_v, str(data.get("title_en") or data.get("title", "")), step_summaries_ko, _ans_for_vis, fsol_en, lang="en"
                )
                fsol = _vis_ko + "\n" + fsol
                fsol_en = _vis_en + "\n" + fsol_en
        except Exception as _ve:
            pass
        fsol_combined = f'<div class="bilingual-ko">{fsol}</div><div class="bilingual-en">{fsol_en}</div>'
    else:
        fsol_combined = fsol

    if len(fexp) < 500:
        _short_ko = f.get("exp", "")
        _short_en = f.get("exp_en") or _short_ko
        _full_ko = f'<b>📌 [최종 본문항 핵심 요약]</b><br>{_short_ko}<hr style="border:none;border-top:1px dashed #cbd5e1;margin:12px 0">{fsol}'
        _full_en = f'<b>📌 [Final Problem Core Summary]</b><br>{_short_en}<hr style="border:none;border-top:1px dashed #cbd5e1;margin:12px 0">{fsol_en}'
        fexp = _esc(_full_ko)
        fexp_en = _esc(_full_en)
        fexp_en_attr = f' data-exp-en="{fexp_en}"'

    diagram_html = ""
    if f.get("diagram"):
        diagram_html = f'<div class="diagram">{f["diagram"]}</div>'
    figure_html = ""
    if f.get("figure"):
        figure_html = f'<div class="figure"><img src="{_esc(f["figure"])}" alt="문제 그림" style="max-width:100%;border-radius:10px"></div>'
    
    fopts = "".join(
        f'<div class="opt"><span class="n">{i+1}</span>{_esc(o)}</div>'
        for i, o in enumerate(fopts_list))
    fbody = f'<div class="opts">{fopts}</div>'
    try:
        final_ans = fopts_list[int(fans_idx) - 1]
    except Exception:
        final_ans = str(f.get("answer", 1))

    fstem_ko = _esc(f.get("stem", ""))
    fstem_en = _esc(f.get("stem_en", ""))
    fstem_html = f'<span class="bilingual-ko">{fstem_ko}</span><div class="bilingual-en">{fstem_en}</div>' if fstem_en else fstem_ko

    solution_block = (
        f'<h2>🎯 최종 문제 + 상세 풀이<span class="bilingual-en">🎯 Final Official Exam Problem & Complete Solution</span></h2>'
        f'{diagram_html}'
        f'{figure_html}'
        f'<div class="sol">{fsol_combined}</div>'
        f'<div class="q" data-ans="{fans_idx}" data-exp="{fexp}"{fexp_en_attr}>'
        f'<div class="lvl"><span class="bilingual-ko">최종 본문항</span><span class="bilingual-en">Final Exam Problem</span></div>'
        f'<div class="stem">{fstem_html}</div>'
        f'{fbody}'
        f'<div class="q-actions" style="margin-top:10px;display:flex;justify-content:flex-end">'
        f'<button type="button" class="exp-toggle-btn" onclick="toggleExp(this)">💡 해설 보기</button>'
        f'</div>'
        f'<div class="exp"></div>'
        f'{REPORT_WRAP_HTML}</div>')
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
    # ★ 원본 문제 상단 표시 블록: ac8dc374.html 표준 규격 적용
    slug_val = str(data.get("slug", "")).strip()
    orig_img = data.get("original_image") or data.get("image") or data.get("figure") or f.get("figure") or ""
    
    # 디스크에 img_{slug}.png가 존재하면 자동으로 원본 이미지로 지정
    if not orig_img and slug_val:
        candidate_img = f"img_{slug_val}.png"
        board_dir_check = os.path.join(os.path.dirname(os.path.abspath(__file__)), "board", candidate_img)
        if os.path.exists(board_dir_check) or os.path.exists(os.path.join("board", candidate_img)):
            orig_img = candidate_img

    orig_text = data.get("original_content") or data.get("original_text") or f.get("stem") or data.get("content") or ""
    
    orig_media_html = ""
    orig_text_html = ""
    if orig_img:
        img_src = str(orig_img).strip()
        if img_src.startswith('/board/'):
            img_src = img_src[7:]
        orig_media_html = f'<div class="orig-media"><img src="{_esc(img_src)}" alt="{_esc(data.get("title", "수학"))} 원본 문제"></div>'
    elif orig_text:
        clean_text = _esc(str(orig_text)).replace("\n", "<br>")
        options = f.get("options", [])
        opts_html = ""
        if options:
            circle_nums = ["①", "②", "③", "④", "⑤"]
            opts_items = "".join(f'<div style="flex:1;min-width:110px"><b>{circle_nums[i] if i < 5 else f"({i+1})"}</b> {_esc(opt)}</div>' for i, opt in enumerate(options))
            opts_html = f'<div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:14px;padding-top:12px;border-top:1px dashed #94a3b8;font-size:0.95rem;color:#0f172a;">{opts_items}</div>'

        orig_text_html = (
            f'<div class="orig-media" style="margin:12px 0;">'
            f'<div class="exam-paper-sheet" style="background:#ffffff;color:#0f172a;border-radius:12px;padding:22px 26px;border:1.5px solid #334155;box-shadow:0 8px 24px rgba(0,0,0,0.35);text-align:left;line-height:1.8;font-family:\'Apple SD Gothic Neo\',\'Malgun Gothic\',sans-serif;">'
            f'<div style="font-weight:700;font-size:1.05rem;color:#0f172a;margin-bottom:6px;">{clean_text}</div>'
            f'{opts_html}'
            f'</div></div>'
        )
        
    original_block = ""
    if orig_media_html or orig_text_html:
        original_block = (
            f'<!-- ★ 원본 문제 카드: 원본 그림 우선 표시 -->\n'
            f'<div class="orig-card">\n'
            f'<div class="orig-tag">📌 원본 문제 (오늘의 목표)<span class="bilingual-en">📌 Original Problem (Today\'s Goal)</span></div>\n'
            f'{orig_media_html}\n'
            f'{orig_text_html}\n'
            f'<div class="orig-tip">💡 아래 0단계 기초 개념부터 차근차근 해결해 나가면 원본 문제를 완벽하게 풀 수 있습니다!<span class="bilingual-en">💡 Step-by-step scaffolding will guide you to master this problem completely!</span></div>\n'
            f'</div>'
        )

    tracking_block = _tracking_html(data.get("slug", ""), _sheets_url)
    slug_js = data.get("slug", "").replace("'", "\\'")
    
    # ★ min7014 수학자료실 공식 연계 심층 학습 자료 매칭
    search_corpus = f"{data.get('title', '')} {data.get('original_content', '')} {data.get('content', '')} {f.get('stem', '')}"
    min7014_materials_block = ""
    visual_tip_html = ""
    try:
        matched_items = min7014_matcher.match_materials(search_corpus, limit=4)
        min7014_materials_block = min7014_matcher.generate_addon_card_html(matched_items, data.get("title", ""))
        v_tip = min7014_matcher.get_visual_tip(search_corpus, matched_items)
        if v_tip:
            visual_tip_html = f'<div class="min-visual-tip">{v_tip}</div>\n'
    except Exception as e:
        min7014_materials_block = ""
        visual_tip_html = ""

    if visual_tip_html and original_block:
        original_block = original_block + "\n" + visual_tip_html

    raw_title = _esc(data.get("title", "퀴즈"))
    title_en = _esc(data.get("title_en", ""))
    if title_en:
        h1_title = f'<span class="bilingual-ko">{raw_title}</span><span class="bilingual-en">📘 {title_en}</span>'
    else:
        h1_title = raw_title

    html = TEMPLATE.format(
        title=raw_title,
        h1_title=h1_title,
        original_block=original_block,
        symbols_block=symbols_block, levels_block=levels_block,
        solution_block=solution_block, final_ans=_esc(final_ans),
        tracking_block=tracking_block,
        min7014_materials_block=min7014_materials_block,
        slug_js=slug_js)
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
