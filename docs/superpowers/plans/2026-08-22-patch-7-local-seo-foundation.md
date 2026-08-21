# Patch 7 Local SEO Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Normalize verified local business information across the site, strengthen Abu Dhabi / Corniche Branch relevance without keyword stuffing, and give Patch 8 a reliable local-business data source for structured data.

**Architecture:** Keep the current static HTML/CSS/JS site. Add a small JSON source of truth at `data/local-business.json` containing verified business identity, phone, address, hours, service area and coming-soon branch status. Important NAP remains visible directly in HTML; tests compare the HTML against the source-of-truth data so local information cannot silently drift.

**Tech Stack:** Static HTML5, CSS3, vanilla JavaScript, JSON, Python `unittest`, existing PowerShell local server.

**Spec:** `docs/superpowers/specs/2026-08-22-silwadi-seo-human-copy-local-growth-design.md`

## Global Constraints

- Main brand remains `Dr. Munir Silwadi Dental Centre`.
- Location-specific branch identity may use the current public listing name `Dr Munir Silwadi Dental Centre - Corniche Branch`.
- Active branch phone: `+971 2 626 2042` / `+97126262042`.
- Active branch email: `info@silwadidentalcentres.ae`.
- Canonical on-site address: `Al Hilal Bank, Bani Yas Tower, Building 117, C Floor, Sultan Bin Zayed The First St, W Corniche Road, Abu Dhabi, United Arab Emirates.`
- Verified hours: Sunday–Wednesday `09:00–21:00`; Thursday `09:00–18:00`; Friday closed; Saturday `09:00–18:00`.
- Local service area wording stays broad: `Abu Dhabi`; do not invent a radius or list unsupported neighborhoods.
- Al Raha Mall remains `Coming Soon` and must not be represented as an operating branch.
- Do not add schema, canonicals, sitemap or robots files in Patch 7; those are Patch 8.
- Do not add rating/review markup.
- Do not turn body copy into repetitive `dentist Abu Dhabi` keyword text.
- Important NAP and location copy remains in HTML, not injected from JavaScript.

---

## File Structure

**Create**
- `data/local-business.json` — verified local-business source of truth consumed by tests now and structured-data work in Patch 8.
- `tests/test_patch7_local_seo.py` — dedicated local SEO/NAP contracts.

**Modify**
- `index.html` — stronger natural Abu Dhabi metadata and compact location signals.
- `locations.html` — normalized branch name/address/hours, exact directions query, service-area statement.
- `contact.html` — normalized NAP, concise map block, branch link.
- `location-pages.css` — local details/map refinement if required.
- `contact-pages.css` — responsive contact-map rules.
- `doctors.html`
- `treatments.html`
- `about.html`
- `digital-dentistry.html`
- `doctors/dr-munir-silwadi.html`
- `treatments/dental-implants.html` — normalize sitewide footer NAP and location links.

**Unchanged in this patch**
- `app.js`
- canonical tags
- JSON-LD/schema
- `robots.txt`
- `sitemap.xml`

---

### Task 1: Define local-business source-of-truth contracts

**Files:**
- Create: `tests/test_patch7_local_seo.py`

**Interfaces:**
- Consumes: repository HTML files and future `data/local-business.json`.
- Produces: `PatchSevenLocalSEOContract` ensuring source data, visible NAP, branch state, metadata and map consistency.

- [ ] **Step 1: Write the failing contract test**

