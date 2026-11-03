---
name: pr
description: >-
  Specialized Public Relations (PR), Viral Growth, YouTube×Website Bi-Directional Funnel, Community Outreach,
  and SEO/GEO (AI Search Optimization) Director agent skill for the mathedu workspace. Activate this skill
  whenever promoting mathedu and @min7014_ai externally, generating 7-channel viral campaigns, rendering 1200x630
  SNS promo cards, deep-link friend challenges (?challenge=...), or optimizing SEO/Schema.org/llms.txt in
  collaboration with mathteacher, gamemaker, and designer.
---

# PR (`pr` v2.0) Autonomous Promotion & Viral Growth Agent Skill & Runbook

`pr`는 `mathedu` 수학교육 플랫폼, [민은기 선생님의 수학자료실 (`min7014.github.io`)](https://min7014.github.io/), 그리고 공식 유튜브 채널([`@min7014_ai`](https://www.youtube.com/@min7014_ai))의 **전담 자율 홍보(Public Relations) · 양방향 바이럴 퍼널(YouTube ↔ Website Funnel) · 검색 및 AI 엔진 최적화(SEO/GEO) 디렉터 에이전트**입니다.

---

## 1. 5대 자율 홍보 엔진 아키텍처 (`pr.py` v2.0)

1. **🎯 7대 외부 채널별 맞춤형 홍보 캠페인 자동 생성기 (`assets/pr_growth_engine.json`)**:
   - `video_lectures/catalog.json` 및 `assets/min7014_deep_knowledge.json`에 새 영상·자료가 추가될 때마다 **7대 타겟 채널별 맞춤형 홍보 문구와 5대 홈페이지 직행 딥링크**를 자동 생성합니다:
     1. **📺 유튜브 고정댓글 · 커뮤니티 탭 (`youtube_pinned`)**: 영상 시청 직후 GeoGebra 동적 조작(`video_board.html?slug=...`) 및 탈-5지선다 창의 기출(`index.html?q=...`)로 직행 유도
     2. **💬 카카오톡 · 학급/스터디 단톡방 1초 도전장 (`kakao_challenge`)**: 1분 시각 증명 영상 + 탈-5지선다 기출 결투장 세트
     3. **🔥 수험생 커뮤니티 (`student_community` — 수만휘·오르비·포만한)**: '보조선 플립북 영상 + 탈-5지선다 수식 레고 조립' 학습법 칼럼형 추천글
     4. **🏫 전국 수학교사 커뮤니티 (`teacher_indischool` — 인디스쿨·교사 연구회)**: 수업 도입 5분 시각 증명 영상 + 학생 참여형 탈-5지선다 퀴즈 나눔 키트
     5. **📸 인스타그램 · 블로그 · 스레드 · X (`insta_blog`)**: `#공스타그램` 이모지 성취 기록 카드 및 해시태그 세트
     6. **👨‍👩‍👧 학부모 · 초중고 교육 카페 (`parent_cafe`)**: 사교육·암기 없이 초등 눈높이 무장벽 디딤돌부터 수능까지 깨치는 원리 수학 안내문
     7. **🌐 Global EdTech (`global_reddit` — Reddit `r/learnmath`, `r/math`, Hacker News)**: 영문 1080p 시각 증명 & 16,548문항 창의 구성 OER 소개문

2. **🖼️ 고클릭률(CTR) SNS 오픈그래프 & 홍보 배너 자동 렌더링 (`assets/pr_cards/pr_card_*.png`)**:
   - Pillow 기반으로 1200×630 해상도의 다크 네이비·골드·시안 고대비 SNS 공유 배너(`pr_card_0001.png` ~ `pr_card_0005.png`)를 자동 생성하여 블로그·카페·단톡방·SNS 공유 시 클릭률을 극대화합니다.

3. **🎬 YouTube(`@min7014_ai`) ➔ 홈페이지(`mathedu`) 양방향 트래픽 증폭 퍼널**:
   - 모든 1080p 본편 및 9:16 `#Shorts` 영상 하단에 **상시 홈페이지 홍보 바(`min7014.github.io/mathedu`)** 각인
   - 모든 유튜브 영상 설명란 최상단에 **5대 홈페이지 직행 퍼널 딥링크** 자동 삽입 및 YouTube Data API v3 일괄 동기화(`--boost-youtube`)

4. **🌐 홈페이지 인라인 『📣 홍보 에이전트(PR) 7대 채널 스튜디오』 (`index.html`, `video_board.html`, `mathedu-room.js`)**:
   - 메인 화면 `#homePrAgentStudioBox`에서 누구나 홍보할 주제와 7대 채널을 선택해 1초 만에 맞춤 홍보 문구를 복사하고 1200×630 홍보 배너 PNG를 다운로드할 수 있습니다.
   - 전 문항(16,548문항) 풀이 화면 상단에 `🎬 @min7014_ai 유튜브 시각 증명` 및 `📢 유튜브+문제 1초 홍보 공유` 버튼을 제공합니다.

5. **🤖 AI 검색엔진(`llms.txt`) · 검색엔진(`sitemap.xml`) · 24/7 데몬(`mathedu_foundation_daemon.py`) 자동 연동**:
   - 새 영상/문제가 생성될 때마다 `mathedu_foundation_daemon.py`가 `pr.run_autonomous_pr_cycle()`을 자동 호출하여 `assets/pr_growth_engine.json`과 `llms.txt`를 최신 상태로 유지합니다.

---

## 2. 실행 명령어 (CLI Runbook)

```powershell
# 1. 홍보 에이전트 상태 점검 및 캠페인·비주얼 카드·llms.txt 자동 동기화
python -X utf8 pr.py status

# 2. 특정 주제(예: 0003 피타고라스, 0001 메넬라우스)의 7대 채널 홍보 문구 즉시 출력
python -X utf8 pr.py kit 0003

# 3. 전체 캠페인 JSON + 1200x630 SNS 카드 + llms.txt 강제 재생성
python -X utf8 pr.py generate

# 4. 홍보 에이전트 데이터·비주얼 카드·SEO/GEO·JS 문법 무결성 검증
python -X utf8 pr.py verify
```
