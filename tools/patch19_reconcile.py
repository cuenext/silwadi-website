from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

# Keep detailed treatment information discoverable in the footer even though it is
# intentionally removed from the primary navigation.
for page in ROOT.rglob("*.html"):
    text = page.read_text(encoding="utf-8")
    prefix = "../" if page.parent.name in {"doctors", "treatments"} else ""
    services_link = f'<a href="{prefix}services.html">Services</a>'
    treatment_link = f'<a href="{prefix}treatments.html">Treatment information</a>'
    if services_link in text and treatment_link not in text:
        text = text.replace(services_link, services_link + treatment_link, 1)
    page.write_text(text, encoding="utf-8")

# Home still deep-links to the detailed implants page for treatment SEO while the
# visible service language correctly presents Prosthodontics & Implantology together.
home_path = ROOT / "index.html"
home = home_path.read_text(encoding="utf-8")
home = home.replace(
    '<a class="treatment-path reveal" href="services.html#prosthodontics-implantology"><span class="treatment-path__index">01</span>',
    '<a class="treatment-path reveal" href="treatments/dental-implants.html"><span class="treatment-path__index">01</span>',
    1,
)
home_path.write_text(home, encoding="utf-8")

# On urgent-care pages, calling the clinic remains the primary mobile action.
emergency_path = ROOT / "treatments" / "emergency-dentist.html"
emergency = emergency_path.read_text(encoding="utf-8")
bar_match = re.search(r'<div class="mobile-actionbar"[^>]*>.*?</div>', emergency, re.S)
if bar_match:
    bar = bar_match.group(0)
    bar = re.sub(r'<a href="tel:\+97126262042">Call</a>', '<a class="mobile-actionbar__primary" href="tel:+97126262042">Call</a>', bar, count=1)
    bar = re.sub(r'<a class="mobile-actionbar__primary" href="\.\./contact\.html#consultation">Book</a>', '<a href="../contact.html#consultation">Book</a>', bar, count=1)
    emergency = emergency[:bar_match.start()] + bar + emergency[bar_match.end():]
emergency_path.write_text(emergency, encoding="utf-8")

# Make the combined service link explicit for accessibility as well as visible text.
services_path = ROOT / "services.html"
services = services_path.read_text(encoding="utf-8")
needle = '<a class="btn btn--secondary service-card__link" href="treatments.html#prosthodontics">Learn More about Prosthodontics &amp; Implantology</a>'
replacement = '<a class="btn btn--secondary service-card__link" href="treatments.html#prosthodontics" aria-label="Learn more about Prosthodontics & Implantology">Learn More about Prosthodontics &amp; Implantology</a>'
services = services.replace(needle, replacement, 1)
services_path.write_text(services, encoding="utf-8")

# Patch 14's exact treatment catalogue remains authoritative for the detailed
# treatment directory; Home now intentionally combines two related service lines.
p14 = ROOT / "tests" / "test_patch14_official_content_alignment.py"
text = p14.read_text(encoding="utf-8")
if "HOME_SERVICE_NAMES" not in text:
    text = text.replace(
        "}\n\n\ndef read(rel):",
        '}\n\nHOME_SERVICE_NAMES = OFFICIAL_SERVICES | {"Prosthodontics &amp; Implantology"}\n\n\ndef read(rel):',
        1,
    )
text = text.replace(
    "self.assertTrue(titles.issubset(OFFICIAL_SERVICES), titles - OFFICIAL_SERVICES)",
    "self.assertTrue(titles.issubset(HOME_SERVICE_NAMES), titles - HOME_SERVICE_NAMES)",
    1,
)
p14.write_text(text, encoding="utf-8")

# Patch 18 contract now recognizes the combined service and richer Services trigger.
p18 = ROOT / "tests" / "test_patch18_services_about_imagery.py"
text = p18.read_text(encoding="utf-8")
text = text.replace('    "Prosthodontics",\n', '    "Prosthodontics & Implantology",\n', 1)
old_regex = r"<a\\s+href=\"(?:\\.\\./)?services\\.html\"[^>]*>Services</a>"
new_regex = r"<a\\s+(?:class=\"nav-services__trigger\"\\s+)?href=\"(?:\\.\\./)?services\\.html\"[^>]*>Services(?:\\s+<span[^>]*>.*?</span>)?</a>"
text = text.replace(old_regex, new_regex, 1)
p18.write_text(text, encoding="utf-8")
