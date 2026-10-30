import os, json, hashlib

BASE = r"C:\Users\min\Desktop\mathedu"

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def mtime(p):
    return os.stat(p).st_mtime

print("=== _regen_cron_check.py state (_cron_state.json) ===")
cc = json.load(open(os.path.join(BASE, "_cron_state.json"), encoding="utf-8"))
entries_cc = cc.get("entries", {})
regen_files = sorted(f for f in os.listdir(BASE) if f.startswith("_regen_") and f.endswith(".py"))
for f in regen_files:
    slug = f[len("_regen_"):-len(".py")]
    sha = sha256(os.path.join(BASE, f))
    mt = mtime(os.path.join(BASE, f))
    entry = entries_cc.get(slug, {})
    old_sha = entry.get("hash", "")
    old_mt = entry.get("mtime", 0)
    ok = (sha == old_sha) and (mt == old_mt)
    print(f"{f}: hash_same={sha==old_sha} mtime_same={mt==old_mt}  -> {'CHANGED' if not ok else 'ok'}")
    if not ok:
        print(f"    old_hash={old_sha} new_hash={sha}")
        print(f"    old_mtime={old_mt} new_mtime={mt}")

print()
print("=== _regen_cron_runner.py state (.regen_cron_state.json) ===")
rc = json.load(open(os.path.join(BASE, ".regen_cron_state.json"), encoding="utf-8"))
entries_rc = rc.get("entries", {})
EXCLUDED = {"cron_check", "data", "cron_runner"}
for f in regen_files:
    slug = f[len("_regen_"):-len(".py")]
    if slug in EXCLUDED:
        continue
    sha = sha256(os.path.join(BASE, f))
    mt = mtime(os.path.join(BASE, f))
    entry = entries_rc.get(slug, {})
    old_sha = entry.get("hash", "")
    old_mt = entry.get("mtime", 0)
    ok = (sha == old_sha) and (mt == old_mt)
    print(f"{f}: hash_same={sha==old_sha} mtime_same={mt==old_mt}  -> {'CHANGED' if not ok else 'ok'}")
    if not ok:
        print(f"    old_hash={old_sha} new_hash={sha}")
        print(f"    old_mtime={old_mt} new_mtime={mt}")

print()
print("=== board html file mtimes (recent) ===")
for f in ["51908207.html", "a33ab59b.html"]:
    p = os.path.join(BASE, "board", f)
    print(f, os.stat(p).st_mtime, "=>", __import__("datetime").datetime.fromtimestamp(os.stat(p).st_mtime, __import__("datetime").timezone.utc))
