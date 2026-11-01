# Silwadi Logo Production Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Put the exact approved Silwadi logo treatment into every real site header and footer without deploying the review page.

**Architecture:** Keep the canonical raster at the existing PNG URL for metadata, and add a self-contained SVG display asset that embeds the same bytes and applies the approved background-key filter. Point visible site placements at the SVG and normalize their intrinsic ratio and CSS sizing.

**Tech Stack:** Static HTML/CSS, SVG filters, Node.js built-in test runner.

**Spec:** `docs/superpowers/specs/2026-11-01-silwadi-logo-production-design.md`

## Global Constraints

- Preserve SHA-256 `f7b77e5eb8e9a170dca0508ed2ef70b6e4983795c845f68ddc847894b74d8ab4` and intrinsic dimensions `259 × 225`.
- Do not add the review page or its markup to production.
- Do not deploy or push.
- Leave Open Graph, schema, and site configuration URLs on `assets/silwadi-logo-official.png`.
- Preserve localized alt text, links, loading behavior, and all non-logo content.

## Review Focus

- Nested relative paths and the absolute URL in the legacy endodontics page must resolve to the SVG.
- FAQ language templates must switch without restoring the old logo.
- The 720 px and 760 px sizing overrides must retain the approved natural ratio.
- Arabic footer rules must not re-enable multiply blending.
- Metadata crawlers must continue receiving the PNG URL while browsers receive the filtered SVG.

---

### Task 1: Lock the production logo contract

**Files:**
- Create: `tests/silwadi-logo-production.test.cjs`
- Create: `assets/silwadi-logo-official.svg`
- Modify: `assets/silwadi-logo-official.png`

**Interfaces:**
- Consumes: supplied PNG bytes and approved filter values from the spec.
- Produces: safe self-contained display asset at `/assets/silwadi-logo-official.svg`.

- [ ] **Step 1: Write the failing contract test**

Assert the PNG hash/dimensions, decoded SVG payload hash, SVG bounds/filter safety, production `<img>` coverage, metadata PNG URLs, approved CSS sizes, and absence of multiply blending.

- [ ] **Step 2: Run the focused test and confirm it fails for the missing SVG/old markup**

Run: `node --test tests/silwadi-logo-production.test.cjs`
Expected: FAIL because the display SVG does not exist.

- [ ] **Step 3: Add the exact raster and self-contained SVG asset**

Copy the supplied raster byte-for-byte to the canonical PNG path; embed those bytes in the SVG and apply the approved filter within `0 0 259 225`.

### Task 2: Replace every real visible placement

**Files:**
- Modify: 67 public HTML files containing visible official logo images
- Modify: `styles.css`
- Modify: `home-reviews.css`
- Modify: `arabic-quality.css`
- Modify: any page-local logo rules identified by the contract test
- Test: `tests/silwadi-logo-production.test.cjs`

**Interfaces:**
- Consumes: `/assets/silwadi-logo-official.svg` from Task 1.
- Produces: consistent header/footer rendering with 259:225 intrinsic dimensions.

- [ ] **Step 1: Mechanically retarget visible official-logo `<img>` elements**

Change only their filename extension to `.svg` and normalize their width/height attributes to `259`/`225`, preserving paths, alt text, classes, and other attributes.

- [ ] **Step 2: Apply the approved responsive sizing**

Use 82 px desktop header width, 72 px mobile header width, 128 px footer width, auto height, aspect ratio `259 / 225`, and normal blending across shared and override styles.

- [ ] **Step 3: Run the focused test and confirm it passes**

Run: `node --test tests/silwadi-logo-production.test.cjs`
Expected: PASS.

### Task 3: Verify the complete site behavior

**Files:**
- Modify only if verification finds a logo-specific regression.

**Interfaces:**
- Consumes: implemented production asset and markup.
- Produces: verified local-only website change.

- [ ] **Step 1: Run all available Node tests and logo-sensitive legacy tests**

Run the full Node suite plus the Python tests where a Python runtime is available. Update only obsolete assertions that intentionally require the visible PNG source.

- [ ] **Step 2: Preview representative routes and breakpoints**

Check `/`, `/ar/`, `/ai/`, an Arabic nested doctor/location page, and a treatment page at desktop, 390 px, 320 px, and the 720/760 px override boundaries.

- [ ] **Step 3: Inspect the final diff and repository state**

Confirm no review-page artifacts, deployment changes, unrelated edits, external SVG references, or missing production logo placements.

- [ ] **Step 4: Commit the local implementation**

Commit only the production asset, markup/CSS, focused test, and design/plan documents; do not push or deploy.
