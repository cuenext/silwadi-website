from pathlib import Path


def replace_idempotent(text, old, new, label):
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"Missing expected source for {label}: {old}")
    return text.replace(old, new, 1)


# Static Arabic homepage: write for Arabic readers, not as literal English translation.
ar_path = Path("ar/index.html")
ar = ar_path.read_text(encoding="utf-8")
static_replacements = [
    ('<p>فريق طبي متكامل بخبرة راسخة.</p>', '<p>خبرات متكاملة في مختلف تخصصات طب الأسنان.</p>', 'team proof'),
    ('<strong>استكشف الخدمات</strong><em>استعرض خدماتنا العلاجية</em>', '<strong>استكشف الخدمات</strong><em>اختر الخدمة المناسبة لك</em>', 'services shortcut'),
    ('<strong>التأمين</strong><em>استفسر عن التغطية التأمينية</em>', '<strong>التأمين</strong><em>تحقّق من التغطية التأمينية</em>', 'insurance shortcut'),
    ('<strong>الفروع</strong><em>ابحث عن أقرب فرع</em>', '<strong>الفروع</strong><em>ابحث عن أقرب فرع إليك</em>', 'locations shortcut'),
    ('<h2>نخدم <span class="nowrap-place">مرضى أبوظبي</span> منذ عام 1980</h2>', '<h2>في خدمة مجتمع <span class="nowrap-place">أبوظبي</span> منذ عام 1980</h2>', 'story heading'),
    ('<p>منذ أكثر من أربعة عقود، يحرص مركز سلوادي لطب الأسنان على تقديم رعاية تضع المريض واحتياجاته في المقام الأول، مع خطط علاج مخصّصة واهتمام بالراحة والتوعية والتواصل الواضح.</p>', '<p>لأكثر من أربعة عقود، يقدّم مركز سلوادي لطب الأسنان رعاية تتمحور حول المريض، مع خطط علاج مخصّصة واهتمام بالراحة والتوعية والتواصل الواضح.</p>', 'story paragraph'),
    ('<h3>تركيبات الأسنان</h3><p>رعاية تخصصية لترميم الأسنان أو تعويضها بالتيجان والجسور والقشور والأطقم وغيرها من الحلول التعويضية.</p>', '<h3>تركيبات الأسنان</h3><p>رعاية تخصصية لترميم الأسنان أو تعويض المفقود منها باستخدام التيجان والجسور والقشور والأطقم وغيرها من الحلول.</p>', 'prosthodontics card'),
    ('<h3>زراعة الأسنان</h3><p>تعوّض زراعة الأسنان جذور الأسنان المفقودة ويمكن أن تدعم التيجان أو الجسور أو الأطقم بعد التقييم والتخطيط العلاجي.</p>', '<h3>زراعة الأسنان</h3><p>تعوّض زراعة الأسنان جذور الأسنان المفقودة، ويمكنها دعم التيجان والجسور أو أطقم الأسنان بعد التقييم ووضع خطة العلاج المناسبة.</p>', 'implantology card'),
    ('<h3>تقويم الأسنان</h3><p>رعاية تخصصية للتقويم والصفافات وتصحيح اصطفاف الأسنان والإطباق.</p>', '<h3>تقويم الأسنان</h3><p>رعاية تخصصية لتقويم الأسنان باستخدام التقويم والصفافات الشفافة وتصحيح اصطفاف الأسنان والإطباق.</p>', 'orthodontics card'),
    ('alt="تجميل الأسنان وتبييض الأسنان"', 'alt="تجميل الأسنان وتبييضها"', 'cosmetic card alt'),
    ('<h3>تجميل الأسنان وتبييض الأسنان</h3><p>رعاية تجميلية تشمل هوليوود سمايل والقشور وتصميم الابتسامة وتبييض الأسنان الاحترافي بعد التقييم.</p>', '<h3>تجميل الأسنان وتبييضها</h3><p>خدمات تجميلية تشمل هوليوود سمايل، والقشور، وتصميم الابتسامة، وتبييض الأسنان الاحترافي بعد التقييم.</p>', 'cosmetic card'),
    ('<h3>العلاجات الوقائية</h3><p>فحوصات دورية وتخطيط وقائي ورعاية تدعم صحة الفم المستمرة.</p>', '<h3>الرعاية الوقائية</h3><p>فحوصات دورية وخطط وقائية تساعد على الحفاظ على صحة الفم والأسنان.</p>', 'preventive card'),
    ('<h3>أمراض اللثة</h3><p>رعاية تخصصية للثة والأنسجة الداعمة المحيطة بالأسنان.</p>', '<h3>علاج اللثة</h3><p>رعاية تخصصية للثة والأنسجة الداعمة للأسنان.</p>', 'periodontics card'),
]
for old, new, label in static_replacements:
    ar = replace_idempotent(ar, old, new, label)
ar_path.write_text(ar, encoding="utf-8")


