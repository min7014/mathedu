import os, time

base = os.path.dirname(os.path.abspath(__file__))

print("=== _regen_*.py files with mtime ===")
for f in sorted(os.listdir(base)):
    if f.startswith('_regen_') and f.endswith('.py'):
        p = os.path.join(base, f)
        if os.path.isfile(p):
            st = os.stat(p)
            print(f"{st.st_mtime:.0f} ({time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(st.st_mtime))})  {f}  size={st.st_size}")

print("\n=== board dir files with mtime ===")
bdir = os.path.join(base, 'board')
if os.path.isdir(bdir):
    for f in sorted(os.listdir(bdir)):
        p = os.path.join(bdir, f)
        if os.path.isfile(p):
            st = os.stat(p)
            print(f"{st.st_mtime:.0f} ({time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(st.st_mtime))})  {f}  size={st.st_size}")

print("\n=== state files ===")
for f in ['.regen_cron_state.json', '._regen_cron_state.json', '.regen_build_log.json', '._regen_build_log.json', '.regen_hash_cache.json']:
    p = os.path.join(base, f)
    if os.path.isfile(p):
        st = os.stat(p)
        print(f"{st.st_mtime:.0f} ({time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(st.st_mtime))})  {f}  size={st.st_size}")
