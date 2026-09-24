@echo off
REM mathedu 퀴즈 크론잡 래퍼
REM schtasks가 shell 리디렉션을 처리하지 못하므로bat에서 수행
"C:\Users\min\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe" "C:\Users\min\Desktop\mathedu\_regen_cron_check.py" >> "C:\Users\min\Desktop\mathedu\_cron.log" 2>&1
