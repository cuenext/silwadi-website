# Legacy Domain Redirect Plan — silwadidentalcentres.ae → silwadi.ae

Date: 2026-09-13

## Priority

**P0 / highest-impact external SEO action.** The previous domain `silwadidentalcentres.ae` is still serving indexable HTML instead of consistently forwarding visitors and search engines to `silwadi.ae`. Current search results still expose the old homepage, doctors, services, contact information, and doctor-detail pages.

This matters for three reasons:

1. It splits brand/domain authority between the old and new websites.
2. It leaves stale information in search, including the old contact page showing the Al Raha Mall location as “Coming Soon”.
3. Some legacy copy uses claims that should not represent the current Silwadi advertising standard, including phrases such as “completely painless”, “highest standard”, and other superiority/outcome language.

Google recommends server-side **301 or 308 permanent redirects** for permanent moves and recommends redirecting old URLs directly to the final corresponding destination rather than through chains.

Official guidance:
- https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes
- https://developers.google.com/search/docs/crawling-indexing/301-redirects

## Required one-to-one redirect map

| Legacy URL path | Destination on silwadi.ae | Status |
|---|---|---|
| `/` | `https://silwadi.ae/` | 301 |
| `/index.php` | `https://silwadi.ae/` | 301 |
| `/doctors.php` | `https://silwadi.ae/doctors.html` | 301 |
| `/services.php` | `https://silwadi.ae/services.html` | 301 |
| `/about-us.php` | `https://silwadi.ae/about.html` | 301 |
| `/contact-us.php` | `https://silwadi.ae/contact.html` | 301 |
| `/doctors-details/dr-mohamed-munir-juma-mousa.php` | `https://silwadi.ae/doctors/dr-munir-silwadi.html` | 301 |
| `/doctors-details/dr-moheb-silwadi.php` | `https://silwadi.ae/doctors/dr-moheb-silwadi.html` | 301 |
| `/doctors-details/dr-hani-bahijie-hasbini.php` | `https://silwadi.ae/doctors/dr-hani-hasbini.html` | 301 |
| `/doctors-details/dr-moammar-rifai.php` | `https://silwadi.ae/doctors/dr-moammar-rifai.html` | 301 |
| `/doctors-details/dr-ahmed-farouk-ghel.php` | `https://silwadi.ae/doctors/dr-ahmed-el-shehri.html` | 301 |
| `/doctors-details/dr-fahd-elia-abi-khalil.php` | `https://silwadi.ae/doctors/dr-fahed-khalil.html` | 301 |
| `/doctors-details/dr-afnan-ibrahim-mohamed-mashal.php` | `https://silwadi.ae/doctors/dr-afnan-mashal.html` | 301 |
| `/doctors-details/Dr-Krishnamurthy-Katta-Balajee.php` | `https://silwadi.ae/doctors/dr-krishnamurthy-katta-balajee.html` | 301 |

### Legacy doctors no longer represented on the current website

The old doctors directory still lists doctors who are not in the current 15-doctor Silwadi roster. Their old detail URLs should **not** be mapped to an unrelated current doctor. If a directly equivalent current profile does not exist, redirect the retired doctor-detail URL to:

`https://silwadi.ae/doctors.html`

This is a deliberate fallback only for obsolete staff pages. Where a true one-to-one replacement exists, use that specific doctor profile instead.

### FAQ and insurance URLs require a deliberate content decision

Do **not** redirect legacy FAQ or insurance URLs to the current private review pages. Those review pages are intentionally unpublished/noindex.

- `/faq.php`: keep available temporarily or redirect to `https://silwadi.ae/contact.html` only if the legacy FAQ is intentionally being retired. When the vetted public FAQ is approved, map the legacy FAQ directly to that public URL.
- Any legacy insurance page: do not imply current insurer participation. Redirect only after reception/management confirms the public destination and current insurance information.

## Apache example

If the old host uses Apache, the exact implementation can be placed in the old domain VirtualHost or `.htaccess`. Use one-hop redirects to the final HTTPS destinations.

