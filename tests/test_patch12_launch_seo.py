from pathlib import Path
import csv
import re
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
LAUNCH_DATE = '2026-08-25'

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
    'doctors/dr-mohammed-abualkas.html': 'https://silwadi.ae/doctors/dr-mohammed-abualkas.html',
    'doctors/dr-reem-alshaer.html': 'https://silwadi.ae/doctors/dr-reem-alshaer.html',
    'doctors/dr-afnan-mashal.html': 'https://silwadi.ae/doctors/dr-afnan-mashal.html',
    'doctors/dr-hawraa-al-ameri.html': 'https://silwadi.ae/doctors/dr-hawraa-al-ameri.html',
    'doctors/dr-ibrahem-abu-shanab.html': 'https://silwadi.ae/doctors/dr-ibrahem-abu-shanab.html',
    'doctors/dr-krishnamurthy-katta-balajee.html': 'https://silwadi.ae/doctors/dr-krishnamurthy-katta-balajee.html',
    'treatments/dental-implants.html': 'https://silwadi.ae/treatments/dental-implants.html',
    'treatments/orthodontics.html': 'https://silwadi.ae/treatments/orthodontics.html',
    'treatments/cosmetic-dentistry.html': 'https://silwadi.ae/treatments/cosmetic-dentistry.html',
    'treatments/general-dentistry.html': 'https://silwadi.ae/treatments/general-dentistry.html',
    'treatments/emergency-dentist.html': 'https://silwadi.ae/treatments/emergency-dentist.html',
}

LEGACY_DOCTORS = {
    'https://silwadidentalcentres.ae/doctors-details/dr-mohamed-munir-juma-mousa.php': 'https://silwadi.ae/doctors/dr-munir-silwadi.html',
    'https://silwadidentalcentres.ae/doctors-details/dr-moheb-silwadi.php': 'https://silwadi.ae/doctors/dr-moheb-silwadi.html',
    'https://silwadidentalcentres.ae/doctors-details/dr-hani-bahijie-hasbini.php': 'https://silwadi.ae/doctors/dr-hani-hasbini.html',
    'https://silwadidentalcentres.ae/doctors-details/dr-moammar-rifai.php': 'https://silwadi.ae/doctors/dr-moammar-rifai.html',
    'https://silwadidentalcentres.ae/doctors-details/dr-ahmed-farouk-ghel.php': 'https://silwadi.ae/doctors/dr-ahmed-el-shehri.html',
    'https://silwadidentalcentres.ae/doctors-details/dr-fahd-elia-abi-khalil.php': 'https://silwadi.ae/doctors/dr-fahed-khalil.html',
    'https://silwadidentalcentres.ae/doctors-details/dr-mohammeda-a-abualkas.php': 'https://silwadi.ae/doctors/dr-mohammed-abualkas.html',
    'https://silwadidentalcentres.ae/doctors-details/dr-reem-h-e-alshaer.php': 'https://silwadi.ae/doctors/dr-reem-alshaer.html',
    'https://silwadidentalcentres.ae/doctors-details/dr-afnan-ibrahim-mohamed-mashal.php': 'https://silwadi.ae/doctors/dr-afnan-mashal.html',
    'https://silwadidentalcentres.ae/doctors-details/Dr-Hawraa-Al-Ameri.php': 'https://silwadi.ae/doctors/dr-hawraa-al-ameri.html',
    'https://silwadidentalcentres.ae/doctors-details/Dr-Ibrahem-Abu-Shanab.php': 'https://silwadi.ae/doctors/dr-ibrahem-abu-shanab.html',
    'https://silwadidentalcentres.ae/doctors-details/Dr-Krishnamurthy-Katta-Balajee.php': 'https://silwadi.ae/doctors/dr-krishnamurthy-katta-balajee.html',
}


def read(rel):
    return (ROOT / rel).read_text(encoding='utf-8')


