# -*- coding: utf-8 -*-
import os, glob, json, hashlib, datetime

base = r'C:\Users\min\Desktop\mathedu'
print("=== state files ===")
for f in ['_cron_state.json', '._regen_cron_state.json', '.regen_hash_cache.json', '.regen_build_log.json', '_regen_data.json']:
    p = os.path.join(base, f)
    if os.path.exists(p):
        print(f"{f} exists=True size={os.path.getsize(p)}")
    else:
        print(f"{f} exists=False")

print("\n=== board dir ===")
board = os.path.join(base, 'board')
for root, dirs, files in os.walk(board):
    for fn in sorted(files):
        p = os.path.join(root, fn)
        st = os.stat(p)
        print(f"{p} | size={st.st_size} | mtime={datetime.datetime.fromtimestamp(st.st_mtime).isoformat()}")

print("\n=== _cron_state.json ===")
p = os.path.join(base, '_cron_state.json')
if os.path.exists(p):
    print(open(p, encoding='utf-8').read())

print("\n=== ._regen_cron_state.json ===")
p = os.path.join(base, '._regen_cron_state.json')
if os.path.exists(p):
    print(open(p, encoding='utf-8').read())

print("\n=== .regen_hash_cache.json ===")
p = os.path.join(base, '.regen_hash_cache.json')
if os.path.exists(p):
    print(open(p, encoding='utf-8').read())

print("\n=== .regen_build_log.json (head) ===")
p = os.path.join(base, '.regen_build_log.json')
if os.path.exists(p):
    d = json.load(open(p, encoding='utf-8'))
    print(json.dumps(d, indent=2, ensure_ascii=False)[:3000])
