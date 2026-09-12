from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DOCTORS = ROOT / "doctors"

RISKY_ADVERTISING_PHRASES = (
    "pain-free",
    "painless",
    "stress-free",
    "anxiety-free",
    "top-tier",
    "highest standard",
    "the best",
    "best dentist",
    "best dental",
    "world-class",
    "guaranteed",
    "guarantee",
    "completely at ease",
    "eliminating pain",
    "predictable treatment journey",
    "predictable treatments",
    "predictable outcomes",
    "lasting smile reconstruction",
)


class DoctorProfileAdvertisingCompliance(unittest.TestCase):
    def test_all_doctor_profiles_avoid_high_risk_promotional_claims(self):
        failures = []
        for path in sorted(DOCTORS.glob("*.html")):
            source = path.read_text(encoding="utf-8").lower()
            hits = [phrase for phrase in RISKY_ADVERTISING_PHRASES if phrase in source]
            if hits:
                failures.append(f"{path.name}: {', '.join(hits)}")
        self.assertFalse(failures, "High-risk advertising wording found:\n" + "\n".join(failures))

    def test_uploaded_source_profiles_are_represented_with_supported_facts(self):
        expectations = {
            "dr-lana-masoud.html": (
                "Dr. Lana Almasoud",
                "Gulf Medical University",
                "Master",
                "Thumbay Dental Hospital",
                "CBCT",
                "microscope",
            ),
            "dr-ehab-hassouneh.html": (
                "RAK College of Dental Sciences",
                "Nitrous Oxide Conscious Sedation",
                "Professional Dental Bleaching",
                "quality control",
            ),
            "dr-nachiket-shah.html": (
                "14 years",
                "MDS in Periodontology and Implantology",
                "UniCamillus",
                "Royal College of Surgeons in Ireland",
                "Er:YAG",
            ),
            "dr-nasr-keshkiea.html": (
                "General Dentist",
                "Damascus University, 2017",
                "Removable Prosthodontics",
                "Hama University, 2022",
                "Syrian Board Certification",
            ),
            "dr-kashmira-pawar-jayprakash.html": (
                "nine years",
                "MDS in Pediatric Dentistry",
                "RGUHS",
                "PALS",
                "BLS",
                "Nitrous Oxide Conscious Sedation",
            ),
        }
        failures = []
        for filename, required in expectations.items():
            source = (DOCTORS / filename).read_text(encoding="utf-8")
            missing = [value for value in required if value.lower() not in source.lower()]
            if missing:
                failures.append(f"{filename}: missing {', '.join(missing)}")
        self.assertFalse(failures, "Source-backed profile facts missing:\n" + "\n".join(failures))

    def test_nasr_is_not_advertised_as_an_abu_dhabi_specialist(self):
        source = (DOCTORS / "dr-nasr-keshkiea.html").read_text(encoding="utf-8")
        self.assertIn("General Dentist", source)
        self.assertNotIn('jobTitle":"Specialist Prosthodontist', source)
        self.assertNotIn("Specialist Prosthodontist Abu Dhabi", source)


if __name__ == "__main__":
    unittest.main()
