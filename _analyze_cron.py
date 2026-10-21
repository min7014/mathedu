# -*- coding: utf-8 -*-
import os, hashlib, json, glob, datetime

BASE = r"C:\Users\min\Desktop\mathedu"

def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

print("=== _regen_*.py 현재 + 상태 비교 ===")
scripts = sorted(glob.glob(BASE + r"\_regen_*.py"))
for sp in scripts:
    fn = os.path.basename(sp)
    slug = fn.replace("_regen_", "")
    st = os.stat(sp)
    print(f"  {fn:24s} mtime={st.st_mtime:.3f} size={st.st_size} sha={sha256(sp)[:12]}")

print("\n=== 상태 파일들 ===")
for sf in [".regen_cron_state.json", "._regen_cron_state.json", "_cron_state.json"]:
    p = os.path.join(BASE, sf)
    if os.path.exists(p):
        try:
            d = json.load(open(p, encoding="utf-8"))
            print(f"  {sf}: entries={list(d.get('entries',{}).keys())} updated_at={d.get('updated_at')}")
        except Exception as e:
            print(f"  {sf}: ERR {e}")

print("\n=== board HTML 파일 ===")
htmls = sorted(glob.glob(BASE + r"\board\*.html"), key=lambda p: os.stat(p).st_mtime)
for h in htmls:
    st = os.stat(h)
    print(f"  {os.path.basename(h)} mtime={st.st_mtime:.3f} size={st.st_size}")
if htmls:
    print(f"  NEWEST: {os.path.basename(htmls[-1])} mtime={os.stat(htmls[-1]).st_mtime:.3f}")
