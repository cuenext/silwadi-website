(function silwadiDirectBookingSubmit() {
  const FORM_ENDPOINT = 'https://formsubmit.co/ajax/appointment@silwadidentalcenter.ae';

  const copy = {
    en: {
      privacy: 'Your details are submitted to our appointments team and used only to respond to this enquiry. Please do not include sensitive medical information.',
      sending: 'Sending your appointment request…',
      success: 'Appointment request sent ✓ Our team will contact you to confirm availability.',
      error: 'We could not send your request right now. Please try again or contact reception by phone or WhatsApp.',
      intro: 'Your request will be sent to the appointments team. They will confirm availability and guide you to the right clinician.',
    },
    ar: {
      privacy: 'تُرسل بياناتك إلى فريق المواعيد وتُستخدم فقط للرد على هذا الطلب. يرجى عدم إدخال معلومات طبية حساسة.',
      sending: 'جارٍ إرسال طلب الموعد…',
      success: 'تم إرسال طلب الموعد ✓ سيتواصل معك فريقنا لتأكيد التوافر.',
      error: 'تعذر إرسال طلبك الآن. يرجى المحاولة مرة أخرى أو التواصل مع الاستقبال عبر الهاتف أو واتساب.',
      intro: 'سيتم إرسال طلبك إلى فريق المواعيد لتأكيد التوافر وتوجيهك إلى الطبيب المناسب.',
    },
  };

  const languageFor = form => {
    const htmlLang = (document.documentElement.lang || '').toLowerCase();
    return form?.closest('[dir="rtl"]') || htmlLang.startsWith('ar') || window.location.pathname.startsWith('/ar/') ? 'ar' : 'en';
  };

  const refreshVisibleCopy = () => {
    document.querySelectorAll('p').forEach(node => {
      const text = (node.textContent || '').trim();
      if (text === 'Your email app will open with the details you enter. We use them only to respond to this appointment enquiry. Please do not include sensitive medical information.' ||
          text === 'Your email app will open with the details you enter. We use them only to respond to this appointment enquiry. Please do not include sensitive medical information in the form.') {
        node.textContent = copy.en.privacy;
      } else if (text === 'Your request will open in your email app addressed to the appointments team. They will confirm availability and guide you to the right clinician.') {
        node.textContent = copy.en.intro;
      } else if (text === 'سيفتح تطبيق البريد الإلكتروني بالتفاصيل التي تدخلها. نستخدم هذه المعلومات فقط للرد على طلب الموعد. يرجى عدم إدخال معلومات طبية حساسة هنا.') {
        node.textContent = copy.ar.privacy;
      } else if (text === 'سيتم الآن فتح تطبيق البريد الإلكتروني مع تفاصيل طلب الموعد.') {
        node.textContent = '';
      }
    });
  };

  const observer = new MutationObserver(refreshVisibleCopy);
  observer.observe(document.documentElement, { childList: true, subtree: true });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', refreshVisibleCopy, { once: true });
  else refreshVisibleCopy();

  document.addEventListener('submit', async event => {
    const form = event.target?.closest?.('[data-consultation-form]');
    if (!form) return;

    event.preventDefault();
    event.stopImmediatePropagation();
    if (!form.reportValidity()) return;

    const data = new FormData(form);
    const language = languageFor(form);
    const strings = copy[language];
    const treatment = String(data.get('treatment') || '').trim();
    const email = String(data.get('email') || '').trim();
    const payload = {
      name: String(data.get('name') || '').trim(),
      email,
      phone: String(data.get('phone') || '').trim(),
      treatment: treatment || 'Not specified',
      preferred_date: String(data.get('date') || '').trim() || 'Not specified',
      preferred_time: String(data.get('time') || '').trim() || 'Not specified',
      preferred_clinic: String(data.get('clinic') || '').trim() || 'Not specified',
      notes: String(data.get('message') || '').trim() || 'None',
      language,
      _subject: treatment ? `Website appointment request - ${treatment}` : 'Website appointment request',
      _template: 'table',
      _captcha: 'false',
      _replyto: email,
      _honey: String(data.get('website') || '').trim(),
      _url: window.location.href,
    };

    const status = form.querySelector('[data-consultation-status]');
    const submit = form.querySelector('button[type="submit"]');
    if (status) status.textContent = strings.sending;
    if (submit) submit.disabled = true;

    try {
      const response = await fetch(FORM_ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify(payload),
      });
      const result = await response.json().catch(() => ({}));
      const rejected = result.success === false || result.success === 'false';
      if (!response.ok || rejected) throw new Error('booking_submit_failed');
      form.reset();
      if (status) status.textContent = strings.success;
    } catch (_) {
      if (status) status.textContent = strings.error;
    } finally {
      if (submit) submit.disabled = false;
    }
  }, true);
})();
