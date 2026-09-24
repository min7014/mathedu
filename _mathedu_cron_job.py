import os, sys, json, hashlib, subprocess
from datetime import datetime, timezone

mathedu_dir = 'C:\\Users\\min\\Desktop\\mathedu'
result_file = os.path.join(mathedu_dir, '_this_run.result')

def log(msg):
    print(msg, flush=True)
    with open(result_file, 'w', encoding='utf-8') as f:
        f.write(msg + '\n')

def compute_hash(filepath):
    sha = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha.update(chunk)
    return sha.hexdigest()

def get_current_scripts():
    scripts = {}
    for f in sorted(os.listdir(mathedu_dir)):
        if f.startswith('_regen_') and f.endswith('.py'):
            fp = os.path.join(mathedu_dir, f)
            slug = f.replace('_regen_', '').replace('.py', '')
            scripts[slug] = {
                'script': f,
                'hash': compute_hash(fp),
                'mtime': os.path.getmtime(fp)
            }
    return scripts

log(f'[{datetime.now(timezone.utc).isoformat()}] mathedu 크론잡 시작')
log(f'파이썬 버전: {sys.version}')

current = get_current_scripts()
log(f'디스크에 {len(current)}개의 _regen_*.py 스크립트 발견: {[f"_regen_{k}.py" for k in sorted(current)]}')

with open(os.path.join(mathedu_dir, '_cron_state.json'), encoding='utf-8') as f:
    saved = json.load(f)
saved_entries = saved.get('entries', {})

new_scripts = [k for k in current if k not in saved_entries]
changed_scripts = []
for k, v in current.items():
    saved_entry = saved_entries.get(k)
    if saved_entry and (v['hash'] != saved_entry['hash'] or v['mtime'] != saved_entry['mtime']):
        changed_scripts.append(k)

to_build = list(set(new_scripts + changed_scripts))

log(f'신규 스크립트: {new_scripts}')
log(f'변경된 스크립트: {changed_scripts}')
log(f'빌드 대상: {to_build}')

if not to_build:
    log('[SILENT]')
    log(f'[{datetime.now(timezone.utc).isoformat()}] mathedu 크론잡 완료 — 변경사항 없음')
else:
    for slug in sorted(to_build):
        v = current[slug]
        script_path = os.path.join(mathedu_dir, v['script'])
        log(f'--- {slug}: {v["script"]} 빌드 시작 (해시: {v["hash"][:16]}...) ---')
        
        log(f'  스크립트 삭제: {v["script"]}')
        os.remove(script_path)
        
        log(f'  mathedu 빌드 실행 중...')
        try:
            result = subprocess.run(
                ['python', 'regen.py'],
                cwd=mathedu_dir,
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.stdout:
                for line in result.stdout.strip().split('\n')[-5:]:
                    log(f'  [build-out] {line}')
            if result.stderr:
                for line in result.stderr.strip().split('\n')[-5:]:
                    log(f'  [build-err] {line}')
            log(f'  빌드 종료 코드: {result.returncode}')
        except subprocess.TimeoutExpired:
            log(f'  빌드 시간 초과 (300초)')
        except Exception as e:
            log(f'  빌드 오류: {e}')
        
        if os.path.exists(script_path):
            new_hash = compute_hash(script_path)
            new_mtime = os.path.getmtime(script_path)
            log(f'  스크립트 재생성됨: 해시={new_hash[:16]}... mtime={datetime.fromtimestamp(new_mtime, tz=timezone.utc).isoformat()}')
        else:
            log(f'  WARNING: 스크립트 재생성되지 않음!')
    
    log(f'[{datetime.now(timezone.utc).isoformat()}] mathedu 크론잡 완료')
