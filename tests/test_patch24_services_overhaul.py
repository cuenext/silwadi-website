from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class Patch24ServicesOverhaul(unittest.TestCase):
    def read(self, rel):
        return (ROOT / rel).read_text(encoding="utf-8")

    def test_services_hub_has_patient_first_starting_points(self):
        html = self.read("services.html")
        self.assertIn('class="services-start"', html)
        self.assertIn("Start with what you need", html)
        self.assertIn('aria-label="Choose a starting point"', html)
        self.assertGreaterEqual(html.count('class="services-start__card'), 3)
        self.assertIn('href="#pedodontics"', html)
        self.assertIn('href="#prosthodontics-implantology"', html)

    def test_services_cards_keep_clear_routes_and_plain_language(self):
        html = self.read("services.html")
        self.assertEqual(9, html.count('class="service-card '))
        cards = re.findall(r'<article class="service-card .*?</article>', html, re.S)
        self.assertEqual(9, len(cards))
        for card in cards:
            self.assertIn('service-card__link', card)
            self.assertRegex(card, r'href="(?:treatments/[^"#]+\.html|treatments\.html#[^"]+)"')
            self.assertIn("Learn More", card)
        self.assertIn("A clear place to begin", html)

    def test_treatment_directory_is_not_numbered_and_every_option_is_actionable(self):
        html = self.read("treatments.html")
        for label in ("01–02", "03–04", "05–06", "07–08", "09–10"):
            self.assertNotIn(label, html)
        self.assertIn('class="treatment-catalog"', html)
        self.assertGreaterEqual(html.count('class="treatment-option'), 10)
        options = re.findall(r'<a class="treatment-option.*?</a>', html, re.S)
        self.assertGreaterEqual(len(options), 10)
        for option in options:
            self.assertRegex(option, r'href="(?:treatments/[^"#]+\.html|services\.html#[^"]+)"')
            self.assertIn("treatment-option__arrow", option)
        self.assertIn("Choose a service", html)

    def test_treatment_directory_preserves_official_h3_catalogue(self):
        html = self.read("treatments.html")
        expected = {
            "Implantology", "Orthodontics", "Periodontics", "Pedodontics",
            "Endodontics", "Cosmetic Dentistry", "Preventive Treatments",
            "Oral Hygiene", "Laser Dentistry", "Prosthodontics",
        }
        directory = html.split('<section class="treatment-directory">', 1)[1].split('<div class="container"><div class="urgent-guidance">', 1)[0]
        headings = set(re.findall(r"<h3>(.*?)</h3>", directory, re.S))
        self.assertEqual(expected, headings)

    def test_services_and_treatments_css_cover_keyboard_and_mobile_cards(self):
        services_css = self.read("services.css")
        treatment_css = self.read("treatment-pages.css")
        for selector in (".services-start__card", ".service-card:focus-within", ".service-card__link"):
            self.assertIn(selector, services_css)
        for selector in (".treatment-catalog", ".treatment-option", ".treatment-option:focus-visible"):
            self.assertIn(selector, treatment_css)
        self.assertIn("grid-template-columns:1fr", treatment_css)


if __name__ == "__main__":
    unittest.main()
