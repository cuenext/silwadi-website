from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel, text):
    (ROOT / rel).write_text(text, encoding="utf-8")

# Keep the About stylesheet include idempotent after generation runs.
about = read("about.html")
about = re.sub(r'(\s*<link rel="stylesheet" href="services\.css">)+', '\n  <link rel="stylesheet" href="services.css">', about)
write("about.html", about)

# Add a restrained three-image service strip to the approved homepage layout.
home = read("index.html")
if 'class="home-service-visuals' not in home:
    visual_strip = '''<div class="home-service-visuals reveal" aria-label="Featured dental services"><a href="services.html#prosthodontics"><img src="assets/services/prosthodontics.webp" alt="Prosthodontic dental restoration" width="1200" height="900" loading="lazy" decoding="async"><span>Prosthodontics</span></a><a href="services.html#orthodontics"><img src="assets/services/orthodontics.webp" alt="Orthodontic dental treatment" width="1200" height="900" loading="lazy" decoding="async"><span>Orthodontics</span></a><a href="services.html#cosmetics"><img src="assets/services/cosmetics.webp" alt="Cosmetic dental care and smile aesthetics" width="1200" height="900" loading="lazy" decoding="async"><span>Cosmetics</span></a></div>'''
    home = home.replace('<div class="treatment-paths">', visual_strip + '<div class="treatment-paths">', 1)
write("index.html", home)

home_css = read("home-reviews.css")
if ".home-service-visuals{" not in home_css:
    home_css += '''\n.home-service-visuals{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:0 0 28px}.home-service-visuals a{position:relative;display:block;aspect-ratio:16/9;overflow:hidden;border-radius:14px;background:#edf3f4;border:1px solid #dce6e8}.home-service-visuals img{width:100%;height:100%;object-fit:cover;transition:transform .35s ease}.home-service-visuals a:hover img{transform:scale(1.025)}.home-service-visuals span{position:absolute;left:12px;bottom:12px;padding:7px 10px;border-radius:9px;background:rgba(255,255,255,.94);color:#083847;font-size:10px;font-weight:800;box-shadow:0 5px 18px rgba(8,56,71,.08)}\n@media(max-width:620px){.home-service-visuals{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:4px}.home-service-visuals a{flex:0 0 78%;scroll-snap-align:start}}\n@media(prefers-reduced-motion:reduce){.home-service-visuals img{transition:none}}\n'''
write("home-reviews.css", home_css)

# Make every service discovery button visibly descriptive for users and search engines.
services_page = read("services.html")
service_links = {
    "Prosthodontics": "treatments.html#prosthodontics",
    "Periodontics": "treatments.html#periodontics",
    "Endodontics": "treatments.html#endodontics",
    "Orthodontics": "treatments/orthodontics.html",
    "Pedodontics": "treatments.html#pedodontics",
    "Cosmetics": "treatments/cosmetic-dentistry.html",
    "Teeth Whitening": "treatments/teeth-whitening.html",
    "Laser Dentistry": "treatments.html#laser-dentistry",
    "Preventive Dentistry": "treatments/general-dentistry.html",
}
for service, href in service_links.items():
    pattern = re.compile(
        rf'<a class="btn btn--secondary service-card__link" href="{re.escape(href)}"(?: aria-label="[^"]+")?>Learn More(?: about [^<]+)?</a>'
    )
    replacement = (
        f'<a class="btn btn--secondary service-card__link" href="{href}" '
        f'aria-label="Learn more about {service}">Learn More about {service}</a>'
    )
    services_page = pattern.sub(replacement, services_page)
write("services.html", services_page)

