# Patch 7 Local SEO Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Normalize verified local business information across the site, strengthen natural Abu Dhabi relevance, and give Patch 8 a reliable local-business source of truth for structured data.

**Architecture:** Keep the current static HTML/CSS/JS site. Add one small JSON source of truth at `data/local-business.json` containing the verified clinic identity, phone, address, hours, service area and coming-soon branch state. Important NAP remains visible directly in HTML; tests compare visible pages against that data so local information cannot silently drift. No canonical/schema/sitemap/robots work is included here.

**Tech Stack:** Static HTML5, CSS3, vanilla JavaScript, JSON, Python `unittest`, existing PowerShell local server.

**Spec:** `docs/superpowers/specs/2026-08-22-silwadi-seo-human-copy-local-growth-design.md`

## Global Constraints

- Source of truth for the active clinic is the clinic's own current public website, verified on 2026-08-22.
- Canonical visible business name: `Dr. Munir Silwadi Dental Centre`.
- Active location label: `Bani Yas Tower`.
- Phone display: `+971 2 626 2042`; telephone URI: `tel:+97126262042`.
- Email: `info@silwadidentalcentres.ae`.
- Canonical active address display: `Al Hilal Bank, Bani Yas Tower, Building 117 C Floor, Sultan Bin Zayed The First St, W Corniche Road, Abu Dhabi, UAE`.
- Verified hours: Sunday–Wednesday `09:00–21:00`; Thursday & Saturday `09:00–18:00`; Friday closed.
- Local service-area wording stays broad: `Abu Dhabi`; do not invent a radius or unsupported neighborhoods.
- Al Raha Mall remains `Coming Soon` and must not be represented as operating.
- Do not use `Corniche Branch` as an official business/branch name unless the clinic later confirms it; third-party results are not authoritative enough for NAP.
- Do not add ratings, review counts, parking claims, insurance acceptance, emergency hours or other unsupported local facts.
- Do not add schema, canonicals, sitemap or robots files in Patch 7; those are Patch 8.
- Keep local copy short and natural; do not repeat `dentist Abu Dhabi` unnaturally.

---

## File Structure

**Create**
- `data/local-business.json` — verified active-clinic source of truth used by tests now and Patch 8 structured-data work later.
- `tests/test_patch7_local_seo.py` — dedicated NAP/local-intent contracts.

**Modify**
- `index.html`
- `locations.html`
- `contact.html`
- `doctors.html`
- `treatments.html`
- `about.html`
- `digital-dentistry.html`
- `doctors/dr-munir-silwadi.html`
- `treatments/dental-implants.html`
- `contact-pages.css`
- `location-pages.css`
- `styles.css` only if footer NAP needs a small reusable rule.

**Unchanged in this patch**
- `app.js`
- canonical tags
- JSON-LD/schema
- `robots.txt`
- `sitemap.xml`

---

### Task 1: Define verified local-business contracts

**Files:**
- Create: `tests/test_patch7_local_seo.py`
- Create: `data/local-business.json`

**Interfaces:**
- `data/local-business.json` produces exact keys used by tests and later Patch 8: `brand_name`, `branch_label`, `phone_display`, `phone_e164`, `email`, `address`, `hours_display`, `hours`, `service_area`, `maps_query`, `coming_soon`.

- [ ] **Step 1: Create the failing contract test**

Create `tests/test_patch7_local_seo.py`:

