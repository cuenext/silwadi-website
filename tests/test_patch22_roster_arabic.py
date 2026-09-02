from pathlib import Path
import json
import re
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]

APPROVED_DOCTORS = [
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

REMOVED_DOCTORS = [
    "Dr. Mohammed Abualkas",
    "Dr. Reem Alshaer",
    "Dr. Hawra'a Al Ameri",
    "Dr. Ibrahem Abu Shanab",
]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class ApprovedDoctorRosterContract(unittest.TestCase):
    def test_directory_contains_exactly_the_approved_fifteen_doctors(self):
        html = read("doctors.html")
        displayed = re.findall(r'data-doctor-card[^>]+data-name="([^"]+)"', html)
        self.assertCountEqual(displayed, APPROVED_DOCTORS)
        self.assertEqual(len(displayed), 15)
        self.assertIn("15 dentists &amp; specialists", html)

    def test_removed_doctors_are_not_featured_anywhere_patient_facing(self):
        patient_facing = read("index.html") + read("doctors.html")
        for doctor in REMOVED_DOCTORS:
            self.assertNotIn(doctor, patient_facing)

    def test_dana_profile_uses_the_supplied_bio_without_inventing_a_portrait(self):
        html = read("doctors/dr-dana-awad.html")
        for phrase in [
            "Dr. Dana Awad",
            "General Dentist",
            "Bachelor of Dental Surgery (BDS)",
            "Istanbul Medipol University",
            "University of Sharjah",
            "Diploma in Esthetic Dentistry",
            "Preventive &amp; Periodontal Care",
            "Restorative Dentistry",
            "Esthetic Dentistry",
            "Comprehensive General Dentistry",
            "Philosophy of Care",
        ]:
            self.assertIn(phrase, html)
        self.assertIn("../assets/doctors/optimized/dr-dana-awad.webp", html)


class ArabicLanguageExperienceContract(unittest.TestCase):
    def test_every_patient_facing_page_loads_language_support_before_app(self):
        pages = [
            *ROOT.glob("*.html"),
            *(ROOT / "doctors").glob("*.html"),
            *(ROOT / "treatments").glob("*.html"),
        ]
        self.assertGreaterEqual(len(pages), 20)
        for page in pages:
            html = page.read_text(encoding="utf-8")
            prefix = "../" if page.parent != ROOT else ""
            language_tag = f'<script src="{prefix}language.js"></script>'
            app_tag = f'<script src="{prefix}app.js"></script>'
            self.assertIn(language_tag, html, page.name)
            self.assertIn(app_tag, html, page.name)
            self.assertLess(html.index(language_tag), html.index(app_tag), page.name)

    def test_language_module_switches_label_direction_and_persists_choice(self):
        script = r'''
const fs = require('fs');
const vm = require('vm');
const attrs = {};
const storage = {};
const headerActions = { children: [], prepend(node) { this.children.unshift(node); } };
const doc = {
  documentElement: { setAttribute(k, v) { attrs[k] = v; } },
  body: { classList: { toggle() {} } },
  querySelector(selector) { return selector === '.header-actions' ? headerActions : null; },
  querySelectorAll() { return []; },
  createElement() { return { className: '', type: '', textContent: '', attrs: {}, setAttribute(k,v){ this.attrs[k]=v; }, addEventListener(type, fn){ this.click=fn; } }; },
};
const context = {
  window: {}, document: doc,
  localStorage: { getItem(k){ return storage[k] || null; }, setItem(k,v){ storage[k]=v; } },
  NodeFilter: { SHOW_TEXT: 4 },
};
context.window = context;
vm.runInNewContext(fs.readFileSync('language.js', 'utf8'), context);
context.SilwadiLanguage.init();
const button = headerActions.children[0];
const before = { label: button.textContent, lang: attrs.lang, dir: attrs.dir };
button.click();
const after = { label: button.textContent, lang: attrs.lang, dir: attrs.dir, stored: storage['silwadi-language'] };
process.stdout.write(JSON.stringify({ before, after, doctor: context.SilwadiLanguage.translate('Find a Doctor', 'ar') }));
'''
        result = subprocess.run(
            ["node", "-e", script], cwd=ROOT, text=True, capture_output=True, check=True
        )
        state = json.loads(result.stdout)
        self.assertEqual(state["before"], {"label": "عربي", "lang": "en", "dir": "ltr"})
        self.assertEqual(state["after"], {"label": "English", "lang": "ar", "dir": "rtl", "stored": "ar"})
        self.assertEqual(state["doctor"], "ابحث عن طبيب")

    def test_doctor_directory_has_natural_arabic_clinical_labels(self):
        script = r'''
const api = require('./language.js');
const values = [
  'Doctors', 'General Dentist', 'Orthodontics', 'Search doctors',
  'Name or specialty', 'Book a Consultation', '15 dentists & specialists'
];
process.stdout.write(JSON.stringify(values.map(value => api.translate(value, 'ar'))));
'''
        result = subprocess.run(
            ["node", "-e", script], cwd=ROOT, text=True, capture_output=True, check=True
        )
        translated = json.loads(result.stdout)
        self.assertEqual(translated, [
            "الأطباء", "طبيب أسنان عام", "تقويم الأسنان", "ابحث عن طبيب",
            "الاسم أو التخصص", "احجز استشارة", "15 طبيباً واختصاصياً",
        ])


if __name__ == "__main__":
    unittest.main()
