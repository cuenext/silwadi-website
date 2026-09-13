# Google Authority Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Safely transplant the already-tested behind-the-scenes Google authority/schema work from `seo-authority-0913` onto current `main` without losing newer AI/private-page work or introducing visible website changes.

**Architecture:** Use `seo-authority-integration-0913`, created from current `main` at `48142f2183aa1f33350b11629b70fd6633407345`, as the only integration branch. Port repository-only tests/workflows/docs first, then reapply the SEO JSON-LD transformation to the current-main HTML so newer page content is preserved. Verify with the full relevant regression set and a final diff audit before merging.

**Tech Stack:** Static HTML, JSON-LD/Schema.org, Python standard-library tests, GitHub Actions, Git.

**Spec:** User-approved behind-the-scenes SEO authority integration request dated 2026-09-13, plus `docs/seo/google-authority-audit-2026-09-13.md` from `seo-authority-0913`.

## Global Constraints

- ZERO visual/design changes.
- No visible body-copy, layout, photo, navigation, CSS, or public-page changes unless separately approved.
- Do not publish or expose private review pages; keep them noindex and absent from the sitemap.
- Do not modify or delete `old-silwadi-site`.
- Do not add “best”, “painless”, “pain-free”, “top-tier”, guaranteed outcome, superiority, or similar medical advertising claims.
- Preserve current-main AI/private-page work.
- Preserve the stable entity IDs: `https://silwadi.ae/#organization`, `https://silwadi.ae/#dentist`, `https://silwadi.ae/#dentist-al-raha`, `https://silwadi.ae/#website`.
- Preserve the approved 15-doctor branch map and English/Arabic parity.
- Do not build public Bani Yas or Al Raha landing pages in this pass.
- Pediatric gallery work remains paused.

---

### Task 1: Establish the integration baseline

**Files:**
- No production changes.

**Interfaces:**
- Consumes: current `main`, `seo-authority-0913`, existing tests and private AI work.
- Produces: confirmed branch divergence, merge base, and regression baseline.

- [ ] **Step 1:** Confirm `main` head is `48142f2183aa1f33350b11629b70fd6633407345` and SEO head is `12bb9ea117c77d29f9f663c415509bb92219797d`.
- [ ] **Step 2:** Confirm merge base is `6777e4d4196653187c14b727a417c8c6acf6d6ef` and the branches are diverged.
- [ ] **Step 3:** Run the current-main relevant regression baseline before applying SEO changes.

### Task 2: Port repository-only SEO authority assets

**Files:**
- Create: `tests/test_google_authority.py`
- Create: `.github/workflows/google-authority-test.yml`
- Create: `scripts/apply_google_authority.py`
- Create: `.github/workflows/apply-google-authority.yml`
- Create: `docs/superpowers/plans/2026-09-13-google-authority-pass.md`
- Create: `docs/seo/google-authority-audit-2026-09-13.md`
- Create: `docs/seo/legacy-domain-redirect-map-2026-09-13.md`

**Interfaces:**
- Consumes: files from `seo-authority-0913`.
- Produces: the tested authority contract, deterministic transformation script, audit, and legacy migration plan on the integration branch.

- [ ] **Step 1:** Copy the files byte-for-byte from the SEO branch.
- [ ] **Step 2:** Confirm none of these files touch visible production UI by themselves.
- [ ] **Step 3:** Run the new authority test against current-main HTML and record expected failures before applying the transformation.

### Task 3: Reapply authority/schema changes to current-main HTML

**Files:**
- Modify only public HTML technical metadata/JSON-LD files selected by `scripts/apply_google_authority.py`.

**Interfaces:**
- Consumes: current-main HTML and the deterministic SEO transformation.
- Produces: stable entity graph, doctor branch references, treatment/service providers, canonical/hreflang consistency, and compliant metadata while preserving visible HTML.

- [ ] **Step 1:** Run `python scripts/apply_google_authority.py --check` if supported; otherwise inspect script behavior before execution.
- [ ] **Step 2:** Execute the transformation against the integration branch working tree.
- [ ] **Step 3:** Review every changed production file and verify changes are limited to `<head>` metadata and/or JSON-LD technical content.
- [ ] **Step 4:** Confirm no `review/`, CSS, JS, image, navigation, body-copy, or pediatric gallery file changed.

### Task 4: Run the full relevant regression suite

**Files:**
- No new production scope.

**Interfaces:**
- Produces: evidence that SEO, doctor, Arabic, sitemap/privacy, and AI/private-page behavior remains intact.

- [ ] **Step 1:** Run `tests/test_google_authority.py`.
- [ ] **Step 2:** Run `tests/test_doctor_profiles_seo.py` and `tests/test_doctor_profile_advertising_compliance.py`.
- [ ] **Step 3:** Run `tests/test_arabic_structured_data.py`, `tests/test_arabic_quality_seo_rebuild.py`, and other Arabic/SEO regressions implicated by changed files.
- [ ] **Step 4:** Run sitemap/indexing/privacy regressions including `tests/test_public_core_seo.py`, `tests/test_patch8_technical_seo.py`, and private review tests.
- [ ] **Step 5:** Run current-main AI/private regressions including `tests/test_private_ai_faq_review.py`, `tests/test_ai_knowledge_v1.py`, and `tests/test_ai_worker_contract.py`.
- [ ] **Step 6:** Run the full Python test suite if runtime is practical.

### Task 5: Diff and compliance review

**Files:**
- No new production scope.

**Interfaces:**
- Produces: explicit no-visual-change and no-private-publication verification.

- [ ] **Step 1:** Compare the integration branch against current `main` and enumerate changed paths.
- [ ] **Step 2:** Reject any CSS, image, JS, visible body-copy, navigation, or private-review publication diff.
- [ ] **Step 3:** Scan changed public metadata/JSON-LD for prohibited advertising language.
- [ ] **Step 4:** Verify `sitemap.xml` still excludes `/review/`, `/.tmp/`, and `old-silwadi-site`.

### Task 6: Merge only after verified green

**Files:**
- No new production scope.

**Interfaces:**
- Produces: a safe integration on `main` with current-main work preserved.

- [ ] **Step 1:** Reconfirm `main` has not moved unexpectedly; if it has, rebase/retransplant and rerun verification before merging.
- [ ] **Step 2:** Merge the integration branch only after all relevant tests and diff checks pass.
- [ ] **Step 3:** Verify the new `main` head and GitHub Actions status before claiming completion.

### Task 7: Continue non-visual Local SEO follow-through

**Files:**
- Repo-only documentation/tests only unless a later approved technical change is needed.

**Interfaces:**
- Produces: actionable next steps without publishing visible location pages or private review pages.

- [ ] **Step 1:** Preserve and refine the P0 legacy-domain 301/308 redirect plan; do not modify `old-silwadi-site`.
- [ ] **Step 2:** Re-audit schema consistency, English/Arabic parity, sitemap/indexing hygiene, and local entity clarity after integration.
- [ ] **Step 3:** Keep dedicated location landing pages as recommendation-only because they are visible/content changes.
- [ ] **Step 4:** Keep Google Business Profile and Search Console actions as a factual implementation checklist until listing/property access exists.
