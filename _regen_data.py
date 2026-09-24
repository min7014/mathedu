import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(r"C:\Users\min\Desktop\mathedu")
DATA_FILE = ROOT / "_regen_data.json"
BOARD = ROOT / "board"

def load():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return {"builds": []}

def save(data):
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def register(slugs):
    data = load()
    builds = data.setdefault("builds", [])
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    for slug in slugs:
        html = BOARD / f"{slug}.html"
        entry = {
            "slug": slug,
            "script": f"_regen_{slug}.py",
            "timestamp": now,
            "mtime": html.stat().st_mtime if html.exists() else None,
            "size": html.stat().st_size if html.exists() else 0,
            "hash": None,
        }
        if html.exists():
            import hashlib
            h = hashlib.sha256()
            with open(html, "rb") as f:
                for chunk in iter(lambda: f.read(1 << 16), b""):
                    h.update(chunk)
            entry["hash"] = h.hexdigest()
        builds.append(entry)
    save(data)
    print(f"  _regen_data.json 갱신 완료: {len(slugs)}개 slug 등록")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        register(sys.argv[1:])
