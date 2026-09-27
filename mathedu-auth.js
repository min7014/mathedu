/**
 * mathedu-auth.js — 수학 mathedu 회원/비회원 통합 인증 및 학습 서재 모듈
 * 
 * 1. 회원가입 및 정식 로그인:
 *    - 교사, 강사, 연구원 및 정회원 가입/로그인 (SHA-256 암호화 해싱, 세션 유지)
 *    - [문제 만들기(create.html)] 및 [학급 수업 배포(mathedu-room.js, dashboard)] 전용 권한
 * 2. 비회원 간편 식별 시스템 (이름 + 간편 비밀번호):
 *    - 비회원이라도 고유한 [이름]과 [간편 비밀번호(4자리)]를 입력하여 동일 사용자 인식
 *    - 나중에 같은 문제에 다시 오거나 다른 기기에서 내 기록 복원
 * 3. 내가 푼 문제 모아보기 (학습 서재):
 *    - 풀었던 모든 문항의 진행 단계, 정답률, 완주 상태를 한눈에 모아보고 이어서 풀기 지원
 * 4. 정식 회원가입 자연스러운 전환:
 *    - 비회원 상태에서 푼 문제 기록을 단 1개도 유실하지 않고 100% 승계하여 정식 회원으로 10초 만에 업그레이드
 */

