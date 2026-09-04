// Keep the canonical homepage URL clean and refresh cached homepage styles after launch.
(function normalizeHomepageUrlAndAssets() {
  const { hostname, pathname, search, hash } = window.location;
  const isSilwadiDomain = hostname === 'silwadi.ae' || hostname === 'www.silwadi.ae';

  if (isSilwadiDomain && /\/index\.html$/.test(pathname)) {
    window.location.replace(`https://silwadi.ae/${search}${hash}`);
    return;
  }

  if (isSilwadiDomain && pathname === '/') {
    const homepageStyles = new Set(['styles.css', 'home-trust.css', 'home-reviews.css']);
    document.querySelectorAll('link[rel="stylesheet"]').forEach(link => {
      const href = link.getAttribute('href') || '';
      if (homepageStyles.has(href)) link.setAttribute('href', `${href}?v=20260905-live2`);
    });
  }
})();

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

// Keep phone and email links easy to scan without replacing their visible labels.
function enhanceContactLinks() {
  const phoneIcon = '<svg class="contact-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M7.2 2.5h3.1l1.1 5.1-2.1 1.7a14.8 14.8 0 0 0 5.4 5.4l1.7-2.1 5.1 1.1v3.1c0 1.1-.9 2-2 2C11.4 18.8 5.2 12.6 5.2 4.5c0-1.1.9-2 2-2Z"/></svg>';
  const emailIcon = '<svg class="contact-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M3 5h18v14H3V5Zm2 2v.7l7 4.6 7-4.6V7l-7 4.6L5 7Z"/></svg>';
  document.querySelectorAll('a[href^="tel:"], a[href^="mailto:"]').forEach(link => {
    if (link.querySelector('.contact-icon')) return;
    link.classList.add('footer-contact-link');
    link.insertAdjacentHTML('afterbegin', link.matches('a[href^="tel:"]') ? phoneIcon : emailIcon);
  });
}

enhanceContactLinks();

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

// Keep the unfiltered directory aligned with the clinic's requested featured order.
const preferredDoctorOrder = [
  'Dr. Munir Silwadi',
  'Dr. Moheb Silwadi',
  'Dr. Ahmed El Shehri',
  'Dr. Hani Hasbini',
  'Dr. Dana Awad',
  'Dr. Afnan Mashal',
];
const doctorGrid = document.querySelector('.doctor-directory-grid');
if (doctorGrid && doctorCards.length) {
  const orderIndex = name => {
    const index = preferredDoctorOrder.indexOf(name);
    return index === -1 ? preferredDoctorOrder.length : index;
  };
  doctorCards.sort((a, b) => {
    const positionDifference = orderIndex(a.dataset.name) - orderIndex(b.dataset.name);
    return positionDifference || (a.dataset.name || '').localeCompare(b.dataset.name || '');
  });
  doctorCards.forEach(card => doctorGrid.appendChild(card));
}

