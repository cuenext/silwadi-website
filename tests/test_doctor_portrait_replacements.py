from pathlib import Path
import hashlib
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
DOCTORS_HTML = (ROOT / "doctors.html").read_text(encoding="utf-8")
ASSET_DIR = ROOT / "assets" / "doctors" / "optimized"

PORTRAITS = {
    "dr-munir-silwadi": ("Dr. Munir Silwadi", "57c214d8da907c062275ea83041bfdd6dbd6ce662f6bce5adb7ac08b1d4ac724"),
    "dr-dana-awad": ("Dr. Dana Awad", "a36694f20c093a82eff235da2728fd6fa62a6a264de21c92c4136b835daf9719"),
    "dr-sara-ismail": ("Dr. Sara Ismail", "f3427aad1aa6a5d8e9d32703c8aee58f61ea5393abf940675fb5004af0214577"),
    "dr-kashmira-pawar-jayprakash": ("Dr. Kashmira Pawar Jayprakash", "f369814cfb954c60204e8c18fba7f5cb0b59550d0e955734f7af63aaf5570ca5"),
    "dr-nachiket-shah": ("Dr. Nachiket Shah", "0852998fcfc6525a129d726dcb8e9ee702c75287a7a623d86434a650cc67ce81"),
    "dr-hani-hasbini": ("Dr. Hani Hasbini", "c38477fa1e6badd47ba454797e157db41c1ada36a152046abd0e6c8d5a3a2c3e"),
    "dr-ahmed-el-shehri": ("Dr. Ahmed El Shehri", "bbb8a98b35792682e9880b7b0baec12e2086aace075083d2035e37909c68d53a"),
    "dr-fahed-khalil": ("Dr. Fahed Abi Khalil", "1b47ddc6b6cff953a05f00e293509087764a404107e96c0af1951c30fe72b4e1"),
    "dr-moheb-silwadi": ("Dr. Moheb Silwadi", "b8ccfb6b42b5d58f28994c1a8ef19c4489eec61626e2858be9767e86817a5dbf"),
    "dr-afnan-mashal": ("Dr. Afnan Mashal", "7de7450e5e989dc95a0c3cdf18012b34c24e498c03b96aaec7e3120956b5bf2f"),
}

ORIGINAL_DIRECTORY_ORDER = [
    "Dr. Afnan Mashal",
    "Dr. Moheb Silwadi",
    "Dr. Ehab Hassouneh Bassam A",
    "Dr. Sara Ismail",
    "Dr. Nasr Keshkiea",
    "Dr. Dana Awad",
    "Dr. Munir Silwadi",
    "Dr. Ahmed El Shehri",
    "Dr. Fahed Abi Khalil",
    "Dr. Moammar Mohamed Rifai",
    "Dr. Hani Hasbini",
    "Dr. Krishnamurthy Balajee",
    "Dr. Kashmira Pawar Jayprakash",
    "Dr. Nachiket Shah",
    "Dr. Lana Masoud",
]


class DoctorPortraitReplacementTests(unittest.TestCase):
    def test_directory_order_is_unchanged(self):
        actual = re.findall(r'data-name="([^"]+)"', DOCTORS_HTML)
        self.assertEqual(actual, ORIGINAL_DIRECTORY_ORDER)

    def test_all_ten_directory_cards_use_the_new_portrait_paths(self):
        for slug, (name, _) in PORTRAITS.items():
            card = re.search(
                rf'<article[^>]*data-name="{re.escape(name)}".*?</article>',
                DOCTORS_HTML,
                re.S,
            )
            self.assertIsNotNone(card, name)
            html = card.group(0)
            self.assertIn(f'assets/doctors/optimized/{slug}.webp', html)
            self.assertNotIn('doctor-directory-card__photo--placeholder', html)

    def test_replacement_assets_match_the_approved_uploads(self):
        for slug, (_, expected_sha256) in PORTRAITS.items():
            path = ASSET_DIR / f"{slug}.webp"
            self.assertTrue(path.is_file(), slug)
            self.assertEqual(path.read_bytes()[:4], b"RIFF", slug)
            self.assertEqual(path.read_bytes()[8:12], b"WEBP", slug)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected_sha256, slug)

    def test_individual_profiles_use_the_same_new_portraits(self):
        for slug, (name, _) in PORTRAITS.items():
            profile_path = ROOT / "doctors" / f"{slug}.html"
            self.assertTrue(profile_path.is_file(), slug)
            profile = profile_path.read_text(encoding="utf-8")
            self.assertIn(f'../assets/doctors/optimized/{slug}.webp', profile, name)
            self.assertNotRegex(profile, r'consultant-portrait__frame doctor-profile-placeholder', name)


if __name__ == "__main__":
    unittest.main()
