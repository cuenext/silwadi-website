from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "review" / "people-of-determination-raha-v1.html"
SELECTED_IMAGES = (
    "DSCF2857.webp",
    "DSCF2848.webp",
    "DSCF2860.webp",
    "DSCF2868.webp",
    "DSCF2873.webp",
    "DSCF2877.webp",
    "DSCF2880.webp",
)


class PeopleOfDeterminationGalleryContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")

    def test_review_page_uses_curated_seven_image_pod_gallery(self):
        refs = re.findall(r'\.\./assets/(DSCF\d+\.webp)', self.html)
        self.assertEqual(refs, list(SELECTED_IMAGES))
        slides = re.findall(r'<figure class="pod-clinic-slide[^>]*data-pod-slide', self.html)
        self.assertEqual(len(slides), 7)

    def test_selected_gallery_assets_exist(self):
        for filename in SELECTED_IMAGES:
            self.assertTrue((ROOT / "assets" / filename).exists(), filename)

    def test_gallery_is_integrated_into_hero_and_old_static_image_is_removed(self):
        hero = re.search(r'<section class="pod-hero".*?</section>', self.html, re.S)
        self.assertIsNotNone(hero)
        hero_html = hero.group(0)
        self.assertIn('data-pod-carousel', hero_html)
        self.assertIn('id="clinic"', hero_html)
        self.assertNotIn('<figure class="pod-hero__visual"', self.html)
        self.assertNotIn('al-raha-accessible-treatment-room-final.webp', self.html)
        self.assertNotIn('<section class="pod-clinic"', self.html)

    def test_partnership_section_markup_remains_valid(self):
        self.assertIn('<section class="pod-partnership" id="partnership">', self.html)
        self.assertNotIn('<section class="pod-partnership id=', self.html)

    def test_gallery_matches_pediatrics_carousel_contract(self):
        required_markers = (
            "--pod-slide-width",
            "pod-clinic-carousel",
            "data-pod-carousel",
            "data-pod-viewport",
            "data-pod-slide",
            "data-pod-current",
            "data-pod-prev",
            "data-pod-next",
            "scroll-snap-type:x mandatory",
            "cloneNode(true)",
            "SWIPE_THRESHOLD = 42",
            "prefers-reduced-motion: reduce",
        )
        for marker in required_markers:
            with self.subTest(marker=marker):
                self.assertIn(marker, self.html)

    def test_gallery_keeps_accessible_semantics_and_loading_hints(self):
        self.assertIn('aria-roledescription="carousel"', self.html)
        self.assertIn('aria-label="Accessible dental treatment room photos"', self.html)
        hero = re.search(r'<section class="pod-hero".*?</section>', self.html, re.S)
        self.assertIsNotNone(hero)
        hero_html = hero.group(0)
        self.assertEqual(hero_html.count('loading="lazy"'), 6)
        self.assertEqual(hero_html.count('fetchpriority="high"'), 1)
        self.assertIn('<span>07</span>', hero_html)


if __name__ == "__main__":
    unittest.main()
