from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets" / "locations"
HTML = (ROOT / "locations.html").read_text(encoding="utf-8")
CSS = (ROOT / "location-pages.css").read_text(encoding="utf-8")


class LocationsPageTests(unittest.TestCase):
    def test_locations_stylesheet_is_cache_busted(self):
        self.assertRegex(HTML, r'href="location-pages\.css\?v=[^"]+"')

    def test_both_branches_have_distinct_section_ids_without_live_status_badges(self):
        self.assertIn('id="bani-yas"', HTML)
        self.assertIn('id="al-raha"', HTML)
        self.assertNotIn('class="location-state"', HTML)

    def test_bani_yas_uses_the_approved_corniche_clinic_photo(self):
        match = re.search(r'<section[^>]*id="bani-yas".*?</section>', HTML, re.S)
        self.assertIsNotNone(match)
        bani_yas = match.group(0)
        self.assertIn('assets/locations/bani-yas-treatment-room.webp', bani_yas)
        self.assertIn('width="1200" height="740"', bani_yas)

    def test_al_raha_exterior_belongs_to_branch_section_and_gallery_has_four_interior_images(self):
        match = re.search(r'<section[^>]*id="al-raha".*?</section>', HTML, re.S)
        self.assertIsNotNone(match)
        al_raha = match.group(0)
        self.assertIn('assets/locations/al-raha-exterior.webp', al_raha)
        self.assertIn('width="1100" height="814"', al_raha)

        gallery = re.search(r'<section[^>]*class="[^"]*branch-gallery[^"]*".*?</section>', HTML, re.S)
        self.assertIsNotNone(gallery)
        gallery_html = gallery.group(0)
        self.assertNotIn('al-raha-exterior.webp', gallery_html)
        expected_gallery = {
            'al-raha-treatment-room.webp': 'width="900" height="658"',
            'al-raha-reception.webp': 'width="900" height="652"',
            'al-raha-children-room.webp': 'width="900" height="653"',
            'al-raha-waiting-area.webp': 'width="900" height="652"',
        }
        for filename, dimensions in expected_gallery.items():
            self.assertIn(filename, gallery_html)
            self.assertIn(dimensions, gallery_html)
            self.assertRegex(gallery_html, re.escape(filename) + r'\?v=[^" ]+')

        for old_png in (
            'al-raha-exterior.png',
            'al-raha-treatment-room.png',
            'al-raha-reception.png',
            'al-raha-children-room.png',
            'al-raha-waiting-area.png',
        ):
            self.assertNotIn(old_png, HTML)

    def test_location_image_assets_are_complete_webps(self):
        expected = (
            'bani-yas-treatment-room.webp',
            'al-raha-exterior.webp',
            'al-raha-treatment-room.webp',
            'al-raha-reception.webp',
            'al-raha-children-room.webp',
            'al-raha-waiting-area.webp',
        )
        for filename in expected:
            path = ASSET_DIR / filename
            self.assertTrue(path.is_file(), filename)
            self.assertGreater(path.stat().st_size, 25_000, filename)
            header = path.read_bytes()[:12]
            self.assertEqual(header[:4], b'RIFF', filename)
            self.assertEqual(header[8:12], b'WEBP', filename)

    def test_official_al_raha_videos_are_present(self):
        self.assertIn('INb7BccskzU', HTML)
        self.assertIn('34mCABC8yTs', HTML)

    def test_al_raha_has_reception_led_ctas(self):
        match = re.search(r'<section[^>]*id="al-raha".*?</section>', HTML, re.S)
        self.assertIsNotNone(match)
        al_raha = match.group(0)
        self.assertIn('Book a Consultation', al_raha)
        self.assertIn('tel:+97126662408', al_raha)
        self.assertIn('Get Directions', al_raha)

    def test_gallery_uses_compact_landscape_frames_on_desktop_and_mobile(self):
        self.assertIn('grid-template-columns:repeat(2,minmax(0,1fr))', CSS)
        self.assertRegex(CSS, r'\.branch-gallery__grid\{[^}]*max-width:980px[^}]*margin-inline:auto')
        self.assertRegex(CSS, r'\.branch-gallery__item img\{[^}]*height:clamp\(190px,22vw,280px\)[^}]*object-fit:cover')
        self.assertRegex(CSS, r'@media\(max-width:620px\).*?\.branch-gallery__grid\{grid-template-columns:1fr', re.S)
        self.assertRegex(CSS, r'@media\(max-width:620px\).*?\.branch-gallery__item img\{height:210px', re.S)

    def test_locations_rtl_rules_exist(self):
        self.assertIn('html[dir="rtl"] body.language-ar .location-branch', CSS)
        self.assertIn('html[dir="rtl"] body.language-ar .branch-gallery', CSS)

    def test_existing_seo_and_language_hooks_are_preserved(self):
        self.assertIn('<link rel="canonical" href="https://silwadi.ae/locations.html">', HTML)
        self.assertIn('hreflang="ar-AE"', HTML)
        self.assertIn('data-seo-schema', HTML)
        self.assertIn('<script src="language.js"></script>', HTML)


if __name__ == '__main__':
    unittest.main()
