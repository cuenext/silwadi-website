from pathlib import Path

path = Path(__file__).resolve().parents[1] / "about.html"
html = path.read_text(encoding="utf-8")
old = '<figure><img src="assets/services/teeth-whitening.webp" alt="Dental shade matching for cosmetic and whitening care" width="1200" height="900" loading="lazy" decoding="async"></figure>'
new = '<figure><img src="assets/services/cosmetics.webp" alt="Cosmetic dental restoration and smile care" width="1200" height="900" loading="lazy" decoding="async"></figure>'
html = html.replace(old, new, 1)
path.write_text(html, encoding="utf-8")
