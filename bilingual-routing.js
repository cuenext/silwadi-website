(function silwadiBilingualRouting() {
  const arabicPathFor = pathname => {
    let path = pathname || '/';
    if (path === '/index.html') path = '/';
    if (path.startsWith('/ar/')) return path;
    return path === '/' ? '/ar/' : `/ar${path}`;
  };

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
