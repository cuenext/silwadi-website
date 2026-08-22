# Patch 13 Lighthouse Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the confirmed Lighthouse performance and accessibility regressions without changing the site’s visual direction or clinical copy.

**Architecture:** Keep the site dependency-free and static. Fix the Dental Implants provider portrait at the HTML source, darken only the existing low-contrast neutral text palette enough to meet WCAG AA on the site’s real light surfaces, and expand shared footer link hit areas to the 24px WCAG 2.2 target-size floor while preserving layout. Use regression tests plus a real Lighthouse rerun as the release gate.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, Python `unittest`, GitHub Actions, Lighthouse CLI/Chrome.

**Spec:** `docs/launch/PRELAUNCH-LIGHTHOUSE.md` and the follow-up Lighthouse diagnostics on the isolated audit branch.

## Global Constraints

- Preserve the premium clinical-institution design; no redesign.
- Do not change clinical claims, doctor credentials, treatment copy, canonical URLs, schema, or navigation structure.
- Do not add runtime libraries, a package manager, or a build system.
- Keep existing optimized doctor WebP assets; do not generate new image derivatives unless tests prove one is missing.
- Lighthouse scores must be reported only from an actual completed run.
- `main` may advance only after full regression, SEO audit, JS syntax, internal-reference, JSON-LD, HTTP smoke, and Lighthouse verification are green.

---

### Task 1: Define the Patch 13 regression contract

**Files:**
- Create: `tests/test_patch13_lighthouse_polish.py`

**Interfaces:**
- Consumes: existing static site files and optimized portraits under `assets/doctors/optimized/`.
- Produces: regression tests that fail on the Patch 12 tree and pass only when the confirmed Lighthouse root causes are removed.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_patch13_lighthouse_polish.py` with tests that:

```python
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding='utf-8')


