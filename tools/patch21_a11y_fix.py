from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

# Let visible Instagram handle be the accessible link name sitewide.
for path in ROOT.rglob("*.html"):
    if any(part in {".git", "node_modules"} for part in path.parts):
        continue
    text = path.read_text(encoding="utf-8")
    if '<footer class="site-footer">' not in text:
        continue
    text = text.replace(
        ' target="_blank" rel="noopener" aria-label="Follow Silwadi Dental Center on Instagram">',
        ' target="_blank" rel="noopener">',
    )
    path.write_text(text, encoding="utf-8")

# Let visible review-card content form the role=button accessible name.
home_path = ROOT / "index.html"
home = home_path.read_text(encoding="utf-8")
home = re.sub(
    r'(<article class="google-review-card"[^>]*data-review-open[^>]*?)\s+aria-label="[^"]*"(>)',
    r'\1\2',
    home,
)
home_path.write_text(home, encoding="utf-8")

# Use an AA-safe neutral for the small footer-hour values.
styles_path = ROOT / "styles.css"
styles = styles_path.read_text(encoding="utf-8")
styles = styles.replace('.footer-hours em{color:#71868d}', '.footer-hours em{color:#526a73}')
styles_path.write_text(styles, encoding="utf-8")
