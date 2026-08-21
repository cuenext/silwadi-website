# Patch 9 High-Intent Treatment SEO Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a focused treatment SEO cluster for five high-intent Abu Dhabi dental searches while keeping the copy concise, clinical, human and conversion-oriented.

**Architecture:** Keep the existing static HTML architecture and shared `treatment-pages.css`. Refine the existing implant page and add four new treatment detail pages under `/treatments/`. Each page receives unique local metadata, canonical/OG URLs, BreadcrumbList + Service JSON-LD, direct consultation/call paths, a relevant clinician/team route, and a compact FAQ. The treatment directory, homepage pathways and sitemap are updated to surface the new pages.

**Tech Stack:** Static HTML5, existing CSS system, vanilla JavaScript, JSON-LD, XML sitemap, Python `unittest` contract tests.

**Spec:** `docs/superpowers/specs/2026-08-22-silwadi-seo-human-copy-local-growth-design.md`

## Global Constraints

- Primary origin remains `https://silwadi.ae` and must continue to work with `tools/update_site_domain.py`.
- No framework or build step.
- Patient-visible copy must be concise and natural; no keyword stuffing or repetitive location phrases.
- No “best”, “world-class”, “cutting-edge”, “state-of-the-art”, guaranteed outcomes, pain-free guarantees, or unsupported superiority claims.
- Medical language must remain conditional where suitability/outcome varies.
- No ratings/review schema.
- Al Raha Mall remains Coming Soon and must not be represented as an operating provider.
- Keep one H1 per page and one canonical URL per page.
- Consultation routes must remain functional; use the existing contact/consultation destination where available.
- New pages must reuse the verified Bani Yas NAP from `data/local-business.json`.

---

### Task 1: Define Patch 9 treatment SEO contracts

**Files:**
- Create: `tests/test_patch9_treatment_seo.py`

**Interfaces:**
- Consumes: `data/site-config.json`, `data/local-business.json`, existing treatment page patterns.
- Produces: contract for five search-intent treatment pages and sitemap/internal-link integration.

- [ ] **Step 1: Write failing tests**

Create tests that assert:

```python
PRIMARY_PAGES = {
    'treatments/dental-implants.html': ('Dental Implants in Abu Dhabi', 'dental implants'),
    'treatments/orthodontics.html': ('Orthodontist & Braces in Abu Dhabi', 'orthodontics'),
    'treatments/cosmetic-dentistry.html': ('Cosmetic Dentistry in Abu Dhabi', 'cosmetic dentistry'),
    'treatments/general-dentistry.html': ('General Dentist in Abu Dhabi', 'general dentistry'),
    'treatments/emergency-dentist.html': ('Emergency Dentist in Abu Dhabi', 'emergency dental care'),
}
```

For each page assert:
- file exists
- exactly one H1
- title includes the intended search concept and `Abu Dhabi`
- non-empty unique meta description
- canonical and `og:url` equal `https://silwadi.ae/<path>`
- breadcrumb JSON-LD has Home → Treatments → current treatment
- exactly one `Service` JSON-LD node with `provider.@id == https://silwadi.ae/#dentist` and `areaServed.name == Abu Dhabi`
- no `aggregateRating`, `review`, `best`, `world-class`, `cutting-edge`, `state-of-the-art`, `guaranteed`, or `pain-free`
- a visible Bani Yas/Abu Dhabi local cue
- a call CTA and a consultation CTA
- FAQ count is 2–4, not a giant content wall

Also assert:
- orthodontics page mentions braces and clear aligners; Invisalign may appear only as an option, never a guaranteed product path
- emergency page tells patients with severe swelling, breathing difficulty, uncontrolled bleeding or significant trauma to seek urgent/emergency medical care rather than wait for routine dental contact
- the implant page links to Dr. Munir
- the treatment directory links all five primary pages
- homepage links implants, orthodontics, cosmetic and general cards to their dedicated pages
- sitemap contains all five primary treatment canonicals exactly once

