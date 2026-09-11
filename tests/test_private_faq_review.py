import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "review/dental-faq-v1.html"


class PrivateFaqReviewContract(unittest.TestCase):
    def test_private_review_page_exists_and_is_not_indexable(self):
        self.assertTrue(REVIEW.exists(), "review/dental-faq-v1.html must exist")
        text = REVIEW.read_text(encoding="utf-8")
        self.assertIn('name="robots" content="noindex,nofollow', text)
        self.assertIn("Private review", text)
        self.assertIn("Not published", text)

    def test_page_has_clean_grouped_faq_structure(self):
        text = REVIEW.read_text(encoding="utf-8")
        for section_id in ["hero", "appointments", "prevention", "children", "treatments", "consultation"]:
            self.assertIn(f'id="{section_id}"', text)
        self.assertEqual(text.count('class="faq-review-group"'), 4)
        self.assertGreaterEqual(text.count("<details"), 12)
        self.assertLessEqual(text.count("<details"), 16)

    def test_old_faq_topics_are_preserved_without_outdated_claims(self):
        text = REVIEW.read_text(encoding="utf-8")
        lowered = text.lower()
        for topic in ["new patient", "x-rays", "floss", "first dental visit", "fluoride", "root canal", "crown", "whitening", "implant"]:
            self.assertIn(topic, lowered)
        self.assertNotIn("we send most claims electronically", lowered)
        self.assertNotIn("training toothpaste without fluoride", lowered)
        self.assertNotIn("x-rays occur on a regular basis", lowered)
        self.assertNotIn("the first dental visit will be fun", lowered)

    def test_seo_copy_is_ready_while_page_remains_private(self):
        text = REVIEW.read_text(encoding="utf-8")
        title = re.search(r"<title>(.*?)</title>", text, re.S)
        description = re.search(r'<meta name="description" content="([^"]+)">', text)
        self.assertIsNotNone(title)
        self.assertIsNotNone(description)
        self.assertIn("Dental FAQ", title.group(1))
        self.assertIn("Abu Dhabi", title.group(1))
        self.assertIn("dental questions", description.group(1).lower())
        self.assertIn("Abu Dhabi", description.group(1))
        self.assertIn("Dental Questions, Answered", text)

    def test_visible_abu_dhabi_is_nonbreaking(self):
        text = REVIEW.read_text(encoding="utf-8")
        body = text.split("</head>", 1)[1]
        self.assertNotIn("Abu Dhabi", body)
        self.assertIn("Abu&nbsp;Dhabi", body)

    def test_private_review_is_not_linked_from_public_pages(self):
        public_pages = ["index.html", "services.html", "treatments.html", "doctors.html", "about.html", "contact.html"]
        for rel in public_pages:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotIn("review/dental-faq-v1.html", text, f"{rel} must not expose the private review URL")


if __name__ == "__main__":
    unittest.main()
