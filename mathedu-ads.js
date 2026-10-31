/*!
 * mathedu-ads.js — Clean EdTech Ad Monetization & In-Game Rewarded Sponsor Engine
 * Managed by: finance agent (in collaboration with mathteacher, gamemaker, designer, pr)
 * Principle: 100% Free-to-Learn forever for students & teachers, sustained by clean,
 * non-intrusive native banners (Google AdSense / Kakao AdFit) & voluntary Rewarded Ad Chests.
 */
(function () {
  'use strict';

  var STORAGE_KEY = 'mathedu_ad_engine_v1';

  var defaultConfig = {
    adsenseClient: 'ca-pub-0000000000000000',
    adsenseSlotMain: '1234567890',
    adfitUnitId: 'DAN-0000000000000000',
    impressions: 0,
    rewardedWatches: 0,
    lastRewardTime: 0
  };

  function loadState() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return Object.assign({}, defaultConfig);
      var parsed = JSON.parse(raw);
      return Object.assign({}, defaultConfig, parsed);
    } catch (e) {
      return Object.assign({}, defaultConfig);
    }
  }

  function saveState(st) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(st));
    } catch (e) {}
  }

  var state = loadState();

  varEDUCATIONAL_SPONSORS = [
    {
      badge: '📐 공식 수학교육 아카이브 스폰서',
      title: '민은기 선생님의 수학자료실 (3,400+ 동적 기하 & 시각적 증명)',
      desc: '단델린의 구 원뿔곡선부터 미적분 리만 합까지, 눈으로 보고 즉시 깨닫는 인터랙티브 GeoGebra 수학 도서관',
      cta: '시각적 증명 도서관 탐험하기 →',
      url: 'https://min7014.github.io/'
    },
    {
      badge: '👑 수능 수학 100점 만점 챌린지 스폰서',
      title: '16,548문항 초등 눈높이 디딤돌 아카이브 — 친구와 3D 보스 결투하기!',
      desc: '막히는 4점 킬러 문항도 제0단계 기호 번역기와 폴리아 3단계 생각 징검다리로 스스로 정복하세요.',
      cta: '친구 도전장 링크 공유하기 →',
      action: 'pr'
    },
    {
      badge: '🏫 전국 수학교사 수업 나눔 스폰서',
      title: 'QR 코드 실시간 수학 교실 & 오프라인 단독 실행 퀴즈 패키지',
      desc: '인터넷이 없는 교실에서도 100% 작동하는 독립형 단계별 수학 퀴즈와 실시간 학생 진도 관제 보드',
      cta: '교사용 출제 스튜디오 열기 →',
      url: 'create.html'
    }
  ];

  function isRealAdsenseConfigured() {
    return (
      state.adsenseClient &&
      state.adsenseClient.indexOf('ca-pub-') === 0 &&
      state.adsenseClient !== 'ca-pub-0000000000000000'
    );
  }

  function isRealAdfitConfigured() {
    return (
      state.adfitUnitId &&
      state.adfitUnitId.indexOf('DAN-') === 0 &&
      state.adfitUnitId !== 'DAN-0000000000000000'
    );
  }

  function ensureAdStyles() {
    if (document.getElementById('matheduAdEngineStyles')) return;
    var st = document.createElement('style');
    st.id = 'matheduAdEngineStyles';
    st.textContent = [
      '.mathedu-clean-ad-wrap{margin:14px 0 6px;padding:12px 16px;border-radius:16px;background:linear-gradient(135deg,rgba(15,23,42,0.92),rgba(30,27,75,0.88));border:1px solid rgba(148,163,184,0.22);box-shadow:0 8px 24px rgba(2,6,23,0.22);color:#f8fafc;font-family:"Pretendard","Inter",sans-serif;display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;backdrop-filter:blur(12px);}',
      '.mathedu-ad-badge{display:inline-flex;align-items:center;gap:6px;padding:3px 9px;border-radius:999px;background:rgba(251,191,36,0.14);border:1px solid rgba(251,191,36,0.35);color:#fde68a;font-size:10.5px;font-weight:800;letter-spacing:0.03em;}',
      '.mathedu-ad-btn{padding:8px 13px;border-radius:11px;font-size:12px;font-weight:800;cursor:pointer;border:1px solid rgba(56,189,248,0.4);background:linear-gradient(135deg,rgba(16,185,129,0.22),rgba(56,189,248,0.22));color:#ecfeff;transition:all 0.2s ease;}',
      '.mathedu-ad-btn:hover{transform:translateY(-1px);border-color:#6ee7b7;box-shadow:0 4px 14px rgba(16,185,129,0.28);}',
      '.mathedu-ad-modal-backdrop{position:fixed;inset:0;z-index:10060;background:rgba(2,6,23,0.82);backdrop-filter:blur(10px);display:flex;align-items:center;justify-content:center;padding:16px;}',
      '.mathedu-ad-modal-card{width:100%;max-width:640px;max-height:90vh;overflow-y:auto;border-radius:22px;background:linear-gradient(160deg,#090d1e,#131c38);border:1px solid rgba(251,191,36,0.35);box-shadow:0 24px 60px rgba(0,0,0,0.65);color:#f8fafc;padding:22px;font-family:"Pretendard","Inter",sans-serif;}'
    ].join('\n');
    document.head.appendChild(st);
  }

  function recordImpression() {
    state.impressions = (state.impressions || 0) + 1;
    saveState(state);
  }

  function renderNativeAdBanner(containerId) {
    ensureAdStyles();
    var container = document.getElementById(containerId);
    if (!container) return;

    recordImpression();
    var sponsor =
      varEDUCATIONAL_SPONSORS[state.impressions % varEDUCATIONAL_SPONSORS.length];

    if (isRealAdsenseConfigured()) {
      container.innerHTML =
        '<div class="mathedu-clean-ad-wrap">' +
        '  <div style="width:100%;display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">' +
        '    <span class="mathedu-ad-badge">AD · 100% 무료 수학교육 운영 후원 광고 (Google AdSense)</span>' +
        '    <div style="display:flex;gap:6px;">' +
        '      <button type="button" class="mathedu-ad-btn" onclick="window.MatheduAdEngine.openRewardedAdModal()">🎁 보상형 광고 (+50 XP·필살기 완충)</button>' +
        '      <button type="button" class="mathedu-ad-btn" style="background:rgba(148,163,184,0.14);border-color:rgba(148,163,184,0.3);" onclick="window.MatheduAdEngine.openFinanceModal()">💼 수익화 관제</button>' +
        '    </div>' +
        '  </div>' +
        '  <ins class="adsbygoogle" style="display:block;width:100%;min-height:90px;" data-ad-client="' +
        state.adsenseClient +
        '" data-ad-slot="' +
        state.adsenseSlotMain +
        '" data-ad-format="auto" data-full-width-responsive="true"></ins>' +
        '</div>';
      try {
        (window.adsbygoogle = window.adsbygoogle || []).push({});
      } catch (e) {}
      return;
    }

    if (isRealAdfitConfigured()) {
      container.innerHTML =
        '<div class="mathedu-clean-ad-wrap">' +
        '  <div style="width:100%;display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">' +
        '    <span class="mathedu-ad-badge">AD · 100% 무료 수학교육 운영 후원 광고 (Kakao AdFit)</span>' +
        '    <button type="button" class="mathedu-ad-btn" onclick="window.MatheduAdEngine.openRewardedAdModal()">🎁 보상형 광고 (+50 XP·필살기 완충)</button>' +
        '  </div>' +
        '  <ins class="kakao_ad_area" style="display:none;width:100%;" data-ad-unit="' +
        state.adfitUnitId +
        '" data-ad-width="728" data-ad-height="90"></ins>' +
        '</div>';
      return;
    }

    container.innerHTML =
      '<div class="mathedu-clean-ad-wrap">' +
      '  <div style="flex:1;min-width:240px;">' +
      '    <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:4px;">' +
      '      <span class="mathedu-ad-badge">SPONSORED · 100% 무료 학습 후원 슬롯</span>' +
      '      <span style="font-size:11px;color:#94a3b8;font-weight:600;">' +
      sponsor.badge +
      '</span>' +
      '    </div>' +
      '    <div style="font-size:13.5px;font-weight:800;color:#f8fafc;margin-bottom:2px;">' +
      sponsor.title +
      '</div>' +
      '    <div style="font-size:11.5px;color:#cbd5e1;line-height:1.45;">' +
      sponsor.desc +
      '</div>' +
      '  </div>' +
      '  <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">' +
      '    <button type="button" class="mathedu-ad-btn" style="background:linear-gradient(135deg,#f59e0b,#d97706);border-color:#fde68a;color:#090d16;" onclick="window.MatheduAdEngine.openRewardedAdModal()">🎁 무료 스폰서 광고 보너스 (+50 XP · 필살기 100%)</button>' +
      '    <button type="button" class="mathedu-ad-btn" onclick="window.MatheduAdEngine.openFinanceModal()">💼 광고 수익화 & 애드센스 설정</button>' +
      '  </div>' +
      '</div>';
  }

  var rewardTimerId = null;

  function openRewardedAdModal() {
    ensureAdStyles();
    var existing = document.getElementById('matheduRewardedAdModal');
    if (existing) existing.remove();
    if (rewardTimerId) {
      clearInterval(rewardTimerId);
      rewardTimerId = null;
    }

    var sponsor =
      varEDUCATIONAL_SPONSORS[
        Math.floor(Math.random() * varEDUCATIONAL_SPONSORS.length)
      ];
    var remaining = 5;

    var modal = document.createElement('div');
    modal.id = 'matheduRewardedAdModal';
    modal.className = 'mathedu-ad-modal-backdrop';
    modal.innerHTML =
      '<div class="mathedu-ad-modal-card">' +
      '  <div style="display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:14px;">' +
      '    <div style="display:flex;align-items:center;gap:8px;">' +
      '      <span class="mathedu-ad-badge">🎁 REWARDED SPONSOR AD · 아르키메데스의 후원 상자</span>' +
      '    </div>' +
      '    <span id="rewardAdCountdownBadge" style="padding:4px 10px;border-radius:999px;background:rgba(56,189,248,0.18);border:1px solid rgba(56,189,248,0.4);color:#7dd3fc;font-size:12px;font-weight:800;">⏳ 5초 후 보상 활성화...</span>' +
      '  </div>' +
      '  <div style="padding:18px;border-radius:16px;background:linear-gradient(135deg,rgba(30,41,59,0.9),rgba(15,23,42,0.95));border:1px solid rgba(56,189,248,0.3);margin-bottom:14px;text-align:center;">' +
      '    <div style="font-size:11px;font-weight:800;color:#fde68a;margin-bottom:6px;">' +
      sponsor.badge +
      '</div>' +
      '    <div style="font-size:18px;font-weight:900;color:#ffffff;margin-bottom:8px;line-height:1.35;">' +
      sponsor.title +
      '</div>' +
      '    <div style="font-size:13px;color:#cbd5e1;line-height:1.6;margin-bottom:14px;">' +
      sponsor.desc +
      '</div>' +
      '    <div style="padding:10px 14px;border-radius:12px;background:rgba(16,185,129,0.12);border:1px solid rgba(16,185,129,0.3);color:#a7f3d0;font-size:12px;font-weight:700;">' +
      '      💡 이 스폰서 슬롯은 학생·교사에게 100% 무료로 제공되는 mathedu의 서버 및 콘텐츠 운영을 후원합니다.' +
      '    </div>' +
      '  </div>' +
      '  <div style="display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;">' +
      '    <div style="font-size:12px;color:#fde68a;font-weight:800;">🎯 시청 완료 보상: <span style="color:#34d399;">+50 XP</span> · <span style="color:#38bdf8;">기하 필살기 100% 완충</span> · <span style="color:#c4b5fd;">사색 통찰 +40%</span></div>' +
      '    <div style="display:flex;gap:8px;">' +
      '      <button type="button" id="btnClaimRewardedAd" disabled style="padding:10px 18px;border-radius:12px;border:1px solid rgba(148,163,184,0.3);background:rgba(51,65,85,0.6);color:#94a3b8;font-size:13px;font-weight:900;cursor:not-allowed;">⏳ 5초 대기 중...</button>' +
      '      <button type="button" onclick="document.getElementById(\'matheduRewardedAdModal\').remove()" style="padding:10px 14px;border-radius:12px;border:1px solid rgba(148,163,184,0.3);background:transparent;color:#cbd5e1;font-size:12px;font-weight:700;cursor:pointer;">닫기</button>' +
      '    </div>' +
      '  </div>' +
      '</div>';

    document.body.appendChild(modal);

    rewardTimerId = setInterval(function () {
      remaining -= 1;
      var badge = document.getElementById('rewardAdCountdownBadge');
      var btn = document.getElementById('btnClaimRewardedAd');
      if (!badge || !btn) {
        clearInterval(rewardTimerId);
        rewardTimerId = null;
        return;
      }
      if (remaining > 0) {
        badge.textContent = '⏳ ' + remaining + '초 후 보상 활성화...';
        btn.textContent = '⏳ ' + remaining + '초 대기 중...';
      } else {
        clearInterval(rewardTimerId);
        rewardTimerId = null;
        badge.textContent = '✅ 스폰서 광고 시청 완료!';
        badge.style.background = 'rgba(16,185,129,0.22)';
        badge.style.borderColor = '#34d399';
        badge.style.color = '#6ee7b7';
        btn.disabled = false;
        btn.style.cursor = 'pointer';
        btn.style.background = 'linear-gradient(135deg,#10b981,#059669)';
        btn.style.borderColor = '#6ee7b7';
        btn.style.color = '#ffffff';
        btn.textContent = '🎉 보상 수령 (+50 XP & 필살기 100% 완충!)';
        btn.onclick = function () {
          claimRewardedAdBonus();
          var m = document.getElementById('matheduRewardedAdModal');
          if (m) m.remove();
        };
      }
    }, 1000);
  }

  function claimRewardedAdBonus() {
    state.rewardedWatches = (state.rewardedWatches || 0) + 1;
    state.lastRewardTime = Date.now();
    saveState(state);

    if (window.MatheduGame && typeof window.MatheduGame.addXP === 'function') {
      try {
        window.MatheduGame.addXP(50, 'rewarded_sponsor_ad');
      } catch (e) {}
    }

    if (
      window.MatheduQuestGame &&
      typeof window.MatheduQuestGame.grantSponsorAdReward === 'function'
    ) {
      try {
        window.MatheduQuestGame.grantSponsorAdReward();
      } catch (e) {}
    }
  }

  function openFinanceModal() {
    ensureAdStyles();
    var existing = document.getElementById('matheduFinanceAdminModal');
    if (existing) existing.remove();

    var estMonthlyViews = Math.max(30000, (state.impressions || 1) * 1500);
    var estBannerRevKrw = Math.round((estMonthlyViews / 1000) * 3200);
    var estRewardRevKrw = Math.round((estMonthlyViews * 0.12 / 1000) * 18000);
    var estTotalKrw = estBannerRevKrw + estRewardRevKrw;

    var modal = document.createElement('div');
    modal.id = 'matheduFinanceAdminModal';
    modal.className = 'mathedu-ad-modal-backdrop';
    modal.innerHTML =
      '<div class="mathedu-ad-modal-card">' +
      '  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">' +
      '    <div>' +
      '      <span class="mathedu-ad-badge">💼 FINANCE AGENT · 무료 수학교육 클린 광고 수익화 관제 센터</span>' +
      '      <h3 style="margin:6px 0 0;font-size:19px;font-weight:900;color:#ffffff;">Google AdSense · Kakao AdFit · 보상형 광고 매니저</h3>' +
      '    </div>' +
      '    <button type="button" onclick="document.getElementById(\'matheduFinanceAdminModal\').remove()" style="padding:6px 12px;border-radius:10px;border:1px solid rgba(148,163,184,0.3);background:rgba(30,41,59,0.8);color:#e2e8f0;font-weight:800;cursor:pointer;">✕ 닫기</button>' +
      '  </div>' +
      '  <p style="font-size:12.5px;color:#cbd5e1;line-height:1.55;margin:0 0 14px;">' +
      '    학생과 교사에게는 <strong>16,548문항 디딤돌 퀴즈와 3D 원정대 게임을 100% 영구 무료</strong>로 제공하면서, 학습을 방해하지 않는 <strong>하단 네이티브 배너</strong>와 자발적 <strong>🎁 보상형 스폰서 상자</strong>로 광고 수익을 창출합니다.' +
      '  </p>' +
      '  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin-bottom:16px;">' +
      '    <div style="padding:12px;border-radius:14px;background:rgba(15,23,42,0.85);border:1px solid rgba(56,189,248,0.28);">' +
      '      <div style="font-size:11px;color:#94a3b8;font-weight:700;">누적 슬롯 노출 (Local PV)</div>' +
      '      <div style="font-size:20px;font-weight:900;color:#38bdf8;margin-top:4px;">' +
      (state.impressions || 0).toLocaleString() +
      '회</div>' +
      '    </div>' +
      '    <div style="padding:12px;border-radius:14px;background:rgba(15,23,42,0.85);border:1px solid rgba(16,185,129,0.28);">' +
      '      <div style="font-size:11px;color:#94a3b8;font-weight:700;">보상형 상자 시청 완료</div>' +
      '      <div style="font-size:20px;font-weight:900;color:#34d399;margin-top:4px;">' +
      (state.rewardedWatches || 0).toLocaleString() +
      '회</div>' +
      '    </div>' +
      '    <div style="padding:12px;border-radius:14px;background:rgba(15,23,42,0.85);border:1px solid rgba(251,191,36,0.32);">' +
      '      <div style="font-size:11px;color:#94a3b8;font-weight:700;">예상 월간 광고 수익 (3만 PV 기준)</div>' +
      '      <div style="font-size:18px;font-weight:900;color:#fbbf24;margin-top:4px;">약 ' +
      estTotalKrw.toLocaleString() +
      '원/월</div>' +
      '    </div>' +
      '  </div>' +
      '  <div style="padding:14px;border-radius:14px;background:rgba(30,41,59,0.65);border:1px solid rgba(148,163,184,0.24);margin-bottom:14px;">' +
      '    <div style="font-size:13px;font-weight:800;color:#fde68a;margin-bottom:10px;">⚙️ Google AdSense / Kakao AdFit 퍼블리셔 ID 설정</div>' +
      '    <div style="display:flex;flex-direction:column;gap:8px;">' +
      '      <label style="font-size:11.5px;color:#cbd5e1;font-weight:700;">Google AdSense Publisher ID (예: ca-pub-1234567890123456)' +
      '        <input id="inpAdsenseClient" type="text" value="' +
      (state.adsenseClient || '') +
      '" style="width:100%;margin-top:4px;padding:8px 10px;border-radius:9px;border:1px solid rgba(148,163,184,0.35);background:#090d16;color:#f8fafc;font-size:12.5px;"/>' +
      '      </label>' +
      '      <label style="font-size:11.5px;color:#cbd5e1;font-weight:700;">Google AdSense 배너 Slot ID (예: 1234567890)' +
      '        <input id="inpAdsenseSlot" type="text" value="' +
      (state.adsenseSlotMain || '') +
      '" style="width:100%;margin-top:4px;padding:8px 10px;border-radius:9px;border:1px solid rgba(148,163,184,0.35);background:#090d16;color:#f8fafc;font-size:12.5px;"/>' +
      '      </label>' +
      '      <label style="font-size:11.5px;color:#cbd5e1;font-weight:700;">Kakao AdFit Unit ID (선택, 예: DAN-xxxxxxxxxxxxxxxx)' +
      '        <input id="inpAdfitUnit" type="text" value="' +
      (state.adfitUnitId || '') +
      '" style="width:100%;margin-top:4px;padding:8px 10px;border-radius:9px;border:1px solid rgba(148,163,184,0.35);background:#090d16;color:#f8fafc;font-size:12.5px;"/>' +
      '      </label>' +
      '    </div>' +
      '    <div style="margin-top:10px;font-size:11px;color:#94a3b8;line-height:1.5;">' +
      '      • 루트 경로에 <a href="ads.txt" target="_blank" style="color:#38bdf8;text-decoration:underline;">ads.txt</a> 파일이 준비되어 있습니다.<br/>' +
      '      • 영구 배포 반영 명령어: <code style="color:#fde68a;">python finance.py set-adsense --client ca-pub-XXXX --slot YYYY</code>' +
      '    </div>' +
      '  </div>' +
      '  <div style="display:flex;justify-content:flex-end;gap:8px;">' +
      '    <button type="button" class="mathedu-ad-btn" onclick="window.MatheduAdEngine.saveConfigFromModal()">💾 광고 ID 설정 저장 및 즉시 적용</button>' +
      '  </div>' +
      '</div>';

    document.body.appendChild(modal);
  }

  function saveConfigFromModal() {
    var cEl = document.getElementById('inpAdsenseClient');
    var sEl = document.getElementById('inpAdsenseSlot');
    var aEl = document.getElementById('inpAdfitUnit');
    if (cEl && cEl.value.trim()) state.adsenseClient = cEl.value.trim();
    if (sEl && sEl.value.trim()) state.adsenseSlotMain = sEl.value.trim();
    if (aEl && aEl.value.trim()) state.adfitUnitId = aEl.value.trim();
    saveState(state);
    mountAllAdSlots();
    var m = document.getElementById('matheduFinanceAdminModal');
    if (m) m.remove();
  }

  function mountAllAdSlots() {
    var questRoot = document.getElementById('matheduQuestConsoleRoot');
    if (questRoot && !document.getElementById('matheduAdSlotQuest')) {
      var qSlot = document.createElement('div');
      qSlot.id = 'matheduAdSlotQuest';
      questRoot.parentNode.insertBefore(qSlot, questRoot.nextSibling);
    }
    var explorerSec = document.getElementById('quizExplorerSection');
    if (explorerSec && !document.getElementById('matheduAdSlotMain')) {
      var mSlot = document.createElement('div');
      mSlot.id = 'matheduAdSlotMain';
      mSlot.className = 'px-margin';
      explorerSec.parentNode.insertBefore(mSlot, explorerSec.nextSibling);
    }
    renderNativeAdBanner('matheduAdSlotQuest');
    renderNativeAdBanner('matheduAdSlotMain');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      setTimeout(mountAllAdSlots, 350);
    });
  } else {
    setTimeout(mountAllAdSlots, 350);
  }

  window.MatheduAdEngine = {
    openRewardedAdModal: openRewardedAdModal,
    openFinanceModal: openFinanceModal,
    saveConfigFromModal: saveConfigFromModal,
    renderNativeAdBanner: renderNativeAdBanner,
    mountAllAdSlots: mountAllAdSlots
  };
})();
