const test = require('node:test');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..');
const pngPath = path.join(root, 'assets', 'silwadi-logo-official.png');
const svgPath = path.join(root, 'assets', 'silwadi-logo-official.svg');
const expectedHash = 'f7b77e5eb8e9a170dca0508ed2ef70b6e4983795c845f68ddc847894b74d8ab4';

function publicFiles(extension) {
  const found = [];
  const visit = (directory) => {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      if (entry.name === '.git' || entry.name === '.superpowers' || entry.name === '.tmp' || entry.name === 'review') continue;
      const absolute = path.join(directory, entry.name);
      if (entry.isDirectory()) visit(absolute);
      else if (entry.isFile() && entry.name.endsWith(extension)) found.push(absolute);
    }
  };
  visit(root);
  return found;
}

function attribute(tag, name) {
  return tag.match(new RegExp(`\\b${name}\\s*=\\s*["']([^"']*)["']`, 'i'))?.[1];
}

function cssRules(source, selector) {
  const escaped = selector.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return [...source.matchAll(new RegExp(`${escaped}\\s*\\{([^{}]*)\\}`, 'g'))].map((match) => {
    const declarations = new Map();
    for (const item of match[1].split(';')) {
      const colon = item.indexOf(':');
      if (colon === -1) continue;
      declarations.set(item.slice(0, colon).trim(), item.slice(colon + 1).trim());
    }
    return declarations;
  });
}

function hasCssRule(source, selector, expected) {
  return cssRules(source, selector).some((rule) =>
    Object.entries(expected).every(([property, value]) => rule.get(property) === value)
  );
}

function sha256(buffer) {
  return crypto.createHash('sha256').update(buffer).digest('hex');
}

function pngDimensions(buffer) {
  const signature = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);
  assert.ok(buffer.subarray(0, 8).equals(signature), 'asset must be a valid PNG');
  return {
    width: buffer.readUInt32BE(16),
    height: buffer.readUInt32BE(20)
  };
}

test('canonical PNG is the exact supplied 259 by 225 artwork', () => {
  const png = fs.readFileSync(pngPath);
  assert.equal(sha256(png), expectedHash);
  assert.deepEqual(pngDimensions(png), { width: 259, height: 225 });
});

test('display SVG embeds the exact supplied PNG in its natural bounds', () => {
  assert.ok(fs.existsSync(svgPath), 'display SVG must exist');
  const svg = fs.readFileSync(svgPath, 'utf8');
  assert.match(svg, /<svg\b[^>]*\bwidth="259"[^>]*\bheight="225"[^>]*\bviewBox="0 0 259 225"/);
  const embedded = svg.match(/<image\b[^>]*\bhref="data:image\/png;base64,([A-Za-z0-9+/=]+)"/);
  assert.ok(embedded, 'SVG must embed the PNG as a data URI');
  const png = Buffer.from(embedded[1], 'base64');
  assert.equal(sha256(png), expectedHash);
  assert.deepEqual(pngDimensions(png), { width: 259, height: 225 });
  assert.match(svg, /<image\b[^>]*\bx="0"[^>]*\by="0"[^>]*\bwidth="259"[^>]*\bheight="225"/);
});

