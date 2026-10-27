import sys
sys.stdout.reconfigure(encoding='utf-8')
import glob
import os
import re

STITCH_FONTS_HEAD = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />"""

STITCH_CSS = """<style>
/* ════════════════════════════════════════════════════════════════════════
   ✨ Google Stitch Screen: projects/8555798074171219045/screens/bc0f63eb3a354cee8f964ce2bc461f3b
   "Mathematical Clarity & Dynamic Geometry" — Exact Component & Token System
   ════════════════════════════════════════════════════════════════════════ */
:root {
  --bg: #fcf8fa;
  --card: #ffffff;
  --card2: #f6f3f5;
  --card3: #f0edef;
  --card-high: #eae7e9;
  --line: #e4e2e4;
  --line-strong: #c5c6cd;
  --txt: #1b1b1d;
  --sub: #45464d;
  --primary: #000000;
  --navy: #131b2e;
  --accent: #006398;
  --accent-sky: #38BDF8;
  --accent2: #4F46E5;
  --good: #10B981;
  --good-dark: #059669;
  --bad: #ba1a1a;
  --gold: #F59E0B;
  --gold-dark: #B45309;
  --glass-blur: 20px;
  --glass-shadow: 0 1px 4px rgba(0, 0, 0, 0.04), 0 2px 10px rgba(19, 27, 46, 0.03);
  --radius: 16px;
}

*, *::before, *::after {
  box-sizing: border-box;
}

html, body {
  overflow-x: hidden !important;
  max-width: 100vw;
  width: 100%;
}

body {
  margin: 0;
  color: var(--txt);
  line-height: 1.65;
  font-family: 'Inter', 'Pretendard', -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", system-ui, sans-serif;
  background-color: var(--bg);
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
}

.material-symbols-outlined {
  font-variation-settings: 'FILL' 0, 'wght' 500, 'GRAD' 0, 'opsz' 24;
  vertical-align: middle;
  line-height: 1;
  user-select: none;
}

.wrap {
  max-width: 768px;
  width: 100%;
  margin: 0 auto;
  padding: 88px 16px 104px;
  overflow-x: hidden;
  box-sizing: border-box;
}

/* ── 1. Fixed Top Header (Exact screens/bc0f63eb3a354cee8f964ce2bc461f3b) ── */
.stitch-app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(252, 248, 250, 0.88);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  box-shadow: 0 1px 8px rgba(0, 0, 0, 0.04);
  border-bottom: 1px solid rgba(228, 226, 228, 0.6);
}

.stitch-app-header-inner {
  max-width: 768px;
  height: 72px;
  margin: 0 auto;
  padding: 0 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.stitch-brand-link {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
  text-decoration: none;
  color: var(--txt);
}

.stitch-brand-logo {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  object-fit: contain;
  flex-shrink: 0;
}

.stitch-brand-text {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.stitch-brand-title {
  font-family: 'Plus Jakarta Sans', 'Pretendard', sans-serif;
  font-size: 1.05rem;
  font-weight: 800;
  color: var(--txt);
  letter-spacing: -0.02em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.25;
}

.stitch-brand-sub {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 2px;
}

.stitch-brand-pill {
  display: inline-flex;
  align-items: center;
  padding: 2px 7px;
  border-radius: 9999px;
  background: rgba(0, 99, 152, 0.10);
  color: var(--accent);
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.01em;
}

.stitch-brand-code {
  font-family: 'Space Grotesk', monospace;
  font-size: 0.7rem;
  color: var(--sub);
  font-weight: 600;
}

.stitch-header-actions {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
}

.stitch-lang-toggle {
  min-width: 40px;
  min-height: 40px;
  border-radius: 12px;
  background: var(--card3);
  color: var(--txt);
  font-size: 0.76rem;
  font-weight: 700;
  border: none;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 4px 8px;
  transition: background 0.15s;
}

.stitch-lang-toggle:hover {
  background: var(--card-high);
}

.stitch-streak-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 11px;
  border-radius: 9999px;
  background: #FEF3C7;
  color: #B45309;
  font-size: 0.76rem;
  font-weight: 700;
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.15);
  cursor: pointer;
}

.stitch-profile-btn {
  width: 34px;
  height: 34px;
  border-radius: 9999px;
  background: #000000;
  color: #ffffff;
  border: none;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: opacity 0.15s;
}

.stitch-profile-btn:hover {
  opacity: 0.85;
}

/* Legacy topbar & score hidden or integrated */
.topbar { display: none !important; }
.score { display: none !important; }

/* ── 2. Stitch Hero Identity Card ── */
.stitch-hero-card {
  background: #ffffff;
  border-radius: var(--radius);
  padding: 20px;
  box-shadow: var(--glass-shadow);
  margin-bottom: 10px;
  position: relative;
  overflow: hidden;
}

.stitch-hero-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 6px;
}

.stitch-hero-brand {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--accent);
  font-size: 0.76rem;
  font-weight: 700;
  letter-spacing: 0.01em;
}

.stitch-free-pill {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  border-radius: 9999px;
  background: rgba(16, 185, 129, 0.10);
  color: #059669;
  font-size: 0.72rem;
  font-weight: 700;
}

.stitch-hero-card h1 {
  font-family: 'Plus Jakarta Sans', 'Pretendard', sans-serif;
  font-size: 1.55rem;
  font-weight: 800;
  letter-spacing: -0.025em;
  line-height: 1.28;
  margin: 4px 0 8px;
  color: var(--txt);
}

.stitch-hero-card h1 .stitch-h1-main {
  display: block;
  color: var(--txt);
}

.stitch-hero-card h1 .stitch-h1-accent {
  display: block;
  color: var(--accent);
  margin-top: 2px;
}

.stitch-hero-card .lead {
  font-size: 0.85rem;
  color: var(--sub);
  line-height: 1.55;
  margin: 0 0 10px;
}

.stitch-chip-scroll {
  display: flex;
  align-items: center;
  gap: 6px;
  overflow-x: auto;
  padding: 4px 2px;
  margin: 2px -2px 0;
  scrollbar-width: none;
}
.stitch-chip-scroll::-webkit-scrollbar { display: none; }

.stitch-feature-chip {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 5px 11px;
  border-radius: 9999px;
  background: var(--card3);
  color: var(--txt);
  font-size: 0.74rem;
  font-weight: 600;
  text-decoration: none;
  border: none;
  cursor: pointer;
  transition: background 0.15s;
}

.stitch-feature-chip:hover {
  background: var(--card-high);
}

.stitch-bento-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 6px;
  margin-top: 14px;
  padding: 12px 10px;
  background: var(--card2);
  border-radius: 12px;
}

.stitch-bento-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.stitch-bento-val {
  font-family: 'Plus Jakarta Sans', 'Space Grotesk', sans-serif;
  font-size: 1.15rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.stitch-bento-lbl {
  font-size: 0.65rem;
  color: var(--sub);
  font-weight: 600;
  margin-top: 2px;
}

.stitch-progress-wrap {
  grid-column: 1 / -1;
  margin-top: 6px;
}

.bar {
  height: 6px;
  background: #e4e2e4;
  border-radius: 9999px;
  overflow: hidden;
  width: 100%;
  display: block;
}

.bar > i {
  display: block;
  height: 100%;
  width: 0;
  background: linear-gradient(90deg, var(--accent), #10b981);
  border-radius: 9999px;
  transition: width 0.3s ease;
}

/* ── 3. Gamification / Daily Streak Strip Card ── */
.stitch-streak-card {
  background: #ffffff;
  border-radius: var(--radius);
  padding: 12px 16px;
  box-shadow: var(--glass-shadow);
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.stitch-streak-left {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.stitch-flame-circle {
  width: 40px;
  height: 40px;
  border-radius: 9999px;
  background: #FEF3C7;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stitch-streak-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.stitch-streak-title-row {
  display: flex;
  align-items: center;
  gap: 6px;
}

.stitch-streak-title {
  font-family: 'Plus Jakarta Sans', 'Pretendard', sans-serif;
  font-size: 0.92rem;
  font-weight: 800;
  color: var(--txt);
}

.stitch-lvl-badge {
  font-size: 0.65rem;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 4px;
  background: var(--card3);
  color: var(--sub);
}

.stitch-streak-sub {
  font-size: 0.78rem;
  color: var(--sub);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.stitch-streak-actions {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
}

.stitch-circle-icon-btn {
  width: 34px;
  height: 34px;
  border-radius: 9999px;
  background: var(--card3);
  color: var(--txt);
  border: none;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s;
}

.stitch-circle-icon-btn:hover {
  background: var(--card-high);
}

/* ── 4. Visual Proof Archive Card (Dandelin Spheres / Visual Proof Spotlight) ── */
.stitch-dandelin-card {
  background: #ffffff;
  border-radius: var(--radius);
  padding: 16px 20px;
  box-shadow: var(--glass-shadow);
  margin-bottom: 14px;
}

.stitch-card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 10px;
}

.stitch-card-head-left {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Space Grotesk', 'Pretendard', sans-serif;
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--txt);
}

.stitch-card-head-right {
  font-size: 0.74rem;
  font-weight: 700;
  color: var(--accent);
  cursor: pointer;
}

.stitch-visual-canvas {
  border-radius: 12px;
  overflow: hidden;
  background: var(--navy);
  display: flex;
  flex-direction: column;
}

.stitch-visual-banner {
  width: 100%;
  height: 168px;
  position: relative;
  background-size: cover;
  background-position: center;
  background-color: #131b2e;
}

.stitch-visual-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.78) 0%, rgba(0,0,0,0.22) 55%, transparent 100%);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 16px;
}

.stitch-visual-eyebrow {
  font-size: 0.68rem;
  font-weight: 700;
  color: #38BDF8;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.stitch-visual-headline {
  font-family: 'Plus Jakarta Sans', 'Pretendard', sans-serif;
  font-size: 1.05rem;
  font-weight: 800;
  color: #ffffff;
  margin: 2px 0 0;
  line-height: 1.3;
}