```python
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

ROOT_PAGES = [
    'index.html', 'doctors.html', 'treatments.html', 'about.html',
    'digital-dentistry.html', 'locations.html', 'contact.html'
]
NESTED_PAGES = [
    'doctors/dr-munir-silwadi.html',
    'treatments/dental-implants.html',
]


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')


class PatchSevenLocalSEOContract(unittest.TestCase):
    def local_data(self):
        return json.loads(read('data/local-business.json'))

    def test_local_business_source_of_truth_exists(self):
        path = ROOT / 'data/local-business.json'
        self.assertTrue(path.is_file(), 'data/local-business.json')
        data = self.local_data()
        self.assertEqual(data['brand_name'], 'Dr. Munir Silwadi Dental Centre')
        self.assertEqual(data['branch_label'], 'Bani Yas Tower')
        self.assertEqual(data['phone_e164'], '+97126262042')
        self.assertEqual(data['service_area'], 'Abu Dhabi')
        self.assertFalse(data['coming_soon']['is_open'])

    def test_contact_and_locations_use_identical_nap(self):
        data = self.local_data()
        for rel in ['contact.html', 'locations.html']:
            html = read(rel)
            self.assertIn(data['brand_name'], html, rel)
            self.assertIn(data['phone_display'], html, rel)
            self.assertIn(data['email'], html, rel)
            self.assertIn(data['address'], html, rel)
            self.assertIn(f'tel:{data["phone_e164"]}', html, rel)

    def test_verified_hours_are_consistent(self):
        expected = self.local_data()['hours_display']
        for rel in ['contact.html', 'locations.html']:
            self.assertIn(expected, read(rel), rel)

    def test_sitewide_footer_contains_active_location_signals(self):
        for rel in ROOT_PAGES + NESTED_PAGES:
            html = read(rel)
            self.assertIn('+971 2 626 2042', html, rel)
            self.assertIn('Bani Yas Tower', html, rel)
            self.assertIn('W Corniche Road, Abu Dhabi', html, rel)

    def test_locations_and_contact_have_google_map_paths(self):
        for rel in ['locations.html', 'contact.html']:
            html = read(rel)
            self.assertRegex(html, r'google\.com/maps', rel)
            self.assertIn('Bani Yas Tower', html, rel)

    def test_local_metadata_is_natural_and_location_specific(self):
        pages = ROOT_PAGES + NESTED_PAGES
        for rel in pages:
            html = read(rel)
            title = re.search(r'<title>(.*?)</title>', html, re.I | re.S)
            description = re.search(r'<meta name="description" content="([^"]+)"', html, re.I)
            self.assertIsNotNone(title, rel)
            self.assertIsNotNone(description, rel)
            self.assertIn('Abu Dhabi', title.group(1), rel)
            self.assertIn('Abu Dhabi', description.group(1), rel)
            self.assertNotIn('dentist abu dhabi dentist abu dhabi', html.lower(), rel)

    def test_al_raha_remains_non_operational(self):
        html = read('locations.html').lower()
        self.assertIn('coming soon', html)
        self.assertNotRegex(html, r'al raha[^<]{0,160}(open now|now open|current location)')

    def test_unverified_corniche_branch_name_is_not_used_as_nap(self):
        for rel in ROOT_PAGES + NESTED_PAGES:
            self.assertNotIn('Dr Munir Silwadi Dental Centre - Corniche Branch', read(rel), rel)


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: Run Patch 7 tests and verify RED**

```bash
python -m unittest tests.test_patch7_local_seo -v
```

Expected: FAIL because the data source does not exist and Contact/footer/meta/map contracts are not yet fully satisfied.

- [ ] **Step 3: Create `data/local-business.json`**

```json
{
  "verified_on": "2026-08-22",
  "brand_name": "Dr. Munir Silwadi Dental Centre",
  "branch_label": "Bani Yas Tower",
  "phone_display": "+971 2 626 2042",
  "phone_e164": "+97126262042",
  "email": "info@silwadidentalcentres.ae",
  "address": "Al Hilal Bank, Bani Yas Tower, Building 117 C Floor, Sultan Bin Zayed The First St, W Corniche Road, Abu Dhabi, UAE",
  "hours_display": "Sun–Wed 09:00–21:00 · Thu & Sat 09:00–18:00 · Friday closed",
  "hours": {
    "Sunday": "09:00-21:00",
    "Monday": "09:00-21:00",
    "Tuesday": "09:00-21:00",
    "Wednesday": "09:00-21:00",
    "Thursday": "09:00-18:00",
    "Friday": "closed",
    "Saturday": "09:00-18:00"
  },
  "service_area": "Abu Dhabi",
  "maps_query": "Dr Munir Silwadi Dental Centre Bani Yas Tower Abu Dhabi",
  "coming_soon": {
    "name": "Al Raha Mall",
    "address": "F14 & F15, Level 1, Al Raha Mall, Abu Dhabi, UAE",
    "is_open": false
  }
}
```

- [ ] **Step 4: Re-run only the source-of-truth test**

```bash
python -m unittest tests.test_patch7_local_seo.PatchSevenLocalSEOContract.test_local_business_source_of_truth_exists -v
```

Expected: PASS.

- [ ] **Step 5: Commit the RED contract and source data**

```bash
git add tests/test_patch7_local_seo.py data/local-business.json
git commit -m "test: define verified Patch 7 local SEO contracts"
```

---

### Task 2: Normalize authoritative Contact and Locations information

**Files:**
- Modify: `locations.html`
- Modify: `contact.html`
- Modify: `location-pages.css`
- Modify: `contact-pages.css`

**Interfaces:**
- Consumes exact values from `data/local-business.json`.
- Produces identical visible active-clinic NAP on Contact and Locations plus responsive Google Maps access on both.

- [ ] **Step 1: Update `locations.html` metadata**

Use:

```html
<title>Dentist in Abu Dhabi - Bani Yas Tower | Silwadi Dental Center</title>
<meta name="description" content="Visit Dr. Munir Silwadi Dental Centre at Bani Yas Tower on W Corniche Road, Abu Dhabi. View opening hours, phone, directions and the upcoming Al Raha Mall location.">
```

- [ ] **Step 2: Normalize active-location content**

Use the exact business/address representation:

```html
<span class="location-state">Current location</span>
<p class="location-brand">Dr. Munir Silwadi Dental Centre</p>
<h2>Bani Yas Tower</h2>
<address class="location-address">Al Hilal Bank, Bani Yas Tower, Building 117 C Floor, Sultan Bin Zayed The First St, W Corniche Road, Abu Dhabi, UAE</address>
<p class="location-service-area">Serving Abu Dhabi.</p>
```

Keep exact phone, email and `hours_display` values from the JSON file.

- [ ] **Step 3: Use one consistent Google Maps query on Locations**

Directions:

```html
<a class="btn btn--secondary" href="https://www.google.com/maps/search/?api=1&amp;query=Dr%20Munir%20Silwadi%20Dental%20Centre%20Bani%20Yas%20Tower%20Abu%20Dhabi">Get Directions</a>
```

Embed:

```html
<iframe title="Map showing Dr. Munir Silwadi Dental Centre at Bani Yas Tower, Abu Dhabi" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Dr.+Munir+Silwadi+Dental+Centre+Bani+Yas+Tower+Abu+Dhabi&amp;output=embed"></iframe>
```

- [ ] **Step 4: Update `contact.html` metadata and NAP**

Use:

```html
<title>Contact Silwadi Dental Center Abu Dhabi | Bani Yas Tower</title>
<meta name="description" content="Contact Dr. Munir Silwadi Dental Centre at Bani Yas Tower, Abu Dhabi for consultations, appointment enquiries, directions and insurance questions.">
```

The location block must show the same brand, exact address, phone, email and hours as Locations.

- [ ] **Step 5: Add a compact map to Contact**

```html
<div class="contact-map">
  <iframe title="Map showing Dr. Munir Silwadi Dental Centre at Bani Yas Tower, Abu Dhabi" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Dr.+Munir+Silwadi+Dental+Centre+Bani+Yas+Tower+Abu+Dhabi&amp;output=embed"></iframe>
