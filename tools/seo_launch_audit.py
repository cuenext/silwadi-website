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
SEO = json.loads((ROOT / 'data' / 'arabic-seo.json').read_text(encoding='utf-8'))
ROUTES = list(SEO)


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


def english_url(route):
    return f'{ORIGIN}/' if route == 'index.html' else f'{ORIGIN}/{route}'


def arabic_url(route):
    return f'{ORIGIN}/ar/' if route == 'index.html' else f'{ORIGIN}/ar/{route}'


def expected_urls():
    return [english_url(route) for route in ROUTES] + [arabic_url(route) for route in ROUTES]


def url_context(url):
    path = urlparse(url).path
    is_arabic = path == '/ar/' or path.startswith('/ar/')
    if path in ('/', '/index.html'):
        route = 'index.html'
    elif path in ('/ar/', '/ar/index.html'):
        route = 'index.html'
    elif is_arabic:
        route = path[len('/ar/'):]
    else:
        route = path.lstrip('/')
    return route, is_arabic


def file_for_url(url):
    route, is_arabic = url_context(url)
    if route == 'index.html':
        return 'ar/index.html' if is_arabic else 'index.html'
    return f'ar/{route}' if is_arabic else route


def resolve_local_asset(page_rel, href):
    if href.startswith('/'):
        return ROOT / href.lstrip('/')
    return (ROOT / page_rel).parent / href


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
    for node in url_nodes:
        loc = node.find('sm:loc', SITEMAP_NS)
        lastmod = node.find('sm:lastmod', SITEMAP_NS)
        if loc is None or not loc.text:
            errors.append('sitemap.xml: URL entry missing loc')
            continue
        current = loc.text.strip()
        locs.append(current)
        if lastmod is None or not lastmod.text:
            errors.append(f'sitemap.xml: {current} missing lastmod')
        elif not re.fullmatch(r'\d{4}-\d{2}-\d{2}', lastmod.text.strip()):
            errors.append(f'sitemap.xml: invalid lastmod {lastmod.text.strip()} for {current}')

    expected = expected_urls()
    if len(locs) != len(expected):
        errors.append(f'sitemap.xml: expected {len(expected)} bilingual URLs, found {len(locs)}')
    if len(locs) != len(set(locs)):
        errors.append('sitemap.xml: duplicate canonical URLs found')
    missing = sorted(set(expected) - set(locs))
    extra = sorted(set(locs) - set(expected))
    for url in missing:
        errors.append(f'sitemap.xml: missing expected URL {url}')
    for url in extra:
        errors.append(f'sitemap.xml: unexpected URL {url}')
    if any(not url.startswith(f'{ORIGIN}/') for url in locs):
        errors.append('sitemap.xml: every URL must use https://silwadi.ae/')

    titles = {'en': [], 'ar': []}
    descriptions = {'en': [], 'ar': []}
    english_canonicals = {english_url(route) for route in ROUTES}

    for url in locs:
        route, is_arabic = url_context(url)
        rel = file_for_url(url)
        path = ROOT / rel
        language = 'ar' if is_arabic else 'en'
        if route not in SEO:
            errors.append(f'{rel}: route is not in the bilingual route manifest')
            continue
        if not path.is_file():
            errors.append(f'{rel}: sitemap target file missing')
            continue
        html = path.read_text(encoding='utf-8')

        title_matches = re.findall(r'<title>(.*?)</title>', html, re.I | re.S)
        if len(title_matches) != 1:
            errors.append(f'{rel}: expected exactly one title, found {len(title_matches)}')
        else:
            titles[language].append(re.sub(r'\s+', ' ', title_matches[0]).strip())

        descs = meta_values(html, 'name', 'description')
        if len(descs) != 1 or not descs[0].strip():
            errors.append(f'{rel}: expected exactly one non-empty meta description')
        else:
            descriptions[language].append(descs[0].strip())

        canonicals = link_values(html, 'canonical')
        canonical_hrefs = [item.get('href', '') for item in canonicals]
        if canonical_hrefs != [url]:
            errors.append(f'{rel}: canonical mismatch {canonical_hrefs!r} != {[url]!r}')

        og_urls = meta_values(html, 'property', 'og:url')
        if og_urls != [url]:
            errors.append(f'{rel}: og:url mismatch {og_urls!r} != {[url]!r}')

        expected_locale = 'ar_AE' if is_arabic else 'en_AE'
        expected_alt_locale = 'en_AE' if is_arabic else 'ar_AE'
        expected_content_language = 'ar' if is_arabic else 'en'
        if meta_values(html, 'property', 'og:locale') != [expected_locale]:
            errors.append(f'{rel}: expected one {expected_locale} og:locale')
        if meta_values(html, 'property', 'og:locale:alternate') != [expected_alt_locale]:
            errors.append(f'{rel}: expected one {expected_alt_locale} og:locale:alternate')
        if meta_values(html, 'name', 'content-language') != [expected_content_language]:
            errors.append(f'{rel}: expected one {expected_content_language} content-language meta')

        html_tag = re.search(r'<html\b[^>]*>', html, re.I)
        html_attrs = attrs(html_tag.group(0)) if html_tag else {}
        if html_attrs.get('lang') != expected_content_language:
            errors.append(f'{rel}: html lang must be {expected_content_language}')
        if is_arabic and html_attrs.get('dir') != 'rtl':
            errors.append(f'{rel}: Arabic page must use dir="rtl"')

        alternates = {
            item.get('hreflang', '').lower(): item.get('href', '')
            for item in link_values(html, 'alternate')
            if item.get('hreflang')
        }
        expected_alternates = {
            'en-ae': english_url(route),
            'ar-ae': arabic_url(route),
            'x-default': english_url(route),
        }
        for hreflang, expected_href in expected_alternates.items():
            if alternates.get(hreflang) != expected_href:
                errors.append(f'{rel}: {hreflang} alternate mismatch {alternates.get(hreflang)!r} != {expected_href!r}')

        if meta_values(html, 'property', 'og:site_name') != [SITE_NAME]:
            errors.append(f'{rel}: missing or duplicate og:site_name')

        robots = meta_values(html, 'name', 'robots')
        if robots != [ROBOTS_POLICY]:
            errors.append(f'{rel}: robots policy must be {ROBOTS_POLICY}')
        if any('noindex' in value.lower() for value in robots):
            errors.append(f'{rel}: noindex is not allowed on canonical pages')

        icons = [item for item in link_values(html, 'icon') if item.get('type') == 'image/svg+xml']
        if len(icons) != 1:
            errors.append(f'{rel}: expected one SVG favicon link')
        else:
            href = icons[0].get('href', '')
            if not href or not resolve_local_asset(rel, href).resolve().is_file():
                errors.append(f'{rel}: favicon target does not resolve: {href!r}')

        if 'https://silwadidentalcentres.ae' in html:
            errors.append(f'{rel}: legacy website origin is still linked as an absolute HTTP URL')

        for node in jsonld_nodes(html, errors, rel):
            if contains_key(node, 'aggregateRating') or contains_key(node, 'review'):
                errors.append(f'{rel}: self-authored review/rating schema is not permitted')

        if is_arabic:
            if 'data-arabic-page-schema' not in html or '"inLanguage":"ar-AE"' not in html:
                errors.append(f'{rel}: Arabic WebPage schema with inLanguage ar-AE is missing')

    for language in ('en', 'ar'):
        if len(titles[language]) != len(set(titles[language])):
            errors.append(f'metadata: duplicate {language} page titles found')
        if len(descriptions[language]) != len(set(descriptions[language])):
            errors.append(f'metadata: duplicate {language} meta descriptions found')

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
            viewbox = icon_root.attrib.get('viewBox', '').split()
            if len(viewbox) != 4:
                errors.append('favicon.svg: valid four-number viewBox is required')
            else:
                try:
                    width = float(viewbox[2])
                    height = float(viewbox[3])
                    if width <= 0 or height <= 0 or abs(width - height) > 1e-9:
                        errors.append('favicon.svg: viewBox must be square')
                except ValueError:
                    errors.append('favicon.svg: viewBox must contain numeric dimensions')
            width_attr = icon_root.attrib.get('width')
            height_attr = icon_root.attrib.get('height')
            if width_attr and height_attr and width_attr != height_attr:
                errors.append('favicon.svg: rendered width and height must match')
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
            if target not in english_canonicals:
                errors.append(f'legacy redirect map: target is not an English canonical: {target!r}')

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
