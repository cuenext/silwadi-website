import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DoctorProfileRefreshContract(unittest.TestCase):
    def read(self, path):
        return (ROOT / path).read_text(encoding="utf-8")

    def test_english_profiles_use_submitted_professional_content(self):
        expected = {
            "doctors/dr-kashmira-pawar-jayprakash.html": [
                "over nine years of clinical experience",
                "MDS in Pediatric Dentistry",
                "Nitrous Oxide Conscious Sedation",
            ],
            "doctors/dr-nasr-keshkiea.html": [
                "over eight years of clinical experience",
                "Master of Science in Removable Prosthodontics",
                "Syrian Board Certification in Removable Prosthodontics",
            ],
            "doctors/dr-ehab-hassouneh.html": [
                "Bachelor of Dental Surgery from RAK College of Dental Sciences",
                "CAD/CAM",
                "Nitrous Oxide Conscious Sedation",
            ],
            "doctors/dr-nachiket-shah.html": [
                "more than 14 years of clinical experience",
                "UniCamillus",
                "Royal College of Surgeons in Ireland",
            ],
            "doctors/dr-sara-ismail.html": [
                "DDS from Ajman University",
                "Diploma in Advanced Esthetic Dentistry",
                "Arabic and English",
            ],
        }
        for path, snippets in expected.items():
            text = self.read(path)
            for snippet in snippets:
                self.assertIn(snippet, text, f"{path} missing {snippet!r}")

    def test_profiles_avoid_promotional_or_guarantee_language(self):
        banned = [
            "pain-free",
            "stress-free",
            "predictable treatment journey",
            "predictable outcomes",
            "highly skilled",
            "distinguished Specialist",
            "expert Pediatric Care",
            "completely at ease",
        ]
        paths = [
            "doctors/dr-kashmira-pawar-jayprakash.html",
            "doctors/dr-nasr-keshkiea.html",
            "doctors/dr-ehab-hassouneh.html",
            "doctors/dr-nachiket-shah.html",
            "doctors/dr-sara-ismail.html",
        ]
        for path in paths:
            text = self.read(path).lower()
            for phrase in banned:
                self.assertNotIn(phrase.lower(), text, f"{path} contains banned phrase {phrase!r}")

    def test_nasr_public_title_remains_general_dentist(self):
        text = self.read("doctors/dr-nasr-keshkiea.html")
        self.assertIn('<p class="consultant-specialty">General Dentist</p>', text)
        self.assertNotIn('<p class="consultant-specialty">Prosthodontic Specialist</p>', text)

    def test_ehab_uses_new_portrait_asset(self):
        text = self.read("doctors/dr-ehab-hassouneh.html")
        directory = self.read("doctors.html")
        self.assertIn("dr-ehab-new-v2.webp", text)
        self.assertIn("dr-ehab-new-v2.webp", directory)
        self.assertTrue((ROOT / "assets/dr-ehab-new-v2.webp").exists())

    def test_arabic_profiles_are_refreshed(self):
        expected = {
            "ar/doctors/dr-kashmira-pawar-jayprakash.html": "أكثر من تسع سنوات",
            "ar/doctors/dr-nasr-keshkiea.html": "أكثر من ثماني سنوات",
            "ar/doctors/dr-ehab-hassouneh.html": "كلية رأس الخيمة لطب الأسنان",
            "ar/doctors/dr-nachiket-shah.html": "أكثر من 14 عاماً",
            "ar/doctors/dr-sara-ismail.html": "جامعة عجمان",
        }
        for path, snippet in expected.items():
            self.assertIn(snippet, self.read(path), f"{path} missing refreshed Arabic content")


if __name__ == "__main__":
    unittest.main()
