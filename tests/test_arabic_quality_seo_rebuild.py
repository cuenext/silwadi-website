from pathlib import Path
import json
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SEO = json.loads((ROOT / "data" / "arabic-seo.json").read_text(encoding="utf-8"))


def english_url(route: str) -> str:
    return "https://silwadi.ae/" if route == "index.html" else f"https://silwadi.ae/{route}"


def arabic_url(route: str) -> str:
    return "https://silwadi.ae/ar/" if route == "index.html" else f"https://silwadi.ae/ar/{route}"


class ArabicQualitySeoRebuild(unittest.TestCase):
    def test_every_patient_route_has_static_arabic_html(self):
        self.assertGreaterEqual(len(SEO), 27)
        for route in SEO:
            target = ROOT / "ar" / route
            self.assertTrue(target.exists(), f"Missing Arabic page: {target.relative_to(ROOT)}")

    def test_arabic_pages_have_real_arabic_metadata_and_language_attributes(self):
        for route, metadata in SEO.items():
            source = (ROOT / "ar" / route).read_text(encoding="utf-8")
            self.assertRegex(source, r'<html[^>]*\blang="ar"[^>]*\bdir="rtl"|<html[^>]*\bdir="rtl"[^>]*\blang="ar"', route)
            self.assertIn(f'<title>{metadata["title"]}</title>', source, route)
            self.assertRegex(metadata["title"], r"[\u0600-\u06ff]", route)
            self.assertRegex(metadata["description"], r"[\u0600-\u06ff]", route)
            self.assertIn(f'href="{arabic_url(route)}"', source, route)
            self.assertIn(f'hreflang="ar-AE" href="{arabic_url(route)}"', source, route)
            self.assertIn(f'hreflang="en-AE" href="{english_url(route)}"', source, route)
            self.assertIn(f'hreflang="x-default" href="{english_url(route)}"', source, route)
            self.assertNotIn("?lang=ar", source, route)

    def test_english_pages_point_to_static_arabic_counterparts(self):
        for route in SEO:
            source = (ROOT / route).read_text(encoding="utf-8")
            self.assertIn(f'hreflang="ar-AE" href="{arabic_url(route)}"', source, route)
            self.assertIn(f'hreflang="en-AE" href="{english_url(route)}"', source, route)
            self.assertIn(f'hreflang="x-default" href="{english_url(route)}"', source, route)
            self.assertIn('/bilingual-routing.js', source, route)
            self.assertIn('/arabic-quality.css', source, route)

    def test_google_reviews_never_reverse_when_arabic_is_selected(self):
        css = (ROOT / "home-reviews.css").read_text(encoding="utf-8")
        reverse_rule = re.compile(r"\.language-ar\s+\.google-reviews-track\s*\{[^}]*animation-direction\s*:\s*reverse", re.S)
        self.assertIsNone(reverse_rule.search(css))
        quality = (ROOT / "arabic-quality.css").read_text(encoding="utf-8")
        self.assertIn(".google-reviews-track{animation-direction:normal!important}", quality)

    def test_homepage_arabic_trust_copy_is_condensed(self):
        source = (ROOT / "ar" / "index.html").read_text(encoding="utf-8")
        trust = re.search(r'<ul[^>]*class="[^"]*premium-home-hero__trust[^"]*"[^>]*>(.*?)</ul>', source, re.S)
        self.assertIsNotNone(trust)
        block = trust.group(1)
        self.assertNotIn("<br", block.lower())
        self.assertNotRegex(block, r">\s*الحجز\s*<")

    def test_mobile_hero_uses_separate_image_and_copy_panel(self):
        css = (ROOT / "arabic-quality.css").read_text(encoding="utf-8")
        self.assertIn("grid-template-rows:minmax(330px,48svh) auto!important", css)
        self.assertIn(".premium-home-hero__media{position:relative!important", css)
        self.assertIn(".premium-home-hero__shade,.premium-home-hero::before{display:none!important}", css)

    def test_homepage_index_redirect_does_not_capture_arabic_index(self):
        app = (ROOT / "app.js").read_text(encoding="utf-8")
        self.assertIn("pathname === '/index.html'", app)
        self.assertNotIn("/\\/index\\.html$/.test(pathname)", app)

    def test_sitemap_contains_every_arabic_route(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        for route in SEO:
            self.assertIn(f"<loc>{arabic_url(route)}</loc>", sitemap, route)

    def test_core_arabic_ui_phrases_are_professional_and_compact(self):
        overrides = json.loads((ROOT / "data" / "arabic-quality-overrides.json").read_text(encoding="utf-8"))
        expected = {
            "Book an Appointment": "احجز موعداً",
            "Explore Services": "استكشف الخدمات",
            "Appointments via reception": "الحجز عبر الاستقبال",
            "Get Directions": "الاتجاهات",
            "Not sure which dentist to choose?": "لست متأكداً من الطبيب المناسب؟",
        }
        for english, arabic in expected.items():
            self.assertEqual(overrides.get(english), arabic)

    def test_audit_file_contains_no_untranslated_core_ui_copy(self):
        audit_path = ROOT / "data" / "arabic-audit.json"
        self.assertTrue(audit_path.exists())
        rows = json.loads(audit_path.read_text(encoding="utf-8"))
        core_terms = re.compile(r"\b(book|appointment|doctor|service|treatment|contact|location|call|whatsapp|directions|team|care|clinic|centre|center|about|home)\b", re.I)
        offenders = [row["source"] for row in rows if row["source"] == row["arabic"] and core_terms.search(row["source"])]
        self.assertEqual(offenders, [], f"Untranslated core UI copy: {offenders[:20]}")


if __name__ == "__main__":
    unittest.main()
