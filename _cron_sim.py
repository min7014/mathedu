import os, json, hashlib
base = r"C:\Users\min\Desktop\mathedu"

print("=== FULL ._regen_cron_state.json ===")
print(open(base + "\\._regen_cron_state.json", encoding="utf-8").read())

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

print("\n=== CURRENT script check (runner logic) ===")
state = json.load(open(base + "\\._regen_cron_state.json", encoding="utf-8"))
entries = state.get("entries", {})
for slug, entry in entries.items():
    script = entry.get("script")
    p = os.path.join(base, script)
    if not os.path.exists(p):
        print(f"{slug}: MISSING script {script}")
        continue
    cs = sha256(p)
    cm = os.stat(p).st_mtime
    old_hash = entry.get("hash", "")
    old_m = entry.get("mtime", 0)
    h_changed = cs != old_hash
    m_changed = cm != old_m
    print(f"{slug}: script={script}")
    print(f"   current sha256={cs}")
    print(f"   state   sha256={old_hash}  match={not h_changed}")
    print(f"   current mtime={cm}  state mtime={old_m}  match={not m_changed}")
    print(f"   -> changed: hash={h_changed}, mtime={m_changed}")
