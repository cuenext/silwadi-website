from pathlib import Path
import json
import re
import html as html_lib
import unittest

ROOT = Path(__file__).resolve().parents[1]

ROOT_PAGES = [
    'index.html', 'doctors.html', 'treatments.html', 'about.html',
    'locations.html', 'contact.html'
]
NESTED_PAGES = [
    'doctors/dr-munir-silwadi.html',
    'treatments/dental-implants.html',
]


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')


class PatchSevenLocalSEOContract(unittest.TestCase):
    def local_data(self):
        return json.loads(read('data/local-business.json'))

    def test_local_business_source_of_truth_exists(self):
        path = ROOT / 'data/local-business.json'
        self.assertTrue(path.is_file(), 'data/local-business.json')
        data = self.local_data()
        self.assertEqual(data['brand_name'], 'Dr. Munir Silwadi Dental Centre')
        self.assertEqual(data['branch_label'], 'Bani Yas Tower')
        self.assertEqual(data['phone_e164'], '+97126262042')
        self.assertEqual(data['service_area'], 'Abu Dhabi')
        self.assertTrue(data['al_raha']['is_open'])
        self.assertEqual(data['al_raha']['phone_e164'], '+97126662408')

    def test_contact_and_locations_use_identical_nap(self):
        data = self.local_data()
        for rel in ['contact.html', 'locations.html']:
            html = read(rel)
            self.assertIn(data['brand_name'], html, rel)
            self.assertIn(data['phone_display'], html, rel)
            self.assertIn(data['email'], html, rel)
            self.assertIn(data['address'], html, rel)
            self.assertIn(f'tel:{data["phone_e164"]}', html, rel)

    def test_verified_hours_are_consistent(self):
        expected = self.local_data()['hours_display']
        for rel in ['contact.html', 'locations.html']:
            self.assertIn(expected, html_lib.unescape(read(rel)), rel)

    def test_sitewide_footer_contains_active_location_signals(self):
        for rel in ROOT_PAGES + NESTED_PAGES:
            html = read(rel)
            self.assertIn('+971 2 626 2042', html, rel)
            self.assertIn('Bani Yas Tower', html, rel)
            self.assertIn('W Corniche Road, Abu Dhabi', html, rel)

    def test_locations_and_contact_have_google_map_paths(self):
        for rel in ['locations.html', 'contact.html']:
            html = read(rel)
            self.assertRegex(html, r'google\.com/maps', rel)
            self.assertIn('Bani Yas Tower', html, rel)

    def test_local_metadata_is_natural_and_location_specific(self):
        pages = ROOT_PAGES + NESTED_PAGES
        for rel in pages:
            html = read(rel)
            title = re.search(r'<title>(.*?)</title>', html, re.I | re.S)
            description = re.search(r'<meta name="description" content="([^"]+)"', html, re.I)
            self.assertIsNotNone(title, rel)
            self.assertIsNotNone(description, rel)
            self.assertIn('Abu Dhabi', title.group(1), rel)
            self.assertIn('Abu Dhabi', description.group(1), rel)
            self.assertNotIn('dentist abu dhabi dentist abu dhabi', html.lower(), rel)

    def test_al_raha_is_operational(self):
        html = read('locations.html').lower()
        self.assertIn('id="al-raha"', html)
        self.assertIn('+971 2 666 2408', html)
        self.assertIn('contact.html#consultation', html)
        self.assertNotIn('coming soon', html)
        self.assertNotIn('not yet open', html)
        self.assertNotIn('class="location-state"', html)

    def test_unverified_corniche_branch_name_is_not_used_as_nap(self):
        for rel in ROOT_PAGES + NESTED_PAGES:
            self.assertNotIn('Dr Munir Silwadi Dental Centre - Corniche Branch', read(rel), rel)


if __name__ == '__main__':
    unittest.main()
