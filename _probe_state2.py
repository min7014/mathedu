import hashlib, json, os

base = r"C:/Users/min/Desktop/mathedu"

# The cron runner references this file
state_path = os.path.join(base, ".regen_cron_state.json")
print("=== STATE: %s ===" % state_path)
print("exists:", os.path.exists(state_path))
if os.path.exists(state_path):
    with open(state_path, "r", encoding="utf-8") as f:
        state = json.load(f)
    entries = state.get("entries", {})
    print("num entries:", len(entries))
    for k in sorted(entries.keys()):
        v = entries[k]
        print("  %-16s hash=%s mtime=%s" % (k, v.get("hash",""), v.get("mtime")))

# Hash cache
hash_cache_path = os.path.join(base, ".regen_hash_cache.json")
print("\n=== HASH CACHE: %s ===" % hash_cache_path)
if os.path.exists(hash_cache_path):
    with open(hash_cache_path, "r", encoding="utf-8") as f:
        hc = json.load(f)
    print("keys:", sorted(hc.keys()))
    for k in sorted(hc.keys()):
        print("  %-16s mtime=%s" % (k, hc[k].get("mtime")))

# Build log
build_log_path = os.path.join(base, ".regen_build_log.json")
print("\n=== BUILD LOG: %s ===" % build_log_path)
if os.path.exists(build_log_path):
    with open(build_log_path, "r", encoding="utf-8") as f:
        bl = json.load(f)
    print("num builds:", len(bl.get("builds", [])))
    for b in bl.get("builds", []):
        print("  %-16s %s exit=%s size=%s" % (b.get("slug"), b.get("timestamp"), b.get("exit_code"), b.get("output_size")))
