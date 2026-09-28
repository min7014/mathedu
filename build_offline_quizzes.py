"""
build_offline_quizzes.py — 모든 수학 문제를 100% 독립 실행 가능한 오프라인 HTML 파일로 일괄 빌드
- 원본 이미지 Base64 인라인 변환 (외부 의존성 제로)
- 온라인 원본 문제 주소(https://min7014.github.io/mathedu/board/{slug}.html) 필수 배너 삽입
- 오프라인 단독 퀴즈 상호작용(채점, 정답, 해설, 점수바) 완벽 보장
- 온라인 연결 시 신규 버전 자동 감지, 업데이트 알림 모달 & 새 버전 다운로드/저장 및 기존 버전 풀이 선택권 제공
- offline/ 디렉토리에 {slug}.html, versions.json 및 오프라인 전체 목차(index.html) 자동 생성
"""
import os
import sys
import re
import base64
import json
import glob
import hashlib
import datetime

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOARD_DIR = os.path.join(BASE_DIR, 'board')
OFFLINE_DIR = os.path.join(BASE_DIR, 'offline')
ONLINE_BASE_URL = 'https://min7014.github.io/mathedu'

os.makedirs(OFFLINE_DIR, exist_ok=True)

OFFLINE_UPDATER_TEMPLATE = """
<!-- 🔔 min7014 mathedu 오프라인 업데이트 안내 모달 -->
<div id="matheduUpdateModal" class="mathedu-update-modal" style="display:none">
  <div class="mathedu-update-card">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
      <div class="mathedu-update-badge">🔔 최신 업데이트 감지</div>
      <button class="mathedu-update-close-btn" onclick="closeUpdateModal()">✕</button>
    </div>
    <h2 style="margin:0 0 8px;font-size:1.35rem;background:linear-gradient(90deg,#7cc4ff,#a78bfa);-webkit-background-clip:text;background-clip:text;color:transparent;font-weight:800">
      ✨ 이 문제의 최신 버전이 있습니다!
    </h2>
    <p style="margin:0 0 16px;color:#cbd5e1;font-size:0.9rem;line-height:1.55">
      선생님께서 문제의 해설 보강, 질문 개선, 또는 새로운 인터랙티브 디딤돌 단계를 업데이트하셨습니다.<br>
      새로운 버전을 다운로드하여 저장 후 풀이하시거나, 지금 바로 현재 버전으로 계속 푸실 수 있습니다.
    </p>

    <div class="mathedu-ver-box">
      <div class="mathedu-ver-item cur">
        <span class="mathedu-ver-lbl">현재 내 오프라인 버전</span>
        <b id="lblCurrentVer">-</b>
      </div>
      <div style="color:#7cc4ff;font-size:1.2rem;font-weight:800">➔</div>
      <div class="mathedu-ver-item new">
        <span class="mathedu-ver-lbl">🚀 온라인 최신 버전</span>
        <b id="lblLatestVer">-</b>
      </div>
    </div>

    <!-- 옵션: 새 버전 다운로드 vs 그냥 현재 버전으로 풀기 -->
    <div class="mathedu-update-btn-row">
      <button id="btnDownloadUpdate" class="mathedu-btn-primary" onclick="downloadLatestOfflineVersion()">
        📥 새 버전 내려받아서 풀기 (저장)
      </button>
      <button class="mathedu-btn-sec" onclick="continueCurrentVersion()">
        📝 그냥 현재 버전으로 풀기
      </button>
      <a id="btnOpenOnlineLatest" href="__ORIGINAL_ONLINE_URL__" target="_blank" rel="noopener" class="mathedu-btn-link">
        🌐 온라인 최신판 웹으로 바로 열기 ➔
      </a>
    </div>

    <div id="updateDownloadSuccess" style="display:none;margin-top:16px;background:rgba(94,234,212,.15);border:1px solid #5eead4;border-radius:12px;padding:14px;text-align:left">
      <div style="font-weight:800;color:#5eead4;margin-bottom:4px">🎉 최신 버전 다운로드 완료!</div>
      <div style="font-size:0.86rem;color:#e2e8f0;line-height:1.5">
        다운로드 폴더에 최신 문제 파일(<code>mathedu___SLUG___offline_latest.html</code>)이 저장되었습니다. 새로 저장된 파일을 브라우저로 열어 풀이하시거나, 온라인 최신 페이지로 바로 이동하실 수 있습니다.
      </div>
      <div style="margin-top:12px;display:flex;gap:8px">
        <a href="__ORIGINAL_ONLINE_URL__" target="_blank" rel="noopener" style="background:#5eead4;color:#0b1020;padding:7px 16px;border-radius:8px;font-size:0.84rem;font-weight:800;text-decoration:none">🌐 온라인 최신판 열기</a>
        <button onclick="closeUpdateModal()" style="background:transparent;border:1px solid #5eead4;color:#5eead4;padding:7px 16px;border-radius:8px;font-size:0.84rem;cursor:pointer;font-weight:700">✕ 닫고 현재 화면 풀기</button>
      </div>
    </div>
  </div>
</div>

<style>
.mathedu-update-modal {
  position: fixed; inset: 0; z-index: 999999;
  background: rgba(10, 13, 26, 0.85);
  backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
  display: flex; align-items: center; justify-content: center;
  padding: 16px; animation: matheduFadeIn .2s ease;
}
@keyframes matheduFadeIn { from { opacity: 0; transform: scale(.97); } to { opacity: 1; transform: scale(1); } }
.mathedu-update-card {
  background: #141833; border: 1.5px solid rgba(124, 196, 255, 0.4);
  border-radius: 20px; max-width: 520px; width: 100%; padding: 26px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.65); color: #eef2ff;
  font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
  position: relative; line-height: 1.6;
}
.mathedu-update-badge {
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(253, 230, 138, 0.15); border: 1px solid #fde68a; color: #fde68a;
  border-radius: 20px; padding: 4px 12px; font-size: 0.8rem; font-weight: 800;
}
.mathedu-update-close-btn {
  background: transparent; border: none; color: #94a3b8; font-size: 1.4rem; cursor: pointer; padding: 0 4px;
}
.mathedu-update-close-btn:hover { color: #fff; }
.mathedu-ver-box {
  display: grid; grid-template-columns: 1fr auto 1fr; gap: 10px; align-items: center;
  background: rgba(13, 16, 32, 0.7); border: 1px solid rgba(255,255,255,0.12);
  border-radius: 12px; padding: 12px 14px; margin: 16px 0; text-align: center;
}
.mathedu-ver-item { font-size: 0.8rem; color: #94a3b8; }
.mathedu-ver-item b { display: block; font-size: 0.95rem; margin-top: 2px; }
.mathedu-ver-item.cur b { color: #cbd5e1; }
.mathedu-ver-item.new b { color: #5eead4; }
.mathedu-update-btn-row {
  display: flex; flex-direction: column; gap: 8px; margin-top: 18px;
}
.mathedu-btn-primary {
  background: linear-gradient(90deg, #38bdf8, #818cf8); color: #0b1020;
  border: none; border-radius: 10px; padding: 12px 18px; font-size: 0.96rem;
  font-weight: 800; cursor: pointer; transition: .15s; text-align: center;
  box-shadow: 0 4px 16px rgba(56,189,248,0.35); text-decoration: none;
}
.mathedu-btn-primary:hover { transform: translateY(-1px); box-shadow: 0 6px 22px rgba(56,189,248,0.5); }
.mathedu-btn-sec {
  background: rgba(255, 255, 255, 0.1); color: #eef2ff;
  border: 1px solid rgba(255,255,255,0.2); border-radius: 10px; padding: 11px 18px;
  font-size: 0.92rem; font-weight: 700; cursor: pointer; transition: .15s; text-align: center;
}
.mathedu-btn-sec:hover { background: rgba(255,255,255,0.18); border-color: rgba(255,255,255,0.35); }
.mathedu-btn-link {
  background: transparent; color: #7cc4ff; border: none; padding: 6px;
  font-size: 0.85rem; cursor: pointer; text-decoration: underline; text-align: center;
}
</style>

<script>
// 오프라인 실행 보장 및 실시간 업데이트 확인 스크립트
window._isOfflineFile = true;
window._offlineQuizSlug = '__SLUG__';
window._offlineBuildTime = '__BUILD_TIMESTAMP__';
window._offlineHash = '__CONTENT_HASH__';
window._offlineVersion = '__BUILD_VERSION__';
window._originalUrl = '__ORIGINAL_ONLINE_URL__';

document.addEventListener("DOMContentLoaded", function() {
  var tf = document.getElementById("trackFull");
  if (tf) {
    var quickBtn = document.createElement("button");
    quickBtn.type = "button";
    quickBtn.className = "btn";
    quickBtn.style.cssText = "background:rgba(56,189,248,.2);border:1px solid #38bdf8;color:#38bdf8;font-size:.9rem;padding:8px 16px;border-radius:10px;cursor:pointer;margin-top:10px;font-weight:700;";
    quickBtn.innerHTML = "⚡ 오프라인 바로 시작하기";
    quickBtn.onclick = function() {
      window._studentName = "오프라인 학습자";
      tf.remove();
      if (window.sendProgress) sendProgress();
      if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise();
    };
    tf.appendChild(quickBtn);
  }
});

// === 온라인 상태 시 최신 업데이트 확인 엔진 ===
(function() {
  var slug = window._offlineQuizSlug || '__SLUG__';
  var localBuildTime = window._offlineBuildTime || '__BUILD_TIMESTAMP__';
  var localHash = window._offlineHash || '__CONTENT_HASH__';
  var originalUrl = window._originalUrl || '__ORIGINAL_ONLINE_URL__';
  var offlineDownloadUrl = 'https://min7014.github.io/mathedu/offline/' + slug + '.html';
  var versionsApiUrl = 'https://min7014.github.io/mathedu/offline/versions.json';

  window._serverUpdateInfo = null;

  function formatTime(isoStr) {
    if (!isoStr) return '-';
    try {
      var d = new Date(isoStr);
      if (isNaN(d.getTime())) return isoStr;
      return d.getFullYear() + '.' + (d.getMonth() + 1) + '.' + d.getDate() + ' ' + (d.getHours() < 10 ? '0' : '') + d.getHours() + ':' + (d.getMinutes() < 10 ? '0' : '') + d.getMinutes();
    } catch(e) {
      return isoStr;
    }
  }

  window.openUpdateModal = function() {
    var modal = document.getElementById('matheduUpdateModal');
    if (!modal) return;
    var info = window._serverUpdateInfo || {};
    var lblCur = document.getElementById('lblCurrentVer');
    var lblNew = document.getElementById('lblLatestVer');
    if (lblCur) lblCur.textContent = formatTime(localBuildTime);
    if (lblNew) lblNew.textContent = formatTime(info.updated_at || new Date().toISOString());
    modal.style.display = 'flex';
  };

  window.closeUpdateModal = function() {
    var modal = document.getElementById('matheduUpdateModal');
    if (modal) modal.style.display = 'none';
  };

  window.continueCurrentVersion = function() {
    closeUpdateModal();
    try {
      sessionStorage.setItem('mathedu_update_dismissed_' + slug, 'true');
    } catch(e) {}
  };

  window.downloadLatestOfflineVersion = async function() {
    var btn = document.getElementById('btnDownloadUpdate');
    var origText = btn ? btn.innerHTML : '';
    if (btn) {
      btn.innerHTML = '⏳ 최신 버전 다운로드 중...';
      btn.style.pointerEvents = 'none';
    }

    try {
      var res = await fetch(offlineDownloadUrl + '?_t=' + Date.now());
      if (!res.ok) throw new Error('파일을 가져올 수 없습니다 (HTTP ' + res.status + ')');
      var blob = await res.blob();
      var url = URL.createObjectURL(blob);
      var a = document.createElement('a');
      a.href = url;
      a.download = 'mathedu_' + slug + '_offline_latest.html';
      document.body.appendChild(a);
      a.click();
      setTimeout(function() {
        a.remove();
        URL.revokeObjectURL(url);
      }, 500);

      if (btn) btn.innerHTML = '✅ 새 버전 저장 완료!';
      var succBox = document.getElementById('updateDownloadSuccess');
      if (succBox) succBox.style.display = 'block';
    } catch(err) {
      alert('새 버전 직접 다운로드 중 오류: ' + err.message + '\\n온라인 최신 페이지로 이동합니다.');
      window.open(originalUrl, '_blank');
      if (btn) {
        btn.innerHTML = origText;
        btn.style.pointerEvents = '';
      }
    }
  };

  window.checkUpdateManual = function() {
    var btn = document.getElementById('btnManualCheckUpdate');
    if (btn) btn.innerHTML = '⏳ 확인 중...';
    performCheck(true);
  };

  function showUpdateDetected(serverInfo) {
    window._serverUpdateInfo = serverInfo;

    var alertSlot = document.getElementById('matheduUpdateAlertSlot');
    if (alertSlot) alertSlot.style.display = 'flex';

    var btnManual = document.getElementById('btnManualCheckUpdate');
    if (btnManual) {
      btnManual.innerHTML = '✨ 새 버전 있음!';
      btnManual.style.background = 'rgba(253,230,138,.25)';
      btnManual.style.color = '#fde68a';
      btnManual.style.borderColor = '#fde68a';
    }

    var dismissed = false;
    try {
      dismissed = sessionStorage.getItem('mathedu_update_dismissed_' + slug) === 'true';
    } catch(e) {}

    if (!dismissed) {
      openUpdateModal();
    }
  }

  function performCheck(isManual) {
    if (!navigator.onLine) {
      if (isManual) alert('현재 오프라인 상태입니다. 인터넷에 연결된 후 다시 확인해주세요.');
      var btn = document.getElementById('btnManualCheckUpdate');
      if (btn) btn.innerHTML = '📡 오프라인 상태';
      return;
    }

    var cacheBust = '?_t=' + Date.now();
    fetch(versionsApiUrl + cacheBust, { cache: 'no-cache' })
      .then(function(res) {
        if (!res.ok) throw new Error('versions.json 응답 오류');
        return res.json();
      })
      .then(function(data) {
        var serverItem = (data && data.quizzes && data.quizzes[slug]) ? data.quizzes[slug] : null;
        if (serverItem) {
          var serverTime = serverItem.updated_at;
          var serverHash = serverItem.hash;
          var hasNewVer = false;

          if (serverHash && localHash && serverHash !== localHash) {
            hasNewVer = true;
          } else if (serverTime && localBuildTime) {
            var diff = new Date(serverTime).getTime() - new Date(localBuildTime).getTime();
            if (diff > 60 * 1000) hasNewVer = true;
          }

          if (hasNewVer) {
            showUpdateDetected(serverItem);
          } else {
            handleUpToDate(isManual);
          }
        } else {
          fallbackCheckHead(isManual);
        }
      })
      .catch(function() {
        fallbackCheckHead(isManual);
      });
  }

  function fallbackCheckHead(isManual) {
    fetch(offlineDownloadUrl + '?_t=' + Date.now(), { method: 'HEAD', cache: 'no-cache' })
      .then(function(res) {
        if (!res.ok) throw new Error('HEAD 실패');
        var lastMod = res.headers.get('Last-Modified');
        if (lastMod && localBuildTime) {
          var diff = new Date(lastMod).getTime() - new Date(localBuildTime).getTime();
          if (diff > 120 * 1000) {
            showUpdateDetected({ updated_at: new Date(lastMod).toISOString() });
            return;
          }
        }
        handleUpToDate(isManual);
      })
      .catch(function() {
        handleUpToDate(isManual);
      });
  }

  function handleUpToDate(isManual) {
    var btn = document.getElementById('btnManualCheckUpdate');
    if (btn) {
      btn.innerHTML = '✅ 최신 버전';
      btn.style.color = '#5eead4';
      btn.style.borderColor = 'rgba(94,234,212,.4)';
    }
    if (isManual) {
      alert('현재 문제 파일이 가장 최신 버전입니다! (새로운 업데이트 없음)');
    }
  }

  setTimeout(function() {
    performCheck(false);
  }, 1000);

  window.addEventListener('online', function() {
    performCheck(false);
  });
})();
</script>
"""

