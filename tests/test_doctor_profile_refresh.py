import unittest
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit

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

    def test_ehab_uses_approved_portrait_asset(self):
        class Portraits(HTMLParser):
            def __init__(self):
                super().__init__()
                self.paths = []

            def handle_starttag(self, tag, attrs):
                if tag != "img":
                    return
                attrs = dict(attrs)
                if "doctor-crop-ehab" in attrs.get("class", "").split():
                    self.paths.append(urlsplit(attrs.get("src", "")).path)

        expected = "assets/dr-ehab-new.png"
        for page in (
            "doctors/dr-ehab-hassouneh.html",
            "ar/doctors/dr-ehab-hassouneh.html",
            "doctors.html",
            "ar/doctors.html",
        ):
            parser = Portraits()
            parser.feed(self.read(page))
            self.assertTrue(parser.paths, f"{page} missing Ehab portrait")
            for path in parser.paths:
                self.assertEqual(path.removeprefix("../").lstrip("/"), expected)
        self.assertTrue((ROOT / expected).is_file())

    def test_ehab_arabic_qualifications_and_clinical_focus_are_translated(self):
        text = self.read("ar/doctors/dr-ehab-hassouneh.html")
        translated = (
            "بكالوريوس جراحة الأسنان من كلية رأس الخيمة لطب الأسنان",
            "تدريب امتياز في طب الأسنان",
            "التهدئة الواعية باستخدام أكسيد النيتروز",
            "الترميز التأميني في أبوظبي",
            "طب الأسنان الترميمي والتجميلي",
            "طب الأسنان الرقمي والتركيبات السنية",
            "التقييم بالأشعة، وتنظيف الأسنان الدوري",
        )
        for phrase in translated:
            self.assertIn(phrase, text)
        for phrase in (
            "Bachelor of Dental Surgery",
            "Dental internship training",
            "Certifications in Nitrous Oxide",
            "Previous experience in healthcare",
            "Radiographic assessment, routine cleaning",
        ):
            self.assertNotIn(phrase, text)

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
