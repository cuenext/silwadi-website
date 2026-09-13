# Silwadi Google Authority & Local SEO Audit

Date: 2026-09-13
Scope: behind-the-scenes technical SEO only

## Executive summary

Silwadi is already discoverable by Google. The highest-value next step is therefore not keyword stuffing or a visual redesign; it is **entity consolidation**: making Google receive one consistent technical description of the Silwadi brand, its two Abu Dhabi branches, its doctors, its services, and the English/Arabic versions of those pages.

This pass implemented that entity architecture without changing visible design, layout, body copy, photos, navigation, or private-page publication status.

The most important external problem discovered is larger than any on-page metadata issue: **the previous domain `silwadidentalcentres.ae` is still serving live, indexable legacy pages.** This splits domain authority and exposes stale information and advertising language. The separate redirect plan in `docs/seo/legacy-domain-redirect-map-2026-09-13.md` should be treated as P0.

## What was implemented behind the scenes

### 1. One stable Silwadi entity graph

The current site now uses stable absolute IDs so Google can connect pages to the same real-world entities:

- Parent brand: `https://silwadi.ae/#organization`
- Bani Yas branch: `https://silwadi.ae/#dentist`
- Al Raha Mall branch: `https://silwadi.ae/#dentist-al-raha`
- Website: `https://silwadi.ae/#website`

The parent Organization connects to:
- Silwadi Dental Center
- founding year 1980
- founder Dr. Munir Silwadi
- official logo
- official website/email
- the two branch entities
- the established official Instagram URL already present in site data

The branch entities connect to their known names, phone numbers, addresses, hours, coordinates, and parent Silwadi Organization. Unsupported ratings, prices, insurance, awards, and outcome claims were deliberately not added.

### 2. Doctor-to-branch authority was normalized

All 15 English and Arabic doctor Profile/Person entities were audited so `worksFor` resolves only to the correct Silwadi branch entities.

Current branch map enforced technically:

| Doctor | Branch authority |
|---|---|
| Dr. Munir Silwadi | Bani Yas + Al Raha |
| Dr. Moheb Silwadi | Al Raha |
| Dr. Hani Hasbini | Bani Yas |
| Dr. Moammar Mohamed Rifai | Bani Yas |
| Dr. Ahmed El Shehri | Bani Yas |
| Dr. Fahed Abi Khalil | Bani Yas |
| Dr. Afnan Mashal | Bani Yas |
| Dr. Krishnamurthy Balajee | Bani Yas + Al Raha |
| Dr. Ehab Hassouneh Bassam A | Al Raha |
| Dr. Sara Ismail | Al Raha |
| Dr. Nasr Keshkiea | Bani Yas |
| Dr. Dana Awad | Bani Yas |
| Dr. Kashmira Pawar Jayprakash | Al Raha |
| Dr. Nachiket Shah | Al Raha |
| Dr. Lana Almasoud | Al Raha |

This is useful because Google can now connect a doctor result to a concrete local Silwadi entity instead of treating the person, clinic, and location as disconnected markup.

### 3. Treatment/service authority was connected to Silwadi

The five public treatment pages in both English and Arabic now connect their `Service` entity to the parent Silwadi Organization and Website:

- Dental Implants
- Orthodontics
- Cosmetic Dentistry
- General Dentistry
- Emergency Dentist

The English and Arabic services hubs also connect the established nine service areas to the same Silwadi entity graph.

No claim was added that a specific treatment is offered at a branch unless current site/doctor data supports it.

### 4. Core page relationships were cleaned up

The About, Doctors, Locations, Contact, Treatments and Services structured data was connected consistently to the Silwadi Website and/or parent Organization where appropriate.

This allows Google to infer the hierarchy:

`Silwadi Dental Center` → `Website` → `Branches / Doctors / Services / Treatments`

rather than seeing many independent JSON-LD objects with inconsistent IDs.

### 5. English/Arabic technical parity was tested

Regression checks cover:
- reciprocal English/Arabic `hreflang`
- self-canonical URLs
- stable doctor branch relationships in both languages
- treatment provider relationships in both languages
- branch entity parity
- sitemap privacy/hygiene

