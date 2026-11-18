/*!
 * mathedu-ads.js — clean web-ad loader (Policy 68 §3-① · Rule 61)
 * -------------------------------------------------------------------------
 * Reads ../ad_config.json (resolved relative to this script, so it works from
 * root pages and board/ pages alike) and renders Google AdSense / Kakao AdFit
 * units ONLY into footer / result slots.
 *
 * Guarantees
 *  - Disabled (default) or missing IDs  -> creates ZERO DOM elements and makes
 *    ZERO third-party requests (only one tiny same-origin ad_config.json fetch,
 *    scheduled after window.load + idle, so it never touches mobile LCP).
 *  - Ads only inside [data-mathedu-ad-slot="footer"|"result"] containers (or one
 *    auto-appended in-flow footer slot when enabled). Never inside canvas, form,
 *    iframe contexts, quiz-solving UI ([data-no-ads]) or fixed/sticky overlays.
 *  - No AdSense Auto ads / anchor / vignette / video formats are requested.
 *  - Never creates <video> or YouTube embeds (Rule 61).
 *  - Lazy: each unit is requested only when its slot scrolls near the viewport.
 *  - KO/EN aware (?lang=en, <html lang>, mathedu_lang): per-language provider
 *    routing from config.langRouting, label "광고" / "Advertisement".
 *
 * Page integration (one line, before </body>):
 *   <script src="assets/mathedu-ads.js?v=20261118" defer></script>
 * Optional explicit slots:
 *   <div data-mathedu-ad-slot="footer"></div>
 *   <div data-mathedu-ad-slot="result"></div>   (inside a result/score screen)
 * Debug: ?ads=off (force off) · ?ads=preview (grey placeholder boxes, no network)
 * Activation: python -X utf8 finance.py set-adsense --client ca-pub-XXXXXXXXXXXXXXXX --slot NNNNNNNNNN
 *             python -X utf8 finance.py set-adfit --unit DAN-XXXXXXXXXXXXXXXX
 */
