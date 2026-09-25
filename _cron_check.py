import sys
from _regen_cron_check import main

if __name__ == "__main__":
    try:
        code = main()
        sys.exit(code if isinstance(code, int) else 0)
    except Exception:
        print("[SILENT]")
        sys.exit(0)