def rel_luminance(hex_color):
    value = hex_color.lstrip('#')
    channels = [int(value[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(foreground, background):
    a, b = rel_luminance(foreground), rel_luminance(background)
    lighter, darker = max(a, b), min(a, b)
    return (lighter + 0.05) / (darker + 0.05)


def rule(css, selector):
    match = re.search(re.escape(selector) + r'\{([^}]*)\}', css)
    if not match:
        raise AssertionError(f'Missing CSS rule: {selector}')
    return match.group(1)


def color_from_rule(css, selector):
    body = rule(css, selector)
    match = re.search(r'(?:^|;)\s*color\s*:\s*(#[0-9a-fA-F]{6})', body)
    if not match:
        raise AssertionError(f'Missing hex color in: {selector}')
    return match.group(1)


class PatchThirteenLighthousePolish(unittest.TestCase):
    def test_html_never_renders_original_doctor_pngs(self):
        for page in ROOT.rglob('*.html'):
            html = page.read_text(encoding='utf-8')
            self.assertNotRegex(html, r'<img[^>]+src="(?:\.\./)?assets/doctors/[^/\"]+\.png"', page.relative_to(ROOT))

    def test_implant_provider_uses_lazy_optimized_dimensioned_portrait(self):
        html = read('treatments/dental-implants.html')
        match = re.search(r'<div class="provider-card"><img\s+([^>]+)>', html, re.I)
        self.assertIsNotNone(match)
        attrs = match.group(1)
        self.assertIn('src="../assets/doctors/optimized/dr-munir-silwadi.webp"', attrs)
        self.assertIn('loading="lazy"', attrs)
        self.assertIn('decoding="async"', attrs)
        self.assertIn('width="720"', attrs)
        self.assertIn('height="720"', attrs)

    def test_light_surface_neutral_text_meets_wcag_aa(self):
        css = read('styles.css')
        muted = re.search(r'--muted\s*:\s*(#[0-9a-fA-F]{6})', css).group(1)
        self.assertGreaterEqual(contrast(muted, '#f7fafb'), 4.5)
        self.assertGreaterEqual(contrast(muted, '#f8fafb'), 4.5)
        checks = [
            ('.legacy-seal span', '#ffffff'),
            ('.care-shortcuts span', '#ffffff'),
            ('.care-shortcuts em', '#ffffff'),
            ('.footer-grid a,.footer-grid span', '#f8fafb'),
            ('.footer-bottom', '#f8fafb'),
        ]
        for selector, background in checks:
            self.assertGreaterEqual(contrast(color_from_rule(css, selector), background), 4.5, selector)

    def test_footer_links_meet_minimum_target_size(self):
        css = read('styles.css')
        body = rule(css, '.footer-grid a')
        self.assertRegex(body, r'min-height\s*:\s*24px')
        self.assertRegex(body, r'display\s*:\s*inline-flex')


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: Run the Patch 13 test on the untouched Patch 12 source and verify RED**

Run in CI from the feature branch:

```bash
python -m unittest tests.test_patch13_lighthouse_polish -v
```

Expected: failures for the Dental Implants PNG/eager image, light-surface contrast, and footer target-size contract.

- [ ] **Step 3: Commit the RED contract**

```bash
git add tests/test_patch13_lighthouse_polish.py
git commit -m "test: define Patch 13 Lighthouse contract"
```

---

### Task 2: Fix the Dental Implants network regression

**Files:**
- Modify: `treatments/dental-implants.html`
- Test: `tests/test_patch13_lighthouse_polish.py`

**Interfaces:**
- Consumes: existing `assets/doctors/optimized/dr-munir-silwadi.webp` (720×720).
- Produces: an offscreen provider portrait that transfers the optimized WebP and defers loading/decoding work.

- [ ] **Step 1: Replace the provider image tag**

Change:

```html
<img src="../assets/doctors/dr-munir-silwadi.png" alt="Dr. Munir Silwadi">
```

To:

```html
<img src="../assets/doctors/optimized/dr-munir-silwadi.webp" alt="Dr. Munir Silwadi" width="720" height="720" loading="lazy" decoding="async">
```

- [ ] **Step 2: Run the image-specific Patch 13 tests**

```bash
python -m unittest tests.test_patch13_lighthouse_polish.PatchThirteenLighthousePolish.test_html_never_renders_original_doctor_pngs tests.test_patch13_lighthouse_polish.PatchThirteenLighthousePolish.test_implant_provider_uses_lazy_optimized_dimensioned_portrait -v
```

Expected: PASS.

- [ ] **Step 3: Commit the image fix**

```bash
git add treatments/dental-implants.html
git commit -m "perf: optimize implant provider portrait"
```

---

### Task 3: Fix confirmed light-surface contrast and footer target size

**Files:**
- Modify: `styles.css`
- Test: `tests/test_patch13_lighthouse_polish.py`

**Interfaces:**
- Consumes: the existing neutral/teal/navy design system.
- Produces: neutral text with at least 4.5:1 contrast on `#f7fafb`, `#f8fafb`, and white where Lighthouse found failures, plus 24px-tall shared footer links.

- [ ] **Step 1: Darken the shared muted neutral for off-white surfaces**

Change the root variable:

```css
--muted:#60777f;
```

This yields at least 4.50:1 on both `#f7fafb` and `#f8fafb` while remaining visually within the current cool-gray palette.

- [ ] **Step 2: Darken the literal low-contrast light-surface colors**

Use `#60777f` for these existing foreground rules:

```css
.legacy-seal span{...color:#60777f;...}
.care-shortcuts span{...color:#60777f;...}
.care-shortcuts em{...color:#60777f;...}
.footer-grid a,.footer-grid span{color:#60777f;...}
.footer-bottom{...color:#60777f;...}
```

Do not change the high-contrast dark-background colors in `.digital-section` or `.consultation-cta`.

- [ ] **Step 3: Increase only footer link hit areas**

Add a focused rule after the existing footer typography rule:

```css
.footer-grid a{display:inline-flex;align-items:center;min-height:24px}
```

The footer uses vertically stacked links with 9px gaps; 24px link boxes satisfy the WCAG 2.2 target-size floor without turning the footer into button UI.

- [ ] **Step 4: Run the CSS-specific Patch 13 tests**

```bash
python -m unittest tests.test_patch13_lighthouse_polish.PatchThirteenLighthousePolish.test_light_surface_neutral_text_meets_wcag_aa tests.test_patch13_lighthouse_polish.PatchThirteenLighthousePolish.test_footer_links_meet_minimum_target_size -v
```

Expected: PASS.

- [ ] **Step 5: Commit the accessibility fix**

```bash
git add styles.css
git commit -m "fix: improve Lighthouse accessibility contrast"
```

---

### Task 4: Full regression and Lighthouse release gate

**Files:**
- Create: `docs/launch/PATCH13-LIGHTHOUSE-QA.md`
- Temporary CI workflow: `.github/workflows/patch13-verify.yml` (must self-delete before integration)

**Interfaces:**
- Consumes: the complete Patch 13 feature branch.
- Produces: fresh automated regression evidence and real Lighthouse mobile/desktop scores for the representative seven-page matrix.

- [ ] **Step 1: Run the complete repository verification**

CI commands:

```bash
python -m pip install --disable-pip-version-check pillow
python -m unittest discover -s tests -p 'test_*.py' -v
node --check app.js
python tools/seo_launch_audit.py
```

Also rerun the existing local-reference, JSON-LD, and HTTP smoke checks used by Patch 12.

Expected: all checks PASS with zero broken references/JSON-LD errors/HTTP failures.

- [ ] **Step 2: Run real Lighthouse mobile and desktop**

Audit these pages against the static feature-branch build:

```text
/
/doctors.html
/doctors/dr-munir-silwadi.html
/treatments.html
/treatments/dental-implants.html
/locations.html
/contact.html
```

Collect Performance, Accessibility, Best Practices, SEO, FCP, LCP, TBT, and CLS.

Release targets:
- No representative mobile Performance score below 95.
- Accessibility improves materially from the Patch 12 baseline and the confirmed contrast/target-size audits no longer fail.
- Best Practices remains 100 on the representative matrix.
- SEO remains 100 on the representative matrix.

- [ ] **Step 3: Record a permanent QA report**

Write `docs/launch/PATCH13-LIGHTHOUSE-QA.md` with:
- source commit SHA,
- complete test count/result,
- JS/SEO/internal-reference/JSON-LD/HTTP results,
- seven-page mobile/desktop Lighthouse table,
- average category scores,
- explicit before/after Dental Implants mobile score and LCP,
- any remaining Lighthouse audit worth reviewing,
- note that production Lighthouse must still be rerun after public deployment.

- [ ] **Step 4: Ensure temporary workflow and generated runtime files are absent**

Verify the feature branch contains no `.github/workflows/patch13-verify.yml`, Lighthouse raw JSON files, `__pycache__`, or `*.pyc` artifacts.

- [ ] **Step 5: Integrate non-force only after the complete gate is green**

Compare `main...patch-13-lighthouse-polish`, confirm the feature branch is based on the current `main`, then advance `main` using a non-force ref update only if every release gate above is green.
