import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKER = ROOT / "worker/silwadi-ai-worker.js"
README = ROOT / "worker/README.md"


class AiWorkerContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = WORKER.read_text(encoding="utf-8")
        cls.lowered = cls.text.lower()

    def test_worker_exists_and_exposes_ask_route(self):
        self.assertTrue(WORKER.exists())
        self.assertIn('/ask', self.text)
        self.assertIn('POST', self.text)

    def test_request_size_and_origin_are_restricted(self):
        self.assertIn('question.length > 500', self.text)
        self.assertIn('ALLOWED_ORIGIN', self.text)
        self.assertIn('Access-Control-Allow-Origin', self.text)
        self.assertNotIn('Access-Control-Allow-Origin": "*"', self.text)

    def test_openai_request_is_private_and_low_cost(self):
        self.assertIn('OPENAI_API_KEY', self.text)
        self.assertIn('gpt-5.6-luna', self.text)
        self.assertIn('store: false', self.text)
        self.assertIn('reasoning: { effort: "none" }', self.text)
        self.assertIn('max_output_tokens: 220', self.text)
        self.assertNotIn('web_search', self.lowered)
        self.assertNotIn('sk-', self.lowered)

    def test_worker_has_required_safety_modes(self):
        for mode in ['clinic', 'general', 'fallback', 'urgent', 'unsafe']:
            self.assertIn(f'"{mode}"', self.text)
        self.assertIn('difficulty breathing', self.lowered)
        self.assertIn('difficulty swallowing', self.lowered)
        self.assertIn('uncontrolled bleeding', self.lowered)
        self.assertIn('antibiotic', self.lowered)
        self.assertIn('صعوبة', self.text)

    def test_worker_does_not_assume_first_output_item_contains_text(self):
        self.assertIn('output_text', self.text)
        self.assertIn('for (const item of', self.text)
        self.assertIn('for (const content of', self.text)

    def test_worker_has_timeout_and_safe_provider_fallback(self):
        self.assertIn('AbortController', self.text)
        self.assertIn('fallbackResponse', self.text)
        self.assertIn('CLINIC_KNOWLEDGE_URL', self.text)
        self.assertIn('DENTAL_GUIDANCE_URL', self.text)

    def test_deployment_readme_exists_and_warns_about_secret(self):
        self.assertTrue(README.exists())
        readme = README.read_text(encoding="utf-8")
        self.assertIn('OPENAI_API_KEY', readme)
        self.assertIn('secret', readme.lower())
        self.assertIn('Cloudflare', readme)
        self.assertNotIn('sk-', readme.lower())


if __name__ == '__main__':
    unittest.main()
