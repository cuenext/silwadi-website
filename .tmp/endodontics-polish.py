from pathlib import Path
import json
import re

path = Path('review/endodontics-v4.html')
text = path.read_text(encoding='utf-8')

title = 'Root Canal Treatment in Abu Dhabi | Silwadi Dental Center'
description = 'Specialist root canal treatment in Abu Dhabi at Silwadi Dental Center, including retreatment, microsurgery, dental trauma care and tooth preservation.'
production_url = 'https://silwadi.ae/treatments/endodontics.html'
hero_url = 'https://silwadi.ae/assets/services/endodontics.webp'

def contract_errors(source):
    errors = []
    required = [
        f'<title>{title}</title>',
        f'<meta name="description" content="{description}">',
        f'<link rel="canonical" href="{production_url}">',
        '<meta property="og:type" content="website">',
        '<meta property="og:locale" content="en_AE">',
        '<meta name="twitter:card" content="summary_large_image">',
        'data-seo-schema',
        'doctor-photo--ahmed',
        'doctor-photo--lana',
        'aspect-ratio:4/3',
        'fetchpriority="high"',
        'aria-label="Breadcrumb"',
    ]
    for item in required:
        if item not in source:
            errors.append(item)
    if source.count('<h1>') != 1:
        errors.append('exactly one h1')
    if 'noindex,nofollow,noarchive,nosnippet,noimageindex' not in source:
        errors.append('review noindex preserved')
    return errors

pre = contract_errors(text)
if not pre:
    raise SystemExit('expected pre-change review page to fail the final contract')
print('RED contract confirmed:', len(pre), 'requirements not yet satisfied')

schema = {
    '@context': 'https://schema.org',
    '@graph': [
        {
            '@type': 'WebPage',
            '@id': production_url + '#webpage',
            'url': production_url,
            'name': title,
            'description': description,
            'inLanguage': 'en-AE',
            'isPartOf': {'@id': 'https://silwadi.ae/#website'},
            'mainEntity': {'@id': production_url + '#service'},
            'primaryImageOfPage': {
                '@type': 'ImageObject',
                'url': hero_url,
                'width': 1200,
                'height': 900,
            },
        },
        {
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': 'https://silwadi.ae/'},
                {'@type': 'ListItem', 'position': 2, 'name': 'Treatments', 'item': 'https://silwadi.ae/treatments.html'},
                {'@type': 'ListItem', 'position': 3, 'name': 'Endodontics', 'item': production_url},
            ],
        },
        {
            '@type': 'Service',
            '@id': production_url + '#service',
            'name': 'Root Canal Treatment and Endodontics',
            'serviceType': 'Specialist endodontic assessment, root canal treatment, retreatment, microsurgery and dental trauma care',
            'url': production_url,
            'provider': {'@id': 'https://silwadi.ae/#organization'},
            'areaServed': {'@type': 'City', 'name': 'Abu Dhabi'},
            'isPartOf': {'@id': 'https://silwadi.ae/#website'},
        },
        {
            '@type': 'Person',
            '@id': 'https://silwadi.ae/doctors/dr-ahmed-el-shehri.html#person',
            'name': 'Dr. Ahmed El Shehri',
            'jobTitle': 'Specialist Endodontist',
            'url': 'https://silwadi.ae/doctors/dr-ahmed-el-shehri.html',
            'worksFor': {'@id': 'https://silwadi.ae/#organization'},
            'knowsAbout': ['Endodontics', 'Root Canal Treatment'],
        },
        {
            '@type': 'Person',
            '@id': 'https://silwadi.ae/doctors/dr-lana-masoud.html#person',
            'name': 'Dr. Lana Almasoud',
            'jobTitle': 'Specialist Endodontist',
            'url': 'https://silwadi.ae/doctors/dr-lana-masoud.html',
            'worksFor': {'@id': 'https://silwadi.ae/#organization'},
            'knowsAbout': ['Endodontics', 'Root Canal Treatment', 'Root Canal Retreatment'],
        },
        {
            '@type': 'FAQPage',
            '@id': production_url + '#faq',
            'mainEntity': [
                {
                    '@type': 'Question',
                    'name': 'What is root canal treatment?',
                    'acceptedAnswer': {'@type': 'Answer', 'text': 'Root canal treatment removes inflamed or infected pulp tissue from inside the tooth. The root canal system is then cleaned, disinfected, shaped and sealed before the tooth receives the restoration appropriate for its condition.'},
                },
                {
                    '@type': 'Question',
                    'name': 'Does root canal treatment hurt?',
                    'acceptedAnswer': {'@type': 'Answer', 'text': 'Root canal treatment is generally carried out under local anaesthesia. Some tenderness can occur afterwards, particularly when the tooth was inflamed or infected before treatment.'},
                },
                {
                    '@type': 'Question',
                    'name': 'Can a root canal save my natural tooth?',
                    'acceptedAnswer': {'@type': 'Answer', 'text': 'Preserving the natural tooth is an important aim of endodontic care when the tooth is suitable for treatment and can be restored appropriately.'},
                },
                {
                    '@type': 'Question',
                    'name': 'Why would a tooth need root canal retreatment?',
                    'acceptedAnswer': {'@type': 'Answer', 'text': 'A previously treated tooth may need reassessment if symptoms persist, infection recurs or the previous root canal system requires additional treatment.'},
                },
                {
                    '@type': 'Question',
                    'name': 'Will I need a crown after root canal treatment?',
                    'acceptedAnswer': {'@type': 'Answer', 'text': 'The final restoration depends on the tooth, the amount of remaining tooth structure and the clinical situation. Your dentist or specialist will advise on the appropriate restoration after treatment.'},
                },
            ],
        },
    ],
}
schema_json = json.dumps(schema, ensure_ascii=False, separators=(',', ':'))

