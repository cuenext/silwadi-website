# Brand and branch location SEO Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Strengthen the exact established homepage brand and correct verified branch coordinates in emitted structured data.

**Architecture:** Change only homepage title/description and WebSite alternate names, plus the two branch GeoCoordinates. Update the existing branch factory and checked-in public HTML; avoid regenerating complete pages because production and Arabic work have independent changes.

**Tech Stack:** Static HTML, existing Python schema helpers and unittest.

**Spec:** Parent task dated 2026-10-26: title `Dr. Munir Silwadi Dental Centre | Dentist in Abu Dhabi`; coordinates Corniche 24.4935218, 54.3610125 and Al Raha 24.4388317, 54.5744795, verified from primary Google Maps data in the sibling live-audit captures.

## Global Constraints

- Preserve shared entity IDs, organization legal names, phone/address/hours, maps embeds, booking and body content.
- No redirect, live hosting, GitHub push/PR/merge or synced sources changes.
- Fresh live patches must preserve all bytes outside targeted metadata/schema. Parent confirmed the parallel graph workflow stopped and authorized all ten live files after fresh hash verification.

## Review Focus

- Branch IDs must select the correct coordinate pair in EN/AR and factory output.
- Original phone/address/hours and shared IDs must remain unchanged.
- Homepage exact brand must survive metadata regeneration and match its Open Graph title.
- Live-only assistant, accreditation and Arabic graph work must survive patch preparation.
- Live patches must include only the allowed metadata/geo changes, with original hashes and rollback files.

### Task 1: Source correction

**Files:** `tests/test_branch_geo.py`, `scripts/apply_google_authority.py`, `index.html`, `ar/index.html`, EN/AR `contact.html`, `locations.html`, `locations/corniche.html`, `locations/al-raha.html`.

- [x] Add semantic tests of real branch factory output and public JSON-LD branch identities/coordinates, including phone/address/hours guards. Add homepage structured site alternate-name checks.
- [x] Run tests and record expected failures from wrong coordinates/missing alternate names.
- [x] Update only coordinates in the factory and affected HTML JSON-LD; update EN homepage title, matching Open Graph title/description, and EN/AR WebSite alternate names. Preserve organization legal names and all other data.
- [x] Run new tests, relevant existing SEO/publication tests, static SEO audit, and compare the full Python suite's failure names against the known same-day baseline.

### Task 2: Live patch preparation and review

**Files:** Sibling `brand-location-deploy/` originals, patched HTML, semantic evidence, SHA manifest and report; no upload.

- [x] Fetch affected production pages fresh using public GET requests.
- [x] Patch only approved metadata or numeric geo values; prove bytes outside those fields and all unrelated parsed schema data remain identical.
- [x] Coordinate AR contact/locations live artifacts with parent; all ten files authorized after the other workflow stopped. Fresh production preflight hashes all match.
- [x] Request independent review of source and live patch artifacts, record findings and deliver exact paths/tests/limitations to parent. Parent reports source review clean; final source also includes the separately reviewed redirect sample patch, preserving the existing exact alias.
