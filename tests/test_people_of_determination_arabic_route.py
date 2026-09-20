from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / "treatments" / "people-of-determination.html"
AR = ROOT / "ar" / "treatments" / "people-of-determination.html"


class PeopleOfDeterminationArabicRouteContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.en = EN.read_text(encoding="utf-8")
        cls.ar = AR.read_text(encoding="utf-8")

    def test_english_pod_switches_point_to_exact_arabic_pod_page(self):
        target = 'href="/ar/treatments/people-of-determination.html"'
        self.assertGreaterEqual(self.en.count(target), 2)
        self.assertNotIn('class="global-language" href="/ar/services.html"', self.en)

    def test_arabic_pod_page_is_real_rtl_counterpart(self):
        self.assertIn('<html lang="ar" dir="rtl">', self.ar)
        self.assertIn('أصحاب الهمم', self.ar)
        self.assertIn('https://silwadi.ae/ar/treatments/people-of-determination.html', self.ar)
        self.assertIn('href="https://silwadi.ae/treatments/people-of-determination.html"', self.ar)

    def test_arabic_pod_page_never_routes_or_canonicalizes_to_endodontics(self):
        lowered = self.ar.lower()
        self.assertNotIn('endodontics.html', lowered)
        self.assertNotIn('/ar/treatments/endodontics', lowered)


if __name__ == "__main__":
    unittest.main()