old_head = '''<meta name="robots" content="noindex,nofollow,noarchive,nosnippet,noimageindex">
<title>Private Review — Endodontics V4 | Silwadi Dental Center</title>
<meta name="description" content="Private review draft of the Silwadi Dental Center endodontics page.">
<meta name="theme-color" content="#083847">
<style>'''
new_head = f'''<meta name="robots" content="noindex,nofollow,noarchive,nosnippet,noimageindex">
<meta name="content-language" content="en">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{production_url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Silwadi Dental Center">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{production_url}">
<meta property="og:image" content="{hero_url}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="900">
<meta property="og:image:alt" content="Endodontic root canal treatment using a rubber dam and rotary file">
<meta property="og:locale" content="en_AE">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{hero_url}">
<link rel="preload" as="image" href="/assets/services/endodontics.webp?v=20260915-review-hero">
<meta name="theme-color" content="#083847">
<script type="application/ld+json" data-seo-schema>{schema_json}</script>
<style>'''

old_photo_css = '.doctor-photo{background:#e8f1f2;min-height:290px}.doctor-photo img{width:100%;height:100%;object-fit:cover;object-position:center top}'
new_photo_css = '.doctor-photo{background:#e8f1f2;min-height:290px;overflow:hidden}.doctor-photo img{width:100%;height:100%;object-fit:cover;object-position:center top}.doctor-photo--ahmed img{object-position:50% 18%}.doctor-photo--lana img{object-position:50% 20%}'
old_mobile = '.doctor-photo{height:360px}'
new_mobile = '.doctor-photo{height:auto;min-height:0;aspect-ratio:4/3}'
old_breadcrumb = '<div class="breadcrumb"><span>Home</span><span>/</span><span>Treatments</span><span>/</span><strong>Endodontics</strong></div>'
new_breadcrumb = '<nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/treatments.html">Treatments</a><span aria-hidden="true">/</span><span aria-current="page">Endodontics</span></nav>'
old_hero = '<img class="hero-visual__image" src="/assets/services/endodontics.webp?v=20260915-review-hero" alt="Root canal treatment under rubber dam at Silwadi Dental Center">'
new_hero = '<img class="hero-visual__image" src="/assets/services/endodontics.webp?v=20260915-review-hero" alt="Endodontic root canal treatment using a rubber dam and rotary file" width="1200" height="900" decoding="async" fetchpriority="high">'
old_ahmed = '<div class="doctor-photo"><img src="https://silwadi.ae/assets/dr-ahmed-new.webp" alt="Dr. Ahmed El Shehri"></div>'
new_ahmed = '<div class="doctor-photo doctor-photo--ahmed"><img src="https://silwadi.ae/assets/dr-ahmed-new.webp" alt="Dr. Ahmed El Shehri" loading="lazy" decoding="async"></div>'
old_lana = '<div class="doctor-photo"><img src="https://silwadi.ae/assets/dr-lana-new-v2.webp" alt="Dr. Lana Almasoud"></div>'
new_lana = '<div class="doctor-photo doctor-photo--lana"><img src="https://silwadi.ae/assets/dr-lana-new-v2.webp" alt="Dr. Lana Almasoud" loading="lazy" decoding="async"></div>'

replacements = [
    (old_head, new_head, 'head SEO block'),
    (old_photo_css, new_photo_css, 'doctor crop CSS'),
    (old_mobile, new_mobile, 'mobile doctor aspect ratio'),
    (old_breadcrumb, new_breadcrumb, 'breadcrumb semantics'),
    (old_hero, new_hero, 'hero image attributes'),
    (old_ahmed, new_ahmed, 'Ahmed portrait class'),
    (old_lana, new_lana, 'Lana portrait class'),
]
for old, new, label in replacements:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly one match, found {count}')
    text = text.replace(old, new, 1)

path.write_text(text, encoding='utf-8')
final = path.read_text(encoding='utf-8')
errors = contract_errors(final)
if errors:
    raise SystemExit('GREEN contract failed: ' + '; '.join(errors))
if not 50 <= len(title) <= 60:
    raise SystemExit(f'unexpected title length: {len(title)}')
if not 140 <= len(description) <= 160:
    raise SystemExit(f'unexpected description length: {len(description)}')
match = re.search(r'<script type="application/ld\+json" data-seo-schema>(.*?)</script>', final, re.S)
if not match:
    raise SystemExit('JSON-LD block missing')
parsed = json.loads(match.group(1))
types = {item.get('@type') for item in parsed.get('@graph', [])}
needed_types = {'WebPage', 'BreadcrumbList', 'Service', 'Person', 'FAQPage'}
if not needed_types.issubset(types):
    raise SystemExit(f'missing schema types: {needed_types - types}')
if final.count('<h1>') != 1:
    raise SystemExit('page must contain exactly one H1')
if 'Private Review — Endodontics V4 | Silwadi Dental Center' in final:
    raise SystemExit('old generic review title still present')
print('GREEN contract passed: responsive portraits + final SEO metadata/schema are valid')
