(function silwadiBilingualRouting() {
  const loadBookingModalAssets = () => {
    if (!document.querySelector('link[data-booking-modal-styles]')) {
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = '/booking-modal.css?v=20260905-1';
      link.setAttribute('data-booking-modal-styles', '');
      document.head.appendChild(link);
    }
    if (!document.querySelector('script[data-booking-modal-script]')) {
      const script = document.createElement('script');
      script.src = '/booking-modal.js?v=20260905-1';
      script.async = false;
      script.setAttribute('data-booking-modal-script', '');
      document.head.appendChild(script);
    }
  };

  loadBookingModalAssets();

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

// Use the exact uploaded Dr. Fahed portrait that is already proven to load on Pages.
(function preloadFahedPortrait() {
  const path = window.location.pathname || '';
  const isFahedRelevantPage = /(?:^|\/)(?:ar\/)?doctors(?:\.html|\/dr-fahed-khalil\.html)$/.test(path);
  if (!isFahedRelevantPage) return;

  const fahedSrc = '/assets/CA01DF50-0B4F-4C3B-91B7-B13D4417FFC4.png?v=20260907-fahed-proven1';
  const preload = document.createElement('link');
  preload.rel = 'preload';
  preload.as = 'image';
  preload.href = fahedSrc;
  preload.type = 'image/png';
  document.head.appendChild(preload);

  const applyFahedPortrait = () => {
    document.querySelectorAll('img[alt="Dr. Fahed Abi Khalil"], img[alt="د. فهد أبي خليل"]').forEach(image => {
      if (image.getAttribute('src') !== fahedSrc) image.setAttribute('src', fahedSrc);
      image.decoding = 'async';
      if (path.includes('dr-fahed-khalil.html')) {
        image.loading = 'eager';
        image.fetchPriority = 'high';
      }
    });
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', applyFahedPortrait, { once: true });
  else applyFahedPortrait();
})();
