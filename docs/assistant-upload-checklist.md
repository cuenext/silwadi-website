# Preserve the FAQ and assistant when publishing

1. Start from the current merged `main` branch. Retain the `ai/` frontend files and the FAQ links and three assistant script tags in every patient page, including Arabic pages.
2. Build the upload folder with `python tools/public_bundle.py <empty-folder-outside-repository>`. The builder stops if the produced folder lacks a required AI file, assistant embed, standalone page setup, or FAQ navigation/footer link. It excludes private AI knowledge, configuration, backend code, and credentials.
3. Before uploading that exact folder, run both checks:

   ```text
   python tools/public_bundle.py <upload-folder> --validate-only
   node tests/assistant-integration.test.mjs <upload-folder>
   ```

4. Upload only the validated public bundle to the Tasjeel website folder. Keep the private booking/AI backend configuration outside the public upload. Back up the live files before replacing them.
5. After uploading, check Home, About, Doctors, the updated page, and `/ai/` in English and Arabic. Confirm the FAQ link, open/close the floating assistant, and send a general clinic question. Inspect the browser console for errors. Do not submit a booking or patient details as a smoke test.

GitHub checks validate both repository source and the built artifact. Manual uploads that bypass this workflow cannot be protected by CI; always run the same pre-upload checks locally. `node tools/restore-assistant.mjs` can repair omitted integration tags in patient source pages before rebuilding.
