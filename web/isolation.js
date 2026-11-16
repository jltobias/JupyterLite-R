/* Original GitHub Pages bootstrap. Local preview supplies headers directly. */
(async () => {
  if (window.crossOriginIsolated) return;
  if (!('serviceWorker' in navigator)) {
    console.error('JupyterLite-R needs service worker support or a host serving COOP/COEP headers.');
    return;
  }
  try {
    await navigator.serviceWorker.register('./isolation-sw.js', {scope:'./'});
    const reload = () => {
      const worker = navigator.serviceWorker.controller;
      if (worker && worker.scriptURL.endsWith('/isolation-sw.js') && !sessionStorage.getItem('jlr-isolation-reload')) {
        sessionStorage.setItem('jlr-isolation-reload','1');
        location.reload();
      }
    };
    navigator.serviceWorker.addEventListener('controllerchange', reload);
    reload();
  } catch (error) { console.error('Isolation setup failed:', error); }
})();
