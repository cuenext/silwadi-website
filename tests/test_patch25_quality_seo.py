from pathlib import Path
from urllib.parse import unquote, urlsplit
import html as html_lib
import re
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def attrs(tag):
    return dict(re.findall(r'([:\w-]+)\s*=\s*["\']([^"\']*)["\']', tag, re.I))


class Patch25QualitySeo(unittest.TestCase):
    def test_local_html_links_and_fragments_resolve(self):
        failures = []
        for page in ROOT.rglob("*.html"):
            if any(part in {"tests", "node_modules"} for part in page.parts):
                continue
            source = page.read_text(encoding="utf-8")
            for raw_href in re.findall(r'<a\b[^>]*\bhref=["\']([^"\']+)', source, re.I):
                href = html_lib.unescape(raw_href)
                if not href or href.startswith(("#", "mailto:", "tel:", "javascript:", "data:", "blob:")):
                    continue
                parsed = urlsplit(href)
                if parsed.scheme or parsed.netloc:
                    continue
                target_rel = unquote(parsed.path)
                target = (page.parent / target_rel).resolve() if target_rel else page.resolve()
                try:
                    target.relative_to(ROOT.resolve())
                except ValueError:
                    failures.append(f"{page.relative_to(ROOT)} -> {href} escapes site root")
                    continue
                if not target.is_file():
                    failures.append(f"{page.relative_to(ROOT)} -> {href} missing file")
                    continue
                if parsed.fragment:
                    target_html = target.read_text(encoding="utf-8")
                    fragment = unquote(parsed.fragment)
                    ids = set(re.findall(r'\bid=["\']([^"\']+)', target_html, re.I))
                    names = set(re.findall(r'\bname=["\']([^"\']+)', target_html, re.I))
                    if fragment not in ids and fragment not in names:
                        failures.append(f"{page.relative_to(ROOT)} -> {href} missing fragment")
        self.assertEqual([], failures)

    def test_about_has_natural_copy_and_a_restrained_photo_story(self):
        source = read("about.html")
        lower = source.lower()
        for phrase in (
            "multi-specialty",
            "questions",
            "comfort",
            "prosthodontics",
            "implantology",
            "dr. munir silwadi",
        ):
            self.assertIn(phrase, lower)
        self.assertNotIn("care that feels considered", lower)
        self.assertIn('class="about-gallery"', source)
        self.assertGreaterEqual(source.count("<figure"), 3)
        self.assertIn('<span class="nowrap-place">Abu Dhabi</span>', source)

    def test_about_images_are_real_dimensioned_assets_with_accessible_alt_text(self):
        source = read("about.html")
        main_match = re.search(r"<main\b.*?</main>", source, re.I | re.S)
        self.assertIsNotNone(main_match)
        main = main_match.group(0)
        images = re.findall(r"<img\b[^>]*>", main, re.I)
        self.assertGreaterEqual(len(images), 7)
        sources = []
        for image in images:
            data = {key.lower(): value for key, value in attrs(image).items()}
            self.assertTrue(data.get("alt", "").strip(), image)
            self.assertRegex(data.get("width", ""), r"^\d+$", image)
            self.assertRegex(data.get("height", ""), r"^\d+$", image)
            sources.append(data.get("src"))
        self.assertEqual(len(sources), len(set(sources)))
        self.assertEqual(source.count("assets/doctors/optimized/dr-munir-silwadi.webp"), 1)
        for image in images:
            if 'fetchpriority="high"' not in image:
                self.assertIn('loading="lazy"', image)

    def test_consultation_form_sets_a_clear_privacy_boundary(self):
        source = read("contact.html")
        form = re.search(r'<form\b[^>]*data-consultation-form.*?</form>', source, re.I | re.S).group(0)
        self.assertIn('aria-describedby="consultation-privacy-note"', form)
        self.assertIn('name="privacy-consent"', form)
        self.assertRegex(form, r'name="privacy-consent"[^>]*required')
        self.assertIn("sensitive medical information", source.lower())
        self.assertIn("email app", source.lower())

    def test_language_seo_adds_uae_open_graph_locale(self):
        source = read("language.js")
        self.assertIn('meta[property="og:locale"]', source)
        self.assertIn('meta[property="og:locale:alternate"]', source)
        self.assertIn("en_AE", source)
        self.assertIn("ar_AE", source)

    def test_language_seo_locale_behavior(self):
        script = r'''
const fs = require('fs');
const vm = require('vm');
const meta = {
  locale: { content: 'en_AE' },
  alternate: { content: 'ar_AE' },
  description: { content: 'Dental care in Abu Dhabi.' },
  ogTitle: { content: 'Silwadi Dental Center' },
  ogDescription: { content: 'Dental care in Abu Dhabi.' },
  contentLanguage: { content: 'en' },
};
const attrs = {};
const doc = {
  title: 'Silwadi Dental Center',
  documentElement: { setAttribute(k, v) { attrs[k] = String(v); } },
  body: { classList: { toggle() {} } },
  querySelector(selector) {
    if (selector === 'meta[property="og:locale"]') return meta.locale;
    if (selector === 'meta[property="og:locale:alternate"]') return meta.alternate;
    if (selector === 'meta[name="description"]') return meta.description;
    if (selector === 'meta[property="og:title"]') return meta.ogTitle;
    if (selector === 'meta[property="og:description"]') return meta.ogDescription;
    if (selector === 'meta[name="content-language"]') return meta.contentLanguage;
    if (selector === 'link[rel="canonical"]') return { getAttribute() { return 'https://silwadi.ae/about.html'; } };
    return null;
  },
  querySelectorAll() { return []; },
  createElement() { return { setAttribute() {}, addEventListener() {} }; },
  head: { appendChild() {} },
};
const context = {
  location: { origin: 'https://silwadi.ae', pathname: '/about.html', search: '?lang=ar', href: 'https://silwadi.ae/about.html?lang=ar' },
  history: { replaceState() {} },
  document: doc,
  localStorage: { getItem() { return null; }, setItem() {} },
  URL,
  NodeFilter: { SHOW_TEXT: 4 },
  CustomEvent: function() {},
};
context.window = context;
vm.runInNewContext(fs.readFileSync('language.js', 'utf8'), context);
context.SilwadiLanguage.init();
process.stdout.write(JSON.stringify({ locale: meta.locale.content, alternate: meta.alternate.content }));
'''
        result = subprocess.run(["node", "-e", script], cwd=ROOT, text=True, capture_output=True, check=True)
        self.assertIn('"locale":"ar_AE"', result.stdout)
        self.assertIn('"alternate":"en_AE"', result.stdout)

    def test_language_seo_treats_hosted_subdirectory_home_as_index(self):
        source = read("language.js")
        self.assertRegex(source, r"const lastSegment = cleanPath \? cleanPath\.split\('/'\)\.pop\(\) : '';")
        self.assertRegex(source, r"return /\\\.html\?\$/i\.test\(lastSegment\) \? lastSegment : 'index\.html';")

    def test_indexable_pages_publish_static_bilingual_share_metadata(self):
        for page in ROOT.rglob("*.html"):
            if any(part in {"tests", "node_modules"} for part in page.parts):
                continue
            source = page.read_text(encoding="utf-8")
            canonical_match = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)', source, re.I)
            self.assertIsNotNone(canonical_match, page)
            canonical = canonical_match.group(1)
            self.assertEqual(["en_AE"], re.findall(r'<meta\s+property=["\']og:locale["\']\s+content=["\']([^"\']+)', source, re.I), page)
            self.assertEqual(["ar_AE"], re.findall(r'<meta\s+property=["\']og:locale:alternate["\']\s+content=["\']([^"\']+)', source, re.I), page)
            self.assertEqual(["en"], re.findall(r'<meta\s+name=["\']content-language["\']\s+content=["\']([^"\']+)', source, re.I), page)
            alternates = {
                attrs(tag).get("hreflang"): attrs(tag).get("href")
                for tag in re.findall(r'<link\b[^>]*\brel=["\']alternate["\'][^>]*>', source, re.I)
            }
            self.assertEqual(canonical, alternates.get("en-AE"), page)
            self.assertEqual(f"{canonical}?lang=ar", alternates.get("ar-AE"), page)
            self.assertEqual(canonical, alternates.get("x-default"), page)


if __name__ == "__main__":
    unittest.main()
