# Patch 13 — Lighthouse Polish QA

Date: 2026-08-22

## Result

Patch 13 addresses the confirmed pre-launch Lighthouse issues without redesigning the site: the Dental Implants provider portrait transfer cost, low-contrast small text, and undersized footer touch targets.

## Regression and launch checks

Fresh GitHub Actions regression run on the verified Patch 13 production blobs:

- Python regression suite: **60/60 tests passed**
- JavaScript syntax: **PASS** (`node --check app.js`)
- SEO launch audit: **24 pages, 0 errors**
- Internal references: **874 local references, 0 broken**
- JSON-LD: **24 blocks, 0 errors**
- Local HTTP smoke: **29/29 returned 200**

## Lighthouse deterministic matrix

A 14-job Lighthouse matrix covered seven representative pages in both mobile and desktop modes:

- Home
- Doctors directory
- Dr. Munir Silwadi profile
- Treatments directory
- Dental Implants
- Locations
- Contact

**14/14 jobs passed** the deterministic release gate:

- Accessibility: **100 required**
- Best Practices: **100 required**
- SEO: **100 required**
- Color contrast: **PASS required**
- Target size: **PASS required when applicable**

Performance scores were recorded but were not treated as a deterministic single-run pass/fail because CI CPU/network throttling caused material score variance between otherwise identical runs.

## Dental Implants performance repeat

Patch 12 baseline diagnostic on Dental Implants mobile:

- Median Lighthouse Performance: **82**
- Median LCP: **4.95 s**
- Largest transferred resource: original Dr. Munir PNG, about **635.9 KB**

Patch 13 repeated mobile Lighthouse runs after replacing that rendered PNG with the optimized WebP and lazy-loading the below-the-fold provider portrait:

| Run | Performance | Accessibility | Best Practices | SEO | LCP | TBT | CLS |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 99 | 100 | 100 | 100 | 1.7 s | 10 ms | 0 |
| 2 | 100 | 100 | 100 | 100 | 1.7 s | 0 ms | 0 |
| 3 | 100 | 100 | 100 | 100 | 1.7 s | 0 ms | 0 |

- Median Performance: **100**
- Median LCP: **1.73 s**
- LCP reduction versus the Patch 12 diagnostic baseline: **about 65%**

## Accessibility fixes verified by Lighthouse

- Shared muted text was darkened enough to clear WCAG AA on the site's quiet/off-white surfaces.
- Home shortcut indices/descriptions, legacy seal text, treatment indices, footer text, and muted location status were brought above the contrast threshold.
- Treatments section indices and Contact channel indices now use the accessible shared muted neutral.
- The Locations preview link selector is scoped so it no longer overrides white text on primary buttons.
- Footer navigation links now provide at least a 24 px target height.

## Image fix

`treatments/dental-implants.html` now renders:

- `assets/doctors/optimized/dr-munir-silwadi.webp`
- explicit `width="720"` and `height="720"`
- `loading="lazy"`
- `decoding="async"`

The original PNG remains in the repository as a source asset but is no longer rendered by public HTML.

## Measurement note

These Lighthouse measurements were run in GitHub Actions against a local static HTTP server. They are valid pre-launch regression evidence, but production Lighthouse / PageSpeed should be rerun after the public deployment because hosting, TLS, caching, third-party resources, and network conditions can change field performance.
