# -*- coding: utf-8 -*-
import os, json, hashlib, datetime

base = r'C:\Users\min\Desktop\mathedu'

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

print("=== Current _regen_*.py ===")
regen_files = sorted([f for f in os.listdir(base) if f.startswith('_regen_') and f.endswith('.py')])
for fn in regen_files:
    p = os.path.join(base, fn)
    st = os.stat(p)
    print(f"{fn} | mtime={datetime.datetime.fromtimestamp(st.st_mtime).isoformat()} | size={st.st_size} | sha={sha256(p)[:16]}...")

print("\n=== _cron_state.json entries ===")
p = os.path.join(base, '_cron_state.json')
if os.path.exists(p):
    d = json.load(open(p, encoding='utf-8'))
    print(json.dumps(d, indent=2, ensure_ascii=False)[:4000])

print("\n=== ._regen_cron_state.json ===")
p = os.path.join(base, '._regen_cron_state.json')
if os.path.exists(p):
    print(open(p, encoding='utf-8').read())

print("\n=== .regen_hash_cache.json ===")
p = os.path.join(base, '.regen_hash_cache.json')
if os.path.exists(p):
    print(open(p, encoding='utf-8').read())
