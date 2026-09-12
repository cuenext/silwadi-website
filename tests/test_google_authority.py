from pathlib import Path
import json
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://silwadi.ae"
ORG_ID = f"{BASE}/#organization"
BANI_ID = f"{BASE}/#dentist"
RAHA_ID = f"{BASE}/#dentist-al-raha"
WEBSITE_ID = f"{BASE}/#website"
ALLOWED_BRANCH_IDS = {BANI_ID, RAHA_ID}

DOCTOR_FILES = [
    "dr-munir-silwadi.html",
    "dr-moheb-silwadi.html",
    "dr-hani-hasbini.html",
    "dr-moammar-rifai.html",
    "dr-ahmed-el-shehri.html",
    "dr-fahed-khalil.html",
    "dr-afnan-mashal.html",
    "dr-krishnamurthy-katta-balajee.html",
    "dr-ehab-hassouneh.html",
    "dr-sara-ismail.html",
    "dr-nasr-keshkiea.html",
    "dr-dana-awad.html",
    "dr-kashmira-pawar-jayprakash.html",
    "dr-nachiket-shah.html",
    "dr-lana-masoud.html",
]

PAIR_FILES = [
    "index.html", "about.html", "services.html", "treatments.html",
    "doctors.html", "locations.html", "contact.html",
    "treatments/dental-implants.html", "treatments/orthodontics.html",
    "treatments/cosmetic-dentistry.html", "treatments/general-dentistry.html",
    "treatments/emergency-dentist.html",
] + [f"doctors/{name}" for name in DOCTOR_FILES]

PROHIBITED_META = (
    "best dentist", "best dental", "painless", "pain-free", "pain free",
    "top-tier", "top tier", "highest standard", "guaranteed outcome",
    "guaranteed results", "predictable outcome",
)


def text(path):
    return (ROOT / path).read_text(encoding="utf-8")


def head(path):
    html = text(path)
    return html.split("</head>", 1)[0].lower()


def jsonld_entities(path):
    html = text(path)
    scripts = re.findall(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html,
        flags=re.I | re.S,
    )
    entities = []
    for raw in scripts:
        data = json.loads(raw)
        if isinstance(data, dict) and isinstance(data.get("@graph"), list):
            entities.extend(data["@graph"])
        else:
            entities.append(data)
    return entities


def entity_by_id(path, entity_id):
    for entity in jsonld_entities(path):
        if isinstance(entity, dict) and entity.get("@id") == entity_id:
            return entity
    return None


class GoogleAuthorityContract(unittest.TestCase):
    def test_homepage_defines_parent_brand_and_both_branches(self):
        organization = entity_by_id("index.html", ORG_ID)
        self.assertIsNotNone(organization, "Homepage must define the parent Silwadi organization")
        self.assertEqual(organization.get("name"), "Silwadi Dental Center")
        self.assertEqual(str(organization.get("foundingDate")), "1980")

        bani = entity_by_id("index.html", BANI_ID)
        raha = entity_by_id("index.html", RAHA_ID)
        self.assertIsNotNone(bani, "Homepage must define Bani Yas branch")
        self.assertIsNotNone(raha, "Homepage must define Al Raha branch")
        self.assertEqual(bani.get("telephone"), "+97126262042")
        self.assertEqual(raha.get("telephone"), "+97126662408")
        self.assertEqual(bani.get("parentOrganization", {}).get("@id"), ORG_ID)
        self.assertEqual(raha.get("parentOrganization", {}).get("@id"), ORG_ID)

        website = entity_by_id("index.html", WEBSITE_ID)
        self.assertIsNotNone(website)
        self.assertEqual(website.get("publisher", {}).get("@id"), ORG_ID)

    def test_about_page_is_about_parent_brand(self):
        about = entity_by_id("about.html", f"{BASE}/about.html#about")
        self.assertIsNotNone(about)
        self.assertEqual(about.get("about", {}).get("@id"), ORG_ID)

    def test_locations_and_contact_reference_stable_branch_ids(self):
        for path in ("locations.html", "contact.html"):
            self.assertIsNotNone(entity_by_id(path, BANI_ID), f"{path} missing Bani Yas entity")
            self.assertIsNotNone(entity_by_id(path, RAHA_ID), f"{path} missing Al Raha entity")

    def test_doctor_worksfor_references_only_known_branches(self):
        for filename in DOCTOR_FILES:
            path = f"doctors/{filename}"
            people = [e for e in jsonld_entities(path) if isinstance(e, dict) and e.get("@type") == "Person"]
            self.assertEqual(len(people), 1, f"{path} should expose one Person entity")
            works_for = people[0].get("worksFor")
            refs = works_for if isinstance(works_for, list) else [works_for]
            ids = {ref.get("@id") for ref in refs if isinstance(ref, dict)}
            self.assertTrue(ids, f"{path} must identify at least one Silwadi branch")
            self.assertTrue(ids <= ALLOWED_BRANCH_IDS, f"{path} has unknown worksFor IDs: {ids}")

    def test_public_metadata_avoids_unverifiable_superiority_claims(self):
        paths = ["index.html", "about.html", "locations.html", "contact.html", "doctors.html", "treatments.html"]
        paths += [f"doctors/{name}" for name in DOCTOR_FILES]
        paths += [
            "treatments/dental-implants.html", "treatments/orthodontics.html",
            "treatments/cosmetic-dentistry.html", "treatments/general-dentistry.html",
            "treatments/emergency-dentist.html",
        ]
        for path in paths:
            page_head = head(path)
            for phrase in PROHIBITED_META:
                self.assertNotIn(phrase, page_head, f"{path} metadata contains prohibited phrase: {phrase}")

    def test_english_pages_have_self_canonical_and_language_alternates(self):
        for path in PAIR_FILES:
            html = text(path)
            public_path = "/" if path == "index.html" else f"/{path}"
            canonical = f'{BASE}{public_path}'
            ar_path = "/ar/" if path == "index.html" else f"/ar/{path}"
            self.assertIn(f'rel="canonical" href="{canonical}"', html, f"{path} canonical mismatch")
            self.assertIn(f'hreflang="en-AE" href="{canonical}"', html, f"{path} missing en-AE")
            self.assertIn(f'hreflang="ar-AE" href="{BASE}{ar_path}"', html, f"{path} missing ar-AE")
            self.assertIn(f'hreflang="x-default" href="{canonical}"', html, f"{path} missing x-default")

    def test_sitemap_exposes_only_public_site_urls(self):
        xml = text("sitemap.xml")
        lowered = xml.lower()
        for forbidden in ("/review/", "/.tmp/", "old-silwadi-site"):
            self.assertNotIn(forbidden, lowered)
        root = ET.fromstring(xml)
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [node.text for node in root.findall("s:url/s:loc", ns)]
        self.assertEqual(len(urls), len(set(urls)), "sitemap must not contain duplicate URLs")
        self.assertTrue(all(url.startswith(f"{BASE}/") for url in urls))


if __name__ == "__main__":
    unittest.main()
