from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PatchFifteenHomepageRedesign(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.css_path = ROOT / "home-premium.css"
        cls.css = cls.css_path.read_text(encoding="utf-8") if cls.css_path.exists() else ""

    def test_home_uses_dedicated_premium_stylesheet(self):
        self.assertIn('href="home-premium.css"', self.home)
        self.assertNotIn('href="home-trust.css"', self.home)
        self.assertTrue(self.css_path.exists())

    def test_uploaded_official_logo_is_used_without_legacy_crop_hack(self):
        self.assertTrue((ROOT / "assets" / "silwadi-logo-official.png").exists())
        self.assertIn('src="assets/silwadi-logo-official.png"', self.home)
        self.assertNotIn('class="brand-crop"', self.home)
        self.assertNotIn('<img src="assets/silwadi-logo-original.jpeg"', self.home)
        self.assertRegex(
            self.home,
            r'<img[^>]+src="assets/silwadi-logo-official\.png"[^>]+alt="Silwadi Dental Center"[^>]+width="[0-9]+"[^>]+height="[0-9]+"',
        )

    def test_old_template_like_home_patterns_are_removed(self):
        for token in (
            'care-shortcuts__grid',
            'legacy-seal',
            'featured-doctors',
            'doctor-card reveal',
            'treatment-paths',
        ):
            self.assertNotIn(token, self.home)

    def test_new_editorial_home_sections_exist(self):
        for token in (
            'home-brand-hero',
            'home-patient-nav',
            'home-service-feature',
            'home-team-editorial',
            'home-legacy-mark',
            'home-google-reviews',
            'home-location-split',
        ):
            self.assertIn(token, self.home)

    def test_home_preserves_verified_clinic_facts_and_service_names(self):
        required = (
            'since 1980',
            '12 dentists',
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
        self.assertNotIn('Founder', self.home)

    def test_hero_portrait_stays_optimized_high_priority_and_immediately_visible(self):
        self.assertRegex(
            self.home,
            r'<img[^>]+src="assets/doctors/optimized/dr-munir-silwadi\.webp"[^>]+width="720"[^>]+height="720"[^>]+fetchpriority="high"',
        )
        self.assertNotIn('home-brand-hero__copy reveal', self.home)
        self.assertNotIn('home-brand-hero__visual reveal', self.home)

    def test_home_css_has_asymmetric_editorial_layout_mobile_composition_and_safe_nav_contrast(self):
        self.assertIn('.home-brand-hero', self.css)
        self.assertRegex(self.css, r'\.home-brand-hero__inner\s*\{[^}]*grid-template-columns\s*:\s*[^;}]+')
        self.assertIn('.home-service-feature', self.css)
        self.assertIn('.home-team-editorial', self.css)
        self.assertRegex(self.css, r'@media\s*\(max-width\s*:\s*720px\)')
        self.assertIn('min-height:48px', self.css.replace(' ', ''))
        self.assertIn('.home-patient-nav small{color:#526a73', self.css.replace('\n', ''))


if __name__ == '__main__':
    unittest.main()
