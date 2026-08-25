# Patch 20 — UI Polish QA

## Scope

- Removed the top utility strip while keeping the main navigation and contact actions.
- Replaced the unequal three-image homepage treatment strip with compact relevant thumbnails on every visible treatment row.
- Strengthened Google Reviews with clearly gold stars, more visual hierarchy, subtle shadows and restrained hover feedback.
- Prevented `Abu Dhabi` from splitting across lines in primary page headings.
- Removed repeated imagery from the About page; its seven main images are unique.
- Restyled the Services mega-menu as separated frosted/glass cards and removed directional arrows from individual service options.
- Added subtle hover shine/lift and mobile press feedback while preserving `prefers-reduced-motion` behavior.

## Functional verification

Patch 20 contract and the full repository regression suite passed on the tested candidate:

- Patch 20 contract: 7/7
- Full regression suite: 108/108
- JavaScript syntax: pass
- SEO launch audit: 24 pages, 0 errors

## Visual verification

Desktop and mobile screenshots were inspected for:

- homepage header without the utility strip
- homepage treatment rows with thumbnails
- Google Reviews styling and gold stars
- Services desktop mega-menu
- Services mobile menu
- About page unique imagery
- locations heading treatment

## Lighthouse

The final visual matrix passed for Home, Services and About on both desktop and mobile with:

- Performance gate: >= 90
- Accessibility: 100
- Best Practices: 100
- SEO: 100
- Contrast audit: pass
- Target-size audit: pass

Representative results on the final visual candidate:

- Home mobile: Performance 99, Accessibility 100, Best Practices 100, SEO 100, LCP 1.73s, CLS 0.000
- Home desktop: Performance 100, Accessibility 100, Best Practices 100, SEO 100, LCP 0.37s, CLS 0.000
- About mobile diagnostic repeat: Performance 99, LCP 1.8s, TBT 40ms, CLS 0.000

An earlier isolated About-mobile run reported Performance 85, but a diagnostic repeat on the same page scored 99 and the subsequent full visual matrix passed About mobile. No site degradation was introduced for a non-reproducible runner variance.
