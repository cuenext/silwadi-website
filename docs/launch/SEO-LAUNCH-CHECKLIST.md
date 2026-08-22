# Silwadi Dental Center — SEO Launch Checklist

Primary launch origin: `https://silwadi.ae`

This checklist is intentionally operational. Do not add search-engine markup or claims that are not visible, verified, and useful to patients.

## Before DNS / hosting cutover

- Confirm `https://silwadi.ae/` serves the production site over a valid HTTPS certificate.
- Pick one hostname as canonical. The site uses the apex host `silwadi.ae`; redirect `www.silwadi.ae` to the apex in one hop.
- Keep the legacy domain `silwadidentalcentres.ae` registered, HTTPS-enabled, and under our control so old URLs can continue to redirect.
- Implement every row in `docs/launch/legacy-redirect-map.csv` as a permanent one-hop 301 redirect. Apply equivalent rules to both legacy apex and `www` hostnames.
- Do not use 302 redirects, JavaScript redirects, or meta refresh for the domain migration.
- Preserve query handling for the old `?lang=en` and `?lang=ar` home URLs; avoid redirect loops or multi-hop chains.
- Confirm unknown/deleted URLs return a genuine HTTP 404 (or 410 when intentionally removed), not a 200 soft-404 page.
- Confirm all 24 canonical URLs return HTTP 200 and no canonical URL redirects internally.
- Confirm `https://silwadi.ae/robots.txt` returns 200 and allows crawling.
- Confirm `https://silwadi.ae/sitemap.xml` returns 200 and contains only the 24 canonical `silwadi.ae` URLs.
- Run `python tools/seo_launch_audit.py` and require `0 errors`.
- Run the full regression suite: `python -m unittest discover -s tests -p '*.py' -v`.
- Run JavaScript syntax validation: `node --check app.js`.

## Structured data and search appearance

- Test the home page, `locations.html`, one doctor profile, and one treatment page in Google's Rich Results Test.
- Confirm JSON-LD matches visible page content and contains no self-authored review or aggregate-rating markup.
- Confirm the home-page favicon is crawlable and remains at the stable `/favicon.svg` URL.
- Confirm canonical, `og:url`, and sitemap URLs all use `https://silwadi.ae` exactly.

## Immediately after launch

- Add/verify the `silwadi.ae` property in Google Search Console.
- Submit `https://silwadi.ae/sitemap.xml` in Google Search Console; do not use deprecated sitemap ping endpoints.
- Use URL Inspection for the home page, doctors directory, treatments directory, locations page, and at least one doctor/treatment detail page. Confirm Google sees the canonical as `silwadi.ae` and request indexing where appropriate.
- Add/verify the site in Bing Webmaster Tools and submit `https://silwadi.ae/sitemap.xml` there.
- Update the website URL in Google Business Profile from the legacy domain to `https://silwadi.ae/` after the new site is publicly reachable.
- Update any other controlled local listings that still link to the legacy domain, prioritizing high-trust profiles and directories.
- Test a representative sample of old indexed URLs (home, doctors, services, contact, and several doctor profiles) and confirm each returns a one-hop 301 to its mapped `silwadi.ae` destination.

## First 7 days

- Review Google Search Console Pages/Indexing and Crawl Stats for unexpected 404, soft 404, redirect, canonical, or blocked-by-robots issues.
- Review Bing Webmaster Tools crawl/index reports for the same migration issues.
- Check server/CDN logs for repeated requests to unmapped legacy PHP paths and add one-to-one redirects where a clear new equivalent exists.
- Verify the legacy domain still resolves and its TLS certificate remains valid; redirect equity is lost if the old host stops responding.
- Check branded searches for the clinic and doctors to ensure the new `silwadi.ae` results begin replacing legacy URLs naturally.

## First 30–90 days

- Keep the legacy domain and SSL active for redirects. Do not cancel the old domain after the first successful crawl; keep redirects available long term.
- Monitor organic clicks/impressions for branded, doctor-name, treatment, emergency-dentist, and Abu Dhabi local-intent queries.
- Fix redirect gaps individually rather than sending unrelated old URLs to the home page.
- Keep business name, phone, address, and hours consistent between the website, Google Business Profile, and other controlled listings.
- When a page receives a significant content/schema/link update, update its sitemap `lastmod` accurately; do not refresh dates for cosmetic-only changes.

## Launch acceptance gate

Launch is accepted only when the static audit and regression suite are green, the 24 canonical URLs are reachable, `robots.txt` and `sitemap.xml` return 200, representative legacy URLs perform one-hop 301 redirects, structured data validates without critical errors, and Search Console/Bing submission steps are completed by the account owner after public deployment.
