from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ApprovedTreatmentPagesLiveTests(unittest.TestCase):
    def read(self, relative):
        return (ROOT / relative).read_text(encoding="utf-8")

    def assert_public_page(self, relative, canonical, markers):
        html = self.read(relative)
        self.assertRegex(html, r'<meta name="robots" content="index,follow[^\"]*">')
        self.assertIn(f'<link rel="canonical" href="{canonical}">', html)
        self.assertNotIn('Private review', html)
        self.assertNotIn('Not published', html)
        self.assertNotIn('<div class="private-note">', html)
        for marker in markers:
            self.assertIn(marker, html)
        return html

    def test_pediatric_review_is_live(self):
        self.assert_public_page(
            "treatments/pediatric-dentistry.html",
            "https://silwadi.ae/treatments/pediatric-dentistry.html",
            [
                "Al Raha Mall · Pediatric Clinic",
                "Dr. Kashmira Pawar Jayprakash",
                "data-pd-carousel",
            ],
        )

    def test_endodontics_review_is_live(self):
        self.assert_public_page(
            "treatments/endodontics.html",
            "https://silwadi.ae/treatments/endodontics.html",
            [
                "Root Canal Treatment in",
                "Dr. Ahmed El Shehri",
                "Dr. Lana Almasoud",
                "/assets/services/endodontics.webp?v=20260915-review-hero",
            ],
        )

    def test_people_of_determination_review_is_live(self):
        html = self.assert_public_page(
            "treatments/people-of-determination.html",
            "https://silwadi.ae/treatments/people-of-determination.html",
            [
                "Dental Care for People of Determination",
                "Official Partnership with Zayed Authority for People of Determination",
                "data-pod-carousel",
                "Al Raha Mall branch",
            ],
        )
        self.assertIn('data-seo-schema', html)
        self.assertIn('og:title', html)

    def test_sitemap_contains_all_three_live_pages(self):
        sitemap = self.read("sitemap.xml")
        for url in [
            "https://silwadi.ae/treatments/pediatric-dentistry.html",
            "https://silwadi.ae/treatments/endodontics.html",
            "https://silwadi.ae/treatments/people-of-determination.html",
        ]:
            self.assertEqual(sitemap.count(f"<loc>{url}</loc>"), 1)

    def test_pod_is_discoverable_from_treatment_directory(self):
        directory = self.read("treatments.html")
        self.assertIn('href="treatments/people-of-determination.html"', directory)
        self.assertIn('People of Determination', directory)
        self.assertIn('"numberOfItems":11', directory)
        self.assertIn('<strong>11 service areas</strong>', directory)

    def test_review_sources_remain_private(self):
        for relative in [
            "review/pediatric-dentistry-v1.html",
            "review/endodontics-v4.html",
            "review/people-of-determination-raha-v1.html",
        ]:
            html = self.read(relative)
            self.assertIn('noindex', html)


if __name__ == "__main__":
    unittest.main()
