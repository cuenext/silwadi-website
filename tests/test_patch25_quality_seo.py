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


def public_indexable_pages():
    for page in ROOT.rglob("*.html"):
        if any(part in {"tests", "node_modules", "old-silwadi-site", ".tmp"} for part in page.parts):
            continue
        source = page.read_text(encoding="utf-8")
        robots = re.search(r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']+)', source, re.I)
        if robots and "noindex" in robots.group(1).lower():
            continue
        yield page, source


def local_target(page, target_rel):
    if not target_rel:
        return page.resolve()
    if target_rel.startswith("/"):
        target = (ROOT / target_rel.lstrip("/")).resolve()
    else:
        target = (page.parent / target_rel).resolve()
    if target.is_dir() or target_rel.endswith("/"):
        target = target / "index.html"
    return target


def bilingual_urls(canonical):
    parsed = urlsplit(canonical)
    path = parsed.path or "/"
    if path == "/ar/" or path.startswith("/ar/"):
        ar_url = canonical
        english_path = path[3:] or "/"
        en_url = f"https://silwadi.ae{english_path}"
    else:
        en_url = canonical
        ar_path = "/ar/" if path == "/" else f"/ar{path}"
        ar_url = f"https://silwadi.ae{ar_path}"
    return en_url, ar_url


class Patch25QualitySeo(unittest.TestCase):
    def test_local_html_links_and_fragments_resolve(self):
        failures = []
        for page in ROOT.rglob("*.html"):
            if any(part in {"tests", "node_modules", "old-silwadi-site"} for part in page.parts):
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
                target = local_target(page, target_rel)
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

    def test_about_has_natural_copy_and_restrained_current_story(self):
        source = read("about.html")
        lower = html_lib.unescape(source).replace("\xa0", " ").lower()
        visible = re.sub(r"<[^>]+>", " ", lower)
        visible = re.sub(r"\s+", " ", visible)
        for phrase in (
            "multi-specialty",
            "questions",
            "comfort",
            "prosthodontics",
            "implantology",
            "dr. munir silwadi",
        ):
            self.assertIn(phrase, visible)
        self.assertNotIn("care that feels considered", visible)
        self.assertIn('class="about-hero"', source)
        self.assertIn('class="about-story-timeline"', source)
        self.assertIn("care for every smile in abu dhabi", visible)

    def test_about_images_are_real_dimensioned_assets_with_accessible_alt_text(self):
        source = read("about.html")
        main_match = re.search(r"<main\b.*?</main>", source, re.I | re.S)
        self.assertIsNotNone(main_match)
        main = main_match.group(0)
        images = re.findall(r"<img\b[^>]*>", main, re.I)
        self.assertGreaterEqual(len(images), 1)
        sources = []
        for image in images:
            data = {key.lower(): value for key, value in attrs(image).items()}
            self.assertTrue(data.get("alt", "").strip(), image)
            self.assertRegex(data.get("width", ""), r"^\d+$", image)
            self.assertRegex(data.get("height", ""), r"^\d+$", image)
            sources.append(data.get("src"))
            if 'fetchpriority="high"' not in image:
                self.assertIn('loading="lazy"', image)
        self.assertEqual(len(sources), len(set(sources)))
        self.assertIn("assets/about/silwadi-clinic-original.jpg", sources)

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
        for page, source in public_indexable_pages():
            canonical_match = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)', source, re.I)
            self.assertIsNotNone(canonical_match, page)
            canonical = canonical_match.group(1)
            en_url, ar_url = bilingual_urls(canonical)
            is_arabic = canonical == ar_url
            expected_locale = "ar_AE" if is_arabic else "en_AE"
            expected_alternate_locale = "en_AE" if is_arabic else "ar_AE"
            expected_language = "ar" if is_arabic else "en"
            self.assertEqual([expected_locale], re.findall(r'<meta\s+property=["\']og:locale["\']\s+content=["\']([^"\']+)', source, re.I), page)
            self.assertEqual([expected_alternate_locale], re.findall(r'<meta\s+property=["\']og:locale:alternate["\']\s+content=["\']([^"\']+)', source, re.I), page)
            self.assertEqual([expected_language], re.findall(r'<meta\s+name=["\']content-language["\']\s+content=["\']([^"\']+)', source, re.I), page)
            alternates = {
                attrs(tag).get("hreflang"): attrs(tag).get("href")
                for tag in re.findall(r'<link\b[^>]*\brel=["\']alternate["\'][^>]*>', source, re.I)
            }
            self.assertEqual(en_url, alternates.get("en-AE"), page)
            self.assertEqual(ar_url, alternates.get("ar-AE"), page)
            self.assertEqual(en_url, alternates.get("x-default"), page)


if __name__ == "__main__":
    unittest.main()