def image_to_base64(img_path):
    if not os.path.isfile(img_path):
        return None
    ext = os.path.splitext(img_path)[1].lower().replace('.', '')
    if ext == 'jpg': ext = 'jpeg'
    mime = f'image/{ext}' if ext in ['png', 'jpeg', 'gif', 'svg', 'webp'] else 'image/png'
    with open(img_path, 'rb') as f:
        encoded = base64.b64encode(f.read()).decode('utf-8')
    return f'data:{mime};base64,{encoded}'

def extract_title(html_content, slug):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html_content, re.DOTALL)
    if m:
        t = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        t = re.sub(r'^[📘📙📕📝]\s*', '', t)
        return t
    m_title = re.search(r'<title>(.*?)</title>', html_content, re.DOTALL)
    if m_title:
        return m_title.group(1).split('·')[0].split('—')[0].strip()
    return slug

def process_file(html_path, build_timestamp, build_version):
    filename = os.path.basename(html_path)
    slug = os.path.splitext(filename)[0]

    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    title = extract_title(content, slug)
    original_online_url = f"{ONLINE_BASE_URL}/board/{slug}.html"
    content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()[:8]

    # 1. 이미지 Base64 인라인화
    def replace_img(match):
        img_tag = match.group(0)
        src_match = re.search(r'src=["\']([^"\']+)["\']', img_tag)
        if not src_match:
            return img_tag
        src = src_match.group(1)
        if src.startswith('data:'):
            return img_tag

        candidate_paths = [
            os.path.join(BOARD_DIR, src),
            os.path.join(BASE_DIR, src),
            os.path.join(BOARD_DIR, os.path.basename(src)),
            os.path.join(BASE_DIR, 'assets', os.path.basename(src))
        ]
        for p in candidate_paths:
            if os.path.isfile(p):
                b64 = image_to_base64(p)
                if b64:
                    return re.sub(r'src=["\'][^"\']+["\']', f'src="{b64}"', img_tag)
        return img_tag

    content = re.sub(r'<img[^>]+>', replace_img, content)

    # 1-1. MathJax 스크립트: 오프라인 로컬 우선 + CDN 폴백
    content = re.sub(
        r'<script id="mj"[^>]*></script>',
        r'<script id="mj" async src="mathjax/tex-mml-chtml.js" onerror="this.onerror=null;this.src=\'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js\'"></script>',
        content
    )

    # 1-2. 네비게이션 바 링크를 오프라인 환경에 맞게 보정
    content = content.replace('href="/board/6wol_mopyung.html"', 'href="index.html"')
    content = content.replace('href="/"', 'href="https://min7014.github.io/mathedu/" target="_blank" rel="noopener"')

    # 1-3. 파비콘 Base64 인라인화
    fav_path = os.path.join(BASE_DIR, 'assets', 'favicon.png')
    fav_b64 = image_to_base64(fav_path)
    if fav_b64:
        content = re.sub(r'href=["\'][^"\']*favicon\.png["\']', f'href="{fav_b64}"', content)

    # 1-4. 온라인 전용 교실 스크립트 제거 (오프라인 환경 404 방지)
    content = re.sub(r'<script[^>]*src=["\'][^"\']*mathedu-room\.js["\'][^>]*></script>', '', content)

    # 2. 오프라인 메타 태그 삽입
    meta_tags = f"""
<link rel="canonical" href="{original_online_url}">
<meta name="original-problem-url" content="{original_online_url}">
<meta name="mathedu-offline-version" content="true">
<meta name="mathedu-quiz-slug" content="{slug}">
<meta name="mathedu-offline-build-time" content="{build_timestamp}">
<meta name="mathedu-offline-hash" content="{content_hash}">
<meta name="mathedu-version-label" content="{build_version}">
"""
    if '</head>' in content:
        content = content.replace('</head>', f'{meta_tags}\n</head>')

    # 3. 오프라인 단독 실행 배너 & 원본 주소 링크 카드 생성
    offline_banner = f"""
<!-- 🌐 오프라인 단독 학습 배너 & 온라인 원본 문제 링크 안내 -->
<div class="mathedu-offline-banner" style="background:linear-gradient(135deg,rgba(56,189,248,.18),rgba(129,140,248,.18));border:2px solid #38bdf8;border-radius:16px;padding:18px 22px;margin:16px 0 24px;box-shadow:0 8px 30px rgba(0,0,0,.45);color:#fff;font-family:system-ui,sans-serif">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:10px">
    <div style="display:inline-flex;align-items:center;gap:6px;background:rgba(56,189,248,.25);border:1px solid #38bdf8;color:#38bdf8;border-radius:20px;padding:4px 14px;font-size:0.82rem;font-weight:800">
      📦 오프라인 단독 실행 파일 (인터넷 접속 없이 풀이 가능)
    </div>
    <div style="display:flex;align-items:center;gap:8px">
      <button id="btnManualCheckUpdate" onclick="checkUpdateManual()" style="background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);color:#cbd5e1;padding:3px 12px;border-radius:14px;font-size:0.75rem;cursor:pointer;font-family:inherit;transition:.15s">🔄 최신 버전 확인</button>
      <span style="font-size:0.78rem;color:#94a3b8">min7014 mathedu</span>
    </div>
  </div>
  <div style="font-size:1.15rem;font-weight:800;color:#ffffff;margin-bottom:6px">{title}</div>
  <div style="font-size:0.86rem;color:#cbd5e1;line-height:1.5;margin-bottom:12px">
    이 파일은 인터넷 연결 없이 웹 브라우저에서 언제든 풀 수 있는 <b>단독 오프라인 인터랙티브 수학 퀴즈</b>입니다.<br>
    보기를 클릭하면 채점과 단계별 상세 해설이 열리며, 점수가 자동 계산됩니다.
  </div>

  <!-- 🔔 업데이트 감지 시 표시되는 인라인 알림 바 -->
  <div id="matheduUpdateAlertSlot" style="display:none;margin-bottom:12px;padding:12px 16px;background:rgba(253,230,138,.14);border:1.5px solid #fde68a;border-radius:12px;color:#fde68a;font-size:0.88rem;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px">
    <div style="display:flex;align-items:center;gap:8px">
      <span style="font-size:1.1rem">🔔</span>
      <span><b>이 문제의 최신 업데이트 버전이 있습니다!</b> (새 버전으로 저장 후 풀이 가능)</span>
    </div>
    <button onclick="openUpdateModal()" style="background:#fde68a;color:#0b1020;border:none;padding:6px 14px;border-radius:8px;font-weight:800;font-size:0.82rem;cursor:pointer">업데이트 보기 ➔</button>
  </div>

  <div style="background:rgba(15,23,42,.7);border:1px solid rgba(255,255,255,.14);border-radius:12px;padding:12px 16px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px">
    <div style="font-size:0.85rem;color:#e2e8f0;word-break:break-all">
      <span style="color:#7cc4ff;font-weight:700">🌐 온라인 원본 문제 주소:</span><br>
      <a href="{original_online_url}" target="_blank" rel="noopener" style="color:#38bdf8;font-weight:700;text-decoration:underline;font-family:monospace">
        {original_online_url}
      </a>
    </div>
    <div style="display:flex;gap:8px">
      <a href="{original_online_url}" target="_blank" rel="noopener" style="background:linear-gradient(90deg,#38bdf8,#818cf8);color:#0b1020;padding:8px 16px;border-radius:8px;font-size:0.82rem;font-weight:800;text-decoration:none;display:inline-flex;align-items:center;gap:4px">
        🌐 온라인 원본 열기 ➔
      </a>
      <a href="https://min7014.github.io/" target="_blank" rel="noopener" style="background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);color:#eef2ff;padding:8px 14px;border-radius:8px;font-size:0.82rem;font-weight:700;text-decoration:none">
        🏛️ min7014 자료실
      </a>
    </div>
  </div>
</div>
"""
    # wrap 다음 또는 body 다음에 배너 삽입
    if '<div class="wrap">' in content:
        content = content.replace('<div class="wrap">', f'<div class="wrap">\n{offline_banner}')
    elif '<body>' in content:
        content = content.replace('<body>', f'<body>\n{offline_banner}')

    # 4. #trackFull 시작 모달 보강 + 오프라인 업데이트 확인 모달 및 스크립트 치환 삽입
    updater_html = OFFLINE_UPDATER_TEMPLATE
    updater_html = updater_html.replace('__SLUG__', slug)
    updater_html = updater_html.replace('__ORIGINAL_ONLINE_URL__', original_online_url)
    updater_html = updater_html.replace('__BUILD_TIMESTAMP__', build_timestamp)
    updater_html = updater_html.replace('__CONTENT_HASH__', content_hash)
    updater_html = updater_html.replace('__BUILD_VERSION__', build_version)

    if '</body>' in content:
        content = content.replace('</body>', f'{updater_html}\n</body>')

    out_path = os.path.join(OFFLINE_DIR, filename)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return {
        'slug': slug,
        'title': title,
        'filename': filename,
        'original_online_url': original_online_url,
        'size': len(content),
        'hash': content_hash,
        'updated_at': build_timestamp,
        'version': build_version
    }

