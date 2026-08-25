from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Patch17HomepageRollbackReviewsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.about = (ROOT / "about.html").read_text(encoding="utf-8")

    def test_restores_pre_redesign_homepage_identity(self):
        self.assertIn("Advanced dentistry.", self.home)
        self.assertIn("Established trust.", self.home)
        self.assertIn('class="home-hero"', self.home)
        self.assertIn('class="team-proof section--compact"', self.home)
        self.assertIn('class="featured-doctors"', self.home)
        self.assertIn('href="home-trust.css"', self.home)
        self.assertNotIn('href="home-premium.css"', self.home)
        self.assertNotIn("Established dentistry.", self.home)

    def test_google_reviews_are_kept_on_restored_home(self):
        self.assertIn('id="reviews"', self.home)
        self.assertIn('class="google-reviews-track"', self.home)
        self.assertIn("https://maps.app.goo.gl/Ln2vEZmQmgWjb3ETA", self.home)
        self.assertIn("4.6", self.home)
        self.assertIn("199 Google reviews", self.home)
        self.assertIn("Read all reviews", self.home)

    def test_official_logo_is_visible_without_crop_hacks(self):
        self.assertIn('src="assets/silwadi-logo-official.png"', self.home)
        self.assertNotIn("brand-crop", self.home)
        self.assertNotIn("footer-logo-crop", self.home)

    def test_al_raha_is_open_on_homepage(self):
        self.assertIn("Al Raha Mall", self.home)
        self.assertIn("+971 2 666 2408", self.home)
        self.assertNotIn("Al Raha Mall coming soon", self.home)
        self.assertNotIn("Our Al Raha Mall branch is coming soon", self.home)

    def test_digital_dentistry_is_not_a_standalone_home_feature(self):
        self.assertNotIn('href="digital-dentistry.html"', self.home)
        self.assertNotIn('class="section digital-section"', self.home)

    def test_about_keeps_human_clinic_copy(self):
        self.assertIn("since 1980", self.about.lower())
        self.assertIn("explain", self.about.lower())
        self.assertIn("questions", self.about.lower())
        self.assertNotIn("multidisciplinary planning", self.about.lower())


if __name__ == "__main__":
    unittest.main()
