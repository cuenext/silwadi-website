from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTAGRAM = "https://www.instagram.com/dr.munirsilwadidental/"

public_pages = [
    *ROOT.glob("*.html"),
    *(ROOT / "doctors").glob("*.html"),
    *(ROOT / "treatments").glob("*.html"),
]

hours_block = (
    '<div class="footer-opening-hours"><h3>Opening hours</h3>'
    '<span>Sunday - Wednesday</span><strong>09:00 AM to 09:00 PM</strong>'
    '<span>Thursday &amp; Saturday</span><strong>09:00 AM to 06:00 PM</strong>'
    '<span class="footer-opening-hours__closed">Friday: Closed</span></div>'
)
instagram_link = (
    f'<a class="footer-social-link" href="{INSTAGRAM}" target="_blank" rel="noopener" '
    'aria-label="Follow Silwadi Dental Center on Instagram">'
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<path fill="currentColor" d="M7.8 2h8.4A5.8 5.8 0 0 1 22 7.8v8.4a5.8 5.8 0 0 1-5.8 5.8H7.8A5.8 5.8 0 0 1 2 16.2V7.8A5.8 5.8 0 0 1 7.8 2Zm-.2 2A3.6 3.6 0 0 0 4 7.6v8.8A3.6 3.6 0 0 0 7.6 20h8.8a3.6 3.6 0 0 0 3.6-3.6V7.6A3.6 3.6 0 0 0 16.4 4H7.6Zm9.15 1.5a1.35 1.35 0 1 1 0 2.7 1.35 1.35 0 0 1 0-2.7ZM12 6.75A5.25 5.25 0 1 1 6.75 12 5.25 5.25 0 0 1 12 6.75Zm0 2A3.25 3.25 0 1 0 15.25 12 3.25 3.25 0 0 0 12 8.75Z"/>'
    '</svg><span>Instagram <strong>@dr.munirsilwadidental</strong></span></a>'
)

for path in public_pages:
    html = path.read_text(encoding="utf-8")
    if 'class="footer-opening-hours"' not in html:
        marker = '<div><h3>Contact</h3>'
        if marker not in html:
            raise RuntimeError(f"Footer contact marker missing in {path}")
        html = html.replace(marker, hours_block + marker, 1)
    if INSTAGRAM not in html:
        marker = '</p></div><div><h3>Care</h3>'
        if marker not in html:
            raise RuntimeError(f"Footer brand marker missing in {path}")
        html = html.replace(marker, '</p>' + instagram_link + '</div><div><h3>Care</h3>', 1)
    path.write_text(html, encoding="utf-8")

# Homepage rating, accessible review expansion, and social schema.
home_path = ROOT / "index.html"
home = home_path.read_text(encoding="utf-8")
old_stars = '<span class="google-rating-card__stars" aria-label="4.6 out of 5 stars">★★★★★</span>'
new_stars = (
    '<span class="google-rating-card__stars" aria-label="4.6 out of 5 stars">'
    '<span class="rating-star rating-star--full" aria-hidden="true">★</span>'
    '<span class="rating-star rating-star--full" aria-hidden="true">★</span>'
    '<span class="rating-star rating-star--full" aria-hidden="true">★</span>'
    '<span class="rating-star rating-star--full" aria-hidden="true">★</span>'
    '<span class="rating-star rating-star--half" aria-hidden="true">★</span>'
    '</span>'
)
if old_stars in home:
    home = home.replace(old_stars, new_stars, 1)

if 'data-review-expand' not in home:
    start = home.index('<div class="google-reviews-group">')
    boundary = home.index('<div class="google-reviews-group" aria-hidden="true">', start)
    visible_group = home[start:boundary]
    visible_group = visible_group.replace(
        '<article class="google-review-card">',
        '<article class="google-review-card" data-review-expand tabindex="0" role="button" aria-haspopup="dialog" aria-label="Open patient review">'
    )
    visible_group = visible_group.replace(
        '</p></article>',
        '</p><span class="review-card__hint">Tap to read</span></article>'
    )
    home = home[:start] + visible_group + home[boundary:]