def main():
    # 수능 및 모의평가 전용 공개 원칙에 따라 board/index.json의 공개 문항만 빌드
    index_json_path = os.path.join(BOARD_DIR, 'index.json')
    public_slugs = set()
    if os.path.exists(index_json_path):
        with open(index_json_path, 'r', encoding='utf-8') as f:
            public_items = json.load(f)
            public_slugs = set(it['slug'] for it in public_items if it.get('is_public') is not False)

    files = sorted(glob.glob(os.path.join(BOARD_DIR, '*.html')))
    quiz_files = [
        f for f in files 
        if not os.path.basename(f).startswith('index') 
        and (not public_slugs or os.path.splitext(os.path.basename(f))[0] in public_slugs)
    ]

    # 비공개 문항 오프라인 파일은 offline/private/ 로 격리 보관
    offline_private_dir = os.path.join(OFFLINE_DIR, 'private')
    os.makedirs(offline_private_dir, exist_ok=True)
    existing_offline_files = glob.glob(os.path.join(OFFLINE_DIR, '*.html'))
    for off_f in existing_offline_files:
        base_name = os.path.basename(off_f)
        if base_name in ['index.html']:
            continue
        slug_name = os.path.splitext(base_name)[0]
        if public_slugs and slug_name not in public_slugs:
            # Move to offline/private/
            target_path = os.path.join(offline_private_dir, base_name)
            if os.path.exists(target_path):
                os.remove(target_path)
            os.rename(off_f, target_path)

    build_timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    build_date_str = datetime.datetime.now().strftime("%Y.%m.%d")
    build_version = f"v{build_date_str}"

    print(f"공개 대상(수능·모의평가) 총 {len(quiz_files)}개 퀴즈 파일을 오프라인 패키지로 변환 시작... (빌드 시각: {build_timestamp})")
    results = []
    for f in quiz_files:
        res = process_file(f, build_timestamp, build_version)
        results.append(res)

    # 1. 버전 매니페스트 (offline/versions.json) 생성
    versions_data = {
        "generated_at": build_timestamp,
        "version": build_version,
        "quizzes": {}
    }
    for r in results:
        versions_data["quizzes"][r['slug']] = {
            "slug": r['slug'],
            "title": r['title'],
            "filename": r['filename'],
            "updated_at": r['updated_at'],
            "version": r['version'],
            "hash": r['hash'],
            "size": r['size']
        }
    with open(os.path.join(OFFLINE_DIR, 'versions.json'), 'w', encoding='utf-8') as f:
        json.dump(versions_data, f, ensure_ascii=False, indent=2)

    # 2. 오프라인 인덱스 페이지(offline/index.html) 생성
    index_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>min7014 mathedu · 오프라인 전체 문제 보관함</title>
