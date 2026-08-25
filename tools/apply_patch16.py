#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel, text):
    (ROOT / rel).write_text(text, encoding="utf-8")


def replace_section(text, start_pattern, end_pattern, replacement, label):
    pattern = re.compile(f"({start_pattern})[\\s\\S]*?(?={end_pattern})")
    new, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError(f"{label}: expected one section replacement, got {count}")
    return new


# ---------- Homepage ----------
home = read("index.html")
home = home.replace(
    'content="Visit Dr. Munir Silwadi Dental Centre in Abu Dhabi for general and specialist dental care at Bani Yas Tower. Established since 1980."',
    'content="Visit Dr. Munir Silwadi Dental Centre in Abu Dhabi for general and specialist dental care at Bani Yas Tower and Al Raha Mall. Established since 1980."',
)
home = home.replace(
    '<div><strong>Bani Yas Tower</strong><span>Al Raha Mall coming soon</span></div>',
    '<div><strong>2 Abu Dhabi locations</strong><span>Bani Yas Tower + Al Raha Mall</span></div>',
)

services = '''    <section class="section" id="treatments">
      <div class="container home-service-feature">
        <header class="home-service-feature__intro reveal">
          <p class="eyebrow">Dental services</p>
          <h2>General and specialist dental care.</h2>
          <p>Explore some of the services available at Silwadi. The full treatment directory follows the 10 service areas published by the centre.</p>
          <a class="text-link" href="treatments.html">View all 10 services <span>→</span></a>
        </header>

        <div class="home-service-grid" aria-label="Featured dental services">
          <a class="home-service-card reveal" href="treatments/dental-implants.html"><span class="home-service-card__mark" aria-hidden="true">IM</span><div><small>01</small><h3>Implantology</h3><p>Assessment, implant planning and implant-supported restorative care.</p><b>Learn more →</b></div></a>
          <a class="home-service-card reveal" href="treatments/orthodontics.html"><span class="home-service-card__mark" aria-hidden="true">OR</span><div><small>02</small><h3>Orthodontics</h3><p>Braces, clear aligners, retainers and bite correction.</p><b>Learn more →</b></div></a>
          <a class="home-service-card reveal" href="treatments.html#periodontics"><span class="home-service-card__mark" aria-hidden="true">PE</span><div><small>03</small><h3>Periodontics</h3><p>Care for the gums and supporting tissues around the teeth.</p><b>Learn more →</b></div></a>
          <a class="home-service-card reveal" href="treatments.html#endodontics"><span class="home-service-card__mark" aria-hidden="true">EN</span><div><small>04</small><h3>Endodontics</h3><p>Root canal treatment, retreatment and specialist endodontic care.</p><b>Learn more →</b></div></a>
          <a class="home-service-card reveal" href="treatments/cosmetic-dentistry.html"><span class="home-service-card__mark" aria-hidden="true">CO</span><div><small>05</small><h3>Cosmetic Dentistry</h3><p>Whitening, veneers and aesthetic restorative treatment.</p><b>Learn more →</b></div></a>
          <a class="home-service-card reveal" href="treatments.html#prosthodontics"><span class="home-service-card__mark" aria-hidden="true">PR</span><div><small>06</small><h3>Prosthodontics</h3><p>Crowns, bridges, dentures and implant-supported restorations.</p><b>Learn more →</b></div></a>
        </div>
        <div class="home-service-feature__urgent reveal"><span>Need urgent dental care?</span><a href="treatments/emergency-dentist.html">View urgent dental care →</a></div>
      </div>
    </section>

'''
home = replace_section(
    home,
    r'<section class="section" id="treatments">',
    r'<section class="section section--quiet" id="legacy">',
    services,
    "home services",
)

