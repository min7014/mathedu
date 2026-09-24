import os, sys, json, hashlib, time
from pathlib import Path

BASE = Path(__file__).resolve().parent
STATE_FILE = BASE / "_cron_state.json"
HASH_CACHE = BASE / ".regen_hash_cache.json"

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}

def save_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def main() -> int:
    now = time.time()
    state = load_json(STATE_FILE)
    entries = state.setdefault("entries", {})
    hash_cache = load_json(HASH_CACHE)

    # 시작 시점의 스크립트만 기준으로 삼음 (스캔 도중 재생성된 스크립트는 무시)
    regen_files = sorted(BASE.glob("_regen_*.py"))
    before = {p.stem.replace("_regen_", ""): p for p in regen_files}
    new_or_changed = []
    touched = set()

    EXCLUDED_SLUGS = {"cron_check"}

    for script_path in regen_files:
        slug = script_path.stem.replace("_regen_", "")
        if slug in EXCLUDED_SLUGS:
            continue
        sha = sha256(script_path)
        mtime = script_path.stat().st_mtime

        entry = entries.get(slug, {})
        old_hash = entry.get("hash", "")
        old_mtime = entry.get("mtime", 0)

        reason = ""
        if sha != old_hash:
            reason = f"hash changed (old={old_hash[:12]}… new={sha[:12]}…)"
        elif mtime != old_mtime:
            reason = f"mtime updated (old={old_mtime} new={mtime})"

        if reason:
            new_or_changed.append({
                "slug": slug,
                "path": str(script_path),
                "reason": reason,
                "old_hash": old_hash,
                "new_hash": sha,
                "new_mtime": mtime,
            })
            entries[slug] = {
                "script": script_path.name,
                "hash": sha,
                "mtime": mtime,
                "last_build": None,
                "last_build_ts": None,
                "output_size": 0,
            }
            touched.add(slug)

    # 삭제된 스크립트 항목을 state에서 정리
    existing_slugs = {sp.stem.replace("_regen_", "") for sp in regen_files}
    stale = [k for k in entries if k not in existing_slugs]
    builds = state.get("builds", [])
    if stale:
        print(f"정리: 존재하지 않는 스크립트 항목 {len(stale)}개 제거")
        for k in stale:
            del entries[k]
            builds = [b for b in builds if b.get("slug") != k]
    state["builds"] = builds

    if not new_or_changed:
        print("[SILENT]")
        return 0

    print(f"변경 감지됨: {len(new_or_changed)}건")
    for item in new_or_changed:
        print(f"  - {item['slug']}: {item['reason']} (mtime={item['new_mtime']})")

    state["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(now))
    builds = state.get("builds", [])
    for slug in touched:
        e = entries[slug]
        builds.append({
            "slug": slug,
            "script": e["script"],
            "timestamp": e.get("last_build") or time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(now)),
            "mtime": e["mtime"],
            "size": e.get("output_size", 0),
            "hash": e["hash"],
        })
    state["builds"] = builds
    save_json(STATE_FILE, state)
    print("상태 파일 업데이트 완료.")
    print("실제 빌드 스크립트로 진행 필요: python _regen_{slug}.py")
    return 1

if __name__ == "__main__":
    sys.exit(main())
