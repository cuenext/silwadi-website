# Patch 1: Mobile navigation and visual stability

**Status:** Approved for implementation by the site owner on 2026-09-03  
**Branch:** `patch-1-mobile-ux`  
**Baseline:** `a73c895d00a96ee0ff7a4e25f737ac99c424721b`

## Goal

Make the existing Silwadi static site reliable and polished at mobile and desktop widths without changing service information, Arabic content, or the original photo assets.

## Scope

1. Make the mobile navigation panel independently scrollable while preserving keyboard and touch access to every link.
2. Replace the home page shortcut grid's hard vertical and horizontal rules with a soft, borderless quick-action card treatment.
3. Add visible, accessible phone and email icons to contact details and footer contact rows.
4. Give mobile sections consistent gutters and prevent text from touching the viewport edge.
5. Keep the source clinic photo pixel-for-pixel; only CSS layout, crop, overlay and responsive sizing may change.
6. Preserve all existing consultation routes and language-switch behavior.

## Non-goals

- No service taxonomy or treatment-page redesign (Patch 2).
- No new Arabic URL tree or schema/sitemap changes (Patch 3).
- No cPanel deployment in this patch.
- No generated or face-altered imagery.

## Files

- Modify `styles.css`: mobile navigation overflow/focus treatment, shortcut-card layout, contact icon styles and responsive gutters.
- Modify `app.js`: close the menu after navigation, handle Escape consistently, and keep focus behavior safe when the menu opens/closes.
- Modify `index.html`, `contact.html`, `locations.html` and shared footer/header markup only where phone/email icon markup is needed. Use inline SVG with `aria-hidden="true"` next to text links; keep the text link as the accessible name.
- No new runtime dependencies.

## Interaction requirements

- At viewport widths up to 1040px, opening the menu exposes a panel with a maximum height based on the viewport and `overflow-y:auto`.
- The page behind the open panel remains locked, but the panel itself can scroll with touch, mouse wheel and keyboard.
- The menu button's `aria-expanded` state tracks visibility; Escape and clicking a navigation link close the menu.
- Focus-visible outlines remain visible.
- Shortcut cards have no full-height side rules. Each card has a clear hit area, hover/focus state and no layout shift.
- Phone links use `tel:`; email links use `mailto:`; icons never replace the visible text labels.
- At 390px wide there is at least 15px horizontal breathing room on every main content block and no horizontal scrollbar.
- At desktop widths the existing max-width container and navigation alignment remain intact.

## Acceptance checks

- Use a real browser at 390x844 and 1280x800.
- Open the mobile menu, expand Services, scroll to the final service, activate a service link, press Escape, and reopen it.
- Confirm `document.body` has no horizontal overflow at either viewport.
- Confirm shortcut cards render without vertical separator borders and retain keyboard focus styles.
- Confirm phone/email icons appear beside text links in contact/footer areas and links still activate.
- Confirm consultation CTA destinations are unchanged.
- Confirm the original image URLs and intrinsic dimensions are unchanged.
- Check `prefers-reduced-motion: reduce` disables transitions.
- Run a static internal-link check and inspect the changed diff before merging.

## Rollback

Patch 1 is isolated on `patch-1-mobile-ux`. Restoring the baseline commit above returns the exact pre-patch site. The implementation commit will be separate from this specification commit.
