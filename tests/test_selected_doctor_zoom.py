import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

INDIVIDUAL = {
    "dr-fahed-new.png": "doctor-crop-fahed",
    "dr-krish-new.png": "doctor-crop-krish",
    "dr-sara-new.png": "doctor-crop-sara",
    "dr-ehab-new.png": "doctor-crop-ehab",
    "dr-afnan-new.png": "doctor-crop-afnan",
}


class SelectedDoctorZoomContract(unittest.TestCase):
    def test_each_selected_doctor_has_its_own_crop_class_everywhere(self):
        misses = []
        for path in ROOT.rglob("*.html"):
            text = path.read_text(encoding="utf-8")
            for asset, crop_class in INDIVIDUAL.items():
                for tag in re.findall(r"<img\b[^>]*>", text, flags=re.I):
                    if asset in tag and crop_class not in tag:
                        misses.append(f"{path.relative_to(ROOT)}: {asset} missing {crop_class}")
        self.assertFalse(misses, "Individual doctor crop classes missing:\n" + "\n".join(misses))

    def test_css_has_individual_directory_and_profile_framing(self):
        css = (ROOT / "doctor-pages.css").read_text(encoding="utf-8")
        expected = {
            "fahed": ("1.22", "8%", "1.17", "8%"),
            "krish": ("1.22", "8%", "1.17", "8%"),
            "sara": ("1", "25%", "1", "22%"),
            "afnan": ("1.18", "10%", "1.14", "10%"),
            "ehab": ("1", "30%", "1", "30%"),
        }
        for doctor, (dir_scale, dir_pos, profile_scale, profile_pos) in expected.items():
            self.assertRegex(
                css,
                rf"\.doctor-directory-card__photo img\.doctor-crop-{doctor}\s*\{{[^}}]*scale\({dir_scale}\)[^}}]*object-position:50% {re.escape(dir_pos)}",
                f"Directory crop missing for {doctor}",
            )
            self.assertRegex(
                css,
                rf"\.consultant-portrait__frame img\.doctor-crop-{doctor}\s*\{{[^}}]*scale\({profile_scale}\)[^}}]*object-position:50% {re.escape(profile_pos)}",
                f"Profile crop missing for {doctor}",
            )

    def test_lana_keeps_existing_shared_crop(self):
        css = (ROOT / "doctor-pages.css").read_text(encoding="utf-8")
        self.assertIn(".doctor-directory-card__photo img.doctor-photo-closer", css)
        self.assertIn(".consultant-portrait__frame img.doctor-photo-closer", css)


if __name__ == "__main__":
    unittest.main()
