/**
 * mathedu-search-logger.js
 * ============================================================================
 * 사용자 검색어 분리 수집 · 수요 분석 및 미충족(0건) 수학 수업자료 자동 제작 연계 로거
 * - index.html (상단 통합검색 / 16,548문항 검색 / 3,400+ 증명 모달 검색)
 * - video_board.html (927+ 설명 영상 게시판 검색)
 * ============================================================================
 */
(function (window, document) {
  'use strict';

  if (window.MatheduSearchLogger) return;

  var API_FALLBACK =
    'https://script.google.com/macros/s/AKfycbxQBW1hKYFSHokaVJMRql-UJpk0t4qMeWMiiy_RFuCLZ5SE4iZytYQkGa9_yoCmm1Ak0Q/exec';
  var SESSION_DEDUP_KEY = 'mathedu_search_logged_session_v1';
  var LOCAL_HISTORY_KEY = 'mathedu_user_search_history_v1';
  var _debounceTimers = {};

  function getLang() {
    if (window.MatheduI18n && typeof window.MatheduI18n.getLanguage === 'function') {
      return window.MatheduI18n.getLanguage() === 'en' ? 'EN' : 'KO';
    }
    var hl = (document.documentElement.lang || 'ko').toLowerCase();
    return hl.indexOf('en') === 0 ? 'EN' : 'KO';
  }

  function isMeaningfulQuery(raw) {
    var q = String(raw || '').trim();
    if (q.length < 2 || q.length > 80) return false;
    // 완성되지 않은 단독 자모 연타 제외
    if (/^[ㄱ-ㅎㅏ-ㅣ\s]+$/.test(q)) return false;
    // 특수기호/숫자 1개만 있는 경우 제외
    var stripped = q.replace(/[\s\.,\?!~_\-+*/=()\[\]{}]+/g, '');
    if (stripped.length < 2) return false;
    return true;
  }

  function wasLoggedInSession(dedupSig) {
    try {
      var map = JSON.parse(sessionStorage.getItem(SESSION_DEDUP_KEY) || '{}');
      return !!map[dedupSig];
    } catch (e) {
      return false;
    }
  }

  function markLoggedInSession(dedupSig) {
    try {
      var map = JSON.parse(sessionStorage.getItem(SESSION_DEDUP_KEY) || '{}');
      map[dedupSig] = Date.now();
      sessionStorage.setItem(SESSION_DEDUP_KEY, JSON.stringify(map));
    } catch (e) {}
  }

  function appendLocalHistory(entry) {
    try {
      var arr = JSON.parse(localStorage.getItem(LOCAL_HISTORY_KEY) || '[]');
      if (!Array.isArray(arr)) arr = [];
      arr.push(entry);
      localStorage.setItem(LOCAL_HISTORY_KEY, JSON.stringify(arr.slice(-50)));
    } catch (e) {}
  }

  function sendBeaconToBackend(slug, totalHits, senderTag, formattedText) {
    var apiUrl = window._sheetsApiUrl || API_FALLBACK;
    var url =
      apiUrl +
      '?action=report' +
      '&quiz=' + encodeURIComponent(slug) +
      '&q=' + encodeURIComponent(String(totalHits)) +
      '&name=' + encodeURIComponent(senderTag) +
      '&text=' + encodeURIComponent(formattedText) +
      '&_t=' + Date.now();

    function fallbackImg() {
      try {
        var img = new Image();
        img.src = url;
      } catch (e) {}
    }

    try {
      if (typeof fetch === 'function') {
        fetch(url, {
          method: 'GET',
          mode: 'no-cors',
          cache: 'no-store',
          keepalive: true
        }).catch(fallbackImg);
      } else {
        fallbackImg();
      }
    } catch (e) {
      fallbackImg();
    }
  }

  function logQuery(rawQuery, meta) {
    var q = String(rawQuery || '').trim().replace(/\s+/g, ' ');
    if (!isMeaningfulQuery(q)) return false;

    var opts = meta || {};
    var proofHits = Math.max(0, parseInt(opts.proofHits || 0, 10) || 0);
    var quizHits = Math.max(0, parseInt(opts.quizHits || 0, 10) || 0);
    var videoHits = Math.max(0, parseInt(opts.videoHits || 0, 10) || 0);
    var totalHits =
      typeof opts.totalHits === 'number'
        ? Math.max(0, opts.totalHits)
        : proofHits + quizHits + videoHits;
    var source = String(opts.source || 'web_search');
    var priority = !!opts.priority;
    var lang = getLang();

    var dedupSig = q.toLowerCase() + '|' + (totalHits === 0 ? 'gap' : 'hit') + '|' + (priority ? 'prio' : 'auto');
    if (!priority && wasLoggedInSession(dedupSig)) {
      return false;
    }
    markLoggedInSession(dedupSig);

    var slug = totalHits === 0 || priority ? '_search_gap' : '_search_log';
    var senderTag = lang + '|' + source;
    var formatted =
      '[검색어] ' + q +
      '\n[매칭수] 총:' + totalHits + ' (증명:' + proofHits + ' / 문항:' + quizHits + ' / 영상:' + videoHits + ')' +
      '\n[언어] ' + lang +
      '\n[출처] ' + source +
      '\n[우선요청] ' + (priority ? 'Y' : 'N');

    appendLocalHistory({
      ts: new Date().toISOString(),
      query: q,
      totalHits: totalHits,
      proofHits: proofHits,
      quizHits: quizHits,
      videoHits: videoHits,
      lang: lang,
      source: source,
      priority: priority
    });

    sendBeaconToBackend(slug, totalHits, senderTag, formatted);
    return true;
  }

  function scheduleLog(channelKey, rawQuery, computeMetaFn, delayMs) {
    var key = String(channelKey || 'default');
    if (_debounceTimers[key]) {
      clearTimeout(_debounceTimers[key]);
      delete _debounceTimers[key];
    }
    var q = String(rawQuery || '').trim();
    if (!isMeaningfulQuery(q)) return;

    _debounceTimers[key] = setTimeout(function () {
      delete _debounceTimers[key];
      var meta = typeof computeMetaFn === 'function' ? computeMetaFn(q) : (computeMetaFn || {});
      logQuery(q, meta);
    }, typeof delayMs === 'number' ? delayMs : 1800);
  }

  function requestPriorityMaterial(rawQuery, source, btnEl) {
    var q = String(rawQuery || '').trim();
    if (!isMeaningfulQuery(q)) return;
    logQuery(q, {
      totalHits: 0,
      proofHits: 0,
      quizHits: 0,
      videoHits: 0,
      source: source || 'zero_result_request',
      priority: true
    });
    if (btnEl) {
      var isEn = getLang() === 'EN';
      btnEl.disabled = true;
      btnEl.textContent = isEn
        ? '✅ Requested! Lesson creation queued'
        : '✅ 수업자료 제작 요청 접수 완료!';
      btnEl.style.opacity = '0.85';
    }
  }

  window.MatheduSearchLogger = {
    logQuery: logQuery,
    scheduleLog: scheduleLog,
    requestPriorityMaterial: requestPriorityMaterial
  };
})(window, document);
