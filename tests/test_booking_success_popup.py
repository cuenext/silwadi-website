from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BookingSuccessPopupRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.js = (ROOT / 'booking-modal.js').read_text(encoding='utf-8')
        cls.css = (ROOT / 'booking-modal.css').read_text(encoding='utf-8')
        cls.routing = (ROOT / 'bilingual-routing.js').read_text(encoding='utf-8')

    def test_success_uses_dedicated_confirmation_view(self):
        self.assertIn('booking-modal__success', self.js)
        self.assertIn('booking-modal__success-title', self.js)
        self.assertIn('Appointment request sent', self.js)
        self.assertIn('Our appointments team will contact you to confirm availability.', self.js)
        self.assertIn("done: 'Done'", self.js)
        self.assertIn("successTitle: 'تم إرسال طلب الموعد'", self.js)

    def test_success_transition_is_animated_and_accessible(self):
        self.assertIn('booking-modal__surface--leaving', self.css)
        self.assertIn('booking-modal__success--visible', self.css)
        self.assertIn('@media(prefers-reduced-motion:reduce)', self.css)
        self.assertIn('prefers-reduced-motion: reduce', self.js)

    def test_success_only_follows_confirmed_backend_ok(self):
        ok_check = "if (!response.ok || result.ok !== true) throw new Error('booking_submit_failed');"
        self.assertIn(ok_check, self.js)
        self.assertIn('showSuccess(copy, language)', self.js)
        self.assertLess(self.js.index(ok_check), self.js.index('showSuccess(copy, language)'))

    def test_booking_assets_are_cache_busted(self):
        self.assertIn('booking-modal.js?v=20260914-success1', self.routing)
        self.assertIn('booking-modal.css?v=20260914-success1', self.routing)


if __name__ == '__main__':
    unittest.main()
