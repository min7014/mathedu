import os, sys, json, hashlib, time
from pathlib import Path
from subprocess import run, PIPE

BASE = Path(os.environ.get("MAThedu_PATH", "C:/Users/min/Desktop/mathedu"))
if not BASE.exists():
    BASE = Path("C:/Users/min/Desktop/mathedu")

STATE_FILE = BASE / "._regen_cron_state.json"
HASH_CACHE = BASE / ".regen_hash_cache.json"
BUILD_LOG = BASE / ".regen_build_log.json"

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

now = time.time()
state = load_json(STATE_FILE)
entries = state.setdefault("entries", {})
hash_cache = load_json(HASH_CACHE)
build_log = load_json(BUILD_LOG)

regen_files = sorted(BASE.glob("_regen_*.py"))
print(f"[cron] 현재 스크립트: {len(regen_files)}개")

EXCLUDED_SLUGS = {"cron_check", "data", "cron_runner"}

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
        reason = f"hash changed"
    elif mtime != entry.get("mtime", 0):
        reason = f"mtime updated"

    if reason:
        new_or_changed.append({
            "slug": slug,
            "path": str(script_path),
            "reason": reason,
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
        print(f"[cron] 변경 감지: {slug} ({reason})")
    else:
        print(f"[cron] 변경 없음: {slug}")

# 삭제 정리
existing_slugs = {sp.stem.replace("_regen_", "") for sp in regen_files}
stale = [k for k in entries if k not in existing_slugs]
for k in stale:
    del entries[k]
    print(f"[cron] 정리: {k} (삭제됨)")

if not new_or_changed:
    print("[SILENT]")
    save_json(STATE_FILE, state)
    sys.exit(0)

print(f"\n[cron] 총 {len(new_or_changed)}건 변경됨. 빌드 진행.")

state["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(now))
state["entries"] = entries
state["builds"] = state.get("builds", [])

for item in new_or_changed:
    slug = item["slug"]
    script_path = Path(item["path"])
    print(f"\n[cron] === 빌드 시작: {slug} ===")

    result = run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        timeout=300,
        cwd=str(BASE)
    )

    now_str = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(now))
    status = "success" if result.returncode == 0 else "failure"
    log_entry = {
        "slug": slug,
        "script": script_path.name,
        "timestamp": now_str,
        "status": status,
        "exit_code": result.returncode,
        "stdout": result.stdout[-2000:] if result.stdout else "",
        "stderr": result.stderr[-2000:] if result.stderr else "",
    }
    build_log.setdefault("logs", []).insert(0, log_entry)
    # 로그 50개까지만 유지
    if len(build_log["logs"]) > 50:
        build_log["logs"] = build_log["logs"][:50]

    if result.returncode == 0:
        print(f"[cron] 빌드 성공: {slug}")
        entries[slug]["last_build"] = now_str
        entries[slug]["last_build_ts"] = now
        if "output_size" not in entries[slug] or entries[slug].get("output_size", 0) == 0:
            # 생성된 파일 크기 추정: 빌드 로그에서 힌트 얻기
            pass
    else:
        print(f"[cron] 빌드 실패: {slug} (종료코드 {result.returncode})")
        if result.stderr:
            print(f"[cron] stderr: {result.stderr[:500]}")
        if result.stdout:
            print(f"[cron] stdout: {result.stdout[:500]}")

    state["builds"].append({
        "slug": slug,
        "script": script_path.name,
        "timestamp": now_str,
        "mtime": item["new_mtime"],
        "status": status,
        "size": entries[slug].get("output_size", 0),
        "hash": sha,
    })

state["entries"] = entries
save_json(STATE_FILE, state)
save_json(BUILD_LOG, build_log)
print("\n[cron] 상태 저장 완료")
