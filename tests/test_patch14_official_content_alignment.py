from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_SERVICES = {
    "Implantology",
    "Orthodontics",
    "Periodontics",
    "Pedodontics",
    "Endodontics",
    "Cosmetic Dentistry",
    "Preventive Treatments",
    "Oral Hygiene",
    "Laser Dentistry",
    "Prosthodontics",
}


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def section(html, marker, next_marker):
    return html.split(marker, 1)[1].split(next_marker, 1)[0]


class PatchFourteenOfficialContentAlignment(unittest.TestCase):
    def test_treatment_directory_uses_exact_official_service_catalogue(self):
        html = read("treatments.html")
        directory = section(
            html,
            '<section class="treatment-directory">',
            '<section class="consultation-cta">',
        )
        titles = set(re.findall(r"<h3>(.*?)</h3>", directory, re.S))
        self.assertEqual(titles, OFFICIAL_SERVICES)

    def test_home_featured_treatments_are_official_service_names(self):
        html = read("index.html")
        featured = section(html, '<section class="section" id="treatments">', '<section class="section section--quiet"')
        titles = set(re.findall(r"<h3>(.*?)</h3>", featured, re.S))
        self.assertTrue(titles)
        self.assertTrue(titles.issubset(OFFICIAL_SERVICES), titles - OFFICIAL_SERVICES)
        self.assertNotIn("Cosmetic & Restorative Dentistry", featured)
        self.assertNotIn("General & Preventive Care", featured)

    def test_home_does_not_claim_unverified_founder_status(self):
        self.assertNotIn("Founder & specialist", read("index.html"))

    def test_home_and_about_reflect_official_patient_care_values(self):
        combined = (read("index.html") + read("about.html")).lower()
        for concept in ("patient-centred", "comfort", "education", "communication", "personalized"):
            self.assertIn(concept, combined)

    def test_contact_states_verified_insurance_claim_handling(self):
        text = read("contact.html").lower()
        self.assertIn("accepts insurance", text)
        self.assertIn("most claims", text)
        self.assertIn("electronically", text)

    def test_locations_states_verified_parking_availability(self):
        html = read("locations.html")
        self.assertRegex(html, r"<dt>Parking</dt>\s*<dd>Available</dd>")

    def test_digital_dentistry_remains_a_capability_not_official_service_line(self):
        html = read("treatments.html")
        directory = section(
            html,
            '<section class="treatment-directory">',
            '<section class="consultation-cta">',
        )
        self.assertNotIn("<h3>Digital Dentistry</h3>", directory)


if __name__ == "__main__":
    unittest.main()