class PatchTwelveLaunchSEOContract(unittest.TestCase):
    def test_all_indexable_pages_have_launch_head_signals(self):
        for rel in PAGE_URLS:
            html = read(rel)
            self.assertEqual(
                len(re.findall(r'<meta\s+name="robots"\s+content="index,follow,max-image-preview:large"\s*/?>', html, re.I)),
                1,
                rel,
            )
            self.assertEqual(
                len(re.findall(r'<meta\s+property="og:site_name"\s+content="Silwadi Dental Center"\s*/?>', html, re.I)),
                1,
                rel,
            )
            expected_icon = '../favicon.svg' if '/' in rel else 'favicon.svg'
            self.assertEqual(
                len(re.findall(rf'<link\s+rel="icon"\s+href="{re.escape(expected_icon)}"\s+type="image/svg\+xml"\s*/?>', html, re.I)),
                1,
                rel,
            )
            self.assertNotRegex(html, r'<meta\s+name="robots"[^>]*noindex', rel)

    def test_titles_and_descriptions_are_unique_across_indexable_pages(self):
        titles = []
        descriptions = []
        for rel in PAGE_URLS:
            html = read(rel)
            title = re.search(r'<title>(.*?)</title>', html, re.I | re.S)
            desc = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html, re.I)
            self.assertIsNotNone(title, rel)
            self.assertIsNotNone(desc, rel)
            titles.append(re.sub(r'\s+', ' ', title.group(1)).strip())
            descriptions.append(desc.group(1).strip())
        self.assertEqual(len(titles), len(set(titles)))
        self.assertEqual(len(descriptions), len(set(descriptions)))

    def test_sitemap_has_accurate_launch_lastmod_for_every_canonical(self):
        root = ET.fromstring(read('sitemap.xml'))
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = root.findall('sm:url', ns)
        self.assertEqual(len(urls), len(PAGE_URLS))
        pairs = []
        for node in urls:
            loc = node.find('sm:loc', ns)
            lastmod = node.find('sm:lastmod', ns)
            self.assertIsNotNone(loc)
            self.assertIsNotNone(lastmod, loc.text if loc is not None else None)
            self.assertEqual(lastmod.text, LAUNCH_DATE, loc.text)
            pairs.append(loc.text)
        self.assertEqual(pairs, list(PAGE_URLS.values()))

    def test_favicon_is_stable_square_svg(self):
        icon = ROOT / 'favicon.svg'
        self.assertTrue(icon.is_file(), icon)
        root = ET.fromstring(icon.read_text(encoding='utf-8'))
        self.assertTrue(root.tag.endswith('svg'))
        self.assertEqual(root.attrib.get('viewBox'), '0 0 64 64')
        self.assertEqual(root.attrib.get('width'), '64')
        self.assertEqual(root.attrib.get('height'), '64')

    def test_redirect_handoff_covers_live_legacy_pages_with_301s(self):
        path = ROOT / 'docs/launch/legacy-redirect-map.csv'
        self.assertTrue(path.is_file(), path)
        with path.open(encoding='utf-8', newline='') as handle:
            rows = list(csv.DictReader(handle))
        self.assertTrue(rows)
        by_source = {row['source_url']: row for row in rows}
        expected_top = {
            'https://silwadidentalcentres.ae/': 'https://silwadi.ae/',
            'https://silwadidentalcentres.ae/index.php': 'https://silwadi.ae/',
            'https://silwadidentalcentres.ae/?lang=en': 'https://silwadi.ae/',
            'https://silwadidentalcentres.ae/?lang=ar': 'https://silwadi.ae/',
            'https://silwadidentalcentres.ae/about-us.php': 'https://silwadi.ae/about.html',
            'https://silwadidentalcentres.ae/contact-us.php': 'https://silwadi.ae/contact.html',
            'https://silwadidentalcentres.ae/doctors.php': 'https://silwadi.ae/doctors.html',
            'https://silwadidentalcentres.ae/services.php': 'https://silwadi.ae/treatments.html',
            'https://silwadidentalcentres.ae/faq.php': 'https://silwadi.ae/treatments.html',
        }
        expected = {**expected_top, **LEGACY_DOCTORS}
        for source, target in expected.items():
            self.assertIn(source, by_source, source)
            self.assertEqual(by_source[source]['target_url'], target, source)
            self.assertEqual(by_source[source]['status'], '301', source)
        for row in rows:
            self.assertTrue(row['target_url'].startswith('https://silwadi.ae/'), row)
            self.assertEqual(row['status'], '301', row)

    def test_launch_checklist_covers_migration_and_search_engine_handoff(self):
        text = read('docs/launch/SEO-LAUNCH-CHECKLIST.md')
        for phrase in [
            'one-hop 301',
            'Google Search Console',
            'Bing Webmaster Tools',
            'Google Business Profile',
            'Rich Results Test',
            'URL Inspection',
            'robots.txt',
            'sitemap.xml',
            'legacy domain',
            '404',
        ]:
            self.assertIn(phrase, text, phrase)
        self.assertNotIn('sitemaps/ping', text)

    def test_repeatable_launch_audit_command_is_green(self):
        script = ROOT / 'tools/seo_launch_audit.py'
        self.assertTrue(script.is_file(), script)
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('23 pages', result.stdout)
        self.assertIn('0 errors', result.stdout)


if __name__ == '__main__':
    unittest.main()