# User-confirmed current Bani Yas address: remove the obsolete landmark from the data source.
local_path = ROOT / "data/local-business.json"
local = json.loads(local_path.read_text(encoding="utf-8"))
local["address"] = "Bani Yas Tower, Building 117 C Floor, Sultan Bin Zayed The First St, W Corniche Road, Abu Dhabi, UAE"
local_path.write_text(json.dumps(local, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

# Patch 18 adds one canonical Services page.
audit = read("tools/seo_launch_audit.py").replace("if len(locs) != 23:", "if len(locs) != 24:").replace("expected 23 canonical URLs", "expected 24 canonical URLs")
write("tools/seo_launch_audit.py", audit)

for rel in ["tests/test_patch8_technical_seo.py", "tests/test_patch12_launch_seo.py"]:
    text = read(rel)
    if "'services.html': 'https://silwadi.ae/services.html'" not in text:
        needle = "    'treatments/emergency-dentist.html': 'https://silwadi.ae/treatments/emergency-dentist.html',\n"
        text = text.replace(needle, needle + "    'services.html': 'https://silwadi.ae/services.html',\n")
    text = text.replace("len(locs), 23", "len(locs), 24")
    text = text.replace("'23 pages'", "'24 pages'")
    write(rel, text)

for rel in ["tests/test_patch9_treatment_seo.py", "tests/test_patch10_doctor_authority.py"]:
    text = read(rel).replace("len(locs),23", "len(locs),24").replace("len(locs), 23", "len(locs), 24")
    write(rel, text)

# The homepage still keeps the approved compact treatment list, but its discovery CTA now routes to Services.
for rel in ["tests/test_patch15_homepage_redesign.py", "tests/test_patch16_truth_reviews_raha.py"]:
    text = read(rel).replace("View all 10 services", "View all services")
    write(rel, text)

# Review-card content has been refreshed; preserve stable listing/rating checks rather than a stale review-count snapshot.
p16 = read("tests/test_patch16_truth_reviews_raha.py")
p16 = p16.replace("        self.assertIn('199', self.home)\n", "")
p16 = p16.replace('(\"Ahmed H\", \"Emily Campbell Scully\", \"Sanaa Freihat\", \"Antoni Y\")', '(\"Ahmed H\", \"Emily Campbell Scully\", \"Victoriya Davydova\", \"Sanaa Freihat\", \"Sahar Alsalman\")')
write("tests/test_patch16_truth_reviews_raha.py", p16)

p17 = read("tests/test_patch17_home_rollback_reviews.py")
p17 = p17.replace('        self.assertIn("199 Google reviews", self.home)\n', '        self.assertIn("Google reviews", self.home)\n        self.assertIn("review-stars", self.home)\n')
write("tests/test_patch17_home_rollback_reviews.py", p17)

# The legacy official services URL should now hand off to the new Services landing page.
redirect = read("docs/launch/legacy-redirect-map.csv").replace(
    "https://silwadidentalcentres.ae/services.php,https://silwadi.ae/treatments.html,301",
    "https://silwadidentalcentres.ae/services.php,https://silwadi.ae/services.html,301",
)
write("docs/launch/legacy-redirect-map.csv", redirect)

p12 = read("tests/test_patch12_launch_seo.py").replace(
    "'https://silwadidentalcentres.ae/services.php': 'https://silwadi.ae/treatments.html'",
    "'https://silwadidentalcentres.ae/services.php': 'https://silwadi.ae/services.html'",
)
write("tests/test_patch12_launch_seo.py", p12)

# Keep footer discovery aligned with Services while retaining the detailed treatment directory.
for page in ROOT.rglob("*.html"):
    text = page.read_text(encoding="utf-8")
    prefix = "../" if page.parent.name in {"doctors", "treatments"} else ""
    text = text.replace(f'<div><h3>Care</h3><a href="{prefix}treatments.html">Treatments</a>', f'<div><h3>Care</h3><a href="{prefix}services.html">Services</a>')
    services_link = f'<a href="{prefix}services.html">Services</a>'
    treatment_link = f'<a href="{prefix}treatments.html">Treatment information</a>'
    if services_link in text and treatment_link not in text:
        text = text.replace(services_link, services_link + treatment_link, 1)
    page.write_text(text, encoding="utf-8")
