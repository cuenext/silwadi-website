# Arabic Quality & SEO Rebuild Design

**Status:** Approved by the site owner on 2026-09-05

## Goal
Make the Arabic experience read and behave like a professionally authored UAE dental website, not a translated English overlay, while giving Arabic content its own crawlable SEO surface.

## Language standard
- Modern Standard Arabic, natural in UAE healthcare context.
- Prefer concise patient-facing phrasing over literal translation.
- Preserve clinical accuracy and established dental terminology.
- Use one consistent Arabic spelling for doctor names, branches, services and recurring UI labels.
- Avoid duplicate ideas, stacked microcopy, repeated labels and unnecessary two-line buttons.

## Scope
1. Audit every patient-facing Arabic string in `language.js` and remove duplicate/conflicting mappings.
2. Rewrite awkward Arabic into concise, natural clinic language.
3. Add tests that detect duplicate translation keys, untranslated patient-facing copy and malformed Arabic SEO metadata.
4. Fix RTL layout globally and page-specifically, including short CTA labels, mixed-direction phone/email content, cards, forms and mobile sticky controls.
5. Fix Google Reviews so language toggling changes text/direction only; it must not reverse or restart the marquee.
6. Add dedicated crawlable Arabic URLs under `/ar/` for homepage, institutional pages, doctor index/profile pages and treatment pages.
7. Arabic pages use `lang="ar"`, `dir="rtl"`, Arabic title/description/Open Graph metadata, self-canonical URLs and reciprocal `hreflang` links.
8. English pages gain reciprocal Arabic `hreflang` links while retaining their existing canonical URLs.
9. Sitemap includes both English and Arabic URLs.

## Architecture
- Keep existing English pages as source-of-truth routes.
- Keep `language.js` for interactive language switching and shared text behavior, but clean and normalize its Arabic dictionary.
- Add a deterministic static Arabic build script that transforms the known patient-facing HTML files into committed `/ar/` counterparts using the same reviewed Arabic dictionary and route map.
- Generated Arabic pages are real HTML, not JS-only translations.
- Arabic pages link to Arabic routes directly; switching to English returns to the paired English route.

## Google Reviews behavior
The marquee keeps one physical animation direction in both languages. Arabic changes card text flow to RTL but does not apply `animation-direction: reverse`, reset transforms, or rebuild the track during the language toggle.

## SEO rules
- English canonical: `https://silwadi.ae/<route>`.
- Arabic canonical: `https://silwadi.ae/ar/<route>`.
- English alternate: `hreflang="en-AE"` to English canonical.
- Arabic alternate: `hreflang="ar-AE"` to Arabic canonical.
- Add `x-default` to English canonical.
- Arabic titles and descriptions are written as Arabic search snippets, not direct word-for-word metadata translations.
- Keep structured data factual and consistent across languages.

## Verification
- Run Arabic translation contract tests.
- Run duplicate-key and untranslated-copy tests.
- Run SEO static tests for canonical/hreflang/lang/dir/title/description on every Arabic page.
- Run route pairing tests ensuring every English patient page has an Arabic counterpart and vice versa.
- Verify Google Reviews CSS contains no Arabic reverse-animation rule.
- Run the existing full test suite and report unrelated legacy failures separately.
