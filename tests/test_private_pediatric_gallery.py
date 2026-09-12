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
        self.assertIn('href="#clinic">Clinic</a>', text)

    def test_gallery_uses_selected_images(self):
        text = PAGE.read_text(encoding="utf-8")
        names = ["dscf2888.webp", "dscf2905.webp", "dscf2896.webp", "dscf2894.webp", "dscf2892.webp"]
        for name in names:
            path = ROOT / "assets" / "review" / "pediatric-clinic" / name
            self.assertTrue(path.exists(), name)
            data = path.read_bytes()
            self.assertEqual(data[:4], b"RIFF", f"{name} must be a valid RIFF WebP")
            self.assertEqual(data[8:12], b"WEBP", f"{name} must be a valid WebP")
            self.assertLess(len(data), 150_000, f"{name} should remain lightweight for page load")
            self.assertIn(name, text)
        self.assertIn("data-pd-carousel", text)
        self.assertIn("data-pd-prev", text)
        self.assertIn("data-pd-next", text)
        self.assertIn('fetchpriority="high"', text)
        self.assertGreaterEqual(text.count('loading="lazy"'), 4)

    def test_gallery_supports_arrows_keyboard_and_swipe(self):
        text = PAGE.read_text(encoding="utf-8")
        self.assertIn('aria-label="Previous clinic photo"', text)
        self.assertIn('aria-label="Next clinic photo"', text)
        self.assertIn("carousel.addEventListener('keydown'", text)
        self.assertIn("carousel.addEventListener('pointerdown'", text)
        self.assertIn("carousel.addEventListener('pointerup'", text)
        self.assertIn("touch-action:pan-y", text)

    def test_review_stays_private_and_uses_current_booking_anchor(self):
        text = PAGE.read_text(encoding="utf-8")
        self.assertIn('name="robots" content="noindex,nofollow', text)
        self.assertIn("Private review", text)
        self.assertIn("Not published", text)
        self.assertNotIn('../contact.html#consultation"', text)
        self.assertIn('../contact.html#consultation-form', text)


if __name__ == "__main__":
    unittest.main()
