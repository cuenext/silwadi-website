# Silwadi Google Authority Pass Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Strengthen how Google understands Silwadi Dental Center, its two Abu Dhabi branches, doctors, services, and language variants without changing the visible website design or publishing private review pages.

**Architecture:** Treat the site as one connected entity graph with stable absolute schema IDs for the parent brand, Bani Yas branch, Al Raha branch, website, doctors, and service pages. Enforce metadata compliance, canonical/hreflang consistency, sitemap hygiene, and doctor-to-branch referential integrity with standard-library Python regression tests. Keep all changes in `<head>`, JSON-LD, XML, tests, workflows, and repo-only documentation; visible HTML content and CSS remain unchanged.

**Tech Stack:** Static HTML, JSON-LD/Schema.org, XML sitemap, Python `unittest`, GitHub Actions.

**Spec:** User-approved behind-the-scenes SEO authority pass in the 2026-09-13 Website Silwadi conversation.

## Global Constraints

- Zero visible design/layout/body-copy changes.
- Do not publish, link, index, or add to sitemap any private `review/` page.
- Do not modify or delete `old-silwadi-site`.
- Do not add unsupported ratings, prices, insurance claims, awards, guarantees, or superiority claims.
- Remove or prevent risky promotional metadata terms such as `best`, `painless`, `pain-free`, `top-tier`, and guaranteed-outcome language.
- Preserve the established doctor roster, specialties, and branch assignments.
- Preserve legacy doctor URLs unless an explicit redirect migration is separately approved.
- Keep booking URL `https://silwadi.ae/contact.html#consultation-form`.
- Use only known official contact, address, hours, and social information.
- Private Pediatric, Endodontics, POD, FAQ, and AI FAQ review pages remain `noindex` and unpublished.

---

### Task 1: Add a permanent sitewide Google-authority regression contract

**Files:**
- Create: `tests/test_google_authority.py`
- Create: `.github/workflows/google-authority-test.yml`

**Interfaces:**
- Consumes: public HTML files, doctor profiles, `sitemap.xml`.
- Produces: automated checks for metadata compliance, stable schema IDs, doctor branch references, sitemap privacy, and canonical/hreflang hygiene.

- [ ] **Step 1: Write failing tests** for prohibited metadata language, stable root entity IDs, both branch entities on the homepage, doctor `worksFor` IDs, and private-review sitemap exclusion.
- [ ] **Step 2: Run the workflow on the SEO branch** and confirm RED failures correspond to current metadata/entity inconsistencies.
- [ ] **Step 3: Keep the tests unchanged while implementing Tasks 2–5.**
- [ ] **Step 4: Re-run the workflow until all tests pass.**

### Task 2: Clean non-visible promotional metadata

**Files:**
- Modify: `index.html`
- Modify only additional public HTML heads if the audit finds prohibited promotional metadata.

**Interfaces:**
- Consumes: existing factual visible content and clinic facts.
- Produces: factual title, description, OG/Twitter metadata without superiority claims.

- [ ] **Step 1: Confirm the RED test catches homepage `Best Dentist` metadata.**
- [ ] **Step 2: Replace only non-visible homepage title/meta/OG/Twitter strings with factual Abu Dhabi wording.**
- [ ] **Step 3: Scan public metadata for other prohibited terms and fix only metadata occurrences.**
- [ ] **Step 4: Run metadata tests to GREEN.**

### Task 3: Unify the Silwadi entity graph

**Files:**
- Modify: `index.html`
- Modify: `locations.html`
- Modify: `contact.html`
- Modify: `about.html` only if its schema uses conflicting local IDs.
- Modify: `doctors.html` and `treatments.html` only if their publisher/about references are inconsistent.

**Interfaces:**
- Produces stable IDs:
  - `https://silwadi.ae/#organization`
  - `https://silwadi.ae/#dentist`
  - `https://silwadi.ae/#dentist-al-raha`
  - `https://silwadi.ae/#website`

