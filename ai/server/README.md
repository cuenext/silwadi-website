# Production assistant accreditation facts

The live Silwadi Assistant uses a separate Node app on Tasjeel. Its current application directory is `/home/silwadia/silwadi-ai-app-20261015`; the repository's legacy Cloudflare worker and review pages are separate implementations.

`accreditations.mjs` provides verified English and Arabic answers based on the published About-page cards. It does not infer branch coverage for the JAWDA card, which has no branch label.

Run the behavior checks with:

```text
node --test tests/assistant_accreditations.test.mjs
```

For the current production app, copy this module to `lib/accreditations.mjs` and apply `tools/server/assistant-accreditations.patch` from the application root. The patch adds the route after existing safety checks and before service/doctor matching and model calls. Keep the original handler for rollback, reload the app, and verify the answer in the live widget.

On this LiteSpeed host, the existing `lsnode` worker remained alive after both the restart marker and cPanel restart controls. Replacing that worker loaded the updated modules. Verify the process owner and exact working directory before terminating only the assistant worker; do not assume a successful panel action means new code is running.

These server files are intentionally excluded from the static public website bundle.
