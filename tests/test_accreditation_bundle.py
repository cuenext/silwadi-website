from pathlib import Path
import re
import shutil
import tempfile
import unittest

from tools.public_bundle import validate_accreditations_bundle


ROOT = Path(__file__).resolve().parents[1]
PAGES = ('index.html', 'ar/index.html', 'about.html', 'ar/about.html')
ASSETS = (
    'accreditations.css', 'accreditations.js',
    'assets/jawda-tasneef-mark.png', 'assets/adhics-aamen-doh-mark.webp',
    'assets/uks-certification-logo.jpg',
)


class AccreditationBundleTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.upload = Path(self.temporary.name)
        for name in PAGES + ASSETS:
            destination = self.upload / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, destination)

    def change(self, page, before, after):
        target = self.upload / page
        html = target.read_text(encoding='utf-8')
        self.assertIn(before, html)
        target.write_text(html.replace(before, after), encoding='utf-8')

    def test_accepts_reviewed_scorecards_in_all_four_uploaded_pages(self):
        self.assertEqual(4, validate_accreditations_bundle(self.upload))

    def test_rejects_upload_after_any_accreditation_section_is_removed(self):
        for page in PAGES:
            with self.subTest(page=page):
                target = self.upload / page
                original = target.read_text(encoding='utf-8')
                target.write_text(re.sub(r'<section[^>]*class="[^"]*about-accreditations[^\"]*"[^>]*>[\s\S]*?</section>', '', original), encoding='utf-8')
                with self.assertRaisesRegex(ValueError, re.escape(page)):
                    validate_accreditations_bundle(self.upload)
                target.write_text(original, encoding='utf-8')

    def test_rejects_missing_upload_dependencies(self):
        for name in ASSETS:
            with self.subTest(asset=name):
                target = self.upload / name
                original = target.read_bytes()
                target.unlink()
                with self.assertRaisesRegex(ValueError, re.escape(name)):
                    validate_accreditations_bundle(self.upload)
                target.write_bytes(original)

    def test_rejects_homepage_with_only_commented_carousel_imports(self):
        for page in PAGES[:2]:
            for tag in ('<link rel="stylesheet" href="/accreditations.css">', '<script src="/accreditations.js"></script>'):
                with self.subTest(page=page, tag=tag):
                    self.change(page, tag, '<!-- ' + tag + ' -->')
                    with self.assertRaisesRegex(ValueError, re.escape(page)):
                        validate_accreditations_bundle(self.upload)
                    self.change(page, '<!-- ' + tag + ' -->', tag)

    def test_rejects_incorrect_jawda_or_adhics_scores_on_each_uploaded_page(self):
        for page in PAGES:
            for before, after in (('99.55<span>', '99.54<span>'), ('98<span>', '97<span>')):
                with self.subTest(page=page, score=before):
                    self.change(page, before, after)
                    with self.assertRaisesRegex(ValueError, re.escape(page)):
                        validate_accreditations_bundle(self.upload)
                    self.change(page, after, before)

    def test_rejects_wrong_grade_authority_heading_or_facility_mapping(self):
        for page in PAGES:
            arabic = page.startswith('ar/')
            changes = (
                ('التصنيف A' if arabic else 'GRADE A', 'التصنيف B' if arabic else 'GRADE B'),
                ('دائرة الصحة' if arabic else 'Department of Health', 'جهة أخرى' if arabic else 'Another authority'),
                ('نتيجة ADHICS' if arabic else 'ADHICS Score', 'الامتثال لمعيار ADHICS' if arabic else 'ADHICS Compliance'),
                ('MF7451', 'MF7452'),
                ('مركز د. منير سلوادي لطب الأسنان' if arabic else 'Dr. Munir Silwadi Dental Centre', 'مركز طبي' if arabic else 'Dr. Munir Silwadi Dental Centres'),
            )
            for before, after in changes:
                with self.subTest(page=page, field=before):
                    self.change(page, before, after)
                    with self.assertRaisesRegex(ValueError, re.escape(page)):
                        validate_accreditations_bundle(self.upload)
                    self.change(page, after, before)


if __name__ == '__main__':
    unittest.main()
