from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
EHAB = "dr-ehab-20260910.png"
SARA = "dr-sara-20260910.png"


def png_size(path: Path):
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    assert data[12:16] == b"IHDR"
    return struct.unpack(">II", data[16:24]), len(data)


def test_new_portrait_assets_are_valid_pngs():
    (ew, eh), esize = png_size(ROOT / "assets" / EHAB)
    (sw, sh), ssize = png_size(ROOT / "assets" / SARA)
    assert (ew, eh) == (900, 1131)
    assert (sw, sh) == (1024, 1536)
    assert esize > 500_000
    assert ssize > 1_000_000


def test_english_and_arabic_pages_reference_new_assets():
    ehab_pages = [
        ROOT / "doctors.html",
        ROOT / "ar" / "doctors.html",
        ROOT / "doctors" / "dr-ehab-hassouneh.html",
        ROOT / "ar" / "doctors" / "dr-ehab-hassouneh.html",
    ]
    sara_pages = [
        ROOT / "doctors.html",
        ROOT / "ar" / "doctors.html",
        ROOT / "doctors" / "dr-sara-ismail.html",
        ROOT / "ar" / "doctors" / "dr-sara-ismail.html",
    ]
    for path in ehab_pages:
        text = path.read_text(encoding="utf-8")
        assert EHAB in text, path
        assert "dr-ehab-new-v2.webp" not in text, path
    for path in sara_pages:
        text = path.read_text(encoding="utf-8")
        assert SARA in text, path
        assert "dr-sara-new.png" not in text, path


def test_new_portraits_are_not_overzoomed():
    css = (ROOT / "doctor-pages.css").read_text(encoding="utf-8")
    assert ".doctor-directory-card__photo img.doctor-crop-ehab{transform:scale(1);object-position:50% 30%}" in css
    assert ".consultant-portrait__frame img.doctor-crop-ehab{transform:scale(1);object-position:50% 30%}" in css
    assert ".doctor-directory-card__photo img.doctor-crop-sara{transform:scale(1);object-position:50% 25%}" in css
    assert ".consultant-portrait__frame img.doctor-crop-sara{transform:scale(1);object-position:50% 22%}" in css
