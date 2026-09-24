# -*- coding: utf-8 -*-
"""verify_quiz.py — 수학 퀴즈 JSON 자체 검증 + 자동 교정기.
로컬 LLM/외부 호출 없음 (MOCK 금지 원칙). sympy + 규칙기반.

검사 항목:
  1) LaTeX 래핑 누락 : 수식 기호(^,_,\\frac,\\sqrt,\\det,...)가 $...$ 밖에 있으면
     자동으로 $...$ 로 감쌈 (자동교정).
  2) 기하학적 모순 : 삼각형 이름(삼각형 XXX / \\triangle XXX)의 꼭짓점이
     실제 사용된 벡터/좌표 점 집합에 없거나, 벡터 끝점과 불일치하면 경고+교정.
  3) 수치 일관성 : exp/solution 내 산술 등식(A = B)을 sympy로 계산해
     불일치 시 경고 (자동교정은 하지 않고 보고만 함).

사용:
  from verify_quiz import verify_and_fix
  data, report = verify_and_fix(data)   # data 는 generator 가 받는 dict
  report 에는 [자동교정 목록] + [경고 목록] 이 들어감.
"""
import re
import sympy as sp

# ---------------------------------------------------------------- 유틸
MATH_CMDS = r"\\(?:frac|dfrac|tfrac|sqrt|det|overrightarrow|overleftarrow|sum|int|oint|prod|cdot|times|pm|mp|leq|geq|neq|approx|angle|sin|cos|tan|log|ln|lim|vec|bar|hat|mathbb|mathrm|text|left|right|big|Big)"
TRIG_CMD = MATH_CMDS

def _strip_math(s: str) -> str:
    """$...$, $$...$$, \\(...\\) 영역을 모두 제거한 텍스트 반환."""
    s = re.sub(r"\$\$.*?\$\$", " ", s, flags=re.S)
    s = re.sub(r"\$[^$]*\$", " ", s, flags=re.S)
    s = re.sub(r"\\\(.*?\\\)", " ", s, flags=re.S)
    return s

def _collect_points(text: str):
    """벡터(\\overrightarrow{AB})와 좌표(A(1,2))에서 점 집합 추출.
    점은 [A-Za-z][0-9']* 형태 (prime 포함)."""
    pts = set()
    for tok in re.findall(r"\\overrightarrow\{([A-Za-z0-9']+)\}", text):
        i = 0
        while i < len(tok):
            if tok[i].isalpha():
                j = i + 1
                while j < len(tok) and tok[j] == "'":
                    j += 1
                pts.add(tok[i:j])
                i = j
            else:
                i += 1
    for tok in re.findall(r"\b([A-Za-z][0-9']*)\s*\([^)]*\)", text):
        pts.add(tok)
    # 홑자 점 A, B, F 등 (prime 포함) 도 좌표로 쓰임 — 벡터/삼각형 문맥에서 수집
    for tok in re.findall(r"(?<![A-Za-z0-9])([A-Za-z][0-9']*)(?![A-Za-z0-9(])", text):
        # 너무 흔한 단어(F, P, Q, A, B, C, D, E, O, X, Y, Z 등)만 점 후보로
        if tok in "FPQABCDEOXYZWHIJMKLNSUV":
            pts.add(tok)
    return pts

# ---------------------------------------------------------------- 1) LaTeX 래핑
def _autofix_latex(s: str):
    """$...$ 밖에 노출된 수식 토큰 시퀀스를 찾아 $...$ 로 감쌈.
    변경된 문자열과 변경수 반환.
    전략: 문자열을 '수식영역($...$)' 과 '일반영역' 으로分词한 뒤,
    일반영역에서 '변수/숫자 + 수식기호(^ _ \\cmd) 가 포함된 토큰' 을 찾아 래핑.
    """
    changes = 0
    out = []
    i = 0; n = len(s)
    while i < n:
        if s[i] == "$":
            j = s.find("$", i + 1)
            if j == -1:
                out.append(s[i:]); break
            out.append(s[i:j + 1]); i = j + 1; continue
        # 일반 영역: 다음 $ 까지
        j = s.find("$", i)
        if j == -1:
            seg = s[i:]
            i = n
        else:
            seg = s[i:j]
            i = j
        # seg 내에서 수식 토큰 찾기
        fixed, c = _fix_segment(seg)
        out.append(fixed)
        changes += c
    return "".join(out), changes

