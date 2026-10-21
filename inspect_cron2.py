import os, json, glob, time, hashlib

root = r'C:\Users\min\Desktop\mathedu'
now = time.time()
print("NOW epoch:", now, "=", time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(now)))

def read_json(fn):
    p = os.path.join(root, fn)
    if not os.path.exists(p):
        return None, p
    try:
        return json.load(open(p, encoding='utf-8')), p
    except Exception as e:
        return None, (p, repr(e))

print("\n=== dot-prefixed state files ===")
for fn in ['.regen_cron_state.json', '.regen_hash_cache.json', '.regen_build_log.json', '._regen_cron_state.json']:
    d, p = read_json(fn)
    print("---", fn)
    if d is None:
        print("  MISSING/ERR", p)
    else:
        if isinstance(d, dict):
            print("  keys:", list(d.keys())[:20])
            if 'entries' in d:
                for k, v in list(d['entries'].items()):
                    print("   ", k, json.dumps(v)[:200])
            elif 'entries' in d:
                pass
        print("  raw head:", json.dumps(d, ensure_ascii=False)[:400])

print("\n=== _cron_state.json entries ===")
d, p = read_json('_cron_state.json')
if d:
    for k, v in d.get('entries', {}).items():
        print(" ", k, json.dumps(v, ensure_ascii=False)[:300])

print("\n=== _regen_cron_state.json (no dot) ===")
d, p = read_json('_regen_cron_state.json')
print(d, p)

print("\n=== per-slug latest change vs last_build ===")
# gather from _cron_state.json entries
st, _ = read_json('_cron_state.json')
if st:
    entries = st.get('entries', {})
    for slug, e in entries.items():
        script = e.get('script')
        last_build_ts = e.get('last_build_ts')
        mtimes = []
        if script and os.path.exists(os.path.join(root, script)):
            mtimes.append(os.stat(os.path.join(root, script)).st_mtime)
        # board html
        bhtml = os.path.join(root, 'board', slug + '.html')
        if os.path.exists(bhtml):
            mtimes.append(os.stat(bhtml).st_mtime)
        maxm = max(mtimes) if mtimes else None
        flag = "NEW/" if (maxm and last_build_ts and maxm > last_build_ts) else ""
        print(f"  {slug:20s} script={os.path.basename(script) if script else '-':35s} last_build_ts={last_build_ts} max_mtime={maxm} {flag}")

print("\n=== board files with mtime > 1792363749 (after last build) ===")
for f in sorted(os.listdir(os.path.join(root, 'board'))):
    if f.endswith('.html'):
        p = os.path.join(root, 'board', f)
        mt = os.stat(p).st_mtime
        if mt > 1792363749:
            print(f"  {f} mt={mt:.0f} ({time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(mt))})")
