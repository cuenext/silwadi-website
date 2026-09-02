from pathlib import Path
import json
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

DOCTORS = {
    'dr-afnan-mashal': ('Dr. Afnan Mashal', 'General Dentist', 'dr-afnan-mashal.webp', 'Bani Yas Tower, Abu Dhabi'),
    'dr-moheb-silwadi': ('Dr. Moheb Silwadi', 'General Dentist', 'dr-moheb-silwadi.webp', 'Al Raha Mall, Abu Dhabi'),
    'dr-ehab-hassouneh': ('Dr. Ehab Hassouneh Bassam A', 'General Dentist', 'dr-ehab-hassouneh.webp', 'Al Raha Mall, Abu Dhabi'),
    'dr-sara-ismail': ('Dr. Sara Ismail', 'General Dentist', None, 'Al Raha Mall, Abu Dhabi'),
    'dr-nasr-keshkiea': ('Dr. Nasr Keshkiea', 'General Dentist', None, 'Bani Yas Tower, Abu Dhabi'),
    'dr-dana-awad': ('Dr. Dana Awad', 'General Dentist', 'dr-dana-awad.webp', 'Bani Yas Tower, Abu Dhabi'),
    'dr-munir-silwadi': ('Dr. Munir Silwadi', 'Specialist Prosthodontist & Implantologist', 'dr-munir-silwadi.webp', 'Both locations, Abu Dhabi'),
    'dr-ahmed-el-shehri': ('Dr. Ahmed El Shehri', 'Endodontist', 'dr-ahmed-el-shehri.webp', 'Bani Yas Tower, Abu Dhabi'),
    'dr-fahed-khalil': ('Dr. Fahed Abi Khalil', 'Periodontist & Implantologist', 'dr-fahed-khalil.webp', 'Bani Yas Tower, Abu Dhabi'),
    'dr-moammar-rifai': ('Dr. Moammar Mohamed Rifai', 'Orthodontist', 'dr-moammer-rifai.webp', 'Bani Yas Tower, Abu Dhabi'),
    'dr-hani-hasbini': ('Dr. Hani Hasbini', 'Consultant Orthodontist', 'dr-hani-hasbini.webp', 'Bani Yas Tower, Abu Dhabi'),
    'dr-krishnamurthy-katta-balajee': ('Dr. Krishnamurthy Balajee', 'Orthodontist', 'dr-krishnamurthy-katta-balajee.webp', 'Both locations, Abu Dhabi'),
    'dr-kashmira-pawar-jayprakash': ('Dr. Kashmira Pawar Jayprakash', 'Pediatric Dentist', None, 'Al Raha Mall, Abu Dhabi'),
    'dr-nachiket-shah': ('Dr. Nachiket Shah', 'Periodontist & Implantologist', None, 'Al Raha Mall, Abu Dhabi'),
    'dr-lana-masoud': ('Dr. Lana Masoud', 'Endodontist', None, 'Al Raha Mall, Abu Dhabi'),
}
BANNED = ['best dentist', 'world-class', 'cutting-edge', 'state-of-the-art', 'guaranteed', 'pain-free', 'completely painless', 'personal promise', 'highest quality of care']

def read(rel): return (ROOT / rel).read_text(encoding='utf-8')

