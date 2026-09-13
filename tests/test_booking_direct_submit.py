import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BookingDirectSubmitContract(unittest.TestCase):
    def test_popup_submits_directly_without_mail_client(self):
        modal = (ROOT / "booking-modal.js").read_text(encoding="utf-8")
        self.assertNotIn("mailto:", modal)
        self.assertIn("fetch(BOOKING_ENDPOINT", modal)
        self.assertIn("method: 'POST'", modal)
        self.assertIn("Appointment request sent", modal)


if __name__ == "__main__":
    unittest.main()
