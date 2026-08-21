# Patch 8 Technical SEO Infrastructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a complete, switchable technical SEO layer for the Silwadi static site using `https://silwadi.ae` as the configured origin.

**Architecture:** Keep the runtime dependency-free and static. Add `data/site-config.json` as the origin source of truth plus `tools/update_site_domain.py` for safe domain changes. Canonical URLs, Open Graph URLs, structured data, `robots.txt`, and `sitemap.xml` are written directly into deployable static files and validated against the config by Python contract tests.

**Tech Stack:** Static HTML5, JSON-LD, XML sitemap, robots.txt, Python standard library tests/helper, existing PowerShell local server.

**Spec:** `docs/superpowers/specs/2026-08-22-silwadi-seo-human-copy-local-growth-design.md`

## Global Constraints

- Primary configured origin is `https://silwadi.ae`.
- A future switch back to `https://silwadidentalcentres.ae` must be a controlled one-command update, not a manual file hunt.
- Canonical URLs and `og:url` values must use fully qualified absolute URLs.
- Home canonical is `https://silwadi.ae/`; static subpages keep their current `.html` paths until hosting proves clean-URL rewrites.
- Use Schema.org `Dentist` for the active practice entity; do not invent `DentalClinic`.
- Use the same Dentist `@id` (`https://silwadi.ae/#dentist`) wherever the practice entity is referenced.
- Use `BreadcrumbList` on non-home pages that expose breadcrumbs/navigation hierarchy.
- Use `Person` schema on Dr. Munir's profile with only currently verified role/specialty/location data.
- Do not add self-serving ratings/review markup.
- Al Raha Mall remains `Coming Soon`; it must not appear as a second operating Dentist entity.
- Do not add unsupported medical claims, awards, accreditations, patient counts, or service guarantees.
- Sitemap includes only indexable current pages and uses absolute canonical URLs.
- `robots.txt` allows normal crawling and points to the configured sitemap.
- Keep important patient-facing content in HTML; structured data is supplemental.

---

## File Structure

**Create**
- `data/site-config.json` — site origin and shared SEO identifiers.
- `tools/update_site_domain.py` — replaces the configured site origin across deployable SEO files and updates config.
- `tests/test_patch8_technical_seo.py` — technical SEO contracts.
- `robots.txt` — crawler access plus sitemap location.
- `sitemap.xml` — canonical URL inventory.

**Modify**
- `index.html`
- `doctors.html`
- `treatments.html`
- `about.html`
- `digital-dentistry.html`
- `locations.html`
- `contact.html`
- `doctors/dr-munir-silwadi.html`
- `treatments/dental-implants.html`

---

### Task 1: Define Patch 8 contracts first

**Files:**
- Create: `tests/test_patch8_technical_seo.py`

**Interfaces:**
- Consumes: all current HTML pages, `data/local-business.json`, future `data/site-config.json`, `robots.txt`, `sitemap.xml`, and `tools/update_site_domain.py`.
- Produces: executable contracts for domain consistency, canonical/OG metadata, JSON-LD, breadcrumbs, sitemap/robots, and domain switching.

- [ ] **Step 1: Write failing tests**

The test module must assert:
- `data/site-config.json` exists and contains `origin=https://silwadi.ae`, `dentist_id=https://silwadi.ae/#dentist`, and `website_id=https://silwadi.ae/#website`.
- Every page has exactly one canonical and exactly one `og:url`, equal to its configured absolute URL.
- Every page has one title, one meta description, and no canonical points at the old domain.
- Home contains JSON-LD `WebSite` plus a `Dentist` entity with phone/address/hours from `data/local-business.json` and no `aggregateRating` / `review` fields.
- `locations.html` and `contact.html` reference the same Dentist `@id` and never create an operating Al Raha Dentist entity.
- All non-home pages contain a valid `BreadcrumbList`; nested pages have three breadcrumb items.
- Dr. Munir profile includes a `Person` entity with name, jobTitle, image, URL, worksFor `@id`, and no unverified founder property.
- `robots.txt` contains `User-agent: *`, `Allow: /`, and `Sitemap: https://silwadi.ae/sitemap.xml`.
- `sitemap.xml` contains exactly the nine current canonical pages, all under `https://silwadi.ae` and no old-domain URLs.
- `tools/update_site_domain.py` can be copied into a temporary project fixture, switch `https://silwadi.ae` to `https://silwadidentalcentres.ae`, and update config/html/sitemap/robots while leaving the email domain untouched.

