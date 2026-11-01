"""Build a static-only upload directory for the UAE web server."""

import argparse
import shutil
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit


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


class AssistantMarkup(HTMLParser):
    """Inspect executable tags and real navigation, ignoring HTML comments."""

    def __init__(self):
        super().__init__()
        self.scripts = []
        self.navigation = []
        self.nav_stack = []
        self.footer_links = []
        self.in_footer = False

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == 'script' and data.get('type', '').lower() in ('', 'module', 'text/javascript', 'application/javascript') and data.get('src'):
            self.scripts.append(data)
        if tag == 'nav':
            relevant = bool(set(data.get('class', '').split()) & {'site-nav', 'mobile-nav__panel', 'global-nav', 'nav'})
            group = [] if relevant else None
            self.nav_stack.append(group)
            if group is not None:
                self.navigation.append(group)
        if tag == 'footer':
            self.in_footer = True
        if tag == 'a' and data.get('href'):
            for group in self.nav_stack:
                if group is not None:
                    group.append(data['href'])
            if self.in_footer:
                self.footer_links.append(data['href'])

    def handle_endtag(self, tag):
        if tag == 'nav' and self.nav_stack:
            self.nav_stack.pop()
        if tag == 'footer':
            self.in_footer = False


def validate_assistant_bundle(root: Path) -> int:
    """Fail closed on the actual upload folder, not merely the source checkout."""
    root = root.resolve()
    for file in root.rglob('*'):
        if file.is_symlink() or (file.is_file() and not public_file(file.relative_to(root))):
            raise ValueError(f'Non-public file in upload folder: {file.relative_to(root)}')
    for name in sorted(PUBLIC_AI_FILES):
        file = root / name
        if not file.is_file() or file.is_symlink() or file.stat().st_size == 0:
            raise ValueError(f'Missing or empty public assistant file: {name}')

    def script_path(data, base):
        parsed = urlsplit(urljoin(base, data['src']))
        return parsed.path if parsed.hostname in ('silwadi.ae', 'www.silwadi.ae') else ''

    def faq_target(value, arabic):
        parsed = urlsplit(urljoin('https://silwadi.ae/', value))
        return parsed.hostname in ('silwadi.ae', 'www.silwadi.ae') and parsed.path == '/ai/' and (not arabic or parsed.query == 'lang=ar')

    count = 0
    required_scripts = {f'/ai/assets/{asset}.js' for asset in ('clinic-text', 'booking', 'silwadi-ai-widget')}
    for file in sorted(root.rglob('*.html')):
        relative = file.relative_to(root)
        if relative.parts[0] == 'ai' or not public_file(relative):
            continue
        markup = AssistantMarkup()
        markup.feed(file.read_text(encoding='utf-8'))
        actual = {script_path(script, 'https://silwadi.ae/' + relative.as_posix()) for script in markup.scripts}
        for missing in sorted(required_scripts - actual):
            raise ValueError(f'{relative}: missing executable assistant script {missing}')
        arabic = relative.parts[0] == 'ar'
        if not markup.navigation or any(not any(faq_target(link, arabic) for link in group) for group in markup.navigation):
            raise ValueError(f'{relative}: missing FAQ navigation')
        if not any(faq_target(link, arabic) for link in markup.footer_links):
            raise ValueError(f'{relative}: missing FAQ footer link')
        count += 1
    if count == 0:
        raise ValueError('Public bundle contains no patient pages')

    standalone = AssistantMarkup()
    standalone.feed((root / 'ai/index.html').read_text(encoding='utf-8'))
    actual = {script_path(script, 'https://silwadi.ae/ai/') for script in standalone.scripts}
    for missing in sorted((required_scripts | {'/ai/assets/faq.js', '/ai/site-shell.js'}) - actual):
        raise ValueError(f'ai/index.html: missing executable script {missing}')
    if not any(script_path(script, 'https://silwadi.ae/ai/') == '/ai/assets/silwadi-ai-widget.js' and script.get('data-presentation') == 'page' for script in standalone.scripts):
        raise ValueError('ai/index.html: missing standalone page presentation')
    return count


