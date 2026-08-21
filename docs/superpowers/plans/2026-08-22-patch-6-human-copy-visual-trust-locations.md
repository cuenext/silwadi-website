# Patch 6 Human Copy, Visual Trust & Locations Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the current Silwadi website feel human, concise and clinically credible, replace the bland doctor-count treatment with real team proof, and add a complete Locations page for Bani Yas and the coming-soon Al Raha branch.

**Architecture:** Keep the existing dependency-light static HTML/CSS/JS structure and local PowerShell preview workflow. Patch 6 changes patient-facing copy and page composition only, adds `locations.html` plus focused location styles, and updates navigation to use the new page. No canonical/schema/sitemap work is introduced here; that belongs to later approved SEO patches.

**Tech Stack:** Static HTML5, CSS3, vanilla JavaScript, Python `unittest` contract tests, existing PowerShell local server.

**Spec:** `docs/superpowers/specs/2026-08-22-silwadi-seo-human-copy-local-growth-design.md`

## Global Constraints

- Preserve the approved premium hospital/private-clinic visual direction.
- High-level pages stay concise; detailed clinical/search content stays on treatment and doctor pages.
- Do not use: `cutting-edge`, `state-of-the-art`, `world-class`, `best-in-class`, `personalised solutions tailored to your unique needs`, or repetitive `multidisciplinary clinical workflows` language.
- Do not invent awards, ratings, accreditations, patient counts, success rates, insurance coverage, parking details or branch opening information.
- `Since 1980` remains the primary heritage signal.
- Replace generic `12 doctors` stat treatment with real doctor/team proof.
- Bani Yas Tower is the active branch; Al Raha Mall must remain clearly marked `Coming Soon`.
- All `#locations` / `index.html#locations` navigation must move to `locations.html`.
- Consultation CTAs continue to route through `contact.html#consultation` via the shared JavaScript behavior.
- Keep important copy in HTML, not generated from JavaScript.
- Keep all current doctor images and names sourced from existing repo assets/content; do not identify or infer people from images.

---

## File Structure

**Create**
- `locations.html` — dedicated branch/location page with Bani Yas operational information, map, and Al Raha coming-soon section.
- `location-pages.css` — location-page-only layout and responsive rules.

**Modify**
- `index.html` — shorter human copy, team proof, simplified trust row, location teaser links.
- `doctors.html` — shorter directory intro and less filler under doctor cards.
- `about.html` — shorter institutional copy with more natural language.
- `digital-dentistry.html` — shorter human explanations, keep clinical caution.
- `treatments.html` — concise directory labels and descriptions.
- `treatments/dental-implants.html` — reduce repetitive explanation while preserving clinical assessment/suitability language.
- `contact.html` — shorten contact guidance and route branch navigation to `locations.html`.
- `styles.css` — homepage trust/team visual treatment and reduced text-density spacing.
- `doctor-pages.css` — directory-card copy-density adjustments if needed.
- `institutional-pages.css` — About/Digital text-density adjustments if needed.
- `contact-pages.css` — shorter contact composition spacing if needed.
- `tests/site_contract_test.py` — Patch 6 contracts for copy, team proof and Locations.

**Unchanged behavior**
- `app.js` — existing menu, doctor filtering, FAQ and consultation-routing behavior stays intact unless a regression test proves a navigation bug.

---

### Task 1: Add Patch 6 content and location contracts

**Files:**
- Modify: `tests/site_contract_test.py`

**Interfaces:**
- Consumes: existing `read(name)` helper and repository-relative paths.
- Produces: `PatchSixHumanCopyAndLocationsContract` test class that later implementation tasks must satisfy.

- [ ] **Step 1: Add failing tests for banned filler and concise homepage trust treatment**

Append this test class before the existing `if __name__ == '__main__':` block:

```python
class PatchSixHumanCopyAndLocationsContract(unittest.TestCase):
    def test_home_replaces_bland_doctor_stat_with_team_proof(self):
        html = read('index.html')
        self.assertIn('12 dentists &amp; specialists', html)
        self.assertIn('One established clinical team.', html)
        self.assertIn('Meet the team', html)
        self.assertGreaterEqual(html.count('team-proof__avatar'), 4)
        self.assertNotIn('<strong>12 doctors</strong><span>General &amp; specialist care</span>', html)

    def test_public_copy_avoids_banned_ai_filler(self):
        banned = [
            'cutting-edge',
            'state-of-the-art',
            'world-class',
            'best-in-class',
            'personalised solutions tailored to your unique needs',
            'multidisciplinary clinical workflows',
        ]
        pages = [
            'index.html', 'doctors.html', 'about.html', 'digital-dentistry.html',
            'treatments.html', 'treatments/dental-implants.html', 'contact.html'
        ]
        for rel in pages:
            text = read(rel).lower()
            for phrase in banned:
                self.assertNotIn(phrase, text, f'{rel}: {phrase}')

    def test_locations_page_has_active_and_coming_soon_branches(self):
        path = ROOT / 'locations.html'
        self.assertTrue(path.is_file(), 'locations.html')
        html = read('locations.html')
        self.assertEqual(len(re.findall(r'<h1\\b', html, re.I)), 1)
        self.assertIn('Bani Yas Tower', html)
        self.assertIn('+971 2 626 2042', html)
        self.assertIn('Sun–Wed 09:00–21:00', html)
        self.assertIn('Al Raha Mall', html)
        self.assertIn('Coming Soon', html)
        self.assertIn('google.com/maps', html)
        self.assertIn('contact.html#consultation', html)

    def test_all_primary_navigation_routes_locations_to_real_page(self):
        root_pages = [
            'index.html', 'doctors.html', 'treatments.html', 'about.html',
            'digital-dentistry.html', 'contact.html', 'locations.html'
        ]
        for rel in root_pages:
            html = read(rel)
            self.assertIn('href="locations.html"', html, rel)

        nested_pages = [
            'doctors/dr-munir-silwadi.html',
            'treatments/dental-implants.html',
        ]
        for rel in nested_pages:
            html = read(rel)
            self.assertIn('href="../locations.html"', html, rel)

    def test_locations_page_does_not_claim_unverified_parking_or_open_al_raha(self):
        html = read('locations.html').lower()
        self.assertNotIn('free parking', html)
        self.assertNotIn('valet', html)
        self.assertNotRegex(html, r'al raha[^<]{0,120}(open now|now open|current location)')
```

- [ ] **Step 2: Run the Patch 6 tests and verify RED**

Run:

```bash
python -m unittest tests.site_contract_test.PatchSixHumanCopyAndLocationsContract -v
```

Expected: FAIL because `locations.html`, `12 dentists & specialists`, the team-proof avatars, and new location links do not exist yet.

- [ ] **Step 3: Commit the failing tests**

```bash
git add tests/site_contract_test.py
git commit -m "test: define Patch 6 human copy and locations contracts"
```

---

### Task 2: Rebuild homepage trust/team proof and shorten homepage copy

**Files:**
- Modify: `index.html`
- Modify: `styles.css`

**Interfaces:**
- Consumes: existing doctor assets under `assets/doctors/` and existing `doctors.html`, `about.html`, `digital-dentistry.html`, `contact.html` routes.
- Produces: `.team-proof`, `.team-proof__avatars`, `.team-proof__avatar`, `.trust-line` homepage components and direct `locations.html` links.

- [ ] **Step 1: Replace hero/support copy with concise patient-facing language**

In `index.html`, preserve the H1 `Advanced dentistry. Established trust.` and replace the hero support paragraph with:

```html
<p class="hero-lead">Dental care in Abu Dhabi since 1980, with general dentists and specialists working together in one established centre.</p>
```

Replace the three generic proof boxes with a simple trust line:

```html
<div class="trust-line" aria-label="Centre trust information">
  <span>Abu Dhabi</span>
  <span aria-hidden="true">·</span>
  <strong>Since 1980</strong>
</div>
```

- [ ] **Step 2: Add the real team-proof block**

Place this block after the hero / before the treatment section:

```html
<section class="team-proof section--compact" aria-labelledby="team-proof-title">
  <div class="container team-proof__inner">
    <div class="team-proof__copy">
      <p class="eyebrow">Our team</p>
      <h2 id="team-proof-title">12 dentists &amp; specialists</h2>
      <p>One established clinical team.</p>
      <a class="text-link" href="doctors.html">Meet the team <span>→</span></a>
    </div>
    <div class="team-proof__avatars" aria-label="Selected members of the Silwadi dental team">
      <span class="team-proof__avatar"><img src="assets/doctors/dr-munir-silwadi.png" alt="Dr. Munir Silwadi"></span>
      <span class="team-proof__avatar"><img src="assets/doctors/dr-hani-hasbini.png" alt="Dr. Hani Hasbini"></span>
      <span class="team-proof__avatar"><img src="assets/doctors/dr-fahed-khalil.png" alt="Dr. Fahed Khalil"></span>
      <span class="team-proof__avatar"><img src="assets/doctors/dr-ahmed-el-shehri.png" alt="Dr. Ahmed El Shehri"></span>
      <span class="team-proof__avatar"><img src="assets/doctors/dr-reem-alshaer.png" alt="Dr. Reem Alshaer"></span>
    </div>
  </div>
</section>
```

- [ ] **Step 3: Shorten Home section copy**

Use these exact concise support lines:

```html
<!-- Treatments section intro -->
<p>Choose a treatment area, or contact us if you are not sure where to start.</p>

<!-- About teaser -->
<p>For more than four decades, Silwadi Dental Center has cared for patients in Abu Dhabi with a simple focus: clear advice, careful planning and the right clinician for the job.</p>
<a class="text-link" href="about.html">Learn more about the centre <span>→</span></a>

<!-- Digital teaser -->
<p>Digital tools support selected restorative, implant and smile-planning cases when they add value to diagnosis, planning or communication.</p>
<a class="text-link" href="digital-dentistry.html">Explore digital dentistry <span>→</span></a>
```

- [ ] **Step 4: Route every Home location link to `locations.html`**

Replace Home navigation/footer/shortcut/location teaser anchors that point to `#locations` with `locations.html`. Keep the visible Bani Yas and Al Raha teaser content short.

- [ ] **Step 5: Add restrained homepage CSS**

Add to `styles.css`:

```css
.section--compact{padding:34px 0}
.trust-line{display:flex;align-items:center;gap:10px;margin-top:26px;color:var(--muted);font-size:11px}
.trust-line strong{color:var(--navy);font-weight:750}
.team-proof{border-top:1px solid var(--line);border-bottom:1px solid var(--line);background:#fff}
.team-proof__inner{display:flex;align-items:center;justify-content:space-between;gap:42px}
.team-proof__copy h2{margin:4px 0 4px;color:var(--navy-deep);font-size:clamp(28px,3vw,40px);line-height:1.06;letter-spacing:-.04em;font-weight:620}
.team-proof__copy p:not(.eyebrow){margin:0 0 12px;color:var(--muted);font-size:11px}
.team-proof__avatars{display:flex;align-items:center;padding-right:14px}
.team-proof__avatar{width:74px;height:74px;border-radius:50%;overflow:hidden;border:4px solid #fff;background:#dcebed;box-shadow:0 0 0 1px var(--line);margin-right:-14px}
.team-proof__avatar img{width:100%;height:100%;object-fit:cover;object-position:center 20%}
@media(max-width:720px){.team-proof__inner{align-items:flex-start;flex-direction:column;gap:20px}.team-proof__avatar{width:62px;height:62px}.team-proof__avatars{padding-bottom:4px}}
```

