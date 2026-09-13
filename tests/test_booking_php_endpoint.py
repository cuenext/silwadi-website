import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BookingPhpEndpointContract(unittest.TestCase):
    def test_php_endpoint_validates_and_sends_server_side(self):
        endpoint = (ROOT / "backend" / "booking-submit.php").read_text(encoding="utf-8")
        for token in [
            "REQUEST_METHOD",
            "application/json",
            "filter_var",
            "FILTER_VALIDATE_EMAIL",
            "appointment@silwadidentalcenter.ae",
            "Reply-To:",
            "mail(",
            "rate_limit",
            "honeypot",
            "Access-Control-Allow-Origin",
            "OPTIONS",
            "https://silwadi.ae",
        ]:
            self.assertIn(token, endpoint)
        self.assertNotIn("RESEND_API_KEY", endpoint)


if __name__ == "__main__":
    unittest.main()
