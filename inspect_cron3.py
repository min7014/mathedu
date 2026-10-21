import os, json, glob, time

root = r'C:\Users\min\Desktop\mathedu'
now = time.time()
print("NOW:", time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(now)))

# latest build timestamp from build log
bl = json.load(open(os.path.join(root, '.regen_build_log.json'), encoding='utf-8'))
latest = None
for e in bl.get('logs', []):
    ts = e.get('timestamp', '')
    ts_e = None
    try:
        from datetime import datetime, timezone
        ts_e = datetime.fromisoformat(ts).timestamp()
    except Exception:
        pass
    if ts_e and (latest is None or ts_e > latest[0]):
        latest = (ts_e, ts, e.get('slug'), e.get('status'))
print("\nlatest build log entry:", latest)

# _regen scripts
print("\n=== _regen_*.py mtimes ===")
for f in sorted(glob.glob(os.path.join(root, '_regen_*.py'))):
    st = os.stat(f)
    print(" ", os.path.basename(f), time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(st.st_mtime)), "newer_than_latest_build:", st.st_mtime > (latest[0] if latest else now))

# board posts
print("\n=== board/*.html mtime vs latest build ===")
newer = []
for f in sorted(os.listdir(os.path.join(root, 'board'))):
    if f.endswith('.html'):
        p = os.path.join(root, 'board', f)
        mt = os.stat(p).st_mtime
        flag = "NEW!" if mt > (latest[0] if latest else now) else ""
        if mt > (latest[0] if latest else now):
            newer.append(f)
        print(f"  {f} mt={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(mt))} {flag}")
print("\nboard files newer than latest build:", newer)
