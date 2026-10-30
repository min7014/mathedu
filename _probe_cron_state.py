import hashlib, json, os

base = r"C:/Users/min/Desktop/mathedu"

# Check the actual cron runner state file
state_path = os.path.join(base, "._regen_cron_state.json")
print("=== CRON RUNNER STATE: %s ===" % state_path)
print("exists:", os.path.exists(state_path))
if os.path.exists(state_path):
    with open(state_path, "r", encoding="utf-8") as f:
        state = json.load(f)
    entries = state.get("entries", {})
    print("num entries:", len(entries))
    for k in sorted(entries.keys()):
        v = entries[k]
        print("  %-16s hash=%s mtime=%s last_build=%s" % (k, v.get("hash",""), v.get("mtime"), v.get("last_build")))

# Current _regen_*.py files
regen_files = sorted([f for f in os.listdir(base) if f.startswith("_regen_") and f.endswith(".py")])
print("\n=== CURRENT _regen_*.py FILES ===")
for f in regen_files:
    p = os.path.join(base, f)
    mtime = os.stat(p).st_mtime
    print("  %-40s mtime=%s" % (f, mtime))
