/**
 * mathedu-i18n.js
 * mathedu · Universal Global Internationalization (i18n) Engine (v2026.11.15)
 * Full-coverage reversible Korean (ko) ⇄ English (en) localization across all pages,
 * dynamic quiz lists, 1,113+ MIN EUN GI's Math Archive items, modals, and interactive labs.
 */
(function(window) {
  'use strict';

  var STORAGE_KEY = 'mathedu_lang';
  var STORAGE_MANUAL_KEY = 'mathedu_lang_manual';
  var VB_STORAGE_KEY = 'mathedu_vb_lang';

  var DICTIONARY = {
    ko: {
      nav: {
        allQuizzes: "📚 퀴즈 모음",
        offlineVault: "📦 오프라인 보관함",
        offlineVaultTitle: "인터넷 없이 풀 수 있는 오프라인 전체 문제 보관함",
        minExplorer: "🌐 동적 기하 탐색관",
        myBadges: "🏆 나의 업적",
        createQuiz: "✨ 문제 출제",
        membersOnly: "회원전용",
        dashboard: "📊 수업 대시보드",
        minHome: "🌐 자료실 홈"
      },
      hero: {
        badgePill: "3,400+ 시각적 수학 증명",
        mainTitleLab: "수학자료실",
        mainTitleHub: "mathedu",
        leadDesc: "3,400+ 시각적 기하 증명과 단델린 구의 통찰을 담은 <b>가입 없는 100% 영구 무료 인터랙티브 수학자료실</b>",
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
        storyDrawerAuthor: "수학의 본질과 직관을 밝히는 수학교육의 지향점입니다.",
        statTopics: "🏛️ 수학 주제",
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
        tag: "💡 오늘의 추천 동적 기하 (수학자료실)",
        btnNext: "다른 추천",
        btnApplet: "🎮 GeoGebra로 조작하기 ➔",
        btnPdf: "📄 원리 증명 PDF",
        btnWeb: "🌐 웹 상세 해설"
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
        title: "디딤돌 수학 문제 목록",
        subtitle: "(학년도 · 학년 · 시행월 · 선택과목 · 번호 선택 시 해당 문제만 즉시 추출)",
        resetBtn: "🔄 필터 전체 초기화",
        policyTitle: "공개 원칙:",
        policyText: "본 게시판은 저작권이 투명한 <b>대학수학능력시험(대수능) 및 한국교육과정평가원·시도교육청 모의평가(전국연합학력평가) 기출문제만 선별 공개</b>합니다.",
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
        searchPlaceholder: "문제 검색 (예: 9월 고3 확통, 10월 미적분 30번, 정규분포, 삼각함수...)",
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
        brandDesc: "mathedu · 단계별 인터랙티브 수학교육 플랫폼",
        collabDesc: "3,400+ 수학자료실과 안티그래비티 AI가 함께 만드는 수학교육의 새 지평",
        terms: "이용약관",
        privacy: "개인정보처리방침",
        home: "수학자료실 홈",
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
      auth: {
        mySolved: "📂 내가 푼 문제",
        myLibrary: "📂 서재({cnt})",
        solvedCount: "📂 푼 문제 ({cnt})",
        googleLogin: "Google 로그인",
        googleUpgrade: "✨ Google 전환",
        logout: "로그아웃",
        guestSuffix: "님"
      },
      dashboard: {
        backHome: "← 메인 홈",
        refresh: "새로고침",
        anonOn: "🔒 학생 익명 보호 (칠판 모드)",
        anonOff: "👀 실명 모드로 복귀 (내 수업)",
        exportCsv: "성적표 저장(CSV)",
        liveSync: "3초 실시간 갱신 중",
        title: "실시간 수업 모니터링 대시보드",
        subtitle: "학생들의 실시간 퀴즈 풀이 진행 현황 및 성취도 관제",
        toolsLabel: "수업 배포 도구:",
        btnProjector: "🖥️ 칠판 빔프로젝터 QR 띄우기",
        btnCopyStudentLink: "📋 학생 참여 링크 복사",
        btnCopied: "✅ 복사 완료!",
        btnActionProjectorAnon: "🖥️ 칠판 프로젝터 모드 (stu1~ 전환)",
        btnActionProjectorReal: "👀 실명 모드로 복귀",
        btnViewAllClasses: "🌐 전체 수업 모아보기",
        statTotal: "👥 총 참여 학생",
        statCompleted: "🏆 완주 학생 (완주율)",
        statAvgScore: "📈 반 평균 정답률",
        statActiveNow: "🟢 현재 풀이 중 (최근 활동)",
        unitStudents: "명",
        shieldActiveTitle: "🔒 학생 개인정보 보호 모드 가동",
        shieldActiveBadge: "stu1, stu2... 자동 순차 부여",
        shieldActiveDesc: "실시간 화면 공유 및 칠판 빔프로젝터 환경에서 실제 학생 이름이 노출되지 않도록 참여 순서대로 <b>stu1, stu2, stu3...</b> 가 자동 부여되어 표시됩니다. (정식회원이 로그인하여 개설한 자기 수업에서만 실명 확인 및 익명 보호 전환이 가능합니다)",
        teacherModeTitle: "👑 회원 전용 자기수업 관제 모드",
        teacherModeBadge: "실제 학생 이름 표시 중",
        teacherModeDesc: "선생님께서 직접 개설하신 수업(<b>{room}</b>)이므로 학생들의 <b>실제 이름</b>이 표시됩니다. 교실 빔프로젝터나 화면 공유 시에는 상단의 <b>[🔒 학생 익명 보호 (칠판 모드)]</b>를 누르면 즉시 <code>stu1, stu2...</code> 로 익명 전환됩니다.",
        projectorModeTitle: "🖥️ 칠판 빔프로젝터 모드 가동 중",
        projectorModeBadge: "전체 학생 stu1, stu2... 익명 송출",
        projectorModeDesc: "현재 교실 빔프로젝터 화면에 맞춰 학생들의 이름이 <b>익명 식별자(stu1~)</b>로 송출되고 있습니다. 실명으로 다시 확인하시려면 상단 <b>[👀 실명 모드로 복귀]</b> 버튼을 누르세요.",
        teacherWarnMsg: "👑 <b>[{room}]</b> 교사 실명 관제 모드입니다. 칠판/빔프로젝터 화면 송출 시 아래 버튼으로 익명 전환하세요.",
        btnSwitchProjAnon: "🖥️ 칠판 프로젝터 익명(stu1~) 전환",
        classCodeLabel: "🏫 수업 코드: ",
        myClassBadge: "👑 내가 개설한 수업 (실명 표시 중)",
        titleAll: "전체 학습 현황 모니터링",
        subAll: "개설된 모든 수업 및 자율 학습 학생들의 실황입니다.",
        titleRoom: "[{room}] 실시간 수업 관제 센터",
        tagMyClass: "(내 수업)",
        subMyRoom: "선생님께서 개설하신 '{room}' 수업입니다. 학생들의 실명과 진도가 실시간 집계됩니다.",
        subOtherRoom: "현재 '{room}' 수업에 참여 중인 학생들의 학습 실황입니다.",
        allRooms: "모든 수업 (전체 보기)",
        allQuizzes: "모든 퀴즈",
        roomOptionSuffix: " 수업",
        searchPlaceholder: "학생 ID (stu1, stu2...) 또는 이름 검색...",
        tabCard: "📇 카드 뷰",
        tabTable: "📋 테이블 뷰",
        loadingText: "실시간 데이터를 불러오는 중...",
        emptyTitle: "아직 풀이를 시작한 학생이 없습니다.",
        emptyDesc: "학생들에게 링크나 QR 코드를 공유하면 이곳에 실시간으로 나타납니다.",
        thStudentReal: "학생 실명 (식별 ID)",
        thStudentAnon: "학생 ID (익명 stu)",
        thRoom: "수업(방)",
        thQuiz: "퀴즈",
        thStep: "진행 단계",
        thCorrect: "맞힌 문항",
        thAccuracy: "정답률",
        thStatus: "상태",
        thLastActive: "마지막 활동",
        badgeMyStudent: "👑 내 학생",
        statusDone: "🎉 풀이 완료",
        statusSolving: "🟢 풀이 중",
        statusWait: "⏳ 대기",
        stepLabel: "진도: ",
        stepUnit: "단계",
        scoreLabel: "점수: ",
        activeLabel: "활동: ",
        selfStudy: "자율학습",
        correctCount: "{n}개 정답",
        statusCompletedText: "완료",
        statusInProgressText: "진행중",
        timeJustNow: "방금 전",
        timeSecAgo: "{n}초 전",
        timeMinAgo: "{n}분 전",
        timeHourAgo: "{n}시간 전",
        timeDayAgo: "{n}일 전",
        modalClose: "✕ 칠판 뷰 닫기",
        modalScanQr: "스마트폰 카메라로 QR 코드를 스캔하세요!",
        modalInstantJoin: "회원가입 없이 즉시 참여할 수 있습니다.",
        alertNoData: "내보낼 데이터가 없습니다.",
        pageTitle: "실시간 수업 대시보드 · mathedu (수학자료실)",
        teacherWarnMsgGeneral: "⚠️ 현재 교사 전용 실명 확인 모드입니다. 빔프로젝터 송출 시 학생 실제 이름이 노출될 수 있습니다!",
        authDeployPrompt: "수업 배포",
        anonymous: "익명"
      },
      report: {
        fabTitle: "오류신고",
        fabTooltip: "오류 신고 (화면 요소를 클릭하여 신고)",
        bannerPrompt: "오류가 있는 화면 요소(문제, 보기, 수식, 그림 등)를 클릭해 주세요.",
        bannerCancel: "✕ 취소 (ESC)",
        bannerWhole: "📄 화면 전체 오류 신고",
        modalTitle: "오류 신고",
        targetTitle: "선택된 영역",
        targetWholePage: "화면 전체 (특정 영역 미지정)",
        reselectBtn: "다시 선택",
        categoryTitle: "오류 유형",
        catMath: "🧮 수식 / 계산 오류",
        catTypo: "✍️ 오타 / 표기 오류",
        catAnswer: "🎯 정답 / 채점 이상",
        catGraphic: "🖼️ 그림 / 그래픽 깨짐",
        catBug: "⚙️ 화면 / 기능 이상",
        catOther: "💡 기타 개선 제안",
        descTitle: "오류 내용",
        descPlaceholder: "어떤 부분이 어떻게 이상한가요? 자세히 적어주시면 신속하게 검토 후 반영하겠습니다.",
        reporterTitle: "신고자 이름 / 닉네임",
        emailTitle: "알림 받을 이메일 (선택사항)",
        emailPlaceholder: "수정 완료 시 알림을 받으실 이메일 주소",
        cancelBtn: "취소",
        submitBtn: "신고 접수",
        submitting: "신고 접수 중...",
        successToast: "✅ 오류 신고가 정상 접수되었습니다. 확인 후 신속하게 반영하겠습니다!",
        errNoDesc: "오류 내용을 입력해 주세요."
      }
    },
    en: {
      nav: {
        allQuizzes: "📚 All Quizzes",
        offlineVault: "📦 Offline Archive",
        offlineVaultTitle: "Download standalone quizzes that run without internet",
        minExplorer: "🌐 Geometry Lab",
        myBadges: "🏆 My Badges",
        createQuiz: "✨ Create Quiz",
        membersOnly: "Members",
        dashboard: "📊 Classroom Dashboard",
        minHome: "🌐 Archive Home"
      },
      hero: {
        badgePill: "3,400+ Visual Math Proofs",
        mainTitleLab: "Math Archive",
        mainTitleHub: "mathedu",
        leadDesc: "MIN EUN GI's Math Archive: Over 3,400 Dynamic Visual Proofs & Scaffolding Quizzes, <b>100% Freely Open</b>",
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
        storyDrawerAuthor: "The pedagogical philosophy of mathematical insight.",
        statTopics: "🏛️ Math Topics",
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
        tag: "💡 Today's Featured Dynamic Geometry (Math Archive)",
        btnNext: "Next Pick",
        btnApplet: "🎮 Explore in GeoGebra ➔",
        btnPdf: "📄 Visual Proof PDF",
        btnWeb: "🌐 Web Details"
      },
      heroCards: {
        teacherTag: "👩‍🏫 For Teachers · Instant Classroom Distribution",
        teacherTitle: "Launch a Classroom in 3 Seconds",
        teacherDesc: "Instantly generate a unique classroom session code, projector QR code, and student link without student accounts.",
        teacherBtn: "🚀 3-Sec Launch (QR)",
        createTag: "🤖 AI Scaffolding · National Math Exams",
        createTitle: "✨ Create Exam Stepping-Stone Quiz",
        createDesc: "Upload an official exam question, and Antigravity AI automatically structures it into a <b>5~8 step interactive scaffolding quiz</b> with GeoGebra visual proofs.",
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
        title: "Stepping-Stone Math Problem Explorer",
        subtitle: "(Filter instantly by Exam Year, Grade, Month, Subject & Question #)",
        resetBtn: "🔄 Reset All Filters",
        policyTitle: "Public Policy:",
        policyText: "This repository features public national college entrance and official mock examination questions transformed into pedagogical step-by-step visual scaffolding ladders.",
        labelYear: "📅 Exam Year",
        allYears: "All Exam Years",
        yearOption: "Academic Year {year}",
        yearBefore2020: "Before Year 2020",
        labelGrade: "🎓 Grade Level",
        allGrades: "All Grades",
        gradeHigh3: "Grade 12 (Senior)",
        gradeHigh2: "Grade 11",
        gradeHigh1: "Grade 10",
        labelMonth: "🗓️ Exam Month / Name",
        allMonths: "All Exam Months",
        month11: "Nov College Entrance Exam",
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
        searchPlaceholder: "Search problems (e.g. Sep G12 Prob & Stats, Calculus #30, normal distribution, parabola, vector...)",
        topicPrefix: "Topics:",
        topicAll: "All Topics",
        topicQuad: "Quadratic & Conics",
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
        emptyFilterDesc: "Request this specific exam question now, and Antigravity AI will automatically craft a 5~8 step interactive scaffolding quiz with GeoGebra visual proofs.",
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
        brandDesc: "mathedu · Interactive Step-by-Step Math Scaffolding Platform",
        collabDesc: "A new horizon in mathematics education uniting 3,400+ visual math archives with Antigravity AI.",
        terms: "Terms of Use",
        privacy: "Privacy Policy",
        home: "Archive Home",
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
      auth: {
        mySolved: "📂 My Solved",
        myLibrary: "📂 Library ({cnt})",
        solvedCount: "📂 Solved ({cnt})",
        googleLogin: "Google Sign In",
        googleUpgrade: "✨ Upgrade",
        logout: "Sign Out",
        guestSuffix: ""
      },
      dashboard: {
        backHome: "← Main Home",
        refresh: "Refresh",
        anonOn: "🔒 Privacy Shield (Projector Mode)",
        anonOff: "👀 Return to Real Names (My Class)",
        exportCsv: "Export Results (CSV)",
        liveSync: "3s Live Auto-Sync",
        title: "Real-Time Classroom Monitor Dashboard",
        subtitle: "Monitor student scaffolding quiz progress and mastery in real time",
        toolsLabel: "Class Tools:",
        btnProjector: "🖥️ Projector Screen & QR",
        btnCopyStudentLink: "📋 Copy Student Join Link",
        btnCopied: "✅ Copied!",
        btnActionProjectorAnon: "🖥️ Projector Mode (stu1~)",
        btnActionProjectorReal: "👀 Return to Real Names",
        btnViewAllClasses: "🌐 View All Classes",
        statTotal: "👥 Total Students",
        statCompleted: "🏆 Completed (Rate)",
        statAvgScore: "📈 Class Average Accuracy",
        statActiveNow: "🟢 Currently Solving (Active)",
        unitStudents: " students",
        shieldActiveTitle: "🔒 Student Privacy Shield Active",
        shieldActiveBadge: "stu1, stu2... Pseudonyms",
        shieldActiveDesc: "To prevent student identity exposure on shared classroom displays, pseudonyms <b>stu1, stu2, stu3...</b> are automatically assigned in join order.",
        teacherModeTitle: "👑 Teacher Classroom Command Mode",
        teacherModeBadge: "Displaying Real Student Names",
        teacherModeDesc: "As the creator of class (<b>{room}</b>), real student names are displayed. For classroom projection, click <b>[🔒 Privacy Shield]</b> above to anonymize names to <code>stu1, stu2...</code>.",
        projectorModeTitle: "🖥️ Classroom Projector Mode Active",
        projectorModeBadge: "All Students stu1, stu2... Anonymized",
        projectorModeDesc: "Student names are displayed as anonymous identifiers (stu1~) for classroom projection. Click <b>[👀 Return to Real Names]</b> above to restore.",
        teacherWarnMsg: "👑 <b>[{room}]</b> Teacher Real Name Mode. Switch to anonymity below before projecting screen.",
        btnSwitchProjAnon: "🖥️ Switch to Projector Privacy (stu1~)",
        classCodeLabel: "🏫 Class Code: ",
        myClassBadge: "👑 My Created Class (Showing Real Names)",
        titleAll: "Live Classroom Monitoring",
        subAll: "Real-time activity across all active classes and independent learners.",
        titleRoom: "[{room}] Live Class Command Center",
        tagMyClass: "(My Class)",
        subMyRoom: "Class '{room}' created by you. Real names and progress are monitored in real time.",
        subOtherRoom: "Real-time learning activity for students participating in '{room}'.",
        allRooms: "All Classes (Show All)",
        allQuizzes: "All Quizzes",
        roomOptionSuffix: " Class",
        searchPlaceholder: "Search by student ID (stu1...) or name...",
        tabCard: "📇 Card View",
        tabTable: "📋 Table View",
        loadingText: "Loading real-time classroom data...",
        emptyTitle: "No student activity yet.",
        emptyDesc: "Share the join link or QR code with your students to see real-time progress here.",
        thStudentReal: "Student Real Name (ID)",
        thStudentAnon: "Student ID (Anonymous stu)",
        thRoom: "Class Room",
        thQuiz: "Quiz",
        thStep: "Progress Step",
        thCorrect: "Correct Answers",
        thAccuracy: "Accuracy",
        thStatus: "Status",
        thLastActive: "Last Active",
        badgeMyStudent: "👑 My Student",
        statusDone: "🎉 Completed",
        statusSolving: "🟢 Solving",
        statusWait: "⏳ Idle",
        stepLabel: "Step: ",
        stepUnit: "",
        scoreLabel: "Score: ",
        activeLabel: "Active: ",
        selfStudy: "Self-Study",
        correctCount: "{n} correct",
        statusCompletedText: "Completed",
        statusInProgressText: "In Progress",
        timeJustNow: "Just now",
        timeSecAgo: "{n}s ago",
        timeMinAgo: "{n}m ago",
        timeHourAgo: "{n}h ago",
        timeDayAgo: "{n}d ago",
        modalClose: "✕ Close Projector View",
        modalScanQr: "Scan QR Code with Smartphone Camera!",
        modalInstantJoin: "Join instantly without signup or login.",
        alertNoData: "No data to export.",
        pageTitle: "Live Classroom Dashboard · mathedu",
        teacherWarnMsgGeneral: "⚠️ Teacher Real Name Mode is active. Projecting this screen may expose student identities!",
        authDeployPrompt: "Classroom Distribution",
        anonymous: "Anonymous"
      },
      report: {
        fabTitle: "Report Issue",
        fabTooltip: "Report Issue (Click an element to report)",
        bannerPrompt: "Click on the problematic part of the screen (question, option, formula, graphic, etc.).",
        bannerCancel: "✕ Cancel (ESC)",
        bannerWhole: "📄 Report Whole Page",
        modalTitle: "Report an Issue",
        targetTitle: "Selected Target",
        targetWholePage: "Whole Page (No specific element)",
        reselectBtn: "Reselect",
        categoryTitle: "Issue Category",
        catMath: "🧮 Math / Calculation Error",
        catTypo: "✍️ Typo / Notation Error",
        catAnswer: "🎯 Answer / Grading Issue",
        catGraphic: "🖼️ Image / Graphic Issue",
        catBug: "⚙️ Layout / Feature Bug",
        catOther: "💡 Other Suggestion",
        descTitle: "Description",
        descPlaceholder: "Please describe what is incorrect or needs improvement in detail.",
        reporterTitle: "Your Name / Nickname",
        emailTitle: "Notification Email (Optional)",
        emailPlaceholder: "Email to receive update notification when fixed",
        cancelBtn: "Cancel",
        submitBtn: "Submit Report",
        submitting: "Submitting...",
        successToast: "✅ Issue report submitted! We will review and fix it promptly.",
        errNoDesc: "Please provide a description of the issue."
      }
    }
  };

  // ══════════════════════════════════════════════════════════════════════════
  // Tier 1: Exact Idiomatic UI Phrase Map (Korean -> Natural English)
  // Covers all static & dynamic UI elements across index.html, video_board.html,
  // mathlab.html, mathedu-room.js, create.html, dashboard.html, game.html,
  // video_studio.html, board/*.html, and offline/index.html.
  // ══════════════════════════════════════════════════════════════════════════
  var EXACT_UI_MAP = {
    // Top Header & Navigation
    "mathedu · 수학자료실": "mathedu · MIN EUN GI's Math Archive",
    "3,400+ 시각적 수학 증명": "3,400+ Visual Math Proofs",
    "다크": "Dark",
    "라이트": "Light",
    "다크/라이트 테마 전환": "Toggle Dark/Light Theme",
    "다크/라이트 테마 전환 (Toggle Dark/Light Theme)": "Toggle Dark/Light Theme",
    "언어 설정 변경": "Switch Language (KO / EN)",
    "연속 학습 스트릭 및 나의 뱃지": "Daily Learning Streak & My Badges",
    "로그인 및 내 서재": "Sign In & My Library",
    "홈": "Home",
    "디딤돌 퀴즈": "Stepping Quizzes",
    "동적 기하관": "Geometry Lab",
    "교사용 출제": "Create Quiz",
    "마이룸": "My Room",

    // Compact Link Hub (Main Directory)
    "수학자료실 · 바로가기 링크": "Math Archive · Quick Directory",
    "디딤돌 문항": "Stepping-Stone Problems ",
    "· 시각적 증명 3,400+": " · 3,400+ Visual Proofs",
    "📋 전체 자료 설명 영상 게시판 (@min7014_ai)": "📋 Visual Proof Video Board (@min7014_ai)",
    "게시판 ➔": "Board ➔",
    "🛠️ 자체 제작 수학공학도구 MathLab v1.4 (AI Lab)": "🛠️ Proprietary Math Engineering Lab · MathLab v1.4",
    "실습 ➔": "Launch ➔",
    "🎬 다국어 PDF 강의 영상 스튜디오": "🎬 Multilingual PDF Lecture Studio",
    "🎮 수학의 성전 3D (퀘스트 게임)": "🎮 Sanctuary of Math 3D (Quest RPG)",
    "📐 3,400+ 동적 기하·증명 검색": "📐 Search 3,400+ Dynamic Proofs",
    "열기 ➔": "Open ➔",
    "🌐 민은기 선생님의 수학자료실 본관": "🌐 MIN EUN GI's Math Archive (Main Site)",
    "✨ 교사용 문제 출제 스튜디오": "✨ Teacher Quiz Creation Studio",
    "📊 실시간 교실 현황 대시보드": "📊 Live Classroom Dashboard",
    "📦 오프라인 단독 퀴즈 보관함": "📦 Standalone Offline Quiz Vault",
    "이동 ➔": "Go ➔",

    // YouTube × mathedu Cinema & PR Hub
    "📺 YouTube × mathedu 홍보·확장 허브": "📺 YouTube × mathedu Visual Cinema Hub",
    "@min7014_ai 1080p 시각적 수학 증명 시네마 & 45초 #Shorts 즉시 재생": "@min7014_ai 1080p Visual Math Proof Cinema & 45s #Shorts Instant Theater",
    "🎓 교실 칠판 QR & 3분 대표작 구독 마중물 ▼": "🎓 Classroom Projector QR & 3-Min Featured Proof ▼",
    "🎬 인라인 유튜브 극장 열기 ▼": "🎬 Open Inline YouTube Theater ▼",
    "🎬 인라인 유튜브 극장 닫기 ▲": "🎬 Close Inline YouTube Theater ▲",
    "📣 홍보 에이전트(PR) 7대 채널 스튜디오 ▼": "📣 PR Growth Studio (7 Channels) ▼",
    "📣 홍보 에이전트(PR) 7대 채널 스튜디오 닫기 ▲": "📣 Close PR Growth Studio ▲",
    "📢 학급·SNS 홍보 카드 1초 복사": "📢 Copy Class & Social Share Kit",
    "🚨 NEW 실전함정 5초 해체(4분 본편) ↗": "🚨 NEW 5-Sec Exam Trap Breakdown (4m) ↗",
    "🔥 NEW 원주각 x=? 3초 챌린지 #Shorts ↗": "🔥 NEW Inscribed Angle x=? 3s #Shorts ↗",
    "⚡ 인기 1위(602뷰) 이등변 Q-#Shorts ↗": "⚡ #1 Popular Isosceles Q-#Shorts ↗",
    "🎬 3분 핵심 시각 증명 본편 ↗": "🎬 3-Min Core Visual Proof ↗",
    "📐 6분 도형 핵심 증명 직강 ↗": "📐 6-Min Geometry Proof Lecture ↗",
    "🛠️ 자체 제작 MathLab v1.4 ↗": "🛠️ MathLab v1.4 Interactive Lab ↗",
    "🔔 @min7014_ai 1초 무료 구독 ↗": "🔔 Subscribe Free to @min7014_ai ↗",
    "🌳 1. 피타고라스 나무 넓이 보존": "🌳 1. Pythagoras Tree Area Invariance",
    "🔥 2. 피타고라스 정리 25단계 증명": "🔥 2. Pythagorean Theorem (25-Step Proof)",
    "📐 3. 체바의 정리 넓이 비 증명": "📐 3. Ceva's Theorem (Area Ratio Proof)",
    "✨ 4. 메넬라우스 평행보조선 증명": "✨ 4. Menelaus' Theorem (Parallel Line)",
    "🌟 5. 정칠각형 종이띠 매듭 원리": "🌟 5. Regular Heptagon Paper Knot",
    "🪐 6. 타원 빛 반사 123프레임": "🪐 6. Ellipse Optical Reflection (123f)",
    "🔺 7. 비비아니 정리 정삼각형": "🔺 7. Viviani's Theorem (Equilateral)",
    "📋 1,113개 전체 영상·숏폼 게시판 ➔": "📋 All 1,113 Video & Shorts Lectures ➔",
    "📱 5대 #Shorts 45초 극장": "📱 Featured 45s #Shorts",
    "📱 #Shorts 1: 피타고라스 나무 (35초)": "📱 #Shorts 1: Pythagoras Tree (35s)",
    "📱 #Shorts 2: 피타고라스 넓이분할 (33초)": "📱 #Shorts 2: Pythagorean Area Split (33s)",
    "📱 #Shorts 3: 체바의 정리 넓이비 (35초)": "📱 #Shorts 3: Ceva's Area Ratio (35s)",
    "📱 #Shorts 4: 메넬라우스 보조선 (41초)": "📱 #Shorts 4: Menelaus Auxiliary Line (41s)",
    "📱 #Shorts 5: 정칠각형 종이매듭 (44초)": "📱 #Shorts 5: Heptagon Paper Knot (44s)",
    "🎬 @min7014_ai v4.0 Viral Cinema (1080p 본편 & 9:16 #Shorts)": "🎬 @min7014_ai v4.0 Visual Proof Cinema (1080p Full & 9:16 #Shorts)",
    "🇰🇷 1080p 본편 (KO)": "🇰🇷 1080p Full (KO)",
    "📱 45초 #Shorts (KO)": "📱 45s #Shorts (KO)",
    "✕ 닫기": "✕ Close",
    "닫기 ✕": "Close ✕",
    "🚀 영상 시청 후 3단계 실력 완성 퍼널": "🚀 3-Step Mastery Path After Watching",
    "📐 1단계: 이 도형 GeoGebra로 직접 조작하기 ➔": "📐 Step 1: Manipulate This Figure in GeoGebra ➔",
    "✍️ 2단계: 탈-5지선다 관련 기출 바로 풀기 ➔": "✍️ Step 2: Solve Related Constructive Quiz ➔",
    "📢 3단계: 이 영상+문제 세트 단톡방 공유하기": "📢 Step 3: Copy & Share This Video + Quiz Set",
    "📺 공식 채널: @min7014_ai": "📺 Official Channel: @min7014_ai",
    "🔔 유튜브 구독하기 ↗": "🔔 Subscribe on YouTube ↗",
    "📣 PR Agent v2.0 가동 중": "📣 PR Growth Studio v2.0",
    "유튜브(@min7014_ai) × 수학홈페이지(mathedu) 7대 채널 맞춤형 홍보 생성 스튜디오": "YouTube (@min7014_ai) × mathedu 7-Channel Share Kit Generator",
    "✕ 스튜디오 닫기": "✕ Close Studio",
    "🎯 1. 홍보할 영상·주제 선택:": "🎯 1. Choose Topic:",
    "📺 유튜브 고정댓글·커뮤니티": "📺 YouTube Pinned & Community",
    "💬 카톡·단톡방 1초 도전장": "💬 Messenger Challenge Card",
    "🔥 수만휘·오르비 수험생 추천글": "🔥 Student Study Forum Post",
    "🏫 인디스쿨·교사 나눔 키트": "🏫 Teacher Lesson Sharing Kit",
    "📸 인스타·블로그 #공스타그램": "📸 Instagram & Study Blog",
    "👨‍👩‍👧 학부모·교육카페 안내문": "👨‍👩‍👧 Parent & Education Guide",
    "💡 채널에 맞게 자동 최적화된 홍보 문구와 5대 홈페이지 직행 딥링크가 포함되어 있습니다.": "💡 Includes channel-tailored copy and 5 direct deep links to visual proofs & constructive quizzes.",
    "📋 이 채널 맞춤 홍보문구 1초 복사 (+30 XP)": "📋 Copy Custom Share Text (+30 XP)",
    "📲 모바일 공유 시트 열기": "📲 Open Native Share Sheet",
    "🖼️ 자동 생성된 SNS·오픈그래프 홍보 카드 (1200×630)": "🖼️ Auto-Generated Social Share Banner (1200×630)",
    "⬇ 고해상도 홍보 배너 PNG 다운로드": "⬇ Download High-Res Banner PNG",
    "• 블로그·카페·인스타·단톡방에 위 문구와 함께 이 이미지를 첨부하면 클릭률(CTR)이 2배 이상 높아집니다.": "• Attach this 1200×630 visual banner alongside the text above when sharing with students or colleagues.",

    // Secondary External Links & Classroom Code
    "🔗 전 단원 개념 증명 PDF": "🔗 All Concept Proof PDFs",
    "🎓 수학교육학 5대 원리 학습법": "🎓 5 Research-Backed Math Principles",
    "🧬 오개념 클리닉 & 유레카 노트": "🧬 Misconception Clinic & Eureka Notes",
    "🔗 3초 수업 QR 개설": "🔗 3-Sec Class QR Launch",
    "📂 내 풀이 기록": "📂 My Solved History",
    "수업 코드 입력": "Class Code",
    "입장": "Join",

    // MIN EUN GI's Math Archive Deep Curriculum Section
    "min7014.github.io 심층 연동": "min7014.github.io Deep Sync",
    "🏛️ 민은기 선생님의 수학자료실 16대 영역 · 165개 세부 단원 시각적 증명 아카이브": "🏛️ MIN EUN GI's Math Archive · 16 Domains & 165 Units Visual Proof Library",
    "📚 1,113개 심층 주제": "📚 1,113 In-Depth Topics",
    "📄 증명 PDF 847": "📄 847 Proof PDFs",
    "🎮 GeoGebra 404": "🎮 404 GeoGebra Labs",
    "📐 AlgeoMath 457": "📐 457 AlgeoMath Labs",
    "📏 작도 60선": "📏 60 Compass Constructions",
    "🎥 영상·숏폼 927": "🎥 927 Videos & Shorts",
    "📐 오늘의 동적 기하 · 시각적 증명": "📐 Today's Dynamic Geometry & Visual Proof",
    "◀ 이전": "◀ Prev",
    "다음 ▶": "Next ▶",
    "🔊 도슨트": "🔊 Voice Guide",
    "🎮 인라인 실험실 열기": "🎮 Open Inline Lab",
    "📄 인라인 플립북 PDF": "📄 Inline Flipbook PDF",
    "PDF 새창 ↗": "Open PDF ↗",
    "▶️ 해설 영상 ↗": "▶️ Video Lecture ↗",
    "원문 ↗": "Original ↗",
    "🎮 실시간 동적 기하 · 시각적 증명 실험실": "🎮 Live Interactive Dynamic Geometry & Visual Proof Lab",
    "✕ 실험실 닫기": "✕ Close Lab",
    "🧭 수학자료실 16대 영역 원클릭 심층 탐색 (클릭 시 단원별 원리·보조선·초등 4단계 디딤돌 즉시 열람):": "🧭 Explore All 16 Domains of MIN EUN GI's Math Archive (Click any domain for visual proofs, auxiliary lines & 4-step scaffolding):",
    "전체 1,113개 주제 탐색관 열기 ➔": "Open All 1,113 Topics Explorer ➔",
    "📐 유클리드 평면기하 (189)": "📐 Euclidean Plane Geometry (189)",
    "🔢 다항식·방정식·수체계 (178)": "🔢 Polynomials & Number Systems (178)",
    "📈 미분·도함수 (101)": "📈 Differentiation & Derivatives (101)",
    "🪐 이차곡선·단델린 (85)": "🪐 Conic Sections & Dandelin (85)",
    "🧭 벡터·공간도형 (80)": "🧭 Vectors & Solid Geometry (80)",
    "🌱 지수·로그 (70)": "🌱 Exponents & Logarithms (70)",
    "🎯 극한과 연속 (69)": "🎯 Limits & Continuity (69)",
    "⭕ 해석기하·원 (61)": "⭕ Analytic Geometry & Circles (61)",
    "🌊 삼각비·삼각함수 (54)": "🌊 Trigonometry (54)",
    "🔗 함수·집합·그래프 (49)": "🔗 Functions, Sets & Graphs (49)",
    "🪞 기하 변환·대칭 (36)": "🪞 Geometric Transformations (36)",
    "🎲 확률과 통계 (35)": "🎲 Probability & Statistics (35)",
    "⚖️ 방정식·부등식 (32)": "⚖️ Equations & Inequalities (32)",
    "⏳ 적분·구분구적법 (32)": "⏳ Integration & Quadrature (32)",
    "🪜 수열·시그마 (22)": "🪜 Sequences & Series (22)",
    "🌐 수학자료실 본관 직통 허브:": "🌐 Direct Links to MIN EUN GI's Math Archive:",
    "📑 내용순 배열(전 단원 트리) ↗": "📑 Curriculum Topic Tree ↗",
    "🗓️ 만든순서별 아카이브 ↗": "🗓️ Chronological Archive ↗",
    "📏 눈금 없는 자와 컴퍼스 작도 ↗": "📏 Straightedge & Compass Constructions ↗",
    "🏫 학년도별 수학수업(2015~2023) ↗": "🏫 Classroom Archives (2015–2023) ↗",
    "🏫 2024학년도 수학수업 ↗": "🏫 2024 Math Classes ↗",
    "🎙️ 특강·강의 자료 ↗": "🎙️ Special Lectures & Notes ↗",
    "🧪 기타자료·Python Colab ↗": "🧪 Python Colab & Math Labs ↗",

    // MathTeacher 5-Innovation Pedagogy Studio
    "수학교사 에이전트(mathteacher) 수학교육 발전 5대 혁신 스튜디오 (탈-5지선다 창의 구성 통합)": "Math Teacher (mathteacher) 5-Pillar Pedagogy Studio (De-Multiple-Choice Constructive Solving)",
    "Freudenthal · Pólya · Lakatos · Brown & Walter (탈-5지선다)": "Freudenthal · Pólya · Lakatos · Brown & Walter (Constructive Math)",
    "초등 기초 직관부터 중등 기하·대수 시각 증명(`min7014.github.io`), 고등 수능 100점 킬러까지 단절 없는 학습 사다리를 제공합니다.": "A seamless learning ladder from elementary intuition and visual proofs (`min7014.github.io`) to advanced college entrance mastery.",
    "🏛️ 수학교육 철학 & 왜 수학을 배울까? ➔": "🏛️ Philosophy & Why Learn Math? ➔",
    "❓ 질문하는 수학 수업 스튜디오 ➔": "❓ Question-Asking Math Studio ➔",
    "🎓 전체 수학교육 발전 스튜디오 열기 ➔": "🎓 Open Full Pedagogy Studio ➔",
    "🌳 1. 초·중·고 수직 계통성 트리": "🌳 1. K-12 Vertical Concept Genealogy",
    "1065대 계보": "1,065 Chains",
    "고등 수학에서 막히는 진짜 이유인 초·중등 뿌리 개념(비율➔기울기➔미분, 모눈➔구분구적➔적분)을 한눈에 복원합니다.": "Reconnects elementary & middle-school roots (Ratio ➔ Slope ➔ Derivative; Grid ➔ Quadrature ➔ Integral) behind advanced math.",
    "계보 트리 & 기출 연동 열기 ➔": "Open Concept Tree & Quizzes ➔",
    "🧭 2. 폴리아 조건➔보조선 사전": "🧭 2. Pólya Condition ➔ Auxiliary Line",
    "1069대 법칙": "1,069 Rules",
    "\"무슨 보조선을 그어야 할까?\" 원의 접선·지름·이차곡선·절댓값 미분가능·정적분 함수 등 12대 단골 조건을 1초 만에 번역합니다.": "\"Which auxiliary line should I draw first?\" Instant geometric & algebraic translations for circles, conics, differentiability, and integrals.",
    "1초 보조선 번역 사전 열기 ➔": "Open Auxiliary Line Dictionary ➔",
    "🔬 3. 오개념 백신 & 반례 실험실": "🔬 3. Lakatos Misconception & Counterexamples",
    "1064대 반례": "1,064 Vaccines",
    "\"f'(a)=0이면 무조건 극값?\", \"역함수 교점은 무조건 y=x 위?\" 학생들이 가장 많이 속는 함정을 1초 반례로 예방합니다.": "\"Does f'(a)=0 always give an extremum?\" \"Are all inverse intersections on y=x?\" Inoculate against classic math traps via 1-second counterexamples.",
    "오개념 진단 & 반례 실험 ➔": "Open Counterexample Lab ➔",
    "👩‍🏫 4. 교사용 5분 탐구 발문 런처": "👩‍🏫 4. 5-Min Classroom Inquiry Launcher",
    "수업 시나리오": "Lesson Scripts",
    "수업 시작 5분, 칠판에 띄워 학생들의 호기심(\"왜 그럴까?\")을 깨우는 발문·GeoGebra 미션·모둠 토의 질문 템플릿입니다.": "Ready-to-project 5-minute classroom warm-ups with Notice & Wonder prompts, GeoGebra missions, and group discussion guides.",
    "5분 수업 발문 시나리오 열기 ➔": "Open 5-Min Lesson Scenarios ➔",
    "✍️ 5. 탈-5지선다 창의 구성 실험실": "✍️ 5. De-Multiple-Choice Creative Lab",
    "NEW 창의력": "Constructive",
    "탈-5지선다 & 문제 발명 열기 ➔": "Open Constructive & What-If-Not Lab ➔",

    // Interactive Mathematical Wonder Lab & Curiosity Section
    "눈으로 만지는 수학의 경이(Wonder) 실험실 & 수학교육 철학": "Interactive Mathematical Wonder Lab & Philosophy of Math",
    "🏛️ \"수학은 암기가 아니라 눈으로 보는 예술이자 질문하는 탐험이다\"": "🏛️ \"Mathematics is not rote memorization — it is visual art and inquiry-driven exploration.\"",
    "공식을 외우기 전에 슬라이더를 직접 움직여 자연·우주·AI 속에 숨겨진 수학의 아름다움과 \"왜 이 수학을 배우는가?\"를 먼저 체험해 보세요!": "Move the sliders before memorizing any formula! Experience the mathematical beauty hidden in nature, space, and AI.",
    "🌍 \"선생님, 이 수학 왜 배워요?\" 8대 호기심 도감 열기 ➔": "🌍 \"Why Do We Learn This Math?\" 8-Domain Curiosity Atlas ➔",
    "🎬 질문형 시각 증명 영상 ➔": "🎬 Inquiry Visual Proof Videos ➔",
    "🌿 1. 피타고라스 프랙탈 나무": "🌿 1. Pythagoras Fractal Tree",
    "🎯 2. 아르키메데스 원주율(π) 극한": "🎯 2. Archimedes Pi (π) Exhaustion",
    "🌻 3. 해바라기 황금각과 피보나치": "🌻 3. Golden Angle & Fibonacci Spiral",
    "🎬 질문형 시각 증명 보기": "🎬 Watch Inquiry Visual Proof",
    "✍️ 관련 기출 디딤돌 풀기": "✍️ Solve Related Stepping Quiz",
    "💎 나의 수학적 깨달음(Eureka) 한 줄 사색 일지": "💎 My One-Line Mathematical Eureka Journal",
    "누적 통찰:": "Saved Insights:",
    "틀렸던 문제에서 찾은 반례나 오늘 나를 감탄하게 만든 보조선·원리를 한 줄로 기록해 보세요!": "Record a counterexample you discovered or an auxiliary line that sparked an 'Aha!' moment today!",
    "예: 원의 접선이 나오면 중심과 접점을 잇는 반지름이 항상 수직(90°)이다!": "e.g. A radius drawn to the point of tangency is always perpendicular (90°) to the tangent line!",
    "💾 통찰 기록": "💾 Save Insight",

    // Global 5-Platform Interactive Math Academy (Clean Trademark-Free Pedagogical Titles)
    "글로벌 5대 수학교육 명작 벤치마킹 · 인터랙티브 수학 아카데미": "Global Interactive Math Academy · Visual & Constructive Labs",
    "Desmos · Mathigon Polypad · Brilliant · NRICH · AoPS 융합": "Function Slides · Algebra Tiles · Low-Floor High-Ceiling · Mastery Map",
    "전 세계 수학교육을 선도하는 5대 플랫폼의 핵심 인터랙션(함수 구슬 챌린지 · 폴리패드 대수타일/양팔저울 · 10초 시각 직관 퍼즐 · 수학사 타임라인 & 마스터리 맵)을 민은기 선생님의 1,113개 시각 증명 및 16,548문항 기출과 결합했습니다.": "Combines interactive function marble slides, virtual algebra tiles & balance scales, 10-second visual intuition puzzles, and historical timelines with MIN EUN GI's 1,113 visual proofs and 16,548 stepping-stone problems.",
    "📊 5대 글로벌 벤치마킹 전체 분석 ➔": "📊 View Full Interactive Pedagogy Architecture ➔",
    "🎢 1. [Desmos형] Marbleslides 함수 구슬 챌린지": "🎢 1. Function Marble Slide Challenge",
    "🧱 2. [Mathigon형] 폴리패드 대수타일 & 양팔저울": "🧱 2. Virtual Algebra Tiles & Balance Scale",
    "🧩 3. [Brilliant×NRICH형] 낮은 문턱·높은 천장 시각 퍼즐": "🧩 3. Low-Floor High-Ceiling Visual Puzzles",
    "🏛️ 4. [Mathigon×Khan형] 인류 수학사 타임라인 & 16대 영역 마스터리": "🏛️ 4. History of Mathematics Timeline & 16-Domain Mastery",
    "Stage 1 · 일차함수": "Stage 1 · Linear",
    "Stage 2 · 이차포물선": "Stage 2 · Parabola",
    "Stage 3 · 삼각사인파": "Stage 3 · Sine Wave",
    "Stage 4 · 절댓값 V계곡": "Stage 4 · Abs Value V",
    "Stage 5 · 삼차변곡점": "Stage 5 · Cubic Curve",
    "🇺🇸 Desmos Classroom 벤치마킹": "🎢 Interactive Function Curve Lab",
    "🔴 구슬 발사! (Launch Marbles)": "🔴 Launch Marbles!",
    "✨ 최적 궤적 맞추기": "✨ Auto-Fit Target Curve",
    "✍️ 방금 실험한 함수 개념으로 수능·모평 기출 도전하기 ➔": "✍️ Practice Exam Quizzes with This Function Concept ➔",
    "🟦 대수타일 넓이 조립: (x+a)(x+b)": "🟦 Algebra Tiles Area: (x+a)(x+b)",
    "⚖️ 등식의 성질 양팔저울: 2x + a = x + b": "⚖️ Equation Balance Scale: 2x + a = x + b",
    "🇬🇧 Mathigon Polypad 벤치마킹 · 가상 수학 교구": "🧱 Virtual Manipulatives Lab",
    "눈으로 만지는 대수타일(Algebra Tiles)과 양팔저울": "Hands-On Algebra Tiles & Equation Balance Scale",
    "추상적인 다항식 전개 공식 (x+a)(x+b) = x² + (a+b)x + ab를 외우지 마세요! 파란색 x² 정사각형 1개, 초록색 x 막대 (a+b)개, 노란색 1 타일 (a×b)개가 빈틈없이 직사각형으로 조립되는 넓이 보존 원리입니다.": "Don't blindly memorize (x+a)(x+b) = x² + (a+b)x + ab! See how 1 blue x² square, (a+b) green x bars, and (a×b) yellow unit tiles assemble into one complete rectangle.",
    "🎬 대수·다항식 시각 증명 영상": "🎬 Algebra Visual Proof Video",
    "✍️ 다항식·방정식 기출 도전 ➔": "✍️ Solve Polynomial Quizzes ➔",
    "◀ 이전 퍼즐": "◀ Prev Puzzle",
    "다음 퍼즐 ▶": "Next Puzzle ▶",
    "⚡ Learn by Doing · 10초 무계산 직관 챌린지": "⚡ Learn by Doing · 10-Sec Visual Intuition Challenge",
    "정답 숫자 입력...": "Enter numeric answer...",
    "정답 확인 (+40 XP)": "Check Answer (+40 XP)",
    "🎬 질문형 시각 증명 영상": "🎬 Inquiry Visual Proof Video",
    "✍️ 수능 연계 문항 풀기 ➔": "✍️ Solve Related Exam Quizzes ➔",
    "🏛️ Mathigon 벤치마킹 · 인류 수학사 타임라인": "🏛️ History of Great Mathematicians Timeline",
    "🎬 이 수학자의 정리 영상 보기": "🎬 Watch Visual Proof of This Theorem",
    "✍️ 관련 기출 문제 도전 ➔": "✍️ Solve Related Exam Quizzes ➔",
    "📊 Khan × AoPS 벤치마킹 · 16대 영역 마스터리 맵": "📊 16-Domain Mathematics Mastery Matrix",
    "클릭 시 해당 단원 기출 & 시각 증명 즉시 실행": "Click any domain to launch visual proofs & quizzes",
    "👑 마스터": "👑 Master",
    "🔷 숙련 단계": "🔷 Proficient",
    "⚡ 탐구 진행": "⚡ Exploring",
    "🔥 집중 공략": "🔥 Core Focus",
    "🎯 킬러 도전": "🎯 Advanced",
    "1. 수와 다항식": "1. Numbers & Polynomials",
    "2. 방정식과 부등식": "2. Equations & Inequalities",
    "3. 도형의 방정식": "3. Analytic Geometry",
    "4. 집합·명제·함수": "4. Sets, Logic & Functions",
    "5. 지수·로그함수": "5. Exponents & Logs",
    "6. 삼각함수·도형": "6. Trigonometry",
    "7. 수열과 귀납법": "7. Sequences & Induction",
    "8. 함수의 극한·연속": "8. Limits & Continuity",
    "9. 다항함수 미분법": "9. Polynomial Calculus (Diff)",
    "10. 다항함수 적분법": "10. Polynomial Calculus (Int)",
    "11. 순열과 조합": "11. Permutations & Comb.",
    "12. 확률과 통계": "12. Probability & Stats",
    "13. 미적분(초월함수)": "13. Transcendental Calculus",
    "14. 기하·이차곡선": "14. Conics & Geometry",
    "15. 벡터·공간도형": "15. Vectors & 3D Space",
    "16. 유클리드 작도": "16. Euclidean Constructions",

    // Daily 3-Minute Math Eureka & Growth Flywheel
    "오늘의 3분 수학 유레카 & 실시간 성장 플라이휠": "Today's 3-Minute Math Eureka & Live Growth Flywheel",
    "📅 오늘의 미션": "📅 Today's Mission",
    "🟢 24/7 자가 진화 데몬 가동 중": "🟢 24/7 Auto-Evolution Engine Active",
    "매일 자정 자동 갱신되는 3분 수학 루틴(창의 기출 1문항 · 10초 오개념 O/X · 나만의 문제 발명)과 실시간 자료 증식 현황입니다.": "Daily 3-minute math routine refreshed at midnight: 1 constructive exam problem, 10-second misconception True/False, and What-If-Not problem invention.",
    "🔥 나의 일일 유레카 달성:": "🔥 Daily Eureka Progress:",
    "🔗 오늘의 3분 챌린지 친구 공유": "🔗 Share Today's 3-Min Challenge",
    "🎯 미션 1 · 오늘의 탈-5지선다 기출": "🎯 Mission 1 · Constructive Exam Problem",
    "도전 대기": "Ready",
    "🔥 오늘의 추천": "🔥 Today's Pick",
    "✅ 오늘 도전 완료!": "✅ Completed Today!",
    "✍️ 보기 가리고 도전하기 (+30 XP) ➔": "✍️ Solve Constructively (+30 XP) ➔",
    "다른 추천 문항 보기": "Next Recommended Problem",
    "⚡ 미션 2 · 오늘의 10초 오개념 O/X": "⚡ Mission 2 · 10-Sec Misconception True/False",
    "⭕ 언제나 참 (O)": "⭕ Always True (T)",
    "❌ 거짓·반례 존재 (X)": "❌ False · Counterexample (F)",
    "다음 O/X 퀴즈": "Next True/False Quiz",
    "🔀 미션 3 · 나만의 변형 문제 발명": "🔀 Mission 3 · Invent Your Own Problem",
    "나의 발명 누적:": "My Inventions:",
    "오늘의 조건 변형(What-If-Not): 직각(90°)을 60°로 바꾸거나 차수를 1 올린 나만의 문제를 만들어 보세요!": "What-If-Not Challenge: Change 90° to 60° or raise the polynomial degree by 1 to invent your own math problem!",
    "예: 만약 정삼각형이 아니라 정육각형 내부의 점 P라면 거리 합은?": "e.g. What if point P is inside a regular hexagon instead of an equilateral triangle?",
    "💡 나만의 문제 등록 (+30 XP)": "💡 Save My Problem (+30 XP)",
    "포트폴리오 ➔": "Portfolio ➔",
    "🚀 5대 지속 성장 플라이휠:": "🚀 5-Pillar Continuous Growth Flywheel:",
    "① min7014.github.io 신간 자동 흡수": "① Auto-Sync min7014.github.io Proofs",
    "② @min7014_ai v4.0 영상·숏폼 24h 생성": "② 24/7 @min7014_ai 1080p & Shorts",
    "③ 탈-5지선다 창의 수식 블록 조립": "③ Constructive Formula Block Solver",
    "④ 학생·교사 문제 발명 집단지성": "④ Student & Teacher Problem Invention",
    "⑤ SEO·AI 검색(llms.txt) 자동 인덱싱": "⑤ Open OER & AI Search Indexing",
    "🙋 새 기출·개념 해설 신청하기 ➔": "🙋 Request a New Problem or Proof ➔",

    // Quiz Explorer Filters, Pills, List & Footer
    "📂 최근 개설한 내 수업:": "📂 My Recent Classes:",
    "전체 대시보드 ➔": "Full Dashboard ➔",
    "실시간 문제 출제 현황": "Live Quiz Creation Queue",
    "확인 중...": "Checking...",
    "✨ 새 문제 출제 ➔": "✨ Create New Quiz ➔",
    "디딤돌 수학 문제 목록": "Stepping-Stone Math Problem Explorer",
    "불러오는 중…": "Loading…",
    "수업 팩 선택": "Select Lesson Pack",
    "🎒 수업 팩 묶기 모드 (체크 중)": "🎒 Lesson Pack Selection Active",
    "🎒 교사용 수업 팩 묶기": "🎒 Bundle Lesson Pack",
    "검색어 지우기": "Clear Search",
    "🎲 랜덤": "🎲 Random",
    "🎲 랜덤 기출 도전": "🎲 Random Quiz",
    "필터 초기화": "Reset Filters",
    "초기화": "Reset",
    "초기화 ✕": "Reset ✕",
    "전체 과목": "All Subjects",
    "공통(수I·II)": "Common (Math I·II)",
    "공통(수학I·II)": "Common (Math I·II)",
    "미적분": "Calculus",
    "기하": "Geometry",
    "확률과 통계": "Prob & Stats",
    "전체 연도": "All Years",
    "⚙️ 상세 조건 (연도·학년·시행월·문항번호·단원 태그) 열기": "⚙️ Detailed Filters (Exam Year · Grade · Month · Question # · Topic Tags)",
    "전체 학년도": "All Exam Years",
    "전체 학년": "All Grades",
    "고3 · N수": "Grade 12 (Senior)",
    "고2": "Grade 11",
    "고1": "Grade 10",
    "전체 시행월": "All Months",
    "11월 수능": "Nov Entrance Exam",
    "9월 모평": "Sep Official Mock",
    "6월 모평": "Jun Official Mock",
    "10월 학평": "Oct Academic Exam",
    "7월 학평": "Jul Academic Exam",
    "5월 모평·학평": "May Official Mock",
    "4월 학평": "Apr Academic Exam",
    "3월 학평": "Mar Academic Exam",
    "수학(가형)": "Math Type Ga (STEM)",
    "수학(나형)": "Math Type Na",
    "수학(고2)": "Math (Grade 11)",
    "공통수학(고1)": "Common Math (Grade 10)",
    "전체 번호": "All Numbers",
    "#전체보기": "#All Topics",
    "#이차함수·이차곡선": "#Quadratics & Conics",
    "#수열": "#Sequences",
    "#지수·로그": "#Exponents & Logs",
    "#삼각함수": "#Trigonometry",
    "#미적분": "#Calculus",
    "#확률·통계": "#Probability & Stats",
    "문항 목록을 불러오는 중…": "Loading math problems…",
    "✓ 완주": "✓ Mastered",
    "진행중": "In Progress",
    "📐 개념증명": "📐 Visual Proof",
    "오프라인": "Offline",
    "수업QR": "Class QR",
    "연관 추천": "Related Pick",
    "수학자료실 본관": "Math Archive Home",
    "수학의 성전 3D 게임": "Sanctuary of Math 3D",
    "오프라인 보관함": "Offline Vault",
    "교실 대시보드": "Class Dashboard",
    "개인정보처리방침": "Privacy Policy",
    "© mathedu · 민은기 선생님의 수학자료실": "© mathedu · MIN EUN GI's Math Archive",
    "📋 링크 복사": "📋 Copy Link",
    "🖥️ 칠판 QR": "🖥️ Projector QR",
    "▶️ 바로 풀기": "▶️ Start Now",

    // MIN EUN GI Explorer Modal & Academic Pedagogy Modal
    "민은기 선생님의 수학자료실 (`min7014.github.io`) 심층 커리큘럼 & AI 도슨트관": "MIN EUN GI's Math Archive (`min7014.github.io`) Deep Curriculum & AI Voice Guide",
    "16대 수학 영역 · 165개 세부 단원 트리 · 초등 4단계 디딤돌 · 시각적 증명 PDF · 실전 보조선 팁 · 🔊 음성 해설": "16 Math Domains · 165 Sub-Units · 4-Step Elementary-to-Advanced Scaffolding · Visual Proof PDFs · Auxiliary Line Tips · 🔊 Voice Guide",
    "🔍 개념·정리·보조선·단원 검색 (예: 타원, 단델린, 피타고라스, 원주각, 체바, 메넬라우스, 정칠각형, 정규분포, 구분구적법, 평균값 정리, 작도)...": "🔍 Search theorem, concept, auxiliary line, or topic (e.g. ellipse, Dandelin, Pythagoras, inscribed angle, Ceva, Menelaus, heptagon, derivative, normal distribution)...",
    "전체 (1,113)": "All (1,113)",
    "유클리드 기하 (189)": "Euclidean Geometry (189)",
    "다항식·수체계 (178)": "Polynomials & Numbers (178)",
    "미분·도함수 (101)": "Differentiation (101)",
    "이차곡선·단델린 (85)": "Conics & Dandelin (85)",
    "벡터·공간도형 (80)": "Vectors & 3D (80)",
    "지수·로그 (70)": "Exponents & Logs (70)",
    "극한·연속 (69)": "Limits & Continuity (69)",
    "해석기하·원 (61)": "Circles & Coords (61)",
    "삼각비·삼각함수 (54)": "Trigonometry (54)",
    "함수·집합 (49)": "Functions & Sets (49)",
    "기하 변환·대칭 (36)": "Transformations (36)",
    "확률과 통계 (35)": "Prob & Stats (35)",
    "방정식·부등식 (32)": "Equations & Ineq. (32)",
    "적분·구분구적법 (32)": "Integration (32)",
    "수열·시그마 (22)": "Sequences (22)",
    "🔥 @min7014_ai 영상·숏폼": "🔥 @min7014_ai Videos & Shorts",
    "자료를 불러오는 중...": "Loading archive materials...",
    "🎬 @min7014_ai 설명 영상 게시판 ➔": "🎬 @min7014_ai Video Lecture Board ➔",
    "🌐 민은기 선생님의 수학자료실 본관 ➔": "🌐 MIN EUN GI's Math Archive ➔",
    "🔊 음성 도슨트": "🔊 Voice Guide",
    "🎬 다국어 스튜디오": "🎬 Multilingual Studio",
    "📄 증명 PDF": "📄 Proof PDF",
    "▶️ 원문 영상": "▶️ Original Video",
    "🔗 연관 기출": "🔗 Related Quizzes",
    "📏 자·컴퍼스 작도": "📏 Compass Construction",
    "🎓 핵심 원리": "🎓 Core Principle",
    "👁️ 시각적 증명": "👁️ Visual Proof",
    "💡 수능 실전 보조선·풀이 팁": "💡 Practical Auxiliary Line & Solving Tip",
    "현대 수학교육학 5대 검증 원리 적용 안내": "5 Research-Validated Principles of Mathematics Education",
    "mathedu의 모든 문항 페이지에는 세계 수학교육학 및 교육인지과학 메타분석(Hattie, NMAP)에서 학습 효과 크기(Effect Size)가 가장 높은 5대 학문적 원리가 탑재되어 있습니다.": "Every problem page on mathedu integrates the five highest-effect-size pedagogical principles validated in global mathematics education & cognitive science research (Hattie, Bruner, Vygotsky, Freudenthal, Pólya).",

    // video_board.html UI
    "🏠 메인 홈": "🏠 Main Home",
    "🎙️ 20개국어 AI 강의 스튜디오": "🎙️ 20-Language Lecture Studio",
    "🎓 교실 칠판 QR 구독카드": "🎓 Classroom QR Subscribe Card",
    "📺 @min7014_ai 공식 채널 ↗": "📺 @min7014_ai Channel ↗",
    "🎬 @min7014 원본 채널 ↗": "🎬 @min7014 Original Channel ↗",
    "📚 수학자료실 원본 ↗": "📚 Math Archive Home ↗",
    "📚 전체 수록 수학 자료": "📚 Total Math Topics",
    "min7014.github.io 전 영역 통합": "Complete min7014.github.io Archive",
    "🤖 @min7014_ai 등록 완료 영상": "🤖 @min7014_ai Published Videos",
    "집계 중...": "Counting...",
    "한국어(KO) · 영어(EN) 1080p 마스터 강의": "Korean (KO) & English (EN) 1080p Master Lectures",
    "📄 단계별 플립북 PDF 자료": "📄 Step-by-Step Flipbook PDFs",
    "AI 단계별 시각 증명 영상 제작 대상": "Step-by-step visual proof source slides",
    "🎬 @min7014 원본 유튜브 연결": "🎬 @min7014 Original Videos",
    "수학자료실 원본 작도·해설 영상 아카이브": "Original construction & proof video archive",
    "🤖 @min7014_ai 자동 제작·업로드 엔진 대기 중 (새 자료 설명영상 제작 후 자동 유튜브 업로드 & 게시판 링크 등록)": "🤖 @min7014_ai Automated Production & YouTube Sync Engine Ready",
    "다음 미등록 1개 자료": "Next 1 Unlisted Topic",
    "다음 미등록 3개 자료": "Next 3 Unlisted Topics",
    "다음 미등록 5개 자료": "Next 5 Unlisted Topics",
    "🚀 AI 설명영상 제작 & @min7014_ai 자동 업로드": "🚀 Produce & Upload to @min7014_ai",
    "🔄 @min7014_ai 채널 링크 동기화": "🔄 Sync @min7014_ai Channel Links",
    "🛡️ 스트릭 보호권 활성": "🛡️ Streak Shield Active",
    "🔥 오늘 직관 스트릭 달성 완료!": "🔥 Today's Intuition Streak Checked In!",
    "⚡ 오늘의 직관 출석 체크 (+1일)": "⚡ Check In Today's Visual Intuition (+1 Day)",
    "🔔 유튜브 구독": "🔔 Subscribe",
    "🟩 5초 시각 암산 챌린지 & 이모지 카드": "🟩 5-Sec Mental Math & Emoji Scorecard",
    "🏛️ min7014.github.io 원문 기반 ↗": "🏛️ Based on min7014.github.io ↗",
    "🟩 3초 컷 (정답 25!)": "🟩 Solved in 3s (25!)",
    "🟨 10초 컷": "🟨 Solved in 10s",
    "🟦 영상 힌트 유레카": "🟦 Eureka via Visual Hint",
    "🏛️ 100% 오리지널 PDF 직강 마스터클래스": "🏛️ 100% Original PDF Step-by-Step Masterclass",
    "51~88분 연속 정주행": "51–88 Min Deep Dive",
    "🍿 오리지널 수학자료실 PDF 직강 마스터클래스 극장": "🍿 Original Math Archive PDF Masterclass Theater",
    "🔔 1초 무료 구독 응원 ↗": "🔔 Subscribe Free ↗",
    "🇰🇷 88분 방정식·부등식 Vol.1 ↗": "🇰🇷 88m Equations & Ineq. Vol.1 ↗",
    "🇰🇷 62분 벡터·기하 Vol.2 ↗": "🇰🇷 62m Vectors & Geometry Vol.2 ↗",
    "🇰🇷 52분 함수·극한 Vol.3 ↗": "🇰🇷 52m Functions & Limits Vol.3 ↗",
    "🇰🇷 37분 원의 성질 ↗": "🇰🇷 37m Circle Properties ↗",
    "영상을 선택하세요": "Select a video lecture",
    "🔔 @min7014_ai 무료 구독하기 ↗": "🔔 Subscribe Free to @min7014_ai ↗",
    "YouTube에서 열기 ↗": "Open on YouTube ↗",
    "✕ 플레이어 닫기": "✕ Close Player",
    "🔗 현재 재생 중인 유튜브 등록 링크": "🔗 Currently Playing YouTube URL",
    "🔔 @min7014_ai 1클릭 구독하기 ↗": "🔔 1-Click Subscribe to @min7014_ai ↗",
    "📂 🇰🇷 한국어 정주행 재생목록 ↗": "📂 🇰🇷 Korean Master Playlist ↗",
    "📣 카톡·커뮤니티 인기 홍보문구 복사": "📣 Copy Shareable Promo Kit",
    "🗳️ 유튜브 커뮤니티 퀴즈·투표 게시물 복사": "🗳️ Copy Community Quiz Post",
    "전체 자료 (1,111)": "All Topics (1,111)",
    "❓ 질문하는 수업 버전 완료": "❓ Inquiry Classroom Edition Ready",
    "🤖 @min7014_ai 영상 등록 완료": "🤖 @min7014_ai Video Published",
    "📱 숏폼 (#Shorts · 9:16) 완료": "📱 #Shorts (9:16) Ready",
    "📄 단계별 PDF 설명자료 (866)": "📄 Step-by-Step PDFs (866)",
    "🎬 원본 유튜브 보유 (939)": "🎬 Original Videos (939)",
    "📐 기하 (Geometry)": "📐 Geometry",
    "🔢 대수·수열·지수로그": "🔢 Algebra, Sequences & Logs",
    "📈 미적분·해석": "📈 Calculus & Analysis",
    "🎲 확률·통계": "🎲 Probability & Statistics",
    "📂 세부 단원 전체 (All Categories)": "📂 All Sub-Categories",
    "50개씩 보기": "Show 50 per page",
    "100개씩 보기": "Show 100 per page",
    "300개씩 보기": "Show 300 per page",
    "1,111개 전체 한눈에 보기": "Show All 1,111 Topics",
    "데이터를 불러오는 중입니다...": "Loading video archive data...",
    "취소": "Cancel",
    "💾 게시판에 링크 저장": "💾 Save Links to Board",

    // game.html & video_studio.html & offline/index.html & create.html
    "수학의 성전 3D": "Sanctuary of Math 3D",
    "16,548 디딤돌 퀘스트 & 동적 기하 RPG": "16,548 Stepping-Stone Quests & Dynamic Geometry RPG",
    "📲 앱 설치": "📲 Install App",
    "📚 16,548문항 전체 서고": "📚 All 16,548 Problems",
    "📐 3,400+ 시각 증명": "📐 3,400+ Visual Proofs",
    "© 2026 민은기 선생님의 수학자료실 (mathedu) · 학생·교사 100% 무료 열린 수학교육": "© 2026 MIN EUN GI's Math Archive (mathedu) · 100% Free Open Math Education",
    "전체 단원 문제은행": "Complete Problem Bank",
    "교사용 출제 스튜디오": "Teacher Creation Studio",
    "민은기 선생님의 수학자료실 · 다국어 PDF 강의 영상 스튜디오": "MIN EUN GI's Math Archive · Multilingual PDF Lecture Studio",
    "설명 텍스트 우선 생성 ➔ 🇰🇷 한국어·🇺🇸 영어 버전은 유튜브(YouTube) 저장 ➔ 전 세계 다국어 나레이션 확장": "Script-First Pipeline ➔ 🇰🇷 KO & 🇺🇸 EN 1080p YouTube Lectures ➔ 20+ Global Languages",
    "🏠 메인 허브로": "🏠 Back to Main Hub",
    "📺 @min7014_ai 채널 ↗": "📺 @min7014_ai Channel ↗",
    "🌐 min7014.github.io 본관 ↗": "🌐 min7014.github.io Home ↗",
    "🎬 단계별 플립북 PDF 강의 영상 시스템 (🇰🇷 한국어 · 🇺🇸 영어 버전 YouTube 저장 방식)": "🎬 Step-by-Step Flipbook PDF Video Lecture Studio (🇰🇷 KO & 🇺🇸 EN YouTube Streaming + 20 Languages)",
    "STEP 1 · 페이지별 설명 텍스트(대본) 우선 생성": "STEP 1 · Generate Step-by-Step Explanation Script",
    "PDF 1페이지~마지막 페이지까지 도형·수식 단계 변화를 분석하여 가벼운 설명 텍스트 대본(JSON)을 먼저 생성·편집합니다.": "Analyzes geometric & algebraic transitions from page 1 to the final slide to build an editable JSON narration script.",
    "STEP 2 · 🇰🇷 한국어 & 🇺🇸 영어 버전은 YouTube에 저장": "STEP 2 · Stream 🇰🇷 Korean & 🇺🇸 English 1080p on YouTube",
    "한국어(KO)와 영어(EN) 1080p 강의 영상·썸네일·자막(.srt)·타임스탬프를 자동 패키징하여 유튜브에 저장·스트리밍합니다.": "Packages 1080p KO/EN lectures, thumbnails, .srt captions, and chapters for instant YouTube streaming without repo bloat.",
    "STEP 3 · 전 세계 어떤 언어로도 설명 영상 즉시 확장": "STEP 3 · Instant Narration in 20+ Global Languages",
    "동일한 설명 텍스트 대본을 바탕으로 일본어·스페인어·중국어·프랑스어·독일어·베트남어 등 모든 국가 언어 영상을 즉시 재생·추출합니다.": "Translates and synthesizes synchronized slide-by-slide voice lectures in Japanese, Spanish, Chinese, French, German, Vietnamese, and more.",
    "📚 수학자료실 PDF 선택 (866개 전체):": "📚 Select Math Archive PDF (All 866):",
    "🔄 이 자료 불러오기": "🔄 Load Selected PDF",
    "⭐ 대표 초고화질 유튜브 패키지(KO/EN) 완비 강의:": "⭐ Featured 1080p KO/EN Master Packages:",
    "🌍 나레이션 및 영상 제작 국가 언어 선택:": "🌍 Target Narration & Video Language:",
    "🌐 [1차 설명 텍스트] ➔ 선택한 국가 언어로 전 페이지 나레이션 자동 생성": "🌐 Auto-Generate Full-Slide Narration in Selected Language",
    "📥 다국어 대본(.json) 다운로드": "📥 Download Script (.json)",
    "📥 현재 언어 자막(.srt) 다운로드": "📥 Download Subtitles (.srt)",
    "건": " items",
    "(가)": "(A)",
    "(나)": "(B)",
    "(다)": "(C)",
    "✨ 새 버전 있음!": "✨ Update Available!",
    "🔥 나의 시각적 수학 직관 스트릭:": "🔥 My Visual Math Intuition Streak: ",
    "일 연속 달성!": "-Day Streak!",
    "공식 암기 대신 매일 딱 1편의": "Instead of rote memorization, watch 1 ",
    "@min7014_ai 시각적 증명": "@min7014_ai Visual Proof",
    "을 눈으로 확인하고 두뇌 직관 스트릭을 이어가세요!": " each day to build your mathematical intuition streak!",
    "원본 PDF를 1페이지부터 끝까지 한 땀 한 땀 설명하는 단원별 51~88분 정주행 마스터클래스입니다!": " original step-by-step PDFs explained from page 1 to Q.E.D. in 51–88 min masterclasses!",
    "자유 학습자": "Independent Learner",
    "익명": "Anonymous",
    "선생님 / 학생": "Teacher / Student",
    "여기로 파일 드래그": "Drop File Here",
    "접수 즉시 전용 퀴즈 링크가 발급": "a dedicated quiz link is issued immediately upon submission",
    "문제를 붙여넣으세요... (이미지만 붙여넣어도 접수 가능합니다)": "Paste problem text or image here... (Image-only paste is also supported)",
    "암호학적 무편향 공정 추첨": "Cryptographically Fair Random Draw",
    "기하 아트워크 포스터": "Geometric Artwork Poster",
    "학년도": "Exam Year",
    "선택과목": "Subject",
    "주제별 탐색": "Browse by Topic",
    "매듭 기하": "Knot Geometry",
    "한국어": "🇰🇷 KO",
    "개인정보처리방침 (Privacy Policy)": "Privacy Policy",

    // mathlab.html UI & Tooltips
    "선택": "Select",
    "객체를 선택하고 드래그하여 이동합니다. 빈 공간을 1초간 누르면 텍스트를, 한번 클릭 후 0.2초 이내에 다시 1초간 누르고 있으면 명령어를 입력할 수 있습니다.": "Select and drag objects to move them. Long-press empty space (1s) to add LaTeX text, or click then hold (1s) to enter an algebraic equation/command.",
    "점": "Point",
    "선분": "Segment",
    "직선": "Line",
    "반직선": "Ray",
    "원": "Circle",
    "포물선": "Parabola",
    "타원": "Ellipse",
    "쌍곡선": "Hyperbola",
    "평행선": "Parallel Line",
    "수선": "Perpendicular Line",
    "중점": "Midpoint",
    "각의 이등분선": "Angle Bisector",
    "∑ 수식 입력": "∑ Formula Input",
    "📐 증명 프리셋": "📐 Proof Presets",
    "포물선 정의 (|PF|=|PH|)": "Parabola Definition (|PF|=|PH|)",
    "타원 정의 (|PF₁|+|PF₂|=2a)": "Ellipse Definition (|PF₁|+|PF₂|=2a)",
    "쌍곡선 정의 (||PF₁|-|PF₂||=2a)": "Hyperbola Definition (||PF₁|-|PF₂||=2a)",
    "원주각과 중심각 불변성": "Inscribed & Central Angle Invariance",
    "삼각함수 라디안 파동 (π/2)": "Trigonometric Radian Wave (π/2)",
    "이차곡선 외부 접선 작도": "External Tangent to Conic Construction",
    "삼각형 외심·수선 작도": "Triangle Circumcenter & Altitude Construction",
    "🔄 빈 캔버스 초기화": "🔄 Clear Canvas",
    "화면 설정": "View Settings",
    "격자": "Grid",
    "좌표축": "Axes",
    "눈금": "Ticks",
    "축": "Axis",
    "학습모드": "Practice Mode",
    "점 찍기": "Plot Points",
    "일차함수 그래프 그리기": "Graph Linear Function",
    "원의 그래프 그리기": "Graph Circle",
    "작도 문제": "Construction Tasks",
    "객체 목록": "Objects",
    "🌙 네온": "🌙 Neon",
    "☀️ 라이트": "☀️ Light",
    "🎯 선택된 영역": "🎯 Selected Target",
    "🎯 다시 선택": "🎯 Reselect",

    // 404.html AI Quiz Builder Waiting Room
    "안티그래비티 AI가 문제를 제작 중입니다!": "Antigravity AI is Crafting Your Quiz!",
    "출제 요청이 성공적으로 접수되어 현재": "Your request has been received and",
    "5~8단계 인터랙티브 퀴즈": "a 5~8 Step Interactive Scaffolding Quiz",
    "를 자동 생성 및 배포 중입니다.": "is being automatically generated and deployed.",
    "보통 1~2분 소요되며,": "This usually takes 1–2 minutes,",
    "제작이 완료되는 즉시 이 페이지가 자동으로 문제 화면으로 바뀝니다.": "and this page will automatically load your quiz as soon as it is ready.",
    "AI 실시간 문제 분석 및 문항 빌드 중...": "Analyzing math structure & building interactive scaffolding steps...",
    "✅ 1단계": "✅ Step 1",
    "문제 접수 완료": "Request Received",
    "⏳ 2단계": "⏳ Step 2",
    "AI 개념 빌드업": "Scaffolding Build",
    "🚀 3단계": "🚀 Step 3",
    "온라인 자동 배포": "Live Deployment",
    "문항 코드:": "Quiz Slug:",
    "접수 제목:": "Title:",
    "진행 상태:": "Status:",
    "제작 및 배포 대기 중 (창을 유지해 주세요)": "Building & deploying quiz (please keep this tab open)",
    "🔄 수동 새로고침": "🔄 Refresh Now",
    "🏠 mathedu 홈으로": "🏠 Back to mathedu Home",
    "페이지를 찾을 수 없습니다 (404)": "Page Not Found (404)",
    "요청하신 주소의 페이지가 존재하지 않거나 이동되었습니다.": "The requested page does not exist or has been moved.",
    "주소를 다시 확인해 주시기 바랍니다.": "Please check the URL or return to the main archive.",
    "🏠 mathedu 메인 홈으로 이동": "🏠 Return to mathedu Home",

    // index.html Interactive Labs (Marbleslides, Polypad, Elo)
    "Stage 1 · 일차함수 미끄럼틀 다리 (y = a·x + b)": "Stage 1 · Linear Slide Bridge (y = a·x + b)",
    "중1·중2 일차함수의 기울기(a)와 y절편(b)": "Slope (a) and y-Intercept (b) of a Linear Function",
    "기울기 a와 y절편 b 슬라이더를 조절해 왼쪽 위에서 떨어지는 구슬이 황금 별(★) 4개를 모두 스치고 지나가게 만드세요!": "Adjust slope a and y-intercept b so the falling marbles collect all 4 golden stars (★)!",
    "💡 별들이 오른쪽 아래로 내려가고 있으므로 기울기 a를 -0.45로 맞추고, y절편 b를 0.6으로 조절해 보세요!": "💡 Since the stars descend to the right, try setting slope a = -0.45 and y-intercept b = 0.6!",
    "Stage 2 · 이차함수 포물선 계곡 (y = a·x² + q)": "Stage 2 · Parabolic Valley (y = a·x² + q)",
    "중3·공통수학1 이차함수의 폭(a)과 y축 평행이동(q)": "Width (a) and Vertical Shift (q) of a Quadratic Parabola",
    "아래로 볼록한 포물선의 폭(a)과 꼭짓점 y좌표(q)를 조절해 구슬이 포물선 계곡을 타고 별(★) 4개를 모두 모으게 하세요!": "Adjust parabola width (a) and vertex height (q) so the marbles roll along the valley and collect all 4 stars (★)!",
    "💡 가장 낮은 별이 (0, -1.8)에 있습니다! 폭 a = 0.15, 꼭짓점 높이 q = -1.8로 맞춰보세요!": "💡 The lowest star sits at (0, -1.8)! Try setting width a = 0.15 and vertex q = -1.8!",
    "Stage 3 · 삼각함수 사인파 롤러코스터 (y = a·sin(b·x) - 0.25x)": "Stage 3 · Sine Wave Coaster (y = a·sin(b·x) - 0.25x)",
    "대수(수I) 삼각함수의 진폭(a)과 주기 계수(b)": "Amplitude (a) and Frequency (b) of a Sine Wave",
    "물결치는 사인 곡선의 진폭(a)과 주파수(b)를 조절해 위아래로 배치된 별(★) 4개를 파도를 타며 획득하세요!": "Tune amplitude (a) and frequency (b) of the sine wave to ride through all 4 stars (★)!",
    "💡 진폭 a = 1.1, 주파수 b = 1.0으로 맞추면 별들의 파도 높낮이와 정확히 일치합니다!": "💡 Setting amplitude a = 1.1 and frequency b = 1.0 matches the wave crests of the stars!",
    "Stage 4 · 절댓값 V자 반사 계곡 (y = a·|x - p| - 1.8)": "Stage 4 · Absolute Value V-Valley (y = a·|x - p| - 1.8)",
    "공통수학 절댓값 그래프의 꺾이는 대칭축(x = p)": "Axis of Symmetry (x = p) of an Absolute Value Graph",
    "절댓값 함수의 꺾이는 꼭짓점 x = p와 기울기 a를 조절해 V자 계곡을 따라 별 4개를 모두 통과시키세요!": "Adjust vertex x = p and slope a of the V-shaped graph to pass through all 4 stars!",
    "💡 가장 낮은 별의 x좌표가 p = 0.5입니다! 기울기 a = 0.55, 꺾이는 점 p = 0.5로 맞춰보세요!": "💡 The lowest star is at x = 0.5! Try slope a = 0.55 and vertex p = 0.5!",
    "Stage 5 · 삼차함수 변곡점 슬라이드 (y = a·x³ + b·x)": "Stage 5 · Cubic Inflection Slide (y = a·x³ + b·x)",
    "수학II(미적분I) 삼차함수의 변곡점 대칭과 계수 부호": "Origin Symmetry & Inflection Point of a Cubic Function",
    "삼차항 계수(a)와 일차항 계수(b)를 조절해 원점 대칭 S자 미끄럼틀을 만들어 별 4개를 한 번에 쓸어담으세요!": "Tune cubic coefficient (a) and linear coefficient (b) to shape an S-curve slide through all 4 stars!",
    "💡 왼쪽 위에서 오른쪽 아래로 부드럽게 내려가는 삼차함수가 되도록 a = -0.06, b = -0.25로 설정해 보세요!": "💡 Try a = -0.06 and b = -0.25 for a smooth descending cubic slide!",
    "그랜드마스터 Grandmaster": "Grandmaster",
    "올림피아드 마스터 Master": "Grand Strategist Master",
    "보조선 장인 Strategist": "Auxiliary Strategist",
    "탐구자 Explorer": "Math Explorer",

    // board/*.html, board/archive.html & mathedu-room.js Schematic & Quiz Strings
    "초등학생도 1단계부터 차근차근 따라가면 수능·학력평가 본문항까지 스스로 풀 수 있는 단계별 디딤돌 퀴즈입니다.": "Step-by-step scaffolding quiz designed so any learner can build up from elementary intuition to solve the full exam problem.",
    "Lv.1 입문자": "Lv.1 Explorer",
    "공식 엠블럼 Dandelin Spheres": "Official Emblem · Dandelin Spheres",
    "시각적 도형 다이어그램": "Visual Concept Diagram",
    "초등 눈높이 디딤돌": "Elementary-to-Advanced Scaffolding",
    "수체계가 확장될 때 규칙이 어떻게 보존되는지": "How operational laws are preserved as number systems expand",
    "최종 본문항": "Final Target Problem",
    "먼저 알아야 할 지식": "Prerequisite Concept",
    "\"만약 문제의 숫자·지수·각도·조건을 바꾼다면 답이 어떻게 달라질까?\"": "\"What if we vary the numbers, exponents, angles, or conditions — how would the answer change?\"",
    "지수의 확장": "Extension of Exponents",
    "중간 전개 과정": "Intermediate Algebraic Steps",
    "최종 결과값": "Final Result",
    "📋 [문제 분석 및 핵심 출제 의도]": "📋 [Problem Analysis & Core Mathematical Objective]",
    "본 문항은": "This problem assesses",
    "단원에서": "in",
    "능력을 평가하는 2점 기출문항입니다.": "(2-point official exam question).",
    "능력을 평가하는 3점 기출문항입니다.": "(3-point official exam question).",
    "능력을 평가하는 4점 기출문항입니다.": "(4-point official exam question).",
    "[출발 조건 & 단원 원리]": "[Given Conditions & Core Principle]",
    "[디딤돌 1~4단계 연결]": "[Scaffolding Steps 1–4]",
    "핵심 식 변형 · 대입": "Key Algebraic Transformation & Substitution",
    "[최종 목표값 도출]": "[Final Target Value]",
    "검산 및 조건 확인 완료": "Verified Against All Conditions",
    "🗺️ [한눈에 보는 도식화 풀이 흐름도]": "🗺️ [Schematic Solution Flowchart]",
    "1단계: 초등 기초 직관 및 구구단·사칙연산 규칙 확인": "Step 1: Elementary Arithmetic Intuition & Pattern Check",
    "2단계: 거듭제곱근과 지수법칙 기호 번역 및 기본 공식 연결": "Step 2: Translate Radical & Exponent Notation to Core Laws",
    "3단계: 출발 조건 식 세우기 (지수의 확장)": "Step 3: Formulate Initial Equation (Extension of Exponents)",
    "4단계: 핵심 관계식 정리 및 중간 값 도출": "Step 4: Simplify Key Relations & Derive Intermediate Value",
    "5단계: 최종 계산 조립 ⇒ 정답": "Step 5: Assemble Final Calculation ⇒ Answer",
    "📐 [단계별 상세 풀이 전개]": "📐 [Step-by-Step Detailed Solution]",
    "✨ [정답 도출 및 실전 점검 포인트]": "✨ [Final Answer & Practical Verification]",
    "따라서 구하는 최종 정답은": "Therefore, the final answer is",
    "입니다.": ".",
    "자료를 깊이 있게 감상하는 법": "How to Explore Visual Proofs Deeply",
    "비회원 안내:": "Guest Mode:",
    "동일 학습자로 자동 인식": "automatically recognized as the same learner",
    "[내가 푼 문제]": "[My Solved Problems]",
    "💡 해설 보기": "💡 View Explanation",
    "💡 해설 닫기": "💡 Hide Explanation",

    // video_board.html & video_studio.html Dynamic Buttons & Labels
    "🇰🇷 한국어 모드 (KO)": "🇰🇷 Korean Mode (KO)",
    "🇺🇸 English Mode (EN)": "🇺🇸 English Mode (EN)",
    "🌐 수학자료실 웹페이지 ↗": "🌐 Math Archive Web ↗",
    "📄 단계별 증명 PDF ↗": "📄 Step-by-Step Proof PDF ↗",
    "🧭 GeoGebra 앱렛 ↗": "🧭 GeoGebra Applet ↗",
    "🎙️ 다국어 AI 강의 스튜디오": "🎙️ Multilingual Lecture Studio",
    "▶ 🇰🇷 한국어 설명영상 재생": "▶ 🇰🇷 Play Korean Video",
    "▶ 🇺🇸 영어 설명영상 재생": "▶ 🇺🇸 Play English Video",
    "🧭 🇰🇷 수학 이슈 × 수학교육 통찰 (1080p)": "🧭 🇰🇷 Math Issue × Insight (KO 1080p)",
    "❓ 🇰🇷 질문하는 수업 버전 (1080p) 재생": "❓ 🇰🇷 Inquiry Classroom Edition (KO 1080p)",
    "🌟 🇰🇷 창의 아이디어 시네마 (Beyond PDF · 1080p)": "🌟 🇰🇷 Visual Idea Cinema (KO 1080p)",
    "🌟📱 🇰🇷 창의 아이디어 숏폼 (9:16)": "🌟📱 🇰🇷 Visual Idea #Shorts (KO)",
    "📱 🇰🇷 일반형 숏폼 재생": "📱 🇰🇷 Standard #Shorts (KO)",
    "❓📱 🇰🇷 질문형 숏폼 재생": "❓📱 🇰🇷 Inquiry Q-#Shorts (KO)",
    "🚀 AI 영상 제작 & @min7014_ai 업로드": "🚀 Produce & Upload to @min7014_ai",
    "🎙️ 스튜디오 즉시 음성강의": "🎙️ Instant Voice Lecture in Studio",
    "🔗 유튜브 링크 직접 등록/수정": "🔗 Edit YouTube Links",
    "🛠️ 자체 제작 MathLab & 보편 수학공학도구 실시간 실습 스튜디오": "🛠️ Interactive MathLab v1.4 Split-Screen Practice Studio",
    "🏫 교사용 5분 발문 & 생기부 세특·영문 탐구 문구 복사": "🏫 Copy 5-Min Inquiry Prompt & Student Research Guide",
    "🏫 교사용 5분 발문 & 생기부 세특·IB IA 문구 복사": "🏫 Copy 5-Min Inquiry Prompt & Student Research Guide",
    "🖨️ 교실 QR 활동지 인쇄": "🖨️ Print Classroom QR Worksheet",
    "🎬 @min7014 원본 영상 재생": "🎬 Play @min7014 Original Video",
    "원본 유튜브 미등록": "Original Video Pending",
    "조건에 해당하는 자료가 없습니다. 검색어나 필터를 초기화해 보세요.": "No matching topics found. Try resetting your search or filters.",
    "📤 @min7014_ai 스튜디오": "📤 @min7014_ai Studio",
    "🎞️ 수학자료실 원본 유튜브 재생": "🎞️ Play Original Archive Video",
    "↗ YouTube에서 열기": "↗ Open on YouTube",
    "🇰🇷 한국어 AI 강의 (@min7014_ai KO)": "🇰🇷 Korean Video Lecture (@min7014_ai KO)",
    "🇺🇸 영어 AI 강의 (@min7014_ai EN)": "🇺🇸 English Video Lecture (@min7014_ai EN)",
    "✅ 유튜브(KO) 저장 완료": "✅ YouTube (KO) Published",
    "▶️ 한국어 유튜브 재생": "▶️ Play KO YouTube",
    "▶️ 영어 유튜브 재생": "▶️ Play EN YouTube",
    "📋 KO 제목·타임스탬프 복사": "📋 Copy KO Title & Chapters",
    "📋 EN 제목·타임스탬프 복사": "📋 Copy EN Title & Chapters",
    "📥 KO .srt 자막": "📥 KO .srt Captions",
    "📥 EN .srt 자막": "📥 EN .srt Captions",
    "🖼️ KO 썸네일": "🖼️ KO Thumbnail",
    "🖼️ EN 썸네일": "🖼️ EN Thumbnail",
    "저장": "Save",
    "@min7014_ai 자동 생성·업로드 CLI": "@min7014_ai Auto-Build & Upload CLI",
    "🔄 @min7014_ai RSS 동기화": "🔄 Sync @min7014_ai RSS",
    "📋 CLI 명령어 복사": "📋 Copy CLI Command",
    "📝 페이지별 [1차 설명 텍스트] & [2차 다국어 나레이션] 대본 편집기": "📝 Slide-by-Slide Visual Proof Script & Multilingual Narration Editor",
    "의 각 PDF 자료는 페이지마다 한 단계씩 전개됩니다. 먼저": "Each PDF unfolds one logical step per slide. First,",
    "설명 텍스트(대본)": "the step-by-step script",
    "를 생성한 뒤, 가장 수요가 높은": "is structured; high-demand",
    "한국어 버전(KO)과 영어 버전(EN) 영상은 유튜브(YouTube)에 저장·스트리밍": "Korean (KO) & English (EN) 1080p lectures stream directly on YouTube",
    "하고, 그 외 모든 국가 언어는 대본으로부터 즉시 생성합니다.": ", while 20+ global languages synthesize on demand from the script.",
    "각 페이지의": "Each slide's",
    "1차 설명 텍스트(한국어 기준)": "base visual proof script",
    "가 먼저 만들어지고, 이를 통해 한국어·영어(유튜브 저장용) 및 전 세계 모든 국가 언어 나레이션이 생성됩니다.": "drives synchronized Korean/English YouTube packages and 20+ global voice narrations.",
    "👁️ 슬라이드 보기": "👁️ View Slide",
    "🇰🇷 [1차] 기본 설명 텍스트 (한국어 원본·수정 가능)": "🇰🇷 [Source] Base Explanation Script (Editable)",
    "도입 · 주제 및 목표": "Intro · Topic & Proof Goal",
    "완결 · 웹 탐구 안내": "Conclusion · Interactive Web Exploration",
    "🔍 주제 검색 (예: 피타고라스, 체바, 타원, 단델린, 중점연결, 미분...)": "🔍 Search topic (e.g. Pythagoras, Ceva, ellipse, Dandelin, derivative...)",
    "직접 코드 입력 (예: nl, sv, el)": "ISO code (e.g. nl, sv, el)",
    "@min7014_ai 한국어 URL (https://youtu.be/...)": "@min7014_ai Korean URL (https://youtu.be/...)",
    "@min7014_ai 영어 URL (https://youtu.be/...)": "@min7014_ai English URL (https://youtu.be/...)",
    "상단 [전 페이지 나레이션 자동 생성] 버튼을 누르거나 직접 입력하세요.": "Click [Auto-Generate Full-Slide Narration] above or edit directly here.",

    // offline/index.html Smart Search & Page Titles & Tooltips & Auth/Cinema Modals
    "🔍 자연어 스마트 문제 검색 (예: \"9월 고3 확통 문제들\", \"10월 고3 미적분\", \"6월 기하 30번\", \"정규분포\")": "🔍 Smart Problem Search (e.g. \"Sep G12 Prob & Stats\", \"Oct G12 Calculus\", \"Jun Geometry #30\", \"normal distribution\")",
    "💡 원클릭 예시 검색:": "💡 Quick Filter Examples:",
    "✨ 9월 고3 확통 문제들": "✨ Sep G12 Prob & Stats",
    "📘 10월 고3 확통 문제들": "📘 Oct G12 Prob & Stats",
    "📐 9월 고3 미적분 문제들": "📐 Sep G12 Calculus",
    "🧭 10월 고3 기하 문제들": "🧭 Oct G12 Geometry",

    // Exact Page <title> & Tooltip / Aria-Label Mappings
    "수학의 성전 3D : 16,548 디딤돌 수학 퀘스트 · mathedu": "Sanctuary of Math 3D: 16,548 Stepping-Stone Math Quests · mathedu",
    "새 문제 출제 & 퀴즈 생성 · mathedu": "Create New Math Problem & Quiz Builder · mathedu",
    "mathedu · 수학자료실 · 오프라인 전체 문제 보관함": "mathedu · Math Archive · Complete Offline Quiz Vault",
    "안티그래비티 AI 퀴즈 제작 대기실 · mathedu": "Antigravity AI Quiz Builder · mathedu",
    "[전 연도·전 학년 수학 기출 통합 플레이어] 2006~2027학년도 고1·고2·고3 16,548문항 단계별 디딤돌 · mathedu 수학자료실": "[All-Years Official Math Exam Player] 2006–2027 Grade 10–12 16,548 Step-by-Step Problems · mathedu Math Archive",
    "수학자료실(min7014.github.io) 다국어 PDF 강의 영상 스튜디오 · KO/EN 유튜브 저장 허브 | mathedu": "Math Archive (min7014.github.io) Multilingual PDF Video Studio · KO/EN YouTube Hub | mathedu",
    "대상 학년": "Target Grade",
    "시행월": "Exam Month",
    "다크 벨벳 네온 시네마 테마 전환": "Toggle Dark Velvet Neon Cinema Theme",
    "새로고침": "Refresh",
    "맨 위로": "Back to Top",
    "[2025학년도 고3 공통(수학I·II)] 기출 변형 퀴즈": "[2025 AY Grade 12 Math I·II] Adapted Exam Quiz",

    // mathedu-auth.js Modals & Buttons
    "또는 기타 로그인 방식": "Or sign in another way",
    "아이디 또는 이메일": "Username or Email",
    "비밀번호": "Password",
    "비밀번호 입력": "Enter password",
    "예: teacher 또는 이메일": "e.g. teacher or email",
    "🔑 아이디 로그인": "🔑 ID Sign In",
    "⚡ 교사 체험 계정": "⚡ Teacher Demo Account",
    "🔑 로그인하기": "🔑 Sign In",
    "🔐 mathedu 정식 회원 서비스": "🔐 mathedu Official Member Sign-In",
    "🌐 Google 공식 인증 지원": "🌐 Official Google Sign-In",
    "Google 계정으로 1초 가입 및 로그인": "1-Click Sign Up & Sign In with Google",
    "별도의 비밀번호 없이 Google 계정으로 안전하게 정식 회원가입 및 즉시 로그인이 완료됩니다.": "Sign up and sign in securely with your Google account — no separate password needed.",
    "🧑‍🎓 비회원 간편 식별": "🧑‍🎓 Quick Guest Access",
    "학습자 이름 & 간편 비밀번호": "Learner Name & Quick PIN",
    "이름과 간편 비밀번호(4자리)를 입력하시면 동일한 학습자로 인식되어, 풀이 기록이 보존되고 나중에 언제든 이어서 풀 수 있습니다.": "Enter your name and a 4-digit PIN to save and resume your problem-solving progress anytime.",
    "이름 또는 닉네임": "Name or Nickname",
    "예: 김철수": "e.g. Alex",
    "간편 비밀번호 (4자리 권장)": "Quick PIN (4+ digits)",
    "👤 학습자 확인 및 기록 불러오기": "👤 Verify Learner & Load Progress",
    "🌐 Google 공식 인증 전환": "🌐 Upgrade with Google",
    "Google 계정으로 정식 회원 전환": "Upgrade to Full Account with Google",
    "Google 계정으로 정식 회원 전환 (기록 100% 승계)": "Upgrade with Google (Keep 100% of Progress)",
    "회원 구분 선택": "Select Member Role",
    "👩‍🏫 초·중·고 수학교사": "👩‍🏫 K-12 Math Teacher",
    "🎓 학원·전문 수학강사": "🎓 Math Instructor / Tutor",
    "🔬 수학교육 연구원": "🔬 Math Education Researcher",
    "🧑‍🎓 예비교사·사범대생": "🧑‍🎓 Pre-Service Teacher",
    "🌟 학생·수학 정회원": "🌟 Student / Learner",
    "소속 학교 / 기관 (선택)": "School / Institution (Optional)",
    "📦 오프라인 전체 문제 보관함": "📦 Complete Offline Problem Vault",
    "🔒 개인정보처리방침": "🔒 Privacy Policy",
    "🗑️ 내 학습 기록 전체 삭제": "🗑️ Clear All My Progress",

    // video_board.html Cinema Stage, Active Thinking 4-Stage Workbench & 8 Neon Simulators
    "🧭 🇰🇷 [수학 분야 화두 × 오리지널 증명] 차별화된 수학교육 통찰 (1080p)": "🧭 🇰🇷 [Math Issue × Original Proof] Deep Math-Ed Insight (1080p)",
    "🌟 🇰🇷 [창의 아이디어 시네마 · Beyond PDF] 5막 스토리텔링 & 절차적 애니메이션 (1080p)": "🌟 🇰🇷 [Visual Idea Math Cinema · Beyond PDF] 5-Act Procedural Animation (1080p)",
    "🌟📱 🇰🇷 [창의 아이디어 숏폼 · Idea-#Shorts] (9:16)": "🌟📱 🇰🇷 [Visual Idea #Shorts] (9:16)",
    "❓ 🇰🇷 [질문하는 수학 수업 버전] Notice & Wonder · What-If-Not (1080p)": "❓ 🇰🇷 [Question-Asking Classroom Edition] Notice & Wonder · What-If-Not (1080p)",
    "🎬 🇰🇷 @min7014_ai v4.0 Viral Cinema 마스터 본편 (1080p)": "🎬 🇰🇷 @min7014_ai v4.0 Visual Cinema Master (1080p)",
    "📱 🇰🇷 @min7014_ai v4.0 9:16 숏폼 (#Shorts)": "📱 🇰🇷 @min7014_ai v4.0 9:16 #Shorts",
    "🇰🇷 @min7014_ai 한국어 설명영상 (YouTube)": "🇰🇷 @min7014_ai Korean Explanation (YouTube)",
    "🎬 @min7014 원본 해설 영상": "🎬 @min7014 Original Proof Video",
    "🎬 @min7014 원본 영상": "🎬 @min7014 Original Video",
    "🏛️ @min7014_ai 오리지널 PDF 정주행 마스터클래스 (YouTube 유효 시청시간 100% 적립)": "🏛️ @min7014_ai Original PDF Complete Masterclass",
    "🇰🇷 YouTube 본편 (16:9)": "🇰🇷 YouTube Full (KO 16:9)",
    "❓ 🇰🇷 질문하는 수업 버전 (1080p)": "❓ 🇰🇷 Inquiry Edition (KO 1080p)",
    "🌟 🇰🇷 창의 아이디어 시네마 (1080p)": "🌟 🇰🇷 Idea Cinema (KO 1080p)",
    "🎬 🇰🇷 v4.0 마스터 (1080p)": "🎬 🇰🇷 v4.0 Master (KO 1080p)",
    "📱 🇰🇷 일반형 숏폼 (9:16)": "📱 🇰🇷 Standard Shorts (KO 9:16)",
    "❓📱 🇰🇷 질문형 숏폼 (9:16)": "❓📱 🇰🇷 Question Shorts (KO 9:16)",
    "🧠 [능동적 수학 사고 4단계 워크벤치] 그냥 보지 말고 내 손과 머리로 먼저 재발명하세요!": "🧠 [4-Stage Active Mathematical Thinking Workbench] Reinvent the proof before watching!",
    "📐 MathLab에서 직접 움직여 보기 ↗": "📐 Explore Dynamically in MathLab ↗",
    "영상을 매끄럽게 구경만 하면": "Passively watching a smooth video creates an ",
    "'이해했다는 착각'": "'illusion of understanding'",
    "에 빠집니다. 아래": ". Click ",
    "1단계 예측": "Stage 1 Prediction",
    "과": " and ",
    "2단계 제1보조선 발상": "Stage 2 First Auxiliary Idea",
    "을 먼저 클릭한 뒤 영상을 재생해 보세요!": " before pressing Play!",
    "1️⃣ [재생 전 직관 예측 걸기]": "1️⃣ [Pre-Play Intuition Prediction] Key idea behind ",
    "의 핵심 열쇠는 어디에 있을까요?": "?",
    "🅰️ 복잡한 수식·공식 대입이 필수일 것 같다": "🅰️ Likely requires heavy algebraic substitution",
    "🅱️ 보조선·대칭·불변량 하나로 단숨에 풀릴 것 같다": "🅱️ One auxiliary line, symmetry, or invariant unlocks it",
    "🔍 특수한 경우(0·직각·중점)부터 실험해 보고 싶다": "🔍 Test a special case (0°, right angle, midpoint) first",
    "2️⃣ [사고 정지 4초 구간 · 나만의 제1발상 선택] 여러분이라면 어떤 첫 아이디어를 쓰시겠습니까?": "2️⃣ [4-Sec Contemplation Pause · Pick Your 1st Auxiliary Idea] Which strategy would you try first?",
    "🪞 대칭이동·거울점": "🪞 Reflection & Mirror Point",
    "📐 수선·직각 분해": "📐 Altitude & Right-Triangle Split",
    "📏 평행선·중점 연결": "📏 Parallel Line & Midpoint",
    "🟩 넓이 보존·등적변형": "🟩 Area-Preserving Shear",
    "🔢 나머지·차 불변량": "🔢 Difference / Remainder Invariant",
    "📈 매개변수·그래프화": "📈 Parameter & Graph View",
    "⚡": "⚡ ",
    "3단계 반례·경계 점검 (Lakatos):": "Stage 3 Boundary & Counterexample Check (Lakatos):",
    "어떤 전제 조건이 빠지면 이 정리가 깨질까요?": "Which missing hypothesis would break this theorem?",
    "4단계 조건 변형 발명 (What-If-Not):": "Stage 4 Condition Variation (What-If-Not):",
    "조건을 하나 바꾼 나만의 새 질문이나 발견을 아래에 남겨 보세요!": "Modify one condition and record your own new mathematical question below!",
    "🙋 내가 먼저 떠올린 보조선이나 '만약 조건을 바꾸면(What-If-Not)?' 아이디어를 기록하세요!": "🙋 Record your auxiliary line idea or 'What-If-Not?' variation here!",
    "💾 내 능동 사고 노트 저장": "💾 Save My Thinking Note",
    "🌟 [8대 창의 수학 네온 시뮬레이터] 슬라이더를 움직여 불변량을 직접 실험하세요!": "🌟 [8 Interactive Neon Math Simulators] Drag the sliders to test invariants live!",
    "🖨️ 교실 QR 탐구 활동지 인쇄": "🖨️ Print Classroom QR Worksheet",
    "🔔 @min7014_ai 1초 구독": "🔔 Subscribe to @min7014_ai",
    "🌳 피타고라스": "🌳 Pythagoras",
    "📐 체바·메넬라우스": "📐 Ceva & Menelaus",
    "🪐 타원 레이저": "🪐 Ellipse Optics",
    "📈 미적분·리만": "📈 Calculus & Riemann",
    "🌊 단위원 사인파": "🌊 Unit Circle Sine",
    "🌻 황금비 나선": "🌻 Golden Spiral",
    "🎲 갈톤 정규분포": "🎲 Galton Normal Bell",
    "⭕ 원주각·방멱": "⭕ Inscribed Angle",
    "🎛️ 가지 각도 / 파라미터 A": "🎛️ Branch Angle / Parameter A",
    "🎚️ 프랙탈 세대 / 분할 수 B": "🎚️ Fractal Depth / Subdivisions B",
    "🎛️ 직각삼각형 예각 (15°~75°)": "🎛️ Right-Triangle Acute Angle (15°–75°)",
    "🎚️ 프랙탈 피어나는 세대 (1~6단)": "🎚️ Fractal Branch Depth (1–6)",
    "🎛️ 내부 교점 P 좌우 이동": "🎛️ Interior Point P Horizontal Shift",
    "🎚️ 내부 교점 P 상하 이동": "🎚️ Interior Point P Vertical Shift",
    "🎛️ 레이저 광선 진행률 (0~100%)": "🎛️ Laser Ray Progress (0–100%)",
    "🎚️ 타원 이심률 스케일 (20~80)": "🎚️ Ellipse Eccentricity Scale (20–80)",
    "🎛️ 할선 Δx 수렴 위치": "🎛️ Secant Δx Convergence",
    "🎚️ 리만 적분 기둥 수 N (4~48)": "🎚️ Riemann Rectangles N (4–48)",
    "🎛️ 단위원 각도 θ (2°~75°)": "🎛️ Unit Circle Angle θ (2°–75°)",
    "🎚️ 파동 주파수 배율 (1~4배)": "🎚️ Wave Frequency Multiplier (1–4×)",
    "🎛️ 해바라기 씨앗 수 (20~144개)": "🎛️ Floret Count (20–144)",
    "🎚️ 회전각 (135°~140°)": "🎚️ Divergence Angle (135°–140°)",
    "🎛️ 낙하 구슬 진행률 (10~100%)": "🎛️ Bead Drop Progress (10–100%)",
    "🎚️ 이항분포 층수 n (4~10층)": "🎚️ Galton Rows n (4–10)",
    "🎛️ 원주 위 점 P 회전각 (15°~165°)": "🎛️ Point P Position on Circle (15°–165°)",
    "🎚️ 호 AB 중심각 크기 (40°~160°)": "🎚️ Central Angle on Arc AB (40°–160°)",
    "💡 핵심 수학 원리": "💡 Core Mathematical Principle",
    "🪜 단계별 시각 증명 디딤돌": "🪜 Step-by-Step Visual Proof Scaffolding",
    "🌐 min7014.github.io 웹페이지 ↗": "🌐 min7014.github.io Page ↗",
    "📄 원본 플립북 PDF ↗": "📄 Original Flipbook PDF ↗",
    "🧭 GeoGebra 인터랙티브 ↗": "🧭 Interactive GeoGebra ↗",
    "🖨️ 교실 배포용 QR 탐구 활동지 인쇄 (학생 30명 구독 연동)": "🖨️ Print Classroom QR Inquiry Worksheet",
    "✍️ 이 개념 탈-5지선다 기출 풀기 ➔": "✍️ Solve Constructive Exam Quizzes on This Topic ➔",
    "🎮 3D 수학 성소 보스 레이드 ➔": "🎮 3D Sanctuary Boss Raid ➔",
    "📢 이 영상+홈페이지 홍보 카드 복사": "📢 Copy Video + Website Share Card",
    "🔔 @min7014_ai 유튜브 채널 바로가기 ↗": "🔔 Visit @min7014_ai YouTube Channel ↗",

    // board/*.html SVG, Schematic, Visual Tip & Creative Solver Labels
    "🎯 최종 정답": "🎯 Final Answer",
    "다음 단계 연결 ➔": "Next Step ➔",
    "밑(Base) 통일 & 지수·로그 막대 결합 도형": "Unifying Base & Combining Exponent/Log Bars",
    "첫째 지수·로그 블록": "1st Exponent/Log Block",
    "둘째 지수·로그 블록": "2nd Exponent/Log Block",
    "결합된 전체 지수·로그 막대 (정수·유리수 완성!)": "Combined Total Exponent/Log Bar",
    "곱셈·나눗셈을 막대 길이의 덧셈·뺄셈으로 시각화": "Multiplication/Division Visualized as Bar Addition/Subtraction",
    "도식화 핵심 구조 및 수치": "Key Schematic Structure & Values",
    "① 주어진 조건 · 기하 구조": "① Given Conditions & Structure",
    "② 핵심 도형 성질 · 변환 공식": "② Core Property & Formula",
    "③ 결정적 관계식 · 수치 도출": "③ Key Equation & Value",
    "프레임별 시각적 증명 분석 (PDF & GeoGebra 탐구)": "Frame-by-Frame Visual Proof Analysis (PDF & GeoGebra)",
    "의 역수 구조로 빈틈없이 확장되는 논리적 필연성": " — logical necessity of extending seamlessly to reciprocal exponents",
    "🚨 이 문제에 이상이 있어요": "🚨 Report an Issue",
    "어떤 부분이 이상한가요? 자세히 적어주세요.": "What looks wrong? Please describe the issue.",
    "예: 보기 3번이 정답이 아닌 것 같습니다. / 문제의 조건이 모호합니다. / 계산 오류가 있습니다.": "e.g. Option #3 seems incorrect / Ambiguous condition / Calculation typo.",
    "신고 접수": "Submit Report",
    "✅ 신고가 접수되었어요. 확인 후 고칠게요!": "✅ Report received! We will verify and fix it right away.",
    "개념·증명·문제 통합 검색 (예: 피타고라스, 타원, 미적분 30번)...": "Search proofs, concepts & problems (e.g. Pythagoras, Ellipse, Calculus #30)...",
    "통합 검색어 지우기": "Clear search query",
    "통합 검색 실행": "Run global search"
  };

  // ══════════════════════════════════════════════════════════════════════════
  // Tier 3: Ordered Mathematical, Curriculum & Pedagogical Term Dictionary
  // Sorted longest-first at initialization so multi-word mathematical terms
  // always translate cleanly before shorter stems.
  // Rules: Rule 20 (Standard Math English), Rule 38 (MIN EUN GI), Rule 51.
  // ══════════════════════════════════════════════════════════════════════════
  var RAW_TERM_PAIRS = [
    // Brand & Author (Rule 38)
    ["민은기 선생님의 수학자료실", "MIN EUN GI's Math Archive"],
    ["민은기 선생님 수학자료실", "MIN EUN GI's Math Archive"],
    ["민은기 선생님", "MIN EUN GI"],
    ["민은기", "MIN EUN GI"],
    ["수학자료실 본관", "Math Archive Main Site"],
    ["수학자료실", "Math Archive"],
    ["안티그래비티 AI", "Antigravity AI"],

    // Exam & Curriculum Headers (Rule 51 compliant)
    ["전 연도·전 학년 수학 기출 통합 플레이어", "All-Years Official Math Exam Player"],
    ["대학수학능력시험", "College Entrance Exam"],
    ["전국연합학력평가", "National Academic Assessment"],
    ["한국교육과정평가원", "Curriculum & Evaluation Institute"],
    ["모의평가", "Official Mock Exam"],
    ["학력평가", "Academic Assessment"],
    ["모의고사", "Mock Exam"],
    ["대수능", "College Entrance Exam"],
    ["수능·모평", "Entrance & Mock"],
    ["수능", "Entrance Exam"],
    ["모평", "Mock Exam"],
    ["학평", "Academic Exam"],
    ["공통(수학I·II)", "Common (Math I·II)"],
    ["공통 (수학I·II)", "Common (Math I·II)"],
    ["공통(수I·II)", "Common (Math I·II)"],
    ["확률과 통계", "Probability & Statistics"],
    ["확률·통계", "Probability & Stats"],
    ["확통", "Prob & Stats"],
    ["공통수학1", "Common Math 1"],
    ["공통수학2", "Common Math 2"],
    ["공통수학", "Common Math"],
    ["수학(가형)", "Math Type Ga"],
    ["수학(나형)", "Math Type Na"],
    ["가형", "Type Ga"],
    ["나형", "Type Na"],
    ["수학II", "Math II"],
    ["수학I", "Math I"],
    ["미적분학", "Calculus"],
    ["미적분", "Calculus"],
    ["단답형", "Short Answer"],
    ["객관식", "Multiple Choice"],
    ["주관식", "Constructed Response"],
    ["기출문제", "Past Exam Problem"],
    ["기출문항", "Exam Problem"],
    ["기출", "Exam"],

    // 16 Curriculum Domains & Sub-domains
    ["유클리드 평면기하", "Euclidean Plane Geometry"],
    ["다항식·방정식·수체계", "Polynomials, Equations & Number Systems"],
    ["미분·도함수", "Differentiation & Derivatives"],
    ["이차곡선·원뿔곡선", "Conic Sections"],
    ["이차곡선·단델린", "Conic Sections & Dandelin"],
    ["벡터·공간도형", "Vectors & Solid Geometry"],
    ["지수·로그함수", "Exponential & Logarithmic Functions"],
    ["지수·로그", "Exponents & Logarithms"],
    ["함수의 극한과 연속", "Limits & Continuity of Functions"],
    ["극한과 연속", "Limits & Continuity"],
    ["해석기하·원의 방정식", "Analytic Geometry & Circles"],
    ["삼각비·삼각함수", "Trigonometry & Trigonometric Functions"],
    ["함수·집합·그래프", "Functions, Sets & Graphs"],
    ["기하 변환·대칭", "Geometric Transformations & Symmetry"],
    ["방정식·부등식", "Equations & Inequalities"],
    ["방정식과 부등식", "Equations & Inequalities"],
    ["적분·구분구적법", "Integration & Mensuration by Parts"],
    ["수열·시그마", "Sequences & Sigma Notation"],
    ["내용순 배열", "Topic Tree"],

    // Geometry & Conic Sections (Rule 20 International Standard Mathematical English)
    ["단델린의 구", "Dandelin Spheres"],
    ["단델린 구", "Dandelin Spheres"],
    ["피타고라스 정리", "Pythagorean Theorem"],
    ["피타고라스의 정리", "Pythagorean Theorem"],
    ["피타고라스 나무", "Pythagoras Tree"],
    ["피타고라스", "Pythagoras"],
    ["체바의 정리", "Ceva's Theorem"],
    ["메넬라우스의 정리", "Menelaus' Theorem"],
    ["메넬라우스 정리", "Menelaus' Theorem"],
    ["톨레미의 정리", "Ptolemy's Theorem"],
    ["비비아니 정리", "Viviani's Theorem"],
    ["스튜어트 정리", "Stewart's Theorem"],
    ["파푸스의 중선정리", "Pappus's Centroid Theorem"],
    ["중선정리", "Apollonius's Theorem"],
    ["아폴로니우스의 원", "Circle of Apollonius"],
    ["삼수선의 정리", "Theorem of Three Perpendiculars"],
    ["꼬인 위치", "Skew Lines"],
    ["엇각", "Alternate Interior Angles"],
    ["동위각", "Corresponding Angles"],
    ["사인법칙", "Law of Sines"],
    ["코사인법칙", "Law of Cosines"],
    ["원주각과 중심각", "Inscribed & Central Angles"],
    ["원주각", "Inscribed Angle"],
    ["중심각", "Central Angle"],
    ["내접사각형", "Cyclic Quadrilateral"],
    ["원에 내접하는 사각형", "Cyclic Quadrilateral"],
    ["등변사다리꼴", "Isosceles Trapezoid"],
    ["사다리꼴", "Trapezoid"],
    ["평행사변형", "Parallelogram"],
    ["직각이등변삼각형", "Right Isosceles Triangle"],
    ["직각삼각형", "Right Triangle"],
    ["이등변삼각형", "Isosceles Triangle"],
    ["정삼각형", "Equilateral Triangle"],
    ["정사각형", "Square"],
    ["직사각형", "Rectangle"],
    ["마름모", "Rhombus"],
    ["정오각형", "Regular Pentagon"],
    ["정육각형", "Regular Hexagon"],
    ["정칠각형", "Regular Heptagon"],
    ["정팔각형", "Regular Octagon"],
    ["정다각형", "Regular Polygon"],
    ["삼각형", "Triangle"],
    ["사각형", "Quadrilateral"],
    ["다각형", "Polygon"],
    ["정사면체", "Regular Tetrahedron"],
    ["정육면체", "Cube"],
    ["정팔면체", "Regular Octahedron"],
    ["정십이면체", "Regular Dodecahedron"],
    ["정이십면체", "Regular Icosahedron"],
    ["직육면체", "Rectangular Prism"],
    ["원기둥", "Cylinder"],
    ["원뿔곡선", "Conic Section"],
    ["이차곡선", "Conic Section"],
    ["원뿔", "Cone"],
    ["포물선", "Parabola"],
    ["쌍곡선", "Hyperbola"],
    ["타원", "Ellipse"],
    ["사이클로이드", "Cycloid"],
    ["수직이등분선", "Perpendicular Bisector"],
    ["각의 이등분선", "Angle Bisector"],
    ["이등분선", "Bisector"],
    ["수선의 발", "Foot of Perpendicular"],
    ["보조선", "Auxiliary Line"],
    ["점근선", "Asymptote"],
    ["접선", "Tangent Line"],
    ["할선", "Secant Line"],
    ["법선", "Normal Line"],
    ["준선", "Directrix"],
    ["초점", "Focus"],
    ["꼭짓점", "Vertex"],
    ["무게중심", "Centroid"],
    ["외접원", "Circumcircle"],
    ["내접원", "Inscribed Circle"],
    ["외심", "Circumcenter"],
    ["내심", "Incenter"],
    ["수심", "Orthocenter"],
    ["방심", "Excenter"],
    ["반지름", "Radius"],
    ["지름", "Diameter"],
    ["빗변", "Hypotenuse"],
    ["밑변", "Base"],
    ["대각선", "Diagonal"],
    ["교점", "Intersection"],
    ["접점", "Point of Tangency"],
    ["중점", "Midpoint"],
    ["내분점", "Internal Division Point"],
    ["외분점", "External Division Point"],
    ["정사영", "Orthogonal Projection"],
    ["이면각", "Dihedral Angle"],
    ["평면벡터", "Plane Vector"],
    ["공간벡터", "Space Vector"],
    ["위치벡터", "Position Vector"],
    ["법선벡터", "Normal Vector"],
    ["방향벡터", "Direction Vector"],
    ["단위벡터", "Unit Vector"],
    ["공간도형", "Solid Geometry"],
    ["공간좌표", "Space Coordinates"],
    ["좌표평면", "Coordinate Plane"],
    ["수직선", "Number Line"],
    ["대칭이동", "Reflection Symmetry"],
    ["평행이동", "Translation"],
    ["회전이동", "Rotation"],
    ["등적변형", "Area-Preserving Shear"],
    ["황금비", "Golden Ratio"],
    ["황금각", "Golden Angle"],
    ["피보나치", "Fibonacci"],
    ["프랙탈", "Fractal"],
    ["내적", "Dot Product"],
    ["벡터", "Vector"],
    ["합동", "Congruence"],
    ["닮음비", "Similarity Ratio"],
    ["닮음", "Similarity"],
    ["작도", "Geometric Construction"],

    // Calculus & Analysis
    ["정적분으로 정의된 함수", "Function Defined by Definite Integral"],
    ["미적분의 기본정리", "Fundamental Theorem of Calculus"],
    ["평균값 정리", "Mean Value Theorem"],
    ["롤의 정리", "Rolle's Theorem"],
    ["사이값 정리", "Intermediate Value Theorem"],
    ["샌드위치 정리", "Squeeze Theorem"],
    ["구분구적법", "Mensuration by Parts"],
    ["부분적분법", "Integration by Parts"],
    ["부분적분", "Integration by Parts"],
    ["치환적분법", "Integration by Substitution"],
    ["치환적분", "Substitution Integration"],
    ["정적분", "Definite Integral"],
    ["부정적분", "Indefinite Integral"],
    ["미분가능성", "Differentiability"],
    ["미분가능", "Differentiable"],
    ["미분계수", "Derivative at a Point"],
    ["순간변화율", "Instantaneous Rate of Change"],
    ["평균변화율", "Average Rate of Change"],
    ["이계도함수", "Second Derivative"],
    ["도함수", "Derivative"],
    ["합성함수", "Composite Function"],
    ["역함수", "Inverse Function"],
    ["삼차함수", "Cubic Function"],
    ["사차함수", "Quartic Function"],
    ["이차함수", "Quadratic Function"],
    ["일차함수", "Linear Function"],
    ["다항함수", "Polynomial Function"],
    ["유리함수", "Rational Function"],
    ["무리함수", "Radical Function"],
    ["지수함수", "Exponential Function"],
    ["로그함수", "Logarithmic Function"],
    ["삼각함수", "Trigonometric Function"],
    ["초월함수", "Transcendental Function"],
    ["연속함수", "Continuous Function"],
    ["우함수", "Even Function"],
    ["기함수", "Odd Function"],
    ["주기함수", "Periodic Function"],
    ["변곡점", "Inflection Point"],
    ["극댓값", "Local Maximum"],
    ["극솟값", "Local Minimum"],
    ["극대", "Local Max"],
    ["극소", "Local Min"],
    ["극값", "Extremum"],
    ["최댓값", "Maximum Value"],
    ["최솟값", "Minimum Value"],
    ["최대·최소", "Maxima & Minima"],
    ["좌극한", "Left-Hand Limit"],
    ["우극한", "Right-Hand Limit"],
    ["등비급수", "Geometric Series"],
    ["무한급수", "Infinite Series"],
    ["급수", "Series"],
    ["수렴", "Convergence"],
    ["발산", "Divergence"],
    ["연속성", "Continuity"],
    ["연속", "Continuity"],
    ["극한값", "Limit Value"],
    ["극한", "Limit"],
    ["미분법", "Differentiation"],
    ["적분법", "Integration"],
    ["미분", "Differentiation"],
    ["적분", "Integration"],
    ["기울기", "Slope"],
    ["절편", "Intercept"],

    // Algebra, Sequences, Exponents & Logs
    ["산술·기하평균", "AM-GM Inequality"],
    ["산술기하평균", "AM-GM Inequality"],
    ["코시-슈바르츠 부등식", "Cauchy-Schwarz Inequality"],
    ["근과 계수의 관계", "Vieta's Formulas"],
    ["나머지정리", "Polynomial Remainder Theorem"],
    ["인수정리", "Factor Theorem"],
    ["인수분해", "Factorization"],
    ["곱셈공식", "Polynomial Expansion"],
    ["이항정리", "Binomial Theorem"],
    ["수학적 귀납법", "Mathematical Induction"],
    ["귀납적 정의", "Recursive Definition"],
    ["점화식", "Recurrence Relation"],
    ["등차수열", "Arithmetic Sequence"],
    ["등비수열", "Geometric Sequence"],
    ["부분분수", "Partial Fractions"],
    ["일반항", "General Term"],
    ["공차", "Common Difference"],
    ["공비", "Common Ratio"],
    ["첫째항", "First Term"],
    ["거듭제곱근", "nth Root"],
    ["거듭제곱", "Power"],
    ["상용로그", "Common Logarithm"],
    ["자연로그", "Natural Logarithm"],
    ["지수법칙", "Laws of Exponents"],
    ["진수조건", "Logarithm Argument Condition"],
    ["이차방정식", "Quadratic Equation"],
    ["삼차방정식", "Cubic Equation"],
    ["연립방정식", "System of Equations"],
    ["절댓값", "Absolute Value"],
    ["판별식", "Discriminant"],
    ["복소수", "Complex Number"],
    ["켤레복소수", "Complex Conjugate"],
    ["유리수", "Rational Number"],
    ["무리수", "Irrational Number"],
    ["자연수", "Natural Number"],
    ["실수", "Real Number"],
    ["정수", "Integer"],
    ["소인수분해", "Prime Factorization"],
    ["다항식", "Polynomial"],
    ["항등식", "Identity"],
    ["방정식", "Equation"],
    ["부등식", "Inequality"],
    ["수열", "Sequence"],
    ["집합", "Set"],
    ["명제", "Proposition"],
    ["대우", "Contrapositive"],
    ["필요충분조건", "Necessary & Sufficient Condition"],
    ["충분조건", "Sufficient Condition"],
    ["필요조건", "Necessary Condition"],
    ["반례", "Counterexample"],

    // Probability & Statistics
    ["같은 것이 있는 순열", "Permutations with Repetition"],
    ["원순열", "Circular Permutation"],
    ["중복순열", "Permutation with Replacement"],
    ["중복조합", "Combination with Repetition"],
    ["경우의 수", "Counting & Combinatorics"],
    ["조건부확률", "Conditional Probability"],
    ["독립시행", "Independent Trials"],
    ["배반사건", "Mutually Exclusive Events"],
    ["여사건", "Complementary Event"],
    ["표본평균", "Sample Mean"],
    ["모평균", "Population Mean"],
    ["표준정규분포", "Standard Normal Distribution"],
    ["정규분포", "Normal Distribution"],
    ["이항분포", "Binomial Distribution"],
    ["확률밀도함수", "Probability Density Function"],
    ["확률질량함수", "Probability Mass Function"],
    ["확률변수", "Random Variable"],
    ["신뢰구간", "Confidence Interval"],
    ["통계적 추정", "Statistical Estimation"],
    ["표준편차", "Standard Deviation"],
    ["분산", "Variance"],
    ["기댓값", "Expected Value"],
    ["순열", "Permutation"],
    ["조합", "Combination"],
    ["확률", "Probability"],
    ["통계", "Statistics"],

    // Pedagogy, UI & Common Korean Phrases
    ["초등 눈높이 디딤돌", "Elementary-to-Advanced Scaffolding"],
    ["단계별 빌드업", "Step-by-Step Buildup"],
    ["단델린·기하 연계", "Dandelin & Visual Geometry"],
    ["시각적 수학 증명", "Visual Math Proof"],
    ["시각적 증명", "Visual Proof"],
    ["시각 증명", "Visual Proof"],
    ["동적 기하", "Dynamic Geometry"],
    ["탈-5지선다", "Constructive (No Multiple-Choice)"],
    ["창의적 구성", "Creative Construction"],
    ["도식화 풀이 흐름도", "Schematic Solution Flowchart"],
    ["오개념 백신", "Misconception Vaccine"],
    ["오답노트", "Review Vault"],
    ["즐겨찾기", "Bookmarks"],
    ["디딤돌", "Stepping-Stone"],
    ["킬러 문항", "Advanced Challenge"],
    ["킬러", "Advanced"],
    ["고난도", "High-Difficulty"],
    ["주요문항", "Key Problem"],
    ["넓이 보존", "Area Invariance"],
    ["넓이 분할", "Area Partition"],
    ["광학적 성질", "Optical Property"],
    ["빛 반사", "Light Reflection"],
    ["최단 경로", "Shortest Path"],
    ["불변량", "Invariant"],
    ["실전 보조선", "Practical Auxiliary Line"],
    ["문제 풀기", "Solve Quiz"],
    ["바로 풀기", "Solve Now"],
    ["이어풀기", "Resume"],
    ["다시풀기", "Re-solve"],
    ["풀기", "Solve"],
    ["넓이", "Area"],
    ["부피", "Volume"],
    ["길이", "Length"],
    ["높이", "Height"],
    ["거리", "Distance"],
    ["각도", "Angle"],
    ["속도", "Velocity"],
    ["가속도", "Acceleration"],
    ["함수", "Function"],
    ["그래프", "Graph"],
    ["증명", "Proof"],
    ["정리", "Theorem"],
    ["공식", "Formula"],
    ["성질", "Property"],
    ["원리", "Principle"],
    ["정의", "Definition"],
    ["활용", "Applications"],
    ["계산", "Calculation"],
    ["추론", "Reasoning"],
    ["탐구", "Inquiry"],
    ["실험실", "Lab"],
    ["스튜디오", "Studio"],
    ["게시판", "Board"],
    ["아카이브", "Archive"],
    ["전체보기", "View All"],
    ["전체", "All"],
    ["검색", "Search"],
    ["초기화", "Reset"],
    ["닫기", "Close"],
    ["열기", "Open"],
    ["복사", "Copy"],
    ["공유", "Share"],
    ["구독", "Subscribe"],
    ["완료", "Completed"],
    ["진행중", "In Progress"],
    ["방금 전", "Just now"],
    ["그림으로 이해하는 시각적 도형·개념 다이어그램", "Visual Concept & Geometric Diagram"],
    ["한눈에 보는 도식화 풀이 흐름도", "Schematic Solution Flowchart"],
    ["문제 분석 및 핵심 출제 의도", "Problem Analysis & Core Objective"],
    ["단계별 상세 풀이 전개", "Step-by-Step Solution"],
    ["정답 도출 및 실전 점검 포인트", "Final Answer & Verification"],
    ["수학 특강·공학도구", "Special Math Lectures & Tools"],
    ["비복원 추출", "Sampling Without Replacement"],
    ["복원 추출", "Sampling With Replacement"],
    ["지수함수와 로그함수", "Exponential & Logarithmic Functions"],
    ["지수와 로그", "Exponents & Logarithms"],
    ["지수의 확장", "Extension of Exponents"],
    ["수체계", "Number System"],
    ["사칙연산", "Four Operations"],
    ["유한소수", "Terminating Decimal"],
    ["무한소수", "Non-terminating Decimal"],
    ["순환소수", "Repeating Decimal"],
    ["발판곡면", "Pedal Surface"],
    ["스트링 아트", "String Art"],
    ["포락선", "Envelope"],
    ["코흐 눈송이", "Koch Snowflake"],
    ["코흐 곡선", "Koch Curve"],
    ["페아노 곡선", "Peano Curve"],
    ["장미 곡선", "Rose Curve"],
    ["중점연결정리", "Midpoint Connector Theorem"],
    ["중점연결", "Midpoint Connector"],
    ["자유학습", "Learner"],
    ["개정 분류", "Curriculum"],
    ["출발 조건", "Given Conditions"],
    ["단원 원리", "Unit Principle"],
    ["목표값", "Target Value"],
    ["결과값", "Result"],
    ["구구단", "Multiplication"],
    ["주파수", "Frequency"],
    ["진폭", "Amplitude"],
    ["대칭축", "Symmetry Axis"],
    ["삼차항", "Cubic Term"],
    ["이차항", "Quadratic Term"],
    ["일차항", "Linear Term"],
    ["상수항", "Constant Term"],
    ["계수", "Coefficient"],
    ["폭", "Width"],
    ["주머니", "Urn"],
    ["매듭", "Knot"],
    ["반원", "Semicircle"],
    ["사면체", "Tetrahedron"],
    ["환의 넓이", "Annular Area"],
    ["어려운", "Challenging"],
    ["페이지", "Slide"],
    ["역수 구조", "Reciprocal Structure"],
    ["역수", "Reciprocal"],
    ["논리적 필연성", "Logical Necessity"],
    ["필연성", "Necessity"],
    ["홀·짝성", "Parity (Odd/Even)"],
    ["실근", "Real Root"],
    ["허근", "Imaginary Root"],
    ["중근", "Double Root"],
    ["밑", "Base"],
    ["지수", "Exponent"],
    ["진수", "Argument"],
    ["부호", "Sign"],
    ["개수", "Number"],
    ["확장", "Extension"],
    ["보존", "Preservation"],
    ["중심극한정리", "Central Limit Theorem"],
    ["가우스", "Gaussian"],
    ["종 곡선", "Bell Curve"],
    ["단위원", "Unit Circle"],
    ["이심률", "Eccentricity"],
    ["방멱", "Power of a Point"],
  ];

  // Sort longest Korean phrase first so longer terms win over substrings
  var TERM_PAIRS = RAW_TERM_PAIRS.slice().sort(function(a, b) {
    return b[0].length - a[0].length;
  });

  // Bidirectional English -> Korean search expansion map so users in EN mode
  // can type English math keywords into search boxes and match Korean corpus!
  var EN_TO_KO_SEARCH_MAP = {
    "pythagoras": "피타고라스",
    "pythagorean": "피타고라스",
    "dandelin": "단델린",
    "ellipse": "타원",
    "parabola": "포물선",
    "hyperbola": "쌍곡선",
    "conic": "이차곡선",
    "conics": "이차곡선",
    "circle": "원",
    "triangle": "삼각형",
    "equilateral": "정삼각형",
    "isosceles": "이등변삼각형",
    "heptagon": "정칠각형",
    "polygon": "다각형",
    "ceva": "체바",
    "menelaus": "메넬라우스",
    "ptolemy": "톨레미",
    "viviani": "비비아니",
    "inscribed": "원주각",
    "tangent": "접선",
    "secant": "할선",
    "asymptote": "점근선",
    "focus": "초점",
    "directrix": "준선",
    "vector": "벡터",
    "vectors": "벡터",
    "dot product": "내적",
    "projection": "정사영",
    "derivative": "미분",
    "differentiation": "미분",
    "differentiable": "미분가능",
    "integral": "적분",
    "integration": "적분",
    "quadrature": "구분구적",
    "limit": "극한",
    "limits": "극한",
    "continuity": "연속",
    "continuous": "연속",
    "inflection": "변곡점",
    "extremum": "극값",
    "maximum": "최댓값",
    "minimum": "최솟값",
    "sequence": "수열",
    "sequences": "수열",
    "arithmetic": "등차수열",
    "geometric": "등비수열",
    "series": "급수",
    "sigma": "시그마",
    "induction": "귀납",
    "recurrence": "점화식",
    "exponent": "지수",
    "exponential": "지수함수",
    "logarithm": "로그",
    "log": "로그",
    "trigonometry": "삼각함수",
    "sine": "사인",
    "cosine": "코사인",
    "polynomial": "다항식",
    "quadratic": "이차함수",
    "cubic": "삼차함수",
    "quartic": "사차함수",
    "inverse": "역함수",
    "composite": "합성함수",
    "equation": "방정식",
    "inequality": "부등식",
    "probability": "확률",
    "conditional": "조건부확률",
    "normal": "정규분포",
    "binomial": "이항",
    "permutation": "순열",
    "combination": "조합",
    "confidence": "신뢰구간",
    "statistics": "통계",
    "construction": "작도",
    "golden": "황금비",
    "fractal": "프랙탈",
    "symmetry": "대칭"
  };

  function expandEnglishSearchQuery(rawQ) {
    var q = String(rawQ || '').trim();
    if (!q || /[가-힣]/.test(q)) return q;
    var low = q.toLowerCase();
    // Check direct keyword map while keeping numbers/years intact
    if (EN_TO_KO_SEARCH_MAP[low]) return EN_TO_KO_SEARCH_MAP[low];
    var tokens = low.split(/[\s,/#]+/).filter(Boolean);
    var mapped = [];
    var changed = false;
    var monthEnMap = {
      "nov": "11월", "november": "11월", "sep": "9월", "sept": "9월", "september": "9월",
      "jun": "6월", "june": "6월", "oct": "10월", "october": "10월",
      "jul": "7월", "july": "7월", "may": "5월", "apr": "4월", "april": "4월", "mar": "3월", "march": "3월"
    };
    for (var i = 0; i < tokens.length; i++) {
      var tk = tokens[i];
      if (monthEnMap[tk]) { mapped.push(monthEnMap[tk]); changed = true; }
      else if (tk === 'g12' || tk === 'grade12') { mapped.push('고3'); changed = true; }
      else if (tk === 'g11' || tk === 'grade11') { mapped.push('고2'); changed = true; }
      else if (tk === 'g10' || tk === 'grade10') { mapped.push('고1'); changed = true; }
      else if (EN_TO_KO_SEARCH_MAP[tk]) { mapped.push(EN_TO_KO_SEARCH_MAP[tk]); changed = true; }
      else { mapped.push(tk); }
    }
    return changed ? mapped.join(' ') : q;
  }

  /**
   * Translates any Korean UI / curriculum / mathematics string into clean English
   * while strictly protecting inline & display LaTeX ($...$, \(...\), \[...\]).
   */
  function toEnglishMathText(rawStr) {
    if (!rawStr || typeof rawStr !== 'string') return rawStr;
    if (!/[가-힣]/.test(rawStr)) return rawStr;

    var mWs = rawStr.match(/^(\s*)([\s\S]*?)(\s*)$/);
    var lead = mWs ? mWs[1] : '';
    var core = mWs ? mWs[2] : rawStr;
    var trail = mWs ? mWs[3] : '';
    if (!core) return rawStr;

    // 1. Exact Phrase Lookup
    if (EXACT_UI_MAP[core]) {
      return lead + EXACT_UI_MAP[core] + trail;
    }
    var normCore = core.replace(/\s+/g, ' ');
    if (EXACT_UI_MAP[normCore]) {
      return lead + EXACT_UI_MAP[normCore] + trail;
    }

    // 1.5. Balanced Trailing (English Title) Extractor for Archive Topics
    // e.g. "[유클리드 평면기하] 정칠각형 매듭(Regular Heptagonal Knot)" -> "[Euclidean Plane Geometry] Regular Heptagonal Knot"
    if (normCore.charAt(normCore.length - 1) === ')') {
      var leadBracketEn = '';
      var restTopic = normCore;
      var mBr = restTopic.match(/^\[([^\]]+)\]\s*([\s\S]+)$/);
      if (mBr && /[가-힣]/.test(mBr[1])) {
        leadBracketEn = '[' + toEnglishMathText(mBr[1]) + '] ';
        restTopic = mBr[2];
      }
      var depth = 0;
      var inMath = false;
      var openPos = -1;
      for (var ci = restTopic.length - 1; ci >= 0; ci--) {
        var ch = restTopic.charAt(ci);
        if (ch === '$') inMath = !inMath;
        if (!inMath) {
          if (ch === ')') depth++;
          else if (ch === '(') {
            depth--;
            if (depth === 0) { openPos = ci; break; }
          }
        }
      }
      if (openPos > 0) {
        var koBefore = restTopic.slice(0, openPos).trim();
        var enInside = restTopic.slice(openPos + 1, -1).trim();
        var enNoMath = enInside.replace(/\$[^$]*\$/g, ' ');
        if (/[가-힣]/.test(koBefore) && !/[가-힣]/.test(enInside) && /[a-z]{2,}/.test(enNoMath)) {
          var wordCount = enNoMath.trim().split(/\s+/).filter(Boolean).length;
          if (wordCount >= 2 || enNoMath.trim().length >= 8) {
            return lead + leadBracketEn + enInside + trail;
          }
        }
      }
    }

    // 2. Mask LaTeX Math Segments ($...$, $$...$$, \(...\), \[...\]) while translating Korean blank labels inside \text{...}
    var mathVault = [];
    var s = normCore.replace(/(\$\$[\s\S]*?\$\$|\$[^$\n]+\$|\\\([\s\S]*?\\\)|\\\[[\s\S]*?\\\])/g, function(match) {
      var cleanedMath = match
        .replace(/\\text\s*\{\s*\(가\)\s*\}/g, '\\text{(A)}')
        .replace(/\\text\s*\{\s*\(나\)\s*\}/g, '\\text{(B)}')
        .replace(/\\text\s*\{\s*\(다\)\s*\}/g, '\\text{(C)}')
        .replace(/\\text\s*\{\s*\(라\)\s*\}/g, '\\text{(D)}')
        .replace(/\\text\s*\{\s*가\s*\}/g, '\\text{A}')
        .replace(/\\text\s*\{\s*나\s*\}/g, '\\text{B}')
        .replace(/\\text\s*\{\s*다\s*\}/g, '\\text{C}')
        .replace(/\\text\s*\{\s*라\s*\}/g, '\\text{D}')
        .replace(/\(가\)/g, '(A)')
        .replace(/\(나\)/g, '(B)')
        .replace(/\(다\)/g, '(C)')
        .replace(/\(라\)/g, '(D)')
        .replace(/\[가\]/g, '[A]')
        .replace(/\[나\]/g, '[B]')
        .replace(/\[다\]/g, '[C]')
        .replace(/일정/g, 'const')
        .replace(/높이/g, 'height')
        .replace(/넓이/g, 'area')
        .replace(/밑변/g, 'base')
        .replace(/최대/g, 'max')
        .replace(/최소/g, 'min');
      var idx = mathVault.length;
      mathVault.push(cleanedMath);
      return '__MTH_' + idx + '__';
    });

    if (!/[가-힣]/.test(s)) {
      s = s.replace(/__MTH_(\d+)__/g, function(_, idx) { return mathVault[parseInt(idx, 10)] || ''; });
      return lead + s + trail;
    }

    // 3. Structured Dynamic Patterns (Exam Titles, Counters, Badges, Pagination, Simulators)
    s = s
      // Korean Blank Labels & Exam Point Badges BEFORE generic word replacement
      .replace(/\(가\)/g, '(A)')
      .replace(/\(나\)/g, '(B)')
      .replace(/\(다\)/g, '(C)')
      .replace(/\(라\)/g, '(D)')
      .replace(/\[\s*(\d+)\s*점\s*\]/g, '[$1 pts]')
      .replace(/(\d+)\s*점짜리/g, '$1-point')
      .replace(/(\d+)\s*점(?=\s|$|[)\].,·])/g, '$1 pts')
      .replace(/🎯\s*최종\s*결론\s*:\s*/g, '🎯 Conclusion: ')
      .replace(/정답\s*:\s*/g, 'Answer: ')
      // Video Board Neon Simulator Readouts
      .replace(/★\s*각도\s*([\d.]+)°\s*·\s*(\d+)세대\((\d+)개\s*가지\):\s*왼쪽\(([\d.]+)\)\s*\+\s*오른쪽\(([\d.]+)\)\s*=\s*뿌리\s*넓이\s*([\d.]+)\s*완벽\s*보존!/g, '★ Angle $1° · Depth $2 ($3 branches): Left ($4) + Right ($5) = Root Area $6 (100% Preserved!)')
      .replace(/★\s*체바\s*넓이\s*밸런스:\s*P\(([^)]+)\)\s*이동\s*무관\s*\(AF\/FB\)×\(BD\/DC\)×\(CE\/EA\)\s*=\s*1\.0000\s*불변!/g, '★ Ceva Area Balance: For any P($1), (AF/FB)×(BD/DC)×(CE/EA) = 1.0000 Invariant!')
      .replace(/★\s*타원\s*광학\s*불변량:\s*12갈래\s*레이저\s*경로\s*합\s*\|PF1\|\s*\+\s*\|PF2\|\s*=\s*2a\s*일정\s*→\s*제2초점\s*F2\s*동시\s*도착!\s*\((\d+)%\)/g, '★ Ellipse Optical Invariant: All 12 rays keep |PF1| + |PF2| = 2a → Simultaneous Focus at F2! ($1%)')
      .replace(/★\s*미적분\s*극한\s*실험:\s*리만\s*분할\s*N\s*=\s*(\d+)개\s*·\s*Δx\s*=\s*([\d.]+)\s*→\s*0\s*수렴\s*시\s*정적분\s*넓이\s*일치!/g, '★ Calculus Limit Lab: Riemann N = $1 · As Δx = $2 → 0, Sum Converges to Definite Integral!')
      .replace(/\(θ→0\s*수렴:\s*1\.0000!\)/g, '(Converges to 1.0000 as θ→0!)')
      .replace(/★\s*황금비\s*φ\s*=\s*1\.618034\s*·\s*회전각\s*([\d.]+)°\s*\(황금각\s*137\.5°에서\s*(\d+)개\s*씨앗\s*무충돌\s*나선\s*배열!\)/g, '★ Golden Ratio φ = 1.618034 · Angle $1° (Collision-free spiral of $2 seeds at 137.5°!)')
      .replace(/★\s*갈톤\s*보드\s*중심극한정리:\s*(\d+)단\s*이항분포\s*B\((\d+),\s*0\.5\)\s*→\s*가우스\s*정규분포\s*종\s*곡선\s*100%\s*수렴!/g, '★ Galton Board CLT: $1-Row Binomial B($2, 0.5) → Converges to Gaussian Normal Curve!')
      .replace(/★\s*원주각\s*불변량:\s*점\s*P가\s*원주\s*위\s*어디로\s*움직여도\(각\s*(\d+)°\)\s*원주각\s*∠APB\s*=\s*([\d.]+)°\s*\(중심각\s*(\d+)°의\s*절반!\)/g, '★ Inscribed Angle Invariant: Wherever P moves ($1°), ∠APB = $2° (Half of Central Angle $3°!)')
      .replace(/★\s*CORE\s*INVARIANT:\s*모든\s*세대의\s*정사각형\s*넓이\s*합\s*=\s*뿌리\s*정사각형\(([\d.]+)\)\s*100%\s*보존!/g, '★ CORE INVARIANT: Total Area of All Generation Squares = Root Square ($1) 100% Preserved!')
      // Video Board & Studio Dynamic Status Lines
      .replace(/검색\s*결과\s*([\d,]+)개\s*자료\s*\(페이지\s*(\d+)\s*\/\s*(\d+)\)/g, '$1 Topics Found (Page $2 / $3)')
      .replace(/전체\s*([\d,]+)개\s*중\s*([\d,~\-]+)번째\s*자료\s*표시/g, 'Showing $2 of $1 Topics')
      .replace(/🤖\s*자연어\s*검색\s*결과:\s*"([^"]*)"\s*조건에\s*일치하는\s*오프라인\s*문제\s*([\d,]+)건이\s*검색되었습니다\./g, '🤖 Smart Search: Found $2 offline quizzes matching "$1".')
      .replace(/자유학습#([A-Za-z0-9]+)/g, 'Learner#$1')
      .replace(/(\d+)번\s*\((\d+)점\)/g, '#$1 ($2 pts)')
      .replace(/정답\s*(\d+)번/g, 'Answer #$1')
      .replace(/(\d+)점\s*기출문항/g, '$1-pt Exam Problem')
      .replace(/(\d+)페이지입니다\./g, 'Slide $1.')
      .replace(/(\d+)페이지/g, 'Slide $1')
      .replace(/초등\s*눈높이\s*디딤돌\s*\((\d+~\d+)단계\)/g, 'Step-by-Step Scaffolding (Steps $1)')
      .replace(/\[디딤돌\s*(\d+~\d+)단계\s*연결\]/g, '[Scaffolding Steps $1]')
      // Pagination & Counters
      .replace(/➕\s*다음\s*(\d+)문항\s*더보기\s*\(현재\s*([\d,]+)\s*\/\s*검색\s*결과\s*([\d,]+)문항\)/g, '➕ Load Next $1 Problems (Showing $2 of $3)')
      .replace(/정확\s*일치\s*([\d,]+)문항/g, '$1 Exact Matches')
      .replace(/\(\+\s*연관\s*([\d,]+)문항\)/g, '(+ $1 Related)')
      .replace(/진행율\s*(\d+)%\s*\(([\d\/]+)\)/g, 'Progress $1% ($2)')
      .replace(/전체\s*\(([\d,\-]+)\)/g, 'All ($1)')
      .replace(/오답노트\s*\(([\d,]+)\)/g, 'Review Vault ($1)')
      .replace(/즐겨찾기\s*\(([\d,]+)\)/g, 'Bookmarks ($1)')
      .replace(/(\d+)\s*\/\s*(\d+)\s*완료/g, '$1 / $2 Completed')
      .replace(/★\s*(\d+)\s*\/\s*(\d+)\s*획득/g, '★ $1 / $2 Collected')
      .replace(/(\d+)건\s*AI\s*제작\s*중/g, '$1 Being Crafted by AI')
      .replace(/전체\s*제작\s*완료\s*\((\d+)건\)/g, 'All Crafted ($1)')
      .replace(/전체\s*([\d,]+)개\s*표시\s*중/g, 'Showing All $1 Items')
      .replace(/검색\s*결과\s*([\d,]+)개/g, '$1 Results Found')
      .replace(/(\d+)개\s*주제\s*×\s*7대\s*채널\s*=\s*(\d+)종\s*맞춤\s*홍보\s*키트\s*준비\s*완료/g, '$1 Topics × 7 Channels = $2 Ready Share Kits')
      .replace(/(\d+)개\s*주제\s*×\s*7대\s*채널\s*=\s*(\d+)종\s*홍보\s*키트\s*자동\s*생성\s*완료/g, '$1 Topics × 7 Channels = $2 Auto-Generated Share Kits')
      .replace(/🟢\s*24\/7\s*자가\s*진화\s*중\s*·\s*v4\.0\s*영상\s*([\d,]+)편\s*·\s*교육모듈\s*확장\s*중/g, '🟢 24/7 Auto-Evolving · $1 v4.0 Videos · Expanding Modules')
      .replace(/📅\s*(\d{4}-\d{2}-\d{2})\s*오늘의\s*유레카/g, "📅 $1 Today's Eureka")
      .replace(/(\d+)초\s*전/g, '$1s ago')
      .replace(/(\d+)분\s*전/g, '$1m ago')
      .replace(/(\d+)시간\s*전/g, '$1h ago')
      .replace(/(\d+)일\s*전/g, '$1d ago')
      // Exam Dates, Years, Months, Grades, Question Numbers
      .replace(/(\d{4})\s*학년도\s*이전/g, 'Before AY $1')
      .replace(/(\d{4})\s*학년도/g, '$1 AY')
      .replace(/(\d{2})\s*학년도/g, '20$1 AY')
      .replace(/(\d{4})\s*년/g, '$1')
      .replace(/11월\s*(?:수능|대수능)/g, 'Nov Entrance Exam')
      .replace(/9월\s*(?:모의평가|모평)/g, 'Sep Official Mock')
      .replace(/6월\s*(?:모의평가|모평)/g, 'Jun Official Mock')
      .replace(/10월\s*(?:학력평가|학평)/g, 'Oct Academic Exam')
      .replace(/7월\s*(?:학력평가|학평)/g, 'Jul Academic Exam')
      .replace(/5월\s*(?:모평·학평|모평|학평)/g, 'May Official Mock')
      .replace(/4월\s*(?:학력평가|학평)/g, 'Apr Academic Exam')
      .replace(/3월\s*(?:학력평가|학평)/g, 'Mar Academic Exam')
      .replace(/11월/g, 'Nov')
      .replace(/12월/g, 'Dec')
      .replace(/10월/g, 'Oct')
      .replace(/9월/g, 'Sep')
      .replace(/8월/g, 'Aug')
      .replace(/7월/g, 'Jul')
      .replace(/6월/g, 'Jun')
      .replace(/5월/g, 'May')
      .replace(/4월/g, 'Apr')
      .replace(/3월/g, 'Mar')
      .replace(/2월/g, 'Feb')
      .replace(/1월/g, 'Jan')
      .replace(/고3\s*·\s*N수/g, 'Grade 12')
      .replace(/고3/g, 'G12')
      .replace(/고2/g, 'G11')
      .replace(/고1/g, 'G10')
      .replace(/중3/g, 'G9')
      .replace(/중2/g, 'G8')
      .replace(/중1/g, 'G7')
      .replace(/초등/g, 'Elementary')
      .replace(/중등/g, 'Middle School')
      .replace(/고등/g, 'High School')
      .replace(/(\d+)\s*번\s*문항/g, 'Question #$1')
      .replace(/(\d+)\s*번/g, '#$1')
      .replace(/(\d+)\s*단계/g, 'Step $1')
      .replace(/(\d+)\s*단(?![어])/g, 'Level $1')
      .replace(/정(\d+)각형/g, 'Regular $1-gon')
      .replace(/(\d+)각형/g, '$1-gon')
      .replace(/([\d,]+)\s*문항/g, '$1 problems')
      .replace(/([\d,]+)\s*개\s*주제/g, '$1 topics')
      .replace(/([\d,]+)\s*개씩\s*보기/g, 'Show $1 per page')
      .replace(/([\d,]+)\s*개/g, '$1')
      .replace(/([\d,]+)\s*건/g, '$1')
      .replace(/([\d,]+)\s*편/g, '$1 videos')
      .replace(/([\d,]+)\s*명/g, '$1 students')
      .replace(/(\d+)\s*초/g, '$1s')
      .replace(/(\d+)\s*분/g, '$1m')
      .replace(/(\d+)\s*일\s*연속\s*달성!/g, '$1-Day Streak!')
      .replace(/(\d+)\s*일차/g, 'Day $1');

    // 4. Comprehensive Term Replacement (Longest-first)
    for (var i = 0; i < TERM_PAIRS.length; i++) {
      var koTerm = TERM_PAIRS[i][0];
      if (s.indexOf(koTerm) !== -1) {
        s = s.split(koTerm).join(TERM_PAIRS[i][1]);
      }
    }

    // 5. Common Korean Connectors, Endings & Postpositions Cleanup
    // When Korean grammatical particles remain attached after translated English nouns/formulas,
    // translate or strip them cleanly so no awkward mixed text remains.
    s = s
      .replace(/의\s*값은\??/g, ' = ?')
      .replace(/의\s*값을\s*구하시오\.?/g, ' — Find the value.')
      .replace(/을\s*구하시오\.?/g, '')
      .replace(/를\s*구하시오\.?/g, '')
      .replace(/구하기/g, '')
      .replace(/에서의/g, ' on ')
      .replace(/으로부터/g, ' from ')
      .replace(/로부터/g, ' from ')
      .replace(/에서/g, ' in ')
      .replace(/으로/g, ' via ')
      .replace(/와\s+/g, ' & ')
      .replace(/과\s+/g, ' & ')
      .replace(/및\s+/g, '& ')
      .replace(/에\s*대한/g, ' on ')
      .replace(/에\s*관한/g, ' on ')
      .replace(/을\s*이용한/g, ' using ')
      .replace(/를\s*이용한/g, ' using ')
      .replace(/이\s*일정한\s*이유/g, ' Invariance')
      .replace(/완전\s*정복/g, 'Mastery')
      .replace(/직관적/g, 'Intuitive')
      .replace(/기하학적/g, 'Geometric')
      .replace(/대수적/g, 'Algebraic')
      .replace(/핵심/g, 'Core')
      .replace(/실전/g, 'Practical')
      .replace(/연습/g, 'Practice')
      .replace(/해설/g, 'Explanation')
      .replace(/강의/g, 'Lecture')
      .replace(/영상/g, 'Video')
      .replace(/원본/g, 'Original')
      .replace(/원문/g, 'Original')
      .replace(/무료/g, 'Free')
      .replace(/실시간/g, 'Live')
      .replace(/오늘의/g, "Today's ")
      .replace(/나의/g, 'My ')
      .replace(/모든/g, 'All ')
      .replace(/새\s+/g, 'New ');

    // Strip residual single-syllable Korean particles directly attached to ASCII/math tokens
    s = s.replace(/([A-Za-z0-9\)\]\}_])(?:은|는|이|가|을|를|의|에|로|도|만|와|과)(?=\s|$|[.,!?:;\)])/g, '$1');

    // If scattered Hangul syllables still remain in a long sentence, clean isolated particles/endings
    if (/[가-힣]/.test(s)) {
      s = s
        .replace(/입니다\.?/g, '.')
        .replace(/합니다\.?/g, '.')
        .replace(/됩니다\.?/g, '.')
        .replace(/보세요!?/g, '!')
        .replace(/하세요!?/g, '!')
        .replace(/[가-힣]+/g, function(rem) {
          // Keep nothing raw-Korean if surrounding English words already convey meaning, or map common stems
          var mini = {
            "수업": "Class", "학생": "Student", "교사": "Teacher", "선생님": "Teacher",
            "문제": "Problem", "문항": "Question", "정답": "Answer", "힌트": "Hint",
            "풀이": "Solution", "개념": "Concept", "단원": "Unit", "영역": "Domain",
            "자료": "Resource", "목록": "List", "선택": "Select", "입력": "Input",
            "확인": "Check", "저장": "Save", "삭제": "Delete", "추가": "Add",
            "변경": "Change", "도전": "Challenge", "성공": "Success", "실패": "Retry",
            "점수": "Score", "등급": "Tier", "단계": "Step", "비율": "Ratio",
            "관계": "Relation", "조건": "Condition", "성립": "Holds", "일정": "Constant",
            "대칭": "Symmetry", "회전": "Rotation", "평행": "Parallel", "수직": "Perpendicular",
            "내접": "Inscribed", "외접": "Circumscribed", "최대": "Max", "최소": "Min",
            "합": "Sum", "차": "Difference", "곱": "Product", "비": "Ratio",
            "점": "Point", "선": "Line", "면": "Plane", "원": "Circle", "구": "Sphere",
            "각": "Angle", "변": "Side", "축": "Axis", "근": "Root", "해": "Solution"
          };
          return mini[rem] || '';
        });
    }

    // Normalize spacing & punctuation
    s = s
      .replace(/\s{2,}/g, ' ')
      .replace(/\s+([.,!?:;])/g, '$1')
      .replace(/\(\s+/g, '(')
      .replace(/\s+\)/g, ')')
      .trim();

    // Restore LaTeX math segments verbatim
    s = s.replace(/__MTH_(\d+)__/g, function(_, idx) {
      return mathVault[parseInt(idx, 10)] || '';
    });

    return lead + s + trail;
  }

  // ══════════════════════════════════════════════════════════════════════════
  // Language Detection, Persistence & Cross-Page Synchronization
  // ══════════════════════════════════════════════════════════════════════════
  var currentLang = 'ko';
  var _isApplyingDom = false;
  var _observer = null;
  var _observerTimer = null;

  function detectDefaultLanguage() {
    try {
      if (typeof Intl !== 'undefined' && Intl.DateTimeFormat) {
        var tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
        if (tz) {
          if (tz === 'Asia/Seoul' || tz === 'ROK' || tz === 'Asia/Pyongyang') {
            return 'ko';
          }
          return 'en';
        }
      }
    } catch (e) {}

    try {
      var langs = (typeof navigator !== 'undefined' && (navigator.languages || [navigator.language || navigator.userLanguage])) || [];
      for (var i = 0; i < langs.length; i++) {
        if (langs[i] && String(langs[i]).toLowerCase().indexOf('ko') === 0) {
          return 'ko';
        }
      }
    } catch (e) {}

    return 'en';
  }

  function persistLanguage(lang, isManual) {
    try {
      localStorage.setItem(STORAGE_KEY, lang);
      localStorage.setItem(VB_STORAGE_KEY, lang);
      if (isManual) {
        localStorage.setItem(STORAGE_MANUAL_KEY, 'true');
      }
    } catch (e) {}
  }

  function initLanguage() {
    var urlParams = (typeof window !== 'undefined' && window.location && window.location.search)
      ? new URLSearchParams(window.location.search)
      : new URLSearchParams('');
    var langParam = (urlParams.get('lang') || '').toLowerCase();
    if (langParam === 'en' || langParam === 'ko') {
      currentLang = langParam;
      persistLanguage(currentLang, true);
    } else {
      var saved = null;
      var savedVb = null;
      var isManual = false;
      try {
        saved = localStorage.getItem(STORAGE_KEY);
        savedVb = localStorage.getItem(VB_STORAGE_KEY);
        isManual = localStorage.getItem(STORAGE_MANUAL_KEY) === 'true';
      } catch (e) {}

      if (isManual && (saved === 'en' || saved === 'ko')) {
        currentLang = saved;
      } else if (saved === 'en' || saved === 'ko') {
        currentLang = saved;
      } else if (savedVb === 'en' || savedVb === 'ko') {
        currentLang = savedVb;
      } else {
        currentLang = detectDefaultLanguage();
      }
    }
    if (typeof document !== 'undefined' && document.documentElement) {
      document.documentElement.lang = currentLang;
      document.documentElement.setAttribute('data-mathedu-lang', currentLang);
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

  // ══════════════════════════════════════════════════════════════════════════
  // Reversible Full-DOM Translation Walker + Bilingual Normalizer + Canvas 2D
  // ══════════════════════════════════════════════════════════════════════════
  var SKIP_CHILD_WALK_TAGS = {
    SCRIPT: 1,
    STYLE: 1,
    NOSCRIPT: 1,
    TEXTAREA: 1,
    CODE: 1,
    PRE: 1,
    MATH: 1,
    'MJX-CONTAINER': 1,
    IFRAME: 1,
    CANVAS: 1
  };

  var BLOCK_TAGS = {
    DIV: 1, P: 1, SECTION: 1, ARTICLE: 1, ASIDE: 1, HEADER: 1, FOOTER: 1,
    FIGURE: 1, TABLE: 1, UL: 1, OL: 1, BLOCKQUOTE: 1, H1: 1, H2: 1, H3: 1, H4: 1, H5: 1, H6: 1
  };

  function injectBilingualCssAndCanvasHook() {
    if (typeof document !== 'undefined' && document.head && !document.getElementById('mathedu-bilingual-global-css')) {
      var st = document.createElement('style');
      st.id = 'mathedu-bilingual-global-css';
      st.textContent =
        'html[lang="ko"] .bilingual-en { display: none !important; }\n' +
        'html[lang="en"] .bilingual-ko { display: none !important; }\n' +
        '.mathedu-floating-lang-pill { position: fixed; top: 12px; right: 14px; z-index: 9998; background: rgba(15,23,42,0.88); color: #f8fafc; border: 1px solid rgba(56,189,248,0.45); border-radius: 999px; padding: 5px 12px; font-size: 12px; font-weight: 800; cursor: pointer; backdrop-filter: blur(10px); box-shadow: 0 4px 14px rgba(0,0,0,0.25); font-family: Pretendard, system-ui, sans-serif; }\n' +
        '.mathedu-floating-lang-pill:hover { border-color: #38bdf8; background: rgba(2,132,199,0.92); }';
      document.head.appendChild(st);
    }

    if (typeof CanvasRenderingContext2D !== 'undefined' && CanvasRenderingContext2D.prototype && !CanvasRenderingContext2D.prototype.__matheduI18nWrapped) {
      var proto = CanvasRenderingContext2D.prototype;
      proto.__matheduI18nWrapped = true;
      var origFillText = proto.fillText;
      var origStrokeText = proto.strokeText;
      var origMeasureText = proto.measureText;
      if (typeof origFillText === 'function') {
        proto.fillText = function(text, x, y, maxWidth) {
          var out = (currentLang === 'en' && typeof text === 'string' && /[가-힣]/.test(text)) ? toEnglishMathText(text) : text;
          return arguments.length >= 4 ? origFillText.call(this, out, x, y, maxWidth) : origFillText.call(this, out, x, y);
        };
      }
      if (typeof origStrokeText === 'function') {
        proto.strokeText = function(text, x, y, maxWidth) {
          var out = (currentLang === 'en' && typeof text === 'string' && /[가-힣]/.test(text)) ? toEnglishMathText(text) : text;
          return arguments.length >= 4 ? origStrokeText.call(this, out, x, y, maxWidth) : origStrokeText.call(this, out, x, y);
        };
      }
      if (typeof origMeasureText === 'function') {
        proto.measureText = function(text) {
          var out = (currentLang === 'en' && typeof text === 'string' && /[가-힣]/.test(text)) ? toEnglishMathText(text) : text;
          return origMeasureText.call(this, out);
        };
      }
    }
  }

  /**
   * Automatically wraps unwrapped Korean sibling nodes next to `.bilingual-en`
   * into `<span/div class="bilingual-ko" data-auto-biko="1">` so CSS hides Korean
   * cleanly in `html[lang="en"]` and restores it in `html[lang="ko"]`.
   */
  function normalizeBilingualContainers(scope) {
    if (!scope || !scope.querySelectorAll) return;
    var enNodes = scope.querySelectorAll('.bilingual-en');
    for (var i = 0; i < enNodes.length; i++) {
      var enEl = enNodes[i];
      var parent = enEl.parentNode;
      if (!parent || parent.nodeType !== 1) continue;
      if (parent.hasAttribute('data-biko-norm')) continue;
      if (parent.classList && (parent.classList.contains('exp') || parent.classList.contains('bilingual-ko') || parent.classList.contains('bilingual-en'))) {
        parent.setAttribute('data-biko-norm', '1');
        continue;
      }
      var hasDirectBiKo = false;
      var ch = parent.children;
      for (var c = 0; c < ch.length; c++) {
        if (ch[c].classList && ch[c].classList.contains('bilingual-ko')) {
          hasDirectBiKo = true;
          break;
        }
      }
      if (hasDirectBiKo) {
        parent.setAttribute('data-biko-norm', '1');
        continue;
      }

      var toWrap = [];
      var hasKoContent = false;
      var hasBlockChild = false;
      var node = parent.firstChild;
      while (node) {
        var next = node.nextSibling;
        var isBiEn = (node.nodeType === 1 && node.classList && node.classList.contains('bilingual-en'));
        var isScriptOrStyle = (node.nodeType === 1 && (node.tagName === 'SCRIPT' || node.tagName === 'STYLE'));
        if (!isBiEn && !isScriptOrStyle) {
          toWrap.push(node);
          if (node.nodeType === 3 && /[가-힣]/.test(node.nodeValue || '')) hasKoContent = true;
          if (node.nodeType === 1) {
            if (/[가-힣]/.test(node.textContent || '')) hasKoContent = true;
            if (BLOCK_TAGS[(node.tagName || '').toUpperCase()]) hasBlockChild = true;
          }
        }
        node = next;
      }

      if (hasKoContent && toWrap.length > 0) {
        var wrapper = document.createElement(hasBlockChild ? 'div' : 'span');
        wrapper.className = 'bilingual-ko';
        wrapper.setAttribute('data-auto-biko', '1');
        if (toWrap[0] && toWrap[0].parentNode === parent) {
          parent.insertBefore(wrapper, toWrap[0]);
        } else {
          parent.appendChild(wrapper);
        }
        for (var w = 0; w < toWrap.length; w++) {
          if (toWrap[w] && toWrap[w].parentNode === parent) {
            wrapper.appendChild(toWrap[w]);
          }
        }
      }
      parent.setAttribute('data-biko-norm', '1');
    }
  }

  function translateMathJaxKoreanBoxes(scope, lang) {
    if (!scope || !scope.querySelectorAll) return;
    var nodes = scope.querySelectorAll('mjx-utext, mtext');
    var koToEnBlank = {
      '가': 'A', '나': 'B', '다': 'C', '라': 'D',
      '(가)': '(A)', '(나)': '(B)', '(다)': '(C)', '(라)': '(D)',
      '[가]': '[A]', '[나]': '[B]', '[다]': '[C]', '[라]': '[D]'
    };
    for (var i = 0; i < nodes.length; i++) {
      var n = nodes[i];
      var cur = (n.textContent || '').trim();
      if (lang === 'en') {
        if (cur && cur !== n._enMjx && /[가-힣]/.test(cur)) {
          n._koMjx = n.textContent;
        }
        if (typeof n._koMjx === 'string') {
          var rawTrim = n._koMjx.trim();
          var rep = koToEnBlank[rawTrim] || toEnglishMathText(rawTrim);
          if (rep) {
            n._enMjx = rep;
            if (n.textContent !== rep) n.textContent = rep;
          }
        }
      } else {
        if (typeof n._koMjx === 'string' && n.textContent !== n._koMjx) {
          n.textContent = n._koMjx;
        }
      }
    }
  }

  function shouldSkipElementSubtree(el) {
    if (!el || el.nodeType !== 1) return true;
    var tag = (el.tagName || '').toUpperCase();
    if (SKIP_CHILD_WALK_TAGS[tag]) return true;
    if (el.hasAttribute('data-no-i18n')) return true;
    var cls = el.className;
    if (typeof cls === 'string' && cls) {
      if (cls.indexOf('notranslate') !== -1 ||
          cls.indexOf('mjx-') !== -1 ||
          cls.indexOf('MathJax') !== -1 ||
          cls.indexOf('katex') !== -1 ||
          cls.indexOf('bilingual-ko') !== -1) {
        return true;
      }
    }
    return false;
  }

  function translateAttributesOnElement(el, lang) {
    if (!el || el.nodeType !== 1) return;
    var attrs = ['placeholder', 'title', 'aria-label'];
    for (var i = 0; i < attrs.length; i++) {
      var a = attrs[i];
      if (a === 'placeholder' && el.hasAttribute('data-i18n-placeholder')) continue;
      if (a === 'title' && el.hasAttribute('data-i18n-title')) continue;
      var cur = el.getAttribute(a);
      if (!cur && !el['_koAttr_' + a]) continue;
      var origProp = '_koAttr_' + a;
      var enProp = '_enAttr_' + a;
      if (lang === 'en') {
        if (cur && cur !== el[enProp] && /[가-힣]/.test(cur)) {
          el[origProp] = cur;
        }
        if (typeof el[origProp] === 'string') {
          var tr = toEnglishMathText(el[origProp]);
          el[enProp] = tr;
          if (tr && tr !== cur) el.setAttribute(a, tr);
        }
      } else {
        if (typeof el[origProp] === 'string' && cur !== el[origProp]) {
          el.setAttribute(a, el[origProp]);
        }
      }
    }

    // Translate pristine default value on text inputs (e.g., create.html preset title) without touching user edits
    if ((el.tagName || '').toUpperCase() === 'INPUT') {
      var tType = (el.getAttribute('type') || 'text').toLowerCase();
      if (tType === 'text' || tType === 'button' || tType === 'submit') {
        var curVal = el.value || '';
        if (lang === 'en') {
          if (curVal && curVal !== el._enInputVal && /[가-힣]/.test(curVal) && (tType !== 'text' || curVal === el.defaultValue)) {
            el._koInputVal = curVal;
          }
          if (typeof el._koInputVal === 'string' && (curVal === el._koInputVal || curVal === el._enInputVal)) {
            var trVal = toEnglishMathText(el._koInputVal);
            if (trVal) {
              el._enInputVal = trVal;
              if (el.value !== trVal) el.value = trVal;
            }
          }
        } else {
          if (typeof el._koInputVal === 'string' && el.value === el._enInputVal) {
            el.value = el._koInputVal;
          }
        }
      }
    }
  }

  function walkAndTranslateNode(node, lang) {
    if (!node) return;

    if (node.nodeType === 3) {
      var val = node.nodeValue;
      if (!val || (!val.trim() && typeof node._koOrig !== 'string')) return;
      var pEl = node.parentNode;
      if (pEl && pEl.tagName === 'OPTION' && !pEl.hasAttribute('value')) {
        pEl.setAttribute('value', pEl.value);
      }
      if (lang === 'en') {
        if (val !== node._enLast && /[가-힣]/.test(val)) {
          node._koOrig = val;
        }
        if (typeof node._koOrig === 'string') {
          var enText = toEnglishMathText(node._koOrig);
          node._enLast = enText;
          if (typeof enText === 'string' && enText !== val) {
            node.nodeValue = enText;
          }
        }
      } else {
        if (typeof node._koOrig === 'string' && val !== node._koOrig) {
          node.nodeValue = node._koOrig;
        }
      }
      return;
    }

    if (node.nodeType !== 1) return;

    // Always translate placeholder/title/aria-label BEFORE skipping TEXTAREA/INPUT children!
    if (!node.hasAttribute('data-no-i18n')) {
      translateAttributesOnElement(node, lang);
    }

    if (shouldSkipElementSubtree(node)) return;

    // Declarative data-en / data-en-html support
    if (node.hasAttribute('data-en')) {
      if (typeof node._koDataEnOrig !== 'string') {
        node._koDataEnOrig = node.textContent;
      }
      var targetTxt = (lang === 'en') ? node.getAttribute('data-en') : node._koDataEnOrig;
      if (node.textContent !== targetTxt) node.textContent = targetTxt;
      return;
    }
    if (node.hasAttribute('data-en-html')) {
      if (typeof node._koDataEnHtmlOrig !== 'string') {
        node._koDataEnHtmlOrig = node.innerHTML;
      }
      var targetHtml = (lang === 'en') ? node.getAttribute('data-en-html') : node._koDataEnHtmlOrig;
      if (node.innerHTML !== targetHtml) node.innerHTML = targetHtml;
      return;
    }

    // Elements managed by DICTIONARY data-i18n: skip in KO mode or if no Hangul remains in EN mode
    if (node.hasAttribute('data-i18n') || node.hasAttribute('data-i18n-html')) {
      if (lang === 'ko' || !/[가-힣]/.test(node.textContent || '')) {
        return;
      }
    }

    var child = node.firstChild;
    while (child) {
      var next = child.nextSibling;
      walkAndTranslateNode(child, lang);
      child = next;
    }
  }

  function ensureGlobalLangButton() {
    if (typeof document === 'undefined' || !document.body) return;
    if (document.getElementById('langToggleSingleBtn') ||
        document.getElementById('vbLangToggleBtn') ||
        document.querySelector('[data-lang-btn]') ||
        document.querySelector('.mathedu-global-lang-btn')) {
      return;
    }

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.setAttribute('data-no-i18n', '1');
    btn.onclick = function() { toggleLanguage(); };

    // Attach inside page header action bar if available, otherwise sleek floating pill
    var headerHost =
      document.querySelector('.gp-nav-actions') ||
      document.querySelector('.topbar-inner > div:last-child') ||
      document.querySelector('.topbar') ||
      document.querySelector('header nav > div:last-child');

    if (headerHost) {
      btn.className = 'mathedu-global-lang-btn';
      btn.style.cssText = 'padding:5px 11px;border-radius:999px;border:1px solid rgba(56,189,248,0.45);background:rgba(15,23,42,0.85);color:#f8fafc;font-size:12px;font-weight:800;cursor:pointer;font-family:inherit;display:inline-flex;align-items:center;gap:4px;';
      if (headerHost.firstChild && headerHost.firstChild.parentNode === headerHost) {
        headerHost.insertBefore(btn, headerHost.firstChild);
      } else {
        headerHost.appendChild(btn);
      }
    } else {
      btn.className = 'mathedu-global-lang-btn mathedu-floating-lang-pill';
      // On mathlab.html, place beside top-right controls without blocking toolbar
      if (document.getElementById('toolbar') && document.getElementById('canvas')) {
        btn.style.top = '10px';
        btn.style.right = '96px';
      }
      document.body.appendChild(btn);
    }
  }

  function updateLanguageButtonsUI(lang) {
    if (typeof document === 'undefined') return;
    ensureGlobalLangButton();

    var btns = document.querySelectorAll('[data-lang-btn]');
    btns.forEach(function(b) {
      b.setAttribute('data-no-i18n', '1');
      var bLang = b.getAttribute('data-lang-btn');
      if (bLang === 'ko' && /[가-힣]/.test(b.textContent || '')) {
        if (!b._koBtnLabelOrig) b._koBtnLabelOrig = b.innerHTML;
        b.innerHTML = (lang === 'en') ? '🇰🇷 KO' : b._koBtnLabelOrig;
      }
      if (bLang === lang) {
        b.classList.add('active');
      } else {
        b.classList.remove('active');
      }
    });

    var singleBtn = document.getElementById('langToggleSingleBtn');
    if (singleBtn) {
      singleBtn.setAttribute('data-no-i18n', '1');
      if (lang === 'en') {
        singleBtn.innerHTML = '<span style="opacity:0.55;font-weight:600">KO</span><span style="margin:0 3px;opacity:0.35">|</span><span style="color:#0284c7;font-weight:900">🌐 EN</span>';
        singleBtn.title = 'Switch to Korean';
      } else {
        singleBtn.innerHTML = '<span style="color:#0284c7;font-weight:900">🇰🇷 KO</span><span style="margin:0 3px;opacity:0.35">|</span><span style="opacity:0.6;font-weight:700">EN</span>';
        singleBtn.title = 'Switch to English';
      }
    }

    var vbBtn = document.getElementById('vbLangToggleBtn');
    if (vbBtn) {
      vbBtn.setAttribute('data-no-i18n', '1');
      vbBtn.textContent = (lang === 'en') ? '🇰🇷 Switch to KO' : '🇺🇸 English Mode (EN)';
    }

    var globalSwitchBtns = document.querySelectorAll('.mathedu-global-lang-btn');
    globalSwitchBtns.forEach(function(gb) {
      gb.setAttribute('data-no-i18n', '1');
      gb.innerHTML = (lang === 'en')
        ? '<span style="opacity:0.6">KO</span><span style="opacity:0.4">|</span><span style="color:#38bdf8">🌐 EN</span>'
        : '<span style="color:#38bdf8">🇰🇷 KO</span><span style="opacity:0.4">|</span><span style="opacity:0.75">EN</span>';
      gb.title = (lang === 'en') ? 'Switch to Korean' : 'Switch to English';
    });
  }

  function applyDomTranslations(customRoot) {
    if (typeof document === 'undefined' || !document.querySelectorAll) return;
    if (_isApplyingDom) return;
    _isApplyingDom = true;
    try {
      injectBilingualCssAndCanvasHook();
      var scope = customRoot || document;

      // 0. Normalize unwrapped Korean siblings next to .bilingual-en
      normalizeBilingualContainers(scope);

      // 1. data-i18n
      var elList = scope.querySelectorAll ? scope.querySelectorAll('[data-i18n]') : [];
      elList.forEach(function(el) {
        var key = el.getAttribute('data-i18n');
        var val = t(key);
        if (typeof val === 'string' && val !== key) {
          if (el.tagName && el.tagName.toLowerCase() === 'title') {
            document.title = val;
          }
          el.textContent = val;
        }
      });

      // 2. data-i18n-html
      var elHtmlList = scope.querySelectorAll ? scope.querySelectorAll('[data-i18n-html]') : [];
      elHtmlList.forEach(function(el) {
        var key = el.getAttribute('data-i18n-html');
        var val = t(key);
        if (typeof val === 'string' && val !== key) {
          el.innerHTML = val;
        }
      });

      // 3. data-i18n-placeholder
      var elPlaceholders = scope.querySelectorAll ? scope.querySelectorAll('[data-i18n-placeholder]') : [];
      elPlaceholders.forEach(function(el) {
        var key = el.getAttribute('data-i18n-placeholder');
        var val = t(key);
        if (typeof val === 'string' && val !== key) {
          el.setAttribute('placeholder', val);
        }
      });

      // 4. data-i18n-title
      var elTitles = scope.querySelectorAll ? scope.querySelectorAll('[data-i18n-title]') : [];
      elTitles.forEach(function(el) {
        var key = el.getAttribute('data-i18n-title');
        var val = t(key);
        if (typeof val === 'string' && val !== key) {
          el.setAttribute('title', val);
        }
      });

      // 5. Update page <title> reversibly
      if (!customRoot && document.title) {
        if (currentLang === 'en' && /[가-힣]/.test(document.title)) {
          document._koTitleOrig = document.title;
          document.title = toEnglishMathText(document.title);
        } else if (currentLang === 'ko' && document._koTitleOrig) {
          document.title = document._koTitleOrig;
        }
      }

      // 6. Update language buttons
      if (!customRoot) {
        updateLanguageButtonsUI(currentLang);
      }

      // 7. Walk and translate all text nodes & attributes reversibly
      var walkRoot = customRoot || document.body;
      if (walkRoot) {
        walkAndTranslateNode(walkRoot, currentLang);
        translateMathJaxKoreanBoxes(walkRoot, currentLang);
      }

      // 8. Typeset MathJax if needed
      if (!customRoot && window.MathJax && MathJax.typesetPromise) {
        var mathStory = document.getElementById('mathStoryDrawer');
        if (mathStory && mathStory.style.display !== 'none') {
          MathJax.typesetPromise([mathStory]).catch(function() {});
        }
      }
    } finally {
      _isApplyingDom = false;
    }
  }

  function ensureMutationObserver() {
    if (_observer || typeof MutationObserver === 'undefined' || typeof document === 'undefined') return;
    if (!document.body) return;
    var pendingRoots = [];
    _observer = new MutationObserver(function(mutations) {
      if (_isApplyingDom || currentLang !== 'en') return;
      for (var i = 0; i < mutations.length; i++) {
        var m = mutations[i];
        var target = m.target;
        if (!target) continue;
        var el = (target.nodeType === 1) ? target : target.parentElement;
        if (!el) continue;
        // Catch late MathJax rendering (<mjx-container> inserting <mtext>(가)</mtext>)
        var tagUpper = (el.tagName || '').toUpperCase();
        if (tagUpper === 'MJX-CONTAINER' || (typeof el.className === 'string' && el.className.indexOf('mjx-') !== -1)) {
          var mjxHost = el.closest ? (el.closest('mjx-container') || el) : el;
          if (pendingRoots.indexOf(mjxHost) === -1) pendingRoots.push(mjxHost);
          continue;
        }
        if (shouldSkipElementSubtree(el)) continue;
        if (pendingRoots.indexOf(el) === -1) {
          pendingRoots.push(el);
        }
      }
      if (!pendingRoots.length || _observerTimer) return;
      _observerTimer = setTimeout(function() {
        _observerTimer = null;
        if (currentLang !== 'en') {
          pendingRoots.length = 0;
          return;
        }
        var batch = pendingRoots.slice();
        pendingRoots.length = 0;
        _isApplyingDom = true;
        try {
          if (batch.length > 60 && document.body) {
            normalizeBilingualContainers(document.body);
            walkAndTranslateNode(document.body, 'en');
            translateMathJaxKoreanBoxes(document.body, 'en');
          } else {
            for (var j = 0; j < batch.length; j++) {
              var rootEl = batch[j];
              if (rootEl && rootEl.isConnected !== false) {
                if ((rootEl.tagName || '').toUpperCase() === 'MJX-CONTAINER') {
                  translateMathJaxKoreanBoxes(rootEl, 'en');
                } else {
                  normalizeBilingualContainers(rootEl);
                  walkAndTranslateNode(rootEl, 'en');
                  translateMathJaxKoreanBoxes(rootEl, 'en');
                }
              }
            }
          }
          updateLanguageButtonsUI('en');
        } finally {
          _isApplyingDom = false;
        }
      }, 20);
    });
    _observer.observe(document.body, {
      childList: true,
      subtree: true,
      characterData: true
    });
  }

  function setLanguage(lang) {
    if (lang !== 'ko' && lang !== 'en') return;
    currentLang = lang;
    persistLanguage(lang, true);

    if (typeof document !== 'undefined' && document.documentElement) {
      document.documentElement.lang = lang;
      document.documentElement.setAttribute('data-mathedu-lang', lang);
    }

    if (typeof window.onMatheduLanguageChange === 'function') {
      try { window.onMatheduLanguageChange(lang); } catch (e) {}
    }
    if (typeof window.setBoardLang === 'function' && !window.__inSetBoardLang) {
      try {
        window.__inSetBoardLang = true;
        window.setBoardLang(lang, false);
      } catch (e) {} finally {
        window.__inSetBoardLang = false;
      }
    }
    if (typeof window.applyVideoBoardGlobalLang === 'function' && !window.__inVbLang) {
      try {
        window.__inVbLang = true;
        window.applyVideoBoardGlobalLang(lang);
      } catch (e) {} finally {
        window.__inVbLang = false;
      }
    }
    if (typeof window.setOfflineLang === 'function' && !window.__inOfflineLang) {
      try {
        window.__inOfflineLang = true;
        window.setOfflineLang(lang, false);
      } catch (e) {} finally {
        window.__inOfflineLang = false;
      }
    }

    applyDomTranslations();
    ensureMutationObserver();

    try {
      window.dispatchEvent(new CustomEvent('mathedu:lang-changed', { detail: { lang: lang } }));
    } catch (e) {}

    setTimeout(function() {
      applyDomTranslations();
    }, 35);
  }

  function toggleLanguage() {
    setLanguage(currentLang === 'en' ? 'ko' : 'en');
    return currentLang;
  }

  function formatProblemMeta(item) {
    if (!item) return '';
    if (currentLang === 'en') {
      var parts = [];
      if (item.examYear) parts.push(item.examYear + ' AY');
      if (item.month) {
        var mMap = {
          '11월': 'Nov Entrance',
          '수능': 'Nov Entrance',
          '9월': 'Sep Mock',
          '6월': 'Jun Mock',
          '10월': 'Oct Exam',
          '7월': 'Jul Exam',
          '5월': 'May Mock',
          '4월': 'Apr Exam',
          '3월': 'Mar Exam'
        };
        parts.push(mMap[item.month] || toEnglishMathText(item.month));
      }
      if (item.grade) {
        var gMap = {
          '고3': 'Grade 12',
          '고2': 'Grade 11',
          '고1': 'Grade 10'
        };
        parts.push(gMap[item.grade] || toEnglishMathText(item.grade));
      }
      if (item.subject) {
        var sMap = {
          '공통(수학I·II)': 'Math I·II',
          '미적분': 'Calculus',
          '기하': 'Geometry',
          '확률과 통계': 'Prob & Stats',
          '공통수학': 'Common Math',
          '수학(가형)': 'Math Ga',
          '수학(나형)': 'Math Na'
        };
        parts.push(sMap[item.subject] || toEnglishMathText(item.subject));
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

  initLanguage();
  injectBilingualCssAndCanvasHook();

  window.MatheduI18n = {
    getLanguage: getLanguage,
    setLanguage: setLanguage,
    toggleLanguage: toggleLanguage,
    detectDefaultLanguage: detectDefaultLanguage,
    t: t,
    toEnglishMathText: toEnglishMathText,
    translateKoText: toEnglishMathText,
    normalizeBilingualContainers: normalizeBilingualContainers,
    expandEnglishSearchQuery: expandEnglishSearchQuery,
    applyDomTranslations: applyDomTranslations,
    formatProblemMeta: formatProblemMeta
  };

  function bootDomI18n() {
    injectBilingualCssAndCanvasHook();
    if (currentLang === 'en') {
      if (typeof window.onMatheduLanguageChange === 'function') {
        try { window.onMatheduLanguageChange('en'); } catch (e) {}
      }
      if (typeof window.applyVideoBoardGlobalLang === 'function' && !window.__inVbLang) {
        try { window.__inVbLang = true; window.applyVideoBoardGlobalLang('en'); } catch (e) {} finally { window.__inVbLang = false; }
      }
      if (typeof window.setOfflineLang === 'function' && !window.__inOfflineLang) {
        try { window.__inOfflineLang = true; window.setOfflineLang('en', false); } catch (e) {} finally { window.__inOfflineLang = false; }
      }
    }
    applyDomTranslations();
    ensureMutationObserver();
  }

  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', bootDomI18n);
    } else {
      setTimeout(bootDomI18n, 0);
    }
  }

})(window);
