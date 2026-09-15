from __future__ import annotations

import html as html_lib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "review"
AR_REVIEW = REVIEW / "ar"

PAGES = {
    "orthodontics-v1.html": {
        "slug": "orthodontics",
        "title": "Orthodontist & Braces in Abu Dhabi | Silwadi Dental Center",
        "description": "Orthodontic care in Abu Dhabi for children, teens and adults, including braces, clear aligners and retention after specialist assessment at Silwadi Dental Center.",
        "service_name": "Orthodontics",
        "service_type": "Orthodontic assessment, braces, clear aligner care and retention",
        "og_image": "https://silwadi.ae/assets/services/orthodontics.webp",
        "faq": [
            ("Are braces the only option?", "No. Depending on the case, options may include fixed braces, clear aligners or other orthodontic systems. A specialist assessment determines what is appropriate."),
            ("Can adults have orthodontic treatment?", "Yes. Orthodontic treatment can be considered for adults as well as children and teenagers, depending on the clinical findings."),
            ("How long does orthodontic treatment take?", "Treatment time varies with the bite, amount of tooth movement, appliance used and how the teeth respond. Your orthodontist can estimate this after assessment."),
            ("Will I need retainers afterwards?", "Retention is commonly part of orthodontic care. Your orthodontist will explain the retention plan that applies to your case."),
            ("Can I choose clear aligners?", "Clear aligners can be suitable for selected cases, but the orthodontist needs to assess whether they can achieve the required movements safely and predictably."),
        ],
    },
    "dental-implants-v1.html": {
        "slug": "dental-implants",
        "title": "Dental Implants in Abu Dhabi | Silwadi Dental Center",
        "description": "Considering dental implants in Abu Dhabi? Learn how implant assessment, restorative planning and long-term maintenance are approached at Silwadi Dental Center.",
        "service_name": "Dental Implants",
        "service_type": "Dental implant assessment, implantology, restorative planning and maintenance",
        "og_image": "https://silwadi.ae/assets/locations/al-raha-treatment-room.png",
        "faq": [
            ("Is everyone suitable for dental implants?", "No. Suitability depends on oral health, available bone, gum condition, medical factors and the planned restoration."),
            ("Do I always need a bone graft?", "No. Bone augmentation is only considered when the available bone and treatment plan indicate that it may be required."),
            ("Do all implant cases use guided surgery?", "No. Digital or guided workflows may be used when they are clinically useful for the individual case."),
            ("How long does implant treatment take?", "Timelines vary depending on the site, healing, whether other procedures are needed and the type of final restoration."),
            ("How do I care for a dental implant?", "Implants require regular cleaning at home and professional maintenance. Your dental team will explain the cleaning approach for your specific restoration."),
        ],
    },
    "cosmetic-dentistry-v1.html": {
        "slug": "cosmetic-dentistry",
        "title": "Cosmetic Dentistry in Abu Dhabi | Silwadi Dental Center",
        "description": "Cosmetic dentistry in Abu Dhabi with health-first planning for whitening, composite bonding, veneers and ceramic restorations at Silwadi Dental Center.",
        "service_name": "Cosmetic Dentistry",
        "service_type": "Aesthetic and restorative dental assessment, whitening, bonding, veneers and ceramic restorations",
        "og_image": "https://silwadi.ae/assets/services/cosmetics.webp",
        "faq": [
            ("Do I need an examination before whitening or veneers?", "Yes. A dental assessment helps identify decay, gum problems, existing restorations or bite issues that may affect the plan."),
            ("Are veneers right for every cosmetic concern?", "No. Veneers are one option. Whitening, bonding, orthodontics, restorative treatment or no treatment may be more appropriate depending on the teeth and your goals."),
            ("Will whitening change the colour of my crowns or fillings?", "No. Existing restorations do not whiten in the same way as natural tooth structure, which is important when planning the final shade."),
            ("Can I preview proposed changes?", "Digital smile planning, photographs, scans or mock-ups may be used in selected cases to support communication before restorative treatment."),
            ("How long do cosmetic restorations last?", "Longevity varies with the material, tooth condition, bite, habits and maintenance. Your dentist can explain the factors relevant to your treatment."),
        ],
    },
    "general-dentistry-v1.html": {
        "slug": "general-dentistry",
        "title": "General Dentist in Abu Dhabi | Silwadi Dental Center",
        "description": "General dentistry in Abu Dhabi for examinations, preventive care, fillings, sensitivity and common restorative concerns at Silwadi Dental Center.",
        "service_name": "General Dentistry",
        "service_type": "General dental examinations, preventive care, restorations and referral when specialist care is indicated",
        "og_image": "https://silwadi.ae/assets/services/preventive-dentistry.webp",
        "faq": [
            ("How often should I have a dental check-up?", "The right interval depends on your oral health and risk factors. Your dentist can recommend a review schedule after examining you."),
            ("Can a general dentist refer me to a specialist?", "Yes. If the problem needs specialist care, the dentist can direct you to the appropriate discipline within the team."),
            ("Do you provide preventive dental care?", "Yes. Preventive planning and oral-hygiene support are part of general dental care, based on individual needs."),
            ("Do I need an X-ray at every visit?", "No. Dental imaging is selected according to clinical need, previous records and the condition being assessed."),
            ("Can I book even if I do not know what treatment I need?", "Yes. Tell reception what is bothering you. A general dentist can assess the problem and explain the appropriate next step."),
        ],
    },
    "emergency-dentist-v1.html": {
        "slug": "emergency-dentist",
        "title": "Emergency Dentist in Abu Dhabi | Silwadi Dental Center",
        "description": "Urgent dental assessment in Abu Dhabi for severe tooth pain, swelling, broken teeth and dental trauma at Silwadi Dental Center's Bani Yas Tower and Al Raha Mall branches.",
        "service_name": "Urgent Dental Care",
        "service_type": "Urgent dental assessment for pain, swelling, fractures and dental trauma",
        "og_image": "https://silwadi.ae/assets/locations/bani-yas-treatment-room.webp",
        "faq": [
            ("Do I need an appointment for an urgent dental problem?", "Call either clinic first. Reception can check the earliest appropriate urgent availability during clinic hours."),
            ("What if I have facial swelling?", "Dental swelling should be assessed promptly. If swelling affects breathing or swallowing, seek emergency medical care immediately."),
            ("What should I do if a permanent tooth is knocked out?", "Handle the tooth carefully by the crown rather than the root and seek urgent dental care immediately. Time can matter in dental trauma."),
            ("Can you tell me the treatment before I arrive?", "No. The dentist needs to assess the cause before recommending treatment."),
            ("Which clinic should I call?", "Bani Yas Tower: +971 2 626 2042. Al Raha Mall: +971 2 666 2408. Reception can advise on current availability."),
        ],
    },
}

DOCTOR_IMAGES = {
    "Dr. Hani Hasbini": "doctor-crop-hani",
    "Dr. Moammar Mohamed Rifai": "doctor-crop-moammar",
    "Dr. Krishnamurthy Balajee": "doctor-crop-krish",
    "Dr. Munir Silwadi": "doctor-crop-munir",
    "Dr. Fahed Abi Khalil": "doctor-crop-fahed",
    "Dr. Moheb Silwadi": "doctor-crop-moheb",
    "Dr. Dana Awad": "doctor-crop-dana",
    "Dr. Afnan Mashal": "doctor-crop-afnan",
    "Dr. Ahmed El Shehri": "doctor-crop-ahmed",
    "Dr. Lana Almasoud": "doctor-crop-lana",
}


