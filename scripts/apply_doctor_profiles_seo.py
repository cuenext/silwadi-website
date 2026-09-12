from pathlib import Path
import html as html_lib
import json
import re
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-09-12"
PAGES = [
    "doctors/dr-munir-silwadi.html",
    "doctors/dr-moheb-silwadi.html",
    "doctors/dr-hani-hasbini.html",
    "doctors/dr-moammar-rifai.html",
    "doctors/dr-ahmed-el-shehri.html",
    "doctors/dr-fahed-khalil.html",
    "doctors/dr-afnan-mashal.html",
    "doctors/dr-krishnamurthy-katta-balajee.html",
    "doctors/dr-ehab-hassouneh.html",
    "doctors/dr-sara-ismail.html",
    "doctors/dr-nasr-keshkiea.html",
    "doctors/dr-dana-awad.html",
    "doctors/dr-kashmira-pawar-jayprakash.html",
    "doctors/dr-nachiket-shah.html",
    "doctors/dr-lana-masoud.html",
]


def clean(value):
    value = re.sub(r"<[^>]+>", "", value)
    return html_lib.unescape(value).replace("\xa0", " ").strip()


def extract(pattern, source, label):
    match = re.search(pattern, source, re.I | re.S)
    if not match:
        raise RuntimeError(f"Could not find {label}")
    return clean(match.group(1))


def replace_title(source, title):
    updated, count = re.subn(r"<title>.*?</title>", f"<title>{html_lib.escape(title)}</title>", source, count=1, flags=re.I | re.S)
    if count != 1:
        raise RuntimeError("Could not replace title")
    return updated


def replace_meta(source, key_type, key, value):
    pattern = rf'(<meta\s+{key_type}="{re.escape(key)}"\s+content=")[^"]*("\s*/?>)'
    replacement = rf'\g<1>{html_lib.escape(value, quote=True)}\2'
    updated, count = re.subn(pattern, replacement, source, count=1, flags=re.I)
    if count != 1:
        raise RuntimeError(f"Could not replace meta {key}")
    return updated


def visible_portrait(source, path):
    match = re.search(r'<div class="consultant-portrait__frame[^>]*>\s*<img[^>]+src="([^"]+)"', source, re.I | re.S)
    if not match:
        return None
    canonical = f"https://silwadi.ae/{path}"
    return urljoin(canonical, html_lib.unescape(match.group(1)))


def branch_works_for(clinical_base):
    value = clinical_base.lower()
    bani = {"@id": "https://silwadi.ae/#dentist"}
    raha = {"@id": "https://silwadi.ae/#dentist-al-raha"}
    if "both" in value:
        return [bani, raha]
    if "al raha" in value:
        return raha
    if "bani yas" in value:
        return bani
    raise RuntimeError(f"Unrecognized clinical base: {clinical_base}")


def treatment_topics(source):
    topics = []
    patterns = [
        r'<div class="clinical-focus-item">\s*<strong>(.*?)</strong>',
        r'<a class="profile-treatment-link"[^>]*>(.*?)<span',
    ]
    for pattern in patterns:
        for raw in re.findall(pattern, source, re.I | re.S):
            topic = clean(raw)
            if topic and topic not in topics and topic.lower() not in {"view treatments", "view all treatments"}:
                topics.append(topic)
    return topics[:8]


def breadcrumb_from_existing(source):
    match = re.search(r'<script type="application/ld\+json" data-seo-schema>(.*?)</script>', source, re.I | re.S)
    if not match:
        raise RuntimeError("Missing data-seo-schema block")
    data = json.loads(match.group(1))
    graph = data.get("@graph", []) if isinstance(data, dict) else []
    for node in graph:
        if isinstance(node, dict) and node.get("@type") == "BreadcrumbList":
            return node
    raise RuntimeError("Missing BreadcrumbList in existing schema")


def apply_page(path):
    file_path = ROOT / path
    source = file_path.read_text(encoding="utf-8")
    name = extract(r'<h1>(.*?)</h1>', source, "doctor name")
    specialty = extract(r'<p class="consultant-specialty">(.*?)</p>', source, "specialty")
    clinical_base = extract(r'<strong>Clinical base</strong>\s*<span>(.*?)</span>', source, "clinical base")
    canonical = f"https://silwadi.ae/{path}"
    portrait = visible_portrait(source, path)

    title = f"{name} | {specialty} Abu Dhabi | Silwadi"
    if "both" in clinical_base.lower():
        location_phrase = "across Bani Yas Tower and Al Raha Mall in Abu Dhabi"
    elif "al raha" in clinical_base.lower():
        location_phrase = "at Al Raha Mall in Abu Dhabi"
    elif "bani yas" in clinical_base.lower():
        location_phrase = "at Bani Yas Tower in Abu Dhabi"
    else:
        raise RuntimeError(f"Unrecognized clinical base: {clinical_base}")
    description = f"Meet {name}, {specialty} at Silwadi Dental Center {location_phrase}. View clinical focus, qualifications and appointment information."
    og_image = portrait or "https://silwadi.ae/assets/silwadi-logo-official.png"

    source = replace_title(source, title)
    source = replace_meta(source, "name", "description", description)
    source = replace_meta(source, "property", "og:type", "profile")
    source = replace_meta(source, "property", "og:title", title)
    source = replace_meta(source, "property", "og:description", description)
    source = replace_meta(source, "property", "og:image", og_image)
    source = source.replace('href="../contact.html#consultation"', 'href="../contact.html#consultation-form"')

    person = {
        "@type": "Person",
        "@id": f"{canonical}#person",
        "name": name,
        "jobTitle": specialty,
        "url": canonical,
        "worksFor": branch_works_for(clinical_base),
    }
    if portrait:
        person["image"] = portrait
    topics = treatment_topics(source)
    if topics:
        person["knowsAbout"] = topics

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            breadcrumb_from_existing(source),
            {
                "@type": "ProfilePage",
                "@id": f"{canonical}#profile",
                "url": canonical,
                "name": title,
                "mainEntity": {"@id": f"{canonical}#person"},
            },
            person,
        ],
    }
    block = '<script type="application/ld+json" data-seo-schema>' + json.dumps(schema, ensure_ascii=False, separators=(",", ":")) + "</script>"
    source, count = re.subn(r'<script type="application/ld\+json" data-seo-schema>.*?</script>', block, source, count=1, flags=re.I | re.S)
    if count != 1:
        raise RuntimeError(f"Could not replace schema for {path}")

    file_path.write_text(source, encoding="utf-8")


def update_sitemap():
    sitemap = ROOT / "sitemap.xml"
    source = sitemap.read_text(encoding="utf-8")
    for path in PAGES:
        url = f"https://silwadi.ae/{path}"
        pattern = rf'(<loc>{re.escape(url)}</loc>\s*<lastmod>)[^<]+(</lastmod>)'
        source, count = re.subn(pattern, rf'\g<1>{TODAY}\2', source, count=1)
        if count != 1:
            raise RuntimeError(f"Could not update sitemap entry for {url}")
    sitemap.write_text(source, encoding="utf-8")


def main():
    for path in PAGES:
        apply_page(path)
    update_sitemap()


if __name__ == "__main__":
    main()
