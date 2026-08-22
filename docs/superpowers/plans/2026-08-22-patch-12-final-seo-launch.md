# Patch 12 Final SEO + Launch Package Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Finish launch-grade SEO QA for the 24-page Silwadi Dental Center site and provide a migration package that preserves the indexed legacy domain when `silwadi.ae` launches.

**Architecture:** Keep the site static and dependency-free. Add only crawl/search appearance signals that are broadly supported, create a repeatable Python SEO audit, and package legacy 301 mappings plus deployment/search-engine handoff instructions. Preserve the existing clinical copy and Patch 6–11 contracts.

**Tech Stack:** Static HTML/CSS/JS, Python standard library, unittest, XML sitemap, JSON-LD.

**Spec:** Patch 12 scope from the project conversation: Final SEO QA + Launch Package.

## Global Constraints

- Primary origin remains `https://silwadi.ae`.
- No new JavaScript libraries, CSS frameworks, package manager, or build system.
- Keep copy short, human, clinical, and non-promotional.
- Do not add review/rating schema, unsupported claims, or unverified business facts.
- Existing original doctor PNGs and optimized WebPs remain intact.
- Lighthouse scores must not be claimed unless Lighthouse is actually run.
- All integration into `main` must be non-force and must pass a `behind_by = 0` ancestry gate.

---

### Task 1: Patch 12 RED contract

**Files:**
- Create: `tests/test_patch12_launch_seo.py`

**Interfaces:**
- Consumes: the existing 24 canonical pages, `robots.txt`, and `sitemap.xml`.
- Produces: a regression contract for favicon/search appearance, crawlability, sitemap freshness, redirect handoff, and launch documentation.

- [ ] **Step 1: Write the failing test**

Require every indexable HTML page to expose a stable favicon reference, `index,follow,max-image-preview:large`, and `og:site_name`; require unique titles/descriptions; require sitemap `lastmod`; require `favicon.svg`; require a 301 legacy redirect CSV; require a launch checklist; require a repeatable `tools/seo_launch_audit.py` command.

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_patch12_launch_seo -v`
Expected: FAIL because the Patch 12 assets/docs/signals do not exist yet.

- [ ] **Step 3: Commit**

Commit message: `test: define Patch 12 launch SEO contract`

### Task 2: Search appearance and sitemap readiness

**Files:**
- Create: `favicon.svg`
- Modify: all 24 canonical HTML pages
- Modify: `sitemap.xml`

**Interfaces:**
- Consumes: existing canonical/OG metadata and 24-page sitemap.
- Produces: stable favicon discovery, explicit indexing/image-preview policy, site-name metadata, and accurate significant-update dates.

- [ ] **Step 1: Add launch head signals**

For root pages use `favicon.svg`; for nested doctor/treatment pages use `../favicon.svg`. Add exactly one `meta[name=robots]` with `index,follow,max-image-preview:large` and exactly one `og:site_name` with `Silwadi Dental Center`.

- [ ] **Step 2: Add sitemap freshness**

Add `<lastmod>2026-08-22</lastmod>` to every canonical URL because Patch 12 significantly updates every page head.

- [ ] **Step 3: Run Patch 12 test**

Run: `python -m unittest tests.test_patch12_launch_seo -v`
Expected: launch-head and sitemap tests PASS; redirect/audit-doc tests may still fail until Task 3.

### Task 3: Legacy-domain migration package

**Files:**
- Create: `docs/launch/legacy-redirect-map.csv`
- Create: `docs/launch/SEO-LAUNCH-CHECKLIST.md`

**Interfaces:**
- Consumes: live indexed legacy URLs on `silwadidentalcentres.ae` and the new canonical URL set.
- Produces: one-to-one permanent redirect requirements and a deployment/search-engine handoff sequence.

- [ ] **Step 1: Add verified legacy redirects**

Include `/`, `/index.php`, `/?lang=en`, `/?lang=ar`, `/about-us.php`, `/contact-us.php`, `/doctors.php`, `/services.php`, `/faq.php`, and all 12 live `doctors-details/*.php` URLs. Use HTTP 301 and exact `https://silwadi.ae/...` targets.

- [ ] **Step 2: Add launch checklist**

Cover HTTPS, apex-host canonicalization, one-hop 301s, genuine 404 behavior, `robots.txt`, sitemap, Google Rich Results Test, Search Console URL Inspection and sitemap submission, Bing Webmaster Tools sitemap submission, Google Business Profile website update, and post-launch 404/coverage monitoring. Keep the legacy domain/SSL active for redirects.

### Task 4: Repeatable final SEO audit

**Files:**
- Create: `tools/seo_launch_audit.py`

**Interfaces:**
- Consumes: repository root.
- Produces: exit code 0 with a compact PASS summary when launch SEO invariants hold; non-zero with actionable failures otherwise.

- [ ] **Step 1: Implement audit**

Check 24 sitemap URLs/files, canonical equality, one title/description, uniqueness, no `noindex`, launch head signals, favicon resolution, JSON-LD parseability, no review/rating schema, robots sitemap declaration, valid sitemap `lastmod`, and valid 301 redirect destinations.

- [ ] **Step 2: Run audit**

Run: `python tools/seo_launch_audit.py`
Expected: exit 0 and summary indicating 24 pages, 0 errors.

### Task 5: Full regression and integration gate

**Files:**
- No new product files.

**Interfaces:**
- Consumes: full branch snapshot.
- Produces: verified release candidate safe to merge.

- [ ] **Step 1: Run full tests**

Run: `python -m unittest discover -s tests -p '*.py' -v`
Expected: 0 failures.

- [ ] **Step 2: Run syntax and static audits**

Run: `node --check app.js` and `python tools/seo_launch_audit.py`.
Expected: exit 0.

- [ ] **Step 3: Run local HTTP smoke**

Serve the repository locally and request the 24 canonicals plus key static assets/robots/sitemap; all expected resources return 200.

- [ ] **Step 4: Compare branch to main**

Require `behind_by = 0` before integration.

- [ ] **Step 5: Integrate non-force**

Advance `main` only with `force=false`, then compare `main` and the Patch 12 release candidate and require identical trees.
