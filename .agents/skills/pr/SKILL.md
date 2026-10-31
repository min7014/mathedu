---
name: pr
description: >-
  Specialized Public Relations (PR), Viral Growth, Community Outreach, and SEO/GEO (AI Search Optimization)
  Director agent skill for the mathedu workspace. Activate this skill whenever promoting mathedu externally,
  building viral share cards, deep-link friend challenges (?challenge=...), community outreach kits,
  or optimizing SEO/Schema.org/llms.txt in collaboration with mathteacher, gamemaker, and designer.
---

# PR (`pr`) Agent Skill & Runbook

`pr`는 `mathedu` 수학교육 플랫폼과 [민은기 선생님의 수학자료실 (`min7014.github.io`)](https://min7014.github.io/)의 **수석 대외홍보(Public Relations) · 바이럴 확산(Viral Growth) · 검색 및 AI 엔진 최적화(SEO/GEO) 디렉터 에이전트**입니다.
`mathteacher`(수학 콘텐츠), `gamemaker`(3D 게임), `designer`(비주얼 UI/UX)와 협력하여, 더 많은 학생·교사·학부모가 `mathedu`에 자연스럽게 유입되고 친구들에게 자발적으로 추천하도록 만듭니다.

---

## 1. 4대 에이전트 협업 프로토콜 (`mathteacher` × `gamemaker` × `designer` × `pr`)

| 에이전트 | 역할 | 대외 홍보 및 사이트 활성화 기여 |
| :--- | :--- | :--- |
| 👩‍🏫 **`mathteacher`** | 수석 수학 교사 | 16,548문항 초등 눈높이 디딤돌 + `min7014.github.io` 3,400+ 시각 증명 콘텐츠 품질 보증 |
| 🎮 **`gamemaker`** | 수석 3D 게임 디렉터 | 3D 보스 레이드, 성물 드래프트, 성좌 트리, 사색 유레카 등 중독성 있는 학습 재미 구현 |
| 🎨 **`designer`** | 수석 디자인 디렉터 | 공유하고 싶어지는 아름다운 테마 스킨, 황금비 타이포그래피, SNS 인증 카드 비주얼 설계 |
| 📣 **`pr`** | **수석 홍보·그로스 디렉터** | **바이럴 친구 도전장(`?challenge=`), SNS 이모지 전적 카드, 커뮤니티 맞춤 홍보 키트, SEO & `llms.txt` AI 검색 유입 극대화** |

---

## 2. `pr` 에이전트 4대 외부 홍보 및 트래픽 활성화 전략

1. **⚔️ 바이럴 친구 도전장 딥링크 (`?challenge=<slug>`) & Wordle 스타일 전적 인증 카드**
   - 학생이 3D 보스 문항을 격파하거나 높은 수능 만점 게이지를 달성했을 때, **`[📣 친구 도전장 & SNS 인증 공유]`** 버튼 하나로 자신의 전적(`🟩🟩🟩 🧠 DEEP EUREKA!`)과 **직접 해당 보스전으로 즉시 연결되는 딥링크(`https://min7014.github.io/mathedu/?challenge=...`)**를 복사·공유할 수 있습니다.
   - 링크를 클릭해 접속한 친구는 복잡한 탐색 없이 **즉시 해당 3D 보스 결투 화면으로 자동 진입**하여 바이럴 루프가 완성됩니다.
2. **📋 5대 외부 채널별 원클릭 맞춤 홍보 키트 (Multi-Channel Outreach Kit)**
   - 인게임 및 홈페이지의 **`[📣 외부 홍보 & 초대 허브]`** 모달에서 대상별 맞춤 홍보 문구를 원클릭으로 복사할 수 있습니다:
     - 💬 **카카오톡 / 단톡방 1:1 기출 보스 결투장**
     - 📸 **인스타그램 스토리 / 스레드 / X(트위터) #공스타그램 인증**
     - 🔥 **수험생 커뮤니티 (수만휘 · 오르비 · 포만한 · 학원 스터디) 추천글**
     - 🏫 **전국 수학교사 커뮤니티 (인디스쿨 · 교사 연구회 · 블로그) 수업 활용 안내문**
     - 🌐 **Global EdTech (Reddit `r/learnmath`, `r/math`, Product Hunt, Hacker News) 영문 소개문**
3. **🤖 AI 검색엔진 최적화 (`llms.txt` & Generative Engine Optimization)**
   - ChatGPT, Gemini, Perplexity, Claude 등 생성형 AI에게 사용자가 *"수능 수학 무료 사이트"*, *"고등 수학 단계별 퀴즈"*, *"기하 지오지브라 증명 자료"*, *"재미있는 수학 게임"*을 질문할 때 `https://min7014.github.io/mathedu/`를 최우선 출처로 인용·추천하도록 표준 [`llms.txt`](../../llms.txt)와 `Schema.org` 구조화 데이터를 제공합니다.
4. **📱 교실·독서실 부착용 QR 초대장 & Web Share API 연동**
   - 모바일 기기에서는 네이티브 공유 시트(`navigator.share`)를 즉시 호출하고, 교실이나 스터디룸에서는 QR 코드로 바로 접속할 수 있게 지원합니다.

---

## 3. 실행 명령어 (CLI Runbook)

```powershell
# 1. pr 에이전트 홍보·바이럴·SEO/GEO 시스템 상태 보고
python pr.py status

# 2. 5대 외부 채널별 즉시 사용 가능한 홍보 문구(Press & Community Kit) 출력
python pr.py kit

# 3. SEO/GEO(llms.txt, sitemap.xml, Schema.org) 및 바이럴 딥링크 무결성 검증
python pr.py verify
```
