import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "review/people-of-determination-raha-v1.html"


class PrivatePodRahaReviewContract(unittest.TestCase):
    def test_private_review_page_exists_and_is_not_indexable(self):
        self.assertTrue(REVIEW.exists(), "review/people-of-determination-raha-v1.html must exist")
        text = REVIEW.read_text(encoding="utf-8")
        self.assertIn('name="robots" content="noindex,nofollow', text)
        self.assertIn("Private review", text)
        self.assertIn("Not published", text)

    def test_page_has_approved_content_flow(self):
        text = REVIEW.read_text(encoding="utf-8")
        for section_id in ["hero", "accessibility", "visit", "care", "raha", "faq", "consultation"]:
            self.assertIn(f'id="{section_id}"', text)
        self.assertIn("Dental Care for People of Determination in", text)
        self.assertIn("Abu&nbsp;Dhabi", text)
        self.assertIn("Al Raha Mall", text)

    def test_raha_accessibility_and_contact_are_grounded(self):
        text = REVIEW.read_text(encoding="utf-8")
        self.assertIn("assets/locations/al-raha-accessible-treatment-room-final.webp", text)
        self.assertIn("+971 2 666 2408", text)
        self.assertIn("F14 &amp; F15, Level 1, Al Raha Mall", text)
        self.assertNotIn("3 dedicated POD treatment rooms", text)

    def test_seo_language_is_present_without_keyword_stuffing(self):
        text = REVIEW.read_text(encoding="utf-8")
        self.assertIn("People of Determination dental care", text)
        self.assertIn("accessible dental care", text)
        self.assertIn("special needs dentistry", text)
        self.assertLessEqual(text.lower().count("special needs dentistry"), 2)

    def test_visible_abu_dhabi_is_nonbreaking(self):
        text = REVIEW.read_text(encoding="utf-8")
        body = text.split("</head>", 1)[1]
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