class AccreditationMarkup(HTMLParser):
    """Read visible accreditation cards and their real asset imports."""

    def __init__(self):
        super().__init__()
        self.section_depth = 0
        self.sections = 0
        self.cards = []
        self.card = None
        self.capture = []
        self.stylesheets = []
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        classes = set(data.get('class', '').split())
        if tag == 'link' and 'stylesheet' in data.get('rel', '').split():
            self.stylesheets.append(data.get('href', ''))
        if tag == 'script' and data.get('type', '').lower() in ('', 'module', 'text/javascript', 'application/javascript'):
            self.scripts.append(data.get('src', ''))
        if tag == 'section':
            if self.section_depth:
                self.section_depth += 1
            elif 'about-accreditations' in classes:
                self.sections += 1
                self.section_depth = 1
        if not self.section_depth:
            return
        if tag == 'article' and 'acc-card' in classes:
            self.card = {key: [] for key in ('text', 'heading', 'authority', 'score', 'grade', 'images')}
            self.card['classes'] = classes
        if self.card is None:
            return
        if tag == 'img':
            self.card['images'].append(data.get('src', ''))
        field = next((field for field in ('authority', 'score', 'grade') if 'acc-card__' + field in classes), None)
        if tag == 'h3':
            field = 'heading'
        if field:
            self.capture.append((tag, field))

    def handle_endtag(self, tag):
        if self.capture and self.capture[-1][0] == tag:
            self.capture.pop()
        if tag == 'article' and self.card is not None:
            self.cards.append(self.card)
            self.card = None
            self.capture = []
        if tag == 'section' and self.section_depth:
            self.section_depth -= 1

    def handle_data(self, data):
        if self.card is not None:
            self.card['text'].append(data)
            for _, field in self.capture:
                self.card[field].append(data)


def validate_accreditations_bundle(root: Path) -> int:
    """Validate the four public scorecard pages in the actual upload folder."""
    root = root.resolve()
    assets = ('accreditations.css', 'accreditations.js', 'assets/jawda-tasneef-mark.png',
              'assets/adhics-aamen-doh-mark.webp', 'assets/uks-certification-logo.jpg')
    for name in assets:
        file = root / name
        if not file.is_file() or not file.stat().st_size:
            raise ValueError(f'Missing or empty accreditation dependency: {name}')

    for name in ('index.html', 'ar/index.html', 'about.html', 'ar/about.html'):
        file = root / name
        if not file.is_file():
            raise ValueError(f'Missing accreditation page: {name}')
        markup = AccreditationMarkup()
        markup.feed(file.read_text(encoding='utf-8'))

        def require(condition, detail):
            if not condition:
                raise ValueError(f'{name}: {detail}')

        require(markup.sections == 1 and len(markup.cards) == 5, 'expected one section with five accreditation cards')
        if name.endswith('index.html'):
            require('/accreditations.css' in markup.stylesheets, 'missing accreditation stylesheet import')
            require('/accreditations.js' in markup.scripts, 'missing accreditation carousel script')
        arabic = name.startswith('ar/')
        authority = 'دائرة الصحة' if arabic else 'Department of Health'
        grade = 'التصنيف A' if arabic else 'GRADE A'
        titles = ('نتيجة جودة JAWDA', 'نتيجة ADHICS') if arabic else ('JAWDA Quality Score', 'ADHICS Score')
        facilities = (
            ('MF368', 'مركز د. منير سلوادي لطب الأسنان' if arabic else 'Dr. Munir Silwadi Dental Centre', 'الكورنيش' if arabic else 'Corniche'),
            ('MF7451', 'مركز د. محمد منير لطب الأسنان' if arabic else 'Dr. Mohamed Munir Dental Centre', 'الراحة مول' if arabic else 'Al Raha Mall'),
        )
        for index, card in enumerate(markup.cards):
            text = ' '.join(' '.join(card['text']).split())
            heading = ''.join(card['heading'])
            image = '/assets/' + ('jawda-tasneef-mark.png' if index == 0 else 'adhics-aamen-doh-mark.webp' if index < 3 else 'uks-certification-logo.jpg')
            require(card['images'] == [image], f'card {index + 1}: incorrect certificate image')
            if index < 3:
                require('acc-card--scored' in card['classes'], f'card {index + 1}: missing scored card layout')
                require(titles[0 if index == 0 else 1] in heading, f'card {index + 1}: incorrect score heading')
                require(''.join(card['authority']).strip() == authority, f'card {index + 1}: incorrect score authority')
                require(''.join(card['score']).strip() == ('99.55%' if index == 0 else '98%'), f'card {index + 1}: incorrect score')
                require(''.join(card['grade']).strip() == grade, f'card {index + 1}: incorrect grade')
            else:
                require(heading.strip() == 'ISO 9001:2015', f'card {index + 1}: incorrect ISO standard')
            if index:
                expected = facilities[(index - 1) % 2]
                require(expected[1] + ' ' + expected[0] in text and expected[2] in text,
                        f'card {index + 1}: incorrect facility mapping')
    return 4


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
    validate_assistant_bundle(output)
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument('--validate-only', action='store_true', help='Check an existing upload folder without modifying it')
    args = parser.parse_args()
    if args.validate_only:
        pages = validate_assistant_bundle(args.output)
        validate_accreditations_bundle(args.output)
        print(f'Assistant/FAQ validation passed on {pages} bundled patient pages; all four accreditation pages passed')
    else:
        count = build_public_bundle(Path.cwd(), args.output)
        validate_accreditations_bundle(args.output)
        print(f"Copied {count} validated public files to {args.output}; all four accreditation pages passed")