def schema_for(spec: dict) -> str:
    canonical = f"https://silwadi.ae/treatments/{spec['slug']}.html"
    graph = [
        {
            "@type": "WebPage",
            "@id": canonical + "#webpage",
            "url": canonical,
            "name": spec["title"],
            "description": spec["description"],
            "inLanguage": "en-AE",
            "isPartOf": {"@id": "https://silwadi.ae/#website"},
            "mainEntity": {"@id": canonical + "#service"},
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://silwadi.ae/"},
                {"@type": "ListItem", "position": 2, "name": "Treatments", "item": "https://silwadi.ae/treatments.html"},
                {"@type": "ListItem", "position": 3, "name": spec["service_name"], "item": canonical},
            ],
        },
        {
            "@type": "Service",
            "@id": canonical + "#service",
            "name": spec["service_name"],
            "serviceType": spec["service_type"],
            "url": canonical,
            "provider": {"@id": "https://silwadi.ae/#organization"},
            "areaServed": {"@type": "City", "name": "Abu Dhabi"},
            "isPartOf": {"@id": "https://silwadi.ae/#website"},
        },
        {
            "@type": "FAQPage",
            "@id": canonical + "#faq",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in spec["faq"]
            ],
        },
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))


def seo_block(name: str, spec: dict) -> str:
    canonical = f"https://silwadi.ae/treatments/{spec['slug']}.html"
    ar_url = f"https://silwadi.ae/ar/treatments/{spec['slug']}.html"
    title = html_lib.escape(spec["title"], quote=True)
    desc = html_lib.escape(spec["description"], quote=True)
    return f'''<!-- REVIEW-SEO-POLISH-START -->
  <meta name="content-language" content="en">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Silwadi Dental Center">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{spec['og_image']}">
  <meta property="og:locale" content="en_AE">
  <meta property="og:locale:alternate" content="ar_AE">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{spec['og_image']}">
  <link rel="alternate" hreflang="en-AE" href="{canonical}">
  <link rel="alternate" hreflang="ar-AE" href="{ar_url}">
  <link rel="alternate" hreflang="x-default" href="{canonical}">
  <script type="application/ld+json" data-seo-schema>{schema_for(spec)}</script>
  <!-- REVIEW-SEO-POLISH-END -->'''


def add_seo(html: str, name: str, spec: dict) -> str:
    html = re.sub(r"\n?\s*<!-- REVIEW-SEO-POLISH-START -->.*?<!-- REVIEW-SEO-POLISH-END -->", "", html, flags=re.S)
    robots = '<meta name="robots" content="noindex,nofollow,noarchive">'
    return html.replace(robots, robots + "\n  " + seo_block(name, spec), 1)


def add_language_switch(html: str, name: str) -> str:
    if f'href="./ar/{name}"' not in html:
        html = html.replace(
            '<div class="global-actions">',
            f'<div class="global-actions"><a class="language-switch" href="./ar/{name}" lang="ar" dir="rtl">العربية</a>',
            1,
        )
    if f'class="language-switch language-switch--mobile" href="./ar/{name}"' not in html:
        html = html.replace(
            '<div class="global-mobile-nav__actions">',
            f'<div class="global-mobile-nav__actions"><a class="language-switch language-switch--mobile" href="./ar/{name}" lang="ar" dir="rtl">العربية</a>',
            1,
        )
    return html


def add_crop_classes(html: str) -> str:
    for doctor, crop in DOCTOR_IMAGES.items():
        pattern = rf'<img(?![^>]*\bclass=)([^>]*?)alt="{re.escape(doctor)}"([^>]*)>'
        html = re.sub(pattern, rf'<img class="{crop}"\1alt="{doctor}"\2>', html)
    return html


def reorder_general(html: str) -> str:
    start = html.find('<div class="doctor-grid">')
    if start == -1:
        return html
    end = html.find('</div></div>\n  </section>', start)
    if end == -1:
        return html
    block = html[start:end]
    cards = re.findall(r'<a class="doctor-card" href="[^"]+">.*?</a>', block, flags=re.S)
    if len(cards) != 3:
        return html
    by_name = {}
    for card in cards:
        for name in ["Dr. Moheb Silwadi", "Dr. Dana Awad", "Dr. Afnan Mashal"]:
            if name in card:
                by_name[name] = card
    if len(by_name) != 3:
        return html
    ordered = "".join(by_name[name] for name in ["Dr. Moheb Silwadi", "Dr. Dana Awad", "Dr. Afnan Mashal"])
    new_block = re.sub(r'(<div class="doctor-grid">).*', r'\1' + ordered, block, count=1, flags=re.S)
    return html[:start] + new_block + html[end:]


def polish_english_pages() -> None:
    for name, spec in PAGES.items():
        path = REVIEW / name
        text = path.read_text(encoding="utf-8")
        text = add_seo(text, name, spec)
        text = add_language_switch(text, name)
        text = add_crop_classes(text)
        if name == "dental-implants-v1.html":
            text = text.replace("../assets/locations/al-raha-treatment-room.webp", "../assets/locations/al-raha-treatment-room.png")
            text = text.replace(
                'alt="Silwadi Dental Center treatment room for implant and restorative care"',
                'alt="Silwadi Dental Center treatment room used for implant and restorative assessment"',
            )
        elif name == "general-dentistry-v1.html":
            text = reorder_general(text)
        elif name == "emergency-dentist-v1.html":
            text = text.replace(
                'For severe tooth pain, a broken tooth, swelling or dental trauma, contact the clinic so reception can check urgent availability and help direct the next step.',
                'For severe tooth pain, swelling, a broken tooth or dental trauma, call either Silwadi branch now. Reception will check the earliest appropriate urgent appointment and direct you to the right clinician.',
            )
            text = text.replace(
                '<div class="hero-actions"><a class="btn btn-primary" href="tel:+97126262042">Call Bani Yas</a><a class="btn btn-secondary" href="../doctors.html">Meet the Team</a></div>',
                '<div class="hero-actions"><a class="btn btn-primary" href="tel:+97126262042">Call Bani Yas Tower</a><a class="btn btn-secondary" href="tel:+97126662408">Call Al Raha Mall</a></div>',
            )
            text = text.replace(
                '<div class="trust-row"><div class="trust-item"><strong>Call first</strong><span>Urgent availability varies</span></div><div class="trust-item"><strong>Assessment</strong><span>Treatment depends on the cause</span></div><div class="trust-item"><strong>Two locations</strong><span>Bani Yas + Al Raha</span></div></div>',
                '<div class="trust-row"><div class="trust-item"><strong>Two Abu Dhabi locations</strong><span>Bani Yas Tower + Al Raha Mall</span></div><div class="trust-item"><strong>Call first</strong><span>Reception checks the earliest urgent slot</span></div><div class="trust-item"><strong>Assessment first</strong><span>Treatment follows the diagnosis</span></div></div>',
            )
        path.write_text(text, encoding="utf-8")


