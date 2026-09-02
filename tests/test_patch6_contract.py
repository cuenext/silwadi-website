from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return (ROOT / name).read_text(encoding='utf-8')


class PatchSixHumanCopyAndLocationsContract(unittest.TestCase):
    def test_home_replaces_bland_doctor_stat_with_team_proof(self):
        html = read('index.html')
        self.assertIn('15 dentists &amp; specialists', html)
        self.assertIn('One established clinical team.', html)
        self.assertIn('Meet the team', html)
        self.assertGreaterEqual(html.count('team-proof__avatar'), 4)
        self.assertNotIn('<strong>15 doctors</strong><span>General &amp; specialist care</span>', html)

    def test_public_copy_avoids_banned_ai_filler(self):
        banned = [
            'cutting-edge',
            'state-of-the-art',
            'world-class',
            'best-in-class',
            'personalised solutions tailored to your unique needs',
            'multidisciplinary clinical workflows',
        ]
        pages = [
            'index.html', 'doctors.html', 'about.html',
            'treatments.html', 'treatments/dental-implants.html', 'contact.html'
        ]
        for rel in pages:
            text = read(rel).lower()
            for phrase in banned:
                self.assertNotIn(phrase, text, f'{rel}: {phrase}')

    def test_locations_page_has_two_active_branches(self):
        path = ROOT / 'locations.html'
        self.assertTrue(path.is_file(), 'locations.html')
        html = read('locations.html')
        self.assertEqual(len(re.findall(r'<h1\b', html, re.I)), 1)
        self.assertIn('Bani Yas Tower', html)
        self.assertIn('+971 2 626 2042', html)
        self.assertIn('Sun–Wed 09:00–21:00', html)
        self.assertIn('Al Raha Mall', html)
        self.assertIn('Now open', html)
        self.assertIn('+971 2 666 2408', html)
        self.assertIn('google.com/maps', html)
        self.assertIn('contact.html#consultation', html)

    def test_all_primary_navigation_routes_locations_to_real_page(self):
        root_pages = [
            'index.html', 'doctors.html', 'treatments.html', 'about.html',
            'contact.html', 'locations.html'
        ]
        for rel in root_pages:
            html = read(rel)
            self.assertIn('href="locations.html"', html, rel)

        nested_pages = [
            'doctors/dr-munir-silwadi.html',
            'treatments/dental-implants.html',
        ]
        for rel in nested_pages:
            html = read(rel)
            self.assertIn('href="../locations.html"', html, rel)

    def test_locations_page_keeps_parking_claim_conservative_and_raha_open(self):
        html = read('locations.html').lower()
        self.assertNotIn('free parking', html)
        self.assertNotIn('valet', html)
        self.assertIn('now open', html)
        self.assertIn('+971 2 666 2408', html)


if __name__ == '__main__':
    unittest.main()
