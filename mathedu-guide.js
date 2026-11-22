/**
 * mathedu-guide.js (v2.0 · Just-in-Time Contextual & Draggable Floating Guide)
 *
 * - Floating draggable compass-star orb (#matheduGuideOrb) that guides users
 *   one tip at a time based on what they are doing right now (Just-in-Time).
 * - Smooth Pointer-Event drag-and-drop on both the orb and the card drag handle,
 *   with viewport clamping and normalized coordinate persistence in localStorage.
 * - 14 situational micro-guides surfaced on real user reactions (focus/click/input),
 *   never repeating an already-seen auto-tip, plus an on-demand situational picker
 *   and Quiet Mode toggle (autoTips ON/OFF).
 * - Full KO/EN bilingual parity, Light/Dark theme sync, mobile ergonomics, and
 *   automatic hiding when Error Report Inspector (#mathedu-report-fab) is active.
 */
(function (window, document) {
  'use strict';

  if (window.MatheduGuide) return;

  var STORAGE_STATE_KEY = 'mathedu_guide_state_v2';
  var STORAGE_POS_KEY = 'mathedu_guide_pos_v1';
  var DRAG_THRESHOLD_PX = 6;
  var SPOTLIGHT_DURATION_MS = 3200;

  var TOPICS = [
    {
      id: 'welcome',
      category: 'start',
      chipLabel: { ko: '✨ 시작 안내', en: '✨ Start' },
      title: {
        ko: '지금 무엇을 찾고 계신가요?',
        en: 'What would you like to do now?'
      },
      body: {
        ko: '사용법이 다양해서 그때그때 필요한 것만 하나씩 안내해 드릴게요. 아래에서 고르거나 화면의 기능을 눌러 보세요.',
        en: 'Because mathedu has many tools, I guide just one item at a time when needed. Pick below or interact anywhere.'
      },
      tipLine: {
        ko: '반짝이는 별 아이콘을 누르면 자세한 사용법이 열리고, 드래그해 옮길 수 있어요.',
        en: 'Tap this glowing star anytime for detailed steps, or drag to reposition it.'
      },
      details: {
        ko: [
          ['통합 검색 ("/")', '상단 검색창에 개념·연도·문항(예: 피타고라스, 9월 미적분 30번)을 입력하면 기출과 시각 증명을 한 번에 찾습니다.'],
          ['시각 증명 먼저 보기', '유형 암기보다 먼저 3,400+ 동적 기하 도형·영상 게시판·MathLab에서 보조선 원리를 눈으로 확인하세요.'],
          ['초등~수능 디딤돌 풀이', '문제 카드를 열면 초등 눈높이 1단계 직관부터 최종 수능 문제까지 막힘없이 이어지는 단계로 풀립니다.'],
          ['100% 무료 · 별 자유 이동', '모든 문제, 오답노트, 회원가입 및 교실 도구는 추가 비용이 전혀 없으며, 이 별을 드래그해 원하는 자리에 두실 수 있습니다.']
        ],
        en: [
          ['Omni-Search ("/")', 'Press "/" or use the top bar (e.g., Pythagoras, Calculus) to search stepping-stone quizzes and visual proofs together.'],
          ['Visual Intuition First', 'Before drilling formulas, open 3,400+ dynamic geometry proofs, the video board, or MathLab to see auxiliary lines move live.'],
          ['Elementary-to-CSAT Steps', 'Every quiz opens with intuitive stepping stones from basic arithmetic and spatial ideas up to advanced problems.'],
          ['100% Free & Draggable Star', 'All materials, history sync, and teacher tools are 100% free with zero fees—and this star orb can be dragged anywhere on screen.']
        ]
      },
      selectors: ['#headerGlobalSearchInput', '#quizFilterBar'],
      relatedIds: ['search', 'visual_proofs', 'teacher_tools', 'deep_labs']
    },
    {
      id: 'search',
      category: 'find',
      chipLabel: { ko: '🔍 통합 검색', en: '🔍 Search' },
      title: {
        ko: '통합 검색 · "/" 단축키',
        en: 'Omni-Search & "/" Shortcut'
      },
      body: {
        ko: '상단 검색창이나 목록 검색창에 단원·기출 키워드(예: 피타고라스, 타원, 9월 미적분 30번)를 입력하면 문항과 시각 증명을 즉시 찾아줍니다.',
        en: 'Type any topic or exam keyword (e.g., Pythagoras, Ellipse, Calculus) to search stepping-stone quizzes and visual proofs together.'
      },
      tipLine: {
        ko: '키보드 "/" 키를 누르면 어느 위치에서든 바로 검색창이 열립니다.',
        en: 'Press "/" anywhere on the page to jump straight to Omni-Search.'
      },
      details: {
        ko: [
          ['키보드 "/" 1초 포커스', '페이지를 내려 보다가도 "/" 키만 누르면 상단 통합 검색창에 즉시 커서가 잡힙니다.'],
          ['복합 키워드 검색', '학년도·시행월·과목·단원명(예: "2027 6월 기하", "단델린 타원")을 조합해 입력해 보세요.'],
          ['기출 + 원문 동시 추천', '입력 즉시 관련 기출문제와 시각 증명 아카이브가 드롭다운으로 함께 정리됩니다.']
        ],
        en: [
          ['Instant "/" Shortcut', 'Press "/" from anywhere on the homepage to focus the global Omni-Search bar immediately.'],
          ['Combine Keywords', 'Mix year, month, subject, or theorem names (e.g., "2027 Geometry", "Dandelin") to narrow results fast.'],
          ['Unified Results Dropdown', 'Matching stepping-stone quizzes and 3,400+ visual proofs appear together as you type.']
        ]
      },
      selectors: ['#headerGlobalSearchInput', '#quizSearchInput', '#mobileHeaderSearchToggleBtn'],
      relatedIds: ['filters', 'visual_proofs', 'csat2027']
    },
    {
      id: 'filters',
      category: 'find',
      chipLabel: { ko: '🎯 과목·연도 필터', en: '🎯 Filters' },
      title: {
        ko: '과목·연도 필터 & 랜덤 도전',
        en: 'Smart Filters & Random Challenge'
      },
      body: {
        ko: '과목·연도 버튼으로 원하는 범위만 좁히고, 상세 조건으로 학년·시행월·번호를 고르세요. 🎲 랜덤 버튼을 누르면 바로 한 문제가 열립니다.',
        en: 'Filter by subject, year, or detailed exam selectors, or click Random to launch a stepping-stone problem right away.'
      },
      tipLine: {
        ko: '모든 문항은 초등 눈높이 1단계 직관부터 차근차근 시작합니다.',
        en: 'Every quiz builds step by step from elementary intuition.'
      },
      details: {
        ko: [
          ['과목·연도 빠른 알약', '"공통(수I·II) · 미적분 · 기하 · 확률과 통계" 및 최근 학년도 알약으로 범위를 1클릭으로 좁힙니다.'],
          ['상세 조건 서랍 열기', '⚙️ "상세 조건"을 펼치면 대상 학년(고1~고3), 시행월(3/6/9/11월), 문항 번호별로 정확히 필터링됩니다.'],
          ['🎲 랜덤 & 초기화', '가볍게 감각을 유지하고 싶다면 "🎲 랜덤"으로 즉시 출제하고, "초기화"로 전체 16,594+ 목록을 복원하세요.']
        ],
        en: [
          ['Subject & Year Pills', 'Tap subject pills (Common, Calculus, Geometry, Prob & Stats) or recent years to narrow the list in one click.'],
          ['Detailed Conditions', 'Expand "Detailed Filters" to select exact grade level, exam month, problem number, or curriculum tags.'],
          ['Random & Reset', 'Hit "Random Quiz Challenge" for a fresh problem right away, or "Reset" to return to all 16,594+ items.']
        ]
      },
      selectors: ['#stitchSubjectPills', '#stitchYearPills', '#btnRandomQuizChallenge', '#quizFilterBar'],
      relatedIds: ['search', 'wrong_bookmarks', 'lesson_pack']
    },
    {
      id: 'wrong_bookmarks',
      category: 'study',
      chipLabel: { ko: '⭐ 오답·즐겨찾기', en: '⭐ Notes & Stars' },
      title: {
        ko: '오답노트 · 즐겨찾기 · 마이룸',
        en: 'Error Notes, Bookmarks & My Room'
      },
      body: {
        ko: '틀렸던 문제는 오답노트에 자동 수집되고 ★ 버튼으로 즐겨찾기에 모아둘 수 있습니다. 내 서재에서 100% 무료 계정으로 기록을 이어 보세요.',
        en: 'Missed items collect in Error Notes, and ★ bookmarks save favorites. Keep your study history across devices 100% free.'
      },
      tipLine: {
        ko: '가입 없이 비회원 이름·비밀번호만으로도 바로 기록 저장이 가능합니다.',
        en: 'Works right in your browser or with a free account—zero fees ever.'
      },
      details: {
        ko: [
          ['오답노트 자동 누적', '퀴즈 풀이 중 한 번이라도 틀린 문제는 자동으로 "오답노트" 탭에 모여 약점 복습을 도와줍니다.'],
          ['★ 나만의 즐겨찾기', '중요하거나 다시 보고 싶은 문항 오른쪽의 별표(★)를 누르면 "즐겨찾기"와 마이룸에 저장됩니다.'],
          ['100% 무료 계정 보관', '우측 상단 프로필(👤)에서 별도 비용 없는 무료 회원가입으로 기기 변경 후에도 학습 기록을 이어갈 수 있습니다.']
        ],
        en: [
          ['Auto Review Vault', 'Any problem missed during practice is automatically collected under "Review Vault" for targeted retry.'],
          ['★ Bookmark Favorites', 'Tap the star next to any item to save it into "Bookmarks" and your personal My Room shelf.'],
          ['100% Free Cloud History', 'Use the top-right profile button to register free of charge and preserve your study records across devices.']
        ]
      },
      selectors: ['#tabBtnWrong', '#tabBtnBookmarks', '#studentLibraryQuickBar', 'button[onclick*="MatheduAuth"]'],
      relatedIds: ['filters', 'quest_streak', 'lesson_pack']
    },
    {
      id: 'lesson_pack',
      category: 'teach',
      chipLabel: { ko: '🎒 수업 팩 묶기', en: '🎒 Lesson Pack' },
      title: {
        ko: '교사용 연속 수업 팩 묶기',
        en: 'Teacher Lesson Pack Builder'
      },
      body: {
        ko: '"수업 팩 선택"을 누른 뒤 문항 옆 체크박스를 고르면 여러 문제를 순서대로 풀 수 있는 전용 수업 링크가 즉시 만들어집니다.',
        en: 'Enable Lesson Pack mode and check multiple problems to generate a single sequenced study link for your class.'
      },
      tipLine: {
        ko: '단 하나의 링크나 QR 공유만으로 학생들이 연속 풀이를 진행합니다.',
        en: 'Share one link or QR code so students complete the set in order.'
      },
      details: {
        ko: [
          ['수업 팩 모드 활성화', '문제 목록 상단 "수업 팩 선택" 탭을 누르면 각 문항 왼쪽에 다중 선택 체크박스가 열립니다.'],
          ['문항 순서대로 선택', '오늘 수업할 문제들을 체크하면 화면 하단에 검은색 수업 팩 생성 플로팅 바가 나타납니다.'],
          ['링크·칠판 QR 1초 공유', '"📋 링크 복사"로 단톡방에 올리거나 "🖥️ 칠판 QR"을 띄워 학생들이 1번부터 순서대로 풀게 하세요.']
        ],
        en: [
          ['Enable Selection Mode', 'Click "Select Lesson Pack" to reveal multi-select checkboxes on every problem row.'],
          ['Assemble Problem Set', 'Check the problems for today’s class—a dark Lesson Pack floating bar tracks your count at the bottom.'],
          ['Copy Link or Show QR', 'Share a single sequenced study URL or classroom QR code so students solve the set in exact order.']
        ]
      },
      selectors: ['#tabBtnLessonPack', '#filterModeTabBar'],
      relatedIds: ['teacher_tools', 'classroom_code', 'filters']
    },
    {
      id: 'csat2027',
      category: 'find',
      chipLabel: { ko: '🎯 2027 수능관', en: '🎯 2027 CSAT' },
      title: {
        ko: '2027 수능 수학 전 46문항 특별관',
        en: '2027 CSAT All 46 Problems Hub'
      },
      body: {
        ko: '공통(1~22)·확통·미적분·기하 전 46문항의 출제 분석, 공식 정답표, 초등 눈높이 디딤돌 퀴즈까지 한 페이지에 모았습니다.',
        en: 'Explore all 46 problems across Common, Probability, Calculus, and Geometry with full analysis and stepping-stone quizzes.'
      },
      tipLine: {
        ko: '특별관 안에서 과목·4점·단답형 필터를 눌러 약점 문항만 추려 보세요.',
        en: 'Use the subject, 4-point, and short-answer filters inside the hub.'
      },
      details: {
        ko: [
          ['전 영역 46문항 완전 수록', '공통 22문항과 선택과목(확통·미적분·기하) 24문항 전체의 원문 분석과 정답표를 한눈에 봅니다.'],
          ['4점·주관식 맞춤 필터', '특별관 상단에서 4점 고난도 문항이나 단답형(주관식) 문항만 골라 집중 훈련할 수 있습니다.'],
          ['시각 도형·디딤돌 직결', '각 문항 카드를 클릭하면 초등 기초 직관부터 보조선 발상까지 단계별 퀴즈와 SVG 풀이가 열립니다.']
        ],
        en: [
          ['All 46 Official Items', 'Browse the complete Common (1–22) plus Probability, Calculus, and Geometry sets on one structured page.'],
          ['Point & Format Filters', 'Filter for 4-point high-difficulty or short-answer questions to focus on challenging topics.'],
          ['Direct Stepping-Stone Quizzes', 'Open any card to work through visual SVG explanations and elementary-to-advanced steps.']
        ]
      },
      selectors: ['a[href="csat2027.html"]'],
      relatedIds: ['filters', 'search', 'visual_proofs']
    },
    {
      id: 'visual_proofs',
      category: 'explore',
      chipLabel: { ko: '📐 시각 증명·영상', en: '📐 Visual Proofs' },
      title: {
        ko: '3,400+ 시각 증명 · 영상 게시판',
        en: '3,400+ Visual Proofs & Video Board'
      },
      body: {
        ko: '공식을 외우기 전에 보조선의 원리를 눈으로 확인하세요. 동적 기하 탐색관에서 GeoGebra·증명 PDF를 보고, 영상 게시판에서 1080p·쇼츠를 재생합니다.',
        en: 'See why auxiliary lines work before memorizing formulas—open GeoGebra proofs, PDFs, and step-by-step videos.'
      },
      tipLine: {
        ko: '"추천 영상 · #Shorts 극장" 서랍을 열면 대표 시각 증명을 바로 시청할 수 있습니다.',
        en: 'Open Featured Videos or the Video Board to watch visual proofs directly.'
      },
      details: {
        ko: [
          ['3,400+ 동적 기하 탐색관', '"📐 3,400+ 동적 기하·증명 검색"을 누르면 16대 영역 847+ 단계별 증명 PDF와 GeoGebra 앱렛을 바로 찾습니다.'],
          ['@min7014_ai 영상 게시판', '표준 설명 1080p 본편, 질문하는 수학 수업 본편, 45초 핵심 #Shorts 영상을 단원별로 시청하세요.'],
          ['이해 후 즉시 기출 실습', '각 증명 아래 링크로 방금 본 원리가 적용된 수능 기출 디딤돌 문제를 바로 풀어볼 수 있습니다.']
        ],
        en: [
          ['3,400+ Dynamic Archive', 'Open the Visual Proofs Search modal to browse 847+ step-by-step proof PDFs and GeoGebra/AlgeoMath applets.'],
          ['Video Proof Board', 'Watch 1080p standard explanations, Question-Asking Classroom editions, and concise #Shorts by topic.'],
          ['Watch, Then Practice', 'Jump straight from any visual proof to interactive stepping-stone exam problems using that theorem.']
        ]
      },
      selectors: ['a[href="video_board.html"]', 'a[onclick*="openMin7014ExplorerModal"]', '#btnQuickDrawerYt'],
      relatedIds: ['mathlab', 'deep_labs', 'search']
    },
    {
      id: 'mathlab',
      category: 'explore',
      chipLabel: { ko: '🛠️ MathLab', en: '🛠️ MathLab' },
      title: {
        ko: '동적 기하·대수 실험실 MathLab',
        en: 'Dynamic MathLab Studio'
      },
      body: {
        ko: '점·직선·원·포물선과 함수 그래프를 직접 작도하고 드래그하며 수학 원리를 발견하는 웹 실험실입니다.',
        en: 'Construct points, lines, conics, and function graphs directly and drag them live to discover invariants.'
      },
      tipLine: {
        ko: '내장된 대표 정리 프리셋을 불러오면 1초 만에 움직이는 증명을 실험합니다.',
        en: 'Load built-in proof presets to experiment immediately.'
      },
      details: {
        ko: [
          ['유클리드 실시간 작도', '점·직선·원·수직이등분선·접선을 캔버스에 작도한 뒤 점을 드래그하면 길이와 각의 불변량이 즉시 갱신됩니다.'],
          ['수식 그래프 동시 연동', '대수 입력창에 y=f(x) 함수나 원·이차곡선 식을 적으면 기하 도형과 교점이 실시간으로 함께 반응합니다.'],
          ['대표 정리 프리셋 1초 실행', '피타고라스·원주각·체바 정리 등 내장 프리셋을 열어 곧바로 보조선을 실험해 보세요.']
        ],
        en: [
          ['Live Euclidean Construction', 'Draw points, lines, circles, and tangents on the canvas and drag vertices live to observe geometric invariants.'],
          ['Algebraic Curve Plotting', 'Enter functions or conics alongside geometry objects to inspect intersections and tangent behavior together.'],
          ['1-Click Proof Presets', 'Load curated presets (Pythagoras, Inscribed Angles, Ceva) to experiment without drawing from scratch.']
        ]
      },
      selectors: ['a[href="mathlab.html"]'],
      relatedIds: ['visual_proofs', 'deep_labs', 'csat2027']
    },
    {
      id: 'deep_labs',
      category: 'explore',
      chipLabel: { ko: '🔬 탐구 실험실', en: '🔬 Math Labs' },
      title: {
        ko: '심층 수학 탐구 연구실 5종',
        en: '5 Interactive Exploration Labs'
      },
      body: {
        ko: '16대 단원 도슨트, 3분 유레카 미션, 폴리아·오개념 백신, 프랙탈 실험실, 구슬·대수타일 아카데미 탭을 눌러 슬라이더를 움직여 보세요.',
        en: 'Open any of the 5 exploration tabs—16-domain proofs, Eureka missions, fallacy lab, fractals, and Desmos/Polypad play.'
      },
      tipLine: {
        ko: '열려 있는 연구실 탭을 다시 누르면 화면이 깔끔하게 접힙니다.',
        en: 'Click an open lab tab again anytime to collapse it.'
      },
      details: {
        ko: [
          ['5개 연구실 탭 선택', '단원 도슨트 · 3분 유레카 · 교사 5대 스튜디오 · 프랙탈 · 글로벌 아카데미 탭 중 원하는 연구실을 엽니다.'],
          ['Desmos 구슬 · Polypad 체험', '아카데미 탭에서 기울기·절편 슬라이더를 맞춰 구슬을 굴리거나 대수타일로 (x+a)(x+b) 넓이를 조립하세요.'],
          ['사색 후 기출 문제 직결', '실험실 하단 "기출 도전하기" 버튼을 누르면 방금 이해한 원리가 쓰인 수능·모평 문항 목록으로 바로 이어집니다.']
        ],
        en: [
          ['Switch 5 Specialized Labs', 'Select tabs for 16-Domain Proofs, Eureka Missions, Teacher Pedagogy Studio, Fractals, or Function/Tile Labs.'],
          ['Interactive Sliders & Tiles', 'Tune slope/intercept sliders to launch marbles or assemble (x+a)(x+b) algebra tiles hands-on.'],
          ['Connect to Exam Practice', 'Use the bottom action buttons in any lab to jump directly to matching stepping-stone exam questions.']
        ]
      },
      selectors: ['#deepMathLabsTabBar', '#deepMathLabsHub'],
      relatedIds: ['mathlab', 'visual_proofs', 'quest_streak']
    },
    {
      id: 'classroom_code',
      category: 'teach',
      chipLabel: { ko: '🔑 수업 코드 입장', en: '🔑 Class Code' },
      title: {
        ko: '수업 코드 5초 입장',
        en: '5-Second Classroom Entry'
      },
      body: {
        ko: '선생님이 안내한 수업 코드(예: MATH-A8F2)를 입력하고 입장을 누르면 교실 전용 문제와 실시간 현황으로 바로 연결됩니다.',
        en: 'Enter your teacher-shared classroom code and tap Join to enter the assigned lesson right away.'
      },
      tipLine: {
        ko: '수업 코드가 없어도 아래 모든 문제와 자료는 100% 자유롭게 풀 수 있습니다.',
        en: 'No code needed—every quiz and visual proof is freely open.'
      },
      details: {
        ko: [
          ['교사 안내 코드 입력', '칠판이나 안내문으로 받은 수업 코드(예: MATH-A8F2)를 입력 칸에 그대로 적어 넣습니다.'],
          ['1클릭 수업실 진입', '"입장" 버튼을 누르면 선생님이 배정한 오늘의 디딤돌 문제 세트와 제출 현황이 바로 열립니다.'],
          ['코드 없는 자율 학습 가능', '개인 학습자는 수업 코드를 비워 둔 채 아래 16,594+ 문항과 모든 자료를 무료로 풀 수 있습니다.']
        ],
        en: [
          ['Enter Class Code', 'Type the alphanumeric code shared by your instructor (e.g., MATH-A8F2) into the class code input field.'],
          ['Instant Room Access', 'Click "Join" to jump straight to your teacher’s curated stepping-stone lesson set.'],
          ['Freely Open Without Code', 'Studying independently? Leave the box blank and solve all 16,594+ quizzes and proofs anytime free.']
        ]
      },
      selectors: ['#inputRoomCode', 'button[onclick*="joinClassroom"]'],
      relatedIds: ['teacher_tools', 'lesson_pack', 'wrong_bookmarks']
    },
    {
      id: 'teacher_tools',
      category: 'teach',
      chipLabel: { ko: '👩‍🏫 교사·오프라인', en: '👩‍🏫 Teacher Tools' },
      title: {
        ko: '교사 · 출제 · 오프라인 보관함',
        en: 'Teacher, Authoring & Offline Vault'
      },
      body: {
        ko: '칠판용 3초 수업 QR 개설, 실시간 교실 대시보드, 기출 디딤돌 자동 출제, 인터넷 없이 쓰는 오프라인 단독 퀴즈까지 모두 무료입니다.',
        en: 'Launch 3-second class QR codes, live dashboards, problem authoring, and offline standalone quizzes—all 100% free.'
      },
      tipLine: {
        ko: '"교사·출제·오프라인 도구 ▾" 서랍에서 출제·대시보드·오프라인 링크를 바로 엽니다.',
        en: 'Toggle the Teacher & Offline drawer to access every classroom utility.'
      },
      details: {
        ko: [
          ['교사·출제 서랍 펼치기', '"👩‍🏫 교사·출제·오프라인 도구 ▾" 버튼을 누르면 맞춤형 문제 출제, 교실 대시보드, 오프라인 보관함 메뉴가 열립니다.'],
          ['칠판 QR · 교실 3초 개설', '우측 하단 "🚀 이 문제로 수업 열기"나 교사 대시보드로 학생 접속용 QR코드와 실시간 현황판을 3초 만에 엽니다.'],
          ['오프라인 단독 HTML 패키지', '학교 방화벽이나 Wi-Fi 불안정 환경에서는 오프라인 보관함에서 단일 HTML 퀴즈 파일을 무료로 열어 수업하세요.']
        ],
        en: [
          ['Expand Tools Drawer', 'Click "Teacher, Studio & Offline Tools" to reveal Authoring Studio, Classroom Dashboard, and Offline Vault links.'],
          ['3-Second Class & QR', 'Open the bottom-right "Open Classroom" action or dashboard to display a scannable join QR on your board.'],
          ['Standalone Offline Packs', 'Download or open self-contained offline quiz files for classrooms without reliable internet access.']
        ]
      },
      selectors: ['#btnQuickDrawerTools', '#teacherQuickToolsDrawer', 'a[data-path="classroom-and-qr"]'],
      prepareAction: function () {
        var drawer = document.getElementById('teacherQuickToolsDrawer');
        if (drawer && drawer.style.display === 'none' && typeof window.toggleHomeQuickDrawer === 'function') {
          try { window.toggleHomeQuickDrawer('tools'); } catch (e) {}
        }
      },
      relatedIds: ['lesson_pack', 'classroom_code', 'report_drag']
    },
    {
      id: 'quest_streak',
      category: 'study',
      chipLabel: { ko: '🎮 3D 성전·스트릭', en: '🎮 3D Quest' },
      title: {
        ko: '3D 수학의 성전 & 학습 스트릭',
        en: '3D Math Sanctuary & Streaks'
      },
      body: {
        ko: '3D 보스 레이드와 원정대 퀘스트로 단원 개념을 정복하고, 상단 불꽃 배지를 눌러 연속 출석 스트릭과 뱃지를 확인하세요.',
        en: 'Master concepts through 3D boss battles and track your daily study streak and achievement badges in the header.'
      },
      tipLine: {
        ko: '매일 한 문제씩 풀면 연속 학습 불꽃과 경험치(XP)가 쌓입니다.',
        en: 'Solve a quiz or puzzle each day to keep your streak flame alive.'
      },
      details: {
        ko: [
          ['3D 수학의 성전 탐험', '바로가기에서 "🎮 수학의 성전 3D 퀘스트"를 열면 3D 월드맵과 단원 보스 배틀을 통해 개념을 게임처럼 정복합니다.'],
          ['깊은 사색 & 유레카 보상', '게임 내에서도 연습장·사색 결계 시간 정지를 지원하며, 차분히 추론해 맞히면 DEEP EUREKA 보너스를 받습니다.'],
          ['불꽃 스트릭 & 성취 뱃지', '상단 주황색 불꽃(🔥) 배지를 누르면 누적 스트릭·레벨·획득 뱃지 현황을 언제든 확인할 수 있습니다.']
        ],
        en: [
          ['Enter 3D Math Sanctuary', 'Click "3D Math Sanctuary Quest" to explore mathematical worlds and defeat concept bosses through real problem solving.'],
          ['Deep Contemplation Time', 'Use in-game time-freeze scratchpads to reason carefully—deep contemplation earns extra Eureka bonuses.'],
          ['Daily Streak & Badges', 'Click the top-right flame badge anytime to view your consecutive study streak, XP level, and earned badges.']
        ]
      },
      selectors: ['a[href="game.html"]', '#headerStreakCount'],
      relatedIds: ['wrong_bookmarks', 'deep_labs', 'mathlab']
    },
    {
      id: 'theme_lang',
      category: 'settings',
      chipLabel: { ko: '🌙 테마·언어', en: '🌙 Theme & Lang' },
      title: {
        ko: '다크/라이트 테마 & 한·영 전환',
        en: 'Dark/Light Theme & KO/EN Switch'
      },
      body: {
        ko: '상단 우측 🌙/☀️ 버튼으로 눈이 편안한 다크 모드를 켜고, KO | EN 버튼으로 문제·해설·메뉴 전체를 영어로 바꿀 수 있습니다.',
        en: 'Switch between crisp Light and cosmic Dark themes or toggle full Korean/English localization from the top header.'
      },
      tipLine: {
        ko: '선택한 테마와 언어는 다음 방문 시에도 자동으로 유지됩니다.',
        en: 'Your theme and language preference stay saved automatically.'
      },
      details: {
        ko: [
          ['다크 / 라이트 즉시 전환', '야간 학습이나 칠판 프로젝터 환경에서는 상단 "🌙 다크 / ☀️ 라이트" 버튼으로 눈의 피로를 줄이세요.'],
          ['완전 한·영 이중언어(KO | EN)', '"KO | EN" 전환 시 메뉴·검색 필터·문항·단계별 해설·수식 안내와 이 도우미까지 100% 영문으로 전환됩니다.'],
          ['자동 브라우저 저장', '한 번 선택한 테마와 언어 설정은 브라우저에 안전하게 저장되어 다음 방문 시에도 그대로 적용됩니다.']
        ],
        en: [
          ['Light & Dark Themes', 'Toggle the header sun/moon button to switch between crisp Light Atelier and Cosmic Dark modes.'],
          ['Full KO / EN Bilingual UI', 'Switching "KO | EN" translates menus, filters, stepping-stone quizzes, solutions, and this guide seamlessly.'],
          ['Persists Automatically', 'Your preferred theme and language are remembered across visits in browser storage.']
        ]
      },
      selectors: ['#themeToggleGlobalBtn', '#langToggleSingleBtn'],
      relatedIds: ['report_drag', 'search', 'welcome']
    },
    {
      id: 'report_drag',
      category: 'settings',
      chipLabel: { ko: '🚨 오류신고·이동', en: '🚨 Siren & Move' },
      title: {
        ko: '오류 사이렌 신고 & 별 이동',
        en: 'Issue Siren & Drag Star Orb'
      },
      body: {
        ko: '수식이나 정답 이상은 우측 상단 빨간 사이렌("오류신고")을 눌러 해당 영역을 클릭해 제보하세요. 이 별 아이콘은 어디든 드래그됩니다.',
        en: 'Spot a typo or math bug? Tap the top-right Siren, then click the target area. Drag this floating star anywhere you like.'
      },
      tipLine: {
        ko: '위치를 옮긴 뒤 카드 상단 ↺ 버튼을 누르면 기본 자리로 돌아옵니다.',
        en: 'Tap ↺ in this card header anytime to return to the default corner.'
      },
      details: {
        ko: [
          ['영역 지정 오류 사이렌', '우측 상단 "오류신고" 버튼을 누른 뒤 이상이 보이는 문제·그림·수식을 직접 클릭하면 해당 요소가 자동 캡처되어 신고됩니다.'],
          ['별 아이콘 & 창 자유 드래그', '반짝이는 별(✦)이나 안내 창 상단 "⠿" 손잡이를 드래그하면 가려지는 곳 없이 화면 어디든 옮길 수 있습니다.'],
          ['기본 위치 복귀 & 음소거', '드래그 후 상단 ↺ 버튼으로 원위치 복귀가 가능하며, "🔔 자동 안내" 버튼으로 자동 팝업 여부를 제어할 수 있습니다.']
        ],
        en: [
          ['Point-and-Click Siren Report', 'Click top-right "Report Issue" then tap any element on screen—the inspector automatically captures context for fast repair.'],
          ['Freely Drag Star or Header', 'Grab the glowing star orb or the card "⠿" grip bar to move it anywhere clear of your active problem.'],
          ['Reset Position or Mute Auto', 'Tap ↺ in the header bar to snap back to default position, or toggle "Auto tips" ON/OFF anytime.']
        ]
      },
      selectors: ['#mathedu-report-fab', '#matheduGuideOrb'],
      relatedIds: ['theme_lang', 'search', 'welcome']
    }
  ];

  var TOPIC_MAP = {};
  for (var ti = 0; ti < TOPICS.length; ti++) {
    TOPIC_MAP[TOPICS[ti].id] = TOPICS[ti];
  }

  var QUICK_PICK_IDS = ['search', 'filters', 'visual_proofs', 'deep_labs', 'teacher_tools', 'theme_lang'];
  var INTENT_PICK_IDS = ['search', 'visual_proofs', 'teacher_tools', 'deep_labs'];

  // Passive global reaction triggers: first matching rule wins.
  var CLICK_RULES = [
    { match: '#mobileHeaderSearchToggleBtn, #headerGlobalSearchForm button', topicId: 'search' },
    { match: '#tabBtnLessonPack, .card-pack-checkbox', topicId: 'lesson_pack' },
    { match: '#tabBtnWrong, #tabBtnBookmarks, .card-bookmark-btn, #studentLibraryQuickBar, button[onclick*="MatheduAuth"], a[data-path="my-room"]', topicId: 'wrong_bookmarks' },
    { match: '.stitch-subj-pill, .stitch-year-pill, #filterYear, #filterSubject, #filterGrade, #filterMonth, #filterNum, .topic-chip, #btnRandomQuizChallenge, #quizFilterBar details summary', topicId: 'filters' },
    { match: 'a[href="csat2027.html"]', topicId: 'csat2027' },
    { match: 'a[href="mathlab.html"]', topicId: 'mathlab' },
    { match: 'a[href="video_board.html"], a[onclick*="openMin7014ExplorerModal"], #btnQuickDrawerYt, #homeYtCinemaChips button, #homeYtShortsQuickBar button, a[data-path="geogebra-3d-explorer"]', topicId: 'visual_proofs' },
    { match: '#deepMathLabsTabBar button[data-deep-tab], button[onclick*="switchHomeDeepLabTab"], #benchmarkAcademyTabs button, #wonderLabModeTabs button, #btnCollapseDeepLabs', topicId: 'deep_labs' },
    { match: 'button[onclick*="joinClassroom"]', topicId: 'classroom_code' },
    { match: '#btnQuickDrawerTools, #teacherQuickToolsDrawer a, #teacherQuickToolsDrawer button, a[data-path="classroom-and-qr"]', topicId: 'teacher_tools' },
    { match: 'a[href="game.html"], div[onclick*="showBadgesModal"], #headerStreakCount', topicId: 'quest_streak' },
    { match: '#themeToggleGlobalBtn, #langToggleSingleBtn', topicId: 'theme_lang' }
  ];

  var FOCUS_RULES = [
    { match: '#headerGlobalSearchInput, #quizSearchInput', topicId: 'search' },
    { match: '#inputRoomCode', topicId: 'classroom_code' }
  ];

  var INPUT_RULES = [
    { match: '#wonderSlider1, #wonderSlider2, #marbleParamASlider, #marbleParamBSlider, #polySlider1, #polySlider2', topicId: 'deep_labs' },
    { match: '#headerGlobalSearchInput, #quizSearchInput', topicId: 'search' }
  ];

  var STORAGE_TIMER_KEY = 'mathedu_star_timer_v1';
  var STORAGE_PAD_KEY = 'mathedu_star_pad_v1';

  var COPY = {
    ko: {
      orbLabel: '유클리드 별 성좌 허브 (클릭 시 4탭 도크·자세한 안내 열기 · 드래그 이동)',
      dragPill: '드래그 · 별 허브',
      badgePrefix: '성좌 허브',
      tabs: { guide: '✨ 안내', tools: '🛠️ 툴', study: '📊 내 학습', pad: '✏️ 연습장' },
      tierNames: ['Lv.1 샛별', 'Lv.2 아쿠아 성좌', 'Lv.3 인디고 탐구별', 'Lv.4 프리즘 별', 'Lv.5 황금 성좌'],
      quickLangBtn: '한/영',
      quickLangTitle: '한국어 / English 언어 전환',
      quickThemeTitle: '다크 / 라이트 테마 전환',
      quickVoiceTitle: '음성 도슨트로 듣기 / 멈추기',
      quickTuckTitle: '화면 가장자리로 반접기',
      tuckedToast: '✨ 별을 가장자리에 접었어요. 누르면 다시 열립니다!',
      detailHeading: '📖 자세한 사용 방법',
      detailOpenBtn: '📖 자세히 보기',
      detailCloseBtn: '간략히 ▴',
      dragHandleTitle: '드래그하여 아이콘과 창 이동',
      resetPosTitle: '기본 위치로 되돌리기',
      closeTitle: '별 아이콘으로 접기',
      locateBtn: '📍 위치 보기',
      quickLabel: '필요한 사용법 바로 보기',
      relatedLabel: '이어서 보기',
      allToggleOpen: '전체 14개 목록 ▴',
      allToggleClosed: '전체 14개 목록 ▾',
      autoOnLabel: '🔔 자동 안내 ON',
      autoOffLabel: '🔕 자동 안내 OFF',
      autoOnTitle: '새 기능을 처음 누를 때 자동으로 한 개씩 안내합니다 (클릭하여 끄기)',
      autoOffTitle: '자동 팝업을 껐습니다. 필요할 때 별을 눌러 확인하세요 (클릭하여 켜기)',
      posSavedToast: '✓ 위치가 저장되었어요! 별을 누르면 언제든 열립니다',
      seenCountUnit: '개 확인됨',
      dailyBadge: '🌟 오늘의 1분 시각 유레카',
      dailyPdfBtn: '📄 증명 PDF',
      dailyYtBtn: '🎬 영상 보기',
      dailyVoiceBtn: '🔊 음성 해설',
      launcherTitle: '6대 핵심 기능 1초 실행',
      toolsGrid: [
        { act: 'omni-search', icon: '🔍', label: '통합 검색' },
        { act: 'mathlab', icon: '🛠️', label: 'MathLab' },
        { act: 'explorer', icon: '📐', label: '3,400+ 증명' },
        { act: 'random-quiz', icon: '🎲', label: '랜덤 1문제' },
        { act: 'lesson-pack', icon: '🎒', label: '수업 팩' },
        { act: 'invite-qr', icon: '✉️', label: '무료 초대·QR' }
      ],
      inviteCopiedToast: '✓ 무료 학습 초대 문구가 복사되었어요! (+15 XP)',
      inviteMsg: '📐 공식 암기 없이 눈으로 깨우치는 수학! 민은기 선생님의 수학자료실(https://min7014.github.io/) × mathedu (16,594+ 디딤돌 문항·회원가입 100% 무료): https://min7014.github.io/mathedu/',
      studyKpis: { streak: '🔥 연속 스트릭', solved: '✅ 해결 문항', wrong: '⚡ 오답 노트', saved: '⭐ 즐겨찾기' },
      studyActions: {
        revenge: '⚡ 오답 리벤지 출격',
        clinic: '🩺 오답 클리닉',
        quest: '🎮 3D 성전'
      },
      noWrongToast: '👍 현재 오답이 없어요! 랜덤 1문제나 3D 성전에 도전해 보세요.',
      timerHeading: '🧘 유레카 사색 결계 타이머',
      timerSub: '찍지 않고 차분히 생각하며 완주하면 +50 XP 보상!',
      timer15: '15분 사색',
      timer25: '25분 몰입',
      timerPause: '⏸ 일시정지',
      timerResume: '▶ 재개',
      timerReset: '↺ 초기화',
      timerDoneToast: '🎉 사색 결계 완주! +50 XP 유레카 보상이 지급되었습니다!',
      padHeading: '✏️ 미니 보조선 연습장 (Pocket Scratchpad)',
      padSub: '계산 전 보조선·대칭선을 먼저 그려 보세요.',
      padEraser: '지우개',
      padUndo: '↶ 되돌리기',
      padClear: '🗑️ 지우기',
      padMathLab: '🛠️ MathLab 확장 ➔',
      padClearedToast: '연습장을 깨끗이 지웠습니다.'
    },
    en: {
      orbLabel: 'Euclid Star Hub (Click for 4-Tab Dock & Detailed Guide, drag to move)',
      dragPill: 'Drag · Star Hub',
      badgePrefix: 'Star Hub',
      tabs: { guide: '✨ Guide', tools: '🛠️ Tools', study: '📊 Study', pad: '✏️ Sketch' },
      tierNames: ['Lv.1 Nova Star', 'Lv.2 Aqua Star', 'Lv.3 Indigo Star', 'Lv.4 Prism Star', 'Lv.5 Golden Constellation'],
      quickLangBtn: 'KO/EN',
      quickLangTitle: 'Switch Korean / English language',
      quickThemeTitle: 'Toggle Dark / Light theme',
      quickVoiceTitle: 'Listen / Stop Voice Docent',
      quickTuckTitle: 'Tuck star orb to screen edge',
      tuckedToast: '✨ Tucked to screen edge. Tap anytime to reopen!',
      detailHeading: '📖 Detailed Walkthrough',
      detailOpenBtn: '📖 Details',
      detailCloseBtn: 'Compact ▴',
      dragHandleTitle: 'Drag to reposition orb and card',
      resetPosTitle: 'Reset to default spot',
      closeTitle: 'Collapse to star orb',
      locateBtn: '📍 Locate',
      quickLabel: 'Jump to what you need',
      relatedLabel: 'Related',
      allToggleOpen: 'All 14 tips ▴',
      allToggleClosed: 'All 14 tips ▾',
      autoOnLabel: '🔔 Auto tips ON',
      autoOffLabel: '🔕 Auto tips OFF',
      autoOnTitle: 'Shows one tip automatically the first time you touch a feature (Click to mute)',
      autoOffTitle: 'Quiet mode: tap the floating star whenever you need detailed steps (Click to enable)',
      posSavedToast: '✓ Position saved! Tap star anytime',
      seenCountUnit: 'seen',
      dailyBadge: '🌟 Daily 1-Min Visual Eureka',
      dailyPdfBtn: '📄 Proof PDF',
      dailyYtBtn: '🎬 Watch Video',
      dailyVoiceBtn: '🔊 Voice Guide',
      launcherTitle: '6 Core Tools · 1-Click Launch',
      toolsGrid: [
        { act: 'omni-search', icon: '🔍', label: 'Omni-Search' },
        { act: 'mathlab', icon: '🛠️', label: 'MathLab' },
        { act: 'explorer', icon: '📐', label: '3,400+ Proofs' },
        { act: 'random-quiz', icon: '🎲', label: 'Random Quiz' },
        { act: 'lesson-pack', icon: '🎒', label: 'Lesson Pack' },
        { act: 'invite-qr', icon: '✉️', label: 'Free Invite & QR' }
      ],
      inviteCopiedToast: '✓ Free math invite copied! (+15 XP)',
      inviteMsg: '📐 Visual Intuition Beyond Rote Formulas! 3,400+ Dynamic Proofs & 16,594+ Stepping-Stone Math Quizzes—100% Free Forever: https://min7014.github.io/mathedu/?lang=en',
      studyKpis: { streak: '🔥 Streak', solved: '✅ Solved', wrong: '⚡ Review Vault', saved: '⭐ Bookmarks' },
      studyActions: {
        revenge: '⚡ Weak-Point Revenge',
        clinic: '🩺 Step Clinic',
        quest: '🎮 3D Quest'
      },
      noWrongToast: '👍 Zero missed problems! Try a Random Quiz or 3D Quest.',
      timerHeading: '🧘 Deep Eureka Contemplation Timer',
      timerSub: 'Think deeply without guessing—complete a focus block for +50 XP!',
      timer15: '15m Focus',
      timer25: '25m Deep',
      timerPause: '⏸ Pause',
      timerResume: '▶ Resume',
      timerReset: '↺ Reset',
      timerDoneToast: '🎉 Deep Eureka session complete! +50 XP awarded!',
      padHeading: '✏️ Pocket Auxiliary-Line Scratchpad',
      padSub: 'Sketch auxiliary lines and symmetry before computing.',
      padEraser: 'Eraser',
      padUndo: '↶ Undo',
      padClear: '🗑️ Clear',
      padMathLab: '🛠️ Expand in MathLab ➔',
      padClearedToast: 'Scratchpad cleared.'
    }
  };

  var state = {
    open: true,
    detailed: false,
    activeTab: 'guide', // 'guide' | 'tools' | 'study' | 'pad'
    activeTopicId: 'welcome',
    seenTopics: {},
    autoTips: true,
    hasDraggedOnce: false,
    showAllTopics: false,
    edgeTucked: null, // null | 'left' | 'right'
    customPos: null, // { rx, ry } normalized [0..1]
    left: null,
    top: null
  };

  var timerState = {
    durationSec: 900,
    remainingSec: 900,
    running: false,
    endAtMs: 0
  };
  var timerInterval = null;

  var padStrokes = [];
  var padColor = '#0284c7';
  var padEraser = false;
  var isDrawingPad = false;
  var inviteRewardedSession = false;

  var rootEl = null;
  var orbEl = null;
  var orbTimerBadgeEl = null;
  var dragHintEl = null;
  var toastPillEl = null;
  var progressCircleEl = null;
  var cardEl = null;

  var activeSpotlightEls = [];
  var spotlightTimer = null;
  var toastTimer = null;
  var dragSession = null;
  var lastAutoTriggerAt = 0;
  var lastRenderedLang = null;
  var lastRenderedDark = null;

  function getLang() {
    if (window.MatheduI18n && typeof window.MatheduI18n.getLanguage === 'function') {
      return window.MatheduI18n.getLanguage() === 'en' ? 'en' : 'ko';
    }
    var hl = (document.documentElement.getAttribute('lang') || 'ko').toLowerCase();
    return hl.indexOf('en') === 0 ? 'en' : 'ko';
  }

  function isDark() {
    var html = document.documentElement;
    var body = document.body;
    return !!(
      html.classList.contains('dark-theme') ||
      html.classList.contains('dark') ||
      html.getAttribute('data-theme') === 'dark' ||
      (body && body.classList.contains('dark-mode'))
    );
  }

  function isInspectorActive() {
    if (document.body && document.body.classList.contains('mathedu-inspect-active')) return true;
    var banner = document.getElementById('mathedu-inspect-banner');
    return !!(banner && window.getComputedStyle(banner).display !== 'none');
  }

  function getOrbSize() {
    return window.innerWidth < 640 ? 46 : 52;
  }

  function countSeenTopics() {
    var cnt = 0;
    for (var i = 0; i < TOPICS.length; i++) {
      if (state.seenTopics[TOPICS[i].id]) cnt++;
    }
    return cnt;
  }

  function loadPersistedState() {
    try {
      var raw = localStorage.getItem(STORAGE_STATE_KEY);
      if (raw) {
        var p = JSON.parse(raw);
        if (p && typeof p === 'object') {
          if (typeof p.open === 'boolean') state.open = p.open;
          if (typeof p.detailed === 'boolean') state.detailed = p.detailed;
          if (p.activeTab && ['guide', 'tools', 'study', 'pad'].indexOf(p.activeTab) !== -1) {
            state.activeTab = p.activeTab;
          }
          if (typeof p.activeTopicId === 'string' && TOPIC_MAP[p.activeTopicId]) {
            state.activeTopicId = p.activeTopicId;
          }
          if (p.seenTopics && typeof p.seenTopics === 'object') {
            state.seenTopics = p.seenTopics;
          }
          if (typeof p.autoTips === 'boolean') state.autoTips = p.autoTips;
          if (p.hasDraggedOnce) state.hasDraggedOnce = true;
          if (p.edgeTucked === 'left' || p.edgeTucked === 'right') {
            state.edgeTucked = p.edgeTucked;
          }
        }
      }
      var rawPos = localStorage.getItem(STORAGE_POS_KEY);
      if (rawPos) {
        var pos = JSON.parse(rawPos);
        if (pos && typeof pos.rx === 'number' && typeof pos.ry === 'number') {
          state.customPos = {
            rx: Math.max(0, Math.min(1, pos.rx)),
            ry: Math.max(0, Math.min(1, pos.ry))
          };
        }
      }
    } catch (e) {}
    loadTimerState();
    loadPadStrokes();
  }

  function saveState() {
    try {
      localStorage.setItem(STORAGE_STATE_KEY, JSON.stringify({
        open: !!state.open,
        detailed: !!state.detailed,
        activeTab: state.activeTab,
        activeTopicId: state.activeTopicId,
        seenTopics: state.seenTopics,
        autoTips: !!state.autoTips,
        hasDraggedOnce: !!state.hasDraggedOnce,
        edgeTucked: state.edgeTucked
      }));
    } catch (e) {}
  }

  function savePos() {
    try {
      if (state.customPos) {
        localStorage.setItem(STORAGE_POS_KEY, JSON.stringify(state.customPos));
      } else {
        localStorage.removeItem(STORAGE_POS_KEY);
      }
    } catch (e) {}
  }

  function formatTimerMMSS(sec) {
    var s = Math.max(0, Math.floor(sec));
    var m = Math.floor(s / 60);
    var r = s % 60;
    return (m < 10 ? '0' : '') + m + ':' + (r < 10 ? '0' : '') + r;
  }

  function saveTimerState() {
    try {
      localStorage.setItem(STORAGE_TIMER_KEY, JSON.stringify({
        durationSec: timerState.durationSec,
        remainingSec: timerState.remainingSec,
        running: timerState.running,
        endAtMs: timerState.endAtMs
      }));
    } catch (e) {}
  }

  function syncTimerVisualsOnly() {
    var txt = formatTimerMMSS(timerState.remainingSec);
    if (orbTimerBadgeEl) {
      if (timerState.running && !state.open) {
        orbTimerBadgeEl.textContent = txt;
        orbTimerBadgeEl.style.display = 'block';
      } else {
        orbTimerBadgeEl.style.display = 'none';
      }
    }
    var clk = document.getElementById('mgTimerClock');
    if (clk) clk.textContent = txt;
    var pauseBtn = document.getElementById('mgTimerPauseBtn');
    if (pauseBtn) {
      var c = COPY[getLang()];
      pauseBtn.textContent = timerState.running ? c.timerPause : c.timerResume;
    }
  }

  function handleTimerComplete() {
    if (timerInterval) {
      clearInterval(timerInterval);
      timerInterval = null;
    }
    timerState.running = false;
    timerState.remainingSec = 0;
    timerState.endAtMs = 0;
    saveTimerState();

    var lang = getLang();
    var c = COPY[lang];
    try {
      if (window.MatheduGame && typeof window.MatheduGame.addXP === 'function') {
        window.MatheduGame.addXP(50, lang === 'en' ? 'Deep Eureka Focus Complete' : '유레카 사색 결계 완주');
      }
      if (window.MatheduGame && typeof window.MatheduGame.triggerConfetti === 'function') {
        window.MatheduGame.triggerConfetti(2500);
      }
    } catch (e) {}
    pulseOrbBriefly();
    showMiniToast(c.timerDoneToast);
    syncTimerVisualsOnly();
    updateOrbStarTier();
    if (state.open && state.activeTab === 'study') {
      renderCardContent(false);
    }
  }

  function ensureTimerTicker() {
    if (timerInterval) clearInterval(timerInterval);
    if (!timerState.running) return;
    timerInterval = setInterval(function () {
      if (!timerState.running) return;
      var rem = Math.max(0, Math.ceil((timerState.endAtMs - Date.now()) / 1000));
      timerState.remainingSec = rem;
      syncTimerVisualsOnly();
      if (rem <= 0) {
        handleTimerComplete();
      }
    }, 500);
  }

  function startTimer(seconds) {
    var sec = Math.max(1, parseInt(seconds, 10) || 900);
    timerState.durationSec = sec;
    timerState.remainingSec = sec;
    timerState.running = true;
    timerState.endAtMs = Date.now() + sec * 1000;
    saveTimerState();
    ensureTimerTicker();
    syncTimerVisualsOnly();
    if (state.open && state.activeTab === 'study') renderCardContent(false);
  }

  function toggleTimerPause() {
    if (timerState.running) {
      timerState.remainingSec = Math.max(0, Math.ceil((timerState.endAtMs - Date.now()) / 1000));
      timerState.running = false;
      timerState.endAtMs = 0;
      if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
      }
    } else {
      var base = timerState.remainingSec > 0 ? timerState.remainingSec : timerState.durationSec;
      timerState.remainingSec = base;
      timerState.running = true;
      timerState.endAtMs = Date.now() + base * 1000;
      ensureTimerTicker();
    }
    saveTimerState();
    syncTimerVisualsOnly();
  }

  function resetTimer() {
    if (timerInterval) {
      clearInterval(timerInterval);
      timerInterval = null;
    }
    timerState.running = false;
    timerState.remainingSec = timerState.durationSec || 900;
    timerState.endAtMs = 0;
    saveTimerState();
    syncTimerVisualsOnly();
  }

  function loadTimerState() {
    try {
      var raw = localStorage.getItem(STORAGE_TIMER_KEY);
      if (!raw) return;
      var t = JSON.parse(raw);
      if (!t || typeof t !== 'object') return;
      if (typeof t.durationSec === 'number') timerState.durationSec = t.durationSec;
      if (t.running && typeof t.endAtMs === 'number') {
        var rem = Math.max(0, Math.ceil((t.endAtMs - Date.now()) / 1000));
        if (rem > 0) {
          timerState.running = true;
          timerState.endAtMs = t.endAtMs;
          timerState.remainingSec = rem;
          ensureTimerTicker();
        } else {
          timerState.running = false;
          timerState.remainingSec = timerState.durationSec;
          timerState.endAtMs = 0;
        }
      } else if (typeof t.remainingSec === 'number') {
        timerState.remainingSec = t.remainingSec;
      }
    } catch (e) {}
  }

  function loadPadStrokes() {
    try {
      var raw = sessionStorage.getItem(STORAGE_PAD_KEY);
      if (raw) {
        var arr = JSON.parse(raw);
        if (Array.isArray(arr)) padStrokes = arr;
      }
    } catch (e) {}
  }

  function savePadStrokes() {
    try {
      sessionStorage.setItem(STORAGE_PAD_KEY, JSON.stringify(padStrokes.slice(-120)));
    } catch (e) {}
  }

  function getStudySnapshot() {
    var streak = 0;
    var xp = 0;
    var wrongs = [];
    var bookmarks = [];
    var solved = [];
    try {
      if (window.MatheduGame) {
        if (typeof window.MatheduGame.getStreak === 'function') streak = (window.MatheduGame.getStreak() || {}).count || 0;
        if (typeof window.MatheduGame.getXP === 'function') xp = window.MatheduGame.getXP() || 0;
        if (typeof window.MatheduGame.getWrongAnswers === 'function') wrongs = window.MatheduGame.getWrongAnswers() || [];
        if (typeof window.MatheduGame.getBookmarks === 'function') bookmarks = window.MatheduGame.getBookmarks() || [];
      }
      if (window.MatheduAuth && typeof window.MatheduAuth.getSolvedProblems === 'function') {
        solved = window.MatheduAuth.getSolvedProblems() || [];
      }
    } catch (e) {}
    return {
      streak: streak,
      xp: xp,
      wrongs: wrongs,
      bookmarks: bookmarks,
      solved: solved
    };
  }

  function computeStarTier() {
    var snap = getStudySnapshot();
    var score = snap.solved.length * 2 + countSeenTopics() + snap.streak + Math.floor(snap.xp / 50);
    if (score >= 35) return 5;
    if (score >= 20) return 4;
    if (score >= 10) return 3;
    if (score >= 4) return 2;
    return 1;
  }

  function updateOrbStarTier() {
    if (!orbEl) return;
    orbEl.setAttribute('data-star-tier', String(computeStarTier()));
  }

  function clampCoords(left, top) {
    var sz = getOrbSize();
    var padX = 12;
    var minY = 14;
    var maxX = Math.max(padX, window.innerWidth - sz - padX);
    var maxY = Math.max(minY, window.innerHeight - sz - 14);
    return {
      left: Math.round(Math.max(padX, Math.min(maxX, left))),
      top: Math.round(Math.max(minY, Math.min(maxY, top))),
      minX: padX,
      maxX: maxX,
      minY: minY,
      maxY: maxY
    };
  }

  function syncCoordsToViewport() {
    var sz = getOrbSize();
    var bounds = clampCoords(0, 0);
    if (state.customPos) {
      var targetL = bounds.minX + state.customPos.rx * (bounds.maxX - bounds.minX);
      var targetT = bounds.minY + state.customPos.ry * (bounds.maxY - bounds.minY);
      var clamped = clampCoords(targetL, targetT);
      state.left = clamped.left;
      state.top = clamped.top;
    } else {
      var defL = window.innerWidth - sz - 20;
      var defT = window.innerHeight - sz - 86;
      var defClamped = clampCoords(defL, defT);
      state.left = defClamped.left;
      state.top = defClamped.top;
    }
    if (orbEl) {
      orbEl.style.left = state.left + 'px';
      orbEl.style.top = state.top + 'px';
      orbEl.classList.toggle('mg-orb-left', (state.left || 0) < window.innerWidth / 2);
      orbEl.classList.toggle('mg-edge-tuck-left', !state.open && state.edgeTucked === 'left');
      orbEl.classList.toggle('mg-edge-tuck-right', !state.open && state.edgeTucked === 'right');
      updateOrbStarTier();
    }
    if (dragHintEl) {
      dragHintEl.style.display = (state.hasDraggedOnce || state.edgeTucked) ? 'none' : '';
    }
    syncTimerVisualsOnly();
    positionCardNearOrb();
  }

  function positionCardNearOrb() {
    if (!cardEl || !state.open) return;
    var sz = getOrbSize();
    var vw = window.innerWidth;
    var vh = window.innerHeight;
    var padX = 12;
    var padY = 14;
    var maxTargetW = (state.activeTab !== 'guide' || state.detailed) ? 388 : 344;
    var cardW = Math.min(maxTargetW, vw - padX * 2);
    cardEl.style.width = cardW + 'px';

    // Measure natural height after applying width
    var cardH = Math.min(cardEl.offsetHeight || 240, vh - padY * 2);
    var gap = 12;
    var orbLeft = state.left || 0;
    var orbTop = state.top || 0;
    var orbCx = orbLeft + sz / 2;
    var orbCy = orbTop + sz / 2;

    var prefLeft = (orbCx > vw / 2) ? (orbLeft + sz - cardW) : orbLeft;
    var cardLeft = Math.max(padX, Math.min(vw - cardW - padX, prefLeft));

    var roomAbove = orbTop - gap - padY;
    var roomBelow = vh - (orbTop + sz + gap) - padY;
    var cardTop;

    if (roomAbove >= cardH && (orbCy >= vh * 0.45 || roomBelow < cardH)) {
      cardTop = orbTop - gap - cardH;
    } else if (roomBelow >= cardH) {
      cardTop = orbTop + sz + gap;
    } else if (roomAbove >= roomBelow) {
      cardTop = padY;
    } else {
      cardTop = Math.max(padY, vh - cardH - padY);
    }

    // Avoid obscuring the orb on narrow viewports if horizontal room permits
    var overlapsH = !(cardLeft + cardW <= orbLeft - 6 || cardLeft >= orbLeft + sz + 6);
    var overlapsV = !(cardTop + cardH <= orbTop - 6 || cardTop >= orbTop + sz + 6);
    if (overlapsH && overlapsV) {
      if (orbLeft >= cardW + padX + 8) {
        cardLeft = orbLeft - cardW - gap;
      } else if (vw - (orbLeft + sz) >= cardW + padX + 8) {
        cardLeft = orbLeft + sz + gap;
      }
    }

    cardEl.style.left = Math.round(Math.max(padX, Math.min(vw - cardW - padX, cardLeft))) + 'px';
    cardEl.style.top = Math.round(Math.max(padY, Math.min(vh - cardH - padY, cardTop))) + 'px';
    positionToastNearOrb();
  }

  function positionToastNearOrb() {
    if (!toastPillEl || toastPillEl.style.display === 'none') return;
    var sz = getOrbSize();
    var vw = window.innerWidth;
    var vh = window.innerHeight;
    var tw = toastPillEl.offsetWidth || 210;
    var left = (state.left + sz / 2 > vw / 2) ? (state.left + sz - tw) : state.left;
    left = Math.max(12, Math.min(vw - tw - 12, left));
    var top = state.top > 64 ? state.top - 36 : state.top + sz + 10;
    top = Math.max(12, Math.min(vh - 38, top));
    toastPillEl.style.left = Math.round(left) + 'px';
    toastPillEl.style.top = Math.round(top) + 'px';
  }

  function showMiniToast(text) {
    if (!toastPillEl) return;
    if (toastTimer) {
      clearTimeout(toastTimer);
      toastTimer = null;
    }
    toastPillEl.textContent = text;
    toastPillEl.style.display = 'block';
    positionToastNearOrb();
    toastTimer = setTimeout(function () {
      toastTimer = null;
      if (toastPillEl) toastPillEl.style.display = 'none';
    }, 2400);
  }

  function injectStyles() {
    if (document.getElementById('mathedu-guide-styles')) return;
    var style = document.createElement('style');
    style.id = 'mathedu-guide-styles';
    style.textContent = [
      '#matheduGuideRoot { position: fixed; inset: 0; pointer-events: none; z-index: 999990; font-family: "Pretendard Variable", Pretendard, "Plus Jakarta Sans", -apple-system, sans-serif; }',
      '#matheduGuideOrb {',
      '  position: fixed; width: 52px; height: 52px; border-radius: 9999px; pointer-events: auto;',
      '  display: flex; align-items: center; justify-content: center; padding: 0;',
      '  background: rgba(255, 255, 255, 0.94); color: #006398;',
      '  border: 1.5px solid rgba(0, 99, 152, 0.28);',
      '  box-shadow: 0 10px 28px rgba(0, 99, 152, 0.18), 0 2px 8px rgba(15, 23, 42, 0.10);',
      '  backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px);',
      '  cursor: grab; touch-action: none; user-select: none; -webkit-user-select: none;',
      '  animation: mgOrbAura 3.4s ease-in-out infinite;',
      '  transition: transform 0.22s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.22s ease, border-color 0.22s ease;',
      '}',
      '#matheduGuideOrb:hover { transform: scale(1.06); animation-play-state: paused; border-color: #0284c7; box-shadow: 0 12px 32px rgba(2, 132, 199, 0.28); }',
      '#matheduGuideOrb[data-star-tier="2"] { color: #0d9488; border-color: rgba(13, 148, 136, 0.36); }',
      '#matheduGuideOrb[data-star-tier="3"] { color: #4f46e5; border-color: rgba(79, 70, 229, 0.38); }',
      '#matheduGuideOrb[data-star-tier="4"] { color: #7c3aed; border-color: rgba(124, 58, 237, 0.42); }',
      '#matheduGuideOrb[data-star-tier="5"] { color: #d97706; border-color: rgba(217, 119, 6, 0.50); box-shadow: 0 10px 28px rgba(217, 119, 6, 0.22); }',
      '#matheduGuideOrb.mg-edge-tuck-left { transform: translateX(-52%); opacity: 0.88; }',
      '#matheduGuideOrb.mg-edge-tuck-right { transform: translateX(52%); opacity: 0.88; }',
      '#matheduGuideOrb.mg-edge-tuck-left:hover, #matheduGuideOrb.mg-edge-tuck-right:hover { transform: translateX(0) scale(1.06); opacity: 1; }',
      '#matheduGuideOrb.mg-dragging { cursor: grabbing !important; transform: scale(1.08) !important; animation: none !important; transition: none !important; box-shadow: 0 18px 40px rgba(2, 132, 199, 0.36) !important; }',
      '#matheduGuideOrb.mg-pulse { border-color: #10B981 !important; box-shadow: 0 0 0 5px rgba(16, 185, 129, 0.22), 0 12px 28px rgba(16, 185, 129, 0.32) !important; }',
      '#mgOrbTimerBadge { position: absolute; top: -8px; right: -6px; display: none; padding: 1px 6px; border-radius: 999px; font-size: 9.5px; font-weight: 800; background: #0f172a; color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.55); box-shadow: 0 3px 8px rgba(0,0,0,0.28); pointer-events: none; font-variant-numeric: tabular-nums; }',
      '.mg-orb-icon { display: inline-flex; align-items: center; justify-content: center; animation: mgIconFloat 3.4s ease-in-out infinite; pointer-events: none; }',
      '#matheduGuideOrb.mg-dragging .mg-orb-icon { animation: none !important; }',
      '@keyframes mgOrbAura {',
      '  0%, 100% { box-shadow: 0 10px 26px rgba(0, 99, 152, 0.18), 0 2px 8px rgba(15, 23, 42, 0.10); }',
      '  50% { box-shadow: 0 14px 32px rgba(2, 132, 199, 0.28), 0 0 0 4px rgba(56, 189, 248, 0.12); }',
      '}',
      '@keyframes mgIconFloat { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-2.5px); } }',
      '.mg-orb-ring { position: absolute; inset: -4px; width: calc(100% + 8px); height: calc(100% + 8px); pointer-events: none; transform: rotate(-90deg); }',
      '.mg-orb-grip { position: absolute; top: 4px; left: 50%; transform: translateX(-50%); display: grid; grid-template-columns: repeat(3, 2.5px); gap: 2px; opacity: 0.45; pointer-events: none; }',
      '.mg-orb-grip span { width: 2.5px; height: 2.5px; border-radius: 99px; background: currentColor; }',
      '.mg-drag-pill { position: absolute; right: calc(100% + 8px); top: 50%; transform: translateY(-50%); white-space: nowrap; font-size: 10px; font-weight: 800; padding: 3px 8px; border-radius: 999px; background: rgba(15, 23, 42, 0.88); color: #f8fafc; pointer-events: none; opacity: 0.92; box-shadow: 0 4px 10px rgba(0,0,0,0.18); transition: opacity 0.18s ease; }',
      '#matheduGuideOrb.mg-orb-left .mg-drag-pill { right: auto; left: calc(100% + 8px); }',
      '#mgOrbToast { position: fixed; display: none; pointer-events: none; white-space: nowrap; font-size: 11px; font-weight: 800; padding: 5px 10px; border-radius: 999px; background: rgba(15, 23, 42, 0.92); color: #6ee7b7; border: 1px solid rgba(16, 185, 129, 0.45); box-shadow: 0 8px 22px rgba(15, 23, 42, 0.28); z-index: 999992; }',
      '#matheduGuideCard {',
      '  position: fixed; pointer-events: auto; border-radius: 18px; padding: 12px 14px;',
      '  max-height: calc(100vh - 28px); overflow-y: auto; box-sizing: border-box;',
      '  background: rgba(255, 255, 255, 0.96); color: #0f172a;',
      '  border: 1px solid rgba(203, 213, 225, 0.85);',
      '  box-shadow: 0 20px 48px rgba(15, 23, 42, 0.18), 0 0 0 1px rgba(0, 99, 152, 0.08);',
      '  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);',
      '  animation: mgCardPop 0.2s cubic-bezier(0.22, 1, 0.36, 1);',
      '  transition: border-color 0.2s ease;',
      '}',
      '#matheduGuideCard.mg-card-detailed { padding: 13px 15px; }',
      '#matheduGuideRoot.mg-dragging-root #matheduGuideCard { transition: none !important; }',
      '@keyframes mgCardPop { from { opacity: 0; transform: scale(0.94) translateY(4px); } to { opacity: 1; transform: scale(1) translateY(0); } }',
      '.mg-card-head { display: flex; align-items: center; justify-content: space-between; gap: 4px; margin-bottom: 8px; flex-wrap: nowrap; }',
      '.mg-drag-handle { display: inline-flex; align-items: center; gap: 4px; cursor: grab; touch-action: none; user-select: none; min-width: 0; }',
      '.mg-drag-handle:active { cursor: grabbing; }',
      '.mg-badge { display: inline-flex; align-items: center; gap: 4px; padding: 2px 7px; border-radius: 999px; font-size: 10.5px; font-weight: 800; background: rgba(0, 99, 152, 0.11); color: #006398; white-space: nowrap; }',
      '.mg-tier-pill { font-size: 10px; font-weight: 800; padding: 2px 6px; border-radius: 999px; background: rgba(245, 158, 11, 0.14); color: #b45309; white-space: nowrap; }',
      '.mg-head-btns { display: inline-flex; align-items: center; gap: 2px; shrink: 0; }',
      '.mg-icon-btn { border: 0; background: transparent; color: #64748b; cursor: pointer; font-size: 11.5px; font-weight: 800; padding: 3px 5px; border-radius: 7px; line-height: 1.2; white-space: nowrap; }',
      '.mg-icon-btn:hover { background: rgba(148, 163, 184, 0.18); color: #0f172a; }',
      '.mg-tab-bar { display: grid; grid-template-columns: repeat(4, 1fr); gap: 4px; padding: 3px; border-radius: 12px; background: rgba(241, 245, 249, 0.9); border: 1px solid rgba(203, 213, 225, 0.7); margin-bottom: 10px; }',
      '.mg-tab-btn { border: 0; border-radius: 9px; padding: 5px 4px; font-size: 11px; font-weight: 800; cursor: pointer; background: transparent; color: #475569; transition: all 0.15s ease; white-space: nowrap; text-align: center; }',
      '.mg-tab-btn:hover { color: #006398; background: rgba(255, 255, 255, 0.6); }',
      '.mg-tab-btn.active { background: #ffffff; color: #006398; box-shadow: 0 2px 6px rgba(15, 23, 42, 0.08); }',
      '.mg-title { font-size: 14.5px; font-weight: 800; line-height: 1.35; margin: 0 0 5px 0; color: inherit; }',
      '.mg-body { font-size: 12.2px; line-height: 1.52; margin: 0 0 8px 0; color: #475569; }',
      '.mg-tip { display: flex; align-items: flex-start; gap: 6px; font-size: 11.5px; font-weight: 700; line-height: 1.45; padding: 7px 10px; border-radius: 10px; margin-bottom: 9px; background: rgba(2, 132, 199, 0.08); color: #0369a1; border: 1px dashed rgba(2, 132, 199, 0.34); }',
      '.mg-details-box { padding: 9px 11px; border-radius: 12px; margin-bottom: 9px; background: rgba(248, 250, 252, 0.92); border: 1px solid rgba(203, 213, 225, 0.85); }',
      '.mg-details-title { font-size: 11.5px; font-weight: 800; color: #006398; margin-bottom: 7px; display: flex; align-items: center; gap: 5px; }',
      '.mg-details-list { display: flex; flex-direction: column; gap: 6px; }',
      '.mg-step-row { display: flex; align-items: flex-start; gap: 7px; font-size: 11.8px; line-height: 1.48; color: #334155; }',
      '.mg-step-num { flex: 0 0 auto; width: 17px; height: 17px; border-radius: 999px; display: inline-flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 800; background: #006398; color: #ffffff; margin-top: 2px; }',
      '.mg-step-label { font-weight: 800; color: #0f172a; }',
      '.mg-sub-label { font-size: 10.5px; font-weight: 800; color: #64748b; margin-bottom: 5px; }',
      '.mg-chips { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 9px; }',
      '.mg-chip { border: 1px solid rgba(148, 163, 184, 0.38); border-radius: 999px; padding: 4px 9px; font-size: 11px; font-weight: 700; cursor: pointer; background: rgba(241, 245, 249, 0.85); color: #1e293b; transition: all 0.15s ease; }',
      '.mg-chip:hover { border-color: #0284c7; color: #0284c7; background: rgba(224, 242, 254, 0.7); }',
      '.mg-chip.active { background: linear-gradient(135deg, #006398, #4f46e5); color: #ffffff; border-color: transparent; }',
      '.mg-chip.seen { border-color: rgba(16, 185, 129, 0.45); }',
      '.mg-daily-card { padding: 10px 11px; border-radius: 12px; background: linear-gradient(135deg, rgba(224,242,254,0.65), rgba(238,242,255,0.65)); border: 1px solid rgba(2, 132, 199, 0.25); margin-bottom: 9px; }',
      '.mg-tool-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin-bottom: 6px; }',
      '.mg-tool-btn { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 3px; padding: 8px 4px; border-radius: 11px; border: 1px solid rgba(148, 163, 184, 0.32); background: rgba(248, 250, 252, 0.9); color: #0f172a; font-size: 10.5px; font-weight: 800; cursor: pointer; text-align: center; transition: all 0.15s ease; }',
      '.mg-tool-btn:hover { border-color: #0284c7; color: #0284c7; transform: translateY(-1px); }',
      '.mg-kpi-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; margin-bottom: 8px; }',
      '.mg-kpi-btn { display: flex; align-items: center; justify-content: space-between; padding: 8px 10px; border-radius: 11px; border: 1px solid rgba(148, 163, 184, 0.3); background: rgba(248, 250, 252, 0.9); color: #0f172a; cursor: pointer; font-size: 11px; font-weight: 700; }',
      '.mg-kpi-btn:hover { border-color: #0284c7; }',
      '.mg-kpi-val { font-size: 14px; font-weight: 900; color: #006398; }',
      '.mg-timer-box { padding: 9px 11px; border-radius: 12px; background: rgba(248, 250, 252, 0.92); border: 1px solid rgba(203, 213, 225, 0.85); margin-top: 8px; }',
      '.mg-timer-row { display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-bottom: 6px; }',
      '.mg-timer-clock { font-size: 20px; font-weight: 900; font-variant-numeric: tabular-nums; color: #006398; letter-spacing: 0.5px; }',
      '.mg-pad-canvas { width: 100%; height: 184px; display: block; border-radius: 12px; border: 1.5px solid rgba(148, 163, 184, 0.45); background-color: #ffffff; background-image: radial-gradient(rgba(100, 116, 139, 0.25) 1px, transparent 1px); background-size: 14px 14px; cursor: crosshair; touch-action: none; }',
      '.mg-pad-toolbar { display: flex; align-items: center; justify-content: space-between; gap: 6px; margin-top: 8px; flex-wrap: wrap; }',
      '.mg-color-dot { width: 18px; height: 18px; border-radius: 999px; border: 2px solid rgba(255,255,255,0.9); box-shadow: 0 0 0 1px rgba(15,23,42,0.2); cursor: pointer; padding: 0; }',
      '.mg-color-dot.active { transform: scale(1.18); box-shadow: 0 0 0 2px #0f172a; }',
      '.mg-actions { display: flex; align-items: center; justify-content: space-between; gap: 6px; flex-wrap: wrap; padding-top: 8px; border-top: 1px solid rgba(148, 163, 184, 0.22); }',
      '.mg-btn-primary { border: 0; border-radius: 9px; padding: 5px 10px; font-size: 11px; font-weight: 800; cursor: pointer; background: linear-gradient(135deg, #006398, #4f46e5); color: #ffffff; box-shadow: 0 3px 10px rgba(0, 99, 152, 0.22); }',
      '.mg-btn-primary:hover { opacity: 0.94; }',
      '.mg-btn-ghost { border: 1px solid rgba(148, 163, 184, 0.38); border-radius: 9px; padding: 5px 9px; font-size: 11px; font-weight: 700; cursor: pointer; background: transparent; color: #475569; }',
      '.mg-btn-ghost:hover { background: rgba(148, 163, 184, 0.12); color: #0f172a; }',
      '.mg-btn-ghost.muted { opacity: 0.75; }',
      '.mg-btn-ghost.active-detail { background: rgba(0, 99, 152, 0.10); color: #006398; border-color: rgba(0, 99, 152, 0.36); }',
      '.mg-spotlight { outline: 2.5px solid #0284c7 !important; outline-offset: 4px !important; box-shadow: 0 0 0 6px rgba(2, 132, 199, 0.20) !important; border-radius: 12px; transition: box-shadow 0.25s ease !important; }',
      '#matheduGuideRoot.mg-dark #matheduGuideOrb { background: rgba(15, 23, 42, 0.94); color: #38bdf8; border-color: rgba(56, 189, 248, 0.38); box-shadow: 0 10px 30px rgba(0,0,0,0.48), 0 0 18px rgba(56,189,248,0.22); }',
      '#matheduGuideRoot.mg-dark #matheduGuideOrb[data-star-tier="2"] { color: #2dd4bf; border-color: rgba(45, 212, 191, 0.45); }',
      '#matheduGuideRoot.mg-dark #matheduGuideOrb[data-star-tier="3"] { color: #818cf8; border-color: rgba(129, 140, 248, 0.48); }',
      '#matheduGuideRoot.mg-dark #matheduGuideOrb[data-star-tier="4"] { color: #c084fc; border-color: rgba(192, 132, 252, 0.50); }',
      '#matheduGuideRoot.mg-dark #matheduGuideOrb[data-star-tier="5"] { color: #fbbf24; border-color: rgba(251, 191, 36, 0.62); }',
      '#matheduGuideRoot.mg-dark #matheduGuideCard { background: rgba(15, 23, 42, 0.95); color: #f8fafc; border-color: rgba(56, 189, 248, 0.30); box-shadow: 0 22px 52px rgba(0,0,0,0.62); }',
      '#matheduGuideRoot.mg-dark .mg-body { color: #cbd5e1; }',
      '#matheduGuideRoot.mg-dark .mg-badge { background: rgba(56, 189, 248, 0.16); color: #7dd3fc; }',
      '#matheduGuideRoot.mg-dark .mg-tier-pill { background: rgba(251, 191, 36, 0.16); color: #fde68a; }',
      '#matheduGuideRoot.mg-dark .mg-sub-label { color: #94a3b8; }',
      '#matheduGuideRoot.mg-dark .mg-tab-bar { background: rgba(30, 41, 59, 0.85); border-color: rgba(56, 189, 248, 0.22); }',
      '#matheduGuideRoot.mg-dark .mg-tab-btn { color: #94a3b8; }',
      '#matheduGuideRoot.mg-dark .mg-tab-btn:hover { color: #e2e8f0; background: rgba(51, 65, 85, 0.55); }',
      '#matheduGuideRoot.mg-dark .mg-tab-btn.active { background: #0f172a; color: #38bdf8; }',
      '#matheduGuideRoot.mg-dark .mg-icon-btn { color: #94a3b8; }',
      '#matheduGuideRoot.mg-dark .mg-icon-btn:hover { background: rgba(148, 163, 184, 0.16); color: #f8fafc; }',
      '#matheduGuideRoot.mg-dark .mg-tip { background: rgba(56, 189, 248, 0.12); color: #7dd3fc; border-color: rgba(56, 189, 248, 0.35); }',
      '#matheduGuideRoot.mg-dark .mg-details-box, #matheduGuideRoot.mg-dark .mg-timer-box { background: rgba(30, 41, 59, 0.72); border-color: rgba(56, 189, 248, 0.24); }',
      '#matheduGuideRoot.mg-dark .mg-daily-card { background: rgba(30, 41, 59, 0.82); border-color: rgba(56, 189, 248, 0.32); }',
      '#matheduGuideRoot.mg-dark .mg-tool-btn, #matheduGuideRoot.mg-dark .mg-kpi-btn { background: rgba(30, 41, 59, 0.85); color: #e2e8f0; border-color: rgba(56, 189, 248, 0.24); }',
      '#matheduGuideRoot.mg-dark .mg-kpi-val, #matheduGuideRoot.mg-dark .mg-timer-clock { color: #38bdf8; }',
      '#matheduGuideRoot.mg-dark .mg-details-title { color: #38bdf8; }',
      '#matheduGuideRoot.mg-dark .mg-step-row { color: #cbd5e1; }',
      '#matheduGuideRoot.mg-dark .mg-step-label { color: #f8fafc; }',
      '#matheduGuideRoot.mg-dark .mg-step-num { background: #0284c7; color: #ffffff; }',
      '#matheduGuideRoot.mg-dark .mg-chip { background: rgba(30, 41, 59, 0.88); color: #e2e8f0; border-color: rgba(148, 163, 184, 0.28); }',
      '#matheduGuideRoot.mg-dark .mg-chip:hover { border-color: #38bdf8; color: #38bdf8; }',
      '#matheduGuideRoot.mg-dark .mg-chip.active { background: linear-gradient(135deg, #0284c7, #6366f1); color: #ffffff; border-color: transparent; }',
      '#matheduGuideRoot.mg-dark .mg-pad-canvas { background-color: #090d16; background-image: radial-gradient(rgba(148, 163, 184, 0.25) 1px, transparent 1px); border-color: rgba(56, 189, 248, 0.35); }',
      '#matheduGuideRoot.mg-dark .mg-color-dot.active { box-shadow: 0 0 0 2px #38bdf8; }',
      '#matheduGuideRoot.mg-dark .mg-btn-ghost { color: #cbd5e1; border-color: rgba(148, 163, 184, 0.35); }',
      '#matheduGuideRoot.mg-dark .mg-btn-ghost:hover { background: rgba(148, 163, 184, 0.14); color: #ffffff; }',
      '#matheduGuideRoot.mg-dark .mg-btn-ghost.active-detail { background: rgba(56, 189, 248, 0.16); color: #7dd3fc; border-color: rgba(56, 189, 248, 0.42); }',
      '@media (max-width: 639px) { #matheduGuideOrb { width: 46px; height: 46px; } }'
    ].join('\n');
    document.head.appendChild(style);
  }

  function clearSpotlight() {
    if (spotlightTimer) {
      clearTimeout(spotlightTimer);
      spotlightTimer = null;
    }
    for (var i = 0; i < activeSpotlightEls.length; i++) {
      try { activeSpotlightEls[i].classList.remove('mg-spotlight'); } catch (e) {}
    }
    activeSpotlightEls = [];
  }

  function isElementVisible(el) {
    if (!el || !el.getBoundingClientRect) return false;
    var cs = window.getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || cs.opacity === '0') return false;
    var r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  }

  function isFixedPositionElement(el) {
    for (var p = el; p && p !== document.body; p = p.parentElement) {
      if (window.getComputedStyle(p).position === 'fixed') return true;
    }
    return false;
  }

  function spotlightTopic(topic, doScroll) {
    clearSpotlight();
    if (!topic || !topic.selectors) return;
    if (typeof topic.prepareAction === 'function') {
      try { topic.prepareAction(); } catch (e) {}
    }

    var firstVisible = null;
    for (var i = 0; i < topic.selectors.length; i++) {
      var list = document.querySelectorAll(topic.selectors[i]);
      for (var k = 0; k < list.length; k++) {
        var el = list[k];
        if (el === orbEl || (rootEl && rootEl.contains(el))) continue;
        if (!isElementVisible(el)) continue;
        if (!firstVisible) firstVisible = el;
        el.classList.add('mg-spotlight');
        activeSpotlightEls.push(el);
      }
    }

    if (doScroll && firstVisible && !isFixedPositionElement(firstVisible)) {
      var r = firstVisible.getBoundingClientRect();
      if (r.top < 88 || r.bottom > window.innerHeight - 84) {
        try { firstVisible.scrollIntoView({ behavior: 'smooth', block: 'center' }); } catch (e) {}
      }
    }

    if (activeSpotlightEls.length) {
      spotlightTimer = setTimeout(clearSpotlight, SPOTLIGHT_DURATION_MS);
    }
  }

  function updateOrbProgressRing() {
    if (!progressCircleEl) return;
    var seen = countSeenTopics();
    var ratio = seen / TOPICS.length;
    var circ = 2 * Math.PI * 26;
    progressCircleEl.setAttribute('stroke-dasharray', circ.toFixed(1));
    progressCircleEl.setAttribute('stroke-dashoffset', (circ * (1 - ratio)).toFixed(1));
  }

  function pulseOrbBriefly() {
    if (!orbEl) return;
    orbEl.classList.add('mg-pulse');
    setTimeout(function () {
      if (orbEl) orbEl.classList.remove('mg-pulse');
    }, 850);
  }

  function pickContextualTopicForScroll() {
    var deep = document.getElementById('deepMathLabsHub');
    if (deep) {
      var dr = deep.getBoundingClientRect();
      if (dr.top < window.innerHeight * 0.72 && dr.bottom > 100) return 'deep_labs';
    }
    var qSec = document.getElementById('quizExplorerSection');
    if (qSec) {
      var qr = qSec.getBoundingClientRect();
      if (qr.top < window.innerHeight * 0.65 && qr.bottom > 120) return 'filters';
    }
    return state.activeTopicId || 'welcome';
  }

  function getSafeFeaturedProof() {
    var fallback = {
      title: {
        ko: '피타고라스 나무 (프랙탈 기하와 면적 보존의 기적)',
        en: 'Pythagoras Tree (Fractal Geometry & Area Invariance)'
      },
      desc: {
        ko: '직각삼각형의 세 변 위에 정사각형을 올려 각 단계별 넓이 합 보존 원리를 관찰해 보세요.',
        en: 'Attach squares onto a right triangle to see why area invariance holds at every fractal stage.'
      },
      pdf: 'https://min7014.github.io/2025/2025013001.pdf#toolbar=0&view=Fit&scrollbar=0',
      yt: 'https://youtu.be/DSgUHigl82o'
    };
    try {
      if (typeof window.getTodayFeaturedProof === 'function') {
        var p = window.getTodayFeaturedProof();
        if (p && p.title) return p;
      }
    } catch (e) {}
    return fallback;
  }

  function stripLatexInline(str) {
    return String(str || '').replace(/\$([^$]+)\$/g, function (_, inner) {
      return inner
        .replace(/\\?overline\s*\{([^}]*)\}/g, '$1')
        .replace(/\\?frac\s*\{([^}]*)\}\s*\{([^}]*)\}/g, '$1/$2')
        .replace(/\\?sqrt\s*\{([^}]*)\}/g, '√$1')
        .replace(/\\?cdot/g, '·')
        .replace(/\\?times/g, '×')
        .replace(/\^2\b/g, '²')
        .replace(/\^3\b/g, '³')
        .replace(/\\[a-zA-Z]+/g, '')
        .replace(/[\t\f\r\n]+/g, ' ')
        .replace(/[{}]/g, '')
        .replace(/\s*([=+])\s*/g, ' $1 ')
        .trim();
    }).replace(/\(\s*\)/g, '').replace(/\s{2,}/g, ' ').trim();
  }

  function speakTextClean(text, title, lang) {
    try {
      if (window.speechSynthesis && window.speechSynthesis.speaking) {
        window.speechSynthesis.cancel();
        return;
      }
    } catch (e) {}
    if (lang === 'ko' && window.MatheduVoiceTeacher && typeof window.MatheduVoiceTeacher.speakRaw === 'function') {
      try {
        window.MatheduVoiceTeacher.speakRaw(text, title);
        return;
      } catch (e) {}
    }
    try {
      if (window.speechSynthesis && typeof window.SpeechSynthesisUtterance !== 'undefined') {
        var u = new window.SpeechSynthesisUtterance(text);
        u.lang = lang === 'en' ? 'en-US' : 'ko-KR';
        window.speechSynthesis.speak(u);
      }
    } catch (e) {}
  }

  function renderGuideTabBody(topic, lang, c) {
    var chipIds = (topic.id === 'welcome') ? INTENT_PICK_IDS : (topic.relatedIds || QUICK_PICK_IDS);
    var chipLabelText = (topic.id === 'welcome') ? c.quickLabel : c.relatedLabel;

    var chipsHtml = '';
    for (var i = 0; i < chipIds.length; i++) {
      var rt = TOPIC_MAP[chipIds[i]];
      if (!rt) continue;
      chipsHtml += '<button type="button" class="mg-chip' + (rt.id === topic.id ? ' active' : '') + '" data-mg-topic="' + rt.id + '">' + rt.chipLabel[lang] + '</button>';
    }

    var detailItems = (topic.details && topic.details[lang]) || [];
    var detailsHtml = '';
    if (state.detailed && detailItems.length) {
      var rowsHtml = '';
      for (var dIdx = 0; dIdx < detailItems.length; dIdx++) {
        var pair = detailItems[dIdx];
        rowsHtml += '<div class="mg-step-row"><span class="mg-step-num">' + (dIdx + 1) + '</span><div><span class="mg-step-label">' + pair[0] + '</span> · ' + pair[1] + '</div></div>';
      }
      detailsHtml = '<div class="mg-details-box" id="mgDetailsBox"><div class="mg-details-title">' + c.detailHeading + '</div><div class="mg-details-list">' + rowsHtml + '</div></div>';
    }

    var seenCnt = countSeenTopics();
    var allListHtml = '';
    if (state.showAllTopics) {
      allListHtml += '<div class="mg-sub-label" style="margin-top:2px;">' + c.quickLabel + ' (' + seenCnt + '/' + TOPICS.length + ' ' + c.seenCountUnit + ')</div>';
      allListHtml += '<div class="mg-chips">';
      for (var j = 0; j < TOPICS.length; j++) {
        var tp = TOPICS[j];
        var cls = 'mg-chip' + (tp.id === topic.id ? ' active' : (state.seenTopics[tp.id] ? ' seen' : ''));
        allListHtml += '<button type="button" class="' + cls + '" data-mg-topic="' + tp.id + '">' + tp.chipLabel[lang] + '</button>';
      }
      allListHtml += '</div>';
    }

    var locateHtml = (topic.id !== 'welcome')
      ? '<button type="button" class="mg-btn-primary" data-mg-act="locate">' + c.locateBtn + '</button>'
      : '';

    var detailBtnCls = 'mg-btn-ghost' + (state.detailed ? ' active-detail' : '');
    var detailBtnLabel = state.detailed ? c.detailCloseBtn : c.detailOpenBtn;
    var autoBtnCls = state.autoTips ? 'mg-btn-ghost' : 'mg-btn-ghost muted';
    var autoLabel = state.autoTips ? c.autoOnLabel : c.autoOffLabel;
    var autoTitle = state.autoTips ? c.autoOnTitle : c.autoOffTitle;
    var allLabel = state.showAllTopics ? c.allToggleOpen : c.allToggleClosed;

    return [
      '<h3 class="mg-title">' + topic.title[lang] + '</h3>',
      '<p class="mg-body">' + topic.body[lang] + '</p>',
      '<div class="mg-tip"><span>💡</span><span>' + topic.tipLine[lang] + '</span></div>',
      detailsHtml,
      '<div class="mg-sub-label">' + chipLabelText + '</div>',
      '<div class="mg-chips">' + chipsHtml + '</div>',
      allListHtml,
      '<div class="mg-actions">',
      '  <div style="display:flex;align-items:center;gap:5px;flex-wrap:wrap;">',
      '    <button type="button" class="' + detailBtnCls + '" data-mg-act="toggle-detail">' + detailBtnLabel + '</button>',
      '    <button type="button" class="mg-btn-ghost" data-mg-act="toggle-all">' + allLabel + '</button>',
      '    <button type="button" class="' + autoBtnCls + '" data-mg-act="toggle-auto" title="' + autoTitle + '">' + autoLabel + '</button>',
      '  </div>',
      '  ' + locateHtml,
      '</div>'
    ].join('');
  }

  function renderToolsTabBody(lang, c) {
    var p = getSafeFeaturedProof();
    var pTitle = (p.title && (p.title[lang] || p.title.ko)) || '';
    var pDesc = stripLatexInline((p.desc && (p.desc[lang] || p.desc.ko)) || '');

    var gridHtml = '';
    for (var i = 0; i < c.toolsGrid.length; i++) {
      var t = c.toolsGrid[i];
      gridHtml += '<button type="button" class="mg-tool-btn" data-mg-tool="' + t.act + '"><span style="font-size:15px;">' + t.icon + '</span><span>' + t.label + '</span></button>';
    }

    return [
      '<div class="mg-daily-card" id="mgDailyEurekaCard">',
      '  <div class="mg-sub-label" style="color:#0284c7;margin-bottom:3px;">' + c.dailyBadge + '</div>',
      '  <div class="mg-title" style="font-size:13.5px;margin-bottom:4px;">' + pTitle + '</div>',
      '  <p class="mg-body" style="font-size:11.5px;margin-bottom:8px;">' + pDesc + '</p>',
      '  <div style="display:flex;gap:5px;flex-wrap:wrap;">',
      '    <button type="button" class="mg-btn-ghost" data-mg-tool="daily-pdf">' + c.dailyPdfBtn + '</button>',
      '    <button type="button" class="mg-btn-ghost" data-mg-tool="daily-yt">' + c.dailyYtBtn + '</button>',
      '    <button type="button" class="mg-btn-primary" data-mg-tool="daily-voice">' + c.dailyVoiceBtn + '</button>',
      '  </div>',
      '</div>',
      '<div class="mg-sub-label">' + c.launcherTitle + '</div>',
      '<div class="mg-tool-grid">' + gridHtml + '</div>'
    ].join('');
  }

  function renderStudyTabBody(lang, c) {
    var snap = getStudySnapshot();
    var pauseLabel = timerState.running ? c.timerPause : c.timerResume;

    return [
      '<div class="mg-kpi-grid">',
      '  <button type="button" class="mg-kpi-btn" data-mg-study="badges"><span>' + c.studyKpis.streak + '</span><span class="mg-kpi-val">' + snap.streak + '</span></button>',
      '  <button type="button" class="mg-kpi-btn" data-mg-study="history"><span>' + c.studyKpis.solved + '</span><span class="mg-kpi-val">' + snap.solved.length + '</span></button>',
      '  <button type="button" class="mg-kpi-btn" data-mg-study="revenge"><span>' + c.studyKpis.wrong + '</span><span class="mg-kpi-val">' + snap.wrongs.length + '</span></button>',
      '  <button type="button" class="mg-kpi-btn" data-mg-study="bookmarks"><span>' + c.studyKpis.saved + '</span><span class="mg-kpi-val">' + snap.bookmarks.length + '</span></button>',
      '</div>',
      '<div style="display:flex;gap:5px;flex-wrap:wrap;margin-bottom:4px;">',
      '  <button type="button" class="mg-btn-primary" data-mg-study="revenge">' + c.studyActions.revenge + '</button>',
      '  <button type="button" class="mg-btn-ghost" data-mg-study="clinic">' + c.studyActions.clinic + '</button>',
      '  <button type="button" class="mg-btn-ghost" data-mg-study="quest">' + c.studyActions.quest + '</button>',
      '</div>',
      '<div class="mg-timer-box" id="mgEurekaTimerBox">',
      '  <div class="mg-sub-label" style="margin-bottom:2px;">' + c.timerHeading + '</div>',
      '  <div style="font-size:11px;color:#64748b;margin-bottom:6px;">' + c.timerSub + '</div>',
      '  <div class="mg-timer-row">',
      '    <span class="mg-timer-clock" id="mgTimerClock">' + formatTimerMMSS(timerState.remainingSec) + '</span>',
      '    <div style="display:flex;gap:4px;flex-wrap:wrap;">',
      '      <button type="button" class="mg-btn-ghost" data-mg-timer="preset-15">' + c.timer15 + '</button>',
      '      <button type="button" class="mg-btn-ghost" data-mg-timer="preset-25">' + c.timer25 + '</button>',
      '    </div>',
      '  </div>',
      '  <div style="display:flex;gap:5px;">',
      '    <button type="button" class="mg-btn-primary" id="mgTimerPauseBtn" data-mg-timer="toggle-pause">' + pauseLabel + '</button>',
      '    <button type="button" class="mg-btn-ghost" data-mg-timer="reset">' + c.timerReset + '</button>',
      '  </div>',
      '</div>'
    ].join('');
  }

  function renderPadTabBody(lang, c) {
    var colors = ['#0284c7', '#ef4444', '#10b981', '#f59e0b'];
    var dotsHtml = '';
    for (var i = 0; i < colors.length; i++) {
      var col = colors[i];
      var actCls = (!padEraser && padColor === col) ? ' active' : '';
      dotsHtml += '<button type="button" class="mg-color-dot' + actCls + '" style="background:' + col + ';" data-mg-pad-color="' + col + '" aria-label="Ink ' + (i + 1) + '"></button>';
    }
    var eraserCls = 'mg-btn-ghost' + (padEraser ? ' active-detail' : '');

    return [
      '<div class="mg-sub-label" style="margin-bottom:2px;">' + c.padHeading + '</div>',
      '<div class="mg-body" style="font-size:11.5px;margin-bottom:7px;">' + c.padSub + '</div>',
      '<canvas id="mgScratchCanvas" class="mg-pad-canvas"></canvas>',
      '<div class="mg-pad-toolbar">',
      '  <div style="display:flex;align-items:center;gap:6px;">' + dotsHtml + '</div>',
      '  <div style="display:flex;align-items:center;gap:4px;flex-wrap:wrap;">',
      '    <button type="button" class="' + eraserCls + '" data-mg-pad="eraser">' + c.padEraser + '</button>',
      '    <button type="button" class="mg-btn-ghost" data-mg-pad="undo">' + c.padUndo + '</button>',
      '    <button type="button" class="mg-btn-ghost" data-mg-pad="clear">' + c.padClear + '</button>',
      '  </div>',
      '</div>',
      '<div class="mg-actions" style="margin-top:8px;">',
      '  <span></span>',
      '  <button type="button" class="mg-btn-primary" data-mg-tool="mathlab">' + c.padMathLab + '</button>',
      '</div>'
    ].join('');
  }

  function redrawPadCanvas() {
    var canvas = document.getElementById('mgScratchCanvas');
    if (!canvas || !canvas.getContext) return;
    var ctx = canvas.getContext('2d');
    var dpr = Math.max(1, window.devicePixelRatio || 1);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, canvas.width / dpr, canvas.height / dpr);

    for (var i = 0; i < padStrokes.length; i++) {
      var st = padStrokes[i];
      if (!st || !st.points || !st.points.length) continue;
      ctx.save();
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      ctx.lineWidth = st.width || 2.4;
      if (st.eraser) {
        ctx.globalCompositeOperation = 'destination-out';
        ctx.strokeStyle = 'rgba(0,0,0,1)';
      } else {
        ctx.globalCompositeOperation = 'source-over';
        ctx.strokeStyle = st.color || '#0284c7';
      }
      ctx.beginPath();
      ctx.moveTo(st.points[0][0], st.points[0][1]);
      for (var k = 1; k < st.points.length; k++) {
        ctx.lineTo(st.points[k][0], st.points[k][1]);
      }
      if (st.points.length === 1) {
        ctx.lineTo(st.points[0][0] + 0.1, st.points[0][1] + 0.1);
      }
      ctx.stroke();
      ctx.restore();
    }
  }

  function setupScratchCanvas() {
    var canvas = document.getElementById('mgScratchCanvas');
    if (!canvas) return;
    var rect = canvas.getBoundingClientRect();
    var cssW = Math.max(240, Math.round(rect.width || 352));
    var cssH = Math.max(140, Math.round(rect.height || 184));
    var dpr = Math.max(1, window.devicePixelRatio || 1);
    canvas.width = Math.round(cssW * dpr);
    canvas.height = Math.round(cssH * dpr);
    redrawPadCanvas();

    var curStroke = null;
    function ptFromEvent(ev) {
      var r = canvas.getBoundingClientRect();
      return [Math.round((ev.clientX - r.left) * 10) / 10, Math.round((ev.clientY - r.top) * 10) / 10];
    }

    canvas.addEventListener('pointerdown', function (ev) {
      ev.stopPropagation();
      if (ev.pointerType === 'mouse' && ev.button !== 0) return;
      isDrawingPad = true;
      curStroke = {
        color: padColor,
        width: padEraser ? 14 : 2.6,
        eraser: !!padEraser,
        points: [ptFromEvent(ev)]
      };
      padStrokes.push(curStroke);
      try { canvas.setPointerCapture(ev.pointerId); } catch (e) {}
      redrawPadCanvas();
    });

    canvas.addEventListener('pointermove', function (ev) {
      if (!isDrawingPad || !curStroke) return;
      ev.stopPropagation();
      curStroke.points.push(ptFromEvent(ev));
      redrawPadCanvas();
    });

    function endPadStroke(ev) {
      if (!isDrawingPad) return;
      isDrawingPad = false;
      curStroke = null;
      savePadStrokes();
      try { canvas.releasePointerCapture(ev.pointerId); } catch (e) {}
    }

    canvas.addEventListener('pointerup', endPadStroke);
    canvas.addEventListener('pointercancel', endPadStroke);
  }

  function renderCardContent(reposition) {
    if (!rootEl || !orbEl || !cardEl) return;
    var lang = getLang();
    var dark = isDark();
    var c = COPY[lang];

    lastRenderedLang = lang;
    lastRenderedDark = dark;

    rootEl.classList.toggle('mg-dark', dark);
    orbEl.classList.toggle('mg-orb-left', (state.left || 0) < window.innerWidth / 2);
    orbEl.classList.toggle('mg-edge-tuck-left', !state.open && state.edgeTucked === 'left');
    orbEl.classList.toggle('mg-edge-tuck-right', !state.open && state.edgeTucked === 'right');
    orbEl.setAttribute('aria-label', c.orbLabel);
    orbEl.title = c.orbLabel;
    updateOrbStarTier();
    if (dragHintEl) {
      dragHintEl.textContent = c.dragPill;
      dragHintEl.style.display = (state.hasDraggedOnce || state.edgeTucked) ? 'none' : '';
    }
    updateOrbProgressRing();
    syncTimerVisualsOnly();

    if (!state.open || isInspectorActive()) {
      cardEl.style.display = 'none';
      return;
    }

    var topic = TOPIC_MAP[state.activeTopicId] || TOPICS[0];
    var tierIdx = computeStarTier() - 1;
    var tierLabel = c.tierNames[tierIdx] || c.tierNames[0];
    cardEl.style.display = 'block';
    cardEl.classList.toggle('mg-card-detailed', !!(state.detailed || state.activeTab !== 'guide'));

    var resetBtn = state.customPos
      ? '<button type="button" class="mg-icon-btn" data-mg-act="reset-pos" title="' + c.resetPosTitle + '" aria-label="' + c.resetPosTitle + '">↺</button>'
      : '';
    var themeIcon = dark ? '☀️' : '🌙';

    var tabOrder = ['guide', 'tools', 'study', 'pad'];
    var tabsHtml = '';
    for (var ti = 0; ti < tabOrder.length; ti++) {
      var tk = tabOrder[ti];
      tabsHtml += '<button type="button" class="mg-tab-btn' + (state.activeTab === tk ? ' active' : '') + '" data-mg-tab="' + tk + '">' + c.tabs[tk] + '</button>';
    }

    var bodyHtml = '';
    if (state.activeTab === 'tools') {
      bodyHtml = renderToolsTabBody(lang, c);
    } else if (state.activeTab === 'study') {
      bodyHtml = renderStudyTabBody(lang, c);
    } else if (state.activeTab === 'pad') {
      bodyHtml = renderPadTabBody(lang, c);
    } else {
      bodyHtml = renderGuideTabBody(topic, lang, c);
    }

    cardEl.innerHTML = [
      '<div class="mg-card-head">',
      '  <span class="mg-drag-handle mg-badge" title="' + c.dragHandleTitle + '">⠿ ' + c.badgePrefix + '</span>',
      '  <span class="mg-tier-pill">' + tierLabel + '</span>',
      '  <div class="mg-head-btns">',
      '    <button type="button" class="mg-icon-btn" data-mg-act="quick-lang" title="' + c.quickLangTitle + '" aria-label="' + c.quickLangTitle + '">' + c.quickLangBtn + '</button>',
      '    <button type="button" class="mg-icon-btn" data-mg-act="quick-theme" title="' + c.quickThemeTitle + '" aria-label="' + c.quickThemeTitle + '">' + themeIcon + '</button>',
      '    <button type="button" class="mg-icon-btn" data-mg-act="quick-voice" title="' + c.quickVoiceTitle + '" aria-label="' + c.quickVoiceTitle + '">🔊</button>',
      '    <button type="button" class="mg-icon-btn" data-mg-act="edge-tuck" title="' + c.quickTuckTitle + '" aria-label="' + c.quickTuckTitle + '">⇥</button>',
      '    ' + resetBtn,
      '    <button type="button" class="mg-icon-btn" data-mg-act="close" title="' + c.closeTitle + '" aria-label="' + c.closeTitle + '">✕</button>',
      '  </div>',
      '</div>',
      '<div class="mg-tab-bar" id="mgTabBar">' + tabsHtml + '</div>',
      bodyHtml
    ].join('');

    if (reposition !== false) {
      positionCardNearOrb();
    }
    if (state.activeTab === 'pad') {
      setupScratchCanvas();
    }
  }

  function showTopic(topicId, opts) {
    if (!TOPIC_MAP[topicId]) return false;
    opts = opts || {};
    var source = opts.source || 'manual';

    if (isInspectorActive()) return false;

    if (source === 'auto') {
      if (!state.autoTips) return false;
      if (state.seenTopics[topicId]) return false;
      if (isDrawingPad || (state.open && state.activeTab === 'pad')) return false;
      var now = Date.now();
      if (now - lastAutoTriggerAt < 250) return false;
      lastAutoTriggerAt = now;
      state.activeTab = 'guide';
      if (typeof opts.detailed !== 'boolean') state.detailed = false;
      pulseOrbBriefly();
    } else if (opts.keepTab !== true) {
      state.activeTab = 'guide';
    }

    state.edgeTucked = null;
    state.seenTopics[topicId] = true;
    state.activeTopicId = topicId;
    state.open = true;
    if (typeof opts.detailed === 'boolean') {
      state.detailed = opts.detailed;
    }
    saveState();
    syncCoordsToViewport();
    renderCardContent(true);

    if (opts.spotlight) {
      spotlightTopic(TOPIC_MAP[topicId], !!opts.scroll);
    }
    return true;
  }

  function openCard(topicId, withDetails) {
    if (isInspectorActive()) return;
    state.edgeTucked = null;
    var targetId = (topicId && TOPIC_MAP[topicId]) ? topicId : pickContextualTopicForScroll();
    state.open = true;
    if (typeof withDetails === 'boolean') {
      state.detailed = withDetails;
    }
    state.activeTopicId = targetId;
    state.seenTopics[targetId] = true;
    saveState();
    syncCoordsToViewport();
    renderCardContent(true);
  }

  function closeCard() {
    clearSpotlight();
    state.open = false;
    state.showAllTopics = false;
    saveState();
    syncCoordsToViewport();
    renderCardContent(false);
  }

  function edgeTuckOrb() {
    clearSpotlight();
    var sz = getOrbSize();
    var vw = window.innerWidth;
    var bounds = clampCoords(state.left || 0, state.top || 0);
    var isLeft = ((state.left || 0) + sz / 2) < vw / 2;
    state.open = false;
    state.showAllTopics = false;
    state.edgeTucked = isLeft ? 'left' : 'right';
    state.customPos = {
      rx: isLeft ? 0 : 1,
      ry: Math.max(0, Math.min(1, (bounds.top - bounds.minY) / Math.max(1, bounds.maxY - bounds.minY)))
    };
    savePos();
    saveState();
    syncCoordsToViewport();
    showMiniToast(COPY[getLang()].tuckedToast);
  }

  function onOrbSelected() {
    if (state.edgeTucked || !state.open) {
      state.edgeTucked = null;
      openCard(null, state.activeTab === 'guide' ? true : state.detailed);
      var openTopic = TOPIC_MAP[state.activeTopicId];
      if (state.activeTab === 'guide' && openTopic && openTopic.id !== 'welcome') {
        spotlightTopic(openTopic, false);
      }
      return;
    }
    if (state.activeTab === 'guide' && !state.detailed) {
      state.detailed = true;
      saveState();
      renderCardContent(true);
      var curTopic = TOPIC_MAP[state.activeTopicId];
      if (curTopic && curTopic.id !== 'welcome') spotlightTopic(curTopic, false);
      return;
    }
    closeCard();
  }

  function toggleCard() {
    if (state.open) {
      closeCard();
    } else {
      openCard();
    }
  }

  function setTab(tabName) {
    if (['guide', 'tools', 'study', 'pad'].indexOf(tabName) === -1) return;
    if (tabName !== 'guide') clearSpotlight();
    state.edgeTucked = null;
    state.activeTab = tabName;
    state.open = true;
    saveState();
    syncCoordsToViewport();
    renderCardContent(true);
  }

  function setAutoTips(enabled) {
    state.autoTips = !!enabled;
    saveState();
    renderCardContent(false);
  }

  function resetPosition() {
    state.customPos = null;
    state.edgeTucked = null;
    savePos();
    saveState();
    syncCoordsToViewport();
    renderCardContent(false);
  }

  function resetSeen() {
    state.seenTopics = {};
    state.activeTopicId = 'welcome';
    saveState();
    renderCardContent(true);
  }

  function matchRule(target, rules) {
    if (!target || !target.closest) return null;
    for (var i = 0; i < rules.length; i++) {
      if (target.closest(rules[i].match)) return rules[i].topicId;
    }
    return null;
  }

  function onDocumentReaction(target, rules) {
    if (!target || (rootEl && rootEl.contains(target))) return;
    var topicId = matchRule(target, rules);
    if (topicId) {
      showTopic(topicId, { source: 'auto', spotlight: false, scroll: false });
    }
  }

  function handleToolsAction(act) {
    var lang = getLang();
    var c = COPY[lang];
    var p = getSafeFeaturedProof();

    if (act === 'daily-pdf') {
      window.open(p.pdf || 'https://min7014.github.io/', '_blank', 'noopener');
    } else if (act === 'daily-yt') {
      window.open(p.yt || 'video_board.html', '_blank', 'noopener');
    } else if (act === 'daily-voice') {
      if (lang === 'ko' && typeof window.speakTodayGeoGebra === 'function') {
        try { window.speakTodayGeoGebra(); return; } catch (e) {}
      }
      var scriptTxt = stripLatexInline(((p.title && (p.title[lang] || p.title.ko)) || '') + '. ' + ((p.desc && (p.desc[lang] || p.desc.ko)) || ''));
      speakTextClean(scriptTxt, (p.title && p.title[lang]) || '', lang);
    } else if (act === 'omni-search') {
      var inp = document.getElementById('headerGlobalSearchInput') || document.getElementById('quizSearchInput');
      if (inp) {
        try { inp.focus(); inp.click(); } catch (e) {}
      }
    } else if (act === 'mathlab') {
      window.location.href = 'mathlab.html';
    } else if (act === 'explorer') {
      if (typeof window.openMin7014ExplorerModal === 'function') window.openMin7014ExplorerModal();
    } else if (act === 'random-quiz') {
      if (typeof window.startRandomQuiz === 'function') window.startRandomQuiz();
    } else if (act === 'lesson-pack') {
      if (typeof window.toggleLessonPackMode === 'function') {
        window.toggleLessonPackMode(true);
        var qBar = document.getElementById('quizFilterBar');
        if (qBar && qBar.scrollIntoView) qBar.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    } else if (act === 'invite-qr') {
      try {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(c.inviteMsg).catch(function () {});
        }
      } catch (e) {}
      if (!inviteRewardedSession) {
        inviteRewardedSession = true;
        try {
          if (window.MatheduGame && typeof window.MatheduGame.addXP === 'function') {
            window.MatheduGame.addXP(15, lang === 'en' ? 'Free Invite Shared' : '100% 무료 학습 초대 공유');
          }
        } catch (e) {}
      }
      showMiniToast(c.inviteCopiedToast);
      if (typeof window.openYoutubeSeedIgniteModal === 'function') {
        try { window.openYoutubeSeedIgniteModal(); } catch (e) {}
      }
    }
  }

  function handleStudyAction(act) {
    var lang = getLang();
    var c = COPY[lang];
    var snap = getStudySnapshot();
    if (act === 'badges') {
      if (window.MatheduGame && typeof window.MatheduGame.showBadgesModal === 'function') window.MatheduGame.showBadgesModal();
    } else if (act === 'history') {
      if (window.MatheduAuth) {
        if (typeof window.MatheduAuth.isLoggedIn === 'function' && window.MatheduAuth.isLoggedIn()) {
          window.MatheduAuth.showMyProblemsModal();
        } else if (typeof window.MatheduAuth.showAuthModal === 'function') {
          window.MatheduAuth.showAuthModal();
        }
      }
    } else if (act === 'bookmarks') {
      if (typeof window.switchFilterMode === 'function') {
        window.switchFilterMode('bookmarks');
        var qBar = document.getElementById('quizFilterBar');
        if (qBar && qBar.scrollIntoView) qBar.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    } else if (act === 'revenge') {
      if (snap.wrongs && snap.wrongs.length > 0 && snap.wrongs[0].slug) {
        window.location.href = 'board/' + encodeURIComponent(snap.wrongs[0].slug) + '.html';
      } else {
        if (typeof window.switchFilterMode === 'function') window.switchFilterMode('wrong');
        showMiniToast(c.noWrongToast);
      }
    } else if (act === 'clinic') {
      if (typeof window.openMathClinicModal === 'function') window.openMathClinicModal();
    } else if (act === 'quest') {
      window.location.href = 'game.html';
    }
  }

  function handleCardClick(ev) {
    var lang = getLang();
    var c = COPY[lang];

    var tabBtn = ev.target && ev.target.closest ? ev.target.closest('[data-mg-tab]') : null;
    if (tabBtn) {
      setTab(tabBtn.getAttribute('data-mg-tab'));
      return;
    }

    var topicBtn = ev.target && ev.target.closest ? ev.target.closest('[data-mg-topic]') : null;
    if (topicBtn) {
      var tid = topicBtn.getAttribute('data-mg-topic');
      showTopic(tid, { source: 'manual', spotlight: true, scroll: false });
      return;
    }

    var toolBtn = ev.target && ev.target.closest ? ev.target.closest('[data-mg-tool]') : null;
    if (toolBtn) {
      handleToolsAction(toolBtn.getAttribute('data-mg-tool'));
      return;
    }

    var studyBtn = ev.target && ev.target.closest ? ev.target.closest('[data-mg-study]') : null;
    if (studyBtn) {
      handleStudyAction(studyBtn.getAttribute('data-mg-study'));
      return;
    }

    var timerBtn = ev.target && ev.target.closest ? ev.target.closest('[data-mg-timer]') : null;
    if (timerBtn) {
      var ta = timerBtn.getAttribute('data-mg-timer');
      if (ta === 'preset-15') startTimer(900);
      else if (ta === 'preset-25') startTimer(1500);
      else if (ta === 'toggle-pause') toggleTimerPause();
      else if (ta === 'reset') resetTimer();
      return;
    }

    var colDot = ev.target && ev.target.closest ? ev.target.closest('[data-mg-pad-color]') : null;
    if (colDot) {
      padColor = colDot.getAttribute('data-mg-pad-color') || '#0284c7';
      padEraser = false;
      renderCardContent(false);
      return;
    }

    var padBtn = ev.target && ev.target.closest ? ev.target.closest('[data-mg-pad]') : null;
    if (padBtn) {
      var pa = padBtn.getAttribute('data-mg-pad');
      if (pa === 'eraser') {
        padEraser = !padEraser;
        renderCardContent(false);
      } else if (pa === 'undo') {
        if (padStrokes.length > 0) {
          padStrokes.pop();
          savePadStrokes();
          redrawPadCanvas();
        }
      } else if (pa === 'clear') {
        padStrokes = [];
        savePadStrokes();
        redrawPadCanvas();
        showMiniToast(c.padClearedToast);
      }
      return;
    }

    var actEl = ev.target && ev.target.closest ? ev.target.closest('[data-mg-act]') : null;
    if (!actEl) return;
    var act = actEl.getAttribute('data-mg-act');
    if (act === 'close') {
      closeCard();
    } else if (act === 'edge-tuck') {
      edgeTuckOrb();
    } else if (act === 'quick-lang') {
      if (window.MatheduI18n && typeof window.MatheduI18n.toggleLanguage === 'function') {
        window.MatheduI18n.toggleLanguage();
      }
      if (typeof window.syncSiteThemeUI === 'function') {
        try { window.syncSiteThemeUI(); } catch (e) {}
      }
    } else if (act === 'quick-theme') {
      if (typeof window.toggleSiteDarkMode === 'function') {
        window.toggleSiteDarkMode();
      }
    } else if (act === 'quick-voice') {
      if (state.activeTab === 'tools') {
        handleToolsAction('daily-voice');
      } else {
        var tObj = TOPIC_MAP[state.activeTopicId] || TOPICS[0];
        var vText = (tObj.title[lang] || '') + '. ' + (tObj.body[lang] || '') + ' ' + (tObj.tipLine[lang] || '');
        speakTextClean(vText, tObj.title[lang] || '', lang);
      }
    } else if (act === 'reset-pos') {
      resetPosition();
    } else if (act === 'toggle-detail') {
      state.detailed = !state.detailed;
      saveState();
      renderCardContent(true);
    } else if (act === 'toggle-all') {
      state.showAllTopics = !state.showAllTopics;
      renderCardContent(true);
    } else if (act === 'toggle-auto') {
      setAutoTips(!state.autoTips);
    } else if (act === 'locate') {
      var cur = TOPIC_MAP[state.activeTopicId];
      if (cur) spotlightTopic(cur, true);
    }
  }

  function startPointerDrag(captureEl, ev, allowClickToggle) {
    if (ev.pointerType === 'mouse' && ev.button !== 0) return;
    if (!allowClickToggle && ev.target && ev.target.closest && ev.target.closest('button')) return;

    dragSession = {
      pointerId: ev.pointerId,
      captureEl: captureEl,
      allowClickToggle: !!allowClickToggle,
      startX: ev.clientX,
      startY: ev.clientY,
      origLeft: state.left || 0,
      origTop: state.top || 0,
      moved: false
    };
    try { captureEl.setPointerCapture(ev.pointerId); } catch (e) {}
  }

  function onGlobalPointerMove(ev) {
    if (!dragSession || ev.pointerId !== dragSession.pointerId) return;
    var dx = ev.clientX - dragSession.startX;
    var dy = ev.clientY - dragSession.startY;
    var dist = Math.hypot(dx, dy);

    if (!dragSession.moved && dist >= DRAG_THRESHOLD_PX) {
      dragSession.moved = true;
      state.edgeTucked = null;
      if (orbEl) orbEl.classList.add('mg-dragging');
      if (orbEl) orbEl.classList.remove('mg-edge-tuck-left', 'mg-edge-tuck-right');
      if (rootEl) rootEl.classList.add('mg-dragging-root');
      if (dragHintEl) dragHintEl.style.display = 'none';
    }
    if (!dragSession.moved) return;

    var c = clampCoords(dragSession.origLeft + dx, dragSession.origTop + dy);
    state.left = c.left;
    state.top = c.top;
    if (orbEl) {
      orbEl.style.left = c.left + 'px';
      orbEl.style.top = c.top + 'px';
      orbEl.classList.toggle('mg-orb-left', c.left < window.innerWidth / 2);
    }
    positionCardNearOrb();
  }

  function onGlobalPointerUp(ev) {
    if (!dragSession || ev.pointerId !== dragSession.pointerId) return;
    var s = dragSession;
    dragSession = null;

    if (orbEl) orbEl.classList.remove('mg-dragging');
    if (rootEl) rootEl.classList.remove('mg-dragging-root');
    try { s.captureEl.releasePointerCapture(ev.pointerId); } catch (e) {}

    if (s.moved) {
      var firstDragEver = !state.hasDraggedOnce;
      var bounds = clampCoords(state.left, state.top);
      var spanX = Math.max(1, bounds.maxX - bounds.minX);
      var spanY = Math.max(1, bounds.maxY - bounds.minY);
      state.customPos = {
        rx: (bounds.left - bounds.minX) / spanX,
        ry: (bounds.top - bounds.minY) / spanY
      };
      if (!state.open && bounds.left <= bounds.minX + 6) {
        state.edgeTucked = 'left';
      } else if (!state.open && bounds.left >= bounds.maxX - 6) {
        state.edgeTucked = 'right';
      } else {
        state.edgeTucked = null;
      }
      state.hasDraggedOnce = true;
      state.seenTopics.report_drag = true;
      savePos();
      saveState();
      syncCoordsToViewport();
      renderCardContent(true);
      if (firstDragEver) {
        showMiniToast(COPY[getLang()].posSavedToast);
      }
    } else if (s.allowClickToggle) {
      onOrbSelected();
    }
  }

  function setupObserversAndGlobalListeners() {
    document.addEventListener('click', function (ev) {
      onDocumentReaction(ev.target, CLICK_RULES);
    }, { passive: true, capture: true });

    document.addEventListener('focusin', function (ev) {
      onDocumentReaction(ev.target, FOCUS_RULES);
    }, { passive: true });

    document.addEventListener('input', function (ev) {
      onDocumentReaction(ev.target, INPUT_RULES);
    }, { passive: true });

    window.addEventListener('mathedu:xp-updated', function () {
      updateOrbStarTier();
      if (state.open && state.activeTab === 'study') renderCardContent(false);
    });
    window.addEventListener('mathedu:streak-updated', function () {
      updateOrbStarTier();
      if (state.open && state.activeTab === 'study') renderCardContent(false);
    });

    if (typeof IntersectionObserver !== 'undefined') {
      var deepEl = document.getElementById('deepMathLabsHub');
      if (deepEl) {
        var io = new IntersectionObserver(function (entries) {
          for (var i = 0; i < entries.length; i++) {
            if (entries[i].isIntersecting && !state.open && state.autoTips && !state.seenTopics.deep_labs) {
              showTopic('deep_labs', { source: 'auto', spotlight: false, scroll: false });
            }
          }
        }, { threshold: 0.45 });
        io.observe(deepEl);
      }
    }

    if (typeof MutationObserver !== 'undefined') {
      var htmlObs = new MutationObserver(function () {
        var lang = getLang();
        var dark = isDark();
        if (lang !== lastRenderedLang || dark !== lastRenderedDark) {
          renderCardContent(false);
        }
      });
      htmlObs.observe(document.documentElement, { attributes: true, attributeFilter: ['class', 'lang', 'data-theme'] });

      if (document.body) {
        var bodyObs = new MutationObserver(function () {
          if (isInspectorActive() && state.open) {
            closeCard();
          }
        });
        bodyObs.observe(document.body, { attributes: true, attributeFilter: ['class'] });
      }
    }
  }

  function buildDom() {
    if (document.getElementById('matheduGuideRoot')) return;

    rootEl = document.createElement('div');
    rootEl.id = 'matheduGuideRoot';
    rootEl.setAttribute('data-no-i18n', '1');

    orbEl = document.createElement('button');
    orbEl.id = 'matheduGuideOrb';
    orbEl.type = 'button';
    orbEl.setAttribute('data-no-i18n', '1');
    orbEl.innerHTML = [
      '<span class="mg-orb-grip" aria-hidden="true"><span></span><span></span><span></span><span></span><span></span><span></span></span>',
      '<span id="mgOrbTimerBadge" aria-hidden="true">15:00</span>',
      '<svg class="mg-orb-ring" viewBox="0 0 56 56" aria-hidden="true">',
      '  <circle cx="28" cy="28" r="26" fill="none" stroke="currentColor" stroke-opacity="0.22" stroke-width="1.5" stroke-dasharray="3 3"></circle>',
      '  <circle id="mgOrbProgressArc" cx="28" cy="28" r="26" fill="none" stroke="#10B981" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="163.4" stroke-dashoffset="163.4"></circle>',
      '</svg>',
      '<span class="mg-orb-icon" aria-hidden="true">',
      '  <svg width="24" height="24" viewBox="0 0 24 24" fill="none">',
      '    <path d="M12 3.2L14.2 9.4L20.4 11.6L14.2 13.8L12 20L9.8 13.8L3.6 11.6L9.8 9.4L12 3.2Z" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>',
      '    <circle cx="12" cy="11.6" r="1.7" fill="currentColor"/>',
      '    <path d="M6.8 19.6L12 5.2L17.2 19.6" stroke="currentColor" stroke-width="1.35" stroke-linecap="round" stroke-opacity="0.72"/>',
      '  </svg>',
      '</span>',
      '<span id="mgOrbDragPill" class="mg-drag-pill" aria-hidden="true"></span>'
    ].join('');

    toastPillEl = document.createElement('div');
    toastPillEl.id = 'mgOrbToast';
    toastPillEl.setAttribute('role', 'status');
    toastPillEl.setAttribute('data-no-i18n', '1');

    cardEl = document.createElement('section');
    cardEl.id = 'matheduGuideCard';
    cardEl.setAttribute('role', 'dialog');
    cardEl.setAttribute('aria-live', 'polite');
    cardEl.setAttribute('data-no-i18n', '1');
    cardEl.style.display = 'none';

    rootEl.appendChild(cardEl);
    rootEl.appendChild(toastPillEl);
    rootEl.appendChild(orbEl);
    document.body.appendChild(rootEl);

    orbTimerBadgeEl = document.getElementById('mgOrbTimerBadge');
    dragHintEl = document.getElementById('mgOrbDragPill');
    progressCircleEl = document.getElementById('mgOrbProgressArc');

    orbEl.addEventListener('pointerdown', function (ev) {
      startPointerDrag(orbEl, ev, true);
    });
    orbEl.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter' || ev.key === ' ') {
        ev.preventDefault();
        onOrbSelected();
      }
    });

    cardEl.addEventListener('pointerdown', function (ev) {
      var handle = ev.target && ev.target.closest ? ev.target.closest('.mg-drag-handle') : null;
      if (handle) {
        startPointerDrag(handle, ev, false);
      }
    });
    cardEl.addEventListener('click', handleCardClick);

    window.addEventListener('pointermove', onGlobalPointerMove);
    window.addEventListener('pointerup', onGlobalPointerUp);
    window.addEventListener('pointercancel', onGlobalPointerUp);
    window.addEventListener('resize', syncCoordsToViewport);
    window.addEventListener('orientationchange', syncCoordsToViewport);
    window.addEventListener('mathedu:lang-changed', function () {
      renderCardContent(true);
    });
  }

  function init() {
    loadPersistedState();
    injectStyles();
    buildDom();
    setupObserversAndGlobalListeners();
    syncCoordsToViewport();
    renderCardContent(true);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  window.MatheduGuide = {
    open: openCard,
    close: closeCard,
    toggle: toggleCard,
    setTab: setTab,
    edgeTuck: edgeTuckOrb,
    startTimer: startTimer,
    pauseTimer: toggleTimerPause,
    resetTimer: resetTimer,
    getPadStrokes: function () { return padStrokes.slice(); },
    showTopic: function (topicId, opts) {
      return showTopic(topicId, opts || { source: 'manual', spotlight: true, scroll: false });
    },
    setDetailed: function (flag) {
      state.detailed = !!flag;
      if (state.detailed) {
        state.open = true;
        state.activeTab = 'guide';
      }
      saveState();
      renderCardContent(true);
    },
    setAutoTips: setAutoTips,
    resetPosition: resetPosition,
    resetSeen: resetSeen,
    getTopics: function () {
      return TOPICS.map(function (t) { return t.id; });
    },
    getState: function () {
      return {
        open: state.open,
        detailed: state.detailed,
        activeTab: state.activeTab,
        edgeTucked: state.edgeTucked,
        starTier: computeStarTier(),
        activeTopicId: state.activeTopicId,
        seenTopics: Object.assign({}, state.seenTopics),
        autoTips: state.autoTips,
        hasDraggedOnce: state.hasDraggedOnce,
        left: state.left,
        top: state.top,
        customPos: state.customPos,
        timerRunning: timerState.running,
        timerRemainingSec: timerState.remainingSec
      };
    }
  };
})(window, document);
