import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLINIC = ROOT / "ai/clinic-knowledge-v1.json"
DENTAL = ROOT / "ai/dental-guidance-v1.json"


class AiKnowledgeV1Contract(unittest.TestCase):
    def test_verified_branch_and_contact_facts(self):
        data = json.loads(CLINIC.read_text(encoding="utf-8"))
        self.assertEqual(data["contact"]["email"], "info@silwadidentalcentres.ae")
        self.assertEqual(data["contact"]["whatsapp"], "+971506260418")
        self.assertEqual(data["branches"]["bani-yas"]["phone"], "+971 2 626 2042")
        self.assertEqual(data["branches"]["al-raha"]["phone"], "+971 2 666 2408")
        self.assertIn("09:00–21:00", data["branches"]["bani-yas"]["hours"])
        self.assertIn("10:00–19:00", data["branches"]["al-raha"]["hours"])
        self.assertIn("Fri closed", data["branches"]["bani-yas"]["hours"])
        self.assertIn("Fri closed", data["branches"]["al-raha"]["hours"])

    def test_current_team_has_fifteen_doctors_and_critical_roles(self):
        data = json.loads(CLINIC.read_text(encoding="utf-8"))
        self.assertEqual(len(data["doctors"]), 15)
        doctors = {d["name"]: d for d in data["doctors"]}
        self.assertEqual(doctors["Dr. Kashmira Pawar Jayprakash"]["role"], "Specialist Pediatric Dentist")
        self.assertEqual(doctors["Dr. Lana Almasoud"]["role"], "Specialist Endodontist")
        self.assertEqual(doctors["Dr. Ahmed El Shehri"]["role"], "Specialist Endodontist")
        self.assertEqual(doctors["Dr. Munir Silwadi"]["role"], "Specialist Prosthodontist & Implantologist")
        self.assertEqual(doctors["Dr. Nasr Keshkiea"]["role"], "General Dentist")

    def test_services_match_public_service_directory(self):
        data = json.loads(CLINIC.read_text(encoding="utf-8"))
        for service in [
            "Prosthodontics",
            "Implantology",
            "Periodontics",
            "Endodontics",
            "Orthodontics",
            "Pedodontics",
            "Cosmetic Dentistry & Teeth Whitening",
            "Laser Dentistry",
            "Preventive Dentistry",
        ]:
            self.assertIn(service, data["services"])

    def test_clinic_data_forbids_unverified_live_claims(self):
        data = json.loads(CLINIC.read_text(encoding="utf-8"))
        rules = " ".join(data["clinicFactRules"]).lower()
        for concept in ["appointments", "prices", "insurance", "schedules"]:
            self.assertIn(concept, rules)

    def test_dental_guidance_has_required_safe_topics(self):
        data = json.loads(DENTAL.read_text(encoding="utf-8"))
        topics = {item["topic"] for item in data["guidance"]}
        for topic in [
            "bleeding-gums",
            "dental-x-rays",
            "first-child-dental-visit",
            "fluoride-toothpaste-children",
            "root-canal",
            "crowns",
            "whitening",
            "dental-implants",
            "brushing-and-interdental-cleaning",
        ]:
            self.assertIn(topic, topics)
        self.assertTrue(data["urgentRedFlags"])
        serialized = json.dumps(data).lower()
        self.assertNotIn("dosage", serialized)
        self.assertNotIn("prescribe", serialized)


if __name__ == "__main__":
    unittest.main()
