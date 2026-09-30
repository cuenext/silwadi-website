# Tasjeel production security configuration

Status: prepared; not installed or verified on Tasjeel. DNS cutover remains October 6.

Use `static-security.htaccess` only for the static frontend document root. The booking API has its own separate hardened configuration. The public bundle excludes this directory and will not automatically activate the snippet.

Before installation:
1. Back up the existing document root and .htaccess outside the public directory.
2. Confirm Apache-compatible rewrite, headers, authorization and Options support.
3. Merge the snippet into the protected preview configuration; preserve its Basic Auth and cPanel certificate rules.
4. Test English and Arabic pages, doctors, About accreditation content, CSS/fonts/images/video, maps, mobile navigation and the booking modal.
5. Verify response headers on both successful pages and errors; confirm sensitive files are denied and directories cannot be listed.
6. Inspect the report-only CSP console violations. The enforced policy currently blocks plugins, foreign base URLs and embedding; it does not yet provide a strict script allowlist.
7. Restore the backed-up .htaccess immediately on a 500 response or broken site behavior.

On October 6, install only after the hostname certificate is valid and perform the agreed backup/maintenance/DNS migration checks. Promote the temporary HTTPS redirect to 301 only after stable operation. Add HSTS cautiously after every relevant hostname is verified; do not preemptively add includeSubDomains or preload.

Outstanding external verification:
- A successful PHP mail call is not proof of inbox delivery. Test the reception inbox with a clearly marked synthetic appointment, with authorization for the recipient and no patient data.
- Obtain provider evidence for server, backup and email locations; a UAE company address does not prove UAE data residency.
- Keep patient-facing AI disabled until the processing requirement is resolved.

References:
- https://httpd.apache.org/docs/2.4/mod/mod_headers.html
- https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html
