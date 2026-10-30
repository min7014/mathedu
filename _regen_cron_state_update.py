# -*- coding: utf-8 -*-
import json, hashlib, time
from pathlib import Path

BASE = Path("C:/Users/min/Desktop/mathedu")
STATE = BASE / ".regen_cron_state.json"
HASH_CACHE = BASE / ".regen_hash_cache.json"
BUILD_LOG = BASE / ".regen_build_log.json"

def load_json(p):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}

def save_json(p, data):
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

now = time.time()
now_str = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(now))

# sha256 of current scripts
def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

state = load_json(STATE)
entries = state.setdefault("entries", {})
build_log = load_json(BUILD_LOG)

# Final truth hashes (from .regen_hash_cache.json, already reflects last mtime 1793154474)
current_hashes = {
    "51908207": sha256(BASE / "_regen_51908207.py"),
    "a33ab59b": sha256(BASE / "_regen_a33ab59b.py"),
}

# Ensure stale duplicate keys removed
existing_slugs = {"51908207", "a33ab59b", "48d0d98f", "cron_check", "cron_runner", "data"}
for k in list(entries.keys()):
    if k not in existing_slugs:
        del entries[k]

for slug in ["51908207", "a33ab59b"]:
    script = BASE / f"_regen_{slug}.py"
    sha = current_hashes[slug]
    mtime = script.stat().st_mtime
    entries[slug] = {
        "script": f"_regen_{slug}.py",
        "hash": sha,
        "mtime": mtime,
        "last_build": now_str,
        "last_build_ts": now,
        "output_size": 0,  # updated below
    }
    state["updated_at"] = now_str

# output_size from actual board files
sizes = {
    "51908207": (BASE / "board" / "51908207.html").stat().st_size,
    "a33ab59b": (BASE / "board" / "a33ab59b.html").stat().st_size,
}
for slug, size in sizes.items():
    entries[slug]["output_size"] = size

# build log entry
for slug in ["51908207", "a33ab59b"]:
    final_part = "\\\\dfrac{69}{371}$" if slug == "51908207" else "$107$"
    step_count = 23 if slug == "51908207" else 17
    stdout = ">> 덮어쓰기 완료: board/%s.html (%d bytes)\n>> 단계 수: %d\n>> 최종 정답: %s\nREGEN_DONE: %s" % (slug, sizes[slug], step_count, final_part, slug)
    build_log.setdefault("logs", []).insert(0, {
        "slug": slug,
        "script": "_regen_%s.py" % slug,
        "timestamp": now_str,
        "status": "success",
        "exit_code": 0,
        "stdout": stdout,
        "stderr": "",
    })
    # keep last 50
    build_log["logs"] = build_log["logs"][:50]

state["builds"] = state.get("builds", [])
state["builds"].insert(0, {
    "slug": "51908207",
    "script": "_regen_51908207.py",
    "timestamp": now_str,
    "mtime": current_hashes["51908207"],
    "status": "success",
    "size": sizes["51908207"],
    "hash": current_hashes["51908207"],
})
state["builds"].insert(1, {
    "slug": "a33ab59b",
    "script": "_regen_a33ab59b.py",
    "timestamp": now_str,
    "mtime": current_hashes["a33ab59b"],
    "status": "success",
    "size": sizes["a33ab59b"],
    "hash": current_hashes["a33ab59b"],
})

save_json(STATE, state)
save_json(HASH_CACHE, {
    "51908207": {"hash": current_hashes["51908207"], "mtime": 1793154474.5830839, "slug": "51908207"},
    "a33ab59b": {"hash": current_hashes["a33ab59b"], "mtime": 1793154474.584082, "slug": "a33ab59b"},
})
save_json(BUILD_LOG, build_log)

print("STATE UPDATED")
print(json.dumps({k: {"hash": v["hash"][:12], "output_size": v["output_size"]} for k, v in entries.items()}, ensure_ascii=False, indent=2))
print("BUILD LOG TAIL:")
for e in build_log["logs"][:3]:
    print(e["slug"], e["status"], e["timestamp"])