reviews = '''    <section class="home-google-reviews" id="reviews" aria-labelledby="googleReviewsTitle">
      <div class="container home-google-reviews__head reveal">
        <div><p class="eyebrow">Google reviews</p><h2 id="googleReviewsTitle">What patients say about Silwadi.</h2><p>Recent public Google reviews for the Corniche location. Review excerpts are shortened for this page.</p></div>
        <a class="google-rating-card" href="https://maps.app.goo.gl/Ln2vEZmQmgWjb3ETA" target="_blank" rel="noopener" aria-label="Read Silwadi reviews on Google Maps">
          <span class="google-rating-card__brand">Google</span><span class="google-rating-card__stars" aria-label="4.6 out of 5 stars">★★★★★</span><strong>4.6</strong><span>199 Google reviews</span><b>Read all reviews →</b>
        </a>
      </div>
      <div class="google-reviews-viewport" aria-label="Patient review excerpts">
        <div class="google-reviews-track">
          <div class="google-reviews-group">
            <article class="google-review-card"><div class="google-review-card__top"><span class="review-avatar">AH</span><div><strong>Ahmed H</strong><span>Google review</span></div></div><p>“Dr. Krishna is an excellent doctor. Very professional and experienced, and the whole process was smooth and comfortable.”</p></article>
            <article class="google-review-card"><div class="google-review-card__top"><span class="review-avatar">EC</span><div><strong>Emily Campbell Scully</strong><span>Google review</span></div></div><p>“Dr. Lujain was so friendly and knowledgeable. She put me at ease straight away.”</p></article>
            <article class="google-review-card"><div class="google-review-card__top"><span class="review-avatar">SF</span><div><strong>Sanaa Freihat</strong><span>Google review</span></div></div><p>“One of the best experiences I’ve had with a dentist. Dr. Moheb is calm and patient.”</p></article>
            <article class="google-review-card"><div class="google-review-card__top"><span class="review-avatar">AY</span><div><strong>Antoni Y</strong><span>Google review</span></div></div><p>“The reception team was so welcoming and friendly.”</p></article>
            <article class="google-review-card"><div class="google-review-card__top"><span class="review-avatar">KF</span><div><strong>Kari F</strong><span>Google review</span></div></div><p>“My cleaning was relaxing and pain free, very professional.”</p></article>
            <article class="google-review-card"><div class="google-review-card__top"><span class="review-avatar">AA</span><div><strong>Adela A</strong><span>Google review</span></div></div><p>“Dr Krishna is a very experienced orthodontist.”</p></article>
          </div>
          <div class="google-reviews-group" aria-hidden="true">
            <article class="google-review-card"><div class="google-review-card__top"><span class="review-avatar">AH</span><div><strong>Ahmed H</strong><span>Google review</span></div></div><p>“Dr. Krishna is an excellent doctor. Very professional and experienced, and the whole process was smooth and comfortable.”</p></article>
            <article class="google-review-card"><div class="google-review-card__top"><span class="review-avatar">EC</span><div><strong>Emily Campbell Scully</strong><span>Google review</span></div></div><p>“Dr. Lujain was so friendly and knowledgeable. She put me at ease straight away.”</p></article>
            <article class="google-review-card"><div class="google-review-card__top"><span class="review-avatar">SF</span><div><strong>Sanaa Freihat</strong><span>Google review</span></div></div><p>“One of the best experiences I’ve had with a dentist. Dr. Moheb is calm and patient.”</p></article>
            <article class="google-review-card"><div class="google-review-card__top"><span class="review-avatar">AY</span><div><strong>Antoni Y</strong><span>Google review</span></div></div><p>“The reception team was so welcoming and friendly.”</p></article>
            <article class="google-review-card"><div class="google-review-card__top"><span class="review-avatar">KF</span><div><strong>Kari F</strong><span>Google review</span></div></div><p>“My cleaning was relaxing and pain free, very professional.”</p></article>
            <article class="google-review-card"><div class="google-review-card__top"><span class="review-avatar">AA</span><div><strong>Adela A</strong><span>Google review</span></div></div><p>“Dr Krishna is a very experienced orthodontist.”</p></article>
          </div>
        </div>
      </div>
    </section>

'''
home = replace_section(
    home,
    r'<section class="home-digital-band" id="digital">',
    r'<section class="section home-location-split" id="locations">',
    reviews,
    "home reviews",
)
home = home.replace(
    '<p>Bani Yas Tower is open now. Our Al Raha Mall branch is coming soon.</p>',
    '<p>Silwadi now welcomes patients at Bani Yas Tower and Al Raha Mall.</p>',
)
home = home.replace('class="home-location-split__soon reveal"', 'class="home-location-split__current home-location-split__current--raha reveal"')
home = home.replace('<span class="home-location-split__status">Coming soon</span>\n            <h3>Al Raha Mall</h3>', '<span class="home-location-split__status">Now open</span>\n            <h3>Al Raha Mall</h3>')
home = home.replace(
    '<div class="home-location-split__actions"><a href="mailto:info@silwadidentalcentres.ae?subject=Al%20Raha%20Mall%20Branch">Branch enquiry →</a></div>',
    '<div class="home-location-split__actions"><a href="tel:+97126662408">Call +971 2 666 2408 →</a><a href="locations.html">Location details →</a></div>',
)
write("index.html", home)

