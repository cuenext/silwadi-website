from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = (ROOT / 'review' / 'dental-faq-ai-v1.html').read_text(encoding='utf-8')
CHAT = (ROOT / 'review' / 'dental-faq-ai-chat.js').read_text(encoding='utf-8')

class AiReviewRedesignTests(unittest.TestCase):
    def test_ai_composer_precedes_conversation_thread(self):
        self.assertIn('data-ai-composer', PAGE)
        self.assertIn('data-ai-thread', PAGE)
        self.assertLess(PAGE.index('data-ai-composer'), PAGE.index('data-ai-thread'))

    def test_old_report_style_hero_and_jump_grid_are_removed(self):
        self.assertNotIn('class="fq-hero"', PAGE)
        self.assertNotIn('class="fq-jump"', PAGE)

    def test_suggestions_are_reduced_to_three_compact_prompts(self):
        self.assertEqual(PAGE.count('data-ai-suggestion='), 3)

    def test_faq_uses_category_switcher_and_single_compact_panel(self):
        for category in ('appointments', 'treatments', 'children', 'clinics'):
            self.assertIn(f'data-faq-filter="{category}"', PAGE)
        self.assertIn('data-faq-panel', PAGE)
        self.assertNotIn('faq-review-group', PAGE)

    def test_chat_enhancer_keeps_session_history(self):
        self.assertIn('data-ai-chat-enhancer', PAGE)
        self.assertIn('appendMessage', CHAT)
        self.assertIn('data-ai-thread', PAGE)

    def test_review_stays_private(self):
        self.assertRegex(PAGE, r'<meta\s+name="robots"\s+content="[^"]*noindex')

if __name__ == '__main__':
    unittest.main()
