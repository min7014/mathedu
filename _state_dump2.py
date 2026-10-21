import json, os

base = r"C:\Users\min\Desktop\mathedu"

# 1) _this_run.result
p = os.path.join(base, "_this_run.result")
print("=== _this_run.result ===")
try:
    with open(p, "r", encoding="utf-8") as fh:
        print(repr(fh.read()))
except Exception as e:
    print("ERROR:", repr(e))

# 2) board index.json
p = os.path.join(base, "board", "index.json")
print("\n=== board/index.json (post timestamps) ===")
try:
    with open(p, "r", encoding="utf-8") as fh:
        idx = json.load(fh)
    print(json.dumps(idx, ensure_ascii=False, indent=1)[:6000])
except Exception as e:
    print("ERROR:", repr(e))

# 3) offline index / versions
for f in ["offline\\index.json", "offline\\versions.json", "board\\index_site.json"]:
    p = os.path.join(base, f)
    print("\n=== %s ===" % f)
    try:
        with open(p, "r", encoding="utf-8") as fh:
            print(json.dumps(json.load(fh), ensure_ascii=False, indent=1)[:4000])
    except Exception as e:
        print("ERROR:", repr(e))
