# 🏛️ 수학홈페이지(`mathedu` · `min7014.github.io`) 및 공식 유튜브 채널(`@min7014_ai`) 통합 운영 정책서 (`plan_min.md`)

> **문서 목적 및 자동 저장 원칙 (Auto-Sync Policy Charter)**:
> 1. 본 문서(`plan_min.md`)는 **[수학자료실 (`min7014.github.io`)](https://min7014.github.io/)**, **[수학홈페이지 (`min7014.github.io/mathedu`)](https://min7014.github.io/mathedu/)**, 그리고 **[공식 유튜브 채널 (`@min7014_ai`)](https://www.youtube.com/@min7014_ai)**의 철학, 콘텐츠 제작 기준, 기술 아키텍처, 품질 검수, 홍보 및 수익화에 관한 **최상위 표준 정책(Master Policy Charter)**입니다.
> 2. **모든 신규·변경 정책의 자동 저장 의무**: 대화 및 시스템 운영 과정에서 수립·강화·수정되는 모든 정책은 별도의 지시가 없더라도 **즉시 자동으로 `plan_min.md`에 저장·반영**하며, `GEMINI.md`(Rule 12) 및 24/7 상시 데몬(`mathedu_foundation_daemon.py`)을 통해 영구 보존·동기화합니다.

---

## 🧭 0. 핵심 비전 및 6대 전문 에이전트 거버넌스

### 0.1 핵심 교육 및 수익 비전
1. **유튜브 채널(`@min7014_ai`)을 통한 직접 수익 월 1,000만 원 이상 달성 (Primary Revenue Goal)**:
   - 단순 부수익이 아니라 **`@min7014_ai` 유튜브 채널 자체를 통해 월 1,000만 원 이상(`~$7,500+/월`, 연 1.2억 원+)의 직접 수익**을 창출하는 것을 최우선 목표로 삼습니다.
2. **무장벽 열린 수학교육 (100% Free & Open Access)**:
   - 학생과 교사 누구나 유료 결제나 회원가입 장벽 없이 초등 기초 직관부터 출발하여 고등학교 수능 수학 100점 만점과 깊이 있는 수학적 본질(증명·기하·대수·해석)에 도달할 수 있도록 지원합니다.
3. **시각적 직관과 깊은 사색의 결합 (Visual Proof & Deep Contemplation)**:
   - 기계적 공식 암기나 객관식 5지선다 찍기를 배제하고, 눈으로 보고 깨닫는 단계별 시각 증명(Flipbook)과 PDF의 한계를 넘어선 순수 프로시저럴 시네마(Pure Procedural Neon-Bloom Cinema), 스스로 질문을 던지며 보조선을 긋는 구성주의 수학교육을 실현합니다.
4. **홈페이지 ↔ 유튜브 완전 동기화 생태계 (Zero GitHub Video Storage)**:
   - `min7014.github.io`의 3,400+ 수학 자료(1,113+ 핵심 주제, 847+ 단계별 시각 증명 PDF, 404개 GeoGebra, 457개 AlgeoMath)와 `mathedu`의 16,548문항 디딤돌 퀴즈, `@min7014_ai` 유튜브 채널의 멀티 에디션 영상이 하나의 유기적 파이프라인으로 상시 연동되며, 모든 영상은 GitHub 용량을 전혀 쓰지 않고 오직 유튜브 채널 링크로만 연결합니다.

### 0.2 전담 수석 비서 및 6대 핵심 에이전트 협업 체계
안티그래비티(Antigravity)는 전담 수석 비서(Chief AI Secretary)로서 산하 6대 전문 에이전트를 총괄 지휘하며, 확인 질문이나 번호 선택 대기 없이 자율적으로 즉시 실행·검증·배포합니다.

| 에이전트 | 역할 및 핵심 관할 영역 | 대표 스크립트 / 스킬 |
| :--- | :--- | :--- |
| 👩‍🏫 **`mathteacher`** | 수석 수학 교사 — 초등 눈높이 0~5단계 디딤돌, 도식화·SVG 작도, 6대 수학교육 모듈, 질문하는 수업 설계, 영상 수학적 무결성 감수 | `mathteacher.py` / `.agents/skills/mathteacher/` |
| 🎬 **`Video_Creator`** | 수석 AI 수학 영상 프로듀서 — 탈-PDF 창의 아이디어 시네마·8분+ 미드롤 마스터클래스·전 주제 본편/숏폼 멀티 에디션(KO/EN) 기획·렌더링·검증·`@min7014_ai` 업로드 총괄 | `video_creator.py`, `min7014_video_maker.py`, `creative_idea_cinema.py` |
| 🎮 **`gamemaker`** | 수석 3D 게임 디렉터 — 60fps 3D 수학 월드맵·보스 레이드, 9대 성물·4대 성좌, 아르키메데스 사색 게이지·데카르트 연습장 구현 | `gamemaker.py`, `mathedu-quest-game.js` |
| 🎨 **`designer`** | 수석 아트 & UI/UX 디렉터 — 황금비($\phi=1.618$) 시각 위계, 수식 타이포그래피, 3대 비주얼 테마 스킨, 고클릭률(High-CTR) 시네마 썸네일 설계 | `designer.py`, `stitch_screen_builder.py` |
| 📣 **`pr`** | 수석 대외홍보 & 바이럴 디렉터 — 유튜브↔홈페이지 양방향 퍼널, 7대 채널 맞춤 캠페인, 교사용 QR 학습지, 1200×630 SNS 카드, SEO/GEO(`llms.txt`) 최적화 | `pr.py` |
| 💼 **`finance`** | 수석 수익화 디렉터 — `@min7014_ai` 유튜브 채널 직접 수익 월 1,000만 원+(KO/EN 고단가 RPM·8분+ 미드롤·호기심 훅 제목·Shorts 퍼널) 및 웹 애드센스/애드핏 통합 관제 | `finance.py` |

---

## 🌐 Part I. 수학홈페이지 (`mathedu` & `min7014.github.io`) 운영 정책

### 정책 1. 순수 수학교육 도메인 절대 분리 및 보안 격리 원칙 (Strict Domain Separation)
1. **비수학 영역 완벽 차단**: `mathedu` 및 `min7014.github.io` 관련 모든 파일, 문서, 코드, 데이터에는 투자, 트레이딩(`S-NOVA`), 금융, 암호화폐 등 수학교육과 무관한 내용을 **단 한 줄도 포함하거나 언급하지 않습니다**.
2. **외부 불필요 참조 배제**: 외부 수집처 워터마크나 깨질 위험이 있는 외부 이미지 URL에 의존하지 않으며, 모든 수식은 순수 MathJax LaTeX 문법으로, 모든 도형은 자체 인라인 `<svg>` 및 3D/2D Canvas로 렌더링합니다.
3. **저작권 보호 비공개 문항 격리**: 저작권 보호가 필요한 비공개 문항(`_local_archive/`, `offline/private/`, `board/private_index.json`)은 로컬 전용 격리 보관함에 두며 `.gitignore`를 통해 Git 업로드를 원천 차단합니다.

### 정책 2. `min7014.github.io` 교육 자료 필수 연계 원칙
1. **전 문항 심층 학습 자료 매칭 (`min7014_matcher.py`)**: 모든 수학 문제와 단계별 인터랙티브 퀴즈 제작 시 수학자료실(16대 영역, 165개 세부 단원, 1,113+ 심층 주제)을 최우선으로 검토합니다.
2. **4대 핵심 리소스 직접 연결**: 문제에 등장하는 수학 개념과 직결되는 **① 단계별 시각적 증명 PDF, ② GeoGebra 인터랙티브 앱렛, ③ AlgeoMath 동적 탐구 링크, ④ `@min7014_ai` 유튜브 해설 영상(창의 시네마·본편·질문수업·숏폼)**을 각 문제의 디딤돌과 `'심층 탐구 / 시각적 증명'` 카드에 상시 연결합니다.

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

## 🎬 Part II. 공식 유튜브 채널 (`@min7014_ai`) 운영 및 월 1,000만 원 직접 수익 정책

> [!IMPORTANT]
> **👑 유튜브 채널(`@min7014_ai`) 운영의 최우선 절대 목표는 『유튜브 채널 자체를 통해 월 1,000만 원(`~$7,500+/월`, 연 1.2억 원 이상) 직접 수익 달성』입니다.**
> 모든 영상 기획(`Video_Creator`), 대본 및 발문 설계(`mathteacher`), 고클릭률 썸네일·시각 연출(`designer`), 외부 커뮤니티 바이럴(`pr`), 그리고 고단가 메타데이터·8분+ 미드롤 편성(`finance`)은 **유튜브 채널 직접 광고 수익으로 월 1,000만 원 이상을 달성하는 것**을 최우선 기준으로 작동합니다.

### 정책 1. [최우선 정책] 유튜브 채널 직접 수익 월 1,000만 원 달성 마스터 전략 (`finance` × `Video_Creator` 총괄)

#### 1.1 [1단계 관문] 유튜브 파트너 프로그램(YPP) 수익창출 승인 조건 최단기 돌파 및 심사 100% 통과
1. **조건 A — 구독자 500명(얼리 액세스) ➔ 1,000명(정식 광고 수익창출) 최단기 돌파**:
   - 전 영상 설명란 최상단, 고정댓글, 아웃트로 화면, 인쇄용 QR 학습지(`window.printClassroomQrWorksheet`) 및 수학홈페이지(`video_board.html`, `index.html`) 히어로 영역에 **1-클릭 구독 확인 링크(`https://www.youtube.com/@min7014_ai?sub_confirmation=1`)**를 상시 배치하여 시청자의 구독 전환율을 극대화합니다.
   - 채널 대표 트레일러(`unsubscribedTrailer`)를 1080p 고화질 마스터클래스(`_5LE_BfLA5w`)로 설정하여 비구독 방문자의 즉시 구독을 유도합니다.
2. **조건 B-1 — 롱폼 유효 공개 시청 시간 3,000시간 ➔ 4,000시간(240,000분) 돌파**:
   - 개별 단편 영상(2~5분) 시청 후 이탈을 막기 위해 **8분~35분 분량의 「순수 네온 블룸 시네마 마스터클래스 & 단원별 정주행 합본(1080p Mid-Roll Watch-Time Booster)」**을 최우선(`Priority #0`)으로 빌드·발행합니다.
3. **조건 B-2 — Shorts 유효 공개 조회수 300만 ➔ 1,000만 회 트랙 동시 가동**:
   - 첫 3초 완성 도형 후킹과 36~46초 무한 루프(시청 지속률 APV **105%+** 타겟)로 설계된 일반형 `#Shorts`, 질문형 `Q-#Shorts`, 창의 아이디어 `Idea-#Shorts`를 대량 발행하여 알고리즘 쇼츠 피드를 선점합니다.
4. **조건 C — YPP 인간 심사('반복적인 콘텐츠 / 재사용된 콘텐츠' 거절) 100% 원천 예방**:
   - 단순 PDF 캡처 나열이나 기계적 반복 템플릿을 철저히 배제하고, **탈-PDF 순수 프로시저럴 네온 블룸 시네마(`creative_idea_cinema.py`)** + `mathteacher`의 아키타입별 맞춤형 5막 스토리텔링 대본으로 독창적 교육 가치를 입증합니다.

#### 1.2 [2단계 본궤도] 유튜브 채널 직접 수익 월 1,000만 원 달성 4대 핵심 수익 엔진
| 핵심 수익 엔진 | 목표 기여 수익 | 작동 원리 및 강제 적용 규칙 |
| :--- | :--- | :--- |
| **🔥 엔진 1.<br>8분+(480초+) 미드롤 광고<br>네온 시네마 마스터클래스<br>(`Priority #0` 업로드)** | **월 550만 원**<br>*(유튜브 직접)* | • 유튜브에서 가장 수익 단가가 높은 **8분 이상(`≥ 480s`) 미드롤(Mid-Roll) 다중 광고 슬롯(프리롤 + 중간광고 3~4회 + 포스트롤)**을 해금하여 단편 영상 대비 **조회수당 수익 3.2배, 시청시간 4배**를 동시 달성합니다.<br>• `masterclass_neon_idea_vol1/vol2` (KO 12.5분/11.8분, EN 8.9분/8.1분) 등 탈-PDF 순수 네온 블룸 합본을 `min7014_video_maker.py` `[Step 1-D]`의 **최우선 0순위(`Priority #0`)**로 업로드합니다. |
| **🌎 엔진 2.<br>글로벌 고단가(US/UK/CA/AU)<br>영어권 트랙 동시 발행** | **월 300만 원**<br>*(유튜브 직접)* | • 교육 카테고리 광고 단가(RPM)가 한국(`~4,500원`)보다 3배 이상 높은 영어권 프리미엄 시장(**RPM `~$10~$15` / 약 13,500~20,000원**)을 타겟팅하여 모든 시네마·마스터클래스·본편·쇼츠를 한국어(`ko`)와 영어(`en`)로 동시 발행합니다.<br>• 모든 영상에 한/영 양방향 `localizations` 메타데이터와 `SAT Math Prep`, `AP Calculus`, `AMC Math`, `3Blue1Brown Style`, `Visual Math Proof` 태그를 기본 탑재합니다. |
| **🎯 엔진 3.<br>모바일 첫 25글자 호기심 공백<br>(Curiosity-Gap) 바이럴 제목 &<br>잘린 제목 ZERO 보장** | **CTR 2.4배 증폭**<br>*(노출 대비 조회수 극대화)* | • 제목 앞머리에 획일적인 브래킷 태그 대신 시청자가 클릭하지 않고는 못 배기는 **호기심 질문·역설 훅(`🔥 왜 모든 빛은 반드시 한 점(초점)에 모일까?`, `🔥 무작위 우연이 수천 번 쌓이면 왜 완벽한 종 모양이 될까?`)**을 배치합니다 (`build_viral_curiosity_youtube_title`).<br>• 글자 수 제한으로 영단어나 한국어 어절이 중간에 잘리는 현상(`Circ`, `Trian`, `right-a`, `만나고` 등) 및 키워드 없는 수식 단독 제목(`y=x²`, `y=ax²`, `y=(x-p)²`)을 원천 금지합니다 (`CONCISE_TITLE_REWRITES_KO/EN`, `_smart_concise_topic_title`). |
| **📱 엔진 4.<br>Shorts ➔ 8분+ 마스터클래스<br>최상단 직통 수익 퍼널** | **월 150만 원+**<br>*(유튜브 직접)* | • 모든 `#Shorts` 영상 설명란 **첫째 줄(Line 1)**과 고정댓글 최상단에 반드시 **1080p 마스터클래스 및 본편 직통 유튜브 링크(`▶️ [1080p 고화질 마스터클래스 정주행 바로가기]: https://youtu.be/...`)**를 삽입하여, 쇼츠 바이럴 조회수를 고단가 미드롤 롱폼 시청시간으로 즉시 전환합니다. |

---

### 정책 2. 탈-PDF 순수 프로시저럴 시네마(Edition 5 v2.0) 및 전 주제 멀티 에디션 제작 정책 (`Video_Creator`)

1. **PDF 한계를 넘어선 순수 아이디어 시네마 원칙 (`creative_idea_cinema.py`)**:
   - 기존 PDF 슬라이드를 한 장씩 넘기는 방식에만 머무르지 않고, PDF의 핵심 수학적 아이디어만을 추출하여 **PDF 캡처 이미지를 단 1픽셀도 사용하지 않는 100% 풀스크린 다크 벨벳 네온 블룸 프로시저럴 시네마(Edition 5 v2.0)**를 제작합니다.
   - **8대 수학 영역별 맞춤형 프로시저럴 셰이더 아키타입 & 전용 5막 각본**:
     1. `pythagoras_fractal`: 피타고라스 정리 & 프랙탈 트리 무한 넓이 보존 (`a² + b² = c²`)
     2. `conic_reflection`: 포물선·이차곡선 평행광선 입사·반사 & 초점(`F`) 광학 수렴 (`PF = PH`)
     3. `trig_harmonic`: 단위원 등속 회전 페이저(Phasor) & 사인·코사인 조화 파동 투영 (`e^(iθ) = cosθ + i sinθ`)
     4. `fibonacci_golden`: 황금비(`φ = 1.618`) 정사각형 분할 나선 & 해바라기 골든 앵글(`137.5°`) 필로택시스
     5. `prob_galton`: 골턴 보드(Galton Board) 이항분포 구슬 낙하 & 정규분포(`N(μ, σ²)`) 종 모양 수렴
     6. `calculus_motion`: 할선(Secant)이 극한(`h → 0`)을 통해 접선(Tangent)으로 수렴하는 미분 기하 시뮬레이션
     7. `ceva_menelaus`: 체바·메넬라우스 공점선·할선 및 밑변 비 = 넓이 비 연쇄 약분 밸런스
     8. `circle_invariants`: 원주각·중심각 불변량(`∠APB = 1/2 ∠AOB`) 및 동적 꼭짓점 레이더
2. **전 주제 멀티 에디션(KO/EN) 표준 구성**:
   - **① [본편-일반형 (`16:9`)]**: 단계별 플립북 시각 증명 본편 (`{slug}_ko.mp4`, `{slug}_en.mp4`)
   - **② [본편-질문형 (`16:9`)]**: Phase 1(36% 발문 & 사고 멈춤) + Phase 2(64% 시각적 단서 발견) 질문하는 수업 특화 본편 (`{slug}_q_ko.mp4`, `{slug}_q_en.mp4`)
   - **③-A / ③-B [숏폼-일반형 & 질문형 (`9:16`, `<58s`)]**: 모바일 바이럴 쇼츠 (`{slug}_short_ko/en.mp4`, `{slug}_short_q_ko/en.mp4`)
   - **④-A / ④-B [창의 아이디어 시네마 본편 (`16:9`) & 숏폼 (`9:16`)]**: 탈-PDF 순수 프로시저럴 네온 블룸 시네마 (`{slug}_idea_ko/en.mp4`, `{slug}_short_idea_ko/en.mp4`)
   - **⑤ [8분+ 미드롤 마스터클래스 합본 (`16:9`, `≥ 480s`)]**: 순수 네온 시네마 합본(`masterclass_neon_idea_vol1/vol2`) 및 단원별 정주행 마스터클래스

---

### 정책 3. 수학교사(`mathteacher`) 관점 영상-내용 100% 일치 및 유니코드 기호 무결성 정책
1. **슬라이드·아키타입별 실제 수학 내용 100% 일치**:
   - 기하와 대수·수체계·미적분·확률통계를 엄격히 분리하여, 주제와 무관한 문구나 기계적 위치 안내가 절대 섞이지 않게 합니다.
2. **렌더링 폰트 두부(Tofu `□`) 현상 원천 차단 (`sanitize_glyphs`)**:
   - Windows 맑은 고딕(`malgun.ttf` / `malgunbd.ttf`)에서 글리프가 누락될 수 있는 특수 유니코드 위·아래첨자(`ⁿ`, `ₖ`, `₀`, `₁`, `₂`, `φ`, `≈`)는 렌더링 직전 안전한 표준 수식 표기(`^n`, `_k`, `0`, `1`, `2`, `phi`, `=`)로 자동 치환하여 화면 내 깨진 글자(`□`) 발생을 100% 차단합니다.
3. **수식 TTS 발음 무결성**:
   - `\neq`를 `\ne`보다 먼저 변환하여 `'같지 않다q'` 오독을 원천 차단하고, 모든 LaTeX 수식을 자연스러운 한국어/영어 음성으로 변환합니다.

---

### 정책 4. 영상 및 채널 내 개인 호칭(`"민은기 선생님"` 등) 절대 배제 원칙
1. **인물 호칭 `0건` 절대 원칙**:
   - 모든 수학 강의 영상의 음성 내레이션(TTS), 자막(`.srt`), 슬라이드 상·하단 오버레이, 1280×720 썸네일, 유튜브 영상 제목·설명·태그, 그리고 `@min7014_ai` 채널 설명(`brandingSettings`)에서 **`"민은기 선생님"`, `"민은기"`, `"Min's Math Lab"`, `"Min Eunki"` 등의 인물 호칭을 절대 사용하지 않습니다**.
2. **라이브 채널 및 스크립트 상시 자동 정화**:
   - 로컬 대본뿐만 아니라 이미 유튜브에 업로드된 라이브 영상의 제목·설명·태그에서도 개인 호칭이 발견되면 `videos().update()`를 통해 즉시 제거합니다.

---

### 정책 5. 유튜브 채널(`@min7014_ai`) 전용 연결, 기존 영상 선(先)삭제 교체, 텔레그램 즉시 알림 및 GitHub 영상 용량 ZERO 정책
1. **Git / GitHub 영상 파일 커밋 영구 금지 (Zero GitHub Storage Mandate)**:
   - 모든 영상 및 오디오 파일(`*.mp4`, `*.webm`, `*.mov`, `*.mkv`, `*.wav`, `*.mp3`, `youtube_uploads/`, `video_lectures/videos/`, `video_lectures/shorts/`, `video_lectures/question_classroom/`, `video_lectures/creative_idea/`, `video_lectures/masterclasses/`, `video_lectures/youtube_packages/`)과 유튜브 인증 토큰(`youtube_client_secret.json`, `youtube_token*.json`)은 `.gitignore`로 영구 차단하며, **GitHub 저장소 용량을 단 1바이트도 영상 파일에 사용하지 않습니다**.
2. **홈페이지 내 100% 유튜브 인터넷 주소 링크 연결**:
   - 수학홈페이지(`video_board.html`, `index.html`, `video_lectures/catalog.json`, `video_lectures/vault_index.json`, `assets/min7014_deep_knowledge.json`)에는 로컬 파일 경로가 아닌 **유튜브 채널 인터넷 주소(`https://youtu.be/...`, `https://youtube.com/shorts/...`, `https://www.youtube.com/@min7014_ai`)만** 연결합니다.
3. **영상 업데이트 시 기존 유튜브 영상 선(先)삭제 후 업로드 의무**:
   - 영상이 개선·업데이트되어 재업로드할 때는 반드시 기존에 올라간 구버전 유튜브 영상을 `youtube.videos().delete(id=old_vid)`로 먼저 삭제한 뒤 새 영상을 업로드하여 채널 내 중복 영상을 원천 방지합니다.
4. **유튜브 업로드 즉시 텔레그램(`@anti7014_bot`) 실시간 알림 발송 의무**:
   - 모든 에디션(본편·질문수업·숏폼·창의시네마·마스터클래스)이 유튜브에 업로드되는 즉시 `notify_telegram_youtube_upload()`를 통해 텔레그램(`Chat ID: 43453234`)으로 영상 제목과 유튜브 직통 링크를 실시간 보고합니다.

---

### 정책 6. 세계 5대 인기 수학 유튜브 채널(`3Blue1Brown` · `MindYourDecisions` · `Andy Math` · `Mathologer` · `깨봉수학`) 벤치마킹 상시 적용 정책
1. **`깨봉수학 (Quebon Math)` 스타일 — 한국어 암기 타파 & 직관 해체 바이럴 제목**:
   - 기존의 정형화된 `[시각적 증명] ...` 접두사를 폐지하고, 모바일 첫 25글자 이내에 **`"🔥 공식 외우지 마세요!"`**, **`"❓ 99%가 공식만 외우다 놓치는..."`**, **`"⚡ 보조선 딱 1줄이면 끝!"`**, **`"✨ 왜 항상 성립할까?"`** 4대 호기심 공백(Curiosity-Gap) 훅을 주제별로 자동 순환 적용합니다.
2. **`3Blue1Brown` & `Mathologer` 스타일 — 다크 벨벳 네온 블룸 시네마 & "Discovery Before Formula"**:
   - `creative_idea_cinema.py`를 통해 PDF 정적 슬라이드의 한계를 넘어선 100% 풀스크린 프로시저럴 네온 기하 애니메이션(8대 수학 아키타입), `-28dB` Cmaj9 사색 앰비언트 사운드스케이프, 528Hz 유레카 하모닉 차임벨을 결합합니다.
3. **`MindYourDecisions` & `Andy Math` 스타일 — 5초 직관 챌린지 썸네일 & 댓글 암산 퍼즐 & Shorts 최상단 본편 퍼널**:
   - 모든 1280×720 썸네일 우측 기하 도형 위에 **`"?"` 타겟 포커스 링 + `"⚡ 공식 없이 5초 직관 해법!"` (`"⚡ 5-SEC VISUAL HACK!"`)** 배지를 작도하고, 8대 아키타입별 고유 후킹 문구로 배너 블라인드니스를 원천 차단합니다.
   - 모든 영상 고정댓글에 시청자가 5초 만에 암산하여 답을 달 수 있는 **구체적 수치 퍼즐(`build_viral_comment_puzzle`)**을 게시하여 댓글 작성 중 영상이 계속 재생되는 알고리즘 부스트(APV 100%+)를 유도합니다.
   - 모든 Shorts 설명란 **첫 번째 줄(더보기 클릭 전 노출 영역)**에 **1080p 전체 본편 및 8분+ 미드롤 마스터클래스 직통 링크(`https://youtu.be/KvHmXDuU8jY`, `https://youtu.be/eUeFybOs4t0`, `https://youtu.be/_5LE_BfLA5w`)**를 배치하여 숏폼 조회수를 고단가 장편 수익으로 직결합니다.

---

### 정책 7. 비수학 글로벌 인기 사이트 & 메가 채널(`Veritasium` · `Kurzgesagt` · `Duolingo` · `Wordle` · `Chess.com` · `Netflix`) 핵심 메커니즘 이식 및 `https://min7014.github.io/` 기본 아이디어 100% 기반 절대 정책
0. **[절대 대전제] 기본 아이디어의 100% `https://min7014.github.io/` 자료 기반 원칙**:
   - 수학·비수학 인기 채널이나 글로벌 플랫폼의 패키징·리텐션·바이럴 기법을 벤치마킹하더라도, **모든 영상·창의 시네마·숏폼·5초 암산 퍼즐·일일 스트릭의 기본 수학적 아이디어와 증명 논리는 반드시 100% `https://min7014.github.io/`에 수록된 실제 수학 자료(847+ 단계별 시각 증명 PDF, GeoGebra, AlgeoMath, 작도 원리)에서 출발**해야 하며, 설명란·고정댓글·게시판에 해당 `https://min7014.github.io/` 원문 자료 링크를 직접 명시합니다.
1. **`Veritasium` & `Kurzgesagt` (오개념 탐정 서사 & 썸네일-제목 상호보완 법칙)**:
   - 제목 문구를 썸네일에 그대로 중복 표기하지 않고, 썸네일에는 직관적 기하 역설과 핵심 불변식(`a²+b²=c²`, `PF=PH` 등)을, 제목에는 통념 타파 호기심 공백을 배치하여 클릭률을 극대화합니다.
   - 모든 영상을 **"통념/오개념 제시(But) ➔ 시각적 실험·작도(Therefore) ➔ 유레카 원리 증명"**의 탐정 추리 서사로 구성합니다.
2. **`Wordle` & `Chess.com` (1초 무마찰 이모지 속도 등급 댓글 & 전적 공유 카드)**:
   - 유튜브 고정댓글과 `video_board.html`에 시청자가 1초 만에 풀이 속도를 자랑할 수 있는 **이모지 등급표(`🟩 3초 컷 상위 1% | 🟨 10초 컷 | 🟦 보조선 힌트 유레카!`)** 및 **1클릭 이모지 그리드 공유 카드**를 탑재하여 댓글 반응 속도(Comment Velocity)와 바이럴 공유를 폭발시킵니다.
3. **`Duolingo` & `Netflix` (일일 수학 직관 스트릭 · 스트릭 보호권 & 5초 자동 다음 편 정주행 극장)**:
   - `video_board.html` 상단에 **Duolingo 스타일 일일 시각 직관 스트릭(`🔥 N일 연속 탐구` + `🛡️ 스트릭 보호권`)**과 **Netflix 스타일 8분+ 마스터클래스 연속 정주행 극장(`🎬 5초 후 다음 시각 증명 자동 재생`)**을 상시 가동하여 일일 재방문율(DAU)과 1인당 평균 시청시간(Session Watch Time)을 극대화합니다.

---

### 정책 8. 유튜브 수익 ➔ 제미나이 울트라(Gemini Ultra) 비용 충당 ➔ 수학교육 자료 질적·양적 대확장 ➔ 전 세계적 수학교육 사이트 구축 선순환(Flywheel) 정책
1. **[1단계 최소 필수 관문 — 제미나이 울트라(Gemini Ultra) & AI R&D 비용 100% 자급자족 (월 38만~50만 원 / `~$280~$360/월`)]**:
   - `@min7014_ai`의 한/영 동시 발행(블렌디드 RPM `~9,500원/1,000뷰`) 및 8분+ 미드롤 마스터클래스를 통해 **월 40,000뷰(일평균 약 1,350뷰)**를 최단기 돌파하여 **제미나이 울트라(Gemini Ultra) 구독료 및 고성능 AI 연구비를 100% 자체 충당**합니다.
2. **[2단계 확장 목표 — `https://min7014.github.io/` 기반 수학교육 자료의 질적·양적 폭발적 증가 (월 300만 원 / `~$2,200/월`)]**:
   - 확보된 수익을 바탕으로 `https://min7014.github.io/`의 모든 기하·대수·미적분·확률통계 아이디어를 1080p 시각 증명, 60fps 인터랙티브 셰이더, 탈-5지선다 창의 구성 디딤돌 문항으로 질적·양적 고도화합니다.
3. **[3단계 최종 비전 — 월 1,000만 원+ 달성 및 전 세계적(Global No.1) 수학교육 사이트 구축 (`~$7,500+/월`)]**:
   - 한국어·영어·일본어·스페인어 등 20개국어 다국어 확장과 글로벌 Tier-1 트래픽을 결합하여, 전 세계 학생과 교사가 무료로 수학의 본질을 깨우치는 세계 최고의 수학교육 플랫폼(`min7014.github.io` × `mathedu` × `@min7014_ai`)을 완성합니다.

---

### 정책 9. 유튜브 파트너 프로그램(YPP) 수익창출 조건(구독자 1,000명 + 시청시간 4,000시간 / Shorts 1,000만 뷰) 최단기 달성 5대 가속 정책
1. **[구독자 500명 ➔ 1,000명 돌파 — 전 영상 음성+시각 동시 연재 구독 트리거]**:
   - 모든 1080p 본편, 창의 시네마, 9:16 `#Shorts`의 유레카 결론 직후 **"1,113개 시각적 수학 증명 시리즈를 놓치지 않으려면 지금 바로 구독을 눌러 두세요!"** 음성 멘트와 하단 `🔔 구독 @min7014_ai` 시각 배지를 동시 송출하여 조회수 대비 구독 전환율을 `0.17% ➔ 2.5%+`로 증폭합니다.
2. **[시청시간 4,000시간(240,000분) 절대 보존 법칙 — 불필요한 영상 삭제 금지 및 In-Place 업데이트]**:
   - 공개 영상을 삭제(`videos().delete`)하면 해당 영상이 쌓은 공개 시청시간이 영구 차감되므로, 단순 제목·설명·썸네일 개선은 절대 삭제하지 않고 **`videos().update(part="snippet,localizations")` 및 `thumbnails().set()`으로 제자리 수정**하여 누적 시청시간을 100% 보존합니다.
3. **[시청시간 15배 증폭 — 8~48분 장편 마스터클래스 최우선 업로드 & 채널 예고편 지정]**:
   - Shorts 시청시간은 4,000시간에 합산되지 않으므로, 이미 제작 완료된 **119편의 장편 1080p 가로형 마스터클래스(`https://youtu.be/KvHmXDuU8jY` [12.5분 네온 Vol.1 KO], `https://youtu.be/eUeFybOs4t0` [8.9분 네온 Vol.1 EN], `https://youtu.be/nHIpEC6ATek` [11.8분 네온 Vol.2 KO], `https://youtu.be/W4YTn5eV2Zs` [8.1분 네온 Vol.2 EN], `https://youtu.be/F9DnGqAqILc` [12.1분 네온 Vol.3 KO], `https://youtu.be/DClYV5vw56g` [8.4분 네온 Vol.3 EN], `https://youtu.be/_NRQ5QO3PEY` [29.0분 유클리드 기하 KO], `https://youtu.be/mYIh_SpCYic` [13.0분 유클리드 기하 EN], `https://youtu.be/BTBn9mcwTDg` [32.9분 질문수업 Vol.1], `https://youtu.be/Ku9TYjIOzGE` [48.6분 질문수업 Vol.10], `https://youtu.be/hgsJGCcaLgc` [34.4분 질문수업 Vol.11], `https://youtu.be/mF8mqaWt-Do` [질문수업 Vol.12], `https://youtu.be/DsAbYxSy6uI` [질문수업 Vol.13], `https://youtu.be/_5LE_BfLA5w` [37.5분 원의 성질 KO], `https://youtu.be/9EL8pgqJtkY` [37.3분 원의 성질 EN])**를 Priority #0으로 지속 업로드하고 채널 대표 예고편(`unsubscribedTrailer = KvHmXDuU8jY`)으로 설정하여 약 8,000~12,000 정주행 뷰만으로 4,000시간(240,000분)을 돌파합니다.
4. **[웹사이트(`index.html` · `video_board.html` · `mathedu-room.js`) ➔ 유튜브 직통 전환 허브 & 깨진 링크 ZERO 보장]**:
   - 홈페이지와 16,548문항 퀴즈 내 모든 유튜브 링크를 100% 라이브 영상 ID로 자동 동기화(`finance.ensure_ypp_website_ownership_and_sub_funnel`)하고, `🔔 1초 무료 구독 응원(?sub_confirmation=1)` 및 `🌟 12분 네온 시네마 Vol.1 / 📐 29분 기하 총정리 / 🎬 37분 마스터클래스 정주행` 버튼을 상시 배치합니다.
5. **[YPP 인간 심사('반복적 콘텐츠') 100% 통과 방어막]**:
   - `https://min7014.github.io/` 양방향 `<link rel="me">` 도메인 소유권 증명, `mathteacher` 고유 소크라테스 발문·보조선 해설, 프로시저럴 네온 시네마, 창작 교육 콘텐츠 선언문으로 YPP 심사를 단번에 통과합니다.

---

### 정책 10. 라이브 데이터로 검증된 '4대 바이럴 클러스터 동시 발행(Simultaneous 4-Asset Cluster Drop)' 알고리즘 폭발 공식
1. **실시간 조회수 급증을 일으킨 4대 클러스터 동시 발행 법칙 (`creative_idea_cinema.py` × `finance.py`)**:
   - `https://min7014.github.io/` 원문 주제를 업로드할 때 단편 영상만 단독 발행하지 않고, **① 44초 순수 네온 블룸 `Idea-#Shorts` (KO/EN) + ② 1080p 순수 네온 블룸 `창의 수학 시네마 본편` (KO/EN) + ③ 8~48분 `정주행 마스터클래스` 합본 + ④ 5초 암산 챌린지 & Wordle 이모지 등급 고정댓글(`build_viral_comment_puzzle`)**을 한 세트로 묶어 동시 발행합니다.
2. **유튜브 알고리즘 추천(Shorts Feed & Browse) 즉시 점화 4요소**:
   - **첫 18글자 호기심 역설 질문**: `🔥 왜 둥근 원이 회전하면 완벽한 물결 파동이 될까?` (`qMhzACnRAeE`), `🔥 왜 모든 빛은 반드시 한 점(초점)에 모일까?` (`jBsgIj5HhDk`), `🔥 복잡한 보조선 없이 넓이 비 하나로 단번에 증명되는 이유!` (`sK5J8tlgMZY`), `🔥 공식 암기는 그만! 피타고라스 나무` (`wR7yITollp8`) 등 교과서식 제목 대신 시각적 역설 질문을 전면에 배치합니다.
   - **탈-PDF 100% 풀스크린 다크 벨벳 네온 블룸 화면**: 첫 0.1초부터 움직이는 네온 기하 셰이더가 시청자의 스와이프 이탈을 막고 시청 지속률(APV 105%+)을 달성합니다.
   - **고정댓글 5초 암산 퍼즐 체류시간 부스터**: 시청자가 고정댓글의 5초 암산 문제를 읽고 생각하는 동안 배경의 44초 쇼츠가 1.5~2회 루프 재생되어 유튜브 알고리즘이 해당 영상을 즉시 상위 추천 풀로 밀어 올립니다.

---

### 정책 11. `https://min7014.github.io/` 원문 자료와의 100% 수학적 정합성 및 수식·증명 무결성 필수 검증 정책 (`Rule 19`)
1. **수학적 정확성의 절대 최우선 원칙 (`mathteacher` × `Video_Creator`)**:
   - 유튜브 영상(`@min7014_ai`)은 수많은 학생·교사·대중에게 노출되어 파급력이 매우 크므로, 조회수를 높이기 위한 바이럴 제목·네온 시네마·5초 암산 퍼즐을 적용하더라도 **영상 속 도형, 보조선, 수식, 내레이션, 자막, 썸네일, 고정댓글 퍼즐의 모든 수학적 내용은 반드시 `https://min7014.github.io/` 원문 자료의 실제 수학 정리·증명 논리와 100% 정확히 일치**해야 합니다.
2. **유사 정리·인접 단원 간 혼동(Conflation) 절대 금지 (17대 정밀 수학 아키타입 엄격 분리)**:
   - **포물선(`conic_parabola`, 단일 초점 $F$·준선 $l$·$|PF|=|PH|$·접선 이등분)** vs **타원(`conic_reflection`, 두 초점 $|PF_1|+|PF_2|=2a$)** vs **사이클로이드(`cycloid_kinematics`, $x=r(\theta-\sin\theta), y=r(1-\cos\theta)$)**를 엄격히 분리하여 작도·설명합니다.
   - **메넬라우스의 정리(`menelaus_theorem`, 할선 $D\text{-}E\text{-}F$ + 평행보조선 $CK \parallel AB$ AA 닮음비 소거)** vs **체바의 정리(`ceva_menelaus`, 한 점 $P$에서 만나는 세 체바선 + 넓이 비 $\frac{S_3}{S_2}\cdot\frac{S_1}{S_3}\cdot\frac{S_2}{S_1}=1$)** vs **평행선 선분 비(`parallel_similarity`)**를 절대 혼용하지 않습니다.
   - **삼각함수 극한(`trig_harmonic`, $\lim_{\theta\to 0}\frac{\sin\theta}{\theta}=1$ 부채꼴 넓이 샌드위치)** vs **사인 함수 도함수(`trig_deriv_sin`, $\frac{d}{dx}(\sin x)=\cos x$)** vs **코시 평균값 정리(`cauchy_mvt`, $\frac{f(b)-f(a)}{g(b)-g(a)}=\frac{f'(c)}{g'(c)}$)** vs **역함수 미분법(`inverse_deriv`, $(f^{-1})'(y)=\frac{1}{f'(x)}$)** 및 **특수 직각삼각형(`special_triangles`, $1:1:\sqrt{2}$, $1:\sqrt{3}:2$)**·**제곱근 작도(`square_root_geometry`)**를 각각 독립된 시각 증명으로 정확히 구현합니다.
