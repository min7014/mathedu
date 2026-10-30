import os, hashlib, json

BASE = r'C:\Users\min\Desktop\mathedu'

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

# Load primary state (read-only)
state = json.load(open(os.path.join(BASE, '_cron_state.json'), encoding='utf-8'))
saved = state.get('entries', {})
print('saved_at:', state.get('updated_at'))

# Current scripts on disk (read-only)
current = {}
for f in sorted(os.listdir(BASE)):
    if f.startswith('_regen_') and f.endswith('.py'):
        fp = os.path.join(BASE, f)
        slug = f.replace('_regen_', '').replace('.py', '')
        current[slug] = {
            'script': f,
            'hash': sha256(fp),
            'mtime': os.path.getmtime(fp),
        }

print('\n--- comparison (saved vs current) ---')
new_slugs = [k for k in current if k not in saved]
changed = []
for slug, info in current.items():
    s = saved.get(slug)
    if not s:
        changed.append((slug, 'NOT_IN_STATE'))
    elif s.get('hash') != info['hash'] or s.get('mtime') != info['mtime']:
        changed.append((slug, 'CHANGED'))

print('new_slugs:', new_slugs)
print('changed:', changed)
print('total scripts on disk:', len(current))
print('total entries in state:', len(saved))

if not new_slugs and not changed:
    print('\nRESULT: [SILENT] — no new or changed _regen_*.py scripts')
else:
    print('\nRESULT: BUILD NEEDED')
