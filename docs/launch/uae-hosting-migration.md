# UAE hosting migration: preparation and gates

Status: preparation only. The live `silwadi.ae` site is served by GitHub Pages. Do not change DNS or upload this repository directly to a web root.

The clinic approved using its existing Tasjeel hosting even if its physical server location is not confirmed. This does not establish UAE data residency. The DNS cutover is reserved for the 6 October maintenance window; do not take down the live site before then.

## Verified inventory (28 September 2026)

- Tasjeel account product: `cPanel Web Hosting - Single Site`, active, annually billed. This is distinct from the provider's separately advertised `Dubai Hosting` product. The current server location is not verified.
- cPanel has `/home/silwadia/booking.silwadi.ae/booking-submit.php` and a separate `public_html` directory with an older site copy, scripts, and `silwadi-website-main.zip`.
- The booking script sends appointment details through PHP `mail()` to an address under `silwadidentalcentre.ae`. No corresponding mailbox exists in this cPanel account. Verify the recipient mail system, routing, retention, backup, and location before claiming end-to-end UAE residency.
- The booking handler limits JSON size, checks exact origins, rate limits by hashed remote IP in the PHP temporary directory, validates email, escapes HTML, and strips CR/LF from the subject. It does not validate the enumerated treatment/time/clinic values, date format, or phone format, and it truncates long values rather than rejecting them. The form's consent checkbox is not sent to the handler. Review these together before changing the live endpoint.
- A 248-file public-only site package was extracted to `/home/silwadia/silwadi-staging-20260928/` outside `public_html`. This is a private preparation area, not an independently tested staging website.
- The current GitHub Pages site publicly serves `review/` pages, `docs/` Markdown and `tests/` files from the repository root. This is a verified information exposure, not evidence of server compromise. Remove those paths from the published website and review repo history before claiming the exposure is resolved.

## Prepare the destination

1. Ask Tasjeel to confirm in writing the current package's server and backup locations. The move may proceed on the existing package, but do not claim UAE residency without that answer. Confirm SFTP/SSH access, PHP version, static site document root, SSL, and backup retention.
2. Verify the booking email service and DNS MX records. Decide whether the appointment destination will remain there and document its data handling. Do not move mailbox routing as a side effect of the website cutover.
3. Set up the Dubai host under a staging hostname with HTTPS. Keep the booking endpoint working until the replacement passes tests.
4. Generate the public files using `python tools/public_bundle.py /path/outside/repo/public-bundle`. This copies only allowlisted static pages and media; it omits repository internals, AI review data, dependencies, archives, and scripts used for development. Inspect the bundle and check local asset links before upload.
5. Configure the new web server to disable indexes, refuse dotfiles, backups, source archives and scripts, and set suitable HTTPS and security headers. Test a Content Security Policy in report-only mode first; the existing site includes inline scripts/styles and third-party resources.
6. Create narrowly scoped, key-based SFTP deployment access. Store its credentials as GitHub Actions secrets after reviewing the exact destination. A workflow should publish the public bundle only after the site build and regression checks pass. It should not have permission to write repository content.

## Cutover gate

During the approved maintenance window: capture backups of DNS, old site, booking script and mail settings; stage and test both languages, mobile, images, booking response and delivery; switch only the web records; verify TLS, redirects and external links; monitor errors and have the prior DNS values ready for rollback. HSTS should follow a stable verified HTTPS period, not precede it.

Do not enable the public AI feature as part of this migration until its processing location and the clinic's audit requirement are reconciled.