- [ ] **Step 6: Run the focused homepage/team test**

```bash
python -m unittest tests.site_contract_test.PatchSixHumanCopyAndLocationsContract.test_home_replaces_bland_doctor_stat_with_team_proof -v
```

Expected: PASS.

- [ ] **Step 7: Commit homepage changes**

```bash
git add index.html styles.css
git commit -m "feat: humanize homepage trust and team proof"
```

---

### Task 3: Human-copy pass across existing pages

**Files:**
- Modify: `doctors.html`
- Modify: `about.html`
- Modify: `digital-dentistry.html`
- Modify: `treatments.html`
- Modify: `treatments/dental-implants.html`
- Modify: `contact.html`
- Modify: `doctor-pages.css`
- Modify: `institutional-pages.css`
- Modify: `contact-pages.css`

**Interfaces:**
- Consumes: existing page structures and clinical claims already present in approved content.
- Produces: shorter intros/card copy without changing doctor roster, treatment taxonomy, or clinical caution.

- [ ] **Step 1: Shorten the Doctors page intro and card filler**

Use:

```html
<h1>Find a Doctor</h1>
<p class="page-hero__lead">Search by name or specialty.</p>
```

For each non-Munir doctor card, keep only name + specialty + one short focus line no longer than one sentence. Example:

```html
<p class="doctor-directory-card__focus">General dental care and restorative treatment.</p>
```

Do not add biographies that are not verified.

- [ ] **Step 2: Shorten About page narrative**

Keep the factual `Since 1980`, `Dr. Munir Silwadi`, `continuity of care` and `multidisciplinary` requirements but use shorter sections. The primary intro becomes:

```html
<p class="institutional-hero__lead">Silwadi Dental Center has cared for patients in Abu Dhabi since 1980. Today, the centre brings general dentists and specialists together under one roof.</p>
```

Where the current page repeats philosophy/process language, reduce it to simple statements such as:

```html
<h2>Care that has grown with the city.</h2>
<p>What began as an established dental practice has grown into a team covering general and specialist dentistry while keeping continuity of care at the centre of the experience.</p>
```

- [ ] **Step 3: Humanize Digital Dentistry copy**

Keep the required terms `CAD / CAM Dentistry`, `Intraoral Scanning`, `Guided Implant Planning`, and `Digital Smile Planning`. Replace broad technology claims with:

```html
<p class="institutional-hero__lead">Digital tools are used when they help the dentist see, plan or explain treatment more clearly.</p>
```

Each technology description should be one sentence and include caution such as `selected cases` where relevant.

- [ ] **Step 4: Shorten Treatments directory copy**

Change the hero support to:

```html
<p class="treatment-hero__lead">Browse by treatment area. If you are unsure where to start, our team can point you to the right dentist or specialist.</p>
```

Keep treatment-row descriptions to one concise sentence each.

- [ ] **Step 5: Reduce Dental Implants repetition without removing clinical safeguards**

Keep these concepts visible in HTML:
- `clinical assessment`
- `selected cases`
- suitability depends on individual findings
- digital/guided planning may be used where appropriate

Use this hero support:

```html
<p class="detail-hero__lead">Implants can replace missing teeth in selected cases. The first step is a clinical assessment to understand your oral health and the restoration you may need.</p>
```

- [ ] **Step 6: Shorten Contact page guidance**

Use:

```html
<p class="contact-hero__lead">Call, email or send a consultation request. If you are not sure who to book with, reception can guide you.</p>
```

Keep operational facts; remove repeated explanations of the same routing process.

- [ ] **Step 7: Adjust page CSS only where copy reduction leaves awkward spacing**

Reduce oversized bottom margins rather than adding decorative cards. Keep existing typography tokens and colors.

- [ ] **Step 8: Run copy-quality contract**

```bash
python -m unittest tests.site_contract_test.PatchSixHumanCopyAndLocationsContract.test_public_copy_avoids_banned_ai_filler -v
```

