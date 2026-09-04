from pathlib import Path
import json
import re
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class Patch3BilingualExperience(unittest.TestCase):
    def run_language(self, search="", saved_language=None, links=None, pathname="/services.html", click=True):
        links = links or []
        storage = json.dumps({"silwadi-language": saved_language} if saved_language else {})
        links_json = json.dumps(links)
        script = rf'''
const fs = require('fs');
const vm = require('vm');
const attrs = {{}};
const meta = {{
  description: {{ content: 'Explore dental services in Abu Dhabi.' }},
  ogTitle: {{ content: 'Dental Services in Abu Dhabi | Silwadi Dental Center' }},
  ogDescription: {{ content: 'Explore dental services at Silwadi Dental Center in Abu Dhabi.' }},
  contentLanguage: {{ content: 'en' }},
}};
const storage = {storage};
const historyCalls = [];
const headerActions = {{ children: [], prepend(node) {{ this.children.unshift(node); }} }};
function makeLink(href) {{
  return {{
    attrs: {{ href }},
    getAttribute(name) {{ return this.attrs[name] ?? null; }},
    setAttribute(name, value) {{ this.attrs[name] = String(value); }},
    hasAttribute(name) {{ return Object.prototype.hasOwnProperty.call(this.attrs, name); }},
    querySelector() {{ return null; }},
    matches(selector) {{ return selector === 'a[href]' || selector === 'a'; }},
  }};
}}
const links = {links_json}.map(makeLink);
const canonical = {{ attrs: {{ href: 'https://silwadi.ae/services.html' }}, getAttribute(n) {{ return this.attrs[n] ?? null; }}, setAttribute(n,v) {{ this.attrs[n] = String(v); }}, hasAttribute(n) {{ return n in this.attrs; }} }};
function metaFor(selector) {{
  if (selector === 'meta[name="description"]') return meta.description;
  if (selector === 'meta[property="og:title"]') return meta.ogTitle;
  if (selector === 'meta[property="og:description"]') return meta.ogDescription;
  if (selector === 'meta[name="content-language"]') return meta.contentLanguage;
  return null;
}}
const doc = {{
  title: 'Dental Services in Abu Dhabi | Silwadi Dental Center',
  documentElement: {{ setAttribute(k,v) {{ attrs[k] = String(v); }} }},
  body: {{ classList: {{ toggle() {{}} }} }},
  head: {{ appendChild(node) {{ (this.children ||= []).push(node); }} }},
  querySelector(selector) {{
    if (selector === '.header-actions') return headerActions;
    if (selector === '[data-language-switch]') return null;
    if (selector === 'link[rel="canonical"]') return canonical;
    return metaFor(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === 'a[href]' || selector === 'a') return links;
    if (selector.includes('meta') || selector.includes('placeholder') || selector.includes('aria-label') || selector.includes('title') || selector.includes('alt')) return [];
    return [];
  }},
  createElement(tag) {{
    return {{ tagName: tag.toUpperCase(), className: '', type: '', textContent: '', attrs: {{}},
      setAttribute(k,v) {{ this.attrs[k] = String(v); }},
      getAttribute(k) {{ return this.attrs[k] ?? null; }},
      addEventListener(type, fn) {{ this.click = fn; }},
    }};
  }},
  dispatchEvent() {{}},
}};
const context = {{
  window: {{}}, document: doc, NodeFilter: {{ SHOW_TEXT: 4 }}, CustomEvent: function(type, init) {{ this.type = type; this.detail = init?.detail; }},
  URL, location: {{ origin: 'https://silwadi.ae', pathname: {json.dumps(pathname)}, search: {json.dumps(search)}, hash: '', href: 'https://silwadi.ae' + {json.dumps(pathname)} + {json.dumps(search)} }},
  history: {{ replaceState(_state, _title, url) {{ historyCalls.push(String(url)); }} }},
  localStorage: {{ getItem(k) {{ return storage[k] || null; }}, setItem(k,v) {{ storage[k] = String(v); }} }},
}};
context.window = context;
vm.runInNewContext(fs.readFileSync('language.js', 'utf8'), context);
context.SilwadiLanguage.init();
const button = headerActions.children[0];
const before = {{ label: button?.textContent, language: context.SilwadiLanguage.getLanguage(), lang: attrs.lang, dir: attrs.dir }};
if ({str(click).lower()} && button?.click) button.click();
const after = {{ label: button?.textContent, language: context.SilwadiLanguage.getLanguage(), lang: attrs.lang, dir: attrs.dir, stored: storage['silwadi-language'] }};
process.stdout.write(JSON.stringify({{
  before, after, links: links.map(link => link.attrs.href), historyCalls,
  title: doc.title, description: meta.description.content, ogTitle: meta.ogTitle.content,
  ogDescription: meta.ogDescription.content, contentLanguage: meta.contentLanguage.content,
  canonical: canonical.attrs.href,
}}));
'''
        result = subprocess.run(
            ["node", "-e", script], cwd=ROOT, text=True, capture_output=True, check=True
        )
        return json.loads(result.stdout)

    def test_url_language_overrides_saved_preference(self):
        state = self.run_language("?lang=ar", "en")
        self.assertEqual(state["before"]["language"], "ar")
        self.assertEqual(state["before"]["lang"], "ar")
        self.assertEqual(state["before"]["dir"], "rtl")

    def test_arabic_internal_links_keep_page_path_and_hash(self):
        state = self.run_language(
            "?lang=ar",
            "ar",
            [
                "treatments.html#pedodontics",
                "../contact.html#consultation-form",
                "mailto:info@example.test",
                "tel:+97126262042",
                "https://example.test/clinic.html",
            ],
            click=False,
        )
        self.assertEqual(
            state["links"],
            [
                "treatments.html?lang=ar#pedodontics",
                "../contact.html?lang=ar#consultation-form",
                "mailto:info@example.test",
                "tel:+97126262042",
                "https://example.test/clinic.html",
            ],
        )

    def test_switching_back_to_english_updates_url_and_removes_query(self):
        state = self.run_language("?lang=ar", "ar", ["about.html"])
        self.assertEqual(state["after"]["language"], "en")
        self.assertEqual(state["after"]["lang"], "en")
        self.assertEqual(state["after"]["dir"], "ltr")
        self.assertEqual(state["after"]["stored"], "en")
        self.assertTrue(state["historyCalls"])
        self.assertEqual(state["historyCalls"][-1], "/services.html")

    def test_arabic_updates_metadata_without_dirtying_canonical(self):
        state = self.run_language("?lang=ar", "en", pathname="/services.html", click=False)
        self.assertNotEqual(state["title"], "Dental Services in Abu Dhabi | Silwadi Dental Center")
        self.assertIn("خدمات", state["title"])
        self.assertIn("أبوظبي", state["description"])
        self.assertIn("أبوظبي", state["ogDescription"])
        self.assertEqual(state["contentLanguage"], "ar")
        self.assertEqual(state["canonical"], "https://silwadi.ae/services.html")

    def test_nested_pages_receive_localized_metadata(self):
        state = self.run_language(
            "?lang=ar",
            "en",
            pathname="/doctors/dr-hani-hasbini.html",
            click=False,
        )
        self.assertIn("هاني حسبيني", state["title"])
        self.assertIn("استشاري تقويم الأسنان", state["title"])
        self.assertIn("هاني حسبيني", state["description"])

    def test_patch2_service_and_treatment_copy_has_natural_arabic_labels(self):
        script = r'''
const api = require('./language.js');
const values = [
  'Start here', 'Start with what you need.', 'For growing smiles',
  'Children’s dental care', 'Restore confidence', 'Replace or repair teeth',
  'Protect your smile', 'Prevention and hygiene', 'A clear place to begin.',
  'Choose a service that matches your next step.', 'Tell us what is bothering you.'
];
process.stdout.write(JSON.stringify(values.map(value => api.translate(value, 'ar'))));
'''
        result = subprocess.run(
            ["node", "-e", script], cwd=ROOT, text=True, capture_output=True, check=True
        )
        translated = json.loads(result.stdout)
        for source, value in zip(
            [
                'Start here', 'Start with what you need.', 'For growing smiles',
                'Children’s dental care', 'Restore confidence', 'Replace or repair teeth',
                'Protect your smile', 'Prevention and hygiene', 'A clear place to begin.',
                'Choose a service that matches your next step.', 'Tell us what is bothering you.'
            ],
            translated,
        ):
            self.assertNotEqual(value, source, source)

    def test_patch2_pages_still_load_language_before_app(self):
        pages = [ROOT / "services.html", ROOT / "treatments.html"]
        for page in pages:
            html = page.read_text(encoding="utf-8")
            self.assertLess(html.index('<script src="language.js"></script>'), html.index('<script src="app.js"></script>'))

    def test_rtl_css_covers_navigation_forms_cards_and_mobile_actions(self):
        css = read("styles.css")
        for selector in (
            'html[dir="rtl"] body.language-ar .header-inner',
            'html[dir="rtl"] body.language-ar .services-start__card',
            'html[dir="rtl"] body.language-ar .consultation-form',
            'html[dir="rtl"] body.language-ar .mobile-actionbar',
        ):
            self.assertIn(selector, css)
        self.assertIn("direction:rtl", css)
        self.assertIn("direction:ltr", css)


if __name__ == "__main__":
    unittest.main()
