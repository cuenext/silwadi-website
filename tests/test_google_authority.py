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
    "dr-munir-silwadi.html", "dr-moheb-silwadi.html", "dr-hani-hasbini.html",
    "dr-moammar-rifai.html", "dr-ahmed-el-shehri.html", "dr-fahed-khalil.html",
    "dr-afnan-mashal.html", "dr-krishnamurthy-katta-balajee.html",
    "dr-ehab-hassouneh.html", "dr-sara-ismail.html", "dr-nasr-keshkiea.html",
    "dr-dana-awad.html", "dr-kashmira-pawar-jayprakash.html",
    "dr-nachiket-shah.html", "dr-lana-masoud.html",
]

DOCTOR_BRANCHES = {
    "dr-munir-silwadi.html": {BANI_ID, RAHA_ID},
    "dr-moheb-silwadi.html": {RAHA_ID},
    "dr-hani-hasbini.html": {BANI_ID},
    "dr-moammar-rifai.html": {BANI_ID},
    "dr-ahmed-el-shehri.html": {BANI_ID},
    "dr-fahed-khalil.html": {BANI_ID},
    "dr-afnan-mashal.html": {BANI_ID},
    "dr-krishnamurthy-katta-balajee.html": {BANI_ID, RAHA_ID},
    "dr-ehab-hassouneh.html": {RAHA_ID},
    "dr-sara-ismail.html": {RAHA_ID},
    "dr-nasr-keshkiea.html": {BANI_ID},
    "dr-dana-awad.html": {BANI_ID},
    "dr-kashmira-pawar-jayprakash.html": {RAHA_ID},
    "dr-nachiket-shah.html": {RAHA_ID},
    "dr-lana-masoud.html": {RAHA_ID},
}

TREATMENT_FILES = [
    "dental-implants.html", "orthodontics.html", "cosmetic-dentistry.html",
    "general-dentistry.html", "emergency-dentist.html",
]

PAIR_FILES = [
    "index.html", "about.html", "services.html", "treatments.html",
    "doctors.html", "locations.html", "contact.html",
] + [f"treatments/{name}" for name in TREATMENT_FILES] + [f"doctors/{name}" for name in DOCTOR_FILES]

PROHIBITED_META = (
    "best dentist", "best dental", "painless", "pain-free", "pain free",
    "top-tier", "top tier", "highest standard", "guaranteed outcome",
    "guaranteed results", "predictable outcome",
)


def text(path):
    return (ROOT / path).read_text(encoding="utf-8")


def head(path):
    return text(path).split("</head>", 1)[0].lower()