Expected: PASS.

- [ ] **Step 9: Run all pre-existing contracts**

```bash
python -m unittest tests.site_contract_test -v
```

Expected: all existing Patch 1–5 tests remain green except the location-routing tests that intentionally wait for Task 4.

- [ ] **Step 10: Commit copy pass**

```bash
git add doctors.html about.html digital-dentistry.html treatments.html treatments/dental-implants.html contact.html doctor-pages.css institutional-pages.css contact-pages.css
git commit -m "refactor: make patient copy shorter and more human"
```

---

### Task 4: Create the dedicated Locations page

**Files:**
- Create: `locations.html`
- Create: `location-pages.css`

**Interfaces:**
- Consumes: `styles.css`, `doctor-pages.css`, `app.js`, existing logo asset, verified Bani Yas address/phone/hours, Al Raha address/status.
- Produces: `locations.html` as the canonical in-site destination for branch information.

- [ ] **Step 1: Create `locations.html` with one H1 and two clearly separated branch states**

Use this page structure:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Locations | Silwadi Dental Center Abu Dhabi</title>
  <meta name="description" content="Visit Silwadi Dental Center at Bani Yas Tower in Abu Dhabi. View contact details, opening hours and the upcoming Al Raha Mall branch.">
  <meta name="theme-color" content="#083847">
  <link rel="stylesheet" href="styles.css">
  <link rel="stylesheet" href="doctor-pages.css">
  <link rel="stylesheet" href="location-pages.css">
</head>
<body>
  <!-- reuse the existing utility strip/header pattern; Locations links to locations.html and Book a Consultation links to contact.html#consultation -->
  <main id="main">
    <section class="location-hero">
      <div class="container">
        <nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span>Locations</span></nav>
        <p class="eyebrow">Abu Dhabi</p>
        <h1>Our locations</h1>
        <p class="location-hero__lead">Visit our Bani Yas Tower centre. A second Silwadi location at Al Raha Mall is coming soon.</p>
      </div>
    </section>

    <section class="location-detail location-detail--active">
      <div class="container location-detail__grid">
        <div class="location-detail__copy">
          <span class="location-state">Current location</span>
          <h2>Bani Yas Tower</h2>
          <p>Al Hilal Bank, Bani Yas Tower, Building 117 C Floor, Sultan Bin Zayed The First St, W Corniche Road, Abu Dhabi.</p>
          <dl class="location-facts">
            <div><dt>Phone</dt><dd><a href="tel:+97126262042">+971 2 626 2042</a></dd></div>
            <div><dt>Email</dt><dd><a href="mailto:info@silwadidentalcentres.ae">info@silwadidentalcentres.ae</a></dd></div>
            <div><dt>Opening hours</dt><dd>Sun–Wed 09:00–21:00 · Thu &amp; Sat 09:00–18:00 · Friday closed</dd></div>
          </dl>
          <div class="location-actions">
            <a class="btn btn--primary" href="contact.html#consultation">Book a Consultation</a>
            <a class="btn btn--secondary" href="https://www.google.com/maps/search/?api=1&amp;query=Dr%20Munir%20Silwadi%20Dental%20Centre%20Bani%20Yas%20Tower%20Abu%20Dhabi">Get Directions</a>
          </div>
        </div>
        <div class="location-map">
          <iframe title="Map showing Silwadi Dental Center at Bani Yas Tower, Abu Dhabi" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Dr.+Munir+Silwadi+Dental+Centre+Bani+Yas+Tower+Abu+Dhabi&amp;output=embed"></iframe>
        </div>
      </div>
    </section>

    <section class="location-detail location-detail--coming">
      <div class="container location-detail__grid location-detail__grid--compact">
        <div class="location-detail__copy">
          <span class="location-state location-state--muted">Coming Soon</span>
          <h2>Al Raha Mall</h2>
          <p>F14 &amp; F15, Level 1, Al Raha Mall, Abu Dhabi, UAE.</p>
          <p class="location-note">This branch is not yet presented as an operating location. Contact the centre for updates.</p>
        </div>
        <div class="location-coming-mark" aria-hidden="true"><span>Al Raha Mall</span><strong>Coming Soon</strong></div>
      </div>
    </section>
  </main>
  <!-- reuse current footer/mobile action bar; include app.js -->