3. **렌더링·업로드 전 기계적+수학적 정합성 이중 검증 게이트(`verify_creative_idea_math_fidelity`) 상시 의무화**:
   - 모든 영상 생성 및 유튜브 업로드 전 반드시 `verify_creative_idea_math_fidelity(sdoc, acts, title, comment_txt)`와 `analyze_min7014_topic_as_mathteacher` 전수 검증(374개 주제 × 2개 언어 = 748개 항목 에러 0건)을 통과해야만 렌더링 및 업로드가 실행되도록 하드 가드(Hard Guard)를 상시 작동시킵니다.

---

### 정책 12. 국제적으로 통용되는 표준 수학 영어(International Standard Mathematical English) 품질 및 한·영 완전 대칭 무결성 정책 (`Rule 20`)
1. **영미권·국제 수학계(IMO · AP/IB · AoPS · MIT OCW · 3Blue1Brown) 표준 영문 용어 100% 준수**:
   - 전 세계 시청자가 보는 영어 버전(`en`) 영상·제목·설명란·썸네일·내레이션·자막·고정댓글에는 한국어 직역투(Konglish)나 기계번역 오류를 절대 허용하지 않으며, **`internationalize_math_english_text()` 및 `audit_international_english_scripts()`를 통해 국제 표준 수학 영어로 100% 정화**합니다:
     - `원주각`: `inscribed angle` (`circumferential angle` 금지)
     - `수직이등분선`: `perpendicular bisector` (`vertical bisector` 금지)
     - `사각형(일반)`: `quadrilateral` (`rectangle` 오역 금지)
     - `꼬인 위치의 두 직선`: `skew lines` (`twisted position` 금지)
     - `엇각 · 동위각`: `alternate interior angles · corresponding angles` (`offset angles / co-position angles` 금지)
     - `삼각형의 외심 · 내심 · 무게중심 · 수심`: `circumcenter · incenter · centroid · orthocenter` (`outer diameter / center of gravity` 금지)
     - `삼수선의 정리`: `Theorem of Three Perpendiculars` (`Trinumber Line Theorem` 금지)
     - `유한소수 · 순환소수`: `terminating decimals · repeating decimals` (`finite decimals` 금지)