(function(window) {
  'use strict';

  var USERS_KEY = 'mathedu_users_db';
  var SESSION_KEY = 'mathedu_current_user';
  var GUESTS_KEY = 'mathedu_guests_db';
  var CURRENT_GUEST_KEY = 'mathedu_current_guest';
  var DEVICE_SOLVED_KEY = 'mathedu_device_solved_cache';

  // 기본 시드 계정 (시연 및 테스트용)
  var DEFAULT_SEED_USERS = [
    {
      username: 'teacher',
      passwordHash: '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', // 'math1234'
      name: '민은기 선생님',
      email: 'min7014@mathedu.kr',
      org: '수학교육연구소',
      role: 'teacher',
      roleLabel: '수학교사',
      createdAt: '2026-09-01T00:00:00.000Z',
      solvedProblems: {}
    }
  ];

  // SHA-256 암호화 해시 함수 (브라우저 SubtleCrypto + 폴백)
  async function sha256(message) {
    if (!message) return '';
    if (window.crypto && window.crypto.subtle && window.crypto.subtle.digest) {
      try {
        var msgBuffer = new TextEncoder().encode(String(message));
        var hashBuffer = await window.crypto.subtle.digest('SHA-256', msgBuffer);
        var hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(function(b) { return b.toString(16).padStart(2, '0'); }).join('');
      } catch (e) {}
    }
    // 폴백 간단 해시
    var hash = 0;
    var str = String(message);
    for (var i = 0; i < str.length; i++) {
      var chr = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + chr;
      hash |= 0;
    }
    return 'fallback_' + Math.abs(hash).toString(16);
  }

  // 사용자(정회원) DB 관리
  function getUsers() {
    try {
      var raw = localStorage.getItem(USERS_KEY);
      if (!raw) {
        localStorage.setItem(USERS_KEY, JSON.stringify(DEFAULT_SEED_USERS));
        return DEFAULT_SEED_USERS.slice();
      }
      return JSON.parse(raw) || [];
    } catch (e) {
      return DEFAULT_SEED_USERS.slice();
    }
  }

  function saveUsers(users) {
    try {
      localStorage.setItem(USERS_KEY, JSON.stringify(users));
    } catch (e) {
      console.error('[mathedu-auth] 사용자 저장 실패:', e);
    }
  }

  // 정회원 세션 관리
  function getSession() {
    try {
      var raw = localStorage.getItem(SESSION_KEY) || sessionStorage.getItem(SESSION_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (e) {
      return null;
    }
  }

  function setSession(user, remember) {
    try {
      var safeUser = {
        username: user.username,
        name: user.name || user.username,
        email: user.email || '',
        org: user.org || '',
        role: user.role || 'member',
        roleLabel: user.roleLabel || '회원',
        solvedProblems: user.solvedProblems || {},
        loginTime: new Date().toISOString()
      };
      var str = JSON.stringify(safeUser);
      localStorage.setItem(SESSION_KEY, str);
      sessionStorage.setItem(SESSION_KEY, str);
      window.dispatchEvent(new CustomEvent('mathedu:auth-changed', { detail: safeUser }));
      updateNavAuthUI();
      return safeUser;
    } catch (e) {
      console.error('[mathedu-auth] 세션 저장 실패:', e);
      return null;
    }
  }

  function clearSession() {
    localStorage.removeItem(SESSION_KEY);
    sessionStorage.removeItem(SESSION_KEY);
    window.dispatchEvent(new CustomEvent('mathedu:auth-changed', { detail: null }));
    updateNavAuthUI();
  }

  // 비회원 게스트 DB 관리 (이름 + 간편 비번 식별자)
  function getGuests() {
    try {
      var raw = localStorage.getItem(GUESTS_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (e) {
      return {};
    }
  }

  function saveGuests(guests) {
    try {
      localStorage.setItem(GUESTS_KEY, JSON.stringify(guests));
    } catch (e) {}
  }

  function getCurrentGuest() {
    try {
      var raw = localStorage.getItem(CURRENT_GUEST_KEY) || sessionStorage.getItem(CURRENT_GUEST_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (e) {
      return null;
    }
  }

  function setCurrentGuest(guest) {
    try {
      if (guest) {
        var str = JSON.stringify(guest);
        localStorage.setItem(CURRENT_GUEST_KEY, str);
        sessionStorage.setItem(CURRENT_GUEST_KEY, str);
      } else {
        localStorage.removeItem(CURRENT_GUEST_KEY);
        sessionStorage.removeItem(CURRENT_GUEST_KEY);
      }
      window.dispatchEvent(new CustomEvent('mathedu:guest-changed', { detail: guest }));
      updateNavAuthUI();
    } catch (e) {}
  }

  // 로컬 기기 풀이 캐시
  function getDeviceSolvedCache() {
    try {
      var raw = localStorage.getItem(DEVICE_SOLVED_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (e) {
      return {};
    }
  }

  function saveDeviceSolvedCache(cache) {
    try {
      localStorage.setItem(DEVICE_SOLVED_KEY, JSON.stringify(cache));
    } catch (e) {}
  }

  // 모듈 객체
  var MatheduAuth = {
    // 1. 상태 조회
    isLoggedIn: function() {
      return !!getSession();
    },

    getCurrentUser: function() {
      return getSession();
    },

    isGuestIdentified: function() {
      return !!getCurrentGuest();
    },

    getCurrentGuest: function() {
      return getCurrentGuest();
    },

    // 현재 사용자(정회원 우선, 없으면 비회원 게스트, 없으면 null)의 표시 이름
    getActiveDisplayName: function() {
      var u = getSession();
      if (u) return u.name;
      var g = getCurrentGuest();
      if (g) return g.name;
      return '';
    },

    // 2. 비회원 간편 식별 (이름 + 간편비밀번호)
    loginGuest: async function(nameInput, pinInput) {
      var name = (nameInput || '').trim();
      var pin = (pinInput || '').trim();

      if (!name) {
        return { success: false, message: '이름(또는 닉네임)을 입력해 주세요.' };
      }
      if (!pin || pin.length < 3) {
        return { success: false, message: '간편 비밀번호를 3자리 이상(권장 4자리) 입력해 주세요.' };
      }

      var guests = getGuests();
      var key = name.toLowerCase();
      var pHash = await sha256(pin);

      if (guests[key]) {
        var existing = guests[key];
        if (existing.pinHash !== pHash) {
          return {
            success: false,
            message: '학습자 [' + name + ']님으로 등록된 비밀번호가 일치하지 않습니다. 올바른 비밀번호를 입력해 주세요.'
          };
        }
        existing.lastActive = new Date().toISOString();
        saveGuests(guests);
        setCurrentGuest(existing);
        showToast('반갑습니다, ' + name + '님! 이전 학습 기록이 복원되었습니다.', '🧑‍🎓');
        return {
          success: true,
          isNew: false,
          guest: existing,
          message: '이전 학습 기록이 복원되었습니다.'
        };
      } else {
        // 새 비회원 사용자 생성
        var newGuest = {
          name: name,
          pinHash: pHash,
          createdAt: new Date().toISOString(),
          lastActive: new Date().toISOString(),
          solvedProblems: {}
        };
        // 기존 기기 풀이 캐시가 있다면 연동
        var devCache = getDeviceSolvedCache();
        for (var slug in devCache) {
          newGuest.solvedProblems[slug] = devCache[slug];
        }
        guests[key] = newGuest;
        saveGuests(guests);
        setCurrentGuest(newGuest);
        showToast('새 학습자로 인식되었습니다: ' + name + '님', '🌱');
        return {
          success: true,
          isNew: true,
          guest: newGuest,
          message: '새로운 학습자로 등록되었습니다.'
        };
      }
    },

    logoutGuest: function() {
      setCurrentGuest(null);
      showToast('비회원 식별이 해제되었습니다.', '👋');
    },

    // 3. 푼 문제 기록 저장 (회원/비회원 공통)
    recordSolvedProblem: function(slug, data) {
      if (!slug) return;
      var item = {
        slug: slug,
        title: data.title || slug,
        stepDone: data.stepDone || 1,
        totalSteps: data.totalSteps || 5,
        correct: (typeof data.correct === 'number') ? data.correct : 0,
        completed: !!data.completed || (data.stepDone >= (data.totalSteps || 5)),
        lastUpdated: new Date().toISOString()
      };

      // 1) 기기 캐시 저장
      var devCache = getDeviceSolvedCache();
      devCache[slug] = item;
      saveDeviceSolvedCache(devCache);

      // 2) 비회원 게스트 저장
      var guest = getCurrentGuest();
      if (guest) {
        if (!guest.solvedProblems) guest.solvedProblems = {};
        guest.solvedProblems[slug] = item;
        guest.lastActive = new Date().toISOString();
        setCurrentGuest(guest);

        var guests = getGuests();
        if (guests[guest.name.toLowerCase()]) {
          guests[guest.name.toLowerCase()] = guest;
          saveGuests(guests);
        }
      }

      // 3) 정회원 저장
      var user = getSession();
      if (user) {
        var users = getUsers();
        var uIdx = users.findIndex(function(u) { return u.username === user.username; });
        if (uIdx !== -1) {
          if (!users[uIdx].solvedProblems) users[uIdx].solvedProblems = {};
          users[uIdx].solvedProblems[slug] = item;
          saveUsers(users);
          user.solvedProblems = users[uIdx].solvedProblems;
          setSession(user, true);
        }
      }

      window.dispatchEvent(new CustomEvent('mathedu:solved-updated', { detail: item }));
      updateNavAuthUI();
    },

    // 내가 푼 전체 문제 목록 반환 (정렬: 최근 풀이순)
    getSolvedProblems: function() {
      var map = {};
      // 기기 캐시 우선 반영
      var dev = getDeviceSolvedCache();
      for (var k in dev) map[k] = dev[k];

      // 게스트 기록 병합
      var guest = getCurrentGuest();
      if (guest && guest.solvedProblems) {
        for (var k in guest.solvedProblems) map[k] = guest.solvedProblems[k];
      }

      // 정회원 기록 병합
      var user = getSession();
      if (user && user.solvedProblems) {
        for (var k in user.solvedProblems) map[k] = user.solvedProblems[k];
      }

      var list = Object.values(map);
      list.sort(function(a, b) {
        return new Date(b.lastUpdated || 0) - new Date(a.lastUpdated || 0);
      });
      return list;
    },

    // 4. 정회원 가입 및 전환
    signUp: async function(data) {
      var username = (data.username || '').trim().toLowerCase();
      var password = (data.password || '').trim();
      var name = (data.name || '').trim();
      var email = (data.email || '').trim();
      var org = (data.org || '').trim();
      var role = data.role || 'teacher';

      if (!username || username.length < 3) {
        return { success: false, message: '아이디는 3자 이상 입력해 주세요.' };
      }
      if (!password || password.length < 4) {
        return { success: false, message: '비밀번호는 4자 이상 입력해 주세요.' };
      }
      if (!name) {
        return { success: false, message: '이름(또는 닉네임)을 입력해 주세요.' };
      }

      var users = getUsers();
      var exists = users.some(function(u) { return u.username === username; });
      if (exists) {
        return { success: false, message: '이미 존재하는 아이디입니다. 다른 아이디를 사용해 주세요.' };
      }

      var roleMap = {
        'teacher': '수학교사',
        'instructor': '학원·전문강사',
        'researcher': '수학연구원',
        'preteacher': '예비교사·대학생',
        'member': '정회원'
      };

      // 기존 비회원 시절 푼 문제 기록들을 그대로 정회원 계정으로 승계
      var solvedToMigrate = {};
      var guest = getCurrentGuest();
      if (guest && guest.solvedProblems) {
        for (var k in guest.solvedProblems) solvedToMigrate[k] = guest.solvedProblems[k];
      }
      var devCache = getDeviceSolvedCache();
      for (var k in devCache) {
        if (!solvedToMigrate[k]) solvedToMigrate[k] = devCache[k];
      }

      var pwdHash = await sha256(password);
      var newUser = {
        username: username,
        passwordHash: pwdHash,
        name: name,
        email: email,
        org: org,
        role: role,
        roleLabel: roleMap[role] || '회원',
        createdAt: new Date().toISOString(),
        solvedProblems: solvedToMigrate
      };

      users.push(newUser);
      saveUsers(users);

      // 자동 로그인 및 게스트 세션 정리
      setCurrentGuest(null);
      setSession(newUser, true);
      return {
        success: true,
        user: newUser,
        migratedCount: Object.keys(solvedToMigrate).length,
        message: '환영합니다! 회원가입이 완료되었습니다.'
      };
    },

    // 비회원 -> 정식 회원 전환
    convertGuestToMember: async function(data) {
      return await MatheduAuth.signUp(data);
    },

    logIn: async function(usernameInput, passwordInput) {
      var username = (usernameInput || '').trim().toLowerCase();
      var password = (passwordInput || '').trim();

      if (!username || !password) {
        return { success: false, message: '아이디와 비밀번호를 모두 입력해 주세요.' };
      }

      var users = getUsers();
      var pwdHash = await sha256(password);

      var matched = users.find(function(u) {
        return (u.username === username || (u.email && u.email.toLowerCase() === username)) &&
               (u.passwordHash === pwdHash || (u.password && u.password === password));
      });

      if (!matched) {
        return { success: false, message: '아이디 또는 비밀번호가 일치하지 않습니다.' };
      }

      // 기존 비회원 게스트 풀이 기록이 있다면 정회원 계정에 안전 병합
      var guest = getCurrentGuest();
      if (guest && guest.solvedProblems) {
        if (!matched.solvedProblems) matched.solvedProblems = {};
        for (var k in guest.solvedProblems) {
          if (!matched.solvedProblems[k]) matched.solvedProblems[k] = guest.solvedProblems[k];
        }
        saveUsers(users);
        setCurrentGuest(null);
      }

      var sessionUser = setSession(matched, true);
      return { success: true, user: sessionUser, message: '로그인되었습니다.' };
    },

    logOut: function() {
      clearSession();
      showToast('로그아웃되었습니다.', '👋');
      setTimeout(function() {
        if (window.location.pathname.indexOf('create.html') !== -1) {
          window.location.reload();
        }
      }, 500);
    },

    // 5. 권한 보호 가드
    requireAuth: function(actionName, onAllowed) {
      if (MatheduAuth.isLoggedIn()) {
        if (typeof onAllowed === 'function') onAllowed(getSession());
        return true;
      }

      var descMap = {
        '문제 출제': '어려운 고난도 문제를 올리고 AI 5~8단계 인터랙티브 빌드업 퀴즈를 자동 제작·배포하는 기능은 <b>mathedu 회원 전용</b>입니다.',
        '문제 배포': '학생들에게 배포할 고유 수업 코드 발급, 칠판 빔프로젝터 QR 생성, 실시간 교실 모니터링은 <b>mathedu 회원(교사) 전용</b>입니다.',
        '수업 배포': '학생 참여 링크 복사 및 대형 빔프로젝터 QR 코드를 띄우려면 <b>mathedu 회원 로그인</b>이 필요합니다.'
      };

      MatheduAuth.showAuthModal({
        title: '🔒 회원 전용: ' + (actionName || '권한 안내'),
        desc: descMap[actionName] || '이 기능은 <b>mathedu 회원</b>만 이용하실 수 있습니다. 10초 만에 무료 회원가입 후 즉시 이용하세요.',
        actionName: actionName,
        onSuccess: function(user) {
          showToast('회원 인증이 완료되었습니다: ' + user.name + '님', '✅');
          if (typeof onAllowed === 'function') onAllowed(user);
        }
      });
      return false;
    },

    // 6. UI 모달: [📂 내가 푼 문제 모아보기 (학습 서재)]
    showMyProblemsModal: function() {
      var existing = document.getElementById('matheduProblemsModal');
      if (existing) existing.remove();

      var user = getSession();
      var guest = getCurrentGuest();
      var solvedList = MatheduAuth.getSolvedProblems();

      var completedCount = solvedList.filter(function(p) { return p.completed; }).length;
      var totalStepsSum = 0;
      var correctSum = 0;
      solvedList.forEach(function(p) {
        totalStepsSum += (p.stepDone || 0);
        correctSum += (p.correct || 0);
      });
      var avgRate = totalStepsSum > 0 ? Math.round((correctSum / totalStepsSum) * 100) : 100;

      var origin = window.location.origin;
      var pathname = window.location.pathname;
      var basePath = pathname.substring(0, pathname.lastIndexOf('/'));
      if (basePath.endsWith('/board')) {
        basePath = basePath.substring(0, basePath.lastIndexOf('/board'));
      }
      var boardPrefix = (basePath ? basePath : '') + '/board/';

      var modal = document.createElement('div');
      modal.id = 'matheduProblemsModal';
      modal.className = 'mathedu-auth-backdrop';

      // 식별 라벨
      var identityHtml = '';
      if (user) {
        identityHtml = '<span class="library-tag tag-member">👤 정회원: <b>' + escapeHtml(user.name) + '</b> (' + escapeHtml(user.roleLabel) + ')</span>';
      } else if (guest) {
        identityHtml = 
          '<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap">' +
            '<span class="library-tag tag-guest">🧑‍🎓 비회원 학습자: <b>' + escapeHtml(guest.name) + '</b></span>' +
            '<button type="button" class="auth-btn-sub" onclick="MatheduAuth.showGuestLoginModal()" style="padding:2px 8px;font-size:0.75rem">비번 변경/재인증</button>' +
          '</div>';
      } else {
        identityHtml = 
          '<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap">' +
            '<span class="library-tag tag-anon">👀 익명 학습자 (기기 캐시)</span>' +
            '<button type="button" class="auth-btn-sub" onclick="MatheduAuth.showGuestLoginModal()" style="padding:3px 10px;font-size:0.78rem">👤 내 이름·비번으로 기록 연동하기</button>' +
          '</div>';
      }

      // 정식 회원 전환 CTA 배너 (정회원이 아닐 때 노출)
      var upgradeBannerHtml = '';
      if (!user) {
        upgradeBannerHtml = 
          '<div class="library-upgrade-banner">' +
            '<div>' +
              '<h4>✨ 정식 회원으로 10초 만에 전환하기</h4>' +
              '<p>현재까지 푼 <b>' + solvedList.length + '개</b>의 문제 기록을 100% 보존하면서, <b>[새 문제 출제]</b> 및 <b>[학급 수업 배포]</b> 권한이 부여되는 정식 회원으로 무료 업그레이드하세요.</p>' +
            '</div>' +
            '<button type="button" class="library-upgrade-btn" onclick="MatheduAuth.showUpgradeModal()">' +
              '🌟 정식 회원 전환 ➔' +
            '</button>' +
          '</div>';
      }

      // 문제 리스트 렌더링
      var listHtml = '';
      if (solvedList.length === 0) {
        listHtml = 
          '<div class="library-empty">' +
            '<div style="font-size:2.4rem;margin-bottom:8px">📝</div>' +
            '<div style="font-size:1.05rem;font-weight:700;color:#f1f5f9;margin-bottom:4px">아직 풀이한 문제가 없습니다.</div>' +
            '<div style="font-size:0.85rem;color:#94a3b8;margin-bottom:16px">3,400+ 고난도 수학 문제를 5~8단계 인터랙티브 퀴즈로 지금 바로 풀어보세요!</div>' +
            '<a href="' + (basePath ? basePath : '.') + '/#quizFilterBar" onclick="MatheduAuth.closeProblemsModal()" class="mathedu-auth-submit-btn" style="display:inline-block;text-decoration:none;padding:8px 20px;font-size:0.9rem;width:auto">' +
              '📚 퀴즈 목록 둘러보기 ➔' +
            '</a>' +
          '</div>';
      } else {
        listHtml = solvedList.map(function(item) {
          var pct = item.totalSteps > 0 ? Math.round((item.stepDone / item.totalSteps) * 100) : 100;
          var statusBadge = item.completed 
            ? '<span class="solved-badge badge-done">🏆 완주 완료 (' + item.stepDone + '/' + item.totalSteps + ')</span>'
            : '<span class="solved-badge badge-prog">⚡ ' + item.stepDone + '/' + item.totalSteps + '단계 진행 중</span>';

          var timeStr = item.lastUpdated ? new Date(item.lastUpdated).toLocaleDateString('ko-KR', { month:'short', day:'numeric', hour:'2-digit', minute:'2-digit' }) : '';

          return '' +
            '<div class="solved-item">' +
              '<div class="solved-item-main">' +
                '<div class="solved-item-title-row">' +
                  '<span class="solved-item-slug">' + escapeHtml(item.slug) + '</span>' +
                  '<h3 class="solved-item-title">' + escapeHtml(item.title) + '</h3>' +
                '</div>' +
                '<div class="solved-item-meta">' +
                  statusBadge +
                  '<span class="solved-meta-stat">정답: <b>' + item.correct + '</b>문항</span>' +
                  '<span class="solved-meta-time">' + timeStr + '</span>' +
                '</div>' +
                '<div class="solved-progress-bar">' +
                  '<div class="solved-progress-fill" style="width:' + pct + '%"></div>' +
                '</div>' +
              '</div>' +
              '<a href="' + boardPrefix + item.slug + '.html" class="solved-item-btn">' +
                (item.completed ? '🔄 다시 풀기' : '🚀 이어서 풀기') +
              '</a>' +
            '</div>';
        }).join('');
      }

      modal.innerHTML = 
        '<div class="mathedu-auth-card mathedu-problems-card">' +
          '<button type="button" class="mathedu-auth-close" onclick="MatheduAuth.closeProblemsModal()">✕</button>' +
          
          '<div class="mathedu-auth-header" style="margin-bottom:14px">' +
            '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;flex-wrap:wrap;gap:8px">' +
              '<div class="mathedu-auth-badge">📚 나의 학습 서재</div>' +
              identityHtml +
            '</div>' +
            '<h2 class="mathedu-auth-title" style="font-size:1.45rem">📂 내가 푼 문제 모아보기</h2>' +
            '<p class="mathedu-auth-desc">회원/비회원 구분 없이 내가 해결한 단계별 수학 문제들을 언제든 복습하고 이어서 풀 수 있습니다.</p>' +
          '</div>' +

          '<div class="library-stats-row">' +
            '<div class="library-stat-card">' +
              '<div class="num">' + solvedList.length + '<span>개</span></div>' +
              '<div class="lbl">📚 도전한 문제</div>' +
            '</div>' +
            '<div class="library-stat-card">' +
              '<div class="num" style="color:#5eead4">' + completedCount + '<span>개</span></div>' +
              '<div class="lbl">🏆 완주한 문제</div>' +
            '</div>' +
            '<div class="library-stat-card">' +
              '<div class="num" style="color:#38bdf8">' + avgRate + '<span>%</span></div>' +
              '<div class="lbl">📈 평균 정답률</div>' +
            '</div>' +
          '</div>' +

          upgradeBannerHtml +

          '<div class="solved-list-wrap">' +
            listHtml +
          '</div>' +
        '</div>';

      document.body.appendChild(modal);
    },

    closeProblemsModal: function() {
      var modal = document.getElementById('matheduProblemsModal');
      if (modal) modal.remove();
    },

    // 7. 비회원 식별 팝업 모달 (이름 + 간편 비번 입력)
    showGuestLoginModal: function(options) {
      options = options || {};
      var existing = document.getElementById('matheduGuestModal');
      if (existing) existing.remove();

      var currentG = getCurrentGuest();
      var modal = document.createElement('div');
      modal.id = 'matheduGuestModal';
      modal.className = 'mathedu-auth-backdrop';

      modal.innerHTML = 
        '<div class="mathedu-auth-card" style="max-width:420px">' +
          '<button type="button" class="mathedu-auth-close" onclick="document.getElementById(\'matheduGuestModal\').remove()">✕</button>' +
          
          '<div class="mathedu-auth-header">' +
            '<div class="mathedu-auth-badge" style="color:#a78bfa;border-color:rgba(167,139,250,.4)">🧑‍🎓 비회원 간편 식별</div>' +
            '<h2 class="mathedu-auth-title" style="font-size:1.3rem">학습자 이름 & 간편 비밀번호</h2>' +
            '<p class="mathedu-auth-desc">이름과 간편 비밀번호(4자리)를 입력하시면 동일한 학습자로 인식되어, 풀이 기록이 보존되고 나중에 언제든 이어서 풀 수 있습니다.</p>' +
          '</div>' +

          '<div id="guestAlertBox" class="mathedu-auth-alert" style="display:none"></div>' +

          '<form onsubmit="MatheduAuth._handleGuestSubmit(event)">' +
            '<div class="mathedu-auth-fg">' +
              '<label for="modalGuestName">이름 또는 닉네임</label>' +
              '<input type="text" id="modalGuestName" value="' + escapeHtml(currentG ? currentG.name : '') + '" placeholder="예: 김철수" required autocomplete="name">' +
            '</div>' +
            '<div class="mathedu-auth-fg">' +
              '<label for="modalGuestPin">간편 비밀번호 (4자리 권장)</label>' +
              '<input type="password" id="modalGuestPin" placeholder="비밀번호 입력" required maxlength="12" autocomplete="current-password">' +
            '</div>' +
            '<button type="submit" class="mathedu-auth-submit-btn" style="background:linear-gradient(135deg,#6366f1,#8b5cf6)">' +
              '👤 학습자 확인 및 기록 불러오기' +
            '</button>' +
          '</form>' +
        '</div>';

      document.body.appendChild(modal);
      modal._successCallback = options.onSuccess;
    },

    _handleGuestSubmit: async function(e) {
      e.preventDefault();
      var name = document.getElementById('modalGuestName').value;
      var pin = document.getElementById('modalGuestPin').value;
      var alertBox = document.getElementById('guestAlertBox');

      var res = await MatheduAuth.loginGuest(name, pin);
      if (!res.success) {
        alertBox.textContent = '⚠️ ' + res.message;
        alertBox.className = 'mathedu-auth-alert alert-error';
        alertBox.style.display = 'block';
        return;
      }

      var modal = document.getElementById('matheduGuestModal');
      var cb = modal ? modal._successCallback : null;
      modal.remove();

      if (typeof cb === 'function') {
        cb(res.guest);
      }
    },

    // 8. 정식 회원 전환 모달
    showUpgradeModal: function() {
      var guest = getCurrentGuest();
      var solvedCount = MatheduAuth.getSolvedProblems().length;

      MatheduAuth.showAuthModal({
        defaultTab: 'signup',
        title: '🌟 정식 회원으로 무료 업그레이드',
        desc: '현재까지 푼 <b>' + solvedCount + '개</b>의 문제 풀이 기록을 100% 안전하게 계정으로 승계합니다. 문제 출제 및 학급 배포 권한을 얻어보세요!',
        prefillName: guest ? guest.name : '',
        onSuccess: function(user) {
          showToast('축하합니다! ' + solvedCount + '개의 기록을 보존하여 정식 회원으로 전환되었습니다.', '🎉');
          MatheduAuth.showMyProblemsModal();
        }
      });
    },

    // 9. 기존 로그인/회원가입 모달
    showAuthModal: function(options) {
      options = options || {};
      var existing = document.getElementById('matheduAuthModal');
      if (existing) existing.remove();

      var modal = document.createElement('div');
      modal.id = 'matheduAuthModal';
      modal.className = 'mathedu-auth-backdrop';

      var defaultTab = options.defaultTab || 'login';
      var title = options.title || '🔐 mathedu 회원 서비스';
      var desc = options.desc || '선생님과 연구자를 위한 문제 출제 및 학급 수업 배포 전용 회원 공간입니다.';
      var prefillName = options.prefillName || '';

      modal.innerHTML = 
        '<div class="mathedu-auth-card">' +
          '<button type="button" class="mathedu-auth-close" onclick="MatheduAuth.closeAuthModal()">✕</button>' +
          
          '<div class="mathedu-auth-header">' +
            '<div class="mathedu-auth-badge">✨ min7014 mathedu membership</div>' +
            '<h2 class="mathedu-auth-title">' + title + '</h2>' +
            '<p class="mathedu-auth-desc">' + desc + '</p>' +
          '</div>' +

          '<div class="mathedu-auth-tabs">' +
            '<button type="button" id="tabBtnLogin" class="mathedu-auth-tab ' + (defaultTab === 'login' ? 'active' : '') + '" onclick="MatheduAuth.switchAuthTab(\'login\')">🔑 로그인</button>' +
            '<button type="button" id="tabBtnSignup" class="mathedu-auth-tab ' + (defaultTab === 'signup' ? 'active' : '') + '" onclick="MatheduAuth.switchAuthTab(\'signup\')">✨ 10초 무료 회원가입</button>' +
          '</div>' +

          '<div id="authAlertBox" class="mathedu-auth-alert" style="display:none"></div>' +

          '<!-- 로그인 폼 -->' +
          '<form id="authLoginForm" style="' + (defaultTab === 'login' ? 'display:block' : 'display:none') + '" onsubmit="MatheduAuth._handleLoginSubmit(event)">' +
            '<div class="mathedu-auth-fg">' +
              '<label for="authLoginId">아이디 또는 이메일</label>' +
              '<input type="text" id="authLoginId" placeholder="예: teacher 또는 이메일" required autocomplete="username">' +
            '</div>' +
            '<div class="mathedu-auth-fg">' +
              '<label for="authLoginPwd">비밀번호</label>' +
              '<input type="password" id="authLoginPwd" placeholder="비밀번호 입력" required autocomplete="current-password">' +
            '</div>' +
            '<button type="submit" class="mathedu-auth-submit-btn">🔑 로그인하여 진행하기</button>' +
            
            '<div class="mathedu-auth-divider"><span>또는 빠른 체험</span></div>' +
            '<button type="button" class="mathedu-auth-quick-btn" onclick="MatheduAuth._quickDemoLogin()">' +
              '⚡ 체험용 교사 계정으로 1초 로그인 (선생님 권한)' +
            '</button>' +
          '</form>' +

          '<!-- 회원가입 폼 -->' +
          '<form id="authSignupForm" style="' + (defaultTab === 'signup' ? 'display:block' : 'display:none') + '" onsubmit="MatheduAuth._handleSignupSubmit(event)">' +
            '<div class="mathedu-auth-grid">' +
              '<div class="mathedu-auth-fg">' +
                '<label for="authSignId">아이디 <span style="color:#f43f5e">*</span></label>' +
                '<input type="text" id="authSignId" placeholder="영문/숫자 3자 이상" required autocomplete="username">' +
              '</div>' +
              '<div class="mathedu-auth-fg">' +
                '<label for="authSignName">이름 / 닉네임 <span style="color:#f43f5e">*</span></label>' +
                '<input type="text" id="authSignName" value="' + escapeHtml(prefillName) + '" placeholder="예: 김선생님 또는 학생이름" required autocomplete="name">' +
              '</div>' +
            '</div>' +

            '<div class="mathedu-auth-grid">' +
              '<div class="mathedu-auth-fg">' +
                '<label for="authSignPwd">비밀번호 <span style="color:#f43f5e">*</span></label>' +
                '<input type="password" id="authSignPwd" placeholder="4자 이상" required autocomplete="new-password">' +
              '</div>' +
              '<div class="mathedu-auth-fg">' +
                '<label for="authSignPwdConfirm">비밀번호 확인 <span style="color:#f43f5e">*</span></label>' +
                '<input type="password" id="authSignPwdConfirm" placeholder="동일하게 재입력" required autocomplete="new-password">' +
              '</div>' +
            '</div>' +

            '<div class="mathedu-auth-grid">' +
              '<div class="mathedu-auth-fg">' +
                '<label for="authSignRole">회원 구분</label>' +
                '<select id="authSignRole">' +
                  '<option value="teacher" selected>👩‍🏫 초·중·고 수학교사</option>' +
                  '<option value="instructor">🎓 학원·전문 수학강사</option>' +
                  '<option value="researcher">🔬 수학교육 연구원</option>' +
                  '<option value="preteacher">🧑‍🎓 예비교사·사범대생</option>' +
                  '<option value="member">🌟 학생·수학 정회원</option>' +
                '</select>' +
              '</div>' +
              '<div class="mathedu-auth-fg">' +
                '<label for="authSignOrg">소속 학교 / 기관 (선택)</label>' +
                '<input type="text" id="authSignOrg" placeholder="예: 한국고등학교">' +
              '</div>' +
            '</div>' +

            '<div class="mathedu-auth-fg">' +
              '<label for="authSignEmail">이메일 (선택 · 퀴즈 생성 알림용)</label>' +
              '<input type="email" id="authSignEmail" placeholder="teacher@school.kr" autocomplete="email">' +
            '</div>' +

            '<button type="submit" class="mathedu-auth-submit-btn" style="background:linear-gradient(135deg,#38bdf8,#818cf8)">' +
              '✨ 10초 만에 무료 회원가입 완료 (기존 풀이 기록 승계)' +
            '</button>' +
          '</form>' +
        '</div>';

      document.body.appendChild(modal);
      modal._authSuccessCallback = options.onSuccess;
    },

    closeAuthModal: function() {
      var modal = document.getElementById('matheduAuthModal');
      if (modal) modal.remove();
    },

    switchAuthTab: function(tab) {
      var tabBtnLogin = document.getElementById('tabBtnLogin');
      var tabBtnSignup = document.getElementById('tabBtnSignup');
      var formLogin = document.getElementById('authLoginForm');
      var formSignup = document.getElementById('authSignupForm');
      var alertBox = document.getElementById('authAlertBox');
      if (alertBox) alertBox.style.display = 'none';

      if (tab === 'signup') {
        tabBtnLogin.classList.remove('active');
        tabBtnSignup.classList.add('active');
        formLogin.style.display = 'none';
        formSignup.style.display = 'block';
      } else {
        tabBtnLogin.classList.add('active');
        tabBtnSignup.classList.remove('active');
        formLogin.style.display = 'block';
        formSignup.style.display = 'none';
      }
    },

    _handleLoginSubmit: async function(e) {
      e.preventDefault();
      var id = document.getElementById('authLoginId').value;
      var pwd = document.getElementById('authLoginPwd').value;
      var alertBox = document.getElementById('authAlertBox');

      var res = await MatheduAuth.logIn(id, pwd);
      if (!res.success) {
        alertBox.textContent = '⚠️ ' + res.message;
        alertBox.className = 'mathedu-auth-alert alert-error';
        alertBox.style.display = 'block';
        return;
      }

      var modal = document.getElementById('matheduAuthModal');
      var cb = modal ? modal._authSuccessCallback : null;
      MatheduAuth.closeAuthModal();

      if (typeof cb === 'function') {
        cb(res.user);
      } else {
        showToast('반갑습니다, ' + res.user.name + '님!', '👋');
      }
    },

    _handleSignupSubmit: async function(e) {
      e.preventDefault();
      var id = document.getElementById('authSignId').value;
      var pwd = document.getElementById('authSignPwd').value;
      var pwdConfirm = document.getElementById('authSignPwdConfirm').value;
      var name = document.getElementById('authSignName').value;
      var role = document.getElementById('authSignRole').value;
      var org = document.getElementById('authSignOrg').value;
      var email = document.getElementById('authSignEmail').value;
      var alertBox = document.getElementById('authAlertBox');

      if (pwd !== pwdConfirm) {
        alertBox.textContent = '⚠️ 비밀번호가 일치하지 않습니다.';
        alertBox.className = 'mathedu-auth-alert alert-error';
        alertBox.style.display = 'block';
        return;
      }

      var res = await MatheduAuth.signUp({
        username: id,
        password: pwd,
        name: name,
        role: role,
        org: org,
        email: email
      });

      if (!res.success) {
        alertBox.textContent = '⚠️ ' + res.message;
        alertBox.className = 'mathedu-auth-alert alert-error';
        alertBox.style.display = 'block';
        return;
      }

      var modal = document.getElementById('matheduAuthModal');
      var cb = modal ? modal._authSuccessCallback : null;
      MatheduAuth.closeAuthModal();

      if (typeof cb === 'function') {
        cb(res.user);
      } else {
        showToast('회원가입이 완료되었습니다: ' + res.user.name + '님', '🎉');
      }
    },

    _quickDemoLogin: async function() {
      var res = await MatheduAuth.logIn('teacher', 'math1234');
      var modal = document.getElementById('matheduAuthModal');
      var cb = modal ? modal._authSuccessCallback : null;
      MatheduAuth.closeAuthModal();
      if (typeof cb === 'function') {
        cb(res.user);
      } else {
        showToast('체험용 교사 계정으로 로그인되었습니다.', '⚡');
      }
    }
  };

  // 상단 네비게이션 UI 업데이트
  function updateNavAuthUI() {
    var user = MatheduAuth.getCurrentUser();
    var guest = MatheduAuth.getCurrentGuest();
    var solvedCount = MatheduAuth.getSolvedProblems().length;

    var navMenu = document.querySelector('.nav-menu') || document.querySelector('.topbar');
    if (!navMenu) return;

    var existingSlot = document.getElementById('navAuthSlot');
    if (!existingSlot) {
      existingSlot = document.createElement('div');
      existingSlot.id = 'navAuthSlot';
      existingSlot.className = 'nav-auth-slot';
      navMenu.appendChild(existingSlot);
    }

    if (user) {
      // 1) 정회원 로그인 상태
      existingSlot.innerHTML = 
        '<div class="auth-logged-pill" title="소속: ' + escapeHtml(user.org || '수학교육') + '">' +
          '<span class="auth-user-icon">👤</span>' +
          '<span class="auth-user-name"><b>' + escapeHtml(user.name) + '</b> (' + escapeHtml(user.roleLabel || '회원') + ')</span>' +
          '<button type="button" class="auth-btn-action" onclick="MatheduAuth.showMyProblemsModal()" title="내가 푼 문제 모아보기">📂 서재(' + solvedCount + ')</button>' +
          '<button type="button" class="auth-btn-logout" onclick="MatheduAuth.logOut()" title="로그아웃">로그아웃</button>' +
        '</div>';
    } else if (guest) {
      // 2) 비회원 간편 식별 상태
      existingSlot.innerHTML = 
        '<div class="auth-guest-pill">' +
          '<span class="auth-user-icon">🧑‍🎓</span>' +
          '<span class="auth-user-name"><b>' + escapeHtml(guest.name) + '</b>님</span>' +
          '<button type="button" class="auth-btn-action" onclick="MatheduAuth.showMyProblemsModal()" title="내가 푼 문제 모아보기">📂 푼 문제 (' + solvedCount + ')</button>' +
          '<button type="button" class="auth-btn-upgrade" onclick="MatheduAuth.showUpgradeModal()" title="정식 회원으로 전환하여 출제/배포 권한 획득">✨ 정회원 전환</button>' +
          '<button type="button" class="auth-btn-logout" onclick="MatheduAuth.logoutGuest()" title="학습자 식별 해제">✕</button>' +
        '</div>';
    } else {
      // 3) 익명 방문자 상태
      existingSlot.innerHTML = 
        '<div style="display:inline-flex;align-items:center;gap:6px">' +
          '<button type="button" class="auth-btn-sub" onclick="MatheduAuth.showMyProblemsModal()" title="내가 푼 문제 모아보기">' +
            '📂 내가 푼 문제' + (solvedCount > 0 ? ' (' + solvedCount + ')' : '') +
          '</button>' +
          '<button type="button" class="auth-btn-login" onclick="MatheduAuth.showAuthModal()">' +
            '🔑 로그인 · 회원가입' +
          '</button>' +
        '</div>';
    }

    // create.html 내의 출제자 정보 자동 채움
    var reqNameInput = document.getElementById('requesterName');
    var reqEmailInput = document.getElementById('requesterEmail');
    if (user) {
      if (reqNameInput && !reqNameInput.value) reqNameInput.value = user.name;
      if (reqEmailInput && !reqEmailInput.value && user.email) reqEmailInput.value = user.email;
    }
  }

  function escapeHtml(s) {
    return String(s || '').replace(/[&<>"']/g, function(c) {
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
    });
  }

  function showToast(msg, icon) {
    icon = icon || '🌿';
    var toast = document.getElementById('matheduGlobalToast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'matheduGlobalToast';
      toast.className = 'mathedu-toast';
      document.body.appendChild(toast);
    }
    toast.innerHTML = '<span>' + icon + '</span><span>' + escapeHtml(msg) + '</span>';
    toast.classList.add('show');
    clearTimeout(toast._timer);
    toast._timer = setTimeout(function() {
      toast.classList.remove('show');
    }, 3500);
  }

  // 스타일 시트 자동 주입
  function injectStyles() {
    if (document.getElementById('mathedu-auth-style')) return;
    var style = document.createElement('style');
    style.id = 'mathedu-auth-style';
    style.textContent = `
      .mathedu-auth-backdrop {
        position: fixed; inset: 0; z-index: 999999;
        background: rgba(11, 15, 26, 0.84);
        backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px);
        display: flex; align-items: center; justify-content: center;
        padding: 16px; animation: authFadeIn .2s ease;
      }
      @keyframes authFadeIn { from { opacity: 0; transform: scale(0.97); } to { opacity: 1; transform: scale(1); } }
      .mathedu-auth-card {
        background: #141b2b;
        border: 1px solid rgba(124, 196, 255, 0.35);
        border-radius: 20px;
        max-width: 480px; width: 100%;
        padding: 28px;
        box-shadow: 0 25px 60px rgba(0,0,0,0.65), 0 0 30px rgba(56, 189, 248, 0.15);
        color: #f1f5f9; position: relative;
        font-family: -apple-system, BlinkMacSystemFont, "Pretendard", "Segoe UI", sans-serif;
      }
      .mathedu-problems-card {
        max-width: 760px; max-height: 88vh; display: flex; flex-direction: column; overflow: hidden;
      }
      .mathedu-auth-close {
        position: absolute; top: 16px; right: 18px;
        background: none; border: none; color: #94a3b8; font-size: 1.4rem; cursor: pointer;
        transition: color .15s;
      }
      .mathedu-auth-close:hover { color: #ffffff; }
      .mathedu-auth-header { margin-bottom: 18px; }
      .mathedu-auth-badge {
        display: inline-block; font-size: 0.76rem; font-weight: 700;
        background: rgba(56, 189, 248, 0.15); color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 9999px;
        padding: 3px 10px; margin-bottom: 8px;
      }
      .mathedu-auth-title {
        font-size: 1.35rem; font-weight: 700; color: #ffffff; margin-bottom: 6px; letter-spacing: -0.4px;
      }
      .mathedu-auth-desc {
        font-size: 0.88rem; color: #94a3b8; line-height: 1.45;
      }
      .mathedu-auth-tabs {
        display: grid; grid-template-columns: 1fr 1fr; gap: 6px;
        background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px; padding: 4px; margin-bottom: 18px;
      }
      .mathedu-auth-tab {
        background: transparent; border: none; color: #94a3b8;
        padding: 8px 12px; border-radius: 8px; font-size: 0.88rem; font-weight: 600;
        cursor: pointer; transition: all .15s;
      }
      .mathedu-auth-tab.active {
        background: rgba(56, 189, 248, 0.2); color: #38bdf8;
        box-shadow: 0 2px 8px rgba(0,0,0,0.25);
      }
      .mathedu-auth-fg {
        display: flex; flex-direction: column; gap: 5px; margin-bottom: 14px;
      }
      .mathedu-auth-fg label {
        font-size: 0.8rem; font-weight: 600; color: #cbd5e1;
      }
      .mathedu-auth-fg input, .mathedu-auth-fg select {
        background: rgba(11, 15, 26, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 10px; padding: 10px 14px; color: #ffffff;
        font-size: 0.92rem; outline: none; transition: border-color .15s;
      }
      .mathedu-auth-fg input:focus, .mathedu-auth-fg select:focus {
        border-color: #38bdf8; box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.25);
      }
      .mathedu-auth-grid {
        display: grid; grid-template-columns: 1fr 1fr; gap: 10px;
      }
      @media(max-width: 460px) { .mathedu-auth-grid { grid-template-columns: 1fr; } }
      .mathedu-auth-submit-btn {
        width: 100%; padding: 11px 16px; border: none; border-radius: 10px;
        background: linear-gradient(135deg, #10b981, #059669);
        color: #ffffff; font-size: 0.95rem; font-weight: 700; cursor: pointer;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3); transition: all .15s;
        margin-top: 6px;
      }
      .mathedu-auth-submit-btn:hover {
        background: linear-gradient(135deg, #059669, #047857);
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.45);
      }
      .mathedu-auth-divider {
        display: flex; align-items: center; margin: 16px 0; text-align: center;
        color: #64748b; font-size: 0.76rem;
      }
      .mathedu-auth-divider::before, .mathedu-auth-divider::after {
        content: ''; flex: 1; border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      }
      .mathedu-auth-divider span { padding: 0 10px; }
      .mathedu-auth-quick-btn {
        width: 100%; padding: 9px 14px; background: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 10px;
        color: #38bdf8; font-size: 0.85rem; font-weight: 600; cursor: pointer;
        transition: all .15s;
      }
      .mathedu-auth-quick-btn:hover {
        background: rgba(56, 189, 248, 0.2); border-color: #38bdf8;
      }
      .mathedu-auth-alert {
        padding: 9px 14px; border-radius: 8px; font-size: 0.82rem; margin-bottom: 14px;
      }
      .mathedu-auth-alert.alert-error {
        background: rgba(244, 63, 94, 0.15); border: 1px solid rgba(244, 63, 94, 0.4);
        color: #fda4af;
      }

      /* Nav Auth Items */
      .nav-auth-slot { display: inline-flex; align-items: center; margin-left: 8px; flex-wrap: wrap; gap: 6px; }
      .auth-btn-login {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.15), rgba(129, 140, 248, 0.15));
        border: 1px solid rgba(56, 189, 248, 0.4); border-radius: 20px;
        color: #38bdf8; font-size: 0.83rem; font-weight: 700; padding: 6px 14px;
        cursor: pointer; transition: all .15s;
      }
      .auth-btn-login:hover {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.28), rgba(129, 140, 248, 0.28));
        box-shadow: 0 0 14px rgba(56, 189, 248, 0.35);
      }
      .auth-btn-sub {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.18); border-radius: 20px;
        color: #e2e8f0; font-size: 0.82rem; font-weight: 600; padding: 6px 13px;
        cursor: pointer; transition: all .15s;
      }
      .auth-btn-sub:hover { background: rgba(255, 255, 255, 0.12); color: #ffffff; }

      .auth-logged-pill {
        display: inline-flex; align-items: center; gap: 8px;
        background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.35);
        border-radius: 20px; padding: 4px 12px; font-size: 0.82rem; color: #10b981;
      }
      .auth-logged-pill .auth-user-name { color: #f1f5f9; }

      .auth-guest-pill {
        display: inline-flex; align-items: center; gap: 7px;
        background: rgba(167, 139, 250, 0.12); border: 1px solid rgba(167, 139, 250, 0.35);
        border-radius: 20px; padding: 4px 12px; font-size: 0.82rem; color: #a78bfa;
      }
      .auth-guest-pill .auth-user-name { color: #f1f5f9; font-weight: 700; }
      
      .auth-btn-action {
        background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.35);
        border-radius: 12px; color: #38bdf8; font-size: 0.74rem; font-weight: 700; padding: 2px 8px;
        cursor: pointer; transition: all .15s;
      }
      .auth-btn-action:hover { background: rgba(56, 189, 248, 0.3); }

      .auth-btn-upgrade {
        background: linear-gradient(135deg, #f59e0b, #d97706); border: none;
        border-radius: 12px; color: #0b0f17; font-size: 0.74rem; font-weight: 800; padding: 3px 9px;
        cursor: pointer; transition: all .15s; box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
      }
      .auth-btn-upgrade:hover { transform: scale(1.03); }

      .auth-btn-logout {
        background: transparent; border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 8px; color: #94a3b8; font-size: 0.72rem; padding: 2px 7px;
        cursor: pointer; transition: all .15s;
      }
      .auth-btn-logout:hover { color: #f43f5e; border-color: rgba(244, 63, 94, 0.4); }

      /* Library Solved Problems Modal Styles */
      .library-tag {
        font-size: 0.78rem; font-weight: 700; padding: 3px 10px; border-radius: 20px;
      }
      .tag-member { background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.35); color: #10b981; }
      .tag-guest { background: rgba(167, 139, 250, 0.15); border: 1px solid rgba(167, 139, 250, 0.35); color: #a78bfa; }
      .tag-anon { background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.15); color: #94a3b8; }

      .library-stats-row {
        display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 16px;
      }
      .library-stat-card {
        background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px; padding: 12px; text-align: center;
      }
      .library-stat-card .num {
        font-size: 1.5rem; font-weight: 800; color: #ffffff;
      }
      .library-stat-card .num span { font-size: 0.85rem; font-weight: 400; color: #94a3b8; margin-left: 2px; }
      .library-stat-card .lbl { font-size: 0.75rem; color: #94a3b8; margin-top: 2px; }

      .library-upgrade-banner {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.12), rgba(217, 119, 6, 0.12));
        border: 1px solid rgba(245, 158, 11, 0.35); border-radius: 14px;
        padding: 14px 18px; margin-bottom: 16px; display: flex; align-items: center;
        justify-content: space-between; gap: 14px; flex-wrap: wrap;
      }
      .library-upgrade-banner h4 { font-size: 0.95rem; font-weight: 800; color: #fbbf24; margin-bottom: 2px; }
      .library-upgrade-banner p { font-size: 0.8rem; color: #e2e8f0; line-height: 1.35; }
      .library-upgrade-btn {
        background: linear-gradient(135deg, #f59e0b, #d97706); border: none;
        color: #0b0f17; font-weight: 800; font-size: 0.85rem; padding: 8px 16px;
        border-radius: 10px; cursor: pointer; transition: all .15s; white-space: nowrap;
        box-shadow: 0 4px 14px rgba(245, 158, 11, 0.35);
      }
      .library-upgrade-btn:hover { transform: translateY(-1px); }

      .solved-list-wrap {
        overflow-y: auto; max-height: 48vh; padding-right: 6px; display: flex; flex-direction: column; gap: 10px;
      }
      .solved-item {
        background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px; padding: 14px 16px; display: flex; align-items: center;
        justify-content: space-between; gap: 14px; transition: all .15s;
      }
      .solved-item:hover {
        background: rgba(255, 255, 255, 0.06); border-color: rgba(124, 196, 255, 0.3);
      }
      .solved-item-main { flex: 1; }
      .solved-item-title-row {
        display: flex; align-items: center; gap: 8px; margin-bottom: 4px; flex-wrap: wrap;
      }
      .solved-item-slug {
        font-family: monospace; font-size: 0.75rem; background: rgba(56, 189, 248, 0.15);
        color: #38bdf8; padding: 2px 6px; border-radius: 4px;
      }
      .solved-item-title {
        font-size: 0.96rem; font-weight: 700; color: #ffffff;
      }
      .solved-item-meta {
        display: flex; align-items: center; gap: 10px; font-size: 0.78rem; color: #94a3b8; margin-bottom: 6px; flex-wrap: wrap;
      }
      .solved-badge {
        font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 6px;
      }
      .badge-done { background: rgba(16, 185, 129, 0.2); color: #10b981; }
      .badge-prog { background: rgba(56, 189, 248, 0.2); color: #38bdf8; }
      .solved-progress-bar {
        background: rgba(255, 255, 255, 0.06); height: 6px; border-radius: 9999px; overflow: hidden; width: 100%; max-width: 280px;
      }
      .solved-progress-fill {
        height: 100%; background: linear-gradient(90deg, #38bdf8, #10b981); border-radius: 9999px;
      }
      .solved-item-btn {
        background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.4);
        border-radius: 10px; color: #38bdf8; font-size: 0.85rem; font-weight: 700;
        padding: 8px 14px; text-decoration: none; cursor: pointer; white-space: nowrap;
        transition: all .15s;
      }
      .solved-item-btn:hover {
        background: rgba(56, 189, 248, 0.25); color: #ffffff; transform: translateY(-1px);
      }
      .library-empty {
        text-align: center; padding: 40px 20px; background: rgba(0,0,0,0.2); border-radius: 14px;
      }

      /* Toast */
      .mathedu-toast {
        position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%) translateY(50px);
        background: #1e293b; border: 1px solid rgba(56, 189, 248, 0.4);
        border-radius: 12px; padding: 12px 20px; font-size: 0.9rem; color: #ffffff;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); display: flex; align-items: center; gap: 10px;
        opacity: 0; pointer-events: none; transition: all .25s ease; z-index: 9999999;
      }
      .mathedu-toast.show { transform: translateX(-50%) translateY(0); opacity: 1; pointer-events: auto; }
    `;
    document.head.appendChild(style);
  }

  // 초기화
  function init() {
    injectStyles();
    updateNavAuthUI();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  window.MatheduAuth = MatheduAuth;

})(window);