- [ ] **Step 2: Run the Patch 9 test and verify RED**

Run:

```bash
python -m unittest tests/test_patch9_treatment_seo.py -v
```

Expected: FAIL because four treatment pages do not exist and directory/home/sitemap are not fully linked.

- [ ] **Step 3: Commit the RED contract**

```bash
git add tests/test_patch9_treatment_seo.py
git commit -m "test: define Patch 9 treatment SEO contracts"
```

---

### Task 2: Refine Dental Implants as the first high-intent template

**Files:**
- Modify: `treatments/dental-implants.html`

**Interfaces:**
- Consumes: existing implant content, `https://silwadi.ae/#dentist`, Dr. Munir profile.
- Produces: reference structure for the remaining four treatment pages.

- [ ] **Step 1: Run the implant-specific contract and confirm failure**

Expected failures should identify the H1/Service schema/consultation-routing gaps.

- [ ] **Step 2: Implement the refined implant page**

Required metadata:

```html
<title>Dental Implants in Abu Dhabi | Silwadi Dental Center</title>
<meta name="description" content="Considering dental implants in Abu Dhabi? Learn how implant assessment, digital planning and restorative care are approached at Silwadi Dental Center.">
<link rel="canonical" href="https://silwadi.ae/treatments/dental-implants.html">
```

H1:

```html
<h1>Dental Implants in Abu Dhabi</h1>
```

Keep sections concise:
1. What implants can replace
2. Who needs assessment first
3. The treatment-planning sequence
4. Digital/guided planning where appropriate
5. Dr. Munir profile route
6. 3 FAQs
7. consultation/call CTA

Add a `Service` schema node:

```json
{
  "@type": "Service",
  "@id": "https://silwadi.ae/treatments/dental-implants.html#service",
  "name": "Dental Implants",
  "serviceType": "Dental implant assessment and restorative care",
  "url": "https://silwadi.ae/treatments/dental-implants.html",
  "provider": {"@id": "https://silwadi.ae/#dentist"},
  "areaServed": {"@type": "City", "name": "Abu Dhabi"}
}
```

- [ ] **Step 3: Run implant contract and verify GREEN**

- [ ] **Step 4: Commit**

```bash
git add treatments/dental-implants.html
git commit -m "feat: refine dental implants search landing page"
```

---

### Task 3: Add Orthodontics / Braces landing page

**Files:**
- Create: `treatments/orthodontics.html`

**Interfaces:**
- Consumes: existing treatment template; verified orthodontic roster: Dr. Hani Hasbini, Dr. Moammar Rifai, Dr. Krishnamurthy Katta Balajee.
- Produces: orthodontics search landing page.

- [ ] **Step 1: Confirm orthodontics test is RED**

- [ ] **Step 2: Create the page**

Metadata:

```html
<title>Orthodontist & Braces in Abu Dhabi | Silwadi Dental Center</title>
<meta name="description" content="Orthodontic care in Abu Dhabi for children, teens and adults, including braces and clear aligners after specialist assessment at Silwadi Dental Center.">
```

H1:

```html
<h1>Orthodontics in Abu Dhabi</h1>
```

Content structure:
- what orthodontic treatment addresses: alignment and bite
- assessment before choosing an appliance
- options may include fixed braces, clear aligners and retainers where appropriate
- mention Invisalign only as one clear-aligner option offered by the orthodontic team, not as a promise for every patient
- compact “Our orthodontic team” section naming the three verified orthodontic clinicians and linking to `../doctors.html`
- 3 FAQs
- consultation + call CTA

Add `Service` schema with `serviceType: "Orthodontic assessment, braces and clear aligner care"`.

- [ ] **Step 3: Run contract and verify GREEN**

- [ ] **Step 4: Commit**

```bash
git add treatments/orthodontics.html
git commit -m "feat: add orthodontics Abu Dhabi landing page"
```

---

