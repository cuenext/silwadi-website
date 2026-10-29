"""Build a static-only upload directory for the UAE web server."""

import argparse
import shutil
from pathlib import Path


PAGE_DIRS = {"ar", "doctors", "locations", "treatments"}
PAGE_EXTENSIONS = {".html", ".css", ".js"}
ASSET_EXTENSIONS = {
    ".webp", ".png", ".jpg", ".jpeg", ".gif", ".avif",
    ".svg", ".woff", ".woff2", ".mp4",
}
ROOT_EXTENSIONS = PAGE_EXTENSIONS | {".svg"}
ROOT_NAMES = {"robots.txt", "sitemap.xml"}
PUBLIC_AI_FILES = {
    "ai/index.html", "ai/privacy.html", "ai/silwadi-ai-page.css",
    "ai/site-shell.css", "ai/site-shell.js", "ai/assets/assistant.svg",
    "ai/assets/faq.js", "ai/assets/clinic-text.js", "ai/assets/booking.js",
    "ai/assets/silwadi-ai-widget.js", "ai/assets/silwadi-ai-widget.css",
}


def public_file(relative: Path) -> bool:
    parts = relative.parts
    if parts[0] == "ai":
        return relative.as_posix() in PUBLIC_AI_FILES
    if len(parts) == 1:
        return relative.name in ROOT_NAMES or relative.suffix.lower() in ROOT_EXTENSIONS
    if parts[0] in PAGE_DIRS:
        return relative.suffix.lower() in PAGE_EXTENSIONS
    if parts[0] == "assets":
        return (
            relative.suffix.lower() in ASSET_EXTENSIONS
            and not any("b64" in part.lower() for part in parts[1:])
            and not (parts[1] == "video" and "review" in relative.name.lower())
        )
    return False


def build_public_bundle(source: Path, output: Path) -> int:
    source = source.resolve()
    output = output.resolve()
    if source == output or source in output.parents:
        raise ValueError("Output must be outside the source tree")
    if output.exists() and any(output.iterdir()):
        raise ValueError("Output directory must be empty")

    count = 0
    for path in source.rglob("*"):
        if not path.is_file() or path.is_symlink():
            continue
        relative = path.relative_to(source)
        if not public_file(relative):
            continue
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        count += 1
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(f"Copied {build_public_bundle(Path.cwd(), args.output)} public files to {args.output}")
