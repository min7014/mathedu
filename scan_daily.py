#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Daily mathedu error scan (cron run)."""
import glob
import importlib.util
import os
import sys

REPO = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, REPO)

import verify_quiz

regens = sorted(glob.glob(os.path.join(REPO, '_regen_*.py')))
total_warn = 0
total_fix = 0
bad = []

for fp in regens:
    fname = os.path.basename(fp)
    mod = 'regen_' + fname[7:-3]
    try:
        s = importlib.util.spec_from_file_location(mod, fp)
        m = importlib.util.module_from_spec(s)
        s.loader.exec_module(m)
    except SystemExit:
        # 모듈이 pre-check에서 조기 종료 (예: pending 게시물 없음) — 정상 스킵
        continue
    except Exception as e:
        print('IMPORT_FAIL', fname, repr(e))
        continue
    data = getattr(m, 'data', None)
    if data is None:
        continue
    _, rep = verify_quiz.verify_and_fix(data)
    w = len(rep.get('warn', []))
    f = len(rep.get('autofix', []))
    total_warn += w
    total_fix += f
    if w or f:
        bad.append((fname, w, f))

print('SCAN_DONE regen=%d warn=%d fix=%d' % (len(regens), total_warn, total_fix))
for b in bad:
    print('BAD', b)