test('display SVG is self-contained and uses the approved background key', () => {
  assert.ok(fs.existsSync(svgPath), 'display SVG must exist');
  const svg = fs.readFileSync(svgPath, 'utf8');
  const normalized = svg.replace(/\s+/g, ' ');

  const withoutSvgNamespace = svg.replace('xmlns="http://www.w3.org/2000/svg"', '');
  assert.doesNotMatch(svg, /<script\b|<foreignObject\b|\bon[a-z]+\s*=/i);
  assert.doesNotMatch(withoutSvgNamespace, /\b(?:https?:|file:|javascript:)/i);
  assert.doesNotMatch(svg, /\b(?:href|xlink:href)="(?!data:image\/png;base64,)[^"]+"/i);
  assert.match(normalized, /<filter id="remove-near-white" filterUnits="userSpaceOnUse" x="0" y="0" width="259" height="225" color-interpolation-filters="sRGB">/);
  assert.match(normalized, /values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 -0\.333333 -0\.333333 -0\.333333 0 1"/);
  assert.match(normalized, /<feFuncA type="linear" slope="12" intercept="-0\.08"\s*\/>/);
  assert.match(normalized, /<feComposite in="SourceGraphic" in2="background-key" operator="in"\s*\/>/);
});

test('every production logo image uses the transparent SVG at the natural ratio', () => {
  let logoCount = 0;
  const filesWithLogos = new Set();

  for (const file of publicFiles('.html')) {
    const html = fs.readFileSync(file, 'utf8');
    const tags = html.match(/<img\b[^>]*\bsrc\s*=\s*["'][^"']*silwadi-logo-official\.(?:png|svg)[^"']*["'][^>]*>/gi) ?? [];
    if (tags.length) filesWithLogos.add(path.relative(root, file));
    for (const tag of tags) {
      logoCount += 1;
      assert.match(attribute(tag, 'src'), /silwadi-logo-official\.svg(?:[?#].*)?$/i, `${path.relative(root, file)}: visible logo must use SVG`);
      assert.equal(attribute(tag, 'width'), '259', `${path.relative(root, file)}: logo width`);
      assert.equal(attribute(tag, 'height'), '225', `${path.relative(root, file)}: logo height`);
      assert.ok(attribute(tag, 'alt')?.trim(), `${path.relative(root, file)}: logo needs localized alt text`);
    }
  }

  assert.equal(filesWithLogos.size, 67, 'all 67 production pages must retain a visible logo');
  assert.equal(logoCount, 133, 'all 133 header/footer/template placements must be updated');
});

test('metadata and schema consumers keep the canonical PNG URL', () => {
  const config = JSON.parse(fs.readFileSync(path.join(root, 'data', 'site-config.json'), 'utf8'));
  assert.equal(config.default_social_image, 'https://silwadi.ae/assets/silwadi-logo-official.png');

  for (const file of publicFiles('.html')) {
    const htmlWithoutImages = fs.readFileSync(file, 'utf8').replace(/<img\b[^>]*>/gi, '');
    assert.doesNotMatch(htmlWithoutImages, /silwadi-logo-official\.svg/i, `${path.relative(root, file)}: metadata must keep PNG`);
  }
});

test('shared, homepage, and treatment shells use the approved responsive sizes', () => {
  const styles = fs.readFileSync(path.join(root, 'styles.css'), 'utf8');
  const home = fs.readFileSync(path.join(root, 'home-reviews.css'), 'utf8');
  const treatment = fs.readFileSync(path.join(root, 'treatments', 'treatment-refresh-v1.css'), 'utf8');
  const arabic = fs.readFileSync(path.join(root, 'arabic-quality.css'), 'utf8');

  assert.ok(hasCssRule(styles, '.site-brand-logo', { width: '96px', height: '72px', flex: '0 0 96px' }));
  assert.ok(hasCssRule(styles, '.site-brand-logo', { width: '84px', height: '62px', 'flex-basis': '84px' }));
  assert.ok(hasCssRule(styles, '.site-brand-logo img', { width: '82px', height: 'auto', 'aspect-ratio': '259/225' }));
  assert.ok(hasCssRule(styles, '.site-brand-logo img', { width: '72px', height: 'auto' }));
  assert.ok(hasCssRule(styles, '.site-footer-logo', { width: '128px', height: 'auto', 'aspect-ratio': '259/225', 'mix-blend-mode': 'normal' }));

  assert.ok(hasCssRule(home, '.home-trust-brand', { width: '96px', height: '72px' }));
  assert.ok(hasCssRule(home, '.home-trust-brand', { width: '84px', height: '62px' }));
  assert.ok(hasCssRule(home, '.home-trust-brand img', { width: '82px', height: 'auto', 'aspect-ratio': '259/225' }));
  assert.ok(hasCssRule(home, '.home-trust-brand img', { width: '72px', height: 'auto' }));
  assert.ok(hasCssRule(home, '.home-trust-footer-logo', { width: '128px', height: 'auto', 'aspect-ratio': '259/225', 'mix-blend-mode': 'normal' }));

  assert.ok(hasCssRule(treatment, '.global-brand img', { width: '82px', height: 'auto', 'aspect-ratio': '259/225' }));
  assert.ok(hasCssRule(treatment, '.global-brand img', { width: '72px', height: 'auto' }));
  assert.doesNotMatch(styles + arabic, /\.site-footer-logo\s*\{[^}]*mix-blend-mode\s*:\s*multiply/);
});

test('page-local logo rules preserve the approved ratio instead of square boxes', () => {
  const files = [
    'treatments/endodontics.html',
    'treatments/pediatric-dentistry.html',
    'treatments/people-of-determination.html',
    'ar/treatments/endodontics.html',
    'ar/treatments/pediatric-dentistry.html',
    'ar/treatments/people-of-determination.html'
  ];

  for (const relative of files) {
    const html = fs.readFileSync(path.join(root, relative), 'utf8');
    const selector = relative === 'treatments/endodontics.html' ? '.brand img' : '.global-brand img';
    assert.ok(hasCssRule(html, selector, { width: '82px', height: 'auto', 'aspect-ratio': '259/225' }), `${relative}: desktop logo sizing`);
    assert.ok(hasCssRule(html, selector, { width: '72px', height: 'auto' }), `${relative}: mobile logo sizing`);
    if (relative.endsWith('endodontics.html')) {
      assert.ok(hasCssRule(html, '.site-footer-logo', { width: '128px', height: 'auto', 'aspect-ratio': '259/225', 'mix-blend-mode': 'normal' }), `${relative}: footer logo sizing`);
    }
  }
});
