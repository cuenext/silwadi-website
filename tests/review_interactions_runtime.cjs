// DOM and scheduling boundaries for the actual review, language and app scripts.
// No browser dependency: renderer output creates fresh card objects on each write.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');

class Target {
  constructor() { this.listeners = new Map(); }
  addEventListener(type, callback) {
    if (!this.listeners.has(type)) this.listeners.set(type, new Set());
    this.listeners.get(type).add(callback);
  }
  removeEventListener(type, callback) { this.listeners.get(type)?.delete(callback); }
  dispatchEvent(event) {
    event.target ||= this;
    event.preventDefault ||= function() { this.defaultPrevented = true; };
    for (const callback of this.listeners.get(event.type) || []) callback(event);
    if (event.bubbles && this.parentElement) this.parentElement.dispatchEvent(event);
    return !event.defaultPrevented;
  }
  listenerCount(type) { return this.listeners.get(type)?.size || 0; }
}

class Element extends Target {
  constructor(attrs = {}, text = '') {
    super(); this.attrs = attrs; this.textContent = text; this.children = [];
    const classes = new Set();
    this.classList = {contains: c => classes.has(c), add: c => classes.add(c),
      remove: (...cs) => cs.forEach(c => classes.delete(c)),
      toggle(c, value) { if (value) classes.add(c); else classes.delete(c); }};
    this.style = {setProperty: (key, value) => { this.style[key] = value; }};
  }
  getAttribute(name) { return this.attrs[name] ?? null; }
  hasAttribute(name) { return name in this.attrs; }
  setAttribute(name, value) { this.attrs[name] = String(value); if (name === 'lang') this.lang = value; }
  removeAttribute(name) { delete this.attrs[name]; }
  closest(selector) {
    if (selector === '[data-review-expand]' && this.hasAttribute('data-review-expand')) return this;
    return this.parentElement?.closest?.(selector) || null;
  }
  focus() { document.activeElement = this; }
  get isConnected() { return !this.detached; }
  querySelector(selector) { return this.selectors?.[selector] || null; }
  querySelectorAll(selector) { return this.selections?.[selector] || []; }
  appendChild(child) { this.children.push(child); return child; }
  getBoundingClientRect() { return {width: this.width || 1000}; }
}

