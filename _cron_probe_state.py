# -*- coding: utf-8 -*-
import os, hashlib, json
from pathlib import Path

base = Path(r"C:\Users\min\Desktop\mathedu")

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

regen_files = sorted(base.glob("_regen_*.py"))
print("=== 현재 _regen_*.py ===")
for sp in regen_files:
    slug = sp.stem.replace("_regen_", "")
    h = sha256(sp)
    m = sp.stat().st_mtime
    print(f"{slug:12s} | mtime={m:.3f} | sha256[:16]={h[:16]}")

print("\n=== .regen_cron_state.json entries ===")
state = json.loads((base / ".regen_cron_state.json").read_text(encoding="utf-8"))
for k, v in state.get("entries", {}).items():
    print(f"{k:12s} | mtime={v.get('mtime',0):.3f} | hash[:16]={str(v.get('hash',''))[:16]} | last_build={v.get('last_build')} | out_size={v.get('output_size')}")

print("\n=== .regen_hash_cache.json ===")
hc = json.loads((base / ".regen_hash_cache.json").read_text(encoding="utf-8"))
print(json.dumps(hc, ensure_ascii=False, indent=2))

print("\n=== .regen_build_log.json tail ===")
bl = json.loads((base / ".regen_build_log.json").read_text(encoding="utf-8"))
logs = bl.get("logs", [])
print(f"total logs: {len(logs)}")
for e in logs[:5]:
    print(e.get("slug"), e.get("status"), e.get("timestamp"))
