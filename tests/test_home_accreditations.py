from html.parser import HTMLParser
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


def normalized(text):
    return re.sub(r"\s+", " ", text).strip()


class AccreditationPageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.landmarks = []
        self.in_accreditations = False
        self.in_heading = False
        self.section_labelledby = None
        self.heading_id = None
        self.heading_text = []
        self.section_text = []
        self.current_card = None
        self.cards = []
        self.controls = []
        self.controls_role = None
        self.track_role = None
        self.dots_present = False
        self.dots_aria_hidden = None
        self.stylesheets = []
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = set(attributes.get("class", "").split())

        if tag == "section" and "team-proof" in classes:
            self.landmarks.append("team")
        elif tag == "nav" and "care-shortcuts" in classes:
            self.landmarks.append("shortcuts")
        elif tag == "section" and "about-accreditations" in classes:
            self.landmarks.append("accreditations")
            self.in_accreditations = True
            self.section_labelledby = attributes.get("aria-labelledby")
        elif tag == "section" and attributes.get("id") == "treatments":
            self.landmarks.append("treatments")

        if tag == "link" and "stylesheet" in attributes.get("rel", "").split():
            self.stylesheets.append(attributes.get("href", ""))
        elif tag == "script" and attributes.get("src"):
            self.scripts.append(attributes["src"])

        if not self.in_accreditations:
            return

        if tag == "h2":
            self.in_heading = True
            self.heading_id = attributes.get("id")
        elif tag == "article" and "acc-card" in classes:
            self.current_card = {"text": [], "images": []}
        elif tag == "img" and self.current_card is not None:
            self.current_card["images"].append(
                (attributes.get("src"), attributes.get("alt"))
            )
        elif tag == "button" and "acc-control" in classes:
            self.controls.append(attributes.get("aria-label"))
        elif tag == "div" and attributes.get("id") == "accDots":
            self.dots_present = True
            self.dots_aria_hidden = attributes.get("aria-hidden")
        elif tag == "div" and attributes.get("id") == "accTrack":
            self.track_role = attributes.get("role")
        elif tag == "div" and "acc-controls" in classes:
            self.controls_role = attributes.get("role")

    def handle_endtag(self, tag):
        if not self.in_accreditations:
            return

        if tag == "h2":
            self.in_heading = False
        elif tag == "article" and self.current_card is not None:
            self.cards.append(
                {
                    "text": normalized(" ".join(self.current_card["text"])),
                    "images": tuple(self.current_card["images"]),
                }
            )
            self.current_card = None
        elif tag == "section":
            self.in_accreditations = False

    def handle_data(self, data):
        if not self.in_accreditations:
            return
        self.section_text.append(data)
        if self.in_heading:
            self.heading_text.append(data)
        if self.current_card is not None:
            self.current_card["text"].append(data)


def parse(relative_path):
    parser = AccreditationPageParser()
    parser.feed((ROOT / relative_path).read_text(encoding="utf-8"))
    return parser


class HomeAccreditations(unittest.TestCase):
    def assert_home_matches_about(self, home_path, about_path):
        home = parse(home_path)
        about = parse(about_path)

        self.assertEqual(
            ["team", "shortcuts", "accreditations", "treatments"],
            home.landmarks[:4],
        )
        self.assertEqual(
            normalized(" ".join(about.heading_text)),
            normalized(" ".join(home.heading_text)),
        )
        self.assertEqual(about.cards, home.cards)
        self.assertEqual(
            normalized(" ".join(about.section_text)),
            normalized(" ".join(home.section_text)),
        )
        self.assertEqual(5, len(home.cards))

        self.assertTrue(home.section_labelledby)
        self.assertEqual(home.section_labelledby, home.heading_id)
        self.assertEqual(about.controls, home.controls)

    def test_english_home_reuses_about_accreditations_before_treatments(self):
        self.assert_home_matches_about("index.html", "about.html")

    def test_arabic_home_reuses_localized_about_accreditations_before_treatments(self):
        self.assert_home_matches_about("ar/index.html", "ar/about.html")

    def test_home_loads_isolated_accreditation_assets(self):
        for relative_path in ("index.html", "ar/index.html"):
            page = parse(relative_path)
            with self.subTest(page=relative_path):
                self.assertIn("/accreditations.css", page.stylesheets)
                self.assertIn("/accreditations.js", page.scripts)

        self.assertTrue((ROOT / "accreditations.css").is_file())
        self.assertTrue((ROOT / "accreditations.js").is_file())

    def test_carousel_groups_and_focusable_dots_are_exposed_to_assistive_technology(self):
        for relative_path in ("index.html", "ar/index.html"):
            page = parse(relative_path)
            with self.subTest(page=relative_path):
                self.assertTrue(page.dots_present)
                self.assertNotEqual("true", page.dots_aria_hidden)
                self.assertEqual("group", page.track_role)
                self.assertEqual("group", page.controls_role)


if __name__ == "__main__":
    unittest.main()