Create `tests/test_patch7_local_seo.py` with:

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
        self.assertEqual(data['gbp_location_name'], 'Dr Munir Silwadi Dental Centre - Corniche Branch')
        self.assertEqual(data['phone_e164'], '+97126262042')
        self.assertEqual(data['service_area'], 'Abu Dhabi')
        self.assertFalse(data['coming_soon']['is_open'])

    def test_contact_and_locations_use_identical_nap(self):
        data = self.local_data()
        for rel in ['contact.html', 'locations.html']:
            html = read(rel)
            self.assertIn(data['phone_display'], html, rel)
            self.assertIn(data['email'], html, rel)
            self.assertIn(data['address'], html, rel)
            self.assertIn(data['gbp_location_name'], html, rel)

    def test_verified_hours_are_consistent(self):
        data = self.local_data()
        expected = data['hours_display']
        for rel in ['contact.html', 'locations.html']:
            self.assertIn(expected, read(rel), rel)

    def test_sitewide_footer_contains_local_contact_signals(self):
        for rel in ROOT_PAGES:
            html = read(rel)
            self.assertIn('+971 2 626 2042', html, rel)
            self.assertIn('W Corniche Road, Abu Dhabi', html, rel)
        for rel in NESTED_PAGES:
            html = read(rel)
            self.assertIn('+971 2 626 2042', html, rel)
            self.assertIn('W Corniche Road, Abu Dhabi', html, rel)

    def test_locations_and_contact_have_google_map_paths(self):
        for rel in ['locations.html', 'contact.html']:
            html = read(rel)
            self.assertRegex(html, r'google\.com/maps', rel)
            self.assertIn('Corniche', html, rel)

    def test_local_metadata_is_natural_and_location_specific(self):
        home = read('index.html')
        locations = read('locations.html')
        contact = read('contact.html')
        self.assertIn('<title>Dentist in Abu Dhabi | Silwadi Dental Center Since 1980</title>', home)
        self.assertIn('<title>Dental Clinic in Abu Dhabi | Silwadi Dental Center Locations</title>', locations)
        self.assertIn('<title>Contact Silwadi Dental Center Abu Dhabi | Bani Yas Tower</title>', contact)
        self.assertLessEqual(home.lower().count('dentist in abu dhabi'), 1)

    def test_al_raha_remains_non_operational(self):
        html = read('locations.html').lower()
        self.assertIn('coming soon', html)
        self.assertNotRegex(html, r'al raha[^<]{0,160}(open now|now open|current location)')


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: Run the Patch 7 test and verify RED**

Run:

```bash
python -m unittest tests.test_patch7_local_seo -v
```

Expected: FAIL because `data/local-business.json` does not exist and contact/location metadata/NAP are not yet normalized.

- [ ] **Step 3: Commit the failing test**

```bash
git add tests/test_patch7_local_seo.py
git commit -m "test: define Patch 7 local SEO contracts"
```

---

### Task 2: Add verified local-business source of truth

**Files:**
- Create: `data/local-business.json`
- Test: `tests/test_patch7_local_seo.py`

**Interfaces:**
- Consumes: verified current public website and Google business listing data checked on 2026-08-22.
- Produces: stable JSON keys used by Patch 7 tests and Patch 8 schema generation.

- [ ] **Step 1: Create `data/local-business.json`**

```json
{
  "verified_on": "2026-08-22",
  "brand_name": "Dr. Munir Silwadi Dental Centre",
  "gbp_location_name": "Dr Munir Silwadi Dental Centre - Corniche Branch",
  "branch_label": "Bani Yas Tower",
  "phone_display": "+971 2 626 2042",
  "phone_e164": "+97126262042",
  "email": "info@silwadidentalcentres.ae",
  "address": "Al Hilal Bank, Bani Yas Tower, Building 117, C Floor, Sultan Bin Zayed The First St, W Corniche Road, Abu Dhabi, United Arab Emirates.",
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
  "maps_query": "Dr Munir Silwadi Dental Centre Corniche Branch Bani Yas Tower Abu Dhabi",
  "coming_soon": {
    "name": "Al Raha Mall",
    "address": "F14 & F15, Level 1, Al Raha Mall, Abu Dhabi, United Arab Emirates.",
    "is_open": false
  }
}
```

- [ ] **Step 2: Run only the source-of-truth test**

```bash
python -m unittest tests.test_patch7_local_seo.PatchSevenLocalSEOContract.test_local_business_source_of_truth_exists -v
```

Expected: PASS.

- [ ] **Step 3: Commit the data file**

```bash
git add data/local-business.json
git commit -m "feat: add verified local business source data"
```

---

### Task 3: Normalize Contact and Locations NAP + maps

**Files:**
- Modify: `locations.html`
- Modify: `contact.html`
- Modify: `location-pages.css`
- Modify: `contact-pages.css`

**Interfaces:**
- Consumes: exact values from `data/local-business.json`.
- Produces: visible, identical active-branch NAP on Contact and Locations and responsive Google Map access on both pages.

- [ ] **Step 1: Update `locations.html` metadata and branch identity**

