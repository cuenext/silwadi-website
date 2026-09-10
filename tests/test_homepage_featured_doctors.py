import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def featured_profile_hrefs(path: str):
    text = (ROOT / path).read_text(encoding="utf-8")
    match = re.search(
        r'<div class="featured-doctors">(.*?)<div class="section-link reveal">',
        text,
        flags=re.S,
    )
    if not match:
        raise AssertionError(f"featured-doctors section not found in {path}")
    return re.findall(r'<a href="([^"]+)">(?:View profile|عرض الملف)', match.group(1))


class HomepageFeaturedDoctorsContract(unittest.TestCase):
    def test_english_featured_doctors_exact_order(self):
        self.assertEqual(
            featured_profile_hrefs("index.html"),
            [
                "doctors/dr-moheb-silwadi.html",
                "doctors/dr-lana-masoud.html",
                "doctors/dr-kashmira-pawar-jayprakash.html",
                "doctors/dr-dana-awad.html",
                "doctors/dr-ahmed-el-shehri.html",
            ],
        )
        text = (ROOT / "index.html").read_text(encoding="utf-8")
        section = re.search(r'<div class="featured-doctors">(.*?)<div class="section-link reveal">', text, re.S).group(1)
        self.assertIn("Dr. Lana Almasoud", section)
        self.assertIn("assets/dr-lana-new.png", section)

    def test_arabic_featured_doctors_exact_order(self):
        self.assertEqual(
            featured_profile_hrefs("ar/index.html"),
            [
                "/ar/doctors/dr-moheb-silwadi.html",
                "/ar/doctors/dr-lana-masoud.html",
                "/ar/doctors/dr-kashmira-pawar-jayprakash.html",
                "/ar/doctors/dr-dana-awad.html",
                "/ar/doctors/dr-ahmed-el-shehri.html",
            ],
        )
        text = (ROOT / "ar/index.html").read_text(encoding="utf-8")
        section = re.search(r'<div class="featured-doctors">(.*?)<div class="section-link reveal">', text, re.S).group(1)
        self.assertIn("د. لانا المسعود", section)
        self.assertIn("/assets/dr-lana-new.png", section)


if __name__ == "__main__":
    unittest.main()