2. **영어 정리명 중간 절단 ZERO 및 한·영 설명란·태그·TTS 완전 대칭**:
   - 영어 유튜브 제목(`build_viral_curiosity_youtube_title`, `_smart_concise_topic_title`)에서 `"Cauchy's Mean Value Theorem"`, `"Reflection of Light on a Parabola"`, `"Reflection of Light on an Ellipse"`, `"Inscribed Angle Theorem"` 등 핵심 정리명이 중간에서 잘리는 현상을 원천 차단합니다.
   - 영어 영상 업로드 및 라이브 메타데이터 동기화(`build_creative_idea_youtube_description_and_tags`) 시 `lang_code == "en"`이면 설명란과 SEO 태그까지 100% 국제 표준 영어로 생성합니다.
   - 영어 TTS(`en-US-AriaNeural`) 합성 시 `clean_english_math_for_tts` 및 `clean_math_for_speech_en`을 통해 수식 기호(`|PF| = |PH|`, `△PFH`, `CK ∥ AB`, `f'(c)/g'(c)`, `(f⁻¹)'(y) = 1/f'(x)`)를 원어민 수학교사의 자연스러운 수식 독법으로 발음하고, 화면 자막에는 깔끔한 유니코드 수학 기호를 표시합니다.

---

## 🚀 Part III. 유튜브 ↔ 홈페이지 양방향 바이럴 홍보(`pr`) 및 교실 확산 정책