- [ ] **Step 2: Run and verify RED**

```bash
python -m unittest tests.test_patch8_technical_seo -v
```

Expected: FAIL because site config, canonicals, schema, sitemap, robots, and domain helper do not exist yet.

- [ ] **Step 3: Commit failing tests**

```bash
git add tests/test_patch8_technical_seo.py
git commit -m "test: define Patch 8 technical SEO contracts"
```

---

### Task 2: Add switchable site origin configuration

**Files:**
- Create: `data/site-config.json`
- Create: `tools/update_site_domain.py`

**Interfaces:**
- Consumes: current configured origin.
- Produces: one-command origin replacement across HTML, `sitemap.xml`, and `robots.txt`.

- [ ] **Step 1: Create config**

```json
{
  "origin": "https://silwadi.ae",
  "site_name": "Silwadi Dental Center",
  "dentist_id": "https://silwadi.ae/#dentist",
  "website_id": "https://silwadi.ae/#website",
  "default_social_image": "https://silwadi.ae/assets/silwadi-logo-original.jpeg"
}
```

- [ ] **Step 2: Implement domain switch helper**

`tools/update_site_domain.py` must:
- accept exactly one `https://...` origin argument without trailing slash;
- read the existing origin from `data/site-config.json`;
- replace only that exact old origin in `*.html`, `sitemap.xml`, and `robots.txt`;
- update `origin`, `dentist_id`, `website_id`, and `default_social_image` in the config;
- never alter `info@silwadidentalcentres.ae`.

- [ ] **Step 3: Run the domain-switch test and verify GREEN**

```bash
python -m unittest tests.test_patch8_technical_seo.PatchEightTechnicalSEOContract.test_domain_switch_helper_updates_site_origin_only -v
```

Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add data/site-config.json tools/update_site_domain.py
git commit -m "feat: add switchable site domain configuration"
```

---

### Task 3: Add canonical and social URL metadata

**Files:**
- Modify all nine HTML pages.

**Interfaces:**
- Consumes: `data/site-config.json` origin.
- Produces: canonical and `og:url` for each page; `og:image` using the configured default social image.

- [ ] **Step 1: Add canonical URLs**

Canonical map:
- `index.html` → `https://silwadi.ae/`
- `doctors.html` → `https://silwadi.ae/doctors.html`
- `treatments.html` → `https://silwadi.ae/treatments.html`
- `about.html` → `https://silwadi.ae/about.html`
- `digital-dentistry.html` → `https://silwadi.ae/digital-dentistry.html`
- `locations.html` → `https://silwadi.ae/locations.html`
- `contact.html` → `https://silwadi.ae/contact.html`
- `doctors/dr-munir-silwadi.html` → `https://silwadi.ae/doctors/dr-munir-silwadi.html`
- `treatments/dental-implants.html` → `https://silwadi.ae/treatments/dental-implants.html`

Each `<head>` gets:

```html
<link rel="canonical" href="ABSOLUTE_URL">
<meta property="og:url" content="ABSOLUTE_URL">
<meta property="og:image" content="https://silwadi.ae/assets/silwadi-logo-original.jpeg">
```

Preserve existing human-readable titles/descriptions unless a duplicate/missing field is discovered.

- [ ] **Step 2: Run metadata contracts**

```bash
python -m unittest tests.test_patch8_technical_seo.PatchEightTechnicalSEOContract.test_all_pages_have_configured_canonical_and_og_urls -v
```

Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add index.html doctors.html treatments.html about.html digital-dentistry.html locations.html contact.html doctors/dr-munir-silwadi.html treatments/dental-implants.html
git commit -m "feat: add canonical and social URL metadata"
```

---

### Task 4: Add restrained structured data

**Files:**
- Modify: `index.html`
- Modify: `locations.html`
- Modify: `contact.html`
- Modify: all non-home pages for BreadcrumbList
- Modify: `doctors/dr-munir-silwadi.html`

**Interfaces:**
- Consumes: `data/local-business.json` and site IDs from `data/site-config.json`.
- Produces: JSON-LD graphs using stable `@id` references.

- [ ] **Step 1: Home graph**

Add a single JSON-LD script containing:
- `WebSite` with `@id=https://silwadi.ae/#website`, `url`, and name.
- `Dentist` with `@id=https://silwadi.ae/#dentist`, name, URL, telephone, email, image, `medicalSpecialty=https://schema.org/Dentistry`, PostalAddress, openingHoursSpecification for all open days, and `areaServed=Abu Dhabi`.