AR_DOCTORS = {
    "hani": {"name": "د. هاني حسبيني", "role": "استشاري تقويم الأسنان", "location": "برج بني ياس", "href": "/ar/doctors/dr-hani-hasbini.html", "image": "/assets/doctors/optimized/dr-hani-hasbini.webp", "crop": "doctor-crop-hani"},
    "moammar": {"name": "د. معمر محمد الرفاعي", "role": "اختصاصي تقويم الأسنان", "location": "برج بني ياس", "href": "/ar/doctors/dr-moammar-rifai.html", "image": "/assets/dr-moammer-new.webp?v=20260907-profilefix", "crop": "doctor-crop-moammar"},
    "krish": {"name": "د. كريشنامورثي بالاجي", "role": "اختصاصي تقويم الأسنان", "location": "كلا الفرعين", "href": "/ar/doctors/dr-krishnamurthy-katta-balajee.html", "image": "/assets/dr-krish-new.png?v=20260910-krish", "crop": "doctor-crop-krish"},
    "munir": {"name": "د. منير سلوادي", "role": "اختصاصي تركيبات وزراعة الأسنان", "location": "كلا الفرعين", "href": "/ar/doctors/dr-munir-silwadi.html", "image": "/assets/dr-munir-new.webp?v=20260907-profilefix", "crop": "doctor-crop-munir"},
    "fahed": {"name": "د. فاهد أبي خليل", "role": "اختصاصي أمراض اللثة وزراعة الأسنان", "location": "برج بني ياس", "href": "/ar/doctors/dr-fahed-khalil.html", "image": "/assets/dr-fahed-new.png?v=20260907-fahed-png-footer-hours2", "crop": "doctor-crop-fahed"},
    "moheb": {"name": "د. مهيب سلوادي", "role": "طبيب أسنان عام", "location": "الراحة مول", "href": "/ar/doctors/dr-moheb-silwadi.html", "image": "/assets/dr-moheb-new.webp?v=20260907-profilefix", "crop": "doctor-crop-moheb"},
    "dana": {"name": "د. دانا عوض", "role": "طبيبة أسنان عامة", "location": "برج بني ياس", "href": "/ar/doctors/dr-dana-awad.html", "image": "/assets/doctors/optimized/dr-dana-awad.webp", "crop": "doctor-crop-dana"},
    "afnan": {"name": "د. أفنان مشعل", "role": "طبيبة أسنان عامة", "location": "برج بني ياس", "href": "/ar/doctors/dr-afnan-mashal.html", "image": "/assets/dr-afnan-new.png?v=20260910-afnan", "crop": "doctor-crop-afnan"},
    "ahmed": {"name": "د. أحمد الشهري", "role": "اختصاصي علاج جذور الأسنان", "location": "برج بني ياس", "href": "/ar/doctors/dr-ahmed-el-shehri.html", "image": "/assets/dr-ahmed-new.webp?v=20260907-profilefix", "crop": "doctor-crop-ahmed"},
    "lana": {"name": "د. لانا المسعود", "role": "اختصاصية علاج جذور الأسنان", "location": "الراحة مول", "href": "/ar/doctors/dr-lana-masoud.html", "image": "/assets/dr-lana-new-v2.webp?v=20260909-lana-profile", "crop": "doctor-crop-lana"},
}

