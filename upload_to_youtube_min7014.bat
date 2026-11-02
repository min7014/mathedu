@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================================================
echo [민은기 선생님의 수학자료실_AI] https://www.youtube.com/@min7014_ai 자동 생성·업로더
echo Target Channel ID: UCSlqQfOEtRfJuMPyGMLgFYA (@min7014_ai)
echo ============================================================================
echo.
echo [자동 실행] 렌더링된 한국어(KO)/영어(EN) 영상들을 @min7014_ai 채널에 자동 업로드합니다.
echo (최초 1회 실행 시 열리는 브라우저에서 @min7014_ai 계정으로 로그인해 주시면 이후 자동 업로드됩니다.)
echo.
python -X utf8 min7014_video_maker.py --upload-all --privacy public
echo.
echo [RSS 자동 동기화] @min7014_ai 채널에서 업로드된 영상 링크를 카탈로그에 반영합니다...
python -X utf8 min7014_video_maker.py --sync-channel
pause
