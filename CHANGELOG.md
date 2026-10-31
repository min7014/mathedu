# 📢 mathedu Release Notes & Product Changelog

> Generated with the `changelog-generator` skill — translating git commit history into clear, student- and teacher-friendly updates.

---

## 🚀 Version 2026.10.31 — Spatial Aurora Design, 5-Agent Ecosystem & Awesome Skills Studio

### ✨ New Features (신규 기능)
- **🛠️ 스마트 학습·교실 스튜디오 (`mathedu-skills-suite.js`)**:
  - **🎨 10대 아틀리에 테마 팩토리 (`theme-factory`)**: *Ocean Depths*, *Sunset Boulevard*, *Forest Canopy*, *Golden Hour*, *Arctic Frost*, *Midnight Galaxy* 등 10가지 전문 컬러 테마를 홈페이지에 즉시 적용할 수 있습니다.
  - **📄 맞춤 수학 시험지 PDF 인쇄 & 학습 리포트 Excel/CSV 내보내기 (`pdf` · `xlsx`)**: 현재 검색·필터링된 기출 문항이나 오답노트 문항을 A4 시험지 양식으로 즉시 인쇄하거나, 학습 성취도 표를 Excel(CSV)로 내려받을 수 있습니다.
  - **🎡 교실 발표자 & 랜덤 기출 공정 추첨기 (`raffle-winner-picker`)**: 암호학적 난수(`crypto.getRandomValues`)와 중복 방지 기능으로 수업 시간 발표 학생 번호나 오늘의 퀴즈 문항을 공정하게 추첨합니다.
  - **🖼️ 수학 기하 포스터 & 배경화면 캔버스 생성기 (`canvas-design`)**: 황금비 기하 곡선과 핵심 수능 공식, 나의 만점 게이지가 담긴 고해상도 `.png` 아트워크 포스터를 즉시 생성·저장합니다.
  - **🧮 인터랙티브 함수 그래프·극값·정적분 계산기 & WolframAlpha 연동 (`wolfram-alpha-api-automation`)**: 다항·삼각·지수 함수의 도함수 $f'(x)$, 극대·극소, 정적분 넓이를 실시간 그래프로 확인하고 원클릭으로 울프람 알파 기호 검증을 실행합니다.
- **🧠 깊은 사색과 수학적 유레카 (`DEEP EUREKA!!`) 시스템 (`mathteacher` × `gamemaker`)**:
  - 아르키메데스의 사색 통찰력 게이지(0% ➔ 100%), 폴리아 3단계 생각 징검다리 체크 바, 데카르트 인게임 모눈종이 수학 연습장, 플라톤의 시간 정지 사색 결계를 탑재했습니다.
- **📣 친구 도전장 딥링크(`?challenge=`) & AI 검색 최적화 (`pr`)**:
  - 링크 클릭만으로 해당 3D 기출 보스전이 즉시 소환되며, `llms.txt`를 통해 ChatGPT·Gemini·Perplexity 등 AI 검색엔진 추천을 최적화했습니다.
- **🎁 100% 무료 학습 기반 클린 광고 후원 상자 (`finance`)**:
  - 학습을 방해하지 않는 네이티브 슬롯과 자발적 5초 스폰서 광고 보너스 상자(`+50 XP · 기하 필살기 100% 완충`)를 지원합니다.

### 🎨 Design & UX Improvements (디자인 및 사용성 개선)
- **🌌 2026 Spatial Aurora & Glass Bento 디자인 (`designer`)**:
  - 데스크톱 와이드(`1120px` / `960px`) 반응형 벤토 그리드, 3중 방사형 오로라 메쉬 배경, 플로팅 글래스 헤더 및 캡슐 하단 독, 원클릭 글로벌 다크/라이트 모드(`toggleSiteDarkMode()`)를 전 페이지(433개 파일)에 적용했습니다.
- **🔍 스마트 자연어 문제 검색**:
  - `"9월 고3 확통 문제들"`, `"10월 미적분 30번"`, `"수1 삼각함수"` 등 자연어 질문으로 16,548문항 전체를 즉시 필터링합니다.
