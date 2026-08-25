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

Latest Patch 18 verification before final visual gate:

- Patch 18 contract: PASS
- Full Python regression suite: **94 tests, 0 failures**
- JavaScript syntax: PASS (`node --check app.js`)
- SEO launch audit: **24 pages, 0 errors**
- Service images: local optimized WebP assets under the configured size gate

## Lighthouse / visual QA

Home and About passed the desktop/mobile deterministic Lighthouse gates during Patch 18 visual QA. A Services SEO issue was identified in the `link-text` audit because nine buttons used identical visible text. The regression contract was tightened and the Services links were changed to visible, service-specific labels such as **“Learn More about Prosthodontics.”**

Final desktop/mobile Home, Services and About visual/Lighthouse verification is run on the post-fix candidate before merge.

## Launch note

This is pre-launch/local-server verification. Production hosting, redirects, HTTPS, public PageSpeed/Lighthouse and search-engine handoff remain part of the deployment phase.
