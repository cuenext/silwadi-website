"""Keep the emitted branch map pins attached to the correct clinic identity."""

from html.parser import HTMLParser
from pathlib import Path
import json
import unittest

from scripts.apply_google_authority import bani_entity, raha_entity, patch_home

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://silwadi.ae"
BRANCHES = {
    BASE + "/#dentist": (24.4935218, 54.3610125, "+97126262042", "Bani Yas Tower"),
    BASE + "/#dentist-al-raha": (24.4388317, 54.5744795, "+97126662408", "Al Raha Mall"),
    BASE + "/locations/corniche.html#dentist": (24.4935218, 54.3610125, "+97126262042", "Bani Yas Tower"),
    BASE + "/locations/al-raha.html#dentist": (24.4388317, 54.5744795, "+97126662408", "Al Raha Mall"),
}


class SchemaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.parts = None

    def handle_starttag(self, tag, attrs):
        if tag == "script" and dict(attrs).get("type") == "application/ld+json":
            self.parts = []

    def handle_data(self, data):
        if self.parts is not None:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.parts is not None:
            data = json.loads("".join(self.parts))
            self.nodes.extend(data.get("@graph", [data]))
            self.parts = None


def schema_nodes(path):
    parser = SchemaParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.nodes


class BranchGeoTest(unittest.TestCase):
    def assert_branch(self, node):
        latitude, longitude, phone, address = BRANCHES[node["@id"]]
        self.assertEqual(node["geo"], {
            "@type": "GeoCoordinates", "latitude": latitude, "longitude": longitude,
        })
        self.assertEqual(node["telephone"], phone)
        self.assertIn(address, node["address"]["streetAddress"])
        self.assertEqual(node["parentOrganization"], {"@id": BASE + "/#organization"})
        hours = node["openingHoursSpecification"]
        self.assertTrue(hours)
        self.assertTrue(all(item["opens"] and item["closes"] for item in hours))

    def test_branch_factory_emits_verified_map_pin_for_each_identity_and_locale(self):
        for locale in ("en", "ar"):
            for factory in (bani_entity, raha_entity):
                with self.subTest(locale=locale, factory=factory.__name__):
                    self.assert_branch(factory(locale))

    def test_every_public_branch_geo_resolves_to_the_correct_clinic(self):
        found = 0
        paths = list(ROOT.glob("*.html"))
        for folder in ("ar", "locations", "doctors", "treatments"):
            paths.extend((ROOT / folder).rglob("*.html"))
        for path in sorted(set(paths)):
            for node in schema_nodes(path):
                if node.get("@type") == "Dentist" and "geo" in node:
                    with self.subTest(path=path.relative_to(ROOT), branch=node["@id"]):
                        self.assertIn(node["@id"], BRANCHES)
                        self.assert_branch(node)
                    found += 1
        self.assertGreaterEqual(found, 16, "Expected homepage, hubs and branch-page clinic pins")

    def test_homepage_site_entity_exposes_full_brand_and_short_name(self):
        for relative in ("index.html", "ar/index.html"):
            nodes = schema_nodes(ROOT / relative)
            website = next(node for node in nodes if node.get("@id") == BASE + "/#website")
            with self.subTest(path=relative):
                self.assertEqual(website.get("alternateName"), ["Dr. Munir Silwadi Dental Centre", "Silwadi"])
                self.assertEqual(website["url"], BASE + "/")
                self.assertEqual(website["publisher"], {"@id": BASE + "/#organization"})

    def test_homepage_schema_helper_retains_site_names_when_updating_branches(self):
        website = {"@type": "WebSite", "@id": BASE + "/#website", "name": "Silwadi Dental Centres"}
        data = {"@graph": [website]}
        patch_home(data)
        self.assertEqual(website.get("alternateName"), ["Dr. Munir Silwadi Dental Centre", "Silwadi"])
        self.assertEqual(website["name"], "Silwadi Dental Centres")
        for node in data["@graph"]:
            if node.get("@id") in BRANCHES:
                self.assert_branch(node)


if __name__ == "__main__":
    unittest.main()
