# -*- coding: utf-8 -*-
import os, json, hashlib
from pathlib import Path

BASE = Path(r"C:/Users/min/Desktop/mathedu")
STATE = BASE / ".regen_cron_state.json"

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

state = json.loads(STATE.read_text(encoding="utf-8"))
entries = state.get("entries", {})
EXCLUDED = {"cron_check", "data", "cron_runner", "check_state"}

changed = []
new_board = []
missing = []

for sp in sorted(BASE.glob("_regen_*.py")):
    slug = sp.stem.replace("_regen_", "")
    if slug in EXCLUDED:
        continue
    cur_hash = sha256(sp)
    cm = entries.get(slug, {})
    same = (cur_hash == cm.get("hash")) and (sp.stat().st_mtime == cm.get("mtime", 0))
    if not same:
        changed.append(slug)
    # also print
    print(f"{slug:<14} hash_same={same}  cur={cur_hash[:12]}  prev={cm.get('hash','')[:12]}  mtime_same={(sp.stat().st_mtime==cm.get('mtime',0))}")

print("\n== CHANGED SCRIPTS ==")
print(changed if changed else "NONE")

# board files new vs state
for bp in sorted((BASE/"board").glob("*.html")):
    slug = bp.stem
    if slug not in entries:
        new_board.append(slug)
print("\n== NEW BOARD FILES ==")
print(new_board if new_board else "NONE")

print("\n== SUMMARY ==")
if changed or new_board:
    print(f"WORK: scripts_changed={changed} new_posts={new_board}")
else:
    print("SILENT: nothing to build")