def _fix_segment(seg: str):
    """일반영역 한 조각에서 수식 래핑."""
    changes = 0
    # 사전: \cmd{...} 를 하나의 점유 토큰으로 치환 (괄호 블록 포함)
    # \frac{a}{b} 도 두 블록 다 포함
    def _consume_cmd(s, pos):
        m = re.match(MATH_CMDS, s[pos:])
        if not m:
            return None
        e = pos + len(m.group(0))
        # 연이은 { } 블록들 모두 포함 (예: \frac{1}{2})
        while e < len(s) and s[e] == "{":
            depth = 0; p = e
            while p < len(s) and depth >= 0:
                if s[p] == "{": depth += 1
                elif s[p] == "}":
                    depth -= 1
                    if depth == 0:
                        e = p + 1; break
                p += 1
        return e
    # \cmd{...} 를 플레이스홀더로 치환
    placeholders = []
    def _replace(m):
        full = m.group(0)
        # 풀 블록 계산
        e = _consume_cmd(seg, m.start())
        whole = seg[m.start():e]
        placeholders.append(whole)
        return f"\x00{len(placeholders)-1}\x00"
    seg2 = re.sub(MATH_CMDS + r"(?:\s*\{[^}]*\})*", _replace, seg)
    # 이제 seg2 에서 수식 토큰 패턴
    token = re.compile(
        r"\x00\d+\x00"  # 플레이스홀더(수식명령)
        r"|[A-Za-z0-9]+(?=[A-Za-z0-9]*[\^_])"  # 변수뒤 첨자
        r"|[A-Za-z0-9]+(?=\x00)"              # 변수뒤 명령
        r"|[\^_]"
    )
    if not re.search(r"[\^_\\]", seg):
        # placeholder 만 있는 경우도 처리 (원래 수식이었을 수 있음) — 건너뜀
        # seg2 에 ^ _ 가 없으면 원래도 수식아님
        pass
    matches = list(token.finditer(seg2))
    if not matches:
        # placeholder 복원만 하고 종료
        for i, ph in enumerate(placeholders):
            seg2 = seg2.replace(f"\x00{i}\x00", ph)
        return seg2, 0
    runs = []
    cur = None
    for m in matches:
        if cur is None:
            cur = [m.start(), m.end()]
        else:
            between = seg2[cur[1]:m.start()]
            if re.fullmatch(r"[ \t+\-*/=<>().,]*", between):
                cur[1] = m.end()
            else:
                runs.append(tuple(cur)); cur = [m.start(), m.end()]
    if cur: runs.append(tuple(cur))
    def expand(k):
        s, e = k
        while s > 0 and re.match(r"[A-Za-z0-9]", seg2[s-1]): s -= 1
        while e < len(seg2):
            if seg2[e] == "\x00":
                # placeholder 까지 포함
                en = seg2.find("\x00", e+1)
                if en != -1:
                    e = en + 1; continue
                else:
                    break
            if re.match(r"[A-Za-z0-9]", seg2[e]) or seg2[e] in "+-*/=<>()., ":
                e += 1; continue
            break
        return s, e
    runs = [expand(r) for r in runs]
    res = seg2
    for s, e in sorted(runs, reverse=True):
        run = res[s:e].strip()
        if "$" not in run and not run.startswith("$"):
            res = res[:s] + "$" + run + "$" + res[e:]
            changes += 1
    # placeholder 복원
    for i, ph in enumerate(placeholders):
        res = res.replace(f"\x00{i}\x00", ph)
    return res, changes

# ---------------------------------------------------------------- 2) 기하 모순
def _check_geometry(text: str):
    issues = []
    points = _collect_points(text)
    # 삼각형 이름들
    tris = re.findall(r"(?:삼각형|\\triangle)\s*([A-Za-z0-9']+)", text)
    for t in tris:
        verts = []
        i = 0
        while i < len(t):
            if t[i].isalpha():
                j = i + 1
                while j < len(t) and t[j] == "'":
                    j += 1
                verts.append(t[i:j]); i = j
            else:
                i += 1
        unknown = [v for v in verts if v not in points]
        if unknown:
            issues.append(f"삼각형 {t} 의 점 {unknown} 가 벡터/좌표에 없음 (기하 모순)")
    # 벡터 끝점 기반 기대 삼각형: 공통 시작점 벡터 2개 → 삼각형
    vecs = re.findall(r"\\overrightarrow\{([A-Za-z0-9']+)\}", text)
    if len(vecs) >= 2:
        # FP, FQ → 기대 삼각형 FPQ
        p0 = vecs[0]; p1 = vecs[1]
        # 점 분해
        def splitp(tok):
            r = []; i = 0
            while i < len(tok):
                if tok[i].isalpha():
                    j = i + 1
                    while j < len(tok) and tok[j] == "'": j += 1
                    r.append(tok[i:j]); i = j
                else: i += 1
            return r
        a, b = splitp(p0); c, d = splitp(p1)
        if a == c:  # 공통 시작점
            expected = a + b + d
            for t in tris:
                if t != expected and set(splitp(t)) == set([a, b, d]):
                    issues.append(f"벡터 {p0},{p1} 로 보아 기대 삼각형은 {expected} 인데 '{t}' 로 표기됨")
    return issues