.stitch-visual-drawer {
  padding: 14px 16px;
  background: var(--card2);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stitch-visual-desc {
  font-size: 0.82rem;
  color: var(--sub);
  line-height: 1.6;
  margin: 0;
}

.stitch-quote-box {
  padding: 10px 12px;
  border-radius: 8px;
  background: #ffffff;
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.stitch-quote-text {
  font-size: 0.8rem;
  color: var(--txt);
  font-weight: 500;
  font-style: italic;
  margin: 0;
  line-height: 1.5;
}

/* ── 5. Original Exam Problem Card (.orig-card — Today's Recommended Dynamic Geometry Style) ── */
.orig-card {
  background: #ffffff;
  border-radius: var(--radius);
  padding: 18px 20px;
  margin: 0 0 14px;
  box-shadow: var(--glass-shadow);
  border: none;
}

.orig-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  flex-wrap: wrap;
  gap: 8px;
}

.orig-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: transparent;
  color: var(--txt);
  font-family: 'Plus Jakarta Sans', 'Pretendard', sans-serif;
  font-size: 0.98rem;
  font-weight: 800;
  padding: 0;
  box-shadow: none;
}

.orig-badge {
  font-size: 0.74rem;
  color: var(--accent);
  font-weight: 700;
  background: rgba(0, 99, 152, 0.12);
  padding: 3px 10px;
  border-radius: 9999px;
  font-family: 'Space Grotesk', 'Pretendard', sans-serif;
}

.orig-grid {
  background: var(--card2);
  border-radius: 12px;
  padding: 16px;
  display: grid;
  grid-template-columns: 1.02fr 0.98fr;
  gap: 16px;
  align-items: start;
}

