import json, os

base = r"C:\Users\min\Desktop\mathedu"

# Read the actual cron state file (with leading dot)
for f in ["._regen_cron_state.json", "._cron_state.json", "_cron_check_regen.log", "_cron_decide.py", "_regen_cron_state.json"]:
    p = os.path.join(base, f)
    print("=" * 90)
    print("FILE:", f)
    try:
        with open(p, "r", encoding="utf-8") as fh:
            content = fh.read()
        print(content[:4000])
    except Exception as e:
        print("ERROR:", repr(e))
    print()
