import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "review/endodontics-v4.html"


class PrivateEndodonticsReviewContract(unittest.TestCase):
    def test_private_review_page_exists_and_is_not_indexable(self):
        self.assertTrue(REVIEW.exists(), "review/endodontics-v4.html must exist")
        text = REVIEW.read_text(encoding="utf-8")
        self.assertIn('name="robots" content="noindex,nofollow', text)
        self.assertIn("Private review", text)
        self.assertIn("Not published", text)

    def test_private_review_is_not_linked_from_public_pages(self):
        public_pages = ["index.html", "services.html", "treatments.html", "doctors.html"]
        for rel in public_pages:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotIn("review/endodontics-v4.html", text, f"{rel} must not expose the private review URL")


if __name__ == "__main__":
    unittest.main()
