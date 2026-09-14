from pathlib import Path


ENDPOINT = "https://booking.silwadi.ae/booking-submit.php"


def update_booking_modal() -> None:
    path = Path("booking-modal.js")
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "(function silwadiBookingModal() {\n",
        "(function silwadiBookingModal() {\n  const BOOKING_ENDPOINT = 'https://booking.silwadi.ae/booking-submit.php';\n\n",
        1,
    )
    text = text.replace(
        "privacy: 'Your email app will open with the details you enter. We use them only to respond to this appointment enquiry. Please do not include sensitive medical information.',",
        "privacy: 'Your details are sent securely to our appointments team and used only to respond to this enquiry. Please do not include sensitive medical information.',",
        1,
    )
    text = text.replace(
        "status: 'Your email app is opening with the appointment request.',",
        "sending: 'Sending your appointment request…',\n    status: 'Appointment request sent ✓ Our team will contact you to confirm availability.',\n    error: 'We could not send your request right now. Please try again or contact reception by phone or WhatsApp.',",
        1,
    )
    text = text.replace(
        "privacy: 'سيفتح تطبيق البريد الإلكتروني بالتفاصيل التي تدخلها. نستخدم هذه المعلومات فقط للرد على طلب الموعد. يرجى عدم إدخال معلومات طبية حساسة هنا.',",
        "privacy: 'تُرسل بياناتك مباشرة وبشكل آمن إلى فريق المواعيد ونستخدمها فقط للرد على طلبك. يرجى عدم إدخال معلومات طبية حساسة هنا.',",
        1,
    )
    text = text.replace(
        "status: 'سيتم الآن فتح تطبيق البريد الإلكتروني مع تفاصيل طلب الموعد.',",
        "sending: 'جارٍ إرسال طلب الموعد…',\n    status: 'تم إرسال طلب الموعد ✓ سيتواصل معك فريقنا لتأكيد التوافر.',\n    error: 'تعذر إرسال طلبك الآن. يرجى المحاولة مرة أخرى أو التواصل مع الاستقبال عبر الهاتف أو واتساب.',",
        1,
    )
    text = text.replace(
        '<form class="booking-modal__form" data-booking-form data-consultation-form aria-describedby="booking-modal-privacy">\n          <p class="booking-modal__privacy"',
        '<form class="booking-modal__form" data-booking-form data-consultation-form aria-describedby="booking-modal-privacy">\n          <label aria-hidden="true" style="position:absolute;left:-10000px;width:1px;height:1px;overflow:hidden"><span>Website</span><input type="text" name="website" tabindex="-1" autocomplete="off"></label>\n          <p class="booking-modal__privacy"',
        1,
    )
    start = text.index("      form?.addEventListener('submit', event => {")
    end = text.index("\n    };\n\n    const open", start)
    handler = """      form?.addEventListener('submit', async event => {
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
          if (status) status.textContent = copy.status;
        } catch (_) {
          if (status) status.textContent = copy.error;
        } finally {
          if (submit) submit.disabled = false;
        }
      });"""
    path.write_text(text[:start] + handler + text[end:], encoding="utf-8")


