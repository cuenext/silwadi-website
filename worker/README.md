# Silwadi AI Worker — Private Review Setup

This Worker is the secure server-side bridge between the private Silwadi AI FAQ page and the OpenAI Responses API.

Do **not** put the OpenAI API key in the website HTML, JavaScript, GitHub repository, or a public URL. `OPENAI_API_KEY` must be added as an encrypted Cloudflare Worker secret.

## Before you start

You need:

1. A Cloudflare account.
2. An OpenAI API account with billing/credits enabled.
3. An OpenAI API key created for this website integration.
4. The private AI page and the two `/ai/*.json` knowledge files deployed at `https://silwadi.ae`.

The public website can remain hosted on GitHub Pages. Cloudflare is only being used for the secure AI endpoint.

## Create the Worker

Cloudflare's dashboard wording can change slightly, but the flow is normally:

1. Sign in to Cloudflare.
2. Open **Workers & Pages**.
3. Choose **Create** / **Create application**.
4. Choose **Worker**.
5. Give it a clear name such as `silwadi-ai-review`.
6. Deploy the starter Worker once.
7. Open **Edit code** for that Worker.
8. Replace the starter code with the contents of `worker/silwadi-ai-worker.js` from this repository.
9. Save/deploy.

At this point the Worker still cannot call the AI until the encrypted secret is added.

## Add the OpenAI key safely

1. Open the `silwadi-ai-review` Worker in Cloudflare.
2. Open **Settings**.
3. Find **Variables and Secrets** (sometimes shown as **Environment Variables**).
4. Choose **Add**.
5. Name: `OPENAI_API_KEY`.
6. Choose the **Secret / encrypted** type, not a normal public text variable.
7. Paste the API key into Cloudflare there.
8. Save and redeploy if Cloudflare asks you to.

Never send the API key in chat. Never commit it to GitHub. If a key is accidentally exposed, revoke it in the OpenAI dashboard and create a new one.

## Add review variables

Under the same Worker variables/settings area, add these normal variables:

- `ALLOWED_ORIGIN` = `https://silwadi.ae`
- `OPENAI_MODEL` = `gpt-5.6-luna`
- `CLINIC_KNOWLEDGE_URL` = `https://silwadi.ae/ai/clinic-knowledge-v1.json`
- `DENTAL_GUIDANCE_URL` = `https://silwadi.ae/ai/dental-guidance-v1.json`

These values are not secrets. The clinic/guidance JSON files contain public approved website information only.

## Get the public Worker URL

After deployment Cloudflare will show a URL similar to:

`https://silwadi-ai-review.<your-account-subdomain>.workers.dev`

The endpoint used by the private page is that URL plus `/ask`, for example:

`https://silwadi-ai-review.<your-account-subdomain>.workers.dev/ask`

Share only this public Worker URL when connecting the review page. Do not share the OpenAI key.

## Private review safety notes

- The Worker accepts browser requests only from the configured `ALLOWED_ORIGIN`.
- Questions longer than 500 characters are rejected.
- Obvious urgent red flags and medication requests are intercepted before the AI call.
- The AI request sets `store: false`.
- No unrestricted AI web-search tool is enabled.
- The Worker does not intentionally write patient questions to application logs.
- The source includes a lightweight per-isolate throttle for private testing. Before a wider public launch, also configure a Cloudflare rate-limiting rule because Worker isolates do not share the in-memory throttle.
- No chat-history database or patient-profile system is used.

## Public launch is a separate step

This setup is for the private/noindex review page. Do not add the AI page to navigation, sitemap, the public FAQ page, or the old-domain `faq.php` redirect until the review experience has been explicitly approved and the final privacy wording has been reviewed against the actual production configuration.
