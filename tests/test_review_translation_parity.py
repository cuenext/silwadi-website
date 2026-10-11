from pathlib import Path
import json
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
REVIEWERS = (
    "Mz2006",
    "Ba Zim",
    "Victoriya Davydova",
    "Sanaa Freihat",
    "Sahar Alsalman",
)


def review_summaries(relative_path):
    html = (ROOT / relative_path).read_text(encoding="utf-8")
    articles = re.findall(r'<article class="google-review-card"[^>]*>.*?</article>', html, re.S)
    if len(articles) != 10:
        raise AssertionError(f"{relative_path}: expected five reviews and five marquee copies, got {len(articles)}")
    results = []
    for article in articles:
        reviewer = re.search(r'<strong>([^<]+)</strong>', article)
        summary = re.search(r'<p>(.*?)</p>', article, re.S)
        if not reviewer or not summary:
            raise AssertionError(f"{relative_path}: a review lacks author or summary")
        results.append((reviewer.group(1), re.sub(r"\s+", " ", summary.group(1)).strip()))
    return results


class ReviewTranslationParity(unittest.TestCase):
    def test_all_five_review_summaries_have_matching_static_and_runtime_arabic(self):
        english = review_summaries("index.html")
        arabic = review_summaries("ar/index.html")
        self.assertEqual(tuple(name for name, _ in english[:5]), REVIEWERS)
        self.assertEqual([name for name, _ in arabic], [name for name, _ in english])
        self.assertEqual(english[:5], english[5:])
        self.assertEqual(arabic[:5], arabic[5:])

        source = [excerpt for _, excerpt in english[:5]]
        node_script = (
            "const lang = require('./language.js');"
            "const phrases = JSON.parse(process.argv[1]);"
            "process.stdout.write(JSON.stringify(phrases.map(s => lang.translate(s, 'ar'))));"
        )
        result = subprocess.run(
            ["node", "-e", node_script, json.dumps(source, ensure_ascii=False)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        translated = json.loads(result.stdout)
        self.assertEqual([excerpt for _, excerpt in arabic[:5]], translated)

        for english_text, arabic_text in zip(source, translated):
            self.assertNotEqual(english_text, arabic_text)
            self.assertRegex(arabic_text, r"[\u0600-\u06ff]")
            self.assertNotIn(english_text, (ROOT / "ar/index.html").read_text(encoding="utf-8"))

    def test_review_wording_does_not_assume_gender_for_unknown_reviewers(self):
        html = (ROOT / "ar/index.html").read_text(encoding="utf-8")
        self.assertNotIn("شارك تجربة إيجابية مع التنظيف الاحترافي", html)
        self.assertNotIn("أشاد بالعمل الاحترافي وفريق العمل الودود", html)
        self.assertNotIn("أشاد بعناية الدكتورة دانا وذكر", html)
        self.assertNotIn("شكر الدكتور أحمد الشهري على علاج الجذور العاجل، وأشاد", html)
        self.assertIn("أشادت بتجربة تنظيف الأسنان", html)
        self.assertIn("أشادت بجودة العمل ولطف فريق المركز", html)

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