The Arabic pages remain visually unchanged. This pass only touches their technical schema where needed.

### 6. Advertising-risk metadata is guarded

A permanent test now rejects risky metadata language such as:
- `best dentist`
- `best dental`
- `painless`
- `pain-free`
- `top-tier`
- `highest standard`
- guaranteed/predictable outcome wording

The current public metadata passed this check. The test is intended to stop future SEO edits from reintroducing the language accidentally.

### 7. Private pages remain private

No private review URL was added to public navigation or the sitemap. The Pediatric, Endodontics, POD, FAQ and AI FAQ review pages remain unpublished/noindex.

## Canonical, hreflang, sitemap and robots audit

### Canonical / hreflang

The audited English/Arabic public counterparts have reciprocal language alternates and self-canonical URLs. A regression contract now protects this pattern for core pages, the five public treatment pages, and all 15 doctor profiles.

### Sitemap

`https://silwadi.ae/sitemap.xml` already has a strong public-only structure. Tests ensure it does not leak:
- `/review/`
- `/.tmp/`
- `old-silwadi-site`

Duplicate sitemap URLs are also rejected.

### robots.txt

Current configuration is appropriate for the public site:

```text
User-agent: *
Allow: /
Sitemap: https://silwadi.ae/sitemap.xml
```

No robots change was necessary.

## Biggest issue discovered: legacy domain still active

The old `silwadidentalcentres.ae` site is still live and searchable instead of consistently forwarding to `silwadi.ae`.

Examples observed during the audit include:
- old Contact page showing Al Raha Mall as “Coming Soon”
- old doctor directory containing an outdated roster
- old Dr. Ahmed profile using “completely painless” / no-discomfort promises
- old Dr. Moheb profile using “highest standard” / “most advanced” language

This should be fixed at the **old host/domain layer**, not inside the current GitHub Pages site. See:

`docs/seo/legacy-domain-redirect-map-2026-09-13.md`

Google’s official site-move guidance recommends permanent server-side 301/308 redirects and direct one-hop mappings:
- https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes
- https://developers.google.com/search/docs/crawling-indexing/301-redirects

## Google Business Profile plan

Google Business Profile changes require access to the actual listings and are deliberately **not** guessed or silently changed here.

### Bani Yas Tower

Use/verify:
- Business name: `Dr. Munir Silwadi Dental Centre`
- Phone: `+971 2 626 2042`
- Address: Bani Yas Tower, Building 117 C Floor, Sultan Bin Zayed The First St, W Corniche Road, Abu Dhabi, UAE
- Hours: Sun–Wed 09:00–21:00; Thu & Sat 09:00–18:00; Fri closed
- Website: current Silwadi site
- Primary category: verify the existing listing; `Dentist` is the natural general category, but do not overwrite an established category without checking the live Profile and licensing context.

### Al Raha Mall

Use/verify:
- Business name: `Dr. Mohamed Munir Dental Centre - Al Raha Mall`
- Phone: `+971 2 666 2408`
- Address: F14 & F15, Level 1, Al Raha Mall, Channel St, Al Rahah, Abu Dhabi, UAE
- Hours: Sat–Thu 10:00–19:00; Fri closed
- Website: current Silwadi site
- Primary/secondary categories: verify against the actual services and current Google category options rather than inventing categories.

### Important GBP link issue

Google’s current Business Profile policy says that for multi-location businesses, action links should lead to a **dedicated landing page for the specific location**, not a generic landing page or another location.

Official policy:
- https://support.google.com/business/answer/13769188
- https://support.google.com/business/answer/6218037

Silwadi currently has a combined Locations page rather than two dedicated public branch landing pages. Creating dedicated Bani Yas and Al Raha pages could therefore improve both local-intent targeting and Business Profile action-link clarity, but this would be a visible/content project and is **recommendation only until approved**.

## Search Console action list

When access is available, execute in this order:

1. Verify Domain properties for `silwadi.ae` and the legacy `silwadidentalcentres.ae` domain.
2. Submit or refresh `https://silwadi.ae/sitemap.xml`.
3. Inspect/index-check:
   - homepage
   - `/locations.html`
   - `/doctors.html`
   - `/treatments.html`
   - `/services.html`
   - five public treatment pages
