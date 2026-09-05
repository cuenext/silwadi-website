(function silwadiBilingualRouting() {
  const normalizeEnglishPath = pathname => {
    let path = pathname || '/';
    if (path.startsWith('/ar/')) path = path.slice(3) || '/';
    if (path === '/index.html') path = '/';
    return path;
  };

  const arabicPathFor = pathname => {
    const english = normalizeEnglishPath(pathname);
    return english === '/' ? '/ar/' : `/ar${english}`;
  };

  const englishPathFor = pathname => normalizeEnglishPath(pathname);
  const isStaticArabicPage = () => Boolean(document.body?.classList.contains('static-arabic'));

  const params = new URLSearchParams(window.location.search);
  let saved = null;
  try { saved = localStorage.getItem('silwadi-language'); } catch (_) {}

  if (params.get('lang') === 'en') {
    try { localStorage.setItem('silwadi-language', 'en'); } catch (_) {}
  } else if ((params.get('lang') === 'ar' || saved === 'ar') && !window.location.pathname.startsWith('/ar/')) {
    window.location.replace(`${arabicPathFor(window.location.pathname)}${window.location.hash || ''}`);
    return;
  }

  document.addEventListener('click', event => {
    const switcher = event.target.closest?.('[data-language-switch]');
    if (!switcher) return;

    // Static /ar/ pages have their own English switch. Do not interfere with it.
    if (window.location.pathname.startsWith('/ar/') && isStaticArabicPage()) return;

    const api = window.SilwadiLanguage;
    if (!api || typeof api.applyLanguage !== 'function') return;

    const current = api.getLanguage?.() || document.documentElement.lang || 'en';
    const next = current === 'ar' ? 'en' : 'ar';
    event.preventDefault();
    event.stopImmediatePropagation();

    try { localStorage.setItem('silwadi-language', next); } catch (_) {}

    // Translate the existing DOM in place. This intentionally preserves the
    // Google Reviews track element and its current animation position.
    api.applyLanguage(next);

    const target = next === 'ar'
      ? arabicPathFor(window.location.pathname)
      : englishPathFor(window.location.pathname);
    window.history.replaceState({}, '', `${target}${window.location.hash || ''}`);
  }, true);
})();