Do not add ratings/reviews.

- [ ] **Step 2: Location and Contact practice entity**

Add a Dentist JSON-LD entity using the same `@id` and same verified NAP/hours. Al Raha may be mentioned only as visible `Coming Soon` HTML, not as another active LocalBusiness/Dentist node.

- [ ] **Step 3: BreadcrumbList on non-home pages**

Root pages: Home → current page.
Nested pages: Home → parent directory → current page.
Use absolute `https://silwadi.ae/...` item URLs.

- [ ] **Step 4: Dr. Munir Person schema**

On `doctors/dr-munir-silwadi.html`, add a `Person` entity:
- `@id=https://silwadi.ae/doctors/dr-munir-silwadi.html#person`
- `name=Dr. Munir Silwadi`
- `jobTitle=Specialist Prosthodontist & Implantologist`
- `url=https://silwadi.ae/doctors/dr-munir-silwadi.html`
- `image=https://silwadi.ae/assets/doctors/dr-munir-silwadi.png`
- `worksFor={"@id":"https://silwadi.ae/#dentist"}`

Do not add founderOf/founder unless separately verified.

- [ ] **Step 5: Run schema contracts**

```bash
python -m unittest \
  tests.test_patch8_technical_seo.PatchEightTechnicalSEOContract.test_home_has_dentist_and_website_schema_without_review_markup \
  tests.test_patch8_technical_seo.PatchEightTechnicalSEOContract.test_non_home_pages_have_breadcrumb_schema \
  tests.test_patch8_technical_seo.PatchEightTechnicalSEOContract.test_munir_profile_has_person_schema -v
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add index.html doctors.html treatments.html about.html digital-dentistry.html locations.html contact.html doctors/dr-munir-silwadi.html treatments/dental-implants.html
git commit -m "feat: add dental practice and breadcrumb structured data"
```

---

### Task 5: Add robots and sitemap

**Files:**
- Create: `robots.txt`
- Create: `sitemap.xml`

**Interfaces:**
- Consumes: canonical page map.
- Produces: crawl instructions and canonical discovery list.

- [ ] **Step 1: Create robots**

```txt
User-agent: *
Allow: /

Sitemap: https://silwadi.ae/sitemap.xml
```

- [ ] **Step 2: Create sitemap**

Use XML sitemap protocol with exactly these nine `<loc>` entries:

```text
https://silwadi.ae/
https://silwadi.ae/doctors.html
https://silwadi.ae/treatments.html
https://silwadi.ae/about.html
https://silwadi.ae/digital-dentistry.html
https://silwadi.ae/locations.html
https://silwadi.ae/contact.html
https://silwadi.ae/doctors/dr-munir-silwadi.html
https://silwadi.ae/treatments/dental-implants.html
```

Do not add speculative `lastmod`, priority, or changefreq values.

- [ ] **Step 3: Run crawl-file contracts**

```bash
python -m unittest \
  tests.test_patch8_technical_seo.PatchEightTechnicalSEOContract.test_robots_points_to_configured_sitemap \
  tests.test_patch8_technical_seo.PatchEightTechnicalSEOContract.test_sitemap_contains_exact_current_canonicals -v
```

Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add robots.txt sitemap.xml
git commit -m "feat: add robots and canonical sitemap"
```

---

### Task 6: Full verification and integration

- [ ] **Step 1: Full tests**

```bash
python -m unittest discover -s tests -p "*.py" -v
```

Expected: all Patch 1–8 tests pass.

- [ ] **Step 2: Syntax/data checks**

```bash
node --check app.js
python -m json.tool data/local-business.json >/dev/null
python -m json.tool data/site-config.json >/dev/null
python tools/update_site_domain.py --help
```

- [ ] **Step 3: Internal link/asset and JSON-LD parse check**

Use a Python standard-library validation script to parse local HTML links/assets and every `application/ld+json` block. Expected: zero broken local references and zero JSON parse errors.

- [ ] **Step 4: HTTP smoke test**

Serve the site locally and confirm HTTP 200 for the nine canonical HTML pages, `/robots.txt`, and `/sitemap.xml`.

- [ ] **Step 5: Compare branch to main**

Expected before integration: branch ahead, behind 0, changed files limited to Patch 8 plan/tests/config/helper/HTML/robots/sitemap.

- [ ] **Step 6: Fast-forward main only after verification**

Then compare `main` and feature branch again; expected `identical`, ahead 0, behind 0.
