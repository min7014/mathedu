import os, json, datetime

d = "C:/Users/min/Desktop/mathedu"
def ls(path):
    out = []
    for root, dirs, files in os.walk(path):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            st = os.stat(p)
            out.append((p, st.st_mtime, st.st_size))
    return out

rows = ls(d)

def regens():
    for p, m, s in rows:
        if "_regen_" in p and p.endswith(".py"):
            yield p, m, s

def board_files():
    for p, m, s in rows:
        if p.startswith(os.path.join(d, "board")) and p.endswith(".html"):
            yield p, m, s

print("===== _regen_*.py =====")
regens_sorted = sorted(regens())
for p, m, s in regens_sorted:
    print(f"{datetime.datetime.fromtimestamp(m, datetime.timezone.utc):%Y-%m-%d %H:%M:%S} UTC  {s:>8}  {p}")
print(f"count={len(regens_sorted)}")

print("\n===== board/*.html (all) =====")
board_sorted = sorted(board_files())
for p, m, s in board_sorted:
    print(f"{datetime.datetime.fromtimestamp(m, datetime.timezone.utc):%Y-%m-%d %H:%M:%S} UTC  {s:>8}  {p}")
print(f"count={len(board_sorted)}")

max_script = max((m for _, m, _ in regens_sorted), default=0)
max_board = max((m for _, m, _ in board_sorted), default=0)
print(f"\nmax script mtime = {datetime.datetime.fromtimestamp(max_script, datetime.timezone.utc) if max_script else None}")
print(f"max board mtime  = {datetime.datetime.fromtimestamp(max_board, datetime.timezone.utc) if max_board else None}")

logp = os.path.join(d, ".regen_build_log.json")
last_build = None
best = None
try:
    with open(logp, encoding="utf-8") as f:
        log = json.load(f)
    entries = log.get("logs", [])
    for e in entries:
        ts = e.get("timestamp", "")
        try:
            t = datetime.datetime.fromisoformat(ts)
        except Exception:
            continue
        if t.tzinfo is None:
            t = t.replace(tzinfo=datetime.timezone.utc)
        if e.get("status") == "success" and (best is None or t > best[1]):
            best = (e.get("slug"), t, e.get("stdout", "")[:90])
    last_build = best[1] if best else None
    print(f"\nlast success build = {last_build}")
    if best:
        print(f"  latest build slug={best[0]} ts={best[1]} stdout={best[2]}")
except Exception as ex:
    print(f"\ncant read build log: {ex}")

if last_build is None:
    print("\n[DECISION] cannot determine last build -> NO work")
elif max_script > last_build.timestamp():
    print(f"\n[DECISION] NEW script(s) newer than last build -> BUILD")
elif max_board > last_build.timestamp():
    print(f"\n[DECISION] board files updated after last build -> BUILD")
else:
    print(f"\n[DECISION] nothing new (scripts {datetime.datetime.fromtimestamp(max_script, datetime.timezone.utc) if max_script else None} <= last build {last_build}, board {datetime.datetime.fromtimestamp(max_board, datetime.timezone.utc) if max_board else None} <= last build) -> [SILENT]")