### Task 4: Add Cosmetic Dentistry landing page

**Files:**
- Create: `treatments/cosmetic-dentistry.html`

**Interfaces:**
- Consumes: Dr. Munir profile and current cosmetic/restorative treatment language.
- Produces: cosmetic dentistry search landing page.

- [ ] **Step 1: Confirm cosmetic page test is RED**

- [ ] **Step 2: Create the page**

Metadata:

```html
<title>Cosmetic Dentistry in Abu Dhabi | Silwadi Dental Center</title>
<meta name="description" content="Explore cosmetic dentistry in Abu Dhabi, including veneers, whitening and restorative smile planning after a clinical assessment at Silwadi Dental Center.">
```

H1:

```html
<h1>Cosmetic Dentistry in Abu Dhabi</h1>
```

Content structure:
- start with oral health and assessment, not aesthetics alone
- possible options: veneers, whitening, crowns/restorative work, digital smile planning
- explain that the right option depends on tooth condition, bite and goals
- link Dr. Munir for prosthodontic/aesthetic restorative care and the full doctor directory for other clinicians
- 3 FAQs
- consultation + call CTA

Service schema `serviceType: "Cosmetic and aesthetic restorative dentistry"`.

- [ ] **Step 3: Verify GREEN and commit**

```bash
git add treatments/cosmetic-dentistry.html
git commit -m "feat: add cosmetic dentistry Abu Dhabi landing page"
```

---

### Task 5: Add General Dentistry landing page

**Files:**
- Create: `treatments/general-dentistry.html`

**Interfaces:**
- Consumes: general-dentist roster from `doctors.html`.
- Produces: general dentistry search landing page.

- [ ] **Step 1: Confirm RED**

- [ ] **Step 2: Create the page**

Metadata:

```html
<title>General Dentist in Abu Dhabi | Silwadi Dental Center</title>
<meta name="description" content="General dental care in Abu Dhabi for examinations, fillings, preventive care and routine dental concerns at Silwadi Dental Center, Bani Yas Tower.">
```

H1:

```html
<h1>General Dentistry in Abu Dhabi</h1>
```

Content structure:
- routine examinations and diagnosis
- fillings/restorative care where indicated
- preventive/hygiene support
- when a specialist referral may be needed
- link to doctor directory
- 3 FAQs
- consultation + call CTA

Service schema `serviceType: "General and preventive dental care"`.

- [ ] **Step 3: Verify GREEN and commit**

```bash
git add treatments/general-dentistry.html
git commit -m "feat: add general dentistry Abu Dhabi landing page"
```

---

### Task 6: Add Emergency Dental Care landing page

**Files:**
- Create: `treatments/emergency-dentist.html`

**Interfaces:**
- Consumes: verified public claim that the centre provides emergency dental services; active centre phone from `data/local-business.json`.
- Produces: urgent-intent dental landing page without unsafe triage promises.

- [ ] **Step 1: Confirm RED**

- [ ] **Step 2: Create the page**

Metadata:

```html
<title>Emergency Dentist in Abu Dhabi | Silwadi Dental Center</title>
<meta name="description" content="Need urgent dental care in Abu Dhabi? Call Silwadi Dental Center for appointment availability and assessment of dental pain, broken teeth and other urgent dental concerns.">
```

H1:

```html
<h1>Emergency Dentist in Abu Dhabi</h1>
```

Primary CTA must be `Call +971 2 626 2042` before the normal consultation CTA.

Content structure:
- examples of urgent dental concerns: severe tooth pain, broken/chipped tooth, lost restoration, dental swelling, dental trauma
- do not promise immediate treatment or 24/7 access
- state that availability depends on clinic hours and clinical assessment
- safety escalation: significant facial/neck swelling with breathing or swallowing difficulty, uncontrolled bleeding, loss of consciousness, or major facial trauma requires emergency medical care rather than waiting for a routine dental appointment
- 2–3 FAQs

Service schema `serviceType: "Emergency dental assessment and urgent dental care"`.

