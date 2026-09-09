import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET_ASSETS = [
    "dr-lana-new.png",
    "dr-fahed-new.png",
    "dr-afnan-new.webp",
    "dr-krish-new%20(2).png",
    "dr-ehab-new%20(2).png",
]


class SelectedDoctorZoomContract(unittest.TestCase):
    def test_zoom_css_exists_for_directory_and_profile_images(self):
        css = (ROOT / "doctor-pages.css").read_text(encoding="utf-8")
        self.assertIn(".doctor-directory-card__photo img.doctor-photo-closer", css)
        self.assertRegex(css, r"\.doctor-directory-card__photo img\.doctor-photo-closer\s*\{[^}]*scale\(1\.15\)")
        self.assertIn(".consultant-portrait__frame img.doctor-photo-closer", css)
        self.assertRegex(css, r"\.consultant-portrait__frame img\.doctor-photo-closer\s*\{[^}]*scale\(1\.12\)")

    def test_every_targeted_portrait_reference_has_closer_class(self):
        misses = []
        for path in ROOT.rglob("*.html"):
            text = path.read_text(encoding="utf-8")
            for asset in TARGET_ASSETS:
                for tag in re.findall(r"<img\b[^>]*>", text, flags=re.I):
                    if asset in tag and "doctor-photo-closer" not in tag:
                        misses.append(f"{path.relative_to(ROOT)}: {asset}")
        self.assertFalse(misses, "Targeted doctor portraits missing closer crop class:\n" + "\n".join(misses))


if __name__ == "__main__":
    unittest.main()