const document = new Target();
document.documentElement = new Element();
document.documentElement.lang = process.argv[3] || 'en';
document.body = new Element();
document.head = new Element();
document.visibilityState = 'visible';
document.readyState = 'complete';
document.title = '';
document.createElement = () => new Element();
document.getElementById = () => null;
const dialog = new Element();
const close = new Element();
const maps = new Element({href: 'https://maps.app.goo.gl/Ln2vEZmQmgWjb3ETA'});
const fields = Object.fromEntries(['name', 'avatar', 'text', 'stars'].map(n => [`[data-review-${n}]`, new Element()]));
dialog.selectors = {...fields, '.review-dialog__maps': maps, '[data-review-url]': maps, 'a': maps};
dialog.open = false;
dialog.showModal = () => { dialog.open = true; close.focus(); };
dialog.close = () => { dialog.open = false; dialog.dispatchEvent({type: 'close'}); };
const viewport = new Element();
viewport.scrollLeft = 0;
const track = new Element();
viewport.selectors = {'.google-reviews-track': track};
let groups;
function parseCards(markup, group) {
  const decode = text => text.replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
  return [...markup.matchAll(/<article\b([^>]*)>([\s\S]*?)<\/article>/g)].map(([, attributes, body]) => {
    const attrs = Object.fromEntries([...attributes.matchAll(/([\w-]+)(?:="([^"]*)")?/g)].map(([, key, value]) => [key, decode(value || '')]));
    const field = regex => decode(body.match(regex)?.[1] || '');
    const card = new Element(attrs);
    card.parentElement = group;
    card.selectors = {
      '.google-review-card__top strong': new Element({}, field(/<strong>(.*?)<\/strong>/)),
      '.review-avatar': new Element({}, field(/class="review-avatar"[^>]*>(.*?)<\/span>/)),
      'p': new Element({}, field(/<p>(.*?)<\/p>/)),
      '.review-stars': new Element({'aria-label': field(/class="review-stars" aria-label="(.*?)"/)}, '★★★★★')
    };
    Object.values(card.selectors).forEach(child => { child.parentElement = card; });
    return card;
  });
}
groups = [new Element(), new Element({'aria-hidden': 'true'})];
for (const group of groups) {
  group.parentElement = document;
  Object.defineProperty(group, 'innerHTML', {set(markup) {
    (this.cards || []).forEach(card => { card.detached = true; });
    this.cards = parseCards(markup, this);
  }});
}
track.firstElementChild = groups[0];
track.selections = {'.google-reviews-group': groups};
document.querySelector = selector => ({'[data-review-dialog]': dialog, '[data-review-close]': close,
  '.google-reviews-viewport': viewport, '.google-reviews-track': track}[selector] || null);
document.querySelectorAll = selector => selector === '[data-review-expand]'
  ? groups[0].cards || [] : [];

const frames = new Map();
let nextFrame = 1;
let cancelled = 0;
let now = 0;
const window = new Target();
window.location = {hostname: 'test.invalid', pathname: document.documentElement.lang === 'ar' ? '/ar/' : '/', href: 'https://test.invalid/', search: '', hash: ''};
const media = {mobile: {matches: true}, reducedMotion: {matches: false}};
window.matchMedia = query => query.includes('760') ? media.mobile : media.reducedMotion;
const context = {window, document, URL, console,
  localStorage: {getItem: () => null, setItem() {}},
  CustomEvent: function(type, options) { this.type = type; this.detail = options.detail; },
  performance: {now: () => now},
  requestAnimationFrame(callback) { const id = nextFrame++; frames.set(id, callback); return id; },
  cancelAnimationFrame(id) { if (frames.delete(id)) cancelled++; }
};
vm.createContext(context);
const run = file => vm.runInContext(fs.readFileSync(file, 'utf8'), context, {filename: file});
run('google-reviews-data.js');
run('google-reviews.js');
run(document.documentElement.lang === 'ar' ? 'arabic-static.js' : 'language.js');
run('app.js');
function click(element) { element.dispatchEvent({type: 'click', bubbles: true}); }
function key(element, value) { const event = {type: 'keydown', key: value, bubbles: true}; element.dispatchEvent(event); return event; }
function tick(time) {
  now = time;
  const pending = [...frames.values()]; frames.clear();
  pending.forEach(callback => callback(time));
}
const scenario = process.argv[2];
const interactive = () => groups[0].cards;
if (scenario === 'dialog-url') {
  // Canonical records 0..125 are Corniche; 126..156 are Al Raha.
  const cards = [interactive()[126], interactive()[0]];
  assert.notEqual(cards[0].getAttribute('data-review-url'), cards[1].getAttribute('data-review-url'));
  for (const card of cards) {
    const canonical = window.SILWADI_GOOGLE_REVIEWS.find(
      review => review.id === card.getAttribute('data-review-id')
    );
    assert.ok(canonical, 'rendered cards must resolve to the trusted review dataset');
    card.setAttribute('data-review-url', 'javascript:alert(1)');
    card.focus(); click(card.querySelector('p'));
    assert.equal(dialog.open, true);
    assert.equal(maps.getAttribute('href'), canonical.sourceUrl,
      'dialog must use the trusted dataset URL rather than mutable DOM text');
    assert.equal(fields['[data-review-text]'].textContent, card.querySelector('p').textContent);
    dialog.close();
  }
} else if (scenario === 'delegation') {
  window.renderSilwadiGoogleReviews('ar');
  const card = interactive()[10];
  for (const activation of ['click', 'Enter', ' ']) {
    card.focus();
    if (activation === 'click') click(card.querySelector('p'));
    else assert.equal(key(card, activation).defaultPrevented, true);
    assert.equal(dialog.open, true, 'fresh cards must open after rendering');
    assert.equal(fields['[data-review-name]'].textContent, card.querySelector('.google-review-card__top strong').textContent);
    dialog.close();
  }
  click(groups[1].cards[0]);
  assert.equal(dialog.open, false, 'loop copy must remain inert');
} else if (scenario === 'focus-close') {
  const card = interactive()[0];
  for (const action of ['close', 'backdrop', 'Escape', 'native']) {
    card.focus(); click(card);
    if (action === 'close') click(close);
    if (action === 'backdrop') click(dialog);
    if (action === 'Escape') key(document, 'Escape');
    if (action === 'native') dialog.close();
    assert.equal(dialog.open, false);
    assert.equal(document.activeElement, card, `${action} must return focus to selected card`);
  }
} else if (scenario === 'language') {
  const id = interactive()[0].getAttribute('data-review-id');
  window.SilwadiLanguage.applyLanguage('ar');
  assert.equal(interactive()[0].querySelector('p').textContent, window.SILWADI_GOOGLE_REVIEWS[0].summary.ar, 'language switch must rerender bilingual summaries');
  window.SilwadiLanguage.applyLanguage('en');
  assert.equal(interactive()[0].querySelector('p').textContent, window.SILWADI_GOOGLE_REVIEWS[0].summary.en);
  assert.equal(interactive()[0].getAttribute('data-review-id'), id);
} else if (scenario === 'initial-language') {
  assert.equal(interactive().length, 157);
  const language = document.documentElement.lang;
  assert.equal(interactive()[0].querySelector('p').textContent, window.SILWADI_GOOGLE_REVIEWS[0].summary[language]);
  click(interactive()[0]); assert.equal(dialog.open, true);
} else if (scenario === 'mobile-wrap') {
  groups[0].width = 1000;
  tick(100);
  viewport.scrollLeft = 999;
  tick(180);
  // 80ms at 35px/s moves 2.8px: crossing 1000px must retain 1.8px.
  assert.ok(Math.abs(viewport.scrollLeft - 1.8) < 1e-9,
    'mobile looping must subtract one group width and preserve the overshoot');
  tick(260);
  assert.ok(Math.abs(viewport.scrollLeft - 4.6) < 1e-9,
    'mobile scrolling must continue smoothly after the wrap');
} else if (scenario === 'mobile-reinit') {
  for (let i = 0; i < 3; i++) {
    viewport.scrollLeft = 300;
    window.renderSilwadiGoogleReviews(i % 2 ? 'en' : 'ar');
    assert.equal(viewport.scrollLeft, 0, 'render must reset stale carousel position');
    assert.equal(frames.size, 1, 'reinitialization must leave exactly one RAF loop');
    assert.equal(viewport.listenerCount('pointerdown'), 1);
    assert.equal(window.listenerCount('pointerup'), 1);
    assert.equal(viewport.listenerCount('wheel'), 1);
    assert.equal(viewport.listenerCount('focusin'), 1);
  }
  assert.equal(cancelled, 3, 'each render must cancel its previous RAF');
  tick(100); tick(180);
  assert.equal(viewport.scrollLeft, 2.8000000000000003);
  viewport.dispatchEvent({type: 'pointerdown'});
  tick(260); assert.equal(viewport.scrollLeft, 2.8000000000000003);
  window.dispatchEvent({type: 'pointerup'});
  tick(5400); assert.ok(viewport.scrollLeft > 2.8);
  const position = viewport.scrollLeft;
  media.reducedMotion.matches = true;
  tick(5480); assert.equal(viewport.scrollLeft, position, 'reduced motion must stop mobile scrolling');
  media.reducedMotion.matches = false;
  media.mobile.matches = false;
  tick(5560); assert.equal(viewport.scrollLeft, position, 'desktop must leave scrolling to CSS');
  media.mobile.matches = true;
  document.visibilityState = 'hidden';
  tick(5640); assert.equal(viewport.scrollLeft, position, 'hidden pages must not move');
} else throw Error(`Unknown scenario: ${scenario}`);
console.log(JSON.stringify({ok: true, scenario}));
