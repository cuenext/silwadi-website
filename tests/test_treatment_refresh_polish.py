from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "review"

PAGES = {
    "orthodontics-v1.html": {
        "canonical": "https://silwadi.ae/treatments/orthodontics.html",
        "arabic": "./ar/orthodontics-v1.html",
    },
    "dental-implants-v1.html": {
        "canonical": "https://silwadi.ae/treatments/dental-implants.html",
        "arabic": "./ar/dental-implants-v1.html",
    },
    "cosmetic-dentistry-v1.html": {
        "canonical": "https://silwadi.ae/treatments/cosmetic-dentistry.html",
        "arabic": "./ar/cosmetic-dentistry-v1.html",
    },
    "general-dentistry-v1.html": {
        "canonical": "https://silwadi.ae/treatments/general-dentistry.html",
        "arabic": "./ar/general-dentistry-v1.html",
    },
    "emergency-dentist-v1.html": {
        "canonical": "https://silwadi.ae/treatments/emergency-dentist.html",
        "arabic": "./ar/emergency-dentist-v1.html",
    },
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_all_review_pages_have_publish_ready_seo_structure_but_stay_private():
    for name, spec in PAGES.items():
        html = read(REVIEW / name)
        assert 'content="noindex,nofollow,noarchive"' in html
        assert f'<link rel="canonical" href="{spec["canonical"]}">' in html
        assert '<meta property="og:title"' in html
        assert '<meta property="og:description"' in html
        assert '<script type="application/ld+json" data-seo-schema>' in html
        assert '"@type":"Service"' in html
        assert '"@type":"FAQPage"' in html
        assert 'hreflang="en-AE"' in html
        assert 'hreflang="ar-AE"' in html
        assert f'href="{spec["arabic"]}"' in html
        assert 'class="language-switch"' in html


def test_arabic_review_equivalents_are_real_rtl_pages_not_machine_toggle_placeholders():
    expected_arabic = {
        "orthodontics-v1.html": ["تقويم الأسنان", "أبوظبي", "الأطباء"],
        "dental-implants-v1.html": ["زراعة الأسنان", "أبوظبي", "الأطباء"],
        "cosmetic-dentistry-v1.html": ["تجميل الأسنان", "أبوظبي", "الأطباء"],
        "general-dentistry-v1.html": ["طب الأسنان العام", "أبوظبي", "الأطباء"],
        "emergency-dentist-v1.html": ["طوارئ الأسنان", "أبوظبي", "الراحة مول"],
    }
    for name, phrases in expected_arabic.items():
        page = REVIEW / "ar" / name
        assert page.exists(), name
        html = read(page)
        assert '<html lang="ar" dir="rtl">' in html
        assert '<meta name="content-language" content="ar">' in html
        assert 'content="noindex,nofollow,noarchive"' in html
        assert 'class="language-switch"' in html
        assert f'href="../{name}"' in html
        for phrase in phrases:
            assert phrase in html, (name, phrase)
        for english_label in [">Overview<", ">Treatment<", ">Process<", ">Doctors<", ">FAQ<"]:
            assert english_label not in html, (name, english_label)


def test_requested_doctor_order_and_portrait_alignment_hooks_are_present():
    ortho = read(REVIEW / "orthodontics-v1.html")
    for crop in ["doctor-crop-hani", "doctor-crop-moammar", "doctor-crop-krish"]:
        assert crop in ortho

    implants = read(REVIEW / "dental-implants-v1.html")
    for crop in ["doctor-crop-munir", "doctor-crop-fahed", "doctor-crop-moheb"]:
        assert crop in implants

    general = read(REVIEW / "general-dentistry-v1.html")
    assert general.index("Dr. Moheb Silwadi") < general.index("Dr. Dana Awad") < general.index("Dr. Afnan Mashal")

    css = read(REVIEW / "treatment-refresh-v1.css")
    for crop in ["doctor-crop-hani", "doctor-crop-moammar", "doctor-crop-krish", "doctor-crop-munir", "doctor-crop-fahed", "doctor-crop-moheb", "doctor-crop-dana", "doctor-crop-afnan", "doctor-crop-ahmed", "doctor-crop-lana"]:
        assert f".{crop}" in css


def test_implant_hero_no_longer_uses_low_quality_webp_room_image():
    html = read(REVIEW / "dental-implants-v1.html")
    assert "../assets/locations/al-raha-treatment-room.webp" not in html
    assert "../assets/locations/al-raha-treatment-room.png" in html


def test_emergency_hero_represents_both_branches_and_both_phone_numbers():
    html = read(REVIEW / "emergency-dentist-v1.html")
    hero = html.split('<section class="hero">', 1)[1].split('</section>', 1)[0]
    assert "Bani Yas Tower" in hero
    assert "Al Raha Mall" in hero
    assert "tel:+97126262042" in hero
    assert "tel:+97126662408" in hero
    assert "Two Abu Dhabi locations" in hero

    ar = read(REVIEW / "ar" / "emergency-dentist-v1.html")
    ar_hero = ar.split('<section class="hero">', 1)[1].split('</section>', 1)[0]
    assert "برج بني ياس" in ar_hero
    assert "الراحة مول" in ar_hero
    assert "tel:+97126262042" in ar_hero
    assert "tel:+97126662408" in ar_hero


def test_shared_css_has_rtl_layout_support_without_forking_the_design():
    css = read(REVIEW / "treatment-refresh-v1.css")
    assert '[dir="rtl"]' in css
    assert '.language-switch' in css
