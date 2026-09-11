import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "review/dental-faq-ai-v1.html"
JS = ROOT / "review/dental-faq-ai-v1.js"
CLINIC = ROOT / "ai/clinic-knowledge-v1.json"
DENTAL = ROOT / "ai/dental-guidance-v1.json"
WORKER = ROOT / "worker/silwadi-ai-worker.js"


class PrivateAiFaqReviewContract(unittest.TestCase):
    def test_review_page_is_private_and_contains_ai_ui(self):
        self.assertTrue(PAGE.exists(), "review/dental-faq-ai-v1.html must exist")
        text = PAGE.read_text(encoding="utf-8")
        self.assertIn('name="robots" content="noindex,nofollow', text)
        self.assertIn("Private review", text)
        self.assertIn("Not published", text)
        self.assertIn("Ask us a question!", text)
        self.assertIn('maxlength="500"', text)
        self.assertIn("Silwadi AI provides general dental information", text)
        self.assertIn('data-ai-answer', text)
        self.assertIn('data-ai-suggestions', text)
        self.assertIn('data-ai-contact-actions', text)
        self.assertIn('aria-live="polite"', text)
        for question in [
            "Which doctor treats children?",
            "What are your Al Raha opening hours?",
            "Why do my gums bleed?",
            "Do you offer root canal treatment?",
        ]:
            self.assertIn(question, text)

    def test_client_has_no_secret_and_has_safe_fallbacks(self):
        self.assertTrue(JS.exists(), "review/dental-faq-ai-v1.js must exist")
        text = JS.read_text(encoding="utf-8")
        lowered = text.lower()
        self.assertNotIn("sk-", lowered)
        self.assertNotIn("openai_api_key", lowered)
        self.assertNotIn("localstorage", lowered)
        self.assertNotIn("sessionstorage", lowered)
        self.assertIn("500", text)
        self.assertIn("AbortController", text)
        self.assertIn("reception", lowered)
        self.assertIn("textContent", text)
        self.assertIn("dir", lowered)

    def test_review_mode_works_before_secure_endpoint_is_connected(self):
        text = JS.read_text(encoding="utf-8")
        self.assertIn("../ai/clinic-knowledge-v1.json", text)
        self.assertIn("../ai/dental-guidance-v1.json", text)
        self.assertIn("runReviewFallback", text)
        self.assertIn("loadReviewData", text)
        self.assertIn("Dr. Kashmira Pawar Jayprakash", text)
        self.assertIn("Specialist Pediatric Dentist", text)
        self.assertIn("review-demo", text)
        self.assertIn("urgent", text.lower())
        self.assertIn("medication", text.lower())
        self.assertIn("insurance", text.lower())
        self.assertIn("root canal", text.lower())
        self.assertIn("نزيف", text)
        self.assertIn("الأطفال", text)

    def test_knowledge_sources_and_worker_exist(self):
        self.assertTrue(CLINIC.exists(), "ai/clinic-knowledge-v1.json must exist")
        self.assertTrue(DENTAL.exists(), "ai/dental-guidance-v1.json must exist")
        self.assertTrue(WORKER.exists(), "worker/silwadi-ai-worker.js must exist")
        clinic = json.loads(CLINIC.read_text(encoding="utf-8"))
        self.assertEqual(clinic["contact"]["email"], "info@silwadidentalcentres.ae")
        self.assertIn("bani-yas", clinic["branches"])
        self.assertIn("al-raha", clinic["branches"])

    def test_private_ai_page_is_not_linked_publicly(self):
        for rel in ["index.html", "services.html", "treatments.html", "doctors.html", "about.html", "contact.html"]:
            self.assertNotIn(
                "review/dental-faq-ai-v1.html",
                (ROOT / rel).read_text(encoding="utf-8"),
                f"{rel} must not expose the private AI review URL",
            )


if __name__ == "__main__":
    unittest.main()
