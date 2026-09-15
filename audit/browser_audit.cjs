const fs = require('fs');
const { chromium } = require('playwright');

const xml = fs.readFileSync('sitemap.xml', 'utf8');
const urls = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => m[1]);
const errors = [];
const warnings = [];
const pages = [];
const failedInternalResources = new Set();

const isInternal = raw => {
  try { return new URL(raw).hostname === 'silwadi.ae'; } catch (_) { return false; }
};

(async () => {
  const browser = await chromium.launch({ headless: true });
  const desktop = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  desktop.setDefaultTimeout(10000);
  let current = '';

  desktop.on('pageerror', e => errors.push(`PAGEERROR | ${current} | ${e.message}`));
  desktop.on('console', msg => {
    if (msg.type() === 'error') warnings.push(`CONSOLE_ERROR | ${current} | ${msg.text()}`);
  });
  desktop.on('requestfailed', req => {
    if (isInternal(req.url())) failedInternalResources.add(`${current} | ${req.url()} | ${req.failure()?.errorText || 'failed'}`);
  });
  desktop.on('response', res => {
    if (isInternal(res.url()) && res.status() >= 400) failedInternalResources.add(`${current} | HTTP ${res.status()} | ${res.url()}`);
  });

  for (const url of urls) {
    current = url;
    try {
      const response = await desktop.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 });
      const state = await desktop.evaluate(() => ({
        title: document.title,
        h1: document.querySelectorAll('h1').length,
        main: !!document.querySelector('main'),
        bodyText: (document.body?.innerText || '').trim().length,
        links: document.querySelectorAll('a[href]').length,
        buttons: document.querySelectorAll('button').length,
        language: document.documentElement.lang,
        direction: document.documentElement.dir || 'ltr',
      }));
      const status = response?.status() || 0;
      pages.push({ url, status, ...state });
      if (status !== 200) errors.push(`BROWSER_HTTP_${status} | ${url}`);
      if (!state.main || state.bodyText < 100) errors.push(`BROWSER_EMPTY_OR_NO_MAIN | ${url}`);
      if (state.h1 !== 1) errors.push(`BROWSER_H1_COUNT_${state.h1} | ${url}`);
    } catch (e) {
      errors.push(`BROWSER_LOAD_FAIL | ${url} | ${e.message}`);
    }
  }

  // Booking CTA journey. Never submit a completed form.
  try {
    current = 'https://silwadi.ae/';
    await desktop.goto(current, { waitUntil: 'domcontentloaded' });
    const book = desktop.locator('a[href*="contact.html#consultation-form"]').first();
    if (!(await book.count())) {
      errors.push('HOME_BOOK_CTA_MISSING');
    } else {
      await book.click();
      await desktop.waitForLoadState('domcontentloaded');
      const dialogOpen = await desktop.locator('[data-booking-modal][open]').count();
      if (!dialogOpen && !desktop.url().includes('contact.html')) {
        errors.push(`HOME_BOOK_CTA_BAD_DESTINATION | ${desktop.url()}`);
      }
      if (!dialogOpen && !(await desktop.locator('#consultation-form').count())) {
        errors.push('HOME_BOOK_CTA_NO_FORM_OR_MODAL');
      }
    }
  } catch (e) {
    errors.push(`HOME_BOOK_CTA_JOURNEY_FAIL | ${e.message}`);
  }

  // Contact forms: existence, required fields, native validation, and no accidental request when invalid.
  for (const url of ['https://silwadi.ae/contact.html', 'https://silwadi.ae/ar/contact.html']) {
    try {
      current = url;
      await desktop.goto(url, { waitUntil: 'domcontentloaded' });
      const form = desktop.locator('[data-consultation-form]').first();
      if (!(await form.count())) {
        errors.push(`CONTACT_FORM_MISSING | ${url}`);
        continue;
      }
      const names = await form.locator('input[name],select[name],textarea[name]').evaluateAll(els => els.map(e => e.getAttribute('name')));
      for (const needed of ['name', 'phone', 'email', 'treatment', 'time', 'clinic', 'privacy-consent']) {
        if (!names.includes(needed)) errors.push(`CONTACT_FIELD_MISSING | ${url} | ${needed}`);
      }
      const submit = form.locator('button[type="submit"]');
      if (!(await submit.count())) errors.push(`CONTACT_SUBMIT_MISSING | ${url}`);
      else {
        let bookingRequests = 0;
        const countRequest = req => { if (req.url().includes('booking-submit.php')) bookingRequests += 1; };
        desktop.on('request', countRequest);
        await submit.click();
        await desktop.waitForTimeout(250);
        desktop.off('request', countRequest);
        const valid = await form.evaluate(el => el.checkValidity());
        if (valid) errors.push(`EMPTY_CONTACT_FORM_UNEXPECTEDLY_VALID | ${url}`);
        if (bookingRequests !== 0) errors.push(`INVALID_FORM_SENT_NETWORK_REQUEST | ${url} | count=${bookingRequests}`);
      }
    } catch (e) {
      errors.push(`CONTACT_FORM_BROWSER_FAIL | ${url} | ${e.message}`);
    }
  }

  // Homepage review dialog.
  try {
    current = 'https://silwadi.ae/';
    await desktop.goto(current, { waitUntil: 'domcontentloaded' });
    const trigger = desktop.locator('[data-review-expand]').first();
    if (await trigger.count()) {
      await trigger.click();
      const dialog = desktop.locator('[data-review-dialog]');
      if (!(await dialog.count()) || !(await dialog.evaluate(el => el.open))) errors.push('REVIEW_DIALOG_DID_NOT_OPEN');
      const close = desktop.locator('[data-review-close]');
      if (await close.count()) await close.click();
      if (await dialog.count() && await dialog.evaluate(el => el.open)) errors.push('REVIEW_DIALOG_DID_NOT_CLOSE');
    } else warnings.push('REVIEW_TRIGGER_NOT_FOUND_ON_HOME');
  } catch (e) {
    errors.push(`REVIEW_DIALOG_FAIL | ${e.message}`);
  }

  // FAQ behavior on every page that has an FAQ button.
  for (const url of urls) {
    try {
      current = url;
      await desktop.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 });
      const first = desktop.locator('[data-faq-button]').first();
      if (!(await first.count())) continue;
      const before = await first.getAttribute('aria-expanded');
      await first.click();
      const after = await first.getAttribute('aria-expanded');
      if (before === after || after !== 'true') errors.push(`FAQ_TOGGLE_FAIL | ${url} | before=${before} after=${after}`);
    } catch (e) {
      errors.push(`FAQ_BROWSER_FAIL | ${url} | ${e.message}`);
    }
  }

  // Doctor search/filter behavior.
  for (const url of ['https://silwadi.ae/doctors.html', 'https://silwadi.ae/ar/doctors.html']) {
    try {
      current = url;
      await desktop.goto(url, { waitUntil: 'domcontentloaded' });
      const search = desktop.locator('[data-doctor-search]');
      const cards = desktop.locator('[data-doctor-card]');
      if (!(await search.count())) {
        warnings.push(`DOCTOR_SEARCH_NOT_FOUND | ${url}`);
      } else {
        const total = await cards.count();
        await search.fill('Munir');
        await desktop.waitForTimeout(100);
        const visible = await cards.evaluateAll(els => els.filter(e => !e.hidden).length);
        if (total && visible >= total) errors.push(`DOCTOR_SEARCH_DID_NOT_FILTER | ${url} | total=${total} visible=${visible}`);
        await search.fill('');
      }
      const filter = desktop.locator('[data-specialty-filter]').filter({ hasNotText: /^All$|^الكل$/ }).first();
      if (await filter.count()) {
        await filter.click();
        if ((await filter.getAttribute('aria-pressed')) !== 'true') errors.push(`DOCTOR_FILTER_ARIA_FAIL | ${url}`);
      }
    } catch (e) {
      errors.push(`DOCTOR_DIRECTORY_FAIL | ${url} | ${e.message}`);
    }
  }

  // Language switch should move between English and Arabic without 404.
  for (const url of ['https://silwadi.ae/', 'https://silwadi.ae/ar/']) {
    try {
      current = url;
      await desktop.goto(url, { waitUntil: 'domcontentloaded' });
      const sw = desktop.locator('[data-language-switch]').first();
      if (!(await sw.count())) {
        warnings.push(`LANGUAGE_SWITCH_NOT_FOUND | ${url}`);
        continue;
      }
      await Promise.all([
        desktop.waitForLoadState('domcontentloaded').catch(() => {}),
        sw.click(),
      ]);
      const destination = desktop.url();
      if (url.endsWith('/ar/') && destination.includes('/ar/')) errors.push(`AR_TO_EN_LANGUAGE_SWITCH_FAIL | ${destination}`);
      if (!url.endsWith('/ar/') && !destination.includes('/ar/')) errors.push(`EN_TO_AR_LANGUAGE_SWITCH_FAIL | ${destination}`);
    } catch (e) {
      errors.push(`LANGUAGE_SWITCH_FAIL | ${url} | ${e.message}`);
    }
  }

  // Mobile rendering: every sitemap page, horizontal overflow, and menu operation wherever present.
  const mobile = await browser.newPage({ viewport: { width: 390, height: 844 }, isMobile: true });
  mobile.setDefaultTimeout(10000);
  for (const url of urls) {
    try {
      current = url;
      await mobile.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 });
      const dim = await mobile.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth }));
      if (dim.sw > dim.cw + 3) warnings.push(`MOBILE_HORIZONTAL_OVERFLOW_${dim.sw - dim.cw}px | ${url}`);
      const menu = mobile.locator('[data-menu-button]').first();
      if (await menu.count()) {
        await menu.click();
        if ((await menu.getAttribute('aria-expanded')) !== 'true') errors.push(`MOBILE_MENU_OPEN_FAIL | ${url}`);
        await menu.click();
        if ((await menu.getAttribute('aria-expanded')) !== 'false') errors.push(`MOBILE_MENU_CLOSE_FAIL | ${url}`);
      }
    } catch (e) {
      errors.push(`MOBILE_BROWSER_FAIL | ${url} | ${e.message}`);
    }
  }

  await browser.close();

  for (const failure of failedInternalResources) errors.push(`FAILED_INTERNAL_RESOURCE | ${failure}`);
  fs.mkdirSync('audit-results', { recursive: true });
  fs.writeFileSync('audit-results/browser-pages.json', JSON.stringify(pages, null, 2));
  const report = [
    'SILWADI FULL-SITE BROWSER AUDIT',
    `SITEMAP_PAGES=${urls.length}`,
    `DESKTOP_PAGES_LOADED=${pages.length}`,
    `ERRORS=${errors.length}`,
    `WARNINGS=${warnings.length}`,
    '',
    '=== ERRORS ===',
    ...(errors.length ? errors : ['None']),
    '',
    '=== WARNINGS ===',
    ...(warnings.length ? warnings : ['None']),
  ].join('\n');
  fs.writeFileSync('audit-results/browser-report.txt', report);
  console.log(report);
})().catch(err => {
  console.error(err);
  process.exitCode = 1;
});
