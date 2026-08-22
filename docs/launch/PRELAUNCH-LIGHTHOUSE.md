# Pre-launch Lighthouse Audit

Run date: 2026-08-22
Source commit: `b652caa1116c6c603688dc61fdf8e2150efa9604`
Environment: GitHub Actions Ubuntu runner, Chrome headless, Lighthouse CLI against the local static Patch 12 build.

> These are pre-launch lab scores. Production hosting, caching, TLS, CDN and network delivery can change performance, so rerun against `https://silwadi.ae` after deployment.

## Scores and Core Web Vitals lab metrics

| Page | Mode | Perf | A11y | Best Practices | SEO | FCP | LCP | TBT | CLS |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Home | Mobile | 94 | 90 | 100 | 100 | 1.1 s | 2.0 s | 270 ms | 0 |
| Home | Desktop | 100 | 89 | 100 | 100 | 0.3 s | 0.4 s | 0 ms | 0 |
| Doctors | Mobile | 99 | 91 | 100 | 100 | 1.1 s | 2.3 s | 0 ms | 0 |
| Doctors | Desktop | 100 | 91 | 100 | 100 | 0.3 s | 0.5 s | 0 ms | 0 |
| Dr. Munir profile | Mobile | 100 | 91 | 100 | 100 | 0.9 s | 1.7 s | 0 ms | 0 |
| Dr. Munir profile | Desktop | 100 | 90 | 100 | 100 | 0.2 s | 0.4 s | 0 ms | 0 |
| Treatments | Mobile | 100 | 90 | 100 | 100 | 0.9 s | 1.5 s | 0 ms | 0 |
| Treatments | Desktop | 100 | 89 | 100 | 100 | 0.2 s | 0.4 s | 0 ms | 0 |
| Dental Implants | Mobile | 82 | 90 | 100 | 100 | 0.9 s | 5.0 s | 0 ms | 0 |
| Dental Implants | Desktop | 99 | 90 | 100 | 100 | 0.2 s | 0.9 s | 0 ms | 0 |
| Locations | Mobile | 100 | 91 | 100 | 100 | 0.9 s | 1.5 s | 0 ms | 0 |
| Locations | Desktop | 100 | 91 | 100 | 100 | 0.5 s | 0.5 s | 0 ms | 0 |
| Contact | Mobile | 100 | 91 | 100 | 100 | 0.9 s | 1.5 s | 0 ms | 0 |
| Contact | Desktop | 100 | 90 | 100 | 100 | 0.5 s | 0.5 s | 0 ms | 0 |

## Average category scores

- **Mobile** — Performance 96.4, Accessibility 90.6, Best Practices 100.0, SEO 100.0.
- **Desktop** — Performance 99.9, Accessibility 90.0, Best Practices 100.0, SEO 100.0.

## Audits worth reviewing

### Home — Mobile
Performance:
- Total Blocking Time (score 0.82) — 270 ms
- Network dependency tree (score 0.00)
- Max Potential First Input Delay (score 0.66) — 200 ms
Accessibility / Best Practices / SEO:
- Background and foreground colors do not have a sufficient contrast ratio. (score 0.00)
- Touch targets do not have sufficient size or spacing. (score 0.00)

### Home — Desktop
Performance:
- Network dependency tree (score 0.00)
Accessibility / Best Practices / SEO:
- Background and foreground colors do not have a sufficient contrast ratio. (score 0.00)
- Touch targets do not have sufficient size or spacing. (score 0.00)

### Doctors — Mobile
Performance:
- Network dependency tree (score 0.00)
Accessibility / Best Practices / SEO:
- Background and foreground colors do not have a sufficient contrast ratio. (score 0.00)
- Touch targets do not have sufficient size or spacing. (score 0.00)

### Doctors — Desktop
Performance:
- LCP request discovery (score 0.00)
- Network dependency tree (score 0.00)
Accessibility / Best Practices / SEO:
- Background and foreground colors do not have a sufficient contrast ratio. (score 0.00)
- Touch targets do not have sufficient size or spacing. (score 0.00)

### Dr. Munir profile — Mobile
Performance:
- Network dependency tree (score 0.00)
Accessibility / Best Practices / SEO:
- Background and foreground colors do not have a sufficient contrast ratio. (score 0.00)
- Touch targets do not have sufficient size or spacing. (score 0.00)

### Dr. Munir profile — Desktop
Performance:
- Network dependency tree (score 0.00)
Accessibility / Best Practices / SEO:
- Background and foreground colors do not have a sufficient contrast ratio. (score 0.00)
- Touch targets do not have sufficient size or spacing. (score 0.00)

### Treatments — Mobile
Performance:
- Network dependency tree (score 0.00)
Accessibility / Best Practices / SEO:
- Background and foreground colors do not have a sufficient contrast ratio. (score 0.00)
- Touch targets do not have sufficient size or spacing. (score 0.00)

### Treatments — Desktop
Performance:
- Network dependency tree (score 0.00)
Accessibility / Best Practices / SEO:
- Background and foreground colors do not have a sufficient contrast ratio. (score 0.00)
- Touch targets do not have sufficient size or spacing. (score 0.00)

### Dental Implants — Mobile
Performance:
- Largest Contentful Paint (score 0.27) — 5.0 s
- Network dependency tree (score 0.00)
- Time to Interactive (score 0.77) — 5.0 s
Accessibility / Best Practices / SEO:
- Background and foreground colors do not have a sufficient contrast ratio. (score 0.00)
- Touch targets do not have sufficient size or spacing. (score 0.00)

### Dental Implants — Desktop
Performance:
- Forced reflow (score 0.00)
- Network dependency tree (score 0.00)
Accessibility / Best Practices / SEO:
- Background and foreground colors do not have a sufficient contrast ratio. (score 0.00)
- Touch targets do not have sufficient size or spacing. (score 0.00)

### Locations — Mobile
Performance:
- Network dependency tree (score 0.00)
Accessibility / Best Practices / SEO:
- Background and foreground colors do not have a sufficient contrast ratio. (score 0.00)
- Touch targets do not have sufficient size or spacing. (score 0.00)

### Locations — Desktop
Performance:
- Network dependency tree (score 0.00)
Accessibility / Best Practices / SEO:
- Background and foreground colors do not have a sufficient contrast ratio. (score 0.00)
- Touch targets do not have sufficient size or spacing. (score 0.00)

### Contact — Mobile
Performance:
- Network dependency tree (score 0.00)
Accessibility / Best Practices / SEO:
- Background and foreground colors do not have a sufficient contrast ratio. (score 0.00)
- Touch targets do not have sufficient size or spacing. (score 0.00)

### Contact — Desktop
Performance:
- Network dependency tree (score 0.00)
- Page prevented back/forward cache restoration (score 0.00) — 1 failure reason
Accessibility / Best Practices / SEO:
- Background and foreground colors do not have a sufficient contrast ratio. (score 0.00)
- Touch targets do not have sufficient size or spacing. (score 0.00)

## Interpretation

- Performance scores are lab measurements, not a promise of production Core Web Vitals.
- Accessibility, Best Practices and SEO scores are automated checks and do not replace manual clinical/content/accessibility review.
- The production Lighthouse rerun after DNS/hosting cutover is the launch-signoff measurement.
