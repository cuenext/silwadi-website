from pathlib import Path
import json
import re
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET


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
            self.assertIn('data-arabic-page-schema', source, route)
            self.assertIn('"inLanguage":"ar-AE"', source, route)
            self.assertIn('/arabic-static.js', source, route)

    def test_english_pages_point_to_static_arabic_counterparts(self):
        for route in SEO:
            source = (ROOT / route).read_text(encoding="utf-8")
            self.assertIn(f'hreflang="ar-AE" href="{arabic_url(route)}"', source, route)
            self.assertIn(f'hreflang="en-AE" href="{english_url(route)}"', source, route)
            self.assertIn(f'hreflang="x-default" href="{english_url(route)}"', source, route)
            self.assertIn('/bilingual-routing.js', source, route)
            self.assertIn('/arabic-quality.css', source, route)

    def test_google_reviews_never_reverse_or_reload_when_arabic_is_selected(self):
        css = (ROOT / "home-reviews.css").read_text(encoding="utf-8")
        reverse_rule = re.compile(r"\.language-ar\s+\.google-reviews-track\s*\{[^}]*animation-direction\s*:\s*reverse", re.S)
        self.assertIsNone(reverse_rule.search(css))
        quality = (ROOT / "arabic-quality.css").read_text(encoding="utf-8")
        self.assertIn(".google-reviews-track{animation-direction:normal!important}", quality)

        routing = (ROOT / "bilingual-routing.js").read_text(encoding="utf-8")
        self.assertIn("api.applyLanguage(next)", routing)
        self.assertIn("window.history.replaceState", routing)
        self.assertIn("Google Reviews track element and its current animation position", routing)
        self.assertNotIn("window.location.assign(`${target}", routing)

    def test_homepage_arabic_hero_and_trust_copy_are_clean_and_not_repeated(self):
        source = (ROOT / "ar" / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="premiumHomeHeroTitle">كيف يمكننا مساعدتك؟</h1>', source)
        self.assertNotIn('كيف يمكننا <span>مساعدتك؟</span>', source)
        self.assertNotIn('الحجز عبر الاستقبال الحجز', source)
        self.assertIn('<strong>نخدم مرضانا منذ عام 1980</strong>', source)
        self.assertIn('<strong>برج بني ياس والراحة مول</strong>', source)
        self.assertIn('<strong>الحجز عبر الاستقبال</strong>', source)

        trust = re.search(r'<ul[^>]*class="[^"]*premium-home-hero__trust[^"]*"[^>]*>(.*?)</ul>', source, re.S)
        self.assertIsNotNone(trust)
        self.assertNotIn("<br", trust.group(1).lower())

    def test_mobile_hero_uses_separate_image_and_copy_panel(self):
        css = (ROOT / "arabic-quality.css").read_text(encoding="utf-8")
        self.assertIn("grid-template-rows:minmax(330px,48svh) auto!important", css)
        self.assertIn(".premium-home-hero__media{position:relative!important", css)
        self.assertIn(".premium-home-hero__shade,.premium-home-hero::before{display:none!important}", css)

    def test_about_and_services_fragmented_headings_are_rewritten_as_complete_arabic(self):
        about = (ROOT / "ar" / "about.html").read_text(encoding="utf-8")
        self.assertIn('اسم راسخ في طب الأسنان بأبوظبي.', about)
        self.assertIn('افتُتح مركز سلوادي لطب الأسنان في أبوظبي.', about)
        self.assertIn('يقدم أطباؤنا العامون والاختصاصيون الرعاية للعائلات في فرعين.', about)

        services = (ROOT / "ar" / "services.html").read_text(encoding="utf-8")
        self.assertIn('خدمات طب الأسنان لكل ابتسامة في أبوظبي.', services)

    def test_no_generated_arabic_page_uses_inconsistent_brand_spelling(self):
        for route in SEO:
            source = (ROOT / "ar" / route).read_text(encoding="utf-8")
            self.assertNotIn('السلوادي', source, route)

    def test_generated_arabic_ctas_do_not_embed_directional_arrow_text(self):
        for route in SEO:
            source = (ROOT / "ar" / route).read_text(encoding="utf-8")
            body = source.split('<body', 1)[-1]
            visible_without_scripts = re.sub(r'<script[\s\S]*?</script>', '', body, flags=re.I)
            self.assertNotRegex(visible_without_scripts, r'[\u0600-\u06ff][^<]{0,80}[←→]', route)

    def test_homepage_index_redirect_does_not_capture_arabic_index(self):
        app = (ROOT / "app.js").read_text(encoding="utf-8")
        self.assertIn("pathname === '/index.html'", app)
        self.assertNotIn("/\\/index\\.html$/.test(pathname)", app)

    def test_sitemap_contains_every_arabic_route(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        for route in SEO:
            self.assertIn(f"<loc>{arabic_url(route)}</loc>", sitemap, route)

    def test_sitemap_has_complete_bilingual_pairs_and_lastmod(self):
        root = ET.fromstring((ROOT / "sitemap.xml").read_text(encoding="utf-8"))
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        nodes = root.findall("sm:url", ns)
        self.assertEqual(len(nodes), len(SEO) * 2)

        expected = {english_url(route) for route in SEO} | {arabic_url(route) for route in SEO}
        actual = set()
        for node in nodes:
            loc = node.find("sm:loc", ns)
            lastmod = node.find("sm:lastmod", ns)
            self.assertIsNotNone(loc)
            self.assertIsNotNone(lastmod, loc.text if loc is not None else "missing URL")
            self.assertRegex(lastmod.text or "", r"^\d{4}-\d{2}-\d{2}$")
            actual.add(loc.text)
        self.assertEqual(actual, expected)

    def test_launch_audit_understands_current_bilingual_architecture(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "seo_launch_audit.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SEO launch audit: 54 pages, 0 errors", result.stdout)

    def test_core_arabic_ui_phrases_are_professional_and_compact(self):
        layers = {}
        for filename in (
            "arabic-quality-overrides.json",
            "arabic-quality-overrides-extra.json",
            "arabic-quality-overrides-critical.json",
        ):
            layers.update(json.loads((ROOT / "data" / filename).read_text(encoding="utf-8")))
        expected = {
            "Book an Appointment": "احجز موعداً",
            "Explore Services": "استكشف الخدمات",
            "Appointments via reception": "الحجز عبر الاستقبال",
            "Get Directions": "الاتجاهات",
            "Not sure which dentist to choose?": "لست متأكداً من الطبيب المناسب؟",
            "Clinical base": "الفرع",
            "Can adults have orthodontic treatment?": "هل يمكن للبالغين الخضوع لتقويم الأسنان؟",
        }
        for english, arabic in expected.items():
            self.assertEqual(layers.get(english), arabic)

    def test_audit_file_contains_no_untranslated_core_ui_copy(self):
        audit_path = ROOT / "data" / "arabic-audit.json"
        self.assertTrue(audit_path.exists())
        rows = json.loads(audit_path.read_text(encoding="utf-8"))
        core_terms = re.compile(r"\b(book|appointment|doctor|service|treatment|contact|location|call|whatsapp|directions|team|care|clinic|centre|center|about|home)\b", re.I)
        offenders = [row["source"] for row in rows if row["source"] == row["arabic"] and core_terms.search(row["source"])]
        self.assertEqual(offenders, [], f"Untranslated core UI copy: {offenders[:20]}")

    def test_audit_has_no_repeated_booking_phrase_or_brand_variant(self):
        audit = (ROOT / "data" / "arabic-audit-compact.tsv").read_text(encoding="utf-8")
        self.assertNotIn('الحجز عبر الاستقبال الحجز', audit)
        self.assertNotIn('السلوادي', audit)


if __name__ == "__main__":
    unittest.main()
