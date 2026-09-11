from pathlib import Path
import re
import unittest

PAGE = Path("review/people-of-determination-raha-v1.html")


class PrivatePodReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")

    def test_page_stays_private_and_unpublished(self):
        self.assertIn('name="robots" content="noindex,nofollow,noarchive,nosnippet,noimageindex"', self.html)
        self.assertIn("Private review", self.html)
        self.assertIn("Not published", self.html)

    def test_sections_follow_approved_visual_flow(self):
        expected = ["hero", "partnership", "individual-care", "complex-needs", "before-visit", "raha", "consultation"]
        positions = [self.html.index(f'id="{section}"') for section in expected]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn('id="faq"', self.html)

    def test_official_partnership_is_prominent_and_source_linked(self):
        self.assertIn("Zayed Authority for People of Determination", self.html)
        self.assertIn("Official partnership", self.html)
        self.assertIn("Dental-Center-to-Enhance-Comprehensive-Healthcare", self.html)

    def test_partnership_uses_approved_visual_hero_layout(self):
        partnership = re.search(r'<section class="pod-partnership" id="partnership">(.*?)</section>', self.html, re.S)
        self.assertIsNotNone(partnership)
        block = partnership.group(1)
        self.assertIn('class="pod-partnership__layout"', block)
        self.assertIn('class="pod-partnership__visual"', block)
        self.assertIn('https://www.za.gov.ae/-/media/Project/ZHO/ZHO/News-Image/008123.JPG', block)
        self.assertIn('class="pod-partnership__benefits"', block)
        self.assertIn("Greater Access to Specialized Care", block)
        self.assertIn("A More Inclusive Community", block)
        self.assertIn("Healthier Smiles, Brighter Futures", block)
        self.assertIn("Stronger together", block)
        self.assertIn("For a more inclusive tomorrow", block)
        self.assertNotIn('class="pod-partnership__icon"', block)

    def test_care_support_is_icon_led_and_compact(self):
        self.assertEqual(self.html.count('class="pod-care-item"'), 4)
        self.assertEqual(self.html.count('class="pod-care-icon"'), 4)

    def test_hero_uses_accessible_room_once(self):
        hero = re.search(r'<section class="pod-hero" id="hero">(.*?)</section>', self.html, re.S)
        self.assertIsNotNone(hero)
        self.assertEqual(self.html.count("al-raha-accessible-treatment-room-final.webp"), 1)
        self.assertEqual(hero.group(1).count("pod-btn--primary"), 1)

    def test_multiple_real_raha_visuals_are_used(self):
        self.assertIn("al-raha-reception.webp", self.html)
        self.assertIn("al-raha-exterior.webp", self.html)

    def test_before_visit_strip_is_scannable(self):
        for label in ["Mobility", "Communication", "Sensory needs", "Medical support", "Caregiver requirements"]:
            self.assertIn(label, self.html)

    def test_booking_uses_canonical_consultation_anchor(self):
        self.assertIn("../contact.html#consultation-form", self.html)
        self.assertNotIn('href="../contact.html#consultation"', self.html)


if __name__ == "__main__":
    unittest.main()
