import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BookingNoOutlookContract(unittest.TestCase):
    def test_booking_submission_is_intercepted_before_mail_clients(self):
        submitter = (ROOT / "booking-direct-submit.js").read_text(encoding="utf-8")
        routing = (ROOT / "bilingual-routing.js").read_text(encoding="utf-8")

        self.assertIn("formsubmit.co/ajax/appointment@silwadidentalcenter.ae", submitter)
        self.assertIn("document.addEventListener('submit'", submitter)
        self.assertIn("event.stopImmediatePropagation()", submitter)
        self.assertIn("data-consultation-form", submitter)
        self.assertIn("booking-direct-submit.js", routing)

    def test_legacy_booking_handlers_no_longer_open_mailto(self):
        app = (ROOT / "app.js").read_text(encoding="utf-8")
        modal = (ROOT / "booking-modal.js").read_text(encoding="utf-8")

        self.assertNotIn("window.location.href = `mailto:appointment@silwadidentalcenter.ae", app)
        self.assertNotIn("window.location.href = `mailto:appointment@silwadidentalcenter.ae", modal)


if __name__ == "__main__":
    unittest.main()