if 'data-review-dialog' not in home:
    review_end = '</div></div></div></section><section class="section" id="locations">'
    dialog = (
        '</div></div></div>'
        '<dialog class="review-dialog" data-review-dialog aria-labelledby="reviewDialogName">'
        '<div class="review-dialog__surface">'
        '<button class="review-dialog__close" type="button" data-review-close aria-label="Close review">×</button>'
        '<div class="review-dialog__top"><span class="review-avatar" data-review-avatar></span><div>'
        '<strong id="reviewDialogName" data-review-name>Patient review</strong><span>Google review</span>'
        '<span class="review-stars" data-review-stars aria-label="5 out of 5 stars">★★★★★</span></div></div>'
        '<p data-review-text></p>'
        '<a class="review-dialog__maps" href="https://maps.app.goo.gl/Ln2vEZmQmgWjb3ETA" target="_blank" rel="noopener">Read reviews on Google Maps →</a>'
        '</div></dialog></section><section class="section" id="locations">'
    )
    if review_end not in home:
        raise RuntimeError("Review section boundary not found")
    home = home.replace(review_end, dialog, 1)

if '"sameAs":["https://www.instagram.com/dr.munirsilwadidental/"]' not in home:
    schema_marker = '"image":"https://silwadi.ae/assets/silwadi-logo-official.png","medicalSpecialty"'
    schema_replacement = '"image":"https://silwadi.ae/assets/silwadi-logo-official.png","sameAs":["https://www.instagram.com/dr.munirsilwadidental/"],"medicalSpecialty"'
    if schema_marker not in home:
        raise RuntimeError("Homepage Dentist schema marker not found")
    home = home.replace(schema_marker, schema_replacement, 1)

home_path.write_text(home, encoding="utf-8")

# Review visuals and dialog styling.
reviews_path = ROOT / "home-reviews.css"
reviews = reviews_path.read_text(encoding="utf-8")
if "/* Patch 21: half-star rating + expandable reviews */" not in reviews:
    reviews += r'''

/* Patch 21: half-star rating + expandable reviews */
.google-rating-card__stars{display:flex;align-items:center;gap:2px;letter-spacing:0}
.rating-star{display:inline-block;font-size:18px;line-height:1;color:#f5b301}
.rating-star--half{background:linear-gradient(90deg,#f5b301 0 50%,#d5dee0 50% 100%);-webkit-background-clip:text;background-clip:text;color:transparent}
.google-review-card[data-review-expand]{cursor:pointer;outline:none}
.google-review-card[data-review-expand]:focus-visible{border-color:#8fc2ca;box-shadow:0 0 0 4px rgba(13,124,144,.13),0 20px 44px rgba(8,56,71,.12)}
.review-card__hint{margin-top:auto;padding-top:16px;color:#0b7182;font-size:9px;font-weight:800;letter-spacing:.02em}
.review-dialog{width:min(620px,calc(100% - 32px));max-height:min(720px,calc(100vh - 48px));padding:0;border:0;border-radius:24px;background:transparent;color:#173943;box-shadow:none}
.review-dialog::backdrop{background:rgba(4,29,37,.54);backdrop-filter:blur(7px);-webkit-backdrop-filter:blur(7px)}
.review-dialog__surface{position:relative;padding:34px 34px 30px;border:1px solid rgba(214,226,228,.94);border-radius:24px;background:linear-gradient(145deg,rgba(255,255,255,.98),rgba(248,252,252,.98));box-shadow:0 30px 90px rgba(4,35,45,.24)}
.review-dialog__close{position:absolute;top:16px;right:16px;width:38px;height:38px;border:1px solid #d7e3e5;border-radius:50%;background:#fff;color:#31545e;font-size:24px;line-height:1;cursor:pointer;transition:transform .18s ease,background .18s ease}
.review-dialog__close:hover{background:#f0f6f7;transform:scale(1.04)}
.review-dialog__top{display:flex;align-items:center;gap:14px;padding-right:46px;margin-bottom:22px}
.review-dialog__top .review-avatar{width:48px;height:48px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex:0 0 48px;background:#e7f3f4;color:#075f6d;font-size:11px;font-weight:800}
.review-dialog__top>div{display:flex;flex-direction:column;gap:4px}.review-dialog__top strong{color:#083847;font-size:15px}.review-dialog__top>div>span:not(.review-stars){color:#60777f;font-size:10px}.review-dialog__top .review-stars{color:#f5b301;font-size:16px;letter-spacing:1.5px}
.review-dialog p{margin:0;color:#385962;font-size:16px;line-height:1.78}
.review-dialog__maps{display:inline-flex;margin-top:24px;color:#0b7182;font-size:11px;font-weight:800}
@media(max-width:620px){.review-dialog{width:calc(100% - 22px);max-height:calc(100vh - 28px);border-radius:20px}.review-dialog__surface{padding:28px 22px 24px;border-radius:20px}.review-dialog p{font-size:15px;line-height:1.72}.review-card__hint{font-size:8px}}
@media(prefers-reduced-motion:reduce){.review-dialog__close{transition:none}.review-dialog__close:hover{transform:none}}
'''
reviews_path.write_text(reviews, encoding="utf-8")

