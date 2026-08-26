from pathlib import Path
import html as html_lib
import re

ROOT = Path(__file__).resolve().parents[1]

INSTAGRAM_URL = "https://www.instagram.com/dr.munirsilwadidental/"

FOOTER_BLOCK = '''<div class="footer-hours-social"><h3>Opening hours</h3><div class="footer-hours"><strong>Bani Yas Tower hours</strong><span><b>Sunday – Wednesday</b><em>09:00 AM – 09:00 PM</em></span><span><b>Thursday &amp; Saturday</b><em>09:00 AM – 06:00 PM</em></span><span><b>Friday</b><em>Closed</em></span></div><a class="footer-instagram" href="https://www.instagram.com/dr.munirsilwadidental/" target="_blank" rel="noopener" aria-label="Follow Silwadi Dental Center on Instagram"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4.1" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17.4" cy="6.7" r="1.1" fill="currentColor"/></svg><span>@dr.munirsilwadidental</span></a></div>'''

DIALOG = '''<dialog class="review-dialog" data-review-dialog aria-labelledby="reviewDialogName" aria-describedby="reviewDialogText"><div class="review-dialog__surface"><button class="review-dialog__close" type="button" data-review-dialog-close aria-label="Close review">×</button><div class="review-dialog__eyebrow">Google review</div><div class="review-dialog__identity"><span class="review-avatar" data-review-dialog-avatar aria-hidden="true"></span><div><h3 id="reviewDialogName" data-review-dialog-name></h3><span class="review-stars" data-review-dialog-stars></span></div></div><p id="reviewDialogText" data-review-dialog-text></p><a class="review-dialog__maps" href="https://maps.app.goo.gl/Ln2vEZmQmgWjb3ETA" target="_blank" rel="noopener">View reviews on Google Maps</a></div></dialog>'''

# Sitewide footer: add verified Bani Yas hours and the official Instagram account.
for path in ROOT.rglob("*.html"):
    if any(part in {".git", "node_modules"} for part in path.parts):
        continue
    text = path.read_text(encoding="utf-8")
    if '<footer class="site-footer">' not in text:
        continue
    if INSTAGRAM_URL not in text:
        marker = '</div><div class="container footer-bottom">'
        if marker not in text:
            raise RuntimeError(f"Footer grid marker not found in {path}")
        text = text.replace(marker, FOOTER_BLOCK + marker, 1)
    path.write_text(text, encoding="utf-8")

# Homepage aggregate Google rating: 4 full + half star while retaining the 4.6 numeric rating.
home_path = ROOT / "index.html"
home = home_path.read_text(encoding="utf-8")
old_aggregate = '<span class="google-rating-card__stars" aria-label="4.6 out of 5 stars">★★★★★</span><strong>4.6</strong>'
new_aggregate = '<span class="google-rating-card__stars" aria-label="4.6 out of 5 stars"><span class="rating-star rating-star--full" aria-hidden="true">★</span><span class="rating-star rating-star--full" aria-hidden="true">★</span><span class="rating-star rating-star--full" aria-hidden="true">★</span><span class="rating-star rating-star--full" aria-hidden="true">★</span><span class="rating-star rating-star--half" aria-hidden="true">★</span></span><strong>4.6</strong>'
if old_aggregate in home:
    home = home.replace(old_aggregate, new_aggregate, 1)

# Make every carousel card mouse/touch readable; only the non-duplicated group participates in tab order.
if 'data-review-open' not in home:
    card_pattern = re.compile(r'<article class="google-review-card">(.*?)</article>', re.S)
    card_index = 0
    def make_interactive(match):
        nonlocal_placeholder = None
        global card_index
        inner = match.group(1)
        name_match = re.search(r'<strong>(.*?)</strong>', inner, re.S)
        name = re.sub(r'<[^>]+>', '', name_match.group(1) if name_match else 'Patient')
        name = html_lib.unescape(name).strip()
        tabindex = "0" if card_index < 5 else "-1"
        card_index += 1
        aria_name = html_lib.escape(f"Read {name}'s Google review", quote=True)
        return f'<article class="google-review-card" data-review-open role="button" tabindex="{tabindex}" aria-haspopup="dialog" aria-label="{aria_name}">{inner}</article>'
    home = card_pattern.sub(make_interactive, home)

