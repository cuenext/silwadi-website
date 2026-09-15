from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "review"

PAGES = {
    "orthodontics-v1.html": {
        "title": "Orthodontics in Abu Dhabi",
        "image": "../assets/services/orthodontics.webp",
        "doctors": ["Dr. Hani Hasbini", "Dr. Moammar Mohamed Rifai", "Dr. Krishnamurthy Balajee"],
    },
    "dental-implants-v1.html": {
        "title": "Dental Implants in Abu Dhabi",
        "image": "../assets/locations/al-raha-treatment-room.webp",
        "doctors": ["Dr. Munir Silwadi", "Dr. Fahed Abi Khalil", "Dr. Moheb Silwadi"],
    },
    "cosmetic-dentistry-v1.html": {
        "title": "Cosmetic Dentistry in Abu Dhabi",
        "image": "../assets/services/cosmetics.webp",
        "doctors": ["Dr. Munir Silwadi", "Dr. Moheb Silwadi", "Dr. Dana Awad"],
    },
    "general-dentistry-v1.html": {
        "title": "General Dentistry in Abu Dhabi",
        "image": "../assets/services/preventive-dentistry.webp",
        "doctors": ["Dr. Dana Awad", "Dr. Moheb Silwadi", "Dr. Afnan Mashal"],
    },
    "emergency-dentist-v1.html": {
        "title": "Emergency Dentist in Abu Dhabi",
        "image": "../assets/locations/bani-yas-treatment-room.webp",
        "doctors": ["Dr. Dana Awad", "Dr. Moheb Silwadi", "Dr. Ahmed El Shehri", "Dr. Lana Almasoud"],
    },
}

def read(name):
    return (REVIEW / name).read_text(encoding="utf-8")

def test_review_pages_exist_and_are_private():
    for name in PAGES:
        page = REVIEW / name
        assert page.exists(), name
        html = read(name)
        assert 'content="noindex,nofollow,noarchive"' in html
        assert 'Private review' in html
        assert 'href="./treatment-refresh-v1.css"' in html
        assert 'src="./treatment-refresh-v1.js"' in html

def test_review_pages_match_endodontics_refresh_structure():
    for name, spec in PAGES.items():
        html = read(name)
        assert spec["title"] in html
        assert spec["image"] in html
        for section_id in ["overview", "options", "process", "team", "faq"]:
            assert f'id="{section_id}"' in html, (name, section_id)
        assert html.count('class="doctor-card"') == len(spec["doctors"])
        for doctor in spec["doctors"]:
            assert doctor in html
        assert html.count('class="signal-card"') >= 5
        assert html.count('class="treatment-card"') >= 4
        assert html.count("<details") >= 4

def test_review_pages_do_not_use_old_detail_page_shell():
    for name in PAGES:
        html = read(name)
        assert 'detail-hero__grid' not in html
        assert 'service-brief' not in html
        assert 'treatment-pages.css' not in html
        assert 'class="hero-grid"' in html
        assert 'class="treatment-subnav"' in html

def test_shared_assets_exist_and_have_expected_contract():
    css = REVIEW / "treatment-refresh-v1.css"
    js = REVIEW / "treatment-refresh-v1.js"
    assert css.exists()
    assert js.exists()
    css_text = css.read_text(encoding="utf-8")
    js_text = js.read_text(encoding="utf-8")
    for token in [".hero-grid", ".signal-grid", ".treatment-grid", ".doctor-grid", ".faq-list", "@media(max-width:760px)"]:
        assert token in css_text
    for token in ["data-menu-button", "data-mobile-nav", "data-faq-details"]:
        assert token in js_text
