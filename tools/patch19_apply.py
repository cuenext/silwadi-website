from pathlib import Path
import re
import ssl
import urllib.request
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
WHATSAPP_NUMBER = "971506260418"
WHATSAPP_URL = (
    "https://wa.me/971506260418?text="
    "Hello%20Silwadi%20Dental%20Center%2C%20I%27d%20like%20to%20book%20an%20appointment."
)

SERVICES = [
    ("Prosthodontics &amp; Implantology", "prosthodontics-implantology", "Restore &amp; replace teeth"),
    ("Periodontics", "periodontics", "Gum &amp; supporting tissue care"),
    ("Endodontics", "endodontics", "Root canal &amp; pulp care"),
    ("Orthodontics", "orthodontics", "Alignment &amp; bite correction"),
    ("Pedodontics", "pedodontics", "Dental care for children"),
    ("Cosmetics", "cosmetics", "Smile aesthetics"),
    ("Teeth Whitening", "teeth-whitening", "Professional whitening"),
    ("Laser Dentistry", "laser-dentistry", "Laser-assisted procedures"),
    ("Preventive Dentistry", "preventive-dentistry", "Routine &amp; preventive care"),
]

WA_ICON = '''<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M12.04 2a9.84 9.84 0 0 0-8.43 14.91L2 22l5.22-1.56A9.9 9.9 0 1 0 12.04 2Zm0 17.98a8.03 8.03 0 0 1-4.09-1.12l-.29-.17-3.1.93.94-3.02-.19-.31A8.04 8.04 0 1 1 12.04 19.98Zm4.4-6.03c-.24-.12-1.43-.7-1.65-.78-.22-.08-.38-.12-.54.12-.16.24-.62.78-.76.94-.14.16-.28.18-.52.06-.24-.12-1.01-.37-1.93-1.19-.71-.64-1.2-1.42-1.34-1.66-.14-.24-.02-.37.1-.49.11-.11.24-.28.36-.42.12-.14.16-.24.24-.4.08-.16.04-.3-.02-.42-.06-.12-.54-1.3-.74-1.78-.19-.47-.39-.4-.54-.41h-.46c-.16 0-.42.06-.64.3-.22.24-.84.82-.84 2s.86 2.32.98 2.48c.12.16 1.7 2.59 4.11 3.63.57.25 1.02.4 1.37.51.58.18 1.1.16 1.51.1.46-.07 1.43-.58 1.63-1.15.2-.57.2-1.06.14-1.16-.06-.1-.22-.16-.46-.28Z"/></svg>'''


def prefix_for(path: Path) -> str:
    return "../" if path.parent.name in {"doctors", "treatments"} else ""


def section_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "services.html" or rel.startswith("treatments/") or rel == "treatments.html":
        return "services"
    if rel == "doctors.html" or rel.startswith("doctors/"):
        return "doctors"
    if rel == "about.html":
        return "about"
    if rel == "locations.html":
        return "locations"
    return ""


def current(section: str, wanted: str) -> str:
    return ' aria-current="page"' if section == wanted else ""


def service_links(prefix: str, mobile: bool = False) -> str:
    items = []
    for label, anchor, note in SERVICES:
        href = f"{prefix}services.html#{anchor}"
        if mobile:
            items.append(f'<a href="{href}"><strong>{label}</strong><span>{note}</span></a>')
        else:
            items.append(f'<a href="{href}"><strong>{label}</strong><small>{note}</small><b aria-hidden="true">→</b></a>')
    return "".join(items)


def desktop_nav(prefix: str, section: str) -> str:
    services_current = current(section, "services")
    return (
        '<nav class="site-nav" aria-label="Primary navigation">'
        '<div class="nav-services">'
        f'<a class="nav-services__trigger" href="{prefix}services.html"{services_current}>Services '
        '<span class="nav-services__chevron" aria-hidden="true">⌄</span></a>'
        '<div class="services-mega" aria-label="Dental services">'
        '<div class="services-mega__head"><div><span>Dental services</span><strong>Choose the care you need</strong></div>'
        f'<a href="{prefix}services.html">View all services <span aria-hidden="true">→</span></a></div>'
        f'<div class="services-mega__grid">{service_links(prefix)}</div>'
        '</div></div>'
        f'<a href="{prefix}doctors.html"{current(section, "doctors")}>Doctors</a>'
        f'<a href="{prefix}about.html"{current(section, "about")}>About</a>'
        f'<a href="{prefix}locations.html"{current(section, "locations")}>Locations</a>'
        '</nav>'
    )


