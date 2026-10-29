import tempfile
import unittest
from pathlib import Path

from tools.public_bundle import build_public_bundle, public_file, PUBLIC_AI_FILES, validate_assistant_bundle


def patient_page(ar=False):
    destination = '/ai/?lang=ar' if ar else '/ai/'
    link = f'<a href="{destination}">FAQ</a>'
    scripts = ''.join(f'<script src="/ai/assets/{asset}.js" defer></script>' for asset in ('clinic-text', 'booking', 'silwadi-ai-widget'))
    return f'<html lang="{"ar" if ar else "en"}"><body><nav class="site-nav">{link}</nav><footer>{link}</footer>{scripts}</body></html>'


def assistant_fixture(source):
    for name in PUBLIC_AI_FILES:
        file = source / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text('/* public fixture */', encoding='utf-8')
    scripts = ''.join('<script src="./assets/' + asset + '.js"' + (' data-presentation="page"' if asset == 'silwadi-ai-widget' else '') + ' defer></script>'
        for asset in ('faq', 'clinic-text', 'booking', 'silwadi-ai-widget'))
    (source / 'ai/index.html').write_text('<html><body>' + scripts + '<script src="./site-shell.js" defer></script></body></html>', encoding='utf-8')


class PublicBundleTests(unittest.TestCase):
    def test_only_reviewed_public_assistant_files_are_published(self):
        for name in PUBLIC_AI_FILES:
            self.assertTrue(public_file(Path(name)), name)
        for name in ('ai/config.php', 'ai/.env', 'ai/knowledge.json', 'ai/private.js', 'ai/preview/index.html', 'ai/backup/index.html'):
            self.assertFalse(public_file(Path(name)), name)

    def test_copies_public_pages_and_assets_without_source_material(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            output = root / "output"
            for name in (
                "index.html", "booking-modal.js", "styles.css", "favicon.svg",
                "robots.txt", "sitemap.xml", "ar/index.html",
                "doctors/profile.html", "assets/photo.webp",
                "assets/review/pediatric-clinic/photo.webp",
                "assets/video/public.mp4", "assets/video/pod-raha-care-review.mp4",
                "assets/video/pod-raha-review-b64/part-00.txt",
                "assets/archive.zip", "review/index.html", "ai/knowledge.json",
                "node_modules/module.js", "docs/secrets.txt", ".env", "CNAME",
            ):
                path = source / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(name)

            assistant_fixture(source)
            for name in ('index.html', 'ar/index.html', 'doctors/profile.html'):
                (source / name).write_text(patient_page(name.startswith('ar/')), encoding='utf-8')

            build_public_bundle(source, output)

            self.assertEqual(
                {path.relative_to(output).as_posix() for path in output.rglob('*') if path.is_file()},
                {
                    "index.html", "booking-modal.js", "styles.css", "favicon.svg",
                    "robots.txt", "sitemap.xml", "ar/index.html",
                    "doctors/profile.html", "assets/photo.webp",
                    "assets/review/pediatric-clinic/photo.webp",
                    "assets/video/public.mp4",
                } | PUBLIC_AI_FILES,
            )

    def test_rejects_bundle_when_required_assistant_asset_is_missing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'source'
            assistant_fixture(source)
            (source / 'index.html').write_text(patient_page(), encoding='utf-8')
            (source / 'ai/assets/booking.js').unlink()
            with self.assertRaisesRegex(ValueError, 'booking.js'):
                build_public_bundle(source, root / 'output')

    def test_rejects_patient_page_with_only_commented_widget_tag(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'source'
            assistant_fixture(source)
            html = patient_page().replace('<script src="/ai/assets/silwadi-ai-widget.js" defer></script>', '<!-- <script src="/ai/assets/silwadi-ai-widget.js" defer></script> -->')
            (source / 'index.html').write_text(html, encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'silwadi-ai-widget'):
                build_public_bundle(source, root / 'output')

    def test_rejects_patient_page_without_faq_navigation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'source'
            assistant_fixture(source)
            (source / 'index.html').write_text(patient_page().replace('<a href="/ai/">FAQ</a>', ''), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'FAQ'):
                build_public_bundle(source, root / 'output')

    def test_rejects_standalone_page_without_page_presentation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'source'
            assistant_fixture(source)
            (source / 'index.html').write_text(patient_page(), encoding='utf-8')
            target = source / 'ai/index.html'
            target.write_text(target.read_text(encoding='utf-8').replace(' data-presentation="page"', ''), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'presentation'):
                build_public_bundle(source, root / 'output')

    def test_revalidates_actual_output_after_an_asset_is_removed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'source'
            output = root / 'output'
            assistant_fixture(source)
            (source / 'index.html').write_text(patient_page(), encoding='utf-8')
            build_public_bundle(source, output)
            (output / 'ai/assets/silwadi-ai-widget.css').unlink()
            with self.assertRaisesRegex(ValueError, 'silwadi-ai-widget.css'):
                validate_assistant_bundle(output)

    def test_rejects_private_file_added_to_upload_folder(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'source'
            output = root / 'output'
            assistant_fixture(source)
            (source / 'index.html').write_text(patient_page(), encoding='utf-8')
            build_public_bundle(source, output)
            (output / 'ai/config.php').write_text('private configuration', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Non-public file'):
                validate_assistant_bundle(output)

    def test_rejects_output_inside_source(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            with self.assertRaises(ValueError):
                build_public_bundle(source, source / "dist")


if __name__ == "__main__":
    unittest.main()
