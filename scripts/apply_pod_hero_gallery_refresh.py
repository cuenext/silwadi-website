from pathlib import Path
import re

PAGE = Path("review/people-of-determination-raha-v1.html")
MARKER = "    /* POD hero + integrated gallery refresh */"

CSS = """
    /* POD hero + integrated gallery refresh */
    .pod-private .container{height:28px}
    .pod-header__inner{height:64px}
    .pod-brand img{width:54px;height:54px}
    .pod-hero{padding:48px 0 66px;background:linear-gradient(180deg,#fff 0%,#fff 66%,#f7fafb 100%);overflow:hidden}
    .pod-hero__intro{max-width:920px;margin:0 auto;text-align:center;padding:0 20px}
    .pod-hero h1{font-size:clamp(46px,5.2vw,68px);max-width:14ch;margin:0 auto;line-height:.98;letter-spacing:-.052em}
    .pod-hero__lead{max-width:650px;margin:20px auto 0;font-size:16px;line-height:1.65}
    .pod-hero__actions{margin-top:26px}
    .pod-hero__gallery{margin-top:40px}
    .pod-hero .pod-clinic{padding:0 0 8px}
    .pod-hero .pod-clinic-viewport{padding-top:8px}
    .pod-hero .pod-clinic-slide img{border-radius:24px}
    .pod-hero .pod-clinic-controls{padding-top:2px}
    @media(max-width:700px){.pod-private{font-size:9px;letter-spacing:.08em}.pod-private .container{height:24px;justify-content:center}.pod-header__inner{height:58px}.pod-brand img{width:48px;height:48px}.pod-header .pod-btn{display:none}.pod-hero{padding:28px 0 44px}.pod-hero__intro{text-align:left;padding:0}.pod-hero .pod-eyebrow{margin-bottom:10px;font-size:10px}.pod-hero h1{font-size:clamp(38px,10.8vw,45px);max-width:10.8ch;margin:0;line-height:.99;letter-spacing:-.048em}.pod-hero__lead{font-size:15px;line-height:1.6;margin:17px 0 0}.pod-hero__actions{margin-top:21px}.pod-hero__actions .pod-btn{width:100%;max-width:370px;min-height:48px}.pod-hero__gallery{margin-top:28px}.pod-hero .pod-clinic{padding:0 0 4px}.pod-clinic-viewport{padding:6px 0 18px}.pod-clinic-controls{padding-inline:20px}}
"""

HERO = """    <section class="pod-hero" id="hero">
      <div class="container pod-hero__intro">
        <p class="pod-eyebrow">People of Determination · Al Raha Mall</p>
        <h1>Dental Care for People of Determination in <span>Abu&nbsp;Dhabi</span></h1>
        <p class="pod-hero__lead">Respectful dental care with an environment and visit plan shaped around the individual patient.</p>
        <div class="pod-hero__actions"><a class="pod-btn pod-btn--primary" href="../contact.html#consultation-form">Request an Appointment</a></div>
      </div>

      <div class="pod-hero__gallery">
        <div class="pod-clinic" id="clinic" aria-label="Accessible dental treatment room photo gallery">
          <div class="pod-clinic-carousel" data-pod-carousel tabindex="0" aria-roledescription="carousel" aria-label="Accessible dental treatment room photos">
            <div class="pod-clinic-viewport" data-pod-viewport>
              <div class="pod-clinic-track">
                <figure class="pod-clinic-slide is-active" data-pod-slide data-pod-focal="center"><img src="../assets/DSCF2857.webp" alt="Wide view of the accessible dental treatment room at Silwadi Dental Center, Al Raha Mall" width="2048" height="1365" fetchpriority="high" decoding="async"></figure>
                <figure class="pod-clinic-slide" data-pod-slide data-pod-focal="center"><img src="../assets/DSCF2848.webp" alt="Wide angled view of the accessible treatment room and dental equipment at Al Raha Mall" width="2048" height="1365" loading="lazy" decoding="async"></figure>
                <figure class="pod-clinic-slide" data-pod-slide data-pod-focal="center"><img src="../assets/DSCF2860.webp" alt="Elevated view of the wheelchair-accessible dental setup at Silwadi Al Raha" width="2048" height="1365" loading="lazy" decoding="async"></figure>
                <figure class="pod-clinic-slide" data-pod-slide data-pod-focal="center"><img src="../assets/DSCF2868.webp" alt="Side view of the wheelchair-accessible dental chair and treatment equipment at Silwadi Al Raha" width="2048" height="1365" loading="lazy" decoding="async"></figure>
                <figure class="pod-clinic-slide" data-pod-slide data-pod-focal="center"><img src="../assets/DSCF2873.webp" alt="Close view of the accessible dental chair and instrument console at Silwadi Al Raha" width="2048" height="1365" loading="lazy" decoding="async"></figure>
                <figure class="pod-clinic-slide" data-pod-slide data-pod-focal="center"><img src="../assets/DSCF2877.webp" alt="Front view of the accessible dental room with treatment equipment at Silwadi Al Raha" width="2048" height="1365" loading="lazy" decoding="async"></figure>
                <figure class="pod-clinic-slide" data-pod-slide data-pod-focal="center"><img src="../assets/DSCF2880.webp" alt="Close detail of the integrated accessible dental equipment beside the wheelchair at Silwadi Al Raha" width="2048" height="1365" loading="lazy" decoding="async"></figure>
              </div>
            </div>
            <div class="container pod-clinic-controls">
              <div class="pod-clinic-status"><span data-pod-current>01</span><span aria-hidden="true"> / </span><span>07</span></div>
              <div class="pod-clinic-controls__buttons">
                <button class="pod-clinic-arrow" type="button" data-pod-prev aria-label="Previous clinic photo"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M14.5 5 7.5 12l7 7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
                <button class="pod-clinic-arrow" type="button" data-pod-next aria-label="Next clinic photo"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m9.5 5 7 7-7 7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>"""


def main():
    html = PAGE.read_text(encoding="utf-8")

    # Repair the malformed partnership opener produced by the first draft patch.
    html = html.replace(
        '<section class="pod-partnership id="partnership">',
        '<section class="pod-partnership" id="partnership">',
    )

    if MARKER not in html:
        if "  </style>" not in html:
            raise SystemExit("Could not find style closing tag")
        html = html.replace("  </style>", CSS + "  </style>", 1)

    if 'class="pod-hero__intro"' not in html:
        pattern = re.compile(
            r'    <section class="pod-hero" id="hero">.*?(?=    <section class="pod-partnership")',
            re.S,
        )
        html, count = pattern.subn(HERO + "\n\n", html, count=1)
        if count != 1:
            raise SystemExit(f"Expected one hero/gallery block, replaced {count}")

    PAGE.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
