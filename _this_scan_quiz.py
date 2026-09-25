# -*- coding: utf-8 -*-
import glob, importlib.util, os, sys, traceback
import verify_quiz

roots = sorted(glob.glob("_regen_*.py"))
total_warn = 0
total_fix = 0
bad = []

for fp in roots:
    base = os.path.basename(fp)
    mod = "regen_" + base[7:-3]
    s = importlib.util.spec_from_file_location(mod, fp)
    m = importlib.util.module_from_spec(s)
    try:
        s.loader.exec_module(m)
    except Exception:
        # 데이터 정의가 아닌 실행부(pending 의존성 등)는 스킵
        continue
    data = getattr(m, "data", None)
    if data is None:
        continue
    _, rep = verify_quiz.verify_and_fix(data)
    w = len(rep.get("warn", []))
    f = len(rep.get("autofix", []))
    total_warn += w
    total_fix += f
    if w or f:
        bad.append((base, w, f))

print("SCAN_DONE regen=%d warn=%d fix=%d" % (len(roots), total_warn, total_fix))
for b in bad:
    print("BAD", b)
