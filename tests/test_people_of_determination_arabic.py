from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / 'treatments' / 'people-of-determination.html'
AR = ROOT / 'ar' / 'treatments' / 'people-of-determination.html'

class PodArabic(unittest.TestCase):
    def test_exact_counterparts_exist(self):
        self.assertTrue(AR.exists())
        en = EN.read_text(encoding='utf-8')
        ar = AR.read_text(encoding='utf-8')
        self.assertIn('/ar/treatments/people-of-determination.html', en)
        self.assertIn('https://silwadi.ae/treatments/people-of-determination.html', ar)
        self.assertIn('<html lang="ar" dir="rtl">', ar)
        self.assertIn('أصحاب الهمم', ar)
        self.assertIn('رعاية أسنان أصحاب الهمم', ar)
        self.assertNotIn('علاج جذور الأسنان في أبوظبي', ar)

    def test_gallery_is_preserved(self):
        ar = AR.read_text(encoding='utf-8')
        for name in ('DSCF2857.webp','DSCF2848.webp','DSCF2860.webp','DSCF2868.webp','DSCF2873.webp','DSCF2877.webp','DSCF2880.webp'):
            self.assertIn(name, ar)
        self.assertIn('<span>07</span>', ar)

    def test_sitemap_contains_arabic_pod(self):
        sitemap = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
        self.assertIn('https://silwadi.ae/ar/treatments/people-of-determination.html', sitemap)

if __name__ == '__main__': unittest.main()
