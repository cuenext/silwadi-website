from pathlib import Path
import html as html_lib
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

SERVICES = [
    "Prosthodontics & Implantology",
    "Periodontics",
    "Endodontics",
    "Orthodontics",
    "Pedodontics",
    "Cosmetics",
    "Teeth Whitening",
    "Laser Dentistry",
    "Preventive Dentistry",
]


class Patch19WhatsAppServicesNav(unittest.TestCase):
    def read(self, rel):
        return (ROOT / rel).read_text(encoding="utf-8")

    def public_html(self):
        return [p for p in ROOT.rglob("*.html") if "/.git/" not in str(p)]

    def test_header_has_polished_whatsapp_cta_sitewide(self):
        missing = []
        for page in self.public_html():
            html = page.read_text(encoding="utf-8")
            if 'class="site-header"' not in html:
                continue
            if 'class="header-whatsapp"' not in html or 'wa.me/971506260418' not in html:
                missing.append(str(page.relative_to(ROOT)))
        self.assertEqual([], missing)
        css = self.read("styles.css")
        self.assertIn(".header-whatsapp", css)
        self.assertIn("#25d366", css.lower())

    def test_mobile_has_whatsapp_as_persistent_contact_action(self):
        html = self.read("index.html")
        self.assertIn('class="mobile-actionbar__whatsapp"', html)
        self.assertIn('wa.me/971506260418', html)

    def test_services_navigation_shows_actual_services_directly(self):
        missing = []
        for page in self.public_html():
            html = page.read_text(encoding="utf-8")
            nav = re.search(r'<nav class="site-nav".*?</nav>', html, re.S)
            if not nav:
                continue
            nav_html = nav.group(0)
            nav_text = html_lib.unescape(nav_html)
            if 'class="nav-services"' not in nav_html or 'class="services-mega"' not in nav_html:
                missing.append(str(page.relative_to(ROOT)))
                continue
            for service in SERVICES:
                if service not in nav_text:
                    missing.append(f"{page.relative_to(ROOT)}::{service}")
            self.assertNotIn('>Treatment information<', nav_html)
        self.assertEqual([], missing)

    def test_mobile_services_menu_lists_all_services(self):
        html = self.read("index.html")
        match = re.search(r'<details class="mobile-services".*?</details>', html, re.S)
        self.assertIsNotNone(match)
        mobile_text = html_lib.unescape(match.group(0))
        for service in SERVICES:
            self.assertIn(service, mobile_text)

    def test_prosthodontics_and_implantology_are_explained_distinctly(self):
        html = self.read("services.html")
        self.assertIn("Prosthodontics &amp; Implantology", html)
        self.assertRegex(html, r'(?is)Implantology.{0,500}artificial tooth roots')
        self.assertRegex(html, r'(?is)Prosthodontics.{0,500}restor(?:e|ing)|replac(?:e|ing)')
        self.assertIn("implant-supported", html)

    def test_home_uses_correct_combined_service_name(self):
        html = self.read("index.html")
        self.assertIn("Prosthodontics &amp; Implantology", html)
        self.assertNotIn('<h3>Implantology</h3>', html)

    def test_endodontics_uses_explicit_official_silwadi_asset(self):
        html = self.read("services.html")
        self.assertIn('assets/services/endodontics-silwadi.webp', html)
        sources = self.read("docs/launch/PATCH19-IMAGE-SOURCES.md")
        self.assertIn("silwadidentalcentres.ae/assets/img/departments/4.jpg", sources)
        self.assertIn("Endodontics", sources)


if __name__ == "__main__":
    unittest.main()
