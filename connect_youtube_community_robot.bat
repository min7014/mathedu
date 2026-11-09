@echo off
chcp 65001 > nul
cd /d C:\Users\min\Desktop\mathedu
echo ==========================================================================
echo [최초 1회 연결] @min7014_ai 유튜브 채널 커뮤니티 직접 제어 로봇 로그인
echo 열리는 Chrome 창에서 구글 로그인을 1회 완료하시면 이후 커뮤니티 게시물/투표/댓글 고정이 100% 자동 제어됩니다!
echo ==========================================================================
C:\Python\Python312\python.exe -X utf8 C:\Users\min\Desktop\mathedu\youtube_community_controller.py --login
pause
