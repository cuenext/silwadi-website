from pathlib import Path
from html.parser import HTMLParser
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    "doctors.html",
    "about.html",
    "locations.html",
    "contact.html",
    "treatments.html",
    "treatments/dental-implants.html",
    "treatments/orthodontics.html",
    "treatments/cosmetic-dentistry.html",
    "treatments/general-dentistry.html",
    "treatments/emergency-dentist.html",
]
TREATMENT_DETAIL_PAGES = [
    "treatments/dental-implants.html",
    "treatments/orthodontics.html",
    "treatments/cosmetic-dentistry.html",
    "treatments/general-dentistry.html",
    "treatments/emergency-dentist.html",
]
EXPECTED_OG_IMAGES = {
    "contact.html": "https://silwadi.ae/assets/locations/bani-yas-reception.webp",
    "treatments/dental-implants.html": "https://silwadi.ae/assets/services/implantology.webp",
    "treatments/orthodontics.html": "https://silwadi.ae/assets/services/orthodontics.webp",
    "treatments/cosmetic-dentistry.html": "https://silwadi.ae/assets/services/cosmetic-dentistry.webp",
}


class HeadParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self._in_title = False
        self.meta = {}
        self.links = []
        self._in_jsonld = False
        self._jsonld_parts = []
        self.jsonld = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            key = attrs.get("name") or attrs.get("property")
            if key and attrs.get("content") is not None:
                self.meta[key] = attrs["content"]
        elif tag == "link":
            self.links.append(attrs)
        elif tag == "script" and attrs.get("type") == "application/ld+json":
            self._in_jsonld = True
            self._jsonld_parts = []

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "script" and self._in_jsonld:
            raw = "".join(self._jsonld_parts).strip()
            if raw:
                self.jsonld.append(json.loads(raw))
            self._in_jsonld = False
            self._jsonld_parts = []

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_jsonld:
            self._jsonld_parts.append(data)


def parse(path):
    html = (ROOT / path).read_text(encoding="utf-8")
    parser = HeadParser()
    parser.feed(html)
    return html, parser


def graph_nodes(parser):
    nodes = []
    for block in parser.jsonld:
        if isinstance(block, dict) and isinstance(block.get("@graph"), list):
            nodes.extend(block["@graph"])
        else:
            nodes.append(block)
    return [node for node in nodes if isinstance(node, dict)]


def nodes_of_type(parser, schema_type):
    found = []
    for node in graph_nodes(parser):
        node_type = node.get("@type")
        types = node_type if isinstance(node_type, list) else [node_type]
        if schema_type in types:
            found.append(node)
    return found


def link_href(parser, rel=None, hreflang=None):
    for link in parser.links:
        rel_value = link.get("rel", "")
        if rel and rel not in rel_value.split():
            continue
        if hreflang and link.get("hreflang") != hreflang:
            continue
        return link.get("href")
    return None


class PublicCoreSeoContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parsed = {path: parse(path) for path in PAGES}

    def test_all_pages_are_indexable_and_have_unique_metadata(self):
        titles = []
        descriptions = []
        for path, (_, parser) in self.parsed.items():
            robots = parser.meta.get("robots", "")
            self.assertIn("index", robots, path)
            self.assertIn("follow", robots, path)
            self.assertTrue(parser.title.strip(), path)
            description = parser.meta.get("description", "").strip()
            self.assertTrue(description, path)
            titles.append(parser.title.strip())
            descriptions.append(description)
        self.assertEqual(len(titles), len(set(titles)), "titles must be unique across the 10 core pages")
        self.assertEqual(len(descriptions), len(set(descriptions)), "descriptions must be unique across the 10 core pages")

    def test_canonicals_open_graph_and_hreflang_are_consistent(self):
        for path, (_, parser) in self.parsed.items():
            canonical = f"https://silwadi.ae/{path}"
            arabic = f"https://silwadi.ae/ar/{path}"
            self.assertEqual(link_href(parser, rel="canonical"), canonical, path)
            self.assertEqual(parser.meta.get("og:url"), canonical, path)
            self.assertTrue(parser.meta.get("og:image", "").startswith("https://"), path)
            self.assertEqual(link_href(parser, rel="alternate", hreflang="en-AE"), canonical, path)
            self.assertEqual(link_href(parser, rel="alternate", hreflang="ar-AE"), arabic, path)
            self.assertEqual(link_href(parser, rel="alternate", hreflang="x-default"), canonical, path)

    def test_jsonld_blocks_are_valid_and_page_specific(self):
        for path, (_, parser) in self.parsed.items():
            self.assertTrue(parser.jsonld, f"{path}: expected JSON-LD")
            self.assertTrue(nodes_of_type(parser, "BreadcrumbList"), f"{path}: expected BreadcrumbList")

        doctors = self.parsed["doctors.html"][1]
        self.assertTrue(nodes_of_type(doctors, "CollectionPage"))
        doctor_lists = nodes_of_type(doctors, "ItemList")
        self.assertTrue(doctor_lists)
        self.assertGreaterEqual(len(doctor_lists[0].get("itemListElement", [])), 15)

        treatments = self.parsed["treatments.html"][1]
        self.assertTrue(nodes_of_type(treatments, "CollectionPage"))
        treatment_lists = nodes_of_type(treatments, "ItemList")
        self.assertTrue(treatment_lists)
        self.assertGreaterEqual(len(treatment_lists[0].get("itemListElement", [])), 10)

        locations = self.parsed["locations.html"][1]
        self.assertTrue(nodes_of_type(locations, "CollectionPage"))
        location_lists = nodes_of_type(locations, "ItemList")
        self.assertTrue(location_lists)
        self.assertGreaterEqual(len(location_lists[0].get("itemListElement", [])), 2)
        self.assertGreaterEqual(len(nodes_of_type(locations, "Dentist")), 2)

        contact = self.parsed["contact.html"][1]
        self.assertTrue(nodes_of_type(contact, "ContactPage"))
        self.assertGreaterEqual(len(nodes_of_type(contact, "Dentist")), 2)

        about = self.parsed["about.html"][1]
        self.assertTrue(nodes_of_type(about, "AboutPage"))

        for path in TREATMENT_DETAIL_PAGES:
            parser = self.parsed[path][1]
            self.assertTrue(nodes_of_type(parser, "Service"), f"{path}: expected Service schema")
            faqs = nodes_of_type(parser, "FAQPage")
            self.assertTrue(faqs, f"{path}: expected FAQPage schema")
            self.assertGreaterEqual(len(faqs[0].get("mainEntity", [])), 2, path)

    def test_selected_pages_use_relevant_open_graph_images(self):
        for path, expected in EXPECTED_OG_IMAGES.items():
            parser = self.parsed[path][1]
            self.assertEqual(parser.meta.get("og:image"), expected, path)

    def test_booking_links_use_canonical_consultation_form_anchor(self):
        for path, (html, _) in self.parsed.items():
            self.assertNotIn('href="contact.html#consultation"', html, path)
            self.assertNotIn('href="../contact.html#consultation"', html, path)


if __name__ == "__main__":
    unittest.main()