AR_PAGES = {
    "orthodontics-v1.html": {
        "slug": "orthodontics", "label": "تقويم الأسنان", "eyebrow": "رعاية تقويمية", "h1": "تقويم الأسنان في", "hero_image": "/assets/services/orthodontics.webp",
        "description": "رعاية تقويم الأسنان في أبوظبي للأطفال والمراهقين والبالغين، بما في ذلك التقويم الثابت والمصففات الشفافة بعد تقييم اختصاصي.",
        "lead": "تقييم تقويمي متخصص للأطفال والمراهقين والبالغين، مع خطة علاج تراعي اصطفاف الأسنان والإطباق وثبات النتيجة على المدى البعيد.",
        "trust": [("بإشراف اختصاصيين", "تقييم تقويمي متكامل"), ("خيارات علاجية", "تقويم ثابت ومصففات شفافة"), ("لمختلف الأعمار", "أطفال ومراهقون وبالغون")],
        "visual": ("التشخيص هو نقطة البداية.", "يقيّم اختصاصي التقويم الإطباق ومواضع الأسنان والسجلات اللازمة قبل التوصية بالتقويم أو المصففات أو أي خيار آخر."),
        "overview_title": "متى يفيد تقييم تقويم الأسنان؟", "overview_intro": "قد تؤثر مشكلات الاصطفاف في المظهر أو الوظيفة أو كليهما. ويعتمد الخيار المناسب على الإطباق ومواضع الأسنان.",
        "signals": [("تزاحم الأسنان", "تراكب الأسنان أو عدم توفر مساحة كافية لاصطفافها."), ("الفراغات", "قد تكون الفراغات الظاهرة بين الأسنان جزءًا من التقييم التقويمي."), ("العضة العميقة", "قد يكون تراكب الأسنان العلوية والسفلية أكبر من الطبيعي."), ("العضة المعكوسة أو السفلية", "قد تلتقي بعض الأسنان أو الفكين بوضع غير طبيعي."), ("عودة الحركة بعد التقويم", "يمكن أن تتحرك الأسنان بعد علاج سابق، خصوصًا عند تغير استخدام المثبتات.")],
        "options_title": "خيارات علاج تقويم الأسنان", "options_intro": "يُختار الجهاز بعد التشخيص، ولا يناسب كل خيار كل حالة.",
        "options": [("التقويم الثابت", "نظام تقويمي يحرّك الأسنان تدريجيًا وفق خطة علاج محددة."), ("المصففات الشفافة", "يمكن استخدام المصففات القابلة للإزالة في حالات مختارة بعد تقييم اختصاصي."), ("خيارات أكثر تحفظًا من الناحية الجمالية", "قد تُناقش أنظمة أقل ظهورًا عندما تكون مناسبة سريريًا ومتوفرة."), ("المثبتات", "تساعد المثبتات في الحفاظ على موضع الأسنان بعد انتهاء مرحلة التحريك الفعلي.")],
        "process_title": "ماذا تتوقع؟", "process_intro": "مسار واضح يربط التشخيص بأهداف العلاج ثم مرحلة التثبيت.",
        "process": [("الاستشارة", "مناقشة المشكلة وفحص الاصطفاف والإطباق."), ("السجلات", "قد تُستخدم الصور أو المسح الرقمي أو الأشعة عند الحاجة السريرية."), ("العلاج الفعلي", "تُراجع أجهزة التقويم أو المصففات في مواعيد منتظمة."), ("التثبيت", "خطة تثبيت تساعد في الحفاظ على النتيجة بعد العلاج.")],
        "approach": ("تخطيط اختصاصي، وليس علاجًا واحدًا يناسب الجميع.", "الهدف لا يقتصر على جعل الأسنان أكثر استقامة؛ بل يشمل طريقة التقاء الأسنان والنمو عند الأطفال وصحة الفم وثبات النتيجة."),
        "approach_points": [("التشخيص أولًا", "اختيار العلاج يتبع الإطباق والنتائج السريرية."), ("سجلات رقمية", "يمكن أن يساعد المسح والتصوير في التخطيط عند الحاجة."), ("التثبيت مهم", "الحفاظ على النتيجة جزء من الخطة العلاجية.")],
        "doctors": ["hani", "moammar", "krish"],
        "faq": [("هل التقويم الثابت هو الخيار الوحيد؟", "لا. قد تشمل الخيارات التقويم الثابت أو المصففات الشفافة أو أنظمة أخرى، ويحدد التقييم الاختصاصي الأنسب للحالة."), ("هل يمكن للبالغين إجراء تقويم الأسنان؟", "نعم. يمكن علاج البالغين كما الأطفال والمراهقين بحسب النتائج السريرية."), ("كم تستغرق مدة العلاج؟", "تختلف المدة حسب الإطباق ومقدار حركة الأسنان ونوع الجهاز واستجابة الأسنان للعلاج."), ("هل سأحتاج إلى مثبت بعد العلاج؟", "غالبًا ما تكون مرحلة التثبيت جزءًا من العلاج، وسيشرح لك اختصاصي التقويم الخطة المناسبة."), ("هل يمكنني اختيار المصففات الشفافة؟", "قد تكون مناسبة لحالات مختارة، ويحدد الاختصاصي إن كانت قادرة على تحقيق الحركات المطلوبة بأمان وبشكل متوقع.")],
        "cta": ("هل ترغب في تقييم تقويمي؟", "اطلب استشارة وسيساعدك فريقنا في اختيار اختصاصي التقويم والفرع المناسبين."),
    },
    "dental-implants-v1.html": {
        "slug": "dental-implants", "label": "زراعة الأسنان", "eyebrow": "طب زراعة الأسنان", "h1": "زراعة الأسنان في", "hero_image": "/assets/locations/al-raha-treatment-room.png",
        "description": "زراعة الأسنان في أبوظبي مع تقييم سريري وتخطيط تعويضي يراعي العظم واللثة والإطباق والتركيبة النهائية.",
        "lead": "يبدأ علاج الزرعات بخطة تعويضية واضحة: ما الأسنان المفقودة، وما الذي يحتاج إلى تعويض، وحالة العظم واللثة، وكيف يجب أن تعمل الأسنان النهائية.",
        "trust": [("رعاية متخصصة", "زراعة وتركيبات الأسنان"), ("تخطيط", "مسارات رقمية عند الحاجة"), ("التعويض أولًا", "الوظيفة والصيانة طويلة المدى")],
        "visual": ("نخطط للتركيبة قبل موضع الزرعة.", "يُنظر إلى موضع الزرعة والعظم واللثة والإطباق والتركيبة النهائية كخطة واحدة قبل بدء العلاج."),
        "overview_title": "متى يمكن التفكير في زراعة الأسنان؟", "overview_intro": "الزرعات خيار لتعويض الأسنان المفقودة، ويعتمد ملاءمتها على الفم والتاريخ الطبي والتركيبة المخطط لها.",
        "signals": [("سن واحد مفقود", "قد تدعم زرعة واحدة تاجًا لتعويض سن مفقود إذا كانت المنطقة مناسبة."), ("عدة أسنان مفقودة", "يمكن في بعض الحالات استخدام الزرعات لدعم جسر يعوض عدة أسنان."), ("طقم أسنان غير ثابت", "قد تساعد الزرعات في تحسين دعم أو ثبات بعض الأطقم المتحركة."), ("سن لا يمكن الحفاظ عليه", "إذا تعذر الحفاظ على السن بشكل متوقع، تُناقش خيارات التعويض بعد التقييم."), ("مشكلة حول زرعة قديمة", "الألم أو الحركة أو النزف أو مشكلات التركيبة حول زرعة موجودة تحتاج إلى تقييم.")],
        "options_title": "خيارات العلاج بالزرعات", "options_intro": "لا يُحدد عدد الزرعات بمعزل عن بقية الخطة؛ فالتركيبة النهائية والأنسجة الداعمة يوجهان العلاج.",
        "options": [("تاج على زرعة واحدة", "يمكن لزرعة واحدة دعم تاج عندما تكون المنطقة والأنسجة المحيطة مناسبة."), ("جسر مدعوم بالزرعات", "قد تُعوض عدة أسنان مفقودة بجسر مدعوم بالزرعات في حالات مختارة."), ("طقم مدعوم بالزرعات", "يمكن لبعض الأطقم المتحركة الاستفادة من الزرعات لتحسين الدعم أو الثبات."), ("إعادة تأهيل فك كامل", "قد تتطلب الحالات المعقدة خطة ثابتة أو متحركة لفك كامل بعد تقييم تفصيلي.")],
        "process_title": "كيف نخطط لعلاج الزرعات؟", "process_intro": "ترتبط المرحلة الجراحية والمرحلة التعويضية منذ بداية الخطة.",
        "process": [("التقييم", "مراجعة صحة الفم والأسنان المفقودة واللثة والإطباق والتاريخ الطبي."), ("التخطيط", "قد نستخدم التصوير التشخيصي والتخطيط الرقمي عند الحاجة."), ("وضع الزرعة والالتئام", "تُدار مرحلة الزرع والالتئام وفق الحالة الفردية."), ("التركيب والصيانة", "تُثبت التركيبة النهائية وتُناقش خطة العناية طويلة المدى.")],
        "approach": ("نجاح الزرعات يعتمد على خطة متكاملة.", "الزرعة ليست مجرد جزء يوضع في العظم؛ فالسن أو التركيبة النهائية والأنسجة الرخوة والعظم والإطباق والنظافة تؤثر جميعها في تسلسل العلاج والنتيجة."),
        "approach_points": [("تخطيط تعويضي", "موضع السن النهائي يوجّه خطة الزرعة."), ("خبرات متعددة", "قد تشارك خبرات التركيبات واللثة بحسب الحالة."), ("الصيانة", "الزرعات تحتاج أيضًا إلى متابعة مهنية وعناية منزلية.")],
        "doctors": ["munir", "fahed", "moheb"],
        "faq": [("هل زراعة الأسنان مناسبة للجميع؟", "لا. تعتمد الملاءمة على صحة الفم وكمية العظم وحالة اللثة والعوامل الطبية والتركيبة المخطط لها."), ("هل أحتاج دائمًا إلى تطعيم عظمي؟", "لا. يُبحث تعزيز العظم فقط عندما تشير كمية العظم والخطة العلاجية إلى الحاجة إليه."), ("هل تُستخدم الجراحة الموجهة في كل الحالات؟", "لا. قد تُستخدم المسارات الرقمية أو الموجهة عندما تكون مفيدة سريريًا للحالة."), ("كم يستغرق علاج الزرعات؟", "تختلف المدة بحسب المنطقة والالتئام والحاجة إلى إجراءات إضافية ونوع التركيبة النهائية."), ("كيف أعتني بالزرعة؟", "تحتاج الزرعات إلى تنظيف يومي ومتابعة مهنية منتظمة، وسيشرح الفريق طريقة العناية المناسبة لتركيبتك.")],
        "cta": ("هل تفكر في زراعة الأسنان؟", "ابدأ بتقييم سريري لمراجعة احتياجاتك التعويضية والأنسجة الداعمة وخيارات العلاج."),
    },
    "cosmetic-dentistry-v1.html": {
        "slug": "cosmetic-dentistry", "label": "تجميل الأسنان", "eyebrow": "رعاية تجميلية وترميمية", "h1": "تجميل الأسنان في", "hero_image": "/assets/services/cosmetics.webp",
        "description": "تجميل الأسنان في أبوظبي مع تخطيط يضع صحة الأسنان واللثة أولًا، وخيارات تشمل التبييض والترميم بالكومبوزيت والقشور والترميمات الخزفية.",
        "lead": "أي تغيير جمالي للابتسامة يجب أن يبدأ بأسنان ولثة سليمتين. نفحص الأسنان أولًا ثم نناقش الخيارات التجميلية والترميمية الأكثر تحفظًا والمناسبة للحالة.",
        "trust": [("تخطيط الابتسامة", "الصحة قبل الجمال"), ("خيارات متعددة", "تبييض، كومبوزيت، قشور"), ("طب أسنان رقمي", "تخطيط عند الحاجة")],
        "visual": ("تجميل قائم على أساس ترميمي سليم.", "نأخذ في الاعتبار اللون والشكل وبنية الأسنان والترميمات الموجودة والإطباق قبل وضع الخطة التجميلية."),
        "overview_title": "ما الذي يرغب المرضى عادة في تحسينه؟", "overview_intro": "يمكن لطب الأسنان التجميلي معالجة اهتمامات مختلفة، لكن العلاج المناسب يعتمد على بنية الأسنان وصحة الفم.",
        "signals": [("لون الأسنان", "يمكن تقييم التصبغات أو اللون الطبيعي الداكن للتبييض أو خيارات أخرى."), ("حواف مكسورة", "قد تُرمم الكسور الصغيرة والحواف المتآكلة بطرق تحفظية في حالات مختارة."), ("الشكل والتناسب", "يُراجع شكل الأسنان بالنسبة إلى الابتسامة واللثة والإطباق."), ("فراغات صغيرة", "يمكن معالجة بعض الفراغات بخيارات ترميمية أو تقويمية."), ("ترميمات قديمة", "يمكن تقييم الحشوات أو التيجان أو القشور الظاهرة من الناحيتين الوظيفية والجمالية.")],
        "options_title": "خيارات تجميل الأسنان", "options_intro": "نبدأ بأكثر خيار مناسب يحافظ على بنية الأسنان؛ فالعلاج الأكثر ليس دائمًا هو الأفضل.",
        "options": [("التبييض الاحترافي", "يمكن للتبييض تفتيح لون الأسنان الطبيعية بعد التأكد من صحة الأسنان واللثة."), ("الترميم بالكومبوزيت", "يمكن استخدام مادة بلون الأسنان لتعديلات مختارة في الشكل والحواف والترميم."), ("القشور الخزفية", "قد تكون القشور خيارًا لبعض الاحتياجات الجمالية والترميمية بعد تخطيط دقيق."), ("ترميمات خزفية", "قد تكون التيجان أو الترميمات الخزفية مناسبة عندما تحتاج الأسنان أيضًا إلى دعم بنيوي.")],
        "process_title": "من المشكلة إلى خطة العلاج", "process_intro": "تنجح المعالجة الجمالية عندما تتوافق التوقعات مع صحة الفم والاحتياجات الترميمية.",
        "process": [("التقييم", "فحص الأسنان واللثة والترميمات الموجودة والإطباق."), ("تحديد الأهداف", "مناقشة ما ترغب في تغييره وما يمكن تحقيقه بصورة واقعية."), ("التخطيط", "قد تساعد الصور والمسح الرقمي أو تخطيط الابتسامة في حالات مختارة."), ("العلاج والمراجعة", "تنفيذ الخطة المتفق عليها ثم مراجعة الوظيفة والراحة والصيانة.")],
        "approach": ("النتائج الطبيعية تبدأ بعلاج محافظ.", "هدفنا تحسين ما يزعجك مع احترام بنية الأسنان السليمة؛ وقد يكون التبييض أو الإضافة بالكومبوزيت أو حتى عدم العلاج أنسب من إجراء غير عكوس في بعض الحالات."),
        "approach_points": [("الصحة أولًا", "يجب علاج التسوس وأمراض اللثة قبل الإجراءات التجميلية."), ("خيارات محافظة", "نحافظ على بنية السن الطبيعي متى كان ذلك ممكنًا سريريًا."), ("توقعات واضحة", "المواد والترميمات الموجودة تؤثر في ما يمكن تغييره.")],
        "doctors": ["munir", "moheb", "dana"],
        "faq": [("هل أحتاج إلى فحص قبل التبييض أو القشور؟", "نعم. يساعد الفحص في اكتشاف التسوس أو مشكلات اللثة أو الترميمات والإطباق التي قد تؤثر في الخطة."), ("هل القشور مناسبة لكل مشكلة تجميلية؟", "لا. قد يكون التبييض أو الكومبوزيت أو التقويم أو العلاج الترميمي أو حتى عدم العلاج أنسب بحسب الحالة والأهداف."), ("هل يتغير لون التيجان والحشوات مع التبييض؟", "لا. لا تتفتح الترميمات الموجودة مثل الأسنان الطبيعية، وهذا مهم عند تخطيط الدرجة النهائية للون."), ("هل يمكن معاينة التغييرات المقترحة؟", "قد تُستخدم الصور أو المسح الرقمي أو المحاكاة أو النماذج التجريبية في حالات مختارة لدعم التواصل قبل العلاج."), ("كم تدوم الترميمات التجميلية؟", "تختلف المدة حسب المادة وحالة السن والإطباق والعادات والصيانة، وسيشرح الطبيب العوامل المتعلقة بعلاجك.")],
        "cta": ("هل تفكر في تغيير ابتسامتك؟", "ابدأ بفحص الأسنان واللثة ثم ناقش مع الطبيب الخيارات الجمالية المناسبة لحالتك."),
    },
    "general-dentistry-v1.html": {
        "slug": "general-dentistry", "label": "طب الأسنان العام", "eyebrow": "رعاية الأسنان العامة", "h1": "طب الأسنان العام في", "hero_image": "/assets/services/preventive-dentistry.webp",
        "description": "طب الأسنان العام في أبوظبي للفحوصات والرعاية الوقائية والحشوات والحساسية والمشكلات الترميمية الشائعة في مركز سلوادي.",
        "lead": "للفحوصات الدورية أو الحساسية أو كسر بسيط في السن أو مشكلة لا تعرف كيف تصنفها، يكون طبيب الأسنان العام غالبًا نقطة البداية المناسبة.",
        "trust": [("نقطة البداية", "فحص وتشخيص"), ("علاج روتيني", "وقاية وترميم"), ("فريق متكامل", "إحالة إلى اختصاصي عند الحاجة")],
        "visual": ("نقطة بداية عملية للرعاية.", "يجمع طب الأسنان العام بين الفحص والتشخيص والوقاية والعلاجات الترميمية الشائعة، مع الإحالة إلى اختصاصي عند الحاجة."),
        "overview_title": "متى تراجع طبيب الأسنان العام؟", "overview_intro": "لا تحتاج إلى معرفة اسم العلاج قبل الحجز؛ ابدأ بوصف المشكلة وسيقيّم الطبيب سببها.",
        "signals": [("فحص دوري", "تساعد المراجعة المنتظمة في اكتشاف تغيرات صحة الفم مبكرًا."), ("حساسية الأسنان", "الحساسية للبارد أو الحلو أو العض تحتاج إلى تقييم لمعرفة السبب."), ("اشتباه بتسوس", "البقع الداكنة أو انحشار الطعام أو الألم قد تحتاج إلى فحص وتصوير."), ("سن مكسور أو متشقق", "تُقيّم الأسنان المتضررة للإصلاح أو الحماية أو الإحالة عند الحاجة."), ("نزف اللثة", "النزف المستمر قد يرتبط بالتهاب اللثة ويحتاج إلى تقييم.")],
        "options_title": "ماذا يشمل طب الأسنان العام؟", "options_intro": "يعتمد العلاج على التشخيص ويغطي مجموعة واسعة من الاحتياجات الروتينية والترميمية.",
        "options": [("فحوصات الأسنان", "تقييم الأسنان واللثة والترميمات الموجودة والمشكلة التي حضرت بسببها."), ("الحشوات والترميمات", "إصلاح محافظ للأسنان المتأثرة بالتسوس أو التآكل أو الكسور البسيطة عندما يكون مناسبًا."), ("الرعاية الوقائية", "إرشادات النظافة والتنظيف المهني وخطة وقاية تناسب عوامل الخطورة الفردية."), ("الإحالة إلى اختصاصي", "يمكن إحالة الحالات المعقدة في الجذور أو التقويم أو اللثة أو التركيبات ضمن الفريق.")],
        "process_title": "مسار رعاية بسيط", "process_intro": "تبدأ الزيارة بالتشخيص بدل افتراض العلاج الذي تحتاجه.",
        "process": [("الاستماع", "فهم المشكلة والأعراض والتاريخ ذي الصلة."), ("الفحص", "تقييم الأسنان واللثة والأنسجة الداعمة."), ("الشرح", "مناقشة النتائج والخيارات المناسبة."), ("العلاج أو الإحالة", "تقديم الرعاية العامة أو إشراك اختصاصي عندما تكون هناك حاجة.")],
        "approach": ("رعاية شاملة من دون تعقيد الزيارة.", "يستطيع طبيب الأسنان العام معالجة كثير من المشكلات مباشرة، مع توفر اختصاصيين ضمن الفريق عندما تحتاج الحالة إلى خبرة إضافية."),
        "approach_points": [("التشخيص أولًا", "العلاج يستند إلى النتائج السريرية."), ("الوقاية", "العناية المنزلية وتقليل عوامل الخطورة جزء من الرعاية الروتينية."), ("رعاية مترابطة", "تتوفر الإحالة إلى اختصاصيي مركز سلوادي عند الحاجة.")],
        "doctors": ["moheb", "dana", "afnan"],
        "faq": [("كم مرة أحتاج إلى فحص الأسنان؟", "يعتمد الفاصل المناسب على صحة الفم وعوامل الخطورة، ويحدد الطبيب جدول المراجعات بعد الفحص."), ("هل يمكن لطبيب الأسنان العام إحالتي إلى اختصاصي؟", "نعم. إذا احتاجت المشكلة إلى رعاية تخصصية، يوجهك الطبيب إلى الاختصاص المناسب ضمن الفريق."), ("هل تقدمون رعاية وقائية؟", "نعم. تشمل الرعاية العامة التخطيط الوقائي ودعم نظافة الفم حسب الحاجة الفردية."), ("هل أحتاج إلى أشعة في كل زيارة؟", "لا. تُختار الأشعة بحسب الحاجة السريرية والسجلات السابقة والحالة التي يجري تقييمها."), ("هل يمكنني الحجز حتى لو لم أعرف العلاج الذي أحتاجه؟", "نعم. أخبر الاستقبال بما يزعجك وسيقيّم طبيب الأسنان العام المشكلة ويشرح الخطوة التالية.")],
        "cta": ("لست متأكدًا أي طبيب تحتاج؟", "ابدأ بتقييم عام للأسنان وسيساعدك فريقنا في تحديد الخطوة التالية."),
    },
    "emergency-dentist-v1.html": {
        "slug": "emergency-dentist", "label": "طوارئ الأسنان", "eyebrow": "رعاية الأسنان العاجلة", "h1": "طوارئ الأسنان في", "hero_image": "/assets/locations/bani-yas-treatment-room.webp",
        "description": "تقييم عاجل لمشكلات الأسنان في أبوظبي مثل الألم الشديد والتورم وكسور الأسنان وإصابات الأسنان في فرعي برج بني ياس والراحة مول.",
        "lead": "للألم الشديد أو التورم أو كسر السن أو إصابة الأسنان، اتصل الآن بأي من فرعي مركز سلوادي. سيتحقق الاستقبال من أقرب موعد عاجل مناسب ويوجهك إلى الطبيب الأنسب.",
        "trust": [("فرعان في أبوظبي", "برج بني ياس + الراحة مول"), ("اتصل أولًا", "الاستقبال يتحقق من أقرب موعد عاجل"), ("التقييم أولًا", "العلاج يعتمد على التشخيص")],
        "visual": ("الرعاية العاجلة تبدأ بالتقييم.", "يحدد الطبيب سبب المشكلة أولًا ثم يناقش العلاج الفوري الأكثر أمانًا وأي متابعة لازمة."),
        "overview_title": "مشكلات قد تحتاج إلى تقييم عاجل", "overview_intro": "اتصل بالعيادة إذا لم تكن متأكدًا. بعض الأعراض تحتاج إلى عناية أسنان سريعة، بينما تتطلب بعض الحالات طوارئ طبية مباشرة.",
        "signals": [("ألم شديد في الأسنان", "الألم المستمر أو الشديد قد يحتاج إلى فحص سريع وتصوير تشخيصي."), ("سن مكسور", "الكسر أو سقوط حشوة أو تاج قد يعرّض السن أو يضعفه."), ("تورم مرتبط بالأسنان", "قد يرتبط التورم بعدوى ويجب تقييمه بسرعة."), ("إصابة الأسنان", "السن المكسور أو المزاح أو المخلوع قد يكون حساسًا للوقت بحسب نوع الإصابة."), ("نزف أو إصابة أنسجة الفم", "تحتاج إصابات الفم إلى تقييم، خصوصًا إذا كان النزف يصعب السيطرة عليه.")],
        "options_title": "ماذا قد تشمل الرعاية العاجلة؟", "options_intro": "لا يوجد علاج واحد لكل طوارئ الأسنان؛ فالسبب هو الذي يحدد الإجراء المناسب بعد الفحص.",
        "options": [("تقييم الألم", "فحص سريري وتصوير عند الحاجة لتحديد المصدر المرجح للألم."), ("تثبيت مؤقت", "قد يُستخدم ترميم مؤقت أو إجراء وقائي عندما لا يمكن إكمال العلاج النهائي فورًا."), ("علاج إصابات الأسنان", "تختلف المعالجة بحسب ما إذا كان السن متشققًا أو مزاحًا أو مخلوعًا أو ترافقه إصابات أخرى."), ("إحالة أو رعاية تخصصية", "قد يُرتب علاج جذور أو علاج جراحي أو رعاية تخصصية أخرى بحسب التشخيص.")],
        "process_title": "ماذا يحدث عندما تتصل بنا؟", "process_intro": "تعتمد المواعيد العاجلة على ساعات العمل وتوفر الأطباء، لذلك يكون الاتصال أولًا أسرع طريقة لتوجيهك.",
        "process": [("صف المشكلة", "أخبر الاستقبال بما حدث وبالأعراض الرئيسية."), ("التحقق من التوفر", "يتحقق الفريق من الفرع والطبيب الأنسب والأقرب توفرًا."), ("تقييم الأسنان", "يفحص الطبيب المشكلة ويحدد السبب المرجح."), ("الخطة الفورية", "تتلقى علاجًا أو تثبيتًا مؤقتًا أو إحالة بحسب التشخيص.")],
        "approach": ("اعرف متى تصبح مشكلة الأسنان طارئًا طبيًا.", "تورم الوجه أو الرقبة المصحوب بصعوبة في التنفس أو البلع، أو النزف غير المسيطر عليه، أو فقدان الوعي، أو إصابات الوجه الكبيرة تحتاج إلى تقييم طبي طارئ بدل انتظار موعد أسنان."),
        "approach_points": [("صعوبة التنفس أو البلع", "اطلب الرعاية الطبية الطارئة فورًا."), ("إصابة كبيرة", "قد تحتاج إلى تقييم طبي طارئ قبل علاج الأسنان."), ("حالة عاجلة تخص الأسنان فقط", "اتصل بالاستقبال لمعرفة أقرب موعد مناسب خلال ساعات العمل.")],
        "doctors": ["dana", "moheb", "ahmed", "lana"],
        "faq": [("هل أحتاج إلى موعد لمشكلة أسنان عاجلة؟", "اتصل بأي من الفرعين أولًا. يمكن للاستقبال التحقق من أقرب موعد عاجل مناسب خلال ساعات العمل."), ("ماذا أفعل إذا كان لدي تورم في الوجه؟", "يجب تقييم التورم المرتبط بالأسنان بسرعة. وإذا أثر التورم في التنفس أو البلع، اطلب الرعاية الطبية الطارئة فورًا."), ("ماذا أفعل إذا خُلع سن دائم بسبب إصابة؟", "أمسك السن من التاج وليس الجذر واطلب رعاية أسنان عاجلة فورًا؛ فالوقت قد يكون مهمًا في إصابات الأسنان."), ("هل يمكن تحديد العلاج قبل وصولي؟", "لا. يحتاج الطبيب إلى تقييم السبب قبل التوصية بالعلاج."), ("أي فرع أتصل به؟", "برج بني ياس: +971 2 626 2042. الراحة مول: +971 2 666 2408. يمكن للاستقبال إرشادك بحسب التوفر الحالي.")],
        "cta": ("تحتاج إلى مساعدة عاجلة للأسنان؟", "اتصل بالفرع الأقرب أولًا حتى يتحقق الاستقبال من أقرب موعد مناسب."),
        "emergency": True,
    },
}


