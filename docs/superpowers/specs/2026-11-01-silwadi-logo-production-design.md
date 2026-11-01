# Silwadi Logo Production Design

## Intent

Replace the stretched/near-square site logo with the exact 259 × 225 Silwadi artwork the user supplied and approved on the local review page. The real header and footer should match that preview on desktop, mobile, English, Arabic, and the FAQ shell, with no visible white image box.

## Goals

- Preserve the supplied artwork byte-for-byte; do not redraw or reshape the mark or wordmark.
- Use the approved natural 259:225 ratio, 82 px desktop header width, 72 px mobile header width, and 128 px footer width.
- Remove the near-white matte visually on site surfaces without relying on multiply blending.
- Update every production header/footer placement, including embedded English/Arabic FAQ templates.
- Retain a raster PNG at the established URL for Open Graph, schema, and other non-browser consumers.

## Non-goals and constraints

- Do not copy or publish the review page.
- Do not deploy or push the change.
- Do not alter navigation, copy, localized alt text, metadata routing, or unrelated imagery.
- Do not add a runtime dependency or external image request.

## Approaches considered

1. **Self-contained filtered SVG (selected).** Embed the exact PNG bytes in one SVG and apply the already-approved near-white alpha key. This preserves the approved appearance, works as a shared static `<img>` asset, and avoids external-resource restrictions inside image-mode SVGs.
2. **Regenerated transparent bitmap.** Rejected because the trial redraw changed the wordmark and line weight instead of preserving the supplied artwork.
3. **CSS blend mode over the opaque PNG.** Rejected because it depends on the background color and changes the logo's colors; it also does not provide the approved transparent treatment.

## Implementation shape

- `assets/silwadi-logo-official.png` becomes the exact supplied raster for social/schema compatibility.
- `assets/silwadi-logo-official.svg` embeds that PNG as a data URI, uses `viewBox="0 0 259 225"`, and applies the approved filter within fixed user-space bounds.
- Visible production logo `<img>` elements use the SVG and intrinsic dimensions `259` × `225`.
- Shared and page-specific logo CSS adopts the approved natural ratio and sizes, with `mix-blend-mode: normal`.
- A Node contract test verifies source identity, safe self-containment, production coverage, metadata stability, and sizing rules.

## Acceptance

The existing test suite and the new logo contract pass. Browser review of representative English, Arabic, nested, FAQ, desktop, and mobile pages shows the approved logo without a white box, distortion, overflow, or missing placements.
