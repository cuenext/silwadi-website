import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';


const carouselSource = readFileSync(
  new URL('../accreditations.js', import.meta.url),
  'utf8',
);


class FakeClassList {
  constructor(owner) {
    this.owner = owner;
  }

  toggle(name, force) {
    const names = new Set(this.owner.className.split(/\s+/).filter(Boolean));
    const enabled = force === undefined ? !names.has(name) : force;
    if (enabled) names.add(name);
    else names.delete(name);
    this.owner.className = [...names].join(' ');
    return enabled;
  }

  contains(name) {
    return this.owner.className.split(/\s+/).includes(name);
  }
}


class FakeElement {
  constructor(document, tagName = 'div') {
    this.document = document;
    this.tagName = tagName.toUpperCase();
    this.attributes = new Map();
    this.children = [];
    this.listeners = new Map();
    this.className = '';
    this.classList = new FakeClassList(this);
    this.scrollLeft = 0;
    this.scrollWidth = 0;
    this.clientWidth = 0;
    this.width = 0;
    this.scrollCalls = [];
    this._disabled = false;
  }

  setAttribute(name, value) {
    this.attributes.set(name, String(value));
  }

  getAttribute(name) {
    return this.attributes.has(name) ? this.attributes.get(name) : null;
  }

  addEventListener(type, listener) {
    if (!this.listeners.has(type)) this.listeners.set(type, []);
    this.listeners.get(type).push(listener);
  }

  dispatch(type) {
    for (const listener of this.listeners.get(type) || []) {
      listener({ currentTarget: this, preventDefault() {} });
    }
  }

  appendChild(child) {
    this.children.push(child);
    return child;
  }

  replaceChildren(...children) {
    if (this.contains(this.document.activeElement)) this.document.activeElement = null;
    this.children = children;
  }

  set innerHTML(value) {
    assert.equal(value, '');
    this.replaceChildren();
  }

  contains(candidate) {
    if (!candidate) return false;
    return this.children.some(
      (child) => child === candidate || child.contains(candidate),
    );
  }

  focus() {
    this.document.activeElement = this;
  }

  set disabled(value) {
    this._disabled = Boolean(value);
    if (this._disabled && this.document.activeElement === this) {
      this.document.activeElement = null;
    }
  }

  get disabled() {
    return this._disabled;
  }

  getBoundingClientRect() {
    return { width: this.width };
  }

  querySelectorAll(selector) {
    return selector === '.acc-card' ? this.cards : [];
  }

  scrollTo(options) {
    this.scrollCalls.push(options);
    this.scrollLeft = options.left;
    this.dispatch('scroll');
  }
}


function createFixture({ lang = 'en', reducedMotion = false } = {}) {
  const document = {
    activeElement: null,
    documentElement: { lang },
    elements: new Map(),
    createElement(tagName) {
      return new FakeElement(document, tagName);
    },
    getElementById(id) {
      return this.elements.get(id) || null;
    },
  };

  const track = new FakeElement(document);
  const previous = new FakeElement(document, 'button');
  const next = new FakeElement(document, 'button');
  const dots = new FakeElement(document);
  const cards = Array.from({ length: 5 }, () => {
    const card = new FakeElement(document, 'article');
    card.width = 280;
    return card;
  });

  track.cards = cards;
  track.gap = '20px';
  track.scrollWidth = 900;
  track.clientWidth = 300;
  document.elements.set('accTrack', track);
  document.elements.set('accPrev', previous);
  document.elements.set('accNext', next);
  document.elements.set('accDots', dots);

  const windowListeners = new Map();
  const window = {
    matchMedia() {
      return { matches: reducedMotion };
    },
    addEventListener(type, listener) {
      if (!windowListeners.has(type)) windowListeners.set(type, []);
      windowListeners.get(type).push(listener);
    },
    dispatch(type) {
      for (const listener of windowListeners.get(type) || []) listener();
    },
  };

  vm.runInNewContext(carouselSource, {
    document,
    getComputedStyle(element) {
      return { gap: element.gap };
    },
    requestAnimationFrame(callback) {
      callback();
      return 1;
    },
    window,
  });

  return { document, dots, next, previous, track, window };
}


test('carousel exposes state, advances, and preserves focus through endpoints and resize', () => {
  const { document, dots, next, previous, track, window } = createFixture();

  assert.equal(dots.children.length, 3);
  assert.equal(dots.children[0].getAttribute('aria-label'), 'Go to accreditation slide 1');
  assert.equal(dots.children[0].getAttribute('aria-current'), 'true');
  assert.equal(previous.getAttribute('aria-disabled'), 'true');
  assert.equal(next.getAttribute('aria-disabled'), 'false');

  next.focus();
  next.dispatch('click');
  assert.equal(track.scrollLeft, 300);
  assert.equal(track.scrollCalls.at(-1).behavior, 'smooth');
  assert.equal(dots.children[1].getAttribute('aria-current'), 'true');
  assert.equal(document.activeElement, next);

  next.dispatch('click');
  assert.equal(track.scrollLeft, 600);
  assert.equal(next.getAttribute('aria-disabled'), 'true');
  assert.equal(previous.getAttribute('aria-disabled'), 'false');
  assert.equal(document.activeElement, next);

  dots.children[2].focus();
  track.clientWidth = 610;
  window.dispatch('resize');
  assert.equal(dots.children.length, 2);
  assert.equal(document.activeElement, dots.children[1]);
});


test('Arabic dot labels are localized and reduced motion avoids smooth scrolling', () => {
  const { dots, track } = createFixture({ lang: 'ar', reducedMotion: true });

  assert.equal(
    dots.children[1].getAttribute('aria-label'),
    'الانتقال إلى الاعتماد رقم 2',
  );
  dots.children[1].dispatch('click');
  assert.equal(track.scrollLeft, 300);
  assert.equal(track.scrollCalls.at(-1).behavior, 'auto');
  assert.equal(dots.children[1].getAttribute('aria-current'), 'true');
});
