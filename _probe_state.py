import hashlib, json, os

base = r"C:/Users/min/Desktop/mathedu"
state_path = os.path.join(base, ".regen_cron_state.json")

with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

entries = state.get("entries", {})
print("=== STATE: %s ===" % state_path)
print("exists entries:", sorted(entries.keys()))
for k in sorted(entries.keys()):
    v = entries[k]
    print("  %-16s hash=%s mtime=%s" % (k, v.get("hash",""), v.get("mtime")))
