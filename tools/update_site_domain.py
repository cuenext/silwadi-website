#!/usr/bin/env python3
"""Switch the deployed site origin used by canonical SEO files.

This changes website-origin URLs only. Contact email addresses are untouched.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data" / "site-config.json"


def normalize_origin(value: str) -> str:
    value = value.strip().rstrip("/")
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc or parsed.path not in ("", "/") or parsed.params or parsed.query or parsed.fragment:
        raise ValueError("origin must be an HTTPS site origin such as https://silwadi.ae")
    return f"https://{parsed.netloc}"


def deployable_files() -> list[Path]:
    files = sorted(ROOT.rglob("*.html"))
    for name in ("sitemap.xml", "robots.txt"):
        path = ROOT / name
        if path.exists():
            files.append(path)
    return files


def switch_origin(new_origin: str) -> tuple[str, int]:
    new_origin = normalize_origin(new_origin)
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    old_origin = normalize_origin(config["origin"])

    changed = 0
    if old_origin != new_origin:
        for path in deployable_files():
            text = path.read_text(encoding="utf-8")
            updated = text.replace(old_origin, new_origin)
            if updated != text:
                path.write_text(updated, encoding="utf-8")
                changed += 1

    config["origin"] = new_origin
    config["dentist_id"] = f"{new_origin}/#dentist"
    config["website_id"] = f"{new_origin}/#website"
    config["default_social_image"] = f"{new_origin}/assets/silwadi-logo-original.jpeg"
    CONFIG_PATH.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return old_origin, changed


def main() -> int:
    parser = argparse.ArgumentParser(description="Switch Silwadi's canonical website origin across static SEO files.")
    parser.add_argument("origin", help="New HTTPS origin, e.g. https://silwadi.ae")
    args = parser.parse_args()
    try:
        old_origin, changed = switch_origin(args.origin)
    except (ValueError, KeyError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    new_origin = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))["origin"]
    print(f"Site origin: {old_origin} -> {new_origin} ({changed} deployable files updated)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
