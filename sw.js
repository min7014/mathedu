/*!
 * sw.js — mathedu & 수학의 성전 3D Official Service Worker (PWA & Google Play TWA)
 * Network-first for HTML/JS/JSON so error-report fixes & live updates reflect immediately,
 * with full offline fallback and 100/100 PWABuilder compliance.
 */
const CACHE_NAME = 'mathedu-play-v20261114-r2';
const CORE_ASSETS = [
  './',
  './index.html',
  './video_board.html',
  './mathlab.html',
  './game.html',
  './privacy.html',
  './manifest.json',
  './mathedu-auth.js',
  './mathedu-gamification.js',
  './mathedu-quest-game.js',
  './mathedu-i18n.js',
  './mathedu-report.js',
  './mathedu-room.js',
  './assets/app_icon_192.png',
  './assets/app_icon_512.png',
  './assets/favicon.png',
  './assets/apple-touch-icon.png',
  './assets/logo_original.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(CORE_ASSETS).catch(() => {});
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.map((k) => {
          if (k !== CACHE_NAME) return caches.delete(k);
        })
      )
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return;

  const isDynamicAsset =
    event.request.mode === 'navigate' ||
    (event.request.headers.get('accept') || '').includes('text/html') ||
    /\.(html|js|json|css)$/i.test(url.pathname);

  // Network-first for HTML/JS/JSON/CSS so homepage updates & bug fixes appear immediately
  if (isDynamicAsset) {
    event.respondWith(
      fetch(event.request)
        .then((resp) => {
          if (resp && resp.status === 200) {
            const copy = resp.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy)).catch(() => {});
          }
          return resp;
        })
        .catch(() =>
          caches.match(event.request).then((r) =>
            r || (event.request.mode === 'navigate' ? (caches.match('./index.html') || caches.match('./game.html')) : undefined)
          )
        )
    );
    return;
  }

  event.respondWith(
    caches.match(event.request).then((cached) => {
      const fetchPromise = fetch(event.request)
        .then((networkResp) => {
          if (networkResp && networkResp.status === 200) {
            const copy = networkResp.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy)).catch(() => {});
          }
          return networkResp;
        })
        .catch(() => cached);
      return cached || fetchPromise;
    })
  );
});
