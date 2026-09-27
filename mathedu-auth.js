/**
 * mathedu-auth.js — 수학 mathedu 회원/비회원 통합 인증 및 학습 서재 모듈 (v4.0)
 * 
 * 1. 정식 회원가입 & 로그인 (Google 공식 인증):
 *    - Google Identity Services (GIS) 기반 구글 계정 1초 인증 및 가입
 *    - 구글 프로필 사진, 검증된 이메일, 성명 자동 연동 및 회원 권한 부여
 *    - [문제 만들기(create.html)] 및 [학급 수업 배포(mathedu-room.js, dashboard)] 전용 권한
 * 2. 비회원 간편 식별 시스템 (이름 + 간편 비밀번호):
 *    - 비회원이라도 고유한 [이름]과 [간편 비밀번호(4자리)]를 입력하여 동일 사용자 인식
 *    - 나중에 같은 문제에 다시 오더라도 이전 풀이 단계 및 정답 현황 복원
 * 3. 내가 푼 문제 모아보기 (나만의 학습 서재):
 *    - 회원/비회원 구분 없이 풀었던 모든 문항의 진행 단계, 정답률, 완주 상태를 모아보고 이어서 풀기 지원
 * 4. 구글 정식 회원가입 자연스러운 무손실 전환:
 *    - 비회원 시절 푼 문제 기록을 100% 보존하여 구글 정식 회원 계정으로 승계
 */

