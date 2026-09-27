/**
 * mathedu-room.js — 수학 mathedu 교사-학생 수업 연동 & 비회원 식별·학습 기록 모듈 (v3.0)
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
 */
(function() {
  'use strict';

  var urlParams = new URLSearchParams(window.location.search);
  var roomId = (urlParams.get('room') || '').trim();
  window._roomId = roomId;

  // 퀴즈 slug 추출
  var currentSlug = window.location.pathname.split('/').pop().replace('.html', '') || 'quiz';

  function ensureAuthLoaded(callback) {
    if (window.MatheduAuth) {
      if (typeof callback === 'function') callback();
      return;
    }
    var script = document.createElement('script');
    var isBoard = window.location.pathname.indexOf('/board/') !== -1;
    script.src = isBoard ? '../mathedu-auth.js' : './mathedu-auth.js';
    script.onload = function() {
      if (typeof callback === 'function') callback();
    };
    script.onerror = function() {
      if (typeof callback === 'function') callback();
    };
    document.head.appendChild(script);
  }

  function initRoom() {
    ensureAuthLoaded(function() {
      // 1. 학생이 특정 방에 참여 중인 경우 UI 표시
      if (roomId) {
        applyStudentRoomUI(roomId);
      }

      // 2. 시작 모달(#trackFull)에 비회원 간편 식별 및 이전 풀이 복원 기능 추가
      enhanceTrackFullModal();

      // 3. 문제 페이지 상단에 [이 문제로 수업 개설] 배너 삽입
      injectProblemPageBanner();

      // 4. 스크롤 중에도 언제든 누를 수 있는 플로팅 [🚀 이 문제로 수업 열기] 버튼
      injectFloatingClassButton();

      // 5. 상단바 tbtn에 버튼 추가 (내가 푼 문제 + 수업 열기)
      injectTopbarButtons();

      // 6. sendProgress 가로채기 (Google Sheets 전송 + MatheduAuth 풀이 기록 영구 저장)
      patchSendProgress();

      // 7. 이전에 풀었던 문제라면 페이지 상단에 진행 안내 바 표시
      checkAndShowResumeBanner();
    });
  }

  function applyStudentRoomUI(rId) {
    var trackFull = document.getElementById('trackFull');
    if (trackFull) {
      var h3 = trackFull.querySelector('h3');
      if (h3) {
        var roomBadge = document.createElement('div');
        roomBadge.style.cssText = 'display:inline-flex;align-items:center;gap:6px;background:rgba(124,196,255,.18);border:1px solid rgba(124,196,255,.35);color:#7cc4ff;border-radius:20px;padding:5px 16px;font-size:0.9rem;margin-bottom:14px;font-weight:700;box-shadow:0 0 16px rgba(124,196,255,.2);animation:popIn .3s ease';
        roomBadge.innerHTML = '🏫 <b>[' + escapeHtml(rId) + ']</b> 수업에 참여합니다';
        h3.parentNode.insertBefore(roomBadge, h3);
      }
      var p = trackFull.querySelector('p');
      if (p) {
        p.textContent = '선생님과 실시간으로 연동됩니다. 이름 또는 출석번호를 입력하세요.';
      }
      var input = document.getElementById('studentName');
      if (input) {
        input.placeholder = '예: 15번 김철수';
      }
    }

    var topbar = document.querySelector('.topbar') || document.querySelector('.navbar');
    if (topbar) {
      var activeRoomBadge = document.createElement('div');
      activeRoomBadge.style.cssText = 'margin-left:auto;display:inline-flex;align-items:center;gap:6px;background:rgba(62,220,151,.15);border:1px solid rgba(62,220,151,.35);color:#3ddc97;border-radius:10px;padding:6px 14px;font-size:0.85rem;font-weight:700;';
      activeRoomBadge.innerHTML = '🟢 <b>' + escapeHtml(rId) + '</b> 수업 참여 중';
      topbar.appendChild(activeRoomBadge);
    }
  }

  function enhanceTrackFullModal() {
    var trackFull = document.getElementById('trackFull');
    if (!trackFull) return;

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
        h3.innerHTML = '👤 <b>' + escapeHtml(currentUser.name) + '</b>님 (' + escapeHtml(currentUser.roleLabel || '회원') + ')';
      }
      var p = trackFull.querySelector('p');
      if (p) {
        if (prevProblem) {
          p.innerHTML = '📌 이전에 <b>' + prevProblem.stepDone + '/' + prevProblem.totalSteps + '단계</b>까지 풀이하셨습니다 (정답 <b>' + prevProblem.correct + '개</b>). 이어서 학습을 진행합니다.';
        } else {
          p.textContent = '인증된 회원 계정으로 풀이 기록이 안전하게 저장됩니다.';
        }
      }
    } else if (currentGuest) {
      if (studentNameInput) studentNameInput.value = currentGuest.name;
      var h3 = trackFull.querySelector('h3');
      if (h3) {
        h3.innerHTML = '🧑‍🎓 <b>' + escapeHtml(currentGuest.name) + '</b>님 (비회원 학습자)';
      }
      var p = trackFull.querySelector('p');
      if (p) {
        if (prevProblem) {
          p.innerHTML = '📌 이전에 <b>' + prevProblem.stepDone + '/' + prevProblem.totalSteps + '단계</b>까지 풀이하셨습니다 (정답 <b>' + prevProblem.correct + '개</b>). 이어서 계속 풀어보세요!';
        } else {
          p.textContent = '인식된 비회원 학습자 [' + currentGuest.name + ']님으로 풀이 기록이 저장됩니다.';
        }
      }
    } else {
      // 익명 상태인 경우: 간편 비밀번호(PIN) 입력 필드 추가
      if (formDiv && !document.getElementById('studentPin')) {
        var pinInput = document.createElement('input');
        pinInput.type = 'password';
        pinInput.id = 'studentPin';
        pinInput.placeholder = '간편비번 4자리 (선택)';
        pinInput.maxLength = 12;
        pinInput.style.cssText = 'background:#222a3d;color:#e8ecf5;border:1px solid #2e3850;border-radius:10px;padding:12px 14px;font-size:1.05rem;max-width:170px;text-align:center;outline:none;';
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
        tipDiv.style.cssText = 'font-size:0.83rem;color:#7cc4ff;margin-top:12px;line-height:1.5;max-width:460px;text-align:center;word-break:keep-all';
        tipDiv.innerHTML = '💡 <b>비회원 안내:</b> [이름]과 [간편 비밀번호]를 넣으시면 나중에 같은 문제에 오더라도 <b>동일 학습자로 자동 인식</b>되어 이전 풀이를 복원하고 <b>[내가 푼 문제]</b>를 모아볼 수 있습니다. (비번 미입력 시 익명 풀이)';
        formDiv.parentNode.insertBefore(tipDiv, formDiv.nextSibling);
      }
    }

    // 2. 하단 액션 버튼 행 (내가 푼 문제 모아보기 + 회원 전환 + 교사 수업 개설)
    var actionRow = document.createElement('div');
    actionRow.style.cssText = 'margin-top:22px;padding-top:18px;border-top:1px solid rgba(255,255,255,.14);display:flex;flex-direction:column;gap:12px;align-items:center;width:100%;max-width:540px;';

    var solvedCount = solvedList.length;
    var guestOrMember = currentUser || currentGuest;

    actionRow.innerHTML = 
      '<div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap;align-items:center">' +
        '<button type="button" id="btnMyProblemsInModal" style="background:rgba(94,234,212,.15);border:1px solid rgba(94,234,212,.35);color:#5eead4;border-radius:10px;padding:9px 16px;font-size:0.86rem;font-weight:700;cursor:pointer;transition:.15s;display:inline-flex;align-items:center;gap:6px">' +
          '📂 내가 푼 문제 모아보기' + (solvedCount > 0 ? ' (' + solvedCount + ')' : '') +
        '</button>' +
        (!currentUser ? 
          '<button type="button" id="btnUpgradeInModal" style="background:linear-gradient(90deg,rgba(124,196,255,.18),rgba(167,139,250,.18));border:1px solid rgba(124,196,255,.4);color:#c4b5fd;border-radius:10px;padding:9px 16px;font-size:0.86rem;font-weight:700;cursor:pointer;transition:.15s;display:inline-flex;align-items:center;gap:6px">' +
            '✨ 정식 회원 전환 / 가입' +
          '</button>' : '') +
        '<button type="button" id="btnDownloadOfflineInModal" style="background:rgba(56,189,248,.15);border:1px solid rgba(56,189,248,.45);color:#38bdf8;border-radius:10px;padding:9px 16px;font-size:0.86rem;font-weight:700;cursor:pointer;transition:.15s;display:inline-flex;align-items:center;gap:6px" title="인터넷 연결 없이 단독으로 풀 수 있는 HTML 파일로 저장">' +
          '📥 오프라인 저장' +
        '</button>' +
        '<button type="button" id="btnTeacherPreviewInModal" style="background:rgba(255,255,255,.06);color:#cbd5e1;border:1px solid rgba(255,255,255,.2);border-radius:10px;padding:9px 16px;font-size:0.86rem;cursor:pointer;transition:.15s;font-weight:600">' +
          '👀 가입 없이 문제 열람 & 자유 풀기' +
        '</button>' +
      '</div>' +
      '<div style="margin-top:4px">' +
        '<button type="button" id="btnTeacherOpenInModal" style="background:rgba(124,196,255,.16);color:#7cc4ff;border:1px solid rgba(124,196,255,.4);border-radius:10px;padding:8px 18px;font-size:0.84rem;font-weight:700;cursor:pointer;transition:.15s;display:inline-flex;align-items:center;gap:6px">' +
          '👩‍🏫 선생님 전용: 3초 수업 개설 (QR)' +
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

    document.getElementById('btnTeacherPreviewInModal').onclick = function() {
      trackFull.remove();
      window._studentName = '자유 학습자';
      if (window.sendProgress) window.sendProgress();
    };

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
        alert('이름 또는 출석번호를 입력하세요.');
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
    banner.style.cssText = 'background:linear-gradient(90deg, rgba(62,220,151,.15), rgba(56,189,248,.15));border:1px solid rgba(62,220,151,.4);border-radius:12px;padding:12px 18px;margin:14px 0 18px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;animation:fadeIn .3s ease;';

    var pct = prev.totalSteps > 0 ? Math.round((prev.stepDone / prev.totalSteps) * 100) : 100;
    var statusText = prev.completed 
      ? '🏆 <b>완주 완료!</b> (' + prev.stepDone + '/' + prev.totalSteps + '단계 모두 해결)'
      : '⚡ 이전에 <b>' + prev.stepDone + '/' + prev.totalSteps + '단계 (' + pct + '%)</b>까지 풀이하셨습니다.';

    banner.innerHTML = 
      '<div style="font-size:0.88rem;color:#eef2ff;display:flex;align-items:center;gap:8px">' +
        '<span>📌</span>' +
        '<div>' + statusText + ' (정답: <b>' + prev.correct + '</b>문항)</div>' +
      '</div>' +
      '<div style="display:flex;gap:8px">' +
        '<button type="button" onclick="MatheduAuth.showMyProblemsModal()" style="background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);color:#eef2ff;border-radius:8px;padding:5px 12px;font-size:0.8rem;cursor:pointer;font-weight:700">📂 내 서재</button>' +
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
    var wrap = document.querySelector('.wrap');
    if (!wrap) return;

    var banner = document.createElement('div');
    banner.className = 'teacher-class-banner';
    banner.style.cssText = 'background:linear-gradient(90deg, rgba(124,196,255,.14), rgba(167,139,250,.14));border:1px solid rgba(124,196,255,.35);border-radius:14px;padding:14px 18px;margin:16px 0 20px;display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;box-shadow:0 4px 20px rgba(0,0,0,.25);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px)';

    banner.innerHTML = 
      '<div>' +
        '<div style="font-weight:800;font-size:1rem;color:#7cc4ff;display:flex;align-items:center;gap:6px">' +
          '👩‍🏫 이 문제로 학급 수업을 시작할 수 있습니다' +
        '</div>' +
        '<div style="font-size:0.83rem;color:#aab4d4;margin-top:3px">' +
          '회원 로그인 후 3초 만에 수업 코드를 만들고, 교실 칠판에 학생용 대형 QR코드를 띄워보세요.' +
        '</div>' +
      '</div>' +
      '<button type="button" onclick="openClassCreatorModal(\'' + currentSlug + '\')" style="background:linear-gradient(90deg,#7cc4ff,#a78bfa);color:#0b1020;border:none;border-radius:10px;padding:10px 20px;font-size:0.9rem;font-weight:800;cursor:pointer;box-shadow:0 4px 14px rgba(124,196,255,.35);transition:.15s;display:inline-flex;align-items:center;gap:6px">' +
        '🚀 이 문제로 수업 열기 (QR / 대시보드)' +
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
    if (document.getElementById('floatClassBtn')) return;
    var floatBtn = document.createElement('button');
    floatBtn.id = 'floatClassBtn';
    floatBtn.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:9998;background:linear-gradient(135deg,#7cc4ff,#a78bfa);color:#0b1020;border:none;border-radius:30px;padding:12px 22px;font-size:0.92rem;font-weight:800;cursor:pointer;box-shadow:0 8px 24px rgba(0,0,0,.5), 0 0 20px rgba(124,196,255,.45);display:flex;align-items:center;gap:8px;transition:.2s';
    floatBtn.innerHTML = '🚀 이 문제로 수업 열기';
    floatBtn.title = '3초 만에 고유 수업 코드 및 빔프로젝터 QR 발급 (회원 전용)';

    floatBtn.onmouseover = function() { floatBtn.style.transform = 'translateY(-2px) scale(1.03)'; };
    floatBtn.onmouseout = function() { floatBtn.style.transform = 'translateY(0) scale(1)'; };
    floatBtn.onclick = function() { openClassCreatorModal(currentSlug); };

    document.body.appendChild(floatBtn);
  }

  function injectTopbarButtons() {
    var topbar = document.querySelector('.topbar') || document.querySelector('.navbar');
    if (!topbar) return;

    // 1. [📂 내가 푼 문제] 학습 서재 버튼
    if (!document.getElementById('btnMyLibraryTopbar')) {
      var libBtn = document.createElement('button');
      libBtn.id = 'btnMyLibraryTopbar';
      libBtn.className = 'tbtn navbtn';
      libBtn.style.cssText = 'background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.2);color:#eef2ff;font-weight:700;cursor:pointer;display:inline-flex;align-items:center;gap:6px;border-radius:10px;padding:6px 12px;font-size:0.84rem;transition:.15s;text-decoration:none;';
      
      function updateLibBtnText() {
        var count = (window.MatheduAuth && window.MatheduAuth.getSolvedProblems) ? window.MatheduAuth.getSolvedProblems().length : 0;
        libBtn.innerHTML = '📂 내가 푼 문제' + (count > 0 ? ' <span style="background:rgba(124,196,255,.25);color:#7cc4ff;padding:1px 6px;border-radius:10px;font-size:0.75rem">' + count + '</span>' : '');
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
      teacherBtn.style.cssText = 'background:linear-gradient(90deg,rgba(124,196,255,.2),rgba(167,139,250,.2));border:1px solid rgba(124,196,255,.4);color:#eef2ff;font-weight:700;cursor:pointer;display:inline-flex;align-items:center;gap:6px;border-radius:10px;padding:6px 12px;font-size:0.84rem;transition:.15s;';
      teacherBtn.innerHTML = '🚀 수업 열기 (QR)';
      teacherBtn.title = '선생님을 위한 3초 수업 생성 및 QR 발급 (회원 전용)';
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
      offlineBtn.style.cssText = 'background:rgba(56,189,248,.12);border:1px solid rgba(56,189,248,.4);color:#7cc4ff;font-weight:700;cursor:pointer;display:inline-flex;align-items:center;gap:6px;border-radius:10px;padding:6px 12px;font-size:0.84rem;transition:.15s;';
      offlineBtn.innerHTML = '📥 오프라인 저장';
      offlineBtn.title = '인터넷 없이 풀 수 있는 단독 오프라인 HTML 파일로 다운로드';
      offlineBtn.onclick = function(e) {
        if (window.downloadOfflineQuiz) {
          window.downloadOfflineQuiz(currentSlug);
        }
      };

      topbar.appendChild(offlineBtn);
    }
  }

  function patchSendProgress() {
    var originalSendProgress = window.sendProgress;
    window.sendProgress = function() {
      var name = (window._studentName || '').trim();
      if (!name) return;

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
      if (window.MatheduAuth && window.MatheduAuth.recordSolvedProblem) {
        var h1 = document.querySelector('h1');
        var pageTitle = h1 ? h1.textContent.trim() : (document.title || currentSlug);
        pageTitle = pageTitle.replace(/^📘\s*/, '').trim();

        window.MatheduAuth.recordSolvedProblem(currentSlug, {
          title: pageTitle,
          stepDone: done.length,
          totalSteps: total,
          correct: correct,
          completed: (total > 0 && done.length >= total)
        });
      }

      if (window._sheetsApiUrl) {
        fetch(window._sheetsApiUrl, {
          method: 'POST',
          mode: 'no-cors',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        }).catch(function(e) {
          console.warn('[mathedu] sendProgress error', e);
        });
      }
    };
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
        callback({ name: '선생님', roleLabel: '교사' });
      }
    });
  }

  // 교사용 수업 생성기 모달 (회원 전용)
  window.openClassCreatorModal = function(slug) {
    ensureAuth('수업 개설 및 배포', function(currentUser) {
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

    var teacherLabel = (currentUser && currentUser.name) ? (currentUser.name + ' (' + (currentUser.roleLabel || '회원') + ')') : '인증된 교사 회원';

    modal.innerHTML = 
      '<div style="background:#141833;border:1px solid rgba(124,196,255,.3);border-radius:20px;max-width:540px;width:100%;padding:28px;box-shadow:0 20px 60px rgba(0,0,0,.6);color:#eef2ff;font-family:system-ui,sans-serif;position:relative">' +
        '<button onclick="document.getElementById(\'classCreatorModal\').remove()" style="position:absolute;top:16px;right:18px;background:none;border:none;color:#9aa6c0;font-size:1.5rem;cursor:pointer">✕</button>' +
        '<div style="display:inline-flex;align-items:center;gap:6px;background:rgba(62,220,151,.15);color:#3ddc97;border-radius:20px;padding:4px 12px;font-size:.78rem;font-weight:700;margin-bottom:10px">✅ ' + escapeHtml(teacherLabel) + '</div>' +
        '<h2 style="margin:0 0 6px;font-size:1.4rem;background:linear-gradient(90deg,#7cc4ff,#a78bfa);-webkit-background-clip:text;background-clip:text;color:transparent">🚀 3초 만에 수업 개설하기</h2>' +
        '<p style="margin:0 0 20px;color:#9aa6c0;font-size:.88rem">선택하신 문제(<b>' + escapeHtml(slug) + '</b>)로 학생들에게 배포할 수업 코드가 생성되었습니다.</p>' +

        '<div style="background:#0d1020;border:1px solid rgba(255,255,255,.12);border-radius:14px;padding:16px;margin-bottom:18px">' +
          '<label style="display:block;font-size:.8rem;color:#7cc4ff;font-weight:700;margin-bottom:6px">수업 코드 / 방 이름 (원하는 이름으로 수정 가능)</label>' +
          '<div style="display:flex;gap:8px">' +
            '<input type="text" id="customRoomInput" value="' + defaultRoom + '" style="flex:1;background:#1a2038;border:1px solid #2e3850;border-radius:10px;padding:10px 14px;color:#fff;font-size:1.05rem;font-weight:700;text-transform:uppercase">' +
            '<button id="btnRegenRoom" style="background:#222a3d;border:1px solid #2e3850;color:#9aa6c0;border-radius:10px;padding:0 14px;cursor:pointer;font-size:.85rem">🔄 재발급</button>' +
          '</div>' +
        '</div>' +

        '<div style="display:grid;grid-template-columns:130px 1fr;gap:16px;align-items:center;background:#0d1020;border:1px solid rgba(255,255,255,.12);border-radius:14px;padding:16px;margin-bottom:20px">' +
          '<div style="text-align:center">' +
            '<img id="modalQrImg" src="" style="width:120px;height:120px;border-radius:10px;background:#fff;padding:6px;box-sizing:border-box" alt="QR Code">' +
            '<div style="font-size:.7rem;color:#9aa6c0;margin-top:4px">학생 스마트폰 스캔용</div>' +
          '</div>' +
          '<div>' +
            '<div style="font-size:.8rem;color:#9aa6c0;margin-bottom:4px">학생 접속 링크</div>' +
            '<div id="modalStudentUrlText" style="font-size:.82rem;color:#7cc4ff;word-break:break-all;background:#141833;padding:8px;border-radius:8px;border:1px solid #2e3850;margin-bottom:8px"></div>' +
            '<div style="display:flex;gap:6px;flex-wrap:wrap">' +
              '<button id="btnCopyStudentUrl" style="background:linear-gradient(90deg,#7cc4ff,#a78bfa);color:#0b1020;border:none;border-radius:8px;padding:8px 12px;font-size:.8rem;font-weight:700;cursor:pointer">📋 학생 링크 복사</button>' +
              '<button id="btnProjectorMode" style="background:#222a3d;color:#eef2ff;border:1px solid #2e3850;border-radius:8px;padding:8px 12px;font-size:.8rem;font-weight:700;cursor:pointer">🖥️ 칠판 빔프로젝터 QR</button>' +
            '</div>' +
          '</div>' +
        '</div>' +

        '<div style="display:flex;gap:10px;justify-content:flex-end">' +
          '<button onclick="document.getElementById(\'classCreatorModal\').remove()" style="background:transparent;color:#9aa6c0;border:1px solid #2e3850;border-radius:10px;padding:10px 18px;font-size:.9rem;cursor:pointer">닫기</button>' +
          '<button id="btnGoDashboard" style="background:linear-gradient(90deg,#3ddc97,#5eead4);color:#0b1020;border:none;border-radius:10px;padding:10px 22px;font-size:.95rem;font-weight:800;cursor:pointer;box-shadow:0 4px 16px rgba(61,220,151,.35)">📊 실시간 모니터링 열기 ➔</button>' +
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
          var prev = b.textContent;
          b.textContent = '✅ 복사 완료!';
          setTimeout(function() { b.textContent = prev; }, 1500);
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
      '<button onclick="document.getElementById(\'projectorScreenModal\').remove()" style="position:absolute;top:20px;right:24px;background:#222a3d;color:#fff;border:1px solid #2e3850;padding:8px 16px;border-radius:10px;font-size:1rem;cursor:pointer">✕ 전체화면 닫기</button>' +
      '<div style="display:inline-block;background:rgba(124,196,255,.2);color:#7cc4ff;border:1px solid rgba(124,196,255,.4);border-radius:30px;padding:6px 20px;font-size:1.1rem;font-weight:700;margin-bottom:14px">🏫 수업 코드: ' + escapeHtml(rId) + '</div>' +
      '<h1 style="font-size:2.4rem;margin:0 0 10px;background:linear-gradient(90deg,#7cc4ff,#a78bfa);-webkit-background-clip:text;background-clip:text;color:transparent">스마트폰 카메라로 QR 코드를 스캔하세요!</h1>' +
      '<p style="color:#9aa6c0;font-size:1.15rem;margin:0 0 24px">별도의 앱 설치나 회원가입 없이 즉시 문제가 열립니다.</p>' +
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
      btn.innerHTML = '⏳ 오프라인 다운로드 중...';
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
          btn.innerHTML = '✅ 다운로드 완료!';
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
              '📦 오프라인 단독 실행 파일 (인터넷 접속 없이 풀이 가능)' +
            '</div>' +
            '<div style="display:flex;align-items:center;gap:8px">' +
              '<button id="btnManualCheckUpdate" onclick="checkUpdateManual()" style="background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);color:#cbd5e1;padding:3px 12px;border-radius:14px;font-size:0.75rem;cursor:pointer;font-family:inherit">🔄 최신 버전 확인</button>' +
              '<span style="font-size:0.78rem;color:#94a3b8">min7014 mathedu</span>' +
            '</div>' +
          '</div>' +
          '<div style="font-size:1.15rem;font-weight:800;color:#ffffff;margin-bottom:6px">' + escapeHtml(quizTitle) + '</div>' +
          '<div style="font-size:0.86rem;color:#cbd5e1;line-height:1.5;margin-bottom:12px">' +
            '이 파일은 인터넷 연결 없이 웹 브라우저에서 언제든 풀 수 있는 <b>단독 오프라인 인터랙티브 수학 퀴즈</b>입니다.<br>' +
            '보기를 클릭하면 채점과 단계별 상세 해설이 열리며, 점수가 자동 계산됩니다.' +
          '</div>' +
          '<div id="matheduUpdateAlertSlot" style="display:none;margin-bottom:12px;padding:12px 16px;background:rgba(253,230,138,.14);border:1.5px solid #fde68a;border-radius:12px;color:#fde68a;font-size:0.88rem;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px">' +
            '<div style="display:flex;align-items:center;gap:8px">' +
              '<span style="font-size:1.1rem">🔔</span>' +
              '<span><b>이 문제의 최신 업데이트 버전이 있습니다!</b> (새 버전으로 저장 후 풀이 가능)</span>' +
            '</div>' +
            '<button onclick="openUpdateModal()" style="background:#fde68a;color:#0b1020;border:none;padding:6px 14px;border-radius:8px;font-weight:800;font-size:0.82rem;cursor:pointer">업데이트 보기 ➔</button>' +
          '</div>' +
          '<div style="background:rgba(15,23,42,.7);border:1px solid rgba(255,255,255,.14);border-radius:12px;padding:12px 16px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px">' +
            '<div style="font-size:0.85rem;color:#e2e8f0;word-break:break-all">' +
              '<span style="color:#7cc4ff;font-weight:700">🌐 온라인 원본 문제 주소:</span><br>' +
              '<a href="' + originalOnlineUrl + '" target="_blank" rel="noopener" style="color:#38bdf8;font-weight:700;text-decoration:underline;font-family:monospace">' + originalOnlineUrl + '</a>' +
            '</div>' +
            '<div style="display:flex;gap:8px">' +
              '<a href="' + originalOnlineUrl + '" target="_blank" rel="noopener" style="background:linear-gradient(90deg,#38bdf8,#818cf8);color:#0b1020;padding:8px 16px;border-radius:8px;font-size:0.82rem;font-weight:800;text-decoration:none">🌐 온라인 원본 열기 ➔</a>' +
              '<a href="https://min7014.github.io/" target="_blank" rel="noopener" style="background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);color:#eef2ff;padding:8px 14px;border-radius:8px;font-size:0.82rem;font-weight:700;text-decoration:none">🏛️ min7014 자료실</a>' +
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
              '<div class="mathedu-update-badge">🔔 최신 업데이트 감지</div>' +
              '<button class="mathedu-update-close-btn" onclick="closeUpdateModal()">✕</button>' +
            '</div>' +
            '<h2 style="margin:0 0 8px;font-size:1.35rem;background:linear-gradient(90deg,#7cc4ff,#a78bfa);-webkit-background-clip:text;background-clip:text;color:transparent;font-weight:800">✨ 이 문제의 최신 버전이 있습니다!</h2>' +
            '<p style="margin:0 0 16px;color:#cbd5e1;font-size:0.9rem;line-height:1.55">선생님께서 문제의 해설 보강, 질문 개선, 또는 새로운 인터랙티브 디딤돌 단계를 업데이트하셨습니다.<br>새로운 버전을 다운로드하여 저장 후 풀이하시거나, 지금 바로 현재 버전으로 계속 푸실 수 있습니다.</p>' +
            '<div class="mathedu-ver-box">' +
              '<div class="mathedu-ver-item cur"><span class="mathedu-ver-lbl">현재 내 오프라인 버전</span><b id="lblCurrentVer">-</b></div>' +
              '<div style="color:#7cc4ff;font-size:1.2rem;font-weight:800">➔</div>' +
              '<div class="mathedu-ver-item new"><span class="mathedu-ver-lbl">🚀 온라인 최신 버전</span><b id="lblLatestVer">-</b></div>' +
            '</div>' +
            '<div class="mathedu-update-btn-row">' +
              '<button id="btnDownloadUpdate" class="mathedu-btn-primary" onclick="downloadLatestOfflineVersion()">📥 새 버전 내려받아서 풀기 (저장)</button>' +
              '<button class="mathedu-btn-sec" onclick="continueCurrentVersion()">📝 그냥 현재 버전으로 풀기</button>' +
              '<a id="btnOpenOnlineLatest" href="' + originalOnlineUrl + '" target="_blank" rel="noopener" class="mathedu-btn-link">🌐 온라인 최신판 웹으로 바로 열기 ➔</a>' +
            '</div>' +
            '<div id="updateDownloadSuccess" style="display:none;margin-top:16px;background:rgba(94,234,212,.15);border:1px solid #5eead4;border-radius:12px;padding:14px;text-align:left">' +
              '<div style="font-weight:800;color:#5eead4;margin-bottom:4px">🎉 최신 버전 다운로드 완료!</div>' +
              '<div style="font-size:0.86rem;color:#e2e8f0;line-height:1.5">다운로드 폴더에 최신 문제 파일이 저장되었습니다. 새로 저장된 파일을 브라우저로 열어 풀이하시거나, 온라인 최신 페이지로 바로 이동하실 수 있습니다.</div>' +
              '<div style="margin-top:12px;display:flex;gap:8px">' +
                '<a href="' + originalOnlineUrl + '" target="_blank" rel="noopener" style="background:#5eead4;color:#0b1020;padding:7px 16px;border-radius:8px;font-size:0.84rem;font-weight:800;text-decoration:none">🌐 온라인 최신판 열기</a>' +
                '<button onclick="closeUpdateModal()" style="background:transparent;border:1px solid #5eead4;color:#5eead4;padding:7px 16px;border-radius:8px;font-size:0.84rem;cursor:pointer;font-weight:700">✕ 닫고 현재 화면 풀기</button>' +
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
            'window.downloadLatestOfflineVersion=async function(){var b=document.getElementById("btnDownloadUpdate");if(b){b.innerHTML="⏳ 최신 버전 다운로드 중...";b.style.pointerEvents="none";}' +
            'try{var r=await fetch(du+"?_t="+Date.now());if(!r.ok)throw new Error("HTTP "+r.status);var bl=await r.blob();var u=URL.createObjectURL(bl);var a=document.createElement("a");a.href=u;a.download="mathedu_"+s+"_offline_latest.html";document.body.appendChild(a);a.click();setTimeout(function(){a.remove();URL.revokeObjectURL(u);},500);if(b)b.innerHTML="✅ 새 버전 저장 완료!";var bx=document.getElementById("updateDownloadSuccess");if(bx)bx.style.display="block";}' +
            'catch(e){alert("다운로드 실패: "+e.message);window.open(ou,"_blank");if(b){b.innerHTML="📥 다시 시도";b.style.pointerEvents="";}}};' +
            'window.checkUpdateManual=function(){var b=document.getElementById("btnManualCheckUpdate");if(b)b.innerHTML="⏳ 확인 중...";chk(true);};' +
            'function showUp(inf){window._serverUpdateInfo=inf;var sl=document.getElementById("matheduUpdateAlertSlot");if(sl)sl.style.display="flex";var bm=document.getElementById("btnManualCheckUpdate");if(bm){bm.innerHTML="✨ 새 버전 있음!";bm.style.background="rgba(253,230,138,.25)";bm.style.color="#fde68a";bm.style.borderColor="#fde68a";}' +
            'var dis=false;try{dis=sessionStorage.getItem("mathedu_update_dismissed_"+s)==="true";}catch(e){}if(!dis)openUpdateModal();}' +
            'function chk(man){if(!navigator.onLine){if(man)alert("현재 오프라인 상태입니다.");var b=document.getElementById("btnManualCheckUpdate");if(b)b.innerHTML="📡 오프라인";return;}' +
            'fetch(vu+"?_t="+Date.now(),{cache:"no-cache"}).then(function(r){if(!r.ok)throw new Error();return r.json();}).then(function(d){' +
            'var it=d&&d.quizzes&&d.quizzes[s];if(it&&it.updated_at&&(new Date(it.updated_at).getTime()-new Date(bt).getTime()>60000)){showUp(it);}else{hUp(man);}}).catch(function(){' +
            'fetch(du+"?_t="+Date.now(),{method:"HEAD",cache:"no-cache"}).then(function(r){var lm=r.headers.get("Last-Modified");if(lm&&(new Date(lm).getTime()-new Date(bt).getTime()>120000)){showUp({updated_at:new Date(lm).toISOString()});}else{hUp(man);}}).catch(function(){hUp(man);});});}' +
            'function hUp(man){var b=document.getElementById("btnManualCheckUpdate");if(b){b.innerHTML="✅ 최신 버전";b.style.color="#5eead4";b.style.borderColor="rgba(94,234,212,.4)";}if(man)alert("현재 문제 파일이 최신 버전입니다.");}' +
            'setTimeout(function(){chk(false);},1000);' +
            'window.addEventListener("online",function(){chk(false);});' +
          '})();' +
        '</script>';

      var dummy = document.createElement('div');
      dummy.innerHTML = updaterHtml;
      while (dummy.firstChild) {
        docClone.body.appendChild(dummy.firstChild);
      }

      var fullHtml = '<!DOCTYPE html>\n<html lang="ko">\n' + docClone.innerHTML + '\n</html>';
      var blob = new Blob([fullHtml], { type: 'text/html;charset=utf-8' });
      triggerBlobDownload(blob, 'mathedu_' + slug + '_offline.html');

      if (btn) {
        btn.innerHTML = '✅ 다운로드 완료!';
        setTimeout(function() { btn.innerHTML = origText; btn.style.pointerEvents = ''; }, 2500);
      }
    } catch(err) {
      alert('오프라인 파일 다운로드 생성 중 오류: ' + err.message);
      if (btn) {
        btn.innerHTML = origText;
        btn.style.pointerEvents = '';
      }
    }
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initRoom);
  } else {
    initRoom();
  }
})();
