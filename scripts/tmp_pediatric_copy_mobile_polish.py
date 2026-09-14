from pathlib import Path

page = Path('review/pediatric-dentistry-v1.html')
text = page.read_text(encoding='utf-8')


def replace_once(old, new):
    global text
    if old not in text:
        raise SystemExit(f'Expected fragment not found: {old[:120]}')
    text = text.replace(old, new, 1)


replace_once(
    '.pd-breadcrumb{display:flex;gap:8px;align-items:center;font-size:11px;color:#809199;margin-bottom:34px}',
    '.pd-breadcrumb{display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-size:11px;color:#809199;margin-bottom:34px}'
)
replace_once(
    '.pd-hero__grid{display:grid;grid-template-columns:minmax(0,1.12fr) minmax(340px,.88fr);gap:72px;align-items:end}',
    '.pd-hero__grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(380px,.82fr);gap:88px;align-items:center}'
)
replace_once(
    '.pd-hero__details{max-width:560px;padding:0 0 7px}',
    '.pd-hero__details{max-width:520px;padding:0}'
)
replace_once(
    '    .pd-hero__micro{display:flex;gap:26px;flex-wrap:wrap;margin-top:31px;padding-top:24px;border-top:1px solid var(--pd-line)}\n    .pd-hero__micro span{color:#6c8087;font-size:11px;font-weight:700}\n',
    ''
)
replace_once(
    '@media(max-width:1000px){.pd-review-nav{display:none}.pd-hero__grid{grid-template-columns:1fr;gap:28px}.pd-hero__details{max-width:700px}.pd-visit-shell,.pd-faq-wrap{grid-template-columns:1fr;gap:42px}.pd-visit-copy{position:static}.pd-specialist-card{grid-template-columns:300px 1fr}.pd-specialist-body{padding-left:46px}}',
    '@media(max-width:1000px){.pd-review-nav{display:none}.pd-hero__grid{grid-template-columns:1fr;gap:24px}.pd-hero__details{max-width:700px}.pd-visit-shell,.pd-faq-wrap{grid-template-columns:1fr;gap:42px}.pd-visit-copy{position:static}.pd-specialist-card{grid-template-columns:300px 1fr}.pd-specialist-body{padding-left:46px}}'
)
replace_once(
    '@media(max-width:760px){.pd-private .container span:last-child{display:none}.pd-review-header__inner{height:70px}.pd-review-actions .pd-btn--secondary{display:none}.pd-section{padding:72px 0}.pd-hero{padding:22px 0 26px}.pd-breadcrumb{margin-bottom:24px}.pd-hero__grid{gap:24px}.pd-hero h1{font-size:47px;max-width:10.8ch}.pd-hero__lead{font-size:15px}.pd-hero__details{padding-bottom:0}.pd-care-grid{grid-template-columns:1fr}.pd-care-card{min-height:auto;padding:27px 25px 29px}.pd-care-card__top{margin-bottom:27px}.pd-specialist-card{grid-template-columns:1fr}.pd-specialist-photo{height:470px;min-height:0}.pd-specialist-body{padding:42px 0}.pd-specialist-body h2{font-size:46px}.pd-consultation__box{padding:34px 28px;display:block}.pd-consultation__box .pd-btn{margin-top:24px}.pd-visit-step{grid-template-columns:58px 1fr;gap:15px}.pd-faq-wrap{gap:30px}}',
    '@media(max-width:760px){.pd-private .container span:last-child{display:none}.pd-review-header__inner{height:70px}.pd-review-actions .pd-btn--secondary{display:none}.pd-section{padding:64px 0}.pd-hero{padding:20px 0 22px}.pd-breadcrumb{margin-bottom:22px}.pd-hero__grid{gap:20px}.pd-hero h1{font-size:clamp(42px,12.5vw,47px);max-width:10.8ch}.pd-hero__lead{font-size:15px;line-height:1.65}.pd-hero__details{padding:0}.pd-care-grid{grid-template-columns:1fr}.pd-care-card{min-height:auto;padding:25px 22px 27px}.pd-care-card__top{margin-bottom:24px}.pd-specialist-card{grid-template-columns:1fr}.pd-specialist-photo{height:430px;min-height:0}.pd-specialist-body{padding:38px 0}.pd-specialist-body h2{font-size:42px}.pd-consultation__box{padding:32px 26px;display:block}.pd-consultation__box .pd-btn{margin-top:22px}.pd-visit-step{grid-template-columns:54px 1fr;gap:14px}.pd-faq-wrap{gap:28px}}'
)
replace_once(
    '    @media(prefers-reduced-motion:reduce){.pd-clinic-viewport{scroll-behavior:auto}.pd-clinic-slide{transition:none}}',
    '    @media(max-width:480px){:root{--pd-slide-width:90vw}.pd-review-actions{display:none}.pd-review-header__inner{height:64px}.pd-review-brand img{width:56px;height:56px}.pd-hero__actions{display:grid;grid-template-columns:1fr}.pd-hero__actions .pd-btn{width:100%}.pd-clinic-track{padding-inline:5vw}.pd-clinic-controls{padding-inline:20px}.pd-specialist-photo{height:390px}.pd-specialist-body h2{font-size:38px}.pd-specialist-actions{display:grid;grid-template-columns:1fr}.pd-specialist-actions .pd-btn{width:100%}.pd-consultation__box{padding:28px 22px}.pd-consultation__box .pd-btn{width:100%}.pd-faq summary{font-size:15px}.pd-faq p{padding-right:34px}}\n    @media(prefers-reduced-motion:reduce){.pd-clinic-viewport{scroll-behavior:auto}.pd-clinic-slide{transition:none}}'
)
replace_once(
    '<p class="pd-eyebrow">Pediatric Dentistry · Pedodontics</p>',
    '<p class="pd-eyebrow">Specialist dental care for children</p>'
)
replace_once(
    '<p class="pd-hero__lead">Specialist dental care for children at Al Raha Mall — focused on prevention, comfort and the right treatment for each stage of a growing smile.</p>',
    '<p class="pd-hero__lead">Care planned around your child’s age, dental needs and clinical findings, with prevention, restorative treatment and dental trauma assessment when appropriate.</p>'
)
replace_once(
    '            <div class="pd-hero__micro"><span>Al Raha Mall</span><span>Children\'s dental care</span><span>Specialist pediatric dentist</span></div>\n',
    ''
)

page.write_text(text, encoding='utf-8')
