(function silwadiBilingualRouting() {
  const arabicPathFor = pathname => {
    let path = pathname || '/';
    if (path === '/index.html') path = '/';
    if (path.startsWith('/ar/')) return path;
    return path === '/' ? '/ar/' : `/ar${path}`;
  };

  const params = new URLSearchParams(window.location.search);
  let saved = null;
  try { saved = localStorage.getItem('silwadi-language'); } catch (_) {}

  if (params.get('lang') === 'en') {
    try { localStorage.setItem('silwadi-language', 'en'); } catch (_) {}
  } else if (params.get('lang') === 'ar' || saved === 'ar') {
    const target = arabicPathFor(window.location.pathname);
    if (!window.location.pathname.startsWith('/ar/')) {
      window.location.replace(`${target}${window.location.hash || ''}`);
      return;
    }
  }

  document.addEventListener('click', event => {
    const switcher = event.target.closest?.('[data-language-switch]');
    if (!switcher) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    try { localStorage.setItem('silwadi-language', 'ar'); } catch (_) {}
    const target = arabicPathFor(window.location.pathname);
    window.location.assign(`${target}${window.location.hash || ''}`);
  }, true);
})();