<link rel="icon" type="image/png" sizes="32x32" href="../assets/favicon.png">
<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
<style>
:root {{
  --bg: #050811; --card: rgba(15, 23, 42, 0.72); --card2: rgba(30, 41, 59, 0.75); --line: rgba(255,255,255,.12);
  --txt: #f8fafc; --sub: #94a3b8; --accent: #38bdf8; --accent2: #818cf8; --good: #34d399; --gold: #fbbf24;
  --glass-blur: 24px; --glass-shadow: 0 16px 40px -10px rgba(0,0,0,.6), inset 0 1px 0 rgba(255,255,255,.12);
  --radius: 18px;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  color: var(--txt); line-height: 1.65;
  font-family: "Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
  -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;
  background:
    radial-gradient(circle at 14% 12%, rgba(56, 189, 248, 0.16) 0%, transparent 45%),
    radial-gradient(circle at 86% 16%, rgba(129, 140, 248, 0.16) 0%, transparent 45%),
    radial-gradient(circle at 50% 50%, rgba(168, 85, 247, 0.10) 0%, transparent 50%),
    radial-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px),
    linear-gradient(175deg, #050811 0%, #0b1022 45%, #060914 100%);
  background-size: 100% 100%, 100% 100%, 100% 100%, 30px 30px, 100% 100%;
  background-attachment: fixed; min-height: 100vh; padding: 36px 20px 80px;
}}
.wrap {{ max-width: 960px; margin: 0 auto; }}
h1 {{
  font-size: 2.2rem; background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent;
  font-weight: 800; margin-bottom: 8px; letter-spacing: -0.02em;
}}
.lead {{ color: var(--sub); font-size: 1.02rem; margin-bottom: 28px; }}
.banner {{
  background: linear-gradient(135deg, rgba(56,189,248,.15), rgba(15,23,42,.8));
  border: 1px solid rgba(56,189,248,.38); border-radius: var(--radius);
  padding: 22px 26px; margin-bottom: 30px; box-shadow: var(--glass-shadow);
  backdrop-filter: blur(var(--glass-blur)); -webkit-backdrop-filter: blur(var(--glass-blur));
}}
.list {{ display: grid; gap: 14px; }}
.card {{
  background: linear-gradient(145deg, rgba(255,255,255,0.05) 0%, rgba(15,23,42,0.78) 100%);
  border: 1px solid rgba(255,255,255,.10); border-radius: var(--radius);
  padding: 20px 24px; display: flex; align-items: center; justify-content: space-between;
  gap: 18px; flex-wrap: wrap; transition: .25s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 10px 30px -8px rgba(0,0,0,.5), inset 0 1px 0 rgba(255,255,255,.1);
  backdrop-filter: blur(var(--glass-blur)); -webkit-backdrop-filter: blur(var(--glass-blur));
}}
.card:hover {{
  border-color: rgba(56,189,248,.45); transform: translateY(-3px);
  box-shadow: 0 20px 45px -10px rgba(56,189,248,.25), inset 0 1px 0 rgba(255,255,255,.2);
}}
.card-title {{ font-size: 1.08rem; font-weight: 700; color: #fff; text-decoration: none; letter-spacing: -0.01em; }}
.card-title:hover {{ color: var(--accent); }}
.card-meta {{ font-size: 0.84rem; color: var(--sub); margin-top: 6px; }}
.btn {{
  background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%); color: #050811;
  padding: 10px 20px; border-radius: 12px; font-weight: 800; font-size: 0.88rem;
  text-decoration: none; display: inline-flex; align-items: center; gap: 6px;
  box-shadow: 0 4px 16px rgba(56,189,248,.4); transition: transform .2s, box-shadow .2s;
}}
.btn:hover {{
  transform: translateY(-2px); box-shadow: 0 8px 24px rgba(56,189,248,.6);
}}
.lang-switcher {{
  display: inline-flex; align-items: center; background: rgba(15,23,42,0.75);
  border: 1px solid rgba(124,196,255,0.35); border-radius: 20px; padding: 2px 4px; gap: 3px;
}}
.lang-btn {{
  background: transparent; border: none; color: var(--sub); font-family: inherit;
  font-size: 0.78rem; font-weight: 800; padding: 4px 9px; border-radius: 14px; cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16,1,0.3,1);
}}
.lang-btn:hover {{ color: #ffffff; background: rgba(255,255,255,0.08); }}
.lang-btn.active {{
  background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%); color: #050811;
  box-shadow: 0 2px 10px rgba(56,189,248,0.45);
}}
</style>
</head>
<body>
<div class="wrap">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:24px">
    <a href="../index.html" style="color:var(--accent);text-decoration:none;font-weight:700;font-size:0.9rem;display:inline-flex;align-items:center;gap:6px">⬅️ <span id="txtBackLink">mathedu 메인으로</span></a>
    <div class="lang-switcher" id="langSwitcher" title="Language">
      <button type="button" class="lang-btn active" data-lang-btn="ko" onclick="setOfflineLang('ko')">🇰🇷 KO</button>
      <button type="button" class="lang-btn" data-lang-btn="en" onclick="setOfflineLang('en')">🌐 EN</button>
    </div>
  </div>

  <h1 id="txtTitle">📦 min7014 mathedu 오프라인 전체 문제 보관함</h1>
  <p class="lead" id="txtLead">인터넷 접속 없이 언제 어디서나 풀이할 수 있는 오프라인 독립 실행형 수학 퀴즈 모음입니다.</p>

  <div class="banner">
    <div style="font-weight:700;color:var(--good);margin-bottom:4px" id="txtBannerTitle">💡 오프라인 단독 파일 안내</div>
    <div style="font-size:0.88rem;color:#cbd5e1" id="txtBannerBody">
      • 각 문제 파일은 이미지와 인터랙티브 채점 로직이 포함된 <b>단일 HTML 파일</b>입니다.<br>
      • 모든 문제에는 온라인 원본 주소(<code>https://min7014.github.io/mathedu/board/...</code>) 및 민은기 선생님 수학자료실 링크가 포함되어 있습니다.<br>
      • 온라인 상태가 되면 <b>새로운 업데이트 버전이 있는지 자동 감지</b>하여 알림창을 통해 [새 버전 내려받기] 또는 [현재 버전 풀기]를 선택할 수 있습니다.<br>
      • 총 <b>{len(results)}개</b>의 문제 파일이 준비되어 있습니다.
    </div>
  </div>

  <div class="list">
"""
    for r in results:
        index_html += f"""    <div class="card">
      <div>
        <a href="{r['filename']}" class="card-title">📘 {r['title']}</a>
        <div class="card-meta">
          <span><span class="txt-slug-prefix">고유 슬러그: </span><code>{r['slug']}</code></span> · 
          <a href="{r['original_online_url']}" target="_blank" rel="noopener" style="color:var(--accent);text-decoration:underline" class="link-online-text">온라인 원본 링크 ➔</a>
        </div>
      </div>
      <div>
        <a href="{r['filename']}" class="btn" download><span class="btn-download-text">📥 다운로드</span></a>
        <a href="{r['filename']}" class="btn" style="background:rgba(255,255,255,.1);color:#fff;border:1px solid var(--line);margin-left:6px"><span class="btn-solve-text">풀기 ➔</span></a>
      </div>
    </div>
"""
    index_html += f"""  </div>
</div>
<script>
function setOfflineLang(lang) {{
  try {{ localStorage.setItem('mathedu_lang', lang); }} catch(e){{}}
  document.documentElement.lang = lang;
  document.querySelectorAll('[data-lang-btn]').forEach(function(b) {{
    if (b.getAttribute('data-lang-btn') === lang) b.classList.add('active');
    else b.classList.remove('active');
  }});
  var isEn = (lang === 'en');
  var elTitle = document.getElementById('txtTitle');
  var elLead = document.getElementById('txtLead');
  var elBannerTitle = document.getElementById('txtBannerTitle');
  var elBannerBody = document.getElementById('txtBannerBody');
  var elBack = document.getElementById('txtBackLink');
  if (elTitle) elTitle.textContent = isEn ? '📦 min7014 mathedu Standalone Offline Problem Archive' : '📦 min7014 mathedu 오프라인 전체 문제 보관함';
  if (elLead) elLead.textContent = isEn ? 'Collection of standalone, self-contained interactive math quizzes that run completely offline without internet.' : '인터넷 접속 없이 언제 어디서나 풀이할 수 있는 오프라인 독립 실행형 수학 퀴즈 모음입니다.';
  if (elBannerTitle) elBannerTitle.textContent = isEn ? '💡 About Offline Standalone Quizzes' : '💡 오프라인 단독 파일 안내';
  if (elBack) elBack.textContent = isEn ? 'Back to mathedu Main' : 'mathedu 메인으로';
  if (elBannerBody) {{
    elBannerBody.innerHTML = isEn ?
      '• Each problem is a <b>self-contained single-file HTML</b> bundle with embedded images and interactive step-by-step scoring.<br>' +
      '• Every quiz links back to its official online URL and Teacher Min Eun-gi’s mathematical research lab.<br>' +
      '• When connected to the internet, it <b>automatically detects online updates</b> with options to download the newest version or continue offline.<br>' +
      '• Total <b>{len(results)}</b> verified offline quizzes available.' :
      '• 각 문제 파일은 이미지와 인터랙티브 채점 로직이 포함된 <b>단일 HTML 파일</b>입니다.<br>' +
      '• 모든 문제에는 온라인 원본 주소(<code>https://min7014.github.io/mathedu/board/...</code>) 및 민은기 선생님 수학자료실 링크가 포함되어 있습니다.<br>' +
      '• 온라인 상태가 되면 <b>새로운 업데이트 버전이 있는지 자동 감지</b>하여 알림창을 통해 [새 버전 내려받기] 또는 [현재 버전 풀기]를 선택할 수 있습니다.<br>' +
      '• 총 <b>{len(results)}개</b>의 문제 파일이 준비되어 있습니다.';
  }}
  document.querySelectorAll('.btn-download-text').forEach(function(el) {{ el.textContent = isEn ? '📥 Download' : '📥 다운로드'; }});
  document.querySelectorAll('.btn-solve-text').forEach(function(el) {{ el.textContent = isEn ? 'Solve ➔' : '풀기 ➔'; }});
  document.querySelectorAll('.link-online-text').forEach(function(el) {{ el.textContent = isEn ? 'Online Original ➔' : '온라인 원본 링크 ➔'; }});
  document.querySelectorAll('.txt-slug-prefix').forEach(function(el) {{ el.textContent = isEn ? 'Slug: ' : '고유 슬러그: '; }});
}}
var curLang = 'ko';
try {{ curLang = localStorage.getItem('mathedu_lang') || 'ko'; }} catch(e){{}}
var p = new URLSearchParams(window.location.search);
if (p.get('lang') === 'en' || p.get('lang') === 'ko') curLang = p.get('lang');
setOfflineLang(curLang);
</script>
</body>
</html>
"""
    with open(os.path.join(OFFLINE_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)

    print(f"✅ 총 {len(results)}개 문제의 오프라인 HTML 파일, offline/versions.json 및 offline/index.html 빌드 완료!")

if __name__ == '__main__':
    main()
