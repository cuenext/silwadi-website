from pathlib import Path
import html as html_lib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    "doctors.html",
    "about.html",
    "locations.html",
    "contact.html",
    "treatments.html",
    "treatments/dental-implants.html",
    "treatments/orthodontics.html",
    "treatments/cosmetic-dentistry.html",
    "treatments/general-dentistry.html",
    "treatments/emergency-dentist.html",
]

DOCTORS = [
    ("Dr. Munir Silwadi", "doctors/dr-munir-silwadi.html"),
    ("Dr. Moheb Silwadi", "doctors/dr-moheb-silwadi.html"),
    ("Dr. Hani Hasbini", "doctors/dr-hani-hasbini.html"),
    ("Dr. Moammar Mohamed Rifai", "doctors/dr-moammar-rifai.html"),
    ("Dr. Ahmed El Shehri", "doctors/dr-ahmed-el-shehri.html"),
    ("Dr. Fahed Abi Khalil", "doctors/dr-fahed-khalil.html"),
    ("Dr. Afnan Mashal", "doctors/dr-afnan-mashal.html"),
    ("Dr. Krishnamurthy Balajee", "doctors/dr-krishnamurthy-katta-balajee.html"),
    ("Dr. Ehab Hassouneh Bassam A", "doctors/dr-ehab-hassouneh.html"),
    ("Dr. Sara Ismail", "doctors/dr-sara-ismail.html"),
    ("Dr. Nasr Keshkiea", "doctors/dr-nasr-keshkiea.html"),
    ("Dr. Dana Awad", "doctors/dr-dana-awad.html"),
    ("Dr. Kashmira Pawar Jayprakash", "doctors/dr-kashmira-pawar-jayprakash.html"),
    ("Dr. Nachiket Shah", "doctors/dr-nachiket-shah.html"),
    ("Dr. Lana Masoud", "doctors/dr-lana-masoud.html"),
]

TREATMENTS = [
    ("Dental Implants", "treatments/dental-implants.html"),
    ("Prosthodontics", "services.html#prosthodontics"),
    ("Orthodontics", "treatments/orthodontics.html"),
    ("Periodontics", "services.html#periodontics"),
    ("Endodontics", "services.html#endodontics"),
    ("Pediatric Dentistry", "services.html#pedodontics"),
    ("Cosmetic Dentistry", "treatments/cosmetic-dentistry.html"),
    ("Preventive Dentistry", "services.html#preventive-dentistry"),
    ("General Dentistry", "treatments/general-dentistry.html"),
    ("Emergency Dentistry", "treatments/emergency-dentist.html"),
]

OG_IMAGES = {
    "about.html": "https://silwadi.ae/assets/about/silwadi-clinic-original.jpg",
    "contact.html": "https://silwadi.ae/assets/locations/bani-yas-reception.webp",
    "treatments/dental-implants.html": "https://silwadi.ae/assets/services/implantology.webp",
    "treatments/orthodontics.html": "https://silwadi.ae/assets/services/orthodontics.webp",
    "treatments/cosmetic-dentistry.html": "https://silwadi.ae/assets/services/cosmetic-dentistry.webp",
    "treatments/general-dentistry.html": "https://silwadi.ae/assets/services/preventive-dentistry.webp",
}

DETAIL_PAGES = {
    "treatments/dental-implants.html",
    "treatments/orthodontics.html",
    "treatments/cosmetic-dentistry.html",
    "treatments/general-dentistry.html",
    "treatments/emergency-dentist.html",
}


def list_items(items):
    return [
        {
            "@type": "ListItem",
            "position": index,
            "name": name,
            "url": f"https://silwadi.ae/{url}",
        }
        for index, (name, url) in enumerate(items, 1)
    ]


