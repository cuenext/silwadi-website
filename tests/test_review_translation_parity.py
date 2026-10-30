from pathlib import Path
from html.parser import HTMLParser
import json
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ReviewCards(HTMLParser):
    """Inspect markup emitted by the real renderer, without a DOM dependency."""

    def __init__(self, markup):
        super().__init__()
        self.cards = []
        self.current = None
        self.field = None
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "article":
            self.current = {"attrs": attrs, "name": "", "summary": "", "stars": "", "hint": "", "metadata": ""}
            self.cards.append(self.current)
        if self.current is None:
            return
        if tag == "strong":
            self.field = "name"
        elif tag == "p":
            self.field = "summary"
        elif tag == "span":
            self.field = {"review-stars": "stars", "review-card__hint": "hint"}.get(attrs.get("class"), "metadata")
            if self.field == "stars":
                self.current["starLabel"] = attrs.get("aria-label")

    def handle_endtag(self, tag):
        if tag in ("span", "strong", "p"):
            self.field = None
        if tag == "article":
            self.current = None

    def handle_data(self, value):
        if self.current is not None and self.field:
            self.current[self.field] += value


def render_reviews(language, fixture=None):
    renderer = ROOT / "google-reviews.js"
    if not renderer.exists():
        raise AssertionError("google-reviews.js must render the canonical dataset")
    # The boundary double only captures DOM writes. All card generation and data
    # selection run in the actual production scripts; HTMLParser inspects output.
    script = r"""
const fs = require('node:fs');
const vm = require('node:vm');
const groups = [{innerHTML: ''}, {innerHTML: '', attrs: {'aria-hidden': 'true'},
  setAttribute(k, v) { this.attrs[k] = v; }}];
const properties = {};
const track = {querySelectorAll(selector) {
  if (selector !== '.google-reviews-group') throw Error(selector);
  return groups;
}, style: {setProperty(k, v) { properties[k] = v; }}};
const events = [];
const document = {documentElement: {lang: process.argv[1]},
  querySelector(selector) {
    if (selector !== '.google-reviews-track') throw Error(selector);
    return track;
  }, dispatchEvent(event) { events.push({type: event.type, detail: event.detail}); }};
const context = {window: {}, document, CustomEvent: function(type, options) {
  this.type = type; this.detail = options.detail;
}};
vm.createContext(context);
vm.runInContext(fs.readFileSync('google-reviews-data.js', 'utf8'), context);
const data = context.window.SILWADI_GOOGLE_REVIEWS;
if (process.argv[2] !== 'null') context.window.SILWADI_GOOGLE_REVIEWS = JSON.parse(process.argv[2]);
vm.runInContext(fs.readFileSync('google-reviews.js', 'utf8'), context);
const initial = {groups: groups.map(g => g.innerHTML), events: events.slice()};
const count = context.window.renderSilwadiGoogleReviews(process.argv[1]);
process.stdout.write(JSON.stringify({initial, count, groups: groups.map(g => g.innerHTML), properties, events, data}));
"""
    result = subprocess.run(
        ["node", "-e", script, language, json.dumps(fixture, ensure_ascii=False)],
        cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=True,
    )
    return json.loads(result.stdout)


