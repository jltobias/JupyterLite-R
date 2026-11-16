/* Original isolation worker, scoped only to lite/lab/. No third-party source copied.
   JupyterLite's root worker remains available for file synchronization. */
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', event => event.waitUntil(self.clients.claim()));
self.addEventListener('fetch', event => {
  if (event.request.cache === 'only-if-cached' && event.request.mode !== 'same-origin') return;
  event.respondWith((async () => {
    const response = await fetch(event.request);
    if (response.type === 'opaque' || response.status === 0) return response;
    const headers = new Headers(response.headers);
    headers.set('Cross-Origin-Opener-Policy', 'same-origin');
    headers.set('Cross-Origin-Embedder-Policy', 'require-corp');
    return new Response(response.body, {status:response.status,statusText:response.statusText,headers});
  })());
});