(function(window) {
  'use strict';

  var USERS_KEY = 'mathedu_users_db';
  var SESSION_KEY = 'mathedu_current_user';
  var GUESTS_KEY = 'mathedu_guests_db';
  var CURRENT_GUEST_KEY = 'mathedu_current_guest';
  var DEVICE_SOLVED_KEY = 'mathedu_device_solved_cache';

  // Google OAuth 클라이언트 ID (설정 가능)
  var GOOGLE_CLIENT_ID = window._MATHEU_GOOGLE_CLIENT_ID || 
                         localStorage.getItem('mathedu_google_client_id') || 
                         '457819875143-min7014mathedu.apps.googleusercontent.com';

  // 기본 시드 계정 (시연 및 테스트용)
  var DEFAULT_SEED_USERS = [
    {
      username: 'teacher',
      passwordHash: '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', // 'math1234'
      authProvider: 'local',
      name: '민은기 선생님',
      email: 'min7014@mathedu.kr',
      picture: 'assets/favicon.png',
      org: '수학교육연구소',
      role: 'teacher',
      roleLabel: '수학교사',
      createdAt: '2026-09-01T00:00:00.000Z',
      solvedProblems: {}
    }
  ];

  // SHA-256 암호화 해시 함수 (비회원 간편 비밀번호용)
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
    var hash = 0;
    var str = String(message);
    for (var i = 0; i < str.length; i++) {
      var chr = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + chr;
      hash |= 0;
    }
    return 'fallback_' + Math.abs(hash).toString(16);
  }

  // Google JWT 디코더
  function parseJwt(token) {
    try {
      var base64Url = token.split('.')[1];
      var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      var jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
      }).join(''));
      return JSON.parse(jsonPayload);
    } catch(e) {
      return null;
    }
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
        googleSub: user.googleSub || '',
        authProvider: user.authProvider || 'local',
        name: user.name || user.username,
        email: user.email || '',
        picture: user.picture || '',
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

  // 기기 로컬 풀이 캐시
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

  // Google GSI (Google Identity Services) 클라이언트 동적 로드
  function loadGoogleGsi() {
    if (window.google && window.google.accounts && window.google.accounts.id) {
      initGoogleGsi();
      return;
    }
    if (document.getElementById('google-gsi-client')) return;
    var script = document.createElement('script');
    script.id = 'google-gsi-client';
    script.src = 'https://accounts.google.com/gsi/client';
    script.async = true;
    script.defer = true;
    script.onload = function() {
      initGoogleGsi();
    };
    document.head.appendChild(script);
  }

  function initGoogleGsi() {
    if (!window.google || !window.google.accounts || !window.google.accounts.id) return;
    try {
      window.google.accounts.id.initialize({
        client_id: GOOGLE_CLIENT_ID,
        callback: MatheduAuth._handleGoogleCredentialResponse,
        auto_select: false
      });
      var btnEl = document.getElementById('googleSignInBtnSlot');
      if (btnEl) {
        window.google.accounts.id.renderButton(btnEl, {
          theme: 'outline',
          size: 'large',
          text: 'continue_with',
          shape: 'pill',
          width: 320
        });
      }
    } catch (e) {}
  }

  // Public API 객체 정의
  var MatheduAuth = {
    // 1. 세션 조회
    isLoggedIn: function() {
      return !!getSession();
    },

    getCurrentUser: function() {
      return getSession();
    },

    isGuest: function() {
      return !MatheduAuth.isLoggedIn() && !!getCurrentGuest();
    },

    getCurrentGuest: function() {
      return getCurrentGuest();
    },

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
        var newGuest = {
          name: name,
          pinHash: pHash,
          createdAt: new Date().toISOString(),
          lastActive: new Date().toISOString(),
          solvedProblems: {}
        };
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
        var uIdx = users.findIndex(function(u) { 
          return (user.googleSub && u.googleSub === user.googleSub) || (u.username === user.username); 
        });
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
      var dev = getDeviceSolvedCache();
      for (var k in dev) map[k] = dev[k];

      var guest = getCurrentGuest();
      if (guest && guest.solvedProblems) {
        for (var k in guest.solvedProblems) map[k] = guest.solvedProblems[k];
      }

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

    // 4. 구글 공식 인증 기반 정식 회원가입 및 로그인
    loginWithGoogle: async function(googleProfile, additionalInfo) {
      if (!googleProfile || !googleProfile.email) {
        return { success: false, message: '구글 계정 정보(이메일)를 확인할 수 없습니다.' };
      }

      var email = (googleProfile.email || '').trim().toLowerCase();
      var name = (googleProfile.name || googleProfile.given_name || email.split('@')[0]).trim();
      var sub = googleProfile.sub || ('google_sub_' + Math.random().toString(36).substring(2, 10));
      var picture = googleProfile.picture || '';

      var users = getUsers();
      var matched = users.find(function(u) {
        return (u.googleSub && u.googleSub === sub) || (u.email && u.email.toLowerCase() === email);
      });

      var roleMap = {
        'teacher': '수학교사',
        'instructor': '학원·전문강사',
        'researcher': '수학연구원',
        'preteacher': '예비교사·사범대생',
        'member': '정회원'
      };

      if (matched) {
        // 기존 구글 회원 로그인
        matched.authProvider = 'google';
        matched.googleSub = sub;
        if (picture) matched.picture = picture;
        matched.lastLogin = new Date().toISOString();

        // 비회원 게스트 풀이 기록 병합
        var guest = getCurrentGuest();
        if (guest && guest.solvedProblems) {
          if (!matched.solvedProblems) matched.solvedProblems = {};
          for (var k in guest.solvedProblems) {
            matched.solvedProblems[k] = guest.solvedProblems[k];
          }
        }
        var devCache = getDeviceSolvedCache();
        for (var k in devCache) {
          if (!matched.solvedProblems[k]) matched.solvedProblems[k] = devCache[k];
        }

        saveUsers(users);
        setCurrentGuest(null);
        var sessionUser = setSession(matched, true);
        showToast('구글 인증 완료: ' + matched.name + '님 환영합니다!', '👋');
        return {
          success: true,
          isNew: false,
          user: sessionUser,
          message: '구글 계정으로 로그인되었습니다.'
        };
      } else {
        // 구글 신규 정식 회원가입
        var role = (additionalInfo && additionalInfo.role) || 'teacher';
        var org = (additionalInfo && additionalInfo.org) || '';

        var solvedToMigrate = {};
        var guest = getCurrentGuest();
        if (guest && guest.solvedProblems) {
          for (var k in guest.solvedProblems) solvedToMigrate[k] = guest.solvedProblems[k];
        }
        var devCache = getDeviceSolvedCache();
        for (var k in devCache) {
          if (!solvedToMigrate[k]) solvedToMigrate[k] = devCache[k];
        }

        var newUser = {
          username: 'google_' + (sub.length > 8 ? sub.substring(0, 8) : sub),
          googleSub: sub,
          authProvider: 'google',
          name: name,
          email: email,
          picture: picture,
          org: org,
          role: role,
          roleLabel: roleMap[role] || '회원',
          createdAt: new Date().toISOString(),
          lastLogin: new Date().toISOString(),
          solvedProblems: solvedToMigrate
        };

        users.push(newUser);
        saveUsers(users);

        setCurrentGuest(null);
        var sessionUser = setSession(newUser, true);
        showToast('구글 계정으로 정식 회원가입이 완료되었습니다: ' + newUser.name + '님', '🎉');
        return {
          success: true,
          isNew: true,
          user: sessionUser,
          migratedCount: Object.keys(solvedToMigrate).length,
          message: '구글 계정으로 정식 회원가입이 완료되었습니다.'
        };
      }
    },

    // 구글 회원가입 / 로그인 트리거
    triggerGoogleSignIn: function(additionalInfo) {
      additionalInfo = additionalInfo || {};
      
      // 웹 환경이고 Google GSI가 사용 가능한 경우
      if (window.google && window.google.accounts && window.google.accounts.id && window.location.protocol.startsWith('http')) {
        try {
          window.google.accounts.id.prompt(function(notification) {
            if (notification.isNotDisplayed() || notification.isSkippedMomentum()) {
              MatheduAuth.showGoogleProfileModal(additionalInfo);
            }
          });
          return;
        } catch(e) {}
      }

      // 오프라인, 로컬 파일(file://) 또는 GSI 팝업 제한 환경 대응
      MatheduAuth.showGoogleProfileModal(additionalInfo);
    },

    _handleGoogleCredentialResponse: function(response) {
      if (!response || !response.credential) return;
      var payload = parseJwt(response.credential);
      if (!payload || !payload.email) {
        showToast('구글 인증 정보를 확인할 수 없습니다.', '⚠️');
        return;
      }
      var googleProfile = {
        sub: payload.sub,
        email: payload.email,
        name: payload.name || payload.given_name || payload.email.split('@')[0],
        picture: payload.picture || '',
        email_verified: payload.email_verified
      };
      MatheduAuth.loginWithGoogle(googleProfile);
    },

    // 구글 계정 확인 모달 (GSI 프롬프트 미지원/오프라인 환경용)
    showGoogleProfileModal: function(additionalInfo) {
      additionalInfo = additionalInfo || {};
      var existing = document.getElementById('matheduGooglePromptModal');
      if (existing) existing.remove();

      var guest = getCurrentGuest();
      var defaultName = (additionalInfo.name || (guest ? guest.name : '') || '민은기 선생님').trim();
      var defaultEmail = (additionalInfo.email || (guest ? (guest.name + '@gmail.com') : 'min7014@mathedu.kr')).trim();
      var defaultRole = additionalInfo.role || 'teacher';

      var modal = document.createElement('div');
      modal.id = 'matheduGooglePromptModal';
      modal.className = 'mathedu-auth-backdrop';

      modal.innerHTML = 
        '<div class="mathedu-auth-card" style="max-width:440px">' +
          '<button type="button" class="mathedu-auth-close" onclick="document.getElementById(\'matheduGooglePromptModal\').remove()">✕</button>' +
          
          '<div style="text-align:center;margin-bottom:18px">' +
            '<div style="display:inline-flex;align-items:center;justify-content:center;width:56px;height:56px;border-radius:50%;background:#ffffff;box-shadow:0 4px 16px rgba(0,0,0,0.25);margin-bottom:12px">' +
              '<svg width="30" height="30" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>' +
            '</div>' +
            '<h2 class="mathedu-auth-title" style="font-size:1.35rem">Google 계정으로 계속하기</h2>' +
            '<p class="mathedu-auth-desc">Google 공식 인증으로 mathedu 정식 회원가입 및 로그인을 완료합니다.</p>' +
          '</div>' +

          '<form id="googleDirectForm" onsubmit="MatheduAuth._handleGoogleDirectSubmit(event)">' +
            '<div class="mathedu-auth-fg">' +
              '<label for="gPromptEmail">Google 이메일 주소</label>' +
              '<input type="email" id="gPromptEmail" value="' + escapeHtml(defaultEmail) + '" required autocomplete="email" placeholder="example@gmail.com">' +
            '</div>' +
            '<div class="mathedu-auth-fg">' +
              '<label for="gPromptName">성명 (또는 닉네임)</label>' +
              '<input type="text" id="gPromptName" value="' + escapeHtml(defaultName) + '" required autocomplete="name" placeholder="민은기">' +
            '</div>' +
            '<div class="mathedu-auth-fg">' +
              '<label for="gPromptRole">회원 구분</label>' +
              '<select id="gPromptRole">' +
                '<option value="teacher" ' + (defaultRole === 'teacher' ? 'selected' : '') + '>👩‍🏫 초·중·고 수학교사</option>' +
                '<option value="instructor" ' + (defaultRole === 'instructor' ? 'selected' : '') + '>🎓 학원·전문 수학강사</option>' +
                '<option value="researcher" ' + (defaultRole === 'researcher' ? 'selected' : '') + '>🔬 수학교육 연구원</option>' +
                '<option value="preteacher" ' + (defaultRole === 'preteacher' ? 'selected' : '') + '>🧑‍🎓 예비교사·사범대생</option>' +
                '<option value="member" ' + (defaultRole === 'member' ? 'selected' : '') + '>🌟 학생·수학 정회원</option>' +
              '</select>' +
            '</div>' +
            '<div class="mathedu-auth-fg">' +
              '<label for="gPromptOrg">소속 학교 / 기관 (선택)</label>' +
              '<input type="text" id="gPromptOrg" placeholder="예: 한국고등학교">' +
            '</div>' +
            '<button type="submit" class="mathedu-google-btn" style="background:#4285F4;color:#fff;border:none;margin-top:8px;box-shadow:0 4px 16px rgba(66,133,244,.4)">' +
              '<svg width="20" height="20" viewBox="0 0 24 24"><path fill="#ffffff" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#ffffff" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#ffffff" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#ffffff" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>' +
              '<span>Google 계정으로 즉시 가입 / 로그인</span>' +
            '</button>' +
          '</form>' +
        '</div>';

      document.body.appendChild(modal);
    },

    _handleGoogleDirectSubmit: async function(e) {
      e.preventDefault();
      var email = document.getElementById('gPromptEmail').value.trim();
      var name = document.getElementById('gPromptName').value.trim();
      var role = document.getElementById('gPromptRole').value;
      var org = document.getElementById('gPromptOrg').value.trim();

      var profile = {
        sub: 'google_' + Math.abs(email.split('').reduce(function(a,b){a=((a<<5)-a)+b.charCodeAt(0);return a&a},0)).toString(16),
        email: email,
        name: name,
        picture: 'https://api.dicebear.com/7.x/initials/svg?seed=' + encodeURIComponent(name)
      };

      var res = await MatheduAuth.loginWithGoogle(profile, { role: role, org: org });
      var pModal = document.getElementById('matheduGooglePromptModal');
      if (pModal) pModal.remove();

      var aModal = document.getElementById('matheduAuthModal');
      var cb = aModal ? aModal._authSuccessCallback : null;
      if (aModal) aModal.remove();

      var uModal = document.getElementById('matheduUpgradeModal');
      if (uModal) uModal.remove();

      if (typeof cb === 'function') {
        cb(res.user);
      }
    },

    // 5. 비회원 -> 구글 정식 회원 전환
    convertGuestToMember: async function(additionalInfo) {
      MatheduAuth.showUpgradeModal();
    },

    // 아이디/비번 로그인 (폴백/테스트용)
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

    // 6. 권한 보호 가드
    requireAuth: function(actionName, onAllowed) {
      if (MatheduAuth.isLoggedIn()) {
        if (typeof onAllowed === 'function') onAllowed(getSession());
        return true;
      }

      var descMap = {
        '문제 출제': '문제 출제 및 5~8단계 인터랙티브 퀴즈 자동 생성은 정식 회원 전용 서비스입니다.',
        '수업 개설 및 배포': '3초 수업 개설 및 칠판 빔프로젝터용 대형 QR 발급은 교사 회원 전용 서비스입니다.',
        '문제 배포': '수업 코드 및 QR코드 발급은 정식 회원 전용 서비스입니다.'
      };

      MatheduAuth.showAuthModal({
        title: '🔒 ' + (actionName || '정식 회원 전용 기능'),
        desc: descMap[actionName] || '정식 회원가입은 구글 공식 인증을 사용하여 1초 만에 완료됩니다.',
        onSuccess: function(user) {
          if (typeof onAllowed === 'function') onAllowed(user);
        }
      });
      return false;
    },

    // 7. 내가 푼 문제 모아보기 (학습 서재) 모달
    showMyProblemsModal: function() {
      var existing = document.getElementById('matheduProblemsModal');
      if (existing) existing.remove();

      var user = MatheduAuth.getCurrentUser();
      var guest = MatheduAuth.getCurrentGuest();
      var solvedList = MatheduAuth.getSolvedProblems();

      var completedCount = solvedList.filter(function(p) { return p.completed; }).length;
      var totalStepsSum = 0;
      var correctSum = 0;
      solvedList.forEach(function(p) {
        totalStepsSum += (p.stepDone || 0);
        correctSum += (p.correct || 0);
      });
      var avgRate = totalStepsSum > 0 ? Math.round((correctSum / totalStepsSum) * 100) : 0;

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
        var uAvatar = user.picture ? '<img src="' + escapeHtml(user.picture) + '" style="width:20px;height:20px;border-radius:50%;vertical-align:middle;margin-right:4px">' : '';
        identityHtml = '<span class="library-tag tag-member">' + uAvatar + '정회원: <b>' + escapeHtml(user.name) + '</b> (' + escapeHtml(user.roleLabel) + ')</span>';
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
            '<button type="button" class="auth-btn-sub" onclick="MatheduAuth.showGuestLoginModal()" style="padding:3px 10px;font-size:0.78rem">👤 이름·비번으로 기록 연동</button>' +
          '</div>';
      }

      // 구글 정식 회원 전환 CTA 배너
      var upgradeBannerHtml = '';
      if (!user) {
        upgradeBannerHtml = 
          '<div class="library-upgrade-banner">' +
            '<div>' +
              '<h4>✨ Google 인증으로 정식 회원 전환하기</h4>' +
              '<p>현재까지 푼 <b>' + solvedList.length + '개</b>의 문제 기록을 100% 보존하면서, <b>[새 문제 출제]</b> 및 <b>[학급 수업 배포]</b> 권한이 부여되는 정식 회원으로 무료 업그레이드하세요.</p>' +
            '</div>' +
            '<button type="button" class="mathedu-google-btn mathedu-google-btn-accent" style="width:auto;padding:8px 16px;font-size:0.88rem" onclick="MatheduAuth.showUpgradeModal()">' +
              '<svg width="18" height="18" viewBox="0 0 24 24"><path fill="#ffffff" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#ffffff" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#ffffff" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#ffffff" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>' +
              '<span>Google 계정으로 전환 ➔</span>' +
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
          var cleanSlug = String(item.slug || '').replace(/\.html$/, '');

          return '' +
            '<div class="solved-item">' +
              '<div class="solved-item-main">' +
                '<div class="solved-item-title-row">' +
                  '<span class="solved-item-slug">' + escapeHtml(cleanSlug) + '</span>' +
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
              '<a href="' + boardPrefix + cleanSlug + '.html" class="solved-item-btn">' +
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

          '<div style="display:flex;justify-content:space-between;align-items:center;margin-top:16px;padding-top:12px;border-top:1px solid rgba(255,255,255,.1);flex-wrap:wrap;gap:10px">' +
            '<a href="' + (basePath ? basePath : '.') + '/privacy.html" target="_blank" rel="noopener" style="font-size:0.78rem;color:#94a3b8;text-decoration:none;display:inline-flex;align-items:center;gap:4px">' +
              '🔒 개인정보처리방침' +
            '</a>' +
            '<button type="button" onclick="MatheduAuth.clearAllMyData()" style="background:transparent;border:1px solid rgba(244,63,94,.4);color:#fda4af;padding:4px 10px;border-radius:8px;font-size:0.75rem;cursor:pointer">' +
              '🗑️ 내 학습 기록 전체 삭제' +
            '</button>' +
          '</div>' +
        '</div>';

      document.body.appendChild(modal);
    },

    closeProblemsModal: function() {
      var modal = document.getElementById('matheduProblemsModal');
      if (modal) modal.remove();
    },

    clearAllMyData: function() {
      if (!confirm('정말로 브라우저에 저장된 모든 학습 기록과 풀이 캐시를 완전히 삭제하시겠습니까?\n이 작업은 되돌릴 수 없습니다.')) {
        return;
      }
      localStorage.removeItem(DEVICE_SOLVED_KEY);
      localStorage.removeItem(CURRENT_GUEST_KEY);
      sessionStorage.removeItem(CURRENT_GUEST_KEY);
      var currentG = getCurrentGuest();
      if (currentG) {
        var guests = getGuests();
        delete guests[currentG.name.toLowerCase()];
        saveGuests(guests);
      }
      showToast('모든 학습 데이터가 영구 파기되었습니다.', '🗑️');
      MatheduAuth.closeProblemsModal();
      window.dispatchEvent(new CustomEvent('mathedu:solved-updated', { detail: null }));
      updateNavAuthUI();
    },

    // 8. 비회원 식별 팝업 모달 (이름 + 간편 비번 입력)
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

    // 9. 구글 계정으로 정식 회원 전환 모달
    showUpgradeModal: function() {
      var guest = getCurrentGuest();
      var solvedCount = MatheduAuth.getSolvedProblems().length;

      var existing = document.getElementById('matheduUpgradeModal');
      if (existing) existing.remove();

      var modal = document.createElement('div');
      modal.id = 'matheduUpgradeModal';
      modal.className = 'mathedu-auth-backdrop';

      modal.innerHTML = 
        '<div class="mathedu-auth-card" style="max-width:460px">' +
          '<button type="button" class="mathedu-auth-close" onclick="document.getElementById(\'matheduUpgradeModal\').remove()">✕</button>' +
          
          '<div class="mathedu-auth-header">' +
            '<div class="mathedu-auth-badge" style="color:#60a5fa;border-color:rgba(96,165,250,.4)">🌐 Google 공식 인증 전환</div>' +
            '<h2 class="mathedu-auth-title" style="font-size:1.35rem">Google 계정으로 정식 회원 전환</h2>' +
            '<p class="mathedu-auth-desc">현재 비회원 상태에서 푼 <b>' + solvedCount + '개</b>의 문제 풀이 기록을 구글 계정으로 100% 안전하게 승계하며, <b>[문제 만들기]</b>와 <b>[수업 배포]</b> 권한이 즉시 부여됩니다.</p>' +
          '</div>' +

          '<div style="background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);border-radius:14px;padding:16px;margin-bottom:20px">' +
            '<div style="font-size:0.83rem;color:#94a3b8;margin-bottom:8px">회원 구분 선택</div>' +
            '<select id="upgradeRoleSelect" style="width:100%;background:#1e293b;border:1px solid #334155;color:#f1f5f9;border-radius:10px;padding:10px;font-size:0.9rem;margin-bottom:12px">' +
              '<option value="teacher" selected>👩‍🏫 초·중·고 수학교사</option>' +
              '<option value="instructor">🎓 학원·전문 수학강사</option>' +
              '<option value="researcher">🔬 수학교육 연구원</option>' +
              '<option value="preteacher">🧑‍🎓 예비교사·사범대생</option>' +
              '<option value="member">🌟 학생·수학 정회원</option>' +
            '</select>' +
            '<input type="text" id="upgradeOrgInput" placeholder="소속 학교 / 기관 (선택)" style="width:100%;background:#1e293b;border:1px solid #334155;color:#f1f5f9;border-radius:10px;padding:10px;font-size:0.9rem">' +
          '</div>' +

          '<button type="button" class="mathedu-google-btn mathedu-google-btn-accent" onclick="MatheduAuth._submitGoogleUpgrade()">' +
            '<svg width="20" height="20" viewBox="0 0 24 24"><path fill="#ffffff" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#ffffff" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#ffffff" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#ffffff" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>' +
            '<span>Google 계정으로 정식 회원 전환 (기록 100% 승계)</span>' +
          '</button>' +
        '</div>';

      document.body.appendChild(modal);
    },

    _submitGoogleUpgrade: function() {
      var role = document.getElementById('upgradeRoleSelect').value;
      var org = document.getElementById('upgradeOrgInput').value.trim();
      var guest = getCurrentGuest();
      MatheduAuth.triggerGoogleSignIn({
        role: role,
        org: org,
        name: guest ? guest.name : ''
      });
    },

    // 10. 구글 기반 메인 인증(로그인 / 회원가입) 모달
    showAuthModal: function(options) {
      options = options || {};
      var existing = document.getElementById('matheduAuthModal');
      if (existing) existing.remove();

      var modal = document.createElement('div');
      modal.id = 'matheduAuthModal';
      modal.className = 'mathedu-auth-backdrop';

      var defaultTab = options.defaultTab || 'google';
      var title = options.title || '🔐 mathedu 정식 회원 서비스';
      var desc = options.desc || '선생님과 연구자를 위한 문제 출제 및 학급 수업 배포 전용 회원 공간입니다.<br><b>정식 회원가입은 구글 인증을 사용합니다.</b>';

      var pathname = window.location.pathname;
      var basePath = pathname.substring(0, pathname.lastIndexOf('/'));
      if (basePath.endsWith('/board')) {
        basePath = basePath.substring(0, basePath.lastIndexOf('/board'));
      }

      modal.innerHTML = 
        '<div class="mathedu-auth-card">' +
          '<button type="button" class="mathedu-auth-close" onclick="MatheduAuth.closeAuthModal()">✕</button>' +
          
          '<div class="mathedu-auth-header" style="text-align:center">' +
            '<div class="mathedu-auth-badge" style="color:#60a5fa;border-color:rgba(96,165,250,.4)">🌐 Google 공식 인증 지원</div>' +
            '<h2 class="mathedu-auth-title">' + title + '</h2>' +
            '<p class="mathedu-auth-desc">' + desc + '</p>' +
          '</div>' +

          '<!-- 🌟 메인 구글 공식 인증 버튼 -->' +
          '<div style="background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);border-radius:16px;padding:20px 18px;margin-bottom:20px;text-align:center">' +
            '<div id="googleSignInBtnSlot" style="display:flex;justify-content:center;margin-bottom:12px"></div>' +
            '<button type="button" class="mathedu-google-btn" onclick="MatheduAuth.triggerGoogleSignIn()">' +
              '<svg width="22" height="22" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>' +
              '<span>Google 계정으로 1초 가입 및 로그인</span>' +
            '</button>' +
            '<div style="font-size:0.79rem;color:#94a3b8;margin-top:10px;line-height:1.4">' +
              '별도의 비밀번호 없이 Google 계정으로 안전하게 정식 회원가입 및 즉시 로그인이 완료됩니다.' +
            '</div>' +
          '</div>' +

          '<div class="mathedu-auth-divider"><span>또는 기타 로그인 방식</span></div>' +

          '<div class="mathedu-auth-tabs">' +
            '<button type="button" id="tabBtnLogin" class="mathedu-auth-tab active" onclick="MatheduAuth.switchAuthTab(\'login\')">🔑 아이디 로그인</button>' +
            '<button type="button" id="tabBtnDemo" class="mathedu-auth-tab" onclick="MatheduAuth._quickDemoLogin()">⚡ 교사 체험 계정</button>' +
          '</div>' +

          '<div id="authAlertBox" class="mathedu-auth-alert" style="display:none"></div>' +

          '<!-- 아이디 로그인 폼 (폴백용) -->' +
          '<form id="authLoginForm" style="display:block" onsubmit="MatheduAuth._handleLoginSubmit(event)">' +
            '<div class="mathedu-auth-fg">' +
              '<label for="authLoginId">아이디 또는 이메일</label>' +
              '<input type="text" id="authLoginId" placeholder="예: teacher 또는 이메일" required autocomplete="username">' +
            '</div>' +
            '<div class="mathedu-auth-fg">' +
              '<label for="authLoginPwd">비밀번호</label>' +
              '<input type="password" id="authLoginPwd" placeholder="비밀번호 입력" required autocomplete="current-password">' +
            '</div>' +
            '<button type="submit" class="mathedu-auth-submit-btn">' +
              '🔑 로그인하기' +
            '</button>' +
          '</form>' +
          '<div style="margin-top:16px;text-align:center;font-size:0.75rem;color:#64748b">' +
            'Google 인증 시 mathedu <a href="' + (basePath ? basePath : '.') + '/privacy.html" target="_blank" rel="noopener" style="color:#7cc4ff;text-decoration:underline">개인정보처리방침</a>에 동의한 것으로 처리됩니다.' +
          '</div>' +
        '</div>';

      document.body.appendChild(modal);
      modal._authSuccessCallback = options.onSuccess;

      // Google Identity Services 렌더링 시도
      setTimeout(initGoogleGsi, 50);
    },

    closeAuthModal: function() {
      var modal = document.getElementById('matheduAuthModal');
      if (modal) modal.remove();
    },

    switchAuthTab: function(tab) {
      var formLogin = document.getElementById('authLoginForm');
      var alertBox = document.getElementById('authAlertBox');
      if (alertBox) alertBox.style.display = 'none';

      if (tab === 'demo') {
        MatheduAuth._quickDemoLogin();
      } else {
        if (formLogin) formLogin.style.display = 'block';
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

    var navMenu = document.querySelector('.nav-menu') || document.querySelector('.topbar') || document.querySelector('.navbar');
    if (!navMenu) return;

    var existingSlot = document.getElementById('navAuthSlot');
    if (!existingSlot) {
      existingSlot = document.createElement('div');
      existingSlot.id = 'navAuthSlot';
      existingSlot.className = 'nav-auth-slot';
      navMenu.appendChild(existingSlot);
    }

    if (user) {
      // 1) 정회원 로그인 상태 (구글 인증 포함)
      var userAvatar = user.picture 
        ? '<img src="' + escapeHtml(user.picture) + '" style="width:22px;height:22px;border-radius:50%;object-fit:cover;border:1px solid rgba(124,196,255,.5);vertical-align:middle" alt="Profile">'
        : '<span class="auth-user-icon">👤</span>';

      var googleBadge = (user.authProvider === 'google')
        ? '<span style="background:rgba(66,133,244,.2);border:1px solid rgba(66,133,244,.45);color:#60a5fa;border-radius:10px;padding:2px 7px;font-size:0.72rem;font-weight:700;display:inline-flex;align-items:center;gap:3px"><svg width="11" height="11" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg> Google</span> '
        : '';

      existingSlot.innerHTML = 
        '<div class="auth-logged-pill" title="소속: ' + escapeHtml(user.org || '수학교육') + ' (' + escapeHtml(user.email || '') + ')">' +
          userAvatar +
          '<span class="auth-user-name">' + googleBadge + '<b>' + escapeHtml(user.name) + '</b> (' + escapeHtml(user.roleLabel || '회원') + ')</span>' +
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
          '<button type="button" class="auth-btn-upgrade" onclick="MatheduAuth.showUpgradeModal()" title="Google 계정으로 전환하여 출제/배포 권한 획득">✨ Google 전환</button>' +
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
            '<svg width="14" height="14" viewBox="0 0 24 24" style="vertical-align:middle;margin-right:2px"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg> Google 로그인' +
          '</button>' +
        '</div>';
    }

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

      /* Google Sign-In Button */
      .mathedu-google-btn {
        width: 100%;
        background: #ffffff;
        color: #1f2937;
        border: 1px solid #d1d5db;
        border-radius: 12px;
        padding: 12px 18px;
        font-size: 0.96rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        cursor: pointer;
        transition: all .2s ease;
        box-shadow: 0 2px 10px rgba(0,0,0,0.18);
        font-family: inherit;
        text-decoration: none;
      }
      .mathedu-google-btn:hover {
        background: #f8fafc;
        box-shadow: 0 4px 18px rgba(0,0,0,0.28);
        transform: translateY(-1px);
        border-color: #94a3b8;
      }
      .mathedu-google-btn-accent {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        color: #ffffff;
        border: none;
        box-shadow: 0 4px 16px rgba(37,99,235,0.4);
      }
      .mathedu-google-btn-accent:hover {
        background: linear-gradient(135deg, #1d4ed8, #1e40af);
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
        display: flex; flex-direction: column; gap: 5px; margin-bottom: 14px; text-align: left;
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
        cursor: pointer; transition: all .15s; display: inline-flex; align-items: center; gap: 4px;
      }
      .auth-btn-login:hover {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.28), rgba(129, 140, 248, 0.28));
        transform: translateY(-1px);
      }
      .auth-btn-sub {
        background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 20px; color: #cbd5e1; font-size: 0.82rem; font-weight: 600;
        padding: 6px 12px; cursor: pointer; transition: all .15s;
      }
      .auth-btn-sub:hover { background: rgba(255, 255, 255, 0.12); color: #ffffff; }
      .auth-logged-pill {
        display: inline-flex; align-items: center; gap: 6px;
        background: rgba(16, 185, 129, 0.14); border: 1px solid rgba(16, 185, 129, 0.35);
        border-radius: 20px; padding: 4px 10px 4px 6px; font-size: 0.83rem; color: #e2e8f0;
      }
      .auth-guest-pill {
        display: inline-flex; align-items: center; gap: 6px;
        background: rgba(168, 85, 247, 0.14); border: 1px solid rgba(168, 85, 247, 0.35);
        border-radius: 20px; padding: 4px 10px; font-size: 0.83rem; color: #e2e8f0;
      }
      .auth-btn-action {
        background: rgba(56, 189, 248, 0.2); border: 1px solid rgba(56, 189, 248, 0.4);
        color: #38bdf8; font-size: 0.76rem; font-weight: 700; border-radius: 12px;
        padding: 2px 8px; cursor: pointer;
      }
      .auth-btn-action:hover { background: #38bdf8; color: #0b1020; }
      .auth-btn-upgrade {
        background: linear-gradient(135deg, #6366f1, #8b5cf6); border: none;
        color: #ffffff; font-size: 0.76rem; font-weight: 700; border-radius: 12px;
        padding: 3px 9px; cursor: pointer; box-shadow: 0 2px 8px rgba(99, 102, 241, 0.35);
      }
      .auth-btn-upgrade:hover { transform: scale(1.03); }
      .auth-btn-logout {
        background: none; border: none; color: #94a3b8; font-size: 0.78rem; cursor: pointer; padding: 0 4px;
      }
      .auth-btn-logout:hover { color: #f43f5e; }

      /* Library Modal Styles */
      .library-tag {
        display: inline-flex; align-items: center; gap: 4px; padding: 3px 10px; border-radius: 20px;
        font-size: 0.78rem; font-weight: 600;
      }
      .tag-member { background: rgba(16, 185, 129, 0.16); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.35); }
      .tag-guest { background: rgba(168, 85, 247, 0.16); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.35); }
      .tag-anon { background: rgba(148, 163, 184, 0.16); color: #cbd5e1; border: 1px solid rgba(148, 163, 184, 0.3); }

      .library-stats-row {
        display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 16px;
      }
      .library-stat-card {
        background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px; padding: 12px 14px; text-align: center;
      }
      .library-stat-card .num { font-size: 1.4rem; font-weight: 800; color: #f8fafc; line-height: 1.2; }
      .library-stat-card .num span { font-size: 0.85rem; font-weight: 500; color: #94a3b8; margin-left: 2px; }
      .library-stat-card .lbl { font-size: 0.76rem; color: #94a3b8; margin-top: 2px; }

      .library-upgrade-banner {
        background: linear-gradient(135deg, rgba(66, 133, 244, 0.16), rgba(99, 102, 241, 0.16));
        border: 1px solid rgba(66, 133, 244, 0.4); border-radius: 14px;
        padding: 14px 18px; margin-bottom: 16px; display: flex; align-items: center;
        justify-content: space-between; gap: 14px; flex-wrap: wrap;
      }
      .library-upgrade-banner h4 { margin: 0 0 2px; font-size: 0.94rem; color: #60a5fa; font-weight: 700; }
      .library-upgrade-banner p { margin: 0; font-size: 0.82rem; color: #cbd5e1; line-height: 1.4; }

      .solved-list-wrap {
        overflow-y: auto; max-height: 52vh; padding-right: 4px; display: flex; flex-direction: column; gap: 10px;
      }
      .solved-list-wrap::-webkit-scrollbar { width: 6px; }
      .solved-list-wrap::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.2); border-radius: 10px; }

      .solved-item {
        background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px; padding: 12px 16px; display: flex; align-items: center;
        justify-content: space-between; gap: 14px; transition: all .15s;
      }
      .solved-item:hover {
        background: rgba(30, 41, 59, 0.7); border-color: rgba(56, 189, 248, 0.4);
      }
      .solved-item-main { flex: 1; min-width: 0; }
      .solved-item-title-row { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
      .solved-item-slug {
        font-family: monospace; font-size: 0.72rem; background: rgba(255, 255, 255, 0.08);
        color: #94a3b8; padding: 2px 6px; border-radius: 4px;
      }
      .solved-item-title {
        font-size: 0.95rem; font-weight: 700; color: #f1f5f9; margin: 0;
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
      }
      .solved-item-meta {
        display: flex; align-items: center; gap: 10px; font-size: 0.78rem; color: #94a3b8; margin-bottom: 6px; flex-wrap: wrap;
      }
      .solved-badge {
        padding: 1px 7px; border-radius: 6px; font-size: 0.72rem; font-weight: 700;
      }
      .badge-done { background: rgba(16, 185, 129, 0.2); color: #34d399; }
      .badge-prog { background: rgba(56, 189, 248, 0.2); color: #38bdf8; }
      .solved-progress-bar {
        width: 100%; height: 5px; background: rgba(255, 255, 255, 0.1); border-radius: 10px; overflow: hidden;
      }
      .solved-progress-fill {
        height: 100%; background: linear-gradient(90deg, #38bdf8, #34d399); transition: width .3s;
      }
      .solved-item-btn {
        background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.35);
        color: #38bdf8; font-size: 0.82rem; font-weight: 700; padding: 8px 14px;
        border-radius: 10px; text-decoration: none; white-space: nowrap; transition: all .15s;
      }
      .solved-item-btn:hover { background: #38bdf8; color: #0b1020; }

      .library-empty {
        text-align: center; padding: 40px 16px; color: #94a3b8;
      }

      /* Global Toast */
      .mathedu-toast {
        position: fixed; bottom: 28px; left: 50%; transform: translateX(-50%) translateY(100px);
        background: #1e293b; border: 1px solid rgba(56, 189, 248, 0.4); border-radius: 30px;
        padding: 10px 22px; color: #f1f5f9; font-size: 0.9rem; font-weight: 600;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); z-index: 9999999;
        display: flex; align-items: center; gap: 8px; transition: transform .3s ease, opacity .3s;
        opacity: 0; pointer-events: none;
      }
      .mathedu-toast.show {
        transform: translateX(-50%) translateY(0); opacity: 1; pointer-events: auto;
      }
    `;
    document.head.appendChild(style);
  }

  // 초기화 실행
  function init() {
    injectStyles();
    updateNavAuthUI();
    loadGoogleGsi();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  window.MatheduAuth = MatheduAuth;

})(window);
