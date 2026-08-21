from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


class PatchOneHomeContract(unittest.TestCase):
    def test_home_uses_approved_hospital_hero(self):
        html = read("index.html")
        self.assertIn("Advanced dentistry. Established trust.", html)
        self.assertIn("Book a Consultation", html)
        self.assertIn("Find a Doctor", html)
        self.assertNotIn("float-pill", html)
        self.assertNotIn("marquee", html.lower())

    def test_home_is_selective_not_crowded(self):
        html = read("index.html")
        self.assertEqual(len(re.findall(r'class="treatment-path\b', html)), 4)
        self.assertEqual(len(re.findall(r'class="doctor-card\b', html)), 4)
        self.assertIn("Serving Abu Dhabi since 1980", html)
        self.assertIn("Not sure which dentist you need?", html)

    def test_essential_home_content_is_in_html_not_generated_by_js(self):
        js = read("app.js")
        self.assertNotIn("const doctors=", js)
        self.assertNotIn("const services=", js)
        self.assertNotIn("innerHTML=doctors.map", js)
        self.assertNotIn("innerHTML=services.map", js)

    def test_logo_and_doctor_assets_resolve(self):
        html = read("index.html")
        for src in re.findall(r'<img[^>]+src="([^"]+)"', html, re.I):
            if src.startswith(("http:", "https:", "data:")):
                continue
            self.assertTrue((ROOT / src).is_file(), src)

    def test_home_has_one_h1_and_accessible_images(self):
        html = read("index.html")
        self.assertEqual(len(re.findall(r"<h1\b", html, re.I)), 1)
        for tag in re.findall(r"<img\b[^>]*>", html, re.I):
            self.assertRegex(tag, r'\balt="[^"]+"')


if __name__ == "__main__":
    unittest.main()
