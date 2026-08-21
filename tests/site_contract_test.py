from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

def read(name):
    return (ROOT / name).read_text(encoding='utf-8')

class PatchOneHomeContract(unittest.TestCase):
    def test_home_uses_approved_hospital_hero(self):
        html = read('index.html')
        self.assertIn('Advanced dentistry. Established trust.', html)
        self.assertIn('Book a Consultation', html)
        self.assertIn('Find a Doctor', html)
        self.assertNotIn('float-pill', html)
        self.assertNotIn('marquee', html.lower())

    def test_home_is_selective_not_crowded(self):
        html = read('index.html')
        self.assertEqual(len(re.findall(r'class="treatment-path\b', html)), 4)
        self.assertEqual(len(re.findall(r'class="doctor-card\b', html)), 4)
        self.assertIn('Serving Abu Dhabi since 1980', html)
        self.assertIn('Not sure which dentist you need?', html)

    def test_essential_home_content_is_in_html_not_generated_by_js(self):
        js = read('app.js')
        self.assertNotIn('const doctors=', js)
        self.assertNotIn('const services=', js)
        self.assertNotIn('innerHTML=doctors.map', js)
        self.assertNotIn('innerHTML=services.map', js)

    def test_logo_and_doctor_assets_resolve(self):
        html = read('index.html')
        for src in re.findall(r'<img[^>]+src="([^"]+)"', html, re.I):
            if src.startswith(('http:', 'https:', 'data:')):
                continue
            self.assertTrue((ROOT / src).is_file(), src)

    def test_home_has_one_h1_and_accessible_images(self):
        html = read('index.html')
        self.assertEqual(len(re.findall(r'<h1\b', html, re.I)), 1)
        for tag in re.findall(r'<img\b[^>]*>', html, re.I):
            self.assertRegex(tag, r'\balt="[^"]+"')


class PatchTwoDoctorsContract(unittest.TestCase):
    def test_doctors_directory_contains_current_roster_and_filters(self):
        html = read('doctors.html')
        for name in [
            'Dr. Munir Silwadi', 'Dr. Moheb Silwadi', 'Dr. Hani Hasbini',
            'Dr. Moammer Rifai', 'Dr. Ahmed El Shehri', 'Dr. Fahed Khalil',
            'Dr. Mohammed Abualkas', 'Dr. Reem Alshaer', 'Dr. Afnan Mashal',
            "Dr. Hawra'a Al Ameri", 'Dr. Ibrahem Abu Shanab',
            'Dr. Krishnamurthy Katta Balajee'
        ]:
            self.assertIn(name, html)
        self.assertIn('data-doctor-search', html)
        self.assertIn('data-specialty-filter', html)
        self.assertIn('href="doctors/dr-munir-silwadi.html"', html)
        self.assertEqual(html.count('data-doctor-card'), 12)

    def test_doctor_directory_uses_real_assets_and_accessible_images(self):
        html = read('doctors.html')
        for src in re.findall(r'<img[^>]+src="([^"]+)"', html, re.I):
            self.assertTrue((ROOT / src).is_file(), src)
        for tag in re.findall(r'<img\b[^>]*>', html, re.I):
            self.assertRegex(tag, r'\balt="[^"]+"')

    def test_munir_profile_has_consultant_structure(self):
        html = read('doctors/dr-munir-silwadi.html')
        self.assertIn('Specialist Prosthodontist &amp; Implantologist', html)
        self.assertIn('Clinical focus', html)
        self.assertIn('Qualifications', html)
        self.assertIn('Book a consultation with Dr. Munir Silwadi', html)
        self.assertIn('Bani Yas Tower', html)
        self.assertEqual(len(re.findall(r'<h1\b', html, re.I)), 1)

    def test_doctor_filter_behavior_is_in_shared_javascript(self):
        js = read('app.js')
        self.assertIn('data-doctor-search', js)
        self.assertIn('data-specialty-filter', js)
        self.assertIn('data-doctor-card', js)
        self.assertIn('filterDoctors', js)

    def test_home_routes_to_new_doctor_pages(self):
        html = read('index.html')
        self.assertIn('href="doctors.html"', html)
        self.assertIn('href="doctors/dr-munir-silwadi.html"', html)


class PatchThreeTreatmentsContract(unittest.TestCase):
    def test_treatments_directory_has_approved_groups(self):
        html = read('treatments.html')
        for heading in ['Implant &amp; Restorative', 'Smile &amp; Aesthetic', 'Specialist Dentistry', 'Routine Care']:
            self.assertIn(heading, html)
        for treatment in ['Dental Implants', 'Prosthodontics', 'Orthodontics', 'Endodontics', 'Periodontics', 'Pediatric Dentistry', 'General Dentistry', 'Preventive Care', 'Oral Hygiene']:
            self.assertIn(treatment, html)
        self.assertIn('href="treatments/dental-implants.html"', html)
        self.assertEqual(len(re.findall(r'<h1\b', html, re.I)), 1)

    def test_implants_page_has_responsible_treatment_structure(self):
        html = read('treatments/dental-implants.html')
        for heading in ['Dental Implants', 'What are dental implants?', 'Who may be suitable?', 'Planning your treatment', 'Digital planning', 'Doctors for implant care', 'Frequently asked questions']:
            self.assertIn(heading, html)
        self.assertIn('../doctors/dr-munir-silwadi.html', html)
        self.assertIn('selected cases', html.lower())
        self.assertIn('clinical assessment', html.lower())
        self.assertNotIn('guarantee', html.lower())
        self.assertEqual(len(re.findall(r'<h1\b', html, re.I)), 1)

    def test_home_and_munir_profile_route_to_treatments(self):
        home = read('index.html')
        profile = read('doctors/dr-munir-silwadi.html')
        self.assertIn('href="treatments.html"', home)
        self.assertIn('href="treatments/dental-implants.html"', home)
        self.assertIn('../treatments/dental-implants.html', profile)


class PatchFourContactContract(unittest.TestCase):
    def test_contact_page_is_real_consultation_destination(self):
        path = ROOT / 'contact.html'
        self.assertTrue(path.is_file(), 'contact.html')
        html = read('contact.html')
        self.assertIn('id="consultation"', html)
        self.assertIn('Contact &amp; Consultations', html)
        self.assertIn('+971 2 626 2042', html)
        self.assertIn('info@silwadidentalcentres.ae', html)
        self.assertIn('Bani Yas Tower', html)
        self.assertIn('Insurance', html)
        self.assertNotIn('<form', html.lower())

    def test_shared_javascript_routes_consultation_ctas_to_contact(self):
        js = read('app.js')
        self.assertIn('routeConsultationCtas', js)
        self.assertIn('contact.html#consultation', js)
        self.assertIn('book a consultation', js.lower())
        self.assertIn('consultationMail', js)

    def test_contact_page_exposes_direct_call_and_email_fallbacks(self):
        html = read('contact.html')
        self.assertIn('href="tel:+97126262042"', html)
        self.assertIn('href="mailto:info@silwadidentalcentres.ae?subject=Consultation%20Request"', html)
        self.assertIn('Choose how you would like to contact the centre', html)


if __name__ == '__main__':
    unittest.main()
