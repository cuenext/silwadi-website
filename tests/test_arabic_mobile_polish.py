from pathlib import Path
import json
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ArabicMobilePolishContract(unittest.TestCase):
    def test_prominent_arabic_heading_uses_one_natural_phrase(self):
        overrides = json.loads((ROOT / "data" / "arabic-quality-overrides-critical.json").read_text(encoding="utf-8"))
        self.assertEqual(
            overrides.get("Specialist expertise. Personal care."),
            "خبرة تخصصية ورعاية باهتمام",
        )

    def test_mobile_arabic_facts_stack_instead_of_squeezing_two_columns(self):
        css = (ROOT / "arabic-quality.css").read_text(encoding="utf-8")
        self.assertIn("html[dir=\"rtl\"] .legacy-facts>div,.static-arabic .legacy-facts>div{grid-template-columns:1fr!important", css)
        self.assertIn("html[dir=\"rtl\"] h1,.static-arabic h1{line-height:1.16!important", css)
        self.assertIn("html[dir=\"rtl\"] h2,.static-arabic h2{line-height:1.22!important", css)

    def test_mobile_reviews_are_swipeable_and_the_track_stays_ltr(self):
        css = (ROOT / "home-reviews.css").read_text(encoding="utf-8")
        self.assertIn(".google-reviews-viewport{overflow-x:auto;scroll-snap-type:x mandatory", css)
        self.assertIn(".google-reviews-track{animation:none!important;transform:none!important;direction:ltr", css)
        self.assertIn(".google-review-card{scroll-snap-align:start", css)


if __name__ == "__main__":
    unittest.main()