4. Inspect representative doctor profiles from both branches, including Dr. Munir, Dr. Lana Almasoud, Dr. Kashmira and a Bani Yas-only doctor.
5. In Pages/Indexing, investigate duplicate/canonical anomalies rather than requesting indexing blindly for every URL.
6. In Performance, monitor impressions/clicks for brand + local/treatment intent groups.
7. After legacy redirects are deployed, inspect representative old URLs and confirm Google detects permanent redirects to the new pages.
8. Use Google’s Change of Address/site-move workflow where available and appropriate for the old domain migration.

## Search-intent ownership map

The objective is one strong Silwadi destination per intent, avoiding multiple pages competing for the same query.

| Search intent | Current/future Silwadi destination |
|---|---|
| dentist Abu Dhabi | `/` |
| dental clinic Abu Dhabi | `/` |
| dentist Bani Yas / dental clinic Bani Yas | `/locations.html` now; dedicated Bani Yas page recommended later |
| dentist Al Raha / Al Raha Mall dentist | `/locations.html` now; dedicated Al Raha page recommended later |
| dental implants Abu Dhabi | `/treatments/dental-implants.html` |
| orthodontist / braces / aligners Abu Dhabi | `/treatments/orthodontics.html` |
| cosmetic dentist / teeth whitening Abu Dhabi | `/treatments/cosmetic-dentistry.html` |
| general dentist Abu Dhabi | `/treatments/general-dentistry.html` |
| emergency dentist Abu Dhabi | `/treatments/emergency-dentist.html` |
| endodontist / root canal Abu Dhabi | private Endodontics review page; **do not target publicly until approved** |
| pediatric dentist Abu Dhabi | private Pediatric review page; **do not target publicly until approved** |
| accessible/POD dental care Abu Dhabi | private POD review page; **do not target publicly until approved** |

## Recommended next actions by impact

### P0 — Legacy-domain 301 migration

Implement the one-to-one redirect map on `silwadidentalcentres.ae`. This is currently the largest authority/consolidation issue.

### P0 — Google Business Profile factual alignment

Check both live Profiles against the exact NAP/hours above. Remove stale status, duplicate locations, wrong phones, old URLs or mismatched hours if present. Do not create unsupported service/category claims.

### P1 — Search Console migration/indexing review

After redirects are live, monitor old-to-new consolidation rather than repeatedly requesting indexing with no migration signal.

### P1 — Dedicated branch landing pages

Consider one high-quality page per physical location. This requires visible design/copy approval, so nothing was created in this pass.

### P1 — Publish vetted specialist pages after approval

Endodontics and Pediatric Dentistry are strong search-intent opportunities because Silwadi has relevant specialists. Their current review pages should be finalized, clinically/compliance checked, and then published only with explicit approval.

### P1 — Publish vetted POD/accessibility page after approval

Useful for accessibility/service discovery and partnership authority, but keep it private until approved.

### P2 — Public FAQ / informational content

Only publish FAQs that are durable, medically cautious, and free of guessed pricing/insurance/schedule claims. Do not revive old-domain FAQ statements blindly.

## Visible opportunities intentionally not implemented

Because this job was explicitly restricted to behind-the-scenes work, the following were not changed:
- headings/body copy
- page layout
- navigation
- colors/fonts/spacing
- doctor cards
- clinic photographs
- page URLs
- dedicated branch pages
- public specialist pages
- public FAQ copy

These should remain separate approval-driven projects.

## What this pass does and does not guarantee

This work improves technical clarity, consistency, crawl interpretation and local entity relationships. It cannot guarantee a particular ranking or ranking date. Search performance also depends on competition, reputation, links/citations, Google Business Profile quality, reviews, content usefulness, and Google’s own systems.

The technical objective is narrower and measurable: when Google crawls Silwadi, it should encounter far less ambiguity about **which organization, branch, doctor, service, language version and URL each page represents**.

## Primary official references

- Google redirects: https://developers.google.com/search/docs/crawling-indexing/301-redirects
- Google site moves: https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes
- Google Business Profile business-link policy: https://support.google.com/business/answer/13769188
- Google Business Profile link management: https://support.google.com/business/answer/6218037
