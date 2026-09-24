#!/usr/bin/env python3
"""
mathedu HTML 내 모든 숫자·분수를 LaTeX로 자동 변환 (제3판).
- <script>, <style> 블록은 변환 대상에서 완전 제외 후 복원
- data-ans 속성(채점키)은 untouched 보존
- data-exp 속성값과 가시적 텍스트 노드만 변환
- math 영역($...$ 등)은 보호, 나머지는 숫자→\text{}, 분수→\frac{}
"""
from pathlib import Path
import re
import sys

SCRIPT_STYLE = re.compile(r'<(script|style)\b[^>]*>.*?</\1>', re.S | re.I)
DATA_ANS = re.compile(r'(data-ans=")[^"]*(")')
DATA_EXP = re.compile(r'(data-exp=")([^"]*)(")')
TEXT_NODE = re.compile(r'>([^<]+)<')

def tokenize_non_math(text: str) -> str:
    tokens = []
    i = 0
    n = len(text)
    while i < n:
        m = re.match(r'\(([^)]+)\)\s*/\s*(\d+)', text[i:])
        if m:
            tokens.append(f'$\frac{{{m.group(1).strip()}}}{{{m.group(2)}}}$')
            i += m.end()
            continue
        m = re.match(r'(\d+)\s*/\s*(\d+)', text[i:])
        if m:
            tokens.append(f'$\frac{{{m.group(1)}}}{{{m.group(2)}}}$')
            i += m.end()
            continue
        m = re.match(r'\d+(?:\.\d+)?', text[i:])
        if m:
            tokens.append(f'$\text{{{m.group(0)}}}$')
            i += m.end()
            continue
        tokens.append(text[i])
        i += 1
    return ''.join(tokens)

def convert_non_math_regions(text: str) -> str:
    out = []
    last = 0
    for m in re.finditer(r'\$[^$]*\$', text):
        if m.start() > last:
            out.append(tokenize_non_math(text[last:m.start()]))
        out.append(m.group(0))
        last = m.end()
    if last < len(text):
        out.append(tokenize_non_math(text[last:]))
    return ''.join(out)

def process_html(path: Path):
    raw = path.read_text(encoding='utf-8')

    # 1) script/style 블록 보호 → 토큰 치환
    ss_slots = {}
    def _ss(m):
        key = f'\x00SS{len(ss_slots)}\x00'
        ss_slots[key] = m.group(0)
        return key
    tmp = SCRIPT_STYLE.sub(_ss, raw)

    # 2) data-ans 보존 (채점키 untouched)
    ans_slots = {}
    def _ans(m):
        key = f'\x00ANS{len(ans_slots)}\x00'
        ans_slots[key] = m.group(0)
        return key
    tmp = DATA_ANS.sub(_ans, tmp)

    # 3) data-exp 속성값 변환
    def _de(m):
        return m.group(1) + convert_non_math_regions(m.group(2)) + m.group(3)
    tmp = DATA_EXP.sub(_de, tmp)

    # 4) visible 텍스트 노드 변환 (script/style/data-ans는 이미 제외됨)
    def _txt(m):
        return '>' + convert_non_math_regions(m.group(1)) + '<'
    tmp = TEXT_NODE.sub(_txt, tmp)

    # 5) data-ans 복원
    for k, v in ans_slots.items():
        tmp = tmp.replace(k, v)

    # 6) script/style 복원 (반드시 마지막)
    for k, v in ss_slots.items():
        tmp = tmp.replace(k, v)

    path.write_text(tmp, encoding='utf-8')

    # 7) 자동 검증: \x00 마커가 남아있으면 경고
    remain = tmp.count('\x00')
    if remain != 0:
        raise RuntimeError(f'[검증실패] {path.name}에 \\x00 마커 {remain}개 남음')
    return path

if __name__ == '__main__':
    base = Path(r'C:\Users\min\Desktop\mathedu\board')
    targets = list(sys.argv[1:]) if len(sys.argv) > 1 else [str(p) for p in base.glob('*.html')]
    for t in targets:
        p = Path(t)
        process_html(p)
        print(f'[OK+검증통과] {p.name}')
