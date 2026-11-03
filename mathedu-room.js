/**
 * mathedu-room.js — 수학 mathedu 교사-학생 수업 연동 & 비회원 식별·학습 기록 모듈 (v3.1 Bilingual)
 * 
 * 1. 학생/비회원:
 *    - ?room=ROOM_ID 링크 접속 시 자동 학급 수업 참여.
 *    - 고유한 [이름]과 [간편 비밀번호(4자리)] 입력 시 동일 학습자로 자동 인식.
 *    - 나중에 같은 문제에 다시 오더라도 이전 풀이 단계(진행률/정답수)를 완벽 복원하여 이어서 풀기 지원.
 *    - [📂 내가 푼 문제 모아보기]를 통해 풀었던 모든 문항을 한곳에서 모아보고 복습.
 *    - [✨ 정식 회원 전환]으로 비회원 풀이 기록 100% 승계하며 즉시 업그레이드.
 * 2. 교사/회원:
 *    - 각 문제 화면(시작 모달, 상단 배너, 플로팅 버튼, 상단바)에서
 *      클릭 한 번으로 3초 만에 수업 코드, 학생용 링크, 칠판 빔프로젝터용 대형 QR 발급.
 *    - 문제 출제 및 수업 개설은 인증된 회원만 가능하도록 권한 보호.
 * 3. 한국어(KO) / 영어(EN) 완전 무결 이중 언어 시스템 (Pure Bilingual Dual-Element Engine) 지원.
 */
