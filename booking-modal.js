(function silwadiBookingModal() {
  const BOOKING_ENDPOINT = 'https://booking.silwadi.ae/booking-submit.php';

  const EN = {
    title: 'Book your appointment',
    intro: 'Share a few details and our appointments team will confirm availability with you.',
    close: 'Close booking form',
    privacy: 'Your details are sent securely to our appointments team and used only to respond to this enquiry. Please do not include sensitive medical information.',
    name: 'Full name',
    mobile: 'Mobile',
    email: 'Email',
    treatment: 'Treatment',
    date: 'Preferred appointment date',
    time: 'Preferred appointment time',
    clinic: 'Preferred clinic',
    notes: 'Notes / other queries',
    choose: 'Please choose',
    consent: 'I agree that Silwadi may use these details to reply to my appointment enquiry.',
    submit: 'Send appointment request',
    sending: 'Sending your appointment request…',
    successTitle: 'Appointment request sent',
    successBody: 'Our appointments team will contact you to confirm availability.',
    done: 'Done',
    error: 'We could not send your request right now. Please try again or contact reception by phone or WhatsApp.',
    treatments: [
      ['General Dentistry', 'General Dentistry'],
      ['Preventive Dentistry', 'Preventive Dentistry'],
      ['Prosthodontics', 'Prosthodontics'],
      ['Cosmetic Dentistry', 'Cosmetic Dentistry'],
      ['Dental Implants', 'Dental Implants'],
      ['Orthodontics', 'Orthodontics'],
      ['Periodontics', 'Periodontics'],
      ['Endodontics', 'Endodontics'],
      ['Paediatric Dentistry', 'Paediatric Dentistry'],
      ['Other / Not sure', 'Other / Not sure'],
    ],
    clinics: [
      ['Bani Yas Tower - Corniche Street', 'Bani Yas Tower - Corniche Street'],
      ['Al Raha Mall', 'Al Raha Mall'],
    ],
  };

  const AR = {
    title: 'احجز موعدك',
    intro: 'شاركنا بعض التفاصيل وسيتواصل معك فريق المواعيد لتأكيد الوقت المناسب.',
    close: 'إغلاق نموذج الحجز',
    privacy: 'تُرسل بياناتك مباشرة وبشكل آمن إلى فريق المواعيد ونستخدمها فقط للرد على طلبك. يرجى عدم إدخال معلومات طبية حساسة هنا.',
    name: 'الاسم الكامل',
    mobile: 'رقم الهاتف',
    email: 'البريد الإلكتروني',
    treatment: 'العلاج',
    date: 'التاريخ المفضل للموعد',
    time: 'الوقت المفضل للموعد',
    clinic: 'الفرع المفضل',
    notes: 'ملاحظات أو استفسارات أخرى',
    choose: 'يرجى الاختيار',
    consent: 'أوافق على استخدام مركز سلوادي لهذه البيانات للرد على طلب الموعد.',
    submit: 'أرسل طلب الموعد',
    sending: 'جارٍ إرسال طلب الموعد…',
    successTitle: 'تم إرسال طلب الموعد',
    successBody: 'سيتواصل معك فريق المواعيد لتأكيد التوافر.',
    done: 'تم',
    error: 'تعذر إرسال طلبك الآن. يرجى المحاولة مرة أخرى أو التواصل مع الاستقبال عبر الهاتف أو واتساب.',
    treatments: [
      ['General Dentistry', 'طب الأسنان العام'],
      ['Preventive Dentistry', 'طب الأسنان الوقائي'],
      ['Prosthodontics', 'تركيبات الأسنان'],
      ['Cosmetic Dentistry', 'طب الأسنان التجميلي'],
      ['Dental Implants', 'زراعة الأسنان'],
      ['Orthodontics', 'تقويم الأسنان'],
      ['Periodontics', 'علاج اللثة'],
      ['Endodontics', 'علاج جذور الأسنان'],
      ['Paediatric Dentistry', 'طب أسنان الأطفال'],
      ['Other / Not sure', 'أخرى / لست متأكداً'],
    ],
    clinics: [
      ['Bani Yas Tower - Corniche Street', 'برج بني ياس - شارع الكورنيش'],
      ['Al Raha Mall', 'الراحة مول'],
    ],
  };

  const currentLanguage = () => {
    const htmlLang = (document.documentElement.lang || '').toLowerCase();
    return htmlLang.startsWith('ar') ||
      document.documentElement.dir === 'rtl' ||
      document.body?.classList.contains('language-ar') ||
      document.body?.classList.contains('static-arabic') ||
      window.location.pathname.startsWith('/ar/') ? 'ar' : 'en';
  };

  const bookingFallback = language => language === 'ar'
    ? '/ar/contact.html#consultation-form'
    : '/contact.html#consultation-form';

  const isBookingLink = link => {
    if (!link) return false;
    const text = (link.textContent || '').replace(/\s+/g, ' ').trim().toLowerCase();
    if (!text) return false;
    const english = /(^|\s)book(\s|$)/.test(text) || text.includes('book a consultation') || text.includes('book your appointment');
    const arabic = text.includes('احجز') || text.includes('حجز موعد') || text.includes('احجز موعداً') || text.includes('احجز موعدا');
    return english || arabic;
  };

  const optionMarkup = (items, placeholder) => [
    `<option value="">${placeholder}</option>`,
    ...items.map(([value, label]) => `<option value="${value}">${label}</option>`),
  ].join('');

  function modalMarkup(copy, language) {
    const rtl = language === 'ar';
    return `
      <div class="booking-modal__surface" dir="${rtl ? 'rtl' : 'ltr'}">
        <button class="booking-modal__close" type="button" data-booking-modal-close aria-label="${copy.close}">×</button>
        <div class="booking-modal__head">
          <p class="booking-modal__eyebrow">${rtl ? 'طلب موعد' : 'Appointment request'}</p>
          <h2 id="booking-modal-title">${copy.title}</h2>
          <p id="booking-modal-intro">${copy.intro}</p>
        </div>
        <form class="booking-modal__form" data-booking-form data-consultation-form aria-describedby="booking-modal-privacy">
          <label aria-hidden="true" style="position:absolute;left:-10000px;width:1px;height:1px;overflow:hidden"><span>Website</span><input type="text" name="website" tabindex="-1" autocomplete="off"></label>
          <p class="booking-modal__privacy" id="booking-modal-privacy">${copy.privacy}</p>
          <div class="booking-modal__grid">
            <label><span>${copy.name} <b aria-hidden="true">*</b></span><input type="text" name="name" autocomplete="name" required></label>
            <label><span>${copy.mobile} <b aria-hidden="true">*</b></span><input type="tel" name="phone" autocomplete="tel" placeholder="+971 5X XXX XXXX" required></label>
            <label><span>${copy.email} <b aria-hidden="true">*</b></span><input type="email" name="email" autocomplete="email" required></label>
            <label><span>${copy.treatment} <b aria-hidden="true">*</b></span><select name="treatment" required>${optionMarkup(copy.treatments, copy.choose)}</select></label>
            <label><span>${copy.date}</span><input type="date" name="date"></label>
            <label><span>${copy.time} <b aria-hidden="true">*</b></span><select name="time" required>${optionMarkup([
              ['09:00','09:00'],['10:00','10:00'],['11:00','11:00'],['12:00','12:00'],['13:00','13:00'],['14:00','14:00'],['15:00','15:00'],['16:00','16:00'],['17:00','17:00'],['18:00','18:00'],['19:00','19:00'],['20:00','20:00']
            ], copy.choose)}</select></label>
            <label><span>${copy.clinic} <b aria-hidden="true">*</b></span><select name="clinic" required>${optionMarkup(copy.clinics, copy.choose)}</select></label>
          </div>
          <label class="booking-modal__notes"><span>${copy.notes}</span><textarea name="message" rows="4"></textarea></label>
          <label class="booking-modal__consent"><input type="checkbox" name="privacy-consent" required><span>${copy.consent}</span></label>
          <button class="btn btn--primary booking-modal__submit" type="submit">${copy.submit}</button>
          <p class="booking-modal__status" data-consultation-status role="status"></p>
        </form>
      </div>`;
  }

  function successMarkup(copy, language) {
    const rtl = language === 'ar';
    return `
      <div class="booking-modal__surface booking-modal__success" dir="${rtl ? 'rtl' : 'ltr'}" role="status" aria-live="polite">
        <div class="booking-modal__success-icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" focusable="false"><path d="M5 12.5 9.2 17 19 7.3"/></svg>
        </div>
        <h2 class="booking-modal__success-title" id="booking-modal-title">${copy.successTitle}</h2>
        <p class="booking-modal__success-copy" id="booking-modal-intro">${copy.successBody}</p>
        <button class="btn btn--primary booking-modal__success-done" type="button" data-booking-success-done>${copy.done}</button>
      </div>`;
  }

  function setup() {
    if (document.querySelector('[data-booking-modal]')) return;

    const bookingDialog = document.createElement('dialog');
    bookingDialog.className = 'booking-modal';
    bookingDialog.setAttribute('data-booking-modal', '');
    bookingDialog.setAttribute('aria-labelledby', 'booking-modal-title');
    bookingDialog.setAttribute('aria-describedby', 'booking-modal-intro');
    document.body.appendChild(bookingDialog);

    let lastTrigger = null;
    const reduceMotion = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false;

    const showSuccess = (copy, language) => {
      const formSurface = bookingDialog.querySelector('.booking-modal__surface');
      let swapped = false;

      const swapView = () => {
        if (swapped) return;
        swapped = true;
        bookingDialog.classList.add('booking-modal--success');
        bookingDialog.innerHTML = successMarkup(copy, language);

        const success = bookingDialog.querySelector('.booking-modal__success');
        const done = bookingDialog.querySelector('[data-booking-success-done]');
        done?.addEventListener('click', () => bookingDialog.close());

        const reveal = () => {
          success?.classList.add('booking-modal__success--visible');
          done?.focus({ preventScroll: true });
        };

        if (reduceMotion) reveal();
        else requestAnimationFrame(() => requestAnimationFrame(reveal));
      };

      if (reduceMotion || !formSurface) {
        swapView();
        return;
      }

      formSurface.classList.add('booking-modal__surface--leaving');
      formSurface.addEventListener('transitionend', swapView, { once: true });
      window.setTimeout(swapView, 260);
    };

    const render = language => {
      const copy = language === 'ar' ? AR : EN;
      bookingDialog.classList.remove('booking-modal--success');
      bookingDialog.innerHTML = modalMarkup(copy, language);
      const form = bookingDialog.querySelector('[data-booking-form]');
      const close = bookingDialog.querySelector('[data-booking-modal-close]');

      close?.addEventListener('click', () => bookingDialog.close());

      form?.addEventListener('submit', async event => {
        event.preventDefault();
        if (!form.reportValidity()) return;

        const data = new FormData(form);
        const payload = {
          name: String(data.get('name') || '').trim(),
          email: String(data.get('email') || '').trim(),
          phone: String(data.get('phone') || '').trim(),
          treatment: String(data.get('treatment') || '').trim(),
          date: String(data.get('date') || '').trim(),
          time: String(data.get('time') || '').trim(),
          clinic: String(data.get('clinic') || '').trim(),
          notes: String(data.get('message') || '').trim(),
          language,
          website: String(data.get('website') || '').trim(),
        };

        const status = form.querySelector('[data-consultation-status]');
        const submit = form.querySelector('.booking-modal__submit');
        if (status) status.textContent = copy.sending;
        if (submit) submit.disabled = true;

        try {
          const response = await fetch(BOOKING_ENDPOINT, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
          });
          const result = await response.json().catch(() => ({}));
          if (!response.ok || result.ok !== true) throw new Error('booking_submit_failed');
          form.reset();
          showSuccess(copy, language);
        } catch (_) {
          if (status) status.textContent = copy.error;
        } finally {
          if (submit) submit.disabled = false;
        }
      });
    };

    const open = trigger => {
      const language = currentLanguage();
      render(language);
      lastTrigger = trigger || document.activeElement;
      document.body.classList.add('booking-modal-open');
      if (typeof bookingDialog.showModal === 'function') bookingDialog.showModal();
      else bookingDialog.setAttribute('open', '');
      window.setTimeout(() => bookingDialog.querySelector('input[name="name"]')?.focus(), 0);
    };

    document.addEventListener('click', event => {
      const link = event.target.closest?.('a');
      if (!isBookingLink(link)) return;
      const language = currentLanguage();
      link.setAttribute('href', bookingFallback(language));
      event.preventDefault();
      closeMenuIfNeeded();
      open(link);
    }, true);

    document.querySelectorAll('a').forEach(link => {
      if (isBookingLink(link)) link.setAttribute('href', bookingFallback(currentLanguage()));
    });

    bookingDialog.addEventListener('click', event => {
      if (event.target !== bookingDialog) return;
      const rect = bookingDialog.getBoundingClientRect();
      const inside = event.clientX >= rect.left && event.clientX <= rect.right && event.clientY >= rect.top && event.clientY <= rect.bottom;
      if (!inside) bookingDialog.close();
    });

    bookingDialog.addEventListener('close', () => {
      document.body.classList.remove('booking-modal-open');
      bookingDialog.classList.remove('booking-modal--success');
      lastTrigger?.focus?.();
      lastTrigger = null;
    });
  }

  function closeMenuIfNeeded() {
    const menu = document.querySelector('[data-mobile-nav]');
    const button = document.querySelector('[data-menu-button]');
    menu?.classList.remove('open');
    document.body.classList.remove('menu-open');
    button?.setAttribute('aria-expanded', 'false');
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setup, { once: true });
  else setup();
})();