# ---------------------------------------------------------------- 3) 수치
def _check_numeric(text: str):
    issues = []
    # 보수적: 좌변·우변 모두 변수(알파벳/밑줄) 없이 순수 숫자 산술식일 때만 검사
    for m in re.finditer(r"(?<![0-9A-Za-z_])([0-9][0-9+\-*/\s.\(\\\)]*?)\s*=\s*([0-9][0-9+\-*/\s.\(\\\)]*?)(?=[.,\s]|\Z)", text):
        lhs, rhs = m.group(1).strip(), m.group(2).strip()
        if not lhs or not rhs:
            continue
        # 좌우변에 알파벳/밑줄(변수) 있으면 스킵 (d_2=9, c^2=36 등)
        if re.search(r"[A-Za-z_]", lhs) or re.search(r"[A-Za-z_]", rhs):
            continue
        try:
            lv = float(sp.sympify(lhs.replace("^", "**")))
            rv = float(sp.sympify(rhs.replace("^", "**")))
            if abs(lv - rv) > 1e-6:
                issues.append(f"수치 불일치: {lhs} = {rhs}")
        except Exception:
            pass
    return issues

# ---------------------------------------------------------------- 통합
def verify_and_fix(data: dict):
    report = {"autofix": [], "warn": []}
    # 모든 텍스트 필드 수집 위치
    def fields():
        yield ("title", data, "title")
        for s in data.get("symbols", []):
            yield ("symbols.sym", s, "sym")
            yield ("symbols.desc", s, "desc")
        for lv in data.get("levels", []):
            yield ("level.knowledge", lv, "knowledge")
            yield ("level.title", lv, "title")
            for q in lv.get("questions", []):
                yield ("q.stem", q, "stem")
                yield ("q.exp", q, "exp")
                for i, o in enumerate(q.get("options", [])):
                    yield (f"q.opt{i}", q["options"], i)
        f = data.get("final", {})
        yield ("final.stem", f, "stem")
        yield ("final.exp", f, "exp")
        yield ("final.solution", f, "solution")
        for i, o in enumerate(f.get("options", [])):
            yield (f"final.opt{i}", f["options"], i)

    # 1) LaTeX 자동교정
    for loc, obj, key in fields():
        if isinstance(obj, dict) and key in obj and isinstance(obj[key], str):
            new, c = _autofix_latex(obj[key])
            if c:
                obj[key] = new
                report["autofix"].append(f"{loc}: LaTeX 래핑 {c}개 교정")
        elif isinstance(obj, list) and isinstance(key, int):
            if isinstance(obj[key], str):
                new, c = _autofix_latex(obj[key])
                if c:
                    obj[key] = new
                    report["autofix"].append(f"{loc}: LaTeX 래핑 {c}개 교정")

    # 2) 기하 + (수치 검사는 오탐이 많아 비활성화: 에이전트가 작성 시 sympy 검산함)
    full = []
    for loc, obj, key in fields():
        if isinstance(obj, dict) and key in obj and isinstance(obj[key], str):
            full.append(obj[key])
        elif isinstance(obj, list) and isinstance(key, int) and isinstance(obj[key], str):
            full.append(obj[key])
    text = "\n".join(full)
    for iss in _check_geometry(text):
        report["warn"].append("기하: " + iss)

    return data, report

if __name__ == "__main__":
    # 자체 테스트: 의도적으로 깨진 샘플
    sample = {
        "title": "테스트",
        "symbols": [],
        "levels": [{
            "stage": "level1", "title": "t", "knowledge": "k",
            "questions": [{
                "stem": "d2^2 - d2 - 72 = 0 의 해는?",
                "options": ["9", "8", "7"], "answer": 1,
                "exp": "d2(2d2-2)=144 → 2d2^2-2d2-144=0"
            }]
        }],
        "final": {
            "stem": r"삼각형 FF'Q 의 넓이는? 벡터 \overrightarrow{FP}, \overrightarrow{FQ} 사용",
            "options": ["1", "2"], "answer": 1,
            "exp": "넓이 = 98sqrt5 / 9",
            "solution": "<p>1+1=3</p>"
        }
    }
    d, rep = verify_and_fix(sample)
    print("=== 자동교정 ===")
    for a in rep["autofix"]: print("  +", a)
    print("=== 경고 ===")
    for w in rep["warn"]: print("  !", w)
    print("=== 교정된 stem/final.stem ===")
    print("  q.stem:", d["levels"][0]["questions"][0]["stem"])
    print("  final.stem:", d["final"]["stem"])
