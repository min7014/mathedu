# -*- coding: utf-8 -*-
import os, json, datetime

base = r'C:\Users\min\Desktop\mathedu'

print("=== board/pending ===")
pending = os.path.join(base, 'board', 'pending')
if os.path.isdir(pending):
    for fn in sorted(os.listdir(pending)):
        p = os.path.join(pending, fn)
        st = os.stat(p)
        print(f"{fn} | size={st.st_size} | mtime={datetime.datetime.fromtimestamp(st.st_mtime).isoformat()}")
else:
    print("pending dir not found")

print("\n=== board root files (recent) ===")
board = os.path.join(base, 'board')
for fn in sorted(os.listdir(board)):
    p = os.path.join(board, fn)
    if os.path.isfile(p):
        st = os.stat(p)
        if st.st_mtime > 1791000000:
            print(f"{fn} | mtime={datetime.datetime.fromtimestamp(st.st_mtime).isoformat()}")

print("\n=== done.json ===")
p = os.path.join(board, 'done.json')
if os.path.exists(p):
    print(open(p, encoding='utf-8').read()[:2000])

print("\n=== git status (if any) ===")
import subprocess
r = subprocess.run(['git', '-C', base, 'status', '--porcelain'], capture_output=True, text=True)
print("stdout:", r.stdout[:2000])
print("stderr:", r.stderr[:500])
