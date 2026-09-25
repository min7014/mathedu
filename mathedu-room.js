/**
 * mathedu-room.js — 무가입 교사-학생 실시간 수업 연동 모듈 (v2.0)
 * 
 * 1. 학생: ?room=ROOM_ID 링크 접속 시 자동 수업 참여,
 *    이름 입력 및 실시간 풀이 진행 시 [ROOM_ID] 태그 및 room_id 동시 전송.
 * 2. 교사: 각 문제 화면 어디서나(시작 모달, 문제 상단 배너, 플로팅 버튼, 상단바)
 *    클릭 한 번으로 3초 만에 수업 코드, 학생용 링크, 칠판 빔프로젝터용 대형 QR 발급.
 */
(function() {
  var urlParams = new URLSearchParams(window.location.search);
  var roomId = (urlParams.get('room') || '').trim();
  window._roomId = roomId;

  // 퀴즈 slug 추출
  var currentSlug = window.location.pathname.split('/').pop().replace('.html', '') || 'quiz';

  function initRoom() {
    // 1. 학생이 특정 방에 참여 중인 경우 UI 표시
    if (roomId) {
      applyStudentRoomUI(roomId);
    }

    // 2. 시작 모달(#trackFull)에 선생님 전용 빠른 액션 추가
    enhanceTrackFullModal();

    // 3. 문제 페이지 상단에 눈에 띄는 [이 문제로 수업 개설] 배너 삽입
    injectProblemPageBanner();

    // 4. 스크롤 중에도 언제든 누를 수 있는 플로팅 [🚀 이 문제로 수업 열기] 버튼
    injectFloatingClassButton();

    // 5. 상단바 tbtn에 버튼 추가
    injectTeacherTopbarButton();

    // 6. sendProgress 가로채기 (room_id 및 [ROOM_ID] 태그 주입)
    patchSendProgress();
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

    var topbar = document.querySelector('.topbar');
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

    var teacherRow = document.createElement('div');
    teacherRow.style.cssText = 'margin-top:22px;padding-top:18px;border-top:1px solid rgba(255,255,255,.14);display:flex;gap:10px;justify-content:center;flex-wrap:wrap;align-items:center';

    teacherRow.innerHTML = 
      '<button type="button" id="btnTeacherOpenInModal" style="background:rgba(124,196,255,.18);color:#7cc4ff;border:1px solid rgba(124,196,255,.45);border-radius:10px;padding:9px 18px;font-size:0.86rem;font-weight:700;cursor:pointer;transition:.15s;display:inline-flex;align-items:center;gap:6px">' +
        '👩‍🏫 선생님이신가요? 3초 만에 수업 개설 (QR)' +
      '</button>' +
      '<button type="button" id="btnTeacherPreviewInModal" style="background:transparent;color:#9aa6c0;border:1px solid #2e3850;border-radius:10px;padding:9px 16px;font-size:0.86rem;cursor:pointer;transition:.15s">' +
        '👀 문제 먼저 둘러보기' +
      '</button>';

    var formDiv = trackFull.querySelector('div');
    if (formDiv) {
      formDiv.parentNode.insertBefore(teacherRow, formDiv.nextSibling);
    } else {
      trackFull.appendChild(teacherRow);
    }

    document.getElementById('btnTeacherOpenInModal').onclick = function() {
      trackFull.remove();
      openClassCreatorModal(currentSlug);
    };

    document.getElementById('btnTeacherPreviewInModal').onclick = function() {
      trackFull.remove();
      window._studentName = '선생님(미리보기)';
    };
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
          '회원가입 없이 3초 만에 수업 코드를 만들고, 교실 칠판에 학생용 대형 QR코드를 띄워보세요.' +
        '</div>' +
      '</div>' +
      '<button type="button" onclick="openClassCreatorModal(\'' + currentSlug + '\')" style="background:linear-gradient(90deg,#7cc4ff,#a78bfa);color:#0b1020;border:none;border-radius:10px;padding:10px 20px;font-size:0.9rem;font-weight:800;cursor:pointer;box-shadow:0 4px 14px rgba(124,196,255,.35);transition:.15s;display:inline-flex;align-items:center;gap:6px">' +
        '🚀 이 문제로 수업 열기 (QR / 대시보드)' +
      '</button>';

    // h1 다음 또는 score 다음 삽입
    var h1 = wrap.querySelector('h1');
    if (h1 && h1.nextSibling) {
      wrap.insertBefore(banner, h1.nextSibling);
    } else {
      var topbar = wrap.querySelector('.topbar');
      if (topbar && topbar.nextSibling) {
        wrap.insertBefore(banner, topbar.nextSibling);
      }
    }
  }

  function injectFloatingClassButton() {
    var floatBtn = document.createElement('button');
    floatBtn.id = 'floatClassBtn';
    floatBtn.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:9998;background:linear-gradient(135deg,#7cc4ff,#a78bfa);color:#0b1020;border:none;border-radius:30px;padding:12px 22px;font-size:0.92rem;font-weight:800;cursor:pointer;box-shadow:0 8px 24px rgba(0,0,0,.5), 0 0 20px rgba(124,196,255,.45);display:flex;align-items:center;gap:8px;transition:.2s';
    floatBtn.innerHTML = '🚀 이 문제로 수업 열기';
    floatBtn.title = '3초 만에 고유 수업 코드 및 빔프로젝터 QR 발급';

    floatBtn.onmouseover = function() { floatBtn.style.transform = 'translateY(-2px) scale(1.03)'; };
    floatBtn.onmouseout = function() { floatBtn.style.transform = 'translateY(0) scale(1)'; };
    floatBtn.onclick = function() { openClassCreatorModal(currentSlug); };

    document.body.appendChild(floatBtn);
  }

  function injectTeacherTopbarButton() {
    var topbar = document.querySelector('.topbar');
    if (!topbar) return;

    var teacherBtn = document.createElement('button');
    teacherBtn.className = 'tbtn';
    teacherBtn.style.cssText = 'background:linear-gradient(90deg,rgba(124,196,255,.2),rgba(167,139,250,.2));border-color:rgba(124,196,255,.4);color:#eef2ff;font-weight:700;cursor:pointer;display:inline-flex;align-items:center;gap:6px;';
    teacherBtn.innerHTML = '🚀 수업 열기 (QR)';
    teacherBtn.title = '선생님을 위한 3초 수업 생성 및 QR 발급';
    teacherBtn.onclick = function() {
      openClassCreatorModal(currentSlug);
    };

    var copyBtn = document.getElementById('copyBtn');
    if (copyBtn && copyBtn.nextSibling) {
      topbar.insertBefore(teacherBtn, copyBtn.nextSibling);
    } else {
      topbar.appendChild(teacherBtn);
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

  // 교사용 수업 생성기 모달 (3초 룸 생성 + QR + 대시보드 링크)
  window.openClassCreatorModal = function(slug) {
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

    modal.innerHTML = 
      '<div style="background:#141833;border:1px solid rgba(124,196,255,.3);border-radius:20px;max-width:540px;width:100%;padding:28px;box-shadow:0 20px 60px rgba(0,0,0,.6);color:#eef2ff;font-family:system-ui,sans-serif;position:relative">' +
        '<button onclick="document.getElementById(\'classCreatorModal\').remove()" style="position:absolute;top:16px;right:18px;background:none;border:none;color:#9aa6c0;font-size:1.5rem;cursor:pointer">✕</button>' +
        '<div style="display:inline-flex;align-items:center;gap:6px;background:rgba(124,196,255,.15);color:#7cc4ff;border-radius:20px;padding:4px 12px;font-size:.78rem;font-weight:700;margin-bottom:10px">👩‍🏫 교사용 · 가입/로그인 불필요</div>' +
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
      var dashboardUrl = origin + basePath + '/dashboard-static.html?room=' + encodeURIComponent(r);
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
  };

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
    } catch(e) {}
  }

  function escapeHtml(s) {
    return String(s || '').replace(/[&<>"']/g, function(c) {
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initRoom);
  } else {
    initRoom();
  }
})();
