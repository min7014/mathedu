"""Update all existing board HTML files to move tracking block to top."""
import os, re, glob

BOARD = "C:/Users/min/Desktop/mathedu/board"
modified = 0

for path in sorted(glob.glob(os.path.join(BOARD, '*.html'))):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and extract the tracking block
    m = re.search(r'(<div id="trackSubmit".*?</script>)', content, re.DOTALL)
    if not m:
        continue
    
    tracking_block = m.group(1)
    
    # Remove from current position
    content = content.replace(tracking_block, '')
    
    # Insert after topbar closing div, before score div
    # Find the score div and insert tracking before it
    score_idx = content.find('<div class="score">')
    if score_idx >= 0:
        content = content[:score_idx] + tracking_block + '\n' + content[score_idx:]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        modified += 1
        print(f"✓ {os.path.basename(path)}")
    else:
        print(f"- {os.path.basename(path)} (no score div found)")

print(f"\nDone: {modified} files updated")