</body>
</html>
```

- [ ] **Step 2: Create `location-pages.css`**

```css
.location-hero{padding:58px 0 52px;background:var(--quiet);border-bottom:1px solid var(--line)}
.location-hero h1{margin:0;color:var(--navy-deep);font-size:clamp(42px,5vw,64px);line-height:1.02;letter-spacing:-.05em;font-weight:620}
.location-hero__lead{max-width:650px;margin:16px 0 0;color:var(--muted);font-size:13px;line-height:1.7}
.location-detail{padding:72px 0;border-bottom:1px solid var(--line)}
.location-detail__grid{display:grid;grid-template-columns:minmax(0,.9fr) minmax(420px,1.1fr);gap:72px;align-items:center}
.location-detail__grid--compact{align-items:stretch}
.location-state{display:inline-block;margin-bottom:16px;color:var(--teal);font-size:9px;font-weight:800;letter-spacing:.12em;text-transform:uppercase}
.location-state--muted{color:var(--muted)}
.location-detail h2{margin:0 0 14px;color:var(--navy-deep);font-size:36px;letter-spacing:-.04em;font-weight:620}
.location-detail__copy>p{max-width:620px;color:var(--muted);font-size:12px;line-height:1.75}
.location-facts{margin:28px 0;border-top:1px solid var(--line)}
.location-facts div{display:grid;grid-template-columns:130px 1fr;gap:20px;padding:14px 0;border-bottom:1px solid var(--line)}
.location-facts dt{color:var(--navy);font-size:10px;font-weight:750}.location-facts dd{margin:0;color:var(--muted);font-size:10px;line-height:1.6}.location-facts a{color:var(--teal)}
.location-map{min-height:420px;border:1px solid var(--line);background:var(--quiet);overflow:hidden}.location-map iframe{width:100%;height:420px;border:0;display:block}
.location-coming-mark{min-height:260px;display:flex;flex-direction:column;justify-content:center;padding:42px;border:1px solid var(--line);background:var(--quiet)}
.location-coming-mark span{color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.12em}.location-coming-mark strong{margin-top:8px;color:var(--navy);font-size:34px;font-weight:620}
.location-note{margin-top:18px}.location-actions{display:flex;gap:10px;flex-wrap:wrap}
@media(max-width:920px){.location-detail__grid{grid-template-columns:1fr;gap:34px}.location-map,.location-map iframe{min-height:340px;height:340px}}
@media(max-width:620px){.location-hero{padding:42px 0}.location-detail{padding:52px 0}.location-detail h2{font-size:30px}.location-facts div{grid-template-columns:1fr;gap:5px}.location-map,.location-map iframe{min-height:300px;height:300px}}
```

- [ ] **Step 3: Run Locations tests**

```bash
python -m unittest \
  tests.site_contract_test.PatchSixHumanCopyAndLocationsContract.test_locations_page_has_active_and_coming_soon_branches \
  tests.site_contract_test.PatchSixHumanCopyAndLocationsContract.test_locations_page_does_not_claim_unverified_parking_or_open_al_raha -v