def ar_schema(page: dict) -> str:
    canonical = f"https://silwadi.ae/ar/treatments/{page['slug']}.html"
    faq = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in page["faq"]]
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebPage", "@id": canonical + "#webpage", "url": canonical, "name": page["label"] + " في أبوظبي | مركز سلوادي لطب الأسنان", "description": page["description"], "inLanguage": "ar-AE", "isPartOf": {"@id": "https://silwadi.ae/#website"}},
            {"@type": "Service", "@id": canonical + "#service", "name": page["label"], "serviceType": page["label"], "url": canonical, "provider": {"@id": "https://silwadi.ae/#organization"}, "areaServed": {"@type": "City", "name": "أبوظبي"}},
            {"@type": "FAQPage", "@id": canonical + "#faq", "mainEntity": faq},
        ],
    }
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def cards(items: list[tuple[str, str]], card_class: str, icon_class: str | None = None) -> str:
    output = []
    for i, (title, body) in enumerate(items, 1):
        if card_class == "signal-card":
            output.append(f'<article class="signal-card"><div class="signal-icon">{i:02d}</div><h3>{title}</h3><p>{body}</p></article>')
        else:
            output.append(f'<article class="treatment-card"><div class="treatment-number">{i:02d}</div><div><h3>{title}</h3><p>{body}</p></div></article>')
    return "".join(output)


