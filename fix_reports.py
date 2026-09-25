import re

with open('C:/Users/min/Desktop/mathedu/board/48d0d98f.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix 1: Move report-msg outside report-form so it remains visible after form is hidden
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.lstrip()
    
    # Check if this line contains a report-msg div (single line)
    if 'class="report-msg"' in stripped and stripped.startswith('<div class="report-msg"') and stripped.rstrip().endswith('</div>'):
        # Next two lines should be closing divs for report-form and report-wrap
        if i + 2 < len(lines):
            close_form = lines[i + 1]  # </div> for report-form
            close_wrap = lines[i + 2]  # </div> for report-wrap
            
            # Use the indentation of close_form for the report-msg
            indent = close_form[:len(close_form) - len(close_form.lstrip())]
            
            # Add closing div for report-form
            new_lines.append(close_form)
            # Add report-msg with same indentation as close_form
            new_lines.append(indent + stripped)
            # Add closing div for report-wrap
            new_lines.append(close_wrap)
            i += 3
            continue
    
    new_lines.append(line)
    i += 1

content = ''.join(new_lines)

# Fix 2: Replace \frac with \dfrac in know sections for better display
def replace_frac_in_know(match):
    section = match.group(0)
    # Replace \frac{ with \dfrac{ but protect existing \dfrac{
    section = re.sub(r'\\dfrac\{', r'\\TEMPFRAC{', section)
    section = re.sub(r'\\frac\{', r'\\dfrac{', section)
    section = re.sub(r'\\TEMPFRAC\{', r'\\dfrac{', section)
    return section

content = re.sub(r'<div class="know">.*?</div>', replace_frac_in_know, content, flags=re.DOTALL)

with open('C:/Users/min/Desktop/mathedu/board/48d0d98f.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! Fixed report visibility and added \\dfrac in know sections.")
