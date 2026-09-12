from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "review/pediatric-dentistry-v1.html"


class PediatricClinicGalleryContract(unittest.TestCase):
    def test_gallery_is_before_hero(self):
        text = PAGE.read_text(encoding="utf-8")
        main = text.split("<main>", 1)[1]
        self.assertLess(main.index('id="clinic"'), main.index('id="hero"'))
        self.assertIn("Explore Our Pediatric Clinic", text)

    def test_gallery_uses_selected_images(self):
        text = PAGE.read_text(encoding="utf-8")
        names = ["dscf2888.webp", "dscf2905.webp", "dscf2896.webp", "dscf2894.webp", "dscf2892.webp"]
        for name in names:
            path = ROOT / "assets" / "review" / "pediatric-clinic" / name
            self.assertTrue(path.exists(), name)
            self.assertIn(name, text)
        self.assertIn("data-pd-carousel", text)
        self.assertIn("data-pd-prev", text)
        self.assertIn("data-pd-next", text)


if __name__ == "__main__":
    unittest.main()
