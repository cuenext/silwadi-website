# Arabic Quality & SEO Rebuild Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a professionally written, visually clean and crawlable Arabic version of every patient-facing Silwadi page, with robust bilingual SEO and stable Google Reviews behavior.

**Architecture:** Existing English pages remain canonical source routes. The Arabic dictionary is normalized and reviewed, a static generator creates `/ar/` HTML counterparts, shared RTL CSS controls presentation, and English/Arabic pages receive reciprocal canonical/hreflang metadata. Google Reviews retains one physical marquee direction regardless of language.

**Tech Stack:** Static HTML/CSS/JavaScript, Python standard library build/test tooling, GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-09-05-arabic-quality-seo-rebuild-design.md`

## Global Constraints
- Use natural Modern Standard Arabic appropriate to UAE healthcare.
- Do not preserve awkward literal translation when a clearer Arabic phrase exists.
- Do not change factual doctor credentials, branch details, phone numbers or clinical claims.
- Arabic pages must be real HTML under `/ar/`, not JS-only translated pages.
- Preserve existing English canonical URLs.
- Every Arabic page must have self-canonical + reciprocal `en-AE`, `ar-AE`, and `x-default` hreflang.
- Google Reviews must not reverse/restart when language changes.

---

### Task 1: Add strict Arabic quality contracts

**Files:**
- Create: `tests/test_arabic_quality_seo_rebuild.py`
- Modify: none

**Interfaces:**
- Consumes: current `language.js`, patient-facing HTML route list, review CSS.
- Produces: failing contracts for duplicate dictionary keys, route pairing, Arabic metadata and review animation behavior.

- [ ] **Step 1: Write failing tests** that parse `language.js` source, enumerate patient-facing `.html` files, require `/ar/` counterparts, require Arabic metadata, and reject `.language-ar .google-reviews-track{animation-direction:reverse}`.
- [ ] **Step 2: Run the targeted test** with `python -m unittest tests.test_arabic_quality_seo_rebuild -v` and confirm failures describe missing `/ar/` routes/metadata and review reverse animation.
- [ ] **Step 3: Commit the red tests** with `test: define Arabic quality and SEO contracts`.

### Task 2: Normalize Arabic copy and translation behavior

**Files:**
- Modify: `language.js`
- Test: `tests/test_arabic_quality_seo_rebuild.py`, `tests/test_patch26_arabic_completion.py`, `tests/test_patch3_bilingual_experience.py`

**Interfaces:**
- Consumes: existing English string keys.
- Produces: one reviewed Arabic mapping per source string and stable translation functions used by the static generator.

- [ ] **Step 1: Audit duplicate/conflicting keys** and consolidate repeated entries so the dictionary has one authoritative mapping for each exact source phrase.
- [ ] **Step 2: Rewrite awkward patient-facing Arabic** with concise MSA, consistent doctor names, service terminology and branch names.
- [ ] **Step 3: Fix short CTA translations** so labels such as Book/Call/Explore/Location remain compact and do not contain embedded arrows that conflict with RTL layout.
- [ ] **Step 4: Run Arabic translation tests** and iterate until they pass.
- [ ] **Step 5: Commit** with `fix: normalize Arabic clinical copy`.

### Task 3: Stabilize Google Reviews on language toggle

**Files:**
- Modify: `home-reviews.css`
- Modify if necessary: `language.js` or `app.js`
- Test: `tests/test_arabic_quality_seo_rebuild.py`

**Interfaces:**
- Consumes: existing review track animation.
- Produces: one animation direction for English and Arabic; RTL only affects card text/layout.

- [ ] **Step 1: Keep the failing review test active**.
- [ ] **Step 2: Remove Arabic animation reversal** and ensure language toggling does not recreate/restart the review track.
- [ ] **Step 3: Keep review card text, dialog and metadata aligned correctly in RTL** without changing marquee transform direction.
- [ ] **Step 4: Run targeted tests** and verify pass.
- [ ] **Step 5: Commit** with `fix: keep reviews stable across language changes`.

### Task 4: Add static Arabic page generator

**Files:**
- Create: `tools/build_arabic_site.py`
- Create: `data/arabic-seo.json`
- Test: `tests/test_arabic_quality_seo_rebuild.py`

**Interfaces:**
- Consumes: English HTML pages, reviewed `language.js` dictionary, Arabic SEO map.
- Produces: deterministic `/ar/...` HTML files with translated visible text/attributes and route-aware metadata.

- [ ] **Step 1: Define the complete patient-facing route manifest** including root pages, all doctor profiles and treatment pages.
- [ ] **Step 2: Add Arabic SEO metadata** for each route: Arabic title and concise search description.
- [ ] **Step 3: Implement a deterministic HTML transformer** using Python standard library parsing so text nodes and selected attributes are translated while scripts/styles/URLs remain safe.
- [ ] **Step 4: Rewrite same-site links** inside generated Arabic pages to `/ar/` counterparts when a paired route exists.
- [ ] **Step 5: Inject `lang="ar" dir="rtl"`, self-canonical and reciprocal hreflang tags** into generated output.
- [ ] **Step 6: Run generator and targeted tests**.
- [ ] **Step 7: Commit** with `feat: generate static Arabic pages`.

### Task 5: Arabic RTL visual polish

**Files:**
- Modify: `styles.css`
- Modify as needed: `home-premium.css`, `home-trust.css`, `home-reviews.css`, `about-redesign.css`, `services.css`, `doctor-pages.css`, `treatment-pages.css`, `location-pages.css`, `contact-pages.css`, `institutional-pages.css`
- Test: `tests/test_arabic_quality_seo_rebuild.py`

**Interfaces:**
- Consumes: generated Arabic page class/lang/dir state.
- Produces: compact, readable Arabic layout on desktop/mobile without duplicated labels or unnecessary short-text wrapping.

- [ ] **Step 1: Add global RTL rules** for text alignment, mixed-direction phone/email, buttons and inline arrows/icons.
- [ ] **Step 2: Add mobile width/white-space rules** for short Arabic CTAs and compact informational rows so they stay on one line when practical.
- [ ] **Step 3: Fix homepage trust cards** to avoid repeated labels and stacked microcopy visible in the supplied screenshot.
- [ ] **Step 4: Review forms, doctor cards, treatment cards, location cards and sticky mobile actions** for logical RTL order.
- [ ] **Step 5: Run static tests** and inspect generated markup for representative pages.
- [ ] **Step 6: Commit** with `fix: polish Arabic RTL layouts`.

### Task 6: Bilingual SEO wiring and sitemap

**Files:**
- Modify: all English patient-facing HTML pages (hreflang only)
- Modify: `sitemap.xml`
- Modify: `robots.txt` only if needed
- Test: `tests/test_arabic_quality_seo_rebuild.py`, existing SEO tests

**Interfaces:**
- Consumes: English/Arabic route manifest.
- Produces: reciprocal language discovery for search engines and sitemap coverage for both language trees.

- [ ] **Step 1: Inject reciprocal hreflang tags into every English page** without changing its canonical.
- [ ] **Step 2: Ensure every Arabic page has self-canonical and reciprocal language alternates**.
- [ ] **Step 3: Add Arabic URLs to `sitemap.xml`** with clean absolute URLs.
- [ ] **Step 4: Run targeted SEO tests plus existing SEO suite**.
- [ ] **Step 5: Commit** with `seo: add crawlable Arabic routes and hreflang`.

### Task 7: Full verification and regression review

**Files:**
- Modify only if a verified regression is found.

**Interfaces:**
- Consumes: completed bilingual site.
- Produces: evidence that Arabic quality, routing, reviews and SEO contracts pass without breaking English pages.

- [ ] **Step 1: Run Arabic-specific tests**.
- [ ] **Step 2: Run all existing tests** with `python -m unittest discover -s tests -v`.
- [ ] **Step 3: Run static SEO audit tool** if compatible with current domain configuration.
- [ ] **Step 4: Review generated homepage, About, Services, Doctors, one doctor profile, Treatments, one treatment detail, Locations and Contact HTML for Arabic metadata and clean copy structure.
- [ ] **Step 5: Verify the final GitHub commit and report any pre-existing unrelated test failures separately rather than hiding them.**
