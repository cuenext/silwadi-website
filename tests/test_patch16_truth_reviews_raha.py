from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PatchSixteenTruthReviewsRaha(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.about = (ROOT / "about.html").read_text(encoding="utf-8")
        cls.locations = (ROOT / "locations.html").read_text(encoding="utf-8")
        cls.contact = (ROOT / "contact.html").read_text(encoding="utf-8")
        cls.css = (ROOT / "home-reviews.css").read_text(encoding="utf-8")
        cls.app = (ROOT / "app.js").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.public_html = [p for p in ROOT.rglob("*.html") if ".github" not in p.parts]

    def test_about_copy_is_plain_human_and_matches_official_values(self):
        text = self.about.lower()
        for required in (
            "since 1980",
            "abu dhabi",
            "explain",
            "questions",
            "comfort",
            "treatment",
        ):
            self.assertIn(required, text)
        for ai_phrase in (
            "established care. evolving practice.",
            "care organised around the next clinical step",
            "personalized planning",
            "patient journey",
            "how we work",
            "coordinate",
        ):
            self.assertNotIn(ai_phrase, text)

    def test_digital_dentistry_is_not_promoted_as_a_standalone_site_section(self):
        self.assertNotIn("digital-dentistry.html", self.sitemap)
        self.assertNotIn("home-digital-band", self.home)
        for page in self.public_html:
            if page.name == "digital-dentistry.html":
                continue
            text = page.read_text(encoding="utf-8")
            self.assertNotRegex(text, r'<a[^>]+href=["\'](?:\.\./)?digital-dentistry\.html["\']')

    def test_al_raha_is_open_everywhere_and_uses_verified_branch_phone(self):
        combined = "\n".join((self.home, self.locations, self.contact)).lower()
        self.assertNotIn("coming soon", combined)
        self.assertNotIn("not yet open", combined)
        self.assertIn("al raha mall", combined)
        self.assertIn("+971 2 666 2408", combined)
        self.assertIn("+97126662408", combined.replace(" ", ""))
        self.assertRegex(self.locations, r'Al Raha Mall[\s\S]{0,1200}(Open|Current location|Now open)')

    def test_google_reviews_section_uses_real_listing_summary_and_maps_link(self):
        self.assertIn('class="home-google-reviews', self.home)
        self.assertIn('4.6', self.home)
        self.assertIn('Google', self.home)
        self.assertIn('https://maps.app.goo.gl/Ln2vEZmQmgWjb3ETA', self.home)
        for reviewer in ("Ahmed H", "Emily Campbell Scully", "Victoriya Davydova", "Sanaa Freihat", "Sahar Alsalman"):
            self.assertIn(reviewer, self.home)
        cards = len(re.findall(r'class="google-review-card', self.home))
        self.assertGreaterEqual(cards, 6)

    def test_reviews_carousel_moves_and_respects_reduced_motion(self):
        self.assertIn('google-reviews-track', self.home)
        self.assertRegex(self.css, r'@keyframes\s+reviews-marquee')
        self.assertRegex(self.css, r'\.google-reviews-track[^}]*animation\s*:')
        reduced = re.search(r'@media\s*\(prefers-reduced-motion:reduce\)([\s\S]+)$', self.css)
        self.assertIsNotNone(reduced)
        self.assertIn('google-reviews-track', reduced.group(1))
        self.assertIn('animation:none', reduced.group(1).replace(' ', ''))

    def test_header_and_footer_use_uploaded_official_logo_without_crop_hacks(self):
        for page in self.public_html:
            text = page.read_text(encoding="utf-8")
            if '<header class="site-header"' not in text:
                continue
            self.assertIn('assets/silwadi-logo-official.png', text, page.as_posix())
            self.assertNotIn('brand-crop', text, page.as_posix())
            self.assertNotIn('footer-logo-crop', text, page.as_posix())

    def test_home_services_use_verified_compact_treatment_paths(self):
        self.assertIn('class="treatment-paths"', self.home)
        for service in (
            "Implantology",
            "Orthodontics",
            "Periodontics",
            "Cosmetic Dentistry",
            "Preventive Treatments",
        ):
            self.assertIn(service, self.home)
        self.assertGreaterEqual(self.home.count('class="treatment-path reveal'), 5)
        self.assertIn('View all services', self.home)


if __name__ == "__main__":
    unittest.main()
