import re
from pathlib import Path

p = Path('board/2411860a.html')
raw = p.read_text(encoding='utf-8')

ss = re.compile(r'<(script|style)\b[^>]*>.*?</\1>', re.DOTALL | re.IGNORECASE)
body = ss.sub('', raw)

math_slots = {}
c = [0]

def _math(m):
    k = f'\x00MATH{c[0]}\x00'
    math_slots[k] = m.group(0)
    c[0] += 1
    return k

no_math = re.sub(r'\$[^$]*\$', _math, body)
def _text(m):
    k = f'\x00TEXT{c[0]}\x00'
    math_slots[k] = m.group(0)
    c[0] += 1
    return k
no_math = re.sub(r'\\text\{[^}]*\}', _text, no_math)
no_math = re.sub(r'\\frac\{[^}]*\}\{[^}]*\}', _text, no_math)
no_math = re.sub(r'\\displaystyle', _text, no_math)

hits = []
for m in re.finditer(r'\d+', no_math):
    st = max(0, m.start()-30)
    en = min(len(no_math), m.end()+30)
    hits.append((m.group(0), no_math[st:en].replace('\n',' ')))

print('=== [잔여 비-LaTeX 연속 숫자 검사] ===')
if not hits:
    print('결과: 없음 — 모든 숫자가 LaTeX 처리됨')
else:
    print(f'검출: {len(hits)}건')
    for num, ctx in hits:
        print(f'  "{num}"  …{ctx}…')

print()
print('=== data-ans 보존 확인 ===')
print('data-ans 값들:', re.findall(r'data-ans="\d+"', raw))

print()
print('=== script/style 복원 확인 ===')
print('잔여 슬롯 마커:', raw.count('\x00MATH') + raw.count('\x00TEXT'))
