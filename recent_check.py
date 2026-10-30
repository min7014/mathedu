import os, datetime
base = r"C:\Users\min\Desktop\mathedu"
last_build = 1793240333.0

print("NOW:", datetime.datetime.utcfromtimestamp(os.path.getmtime(__file__)).strftime("%Y-%m-%dT%H:%M:%SZ"))

print("\n--- files in base dir with mtime > %s ---" % last_build)
recent = []
for fn in sorted(os.listdir(base)):
    p = os.path.join(base, fn)
    if os.path.isfile(p):
        st = os.stat(p)
        if st.st_mtime > last_build:
            recent.append((fn, st.st_mtime, st.st_size))
for fn, mt, sz in sorted(recent, key=lambda x: -x[1]):
    print(fn, datetime.datetime.utcfromtimestamp(mt).strftime("%Y-%m-%dT%H:%M:%SZ"), sz)

print("\n--- _watchdog files ---")
for fn in sorted(os.listdir(base)):
    if fn.startswith("_watchdog"):
        p = os.path.join(base, fn)
        if os.path.exists(p):
            st = os.stat(p)
            print(fn, "mtime=" + str(st.st_mtime), "size=" + str(st.st_size))
            try:
                with open(p, "r", encoding="utf-8", errors="replace") as f:
                    print("  content:", f.read()[:500])
            except Exception as e:
                print("  read err:", e)

print("\n--- board dir recent files (mtime > %s) ---" % last_build)
board = os.path.join(base, "board")
recent_board = []
for fn in sorted(os.listdir(board)):
    p = os.path.join(board, fn)
    if os.path.isfile(p):
        st = os.stat(p)
        if st.st_mtime > last_build:
            recent_board.append((fn, st.st_mtime, st.st_size))
for fn, mt, sz in sorted(recent_board, key=lambda x: -x[1]):
    print(fn, datetime.datetime.utcfromtimestamp(mt).strftime("%Y-%m-%dT%H:%M:%SZ"), sz)
print("  count:", len(recent_board))
