# Patch 18 — Services, About & Imagery QA

## Scope

- Added a sitewide **Services** primary navigation tab.
- Added a canonical, image-led `services.html` landing page covering nine dental service areas.
- Added optimized local WebP service imagery and a restrained homepage service-image strip while preserving the approved homepage identity.
- Expanded the About page with Silwadi-specific history, team, clinical scope, locations and relevant imagery.
- Added individual star rows to homepage Google review cards.
- Removed the obsolete **Al Hilal Bank** landmark from visible pages and the local-business source data.
- Kept the detailed treatment directory available for deeper treatment information and SEO discovery.
- Updated the legacy services redirect to the new Services landing page.

## Automated verification

Final Patch 18 candidate verification:

- Patch 18 contract: PASS
- Full Python regression suite: **94 tests, 0 failures**
- JavaScript syntax: PASS (`node --check app.js`)
- SEO launch audit: **24 pages, 0 errors**
- Service images: local optimized WebP assets under the configured size gate

## Lighthouse / visual QA

A Services SEO issue was identified during QA because nine buttons initially used identical visible `Learn More` text. Lighthouse's `link-text` audit scored the page at 92 even when the links had service-specific `aria-label` values. The regression contract was tightened and the visible buttons were changed to service-specific labels such as **“Learn More about Prosthodontics.”**

Post-fix visual verification passed on the final site candidate:

- Fully loaded screenshot capture: PASS
- Home — mobile Lighthouse: PASS
- Home — desktop Lighthouse: PASS
- Services — mobile Lighthouse: PASS
- Services — desktop Lighthouse: PASS
- About — mobile Lighthouse: PASS
- About — desktop Lighthouse: PASS
- Deterministic Accessibility / Best Practices / SEO gates: PASS
- Contrast and target-size gates: PASS

Temporary Patch 18 CI workflows and generation/reconciliation helpers were removed before integration into `main`.

## Launch note

This is pre-launch/local-server verification. Production hosting, redirects, HTTPS, public PageSpeed/Lighthouse and search-engine handoff remain part of the deployment phase.
