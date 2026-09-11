(() => {
  'use strict';

  const root = document.querySelector('[data-ai-assistant]');
  if (!root) return;

  const form = root.querySelector('[data-ai-form]');
  const input = root.querySelector('[data-ai-input]');
  const submit = root.querySelector('[data-ai-submit]');
  const count = root.querySelector('[data-ai-count]');
  const status = root.querySelector('[data-ai-status]');
  const answer = root.querySelector('[data-ai-answer]');
  const contacts = root.querySelector('[data-ai-contact-actions]');
  const suggestions = root.querySelectorAll('[data-ai-suggestion]');

  const MAX_QUESTION_LENGTH = 500;
  const REQUEST_TIMEOUT_MS = 12000;
  let activeController = null;

  const containsArabic = (value) => /[\u0600-\u06FF]/.test(value || '');

  function languageFor(value) {
    return containsArabic(value) ? 'ar' : 'en';
  }

  function setDirection(language) {
    const direction = language === 'ar' ? 'rtl' : 'ltr';
    answer.dir = direction;
    answer.lang = language;
    status.dir = direction;
    status.lang = language;
  }

  function setBusy(isBusy, language) {
    submit.disabled = isBusy;
    input.disabled = isBusy;
    status.dataset.busy = isBusy ? 'true' : 'false';
    if (isBusy) {
      status.textContent = language === 'ar'
        ? 'جارٍ التحقق من معلومات سلوادي…'
        : 'Checking Silwadi information…';
    }
  }

  function clearResult() {
    answer.hidden = true;
    answer.textContent = '';
    contacts.hidden = true;
    status.textContent = '';
    status.dataset.busy = 'false';
  }

  function showAnswer(text, language, mode = 'general') {
    setDirection(language);
    answer.hidden = false;
    answer.textContent = String(text || '').slice(0, 1600);
    status.textContent = '';
    status.dataset.busy = 'false';
    contacts.hidden = !['fallback', 'urgent', 'unsafe'].includes(mode);
  }

  function showFallback(language, reason = 'unknown') {
    const connectionMissing = reason === 'endpoint';
    setDirection(language);
    answer.hidden = false;
    answer.textContent = language === 'ar'
      ? (connectionMissing
        ? 'نسخة المراجعة جاهزة، لكن اتصال الذكاء الاصطناعي لم يتم تفعيله بعد. يمكن لفريق الاستقبال مساعدتك الآن.'
        : 'لا أملك معلومات موثقة كافية للإجابة بدقة. يمكن لفريق الاستقبال تأكيد ذلك لك.')
      : (connectionMissing
        ? 'The review interface is ready, but the AI test connection has not been activated yet. Reception can help you in the meantime.'
        : "I don’t have enough verified information to answer that accurately. Reception can confirm this for you.");
    status.textContent = '';
    status.dataset.busy = 'false';
    contacts.hidden = false;
  }

  function updateCount() {
    const length = input.value.length;
    count.textContent = `${length} / ${MAX_QUESTION_LENGTH}`;
  }

  async function askQuestion(question) {
    const trimmed = String(question || '').trim();
    const language = languageFor(trimmed);
    setDirection(language);

    if (!trimmed) {
      clearResult();
      status.textContent = language === 'ar' ? 'اكتب سؤالك أولاً.' : 'Please type your question first.';
      input.focus();
      return;
    }

    if (trimmed.length > MAX_QUESTION_LENGTH) {
      clearResult();
      status.textContent = language === 'ar'
        ? 'يرجى اختصار سؤالك إلى 500 حرف أو أقل.'
        : 'Please keep your question to 500 characters or fewer.';
      return;
    }

    const endpoint = String(root.dataset.aiEndpoint || '').trim();
    if (!endpoint) {
      clearResult();
      showFallback(language, 'endpoint');
      return;
    }

    if (activeController) activeController.abort();
    activeController = new AbortController();
    const controller = activeController;
    const timeout = window.setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

    clearResult();
    setBusy(true, language);

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: trimmed }),
        signal: controller.signal,
        credentials: 'omit',
        cache: 'no-store',
        referrerPolicy: 'strict-origin-when-cross-origin'
      });

      if (!response.ok) throw new Error(`Silwadi AI request failed: ${response.status}`);

      const payload = await response.json();
      const mode = ['clinic', 'general', 'fallback', 'urgent', 'unsafe'].includes(payload.mode)
        ? payload.mode
        : 'fallback';
      const responseLanguage = payload.language === 'ar' ? 'ar' : (payload.language === 'en' ? 'en' : language);
      const responseText = typeof payload.answer === 'string' ? payload.answer.trim() : '';

      if (!responseText) {
        showFallback(responseLanguage);
        return;
      }

      showAnswer(responseText, responseLanguage, mode);
    } catch (error) {
      if (controller.signal.aborted) {
        status.textContent = language === 'ar'
          ? 'استغرق الرد وقتاً أطول من المتوقع.'
          : 'The answer took longer than expected.';
      }
      showFallback(language);
    } finally {
      window.clearTimeout(timeout);
      if (activeController === controller) activeController = null;
      submit.disabled = false;
      input.disabled = false;
      status.dataset.busy = 'false';
    }
  }

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    askQuestion(input.value);
  });

  suggestions.forEach((button) => {
    button.addEventListener('click', () => {
      const question = button.dataset.aiSuggestion || button.textContent || '';
      input.value = question.slice(0, MAX_QUESTION_LENGTH);
      updateCount();
      askQuestion(input.value);
    });
  });

  input.addEventListener('input', updateCount);
  updateCount();
})();
