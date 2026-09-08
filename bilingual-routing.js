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

  const syncFooterSocials = () => {
    const instagram = document.querySelector('a.footer-social-link[href*="instagram.com"]');
    if (!instagram) return;

    instagram.href = 'https://www.instagram.com/silwadi.ae/';
    instagram.setAttribute('aria-label', 'Follow Silwadi Dental Center on Instagram');
    instagram.setAttribute('data-social', 'instagram');
    const instagramLabel = instagram.querySelector('span');
    if (instagramLabel) instagramLabel.innerHTML = 'Instagram <strong>@silwadi.ae</strong>';

    let tiktok = document.querySelector('a.footer-social-link[data-social="tiktok"]');
    if (!tiktok) {
      tiktok = instagram.cloneNode(true);
      tiktok.setAttribute('data-social', 'tiktok');
      tiktok.style.marginInlineStart = '8px';
      instagram.insertAdjacentElement('afterend', tiktok);
    }

    tiktok.href = 'https://www.tiktok.com/@silwadi.ae';
    tiktok.setAttribute('aria-label', 'Follow Silwadi Dental Center on TikTok');
    const tiktokLabel = tiktok.querySelector('span');
    if (tiktokLabel) tiktokLabel.innerHTML = 'TikTok <strong>@silwadi.ae</strong>';
    const tiktokIcon = tiktok.querySelector('svg');
    if (tiktokIcon) {
      tiktokIcon.setAttribute('viewBox', '0 0 24 24');
      tiktokIcon.innerHTML = '<path fill="currentColor" d="M14 3v10.8a4.4 4.4 0 1 1-2-3.95V6.2l7-1.55V8l-5 1.1V3Z"/>';
    }
  };

  loadBookingModalAssets();

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', syncFooterSocials, { once: true });
  } else {
    syncFooterSocials();
  }

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
    syncFooterSocials();

    const target = next === 'ar'
      ? arabicPathFor(window.location.pathname)
      : englishPathFor(window.location.pathname);
    window.history.replaceState({}, '', `${target}${window.location.hash || ''}`);
  }, true);
})();
