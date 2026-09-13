import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BookingWorkerContract(unittest.TestCase):
    def test_worker_sends_booking_email_server_side(self):
        worker = (ROOT / "worker" / "silwadi-booking-worker.js").read_text(encoding="utf-8")
        for token in [
            "https://api.resend.com/emails",
            "RESEND_API_KEY",
            "BOOKING_RECIPIENT",
            "appointment@silwadidentalcenter.ae",
            "BOOKING_FROM",
            "/request",
            "Access-Control-Allow-Origin",
            "silwadi.ae",
        ]:
            self.assertIn(token, worker)
        self.assertNotIn("Bearer re_", worker)


if __name__ == "__main__":
    unittest.main()
