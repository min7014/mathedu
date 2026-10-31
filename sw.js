/*!
 * sw.js — mathedu & 수학의 성전 3D Official Service Worker (PWA & Google Play TWA)
 * Enables offline fallback, fast shell caching, and 100/100 PWABuilder / Google Play compliance.
 */
const CACHE_NAME = 'mathedu-play-v20261101';
const CORE_ASSETS = [
  './',
  './index.html',
  './game.html',
  './play.html',
  './privacy.html',
  './manifest.json',
  './mathedu-auth.js',
  './mathedu-gamification.js',
  './mathedu-quest-game.js',
  './mathedu-i18n.js',
  './mathedu-report.js',
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

  // Network-first for HTML navigation, Stale-While-Revalidate for static assets
  if (event.request.mode === 'navigate' || (event.request.headers.get('accept') || '').includes('text/html')) {
    event.respondWith(
      fetch(event.request)
        .then((resp) => {
          const copy = resp.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy)).catch(() => {});
          return resp;
        })
        .catch(() => caches.match(event.request).then((r) => r || caches.match('./game.html') || caches.match('./index.html')))
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
