import os, glob, json, datetime

base = "C:/Users/min/Desktop/mathedu"

print("=== .regen_cron_state.json ===")
try:
    print(open(base + "/._regen_cron_state.json", encoding="utf-8").read())
except Exception as e:
    print("ERR", e)

print("=== exact mtimes of _regen scripts ===")
for p in sorted(glob.glob(base + "/_regen_*.py")):
    st = os.stat(p)
    dt = datetime.datetime.fromtimestamp(st.st_mtime, datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"{os.path.basename(p):35s} mtime={st.st_mtime:.0f} {dt}")

print("=== board html count ===")
fs = sorted(glob.glob(base + "/board/*.html"))
print("count:", len(fs))
if fs:
    st = os.stat(fs[-1])
    dt = datetime.datetime.fromtimestamp(st.st_mtime, datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print("newest:", os.path.basename(fs[-1]), st.st_mtime, dt, st.st_size)

print("=== .regen_build_log.json latest 5 logs ===")
try:
    bl = json.load(open(base + "/.regen_build_log.json", encoding="utf-8"))
    for e in bl.get("logs", [])[:8]:
        print(e.get("slug"), e.get("timestamp"), e.get("status"), e.get("exit_code"), (e.get("stdout") or "")[:60].replace("\n", " "))
except Exception as ex:
    print("ERR", ex)
