from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PORTRAITS = {
    "ehab": {
        "asset": "dr-ehab-new.png",
        "version": "20260910-ehab",
        "pages": [
            "doctors.html", "ar/doctors.html",
            "doctors/dr-ehab-hassouneh.html", "ar/doctors/dr-ehab-hassouneh.html",
        ],
        "stale": ["dr-ehab-new-v2.webp"],
    },
    "sara": {
        "asset": "dr-sara-new.png",
        "version": "20260910-sara",
        "pages": [
            "doctors.html", "ar/doctors.html",
            "doctors/dr-sara-ismail.html", "ar/doctors/dr-sara-ismail.html",
        ],
        "stale": ["20260909-sara"],
    },
    "afnan": {
        "asset": "dr-afnan-new.png",
        "version": "20260910-afnan",
        "pages": [
            "doctors.html", "ar/doctors.html",
            "doctors/dr-afnan-mashal.html", "ar/doctors/dr-afnan-mashal.html",
        ],
        "stale": ["dr-afnan-new.webp"],
    },
    "krish": {
        "asset": "dr-krish-new.png",
        "version": "20260910-krish",
        "pages": [
            "doctors.html", "ar/doctors.html",
            "doctors/dr-krishnamurthy-katta-balajee.html", "ar/doctors/dr-krishnamurthy-katta-balajee.html",
        ],
        "stale": ["dr-krish-new%20(2).png", "dr-krish-new (2).png"],
    },
}


def test_uploaded_portraits_are_real_png_files():
    for doctor, cfg in PORTRAITS.items():
        path = ROOT / "assets" / cfg["asset"]
        data = path.read_bytes()
        assert data[:8] == b"\x89PNG\r\n\x1a\n", f"{doctor}: invalid PNG signature"
        assert data[12:16] == b"IHDR", f"{doctor}: missing PNG IHDR"
        assert len(data) > 500_000, f"{doctor}: unexpectedly small portrait ({len(data)} bytes)"


def test_english_and_arabic_pages_use_uploaded_assets_with_cache_busting():
    for doctor, cfg in PORTRAITS.items():
        for rel in cfg["pages"]:
            text = (ROOT / rel).read_text(encoding="utf-8")
            assert cfg["asset"] in text, f"{doctor}: missing new asset in {rel}"
            assert cfg["version"] in text, f"{doctor}: missing fresh cache token in {rel}"
            for stale in cfg["stale"]:
                assert stale not in text, f"{doctor}: stale portrait reference remains in {rel}: {stale}"


def test_ehab_and_sara_portraits_are_not_overzoomed():
    css = (ROOT / "doctor-pages.css").read_text(encoding="utf-8")
    assert ".doctor-directory-card__photo img.doctor-crop-ehab{transform:scale(1);object-position:50% 30%}" in css
    assert ".consultant-portrait__frame img.doctor-crop-ehab{transform:scale(1);object-position:50% 30%}" in css
    assert ".doctor-directory-card__photo img.doctor-crop-sara{transform:scale(1);object-position:50% 25%}" in css
    assert ".consultant-portrait__frame img.doctor-crop-sara{transform:scale(1);object-position:50% 22%}" in css


def test_ehab_does_not_stack_generic_closer_zoom_on_custom_crop():
    for rel in [
        "doctors.html", "ar/doctors.html",
        "doctors/dr-ehab-hassouneh.html", "ar/doctors/dr-ehab-hassouneh.html",
    ]:
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert "doctor-photo-closer doctor-crop-ehab" not in text, rel
