# 🔓 @min7014_ai 유튜브 업로드 제한(할당량·일일 한도) 완벽 해제 가이드

현재 유튜브 자동 업로드에서 발생할 수 있는 제한은 **① Google Cloud API 일일 할당량(하루 6개 제한)**과 **② 유튜브 채널 자체 일일 업로드 한도(하루 10~15개 제한)** 두 가지입니다. 아래 방법으로 두 제한을 모두 영구적으로 해제할 수 있습니다.

---

## 1️⃣ [가장 빠른 즉시 해결] 유튜브 스튜디오 '3단계 고급 기능' 활성화 (채널 일일 한도 무제한 해제)
유튜브 채널(`@min7014_ai`) 자체의 24시간 업로드 제한(`uploadLimitExceeded`)을 하루 50~100개 이상으로 푸는 방법입니다.

1. **[YouTube Studio](https://studio.youtube.com/channel/UCSlqQfOEtRfJuMPyGMLgFYA)** 접속 ➔ 좌측 하단 **⚙️ 설정(Settings)** 클릭
2. **채널(Channel)** ➔ **기능 사용 자격 요건(Feature eligibility)** 탭 클릭
3. **3. 고급 기능(Advanced features)** 옆의 **[기능 사용 신청]** 클릭 후 **휴대폰 QR 영상 인증(30초 소요)** 완료
4. 완료 즉시 채널의 하루 업로드 한도가 대폭 상향되며, [`youtube_uploads/top5_shorts_now/`](../youtube_uploads/top5_shorts_now) 폴더의 파일들을 마우스로 한 번에 드래그해 하루 수십 개씩 즉시 올릴 수 있습니다! (설명은 백그라운드 데몬이 자동 입력)

---

## 2️⃣ [API 무인 업로드 2~5배 즉시 확장] Google Cloud 다중 프로젝트(Multi-Project) 토큰 로테이션
Google Cloud의 무료 프로젝트 1개당 하루 **10,000 유닛(영상 업로드 6개)**이 기본 제공됩니다. [`min7014_video_maker.py`](../min7014_video_maker.py)에는 여러 프로젝트 토큰(`youtube_token_min7014_ai_2.json`, `youtube_token_min7014_ai_3.json` 등)을 자동으로 번갈아 사용하는 **다중 토큰 로테이션 풀(`get_available_youtube_upload_service`)**이 탑재되어 있습니다.

1. **[Google Cloud Console 프로젝트 생성](https://console.cloud.google.com/projectcreate)**에서 새 프로젝트(예: `mathedu-yt-2`, `mathedu-yt-3`)를 추가 생성합니다.
2. 각 프로젝트에서 **[YouTube Data API v3 사용 설정](https://console.cloud.google.com/apis/library/youtube.googleapis.com)**을 켭니다.
3. **사용자 인증 정보(Credentials) ➔ OAuth 클라이언트 ID (데스크톱 앱)** 생성 후 JSON 파일을 다운로드하여 `mathedu` 폴더에 넣고 인증하면, 프로젝트 개수 × 6개(예: 3개면 하루 **18개** 완전 무인 API 업로드)가 매일 자동 업로드됩니다!

---

## 3️⃣ [근본 해결 · 무료] Google 공식 YouTube API 할당량 상향 신청 (하루 6개 ➔ 하루 600개 무료)
현재 사용 중인 Google Cloud 프로젝트(`Project Number: 711696878912`)의 일일 할당량을 무료로 100배(1,000,000 유닛/일) 늘리는 공식 신청서입니다.

- **신청 링크**: **[Google YouTube API 할당량 상향 신청 폼 열기](https://support.google.com/youtube/contact/yt_api_form)**
- **할당량 확인 링크**: **[GCP 프로젝트 711696878912 할당량 콘솔](https://console.cloud.google.com/iam-admin/quotas?project=711696878912&service=youtube.googleapis.com)**
- **신청서 복사·붙여넣기용 답변**:
  - **Project Number**: `711696878912`
  - **YouTube Channel URL**: `https://www.youtube.com/@min7014_ai`
  - **Website URL**: `https://min7014.github.io/mathedu/`
  - **Requested Quota**: `100,000 units/day` (하루 약 60개 영상 업로드 가능)
  - **Use Case Description (복사해서 붙여넣기)**:
    > We operate an open-access, 100% free K-12 mathematics education platform (Min's Math Lab, https://min7014.github.io/mathedu/) with 1,113 step-by-step visual geometry proofs and 16,548 interactive math problems. Our automated pipeline renders Korean and English 1080p visual proof lectures and 9:16 YouTube Shorts and uploads them to our official educational channel (@min7014_ai) using YouTube Data API v3 (`videos.insert`, `videos.update`, `thumbnails.set`, `playlistItems.insert`). Because each `videos.insert` call consumes 1,600 units, the default 10,000 units/day limit only allows 6 uploads per day. We request a quota increase to 100,000 units/day to publish our 1,113 multilingual math proof videos and Shorts for students and teachers worldwide.
