from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PatchFifteenHomepageRedesign(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.trust_css = (ROOT / "home-trust.css").read_text(encoding="utf-8")
        cls.reviews_css = (ROOT / "home-reviews.css").read_text(encoding="utf-8")

    def test_home_uses_approved_trust_layout_and_reviews_stylesheet(self):
        self.assertIn('href="home-trust.css"', self.home)
        self.assertIn('href="home-reviews.css"', self.home)
        self.assertNotIn('href="home-premium.css"', self.home)

    def test_uploaded_official_logo_is_used_without_legacy_crop_hack(self):
        self.assertTrue((ROOT / "assets" / "silwadi-logo-official.png").exists())
        self.assertIn('src="assets/silwadi-logo-official.png"', self.home)
        self.assertNotIn('class="brand-crop"', self.home)
        self.assertNotIn('<img src="assets/silwadi-logo-original.jpeg"', self.home)
        self.assertRegex(
            self.home,
            r'<img[^>]+src="assets/silwadi-logo-official\.png"[^>]+alt="Silwadi Dental Center"[^>]+width="[0-9]+"[^>]+height="[0-9]+"',
        )

    def test_approved_compact_home_patterns_are_restored(self):
        for token in (
            'care-shortcuts__grid',
            'legacy-seal',
            'featured-doctors',
            'doctor-card reveal',
            'treatment-paths',
        ):
            self.assertIn(token, self.home)

    def test_home_keeps_reviews_and_current_location_content(self):
        for token in (
            'home-hero',
            'team-proof section--compact',
            'home-google-reviews',
            'google-reviews-track',
            'locations-preview',
        ):
            self.assertIn(token, self.home)
        self.assertNotIn('home-brand-hero', self.home)
        self.assertNotIn('home-team-editorial', self.home)

    def test_home_preserves_verified_clinic_facts_and_featured_services(self):
        required = (
            'since 1980',
            '15 dentists',
            'Implantology',
            'Orthodontics',
            'Periodontics',
            'Cosmetic Dentistry',
            'Preventive Treatments',
            'Bani Yas Tower',
            'Al Raha Mall',
            'patient-centred',
        )
        text = self.home.lower()
        for value in required:
            self.assertIn(value.lower(), text)
        self.assertIn('View all services', self.home)
        self.assertNotIn('Founder', self.home)

    def test_hero_portrait_stays_optimized_and_high_priority(self):
        self.assertRegex(
            self.home,
            r'<img[^>]+src="assets/doctors/optimized/dr-munir-silwadi\.webp"[^>]+width="720"[^>]+height="720"[^>]+fetchpriority="high"',
        )

    def test_restored_home_keeps_mobile_and_reduced_motion_support(self):
        self.assertTrue(self.trust_css)
        self.assertRegex(self.trust_css, r'@media\s*\(max-width')
        self.assertRegex(self.reviews_css, r'@media\s*\(max-width')
        self.assertIn('@media(prefers-reduced-motion:reduce)', self.reviews_css.replace(' ', ''))
        self.assertIn('animation:none', self.reviews_css.replace(' ', ''))


if __name__ == '__main__':
    unittest.main()
