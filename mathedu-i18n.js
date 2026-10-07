/**
 * mathedu-i18n.js
 * mathedu · Global Internationalization (i18n) Engine
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
        minExplorer: "🌐 동적 기하 탐색관",
        myBadges: "🏆 나의 업적",
        createQuiz: "✨ 문제 출제",
        membersOnly: "회원전용",
        dashboard: "📊 수업 대시보드",
        minHome: "🌐 자료실 홈"
      },
      hero: {
        badgePill: "🏛️ 3,400+ 시각적 수학 증명과 직관 · 수학자료실",
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
      hongik: {
        badge: "🏛️ 弘益人間 · 널리 세상을 이롭게 하는 열린 수학교육",
        title: "수학의 직관과 아름다움을 모든 인류에게",
        desc: "수학교육자료실(min7014)은 <b>3,400+ 주제의 시각적 증명과 단계별 인터랙티브 디딤돌 퀴즈</b>를 광고나 결제, 가입 장벽 없이 <b>전 세계 모든 학생과 선생님께 100% 영구 무료</b>로 바칩니다. 초등학생부터 수능 킬러 문항까지, 누구나 스스로 깨우칠 수 있도록 널리 전파해 주세요.",
        pill1: "🌐 100% 영구 무료 & 무광고 열린 교육 (OER)",
        pill2: "📐 3,400+ GeoGebra & 원리 증명 PDF",
        pill3: "🪜 초등부터 수능 킬러까지 무장벽 디딤돌",
        pill4: "🏫 학교·교실·블로그 자유 탑재 & 수업 활용 환영",
        shareBtnNative: "📤 1초 전세계 공유하기",
        shareBtnTwitter: "𝕏 트위터 공유",
        shareBtnKakao: "💬 카카오톡 공유",
        shareBtnFacebook: "📘 페이스북",
        shareBtnWhatsapp: "📱 WhatsApp",
        shareBtnTelegram: "✈️ 텔레그램",
        btnQrCode: "📱 대형 QR코드 (교실 빔프로젝터용)",
        btnEmbed: "📋 블로그/LMS 탑재 코드 복사",
        copiedToast: "✅ 공유 링크가 클립보드에 복사되었습니다! 널리 알려주셔서 감사합니다.",
        embedCopiedToast: "✅ iframe 삽입 코드가 복사되었습니다! 학교 홈페이지, 블로그, 노션에 자유롭게 붙여넣으세요.",
        qrModalTitle: "📱 교실 빔프로젝터 및 스마트폰 접속용 대형 QR코드",
        qrModalSub: "스마트폰 카메라로 스캔하면 가입이나 로그인 없이 1초 만에 전체 퀴즈를 무료로 시작합니다.",
        embedModalTitle: "📋 웹사이트 / 블로그 / LMS (노션, 클래스룸) 탑재 코드",
        embedModalSub: "아래 HTML 코드를 복사하여 학교 LMS나 개인 블로그에 붙여넣으면 대화형 수학자료실이 그대로 탑재됩니다."
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
        badgePill: "🏛️ 3,400+ Dynamic Visual Proofs & Geometric Intuition · Math Archive",
        mainTitleLab: "수학자료실",
        mainTitleHub: "mathedu",
        leadDesc: "Math Archive: Over 3,400 Dynamic Visual Proofs & Scaffolding Quizzes, <b>100% Freely Open</b>",
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
      hongik: {
        badge: "🏛️ Hongik Ingan · For the Benefit of All Humankind",
        title: "Bringing Mathematical Intuition & Beauty to the World",
        desc: "Mathematics Archive (min7014) permanently opens <b>3,400+ visual geometric proofs and interactive scaffolding quizzes</b> 100% freely to students, teachers, and curious minds worldwide—without ads, paywalls, or mandatory signups. Help us spread the joy of visual mathematical understanding.",
        pill1: "🌐 100% Free Forever & Open Educational Resource (OER)",
        pill2: "📐 3,400+ GeoGebra & Proof PDFs",
        pill3: "🪜 Barrier-Free Scaffolding (Elementary to Advanced)",
        pill4: "🏫 Free for Classrooms, Schools & Educational Blogs",
        shareBtnNative: "📤 Share Globally (1s)",
        shareBtnTwitter: "𝕏 Share on X",
        shareBtnKakao: "💬 KakaoTalk",
        shareBtnFacebook: "📘 Facebook",
        shareBtnWhatsapp: "📱 WhatsApp",
        shareBtnTelegram: "✈️ Telegram",
        btnQrCode: "📱 Classroom Projector QR Code",
        btnEmbed: "📋 Copy Embed Code for LMS/Blog",
        copiedToast: "✅ Link copied to clipboard! Thank you for sharing math education.",
        embedCopiedToast: "✅ Iframe embed code copied! Paste freely into your LMS, Notion, or school website.",
        qrModalTitle: "📱 Large QR Code for Classroom Projection & Handouts",
        qrModalSub: "Scan with any smartphone camera to open and solve immediately without signup.",
        embedModalTitle: "📋 Embed on Websites, Blogs & Learning Platforms",
        embedModalSub: "Copy the HTML snippet below to embed this interactive mathematics archive directly into your school LMS, Google Sites, or blog."
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
        shieldActiveDesc: "To prevent student identity exposure on shared classroom displays, pseudonyms <b>stu1, stu2, stu3...</b> are automatically assigned in join order. (Real names and privacy controls are only accessible to authenticated teachers in their own classes.)",
        teacherModeTitle: "👑 Teacher Classroom Command Mode",
        teacherModeBadge: "Displaying Real Student Names",
        teacherModeDesc: "As the creator of class (<b>{room}</b>), real student names are displayed. For classroom projection or screen sharing, click <b>[🔒 Privacy Shield (Projector Mode)]</b> above to anonymize names to <code>stu1, stu2...</code> immediately.",
        projectorModeTitle: "🖥️ Classroom Projector Mode Active",
        projectorModeBadge: "All Students stu1, stu2... Anonymized",
        projectorModeDesc: "Student names are displayed as anonymous identifiers (stu1~) for classroom projector display. To view real names again, click <b>[👀 Return to Real Names]</b> above.",
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

  var STORAGE_KEY = 'mathedu_lang';
  var STORAGE_MANUAL_KEY = 'mathedu_lang_manual';

  var currentLang = 'ko';

  /**
   * Detect default language based on visitor's location:
   * - Korea (Asia/Seoul, ROK, Asia/Pyongyang) -> 'ko'
   * - Outside Korea (any other timezone / non-Korean locale) -> 'en'
   */
  function detectDefaultLanguage() {
    // 1. Timezone detection (0ms synchronous, 100% reliable)
    try {
      if (typeof Intl !== 'undefined' && Intl.DateTimeFormat) {
        var tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
        if (tz) {
          if (tz === 'Asia/Seoul' || tz === 'ROK' || tz === 'Asia/Pyongyang') {
            return 'ko';
          }
          // Any other recognized timezone means visitor is outside Korea
          return 'en';
        }
      }
    } catch(e) {}

    // 2. Fallback: Browser language
    try {
      var langs = (typeof navigator !== 'undefined' && (navigator.languages || [navigator.language || navigator.userLanguage])) || [];
      for (var i = 0; i < langs.length; i++) {
        if (langs[i] && String(langs[i]).toLowerCase().indexOf('ko') === 0) {
          return 'ko';
        }
      }
    } catch(e) {}

    // 3. International default
    return 'en';
  }

  function initLanguage() {
    var urlParams = (typeof window !== 'undefined' && window.location && window.location.search) ? new URLSearchParams(window.location.search) : new URLSearchParams('');
    var langParam = urlParams.get('lang');
    if (langParam === 'en' || langParam === 'ko') {
      currentLang = langParam;
      try {
        localStorage.setItem(STORAGE_KEY, currentLang);
        localStorage.setItem(STORAGE_MANUAL_KEY, 'true');
      } catch(e){}
    } else {
      var saved = null;
      var isManual = false;
      try {
        saved = localStorage.getItem(STORAGE_KEY);
        isManual = localStorage.getItem(STORAGE_MANUAL_KEY) === 'true';
      } catch(e){}

      if (isManual && (saved === 'en' || saved === 'ko')) {
        currentLang = saved;
      } else {
        // Auto-detect based on physical location (Korea -> 'ko', Outside Korea -> 'en')
        currentLang = detectDefaultLanguage();
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
    try {
      localStorage.setItem(STORAGE_KEY, lang);
      localStorage.setItem(STORAGE_MANUAL_KEY, 'true');
    } catch(e){}
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
    try {
      window.dispatchEvent(new CustomEvent('mathedu:lang-changed', { detail: { lang: lang } }));
    } catch(e) {}
  }

  function applyDomTranslations() {
    if (typeof document === 'undefined' || !document.querySelectorAll) return;
    // 1. Text elements: data-i18n
    var elList = document.querySelectorAll('[data-i18n]');
    elList.forEach(function(el) {
      var key = el.getAttribute('data-i18n');
      var val = t(key);
      if (typeof val === 'string') {
        if (el.tagName && el.tagName.toLowerCase() === 'title') {
          document.title = val;
        }
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

    // 5. Update language switchers
    var btns = document.querySelectorAll('[data-lang-btn]');
    btns.forEach(function(b) {
      if (b.getAttribute('data-lang-btn') === currentLang) {
        b.classList.add('active');
      } else {
        b.classList.remove('active');
      }
    });

    // 6. Typeset math if needed
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
    detectDefaultLanguage: detectDefaultLanguage,
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
