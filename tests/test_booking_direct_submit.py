import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENDPOINT = "https://booking.silwadi.ae/booking-submit.php"
RECIPIENT = "appointment@silwadidentalcenter.ae"


class BookingDirectSubmitContract(unittest.TestCase):
    def test_popup_submits_directly_without_mail_client(self):
        modal = (ROOT / "booking-modal.js").read_text(encoding="utf-8")
        self.assertNotIn("mailto:", modal)
        self.assertIn(f"const BOOKING_ENDPOINT = '{ENDPOINT}';", modal)
        self.assertIn("fetch(BOOKING_ENDPOINT", modal)
        self.assertIn("method: 'POST'", modal)
        self.assertIn("Appointment request sent", modal)
        self.assertIn("تم إرسال طلب الموعد", modal)

    def test_contact_form_uses_same_direct_endpoint(self):
        app = (ROOT / "app.js").read_text(encoding="utf-8")
        self.assertNotIn(f"mailto:{RECIPIENT}", app)
        self.assertIn(f"const CONSULTATION_BOOKING_ENDPOINT = '{ENDPOINT}';", app)
        self.assertIn("fetch(CONSULTATION_BOOKING_ENDPOINT", app)
        self.assertIn("Appointment request sent", app)

    def test_contact_pages_no_longer_claim_mail_app_will_open(self):
        english = (ROOT / "contact.html").read_text(encoding="utf-8")
        arabic = (ROOT / "ar" / "contact.html").read_text(encoding="utf-8")
        self.assertNotIn("Your email app will open", english)
        self.assertNotIn("open in your email app", english)
        self.assertNotIn("تطبيق البريد الإلكتروني", arabic)

    def test_booking_modal_cache_version_is_bumped_for_release(self):
        routing = (ROOT / "bilingual-routing.js").read_text(encoding="utf-8")
        self.assertIn("/booking-modal.js?v=20260914-1", routing)


if __name__ == "__main__":
    unittest.main()
