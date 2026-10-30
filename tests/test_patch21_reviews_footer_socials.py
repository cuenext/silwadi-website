from pathlib import Path
import re
import subprocess
import unittest
from tests.test_review_translation_parity import ReviewCards, render_reviews

ROOT = Path(__file__).resolve().parents[1]


def run_review_scenario(scenario, language="en"):
    result = subprocess.run(
        ["node", "tests/review_interactions_runtime.cjs", scenario, language],
        cwd=ROOT, text=True, encoding="utf-8", capture_output=True,
    )
    if result.returncode:
        raise AssertionError(result.stderr)


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
        rating = re.search(r'<a class="google-rating-card".*?</a>', self.home, re.S)
        self.assertIsNotNone(rating)
        block = rating.group(0)
        self.assertIn('aria-label="4.6 out of 5 stars"', block)
        self.assertEqual(block.count('class="rating-star rating-star--full"'), 4)
        self.assertEqual(block.count('class="rating-star rating-star--half"'), 1)
        self.assertIn('.rating-star--half', self.css)

    def test_review_cards_are_tappable_and_open_accessible_dialog(self):
        result = render_reviews("en")
        cards, copies = [ReviewCards(markup).cards for markup in result["groups"]]
        self.assertEqual(len(cards), 157)
        self.assertEqual(len(copies), 157)
        for card in cards:
            self.assertIn("data-review-expand", card["attrs"])
            self.assertEqual(card["attrs"].get("tabindex"), "0")
            self.assertEqual(card["attrs"].get("role"), "button")
            self.assertEqual(card["attrs"].get("aria-haspopup"), "dialog")
        self.assertTrue(all("data-review-expand" not in card["attrs"] for card in copies))
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

    def test_review_dialog_uses_selected_cards_branch_url(self):
        run_review_scenario("dialog-url")

    def test_delegated_click_enter_and_space_survive_card_replacement(self):
        run_review_scenario("delegation")

    def test_all_dialog_close_paths_restore_trigger_focus(self):
        run_review_scenario("focus-close")

    def test_language_selection_rerenders_bilingual_review_content(self):
        run_review_scenario("language")

    def test_both_static_homepage_languages_initialize_reviews(self):
        for language in ("en", "ar"):
            with self.subTest(language=language):
                run_review_scenario("initial-language", language)

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
