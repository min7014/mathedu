# -*- coding: utf-8 -*-
import os, json, glob, time, datetime

base = "C:/Users/min/Desktop/mathedu"
thr = 1793240333.0

print("now_epoch", round(time.time(), 1))
print("last_build_epoch 1793240333")

def utc(m):
    return datetime.datetime.fromtimestamp(m, datetime.timezone.utc).isoformat()

print("BOARD files modified after last_build:")
n = 0
for p in sorted(glob.glob(base + "/board/*.html")):
    m = os.stat(p).st_mtime
    if m > thr:
        n += 1
        print(" NEW", os.path.basename(p), utc(m))
print("BOARD_NEW_COUNT", n)

print("Other files modified after last_build:")
n2 = 0
for p in sorted(glob.glob(base + "/*.html") + glob.glob(base + "/*.json") + glob.glob(base + "/*.xml")):
    m = os.stat(p).st_mtime
    if m > thr:
        n2 += 1
        print(" NEW", os.path.basename(p), utc(m))
print("POST_BUILD_FILES", n2)

# All regen main scripts with mtimes
print("REGEN_MAIN mtimes:")
for f in sorted(glob.glob(base + "/_regen_48d0d98f.py") + glob.glob(base + "/_regen_51908207.py") + glob.glob(base + "/_regen_a33ab59b.py")):
    print(os.path.basename(f), "mtime", round(os.stat(f).st_mtime, 1), utc(os.stat(f).st_mtime))
