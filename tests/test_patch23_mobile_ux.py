from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Patch23MobileUx(unittest.TestCase):
    def read(self, path):
        return (ROOT / path).read_text(encoding="utf-8")

    def test_mobile_navigation_has_its_own_scroll_surface(self):
        css = self.read("styles.css")
        self.assertRegex(css, r"\.mobile-nav\{[^}]*max-height:")
        self.assertRegex(css, r"\.mobile-nav\{[^}]*overflow-y:auto")
        self.assertRegex(css, r"\.mobile-nav__panel\{[^}]*overscroll-behavior:contain")
        self.assertIn("body.menu-open{overflow:hidden}", css)

    def test_shortcuts_are_cards_without_full_height_rules(self):
        css = self.read("styles.css")
        shortcut_rule = re.search(r"\.care-shortcuts a\{[^}]*\}", css)
        self.assertIsNotNone(shortcut_rule)
        rule = shortcut_rule.group(0)
        self.assertNotIn("border-right:1px solid var(--line)", rule)
        self.assertIn("border-radius:", rule)
        self.assertIn("gap:", css)
        self.assertRegex(css, r"\.care-shortcuts a:focus-visible\{")
        self.assertRegex(css, r"\.care-shortcuts__grid\{[^}]*gap:")

    def test_contact_links_get_phone_and_email_icons_sitewide(self):
        js = self.read("app.js")
        self.assertIn("function enhanceContactLinks()", js)
        self.assertIn("a[href^=\"tel:\"]", js)
        self.assertIn("a[href^=\"mailto:\"]", js)
        self.assertIn("classList.add('footer-contact-link')", js)
        self.assertIn("class=\"contact-icon\"", js)
        for path in ("index.html", "contact.html", "locations.html"):
            html = self.read(path)
            self.assertIn('href="tel:+97126262042"', html)
            self.assertIn('href="mailto:info@silwadidentalcentres.ae"', html)

    def test_menu_close_contract_is_preserved(self):
        js = self.read("app.js")
        self.assertIn("function closeMenu()", js)
        self.assertIn("mobileNav.classList.remove('open')", js)
        self.assertIn("document.body.classList.remove('menu-open')", js)
        self.assertIn("menuButton.setAttribute('aria-expanded', 'false')", js)
        self.assertIn("event.key === 'Escape'", js)
        self.assertIn("mobileNav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu))", js)


if __name__ == "__main__":
    unittest.main()
