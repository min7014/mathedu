import os, json, hashlib
from pathlib import Path

BASE = Path(r"C:\Users\min\Desktop\mathedu")
STATE_FILE = BASE / "._regen_cron_state.json"
HASH_CACHE = BASE / ".regen_hash_cache.json"
BUILD_LOG = BASE / ".regen_build_log.json"

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
entries = state.setdefault("entries", {})
regen_files = sorted(BASE.glob("_regen_*.py"))
EXCLUDED_SLUGS = {"cron_check", "data", "cron_runner", "check_state"}

new_or_changed = []
touched = set()

for script_path in regen_files:
    slug = script_path.stem.replace("_regen_", "")
    if slug in EXCLUDED_SLUGS:
        continue
    sha = sha256(script_path)
    mtime = script_path.stat().st_mtime
    entry = entries.get(slug, {})
    old_hash = entry.get("hash", "")
    reason = ""
    if sha != old_hash:
        reason = "hash changed"
    elif mtime != entry.get("mtime", 0):
        reason = "mtime updated"
    if reason:
        new_or_changed.append(slug)
        touched.add(slug)
        print(f"[cron] 변경 감지: {slug} ({reason})")
    else:
        print(f"[cron] 변경 없음: {slug}")

if not new_or_changed:
    print("\n[cron] 변경 없음. SILENT.")
else:
    print(f"\n[cron] 변경 {len(new_or_changed)}건 → 빌드 진행.")
