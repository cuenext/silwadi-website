from __future__ import annotations

from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
import json
import re
import ssl
import time
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "audit-results"
OUT.mkdir(exist_ok=True)
BASE = "https://silwadi.ae/"
BOOKING_ENDPOINT = "https://booking.silwadi.ae/booking-submit.php"
errors: list[str] = []
warnings: list[str] = []
info: list[str] = []


class Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.dir = ""
        self.title: list[str] = []
        self.in_title = False
        self.meta: list[dict[str, str]] = []
        self.links: list[tuple[str, dict[str, str]]] = []
        self.images: list[dict[str, str]] = []
        self.buttons: list[dict] = []
        self.forms: list[dict[str, str]] = []
        self.fields: list[tuple[str, dict[str, str]]] = []
        self.ids: list[str] = []
        self.h1 = 0
        self.scripts: list[str] = []
        self.styles: list[str] = []
        self.jsonld: list[str] = []
        self.in_json = False
        self.jsonbuf: list[str] = []
        self.skip_depth = 0
        self.visible: list[str] = []
        self.current_button = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang", "")
            self.dir = a.get("dir", "")
        if tag == "title":
            self.in_title = True
        if tag == "meta":
            self.meta.append(a)
        if tag == "link":
            self.links.append(("link", a))
            if "stylesheet" in (a.get("rel") or "").lower() and a.get("href"):
                self.styles.append(a["href"])
        if tag == "a":
            self.links.append(("a", a))
        if tag == "img":
            self.images.append(a)
        if tag == "button":
            self.current_button = {"attrs": a, "text": []}
            self.buttons.append(self.current_button)
        if tag == "form":
            self.forms.append(a)
        if tag in ("input", "select", "textarea"):
            self.fields.append((tag, a))
        if a.get("id"):
            self.ids.append(a["id"])
        if tag == "h1":
            self.h1 += 1
        if tag == "script":
            if a.get("src"):
                self.scripts.append(a["src"])
            if a.get("type") == "application/ld+json":
                self.in_json = True
                self.jsonbuf = []
            self.skip_depth += 1
        if tag == "style":
            self.skip_depth += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "button":
            self.current_button = None
        if tag == "script":
            if self.in_json:
                self.jsonld.append("".join(self.jsonbuf).strip())
                self.in_json = False
            if self.skip_depth:
                self.skip_depth -= 1
        if tag == "style" and self.skip_depth:
            self.skip_depth -= 1

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)
        if self.in_json:
            self.jsonbuf.append(data)
        if self.current_button is not None:
            self.current_button["text"].append(data)
        if not self.skip_depth and data.strip():
            self.visible.append(data.strip())


def local_file(url: str) -> Path:
    path = urlparse(url).path
    if path in ("", "/"):
        return ROOT / "index.html"
    p = ROOT / path.lstrip("/")
    return p / "index.html" if path.endswith("/") else p


def internal_local_target(source: Path, href: str, absolute_url: str) -> Path:
    parsed = urlparse(absolute_url)
    if parsed.path == "/":
        return ROOT / "index.html"
    target = ROOT / parsed.path.lstrip("/")
    if parsed.path.endswith("/"):
        target = target / "index.html"
    return target


ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
urls = [node.text.strip() for node in ET.parse(ROOT / "sitemap.xml").findall(".//s:loc", ns)]
info.append(f"SITEMAP_URLS={len(urls)}")
if len(urls) != len(set(urls)):
    errors.append("SITEMAP duplicate <loc> entries")

parsed_pages: dict[str, tuple[Path, Parser, str]] = {}
titles = defaultdict(list)
descriptions = defaultdict(list)

