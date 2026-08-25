from pathlib import Path
import html as html_lib
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

SERVICES = [
    "Prosthodontics & Implantology",
    "Periodontics",
    "Endodontics",
    "Orthodontics",
    "Pedodontics",
    "Cosmetics",
    "Teeth Whitening",
    "Laser Dentistry",
    "Preventive Dentistry",
]

class Patch18ServicesAboutImagery(unittest.TestCase):
    def read(self, name):
        return (ROOT / name).read_text(encoding="utf-8")

    def test_services_page_has_nine_image_led_services_and_learn_more_links(self):
        html = self.read("services.html")
        rendered = html_lib.unescape(html)
        for service in SERVICES:
            self.assertIn(service, rendered)
            self.assertIn(f'aria-label="Learn more about {service}"', rendered)
            self.assertIn(f'>Learn More about {service}</a>', rendered)
        self.assertGreaterEqual(html.count('class="service-card'), 9)
        self.assertGreaterEqual(html.count('class="service-card__image'), 9)
        self.assertGreaterEqual(html.count('Learn More'), 9)
        self.assertIn('application/ld+json', html)
        self.assertIn('"@type":"Service"', html)

    def test_primary_navigation_exposes_services_sitewide(self):
        pages = [p for p in ROOT.rglob("*.html") if "/.git/" not in str(p)]
        self.assertGreater(len(pages), 10)
        missing = []
        for page in pages:
            text = page.read_text(encoding="utf-8")
            nav_match = re.search(r'<nav class="site-nav".*?</nav>', text, re.S)
            if nav_match and not re.search(r'href="(?:\.\./)?services\.html"[^>]*>Services(?:\s|<)', nav_match.group(0)):
                missing.append(str(page.relative_to(ROOT)))
        self.assertEqual([], missing)

    def test_home_keeps_approved_identity_and_adds_restrained_service_imagery(self):
        html = self.read("index.html")
        self.assertIn("Advanced dentistry.", html)
        self.assertIn("Established trust.", html)
        self.assertIn('href="home-trust.css"', html)
        self.assertNotIn('href="home-premium.css"', html)
        self.assertIn('class="home-service-visuals', html)
        images = re.findall(r'<div class="home-service-visuals[^>]*>[\s\S]*?</div>', html)
        self.assertTrue(images)
        self.assertGreaterEqual(images[0].count('assets/services/'), 3)

    def test_google_review_cards_show_individual_star_rows(self):
        html = self.read("index.html")
        cards = re.findall(r'<article class="google-review-card.*?</article>', html, re.S)
        self.assertGreaterEqual(len(cards), 3)
        for card in cards:
            self.assertIn('review-stars', card)
            self.assertRegex(card, r'aria-label="[1-5] out of 5 stars"')

    def test_stale_al_hilal_bank_landmark_is_removed_everywhere(self):
        offenders = []
        for page in ROOT.rglob("*.html"):
            text = page.read_text(encoding="utf-8")
            if "Al Hilal Bank" in text:
                offenders.append(str(page.relative_to(ROOT)))
        self.assertEqual([], offenders)

    def test_about_is_about_silwadi_and_uses_multiple_relevant_images(self):
        html = self.read("about.html")
        required = [
            "since 1980",
            "multi-specialty",
            "12 dentists",
            "Bani Yas Tower",
            "Al Raha Mall",
            "Dr. Munir Silwadi",
            "prosthodontics",
            "implantology",
        ]
        lower = html.lower()
        for phrase in required:
            self.assertIn(phrase.lower(), lower)
        main = re.search(r'<main.*?</main>', html, re.S).group(0)
        self.assertGreaterEqual(main.count('<img '), 4)
        self.assertNotIn('Questions are welcome.', html)
        self.assertNotIn('<h3>Ask</h3>', html)

    def test_service_images_are_local_optimized_assets(self):
        html = self.read("services.html")
        paths = re.findall(r'<img[^>]+src="(assets/services/[^"]+\.webp)"', html)
        self.assertGreaterEqual(len(set(paths)), 9)
        for rel in set(paths):
            path = ROOT / rel
            self.assertTrue(path.exists(), rel)
            self.assertLess(path.stat().st_size, 450_000, rel)

if __name__ == "__main__":
    unittest.main()
