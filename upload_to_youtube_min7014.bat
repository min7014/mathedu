@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================================================
echo [민은기 선생님의 수학자료실_AI] https://www.youtube.com/@min7014_ai 자동 생성·업로더
echo Target Channel ID: UCSlqQfOEtRfJuMPyGMLgFYA (@min7014_ai)
echo ============================================================================
"C:\Python\Python312\python.exe" -u -X utf8 min7014_video_maker.py --upload-all --privacy public
"C:\Python\Python312\python.exe" -u -X utf8 min7014_video_maker.py --sync-channel
git add video_lectures/ assets/
git commit -m "chore(youtube-vault): sync uploaded @min7014_ai video URLs"
git push origin main
pause
