from pathlib import Path
import json
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

DOCTORS = {
    'dr-munir-silwadi': ('Dr. Munir Silwadi', 'Specialist Prosthodontist & Implantologist', 'dr-munir-silwadi.png'),
    'dr-moheb-silwadi': ('Dr. Moheb Silwadi', 'General Dentist', 'dr-moheb-silwadi.png'),
    'dr-hani-hasbini': ('Dr. Hani Hasbini', 'Consultant Orthodontics', 'dr-hani-hasbini.png'),
    'dr-moammar-rifai': ('Dr. Moammar Rifai', 'Specialist Orthodontics', 'dr-moammer-rifai.png'),
    'dr-ahmed-el-shehri': ('Dr. Ahmed El Shehri', 'Specialist Endodontics', 'dr-ahmed-el-shehri.png'),
    'dr-fahed-khalil': ('Dr. Fahed Khalil', 'Specialist Periodontics', 'dr-fahed-khalil.png'),
    'dr-mohammed-abualkas': ('Dr. Mohammed Abualkas', 'General Dentist', 'dr-mohammed-abualkas.png'),
    'dr-reem-alshaer': ('Dr. Reem Alshaer', 'General Dentist', 'dr-reem-alshaer.png'),
    'dr-afnan-mashal': ('Dr. Afnan Mashal', 'General Dentist', 'dr-afnan-mashal.png'),
    'dr-hawraa-al-ameri': ("Dr. Hawra'a Al Ameri", 'Specialist Periodontist', 'dr-hawraa-al-ameri.png'),
    'dr-ibrahem-abu-shanab': ('Dr. Ibrahem Abu Shanab', 'General Dentist', 'dr-ibrahem-abu-shanab.png'),
    'dr-krishnamurthy-katta-balajee': ('Dr. Krishnamurthy Katta Balajee', 'Specialist Orthodontist', 'dr-krishnamurthy-katta-balajee.png'),
}

BANNED = [
    'best dentist', 'world-class', 'cutting-edge', 'state-of-the-art',
    'guaranteed', 'pain-free', 'completely painless', 'personal promise',
    'highest quality of care',
]


def read(rel):
    return (ROOT / rel).read_text(encoding='utf-8')