def extra_schema(path, source):
    if path == "doctors.html":
        return {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "CollectionPage",
                    "@id": "https://silwadi.ae/doctors.html#page",
                    "url": "https://silwadi.ae/doctors.html",
                    "name": "Dentists and Dental Specialists in Abu Dhabi",
                    "mainEntity": {"@id": "https://silwadi.ae/doctors.html#doctor-list"},
                },
                {
                    "@type": "ItemList",
                    "@id": "https://silwadi.ae/doctors.html#doctor-list",
                    "name": "Silwadi Dental Center medical team",
                    "numberOfItems": 15,
                    "itemListElement": list_items(DOCTORS),
                },
            ],
        }
    if path == "treatments.html":
        return {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "CollectionPage",
                    "@id": "https://silwadi.ae/treatments.html#page",
                    "url": "https://silwadi.ae/treatments.html",
                    "name": "Dental Treatments in Abu Dhabi",
                    "mainEntity": {"@id": "https://silwadi.ae/treatments.html#treatment-list"},
                },
                {
                    "@type": "ItemList",
                    "@id": "https://silwadi.ae/treatments.html#treatment-list",
                    "name": "Silwadi Dental Center treatment areas",
                    "numberOfItems": 10,
                    "itemListElement": list_items(TREATMENTS),
                },
            ],
        }
    if path == "locations.html":
        return {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "CollectionPage",
                    "@id": "https://silwadi.ae/locations.html#page",
                    "url": "https://silwadi.ae/locations.html",
                    "name": "Silwadi Dental Center Locations in Abu Dhabi",
                    "mainEntity": {"@id": "https://silwadi.ae/locations.html#location-list"},
                },
                {
                    "@type": "ItemList",
                    "@id": "https://silwadi.ae/locations.html#location-list",
                    "name": "Silwadi Dental Center locations",
                    "numberOfItems": 2,
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Bani Yas Tower", "url": "https://silwadi.ae/locations.html#bani-yas"},
                        {"@type": "ListItem", "position": 2, "name": "Al Raha Mall", "url": "https://silwadi.ae/locations.html#al-raha"},
                    ],
                },
            ],
        }
    if path == "contact.html":
        return {
            "@context": "https://schema.org",
            "@type": "ContactPage",
            "@id": "https://silwadi.ae/contact.html#page",
            "url": "https://silwadi.ae/contact.html",
            "name": "Contact Silwadi Dental Center Abu Dhabi",
            "mainEntity": [
                {"@id": "https://silwadi.ae/#dentist"},
                {"@id": "https://silwadi.ae/#dentist-al-raha"},
            ],
        }
    if path in DETAIL_PAGES:
        pairs = re.findall(
            r'<button class="faq-question"[^>]*>(.*?)<span>\+</span></button>\s*<div class="faq-answer">(.*?)</div>',
            source,
            re.I | re.S,
        )
        entities = []
        for question, answer in pairs:
            question = html_lib.unescape(re.sub(r"<[^>]+>", "", question)).strip()
            answer = html_lib.unescape(re.sub(r"<[^>]+>", "", answer)).strip()
            if question and answer:
                entities.append(
                    {
                        "@type": "Question",
                        "name": question,
                        "acceptedAnswer": {"@type": "Answer", "text": answer},
                    }
                )
        if len(entities) < 2:
            raise RuntimeError(f"Expected visible FAQ content in {path}; found {len(entities)} entries")
        return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}
    return None


def replace_og_image(source, url):
    pattern = r'(<meta\s+property="og:image"\s+content=")[^"]+("\s*/?>)'
    updated, count = re.subn(pattern, rf'\g<1>{url}\2', source, count=1, flags=re.I)
    if count != 1:
        raise RuntimeError("Could not replace og:image")
    return updated


def apply_page(path):
    file_path = ROOT / path
    source = file_path.read_text(encoding="utf-8")
    source = source.replace('href="contact.html#consultation"', 'href="contact.html#consultation-form"')
    source = source.replace('href="../contact.html#consultation"', 'href="../contact.html#consultation-form"')
    if path in OG_IMAGES:
        source = replace_og_image(source, OG_IMAGES[path])
    schema = extra_schema(path, source)
    marker = "data-public-core-seo-v1"
    if schema and marker not in source:
        block = '<script type="application/ld+json" data-public-core-seo-v1>' + json.dumps(schema, ensure_ascii=False, separators=(",", ":")) + "</script>"
        if "</head>" not in source:
            raise RuntimeError(f"Missing </head> in {path}")
        source = source.replace("</head>", block + "</head>", 1)
    file_path.write_text(source, encoding="utf-8")


def update_sitemap():
    sitemap = ROOT / "sitemap.xml"
    source = sitemap.read_text(encoding="utf-8")
    for path in TARGETS:
        url = f"https://silwadi.ae/{path}"
        pattern = rf'(<loc>{re.escape(url)}</loc>\s*<lastmod>)[^<]+(</lastmod>)'
        source, count = re.subn(pattern, rf'\g<1>2026-09-12\2', source, count=1)
        if count != 1:
            raise RuntimeError(f"Could not update sitemap entry for {url}")
    sitemap.write_text(source, encoding="utf-8")


def main():
    for path in TARGETS:
        apply_page(path)
    update_sitemap()


if __name__ == "__main__":
    main()
