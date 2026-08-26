from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Patch21ReviewsFooterSocials(unittest.TestCase):
    def setUp(self):
        self.home = (ROOT / "index.html").read_text(encoding="utf-8")
        self.css = (ROOT / "home-reviews.css").read_text(encoding="utf-8")
        self.app = (ROOT / "app.js").read_text(encoding="utf-8")
        self.public_pages = [
            *ROOT.glob("*.html"),
            *(ROOT / "doctors").glob("*.html"),
            *(ROOT / "treatments").glob("*.html"),
        ]

    def test_google_summary_visually_uses_four_full_and_one_half_star(self):
        rating = re.search(r'<div class="google-rating-card".*?</div>', self.home, re.S)
        self.assertIsNotNone(rating)
        block = rating.group(0)
        self.assertIn('aria-label="4.6 out of 5 stars"', block)
        self.assertEqual(block.count('class="rating-star rating-star--full"'), 4)
        self.assertEqual(block.count('class="rating-star rating-star--half"'), 1)
        self.assertIn('.rating-star--half', self.css)

    def test_review_cards_are_tappable_and_open_accessible_dialog(self):
        cards = re.findall(r'class="google-review-card[^\"]*"', self.home)
        self.assertGreaterEqual(len(cards), 6)
        self.assertGreaterEqual(self.home.count('data-review-expand'), 6)
        self.assertIn('<dialog class="review-dialog"', self.home)
        self.assertIn('data-review-dialog', self.home)
        self.assertIn('data-review-close', self.home)
        self.assertIn('showModal()', self.app)
        self.assertIn('data-review-expand', self.app)
        self.assertIn('Escape', self.app)

    def test_footer_shows_original_opening_hours_sitewide(self):
        for path in self.public_pages:
            html = path.read_text(encoding="utf-8")
            self.assertIn('Sunday - Wednesday', html, path.as_posix())
            self.assertIn('09:00 AM to 09:00 PM', html, path.as_posix())
            self.assertIn('Thursday &amp; Saturday', html, path.as_posix())
            self.assertIn('09:00 AM to 06:00 PM', html, path.as_posix())
            self.assertIn('Friday: Closed', html, path.as_posix())

    def test_official_instagram_is_visible_in_footer_sitewide(self):
        instagram = 'https://www.instagram.com/dr.munirsilwadidental/'
        for path in self.public_pages:
            html = path.read_text(encoding="utf-8")
            self.assertIn(instagram, html, path.as_posix())
            self.assertIn('@dr.munirsilwadidental', html, path.as_posix())

    def test_home_schema_exposes_official_instagram(self):
        self.assertIn('"sameAs":["https://www.instagram.com/dr.munirsilwadidental/"]', self.home)


if __name__ == "__main__":
    unittest.main()
