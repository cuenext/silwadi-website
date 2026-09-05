import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BookingModalContract(unittest.TestCase):
    def test_booking_ctas_open_modal_without_losing_contact_fallback(self):
        app = (ROOT / "app.js").read_text(encoding="utf-8")
        self.assertIn('data-booking-modal', app)
        self.assertIn('data-booking-modal-close', app)
        self.assertIn('bookingDialog.showModal()', app)
        self.assertIn('event.preventDefault()', app)
        self.assertIn('contact.html#consultation-form', app)

    def test_booking_modal_is_bilingual_and_contains_the_appointment_fields(self):
        app = (ROOT / "app.js").read_text(encoding="utf-8")
        for token in [
            'Book your appointment',
            'احجز موعدك',
            'Full name',
            'الاسم الكامل',
            'Preferred clinic',
            'الفرع المفضل',
            'Send appointment request',
            'أرسل طلب الموعد',
            'data-consultation-form',
        ]:
            self.assertIn(token, app)

    def test_modal_has_global_mobile_accessible_styling(self):
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertIn('.booking-modal{', css)
        self.assertIn('.booking-modal::backdrop', css)
        self.assertIn('.booking-modal__close', css)
        self.assertIn('@media(max-width:720px)', css)

    def test_important_notice_is_removed_from_source_contact_page(self):
        html = (ROOT / "contact.html").read_text(encoding="utf-8")
        css = (ROOT / "contact-pages.css").read_text(encoding="utf-8")
        self.assertNotIn('Important notice', html)
        self.assertNotIn('false online offers promising free treatments', html)
        self.assertNotIn('appointment-disclaimer', html)
        self.assertNotIn('.appointment-disclaimer', css)


if __name__ == '__main__':
    unittest.main()
