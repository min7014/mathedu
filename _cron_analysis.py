import os, json, hashlib

BASE = "C:/Users/min/Desktop/mathedu"

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

# Runner's state file
runner_state_path = os.path.join(BASE, "._regen_cron_state.json")
try:
    with open(runner_state_path, encoding="utf-8") as f:
        runner_state = json.load(f)
    runner_entries = runner_state.get("entries", {})
    print("RUNNER STATE (._regen_cron_state.json):")
    print("  updated_at =", runner_state.get("updated_at"))
    print("  entries:", sorted(runner_entries.keys()))
except Exception as e:
    print("RUNNER STATE ERROR:", e)
    runner_entries = {}

# Test/dev state
test_state_path = os.path.join(BASE, "_cron_state.json")
try:
    with open(test_state_path, encoding="utf-8") as f:
        test_state = json.load(f)
    test_entries = test_state.get("entries", {})
    print("\nTEST STATE (_cron_state.json):")
    print("  updated_at =", test_state.get("updated_at"))
    print("  entries:", sorted(test_entries.keys()))
except Exception as e:
    print("TEST STATE ERROR:", e)
    test_entries = {}

# Current _regen_*.py files
regen_files = sorted(f for f in os.listdir(BASE) if f.startswith("_regen_") and f.endswith(".py"))
print("\nCURRENT _regen_*.py files:")
print("  count:", len(regen_files))
for fn in regen_files:
    fp = os.path.join(BASE, fn)
    st = os.stat(fp)
    print(f"  {fn}: size={st.st_size} mtime={st.st_mtime:.6f}")

# EXCLUDED slugs per runner
EXCLUDED = {"cron_check", "data", "cron_runner", "check_state"}

print("\n=== COMPARISON vs RUNNER STATE ===")
for fn in sorted(regen_files):
    sl = fn.replace("_regen_", "").replace(".py", "")
    if sl in EXCLUDED:
        print(f"  {sl}: EXCLUDED")
        continue
    fp = os.path.join(BASE, fn)
    h = sha256(fp)
    m = os.path.getmtime(fp)
    entry = runner_entries.get(sl, {})
    e_hash = entry.get("hash", "")
    e_mtime = entry.get("mtime", 0)
    hash_ok = (h == e_hash)
    mtime_ok = (m == e_mtime)
    print(f"  {sl}: disk hash_ok={hash_ok} ({h[:16]}...) mtime_ok={mtime_ok} ({m:.6f})")
    if not (hash_ok and mtime_ok):
        print(f"      state hash={e_hash[:16]}... mtime={e_mtime}")

print("\n=== COMPARISON vs TEST STATE (_cron_state.json) ===")
for fn in sorted(regen_files):
    sl = fn.replace("_regen_", "").replace(".py", "")
    if sl in EXCLUDED:
        continue
    fp = os.path.join(BASE, fn)
    h = sha256(fp)
    m = os.path.getmtime(fp)
    entry = test_entries.get(sl, {})
    e_hash = entry.get("hash", "")
    e_mtime = entry.get("mtime", 0)
    hash_ok = (h == e_hash)
    mtime_ok = (m == e_mtime)
    print(f"  {sl}: disk hash_ok={hash_ok} mtime_ok={mtime_ok}")