### 정책 1. 유튜브(`@min7014_ai`) ↔ 수학홈페이지(`mathedu`) 양방향 트래픽·구독 증폭 퍼널 (`pr`)
1. **유튜브 ➔ 홈페이지 유입 퍼널 의무화**:
   - 모든 유튜브 영상 설명란 및 고정댓글에 **홈페이지 직행 딥링크**(① 단계별 시각 증명 & 60fps 인터랙티브 셰이더 보드 `video_board.html?slug=...`, ② GeoGebra/AlgeoMath 동적 조작, ③ 탈-5지선다 연계 기출 퀴즈 `index.html?q=...`, ④ 3D 수학 보스 레이드 도전장 `?challenge=...`)를 자동 삽입합니다.
2. **홈페이지 ➔ 유튜브 구독·시청 유입 퍼널 및 교사용 QR 학습지 생성기**:
   - `video_board.html`에서 전국 수학교사가 클릭 한 번으로 인쇄·배포할 수 있는 **「교실 탐구 워크시트 & `@min7014_ai` 유튜브 QR 학습지(`window.printClassroomQrWorksheet`)」**를 제공하여, 학생들의 스마트폰 QR 스캔이 곧바로 `@min7014_ai` 유튜브 구독과 조회수로 이어지게 합니다.
