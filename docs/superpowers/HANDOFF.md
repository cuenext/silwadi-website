# Silwadi Website Project Handoff

Last updated: 2026-09-14

## Current focus

The finished pediatric dentistry carousel is being published only to the existing private review page so the user can inspect it on `silwadi.ae`. Do not change the public pediatric/service page, public navigation, sitemap, archived old website, or any other public design/copy until the user explicitly approves the review.

The private FAQ AI assistant work remains preserved below and is still pending external Cloudflare/OpenAI setup.

## Repository

- Repository: `cuenext/silwadi-website`
- Production branch: `main`
- Pediatric development branch: `pediatric-carousel-review-0914`
- Hosting: GitHub Pages
- Production site: `https://silwadi.ae`
- Pediatric review URL: `https://silwadi.ae/review/pediatric-dentistry-v1.html`
- The review page may live on `main` for inspection, but it must remain `noindex`, unlinked from public navigation/pages, absent from the sitemap, and clearly marked `Private review` / `Not published`.

## Pediatric private review state

- Page: `review/pediatric-dentistry-v1.html`
- Robots: `noindex,nofollow,noarchive,nosnippet,noimageindex`.
- The clinic gallery appears before the pediatric hero.
- The rejected absolute-position / transform-stack carousel has been replaced with a horizontal scroll-snap carousel so slides do not overlap.
- Desktop center slide width is `min(82vw,1120px)`; mobile slide width is `86vw`, leaving controlled neighboring peeks while keeping the active photo dominant.
- Arrow buttons, keyboard navigation, click-to-center, native mobile swipe, centered-slide detection and image counter are retained.
- Reduced-motion behavior is included.
- The public pediatric/service page is intentionally unchanged pending user approval.

### Pediatric assets

The five optimized 1500×1000 WebPs are stored under:

`assets/review/pediatric-clinic/`

- `dscf2888.webp` — 127,912 bytes
- `dscf2892.webp` — 122,232 bytes
- `dscf2894.webp` — 86,766 bytes
- `dscf2896.webp` — 101,836 bytes
- `dscf2905.webp` — 115,114 bytes

All five pass RIFF/WEBP signature checks and the lightweight-image limit. They reuse the exact valid blobs from the user's successful manual binary upload; no connector re-encoding is used.

The user's manual upload also placed unreferenced copies/ZIP under root `assets/` on `main`. Leave those untouched unless the user explicitly requests cleanup.

### Pediatric TDD / verification baseline

- Initial layout RED commit: `07622b3213068a0ce082769377df8da7c2af9aa7`.
- Initial RED workflow: `34813425322`.
- Scroll-snap implementation: `ec1d9564de50288ea3068c5f8546b16ed5cf01de`.
- Valid optimized gallery blobs restored in review branch commit `b0787f63f96e5528d089e22c939a4ae56939edfc`.
- Dominant-center-slide RED test commit: `a548b64388f2e1d2478acfe8e2fe7f13624c9f01`.
- RED workflow `34817275259`: 107 tests, 106 passed; only the new proportion requirement failed as intended. Image-integrity checks already passed there.
- Final proportion implementation: `c21bfb308fdf4c927fbc4fc5bae3c137a200c608`.
- Final branch verification commit: `6b80dee9eaf262a56406c67e0d4871d7184b8544`.
- Final branch workflow: `34817583900`.
- Baseline result: **107 tests run, 107 passed, 0 failures**.
- Before claiming the review is live, verify the exact `main` publication commit has both successful regression CI and successful GitHub Pages deployment.

### Visual-review note

Automated browser rendering from the local container was blocked by the environment's browser administrator policy, so do not claim a live visual browser check from that session. Structural/layout behavior and asset integrity are regression-tested; the user must visually approve the rendered review URL before equivalent public-page implementation.

## Pediatric exact next step

1. User reviews `https://silwadi.ae/review/pediatric-dentistry-v1.html` on desktop and phone.
2. If the user requests adjustments, change the private review only and preserve the green regression baseline.
3. Only after explicit approval should the equivalent carousel/design be reconciled with current `main` and implemented on the public pediatric/service page.

## Approved AI design

- Design spec: `docs/superpowers/specs/2026-09-11-silwadi-ai-assistant-design.md`
- Implementation plan: `docs/superpowers/plans/2026-09-11-silwadi-ai-assistant-v1.md`
- Original implementation merged in PR #18 on 2026-09-11.

## Private AI review pages

- Static FAQ comparison page: `review/dental-faq-v1.html`
- AI FAQ review page: `review/dental-faq-ai-v1.html`
- Review URL: `https://silwadi.ae/review/dental-faq-ai-v1.html`
- Both review pages must remain `noindex,nofollow`, unlinked from public pages, and absent from the sitemap/navigation.
- The AI page retains the static FAQs so FAQ content remains available if the AI endpoint fails.

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
- Optional/config variables:
  - `ALLOWED_ORIGIN=https://silwadi.ae`
  - `OPENAI_MODEL=gpt-5.6-luna`
  - `CLINIC_KNOWLEDGE_URL=https://silwadi.ae/ai/clinic-knowledge-v1.json`
  - `DENTAL_GUIDANCE_URL=https://silwadi.ae/ai/dental-guidance-v1.json`
- Worker calls the OpenAI Responses API with `store: false`, no web-search tool, a 500-character input cap, low output cap, timeout, origin restriction, safe fallbacks, and private-review throttling.

## AI tests / workflow

- Page regression: `tests/test_private_ai_faq_review.py`
- Knowledge regression: `tests/test_ai_knowledge_v1.py`
- Worker contract: `tests/test_ai_worker_contract.py`
- Workflow: `.github/workflows/private-ai-faq-review-test.yml`
- Public-site non-linking is included in the private AI page contract.
- Root-cause fix commit `02cc93109d6fb5adc9f8c0c31390bf2b1114ae3b` changed only the private AI clinic knowledge entry to `Dr. Lana Almasoud`.
- TDD GREEN was verified on workflow run `34745799513` for the private AI page, knowledge and Worker checks.

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

## AI exact next step after pediatric work

1. User creates/funds an OpenAI API project/account and creates a project API key. Never paste the key into chat.
2. User creates a Cloudflare Worker and pastes `worker/silwadi-ai-worker.js` into it.
3. User adds `OPENAI_API_KEY` as a Cloudflare Secret and the non-secret variables above.
4. User deploys the Worker and shares only the public `workers.dev` URL, not the API key.
5. Agent follows TDD for the connection change, then sets the private page endpoint to `<workers.dev URL>/ask`.
6. Run/verify the private AI workflow and GitHub Pages deployment.
7. Test English, Arabic/RTL, unknown facts, medication, red flags, rate/timeout fallback, and static FAQ fallback on the private page.
8. Keep all public FAQ/navigation/sitemap changes out of scope until explicit approval.