(function() {
  'use strict';

  var urlParams = new URLSearchParams(window.location.search);
  var roomId = (urlParams.get('room') || '').trim();
  window._roomId = roomId;

  // 퀴즈 slug 추출
  var currentSlug = window.location.pathname.split('/').pop().replace('.html', '') || 'quiz';

  // 🌐 i18n 헬퍼 함수
  function isEnMode() {
    var l = (typeof document !== 'undefined' && document.documentElement && document.documentElement.lang) ? document.documentElement.lang : '';
    return l.toLowerCase().startsWith('en');
  }

  function getVisitorAnonId() {
    try {
      var vid = localStorage.getItem('mathedu_visitor_id');
      if (!vid) {
        vid = Math.random().toString(36).substring(2, 6).toUpperCase();
        localStorage.setItem('mathedu_visitor_id', vid);
      }
      return vid;
    } catch(e) {
      if (!window._fallbackVid) window._fallbackVid = Math.floor(1000 + Math.random() * 9000).toString();
      return window._fallbackVid;
    }
  }

  function getVisitorAnonName() {
    var vid = getVisitorAnonId();
    return isEnMode() ? ('Guest#' + vid) : ('자유학습#' + vid);
  }

  function bilingual(ko, en) {
    return '<span class="bilingual-ko">' + ko + '</span><span class="bilingual-en">' + en + '</span>';
  }

  function injectBilingualStyles() {
    if (document.getElementById('mathedu-bilingual-engine-styles')) return;
    var style = document.createElement('style');
    style.id = 'mathedu-bilingual-engine-styles';
    style.textContent = 
      '.bilingual-en { display: none !important; }\n' +
      'html[lang="en"] .bilingual-ko { display: none !important; }\n' +
      'html[lang="en"] .bilingual-en { display: inline !important; color: inherit !important; font-size: inherit !important; font-weight: inherit !important; }\n' +
      'html[lang="en"] div.bilingual-en, html[lang="en"] p.bilingual-en, html[lang="en"] section.bilingual-en, html[lang="en"] li.bilingual-en { display: block !important; }\n' +
      'html[lang="en"] div.bilingual-en[style*="display: flex"], html[lang="en"] div.bilingual-en[style*="display:flex"] { display: flex !important; }\n';
    (document.head || document.documentElement).appendChild(style);
  }
  injectBilingualStyles();

  function ensureAuthLoaded(callback) {
    var isBoard = window.location.pathname.indexOf('/board/') !== -1;
    var toLoad = [];
    if (!window.MatheduAuth) toLoad.push(isBoard ? '../mathedu-auth.js' : './mathedu-auth.js');
    if (!window.MatheduGame) toLoad.push(isBoard ? '../mathedu-gamification.js' : './mathedu-gamification.js');

    if (toLoad.length === 0) {
      if (typeof callback === 'function') callback();
      return;
    }

    var loaded = 0;
    toLoad.forEach(function(src) {
      var script = document.createElement('script');
      script.src = src;
      script.onload = script.onerror = function() {
        loaded++;
        if (loaded >= toLoad.length && typeof callback === 'function') {
          callback();
        }
      };
      document.head.appendChild(script);
    });
  }

  function logInitialPageVisit() {
    try {
      if (window.location.protocol !== 'http:' && window.location.protocol !== 'https:') return;
      if (navigator && navigator.webdriver) return;
      var visitKey = 'mathedu_visit_logged_' + currentSlug;
      if (sessionStorage.getItem(visitKey)) return;
      sessionStorage.setItem(visitKey, '1');
      if (!window._studentName) {
        var u = window.MatheduAuth && window.MatheduAuth.getCurrentUser ? window.MatheduAuth.getCurrentUser() : null;
        var g = window.MatheduAuth && window.MatheduAuth.getCurrentGuest ? window.MatheduAuth.getCurrentGuest() : null;
        window._studentName = (u && u.name) ? u.name : ((g && g.name) ? g.name : getVisitorAnonName());
      }
      if (typeof window.sendProgress === 'function') {
        window.sendProgress();
      }
    } catch (e) {}
  }

  function initRoom() {
    injectBilingualStyles();
    // 즉시 sendProgress를 CORS-safe 버전으로 패치 (외부 스크립트 로드 전 클릭 시에도 누락 방지)
    patchSendProgress();
    ensureAuthLoaded(function() {
      // 0. 선생님의 오늘의 수업 팩(?pack=slug1,slug2,...) 네비게이션 안내
      injectLessonPackBanner();

      // 1. 학생이 특정 방에 참여 중인 경우 UI 표시
      if (roomId) {
        applyStudentRoomUI(roomId);
      }

      // 2. 시작 모달(#trackFull)에 비회원 간편 식별 및 이전 풀이 복원 기능 추가 (Stitch 0초 즉시 학습: 일반 접속 시 모달 자동 패스)
      enhanceTrackFullModal();
      if (!roomId) {
        var tfAuto = document.getElementById('trackFull');
        if (tfAuto) tfAuto.style.display = 'none';
        if (!window._studentName) {
          var uAuto = window.MatheduAuth && window.MatheduAuth.getCurrentUser ? window.MatheduAuth.getCurrentUser() : null;
          var gAuto = window.MatheduAuth && window.MatheduAuth.getCurrentGuest ? window.MatheduAuth.getCurrentGuest() : null;
          window._studentName = (uAuto && uAuto.name) ? uAuto.name : ((gAuto && gAuto.name) ? gAuto.name : getVisitorAnonName());
        }
      }

      // 3. 문제 페이지 상단에 [이 문제로 수업 개설] 배너 삽입
      injectProblemPageBanner();

      // 4. 스크롤 중에도 언제든 누를 수 있는 플로팅 [🚀 이 문제로 수업 열기] 버튼
      injectFloatingClassButton();

      // 5. 상단바 tbtn에 버튼 추가 (내가 푼 문제 + 수업 열기 + 즐겨찾기 + A4 인쇄 + 칠판모드)
      injectTopbarButtons();

      // 6. sendProgress 가로채기 (Google Sheets 전송 + MatheduAuth 풀이 기록 + 게이미피케이션 XP/Confetti)
      patchSendProgress();

      // 6-1. 외부 방문자 페이지 진입 즉시 자동 방문 기록 (모달 클릭 전 이탈자도 100% 추적)
      logInitialPageVisit();

      // 7. 이전에 풀었던 문제라면 페이지 상단에 진행 안내 바 표시
      checkAndShowResumeBanner();

      // 8. 오답 선택 감지기 (학생 오답노트 자동 적립)
      attachWrongAnswerTracker();

      // 9. 🪜 차분한 단계별 몰입형 순차 공개 시스템 (스크롤 훑어보기 방지)
      initProgressiveScaffolding();

      // 10. 🎓 수학교육학 5대 학문 통합 엔진 (CPA 다중표상 · ZPD 힌트사다리 · 블라인드 인출 · 폴리아/쇤펠드 메타인지 · 정교한 오개념 진단)
      initAcademicPedagogyEngine();

      // 11. 🔊 AI 수식-음성 변환 해설 선생님 & min7014.github.io 1,111개 자료 심층 도슨트 연동
      initVoiceTeacherAndMin7014Deep();
    });
  }

  function applyStudentRoomUI(rId) {
    var trackFull = document.getElementById('trackFull');
    if (trackFull) {
      var h3 = trackFull.querySelector('h3');
      if (h3) {
        var roomBadge = document.createElement('div');
        roomBadge.style.cssText = 'display:inline-flex;align-items:center;gap:6px;background:rgba(0,99,152,.10);border:1px solid rgba(0,99,152,.28);color:#006398;border-radius:20px;padding:5px 16px;font-size:0.9rem;margin-bottom:14px;font-weight:700;animation:popIn .3s ease';
        roomBadge.innerHTML = bilingual('🏫 <b>[' + escapeHtml(rId) + ']</b> 수업에 참여합니다', '🏫 Joining Class <b>[' + escapeHtml(rId) + ']</b>');
        h3.parentNode.insertBefore(roomBadge, h3);
      }
      var p = trackFull.querySelector('p');
      if (p) {
        p.innerHTML = bilingual('선생님과 실시간으로 연동됩니다. 이름 또는 출석번호를 입력하세요.', 'Connected with teacher in real time. Enter your name or student number.');
      }
      var input = document.getElementById('studentName');
      if (input) {
        input.setAttribute('data-ko-placeholder', '예: 15번 김철수');
        input.setAttribute('data-en-placeholder', 'e.g. Student #15 John');
        input.placeholder = isEnMode() ? 'e.g. Student #15 John' : '예: 15번 김철수';
      }
    }

    var topbar = document.querySelector('.topbar') || document.querySelector('.navbar');
    if (topbar) {
      var activeRoomBadge = document.createElement('div');
      activeRoomBadge.style.cssText = 'margin-left:auto;display:inline-flex;align-items:center;gap:6px;background:#ecfdf5;border:1px solid #10b981;color:#047857;border-radius:10px;padding:6px 14px;font-size:0.85rem;font-weight:700;';
      activeRoomBadge.innerHTML = bilingual('🟢 <b>' + escapeHtml(rId) + '</b> 수업 참여 중', '🟢 In Class <b>' + escapeHtml(rId) + '</b>');
      topbar.appendChild(activeRoomBadge);
    }
  }

  function enhanceTrackFullModal() {
    var trackFull = document.getElementById('trackFull');
    if (!trackFull) return;

    // 🌐 첫 화면 언어 선택기 (KO / EN Language Switcher on Start Modal)
    var curLang = document.documentElement.lang || 'ko';
    try {
      var savedL = localStorage.getItem('mathedu_lang');
      if (savedL === 'en' || savedL === 'ko') curLang = savedL;
    } catch(e) {}

    var existingLangSwitcher = document.getElementById('trackFullLangSwitcher');
    if (!existingLangSwitcher) {
      var langSwitcher = document.createElement('div');
      langSwitcher.id = 'trackFullLangSwitcher';
      langSwitcher.style.cssText = 'position:absolute;top:18px;right:20px;z-index:100;display:inline-flex;align-items:center;background:#f0edef;border:1.5px solid #e4e2e4;border-radius:24px;padding:3px 4px;gap:3px;box-shadow:0 2px 8px rgba(19,27,46,.06);';
      langSwitcher.innerHTML = 
        '<button type="button" id="btnTrackFullLangKo" onclick="window.setBoardLanguage(\'ko\')" style="background:' + (curLang === 'en' ? 'transparent' : '#38bdf8') + ';color:' + (curLang === 'en' ? '#cbd5e1' : '#0b1020') + ';border:none;border-radius:18px;padding:5px 12px;font-size:0.82rem;font-weight:' + (curLang === 'en' ? '700' : '800') + ';cursor:pointer;transition:.15s">🇰🇷 한국어</button>' +
        '<button type="button" id="btnTrackFullLangEn" onclick="window.setBoardLanguage(\'en\')" style="background:' + (curLang === 'en' ? '#38bdf8' : 'transparent') + ';color:' + (curLang === 'en' ? '#0b1020' : '#cbd5e1') + ';border:none;border-radius:18px;padding:5px 12px;font-size:0.82rem;font-weight:' + (curLang === 'en' ? '800' : '700') + ';cursor:pointer;transition:.15s">🌐 English</button>';
      trackFull.appendChild(langSwitcher);
    }

    var existingCenterSwitcher = document.getElementById('modalCenterLangSwitcher');
    if (!existingCenterSwitcher) {
      var centerSwitcher = document.createElement('div');
      centerSwitcher.id = 'modalCenterLangSwitcher';
      centerSwitcher.style.cssText = 'margin:4px 0 16px;display:inline-flex;align-items:center;justify-content:center;background:#f0edef;border:1.5px solid #e4e2e4;border-radius:28px;padding:4px 8px;gap:5px;box-shadow:0 2px 10px rgba(19,27,46,.06);z-index:10';
      centerSwitcher.innerHTML = 
        '<span style="font-size:0.83rem;color:#45464d;font-weight:700;margin:0 4px 0 8px;display:inline-flex;align-items:center;gap:4px">' +
          '<span>🌐</span><span class="bilingual-ko">언어 선택:</span><span class="bilingual-en">Language:</span>' +
        '</span>' +
        '<button type="button" id="btnModalCenterLangKo" onclick="window.setBoardLanguage(\'ko\')" style="background:' + (curLang === 'en' ? 'transparent' : 'linear-gradient(135deg,#38bdf8 0%,#818cf8 100%)') + ';color:' + (curLang === 'en' ? '#cbd5e1' : '#0b1020') + ';border:none;border-radius:20px;padding:6px 16px;font-size:0.86rem;font-weight:' + (curLang === 'en' ? '700' : '800') + ';cursor:pointer;transition:all .18s;' + (curLang === 'en' ? '' : 'box-shadow:0 2px 10px rgba(56,189,248,.45)') + '">🇰🇷 한국어</button>' +
        '<button type="button" id="btnModalCenterLangEn" onclick="window.setBoardLanguage(\'en\')" style="background:' + (curLang === 'en' ? 'linear-gradient(135deg,#38bdf8 0%,#818cf8 100%)' : 'transparent') + ';color:' + (curLang === 'en' ? '#0b1020' : '#cbd5e1') + ';border:none;border-radius:20px;padding:6px 16px;font-size:0.86rem;font-weight:' + (curLang === 'en' ? '800' : '700') + ';cursor:pointer;transition:all .18s;' + (curLang === 'en' ? 'box-shadow:0 2px 10px rgba(56,189,248,.45)' : '') + '">🌐 English</button>';
      var h2 = trackFull.querySelector('h2');
      if (h2 && h2.nextSibling) {
        trackFull.insertBefore(centerSwitcher, h2.nextSibling);
      } else {
        trackFull.insertBefore(centerSwitcher, trackFull.firstChild);
      }
    }

    updateModalLangButtons(curLang);

    var currentUser = window.MatheduAuth ? window.MatheduAuth.getCurrentUser() : null;
    var currentGuest = window.MatheduAuth ? window.MatheduAuth.getCurrentGuest() : null;
    var solvedList = (window.MatheduAuth && window.MatheduAuth.getSolvedProblems) ? window.MatheduAuth.getSolvedProblems() : [];
    var prevProblem = solvedList.find(function(p) { return p.slug === currentSlug; });

    var studentNameInput = document.getElementById('studentName');
    var formDiv = trackFull.querySelector('div');

    // 1. 이미 정회원 또는 비회원으로 식별된 경우 자동 채움 및 이전 기록 안내
    if (currentUser) {
      if (studentNameInput) studentNameInput.value = currentUser.name;
      var h3 = trackFull.querySelector('h3');
      if (h3) {
        h3.innerHTML = '👤 <b>' + escapeHtml(currentUser.name) + '</b>' + bilingual('님 (' + escapeHtml(currentUser.roleLabel || '회원') + ')', ' (' + escapeHtml(currentUser.roleLabel || 'Member') + ')');
      }
      var p = trackFull.querySelector('p');
      if (p) {
        if (prevProblem) {
          p.innerHTML = bilingual(
            '📌 이전에 <b>' + prevProblem.stepDone + '/' + prevProblem.totalSteps + '단계</b>까지 풀이하셨습니다 (정답 <b>' + prevProblem.correct + '개</b>). 이어서 학습을 진행합니다.',
            '📌 Previously solved up to <b>Step ' + prevProblem.stepDone + '/' + prevProblem.totalSteps + '</b> (<b>' + prevProblem.correct + '</b> correct). Resuming practice.'
          );
        } else {
          p.innerHTML = bilingual('인증된 회원 계정으로 풀이 기록이 안전하게 저장됩니다.', 'Your progress is safely saved to your authenticated account.');
        }
      }
    } else if (currentGuest) {
      if (studentNameInput) studentNameInput.value = currentGuest.name;
      var h3 = trackFull.querySelector('h3');
      if (h3) {
        h3.innerHTML = '🧑‍🎓 <b>' + escapeHtml(currentGuest.name) + '</b>' + bilingual('님 (비회원 학습자)', ' (Guest Learner)');
      }
      var p = trackFull.querySelector('p');
      if (p) {
        if (prevProblem) {
          p.innerHTML = bilingual(
            '📌 이전에 <b>' + prevProblem.stepDone + '/' + prevProblem.totalSteps + '단계</b>까지 풀이하셨습니다 (정답 <b>' + prevProblem.correct + '개</b>). 이어서 계속 풀어보세요!',
            '📌 Previously solved up to <b>Step ' + prevProblem.stepDone + '/' + prevProblem.totalSteps + '</b> (<b>' + prevProblem.correct + '</b> correct). Continue solving!'
          );
        } else {
          p.innerHTML = bilingual('인식된 비회원 학습자 [' + escapeHtml(currentGuest.name) + ']님으로 풀이 기록이 저장됩니다.', 'Progress saved for recognized guest learner [' + escapeHtml(currentGuest.name) + '].');
        }
      }
    } else {
      // 익명 상태인 경우: 간편 비밀번호(PIN) 입력 필드 추가
      if (formDiv && !document.getElementById('studentPin')) {
        var pinInput = document.createElement('input');
        pinInput.type = 'password';
        pinInput.id = 'studentPin';
        pinInput.setAttribute('data-ko-placeholder', '간편비번 4자리 (선택)');
        pinInput.setAttribute('data-en-placeholder', '4-digit PIN (optional)');
        pinInput.placeholder = isEnMode() ? '4-digit PIN (optional)' : '간편비번 4자리 (선택)';
        pinInput.maxLength = 12;
        pinInput.style.cssText = 'background:#ffffff;color:#1b1b1d;border:1.5px solid #c5c6cd;border-radius:10px;padding:12px 14px;font-size:1.05rem;max-width:170px;text-align:center;outline:none;';
        pinInput.autocomplete = 'current-password';

        // 시작하기 버튼 앞에 삽입
        var startBtn = formDiv.querySelector('button');
        if (startBtn) {
          formDiv.insertBefore(pinInput, startBtn);
        } else {
          formDiv.appendChild(pinInput);
        }

        pinInput.addEventListener('keydown', function(e) {
          if (e.key === 'Enter') window.registerName();
        });

        var tipDiv = document.createElement('div');
        tipDiv.style.cssText = 'font-size:0.83rem;color:#006398;margin-top:12px;line-height:1.5;max-width:460px;text-align:center;word-break:keep-all';
        tipDiv.innerHTML = bilingual(
          '💡 <b>비회원 안내:</b> [이름]과 [간편 비밀번호]를 넣으시면 나중에 같은 문제에 오더라도 <b>동일 학습자로 자동 인식</b>되어 이전 풀이를 복원하고 <b>[내가 푼 문제]</b>를 모아볼 수 있습니다. (비번 미입력 시 익명 풀이)',
          '💡 <b>Guest Notice:</b> Entering [Name] and [4-digit PIN] lets the system <b>recognize you automatically</b> when returning, restoring previous steps and tracking your <b>[Solved Problems]</b>. (Anonymous if left blank)'
        );
        formDiv.parentNode.insertBefore(tipDiv, formDiv.nextSibling);
      }
    }

    // 0. [맨 위 배치] 사용자 요청: [👀 가입 없이 문제 열람 & 자유 풀기]를 모달 최상단에 배치하여 1초 만에 무장벽 진입 보장
    var existingTop = document.getElementById('btnTeacherPreviewInModal');
    if (!existingTop) {
      var topGuestBox = document.createElement('div');
      topGuestBox.id = 'topGuestFreePassRow';
      topGuestBox.style.cssText = 'margin:12px 0 16px;width:100%;max-width:440px;display:flex;flex-direction:column;align-items:center;gap:10px;';
      topGuestBox.innerHTML = 
        '<button type="button" id="btnTeacherPreviewInModal" style="width:100%;max-width:400px;background:linear-gradient(135deg,rgba(56,189,248,.25) 0%,rgba(99,102,241,.25) 100%);color:#e0f2fe;border:1.5px solid rgba(56,189,248,.65);border-radius:12px;padding:13px 20px;font-size:1.02rem;font-weight:800;cursor:pointer;transition:.18s;box-shadow:0 4px 16px rgba(56,189,248,.2);display:inline-flex;align-items:center;justify-content:center;gap:8px" ' +
          'onmouseover="this.style.background=\'linear-gradient(135deg,#38bdf8 0%,#6366f1 100%)\';this.style.color=\'#0b1020\';this.style.transform=\'scale(1.02)\';this.style.boxShadow=\'0 6px 20px rgba(56,189,248,.4)\'" ' +
          'onmouseout="this.style.background=\'linear-gradient(135deg,rgba(56,189,248,.25) 0%,rgba(99,102,241,.25) 100%)\';this.style.color=\'#e0f2fe\';this.style.transform=\'none\';this.style.boxShadow=\'0 4px 16px rgba(56,189,248,.2)\'">' +
          bilingual('👀 가입 없이 문제 열람 & 자유 풀기', '👀 Free Practice (No Signup)') +
        '</button>' +
        '<div style="font-size:0.81rem;color:#94a3b8;display:flex;align-items:center;gap:8px;width:100%;max-width:380px">' +
          '<span style="flex:1;height:1px;background:rgba(255,255,255,.15)"></span>' +
          '<span>' + bilingual('또는 이름을 입력하고 학습 기록 저장', 'Or enter name to save your progress') + '</span>' +
          '<span style="flex:1;height:1px;background:rgba(255,255,255,.15)"></span>' +
        '</div>';

      var h2 = trackFull.querySelector('h2');
      if (h2 && h2.nextSibling) {
        trackFull.insertBefore(topGuestBox, h2.nextSibling);
      } else {
        trackFull.insertBefore(topGuestBox, trackFull.firstChild);
      }
    }

    // 2. 하단 보조 액션 버튼 행 (내가 푼 문제 모아보기 + 회원 전환 + 오프라인 저장 + 교사 수업 개설)
    var actionRow = document.createElement('div');
    actionRow.style.cssText = 'margin-top:22px;padding-top:18px;border-top:1px solid #e4e2e4;display:flex;flex-direction:column;gap:12px;align-items:center;width:100%;max-width:540px;';

    var solvedCount = solvedList.length;

    actionRow.innerHTML = 
      '<div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap;align-items:center">' +
        '<button type="button" id="btnMyProblemsInModal" style="background:#ecfdf5;border:1px solid #a7f3d0;color:#047857;border-radius:10px;padding:9px 16px;font-size:0.86rem;font-weight:700;cursor:pointer;transition:.15s;display:inline-flex;align-items:center;gap:6px">' +
          bilingual('📂 내가 푼 문제 모아보기', '📂 My Solved Problems') + (solvedCount > 0 ? ' (' + solvedCount + ')' : '') +
        '</button>' +
        (!currentUser ? 
          '<button type="button" id="btnUpgradeInModal" style="background:#eef2ff;border:1px solid #c7d2fe;color:#4338ca;border-radius:10px;padding:9px 16px;font-size:0.86rem;font-weight:700;cursor:pointer;transition:.15s;display:inline-flex;align-items:center;gap:6px">' +
            bilingual('✨ 정식 회원 전환 / 가입', '✨ Upgrade to Member / Sign Up') +
          '</button>' : '') +
        '<button type="button" id="btnDownloadOfflineInModal" style="background:#f0f7ff;border:1px solid #bae6fd;color:#0369a1;border-radius:10px;padding:9px 16px;font-size:0.86rem;font-weight:700;cursor:pointer;transition:.15s;display:inline-flex;align-items:center;gap:6px" ' +
          'data-ko-title="인터넷 연결 없이 단독으로 풀 수 있는 HTML 파일로 저장" data-en-title="Download standalone HTML that runs without internet" ' +
          'title="' + (isEnMode() ? 'Download standalone HTML that runs without internet' : '인터넷 연결 없이 단독으로 풀 수 있는 HTML 파일로 저장') + '">' +
          bilingual('📥 오프라인 저장', '📥 Offline Save') +
        '</button>' +
      '</div>' +
      '<div style="margin-top:4px">' +
        '<button type="button" id="btnTeacherOpenInModal" style="background:#131b2e;color:#ffffff;border:1px solid #131b2e;border-radius:10px;padding:8px 18px;font-size:0.84rem;font-weight:700;cursor:pointer;transition:.15s;display:inline-flex;align-items:center;gap:6px">' +
          bilingual('👩‍🏫 선생님 전용: 3초 수업 개설 (QR)', '👩‍🏫 Teacher Only: 3-Sec Class Launch (QR)') +
        '</button>' +
      '</div>';

    trackFull.appendChild(actionRow);

    document.getElementById('btnMyProblemsInModal').onclick = function() {
      if (window.MatheduAuth) {
        window.MatheduAuth.showMyProblemsModal();
      }
    };

    var btnUpgrade = document.getElementById('btnUpgradeInModal');
    if (btnUpgrade) {
      btnUpgrade.onclick = function() {
        if (window.MatheduAuth) {
          window.MatheduAuth.showUpgradeModal();
        }
      };
    }

    var btnDownloadOffline = document.getElementById('btnDownloadOfflineInModal');
    if (btnDownloadOffline) {
      btnDownloadOffline.onclick = function() {
        if (window.downloadOfflineQuiz) {
          window.downloadOfflineQuiz(currentSlug);
        }
      };
    }

    window.startFreePractice = function() {
      var tf = document.getElementById('trackFull');
      if (tf) tf.remove();
      window._studentName = getVisitorAnonName();
      if (window.sendProgress) window.sendProgress();
      if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise();
    };

    var btnPreview = document.getElementById('btnTeacherPreviewInModal');
    if (btnPreview) {
      btnPreview.onclick = window.startFreePractice;
    }

    document.getElementById('btnTeacherOpenInModal').onclick = function() {
      trackFull.remove();
      openClassCreatorModal(currentSlug);
    };

    // 3. window.registerName 가로채기 (이름 + 간편비밀번호 SHA-256 검증 및 자동 연동)
    window.registerName = async function() {
      var nameInput = document.getElementById('studentName');
      var pinInput = document.getElementById('studentPin');
      var n = nameInput ? nameInput.value.trim() : '';
      var p = pinInput ? pinInput.value.trim() : '';

      if (!n) {
        alert(isEnMode() ? 'Please enter your name or student number.' : '이름 또는 출석번호를 입력하세요.');
        if (nameInput) nameInput.focus();
        return;
      }

      // 정회원인 경우
      if (window.MatheduAuth && window.MatheduAuth.getCurrentUser()) {
        window._studentName = n;
        finishRegister();
        return;
      }

      // 간편 비밀번호가 입력된 경우 -> 비회원 식별/등록
      if (p && window.MatheduAuth && window.MatheduAuth.loginGuest) {
        var res = await window.MatheduAuth.loginGuest(n, p);
        if (!res.success) {
          alert('⚠️ ' + res.message);
          if (pinInput) pinInput.focus();
          return;
        }
        window._studentName = n;
        finishRegister();
        return;
      }

      // 비번 미입력 상태이지만 기존 게스트 세션이 있는 경우
      var curG = window.MatheduAuth ? window.MatheduAuth.getCurrentGuest() : null;
      if (curG && curG.name.toLowerCase() === n.toLowerCase()) {
        window._studentName = n;
        finishRegister();
        return;
      }

      // 비번 없이 이름만 넣고 자유 풀이 시작
      window._studentName = n;
      finishRegister();

      function finishRegister() {
        var tf = document.getElementById('trackFull');
        if (tf) tf.remove();
        if (window.sendProgress) window.sendProgress();
        if (window.MathJax && MathJax.typesetPromise) {
          MathJax.typesetPromise();
        }

        // 이전 풀이 기록이 있을 경우 해당 단계로 부드럽게 스크롤 안내
        if (prevProblem && prevProblem.stepDone > 0) {
          setTimeout(function() {
            var qs = document.querySelectorAll('.q');
            var targetIdx = Math.min(prevProblem.stepDone, qs.length - 1);
            if (qs[targetIdx]) {
              qs[targetIdx].scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
          }, 350);
        }
      }
    };
  }

  function checkAndShowResumeBanner() {
    if (!window.MatheduAuth || !window.MatheduAuth.getSolvedProblems) return;
    var solvedList = window.MatheduAuth.getSolvedProblems();
    var prev = solvedList.find(function(p) { return p.slug === currentSlug; });
    if (!prev || prev.stepDone <= 0) return;

    // 이미 배너가 있다면 생략
    if (document.getElementById('problemResumeBanner')) return;

    var wrap = document.querySelector('.wrap');
    if (!wrap) return;

    var banner = document.createElement('div');
    banner.id = 'problemResumeBanner';
    banner.style.cssText = 'background:#ecfdf5;border:1px solid #a7f3d0;border-radius:12px;padding:12px 18px;margin:14px 0 18px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;animation:fadeIn .3s ease;';

    var pct = prev.totalSteps > 0 ? Math.round((prev.stepDone / prev.totalSteps) * 100) : 100;
    var statusText = prev.completed 
      ? bilingual('🏆 <b>완주 완료!</b> (' + prev.stepDone + '/' + prev.totalSteps + '단계 모두 해결)', '🏆 <b>Completed!</b> (All ' + prev.stepDone + '/' + prev.totalSteps + ' steps solved)')
      : bilingual('⚡ 이전에 <b>' + prev.stepDone + '/' + prev.totalSteps + '단계 (' + pct + '%)</b>까지 풀이하셨습니다.', '⚡ Previously solved up to <b>Step ' + prev.stepDone + '/' + prev.totalSteps + ' (' + pct + '%)</b>.');

    banner.innerHTML = 
      '<div style="font-size:0.88rem;color:#065f46;display:flex;align-items:center;gap:8px">' +
        '<span>📌</span>' +
        '<div>' + statusText + ' ' + bilingual('(정답: <b>' + prev.correct + '</b>문항)', '(Correct: <b>' + prev.correct + '</b>)') + '</div>' +
      '</div>' +
      '<div style="display:flex;gap:8px">' +
        '<button type="button" onclick="MatheduAuth.showMyProblemsModal()" style="background:#ffffff;border:1px solid #10b981;color:#047857;border-radius:8px;padding:5px 12px;font-size:0.8rem;cursor:pointer;font-weight:700">' +
          bilingual('📂 내 서재', '📂 My Library') +
        '</button>' +
        '<button type="button" onclick="document.getElementById(\'problemResumeBanner\').remove()" style="background:transparent;border:none;color:#94a3b8;font-size:1.1rem;cursor:pointer">✕</button>' +
      '</div>';

    var score = wrap.querySelector('.score') || wrap.querySelector('h1');
    if (score && score.nextSibling) {
      wrap.insertBefore(banner, score.nextSibling);
    } else {
      wrap.insertBefore(banner, wrap.firstChild);
    }
  }

  function injectProblemPageBanner() {
    if (document.querySelector('.stitch-gateway-grid') || document.querySelector('.stitch-hero-card')) return;
    var wrap = document.querySelector('.wrap');
    if (!wrap) return;

    var banner = document.createElement('div');
    banner.className = 'teacher-class-banner';
    banner.style.cssText = 'background:#ffffff;border:1px solid #e4e2e4;border-left:4px solid #006398;border-radius:14px;padding:14px 18px;margin:16px 0 20px;display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;box-shadow:0 2px 12px rgba(19,27,46,.05);';

    banner.innerHTML = 
      '<div>' +
        '<div style="font-weight:800;font-size:1rem;color:#131b2e;display:flex;align-items:center;gap:6px">' +
          bilingual('👩‍🏫 이 문제로 학급 수업을 시작할 수 있습니다', '👩‍🏫 Start a Classroom Lesson with This Problem') +
        '</div>' +
        '<div style="font-size:0.83rem;color:#45464d;margin-top:3px">' +
          bilingual('회원 로그인 후 3초 만에 수업 코드를 만들고, 교실 칠판에 학생용 대형 QR코드를 띄워보세요.', 'Generate a class session code in 3 seconds and display a projector QR code on the blackboard.') +
        '</div>' +
      '</div>' +
      '<button type="button" onclick="openClassCreatorModal(\'' + currentSlug + '\')" style="background:#131b2e;color:#ffffff;border:none;border-radius:10px;padding:10px 20px;font-size:0.9rem;font-weight:800;cursor:pointer;box-shadow:0 2px 8px rgba(19,27,46,.15);transition:.15s;display:inline-flex;align-items:center;gap:6px">' +
        bilingual('🚀 이 문제로 수업 열기 (QR / 대시보드)', '🚀 Open Classroom (QR / Dashboard)') +
      '</button>';

    var h1 = wrap.querySelector('h1');
    if (h1 && h1.nextSibling) {
      wrap.insertBefore(banner, h1.nextSibling);
    } else {
      var topbar = wrap.querySelector('.topbar') || wrap.querySelector('.navbar');
      if (topbar && topbar.nextSibling) {
        wrap.insertBefore(banner, topbar.nextSibling);
      }
    }
  }

  function injectFloatingClassButton() {
    if (document.querySelector('.stitch-bottom-nav') || document.getElementById('floatClassBtn')) return;
    var floatBtn = document.createElement('button');
    floatBtn.id = 'floatClassBtn';
    floatBtn.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:9998;background:#131b2e;color:#ffffff;border:1px solid rgba(255,255,255,.15);border-radius:30px;padding:12px 22px;font-size:0.92rem;font-weight:800;cursor:pointer;box-shadow:0 8px 24px rgba(19,27,46,.22);display:flex;align-items:center;gap:8px;transition:.2s';
    floatBtn.innerHTML = bilingual('🚀 이 문제로 수업 열기', '🚀 Open Classroom');
    floatBtn.setAttribute('data-ko-title', '3초 만에 고유 수업 코드 및 빔프로젝터 QR 발급 (회원 전용)');
    floatBtn.setAttribute('data-en-title', 'Instant class code & projector QR in 3 seconds (Teachers)');
    floatBtn.title = isEnMode() ? floatBtn.getAttribute('data-en-title') : floatBtn.getAttribute('data-ko-title');

    floatBtn.onmouseover = function() { floatBtn.style.transform = 'translateY(-2px) scale(1.03)'; };
    floatBtn.onmouseout = function() { floatBtn.style.transform = 'translateY(0) scale(1)'; };
    floatBtn.onclick = function() { openClassCreatorModal(currentSlug); };

    document.body.appendChild(floatBtn);
  }

  function injectTopbarButtons() {
    if (document.querySelector('.stitch-app-header')) {
      try {
        if (window.MatheduGame && window.MatheduGame.getStreak) {
          var st = window.MatheduGame.getStreak();
          var hs = document.getElementById('stitchHeaderStreak');
          if (hs) hs.textContent = (st && st.count > 0) ? st.count : 14;
        }
      } catch(e) {}
      return;
    }
    var topbar = document.querySelector('.topbar') || document.querySelector('.navbar');
    if (!topbar) return;

    // 1. [📂 내가 푼 문제] 학습 서재 버튼
    if (!document.getElementById('btnMyLibraryTopbar')) {
      var libBtn = document.createElement('button');
      libBtn.id = 'btnMyLibraryTopbar';
      libBtn.className = 'tbtn navbtn';
      libBtn.style.cssText = 'background:#ffffff;border:1px solid #e4e2e4;color:#1b1b1d;font-weight:700;cursor:pointer;display:inline-flex;align-items:center;gap:6px;border-radius:10px;padding:6px 12px;font-size:0.84rem;transition:.15s;text-decoration:none;';
      
      function updateLibBtnText() {
        var count = (window.MatheduAuth && window.MatheduAuth.getSolvedProblems) ? window.MatheduAuth.getSolvedProblems().length : 0;
        var badge = count > 0 ? ' <span style="background:rgba(0,99,152,.12);color:#006398;padding:1px 6px;border-radius:10px;font-size:0.75rem">' + count + '</span>' : '';
        libBtn.innerHTML = bilingual('📂 내가 푼 문제' + badge, '📂 Solved' + badge);
      }
      updateLibBtnText();
      libBtn.onclick = function() {
        if (window.MatheduAuth) window.MatheduAuth.showMyProblemsModal();
      };

      topbar.appendChild(libBtn);
      window.addEventListener('mathedu:solved-updated', updateLibBtnText);
      window.addEventListener('mathedu:auth-changed', updateLibBtnText);
    }

    // 2. [🚀 수업 열기 (QR)] 버튼
    if (!document.getElementById('btnTeacherTopbar')) {
      var teacherBtn = document.createElement('button');
      teacherBtn.id = 'btnTeacherTopbar';
      teacherBtn.className = 'tbtn navbtn';
      teacherBtn.style.cssText = 'background:#f0f7ff;border:1px solid rgba(0,99,152,.25);color:#006398;font-weight:700;cursor:pointer;display:inline-flex;align-items:center;gap:6px;border-radius:10px;padding:6px 12px;font-size:0.84rem;transition:.15s;';
      teacherBtn.innerHTML = bilingual('🚀 수업 열기 (QR)', '🚀 Open Class (QR)');
      teacherBtn.setAttribute('data-ko-title', '선생님을 위한 3초 수업 생성 및 QR 발급 (회원 전용)');
      teacherBtn.setAttribute('data-en-title', '3-second class creation & QR code for teachers (Members)');
      teacherBtn.title = isEnMode() ? teacherBtn.getAttribute('data-en-title') : teacherBtn.getAttribute('data-ko-title');
      teacherBtn.onclick = function() {
        openClassCreatorModal(currentSlug);
      };

      topbar.appendChild(teacherBtn);
    }

    // 3. [📥 오프라인 저장] 버튼
    if (!document.getElementById('btnOfflineTopbar')) {
      var offlineBtn = document.createElement('button');
      offlineBtn.id = 'btnOfflineTopbar';
      offlineBtn.className = 'tbtn navbtn';
      offlineBtn.style.cssText = 'background:#ffffff;border:1px solid #e4e2e4;color:#006398;font-weight:700;cursor:pointer;display:inline-flex;align-items:center;gap:6px;border-radius:10px;padding:6px 12px;font-size:0.84rem;transition:.15s;';
      offlineBtn.innerHTML = bilingual('📥 오프라인 저장', '📥 Save Offline');
      offlineBtn.setAttribute('data-ko-title', '인터넷 없이 풀 수 있는 단독 오프라인 HTML 파일로 다운로드');
      offlineBtn.setAttribute('data-en-title', 'Download standalone offline HTML file that runs without internet');
      offlineBtn.title = isEnMode() ? offlineBtn.getAttribute('data-en-title') : offlineBtn.getAttribute('data-ko-title');
      offlineBtn.onclick = function(e) {
        if (window.downloadOfflineQuiz) {
          window.downloadOfflineQuiz(currentSlug);
        }
      };

      topbar.appendChild(offlineBtn);
    }
    // 4. [⭐ 즐겨찾기] 버튼
    if (!document.getElementById('btnBookmarkTopbar')) {
      var bmBtn = document.createElement('button');
      bmBtn.id = 'btnBookmarkTopbar';
      bmBtn.className = 'tbtn navbtn';
      bmBtn.style.cssText = 'background:#fffbeb;border:1px solid #fde68a;color:#b45309;font-weight:700;cursor:pointer;display:inline-flex;align-items:center;gap:6px;border-radius:10px;padding:6px 12px;font-size:0.84rem;transition:.15s;';
      
      function updateBmBtn() {
        var isBm = (window.MatheduGame && window.MatheduGame.isBookmarked) ? window.MatheduGame.isBookmarked(currentSlug) : false;
        bmBtn.innerHTML = isBm ? bilingual('★ 즐겨찾기됨', '★ Bookmarked') : bilingual('☆ 즐겨찾기', '☆ Bookmark');
        bmBtn.style.background = isBm ? '#fef3c7' : '#fffbeb';
        bmBtn.style.color = isBm ? '#92400e' : '#b45309';
      }
      updateBmBtn();
      bmBtn.onclick = function() {
        if (window.MatheduGame && window.MatheduGame.toggleBookmark) {
          window.MatheduGame.toggleBookmark(currentSlug);
          updateBmBtn();
        }
      };
      topbar.appendChild(bmBtn);
      window.addEventListener('mathedu:bookmarks-updated', updateBmBtn);
    }

    // 5. [🖨️ A4 학습지 인쇄] 버튼 (교사용/학생 출력용)
    if (!document.getElementById('btnPrintWorksheetTopbar')) {
      var printBtn = document.createElement('button');
      printBtn.id = 'btnPrintWorksheetTopbar';
      printBtn.className = 'tbtn navbtn';
      printBtn.style.cssText = 'background:#ffffff;border:1px solid #e4e2e4;color:#1b1b1d;font-weight:700;cursor:pointer;display:inline-flex;align-items:center;gap:6px;border-radius:10px;padding:6px 12px;font-size:0.84rem;transition:.15s;';
      printBtn.innerHTML = bilingual('🖨️ A4 학습지 인쇄', '🖨️ Print Worksheet');
      printBtn.setAttribute('data-ko-title', '교실 유인물 및 학생 필기 공간이 포함된 규격 A4 시험지 인쇄/PDF 저장');
      printBtn.setAttribute('data-en-title', 'Print standard A4 worksheet with student note area / Save PDF');
      printBtn.title = isEnMode() ? printBtn.getAttribute('data-en-title') : printBtn.getAttribute('data-ko-title');
      printBtn.onclick = function() {
        if (window.MatheduGame && window.MatheduGame.printWorksheet) {
          window.MatheduGame.printWorksheet();
        } else {
          window.print();
        }
      };
      topbar.appendChild(printBtn);
    }

    // 6. [🖥️ 칠판 모드] 버튼 (교실 빔프로젝터/전자칠판 판서용 고대비 뷰)
    if (!document.getElementById('btnChalkboardModeTopbar')) {
      var chalkBtn = document.createElement('button');
      chalkBtn.id = 'btnChalkboardModeTopbar';
      chalkBtn.className = 'tbtn navbtn';
      chalkBtn.style.cssText = 'background:#ecfdf5;border:1px solid #a7f3d0;color:#047857;font-weight:700;cursor:pointer;display:inline-flex;align-items:center;gap:6px;border-radius:10px;padding:6px 12px;font-size:0.84rem;transition:.15s;';
      chalkBtn.innerHTML = bilingual('🖥️ 칠판 모드', '🖥️ Board Mode');
      chalkBtn.setAttribute('data-ko-title', '교실 칠판 판서 및 빔프로젝터 투사를 위한 초대형 폰트 & 고대비 뷰');
      chalkBtn.setAttribute('data-en-title', 'High-contrast large font view for classroom chalkboard / projector');
      chalkBtn.title = isEnMode() ? chalkBtn.getAttribute('data-en-title') : chalkBtn.getAttribute('data-ko-title');
      chalkBtn.onclick = function() {
        if (window.MatheduGame && window.MatheduGame.toggleChalkboardMode) {
          window.MatheduGame.toggleChalkboardMode();
        }
      };
      topbar.appendChild(chalkBtn);
    }
  }

  // === 오늘의 수업 팩(?pack=slug1,slug2,...) 가이드 바 ===
  function injectLessonPackBanner() {
    var packParam = (urlParams.get('pack') || '').trim();
    if (!packParam) return;

    var slugs = packParam.split(',').map(function(s) { return s.trim().replace(/\.html$/, ''); }).filter(Boolean);
    if (slugs.length <= 1) return;

    var curIdx = slugs.indexOf(currentSlug);
    if (curIdx === -1) return;

    var wrap = document.querySelector('.wrap');
    if (!wrap) return;

    var packBar = document.createElement('div');
    packBar.className = 'lesson-pack-nav-bar';
    packBar.style.cssText = 'background:#eef2ff;border:1.5px solid #c7d2fe;border-radius:14px;padding:12px 18px;margin:12px 0 16px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;box-shadow:0 2px 10px rgba(19,27,46,.05);animation:matheduFadeIn .3s ease';

    var prevSlug = curIdx > 0 ? slugs[curIdx - 1] : null;
    var nextSlug = curIdx < slugs.length - 1 ? slugs[curIdx + 1] : null;
    var rParam = roomId ? ('&room=' + encodeURIComponent(roomId)) : '';

    var dotsHtml = slugs.map(function(s, idx) {
      var isCurrent = (idx === curIdx);
      var linkUrl = s + '.html?pack=' + encodeURIComponent(packParam) + rParam;
      var dotTitle = (idx + 1) + (isEnMode() ? ' Problem' : '번 문제');
      return (
        '<a href="' + linkUrl + '" style="display:inline-block;width:' + (isCurrent ? '24px' : '10px') + ';height:10px;border-radius:5px;background:' + (isCurrent ? '#a78bfa' : 'rgba(255,255,255,.25)') + ';transition:.2s;text-decoration:none" title="' + dotTitle + '">' +
        '</a>'
      );
    }).join('');

    packBar.innerHTML = 
      '<div style="display:flex;align-items:center;gap:10px">' +
        '<span style="font-size:1.2rem">🎒</span>' +
        '<div>' +
          '<div style="font-size:0.92rem;font-weight:800;color:#3730a3">' +
            bilingual('오늘의 수업 팩 진행 중 (문제 ' + (curIdx + 1) + ' / ' + slugs.length + ')', 'Lesson Pack in Progress (Problem ' + (curIdx + 1) + ' / ' + slugs.length + ')') +
          '</div>' +
          '<div style="display:flex;gap:4px;align-items:center;margin-top:4px">' + dotsHtml + '</div>' +
        '</div>' +
      '</div>' +
      '<div style="display:flex;gap:8px;align-items:center">' +
        (prevSlug ? ('<a href="' + prevSlug + '.html?pack=' + encodeURIComponent(packParam) + rParam + '" class="tbtn" style="padding:5px 12px;font-size:0.8rem">' + bilingual('◀ 이전 문제', '◀ Previous') + '</a>') : '') +
        (nextSlug ? ('<a href="' + nextSlug + '.html?pack=' + encodeURIComponent(packParam) + rParam + '" class="tbtn" style="background:linear-gradient(90deg,#a78bfa,#7cc4ff);color:#0b1020;border:none;padding:6px 14px;font-size:0.82rem;font-weight:800">' + bilingual('다음 문제 ▶', 'Next ▶') + '</a>') : '<span style="font-size:0.8rem;color:#5eead4;font-weight:700">' + bilingual('🏁 마지막 문항', '🏁 Final Problem') + '</span>') +
      '</div>';

    var topbar = wrap.querySelector('.topbar') || wrap.querySelector('.navbar');
    if (topbar && topbar.nextSibling) {
      wrap.insertBefore(packBar, topbar.nextSibling);
    } else {
      wrap.insertBefore(packBar, wrap.firstChild);
    }
  }

  // === 학생 오답 감지기 (오답 선택 시 오답노트에 자동 수집) ===
  function attachWrongAnswerTracker() {
    document.addEventListener('click', function(e) {
      var opt = e.target.closest ? e.target.closest('.opt') : null;
      if (!opt) return;

      setTimeout(function() {
        if (opt.classList.contains('wrong')) {
          var qEl = opt.closest('.q');
          var qIdx = qEl ? Array.from(document.querySelectorAll('.q')).indexOf(qEl) + 1 : 1;
          var h1 = document.querySelector('h1');
          var pageTitle = h1 ? h1.textContent.trim().replace(/^📘\s*/, '') : currentSlug;

          if (window.MatheduGame && window.MatheduGame.recordWrongAnswer) {
            window.MatheduGame.recordWrongAnswer(currentSlug, qIdx, pageTitle);
          }
        }
      }, 100);
    });
  }

  var _lastDoneSteps = 0;
  var _hasTriggeredCompletion = false;

  function patchSendProgress() {
    window.sendProgress = function() {
      var name = (window._studentName || '').trim();
      if (!name || name === '자유 학습자' || name === 'Guest Learner') {
        name = getVisitorAnonName();
        window._studentName = name;
      }

      var qs = document.querySelectorAll('.q');
      var total = qs.length;
      var done = document.querySelectorAll('.q.done');
      var correct = 0;
      done.forEach(function(q) {
        if (q.querySelector('.opt.correct')) correct++;
      });
      if (total === 0) return;

      var rId = window._roomId || '';
      var studentNameWithRoom = rId ? (name + ' [' + rId + ']') : name;

      var payload = {
        quiz_slug: currentSlug,
        student_name: studentNameWithRoom,
        room_id: rId,
        raw_name: name,
        current_step: done.length,
        total_steps: total,
        correct: correct
      };

      // === MatheduAuth 푼 문제 기록 저장 (기기 캐시 + 비회원 게스트 DB + 정회원 DB) ===
      var h1 = document.querySelector('h1');
      var pageTitle = h1 ? h1.textContent.trim() : (document.title || currentSlug);
      pageTitle = pageTitle.replace(/^📘\s*/, '').trim();

      if (window.MatheduAuth && window.MatheduAuth.recordSolvedProblem) {
        window.MatheduAuth.recordSolvedProblem(currentSlug, {
          title: pageTitle,
          stepDone: done.length,
          totalSteps: total,
          correct: correct,
          completed: (total > 0 && done.length >= total)
        });
      }

      // === 게이미피케이션 XP 및 축하 연출 ===
      if (window.MatheduGame) {
        if (done.length > _lastDoneSteps) {
          var stepDiff = done.length - _lastDoneSteps;
          _lastDoneSteps = done.length;
          window.MatheduGame.addXP(stepDiff * 10, isEnMode() ? 'Step Cleared' : '디딤돌 통과');
          window.MatheduGame.unlockBadge('first_step');
        }

        // 전체 완료 시 축하 폭죽(Confetti) & 출석 스트릭 & 대형 보너스
        if (done.length >= total && !_hasTriggeredCompletion) {
          _hasTriggeredCompletion = true;
          window.MatheduGame.addXP(50, isEnMode() ? '🎉 Problem Completed Bonus' : '🎉 문제 완주 축하 보너스');
          window.MatheduGame.recordActivity();
          window.MatheduGame.unlockBadge('full_clear');
          if (correct === total) {
            window.MatheduGame.unlockBadge('perfect_run');
          }
          window.MatheduGame.clearWrongAnswer(currentSlug);
          window.MatheduGame.triggerConfetti(4000);

          // 수업 팩 연계 안내
          var packParam = (urlParams.get('pack') || '').trim();
          if (packParam) {
            var slugs = packParam.split(',').map(function(s) { return s.trim(); });
            var curIdx = slugs.indexOf(currentSlug);
            if (curIdx !== -1 && curIdx < slugs.length - 1) {
              var nextSlug = slugs[curIdx + 1];
              var rParam = roomId ? ('&room=' + encodeURIComponent(roomId)) : '';
              var nextUrl = nextSlug + '.html?pack=' + encodeURIComponent(packParam) + rParam;
              setTimeout(function() {
                var fin = document.querySelector('.final');
                if (fin && !document.getElementById('btnNextPackQuestion')) {
                  var nextBtn = document.createElement('a');
                  nextBtn.id = 'btnNextPackQuestion';
                  nextBtn.href = nextUrl;
                  nextBtn.className = 'btn';
                  nextBtn.style.cssText = 'display:inline-block;margin-top:14px;background:linear-gradient(90deg,#5eead4,#38bdf8);color:#0b1020;padding:12px 28px;font-size:1.05rem;font-weight:800;text-decoration:none;border-radius:12px;box-shadow:0 8px 24px rgba(94,234,212,.4);animation:matheduPopUp .3s ease';
                  nextBtn.innerHTML = bilingual('🚀 다음 ' + (curIdx + 2) + '번 문제로 계속하기 ➔', '🚀 Continue to Problem #' + (curIdx + 2) + ' ➔');
                  fin.appendChild(nextBtn);
                }
              }, 600);
            }
          }
        }
      }

      if (window._sheetsApiUrl) {
        fetch(window._sheetsApiUrl, {
          method: 'POST',
          mode: 'no-cors',
          keepalive: true,
          headers: { 'Content-Type': 'text/plain;charset=utf-8' },
          body: JSON.stringify(payload)
        }).catch(function(e) {
          console.warn('[mathedu] sendProgress error', e);
        });
      }
    };
  }

  /* ══════════════════════════════════════════════════════════════
     🪜 차분한 단계별 몰입형 순차 공개 시스템 (Progressive Scaffolding Focus Mode)
     한 화면에 모든 문제가 펼쳐져 있어 스크롤로 훑어내려가는 불상사를 방지하고,
     학생이 한 번에 하나의 디딤돌에만 온전히 깊이 고민할 수 있도록 제어
     ══════════════════════════════════════════════════════════════ */
  function initProgressiveScaffolding() {
    var qs = Array.from(document.querySelectorAll('.q'));
    if (qs.length <= 1) return; // 문항이 1개뿐이면 분절화 불필요

    // 0. trackFull(입장 모달) 등 고정 오버레이 요소가 .wrap 내부에 있다면 document.body로 안전하게 이동하여 문항 형제 간섭 원천 배제
    var tfModal = document.getElementById('trackFull');
    if (tfModal && tfModal.parentNode && tfModal.parentNode !== document.body) {
      document.body.appendChild(tfModal);
    }
    if (tfModal) {
      tfModal.classList.remove('mathedu-step-hidden');
    }

    // 1. 필수 CSS 주입
    if (!document.getElementById('mathedu-scaffolding-focus-styles')) {
      var st = document.createElement('style');
      st.id = 'mathedu-scaffolding-focus-styles';
      st.textContent = 
        '.mathedu-step-hidden { display: none !important; }\n' +
        '.mathedu-step-unlocked { animation: matheduStepFadeIn 0.35s ease-out forwards; }\n' +
        '@keyframes matheduStepFadeIn { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }\n' +
        '.mathedu-step-mode-switch { display: inline-flex; align-items: center; gap: 5px; background: #f0edef; border: 1px solid var(--line); border-radius: 20px; padding: 4px 12px; font-size: 0.78rem; font-weight: 700; color: var(--txt); cursor: pointer; transition: .15s; }\n' +
        '.mathedu-step-mode-switch:hover { border-color: var(--accent); color: #fff; background: #131b2e; }\n' +
        '.mathedu-next-step-hint { background: #f0f7ff; border: 1.5px dashed rgba(0,99,152,.35); border-radius: var(--radius); padding: 18px 22px; margin: 24px 0; text-align: center; color: #006398; font-size: 0.92rem; font-weight: 700; box-shadow: 0 2px 10px rgba(19,27,46,.04); }\n' +
        '.mathedu-step-progress-badge { display: inline-flex; align-items: center; gap: 6px; background: rgba(0,99,152,.10); color: #006398; border: 1px solid rgba(0,99,152,.25); border-radius: 12px; padding: 2px 10px; font-size: 0.76rem; font-weight: 800; margin-bottom: 6px; }\n' +
        '.viral-share-card { display: none !important; }\n'; // 번잡한 바이럴 카드 숨김
      (document.head || document.documentElement).appendChild(st);
    }

    var isFocusMode = false; // 기본값: Stitch 전체 카드 수직 스크롤 모드 (단계별 집중 모드 선택 가능)
    try {
      var saved = localStorage.getItem('mathedu_step_mode');
      if (saved === 'focus') isFocusMode = true;
    } catch(e) {}
    window.toggleStitchStepMode = function(mode) {
      if (mode === 'focus') isFocusMode = true;
      else if (mode === 'all') isFocusMode = false;
      else isFocusMode = !isFocusMode;
      try { localStorage.setItem('mathedu_step_mode', isFocusMode ? 'focus' : 'all'); } catch(e) {}
      updateSwitchText();
      applyStepVisibility(false);
      document.querySelectorAll('[data-stitch-mode-pill]').forEach(function(btn) {
        btn.classList.toggle('active', btn.getAttribute('data-stitch-mode-pill') === (isFocusMode ? 'focus' : 'all'));
      });
    };

    // 최종 해설 요소들 (.sol, .final 및 관련 제목)
    var solEl = document.querySelector('.sol');
    var finalHeading = solEl ? solEl.previousElementSibling : null;
    var finalEl = document.querySelector('.final');

    // 상단 점수 바 또는 상단 네비게이션에 모드 전환 버튼 배치
    var scoreBar = document.querySelector('.score') || document.querySelector('.topbar');
    var switchBtn = document.createElement('button');
    switchBtn.type = 'button';
    switchBtn.className = 'mathedu-step-mode-switch';
    switchBtn.id = 'btnStepModeSwitch';

    function updateSwitchText() {
      switchBtn.innerHTML = isFocusMode 
        ? bilingual('🪜 단계별 집중 모드', '🪜 Step Focus Mode')
        : bilingual('📖 전체 펼쳐보기', '📖 View All Steps');
      switchBtn.title = isFocusMode
        ? (isEnMode() ? 'Switch to view all steps at once' : '전체 문제를 한 번에 펼쳐보기')
        : (isEnMode() ? 'Switch to step-by-step focus mode' : '차분한 단계별 집중 풀기 모드로 전환');
    }
    updateSwitchText();

    switchBtn.onclick = function() {
      isFocusMode = !isFocusMode;
      try { localStorage.setItem('mathedu_step_mode', isFocusMode ? 'focus' : 'all'); } catch(e) {}
      updateSwitchText();
      applyStepVisibility(true);
    };

    if (scoreBar) {
      scoreBar.appendChild(switchBtn);
    }

    function applyStepVisibility(shouldScroll) {
      if (!isFocusMode) {
        // 전체 펼쳐보기: 모든 숨김 해제
        document.querySelectorAll('.mathedu-step-hidden').forEach(function(el) {
          el.classList.remove('mathedu-step-hidden');
        });
        if (solEl) solEl.classList.remove('mathedu-step-hidden');
        if (finalHeading) finalHeading.classList.remove('mathedu-step-hidden');
        if (finalEl) finalEl.classList.remove('mathedu-step-hidden');
        var hintBox = document.getElementById('matheduNextStepHintBox');
        if (hintBox) hintBox.remove();
        return;
      }

      // 단계별 집중 모드: 아직 안 푼 첫 번째 문제까지 표시
      var firstUnsolvedIndex = -1;
      for (var i = 0; i < qs.length; i++) {
        if (!qs[i].classList.contains('done')) {
          firstUnsolvedIndex = i;
          break;
        }
      }

      var allDone = (firstUnsolvedIndex === -1);
      var maxVisibleIndex = allDone ? (qs.length - 1) : firstUnsolvedIndex;

      for (var idx = 0; idx < qs.length; idx++) {
        var q = qs[idx];
        var isVisible = (idx <= maxVisibleIndex);

        if (isVisible) {
          if (q.classList.contains('mathedu-step-hidden')) {
            q.classList.remove('mathedu-step-hidden');
            q.classList.add('mathedu-step-unlocked');
          }
        } else {
          q.classList.add('mathedu-step-hidden');
        }

        // q 바로 앞의 형제 요소들(개념 카드, h2, h3, .know, .sym-card 등)도 동일하게 연동
        // 단, qs[0] 이전의 인트로 및 원본 문제는 항상 표시
        if (idx > 0) {
          var prev = q.previousElementSibling;
          while (prev && prev !== qs[idx - 1] && !prev.classList.contains('q')) {
            // 입장 모달, 다이얼로그, 시스템 스크립트/스타일은 스캐폴딩 숨김 대상에서 절대 제외
            var isModalOrSpecial = (prev.id === 'trackFull' || prev.id === 'topGuestFreePassRow' || 
                                    prev.classList.contains('mathedu-modal') || prev.classList.contains('mathedu-dialog') || 
                                    prev.tagName === 'SCRIPT' || prev.tagName === 'STYLE');
            if (isModalOrSpecial) {
              prev = prev.previousElementSibling;
              continue;
            }

            // 단, .sol(최종 해설 본문)은 마지막 문항까지 풀기 전에는 절대 노출하지 않음 (제목인 finalHeading은 최종 문항 도달 시 표시)
            var isSolRelated = (prev === solEl || prev.classList.contains('sol'));
            var isQPart = (prev.classList.contains('opts') || prev.classList.contains('q-actions') || 
                           prev.classList.contains('exp') || prev.classList.contains('report-wrap') || 
                           prev.classList.contains('opt'));
            if (isSolRelated) {
              if (allDone) prev.classList.remove('mathedu-step-hidden');
              else prev.classList.add('mathedu-step-hidden');
            } else if (isQPart) {
              // 앞선 문항(qs[idx - 1])에 속한 보기/해설/신고 폼인 경우, 앞 문항이 보이면 항상 표시
              var prevVisible = ((idx - 1) <= maxVisibleIndex);
              if (prevVisible) prev.classList.remove('mathedu-step-hidden');
              else prev.classList.add('mathedu-step-hidden');
            } else {
              if (isVisible) prev.classList.remove('mathedu-step-hidden');
              else prev.classList.add('mathedu-step-hidden');
            }
            prev = prev.previousElementSibling;
          }
        }
      }

      // qs[last] 뒤에 위치한 요소들(결과, 최종 풀이 등) 제어
      if (solEl) {
        if (allDone) solEl.classList.remove('mathedu-step-hidden');
        else solEl.classList.add('mathedu-step-hidden');
      }
      if (finalHeading) {
        if (maxVisibleIndex >= qs.length - 1) finalHeading.classList.remove('mathedu-step-hidden');
        else finalHeading.classList.add('mathedu-step-hidden');
      }
      if (finalEl) {
        if (allDone) finalEl.classList.remove('mathedu-step-hidden');
        else finalEl.classList.add('mathedu-step-hidden');
      }

      // qs[qs.length - 1] 뒤의 다른 형제 요소들도 allDone 전에는 숨김
      var lastQ = qs[qs.length - 1];
      var nextAfterLast = lastQ ? lastQ.nextElementSibling : null;
      while (nextAfterLast) {
        var isSpecial = (nextAfterLast.id === 'matheduNextStepHintBox' || 
                         nextAfterLast.id === 'trackFull' || 
                         nextAfterLast.id === 'topGuestFreePassRow' || 
                         nextAfterLast.classList.contains('mathedu-modal') || 
                         nextAfterLast.classList.contains('mathedu-dialog') || 
                         nextAfterLast.tagName === 'SCRIPT' || 
                         nextAfterLast.tagName === 'STYLE');
        if (!isSpecial) {
          if (allDone) nextAfterLast.classList.remove('mathedu-step-hidden');
          else nextAfterLast.classList.add('mathedu-step-hidden');
        }
        nextAfterLast = nextAfterLast.nextElementSibling;
      }

      // 다음 디딤돌 잠금 안내 박스
      var hintBox = document.getElementById('matheduNextStepHintBox');
      if (!allDone && isFocusMode) {
        if (!hintBox) {
          hintBox = document.createElement('div');
          hintBox.id = 'matheduNextStepHintBox';
          hintBox.className = 'mathedu-next-step-hint';
        }
        var nextStepNum = maxVisibleIndex + 1;
        var totalStepNum = qs.length;
        hintBox.innerHTML = 
          '<div class="mathedu-step-progress-badge">' +
            bilingual('진행 중: ' + nextStepNum + ' / ' + totalStepNum + ' 단계', 'Progress: Step ' + nextStepNum + ' of ' + totalStepNum) +
          '</div>' +
          '<div>' +
            bilingual(
              '💡 <b>' + nextStepNum + '단계 디딤돌</b>을 차분히 풀면 다음 단계가 열립니다.<br><span style="font-size:0.82rem;color:var(--sub);font-weight:400">앞 단계를 해결하면서 수학적 원리를 한 계단씩 스스로 깨우쳐보세요.</span>',
              '💡 Solve <b>Step ' + nextStepNum + '</b> to unlock the next step.<br><span style="font-size:0.82rem;color:var(--sub);font-weight:400">Think calmly and take your time with each mathematical step.</span>'
            ) +
          '</div>';

        var curQ = qs[maxVisibleIndex];
        // curQ에 속한 뒤따르는 형제 요소(.opts, .q-actions, .exp, .report-wrap)가 있다면 그 뒤에 안내 박스 배치
        var insertAnchor = curQ;
        while (insertAnchor && insertAnchor.nextElementSibling && 
               (insertAnchor.nextElementSibling.classList.contains('opts') ||
                insertAnchor.nextElementSibling.classList.contains('q-actions') ||
                insertAnchor.nextElementSibling.classList.contains('exp') ||
                insertAnchor.nextElementSibling.classList.contains('report-wrap'))) {
          insertAnchor = insertAnchor.nextElementSibling;
        }
        if (insertAnchor && insertAnchor.nextSibling) {
          insertAnchor.parentNode.insertBefore(hintBox, insertAnchor.nextSibling);
        } else if (insertAnchor) {
          insertAnchor.parentNode.appendChild(hintBox);
        }
      } else if (hintBox) {
        hintBox.remove();
      }

      if (shouldScroll && maxVisibleIndex < qs.length) {
        setTimeout(function() {
          var targetQ = qs[maxVisibleIndex];
          if (targetQ) {
            targetQ.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }
        }, 150);
      }
    }

    // 옵션 클릭 감지하여 자동 다음 단계 언락
    document.addEventListener('click', function(e) {
      var opt = e.target.closest ? e.target.closest('.opt') : null;
      if (!opt) return;
      setTimeout(function() {
        applyStepVisibility(true);
      }, 60);
    });

    // 초기 적용
    applyStepVisibility(false);
  }

  function ensureAuth(actionName, callback) {
    if (window.MatheduAuth) {
      window.MatheduAuth.requireAuth(actionName, callback);
      return;
    }
    ensureAuthLoaded(function() {
      if (window.MatheduAuth) {
        window.MatheduAuth.requireAuth(actionName, callback);
      } else {
        callback({ name: isEnMode() ? 'Teacher' : '선생님', roleLabel: isEnMode() ? 'Teacher' : '교사' });
      }
    });
  }

  // 교사용 수업 생성기 모달 (회원 전용)
  window.openClassCreatorModal = function(slug) {
    ensureAuth(isEnMode() ? 'Launch Classroom' : '수업 개설 및 배포', function(currentUser) {
      _openClassCreatorModal(slug, currentUser);
    });
  };

  function _openClassCreatorModal(slug, currentUser) {
    var existing = document.getElementById('classCreatorModal');
    if (existing) existing.remove();

    var defaultRoom = 'MATH-' + Math.random().toString(36).substring(2, 6).toUpperCase();

    var origin = window.location.origin;
    var pathname = window.location.pathname;
    var basePath = pathname.substring(0, pathname.lastIndexOf('/'));
    if (basePath.endsWith('/board')) {
      basePath = basePath.substring(0, basePath.lastIndexOf('/board'));
    }

    var modal = document.createElement('div');
    modal.id = 'classCreatorModal';
    modal.style.cssText = 'position:fixed;inset:0;z-index:99999;background:rgba(10,13,26,.85);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);display:flex;align-items:center;justify-content:center;padding:16px;animation:fadeIn .2s ease';

    var teacherLabel = (currentUser && currentUser.name) 
      ? (currentUser.name + ' (' + (currentUser.roleLabel || (isEnMode() ? 'Member' : '회원')) + ')') 
      : (isEnMode() ? 'Verified Teacher Member' : '인증된 교사 회원');

    modal.innerHTML = 
      '<div style="background:#ffffff;border:1px solid #e4e2e4;border-radius:20px;max-width:540px;width:100%;padding:28px;box-shadow:0 20px 60px rgba(19,27,46,.18);color:#1b1b1d;font-family:Inter,Pretendard,system-ui,sans-serif;position:relative">' +
        '<button onclick="document.getElementById(\'classCreatorModal\').remove()" style="position:absolute;top:16px;right:18px;background:#f0edef;border:none;color:#45464d;width:32px;height:32px;border-radius:50%;font-size:1.1rem;cursor:pointer">✕</button>' +
        '<div style="display:inline-flex;align-items:center;gap:6px;background:rgba(16,185,129,.12);color:#059669;border-radius:20px;padding:4px 12px;font-size:.78rem;font-weight:700;margin-bottom:10px">✅ ' + escapeHtml(teacherLabel) + '</div>' +
        '<h2 style="margin:0 0 6px;font-size:1.4rem;color:#1b1b1d;font-weight:800">' +
          bilingual('🚀 3초 만에 수업 개설하기', '🚀 Launch Classroom in 3 Seconds') +
        '</h2>' +
        '<p style="margin:0 0 20px;color:#45464d;font-size:.88rem">' +
          bilingual('선택하신 문제(<b>' + escapeHtml(slug) + '</b>)로 학생들에게 배포할 수업 코드가 생성되었습니다.', 'Class session code generated for problem <b>' + escapeHtml(slug) + '</b>.') +
        '</p>' +

        '<div style="background:#f6f3f5;border:1px solid #e4e2e4;border-radius:14px;padding:16px;margin-bottom:18px">' +
          '<label style="display:block;font-size:.8rem;color:#006398;font-weight:700;margin-bottom:6px">' +
            bilingual('수업 코드 / 방 이름 (원하는 이름으로 수정 가능)', 'Class Code / Room Name (Customizable)') +
          '</label>' +
          '<div style="display:flex;gap:8px">' +
            '<input type="text" id="customRoomInput" value="' + defaultRoom + '" style="flex:1;background:#ffffff;border:1px solid #c5c6cd;border-radius:10px;padding:10px 14px;color:#1b1b1d;font-size:1.05rem;font-weight:700;text-transform:uppercase">' +
            '<button id="btnRegenRoom" style="background:#f0edef;border:1px solid #e4e2e4;color:#1b1b1d;border-radius:10px;padding:0 14px;cursor:pointer;font-size:.85rem;font-weight:600">' +
              bilingual('🔄 재발급', '🔄 Regenerate') +
            '</button>' +
          '</div>' +
        '</div>' +

        '<div style="display:grid;grid-template-columns:130px 1fr;gap:16px;align-items:center;background:#f6f3f5;border:1px solid #e4e2e4;border-radius:14px;padding:16px;margin-bottom:20px">' +
          '<div style="text-align:center">' +
            '<img id="modalQrImg" src="" style="width:120px;height:120px;border-radius:10px;background:#fff;padding:6px;border:1px solid #e4e2e4;box-sizing:border-box" alt="QR Code">' +
            '<div style="font-size:.7rem;color:#45464d;margin-top:4px">' +
              bilingual('학생 스마트폰 스캔용', 'Scan with smartphone camera') +
            '</div>' +
          '</div>' +
          '<div>' +
            '<div style="font-size:.8rem;color:#45464d;margin-bottom:4px">' +
              bilingual('학생 접속 링크', 'Student Join Link') +
            '</div>' +
            '<div id="modalStudentUrlText" style="font-size:.82rem;color:#006398;word-break:break-all;background:#ffffff;padding:8px;border-radius:8px;border:1px solid #e4e2e4;margin-bottom:8px;font-weight:600"></div>' +
            '<div style="display:flex;gap:6px;flex-wrap:wrap">' +
              '<button id="btnCopyStudentUrl" style="background:#006398;color:#ffffff;border:none;border-radius:8px;padding:8px 12px;font-size:.8rem;font-weight:700;cursor:pointer">' +
                bilingual('📋 학생 링크 복사', '📋 Copy Student Link') +
              '</button>' +
              '<button id="btnProjectorMode" style="background:#f0edef;color:#1b1b1d;border:1px solid #e4e2e4;border-radius:8px;padding:8px 12px;font-size:.8rem;font-weight:700;cursor:pointer">' +
                bilingual('🖥️ 칠판 빔프로젝터 QR', '🖥️ Projector Screen QR') +
              '</button>' +
            '</div>' +
          '</div>' +
        '</div>' +

        '<div style="display:flex;gap:10px;justify-content:flex-end">' +
          '<button onclick="document.getElementById(\'classCreatorModal\').remove()" style="background:#f0edef;color:#45464d;border:1px solid #e4e2e4;border-radius:10px;padding:10px 18px;font-size:.9rem;font-weight:600;cursor:pointer">' +
            bilingual('닫기', 'Close') +
          '</button>' +
          '<button id="btnGoDashboard" style="background:#000000;color:#ffffff;border:none;border-radius:10px;padding:10px 22px;font-size:.95rem;font-weight:800;cursor:pointer">' +
            bilingual('📊 실시간 모니터링 열기 ➔', '📊 Open Live Dashboard ➔') +
          '</button>' +
        '</div>' +
      '</div>';

    document.body.appendChild(modal);

    function updateUrls() {
      var r = (document.getElementById('customRoomInput').value || '').trim() || defaultRoom;
      var studentUrl = origin + basePath + '/board/' + slug + '.html?room=' + encodeURIComponent(r);
      var dashboardUrl = origin + basePath + '/dashboard.html?room=' + encodeURIComponent(r);
      var qrApiUrl = 'https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=' + encodeURIComponent(studentUrl);

      document.getElementById('modalStudentUrlText').textContent = studentUrl;
      document.getElementById('modalQrImg').src = qrApiUrl;

      saveTeacherRoom(r, slug);

      document.getElementById('btnCopyStudentUrl').onclick = function() {
        navigator.clipboard.writeText(studentUrl).then(function() {
          var b = document.getElementById('btnCopyStudentUrl');
          var prev = b.innerHTML;
          b.innerHTML = bilingual('✅ 복사 완료!', '✅ Copied!');
          setTimeout(function() { b.innerHTML = prev; }, 1500);
        });
      };

      document.getElementById('btnGoDashboard').onclick = function() {
        window.open(dashboardUrl, '_blank');
      };

      document.getElementById('btnProjectorMode').onclick = function() {
        openProjectorScreen(studentUrl, r);
      };
    }

    document.getElementById('customRoomInput').oninput = updateUrls;
    document.getElementById('btnRegenRoom').onclick = function() {
      document.getElementById('customRoomInput').value = 'MATH-' + Math.random().toString(36).substring(2, 6).toUpperCase();
      updateUrls();
    };

    updateUrls();
  }

  function openProjectorScreen(url, rId) {
    var pModal = document.createElement('div');
    pModal.id = 'projectorScreenModal';
    pModal.style.cssText = 'position:fixed;inset:0;z-index:999999;background:#0a0d1a;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:24px;text-align:center;color:#fff;font-family:system-ui,sans-serif';
    
    var qrBig = 'https://api.qrserver.com/v1/create-qr-code/?size=450x450&data=' + encodeURIComponent(url);

    pModal.innerHTML = 
      '<button onclick="document.getElementById(\'projectorScreenModal\').remove()" style="position:absolute;top:20px;right:24px;background:#222a3d;color:#fff;border:1px solid #2e3850;padding:8px 16px;border-radius:10px;font-size:1rem;cursor:pointer">' +
        bilingual('✕ 전체화면 닫기', '✕ Close Fullscreen') +
      '</button>' +
      '<div style="display:inline-block;background:rgba(124,196,255,.2);color:#7cc4ff;border:1px solid rgba(124,196,255,.4);border-radius:30px;padding:6px 20px;font-size:1.1rem;font-weight:700;margin-bottom:14px">' +
        bilingual('🏫 수업 코드: ' + escapeHtml(rId), '🏫 Class Code: ' + escapeHtml(rId)) +
      '</div>' +
      '<h1 style="font-size:2.4rem;margin:0 0 10px;background:linear-gradient(90deg,#7cc4ff,#a78bfa);-webkit-background-clip:text;background-clip:text;color:transparent">' +
        bilingual('스마트폰 카메라로 QR 코드를 스캔하세요!', 'Scan QR Code with Smartphone Camera!') +
      '</h1>' +
      '<p style="color:#9aa6c0;font-size:1.15rem;margin:0 0 24px">' +
        bilingual('별도의 앱 설치나 회원가입 없이 즉시 문제가 열립니다.', 'Starts immediately without signup or app installation.') +
      '</p>' +
      '<div style="background:#fff;padding:16px;border-radius:24px;box-shadow:0 0 60px rgba(124,196,255,.4);margin-bottom:20px">' +
        '<img src="' + qrBig + '" style="width:340px;height:340px;display:block" alt="Large QR">' +
      '</div>' +
      '<div style="background:rgba(255,255,255,.08);padding:10px 24px;border-radius:12px;font-size:1.1rem;color:#7cc4ff;font-family:monospace">' + escapeHtml(url) + '</div>';

    document.body.appendChild(pModal);
  }

  function saveTeacherRoom(rId, slug) {
    try {
      var key = 'mathedu_teacher_rooms';
      var rooms = JSON.parse(localStorage.getItem(key) || '[]');
      rooms = rooms.filter(function(item) { return item.room !== rId; });
      rooms.unshift({ room: rId, slug: slug, time: new Date().toISOString() });
      if (rooms.length > 20) rooms = rooms.slice(0, 20);
      localStorage.setItem(key, JSON.stringify(rooms));

      if (window.MatheduAuth && window.MatheduAuth.recordCreatedRoom) {
        window.MatheduAuth.recordCreatedRoom(rId, slug);
      }
    } catch(e) {}
  }

  function escapeHtml(s) {
    return String(s || '').replace(/[&<>"']/g, function(c) {
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
    });
  }

  // === 오프라인 단독 실행 HTML 다운로드 모듈 ===
  function triggerBlobDownload(blob, filename) {
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    setTimeout(function() {
      if (a.parentNode) a.parentNode.removeChild(a);
      URL.revokeObjectURL(url);
    }, 400);
  }

  window.downloadOfflineQuiz = async function(targetSlug) {
    var slug = (targetSlug || currentSlug || '').replace(/\.html$/, '');
    if (!slug) return;

    var btn = (window.event && window.event.target) ? window.event.target.closest('button, a') : null;
    var origText = btn ? btn.innerHTML : '';
    if (btn) {
      btn.innerHTML = bilingual('⏳ 오프라인 다운로드 중...', '⏳ Downloading offline...');
      btn.style.pointerEvents = 'none';
    }

    try {
      // 1. 사전 빌드된 offline/{slug}.html 가져오기 시도
      var isBoard = window.location.pathname.indexOf('/board/') !== -1;
      var candidateUrls = [
        isBoard ? ('../offline/' + slug + '.html') : ('offline/' + slug + '.html'),
        'https://min7014.github.io/mathedu/offline/' + slug + '.html'
      ];

      var fetchedBlob = null;
      for (var i = 0; i < candidateUrls.length; i++) {
        try {
          var resp = await fetch(candidateUrls[i]);
          if (resp.ok) {
            fetchedBlob = await resp.blob();
            break;
          }
        } catch (fetchErr) {}
      }

      if (fetchedBlob && fetchedBlob.size > 1000) {
        triggerBlobDownload(fetchedBlob, 'mathedu_' + slug + '_offline.html');
        if (btn) {
          btn.innerHTML = bilingual('✅ 다운로드 완료!', '✅ Downloaded!');
          setTimeout(function() { btn.innerHTML = origText; btn.style.pointerEvents = ''; }, 2500);
        }
        return;
      }
    } catch (e) {
      console.warn('Prebuilt offline quiz fetch fallback:', e);
    }

    // 2. Fallback: 현재 DOM 기반 실시간 오프라인 패키징 (Base64 인라인 + 배너 삽입)
    try {
      var docClone = document.documentElement.cloneNode(true);

      // 시작 모달 제거 (오프라인에서 바로 풀 수 있게)
      var tf = docClone.querySelector('#trackFull');
      if (tf) tf.remove();

      // 플로팅 개설 버튼 제거
      var floatBtn = docClone.querySelector('#floatClassBtn');
      if (floatBtn) floatBtn.remove();

      var originalOnlineUrl = 'https://min7014.github.io/mathedu/board/' + slug + '.html';
      var h1El = docClone.querySelector('h1');
      var quizTitle = h1El ? h1El.textContent.replace(/^[📘📙📕📝]\s*/, '').trim() : slug;

      // 이미지 base64 변환
      var imgs = docClone.querySelectorAll('img');
      for (var j = 0; j < imgs.length; j++) {
        var img = imgs[j];
        if (img.src && !img.src.startsWith('data:')) {
          try {
            var canvas = document.createElement('canvas');
            canvas.width = img.naturalWidth || img.width || 400;
            canvas.height = img.naturalHeight || img.height || 300;
            var ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0);
            var dataUrl = canvas.toDataURL('image/png');
            if (dataUrl && dataUrl.length > 50) {
              img.src = dataUrl;
            }
          } catch(cvsErr) {}
        }
      }

      // 오프라인 배너 및 원본 주소 안내 삽입
      var bannerExisting = docClone.querySelector('.mathedu-offline-banner');
      if (!bannerExisting) {
        var bannerDiv = document.createElement('div');
        bannerDiv.className = 'mathedu-offline-banner';
        bannerDiv.style.cssText = 'background:linear-gradient(135deg,rgba(56,189,248,.18),rgba(129,140,248,.18));border:2px solid #38bdf8;border-radius:16px;padding:18px 22px;margin:16px 0 24px;box-shadow:0 8px 30px rgba(0,0,0,.45);color:#fff;font-family:system-ui,sans-serif';
        bannerDiv.innerHTML = 
          '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:10px">' +
            '<div style="display:inline-flex;align-items:center;gap:6px;background:rgba(56,189,248,.25);border:1px solid #38bdf8;color:#38bdf8;border-radius:20px;padding:4px 14px;font-size:0.82rem;font-weight:800">' +
              bilingual('📦 오프라인 단독 실행 파일 (인터넷 접속 없이 풀이 가능)', '📦 Offline Standalone Quiz (Runs without internet)') +
            '</div>' +
            '<div style="display:flex;align-items:center;gap:8px">' +
              '<button id="btnManualCheckUpdate" onclick="checkUpdateManual()" style="background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);color:#cbd5e1;padding:3px 12px;border-radius:14px;font-size:0.75rem;cursor:pointer;font-family:inherit">' +
                bilingual('🔄 최신 버전 확인', '🔄 Check Updates') +
              '</button>' +
              '<span style="font-size:0.78rem;color:#94a3b8">min7014 mathedu</span>' +
            '</div>' +
          '</div>' +
          '<div style="font-size:1.15rem;font-weight:800;color:#ffffff;margin-bottom:6px">' + escapeHtml(quizTitle) + '</div>' +
          '<div style="font-size:0.86rem;color:#cbd5e1;line-height:1.5;margin-bottom:12px">' +
            bilingual(
              '이 파일은 인터넷 연결 없이 웹 브라우저에서 언제든 풀 수 있는 <b>단독 오프라인 인터랙티브 수학 퀴즈</b>입니다.<br>보기를 클릭하면 채점과 단계별 상세 해설이 열리며, 점수가 자동 계산됩니다.',
              'This file is a <b>standalone offline interactive math quiz</b> that runs anytime in your browser without internet.<br>Clicking options grades your answer and reveals detailed visual explanations.'
            ) +
          '</div>' +
          '<div id="matheduUpdateAlertSlot" style="display:none;margin-bottom:12px;padding:12px 16px;background:rgba(253,230,138,.14);border:1.5px solid #fde68a;border-radius:12px;color:#fde68a;font-size:0.88rem;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px">' +
            '<div style="display:flex;align-items:center;gap:8px">' +
              '<span style="font-size:1.1rem">🔔</span>' +
              '<span>' +
                bilingual('<b>이 문제의 최신 업데이트 버전이 있습니다!</b> (새 버전으로 저장 후 풀이 가능)', '<b>A newer update of this problem is available!</b> (Download to practice)') +
              '</span>' +
            '</div>' +
            '<button onclick="openUpdateModal()" style="background:#fde68a;color:#0b1020;border:none;padding:6px 14px;border-radius:8px;font-weight:800;font-size:0.82rem;cursor:pointer">' +
              bilingual('업데이트 보기 ➔', 'View Update ➔') +
            '</button>' +
          '</div>' +
          '<div style="background:rgba(15,23,42,.7);border:1px solid rgba(255,255,255,.14);border-radius:12px;padding:12px 16px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px">' +
            '<div style="font-size:0.85rem;color:#e2e8f0;word-break:break-all">' +
              '<span style="color:#7cc4ff;font-weight:700">' + bilingual('🌐 온라인 원본 문제 주소:', '🌐 Online Original URL:') + '</span><br>' +
              '<a href="' + originalOnlineUrl + '" target="_blank" rel="noopener" style="color:#38bdf8;font-weight:700;text-decoration:underline;font-family:monospace">' + originalOnlineUrl + '</a>' +
            '</div>' +
            '<div style="display:flex;gap:8px">' +
              '<a href="' + originalOnlineUrl + '" target="_blank" rel="noopener" style="background:linear-gradient(90deg,#38bdf8,#818cf8);color:#0b1020;padding:8px 16px;border-radius:8px;font-size:0.82rem;font-weight:800;text-decoration:none">' +
                bilingual('🌐 온라인 원본 열기 ➔', '🌐 Open Online Original ➔') +
              '</a>' +
              '<a href="https://min7014.github.io/" target="_blank" rel="noopener" style="background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);color:#eef2ff;padding:8px 14px;border-radius:8px;font-size:0.82rem;font-weight:700;text-decoration:none">' +
                bilingual('🏛️ min7014 자료실', '🏛️ min7014 Library') +
              '</a>' +
            '</div>' +
          '</div>';

        var wrapEl = docClone.querySelector('.wrap') || docClone.querySelector('body');
        if (wrapEl) wrapEl.insertBefore(bannerDiv, wrapEl.firstChild);
      }

      var nowIso = new Date().toISOString();
      var updaterHtml = 
        '<div id="matheduUpdateModal" class="mathedu-update-modal" style="display:none">' +
          '<div class="mathedu-update-card">' +
            '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">' +
              '<div class="mathedu-update-badge">' + bilingual('🔔 최신 업데이트 감지', '🔔 Update Detected') + '</div>' +
              '<button class="mathedu-update-close-btn" onclick="closeUpdateModal()">✕</button>' +
            '</div>' +
            '<h2 style="margin:0 0 8px;font-size:1.35rem;background:linear-gradient(90deg,#7cc4ff,#a78bfa);-webkit-background-clip:text;background-clip:text;color:transparent;font-weight:800">' +
              bilingual('✨ 이 문제의 최신 버전이 있습니다!', '✨ A newer version of this problem is available!') +
            '</h2>' +
            '<p style="margin:0 0 16px;color:#cbd5e1;font-size:0.9rem;line-height:1.55">' +
              bilingual(
                '선생님께서 문제의 해설 보강, 질문 개선, 또는 새로운 인터랙티브 디딤돌 단계를 업데이트하셨습니다.<br>새로운 버전을 다운로드하여 저장 후 풀이하시거나, 지금 바로 현재 버전으로 계속 푸실 수 있습니다.',
                'The teacher has updated explanations, improved scaffolding prompts, or added interactive stepping stones.<br>Download the new version to practice, or continue with your current version.'
              ) +
            '</p>' +
            '<div class="mathedu-ver-box">' +
              '<div class="mathedu-ver-item cur"><span class="mathedu-ver-lbl">' + bilingual('현재 내 오프라인 버전', 'Current Offline Version') + '</span><b id="lblCurrentVer">-</b></div>' +
              '<div style="color:#7cc4ff;font-size:1.2rem;font-weight:800">➔</div>' +
              '<div class="mathedu-ver-item new"><span class="mathedu-ver-lbl">' + bilingual('🚀 온라인 최신 버전', '🚀 Latest Online Version') + '</span><b id="lblLatestVer">-</b></div>' +
            '</div>' +
            '<div class="mathedu-update-btn-row">' +
              '<button id="btnDownloadUpdate" class="mathedu-btn-primary" onclick="downloadLatestOfflineVersion()">' +
                bilingual('📥 새 버전 내려받아서 풀기 (저장)', '📥 Download New Version & Practice') +
              '</button>' +
              '<button class="mathedu-btn-sec" onclick="continueCurrentVersion()">' +
                bilingual('📝 그냥 현재 버전으로 풀기', '📝 Continue with Current Version') +
              '</button>' +
              '<a id="btnOpenOnlineLatest" href="' + originalOnlineUrl + '" target="_blank" rel="noopener" class="mathedu-btn-link">' +
                bilingual('🌐 온라인 최신판 웹으로 바로 열기 ➔', '🌐 Open Latest Web Version ➔') +
              '</a>' +
            '</div>' +
            '<div id="updateDownloadSuccess" style="display:none;margin-top:16px;background:rgba(94,234,212,.15);border:1px solid #5eead4;border-radius:12px;padding:14px;text-align:left">' +
              '<div style="font-weight:800;color:#5eead4;margin-bottom:4px">' +
                bilingual('🎉 최신 버전 다운로드 완료!', '🎉 Latest Version Downloaded!') +
              '</div>' +
              '<div style="font-size:0.86rem;color:#e2e8f0;line-height:1.5">' +
                bilingual(
                  '다운로드 폴더에 최신 문제 파일이 저장되었습니다. 새로 저장된 파일을 브라우저로 열어 풀이하시거나, 온라인 최신 페이지로 바로 이동하실 수 있습니다.',
                  'The latest problem file has been saved to your Downloads folder. Open the newly saved file in your browser or jump directly to the online page.'
                ) +
              '</div>' +
              '<div style="margin-top:12px;display:flex;gap:8px">' +
                '<a href="' + originalOnlineUrl + '" target="_blank" rel="noopener" style="background:#5eead4;color:#0b1020;padding:7px 16px;border-radius:8px;font-size:0.84rem;font-weight:800;text-decoration:none">' +
                  bilingual('🌐 온라인 최신판 열기', '🌐 Open Online Latest') +
                '</a>' +
                '<button onclick="closeUpdateModal()" style="background:transparent;border:1px solid #5eead4;color:#5eead4;padding:7px 16px;border-radius:8px;font-size:0.84rem;cursor:pointer;font-weight:700">' +
                  bilingual('✕ 닫고 현재 화면 풀기', '✕ Close & Continue') +
                '</button>' +
              '</div>' +
            '</div>' +
          '</div>' +
        '</div>' +
        '<style>' +
          '.mathedu-update-modal{position:fixed;inset:0;z-index:999999;background:rgba(10,13,26,.85);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);display:flex;align-items:center;justify-content:center;padding:16px}' +
          '.mathedu-update-card{background:#141833;border:1.5px solid rgba(124,196,255,.4);border-radius:20px;max-width:520px;width:100%;padding:26px;box-shadow:0 20px 60px rgba(0,0,0,.65);color:#eef2ff;font-family:system-ui,sans-serif;position:relative;line-height:1.6}' +
          '.mathedu-update-badge{display:inline-flex;align-items:center;gap:6px;background:rgba(253,230,138,.15);border:1px solid #fde68a;color:#fde68a;border-radius:20px;padding:4px 12px;font-size:.8rem;font-weight:800}' +
          '.mathedu-update-close-btn{background:transparent;border:none;color:#94a3b8;font-size:1.4rem;cursor:pointer;padding:0 4px}' +
          '.mathedu-ver-box{display:grid;grid-template-columns:1fr auto 1fr;gap:10px;align-items:center;background:rgba(13,16,32,.7);border:1px solid rgba(255,255,255,.12);border-radius:12px;padding:12px 14px;margin:16px 0;text-align:center}' +
          '.mathedu-ver-item{font-size:.8rem;color:#94a3b8}.mathedu-ver-item b{display:block;font-size:.95rem;margin-top:2px}' +
          '.mathedu-ver-item.cur b{color:#cbd5e1}.mathedu-ver-item.new b{color:#5eead4}' +
          '.mathedu-update-btn-row{display:flex;flex-direction:column;gap:8px;margin-top:18px}' +
          '.mathedu-btn-primary{background:linear-gradient(90deg,#38bdf8,#818cf8);color:#0b1020;border:none;border-radius:10px;padding:12px 18px;font-size:.96rem;font-weight:800;cursor:pointer;text-align:center}' +
          '.mathedu-btn-sec{background:rgba(255,255,255,.1);color:#eef2ff;border:1px solid rgba(255,255,255,.2);border-radius:10px;padding:11px 18px;font-size:.92rem;font-weight:700;cursor:pointer;text-align:center}' +
          '.mathedu-btn-link{background:transparent;color:#7cc4ff;border:none;padding:6px;font-size:.85rem;cursor:pointer;text-decoration:underline;text-align:center}' +
        '</style>' +
        '<script>' +
          'window._isOfflineFile=true;' +
          'window._offlineQuizSlug="' + slug + '";' +
          'window._offlineBuildTime="' + nowIso + '";' +
          'window._originalUrl="' + originalOnlineUrl + '";' +
          '(function(){' +
            'var s="' + slug + '",bt="' + nowIso + '",ou="' + originalOnlineUrl + '";' +
            'var du="https://min7014.github.io/mathedu/offline/"+s+".html";' +
            'var vu="https://min7014.github.io/mathedu/offline/versions.json";' +
            'window._serverUpdateInfo=null;' +
            'function fmt(t){if(!t)return "-";try{var d=new Date(t);return d.getFullYear()+"."+(d.getMonth()+1)+"."+d.getDate()+" "+(d.getHours()<10?"0":"")+d.getHours()+":"+(d.getMinutes()<10?"0":"")+d.getMinutes();}catch(e){return t;}}' +
            'window.openUpdateModal=function(){var m=document.getElementById("matheduUpdateModal");if(!m)return;var c=document.getElementById("lblCurrentVer"),n=document.getElementById("lblLatestVer");if(c)c.textContent=fmt(bt);if(n)n.textContent=fmt(window._serverUpdateInfo?window._serverUpdateInfo.updated_at:new Date().toISOString());m.style.display="flex";};' +
            'window.closeUpdateModal=function(){var m=document.getElementById("matheduUpdateModal");if(m)m.style.display="none";};' +
            'window.continueCurrentVersion=function(){closeUpdateModal();try{sessionStorage.setItem("mathedu_update_dismissed_"+s,"true");}catch(e){}};' +
            'window.downloadLatestOfflineVersion=async function(){var b=document.getElementById("btnDownloadUpdate");if(b){b.innerHTML="' + (isEnMode() ? '⏳ Downloading latest version...' : '⏳ 최신 버전 다운로드 중...') + '";b.style.pointerEvents="none";}' +
            'try{var r=await fetch(du+"?_t="+Date.now());if(!r.ok)throw new Error("HTTP "+r.status);var bl=await r.blob();var u=URL.createObjectURL(bl);var a=document.createElement("a");a.href=u;a.download="mathedu_"+s+"_offline_latest.html";document.body.appendChild(a);a.click();setTimeout(function(){a.remove();URL.revokeObjectURL(u);},500);if(b)b.innerHTML="' + (isEnMode() ? '✅ New version saved!' : '✅ 새 버전 저장 완료!') + '";var bx=document.getElementById("updateDownloadSuccess");if(bx)bx.style.display="block";}' +
            'catch(e){alert("' + (isEnMode() ? 'Download failed: ' : '다운로드 실패: ') + '"+e.message);window.open(ou,"_blank");if(b){b.innerHTML="' + (isEnMode() ? '📥 Retry' : '📥 다시 시도') + '";b.style.pointerEvents="";}}};' +
            'window.checkUpdateManual=function(){var b=document.getElementById("btnManualCheckUpdate");if(b)b.innerHTML="' + (isEnMode() ? '⏳ Checking...' : '⏳ 확인 중...') + '";chk(true);};' +
            'function showUp(inf){window._serverUpdateInfo=inf;var sl=document.getElementById("matheduUpdateAlertSlot");if(sl)sl.style.display="flex";var bm=document.getElementById("btnManualCheckUpdate");if(bm){bm.innerHTML="' + (isEnMode() ? '✨ New version available!' : '✨ 새 버전 있음!') + '";bm.style.background="rgba(253,230,138,.25)";bm.style.color="#fde68a";bm.style.borderColor="#fde68a";}' +
            'var dis=false;try{dis=sessionStorage.getItem("mathedu_update_dismissed_"+s)==="true";}catch(e){}if(!dis)openUpdateModal();}' +
            'function chk(man){if(!navigator.onLine){if(man)alert("' + (isEnMode() ? 'Currently offline.' : '현재 오프라인 상태입니다.') + '");var b=document.getElementById("btnManualCheckUpdate");if(b)b.innerHTML="' + (isEnMode() ? '📡 Offline' : '📡 오프라인') + '";return;}' +
            'fetch(vu+"?_t="+Date.now(),{cache:"no-cache"}).then(function(r){if(!r.ok)throw new Error();return r.json();}).then(function(d){' +
            'var it=d&&d.quizzes&&d.quizzes[s];if(it&&it.updated_at&&(new Date(it.updated_at).getTime()-new Date(bt).getTime()>60000)){showUp(it);}else{hUp(man);}}).catch(function(){' +
            'fetch(du+"?_t="+Date.now(),{method:"HEAD",cache:"no-cache"}).then(function(r){var lm=r.headers.get("Last-Modified");if(lm&&(new Date(lm).getTime()-new Date(bt).getTime()>120000)){showUp({updated_at:new Date(lm).toISOString()});}else{hUp(man);}}).catch(function(){hUp(man);});});}' +
            'function hUp(man){var b=document.getElementById("btnManualCheckUpdate");if(b){b.innerHTML="' + (isEnMode() ? '✅ Latest' : '✅ 최신 버전') + '";b.style.color="#5eead4";b.style.borderColor="rgba(94,234,212,.4)";}if(man)alert("' + (isEnMode() ? 'You are using the latest version.' : '현재 문제 파일이 최신 버전입니다.') + '");}' +
            'setTimeout(function(){chk(false);},1000);' +
            'window.addEventListener("online",function(){chk(false);});' +
          '})();' +
        '</script>';

      var dummy = document.createElement('div');
      dummy.innerHTML = updaterHtml;
      while (dummy.firstChild) {
        docClone.body.appendChild(dummy.firstChild);
      }

      var fullHtml = '<!DOCTYPE html>\n<html lang="' + (isEnMode() ? 'en' : 'ko') + '">\n' + docClone.innerHTML + '\n</html>';
      var blob = new Blob([fullHtml], { type: 'text/html;charset=utf-8' });
      triggerBlobDownload(blob, 'mathedu_' + slug + '_offline.html');

      if (btn) {
        btn.innerHTML = bilingual('✅ 다운로드 완료!', '✅ Downloaded!');
        setTimeout(function() { btn.innerHTML = origText; btn.style.pointerEvents = ''; }, 2500);
      }
    } catch(err) {
      alert((isEnMode() ? 'Error generating offline download file: ' : '오프라인 파일 다운로드 생성 중 오류: ') + err.message);
      if (btn) {
        btn.innerHTML = origText;
        btn.style.pointerEvents = '';
      }
    }
  };

  // ════════════════════════════════════════════════════════════════════════
  // 🚀 4대 무비용 바이럴 성장 엔진 (Zero-Cost Organic Viral Loop Suite)
  // 1. 지적 성취감 과시 (Intellectual Flex & Result Card)
  // 2. 친구 승부욕 자극 (도전장 챌린지 - Duel Mode: ?challenger=...)
  // 3. 커뮤니티 전파용 워들 스타일 이모지 텍스트 복사 (Wordle-Style Text Copy)
  // 4. 수포자 친구 살리기 이타적 추천 (Altruistic Scaffolding Gift)
  // ════════════════════════════════════════════════════════════════════════

  function showViralToast(msg) {
    var t = document.getElementById('mathedu-viral-toast');
    if (!t) {
      t = document.createElement('div');
      t.id = 'mathedu-viral-toast';
      t.style.cssText = 'position:fixed;bottom:28px;left:50%;transform:translateX(-50%) translateY(20px);background:rgba(15,23,42,.96);color:#fff;border:1.5px solid rgba(56,189,248,.65);border-radius:14px;padding:12px 22px;font-size:0.92rem;font-weight:700;z-index:99999999;box-shadow:0 12px 35px rgba(0,0,0,.65);transition:opacity .25s ease,transform .25s ease;opacity:0;pointer-events:none;display:flex;align-items:center;gap:10px;backdrop-filter:blur(12px);max-width:90vw;text-align:center;word-break:keep-all;font-family:system-ui,sans-serif;';
      document.body.appendChild(t);
    }
    t.innerHTML = msg;
    t.style.opacity = '1';
    t.style.transform = 'translateX(-50%) translateY(0)';
    clearTimeout(t._timer);
    t._timer = setTimeout(function() {
      t.style.opacity = '0';
      t.style.transform = 'translateX(-50%) translateY(20px)';
    }, 3200);
  }

  function getProblemTitle() {
    var h1 = document.querySelector('h1');
    if (h1) {
      var clone = h1.cloneNode(true);
      var hidden = clone.querySelectorAll('.bilingual-en, [style*="display: none"], [style*="display:none"]');
      if (isEnMode()) {
        hidden = clone.querySelectorAll('.bilingual-ko');
      }
      hidden.forEach(function(el) { el.remove(); });
      var t = clone.innerText.trim();
      if (t) return t.replace(/^📐\s*/, '').replace(/^📘\s*/, '');
    }
    return document.title.replace(/\|.*$/, '').trim() || (isEnMode() ? 'Math Problem' : '수학 문제');
  }

  function getBaseShareUrl() {
    return window.location.origin + window.location.pathname;
  }

  function getChallengeUrl(name) {
    var n = (name || window._studentName || (isEnMode() ? 'Friend' : '익명 도전자')).trim();
    return getBaseShareUrl() + '?challenger=' + encodeURIComponent(n);
  }

  function getQuizStats() {
    var qs = document.querySelectorAll('.q');
    var total = qs.length || 6;
    var done = document.querySelectorAll('.q.done');
    var correct = 0;
    done.forEach(function(q) {
      if (q.querySelector('.opt.correct')) correct++;
    });
    if (correct === 0 && done.length > 0) correct = done.length;
    if (correct === 0) correct = total;
    return { total: total, correct: correct, done: done.length || total };
  }

  function buildGreenBlocks(total, correct) {
    var blocks = '';
    for (var i = 0; i < total; i++) {
      blocks += (i < correct) ? '🟩' : '🟨';
    }
    return blocks;
  }

  function nativeShareOrCopy(shareData, fallbackMsg) {
    if (navigator.share) {
      navigator.share(shareData).catch(function(err) {
        if (err && err.name !== 'AbortError') {
          copyToClipboard(shareData.text + '\n' + shareData.url, fallbackMsg);
        }
      });
    } else {
      copyToClipboard(shareData.text + '\n' + shareData.url, fallbackMsg);
    }
  }

  function copyToClipboard(text, successMsg) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function() {
        showViralToast(successMsg || (isEnMode() ? '✅ Copied to clipboard!' : '✅ 클립보드에 복사되었습니다!'));
      }).catch(function() {
        legacyCopy(text, successMsg);
      });
    } else {
      legacyCopy(text, successMsg);
    }
  }

  function legacyCopy(text, successMsg) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try {
      document.execCommand('copy');
      showViralToast(successMsg || (isEnMode() ? '✅ Copied to clipboard!' : '✅ 클립보드에 복사되었습니다!'));
    } catch (e) {
      showViralToast(isEnMode() ? '⚠️ Please copy manually.' : '⚠️ 수동으로 복사해주세요.');
    }
    ta.remove();
  }

  // 1. 친구에게 3초 도전장 보내기 (호승심/승부욕 자극)
  window.shareAsChallenge = function() {
    var stats = getQuizStats();
    var name = (window._studentName || (isEnMode() ? 'A friend' : '친구')).trim();
    var title = getProblemTitle();
    var url = getChallengeUrl(name);
    
    var shareText = isEnMode()
      ? '⚔️ [' + name + '] sent you a Math Quest Challenge!\n"I cleared ' + title + ' (' + stats.total + ' steps) with zero errors. Can you beat me?"'
      : '⚔️ [' + name + '] 님이 보낸 수능 킬러 도전장!\n"나 ' + title + ' ' + stats.total + '단계 오답 없이 완주했는데, 너도 나처럼 풀 수 있을까?"';
      
    var msg = isEnMode() 
      ? '⚔️ Challenge link copied! Send it to your friend to spark a duel!' 
      : '⚔️ 도전장 링크가 복사되었습니다! 친구나 단톡방에 공유해보세요!';
      
    nativeShareOrCopy({
      title: isEnMode() ? 'Math Quest Challenge' : '수능 킬러 수학 도전장',
      text: shareText,
      url: url
    }, msg);
  };

  // 2. 커뮤니티 자랑용 텍스트 복사 (워들 포맷)
  window.copyCommunityScoreText = function() {
    var stats = getQuizStats();
    var title = getProblemTitle();
    var blocks = buildGreenBlocks(stats.total, stats.correct);
    var rate = Math.round((stats.correct / stats.total) * 100);
    var url = getBaseShareUrl();
    
    var text = isEnMode()
      ? '📘 mathedu Math Quest Challenge!\n' +
        '📐 ' + title + '\n' +
        blocks + ' ' + stats.total + '/' + stats.total + ' Steps Cleared! (' + rate + '% Accuracy)\n\n' +
        'Mastered this high-level exam problem in 10 mins with micro-scaffolding! 🚀\n' +
        '👉 Try beating my score: ' + url
      : '📘 mathedu 수능 킬러 정복 챌린지!\n' +
        '📐 ' + title + '\n' +
        blocks + ' ' + stats.total + '/' + stats.total + ' 단계 올클리어! (정답률 ' + rate + '%)\n\n' +
        '초등학생 눈높이 사다리로 수능 킬러 10분 컷 완주 완료 🚀\n' +
        '👉 너도 풀 수 있는지 도전해봐: ' + url;

    copyToClipboard(text, isEnMode() ? '📋 Community share text copied! Paste it in Reddit, Discord, or group chats!' : '📋 커뮤니티(수만휘, 오르비, 에타, 단톡방)용 결과 텍스트가 복사되었습니다!');
  };

  // 3. 수포자 친구 살리기 디딤돌 풀이 선물하기 (이타적 추천 & Pay-It-Forward 루프)
  window.shareAsGift = function() {
    var title = getProblemTitle();
    var name = (window._studentName || (isEnMode() ? 'A friend' : '친구')).trim();
    var url = getBaseShareUrl() + '?gift_from=' + encodeURIComponent(name);
    
    var shareText = isEnMode()
      ? '💝 [' + name + '] sent you a helpful step-by-step Math Scaffolding Gift!\n' +
        '📐 ' + title + '\n' +
        'Starts from elementary fundamentals and leads all the way to the full proof.\n' +
        'Try it freely without signup: '
      : '💝 [' + name + '] 님이 보낸 디딤돌 수학 풀이 선물!\n' +
        '📐 ' + title + '\n' +
        '수능 킬러 문제인데 초등학교 사칙연산 수준부터 한 계단씩 풀리는 신기한 디딤돌이야. 가입 없이 바로 풀 수 있어 꼭 해봐:\n';
        
    var msg = isEnMode()
      ? '💝 Gift solution link copied! Send it to encourage your friends!'
      : '💝 친구 선물용 디딤돌 풀이 링크가 복사되었습니다! 카톡으로 전송해보세요!';
      
    nativeShareOrCopy({
      title: isEnMode() ? 'Helpful Math Gift' : '선물: 디딤돌 수학 풀이',
      text: shareText,
      url: url
    }, msg);
  };

  // 선물해준 친구에게 고마움 전하기
  window.sendThankYouToGiver = function(giverName) {
    var title = getProblemTitle();
    var text = isEnMode()
      ? '🎉 Thanks ' + giverName + '! I cleared ' + title + ' all the way to the end thanks to your scaffolding gift! 🚀'
      : '🎉 나 너가 보내준 디딤돌 풀이로 [' + title + '] 끝까지 다 풀었어! 진짜 초등학교 수준부터 쪼개져 있어서 다 이해되더라 고마워! 🚀';
    
    nativeShareOrCopy({
      title: isEnMode() ? 'Thank You!' : '고마워! 수능 킬러 완주 성공!',
      text: text,
      url: getBaseShareUrl()
    }, isEnMode() ? '💌 Thank-you message copied!' : '💌 고마움 메시지가 복사되었습니다! 친구에게 카톡으로 보내보세요!');
  };

  // 4. 완주 시 축하 & 바이럴 통합 모달 팝업
  window.showCompletionViralModal = function(total, correct) {
    if (document.getElementById('matheduViralModal')) return;

    var title = getProblemTitle();
    var studentName = (window._studentName || (isEnMode() ? 'Guest Learner' : '자유 학습자')).trim();
    var greenBlocks = buildGreenBlocks(total, correct);
    var rate = Math.round((correct / total) * 100);

    var giftFrom = (urlParams.get('gift_from') || urlParams.get('gift') || '').trim();
    var giftCongratHtml = giftFrom ? 
      '<div style="background:rgba(236,72,153,.15);border:1px solid rgba(236,72,153,.5);border-radius:12px;padding:10px 14px;margin-bottom:14px;font-size:0.86rem;color:#fbcfe8">' +
        bilingual('🎉 <b>' + escapeHtml(giftFrom) + '</b> 님의 디딤돌 선물을 딛고 수능 킬러 문제를 완주하셨습니다! 대단합니다!', '🎉 You cleared this problem thanks to <b>' + escapeHtml(giftFrom) + '</b>\'s scaffolding gift!') +
      '</div>' : '';

    var modal = document.createElement('div');
    modal.id = 'matheduViralModal';
    modal.style.cssText = 'position:fixed;inset:0;z-index:999999;background:rgba(10,13,26,.88);backdrop-filter:blur(16px);display:flex;align-items:center;justify-content:center;padding:16px;animation:matheduFadeIn .25s ease;font-family:system-ui,sans-serif';

    modal.innerHTML = 
      '<div style="background:linear-gradient(160deg,#141833 0%,#0e1222 100%);border:2px solid rgba(124,196,255,.45);border-radius:24px;max-width:500px;width:100%;max-height:90vh;overflow-y:auto;padding:26px;color:#fff;box-shadow:0 24px 60px rgba(0,0,0,.8);position:relative;text-align:center;box-sizing:border-box">' +
        '<button type="button" onclick="document.getElementById(\'matheduViralModal\').remove()" style="position:absolute;top:16px;right:16px;background:rgba(255,255,255,.1);border:none;color:#94a3b8;font-size:1.2rem;cursor:pointer;border-radius:50%;width:32px;height:32px;display:flex;align-items:center;justify-content:center;transition:.15s" onmouseover="this.style.color=\'#fff\'">✕</button>' +
        '<div style="font-size:2.6rem;margin-bottom:4px;animation:matheduPopUp .4s ease">🏆</div>' +
        '<div style="display:inline-block;background:linear-gradient(90deg,rgba(56,189,248,.2),rgba(94,234,212,.2));border:1px solid #5eead4;color:#5eead4;padding:4px 14px;border-radius:20px;font-size:0.8rem;font-weight:800;margin-bottom:8px">' +
          bilingual('수능 킬러 문항 정복 완료', 'PROBLEM MASTERED') +
        '</div>' +
        '<h2 style="font-size:1.28rem;margin:0 0 6px;background:linear-gradient(90deg,#7cc4ff,#a78bfa);-webkit-background-clip:text;background-clip:text;color:transparent;font-weight:800;line-height:1.4">' +
          escapeHtml(title) +
        '</h2>' +
        giftCongratHtml +
        '<p style="color:#cbd5e1;font-size:0.88rem;margin:0 0 16px">' +
          bilingual('👤 <b>' + escapeHtml(studentName) + '</b> 님, 축하합니다! 초등학생 디딤돌부터 끝까지 완주하셨습니다!', '👤 Congratulations <b>' + escapeHtml(studentName) + '</b>! You cleared all scaffolding steps!') +
        '</p>' +
        '<div style="background:rgba(15,20,38,.85);border:1px solid rgba(124,196,255,.3);border-radius:16px;padding:14px;margin-bottom:18px">' +
          '<div style="font-size:1.35rem;letter-spacing:4px;margin-bottom:8px">' + greenBlocks + '</div>' +
          '<div style="display:flex;justify-content:space-around;font-size:0.83rem;color:#94a3b8;border-top:1px dashed rgba(255,255,255,.12);padding-top:10px">' +
            '<div>' + bilingual('완주: ', 'Cleared: ') + '<b style="color:#5eead4">' + total + '/' + total + '</b></div>' +
            '<div>' + bilingual('정답: ', 'Score: ') + '<b style="color:#38bdf8">' + correct + ' (' + rate + '%)</b></div>' +
            '<div>' + bilingual('보너스: ', 'Bonus: ') + '<b style="color:#fde68a">+50 XP</b></div>' +
          '</div>' +
        '</div>' +
        '<div style="display:flex;flex-direction:column;gap:10px;text-align:left">' +
          (giftFrom ? 
            '<button type="button" onclick="window.sendThankYouToGiver(\'' + escapeHtml(giftFrom) + '\')" style="background:linear-gradient(90deg,#ec4899,#f43f5e);color:#fff;border:none;border-radius:14px;padding:13px 18px;font-size:0.94rem;font-weight:800;cursor:pointer;display:flex;align-items:center;justify-content:space-between;box-shadow:0 6px 20px rgba(236,72,153,.35);transition:transform .15s" onmouseover="this.style.transform=\'scale(1.02)\'" onmouseout="this.style.transform=\'none\'">' +
              '<div style="display:flex;align-items:center;gap:10px">' +
                '<span style="font-size:1.3rem">💌</span>' +
                '<div>' +
                  '<div>' + bilingual(escapeHtml(giftFrom) + ' 님에게 "나 다 풀었다!" 고마움 전하기', 'Thank ' + escapeHtml(giftFrom) + ' for the Scaffolding Gift') + '</div>' +
                  '<div style="font-size:0.75rem;color:rgba(255,255,255,.85);font-weight:400">' + bilingual('선물 덕분에 수능 킬러 완주 성공 인증', 'Share your success and joy') + '</div>' +
                '</div>' +
              '</div>' +
              '<span style="font-size:1.1rem">➔</span>' +
            '</button>' : '') +
          '<button type="button" onclick="window.shareAsChallenge()" style="background:linear-gradient(90deg,#f59e0b,#ef4444);color:#fff;border:none;border-radius:14px;padding:13px 18px;font-size:0.94rem;font-weight:800;cursor:pointer;display:flex;align-items:center;justify-content:space-between;box-shadow:0 6px 20px rgba(245,158,11,.3);transition:transform .15s" onmouseover="this.style.transform=\'scale(1.02)\'" onmouseout="this.style.transform=\'none\'">' +
            '<div style="display:flex;align-items:center;gap:10px">' +
              '<span style="font-size:1.3rem">⚔️</span>' +
              '<div>' +
                '<div>' + bilingual('친구에게 3초 도전장 보내기', 'Send 3-Sec Challenge to Friend') + '</div>' +
                '<div style="font-size:0.75rem;color:rgba(255,255,255,.85);font-weight:400">' + bilingual('"나 다 풀었는데 너도 풀 수 있어?" 호승심 자극', '"I solved it, can you beat me?"') + '</div>' +
              '</div>' +
            '</div>' +
            '<span style="font-size:1.1rem">➔</span>' +
          '</button>' +
          '<button type="button" onclick="window.copyCommunityScoreText()" style="background:linear-gradient(90deg,#3b82f6,#8b5cf6);color:#fff;border:none;border-radius:14px;padding:13px 18px;font-size:0.94rem;font-weight:800;cursor:pointer;display:flex;align-items:center;justify-content:space-between;box-shadow:0 6px 20px rgba(59,130,246,.3);transition:transform .15s" onmouseover="this.style.transform=\'scale(1.02)\'" onmouseout="this.style.transform=\'none\'">' +
            '<div style="display:flex;align-items:center;gap:10px">' +
              '<span style="font-size:1.3rem">📋</span>' +
              '<div>' +
                '<div>' + bilingual('커뮤니티 자랑용 텍스트 복사 (워들 포맷)', 'Copy Community Text (Wordle Format)') + '</div>' +
                '<div style="font-size:0.75rem;color:rgba(255,255,255,.85);font-weight:400">' + bilingual('수만휘, 오르비, 에타, 단톡방 1초 복붙', 'Paste in Reddit, Discord, or group chats') + '</div>' +
              '</div>' +
            '</div>' +
            '<span style="font-size:1.1rem">➔</span>' +
          '</button>' +
          '<button type="button" onclick="window.shareAsGift()" style="background:linear-gradient(90deg,#ec4899,#a855f7);color:#fff;border:none;border-radius:14px;padding:13px 18px;font-size:0.94rem;font-weight:800;cursor:pointer;display:flex;align-items:center;justify-content:space-between;box-shadow:0 6px 20px rgba(236,72,153,.3);transition:transform .15s" onmouseover="this.style.transform=\'scale(1.02)\'" onmouseout="this.style.transform=\'none\'">' +
            '<div style="display:flex;align-items:center;gap:10px">' +
              '<span style="font-size:1.3rem">💝</span>' +
              '<div>' +
                '<div>' + bilingual('또 다른 수포자 친구에게 디딤돌 풀이 선물하기', 'Gift Scaffolding Solution to Another Friend') + '</div>' +
                '<div style="font-size:0.75rem;color:rgba(255,255,255,.85);font-weight:400">' + bilingual('초등학생 눈높이 사다리로 수학 개념 구원', 'Help friends master difficult math concepts') + '</div>' +
              '</div>' +
            '</div>' +
            '<span style="font-size:1.1rem">➔</span>' +
          '</button>' +
        '</div>' +
        '<div style="margin-top:16px">' +
          '<button type="button" onclick="document.getElementById(\'matheduViralModal\').remove()" style="background:rgba(255,255,255,.08);color:#94a3b8;border:1px solid rgba(255,255,255,.2);border-radius:10px;padding:9px 18px;font-size:0.85rem;cursor:pointer;transition:.15s" onmouseover="this.style.color=\'#fff\'">' +
            bilingual('🔍 닫고 해설 및 GeoGebra 계속 탐구하기', '🔍 Close & Explore GeoGebra Solutions') +
          '</button>' +
        '</div>' +
      '</div>';

    document.body.appendChild(modal);
  };

  // 5. 친구 도전장(?challenger=...) 및 선물(?gift_from=...) 파라미터 감지 및 상단 배너 표시
  function checkAndShowIncomingChallenge() {
    var challengerName = (urlParams.get('challenger') || '').trim();
    var giftFrom = (urlParams.get('gift_from') || urlParams.get('gift') || '').trim();
    var steps = (urlParams.get('steps') || '').trim();

    var trackFull = document.getElementById('trackFull');

    // 1. 디딤돌 선물(?gift_from=...)로 유입된 경우 따뜻한 환영 카드 노출
    if (giftFrom && trackFull && !document.getElementById('incomingGiftBox')) {
      var gBox = document.createElement('div');
      gBox.id = 'incomingGiftBox';
      gBox.style.cssText = 'background:linear-gradient(135deg,rgba(236,72,153,.18) 0%,rgba(168,85,247,.18) 100%);border:1.5px solid rgba(236,72,153,.65);border-radius:14px;padding:13px 18px;margin:8px 0 14px;width:100%;max-width:440px;box-shadow:0 4px 20px rgba(236,72,153,.25);animation:matheduPopUp .3s ease;text-align:center;box-sizing:border-box';
      gBox.innerHTML = 
        '<div style="font-size:1.06rem;font-weight:800;color:#f472b6;display:flex;align-items:center;justify-content:center;gap:6px">' +
          '💝 <span>' + escapeHtml(giftFrom) + '</span>' + bilingual(' 님이 보낸 디딤돌 수학 선물!', '\'s Math Scaffolding Gift!') +
        '</div>' +
        '<div style="font-size:0.84rem;color:#f1f5f9;margin-top:5px;line-height:1.55">' +
          bilingual(
            '수능 킬러 문제도 겁먹을 필요 없어요! 초등학교 사칙연산 수준의 쉬운 디딤돌부터 한 계단씩 밟아 올라가면 누구나 100% 풀 수 있습니다.',
            'No need to fear complex math problems! With simple micro-steps, anyone can master this problem 100%.'
          ) +
        '</div>' +
        '<div style="font-size:0.78rem;color:#fbcfe8;margin-top:6px;font-weight:700">' +
          bilingual('✨ 가입 없이 아래 [👀 자유 풀기] 버튼을 누르면 즉시 시작됩니다!', '✨ Click the button below to start solving freely in 1 sec!') +
        '</div>';

      var centerSw = document.getElementById('modalCenterLangSwitcher');
      var refNode = (centerSw && centerSw.nextSibling) ? centerSw.nextSibling : (h2 && h2.nextSibling ? h2.nextSibling : null);
      if (refNode) {
        trackFull.insertBefore(gBox, refNode);
      } else {
        trackFull.appendChild(gBox);
      }
    }

    // 2. 친구 도전장(?challenger=...)으로 유입된 경우 도전 박스 노출
    if (challengerName && trackFull && !document.getElementById('incomingChallengeBox')) {
      var box = document.createElement('div');
      box.id = 'incomingChallengeBox';
      box.style.cssText = 'background:linear-gradient(135deg,rgba(245,158,11,.18) 0%,rgba(239,68,68,.18) 100%);border:1.5px solid rgba(245,158,11,.7);border-radius:14px;padding:12px 16px;margin:8px 0 14px;width:100%;max-width:440px;box-shadow:0 4px 20px rgba(245,158,11,.25);animation:matheduPopUp .3s ease;text-align:center;box-sizing:border-box';
      box.innerHTML = 
        '<div style="font-size:1.06rem;font-weight:800;color:#fcd34d;display:flex;align-items:center;justify-content:center;gap:6px">' +
          '⚔️ <span>' + escapeHtml(challengerName) + '</span>' + bilingual(' 님의 수능 킬러 도전장!', '\'s Math Quest Challenge!') +
        '</div>' +
        '<div style="font-size:0.83rem;color:#e2e8f0;margin-top:4px;line-height:1.45">' +
          bilingual(
            '<b>' + escapeHtml(challengerName) + '</b> 님이 이 문제의 ' + (steps ? steps + '단계 ' : '') + '풀이를 완주하고 도전장을 보냈습니다. 너도 오답 없이 완주할 수 있을까?',
            '<b>' + escapeHtml(challengerName) + '</b> finished this problem and challenged you to beat their score!'
          ) +
        '</div>';

      var h2Target = trackFull.querySelector('h2');
      var centerSwTarget = document.getElementById('modalCenterLangSwitcher');
      var refNodeTarget = (centerSwTarget && centerSwTarget.nextSibling) ? centerSwTarget.nextSibling : (h2Target && h2Target.nextSibling ? h2Target.nextSibling : null);
      if (refNodeTarget) {
        trackFull.insertBefore(box, refNodeTarget);
      } else {
        trackFull.appendChild(box);
      }
    }

    // 3. 문제 본문화면 상단 고정 안내 배너
    var wrap = document.querySelector('.wrap');
    if (wrap) {
      if (giftFrom && !document.getElementById('activeGiftBanner')) {
        var gBanner = document.createElement('div');
        gBanner.id = 'activeGiftBanner';
        gBanner.style.cssText = 'background:linear-gradient(90deg,rgba(236,72,153,.18),rgba(168,85,247,.18));border:1px solid rgba(236,72,153,.5);border-radius:12px;padding:10px 16px;margin-bottom:16px;display:flex;align-items:center;justify-content:space-between;color:#fbcfe8;font-size:0.86rem;font-weight:700;flex-wrap:wrap;gap:8px';
        gBanner.innerHTML = 
          '<div style="display:flex;align-items:center;gap:8px">' +
            '<span style="font-size:1.1rem">💝</span>' +
            '<span>' + bilingual('<b>' + escapeHtml(giftFrom) + '</b> 님이 선물한 디딤돌 풀이 진행 중! 천천히 한 계단씩 올라가면 누구나 풀 수 있어요.', 'Gifted by <b>' + escapeHtml(giftFrom) + '</b>! Take your time with each step.') + '</span>' +
          '</div>' +
          '<span style="font-size:0.75rem;background:rgba(236,72,153,.3);border:1px solid rgba(236,72,153,.6);padding:3px 10px;border-radius:8px;color:#fff;font-weight:800">STUDY GIFT</span>';
        wrap.insertBefore(gBanner, wrap.firstChild);
      } else if (challengerName && !document.getElementById('activeChallengerBanner')) {
        var banner = document.createElement('div');
        banner.id = 'activeChallengerBanner';
        banner.style.cssText = 'background:linear-gradient(90deg,rgba(245,158,11,.18),rgba(239,68,68,.18));border:1px solid rgba(245,158,11,.5);border-radius:12px;padding:10px 16px;margin-bottom:16px;display:flex;align-items:center;justify-content:space-between;color:#fde68a;font-size:0.86rem;font-weight:700;flex-wrap:wrap;gap:8px';
        banner.innerHTML = 
          '<div style="display:flex;align-items:center;gap:8px">' +
            '<span style="font-size:1.1rem">⚔️</span>' +
            '<span>' + bilingual('<b>' + escapeHtml(challengerName) + '</b> 님의 도전 진행 중! 끝까지 완주하여 승리를 증명하세요!', 'Challenged by <b>' + escapeHtml(challengerName) + '</b>! Clear all steps to win!') + '</span>' +
          '</div>' +
          '<span style="font-size:0.75rem;background:rgba(245,158,11,.3);border:1px solid rgba(245,158,11,.6);padding:3px 10px;border-radius:8px;color:#fff;font-weight:800">VS DUEL</span>';
        wrap.insertBefore(banner, wrap.firstChild);
      }
    }
  }

  // 6. 해설 하단 상시 선물/도전장 공유 카드 삽입
  function injectAltruisticShareCard() {
    if (document.getElementById('matheduAltruisticShareCard')) return;
    var target = document.querySelector('.sol') || document.querySelector('.wrap');
    if (!target) return;

    var card = document.createElement('div');
    card.id = 'matheduAltruisticShareCard';
    card.className = 'altruistic-share-card';
    card.style.cssText = 'margin:32px 0 16px;background:#ffffff;border:1.5px solid #f472b6;border-radius:18px;padding:22px;color:#1b1b1d;text-align:center;box-shadow:0 4px 20px rgba(19,27,46,.05)';
    card.innerHTML = 
      '<div style="font-size:2rem;margin-bottom:6px">💝</div>' +
      '<h3 style="margin:0 0 6px;font-size:1.18rem;color:#db2777">' +
        bilingual('이 문제가 헷갈려하는 친구에게 디딤돌 풀이 선물하기', 'Share this Scaffolding Solution with Friends') +
      '</h3>' +
      '<p style="font-size:0.88rem;color:#45464d;line-height:1.6;max-width:540px;margin:0 auto 16px">' +
        bilingual(
          '아무리 복잡한 수능 킬러 문제도 초등학생 눈높이 미세 디딤돌과 수학자료실(min7014)의 시각적 증명으로 보면 누구나 직관적으로 이해할 수 있습니다. 함께 공부하는 친구들에게 이 풀이를 선물해보세요!',
          'Complex exam problems become crystal clear with micro-scaffolding steps and visual proofs. Share this friendly learning gift with your classmates!'
        ) +
      '</p>' +
      '<div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap">' +
        '<button type="button" onclick="window.shareAsGift()" style="background:linear-gradient(90deg,#ec4899,#a855f7);color:#fff;font-weight:800;border:none;padding:10px 20px;border-radius:10px;cursor:pointer;display:inline-flex;align-items:center;gap:6px;transition:transform .15s" onmouseover="this.style.transform=\'scale(1.03)\'" onmouseout="this.style.transform=\'none\'">' +
          bilingual('🎁 친구에게 풀이 선물하기 (카톡/공유)', '🎁 Gift to Friend (Kakao/Share)') +
        '</button>' +
        '<button type="button" onclick="window.shareAsChallenge()" style="background:#fffbeb;color:#b45309;border:1px solid #fcd34d;font-weight:700;padding:10px 18px;border-radius:10px;cursor:pointer;display:inline-flex;align-items:center;gap:6px;transition:transform .15s" onmouseover="this.style.transform=\'scale(1.03)\'" onmouseout="this.style.transform=\'none\'">' +
          bilingual('⚔️ 친구에게 도전장 보내기', '⚔️ Send Challenge to Friend') +
        '</button>' +
        '<button type="button" onclick="window.copyCommunityScoreText()" style="background:#f6f3f5;color:#1b1b1d;border:1px solid #e4e2e4;font-weight:600;padding:10px 18px;border-radius:10px;cursor:pointer;display:inline-flex;align-items:center;gap:6px;transition:transform .15s" onmouseover="this.style.transform=\'scale(1.03)\'" onmouseout="this.style.transform=\'none\'">' +
          bilingual('📋 커뮤니티 자랑 텍스트 복사', '📋 Copy Community Text') +
        '</button>' +
      '</div>';

    if (target.classList && target.classList.contains('sol')) {
      target.appendChild(card);
    } else {
      var sol = document.querySelector('.sol');
      if (sol) {
        sol.parentNode.insertBefore(card, sol.nextSibling);
      } else {
        target.appendChild(card);
      }
    }
  }

  // 🌐 모달 및 전체 화면 언어 전환 제어기
  window.setBoardLanguage = function(lang) {
    if (lang !== 'ko' && lang !== 'en') return;
    document.documentElement.lang = lang;
    try {
      localStorage.setItem('mathedu_lang', lang);
      localStorage.setItem('mathedu_lang_manual', 'true');
    } catch(e) {}

    updateModalLangButtons(lang);

    if (window.setBoardLang) {
      window.setBoardLang(lang, true);
    }
    if (window.MatheduI18n && window.MatheduI18n.setLanguage) {
      window.MatheduI18n.setLanguage(lang);
    }

    var sn = document.getElementById('studentName');
    if (sn) sn.placeholder = (lang === 'en') ? 'Enter name' : '이름 입력';

    var pin = document.getElementById('studentPin');
    if (pin) pin.placeholder = (lang === 'en') ? '4-digit PIN (optional)' : '간편비번 4자리 (선택)';

    try {
      window.dispatchEvent(new CustomEvent('mathedu:lang-changed', { detail: { lang: lang } }));
    } catch(e) {}
  };

  function updateModalLangButtons(lang) {
    var isEn = (lang === 'en' || (typeof lang === 'string' && lang.toLowerCase().startsWith('en')));
    var btnKo = document.getElementById('btnTrackFullLangKo');
    var btnEn = document.getElementById('btnTrackFullLangEn');
    if (btnKo && btnEn) {
      if (isEn) {
        btnKo.style.background = 'transparent';
        btnKo.style.color = '#45464d';
        btnKo.style.fontWeight = '700';
        btnEn.style.background = '#38bdf8';
        btnEn.style.color = '#0b1020';
        btnEn.style.fontWeight = '800';
      } else {
        btnKo.style.background = '#38bdf8';
        btnKo.style.color = '#0b1020';
        btnKo.style.fontWeight = '800';
        btnEn.style.background = 'transparent';
        btnEn.style.color = '#45464d';
        btnEn.style.fontWeight = '700';
      }
    }

    var cKo = document.getElementById('btnModalCenterLangKo');
    var cEn = document.getElementById('btnModalCenterLangEn');
    if (cKo && cEn) {
      if (isEn) {
        cKo.style.background = 'transparent';
        cKo.style.color = '#45464d';
        cKo.style.fontWeight = '700';
        cKo.style.boxShadow = 'none';
        cEn.style.background = 'linear-gradient(135deg, #38bdf8 0%, #818cf8 100%)';
        cEn.style.color = '#0b1020';
        cEn.style.fontWeight = '800';
        cEn.style.boxShadow = '0 2px 10px rgba(56,189,248,.45)';
      } else {
        cKo.style.background = 'linear-gradient(135deg, #38bdf8 0%, #818cf8 100%)';
        cKo.style.color = '#0b1020';
        cKo.style.fontWeight = '800';
        cKo.style.boxShadow = '0 2px 10px rgba(56,189,248,.45)';
        cEn.style.background = 'transparent';
        cEn.style.color = '#45464d';
        cEn.style.fontWeight = '700';
        cEn.style.boxShadow = 'none';
      }
    }
  }

  // 🌐 언어 변경 이벤트 리스너 (mathedu:lang-changed)
  window.addEventListener('mathedu:lang-changed', function(e) {
    var lang = (e && e.detail && e.detail.lang) || document.documentElement.lang || 'ko';
    var isEn = lang.toLowerCase().startsWith('en');
    
    // Update modal buttons
    updateModalLangButtons(lang);

    // Update placeholders
    var inputs = document.querySelectorAll('input[data-ko-placeholder]');
    inputs.forEach(function(inp) {
      inp.placeholder = isEn ? (inp.getAttribute('data-en-placeholder') || '') : (inp.getAttribute('data-ko-placeholder') || '');
    });

    // Update titles
    var titleEls = document.querySelectorAll('[data-ko-title]');
    titleEls.forEach(function(el) {
      el.title = isEn ? (el.getAttribute('data-en-title') || '') : (el.getAttribute('data-ko-title') || '');
    });
  });


  // ════════════════════════════════════════════════════════════════════════
  // 🎓 수학교육학 5대 학문 통합 엔진 (Academic Math Pedagogy Engine v1.0)
  // 1. CPA & Duval 다중 표상 변환기 (구체적 수치 ⟷ 기하 도형·GeoGebra ⟷ 대수 기호·흐름도 동시 대조)
  // 2. Vygotsky ZPD & Sweller 인지부하이론 (3단계 무오류 점진적 힌트 사다리 & 레고 브릿지)
  // 3. Roediger 능동적 인출 효과 (블라인드 선지 가리기 · 생각 먼저 인출 연습 모드)
  // 4. Pólya & Schoenfeld 발견술·메타인지 자기조절 코치 + 데카르트 인페이지 수학 연습장
  // 5. Hattie 정교한 오개념 진단 피드백 & Freudenthal 안내된 재발명(Guided Reinvention) 연결
  // ════════════════════════════════════════════════════════════════════════

  var PEDAGOGY_STATE_KEY = 'mathedu_academic_pedagogy_v1';

  function loadPedagogyState() {
    try {
      var raw = localStorage.getItem(PEDAGOGY_STATE_KEY);
      if (!raw) return { retrievalBlindMode: false, cpaCount: 0, hintUsed: 0, retrievalSuccess: 0, metacogChecks: 0, scratchpadUsed: 0 };
      return Object.assign({ retrievalBlindMode: false, cpaCount: 0, hintUsed: 0, retrievalSuccess: 0, metacogChecks: 0, scratchpadUsed: 0 }, JSON.parse(raw));
    } catch (e) {
      return { retrievalBlindMode: false, cpaCount: 0, hintUsed: 0, retrievalSuccess: 0, metacogChecks: 0, scratchpadUsed: 0 };
    }
  }

  function savePedagogyState(st) {
    try { localStorage.setItem(PEDAGOGY_STATE_KEY, JSON.stringify(st)); } catch (e) {}
  }

  function injectAcademicPedagogyStyles() {
    if (document.getElementById('matheduAcademicPedagogyStyles')) return;
    var st = document.createElement('style');
    st.id = 'matheduAcademicPedagogyStyles';
    st.textContent = [
      '.acad-workbench-bar{margin:12px 0 16px;padding:12px 16px;border-radius:16px;background:linear-gradient(135deg,#f8fafc 0%,#eff6ff 100%);border:1.5px solid #bfdbfe;box-shadow:0 4px 14px rgba(0,99,152,0.06);display:flex;flex-direction:column;gap:10px;}',
      'html.dark-theme .acad-workbench-bar{background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);border-color:#334155;color:#f8fafc;}',
      '.acad-workbench-top{display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap;}',
      '.acad-workbench-title{display:inline-flex;align-items:center;gap:6px;font-size:0.84rem;font-weight:800;color:#006398;}',
      'html.dark-theme .acad-workbench-title{color:#38bdf8;}',
      '.acad-pill-row{display:flex;align-items:center;gap:6px;flex-wrap:wrap;}',
      '.acad-pill-btn{display:inline-flex;align-items:center;gap:5px;padding:6px 12px;border-radius:999px;border:1px solid #cbd5e1;background:#ffffff;color:#1e293b;font-size:0.77rem;font-weight:800;cursor:pointer;transition:all 0.16s ease;font-family:inherit;}',
      'html.dark-theme .acad-pill-btn{background:#1e293b;border-color:#475569;color:#e2e8f0;}',
      '.acad-pill-btn:hover,.acad-pill-btn.active{background:#006398;color:#ffffff;border-color:#006398;box-shadow:0 3px 10px rgba(0,99,152,0.22);}',
      '.acad-drawer-panel{display:none;margin-top:4px;padding:14px;border-radius:12px;background:#ffffff;border:1px solid #cbd5e1;color:#1e293b;font-size:0.84rem;line-height:1.6;}',
      'html.dark-theme .acad-drawer-panel{background:#0f172a;border-color:#334155;color:#e2e8f0;}',
      '.acad-drawer-panel.open{display:block;animation:matheduStepFadeIn 0.25s ease-out;}',
      '.acad-cpa-tabs{display:flex;gap:6px;margin-bottom:10px;flex-wrap:wrap;border-bottom:1px solid #e2e8f0;padding-bottom:8px;}',
      '.acad-cpa-tab{padding:5px 12px;border-radius:8px;border:1px solid #cbd5e1;background:#f8fafc;color:#475569;font-size:0.76rem;font-weight:800;cursor:pointer;}',
      '.acad-cpa-tab.active{background:#0284c7;color:#ffffff;border-color:#0284c7;}',
      '.acad-blind-mask{margin-top:8px;padding:14px;border-radius:12px;background:linear-gradient(135deg,rgba(2,132,199,0.08),rgba(79,70,229,0.08));border:1.5px dashed #0284c7;text-align:center;}',
      '.acad-blind-btn{padding:8px 16px;border-radius:999px;border:none;background:linear-gradient(135deg,#006398,#4f46e5);color:#ffffff;font-size:0.8rem;font-weight:800;cursor:pointer;box-shadow:0 4px 12px rgba(0,99,152,0.25);}',
      '.acad-hint-btn{margin-right:6px;padding:5px 11px;border-radius:8px;border:1px solid #93c5fd;background:#eff6ff;color:#0369a1;font-size:0.76rem;font-weight:800;cursor:pointer;transition:0.15s;}',
      '.acad-hint-btn:hover{background:#dbeafe;}',
      '.acad-hint-box{display:none;margin-top:8px;padding:11px 14px;border-radius:10px;background:#f0f9ff;border-left:4px solid #0284c7;color:#0f172a;font-size:0.82rem;line-height:1.55;}',
      'html.dark-theme .acad-hint-box{background:#1e293b;color:#e2e8f0;}',
      '.acad-hint-box.show{display:block;}',
      '.acad-diag-box{margin:0 0 12px;padding:12px 14px;border-radius:10px;font-size:0.83rem;line-height:1.55;}',
      '.acad-diag-wrong{background:#fef2f2;border:1.5px solid #fca5a5;color:#7f1d1d;}',
      'html.dark-theme .acad-diag-wrong{background:rgba(127,29,29,0.25);border-color:#ef4444;color:#fecaca;}',
      '.acad-diag-correct{background:#ecfdf5;border:1.5px solid #6ee7b7;color:#065f46;}',
      'html.dark-theme .acad-diag-correct{background:rgba(6,95,70,0.25);border-color:#10b981;color:#a7f3d0;}'
    ].join('\n');
    (document.head || document.documentElement).appendChild(st);
  }

  window.initAcademicPedagogyEngine = initAcademicPedagogyEngine;
  function initAcademicPedagogyEngine() {
    var qs = Array.from(document.querySelectorAll('.q'));
    if (qs.length === 0) return;
    injectAcademicPedagogyStyles();

    var pState = loadPedagogyState();

    // 1. 상단 수학교육학 5대 원리 워크벤치 바 주입
    var targetAnchor = document.querySelector('.stitch-filter-card') || document.getElementById('examSymContainer');
    if (targetAnchor && !document.getElementById('acadWorkbenchBar')) {
      var wb = document.createElement('div');
      wb.id = 'acadWorkbenchBar';
      wb.className = 'acad-workbench-bar';
      wb.innerHTML =
        '<div class="acad-workbench-top">' +
          '<div class="acad-workbench-title">' +
            '<span>🎓</span>' +
            bilingual('수학교육학 5대 검증 학습 도구 (CPA 다중표상 · 능동인출 · ZPD 비계 · 메타인지)', '5 Proven Math Pedagogy Tools (CPA · Retrieval · ZPD · Metacognition)') +
          '</div>' +
          '<div class="acad-pill-row">' +
            '<button type="button" class="acad-pill-btn" id="btnAcadCpa" onclick="window.toggleAcadDrawer(\'cpa\')">' +
              bilingual('🎨 CPA 다중표상 대조', '🎨 CPA Multi-Representation') +
            '</button>' +
            '<button type="button" class="acad-pill-btn active" id="btnAcadRetrieval" onclick="window.toggleAcadRetrievalMode()">' +
              bilingual('✍️ 탈-5지선다 창의 구성 모드 ON (기본)', '✍️ Creative Constructive Mode ON') +
            '</button>' +
            '<button type="button" class="acad-pill-btn" id="btnAcadScratch" onclick="window.toggleAcadDrawer(\'scratch\')">' +
              bilingual('✏️ 데카르트 연습장', '✏️ Math Scratchpad') +
            '</button>' +
            '<button type="button" class="acad-pill-btn" id="btnAcadMetacog" onclick="window.toggleAcadDrawer(\'metacog\')">' +
              bilingual('🧭 폴리아·쇤펠드 코치', '🧭 Pólya & Schoenfeld Coach') +
            '</button>' +
            '<button type="button" class="acad-pill-btn" id="btnAcadVariation" onclick="window.toggleAcadDrawer(\'variation\')">' +
              bilingual('🔄 변이·전이 & 유레카 노트', '🔄 Variation & Eureka Note') +
            '</button>' +
            '<button type="button" class="acad-pill-btn" id="btnAcadYoutube" onclick="window.toggleAcadDrawer(\'youtube\')" style="background:linear-gradient(135deg,#e11d48,#be123c);color:#ffffff;border-color:#e11d48">' +
              bilingual('🎬 @min7014_ai 유튜브 시각 증명', '🎬 @min7014_ai YouTube Proof') +
            '</button>' +
            '<button type="button" class="acad-pill-btn" id="btnAcadYtShare" onclick="window.shareProblemWithYoutube()" style="background:#fef2f2;color:#be123c;border-color:#fda4af">' +
              bilingual('📢 유튜브+문제 1초 홍보 공유', '📢 Share Video + Problem') +
            '</button>' +
          '</div>' +
        '</div>' +
        '<div id="acadDrawerCpa" class="acad-drawer-panel"></div>' +
        '<div id="acadDrawerScratch" class="acad-drawer-panel"></div>' +
        '<div id="acadDrawerMetacog" class="acad-drawer-panel"></div>' +
        '<div id="acadDrawerVariation" class="acad-drawer-panel"></div>' +
        '<div id="acadDrawerYoutube" class="acad-drawer-panel"></div>';

      if (targetAnchor.parentNode) {
        targetAnchor.parentNode.insertBefore(wb, targetAnchor.nextSibling);
      }
    }

    // 2. CPA 다중 표상 드로어 렌더러 (Bruner EIS / Duval 다중 표상 동시 대조)
    function renderCpaDrawer(tab) {
      var drawer = document.getElementById('acadDrawerCpa');
      if (!drawer) return;
      var curTab = tab || 'iconic';
      var svgFig = document.querySelector('.math-visual-diagram');
      var svgHtml = svgFig ? svgFig.outerHTML : '<p>시각적 도형 다이어그램이 아래 해설 섹션에 준비되어 있습니다.</p>';
      var symEl = document.getElementById('examSymContainer');
      var symHtml = symEl ? symEl.innerHTML : '';
      var flowEl = document.querySelector('.math-schematic-flow');
      var flowHtml = flowEl ? flowEl.outerHTML : '';
      var step1Know = qs[0] && qs[0].previousElementSibling && qs[0].previousElementSibling.classList.contains('know')
        ? qs[0].previousElementSibling.innerHTML
        : '작은 자연수($n=1, 2, 3$ 또는 $x=0, 1, 2$)를 직접 대입해 규칙을 먼저 관찰하세요.';

      var ggbBtn = document.querySelector('.min-btn-ggb, .min-btn-algeo');
      var ggbLinkHtml = ggbBtn
        ? '<div style="margin-top:8px;text-align:right"><button type="button" class="acad-pill-btn" onclick="var el=document.querySelector(\'.min7014-addon-card\');if(el)el.scrollIntoView({behavior:\'smooth\'});">📐 min7014 동적 기하(GeoGebra/AlgeoMath) 바로 조작하기 ➔</button></div>'
        : '';

      var bodyHtml = '';
      if (curTab === 'iconic') {
        bodyHtml =
          '<div style="font-size:0.79rem;color:#0369a1;font-weight:700;margin-bottom:6px">' +
            bilingual('💡 [뒤발(Duval) & 브루너(Bruner) 영상적 표상]: 아래 문제를 풀면서 시각적 기하·개념 도형을 동시에 대조해 보세요.', '💡 [Duval & Bruner Iconic Representation]: Compare the visual diagram side-by-side while solving each step.') +
          '</div>' +
          svgHtml + ggbLinkHtml;
      } else if (curTab === 'enactive') {
        bodyHtml =
          '<div style="font-size:0.79rem;color:#047857;font-weight:700;margin-bottom:6px">' +
            bilingual('💡 [프로이덴탈(Freudenthal) 구체적 수치 실험]: 추상적인 문자($x, n, k$)가 낯설 때는 가장 작은 정수($1, 2, 3$)를 대입해 구체적 감각을 먼저 깨우세요.', '💡 [Freudenthal Concrete Experiment]: Substitute small integers (1, 2, 3) to build concrete intuition before algebraic manipulation.') +
          '</div>' +
          '<div style="padding:10px 12px;border-radius:10px;background:#f0fdf4;border:1px solid #86efac;color:#065f46;margin-bottom:8px">' + step1Know + '</div>' +
          '<div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:6px">' +
            '<span style="font-size:0.78rem;font-weight:800">🔢 빠른 수식/수치 대입 계산기:</span>' +
            '<input id="acadQuickCalcInput" type="text" placeholder="예: (3^2)*(1/4) - 1/2 또는 2*3+1" style="flex:1;min-width:180px;padding:6px 10px;border:1px solid #cbd5e1;border-radius:8px;font-size:0.8rem">' +
            '<button type="button" class="acad-pill-btn" onclick="window.runAcadQuickCalc()">계산 확인</button>' +
            '<span id="acadQuickCalcOut" style="font-weight:900;color:#006398"></span>' +
          '</div>';
      } else {
        bodyHtml =
          '<div style="font-size:0.79rem;color:#4f46e5;font-weight:700;margin-bottom:6px">' +
            bilingual('💡 [기호 번역 & 도식화 흐름도]: 수식 기호의 약속과 단계별 연쇄 흐름을 한눈에 대조합니다.', '💡 [Symbolic & Schematic Flowchart]: Connect symbol definitions directly to the overall logical flow.') +
          '</div>' +
          '<div style="margin-bottom:10px">' + symHtml + '</div>' +
          flowHtml;
      }

      drawer.innerHTML =
        '<div class="acad-cpa-tabs">' +
          '<button type="button" class="acad-cpa-tab' + (curTab === 'iconic' ? ' active' : '') + '" onclick="window.switchAcadCpaTab(\'iconic\')">🎨 영상적 표상 (시각 도형·GeoGebra)</button>' +
          '<button type="button" class="acad-cpa-tab' + (curTab === 'enactive' ? ' active' : '') + '" onclick="window.switchAcadCpaTab(\'enactive\')">🧱 활동적 표상 (구체적 수치·초등 직관)</button>' +
          '<button type="button" class="acad-cpa-tab' + (curTab === 'symbolic' ? ' active' : '') + '" onclick="window.switchAcadCpaTab(\'symbolic\')">📐 기호적 표상 (기호 번역·도식화 흐름도)</button>' +
        '</div>' +
        bodyHtml;

      if (window.MathJax && window.MathJax.typesetPromise) {
        window.MathJax.typesetPromise([drawer]).catch(function() {});
      }
    }

    window.switchAcadCpaTab = function(tab) {
      renderCpaDrawer(tab);
    };

    window.runAcadQuickCalc = function() {
      var inp = document.getElementById('acadQuickCalcInput');
      var out = document.getElementById('acadQuickCalcOut');
      if (!inp || !out) return;
      var expr = (inp.value || '').replace(/\^/g, '**').replace(/[^0-9+\-*/().\s*]/g, '');
      if (!expr.trim()) return;
      try {
        var val = Function('"use strict";return (' + expr + ')')();
        out.textContent = '⇒ ' + (typeof val === 'number' && !isFinite(val) ? '정의되지 않음' : Number(val.toFixed(6)));
      } catch (e) {
        out.textContent = '수식 확인 필요';
      }
    };

    // 3. 데카르트 인페이지 수학 연습장 (Scratchpad Canvas)
    function renderScratchDrawer() {
      var drawer = document.getElementById('acadDrawerScratch');
      if (!drawer || drawer.dataset.ready === '1') return;
      drawer.dataset.ready = '1';
      drawer.innerHTML =
        '<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;margin-bottom:8px">' +
          '<span style="font-size:0.8rem;font-weight:800;color:#006398">✏️ 데카르트 수학 연습장 — 보조선 작도·수식 전개·작은 수 대입을 직접 손이나 마우스로 적어보세요</span>' +
          '<div style="display:flex;gap:6px;flex-wrap:wrap">' +
            '<button type="button" class="acad-pill-btn active" id="scrPenBlue" onclick="window.setAcadScratchPen(\'#006398\',2.4,this)">파란 펜</button>' +
            '<button type="button" class="acad-pill-btn" id="scrPenRed" onclick="window.setAcadScratchPen(\'#e11d48\',2.4,this)">보조선(빨강)</button>' +
            '<button type="button" class="acad-pill-btn" id="scrPenGold" onclick="window.setAcadScratchPen(\'rgba(245,158,11,0.35)\',12,this)">형광펜</button>' +
            '<button type="button" class="acad-pill-btn" onclick="window.clearAcadScratch()">🗑️ 전체 지우기</button>' +
          '</div>' +
        '</div>' +
        '<canvas id="acadScratchCanvas" width="860" height="240" style="width:100%;height:220px;background:#ffffff;background-image:radial-gradient(#cbd5e1 1px,transparent 1px);background-size:18px 18px;border:1.5px solid #94a3b8;border-radius:10px;touch-action:none;cursor:crosshair;display:block"></canvas>';

      var cvs = document.getElementById('acadScratchCanvas');
      if (!cvs) return;
      var ctx = cvs.getContext('2d');
      var drawing = false;
      window._acadPenColor = '#006398';
      window._acadPenWidth = 2.4;

      function getPos(ev) {
        var r = cvs.getBoundingClientRect();
        var clientX = ev.touches && ev.touches[0] ? ev.touches[0].clientX : ev.clientX;
        var clientY = ev.touches && ev.touches[0] ? ev.touches[0].clientY : ev.clientY;
        return {
          x: (clientX - r.left) * (cvs.width / r.width),
          y: (clientY - r.top) * (cvs.height / r.height)
        };
      }
      function start(ev) {
        drawing = true;
        var p = getPos(ev);
        ctx.beginPath();
        ctx.moveTo(p.x, p.y);
        ev.preventDefault();
      }
      function move(ev) {
        if (!drawing) return;
        var p = getPos(ev);
        ctx.strokeStyle = window._acadPenColor;
        ctx.lineWidth = window._acadPenWidth;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        ctx.lineTo(p.x, p.y);
        ctx.stroke();
        ev.preventDefault();
      }
      function stop() { drawing = false; }

      cvs.addEventListener('mousedown', start);
      cvs.addEventListener('mousemove', move);
      window.addEventListener('mouseup', stop);
      cvs.addEventListener('touchstart', start, { passive: false });
      cvs.addEventListener('touchmove', move, { passive: false });
      cvs.addEventListener('touchend', stop);
    }

    window.setAcadScratchPen = function(color, width, btnEl) {
      window._acadPenColor = color;
      window._acadPenWidth = width;
      var parent = btnEl && btnEl.parentNode;
      if (parent) {
        parent.querySelectorAll('.acad-pill-btn').forEach(function(b) { b.classList.remove('active'); });
      }
      if (btnEl) btnEl.classList.add('active');
    };

    window.clearAcadScratch = function() {
      var cvs = document.getElementById('acadScratchCanvas');
      if (!cvs) return;
      cvs.getContext('2d').clearRect(0, 0, cvs.width, cvs.height);
    };

    // 4. 폴리아(Pólya) 4단계 발견술 & 쇤펠드(Schoenfeld) 메타인지 코치 드로어
    function renderMetacogDrawer() {
      var drawer = document.getElementById('acadDrawerMetacog');
      if (!drawer) return;
      var st = loadPedagogyState();
      var doneCnt = document.querySelectorAll('.q.done').length;
      drawer.innerHTML =
        '<div style="font-weight:800;color:#006398;margin-bottom:8px">🧭 폴리아(G. Pólya) 문제해결 4단계 & 쇤펠드(Schoenfeld) 메타인지 자기조절 체크리스트</div>' +
        '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:8px;margin-bottom:10px">' +
          '<label style="display:flex;align-items:flex-start;gap:6px;padding:8px 10px;border-radius:10px;background:#f8fafc;border:1px solid #cbd5e1;cursor:pointer;font-size:0.79rem">' +
            '<input type="checkbox" onchange="window.recordAcadMetacogCheck()"> <span><b>1. 문제 이해 (Understand)</b><br>구하려는 목표값과 주어진 조건, 정의역·진수·부호 범위를 분리했는가?</span>' +
          '</label>' +
          '<label style="display:flex;align-items:flex-start;gap:6px;padding:8px 10px;border-radius:10px;background:#f8fafc;border:1px solid #cbd5e1;cursor:pointer;font-size:0.79rem">' +
            '<input type="checkbox" onchange="window.recordAcadMetacogCheck()"> <span><b>2. 계획 수립 (Plan · CPA)</b><br>수식을 도형(그래프)으로, 또는 작은 수($n=1,2$)로 먼저 실험해 보았는가?</span>' +
          '</label>' +
          '<label style="display:flex;align-items:flex-start;gap:6px;padding:8px 10px;border-radius:10px;background:#f8fafc;border:1px solid #cbd5e1;cursor:pointer;font-size:0.79rem">' +
            '<input type="checkbox" onchange="window.recordAcadMetacogCheck()"> <span><b>3. 계획 실행 (Carry Out)</b><br>앞 단계 디딤돌에서 얻은 식을 다음 단계의 빈칸에 레고처럼 결합했는가?</span>' +
          '</label>' +
          '<label style="display:flex;align-items:flex-start;gap:6px;padding:8px 10px;border-radius:10px;background:#f8fafc;border:1px solid #cbd5e1;cursor:pointer;font-size:0.79rem">' +
            '<input type="checkbox" onchange="window.recordAcadMetacogCheck()"> <span><b>4. 반성적 점검 (Look Back)</b><br>구한 답을 원래 조건에 역산 대입하거나 다른 관점(기하/대수)으로 검증했는가?</span>' +
          '</label>' +
        '</div>' +
        '<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;padding:8px 12px;border-radius:10px;background:#eff6ff;border:1px solid #bfdbfe;font-size:0.78rem;color:#1e3a8a">' +
          '<span>📊 <b>나의 수학교육학 5대 학습 역량 누적 지표</b></span>' +
          '<span>CPA 표상 대조: <b>' + st.cpaCount + '회</b> · 능동 인출 성공: <b>' + st.retrievalSuccess + '회</b> · ZPD 비계 활용: <b>' + st.hintUsed + '회</b> · 메타인지 점검: <b>' + st.metacogChecks + '회</b> · 현재 문항 진도: <b>' + doneCnt + '/' + qs.length + '</b></span>' +
        '</div>';
    }

    window.recordAcadMetacogCheck = function() {
      var st = loadPedagogyState();
      st.metacogChecks = (st.metacogChecks || 0) + 1;
      savePedagogyState(st);
      if (window.MatheduGame && window.MatheduGame.addXP) {
        window.MatheduGame.addXP(5, '🧭 메타인지 자기점검');
      }
    };

    // 4-2. 마르톤의 변이 이론(Variation Theory) & 파인만 1줄 자기설명(Feynman Self-Explanation) 유레카 노트 드로어
    function renderVariationDrawer() {
      var drawer = document.getElementById('acadDrawerVariation');
      if (!drawer) return;
      var notesMap = {};
      try { notesMap = JSON.parse(localStorage.getItem('mathedu_eureka_notes_v1') || '{}'); } catch (e) {}
      var savedNote = (notesMap[currentSlug] && notesMap[currentSlug].note) ? notesMap[currentSlug].note : '';
      var probTitle = getProblemTitle();

      drawer.innerHTML =
        '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px">' +
          '<div style="padding:12px;border-radius:10px;background:#f8fafc;border:1px solid #cbd5e1">' +
            '<div style="font-weight:800;color:#006398;margin-bottom:6px">🔄 마르톤의 변이 이론 (Marton Variation Theory) 사고 실험</div>' +
            '<div style="font-size:0.78rem;color:#334155;line-height:1.55">' +
              '• <b>불변 원리 포착</b>: 숫자와 식의 형태가 바뀌어도 이 문제에서 절대 변하지 않는 <b>단 하나의 핵심 성질</b>은 무엇인가요?<br>' +
              '• <b>조건 변이 실험</b>: 만약 주어진 지수·계수·부호가 역수나 반대 부호로 바뀐다면 <b>3단계 (가)</b>와 <b>4단계 (나)</b> 식은 어떻게 달라질까요?<br>' +
              '• <b>역문제(Converse) 구성</b>: 최종 정답을 조건으로 주고 처음 식의 상수를 미지수 $k$로 둔다면 어떤 순서로 역추적해야 할까요?' +
            '</div>' +
            '<div style="margin-top:8px;display:flex;gap:6px;flex-wrap:wrap">' +
              '<button type="button" class="acad-pill-btn" onclick="if(window.stitchRunGlobalSearch)window.stitchRunGlobalSearch()">🔗 동일 단원 유사 기출 전이 훈련 ➔</button>' +
            '</div>' +
          '</div>' +
          '<div style="padding:12px;border-radius:10px;background:#fefce8;border:1px solid #fde047">' +
            '<div style="font-weight:800;color:#b45309;margin-bottom:6px">💡 파인만 1줄 자기설명 (Feynman Self-Explanation · d = 0.64)</div>' +
            '<div style="font-size:0.77rem;color:#713f12;margin-bottom:6px">이 문제를 풀면서 깨달은 <b>결정적 한 줄 열쇠(보조선, 공식 변환, 함정 주의점)</b>를 내 언어로 요약해 두면 장기기억 전이율이 2배 이상 높아집니다.</div>' +
            '<textarea id="acadEurekaNoteInput" rows="2" placeholder="예: 밑을 3으로 통일한 뒤 지수 법칙으로 합치면 지수가 0이 되어 3^0 = 1이 된다!" style="width:100%;padding:8px;border-radius:8px;border:1px solid #facc15;background:#ffffff;color:#1e293b;font-size:0.8rem;resize:vertical;box-sizing:border-box">' + escapeHtml(savedNote) + '</textarea>' +
            '<div style="display:flex;justify-content:space-between;align-items:center;margin-top:6px;gap:6px;flex-wrap:wrap">' +
              '<span id="acadEurekaSavedStatus" style="font-size:0.75rem;color:#059669;font-weight:800">' + (savedNote ? '✅ 내 유레카 노트에 저장됨' : '') + '</span>' +
              '<button type="button" class="acad-pill-btn" style="background:#d97706;color:#ffffff;border-color:#d97706" onclick="window.saveAcadEurekaNote()">💾 나만의 유레카 노트 저장 (+20 XP)</button>' +
            '</div>' +
          '</div>' +
        '</div>';
    }

    window.saveAcadEurekaNote = function() {
      var inp = document.getElementById('acadEurekaNoteInput');
      var stEl = document.getElementById('acadEurekaSavedStatus');
      if (!inp) return;
      var txt = (inp.value || '').trim();
      if (!txt) return;
      try {
        var map = JSON.parse(localStorage.getItem('mathedu_eureka_notes_v1') || '{}');
        var isNew = !map[currentSlug];
        map[currentSlug] = {
          slug: currentSlug,
          title: getProblemTitle(),
          note: txt,
          updatedAt: new Date().toISOString()
        };
        localStorage.setItem('mathedu_eureka_notes_v1', JSON.stringify(map));
        if (stEl) stEl.textContent = '✅ 저장 완료! (메인 화면 유레카 노트에서 모아보기 가능)';
        if (isNew && window.MatheduGame && window.MatheduGame.addXP) {
          window.MatheduGame.addXP(20, '💡 파인만 1줄 유레카 노트 작성');
        }
      } catch (e) {}
    };

    window.recordStepClinicWeakness = function(stepIndex, reasonType) {
      try {
        var raw = localStorage.getItem('mathedu_step_clinic_v1');
        var data = raw ? JSON.parse(raw) : { stepCounts: { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0 }, reviewQueue: {} };
        if (!data.stepCounts) data.stepCounts = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0 };
        if (!data.reviewQueue) data.reviewQueue = {};
        var sKey = Math.min(6, Math.max(1, stepIndex + 1));
        data.stepCounts[sKey] = (data.stepCounts[sKey] || 0) + 1;
        var prevItem = data.reviewQueue[currentSlug] || { count: 0 };
        var intervals = [1, 3, 7, 14];
        var nextDays = intervals[Math.min(intervals.length - 1, prevItem.count || 0)];
        var nextReviewDate = new Date(Date.now() + nextDays * 86400000).toISOString().slice(0, 10);
        data.reviewQueue[currentSlug] = {
          slug: currentSlug,
          title: getProblemTitle(),
          weakStep: sKey,
          reason: reasonType || 'wrong',
          count: (prevItem.count || 0) + 1,
          nextReviewDate: nextReviewDate,
          updatedAt: new Date().toISOString()
        };
        localStorage.setItem('mathedu_step_clinic_v1', JSON.stringify(data));
      } catch (e) {}
    };

    function getMatchedYoutubeCoachItem() {
      var title = (getProblemTitle() || '') + ' ' + (document.body ? document.body.textContent.slice(0, 600) : '');
      var items = [
        { slug: '0001', title: '메넬라우스의 정리 (20단계 평행보조선 시각 증명)', ytKo: '7zD66SWWceg', ytEn: 'CjE2nyyzG2s', kw: '메넬라우스|비율|할선|외분|내분' },
        { slug: '0002', title: '체바의 정리 (17단계 삼각형 넓이 비 시각 증명)', ytKo: 'W_AWH-Gk89w', ytEn: 'ffNJhPRvh4Y', kw: '체바|무게중심|수심|내심|넓이 비' },
        { slug: '0003', title: '피타고라스 정리 (25단계 넓이 분할·전단 이동 증명)', ytKo: 'k6LBYa5SCiA', ytEn: 'n9zyKwXXsbA', kw: '피타고라스|직각삼각형|빗변|코사인|사인|거리' },
        { slug: '0004', title: '피타고라스 나무 (11단계 프랙탈 넓이 보존·등비급수)', ytKo: 'bQO7fnT6aDU', ytEn: '9JKLflqrtDU', kw: '등비|급수|수열|지수|거듭제곱|극한|프랙탈' },
        { slug: '0005', title: '종이띠로 접는 정칠각형 매듭 원리 (11단계 대칭 작도)', ytKo: 'Mq6s2JLV9mQ', ytEn: 'fXQJ8s1La-E', kw: '다각형|원|접선|각도|대칭' }
      ];
      for (var i = 0; i < items.length; i++) {
        if (new RegExp(items[i].kw).test(title)) return items[i];
      }
      return items[2];
    }

    function renderYoutubeCoachDrawer(customIdx, customLang) {
      var drawer = document.getElementById('acadDrawerYoutube');
      if (!drawer) return;
      var list = [
        { slug: '0003', title: '피타고라스 정리 (25단계 넓이 분할 증명)', ytKo: 'k6LBYa5SCiA', ytEn: 'n9zyKwXXsbA' },
        { slug: '0004', title: '피타고라스 나무 (11단계 넓이 보존·수열·지수)', ytKo: 'bQO7fnT6aDU', ytEn: '9JKLflqrtDU' },
        { slug: '0001', title: '메넬라우스의 정리 (20단계 평행보조선 증명)', ytKo: '7zD66SWWceg', ytEn: 'CjE2nyyzG2s' },
        { slug: '0002', title: '체바의 정리 (17단계 삼각형 넓이 비 증명)', ytKo: 'W_AWH-Gk89w', ytEn: 'ffNJhPRvh4Y' },
        { slug: '0005', title: '정칠각형 종이띠 매듭 (11단계 기하 작도)', ytKo: 'Mq6s2JLV9mQ', ytEn: 'fXQJ8s1La-E' }
      ];
      var matched = getMatchedYoutubeCoachItem();
      var selIdx = (typeof customIdx === 'number') ? customIdx : list.findIndex(function(x){ return x.slug === matched.slug; });
      if (selIdx < 0) selIdx = 0;
      var cur = list[selIdx];
      var lang = customLang || (isEnMode() ? 'en' : 'ko');
      var vidId = (lang === 'en') ? cur.ytEn : cur.ytKo;
      var isBoard = window.location.pathname.indexOf('/board/') !== -1 || window.location.pathname.indexOf('/offline/') !== -1;
      var boardHref = (isBoard ? '../video_board.html' : 'video_board.html') + '?slug=' + cur.slug + '&from=quiz';
      var topicBtns = list.map(function(it, i) {
        var activeStyle = (i === selIdx) ? 'background:#e11d48;color:#fff;border-color:#e11d48' : 'background:#f8fafc;color:#334155;border-color:#cbd5e1';
        return '<button type="button" onclick="window.switchAcadYoutubeCoach(' + i + ', \'' + lang + '\')" style="padding:5px 10px;border-radius:8px;border:1px solid;font-size:0.75rem;font-weight:800;cursor:pointer;' + activeStyle + '">🎬 ' + it.title + '</button>';
      }).join('');
      drawer.innerHTML =
        '<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;margin-bottom:8px">' +
          '<div style="font-weight:900;color:#be123c;font-size:0.86rem">📺 @min7014_ai 유튜브 시각 증명 코치 × mathedu 양방향 학습 극장</div>' +
          '<div style="display:flex;gap:6px;flex-wrap:wrap">' +
            '<button type="button" onclick="window.switchAcadYoutubeCoach(' + selIdx + ', \'ko\')" style="padding:4px 10px;border-radius:999px;border:1px solid #e11d48;background:' + (lang==='ko'?'#e11d48':'#fff') + ';color:' + (lang==='ko'?'#fff':'#e11d48') + ';font-size:0.74rem;font-weight:800;cursor:pointer">🇰🇷 한국어 1080p</button>' +
            '<button type="button" onclick="window.switchAcadYoutubeCoach(' + selIdx + ', \'en\')" style="padding:4px 10px;border-radius:999px;border:1px solid #2563eb;background:' + (lang==='en'?'#2563eb':'#fff') + ';color:' + (lang==='en'?'#fff':'#2563eb') + ';font-size:0.74rem;font-weight:800;cursor:pointer">🇺🇸 English 1080p</button>' +
            '<a href="https://www.youtube.com/@min7014_ai?sub_confirmation=1" target="_blank" rel="noopener" style="padding:4px 10px;border-radius:999px;background:#0f172a;color:#fff;font-size:0.74rem;font-weight:800;text-decoration:none">🔔 @min7014_ai 구독 ↗</a>' +
            '<a href="' + boardHref + '" style="padding:4px 10px;border-radius:999px;background:#0284c7;color:#fff;font-size:0.74rem;font-weight:800;text-decoration:none">📋 1,113개 설명영상 게시판 ↗</a>' +
          '</div>' +
        '</div>' +
        '<div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px">' + topicBtns + '</div>' +
        '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px;align-items:center">' +
          '<div style="aspect-ratio:16/9;width:100%;background:#000;border-radius:10px;overflow:hidden;border:1.5px solid #fda4af">' +
            '<iframe src="https://www.youtube-nocookie.com/embed/' + vidId + '?rel=0" style="width:100%;height:100%;border:0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>' +
          '</div>' +
          '<div style="padding:12px;border-radius:10px;background:linear-gradient(135deg,#fff1f2 0%,#f0f9ff 100%);border:1px solid #fecdd3;font-size:0.8rem;line-height:1.6;color:#1e293b">' +
            '<div style="font-weight:900;color:#be123c;margin-bottom:4px">🚀 유튜브 영상 × 홈페이지 자생 성장 루프</div>' +
            '• <b>1단계 (유튜브 시각 직관)</b>: 보조선이 그어지고 도형이 이동하는 1080p 플립북 영상으로 공식 암기 없이 원리를 깨칩니다.<br>' +
            '• <b>2단계 (탈-5지선다 창의 구성)</b>: 깨달은 원리로 아래 디딤돌 단계에서 5지선다 찍기 없이 직접 식을 조립해 해결합니다.<br>' +
            '• <b>3단계 (친구 도전장 & 홍보 공유)</b>: 이 문제와 @min7014_ai 유튜브 설명영상을 카톡·단톡방에 공유해 친구와 함께 도전하세요!' +
            '<div style="margin-top:10px;display:flex;gap:6px;flex-wrap:wrap">' +
              '<button type="button" onclick="window.shareProblemWithYoutube()" style="padding:7px 13px;border-radius:8px;border:none;background:linear-gradient(135deg,#e11d48,#be123c);color:#fff;font-size:0.78rem;font-weight:900;cursor:pointer">📢 이 문제 + @min7014_ai 유튜브 영상 1초 공유 (+30 XP)</button>' +
            '</div>' +
          '</div>' +
        '</div>';
    }

    window.switchAcadYoutubeCoach = function(idx, lang) {
      renderYoutubeCoachDrawer(idx, lang);
    };

    window.shareProblemWithYoutube = function() {
      var matched = getMatchedYoutubeCoachItem();
      var probTitle = getProblemTitle();
      var shareUrl = window.location.href.split('#')[0];
      var msg = [
        '🔥 [민은기 선생님의 수학자료실 × @min7014_ai 시각 증명 & 탈-5지선다 창의 수학 도전장!]',
        '📌 도전 문항: ' + probTitle,
        '✍️ 5지선다 찍기 없이 스스로 수식을 조립해 푸는 창의 디딤돌 바로 도전:',
        '👉 ' + shareUrl,
        '',
        '🎬 연관 시각적 수학 증명 1080p 유튜브 (@min7014_ai - ' + matched.title + '):',
        '👉 https://youtu.be/' + matched.ytKo,
        '📋 전체 1,113개 수학 설명영상 게시판: https://min7014.github.io/mathedu/video_board.html'
      ].join('\n');
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(msg).catch(function(){});
      }
      if (window.MatheduGame && window.MatheduGame.addXP) {
        window.MatheduGame.addXP(30, '📢 유튜브 영상 + 수학 문제 홍보 공유');
      }
      alert('📢 [유튜브 설명영상 + 현재 수학 문제] 단톡방·SNS 홍보 카드가 클립보드에 복사되었습니다! (+30 XP)\n\n' + msg);
    };

    window.toggleAcadDrawer = function(which) {
      var map = {
        cpa: { id: 'acadDrawerCpa', btn: 'btnAcadCpa', init: function() { renderCpaDrawer('iconic'); } },
        scratch: { id: 'acadDrawerScratch', btn: 'btnAcadScratch', init: renderScratchDrawer },
        metacog: { id: 'acadDrawerMetacog', btn: 'btnAcadMetacog', init: renderMetacogDrawer },
        variation: { id: 'acadDrawerVariation', btn: 'btnAcadVariation', init: renderVariationDrawer },
        youtube: { id: 'acadDrawerYoutube', btn: 'btnAcadYoutube', init: function() { renderYoutubeCoachDrawer(); } }
      };
      var item = map[which];
      if (!item) return;
      var el = document.getElementById(item.id);
      var btn = document.getElementById(item.btn);
      if (!el) return;
      var isOpen = el.classList.contains('open');
      ['acadDrawerCpa', 'acadDrawerScratch', 'acadDrawerMetacog', 'acadDrawerVariation', 'acadDrawerYoutube'].forEach(function(id) {
        var d = document.getElementById(id);
        if (d) d.classList.remove('open');
      });
      ['btnAcadCpa', 'btnAcadScratch', 'btnAcadMetacog', 'btnAcadVariation', 'btnAcadYoutube'].forEach(function(bid) {
        var b = document.getElementById(bid);
        if (b) b.classList.remove('active');
      });
      if (!isOpen) {
        item.init();
        el.classList.add('open');
        if (btn) btn.classList.add('active');
        var st = loadPedagogyState();
        if (which === 'cpa') st.cpaCount = (st.cpaCount || 0) + 1;
        if (which === 'scratch') st.scratchpadUsed = (st.scratchpadUsed || 0) + 1;
        savePedagogyState(st);
      }
    };

    // 5. ✍️ 탈-5지선다 창의적 구성주의 수학 풀이 엔진 (Creativity-First Constructive Math Solving Engine v2.0)
    //    - 기본값(Default): 5지선다 객관식 보기(①~⑤)를 숨기고, 학생이 직접 발상(보조선)을 세운 뒤
    //      수식 레고 블록 조립 또는 직접 수식/수치 입력으로 답을 구성하도록 유도하여 수학적 창의성을 극대화합니다.
    function isCreativeConstructiveModeOn() {
      try {
        var saved = localStorage.getItem('mathedu_creative_mode_v2');
        if (saved === 'off') return false;
        return true; // 기본 ON (5지선다 찍기 방지 & 창의적 구성주의 기본 적용)
      } catch (e) {
        return true;
      }
    }

    function setCreativeConstructiveMode(on) {
      try {
        localStorage.setItem('mathedu_creative_mode_v2', on ? 'on' : 'off');
      } catch (e) {}
    }

    function stripHtmlAndSpanN(rawHtml) {
      var s = String(rawHtml || '').replace(/<span class="n">\s*\d+\s*<\/span>/gi, '');
      s = s.replace(/<[^>]+>/g, ' ');
      s = s.replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"');
      return s.trim();
    }

    function extractPureOptionHtml(optEl) {
      if (!optEl) return '';
      var clone = optEl.cloneNode(true);
      var nSpan = clone.querySelector('.n');
      if (nSpan) nSpan.remove();
      var mjxList = clone.querySelectorAll('mjx-container');
      if (mjxList.length > 0 && optEl.dataset && optEl.dataset.rawTex) {
        return optEl.dataset.rawTex;
      }
      return clone.innerHTML.trim();
    }

    function normalizeMathExpr(str) {
      var s = String(str || '').trim();
      if (!s) return '';
      s = s.replace(/\$/g, '');
      s = s.replace(/^=\s*/, '');
      s = s.replace(/\\(?:displaystyle|textstyle|left|right|Big|big|quad|qquad|,|;|:|!)/g, '');
      s = s.replace(/\\(?:d|t)?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}/g, '(($1)/($2))');
      s = s.replace(/\\(?:d|t)?frac\s*([0-9a-zA-Z])\s*([0-9a-zA-Z])/g, '(($1)/($2))');
      s = s.replace(/\\sqrt\s*\{([^{}]*)\}/g, 'sqrt($1)');
      s = s.replace(/\\sqrt\s*([0-9a-zA-Z]+)/g, 'sqrt($1)');
      s = s.replace(/루트\s*\(?([0-9a-zA-Z]+)\)?/g, 'sqrt($1)');
      s = s.replace(/√\s*\(?([0-9a-zA-Z]+)\)?/g, 'sqrt($1)');
      s = s.replace(/([0-9]+)\s*분의\s*([0-9]+)/g, '(($2)/($1))');
      s = s.replace(/\\times|×|\\cdot|·/g, '*');
      s = s.replace(/\\div|÷/g, '/');
      s = s.replace(/\\pi|파이|π/g, 'pi');
      s = s.replace(/\^\{\\circ\}|\^\\circ|°|도|가지|개|번/g, '');
      s = s.replace(/\^\{([^{}]+)\}/g, '^($1)');
      s = s.replace(/_\{([^{}]+)\}/g, '_$1');
      s = s.replace(/[{}]/g, '');
      s = s.replace(/\s+/g, '');
      return s.toLowerCase();
    }

    function tryEvalMathNumber(normStr) {
      if (!normStr) return NaN;
      var s = normStr;
      s = s.replace(/([0-9])\s*(sqrt|pi|\()/g, '$1*$2');
      s = s.replace(/(\))\s*([0-9a-zA-Z(])/g, '$1*$2');
      s = s.replace(/sqrt\(([^()]+)\)/g, 'Math.sqrt($1)');
      s = s.replace(/pi/g, 'Math.PI');
      s = s.replace(/\^/g, '**');
      if (!/^[0-9+\-*/().\sMathsqrtPI*]+$/.test(s)) return NaN;
      try {
        var v = Function('"use strict";return (' + s + ')')();
        return (typeof v === 'number' && isFinite(v)) ? v : NaN;
      } catch (e) {
        return NaN;
      }
    }

    function checkCreativeMathEquivalence(userInput, correctRaw, allOptsRaw) {
      var uRaw = String(userInput || '').trim();
      if (!uRaw) return { ok: false, reason: 'empty' };

      var cClean = stripHtmlAndSpanN(correctRaw);
      var uNorm = normalizeMathExpr(uRaw);
      var cNorm = normalizeMathExpr(cClean);

      if (uNorm && cNorm && uNorm === cNorm) {
        return { ok: true, mode: 'exact_symbolic' };
      }

      // Check if correctRaw contains multi-step '=' like '= 3^0 = 1'
      var eqParts = cClean.split('=').map(function(p) { return p.trim(); }).filter(Boolean);
      for (var i = 0; i < eqParts.length; i++) {
        var pNorm = normalizeMathExpr(eqParts[i]);
        if (pNorm && uNorm === pNorm) {
          return { ok: true, mode: 'step_equation_match' };
        }
        var uValPart = tryEvalMathNumber(uNorm);
        var pValPart = tryEvalMathNumber(pNorm);
        if (!isNaN(uValPart) && !isNaN(pValPart) && Math.abs(uValPart - pValPart) < 1e-6) {
          return { ok: true, mode: 'numeric_equivalence' };
        }
      }

      var uVal = tryEvalMathNumber(uNorm);
      var cVal = tryEvalMathNumber(cNorm);
      if (!isNaN(uVal) && !isNaN(cVal) && Math.abs(uVal - cVal) < 1e-6) {
        return { ok: true, mode: 'numeric_equivalence' };
      }

      // Check without parentheses for simple expressions like 3^(1/2)*3^(-1/2)
      var uFlat = uNorm.replace(/[()]/g, '');
      var cFlat = cNorm.replace(/[()]/g, '');
      if (uFlat && cFlat && uFlat === cFlat) {
        return { ok: true, mode: 'structural_equivalence' };
      }

      // Partial insight analysis for Socratic Coaching
      var matchedTokens = [];
      var numMatches = cClean.match(/[0-9]+|[a-zA-Z]+/g) || [];
      numMatches.forEach(function(tok) {
        if (tok && uRaw.indexOf(tok) !== -1 && matchedTokens.indexOf(tok) === -1) {
          matchedTokens.push(tok);
        }
      });

      // Check if user accidentally typed another option's value
      var matchedWrongOpt = -1;
      if (Array.isArray(allOptsRaw)) {
        for (var j = 0; j < allOptsRaw.length; j++) {
          var oNorm = normalizeMathExpr(stripHtmlAndSpanN(allOptsRaw[j]));
          if (oNorm && oNorm !== cNorm && uNorm === oNorm) {
            matchedWrongOpt = j + 1;
            break;
          }
        }
      }

      return {
        ok: false,
        matchedTokens: matchedTokens,
        matchedWrongOpt: matchedWrongOpt,
        uVal: uVal,
        cVal: cVal
      };
    }

    function buildCreativeLegoTokens(correctRaw, allOptsRaw, seedIdx) {
      var cleanAns = stripHtmlAndSpanN(correctRaw).replace(/^\$|\$$/g, '').trim();
      var tokens = [];

      // Split expression into meaningful constructive chunks
      var parts = cleanAns.split(/(\s*\\times\s*|\s*\+\s*|\s*-\s*|\s*=\s*)/).map(function(s) { return s.trim(); }).filter(Boolean);
      if (parts.length >= 2 && parts.length <= 6) {
        parts.forEach(function(p) {
          tokens.push({ display: '$' + p + '$', insert: p, isTruePart: true });
        });
      } else {
        tokens.push({ display: correctRaw, insert: cleanAns, isTruePart: true });
      }

      // Add distractor building blocks from other options so student must actively reason & construct
      if (Array.isArray(allOptsRaw)) {
        allOptsRaw.forEach(function(oRaw, j) {
          var oClean = stripHtmlAndSpanN(oRaw).replace(/^\$|\$$/g, '').trim();
          if (!oClean || oClean === cleanAns) return;
          var oParts = oClean.split(/(\s*\\times\s*|\s*\+\s*|\s*-\s*|\s*=\s*)/).map(function(s) { return s.trim(); }).filter(Boolean);
          if (oParts.length >= 2 && parts.length >= 2) {
            oParts.forEach(function(op) {
              if (!tokens.some(function(t) { return t.insert === op; }) && tokens.length < 7) {
                tokens.push({ display: '$' + op + '$', insert: op, isTruePart: false });
              }
            });
          } else if (!tokens.some(function(t) { return t.insert === oClean; }) && tokens.length < 6) {
            tokens.push({ display: oRaw, insert: oClean, isTruePart: false });
          }
        });
      }

      // Deterministic shuffle based on seedIdx + string length
      var out = tokens.slice();
      for (var i = out.length - 1; i > 0; i--) {
        var k = (i * 7 + (seedIdx + 3) * 13 + cleanAns.length) % (i + 1);
        var tmp = out[i];
        out[i] = out[k];
        out[k] = tmp;
      }
      return out;
    }

    function getCreativeHeuristicsForStem(stemText) {
      var s = String(stemText || '');
      if (/지수|거듭제곱|로그|\log/.test(s)) {
        return ['🔍 밑(Base)을 소수로 통일하기', '📐 분수·음수 지수로 변환하기', '🧪 작은 정수 대입해 규칙 확인', '🔗 앞 단계 결과식 대입하기'];
      }
      if (/삼각|sin|cos|tan|원|접선|타원|포물선|쌍곡선|벡터|넓이/.test(s)) {
        return ['📐 원의 중심·초점과 교점 잇기(보조선)', '🔍 직각삼각형·피타고라스 관계 찾기', '🧭 단위원 대칭성·주기성 활용', '🔗 사인·코사인법칙 관계식 세우기'];
      }
      if (/수열|등차|등비|시그마|\sum|귀납/.test(s)) {
        return ['🧪 n=1, 2, 3 차례대로 대입해 나열하기', '🔍 이웃한 두 항의 차(공차)·비(공비) 관찰', '🧱 부분분수·연쇄 상쇄 구조 만들기', '🔗 일반항 a_n과 합 S_n 관계식 세우기'];
      }
      if (/극한|연속|미분|도함수|접선|극대|극소|적분|\int|\lim/.test(s)) {
        return ['🔍 0/0 꼴 공통인수 약분·인수분해', '📐 접점의 x좌표를 미지수 t로 설정', '📊 도함수 f′(x)=0 부호 변화 관찰', '🧭 그래프 대칭성·정적분 넓이 해석'];
      }
      if (/경우의 수|확률|조합|순열|정규분포|통계|독립|조건부/.test(s)) {
        return ['🗂️ 빠짐없이 중복 없이 케이스 분류', '🔄 여사건(1 - 반대 확률) 활용하기', '📐 조건부확률 분모(표본공간) 축소', '📊 표준화(Z) 및 대칭 넓이 활용'];
      }
      return ['🧪 작은 숫자(1, 2)를 먼저 대입해 관찰', '🔍 구하려는 목표값을 미지수로 설정', '📐 주어진 조건을 등식·도형으로 번역', '🧱 앞 단계에서 구한 조각 결합하기'];
    }

    function applyOrigPaperCreativeMask() {
      var origOpts = document.getElementById('examOrigOptsContent');
      if (!origOpts) return;
      var creativeOn = isCreativeConstructiveModeOn();
      var mask = document.getElementById('examOrigCreativeBanner');
      if (!creativeOn || origOpts.dataset.origRevealed === '1') {
        origOpts.style.display = '';
        if (mask) mask.remove();
        return;
      }
      origOpts.style.display = 'none';
      if (!mask) {
        mask = document.createElement('div');
        mask.id = 'examOrigCreativeBanner';
        mask.style.cssText = 'margin-top:10px;padding:10px 14px;border-radius:10px;background:linear-gradient(135deg,#f0fdf4 0%,#eff6ff 100%);border:1.5px dashed #059669;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;font-size:0.82rem;color:#065f46;font-weight:700';
        mask.innerHTML =
          '<span>✍️ <b>[탈-5지선다 창의적 구성 모드]</b>: 객관식 보기에 의존하지 않고 스스로 식을 세워 풀어보세요!</span>' +
          '<button type="button" onclick="var el=document.getElementById(\'examOrigOptsContent\');if(el){el.dataset.origRevealed=\'1\';el.style.display=\'\';}this.parentElement.remove();" style="padding:4px 10px;border-radius:999px;border:1px solid #059669;background:#ffffff;color:#047857;font-size:0.75rem;font-weight:800;cursor:pointer">👁️ 원본 5지선다 보기 대조</button>';
        origOpts.parentNode.insertBefore(mask, origOpts);
      }
    }

    function applyRetrievalBlindMode() {
      qs = Array.from(document.querySelectorAll('.q'));
      var creativeOn = isCreativeConstructiveModeOn();
      var btn = document.getElementById('btnAcadRetrieval');
      if (btn) {
        btn.classList.toggle('active', creativeOn);
        btn.innerHTML = bilingual(
          '✍️ 탈-5지선다 창의 구성 모드 ' + (creativeOn ? 'ON (기본)' : 'OFF (5지선다)'),
          '✍️ Creative Constructive Mode ' + (creativeOn ? 'ON' : 'OFF')
        );
      }
      applyOrigPaperCreativeMask();

      qs.forEach(function(q, idx) {
        var opts = q.querySelector('.opts');
        if (!opts) return;
        var optEls = Array.from(opts.querySelectorAll('.opt'));
        optEls.forEach(function(oEl) {
          if (!oEl.dataset.rawTex) {
            oEl.dataset.rawTex = oEl.innerHTML.replace(/<span class="n">\s*\d+\s*<\/span>/i, '').trim();
          }
        });

        var studioId = 'acadCreativeStudio_' + idx;
        var existingStudio = document.getElementById(studioId);

        if (!creativeOn) {
          opts.style.display = '';
          if (existingStudio) existingStudio.style.display = 'none';
          return;
        }

        if (q.classList.contains('done') || q.dataset.retrievalRevealed === '1') {
          opts.style.display = '';
          if (existingStudio) existingStudio.style.display = 'block';
          return;
        }

        // Hide passive 5-choice options by default!
        opts.style.display = 'none';

        if (existingStudio) {
          existingStudio.style.display = 'block';
          return;
        }

        var ansNum = +(q.dataset.ans || 1);
        var correctOptEl = optEls[ansNum - 1] || optEls[0];
        var correctRaw = correctOptEl ? (correctOptEl.dataset.rawTex || extractPureOptionHtml(correctOptEl)) : '';
        var allOptsRaw = optEls.map(function(oEl) { return oEl.dataset.rawTex || extractPureOptionHtml(oEl); });
        var stemEl = q.querySelector('.stem');
        var stemText = stemEl ? stemEl.textContent : '';
        var heuristics = getCreativeHeuristicsForStem(stemText);
        var legoTokens = buildCreativeLegoTokens(correctRaw, allOptsRaw, idx);

        var studio = document.createElement('div');
        studio.id = studioId;
        studio.className = 'acad-creative-studio';
        studio.style.cssText = 'margin-top:12px;padding:16px;border-radius:14px;background:linear-gradient(145deg,#ffffff 0%,#f0f9ff 55%,#f0fdf4 100%);border:1.5px solid #38bdf8;box-shadow:0 6px 20px rgba(0,99,152,0.08);text-align:left;';

        var heurButtonsHtml = heuristics.map(function(h) {
          return '<button type="button" class="creative-heur-chip" onclick="window.selectCreativeHeuristic(' + idx + ', this)" style="padding:5px 11px;border-radius:999px;border:1px solid #bae6fd;background:#ffffff;color:#0369a1;font-size:0.76rem;font-weight:700;cursor:pointer;transition:0.15s">' + h + '</button>';
        }).join('');

        var legoButtonsHtml = legoTokens.map(function(t) {
          var safeInsert = String(t.insert || '').replace(/\\/g, '\\\\').replace(/'/g, "\\'");
          return '<button type="button" class="creative-lego-chip" onclick="window.appendCreativeLegoToken(' + idx + ', \'' + safeInsert + '\')" style="padding:6px 12px;border-radius:10px;border:1.5px solid #c7d2fe;background:#ffffff;color:#1e293b;font-size:0.84rem;font-weight:800;cursor:pointer;box-shadow:0 2px 6px rgba(79,70,229,0.08);transition:transform 0.12s">' + t.display + '</button>';
        }).join('');

        var symQuickList = [
          { lbl: '분수 a/b', val: '/' },
          { lbl: '√(루트)', val: 'sqrt(' },
          { lbl: '^ ( 거듭제곱 )', val: '^' },
          { lbl: '×', val: '*' },
          { lbl: '+', val: '+' },
          { lbl: '-', val: '-' },
          { lbl: '=', val: '=' },
          { lbl: '(', val: '(' },
          { lbl: ')', val: ')' },
          { lbl: 'π', val: 'pi' }
        ];
        var symQuickHtml = symQuickList.map(function(sym) {
          return '<button type="button" onclick="window.appendCreativeLegoToken(' + idx + ', \'' + sym.val + '\')" style="padding:3px 9px;border-radius:6px;border:1px solid #cbd5e1;background:#f8fafc;color:#334155;font-size:0.74rem;font-weight:800;cursor:pointer">' + sym.lbl + '</button>';
        }).join('');

        studio.innerHTML =
          '<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;margin-bottom:10px;padding-bottom:8px;border-bottom:1px dashed #bae6fd">' +
            '<div style="display:flex;align-items:center;gap:6px;font-size:0.84rem;font-weight:900;color:#006398">' +
              '<span>✍️</span>' +
              bilingual('탈-5지선다 창의적 구성주의 풀이 스튜디오 (스스로 발상·수식 조립)', 'Creativity-First Constructive Math Studio (No Multiple-Choice Guessing)') +
            '</div>' +
            '<div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap">' +
              '<button type="button" onclick="window.toggleCreativeWhatIfLab(' + idx + ')" style="padding:4px 10px;border-radius:999px;border:1px solid #c084fc;background:#faf5ff;color:#6b21a8;font-size:0.74rem;font-weight:800;cursor:pointer">' +
                bilingual('🔀 조건 바꿔 새 문제 발명 (What-If)', '🔀 What-If Problem Posing Lab') +
              '</button>' +
              '<button type="button" onclick="window.revealAcadRetrievalStep(' + idx + ')" style="padding:4px 10px;border-radius:999px;border:1px solid #cbd5e1;background:#ffffff;color:#475569;font-size:0.74rem;font-weight:700;cursor:pointer">' +
                bilingual('👁️ 막힐 때 5지선다 보기 열기', '👁️ Reveal 5 Choices') +
              '</button>' +
            '</div>' +
          '</div>' +

          // Step A: Creative Idea & Auxiliary-Line Sketcher
          '<div style="margin-bottom:10px;padding:10px 12px;border-radius:10px;background:rgba(255,255,255,0.85);border:1px solid #e0f2fe">' +
            '<div style="font-size:0.77rem;font-weight:800;color:#0369a1;margin-bottom:6px">' +
              bilingual('🧭 [1단계 · 나만의 제1발상 & 보조선 설계]: 계산하기 전에 어떤 수학적 아이디어로 접근할지 선택하거나 적어보세요!', '🧭 [Step 1 · Creative Strategy Sketch]: Choose or write your mathematical approach before computing!') +
            '</div>' +
            '<div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:6px">' + heurButtonsHtml + '</div>' +
            '<input type="text" id="creativeIdeaInput_' + idx + '" placeholder="💭 나만의 풀이 발상·보조선·규칙을 자유롭게 한 줄로 스케치해 보세요 (선택 사항)" style="width:100%;padding:6px 10px;border-radius:8px;border:1px solid #cbd5e1;background:#ffffff;color:#1e293b;font-size:0.78rem;box-sizing:border-box">' +
          '</div>' +

          // Step B: Constructive Math Lego Blocks & Direct Expression Input
          '<div style="padding:10px 12px;border-radius:10px;background:rgba(255,255,255,0.92);border:1px solid #c7d2fe">' +
            '<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:6px;margin-bottom:6px">' +
              '<span style="font-size:0.78rem;font-weight:800;color:#3730a3">' +
                bilingual('🧩 [2단계 · 수식 레고 블록 조립 또는 직접 입력]: 아래 수식 조각을 클릭해 조립하거나 키보드로 답을 직접 구성하세요!', '🧩 [Step 2 · Assemble Math Blocks or Type Directly]: Click math blocks below or type your answer!') +
              '</span>' +
              '<span style="font-size:0.72rem;color:#059669;font-weight:800">🌟 선지 안 보고 해결 시 +30 창의력 XP</span>' +
            '</div>' +
            '<div id="creativeLegoTray_' + idx + '" style="display:flex;gap:7px;flex-wrap:wrap;align-items:center;margin-bottom:8px;padding:8px;border-radius:8px;background:#f5f3ff;border:1px dashed #a5b4fc">' +
              '<span style="font-size:0.73rem;font-weight:800;color:#4f46e5;margin-right:2px">🧩 수식 블록:</span>' +
              legoButtonsHtml +
            '</div>' +
            '<div style="display:flex;gap:5px;flex-wrap:wrap;align-items:center;margin-bottom:8px">' +
              '<span style="font-size:0.72rem;font-weight:700;color:#64748b">⌨️ 기호 패드:</span>' +
              symQuickHtml +
            '</div>' +
            '<div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap">' +
              '<input type="text" id="creativeAnsInput_' + idx + '" onkeydown="if(event.key===\'Enter\')window.submitCreativeConstructiveAns(' + idx + ')" placeholder="정답 값 또는 조립한 수식을 입력하세요 (예: 2, 1/3, 루트3, (3^2)^(1/4)*3^(-1/2) 등)" style="flex:1;min-width:200px;padding:9px 12px;border-radius:10px;border:1.5px solid #6366f1;background:#ffffff;color:#0f172a;font-size:0.88rem;font-weight:800;outline:none;box-sizing:border-box">' +
              '<button type="button" onclick="window.clearCreativeConstructiveAns(' + idx + ')" style="padding:9px 11px;border-radius:10px;border:1px solid #cbd5e1;background:#f8fafc;color:#475569;font-size:0.78rem;font-weight:800;cursor:pointer" title="입력 초기화">🔄 지우기</button>' +
              '<button type="button" onclick="window.submitCreativeConstructiveAns(' + idx + ')" style="padding:9px 16px;border-radius:10px;border:none;background:linear-gradient(135deg,#006398 0%,#4f46e5 100%);color:#ffffff;font-size:0.84rem;font-weight:900;cursor:pointer;box-shadow:0 4px 12px rgba(79,70,229,0.28)">' +
                bilingual('✨ 창의 답안 제출 · 검증', '✨ Submit Answer') +
              '</button>' +
            '</div>' +
            '<div id="creativeFeedbackBox_' + idx + '" style="display:none;margin-top:8px;padding:10px 12px;border-radius:10px;font-size:0.81rem;line-height:1.55"></div>' +
          '</div>' +

          // Step C: Brown & Walter What-If-Not Creative Problem Posing Lab
          '<div id="creativeWhatIfLab_' + idx + '" style="display:none;margin-top:10px;padding:12px;border-radius:10px;background:linear-gradient(135deg,#faf5ff 0%,#fdf2f8 100%);border:1.5px solid #d8b4fe">' +
            '<div style="font-size:0.8rem;font-weight:900;color:#6b21a8;margin-bottom:4px">' +
              bilingual('🔀 [브라운 & 월터(Brown & Walter) What-If-Not 창의적 문제 변형·발명 실험실]', '🔀 [Brown & Walter What-If-Not Creative Problem Posing Lab]') +
            '</div>' +
            '<div style="font-size:0.76rem;color:#581c87;margin-bottom:8px;line-height:1.5">' +
              bilingual(
                '진짜 수학적 창의성은 주어진 문제를 푸는 것을 넘어 <b>"만약 문제의 숫자·지수·각도·조건을 바꾼다면 답이 어떻게 달라질까?"</b>를 스스로 질문하고 새 문제를 발명할 때 폭발합니다!',
                'True mathematical creativity shines when you ask "What if this condition changes?" and invent your own variation!'
              ) +
            '</div>' +
            '<div style="display:flex;gap:6px;flex-wrap:wrap">' +
              '<input type="text" id="creativeWhatIfInput_' + idx + '" placeholder="예: 만약 밑 9를 27로 바꾸거나 지수 부호를 반대로 바꾸면 새로운 답은 얼마가 될까? (나만의 변형 문제 & 답 기록)" style="flex:1;min-width:220px;padding:7px 10px;border-radius:8px;border:1px solid #c084fc;background:#ffffff;color:#1e293b;font-size:0.78rem">' +
              '<button type="button" onclick="window.saveCreativeWhatIfProblem(' + idx + ')" style="padding:7px 13px;border-radius:8px;border:none;background:#7e22ce;color:#ffffff;font-size:0.76rem;font-weight:800;cursor:pointer">💾 나만의 발명 문제 저장 (+25 XP)</button>' +
            '</div>' +
            '<div id="creativeWhatIfSaved_' + idx + '" style="font-size:0.74rem;color:#059669;font-weight:800;margin-top:5px"></div>' +
          '</div>';

        opts.parentNode.insertBefore(studio, opts);
        if (window.MathJax && window.MathJax.typesetPromise) {
          window.MathJax.typesetPromise([studio]).catch(function() {});
        }
      });
    }

    window.selectCreativeHeuristic = function(idx, btnEl) {
      if (!btnEl) return;
      var parent = btnEl.parentNode;
      if (parent) {
        parent.querySelectorAll('.creative-heur-chip').forEach(function(b) {
          b.style.background = '#ffffff';
          b.style.color = '#0369a1';
          b.style.borderColor = '#bae6fd';
        });
      }
      btnEl.style.background = '#0284c7';
      btnEl.style.color = '#ffffff';
      btnEl.style.borderColor = '#0284c7';
      var ideaInp = document.getElementById('creativeIdeaInput_' + idx);
      if (ideaInp && !ideaInp.value) {
        ideaInp.value = '나의 제1발상: ' + btnEl.textContent.trim();
      }
      if (window.MatheduGame && window.MatheduGame.addXP && !btnEl.dataset.xpAwarded) {
        btnEl.dataset.xpAwarded = '1';
        window.MatheduGame.addXP(10, '🧭 창의적 제1발상·보조선 설계');
      }
    };

    window.appendCreativeLegoToken = function(idx, tokenStr) {
      var inp = document.getElementById('creativeAnsInput_' + idx);
      if (!inp) return;
      var cur = inp.value || '';
      if (cur && !/[+\-*/^=(]$/.test(cur) && !/^[+\-*/^=)]/.test(tokenStr)) {
        inp.value = cur + ' ' + tokenStr;
      } else {
        inp.value = cur + tokenStr;
      }
      inp.focus();
    };

    window.clearCreativeConstructiveAns = function(idx) {
      var inp = document.getElementById('creativeAnsInput_' + idx);
      if (inp) {
        inp.value = '';
        inp.focus();
      }
      var fb = document.getElementById('creativeFeedbackBox_' + idx);
      if (fb) fb.style.display = 'none';
    };

    window.toggleCreativeWhatIfLab = function(idx) {
      var lab = document.getElementById('creativeWhatIfLab_' + idx);
      if (!lab) return;
      lab.style.display = (lab.style.display === 'none' || !lab.style.display) ? 'block' : 'none';
    };

    window.saveCreativeWhatIfProblem = function(idx) {
      var inp = document.getElementById('creativeWhatIfInput_' + idx);
      var msgEl = document.getElementById('creativeWhatIfSaved_' + idx);
      if (!inp || !inp.value.trim()) return;
      try {
        var list = JSON.parse(localStorage.getItem('mathedu_invented_problems_v1') || '[]');
        list.unshift({
          slug: currentSlug,
          title: getProblemTitle(),
          step: idx + 1,
          invented: inp.value.trim(),
          createdAt: new Date().toISOString()
        });
        if (list.length > 100) list = list.slice(0, 100);
        localStorage.setItem('mathedu_invented_problems_v1', JSON.stringify(list));
        if (msgEl) msgEl.textContent = '✅ 내가 발명한 창의 변형 문제가 포트폴리오에 저장되었습니다! (+25 창의력 XP)';
        if (window.MatheduGame && window.MatheduGame.addXP) {
          window.MatheduGame.addXP(25, '🔀 What-If 창의적 변형 문제 발명');
        }
      } catch (e) {}
    };

    window.submitCreativeConstructiveAns = function(idx) {
      qs = Array.from(document.querySelectorAll('.q'));
      var q = qs[idx];
      if (!q) return;
      var inp = document.getElementById('creativeAnsInput_' + idx);
      var fb = document.getElementById('creativeFeedbackBox_' + idx);
      if (!inp || !fb) return;

      var userVal = (inp.value || '').trim();
      if (!userVal) {
        fb.style.display = 'block';
        fb.style.background = '#fefce8';
        fb.style.border = '1px solid #fde047';
        fb.style.color = '#713f12';
        fb.innerHTML = '✍️ 먼저 생각한 값이나 수식을 입력하거나, 위의 <b>🧩 수식 블록</b>을 클릭해 조립해 보세요!';
        return;
      }

      var opts = q.querySelectorAll('.opt');
      var ansNum = +(q.dataset.ans || 1);
      var correctOpt = opts[ansNum - 1] || opts[0];
      var correctRaw = correctOpt ? (correctOpt.dataset.rawTex || extractPureOptionHtml(correctOpt)) : '';
      var allOptsRaw = Array.from(opts).map(function(o) { return o.dataset.rawTex || extractPureOptionHtml(o); });

      var res = checkCreativeMathEquivalence(userVal, correctRaw, allOptsRaw);
      if (res.ok) {
        fb.style.display = 'block';
        fb.style.background = '#ecfdf5';
        fb.style.border = '1.5px solid #10b981';
        fb.style.color = '#065f46';
        fb.innerHTML =
          '🌟 <b>[탈-5지선다 창의적 자력 구성 성공!]</b> 객관식 보기에 의존하지 않고 스스로 <b>' + correctRaw + '</b>을(를) 완벽하게 구성하여 도출했습니다! (+30 창의력 XP)<br>' +
          '<span style="font-size:0.76rem;color:#047857">💡 이제 아래 열린 <b>🔀 What-If 조건 변형 실험실</b>에서 조건을 살짝 바꿔 나만의 새 문제도 발명해 보세요!</span>';

        var st = loadPedagogyState();
        st.retrievalSuccess = (st.retrievalSuccess || 0) + 1;
        savePedagogyState(st);
        if (window.MatheduGame && window.MatheduGame.addXP) {
          window.MatheduGame.addXP(30, '🌟 탈-5지선다 창의적 자력 구성 해결');
        }

        // Trigger the underlying correct option click so score, progress bar, explanation, and next-step unlock all fire seamlessly!
        q.dataset.retrievalRevealed = '1';
        opts.forEach(function(o) { o.style.display = ''; });
        if (correctOpt && !q.classList.contains('done')) {
          correctOpt.click();
        }
        var whatIfLab = document.getElementById('creativeWhatIfLab_' + idx);
        if (whatIfLab) whatIfLab.style.display = 'block';
        if (window.MathJax && window.MathJax.typesetPromise) {
          window.MathJax.typesetPromise([fb]).catch(function() {});
        }
      } else {
        // Socratic Partial-Insight Coaching (never locks out on constructive attempts!)
        fb.style.display = 'block';
        fb.style.background = '#fffbeb';
        fb.style.border = '1.5px solid #f59e0b';
        fb.style.color = '#92400e';
        var partialMsg = '';
        if (res.matchedTokens && res.matchedTokens.length > 0) {
          partialMsg = '입력하신 식에서 핵심 요소(<b>' + res.matchedTokens.join(', ') + '</b>)를 정확히 포착했습니다! ';
        }
        if (res.matchedWrongOpt > 0) {
          partialMsg += '다만 흔히 범하기 쉬운 함정 값(부호·지수·계수 착오)에 해당합니다. ';
        }
        fb.innerHTML =
          '🧭 <b>[소크라테스식 창의 발문 코칭 · 재도전 가능]</b><br>' +
          partialMsg +
          '최종 부호(`+`/`-`), 지수 결합, 또는 약분 결과를 한 번만 더 점검해 볼까요?<br>' +
          '<span style="font-size:0.75rem;color:#b45309">💡 팁: 위의 <b>🧩 수식 블록</b>을 조합해 보거나, 아래 <b>🪜 ZPD 단계 힌트</b>를 열어 스스로 완성해 보세요!</span>';
      }
    };

    window.toggleAcadRetrievalMode = function() {
      var nextOn = !isCreativeConstructiveModeOn();
      setCreativeConstructiveMode(nextOn);
      var st = loadPedagogyState();
      st.retrievalBlindMode = nextOn;
      savePedagogyState(st);
      applyRetrievalBlindMode();
    };

    window.revealAcadRetrievalStep = function(idx) {
      qs = Array.from(document.querySelectorAll('.q'));
      var q = qs[idx];
      if (!q) return;
      q.dataset.retrievalRevealed = '1';
      var st = loadPedagogyState();
      st.retrievalSuccess = (st.retrievalSuccess || 0) + 1;
      savePedagogyState(st);
      applyRetrievalBlindMode();
    };

    window.MatheduCreativeSolver = {
      refreshAll: function() {
        applyRetrievalBlindMode();
      },
      isCreativeOn: isCreativeConstructiveModeOn
    };

    applyRetrievalBlindMode();

    // 6. 각 단계(.q)별 ZPD 3단계 점진적 힌트 사다리 & Hattie/Freudenthal 정교한 오개념 진단 피드백 장착
    qs.forEach(function(q, idx) {
      if (q.dataset.acadBound === '1') return;
      q.dataset.acadBound = '1';

      var actions = q.querySelector('.q-actions');
      var expEl = q.querySelector('.exp');
      var knowEl = q.previousElementSibling && q.previousElementSibling.classList.contains('know') ? q.previousElementSibling : null;

      // ZPD 힌트 박스 및 버튼 추가
      if (actions) {
        var hintBox = document.createElement('div');
        hintBox.className = 'acad-hint-box';
        hintBox.id = 'acadHintBox_' + idx;
        if (expEl && expEl.parentNode) {
          expEl.parentNode.insertBefore(hintBox, expEl);
        } else {
          q.appendChild(hintBox);
        }

        var hintBtn = document.createElement('button');
        hintBtn.type = 'button';
        hintBtn.className = 'acad-hint-btn';
        hintBtn.innerHTML = bilingual('🪜 ZPD 단계 힌트 (1/2)', '🪜 ZPD Step Hint (1/2)');
        hintBtn.onclick = function() {
          var level = parseInt(q.dataset.hintLevel || '0', 10) + 1;
          q.dataset.hintLevel = String(level);
          var st = loadPedagogyState();
          st.hintUsed = (st.hintUsed || 0) + 1;
          savePedagogyState(st);
          if (window.recordStepClinicWeakness) window.recordStepClinicWeakness(idx, 'hint');

          var prevQ = idx > 0 ? qs[idx - 1] : null;
          var prevAnsIdx = prevQ ? (+prevQ.dataset.ans - 1) : -1;
          var prevOpts = prevQ ? prevQ.querySelectorAll('.opt') : [];
          var prevAnsText = (prevOpts && prevOpts[prevAnsIdx]) ? prevOpts[prevAnsIdx].innerHTML.replace(/<span class="n">\d+<\/span>/, '') : '';

          var knowText = knowEl ? knowEl.innerHTML : '제0단계 수학 기호 번역기의 기본 공식을 먼저 확인하세요.';
          if (level === 1) {
            hintBox.innerHTML =
              '<b>🔍 [1차 비계 힌트 · 핵심 원리 및 발문 (Vygotsky ZPD)]</b><br>' +
              knowText +
              (prevAnsText ? '<div style="margin-top:6px;padding:6px 10px;background:#ffffff;border-radius:8px;border:1px solid #bae6fd">🔗 <b>앞 단계(' + idx + '단계)에서 구한 레고 조각</b>: ' + prevAnsText + '</div>' : '');
            hintBtn.innerHTML = bilingual('🧭 2차 결정적 식 힌트 (2/2)', '🧭 2nd Formula Bridge Hint (2/2)');
          } else {
            var rawExp = q.dataset.exp || '';
            hintBox.innerHTML =
              '<b>🧭 [2차 비계 힌트 · 수식 유도 브릿지 (Sweller Faded Example)]</b><br>' +
              rawExp;
            hintBtn.innerHTML = bilingual('✅ 힌트 모두 열림', '✅ All Hints Opened');
          }
          hintBox.classList.add('show');
          if (window.MathJax && window.MathJax.typesetPromise) {
            window.MathJax.typesetPromise([hintBox]).catch(function() {});
          }
        };
        actions.insertBefore(hintBtn, actions.firstChild);
      }

      // Hattie 정교한 오개념 진단 & Freudenthal 안내된 재발명 피드백
      var opts = q.querySelectorAll('.opt');
      var ansNum = +q.dataset.ans;
      opts.forEach(function(optEl, optIdx) {
        optEl.addEventListener('click', function() {
          setTimeout(function() {
            if (!expEl || expEl.querySelector('.acad-diag-box')) return;
            var chosenNum = optIdx + 1;
            var chosenTex = optEl.innerHTML.replace(/<span class="n">\d+<\/span>/, '').trim();
            var correctOpt = opts[ansNum - 1];
            var correctTex = correctOpt ? correctOpt.innerHTML.replace(/<span class="n">\d+<\/span>/, '').trim() : '';

            var diagDiv = document.createElement('div');
            if (chosenNum === ansNum) {
              var nextStepGuide = (idx < qs.length - 1)
                ? ('이제 방금 스스로 도출한 <b>' + correctTex + '</b> 조각을 다음 <b>' + (idx + 2) + '단계</b>의 조건에 레고 블록처럼 결합해 보세요!')
                : '초등 기초 직관(1단계)부터 출발해 수능 본문항까지 스스로 재발명(Guided Reinvention)하여 완주했습니다!';
              diagDiv.className = 'acad-diag-box acad-diag-correct';
              diagDiv.innerHTML =
                '<b>✨ [프로이덴탈 안내된 재발명(Guided Reinvention) 성공!]</b><br>' +
                '정확합니다! 선택한 <b>' + chosenTex + '</b>은(는) 이 단계의 핵심 수학적 변환을 완벽히 만족합니다. ' + nextStepGuide;
            } else {
              if (window.recordStepClinicWeakness) window.recordStepClinicWeakness(idx, 'wrong');
              var prevCheckMsg = idx > 0
                ? ('앞선 <b>' + idx + '단계 디딤돌</b>의 결과와 <b>제0단계 기호 번역기</b>의 지수·부호·정의역 약속을 다시 대조해 보세요.')
                : '<b>제0단계 수학 기호 번역기</b>의 기본 연산 약속(곱셈 횟수, 부호, 분수 계산)을 작은 숫자로 먼저 확인해 보세요.';
              diagDiv.className = 'acad-diag-box acad-diag-wrong';
              diagDiv.innerHTML =
                '<b>🔬 [수학교육학 오개념 정밀 진단 (Hattie Elaborative Feedback)]</b><br>' +
                '• 내가 선택한 보기(' + chosenNum + '번): <b>' + chosenTex + '</b> ➔ 목표 정답(' + ansNum + '번): <b>' + correctTex + '</b><br>' +
                '• <b>진단 포인트</b>: 이 단계에서 흔히 발생하는 착오는 <b>① 지수·괄호·부호 결합 법칙의 혼동</b> 또는 <b>② 앞 단계 관계식 대입 과정의 계수/상수 착오</b>입니다. ' + prevCheckMsg;
            }
            expEl.insertBefore(diagDiv, expEl.firstChild);
            if (window.MathJax && window.MathJax.typesetPromise) {
              window.MathJax.typesetPromise([diagDiv]).catch(function() {});
            }
          }, 30);
        });
      });
    });
  }


  // ════════════════════════════════════════════════════════════════════════
  // 🔊 11. AI 수식-음성 변환 해설 선생님 (MatheduVoiceTeacher: LaTeX-to-Speech Engine)
  //     & 민은기 선생님(min7014.github.io) 1,111개 자료 심층 원리·보조선 도슨트 연동
  // ════════════════════════════════════════════════════════════════════════
  function initVoiceTeacherAndMin7014Deep() {
    if (window.MatheduVoiceTeacher) return;

    // Style injection for Voice Teacher Floating Player & min7014 Deep Insight Box
    if (!document.getElementById('mathedu-voice-teacher-styles')) {
      var vStyle = document.createElement('style');
      vStyle.id = 'mathedu-voice-teacher-styles';
      vStyle.textContent =
        '.mathedu-voice-btn { display:inline-flex; align-items:center; gap:5px; padding:6px 12px; border-radius:999px; font-size:0.76rem; font-weight:800; border:1px solid rgba(79,70,229,0.32); background:linear-gradient(135deg,#eef2ff 0%,#e0f2fe 100%); color:#3730a3; cursor:pointer; transition:all 0.15s ease; }\n' +
        '.mathedu-voice-btn:hover { background:linear-gradient(135deg,#4f46e5 0%,#006398 100%); color:#ffffff; border-color:transparent; box-shadow:0 4px 12px rgba(79,70,229,0.25); }\n' +
        '.mathedu-voice-btn.speaking { background:linear-gradient(135deg,#4f46e5 0%,#059669 100%); color:#ffffff; border-color:transparent; animation:voicePulse 1.6s infinite; }\n' +
        '@keyframes voicePulse { 0%,100% { box-shadow:0 0 0 0 rgba(79,70,229,0.45); } 50% { box-shadow:0 0 0 7px rgba(79,70,229,0); } }\n' +
        '#matheduVoiceFloatingBar { position:fixed; bottom:74px; left:50%; transform:translateX(-50%); z-index:1000005; width:calc(100% - 24px); max-width:780px; background:rgba(15,23,42,0.95); backdrop-filter:blur(16px); -webkit-backdrop-filter:blur(16px); color:#f8fafc; border:1.5px solid rgba(56,189,248,0.42); border-radius:16px; padding:12px 16px; box-shadow:0 16px 40px rgba(0,0,0,0.45); display:none; flex-direction:column; gap:8px; }\n' +
        '#matheduVoiceFloatingBar.show { display:flex; }\n' +
        '.voice-bar-top { display:flex; align-items:center; justify-content:space-between; gap:10px; flex-wrap:wrap; }\n' +
        '.voice-bar-title { font-size:0.8rem; font-weight:800; color:#38bdf8; display:flex; align-items:center; gap:6px; }\n' +
        '.voice-bar-controls { display:flex; align-items:center; gap:6px; flex-wrap:wrap; }\n' +
        '.voice-ctrl-btn { padding:4px 10px; border-radius:8px; font-size:0.74rem; font-weight:800; border:1px solid rgba(148,163,184,0.35); background:rgba(30,41,59,0.9); color:#f8fafc; cursor:pointer; }\n' +
        '.voice-ctrl-btn:hover { background:#0284c7; border-color:#38bdf8; }\n' +
        '#matheduVoiceSubtitle { font-size:0.84rem; color:#e2e8f0; line-height:1.55; padding:8px 12px; background:rgba(30,41,59,0.75); border-radius:10px; border-left:3px solid #38bdf8; max-height:92px; overflow-y:auto; }\n' +
        '.min7014-deep-box { margin-top:8px; padding:10px 12px; border-radius:10px; background:linear-gradient(135deg,#f8fafc 0%,#f0f9ff 100%); border:1px solid #bae6fd; font-size:0.8rem; color:#1e293b; line-height:1.55; }\n' +
        '.min7014-deep-tip { margin-top:5px; padding:6px 10px; border-radius:8px; background:#fefce8; border:1px solid #fde047; color:#713f12; font-size:0.77rem; font-weight:700; }\n' +
        'html.dark-theme .mathedu-voice-btn { background:rgba(49,46,129,0.65); color:#c7d2fe; border-color:rgba(129,140,248,0.4); }\n' +
        'html.dark-theme .min7014-deep-box { background:rgba(15,23,42,0.85) !important; border-color:rgba(56,189,248,0.28) !important; color:#e2e8f0 !important; }\n' +
        'html.dark-theme .min7014-deep-tip { background:rgba(66,32,6,0.55) !important; border-color:rgba(250,204,21,0.35) !important; color:#fef08a !important; }\n';
      (document.head || document.documentElement).appendChild(vStyle);
    }

    // Tag all rendered MathJax containers with their original LaTeX string
    function annotateMathJaxNodes(rootEl) {
      try {
        if (window.MathJax && window.MathJax.startup && window.MathJax.startup.document && typeof window.MathJax.startup.document.getMathItemsWithin === 'function') {
          var items = window.MathJax.startup.document.getMathItemsWithin(rootEl || document.body);
          items.forEach(function(it) {
            if (it && it.typesetRoot && typeof it.math === 'string') {
              it.typesetRoot.setAttribute('data-mjx-tex', it.math);
            }
          });
        }
      } catch (e) {}
    }

    // Convert a single LaTeX expression into natural Korean or English spoken words
    function compileFormulaToSpeech(tex, isEn) {
      var s = String(tex || '').trim();
      if (!s) return '';

      // Remove purely visual formatting commands
      s = s.replace(/\\(?:displaystyle|textstyle|scriptstyle|underline|mathbf|mathrm|mathit|mathcal|mathbb|textbf|textrm|left|right|Big|big|quad|qquad|,|;|:|!)/g, ' ');
      s = s.replace(/\\text\s*\{([^{}]*)\}/g, ' $1 ');

      if (isEn) {
        s = s.replace(/\\cancel\s*\{([^{}]*)\}/g, ' canceled $1 ');
        for (var i = 0; i < 3; i++) {
          s = s.replace(/\\(?:d|t)?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}/g, ' $1 over $2 ');
        }
        s = s.replace(/\\sqrt\s*\[([^{}\]]*)\]\s*\{([^{}]*)\}/g, ' $1-th root of $2 ');
        s = s.replace(/\\sqrt\s*\{([^{}]*)\}/g, ' square root of $2 ');
        s = s.replace(/\\lim_\{([^{}]*)\\to\s*([^{}]*)\}/g, ' limit as $1 approaches $2 of ');
        s = s.replace(/\\sum_\{([^{}]*)\}\^\{([^{}]*)\}/g, ' sum from $1 to $2 of ');
        s = s.replace(/\\int_\{([^{}]*)\}\^\{([^{}]*)\}/g, ' integral from $1 to $2 of ');
        s = s.replace(/\\log_\{([^{}]*)\}/g, ' log base $1 of ');
        s = s.replace(/\^\{2\}|\^2/g, ' squared ');
        s = s.replace(/\^\{3\}|\^3/g, ' cubed ');
        s = s.replace(/\^\{([^{}]+)\}/g, ' to the power of $1 ');
        s = s.replace(/_\{([^{}]+)\}|_([a-zA-Z0-9])/g, ' $1$2 ');
        s = s.replace(/\\le|\\leq|≤/g, ' is less than or equal to ');
        s = s.replace(/\\ge|\\geq|≥/g, ' is greater than or equal to ');
        s = s.replace(/\\ne|\\neq|≠/g, ' is not equal to ');
        s = s.replace(/\\implies|\\Rightarrow|⇒|➔/g, ', which implies ');
        s = s.replace(/\\infty|∞/g, ' infinity ');
        s = s.replace(/\\times|×|\\cdot/g, ' times ');
        s = s.replace(/\\div|÷/g, ' divided by ');
        s = s.replace(/[{}]/g, ' ').replace(/\\/g, ' ');
        return s.replace(/\s+/g, ' ').trim();
      }

      // Korean natural mathematical speech conversion (분모 먼저 읽기: \frac{A}{B} -> B 분의 A)
      s = s.replace(/\\cancel\s*\{([^{}]*)\}/g, ' 소거되는 $1 ');
      s = s.replace(/\\(?:overrightarrow|vec)\s*\{([^{}]*)\}/g, ' 벡터 $1 ');
      s = s.replace(/\\overline\s*\{([^{}]*)\}/g, ' 선분 $1 ');
      s = s.replace(/\\triangle\s*([A-Za-z0-9]*)/g, ' 삼각형 $1 ');
      s = s.replace(/\\angle\s*([A-Za-z0-9]*)/g, ' 각 $1 ');

      // Nested fractions (3 passes): \frac{num}{den} -> den 분의 num
      for (var k = 0; k < 3; k++) {
        s = s.replace(/\\(?:d|t)?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}/g, ' $2 분의 $1 ');
      }
      s = s.replace(/\\(?:d|t)?frac\s*([0-9a-zA-Z])\s*([0-9a-zA-Z])/g, ' $2 분의 $1 ');

      // Roots
      s = s.replace(/\\sqrt\s*\[([^{}\]]*)\]\s*\{([^{}]*)\}/g, ' $1제곱근 $2 ');
      s = s.replace(/\\sqrt\s*\{([^{}]*)\}/g, ' 루트 $1 ');
      s = s.replace(/\\sqrt\s*([0-9a-zA-Z]+)/g, ' 루트 $1 ');

      // Limits, Sums, Integrals, Logs
      s = s.replace(/\\lim_\{([^{}]*)\\to\s*\\infty\}/g, ' 리미트 $1 이 무한대로 갈 때 ');
      s = s.replace(/\\lim_\{([^{}]*)\\to\s*([^{}]*)\}/g, ' 리미트 $1 이 $2 로 갈 때 ');
      s = s.replace(/\\sum_\{([^{}]*)\}\^\{([^{}]*)\}/g, ' 시그마 $1 부터 $2 까지 ');
      s = s.replace(/\\int_\{([^{}]*)\}\^\{([^{}]*)\}/g, ' $1 에서 $2 까지 정적분 ');
      s = s.replace(/\\int_([0-9a-zA-Z]+)\^([0-9a-zA-Z]+)/g, ' $1 에서 $2 까지 정적분 ');
      s = s.replace(/\\int/g, ' 인테그랄 ');
      s = s.replace(/\\sum/g, ' 시그마 ');
      s = s.replace(/\\log_\{([^{}]*)\}\s*\{([^{}]*)\}/g, ' 로그 $1 의 $2 ');
      s = s.replace(/\\log_\{([^{}]*)\}/g, ' 밑이 $1 인 로그 ');
      s = s.replace(/\\log_([0-9a-zA-Z]+)/g, ' 로그 $1 의 ');
      s = s.replace(/\\ln/g, ' 자연로그 ');

      // Trig & Functions
      s = s.replace(/\\sin\^2/g, ' 사인 제곱 ');
      s = s.replace(/\\cos\^2/g, ' 코사인 제곱 ');
      s = s.replace(/\\tan\^2/g, ' 탄젠트 제곱 ');
      s = s.replace(/\\sin/g, ' 사인 ');
      s = s.replace(/\\cos/g, ' 코사인 ');
      s = s.replace(/\\tan/g, ' 탄젠트 ');
      s = s.replace(/([fghFGH])''\s*\(([^)]+)\)/g, ' $1 더블프라임 $2 ');
      s = s.replace(/([fghFGH])'\s*\(([^)]+)\)/g, ' $1 프라임 $2 ');

      // Exponents & Subscripts
      s = s.replace(/\^\{\\circ\}|\^\\circ|°/g, ' 도 ');
      s = s.replace(/\^\{2\}|\^2/g, ' 제곱 ');
      s = s.replace(/\^\{3\}|\^3/g, ' 세제곱 ');
      s = s.replace(/\^\{-1\}/g, ' 의 마이너스 1제곱 ');
      s = s.replace(/\^\{([^{}]+)\}/g, ' 의 $1제곱 ');
      s = s.replace(/\^([0-9a-zA-Z]+)/g, ' 의 $1제곱 ');
      s = s.replace(/_\{([^{}]+)\}/g, ' $1 ');
      s = s.replace(/_([0-9a-zA-Z]+)/g, ' $1 ');

      // Greek letters & Symbols
      var greekMap = {
        '\\alpha': '알파', '\\beta': '베타', '\\gamma': '감마', '\\delta': '델타', '\\Delta': '델타',
        '\\theta': '세타', '\\pi': '파이', '\\sigma': '시그마', '\\omega': '오메가', '\\lambda': '람다',
        '\\mu': '뮤', '\\phi': '파이', '\\ell': '엘'
      };
      Object.keys(greekMap).forEach(function(gKey) {
        s = s.split(gKey).join(' ' + greekMap[gKey] + ' ');
      });

      s = s.replace(/\\le|\\leq|≤/g, ' 이하 ');
      s = s.replace(/\\ge|\\geq|≥/g, ' 이상 ');
      s = s.replace(/\\ne|\\neq|≠/g, ' 같지 않고 ');
      s = s.replace(/\\implies|\\Rightarrow|⇒|➔/g, ', 즉 ');
      s = s.replace(/\\iff|\\Leftrightarrow|⇔/g, ', 필요충분조건으로 ');
      s = s.replace(/\\to|\\rightarrow|→/g, ' 에서 ');
      s = s.replace(/\\infty|∞/g, ' 무한대 ');
      s = s.replace(/\\pm|±/g, ' 플러스마이너스 ');
      s = s.replace(/\\times|×|\\cdot/g, ' 곱하기 ');
      s = s.replace(/\\div|÷/g, ' 나누기 ');
      s = s.replace(/\\therefore|∴/g, ' 따라서 ');
      s = s.replace(/\\because|∵/g, ' 왜냐하면 ');
      s = s.replace(/\\sim/g, ' 따른다 ');
      s = s.replace(/\\in|∈/g, ' 속하며 ');
      s = s.replace(/\\cup/g, ' 합집합 ');
      s = s.replace(/\\cap/g, ' 교집합 ');
      s = s.replace(/\\perp/g, ' 수직 ');
      s = s.replace(/\\parallel/g, ' 평행 ');
      s = s.replace(/=/g, ' 는 ');
      s = s.replace(/\+/g, ' 더하기 ');
      s = s.replace(/([0-9a-zA-Z])\s*-\s*([0-9a-zA-Z])/g, '$1 마이너스 $2');
      s = s.replace(/-\s*([0-9]+)/g, ' 마이너스 $1');
      s = s.replace(/[{}]/g, ' ').replace(/\\/g, ' ');
      return s.replace(/\s+/g, ' ').trim();
    }

    function htmlOrTextToSpeechScript(rawInput, isEn) {
      var str = '';
      if (typeof rawInput === 'string') {
        str = rawInput;
      } else if (rawInput && rawInput.nodeType === 1) {
        annotateMathJaxNodes(rawInput);
        var clone = rawInput.cloneNode(true);
        var toRemove = clone.querySelectorAll('svg, style, script, .report-wrap, .q-actions, .acad-hint-box, .acad-blind-mask');
        toRemove.forEach(function(el) { el.remove(); });
        var hiddenLang = clone.querySelectorAll(isEn ? '.bilingual-ko' : '.bilingual-en');
        hiddenLang.forEach(function(el) { el.remove(); });
        var mjxList = clone.querySelectorAll('mjx-container');
        mjxList.forEach(function(mjx) {
          var tex = mjx.getAttribute('data-mjx-tex') || '';
          var span = document.createElement('span');
          span.textContent = tex ? (' $' + tex + '$ ') : ' ';
          if (mjx.parentNode) mjx.parentNode.replaceChild(span, mjx);
        });
        str = clone.innerHTML;
      }

      if (!str) return '';

      // Strip SVG, style, script tags from raw HTML strings
      str = str.replace(/<svg[\s\S]*?<\/svg>/gi, ' ');
      str = str.replace(/<style[\s\S]*?<\/style>/gi, ' ');
      str = str.replace(/<script[\s\S]*?<\/script>/gi, ' ');
      str = str.replace(/<br\s*\/?>|<\/p>|<\/li>|<\/div>|<\/h[1-6]>|<\/tr>/gi, '. ');
      str = str.replace(/<\/td>|<\/th>/gi, ', ');
      str = str.replace(/<[^>]+>/g, ' ');

      // Decode common HTML entities
      str = str
        .replace(/&nbsp;/g, ' ')
        .replace(/&le;/g, '≤')
        .replace(/&ge;/g, '≥')
        .replace(/&ne;/g, '≠')
        .replace(/&times;/g, '×')
        .replace(/&divide;/g, '÷')
        .replace(/&amp;/g, '&')
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>')
        .replace(/&quot;/g, '"')
        .replace(/&#39;/g, "'");

      // Compile display math $$...$$ and inline math $...$
      str = str.replace(/\$\$([\s\S]*?)\$\$/g, function(_, tex) {
        return ' ' + compileFormulaToSpeech(tex, isEn) + '. ';
      });
      str = str.replace(/\$([^\$]+?)\$/g, function(_, tex) {
        return ' ' + compileFormulaToSpeech(tex, isEn) + ' ';
      });
      str = str.replace(/\\\(([\s\S]*?)\\\)/g, function(_, tex) {
        return ' ' + compileFormulaToSpeech(tex, isEn) + ' ';
      });

      // Clean decorative emojis & symbols for smooth TTS
      str = str.replace(/[🔰🌿🌱🌳💎🏆🎨🗺️📐📋✨📌🔗🎬📂🎮📄🎥▶️💡🧭🪜🧠🔬⭕❌▲■•]/g, ' ');
      str = str.replace(/\s+/g, ' ').replace(/\.\s*\./g, '.').trim();
      return str;
    }

    function splitIntoSentences(scriptText) {
      var rawParts = String(scriptText || '').split(/(?<=[.!?])\s+|\s*\.\s+/);
      var chunks = [];
      var buf = '';
      for (var i = 0; i < rawParts.length; i++) {
        var p = rawParts[i].trim();
        if (!p) continue;
        if ((buf + ' ' + p).length < 110) {
          buf = buf ? (buf + '. ' + p) : p;
        } else {
          if (buf) chunks.push(buf);
          buf = p;
        }
      }
      if (buf) chunks.push(buf);
      return chunks.length > 0 ? chunks : [scriptText];
    }

    function ensureVoiceFloatingBar() {
      var bar = document.getElementById('matheduVoiceFloatingBar');
      if (bar) return bar;
      bar = document.createElement('div');
      bar.id = 'matheduVoiceFloatingBar';
      bar.innerHTML =
        '<div class="voice-bar-top">' +
          '<div class="voice-bar-title">' +
            '<span>🔊 AI 수학 음성 선생님</span>' +
            '<span id="matheduVoiceTitleLabel" style="color:#f8fafc;font-weight:700"></span>' +
          '</div>' +
          '<div class="voice-bar-controls">' +
            '<button type="button" class="voice-ctrl-btn" onclick="window.MatheduVoiceTeacher.prev()">⏮️ 이전</button>' +
            '<button type="button" class="voice-ctrl-btn" id="matheduVoicePauseBtn" onclick="window.MatheduVoiceTeacher.togglePause()">⏸️ 일시정지</button>' +
            '<button type="button" class="voice-ctrl-btn" onclick="window.MatheduVoiceTeacher.next()">⏭️ 다음</button>' +
            '<button type="button" class="voice-ctrl-btn" id="matheduVoiceRateBtn" onclick="window.MatheduVoiceTeacher.cycleRate()">⚡ 1.0x</button>' +
            '<button type="button" class="voice-ctrl-btn" style="background:#be123c;border-color:#fb7185" onclick="window.MatheduVoiceTeacher.stop()">⏹️ 닫기</button>' +
          '</div>' +
        '</div>' +
        '<div id="matheduVoiceSubtitle">음성 강의를 준비 중입니다...</div>';
      document.body.appendChild(bar);
      return bar;
    }

    var voiceState = {
      chunks: [],
      idx: 0,
      rate: 1.0,
      playing: false,
      paused: false,
      title: ''
    };

    function playCurrentChunk() {
      var bar = ensureVoiceFloatingBar();
      var subEl = document.getElementById('matheduVoiceSubtitle');
      var titleEl = document.getElementById('matheduVoiceTitleLabel');
      var pauseBtn = document.getElementById('matheduVoicePauseBtn');

      if (voiceState.idx >= voiceState.chunks.length) {
        voiceState.playing = false;
        if (subEl) subEl.textContent = '✅ 음성 해설이 완료되었습니다. (다시 들으려면 버튼을 누르세요)';
        if (pauseBtn) pauseBtn.textContent = '🔄 처음부터';
        document.querySelectorAll('.mathedu-voice-btn.speaking').forEach(function(b) { b.classList.remove('speaking'); });
        return;
      }

      var chunk = voiceState.chunks[voiceState.idx];
      if (titleEl) {
        titleEl.textContent = '· ' + voiceState.title + ' (' + (voiceState.idx + 1) + '/' + voiceState.chunks.length + ')';
      }
      if (subEl) {
        subEl.textContent = chunk;
      }
      if (pauseBtn) {
        pauseBtn.textContent = '⏸️ 일시정지';
      }

      if (!('speechSynthesis' in window)) {
        if (subEl) subEl.textContent = '💬 [자막 모드]: ' + chunk;
        return;
      }

      try {
        window.speechSynthesis.cancel();
        var utter = new SpeechSynthesisUtterance(chunk);
        var en = isEnMode();
        utter.lang = en ? 'en-US' : 'ko-KR';
        utter.rate = voiceState.rate;
        utter.pitch = 1.02;

        // Try to pick the clearest Korean / English voice available
        var voices = window.speechSynthesis.getVoices ? window.speechSynthesis.getVoices() : [];
        if (voices && voices.length > 0) {
          var targetPrefix = en ? 'en' : 'ko';
          var preferred = voices.find(function(v) {
            return v.lang && v.lang.toLowerCase().indexOf(targetPrefix) === 0 && (v.name.indexOf('Natural') !== -1 || v.name.indexOf('Google') !== -1 || v.name.indexOf('Heami') !== -1 || v.name.indexOf('SunHi') !== -1);
          }) || voices.find(function(v) {
            return v.lang && v.lang.toLowerCase().indexOf(targetPrefix) === 0;
          });
          if (preferred) utter.voice = preferred;
        }

        utter.onend = function() {
          if (!voiceState.playing || voiceState.paused) return;
          voiceState.idx++;
          playCurrentChunk();
        };
        utter.onerror = function() {
          if (!voiceState.playing || voiceState.paused) return;
          voiceState.idx++;
          playCurrentChunk();
        };

        window.speechSynthesis.speak(utter);
      } catch (e) {}
    }

    window.MatheduVoiceTeacher = {
      compileToSpeech: htmlOrTextToSpeechScript,
      speakRaw: function(rawHtmlOrNode, titleLabel, btnEl) {
        var en = isEnMode();
        var script = htmlOrTextToSpeechScript(rawHtmlOrNode, en);
        if (!script) return;
        document.querySelectorAll('.mathedu-voice-btn.speaking').forEach(function(b) { b.classList.remove('speaking'); });
        if (btnEl && btnEl.classList) btnEl.classList.add('speaking');

        voiceState.chunks = splitIntoSentences(script);
        voiceState.idx = 0;
        voiceState.playing = true;
        voiceState.paused = false;
        voiceState.title = titleLabel || (en ? 'AI Math Voice Explanation' : 'AI 수학 음성 해설');

        var bar = ensureVoiceFloatingBar();
        bar.classList.add('show');
        playCurrentChunk();
      },
      speakQuizStep: function(idx, btnEl) {
        var qs = document.querySelectorAll('.q');
        var q = qs[idx];
        if (!q) return;
        var en = isEnMode();
        var knowEl = q.previousElementSibling && q.previousElementSibling.classList.contains('know') ? q.previousElementSibling : null;
        var stemEl = q.querySelector('.stem');
        var isDone = q.classList.contains('done') || (q.querySelector('.exp') && q.querySelector('.exp').classList.contains('show'));

        var parts = [];
        parts.push(en ? ('Step ' + (idx + 1) + ' explanation.') : ((idx + 1) + '단계 디딤돌 음성 설명입니다.'));
        if (knowEl) {
          parts.push(htmlOrTextToSpeechScript(knowEl, en));
        }
        if (stemEl) {
          parts.push((en ? 'Question: ' : '문제 조건을 함께 읽어봅시다. ') + htmlOrTextToSpeechScript(stemEl, en));
        }
        if (isDone) {
          var rawExp = en ? (q.dataset.expEn || q.dataset.exp || '') : (q.dataset.exp || '');
          parts.push((en ? 'Step Solution: ' : '이 단계의 풀이 및 정답 도출 과정입니다. ') + htmlOrTextToSpeechScript(rawExp, en));
        } else {
          parts.push(en ? 'Try thinking of the answer before checking the options, or click the ZPD Step Hint button if you need a clue.' : '아직 문제를 풀기 전이므로 정답은 스포일러하지 않습니다. 위 원리를 바탕으로 빈칸이나 값을 먼저 추론해 보세요!');
        }

        window.MatheduVoiceTeacher.speakRaw(parts.join(' '), (idx + 1) + '단계 ' + (isDone ? '문제·해설 강의' : '개념·발문 코칭'), btnEl);
      },
      speakFullProblemTour: function(btnEl) {
        var en = isEnMode();
        var parts = [];
        var h1 = document.querySelector('.stitch-hero-card h1') || document.querySelector('h1');
        if (h1) parts.push((en ? 'Problem Overview: ' : '민은기 선생님의 수학자료실 AI 음성 수학 강의입니다. 이번 문항은 ') + htmlOrTextToSpeechScript(h1, en));
        var origBox = document.getElementById('examOrigPaperBox') || document.querySelector('.orig-text-box');
        if (origBox) parts.push((en ? 'Original Exam Question: ' : '수능 및 모의평가 원문 조건입니다. ') + htmlOrTextToSpeechScript(origBox, en));
        var symEl = document.getElementById('examSymContainer');
        if (symEl) parts.push((en ? 'Key Symbol Definitions: ' : '제0단계 수학 기호 번역기입니다. ') + htmlOrTextToSpeechScript(symEl, en));
        var flowEl = document.querySelector('.math-schematic-flow');
        if (flowEl) parts.push((en ? 'Schematic Solution Flowchart: ' : '한눈에 보는 도식화 풀이 흐름도입니다. ') + htmlOrTextToSpeechScript(flowEl, en));

        window.MatheduVoiceTeacher.speakRaw(parts.join(' '), en ? 'Full Problem Audio Lecture' : '문항 전체 핵심 흐름 음성 강의', btnEl);
      },
      speakFinalSolution: function(btnEl) {
        var en = isEnMode();
        var solEl = document.querySelector('.sol');
        if (!solEl) return;
        window.MatheduVoiceTeacher.speakRaw(solEl, en ? 'Complete Step-by-Step Solution Audio' : '완결 풀이 및 단계별 총정리 음성 강의', btnEl);
      },
      togglePause: function() {
        var pauseBtn = document.getElementById('matheduVoicePauseBtn');
        if (!voiceState.playing) {
          voiceState.idx = 0;
          voiceState.playing = true;
          voiceState.paused = false;
          playCurrentChunk();
          return;
        }
        if (voiceState.paused) {
          voiceState.paused = false;
          if ('speechSynthesis' in window && window.speechSynthesis.paused) {
            window.speechSynthesis.resume();
          } else {
            playCurrentChunk();
          }
          if (pauseBtn) pauseBtn.textContent = '⏸️ 일시정지';
        } else {
          voiceState.paused = true;
          if ('speechSynthesis' in window) window.speechSynthesis.pause();
          if (pauseBtn) pauseBtn.textContent = '▶️ 계속 듣기';
        }
      },
      prev: function() {
        if (voiceState.chunks.length === 0) return;
        voiceState.idx = Math.max(0, voiceState.idx - 1);
        voiceState.playing = true;
        voiceState.paused = false;
        playCurrentChunk();
      },
      next: function() {
        if (voiceState.chunks.length === 0) return;
        voiceState.idx = Math.min(voiceState.chunks.length - 1, voiceState.idx + 1);
        voiceState.playing = true;
        voiceState.paused = false;
        playCurrentChunk();
      },
      cycleRate: function() {
        var rates = [0.85, 1.0, 1.2, 1.4];
        var curIdx = rates.indexOf(voiceState.rate);
        voiceState.rate = rates[(curIdx + 1) % rates.length];
        var rBtn = document.getElementById('matheduVoiceRateBtn');
        if (rBtn) rBtn.textContent = '⚡ ' + voiceState.rate.toFixed(2).replace(/\.00$/, '.0').replace(/0$/, '') + 'x';
        if (voiceState.playing && !voiceState.paused) {
          playCurrentChunk();
        }
      },
      stop: function() {
        voiceState.playing = false;
        voiceState.paused = false;
        if ('speechSynthesis' in window) {
          try { window.speechSynthesis.cancel(); } catch (e) {}
        }
        var bar = document.getElementById('matheduVoiceFloatingBar');
        if (bar) bar.classList.remove('show');
        document.querySelectorAll('.mathedu-voice-btn.speaking').forEach(function(b) { b.classList.remove('speaking'); });
      }
    };

    // Attach Voice Lecture buttons to Problem Page elements
    var pillRow = document.querySelector('#matheduAcademicWorkbench .acad-pill-row');
    if (pillRow && !document.getElementById('btnAcadVoiceLecture')) {
      var vTopBtn = document.createElement('button');
      vTopBtn.type = 'button';
      vTopBtn.id = 'btnAcadVoiceLecture';
      vTopBtn.className = 'mathedu-voice-btn';
      vTopBtn.innerHTML = bilingual('🔊 AI 음성 강의 듣기', '🔊 AI Voice Lecture');
      vTopBtn.onclick = function() {
        window.MatheduVoiceTeacher.speakFullProblemTour(vTopBtn);
      };
      pillRow.insertBefore(vTopBtn, pillRow.firstChild);
    }

    // Add step-level voice button to every .q
    var qsAll = document.querySelectorAll('.q');
    qsAll.forEach(function(q, idx) {
      var actions = q.querySelector('.q-actions');
      if (!actions || actions.querySelector('.step-voice-btn')) return;
      var sBtn = document.createElement('button');
      sBtn.type = 'button';
      sBtn.className = 'mathedu-voice-btn step-voice-btn';
      sBtn.style.marginRight = '6px';
      sBtn.innerHTML = bilingual('🔊 음성 설명', '🔊 Voice Guide');
      sBtn.onclick = function() {
        window.MatheduVoiceTeacher.speakQuizStep(idx, sBtn);
      };
      actions.insertBefore(sBtn, actions.firstChild);
    });

    // Add full solution voice button to .sol
    var solBox = document.querySelector('.sol');
    if (solBox && !solBox.querySelector('.sol-voice-header-bar')) {
      var solBar = document.createElement('div');
      solBar.className = 'sol-voice-header-bar';
      solBar.style.cssText = 'display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;padding:10px 14px;margin-bottom:14px;border-radius:12px;background:linear-gradient(135deg,#eef2ff 0%,#f0f9ff 100%);border:1px solid #bae6fd;';
      solBar.innerHTML =
        '<span style="font-size:0.82rem;font-weight:800;color:#006398">' +
          bilingual('🎧 눈으로 도형·흐름도를 보면서 선생님의 칠판 풀이 음성 강의를 함께 들어보세요!', '🎧 Listen to the step-by-step audio explanation while viewing the visual diagram!') +
        '</span>' +
        '<button type="button" class="mathedu-voice-btn" onclick="window.MatheduVoiceTeacher.speakFinalSolution(this)">' +
          bilingual('🔊 완결 풀이 전체 음성으로 듣기', '🔊 Listen to Full Solution') +
        '</button>';
      solBox.insertBefore(solBar, solBox.firstChild);
    }

    // Enrich .min7014-addon-card items with Deep Knowledge & Voice Docent
    var minItems = document.querySelectorAll('.min7014-addon-card .min-item');
    if (minItems.length > 0) {
      var isBoard = window.location.pathname.indexOf('/board/') !== -1 || window.location.pathname.indexOf('/offline/') !== -1;
      var lookupUrl = isBoard ? '../assets/min7014_lookup.json' : 'assets/min7014_lookup.json';

      function applyMinItemEnrichment(lookupMap) {
        minItems.forEach(function(itemEl) {
          if (itemEl.dataset.minDeepBound === '1') return;
          itemEl.dataset.minDeepBound = '1';

          var linkEl = itemEl.querySelector('a.min-item-title');
          var href = linkEl ? (linkEl.getAttribute('href') || '') : '';
          var slugKey = href.split('/').pop().replace('.html', '');
          var info = (lookupMap && lookupMap[slugKey]) ? lookupMap[slugKey] : null;

          var rawTitle = linkEl ? linkEl.textContent.replace('📌', '').trim() : '수학자료실 개념 증명';
          var subDomain = info && info.s ? info.s : '동적 기하·시각적 원리 증명';
          var coreConcept = info && info.c ? info.c : ('[' + rawTitle + ']의 기하학적 불변 성질과 대수적 관계식을 동적 작도와 플립북 증명으로 규명합니다.');
          var visSummary = info && info.v ? info.v : 'GeoGebra 슬라이더를 움직이거나 증명 PDF를 한 프레임씩 넘기며 보조선이 그어지는 순간의 성질을 관찰하세요.';
          var solvingTip = info && info.p ? info.p : '수능 실전 문항에서 복잡한 계산에 막힐 때는 이 자료의 기하학적 정의와 대칭 보조선으로 돌아가면 직관적으로 해결됩니다.';
          var voiceScript = info && info.w ? info.w : (rawTitle + '. ' + coreConcept + ' ' + visSummary + ' 실전 팁으로, ' + solvingTip);

          var catBadge = itemEl.querySelector('.min-cat-badge');
          if (catBadge) {
            catBadge.textContent = '📂 ' + subDomain;
          }

          var mainDiv = itemEl.querySelector('.min-item-main');
          if (mainDiv) {
            var deepBox = document.createElement('div');
            deepBox.className = 'min7014-deep-box';
            deepBox.innerHTML =
              '<div><b>🎓 핵심 원리</b>: ' + coreConcept + '</div>' +
              '<div style="margin-top:3px;color:#0369a1"><b>👁️ 시각적 탐구</b>: ' + visSummary + '</div>' +
              '<div class="min7014-deep-tip">💡 <b>수능 실전 보조선·풀이 팁</b>: ' + solvingTip + '</div>';
            mainDiv.appendChild(deepBox);
            if (window.MathJax && window.MathJax.typesetPromise) {
              window.MathJax.typesetPromise([deepBox]).catch(function() {});
            }
          }

          var actDiv = itemEl.querySelector('.min-item-actions');
          if (actDiv) {
            var pdfLinkEl = actDiv.querySelector('a[href$=".pdf"], a[href*=".pdf"]');
            if (pdfLinkEl && !actDiv.querySelector('.min-video-studio-btn')) {
              var pdfHref = pdfLinkEl.getAttribute('href') || '';
              var studioBase = isBoard ? '../video_studio.html' : 'video_studio.html';
              var vidBtn = document.createElement('a');
              vidBtn.href = studioBase + '?pdf=' + encodeURIComponent(pdfHref);
              vidBtn.className = 'mathedu-voice-btn min-video-studio-btn';
              vidBtn.style.textDecoration = 'none';
              vidBtn.innerHTML = bilingual('🎬 다국어 강의 영상', '🎬 Multi-Lang Video');
              actDiv.insertBefore(vidBtn, actDiv.firstChild);
            }
            if (info && (info.yk || info.ye) && !actDiv.querySelector('.min-yt-vault-btn')) {
              var vaultBtn = document.createElement('button');
              vaultBtn.type = 'button';
              vaultBtn.className = 'mathedu-voice-btn min-yt-vault-btn';
              vaultBtn.style.background = 'linear-gradient(135deg,#e11d48,#be123c)';
              vaultBtn.innerHTML = bilingual('📺 @min7014_ai 영상저장고 재생', '📺 @min7014_ai Video Vault');
              vaultBtn.onclick = function() {
                var targetYt = (isEnMode() && info.ye) ? info.ye : (info.yk || info.ye);
                window.open(targetYt || 'https://www.youtube.com/@min7014_ai', '_blank');
              };
              actDiv.insertBefore(vaultBtn, actDiv.firstChild);
            }
            var docentBtn = document.createElement('button');
            docentBtn.type = 'button';
            docentBtn.className = 'mathedu-voice-btn';
            docentBtn.innerHTML = bilingual('🔊 원리 음성 도슨트', '🔊 Audio Docent');
            docentBtn.onclick = function() {
              window.MatheduVoiceTeacher.speakRaw(voiceScript, '민은기 선생님 자료 도슨트', docentBtn);
            };
            actDiv.insertBefore(docentBtn, actDiv.firstChild);
          }
        });
      }

      fetch(lookupUrl)
        .then(function(r) { return r.ok ? r.json() : {}; })
        .then(function(map) { applyMinItemEnrichment(map); })
        .catch(function() { applyMinItemEnrichment({}); });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initRoom);
  } else {
    initRoom();
  }
})();