for url in urls:
    file = local_file(url)
    if not file.exists():
        errors.append(f"SITEMAP_MISSING_FILE | {url} -> {file.relative_to(ROOT)}")
        continue

    raw = file.read_text(encoding="utf-8", errors="replace")
    p = Parser()
    p.feed(raw)
    parsed_pages[url] = (file, p, raw)

    title = "".join(p.title).strip()
    meta_name = {m.get("name", "").lower(): m.get("content", "").strip() for m in p.meta if m.get("name")}
    meta_prop = {m.get("property", ""): m.get("content", "").strip() for m in p.meta if m.get("property")}
    description = meta_name.get("description", "")
    canonicals = [a.get("href", "") for typ, a in p.links if typ == "link" and (a.get("rel") or "").lower() == "canonical"]
    alternates = [(a.get("hreflang"), a.get("href")) for typ, a in p.links if typ == "link" and (a.get("rel") or "").lower() == "alternate" and a.get("hreflang")]

    if not title:
        errors.append(f"NO_TITLE | {file.relative_to(ROOT)}")
    else:
        titles[title].append(str(file.relative_to(ROOT)))
        if len(title) > 65:
            warnings.append(f"TITLE_LONG({len(title)}) | {file.relative_to(ROOT)} | {title}")

    if not description:
        errors.append(f"NO_META_DESCRIPTION | {file.relative_to(ROOT)}")
    else:
        descriptions[description].append(str(file.relative_to(ROOT)))
        if len(description) > 170:
            warnings.append(f"DESCRIPTION_LONG({len(description)}) | {file.relative_to(ROOT)}")

    if p.h1 != 1:
        errors.append(f"H1_COUNT={p.h1} | {file.relative_to(ROOT)}")
    if len(canonicals) != 1:
        errors.append(f"CANONICAL_COUNT={len(canonicals)} | {file.relative_to(ROOT)}")
    elif canonicals[0] != url:
        errors.append(f"CANONICAL_MISMATCH | {file.relative_to(ROOT)} | {canonicals[0]} != {url}")

    hreflangs = {x[0] for x in alternates}
    if not {"en-AE", "ar-AE", "x-default"}.issubset(hreflangs):
        errors.append(f"HREFLANG_INCOMPLETE | {file.relative_to(ROOT)} | {sorted(hreflangs)}")

    if "/ar/" in url:
        if p.lang != "ar" or p.dir != "rtl":
            errors.append(f"AR_LANG_DIR | {file.relative_to(ROOT)} | lang={p.lang} dir={p.dir}")
    elif p.lang != "en":
        errors.append(f"EN_LANG | {file.relative_to(ROOT)} | lang={p.lang}")

    duplicate_ids = sorted(k for k, count in Counter(p.ids).items() if count > 1)
    if duplicate_ids:
        errors.append(f"DUPLICATE_IDS | {file.relative_to(ROOT)} | {duplicate_ids}")

    for block in p.jsonld:
        if block:
            try:
                json.loads(block)
            except Exception as exc:
                errors.append(f"INVALID_JSONLD | {file.relative_to(ROOT)} | {exc}")

    for required_og in ("og:title", "og:description", "og:url", "og:image"):
        if not meta_prop.get(required_og):
            warnings.append(f"MISSING_{required_og.upper()} | {file.relative_to(ROOT)}")
    if not meta_name.get("robots"):
        warnings.append(f"NO_META_ROBOTS | {file.relative_to(ROOT)}")

    for image in p.images:
        src = image.get("src", "")
        if image.get("alt") is None:
            errors.append(f"IMG_NO_ALT | {file.relative_to(ROOT)} | {src}")
        if not image.get("width") or not image.get("height"):
            warnings.append(f"IMG_NO_DIMENSIONS | {file.relative_to(ROOT)} | {src}")
        if src and not src.startswith(("http://", "https://", "data:")):
            clean = src.split("?", 1)[0]
            target = ROOT / clean.lstrip("/") if clean.startswith("/") else file.parent / clean
            if not target.exists():
                errors.append(f"IMG_MISSING_FILE | {file.relative_to(ROOT)} | {src}")

    for button in p.buttons:
        label = "".join(button["text"]).strip() or button["attrs"].get("aria-label", "") or button["attrs"].get("title", "")
        if not label:
            errors.append(f"UNLABELED_BUTTON | {file.relative_to(ROOT)} | {button['attrs']}")

    for asset in p.scripts + p.styles:
        if asset and not asset.startswith(("http://", "https://", "//", "data:")):
            clean = asset.split("?", 1)[0]
            target = ROOT / clean.lstrip("/") if clean.startswith("/") else file.parent / clean
            if not target.exists():
                errors.append(f"MISSING_LOCAL_ASSET | {file.relative_to(ROOT)} | {asset}")

    if "Your email app will open" in raw or "Your request will open in your email app" in raw:
        errors.append(f"STALE_BOOKING_COPY | {file.relative_to(ROOT)}")