- [ ] **Step 3: Verify GREEN and commit**

```bash
git add treatments/emergency-dentist.html
git commit -m "feat: add emergency dentist Abu Dhabi landing page"
```

---

### Task 7: Connect treatment directory and homepage to the new pages

**Files:**
- Modify: `treatments.html`
- Modify: `index.html`
- Modify: `treatment-pages.css` only if a compact urgent-care row or shared service-team layout needs styling.

**Interfaces:**
- Consumes: all five primary treatment URLs.
- Produces: crawlable, patient-visible internal link architecture.

- [ ] **Step 1: Run directory/home internal-link tests and confirm RED**

- [ ] **Step 2: Update `treatments.html`**

Make these rows actual anchors:
- Dental Implants → `treatments/dental-implants.html`
- Cosmetic Dentistry → `treatments/cosmetic-dentistry.html`
- Orthodontics → `treatments/orthodontics.html`
- General Dentistry → `treatments/general-dentistry.html`
- Emergency Dental Care → `treatments/emergency-dentist.html`

Add Emergency Dental Care as a concise high-priority row without turning the directory into a warning banner.

- [ ] **Step 3: Update `index.html`**

Wire the four existing homepage treatment pathways:
- implants → implants page
- orthodontics → orthodontics page
- cosmetic/restorative → cosmetic page
- general/preventive → general page

Add one small text link near the treatment section: `Need urgent dental care? Call the centre →` linking to the emergency page or phone, without adding another large homepage card.

- [ ] **Step 4: Run tests and verify GREEN**

- [ ] **Step 5: Commit**

```bash
git add treatments.html index.html treatment-pages.css
git commit -m "feat: connect high-intent treatment journeys"
```

---

### Task 8: Expand sitemap and verify the domain switch system

**Files:**
- Modify: `sitemap.xml`
- Test: `tests/test_patch8_technical_seo.py`
- Test: `tests/test_patch9_treatment_seo.py`

**Interfaces:**
- Consumes: four new treatment URLs plus existing implant URL.
- Produces: 13-URL sitemap and continued domain-switch coverage.

- [ ] **Step 1: Add canonical URLs**

Append:

```xml
<url><loc>https://silwadi.ae/treatments/orthodontics.html</loc></url>
<url><loc>https://silwadi.ae/treatments/cosmetic-dentistry.html</loc></url>
<url><loc>https://silwadi.ae/treatments/general-dentistry.html</loc></url>
<url><loc>https://silwadi.ae/treatments/emergency-dentist.html</loc></url>
```

Keep each URL exactly once.

- [ ] **Step 2: Update Patch 8 sitemap expectation from 9 to 13 current pages**

Do not weaken canonical/schema/domain-switch assertions.

- [ ] **Step 3: Run all tests**

```bash
python -m unittest discover -s tests -p 'test*.py' -v
```

Expected: PASS.

- [ ] **Step 4: Run non-test verification**

```bash
node --check app.js
```

Run the static internal-link/asset checker and Python HTTP smoke checks for all 13 canonical pages, `robots.txt`, `sitemap.xml`, relevant CSS, logo and representative doctor portraits.

- [ ] **Step 5: Commit**

```bash
git add sitemap.xml tests/test_patch8_technical_seo.py tests/test_patch9_treatment_seo.py
git commit -m "seo: expand treatment sitemap coverage"
```

---

### Task 9: Final branch review and fast-forward safety gate

- [ ] Verify branch is `ahead > 0`, `behind == 0` against `main`.
- [ ] Confirm changed files are limited to Patch 9 plan/tests, the five treatment pages, treatment directory, homepage, optional treatment CSS, and sitemap.
- [ ] Fetch representative new pages from GitHub and confirm canonical/H1/Service schema/CTA content.
- [ ] Fast-forward `main` with `force=false` only after all checks pass.
- [ ] Compare `main` vs feature branch and require `status: identical`.
