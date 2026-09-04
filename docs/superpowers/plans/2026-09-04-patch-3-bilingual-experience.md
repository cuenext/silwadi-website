# Patch 3 bilingual experience Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Arabic persist across Silwadi page navigation and present a complete, natural RTL experience with localized page metadata.

**Architecture:** Extend the existing dependency-free `language.js` controller instead of introducing a framework or duplicating Arabic HTML pages. The controller reads the URL/local-storage preference, translates the existing DOM, decorates same-origin page links, and updates language-specific metadata while shared CSS supplies a small RTL layer.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, Node-based contract tests, Python `unittest`.

**Spec:** `docs/superpowers/specs/2026-09-04-patch-3-bilingual-experience-design.md`

## Global Constraints

- Keep the existing static HTML/CSS/vanilla-JS architecture.
- No new runtime dependencies.
- Canonical URLs remain clean and unchanged.
- Preserve phone/email/consultation destinations and Patch 1–2 service routes.
- Use only concise, verified Arabic clinic wording; do not invent clinical claims.
- Do not change image pixels or add generated imagery.

---

### Task 1: Define the Patch 3 regression contract

**Files:**
- Create: `tests/test_patch3_bilingual_experience.py`
- Test: `tests/test_patch3_bilingual_experience.py`

**Interfaces:**
- Consumes: the public `SilwadiLanguage` API in `language.js` and page source files.
- Produces: failing tests for language-query precedence, internal-link propagation, metadata localization, RTL state, and Patch 2 Arabic coverage.

- [ ] **Step 1: Write the failing tests**

  Add a Node VM harness with `document`, `history`, `location`, `localStorage`, `CustomEvent`, and lightweight elements. Assert:

  ```python
  def test_url_language_overrides_saved_preference(self):
      state = self.run_language("?lang=ar", {"silwadi-language": "en"})
      self.assertEqual(state["language"], "ar")

  def test_arabic_internal_links_keep_page_path_and_hash(self):
      state = self.run_language("?lang=ar", {"silwadi-language": "ar"}, links=[
          "treatments.html#pedodontics", "../contact.html#consultation-form",
          "mailto:info@example.test", "tel:+97126262042"
      ])
      self.assertEqual(state["links"], [
          "treatments.html?lang=ar#pedodontics",
          "../contact.html?lang=ar#consultation-form",
          "mailto:info@example.test", "tel:+97126262042"
      ])

  def test_arabic_updates_metadata_without_dirtying_canonical(self):
      state = self.run_language("?lang=ar", {"silwadi-language": "en"})
      self.assertEqual(state["dir"], "rtl")
      self.assertEqual(state["canonical"], "https://silwadi.ae/services.html")
      self.assertTrue(state["title"])
      self.assertTrue(state["description"])
  ```

  Add static assertions that the Patch 2 phrases (`Start with what you need.`, `Children’s dental care`, `Replace or repair teeth`, `Prevention and hygiene`, `Tell us what is bothering you.`) have Arabic translations and that all patient-facing pages still load the language script before the app script.

- [ ] **Step 2: Run the contract to verify it fails for the missing behavior**

  Run:

  ```bash
  python -m unittest tests.test_patch3_bilingual_experience -v
  ```

  Expected: FAIL because URL query precedence, link decoration and localized metadata APIs do not yet exist.

- [ ] **Step 3: Commit the red contract**

  ```bash
  git add tests/test_patch3_bilingual_experience.py
  git commit -m "test: define Patch 3 bilingual experience contract"
  ```

### Task 2: Extend the language controller

**Files:**
- Modify: `language.js`
- Test: `tests/test_patch3_bilingual_experience.py`

**Interfaces:**
- Consumes: `STORAGE_KEY`, `translate`, `applyLanguage`, and existing `silwadi:languagechange` event.
- Produces: `getRequestedLanguage()`, `decorateInternalLinks(language)`, and `updateLocalizedSeo(language)` helpers used internally by `init`/`applyLanguage`.

- [ ] **Step 1: Add query/local-storage resolution and URL helpers**

  Implement explicit `?lang=ar|en` precedence, preserving the current page path and hash. When Arabic is active, append or replace only the `lang` query on same-origin `.html`/root page links. Skip hashes, assets, downloads, `mailto:`, `tel:`, `javascript:`, and external origins.