# ---------- About: simpler, human copy ----------
about = read("about.html")
about_main = '''  <main id="main">
    <section class="institutional-hero"><div class="container"><nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span>About</span></nav><div class="institutional-hero__grid"><div><p class="eyebrow">About Silwadi</p><h1>Caring for Abu Dhabi since 1980.</h1><p class="institutional-hero__lead">Dr. Munir Silwadi Dental Centre has been caring for patients in Abu Dhabi since 1980. Today, general dentists and specialists work together across routine, cosmetic and specialist dental care.</p></div><aside class="institutional-hero__aside"><strong>More than four decades</strong><span>Two Abu Dhabi locations: Bani Yas Tower and Al Raha Mall.</span></aside></div></div></section>

    <section class="institutional-section"><div class="container story-grid"><div class="story-kicker"><p class="eyebrow">Our centre</p><h2>Good dental care starts with taking the time to listen.</h2><p>We want patients to understand what is happening, why treatment is recommended and what their options are.</p></div><div class="story-copy"><article class="story-block"><h3>We explain treatment</h3><p>Our team takes time to explain procedures and treatment options, answer questions and make sure patients know what to expect.</p></article><article class="story-block"><h3>Comfort matters</h3><p>The centre’s published approach puts patient comfort and a compassionate setting at the centre of the visit.</p></article><article class="story-block"><h3>Care under one roof</h3><p>Patients can access general and specialist dentistry, from check-ups and cleanings to implants, crowns, bridges and other treatments.</p></article></div></div></section>

    <section class="institutional-section institutional-section--quiet"><div class="container"><div class="institutional-facts"><div class="institutional-fact"><strong>Since 1980</strong><span>Dental care in Abu Dhabi</span></div><div class="institutional-fact"><strong>12 dentists &amp; specialists</strong><span>General and specialist care</span></div><div class="institutional-fact"><strong>2 locations</strong><span>Bani Yas Tower + Al Raha Mall</span></div></div></div></section>

    <section class="institutional-section"><div class="container leadership-grid"><div class="leadership-photo"><img src="assets/doctors/optimized/dr-munir-silwadi.webp" alt="Dr. Munir Silwadi" width="720" height="720" loading="lazy" decoding="async"></div><div class="leadership-copy"><p class="eyebrow">Dr. Munir Silwadi</p><h2>Specialist Prosthodontist &amp; Implantologist</h2><p>Dr. Munir Silwadi’s professional profile includes implantology, full-mouth rehabilitation and CAD/CAM aesthetic dentistry. He is also an international lecturer and certified CEREC trainer.</p><a class="btn btn--secondary" href="doctors/dr-munir-silwadi.html">View Dr. Munir’s profile</a></div></div></section>

    <section class="institutional-section"><div class="container"><header class="section-intro"><div><p class="eyebrow">Patient information</p><h2>Questions are welcome.</h2></div><p>If you are unsure which dentist or specialist you need, tell reception what you would like help with. The team can guide your appointment enquiry.</p></header><div class="principles-grid"><article class="principle"><span>01</span><h3>Ask</h3><p>Tell us what is bothering you or what treatment you are considering.</p></article><article class="principle"><span>02</span><h3>Understand</h3><p>Your dentist will explain the findings and the treatment options relevant to you.</p></article><article class="principle"><span>03</span><h3>Decide</h3><p>Take the time you need to ask questions before moving forward with treatment.</p></article></div></div></section>

    <section class="consultation-cta"><div class="container consultation-cta__inner"><div><p class="eyebrow eyebrow--light">Appointments</p><h2>Looking for a dentist at Silwadi?</h2><p>Browse the team or contact reception for help choosing the right appointment.</p></div><div class="consultation-cta__actions"><a class="btn btn--light" href="contact.html#consultation">Contact the centre</a><a class="btn btn--outline-light" href="doctors.html">Meet our doctors</a></div></div></section>
  </main>'''
about, n = re.subn(r'<main id="main">[\s\S]*?</main>', about_main, about, count=1)
if n != 1:
    raise RuntimeError("about main replacement failed")
write("about.html", about)

