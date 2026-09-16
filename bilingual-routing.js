(function silwadiBilingualRouting() {
  const loadBookingModalAssets = () => {
    if (!document.querySelector('link[data-booking-modal-styles]')) {
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = '/booking-modal.css?v=20260914-success1';
      link.setAttribute('data-booking-modal-styles', '');
      document.head.appendChild(link);
    }
    if (!document.querySelector('script[data-booking-modal-script]')) {
      const script = document.createElement('script');
      script.src = '/booking-modal.js?v=20260914-success1';
      script.async = false;
      script.setAttribute('data-booking-modal-script', '');
      document.head.appendChild(script);
    }
    if (!document.querySelector('script[data-booking-email-validation]')) {
      const validator = document.createElement('script');
      validator.src = '/booking-email-validation.js?v=20260914-email1';
      validator.async = false;
      validator.setAttribute('data-booking-email-validation', '');
      document.head.appendChild(validator);
    }
  };

  const loadSpecializedCareNavStyles = () => {
    if (document.querySelector('link[data-specialized-care-nav-styles]')) return;
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = '/specialized-care-nav.css?v=20260916-live1';
    link.setAttribute('data-specialized-care-nav-styles', '');
    document.head.appendChild(link);
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

  const placePodPartnershipBeforeGallery = () => {
    const path = window.location.pathname || '';
    const isPodPage = /(?:\/ar)?\/treatments\/people-of-determination\.html$/.test(path)
      || path.endsWith('/review/people-of-determination-raha-v1.html');
    if (!isPodPage) return;

    const partnership = document.querySelector('.pod-partnership');
    const gallery = document.querySelector('.pod-hero__gallery');
    if (!partnership || !gallery) return;

    partnership.insertAdjacentElement('afterend', gallery);
  };

  const isArabicUi = () => {
    const apiLanguage = window.SilwadiLanguage?.getLanguage?.();
    return apiLanguage === 'ar'
      || document.documentElement.lang?.toLowerCase().startsWith('ar')
      || document.documentElement.dir === 'rtl'
      || document.body?.classList.contains('language-ar')
      || window.location.pathname.startsWith('/ar/');
  };

  const removePediatricFromServicesMenus = () => {
    document.querySelectorAll('.services-mega__grid a, .mobile-services__links a').forEach(link => {
      const href = (link.getAttribute('href') || '').toLowerCase();
      const label = (link.textContent || '').trim().toLowerCase();
      const isPediatric = href.includes('pediatric-dentistry')
        || href.includes('#pedodontics')
        || label.includes('pedodontics')
        || label.includes('طب أسنان الأطفال')
        || label.includes('أسنان الأطفال');
      if (isPediatric) link.remove();
    });
  };

  const specializedCareCopy = arabic => arabic ? {
    trigger: 'الرعاية المتخصصة',
    eyebrow: 'مسارات رعاية مخصصة',
    title: 'الرعاية المتخصصة',
    description: 'رعاية مخصصة تراعي احتياجات كل مريض وتفاصيل زيارته.',
    pediatricTitle: 'طب أسنان الأطفال',
    pediatricDescription: 'رعاية أسنان مخصصة للأطفال',
    pediatricCta: 'استكشف رعاية الأطفال ←',
    podTitle: 'أصحاب الهمم',
    podDescription: 'الراحة وسهولة الوصول والدعم المصمم لكل مريض',
    podCta: 'استكشف الرعاية المخصصة ←',
    aria: 'الرعاية المتخصصة'
  } : {
    trigger: 'Specialized Care',
    eyebrow: 'Focused care pathways',
    title: 'Specialized Care',
    description: 'Dedicated care experiences designed around specific patient needs.',
    pediatricTitle: 'Pediatric Dentistry',
    pediatricDescription: 'Dedicated dental care for children',
    pediatricCta: 'Explore pediatric care →',
    podTitle: 'People of Determination',
    podDescription: 'Comfort, accessibility & individualized support',
    podCta: 'Explore dedicated care →',
    aria: 'Specialized care'
  };

  const buildDesktopSpecializedCare = (arabic, copy) => {
    const wrapper = document.createElement('div');
    wrapper.className = 'nav-specialized';
    wrapper.setAttribute('data-specialized-care-nav', 'desktop');

    const pediatricHref = arabic
      ? '/ar/treatments/pediatric-dentistry.html'
      : '/treatments/pediatric-dentistry.html';
    const podHref = arabic
      ? '/ar/treatments/people-of-determination.html'
      : '/treatments/people-of-determination.html';

    wrapper.innerHTML = `
      <a class="nav-specialized__trigger" href="#" aria-haspopup="true" aria-expanded="false">
        ${copy.trigger} <span class="nav-specialized__chevron" aria-hidden="true">⌄</span>
      </a>
      <div class="specialized-care-menu" aria-label="${copy.aria}">
        <div class="specialized-care-menu__head">
          <div><span class="specialized-care-menu__eyebrow">${copy.eyebrow}</span><strong>${copy.title}</strong></div>
          <span>${copy.description}</span>
        </div>
        <div class="specialized-care-menu__grid">
          <a class="specialized-care-card" href="${pediatricHref}"><span class="specialized-care-card__index">01</span><strong>${copy.pediatricTitle}</strong><small>${copy.pediatricDescription}</small><b>${copy.pediatricCta}</b></a>
          <a class="specialized-care-card specialized-care-card--pod" href="${podHref}"><span class="specialized-care-card__index">02</span><strong>${copy.podTitle}</strong><small>${copy.podDescription}</small><b>${copy.podCta}</b></a>
        </div>
      </div>`;

    const trigger = wrapper.querySelector('.nav-specialized__trigger');
    trigger?.addEventListener('click', event => {
      event.preventDefault();
      const open = wrapper.classList.toggle('is-open');
      trigger.setAttribute('aria-expanded', String(open));
    });
    wrapper.addEventListener('mouseleave', () => {
      wrapper.classList.remove('is-open');
      trigger?.setAttribute('aria-expanded', 'false');
    });

    return wrapper;
  };

  const buildMobileSpecializedCare = (arabic, copy) => {
    const details = document.createElement('details');
    details.className = 'mobile-specialized-care';
    details.setAttribute('data-specialized-care-nav', 'mobile');

    const pediatricHref = arabic
      ? '/ar/treatments/pediatric-dentistry.html'
      : '/treatments/pediatric-dentistry.html';
    const podHref = arabic
      ? '/ar/treatments/people-of-determination.html'
      : '/treatments/people-of-determination.html';

    details.innerHTML = `
      <summary>${copy.trigger}</summary>
      <div class="mobile-specialized-care__links">
        <a href="${pediatricHref}"><strong>${copy.pediatricTitle}</strong><span>${copy.pediatricDescription}</span></a>
        <a href="${podHref}"><strong>${copy.podTitle}</strong><span>${copy.podDescription}</span></a>
      </div>`;
    return details;
  };

  const syncSpecializedCareNavigation = forcedArabic => {
    removePediatricFromServicesMenus();
    document.querySelectorAll('[data-specialized-care-nav]').forEach(node => node.remove());

    const arabic = typeof forcedArabic === 'boolean' ? forcedArabic : isArabicUi();
    const copy = specializedCareCopy(arabic);

    document.querySelectorAll('.site-nav, .global-nav').forEach(nav => {
      const serviceContainer = nav.querySelector('.nav-services');
      const directServiceLink = [...nav.children].find(child => {
        if (!(child instanceof HTMLAnchorElement)) return false;
        return (child.getAttribute('href') || '').includes('services');
      });
      const anchor = serviceContainer || directServiceLink;
      if (!anchor) return;
      anchor.insertAdjacentElement('afterend', buildDesktopSpecializedCare(arabic, copy));
    });

    document.querySelectorAll('.mobile-nav__panel, .global-mobile-nav__inner').forEach(nav => {
      const serviceDetails = nav.querySelector('.mobile-services');
      const directServiceLink = [...nav.children].find(child => {
        if (!(child instanceof HTMLAnchorElement)) return false;
        return (child.getAttribute('href') || '').includes('services');
      });
      const anchor = serviceDetails || directServiceLink;
      if (!anchor) return;
      anchor.insertAdjacentElement('afterend', buildMobileSpecializedCare(arabic, copy));
    });
  };

  loadBookingModalAssets();
  loadSpecializedCareNavStyles();

  const runReadyEnhancements = () => {
    syncFooterSocials();
    placePodPartnershipBeforeGallery();
    syncSpecializedCareNavigation();
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', runReadyEnhancements, { once: true });
  } else {
    runReadyEnhancements();
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
    syncSpecializedCareNavigation(next === 'ar');

    const target = next === 'ar'
      ? arabicPathFor(window.location.pathname)
      : englishPathFor(window.location.pathname);
    window.history.replaceState({}, '', `${target}${window.location.hash || ''}`);
  }, true);

  document.addEventListener('silwadi:languagechange', syncSpecializedCareNavigation);

  document.addEventListener('click', event => {
    document.querySelectorAll('.nav-specialized.is-open').forEach(menu => {
      if (menu.contains(event.target)) return;
      menu.classList.remove('is-open');
      menu.querySelector('.nav-specialized__trigger')?.setAttribute('aria-expanded', 'false');
    });
  });
})();