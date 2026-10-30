# -*- coding: utf-8 -*-
import os, json, hashlib

BASE = 'C:/Users/min/Desktop/mathedu'

def sha256_file(fp):
    h = hashlib.sha256()
    with open(fp, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

# Collect current _regen_*.py
current = {}
for f in sorted(os.listdir(BASE)):
    if f.startswith('_regen_') and f.endswith('.py'):
        fp = os.path.join(BASE, f)
        current[f.replace('_regen_','').replace('.py','')] = {
            'script': f,
            'hash': sha256_file(fp),
            'mtime': os.path.getmtime(fp),
        }

print('=== 현재 _regen_*.py 스크립트 ===')
for k in sorted(current):
    print(f"{k}: {current[k]['script']}  mtime={current[k]['mtime']}  hash={current[k]['hash'][:16]}")

# Load state files
for state_name in ['.regen_cron_state.json', '._regen_cron_state.json', '_cron_state.json']:
    sp = os.path.join(BASE, state_name)
    if os.path.exists(sp):
        with open(sp, encoding='utf-8') as f:
            st = json.load(f)
        entries = st.get('entries', {})
        print(f'\n=== 상태 파일 {state_name} ===')
        for slug in sorted(set(list(current) + list(entries))):
            e = entries.get(slug, {})
            c = current.get(slug)
            in_state = slug in entries
            in_current = slug in current
            if in_state and in_current:
                match = (e.get('hash') == c['hash'] and e.get('mtime') == c['mtime'])
                print(f"{slug}: state={e.get('hash','')[:12]}... mtime={e.get('mtime')} | current={c['hash'][:12]}... mtime={c['mtime']} | {'MATCH' if match else 'DIFF'}")
            elif in_current and not in_state:
                print(f"{slug}: state에 없음 (신규 후보)")
            elif in_state and not in_current:
                print(f"{slug}: current에 없음 (삭제 후보)")
