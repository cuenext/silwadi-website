#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import urlparse
import csv
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://silwadi.ae'
SITE_NAME = 'Silwadi Dental Center'
ROBOTS_POLICY = 'index,follow,max-image-preview:large'
SITEMAP_NS = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
ATTR_RE = re.compile(r'([:\w-]+)\s*=\s*["\']([^"\']*)["\']', re.I)


def read(rel):
    return (ROOT / rel).read_text(encoding='utf-8')


def attrs(tag):
    return {key.lower(): value for key, value in ATTR_RE.findall(tag)}


def tags(html, name):
    return re.findall(rf'<{name}\b[^>]*>', html, re.I)


def meta_values(html, attr_name, attr_value):
    values = []
    for tag in tags(html, 'meta'):
        data = attrs(tag)
        if data.get(attr_name.lower(), '').lower() == attr_value.lower():
            values.append(data.get('content', ''))
    return values


def link_values(html, rel_value):
    values = []
    for tag in tags(html, 'link'):
        data = attrs(tag)
        if data.get('rel', '').lower() == rel_value.lower():
            values.append(data)
    return values


def jsonld_nodes(html, errors, rel):
    nodes = []
    blocks = re.findall(
        r'<script\s+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html,
        re.I | re.S,
    )
    for index, block in enumerate(blocks, start=1):
        try:
            parsed = json.loads(block)
        except json.JSONDecodeError as exc:
            errors.append(f'{rel}: JSON-LD block {index} is invalid: {exc}')
            continue
        if isinstance(parsed, dict) and isinstance(parsed.get('@graph'), list):
            nodes.extend(parsed['@graph'])
        else:
            nodes.append(parsed)
    return nodes


def contains_key(value, target):
    if isinstance(value, dict):
        if target in value:
            return True
        return any(contains_key(v, target) for v in value.values())
    if isinstance(value, list):
        return any(contains_key(v, target) for v in value)
    return False


def file_for_url(url):
    path = urlparse(url).path
    return 'index.html' if path == '/' else path.lstrip('/')


