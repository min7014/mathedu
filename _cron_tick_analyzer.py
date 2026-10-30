# -*- coding: utf-8 -*-
import os, sys, json, hashlib, time
from pathlib import Path

BASE = Path("C:/Users/min/Desktop/mathedu")

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def load_json(p):
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}

def save_json(p, data):
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

state = load_json(BASE / ".regen_cron_state.json")
entries = state.setdefault("entries", {})
hash_cache = load_json(BASE / ".regen_hash_cache.json")
build_log = load_json(BASE / ".regen_build_log.json")
builds = state.get("builds", [])

regen_files = sorted(BASE.glob("_regen_*.py"))
print(f"[cron] 현재 스크립트: {len(regen_files)}개")

# 1) 각 스크립트의 현재 sha256 + mtime
current = {}
for sp in regen_files:
    slug = sp.stem.replace("_regen_", "")
    current[slug] = {"path": str(sp), "sha": sha256(sp), "mtime": sp.stat().st_mtime}

# 2) cache와 비교 (hash + mtime 기준)
#    .regen_hash_cache.json은 {slug: {hash, mtime}} 형태
for slug, info in current.items():
    ch = hash_cache.get(slug, {})
    old_hash = ch.get("hash", "")
    old_mtime = ch.get("mtime", 0)
    reason = ""
    if info["sha"] != old_hash:
        reason = "hash changed"
    elif info["mtime"] != old_mtime:
        reason = "mtime updated"
    if reason:
        print(f"[cron] 변경 감지: {slug} ({reason})")
        entries[slug] = {"script": sp.name, "hash": info["sha"], "mtime": info["mtime"],
                         "last_build": None, "last_build_ts": None, "output_size": 0}
    else:
        print(f"[cron] 변경 없음: {slug}")

# 3) 삭제 정리 (state의 slug 중 현재 스크립트가 없는 것)
existing_slugs = set(current.keys())
stale = [k for k in entries if k not in existing_slugs]
for k in stale:
    del entries[k]
    print(f"[cron] 정리: {k} (삭제됨)")

# 4) 결과 판정
if not stale and not any(entries.get(k, {}).get("last_build") is None for k in entries):
    # 실제로 last_build가 없는(즉 아직 빌드 안 된) 항목이 있는지 확인
    unbuilt = [k for k, v in entries.items() if v.get("last_build") is None]
    if unbuilt:
        print(f"[cron] 빌드하지 않은 항목: {unbuilt}")
        print("[SILENT]")  # 아직 빌드 기록 없음 -> 그대로 침묵
        sys.exit(0)

# 미변경이면 SILENT
if not entries or all(v.get("last_build") for v in entries.values()):
    print("[SILENT]")
    save_json(BASE / ".regen_cron_state.json", state)
    sys.exit(0)

print(f"\n[cron] 변경/빌드 필요: {len(entries)}개 항목")
print("[콘솔 출력 끝]")
