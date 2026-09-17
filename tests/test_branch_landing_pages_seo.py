from html.parser import HTMLParser
from pathlib import Path
import json
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PageSignals(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = None
        self.hreflang = {}
        self.h1 = []
        self._in_h1 = False
        self._h1_parts = []
        self.schemas = []
        self._in_schema = False
        self._schema_parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href")
        if tag == "link" and attrs.get("rel") == "alternate" and attrs.get("hreflang"):
            self.hreflang[attrs["hreflang"]] = attrs.get("href")
        if tag == "h1":
            self._in_h1 = True
            self._h1_parts = []
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self._in_schema = True
            self._schema_parts = []

    def handle_endtag(self, tag):
        if tag == "h1" and self._in_h1:
            self.h1.append("".join(self._h1_parts).replace("\xa0", " ").strip())
            self._in_h1 = False
        if tag == "script" and self._in_schema:
            source = "".join(self._schema_parts).strip()
            if source:
                self.schemas.append(json.loads(source))
            self._in_schema = False

    def handle_data(self, data):
        if self._in_h1:
            self._h1_parts.append(data)
        if self._in_schema:
            self._schema_parts.append(data)


def parse_page(path):
    parser = PageSignals()
    parser.feed((ROOT / path).read_text(encoding="utf-8"))
    return parser


def graph_nodes(page):
    nodes = []
    for schema in page.schemas:
        nodes.extend(schema.get("@graph", [schema]))
    return nodes


class BranchLandingPageSeoTests(unittest.TestCase):
    def test_homepage_primary_headings_state_abu_dhabi_dental_intent(self):
        self.assertEqual(parse_page("index.html").h1, ["Dental Care in Abu Dhabi."])
        self.assertEqual(parse_page("ar/index.html").h1, ["رعاية أسنان في أبوظبي"])

    def test_each_branch_has_a_dedicated_bilingual_indexable_page(self):
        expected = {
            "locations/corniche.html": (
                "https://silwadi.ae/locations/corniche.html",
                "https://silwadi.ae/ar/locations/corniche.html",
                "Dentist on Abu Dhabi Corniche",
            ),
            "locations/al-raha.html": (
                "https://silwadi.ae/locations/al-raha.html",
                "https://silwadi.ae/ar/locations/al-raha.html",
                "Dentist in Al Raha, Abu Dhabi",
            ),
            "ar/locations/corniche.html": (
                "https://silwadi.ae/ar/locations/corniche.html",
                "https://silwadi.ae/locations/corniche.html",
                "طبيب أسنان في كورنيش أبوظبي",
            ),
            "ar/locations/al-raha.html": (
                "https://silwadi.ae/ar/locations/al-raha.html",
                "https://silwadi.ae/locations/al-raha.html",
                "طبيب أسنان في الراحة، أبوظبي",
            ),
        }
        for path, (canonical, alternate, h1) in expected.items():
            with self.subTest(path=path):
                page = parse_page(path)
                self.assertEqual(page.canonical, canonical)
                self.assertEqual(page.h1, [h1])
                self.assertEqual(page.hreflang["x-default"], canonical if not path.startswith("ar/") else alternate)
                if path.startswith("ar/"):
                    self.assertEqual(page.hreflang["en-AE"], alternate)
                else:
                    self.assertEqual(page.hreflang["ar-AE"], alternate)

    def test_branch_schema_uses_the_public_business_profile_names_and_branch_urls(self):
        expected = {
            "locations/corniche.html": (
                "Dr Munir Silwadi Dental Centre - Corniche Branch",
                "https://silwadi.ae/locations/corniche.html",
                "+97126262042",
            ),
            "locations/al-raha.html": (
                "Al Raha Branch - Dr. Mohamed Munir Dental Centre - LLC",
                "https://silwadi.ae/locations/al-raha.html",
                "+97126662408",
            ),
        }
        for path, expected_branch in expected.items():
            with self.subTest(path=path):
                dentists = [n for n in graph_nodes(parse_page(path)) if n.get("@type") == "Dentist"]
                self.assertEqual(len(dentists), 1)
                self.assertEqual(
                    (dentists[0]["name"], dentists[0]["url"], dentists[0]["telephone"]),
                    expected_branch,
                )

    def test_branch_pages_are_linked_from_locations_and_listed_in_sitemap(self):
        locations = (ROOT / "locations.html").read_text(encoding="utf-8")
        arabic_locations = (ROOT / "ar/locations.html").read_text(encoding="utf-8")
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        for slug in ("corniche", "al-raha"):
            self.assertIn(f'href="/locations/{slug}.html"', locations)
            self.assertIn(f'href="/ar/locations/{slug}.html"', arabic_locations)
            self.assertIn(f"https://silwadi.ae/locations/{slug}.html", sitemap)
            self.assertIn(f"https://silwadi.ae/ar/locations/{slug}.html", sitemap)


if __name__ == "__main__":
    unittest.main()