if 'data-review-dialog' not in home:
    marker = '</section><section class="section" id="locations">'
    if marker not in home:
        raise RuntimeError("Could not place review dialog before locations section")
    home = home.replace(marker, '</section>' + DIALOG + '<section class="section" id="locations">', 1)

home_path.write_text(home, encoding="utf-8")

# Add review-dialog behavior without changing existing navigation/reveal behavior.
app_path = ROOT / "app.js"
app = app_path.read_text(encoding="utf-8")
if "data-review-dialog" not in app:
    app += r'''

// Expand Google review excerpts into an accessible reading dialog.
const reviewDialog = document.querySelector('[data-review-dialog]');
const reviewDialogClose = document.querySelector('[data-review-dialog-close]');
const reviewDialogName = document.querySelector('[data-review-dialog-name]');
const reviewDialogText = document.querySelector('[data-review-dialog-text]');
const reviewDialogStars = document.querySelector('[data-review-dialog-stars]');
const reviewDialogAvatar = document.querySelector('[data-review-dialog-avatar]');
let lastReviewTrigger = null;

function openReviewDialog(card) {
  if (!reviewDialog || !card) return;
  const name = card.querySelector('.google-review-card__top strong')?.textContent?.trim() || 'Patient review';
  const text = card.querySelector('p')?.textContent?.trim() || '';
  const stars = card.querySelector('.review-stars');
  const avatar = card.querySelector('.review-avatar')?.textContent?.trim() || '';
  if (reviewDialogName) reviewDialogName.textContent = name;
  if (reviewDialogText) reviewDialogText.textContent = text;
  if (reviewDialogAvatar) reviewDialogAvatar.textContent = avatar;
  if (reviewDialogStars && stars) {
    reviewDialogStars.textContent = stars.textContent || '';
    reviewDialogStars.setAttribute('aria-label', stars.getAttribute('aria-label') || 'Google review rating');
  }
  lastReviewTrigger = card;
  if (typeof reviewDialog.showModal === 'function') reviewDialog.showModal();
  else reviewDialog.setAttribute('open', '');
}

document.querySelectorAll('[data-review-open]').forEach(card => {
  card.addEventListener('click', () => openReviewDialog(card));
  card.addEventListener('keydown', event => {
    if (event.key !== 'Enter' && event.key !== ' ') return;
    event.preventDefault();
    openReviewDialog(card);
  });
});

reviewDialogClose?.addEventListener('click', () => reviewDialog?.close());
reviewDialog?.addEventListener('click', event => {
  if (event.target === reviewDialog) reviewDialog.close();
});
reviewDialog?.addEventListener('close', () => {
  if (lastReviewTrigger?.isConnected && lastReviewTrigger.tabIndex >= 0) lastReviewTrigger.focus();
});
'''
app_path.write_text(app, encoding="utf-8")

