---
name: finance
description: >-
  Specialized Ad Monetization & Sustainable Free-EdTech Director agent skill for the mathedu workspace.
  Activate this skill whenever setting up or optimizing Google AdSense, Kakao AdFit, ads.txt,
  non-intrusive native banner slots, or in-game rewarded ad chests while keeping mathedu 100% free for learners.
---

# Finance (`finance`) Agent Skill & Runbook (100% 무료 학습 + 클린 광고 수익화)

`finance`는 `mathedu` 수학교육 플랫폼의 **수석 광고 수익화(Ad Monetization) 및 무료 교육 지속가능성 디렉터 에이전트**입니다.
**학생과 교사에게는 모든 수학 콘텐츠를 100% 무료로 제공**하면서, **`mathteacher` · `gamemaker` · `designer` · `pr`** 에이전트와 협력하여 **구글 애드센스(Google AdSense), 카카오 애드핏(Kakao AdFit), 인게임 보상형 스폰서 상자(Rewarded Ad Chest)**를 통해 안정적인 광고 수익을 창출합니다.

---

## 1. 5대 에이전트 협업 생태계 (`mathteacher` × `gamemaker` × `designer` × `pr` × `finance`)

```mermaid
flowchart LR
    M["👩‍🏫 mathteacher<br/>16,548문항 디딤돌 &<br/>3,400+ 시각 증명"] --> G["🎮 gamemaker<br/>3D 보스 레이드 &<br/>깊은 사색 유레카"]
    G --> D["🎨 designer<br/>3대 테마 스킨 &<br/>네이티브 광고 UI"]
    D --> P["📣 pr<br/>바이럴 도전장 &<br/>SEO/AI 유입 증폭"]
    P --> F["💼 finance<br/>클린 애드센스/애드핏 &<br/>보상형 광고 수익화"]
```

---

## 2. `finance` 에이전트 4대 클린 광고 수익화 아키텍처

1. **🎁 인게임 자발적 보상형 광고 — 「아르키메데스의 후원 상자 (Rewarded Sponsor Chest)」**
   - *Duolingo* 등 세계적인 무료 교육 앱이 채택한 최고 효율 수익 모델입니다.
   - 학생이 원할 때 **`[🎁 무료 스폰서 광고 보고 보너스 충전 (+50 XP & 필살기 100% 완충)]`** 버튼을 클릭하면 5초 스폰서/애드센스 광고 모달이 노출된 후 즉시 게임 보상(`+50 XP`, `기하 통찰 필살기 100% 완충`, `사색 통찰 게이지 +40%`)이 지급됩니다.
   - 학습 흐름을 전혀 방해하지 않으면서 일반 배너 대비 **5~10배 높은 광고 단가(eCPM)**를 달성합니다.
2. **🖼️ 비침습적 네이티브 글래스모피즘 배너 슬롯 (`mathedu-ads.js`)**
   - 문제 풀이 화면이나 수식을 가리지 않고,① 메인 포털 탐색기 하단(`#matheduAdSlotMain`), ② 3D 원정대 콘솔 푸터(`#matheduAdSlotQuest`), ③ 보스 격파 승리 결과창 하단에만 깔끔한 네이티브 카드 형태로 광고 슬롯을 배치합니다.
3. **📄 표준 `ads.txt` 및 원클릭 퍼블리셔 ID 연동 (`ad_config.json` / `finance.py`)**
   - 루트 경로의 [`ads.txt`](../../ads.txt)를 통해 Google AdSense(`google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0`) 및 Kakao AdFit 공식 인증을 즉시 통과할 수 있도록 구성합니다.
   - 퍼블리셔 ID가 아직 입력되지 않은 초기 상태에서는 **클린 교육 스폰서 프리뷰 배너**로 작동하며, `python finance.py set-adsense ca-pub-XXXX` 명령 한 줄(또는 인게임 광고 관제 모달)로 실제 광고 송출이 즉시 활성화됩니다.
4. **📊 인게임 「광고 수익화 & 애드센스 관제 센터 모달 (`openFinanceModal`)」**
   - 누적 광고 노출수(Impressions), 보상형 상자 오픈수, `pr` 에이전트 유입 기반 월간 예상 광고 수익 시뮬레이터, 애드센스/애드핏 코드 원클릭 설정 가이드를 제공합니다.

---

## 3. 실행 명령어 (CLI Runbook)

```powershell
# 1. finance 에이전트 광고 슬롯·보상형 광고·ads.txt 상태 보고
python finance.py status

# 2. 구글 애드센스 퍼블리셔 ID 및 슬롯 설정 적용
python finance.py set-adsense --client ca-pub-0000000000000000 --slot 1234567890

# 3. 카카오 애드핏 단위 ID 설정 적용
python finance.py set-adfit --unit DAN-0000000000000000

# 4. 광고 스크립트 문법 및 전체 플랫폼 무결성 검증
python finance.py verify
```
