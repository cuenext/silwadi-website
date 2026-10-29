import json
import re
import unittest
from html import unescape
from pathlib import Path
from urllib.parse import urljoin


ROOT = Path(__file__).resolve().parents[1]
SLUG = "dr-mithra-pothancheri"
EN_PROFILE = ROOT / "doctors" / f"{SLUG}.html"
AR_PROFILE = ROOT / "ar" / "doctors" / f"{SLUG}.html"
PORTRAIT = ROOT / "assets" / "doctors" / "optimized" / f"{SLUG}.webp"


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def jsonld_nodes(source):
    nodes = []
    for block in re.findall(
        r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>',
        source,
        re.I | re.S,
    ):
        value = json.loads(block)
        nodes.extend(value.get("@graph", []) if isinstance(value, dict) else [value])
    return nodes


def directory_cards(source):
    cards = []
    for article in re.findall(
        r'<article\b[^>]*\bdata-doctor-card(?:="")?[^>]*>(.*?)</article>',
        source,
        re.I | re.S,
    ):
        name = re.search(r"<h2>(.*?)</h2>", article, re.I | re.S)
        link = re.search(
            r'<a\b[^>]*class="doctor-directory-card__link"[^>]*href="([^"]+)"',
            article,
            re.I | re.S,
        )
        if name and link:
            cards.append((unescape(re.sub(r"<[^>]+>", "", name.group(1))).strip(), link.group(1)))
    return cards