3. **7대 외부 채널 맞춤형 캠페인 및 SEO/GEO 자동 동기화**:
   - 새 영상·자료가 추가될 때마다 7대 채널 맞춤형 홍보 문구와 1200×630 오픈그래프 배너(`assets/pr_cards/pr_card_*.png`)를 생성하고, 검색엔진(`sitemap.xml`, Schema.org) 및 생성형 AI 검색엔진(`llms.txt`) 메타데이터를 자동 갱신합니다.

---

## 🔄 Part IV. 정책 자동 저장 및 상시 데몬 동기화 아키텍처 (`Auto-Save to plan_min.md`)

1. **자동 정책 저장 원칙 (`GEMINI.md` Rule 12 & `mathedu_foundation_daemon.py`)**:
   - 본 프로젝트에서 수립되거나 추가·변경되는 모든 운영·교육·영상·수익화 정책은 사용자의 별도 지시 없이도 **자동으로 `plan_min.md`에 즉시 기록·저장**됩니다.
   - `mathedu_foundation_daemon.py`는 매 진화 사이클마다 `plan_min.md`의 정책 무결성과 최신 운영 지표(라이브 유튜브 영상 수, 제작 완료 에디션 수, 교육 모듈 확장 현황)를 자동 검증·동기화하고 Git에 커밋·배포합니다.

