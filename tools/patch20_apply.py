from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def wrap_abu_dhabi_headings(html: str) -> str:
    def repl(match):
        opening, inner, closing = match.groups()
        plain = re.sub(r"<[^>]+>", "", inner)
        if "Abu Dhabi" not in plain or 'class="nowrap-place"' in inner:
            return match.group(0)
        return opening + inner.replace("Abu Dhabi", '<span class="nowrap-place">Abu Dhabi</span>') + closing
    return re.sub(r'(<h[12][^>]*>)(.*?)(</h[12]>)', repl, html, flags=re.S)


for path in ROOT.rglob("*.html"):
    if any(part in {"node_modules", ".git"} for part in path.parts):
        continue
    html = path.read_text(encoding="utf-8")
    html = re.sub(
        r'<div class="utility-strip">.*?</div></div></div>',
        '',
        html,
        count=1,
        flags=re.S,
    )
    # Remove only the directional arrow attached to each mega-menu service option.
    html = html.replace('</small><b aria-hidden="true">→</b>', '</small>')
    html = wrap_abu_dhabi_headings(html)
    path.write_text(html, encoding="utf-8")

# Homepage: give every visible treatment row its own relevant image and remove the unequal 3-image strip.
index_path = ROOT / "index.html"
index = index_path.read_text(encoding="utf-8")
index = re.sub(
    r'<div class="home-service-visuals reveal".*?</div><div class="treatment-paths">',
    '<div class="treatment-paths">',
    index,
    count=1,
    flags=re.S,
)
thumbs = {
    "01": ("prosthodontics.webp", "Prosthodontics and implantology"),
    "02": ("orthodontics.webp", "Orthodontic care"),
    "03": ("cosmetics.webp", "Cosmetic dentistry"),
    "04": ("preventive-dentistry.webp", "Preventive dental care"),
    "05": ("periodontics.webp", "Periodontal care"),
}
for number, (filename, alt) in thumbs.items():
    old = f'<span class="treatment-path__index">{number}</span><div>'
    new = (
        f'<span class="treatment-path__index">{number}</span>'
        f'<span class="treatment-path__thumb"><img src="assets/services/{filename}" alt="{alt}" '
        f'width="1200" height="900" loading="lazy" decoding="async"></span><div>'
    )
    index = index.replace(old, new, 1)
index_path.write_text(index, encoding="utf-8")

# About: Dr. Munir belongs in the leadership section once; use a different teeth-focused image in the story mosaic.
about_path = ROOT / "about.html"
about = about_path.read_text(encoding="utf-8")
about = about.replace(
    '<figure><img src="assets/doctors/optimized/dr-munir-silwadi.webp" alt="Dr. Munir Silwadi at Silwadi Dental Center" width="720" height="720" loading="lazy" decoding="async"></figure>',
    '<figure><img src="assets/services/teeth-whitening.webp" alt="Professional smile and teeth care at Silwadi Dental Center" width="1200" height="900" loading="lazy" decoding="async"></figure>',
    1,
)
about_path.write_text(about, encoding="utf-8")

# Reviews: real gold stars and stronger premium visual hierarchy.
reviews_path = ROOT / "home-reviews.css"
reviews = reviews_path.read_text(encoding="utf-8")
reviews = reviews.replace('color:#946000;letter-spacing:2px;font-size:15px', 'color:#f5b301;letter-spacing:2px;font-size:17px')
if "/* Patch 20: review emphasis + service thumbnails */" not in reviews:
    reviews += r'''

/* Patch 20: review emphasis + service thumbnails */
.home-google-reviews{background:linear-gradient(180deg,#f8fbfc 0%,#eef5f6 100%)}
.google-rating-card{position:relative;overflow:hidden;border-color:#d4e1e3;background:linear-gradient(145deg,#fff 0%,#fbfdfd 72%,#fff9e8 100%);box-shadow:0 18px 46px rgba(8,56,71,.11),inset 0 1px 0 rgba(255,255,255,.9);transition:transform .22s ease,box-shadow .22s ease,border-color .22s ease}
.google-rating-card::before{content:"";position:absolute;inset:0 0 auto;height:3px;background:linear-gradient(90deg,#f5b301,#ffd86a,#f5b301)}
.google-rating-card:hover{transform:translateY(-3px);border-color:#c8dadd;box-shadow:0 24px 54px rgba(8,56,71,.14),inset 0 1px 0 rgba(255,255,255,.95)}
.google-rating-card__stars{color:#f5b301;text-shadow:0 1px 0 rgba(130,83,0,.12)}
.google-review-card{position:relative;border-color:#d4e1e3;background:linear-gradient(150deg,#fff 0%,#fbfdfd 100%);box-shadow:0 12px 32px rgba(8,56,71,.075);transition:transform .22s ease,box-shadow .22s ease,border-color .22s ease}
.google-review-card::after{content:"";position:absolute;left:22px;right:22px;bottom:0;height:2px;border-radius:2px;background:linear-gradient(90deg,transparent,rgba(245,179,1,.72),transparent);opacity:.55}
.google-review-card:hover{transform:translateY(-4px);border-color:#c7dadd;box-shadow:0 20px 44px rgba(8,56,71,.12)}
.google-review-card__top div>.review-stars{display:block;color:#f5b301;font-size:14px;line-height:1;letter-spacing:1.5px;margin-top:2px;text-shadow:0 1px 0 rgba(130,83,0,.10)}
.treatment-path__thumb{width:64px;aspect-ratio:4/3;display:block;overflow:hidden;border-radius:12px;border:1px solid #d8e4e6;background:#edf3f4;box-shadow:0 7px 18px rgba(8,56,71,.07)}
.treatment-path__thumb img{display:block;width:100%;height:100%;object-fit:cover;transition:transform .3s ease,filter .3s ease}
.treatment-path:hover .treatment-path__thumb img{transform:scale(1.06);filter:saturate(1.04)}
@media(max-width:620px){.treatment-path__thumb{width:54px;border-radius:10px}}
@media(prefers-reduced-motion:reduce){.google-rating-card,.google-review-card,.treatment-path__thumb img{transition:none}.google-rating-card:hover,.google-review-card:hover{transform:none}.treatment-path:hover .treatment-path__thumb img{transform:none}}
'''
reviews_path.write_text(reviews, encoding="utf-8")

