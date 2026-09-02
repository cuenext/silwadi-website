from pathlib import Path
import json
import re
import shutil
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

PAGE_URLS = {
    'index.html': 'https://silwadi.ae/',
    'doctors.html': 'https://silwadi.ae/doctors.html',
    'treatments.html': 'https://silwadi.ae/treatments.html',
    'about.html': 'https://silwadi.ae/about.html',
    'locations.html': 'https://silwadi.ae/locations.html',
    'contact.html': 'https://silwadi.ae/contact.html',
    'doctors/dr-munir-silwadi.html': 'https://silwadi.ae/doctors/dr-munir-silwadi.html',
    'doctors/dr-moheb-silwadi.html': 'https://silwadi.ae/doctors/dr-moheb-silwadi.html',
    'doctors/dr-hani-hasbini.html': 'https://silwadi.ae/doctors/dr-hani-hasbini.html',
    'doctors/dr-moammar-rifai.html': 'https://silwadi.ae/doctors/dr-moammar-rifai.html',
    'doctors/dr-ahmed-el-shehri.html': 'https://silwadi.ae/doctors/dr-ahmed-el-shehri.html',
    'doctors/dr-fahed-khalil.html': 'https://silwadi.ae/doctors/dr-fahed-khalil.html',
    'doctors/dr-afnan-mashal.html': 'https://silwadi.ae/doctors/dr-afnan-mashal.html',
    'doctors/dr-krishnamurthy-katta-balajee.html': 'https://silwadi.ae/doctors/dr-krishnamurthy-katta-balajee.html',
    'doctors/dr-ehab-hassouneh.html': 'https://silwadi.ae/doctors/dr-ehab-hassouneh.html',
    'doctors/dr-sara-ismail.html': 'https://silwadi.ae/doctors/dr-sara-ismail.html',
    'doctors/dr-nasr-keshkiea.html': 'https://silwadi.ae/doctors/dr-nasr-keshkiea.html',
    'doctors/dr-dana-awad.html': 'https://silwadi.ae/doctors/dr-dana-awad.html',
    'doctors/dr-kashmira-pawar-jayprakash.html': 'https://silwadi.ae/doctors/dr-kashmira-pawar-jayprakash.html',
    'doctors/dr-nachiket-shah.html': 'https://silwadi.ae/doctors/dr-nachiket-shah.html',
    'doctors/dr-lana-masoud.html': 'https://silwadi.ae/doctors/dr-lana-masoud.html',
    'treatments/dental-implants.html': 'https://silwadi.ae/treatments/dental-implants.html',
    'treatments/orthodontics.html': 'https://silwadi.ae/treatments/orthodontics.html',
    'treatments/cosmetic-dentistry.html': 'https://silwadi.ae/treatments/cosmetic-dentistry.html',
    'treatments/general-dentistry.html': 'https://silwadi.ae/treatments/general-dentistry.html',
    'treatments/emergency-dentist.html': 'https://silwadi.ae/treatments/emergency-dentist.html',
    'services.html': 'https://silwadi.ae/services.html',
}


def read(rel):
    return (ROOT / rel).read_text(encoding='utf-8')


def jsonld(rel):
    html = read(rel)
    blocks = re.findall(
        r'<script\s+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html,
        flags=re.I | re.S,
    )
    return [json.loads(block) for block in blocks]


def nodes(rel):
    out = []
    for block in jsonld(rel):
        if isinstance(block, dict) and isinstance(block.get('@graph'), list):
            out.extend(block['@graph'])
        else:
            out.append(block)
    return out


def has_key_deep(value, target):
    if isinstance(value, dict):
        if target in value:
            return True
        return any(has_key_deep(v, target) for v in value.values())
    if isinstance(value, list):
        return any(has_key_deep(v, target) for v in value)
    return False