Use:

```html
<title>Dental Clinic in Abu Dhabi | Silwadi Dental Center Locations</title>
<meta name="description" content="Visit Dr. Munir Silwadi Dental Centre at Bani Yas Tower on W Corniche Road, Abu Dhabi. View hours, phone, directions and the upcoming Al Raha Mall branch.">
```

In the active branch section show:

```html
<span class="location-state">Current location</span>
<p class="location-branch-id">Dr Munir Silwadi Dental Centre - Corniche Branch</p>
<h2>Bani Yas Tower</h2>
<p>Al Hilal Bank, Bani Yas Tower, Building 117, C Floor, Sultan Bin Zayed The First St, W Corniche Road, Abu Dhabi, United Arab Emirates.</p>
<p class="location-service-area">Serving patients across Abu Dhabi.</p>
```

Keep phone/email/hours exactly aligned with `data/local-business.json`.

- [ ] **Step 2: Use one map query on Locations**

Directions link:

```html
<a class="btn btn--secondary" href="https://www.google.com/maps/search/?api=1&amp;query=Dr%20Munir%20Silwadi%20Dental%20Centre%20Corniche%20Branch%20Bani%20Yas%20Tower%20Abu%20Dhabi">Get Directions</a>
```

Embed:

```html
<iframe title="Map showing Dr Munir Silwadi Dental Centre - Corniche Branch at Bani Yas Tower, Abu Dhabi" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Dr+Munir+Silwadi+Dental+Centre+Corniche+Branch+Bani+Yas+Tower+Abu+Dhabi&amp;output=embed"></iframe>
```

- [ ] **Step 3: Update `contact.html` metadata and NAP**

Use:

```html
<title>Contact Silwadi Dental Center Abu Dhabi | Bani Yas Tower</title>
<meta name="description" content="Contact Dr. Munir Silwadi Dental Centre at Bani Yas Tower, Abu Dhabi for consultations, appointment enquiries, directions and insurance questions.">
```

Change the location panel to include the exact branch identity and canonical address:

```html
<p class="eyebrow">Corniche Branch · Bani Yas Tower</p>
<h2>Dr. Munir Silwadi Dental Centre</h2>
<p class="local-branch-name">Dr Munir Silwadi Dental Centre - Corniche Branch</p>
```

Then display the exact address, phone, email and `hours_display` from the JSON file.

- [ ] **Step 4: Add a compact responsive map to Contact**

Under the contact detail list add:

```html
<div class="contact-map">
  <iframe title="Map showing Dr Munir Silwadi Dental Centre - Corniche Branch in Abu Dhabi" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Dr+Munir+Silwadi+Dental+Centre+Corniche+Branch+Bani+Yas+Tower+Abu+Dhabi&amp;output=embed"></iframe>
</div>
<p class="contact-map-link"><a href="https://www.google.com/maps/search/?api=1&amp;query=Dr%20Munir%20Silwadi%20Dental%20Centre%20Corniche%20Branch%20Bani%20Yas%20Tower%20Abu%20Dhabi">Open in Google Maps →</a></p>
```

- [ ] **Step 5: Add compact map CSS**

Append to `contact-pages.css`:

```css
.contact-map{margin-top:22px;overflow:hidden;border:1px solid var(--line);border-radius:18px;background:#edf4f4}
.contact-map iframe{display:block;width:100%;height:260px;border:0}
.contact-map-link{margin:10px 0 0}
.contact-map-link a{color:var(--teal);font-weight:750;text-decoration:none}
.local-branch-name,.location-branch-id,.location-service-area{color:var(--muted)}
```

- [ ] **Step 6: Run focused NAP/map tests**

```bash
python -m unittest \
  tests.test_patch7_local_seo.PatchSevenLocalSEOContract.test_contact_and_locations_use_identical_nap \
  tests.test_patch7_local_seo.PatchSevenLocalSEOContract.test_verified_hours_are_consistent \
  tests.test_patch7_local_seo.PatchSevenLocalSEOContract.test_locations_and_contact_have_google_map_paths -v
```

Expected: PASS.

- [ ] **Step 7: Commit Contact/Locations changes**

```bash
git add locations.html contact.html location-pages.css contact-pages.css
git commit -m "feat: normalize Abu Dhabi branch NAP and maps"
```

