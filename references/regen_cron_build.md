# regen_cron_build.md

## 개요
이 크론잡은 `C:\Users\min\Desktop\mathedu`의 `_regen_*.py` 스크립트들을 감시하여, 새 스크립트 추가나 기존 스크립트 변경 시 빌드/업데이트를 실행한다.

## 스케줄
1분마다 실행 (Windows cron)

## 감지 로직
### _regen_*.py 감시
- glob으로 `_regen_*.py` 목록 수집
- 각 `_regen_*.py`에 대해:
  - `script_mtime = os.path.getmtime(path)`
  - `key = path.stem.replace('_regen_', '')`  → slug 추출 (파일명 전체가 아님)
  - `last_build = state.get(key, {}).get('last_build')`
  - `hash = sha256file(path)` (SHA-256, 64자)
  - `state_hash = state.get(key, {}).get('hash')`
  - 변경 감지 조건: `last_build is None` (아직 빌드 안함) 또는 `script_mtime > last_build` (mtime 변경) 또는 `hash != state_hash` (내용 변경)
  - 변경 감지 시: 빌드 실행 → 빌드 성공 시 `state[key] = {'last_build': now, 'hash': hash, 'slug': key}` 갱신

### 상태 파일 구조
```json
{
  "577f9ca3": {
    "last_build": 1693700000.0,
    "hash": "sha256_hex_64chars",
    "slug": "577f9ca3"
  },
  "a33ab59b": { ... }
}
```
- 키는 **반드시 slug 만으로** 구성 (예: `"577f9ca3"`). `_regen_577f9ca3.py` 형태의 키를 사용하면 slug 키와 충돌해 JSON이 깨짐.
- `hash`는 **SHA-256** (64자). MD5(32자)와 혼동 금지.
- `mtime`도 실제 `os.path.getmtime` 값을 그대로 기록할 것.

### 새 스크립트 감지 (아직 state에 없음)
- state에 키가 없는 `_regen_*.py`가 있으면 → 무조건 빌드 실행

### 빌드 실행
- `python _regen_<slug>.py` 실행 (이 호스트에서는 `python3`가 깨져 있으므로 venv python 사용 권장)
- 빌드 성공 여부: 스크립트 exit code 0
- 빌드 성공 시: state 갱신 (hash, last_build, slug)
- 빌드 실패 시: state 갱신하지 않음 (다음 틱에 재시도)

### 빌드가 필요 없는 경우
- 모든 `_regen_*.py`가 state에 있고, mtime ≤ last_build 이며 hash 일치 → 아무 작업도 하지 않음
- 이 경우 `[SILENT]` 출력

## 환경 주의사항
- 이 호스트에서 `python3` 명령어는 깨져 있음 → `python` (3.11.15) 또는 venv python(`C:\Users\min\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe`) 사용
- 크론잡은 PowerShell이 아닌 git-bash(MSYS) 환경에서 실행됨

## 참고
- `_regen_*.py`는 내부적으로 `verify_quiz.verify_and_fix(data)`를 호출해 LaTeX 자동교정 + 기하 모순 경고를 수행한다.
- 빌드 후 `board/<slug>.html`이 생성/갱신된다.
- Flask 앱(app.py)은 port 5055에서 실행 중이며, `board/<slug>.html`을 serves한다.
