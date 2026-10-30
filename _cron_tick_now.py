import os, hashlib, json, glob, time

base = r"C:\Users\min\Desktop\mathedu"

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

# list real files
print("=== DOTFILES IN BASE ===")
for n in sorted(os.listdir(base)):
    if n.startswith("."):
        print("  ", repr(n), os.path.getsize(os.path.join(base, n)))

print("\n=== CACHED vs CURRENT _regen_*.py ===")
cache = {}
try:
    with open(os.path.join(base, ".regen_hash_cache.json")) as f:
        cache = json.load(f)
    print("cache loaded OK with keys:", sorted(cache.keys()))
except Exception as e:
    print("cache load error:", repr(e))

all_changed = False
for slug, entry in sorted(cache.items()):
    fn = "_regen_%s.py" % slug
    p = os.path.join(base, fn)
    if not os.path.exists(p):
        print("  %s: MISSING on disk" % slug)
        all_changed = True
        continue
    st = os.stat(p)
    cur_hash = sha256_file(p)
    cur_mtime = st.st_mtime
    cached_hash = entry.get("hash", "")
    cached_mtime = entry.get("mtime", 0)
    hash_ok = (cur_hash == cached_hash)
    mtime_ok = (cur_mtime == cached_mtime)
    status = "OK"
    if not hash_ok or not mtime_ok:
        status = "CHANGED"
        all_changed = True
    print("  %s: hash_ok=%s mtime_ok=%s -> %s" % (slug, hash_ok, mtime_ok, status))
    if not hash_ok:
        print("      cached_hash=%s cur_hash=%s" % (cached_hash[:16], cur_hash[:16]))
    if not mtime_ok:
        print("      cached_mtime=%s cur_mtime=%s" % (cached_mtime, cur_mtime))

print("\n=== ALL _regen_*.py ON DISK (with mtime) ===")
for p in sorted(glob.glob(os.path.join(base, "_regen_*.py"))):
    st = os.stat(p)
    rel = os.path.basename(p)
    h = sha256_file(p)
    print("  %s  mtime=%.4f  size=%d" % (rel, st.st_mtime, st.st_size))

print("\n=== WATCHDOG PENDING ===")
try:
    with open(os.path.join(base, ".watchdog_pending.json")) as f:
        pend = json.load(f)
    print("  pending=", json.dumps(pend, ensure_ascii=False)[:500])
except Exception as e:
    print("  err", repr(e))

print("\n=== BOARD HTML RECENT (last 60s) ===")
cutoff = time.time() - 60
found = False
for p in sorted(glob.glob(os.path.join(base, "board", "*.html"))):
    st = os.stat(p)
    if st.st_mtime > cutoff:
        print("  %s  mtime=%.4f  size=%d" % (os.path.basename(p), st.st_mtime, st.st_size))
        found = True
if not found:
    print("  (none in last 60s)")

print("\n=== OTHER HTML/JASON RECENT (last 300s) ===")
cutoff2 = time.time() - 300
found2 = False
for p in sorted(glob.glob(os.path.join(base, "*.html"))) + sorted(glob.glob(os.path.join(base, "*.json"))):
    st = os.stat(p)
    if st.st_mtime > cutoff2:
        print("  %s  mtime=%.4f  size=%d" % (os.path.basename(p), st.st_mtime, st.st_size))
        found2 = True
if not found2:
    print("  (none in last 300s)")

print("\nOVERALL:", "HAS_CHANGES" if all_changed else "NO_CHANGES")
