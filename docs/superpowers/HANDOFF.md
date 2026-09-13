# Silwadi Website Project Handoff

Last updated: 2026-09-13

## Current focus

Private review of the Silwadi Dental Centre FAQ AI assistant. Do not change the public FAQ page, public navigation, sitemap, or archived old website unless explicitly approved by the user.

## Repository

- Repository: `cuenext/silwadi-website`
- Branch: `main`
- Hosting: GitHub Pages
- Production site: `https://silwadi.ae`

## Approved AI design

- Design spec: `docs/superpowers/specs/2026-09-11-silwadi-ai-assistant-design.md`
- Implementation plan: `docs/superpowers/plans/2026-09-11-silwadi-ai-assistant-v1.md`
- Original implementation merged in PR #18 on 2026-09-11.

## Private review pages

- Static FAQ comparison page: `review/dental-faq-v1.html`
- AI FAQ review page: `review/dental-faq-ai-v1.html`
- Review URL: `https://silwadi.ae/review/dental-faq-ai-v1.html`
- Both review pages must remain `noindex,nofollow`, unlinked from public pages, and absent from the sitemap/navigation.
- The AI page retains the static FAQs so the FAQ content remains useful if the AI endpoint fails.

## AI frontend state

- Client: `review/dental-faq-ai-v1.js`
- The private page currently has `data-ai-endpoint=""` intentionally.
- With no endpoint configured, the page uses its deterministic private-review fallback so UI/safety flows can be reviewed before credentials are connected.
- The browser sends only `{ "question": "..." }` to the configured endpoint.
- No OpenAI secret belongs in HTML, browser JavaScript, GitHub, or this handoff file.

## Worker state

- Worker source: `worker/silwadi-ai-worker.js`
- Setup guide: `worker/README.md`
- Route: `POST /ask`
- Required secret: `OPENAI_API_KEY`
- Optional/config variables used by the current Worker:
  - `ALLOWED_ORIGIN=https://silwadi.ae`
  - `OPENAI_MODEL=gpt-5.6-luna`
  - `CLINIC_KNOWLEDGE_URL=https://silwadi.ae/ai/clinic-knowledge-v1.json`
  - `DENTAL_GUIDANCE_URL=https://silwadi.ae/ai/dental-guidance-v1.json`
- Current model choice was re-verified on 2026-09-13 against current OpenAI documentation: `gpt-5.6-luna` remains the intended fast/cost-sensitive model.
- Worker calls the OpenAI Responses API with `store: false`, no web-search tool, a 500-character input cap, low output cap, timeout, origin restriction, safe fallbacks, and private-review throttling.

## Tests / workflow

- Page regression: `tests/test_private_ai_faq_review.py`
- Knowledge regression: `tests/test_ai_knowledge_v1.py`
- Worker contract: `tests/test_ai_worker_contract.py`
- Workflow: `.github/workflows/private-ai-faq-review-test.yml`
- Workflow checks Python contracts plus JavaScript syntax.
- Public-site non-linking is included in the private AI page contract.

## Safety constraints that must not regress

- Same-language English/Arabic answers; Arabic RTL.
- Verified Silwadi clinic facts only. Unknown/live clinic facts go to reception.
- General dental education is allowed; diagnosis is not.
- No medication prescribing/dosing and no instructions to stop/change prescribed medication.
- No guarantees about outcomes, painlessness, prices, insurance, or appointment availability.
- No doctor superiority/best-doctor ranking.
- Red flags such as breathing/swallowing difficulty, uncontrolled bleeding, severe/rapid swelling, or major trauma require urgent-care guidance.
- No unrestricted web search.
- No V1 uploads, patient accounts, chat-history database, profile, or memory.
- Do not intentionally store patient questions/answers in a Silwadi database/log.
- Warn users not to enter personal or sensitive health information.

## Exact next step

The repository implementation is present. The real AI connection is intentionally the remaining step:

1. User creates/funds an OpenAI API project/account and creates a project API key. Never paste the key into chat.
2. User creates a Cloudflare Worker and pastes `worker/silwadi-ai-worker.js` into it.
3. User adds `OPENAI_API_KEY` as a Cloudflare **Secret** and adds the non-secret variables listed above.
4. User deploys the Worker and shares only the public `workers.dev` URL (safe to share), not the API key.
5. Agent follows TDD for the connection change, then sets the private page endpoint to `<workers.dev URL>/ask`.
6. Run/verify the private AI workflow and GitHub Pages deployment.
7. Test English, Arabic/RTL, unknown facts, medication, red flags, rate/timeout fallback, and static FAQ fallback on the private page.
8. Keep all public FAQ/navigation/sitemap changes out of scope until explicit approval.
