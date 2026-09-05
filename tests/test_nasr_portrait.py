import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGE = "dr-nasr-keshkiea.webp"
PUBLIC_IMAGE = f"https://silwadi.ae/assets/doctors/optimized/{IMAGE}"


class NasrPortraitContract(unittest.TestCase):
    def test_optimized_portrait_exists(self):
        portrait = ROOT / "assets" / "doctors" / "optimized" / IMAGE
        self.assertTrue(portrait.exists(), "Dr. Nasr's uploaded portrait must exist as an optimized WebP")
        self.assertGreater(portrait.stat().st_size, 10_000)

    def test_english_directory_uses_portrait_not_placeholder(self):
        html = (ROOT / "doctors.html").read_text(encoding="utf-8")
        self.assertIn(f'assets/doctors/optimized/{IMAGE}', html)
        nasr_card = html.split('data-name="Dr. Nasr Keshkiea"', 1)[1].split('</article>', 1)[0]
        self.assertNotIn('doctor-directory-card__photo--placeholder', nasr_card)
        self.assertNotIn('>NK<', nasr_card)

    def test_english_profile_uses_portrait_and_matching_metadata(self):
        html = (ROOT / "doctors" / "dr-nasr-keshkiea.html").read_text(encoding="utf-8")
        self.assertIn(f'../assets/doctors/optimized/{IMAGE}', html)
        self.assertNotIn('doctor-profile-placeholder', html)
        self.assertNotIn('>NK<', html)
        self.assertIn(f'<meta property="og:image" content="{PUBLIC_IMAGE}">', html)
        self.assertIn(f'"image":"{PUBLIC_IMAGE}"', html)
        self.assertNotIn('assets/doctors/dr-moheb-silwadi.png', html)

    def test_arabic_directory_and_profile_use_same_portrait(self):
        directory = (ROOT / "ar" / "doctors.html").read_text(encoding="utf-8")
        profile = (ROOT / "ar" / "doctors" / "dr-nasr-keshkiea.html").read_text(encoding="utf-8")
        self.assertIn(IMAGE, directory)
        self.assertIn(IMAGE, profile)
        self.assertNotIn('doctor-profile-placeholder', profile)
        self.assertIn(PUBLIC_IMAGE, profile)


if __name__ == "__main__":
    unittest.main()
