#!/usr/bin/env python3
"""
mathedu HTML 내 모든 숫자·분수를 LaTeX로 자동 변환하는 스크립트.
- <script>, <style> 블록은 제외
- data-ans 속성(채점용 숫자)은 제외
- data-exp 속성(LaTeX 해설)과 가시적 텍스트 노드는 변환 대상
- 비수학 영역의 숫자 → $\text{...}$
- 비수학 영역의 단순 분수(a/b) 및 괄호서술형 분수((...)/b) → $\frac{...}{...}$
- 이미 $...$로 감싸인 수학 영역은 그대로 보존
"""

import re
import sys
from pathlib import Path

SCRIPT_STYLE_RE = re.compile(r'<(script|style)\b[^>]*>.*?</\1>', re.DOTALL | re.IGNORECASE)
DATA_EXP_RE = re.compile(r'(data-exp)="([^"]*)"')
TEXT_NODE_RE = re.compile(r'>([^<]+)<')
DATA_ANS_RE = re.compile(r'(data-ans)="(\d+)"')


def tokenize_non_math(text: str):
    """비수학 영역을 왼쪽부터 스캔하며 분수→\frac, 숫자→\text{...}로 토큰화한다."""
    tokens = []
    pos = 0
    n = len(text)

    while pos < n:
        # 1) 괄호서술형 분수: ( ... ) / digit
        m = re.match(r'\(([^)]+)\)\s*/\s*(\d+)', text[pos:])
        if m:
            num = m.group(1).strip()
            den = m.group(2)
            tokens.append(f'$\\frac{{{num}}}{{{den}}}$')
            pos += m.end()
            continue

        # 2) 단순 분수: digit / digit
        m = re.match(r'(\d+)\s*/\s*(\d+)', text[pos:])
        if m:
            tokens.append(f'$\\frac{{{m.group(1)}}}{{{m.group(2)}}}$')
            pos += m.end()
            continue

        # 3) 소수 포함 정수
        m = re.match(r'\d+(?:\.\d+)?', text[pos:])
        if m:
            tokens.append(f'$\\text{{{m.group(0)}}}$')
            pos += m.end()
            continue

        # 4) 일반 문자
        tokens.append(text[pos])
        pos += 1

    return ''.join(tokens)


def convert_non_math_regions(text: str) -> str:
    """$...$로 이미 감싸인 수학 영역을 보존한 채, 나머지 비수학 영역만 변환."""
    out = []
    last = 0
    for m in re.finditer(r'\$(.*?)\$', text):
        if m.start() > last:
            out.append(tokenize_non_math(text[last:m.start()]))
        out.append(f'${m.group(1)}$')
        last = m.end()
    if last < len(text):
        out.append(tokenize_non_math(text[last:]))
    return ''.join(out)


def process_html(path: Path):
    raw = path.read_text(encoding='utf-8')

    # (1) script / style 블록 보존
    ss_slots = {}
    counter = 0

    def _ss(m):
        nonlocal counter
        key = f'\x00SS{counter}\x00'
        ss_slots[key] = m.group(0)
        counter += 1
        return key

    tmp = SCRIPT_STYLE_RE.sub(_ss, raw)

    # (2) data-ans는 채점 로직용이므로 보존 (변환하지 않음)
    #     먼저 data-ans 값을 슬롯으로 빼둔다
    ans_slots = {}

    def _ans(m):
        key = f'\x00ANS{counter}\x00'
        # counter와 충돌하지 않게 별도 카운터 사용
        ans_slots[key] = m.group(0)
        return key

    # data-ans는 숫자로만 구성된 속성값이므로 별도 처리
    tmp = DATA_ANS_RE.sub(lambda m: f'\x00ANS{len(ans_slots)}\x00', tmp)
    # 위 서브에서 카운터 꼬임 방지: 다시 mapping
    # 실제로는 아래처럼 정정:
    ans_slots.clear()
    tmp = raw  # 재설정
    tmp = SCRIPT_STYLE_RE.sub(_ss, tmp)
    # data-ans 슬롯팅 (counter 재사용 금지)
    ans_idx = [0]

    def _ans2(m):
        key = f'\x00ANS{ans_idx[0]}\x00'
        ans_slots[key] = m.group(0)
        ans_idx[0] += 1
        return key

    tmp = DATA_ANS_RE.sub(_ans2, tmp)

    # (3) data-exp 속성값 변환 (LaTeX 해설, 가시적 영역)
    def _de(m):
        return f'{m.group(1)}="{convert_non_math_regions(m.group(2))}"'

    tmp = DATA_EXP_RE.sub(_de, tmp)

    # (4) 가시적 텍스트 노드 변환
    def _txt(m):
        return f'>{convert_non_math_regions(m.group(1))}<'

    tmp = TEXT_NODE_RE.sub(_txt, tmp)

    # (5) script/style 복원
    for k, v in ss_slots.items():
        tmp = tmp.replace(k, v)

    # (6) data-ans 복원
    for k, v in ans_slots.items():
        tmp = tmp.replace(k, v)

    path.write_text(tmp, encoding='utf-8')
    return path


if __name__ == '__main__':
    board = Path(r'C:\Users\min\Desktop\mathedu\board')
    targets = list(board.glob('*.html'))
    if len(sys.argv) > 1:
        targets = [Path(sys.argv[1])]
    for p in targets:
        process_html(p)
        print(f'[OK] {p.name}')