def jsonld_entities(path):
    scripts = re.findall(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        text(path), flags=re.I | re.S,
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


def person_branch_ids(path):
    people = [e for e in jsonld_entities(path) if isinstance(e, dict) and e.get("@type") == "Person"]
    if len(people) != 1:
        raise AssertionError(f"{path} should expose one Person entity, found {len(people)}")
    works_for = people[0].get("worksFor")
    refs = works_for if isinstance(works_for, list) else [works_for]
    return {ref.get("@id") for ref in refs if isinstance(ref, dict)}


class GoogleAuthorityContract(unittest.TestCase):
    def test_homepage_defines_parent_brand_and_both_branches(self):
        for path in ("index.html", "ar/index.html"):
            organization = entity_by_id(path, ORG_ID)
            self.assertIsNotNone(organization, f"{path} must define the parent Silwadi organization")
            self.assertEqual(organization.get("name"), "Silwadi Dental Center")
            self.assertEqual(str(organization.get("foundingDate")), "1980")
            bani = entity_by_id(path, BANI_ID)
            raha = entity_by_id(path, RAHA_ID)
            self.assertIsNotNone(bani, f"{path} must define Bani Yas branch")
            self.assertIsNotNone(raha, f"{path} must define Al Raha branch")
            self.assertEqual(bani.get("telephone"), "+97126262042")
            self.assertEqual(raha.get("telephone"), "+97126662408")
            self.assertEqual(bani.get("parentOrganization", {}).get("@id"), ORG_ID)
            self.assertEqual(raha.get("parentOrganization", {}).get("@id"), ORG_ID)
            website = entity_by_id(path, WEBSITE_ID)
            self.assertIsNotNone(website)
            self.assertEqual(website.get("publisher", {}).get("@id"), ORG_ID)

    def test_about_page_is_about_parent_brand(self):
        about = entity_by_id("about.html", f"{BASE}/about.html#about")
        self.assertIsNotNone(about)
        self.assertEqual(about.get("about", {}).get("@id"), ORG_ID)
        self.assertEqual(about.get("isPartOf", {}).get("@id"), WEBSITE_ID)

    def test_locations_and_contact_have_bilingual_branch_entity_parity(self):
        for path, locale_prefix in (
            ("locations.html", ""), ("contact.html", ""),
            ("ar/locations.html", "/ar"), ("ar/contact.html", "/ar"),
        ):
            bani = entity_by_id(path, BANI_ID)
            raha = entity_by_id(path, RAHA_ID)
            self.assertIsNotNone(bani, f"{path} missing Bani Yas entity")
            self.assertIsNotNone(raha, f"{path} missing Al Raha entity")
            for entity in (bani, raha):
                self.assertEqual(entity.get("parentOrganization", {}).get("@id"), ORG_ID)
                self.assertEqual(entity.get("email"), "info@silwadidentalcentres.ae")
                self.assertIsInstance(entity.get("geo"), dict, f"{path} branch entity must include geo")
            self.assertEqual(bani.get("url"), f"{BASE}{locale_prefix}/locations.html#bani-yas")
            self.assertEqual(raha.get("url"), f"{BASE}{locale_prefix}/locations.html#al-raha")

    def test_doctor_branch_assignments_are_exact_in_both_languages(self):
        for filename, expected in DOCTOR_BRANCHES.items():
            for prefix in ("doctors/", "ar/doctors/"):
                path = f"{prefix}{filename}"
                ids = person_branch_ids(path)
                self.assertEqual(ids, expected, f"{path} has incorrect worksFor branch IDs")
                self.assertTrue(ids <= ALLOWED_BRANCH_IDS)

    def test_treatment_service_provider_resolves_to_parent_brand_in_both_languages(self):
        for filename in TREATMENT_FILES:
            for prefix in ("treatments/", "ar/treatments/"):
                path = f"{prefix}{filename}"
                services = [e for e in jsonld_entities(path) if isinstance(e, dict) and e.get("@type") == "Service"]
                self.assertEqual(len(services), 1, f"{path} should expose one Service entity")
                self.assertEqual(services[0].get("provider", {}).get("@id"), ORG_ID)
                self.assertEqual(services[0].get("isPartOf", {}).get("@id"), WEBSITE_ID)

    def test_services_hub_service_entities_reference_parent_brand(self):
        for path in ("services.html", "ar/services.html"):
            services = [e for e in jsonld_entities(path) if isinstance(e, dict) and e.get("@type") == "Service"]
            self.assertEqual(len(services), 9, f"{path} should expose the nine established service areas")
            for service in services:
                self.assertEqual(service.get("provider", {}).get("@id"), ORG_ID)
                self.assertEqual(service.get("isPartOf", {}).get("@id"), WEBSITE_ID)

    def test_treatments_collection_is_connected_to_brand_and_website(self):
        page = entity_by_id("treatments.html", f"{BASE}/treatments.html#page")
        self.assertIsNotNone(page)
        self.assertEqual(page.get("about", {}).get("@id"), ORG_ID)
        self.assertEqual(page.get("isPartOf", {}).get("@id"), WEBSITE_ID)

    def test_public_metadata_avoids_unverifiable_superiority_claims(self):
        paths = ["index.html", "about.html", "locations.html", "contact.html", "doctors.html", "treatments.html", "services.html"]
        paths += [f"doctors/{name}" for name in DOCTOR_FILES]
        paths += [f"treatments/{name}" for name in TREATMENT_FILES]
        for path in paths:
            page_head = head(path)
            for phrase in PROHIBITED_META:
                self.assertNotIn(phrase, page_head, f"{path} metadata contains prohibited phrase: {phrase}")

    def test_english_and_arabic_pages_have_reciprocal_canonical_hreflang(self):
        for path in PAIR_FILES:
            english_html = text(path)
            public_path = "/" if path == "index.html" else f"/{path}"
            canonical = f"{BASE}{public_path}"
            ar_path = "/ar/" if path == "index.html" else f"/ar/{path}"
            arabic_url = f"{BASE}{ar_path}"
            arabic_file = "ar/index.html" if path == "index.html" else f"ar/{path}"
            arabic_html = text(arabic_file)
            self.assertIn(f'rel="canonical" href="{canonical}"', english_html)
            self.assertIn(f'hreflang="en-AE" href="{canonical}"', english_html)
            self.assertIn(f'hreflang="ar-AE" href="{arabic_url}"', english_html)
            self.assertIn(f'hreflang="x-default" href="{canonical}"', english_html)
            self.assertIn(f'rel="canonical" href="{arabic_url}"', arabic_html)
            self.assertIn(f'hreflang="en-AE" href="{canonical}"', arabic_html)
            self.assertIn(f'hreflang="ar-AE" href="{arabic_url}"', arabic_html)
            self.assertIn(f'hreflang="x-default" href="{canonical}"', arabic_html)

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
