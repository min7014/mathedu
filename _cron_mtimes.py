import os, glob, time, json
base = r"C:\Users\min\Desktop\mathedu"

print("=== board HTML mtimes (sorted asc) ===")
hs = []
for f in glob.glob(base + r"\board\*.html"):
    st = os.stat(f)
    hs.append((st.st_mtime, os.path.basename(f), st.st_size))
for m, b, s in sorted(hs):
    print(time.strftime("%Y-%m-%dT%H:%M:%S+09:00", time.localtime(m)), b, s)

print("\n=== current time ===")
print(time.strftime("%Y-%m-%dT%H:%M:%S+09:00", time.localtime()), "epoch", time.time())

print("\n=== scripts in dir ===")
for f in sorted(glob.glob(base + r"\_regen_*.py")):
    st = os.stat(f)
    print(time.strftime("%Y-%m-%dT%H:%M:%S+09:00", time.localtime(st.st_mtime)), os.path.basename(f), st.st_size)
