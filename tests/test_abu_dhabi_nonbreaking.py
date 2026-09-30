import re
from html.parser import HTMLParser
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAIN = re.compile(r"Abu[ \t\r\n]+Dhabi")

class VisibleTextParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hidden = 0
        self.parts = []
    def handle_starttag(self, tag, attrs):
        if tag in {'head', 'script', 'style', 'noscript', 'template'}:
            self.hidden += 1
    def handle_endtag(self, tag):
        if tag in {'head', 'script', 'style', 'noscript', 'template'}:
            self.hidden = max(0, self.hidden - 1)
    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)

def visible_body_text(html: str) -> str:
    parser = VisibleTextParser()
    parser.feed(html)
    return ''.join(parser.parts)


class AbuDhabiNonbreakingContract(unittest.TestCase):
    def test_visible_abu_dhabi_never_breaks_across_lines(self):
        offenders = []
        for path in ROOT.rglob("*.html"):
            text = path.read_text(encoding="utf-8")
            if PLAIN.search(visible_body_text(text)):
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual([], offenders, "Visible 'Abu Dhabi' must use a non-breaking space in: " + ", ".join(offenders))

    def test_head_metadata_keeps_normal_space(self):
        offenders = []
        for path in ROOT.rglob("*.html"):
            text = path.read_text(encoding="utf-8")
            head = text.split("</head>", 1)[0]
            if "Abu&nbsp;Dhabi" in head or "Abu\u00a0Dhabi" in head:
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual([], offenders, "Do not alter Abu Dhabi inside head metadata/schema: " + ", ".join(offenders))


if __name__ == "__main__":
    unittest.main()
