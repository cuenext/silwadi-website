# Silwadi Header Logo Size Tweak Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make every public header logo roughly 10% smaller without changing footer logos or header layout.

**Architecture:** Keep all header containers at their current dimensions and change only the responsive image widths. Use the existing static CSS contract test to cover shared styles, homepage overrides, treatment styles, and inline treatment-page variants.

**Tech Stack:** Static HTML/CSS, Node.js built-in test runner.

**Spec:** `docs/superpowers/specs/2026-11-01-silwadi-header-logo-size-tweak-design.md`

## Global Constraints

- Header image width is 74px on desktop and 65px on mobile.
- Header wrappers and heights remain unchanged.
- Footer logo width remains 128px.
- The official transparent SVG and its 259:225 aspect ratio remain unchanged.

## Review Focus

- Homepage overrides must not mask the shared smaller size.
- Arabic and English treatment-page inline styles must remain equal.
- The FAQ/AI shell must inherit the shared header size.
- Mobile sizing must not change the header frame or menu placement.
- Footer rules must remain at 128px.

---

### Task 1: Responsive header sizing contract

**Files:**
- Modify: `tests/silwadi-logo-production.test.cjs`
- Modify: `styles.css`
- Modify: `home-reviews.css`
- Modify: `treatments/treatment-refresh-v1.css`
- Modify: `treatments/endodontics.html`
- Modify: `treatments/pediatric-dentistry.html`
- Modify: `treatments/people-of-determination.html`
- Modify: `ar/treatments/endodontics.html`
- Modify: `ar/treatments/pediatric-dentistry.html`
- Modify: `ar/treatments/people-of-determination.html`

**Interfaces:**
- Consumes: existing header selectors and the official SVG asset.
- Produces: a 74px desktop / 65px mobile header logo contract across every public shell; footer remains 128px.

- [x] **Step 1: Write the failing test**

Change the existing responsive-size assertions to require 74px desktop and 65px mobile while retaining every 128px footer assertion.

- [x] **Step 2: Run the focused test and verify RED**

Run: `node --test tests/silwadi-logo-production.test.cjs`

Expected: the shared-size and page-local-size tests fail because production CSS still uses 82px and 72px.

- [x] **Step 3: Implement the minimal CSS changes**

Update only the header-image widths in the files listed above. Do not alter wrapper sizes, header heights, footer widths, assets, markup, or content.

- [x] **Step 4: Run the focused test and verify GREEN**

Run: `node --test tests/silwadi-logo-production.test.cjs`

Expected: 7 tests pass, 0 fail.

- [x] **Step 5: Run repository checks and visual verification**

Run the available Node tests, validate the public bundle, and inspect English/Arabic desktop and mobile headers in a local preview. Confirm footer sizing is unchanged.

- [x] **Step 6: Commit**

Commit the test, CSS/HTML changes, specification, and plan together with a focused message.
