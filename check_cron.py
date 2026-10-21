# -*- coding: utf-8 -*-
import os, glob, time, subprocess

base = r"C:\Users\min\Desktop\mathedu"

def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)

print("=== _regen_*.py files ===")
for f in sorted(glob.glob(os.path.join(base, "_regen_*.py"))):
    st = os.stat(f)
    mt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(st.st_mtime))
    print(f"{mt}  {st.st_size:>8}  {f}")

print("\n=== git status --porcelain ===")
r = run(["git","-C",base,"status","--porcelain"])
print(r.stdout or "(clean)")
if r.stderr:
    print("stderr:", r.stderr[:2000])

print("\n=== git log --oneline -5 ===")
r = run(["git","-C",base,"log","--oneline","-5"])
print(r.stdout)

print("\n=== boards dir listing ===")
bdir = os.path.join(base, "board")
if os.path.isdir(bdir):
    for f in sorted(os.listdir(bdir)):
        st = os.stat(os.path.join(bdir,f))
        print(f"{time.strftime('%m-%d %H:%M', time.localtime(st.st_mtime))}  {st.st_size}  {f}")

print("\n=== grep for 'new_post' or 'create' in _regen files ===")
for f in sorted(glob.glob(os.path.join(base, "_regen_*.py"))):
    try:
        txt = open(f, encoding='utf-8').read()
    except Exception as e:
        print(f, "read err", e); continue
    lines = [l for l in txt.splitlines() if 'new_post' in l or 'create' in l or 'update' in l]
    if lines:
        print(f"--- {f} ({len(lines)} hits) ---")
        for l in lines[:6]:
            print("   ", l.strip()[:120])
