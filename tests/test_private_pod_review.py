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

    def test_sections_follow_clean_patient_journey(self):
        expected = ["hero", "support", "visit", "care", "raha", "faq", "consultation"]
        positions = [self.html.index(f'id="{section}"') for section in expected]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn('id="accessibility"', self.html)

    def test_support_section_is_simple_not_card_heavy(self):
        self.assertIn("How we support your visit", self.html)
        self.assertIn('class="pod-support-list"', self.html)
        self.assertEqual(self.html.count('class="pod-support-point"'), 3)
        self.assertNotIn("pod-access-grid", self.html)
        self.assertNotIn("pod-access-item", self.html)

    def test_hero_has_one_primary_action_and_no_overlay_caption(self):
        hero = re.search(r'<section class="pod-hero" id="hero">(.*?)</section>', self.html, re.S)
        self.assertIsNotNone(hero)
        hero_html = hero.group(1)
        self.assertEqual(hero_html.count("pod-btn--primary"), 1)
        self.assertNotIn("pod-hero__caption", hero_html)

    def test_accessible_room_image_is_not_repeated(self):
        image = "al-raha-accessible-treatment-room-final.webp"
        self.assertEqual(self.html.count(image), 1)

    def test_care_section_is_compact(self):
        self.assertEqual(self.html.count('class="pod-care-item"'), 4)
        self.assertNotIn("pod-care-item svg", self.html)

    def test_branch_facts_and_current_contact_remain(self):
        self.assertIn("+971 2 666 2408", self.html)
        self.assertIn("Saturday–Thursday 10:00 AM–7:00 PM", self.html)
        self.assertIn("Abu&nbsp;Dhabi", self.html)
        self.assertIn("Accessible dental treatment room", self.html)


if __name__ == "__main__":
    unittest.main()