# Sitewide glass menu, compact service thumbnails and location-name wrapping.
styles_path = ROOT / "styles.css"
styles = styles_path.read_text(encoding="utf-8")
if "/* Patch 20: glass services + tactile UI */" not in styles:
    styles += r'''

/* Patch 20: glass services + tactile UI */
.nowrap-place{display:inline-block;white-space:nowrap}
.treatment-path{grid-template-columns:38px 64px minmax(0,1fr) 32px;gap:18px;padding:17px 12px;border:1px solid transparent;border-bottom-color:var(--line);border-radius:12px;transition:background .22s ease,border-color .22s ease,box-shadow .22s ease,transform .18s ease,padding .22s ease}
.treatment-path:hover{padding-left:16px;padding-right:16px;background:rgba(247,251,251,.94);border-color:#dce7e9;box-shadow:0 10px 28px rgba(8,56,71,.055);transform:translateY(-1px)}
.treatment-path:active{transform:translateY(0) scale(.995)}
.services-mega{background:rgba(250,253,253,.90);border-color:rgba(200,218,222,.9);backdrop-filter:blur(22px) saturate(150%);-webkit-backdrop-filter:blur(22px) saturate(150%);box-shadow:0 24px 70px rgba(8,56,71,.16),inset 0 1px 0 rgba(255,255,255,.94)}
.services-mega__grid{gap:10px}
.services-mega__grid>a{position:relative;overflow:hidden;border-radius:14px;background:rgba(255,255,255,.58);border:1px solid rgba(206,222,225,.78);backdrop-filter:blur(18px) saturate(145%);-webkit-backdrop-filter:blur(18px) saturate(145%);box-shadow:inset 0 1px 0 rgba(255,255,255,.88),0 5px 16px rgba(8,56,71,.035);transition:transform .2s ease,background .2s ease,border-color .2s ease,box-shadow .2s ease}
.site-nav .services-mega__grid>a{border-radius:14px;background:rgba(255,255,255,.58);border-color:rgba(206,222,225,.78);padding:13px 14px 12px}
.services-mega__grid>a::before{content:"";position:absolute;top:-45%;left:-70%;width:54%;height:190%;pointer-events:none;transform:rotate(18deg);background:linear-gradient(90deg,transparent,rgba(255,255,255,.88),transparent);opacity:0;transition:left .42s ease,opacity .22s ease}
.site-nav .services-mega__grid>a:hover,.site-nav .services-mega__grid>a:focus-visible{background:rgba(255,255,255,.84);border-color:#c7dde1;transform:translateY(-2px) scale(1.008);box-shadow:0 11px 25px rgba(8,56,71,.075),inset 0 1px 0 #fff}
.services-mega__grid>a:hover::before,.services-mega__grid>a:focus-visible::before{left:118%;opacity:.9}
.services-mega__grid>a:active{transform:translateY(0) scale(.982)!important;box-shadow:inset 0 2px 7px rgba(8,56,71,.08)!important}
.mobile-services__links a{position:relative;overflow:hidden;background:rgba(248,252,252,.86)!important;backdrop-filter:blur(14px) saturate(140%);-webkit-backdrop-filter:blur(14px) saturate(140%);box-shadow:inset 0 1px 0 #fff,0 5px 14px rgba(8,56,71,.035);transition:transform .18s ease,background .18s ease,box-shadow .18s ease}
.mobile-services__links a:active{transform:scale(.975);background:#fff!important;box-shadow:inset 0 2px 8px rgba(8,56,71,.08)}
@media(max-width:720px){.treatment-path{grid-template-columns:30px 54px minmax(0,1fr) 22px;gap:12px;padding:14px 6px}.treatment-path:hover{padding-left:8px;padding-right:8px}}
@media(prefers-reduced-motion:reduce){.treatment-path,.services-mega__grid>a,.mobile-services__links a{transition:none!important}.services-mega__grid>a::before{display:none}.treatment-path:hover,.site-nav .services-mega__grid>a:hover,.site-nav .services-mega__grid>a:focus-visible,.mobile-services__links a:active{transform:none!important}}
'''
styles_path.write_text(styles, encoding="utf-8")
