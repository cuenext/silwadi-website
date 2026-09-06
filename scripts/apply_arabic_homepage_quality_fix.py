from pathlib import Path


def replace_idempotent(text, old, new, label):
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"Missing expected source for {label}")
    return text.replace(old, new, 1)


# Static Arabic homepage
ar_path = Path("ar/index.html")
ar = ar_path.read_text(encoding="utf-8")
ar = replace_idempotent(
    ar,
    '<strong>استكشف الخدمات</strong><em>اعثر على الرعاية المناسبة</em>',
    '<strong>استكشف الخدمات</strong><em>استعرض خدماتنا العلاجية</em>',
    "services shortcut",
)
ar = replace_idempotent(
    ar,
    '<strong>التأمين</strong><em>نقبل التأمين</em>',
    '<strong>التأمين</strong><em>استفسر عن التغطية التأمينية</em>',
    "insurance shortcut",
)
ar = replace_idempotent(
    ar,
    '<strong>الفروع</strong><em>زيارة المركز</em>',
    '<strong>الفروع</strong><em>ابحث عن أقرب فرع</em>',
    "locations shortcut",
)
ar = replace_idempotent(
    ar,
    'نخدم <span class="nowrap-place">أبوظبي</span> منذ عام 1980',
    'نخدم <span class="nowrap-place">مرضى أبوظبي</span> منذ عام 1980',
    "story heading",
)
ar = replace_idempotent(
    ar,
    'على مدى أكثر من أربعة عقود، ركّز مركز سلوادي لطب الأسنان على رعاية تضع احتياجات المريض أولاً، مع علاج مخصص واهتمام بالراحة والتوعية والتواصل الواضح.',
    'منذ أكثر من أربعة عقود، يحرص مركز سلوادي لطب الأسنان على تقديم رعاية تضع المريض واحتياجاته في المقام الأول، مع خطط علاج مخصّصة واهتمام بالراحة والتوعية والتواصل الواضح.',
    "story paragraph",
)
ar_path.write_text(ar, encoding="utf-8")


# Dynamic English -> Arabic language switching
lang_path = Path("language.js")
lang = lang_path.read_text(encoding="utf-8")
lang = replace_idempotent(
    lang,
    "'Find the right care': 'اعثر على الرعاية المناسبة',",
    "'Find the right care': 'استعرض خدماتنا العلاجية',",
    "dynamic services shortcut",
)
lang = replace_idempotent(
    lang,
    "'Insurance accepted': 'نقبل التأمين',",
    "'Insurance accepted': 'استفسر عن التغطية التأمينية',",
    "dynamic insurance shortcut",
)
lang = replace_idempotent(
    lang,
    "'Visit the centre': 'زر المركز',",
    "'Visit the centre': 'ابحث عن أقرب فرع',",
    "dynamic locations shortcut",
)
lang = replace_idempotent(
    lang,
    "'Serving Abu Dhabi since 1980.': 'نخدم أبوظبي منذ عام 1980.',",
    "'Serving Abu Dhabi since 1980.': 'نخدم مرضى أبوظبي منذ عام 1980.',",
    "dynamic story heading",
)
lang = replace_idempotent(
    lang,
    "'For more than four decades, Silwadi Dental Center has focused on patient-centred care, personalized treatment, comfort, patient education and open communication.': 'على مدى أكثر من أربعة عقود، ركّز مركز سلوادي لطب الأسنان على رعاية تتمحور حول المريض، وعلاج مخصص، وراحة المراجع، والتوعية الصحية، والتواصل الواضح.',",
    "'For more than four decades, Silwadi Dental Center has focused on patient-centred care, personalized treatment, comfort, patient education and open communication.': 'منذ أكثر من أربعة عقود، يحرص مركز سلوادي لطب الأسنان على تقديم رعاية تضع المريض واحتياجاته في المقام الأول، مع خطط علاج مخصّصة واهتمام بالراحة والتوعية والتواصل الواضح.',",
    "dynamic story paragraph",
)

additions = """  Object.assign(arabic, {
    'Cosmetic Dentistry & Teeth Whitening': 'تجميل الأسنان وتبييض الأسنان',
    'Specialist restorative care for repairing or replacing teeth with crowns, bridges, veneers, dentures and other prosthetic solutions.': 'رعاية تخصصية لترميم الأسنان أو تعويضها بالتيجان والجسور والقشور والأطقم وغيرها من الحلول التعويضية.',
    'Dental implants replace missing tooth roots and can support crowns, bridges or dentures after clinical assessment and treatment planning.': 'تعوّض زراعة الأسنان جذور الأسنان المفقودة ويمكن أن تدعم التيجان أو الجسور أو الأطقم بعد التقييم والتخطيط العلاجي.',
    'Aesthetic dental care including Hollywood Smile planning, veneers, smile design and professional teeth whitening after assessment.': 'رعاية تجميلية تشمل هوليوود سمايل والقشور وتصميم الابتسامة وتبييض الأسنان الاحترافي بعد التقييم.'
  });

"""
marker = '  Object.assign(arabic, {\n    "Open navigation": "فتح القائمة",'
if "'Specialist restorative care for repairing or replacing teeth with crowns, bridges, veneers, dentures and other prosthetic solutions.'" not in lang:
    if marker not in lang:
        raise SystemExit("Could not find language.js insertion marker")
    lang = lang.replace(marker, additions + marker, 1)

lang_path.write_text(lang, encoding="utf-8")