def mobile_nav(prefix: str, section: str) -> str:
    return (
        '<div class="mobile-nav" id="mobileNav" data-mobile-nav><nav class="mobile-nav__panel" aria-label="Mobile navigation">'
        f'<a href="{prefix}index.html">Home</a>'
        f'<details class="mobile-services"{" open" if section == "services" else ""}><summary>Services</summary>'
        f'<div class="mobile-services__links">{service_links(prefix, mobile=True)}</div></details>'
        f'<a href="{prefix}doctors.html"{current(section, "doctors")}>Doctors</a>'
        f'<a href="{prefix}about.html"{current(section, "about")}>About</a>'
        f'<a href="{prefix}locations.html"{current(section, "locations")}>Locations</a>'
        f'<a class="mobile-nav-whatsapp" href="{WHATSAPP_URL}" target="_blank" rel="noopener">{WA_ICON}<span>Chat on WhatsApp</span></a>'
        f'<a class="btn btn--primary" href="{prefix}contact.html#consultation">Book a Consultation</a>'
        '</nav></div>'
    )


def header_actions(prefix: str) -> str:
    return (
        '<div class="header-actions">'
        f'<a class="header-whatsapp" href="{WHATSAPP_URL}" target="_blank" rel="noopener" aria-label="Chat with Silwadi Dental Center on WhatsApp">'
        f'{WA_ICON}<span>WhatsApp</span></a>'
        f'<a class="btn btn--primary header-consult" href="{prefix}contact.html#consultation">Book a Consultation</a>'
        '<button class="menu-button" type="button" data-menu-button aria-expanded="false" aria-controls="mobileNav" aria-label="Open navigation"><span></span><span></span></button>'
        '</div>'
    )


def mobile_actionbar(prefix: str) -> str:
    return (
        '<div class="mobile-actionbar">'
        f'<a class="mobile-actionbar__whatsapp" href="{WHATSAPP_URL}" target="_blank" rel="noopener" aria-label="WhatsApp Silwadi Dental Center">{WA_ICON}<span>WhatsApp</span></a>'
        '<a href="tel:+97126262042">Call</a>'
        f'<a class="mobile-actionbar__primary" href="{prefix}contact.html#consultation">Book</a>'
        '</div>'
    )


for page in ROOT.rglob("*.html"):
    text = page.read_text(encoding="utf-8")
    if 'class="site-header"' not in text:
        continue
    prefix = prefix_for(page)
    section = section_for(page)
    text = re.sub(r'<nav class="site-nav".*?</nav>', desktop_nav(prefix, section), text, count=1, flags=re.S)
    text = re.sub(r'<div class="header-actions">.*?</div>', header_actions(prefix), text, count=1, flags=re.S)
    text = re.sub(r'<div class="mobile-nav"[^>]*>.*?</nav></div>', mobile_nav(prefix, section), text, count=1, flags=re.S)
    text = re.sub(r'<div class="mobile-actionbar">.*?</div>', mobile_actionbar(prefix), text, count=1, flags=re.S)
    page.write_text(text, encoding="utf-8")

# Correct the combined prosthodontics / implantology service and its meaning.
services_path = ROOT / "services.html"
services = services_path.read_text(encoding="utf-8")
services = services.replace("prosthodontics, periodontics", "prosthodontics and implantology, periodontics")
services = services.replace('"name":"Prosthodontics"', '"name":"Prosthodontics & Implantology"', 1)
services = services.replace('services.html#prosthodontics"', 'services.html#prosthodontics-implantology"', 1)
first_card = '''<article class="service-card reveal" id="prosthodontics-implantology"><div class="service-card__image"><img src="assets/services/prosthodontics.webp" alt="Prosthodontics and implantology care at Silwadi Dental Center Abu Dhabi" width="1200" height="900" loading="lazy" decoding="async"></div><div class="service-card__body"><h2>Prosthodontics &amp; Implantology</h2><p><strong>Implantology</strong> focuses on planning and surgically placing dental implants—artificial tooth roots that support replacement teeth. <strong>Prosthodontics</strong> focuses on restoring or replacing teeth with crowns, bridges, veneers, dentures and implant-supported restorations, including full-mouth rehabilitation.</p><a class="btn btn--secondary service-card__link" href="treatments.html#prosthodontics">Learn More about Prosthodontics &amp; Implantology</a></div></article>'''
services = re.sub(r'<article class="service-card reveal" id="prosthodontics">.*?</article>', first_card, services, count=1, flags=re.S)
services = services.replace('assets/services/endodontics.webp', 'assets/services/endodontics-silwadi.webp')
services = services.replace('<article class="service-card reveal" id="endodontics"><div class="service-card__image">', '<article class="service-card reveal" id="endodontics"><div class="service-card__image service-card__image--official">', 1)
services_path.write_text(services, encoding="utf-8")

