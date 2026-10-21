# -*- coding: utf-8 -*-
import os, json, hashlib, glob, datetime

BASE = r"C:\Users\min\Desktop\mathedu"

def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)

def basename(p):
    return os.path.basename(p)

# 1) current _regen scripts
cur = {}
for f in sorted(glob.glob(BASE + r"\_regen_*.py")):
    st = os.stat(f)
    cur[os.path.basename(f)] = {'mtime': st.st_mtime, 'size': st.st_size, 'sha256': sha256(f)}

print("### 1) 현재 _regen_*.py ###")
for k in sorted(cur):
    print(f"  {k:28s} mtime={cur[k]['mtime']:.3f} size={cur[k]['size']} sha={cur[k]['sha256'][:12]}")

# 2) active cron states
states = []
for sf in [".regen_cron_state.json", "._regen_cron_state.json", "_cron_state.json"]:
    p = os.path.join(BASE, sf)
    if os.path.exists(p):
        try:
            st = load(p)
            states.append((sf, st))
            print(f"\n### 2) {sf} (updated_at={st.get('updated_at')}) entries={list(st.get('entries',{}).keys())} ###")
        except Exception as e:
            print(f"  ERR {sf}: {e}")

# 3) comparison
for sf, st in states:
    print(f"\n--- compare {sf} ---")
    for slug, e in sorted(st.get('entries', {}).items()):
        fn = os.path.join(BASE, "_regen_" + slug + ".py")
        if os.path.exists(fn):
            c = cur[basename(fn)]
            h_ok = c['sha256'] == e.get('hash')
            m_ok = abs(c['mtime'] - e.get('mtime', 0)) < 1.0
            s_ok = c['size'] == e.get('output_size', 0)
            print(f"  {slug:16s} hash_ok={h_ok} mtime_ok={m_ok} size_ok={s_ok}")
        else:
            print(f"  {slug:16s} (script MISSING)")

# 4) newest board html mtime vs last build
print("\n### 4) board html mtimes ###")
htmls = sorted(glob.glob(BASE + r"\board\*.html"), key=lambda p: os.stat(p).st_mtime)
if htmls:
    st = os.stat(htmls[-1])
    print(f"  newest: {os.path.basename(htmls[-1])} mtime={st.st_mtime:.3f} ({datetime.datetime.utcfromtimestamp(st.st_mtime).isoformat()}Z) size={st.st_size}")

# 5) index_site.json vs index.json (compare_index concern)
print("\n### 5) index_site.json vs index.json ###")
for f in ["board/index_site.json", "board/index.json"]:
    p = os.path.join(BASE, f)
    if os.path.exists(p):
        d = load(p)
        print(f"  {f}: count={len(d)}")
        slugs = [e.get('slug') for e in d]
        print(f"    slugs(sample): {slugs[:8]}")
site = load(BASE + r"\board\index_site.json")
local = load(BASE + r"\board\index.json")
site_slugs = {e['slug'] for e in site}
local_slugs = {e['slug'] for e in local}
print("  only in site:", sorted(site_slugs - local_slugs))
print("  only in local:", sorted(local_slugs - site_slugs))

# 6) build log latest
print("\n### 6) build log latest 3 ###")
bl = load(BASE + r"\.regen_build_log.json")
for e in bl.get('logs', [])[-3:]:
    print(f"  {e.get('slug'):16s} {e.get('timestamp')} {e.get('status')} stdout[:50]={str(e.get('stdout'))[:50]!r}")
