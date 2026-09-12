from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class LanaAlmasoudNameRegression(unittest.TestCase):
    def test_doctors_directory_uses_correct_name(self):
        source = (ROOT / "doctors.html").read_text(encoding="utf-8")
        self.assertIn("Dr. Lana Almasoud", source)
        self.assertNotIn("Dr. Lana Masoud", source)


if __name__ == "__main__":
    unittest.main()