# Make the approved homepage service path clinically clear without redesigning the page.
home_path = ROOT / "index.html"
home = home_path.read_text(encoding="utf-8")
home = home.replace('href="services.html#prosthodontics"', 'href="services.html#prosthodontics-implantology"')
home = home.replace('<span>Prosthodontics</span>', '<span>Prosthodontics &amp; Implantology</span>', 1)
home = re.sub(
    r'<a class="treatment-path reveal" href="treatments/dental-implants\.html"><span class="treatment-path__index">01</span><div><h3>Implantology</h3><p>.*?</p></div><b aria-hidden="true">→</b></a>',
    '<a class="treatment-path reveal" href="services.html#prosthodontics-implantology"><span class="treatment-path__index">01</span><div><h3>Prosthodontics &amp; Implantology</h3><p>Implants replace missing tooth roots; prosthodontic restorations rebuild the visible teeth and bite with crowns, bridges, dentures and implant-supported solutions.</p></div><b aria-hidden="true">→</b></a>',
    home,
    count=1,
    flags=re.S,
)
home_path.write_text(home, encoding="utf-8")

# Re-import the exact Endodontics department image used by Silwadi's official website.
source_url = "https://silwadidentalcentres.ae/assets/img/departments/4.jpg"
request = urllib.request.Request(source_url, headers={"User-Agent": "Mozilla/5.0"})
context = ssl._create_unverified_context()
asset_dir = ROOT / "assets" / "services"
asset_dir.mkdir(parents=True, exist_ok=True)
tmp = asset_dir / ".endodontics-silwadi-source.jpg"
with urllib.request.urlopen(request, context=context, timeout=30) as response:
    tmp.write_bytes(response.read())
with Image.open(tmp) as image:
    image = ImageOps.exif_transpose(image).convert("RGB")
    if image.width > 1600:
        image.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
    image.save(asset_dir / "endodontics-silwadi.webp", "WEBP", quality=88, method=6)
tmp.unlink(missing_ok=True)

source_doc = ROOT / "docs" / "launch" / "PATCH19-IMAGE-SOURCES.md"
source_doc.write_text(
    "# Patch 19 — Image sources\n\n"
    "- **Endodontics:** exact department image re-imported from Dr. Munir Silwadi Dental Centre's official website: "
    "https://silwadidentalcentres.ae/assets/img/departments/4.jpg\n"
    "- Converted locally to `assets/services/endodontics-silwadi.webp` for performance; the full official image is preserved rather than replaced with a generic stock visual.\n",
    encoding="utf-8",
)