for title, files in titles.items():
    if len(files) > 1:
        warnings.append(f"DUPLICATE_TITLE | {title} | {files}")
for description, files in descriptions.items():
    if len(files) > 1:
        warnings.append(f"DUPLICATE_DESCRIPTION | {files}")

# Every sitemap URL should have an English/Arabic counterpart.
urlset = set(urls)
for url in urls:
    path = urlparse(url).path
    if path.startswith("/ar/"):
        counterpart = BASE if path == "/ar/" else BASE.rstrip("/") + path[3:]
    else:
        counterpart = BASE + "ar/" if path == "/" else BASE.rstrip("/") + "/ar" + path
    if counterpart not in urlset:
        errors.append(f"MISSING_LANGUAGE_COUNTERPART | {url} -> {counterpart}")

# Repository-side internal link and same-page fragment validation.
internal_live_targets = set(urls)
for page_url, (file, p, raw) in parsed_pages.items():
    ids = set(p.ids)
    for typ, anchor in p.links:
        if typ != "a":
            continue
        href = anchor.get("href", "")
        if not href:
            warnings.append(f"EMPTY_HREF | {file.relative_to(ROOT)} | {anchor}")
            continue
        if href.startswith(("mailto:", "tel:", "javascript:", "data:")):
            continue
        if href.startswith("#"):
            if len(href) > 1 and href[1:] not in ids:
                errors.append(f"BROKEN_FRAGMENT | {file.relative_to(ROOT)} | {href}")
            continue

        absolute = urljoin(page_url, href)
        q = urlparse(absolute)
        if q.netloc and q.netloc != "silwadi.ae":
            continue
        target = internal_local_target(file, href, absolute)
        if not target.exists():
            errors.append(f"BROKEN_INTERNAL_LINK | {file.relative_to(ROOT)} | {href} -> {target.relative_to(ROOT)}")
        if q.fragment and q.path == urlparse(page_url).path and q.fragment not in ids:
            errors.append(f"BROKEN_FRAGMENT | {file.relative_to(ROOT)} | {href}")
        internal_live_targets.add(q._replace(fragment="", query="").geturl())

# Booking implementation checks; intentionally no POST request.
for js_name in ("app.js", "booking-modal.js"):
    js = (ROOT / js_name).read_text(encoding="utf-8", errors="replace")
    if BOOKING_ENDPOINT not in js:
        errors.append(f"BOOKING_ENDPOINT_MISSING | {js_name}")

required_fields = [
    'name="name"', 'name="phone"', 'name="email"', 'name="treatment"',
    'name="time"', 'name="clinic"', 'name="privacy-consent"'
]
for file in (ROOT / "contact.html", ROOT / "ar/contact.html"):
    raw = file.read_text(encoding="utf-8", errors="replace")
    if "data-consultation-form" not in raw:
        errors.append(f"BOOKING_FORM_HOOK_MISSING | {file.relative_to(ROOT)}")
    for token in required_fields:
        if token not in raw:
            errors.append(f"BOOKING_FIELD_MISSING | {file.relative_to(ROOT)} | {token}")

