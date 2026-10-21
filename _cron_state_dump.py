import json, os

base = r"C:\Users\min\Desktop\mathedu"

for f in ["._regen_cron_state.json", "_cron_state.json", ".regen_build_log.json",
          "_regen_hash_cache.json", "_regen_cron_state.json", "_regen_data.json"]:
    path = os.path.join(base, f)
    print("=" * 90)
    print("FILE:", f)
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        print(json.dumps(data, ensure_ascii=False, indent=1)[:4000])
    except Exception as e:
        print("ERROR:", repr(e))
    print()
