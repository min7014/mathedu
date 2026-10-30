# -*- coding: utf-8 -*-
import os, json, hashlib
from pathlib import Path

BASE = Path(r"C:/Users/min/Desktop/mathedu")
STATE = BASE / "._regen_cron_state.json"   # 실제 상태 파일 (cron_runner가 사용)

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

for sp in sorted(BASE.glob("_regen_*.py")):
    slug = sp.stem.replace("_regen_", "")
    if slug in EXCLUDED:
        continue
    cur_hash = sha256(sp)
    cm = entries.get(slug, {})
    same = (cur_hash == cm.get("hash")) and (sp.stat().st_mtime == cm.get("mtime", 0))
    if not same:
        changed.append(slug)
    print(f"{slug:<14} hash_same={same}  cur={cur_hash[:12]}  prev={cm.get('hash','')[:12]}  mtime_same={(sp.stat().st_mtime==cm.get('mtime',0))}")

print("\n== CHANGED (against real state) ==")
print(changed if changed else "NONE")

# board files: check if any board html is NOT tracked in state entries
for bp in sorted((BASE/"board").glob("*.html")):
    slug = bp.stem
    if slug not in entries:
        pass  # no per-board tracking; skip
print("=== board files: no per-board tracking in state (by design) ===")