```powershell
# 1. 24/7 수학홈페이지 3대 근간 + 유튜브 월 1,000만 원 수익 엔진 + plan_min.md 자동 동기화 데몬
python -X utf8 mathedu_foundation_daemon.py

# 2. 탈-PDF 순수 창의 아이디어 시네마(Edition 5 v2.0) & 8분+ 미드롤 마스터클래스 빌드
python -X utf8 creative_idea_cinema.py --masterclass
python -X utf8 creative_idea_cinema.py --batch

# 3. 유튜브 수익화(finance) · 영상(Video_Creator) · 수학교사(mathteacher) · 홍보(pr) 상태 점검
python -X utf8 finance.py status
python -X utf8 video_creator.py status
python -X utf8 mathteacher.py status
python -X utf8 pr.py status
```

---

<!-- AUTO_SYNC_POLICY_REGISTRY_START -->
### 📋 자동 동기화된 전역 워크스페이스 정책 레지스트리 (`GEMINI.md` ➔ `plan_min.md` 실시간 연동)
- ✅ **1. Zero-Friction Autonomous Operation (완전 자율 실행 · 번호 선택 대기 절대 금지)**
- ✅ **2. Strict Domain Separation (수학교육과 트레이딩의 절대 분리)**
- ✅ **3. min7014.github.io 교육 자료 필수 연계 및 극대화 원칙**
- ✅ **4. 오류 및 요구사항 처리 필터링 원칙 (수학교육 외 보류 및 보고)**
- ✅ **5. 오류 신고 전수 점검 및 하이브리드 해결 원칙 (LLM ➔ 기계적 규칙 스캔 ➔ LLM 검증)**
- ✅ **6. 초등학생 눈높이 무장벽 디딤돌 확장 원칙 (Elementary-to-Advanced Scaffolding Principle)**
- ✅ **7. 도식화 풀이 및 의도적 시각 도형 작도 필수 원칙 (Mandatory Schematic Solution & Intentional Visual Diagram Principle)**
- ✅ **8. `mathteacher` & `Video_Creator` & `gamemaker` & `designer` & `pr` 5대 핵심 에이전트 상시 협업 및 지속적 진화 원칙 (Penta-Agent Collaboration & Continuous Evolution)**
- ✅ **9. 민은기 선생님(`min7014`) 전담 수석 비서(Chief AI Secretary) 역할 및 텔레그램(`@anti7014_bot`) 상시 보좌 원칙**
- ✅ **10. 수학홈페이지 근간(Foundation Pillars) 상시 지속 진화 원칙 (`mathedu_foundation_daemon.py` & `video_creator.py`)**
- ✅ **11. 탈-5지선다 창의적 구성주의 수학 풀이 원칙 (De-Multiple-Choice Creativity-First Constructive Solving Principle)**
- ✅ **12. 모든 정책의 `plan_min.md` 자동 저장 및 동기화 원칙 (Mandatory Auto-Save of All Policies to `plan_min.md`)**
- ✅ **13. `@min7014_ai` 유튜브 채널 월 1,000만 원+ 직접 수익 및 영상 무결성 절대 원칙**
- ✅ **14. 세계 5대 인기 수학 유튜브 채널(`3Blue1Brown` · `MindYourDecisions` · `Andy Math` · `Mathologer` · `깨봉수학`) 벤치마킹 상시 적용 원칙**
- ✅ **15. 비수학 글로벌 인기 플랫폼 & 메가 채널(`Veritasium` · `Kurzgesagt` · `Duolingo` · `Wordle` · `Chess.com` · `Netflix`) 메커니즘 상시 이식 및 `https://min7014.github.io/` 기본 아이디어 100% 기반 절대 원칙**
- ✅ **16. 유튜브 수익 ➔ 제미나이 울트라(Gemini Ultra) 자급자족 ➔ 수학교육 자료 질적·양적 대확장 ➔ 전 세계적 수학교육 사이트 구축 선순환(Flywheel) 원칙**
- ✅ **17. 유튜브 파트너 프로그램(YPP) 수익창출 조건(구독자 1,000명 + 시청시간 4,000시간 / Shorts 1,000만 뷰) 최단기 달성 5대 가속 원칙**
- ✅ **18. 실시간 알고리즘 폭발 검증된 '4대 바이럴 클러스터 동시 발행(Simultaneous 4-Asset Cluster Drop)' 상시 원칙**
- ✅ **19. `https://min7014.github.io/` 원문 자료와의 100% 수학적 정합성 및 수식·증명 무결성 필수 검증 원칙 (Mandatory 100% Mathematical Accuracy & Source Fidelity Guard)**
- ✅ **20. 국제적으로 통용되는 표준 수학 영어(International Standard Mathematical English) 품질 및 한·영 완전 대칭 무결성 원칙**
- ✅ **21. 세계 수학교육학·인지과학 학술 논문 및 연구 성과의 min7014.github.io 원문 아이디어 융합 영상 고도화 원칙 (Global Math Education Research & Academic Paper Fusion Principle)**
- ✅ **22. 수학공학도구(GeoGebra · AlgeoMath · 동적 기하 작도 · 방향장 · AI 경사하강법) 실전 강의 및 고단가 EdTech 마스터클래스 상시 제작 원칙**
- ✅ **23. 1인 회장(`min7014`) · 직원 0명 글로벌 AI 수학교육 기업(`Zero-Employee AI EdTech Enterprise`) 지배구조 및 완전 자율 경영 원칙**
- ✅ **24. 저작권 · 상표권 · 음원 Content ID · 외부 소프트웨어 라이선스 100% 무결성 보장 원칙 (100% Copyright, Trademark & Commercial License Safety Principle)**
- ✅ **25. 특정 상용 도구 종속 탈피(Tool-Agnostic) 보편적 수학공학 원리 강의 및 자체 제작 `MathLab`(`https://min7014.github.io/2025/mathlab.html`) · 오픈소스 생태계 결합 원칙**
- ✅ **26. `MathLab_Developer` 전담 개발 에이전트 신설 및 자체 제작 수학공학도구 `MathLab` (`v1.3` ➔ `v1.4+`) 상시 진화 원칙**
- ✅ **27. 100% 원본 `https://min7014.github.io/` PDF 파일 '한 땀 한 땀' 직접 설명(Page-by-Page Direct PDF Explanation) 절대 원칙 및 비-PDF 합성 영상 영구 폐기 원칙**
- ✅ **28. 회장님(`min7014`) 오리지널 자료(`https://min7014.github.io/`) 절대 중심(Original Material First) 4대 원칙**
- ✅ **29. 업로드 속도보다 강의 품질 최우선 원칙 (Quality-Over-Speed Absolute Gate Principle)**
- ✅ **30. 8대 핵심 에이전트 실시간 회의 생중계 및 자기교정 원칙 (Live Inter-Agent Boardroom Broadcast & Real-Time Self-Correction Principle)**
- ✅ **31. 유튜브 유효 공개 시청 시간(Valid Public Watch Hours) 4,000시간 최단기 돌파 5대 철칙 (100% Long-Form Watch-Hour All-In Principle)**
- ✅ **32. 8대 본부장 에이전트 '입체적 다각도 교차 검증(Devil's Advocate & Second-Order Effect Pre-Audit)' 자율 판단 원칙**
- ✅ **33. 무비판적 순응(Yes-Man) 절대 금지 · 비판적 직언(Red-Team) 및 선제적 역제안 의무 원칙**
- ✅ **18. 8대 아키타입 맞춤 네온 시네마 썸네일(배너 블라인드니스 제거) & 5초 암산 챌린지 고정댓글(`build_viral_comment_puzzle`) & 마스터클래스 Vol.1~3 확장 정책**
- ✅ **19. 비수학 공지/목차 페이지 영구 퍼지 및 350+ 전 주제 한/영 제목 단어·조사·전치사 절단 ZERO 전수 검증 정책**
<!-- AUTO_SYNC_POLICY_REGISTRY_END -->