def jsonld_nodes(rel):
    blocks = re.findall(r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>', read(rel), re.I | re.S)
    nodes = []
    for block in blocks:
        parsed = json.loads(block)
        nodes.extend(parsed['@graph'] if isinstance(parsed, dict) and isinstance(parsed.get('@graph'), list) else [parsed])
    return nodes

class PatchTenDoctorAuthority(unittest.TestCase):
    def test_all_fifteen_profiles_exist_and_have_core_identity(self):
        for slug, (name, specialty, image, location) in DOCTORS.items():
            rel = f'doctors/{slug}.html'; path = ROOT / rel
            self.assertTrue(path.is_file(), rel); html = path.read_text(encoding='utf-8')
            h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.I | re.S)
            self.assertEqual(len(h1s), 1, rel); self.assertEqual(re.sub(r'<[^>]+>', '', h1s[0]).strip(), name, rel)
            self.assertIn(specialty, html, rel); self.assertIn(location, html, rel)
            self.assertIn(f'../assets/doctors/optimized/{image}', html, rel) if image else self.assertIn('doctor-profile-placeholder', html, rel)
            self.assertIn('../contact.html#consultation', html, rel); self.assertIn('../treatments.html', html, rel)
            for phrase in BANNED: self.assertNotIn(phrase, html.lower(), (rel, phrase))

    def test_every_profile_has_unique_metadata_breadcrumb_and_person_schema(self):
        titles, descriptions = [], []
        for slug, (name, specialty, image, _) in DOCTORS.items():
            rel = f'doctors/{slug}.html'; html = read(rel); canonical = f'https://silwadi.ae/{rel}'
            title = re.search(r'<title>(.*?)</title>', html, re.I | re.S); desc = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html, re.I)
            self.assertIsNotNone(title, rel); self.assertIsNotNone(desc, rel); self.assertIn('Abu Dhabi', title.group(1), rel)
            self.assertIn(f'<link rel="canonical" href="{canonical}">', html, rel); self.assertIn(f'<meta property="og:url" content="{canonical}">', html, rel)
            nodes = jsonld_nodes(rel); person = next((n for n in nodes if n.get('@type') == 'Person'), None); crumbs = next((n for n in nodes if n.get('@type') == 'BreadcrumbList'), None)
            self.assertIsNotNone(person, rel); self.assertIsNotNone(crumbs, rel); self.assertEqual(person['name'], name, rel); self.assertEqual(person['jobTitle'], specialty, rel)
            self.assertEqual(person['url'], canonical, rel); self.assertEqual(person['worksFor']['@id'], 'https://silwadi.ae/#dentist', rel)
            if image:
                expected = f'https://silwadi.ae/assets/doctors/{image.replace(".webp", ".png")}'
                if slug in {'dr-dana-awad', 'dr-ehab-hassouneh'}:
                    expected = f'https://silwadi.ae/assets/doctors/optimized/{image}'
                self.assertEqual(person['image'], expected, rel)
            else: self.assertNotIn('image', person, rel)
            self.assertEqual(len(crumbs['itemListElement']), 3, rel); titles.append(title.group(1).strip()); descriptions.append(desc.group(1).strip())
        self.assertEqual(len(titles), len(set(titles))); self.assertEqual(len(descriptions), len(set(descriptions)))

    def test_directory_links_every_approved_doctor_to_a_profile(self):
        html = read('doctors.html')
        for slug, (name, _, _, _) in DOCTORS.items(): self.assertIn(name, html); self.assertIn(f'href="doctors/{slug}.html"', html, slug)
        self.assertEqual(html.count('data-doctor-card'), 15); self.assertIn('15 dentists &amp; specialists', html)

    def test_verified_profile_facts_are_preserved_without_inventing_new_credentials(self):
        expectations = {
            'doctors/dr-moheb-silwadi.html': ['University of Jordan', '2008', 'Digital Smile Design', 'Dental implants'],
            'doctors/dr-hani-hasbini.html': ['Saint Joseph University', '1985', 'Paris VII University', '1989'],
            'doctors/dr-moammar-rifai.html': ['Lebanese University', '1993', 'Bordeaux', '1997'],
            'doctors/dr-fahed-khalil.html': ['Lebanese University', '2003', 'periodontology', '2006'],
            'doctors/dr-afnan-mashal.html': ['35 years', 'CAD/CAM', 'full-mouth rehabilitation'],
            'doctors/dr-krishnamurthy-katta-balajee.html': ['25 years', 'Pierre Fauchard Academy', 'lingual braces', 'clear aligners'],
            'doctors/dr-dana-awad.html': ['Istanbul Medipol University', 'University of Sharjah', 'Mastery Dental Academy'],
        }
        for rel, terms in expectations.items():
            html = read(rel)
            for term in terms: self.assertIn(term, html, (rel, term))
        for slug in ['dr-ehab-hassouneh', 'dr-sara-ismail', 'dr-nasr-keshkiea', 'dr-kashmira-pawar-jayprakash', 'dr-nachiket-shah', 'dr-lana-masoud']:
            html = read(f'doctors/{slug}.html'); self.assertIn('intentionally limited', html); self.assertNotRegex(html, r'University|Master|Board|Fellow')

    def test_treatment_pages_link_only_to_current_relevant_profiles(self):
        mapping = {
            'treatments/orthodontics.html': ['dr-hani-hasbini', 'dr-moammar-rifai', 'dr-krishnamurthy-katta-balajee'],
            'treatments/dental-implants.html': ['dr-munir-silwadi', 'dr-moheb-silwadi', 'dr-fahed-khalil'],
            'treatments/cosmetic-dentistry.html': ['dr-moheb-silwadi', 'dr-dana-awad', 'dr-afnan-mashal'],
            'treatments/general-dentistry.html': ['dr-afnan-mashal', 'dr-moheb-silwadi', 'dr-ehab-hassouneh', 'dr-sara-ismail', 'dr-nasr-keshkiea', 'dr-dana-awad'],
        }
        for rel, slugs in mapping.items():
            html = read(rel)
            for slug in slugs: self.assertIn(f'../doctors/{slug}.html', html)

    def test_sitemap_contains_all_current_doctor_profiles_once(self):
        root = ET.fromstring(read('sitemap.xml')); ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}; locs = [e.text for e in root.findall('sm:url/sm:loc', ns)]
        for slug in DOCTORS: self.assertEqual(locs.count(f'https://silwadi.ae/doctors/{slug}.html'), 1, slug)
        self.assertEqual(len(locs), 27)

    def test_directory_consultation_uses_contact_page_and_result_label_is_human(self):
        self.assertIn('href="contact.html#consultation"', read('doctors.html')); self.assertIn('dentists & specialists', read('app.js'))

if __name__ == '__main__': unittest.main()
