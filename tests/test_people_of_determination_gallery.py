from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "review" / "people-of-determination-raha-v1.html"
SELECTED_IMAGES = (
    "DSCF2857.webp",
    "DSCF2868.webp",
    "DSCF2880.webp",
)


class PeopleOfDeterminationGalleryContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")

    def test_review_page_uses_a_minimal_three_image_pod_gallery(self):
        refs = re.findall(r'\.\./assets/(DSCF\d+\.webp)', self.html)
        self.assertEqual(refs, list(SELECTED_IMAGES))

    def test_selected_gallery_assets_exist(self):
        for filename in SELECTED_IMAGES:
            self.assertTrue((ROOT / "assets" / filename).exists(), filename)

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
        self.assertEqual(self.html.count('data-pod-slide'), 3)
        self.assertEqual(self.html.count('loading="lazy"'), 5)  # two existing page images + gallery slides 2 and 3
        self.assertIn('fetchpriority="high"', self.html)


if __name__ == "__main__":
    unittest.main()
