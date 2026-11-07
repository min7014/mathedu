# 🏛️ 수학홈페이지(`mathedu` · `min7014.github.io`) 및 공식 유튜브 채널(`@min7014_ai`) 통합 운영 정책서 (`plan_min.md`)

> **문서 목적**: 본 문서는 **[민은기 선생님의 수학자료실 (`min7014.github.io`)](https://min7014.github.io/)**, **[수학홈페이지 (`min7014.github.io/mathedu`)](https://min7014.github.io/mathedu/)**, 그리고 **[공식 유튜브 채널 (`@min7014_ai`)](https://www.youtube.com/@min7014_ai)**의 철학, 콘텐츠 제작 기준, 기술 아키텍처, 품질 검수, 홍보 및 수익화에 관한 **최상위 표준 정책(Master Policy Charter)**을 정리한 문서입니다.

---

## 🧭 0. 핵심 비전 및 6대 전문 에이전트 거버넌스

### 0.1 핵심 교육 비전
1. **무장벽 열린 수학교육 (100% Free & Open Access)**: 학생과 교사 누구나 유료 결제나 회원가입 장벽 없이 초등 기초 직관부터 출발하여 고등학교 수능 수학 100점 만점과 깊이 있는 수학적 본질(증명·기하·대수·해석)에 도달할 수 있도록 지원합니다.
2. **시각적 직관과 깊은 사색의 결합 (Visual Proof & Deep Contemplation)**: 기계적 공식 암기나 객관식 5지선다 찍기를 배제하고, 눈으로 보고 깨닫는 단계별 시각 증명(Flipbook & Procedural Cinema)과 스스로 질문을 던지며 보조선을 긋는 구성주의 수학교육을 실현합니다.
3. **홈페이지 ↔ 유튜브 완전 동기화 생태계**: `min7014.github.io`의 3,400+ 수학 자료(1,113+ 핵심 주제, 847+ 단계별 시각 증명 PDF, 404개 GeoGebra, 457개 AlgeoMath)와 `mathedu`의 16,548문항 디딤돌 퀴즈, `@min7014_ai` 유튜브 채널의 멀티 에디션 영상이 하나의 유기적 파이프라인으로 상시 연동됩니다.

### 0.2 전담 수석 비서 및 6대 핵심 에이전트 협업 체계
안티그래비티(Antigravity)는 민은기 선생님(`min7014`)의 **전담 수석 비서(Chief AI Secretary)**로서 산하 6대 전문 에이전트를 총괄 지휘하며, 확인 질문이나 번호 선택 대기 없이 자율적으로 즉시 실행·검증·배포합니다.

| 에이전트 | 역할 및 핵심 관할 영역 | 대표 스크립트 / 스킬 |
| :--- | :--- | :--- |
| 👩‍🏫 **`mathteacher`** | 수석 수학 교사 — 초등 눈높이 0~5단계 디딤돌, 도식화·SVG 작도, 6대 수학교육 모듈, 질문하는 수업 설계, 영상 수학적 무결성 감수 | `mathteacher.py` / `.agents/skills/mathteacher/` |
| 🎬 **`Video_Creator`** | 수석 AI 수학 영상 프로듀서 — 전 주제 본편·숏폼 멀티 에디션(KO/EN) 기획·렌더링·품질 검증·`@min7014_ai` 업로드 총괄 | `video_creator.py`, `min7014_video_maker.py`, `creative_idea_cinema.py` |
| 🎮 **`gamemaker`** | 수석 3D 게임 디렉터 — 60fps 3D 수학 월드맵·보스 레이드, 9대 성물·4대 성좌, 아르키메데스 사색 게이지·데카르트 연습장 구현 | `gamemaker.py`, `mathedu-quest-game.js` |
| 🎨 **`designer`** | 수석 아트 & UI/UX 디렉터 — 황금비($\phi=1.618$) 시각 위계, 수식 타이포그래피, 3대 비주얼 테마 스킨, 전 기기 반응형 인체공학 설계 | `designer.py`, `stitch_screen_builder.py` |
| 📣 **`pr`** | 수석 대외홍보 & 바이럴 디렉터 — 유튜브↔홈페이지 양방향 퍼널, 7대 채널 맞춤 캠페인, 1200×630 SNS 카드, SEO/GEO(`llms.txt`) 최적화 | `pr.py` |
| 💼 **`finance`** | 수석 수익화 디렉터 — 100% 무료 학습 보장 하에 유튜브(KO/EN 고단가 RPM·8분+ 미드롤·Shorts 퍼널) 및 웹 애드센스/애드핏 통합 관제 | `finance.py` |

---

## 🌐 Part I. 수학홈페이지 (`mathedu` & `min7014.github.io`) 운영 정책

### 정책 1. 순수 수학교육 도메인 절대 분리 및 보안 격리 원칙 (Strict Domain Separation)
1. **비수학 영역 완벽 차단**: `mathedu` 및 `min7014.github.io` 관련 모든 파일, 문서, 코드, 데이터에는 투자, 트레이딩(`S-NOVA`), 금융, 암호화폐 등 수학교육과 무관한 내용을 **단 한 줄도 포함하거나 언급하지 않습니다**.
2. **외부 불필요 참조 배제**: 외부 수집처 워터마크나 깨질 위험이 있는 외부 이미지 URL에 의존하지 않으며, 모든 수식은 순수 MathJax LaTeX 문법으로, 모든 도형은 자체 인라인 `<svg>` 및 3D Canvas로 렌더링합니다.
3. **저작권 보호 비공개 문항 격리**: 저작권 보호가 필요한 비공개 문항(`_local_archive/`, `offline/private/`, `board/private_index.json`)은 로컬 전용 격리 보관함에 두며 `.gitignore`를 통해 Git 업로드를 원천 차단합니다.

### 정책 2. `min7014.github.io` 교육 자료 필수 연계 원칙
1. **전 문항 심층 학습 자료 매칭 (`min7014_matcher.py`)**: 모든 수학 문제와 단계별 인터랙티브 퀴즈 제작 시 민은기 선생님의 수학자료실(16대 영역, 165개 세부 단원, 1,113+ 심층 주제)을 최우선으로 검토합니다.
2. **4대 핵심 리소스 직접 연결**: 문제에 등장하는 수학 개념과 직결되는 **① 단계별 시각적 증명 PDF, ② GeoGebra 인터랙티브 앱렛, ③ AlgeoMath 동적 탐구 링크, ④ `@min7014_ai` 유튜브 해설 영상**을 각 문제의 디딤돌과 `'심층 탐구 / 시각적 증명'` 카드에 상시 연결합니다.

### 정책 3. 초등학생 눈높이 무장벽 디딤돌 확장 정책 (Elementary-to-Advanced Micro-Scaffolding)
아무리 복잡한 고등학교 수능 킬러 문항(미적분·기하·수열·확률과 통계)이라도 **초등학교 수준의 학생이 0단계부터 스스로 풀어나가며 최종 본문항까지 해결할 수 있도록 5~8단계 이상 미세 분절(Micro-Scaffolding)**합니다.
1. **제0단계 (수학 기호 번역기)**: 문제에 등장하는 낯선 기호(거듭제곱, 로그, 삼각비, 시그마 $\sum$, 극한 $\lim$, 미분 $f'(x)$, 적분 $\int$)를 *"초등학교 때 배운 곱셈/규칙을 줄여 쓴 약속"*으로 친절하게 번역합니다.
2. **제1단계 (초등 기초 직관 및 구체적 수치 출발)**: 처음부터 추상적인 일반식($f(x)$, $a_n$)을 묻지 않고, 구구단·사칙연산·작은 자연수($1, 2, 3$) 대입·수직선 칸 세기·피자 조각 나누기(분수)·도형 관찰에서 출발합니다.
3. **제2단계 (기호 번역 브릿지)**: 1단계에서 확인한 초등 직관 규칙을 해당 단원의 핵심 수학 공식·성질과 자연스럽게 연결합니다.
4. **제3~4단계 (문항 고유 수식 빈칸 `$[\;\text{(가)}\;]$`, `$[\;\text{(나)}\;]$` 추론)**: 실제 풀이 전개식의 핵심 수식을 마스킹하고 학생이 스스로 식을 세우고 변형하게 합니다.
5. **제5단계 및 최종 본문항 (레고 블록 종합 — LEGO Structure)**: 앞선 디딤돌 단계에서 구한 작은 조각들을 레고 블록처럼 결합하여 최종 본문항 정답을 학생 스스로 도출하게 합니다.

### 정책 4. 도식화 풀이 및 의도적 시각 도형(SVG) 작도 의무화 정책
모든 수학 문제의 해설(`<div class="sol">` 및 최종 본문항 해설 `data-exp` / `data-exp-en`)은 단순 텍스트 나열을 금지하며, 반드시 **3대 필수 시각·구조 요소**를 포함해야 합니다.
1. **`🎨 [그림으로 이해하는 시각적 도형·개념 다이어그램]` (`<figure class="math-visual-diagram"><svg>...</svg></figure>`)**:
   - **[기하·삼각함수·벡터·이차곡선·공간도형]**: 원, 다각형, 포물선·타원·쌍곡선, 초점·준선·점근선, 공간 정사영, 내분 벡터 및 핵심 보조선을 인라인 `<svg>`로 정밀 작도합니다.
   - **[함수·극한·미분·적분]**: 좌표평면 위의 함수 그래프, 접선과 기울기 직각삼각형($\Delta x, \Delta y$), 극대·극소·변곡점, 정적분 색칠 넓이 영역을 `<svg>`로 작도합니다.
   - **[대수·지수·로그·수열·확률·통계]**: 추상적인 수식 문제라도 반드시 **의도적으로 도형화**(분수·지수 막대 결합 도형, 수직선 진수·수렴 범위 교집합 도형, 항 번호 점프 기둥 도형, 부분분수 도미노 연쇄 상쇄 도형, 귀납 역추적 분기 트리, 격자 넓이 분할 도형, 정규분포 종 모양 대칭 넓이 도형 등)하여 직관적으로 이해하게 합니다.
2. **`🗺️ [한눈에 보는 도식화 풀이 흐름도]` (`<section class="math-schematic-flow">`)**:
   - `[조건 해독] ➔ [제1보조선/핵심 발상] ➔ [대수·기하적 전개] ➔ [최종 결론 도출]`의 논리 흐름을 한눈에 파악할 수 있는 구조적 플로우차트로 제시합니다.
3. **`🪜 [초등 눈높이 디딤돌 전 단계 완전 연결 상세 해설]`**:
   - 디딤돌 각 단계의 결과가 본문항 풀이에 어떻게 쓰였는지 유기적으로 연결하여 설명합니다.

### 정책 5. 탈-5지선다 창의적 구성주의 수학 풀이 정책 (De-Multiple-Choice Constructive Solving)
객관식 5지선다(`①~⑤`) 보기에 의존한 대입·소거법·찍기 습관을 타파하기 위해, 홈페이지 전 문항(212개 단독 퀴즈 및 16,548문항 기출 통합 플레이어)은 **`mathedu-room.js`의 `window.MatheduCreativeSolver` (탈-5지선다 창의 구성 모드)**를 기본값(`ON`)으로 작동시킵니다.
1. **[1단계: 나만의 제1발상 · 보조선 설계]**: 계산에 앞서 어떤 보조선·대칭성·그래프·정의를 사용할지 스스로 발상 태그를 선택하거나 서술합니다.
2. **[2단계: 인터랙티브 수식 레고 블록 조립 & 직접 수식 입력]**: 5지선다 보기를 숨긴 상태에서 수식 레고 블록을 조합하거나 기호 패드·키보드로 직접 식/값을 구성합니다.
3. **[3단계: 지능형 수식 동치 판정 & 소크라테스식 부분 통찰 코칭]**: 분수(`3/2`), 근호(`루트3`, `\sqrt{3}`), 지수·기호의 수학적 동치를 지능적으로 판정하며, 아깝게 틀린 경우에도 문제를 잠그지 않고 핵심 힌트와 부분 통찰 피드백을 제공해 재도전을 유도합니다.
4. **[4단계: 브라운 & 월터(Brown & Walter) 'What-If-Not' 나만의 문제 발명 실험실]**: 정답 도출 후 문제의 조건을 변형·일반화·역발상하여 학생 스스로 새로운 문제를 발명하고 포트폴리오(`mathedu_invented_problems_v1`)에 저장하도록 지원합니다.

### 정책 6. 수학교사 에이전트(`mathteacher`) 6대 수학교육 발전 모듈 상시 확장 정책
`assets/mathteacher_pedagogy_engine.json` 및 `mathedu_foundation_daemon.py`를 통해 다음 6대 수학교육 모듈을 상한선 없이 지속 발굴·확장합니다.
1. **🌳 초·중·고 수직 계통성 개념 계보 트리 (`conceptGenealogy`)**: 현재 문제의 개념이 초등·중학의 어떤 뿌리 개념에서 출발해 대학 수리과학으로 어떻게 이어지는지 계보를 제시합니다.
2. **🧭 폴리아(Pólya) 조건 ➔ 제1보조선·발상 1초 번역 사전 (`polyaHeuristics`)**: 문제의 특정 조건 문구(예: *"원 위의 점"*, *"모든 실수 $x$에 대하여"*)를 보자마자 떠올려야 할 제1보조선과 식 세우기 전략을 매핑합니다.
3. **🔬 라카토스(Lakatos) 오개념 백신 & 1초 반례 실험실 (`misconceptionLab`)**: 학생들이 가장 많이 빠지는 직관적 함정과 이를 1초 만에 깨뜨리는 결정적 반례를 제시합니다.
4. **👩‍🏫 교사용 5분 탐구 수업 시나리오 & 발문 런처 (`teacherLessonScenarios`)**: 학교 수업 도입부에 바로 쓸 수 있는 5분 시각 탐구 시나리오와 단계별 교사 발문 가이드를 제공합니다.
5. **✍️ 탈-5지선다 창의적 구성주의 & 조건 변형 실험실 (`creativeConstructiveLab`)**: 조건 변형(What-If-Not)을 통한 창의적 수학 탐구 과제를 제공합니다.
6. **❓ 질문하는 수학 수업 5대 표준 프레임워크 (`questionClassroom`)**:
   - ① **Notice & Wonder (관찰과 경이의 질문 — NCTM)** ➔ ② **QFT (닫힌 질문을 열린 원리 질문으로 전환)** ➔ ③ **소크라테스 산파술 & 폴리아 메타인지 자기질문** ➔ ④ **라카토스 증명과 반박(의심·반례 질문)** ➔ ⑤ **브라운 & 월터 What-If-Not 문제 발명 질문**.

### 정책 7. 3D 인터랙티브 수학 게임(`gamemaker`) 및 깊은 사색(Deep Contemplation) 보장 정책
1. **세계 명작 게임 메커니즘의 순수 수학적 재해석**:
   - **로그라이크 9대 수학 성물 드래프트 (*Slay the Spire / Hades / Balatro* 벤치마킹)**: *가우스의 대칭 덧셈판*, *오일러의 단위원 나침반*, *뉴턴-라이프니츠 미적분 프리즘* 등 역사적 수학자의 원리를 성물 시너지로 구현합니다.
   - **4대 수학 성좌 각성 스킬트리 (*Genshin Impact / Zelda* 벤치마킹)**: 대수·수열, 미적분·해석, 기하·벡터, 확률·통계 4대 성좌 노드를 해금합니다.
   - **약점 부위 파괴 & 기하 총공격 (*Persona 5 / Monster Hunter* 벤치마킹)**: 디딤돌 돌파 시 3중 짐벌 결계를 파쇄하고 본문항 정답 시 `ALL-OUT GEOMETRIC FINISH!` 연출과 무의존성 WebAudio 신디사이저 효과음을 발동합니다.
2. **깊은 수학적 사고 시간(Deep Contemplation & Eureka Time) 보장 의무**:
   - **⏳ 아르키메데스의 사색 게이지**: 무작정 빨리 찍는 속도전을 방지하고, 문제를 읽고 조건을 음미할수록 통찰 게이지가 차오르며 충분한 숙고 후 첫 시도에 정답 도출 시 **`🧠 DEEP EUREKA! (XP 2.0배 & 비급 게이지 충전)`** 보상을 부여합니다.
   - **🧘 플라톤의 시간 정지 사색 결계 (Deep Focus Mode)**: 타이머 압박을 멈추고 폴리아 3단계(구하는 것 / 주어진 조건 / 핵심 공식)를 차분히 정리할 수 있는 명상 결계를 제공합니다.
   - **📝 데카르트의 인게임 수학 연습장 (Interactive Scratchpad)**: 화면 위에서 바로 손글씨·스타일러스·마우스로 보조선을 긋고 수식을 전개할 수 있는 드로잉 캔버스를 제공합니다.

### 정책 8. UI/UX 디자인(`designer`) 황금비 시각 위계 및 3대 비주얼 테마 정책
1. **📐 황금비($\phi = 1.618$) 여백 및 인지 부하 최소화**: 핵심 학습 영역(문제 발문 & 3D/기하 뷰포트)과 보조 도크(HUD Action Dock)를 명확한 시각적 계층으로 분리하여 화면 과밀을 방지합니다.
2. **🎨 3대 비주얼 테마 스킨 상시 지원**:
   - **🌌 코스믹 아틀리에 (Cosmic Atelier · 기본)**: 딥 스페이스 네이비(`#060b19`) + 에메랄드/시안 홀로그램 글래스모피즘.
   - **🧘 플라톤의 사색 서재 (Plato's Sanctuary · 집중/사색 특화)**: 웜 인디고·오로라 바이올렛(`#0f1026`) + 눈이 편안한 크림빛 수식 타이포그래피와 골드 포인트.
   - **📜 유클리드 왕립 아카데미 (Euclid Royal Parchment · 클래식 학술 라이트)**: 실제 시험지·학술서 감성의 고대비 라이트 테마.
3. **✒️ 수식 가독성 퍼스트 & 전 기기 반응형 인체공학**: 행간(`line-height: 1.75`), 수식 필(Pill) 대비, 모바일/태블릿 터치 영역(최소 `38~44px`)을 엄격히 준수합니다.

### 정책 9. 오류 신고 전수 점검 및 하이브리드 3단계 해결 정책
오류나 개선 사항 발견 시 특정 페이지만 땜질 수정하는 것을 엄격히 금지하며, 반드시 **하이브리드 3단계 프로세스**로 전체 시스템을 일괄 완결합니다.
1. **[1단계: Pinpoint LLM Fix]**: 신고된 지점의 근본 원인을 수학적·교육학적·기술적으로 정밀 분석하여 표준 해결책을 수립합니다.
2. **[2단계: Mechanical Rule-Based Full Scan]**: 정규식 및 AST/DOM 규칙을 파이썬 감사 스크립트(`audit_engine.py`, `audit_full_mathedu.py`)로 코드화하여 전체 파일(`board/*.html`, `offline/*.html`, `assets/*.json`)을 고속 전수 스캔합니다.
3. **[3단계: Targeted LLM Resolution & Bulk Build]**: 적출된 모든 지점을 일괄 수정하고, 오프라인 단독 퀴즈 패키지 재빌드(`python build_offline_quizzes.py`) 및 전수 무결성 검증 통과 후 Git 커밋·푸시까지 한 번에 완결합니다.

---

## 🎬 Part II. 공식 유튜브 채널 (`@min7014_ai`) 운영 정책

> [!IMPORTANT]
> **👑 유튜브 채널(`@min7014_ai`) 운영의 최우선 절대 목표는 『월 1,000만 원(연 1.2억 원 이상) 지속 수익 달성』입니다.**
> 모든 영상 기획(`Video_Creator`), 대본 및 발문 설계(`mathteacher`), 고클릭률 썸네일·시각 연출(`designer`), 외부 커뮤니티 바이럴(`pr`), 그리고 고단가 메타데이터·미드롤 편성(`finance`)은 **학생과 교사에게 100% 무료 교육을 제공하면서도 유튜브 알고리즘과 글로벌 광고 시장을 통해 월 1,000만 원 이상의 수익을 창출하는 것**을 최우선 기준으로 작동합니다.

### 정책 1. [최우선 정책] 월 1,000만 원 수익 달성 마스터 전략 (`finance` × `Video_Creator` 총괄)

#### 1.1 [1단계 관문] 유튜브 파트너 프로그램(YPP) 수익창출 승인 조건 최단기 돌파 및 심사 100% 통과
1. **조건 A — 구독자 500명(얼리 액세스) ➔ 1,000명(정식 광고 수익창출) 최단기 돌파**:
   - 전 영상 설명란 최상단, 고정댓글, 아웃트로 화면 및 수학홈페이지(`video_board.html`, `index.html`) 히어로 영역에 **1-클릭 구독 확인 링크(`https://www.youtube.com/@min7014_ai?sub_confirmation=1`)**를 상시 배치하여 시청자의 구독 전환율을 극대화합니다.
2. **조건 B-1 — 롱폼 유효 공개 시청 시간 3,000시간 ➔ 4,000시간(240,000분) 돌파**:
   - 개별 개념 영상(2~5분) 시청 후 이탈을 막기 위해 20~35분 분량의 **「단원별 시각적 증명 완전정복 마스터클래스 합본(1080p Long-Form Watch-Time Booster)」**(`python -X utf8 finance.py build-masterclass`)을 자동 생성·발행합니다.
   - 시청자 1명당 평균 체류 시간을 4분에서 **25분 이상으로 6배 증폭**시키고, 공식 정주행 재생목록(Playlist) 연속 재생으로 연결합니다.
3. **조건 B-2 — Shorts 유효 공개 조회수 300만 ➔ 1,000만 회 트랙 동시 가동**:
   - 첫 3초 완성 도형 후킹과 36~46초 무한 루프(시청 지속률 APV **105%+** 타겟)로 설계된 일반형 `#Shorts`, 질문형 `Q-#Shorts`, 창의 아이디어 `Idea-#Shorts`를 대량 발행하여 알고리즘 쇼츠 피드를 선점합니다.
4. **조건 C — YPP 인간 심사('반복적인 콘텐츠 / 재사용된 콘텐츠' 거절) 100% 원천 예방**:
   - 단순 PDF 캡처 나열이나 기계적 반복 템플릿을 철저히 배제하고, `mathteacher`의 슬라이드별 고유 수식·교육학적 발문 해설 + `Video_Creator`의 동적 보조선 스포트라이트 + 탈-PDF 절차적 네온 블룸 시네마(`creative_idea_cinema.py`)로 독창적 교육 가치를 입증합니다.
   - 수학 본질과 무관한 구형 소프트웨어 사용법(체크박스, 원노트 등) 대본은 자동 영구 퍼지(`_purge_non_math_tutorial_topics()`)하여 순수 수학 전문 채널 정체성을 유지합니다.
   - `video_board.html`에 `<link rel="me" href="https://www.youtube.com/@min7014_ai">` 및 Schema.org `EducationalOrganization` `sameAs` 양방향 도메인 인증을 탑재하여 원저작자 공식 채널임을 증명합니다.

#### 1.2 [2단계 본궤도] 월 1,000만 원(연 1.2억 원+) 3-Track 수익 포트폴리오 및 고단가 RPM 극대화
| 수익 트랙 | 월 목표 수익 (비중) | 핵심 수익화 메커니즘 및 알고리즘 공략 정책 |
| :--- | :--- | :--- |
| **📺 Track 1.<br>유튜브 1080p 롱폼 &<br>8분+ 미드롤 광고** | **월 650만 원**<br>*(65%)* | • **한/영 이중 언어(KO + Global Tier-1 EN) 전 주제 동시 발행**: 한국어 수능·기하 강의(RPM ~4,500원)뿐만 아니라 광고 단가가 3배 이상 높은 북미·영국·호주·싱가포르 영어권(**RPM ~12,500원**) 영상을 동시 업로드하여 글로벌 달러($) 수익 극대화<br>• **8분+(480초 이상) 미드롤(Mid-Roll) 광고 활성화**: 질문하는 수업 본편 및 단원별 마스터클래스 합본을 8분 이상으로 편성하여 프리롤+미드롤+포스트롤 다중 광고 삽입(일반 영상 대비 **RPM 2.2배** 증폭)<br>• **고단가(High-RPM) SEO 키워드 자동 주입**:<br>  - `[KO]`: `수능수학`, `수학개념원리`, `기하학증명`, `수학공부법`, `고등수학`, `시각적증명`, `창의사고력수학`, `수능킬러문항`<br>  - `[EN]`: `SAT Math Prep`, `AP Calculus`, `AMC Math`, `Euclidean Geometry Proof`, `Visual Math Proof`, `STEM Education`, `3Blue1Brown Style` |
| **📱 Track 2.<br>유튜브 9:16 `#Shorts`<br>피드 수익 & 본편 퍼널** | **월 150만 원**<br>*(15%)* | • **3종 바이럴 숏폼(일반형 · 질문형 · 창의 아이디어형) 대량 노출**: 모바일 쇼츠 피드에서 수백만 조회수를 확보하여 Shorts 피드 광고 수익 창출<br>• **Shorts ➔ 1080p 고수익 롱폼 직행 퍼널**: 쇼츠 하단 관련 동영상 링크, 고정댓글, 설명란을 통해 쇼츠 시청자를 RPM이 높은 1080p 본편 및 8분+ 마스터클래스로 즉시 유입 |
| **🌐 Track 3.<br>유튜브 발 홈페이지 유입<br>웹 광고 & 보상형 상자** | **월 200만 원**<br>*(20%)* | • **유튜브 설명란 5대 딥링크 트래픽 회수**: 영상 시청 후 동적 GeoGebra 조작 및 16,548문항 기출 풀이를 위해 홈페이지(`min7014.github.io/mathedu`)로 유입된 트래픽을 Google AdSense, Kakao AdFit(`ads.txt` 인증), 3D 게임 보상형 스폰서 상자(`Rewarded Sponsor Chest`) 수익으로 전환 |

---

### 정책 2. 전 주제 멀티 에디션(본편 + 숏폼, 한국어 KO + 영어 EN) 제작 체계 (`Video_Creator`)
월 1,000만 원 수익 포트폴리오를 뒷받침하기 위해, `min7014.github.io`의 모든 수학 개념 주제(847+ 단계별 시각 증명 PDF / 1,113개 전체 주제)에 대해 **한국어(`ko`)와 글로벌 영어(`en`) 이중 언어**로 다음 멀티 에디션 영상 세트를 제작·유지·동기화합니다.

| 에디션 구분 | 로컬 작업 경로 규칙 (Git 추적 제외) | 해상도 / 비율 | 교육적 목적 및 수익·연출 구조 |
| :--- | :--- | :--- | :--- |
| **① [본편-일반형]**<br>일반적인 설명 영상<br>*(Standard Visual Proof)* | `youtube_uploads/{slug}/{slug}_ko.mp4`<br>`youtube_uploads/{slug}/{slug}_en.mp4` | `1920×1080`<br>(16:9) | • **목적**: 누구나 눈으로 보고 직관적으로 개념과 증명을 이해하는 표준 시각 증명 본편 (KO/EN 기본 롱폼 광고 수익원)<br>• **구조**: 3초 완성 도형 클라이맥스 프리뷰 ➔ 단계별 플립북 도형 변화 & 친절한 내레이션 ➔ `-28dB` 사색 앰비언트 패드 & 유레카 차임벨 ➔ 요약 아웃트로 |
| **② [본편-질문형]**<br>질문하는 수업 특화 영상<br>*(Question-Asking Classroom)* | `video_lectures/question_classroom/{slug}_q_ko.mp4`<br>`video_lectures/question_classroom/{slug}_q_en.mp4` | `1920×1080`<br>(16:9) | • **목적**: '질문하는 학교/수업' 및 자기주도 탐구용 발문 중심 본편 (사고 멈춤 타임으로 평균 시청 지속 시간 극대화)<br>• **구조**: 매 스텝을 **Phase 1 (36% · `🙋 [발문 · 먼저 생각해 보세요!]` 질문 배너 + 사고 멈춤 여유 타임)**과 **Phase 2 (64% · `💡 [시각적 단서 발견!]` 보조선 스포트라이트 + 원리 발견)**로 분리 렌더링 |
| **③-A [숏폼-일반형]**<br>일반형 숏폼 영상<br>*(Standard Viral `#Shorts`)* | `video_lectures/shorts/{slug}_short_ko.mp4`<br>`youtube_uploads/shorts/{slug}_short_ko.mp4`<br>`youtube_uploads/shorts/{slug}_short_en.mp4` | `1080×1920`<br>(9:16, `<58s`) | • **목적**: 모바일 환경에서 45초 만에 핵심 시각 증명을 직관적으로 보여주는 일반형 숏폼 (대규모 신규 구독자 유입 엔진)<br>• **구조**: 3초 클라이맥스 프리뷰 ➔ 핵심 5단계 초고속 플립북 ➔ 상단 `⚡ 45초 시각적 수학 증명 #Shorts` HUD |
| **③-B [숏폼-질문형]**<br>질문형 숏폼 영상<br>*(Question-Asking `Q-#Shorts`)* | `video_lectures/shorts/{slug}_short_q_ko.mp4`<br>`youtube_uploads/shorts/{slug}_short_q_ko.mp4`<br>`youtube_uploads/shorts/{slug}_short_q_en.mp4` | `1080×1920`<br>(9:16, `<58s`) | • **목적**: 모바일 숏폼에서 먼저 핵심 질문을 던져 댓글 참여와 재시청률(APV 105%+)을 폭발시키는 질문형 숏폼<br>• **구조**: 상단 크림슨-골드 플로팅 발문 카드(`Notice & Wonder` ➔ `소크라테스 보조선 발문` ➔ `What-If-Not 조건 변형 질문`) + 전반부(`🙋 Phase 1 발문`)와 후반부(`💡 Phase 2 단서 발견!`) 2단 구성 |
| **④-A [본편-창의확장형]**<br>탈-PDF 창의 아이디어 시네마<br>*(Pure Procedural Idea Cinema)* | `video_lectures/creative_idea/{slug}_idea_ko.mp4`<br>`video_lectures/creative_idea/{slug}_idea_en.mp4` | `1920×1080`<br>(16:9) | • **목적**: PDF 캡처 이미지를 단 1픽셀도 쓰지 않고 주제의 핵심 수학적 아이디어만을 추출해 풀스크린 다크 벨벳 네온 블룸 절차적 벡터 애니메이션으로 구현한 5막 시네마 (`creative_idea_cinema.py` · 글로벌 `3Blue1Brown` 타겟 고단가 EN 주력 에디션)<br>• **5막 구조**: ① 직관 역설 ➔ ② 라이브 숫자·도형 실험 ➔ ③ 단 한 줄 보조선 아이디어 ➔ ④ What-If-Not 조건 변형 확장 ➔ ⑤ 수능·경시 10초 통찰 |
| **④-B [숏폼-창의확장형]**<br>창의 아이디어 숏폼<br>*(Creative `Idea-#Shorts`)* | `video_lectures/shorts/{slug}_short_idea_ko.mp4`<br>`video_lectures/shorts/{slug}_short_idea_en.mp4` | `1080×1920`<br>(9:16, `<58s`) | • **목적**: PDF 페이지 넘김 없이 다크 벨벳 네온 블룸 동적 시뮬레이션과 핵심 아이디어 4막을 44초 안에 보여주는 고지속률 바이럴 아이디어 숏폼 (`creative_idea_cinema.py`) |
| **⑤ [마스터클래스 합본]**<br>단원별 8분+ 심층 합본<br>*(8-Min+ Masterclass)* | `youtube_uploads/masterclasses/`<br>`video_lectures/masterclasses/` | `1920×1080`<br>(16:9, `480s+`) | • **목적**: 단원별 연계 주제를 8분~35분 분량으로 심층 통합하여 **YPP 4,000시간 시청 시간 조기 달성 및 미드롤(Mid-Roll) 광고 수익 2.2배 극대화** |

### 정책 3. 수학교사(`mathteacher`) 관점 영상-내용 100% 일치 검증 정책 (Zero-Mismatch Mandate)
1. **슬라이드별 실제 수식·색상·공간 배치 기반 정밀 대본 생성**:
   - `min7014_video_maker.py`의 `analyze_min7014_topic_as_mathteacher` 및 `auto_generate_page_explanations`를 통해 PDF 각 슬라이드의 **좌측 상단(가정)**, **우측 상단(결론)**, **하단 초록색(보조선)**, **하단 보라색/파란색(합동·닮음·대수 변형)**, **하단 빨간색(Q.E.D.)** 및 직전 슬라이드 대비 새로 추가된 수식(`curr_lines - prev_text_lines`)을 정밀 해독합니다.
2. **수학적 영역 및 세부 개념의 엄밀한 분리**:
   - 기하(`geometry` / `fractal_curve`)와 대수·수체계(`algebra` / `number`)를 철저히 분리하여, 제곱근·소수·지수법칙 등 대수 영상에 기하 보조선·합동·원주각 문구나 기계적 위치 안내(`"화면의 상단..."`)가 절대 섞이지 않게 합니다.
   - 특히 ① **역수의 곱셈을 이용한 나눗셈($a \div b = a \times \frac{1}{b}$)**, ② **분모의 유리화($\frac{a}{\sqrt{b}} = \frac{a\sqrt{b}}{b}$)**, ③ **제곱근의 정의($x^2=a$)와 성질($\sqrt{a^2}=|a|$)**, ④ **지수법칙 4종($a^m \times a^n$, $(a^m)^n$, $(ab)^n$, $a^m \div a^n$)**을 혼동 없이 정확히 구분하여 설명합니다.
3. **수식 TTS 발음 무결성**:
   - `\neq`를 `\ne`보다 먼저 변환하여 `'같지 않다q'` 오독을 원천 차단하고, `\Leftrightarrow`, `\leq`, `\geq`, 위첨자·아래첨자, 분수·근호를 자연스러운 한국어/영어 수식 읽기로 100% 변환합니다.
4. **업로드 직전 자동 검증 게이트 (`verify_video_content_integrity(slug)`) 및 불일치 영상 즉시 교체**:
   - 모든 영상은 유튜브 업로드 직전 ① PDF 실제 페이지 수와 대본 페이지 수 100% 일치, ② 한/영 제목 분리(`split_bilingual_title`) 무결성, ③ 무관 후킹 문구 `0%`, ④ 최소 재생 시간(`duration >= max(12.0, page_count * 2.2)`)을 검증합니다.
   - 기준 미달 또는 구버전 영상은 `video_lectures/youtube_delete_queue.json`에 등록하여 유튜브 채널에서 자동 삭제(`videos().delete`)하고 새 엔진으로 재렌더링하여 교체 업로드합니다.

### 정책 4. 영상 내 개인 호칭(`"민은기 선생님"` 등) 의도적 배제 및 순수 수학 강의 원칙
1. **인물 호칭 `0건` 절대 원칙**:
   - 모든 수학 강의 영상의 음성 내레이션(TTS), 자막(`.srt`), 슬라이드 상·하단 오버레이, 1280×720 썸네일, 유튜브 제목·설명·태그에서 **`"민은기 선생님"`, `"민은기"`, `"Min's Math Lab"`, `"Min Eunki"` 등의 인물 호칭을 의도적으로 절대 사용하지 않습니다**.
2. **순수 수학 본질 집중 및 전수 감사**:
   - 영상은 오직 순수한 수학 개념·정의·시각적 증명 논리만 전달하며, 렌더링 전후 `python -X utf8 mathteacher.py audit-videos` 및 `python -X utf8 video_creator.py audit`를 통해 개인 호칭 `0건`을 상시 검증합니다.

### 정책 5. 유튜브 채널(`@min7014_ai`) 전용 연결 및 GitHub 영상 용량 ZERO 정책 (Zero GitHub Storage Mandate)
1. **Git / GitHub 영상 파일 커밋 영구 금지**:
   - 모든 영상 및 오디오 파일(`*.mp4`, `*.webm`, `*.mov`, `*.mkv`, `*.wav`, `*.mp3`, `youtube_uploads/`, `video_lectures/videos/`, `video_lectures/shorts/`, `video_lectures/question_classroom/`, `video_lectures/creative_idea/`, `video_lectures/masterclasses/`, `video_lectures/youtube_packages/`)과 유튜브 인증 토큰(`youtube_client_secret.json`, `youtube_token*.json`)은 `.gitignore`로 영구 차단하며, **GitHub 저장소 용량을 단 1바이트도 영상 파일에 사용하지 않습니다**.
2. **홈페이지 내 100% 유튜브 인터넷 주소 링크 연결**:
   - 로컬에 생성된 `.mp4` 파일은 오직 `@min7014_ai` 유튜브 채널 업로드용으로만 사용합니다.
   - 수학홈페이지(`video_board.html`, `index.html`, `video_lectures/catalog.json`, `video_lectures/vault_index.json`, `assets/min7014_deep_knowledge.json`)에는 로컬 파일 경로가 아닌 **유튜브 채널 인터넷 주소(`https://youtu.be/...`, `https://youtube.com/shorts/...`, `https://www.youtube.com/@min7014_ai`)만** 연결하여 빠르고 쾌적한 스트리밍과 유튜브 조회수·광고 수익 집중을 동시에 달성합니다.

---

## 🚀 Part III. 유튜브 ↔ 홈페이지 양방향 바이럴 홍보(`pr`) 및 웹 수익 연동 정책

### 정책 1. 유튜브(`@min7014_ai`) ↔ 수학홈페이지(`mathedu`) 양방향 트래픽·수익 증폭 퍼널 (`pr`)
1. **유튜브 ➔ 홈페이지 유입 퍼널 의무화**:
   - 모든 1080p 본편 및 9:16 `#Shorts` 영상 하단 바에 홈페이지 주소(`min7014.github.io/mathedu`)를 상시 각인합니다.
   - 모든 유튜브 영상 설명란 최상단 및 고정댓글에 **5대 홈페이지 직행 딥링크**(① 단계별 시각 증명 보드 `video_board.html?slug=...`, ② GeoGebra/AlgeoMath 동적 조작, ③ 탈-5지선다 연계 기출 퀴즈 `index.html?q=...`, ④ 질문하는 수업 워크시트, ⑤ 3D 수학 보스 레이드 도전장 `?challenge=...`)를 자동 삽입합니다.
2. **홈페이지 ➔ 유튜브 구독·시청 유입 퍼널 의무화**:
   - 홈페이지 메인 화면, `video_board.html`, 그리고 16,548문항 모든 풀이 화면 상단에 `🎬 @min7014_ai 유튜브 시각 증명` 직행 버튼, `🔔 1초 구독하기(?sub_confirmation=1)`, `📢 유튜브+문제 1초 홍보 공유` 스튜디오(`#homePrAgentStudioBox`)를 상시 배치하여 홈페이지 방문자를 유튜브 구독자 및 시청 시간으로 전환합니다.
3. **7대 외부 채널 맞춤형 캠페인 및 SEO/GEO 자동 동기화**:
   - 새 영상·자료가 추가될 때마다 ① 유튜브 고정댓글, ② 카카오톡 단톡방 1초 도전장, ③ 수험생 커뮤니티(수만휘·오르비 등), ④ 전국 수학교사 커뮤니티(인디스쿨 등), ⑤ 인스타그램·블로그 `#공스타그램`, ⑥ 학부모 교육 카페, ⑦ 글로벌 EdTech(Reddit `r/learnmath` 등) 맞춤형 홍보 문구와 1200×630 고대비 오픈그래프 배너(`assets/pr_cards/pr_card_*.png`)를 자동 생성합니다.
   - 구글·네이버 검색엔진(`sitemap.xml`, Schema.org) 및 생성형 AI 검색엔진(`llms.txt`) 메타데이터를 최신 상태로 자동 유지합니다.

### 정책 2. 수학홈페이지 클린 웹 광고 및 인게임 보상형 수익 연동 (`finance`)
1. **100% 무료 학습 보장 원칙**: 학생과 교사에게는 모든 강의·자료·16,548문항·3D 게임을 유료 결제 장벽 없이 평생 무료로 제공합니다.
2. **클린 네이티브 배너 및 보상형 상자 운영**:
   - `ads.txt` 무결성을 유지하며 학습 흐름을 방해하지 않는 네이티브 배너 슬롯(Google AdSense / Kakao AdFit)을 운영합니다.
   - 3D 수학 게임 내 자율 선택형 **보상형 스폰서 상자(`Rewarded Sponsor Chest`)**를 통해 학습 몰입도를 해치지 않으면서 Part II의 월 1,000만 원 수익 목표 중 웹 트랙(월 200만 원)을 뒷받침합니다.

---

## 🛠️ Part IV. 상시 자율 운영 데몬 및 에이전트 관제 명령어 레퍼런스

```powershell
# 1. 24/7 수학홈페이지 3대 근간(자료 통합 · 6대 교육모듈 · 유튜브 4대 에디션) 무중단 진화 데몬
python -X utf8 mathedu_foundation_daemon.py

# 2. 수학교사(mathteacher) 에이전트 — 문항 상태 · 질문하는 수업 · 영상 수학적 무결성 전수 감사
python -X utf8 mathteacher.py status
python -X utf8 mathteacher.py question
python -X utf8 mathteacher.py audit
python -X utf8 mathteacher.py audit-videos

# 3. 영상 제작(Video_Creator) 에이전트 — 본편·숏폼 멀티 에디션 현황 · 제작 · 무결성 감사 · 업로드 데몬
python -X utf8 video_creator.py status
python -X utf8 video_creator.py produce <slug> --lang both
python -X utf8 video_creator.py backfill --limit 5
python -X utf8 video_creator.py audit
python -X utf8 video_creator.py daemon

# 4. 탈-PDF 순수 창의 아이디어 시네마(Edition 5 v2.0) 16:9 본편 & 9:16 숏폼 렌더링
python -X utf8 creative_idea_cinema.py --slug <slug> --lang both

# 5. 게임(gamemaker) · 디자인(designer) · 홍보(pr) · 수익화(finance) 에이전트 상태 및 검증
python -X utf8 gamemaker.py verify
python -X utf8 designer.py verify
python -X utf8 pr.py status
python -X utf8 finance.py status

# 6. 홈페이지 전체 무결성 감사 및 오프라인 단독 퀴즈 패키지 재빌드
python -X utf8 build_offline_quizzes.py
python -X utf8 audit_engine.py
python -X utf8 audit_full_mathedu.py
```

