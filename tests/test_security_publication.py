import re
import unittest
from pathlib import Path
from tools.public_bundle import public_file

ROOT = Path(__file__).resolve().parents[1]

class SecurityPublicationTests(unittest.TestCase):
    def test_private_material_is_excluded(self):
        for name in ['.env', '.git/config', 'tests/example.py', 'docs/report.md', 'data/private.json', 'review/example.html', 'worker/index.js', 'node_modules/pkg/index.js', 'assets/backup.zip', 'assets/key.pem']:
            self.assertFalse(public_file(Path(name)), name)
        for name in ['index.html', 'ar/about.html', 'doctors/example.html', 'assets/doctors/photo.webp', 'booking-modal.js']:
            self.assertTrue(public_file(Path(name)), name)

    def test_no_repository_write_workflows(self):
        for file in (ROOT / '.github/workflows').glob('*.yml'):
            text = file.read_text()
            self.assertIsNone(re.search(r'contents:\s*write|write-all|pull_request_target', text), file.name)

    def test_booking_consent_is_transmitted(self):
        for name in ['app.js', 'booking-modal.js']:
            self.assertIn("consent: data.get('privacy-consent') === 'on'", (ROOT/name).read_text())
