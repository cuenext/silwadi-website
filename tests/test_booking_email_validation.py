from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BookingEmailValidationRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.js = (ROOT / 'booking-modal.js').read_text(encoding='utf-8')

    def test_rejects_incomplete_email_before_network_request(self):
        self.assertIn("invalidEmail: 'Please enter a valid email address.'", self.js)
        self.assertIn("invalidEmail: 'يرجى إدخال بريد إلكتروني صالح.'", self.js)
        self.assertIn('emailInput.setCustomValidity', self.js)
        self.assertIn('isValidEmailAddress(payload.email)', self.js)
        self.assertLess(self.js.index('isValidEmailAddress(payload.email)'), self.js.index('await fetch(BOOKING_ENDPOINT'))

    def test_backend_invalid_email_gets_specific_message(self):
        self.assertIn("result.error === 'invalid_email'", self.js)
        self.assertIn('copy.invalidEmail', self.js)


if __name__ == '__main__':
    unittest.main()
