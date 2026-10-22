import os, json, hashlib

mathedu = "C:/Users/min/Desktop/mathedu"

def compute_hash(fp):
    h = hashlib.sha256()
    with open(fp, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

# Read saved state
with open(os.path.join(mathedu, "_cron_state.json"), encoding="utf-8") as f:
    saved = json.load(f)
saved_entries = saved.get("entries", {})

# Current scripts on disk
current = {}
for fn in sorted(os.listdir(mathedu)):
    if fn.startswith("_regen_") and fn.endswith(".py"):
        fp = os.path.join(mathedu, fn)
        slug = fn.replace("_regen_", "").replace(".py", "")
        current[slug] = {
            "script": fn,
            "hash": compute_hash(fp),
            "mtime": os.path.getmtime(fp),
        }

print("=== Disk scripts vs saved state ===")
for slug in sorted(current):
    c = current[slug]
    s = saved_entries.get(slug)
    if s is None:
        print(f"{slug}: NEW on disk (not in state)")
    else:
        match = (c["hash"] == s["hash"]) and (c["mtime"] == s["mtime"])
        flag = "MATCH" if match else "DIFFER"
        print(f"{slug}: {flag}  (disk mtime={c['mtime']:.0f}, saved mtime={s.get('mtime', 'NA')})")
        if not match:
            print(f"   disk hash={c['hash']}")
            print(f"   saved hash={s.get('hash', 'NA')}")

# Also list scripts in state but not on disk
for slug in sorted(saved_entries):
    if slug not in current:
        print(f"{slug}: in state but NOT on disk")

print("\n=== Verdict ===")
new_or_changed = [s for s in current if saved_entries.get(s) is None
                  or (current[s]["hash"] != saved_entries[s]["hash"]
                      or current[s]["mtime"] != saved_entries[s]["mtime"])]
if new_or_changed:
    print(f"BUILD NEEDED: {new_or_changed}")
else:
    print("NO CHANGES — write [SILENT]")
