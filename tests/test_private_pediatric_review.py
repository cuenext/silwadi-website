import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "review/pediatric-dentistry-v1.html"


class PrivatePediatricReviewContract(unittest.TestCase):
    def test_private_review_page_exists_and_is_not_indexable(self):
        self.assertTrue(REVIEW.exists(), "review/pediatric-dentistry-v1.html must exist")
        text = REVIEW.read_text(encoding="utf-8")
        self.assertIn('name="robots" content="noindex,nofollow', text)
        self.assertIn("Private review", text)
        self.assertIn("Not published", text)

    def test_page_has_approved_concise_flow(self):
        text = REVIEW.read_text(encoding="utf-8")
        for section_id in ["hero", "care", "visit", "specialist", "faq", "consultation"]:
            self.assertIn(f'id="{section_id}"', text)
        self.assertNotIn('id="when-to-visit"', text)
        self.assertNotIn('id="treatments"', text)
        self.assertNotIn('id="first-visit"', text)
        self.assertEqual(text.count('class="pd-care-card"'), 4)
        self.assertEqual(text.count('class="pd-visit-step"'), 3)
        self.assertEqual(text.count("<details>"), 4)
        self.assertIn("Dr. Kashmira Pawar Jayprakash", text)
        self.assertIn("assets/doctors/dr-kashmira-pawar-jayprakash.webp", text)

    def test_page_is_seo_ready_while_remaining_private(self):
        text = REVIEW.read_text(encoding="utf-8")
        title = re.search(r"<title>(.*?)</title>", text, re.S)
        description = re.search(r'<meta name="description" content="([^"]+)">', text)
        self.assertIsNotNone(title)
        self.assertIsNotNone(description)
        self.assertIn("Pediatric Dentist in Abu Dhabi", title.group(1))
        self.assertIn("pediatric dentist in Abu Dhabi", description.group(1))
        self.assertIn("children", description.group(1).lower())
        self.assertIn("Pediatric Dentistry in", text)
        self.assertIn("Abu&nbsp;Dhabi", text)
        self.assertIn("baby teeth", text.lower())
        self.assertIn("dental trauma", text.lower())
        self.assertIn("pulp therapy", text.lower())

    def test_visible_abu_dhabi_is_nonbreaking(self):
        text = REVIEW.read_text(encoding="utf-8")
        body = text.split("</head>", 1)[1]
        self.assertNotIn("Abu Dhabi", body)
        self.assertIn("Abu&nbsp;Dhabi", body)

    def test_private_review_is_not_linked_from_public_pages(self):
        public_pages = ["index.html", "services.html", "treatments.html", "doctors.html"]
        for rel in public_pages:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotIn("review/pediatric-dentistry-v1.html", text, f"{rel} must not expose the private review URL")


if __name__ == "__main__":
    unittest.main()