# Global interaction styling: premium WhatsApp CTA + service mega-menu.
styles_path = ROOT / "styles.css"
styles = styles_path.read_text(encoding="utf-8")
marker = "/* Patch 19: WhatsApp + direct services navigation */"
if marker not in styles:
    styles += '''\n/* Patch 19: WhatsApp + direct services navigation */\n.header-whatsapp{min-height:42px;padding:0 14px;display:inline-flex;align-items:center;gap:8px;border:1px solid #bfe9ce;border-radius:8px;background:#f1fbf5;color:#12683d;font-size:11px;font-weight:800;letter-spacing:.01em;transition:transform .2s ease,background .2s ease,border-color .2s ease,color .2s ease,box-shadow .2s ease}.header-whatsapp svg{width:17px;height:17px;flex:0 0 17px;color:#25d366}.header-whatsapp:hover{transform:translateY(-1px);background:#e9f9ef;border-color:#8fd9aa;box-shadow:0 8px 22px rgba(37,211,102,.13)}.site-nav{gap:22px}.nav-services{position:relative;display:flex;align-items:stretch}.nav-services__trigger{display:inline-flex;align-items:center;gap:5px}.nav-services__chevron{color:#6d858d;font-size:12px;transition:transform .2s ease}.nav-services:hover .nav-services__chevron,.nav-services:focus-within .nav-services__chevron{transform:rotate(180deg)}.services-mega{position:absolute;z-index:120;top:calc(100% - 10px);left:50%;width:min(780px,calc(100vw - 48px));padding:18px;background:#fff;border:1px solid #dce6e8;border-radius:16px;box-shadow:0 22px 60px rgba(8,56,71,.16);opacity:0;visibility:hidden;pointer-events:none;transform:translate(-50%,10px);transition:opacity .18s ease,transform .18s ease,visibility .18s ease}.services-mega::before{content:"";position:absolute;left:0;right:0;top:-16px;height:16px}.nav-services:hover .services-mega,.nav-services:focus-within .services-mega{opacity:1;visibility:visible;pointer-events:auto;transform:translate(-50%,0)}.services-mega__head{display:flex;align-items:end;justify-content:space-between;gap:24px;padding:2px 4px 15px;border-bottom:1px solid #e3eaec}.services-mega__head div{display:grid;gap:3px}.services-mega__head div span{color:#0d7c90;font-size:9px;font-weight:800;letter-spacing:.13em;text-transform:uppercase}.services-mega__head div strong{color:#083847;font-size:17px;letter-spacing:-.02em}.site-nav .services-mega__head>a{padding:8px 0;color:#0d7c90;font-size:10px;font-weight:800}.services-mega__grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px;padding-top:12px}.site-nav .services-mega__grid>a{min-height:72px;padding:12px 12px 11px;display:grid;grid-template-columns:1fr auto;grid-template-rows:auto auto;column-gap:8px;align-content:center;border:1px solid transparent;border-radius:10px;transition:background .18s ease,border-color .18s ease,transform .18s ease}.site-nav .services-mega__grid>a::after,.site-nav .services-mega__head>a::after{display:none}.services-mega__grid>a:hover,.services-mega__grid>a:focus-visible{background:#f5f9f9;border-color:#d8e5e7;transform:translateY(-1px)}.services-mega__grid strong{color:#083847;font-size:11px;line-height:1.3}.services-mega__grid small{margin-top:4px;color:#688087;font-size:9px;line-height:1.35}.services-mega__grid b{grid-column:2;grid-row:1/3;align-self:center;color:#0d7c90;font-size:15px;font-weight:400}.mobile-services{border-bottom:1px solid #dce6e8}.mobile-services summary{min-height:50px;display:flex;align-items:center;justify-content:space-between;cursor:pointer;color:#083847;font-size:13px;font-weight:750;list-style:none}.mobile-services summary::-webkit-details-marker{display:none}.mobile-services summary::after{content:"+";color:#0d7c90;font-size:18px;font-weight:400}.mobile-services[open] summary::after{content:"−"}.mobile-services__links{display:grid;grid-template-columns:1fr 1fr;gap:7px;padding:0 0 14px}.mobile-services__links a{min-height:58px;padding:10px 11px!important;display:flex!important;flex-direction:column;align-items:flex-start!important;justify-content:center;border:1px solid #dce6e8!important;border-radius:9px;background:#f8fbfb}.mobile-services__links strong{color:#083847;font-size:10px;line-height:1.25}.mobile-services__links span{margin-top:3px;color:#6a8087;font-size:8px;line-height:1.3}.mobile-nav-whatsapp{display:flex!important;align-items:center!important;justify-content:center!important;gap:8px!important;min-height:46px!important;margin-top:10px;border:1px solid #bfe9ce!important;border-radius:8px;background:#f1fbf5;color:#12683d!important;font-weight:800!important}.mobile-nav-whatsapp svg{width:17px;height:17px;color:#25d366}.mobile-actionbar__whatsapp{display:flex!important;align-items:center!important;justify-content:center!important;gap:5px!important;background:#effaf3!important;color:#12683d!important}.mobile-actionbar__whatsapp svg{width:16px;height:16px;color:#25d366}.mobile-actionbar__whatsapp span{font-size:10px;font-weight:800}@media(max-width:900px){.header-whatsapp{display:none}.mobile-actionbar{grid-template-columns:1fr .8fr 1.25fr!important}.services-mega{display:none}}@media(max-width:430px){.mobile-services__links{grid-template-columns:1fr}.mobile-actionbar__whatsapp span{font-size:9px}}@media(prefers-reduced-motion:reduce){.services-mega,.nav-services__chevron,.header-whatsapp{transition:none}}\n'''
styles_path.write_text(styles, encoding="utf-8")

services_css_path = ROOT / "services.css"
services_css = services_css_path.read_text(encoding="utf-8")
if ".service-card__image--official" not in services_css:
    services_css += "\n.service-card__image--official{background:#f6f8f8}.service-card__image--official img{object-fit:contain;background:#f6f8f8}\n"
services_css_path.write_text(services_css, encoding="utf-8")
