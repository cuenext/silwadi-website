const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = path.resolve(__dirname, '..');
const app = fs.readFileSync(path.join(root, 'app.js'), 'utf8');
const language = fs.readFileSync(path.join(root, 'language.js'), 'utf8');
const routeStart = app.indexOf('(function routeConsultationCtas()');
const routeEnd = app.indexOf('})();', routeStart) + 5;
const route = app.slice(routeStart, routeEnd);
const helperStart = language.indexOf('  function locationHref()');
const helperEnd = language.indexOf('  function historyUrl(', helperStart);
const languageHelpers = language.slice(helperStart, helperEnd);

function routeHref(sourceUrl, originalHref = 'tel:+97126662408') {
  const anchor = {
    href: originalHref,
    textContent: 'Book a Consultation',
    getAttribute(name) { return name === 'href' ? this.href : null; },
    setAttribute(name, value) { if (name === 'href') this.href = value; }
  };
  const location = new URL(sourceUrl);
  const context = {
    URL,
    window: { location },
    document: { querySelectorAll(selector) {
      assert.equal(selector, 'a');
      return [anchor];
    } }
  };

  vm.runInNewContext(
    `${languageHelpers}\nwindow.SilwadiLanguage = { withLanguageQuery, getRequestedLanguage, getLanguage() { return 'en'; } };\n${route}`,
    context
  );
  return { emittedHref: anchor.href, resolvedUrl: new URL(anchor.href, sourceUrl).href };
}

test('English location consultation links resolve to the site contact form', () => {
  for (const branch of ['al-raha', 'corniche']) {
    const result = routeHref(`https://silwadi.ae/locations/${branch}.html`);
    assert.equal(result.resolvedUrl, 'https://silwadi.ae/contact.html#consultation-form');
  }
});

test('Arabic location consultation links keep the Arabic route and language query', () => {
  const result = routeHref('https://silwadi.ae/ar/locations/al-raha.html?lang=ar');
  assert.equal(result.emittedHref, '../contact.html?lang=ar#consultation-form');
  assert.equal(result.resolvedUrl, 'https://silwadi.ae/ar/contact.html?lang=ar#consultation-form');
});

test('root, doctor, and treatment consultation links keep their existing destinations', () => {
  const cases = [
    ['https://silwadi.ae/', 'https://silwadi.ae/contact.html#consultation-form'],
    ['https://silwadi.ae/doctors/dr-one.html', 'https://silwadi.ae/contact.html#consultation-form'],
    ['https://silwadi.ae/treatments/implants.html', 'https://silwadi.ae/contact.html#consultation-form']
  ];
  for (const [source, expected] of cases) {
    assert.equal(routeHref(source).resolvedUrl, expected);
  }
});

test('contact page consultation controls are left to the page-level behavior', () => {
  const result = routeHref('https://silwadi.ae/contact.html', '#consultation-form');
  assert.equal(result.emittedHref, '#consultation-form');
  assert.equal(result.resolvedUrl, 'https://silwadi.ae/contact.html#consultation-form');
});
