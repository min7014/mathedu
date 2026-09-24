#!/bin/bash
cd /c/Users/min/Desktop/mathedu
echo "=== mathedu 크론잡 실행 $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo ""
echo "--- 1. _regen_*.py 스크립트 현황 확인 ---"
C:/Python/Python312/python _regen_cron_check.py 2>&1
EXIT_CODE=$?
echo ""
echo "--- 2. 크론 체크 결과 ---"
if [ $EXIT_CODE -eq 0 ]; then
    echo "[SILENT - 변경사항 없음, 작업 종료]"
else
    echo "[변경사항 감지됨 - 빌드 필요]"
fi
echo ""
echo "=== 크론잡 완료 ==="
