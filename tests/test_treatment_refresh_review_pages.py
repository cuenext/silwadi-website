from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "review"

PAGES = {
    "orthodontics-v1.html": {
        "title": "Orthodontics in Abu Dhabi",
        "image": "../assets/services/orthodontics.webp",
        "doctors": ["Dr. Hani Hasbini", "Dr. Moammar Mohamed Rifai", "Dr. Krishnamurthy Balajee"],
        "live": "https://silwadi.ae/treatments/orthodontics.html",
        "arabic": "./ar/orthodontics-v1.html",
    },
    "dental-implants-v1.html": {
        "title": "Dental Implants in Abu Dhabi",
        "image": "../assets/locations/al-raha-treatment-room.png",
        "doctors": ["Dr. Munir Silwadi", "Dr. Fahed Abi Khalil", "Dr. Moheb Silwadi"],
        "live": "https://silwadi.ae/treatments/dental-implants.html",
        "arabic": "./ar/dental-implants-v1.html",
    },
    "cosmetic-dentistry-v1.html": {
        "title": "Cosmetic Dentistry in Abu Dhabi",
        "image": "../assets/services/cosmetics.webp",
        "doctors": ["Dr. Munir Silwadi", "Dr. Moheb Silwadi", "Dr. Dana Awad"],
        "live": "https://silwadi.ae/treatments/cosmetic-dentistry.html",
        "arabic": "./ar/cosmetic-dentistry-v1.html",
    },
    "general-dentistry-v1.html": {
        "title": "General Dentistry in Abu Dhabi",
        "image": "../assets/services/preventive-dentistry.webp",
        "doctors": ["Dr. Moheb Silwadi", "Dr. Dana Awad", "Dr. Afnan Mashal"],
        "live": "https://silwadi.ae/treatments/general-dentistry.html",
        "arabic": "./ar/general-dentistry-v1.html",
    },
    "emergency-dentist-v1.html": {
        "title": "Emergency Dentist in Abu Dhabi",
        "image": "../assets/locations/bani-yas-treatment-room.webp",
        "doctors": ["Dr. Dana Awad", "Dr. Moheb Silwadi", "Dr. Ahmed El Shehri", "Dr. Lana Almasoud"],
        "live": "https://silwadi.ae/treatments/emergency-dentist.html",
        "arabic": "./ar/emergency-dentist-v1.html",
    },
}

ARABIC_TITLES = {
    "orthodontics-v1.html": "تقويم الأسنان في أبوظبي",
    "dental-implants-v1.html": "زراعة الأسنان في أبوظبي",
    "cosmetic-dentistry-v1.html": "تجميل الأسنان في أبوظبي",
    "general-dentistry-v1.html": "طب الأسنان العام في أبوظبي",
    "emergency-dentist-v1.html": "طوارئ الأسنان في أبوظبي",
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


def test_requested_doctor_order_and_portrait_alignment_contract():
    general = read("general-dentistry-v1.html")
    positions = [general.index(name) for name in PAGES["general-dentistry-v1.html"]["doctors"]]
    assert positions == sorted(positions)

    ortho = read("orthodontics-v1.html")
    for crop in ["doctor-crop-hani", "doctor-crop-moammar", "doctor-crop-krish"]:
        assert crop in ortho

    implants = read("dental-implants-v1.html")
    for crop in ["doctor-crop-munir", "doctor-crop-fahed", "doctor-crop-moheb"]:
        assert crop in implants

    css = read("treatment-refresh-v1.css")
    for crop in ["doctor-crop-hani", "doctor-crop-moammar", "doctor-crop-krish", "doctor-crop-munir", "doctor-crop-fahed", "doctor-crop-moheb"]:
        assert crop in css


def test_emergency_hero_represents_both_locations_equally():
    html = read("emergency-dentist-v1.html")
    hero = html.split('<section class="hero">', 1)[1].split('</section>', 1)[0]
    assert "Bani Yas Tower" in hero
    assert "Al Raha Mall" in hero
    assert hero.count('href="tel:+97126262042"') == 1
    assert hero.count('href="tel:+97126662408"') == 1
    assert "Two Abu Dhabi locations" in hero or "Both Abu Dhabi clinics" in hero
    assert "Call Bani Yas Tower" in hero
    assert "Call Al Raha Mall" in hero


def test_review_pages_have_production_ready_seo_while_remaining_noindex():
    for name, spec in PAGES.items():
        html = read(name)
        assert f'<link rel="canonical" href="{spec["live"]}">' in html
        assert '<meta property="og:type" content="website">' in html
        assert '<meta property="og:site_name" content="Silwadi Dental Center">' in html
        assert '<meta name="twitter:card" content="summary_large_image">' in html
        assert 'application/ld+json' in html
        assert f'hreflang="en-AE" href="{spec["live"]}"' in html
        assert 'hreflang="ar-AE"' in html
        assert f'href="{spec["arabic"]}"' in html


def test_arabic_review_counterparts_exist_and_are_rtl():
    ar_dir = REVIEW / "ar"
    for name, title in ARABIC_TITLES.items():
        page = ar_dir / name
        assert page.exists(), name
        html = page.read_text(encoding="utf-8")
        assert '<html lang="ar" dir="rtl">' in html
        assert 'content="noindex,nofollow,noarchive"' in html
        assert title in html
        assert 'href="../treatment-refresh-v1.css"' in html
        assert 'src="../treatment-refresh-v1.js"' in html
        assert 'class="language-switch"' in html
        assert "معاينة خاصة" in html or "مراجعة خاصة" in html
        assert "احجز" in html
        assert "واتساب" in html
        assert "الأسئلة الشائعة" in html


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
    for token in [
        ".hero-grid", ".signal-grid", ".treatment-grid", ".doctor-grid", ".faq-list",
        ".language-switch", '[dir="rtl"]', "@media(max-width:760px)"
    ]:
        assert token in css_text
    for token in ["data-menu-button", "data-mobile-nav", "data-faq-details"]:
        assert token in js_text