```apache
RewriteEngine On

RewriteRule ^$ https://silwadi.ae/ [R=301,L]
RewriteRule ^index\.php$ https://silwadi.ae/ [R=301,L]
RewriteRule ^doctors\.php$ https://silwadi.ae/doctors.html [R=301,L]
RewriteRule ^services\.php$ https://silwadi.ae/services.html [R=301,L]
RewriteRule ^about-us\.php$ https://silwadi.ae/about.html [R=301,L]
RewriteRule ^contact-us\.php$ https://silwadi.ae/contact.html [R=301,L]

RewriteRule ^doctors-details/dr-mohamed-munir-juma-mousa\.php$ https://silwadi.ae/doctors/dr-munir-silwadi.html [R=301,L,NC]
RewriteRule ^doctors-details/dr-moheb-silwadi\.php$ https://silwadi.ae/doctors/dr-moheb-silwadi.html [R=301,L,NC]
RewriteRule ^doctors-details/dr-hani-bahijie-hasbini\.php$ https://silwadi.ae/doctors/dr-hani-hasbini.html [R=301,L,NC]
RewriteRule ^doctors-details/dr-moammar-rifai\.php$ https://silwadi.ae/doctors/dr-moammar-rifai.html [R=301,L,NC]
RewriteRule ^doctors-details/dr-ahmed-farouk-ghel\.php$ https://silwadi.ae/doctors/dr-ahmed-el-shehri.html [R=301,L,NC]
RewriteRule ^doctors-details/dr-fahd-elia-abi-khalil\.php$ https://silwadi.ae/doctors/dr-fahed-khalil.html [R=301,L,NC]
RewriteRule ^doctors-details/dr-afnan-ibrahim-mohamed-mashal\.php$ https://silwadi.ae/doctors/dr-afnan-mashal.html [R=301,L,NC]
RewriteRule ^doctors-details/Dr-Krishnamurthy-Katta-Balajee\.php$ https://silwadi.ae/doctors/dr-krishnamurthy-katta-balajee.html [R=301,L,NC]
```

The old host must also normalize `www.silwadidentalcentres.ae`, non-`www`, HTTP, and HTTPS so every old variant reaches the **final** `https://silwadi.ae/...` destination in one redirect wherever technically possible.

## NGINX example

```nginx
server {
    listen 80;
    listen 443 ssl;
    server_name silwadidentalcentres.ae www.silwadidentalcentres.ae;

    location = / { return 301 https://silwadi.ae/; }
    location = /index.php { return 301 https://silwadi.ae/; }
    location = /doctors.php { return 301 https://silwadi.ae/doctors.html; }
    location = /services.php { return 301 https://silwadi.ae/services.html; }
    location = /about-us.php { return 301 https://silwadi.ae/about.html; }
    location = /contact-us.php { return 301 https://silwadi.ae/contact.html; }

    location = /doctors-details/dr-mohamed-munir-juma-mousa.php { return 301 https://silwadi.ae/doctors/dr-munir-silwadi.html; }
    location = /doctors-details/dr-moheb-silwadi.php { return 301 https://silwadi.ae/doctors/dr-moheb-silwadi.html; }
    location = /doctors-details/dr-hani-bahijie-hasbini.php { return 301 https://silwadi.ae/doctors/dr-hani-hasbini.html; }
    location = /doctors-details/dr-moammar-rifai.php { return 301 https://silwadi.ae/doctors/dr-moammar-rifai.html; }
    location = /doctors-details/dr-ahmed-farouk-ghel.php { return 301 https://silwadi.ae/doctors/dr-ahmed-el-shehri.html; }
    location = /doctors-details/dr-fahd-elia-abi-khalil.php { return 301 https://silwadi.ae/doctors/dr-fahed-khalil.html; }
    location = /doctors-details/dr-afnan-ibrahim-mohamed-mashal.php { return 301 https://silwadi.ae/doctors/dr-afnan-mashal.html; }
    location = /doctors-details/Dr-Krishnamurthy-Katta-Balajee.php { return 301 https://silwadi.ae/doctors/dr-krishnamurthy-katta-balajee.html; }
}
```

## Deployment verification

For each mapped URL, verify:

```bash
curl -I https://silwadidentalcentres.ae/contact-us.php
```

Expected:
- status `301` or `308`
- `Location: https://silwadi.ae/contact.html`
- no intermediate destination or chain

Repeat for the homepage, core pages, and every mapped doctor profile. Keep the old domain registered and its hosting/edge configuration alive long enough to serve the redirects reliably; do not simply let the old domain expire.

## Search Console after redirect deployment

1. Verify ownership of the old and new domains/properties.
2. Submit/refresh `https://silwadi.ae/sitemap.xml` in the new property.
3. Use Google’s site-move/Change of Address workflow where available and applicable.
4. Inspect representative old URLs and confirm Google sees the permanent redirect.
5. Monitor Indexing/Pages and Performance for the old-domain URLs declining while corresponding `silwadi.ae` URLs consolidate.
6. Do not remove the redirects after only a few weeks; domain migrations need durable redirects.

## Evidence observed during this audit

At audit time Google/web search still surfaced live legacy pages, including:
- `https://silwadidentalcentres.ae/contact-us.php` with Al Raha labelled “Coming Soon”.
- `https://silwadidentalcentres.ae/doctors.php` with an outdated doctor roster.
- `https://silwadidentalcentres.ae/doctors-details/dr-ahmed-farouk-ghel.php` containing “completely painless” / no-discomfort outcome language.
- `https://www.silwadidentalcentres.ae/doctors-details/dr-moheb-silwadi.php` containing “highest standard” / “most advanced” promotional language.

This redirect project should therefore be treated as both an SEO consolidation task and a current-information/compliance cleanup.