def doctor_cards(keys: list[str]) -> str:
    result = []
    for key in keys:
        d = AR_DOCTORS[key]
        result.append(
            f'<a class="doctor-card" href="{d["href"]}"><div class="doctor-card__photo"><img class="{d["crop"]}" src="{d["image"]}" alt="{d["name"]}" loading="lazy" decoding="async"></div>'
            f'<div class="doctor-card__body"><h3>{d["name"]}</h3><div class="doctor-card__role">{d["role"]}</div><div class="doctor-card__location">{d["location"]}</div><p class="doctor-card__focus">تعرّف إلى خبرة الطبيب ومجالات اهتمامه السريري وخيارات الحجز.</p><div class="doctor-card__link">عرض الملف <span>←</span></div></div></a>'
        )
    return "".join(result)


def ar_page(name: str, p: dict) -> str:
    live_en = f"https://silwadi.ae/treatments/{p['slug']}.html"
    live_ar = f"https://silwadi.ae/ar/treatments/{p['slug']}.html"
    title = p["label"] + " في أبوظبي | مركز سلوادي لطب الأسنان"
    if p.get("emergency"):
        hero_actions = '<div class="hero-actions"><a class="btn btn-primary" href="tel:+97126262042">اتصل بفرع برج بني ياس</a><a class="btn btn-secondary" href="tel:+97126662408">اتصل بفرع الراحة مول</a></div>'
        cta_actions = '<div class="cta-actions"><a class="btn btn-primary" href="tel:+97126262042">اتصل ببرج بني ياس</a><a class="btn btn-secondary" href="tel:+97126662408">اتصل بالراحة مول</a></div>'
    else:
        hero_actions = '<div class="hero-actions"><a class="btn btn-primary" href="/ar/contact.html#consultation-form">احجز استشارة</a><a class="btn btn-secondary" href="/ar/doctors.html">تعرّف إلى الفريق</a></div>'
        cta_actions = '<div class="cta-actions"><a class="btn btn-primary" href="/ar/contact.html#consultation-form">احجز استشارة</a><a class="btn btn-secondary" href="/ar/locations.html">عرض الفروع</a></div>'

    trust = ''.join(f'<div class="trust-item"><strong>{a}</strong><span>{b}</span></div>' for a, b in p["trust"])
    process = ''.join(f'<article class="process-step"><div class="process-step__dot">{i:02d}</div><h3>{a}</h3><p>{b}</p></article>' for i, (a, b) in enumerate(p["process"], 1))
    points = ''.join(f'<div class="approach-point"><strong>{a}</strong><span>{b}</span></div>' for a, b in p["approach_points"])
    faq = ''.join(f'<details data-faq-details><summary>{q}</summary><div class="faq-answer">{a}</div></details>' for q, a in p["faq"])

    return f'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="robots" content="noindex,nofollow,noarchive">
  <meta name="content-language" content="ar">
  <title>{title}</title>
  <meta name="description" content="{p['description']}">
  <link rel="canonical" href="{live_ar}">
  <meta property="og:type" content="website"><meta property="og:site_name" content="Silwadi Dental Center"><meta property="og:title" content="{title}"><meta property="og:description" content="{p['description']}"><meta property="og:url" content="{live_ar}"><meta property="og:image" content="https://silwadi.ae{p['hero_image']}"><meta property="og:locale" content="ar_AE"><meta property="og:locale:alternate" content="en_AE">
  <link rel="alternate" hreflang="en-AE" href="{live_en}"><link rel="alternate" hreflang="ar-AE" href="{live_ar}"><link rel="alternate" hreflang="x-default" href="{live_en}">
  <meta name="theme-color" content="#083847"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="../treatment-refresh-v1.css">
  <script type="application/ld+json" data-seo-schema>{ar_schema(p)}</script>