def jsonld_nodes(rel):
    html = read(rel)
    blocks = re.findall(r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>', html, re.I | re.S)
    nodes = []
    for block in blocks:
        parsed = json.loads(block)
        if isinstance(parsed, dict) and isinstance(parsed.get('@graph'), list):
            nodes.extend(parsed['@graph'])
        else:
            nodes.append(parsed)
    return nodes


class PatchTenDoctorAuthority(unittest.TestCase):
    def test_all_twelve_profiles_exist_and_have_core_identity(self):
        for slug, (name, specialty, image) in DOCTORS.items():
            rel = f'doctors/{slug}.html'
            path = ROOT / rel
            self.assertTrue(path.is_file(), rel)
            html = path.read_text(encoding='utf-8')
            h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.I | re.S)
            self.assertEqual(len(h1s), 1, rel)
            self.assertEqual(re.sub(r'<[^>]+>', '', h1s[0]).strip(), name, rel)
            self.assertIn(specialty, html, rel)
            self.assertIn(f'../assets/doctors/{image}', html, rel)
            self.assertIn('Bani Yas Tower, Abu Dhabi', html, rel)
            self.assertIn('../contact.html#consultation', html, rel)
            self.assertIn('../treatments.html', html, rel)
            self.assertLess(len(re.sub(r'<[^>]+>', ' ', html).split()), 650, rel)
            lowered = html.lower()
            for phrase in BANNED:
                self.assertNotIn(phrase, lowered, (rel, phrase))

    def test_every_profile_has_unique_metadata_breadcrumb_and_person_schema(self):
        titles = []
        descriptions = []
        for slug, (name, specialty, image) in DOCTORS.items():
            rel = f'doctors/{slug}.html'
            html = read(rel)
            canonical = f"https://silwadi.ae/{rel}"
            title = re.search(r'<title>(.*?)</title>', html, re.I | re.S)
            desc = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html, re.I)
            self.assertIsNotNone(title, rel)
            self.assertIsNotNone(desc, rel)
            self.assertIn(name.replace('Dr. ', ''), title.group(1), rel)
            self.assertIn('Abu Dhabi', title.group(1), rel)
            self.assertIn(f'<link rel="canonical" href="{canonical}">', html, rel)
            self.assertIn(f'<meta property="og:url" content="{canonical}">', html, rel)
            nodes = jsonld_nodes(rel)
            persons = [n for n in nodes if n.get('@type') == 'Person']
            crumbs = [n for n in nodes if n.get('@type') == 'BreadcrumbList']
            self.assertEqual(len(persons), 1, rel)
            self.assertEqual(len(crumbs), 1, rel)
            person = persons[0]
            self.assertEqual(person['name'], name, rel)
            self.assertEqual(person['jobTitle'], specialty, rel)
            self.assertEqual(person['url'], canonical, rel)
            self.assertEqual(person['image'], f'https://silwadi.ae/assets/doctors/{image}', rel)
            self.assertEqual(person['worksFor']['@id'], 'https://silwadi.ae/#dentist', rel)
            self.assertNotIn('award', json.dumps(person).lower(), rel)
            self.assertEqual(len(crumbs[0]['itemListElement']), 3, rel)
            titles.append(title.group(1).strip())
            descriptions.append(desc.group(1).strip())
        self.assertEqual(len(titles), len(set(titles)))
        self.assertEqual(len(descriptions), len(set(descriptions)))

    def test_directory_links_every_doctor_to_a_profile(self):
        html = read('doctors.html')
        for slug, (name, _, _) in DOCTORS.items():
            self.assertIn(name, html)
            self.assertIn(f'href="doctors/{slug}.html"', html, slug)
        self.assertGreaterEqual(html.count('View profile'), 12)
        self.assertNotIn('data-doctor-results>12 doctors</div>', html)
        self.assertIn('12 dentists &amp; specialists', html)

    def test_verified_high_confidence_profile_facts_are_preserved_without_hype(self):
        expectations = {
            'doctors/dr-moheb-silwadi.html': ['University of Jordan', '2008', 'Digital Smile Design', 'Dental implants'],
            'doctors/dr-hani-hasbini.html': ['Saint Joseph University', '1985', 'Paris VII University', '1989'],
            'doctors/dr-moammar-rifai.html': ['Lebanese University', '1993', 'Bordeaux', '1997'],
            'doctors/dr-fahed-khalil.html': ['Lebanese University', '2003', 'periodontology', '2006'],
            'doctors/dr-mohammed-abualkas.html': ['Ajman University', '2006', 'cosmetic dentistry', 'prosthodontics'],
            'doctors/dr-reem-alshaer.html': ['Ajman University', '2016', 'MFD RCSI', '2017'],
            'doctors/dr-afnan-mashal.html': ['35 years', 'CAD/CAM', 'full-mouth rehabilitation'],
            'doctors/dr-ibrahem-abu-shanab.html': ['2016', 'Fixed Prosthodontics', '2021', 'Syrian Board', '2022'],
            'doctors/dr-krishnamurthy-katta-balajee.html': ['25 years', 'Pierre Fauchard Academy', 'lingual braces', 'clear aligners'],
        }
        for rel, terms in expectations.items():
            html = read(rel)
            for term in terms:
                self.assertIn(term, html, (rel, term))

    def test_low_confidence_profiles_stay_conservative(self):
        hawraa = read('doctors/dr-hawraa-al-ameri.html')
        self.assertIn('Specialist Periodontist', hawraa)
        self.assertIn('periodontal', hawraa.lower())
        self.assertNotRegex(hawraa, r'University|Master|Board|Fellow')

        ahmed = read('doctors/dr-ahmed-el-shehri.html')
        self.assertIn('root canal', ahmed.lower())
        self.assertIn('minimally invasive', ahmed.lower())
        self.assertNotIn('7,000', ahmed)
        self.assertNotIn('7000', ahmed)
        self.assertNotIn('Cairo University', ahmed)
        self.assertNotIn('Ajman University', ahmed)

    def test_treatment_pages_link_to_relevant_verified_profiles(self):
        orthodontics = read('treatments/orthodontics.html')
        for slug in ['dr-hani-hasbini', 'dr-moammar-rifai', 'dr-krishnamurthy-katta-balajee']:
            self.assertIn(f'../doctors/{slug}.html', orthodontics)

        implants = read('treatments/dental-implants.html')
        for slug in ['dr-munir-silwadi', 'dr-moheb-silwadi', 'dr-fahed-khalil']:
            self.assertIn(f'../doctors/{slug}.html', implants)

        cosmetic = read('treatments/cosmetic-dentistry.html')
        for slug in ['dr-moheb-silwadi', 'dr-mohammed-abualkas', 'dr-afnan-mashal']:
            self.assertIn(f'../doctors/{slug}.html', cosmetic)

        general = read('treatments/general-dentistry.html')
        for slug in ['dr-moheb-silwadi', 'dr-mohammed-abualkas', 'dr-reem-alshaer', 'dr-afnan-mashal', 'dr-ibrahem-abu-shanab']:
            self.assertIn(f'../doctors/{slug}.html', general)

    def test_sitemap_contains_all_doctor_profiles_once(self):
        root = ET.fromstring(read('sitemap.xml'))
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        locs = [el.text for el in root.findall('sm:url/sm:loc', ns)]
        for slug in DOCTORS:
            url = f'https://silwadi.ae/doctors/{slug}.html'
            self.assertEqual(locs.count(url), 1, url)
        self.assertEqual(len(locs), 24)

    def test_directory_consultation_uses_contact_page_and_result_label_is_human(self):
        directory = read('doctors.html')
        self.assertIn('href="contact.html#consultation"', directory)
        self.assertNotIn('subject=Doctor%20Consultation%20Request', directory)
        app = read('app.js')
        self.assertIn('dentists & specialists', app)
        self.assertNotIn('doctor${visible === 1 ?', app)


if __name__ == '__main__':
    unittest.main()