.orig-col-media {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.orig-media-tabs {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.orig-tab-btn {
  background: #ffffff;
  color: var(--sub);
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 5px 11px;
  font-size: .78rem;
  font-weight: 700;
  cursor: pointer;
  transition: .15s;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.orig-tab-btn.active {
  background: #000000;
  color: #ffffff;
  border-color: #000000;
}

.orig-media-frame {
  background: #ffffff;
  border-radius: 10px;
  padding: 10px;
  text-align: center;
  border: 1px solid var(--line);
  overflow: hidden;
}

.orig-media-frame img, .orig-media-frame svg {
  max-width: 100%;
  max-height: 400px;
  width: auto;
  height: auto;
  border-radius: 6px;
  display: block;
  margin: 0 auto;
}

.orig-media-sub {
  text-align: center;
  font-size: .75rem;
  color: var(--sub);
}

.orig-col-desc {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.orig-text-box {
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 14px 16px;
  font-size: .9rem;
  line-height: 1.65;
  color: var(--txt);
}

.orig-text-box h4 {
  margin: 0 0 6px;
  color: var(--accent);
  font-size: .88rem;
  font-weight: 800;
}

.orig-tip {
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 10px 14px;
  font-size: .82rem;
  color: var(--txt);
  line-height: 1.55;
}

.min-visual-tip {
  background: var(--card2);
  border-radius: 10px;
  padding: 12px 16px;
  margin-top: 12px !important;
  font-size: .82rem;
  color: var(--sub);
  line-height: 1.6;
}

.stitch-orig-cta-stack {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 12px;
}

.stitch-cta-black {
  width: 100%;
  height: 44px;
  border-radius: 10px;
  background: #000000;
  color: #ffffff;
  font-family: 'Plus Jakarta Sans', 'Pretendard', sans-serif;
  font-size: 0.88rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  text-decoration: none;
  border: none;
  cursor: pointer;
  transition: background 0.15s;
}

.stitch-cta-black:hover {
  background: #262626;
}

.stitch-cta-sub-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.stitch-cta-gray {
  height: 40px;
  border-radius: 10px;
  background: var(--card3);
  color: var(--txt);
  font-size: 0.8rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  text-decoration: none;
  border: none;
  cursor: pointer;
  transition: background 0.15s;
}

.stitch-cta-gray:hover {
  background: var(--card-high);
}

/* ── 6. Two-Pillar User Gateway Cards (Teacher & Student Quick Action) ── */
.stitch-gateway-grid {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.stitch-gateway-card {
  background: #ffffff;
  border-radius: var(--radius);
  padding: 18px 20px;
  box-shadow: var(--glass-shadow);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stitch-gw-head {
  display: flex;
  align-items: center;
  gap: 10px;
}

.stitch-gw-tag {
  font-size: 0.68rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}

.stitch-gw-title {
  font-family: 'Plus Jakarta Sans', 'Pretendard', sans-serif;
  font-size: 0.98rem;
  font-weight: 800;
  color: var(--txt);
}

.stitch-gw-desc {
  font-size: 0.8rem;
  color: var(--sub);
  margin: 0;
  line-height: 1.55;
}

.stitch-gw-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 4px;
}

.stitch-btn-azure {
  flex: 1;
  height: 44px;
  border-radius: 10px;
  background: var(--accent);
  color: #ffffff;
  font-size: 0.88rem;
  font-weight: 700;
  border: none;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: opacity 0.15s;
}

.stitch-btn-azure:hover {
  opacity: 0.92;
}

.stitch-gw-input {
  flex: 1;
  height: 44px;
  padding: 0 14px;
  border-radius: 10px;
  background: var(--card2);
  border: 1px solid transparent;
  font-family: 'Space Grotesk', 'Pretendard', sans-serif;
  font-size: 0.86rem;
  color: var(--txt);
  outline: none;
}

.stitch-gw-input:focus {
  background: var(--card3);
  border-color: var(--accent);
}

.stitch-btn-enter {
  height: 44px;
  padding: 0 20px;
  border-radius: 10px;
  background: #000000;
  color: #ffffff;
  font-size: 0.88rem;
  font-weight: 700;
  border: none;
  cursor: pointer;
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}

.stitch-gw-links {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 4px;
  font-size: 0.78rem;
}

.stitch-gw-links a {
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-weight: 600;
}

/* ── 7. Precision Step Filter & Quiz Explorer Header ── */
.stitch-explorer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 22px 0 10px;
}

.stitch-explorer-title-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stitch-explorer-title {
  font-family: 'Plus Jakarta Sans', 'Pretendard', sans-serif;
  font-size: 1.08rem;
  font-weight: 800;
  color: var(--txt);
  margin: 0;
}

.stitch-count-badge {
  padding: 2px 8px;
  border-radius: 9999px;
  background: rgba(0, 99, 152, 0.10);
  color: var(--accent);
  font-size: 0.7rem;
  font-weight: 700;
}

.stitch-explorer-sub {
  font-size: 0.7rem;
  color: var(--sub);
  display: block;
}

.stitch-filter-card {
  background: #ffffff;
  border-radius: var(--radius);
  padding: 16px 18px;
  box-shadow: var(--glass-shadow);
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.stitch-filter-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.stitch-filter-label {
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--sub);
}

.stitch-pill-row {
  display: flex;
  align-items: center;
  gap: 6px;
  overflow-x: auto;
  padding: 2px 0;
  scrollbar-width: none;
}
.stitch-pill-row::-webkit-scrollbar { display: none; }

.stitch-mode-pill {
  flex-shrink: 0;
  padding: 6px 14px;
  border-radius: 9999px;
  font-size: 0.76rem;
  font-weight: 600;
  background: var(--card3);
  color: var(--sub);
  border: none;
  cursor: pointer;
  transition: all 0.15s;
}

.stitch-mode-pill.active {
  background: #000000;
  color: #ffffff;
  font-weight: 700;
}

.stitch-step-pill {
  flex-shrink: 0;
  padding: 6px 13px;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  background: var(--card3);
  color: var(--sub);
  border: none;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.15s;
}

.stitch-step-pill.active, .stitch-step-pill:hover {
  background: var(--accent);
  color: #ffffff;
  font-weight: 700;
}

/* ── 8. Section Headings, Symbol Translator (.sym), Prerequisite (.know) & Question Cards (.q) ── */
h2 {
  font-family: 'Plus Jakarta Sans', 'Pretendard', sans-serif;
  font-size: 1.05rem;
  font-weight: 800;
  letter-spacing: -0.015em;
  margin: 24px 0 10px;
  color: var(--txt);
  border-left: 4px solid var(--accent);
  padding-left: 10px;
  line-height: 1.38;
}

code {
  background: var(--card3);
  padding: 2px 6px;
  border-radius: 6px;
  color: var(--accent);
  font-family: 'Space Grotesk', monospace;
  font-size: 0.9em;
}

.sym {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin: 10px 0 16px;
}

.sym > div {
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 14px 16px;
  font-size: .88rem;
  box-shadow: var(--glass-shadow);
  color: var(--txt);
}

.sym b {
  color: var(--accent);
  font-size: .96rem;
  display: block;
  margin-bottom: 4px;
}

.sym-card {
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 18px 20px;
  margin: 10px 0 16px;
  box-shadow: var(--glass-shadow);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.sym-card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.sym-badge {
  background: rgba(0, 99, 152, 0.10);
  color: var(--accent);
  font-size: .74rem;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: 6px;
}

.sym-title {
  margin: 0;
  font-size: 1rem;
  color: var(--txt);
  font-weight: 800;
}

.sym-visual-box {
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 14px;
  text-align: center;
}

.sym-visual-box svg, .sym-visual-box img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 0 auto;
}

.sym-caption {
  font-size: .78rem;
  color: var(--sub);
  margin-top: 8px;
  line-height: 1.45;
}

.sym-desc {
  background: var(--card2);
  border-radius: 12px;
  padding: 14px 16px;
  font-size: .88rem;
  line-height: 1.65;
  color: var(--txt);
}

.know {
  background: #ffffff;
  border: 1px solid var(--line);
  border-left: 4px solid var(--accent);
  border-radius: 14px;
  padding: 16px 18px;
  margin: 10px 0;
  font-size: .9rem;
  box-shadow: var(--glass-shadow);
  color: var(--txt);
}

.know h3 {
  margin: 0 0 8px;
  color: var(--accent);
  font-size: .95rem;
  font-weight: 800;
}

.know ul {
  margin: 6px 0 0 18px;
  padding: 0;
}

.know li {
  margin: 4px 0;
}

.step0-visual-box {
  background: #ffffff !important;
  border: 1px solid var(--line) !important;
  border-radius: 14px !important;
  padding: 16px !important;
  margin: 12px 0 !important;
  box-shadow: var(--glass-shadow) !important;
}

/* ── Question Card (.q) Matching Exact Quiz Cards in screens/bc0f63eb3a354cee8f964ce2bc461f3b ── */
.q {
  background: #ffffff;
  border: 1px solid rgba(228, 226, 228, 0.85);
  border-radius: var(--radius);
  padding: 20px;
  margin: 12px 0 18px;
  transition: all .2s ease;
  box-shadow: var(--glass-shadow);
}

.q.correct-q {
  border-color: #10B981;
  box-shadow: 0 4px 18px rgba(16, 185, 129, 0.10);
}

.q .lvl {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  background: transparent;
  padding: 0 0 10px;
  margin-bottom: 10px;
  border-bottom: 1px solid var(--card3);
  border-radius: 0;
  font-size: .75rem;
  color: var(--accent);
  font-weight: 700;
}

.q .lvl > span:first-child {
  background: rgba(0, 99, 152, 0.10);
  color: var(--accent);
  padding: 4px 10px;
  border-radius: 6px;
  font-weight: 700;
}

.q .lvl::after {
  content: "🪜 단계별 빌드업";
  color: #D97706;
  background: #FEF3C7;
  padding: 3px 9px;
  border-radius: 6px;
  font-size: 0.72rem;
  font-weight: 700;
  flex-shrink: 0;
}

.q .stem {
  font-size: 1.02rem;
  margin-bottom: 14px;
  font-weight: 600;
  color: var(--txt);
  line-height: 1.65;
}

.opts {
  display: grid;
  gap: 8px;
}

.opts.opts-inline {
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
}

.opts.opts-inline .opt {
  justify-content: center;
  padding: 10px 8px;
}

.opt {
  background: var(--card2);
  border: 1.5px solid var(--line);
  border-radius: 12px;
  padding: 11px 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all .15s ease;
  font-size: .94rem;
  color: var(--txt);
}

.opt:hover {
  background: var(--card3);
  border-color: var(--accent);
  transform: translateY(-1px);
}

.opt .n {
  width: 24px;
  height: 24px;
  flex: 0 0 24px;
  border-radius: 50%;
  background: #ffffff;
  border: 1px solid var(--line-strong);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: .78rem;
  font-weight: 700;
  color: var(--txt);
  font-family: 'Space Grotesk', sans-serif;
}

.opt.correct {
  background: rgba(16, 185, 129, 0.12) !important;
  border-color: #10B981 !important;
  color: #065f46 !important;
  font-weight: 600;
}

.opt.correct .n {
  background: #10B981 !important;
  border-color: #10B981 !important;
  color: #ffffff !important;
}

.opt.wrong {
  background: rgba(239, 68, 68, 0.10) !important;
  border-color: #ef4444 !important;
  color: #991b1b !important;
}

.opt.wrong .n {
  background: #ef4444 !important;
  border-color: #ef4444 !important;
  color: #ffffff !important;
}

.opt.locked {
  cursor: default;
}

.q-actions {
  margin-top: 14px !important;
  padding-top: 12px !important;
  border-top: 1px solid var(--card3) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
}

.q-actions::before {
  content: "✓ 즉시 채점 · 상세 해설";
  font-size: 0.75rem;
  font-weight: 600;
  color: #059669;
}

.exp-toggle-btn {
  background: #000000 !important;
  border: none !important;
  color: #ffffff !important;
  border-radius: 8px !important;
  padding: 8px 16px !important;
  font-size: .8rem !important;
  font-weight: 700 !important;
  cursor: pointer;
  transition: background .15s;
}

.exp-toggle-btn:hover {
  background: #262626 !important;
}

.exp {
  margin-top: 12px;
  padding: 14px 16px;
  border-radius: 12px;
  background: var(--card2);
  border: 1px solid var(--line);
  border-left: 4px solid var(--accent);
  font-size: .9rem;
  display: none;
  color: var(--txt);
  line-height: 1.7;
}

.exp.show {
  display: block;
}

.exp b {
  color: var(--navy);
}

/* ── 9. Solution Card (.sol), Visual Diagrams & Schematic Flowcharts ── */
.sol {
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 20px;
  margin: 14px 0;
  box-shadow: var(--glass-shadow);
  color: var(--txt);
}

.sol h4 {
  color: var(--navy);
  margin: 18px 0 8px;
  font-size: 1rem;
  font-weight: 800;
}

.sol-highlight {
  background: #f0f7ff;
  border-left: 4px solid var(--accent);
  border-radius: 0 8px 8px 0;
  padding: 10px 14px;
  margin: 12px 0;
  color: var(--txt);
}

.diagram {
  background: #ffffff;
  color: #1b2436;
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 14px;
  margin: 14px 0;
  text-align: center;
}

.diagram svg, .diagram img {
  max-width: 100%;
  height: auto;
}

.diagram-caption {
  font-size: .8rem;
  color: var(--sub);
  margin-top: 8px;
}

figure.math-visual-diagram {
  background: #f8fafc !important;
  border: 1px solid #cbd5e1 !important;
  border-radius: 14px !important;
  padding: 14px !important;
  margin: 12px 0 18px !important;
  text-align: center !important;
}

figure.math-visual-diagram figcaption {
  color: #475569 !important;
  font-size: 0.84rem !important;
  margin-top: 10px !important;
  line-height: 1.55 !important;
}

section.math-schematic-flow {
  background: #f8fafc !important;
  border: 1px solid #cbd5e1 !important;
  border-radius: 14px !important;
  padding: 14px !important;
  margin: 12px 0 18px !important;
}

section.math-schematic-flow table {
  background: transparent !important;
}

section.math-schematic-flow td,
section.math-schematic-flow th {
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
  color: #1e293b !important;
}

section.math-schematic-flow thead tr,
section.math-schematic-flow thead th {
  background: #f1f5f9 !important;
  color: #0f172a !important;
}

section.math-schematic-flow td span,
section.math-schematic-flow td b {
  color: #1e293b !important;
}

section.math-schematic-flow td > b:first-child {
  color: #006398 !important;
}

.btn {
  background: #000000;
  color: #ffffff;
  border: none;
  border-radius: 10px;
  padding: 10px 20px;
  font-weight: 700;
  cursor: pointer;
  transition: .15s;
}

.btn:hover {
  background: #262626;
}

.final {
  text-align: center;
  margin: 24px 0;
  padding: 24px;
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  box-shadow: var(--glass-shadow);
  font-size: 1.02rem;
}

.final .ans {
  font-size: 1.55rem;
  color: var(--good-dark);
  font-weight: 800;
  margin: 8px 0 14px;
  font-family: 'Plus Jakarta Sans', 'Pretendard', sans-serif;
}

/* ── Cards (Playing Cards Visual) ── */
.cards { display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; margin: 14px 0; }
.card { width: 64px; height: 92px; border-radius: 10px; display: flex; flex-direction: column; align-items: center; justify-content: center; font-weight: 700; border: 2px solid var(--line-strong); }
.card .num { font-size: 1.3rem; }
.card .face { font-size: .7rem; margin-top: 4px; opacity: .85; }
.card.front { background: #ffffff; color: #1b2436; border-color: #94a3b8; }
.card.back { background: #334155; color: #ffffff; border-color: #1e293b; }

/* ── 10. min7014 Deep Exploration Addon Card ── */
.min7014-addon-card {
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 20px;
  margin: 20px 0;
  box-shadow: var(--glass-shadow);
}

.min-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  flex-wrap: wrap;
  gap: 8px;
}

.min-header-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.02rem;
  font-weight: 800;
  color: var(--txt);
  font-family: 'Plus Jakarta Sans', 'Pretendard', sans-serif;
}

.min-logo {
  width: 24px;
  height: 24px;
  border-radius: 6px;
}

.min-tag {
  background: rgba(0, 99, 152, 0.10);
  color: var(--accent);
  padding: 3px 10px;
  border-radius: 9999px;
  font-size: .72rem;
  font-weight: 700;
}

.min-lead {
  font-size: .84rem;
  color: var(--sub);
  margin-bottom: 14px;
  line-height: 1.55;
}

.min-guide-banner {
  background: var(--card2) !important;
  border: 1px solid var(--line) !important;
  border-radius: 10px !important;
  padding: 12px 14px !important;
  margin-bottom: 14px !important;
  font-size: .82rem !important;
  line-height: 1.6 !important;
  color: var(--txt) !important;
}

.min-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
  width: 100%;
}

.min-item {
  background: var(--card2);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.min-item-title {
  display: block;
  color: var(--txt);
  font-size: .92rem;
  font-weight: 700;
  text-decoration: none;
  line-height: 1.5;
}

.min-item-sub {
  display: block;
  font-size: .78rem;
  font-weight: 400;
  color: var(--sub);
  margin-top: 2px;
}

.min-item-actions {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  align-items: center;
}

.min-btn {
  font-size: .76rem;
  font-weight: 700;
  padding: 6px 12px;
  border-radius: 8px;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
}

.min-btn-ggb { background: rgba(0, 99, 152, 0.10); border: 1px solid rgba(0, 99, 152, 0.25); color: var(--accent); }
.min-btn-pdf { background: var(--card3); border: 1px solid var(--line); color: var(--txt); }
.min-btn-yt { background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.22); color: #dc2626; }
.min-btn-algeo { background: rgba(16, 185, 129, 0.10); border: 1px solid rgba(16, 185, 129, 0.25); color: #059669; }
.min-btn-detail { background: #000000; border: 1px solid #000000; color: #ffffff; }

.min-cat-badge {
  display: inline-block;
  font-size: .7rem;
  padding: 2px 8px;
  border-radius: 6px;
  background: rgba(0, 99, 152, 0.08);
  color: var(--accent);
  margin-bottom: 4px;
  font-weight: 700;
}

.min-ggb-frame-wrap {
  margin-top: 10px;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid var(--line);
  background: #ffffff;
  display: none;
}
.min-ggb-frame-wrap.active { display: block; }

.min-footer {
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px dashed var(--line);
  text-align: right;
}
.min-footer-link { color: var(--accent); font-size: .82rem; font-weight: 700; text-decoration: none; }

/* ── 11. Stitch Dark Navy Lesson Pack Banner & Curated Collections ── */
.stitch-pack-banner {
  background: #131b2e;
  color: #ffffff;
  border-radius: var(--radius);
  padding: 16px 18px;
  margin: 18px 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  box-shadow: 0 4px 16px rgba(19, 27, 46, 0.14);
}

.stitch-pack-left {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.stitch-pack-icon {
  width: 40px;
  height: 40px;
  border-radius: 9999px;
  background: rgba(0, 99, 152, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stitch-pack-btn {
  height: 36px;
  padding: 0 14px;
  border-radius: 8px;
  background: #93ccff;
  color: #003352;
  font-size: 0.76rem;
  font-weight: 800;
  border: none;
  cursor: pointer;
  flex-shrink: 0;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
}

.stitch-collections-section {
  margin: 24px 0 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.stitch-collection-card {
  padding: 16px;
  border-radius: var(--radius);
  background: #ffffff;
  box-shadow: var(--glass-shadow);
  display: flex;
  align-items: center;
  justify-content: space-between;
  text-decoration: none;
  color: var(--txt);
  transition: background 0.15s;
}

.stitch-collection-card:hover {
  background: var(--card2);
}

.stitch-col-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.stitch-col-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stitch-col-title {
  font-family: 'Plus Jakarta Sans', 'Pretendard', sans-serif;
  font-size: 0.92rem;
  font-weight: 800;
  color: var(--txt);
  display: block;
}

.stitch-col-sub {
  font-size: 0.76rem;
  color: var(--sub);
  display: block;
  margin-top: 2px;
}

.stitch-footer {
  margin-top: 28px;
  padding: 16px 0 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 6px;
}

.stitch-footer-links {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.74rem;
  font-weight: 600;
  color: var(--sub);
}

.stitch-footer-links a {
  color: var(--sub);
  text-decoration: none;
}

.stitch-footer-copy {
  font-size: 0.68rem;
  color: var(--sub);
  max-width: 340px;
  margin: 0;
}

/* ── 12. Fixed Bottom Navigation Bar (Exact screens/bc0f63eb3a354cee8f964ce2bc461f3b) ── */
.stitch-bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(252, 248, 250, 0.92);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.05);
  border-top: 1px solid rgba(228, 226, 228, 0.6);
}

.stitch-bottom-nav-inner {
  max-width: 768px;
  height: 64px;
  margin: 0 auto;
  padding: 0 8px;
  display: flex;
  align-items: center;
  justify-content: space-around;
}

.stitch-bnav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 56px;
  min-height: 44px;
  gap: 2px;
  text-decoration: none;
  color: var(--sub);
  font-size: 0.7rem;
  font-weight: 500;
  background: transparent;
  border: none;
  cursor: pointer;
}

.stitch-bnav-item.active {
  color: var(--accent);
  font-weight: 700;
}

/* ── Report Form & Bilingual Engine ── */
.report-wrap { margin-top: 8px !important; border-top: none !important; padding-top: 4px !important; }
.report-btn { background: transparent !important; color: #64748b !important; border: 1px solid var(--line) !important; }
.report-text { background: #ffffff !important; color: var(--txt) !important; border: 1px solid var(--line-strong) !important; }
.report-cancel { background: #ffffff !important; color: var(--sub) !important; border: 1px solid var(--line-strong) !important; }

#trackFull {
  display: none;
  background: rgba(252, 248, 250, 0.96) !important;
  backdrop-filter: blur(18px) !important;
  color: var(--txt) !important;
}

.bilingual-en { display: none; }
.bilingual-ko { display: inline; }
div.bilingual-ko, p.bilingual-ko { display: block; }
html[lang="en"] .bilingual-ko { display: none !important; }
html[lang="en"] .bilingual-en {
  display: block;
  margin-top: 6px;
  color: #006398;
  font-size: 0.92em;
  line-height: 1.6;
}
html[lang="en"] span.bilingual-en {
  display: inline !important;
  margin-top: 0 !important;
}

/* ── Responsive MathJax & Mobile Layout ── */
h1, h2, h3, h4, h5, h6, p, div, span, li, a, label {
  overflow-wrap: break-word;
  word-break: keep-all;
}
mjx-container { max-width: 100% !important; box-sizing: border-box !important; }
mjx-container[display="true"] {
  display: block !important;
  max-width: 100% !important;
  overflow-x: auto !important;
  overflow-y: hidden !important;
  margin: 0.75em 0 !important;
  padding: 10px 12px !important;
  background: var(--card2) !important;
  border-radius: 10px;
  border: 1px solid var(--line) !important;
  color: var(--txt) !important;
  text-align: center !important;
}
mjx-container:not([display="true"]) {
  display: inline-flex !important;
  vertical-align: middle !important;
  max-width: 100% !important;
  overflow: visible !important;
}

@media (max-width: 768px) {
  .orig-grid { grid-template-columns: 1fr !important; gap: 12px !important; }
  .sym { grid-template-columns: 1fr !important; }
}
@media (max-width: 640px) {
  .wrap { padding: 82px 14px 96px !important; }
  .opts.opts-inline { grid-template-columns: repeat(2, 1fr) !important; }
  mjx-container { font-size: 92% !important; }
}
</style>"""


CUSTOM_TITLE_MAP = {
    '1b623c24': (
        '확률과 통계 · 독립시행과 패리티',
        '카드 뒤집기 4회 반복 후 모두 앞면일 확률',
        'Probability & Parity · All 6 Cards Face-Up After 4 Dice Rolls'
    ),
    '36790012': (
        '확률과 통계 · 모평균의 신뢰구간',
        '정규분포 신뢰구간으로 표본크기 n 구하기',
        'Statistical Estimation · Finding Sample Size n from Confidence Interval'
    ),
    '4cb6d212': (
        '확률과 통계 · 조합(nCr)의 활용',
        '3 ≤ x < y < z < w ≤ 13 자연수 순서쌍의 개수',
        'Combinatorics · Counting Strictly Increasing Integer Quadruples'
    ),
    '51908207': (
        '확률과 통계 · 조건부확률과 상태전이',
        '카드 교환 주사위 게임 · 4회 후 초기 상태일 때의 조건부확률',
        'Conditional Probability & State Transition · 4-Round Card Swap Game'
    ),
    '8e9d528d': (
        '수학I · 로그의 성질과 밑의 변환',
        'log 2 = a, log 3 = b일 때 log 12를 a, b로 나타내기',
        'Logarithm Properties · Expressing log 12 in Terms of a = log 2 and b = log 3'
    ),
    '8f24f3c3': (
        '확률과 통계 · 수학적 확률과 표본공간',
        '주사위를 두 번 굴려 눈의 합이 7이 나올 확률',
        'Mathematical Probability · Sum of Two Dice Equals 7'
    ),
    'a05b47bc': (
        '확률과 통계 · 순서가 정해진 순열',
        '7개 깃발 배열에서 빨강이 노랑·파랑보다 왼쪽에 올 경우의 수',
        'Permutations with Order Constraints · Arranging 7 Colored Flags'
    ),
    'a33ab59b': (
        '기하 · 이차곡선(쌍곡선의 정의)',
        "쌍곡선 PF' - PF = 2 조건의 점 P 좌표와 삼각형 넓이",
        "Conic Sections (Hyperbola) · Coordinates of P and Area of △PF'F"
    ),
    'ac8dc374': (
        '2027학년도 9월 모의평가 수학 21번',
        '삼차함수와 절댓값 함수의 미분가능성',
        '2027 AY Sep Mock CSAT Math #21 · Cubic Function & Absolute Value Differentiability'
    ),
    'd7abad20': (
        '2009학년도 6월 학력평가 수학 29번',
        '삼각함수 덧셈정리를 활용한 나무 높이 측정',
        '2009 AY June Exam Math #29 · Measuring Tree Height via Tangent Addition Formula'
    ),
    'e7d51a27': (
        '수학II · 절댓값 함수의 미분가능성',
        '절댓값 합성함수의 미분가능 조건과 자연수 n의 합',
        'Calculus · Differentiability of Absolute Value Composite Functions'
    ),
}


def split_title_two_tone(h1_ko_raw, slug=""):
    if slug in CUSTOM_TITLE_MAP:
        return CUSTOM_TITLE_MAP[slug][0], CUSTOM_TITLE_MAP[slug][1]
    # Clean leading emoji and internal tags
    clean = re.sub(r'^[📘📙📕📝📐]\s*', '', h1_ko_raw).strip()
    clean = re.sub(r'\s*\(자동 폴백 아님[^)]*\)', '', clean).strip()
    m = re.match(r'^\[([^\]]+)\]\s*(.+)$', clean)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    # If there's a middle dot outside parentheses
    if '·' in clean and not clean.endswith(')'):
        parts = clean.split('·', 1)
        return parts[0].strip(), parts[1].strip()
    return "수능·학력평가 기출 디딤돌", clean


def latex_ans_to_svg_text(html):
    m = re.search(r'<div class="ans" id="finalAns">(.*?)</div>', html, flags=re.S)
    if not m:
        return None
    raw = m.group(1)
    raw = re.sub(r'<span class="bilingual-en">.*?</span>', '', raw, flags=re.S)
    raw = re.sub(r'<[^>]+>', ' ', raw)
    raw = re.sub(r'(?:정답|Correct Answer|Answer|\:)', ' ', raw, flags=re.I).strip()
    raw = raw.strip('$').strip()
    # Convert \sqrt[3]{...} and \sqrt{...} FIRST before \frac/\dfrac so nested braces work!
    for _ in range(3):
        raw = re.sub(r'\\sqrt\[3\]\{([^{}]+)\}', r'³√\1', raw)
        raw = re.sub(r'\\sqrt\{([^{}]+)\}', r'√\1', raw)
        raw = re.sub(
            r'\\d?frac\{([^{}]+)\}\{([^{}]+)\}',
            lambda fm: (f"({fm.group(1)})" if ('+' in fm.group(1) or '-' in fm.group(1)[1:]) else fm.group(1)) + '/' + fm.group(2),
            raw
        )
    raw = raw.replace(r'\pi', 'π').replace(r'\ln', 'ln ').replace(r'\le', '≤').replace(r'\ge', '≥')
    raw = raw.replace('^2', '²').replace('^3', '³')
    raw = raw.replace('$', '').replace('{', '').replace('}', '').replace('\\', '').strip()
    raw = re.sub(r'\s+', ' ', raw)
    return raw


def convert_svg_to_stitch_light(svg_str, clean_ans=None):
    if clean_ans:
        svg_str = re.sub(r'Answer:\s*[^<]+(?=</text>)', f'Answer: {clean_ans}', svg_str)
        svg_str = re.sub(r'🎯 최종 결론:\s*[^<]+(?=</text>)', f'🎯 최종 결론: {clean_ans}', svg_str)

    # 1. Regex replacements for dark rgba fills on rects/paths
    svg_str = re.sub(r'fill="rgba\(15,\s*23,\s*42,\s*[0-9.]+\)"', 'fill="#ffffff"', svg_str)
    svg_str = re.sub(r'fill="rgba\(30,\s*41,\s*59,\s*[0-9.]+\)"', 'fill="#f8fafc"', svg_str)
    svg_str = re.sub(r'(<rect\b[^>]*?)\bfill="#(?:131b2e|0f172a|0b1120)"', r'\1fill="#f8fafc"', svg_str)
    svg_str = re.sub(r'(<rect\b[^>]*?)\bfill="#065f46"', r'\1fill="#ecfdf5"', svg_str)

    svg_replacements = [
        ('background:linear-gradient(145deg,#0b1120 0%,#131c33 100%)', 'background:linear-gradient(145deg,#ffffff 0%,#f6f3f5 100%)'),
        ('border:1.5px solid rgba(124,196,255,0.35);box-shadow:0 6px 24px rgba(0,0,0,0.45)', 'border:1.5px solid #cbd5e1;box-shadow:0 4px 16px rgba(19,27,46,0.06)'),
        ('stroke="rgba(148,163,184,0.08)"', 'stroke="rgba(0,99,184,0.06)"'),
        ('fill="rgba(56,189,248,0.12)" stroke="rgba(56,189,248,0.35)"', 'fill="#e0f2fe" stroke="#7dd3fc"'),
        ('fill="rgba(56,189,248,0.12)"', 'fill="#eff6ff"'),
        ('fill="rgba(56,189,248,0.14)"', 'fill="#eff6ff"'),
        ('fill="rgba(56,189,248,0.15)"', 'fill="#eff6ff"'),
        ('fill="rgba(56,189,248,0.16)"', 'fill="#e0f2fe"'),
        ('fill="rgba(56,189,248,0.18)"', 'fill="#e0f2fe"'),
        ('fill="rgba(167,139,250,0.12)"', 'fill="#f5f3ff"'),
        ('fill="rgba(167,139,250,0.15)"', 'fill="#f5f3ff"'),
        ('fill="rgba(52,211,153,0.12)"', 'fill="#ecfdf5"'),
        ('fill="rgba(52,211,153,0.15)"', 'fill="#ecfdf5"'),
        ('fill="rgba(52,211,153,0.16)"', 'fill="#ecfdf5"'),
        ('fill="rgba(52,211,153,0.22)"', 'fill="#ecfdf5"'),
        ('fill="rgba(52,211,153,0.32)"', 'fill="#dcfce7"'),
        ('fill="rgba(52,211,153,0.45)"', 'fill="#bbf7d0"'),
        ('fill="rgba(251,191,36,0.14)"', 'fill="#fef3c7"'),
        ('fill="rgba(251,191,36,0.18)"', 'fill="#fef3c7"'),
        ('fill="rgba(251,191,36,0.2)"', 'fill="#fef3c7"'),
        ('fill="rgba(251,191,36,0.22)"', 'fill="#fef3c7"'),
        ('fill="rgba(251,113,133,0.12)"', 'fill="#fff1f2"'),
        ('fill="rgba(251,113,133,0.14)"', 'fill="#fff1f2"'),
        ('fill="rgba(251,113,133,0.18)"', 'fill="#ffe4e6"'),
        ('fill="rgba(251,113,133,0.28)"', 'fill="#ffe4e6"'),
        ('fill="#38bdf8"', 'fill="#006398"'),
        ('fill="#7cc4ff"', 'fill="#006398"'),
        ('fill="#bae6fd"', 'fill="#006398"'),
        ('fill="#fde68a"', 'fill="#b45309"'),
        ('fill="#6ee7b7"', 'fill="#047857"'),
        ('fill="#a7f3d0"', 'fill="#047857"'),
        ('fill="#c4b5fd"', 'fill="#4f46e5"'),
        ('fill="#ddd6fe"', 'fill="#4f46e5"'),
        ('fill="#fecdd3"', 'fill="#be123c"'),
        ('fill="#fb7185"', 'fill="#be123c"'),
        ('fill="#e2e8f0"', 'fill="#334155"'),
        ('fill="#cbd5e1"', 'fill="#475569"'),
        ('stroke="#0b1120"', 'stroke="#ffffff"'),
        ('fill="#0b1120"', 'fill="#ffffff"'),
    ]
    for old_s, new_s in svg_replacements:
        svg_str = svg_str.replace(old_s, new_s)

    # Only on <text> tags (when not on the same line as a <circle>), replace light text fills with high-contrast dark fills
    lines = svg_str.split('\n')
    out_lines = []
    for ln in lines:
        if '<text' in ln and '<circle' not in ln:
            ln = ln.replace('fill="#fff"', 'fill="#1b1b1d"')
            ln = ln.replace('fill="#ffffff"', 'fill="#1b1b1d"')
            ln = ln.replace('fill="#f8fafc"', 'fill="#131b2e"')
            ln = ln.replace('fill="#ecfdf5"', 'fill="#065f46"')
        out_lines.append(ln)
    return '\n'.join(out_lines)


def build_stitch_top_shell(slug, asset_prefix, h1_full_inner, h1_ko_line1, h1_ko_line2, h1_en_text, lead_inner, q_count):
    return f"""<!-- STITCH_HEADER_START -->
<header class="stitch-app-header">
  <div class="stitch-app-header-inner">
    <a href="/mathedu/" class="stitch-brand-link">
      <img src="{asset_prefix}assets/favicon.png" alt="mathedu" class="stitch-brand-logo">
      <div class="stitch-brand-text">
        <span class="stitch-brand-title">mathedu · 수학자료실</span>
        <div class="stitch-brand-sub">
          <span class="stitch-brand-pill"><span class="bilingual-ko">3,400+ 시각적 수학 증명</span><span class="bilingual-en">3,400+ Visual Proofs</span></span>
          <span class="stitch-brand-code">{slug.upper()}</span>
        </div>
      </div>
    </a>
    <div class="stitch-header-actions">
      <button type="button" id="langToggleSingleBtn" class="stitch-lang-toggle" onclick="var nextL=(document.documentElement.lang==='en')?'ko':'en';setBoardLang(nextL,true);this.textContent=nextL.toUpperCase();">KO</button>
      <div class="lang-group" style="display:none">
        <button type="button" class="lang-btn active" data-lang-btn="ko" onclick="setBoardLang('ko', true)">한국어</button>
        <button type="button" class="lang-btn" data-lang-btn="en" onclick="setBoardLang('en', true)">English</button>
      </div>
      <div class="stitch-streak-pill" onclick="if(window.MatheduGame)MatheduGame.showBadgesModal()" title="연속 학습 스트릭 및 뱃지">
        <span class="material-symbols-outlined" style="font-size:16px;color:#F59E0B;font-variation-settings:'FILL' 1">local_fire_department</span>
        <span id="stitchHeaderStreak">14</span>
      </div>
      <button type="button" class="stitch-profile-btn" onclick="if(window.MatheduAuth){{MatheduAuth.isLoggedIn()?MatheduAuth.showMyProblemsModal():MatheduAuth.showAuthModal()}}" title="내 서재 및 학습 기록">
        <span class="material-symbols-outlined" style="font-size:18px;color:#ffffff">person</span>
      </button>
    </div>
  </div>
</header>

<!-- 1. Brand / Problem Identity Hero Card (screens/bc0f63eb3a354cee8f964ce2bc461f3b) -->
<div class="stitch-hero-card">
  <div class="stitch-hero-top">
    <div class="stitch-hero-brand">
      <span class="material-symbols-outlined" style="font-size:20px;color:#006398">architecture</span>
      <span>수학자료실 · mathedu</span>
    </div>
    <span class="stitch-free-pill"><span class="bilingual-ko">100% 영구 무료</span><span class="bilingual-en">100% Forever Free</span></span>
  </div>
  <h1>
    <span class="bilingual-ko">
      <span class="stitch-h1-main">{h1_ko_line1}</span>
      <span class="stitch-h1-accent">{h1_ko_line2}</span>
    </span>
    <span class="bilingual-en">{h1_en_text}</span>
  </h1>
  <p class="lead">{lead_inner}</p>
  <div class="stitch-chip-scroll">
    <button type="button" class="stitch-feature-chip" onclick="scrollToQuizStep(0)">
      <span class="material-symbols-outlined" style="font-size:14px;color:#F59E0B">bolt</span>
      <span class="bilingual-ko">무가입 5초 즉시 학습</span><span class="bilingual-en">Instant Free Practice</span>
    </button>
    <button type="button" class="stitch-feature-chip" onclick="if(window.toggleStitchStepMode)window.toggleStitchStepMode()">
      <span class="material-symbols-outlined" style="font-size:14px;color:#006398">target</span>
      <span class="bilingual-ko">0~{max(1, q_count-1)}단계 빌드업</span><span class="bilingual-en">Step-by-Step Build-up</span>
    </button>
    <button type="button" class="stitch-feature-chip" onclick="if(window.openClassCreatorModal)openClassCreatorModal('{slug}')">
      <span class="material-symbols-outlined" style="font-size:14px;color:#4F46E5">qr_code_2</span>
      <span class="bilingual-ko">3초 수업 QR</span><span class="bilingual-en">3-Sec Class QR</span>
    </button>
    <button type="button" class="stitch-feature-chip" onclick="if(window.downloadOfflineQuiz)window.downloadOfflineQuiz('{slug}')">
      <span class="material-symbols-outlined" style="font-size:14px;color:#45464d">inventory_2</span>
      <span class="bilingual-ko">100% 오프라인 보관함</span><span class="bilingual-en">100% Offline Save</span>
    </button>
    <button type="button" class="stitch-feature-chip" id="copyBtn" onclick="copyLink()">
      <span class="material-symbols-outlined" style="font-size:14px;color:#10B981">monitoring</span>
      <span class="bilingual-ko">링크 복사 · 공유</span><span class="bilingual-en">Copy Link</span>
    </button>
  </div>
  <div class="stitch-bento-stats">
    <div class="stitch-bento-item">
      <span class="stitch-bento-val" style="color:#1b1b1d">3,400+</span>
      <span class="stitch-bento-lbl"><span class="bilingual-ko">수학 주제</span><span class="bilingual-en">Topics</span></span>
    </div>
    <div class="stitch-bento-item">
      <span class="stitch-bento-val" style="color:#006398"><b id="pts">0</b> / <b id="tot">{q_count}</b></span>
      <span class="stitch-bento-lbl"><span class="bilingual-ko">디딤돌 정답</span><span class="bilingual-en">Score</span></span>
    </div>
    <div class="stitch-bento-item">
      <span class="stitch-bento-val" style="color:#F59E0B" id="pct">0%</span>
      <span class="stitch-bento-lbl"><span class="bilingual-ko">수능·디딤돌</span><span class="bilingual-en">Progress</span></span>
    </div>
    <div class="stitch-bento-item">
      <span class="stitch-bento-val" style="color:#10B981">100%</span>
      <span class="stitch-bento-lbl"><span class="bilingual-ko">오프라인</span><span class="bilingual-en">Offline</span></span>
    </div>
    <div class="stitch-progress-wrap">
      <span class="bar"><i id="bar"></i></span>
    </div>
  </div>
</div>
<!-- STITCH_HEADER_END -->"""


def build_stitch_explorer_shell(q_count):
    step_pills = []
    for i in range(1, q_count):
        step_pills.append(f'<button type="button" class="stitch-step-pill" onclick="scrollToQuizStep({i-1})">{i}단계</button>')
    if q_count >= 1:
        step_pills.append(f'<button type="button" class="stitch-step-pill" onclick="scrollToQuizStep({q_count-1})">최종 본문항</button>')
    step_pills_html = "\n        ".join(step_pills)

    return f"""<!-- STITCH_EXPLORER_START -->
<div class="stitch-explorer-header" id="stitchQuizStepsSection">
  <div class="stitch-explorer-title-wrap">
    <span class="material-symbols-outlined" style="font-size:22px;color:#006398">tune</span>
    <div>
      <div style="display:flex;align-items:center;gap:8px">
        <h3 class="stitch-explorer-title"><span class="bilingual-ko">수능·모의평가 기출 디딤돌 탐색기</span><span class="bilingual-en">Step-by-Step Scaffolding Explorer</span></h3>
        <span class="stitch-count-badge">총 {q_count}문항</span>
      </div>
      <span class="stitch-explorer-sub"><span class="bilingual-ko">원본 기출 · 제0단계 기호 번역 · 1~{max(1,q_count-1)}단계 디딤돌 즉시 이동</span><span class="bilingual-en">Jump to Original Problem, Symbol Translator, or any Scaffolding Step</span></span>
    </div>
  </div>
  <button type="button" class="stitch-circle-icon-btn" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" title="맨 위로">
    <span class="material-symbols-outlined" style="font-size:18px">restart_alt</span>
  </button>
</div>

<div class="stitch-filter-card">
  <div class="stitch-filter-group">
    <span class="stitch-filter-label"><span class="bilingual-ko">학습 모드</span><span class="bilingual-en">Learning Mode</span></span>
    <div class="stitch-pill-row">
      <button type="button" class="stitch-mode-pill active" data-stitch-mode-pill="all" onclick="if(window.toggleStitchStepMode)window.toggleStitchStepMode('all')"><span class="bilingual-ko">전체 펼쳐보기</span><span class="bilingual-en">View All Steps</span></button>
      <button type="button" class="stitch-mode-pill" data-stitch-mode-pill="focus" onclick="if(window.toggleStitchStepMode)window.toggleStitchStepMode('focus')"><span class="bilingual-ko">단계별 집중 모드</span><span class="bilingual-en">Step Focus Mode</span></button>
      <button type="button" class="stitch-mode-pill" onclick="scrollToSolSection()"><span class="bilingual-ko">시각적 도형·상세 풀이</span><span class="bilingual-en">Visual Proof & Solution</span></button>
      <button type="button" class="stitch-mode-pill" onclick="window.print()"><span class="bilingual-ko">A4 시험지 인쇄</span><span class="bilingual-en">Print A4 Worksheet</span></button>
    </div>
  </div>
  <div class="stitch-filter-group">
    <span class="stitch-filter-label"><span class="bilingual-ko">디딤돌 단계 선택</span><span class="bilingual-en">Select Scaffolding Step</span></span>
    <div class="stitch-pill-row">
      <button type="button" class="stitch-step-pill active" onclick="scrollToOrigCard()">원본 문제</button>
      {step_pills_html}
    </div>
  </div>
</div>
<!-- STITCH_EXPLORER_END -->"""


def build_stitch_bottom_shell(slug, asset_prefix, h1_ko_line2, q_count):
    return f"""<!-- STITCH_FOOTER_START -->
<!-- Gamification / Daily Streak Banner (screens/bc0f63eb3a354cee8f964ce2bc461f3b) -->
<div class="stitch-streak-card">
  <div class="stitch-streak-left">
    <div class="stitch-flame-circle">
      <span class="material-symbols-outlined" style="font-size:22px;color:#F59E0B;font-variation-settings:'FILL' 1">local_fire_department</span>
    </div>
    <div class="stitch-streak-info">
      <div class="stitch-streak-title-row">
        <span class="stitch-streak-title"><span class="bilingual-ko">연속 출석 1일차</span><span class="bilingual-en">Day 1 Streak</span></span>
        <span class="stitch-lvl-badge">Lv.1 입문자</span>
      </div>
      <span class="stitch-streak-sub"><span class="bilingual-ko">오늘 수학 문제 풀면 불꽃 유지! (0 / 100 XP)</span><span class="bilingual-en">Solve steps today to keep the streak! (0 / 100 XP)</span></span>
    </div>
  </div>
  <div class="stitch-streak-actions">
    <button type="button" class="stitch-circle-icon-btn" onclick="if(window.MatheduGame)MatheduGame.showBadgesModal()" title="나의 뱃지">
      <span class="material-symbols-outlined" style="font-size:18px">military_tech</span>
    </button>
    <button type="button" class="stitch-circle-icon-btn" style="color:#ba1a1a" onclick="if(window.MatheduGame&&MatheduGame.toggleBookmark)MatheduGame.toggleBookmark('{slug}')" title="즐겨찾기 및 오답노트">
      <span class="material-symbols-outlined" style="font-size:18px">bookmark</span>
    </button>
  </div>
</div>

<!-- Two-Pillar User Gateway: Teacher & Student Quick Action (screens/bc0f63eb3a354cee8f964ce2bc461f3b) -->
<div class="stitch-gateway-grid">
  <div class="stitch-gateway-card">
    <div class="stitch-gw-head">
      <span class="material-symbols-outlined" style="font-size:22px;color:#006398">co_present</span>
      <div>
        <div class="stitch-gw-tag" style="color:#006398"><span class="bilingual-ko">교사 회원 전용 · 수업 배포</span><span class="bilingual-en">FOR TEACHERS · CLASSROOM</span></div>
        <div class="stitch-gw-title"><span class="bilingual-ko">3초 만에 수업 개설하기</span><span class="bilingual-en">Launch Classroom in 3 Seconds</span></div>
      </div>
    </div>
    <p class="stitch-gw-desc"><span class="bilingual-ko">회원 로그인 후 즉시 고유 수업 코드를 생성하고, 칠판 빔프로젝터용 대형 QR코드와 학생 배포용 링크를 발급받으세요.</span><span class="bilingual-en">Generate a unique classroom code, projector QR code, and student link in 3 seconds.</span></p>
    <div class="stitch-gw-actions">
      <button type="button" class="stitch-btn-azure" onclick="if(window.openClassCreatorModal)openClassCreatorModal('{slug}')">
        <span class="material-symbols-outlined" style="font-size:18px">qr_code_2</span>
        <span class="bilingual-ko">3초 수업 개설 (QR)</span><span class="bilingual-en">3-Sec Class QR</span>
      </button>
      <a href="{asset_prefix}dashboard.html" class="stitch-cta-gray" style="height:44px;padding:0 14px">
        <span class="material-symbols-outlined" style="font-size:18px">dashboard</span>
        <span class="bilingual-ko">현황판</span><span class="bilingual-en">Dashboard</span>
      </a>
    </div>
  </div>

  <div class="stitch-gateway-card">
    <div class="stitch-gw-head">
      <span class="material-symbols-outlined" style="font-size:22px;color:#4F46E5">school</span>
      <div>
        <div class="stitch-gw-tag" style="color:#4F46E5"><span class="bilingual-ko">비회원·학생 · 100% 자유 풀이</span><span class="bilingual-en">STUDENTS & GUESTS · 100% FREE</span></div>
        <div class="stitch-gw-title"><span class="bilingual-ko">수업 코드로 입장하기 (또는 자유 풀이)</span><span class="bilingual-en">Enter with Class Code or Name (Free Practice)</span></div>
      </div>
    </div>
    <p class="stitch-gw-desc"><span class="bilingual-ko">회원가입 없이 누구나 전체 문제를 자유롭게 열람하고 단계별 풀이를 시작할 수 있습니다.</span><span class="bilingual-en">Anyone can freely view all problems and start step-by-step practice without signing up.</span></p>
    <div class="stitch-gw-actions">
      <input type="text" id="stitchStudentNameInline" class="stitch-gw-input" placeholder="이름 또는 6자리 수업 코드 입력" onkeydown="if(event.key==='Enter')stitchSaveInlineName()">
      <button type="button" class="stitch-btn-enter" onclick="stitchSaveInlineName()">
        <span class="bilingual-ko">입장 ➔</span><span class="bilingual-en">Join ➔</span>
      </button>
    </div>
    <div class="stitch-gw-links">
      <a href="#" style="color:#006398" onclick="if(window.MatheduAuth)MatheduAuth.showMyProblemsModal();return false;">
        <span class="material-symbols-outlined" style="font-size:16px">folder_open</span>
        <span class="bilingual-ko">내가 푼 문제 모아보기</span><span class="bilingual-en">My Solved Problems</span>
      </a>
      <a href="#" style="color:#45464d" onclick="if(window.MatheduAuth)MatheduAuth.showGuestLoginModal();return false;">
        <span class="material-symbols-outlined" style="font-size:16px">manage_accounts</span>
        <span class="bilingual-ko">익명 기록 연동</span><span class="bilingual-en">Sync Guest Record</span>
      </a>
    </div>
  </div>
</div>

<!-- Emblem / Dandelin Spheres Visual Proof Spotlight (screens/bc0f63eb3a354cee8f964ce2bc461f3b) -->
<div class="stitch-dandelin-card">
  <div class="stitch-card-head">
    <div class="stitch-card-head-left">
      <span class="material-symbols-outlined" style="font-size:20px;color:#4F46E5">view_in_ar</span>
      <span>공식 엠블럼 Dandelin Spheres</span>
    </div>
    <span class="stitch-card-head-right" onclick="scrollToSolSection()"><span class="bilingual-ko">시각적 기하 증명 ➔</span><span class="bilingual-en">Visual Proof ➔</span></span>
  </div>
  <div class="stitch-visual-canvas">
    <div class="stitch-visual-banner" style="background-image: url('{asset_prefix}assets/stitch_dandelin_hero.png')">
      <div class="stitch-visual-overlay">
        <span class="stitch-visual-eyebrow">VISUAL PROOF ARCHIVE</span>
        <p class="stitch-visual-headline"><span class="bilingual-ko">{h1_ko_line2} · 시각적 도형과 단계별 증명</span><span class="bilingual-en">Visual Geometric Proof & Step-by-Step Derivation</span></p>
      </div>
    </div>
    <div class="stitch-visual-drawer">
      <p class="stitch-visual-desc">
        <span class="bilingual-ko">복잡한 수능 킬러 문항도 <strong style="color:#1b1b1d">시각적 도형 다이어그램</strong>과 <strong style="color:#006398">초등 눈높이 디딤돌(1~{max(1,q_count-1)}단계)</strong>로 분해하면 원리가 한눈에 보입니다.</span>
        <span class="bilingual-en">Even the most challenging exam problems become intuitive through <strong style="color:#1b1b1d">visual geometric models</strong> and <strong style="color:#006398">elementary-grounded micro-steps</strong>.</span>
      </p>
      <div class="stitch-quote-box">
        <span class="material-symbols-outlined" style="font-size:18px;color:#F59E0B;flex-shrink:0;margin-top:2px">format_quote</span>
        <p class="stitch-quote-text">
          <span class="bilingual-ko">"수식에 갇히지 않고, 눈으로 원리를 통찰하는 수학 — 수학교육의 지향점입니다."</span>
          <span class="bilingual-en">"Mathematics that sees principles visually rather than being trapped in formulas."</span>
        </p>
      </div>
    </div>
  </div>
</div>

<div class="stitch-pack-banner">
  <div class="stitch-pack-left">
    <div class="stitch-pack-icon">
      <span class="material-symbols-outlined" style="font-size:22px;color:#93ccff">backpack</span>
    </div>
    <div style="min-width:0">
      <div style="font-family:'Plus Jakarta Sans','Pretendard',sans-serif;font-size:0.9rem;font-weight:800;color:#ffffff"><span class="bilingual-ko">선택한 문항으로 수업 팩 묶기</span><span class="bilingual-en">Bundle Problems into a Lesson Pack</span></div>
      <div style="font-size:0.76rem;color:rgba(255,255,255,0.72)"><span class="bilingual-ko">학생들에게 링크 1개로 오늘 수업 문항 제공</span><span class="bilingual-en">Share multiple problems with a single link</span></div>
    </div>
  </div>
  <a href="{asset_prefix}index.html#quizExplorerSection" class="stitch-pack-btn"><span class="bilingual-ko">수업 팩 생성</span><span class="bilingual-en">Create Pack</span></a>
</div>

<div class="stitch-collections-section" id="stitchMin7014Section">
  <div style="display:flex;align-items:center;gap:8px">
    <span class="material-symbols-outlined" style="font-size:22px;color:#006398">folder_special</span>
    <h3 style="margin:0;font-family:'Plus Jakarta Sans','Pretendard',sans-serif;font-size:1.05rem;font-weight:800;color:#1b1b1d"><span class="bilingual-ko">수학자료실 공인 학습 컬렉션</span><span class="bilingual-en">Official Curated Math Collections</span></h3>
  </div>
  <a class="stitch-collection-card" href="https://www.geogebra.org/u/min7014" target="_blank" rel="noopener noreferrer">
    <div class="stitch-col-left">
      <div class="stitch-col-icon" style="background:rgba(0,99,152,0.10)">
        <span class="material-symbols-outlined" style="font-size:24px;color:#006398">view_in_ar</span>
      </div>
      <div>
        <span class="stitch-col-title">GeoGebra Tube 국제 공인 컬렉션</span>
        <span class="stitch-col-sub">3,000+ 전 세계 인증 인터랙티브 수학 앱렛</span>
      </div>
    </div>
    <span class="material-symbols-outlined" style="font-size:20px;color:#45464d">open_in_new</span>
  </a>
  <a class="stitch-collection-card" href="https://www.algeomath.kr" target="_blank" rel="noopener noreferrer">
    <div class="stitch-col-left">
      <div class="stitch-col-icon" style="background:rgba(16,185,129,0.10)">
        <span class="material-symbols-outlined" style="font-size:24px;color:#10B981">calculate</span>
      </div>
      <div>
        <span class="stitch-col-title">AlgeoMath 한국과학창의재단 자료</span>
        <span class="stitch-col-sub">한국 교육과정에 맞춘 공식 기하 탐구 활동</span>
      </div>
    </div>
    <span class="material-symbols-outlined" style="font-size:20px;color:#45464d">open_in_new</span>
  </a>
  <a class="stitch-collection-card" href="https://min7014.github.io/2019080802.html" target="_blank" rel="noopener noreferrer">
    <div class="stitch-col-left">
      <div class="stitch-col-icon" style="background:rgba(245,158,11,0.10)">
        <span class="material-symbols-outlined" style="font-size:24px;color:#F59E0B">menu_book</span>
      </div>
      <div>
        <span class="stitch-col-title">중등~고등 전 단원 개념 증명 PDF</span>
        <span class="stitch-col-sub">순서대로 체계적으로 정리된 다운로드 보관함</span>
      </div>
    </div>
    <span class="material-symbols-outlined" style="font-size:20px;color:#45464d">download</span>
  </a>
</div>

<div class="stitch-footer">
  <div class="stitch-footer-links">
    <a href="https://min7014.github.io/">공식 웹사이트</a>
    <span>·</span>
    <a href="{asset_prefix}dashboard.html">실시간 관제 대시보드</a>
    <span>·</span>
    <a href="{asset_prefix}privacy.html">개인정보처리방침</a>
  </div>
  <p class="stitch-footer-copy">© mathedu · 수학자료실. 3,400+ 시각적 수학 증명과 안티그래비티 AI가 함께 만드는 수학교육의 새 지평.</p>
</div>

<nav class="stitch-bottom-nav">
  <div class="stitch-bottom-nav-inner">
    <a href="/mathedu/" class="stitch-bnav-item">
      <span class="material-symbols-outlined" style="font-size:22px">home</span>
      <span><span class="bilingual-ko">홈</span><span class="bilingual-en">Home</span></span>
    </a>
    <button type="button" class="stitch-bnav-item active" onclick="scrollToQuizStep(0)">
      <span class="material-symbols-outlined" style="font-size:22px">quiz</span>
      <span><span class="bilingual-ko">디딤돌 퀴즈</span><span class="bilingual-en">Quizzes</span></span>
    </button>
    <button type="button" class="stitch-bnav-item" onclick="scrollToSolSection()">
      <span class="material-symbols-outlined" style="font-size:22px">view_in_ar</span>
      <span><span class="bilingual-ko">동적 기하관</span><span class="bilingual-en">Visual Proof</span></span>
    </button>
    <button type="button" class="stitch-bnav-item" onclick="if(window.openClassCreatorModal)openClassCreatorModal('{slug}')">
      <span class="material-symbols-outlined" style="font-size:22px">qr_code_scanner</span>
      <span><span class="bilingual-ko">교사용 출제</span><span class="bilingual-en">Class QR</span></span>
    </button>
    <button type="button" class="stitch-bnav-item" onclick="if(window.MatheduAuth)MatheduAuth.showMyProblemsModal()">
      <span class="material-symbols-outlined" style="font-size:22px">folder_special</span>
      <span><span class="bilingual-ko">마이룸</span><span class="bilingual-en">My Room</span></span>
    </button>
  </div>
</nav>
<script>
function scrollToOrigCard() {{
  var el = document.querySelector('.orig-card');
  if (el) el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
}}
function scrollToQuizStep(idx) {{
  var qs = document.querySelectorAll('.q');
  if (qs[idx]) {{
    if (qs[idx].classList.contains('mathedu-step-hidden') && window.toggleStitchStepMode) {{
      window.toggleStitchStepMode('all');
    }}
    qs[idx].scrollIntoView({{ behavior: 'smooth', block: 'center' }});
  }}
}}
function scrollToSolSection() {{
  var sol = document.querySelector('.sol') || document.querySelector('.min7014-addon-card');
  if (sol) {{
    if (sol.classList.contains('mathedu-step-hidden') && window.toggleStitchStepMode) {{
      window.toggleStitchStepMode('all');
    }}
    sol.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
  }}
}}
function stitchSaveInlineName() {{
  var inp = document.getElementById('stitchStudentNameInline');
  if (!inp) return;
  var val = inp.value.trim();
  if (!val) {{
    scrollToQuizStep(0);
    return;
  }}
  window._studentName = val;
  var sn = document.getElementById('studentName');
  if (sn) sn.value = val;
  if (typeof sendProgress === 'function') sendProgress();
  inp.value = '';
  inp.placeholder = '✅ ' + val + ' 님 기록 연동됨';
}}
</script>
<!-- STITCH_FOOTER_END -->"""


def clean_non_svg_inline_colors(html):
    import html as html_mod
    clean_ans = latex_ans_to_svg_text(html)

    # Convert inline <svg>...</svg> to Stitch Light Blueprint theme
    svgs = []
    def mask_svg(m):
        converted = convert_svg_to_stitch_light(m.group(0), clean_ans)
        svgs.append(converted)
        return f"__SVG_PLACEHOLDER_{len(svgs)-1}__"

    def mask_escaped_svg(m):
        unesc = html_mod.unescape(m.group(0))
        converted = convert_svg_to_stitch_light(unesc, clean_ans)
        re_esc = html_mod.escape(converted, quote=True)
        svgs.append(re_esc)
        return f"__SVG_PLACEHOLDER_{len(svgs)-1}__"

    masked = re.sub(r'<svg\b[^>]*>.*?</svg>', mask_svg, html, flags=re.S | re.I)
    masked = re.sub(r'&lt;svg\b.*?&lt;/svg&gt;', mask_escaped_svg, masked, flags=re.S | re.I)

    # Replace dark/pale inline styles outside SVGs
    replacements = [
        ('color:#7cc4ff', 'color:#006398'),
        ('color:#5eead4', 'color:#047857'),
        ('color:#6ee7b7', 'color:#047857'),
        ('color:#93c5fd', 'color:#0284c7'),
        ('color:#a78bfa', 'color:#4f46e5'),
        ('color:#fde68a', 'color:#b45309'),
        ('color:#fecdd3', 'color:#be123c'),
        ('color:#fb7185', 'color:#be123c'),
        ('color:#9aa6c0', 'color:#64748b'),
        ("color='#9aa6c0'", "color='#64748b'"),
        ('color:#cbd5e1', 'color:#475569'),
        ('color:#67e8f9', 'color:#006398'),
        ('color:#c084fc', 'color:#4f46e5'),
        ('color:#d8b4fe', 'color:#4f46e5'),
        ('border:1px solid #2e3850', 'border:1px solid #cbd5e1'),
        ("borderColor='#2e3850'", "borderColor='#cbd5e1'"),
        ('background:rgba(255,255,255,.06)', 'background:#f1f5f9'),
        ('background:rgba(124,196,255,.16)', 'background:#e0f2fe'),
        ('border:1px solid rgba(124,196,255,.25)', 'border:1px solid #cbd5e1'),
        ('border:1px solid rgba(124,196,255,.35)', 'border:1px solid #cbd5e1'),
        ('border-top:1px dashed rgba(124,196,255,.35)', 'border-top:1px dashed #cbd5e1'),
        ('background:rgba(94,234,212,.14)', 'background:#ecfdf5'),
        ('background:rgba(94,234,212,.10)', 'background:#f0fdf4'),
        ('background:rgba(251,113,133,.12)', 'background:#fff1f2'),
    ]
    for old_s, new_s in replacements:
        masked = masked.replace(old_s, new_s)

    # Hide trackFull by default so 0-sec entry works immediately
    masked = re.sub(
        r'(<div\s+id="trackFull"\s+style="position:fixed;inset:0;z-index:9999;)display:flex;',
        r'\1display:none;',
        masked
    )

    # Add cache-busting query string to mathedu-room.js and mathedu-report.js
    masked = re.sub(r'mathedu-room\.js(\?v=[^"\']*)?', 'mathedu-room.js?v=20261027_stitch3', masked)
    masked = re.sub(r'mathedu-report\.js(\?v=[^"\']*)?', 'mathedu-report.js?v=20261027_stitch3', masked)

    # Restore SVGs
    for idx, s in enumerate(svgs):
        masked = masked.replace(f"__SVG_PLACEHOLDER_{idx}__", s)

    return masked


def transform_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    slug = os.path.basename(filepath).replace('.html', '')
    is_private = ('private' in filepath.replace('\\', '/'))
    asset_prefix = '../../' if is_private else '../'

    # 1. Extract h1 and lead BEFORE stripping STITCH_HEADER
    h1_m = re.search(r'<h1[^>]*>(.*?)</h1>', html, flags=re.S)
    h1_inner = h1_m.group(1) if h1_m else slug
    main_m = re.search(r'<span class="stitch-h1-main">(.*?)</span>', h1_inner, flags=re.S)
    acc_m = re.search(r'<span class="stitch-h1-accent">(.*?)</span>', h1_inner, flags=re.S)
    en_m = re.search(r'<span class="bilingual-en">(.*?)</span>', h1_inner, flags=re.S)
    if slug in CUSTOM_TITLE_MAP:
        h1_line1, h1_line2, h1_en_text = CUSTOM_TITLE_MAP[slug]
    elif main_m and acc_m:
        h1_line1 = main_m.group(1).strip()
        h1_line2 = acc_m.group(1).strip()
        h1_en_text = en_m.group(1).strip() if en_m else (h1_line1 + ' ' + h1_line2)
    else:
        ko_m = re.search(r'<span class="bilingual-ko">(.*?)</span>', h1_inner, flags=re.S)
        if ko_m:
            h1_ko_raw = re.sub(r'<[^>]+>', '', ko_m.group(1)).strip()
        else:
            h1_ko_raw = re.sub(r'<[^>]+>', '', h1_inner).strip()
        h1_en_text = en_m.group(1).strip() if en_m else h1_ko_raw
        h1_line1, h1_line2 = split_title_two_tone(h1_ko_raw, slug=slug)

    lead_m = re.search(r'<p class="lead">(.*?)</p>', html, flags=re.S)
    lead_inner = lead_m.group(1) if lead_m else '초등학생도 1단계부터 차근차근 따라가면 수능·학력평가 본문항까지 스스로 풀 수 있는 단계별 디딤돌 퀴즈입니다.'

    # 2. Strip any previous STITCH_HEADER / STITCH_EXPLORER / STITCH_FOOTER blocks if re-running
    html = re.sub(r'<!-- STITCH_HEADER_START -->.*?<!-- STITCH_HEADER_END -->\s*', '', html, flags=re.S)
    html = re.sub(r'<!-- STITCH_EXPLORER_START -->.*?<!-- STITCH_EXPLORER_END -->\s*', '', html, flags=re.S)
    html = re.sub(r'\s*<!-- STITCH_FOOTER_START -->.*?<!-- STITCH_FOOTER_END -->', '', html, flags=re.S)

    # 3. Ensure Google Fonts & Material Symbols Outlined before <style>
    html = re.sub(
        r'(<link rel="preconnect" href="https://fonts\.googleapis\.com">.*?pretendard\.min\.css"\s*/>\s*)*<style>.*?</style>',
        lambda m: STITCH_FONTS_HEAD + '\n' + STITCH_CSS,
        html,
        count=1,
        flags=re.S
    )

    q_count = len(re.findall(r'<div class="q[\s"]', html))

    stitch_top = build_stitch_top_shell(
        slug, asset_prefix, h1_inner, h1_line1, h1_line2, h1_en_text, lead_inner, q_count
    )
    stitch_explorer = build_stitch_explorer_shell(q_count)
    stitch_bottom = build_stitch_bottom_shell(slug, asset_prefix, h1_line2, q_count)

    # 4. Replace from <div class="wrap"> through <p class="lead">...</p> with <div class="wrap">\n + stitch_top
    pattern_top = re.compile(
        r'<div class="wrap">\s*<div class="topbar">.*?</div>\s*</div>\s*<div class="score">.*?</div>\s*<h1[^>]*>.*?</h1>\s*<p class="lead">.*?</p>',
         flags=re.S
    )
    if pattern_top.search(html):
        html = pattern_top.sub(lambda m: '<div class="wrap">\n' + stitch_top, html, count=1)
    else:
        pattern_top_alt = re.compile(
            r'<div class="wrap">.*?(?=<!-- ★ 원본 문제 카드|<div class="orig-card"|<h2>)',
            flags=re.S
        )
        html = pattern_top_alt.sub(lambda m: '<div class="wrap">\n' + stitch_top + '\n', html, count=1)

    # 5. Add Stitch CTA buttons inside .orig-card right before its closing </div> (if not already present)
    if '<div class="stitch-orig-cta-stack">' not in html:
        orig_cta_html = f"""
  <div class="stitch-orig-cta-stack">
    <button type="button" class="stitch-cta-black" onclick="scrollToQuizStep(0)">
      <span class="material-symbols-outlined" style="font-size:18px">sports_esports</span>
      <span><span class="bilingual-ko">1단계 디딤돌부터 바로 풀기</span><span class="bilingual-en">Start Solving from Step 1</span></span>
      <span class="material-symbols-outlined" style="font-size:16px">arrow_forward</span>
    </button>
    <div class="stitch-cta-sub-grid">
      <button type="button" class="stitch-cta-gray" onclick="scrollToSolSection()">
        <span class="material-symbols-outlined" style="font-size:16px;color:#006398">picture_as_pdf</span>
        <span><span class="bilingual-ko">시각적 도형·원리 해설</span><span class="bilingual-en">Visual Proof & Solution</span></span>
      </button>
      <button type="button" class="stitch-cta-gray" onclick="var m=document.querySelector('.min7014-addon-card');if(m)m.scrollIntoView({{behavior:'smooth'}});">
        <span class="material-symbols-outlined" style="font-size:16px;color:#45464d">language</span>
        <span><span class="bilingual-ko">수학자료실 웹 탐구</span><span class="bilingual-en">Explore Archive</span></span>
      </button>
    </div>
  </div>
</div>"""
        html = re.sub(
            r'(<div class="orig-card">(?:(?!<h2).)*?)(</div>(\s*<!--[^>]*-->)*\s*(?=<h2))',
            lambda m: m.group(1) + orig_cta_html + '\n',
            html,
            count=1,
            flags=re.S
        )

    # 5b. Insert stitch_explorer right before the first <h2> (which is right after .orig-card)
    html = re.sub(
        r'(<h2)',
        lambda m: stitch_explorer + '\n' + m.group(1),
        html,
        count=1
    )

    # 6. Insert stitch_bottom right after <div class="final">...</button></div>
    html = re.sub(
        r'(<div class="final">.*?</button>\s*</div>)',
        lambda m: m.group(1) + '\n' + stitch_bottom,
        html,
        count=1,
        flags=re.S
    )

    # 7. Clean non-SVG pale/dark inline colors, convert SVGs to Stitch Light, & hide #trackFull by default
    html = clean_non_svg_inline_colors(html)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)


if __name__ == '__main__':
    files = sorted(glob.glob('board/*.html') + glob.glob('board/private/*.html'))
    for idx, fp in enumerate(files):
        transform_file(fp)
    print(f"Successfully transformed {len(files)} board files to exact Stitch screen bc0f63eb3a354cee8f964ce2bc461f3b design!")
