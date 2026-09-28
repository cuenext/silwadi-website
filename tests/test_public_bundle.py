import tempfile
import unittest
from pathlib import Path

from tools.public_bundle import build_public_bundle


class PublicBundleTests(unittest.TestCase):
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

            build_public_bundle(source, output)

            self.assertEqual(
                {path.relative_to(output).as_posix() for path in output.rglob('*') if path.is_file()},
                {
                    "index.html", "booking-modal.js", "styles.css", "favicon.svg",
                    "robots.txt", "sitemap.xml", "ar/index.html",
                    "doctors/profile.html", "assets/photo.webp",
                    "assets/review/pediatric-clinic/photo.webp",
                    "assets/video/public.mp4",
                },
            )

    def test_rejects_output_inside_source(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            with self.assertRaises(ValueError):
                build_public_bundle(source, source / "dist")


if __name__ == "__main__":
    unittest.main()