</head>
<body class="treatment-review language-ar" data-treatment-review>
  <div class="private-note"><div class="container"><span><strong>معاينة خاصة</strong> · تحديث صفحة العلاج</span><span>{p['label']} · غير منشورة</span></div></div>
  <header class="global-header"><div class="container global-header__inner"><a class="global-brand" href="/ar/" aria-label="الصفحة الرئيسية لمركز سلوادي"><img src="/assets/silwadi-logo-official.png" alt="مركز سلوادي لطب الأسنان" width="180" height="180"></a><nav class="global-nav" aria-label="التنقل الرئيسي"><a href="/ar/services.html">الخدمات</a><a href="/ar/doctors.html">الأطباء</a><a href="/ar/about.html">عن المركز</a><a href="/ar/locations.html">الفروع</a></nav><div class="global-actions"><a class="language-switch" href="../{name}" lang="en" dir="ltr">English</a><a class="global-whatsapp" href="https://wa.me/971506260418" target="_blank" rel="noopener">واتساب</a><a class="global-book" href="/ar/contact.html#consultation-form">احجز موعدًا</a></div><button class="global-menu-button" type="button" data-menu-button aria-expanded="false" aria-controls="reviewMobileNav" aria-label="فتح القائمة"><span></span><span></span></button></div></header>
  <div class="global-mobile-nav" id="reviewMobileNav" data-mobile-nav><div class="container global-mobile-nav__inner"><a href="/ar/services.html">الخدمات</a><a href="/ar/doctors.html">الأطباء</a><a href="/ar/about.html">عن المركز</a><a href="/ar/locations.html">الفروع</a><div class="global-mobile-nav__actions"><a class="language-switch language-switch--mobile" href="../{name}" lang="en" dir="ltr">English</a><a href="/ar/contact.html#consultation-form">احجز</a></div></div></div>
  <nav class="treatment-subnav" aria-label="أقسام صفحة {p['label']}"><div class="container treatment-subnav__inner"><span class="treatment-subnav__label">{p['label']}</span><div class="treatment-subnav__links"><a href="#overview">نظرة عامة</a><a href="#options">العلاج</a><a href="#process">الخطوات</a><a href="#team">الأطباء</a><a href="#faq">الأسئلة الشائعة</a></div></div></nav>
