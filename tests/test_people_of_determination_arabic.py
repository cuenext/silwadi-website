from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
ENGLISH_PAGE = ROOT / "treatments" / "people-of-determination.html"
ARABIC_PAGE = ROOT / "ar" / "treatments" / "people-of-determination.html"
SITEMAP = ROOT / "sitemap.xml"


class PeopleOfDeterminationArabicContract(unittest.TestCase):
    def test_arabic_pod_page_exists_and_is_really_pod(self):
        self.assertTrue(ARABIC_PAGE.exists(), "Arabic POD page is missing")
        html = ARABIC_PAGE.read_text(encoding="utf-8")
        self.assertIn('<html lang="ar" dir="rtl">', html)
        self.assertIn("أصحاب الهمم", html)
        self.assertIn("رعاية أسنان أصحاب الهمم", html)
        self.assertNotIn("علاج جذور الأسنان في أبوظبي", html)
        self.assertIn('href="/treatments/people-of-determination.html"', html)

    def test_english_pod_language_switch_targets_exact_arabic_counterpart(self):
        html = ENGLISH_PAGE.read_text(encoding="utf-8")
        target = '/ar/treatments/people-of-determination.html'
        self.assertGreaterEqual(html.count(target), 2)
        self.assertNotIn('class="global-language" href="/ar/services.html"', html)

    def test_arabic_pod_preserves_current_seven_photo_gallery(self):
        html = ARABIC_PAGE.read_text(encoding="utf-8")
        for filename in (
            "DSCF2857.webp",
            "DSCF2848.webp",
            "DSCF2860.webp",
            "DSCF2868.webp",
            "DSCF2873.webp",
            "DSCF2877.webp",
            "DSCF2880.webp",
        ):
            self.assertIn(f'/assets/{filename}', html)
        self.assertIn('<span>07</span>', html)

    def test_arabic_pod_is_in_sitemap(self):
        sitemap = SITEMAP.read_text(encoding="utf-8")
        self.assertIn(
            "https://silwadi.ae/ar/treatments/people-of-determination.html",
            sitemap,
        )


if __name__ == "__main__":
    unittest.main()
