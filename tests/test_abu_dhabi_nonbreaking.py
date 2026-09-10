import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_BLOCKS = re.compile(r"(?is)<(?:script|style|noscript|template)\b.*?</(?:script|style|noscript|template)\s*>")
TAGS = re.compile(r"(?is)<[^>]+>")
PLAIN = re.compile(r"Abu[ \t\r\n]+Dhabi")


def visible_body_text(html: str) -> str:
    match = re.search(r"(?is)<body\b[^>]*>(.*)</body\s*>", html)
    body = match.group(1) if match else html
    body = SKIP_BLOCKS.sub("", body)
    return TAGS.sub("", body)


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
