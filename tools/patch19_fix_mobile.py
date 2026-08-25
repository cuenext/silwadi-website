from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
WHATSAPP_URL = "https://wa.me/971506260418?text=Hello%20Silwadi%20Dental%20Center%2C%20I%27d%20like%20to%20book%20an%20appointment."
WA_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M12.04 2a9.84 9.84 0 0 0-8.43 14.91L2 22l5.22-1.56A9.9 9.9 0 1 0 12.04 2Zm0 17.98a8.03 8.03 0 0 1-4.09-1.12l-.29-.17-3.1.93.94-3.02-.19-.31A8.04 8.04 0 1 1 12.04 19.98Zm4.4-6.03c-.24-.12-1.43-.7-1.65-.78-.22-.08-.38-.12-.54.12-.16.24-.62.78-.76.94-.14.16-.28.18-.52.06-.24-.12-1.01-.37-1.93-1.19-.71-.64-1.2-1.42-1.34-1.66-.14-.24-.02-.37.1-.49.11-.11.24-.28.36-.42.12-.14.16-.24.24-.4.08-.16.04-.3-.02-.42-.06-.12-.54-1.3-.74-1.78-.19-.47-.39-.4-.54-.41h-.46c-.16 0-.42.06-.64.3-.22.24-.84.82-.84 2s.86 2.32.98 2.48c.12.16 1.7 2.59 4.11 3.63.57.25 1.02.4 1.37.51.58.18 1.1.16 1.51.1.46-.07 1.43-.58 1.63-1.15.2-.57.2-1.06.14-1.16-.06-.1-.22-.16-.46-.28Z"/></svg>'

for page in ROOT.rglob("*.html"):
    text = page.read_text(encoding="utf-8")
    if 'class="mobile-actionbar"' not in text:
        continue
    prefix = "../" if page.parent.name in {"doctors", "treatments"} else ""
    replacement = (
        '<div class="mobile-actionbar" aria-label="Quick contact">'
        f'<a class="mobile-actionbar__whatsapp" href="{WHATSAPP_URL}" target="_blank" rel="noopener" aria-label="WhatsApp Silwadi Dental Center">{WA_ICON}<span>WhatsApp</span></a>'
        '<a href="tel:+97126262042">Call</a>'
        f'<a class="mobile-actionbar__primary" href="{prefix}contact.html#consultation">Book</a>'
        '</div>'
    )
    text = re.sub(r'<div class="mobile-actionbar"[^>]*>.*?</div>', replacement, text, count=1, flags=re.S)
    page.write_text(text, encoding="utf-8")
