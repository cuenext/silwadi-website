# Patch 4 — SEO, accessibility and launch-quality pass

## Goal

Make the static site easier to discover, easier to use on a phone and safer to
maintain without changing the approved clinic facts or inventing clinical claims.

## Scope

1. Remove the last broken internal service route and verify every local anchor
   used by the service hub resolves to a real section.
2. Rework the About page copy and imagery around verified Silwadi information:
   a natural story, a restrained clinic-photo gallery, descriptive image text,
   and an explicit path to the doctors and services.
3. Add practical appointment-form privacy guidance and an explicit consent
   control. The form opens the visitor's own email app, so it must not imply
   that sensitive medical information is collected securely by the website.
4. Improve bilingual/share metadata and image loading hints without changing
   canonical URLs, the redirect handoff, or the existing approved navigation.
5. Add repeatable regression checks for broken routes, About-page quality,
   consent copy, and the metadata behavior.

## Guardrails

- Keep the current 27 indexable launch URLs and sitemap contract.
- Use only supplied/verified clinic and doctor assets; do not generate or
  retouch people in photographs.
- Keep Arabic and English paths on the same canonical URL with the existing
  `?lang=ar` behavior.
- Do not publish self-authored reviews, ratings, guarantees, or medical advice.
- Treat the privacy note as plain-language website guidance, not a substitute
  for the clinic's legal/compliance review.

## Verification

- Run the new Patch 4 tests first (red before implementation).
- Run the complete Python test suite and `tools/seo_launch_audit.py`.
- Check all local HTML links and image targets.
- Validate JavaScript syntax and inspect a local mobile/desktop render before
  publishing the patch.
