from pathlib import Path
from PIL import Image
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
DOCTOR_ASSETS = sorted((ROOT / 'assets' / 'doctors').glob('*.png'))
OPT_DIR = ROOT / 'assets' / 'doctors' / 'optimized'


def read(rel):
    return (ROOT / rel).read_text(encoding='utf-8')


class PatchElevenPerformanceMobile(unittest.TestCase):
    def test_all_doctor_portraits_have_smaller_webp_derivatives(self):
        self.assertEqual(len(DOCTOR_ASSETS), 12)
        for original in DOCTOR_ASSETS:
            webp = OPT_DIR / f'{original.stem}.webp'
            self.assertTrue(webp.is_file(), webp)
            self.assertLess(webp.stat().st_size, original.stat().st_size, original.name)
            with Image.open(webp) as im:
                self.assertEqual(im.format, 'WEBP', webp.name)
                self.assertLessEqual(max(im.size), 720, webp.name)

    def test_home_lcp_portrait_is_optimized_eager_and_dimensioned(self):
        html = read('index.html')
        match = re.search(r'<div class="clinical-portrait">\s*<img\s+([^>]+)>', html, re.I)
        self.assertIsNotNone(match)
        attrs = match.group(1)
        self.assertIn('src="assets/doctors/optimized/dr-munir-silwadi.webp"', attrs)
        self.assertIn('fetchpriority="high"', attrs)
        self.assertIn('decoding="async"', attrs)
        self.assertRegex(attrs, r'width="\d+"')
        self.assertRegex(attrs, r'height="\d+"')
        self.assertNotIn('loading="lazy"', attrs)

    def test_home_offscreen_doctor_images_are_lazy_optimized_and_dimensioned(self):
        html = read('index.html')
        portrait_tags = re.findall(r'<img\s+[^>]*src="assets/doctors/optimized/[^"]+\.webp"[^>]*>', html, re.I)
        self.assertGreaterEqual(len(portrait_tags), 10)
        eager = [tag for tag in portrait_tags if 'loading="lazy"' not in tag]
        self.assertEqual(len(eager), 1, eager)
        for tag in portrait_tags:
            self.assertRegex(tag, r'width="\d+"', tag)
            self.assertRegex(tag, r'height="\d+"', tag)
            self.assertIn('decoding="async"', tag)

    def test_directory_and_profiles_use_optimized_portraits(self):
        directory = read('doctors.html')
        self.assertNotRegex(directory, r'<img[^>]+src="assets/doctors/[^/\"]+\.png"')
        self.assertGreaterEqual(directory.count('assets/doctors/optimized/'), 12)
        self.assertGreaterEqual(directory.count('loading="lazy"'), 12)
        for page in sorted((ROOT / 'doctors').glob('*.html')):
            html = page.read_text(encoding='utf-8')
            self.assertIn('../assets/doctors/optimized/', html, page.name)
            self.assertRegex(html, r'<img[^>]+width="\d+"[^>]+height="\d+"', page.name)
            self.assertIn('decoding="async"', html, page.name)

    def test_map_keeps_lazy_loading_and_stable_dimensions(self):
        html = read('locations.html')
        iframe = re.search(r'<iframe\s+([^>]+)>', html, re.I | re.S)
        self.assertIsNotNone(iframe)
        attrs = iframe.group(1)
        self.assertIn('loading="lazy"', attrs)
        self.assertRegex(attrs, r'width="\d+"')
        self.assertRegex(attrs, r'height="\d+"')

    def test_mobile_actionbar_respects_safe_area_and_touch_size(self):
        css = read('styles.css')
        self.assertIn('env(safe-area-inset-bottom)', css)
        self.assertRegex(css, r'body\{padding-bottom:calc\([^}]*safe-area-inset-bottom')
        self.assertRegex(css, r'\.mobile-actionbar a\{[^}]*min-height:48px')

    def test_emergency_mobile_bar_prioritizes_call(self):
        html = read('treatments/emergency-dentist.html')
        bar = re.search(r'<div class="mobile-actionbar"[^>]*>(.*?)</div>', html, re.I | re.S)
        self.assertIsNotNone(bar)
        body = bar.group(1)
        self.assertRegex(body, r'class="mobile-actionbar__primary" href="tel:\+97126262042"')
        self.assertIn('../contact.html#consultation', body)

    def test_javascript_throttles_scroll_and_respects_reduced_motion(self):
        js = read('app.js')
        self.assertIn('requestAnimationFrame', js)
        self.assertIn('prefers-reduced-motion: reduce', js)
        self.assertNotIn('jquery', js.lower())
        self.assertNotIn('lodash', js.lower())
        self.assertNotRegex(js, r'from\s+[\'\"]|require\(')

    def test_reduced_motion_css_remains_present(self):
        css = read('styles.css')
        self.assertIn('@media(prefers-reduced-motion:reduce)', css)
        self.assertIn('transition:none!important', css)
        self.assertIn('.reveal{opacity:1!important;transform:none!important}', css)


if __name__ == '__main__':
    unittest.main()