---

### Task 4: Add natural local metadata and sitewide footer location signals

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
- Consumes: canonical active branch details from `data/local-business.json`.
- Produces: consistent sitewide local contact signals without adding schema or keyword-heavy body sections.

- [ ] **Step 1: Update Home metadata**

Use:

```html
<title>Dentist in Abu Dhabi | Silwadi Dental Center Since 1980</title>
<meta name="description" content="Dr. Munir Silwadi Dental Centre provides general and specialist dental care in Abu Dhabi. Established since 1980 at Bani Yas Tower on W Corniche Road.">
```

Do not add another exact-match `Dentist in Abu Dhabi` phrase to body copy.

- [ ] **Step 2: Standardize footer contact block on root pages**

Use this visible footer contact pattern on every root page:

```html
<div>
  <h3>Contact</h3>
  <a href="tel:+97126262042">+971 2 626 2042</a>
  <a href="mailto:info@silwadidentalcentres.ae">info@silwadidentalcentres.ae</a>
  <address>Bani Yas Tower, Building 117, C Floor<br>Sultan Bin Zayed The First St, W Corniche Road, Abu Dhabi</address>
</div>
```

- [ ] **Step 3: Standardize nested-page footer contact block**

Use the same visible address/phone/email copy in `doctors/dr-munir-silwadi.html` and `treatments/dental-implants.html`. Relative links are not needed for tel/mailto/address text.

- [ ] **Step 4: Add one concise local cue to core page intros where natural**

Keep copy minimal. Allowed examples:

```html
<!-- Doctors -->
<p class="page-hero__lead">Search our Abu Dhabi dental team by name or specialty.</p>

<!-- Treatments -->
<p class="treatment-hero__lead">Explore dental care available through our Abu Dhabi team, or contact us if you are not sure where to start.</p>
```

About and Digital Dentistry already mention Abu Dhabi and do not need additional repeated location phrases.

- [ ] **Step 5: Run metadata/footer tests**

```bash
python -m unittest \
  tests.test_patch7_local_seo.PatchSevenLocalSEOContract.test_sitewide_footer_contains_local_contact_signals \
  tests.test_patch7_local_seo.PatchSevenLocalSEOContract.test_local_metadata_is_natural_and_location_specific -v
```

Expected: PASS.

- [ ] **Step 6: Commit sitewide local signals**

```bash
git add index.html doctors.html treatments.html about.html digital-dentistry.html locations.html contact.html doctors/dr-munir-silwadi.html treatments/dental-implants.html
git commit -m "feat: strengthen consistent Abu Dhabi local signals"
```

---

### Task 5: Full Patch 7 verification

**Files:**
- Test only.

**Interfaces:**
- Consumes: complete Patch 7 branch.
- Produces: evidence that local SEO changes preserve all previous site contracts.

- [ ] **Step 1: Run Patch 7 tests**

```bash
python -m unittest tests.test_patch7_local_seo -v
```

Expected: all Patch 7 tests PASS.

- [ ] **Step 2: Run full regression suite**

```bash
python -m unittest discover -s tests -p 'test*.py' -v
```

Expected: 0 failures / 0 errors.

- [ ] **Step 3: Check JavaScript syntax**

```bash
node --check app.js
```

Expected: exit code 0.

- [ ] **Step 4: Check local links and assets**

Run the existing repository link/asset checker used in previous patches, or equivalent Python validation over all `.html` files, skipping `http:`, `https:`, `mailto:`, `tel:` and fragment-only links.

Expected: no missing local files.

- [ ] **Step 5: HTTP smoke-test major routes**

Serve the branch with the existing PowerShell dev server and verify HTTP 200 for:

```text
/
/index.html
/locations.html
/contact.html
/doctors.html
/treatments.html
/about.html
/digital-dentistry.html
/doctors/dr-munir-silwadi.html
/treatments/dental-implants.html
/data/local-business.json
```

- [ ] **Step 6: Compare branch with `main`**

Expected before integration: Patch 7 branch is ahead of `main`, behind by 0, with only files listed in this plan changed.

- [ ] **Step 7: Integrate using the established project workflow**

Fast-forward `main` only after fresh verification and confirm `main` and the Patch 7 branch are identical.
