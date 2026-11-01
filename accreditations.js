(function () {
  const track = document.getElementById('accTrack');
  const previous = document.getElementById('accPrev');
  const next = document.getElementById('accNext');
  const dots = document.getElementById('accDots');

  if (!track || !previous || !next || !dots) return;

  const cards = [...track.querySelectorAll('.acc-card')];
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const isArabic = document.documentElement.lang.toLowerCase().startsWith('ar');
  let positions = [];

  function scrollBehavior() {
    return prefersReducedMotion.matches ? 'auto' : 'smooth';
  }

  function step() {
    if (!cards.length) return 0;
    const gap = parseFloat(getComputedStyle(track).gap) || 0;
    return cards[0].getBoundingClientRect().width + gap;
  }

  function currentIndex() {
    if (!positions.length) return 0;
    let best = 0;
    let distance = Infinity;

    positions.forEach((position, index) => {
      const candidateDistance = Math.abs(track.scrollLeft - position);
      if (candidateDistance < distance) {
        distance = candidateDistance;
        best = index;
      }
    });

    return best;
  }

  function update() {
    const index = currentIndex();
    [...dots.children].forEach((dot, dotIndex) => {
      dot.classList.toggle('is-active', dotIndex === index);
      dot.setAttribute('aria-current', dotIndex === index ? 'true' : 'false');
    });
    previous.setAttribute('aria-disabled', index === 0 ? 'true' : 'false');
    next.setAttribute('aria-disabled', index === positions.length - 1 ? 'true' : 'false');
  }

  function renderDots() {
    const existingDots = [...dots.children];
    if (existingDots.length === positions.length) return;

    const focusedIndex = existingDots.indexOf(document.activeElement);
    dots.replaceChildren();

    positions.forEach((_, index) => {
      const dot = document.createElement('button');
      dot.type = 'button';
      dot.className = 'acc-dot';
      dot.setAttribute(
        'aria-label',
        isArabic
          ? `الانتقال إلى الاعتماد رقم ${index + 1}`
          : `Go to accreditation slide ${index + 1}`,
      );
      dot.addEventListener('click', () => {
        track.scrollTo({ left: positions[index], behavior: scrollBehavior() });
      });
      dots.appendChild(dot);
    });

    if (focusedIndex >= 0) {
      dots.children[Math.min(focusedIndex, dots.children.length - 1)]?.focus();
    }
  }

  function rebuild() {
    const cardStep = step();
    const maximum = Math.max(0, track.scrollWidth - track.clientWidth);
    const count = maximum < 8 || cardStep <= 0
      ? 1
      : Math.round(maximum / cardStep) + 1;
    positions = Array.from(
      { length: count },
      (_, index) => index === count - 1 ? maximum : Math.min(index * cardStep, maximum),
    );

    renderDots();
    update();
  }

  previous.addEventListener('click', () => {
    if (previous.getAttribute('aria-disabled') === 'true') return;
    const index = currentIndex();
    track.scrollTo({
      left: positions[Math.max(0, index - 1)] || 0,
      behavior: scrollBehavior(),
    });
  });

  next.addEventListener('click', () => {
    if (next.getAttribute('aria-disabled') === 'true') return;
    const index = currentIndex();
    track.scrollTo({
      left: positions[Math.min(positions.length - 1, index + 1)] || 0,
      behavior: scrollBehavior(),
    });
  });

  track.addEventListener('scroll', () => requestAnimationFrame(update), { passive: true });
  window.addEventListener('resize', () => requestAnimationFrame(rebuild));

  rebuild();
}());
