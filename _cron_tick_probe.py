import os, json, glob, hashlib, time

base = "C:/Users/min/Desktop/mathedu"

# max mtime in board dir
bmax = 0; bmaxf = None
for f in os.listdir(base + "/board"):
    p = os.path.join(base, "board", f)
    if os.path.isfile(p):
        m = os.stat(p).st_mtime
        if m > bmax:
            bmax = m; bmaxf = f
print("board newest:", bmaxf, "%.3f" % bmax, time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(bmax)))

# scripts newer than last state-update (2026-10-29T20:14:20 UTC)
cutoff = 1793304860.4945037
print("\nscripts newer than last state-update:")
for p in sorted(glob.glob(base + "/_regen_*.py")):
    m = os.stat(p).st_mtime
    flag = "NEW/CHANGED" if m > cutoff else "ok"
    print("  %-24s mtime=%.3f %s" % (os.path.basename(p), m, flag))

# all _regen_*.py vs state hash (fresh)
st = json.load(open(base + "/._regen_cron_state.json", encoding="utf-8"))
ents = st.get("entries", {})
print("\nscript state match (hash+mtime):")
for p in sorted(glob.glob(base + "/_regen_*.py")):
    slug = os.path.basename(p).replace("_regen_", "")
    cur = hashlib.sha256(open(p, "rb").read()).hexdigest()
    e = ents.get(slug, {})
    h_ok = e.get("hash", "") == cur
    m_ok = abs(e.get("mtime", 0) - os.stat(p).st_mtime) < 0.001
    print("  %-16s hash_ok=%s mtime_ok=%s" % (slug, h_ok, m_ok))
