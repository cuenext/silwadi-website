from pathlib import Path
import re

page = Path("review/people-of-determination-raha-v1.html")
html = page.read_text(encoding="utf-8")

start = html.index('<div class="pod-partnership__partners"')
end = html.index('<div class="pod-partnership__copy">', start)
new_partners = '''<div class="pod-partnership__partners" aria-label="Official partnership logos">
            <div class="pod-partner-logo-wrap pod-partner-logo-wrap--munir"><img class="pod-partner-logo pod-partner-logo--munir" src="../assets/brand/mohammed-munir-pod-logo.png" alt="Dr. Mohammed Munir Dental Center People of Determination logo"></div>
            <span class="pod-partnership__divider" aria-hidden="true"></span>
            <div class="pod-partner-logo-wrap pod-partner-logo-wrap--zayed"><img class="pod-partner-logo pod-partner-logo--zayed" src="../assets/brand/zayed-authority-pod-logo.png" alt="Zayed Authority for People of Determination logo"></div>
          </div>
          '''
html = html[:start] + new_partners + html[end:]

old_heading = '<h2>Zayed Authority for People of Determination <span>×</span> Dr. Mohammed Munir Dental Center</h2>'
new_heading = '<h2>Official Partnership with Zayed Authority for People of Determination</h2>'
if old_heading not in html:
    raise SystemExit("Old partnership heading not found")
html = html.replace(old_heading, new_heading, 1)

html = re.sub(r'\s*<figcaption class="pod-partnership__badge">.*?</figcaption>', '', html, count=1, flags=re.S)
html = re.sub(r'\s*<div class="pod-partnership__aside"[^>]*>.*?</div>', '', html, count=1, flags=re.S)

css = '''
    /* Approved POD partnership branding refinement */
    .pod-partnership__partners{display:flex;align-items:center;gap:18px;margin:0 0 32px;min-height:88px}
    .pod-partner-logo-wrap{display:flex;align-items:center;justify-content:center;background:#fff;border:1px solid rgba(255,255,255,.38);border-radius:16px;box-shadow:0 10px 28px rgba(0,20,27,.14)}
    .pod-partner-logo-wrap--munir{width:96px;height:88px;padding:8px}
    .pod-partner-logo-wrap--zayed{min-width:238px;height:88px;padding:12px 18px}
    .pod-partner-logo{display:block;object-fit:contain}
    .pod-partner-logo--munir{width:76px;height:76px}
    .pod-partner-logo--zayed{width:204px;height:auto}
    .pod-partnership__divider{display:block;width:1px;height:64px;background:rgba(255,255,255,.24)}
    .pod-partnership__visual{margin:0;min-width:0}
    .pod-partnership__copy h2{max-width:760px}
    @media(max-width:700px){.pod-partnership__partners{gap:10px;flex-wrap:nowrap;margin-bottom:26px}.pod-partner-logo-wrap--munir{width:76px;height:70px}.pod-partner-logo-wrap--zayed{min-width:0;width:190px;height:70px;padding:10px 14px}.pod-partner-logo--munir{width:58px;height:58px}.pod-partner-logo--zayed{width:158px}.pod-partnership__divider{height:48px}}
'''
if "Approved POD partnership branding refinement" not in html:
    html = html.replace("  </style>", css + "  </style>", 1)

page.write_text(html, encoding="utf-8")

test = Path("tests/test_private_pod_review.py")
txt = test.read_text(encoding="utf-8").replace("../assets/brand/mohammed-munir-pod-logo.jpg", "../assets/brand/mohammed-munir-pod-logo.png")
test.write_text(txt, encoding="utf-8")
