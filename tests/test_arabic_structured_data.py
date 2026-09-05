from pathlib import Path
from urllib.parse import urlparse
import json
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SEO = json.loads((ROOT / "data" / "arabic-seo.json").read_text(encoding="utf-8"))
ROUTES = set(SEO)


def route_from_path(path: str):
    if path in ("/", "/index.html"):
        return "index.html"
    candidate = path.lstrip("/")
    return candidate if candidate in ROUTES else None


def walk_strings(value):
    if isinstance(value, dict):
        for child in value.values():
            yield from walk_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_strings(child)
    elif isinstance(value, str):
        yield value


class ArabicStructuredDataContract(unittest.TestCase):
    def test_page_specific_internal_schema_urls_use_arabic_routes(self):
        for route in SEO:
            source = (ROOT / "ar" / route).read_text(encoding="utf-8")
            blocks = re.findall(
                r'<script[^>]*data-seo-schema[^>]*>(.*?)</script>',
                source,
                re.I | re.S,
            )
            for block in blocks:
                data = json.loads(block)
                for value in walk_strings(data):
                    if not value.startswith("https://silwadi.ae/"):
                        continue
                    parsed = urlparse(value)
                    paired = route_from_path(parsed.path)
                    if not paired or paired == "index.html":
                        continue
                    self.assertTrue(
                        parsed.path.startswith("/ar/"),
                        f"{route}: structured data still points to English page URL {value}",
                    )


if __name__ == "__main__":
    unittest.main()
