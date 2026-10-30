import os, json, time
base = r"C:\Users\min\Desktop\mathedu"
for f in ["_regen_cron_runner.py","_regen_cron_check.py","_regen_data.py"]:
    print("="*30, f, "="*30)
    print(open(base + "\\" + f, encoding="utf-8", errors="replace").read())