```

Expected: PASS.

- [ ] **Step 4: Commit Locations page**

```bash
git add locations.html location-pages.css
git commit -m "feat: add dedicated Abu Dhabi locations page"
```

---

### Task 5: Route location navigation across every page

**Files:**
- Modify: `index.html`
- Modify: `doctors.html`
- Modify: `doctors/dr-munir-silwadi.html`
- Modify: `treatments.html`
- Modify: `treatments/dental-implants.html`
- Modify: `about.html`
- Modify: `digital-dentistry.html`
- Modify: `contact.html`
- Modify: `locations.html`

**Interfaces:**
- Consumes: new `locations.html` route.
- Produces: consistent root `locations.html` and nested `../locations.html` navigation.

- [ ] **Step 1: Update root-level page navigation**

On `index.html`, `doctors.html`, `treatments.html`, `about.html`, `digital-dentistry.html`, `contact.html`, and `locations.html`, ensure primary/mobile/footer location links use:

```html
<a href="locations.html">Locations</a>
```

- [ ] **Step 2: Update nested pages**

On `doctors/dr-munir-silwadi.html` and `treatments/dental-implants.html`, use:

```html
<a href="../locations.html">Locations</a>
```

- [ ] **Step 3: Run navigation contract**

```bash
python -m unittest tests.site_contract_test.PatchSixHumanCopyAndLocationsContract.test_all_primary_navigation_routes_locations_to_real_page -v
```

Expected: PASS.

- [ ] **Step 4: Commit route updates**

```bash
git add index.html doctors.html doctors/dr-munir-silwadi.html treatments.html treatments/dental-implants.html about.html digital-dentistry.html contact.html locations.html
git commit -m "feat: route location navigation to dedicated page"
```

---

### Task 6: Full Patch 6 verification

**Files:**
- Test: `tests/site_contract_test.py`
- Verify: all changed HTML/CSS/JS assets.

**Interfaces:**
- Consumes: Tasks 1–5.
- Produces: a branch that is safe to fast-forward to `main`.

- [ ] **Step 1: Run the entire contract suite**

```bash
python -m unittest tests.site_contract_test -v
```

Expected: all Patch 1–6 tests PASS with zero failures/errors.

- [ ] **Step 2: Check JavaScript syntax**

```bash
node --check app.js
```

Expected: exit code 0 and no syntax errors.

- [ ] **Step 3: Check local internal links and assets**

Run a Python script from repo root:

```bash
python - <<'PY'
from pathlib import Path
import re
root = Path('.')
html_files = [p for p in root.rglob('*.html') if '.git' not in p.parts]
missing = []
for page in html_files:
    text = page.read_text(encoding='utf-8')
    for attr, value in re.findall(r'\b(href|src)="([^"]+)"', text, re.I):
        if value.startswith(('http:', 'https:', 'mailto:', 'tel:', '#', 'data:')):
            continue
        target = value.split('#',1)[0].split('?',1)[0]
        if not target:
            continue
        resolved = (page.parent / target).resolve()
        if not resolved.exists():
            missing.append(f'{page}: {value}')
if missing:
    raise SystemExit('\n'.join(missing))
print(f'OK: checked {len(html_files)} HTML files; no missing local links/assets')
PY
```

Expected: `OK` and zero missing paths.

- [ ] **Step 4: Start local server and smoke-test key pages**

Use the existing local preview server, then verify HTTP 200 for:

```text
/index.html
/doctors.html
/treatments.html
/about.html
/digital-dentistry.html
/locations.html
/contact.html
/doctors/dr-munir-silwadi.html
/treatments/dental-implants.html
```

Also verify the Bani Yas map iframe is present in `/locations.html` HTML and the page remains usable if the external map fails to load.

- [ ] **Step 5: Confirm branch is fast-forwardable**

Compare the Patch 6 branch against `main`. Required state before promotion:

```text
behind_by = 0
```

- [ ] **Step 6: Fast-forward `main` and verify identity**

After moving `main`, compare `main` vs the Patch 6 branch. Required result:

```text
status = identical
ahead_by = 0
behind_by = 0
```

- [ ] **Step 7: Final commit if verification required a code fix**

If any verification fix was necessary, commit only the fix with a narrow message such as:

```bash
git commit -am "fix: resolve Patch 6 navigation regression"
```

Do not mix future Patch 7 SEO work into Patch 6.
