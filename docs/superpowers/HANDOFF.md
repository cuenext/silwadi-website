# Silwadi Website Project Handoff

Last updated: 2026-09-14

## Current focus

Private review of the pediatric dentistry page, specifically replacing the broken clinic-photo carousel with a clean centered slideshow. Do not change the public pediatric/service page, public navigation, sitemap, archived old website, or any other public design/copy without explicit user approval.

The private FAQ AI assistant work remains preserved below and is still pending external Cloudflare/OpenAI setup.

## Repository

- Repository: `cuenext/silwadi-website`
- Production branch: `main`
- Current pediatric review branch: `pediatric-carousel-review-0914`
- Hosting: GitHub Pages
- Production site: `https://silwadi.ae`
- Pediatric carousel branch was created from main commit `a76b852be4c488706a36131259b8d0b16337d2b0`.
- Do not merge the pediatric branch to `main` until the user visually approves the private review and the full regression suite is green.

## Pediatric private review state

- Page: `review/pediatric-dentistry-v1.html`
- The page remains `noindex,nofollow,noarchive,nosnippet,noimageindex`, marked `Private review` / `Not published`, unlinked from the public site and absent from the sitemap.
- The clinic-gallery section remains before the pediatric hero, as previously approved.
- The old gallery used absolutely positioned slides and large left/right transforms. This produced the crowded/overlapping appearance the user rejected.
- New carousel implementation uses a horizontal scroll-snap viewport/track instead of stacked absolute cards.
- The center slide is the active slide; neighboring slides are natural side previews rather than cards layered over the center image.
- Arrow buttons, keyboard navigation, click-to-center and native mobile swipe are retained.
- Manual pointer-capture swipe code was removed so mobile uses native horizontal scrolling/snap behavior.
- Reduced-motion behavior is included.
- Public pages have not been changed by this branch.

### Pediatric TDD status

- RED test commit: `07622b3213068a0ce082769377df8da7c2af9aa7` (`test: define pediatric carousel layout contract`).
- RED workflow run: `34813425322`, completed with failure before implementation as expected.
- Carousel implementation commit: `ec1d9564de50288ea3068c5f8546b16ed5cf01de` (`fix: rebuild pediatric clinic carousel layout`).
- Implementation workflow run: `34813693467`.
- In run `34813693467`, the new carousel layout/navigation tests passed, as did the existing private pediatric review tests and the rest of the Google-authority/private regression suite.
- The only remaining failure is `test_gallery_uses_selected_images`, because the five WebP files already present in GitHub are corrupted/truncated.
- GitHub currently reports these corrupted files at exactly 14,998–14,999 bytes each. The first file begins with invalid bytes instead of the required `RIFF....WEBP` signature.
- This confirms the previous connector binary-upload limitation rather than a carousel-code problem.

### Correct pediatric assets prepared locally

Correct optimized files are derived from the user's original high-resolution ZIP and retain valid WebP signatures:

- `dscf2888.webp` — 127,912 bytes
- `dscf2892.webp` — 122,232 bytes
- `dscf2894.webp` — 86,766 bytes
- `dscf2896.webp` — 101,836 bytes
- `dscf2905.webp` — 115,114 bytes

They are 1500×1000 WebP gallery images with metadata stripped. The five-image set is about 0.53 MB total versus about 12 MB for the selected originals.

Required repository path:
`assets/review/pediatric-clinic/`

Do not accept or merge a supposed image fix unless all five repo files are valid RIFF/WebP files and the full workflow turns green.

## Pediatric exact next step

1. Replace the five corrupted repo WebPs on branch `pediatric-carousel-review-0914` with the five prepared optimized files using a binary-safe upload route. The current ChatGPT GitHub connector must not be used for these binaries because it truncates them near 15 KB.
2. Re-run the Google authority/private regression workflow and require 0 failures.
3. Visually verify the carousel on desktop and mobile: one dominant centered image, controlled neighboring previews, no overlap/collision, smooth arrows, keyboard behavior and native swipe.
4. Give the user the private review result for approval.
5. Only after explicit approval should any equivalent change be merged/published.

## Approved AI design

- Design spec: `docs/superpowers/specs/2026-09-11-silwadi-ai-assistant-design.md`
- Implementation plan: `docs/superpowers/plans/2026-09-11-silwadi-ai-assistant-v1.md`
- Original implementation merged in PR #18 on 2026-09-11.

## Private AI review pages

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

## AI tests / workflow

- Page regression: `tests/test_private_ai_faq_review.py`
- Knowledge regression: `tests/test_ai_knowledge_v1.py`
- Worker contract: `tests/test_ai_worker_contract.py`
- Workflow: `.github/workflows/private-ai-faq-review-test.yml`
- Public-site non-linking is included in the private AI page contract.
- Root-cause fix commit `02cc93109d6fb5adc9f8c0c31390bf2b1114ae3b` changed only the private AI clinic knowledge entry to `Dr. Lana Almasoud`.
- TDD GREEN was verified on workflow run `34745799513` for the private AI page, knowledge and worker checks.

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
3. User adds `OPENAI_API_KEY` as a Cloudflare **Secret** and adds the non-secret variables listed above.
4. User deploys the Worker and shares only the public `workers.dev` URL, not the API key.
5. Agent follows TDD for the connection change, then sets the private page endpoint to `<workers.dev URL>/ask`.
6. Run/verify the private AI workflow and GitHub Pages deployment.
7. Test English, Arabic/RTL, unknown facts, medication, red flags, rate/timeout fallback, and static FAQ fallback on the private page.
8. Keep all public FAQ/navigation/sitemap changes out of scope until explicit approval.