def update_app() -> None:
    path = Path("app.js")
    text = path.read_text(encoding="utf-8")
    start = text.index("// Prepare consultation requests in the visitor's email app for the appointments team.")
    end = text.index("// Shared FAQ accordion behavior.", start)
    direct = """// Send consultation requests directly to the appointments team without opening a mail app.
const CONSULTATION_BOOKING_ENDPOINT = 'https://booking.silwadi.ae/booking-submit.php';
document.querySelectorAll('[data-consultation-form]').forEach(form => {
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (!form.reportValidity()) return;

    const data = new FormData(form);
    const language = (document.documentElement.lang || '').toLowerCase().startsWith('ar')
      ? 'ar'
      : (window.SilwadiLanguage?.getLanguage?.() || 'en');
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
    const submit = form.querySelector('button[type="submit"]');
    const sendingMessage = language === 'ar' ? 'جارٍ إرسال طلب الموعد…' : 'Sending your appointment request…';
    const successMessage = language === 'ar'
      ? 'تم إرسال طلب الموعد ✓ سيتواصل معك فريقنا لتأكيد التوافر.'
      : 'Appointment request sent ✓ Our team will contact you to confirm availability.';
    const errorMessage = language === 'ar'
      ? 'تعذر إرسال طلبك الآن. يرجى المحاولة مرة أخرى أو التواصل مع الاستقبال عبر الهاتف أو واتساب.'
      : 'We could not send your request right now. Please try again or contact reception by phone or WhatsApp.';

    if (status) status.textContent = sendingMessage;
    if (submit) submit.disabled = true;

    try {
      const response = await fetch(CONSULTATION_BOOKING_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const result = await response.json().catch(() => ({}));
      if (!response.ok || result.ok !== true) throw new Error('booking_submit_failed');
      form.reset();
      if (status) status.textContent = successMessage;
    } catch (_) {
      if (status) status.textContent = errorMessage;
    } finally {
      if (submit) submit.disabled = false;
    }
  });
});


"""
    path.write_text(text[:start] + direct + text[end:], encoding="utf-8")


def update_contact_pages() -> None:
    path = Path("contact.html")
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "Your request will open in your email app addressed to the appointments team. They will confirm availability and guide you to the right clinician.",
        "Your request is sent directly to our appointments team. They will contact you to confirm availability and guide you to the right clinician.",
        1,
    )
    text = text.replace(
        "Your email app will open with the details you enter. We use them only to respond to this appointment enquiry. Please do not include sensitive medical information in the form.",
        "Your details are sent securely to our appointments team and used only to respond to this appointment enquiry. Please do not include sensitive medical information in the form.",
        1,
    )
    text = text.replace(
        '<form class="consultation-form" data-consultation-form aria-describedby="consultation-privacy-note"><p id="consultation-privacy-note"',
        '<form class="consultation-form" data-consultation-form aria-describedby="consultation-privacy-note"><label aria-hidden="true" style="position:absolute;left:-10000px;width:1px;height:1px;overflow:hidden"><span>Website</span><input type="text" name="website" tabindex="-1" autocomplete="off"></label><p id="consultation-privacy-note"',
        1,
    )
    path.write_text(text, encoding="utf-8")

    path = Path("ar/contact.html")
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "سيفتح طلبك في تطبيق البريد الإلكتروني موجهاً إلى فريق المواعيد. سيؤكد الفريق التوافر ويوجهك إلى الطبيب المناسب.",
        "يُرسل طلبك مباشرة إلى فريق المواعيد. سيتواصل معك الفريق لتأكيد التوافر وتوجيهك إلى الطبيب المناسب.",
        1,
    )
    text = text.replace(
        "سيفتح تطبيق البريد الإلكتروني مع التفاصيل التي تدخلها. نستخدمها فقط للرد على استفسار الموعد. يرجى عدم إدخال معلومات طبية حساسة في النموذج.",
        "تُرسل بياناتك مباشرة وبشكل آمن إلى فريق المواعيد ونستخدمها فقط للرد على طلب الموعد. يرجى عدم إدخال معلومات طبية حساسة في النموذج.",
        1,
    )
    text = text.replace(
        '<form class="consultation-form" data-consultation-form="" aria-describedby="consultation-privacy-note"><p id="consultation-privacy-note"',
        '<form class="consultation-form" data-consultation-form="" aria-describedby="consultation-privacy-note"><label aria-hidden="true" style="position:absolute;left:-10000px;width:1px;height:1px;overflow:hidden"><span>Website</span><input type="text" name="website" tabindex="-1" autocomplete="off"></label><p id="consultation-privacy-note"',
        1,
    )
    path.write_text(text, encoding="utf-8")


def bump_cache() -> None:
    path = Path("bilingual-routing.js")
    text = path.read_text(encoding="utf-8")
    text = text.replace('/booking-modal.css?v=20260905-1', '/booking-modal.css?v=20260914-1')
    text = text.replace('/booking-modal.js?v=20260905-1', '/booking-modal.js?v=20260914-1')
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    update_booking_modal()
    update_app()
    update_contact_pages()
    bump_cache()