# Known objective Arabic localization leaks. Proper names/brands are intentionally not blanket-rejected.
known_arabic_leaks = [
    "Prosthodontic restorations",
    "Cosmetic dentistry and teeth whitening",
    "Treatment room at Silwadi Dental Centre",
    "Silwadi Dental Centre at Al Raha Mall",
    "Bani Yas Tower (Corniche)",
    "Sun–Wed:",
    "Thu & Sat:",
    "Sat–Thu:",
    "Dr. Mohamed Munir Dental Centre - Al Raha Mall",
    "Level 1, Al Raha Mall",
    "Channel St, Al Rahah",
    "Excellence for Every Ability, A Smile for Every Soul.",
]
for url, (file, p, raw) in parsed_pages.items():
    if "/ar/" not in url:
        continue
    for phrase in known_arabic_leaks:
        if phrase in raw:
            errors.append(f"ARABIC_ENGLISH_LEAK | {file.relative_to(ROOT)} | {phrase}")

    visible = " ".join(p.visible)
    scrub = visible
    allowed = [
        "Google", "WhatsApp", "Instagram", "Invisalign", "F14", "F15", "DOH", "BDS", "MSc",
        "MClinDent", "DDS", "DMD", "PhD", "FRACDS", "MOrth", "Ahmed H", "Emily Campbell Scully",
        "Victoriya Davydova", "Sanaa Freihat", "Sahar Alsalman", "@dr.munirsilwadidental"
    ]
    for phrase in allowed:
        scrub = scrub.replace(phrase, " ")
    suspects = []
    for match in re.finditer(r"(?<![@\w])[A-Za-z][A-Za-z0-9.&+’\-]*(?:\s+[A-Za-z][A-Za-z0-9.&+’\-]*){1,11}", scrub):
        phrase = " ".join(match.group(0).split()).strip()
        if len(phrase) >= 5 and phrase not in suspects:
            suspects.append(phrase)
    for phrase in suspects[:80]:
        warnings.append(f"ARABIC_LATIN_VISIBLE_SUSPECT | {file.relative_to(ROOT)} | {phrase}")

robots = (ROOT / "robots.txt").read_text(encoding="utf-8", errors="replace") if (ROOT / "robots.txt").exists() else ""
if not robots:
    errors.append("ROBOTS_MISSING")
if "Sitemap:" not in robots:
    warnings.append("ROBOTS_NO_SITEMAP")
if re.search(r"^\s*Disallow:\s*/\s*$", robots, re.M):
    errors.append("ROBOTS_BLOCKS_ALL")

# Live GET every sitemap/internal target; no form submission.
sslctx = ssl.create_default_context()
live_results = []
for url in sorted(internal_live_targets):
    started = time.time()
    try:
        req = Request(url, headers={"User-Agent": "Silwadi-QA-Audit/2026-09-16"})
        with urlopen(req, timeout=20, context=sslctx) as response:
            status = getattr(response, "status", 200)
            ctype = response.headers.get("Content-Type", "")
            response.read(16384)
        elapsed = int((time.time() - started) * 1000)
        live_results.append((status, elapsed, url, ctype))
        if status != 200:
            errors.append(f"LIVE_HTTP_{status} | {url}")
    except HTTPError as exc:
        live_results.append((exc.code, -1, url, ""))
        errors.append(f"LIVE_HTTP_{exc.code} | {url}")
    except Exception as exc:
        live_results.append(("ERR", -1, url, ""))
        errors.append(f"LIVE_FAIL | {url} | {type(exc).__name__}: {exc}")

try:
    req = Request(BOOKING_ENDPOINT, headers={"User-Agent": "Silwadi-QA-Audit/2026-09-16"})
    try:
        with urlopen(req, timeout=15, context=sslctx) as response:
            booking_get_code = getattr(response, "status", 200)
    except HTTPError as exc:
        booking_get_code = exc.code
    info.append(f"BOOKING_ENDPOINT_GET_HTTP={booking_get_code} (reachability only; NO appointment submitted)")
    if int(booking_get_code) >= 500:
        errors.append(f"BOOKING_ENDPOINT_SERVER_ERROR | HTTP {booking_get_code}")
except Exception as exc:
    errors.append(f"BOOKING_ENDPOINT_UNREACHABLE | {type(exc).__name__}: {exc}")

report = [
    "SILWADI FULL-SITE STATIC/LIVE AUDIT",
    *info,
    "",
    f"ERRORS={len(errors)}",
    f"WARNINGS={len(warnings)}",
    "",
    "=== ERRORS ===",
    *(errors or ["None"]),
    "",
    "=== WARNINGS ===",
    *(warnings or ["None"]),
    "",
    "=== LIVE URLS ===",
]
report.extend(f"{status} | {elapsed}ms | {url} | {ctype}" for status, elapsed, url, ctype in live_results)
(OUT / "static-live-report.txt").write_text("\n".join(report), encoding="utf-8")
(OUT / "static-summary.json").write_text(
    json.dumps({"sitemap_urls": len(urls), "errors": errors, "warnings": warnings, "info": info}, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print("\n".join(report))