(function () {
  'use strict';
  if (window.MatheduAds) return;

  var VERSION = '20261118';
  var SLOT_ATTR = 'data-mathedu-ad-slot';
  var ADSENSE_RE = /^ca-pub-\d{16}$/;
  var ADSENSE_SLOT_RE = /^\d{6,16}$/;
  var ADFIT_RE = /^DAN-[A-Za-z0-9]{6,40}$/;

  var script = document.currentScript;
  var configUrl;
  try {
    configUrl = (script && script.getAttribute('data-config')) ||
      new URL('../ad_config.json', (script && script.src) || location.href).href;
  } catch (e) { configUrl = 'ad_config.json'; }

  var api = {
    version: VERSION,
    config: null,
    active: false,
    mode: 'pending',
    rendered: [],
    scan: function () {},
    lang: currentLang
  };
  window.MatheduAds = api;

  function qs(name) {
    try { return new URLSearchParams(location.search).get(name); } catch (e) { return null; }
  }

  function currentLang() {
    var p = (qs('lang') || '').toLowerCase();
    if (p === 'en' || p === 'ko') return p;
    var h = (document.documentElement.getAttribute('lang') || '').toLowerCase();
    if (h.indexOf('en') === 0) return 'en';
    if (h.indexOf('ko') === 0) return 'ko';
    try {
      var s = localStorage.getItem('mathedu_lang') || localStorage.getItem('mathedu_vb_lang');
      if (s === 'en' || s === 'ko') return s;
    } catch (e) { /* storage blocked */ }
    return 'ko';
  }

  function inIframe() {
    try { return window.self !== window.top; } catch (e) { return true; }
  }

  function pathExcluded(cfg) {
    var list = (cfg.placement && cfg.placement.excludePaths) || [];
    var path = location.pathname.toLowerCase();
    for (var i = 0; i < list.length; i++) {
      if (list[i] && path.indexOf(String(list[i]).toLowerCase()) !== -1) return true;
    }
    return false;
  }

  function adsenseReady(c) {
    return !!(c && c.enabled === true && ADSENSE_RE.test(c.clientId || '') &&
      (ADSENSE_SLOT_RE.test(c.slotMain || '') || ADSENSE_SLOT_RE.test(c.slotResult || '')));
  }

  function adfitReady(c) {
    return !!(c && c.enabled === true && (ADFIT_RE.test(c.unitMain || '') || ADFIT_RE.test(c.unitMobile || '')));
  }

  function providersFor(cfg, lang) {
    var routing = (cfg.langRouting && cfg.langRouting[lang]) || ['adsense', 'kakaoAdfit'];
    var out = [];
    for (var i = 0; i < routing.length; i++) {
      var name = routing[i];
      if (name === 'adsense' && adsenseReady(cfg.adsense)) out.push(name);
      if (name === 'kakaoAdfit' && adfitReady(cfg.kakaoAdfit)) out.push(name);
    }
    return out;
  }

  function anyProviderReady(cfg) {
    return adsenseReady(cfg.adsense) || adfitReady(cfg.kakaoAdfit);
  }

  // ---- placement guard: never over solving UI / canvas / overlays ----------
  function slotAllowed(el, cfg) {
    var kind = el.getAttribute(SLOT_ATTR);
    var allowed = (cfg.placement && cfg.placement.allowedSlots) || ['footer', 'result'];
    if (allowed.indexOf(kind) === -1) return false;
    var forbidden = (cfg.placement && cfg.placement.forbiddenAncestors) ||
      'canvas, form, video, iframe, [data-no-ads], [contenteditable="true"]';
    try { if (el.parentElement && el.parentElement.closest(forbidden)) return false; } catch (e) { return false; }
    for (var n = el; n && n.nodeType === 1 && n !== document.body; n = n.parentElement) {
      var pos = getComputedStyle(n).position;
      if (pos === 'fixed' || pos === 'sticky') return false;
    }
    return true;
  }

  // ---- shared DOM helpers (used only when active/preview) -----------------
  var styleInjected = false;
  function injectStyle() {
    if (styleInjected) return;
    styleInjected = true;
    var st = document.createElement('style');
    st.setAttribute('data-mathedu-ads', 'style');
    st.textContent =
      '[' + SLOT_ATTR + '].mathedu-ad-on{display:block;clear:both;margin:28px auto 20px;max-width:980px;' +
      'padding:0 12px;text-align:center;min-height:120px;contain:layout}' +
      '.mathedu-ad-label{display:block;font:500 11px/1.6 system-ui,-apple-system,"Noto Sans KR",sans-serif;' +
      'letter-spacing:.08em;color:#94a3b8;margin-bottom:6px;text-transform:uppercase}' +
      '.mathedu-ad-preview{display:flex;align-items:center;justify-content:center;margin:0 auto;max-width:728px;' +
      'height:90px;border:1px dashed #64748b;border-radius:10px;color:#94a3b8;font:12px system-ui,sans-serif}';
    document.head.appendChild(st);
  }

  function labelText(lang) { return lang === 'en' ? 'Advertisement' : '광고'; }

  function addLabel(slot, lang) {
    var lb = document.createElement('span');
    lb.className = 'mathedu-ad-label notranslate';
    lb.setAttribute('translate', 'no');
    lb.setAttribute('aria-hidden', 'true');
    lb.textContent = labelText(lang);
    slot.appendChild(lb);
  }

  var loadedScripts = {};
  function loadScriptOnce(key, src, attrs) {
    if (loadedScripts[key]) return;
    loadedScripts[key] = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = src;
    if (attrs) for (var k in attrs) s.setAttribute(k, attrs[k]);
    s.setAttribute('data-mathedu-ads', key);
    document.head.appendChild(s);
  }

  function renderAdsense(slot, cfg) {
    var a = cfg.adsense;
    var kind = slot.getAttribute(SLOT_ATTR);
    var slotId = (kind === 'result' && ADSENSE_SLOT_RE.test(a.slotResult || '')) ? a.slotResult : a.slotMain;
    if (!ADSENSE_SLOT_RE.test(slotId || '')) slotId = a.slotResult;
    if (!ADSENSE_SLOT_RE.test(slotId || '')) return false;
    var ins = document.createElement('ins');
    ins.className = 'adsbygoogle';
    ins.style.display = 'block';
    ins.setAttribute('data-ad-client', a.clientId);
    ins.setAttribute('data-ad-slot', slotId);
    ins.setAttribute('data-ad-format', a.format || 'auto');
    ins.setAttribute('data-full-width-responsive', 'true');
    slot.appendChild(ins);
    loadScriptOnce('adsense',
      'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + encodeURIComponent(a.clientId),
      { crossorigin: 'anonymous' });
    try { (window.adsbygoogle = window.adsbygoogle || []).push({}); } catch (e) { /* ignore */ }
    return true;
  }

  function renderAdfit(slot, cfg) {
    var k = cfg.kakaoAdfit;
    var w = slot.clientWidth || document.documentElement.clientWidth || 360;
    var unit = k.unitMain, uw = +k.width || 728, uh = +k.height || 90;
    var mobileOk = ADFIT_RE.test(k.unitMobile || '');
    if (mobileOk && (w < uw || !ADFIT_RE.test(unit || ''))) {
      unit = k.unitMobile; uw = +k.mobileWidth || 320; uh = +k.mobileHeight || 100;
    }
    if (!ADFIT_RE.test(unit || '') || w < uw) return false;
    var ins = document.createElement('ins');
    ins.className = 'kakao_ad_area';
    ins.style.display = 'none';
    ins.setAttribute('data-ad-unit', unit);
    ins.setAttribute('data-ad-width', String(uw));
    ins.setAttribute('data-ad-height', String(uh));
    slot.appendChild(ins);
    // ba.min.js scans unprocessed .kakao_ad_area nodes each time it executes.
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://t1.daumcdn.net/kas/static/ba.min.js';
    s.setAttribute('data-mathedu-ads', 'adfit');
    slot.appendChild(s);
    return true;
  }

  function renderPreview(slot, lang) {
    var box = document.createElement('div');
    box.className = 'mathedu-ad-preview';
    box.textContent = (lang === 'en' ? 'Ad slot preview · ' : '광고 슬롯 미리보기 · ') + slot.getAttribute(SLOT_ATTR);
    slot.appendChild(box);
    return true;
  }

  function renderSlot(slot, cfg, preview) {
    if (slot.getAttribute('data-mathedu-ad-state')) return;
    if (!slotAllowed(slot, cfg)) { slot.setAttribute('data-mathedu-ad-state', 'blocked'); return; }
    var lang = currentLang();
    var providers = preview ? ['preview'] : providersFor(cfg, lang);
    if (!providers.length) return; // e.g. EN page with only AdFit configured: stay empty
    injectStyle();
    slot.classList.add('mathedu-ad-on');
    slot.setAttribute('role', 'complementary');
    slot.setAttribute('aria-label', labelText(lang));
    addLabel(slot, lang);
    var ok = false;
    for (var i = 0; i < providers.length && !ok; i++) {
      if (providers[i] === 'preview') ok = renderPreview(slot, lang);
      else if (providers[i] === 'adsense') ok = renderAdsense(slot, cfg);
      else if (providers[i] === 'kakaoAdfit') ok = renderAdfit(slot, cfg);
      if (ok) slot.setAttribute('data-mathedu-ad-provider', providers[i]);
    }
    if (!ok) {
      slot.classList.remove('mathedu-ad-on');
      while (slot.firstChild) slot.removeChild(slot.firstChild);
      slot.setAttribute('data-mathedu-ad-state', 'nofit');
      return;
    }
    slot.setAttribute('data-mathedu-ad-state', 'rendered');
    api.rendered.push(slot);
  }

  function ensureAutoFooter(cfg) {
    if (!(cfg.placement && cfg.placement.autoFooter)) return;
    if (document.querySelector('[' + SLOT_ATTR + '="footer"]')) return;
    var slot = document.createElement('div');
    slot.setAttribute(SLOT_ATTR, 'footer');
    slot.setAttribute('data-mathedu-ad-auto', '1');
    var footer = document.querySelector('body > footer, footer#siteFooter, footer.site-footer');
    if (footer && footer.parentNode) footer.parentNode.insertBefore(slot, footer);
    else document.body.appendChild(slot);
  }

  function start(cfg, preview) {
    api.active = true;
    api.mode = preview ? 'preview' : 'live';
    ensureAutoFooter(cfg);
    var margin = (cfg.placement && cfg.placement.lazyRootMargin) || '300px 0px';
    var io = ('IntersectionObserver' in window) ? new IntersectionObserver(function (entries) {
      for (var i = 0; i < entries.length; i++) {
        var en = entries[i];
        if (en.isIntersecting && en.target.offsetWidth > 0) {
          io.unobserve(en.target);
          renderSlot(en.target, cfg, preview);
        }
      }
    }, { rootMargin: margin }) : null;

    api.scan = function () {
      var slots = document.querySelectorAll('[' + SLOT_ATTR + ']:not([data-mathedu-ad-watch])');
      for (var i = 0; i < slots.length; i++) {
        slots[i].setAttribute('data-mathedu-ad-watch', '1');
        if (io) io.observe(slots[i]); else renderSlot(slots[i], cfg, preview);
      }
    };
    api.scan();

    // Result screens are often injected later by quiz scripts.
    if ('MutationObserver' in window) {
      var pending = false;
      new MutationObserver(function () {
        if (pending) return;
        pending = true;
        setTimeout(function () { pending = false; api.scan(); }, 400);
      }).observe(document.body, { childList: true, subtree: true });
    }
    // Keep the label in sync with the KO/EN toggle.
    new MutationObserver(function () {
      var lang = currentLang();
      var labels = document.querySelectorAll('.mathedu-ad-label');
      for (var i = 0; i < labels.length; i++) labels[i].textContent = labelText(lang);
    }).observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });
  }

  function boot() {
    var flag = (qs('ads') || '').toLowerCase();
    if (flag === 'off' || inIframe()) { api.mode = 'off'; return; }
    var preview = flag === 'preview';
    var host = (location.hostname || '').toLowerCase();
    var isLocalOrBot = (location.protocol === 'file:' || host === 'localhost' || host === '127.0.0.1' || host === '[::1]' || !!navigator.webdriver);
    if (!preview && isLocalOrBot) { api.mode = 'local-or-bot-skip'; return; }
    fetch(configUrl, { cache: 'no-cache', credentials: 'same-origin' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (cfg) {
        if (!cfg) { api.mode = 'no-config'; return; }
        api.config = cfg;
        if (pathExcluded(cfg)) { api.mode = 'excluded'; return; }
        if (!preview && !anyProviderReady(cfg)) { api.mode = 'disabled'; return; }
        start(cfg, preview);
      })
      .catch(function () { api.mode = 'no-config'; });
  }

  function whenIdle() {
    var delay = 1500;
    var go = function () {
      if ('requestIdleCallback' in window) requestIdleCallback(boot, { timeout: 4000 });
      else setTimeout(boot, 200);
    };
    setTimeout(go, delay);
  }

  if (document.readyState === 'complete') whenIdle();
  else window.addEventListener('load', whenIdle, { once: true });
})();
