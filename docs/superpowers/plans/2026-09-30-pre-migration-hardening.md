# Pre-migration hardening implementation plan

Goal: harden the live GitHub Pages website, repository automation and booking handler while retaining the October 6 hosting cutover.
Architecture: publish an allowlisted static bundle; keep development files in git; enforce validation in PHP rather than trusting browser inputs. Deploy with backups and verify failure cases before legitimate email delivery.
Tech stack: Python bundle checks, GitHub Actions, vanilla JS, PHP 8.2, Apache/LiteSpeed.

- [ ] Enforce HTTPS and verify HTTP redirect without changing DNS.
- [ ] Add public bundle allowlist and security checks. Exclude tests/docs/review/data/dependencies/archive files; verify all page asset links still resolve.
- [ ] Remove tracked dependencies and replace legacy write workflows with read-only build validation. Keep needed generated Arabic build as artifact/check instead of git push.
- [ ] Pin GitHub actions, enable Dependabot/secret protection, require new passing security checks.
- [ ] Audit booking source with sensitive configuration excluded. Reject overlong/invalid field types and values, validate real dates and phones, enforce consent. Preserve existing destination and send behavior. Test invalid requests without mailing clinic.
- [ ] Prepare Tasjeel headers, deny sensitive files, preserve preview Basic auth. CSP report-only first; defer HSTS until HTTPS/cutover stability.
- [ ] Verify English/Arabic live pages, bundle exclusion, TLS, booking response, GitHub restrictions. Record provider/mail/access limitations.

Constraints: no DNS cutover, no private repo conversion while Pages is live, no patient records in repo, no forced history rewrite. Independent reviewer approvals require a real second maintainer; do not self-approve or block the sole maintainer.