# Dynamic English -> Arabic switcher: keep the same natural Arabic where those English strings appear.
lang_path = Path("language.js")
lang = lang_path.read_text(encoding="utf-8")
dynamic_replacements = [
    ("'One established clinical team.': 'فريق طبي متكامل بخبرة راسخة.',", "'One established clinical team.': 'خبرات متكاملة في مختلف تخصصات طب الأسنان.',", 'dynamic team proof'),
    ("'Find the right care': 'استعرض خدماتنا العلاجية',", "'Find the right care': 'اختر الخدمة المناسبة لك',", 'dynamic services shortcut'),
    ("'Insurance accepted': 'استفسر عن التغطية التأمينية',", "'Insurance accepted': 'تحقّق من التغطية التأمينية',", 'dynamic insurance shortcut'),
    ("'Visit the centre': 'ابحث عن أقرب فرع',", "'Visit the centre': 'ابحث عن أقرب فرع إليك',", 'dynamic locations shortcut'),
    ("'Serving Abu Dhabi since 1980.': 'نخدم مرضى أبوظبي منذ عام 1980.',", "'Serving Abu Dhabi since 1980.': 'في خدمة مجتمع أبوظبي منذ عام 1980.',", 'dynamic story heading'),
    ("'For more than four decades, Silwadi Dental Center has focused on patient-centred care, personalized treatment, comfort, patient education and open communication.': 'منذ أكثر من أربعة عقود، يحرص مركز سلوادي لطب الأسنان على تقديم رعاية تضع المريض واحتياجاته في المقام الأول، مع خطط علاج مخصّصة واهتمام بالراحة والتوعية والتواصل الواضح.',", "'For more than four decades, Silwadi Dental Center has focused on patient-centred care, personalized treatment, comfort, patient education and open communication.': 'لأكثر من أربعة عقود، يقدّم مركز سلوادي لطب الأسنان رعاية تتمحور حول المريض، مع خطط علاج مخصّصة واهتمام بالراحة والتوعية والتواصل الواضح.',", 'dynamic story paragraph'),
    ("'Cosmetic Dentistry & Teeth Whitening': 'تجميل الأسنان وتبييض الأسنان',", "'Cosmetic Dentistry & Teeth Whitening': 'تجميل الأسنان وتبييضها',", 'dynamic cosmetic title'),
    ("'Specialist care for braces, aligners, tooth alignment and bite correction.': 'رعاية تخصصية للتقويم والصفافات وتصحيح اصطفاف الأسنان والإطباق.',", "'Specialist care for braces, aligners, tooth alignment and bite correction.': 'رعاية تخصصية لتقويم الأسنان باستخدام التقويم والصفافات الشفافة وتصحيح اصطفاف الأسنان والإطباق.',", 'dynamic orthodontics card'),
    ("'Routine examinations, preventive planning and care that supports ongoing oral health.': 'فحوصات دورية وتخطيط وقائي ورعاية تدعم صحة الفم المستمرة.',", "'Routine examinations, preventive planning and care that supports ongoing oral health.': 'فحوصات دورية وخطط وقائية تساعد على الحفاظ على صحة الفم والأسنان.',", 'dynamic preventive card'),
    ("'Specialist care for the gums and supporting tissues around the teeth.': 'رعاية تخصصية للثة والأنسجة الداعمة المحيطة بالأسنان.',", "'Specialist care for the gums and supporting tissues around the teeth.': 'رعاية تخصصية للثة والأنسجة الداعمة للأسنان.',", 'dynamic periodontics card'),
    ("'Specialist restorative care for repairing or replacing teeth with crowns, bridges, veneers, dentures and other prosthetic solutions.': 'رعاية تخصصية لترميم الأسنان أو تعويضها بالتيجان والجسور والقشور والأطقم وغيرها من الحلول التعويضية.',", "'Specialist restorative care for repairing or replacing teeth with crowns, bridges, veneers, dentures and other prosthetic solutions.': 'رعاية تخصصية لترميم الأسنان أو تعويض المفقود منها باستخدام التيجان والجسور والقشور والأطقم وغيرها من الحلول.',", 'dynamic prosthodontics card'),
    ("'Dental implants replace missing tooth roots and can support crowns, bridges or dentures after clinical assessment and treatment planning.': 'تعوّض زراعة الأسنان جذور الأسنان المفقودة ويمكن أن تدعم التيجان أو الجسور أو الأطقم بعد التقييم والتخطيط العلاجي.',", "'Dental implants replace missing tooth roots and can support crowns, bridges or dentures after clinical assessment and treatment planning.': 'تعوّض زراعة الأسنان جذور الأسنان المفقودة، ويمكنها دعم التيجان والجسور أو أطقم الأسنان بعد التقييم ووضع خطة العلاج المناسبة.',", 'dynamic implantology card'),
    ("'Aesthetic dental care including Hollywood Smile planning, veneers, smile design and professional teeth whitening after assessment.': 'رعاية تجميلية تشمل هوليوود سمايل والقشور وتصميم الابتسامة وتبييض الأسنان الاحترافي بعد التقييم.'", "'Aesthetic dental care including Hollywood Smile planning, veneers, smile design and professional teeth whitening after assessment.': 'خدمات تجميلية تشمل هوليوود سمايل، والقشور، وتصميم الابتسامة، وتبييض الأسنان الاحترافي بعد التقييم.'", 'dynamic cosmetic card'),
]
for old, new, label in dynamic_replacements:
    lang = replace_idempotent(lang, old, new, label)
lang_path.write_text(lang, encoding="utf-8")
