from pathlib import Path
from urllib.parse import urlsplit
import re

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "review"
ENGLISH = [
    "orthodontics-v1.html",
    "dental-implants-v1.html",
    "cosmetic-dentistry-v1.html",
    "general-dentistry-v1.html",
    "emergency-dentist-v1.html",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_check_1_clinical_doctor_location_and_contact_facts():
    ortho = read(REVIEW / "orthodontics-v1.html")
    assert all(x in ortho for x in [
        "Dr. Hani Hasbini", "Consultant Orthodontist", "Bani Yas Tower",
        "Dr. Moammar Mohamed Rifai", "Specialist Orthodontist",
        "Dr. Krishnamurthy Balajee", "Both locations",
    ])
    implants = read(REVIEW / "dental-implants-v1.html")
    assert all(x in implants for x in [
        "Dr. Munir Silwadi", "Specialist Prosthodontist &amp; Implantologist", "Both locations",
        "Dr. Fahed Abi Khalil", "Specialist Periodontist &amp; Implantologist", "Bani Yas Tower",
        "Dr. Moheb Silwadi", "General Dentist", "Al Raha Mall",
    ])
    cosmetic = read(REVIEW / "cosmetic-dentistry-v1.html")
    assert "Health first" in cosmetic
    assert "Existing restorations do not whiten" in cosmetic
    general = read(REVIEW / "general-dentistry-v1.html")
    assert general.index("Dr. Moheb Silwadi") < general.index("Dr. Dana Awad") < general.index("Dr. Afnan Mashal")
    emergency = read(REVIEW / "emergency-dentist-v1.html")
    assert "tel:+97126262042" in emergency and "tel:+97126662408" in emergency
    assert "difficulty breathing or swallowing" in emergency
    assert "Emergency medical assessment" in emergency
    assert "earliest appropriate urgent appointment" in emergency


def test_check_2_arabic_is_rtl_natural_and_routeable():
    required = {
        "orthodontics-v1.html": ["تقويم الأسنان", "الإطباق", "المصففات الشفافة"],
        "dental-implants-v1.html": ["زراعة الأسنان", "العظم واللثة", "التركيبة النهائية"],
        "cosmetic-dentistry-v1.html": ["تجميل الأسنان", "التبييض", "القشور الخزفية"],
        "general-dentistry-v1.html": ["طب الأسنان العام", "الحشوات والترميمات", "الإحالة إلى اختصاصي"],
        "emergency-dentist-v1.html": ["طوارئ الأسنان", "برج بني ياس", "الراحة مول"],
    }
    for name, phrases in required.items():
        html = read(REVIEW / "ar" / name)
        assert '<html lang="ar" dir="rtl">' in html
        assert f'href="../{name}"' in html
        assert 'href="#overview">نظرة عامة</a>' in html
        assert 'href="#team">الأطباء</a>' in html
        for phrase in phrases:
            assert phrase in html
        assert not any(label in html for label in [">Overview<", ">Treatment<", ">Process<", ">Doctors<", ">FAQ<"])


def test_check_3_doctor_portraits_and_implant_hero_have_explicit_presentation_controls():
    css = read(REVIEW / "treatment-refresh-v1.css")
    crops = ["hani", "moammar", "krish", "munir", "fahed", "moheb", "dana", "afnan", "ahmed", "lana"]
    for crop in crops:
        assert f"doctor-crop-{crop}" in css
    assert "doctor-crop-fahed{object-position:50% 7%;transform:scale(1.18)}" in css
    assert "doctor-crop-krish{object-position:50% 8%;transform:scale(1.14)}" in css
    implants = read(REVIEW / "dental-implants-v1.html")
    assert "al-raha-treatment-room.png" in implants
    assert "al-raha-treatment-room.webp" not in implants
    assert 'class="doctor-crop-fahed"' in implants
    ortho = read(REVIEW / "orthodontics-v1.html")
    assert all(f'class="doctor-crop-{x}"' in ortho for x in ["hani", "moammar", "krish"])


def test_check_4_seo_is_publish_ready_while_review_pages_remain_noindex():
    expected = {
        "orthodontics-v1.html": "orthodontics",
        "dental-implants-v1.html": "dental-implants",
        "cosmetic-dentistry-v1.html": "cosmetic-dentistry",
        "general-dentistry-v1.html": "general-dentistry",
        "emergency-dentist-v1.html": "emergency-dentist",
    }
    for name, slug in expected.items():
        html = read(REVIEW / name)
        assert '<meta name="robots" content="noindex,nofollow,noarchive">' in html
        assert f'<link rel="canonical" href="https://silwadi.ae/treatments/{slug}.html">' in html
        assert '<meta property="og:title"' in html and '<meta property="og:description"' in html
        assert '<meta name="twitter:card" content="summary_large_image">' in html
        assert 'hreflang="en-AE"' in html and 'hreflang="ar-AE"' in html and 'hreflang="x-default"' in html
        assert '"@type":"WebPage"' in html
        assert '"@type":"Service"' in html
        assert '"@type":"FAQPage"' in html
        ar = read(REVIEW / "ar" / name)
        assert '<meta name="robots" content="noindex,nofollow,noarchive">' in ar
        assert f'<link rel="canonical" href="https://silwadi.ae/ar/treatments/{slug}.html">' in ar
        assert '"inLanguage":"ar-AE"' in ar


def _local_target(page: Path, raw: str) -> Path | None:
    raw = raw.strip()
    if not raw or raw.startswith(("#", "http://", "https://", "tel:", "mailto:", "javascript:")):
        return None
    clean = urlsplit(raw).path
    if not clean:
        return None
    if clean.startswith("/"):
        return ROOT / clean.lstrip("/")
    return (page.parent / clean).resolve()


def test_check_5_internal_links_assets_language_switches_and_emergency_ctas_resolve():
    pages = [REVIEW / name for name in ENGLISH] + [REVIEW / "ar" / name for name in ENGLISH]
    for page in pages:
        html = read(page)
        refs = re.findall(r'(?:href|src)="([^"]+)"', html)
        unresolved = []
        for ref in refs:
            target = _local_target(page, ref)
            if target is not None and not target.exists():
                unresolved.append((ref, str(target)))
        assert not unresolved, (page.name, unresolved)
        assert 'class="language-switch' in html
    emergency = read(REVIEW / "emergency-dentist-v1.html")
    hero = emergency.split('<section class="hero">', 1)[1].split('</section>', 1)[0]
    assert "Call Bani Yas Tower" in hero and "Call Al Raha Mall" in hero
    ar_emergency = read(REVIEW / "ar" / "emergency-dentist-v1.html")
    ar_hero = ar_emergency.split('<section class="hero">', 1)[1].split('</section>', 1)[0]
    assert "اتصل بفرع برج بني ياس" in ar_hero and "اتصل بفرع الراحة مول" in ar_hero