# ---------- Locations ----------
locations = read("locations.html")
locations = locations.replace('Dentist in Abu Dhabi - Bani Yas Tower | Silwadi Dental Center', 'Dental Clinics in Abu Dhabi | Bani Yas & Al Raha | Silwadi')
locations = locations.replace('Visit Dr. Munir Silwadi Dental Centre at Bani Yas Tower on W Corniche Road, Abu Dhabi. View opening hours, phone, directions and the upcoming Al Raha Mall location.', 'Visit Silwadi Dental Centre at Bani Yas Tower or Al Raha Mall in Abu Dhabi. Find branch phone numbers, directions and location details.')
locations_main = '''  <main id="main">
    <section class="location-hero"><div class="container"><nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span>Locations</span></nav><p class="eyebrow">Abu Dhabi</p><h1>Our locations</h1><p class="location-hero__lead">Silwadi Dental Centre now welcomes patients at Bani Yas Tower and Al Raha Mall.</p></div></section>

    <section class="location-detail location-detail--active"><div class="container location-detail__grid"><div class="location-detail__copy"><span class="location-state">Open</span><p class="location-brand">Dr. Munir Silwadi Dental Centre</p><h2>Bani Yas Tower</h2><p>Al Hilal Bank, Bani Yas Tower, Building 117 C Floor, Sultan Bin Zayed The First St, W Corniche Road, Abu Dhabi, UAE</p><dl class="location-facts"><div><dt>Phone</dt><dd><a href="tel:+97126262042">+971 2 626 2042</a></dd></div><div><dt>Email</dt><dd><a href="mailto:info@silwadidentalcentres.ae">info@silwadidentalcentres.ae</a></dd></div><div><dt>Opening hours</dt><dd>Sun–Wed 09:00–21:00 · Thu &amp; Sat 09:00–18:00 · Friday closed</dd></div><div><dt>Parking</dt><dd>Available</dd></div></dl><div class="location-actions"><a class="btn btn--primary" href="contact.html#consultation">Book a Consultation</a><a class="btn btn--secondary" href="https://www.google.com/maps/search/?api=1&amp;query=Dr%20Munir%20Silwadi%20Dental%20Centre%20Bani%20Yas%20Tower%20Abu%20Dhabi">Get Directions</a></div></div><div class="location-map"><iframe title="Map showing Dr. Munir Silwadi Dental Centre at Bani Yas Tower, Abu Dhabi" width="600" height="420" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Dr.+Munir+Silwadi+Dental+Centre+Bani+Yas+Tower+Abu+Dhabi&amp;output=embed"></iframe></div></div></section>

    <section class="location-detail location-detail--active location-detail--raha"><div class="container location-detail__grid"><div class="location-detail__copy"><span class="location-state">Now open</span><p class="location-brand">Dr. Munir Silwadi Dental Centre</p><h2>Al Raha Mall</h2><p>F14 &amp; F15, Level 1, Al Raha Mall, Channel St, Al Rahah, Abu Dhabi, UAE.</p><dl class="location-facts"><div><dt>Phone</dt><dd><a href="tel:+97126662408">+971 2 666 2408</a></dd></div><div><dt>Location</dt><dd>Al Raha Mall, Level 1</dd></div></dl><div class="location-actions"><a class="btn btn--primary" href="tel:+97126662408">Call Al Raha</a><a class="btn btn--secondary" href="https://www.google.com/maps/search/?api=1&amp;query=Dr%20Munir%20Silwadi%20Dental%20Centre%20Al%20Raha%20Mall%20Abu%20Dhabi">Get Directions</a></div></div><div class="location-map"><iframe title="Map showing Dr. Munir Silwadi Dental Centre at Al Raha Mall, Abu Dhabi" width="600" height="420" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Dr.+Munir+Silwadi+Dental+Centre+Al+Raha+Mall+Abu+Dhabi&amp;output=embed"></iframe></div></div></section>
  </main>'''
locations, n = re.subn(r'<main id="main">[\s\S]*?</main>', locations_main, locations, count=1)
if n != 1:
    raise RuntimeError("locations main replacement failed")

