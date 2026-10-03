/**
 * mathedu-gamification.js — 학생과 교사를 위한 게이미피케이션 & 학습 보관함 & 수업 도구 엔진
 * 
 * [학생 기능]
 * 1. 🔥 연속 학습 스트릭 (Daily Learning Streak): 매일 문제 풀이 시 스트릭 누적 & 축하
 * 2. 🏆 경험치(XP) & 수학 칭호 레벨 시스템 (Lv.1 디딤돌 입문자 ~ Lv.5 수능 정복자)
 * 3. 🎖️ 성취 뱃지 컬렉션 (첫 디딤돌, 기하의 눈, 완벽주의자, 스트릭 불꽃 등)
 * 4. 🎉 Canvas Confetti 축하 폭죽 파티클 (외부 의존성 제로 순수 인라인 캔버스)
 * 5. 🔴 오답노트 자동 수집 및 재도전 연동
 * 6. ⭐ 핵심 문제 북마크 / 즐겨찾기
 * 
 * [교사 기능]
 * 1. 📦 오늘의 수업 큐레이션 세트 (Lesson Pack) 진도 연동 (?pack=slug1,slug2,...)
 * 2. 🖨️ A4 시험지 / 학습지 최적화 인쇄 모드 (Print Worksheet Mode)
 * 3. 🖥️ 교실 칠판 / 빔프로젝터 고대비 판서 모드 (Chalkboard Mode)
 */

