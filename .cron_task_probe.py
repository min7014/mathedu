# -*- coding: utf-8 -*-
import os, json, hashlib
from pathlib import Path

BASE = Path("C:/Users/min/Desktop/mathedu")

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

state = json.loads((BASE / ".regen_cron_state.json").read_text(encoding="utf-8"))
entries = state.get("entries", {})

# tracked slugs: scripts that exist AND are not excluded
EXCLUDED = {"cron_check", "data", "cron_runner", "check_state"}
scripts = {}
for sp in sorted(BASE.glob("_regen_*.py")):
    slug = sp.stem.replace("_regen_", "")
    if slug in EXCLUDED:
        continue
    scripts[slug] = {
        "hash": sha256(sp),
        "mtime": sp.stat().st_mtime,
        "in_state": slug in entries,
    }

# board files
board_files = {}
for bp in sorted((BASE / "board").glob("*.html")):
    slug = bp.stem
    board_files[slug] = {
        "size": bp.stat().st_size,
        "mtime": bp.stat().st_mtime,
    }

print("=== SCRIPT HASHES ===")
for slug, info in sorted(scripts.items()):
    st = entries.get(slug, {})
    same = (info["hash"] == st.get("hash")) and (info["mtime"] == st.get("mtime", 0))
    print(f"{slug}: hash_same={same} in_state={info['in_state']} "
          f"cur_hash={info['hash'][:12]} prev_hash={st.get('hash','')[:12] if st else 'N/A'} "
          f"cur_mtime={info['mtime']} prev_mtime={st.get('mtime',0)}")

print("\n=== BOARD FILES ===")
for slug, info in sorted(board_files.items()):
    st = entries.get(slug, {})
    print(f"{slug}: size={info['size']} mtime={info['mtime']} in_state={slug in entries} "
          f"last_build={st.get('last_build')}")

print("\n=== SUMMARY ===")
for slug, info in sorted(scripts.items()):
    st = entries.get(slug, {})
    changed = (info["hash"] != st.get("hash")) or (info["mtime"] != st.get("mtime", 0))
    if changed:
        print(f"NEED BUILD: script {slug} changed")
for slug, info in sorted(board_files.items()):
    if slug not in entries:
        print(f"NEED BUILD: new post {slug}")
