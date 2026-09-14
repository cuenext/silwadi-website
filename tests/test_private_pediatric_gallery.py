from pathlib import Path
import unittest

# Private pediatric clinic carousel review contract.
ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "review/pediatric-dentistry-v1.html"


class PediatricClinicGalleryContract(unittest.TestCase):
    def test_hero_is_first_and_gallery_follows_it(self):
        text = PAGE.read_text(encoding="utf-8")
        main = text.split("<main>", 1)[1]
        self.assertLess(main.index('id="hero"'), main.index('id="clinic"'))
        self.assertIn('href="#hero">Overview</a>', text)
        self.assertIn('href="#clinic">Clinic</a>', text)
        self.assertIn("Explore Our Pediatric Clinic", text)

    def test_hero_uses_requested_heading_without_large_visual(self):
        text = PAGE.read_text(encoding="utf-8")
        self.assertIn('<h1>Pediatric Dentistry in <span>Abu&nbsp;Dhabi</span></h1>', text)
        self.assertNotIn('<div class="pd-hero__visual">', text)
        self.assertNotIn('../assets/about/silwadi-hero.jpg', text)

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

    def test_gallery_uses_non_overlapping_scroll_snap_layout(self):
        text = PAGE.read_text(encoding="utf-8")
        self.assertIn('class="pd-clinic-viewport"', text)
        self.assertIn('data-pd-viewport', text)
        self.assertIn('class="pd-clinic-track"', text)
        self.assertIn('scroll-snap-type:x mandatory', text)
        self.assertIn('scroll-snap-align:center', text)
        self.assertNotIn('.pd-clinic-slide{position:absolute', text)
        self.assertNotIn('translate(-147%', text)
        self.assertNotIn('translate(47%', text)

    def test_desktop_gallery_keeps_one_dominant_center_slide(self):
        text = PAGE.read_text(encoding="utf-8")
        self.assertIn('--pd-slide-width:min(82vw,1120px)', text)
        self.assertIn('--pd-slide-width:86vw', text)

    def test_gallery_supports_arrows_keyboard_native_swipe_and_button_looping(self):
        text = PAGE.read_text(encoding="utf-8")
        self.assertIn('aria-label="Previous clinic photo"', text)
        self.assertIn('aria-label="Next clinic photo"', text)
        self.assertIn("carousel.addEventListener('keydown'", text)
        self.assertIn("viewport.scrollTo({", text)
        self.assertIn("touch-action:pan-y", text)
        self.assertIn('index = (nextIndex + slides.length) % slides.length;', text)
        self.assertIn("previous.addEventListener('click', () => go(-1))", text)
        self.assertIn("next.addEventListener('click', () => go(1))", text)
        self.assertNotIn("carousel.addEventListener('pointerdown'", text)
        self.assertNotIn("carousel.addEventListener('pointerup'", text)

    def test_review_stays_private_and_uses_current_booking_anchor(self):
        text = PAGE.read_text(encoding="utf-8")
        self.assertIn('name="robots" content="noindex,nofollow', text)
        self.assertIn("Private review", text)
        self.assertIn("Not published", text)
        self.assertNotIn('../contact.html#consultation"', text)
        self.assertIn('../contact.html#consultation-form', text)


if __name__ == "__main__":
    unittest.main()
