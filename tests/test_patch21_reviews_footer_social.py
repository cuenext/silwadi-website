from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Patch21ReviewsFooterSocial(unittest.TestCase):
    def read(self, path):
        return (ROOT / path).read_text(encoding="utf-8")

    def public_pages_with_footer(self):
        pages = []
        for path in ROOT.rglob("*.html"):
            if any(part in {".git", "node_modules"} for part in path.parts):
                continue
            text = path.read_text(encoding="utf-8")
            if '<footer class="site-footer">' in text:
                pages.append((path, text))
        self.assertTrue(pages, "Expected public HTML pages with the shared footer")
        return pages

    def test_google_aggregate_rating_uses_four_full_and_one_half_star(self):
        home = self.read("index.html")
        match = re.search(r'<span class="google-rating-card__stars"[^>]*>(.*?)</span><strong>4\.6</strong>', home, re.S)
        self.assertIsNotNone(match, "Expected the Google aggregate star display beside the 4.6 rating")
        stars = match.group(1)
        self.assertEqual(stars.count('rating-star--full'), 4)
        self.assertEqual(stars.count('rating-star--half'), 1)
        self.assertIn('aria-label="4.6 out of 5 stars"', home)

    def test_review_cards_open_an_accessible_reading_dialog(self):
        home = self.read("index.html")
        app = self.read("app.js")
        self.assertGreaterEqual(home.count('data-review-open'), 5)
        self.assertIn('aria-haspopup="dialog"', home)
        self.assertIn('<dialog class="review-dialog" data-review-dialog', home)
        self.assertIn('data-review-dialog-close', home)
        self.assertIn('data-review-dialog-name', home)
        self.assertIn('data-review-dialog-text', home)
        self.assertIn("showModal()", app)
        self.assertIn("data-review-open", app)
        self.assertIn("data-review-dialog-close", app)

    def test_interactive_reviews_keep_visible_text_as_accessible_name(self):
        home = self.read("index.html")
        first_group = re.search(r'<div class="google-reviews-group">(.*?)</div><div class="google-reviews-group" aria-hidden="true">', home, re.S)
        self.assertIsNotNone(first_group)
        cards = re.findall(r'<article class="google-review-card"[^>]*data-review-open[^>]*>', first_group.group(1))
        self.assertGreaterEqual(len(cards), 5)
        for card in cards:
            self.assertNotIn('aria-label=', card, "Visible review text should provide the button accessible name")

    def test_sitewide_footer_has_verified_bani_yas_hours(self):
        required = [
            "Bani Yas Tower hours",
            "Sunday – Wednesday",
            "09:00 AM – 09:00 PM",
            "Thursday &amp; Saturday",
            "09:00 AM – 06:00 PM",
            "Friday",
            "Closed",
        ]
        for path, html in self.public_pages_with_footer():
            for text in required:
                self.assertIn(text, html, f"{path} missing footer-hours text: {text}")

    def test_sitewide_footer_links_official_instagram(self):
        url = "https://www.instagram.com/dr.munirsilwadidental/"
        for path, html in self.public_pages_with_footer():
            self.assertIn(url, html, f"{path} missing official Instagram URL")
            self.assertIn("@dr.munirsilwadidental", html, f"{path} missing Instagram handle")
            instagram = re.search(r'<a class="footer-instagram"[^>]*>', html)
            self.assertIsNotNone(instagram, f"{path} missing Instagram link")
            self.assertNotIn('aria-label=', instagram.group(0), f"{path} should use the visible Instagram handle as its name")

    def test_footer_hours_text_uses_accessible_contrast(self):
        css = self.read("styles.css")
        self.assertRegex(css, r'\.footer-hours em\{color:#526a73\}')


if __name__ == "__main__":
    unittest.main()
