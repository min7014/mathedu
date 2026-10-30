import os, json, glob, hashlib

root = r"C:\Users\min\Desktop\mathedu"

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

print("=== Current script hashes ===")
for f in sorted(glob.glob(os.path.join(root, "_regen_*.py"))):
    print(f"  {os.path.basename(f)}: {sha256_file(f)}")

print("\n=== State file recorded hashes ===")
with open(os.path.join(root, ".regen_cron_state.json"), encoding="utf-8") as fh:
    st = json.load(fh)
for sid, e in st.get("entries", {}).items():
    print(f"  {sid}: {e.get('hash')}")