class PatchEightTechnicalSEOContract(unittest.TestCase):
    def test_site_config_declares_primary_origin_and_stable_ids(self):
        path = ROOT / 'data/site-config.json'
        self.assertTrue(path.is_file(), 'data/site-config.json')
        data = json.loads(path.read_text(encoding='utf-8'))
        self.assertEqual(data['origin'], 'https://silwadi.ae')
        self.assertEqual(data['dentist_id'], 'https://silwadi.ae/#dentist')
        self.assertEqual(data['website_id'], 'https://silwadi.ae/#website')
        self.assertEqual(data['default_social_image'], 'https://silwadi.ae/assets/silwadi-logo-official.png')

    def test_all_pages_have_configured_canonical_and_og_urls(self):
        for rel, expected in PAGE_URLS.items():
            html = read(rel)
            canonicals = re.findall(r'<link\s+rel="canonical"\s+href="([^"]+)"', html, re.I)
            og_urls = re.findall(r'<meta\s+property="og:url"\s+content="([^"]+)"', html, re.I)
            self.assertEqual(canonicals, [expected], rel)
            self.assertEqual(og_urls, [expected], rel)
            self.assertEqual(len(re.findall(r'<title>.*?</title>', html, re.I | re.S)), 1, rel)
            self.assertEqual(len(re.findall(r'<meta\s+name="description"\s+content="[^"]+"', html, re.I)), 1, rel)
            self.assertRegex(html, r'property="og:image" content="https://silwadi\.ae/assets/[^"]+"', rel)
            self.assertNotIn('https://silwadidentalcentres.ae/', html, rel)

    def test_home_has_dentist_and_website_schema_without_review_markup(self):
        home_nodes = nodes('index.html')
        dentist = next((n for n in home_nodes if n.get('@type') == 'Dentist'), None)
        website = next((n for n in home_nodes if n.get('@type') == 'WebSite'), None)
        self.assertIsNotNone(dentist)
        self.assertIsNotNone(website)
        local = json.loads(read('data/local-business.json'))
        self.assertEqual(dentist['@id'], 'https://silwadi.ae/#dentist')
        self.assertEqual(dentist['url'], 'https://silwadi.ae/')
        self.assertEqual(dentist['telephone'], local['phone_e164'])
        self.assertEqual(dentist['email'], local['email'])
        self.assertIn('W Corniche Road', dentist['address']['streetAddress'])
        self.assertEqual(dentist['address']['addressLocality'], 'Abu Dhabi')
        self.assertEqual(dentist['areaServed']['name'], 'Abu Dhabi')
        self.assertEqual(dentist['medicalSpecialty'], 'https://schema.org/Dentistry')
        self.assertGreaterEqual(len(dentist['openingHoursSpecification']), 2)
        self.assertEqual(website['@id'], 'https://silwadi.ae/#website')
        for block in jsonld('index.html'):
            self.assertFalse(has_key_deep(block, 'aggregateRating'))
            self.assertFalse(has_key_deep(block, 'review'))

    def test_contact_and_locations_reference_both_active_branches(self):
        for rel in ['contact.html', 'locations.html']:
            practice_nodes = [n for n in nodes(rel) if n.get('@type') == 'Dentist']
            self.assertEqual(len(practice_nodes), 2, rel)
            self.assertEqual(practice_nodes[0]['@id'], 'https://silwadi.ae/#dentist', rel)
            self.assertEqual(practice_nodes[1]['@id'], 'https://silwadi.ae/#dentist-al-raha', rel)
            self.assertEqual(practice_nodes[1]['telephone'], '+97126662408', rel)
            for node in practice_nodes:
                self.assertFalse(has_key_deep(node, 'aggregateRating'))
                self.assertFalse(has_key_deep(node, 'review'))

    def test_non_home_pages_have_breadcrumb_schema(self):
        for rel in PAGE_URLS:
            if rel == 'index.html':
                continue
            crumbs = [n for n in nodes(rel) if n.get('@type') == 'BreadcrumbList']
            self.assertEqual(len(crumbs), 1, rel)
            items = crumbs[0].get('itemListElement', [])
            expected_count = 3 if '/' in rel else 2
            self.assertEqual(len(items), expected_count, rel)
            self.assertEqual([i['position'] for i in items], list(range(1, expected_count + 1)), rel)
            for item in items:
                self.assertTrue(item['item'].startswith('https://silwadi.ae/'), (rel, item))

    def test_munir_profile_has_person_schema(self):
        person = next((n for n in nodes('doctors/dr-munir-silwadi.html') if n.get('@type') == 'Person'), None)
        self.assertIsNotNone(person)
        self.assertEqual(person['@id'], 'https://silwadi.ae/doctors/dr-munir-silwadi.html#person')
        self.assertEqual(person['name'], 'Dr. Munir Silwadi')
        self.assertEqual(person['jobTitle'], 'Specialist Prosthodontist & Implantologist')
        self.assertEqual(person['url'], 'https://silwadi.ae/doctors/dr-munir-silwadi.html')
        self.assertEqual(person['image'], 'https://silwadi.ae/assets/doctors/dr-munir-silwadi.png')
        self.assertEqual(person['worksFor']['@id'], 'https://silwadi.ae/#dentist')
        self.assertFalse(has_key_deep(person, 'founder'))
        self.assertFalse(has_key_deep(person, 'founderOf'))

    def test_robots_points_to_configured_sitemap(self):
        robots = read('robots.txt')
        self.assertIn('User-agent: *', robots)
        self.assertIn('Allow: /', robots)
        self.assertIn('Sitemap: https://silwadi.ae/sitemap.xml', robots)
        self.assertNotIn('silwadidentalcentres.ae', robots)

    def test_sitemap_contains_exact_current_canonicals(self):
        root = ET.fromstring(read('sitemap.xml'))
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        locs = [el.text for el in root.findall('sm:url/sm:loc', ns)]
        self.assertEqual(locs, list(PAGE_URLS.values()))
        self.assertEqual(len(locs), 27)
        self.assertTrue(all(url.startswith('https://silwadi.ae/') for url in locs))
        self.assertFalse(any('silwadidentalcentres.ae' in url for url in locs))

    def test_domain_switch_helper_updates_site_origin_only(self):
        script = ROOT / 'tools/update_site_domain.py'
        self.assertTrue(script.is_file(), script)
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / 'tools').mkdir()
            (project / 'data').mkdir()
            shutil.copy2(script, project / 'tools/update_site_domain.py')
            shutil.copy2(ROOT / 'data/site-config.json', project / 'data/site-config.json')
            (project / 'index.html').write_text(
                '<link rel="canonical" href="https://silwadi.ae/">'
                '<meta property="og:url" content="https://silwadi.ae/">'
                '<a href="mailto:info@silwadidentalcentres.ae">Email</a>',
                encoding='utf-8',
            )
            (project / 'robots.txt').write_text('Sitemap: https://silwadi.ae/sitemap.xml\n', encoding='utf-8')
            (project / 'sitemap.xml').write_text('<loc>https://silwadi.ae/</loc>\n', encoding='utf-8')
            result = subprocess.run(
                ['python', str(project / 'tools/update_site_domain.py'), 'https://silwadidentalcentres.ae'],
                cwd=project,
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            config = json.loads((project / 'data/site-config.json').read_text(encoding='utf-8'))
            self.assertEqual(config['origin'], 'https://silwadidentalcentres.ae')
            self.assertEqual(config['dentist_id'], 'https://silwadidentalcentres.ae/#dentist')
            self.assertEqual(config['website_id'], 'https://silwadidentalcentres.ae/#website')
            self.assertIn('https://silwadidentalcentres.ae/', (project / 'index.html').read_text(encoding='utf-8'))
            self.assertIn('Sitemap: https://silwadidentalcentres.ae/sitemap.xml', (project / 'robots.txt').read_text(encoding='utf-8'))
            self.assertIn('<loc>https://silwadidentalcentres.ae/</loc>', (project / 'sitemap.xml').read_text(encoding='utf-8'))
            self.assertIn('info@silwadidentalcentres.ae', (project / 'index.html').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
