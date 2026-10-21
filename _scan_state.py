import os, json, hashlib, datetime

root = r"C:\Users\min\Desktop\mathedu"

def mtime_hash(p):
    st = os.stat(p)
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return st.st_mtime, st.st_size, h.hexdigest()

print("=== _regen_*.py current state ===")
scripts = sorted(glob.glob(r"C:\Users\min\Desktop\mathedu\_regen_*.py")) if False else sorted(
    [os.path.join(dp,f) for dp,_,fn in os.walk(root) for f in fn if f.startswith('_regen_') and f.endswith('.py')]
)
for p in scripts:
    m, s, h = mtime_hash(p)
    rel = os.path.relpath(p, root)
    print(f"{rel} | mtime={datetime.datetime.fromtimestamp(m)} | size={s} | hash={h[:12]}")

print()
print("=== state files ===")
for sf in ["._cron_state.json", "._regen_cron_state.json", ".regen_hash_cache.json", ".regen_build_log.json", ".regen_cron_state.json"]:
    p = os.path.join(root, sf)
    if os.path.exists(p):
        st = os.stat(p)
        print(f"\n--- {sf} (mtime={datetime.datetime.fromtimestamp(st.st_mtime)}) ---")
        with open(p, encoding='utf-8') as f:
            data = json.load(f)
        print(json.dumps(data, ensure_ascii=False, indent=1)[:3000])
