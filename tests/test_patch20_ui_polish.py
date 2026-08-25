from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Patch20UiPolish(unittest.TestCase):
    def read(self, path):
        return (ROOT / path).read_text(encoding="utf-8")

    def test_top_utility_strip_is_removed_from_public_pages(self):
        for path in ROOT.rglob("*.html"):
            if any(part in {"tests", "node_modules"} for part in path.parts):
                continue
            html = path.read_text(encoding="utf-8")
            self.assertNotIn('class="utility-strip"', html, str(path.relative_to(ROOT)))

    def test_home_service_rows_each_have_a_thumbnail_and_old_three_image_strip_is_gone(self):
        html = self.read("index.html")
        self.assertNotIn('class="home-service-visuals', html)
        treatment_section = html.split('id="treatments"', 1)[1].split('id="legacy"', 1)[0]
        rows = re.findall(r'<a class="treatment-path[^>]*>.*?</a>', treatment_section, flags=re.S)
        self.assertEqual(len(rows), 5)
        for row in rows:
            self.assertIn('class="treatment-path__thumb"', row)
            self.assertRegex(row, r'<img[^>]+assets/services/[^>]+\.webp')

    def test_review_stars_are_gold_and_reviews_have_stronger_visual_emphasis(self):
        css = self.read("home-reviews.css")
        self.assertRegex(css, r'\.review-stars\{[^}]*color:#(?:f4b400|f5b301|f7b500|ffb800)', "individual review stars must be visibly gold")
        self.assertRegex(css, r'\.google-rating-card__stars\{[^}]*color:#(?:f4b400|f5b301|f7b500|ffb800)', "rating summary stars must be visibly gold")
        self.assertIn('.google-review-card:hover', css)
        self.assertIn('box-shadow:', css)

    def test_abu_dhabi_headings_keep_city_name_together(self):
        for page in ("index.html", "about.html", "services.html", "locations.html"):
            html = self.read(page)
            headings = re.findall(r'<h[12][^>]*>.*?</h[12]>', html, flags=re.S)
            for heading in headings:
                if "Abu Dhabi" in re.sub(r'<[^>]+>', '', heading):
                    self.assertIn('<span class="nowrap-place">Abu Dhabi</span>', heading, f"{page}: {heading}")
        css = self.read("styles.css")
        self.assertRegex(css, r'\.nowrap-place\{[^}]*white-space:nowrap')

    def test_about_page_uses_no_repeated_main_images(self):
        html = self.read("about.html")
        self.assertEqual(html.count('assets/doctors/optimized/dr-munir-silwadi.webp'), 1)
        main = re.search(r'<main.*?</main>', html, flags=re.S).group(0)
        sources = re.findall(r'<img[^>]+src="([^"]+)"', main)
        self.assertGreaterEqual(len(sources), 7)
        self.assertEqual(len(sources), len(set(sources)), sources)

    def test_services_mega_menu_uses_glass_cards_without_option_arrows(self):
        html = self.read("index.html")
        mega = html.split('class="services-mega"', 1)[1].split('</div></div></div><a href="doctors.html"', 1)[0]
        self.assertNotIn('<b aria-hidden="true">→</b>', mega)
        css = self.read("styles.css")
        self.assertRegex(css, r'\.services-mega__grid>a\{[^}]*border-radius:')
        self.assertRegex(css, r'\.services-mega__grid>a\{[^}]*backdrop-filter:blur')
        self.assertIn('.services-mega__grid>a::before', css)
        self.assertIn('.services-mega__grid>a:hover::before', css)
        self.assertIn('.services-mega__grid>a:active', css)

    def test_service_microinteractions_respect_reduced_motion(self):
        css = self.read("styles.css")
        self.assertIn('@media(prefers-reduced-motion:reduce)', css)
        self.assertIn('.services-mega__grid>a', css)
        reviews = self.read("home-reviews.css")
        self.assertIn('@media(prefers-reduced-motion:reduce)', reviews)


if __name__ == "__main__":
    unittest.main()
