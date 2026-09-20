const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { JSDOM } = require('jsdom');

const root = path.resolve(__dirname, '..');
const page = fs.readFileSync(path.join(root, 'review/dental-faq-ai-v1.html'), 'utf8');
const assistantScript = fs.readFileSync(path.join(root, 'review/dental-faq-ai-v1.js'), 'utf8');
const chatScript = fs.readFileSync(path.join(root, 'review/dental-faq-ai-chat.js'), 'utf8');

function createDom() {
  const dom = new JSDOM(page, {
    runScripts: 'outside-only',
    url: 'https://silwadi.ae/review/dental-faq-ai-v1.html'
  });
  dom.window.matchMedia = () => ({ matches: true });
  dom.window.HTMLElement.prototype.scrollIntoView = () => {};
  return dom;
}

test('chat card keeps the conversation above its bottom composer', (t) => {
  const dom = createDom();
  t.after(() => dom.window.close());
  const document = dom.window.document;
  const assistant = document.querySelector('[data-ai-assistant]');
  const header = assistant.querySelector('[data-ai-assistant-header]');
  const thread = assistant.querySelector('[data-ai-thread]');
  const composer = assistant.querySelector('[data-ai-composer]');

  assert.ok(header, 'the assistant needs a clear identity header');
  assert.ok(header.querySelector('img[alt=""]'), 'the assistant identity should use the Silwadi mark');
  assert.ok(thread.compareDocumentPosition(composer) & dom.window.Node.DOCUMENT_POSITION_FOLLOWING);
});

test('starting a conversation hides starter prompts and renders a branded assistant identity', (t) => {
  const dom = createDom();
  t.after(() => dom.window.close());
  dom.window.eval(chatScript);
  const document = dom.window.document;
  const suggestion = document.querySelector('[data-ai-suggestion]');

  suggestion.click();

  const assistant = document.querySelector('[data-ai-assistant]');
  assert.equal(assistant.dataset.aiStarted, 'true');
  assert.ok(document.querySelector('.ai-message--assistant .ai-message__avatar img[alt=""]'));
  assert.match(document.querySelector('.ai-message--assistant').textContent, /Silwadi Assistant/);
});

test('only the newest overlapping request may update the visible answer', async (t) => {
  const dom = createDom();
  t.after(() => dom.window.close());
  const pending = [];
  dom.window.fetch = (_url, options) => new Promise((resolve) => {
    pending.push({
      question: JSON.parse(options.body).question,
      resolve: (answer) => resolve({
        ok: true,
        json: async () => ({ answer, language: 'en', mode: 'general' })
      })
    });
  });

  const assistant = dom.window.document.querySelector('[data-ai-assistant]');
  assistant.dataset.aiEndpoint = 'https://example.test/ask';
  dom.window.eval(assistantScript);

  const form = assistant.querySelector('[data-ai-form]');
  const input = assistant.querySelector('[data-ai-input]');
  input.value = 'First question';
  form.dispatchEvent(new dom.window.Event('submit', { bubbles: true, cancelable: true }));
  input.value = 'Second question';
  form.dispatchEvent(new dom.window.Event('submit', { bubbles: true, cancelable: true }));

  assert.equal(pending.length, 2);
  pending[1].resolve('Newest answer');
  await new Promise((resolve) => dom.window.setTimeout(resolve, 0));
  pending[0].resolve('Stale answer');
  await new Promise((resolve) => dom.window.setTimeout(resolve, 0));

  assert.equal(assistant.querySelector('[data-ai-answer]').textContent, 'Newest answer');
});

test('fallback help is presented as one reception card instead of four repeated buttons', async (t) => {
  const dom = createDom();
  t.after(() => dom.window.close());
  dom.window.eval(chatScript);
  const document = dom.window.document;
  const suggestion = document.querySelector('[data-ai-suggestion]');
  suggestion.click();

  const answer = document.querySelector('[data-ai-answer]');
  const contacts = document.querySelector('[data-ai-contact-actions]');
  contacts.hidden = false;
  answer.textContent = 'Reception can confirm this for you.';
  answer.hidden = false;

  await new Promise((resolve) => dom.window.setTimeout(resolve, 0));
  const card = document.querySelector('.ai-escalation');
  assert.ok(card);
  assert.match(card.textContent, /Contact reception/i);
  assert.ok(card.querySelectorAll('a').length <= 2);
});