# Review stars + modal visuals.
reviews_path = ROOT / "home-reviews.css"
reviews = reviews_path.read_text(encoding="utf-8")
if "/* Patch 21: aggregate half-star + readable review dialog */" not in reviews:
    reviews += r'''

/* Patch 21: aggregate half-star + readable review dialog */
.google-rating-card__stars{display:flex;align-items:center;gap:2px;letter-spacing:0}
.rating-star{position:relative;display:inline-block;width:1em;color:#d6dee0;line-height:1}
.rating-star--full{color:#f5b301}
.rating-star--half::before{content:"★";position:absolute;inset:0 auto 0 0;width:50%;overflow:hidden;color:#f5b301}
.google-review-card[data-review-open]{cursor:pointer}
.google-review-card[data-review-open]:focus-visible{outline:3px solid rgba(13,124,144,.32);outline-offset:4px}
.review-dialog{width:min(620px,calc(100% - 32px));max-height:min(82vh,720px);padding:0;border:0;border-radius:24px;background:transparent;color:#173943;overflow:visible}
.review-dialog::backdrop{background:rgba(5,42,54,.54);backdrop-filter:blur(7px);-webkit-backdrop-filter:blur(7px)}
.review-dialog__surface{position:relative;padding:34px 36px 32px;border:1px solid rgba(210,226,229,.95);border-radius:24px;background:linear-gradient(145deg,rgba(255,255,255,.98),rgba(248,252,252,.98));box-shadow:0 32px 90px rgba(5,42,54,.28);animation:review-dialog-in .2s ease-out}
.review-dialog__close{position:absolute;top:16px;right:16px;width:38px;height:38px;border:1px solid #d6e2e4;border-radius:50%;background:#fff;color:#083847;font-size:24px;line-height:1;cursor:pointer;transition:transform .18s ease,background .18s ease}
.review-dialog__close:hover{background:#f2f7f7;transform:scale(1.04)}
.review-dialog__eyebrow{margin:0 0 20px;color:#0d7c90;font-size:10px;font-weight:800;letter-spacing:.14em;text-transform:uppercase}
.review-dialog__identity{display:flex;align-items:center;gap:14px;padding-right:44px}
.review-dialog__identity .review-avatar{width:50px;height:50px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex:0 0 50px;background:#e7f3f4;color:#075f6d;font-size:12px;font-weight:800}
.review-dialog__identity h3{margin:0 0 7px;color:#083847;font-size:22px;line-height:1.15;letter-spacing:-.025em}
.review-dialog__identity .review-stars{display:block;color:#f5b301;font-size:16px;letter-spacing:2px}
.review-dialog__surface>p{margin:26px 0 24px;color:#36545e;font-size:17px;line-height:1.72}
.review-dialog__maps{display:inline-flex;min-height:42px;align-items:center;padding:0 15px;border:1px solid #d5e2e4;border-radius:11px;background:#fff;color:#0b7182;font-size:11px;font-weight:750;transition:transform .18s ease,border-color .18s ease,box-shadow .18s ease}
.review-dialog__maps:hover{transform:translateY(-1px);border-color:#bdd4d8;box-shadow:0 8px 20px rgba(8,56,71,.08)}
@keyframes review-dialog-in{from{opacity:0;transform:translateY(10px) scale(.985)}to{opacity:1;transform:none}}
@media(max-width:620px){.review-dialog{width:calc(100% - 22px)}.review-dialog__surface{padding:28px 22px 24px;border-radius:20px}.review-dialog__surface>p{font-size:16px;line-height:1.68}.review-dialog__identity h3{font-size:19px}}
@media(prefers-reduced-motion:reduce){.review-dialog__surface{animation:none}.review-dialog__close,.review-dialog__maps{transition:none}.review-dialog__close:hover,.review-dialog__maps:hover{transform:none}}
'''
reviews_path.write_text(reviews, encoding="utf-8")

# Footer layout + hours/social styling.
styles_path = ROOT / "styles.css"
styles = styles_path.read_text(encoding="utf-8")
if "/* Patch 21: footer hours + social */" not in styles:
    styles += r'''

/* Patch 21: footer hours + social */
.footer-hours-social{min-width:0}
.footer-hours{display:grid;gap:8px;margin-bottom:13px}
.footer-hours>strong{color:#083847;font-size:10px;font-weight:700;line-height:1.4}
.footer-hours>span{display:grid;gap:2px}
.footer-hours b,.footer-hours em{font-size:9px;line-height:1.35;font-style:normal;font-weight:500}
.footer-hours b{color:#526a73}.footer-hours em{color:#71868d}
.footer-instagram{width:max-content;max-width:100%;gap:7px;color:#0b7182!important;font-weight:700}
.footer-instagram svg{width:16px;height:16px;flex:0 0 16px}
.footer-instagram span{overflow-wrap:anywhere;color:inherit!important}
@media(min-width:901px){.footer-grid{grid-template-columns:1.2fr .7fr .7fr 1.15fr 1.05fr;gap:34px}}
'''
styles_path.write_text(styles, encoding="utf-8")