- [ ] **Step 1: Confirm tests fail because branch/entity IDs are page-local or incomplete.**
- [ ] **Step 2: Add a parent `Organization` entity for Silwadi Dental Center with founding year 1980, founder, official logo, website, email, WhatsApp/contact point where appropriate, and known Instagram only.**
- [ ] **Step 3: Represent Bani Yas and Al Raha as separate `Dentist` entities using their exact known names, addresses, phones, geo, and opening hours; remove unsupported `priceRange` if present.**
- [ ] **Step 4: Make `WebSite.publisher`, page `about`, and doctor `worksFor` references resolve to the stable absolute IDs.**
- [ ] **Step 5: Run entity-reference tests to GREEN.**

### Task 4: Canonical, hreflang, and sitemap hygiene

**Files:**
- Modify: public English/Arabic HTML head tags only where an actual mismatch exists.
- Modify: `sitemap.xml` only when necessary.

**Interfaces:**
- Produces clean self-canonicals, reciprocal English/Arabic alternates where counterparts exist, and an indexable-only sitemap.

- [ ] **Step 1: Audit canonical/hreflang pairs for current public pages.**
- [ ] **Step 2: Add regression checks for duplicate/missing canonicals and review-page sitemap leakage.**
- [ ] **Step 3: Fix only technical head-tag mismatches; do not change visible language or navigation.**
- [ ] **Step 4: Ensure `sitemap.xml` contains no `review/`, `.tmp/`, or `old-silwadi-site` URLs.**
- [ ] **Step 5: Run canonical/hreflang/sitemap tests to GREEN.**

### Task 5: Doctor and service authority consistency

**Files:**
- Modify: doctor/profile JSON-LD only if referential inconsistencies are found.
- Modify: treatment-page JSON-LD only if publisher/provider references are inconsistent.

**Interfaces:**
- Consumes: established 15-doctor roster and branch map.
- Produces: consistent doctor-to-branch and service-to-provider relationships without changing visible doctor bios.

- [ ] **Step 1: Parse all 15 English doctor pages and verify `Person.worksFor` uses only the two approved branch IDs.**
- [ ] **Step 2: Verify treatment `Service.provider`/publisher references resolve to the Silwadi graph where present.**
- [ ] **Step 3: Fix schema references only where necessary.**
- [ ] **Step 4: Re-run existing doctor SEO/compliance tests plus the new authority tests.**

### Task 6: Produce the Google/Local SEO action report

**Files:**
- Create: `docs/seo/google-authority-audit-2026-09-13.md`

**Interfaces:**
- Produces: repo-only audit of implemented technical changes plus recommendations requiring manual Google Business Profile/Search Console or user approval.

- [ ] **Step 1: Record the before/after entity graph, metadata issues fixed, sitemap/canonical status, and test evidence.**
- [ ] **Step 2: Document Google Business Profile recommendations separately for Bani Yas and Al Raha using only known facts.**
- [ ] **Step 3: List Search Console actions: sitemap submission/refresh, URL inspection priorities, indexing checks, and performance queries to watch.**
- [ ] **Step 4: Put all potentially visible SEO improvements in a recommendation section only; do not implement them.**

### Task 7: Final verification and release

**Files:**
- No new production scope.

- [ ] **Step 1: Run new Google-authority tests and existing doctor SEO/compliance tests.**
- [ ] **Step 2: Compare branch against `main` and confirm no CSS, visible body copy, private-page publication, or pediatric asset changes.**
- [ ] **Step 3: Verify JSON-LD parses and XML sitemap remains valid.**
- [ ] **Step 4: Fast-forward `main` only after all checks pass because this SEO work was explicitly approved.**
- [ ] **Step 5: Verify GitHub Pages deployment/status and report exact changes, remaining manual Google actions, and any deferred visible recommendations.**
