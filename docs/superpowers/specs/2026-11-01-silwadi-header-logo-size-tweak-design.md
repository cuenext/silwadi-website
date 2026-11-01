# Silwadi Header Logo Size Tweak

## Intent

Make the newly published official Silwadi logo feel slightly less dominant in website headers, matching the user's screenshot feedback, while leaving the approved artwork and footer presentation unchanged.

## Goals

- Reduce every production header-logo image from 82px to 74px on desktop and from 72px to 65px on mobile.
- Keep the existing header wrappers and header heights unchanged so navigation does not shift.
- Apply the same size to standard English/Arabic pages, homepages, treatment shells, page-local treatment headers, and the FAQ/AI shell.
- Keep footer logos at 128px and preserve the transparent SVG, natural 259:225 ratio, and localized alt text.

## Non-goals and anti-goals

- Do not edit the official PNG or SVG.
- Do not resize footer logos.
- Do not change navigation spacing, header height, page content, metadata, or the private review page.
- Do not create a page-specific exception that makes the brand inconsistent.

## Approaches

1. **Reduce only the logo image width (selected).** This produces the requested subtle change without moving navigation or changing the header frame.
2. Reduce both the logo image and its wrapper. This would reclaim space but would also shift navigation and make the change more noticeable than requested.
3. Change only the homepage. This would match the screenshot but leave doctor, treatment, Arabic, and FAQ headers inconsistent.

## Implementation scope

Update the shared, homepage, treatment-shell, and six page-local header rules to 74px desktop and 65px mobile. Extend the existing logo production contract test first so it fails on the current 82px/72px values and continues asserting that footer logos remain 128px.
