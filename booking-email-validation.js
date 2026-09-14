(function silwadiBookingEmailValidation() {
  const copyForCurrentLanguage = () => {
    const isArabic = (document.documentElement.lang || '').toLowerCase().startsWith('ar') ||
      document.documentElement.dir === 'rtl' ||
      window.location.pathname.startsWith('/ar/');

    return isArabic
      ? 'يرجى إدخال بريد إلكتروني صالح.'
      : 'Please enter a valid email address.';
  };

  const isValidEmailAddress = value => {
    const email = String(value || '').trim();
    return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email);
  };

  document.addEventListener('submit', event => {
    const form = event.target?.closest?.('[data-booking-form]');
    if (!form) return;

    const emailInput = form.querySelector('input[name="email"]');
    if (!emailInput) return;

    emailInput.setCustomValidity('');
    if (isValidEmailAddress(emailInput.value)) return;

    event.preventDefault();
    event.stopImmediatePropagation();

    const message = copyForCurrentLanguage();
    emailInput.setCustomValidity(message);
    const status = form.querySelector('[data-consultation-status]');
    if (status) status.textContent = message;
    emailInput.reportValidity();
    emailInput.focus({ preventScroll: true });
  }, true);

  document.addEventListener('input', event => {
    const emailInput = event.target?.closest?.('[data-booking-form] input[name="email"]');
    if (!emailInput) return;
    emailInput.setCustomValidity('');

    const form = emailInput.closest('[data-booking-form]');
    const status = form?.querySelector('[data-consultation-status]');
    if (status && (status.textContent === 'Please enter a valid email address.' || status.textContent === 'يرجى إدخال بريد إلكتروني صالح.')) {
      status.textContent = '';
    }
  }, true);
})();
