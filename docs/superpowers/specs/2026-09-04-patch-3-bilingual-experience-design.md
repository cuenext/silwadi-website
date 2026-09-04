# Patch 3: Arabic and bilingual experience

**Status:** Approved for implementation by the site owner on 2026-09-04
**Baseline:** Patch 2 merge (`7f34cb6bd1915d37df8d3cfcec322da2362ca9c5`)

## Goal

Make Arabic a dependable, patient-facing version of the Silwadi site rather than a translation overlay that disappears when a visitor follows a link.

## Scope

1. Treat an explicit `?lang=ar` or `?lang=en` query value as the page-level language choice, with the existing `localStorage` preference as the fallback.
2. Add the active language to same-origin page links while Arabic is selected, preserving hashes and relative paths so navigation, service anchors, doctor profiles and the consultation route stay usable.
3. Keep the preference after a language toggle by updating the current URL without a page reload and by dispatching the existing `silwadi:languagechange` event.
4. Complete the Arabic dictionary for Patch 2 service/treatment copy, booking labels, navigation controls and page-level status text using concise clinic language.
5. Translate user-facing `placeholder`, `aria-label`, `title` and image `alt` attributes when a verified dictionary entry exists; restore the original value when English is selected.
6. Update document language/direction and add localized title/description/Open Graph values for the current static pages without changing clean canonical URLs.
7. Add lightweight RTL layout rules for navigation, forms, cards, controls and consultation actions, including mobile overflow protection and readable Arabic line lengths.

## Non-goals

- No new CMS, framework or runtime dependency.
- No generated or face-altered imagery.
- No change to the English copy, service taxonomy, booking mail destination or cPanel deployment.
- No claim that dynamically injected metadata alone replaces Search Console or server-side language routing; the clean canonical URL remains the source of truth.

## User experience

- Clicking `عربي` changes the current page immediately to Arabic, changes the button to `English`, sets `dir="rtl"`, and records the choice.
- Following any internal page link while Arabic is active opens the same page with `?lang=ar`; the next page therefore renders Arabic on first initialization rather than relying only on an old tab state.
- Clicking `English` removes the language query and stores English. Existing clean URLs remain valid.
- External, telephone, email, download, asset and same-page hash links are never given a language query.
- Arabic uses the existing IBM Plex Sans Arabic/Noto Kufi Arabic fonts and right-to-left alignment, but English names, phone numbers, email addresses and clinical abbreviations retain their readable direction.

## SEO and accessibility

- Canonical URLs stay clean (`https://silwadi.ae/<path>.html`).
- The controller updates `html[lang]`, `html[dir]`, the document title, description, Open Graph title/description and `content-language` for the visible language.
- Alternate language links point to the clean page URL and its `?lang=ar` representation; they are marked `hreflang="en"` and `hreflang="ar"`.
- Existing visible text remains the accessible name for phone, email and consultation links; icons and language controls keep explicit labels.

## Verification

- Unit-style Node tests exercise query precedence, link propagation, URL preservation, language toggle state, and localized SEO fields.
- Static tests confirm the dictionary covers the Patch 2 service/treatment phrases and all patient-facing pages still load `language.js` before `app.js`.
- Run the Patch 3 contract, existing Arabic contract, Patch 1–2 contracts, and the full suite. Existing About-page baseline failures are reported separately if unchanged.
