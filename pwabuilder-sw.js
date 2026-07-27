// This is the "Offline page" service worker

importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');

const CACHE = "pwabuilder-page";

self.addEventListener("message", (event) => {
    if (event.data && event.data.type === "SKIP_WAITING") {
        self.skipWaiting();
    }
});

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE)
            .then((cache) => {
                // cache.addAll(offlineFallbackPage);
            })
    );
});

if (workbox.navigationPreload.isSupported()) {
    workbox.navigationPreload.enable();
}

self.addEventListener('fetch', (event) => {
    if (event.request.mode === 'navigate') {
        event.respondWith((async () => {
            try {
                const preloadResp = await event.preloadResponse;
                if (preloadResp) {
                    return preloadResp;
                }

                const networkResp = await fetch(event.request);
                return networkResp;
            } catch (error) {
                const cache = await caches.open(CACHE);
                const cachedResp = await cache.match(event.request);
                return cachedResp;
            }
        })());
    }
});

// ==========================================
// Lógica para notificaciones push de alarma
// ==========================================

self.addEventListener('push', function(event) {
    const title = 'Recordatorio de Medicamentos';
    const options = {
        body: event.data ? event.data.text() : '¡Es hora de tomar tu medicina!',
        icon: '/static/icon.png',
        badge: '/static/badge.png',
        vibrate: [500, 200, 500, 200, 500, 200, 500],
        tag: 'alarma-medicamento',
        renotify: true,
        requireInteraction: true
    };

    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    event.waitUntil(
        clients.openWindow('/')
    );
});
