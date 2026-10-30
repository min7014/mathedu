import os, sys, json, hashlib, time, subprocess
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(r"C:\Users\min\Desktop\mathedu")
STATE_FILE = BASE / "_cron_state.json"
HASH_CACHE = BASE / ".regen_hash_cache.json"
PENDING_DIR = BASE / "board" / "pending"
WATCHDOG_STATE = BASE / ".watchdog_pending.json"

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

def check_pending():
    """pending 디렉토리 새 파일 확인"""
    if not PENDING_DIR.exists():
        return []
    watchdog_state = load_json(WATCHDOG_STATE)
    new_files = []
    for f in PENDING_DIR.iterdir():
        if f.name.startswith('.'):
            continue
        fh = sha256(f)
        key = f.name
        if key not in watchdog_state or watchdog_state[key].get("hash") != fh:
            new_files.append({
                "path": str(f), "name": f.name, "hash": fh,
                "is_image": f.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.bmp'],
                "is_json": f.suffix.lower() == '.json'
            })
            watchdog_state[key] = {"hash": fh, "detected_at": datetime.now(timezone.utc).isoformat()}
    save_json(WATCHDOG_STATE, watchdog_state)
    return new_files

def trigger_quiz_builder():
    """quiz-builder 크론잡 수동 실행 시도"""
    try:
        result = subprocess.run(
            ["curl", "-s", "-X", "POST",
             "http://127.0.0.1:5000/api/cron/jobs/a10910600cae/fire"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            return True, result.stdout[:200]
    except Exception:
        pass
    return False, "API 호출 실패"

def main() -> int:
    now = time.time()
    state = load_json(STATE_FILE)
    entries = state.setdefault("entries", {})
    hash_cache = load_json(HASH_CACHE)
    
    # 1. _regen_*.py 변경 확인
    regen_files = sorted(BASE.glob("_regen_*.py"))
    new_or_changed = []
    touched = set()

    for script_path in regen_files:
        slug = script_path.stem.replace("_regen_", "")
        sha = sha256(script_path)
        mtime = script_path.stat().st_mtime

        entry = entries.get(slug, {})
        old_hash = entry.get("hash", "")
        old_mtime = entry.get("mtime", 0)
        cache_entry = hash_cache.get(slug, {})
        cache_hash = cache_entry.get("hash", "")

        reason = ""
        if sha != old_hash:
            reason = "hash changed"
        elif mtime != old_mtime:
            reason = "mtime updated"
        elif cache_hash != sha:
            reason = "hash cache drift"

        if reason:
            new_or_changed.append({"slug": slug, "path": str(script_path), "reason": reason})
            entries[slug] = {"script": script_path.name, "hash": sha, "mtime": mtime, "last_build": None, "last_build_ts": None, "output_size": 0}
            touched.add(slug)

    # 2. 변경 없으면 pending 확인 (워치독 역할)
    pending_detected = []
    if not new_or_changed:
        pending_detected = check_pending()
    
    # 3. 아무 것도 없으면 [SILENT]
    if not new_or_changed and not pending_detected:
        print("[SILENT]")
        return 0
    
    # 4. 결과 출력
    output_lines = []
    
    if new_or_changed:
        output_lines.append(f"변경 감지됨: {len(new_or_changed)}건")
        for item in new_or_changed:
            output_lines.append(f"  - {item['slug']}: {item['reason']}")
    
    if pending_detected:
        output_lines.append(f"새 문제 감지: {len(pending_detected)}건")
        for item in pending_detected:
            kind = '이미지' if item['is_image'] else ('JSON' if item['is_json'] else '기타')
            output_lines.append(f"  - {item['name']} ({kind})")
        
        success, msg = trigger_quiz_builder()
        if success:
            output_lines.append(f"빌드 트리거 성공")
        else:
            output_lines.append(f"빌드 트리거 실패 (quiz-builder가 곧 자동 처리)")
    
    state["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(now))
    save_json(STATE_FILE, state)
    
    hc_new = {}
    for sp in regen_files:
        s = sp.stem.replace("_regen_", "")
        hc_new[s] = {"hash": sha256(sp), "mtime": sp.stat().st_mtime, "slug": s}
    save_json(HASH_CACHE, hc_new)
    
    print("\n".join(output_lines))
    return 0

if __name__ == "__main__":
    sys.exit(main())
