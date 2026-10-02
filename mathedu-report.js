/**
 * mathedu-report.js
 * min7014 mathedu · 전 페이지 범용 오류 신고(경광등/사이렌) 및 영역 선택 시스템 (Universal Issue Reporter)
 * 
 * 주요 기능:
 * 1. 화면 스크롤과 무관하게 우측 상단에 영구 고정된 경광등(사이렌) 플로팅 아이콘 (Fixed FAB)
 * 2. 아이콘 클릭 시 인터랙티브 영역 선택 모드(Element Inspector) 가동
 *    - 마우스 오버 시 문제, 보기, 수식, 그림, 지문 등 오류 영역 하이라이트 및 단계 식별
 *    - 클릭 시 해당 요소 정보를 자동 캡처하여 신고 모달에 바인딩
 * 3. 기존 '이 문제에 이상이 있어요'를 일반화하여 전 페이지(index, dashboard, board 등) 통합 처리
 * 4. Google Sheets 백엔드(progress-api-url) 및 안티그래비티 감시 데몬 연동
 * 5. 한국어(KO) 및 영어(EN) 완벽한 다국어 동기화 지원
 */

(function(window, document) {
  'use strict';

  if (window.MatheduReport) {
    return; // 중복 초기화 방지
  }

  var API_FALLBACK = 'https://script.google.com/macros/s/AKfycbxQBW1hKYFSHokaVJMRql-UJpk0t4qMeWMiiy_RFuCLZ5SE4iZytYQkGa9_yoCmm1Ak0Q/exec';

  var state = {
    isInspecting: false,
    hoveredEl: null,
    selectedTarget: null,
    isModalOpen: false
  };

  // 🌐 i18n 텍스트 헬퍼
  function t(path, fallback) {
    if (window.MatheduI18n && typeof window.MatheduI18n.t === 'function') {
      var val = window.MatheduI18n.t(path);
      if (val && val !== path) return val;
    }
    var lang = (document.documentElement.lang || 'ko').toLowerCase();
    var isEn = lang.startsWith('en');

    var defaults = {
      'report.fabTitle': isEn ? 'Report Issue' : '오류신고',
      'report.fabTooltip': isEn ? 'Report Issue (Click an element on screen)' : '오류 신고 (화면 요소를 클릭하여 신고)',
      'report.bannerPrompt': isEn ? '🎯 Click on the problematic part of the screen (question, option, formula, figure, etc.).' : '🎯 오류가 있는 화면 요소(문제, 보기, 수식, 그림 등)를 클릭해 주세요.',
      'report.bannerCancel': isEn ? '✕ Cancel (ESC)' : '✕ 취소 (ESC)',
      'report.bannerWhole': isEn ? '📄 Report Whole Page' : '📄 화면 전체 오류 신고',
      'report.modalTitle': isEn ? '🚨 Report an Issue' : '🚨 오류 신고',
      'report.targetTitle': isEn ? 'Selected Target' : '선택된 영역',
      'report.targetWholePage': isEn ? 'Whole Page (No specific element)' : '화면 전체 (특정 영역 미지정)',
      'report.reselectBtn': isEn ? '🎯 Reselect' : '🎯 다시 선택',
      'report.categoryTitle': isEn ? 'Issue Category' : '오류 유형',
      'report.catMath': isEn ? '🧮 Math / Calculation Error' : '🧮 수식 / 계산 오류',
      'report.catTypo': isEn ? '✍️ Typo / Notation Error' : '✍️ 오타 / 표기 오류',
      'report.catAnswer': isEn ? '🎯 Answer / Grading Issue' : '🎯 정답 / 채점 이상',
      'report.catGraphic': isEn ? '🖼️ Image / Graphic Issue' : '🖼️ 그림 / 그래픽 깨짐',
      'report.catBug': isEn ? '⚙️ Layout / Feature Bug' : '⚙️ 화면 / 기능 이상',
      'report.catOther': isEn ? '💡 Other Suggestion' : '💡 기타 개선 제안',
      'report.descTitle': isEn ? 'Description' : '오류 내용',
      'report.descPlaceholder': isEn ? 'Please describe what is incorrect or needs improvement in detail.' : '어떤 부분이 어떻게 이상한가요? 자세히 적어주시면 신속하게 검토 후 반영하겠습니다.',
      'report.reporterTitle': isEn ? 'Your Name / Nickname' : '신고자 이름 / 닉네임',
      'report.emailTitle': isEn ? 'Notification Email (Optional)' : '알림 받을 이메일 (선택사항)',
      'report.emailPlaceholder': isEn ? 'Email to receive update notification when fixed' : '수정 완료 시 알림을 받으실 이메일 주소',
      'report.cancelBtn': isEn ? 'Cancel' : '취소',
      'report.submitBtn': isEn ? '🚨 Submit Report' : '🚨 신고 접수',
      'report.submitting': isEn ? 'Submitting...' : '신고 접수 중...',
      'report.successToast': isEn ? '✅ Issue report submitted! We will review and fix it promptly.' : '✅ 오류 신고가 정상 접수되었습니다. 확인 후 신속하게 반영하겠습니다!',
      'report.errNoDesc': isEn ? 'Please provide a description of the issue.' : '오류 내용을 입력해 주세요.'
    };
    return defaults[path] || fallback || '';
  }

  // 🎨 스타일 주입
  function injectStyles() {
    if (document.getElementById('mathedu-report-styles')) return;

    var css = `
      /* ═══════════════════════════════════════════════════════════
         🚨 mathedu Universal Siren & Report Widget Styles
         ═══════════════════════════════════════════════════════════ */
      
      /* 1. 고정 플로팅 사이렌 버튼 (Top-Right Fixed FAB) */
      #mathedu-report-fab {
        position: fixed !important;
        top: 18px !important;
        right: 20px !important;
        z-index: 999999 !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 8px !important;
        padding: 8px 16px !important;
        background: rgba(15, 23, 42, 0.88) !important;
        border: 1.5px solid rgba(255, 77, 79, 0.5) !important;
        border-radius: 999px !important;
        color: #ffffff !important;
        font-family: "Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        font-size: 0.86rem !important;
        font-weight: 700 !important;
        line-height: 1 !important;
        text-decoration: none !important;
        cursor: pointer !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.45), 0 0 16px rgba(255, 77, 79, 0.28) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
        user-select: none !important;
      }
      #mathedu-report-fab:hover {
        background: rgba(28, 16, 26, 0.96) !important;
        border-color: rgba(255, 77, 79, 0.9) !important;
        color: #ff9da0 !important;
        transform: translateY(-2px) scale(1.03) !important;
        box-shadow: 0 8px 28px rgba(0, 0, 0, 0.55), 0 0 24px rgba(255, 77, 79, 0.55) !important;
      }
      #mathedu-report-fab:active {
        transform: translateY(0) scale(0.98) !important;
      }
      
      /* 사이렌 광선 애니메이션 */
      .mathedu-siren-ray {
        animation: mathedu-siren-spark 1.8s ease-in-out infinite;
        transform-origin: center;
      }
      .mathedu-siren-ray:nth-child(2) {
        animation-delay: 0.3s;
      }
      .mathedu-siren-ray:nth-child(3) {
        animation-delay: 0.6s;
      }
      @keyframes mathedu-siren-spark {
        0%, 100% { opacity: 0.4; }
        50% { opacity: 1; stroke: #FDE047; filter: drop-shadow(0 0 4px #FBBF24); }
      }

      /* 2. 영역 선택 모드 (Element Inspector) 상단 가이드 바 */
      #mathedu-inspect-banner {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        box-sizing: border-box !important;
        z-index: 10000001 !important;
        display: none;
        align-items: center !important;
        justify-content: space-between !important;
        padding: 12px 24px !important;
        background: rgba(13, 16, 32, 0.94) !important;
        border-bottom: 2px solid #ff4d4f !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6) !important;
        color: #ffffff !important;
        font-family: inherit !important;
        animation: mathedu-slide-down 0.25s ease-out;
      }
      @keyframes mathedu-slide-down {
        from { transform: translateY(-100%); }
        to { transform: translateY(0); }
      }
      .mathedu-banner-left {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 0.92rem;
        font-weight: 700;
        letter-spacing: -0.01em;
      }
      .mathedu-banner-icon {
        font-size: 1.3rem;
        animation: mathedu-bounce 1s infinite alternate ease-in-out;
      }
      @keyframes mathedu-bounce {
        from { transform: scale(1); }
        to { transform: scale(1.2); }
      }
      .mathedu-banner-right {
        display: flex;
        align-items: center;
        gap: 10px;
      }
      .mathedu-banner-btn {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: #ffffff;
        padding: 6px 14px;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.15s ease;
      }
      .mathedu-banner-btn:hover {
        background: rgba(255, 255, 255, 0.2);
        border-color: #ffffff;
      }
      .mathedu-banner-btn-whole {
        background: linear-gradient(135deg, rgba(255, 77, 79, 0.25), rgba(244, 63, 94, 0.35));
        border: 1px solid rgba(255, 77, 79, 0.6);
        color: #ffc9cb;
      }
      .mathedu-banner-btn-whole:hover {
        background: linear-gradient(135deg, #ff4d4f, #f43f5e);
        color: #ffffff;
      }

      /* 3. 인스펙터 하이라이트 박스 */
      #mathedu-inspect-box {
        position: absolute !important;
        pointer-events: none !important;
        z-index: 10000000 !important;
        display: none;
        border: 2.5px dashed #ff4d4f !important;
        border-radius: 8px !important;
        background: rgba(255, 77, 79, 0.12) !important;
        box-shadow: 0 0 24px rgba(255, 77, 79, 0.45), inset 0 0 16px rgba(255, 77, 79, 0.2) !important;
        transition: all 0.06s ease-out !important;
      }
      #mathedu-inspect-label {
        position: absolute !important;
        top: -30px !important;
        left: 0 !important;
        background: #ff4d4f !important;
        color: #ffffff !important;
        font-size: 0.76rem !important;
        font-weight: 800 !important;
        padding: 3px 10px !important;
        border-radius: 6px !important;
        white-space: nowrap !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35) !important;
        letter-spacing: -0.01em !important;
      }

      body.mathedu-inspect-active * {
        cursor: crosshair !important;
      }

      /* 4. 오류 신고 모달 팝업 */
      #mathedu-report-modal {
        position: fixed !important;
        inset: 0 !important;
        z-index: 10000002 !important;
        display: none;
        align-items: center !important;
        justify-content: center !important;
        padding: 20px !important;
        background: rgba(5, 8, 17, 0.8) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        animation: mathedu-fade-in 0.2s ease-out;
      }
      @keyframes mathedu-fade-in {
        from { opacity: 0; }
        to { opacity: 1; }
      }
      .mathedu-modal-card {
        background: linear-gradient(160deg, rgba(20, 27, 48, 0.96) 0%, rgba(10, 14, 28, 0.98) 100%);
        border: 1px solid rgba(255, 77, 79, 0.45);
        border-radius: 20px;
        max-width: 580px;
        width: 100%;
        max-height: 90vh;
        overflow-y: auto;
        padding: 28px;
        box-shadow: 0 24px 60px rgba(0, 0, 0, 0.65), 0 0 32px rgba(255, 77, 79, 0.2);
        color: #f8fafc;
        font-family: inherit;
        box-sizing: border-box;
      }
      .mathedu-modal-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
        padding-bottom: 14px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      }
      .mathedu-modal-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 0;
      }
      .mathedu-modal-close {
        background: transparent;
        border: none;
        color: #94a3b8;
        font-size: 1.5rem;
        line-height: 1;
        cursor: pointer;
        padding: 4px 8px;
        border-radius: 8px;
        transition: all 0.15s ease;
      }
      .mathedu-modal-close:hover {
        color: #ffffff;
        background: rgba(255, 255, 255, 0.1);
      }

      /* 선택 영역 프리뷰 */
      .mathedu-target-preview {
        background: rgba(255, 77, 79, 0.08);
        border: 1px solid rgba(255, 77, 79, 0.3);
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 18px;
        font-size: 0.88rem;
      }
      .mathedu-target-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
      }
      .mathedu-target-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        color: #ff9da0;
        font-weight: 800;
        font-size: 0.82rem;
      }
      .mathedu-target-btn {
        background: transparent;
        border: 1px solid rgba(255, 77, 79, 0.4);
        color: #ffc9cb;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.74rem;
        cursor: pointer;
      }
      .mathedu-target-btn:hover {
        background: rgba(255, 77, 79, 0.2);
        color: #ffffff;
      }
      .mathedu-target-snippet {
        color: #cbd5e1;
        font-size: 0.84rem;
        background: rgba(0, 0, 0, 0.3);
        padding: 8px 10px;
        border-radius: 6px;
        font-family: inherit;
        word-break: break-all;
        max-height: 80px;
        overflow-y: auto;
      }

      /* 카테고리 칩 선택 */
      .mathedu-cat-group {
        margin-bottom: 18px;
      }
      .mathedu-form-label {
        display: block;
        font-size: 0.84rem;
        font-weight: 700;
        color: #94a3b8;
        margin-bottom: 8px;
      }
      .mathedu-cat-chips {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
        gap: 8px;
      }
      .mathedu-cat-chip {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 8px 12px;
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 10px;
        font-size: 0.82rem;
        font-weight: 600;
        color: #cbd5e1;
        cursor: pointer;
        transition: all 0.15s ease;
      }
      .mathedu-cat-chip:hover {
        border-color: rgba(255, 77, 79, 0.5);
        background: rgba(255, 77, 79, 0.12);
        color: #ffffff;
      }
      .mathedu-cat-chip.active {
        background: linear-gradient(135deg, rgba(255, 77, 79, 0.25), rgba(244, 63, 94, 0.25));
        border-color: #ff4d4f;
        color: #ff9da0;
        font-weight: 800;
        box-shadow: 0 0 12px rgba(255, 77, 79, 0.25);
      }

      /* 내용 입력 텍스트에어리어 */
      .mathedu-textarea {
        width: 100%;
        box-sizing: border-box;
        background: rgba(10, 14, 28, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.16);
        border-radius: 10px;
        padding: 12px;
        color: #f8fafc;
        font-size: 0.9rem;
        font-family: inherit;
        line-height: 1.6;
        resize: vertical;
        min-height: 100px;
        outline: none;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 18px;
      }
      .mathedu-textarea:focus {
        border-color: #ff4d4f;
        box-shadow: 0 0 12px rgba(255, 77, 79, 0.3);
      }

      /* 연락처 / 이메일 */
      .mathedu-reporter-row {
        display: grid;
        grid-template-columns: 1fr 1.3fr;
        gap: 12px;
        margin-bottom: 22px;
      }
      @media (max-width: 480px) {
        .mathedu-reporter-row {
          grid-template-columns: 1fr;
        }
      }
      .mathedu-input {
        width: 100%;
        box-sizing: border-box;
        background: rgba(10, 14, 28, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.16);
        border-radius: 10px;
        padding: 8px 12px;
        color: #f8fafc;
        font-size: 0.85rem;
        font-family: inherit;
        outline: none;
      }
      .mathedu-input:focus {
        border-color: #ff4d4f;
      }

      /* 모달 푸터 버튼 */
      .mathedu-modal-footer {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        gap: 10px;
      }
      .mathedu-btn-cancel {
        background: transparent;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: #94a3b8;
        padding: 8px 16px;
        border-radius: 10px;
        font-size: 0.88rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.15s ease;
      }
      .mathedu-btn-cancel:hover {
        color: #ffffff;
        border-color: #ffffff;
      }
      .mathedu-btn-submit {
        background: linear-gradient(135deg, #ff4d4f 0%, #ee5a5a 100%);
        border: none;
        color: #ffffff;
        padding: 9px 20px;
        border-radius: 10px;
        font-size: 0.88rem;
        font-weight: 800;
        cursor: pointer;
        box-shadow: 0 4px 16px rgba(255, 77, 79, 0.4);
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        display: inline-flex;
        align-items: center;
        gap: 6px;
      }
      .mathedu-btn-submit:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 22px rgba(255, 77, 79, 0.6);
      }
      .mathedu-btn-submit:disabled {
        opacity: 0.6;
        cursor: not-allowed;
      }

      /* 5. 토스트 알림 */
      #mathedu-report-toast {
        position: fixed !important;
        bottom: 30px !important;
        left: 50% !important;
        transform: translateX(-50%) translateY(20px) !important;
        z-index: 10000003 !important;
        background: rgba(13, 16, 32, 0.95) !important;
        border: 1px solid #3ddc97 !important;
        color: #f8fafc !important;
        padding: 12px 24px !important;
        border-radius: 999px !important;
        font-size: 0.9rem !important;
        font-weight: 700 !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(61, 220, 151, 0.3) !important;
        backdrop-filter: blur(16px) !important;
        opacity: 0;
        pointer-events: none;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
      }
      #mathedu-report-toast.show {
        opacity: 1 !important;
        transform: translateX(-50%) translateY(0) !important;
      }

      @media (max-width: 640px) {
        #mathedu-report-fab {
          top: 12px !important;
          right: 12px !important;
          padding: 6px 12px !important;
          font-size: 0.78rem !important;
          gap: 6px !important;
        }
        #mathedu-inspect-banner {
          padding: 10px 14px !important;
        }
        .mathedu-banner-left {
          font-size: 0.82rem;
        }
      }

      /* 6. 기존 개별 문항의 중복 인라인 '이 문제에 이상이 있어요' 버튼 완전 일반화 및 일원화 */
      .report-wrap {
        display: none !important;
      }
    `;

    var styleEl = document.createElement('style');
    styleEl.id = 'mathedu-report-styles';
    styleEl.textContent = css;
    document.head.appendChild(styleEl);
  }

  // 🚨 사이렌 SVG 아이콘 마크업 (참고 이미지 기반: 빨간 돔 + 황색 섬광 + 은색 받침대)
  function getSirenSvg() {
    return `
      <svg class="mathedu-siren-svg" viewBox="0 0 32 32" width="20" height="20" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path class="mathedu-siren-ray" d="M10 5L7 2" stroke="#FBBF24" stroke-width="2.2" stroke-linecap="round"/>
        <path class="mathedu-siren-ray" d="M16 4V1" stroke="#FBBF24" stroke-width="2.2" stroke-linecap="round"/>
        <path class="mathedu-siren-ray" d="M22 5L25 2" stroke="#FBBF24" stroke-width="2.2" stroke-linecap="round"/>
        <path d="M10 24C10 16 11.5 8 16 8C20.5 8 22 16 22 24H10Z" fill="url(#matheduSirenGrad)"/>
        <path d="M17.5 10.5C19.5 11.5 20.2 13.5 20.2 17" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round" opacity="0.85"/>
        <rect x="7" y="23" width="18" height="4" rx="2" fill="#E2E8F0"/>
        <rect x="6" y="26" width="20" height="3" rx="1.5" fill="#94A3B8"/>
        <defs>
          <linearGradient id="matheduSirenGrad" x1="10" y1="8" x2="22" y2="24" gradientUnits="userSpaceOnUse">
            <stop stop-color="#FF4D4F"/>
            <stop offset="0.6" stop-color="#EF4444"/>
            <stop offset="1" stop-color="#B91C1C"/>
          </linearGradient>
        </defs>
      </svg>
    `;
  }

  // 🛠️ DOM 요소 생성 및 마운트
  function createElements() {
    if (document.getElementById('mathedu-report-fab')) return;

    // 1. Fixed FAB
    var fab = document.createElement('button');
    fab.id = 'mathedu-report-fab';
    fab.type = 'button';
    fab.title = t('report.fabTooltip');
    fab.innerHTML = getSirenSvg() + '<span id="mathedu-report-fab-label">' + t('report.fabTitle') + '</span>';
    fab.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      MatheduReport.startInspect();
    });
    document.body.appendChild(fab);

    // 2. Inspect Banner
    var banner = document.createElement('div');
    banner.id = 'mathedu-inspect-banner';
    banner.innerHTML = `
      <div class="mathedu-banner-left">
        <span class="mathedu-banner-icon">🎯</span>
        <span id="mathedu-banner-prompt-text">${t('report.bannerPrompt')}</span>
      </div>
      <div class="mathedu-banner-right">
        <button type="button" class="mathedu-banner-btn" id="mathedu-inspect-cancel-btn">${t('report.bannerCancel')}</button>
        <button type="button" class="mathedu-banner-btn mathedu-banner-btn-whole" id="mathedu-inspect-whole-btn">${t('report.bannerWhole')}</button>
      </div>
    `;
    document.body.appendChild(banner);

    var cancelInspectBtn = banner.querySelector('#mathedu-inspect-cancel-btn');
    if (cancelInspectBtn) {
      cancelInspectBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        MatheduReport.stopInspect();
      });
    }
    var wholeInspectBtn = banner.querySelector('#mathedu-inspect-whole-btn');
    if (wholeInspectBtn) {
      wholeInspectBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        MatheduReport.stopInspect();
        MatheduReport.openModal(null);
      });
    }

    // 3. Inspect Box & Label
    var box = document.createElement('div');
    box.id = 'mathedu-inspect-box';
    var label = document.createElement('div');
    label.id = 'mathedu-inspect-label';
    label.textContent = '선택된 영역';
    box.appendChild(label);
    document.body.appendChild(box);

    // 4. Report Modal
    var modal = document.createElement('div');
    modal.id = 'mathedu-report-modal';
    modal.innerHTML = `
      <div class="mathedu-modal-card" onclick="event.stopPropagation()">
        <div class="mathedu-modal-header">
          <h3 class="mathedu-modal-title" id="mathedu-modal-title-text">
            ${getSirenSvg()}
            <span>${t('report.modalTitle')}</span>
          </h3>
          <button type="button" class="mathedu-modal-close" id="mathedu-modal-close-btn" title="닫기">&times;</button>
        </div>

        <!-- Target preview -->
        <div class="mathedu-target-preview">
          <div class="mathedu-target-top">
            <span class="mathedu-target-badge" id="mathedu-target-badge">🎯 ${t('report.targetTitle')}</span>
            <button type="button" class="mathedu-target-btn" id="mathedu-target-reselect-btn">${t('report.reselectBtn')}</button>
          </div>
          <div class="mathedu-target-snippet" id="mathedu-target-snippet-text">-</div>
        </div>

        <!-- Category -->
        <div class="mathedu-cat-group">
          <label class="mathedu-form-label" id="mathedu-label-cat">${t('report.categoryTitle')}</label>
          <div class="mathedu-cat-chips" id="mathedu-cat-chips-wrap">
            <div class="mathedu-cat-chip active" data-cat="math">${t('report.catMath')}</div>
            <div class="mathedu-cat-chip" data-cat="typo">${t('report.catTypo')}</div>
            <div class="mathedu-cat-chip" data-cat="answer">${t('report.catAnswer')}</div>
            <div class="mathedu-cat-chip" data-cat="graphic">${t('report.catGraphic')}</div>
            <div class="mathedu-cat-chip" data-cat="bug">${t('report.catBug')}</div>
            <div class="mathedu-cat-chip" data-cat="other">${t('report.catOther')}</div>
          </div>
        </div>

        <!-- Textarea -->
        <div>
          <label class="mathedu-form-label" id="mathedu-label-desc">${t('report.descTitle')}</label>
          <textarea class="mathedu-textarea" id="mathedu-report-textarea" rows="4" placeholder="${t('report.descPlaceholder')}"></textarea>
        </div>

        <!-- Reporter Row -->
        <div class="mathedu-reporter-row">
          <div>
            <label class="mathedu-form-label" id="mathedu-label-reporter">${t('report.reporterTitle')}</label>
            <input type="text" class="mathedu-input" id="mathedu-reporter-name" placeholder="선생님 / 학생">
          </div>
          <div>
            <label class="mathedu-form-label" id="mathedu-label-email">${t('report.emailTitle')}</label>
            <input type="email" class="mathedu-input" id="mathedu-reporter-email" placeholder="${t('report.emailPlaceholder')}">
          </div>
        </div>

        <!-- Actions -->
        <div class="mathedu-modal-footer">
          <button type="button" class="mathedu-btn-cancel" id="mathedu-btn-cancel">${t('report.cancelBtn')}</button>
          <button type="button" class="mathedu-btn-submit" id="mathedu-btn-submit">
            ${getSirenSvg()}
            <span id="mathedu-submit-text">${t('report.submitBtn')}</span>
          </button>
        </div>
      </div>
    `;
    document.body.appendChild(modal);

    modal.addEventListener('click', function(e) {
      if (e.target === modal) MatheduReport.closeModal();
    });
    var modalCloseBtn = modal.querySelector('#mathedu-modal-close-btn');
    if (modalCloseBtn) modalCloseBtn.addEventListener('click', function() { MatheduReport.closeModal(); });

    var btnCancel = modal.querySelector('#mathedu-btn-cancel');
    if (btnCancel) btnCancel.addEventListener('click', function() { MatheduReport.closeModal(); });

    var targetReselectBtn = modal.querySelector('#mathedu-target-reselect-btn');
    if (targetReselectBtn) targetReselectBtn.addEventListener('click', function() {
      MatheduReport.closeModal();
      MatheduReport.startInspect();
    });

    var btnSubmit = modal.querySelector('#mathedu-btn-submit');
    if (btnSubmit) btnSubmit.addEventListener('click', function() {
      submitCurrentReport();
    });

    // 카테고리 칩 선택 토글
    var chips = modal.querySelectorAll('.mathedu-cat-chip');
    chips.forEach(function(chip) {
      chip.addEventListener('click', function() {
        chips.forEach(function(c) { c.classList.remove('active'); });
        chip.classList.add('active');
      });
    });

    // 5. Toast
    var toast = document.createElement('div');
    toast.id = 'mathedu-report-toast';
    document.body.appendChild(toast);

    // ESC 키 핸들러
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        if (state.isInspecting) {
          MatheduReport.stopInspect();
        } else if (state.isModalOpen) {
          MatheduReport.closeModal();
        }
      }
    });

    // 기존 페이지의 레거시 `.report-btn` 버튼 연동
    attachLegacyButtons();
  }

  // 🔗 기존 inline '.report-btn' 버튼이 있다면 범용 리포터로 연결
  function attachLegacyButtons() {
    var legacyBtns = document.querySelectorAll('.report-btn');
    legacyBtns.forEach(function(btn) {
      if (btn._matheduHooked) return;
      btn._matheduHooked = true;
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        var qEl = btn.closest ? btn.closest('.q') : btn.parentElement;
        MatheduReport.openModal(qEl || btn);
      });
    });
  }

  // 🔍 요소 인스펙션 모드 시작
  function startInspect() {
    state.isInspecting = true;
    document.body.classList.add('mathedu-inspect-active');
    
    var banner = document.getElementById('mathedu-inspect-banner');
    if (banner) banner.style.display = 'flex';

    var box = document.getElementById('mathedu-inspect-box');
    if (box) box.style.display = 'none';

    document.addEventListener('mousemove', onInspectMouseMove, true);
    document.addEventListener('click', onInspectClick, true);
  }

  // 🛑 요소 인스펙션 모드 중단
  function stopInspect() {
    state.isInspecting = false;
    document.body.classList.remove('mathedu-inspect-active');

    var banner = document.getElementById('mathedu-inspect-banner');
    if (banner) banner.style.display = 'none';

    var box = document.getElementById('mathedu-inspect-box');
    if (box) box.style.display = 'none';

    document.removeEventListener('mousemove', onInspectMouseMove, true);
    document.removeEventListener('click', onInspectClick, true);
  }

  // 마우스 이동 시 하이라이트 박스 업데이트
  function onInspectMouseMove(e) {
    if (!state.isInspecting) return;

    var target = document.elementFromPoint(e.clientX, e.clientY);
    if (!target) return;

    // 리포터 관련 UI 요소 무시
    if (target.closest && (
      target.closest('#mathedu-report-fab') ||
      target.closest('#mathedu-inspect-banner') ||
      target.closest('#mathedu-inspect-box') ||
      target.closest('#mathedu-report-modal') ||
      target.closest('#mathedu-report-toast')
    )) {
      return;
    }

    state.hoveredEl = target;
    updateInspectBox(target);
  }

  // 클릭 시 해당 요소 선택 및 모달 열기
  function onInspectClick(e) {
    if (!state.isInspecting) return;

    var target = document.elementFromPoint(e.clientX, e.clientY);
    if (!target) return;

    // 리포터 관련 UI 배너/버튼 클릭 시 해당 이벤트 통과
    if (target.closest && (
      target.closest('#mathedu-report-fab') ||
      target.closest('#mathedu-inspect-banner') ||
      target.closest('#mathedu-report-modal')
    )) {
      return;
    }

    e.preventDefault();
    e.stopPropagation();

    stopInspect();
    MatheduReport.openModal(target);
  }

  // 요소 정보 추출 및 인스펙트 박스 위치 설정
  function updateInspectBox(el) {
    var box = document.getElementById('mathedu-inspect-box');
    var label = document.getElementById('mathedu-inspect-label');
    if (!box || !label) return;

    var rect = el.getBoundingClientRect();
    var scrollX = window.pageXOffset || document.documentElement.scrollLeft || 0;
    var scrollY = window.pageYOffset || document.documentElement.scrollTop || 0;

    box.style.display = 'block';
    box.style.top = (rect.top + scrollY) + 'px';
    box.style.left = (rect.left + scrollX) + 'px';
    box.style.width = rect.width + 'px';
    box.style.height = rect.height + 'px';

    var meta = getElementMeta(el);
    label.textContent = meta.label;
  }

  // 요소 메타데이터(단계, 이름, 요약 텍스트 등) 스마트 분석
  function getElementMeta(el) {
    if (!el) {
      return {
        label: t('report.targetWholePage'),
        snippet: window.location.href,
        stepNum: 0,
        selector: 'page'
      };
    }

    var qEl = el.closest ? el.closest('.q') : null;
    var stepNum = 0;
    if (qEl) {
      var allQ = Array.from(document.querySelectorAll('.q'));
      var idx = allQ.indexOf(qEl);
      stepNum = idx >= 0 ? (idx + 1) : 0;
    }

    var label = '';
    if (el.closest && el.closest('.opt')) {
      label = (stepNum > 0 ? ('제' + stepNum + '단계 ') : '') + '보기 항목';
    } else if (el.closest && el.closest('.stem')) {
      label = (stepNum > 0 ? ('제' + stepNum + '단계 ') : '') + '문제 지문';
    } else if (el.closest && el.closest('.exp')) {
      label = (stepNum > 0 ? ('제' + stepNum + '단계 ') : '') + '해설 / 풀이';
    } else if (el.closest && el.closest('.know')) {
      label = '사전 지식 영역';
    } else if (el.closest && (el.closest('svg') || el.closest('img') || el.closest('.diagram'))) {
      label = '기하 그림 / 다이어그램';
    } else if (el.closest && (el.closest('.math') || el.closest('mjx-container') || el.closest('.katex'))) {
      label = '수식 영역 (LaTeX)';
    } else if (qEl) {
      label = '제' + stepNum + '단계 문제 영역 전체';
    } else if (el.closest && el.closest('.top-nav-bar')) {
      label = '상단 네비게이션 메뉴';
    } else if (el.closest && el.closest('.brand-hero-card')) {
      label = '대표 엠블럼 히어로 카드';
    } else {
      var tag = el.tagName ? el.tagName.toLowerCase() : 'element';
      var cls = el.className && typeof el.className === 'string' ? ('.' + el.className.trim().split(/\s+/).slice(0, 2).join('.')) : '';
      label = tag + cls;
    }

    var rawText = (el.innerText || el.textContent || '').trim().replace(/\s+/g, ' ');
    var snippet = rawText.length > 120 ? (rawText.substring(0, 117) + '...') : (rawText || '(텍스트 없음 / 그래픽 또는 레이아웃 요소)');

    return {
      label: label,
      snippet: snippet,
      stepNum: stepNum,
      tag: el.tagName ? el.tagName.toLowerCase() : '',
      className: el.className ? String(el.className) : ''
    };
  }

  // 📝 모달 열기
  function openModal(targetEl) {
    state.selectedTarget = targetEl;
    state.isModalOpen = true;

    var modal = document.getElementById('mathedu-report-modal');
    if (!modal) return;

    var meta = getElementMeta(targetEl);
    var badge = document.getElementById('mathedu-target-badge');
    var snippet = document.getElementById('mathedu-target-snippet-text');
    var reselectBtn = document.getElementById('mathedu-target-reselect-btn');

    if (badge) badge.textContent = '🎯 ' + meta.label;
    if (snippet) snippet.textContent = meta.snippet;
    if (reselectBtn) reselectBtn.textContent = targetEl ? t('report.reselectBtn') : '🎯 특정 요소 선택';

    // 작성자 / 이메일 자동 채우기
    var nameInput = document.getElementById('mathedu-reporter-name');
    var emailInput = document.getElementById('mathedu-reporter-email');

    var currentName = '';
    var currentEmail = '';

    if (window.MatheduAuth && typeof window.MatheduAuth.getCurrentUser === 'function') {
      var user = window.MatheduAuth.getCurrentUser();
      if (user) {
        currentName = user.name || user.username || '';
        currentEmail = user.email || '';
      }
    }
    if (!currentName && window._studentName) {
      currentName = window._studentName;
    }
    if (!currentName) {
      try {
        currentName = localStorage.getItem('mathedu_guest_name') || '';
      } catch(e){}
    }

    if (nameInput && !nameInput.value) nameInput.value = currentName || '선생님 / 학생';
    if (emailInput && !emailInput.value) emailInput.value = currentEmail;

    var textarea = document.getElementById('mathedu-report-textarea');
    if (textarea) {
      textarea.value = '';
      setTimeout(function() { textarea.focus(); }, 150);
    }

    modal.style.display = 'flex';
  }

  // 🚪 모달 닫기
  function closeModal() {
    state.isModalOpen = false;
    var modal = document.getElementById('mathedu-report-modal');
    if (modal) modal.style.display = 'none';
  }

  // 🚀 신고 제출 실행
  function submitCurrentReport() {
    var textarea = document.getElementById('mathedu-report-textarea');
    var text = textarea ? textarea.value.trim() : '';

    if (!text) {
      showToast(t('report.errNoDesc'));
      if (textarea) textarea.focus();
      return;
    }

    var submitBtn = document.getElementById('mathedu-btn-submit');
    var submitText = document.getElementById('mathedu-submit-text');
    if (submitBtn) submitBtn.disabled = true;
    if (submitText) submitText.textContent = t('report.submitting');

    var activeChip = document.querySelector('.mathedu-cat-chip.active');
    var category = activeChip ? activeChip.textContent.trim() : '수식 / 계산 오류';

    var nameInput = document.getElementById('mathedu-reporter-name');
    var emailInput = document.getElementById('mathedu-reporter-email');
    var reporterName = nameInput ? (nameInput.value.trim() || '익명') : '익명';
    var email = emailInput ? emailInput.value.trim() : '';

    var meta = getElementMeta(state.selectedTarget);

    // 슬러그 추출
    var slug = '';
    var pathParts = window.location.pathname.split('/').filter(Boolean);
    var lastPart = pathParts.length ? pathParts[pathParts.length - 1] : '';
    if (lastPart.endsWith('.html')) {
      slug = lastPart.replace('.html', '');
    } else {
      slug = lastPart || 'index';
    }

    // 포맷팅된 최종 리포트 본문
    var formattedReport = [
      '[오류유형] ' + category,
      '[상세내용] ' + text,
      '[선택위치] ' + meta.label,
      '[발췌문구] ' + meta.snippet,
      '[페이지URL] ' + window.location.href,
      '[화면해상도] ' + window.innerWidth + 'x' + window.innerHeight,
      email ? ('[이메일] ' + email) : ''
    ].filter(Boolean).join('\n');

    var apiUrl = window._sheetsApiUrl || API_FALLBACK;
    var questionNum = meta.stepNum || 0;

    var payload = {
      action: 'report',
      quiz: slug,
      q: String(questionNum),
      name: reporterName,
      text: formattedReport
    };

    // 1) POST 전송 시도
    var fetchPromise = null;
    try {
      fetchPromise = fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'text/plain;charset=utf-8' },
        body: JSON.stringify(payload),
        mode: 'no-cors',
        keepalive: true
      });
    } catch(e){}

    // 2) Fallback: GET Beacon 전송 (Google Apps Script doGet 지원)
    var getUrl = apiUrl + '?action=report'
      + '&quiz=' + encodeURIComponent(slug)
      + '&q=' + encodeURIComponent(questionNum)
      + '&name=' + encodeURIComponent(reporterName)
      + '&text=' + encodeURIComponent(formattedReport)
      + '&_t=' + Date.now();

    try {
      var beaconImg = new Image();
      beaconImg.src = getUrl;
    } catch(e){}

    setTimeout(function() {
      if (submitBtn) submitBtn.disabled = false;
      if (submitText) submitText.textContent = t('report.submitBtn');
      closeModal();
      showToast(t('report.successToast'));

      // 기존 보드 페이지의 report-msg가 있다면 함께 활성화
      if (state.selectedTarget && state.selectedTarget.closest) {
        var wrap = state.selectedTarget.closest('.report-wrap');
        if (wrap) {
          var msg = wrap.querySelector('.report-msg');
          var form = wrap.querySelector('.report-form');
          if (msg) msg.style.display = 'block';
          if (form) form.style.display = 'none';
        }
      }
    }, 400);
  }

  // 🍞 토스트 팝업 표시
  function showToast(msg) {
    var toast = document.getElementById('mathedu-report-toast');
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add('show');
    setTimeout(function() {
      toast.classList.remove('show');
    }, 3500);
  }

  // 🌐 언어 변경 시 텍스트 동기화
  function updateTexts() {
    var fabLabel = document.getElementById('mathedu-report-fab-label');
    var fab = document.getElementById('mathedu-report-fab');
    if (fabLabel) fabLabel.textContent = t('report.fabTitle');
    if (fab) fab.title = t('report.fabTooltip');

    var bannerPrompt = document.getElementById('mathedu-banner-prompt-text');
    var bannerCancel = document.getElementById('mathedu-inspect-cancel-btn');
    var bannerWhole = document.getElementById('mathedu-inspect-whole-btn');
    if (bannerPrompt) bannerPrompt.textContent = t('report.bannerPrompt');
    if (bannerCancel) bannerCancel.textContent = t('report.bannerCancel');
    if (bannerWhole) bannerWhole.textContent = t('report.bannerWhole');

    var modalTitle = document.getElementById('mathedu-modal-title-text');
    if (modalTitle) {
      modalTitle.innerHTML = getSirenSvg() + '<span>' + t('report.modalTitle') + '</span>';
    }

    var labelCat = document.getElementById('mathedu-label-cat');
    var labelDesc = document.getElementById('mathedu-label-desc');
    var labelReporter = document.getElementById('mathedu-label-reporter');
    var labelEmail = document.getElementById('mathedu-label-email');
    var btnCancel = document.getElementById('mathedu-btn-cancel');
    var submitText = document.getElementById('mathedu-submit-text');
    var textarea = document.getElementById('mathedu-report-textarea');
    var emailInput = document.getElementById('mathedu-reporter-email');

    if (labelCat) labelCat.textContent = t('report.categoryTitle');
    if (labelDesc) labelDesc.textContent = t('report.descTitle');
    if (labelReporter) labelReporter.textContent = t('report.reporterTitle');
    if (labelEmail) labelEmail.textContent = t('report.emailTitle');
    if (btnCancel) btnCancel.textContent = t('report.cancelBtn');
    if (submitText) submitText.textContent = t('report.submitBtn');
    if (textarea) textarea.placeholder = t('report.descPlaceholder');
    if (emailInput) emailInput.placeholder = t('report.emailPlaceholder');

    var chipsWrap = document.getElementById('mathedu-cat-chips-wrap');
    if (chipsWrap) {
      var currentActiveCat = (chipsWrap.querySelector('.mathedu-cat-chip.active') || {}).dataset ? chipsWrap.querySelector('.mathedu-cat-chip.active').dataset.cat : 'math';
      chipsWrap.innerHTML = `
        <div class="mathedu-cat-chip ${currentActiveCat === 'math' ? 'active' : ''}" data-cat="math">${t('report.catMath')}</div>
        <div class="mathedu-cat-chip ${currentActiveCat === 'typo' ? 'active' : ''}" data-cat="typo">${t('report.catTypo')}</div>
        <div class="mathedu-cat-chip ${currentActiveCat === 'answer' ? 'active' : ''}" data-cat="answer">${t('report.catAnswer')}</div>
        <div class="mathedu-cat-chip ${currentActiveCat === 'graphic' ? 'active' : ''}" data-cat="graphic">${t('report.catGraphic')}</div>
        <div class="mathedu-cat-chip ${currentActiveCat === 'bug' ? 'active' : ''}" data-cat="bug">${t('report.catBug')}</div>
        <div class="mathedu-cat-chip ${currentActiveCat === 'other' ? 'active' : ''}" data-cat="other">${t('report.catOther')}</div>
      `;
      chipsWrap.querySelectorAll('.mathedu-cat-chip').forEach(function(chip) {
        chip.addEventListener('click', function() {
          chipsWrap.querySelectorAll('.mathedu-cat-chip').forEach(function(c) { c.classList.remove('active'); });
          chip.classList.add('active');
        });
      });
    }
  }

  // 🚀 초기화
  function init() {
    injectStyles();
    createElements();

    // 언어 변경 이벤트 청취
    window.addEventListener('mathedu:lang-changed', function() {
      updateTexts();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // 전역 API 노출
  window.MatheduReport = {
    init: init,
    startInspect: startInspect,
    stopInspect: stopInspect,
    openModal: openModal,
    closeModal: closeModal,
    submitCurrentReport: submitCurrentReport,
    showToast: showToast,
    updateTexts: updateTexts
  };

  // 레거시 inline 함수 호환성 연결
  window.toggleReport = function(el) {
    var qEl = el ? (el.closest ? el.closest('.q') : el.parentElement) : null;
    MatheduReport.openModal(qEl || el);
  };

})(window, document);
