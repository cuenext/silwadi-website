import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { JSDOM } from 'jsdom';

const require = createRequire(import.meta.url);
const language = require('../language.js');
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const seo = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/arabic-seo.json'), 'utf8'));
const overrides = Object.assign(
  {},
  JSON.parse(fs.readFileSync(path.join(ROOT, 'data/arabic-quality-overrides.json'), 'utf8')),
  JSON.parse(fs.readFileSync(path.join(ROOT, 'data/arabic-quality-overrides-extra.json'), 'utf8'))
);
const routes = Object.keys(seo);
const routeSet = new Set(routes.map(route => route === 'index.html' ? '/' : `/${route}`));
const audit = new Map();

const normalize = value => String(value ?? '').replace(/\s+/g, ' ').trim();
const englishUrl = route => route === 'index.html' ? 'https://silwadi.ae/' : `https://silwadi.ae/${route}`;
const arabicUrl = route => route === 'index.html' ? 'https://silwadi.ae/ar/' : `https://silwadi.ae/ar/${route}`;

function translate(source, route) {
  const clean = normalize(source);
  if (!clean) return clean;
  const translated = overrides[clean] || language.translate(clean, 'ar');
  const key = `${clean}\u0000${translated}`;
  if (!audit.has(key)) audit.set(key, { source: clean, arabic: translated, routes: [], override: Boolean(overrides[clean]) });
  const entry = audit.get(key);
  if (!entry.routes.includes(route)) entry.routes.push(route);
  return translated;
}

