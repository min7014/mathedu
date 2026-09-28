import os
import glob
import re
import json
import min7014_matcher

EXTRA_CSS = """
.min-btn-algeo{background:rgba(168,85,247,.16);border:1px solid rgba(168,85,247,.45);color:#c084fc}
.min-btn-algeo:hover{background:#a855f7;color:#fff}
.min-cat-badge{display:inline-block;font-size:.72rem;padding:2px 8px;border-radius:6px;background:rgba(124,196,255,.12);color:#93c5fd;border:1px solid rgba(124,196,255,.25);margin-bottom:6px}
.min-visual-tip{background:linear-gradient(135deg,rgba(124,196,255,.12) 0%,rgba(167,139,250,.10) 100%);border:1px solid rgba(124,196,255,.35);border-left:4px solid #38bdf8;border-radius:12px;padding:12px 16px;margin:18px 0;font-size:.88rem;line-height:1.6;color:#e0e7ff}
.min-visual-tip b{color:#67e8f9}
.min-ggb-frame-wrap{margin-top:12px;border-radius:12px;overflow:hidden;border:1px solid rgba(56,189,248,.4);background:#000;display:none}
.min-ggb-frame-wrap.active{display:block}
"""

def update_board_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract clean title
    title_m = re.search(r'<title>(.*?)</title>', content)
    raw_title = title_m.group(1).strip() if title_m else ""
    clean_title = re.sub(r'\s*·\s*min7014.*|\s*\|\s*min7014.*', '', raw_title).strip()

    matched_items = min7014_matcher.match_materials(clean_title, limit=4)

    # 1. Update CSS if missing .min-btn-algeo
    if '.min-btn-algeo' not in content:
        content = content.replace('</style>', EXTRA_CSS + '\n</style>', 1)

    # 2. Insert or replace .min-visual-tip
    v_tip = min7014_matcher.get_visual_tip(clean_title, matched_items)
    v_tip_html = f'<div class="min-visual-tip">{v_tip}</div>'

    # If already has min-visual-tip, replace it
    if '<div class="min-visual-tip">' in content:
        content = re.sub(r'<div class="min-visual-tip">.*?</div>', lambda m: v_tip_html, content, count=1, flags=re.DOTALL)
    else:
        # Insert after orig-card closing </div> or before <h2>🔰
        if '</div>\n<h2>🔰' in content:
            content = content.replace('</div>\n<h2>🔰', f'</div>\n{v_tip_html}\n<h2>🔰', 1)
        elif '</div><h2>🔰' in content:
            content = content.replace('</div><h2>🔰', f'</div>\n{v_tip_html}\n<h2>🔰', 1)
        elif '<div class="orig-card">' in content:
            idx = content.find('<div class="orig-card">')
            end_card_idx = content.find('</div>', content.find('orig-tip', idx) if 'orig-tip' in content[idx:] else idx)
            if end_card_idx != -1:
                end_card_close = content.find('</div>', end_card_idx)
                end_pos = end_card_close + 6
                content = content[:end_pos] + '\n' + v_tip_html + content[end_pos:]

    # 3. Update min7014-addon-card
    new_card_html = min7014_matcher.generate_addon_card_html(matched_items, clean_title)

    old_card_pattern = re.compile(
        r'(?:<!-- 📚 min7014 수학자료실 공식 연계 심층 탐구 자료 카드 -->\s*)?<div class="min7014-addon-card">.*?</div>\s*(?:<script>.*?</script>)?(?=\s*(?:<div class="final">|<div class="q-actions">|<script\b|$))',
        re.DOTALL
    )

    if old_card_pattern.search(content):
        content = old_card_pattern.sub(lambda m: new_card_html.strip() + '\n', content, count=1)
    else:
        if '<div class="final">' in content:
            content = content.replace('<div class="final">', new_card_html + '\n<div class="final">', 1)
        elif '</body>' in content:
            content = content.replace('</body>', new_card_html + '\n</body>', 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return len(matched_items)

def run():
    files = sorted(glob.glob('board/*.html'))
    print(f"Applying deep min7014 precision analysis to {len(files)} board files...")
    
    for f in files:
        count = update_board_file(f)
        print(f"  [OK] {os.path.basename(f)} (matched {count} materials)")

    print("All board files updated successfully with precision matches!")

if __name__ == '__main__':
    run()