</div>
<p class="contact-map-link"><a href="https://www.google.com/maps/search/?api=1&amp;query=Dr%20Munir%20Silwadi%20Dental%20Centre%20Bani%20Yas%20Tower%20Abu%20Dhabi">Open in Google Maps →</a></p>
```

- [ ] **Step 6: Add focused responsive CSS**

```css
.location-address{font-style:normal;color:var(--body);line-height:1.7}
.location-brand,.location-service-area{color:var(--muted)}
.contact-map{margin-top:22px;overflow:hidden;border:1px solid var(--line);border-radius:18px;background:#edf4f4}
.contact-map iframe{display:block;width:100%;height:260px;border:0}
.contact-map-link{margin:10px 0 0}
.contact-map-link a{color:var(--teal);font-weight:750;text-decoration:none}
```

- [ ] **Step 7: Run focused Contact/Locations tests**

```bash
python -m unittest \
  tests.test_patch7_local_seo.PatchSevenLocalSEOContract.test_contact_and_locations_use_identical_nap \
  tests.test_patch7_local_seo.PatchSevenLocalSEOContract.test_verified_hours_are_consistent \
  tests.test_patch7_local_seo.PatchSevenLocalSEOContract.test_locations_and_contact_have_google_map_paths -v
```

Expected: PASS.

- [ ] **Step 8: Commit authoritative local pages**

```bash
git add locations.html contact.html location-pages.css contact-pages.css
git commit -m "feat: normalize Bani Yas NAP and maps"
```

---

### Task 3: Add natural Abu Dhabi metadata across indexable pages

**Files:**
- Modify: `index.html`
- Modify: `doctors.html`
- Modify: `treatments.html`
- Modify: `about.html`
- Modify: `digital-dentistry.html`
- Modify: `locations.html`
- Modify: `contact.html`
- Modify: `doctors/dr-munir-silwadi.html`
- Modify: `treatments/dental-implants.html`

**Interfaces:**
- Produces unique local-intent `<title>` and meta descriptions without adding Patch 8 canonical/schema values.

- [ ] **Step 1: Use these title targets**

```text
Home: Dentist in Abu Dhabi | Silwadi Dental Center
Doctors: Dentists & Dental Specialists in Abu Dhabi | Silwadi Dental Center
Treatments: Dental Treatments in Abu Dhabi | Silwadi Dental Center
Locations: Dentist in Abu Dhabi - Bani Yas Tower | Silwadi Dental Center
Contact: Contact Silwadi Dental Center Abu Dhabi | Bani Yas Tower
About: About Silwadi Dental Center Abu Dhabi | Since 1980
Digital Dentistry: Digital Dentistry in Abu Dhabi | Silwadi Dental Center
Dr. Munir: Dr. Munir Silwadi | Prosthodontist & Implantologist Abu Dhabi
Dental Implants: Dental Implants in Abu Dhabi | Silwadi Dental Center
```

- [ ] **Step 2: Give each page a distinct short description**

Each description must mention `Abu Dhabi` once and describe the actual page. Examples:

```html
<meta name="description" content="Visit Dr. Munir Silwadi Dental Centre in Abu Dhabi for general and specialist dental care at Bani Yas Tower. Established since 1980.">
```

```html
<meta name="description" content="Find dentists and dental specialists at Silwadi Dental Center in Abu Dhabi across orthodontics, periodontics, endodontics, prosthodontics and general dentistry.">
```

```html
<meta name="description" content="Explore dental implant assessment and treatment planning at Silwadi Dental Center in Abu Dhabi, including restorative and guided planning for selected cases.">
```

- [ ] **Step 3: Keep H1s patient-first**

Do not force location keywords into every H1. `Find a Doctor`, `Our locations`, `Dental Implants` and similar clear headings remain unchanged unless copy quality requires a human edit.

- [ ] **Step 4: Run local metadata tests**

```bash
python -m unittest tests.test_patch7_local_seo.PatchSevenLocalSEOContract.test_local_metadata_is_natural_and_location_specific -v
```

Expected: PASS.

- [ ] **Step 5: Commit metadata changes**

```bash
git add index.html doctors.html treatments.html about.html digital-dentistry.html locations.html contact.html doctors/dr-munir-silwadi.html treatments/dental-implants.html
git commit -m "seo: add natural Abu Dhabi metadata"
```

---

### Task 4: Normalize sitewide footer local identity

**Files:**
- Modify: all nine indexable HTML pages above.
- Modify: `styles.css` only if needed for one reusable address rule.

**Interfaces:**
- Consumes canonical NAP values from `data/local-business.json`.
- Produces consistent business/local contact signals without making the footer visually heavy.

- [ ] **Step 1: Use one compact footer address pattern**

On every page, the Contact footer column should contain:

```html
<address class="footer-address">
  <strong>Dr. Munir Silwadi Dental Centre</strong>
  <span>Al Hilal Bank, Bani Yas Tower, Building 117 C Floor</span>
  <span>Sultan Bin Zayed The First St, W Corniche Road, Abu Dhabi, UAE</span>
  <a href="tel:+97126262042">+971 2 626 2042</a>
  <a href="mailto:info@silwadidentalcentres.ae">info@silwadidentalcentres.ae</a>
</address>
```

- [ ] **Step 2: Keep the header utility strip concise**

`Bani Yas Tower, Abu Dhabi` remains acceptable in the utility strip. Do not duplicate the full address at the top of every page.

- [ ] **Step 3: Add footer CSS if needed**

```css
.footer-address{font-style:normal;display:grid;gap:5px;color:rgba(255,255,255,.72)}
.footer-address strong{color:#fff;font-weight:650}
.footer-address span,.footer-address a{font-size:11px;line-height:1.45}
```

- [ ] **Step 4: Run sitewide footer + Al Raha + unverified-name tests**

```bash
python -m unittest \
  tests.test_patch7_local_seo.PatchSevenLocalSEOContract.test_sitewide_footer_contains_active_location_signals \
  tests.test_patch7_local_seo.PatchSevenLocalSEOContract.test_al_raha_remains_non_operational \
  tests.test_patch7_local_seo.PatchSevenLocalSEOContract.test_unverified_corniche_branch_name_is_not_used_as_nap -v
```

Expected: PASS.

- [ ] **Step 5: Commit sitewide NAP normalization**

```bash
git add index.html doctors.html treatments.html about.html digital-dentistry.html locations.html contact.html doctors/dr-munir-silwadi.html treatments/dental-implants.html styles.css
git commit -m "seo: normalize sitewide clinic NAP"
```

---

### Task 5: Full regression and local smoke verification

**Files:**
- No product changes unless verification exposes a defect.

**Interfaces:**
- Verifies Patch 1–7 behavior together.

- [ ] **Step 1: Run all tests**

```bash
python -m unittest discover -s tests -p 'test*.py' -v
```

Expected: 0 failures.

- [ ] **Step 2: Verify JavaScript syntax**

```bash
node --check app.js
```

Expected: exit 0.

- [ ] **Step 3: Verify internal local links/assets**

Run a Python scan across all HTML for repository-relative `href`, `src` and stylesheet/script references. Expected: no missing local files.

- [ ] **Step 4: Run HTTP smoke tests**

Serve with the existing local dev server and request at minimum:
- `/`
- `/locations.html`
- `/contact.html`
- `/doctors.html`
- `/treatments.html`
- `/about.html`
- `/digital-dentistry.html`
- `/doctors/dr-munir-silwadi.html`
- `/treatments/dental-implants.html`

Expected: HTTP 200 for each.

- [ ] **Step 5: Verify branch diff**

```bash
git diff main...patch-7-local-seo --stat
git log --oneline main..patch-7-local-seo
```

Expected: only Patch 7 plan/data/test/HTML/CSS files; branch remains 0 behind `main`.

- [ ] **Step 6: Integrate using the already-approved workflow**

Fast-forward `main` only after fresh verification, then confirm `main` and `patch-7-local-seo` are identical.
