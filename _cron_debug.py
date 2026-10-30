import os, hashlib, json
from pathlib import Path
BASE = Path(__file__).resolve().parent
STATE_FILE = BASE / "._regen_cron_state.json"
HASH_CACHE = BASE / ".regen_hash_cache.json"

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

state = json.load(open(STATE_FILE))
entries = state.get("entries", {})
print("--- 상태 파일 entries ---")
for k, v in entries.items():
    print(f"  {k}: {v}")

regen_files = sorted(BASE.glob("_regen_*.py"))
print("\n--- _regen_*.py 파일 ---")
for sp in regen_files:
    print(f"  {sp.name}")

print("\n--- 체크 로직 ---")
EXCLUDED_SLUGS = {"cron_check"}
new_or_changed = []
for sp in regen_files:
    slug = sp.stem.replace("_regen_", "")
    if slug in EXCLUDED_SLUGS:
        print(f"  {sp.name}: EXCLUDED (cron_check)")
        continue
    sha = sha256(sp)
    mtime = sp.stat().st_mtime
    entry = entries.get(slug, {})
    old_hash = entry.get("hash", "")
    old_mtime = entry.get("mtime", 0)
    reason = ""
    if sha != old_hash:
        reason = f"hash changed"
    elif mtime != old_mtime:
        reason = f"mtime updated"
    print(f"  {sp.name}: slug={slug} sha={sha[:12]} old_hash={old_hash[:12] if old_hash else None} reason='{reason}'")
    if reason:
        new_or_changed.append(slug)
print(f"\nnew_or_changed = {new_or_changed}")
print(f"결과가 있으면 변경 감지, 없으면 SILENT")