def audit():
    errors = []
    sitemap_path = ROOT / 'sitemap.xml'
    if not sitemap_path.is_file():
        return ['sitemap.xml: missing'], 0

    try:
        sitemap_root = ET.fromstring(sitemap_path.read_text(encoding='utf-8'))
    except ET.ParseError as exc:
        return [f'sitemap.xml: invalid XML: {exc}'], 0

    url_nodes = sitemap_root.findall('sm:url', SITEMAP_NS)
    locs = []
    lastmods = []
    for node in url_nodes:
        loc = node.find('sm:loc', SITEMAP_NS)
        lastmod = node.find('sm:lastmod', SITEMAP_NS)
        if loc is None or not loc.text:
            errors.append('sitemap.xml: URL entry missing loc')
            continue
        locs.append(loc.text.strip())
        if lastmod is None or not lastmod.text:
            errors.append(f'sitemap.xml: {loc.text.strip()} missing lastmod')
        else:
            value = lastmod.text.strip()
            lastmods.append(value)
            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
                errors.append(f'sitemap.xml: invalid lastmod {value} for {loc.text.strip()}')

    if len(locs) != 27:
        errors.append(f'sitemap.xml: expected 27 canonical URLs, found {len(locs)}')
    if len(locs) != len(set(locs)):
        errors.append('sitemap.xml: duplicate canonical URLs found')
    if any(not url.startswith(f'{ORIGIN}/') for url in locs):
        errors.append('sitemap.xml: every URL must use https://silwadi.ae/')

    titles = []
    descriptions = []
    canonical_set = set(locs)

    for url in locs:
        rel = file_for_url(url)
        path = ROOT / rel
        if not path.is_file():
            errors.append(f'{rel}: sitemap target file missing')
            continue
        html = path.read_text(encoding='utf-8')

        title_matches = re.findall(r'<title>(.*?)</title>', html, re.I | re.S)
        if len(title_matches) != 1:
            errors.append(f'{rel}: expected exactly one title, found {len(title_matches)}')
        else:
            titles.append(re.sub(r'\s+', ' ', title_matches[0]).strip())

        descs = meta_values(html, 'name', 'description')
        if len(descs) != 1 or not descs[0].strip():
            errors.append(f'{rel}: expected exactly one non-empty meta description')
        else:
            descriptions.append(descs[0].strip())

        canonicals = link_values(html, 'canonical')
        canonical_hrefs = [item.get('href', '') for item in canonicals]
        if canonical_hrefs != [url]:
            errors.append(f'{rel}: canonical mismatch {canonical_hrefs!r} != {[url]!r}')

        og_urls = meta_values(html, 'property', 'og:url')
        if og_urls != [url]:
            errors.append(f'{rel}: og:url mismatch {og_urls!r} != {[url]!r}')

        if meta_values(html, 'property', 'og:site_name') != [SITE_NAME]:
            errors.append(f'{rel}: missing or duplicate og:site_name')

        robots = meta_values(html, 'name', 'robots')
        if robots != [ROBOTS_POLICY]:
            errors.append(f'{rel}: robots policy must be {ROBOTS_POLICY}')
        if any('noindex' in value.lower() for value in robots):
            errors.append(f'{rel}: noindex is not allowed on canonical launch pages')

        icons = link_values(html, 'icon')
        expected_icon = '../favicon.svg' if '/' in rel else 'favicon.svg'
        matching_icons = [item for item in icons if item.get('href') == expected_icon and item.get('type') == 'image/svg+xml']
        if len(matching_icons) != 1:
            errors.append(f'{rel}: expected one favicon link to {expected_icon}')
        else:
            resolved = (path.parent / expected_icon).resolve()
            if not resolved.is_file():
                errors.append(f'{rel}: favicon target does not resolve')

        if 'https://silwadidentalcentres.ae' in html:
            errors.append(f'{rel}: legacy website origin is still linked as an absolute HTTP URL')

        for node in jsonld_nodes(html, errors, rel):
            if contains_key(node, 'aggregateRating') or contains_key(node, 'review'):
                errors.append(f'{rel}: self-authored review/rating schema is not permitted')

    if len(titles) != len(set(titles)):
        errors.append('metadata: duplicate page titles found')
    if len(descriptions) != len(set(descriptions)):
        errors.append('metadata: duplicate meta descriptions found')

    robots_path = ROOT / 'robots.txt'
    if not robots_path.is_file():
        errors.append('robots.txt: missing')
    else:
        robots_text = robots_path.read_text(encoding='utf-8')
        if 'User-agent: *' not in robots_text or 'Allow: /' not in robots_text:
            errors.append('robots.txt: crawler allow rules missing')
        if f'Sitemap: {ORIGIN}/sitemap.xml' not in robots_text:
            errors.append('robots.txt: canonical sitemap declaration missing')

    favicon = ROOT / 'favicon.svg'
    if not favicon.is_file():
        errors.append('favicon.svg: missing')
    else:
        try:
            icon_root = ET.fromstring(favicon.read_text(encoding='utf-8'))
            if not icon_root.tag.endswith('svg'):
                errors.append('favicon.svg: root element is not svg')
            if icon_root.attrib.get('viewBox') != '0 0 64 64':
                errors.append('favicon.svg: expected square 0 0 64 64 viewBox')
        except ET.ParseError as exc:
            errors.append(f'favicon.svg: invalid XML: {exc}')

    redirect_path = ROOT / 'docs/launch/legacy-redirect-map.csv'
    if not redirect_path.is_file():
        errors.append('legacy redirect map: missing')
    else:
        with redirect_path.open(encoding='utf-8', newline='') as handle:
            rows = list(csv.DictReader(handle))
        if not rows:
            errors.append('legacy redirect map: empty')
        for row in rows:
            source = row.get('source_url', '')
            target = row.get('target_url', '')
            status = row.get('status', '')
            if not source.startswith('https://silwadidentalcentres.ae/'):
                errors.append(f'legacy redirect map: invalid source {source!r}')
            if status != '301':
                errors.append(f'legacy redirect map: {source} must use 301')
            if target not in canonical_set:
                errors.append(f'legacy redirect map: target is not canonical: {target!r}')

    checklist = ROOT / 'docs/launch/SEO-LAUNCH-CHECKLIST.md'
    if not checklist.is_file():
        errors.append('SEO launch checklist: missing')

    return errors, len(locs)


def main():
    errors, page_count = audit()
    print(f'SEO launch audit: {page_count} pages, {len(errors)} errors')
    for error in errors:
        print(f'- {error}')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
