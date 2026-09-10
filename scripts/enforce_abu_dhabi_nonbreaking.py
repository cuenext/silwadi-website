from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PLAIN = re.compile(r"Abu[ \t\r\n]+Dhabi")
PROTECTED = re.compile(
    r"(?is)(<!--.*?-->|<(?:script|style|noscript|template)\b.*?</(?:script|style|noscript|template)\s*>|<[^>]+>)"
)
HEAD_END = re.compile(r"(?is)</head\s*>")


def update_visible_body(html: str):
    head = HEAD_END.search(html)
    split_at = head.end() if head else 0
    prefix, body = html[:split_at], html[split_at:]
    parts = PROTECTED.split(body)
    replacements = 0

    for index, part in enumerate(parts):
        if not part or part.startswith("<"):
            continue
        parts[index], count = PLAIN.subn("Abu&nbsp;Dhabi", part)
        replacements += count

    return prefix + "".join(parts), replacements


def main():
    changed = []
    total = 0
    for path in ROOT.rglob("*.html"):
        original = path.read_text(encoding="utf-8")
        updated, count = update_visible_body(original)
        if count:
            path.write_text(updated, encoding="utf-8")
            changed.append(str(path.relative_to(ROOT)))
            total += count

    print(f"Updated {total} visible 'Abu Dhabi' occurrence(s) across {len(changed)} file(s).")
    for rel in changed:
        print(rel)


if __name__ == "__main__":
    main()
