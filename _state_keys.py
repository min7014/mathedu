import json
from pathlib import Path

p = Path('._regen_cron_state.json')
raw = p.read_text(encoding='utf-8')
print('=== RAW (first 600 chars) ===')
print(raw[:600])
print()
print('=== PARSED ===')
state = json.loads(raw)
print('TOP-LEVEL KEYS:', list(state.keys()))
print('entries keys:', list(state.get('entries', {}).keys()))
for k, v in state.get('entries', {}).items():
    print('  key={!r}  script={!r}  hash={!r}  mtime={!r}  last_build={!r}'.format(
        k, v.get('script'), v.get('hash'), v.get('mtime'), v.get('last_build')))