class ReviewTranslationParity(unittest.TestCase):
    def test_homepages_mount_reviews_before_language_and_app_initialization(self):
        for path in ("index.html", "ar/index.html"):
            with self.subTest(path=path):
                home = (ROOT / path).read_text(encoding="utf-8")
                self.assertRegex(home, r'<div class="google-reviews-group" data-reviews-mount>\s*</div>')
                self.assertRegex(home, r'<div class="google-reviews-group" aria-hidden="true">\s*</div>')
                scripts = re.findall(r'<script\b([^>]*)\bsrc="([^"]+)"([^>]*)>', home)
                filenames = [src.split("?")[0].split("/")[-1] for _, src, _ in scripts]
                self.assertLess(filenames.index("google-reviews-data.js"), filenames.index("google-reviews.js"))
                for dependency in ("language.js", "arabic-static.js", "app.js"):
                    if dependency in filenames:
                        self.assertLess(filenames.index("google-reviews.js"), filenames.index(dependency))
                for before, src, after in scripts:
                    if "google-reviews" in src:
                        self.assertNotRegex(before + after, r'\b(?:async|defer)\b')
                self.assertRegex(home, r'<noscript>[\s\S]*?href="https://maps\.app\.goo\.gl/Ln2vEZmQmgWjb3ETA"[\s\S]*?</noscript>')

    def test_renderer_preserves_all_identities_order_and_localized_content(self):
        for language in ("en", "ar"):
            with self.subTest(language=language):
                result = render_reviews(language)
                interactive, loop = [ReviewCards(markup).cards for markup in result["groups"]]
                self.assertEqual(result["count"], 157)
                self.assertEqual(len(interactive), 157)
                self.assertEqual(len(loop), 157)
                ids = [card["attrs"]["data-review-id"] for card in interactive]
                self.assertEqual(len(set(ids)), 157)
                self.assertEqual(ids, [record["id"] for record in result["data"]])
                self.assertEqual(ids, [card["attrs"]["data-review-id"] for card in loop])
                for card, copy, record in zip(interactive, loop, result["data"]):
                    self.assertEqual(card["name"], record["reviewer"])
                    self.assertEqual(card["summary"], record["summary"][language])
                    self.assertEqual(card["attrs"]["data-review-url"], record["sourceUrl"])
                    self.assertEqual(card["stars"], "★★★★★")
                    self.assertEqual(card["starLabel"], "٥ من ٥ نجوم" if language == "ar" else "5 out of 5 stars")
                    self.assertEqual(card["attrs"].get("role"), "button")
                    self.assertEqual(card["attrs"].get("tabindex"), "0")
                    self.assertEqual(card["attrs"].get("aria-haspopup"), "dialog")
                    self.assertEqual(card["attrs"].get("aria-label"), "فتح تقييم المريض" if language == "ar" else "Open patient review")
                    self.assertIn("data-review-expand", card["attrs"])
                    self.assertEqual(card["hint"], "اضغط للقراءة" if language == "ar" else "Tap to read")
                    branch = {"en": {"corniche": "Corniche", "al-raha": "Al Raha"}, "ar": {"corniche": "الكورنيش", "al-raha": "الراحة"}}[language][record["branch"]]
                    self.assertIn(branch, card["metadata"])
                    self.assertNotIn(record["sourceAge"], card["metadata"])
                    self.assertNotIn("id", card["attrs"])
                    self.assertNotIn("id", copy["attrs"])
                    for attribute in ("data-review-expand", "tabindex", "role", "aria-haspopup", "aria-label"):
                        self.assertNotIn(attribute, copy["attrs"])
                    self.assertEqual({k: v for k, v in card.items() if k != "attrs"}, {k: v for k, v in copy.items() if k != "attrs"})

    def test_renderer_runs_synchronously_is_repeatable_and_reports_count(self):
        result = render_reviews("ar")
        self.assertEqual(result["initial"]["groups"], result["groups"])
        self.assertEqual(result["initial"]["events"], [{"type": "silwadi:reviews-rendered", "detail": {"count": 157, "language": "ar"}}])
        self.assertEqual(result["events"][-1], result["initial"]["events"][0])
        self.assertAlmostEqual(float(result["properties"]["--reviews-duration"].removesuffix("s")), 1444.4)

    def test_renderer_escapes_content_and_keeps_minimum_duration_for_small_sets(self):
        record = {"id": 'id"<1>', "reviewer": '<img src=x onerror="bad()">', "branch": "corniche", "rating": 5, "sourceAge": "a year ago", "sourceUrl": 'https://example.test/?a=1&b="x"', "summary": {"en": "<script>bad()</script> & text", "ar": "نص آمن"}}
        result = render_reviews("en", [record])
        cards = ReviewCards(result["groups"][0]).cards
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0]["name"], record["reviewer"])
        self.assertEqual(cards[0]["summary"], record["summary"]["en"])
        self.assertEqual(cards[0]["attrs"]["data-review-id"], record["id"])
        self.assertEqual(cards[0]["attrs"]["data-review-url"], record["sourceUrl"])
        self.assertNotIn("<script>", result["groups"][0])
        self.assertNotIn("<img", result["groups"][0])
        self.assertEqual(result["properties"]["--reviews-duration"], "46s")

    def test_home_labels_and_review_metadata_are_natural_arabic(self):
        home = (ROOT / "ar/index.html").read_text(encoding="utf-8")
        self.assertEqual(home.count(">تفاصيل الفرع</a>"), 2)
        self.assertIn('<span class="location-status">فرع الكورنيش</span>', home)
        self.assertIn('<span class="location-status">فرع الراحة</span>', home)
        self.assertNotIn('>مفتوح الآن</span>', home)
        self.assertNotIn("تقييمات خمس نجوم لفرع برج بني ياس، روجعت في 6 أكتوبر 2026", home)

    def test_shared_footer_is_localized_on_all_static_arabic_routes(self):
        seo = json.loads((ROOT / "data/arabic-seo.json").read_text(encoding="utf-8"))
        for route in seo:
            relative_path = ROOT / "ar" / route
            html = relative_path.read_text(encoding="utf-8")
            if 'class="footer-opening-hours"' not in html:
                continue
            with self.subTest(route=route):
                self.assertIn("الأحد–الأربعاء: ٩:٠٠ صباحاً", html)
                self.assertIn("الخميس والسبت: ٩:٠٠ صباحاً", html)
                self.assertIn("السبت–الخميس: ١٠:٠٠ صباحاً", html)
                self.assertNotIn(">Bani Yas Tower (Corniche)<", html)
                self.assertNotIn(">Sun–Wed:", html)
                self.assertNotIn(">Thu &amp; Sat:", html)
                self.assertNotIn(">Sat–Thu:", html)
                self.assertNotIn(">Excellence for Every Ability, A Smile for Every Soul.<", html)

    def test_language_switch_keeps_home_marquee_and_uses_static_arabic_on_subpages(self):
        routing = (ROOT / "bilingual-routing.js").read_text(encoding="utf-8")
        self.assertIn("const isHomepage =", routing)
        self.assertIn("window.location.assign(destination.href)", routing)
        self.assertIn("api.applyLanguage(next)", routing)
        self.assertIn("Google Reviews track element and its current animation position", routing)
        builder = (ROOT / "tools/build-arabic-site.mjs").read_text(encoding="utf-8")
        self.assertIn("عرض هذه الصفحة باللغة الإنجليزية", builder)


if __name__ == "__main__":
    unittest.main()
