@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================================================
echo  ⚡ [@min7014_ai 무쿼터(Zero-API-Quota) YouTube Studio 로봇 브라우저 활성화]
echo ============================================================================
echo  - Google Cloud API 쿼터(일 10,000 units)와 무관하게 작동하는
echo    YouTube Studio 직접 업로드 로봇 프로필(.yt_studio_profile_min7014_ai)을 초기화합니다.
echo  - 열리는 크롬 창에서 @min7014_ai 계정으로 딱 1번만 로그인해 주시면,
echo    이후 API 쿼터가 소진되더라도 브라우저 로봇이 무쿼터로 자동 업로드를 이어갑니다!
echo ============================================================================
python -X utf8 -c "import min7014_video_maker as m; m.upload_slug_via_studio_browser('2017090603', langs=('ko',))"
pause
