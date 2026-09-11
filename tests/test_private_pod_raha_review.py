import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "review/people-of-determination-raha-v1.html"


class PrivatePodRahaReviewContract(unittest.TestCase):
    def setUp(self):
        self.text = REVIEW.read_text(encoding="utf-8")

    def test_private_review_page_exists_and_is_not_indexable(self):
        self.assertTrue(REVIEW.exists())
        self.assertIn('name="robots" content="noindex,nofollow', self.text)
        self.assertIn("Private review", self.text)
        self.assertIn("Not published", self.text)

    def test_page_has_approved_reference_based_flow(self):
        for section_id in ["hero", "partnership", "individual-care", "complex-needs", "before-visit", "raha", "consultation"]:
            self.assertIn(f'id="{section_id}"', self.text)
        self.assertIn("Dental Care for People of Determination in", self.text)
        self.assertIn("Abu&nbsp;Dhabi", self.text)
        self.assertIn("Al Raha Mall", self.text)

    def test_raha_accessibility_content_is_grounded(self):
        self.assertIn("assets/locations/al-raha-accessible-treatment-room-final.webp", self.text)
        self.assertIn("F14 &amp; F15, Level 1, Al Raha Mall", self.text)
        self.assertIn("Accessible dental treatment room", self.text)
        self.assertNotIn("3 dedicated POD treatment rooms", self.text)

    def test_official_partnership_source_is_present(self):
        self.assertIn("Zayed Authority for People of Determination", self.text)
        self.assertIn("10 April 2026", self.text)
        self.assertIn("Dental-Center-to-Enhance-Comprehensive-Healthcare", self.text)

    def test_visible_abu_dhabi_is_nonbreaking(self):
        body = self.text.split("</head>", 1)[1]
        visible_text = re.sub(r"<[^>]+>", " ", body)
        self.assertNotIn("Abu Dhabi", visible_text)
        self.assertIn("Abu&nbsp;Dhabi", visible_text)

    def test_private_review_is_not_linked_from_public_pages(self):
        public_pages = ["index.html", "services.html", "treatments.html", "doctors.html", "locations.html"]
        for rel in public_pages:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotIn("review/people-of-determination-raha-v1.html", text, f"{rel} must not expose the private review URL")


if __name__ == "__main__":
    unittest.main()
