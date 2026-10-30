import os, json, glob, datetime

root = r"C:\Users\min\Desktop\mathedu"

def ts(s):
    return datetime.datetime.fromtimestamp(s, datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=9)))

print("=== Current _regen_*.py mtimes ===")
for f in sorted(glob.glob(os.path.join(root, "_regen_*.py"))):
    st = os.stat(f)
    print(f"  {os.path.basename(f)}: size={st.st_size} mtime={st.st_mtime:.3f} = {ts(st.st_mtime)}")

print("\n=== Main state: .regen_cron_state.json ===")
with open(os.path.join(root, ".regen_cron_state.json"), encoding="utf-8") as fh:
    st = json.load(fh)
print("updated_at:", st.get("updated_at"))
for sid, e in st.get("entries", {}).items():
    print(f"  {sid}: mtime={e.get('mtime')} last_build={e.get('last_build')} output_size={e.get('output_size')} hash={e.get('hash','')[:10]}...")

print("\n=== _this_run.result ===")
with open(os.path.join(root, "_this_run.result"), encoding="utf-8") as fh:
    print(fh.read())
