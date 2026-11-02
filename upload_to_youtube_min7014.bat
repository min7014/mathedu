@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================================================
echo [민은기 선생님의 수학자료실] https://www.youtube.com/@min7014 자동 업로더
echo Target Channel ID: UC7DN_e571yaTderHffKFTTg (@min7014)
echo ============================================================================

if exist "youtube_client_secret.json" (
    echo [1] Google OAuth 시크릿 파일 감지 완료 -> @min7014 채널로 한국어(KO)/영어(EN) 영상 자동 업로드 실행...
    python -X utf8 min7014_video_maker.py --upload-all --privacy public
    pause
    exit /b 0
)

if exist "client_secret.json" (
    echo [1] Google OAuth 시크릿 파일 감지 완료 -> @min7014 채널로 한국어(KO)/영어(EN) 영상 자동 업로드 실행...
    python -X utf8 min7014_video_maker.py --upload-all --privacy public
    pause
    exit /b 0
)

echo [안내] Google Cloud OAuth 파일(youtube_client_secret.json)이 아직 등록되지 않아
echo @min7014 공식 YouTube Studio 업로드 창과 로컬 마스터 MP4 폴더(youtube_uploads)를 즉시 엽니다.
python -X utf8 min7014_video_maker.py --open-studio
echo.
echo [업로드 완료 후 사이트 자동 연동]
echo 유튜브에 영상을 올리신 뒤 아래 명령어를 실행하면 @min7014 채널 RSS에서 링크를 자동으로 가져와 연결합니다:
echo python -X utf8 min7014_video_maker.py --sync-channel
pause
