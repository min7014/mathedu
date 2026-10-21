import os, json, glob, time

root = r'C:\Users\min\Desktop\mathedu'
now = time.time()
print("NOW epoch:", now)

print("\n=== _regen_*.py in root ===")
for f in sorted(glob.glob(os.path.join(root, '_regen_*.py'))):
    st = os.stat(f)
    print(os.path.basename(f), "mtime=%.0f" % st.st_mtime, "size=%d" % st.st_size)

for fn in ['_regen_cron_state.json', '_regen_data.json', '_regen_hash_cache.json', '_cron_state.json']:
    p = os.path.join(root, fn)
    print("\n=====", fn, "=====")
    if os.path.exists(p):
        try:
            txt = open(p, encoding='utf-8').read()
            print(txt[:3000])
        except Exception as e:
            print("ERR", repr(e))
    else:
        print("MISSING")