function filterDoctors() {
  if (!doctorCards.length) return;
  const query = (doctorSearch?.value || '').trim().toLowerCase();
  let visible = 0;

  doctorCards.forEach(card => {
    const name = (card.dataset.name || '').toLowerCase();
    const specialty = (card.dataset.specialty || '').toLowerCase();
    const arabicSearch = (card.dataset.arSearch || '').toLowerCase();
    const matchesText = !query || name.includes(query) || specialty.includes(query) || arabicSearch.includes(query);
    const matchesSpecialty = activeSpecialty === 'all' || specialty.includes(activeSpecialty);
    const show = matchesText && matchesSpecialty;
    card.hidden = !show;
    if (show) visible += 1;
  });

  if (doctorResults) {
    const unfiltered = !query && activeSpecialty === 'all';
    const language = window.SilwadiLanguage?.getLanguage?.() || 'en';
    const englishLabel = unfiltered ? `${visible} dentists & specialists` : `${visible} clinician${visible === 1 ? '' : 's'}`;
    doctorResults.textContent = window.SilwadiLanguage?.translate?.(englishLabel, language) || englishLabel;
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
document.addEventListener('silwadi:languagechange', filterDoctors);

// Prepare consultation requests in the visitor's email app for the appointments team.
document.querySelectorAll('[data-consultation-form]').forEach(form => {
  form.addEventListener('submit', event => {
    event.preventDefault();
    const data = new FormData(form);
    const name = String(data.get('name') || '').trim();
    const email = String(data.get('email') || '').trim();
    const phone = String(data.get('phone') || '').trim();
    const treatment = String(data.get('treatment') || '').trim();
    const date = String(data.get('date') || '').trim();
    const time = String(data.get('time') || '').trim();
    const clinic = String(data.get('clinic') || '').trim();
    const subject = treatment ? `Appointment request - ${treatment}` : 'Consultation request';
    const message = String(data.get('message') || '').trim();
    const body = [`Name: ${name}`, `Email: ${email}`, `Phone: ${phone}`, `Treatment: ${treatment || 'Not specified'}`, `Preferred date: ${date || 'Not specified'}`, `Preferred time: ${time || 'Not specified'}`, `Preferred clinic: ${clinic || 'Not specified'}`, '', `Notes: ${message || 'None'}`].join('\\n');
    window.location.href = `mailto:appointment@silwadidentalcenter.ae?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    const status = form.querySelector('[data-consultation-status]');
    if (status) {
      const language = window.SilwadiLanguage?.getLanguage?.() || 'en';
      const message = 'Your email app is opening with the appointment request.';
      status.textContent = window.SilwadiLanguage?.translate?.(message, language) || message;
    }
  });
});


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
  const target = nested ? '../contact.html#consultation-form' : 'contact.html#consultation-form';
  const languageApi = window.SilwadiLanguage;
  const activeLanguage = languageApi?.getRequestedLanguage?.() || languageApi?.getLanguage?.() || 'en';
  const localizedTarget = languageApi?.withLanguageQuery?.(target, activeLanguage) || target;
  document.querySelectorAll('a').forEach(link => {
    const text = (link.textContent || '').trim().toLowerCase();
    const href = link.getAttribute('href') || '';
    const primaryConsultation = text.includes('book a consultation') || text.includes('book a consultation with') || text.includes('احجز استشارة') || text === 'احجز';
    const consultationMail = href.startsWith('mailto:') && /consultation/i.test(href);
    if (primaryConsultation || consultationMail) link.setAttribute('href', localizedTarget);
  });
})();


// Expandable Google review dialog.
const reviewDialog = document.querySelector('[data-review-dialog]');
const reviewClose = document.querySelector('[data-review-close]');
const reviewTriggers = [...document.querySelectorAll('[data-review-expand]')];

function openReviewDialog(card) {
  if (!reviewDialog || !card) return;
  const name = card.querySelector('.google-review-card__top strong')?.textContent?.trim() || 'Patient review';
  const avatar = card.querySelector('.review-avatar')?.textContent?.trim() || '';
  const text = card.querySelector('p')?.textContent?.trim() || '';
  const stars = card.querySelector('.review-stars');
  const starText = stars?.textContent?.trim() || '★★★★★';
  const starLabel = stars?.getAttribute('aria-label') || '5 out of 5 stars';
  const dialogName = reviewDialog.querySelector('[data-review-name]');
  const dialogAvatar = reviewDialog.querySelector('[data-review-avatar]');
  const dialogText = reviewDialog.querySelector('[data-review-text]');
  const dialogStars = reviewDialog.querySelector('[data-review-stars]');
  if (dialogName) dialogName.textContent = name;
  if (dialogAvatar) dialogAvatar.textContent = avatar;
  if (dialogText) dialogText.textContent = text;
  if (dialogStars) {
    dialogStars.textContent = starText;
    dialogStars.setAttribute('aria-label', starLabel);
  }
  if (typeof reviewDialog.showModal === 'function') reviewDialog.showModal();
  else reviewDialog.setAttribute('open', '');
}

reviewTriggers.forEach(card => {
  card.addEventListener('click', () => openReviewDialog(card));
  card.addEventListener('keydown', event => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      openReviewDialog(card);
    }
  });
});

reviewClose?.addEventListener('click', () => reviewDialog?.close());
reviewDialog?.addEventListener('click', event => {
  if (event.target === reviewDialog) reviewDialog.close();
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && reviewDialog?.open) reviewDialog.close();
});

// Swap uploaded doctor portraits into the remaining placeholder frames.
(function replaceUploadedDoctorPortraits() {
  const portraits = {
    'Dr. Sara Ismail': 'dr-sara-ismail.webp',
    'Dr. Kashmira Pawar Jayprakash': 'dr-kashmira-pawar-jayprakash.webp',
    'Dr. Nachiket Shah': 'dr-nachiket-shah.webp',
  };
  const path = window.location.pathname || '';
  const nestedDoctorProfile = /\/doctors\/[^/]+\.html$/.test(path);
  const basePath = nestedDoctorProfile ? '../assets/doctors/optimized/' : 'assets/doctors/optimized/';

  Object.entries(portraits).forEach(([doctorName, fileName]) => {
    document.querySelectorAll(`[aria-label="${doctorName}"]`).forEach(frame => {
      const isDirectoryPhoto = frame.classList.contains('doctor-directory-card__photo');
      const isProfilePhoto = frame.classList.contains('consultant-portrait__frame');
      if (!isDirectoryPhoto && !isProfilePhoto) return;

      frame.classList.remove('doctor-directory-card__photo--placeholder', 'doctor-profile-placeholder');
      frame.removeAttribute('role');
      frame.innerHTML = '';

      const image = document.createElement('img');
      image.src = `${basePath}${fileName}?v=20260904-portraits`;
      image.alt = doctorName;
      image.width = isProfilePhoto ? 720 : 600;
      image.height = isProfilePhoto ? 720 : 600;
      image.decoding = 'async';
      if (isProfilePhoto) image.fetchPriority = 'high';
      else image.loading = 'lazy';

      frame.appendChild(image);
    });
  });
})();

window.SilwadiLanguage?.init?.();