<main>
  <section class="hero"><div class="container"><nav class="breadcrumb" aria-label="مسار الصفحة"><a href="/ar/">الرئيسية</a><span>/</span><a href="/ar/treatments.html">العلاجات</a><span>/</span><strong>{p['label']}</strong></nav><div class="hero-grid"><div class="hero-copy"><p class="eyebrow">{p['eyebrow']}</p><h1>{p['h1']} <span>أبوظبي</span></h1><p class="lead">{p['lead']}</p>{hero_actions}<div class="trust-row">{trust}</div></div><div class="hero-visual"><img class="hero-visual__image" src="{p['hero_image']}" alt="{p['label']} في مركز سلوادي لطب الأسنان" fetchpriority="high"><div class="visual-note"><strong>{p['visual'][0]}</strong><span>{p['visual'][1]}</span></div></div></div></div></section>
  <section class="section" id="overview"><div class="container"><div class="section-head"><p class="eyebrow">متى تحتاج إلى التقييم؟</p><h2>{p['overview_title']}</h2><p>{p['overview_intro']}</p></div><div class="signal-grid">{cards(p['signals'], 'signal-card')}</div><p class="section-note">هذه المعلومات عامة ولا تغني عن التقييم السريري. يحدد طبيب الأسنان أو الاختصاصي الخطة المناسبة بعد فحص الحالة.</p></div></section>
  <section class="section section-soft" id="options"><div class="container"><div class="section-head"><p class="eyebrow">العلاج</p><h2>{p['options_title']}</h2><p>{p['options_intro']}</p></div><div class="treatment-grid">{cards(p['options'], 'treatment-card')}</div></div></section>
  <section class="section" id="process"><div class="container"><div class="section-head"><p class="eyebrow">مسار الرعاية</p><h2>{p['process_title']}</h2><p>{p['process_intro']}</p></div><div class="process-wrap"><div class="process-line" aria-hidden="true"></div><div class="process-grid">{process}</div></div></div></section>
  <section class="approach-band"><div class="container approach-grid"><div><p class="eyebrow" style="color:#8fd5de">نهجنا في الرعاية</p><h2>{p['approach'][0]}</h2></div><div><p>{p['approach'][1]}</p><div class="approach-points">{points}</div></div></div></section>
  <section class="section section-soft" id="team"><div class="container"><div class="section-head"><p class="eyebrow">الفريق السريري</p><h2>الأطباء المرتبطون بهذه الرعاية</h2><p>يعتمد الطبيب المناسب على الحالة والفرع والتوفر السريري. يمكنك مراجعة ملف كل طبيب لمزيد من التفاصيل.</p></div><div class="doctor-grid">{doctor_cards(p['doctors'])}</div></div></section>
  <section class="section" id="faq"><div class="container"><div class="section-head"><p class="eyebrow">الأسئلة الشائعة</p><h2>أسئلة شائعة حول {p['label']}</h2><p>إجابات مختصرة للمعلومات العامة، ويمكن للطبيب توضيح ما ينطبق على حالتك.</p></div><div class="faq-list">{faq}</div></div></section>
  <section class="cta-section"><div class="container"><div class="cta-box"><div><h2>{p['cta'][0]}</h2><p>{p['cta'][1]}</p></div>{cta_actions}</div></div></section>
</main>
<footer class="review-footer"><div class="container review-footer__inner"><span>معاينة خاصة لصفحة العلاج · غير مرتبطة بالموقع العام</span><a href="/ar/treatments/endodontics.html">العودة إلى صفحات العلاج</a></div></footer>
<script src="../treatment-refresh-v1.js"></script>
</body></html>'''


def write_arabic_pages() -> None:
    AR_REVIEW.mkdir(parents=True, exist_ok=True)
    for name, page in AR_PAGES.items():
        (AR_REVIEW / name).write_text(ar_page(name, page), encoding="utf-8")


def polish_css() -> None:
    path = REVIEW / "treatment-refresh-v1.css"
    text = path.read_text(encoding="utf-8")
    marker = "/* TREATMENT-REVIEW-POLISH-V2 */"
    if marker in text:
        text = text.split(marker, 1)[0].rstrip() + "\n"
    additions = r'''
/* TREATMENT-REVIEW-POLISH-V2 */
.language-switch{height:42px;padding:0 13px;border:1px solid #cbdadd;border-radius:5px;background:#fff;color:var(--navy);display:inline-flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;white-space:nowrap}
.language-switch:hover{border-color:#9bbbc1;color:var(--teal)}
.doctor-card__photo img.doctor-crop-hani{object-position:50% 16%}
.doctor-card__photo img.doctor-crop-moammar{object-position:50% 14%}
.doctor-card__photo img.doctor-crop-krish{object-position:50% 8%;transform:scale(1.14)}
.doctor-card__photo img.doctor-crop-munir{object-position:50% 14%}
.doctor-card__photo img.doctor-crop-fahed{object-position:50% 7%;transform:scale(1.18)}
.doctor-card__photo img.doctor-crop-moheb{object-position:50% 14%}
.doctor-card__photo img.doctor-crop-dana{object-position:50% 14%}
.doctor-card__photo img.doctor-crop-afnan{object-position:50% 9%;transform:scale(1.12)}
.doctor-card__photo img.doctor-crop-ahmed{object-position:50% 16%}
.doctor-card__photo img.doctor-crop-lana{object-position:50% 18%}
.doctor-card:hover .doctor-card__photo img.doctor-crop-krish{transform:scale(1.155)}
.doctor-card:hover .doctor-card__photo img.doctor-crop-fahed{transform:scale(1.195)}
.doctor-card:hover .doctor-card__photo img.doctor-crop-afnan{transform:scale(1.135)}
[dir="rtl"] body{font-family:Tahoma,"Segoe UI",Arial,sans-serif}
[dir="rtl"] .global-nav{margin-left:0;margin-right:auto}
[dir="rtl"] .treatment-subnav__label{padding-right:0;padding-left:18px;border-right:0;border-left:1px solid var(--line)}
[dir="rtl"] .breadcrumb,[dir="rtl"] .trust-row,[dir="rtl"] .hero-actions,[dir="rtl"] .global-actions{direction:rtl}
[dir="rtl"] .section-head,[dir="rtl"] .process-step,[dir="rtl"] .doctor-card__body,[dir="rtl"] .cta-box{text-align:right}
[dir="rtl"] .faq-list summary{text-align:right}
[dir="rtl"] .faq-answer{padding:0 2px 24px 50px;text-align:right}
[dir="rtl"] .doctor-card__link span{display:inline-block;transform:none}
[dir="rtl"] .cta-actions{justify-content:flex-start}
@media(max-width:760px){
  [dir="rtl"] .section-head{text-align:right}
  [dir="rtl"] .process-grid,[dir="rtl"] .process-step{text-align:right}
  [dir="rtl"] .process-step{grid-template-columns:1fr 54px}
  [dir="rtl"] .process-step__dot{grid-column:2;grid-row:1/3}
  [dir="rtl"] .process-step h3,[dir="rtl"] .process-step p{grid-column:1}
  [dir="rtl"] .process-step p{margin:6px 0 0}
  [dir="rtl"] .faq-answer{padding-left:40px;padding-right:0}
  .language-switch--mobile{width:100%;height:auto}
}
'''
    path.write_text(text + additions, encoding="utf-8")


def main() -> None:
    polish_english_pages()
    write_arabic_pages()
    polish_css()


if __name__ == "__main__":
    main()
