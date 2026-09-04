from pathlib import Path
import json
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


def translate(values):
    script = r'''
const api = require('./language.js');
const values = JSON.parse(process.argv[1]);
process.stdout.write(JSON.stringify(values.map(value => api.translate(value, 'ar'))));
'''
    result = subprocess.run(
        ["node", "-e", script, json.dumps(values, ensure_ascii=False)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


class ArabicCompletionContract(unittest.TestCase):
    def test_implant_page_copy_is_translated_as_complete_arabic_phrases(self):
        values = [
            "Dental Implants in",
            "Missing a tooth or several teeth? Implant treatment starts with an assessment of your oral health, bone, bite and the restoration you may need.",
            "Next step",
            "Clinical assessment before treatment planning",
            "At a glance",
            "Implant care, planned around the restoration.",
            "What are dental implants?",
            "Dental implants can support a replacement tooth or an implant-supported restoration when a patient is clinically suitable. The restoration is planned around the missing tooth or teeth, the bite and the surrounding tissues.",
            "Who may be suitable?",
            "Digital planning",
            "Doctors for implant care",
            "Is everyone suitable for dental implants?",
            "Do all implant cases use guided surgery?",
            "How do I know which implant restoration I need?",
            "Location & directions →",
        ]
        translated = translate(values)
        for source, value in zip(values, translated):
            self.assertNotEqual(value, source, source)
            self.assertRegex(value, r"[\u0600-\u06ff]", source)

    def test_all_treatment_detail_pages_translate_their_primary_headings_and_leads(self):
        values = [
            "Cosmetic Dentistry in",
            "Thinking about changing the colour, shape or appearance of your smile? The first step is to understand the health of the teeth and which options are appropriate.",
            "Emergency Dentist in",
            "Dental pain or a broken tooth can be difficult to ignore. Call the centre first so we can check clinic availability and help direct the next step.",
            "General Dentistry in",
            "For routine dental concerns, check-ups or a problem you are not sure how to classify, a general dentist is usually the best place to start.",
            "Orthodontics in",
            "Concerned about tooth alignment or your bite? Our orthodontic specialists assess the problem first, then discuss the treatment options that fit the case.",
        ]
        translated = translate(values)
        for source, value in zip(values, translated):
            self.assertNotEqual(value, source, source)
            self.assertRegex(value, r"[\u0600-\u06ff]", source)

    def test_shared_detail_labels_have_natural_arabic(self):
        values = [
            "Meet Dr. Munir",
            "Bani Yas Tower, Abu Dhabi",
            "Assessment before treatment",
            "Digital planning where appropriate",
            "Specialist prosthodontic input",
            "What to expect",
            "Assessment",
            "Treatment approach",
            "Your next step",
            "Speak with the team",
            "Location & directions →",
        ]
        translated = translate(values)
        for source, value in zip(values, translated):
            self.assertNotEqual(value, source, source)
            self.assertRegex(value, r"[\u0600-\u06ff]", source)

    def test_language_query_is_carried_to_nested_pages_without_losing_existing_query_or_hash(self):
        script = r'''
const api = require('./language.js');
const values = [
  api.withLanguageQuery('treatments/dental-implants.html?from=home#what-are-dental-implants', 'ar'),
  api.withLanguageQuery('../doctors/dr-munir-silwadi.html#profile', 'ar'),
  api.withLanguageQuery('treatments/dental-implants.html?from=home&lang=ar#what-are-dental-implants', 'en')
];
process.stdout.write(JSON.stringify(values));
'''
        result = subprocess.run(
            ["node", "-e", script], cwd=ROOT, text=True, capture_output=True, check=True
        )
        self.assertEqual(
            json.loads(result.stdout),
            [
                "treatments/dental-implants.html?from=home&lang=ar#what-are-dental-implants",
                "../doctors/dr-munir-silwadi.html?lang=ar#profile",
                "treatments/dental-implants.html?from=home#what-are-dental-implants",
            ],
        )

    def test_treatment_pages_load_language_before_app(self):
        for page in (ROOT / "treatments").glob("*.html"):
            source = page.read_text(encoding="utf-8")
            self.assertLess(
                source.index('<script src="../language.js"></script>'),
                source.index('<script src="../app.js"></script>'),
                page.name,
            )


if __name__ == "__main__":
    unittest.main()
