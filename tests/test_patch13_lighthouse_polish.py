from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding='utf-8')


def rel_luminance(hex_color):
    value = hex_color.lstrip('#')
    channels = [int(value[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(foreground, background):
    a, b = rel_luminance(foreground), rel_luminance(background)
    lighter, darker = max(a, b), min(a, b)
    return (lighter + 0.05) / (darker + 0.05)


def rule(css, selector):
    match = re.search(re.escape(selector) + r'\{([^}]*)\}', css)
    if not match:
        raise AssertionError(f'Missing CSS rule: {selector}')
    return match.group(1)


def color_from_rule(css, selector):
    body = rule(css, selector)
    match = re.search(r'(?:^|;)\s*color\s*:\s*(#[0-9a-fA-F]{6})', body)
    if not match:
        raise AssertionError(f'Missing hex color in: {selector}')
    return match.group(1)


class PatchThirteenLighthousePolish(unittest.TestCase):
    def test_html_never_renders_original_doctor_pngs(self):
        for page in ROOT.rglob('*.html'):
            html = page.read_text(encoding='utf-8')
            self.assertNotRegex(
                html,
                r'<img[^>]+src="(?:\.\./)?assets/doctors/[^/\"]+\.png"',
                page.relative_to(ROOT),
            )

    def test_implant_provider_uses_lazy_optimized_dimensioned_portrait(self):
        html = read('treatments/dental-implants.html')
        match = re.search(r'<div class="provider-card"><img\s+([^>]+)>', html, re.I)
        self.assertIsNotNone(match)
        attrs = match.group(1)
        self.assertIn('src="../assets/doctors/optimized/dr-munir-silwadi.webp"', attrs)
        self.assertIn('loading="lazy"', attrs)
        self.assertIn('decoding="async"', attrs)
        self.assertIn('width="720"', attrs)
        self.assertIn('height="720"', attrs)

    def test_light_surface_neutral_text_meets_wcag_aa(self):
        css = read('styles.css')
        muted = re.search(r'--muted\s*:\s*(#[0-9a-fA-F]{6})', css).group(1)
        self.assertGreaterEqual(contrast(muted, '#f7fafb'), 4.5)
        self.assertGreaterEqual(contrast(muted, '#f8fafb'), 4.5)
        checks = [
            ('.legacy-seal span', '#ffffff'),
            ('.care-shortcuts span', '#ffffff'),
            ('.care-shortcuts em', '#ffffff'),
            ('.footer-grid a,.footer-grid span', '#f8fafb'),
            ('.footer-bottom', '#f8fafb'),
        ]
        for selector, background in checks:
            self.assertGreaterEqual(
                contrast(color_from_rule(css, selector), background),
                4.5,
                selector,
            )

    def test_footer_links_meet_minimum_target_size(self):
        css = read('styles.css')
        body = rule(css, '.footer-grid a')
        self.assertRegex(body, r'min-height\s*:\s*24px')
        self.assertRegex(body, r'display\s*:\s*inline-flex')


if __name__ == '__main__':
    unittest.main()
