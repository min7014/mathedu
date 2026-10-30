import hashlib, json, os

base = os.path.abspath('.')

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

with open(base + '/.regen_hash_cache.json') as f:
    cache = json.load(f)

print('cwd:', os.getcwd())
print('cache file:', base + '/.regen_hash_cache.json')
print('exists:', os.path.exists(base + '/.regen_hash_cache.json'))
print('stat size:', os.path.getsize(base + '/.regen_hash_cache.json'))
print()

print('=== Script hash check (on-disk vs cache) ===')
for slug in ['48d0d98f', '51908207', 'a33ab59b']:
    p = os.path.join(base, '_regen_' + slug + '.py')
    dh = sha(p)
    eh = cache.get(slug, {}).get('hash')
    match = (dh == eh)
    print('%s: MATCH=%s  ondisk=%s  exp=%s' % (slug, match, dh[:16], (eh or '')[:16]))

print()
print('=== _regen_*.py files on disk ===')
for f in sorted(os.listdir(base)):
    if f.startswith('_regen_') and f.endswith('.py'):
        p = os.path.join(base, f)
        print('  %s  size=%d' % (f, os.path.getsize(p)))

print()
print('=== board/ HTML files (modified after 2026-10-28 11:00 KST) ===')
board = sorted(os.listdir(base + '/board'))
for f in board:
    p = os.path.join(base, 'board', f)
    sz = os.path.getsize(p)
    if sz > 1000:
        print('  %s  size=%d' % (f, sz))