# Footer hour/social presentation.
styles_path = ROOT / "styles.css"
styles = styles_path.read_text(encoding="utf-8")
if "/* Patch 21: footer hours + official social */" not in styles:
    styles += r'''

/* Patch 21: footer hours + official social */
.site-footer .footer-grid{grid-template-columns:1.4fr .72fr .72fr 1.08fr 1.18fr;gap:34px}
.footer-opening-hours{display:flex!important;flex-direction:column;gap:5px}
.footer-opening-hours h3{margin-bottom:9px}
.footer-opening-hours span{color:#60777f;font-size:9px;line-height:1.4}
.footer-opening-hours strong{color:#183f4a;font-size:10px;font-weight:700;line-height:1.45;margin-bottom:5px}
.footer-opening-hours__closed{margin-top:2px;color:#31545e!important;font-weight:700}
.footer-social-link{display:inline-flex!important;align-items:center;gap:8px;width:max-content;max-width:100%;margin-top:14px;padding:8px 10px;border:1px solid #d7e4e6;border-radius:10px;background:#fff;color:#31545e!important;transition:transform .18s ease,border-color .18s ease,box-shadow .18s ease}
.footer-social-link svg{width:16px;height:16px;flex:0 0 16px;color:#0d7c90}.footer-social-link span{font-size:9px!important}.footer-social-link strong{color:#083847;font-weight:750}
.footer-social-link:hover{transform:translateY(-1px);border-color:#bdd6da;box-shadow:0 7px 18px rgba(8,56,71,.06)}
@media(max-width:980px){.site-footer .footer-grid{grid-template-columns:1.3fr 1fr 1fr;gap:32px}.footer-brand-block{grid-column:1/-1}}
@media(max-width:620px){.site-footer .footer-grid{grid-template-columns:1fr;gap:26px}.footer-brand-block{grid-column:auto}.footer-social-link{margin-top:10px}}
@media(prefers-reduced-motion:reduce){.footer-social-link{transition:none}.footer-social-link:hover{transform:none}}
'''
styles_path.write_text(styles, encoding="utf-8")

# Review dialog behavior.
app_path = ROOT / "app.js"
app = app_path.read_text(encoding="utf-8")
if "// Expandable Google review dialog." not in app:
    app += r'''

// Expandable Google review dialog.
const reviewDialog = document.querySelector('[data-review-dialog]');
const reviewClose = document.querySelector('[data-review-close]');
const reviewTriggers = [...document.querySelectorAll('[data-review-expand]')];

function openReviewDialog(card) {
  if (!reviewDialog || !card) return;
  const name = card.querySelector('.google-review-card__top strong')?.textContent?.trim() || 'Patient review';
  const avatar = card.querySelector('.review-avatar')?.textContent?.trim() || '';
  const text = card.querySelector('p')?.textContent?.trim() || '';
  const stars = card.querySelector('.review-stars');
  const starText = stars?.textContent?.trim() || '★★★★★';
  const starLabel = stars?.getAttribute('aria-label') || '5 out of 5 stars';
  const dialogName = reviewDialog.querySelector('[data-review-name]');
  const dialogAvatar = reviewDialog.querySelector('[data-review-avatar]');
  const dialogText = reviewDialog.querySelector('[data-review-text]');
  const dialogStars = reviewDialog.querySelector('[data-review-stars]');
  if (dialogName) dialogName.textContent = name;
  if (dialogAvatar) dialogAvatar.textContent = avatar;
  if (dialogText) dialogText.textContent = text;
  if (dialogStars) {
    dialogStars.textContent = starText;
    dialogStars.setAttribute('aria-label', starLabel);
  }
  if (typeof reviewDialog.showModal === 'function') reviewDialog.showModal();
  else reviewDialog.setAttribute('open', '');
}

reviewTriggers.forEach(card => {
  card.addEventListener('click', () => openReviewDialog(card));
  card.addEventListener('keydown', event => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      openReviewDialog(card);
    }
  });
});

reviewClose?.addEventListener('click', () => reviewDialog?.close());
reviewDialog?.addEventListener('click', event => {
  if (event.target === reviewDialog) reviewDialog.close();
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && reviewDialog?.open) reviewDialog.close();
});
'''
app_path.write_text(app, encoding="utf-8")
