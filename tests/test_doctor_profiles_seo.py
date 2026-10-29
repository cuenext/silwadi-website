from pathlib import Path
from html.parser import HTMLParser
import html as html_lib
import importlib.util
import json
import re
import tempfile
import unittest
from unittest import mock
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "apply_doctor_profiles_seo.py"
SCRIPT_SPEC = importlib.util.spec_from_file_location("apply_doctor_profiles_seo", SCRIPT_PATH)
SEO_SCRIPT = importlib.util.module_from_spec(SCRIPT_SPEC)
SCRIPT_SPEC.loader.exec_module(SEO_SCRIPT)
TODAY = "2026-09-12"
PAGES = [
    "doctors/dr-munir-silwadi.html",
    "doctors/dr-moheb-silwadi.html",
    "doctors/dr-hani-hasbini.html",
    "doctors/dr-moammar-rifai.html",
    "doctors/dr-ahmed-el-shehri.html",
    "doctors/dr-fahed-khalil.html",
    "doctors/dr-afnan-mashal.html",
    "doctors/dr-krishnamurthy-katta-balajee.html",
    "doctors/dr-ehab-hassouneh.html",
    "doctors/dr-sara-ismail.html",
    "doctors/dr-nasr-keshkiea.html",
    "doctors/dr-dana-awad.html",
    "doctors/dr-mithra-pothancheri.html",
    "doctors/dr-kashmira-pawar-jayprakash.html",
    "doctors/dr-nachiket-shah.html",
    "doctors/dr-lana-masoud.html",
]


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self._in_title = False
        self.meta = {}
        self.links = []
        self._jsonld = False
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
            self._jsonld = True
            self._jsonld_parts = []

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "script" and self._jsonld:
            raw = "".join(self._jsonld_parts).strip()
            if raw:
                self.jsonld.append(json.loads(raw))
            self._jsonld = False
            self._jsonld_parts = []

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._jsonld:
            self._jsonld_parts.append(data)


def parse(path):
    source = (ROOT / path).read_text(encoding="utf-8")
    parser = Parser()
    parser.feed(source)
    return source, parser


def graph_nodes(parser):
    nodes = []
    for block in parser.jsonld:
        if isinstance(block, dict) and isinstance(block.get("@graph"), list):
            nodes.extend(block["@graph"])
        elif isinstance(block, dict):
            nodes.append(block)
    return nodes


def nodes_of_type(parser, schema_type):
    result = []
    for node in graph_nodes(parser):
        node_type = node.get("@type")
        values = node_type if isinstance(node_type, list) else [node_type]
        if schema_type in values:
            result.append(node)
    return result


def link_href(parser, rel=None, hreflang=None):
    for link in parser.links:
        if rel and rel not in link.get("rel", "").split():
            continue
        if hreflang and link.get("hreflang") != hreflang:
            continue
        return link.get("href")
    return None


def visible_profile_identity(source):
    name_match = re.search(r'<h1>(.*?)</h1>', source, re.I | re.S)
    specialty_match = re.search(r'<p class="consultant-specialty">(.*?)</p>', source, re.I | re.S)
    base_match = re.search(r'<strong>Clinical base</strong>\s*<span>(.*?)</span>', source, re.I | re.S)
    if not (name_match and specialty_match and base_match):
        raise AssertionError("Doctor profile is missing visible name, specialty, or clinical base")
    clean = lambda value: html_lib.unescape(re.sub(r"<[^>]+>", "", value)).replace("\xa0", " ").strip()
    return clean(name_match.group(1)), clean(specialty_match.group(1)), clean(base_match.group(1))


def visible_portrait_url(source, path):
    match = re.search(
        r'<div class="consultant-portrait__frame[^>]*>\s*<img[^>]+src="([^"]+)"',
        source,
        re.I | re.S,
    )
    if not match:
        return None
    canonical = f"https://silwadi.ae/{path}"
    return urljoin(canonical, html_lib.unescape(match.group(1)))


class DoctorProfileSeoContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parsed = {path: parse(path) for path in PAGES}

    def test_all_16_profiles_are_indexable_and_have_unique_metadata(self):
        self.assertEqual(len(self.parsed), 16)
        titles = []
        descriptions = []
        for path, (source, parser) in self.parsed.items():
            name, specialty, _ = visible_profile_identity(source)
            self.assertIn("index", parser.meta.get("robots", ""), path)
            self.assertIn("follow", parser.meta.get("robots", ""), path)
            self.assertTrue(parser.title.startswith("Dr. "), path)
            self.assertIn(name, parser.title, path)
            self.assertIn("Abu Dhabi", parser.title, path)
            description = parser.meta.get("description", "")
            self.assertIn(name, description, path)
            description_specialty = (
                "General Dentist and Clinical Quality Coordinator"
                if path.endswith("dr-mithra-pothancheri.html")
                else specialty
            )
            self.assertIn(description_specialty, description, path)
            self.assertIn("Abu Dhabi", description, path)
            titles.append(parser.title)
            descriptions.append(description)
        self.assertEqual(len(titles), len(set(titles)))
        self.assertEqual(len(descriptions), len(set(descriptions)))

    def test_canonical_hreflang_and_open_graph_match_each_profile(self):
        for path, (source, parser) in self.parsed.items():
            canonical = f"https://silwadi.ae/{path}"
            arabic = f"https://silwadi.ae/ar/{path}"
            self.assertEqual(link_href(parser, rel="canonical"), canonical, path)
            self.assertEqual(parser.meta.get("og:url"), canonical, path)
            self.assertEqual(parser.meta.get("og:type"), "profile", path)
            self.assertEqual(link_href(parser, rel="alternate", hreflang="en-AE"), canonical, path)
            self.assertEqual(link_href(parser, rel="alternate", hreflang="ar-AE"), arabic, path)
            self.assertEqual(link_href(parser, rel="alternate", hreflang="x-default"), canonical, path)
            portrait = visible_portrait_url(source, path)
            og_image = parser.meta.get("og:image")
            if portrait:
                self.assertEqual(og_image, portrait, path)
            else:
                self.assertEqual(og_image, "https://silwadi.ae/assets/silwadi-logo-official.png", path)

    def test_profilepage_person_and_branch_affiliation_are_valid(self):
        for path, (source, parser) in self.parsed.items():
            canonical = f"https://silwadi.ae/{path}"
            name, specialty, clinical_base = visible_profile_identity(source)
            self.assertTrue(nodes_of_type(parser, "BreadcrumbList"), path)
            profiles = nodes_of_type(parser, "ProfilePage")
            people = nodes_of_type(parser, "Person")
            self.assertEqual(len(profiles), 1, path)
            self.assertEqual(len(people), 1, path)
            profile = profiles[0]
            person = people[0]
            self.assertEqual(profile.get("url"), canonical, path)
            self.assertEqual(profile.get("mainEntity", {}).get("@id"), f"{canonical}#person", path)
            self.assertEqual(person.get("@id"), f"{canonical}#person", path)
            self.assertEqual(person.get("name"), name, path)
            self.assertEqual(person.get("jobTitle"), specialty, path)
            works_for = person.get("worksFor")
            if isinstance(works_for, dict):
                works_for = [works_for]
            ids = {item.get("@id") for item in (works_for or []) if isinstance(item, dict)}
            if "Both locations" in clinical_base:
                self.assertEqual(ids, {"https://silwadi.ae/#dentist", "https://silwadi.ae/#dentist-al-raha"}, path)
            elif "Al Raha" in clinical_base:
                self.assertEqual(ids, {"https://silwadi.ae/#dentist-al-raha"}, path)
            else:
                self.assertEqual(ids, {"https://silwadi.ae/#dentist"}, path)
            portrait = visible_portrait_url(source, path)
            if portrait:
                self.assertEqual(person.get("image"), portrait, path)
            else:
                self.assertNotIn("image", person, path)

    def test_booking_links_use_canonical_consultation_form_anchor(self):
        for path, (source, _) in self.parsed.items():
            self.assertNotIn('href="../contact.html#consultation"', source, path)
            self.assertIn('href="../contact.html#consultation-form"', source, path)

    def test_sitemap_is_fresh_for_all_doctor_profiles(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        for path in PAGES:
            url = f"https://silwadi.ae/{path}"
            match = re.search(rf'<loc>{re.escape(url)}</loc>\s*<lastmod>([^<]+)</lastmod>', sitemap)
            self.assertIsNotNone(match, path)
            self.assertGreaterEqual(match.group(1), TODAY, path)


class DoctorProfileSeoScriptTest(unittest.TestCase):
    def test_sitemap_update_preserves_newer_lastmod_and_is_idempotent(self):
        older_path = "doctors/dr-munir-silwadi.html"
        newer_path = "doctors/dr-mithra-pothancheri.html"
        original = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://silwadi.ae/doctors/dr-munir-silwadi.html</loc>
    <lastmod>2026-08-01</lastmod>
  </url>
  <url>
    <loc>https://silwadi.ae/doctors/dr-mithra-pothancheri.html</loc>
    <lastmod>2026-10-29</lastmod>
  </url>
</urlset>
"""

        with tempfile.TemporaryDirectory(dir=ROOT) as temp_dir:
            sitemap = Path(temp_dir) / "sitemap.xml"
            sitemap.write_text(original, encoding="utf-8")
            with (
                mock.patch.object(SEO_SCRIPT, "ROOT", Path(temp_dir)),
                mock.patch.object(SEO_SCRIPT, "PAGES", [older_path, newer_path]),
                mock.patch.object(SEO_SCRIPT, "TODAY", "2026-09-12"),
            ):
                SEO_SCRIPT.update_sitemap()
                first_update = sitemap.read_text(encoding="utf-8")
                SEO_SCRIPT.update_sitemap()
                second_update = sitemap.read_text(encoding="utf-8")

        self.assertIn("<lastmod>2026-09-12</lastmod>", first_update)
        self.assertIn(
            "<loc>https://silwadi.ae/doctors/dr-mithra-pothancheri.html</loc>\n"
            "    <lastmod>2026-10-29</lastmod>",
            first_update,
        )
        self.assertEqual(second_update, first_update)


if __name__ == "__main__":
    unittest.main()
