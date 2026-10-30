# -*- coding: utf-8 -*-
import os, json, hashlib

mathedu = "C:/Users/min/Desktop/mathedu"

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

current = {}
for f in sorted(os.listdir(mathedu)):
    if f.startswith("_regen_") and f.endswith(".py"):
        fp = os.path.join(mathedu, f)
        slug = f.replace("_regen_", "").replace(".py", "")
        current[slug] = {
            "script": f,
            "hash": sha256_file(fp),
            "mtime": os.path.getmtime(fp),
        }

with open(os.path.join(mathedu, "_cron_state.json"), encoding="utf-8") as f:
    saved = json.load(f)
saved_entries = saved.get("entries", {})

print("=== SCRIPT COMPARISON ===")
new_scripts = []
changed_scripts = []
for slug in sorted(current):
    v = current[slug]
    se = saved_entries.get(slug)
    if se is None:
        new_scripts.append(slug)
        print(f"{slug}: NEW (not in state)")
    else:
        same = (v["hash"] == se.get("hash")) and (v["mtime"] == se.get("mtime", 0))
        if not same:
            changed_scripts.append(slug)
            print(f"{slug}: CHANGED  cur={v['hash'][:12]}... cur_mtime={v['mtime']} | prev_hash={se.get('hash','')[:12]}... prev_mtime={se.get('mtime',0)}")
        else:
            print(f"{slug}: OK (hash+mtime match)")

print(f"\nnew_scripts={new_scripts}")
print(f"changed_scripts={changed_scripts}")
print(f"to_build={list(set(new_scripts + changed_scripts))}")
