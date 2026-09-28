/**
 * mathedu-i18n.js
 * min7014 mathedu · Global Internationalization (i18n) Engine
 * Supports Korean (ko) and English (en) with zero-latency instant switching.
 */
(function(window) {
  'use strict';

  var STORAGE_KEY = 'mathedu_lang';

  var DICTIONARY = {
    ko: {
      nav: {
        allQuizzes: "📚 퀴즈 모음",
        offlineVault: "📦 오프라인 보관함",
        offlineVaultTitle: "인터넷 없이 풀 수 있는 오프라인 전체 문제 보관함",
        minExplorer: "🌐 min7014 기하 탐색관",
        myBadges: "🏆 나의 업적",
        createQuiz: "✨ 문제 출제",
        membersOnly: "회원전용",
        dashboard: "📊 수업 대시보드",
        minHome: "🌐 min7014 홈"
      },
      hero: {
        badgePill: "🏛️ 대한민국의 수학교사 민은기 · 세계적인 수학교사의 평생 연구실",
        mainTitleLab: "min7014",
        mainTitleHub: "mathedu",
        leadDesc: "대한민국의 수학교사 민은기 선생님의 3,400+ 평생 시각적 증명과 단델린 구의 통찰을 담은 <b>가입 없는 100% 영구 무료 인터랙티브 수학 플랫폼</b>",
        emblemCaption: "📐 공식 엠블럼",
        emblemSub: "Dandelin Spheres",
        emblemTitle: "클릭하여 단델린 구의 기하학적 원리 보기",
        pill1: "⚡ 학생: 무가입 5초 즉시 학습",
        pill2: "🎯 0~5단계 개념 빌드업",
        pill3: "📊 실시간 교실 현황 분석 (stu1~ 익명 보호)",
        pill4: "📦 100% 오프라인 다운로드",
        pill5: "🔐 회원 전용 출제 & 배포",
        storyBtn: "엠블럼의 수학적 원리 (단델린의 구와 원뿔곡선)",
        storyDrawerTitle: "🔬 단델린의 구(Dandelin Spheres)와 원뿔곡선의 기하학적 증명",
        storyDrawerP1: "원뿔을 비스듬한 평면으로 자를 때 생기는 곡선(쌍곡선/타원/포물선)에 내접하는 두 개의 구를 <b>단델린의 구</b>라고 합니다.",
        storyDrawerP2: "구가 평면과 접하는 점($F_1, F_2$)이 바로 원뿔곡선의 <b>초점(Focus)</b>이 되며, 곡선 위의 점에서 두 초점까지의 거리의 차(또는 합)가 일정함을 입체 기하학으로 우아하게 밝혀냅니다.",
        storyDrawerQuote: '"수식에 갇히지 않고, 눈으로 원리를 통찰하는 수학"',
        storyDrawerAuthor: "대한민국의 수학교사 민은기 선생님의 평생 수학 교육 철학입니다.",
        statTopics: "🏛️ 평생 수학 주제",
        statAssets: "📐 GeoGebra & PDF 증명",
        statQuizzes: "🎯 수능·모평 디딤돌 퀴즈",
        statRigor: "⚡ 무결성 오프라인 & 관제"
      },
      gamification: {
        streakDay: "연속 출석 {day}일차",
        streakSub: "오늘 수학 문제 풀면 불꽃 유지!",
        levelTitle: "🔰 Lv.{lvl} {title}",
        badgesBtn: "🏆 나의 뱃지",
        wrongVaultBtn: "🔴 오답노트 ({cnt})",
        novice: "디딤돌 입문자",
        apprentice: "개념 탐험가",
        adept: "기하 증명가",
        expert: "원뿔곡선 마스터",
        master: "수학의 거장"
      },
      todayGgb: {
        tag: "💡 오늘의 추천 동적 기하 (min7014 수학자료실)",
        title: "타원에서의 빛 반사 (Reflection of Light on an Ellipse)",
        desc: "한 초점에서 나온 빛은 타원에 반사되어 다른 초점을 반드시 통과합니다. GeoGebra 앱렛으로 초점을 직접 끌어보며 기하학적 궤적을 확인하세요.",
        btnApplet: "🎮 GeoGebra로 조작하기 ➔",
        btnPdf: "📄 원리 증명 PDF"
      },
      heroCards: {
        teacherTag: "👩‍🏫 교사 회원 전용 · 수업 배포",
        teacherTitle: "3초 만에 수업 개설하기",
        teacherDesc: "회원 로그인 후 즉시 고유 수업 코드를 생성하고, 칠판 빔프로젝터용 대형 QR코드와 학생 배포용 링크를 발급받으세요.",
        teacherBtn: "🚀 3초 수업 개설 (QR)",
        createTag: "🤖 수능·모평 기출 전용 · 1일 1문제",
        createTitle: "✨ 수능·모의평가 기출 출제",
        createDesc: "공개된 <b>수능 및 모의평가(평가원/교육청) 기출문제</b>를 올리면, <b>안티그래비티 AI</b>가 초·중학생도 풀 수 있는 <b>5~8단계 인터랙티브 빌드업 퀴즈</b>로 자동 제작하여 깃에 배포합니다. (정회원 1일 1문제)",
        createBtn: "✨ 수능·모평 퀴즈 만들기 (회원 전용) ➔",
        studentTag: "🧑‍🎓 비회원·학생 · 100% 자유 풀이",
        studentTitle: "수업 코드로 입장하기 (또는 자유 풀이)",
        studentDesc: "회원가입 없이 누구나 전체 문제를 자유롭게 열람하고 단계별 풀이를 시작할 수 있습니다. 고유 이름과 비밀번호를 등록하면 언제든 내 기록을 모아볼 수 있습니다.",
        studentPlaceholder: "예: MATH-A8F2",
        studentJoinBtn: "입장 ➔",
        studentMySolved: "📂 내가 푼 문제 모아보기",
        studentGuestSync: "👤 비회원 이름·비번 연동",
        studentMyLibrary: "📂 내 서재 ({cnt}개 문항)",
        studentSolvedCount: "📂 푼 문제 ({cnt}개)",
        studentUpgrade: "✨ 정회원 전환"
      },
      filterTabs: {
        allQuizzes: "📚 전체 퀴즈",
        wrongVault: "🔴 나의 오답노트",
        bookmarks: "⭐ 즐겨찾기",
        lessonPack: "🎒 교사용 수업 팩 묶기"
      },
      examFinder: {
        title: "수능·모의평가 기출 정밀 탐색기",
        subtitle: "(학년도 · 학년 · 시행월 · 선택과목 · 번호 선택 시 해당 문제만 즉시 추출)",
        resetBtn: "🔄 필터 전체 초기화",
        policyTitle: "공개 원칙:",
        policyText: "본 게시판은 저작권이 투명한 <b>대학수학능력시험(대수능) 및 한국교육과정평가원·시도교육청 모의평가(전국연합학력평가) 기출문제만 선별 공개</b>합니다. (기타 사설·경시·일반 문제는 비공개 전환)",
        labelYear: "📅 학년도",
        allYears: "전체 학년도",
        yearOption: "{year}학년도",
        yearBefore2020: "2020학년도 이전",
        labelGrade: "🎓 대상 학년",
        allGrades: "전체 학년",
        gradeHigh3: "고3 · N수",
        gradeHigh2: "고2",
        gradeHigh1: "고1",
        labelMonth: "🗓️ 시행월 (시험명)",
        allMonths: "전체 시행월",
        month11: "11월 수능 (대수능)",
        month9: "9월 모의평가 (평가원)",
        month6: "6월 모의평가 (평가원)",
        month10: "10월 학력평가",
        month7: "7월 학력평가",
        month4: "4월 학력평가",
        month3: "3월 학력평가",
        labelSubject: "📐 선택과목",
        allSubjects: "전체 과목",
        subCommon12: "공통 (수학I·II)",
        subCalc: "미적분",
        subGeom: "기하",
        subProb: "확률과 통계",
        subCommon1: "공통수학 (고1)",
        labelNum: "🔢 문항 번호",
        allNums: "전체 번호 (1~30)",
        searchPlaceholder: "🔍 문제 제목, 키워드(포물선, 수열, 미분, 확률 등), 슬러그 직접 검색...",
        topicPrefix: "주제별:",
        topicAll: "전체보기",
        topicQuad: "이차함수·포물선",
        topicSeq: "수열",
        topicProb: "확률·통계",
        topicExp: "지수·로그",
        topicTrig: "삼각함수",
        topicCalc: "미적분"
      },
      listHeader: {
        title: "📚 수능·모의평가 기출 인터랙티브 퀴즈 목록 (비회원 누구나 100% 무료 열람 & 즉시 풀이)",
        newQuiz: "✨ 새 퀴즈 출제하기",
        liveDashboard: "📊 전체 실시간 현황판"
      },
      cards: {
        exactMatchFound: "선택하신 기출문항을 정확히 찾았습니다!",
        instantSolve: "🚀 1초 바로 풀기 ➔",
        slugLabel: "슬러그:",
        btnLaunch: "🚀 수업 열기",
        btnOffline: "📥 오프라인",
        btnOfflineTitle: "인터넷 없이 풀 수 있는 단독 오프라인 HTML 파일 다운로드",
        btnSolve: "풀기 ➔",
        btnResume: "🚀 이어서 풀기 ➔",
        btnReSolve: "🔄 다시 풀기 ➔",
        badgeCompleted: "🏆 완주",
        bmAdd: "즐겨찾기 추가",
        bmRemove: "즐겨찾기 해제",
        emptyWrongTitle: "오답노트가 깨끗하게 비어 있습니다!",
        emptyWrongDesc: "틀린 문제가 없거나 모든 오답을 성공적으로 복습하셨습니다. 완벽합니다!",
        emptyBmTitle: "즐겨찾기한 문제가 아직 없습니다",
        emptyBmDesc: "문제 카드 오른쪽의 별표(☆)를 누르면 나만의 핵심 유형으로 보관할 수 있습니다.",
        emptyFilterTitle: "선택하신 조건의 기출문항이 아직 등록되지 않았습니다",
        emptyFilterDesc: "문항을 지금 바로 출제 요청하시면, 안티그래비티 AI가 5~8단계 인터랙티브 빌드업 퀴즈와 GeoGebra 시각화로 자동 제작해 드립니다.",
        emptyRequestBtn: "✨ 이 기출문제 지금 출제 요청하기 ➔",
        btnViewAll: "전체 문제 둘러보기 ➔",
        noMatch: "검색 조건에 일치하는 퀴즈가 없습니다."
      },
      pack: {
        floatTitle: "선택한 {cnt}개 문제로 수업 팩 만들기",
        floatDesc: "학생들에게 링크 1개로 오늘 수업할 문항들을 순서대로 제공합니다.",
        btnCopyLink: "📋 학생 배포 링크 복사",
        btnQr: "🖥️ 칠판 대형 QR",
        btnStart: "▶️ 1번 바로 풀기"
      },
      footer: {
        brandDesc: "min7014 mathedu · 단계별 인터랙티브 수학교육 플랫폼",
        collabDesc: "민은기 선생님의 3,400+ 수학 자료실과 안티그래비티 AI가 함께 만드는 수학교육의 새 지평",
        terms: "이용약관",
        privacy: "개인정보처리방침",
        home: "min7014 홈",
        github: "GitHub 저장소"
      },
      meta: {
        yearSuffix: "학년도",
        qNumSuffix: "번",
        gradeHigh3: "고3",
        gradeHigh2: "고2",
        gradeHigh1: "고1",
        subjectCommon12: "공통(수학I·II)",
        subjectCalc: "미적분",
        subjectGeom: "기하",
        subjectProb: "확률과 통계",
        subjectCommon1: "공통수학"
      },
      dashboard: {
        backHome: "🏠 mathedu 홈",
        refresh: "🔄 새로고침",
        anonOn: "🛡️ 학생 익명 보호(stu1~): ON",
        anonOff: "👤 실명 모드: ON",
        exportCsv: "📊 채점표(CSV) 저장",
        liveSync: "3초 실시간 자동 동기화",
        title: "📊 실시간 수업 모니터링 대시보드",
        subtitle: "학생들의 실시간 디딤돌 풀이 진행 상황 및 성취도 관제"
      }
    },
    en: {
      nav: {
        allQuizzes: "📚 All Quizzes",
        offlineVault: "📦 Offline Archive",
        offlineVaultTitle: "Download standalone quizzes that run without internet",
        minExplorer: "🌐 min7014 Geometry Lab",
        myBadges: "🏆 My Badges",
        createQuiz: "✨ Create Quiz",
        membersOnly: "Members",
        dashboard: "📊 Classroom Dashboard",
        minHome: "🌐 min7014 Home"
      },
      hero: {
        badgePill: "🏛️ Min Eun-gi — Korea's Master Mathematics Educator · Global Visual Geometry Lab",
        mainTitleLab: "min7014",
        mainTitleHub: "mathedu",
        leadDesc: "Lifelong Mathematical Legacy of Master Educator Min Eun-gi: Over 3,400 Dynamic Visual Proofs & Scaffolding Quizzes, <b>100% Freely Open Worldwide</b>",
        emblemCaption: "📐 Official Emblem",
        emblemSub: "Dandelin Spheres",
        emblemTitle: "Click to explore the geometric principle of Dandelin Spheres",
        pill1: "⚡ Students: 5-sec Instant Start (No Signup)",
        pill2: "🎯 3~8 Step Guided Scaffolding",
        pill3: "📊 Real-Time Class Dashboard (stu1~ Privacy Protected)",
        pill4: "📦 100% Offline Single-File HTML",
        pill5: "🔐 Verified Teacher Quiz Creation",
        storyBtn: "Mathematical Principle of the Emblem (Dandelin Spheres & Conics)",
        storyDrawerTitle: "🔬 Geometric Proof of Dandelin Spheres & Conic Sections",
        storyDrawerP1: "When an oblique cutting plane intersects a double cone, the two spheres inscribed in the cone and tangent to the plane are known as <b>Dandelin Spheres</b>.",
        storyDrawerP2: "The points of tangency where the spheres touch the plane ($F_1, F_2$) are precisely the <b>foci</b> of the conic section (ellipse, parabola, or hyperbola). This solid geometry construction elegantly proves that the sum or difference of distances from any point on the curve to the two foci is constant.",
        storyDrawerQuote: '"Math that frees you from blind calculation to see the deep visual principle."',
        storyDrawerAuthor: "The lifelong pedagogical philosophy of Master Educator Min Eun-gi.",
        statTopics: "🏛️ Lifelong Math Topics",
        statAssets: "📐 GeoGebra & Visual Proofs",
        statQuizzes: "🎯 College Entrance Quizzes",
        statRigor: "⚡ Offline Rigor & Live Monitor"
      },
      gamification: {
        streakDay: "Day {day} Streak",
        streakSub: "Solve a problem today to keep the flame burning!",
        levelTitle: "🔰 Lv.{lvl} {title}",
        badgesBtn: "🏆 My Badges",
        wrongVaultBtn: "🔴 Review Vault ({cnt})",
        novice: "Scaffolding Novice",
        apprentice: "Concept Explorer",
        adept: "Geometric Prover",
        expert: "Conic Section Master",
        master: "Grand Mathematician"
      },
      todayGgb: {
        tag: "💡 Today's Featured Dynamic Geometry (min7014 Lab)",
        title: "Reflection of Light on an Ellipse (Optical Property)",
        desc: "A ray of light emanating from one focus reflects off the ellipse and always passes through the other focus. Drag the focal points in GeoGebra to discover the locus interactively.",
        btnApplet: "🎮 Explore in GeoGebra ➔",
        btnPdf: "📄 Visual Proof PDF"
      },
      heroCards: {
        teacherTag: "👩‍🏫 For Teachers · Instant Classroom Distribution",
        teacherTitle: "Launch a Classroom in 3 Seconds",
        teacherDesc: "Instantly generate a unique classroom session code, projector QR code, and student link without student accounts.",
        teacherBtn: "🚀 3-Sec Launch (QR)",
        createTag: "🤖 AI Scaffolding · Standardized Math Exams",
        createTitle: "✨ Create Exam Stepping-Stone Quiz",
        createDesc: "Upload an official exam question, and Antigravity AI automatically structures it into a <b>3~8 step interactive scaffolding quiz</b> with GeoGebra visual proofs.",
        createBtn: "✨ Create Exam Quiz (Members) ➔",
        studentTag: "🧑‍🎓 Students & Guests · 100% Free Practice",
        studentTitle: "Join with Class Code (or Free Practice)",
        studentDesc: "Explore all problems freely with interactive step-by-step guidance. Register your name and passcode to preserve and sync your solved problem history.",
        studentPlaceholder: "e.g. MATH-A8F2",
        studentJoinBtn: "Join ➔",
        studentMySolved: "📂 My Solved Problems",
        studentGuestSync: "👤 Sync Guest Profile",
        studentMyLibrary: "📂 My Library ({cnt} problems)",
        studentSolvedCount: "📂 Solved ({cnt})",
        studentUpgrade: "✨ Upgrade to Member"
      },
      filterTabs: {
        allQuizzes: "📚 All Quizzes",
        wrongVault: "🔴 My Review Vault",
        bookmarks: "⭐ Bookmarks",
        lessonPack: "🎒 Bundle Lesson Pack"
      },
      examFinder: {
        title: "Standardized Math Exam Problem Finder",
        subtitle: "(Filter instantly by Exam Year, Grade, Month, Subject & Question #)",
        resetBtn: "🔄 Reset All Filters",
        policyTitle: "Public Policy:",
        policyText: "This repository features public Korean CSAT (College Scholastic Ability Test) and official mock examination questions transformed into pedagogical step-by-step visual scaffolding ladders.",
        labelYear: "📅 Exam Year",
        allYears: "All Exam Years",
        yearOption: "Academic Year {year}",
        yearBefore2020: "Before Year 2020",
        labelGrade: "🎓 Grade Level",
        allGrades: "All Grades",
        gradeHigh3: "Grade 12 (College Bound)",
        gradeHigh2: "Grade 11",
        gradeHigh1: "Grade 10",
        labelMonth: "🗓️ Exam Month / Name",
        allMonths: "All Exam Months",
        month11: "Nov Official CSAT",
        month9: "Sep Official Mock",
        month6: "Jun Official Mock",
        month10: "Oct Academic Exam",
        month7: "Jul Academic Exam",
        month4: "Apr Academic Exam",
        month3: "Mar Academic Exam",
        labelSubject: "📐 Math Subject",
        allSubjects: "All Subjects",
        subCommon12: "Common (Math I·II)",
        subCalc: "Calculus",
        subGeom: "Geometry",
        subProb: "Probability & Statistics",
        subCommon1: "Common Math (Grade 10)",
        labelNum: "🔢 Question Number",
        allNums: "All Numbers (1~30)",
        searchPlaceholder: "🔍 Search problem title, topic (parabola, sequence, derivative, probability), slug...",
        topicPrefix: "Topics:",
        topicAll: "All Topics",
        topicQuad: "Quadratic & Parabola",
        topicSeq: "Sequences",
        topicProb: "Probability & Stats",
        topicExp: "Exponents & Logs",
        topicTrig: "Trigonometry",
        topicCalc: "Calculus"
      },
      listHeader: {
        title: "📚 Interactive Scaffolding Math Problem Quizzes (100% Free & Open Access)",
        newQuiz: "✨ Create New Quiz",
        liveDashboard: "📊 Live Class Monitor"
      },
      cards: {
        exactMatchFound: "Found the exact matching exam problem!",
        instantSolve: "🚀 Instant Solve ➔",
        slugLabel: "Slug:",
        btnLaunch: "🚀 Launch Class",
        btnOffline: "📥 Offline HTML",
        btnOfflineTitle: "Download standalone single-file HTML that runs offline without internet",
        btnSolve: "Solve ➔",
        btnResume: "🚀 Resume ➔",
        btnReSolve: "🔄 Re-solve ➔",
        badgeCompleted: "🏆 Mastered",
        bmAdd: "Add to Bookmarks",
        bmRemove: "Remove from Bookmarks",
        emptyWrongTitle: "Your Review Vault is completely clean!",
        emptyWrongDesc: "You have no unsolved mistakes or have successfully mastered all review questions. Outstanding!",
        emptyBmTitle: "No bookmarked questions yet",
        emptyBmDesc: "Click the star icon (☆) on any problem card to save it as your core reference collection.",
        emptyFilterTitle: "No exam problem found matching these exact criteria yet",
        emptyFilterDesc: "Request this specific exam question now, and Antigravity AI will automatically craft a 3~8 step interactive scaffolding quiz with GeoGebra visual proofs.",
        emptyRequestBtn: "✨ Request this Exam Problem Now ➔",
        btnViewAll: "Browse All Quizzes ➔",
        noMatch: "No quizzes match your current search criteria."
      },
      pack: {
        floatTitle: "Create a Lesson Pack with {cnt} Selected Problems",
        floatDesc: "Provide students with a single link to practice today's curated sequence of problems.",
        btnCopyLink: "📋 Copy Student Link",
        btnQr: "🖥️ Large Projector QR",
        btnStart: "▶️ Start Problem #1"
      },
      footer: {
        brandDesc: "min7014 mathedu · Interactive Step-by-Step Math Scaffolding Platform",
        collabDesc: "A new horizon in mathematics education uniting Teacher Min Eun-gi's 3,400+ visual math archives with Antigravity AI.",
        terms: "Terms of Use",
        privacy: "Privacy Policy",
        home: "min7014 Home",
        github: "GitHub Repository"
      },
      meta: {
        yearSuffix: " AY",
        qNumSuffix: "",
        gradeHigh3: "Grade 12",
        gradeHigh2: "Grade 11",
        gradeHigh1: "Grade 10",
        subjectCommon12: "Common (Math I·II)",
        subjectCalc: "Calculus",
        subjectGeom: "Geometry",
        subjectProb: "Probability & Stats",
        subjectCommon1: "Common Math"
      },
      dashboard: {
        backHome: "🏠 mathedu Home",
        refresh: "🔄 Refresh",
        anonOn: "🛡️ Privacy Shield (stu1~): ON",
        anonOff: "👤 Real Name Mode: ON",
        exportCsv: "📊 Export Results (CSV)",
        liveSync: "Live 3-sec Auto-sync",
        title: "📊 Real-Time Classroom Monitor Dashboard",
        subtitle: "Monitor student scaffolding step progress and mastery in real time"
      }
    }
  };

  var currentLang = 'ko';

  function initLanguage() {
    var urlParams = (typeof window !== 'undefined' && window.location && window.location.search) ? new URLSearchParams(window.location.search) : new URLSearchParams('');
    var langParam = urlParams.get('lang');
    if (langParam === 'en' || langParam === 'ko') {
      currentLang = langParam;
      try { localStorage.setItem(STORAGE_KEY, currentLang); } catch(e){}
    } else {
      var saved = null;
      try { saved = localStorage.getItem(STORAGE_KEY); } catch(e){}
      if (saved === 'en' || saved === 'ko') {
        currentLang = saved;
      } else {
        // default ko
        currentLang = 'ko';
      }
    }
    if (typeof document !== 'undefined' && document.documentElement) {
      document.documentElement.lang = currentLang;
    }
  }

  function getLanguage() {
    return currentLang;
  }

  function t(path, params) {
    var parts = path.split('.');
    var obj = DICTIONARY[currentLang] || DICTIONARY.ko;
    for (var i = 0; i < parts.length; i++) {
      if (obj && obj[parts[i]] !== undefined) {
        obj = obj[parts[i]];
      } else {
        // Fallback to ko
        var fb = DICTIONARY.ko;
        for (var j = 0; j < parts.length; j++) {
          if (fb && fb[parts[j]] !== undefined) fb = fb[parts[j]];
          else return path;
        }
        obj = fb;
        break;
      }
    }
    if (typeof obj === 'string' && params) {
      for (var k in params) {
        obj = obj.replace(new RegExp('\\{' + k + '\\}', 'g'), params[k]);
      }
    }
    return obj;
  }

  function setLanguage(lang) {
    if (lang !== 'ko' && lang !== 'en') return;
    currentLang = lang;
    try { localStorage.setItem(STORAGE_KEY, lang); } catch(e){}
    if (typeof document !== 'undefined' && document.documentElement) {
      document.documentElement.lang = lang;
    }
    
    // Update language switchers
    if (typeof document !== 'undefined' && document.querySelectorAll) {
      var btns = document.querySelectorAll('[data-lang-btn]');
      btns.forEach(function(b) {
        if (b.getAttribute('data-lang-btn') === lang) {
          b.classList.add('active');
        } else {
          b.classList.remove('active');
        }
      });
    }

    applyDomTranslations();

    // Call onLanguageChange callback if registered
    if (typeof window.onMatheduLanguageChange === 'function') {
      window.onMatheduLanguageChange(lang);
    }
  }

  function applyDomTranslations() {
    if (typeof document === 'undefined' || !document.querySelectorAll) return;
    // 1. Text elements: data-i18n
    var elList = document.querySelectorAll('[data-i18n]');
    elList.forEach(function(el) {
      var key = el.getAttribute('data-i18n');
      var val = t(key);
      if (typeof val === 'string') {
        el.textContent = val;
      }
    });

    // 2. HTML elements: data-i18n-html
    var elHtmlList = document.querySelectorAll('[data-i18n-html]');
    elHtmlList.forEach(function(el) {
      var key = el.getAttribute('data-i18n-html');
      var val = t(key);
      if (typeof val === 'string') {
        el.innerHTML = val;
      }
    });

    // 3. Placeholders: data-i18n-placeholder
    var elPlaceholders = document.querySelectorAll('[data-i18n-placeholder]');
    elPlaceholders.forEach(function(el) {
      var key = el.getAttribute('data-i18n-placeholder');
      var val = t(key);
      if (typeof val === 'string') {
        el.setAttribute('placeholder', val);
      }
    });

    // 4. Titles: data-i18n-title
    var elTitles = document.querySelectorAll('[data-i18n-title]');
    elTitles.forEach(function(el) {
      var key = el.getAttribute('data-i18n-title');
      var val = t(key);
      if (typeof val === 'string') {
        el.setAttribute('title', val);
      }
    });

    // 5. Typeset math if needed
    if (window.MathJax && MathJax.typesetPromise) {
      var mathStory = document.getElementById('mathStoryDrawer');
      if (mathStory) {
        MathJax.typesetPromise([mathStory]).catch(function(){});
      }
    }
  }

  // Format meta chips into natural localized language
  function formatProblemMeta(item) {
    if (currentLang === 'en') {
      var parts = [];
      if (item.examYear) parts.push(item.examYear + ' AY');
      if (item.month) {
        var mMap = {
          '11월': 'Nov CSAT',
          '9월': 'Sep Mock',
          '6월': 'Jun Mock',
          '10월': 'Oct Exam',
          '7월': 'Jul Exam',
          '4월': 'Apr Exam',
          '3월': 'Mar Exam'
        };
        parts.push(mMap[item.month] || item.month);
      }
      if (item.grade) {
        var gMap = {
          '고3': 'Grade 12',
          '고2': 'Grade 11',
          '고1': 'Grade 10'
        };
        parts.push(gMap[item.grade] || item.grade);
      }
      if (item.subject) {
        var sMap = {
          '공통(수학I·II)': 'Math I·II',
          '미적분': 'Calculus',
          '기하': 'Geometry',
          '확률과 통계': 'Prob & Stats',
          '공통수학': 'Common Math'
        };
        parts.push(sMap[item.subject] || item.subject);
      }
      if (item.qNum) {
        parts.push('#' + item.qNum);
      }
      return parts.join(' ');
    } else {
      var partsKo = [
        item.examYear ? item.examYear + '학년도' : '',
        item.month || '',
        item.grade || '',
        item.subject || '',
        item.qNum ? item.qNum + '번' : ''
      ].filter(Boolean);
      return partsKo.join(' ');
    }
  }

  // Initialize immediately
  initLanguage();

  // Export to window
  window.MatheduI18n = {
    getLanguage: getLanguage,
    setLanguage: setLanguage,
    t: t,
    applyDomTranslations: applyDomTranslations,
    formatProblemMeta: formatProblemMeta
  };

  // Run on DOMContentLoaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      applyDomTranslations();
    });
  } else {
    setTimeout(applyDomTranslations, 0);
  }

})(window);