bani_schema = {
    "@type": "Dentist", "@id": "https://silwadi.ae/#dentist", "name": "Dr. Munir Silwadi Dental Centre", "url": "https://silwadi.ae/", "telephone": "+97126262042", "email": "info@silwadidentalcentres.ae", "image": "https://silwadi.ae/assets/silwadi-logo-official.png", "medicalSpecialty": "https://schema.org/Dentistry",
    "address": {"@type": "PostalAddress", "streetAddress": "Al Hilal Bank, Bani Yas Tower, Building 117 C Floor, Sultan Bin Zayed The First St, W Corniche Road", "addressLocality": "Abu Dhabi", "addressCountry": "AE"},
    "areaServed": {"@type": "City", "name": "Abu Dhabi"},
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["https://schema.org/Sunday", "https://schema.org/Monday", "https://schema.org/Tuesday", "https://schema.org/Wednesday"], "opens": "09:00", "closes": "21:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["https://schema.org/Thursday", "https://schema.org/Saturday"], "opens": "09:00", "closes": "18:00"},
    ],
}
raha_schema = {
    "@type": "Dentist", "@id": "https://silwadi.ae/#dentist-al-raha", "name": "Dr. Munir Silwadi Dental Centre - Al Raha Mall", "url": "https://silwadi.ae/locations.html#al-raha", "telephone": "+97126662408", "image": "https://silwadi.ae/assets/silwadi-logo-official.png", "medicalSpecialty": "https://schema.org/Dentistry",
    "address": {"@type": "PostalAddress", "streetAddress": "F14 & F15, Level 1, Al Raha Mall, Channel St, Al Rahah", "addressLocality": "Abu Dhabi", "addressCountry": "AE"}, "areaServed": {"@type": "City", "name": "Abu Dhabi"}
}
breadcrumb_locations = {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://silwadi.ae/"}, {"@type": "ListItem", "position": 2, "name": "Locations", "item": "https://silwadi.ae/locations.html"}]}
loc_json = json.dumps({"@context": "https://schema.org", "@graph": [bani_schema, raha_schema, breadcrumb_locations]}, separators=(",", ":"))
locations, n = re.subn(r'<script type="application/ld\+json" data-seo-schema>[\s\S]*?</script>', f'<script type="application/ld+json" data-seo-schema>{loc_json}</script>', locations, count=1)
if n != 1:
    raise RuntimeError("locations schema replacement failed")
write("locations.html", locations)

# ---------- Contact ----------
contact = read("contact.html")
contact = contact.replace('Contact Silwadi Dental Center Abu Dhabi | Bani Yas Tower', 'Contact Silwadi Dental Center Abu Dhabi | Two Locations')
contact = contact.replace('Contact Dr. Munir Silwadi Dental Centre at Bani Yas Tower, Abu Dhabi for consultations, appointment enquiries, directions and insurance questions.', 'Contact Silwadi Dental Centre in Abu Dhabi for Bani Yas Tower or Al Raha Mall appointments, directions and insurance enquiries.')
contact = contact.replace(
    '<article class="guidance-card"><span>Second location</span><h3>Al Raha Mall</h3><p>F14 &amp; F15, Level 1, Al Raha Mall, Abu Dhabi, UAE. The branch is currently shown as coming soon.</p></article>',
    '<article class="guidance-card"><span>Al Raha Mall · now open</span><h3>Second Abu Dhabi location</h3><p>F14 &amp; F15, Level 1, Al Raha Mall, Abu Dhabi, UAE.</p><p><a href="tel:+97126662408">Call +971 2 666 2408 →</a></p></article>',
)
contact_json = json.dumps({"@context": "https://schema.org", "@graph": [bani_schema, raha_schema, {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://silwadi.ae/"}, {"@type": "ListItem", "position": 2, "name": "Contact", "item": "https://silwadi.ae/contact.html"}]}]}, separators=(",", ":"))
contact, n = re.subn(r'<script type="application/ld\+json" data-seo-schema>[\s\S]*?</script>', f'<script type="application/ld+json" data-seo-schema>{contact_json}</script>', contact, count=1)
if n != 1:
    raise RuntimeError("contact schema replacement failed")
write("contact.html", contact)

# ---------- Sitewide logo + remove Digital Dentistry from nav/footer ----------
for page in sorted(ROOT.rglob("*.html")):
    if page.name == "digital-dentistry.html":
        continue
    rel = page.relative_to(ROOT)
    depth = len(rel.parts) - 1
    prefix = "../" * depth
    logo = f"{prefix}assets/silwadi-logo-official.png"
    text = page.read_text(encoding="utf-8")
    text = text.replace("https://silwadi.ae/assets/silwadi-logo-original.jpeg", "https://silwadi.ae/assets/silwadi-logo-official.png")
    text = text.replace(f'{prefix}assets/silwadi-logo-original.jpeg', logo)
    text = re.sub(r'<a class="brand"([^>]*)><span class="brand-crop"><img[^>]*alt="Silwadi Dental Center"[^>]*></span></a>', rf'<a class="brand site-brand-logo"\1><img src="{logo}" alt="Silwadi Dental Center" width="180" height="180" decoding="async"></a>', text)
    text = text.replace('class="brand home-brand-logo"', 'class="brand site-brand-logo home-brand-logo"')
    text = re.sub(r'<span class="footer-logo-crop"><img[^>]*alt="Silwadi Dental Center"[^>]*></span>', f'<img class="site-footer-logo" src="{logo}" alt="Silwadi Dental Center" width="180" height="180" loading="lazy" decoding="async">', text)
    text = text.replace('class="home-footer-logo"', 'class="site-footer-logo home-footer-logo"')
    text = re.sub(r'<a[^>]+href="(?:\.\./)?digital-dentistry\.html"[^>]*>\s*Digital Dentistry\s*</a>', '', text, flags=re.I)
    page.write_text(text, encoding="utf-8")

# ---------- Shared logo styling ----------
styles = read("styles.css")
if "/* Patch 16 sitewide brand */" not in styles:
    styles += '''\n\n/* Patch 16 sitewide brand */
.site-brand-logo{display:flex;align-items:center;justify-content:center;width:82px;height:72px;flex:0 0 82px;overflow:visible}
.site-brand-logo img{display:block;width:68px;height:68px;object-fit:contain;object-position:center}
.site-footer-logo{display:block;width:108px;height:108px;object-fit:contain;margin:0 0 10px}
@media(max-width:720px){.site-brand-logo{width:68px;height:62px;flex-basis:68px}.site-brand-logo img{width:58px;height:58px}.site-footer-logo{width:92px;height:92px}}
'''
write("styles.css", styles)

# ---------- Homepage card/review styling ----------
home_css = read("home-premium.css")
if "/* Patch 16 service cards + Google reviews */" not in home_css:
    home_css += '''\n\n/* Patch 16 service cards + Google reviews */
.home-service-feature{display:block}
.home-service-feature__intro{max-width:760px;margin:0 auto 42px;text-align:center}
.home-service-feature__intro h2{margin:10px 0 14px;color:#083847;font-size:clamp(34px,4.5vw,56px);line-height:1.04;letter-spacing:-.04em}
.home-service-feature__intro>p:not(.eyebrow){max-width:660px;margin:0 auto 18px;color:#526a73;font-size:13px;line-height:1.75}
.home-service-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.home-service-card{min-height:310px;border:1px solid #dce7e9;border-radius:22px;background:#fff;overflow:hidden;display:flex;flex-direction:column;color:#083847;transition:transform .22s ease,box-shadow .22s ease,border-color .22s ease}
.home-service-card:hover{transform:translateY(-4px);box-shadow:0 18px 44px rgba(8,56,71,.10);border-color:#bfd4d8}
.home-service-card__mark{min-height:132px;display:flex;align-items:flex-end;padding:22px 24px;background:linear-gradient(135deg,#e7f5f6 0%,#f5f8f8 65%,#eef1f2 100%);color:#0b7f91;font-size:48px;font-weight:720;letter-spacing:-.06em}
.home-service-card>div{padding:22px 24px 24px;display:flex;flex-direction:column;flex:1}
.home-service-card small{color:#526a73;font-size:9px;font-weight:800;letter-spacing:.12em}
.home-service-card h3{margin:8px 0 8px;font-size:20px;letter-spacing:-.025em}
.home-service-card p{margin:0 0 18px;color:#526a73;font-size:11px;line-height:1.65}
.home-service-card b{margin-top:auto;color:#0b7f91;font-size:10px}
.home-service-feature__urgent{margin-top:20px;padding:19px 22px;border-radius:16px;background:#f4f8f8;display:flex;justify-content:space-between;gap:20px;align-items:center}

.home-google-reviews{padding:104px 0;background:#f6f8f9;overflow:hidden;border-top:1px solid #e2eaec;border-bottom:1px solid #e2eaec}
.home-google-reviews__head{display:grid;grid-template-columns:1fr 280px;gap:72px;align-items:end;margin-bottom:42px}
.home-google-reviews__head h2{margin:9px 0 12px;color:#083847;font-size:clamp(36px,4.8vw,58px);line-height:1.03;letter-spacing:-.045em}
.home-google-reviews__head>div>p:not(.eyebrow){max-width:600px;margin:0;color:#526a73;font-size:12px;line-height:1.7}
.google-rating-card{padding:24px;border:1px solid #d9e4e6;border-radius:20px;background:#fff;box-shadow:0 14px 36px rgba(8,56,71,.07);display:grid;grid-template-columns:1fr auto;align-items:end;gap:6px 16px;color:#083847}
.google-rating-card__brand{grid-column:1/-1;font-size:17px;font-weight:700;letter-spacing:-.02em}
.google-rating-card__stars{grid-column:1/-1;color:#f5b51b;letter-spacing:2px;font-size:16px}
.google-rating-card strong{font-size:45px;line-height:1;font-weight:680;letter-spacing:-.05em}
.google-rating-card>span:nth-of-type(3){color:#526a73;font-size:10px;align-self:center}
.google-rating-card b{grid-column:1/-1;margin-top:8px;color:#0b7f91;font-size:10px}
.google-reviews-viewport{width:100%;overflow:hidden;padding:4px 0 12px}
.google-reviews-track{display:flex;width:max-content;animation:reviews-marquee 46s linear infinite;will-change:transform}
.google-reviews-track:hover,.google-reviews-track:focus-within{animation-play-state:paused}
.google-reviews-group{display:flex;gap:18px;padding-right:18px}
.google-review-card{width:350px;min-height:220px;padding:24px;border:1px solid #dce6e8;border-radius:20px;background:#fff;box-shadow:0 8px 28px rgba(8,56,71,.055);display:flex;flex-direction:column}
.google-review-card__top{display:flex;align-items:center;gap:12px;margin-bottom:21px}
.review-avatar{width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#e7f3f4;color:#0b7f91;font-size:11px;font-weight:800;flex:0 0 42px}
.google-review-card__top div{display:flex;flex-direction:column;gap:3px}.google-review-card__top strong{color:#083847;font-size:12px}.google-review-card__top span{color:#60777f;font-size:9px}
.google-review-card p{margin:0;color:#435f68;font-size:12px;line-height:1.72}
@keyframes reviews-marquee{from{transform:translateX(0)}to{transform:translateX(-50%)}}

.home-location-split__current--raha{background:#eef8f8}

@media(max-width:1040px){.home-service-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.home-google-reviews__head{grid-template-columns:1fr 250px;gap:40px}}
@media(max-width:720px){.home-service-feature__intro{text-align:left;margin-bottom:28px}.home-service-feature__intro>p:not(.eyebrow){margin-left:0}.home-service-grid{grid-template-columns:1fr 1fr;gap:12px}.home-service-card{min-height:255px;border-radius:17px}.home-service-card__mark{min-height:92px;padding:16px 17px;font-size:35px}.home-service-card>div{padding:16px 17px 18px}.home-service-card h3{font-size:16px}.home-service-card p{font-size:9.5px}.home-service-feature__urgent{align-items:flex-start;flex-direction:column}.home-google-reviews{padding:72px 0}.home-google-reviews__head{grid-template-columns:1fr;gap:24px;margin-bottom:30px}.google-rating-card{max-width:290px}.google-review-card{width:285px;min-height:205px;padding:20px}}
@media(max-width:430px){.home-service-grid{grid-template-columns:1fr}.home-service-card{min-height:225px}.home-service-card__mark{min-height:82px}.google-review-card{width:270px}}
@media(prefers-reduced-motion:reduce){.google-reviews-viewport{overflow-x:auto}.google-reviews-track{animation:none;will-change:auto}}
'''
write("home-premium.css", home_css)

# ---------- Local business source of truth ----------
local = json.loads(read("data/local-business.json"))
local["verified_on"] = "2026-08-25"
local.pop("coming_soon", None)
local["al_raha"] = {
    "name": "Al Raha Mall",
    "address": "F14 & F15, Level 1, Al Raha Mall, Channel St, Al Rahah, Abu Dhabi, UAE",
    "phone_display": "+971 2 666 2408",
    "phone_e164": "+97126662408",
    "is_open": True,
}
write("data/local-business.json", json.dumps(local, indent=2, ensure_ascii=False) + "\n")

site_config = json.loads(read("data/site-config.json"))
site_config["default_social_image"] = "https://silwadi.ae/assets/silwadi-logo-official.png"
write("data/site-config.json", json.dumps(site_config, indent=2) + "\n")

# ---------- Remove standalone Digital Dentistry page from indexable site ----------
digital = ROOT / "digital-dentistry.html"
if digital.exists():
    digital.unlink()

sitemap = read("sitemap.xml")
sitemap = re.sub(r'\s*<url>\s*<loc>https://silwadi\.ae/digital-dentistry\.html</loc>\s*<lastmod>[^<]+</lastmod>\s*</url>', '', sitemap)
sitemap = re.sub(r'<lastmod>\d{4}-\d{2}-\d{2}</lastmod>', '<lastmod>2026-08-25</lastmod>', sitemap)
write("sitemap.xml", sitemap)

# ---------- Update earlier regression assumptions superseded by current facts ----------
p6 = read("tests/test_patch6_contract.py")
p6 = p6.replace("'index.html', 'doctors.html', 'about.html', 'digital-dentistry.html',\n            'treatments.html'", "'index.html', 'doctors.html', 'about.html',\n            'treatments.html'")
p6 = p6.replace("def test_locations_page_has_active_and_coming_soon_branches(self):", "def test_locations_page_has_two_active_branches(self):")
p6 = p6.replace("        self.assertIn('Coming Soon', html)\n", "        self.assertIn('Now open', html)\n        self.assertIn('+971 2 666 2408', html)\n")
p6 = p6.replace("            'digital-dentistry.html', 'contact.html', 'locations.html'", "            'contact.html', 'locations.html'")
p6 = re.sub(r"    def test_locations_page_does_not_claim_unverified_parking_or_open_al_raha\(self\):[\s\S]*?\n\n\nif __name__", '''    def test_locations_page_keeps_parking_claim_conservative_and_raha_open(self):
        html = read('locations.html').lower()
        self.assertNotIn('free parking', html)
        self.assertNotIn('valet', html)
        self.assertIn('now open', html)
        self.assertIn('+971 2 666 2408', html)


if __name__''', p6)
write("tests/test_patch6_contract.py", p6)

p7 = read("tests/test_patch7_local_seo.py")
p7 = p7.replace("    'digital-dentistry.html', 'locations.html', 'contact.html'", "    'locations.html', 'contact.html'")
p7 = p7.replace("        self.assertFalse(data['coming_soon']['is_open'])", "        self.assertTrue(data['al_raha']['is_open'])\n        self.assertEqual(data['al_raha']['phone_e164'], '+97126662408')")
p7 = re.sub(r"    def test_al_raha_remains_non_operational\(self\):[\s\S]*?\n\n    def test_unverified", '''    def test_al_raha_is_operational(self):
        html = read('locations.html').lower()
        self.assertIn('now open', html)
        self.assertIn('+971 2 666 2408', html)
        self.assertNotIn('coming soon', html)

    def test_unverified''', p7)
write("tests/test_patch7_local_seo.py", p7)

for rel in ("tests/test_patch8_technical_seo.py", "tests/test_patch12_launch_seo.py"):
    text = read(rel)
    text = text.replace("    'digital-dentistry.html': 'https://silwadi.ae/digital-dentistry.html',\n", "")
    text = text.replace("self.assertEqual(len(locs), 24)", "self.assertEqual(len(locs), 23)")
    text = text.replace("self.assertIn('24 pages', result.stdout)", "self.assertIn('23 pages', result.stdout)")
    text = text.replace("LAUNCH_DATE = '2026-08-22'", "LAUNCH_DATE = '2026-08-25'")
    if rel.endswith("test_patch8_technical_seo.py"):
        text = text.replace("self.assertEqual(data['default_social_image'], 'https://silwadi.ae/assets/silwadi-logo-original.jpeg')", "self.assertEqual(data['default_social_image'], 'https://silwadi.ae/assets/silwadi-logo-official.png')")
        text = re.sub(r"    def test_contact_and_locations_reference_same_active_dentist_only\(self\):[\s\S]*?\n\n    def test_non_home_pages_have_breadcrumb_schema", '''    def test_contact_and_locations_reference_both_active_branches(self):
        for rel in ['contact.html', 'locations.html']:
            practice_nodes = [n for n in nodes(rel) if n.get('@type') == 'Dentist']
            self.assertEqual(len(practice_nodes), 2, rel)
            self.assertEqual(practice_nodes[0]['@id'], 'https://silwadi.ae/#dentist', rel)
            self.assertEqual(practice_nodes[1]['@id'], 'https://silwadi.ae/#dentist-al-raha', rel)
            self.assertEqual(practice_nodes[1]['telephone'], '+97126662408', rel)
            for node in practice_nodes:
                self.assertFalse(has_key_deep(node, 'aggregateRating'))
                self.assertFalse(has_key_deep(node, 'review'))

    def test_non_home_pages_have_breadcrumb_schema''', text)
    write(rel, text)

p15 = read("tests/test_patch15_homepage_redesign.py")
p15 = p15.replace("            'home-digital-band',\n", "            'home-google-reviews',\n")
write("tests/test_patch15_homepage_redesign.py", p15)

# Patch 12/8 page count and audit.
audit = read("tools/seo_launch_audit.py").replace("if len(locs) != 24:", "if len(locs) != 23:").replace("expected 24 canonical URLs", "expected 23 canonical URLs")
write("tools/seo_launch_audit.py", audit)

print("Patch 16 changes applied")
