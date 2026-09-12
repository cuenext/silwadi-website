from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://silwadi.ae"
ORG_ID = f"{BASE}/#organization"
BANI_ID = f"{BASE}/#dentist"
RAHA_ID = f"{BASE}/#dentist-al-raha"
WEBSITE_ID = f"{BASE}/#website"


def load(path):
    return (ROOT / path).read_text(encoding="utf-8")


def save(path, value):
    (ROOT / path).write_text(value, encoding="utf-8")


def mutate_jsonld_script(path, marker, mutate):
    html = load(path)
    pattern = re.compile(
        rf'(<script[^>]*type="application/ld\+json"[^>]*{re.escape(marker)}[^>]*>)(.*?)(</script>)',
        re.I | re.S,
    )
    matches = list(pattern.finditer(html))
    if len(matches) != 1:
        raise RuntimeError(f"Expected exactly one {marker} JSON-LD block in {path}, found {len(matches)}")
    match = matches[0]
    data = json.loads(match.group(2))
    mutate(data)
    encoded = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    html = html[:match.start()] + match.group(1) + encoded + match.group(3) + html[match.end():]
    save(path, html)


def graph(data):
    if not isinstance(data, dict) or not isinstance(data.get("@graph"), list):
        raise RuntimeError("Expected JSON-LD @graph")
    return data["@graph"]


def by_id(items, entity_id):
    for item in items:
        if isinstance(item, dict) and item.get("@id") == entity_id:
            return item
    return None


def bani_entity():
    return {
        "@type": "Dentist",
        "@id": BANI_ID,
        "name": "Dr. Munir Silwadi Dental Centre",
        "url": f"{BASE}/locations.html#bani-yas",
        "telephone": "+97126262042",
        "email": "info@silwadidentalcentres.ae",
        "image": f"{BASE}/assets/silwadi-logo-official.png",
        "medicalSpecialty": "https://schema.org/Dentistry",
        "parentOrganization": {"@id": ORG_ID},
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Bani Yas Tower, Building 117 C Floor, Sultan Bin Zayed The First St, W Corniche Road",
            "addressLocality": "Abu Dhabi",
            "addressCountry": "AE",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": 24.443115, "longitude": 54.394263},
        "areaServed": {"@type": "City", "name": "Abu Dhabi"},
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": [
                    "https://schema.org/Sunday", "https://schema.org/Monday",
                    "https://schema.org/Tuesday", "https://schema.org/Wednesday",
                ],
                "opens": "09:00", "closes": "21:00",
            },
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["https://schema.org/Thursday", "https://schema.org/Saturday"],
                "opens": "09:00", "closes": "18:00",
            },
        ],
    }


def raha_entity():
    return {
        "@type": "Dentist",
        "@id": RAHA_ID,
        "name": "Dr. Mohamed Munir Dental Centre - Al Raha Mall",
        "url": f"{BASE}/locations.html#al-raha",
        "telephone": "+97126662408",
        "email": "info@silwadidentalcentres.ae",
        "image": f"{BASE}/assets/silwadi-logo-official.png",
        "medicalSpecialty": "https://schema.org/Dentistry",
        "parentOrganization": {"@id": ORG_ID},
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "F14 & F15, Level 1, Al Raha Mall, Channel St, Al Rahah",
            "addressLocality": "Abu Dhabi",
            "addressCountry": "AE",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": 24.432323448790137, "longitude": 54.468755061562355},
        "areaServed": {"@type": "City", "name": "Abu Dhabi"},
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": [
                    "https://schema.org/Saturday", "https://schema.org/Sunday",
                    "https://schema.org/Monday", "https://schema.org/Tuesday",
                    "https://schema.org/Wednesday", "https://schema.org/Thursday",
                ],
                "opens": "10:00", "closes": "19:00",
            }
        ],
    }


def organization_entity():
    return {
        "@type": "Organization",
        "@id": ORG_ID,
        "name": "Silwadi Dental Center",
        "alternateName": "Dr. Munir Silwadi Dental Centre",
        "url": f"{BASE}/",
        "logo": {"@type": "ImageObject", "url": f"{BASE}/assets/silwadi-logo-official.png"},
        "email": "info@silwadidentalcentres.ae",
        "foundingDate": "1980",
        "founder": {"@id": f"{BASE}/doctors/dr-munir-silwadi.html#person"},
        "sameAs": ["https://www.instagram.com/dr.munirsilwadidental/"],
        "subOrganization": [{"@id": BANI_ID}, {"@id": RAHA_ID}],
    }


def patch_home(data):
    items = graph(data)
    website = by_id(items, WEBSITE_ID)
    if website is None:
        raise RuntimeError("Homepage WebSite entity missing")
    website["publisher"] = {"@id": ORG_ID}

    # Replace the branch definitions with the canonical factual versions while
    # preserving all unrelated entities in the existing graph.
    items[:] = [item for item in items if not (isinstance(item, dict) and item.get("@id") in {ORG_ID, BANI_ID, RAHA_ID})]
    website_index = items.index(website)
    items[website_index:website_index] = [organization_entity()]
    items.extend([bani_entity(), raha_entity()])


def patch_core_branches(data):
    items = graph(data)
    bani = by_id(items, BANI_ID)
    raha = by_id(items, RAHA_ID)
    if bani is None or raha is None:
        raise RuntimeError("Expected both branch entities")
    bani.update(bani_entity())
    raha.update(raha_entity())


def patch_about(data):
    items = graph(data)
    entity = by_id(items, f"{BASE}/about.html#about")
    if entity is None:
        raise RuntimeError("AboutPage entity missing")
    entity["about"] = {"@id": ORG_ID}
    entity["isPartOf"] = {"@id": WEBSITE_ID}


def patch_collection(path, page_id):
    def mutate(data):
        items = graph(data)
        entity = by_id(items, page_id)
        if entity is None:
            raise RuntimeError(f"Collection/page entity missing in {path}")
        entity["isPartOf"] = {"@id": WEBSITE_ID}
        entity["about"] = {"@id": ORG_ID}
    mutate_jsonld_script(path, "data-public-core-seo-v1", mutate)


def main():
    mutate_jsonld_script("index.html", "data-seo-schema", patch_home)
    mutate_jsonld_script("locations.html", "data-seo-schema", patch_core_branches)
    mutate_jsonld_script("contact.html", "data-seo-schema", patch_core_branches)
    mutate_jsonld_script("about.html", "data-seo-schema", patch_about)
    patch_collection("doctors.html", f"{BASE}/doctors.html#page")
    patch_collection("locations.html", f"{BASE}/locations.html#page")

    # ContactPage is not a graph in its secondary block, so add graph references
    # without altering any visible content.
    def patch_contact_page(data):
        if not isinstance(data, dict) or data.get("@id") != f"{BASE}/contact.html#page":
            raise RuntimeError("ContactPage entity missing")
        data["isPartOf"] = {"@id": WEBSITE_ID}
        data["about"] = {"@id": ORG_ID}
    mutate_jsonld_script("contact.html", "data-public-core-seo-v1", patch_contact_page)

    print("Applied Silwadi Google authority entity-graph patch")


if __name__ == "__main__":
    main()