function updateEnglishHead(source, route) {
  const en = englishUrl(route);
  const ar = arabicUrl(route);
  let html = source.replace(/<link\b(?=[^>]*\brel=["']alternate["'])(?=[^>]*\bhreflang=)[^>]*>/gi, '');
  const alternates = `<link rel="alternate" hreflang="en-AE" href="${en}"><link rel="alternate" hreflang="ar-AE" href="${ar}"><link rel="alternate" hreflang="x-default" href="${en}">`;
  html = html.replace('</head>', `${alternates}</head>`);
  if (!html.includes('arabic-quality.css')) html = html.replace('</head>', '<link rel="stylesheet" href="/arabic-quality.css"></head>');
  if (!html.includes('bilingual-routing.js')) html = html.replace('</head>', '<script src="/bilingual-routing.js"></script></head>');
  return html;
}

function ensureMeta(document, selector, attributes) {
  let element = document.querySelector(selector);
  if (!element) {
    element = document.createElement(attributes.tag || 'meta');
    document.head.appendChild(element);
  }
  Object.entries(attributes).forEach(([name, value]) => {
    if (name !== 'tag') element.setAttribute(name, value);
  });
  return element;
}

function setAlternates(document, route) {
  document.querySelectorAll('link[rel="alternate"][hreflang]').forEach(node => node.remove());
  const values = [
    ['en-AE', englishUrl(route)],
    ['ar-AE', arabicUrl(route)],
    ['x-default', englishUrl(route)]
  ];
  values.forEach(([hreflang, href]) => {
    const link = document.createElement('link');
    link.rel = 'alternate';
    link.hreflang = hreflang;
    link.href = href;
    document.head.appendChild(link);
  });
}

function routeFromPathname(pathname) {
  if (pathname === '/' || pathname === '/index.html') return 'index.html';
  const route = pathname.replace(/^\//, '');
  return routes.includes(route) ? route : null;
}

function rewriteUrl(value, route, attribute = 'href') {
  if (!value || /^(mailto:|tel:|sms:|javascript:|data:)/i.test(value)) return value;
  if (value.startsWith('#')) return value;
  const base = englishUrl(route);
  let url;
  try { url = new URL(value, base); } catch (_) { return value; }
  if (url.hostname !== 'silwadi.ae' && url.hostname !== 'www.silwadi.ae') return value;
  url.searchParams.delete('lang');
  const paired = routeFromPathname(url.pathname);
  if (attribute === 'href' && paired) {
    const target = paired === 'index.html' ? '/ar/' : `/ar/${paired}`;
    return `${target}${url.search}${url.hash}`;
  }
  return `${url.pathname}${url.search}${url.hash}`;
}

function translateDocument(document, route, window) {
  const walker = document.createTreeWalker(document.body, window.NodeFilter.SHOW_TEXT);
  const nodes = [];
  let node = walker.nextNode();
  while (node) { nodes.push(node); node = walker.nextNode(); }
  for (const textNode of nodes) {
    const parent = textNode.parentElement;
    if (!parent || parent.closest('script,style,noscript,code,pre,svg')) continue;
    const original = textNode.nodeValue || '';
    const clean = normalize(original);
    if (!clean || !/[A-Za-z]/.test(clean)) continue;
    const replacement = translate(clean, route);
    if (replacement === clean) continue;
    const leading = original.match(/^\s*/)?.[0] || '';
    const trailing = original.match(/\s*$/)?.[0] || '';
    textNode.nodeValue = `${leading}${replacement}${trailing}`;
  }

  document.querySelectorAll('[placeholder],[aria-label],[title],[alt]').forEach(element => {
    for (const attribute of ['placeholder', 'aria-label', 'title', 'alt']) {
      if (!element.hasAttribute(attribute)) continue;
      const value = element.getAttribute(attribute);
      if (!value || !/[A-Za-z]/.test(value)) continue;
      const replacement = translate(value, route);
      if (replacement !== normalize(value)) element.setAttribute(attribute, replacement);
    }
  });
}

function condenseArabicHomepage(document) {
  document.querySelectorAll('.premium-home-hero__trust li').forEach(item => {
    item.querySelectorAll('br').forEach(br => br.replaceWith(' '));
    const strong = item.querySelector('strong');
    if (!strong) return;
    const secondary = [...item.querySelectorAll('small,p,span')].filter(element => {
      if (element.classList.contains('premium-home-hero__icon')) return false;
      if (strong.contains(element)) return false;
      const text = normalize(element.textContent);
      return ['الحجز', 'الموقع', 'منذ عام 1980', 'Booking', 'Location', 'Since 1980'].includes(text);
    });
    secondary.forEach(element => element.remove());
  });
}

function makeArabicPage(source, route) {
  const dom = new JSDOM(source, { url: englishUrl(route) });
  const { document } = dom.window;
  document.documentElement.lang = 'ar';
  document.documentElement.dir = 'rtl';
  document.body.classList.add('language-ar', 'static-arabic');
  document.title = seo[route].title;
  ensureMeta(document, 'meta[name="description"]', { name: 'description', content: seo[route].description });
  ensureMeta(document, 'meta[name="content-language"]', { name: 'content-language', content: 'ar' });
  ensureMeta(document, 'meta[property="og:title"]', { property: 'og:title', content: seo[route].title });
  ensureMeta(document, 'meta[property="og:description"]', { property: 'og:description', content: seo[route].description });
  ensureMeta(document, 'meta[property="og:url"]', { property: 'og:url', content: arabicUrl(route) });
  ensureMeta(document, 'meta[property="og:locale"]', { property: 'og:locale', content: 'ar_AE' });
  ensureMeta(document, 'meta[property="og:locale:alternate"]', { property: 'og:locale:alternate', content: 'en_AE' });
  const canonical = document.querySelector('link[rel="canonical"]') || document.head.appendChild(document.createElement('link'));
  canonical.rel = 'canonical';
  canonical.href = arabicUrl(route);
  setAlternates(document, route);

  document.querySelectorAll('link[href]').forEach(element => {
    if (element.rel === 'alternate' || element.rel === 'canonical') return;
    element.setAttribute('href', rewriteUrl(element.getAttribute('href'), route, 'asset'));
  });
  document.querySelectorAll('script[src],img[src],source[src],iframe[src]').forEach(element => {
    const src = element.getAttribute('src');
    if (!src) return;
    const parsed = rewriteUrl(src, route, 'asset');
    if (/language\.js(?:\?|$)/.test(src)) element.setAttribute('src', '/arabic-static.js');
    else element.setAttribute('src', parsed);
  });
  document.querySelectorAll('a[href]').forEach(element => element.setAttribute('href', rewriteUrl(element.getAttribute('href'), route, 'href')));
  document.querySelectorAll('form[action]').forEach(element => element.setAttribute('action', rewriteUrl(element.getAttribute('action'), route, 'href')));

  translateDocument(document, route, dom.window);
  if (route === 'index.html') condenseArabicHomepage(document);

  if (!document.querySelector('link[href="/arabic-quality.css"]')) {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = '/arabic-quality.css';
    document.head.appendChild(link);
  }

  return '<!doctype html>\n' + document.documentElement.outerHTML;
}

function patchRuntimeFiles() {
  const appPath = path.join(ROOT, 'app.js');
  let app = fs.readFileSync(appPath, 'utf8');
  app = app.replace("if (isSilwadiDomain && /\\/index\\.html$/.test(pathname)) {", "if (isSilwadiDomain && pathname === '/index.html') {");
  fs.writeFileSync(appPath, app);

  const reviewsPath = path.join(ROOT, 'home-reviews.css');
  let reviews = fs.readFileSync(reviewsPath, 'utf8');
  reviews = reviews.replace(/\.language-ar \.google-reviews-track\s*\{\s*animation-direction\s*:\s*reverse\s*;?\s*\}/g, '');
  fs.writeFileSync(reviewsPath, reviews);
}

function updateSitemap() {
  const sitemapPath = path.join(ROOT, 'sitemap.xml');
  let sitemap = fs.readFileSync(sitemapPath, 'utf8');
  sitemap = sitemap.replace(/\s*<url>\s*<loc>https:\/\/silwadi\.ae\/ar\/[^<]*<\/loc>[\s\S]*?<\/url>/g, '');
  const arabicEntries = routes.map(route => `  <url><loc>${arabicUrl(route)}</loc></url>`).join('\n');
  sitemap = sitemap.replace('</urlset>', `${arabicEntries}\n</urlset>`);
  fs.writeFileSync(sitemapPath, sitemap);
}

for (const route of routes) {
  const file = path.join(ROOT, route);
  if (!fs.existsSync(file)) throw new Error(`Missing English source route: ${route}`);
  const original = fs.readFileSync(file, 'utf8');
  const english = updateEnglishHead(original, route);
  fs.writeFileSync(file, english);
  const arabic = makeArabicPage(english, route);
  const output = path.join(ROOT, 'ar', route);
  fs.mkdirSync(path.dirname(output), { recursive: true });
  fs.writeFileSync(output, arabic);
}

patchRuntimeFiles();
updateSitemap();

const auditRows = [...audit.values()].sort((a, b) => a.source.localeCompare(b.source));
fs.writeFileSync(path.join(ROOT, 'data/arabic-audit.json'), JSON.stringify(auditRows, null, 2) + '\n');
console.log(`Generated ${routes.length} Arabic pages and audited ${auditRows.length} distinct patient-facing strings.`);
