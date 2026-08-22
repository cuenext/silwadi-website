const header = document.getElementById('siteHeader');
const menuButton = document.querySelector('[data-menu-button]');
const mobileNav = document.querySelector('[data-mobile-nav]');

if (header) {
  let headerFramePending = false;
  const syncHeaderState = () => {
    header.classList.toggle('scrolled', window.scrollY > 12);
    headerFramePending = false;
  };
  window.addEventListener('scroll', () => {
    if (headerFramePending) return;
    headerFramePending = true;
    requestAnimationFrame(syncHeaderState);
  }, { passive: true });
  syncHeaderState();
}

function closeMenu() {
  if (!menuButton || !mobileNav) return;
  mobileNav.classList.remove('open');
  document.body.classList.remove('menu-open');
  menuButton.setAttribute('aria-expanded', 'false');
}

if (menuButton && mobileNav) {
  menuButton.addEventListener('click', () => {
    const open = !mobileNav.classList.contains('open');
    mobileNav.classList.toggle('open', open);
    document.body.classList.toggle('menu-open', open);
    menuButton.setAttribute('aria-expanded', String(open));
  });
  mobileNav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
}

document.addEventListener('keydown', event => {
  if (event.key === 'Escape') closeMenu();
});

const reveals = document.querySelectorAll('.reveal');
const reduceMotion = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false;
if (reduceMotion || !('IntersectionObserver' in window)) {
  reveals.forEach(item => item.classList.add('visible'));
} else {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });
  reveals.forEach(item => observer.observe(item));
}


// Doctor directory search and specialty filtering.
const doctorSearch = document.querySelector('[data-doctor-search]');
const specialtyFilters = [...document.querySelectorAll('[data-specialty-filter]')];
const doctorCards = [...document.querySelectorAll('[data-doctor-card]')];
const doctorResults = document.querySelector('[data-doctor-results]');
const doctorEmpty = document.querySelector('[data-doctor-empty]');
let activeSpecialty = 'all';

function filterDoctors() {
  if (!doctorCards.length) return;
  const query = (doctorSearch?.value || '').trim().toLowerCase();
  let visible = 0;

  doctorCards.forEach(card => {
    const name = (card.dataset.name || '').toLowerCase();
    const specialty = (card.dataset.specialty || '').toLowerCase();
    const matchesText = !query || name.includes(query) || specialty.includes(query);
    const matchesSpecialty = activeSpecialty === 'all' || specialty.includes(activeSpecialty);
    const show = matchesText && matchesSpecialty;
    card.hidden = !show;
    if (show) visible += 1;
  });

  if (doctorResults) {
    const unfiltered = !query && activeSpecialty === 'all';
    doctorResults.textContent = unfiltered ? `${visible} dentists & specialists` : `${visible} clinician${visible === 1 ? '' : 's'}`;
  }
  if (doctorEmpty) doctorEmpty.hidden = visible !== 0;
}

if (doctorSearch) doctorSearch.addEventListener('input', filterDoctors);
specialtyFilters.forEach(button => {
  button.addEventListener('click', () => {
    activeSpecialty = button.dataset.specialtyFilter || 'all';
    specialtyFilters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    filterDoctors();
  });
});
filterDoctors();


// Shared FAQ accordion behavior.
document.querySelectorAll('[data-faq-button]').forEach(button => {
  button.addEventListener('click', () => {
    const item = button.closest('[data-faq-item]');
    if (!item) return;
    const open = item.classList.toggle('is-open');
    button.setAttribute('aria-expanded', String(open));
  });
});

// Route primary consultation CTAs through the dedicated contact destination.
(function routeConsultationCtas() {
  const path = window.location.pathname || '';
  if (path.endsWith('/contact.html') || path.endsWith('contact.html')) return;
  const nested = /\/(doctors|treatments)\/[^/]+\.html$/.test(path);
  const target = nested ? '../contact.html#consultation' : 'contact.html#consultation';
  document.querySelectorAll('a').forEach(link => {
    const text = (link.textContent || '').trim().toLowerCase();
    const href = link.getAttribute('href') || '';
    const primaryConsultation = text.includes('book a consultation') || text.includes('book a consultation with');
    const consultationMail = href.startsWith('mailto:') && /consultation/i.test(href);
    if (primaryConsultation || consultationMail) link.setAttribute('href', target);
  });
})();