- [ ] **Step 2: Add language-aware metadata and alternates**

  Store a per-page Arabic title/description map with a conservative fallback. Update `document.title`, `meta[name="description"]`, `meta[property="og:title"]`, `meta[property="og:description"]`, and `meta[name="content-language"]`; leave the canonical link unchanged. Add/update `hreflang="en"` and `hreflang="ar"` links for the clean URL and Arabic query representation.

- [ ] **Step 3: Make toggles update the current URL and re-decorate links**

  The language button calls `applyLanguage(next)`; `applyLanguage` stores the choice, uses `history.replaceState` when available, updates `lang`/`dir`/body class, translates attributes including `alt`, and decorates links. Keep the event dispatch and existing Node-test behavior intact when browser APIs are absent.

- [ ] **Step 4: Run the focused contract**

  Run:

  ```bash
  python -m unittest tests.test_patch3_bilingual_experience -v
  ```

  Expected: PASS for query precedence, link preservation, language state, and metadata assertions.

- [ ] **Step 5: Commit the controller**

  ```bash
  git add language.js tests/test_patch3_bilingual_experience.py
  git commit -m "feat: persist Arabic language across page navigation"
  ```

### Task 3: Complete Arabic copy and RTL presentation

**Files:**
- Modify: `language.js`
- Modify: `styles.css`
- Test: `tests/test_patch3_bilingual_experience.py`

**Interfaces:**
- Consumes: the shared language controller and existing `language-ar` class.
- Produces: translated Patch 2 service/treatment labels, readable Arabic form controls, right-aligned cards/actions, and mobile-safe RTL layout.

- [ ] **Step 1: Add concise Arabic dictionary entries**

  Add translations for every new Patch 2 heading, card label, description, CTA and status string. Replace the awkward `Advanced dentistry.` value with a natural concise phrase while retaining the English source text unchanged.

- [ ] **Step 2: Add scoped RTL rules**

  Append CSS for Arabic navigation direction, breadcrumbs, form labels/selects, cards, treatment catalog actions, service starting cards, consultation action rows and mobile action bar. Keep phone/email and Latin clinical abbreviations readable with `direction:ltr` where needed. Include `prefers-reduced-motion: reduce` parity.

- [ ] **Step 3: Run copy and layout contract tests**

  Run:

  ```bash
  python -m unittest tests.test_patch3_bilingual_experience tests.test_patch22_roster_arabic -v
  ```

  Expected: PASS, with the pre-existing About assertions reported only by the broader suite if still present.

- [ ] **Step 4: Commit the Arabic UX layer**

  ```bash
  git add language.js styles.css tests/test_patch3_bilingual_experience.py
  git commit -m "feat: polish Arabic copy and RTL layout"
  ```

### Task 4: Verify the full patch and publish

**Files:**
- Modify: none unless verification finds a scoped regression.
- Test: `tests/test_patch3_bilingual_experience.py`, existing `tests/` suite.

**Interfaces:**
- Consumes: all Patch 3 commits.
- Produces: verification evidence and a merged GitHub PR; no cPanel changes.

- [ ] **Step 1: Run JavaScript syntax and focused contracts**

  ```bash
  node --check language.js
  python -m unittest tests.test_patch3_bilingual_experience tests.test_patch24_services_overhaul tests.test_patch23_mobile_ux -v
  ```

- [ ] **Step 2: Run the complete regression suite**

  ```bash
  python -m unittest discover -s tests -p 'test*.py' -v
  ```

  Record the exact pass/failure count and distinguish any unchanged About-page baseline failures from Patch 3 regressions.

- [ ] **Step 3: Review the diff and clean working tree**

  ```bash
  git diff --check
  git status --short
  git log --oneline -5
  ```

- [ ] **Step 4: Push via the configured GitHub workflow and merge only after checks**

  Create a non-draft PR titled `Patch 3: Arabic and bilingual experience`, include the verification counts and explicitly state that cPanel was not touched. Merge with squash only after the head SHA is revalidated.

- [ ] **Step 5: Report the live links and rollback point**

  Provide the merged commit/PR URL, note that GitHub Pages may cache briefly, and identify the Patch 3 merge SHA as the exact rollback reference.
