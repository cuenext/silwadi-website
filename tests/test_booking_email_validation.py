from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BookingEmailValidationRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.js = (ROOT / 'booking-email-validation.js').read_text(encoding='utf-8')
        cls.routing = (ROOT / 'bilingual-routing.js').read_text(encoding='utf-8')

    def test_rejects_incomplete_email_before_booking_handler(self):
        self.assertIn('Please enter a valid email address.', self.js)
        self.assertIn('يرجى إدخال بريد إلكتروني صالح.', self.js)
        self.assertIn('emailInput.setCustomValidity', self.js)
        self.assertIn('isValidEmailAddress(emailInput.value)', self.js)
        self.assertIn("event.stopImmediatePropagation()", self.js)
        self.assertIn("document.addEventListener('submit'", self.js)

    def test_validator_is_loaded_on_booking_pages(self):
        self.assertIn('booking-email-validation.js?v=20260914-email1', self.routing)
        self.assertIn('data-booking-email-validation', self.routing)


if __name__ == '__main__':
    unittest.main()
