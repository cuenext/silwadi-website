# Silwadi logo-size cache-bust plan

## Goal

Ensure existing visitors receive the newly published header-logo sizing despite the host's seven-day CSS cache lifetime.

## Scope

- Use one release token: `20261101-logo-size`.
- Version every production HTML reference to `styles.css`, `home-reviews.css`, and `treatments/treatment-refresh-v1.css`.
- Preserve relative/absolute paths, page content, logo assets, header geometry, and footer sizing.
- Leave the two endodontics pages that own their logo rules inline unchanged.

## Verification

1. Add a failing contract that inventories all 67 relevant stylesheet links across 65 HTML pages.
2. Update only those link URLs and make the contract pass.
3. Run the available 15-test Node suite, independent review, and all GitHub checks.
4. Deploy the validated merged artifact with a separate backup and verify a normal live load computes the header at 74 px desktop / 65 px mobile while the footer remains 128 px.