class MithraProfileContract(unittest.TestCase):
    def test_bilingual_profiles_and_portrait_publish_supplied_facts(self):
        self.assertTrue(PORTRAIT.is_file())
        self.assertGreater(PORTRAIT.stat().st_size, 10_000)
        self.assertTrue(EN_PROFILE.is_file())
        self.assertTrue(AR_PROFILE.is_file())

        en = EN_PROFILE.read_text(encoding="utf-8")
        en_main = en.split('<main id="main">', 1)[1]
        for fact in [
            "Dr. Mithra Pothancheri",
            "General Dentist &amp; Clinical Quality Coordinator",
            "DOH-licensed",
            "A.J. Shetty College of Dental Sciences",
            "Rajiv Gandhi University of Health Sciences",
            "TRIOS 3Shape",
            "Clinical photography",
            "Preventive dentistry",
            "Professional teeth whitening",
            "Clinical governance",
            "Bani Yas Tower, Abu&nbsp;Dhabi",
            f"../assets/doctors/optimized/{SLUG}.webp",
        ]:
            self.assertIn(fact, en)
        self.assertIn("patient education", en_main)
        self.assertIn("conservative care", en_main)
        self.assertIn(
            f'<link rel="canonical" href="https://silwadi.ae/doctors/{SLUG}.html">',
            en,
        )
        self.assertIn(
            f'hreflang="ar-AE" href="https://silwadi.ae/ar/doctors/{SLUG}.html"',
            en,
        )

        person = next(
            node for node in jsonld_nodes(en) if node.get("@type") == "Person"
        )
        self.assertEqual(person["name"], "Dr. Mithra Pothancheri")
        self.assertEqual(
            person["jobTitle"], "General Dentist & Clinical Quality Coordinator"
        )
        self.assertEqual(person["worksFor"]["@id"], "https://silwadi.ae/#dentist")
        self.assertEqual(
            person["image"],
            f"https://silwadi.ae/assets/doctors/optimized/{SLUG}.webp",
        )
        self.assertIn("Professional teeth whitening", person["knowsAbout"])

        ar = AR_PROFILE.read_text(encoding="utf-8")
        ar_main = ar.split('<main id="main">', 1)[1]
        for fact in [
            "د. ميثرا بوثانتشيري",
            "طبيبة أسنان عامة ومنسقة الجودة السريرية",
            "كلية إيه جي شيتي لعلوم طب الأسنان",
            "جامعة راجيف غاندي للعلوم الصحية",
            "TRIOS 3Shape",
            "التصوير السريري للأسنان",
            "طب الأسنان الوقائي",
            "تبييض الأسنان المهني",
            "الحوكمة السريرية",
            "برج بني ياس، أبوظبي",
            f"/assets/doctors/optimized/{SLUG}.webp",
        ]:
            self.assertIn(fact, ar)
        self.assertIn("تثقيف المرضى", ar_main)
        self.assertIn("الرعاية المتحفظة", ar_main)
        self.assertIn(
            f'<link rel="canonical" href="https://silwadi.ae/ar/doctors/{SLUG}.html">',
            ar,
        )
        ar_person = next(
            node for node in jsonld_nodes(ar) if node.get("@type") == "Person"
        )
        self.assertIn("تبييض الأسنان المهني", ar_person["knowsAbout"])

    def test_directories_order_counts_and_sitemap_include_mithra_once(self):
        en = read("doctors.html")
        ar = read("ar/doctors.html")
        for source in (en, ar):
            self.assertEqual(source.count('data-name="Dr. Mithra Pothancheri"'), 1)
            self.assertIn(f"doctors/{SLUG}.html", source)
            self.assertIn("16", source)
        self.assertEqual(en.count("data-doctor-card"), 16)
        self.assertEqual(ar.count("data-doctor-card"), 16)
        self.assertIn('"numberOfItems":16', en)
        self.assertIn('"numberOfItems":16', ar)

        app = read("app.js")
        self.assertIn("'Dr. Mithra Pothancheri'", app)
        self.assertLess(app.index("'Dr. Dana Awad'"), app.index("'Dr. Mithra Pothancheri'"))
        self.assertLess(app.index("'Dr. Mithra Pothancheri'"), app.index("'Dr. Afnan Mashal'"))

        sitemap = read("sitemap.xml")
        self.assertEqual(
            sitemap.count(f"https://silwadi.ae/doctors/{SLUG}.html"), 1
        )
        self.assertEqual(
            sitemap.count(f"https://silwadi.ae/ar/doctors/{SLUG}.html"), 1
        )

    def test_directory_itemlists_match_visible_card_order_names_and_urls(self):
        expected_middle = {
            "doctors.html": [
                ("Dr. Dana Awad", "doctors/dr-dana-awad.html"),
                ("Dr. Mithra Pothancheri", f"doctors/{SLUG}.html"),
                ("Dr. Afnan Mashal", "doctors/dr-afnan-mashal.html"),
            ],
            "ar/doctors.html": [
                ("د. دانا عوض", "/ar/doctors/dr-dana-awad.html"),
                ("د. ميثرا بوثانتشيري", f"/ar/doctors/{SLUG}.html"),
                ("د. أفنان مشعل", "/ar/doctors/dr-afnan-mashal.html"),
            ],
        }

        for path, middle in expected_middle.items():
            with self.subTest(path=path):
                source = read(path)
                cards = directory_cards(source)
                item_list = next(
                    node for node in jsonld_nodes(source) if node.get("@type") == "ItemList"
                )
                items = item_list["itemListElement"]

                self.assertEqual(cards[4:7], middle)
                self.assertEqual(
                    [item["position"] for item in items],
                    list(range(1, len(cards) + 1)),
                )
                self.assertEqual(
                    [item["name"] for item in items],
                    [name for name, _ in cards],
                )
                self.assertEqual(
                    [item["url"] for item in items],
                    [urljoin("https://silwadi.ae/", href) for _, href in cards],
                )

    def test_arabic_directory_collection_and_itemlist_are_localized_canonicals(self):
        source = read("ar/doctors.html")
        nodes = jsonld_nodes(source)
        collection = next(
            node for node in nodes if node.get("@type") == "CollectionPage"
        )
        item_list = next(node for node in nodes if node.get("@type") == "ItemList")

        self.assertEqual(collection["@id"], "https://silwadi.ae/ar/doctors.html#page")
        self.assertEqual(collection["url"], "https://silwadi.ae/ar/doctors.html")
        self.assertEqual(collection["name"], "أطباء الأسنان في أبوظبي | فريق مركز سلوادي")
        self.assertEqual(
            collection["mainEntity"]["@id"],
            "https://silwadi.ae/ar/doctors.html#doctor-list",
        )
        self.assertEqual(
            item_list["@id"], "https://silwadi.ae/ar/doctors.html#doctor-list"
        )
        self.assertEqual(item_list["name"], "فريق مركز سلوادي لطب الأسنان")
        self.assertTrue(
            all(
                item["url"].startswith("https://silwadi.ae/ar/doctors/")
                for item in item_list["itemListElement"]
            )
        )
        self.assertTrue(
            all(
                re.search(r"[\u0600-\u06ff]", item["name"])
                for item in item_list["itemListElement"]
            )
        )

    def test_site_counts_translations_routes_and_ai_knowledge_are_current(self):
        for page in ["index.html", "about.html"]:
            self.assertIn("16 dentists &amp; specialists", read(page))
        for page in ["ar/index.html", "ar/about.html"]:
            self.assertIn("16 طبيباً واختصاصياً", read(page))

        language = read("language.js")
        self.assertIn("'Dr. Mithra Pothancheri': 'د. ميثرا بوثانتشيري'", language)
        self.assertIn("'16 dentists & specialists': '16 طبيباً واختصاصياً'", language)

        routes = json.loads(read("data/arabic-seo.json"))
        self.assertIn(f"doctors/{SLUG}.html", routes)

        knowledge = json.loads(read("ai/clinic-knowledge-v1.json"))
        doctors = {doctor["name"]: doctor for doctor in knowledge["doctors"]}
        self.assertEqual(len(doctors), 16)
        mithra = doctors["Dr. Mithra Pothancheri"]
        self.assertEqual(mithra["role"], "General Dentist")
        self.assertEqual(mithra["additionalRole"], "Clinical Quality Coordinator")
        self.assertEqual(mithra["branches"], ["bani-yas"])
        self.assertIn("TRIOS 3Shape", " ".join(mithra["clinicalFocus"]))
        self.assertIn("A.J. Shetty College of Dental Sciences", mithra["credentials"])


if __name__ == "__main__":
    unittest.main()
