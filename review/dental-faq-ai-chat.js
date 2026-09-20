(() => {
  const root = document.querySelector('[data-ai-assistant]');
  if (!root) return;

  const form = root.querySelector('[data-ai-form]');
  const input = root.querySelector('[data-ai-input]');
  const count = root.querySelector('[data-ai-count]');
  const answerSource = root.querySelector('[data-ai-answer]');
  const statusSource = root.querySelector('[data-ai-status]');
  const contactsSource = root.querySelector('[data-ai-contact-actions]');
  const thread = root.querySelector('[data-ai-thread]');
  const empty = root.querySelector('[data-ai-empty]');
  const suggestions = root.querySelectorAll('[data-ai-suggestion]');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let pending = null;
  let lastRenderedAnswer = '';

  const clearEmpty = () => {
    if (empty && empty.isConnected) empty.remove();
  };

  const scrollToLatest = () => {
    const scroll = () => {
      if (typeof thread.scrollTo === 'function') {
        thread.scrollTo({
          top: thread.scrollHeight,
          behavior: reduceMotion ? 'auto' : 'smooth'
        });
      } else {
        thread.scrollTop = thread.scrollHeight;
      }
    };
    if (typeof window.requestAnimationFrame === 'function') window.requestAnimationFrame(scroll);
    else scroll();
  };

  function createAssistantAvatar() {
    const avatar = document.createElement('span');
    avatar.className = 'ai-message__avatar';
    avatar.setAttribute('aria-hidden', 'true');
    const mark = document.createElement('img');
    mark.src = '../favicon.svg';
    mark.alt = '';
    avatar.appendChild(mark);
    return avatar;
  }

  function appendMessage(role, text, language = 'en') {
    clearEmpty();
    const row = document.createElement('div');
    row.className = `ai-message ai-message--${role}`;
    row.dir = language === 'ar' ? 'rtl' : 'ltr';

    if (role === 'assistant') row.appendChild(createAssistantAvatar());

    const content = document.createElement('div');
    content.className = 'ai-message__content';
    if (role === 'assistant') {
      const name = document.createElement('span');
      name.className = 'ai-message__name';
      name.textContent = language === 'ar' ? 'مساعد سلوادي' : 'Silwadi Assistant';
      content.appendChild(name);
    }

    const bubble = document.createElement('div');
    bubble.className = 'ai-message__bubble';
    bubble.textContent = text;
    content.appendChild(bubble);
    row.appendChild(content);
    thread.appendChild(row);
    scrollToLatest();
    return row;
  }

  function appendTyping(language = 'en') {
    clearEmpty();
    const row = document.createElement('div');
    row.className = 'ai-message ai-message--assistant';
    row.dir = language === 'ar' ? 'rtl' : 'ltr';
    row.appendChild(createAssistantAvatar());

    const content = document.createElement('div');
    content.className = 'ai-message__content';
    const name = document.createElement('span');
    name.className = 'ai-message__name';
    name.textContent = language === 'ar' ? 'مساعد سلوادي' : 'Silwadi Assistant';
    const bubble = document.createElement('div');
    bubble.className = 'ai-message__bubble';
    bubble.innerHTML = '<span class="ai-typing" aria-label="Silwadi is responding"><i></i><i></i><i></i></span>';
    content.append(name, bubble);
    row.appendChild(content);
    thread.appendChild(row);
    pending = row;
    scrollToLatest();
    return row;
  }

  function addContactActions(row) {
    if (!row || !contactsSource || contactsSource.hidden) return;
    const links = [...contactsSource.querySelectorAll('a')].slice(0, 2);
    if (!links.length) return;

    const card = document.createElement('div');
    card.className = 'ai-escalation';
    const copy = document.createElement('div');
    copy.className = 'ai-escalation__copy';
    const title = document.createElement('strong');
    title.textContent = 'Contact reception';
    const description = document.createElement('span');
    description.textContent = 'For availability, insurance, prices or anything requiring confirmation.';
    copy.append(title, description);

    const actions = document.createElement('div');
    actions.className = 'ai-escalation__actions';
    links.forEach((link) => actions.appendChild(link.cloneNode(true)));
    card.append(copy, actions);
    row.after(card);
    scrollToLatest();
  }

  function captureQuestion(question) {
    const value = String(question || '').trim();
    if (!value) return;
    const language = /[\u0600-\u06FF]/.test(value) ? 'ar' : 'en';
    root.dataset.aiStarted = 'true';
    lastRenderedAnswer = '';
    appendMessage('user', value, language);
    if (pending) pending.remove();
    appendTyping(language);
    input.value = '';
    input.style.height = 'auto';
    if (count) count.textContent = '0 / 500';
  }

  form.addEventListener('submit', () => captureQuestion(input.value));
  suggestions.forEach((button) => {
    button.addEventListener('click', () => {
      captureQuestion(button.dataset.aiSuggestion || button.textContent || '');
    });
  });

  const flushAnswer = () => {
    if (!answerSource || answerSource.hidden) return;
    const text = String(answerSource.textContent || '').trim();
    if (!text || text === lastRenderedAnswer) return;
    lastRenderedAnswer = text;
    const language = answerSource.lang === 'ar' || answerSource.dir === 'rtl' ? 'ar' : 'en';
    if (pending) {
      pending.remove();
      pending = null;
    }
    const row = appendMessage('assistant', text, language);
    addContactActions(row);
    input.focus({ preventScroll: true });
  };

  const observer = new MutationObserver(() => queueMicrotask(flushAnswer));
  observer.observe(answerSource, {
    childList: true,
    subtree: true,
    characterData: true,
    attributes: true,
    attributeFilter: ['hidden', 'lang', 'dir', 'data-response-id']
  });

  const statusObserver = new MutationObserver(() => {
    if (!pending || !statusSource) return;
    if (statusSource.dataset.busy === 'true' || !answerSource.hidden) return;
    const text = String(statusSource.textContent || '').trim();
    if (!text) return;
    const bubble = pending.querySelector('.ai-message__bubble');
    if (bubble) bubble.textContent = text;
    pending = null;
    scrollToLatest();
  });
  statusObserver.observe(statusSource, {
    childList: true,
    subtree: true,
    characterData: true,
    attributes: true,
    attributeFilter: ['data-busy']
  });

  const resizeInput = () => {
    input.style.height = 'auto';
    input.style.height = `${Math.min(input.scrollHeight, 130)}px`;
    if (count) count.style.display = input.value.length >= 450 ? 'block' : 'none';
  };
  input.addEventListener('input', resizeInput);
  resizeInput();

  const filters = document.querySelectorAll('[data-faq-filter]');
  const panels = document.querySelectorAll('[data-faq-panel]');
  filters.forEach((button) => {
    button.addEventListener('click', () => {
      const target = button.dataset.faqFilter;
      filters.forEach((item) => item.setAttribute('aria-selected', item === button ? 'true' : 'false'));
      panels.forEach((panel) => {
        panel.hidden = panel.dataset.faqPanel !== target;
        panel.querySelectorAll('details[open]').forEach((detail) => detail.removeAttribute('open'));
      });
    });
  });
  panels.forEach((panel) => {
    panel.querySelectorAll('details').forEach((detail) => {
      detail.addEventListener('toggle', () => {
        if (!detail.open) return;
        panel.querySelectorAll('details[open]').forEach((other) => {
          if (other !== detail) other.removeAttribute('open');
        });
      });
    });
  });
})();
