(function silwadiStaticArabic() {
  const dynamic = {
    'Your email app is opening with the appointment request.': 'سيُفتح تطبيق البريد لإرسال طلب الموعد.',
    'Patient review': 'تقييم مريض',
    '5 out of 5 stars': '5 من 5 نجوم'
  };

  const normalize = value => String(value ?? '').replace(/\s+/g, ' ').trim();
  const englishPathFor = pathname => {
    let path = pathname || '/ar/';
    path = path.replace(/^\/ar(?=\/|$)/, '') || '/';
    if (path === '/index.html') path = '/';
    return path;
  };

  window.SilwadiLanguage = {
    getLanguage: () => 'ar',
    getRequestedLanguage: () => 'ar',
    translate(value, language = 'ar') {
      const clean = normalize(value);
      if (language !== 'ar') return clean;
      if (dynamic[clean]) return dynamic[clean];
      const count = clean.match(/^(\d+) dentists & specialists$/);
      if (count) return `${count[1]} طبيباً واختصاصياً`;
      const clinicians = clean.match(/^(\d+) clinicians?$/);
      if (clinicians) return `${clinicians[1]} من أفراد الفريق الطبي`;
      return clean;
    },
    withLanguageQuery(href) { return href; },
    init() { return 'ar'; }
  };

  const installSwitch = () => {
    const headerActions = document.querySelector('.header-actions');
    if (!headerActions || headerActions.querySelector('[data-language-switch]')) return;
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'language-switch';
    button.setAttribute('data-language-switch', '');
    button.setAttribute('aria-label', 'التبديل إلى الإنجليزية');
    button.textContent = 'English';
    button.addEventListener('click', () => {
      try { localStorage.setItem('silwadi-language', 'en'); } catch (_) {}
      window.location.assign(`${englishPathFor(window.location.pathname)}${window.location.hash || ''}`);
    });
    headerActions.prepend(button);
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', installSwitch, { once: true });
  else installSwitch();
})();
