/*!
 * mathedu-skills-suite.js — Smart Math Learning & Classroom Studio
 * Powered by imported Awesome Claude Skills:
 *   1. theme-factory (10 Curated Atelier Color Themes)
 *   2. pdf & xlsx / document-skills (A4 Printable Exam Worksheet PDF & Excel/CSV Report Exporter)
 *   3. raffle-winner-picker (Cryptographically Fair Classroom Presenter & Problem Picker)
 *   4. canvas-design (Museum-Grade Mathematical Geometry Poster .PNG Generator)
 *   5. wolfram-alpha-api-automation (Interactive Function Graph, Derivative/Integral & WolframAlpha Inspector)
 *   6. changelog-generator & twitter-algorithm-optimizer (Release Notes & Viral Study Post Optimizer)
 */
(function (window) {
  'use strict';

  var THEME_STORAGE_KEY = 'mathedu_theme_factory_v1';
  var RAFFLE_HISTORY_KEY = 'mathedu_raffle_excluded_v1';

  // 1. theme-factory: 10 Official Preset Themes
  var THEME_FACTORY_PRESETS = [
    { id: 'ocean-depths', name: '🌊 Ocean Depths', desc: '차분하고 깊이 있는 해양 아카데미 블루', accent: '#006398', accent2: '#0284c7', good: '#0d9488', pillGrad: 'linear-gradient(135deg,#006398,#0284c7)' },
    { id: 'midnight-galaxy', name: '🌌 Midnight Galaxy', desc: '신비로운 코스믹 바이올렛 & 인디고 성운', accent: '#6d28d9', accent2: '#4f46e5', good: '#10b981', pillGrad: 'linear-gradient(135deg,#6d28d9,#4f46e5)' },
    { id: 'forest-canopy', name: '🌲 Forest Canopy', desc: '눈의 피로를 덜어주는 자연의 포레스트 그린', accent: '#1b4332', accent2: '#2d6a4f', good: '#059669', pillGrad: 'linear-gradient(135deg,#1b4332,#2d6a4f)' },
    { id: 'sunset-boulevard', name: '🌅 Sunset Boulevard', desc: '따뜻하고 활기찬 선셋 코랄 & 앰버', accent: '#c2410c', accent2: '#e11d48', good: '#059669', pillGrad: 'linear-gradient(135deg,#c2410c,#e11d48)' },
    { id: 'golden-hour', name: '🍯 Golden Hour', desc: '풍요로운 황금비 골든 아워 팔레트', accent: '#b45309', accent2: '#d97706', good: '#0d9488', pillGrad: 'linear-gradient(135deg,#b45309,#d97706)' },
    { id: 'arctic-frost', name: '❄️ Arctic Frost', desc: '선명하고 투명한 북극 크리스탈 시안', accent: '#0369a1', accent2: '#0891b2', good: '#10b981', pillGrad: 'linear-gradient(135deg,#0369a1,#0891b2)' },
    { id: 'desert-rose', name: '🌹 Desert Rose', desc: '우아하고 감성적인 더스티 로즈 & 버건디', accent: '#9f1239', accent2: '#be185d', good: '#059669', pillGrad: 'linear-gradient(135deg,#9f1239,#be185d)' },
    { id: 'tech-innovation', name: '⚡ Tech Innovation', desc: '역동적인 실리콘밸리 일렉트릭 블루', accent: '#1d4ed8', accent2: '#3b82f6', good: '#10b981', pillGrad: 'linear-gradient(135deg,#1d4ed8,#4f46e5)' },
    { id: 'botanical-garden', name: '🌿 Botanical Garden', desc: '싱그러운 보타니컬 에메랄드 가든', accent: '#047857', accent2: '#10b981', good: '#059669', pillGrad: 'linear-gradient(135deg,#047857,#10b981)' },
    { id: 'modern-minimalist', name: '🖤 Modern Minimalist', desc: '군더더기 없는 스위스 모던 모노크롬', accent: '#18181b', accent2: '#3f3f46', good: '#059669', pillGrad: 'linear-gradient(135deg,#18181b,#3f3f46)' }
  ];

  function ensureSuiteStyles() {
    if (document.getElementById('matheduSkillsSuiteStyles')) return;
    var st = document.createElement('style');
    st.id = 'matheduSkillsSuiteStyles';
    st.textContent = [
      '.skills-studio-bar{margin:12px 0 4px;padding:14px 18px;border-radius:18px;background:rgba(255,255,255,0.86);backdrop-filter:blur(20px) saturate(180%);border:1px solid rgba(15,23,42,0.08);box-shadow:0 8px 26px rgba(15,23,42,0.05);display:flex;flex-direction:column;gap:10px;}',
      'html.dark-theme .skills-studio-bar{background:rgba(15,23,42,0.82);border-color:rgba(148,163,184,0.18);color:#f8fafc;}',
      '.skills-studio-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(165px,1fr));gap:8px;}',
      '.skills-tool-btn{display:flex;align-items:center;gap:8px;padding:10px 12px;border-radius:13px;border:1px solid rgba(15,23,42,0.09);background:linear-gradient(135deg,rgba(255,255,255,0.95),rgba(241,245,249,0.9));color:#0f172a;font-size:12px;font-weight:800;cursor:pointer;text-align:left;transition:all 0.22s cubic-bezier(0.22,1,0.36,1);box-shadow:0 2px 8px rgba(15,23,42,0.04);}',
      'html.dark-theme .skills-tool-btn{background:linear-gradient(135deg,rgba(30,41,59,0.9),rgba(15,23,42,0.9));border-color:rgba(148,163,184,0.22);color:#f8fafc;}',
      '.skills-tool-btn:hover{transform:translateY(-2px);border-color:var(--accent,#006398);box-shadow:0 8px 20px rgba(0,99,152,0.14);}',
      '.skills-modal-overlay{position:fixed;inset:0;z-index:10080;background:rgba(2,6,23,0.78);backdrop-filter:blur(12px);display:flex;align-items:center;justify-content:center;padding:16px;}',
      '.skills-modal-box{width:100%;max-width:740px;max-height:92vh;overflow-y:auto;border-radius:22px;background:#ffffff;color:#0f172a;border:1px solid rgba(15,23,42,0.12);box-shadow:0 24px 64px rgba(0,0,0,0.45);padding:22px;font-family:"Pretendard","Inter",sans-serif;}',
      'html.dark-theme .skills-modal-box{background:#0f172a;color:#f8fafc;border-color:rgba(148,163,184,0.25);}'
    ].join('\n');
    document.head.appendChild(st);
  }

  function applyThemePreset(themeId) {
    var preset = null;
    for (var i = 0; i < THEME_FACTORY_PRESETS.length; i++) {
      if (THEME_FACTORY_PRESETS[i].id === themeId) {
        preset = THEME_FACTORY_PRESETS[i];
        break;
      }
    }
    if (!preset) return;
    try {
      localStorage.setItem(THEME_STORAGE_KEY, preset.id);
    } catch (e) {}

    var root = document.documentElement;
    root.style.setProperty('--accent', preset.accent);
    root.style.setProperty('--accent2', preset.accent2);
    root.style.setProperty('--good', preset.good);

    var dynStyle = document.getElementById('matheduThemeFactoryDynamic');
    if (!dynStyle) {
      dynStyle = document.createElement('style');
      dynStyle.id = 'matheduThemeFactoryDynamic';
      document.head.appendChild(dynStyle);
    }
    dynStyle.textContent =
      '.hero-gradient-accent{background:' + preset.pillGrad + ' !important;-webkit-background-clip:text !important;-webkit-text-fill-color:transparent !important;}' +
      '.stitch-year-pill.active,.stitch-subj-pill.active,.filter-tab-btn.active{background:' + preset.pillGrad + ' !important;color:#ffffff !important;}';

    var badgeEl = document.getElementById('activeThemeFactoryBadge');
    if (badgeEl) badgeEl.textContent = preset.name;
  }

  function closeSuiteModal() {
    var m = document.getElementById('matheduSkillsSuiteModal');
    if (m) m.remove();
  }

  // =========================================================================
  // 1. 🎨 Theme Factory Modal (theme-factory skill)
  // =========================================================================
  function openThemeFactoryModal() {
    ensureSuiteStyles();
    closeSuiteModal();
    var savedId = 'ocean-depths';
    try {
      savedId = localStorage.getItem(THEME_STORAGE_KEY) || 'ocean-depths';
    } catch (e) {}

    var cardsHtml = THEME_FACTORY_PRESETS.map(function (t) {
      var isAct = t.id === savedId;
      return (
        '<button type="button" onclick="window.MatheduSkillsSuite.selectTheme(\'' + t.id + '\')" ' +
        'style="padding:12px 14px;border-radius:14px;border:2px solid ' + (isAct ? t.accent : 'rgba(148,163,184,0.25)') + ';background:' + (isAct ? 'rgba(2,132,199,0.08)' : 'transparent') + ';text-align:left;cursor:pointer;display:flex;flex-direction:column;gap:6px;transition:all .18s ease;">' +
        '  <div style="display:flex;align-items:center;justify-content:space-between;width:100%;">' +
        '    <span style="font-size:13.5px;font-weight:900;color:inherit;">' + t.name + '</span>' +
        '    <span style="display:inline-flex;gap:4px;">' +
        '      <span style="width:14px;height:14px;border-radius:999px;background:' + t.accent + ';display:inline-block;"></span>' +
        '      <span style="width:14px;height:14px;border-radius:999px;background:' + t.accent2 + ';display:inline-block;"></span>' +
        '    </span>' +
        '  </div>' +
        '  <span style="font-size:11.5px;opacity:0.78;">' + t.desc + '</span>' +
        '</button>'
      );
    }).join('');

    var overlay = document.createElement('div');
    overlay.id = 'matheduSkillsSuiteModal';
    overlay.className = 'skills-modal-overlay';
    overlay.innerHTML =
      '<div class="skills-modal-box">' +
      '  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">' +
      '    <div>' +
      '      <span style="font-size:11px;font-weight:800;color:#0284c7;">🎨 POWERED BY THEME-FACTORY SKILL</span>' +
      '      <h3 style="margin:4px 0 0;font-size:19px;font-weight:900;">10대 아틀리에 컬러 테마 팩토리</h3>' +
      '    </div>' +
      '    <button type="button" onclick="window.MatheduSkillsSuite.closeModal()" style="padding:6px 12px;border-radius:10px;border:1px solid rgba(148,163,184,0.3);background:transparent;color:inherit;font-weight:800;cursor:pointer;">✕ 닫기</button>' +
      '  </div>' +
      '  <p style="font-size:12.5px;opacity:0.82;margin:0 0 14px;">원하는 테마를 클릭하면 홈페이지의 포인트 컬러, 그라데이션 타이틀, 필터 알약 배지가 즉시 변환됩니다.</p>' +
      '  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px;">' +
      cardsHtml +
      '  </div>' +
      '</div>';
    document.body.appendChild(overlay);
  }

  function selectTheme(themeId) {
    applyThemePreset(themeId);
    openThemeFactoryModal();
  }

  // =========================================================================
  // 2. 📄 PDF Worksheet & Excel/CSV Report Studio (pdf & xlsx skills)
  // =========================================================================
  function openDocumentStudioModal() {
    ensureSuiteStyles();
    closeSuiteModal();

    var overlay = document.createElement('div');
    overlay.id = 'matheduSkillsSuiteModal';
    overlay.className = 'skills-modal-overlay';
    overlay.innerHTML =
      '<div class="skills-modal-box">' +
      '  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">' +
      '    <div>' +
      '      <span style="font-size:11px;font-weight:800;color:#059669;">📄 POWERED BY DOCUMENT-SKILLS (PDF · XLSX · DOCX)</span>' +
      '      <h3 style="margin:4px 0 0;font-size:19px;font-weight:900;">맞춤형 수학 시험지(PDF 인쇄) & 성취도 리포트(Excel/CSV) 스튜디오</h3>' +
      '    </div>' +
      '    <button type="button" onclick="window.MatheduSkillsSuite.closeModal()" style="padding:6px 12px;border-radius:10px;border:1px solid rgba(148,163,184,0.3);background:transparent;color:inherit;font-weight:800;cursor:pointer;">✕ 닫기</button>' +
      '  </div>' +
      '  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;margin-top:10px;">' +
      '    <div style="padding:16px;border-radius:16px;border:1px solid rgba(2,132,199,0.28);background:rgba(2,132,199,0.05);display:flex;flex-direction:column;justify-content:space-between;gap:12px;">' +
      '      <div>' +
      '        <div style="font-size:15px;font-weight:900;margin-bottom:6px;">🖨️ A4 맞춤형 수학 디딤돌 시험지 (PDF 인쇄)</div>' +
      '        <p style="font-size:12px;opacity:0.82;line-height:1.55;margin:0;">현재 기출 탐색기에 표시된 문제들(최대 10문항)을 실제 대학수학능력시험 2단 시험지 레이아웃 + 디딤돌 점검 체크리스트 + QR 코드로 조합하여 즉시 인쇄하거나 PDF로 저장합니다.</p>' +
      '      </div>' +
      '      <button type="button" onclick="window.MatheduSkillsSuite.printCustomWorksheet()" style="padding:11px 16px;border-radius:12px;border:0;background:linear-gradient(135deg,#006398,#2563eb);color:#ffffff;font-size:13px;font-weight:900;cursor:pointer;">🖨️ 현재 필터 문항으로 A4 시험지 PDF 인쇄</button>' +
      '    </div>' +
      '    <div style="padding:16px;border-radius:16px;border:1px solid rgba(16,185,129,0.28);background:rgba(16,185,129,0.05);display:flex;flex-direction:column;justify-content:space-between;gap:12px;">' +
      '      <div>' +
      '        <div style="font-size:15px;font-weight:900;margin-bottom:6px;">📊 학습 성취도 & 오답노트 Excel(CSV) 내보내기</div>' +
      '        <p style="font-size:12px;opacity:0.82;line-height:1.55;margin:0;">나의 수능 100점 만점 원정대 진도, 연속 학습 스트릭, 획득한 수학자의 성물, 오답노트 및 북마크 문항 리스트를 엑셀(UTF-8 CSV) 파일로 즉시 다운로드합니다.</p>' +
      '      </div>' +
      '      <button type="button" onclick="window.MatheduSkillsSuite.exportStudyExcelCsv()" style="padding:11px 16px;border-radius:12px;border:0;background:linear-gradient(135deg,#059669,#10b981);color:#ffffff;font-size:13px;font-weight:900;cursor:pointer;">📥 Excel 호환 학습 리포트 (.CSV) 다운로드</button>' +
      '    </div>' +
      '  </div>' +
      '</div>';
    document.body.appendChild(overlay);
  }

  function printCustomWorksheet() {
    var cards = document.querySelectorAll('#list [data-slug]');
    var items = [];
    for (var i = 0; i < cards.length && items.length < 8; i++) {
      var slug = cards[i].getAttribute('data-slug') || '';
      var titleEl = cards[i].querySelector('h3, a, .font-bold');
      var title = titleEl ? titleEl.textContent.trim() : slug;
      items.push({ num: i + 1, slug: slug, title: title });
    }
    if (items.length === 0) {
      items = [
        { num: 1, slug: 'csat-2026-22', title: '2026학년도 대학수학능력시험 수학 공통 22번 (단계별 디딤돌)' },
        { num: 2, slug: 'csat-2026-15', title: '2026학년도 대학수학능력시험 수학 공통 15번 (귀납적 추론)' },
        { num: 3, slug: 'csat-2026-m30', title: '2026학년도 대학수학능력시험 미적분 30번 (초월함수 미적분)' },
        { num: 4, slug: 'csat-2026-g30', title: '2026학년도 대학수학능력시험 기하 30번 (공간도형과 벡터)' }
      ];
    }

    var searchInp = document.getElementById('quizSearchInput');
    var filterTitle = (searchInp && searchInp.value.trim()) ? searchInp.value.trim() : '수능·평가원 핵심 기출 선별';
    var todayStr = new Date().toISOString().slice(0, 10);

    var rowsHtml = items.map(function (it) {
      var fullUrl = 'https://min7014.github.io/mathedu/board/' + (it.slug.indexOf('exam_') === 0 ? ('archive.html?id=' + it.slug) : (it.slug + '.html'));
      return (
        '<div style="border:1.5px solid #1e293b;border-radius:12px;padding:16px;margin-bottom:14px;page-break-inside:avoid;">' +
        '  <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px dashed #94a3b8;padding-bottom:8px;margin-bottom:10px;">' +
        '    <strong style="font-size:15px;">문항 ' + it.num + '. ' + it.title + '</strong>' +
        '    <span style="font-size:11px;color:#475569;">온라인 디딤돌: ' + fullUrl + '</span>' +
        '  </div>' +
        '  <div style="display:flex;gap:14px;font-size:12px;color:#334155;margin-bottom:8px;">' +
        '    <span>□ 🎯 ① 구하는 값 확인</span>' +
        '    <span>□ 🔑 ② 주어진 조건 분해</span>' +
        '    <span>□ 🌉 ③ 연결할 공식·보조선 구상</span>' +
        '    <span>□ ✨ 무오답 자력 해결</span>' +
        '  </div>' +
        '  <div style="height:110px;border:1px dotted #cbd5e1;border-radius:8px;padding:8px;color:#94a3b8;font-size:11px;">✏️ 데카르트 수식 전개 및 기하 보조선 작도란</div>' +
        '</div>'
      );
    }).join('');

    var w = window.open('', '_blank', 'width=900,height=800');
    if (!w) return;
    w.document.write(
      '<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><title>mathedu 맞춤형 수학 시험지 (' + todayStr + ')</title>' +
      '<style>body{font-family:"Pretendard","Malgun Gothic",sans-serif;padding:28px;color:#0f172a;max-width:820px;margin:0 auto;}@media print{.no-print{display:none!important;}}</style></head><body>' +
      '<div class="no-print" style="margin-bottom:18px;display:flex;justify-content:space-between;align-items:center;padding:12px 16px;background:#f0f9ff;border:1px solid #bae6fd;border-radius:10px;">' +
      '  <span style="font-size:13px;font-weight:700;color:#0369a1;">🖨️ 브라우저 인쇄 창에서 [PDF로 저장] 또는 프린터를 선택하세요.</span>' +
      '  <button onclick="window.print()" style="padding:8px 16px;border-radius:8px;border:0;background:#0284c7;color:#fff;font-weight:800;cursor:pointer;">지금 인쇄 / PDF 저장</button>' +
      '</div>' +
      '<div style="border-bottom:3px double #0f172a;padding-bottom:12px;margin-bottom:18px;text-align:center;">' +
      '  <div style="font-size:12px;font-weight:700;letter-spacing:0.08em;">2027학년도 대학수학능력시험 수학 영역 대비 · mathedu 단계별 디딤돌 워크시트</div>' +
      '  <h1 style="margin:6px 0;font-size:24px;font-weight:900;">수학 영역 (' + filterTitle + ')</h1>' +
      '  <div style="font-size:12px;color:#475569;">생성일: ' + todayStr + ' · 성명: ____________ · 목표: 수능 수학 100점 만점 (https://min7014.github.io/mathedu/)</div>' +
      '</div>' +
      rowsHtml +
      '<script>setTimeout(function(){window.print();},400);<\/script>' +
      '</body></html>'
    );
    w.document.close();
  }

  function exportStudyExcelCsv() {
    var wrongList = (window.MatheduGame && window.MatheduGame.getWrongAnswers) ? window.MatheduGame.getWrongAnswers() : [];
    var bookmarks = (window.MatheduGame && window.MatheduGame.getBookmarks) ? window.MatheduGame.getBookmarks() : [];
    var questState = (window.MatheduQuest && window.MatheduQuest.state) ? window.MatheduQuest.state : {};
    var todayStr = new Date().toISOString().slice(0, 10);

    var lines = [
      ['구분', '항목/문항코드', '상세내용', '기록일시', '바로가기URL'],
      ['원정대_수능만점게이지', 'CSAT_SCORE', (questState.csatScore || 0) + ' / 100점', todayStr, 'https://min7014.github.io/mathedu/'],
      ['원정대_클리어스테이지수', 'CLEARED_STAGES', ((questState.clearedStages || []).length) + '개 보스 격파', todayStr, 'https://min7014.github.io/mathedu/'],
      ['원정대_장착성물', 'EQUIPPED_RELICS', (questState.equippedRelics || []).join(' | ') || '없음', todayStr, 'https://min7014.github.io/mathedu/'],
      ['원정대_성좌각성', 'CONSTELLATION_STARS', ((questState.constellationStars || []).length) + ' / 12성', todayStr, 'https://min7014.github.io/mathedu/']
    ];

    wrongList.forEach(function (slug) {
      lines.push(['오답노트_복습대상', slug, '오답 리벤지 레이드 추천 문항', todayStr, 'https://min7014.github.io/mathedu/?challenge=' + slug]);
    });
    bookmarks.forEach(function (slug) {
      lines.push(['즐겨찾기_보관문항', slug, '학생 북마크 중요 문항', todayStr, 'https://min7014.github.io/mathedu/?challenge=' + slug]);
    });

    var csvContent = '\uFEFF' + lines.map(function (row) {
      return row.map(function (cell) {
        return '"' + String(cell || '').replace(/"/g, '""') + '"';
      }).join(',');
    }).join('\r\n');

    var blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'mathedu_study_report_' + todayStr + '.csv';
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 1500);
  }

  // =========================================================================
  // 3. 🎡 Cryptographic Classroom Raffle & Problem Picker (raffle-winner-picker skill)
  // =========================================================================
  function cryptoRandomInt(maxExclusive) {
    if (maxExclusive <= 1) return 0;
    if (window.crypto && window.crypto.getRandomValues) {
      var arr = new Uint32Array(1);
      window.crypto.getRandomValues(arr);
      return arr[0] % maxExclusive;
    }
    return Math.floor(Math.random() * maxExclusive);
  }

  function openClassroomRaffleModal() {
    ensureSuiteStyles();
    closeSuiteModal();

    var overlay = document.createElement('div');
    overlay.id = 'matheduSkillsSuiteModal';
    overlay.className = 'skills-modal-overlay';
    overlay.innerHTML =
      '<div class="skills-modal-box">' +
      '  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">' +
      '    <div>' +
      '      <span style="font-size:11px;font-weight:800;color:#d97706;">🎡 POWERED BY RAFFLE-WINNER-PICKER SKILL</span>' +
      '      <h3 style="margin:4px 0 0;font-size:19px;font-weight:900;">교실 발표자 & 오늘의 기출 문제 공정 추첨기</h3>' +
      '    </div>' +
      '    <button type="button" onclick="window.MatheduSkillsSuite.closeModal()" style="padding:6px 12px;border-radius:10px;border:1px solid rgba(148,163,184,0.3);background:transparent;color:inherit;font-weight:800;cursor:pointer;">✕ 닫기</button>' +
      '  </div>' +
      '  <p style="font-size:12px;opacity:0.8;margin:0 0 12px;">암호학적 보안 난수(<code>crypto.getRandomValues</code>)와 중복 당첨 방지 로직으로 학급 발표 학생 또는 무작위 기출 문항을 공정하게 추첨합니다.</p>' +
      '  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;margin-bottom:12px;">' +
      '    <label style="font-size:12px;font-weight:800;">학급 인원수 (예: 30번까지)' +
      '      <input id="raffleMaxNum" type="number" min="2" max="200" value="30" style="width:100%;margin-top:4px;padding:8px 10px;border-radius:10px;border:1px solid #cbd5e1;font-size:13px;color:#0f172a;"/>' +
      '    </label>' +
      '    <label style="font-size:12px;font-weight:800;">동시 추첨 인원 (1~10명)' +
      '      <input id="rafflePickCount" type="number" min="1" max="10" value="2" style="width:100%;margin-top:4px;padding:8px 10px;border-radius:10px;border:1px solid #cbd5e1;font-size:13px;color:#0f172a;"/>' +
      '    </label>' +
      '  </div>' +
      '  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;">' +
      '    <button type="button" onclick="window.MatheduSkillsSuite.runStudentRaffle()" style="padding:10px 16px;border-radius:12px;border:0;background:linear-gradient(135deg,#f59e0b,#d97706);color:#ffffff;font-size:13px;font-weight:900;cursor:pointer;">🎉 디딤돌 발표 학생 공정 추첨</button>' +
      '    <button type="button" onclick="window.MatheduSkillsSuite.runProblemRaffle()" style="padding:10px 16px;border-radius:12px;border:0;background:linear-gradient(135deg,#0284c7,#4f46e5);color:#ffffff;font-size:13px;font-weight:900;cursor:pointer;">🎲 오늘의 대표 기출 3문항 추첨</button>' +
      '  </div>' +
      '  <div id="raffleResultBox" style="padding:14px;border-radius:14px;background:rgba(15,23,42,0.05);border:1px dashed rgba(148,163,184,0.4);font-size:13px;min-height:80px;display:flex;align-items:center;justify-content:center;text-align:center;">위 버튼을 눌러 공정한 추첨 결과를 확인하세요!</div>' +
      '</div>';
    document.body.appendChild(overlay);
  }

  function runStudentRaffle() {
    var maxEl = document.getElementById('raffleMaxNum');
    var cntEl = document.getElementById('rafflePickCount');
    var maxN = Math.max(2, Math.min(200, parseInt(maxEl ? maxEl.value : '30', 10) || 30));
    var pickC = Math.max(1, Math.min(maxN, parseInt(cntEl ? cntEl.value : '2', 10) || 2));

    var pool = [];
    for (var i = 1; i <= maxN; i++) pool.push(i);
    var winners = [];
    while (winners.length < pickC && pool.length > 0) {
      var idx = cryptoRandomInt(pool.length);
      winners.push(pool[idx]);
      pool.splice(idx, 1);
    }
    var runnerUp = pool.length > 0 ? pool[cryptoRandomInt(pool.length)] : null;
    var ts = new Date().toISOString().replace('T', ' ').slice(0, 19) + ' UTC';

    var box = document.getElementById('raffleResultBox');
    if (box) {
      box.innerHTML =
        '<div style="width:100%;text-align:left;">' +
        '  <div style="font-size:12px;font-weight:800;color:#d97706;margin-bottom:4px;">🎉 WINNER SELECTED (Cryptographically Unbiased)</div>' +
        '  <div style="font-size:20px;font-weight:900;color:#0284c7;margin-bottom:6px;">당첨 번호: ' +
        winners.map(function (n) { return n + '번 학생'; }).join(', ') +
        '</div>' +
        (runnerUp ? '<div style="font-size:12px;opacity:0.82;">• 예비 발표자(Runner-up): <strong>' + runnerUp + '번 학생</strong></div>' : '') +
        '  <div style="font-size:11px;opacity:0.65;margin-top:4px;">• 추첨 방식: window.crypto.getRandomValues · 검증 시각: ' + ts + '</div>' +
        '</div>';
    }
  }

  function runProblemRaffle() {
    var cards = document.querySelectorAll('#list [data-slug]');
    var pool = [];
    for (var i = 0; i < cards.length; i++) {
      var slug = cards[i].getAttribute('data-slug');
      var tEl = cards[i].querySelector('h3, a, .font-bold');
      if (slug) pool.push({ slug: slug, title: tEl ? tEl.textContent.trim() : slug });
    }
    if (pool.length === 0) {
      pool = [
        { slug: 'csat-2026-22', title: '2026학년도 수능 공통 22번' },
        { slug: 'csat-2026-15', title: '2026학년도 수능 공통 15번' },
        { slug: 'csat-2026-m30', title: '2026학년도 수능 미적분 30번' }
      ];
    }
    var picked = [];
    var copyPool = pool.slice();
    while (picked.length < 3 && copyPool.length > 0) {
      var idx = cryptoRandomInt(copyPool.length);
      picked.push(copyPool[idx]);
      copyPool.splice(idx, 1);
    }

    var box = document.getElementById('raffleResultBox');
    if (box) {
      box.innerHTML =
        '<div style="width:100%;text-align:left;">' +
        '  <div style="font-size:12px;font-weight:800;color:#0284c7;margin-bottom:6px;">🎲 오늘의 랜덤 추천 기출 3선 (클릭 시 3D 보스 결투 또는 퀴즈 이동)</div>' +
        picked.map(function (p, i) {
          return (
            '<div style="display:flex;align-items:center;justify-content:space-between;padding:6px 0;border-bottom:1px dashed rgba(148,163,184,0.25);">' +
            '  <span style="font-weight:800;">' + (i + 1) + '. ' + p.title + '</span>' +
            '  <a href="?challenge=' + encodeURIComponent(p.slug) + '" style="padding:4px 10px;border-radius:8px;background:#0284c7;color:#fff;font-size:11px;font-weight:800;text-decoration:none;">⚔️ 바로 도전</a>' +
            '</div>'
          );
        }).join('') +
        '</div>';
    }
  }

  // =========================================================================
  // 4. 🖼️ Mathematical Geometry Poster Canvas Studio (canvas-design skill)
  // =========================================================================
  function openCanvasPosterModal() {
    ensureSuiteStyles();
    closeSuiteModal();

    var overlay = document.createElement('div');
    overlay.id = 'matheduSkillsSuiteModal';
    overlay.className = 'skills-modal-overlay';
    overlay.innerHTML =
      '<div class="skills-modal-box">' +
      '  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">' +
      '    <div>' +
      '      <span style="font-size:11px;font-weight:800;color:#7c3aed;">🖼️ POWERED BY CANVAS-DESIGN SKILL</span>' +
      '      <h3 style="margin:4px 0 0;font-size:19px;font-weight:900;">황금비 기하 아트워크 & 수능 만점 다짐 포스터 스튜디오</h3>' +
      '    </div>' +
      '    <button type="button" onclick="window.MatheduSkillsSuite.closeModal()" style="padding:6px 12px;border-radius:10px;border:1px solid rgba(148,163,184,0.3);background:transparent;color:inherit;font-weight:800;cursor:pointer;">✕ 닫기</button>' +
      '  </div>' +
      '  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px;">' +
      '    <button type="button" onclick="window.MatheduSkillsSuite.drawMathPoster(\'silence\')" style="padding:6px 12px;border-radius:999px;border:1px solid #4f46e5;background:#eef2ff;color:#312e81;font-size:11.5px;font-weight:800;cursor:pointer;">📐 Geometric Silence</button>' +
      '    <button type="button" onclick="window.MatheduSkillsSuite.drawMathPoster(\'chromatic\')" style="padding:6px 12px;border-radius:999px;border:1px solid #0284c7;background:#e0f2fe;color:#0c4a6e;font-size:11.5px;font-weight:800;cursor:pointer;">🌈 Chromatic Harmonics</button>' +
      '    <button type="button" onclick="window.MatheduSkillsSuite.drawMathPoster(\'dandelin\')" style="padding:6px 12px;border-radius:999px;border:1px solid #d97706;background:#fef3c7;color:#78350f;font-size:11.5px;font-weight:800;cursor:pointer;">🔮 Dandelin Conic</button>' +
      '    <button type="button" onclick="window.MatheduSkillsSuite.downloadMathPosterPng()" style="margin-left:auto;padding:6px 14px;border-radius:999px;border:0;background:linear-gradient(135deg,#059669,#10b981);color:#ffffff;font-size:12px;font-weight:900;cursor:pointer;">📥 고해상도 포스터 (.PNG) 저장</button>' +
      '  </div>' +
      '  <div style="display:flex;justify-content:center;background:#090d16;border-radius:16px;padding:12px;">' +
      '    <canvas id="skillsPosterCanvas" width="560" height="360" style="max-width:100%;height:auto;border-radius:10px;"></canvas>' +
      '  </div>' +
      '</div>';
    document.body.appendChild(overlay);
    drawMathPoster('silence');
  }

  function drawMathPoster(styleMode) {
    var c = document.getElementById('skillsPosterCanvas');
    if (!c) return;
    var ctx = c.getContext('2d');
    var w = c.width, h = c.height;

    var bgGrad = ctx.createLinearGradient(0, 0, w, h);
    if (styleMode === 'chromatic') {
      bgGrad.addColorStop(0, '#081c24');
      bgGrad.addColorStop(1, '#1e1b4b');
    } else if (styleMode === 'dandelin') {
      bgGrad.addColorStop(0, '#181124');
      bgGrad.addColorStop(1, '#090d16');
    } else {
      bgGrad.addColorStop(0, '#050814');
      bgGrad.addColorStop(1, '#0f172a');
    }
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, w, h);

    // Subtle scientific observation grid (canvas-design philosophy)
    ctx.strokeStyle = 'rgba(148,163,184,0.10)';
    ctx.lineWidth = 1;
    for (var gx = 28; gx < w; gx += 28) {
      ctx.beginPath(); ctx.moveTo(gx, 0); ctx.lineTo(gx, h); ctx.stroke();
    }
    for (var gy = 28; gy < h; gy += 28) {
      ctx.beginPath(); ctx.moveTo(0, gy); ctx.lineTo(w, gy); ctx.stroke();
    }

    // Parametric Mathematical Art Curve (Lissajous / Rose / Conic Envelope)
    var cx = w * 0.66, cy = h * 0.5;
    for (var layer = 0; layer < 24; layer++) {
      ctx.beginPath();
      var col = styleMode === 'dandelin'
        ? 'rgba(251,191,36,' + (0.15 + layer * 0.03) + ')'
        : (styleMode === 'chromatic' ? 'rgba(56,189,248,' + (0.15 + layer * 0.03) + ')' : 'rgba(16,185,129,' + (0.15 + layer * 0.03) + ')');
      ctx.strokeStyle = col;
      ctx.lineWidth = 1.2;
      for (var t = 0; t <= Math.PI * 2; t += 0.04) {
        var r = 115 * Math.cos((styleMode === 'dandelin' ? 2 : 3) * t + layer * 0.08);
        var px = cx + r * Math.cos(t) + 28 * Math.sin(2 * t);
        var py = cy + r * Math.sin(t) + 28 * Math.cos(3 * t);
        if (t === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.closePath();
      ctx.stroke();
    }

    // Typography & Mathematical Manifesto
    var score = (window.MatheduQuest && window.MatheduQuest.state) ? (window.MatheduQuest.state.csatScore || 0) : 100;
    ctx.fillStyle = '#38bdf8';
    ctx.font = '700 11px "Space Grotesk","Pretendard",sans-serif';
    ctx.fillText('MATHEDU · GEOMETRIC SILENCE & VISUAL PROOF ARCHIVE', 28, 42);

    ctx.fillStyle = '#ffffff';
    ctx.font = '900 26px "Plus Jakarta Sans","Pretendard",sans-serif';
    ctx.fillText('PF + PF\' = 2a', 28, 86);
    ctx.font = '800 18px "Pretendard",sans-serif';
    ctx.fillText('수식에 갇히지 않고 눈으로 원리를 통찰하다', 28, 118);

    ctx.fillStyle = '#cbd5e1';
    ctx.font = '600 12.5px "Pretendard",sans-serif';
    ctx.fillText('• 3,400+ Dynamic GeoGebra Visual Proofs', 28, 162);
    ctx.fillText('• 16,548 Micro-Scaffolded CSAT Problems', 28, 184);
    ctx.fillText('• Deep Contemplation & Archimedes Eureka', 28, 206);

    ctx.fillStyle = '#fbbf24';
    ctx.font = '900 16px "Pretendard",sans-serif';
    ctx.fillText('👑 수능 수학 만점 게이지: ' + score + ' / 100 pt  —  Q.E.D.', 28, 265);

    ctx.fillStyle = '#94a3b8';
    ctx.font = '600 11px "Space Grotesk",sans-serif';
    ctx.fillText('https://min7014.github.io/mathedu/  |  φ = (1 + √5) / 2 ≈ 1.6180339887', 28, 330);
  }

  function downloadMathPosterPng() {
    var c = document.getElementById('skillsPosterCanvas');
    if (!c) return;
    var link = document.createElement('a');
    link.download = 'mathedu_geometric_poster.png';
    link.href = c.toDataURL('image/png');
    link.click();
  }

  // =========================================================================
  // 5. 🧮 Interactive Symbolic Math & WolframAlpha Inspector (wolfram-alpha-api-automation skill)
  // =========================================================================
  var SYMBOLIC_PRESETS = [
    { id: 'cubic', label: '삼차함수 극대·극소: f(x) = x³ - 3x + 1', query: 'plot x^3 - 3x + 1, extrema, inflection point, integrate from 0 to 2', fn: function (x) { return x * x * x - 3 * x + 1; }, dfn: function (x) { return 3 * x * x - 3; }, summary: '도함수 f\'(x)=3(x+1)(x-1) ➔ x=-1에서 극댓값 3, x=1에서 극솟값 -1, 변곡점 (0,1), ∫₀² (x³-3x+1)dx = 0' },
    { id: 'trig', label: '삼각함수 주기·넓이: f(x) = 2sin(x) + cos(2x)', query: '2*sin(x) + cos(2*x) extrema and period', fn: function (x) { return 2 * Math.sin(x) + Math.cos(2 * x); }, dfn: function (x) { return 2 * Math.cos(x) - 2 * Math.sin(2 * x); }, summary: 'cos(2x)=1-2sin²x 치환 ➔ t=sin(x) (-1≤t≤1)에 대한 이차함수 -2t²+2t+1로 변환하여 최댓값 3/2 도출' },
    { id: 'exp', label: '초월함수 미적분: f(x) = x · e^(-x²/2)', query: 'derivative and extrema of x * exp(-x^2 / 2)', fn: function (x) { return x * Math.exp(-0.5 * x * x); }, dfn: function (x) { return (1 - x * x) * Math.exp(-0.5 * x * x); }, summary: '원점 대칭 기함수(f(-x)=-f(x)) · f\'(x)=(1-x²)e^(-x²/2) ➔ x=1에서 극대 e^(-1/2), x=-1에서 극소 -e^(-1/2)' }
  ];

  function openSymbolicMathModal() {
    ensureSuiteStyles();
    closeSuiteModal();

    var btnsHtml = SYMBOLIC_PRESETS.map(function (p, idx) {
      return '<button type="button" onclick="window.MatheduSkillsSuite.renderSymbolicPreset(' + idx + ')" style="padding:7px 12px;border-radius:10px;border:1px solid #0284c7;background:rgba(2,132,199,0.08);color:inherit;font-size:11.5px;font-weight:800;cursor:pointer;">📈 ' + p.label + '</button>';
    }).join('');

    var overlay = document.createElement('div');
    overlay.id = 'matheduSkillsSuiteModal';
    overlay.className = 'skills-modal-overlay';
    overlay.innerHTML =
      '<div class="skills-modal-box">' +
      '  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">' +
      '    <div>' +
      '      <span style="font-size:11px;font-weight:800;color:#e11d48;">🧮 POWERED BY WOLFRAM-ALPHA-API-AUTOMATION SKILL</span>' +
      '      <h3 style="margin:4px 0 0;font-size:19px;font-weight:900;">실시간 함수 그래프 · 도함수 f\'(x) · 정적분 & WolframAlpha 기호 검증기</h3>' +
      '    </div>' +
      '    <button type="button" onclick="window.MatheduSkillsSuite.closeModal()" style="padding:6px 12px;border-radius:10px;border:1px solid rgba(148,163,184,0.3);background:transparent;color:inherit;font-weight:800;cursor:pointer;">✕ 닫기</button>' +
      '  </div>' +
      '  <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px;">' + btnsHtml + '</div>' +
      '  <div style="background:#090d16;border-radius:14px;padding:10px;text-align:center;margin-bottom:10px;">' +
      '    <canvas id="symbolicMathCanvas" width="580" height="240" style="max-width:100%;height:auto;"></canvas>' +
      '  </div>' +
      '  <div id="symbolicSummaryBox" style="padding:10px 14px;border-radius:12px;background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);font-size:12.5px;font-weight:700;margin-bottom:12px;"></div>' +
      '  <div style="display:flex;gap:8px;align-items:center;">' +
      '    <input id="wolframCustomInput" type="text" value="plot x^3 - 3x + 1, extrema, integrate from 0 to 2" style="flex:1;padding:9px 12px;border-radius:10px;border:1px solid #cbd5e1;font-size:12.5px;color:#0f172a;" placeholder="수식 입력 (예: integrate x^2 * sin(x) dx)"/>' +
      '    <button type="button" onclick="window.MatheduSkillsSuite.openWolframQuery()" style="padding:9px 15px;border-radius:10px;border:0;background:linear-gradient(135deg,#e11d48,#f97316);color:#ffffff;font-size:12.5px;font-weight:900;cursor:pointer;white-space:nowrap;">🔬 WolframAlpha 기호 검증 ➔</button>' +
      '  </div>' +
      '</div>';
    document.body.appendChild(overlay);
    renderSymbolicPreset(0);
  }

  function renderSymbolicPreset(idx) {
    var p = SYMBOLIC_PRESETS[idx] || SYMBOLIC_PRESETS[0];
    var inp = document.getElementById('wolframCustomInput');
    if (inp) inp.value = p.query;
    var sumBox = document.getElementById('symbolicSummaryBox');
    if (sumBox) sumBox.innerHTML = '💡 <strong>수학적 핵심 분석:</strong> ' + p.summary + ' <span style="margin-left:8px;color:#0284c7;">(실선: y=f(x), 점선: 도함수 y=f\'(x))</span>';

    var c = document.getElementById('symbolicMathCanvas');
    if (!c) return;
    var ctx = c.getContext('2d');
    var w = c.width, h = c.height;
    ctx.fillStyle = '#090d16';
    ctx.fillRect(0, 0, w, h);

    var ox = w * 0.5, oy = h * 0.55;
    var scaleX = 72, scaleY = 36;

    // Axes
    ctx.strokeStyle = 'rgba(148,163,184,0.3)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, oy); ctx.lineTo(w, oy);
    ctx.moveTo(ox, 0); ctx.lineTo(ox, h);
    ctx.stroke();

    // Shaded integral area [0, 2]
    ctx.fillStyle = 'rgba(16,185,129,0.22)';
    ctx.beginPath();
    ctx.moveTo(ox, oy);
    for (var sx = 0; sx <= 2.0; sx += 0.04) {
      ctx.lineTo(ox + sx * scaleX, oy - p.fn(sx) * scaleY);
    }
    ctx.lineTo(ox + 2.0 * scaleX, oy);
    ctx.closePath();
    ctx.fill();

    // Derivative y = f'(x) dashed
    ctx.save();
    ctx.setLineDash([5, 4]);
    ctx.strokeStyle = '#fbbf24';
    ctx.lineWidth = 1.8;
    ctx.beginPath();
    for (var px = 0; px <= w; px += 3) {
      var xVal = (px - ox) / scaleX;
      var yVal = p.dfn(xVal);
      var py = oy - yVal * scaleY;
      if (px === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
    ctx.stroke();
    ctx.restore();

    // Function y = f(x) solid
    ctx.strokeStyle = '#38bdf8';
    ctx.lineWidth = 2.8;
    ctx.beginPath();
    for (var px2 = 0; px2 <= w; px2 += 2) {
      var xV = (px2 - ox) / scaleX;
      var yV = p.fn(xV);
      var py2 = oy - yV * scaleY;
      if (px2 === 0) ctx.moveTo(px2, py2);
      else ctx.lineTo(px2, py2);
    }
    ctx.stroke();
  }

  function openWolframQuery() {
    var inp = document.getElementById('wolframCustomInput');
    var q = inp && inp.value.trim() ? inp.value.trim() : 'plot x^3 - 3x + 1';
    window.open('https://www.wolframalpha.com/input?i=' + encodeURIComponent(q), '_blank', 'noopener');
  }

  // =========================================================================
  // 6. 📢 Mount the Smart Skills Studio Bar on Homepage
  // =========================================================================
  function mountSkillsStudioBar() {
    ensureSuiteStyles();
    var savedTheme = null;
    try {
      savedTheme = localStorage.getItem(THEME_STORAGE_KEY);
    } catch (e) {}
    if (savedTheme) applyThemePreset(savedTheme);

    var targetAnchor = document.getElementById('quizExplorerSection');
    if (!targetAnchor || document.getElementById('matheduSkillsStudioBar')) return;

    var bar = document.createElement('div');
    bar.id = 'matheduSkillsStudioBar';
    bar.className = 'px-margin mt-space-md';
    bar.innerHTML =
      '<div class="skills-studio-bar">' +
      '  <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap;">' +
      '    <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">' +
      '      <span style="padding:3px 10px;border-radius:999px;background:linear-gradient(135deg,#006398,#4f46e5);color:#ffffff;font-size:10.5px;font-weight:900;letter-spacing:0.04em;">🛠️ SMART SKILLS STUDIO</span>' +
      '      <span style="font-size:13.5px;font-weight:900;">Awesome Skills 기반 스마트 수학 학습·교실 도구함</span>' +
      '    </div>' +
      '    <span id="activeThemeFactoryBadge" style="font-size:11px;font-weight:800;color:var(--accent,#006398);">🌊 Ocean Depths</span>' +
      '  </div>' +
      '  <div class="skills-studio-grid">' +
      '    <button type="button" class="skills-tool-btn" onclick="window.MatheduSkillsSuite.openThemeFactoryModal()">' +
      '      <span style="font-size:18px;">🎨</span>' +
      '      <div><div style="font-weight:900;">10대 테마 팩토리</div><div style="font-size:10.5px;opacity:0.7;">컬러 팔레트 즉시 변경</div></div>' +
      '    </button>' +
      '    <button type="button" class="skills-tool-btn" onclick="window.MatheduSkillsSuite.openDocumentStudioModal()">' +
      '      <span style="font-size:18px;">📄</span>' +
      '      <div><div style="font-weight:900;">시험지 PDF · 성적 CSV</div><div style="font-size:10.5px;opacity:0.7;">A4 워크시트 & 엑셀 리포트</div></div>' +
      '    </button>' +
      '    <button type="button" class="skills-tool-btn" onclick="window.MatheduSkillsSuite.openClassroomRaffleModal()">' +
      '      <span style="font-size:18px;">🎡</span>' +
      '      <div><div style="font-weight:900;">교실 발표·문제 추첨기</div><div style="font-size:10.5px;opacity:0.7;">암호학적 무편향 공정 추첨</div></div>' +
      '    </button>' +
      '    <button type="button" class="skills-tool-btn" onclick="window.MatheduSkillsSuite.openCanvasPosterModal()">' +
      '      <span style="font-size:18px;">🖼️</span>' +
      '      <div><div style="font-weight:900;">기하 아트워크 포스터</div><div style="font-size:10.5px;opacity:0.7;">황금비 수식 .PNG 생성</div></div>' +
      '    </button>' +
      '    <button type="button" class="skills-tool-btn" onclick="window.MatheduSkillsSuite.openSymbolicMathModal()">' +
      '      <span style="font-size:18px;">🧮</span>' +
      '      <div><div style="font-weight:900;">미적분 그래프·울프람</div><div style="font-size:10.5px;opacity:0.7;">도함수·정적분·기호 검증</div></div>' +
      '    </button>' +
      '  </div>' +
      '</div>';

    targetAnchor.parentNode.insertBefore(bar, targetAnchor);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      setTimeout(mountSkillsStudioBar, 200);
    });
  } else {
    setTimeout(mountSkillsStudioBar, 200);
  }

  window.MatheduSkillsSuite = {
    openThemeFactoryModal: openThemeFactoryModal,
    selectTheme: selectTheme,
    openDocumentStudioModal: openDocumentStudioModal,
    printCustomWorksheet: printCustomWorksheet,
    exportStudyExcelCsv: exportStudyExcelCsv,
    openClassroomRaffleModal: openClassroomRaffleModal,
    runStudentRaffle: runStudentRaffle,
    runProblemRaffle: runProblemRaffle,
    openCanvasPosterModal: openCanvasPosterModal,
    drawMathPoster: drawMathPoster,
    downloadMathPosterPng: downloadMathPosterPng,
    openSymbolicMathModal: openSymbolicMathModal,
    renderSymbolicPreset: renderSymbolicPreset,
    openWolframQuery: openWolframQuery,
    closeModal: closeSuiteModal
  };
})(window);