(function(window) {
  'use strict';

  var STREAK_KEY = 'mathedu_streak_data';
  var XP_KEY = 'mathedu_user_xp';
  var BADGES_KEY = 'mathedu_unlocked_badges';
  var WRONG_KEY = 'mathedu_wrong_answers';
  var BOOKMARKS_KEY = 'mathedu_bookmarks';

  // 🌐 i18n 헬퍼 함수
  function isEnMode() {
    var l = (typeof document !== 'undefined' && document.documentElement && document.documentElement.lang) ? document.documentElement.lang : '';
    return l.toLowerCase().startsWith('en');
  }

  function bilingual(ko, en) {
    return '<span class="bilingual-ko">' + ko + '</span><span class="bilingual-en">' + en + '</span>';
  }

  function escapeHtml(s) {
    return String(s || '').replace(/[&<>"']/g, function(c) {
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
    });
  }

  // 1. 레벨 테이블
  var LEVELS = [
    { level: 1, title: '🔰 디딤돌 입문자', titleEn: '🔰 Scaffolding Novice', minXP: 0, maxXP: 99 },
    { level: 2, title: '🌿 수식 탐험가', titleEn: '🌿 Formula Explorer', minXP: 100, maxXP: 299 },
    { level: 3, title: '💡 원리 분석가', titleEn: '💡 Principle Analyst', minXP: 300, maxXP: 599 },
    { level: 4, title: '📐 기하 마스터', titleEn: '📐 Geometry Master', minXP: 600, maxXP: 999 },
    { level: 5, title: '👑 수능 정복자', titleEn: '👑 Exam Conqueror', minXP: 1000, maxXP: 999999 }
  ];

  // 2. 뱃지 마스터 정의
  var ALL_BADGES = [
    { id: 'first_step', icon: '🔰', title: '첫 발자국', titleEn: 'First Step', desc: '첫 번째 디딤돌 문제를 정답으로 통과함', descEn: 'Passed the first stepping stone question' },
    { id: 'full_clear', icon: '🎯', title: '완전 정복', titleEn: 'Full Clear', desc: '수능·모평 본문항까지 모든 단계를 완주함', descEn: 'Completed all steps through the main exam problem' },
    { id: 'perfect_run', icon: '🛡️', title: '완벽주의자', titleEn: 'Perfectionist', desc: '오답 없이 한 번에 모든 단계를 클리어함', descEn: 'Cleared all steps on the first attempt with zero mistakes' },
    { id: 'streak_3', icon: '🔥', title: '열정의 불꽃', titleEn: 'Flame of Passion', desc: '3일 연속으로 수학 문제를 풀이함', descEn: 'Solved math problems 3 days in a row' },
    { id: 'streak_7', icon: '⚡', title: '수학의 달인', titleEn: 'Math Master', desc: '7일 연속 학습 스트릭을 달성함', descEn: 'Maintained a 7-day daily study streak' },
    { id: 'min7014_explorer', icon: '📐', title: '기하의 눈', titleEn: 'Eye of Geometry', desc: 'min7014의 GeoGebra 증명 자료를 3회 이상 탐구함', descEn: "Explored min7014 GeoGebra proofs 3+ times" },
    { id: 'review_master', icon: '🔄', title: '복습의 제왕', titleEn: 'King of Review', desc: '오답노트에 기록된 문제를 다시 풀어 극복함', descEn: 'Conquered and solved problems from the Review Vault' }
  ];

  var MatheduGame = {
    // === 날짜 유틸 (KST 기준) ===
    getTodayStr: function() {
      var now = new Date();
      var kst = new Date(now.getTime() + (9 * 60 * 60 * 1000));
      return kst.toISOString().slice(0, 10);
    },

    // === 1. 연속 출석 스트릭 (Streak) ===
    getStreak: function() {
      try {
        var raw = localStorage.getItem(STREAK_KEY);
        if (!raw) return { count: 0, lastDate: '', activeToday: false };
        var data = JSON.parse(raw);
        var today = MatheduGame.getTodayStr();
        var activeToday = (data.lastDate === today);
        return {
          count: data.count || 0,
          lastDate: data.lastDate || '',
          activeToday: activeToday
        };
      } catch (e) {
        return { count: 0, lastDate: '', activeToday: false };
      }
    },

    recordActivity: function() {
      try {
        var current = MatheduGame.getStreak();
        var today = MatheduGame.getTodayStr();
        if (current.lastDate === today) {
          return current; // 오늘 이미 출석 반영됨
        }

        var newCount = 1;
        if (current.lastDate) {
          var last = new Date(current.lastDate);
          var cur = new Date(today);
          var diffDays = Math.round((cur - last) / (1000 * 60 * 60 * 24));
          if (diffDays === 1) {
            newCount = current.count + 1; // 어제 풀고 오늘 풀었으면 1 증가
          } else if (diffDays === 0) {
            newCount = current.count;
          }
        }

        var updated = { count: newCount, lastDate: today };
        localStorage.setItem(STREAK_KEY, JSON.stringify(updated));

        // 스트릭 뱃지 판정
        if (newCount >= 3) MatheduGame.unlockBadge('streak_3');
        if (newCount >= 7) MatheduGame.unlockBadge('streak_7');

        window.dispatchEvent(new CustomEvent('mathedu:streak-updated', { detail: updated }));
        return { count: newCount, lastDate: today, activeToday: true };
      } catch (e) {
        return { count: 1, lastDate: '', activeToday: true };
      }
    },

    // === 2. 경험치(XP) & 레벨 시스템 ===
    getXP: function() {
      try {
        return parseInt(localStorage.getItem(XP_KEY) || '0', 10);
      } catch (e) {
        return 0;
      }
    },

    addXP: function(amount, reason) {
      if (!amount || amount <= 0) return;
      var cur = MatheduGame.getXP();
      var next = cur + amount;
      try {
        localStorage.setItem(XP_KEY, String(next));
      } catch (e) {}

      var oldLv = MatheduGame.getLevelInfo(cur);
      var newLv = MatheduGame.getLevelInfo(next);

      MatheduGame.showToastXP(amount, reason);

      if (newLv.level > oldLv.level) {
        MatheduGame.showLevelUpModal(newLv);
      }

      window.dispatchEvent(new CustomEvent('mathedu:xp-updated', { detail: { xp: next, level: newLv } }));
      return next;
    },

    getLevelInfo: function(customXP) {
      var xp = (typeof customXP === 'number') ? customXP : MatheduGame.getXP();
      for (var i = LEVELS.length - 1; i >= 0; i--) {
        if (xp >= LEVELS[i].minXP) {
          var curLv = LEVELS[i];
          var nextLv = LEVELS[i + 1] || null;
          var span = nextLv ? (nextLv.minXP - curLv.minXP) : 1000;
          var curProgress = nextLv ? (xp - curLv.minXP) : span;
          var pct = nextLv ? Math.min(100, Math.round((curProgress / span) * 100)) : 100;
          return {
            level: curLv.level,
            title: curLv.title,
            currentXP: xp,
            minXP: curLv.minXP,
            nextXP: nextLv ? nextLv.minXP : null,
            progressPct: pct
          };
        }
      }
      return { level: 1, title: LEVELS[0].title, currentXP: xp, minXP: 0, nextXP: 100, progressPct: 0 };
    },

    // === 3. 뱃지 시스템 ===
    getUnlockedBadges: function() {
      try {
        return JSON.parse(localStorage.getItem(BADGES_KEY) || '[]');
      } catch (e) {
        return [];
      }
    },

    unlockBadge: function(badgeId) {
      var unlocked = MatheduGame.getUnlockedBadges();
      if (unlocked.indexOf(badgeId) !== -1) return false;
      unlocked.push(badgeId);
      try {
        localStorage.setItem(BADGES_KEY, JSON.stringify(unlocked));
      } catch (e) {}

      var target = ALL_BADGES.find(function(b) { return b.id === badgeId; });
      if (target) {
        MatheduGame.showBadgeUnlockToast(target);
      }
      window.dispatchEvent(new CustomEvent('mathedu:badge-unlocked', { detail: { badgeId: badgeId } }));
      return true;
    },

    // === 4. 오답노트 (Wrong Answers Vault) ===
    recordWrongAnswer: function(slug, qIdx, title) {
      if (!slug) return;
      try {
        var map = JSON.parse(localStorage.getItem(WRONG_KEY) || '{}');
        if (!map[slug]) {
          map[slug] = {
            slug: slug,
            title: title || slug,
            wrongSteps: [],
            count: 0,
            lastAt: new Date().toISOString()
          };
        }
        if (typeof qIdx === 'number' && map[slug].wrongSteps.indexOf(qIdx) === -1) {
          map[slug].wrongSteps.push(qIdx);
        }
        map[slug].count = (map[slug].count || 0) + 1;
        map[slug].lastAt = new Date().toISOString();
        localStorage.setItem(WRONG_KEY, JSON.stringify(map));
        window.dispatchEvent(new CustomEvent('mathedu:wrong-updated'));
      } catch (e) {}
    },

    getWrongAnswers: function() {
      try {
        var map = JSON.parse(localStorage.getItem(WRONG_KEY) || '{}');
        return Object.values(map);
      } catch (e) {
        return [];
      }
    },

    clearWrongAnswer: function(slug) {
      try {
        var map = JSON.parse(localStorage.getItem(WRONG_KEY) || '{}');
        if (map[slug]) {
          delete map[slug];
          localStorage.setItem(WRONG_KEY, JSON.stringify(map));
          MatheduGame.unlockBadge('review_master');
          window.dispatchEvent(new CustomEvent('mathedu:wrong-updated'));
        }
      } catch (e) {}
    },

    // === 5. 북마크 / 즐겨찾기 ===
    getBookmarks: function() {
      try {
        return JSON.parse(localStorage.getItem(BOOKMARKS_KEY) || '[]');
      } catch (e) {
        return [];
      }
    },

    isBookmarked: function(slug) {
      if (!slug) return false;
      return MatheduGame.getBookmarks().indexOf(slug) !== -1;
    },

    toggleBookmark: function(slug) {
      if (!slug) return false;
      var list = MatheduGame.getBookmarks();
      var idx = list.indexOf(slug);
      var state = false;
      if (idx !== -1) {
        list.splice(idx, 1);
        state = false;
      } else {
        list.unshift(slug);
        state = true;
      }
      try {
        localStorage.setItem(BOOKMARKS_KEY, JSON.stringify(list));
      } catch (e) {}
      window.dispatchEvent(new CustomEvent('mathedu:bookmarks-updated', { detail: { slug: slug, bookmarked: state } }));
      return state;
    },

    // === 6. 순수 JavaScript Canvas Confetti 폭죽 파티클 엔진 ===
    triggerConfetti: function(durationMs) {
      durationMs = durationMs || 3000;
      var canvas = document.getElementById('matheduConfettiCanvas');
      if (!canvas) {
        canvas = document.createElement('canvas');
        canvas.id = 'matheduConfettiCanvas';
        canvas.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:999999;';
        document.body.appendChild(canvas);
      }
      var ctx = canvas.getContext('2d');
      var width = window.innerWidth;
      var height = window.innerHeight;
      canvas.width = width;
      canvas.height = height;

      var colors = ['#7cc4ff', '#a78bfa', '#5eead4', '#fde68a', '#f472b6', '#38bdf8', '#34d399'];
      var particles = [];
      var count = 120;

      for (var i = 0; i < count; i++) {
        particles.push({
          x: width * (0.3 + Math.random() * 0.4),
          y: height * 0.5,
          vx: (Math.random() - 0.5) * 16,
          vy: (Math.random() - 0.8) * 18,
          size: 6 + Math.random() * 6,
          color: colors[Math.floor(Math.random() * colors.length)],
          rotation: Math.random() * 360,
          rotSpeed: (Math.random() - 0.5) * 12,
          gravity: 0.35 + Math.random() * 0.2,
          opacity: 1
        });
      }

      var startTime = Date.now();
      function render() {
        var elapsed = Date.now() - startTime;
        ctx.clearRect(0, 0, width, height);

        var alive = 0;
        particles.forEach(function(p) {
          p.x += p.vx;
          p.y += p.vy;
          p.vy += p.gravity;
          p.rotation += p.rotSpeed;
          p.vx *= 0.98;

          if (elapsed > durationMs - 1000) {
            p.opacity = Math.max(0, 1 - (elapsed - (durationMs - 1000)) / 1000);
          }

          if (p.opacity > 0 && p.y < height + 50) {
            alive++;
            ctx.save();
            ctx.translate(p.x, p.y);
            ctx.rotate((p.rotation * Math.PI) / 180);
            ctx.globalAlpha = p.opacity;
            ctx.fillStyle = p.color;
            ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.6);
            ctx.restore();
          }
        });

        if (alive > 0 && elapsed < durationMs) {
          requestAnimationFrame(render);
        } else {
          ctx.clearRect(0, 0, width, height);
          if (canvas.parentNode) canvas.parentNode.removeChild(canvas);
        }
      }
      requestAnimationFrame(render);
    },

    // === UI 토스트 & 모달 연출 ===
    showToastXP: function(amount, reason) {
      var toast = document.createElement('div');
      toast.style.cssText = 'position:fixed;bottom:80px;left:50%;transform:translateX(-50%);z-index:999999;background:linear-gradient(90deg,rgba(124,196,255,.95),rgba(167,139,250,.95));color:#0b1020;padding:10px 22px;border-radius:30px;font-weight:800;font-size:0.95rem;box-shadow:0 10px 30px rgba(0,0,0,.5);display:flex;align-items:center;gap:8px;animation:matheduPopUp .3s ease;pointer-events:none;font-family:system-ui,sans-serif';
      toast.innerHTML = '⚡ <b>+' + amount + ' XP</b> ' + (reason ? ('<span style="font-size:0.82rem;font-weight:600;color:#1e293b">(' + reason + ')</span>') : '');
      document.body.appendChild(toast);
      setTimeout(function() {
        toast.style.transition = 'opacity .4s ease, transform .4s ease';
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(-50%) translateY(-10px)';
        setTimeout(function() { toast.remove(); }, 400);
      }, 1600);
    },

    showBadgeUnlockToast: function(badge) {
      var toast = document.createElement('div');
      toast.style.cssText = 'position:fixed;top:24px;right:24px;z-index:999999;background:#141833;border:1.5px solid #fde68a;border-radius:16px;padding:14px 18px;color:#fff;box-shadow:0 12px 40px rgba(0,0,0,.6);display:flex;align-items:center;gap:12px;animation:matheduSlideIn .3s ease;font-family:system-ui,sans-serif;max-width:320px';
      var bTitle = isEnMode() ? (badge.titleEn || badge.title) : badge.title;
      var bDesc = isEnMode() ? (badge.descEn || badge.desc) : badge.desc;
      toast.innerHTML = 
        '<div style="font-size:2rem">' + badge.icon + '</div>' +
        '<div>' +
          '<div style="font-size:0.75rem;color:#fde68a;font-weight:800">' + bilingual('🎉 새로운 뱃지 획득!', '🎉 New Badge Unlocked!') + '</div>' +
          '<div style="font-size:0.95rem;font-weight:700">' + escapeHtml(bTitle) + '</div>' +
          '<div style="font-size:0.78rem;color:#94a3b8">' + escapeHtml(bDesc) + '</div>' +
        '</div>';
      document.body.appendChild(toast);
      MatheduGame.triggerConfetti(2000);
      setTimeout(function() {
        toast.style.transition = 'opacity .4s ease, transform .4s ease';
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(-10px)';
        setTimeout(function() { toast.remove(); }, 400);
      }, 4000);
    },

    showLevelUpModal: function(levelInfo) {
      var modal = document.createElement('div');
      modal.style.cssText = 'position:fixed;inset:0;z-index:9999999;background:rgba(10,13,26,.85);backdrop-filter:blur(16px);display:flex;align-items:center;justify-content:center;padding:16px;animation:matheduFadeIn .2s ease;font-family:system-ui,sans-serif';
      var lvTitle = isEnMode() ? (levelInfo.titleEn || levelInfo.title) : levelInfo.title;
      modal.innerHTML = 
        '<div style="background:#141833;border:2px solid #5eead4;border-radius:24px;max-width:440px;width:100%;padding:32px 24px;text-align:center;color:#fff;box-shadow:0 24px 60px rgba(0,0,0,.7);position:relative">' +
          '<div style="font-size:3.5rem;margin-bottom:8px">👑</div>' +
          '<div style="display:inline-block;background:rgba(94,234,212,.2);color:#5eead4;border:1px solid #5eead4;padding:4px 14px;border-radius:20px;font-size:0.8rem;font-weight:800;margin-bottom:10px">LEVEL UP!</div>' +
          '<h2 style="font-size:1.6rem;margin:0 0 10px;background:linear-gradient(90deg,#5eead4,#7cc4ff);-webkit-background-clip:text;background-clip:text;color:transparent">' + escapeHtml(lvTitle) + '</h2>' +
          '<p style="color:#cbd5e1;font-size:0.92rem;line-height:1.6;margin-bottom:24px">' +
            bilingual('축하합니다! 수학적 원리와 디딤돌을 성실하게 정복하여 <b>레벨 ' + levelInfo.level + '</b>로 승급하셨습니다.', 'Congratulations! You mastered mathematical principles and scaffolding steps to reach <b>Level ' + levelInfo.level + '</b>.') +
          '</p>' +
          '<button onclick="this.closest(\'div\').parentElement.remove()" style="background:linear-gradient(90deg,#5eead4,#38bdf8);color:#0b1020;border:none;border-radius:12px;padding:12px 32px;font-size:1rem;font-weight:800;cursor:pointer">' +
            bilingual('계속 도전하기 ➔', 'Continue Practice ➔') +
          '</button>' +
        '</div>';
      document.body.appendChild(modal);
      MatheduGame.triggerConfetti(3500);
    },

    showBadgesModal: function() {
      var unlocked = MatheduGame.getUnlockedBadges();
      var modal = document.createElement('div');
      modal.id = 'matheduBadgesModal';
      modal.style.cssText = 'position:fixed;inset:0;z-index:999999;background:rgba(10,13,26,.85);backdrop-filter:blur(16px);display:flex;align-items:center;justify-content:center;padding:16px;animation:matheduFadeIn .2s ease;font-family:system-ui,sans-serif';

      var badgesHtml = ALL_BADGES.map(function(b) {
        var isUnlocked = unlocked.indexOf(b.id) !== -1;
        var bTitle = isEnMode() ? (b.titleEn || b.title) : b.title;
        var bDesc = isEnMode() ? (b.descEn || b.desc) : b.desc;
        var badgeStatus = isUnlocked ? bilingual(' <span style="font-size:0.75rem;color:#5eead4">✓ 획득</span>', ' <span style="font-size:0.75rem;color:#5eead4">✓ Unlocked</span>') : '';
        return (
          '<div style="background:' + (isUnlocked ? 'rgba(124,196,255,.12)' : 'rgba(255,255,255,.04)') + ';' +
                      'border:1px solid ' + (isUnlocked ? 'rgba(124,196,255,.4)' : 'rgba(255,255,255,.1)') + ';' +
                      'border-radius:14px;padding:14px;display:flex;align-items:center;gap:12px;' +
                      (isUnlocked ? '' : 'filter:grayscale(1);opacity:.5') + '">' +
            '<div style="font-size:2rem">' + b.icon + '</div>' +
            '<div style="flex:1">' +
              '<div style="font-size:0.95rem;font-weight:700;color:' + (isUnlocked ? '#7cc4ff' : '#94a3b8') + '">' +
                escapeHtml(bTitle) + badgeStatus +
              '</div>' +
              '<div style="font-size:0.78rem;color:#aab4d4;margin-top:2px">' + escapeHtml(bDesc) + '</div>' +
            '</div>' +
          '</div>'
        );
      }).join('');

      var lv = MatheduGame.getLevelInfo();
      var streak = MatheduGame.getStreak();
      var lvTitle = isEnMode() ? (lv.titleEn || lv.title) : lv.title;

      modal.innerHTML = 
        '<div style="background:#141833;border:1.5px solid rgba(124,196,255,.35);border-radius:22px;max-width:560px;width:100%;max-height:85vh;overflow-y:auto;padding:26px;color:#fff;box-shadow:0 24px 60px rgba(0,0,0,.7);position:relative">' +
          '<button onclick="document.getElementById(\'matheduBadgesModal\').remove()" style="position:absolute;top:18px;right:18px;background:none;border:none;color:#94a3b8;font-size:1.5rem;cursor:pointer">✕</button>' +
          '<div style="display:flex;align-items:center;gap:10px;margin-bottom:14px">' +
            '<span style="font-size:1.8rem">🏆</span>' +
            '<div>' +
              '<h2 style="font-size:1.35rem;margin:0;background:linear-gradient(90deg,#7cc4ff,#a78bfa);-webkit-background-clip:text;background-clip:text;color:transparent">' +
                bilingual('나의 수학 업적 & 명예의 전당', 'My Math Badges & Hall of Fame') +
              '</h2>' +
              '<div style="font-size:0.82rem;color:#94a3b8;margin-top:2px">' +
                bilingual(
                  '현재 레벨: <b>' + escapeHtml(lv.title) + '</b> (총 <b>' + lv.currentXP + ' XP</b>) · 연속 출석: <b>' + streak.count + '일</b>',
                  'Current Level: <b>' + escapeHtml(lvTitle) + '</b> (Total <b>' + lv.currentXP + ' XP</b>) · Streak: <b>' + streak.count + ' days</b>'
                ) +
              '</div>' +
            '</div>' +
          '</div>' +
          '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:10px;margin-top:16px">' +
            badgesHtml +
          '</div>' +
        '</div>';

      document.body.appendChild(modal);
    },

    // === 7. 교사용 A4 시험지 / 학습지 최적화 인쇄 모드 ===
    printWorksheet: function() {
      // 인쇄용 스타일 주입
      var styleId = 'matheduWorksheetPrintStyle';
      var existing = document.getElementById(styleId);
      if (!existing) {
        var style = document.createElement('style');
        style.id = styleId;
        style.innerHTML = 
          '@media print {' +
            'body { background: #fff !important; color: #000 !important; font-family: "Malgun Gothic", serif !important; padding: 0 !important; }' +
            '.topbar, .brand-btn, #copyBtn, .score, #trackSubmit, #trackFull, .exp-toggle-btn, .exp, .report-wrap, #problemResumeBanner, .teacher-class-banner, #floatClassBtn, #btnTeacherTopbar, #btnOfflineTopbar, #btnMyLibraryTopbar, .final button, .lesson-pack-nav-bar { display: none !important; }' +
            '.wrap { max-width: 100% !important; padding: 0 !important; margin: 0 !important; }' +
            'h1 { color: #000 !important; font-size: 1.4rem !important; border-bottom: 2px solid #000; padding-bottom: 6px; margin-bottom: 12px; }' +
            'h2 { color: #000 !important; font-size: 1.1rem !important; border-left: 4px solid #333 !important; padding-left: 8px; margin-top: 20px !important; }' +
            '.lead { color: #555 !important; font-size: 0.85rem !important; }' +
            '.orig-card, .know, .q, .sol { background: #fff !important; border: 1px solid #ccc !important; box-shadow: none !important; color: #000 !important; backdrop-filter: none !important; }' +
            '.sym div { background: #f8f8f8 !important; border: 1px solid #ddd !important; color: #000 !important; }' +
            '.opt { background: #fff !important; border: 1px solid #bbb !important; color: #000 !important; }' +
            '.opt .n { background: #e0e0e0 !important; color: #000 !important; }' +
            '.worksheet-notes-box { display: block !important; border: 1px dashed #999; border-radius: 8px; height: 140px; margin: 12px 0; padding: 8px; color: #777; font-size: 0.8rem; }' +
            '.min7014-addon-card { border: 1px solid #ccc !important; background: #fafafa !important; color: #000 !important; page-break-inside: avoid; }' +
            '.min-header-title { color: #000 !important; }' +
            '.min-item { background: #fff !important; border: 1px solid #ddd !important; color: #000 !important; }' +
            '.min-item-title { color: #000 !important; }' +
          '}';
        document.head.appendChild(style);
      }

      // 학생 풀이 여백 박스 삽입 (인쇄용)
      var origCard = document.querySelector('.orig-card');
      if (origCard && !document.getElementById('worksheetNoteBox')) {
        var noteBox = document.createElement('div');
        noteBox.id = 'worksheetNoteBox';
        noteBox.className = 'worksheet-notes-box';
        noteBox.style.display = 'none';
        noteBox.innerHTML = bilingual('✏️ <b>[학생 풀이 및 증명 필기 공간]</b>', '✏️ <b>[Student Scratch & Proof Work Area]</b>');
        origCard.parentNode.insertBefore(noteBox, origCard.nextSibling);
      }

      window.print();
    },

    // === 8. 교실 칠판 / 빔프로젝터 고대비 판서 모드 (Chalkboard Mode) ===
    toggleChalkboardMode: function() {
      var isChalk = document.body.classList.toggle('mathedu-chalkboard-mode');
      var btn = document.getElementById('btnChalkboardModeTopbar');
      if (btn) {
        btn.innerHTML = isChalk ? bilingual('🖥️ 일반 화면', '🖥️ Normal View') : bilingual('🖥️ 칠판 모드', '🖥️ Board Mode');
      }

      var styleId = 'matheduChalkboardStyle';
      var style = document.getElementById(styleId);
      if (!style) {
        style = document.createElement('style');
        style.id = styleId;
        style.innerHTML = 
          '.mathedu-chalkboard-mode {' +
            'background: #0f1c15 !important;' +
            'color: #f1f5f9 !important;' +
          '}' +
          '.mathedu-chalkboard-mode .q, .mathedu-chalkboard-mode .orig-card {' +
            'background: #172d22 !important;' +
            'border: 2px solid #5eead4 !important;' +
            'font-size: 1.15rem !important;' +
          '}' +
          '.mathedu-chalkboard-mode .stem {' +
            'font-size: 1.25rem !important;' +
            'line-height: 1.8 !important;' +
          '}' +
          '.mathedu-chalkboard-mode .opt {' +
            'font-size: 1.15rem !important;' +
            'padding: 14px 18px !important;' +
            'background: #1f3b2d !important;' +
          '}';
        document.head.appendChild(style);
      }
    }
  };

  // 애니메이션 키프레임 인라인 등록
  var animStyle = document.createElement('style');
  animStyle.innerHTML = 
    '@keyframes matheduPopUp { from { opacity:0; transform:translateX(-50%) scale(.85); } to { opacity:1; transform:translateX(-50%) scale(1); } }' +
    '@keyframes matheduSlideIn { from { opacity:0; transform:translateX(40px); } to { opacity:1; transform:translateX(0); } }' +
    '@keyframes matheduFadeIn { from { opacity:0; } to { opacity:1; } }';
  document.head.appendChild(animStyle);

  window.MatheduGame = MatheduGame;
})(window);
