# Pediatric Publish + Endodontics Booking + POD Review Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish the approved Pediatric Dentistry page with the same global/header architecture as Endodontics, make Endodontics booking CTAs open the consultation form directly, and repair the POD review page so its header and gallery feel intentional rather than oversized.

**Architecture:** Keep each change isolated. Pediatric is promoted from the approved review page into a production treatment URL and wired into internal links + sitemap. Endodontics only changes booking targets. POD remains a noindex review page, but adopts the same global navigation pattern and a smaller carousel width so the imagery no longer dominates the viewport.

**Tech Stack:** Static HTML/CSS/JS on GitHub Pages, Python string/regex transformations inside a temporary GitHub Actions workflow, existing `styles.css` and page-local CSS.

**Spec:** User approval and screenshots in the active Website Silwadi conversation on 2026-09-16.

## Global Constraints

- Preserve the approved Pediatric page content/design except for production metadata, navigation/header architecture, and link wiring.
- Pediatric production header must match the approved Endodontics pattern: Silwadi global header + subtle `On this page` utility strip.
- Endodontics `Book an Appointment` must link directly to `/contact.html#consultation-form`, never to an intermediate `#consultation` section.
- POD stays under `/review/`, stays `noindex`, and must not be published yet.
- POD gallery must render substantially smaller on desktop while retaining side peeks and mobile swipe behavior.
- Do not alter unrelated treatment pages.

---

### Task 1: Publish Pediatric Dentistry

**Files:**
- Create: `treatments/pediatric-dentistry.html`
- Modify: `services.html`
- Modify: `treatments.html`
- Modify: `sitemap.xml`
- Source: `review/pediatric-dentistry-v1.html`

**Interfaces:**
- Consumes: approved Pediatric review HTML and Endodontics global/header pattern.
- Produces: indexable `https://silwadi.ae/treatments/pediatric-dentistry.html` linked from services/treatments navigation.

- [ ] **Step 1: Write the failing contract**

Run a Python assertion that the production Pediatric file does not yet satisfy all of: exists, `index,follow`, canonical URL, global header, `On this page` utility nav, and sitemap/internal-link references.

- [ ] **Step 2: Run the contract and verify RED**

Expected: failure because `treatments/pediatric-dentistry.html` does not yet exist.

- [ ] **Step 3: Create the production page**

Copy the approved review file, remove the private-review bar, replace the review-only header with the Endodontics-style global header + utility strip, convert relative assets/links to production-safe root-relative paths, set `index,follow`, canonical/OG/Twitter metadata, and add Pediatric/Breadcrumb/FAQ structured data.

- [ ] **Step 4: Wire internal links**

Replace `services.html#pedodontics` references in `services.html` and `treatments.html` with `/treatments/pediatric-dentistry.html`, including structured-data URLs. Add the Pediatric URL to `sitemap.xml` with `2026-09-16` as `lastmod`.

- [ ] **Step 5: Verify GREEN**

Assert one H1, indexable robots, canonical URL, global header + utility strip, Dr. Kashmira profile link, direct contact-form booking links, services/treatments internal links, and sitemap entry.

- [ ] **Step 6: Commit**

Commit the Pediatric publish separately.

---

### Task 2: Make Endodontics booking direct

**Files:**
- Modify: `treatments/endodontics.html`

**Interfaces:**
- Consumes: existing Endodontics production page.
- Produces: hero booking CTA that opens the consultation form immediately.

- [ ] **Step 1: Write the failing contract**

Assert that the hero CTA contains `href="/contact.html#consultation-form"` and that no primary booking CTA uses `href="#consultation"`.

- [ ] **Step 2: Run and verify RED**

Expected: failure because the hero CTA currently points to `#consultation`.

- [ ] **Step 3: Implement the minimal fix**

Change only the hero `Book an Appointment` target from `#consultation` to `/contact.html#consultation-form`.

- [ ] **Step 4: Verify GREEN**

Re-run the contract and confirm the CTA is direct while the page structure remains unchanged.

- [ ] **Step 5: Commit**

Commit the Endodontics booking fix separately.

---

### Task 3: Repair POD review presentation

**Files:**
- Modify: `review/people-of-determination-raha-v1.html`

**Interfaces:**
- Consumes: existing POD review page and Endodontics navigation pattern.
- Produces: still-private POD review page with normal Silwadi navigation and a restrained desktop gallery.

- [ ] **Step 1: Write the failing contract**

Assert that POD contains a global header, an `On this page` utility strip, remains `noindex`, and uses a desktop slide width capped at `880px` or less instead of `1120px`.

- [ ] **Step 2: Run and verify RED**

Expected: failure because the current page has a minimal review header and `--pod-slide-width:min(82vw,1120px)`.

- [ ] **Step 3: Implement the header fix**

Keep the private-review bar but replace the minimal POD header with the normal Silwadi global header and a subtle utility strip linking to `#partnership`, `#individual-care`, `#complex-needs`, `#raha`, and the appointment form.

- [ ] **Step 4: Implement the gallery-size fix**

Change desktop `--pod-slide-width` to `min(68vw,880px)`, retain 3:2 cropping and side peeks, and keep mobile width rules unchanged so swipe behavior remains usable.

- [ ] **Step 5: Verify GREEN**

Assert `noindex` remains, global header exists once, utility strip exists once, no duplicate top-level appointment CTA exists in the utility strip, desktop gallery cap is <=880px, and carousel JS/data attributes remain present.

- [ ] **Step 6: Commit**

Commit the POD review repair separately.

---

### Task 4: Final integration verification

**Files:**
- Verify all files touched above.

- [ ] **Step 1: Run cross-page contracts**

Check Pediatric production URL wiring, Endodontics direct booking, POD noindex status, and absence of temporary workflow artifacts.

- [ ] **Step 2: Confirm GitHub Pages deployment**

Wait for the final Pages workflow to complete successfully before reporting completion.
