from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
APP_JS = ROOT / "app.js"
BOOKING_JS = ROOT / "booking-modal.js"


class PediatricBookingModalContract(unittest.TestCase):
    def test_booking_ctas_load_existing_popup_and_prevent_navigation(self):
        app = APP_JS.read_text(encoding="utf-8")
        booking = BOOKING_JS.read_text(encoding="utf-8")
        self.assertIn("/review/pediatric-dentistry-v1.html", app)
        self.assertIn("../booking-modal.css", app)
        self.assertIn("../booking-modal.js", app)
        self.assertIn("event.preventDefault();", booking)
        self.assertIn("open(link);", booking)


if __name__ == "__main__":
    unittest.main()
