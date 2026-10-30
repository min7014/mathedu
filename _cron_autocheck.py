import os, json, hashlib

root = r"C:\Users\min\Desktop\mathedu"

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

# Current disk state
print("=== CURRENT DISK _regen_*.py ===")
cur = {}
for f in sorted(os.listdir(root)):
    if f.startswith('_regen_') and f.endswith('.py'):
        fp = os.path.join(root, f)
        st = os.stat(fp)
        h = sha256_file(fp)
        sl = f.replace('_regen_','').replace('.py','')
        cur[sl] = {'script': f, 'size': st.st_size, 'mtime': st.st_mtime, 'hash': h}
        print(f"{sl}: size={st.st_size} mtime={st.st_mtime:.6f} hash={h[:16]}...")

# Saved state
with open(os.path.join(root, '_cron_state.json'), encoding='utf-8') as f:
    saved = json.load(f)
saved_entries = saved.get('entries', {})
print("\n=== SAVED _cron_state.json entries ===")
for k, v in sorted(saved_entries.items()):
    print(f"{k}: script={v.get('script')} hash={v.get('hash','')[:16]}... mtime={v.get('mtime')}")

# Compare
print("\n=== COMPARISON ===")
new_scripts = [k for k in cur if k not in saved_entries]
changed = []
for k, v in cur.items():
    se = saved_entries.get(k)
    if se and (se.get('hash') != v['hash'] or se.get('mtime') != v['mtime']):
        changed.append(k)
to_build = sorted(set(new_scripts + changed))
print("new_scripts:", new_scripts)
print("changed:", changed)
print("to_build:", to_build)
if not to_build:
    print("[SILENT]")
