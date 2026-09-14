from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "review/pediatric-dentistry-v1.html"
BOOKING_JS = ROOT / "booking-modal.js"


class PediatricBookingModalContract(unittest.TestCase):
    def test_booking_ctas_load_existing_popup_and_prevent_navigation(self):
        page = PAGE.read_text(encoding="utf-8")
        booking = BOOKING_JS.read_text(encoding="utf-8")
        self.assertIn('<link rel="stylesheet" href="../booking-modal.css">', page)
        self.assertIn('<script src="../booking-modal.js"></script>', page)
        self.assertLess(page.index('../booking-modal.js'), page.index('../app.js'))
        self.assertIn('event.preventDefault();', booking)
        self.assertIn('open(link);', booking)


if __name__ == "__main__":
    unittest.main()
