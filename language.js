(function attachSilwadiLanguage(root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  root.SilwadiLanguage = api;
})(typeof window !== 'undefined' ? window : globalThis, function createSilwadiLanguage() {
  const STORAGE_KEY = 'silwadi-language';
  const textOriginals = typeof WeakMap === 'function' ? new WeakMap() : null;
  const attributeOriginals = typeof WeakMap === 'function' ? new WeakMap() : null;
  let currentLanguage = 'en';
  let languageButton = null;
  const seoOriginals = {
    title: null,
    description: null,
    ogTitle: null,
    ogDescription: null,
    ogLocale: null,
    ogLocaleAlternate: null,
  };

  const arabic = {
    'Skip to content': 'انتقل إلى المحتوى',
    'Home': 'الرئيسية',
    'Services': 'الخدمات',
    'Doctors': 'الأطباء',
    'About': 'عن المركز',
    'Locations': 'الفروع',
    'Contact': 'تواصل معنا',
    'Centre': 'المركز',
    'Care': 'الرعاية',
    'Treatments': 'العلاجات',
    'Treatment information': 'معلومات العلاج',
    'Dental services': 'خدمات طب الأسنان',
    'Choose the care you need': 'اختر الرعاية التي تحتاجها',
    'View all services': 'عرض جميع الخدمات',
    'Book a Consultation': 'احجز استشارة',
    'Request a Consultation': 'اطلب استشارة',
    'Request a consultation': 'اطلب استشارة',
    'Book': 'احجز',
    'Call': 'اتصل',
    'Call Us': 'اتصل بنا',
    'Call the Centre': 'اتصل بالمركز',
    'Call the centre': 'اتصل بالمركز',
    'WhatsApp': 'واتساب',
    'Chat on WhatsApp': 'تواصل عبر واتساب',
    'Find a Doctor': 'ابحث عن طبيب',
    'Find a Doctor →': 'ابحث عن طبيب ←',
    'Medical team': 'الفريق الطبي',
    'Dr. Afnan Mashal': 'د. أفنان مشعل',
    'Dr. Moheb Silwadi': 'د. مهيب سلوادي',
    'Dr. Ehab Hassouneh Bassam A': 'د. إيهاب حسونة بسام',
    'Dr. Sara Ismail': 'د. سارة إسماعيل',
    'Dr. Nasr Keshkiea': 'د. نصر كشكية',
    'Dr. Dana Awad': 'د. دانا عوض',
    'Dr. Munir Silwadi': 'د. منير سلوادي',
    'Dr. Ahmed El Shehri': 'د. أحمد الشهري',
    'Dr. Fahed Abi Khalil': 'د. فهد أبي خليل',
    'Dr. Moammar Mohamed Rifai': 'د. معمر محمد الرفاعي',
    'Dr. Hani Hasbini': 'د. هاني حسبيني',
    'Dr. Krishnamurthy Balajee': 'د. كريشنامورثي بالاجي',
    'Dr. Kashmira Pawar Jayprakash': 'د. كاشميرا باوار جايبراكاش',
    'Dr. Nachiket Shah': 'د. ناشيكيت شاه',
    'Dr. Lana Masoud': 'د. لانا مسعود',
    'Our team': 'فريقنا',
    'Our doctors': 'أطباؤنا',
    'Meet the team': 'تعرّف إلى الفريق',
    'Meet the medical team': 'تعرّف إلى الفريق الطبي',
    'Meet the full medical team': 'تعرّف إلى جميع أفراد الفريق الطبي',
    'View medical team': 'عرض الفريق الطبي',
    'View profile': 'عرض الملف',
    'View all doctors': 'عرض جميع الأطباء',
    'Browse all dentists & specialists →': 'تصفّح جميع أطباء الأسنان والاختصاصيين ←',
    'Search doctors': 'ابحث عن طبيب',
    'Name or specialty': 'الاسم أو التخصص',
    'All': 'الكل',
    'Specialty': 'التخصص',
    'General Dentist': 'طبيب أسنان عام',
    'General Dentistry': 'طب الأسنان العام',
    'General dentistry': 'طب الأسنان العام',
    'Orthodontics': 'تقويم الأسنان',
    'Specialist Orthodontics': 'اختصاصي تقويم أسنان',
    'Specialist Orthodontist': 'اختصاصي تقويم أسنان',
    'Orthodontist': 'اختصاصي تقويم أسنان',
    'Consultant Orthodontist': 'استشاري تقويم أسنان',
    'Consultant Orthodontics': 'استشاري تقويم أسنان',
    'Periodontics': 'أمراض اللثة',
    'Specialist Periodontics': 'اختصاصي أمراض اللثة',
    'Specialist Periodontist': 'اختصاصي أمراض اللثة',
    'Periodontist & Implantologist': 'اختصاصي أمراض اللثة وزراعة الأسنان',
    'Endodontics': 'علاج جذور الأسنان',
    'Specialist Endodontics': 'اختصاصي علاج جذور الأسنان',
    'Endodontist': 'اختصاصي علاج جذور الأسنان',
    'Prosthodontics': 'تركيبات الأسنان',
    'Prosthodontics & Implantology': 'تركيبات وزراعة الأسنان',
    'Specialist Prosthodontist': 'اختصاصي تركيبات أسنان',
    'Specialist Prosthodontist & Implantologist': 'اختصاصي تركيبات وزراعة الأسنان',
    'Pediatric Dentist': 'اختصاصي طب أسنان الأطفال',
    'Pediatric Dentistry': 'طب أسنان الأطفال',
    'Pedodontics': 'طب أسنان الأطفال',
    'Cosmetics': 'تجميل الأسنان',
    'Cosmetic Dentistry': 'طب الأسنان التجميلي',
    'Teeth Whitening': 'تبييض الأسنان',
    'Laser Dentistry': 'طب الأسنان بالليزر',
    'Preventive Dentistry': 'طب الأسنان الوقائي',
    'Preventive Treatments': 'العلاجات الوقائية',
    'Preventive dentistry': 'طب الأسنان الوقائي',
    'Restore & replace teeth': 'ترميم الأسنان وتعويض المفقود منها',
    'Gum & supporting tissue care': 'العناية باللثة والأنسجة الداعمة',
    'Root canal & pulp care': 'علاج الجذور ولب الأسنان',
    'Alignment & bite correction': 'تصحيح اصطفاف الأسنان والإطباق',
    'Dental care for children': 'العناية بأسنان الأطفال',
    'Smile aesthetics': 'تجميل الابتسامة',
    'Professional whitening': 'تبييض احترافي',
    'Laser-assisted procedures': 'إجراءات علاجية بمساعدة الليزر',
    'Routine & preventive care': 'رعاية دورية ووقائية',
    'Specialist care for braces, aligners, tooth alignment and bite correction.': 'رعاية تخصصية للتقويم والصفافات وتصحيح اصطفاف الأسنان والإطباق.',
    'Aesthetic dental care including whitening, veneers and restorative smile planning after assessment.': 'رعاية تجميلية تشمل التبييض والقشور والتخطيط الترميمي للابتسامة بعد التقييم.',
    'Routine examinations, preventive planning and care that supports ongoing oral health.': 'فحوصات دورية وتخطيط وقائي ورعاية تدعم صحة الفم المستمرة.',
    'Specialist care for the gums and supporting tissues around the teeth.': 'رعاية تخصصية للثة والأنسجة الداعمة المحيطة بالأسنان.',
    'Implants replace missing tooth roots; prosthodontic restorations rebuild the visible teeth and bite with crowns, bridges, dentures and implant-supported solutions.': 'تعوّض زراعة الأسنان جذور الأسنان المفقودة، بينما تعيد التركيبات بناء الأسنان الظاهرة والإطباق باستخدام التيجان والجسور والأطقم والحلول المدعومة بالزراعة.',
    'Root canal & pulp care': 'علاج الجذور ولب الأسنان',
    'Alignment & bite correction': 'تصحيح اصطفاف الأسنان والإطباق',
    'Gum & supporting tissue care': 'العناية باللثة والأنسجة الداعمة',
    'Dental care for children': 'العناية بأسنان الأطفال',
    'Smile aesthetics': 'تجميل الابتسامة',
    'Professional whitening': 'تبييض احترافي',
    'Laser-assisted procedures': 'إجراءات علاجية بمساعدة الليزر',
    'Routine & preventive care': 'رعاية دورية ووقائية',
    'Restore & replace teeth': 'ترميم الأسنان وتعويض المفقود منها',
    'No doctors match your current search. Try a different name or specialty.': 'لا يوجد أطباء مطابقون لبحثك الحالي. جرّب اسماً أو تخصصاً آخر.',
    'Not sure which dentist to choose?': 'لست متأكداً أي طبيب تختار؟',
    'Tell us what you need help with and reception can point you to the right dentist or specialist.': 'أخبر فريق الاستقبال بما تحتاج إليه وسنوجّهك إلى طبيب الأسنان أو الاختصاصي المناسب.',
    'Search our Abu Dhabi dental team by name or specialty.': 'ابحث في فريق أطباء الأسنان لدينا في أبوظبي حسب الاسم أو التخصص.',
    'One team. Multiple specialties.': 'فريق واحد بتخصصات متعددة.',
    '15 dentists and specialists across general and specialist dentistry.': '15 طبيباً واختصاصياً في طب الأسنان العام والتخصصي.',
    'Bani Yas Tower': 'برج بني ياس',
    'Al Raha Mall': 'الراحة مول',
    'Both locations': 'كلا الفرعين',
    'Corniche location': 'فرع الكورنيش',
    'Al Raha location': 'فرع الراحة',
    'Location': 'الموقع',
    'Location details': 'تفاصيل الموقع',
    'Our locations': 'فروعنا',
    'Two locations': 'فرعان',
    'Current location': 'الفرع الحالي',
    'Now open': 'مفتوح الآن',
    'Get Directions': 'عرض الاتجاهات',
    'Ask for directions': 'اطلب الاتجاهات',
    'Visit the centre': 'زر المركز',
    'Advanced dentistry.': 'طب أسنان متقدم.',
    'Established trust.': 'ثقة راسخة.',
    'Dental care in Abu Dhabi since 1980, with general dentists and specialists working together in one established centre.': 'رعاية أسنان في أبوظبي منذ عام 1980، يقدمها أطباء عامون واختصاصيون يعملون معاً ضمن مركز عريق.',
    'Since 1980': 'منذ عام 1980',
    'Established': 'تأسس',
    'Serving': 'نخدم',
    'since 1980.': 'منذ عام 1980.',
    'Dental care in': 'رعاية أسنان في',
    'Abu Dhabi': 'أبوظبي',
    'One established clinical team.': 'فريق سريري واحد متكامل.',
    '15 dentists & specialists': '15 طبيباً واختصاصياً',
    '15 dentists & specialists across two Abu Dhabi locations.': '15 طبيباً واختصاصياً في فرعين بأبوظبي.',
    'Explore Services': 'استكشف الخدمات',
    'Find the right care': 'اعثر على الرعاية المناسبة',
    'Insurance': 'التأمين',
    'Insurance accepted': 'نقبل التأمين',
    'Dental services at Silwadi.': 'خدمات طب الأسنان في سلوادي.',
    'Choose a treatment area, or contact us if you are not sure where to start.': 'اختر مجال العلاج، أو تواصل معنا إذا لم تكن متأكداً من أين تبدأ.',
    'Our story': 'قصتنا',
    'Serving Abu Dhabi since 1980.': 'نخدم أبوظبي منذ عام 1980.',
    'For more than four decades, Silwadi Dental Center has focused on patient-centred care, personalized treatment, comfort, patient education and open communication.': 'على مدى أكثر من أربعة عقود، ركّز مركز سلوادي لطب الأسنان على رعاية تتمحور حول المريض، وعلاج مخصص، وراحة المراجع، والتوعية الصحية، والتواصل الواضح.',
    'Learn more about the centre': 'اعرف المزيد عن المركز',
    'Specialist expertise. Personal care.': 'خبرة تخصصية ورعاية شخصية.',
    'Meet some of our dentists and specialists, or browse the full team by specialty.': 'تعرّف إلى عدد من أطبائنا واختصاصيينا، أو تصفّح الفريق كاملاً حسب التخصص.',
    'Consultations': 'الاستشارات',
    'Not sure which dentist you need?': 'لست متأكداً أي طبيب تحتاج؟',
    'Tell our team what you need help with and we can guide you toward the appropriate clinician.': 'أخبر فريقنا بما تحتاج إليه وسنوجّهك إلى الطبيب المناسب.',
    'What patients say about Silwadi.': 'ماذا يقول المرضى عن سلوادي؟',
    'Google reviews': 'تقييمات Google',
    'Google review': 'تقييم على Google',
    'Open patient review': 'فتح تقييم المريض',
    'Close review': 'إغلاق التقييم',
    '5 out of 5 stars': '5 من 5 نجوم',
    '4.6 out of 5 stars': '4.6 من 5 نجوم',
    'Read Silwadi reviews on Google Maps': 'اقرأ تقييمات سلوادي على خرائط Google',
    'Read all reviews →': 'اقرأ جميع التقييمات ←',
    'Tap to read': 'اضغط للقراءة',
    'Read reviews on Google Maps →': 'اقرأ التقييمات على خرائط Google ←',
    'Recent public review highlights for the Bani Yas Tower location. Read the full reviews on Google Maps.': 'أبرز التقييمات العامة الحديثة لفرع برج بني ياس. اقرأ التقييمات كاملةً على خرائط Google.',
    'Patient review': 'تقييم المريض',
    'Praised Dr. Krishna’s professionalism and experience, and described Invisalign treatment as smooth and comfortable.': 'أشاد باحترافية الدكتور كريشنا وخبرته، ووصف علاج إنفزلاين بأنه سلس ومريح.',
    'Highlighted a friendly, knowledgeable check-up and cleaning with Dr. Lujain, along with helpful reception staff.': 'أشاد بفحص وتنظيف ودّي ومتميز مع الدكتورة لجين، وبفريق استقبال متعاون.',
    'Shared a positive experience with professional cleaning and Dr. Lujain, noting the clinic was clean and the visit well organized.': 'شارك تجربة إيجابية مع التنظيف الاحترافي والدكتورة لجين، مشيراً إلى نظافة العيادة وحسن تنظيم الزيارة.',
    'Described one of her best dental experiences and praised Dr. Moheb’s calm, patient manner and the quality of his work.': 'وصفت التجربة بأنها من أفضل تجاربها في طب الأسنان، وأشادت بهدوء الدكتور مهيب وصبره وجودة عمله.',
    'Praised the professional work and friendly staff, with a special mention for Aliyah.': 'أشاد بالعمل الاحترافي وفريق العمل الودود، وخصّ عليّة بالذكر.',
    'Need urgent dental care?': 'هل تحتاج إلى رعاية أسنان عاجلة؟',
    'Call or view urgent care →': 'اتصل بنا أو اطّلع على الرعاية العاجلة ←',
    'Bani Yas Tower + Al Raha Mall': 'برج بني ياس + الراحة مول',
    'Dental care in Abu Dhabi.': 'رعاية أسنان في أبوظبي.',
    'Silwadi welcomes patients at Bani Yas Tower and Al Raha Mall.': 'يستقبل مركز سلوادي المرضى في برج بني ياس والراحة مول.',
    'About Silwadi': 'عن سلوادي',
    'The Silwadi story': 'قصة سلوادي',
    'How Silwadi approaches care': 'نهج سلوادي في تقديم الرعاية',
    'Patient contact': 'التواصل مع المرضى',
    'Clear explanations and care built around the patient.': 'شرح واضح ورعاية تتمحور حول المريض.',
    'Team-based care': 'رعاية يقدمها فريق متكامل',
    'A multi-specialty dental team': 'فريق أسنان متعدد التخصصات',
    'Contact & Consultations': 'التواصل والاستشارات',
    'Choose how you would like to contact the centre.': 'اختر الطريقة التي تفضلها للتواصل مع المركز.',
    'Message us on WhatsApp': 'راسلنا عبر واتساب',
    'Open WhatsApp →': 'فتح واتساب ←',
    'ONLINE FORM': 'نموذج إلكتروني',
    'Appointment request': 'طلب موعد',
    'Tell us how we can help.': 'أخبرنا كيف يمكننا مساعدتك.',
    'Your request will open in your email app addressed to the appointments team. They will confirm availability and guide you to the right clinician.': 'سيفتح طلبك في تطبيق البريد الإلكتروني موجهاً إلى فريق المواعيد. سيؤكد الفريق التوافر ويوجهك إلى الطبيب المناسب.',
    'Name': 'الاسم',
    'Phone number': 'رقم الهاتف',
    'Subject': 'الموضوع',
    'How can we help?': 'كيف يمكننا مساعدتك؟',
    'Send appointment request': 'إرسال طلب الموعد',
    'Your email app is opening with the appointment request.': 'يفتح تطبيق البريد الإلكتروني الآن مع طلب الموعد.',
    'Phone': 'الهاتف',
    'Email': 'البريد الإلكتروني',
    'Appointments': 'المواعيد',
    'Insurance enquiries': 'استفسارات التأمين',
    'Before your visit': 'قبل زيارتك',
    'Opening hours': 'ساعات العمل',
    'Sunday - Wednesday': 'الأحد - الأربعاء',
    'Thursday & Saturday': 'الخميس والسبت',
    'Friday: Closed': 'الجمعة: مغلق',
    'Address': 'العنوان',
    'Parking': 'مواقف السيارات',
    'General and specialist dental care across ten established service areas.': 'رعاية أسنان عامة وتخصصية ضمن عشرة مجالات علاجية متكاملة.',
    'Find the care you are looking for.': 'اعثر على الرعاية التي تبحث عنها.',
    'What we do': 'خدماتنا',
    'What to expect': 'ما الذي تتوقعه',
    'Assessment': 'التقييم',
    'Planning your treatment': 'تخطيط العلاج',
    'Frequently asked questions': 'الأسئلة الشائعة',
    'Common questions': 'أسئلة شائعة',
    'Clinical focus': 'مجالات الاهتمام السريري',
    'Qualifications': 'المؤهلات',
    'Qualifications & professional credentials': 'المؤهلات والاعتمادات المهنية',
    'Education & professional background': 'الخلفية الأكاديمية والمهنية',
    'Academic & Professional Background': 'الخلفية الأكاديمية والمهنية',
    'Areas of Expertise': 'مجالات الخبرة',
    'Philosophy of Care': 'فلسفة الرعاية',
    'Preventive & Periodontal Care': 'الرعاية الوقائية ورعاية اللثة',
    'Restorative Dentistry': 'طب الأسنان الترميمي',
    'Esthetic Dentistry': 'طب الأسنان التجميلي',
    'Comprehensive General Dentistry': 'طب الأسنان العام الشامل',
    'Dr. Dana earned her Bachelor of Dental Surgery (BDS) from Istanbul Medipol University and completed her comprehensive clinical residency at the University of Sharjah, gaining experience across a broad range of general dental procedures and patient care. With a particular interest in esthetic dentistry, she further advanced her training by completing a Diploma in Esthetic Dentistry from Mastery Dental Academy in Dubai.': 'حصلت الدكتورة دانا على بكالوريوس جراحة الأسنان من جامعة إسطنبول ميديبول، وأكملت إقامتها السريرية الشاملة في جامعة الشارقة، حيث اكتسبت خبرة في مجموعة واسعة من إجراءات طب الأسنان العام ورعاية المرضى. ونظراً لاهتمامها الخاص بطب الأسنان التجميلي، واصلت تطوير مهاراتها بحصولها على دبلوم في طب الأسنان التجميلي من أكاديمية ماستري لطب الأسنان في دبي.',
    'Dr. Dana believes that excellent dentistry combines clinical precision with clear communication and patient comfort. She takes a personalized approach to treatment, ensuring that patients understand their oral health needs and feel confident throughout their dental journey.': 'تؤمن الدكتورة دانا بأن طب الأسنان المتميز يجمع بين الدقة السريرية والتواصل الواضح وراحة المريض. وتتبع نهجاً علاجياً مخصصاً لكل مريض، بما يضمن فهمه لاحتياجات صحة فمه وشعوره بالثقة والاطمئنان طوال رحلة العلاج.',
    'Contact reception to request an appointment with Dr. Dana Awad. The team can confirm availability and help route your enquiry.': 'تواصل مع الاستقبال لطلب موعد مع الدكتورة دانا عوض. سيساعدك الفريق في التأكد من المواعيد المتاحة وتوجيه استفسارك.',
    'Routine examinations, professional cleaning, and maintenance of healthy teeth and gums.': 'الفحوصات الدورية والتنظيف الاحترافي والمحافظة على صحة الأسنان واللثة.',
    'Conservative management of dental caries and restoration of tooth structure and function.': 'العلاج المحافظ لتسوس الأسنان واستعادة بنية السن ووظيفته.',
    'Improving smile appearance through natural-looking, minimally invasive treatments.': 'تحسين مظهر الابتسامة بعلاجات طبيعية المظهر وقليلة التدخل.',
    'Diagnosis, treatment planning, and management of common dental conditions with a patient-centered approach.': 'تشخيص الحالات الشائعة وتخطيط علاجها وإدارتها بأسلوب يضع المريض في صميم الرعاية.',
    'General dental care and treatment planning.': 'رعاية الأسنان العامة وتخطيط العلاج.',
    'General dental care and patient-centred treatment planning.': 'رعاية الأسنان العامة وتخطيط علاجي يتمحور حول المريض.',
    'General dental care and routine treatment planning.': 'رعاية الأسنان العامة وتخطيط العلاجات الروتينية.',
    'Preventive, restorative and esthetic dentistry with patient-centred care.': 'طب الأسنان الوقائي والترميمي والتجميلي ضمن رعاية تتمحور حول المريض.',
    'Implantology, full-mouth rehabilitation and CAD/CAM aesthetic dentistry.': 'زراعة الأسنان وإعادة تأهيل الفم الكامل وطب الأسنان التجميلي بتقنيات CAD/CAM.',
    'Endodontic diagnosis and root canal care.': 'تشخيص حالات جذور الأسنان وعلاج قنوات الجذر.',
    'Periodontal care, gum health and implantology.': 'رعاية اللثة والمحافظة على صحتها وزراعة الأسنان.',
    'Orthodontic care for alignment and bite correction.': 'رعاية تقويمية لتصحيح اصطفاف الأسنان والإطباق.',
    'Consultant-led orthodontic assessment and treatment.': 'تقييم وعلاج تقويم الأسنان بإشراف استشاري.',
    'Orthodontic care and treatment planning.': 'رعاية تقويم الأسنان وتخطيط العلاج.',
    'Dental care for children and adolescents.': 'رعاية أسنان الأطفال واليافعين.',
    'Related care': 'الرعاية ذات الصلة',
    'Related doctors': 'أطباء ذوو صلة',
    'Doctor profile': 'ملف الطبيب',
    'General dental care': 'رعاية أسنان عامة',
    'Preventive care': 'رعاية وقائية',
    'Restorative care': 'رعاية ترميمية',
    'Aesthetic dentistry': 'طب الأسنان التجميلي',
    'Comprehensive dentistry': 'طب أسنان شامل',
    'Expert care. Lasting smiles.': 'رعاية متخصصة وابتسامات تدوم.',
    'Established dental care in Abu Dhabi since 1980.': 'رعاية أسنان راسخة في أبوظبي منذ عام 1980.',
    'Insurance Enquiry': 'استفسار عن التأمين',
    'View treatments': 'عرض العلاجات',
    'Explore services': 'استكشف الخدمات',
    'View all treatments': 'عرض جميع العلاجات',
    'View the full dental team →': 'عرض الفريق الطبي كاملاً ←',
    'Talk to our team': 'تحدث مع فريقنا',
    'Speak with reception': 'تواصل مع الاستقبال',
    'Check availability': 'تحقق من المواعيد المتاحة',
    'Modern dentistry, with a human welcome.': 'طب أسنان حديث بترحيب إنساني.',
    'For more than four decades, Silwadi Dental Centre has cared for Abu Dhabi families through clear advice, specialist expertise and a calm, welcoming experience.': 'على مدى أكثر من أربعة عقود، قدّم مركز سلوادي لطب الأسنان الرعاية لعائلات أبوظبي من خلال نصائح واضحة وخبرة تخصصية وتجربة هادئة ترحّب بالجميع.',
    'Meet our doctors →': 'تعرّف إلى أطبائنا ←',
    'The Silwadi story': 'قصة سلوادي',
    'A centre built around trust.': 'مركز يقوم على الثقة.',
    'Silwadi began serving patients in Abu Dhabi in 1980. Today, general dentists and specialists work together across restorative, preventive, cosmetic and specialist care.': 'بدأ سلوادي خدمة المرضى في أبوظبي عام 1980. واليوم يعمل أطباء الأسنان العامون والاختصاصيون معاً في مجالات الرعاية الترميمية والوقائية والتجميلية والتخصصية.',
    'Every visit starts with listening, clear explanations and a treatment plan that makes sense for the patient.': 'تبدأ كل زيارة بالاستماع والشرح الواضح وخطة علاج مناسبة للمريض.',
    'Talk to our team →': 'تحدث مع فريقنا ←',
    'One team, working together around the patient.': 'فريق واحد يعمل معاً حول احتياجات المريض.',
    'Designed for real life': 'مصمم لاحتياجات الحياة اليومية',
    'Care that feels considered.': 'رعاية مدروسة بعناية.',
    'Our clinic profile reflects a centre designed for comfortable care across generations, with dedicated support for children and People of Determination.': 'يعكس ملف المركز التعريفي مركزاً مصمماً لتقديم رعاية مريحة لجميع أفراد الأسرة، مع دعم مخصص للأطفال وأصحاب الهمم.',
    'A dedicated children’s zone helps young patients and families feel more at ease from the moment they arrive.': 'تساعد منطقة الأطفال المخصصة المرضى الصغار وعائلاتهم على الشعور براحة أكبر منذ لحظة وصولهم.',
    'Explore children’s care →': 'استكشف رعاية الأطفال ←',
    'Three dedicated rooms and an accessible layout support People of Determination with dignity and comfort.': 'تدعم ثلاث غرف مخصصة وتصميم ميسّر أصحاب الهمم بما يحفظ كرامتهم وراحتهم.',
    'Plan your visit →': 'خطط لزيارتك ←',
    'Digital X-rays, CAD/CAM, 3D printing, laser dentistry and intraoral imaging support careful planning.': 'تدعم الأشعة الرقمية وتقنيات CAD/CAM والطباعة ثلاثية الأبعاد وطب الأسنان بالليزر والتصوير داخل الفم التخطيط الدقيق.',
    'See our services →': 'اطّلع على خدماتنا ←',
    'Inside Silwadi': 'داخل سلوادي',
    'A welcoming place to begin.': 'مكان ترحيبي لبدء رحلتك.',
    'From the front desk to the clinical team, our centre is designed to make every step feel clear and comfortable.': 'من الاستقبال إلى الفريق السريري، صُمم مركزنا لتكون كل خطوة واضحة ومريحة.',
    'Our clinical team': 'فريقنا السريري',
    'One connected team': 'فريق واحد متكامل',
    'Care, planned together': 'رعاية نخطط لها معاً',
    'Two locations in Abu Dhabi.': 'فرعان في أبوظبي.',
    'Visit us at Bani Yas Tower or Al Raha Mall. Our team can help you choose the right appointment.': 'زورونا في برج بني ياس أو الراحة مول. يساعدك فريقنا في اختيار الموعد المناسب.',
    'Care for every patient': 'رعاية لكل مريض',
    'Thoughtful spaces, modern tools and a welcoming team.': 'مساحات مدروسة وتقنيات حديثة وفريق يرحّب بالجميع.',
    'Our published clinic profile describes a centre designed for comfortable care across generations, with dedicated support for children and People of Determination.': 'يوضح الملف التعريفي المنشور للمركز أنه مصمم لتقديم رعاية مريحة لجميع أفراد الأسرة، مع دعم مخصص للأطفال وأصحاب الهمم.',
    'Children’s dentistry': 'طب أسنان الأطفال',
    'A dedicated children’s zone creates a calmer, more familiar environment for young patients and families.': 'توفر منطقة الأطفال بيئة أكثر هدوءاً وألفةً للمرضى الصغار وعائلاتهم.',
    'Accessible care': 'رعاية ميسّرة',
    'Three dedicated rooms and an accessible layout support People of Determination with dignity and comfort.': 'تدعم ثلاث غرف مخصصة وتصميم ميسّر أصحاب الهمم بما يحفظ كرامتهم وراحتهم.',
    'Digital dentistry': 'طب الأسنان الرقمي',
    'Digital X-rays, CAD/CAM, 3D printing, laser dentistry and intraoral imaging support careful treatment planning.': 'تدعم الأشعة الرقمية وتقنيات CAD/CAM والطباعة ثلاثية الأبعاد وطب الأسنان بالليزر والتصوير داخل الفم تخطيط العلاج بدقة.',
  };

  const normalize = value => String(value ?? '').replace(/\s+/g, ' ').trim();

  const arabicSeo = {
    'index.html': {
      title: 'طبيب أسنان في أبوظبي | مركز الدكتور منير السلوادي لطب الأسنان',
      description: 'رعاية أسنان عامة وتخصصية في أبوظبي لدى مركز الدكتور منير السلوادي لطب الأسنان، في برج بني ياس والراحة مول، منذ عام 1980.',
    },
    'services.html': {
      title: 'خدمات طب الأسنان في أبوظبي | مركز سلوادي لطب الأسنان',
      description: 'تعرّف إلى خدمات طب الأسنان في مركز سلوادي بأبوظبي، من زراعة وتركيبات الأسنان إلى التقويم وعلاج اللثة والجذور ورعاية الأطفال والوقاية.',
    },
    'treatments.html': {
      title: 'علاجات الأسنان في أبوظبي | مركز سلوادي لطب الأسنان',
      description: 'استكشف مجالات علاج الأسنان في مركز سلوادي بأبوظبي، أو تواصل مع فريق الاستقبال لمساعدتك في اختيار نقطة البداية المناسبة.',
    },
    'doctors.html': {
      title: 'أطباء الأسنان والاختصاصيون في أبوظبي | سلوادي',
      description: 'تعرّف إلى أطباء الأسنان والاختصاصيين في مركز سلوادي بأبوظبي ضمن تخصصات التقويم واللثة والجذور والتركيبات وطب الأسنان العام.',
    },
    'about.html': {
      title: 'عن مركز سلوادي لطب الأسنان في أبوظبي | منذ 1980',
      description: 'تعرّف إلى قصة مركز سلوادي لطب الأسنان في أبوظبي، الذي يقدّم رعاية عامة وتخصصية للعائلات منذ عام 1980.',
    },
    'locations.html': {
      title: 'فروع عيادات الأسنان في أبوظبي | بني ياس والراحة | سلوادي',
      description: 'اعثر على تفاصيل فرعي مركز سلوادي لطب الأسنان في برج بني ياس والراحة مول بأبوظبي، بما في ذلك أرقام التواصل والاتجاهات.',
    },
    'contact.html': {
      title: 'تواصل مع مركز سلوادي لطب الأسنان في أبوظبي | فرعان',
      description: 'تواصل مع مركز سلوادي لطب الأسنان في أبوظبي لحجز موعد أو الاستفسار عن فرعي برج بني ياس والراحة مول والتأمين.',
    },
    'dr-afnan-mashal.html': {
      title: 'د. أفنان مشعل | طبيب أسنان عام في أبوظبي | مركز سلوادي لطب الأسنان',
      description: 'تعرّف إلى د. أفنان مشعل، طبيب أسنان عام في مركز سلوادي بأبوظبي، واطّلع على مجالات اهتمامه وبيانات الملف وطلب الموعد.',
    },
    'dr-ahmed-el-shehri.html': {
      title: 'د. أحمد الشهري | اختصاصي علاج الجذور في أبوظبي | مركز سلوادي',
      description: 'تعرّف إلى د. أحمد الشهري، اختصاصي علاج الجذور في مركز سلوادي بأبوظبي، واطّلع على مجالات اهتمامه وتفاصيل الاستشارة.',
    },
    'dr-dana-awad.html': {
      title: 'د. دانا عوض | طبيبة أسنان عامة في أبوظبي | مركز سلوادي',
      description: 'تعرّف إلى د. دانا عوض، طبيبة أسنان عامة في مركز سلوادي بأبوظبي، مع اهتمام بالوقاية والترميم وطب الأسنان التجميلي.',
    },
    'dr-ehab-hassouneh.html': {
      title: 'د. إيهاب حسونة بسام | طبيب أسنان عام في أبوظبي | مركز سلوادي',
      description: 'تعرّف إلى د. إيهاب حسونة بسام، طبيب أسنان عام في مركز سلوادي بأبوظبي، واطّلع على مجالات الرعاية ومعلومات الموعد.',
    },
    'dr-fahed-khalil.html': {
      title: 'د. فهد أبي خليل | اختصاصي أمراض اللثة وزراعة الأسنان في أبوظبي | سلوادي',
      description: 'تعرّف إلى د. فهد أبي خليل، اختصاصي أمراض اللثة وزراعة الأسنان في مركز سلوادي بأبوظبي، واطّلع على تفاصيل الاستشارة.',
    },
    'dr-hani-hasbini.html': {
      title: 'د. هاني حسبيني | استشاري تقويم الأسنان في أبوظبي | مركز سلوادي',
      description: 'تعرّف إلى د. هاني حسبيني، استشاري تقويم الأسنان في مركز سلوادي بأبوظبي، واطّلع على مجالات اهتمامه وتفاصيل الموعد.',
    },
    'dr-kashmira-pawar-jayprakash.html': {
      title: 'د. كاشميرا باوار جايبراكاش | اختصاصية طب أسنان الأطفال في أبوظبي | سلوادي',
      description: 'تعرّف إلى د. كاشميرا باوار جايبراكاش، اختصاصية طب أسنان الأطفال في مركز سلوادي بأبوظبي، واطّلع على معلومات الملف والموعد.',
    },
    'dr-krishnamurthy-katta-balajee.html': {
      title: 'د. كريشنامورثي بالاجي | اختصاصي تقويم الأسنان في أبوظبي | سلوادي',
      description: 'تعرّف إلى د. كريشنامورثي بالاجي، اختصاصي تقويم الأسنان في مركز سلوادي بأبوظبي، واطّلع على مجالات الرعاية وتفاصيل الاستشارة.',
    },
    'dr-lana-masoud.html': {
      title: 'د. لانا مسعود | اختصاصية علاج الجذور في أبوظبي | مركز سلوادي',
      description: 'تعرّف إلى د. لانا مسعود، اختصاصية علاج الجذور في مركز سلوادي بأبوظبي، واطّلع على مجالات الرعاية وتفاصيل الموعد.',
    },
    'dr-moammar-rifai.html': {
      title: 'د. معمر محمد الرفاعي | اختصاصي تقويم الأسنان في أبوظبي | سلوادي',
      description: 'تعرّف إلى د. معمر محمد الرفاعي، اختصاصي تقويم الأسنان في مركز سلوادي بأبوظبي، واطّلع على مجالات اهتمامه وتفاصيل الاستشارة.',
    },
    'dr-moheb-silwadi.html': {
      title: 'د. مهيب سلوادي | طبيب أسنان عام في أبوظبي | مركز سلوادي',
      description: 'تعرّف إلى د. مهيب سلوادي، طبيب أسنان عام في مركز سلوادي بأبوظبي، واطّلع على معلومات الملف وطلب الموعد.',
    },
    'dr-munir-silwadi.html': {
      title: 'د. منير سلوادي | اختصاصي التركيبات وزراعة الأسنان في أبوظبي | سلوادي',
      description: 'تعرّف إلى د. منير سلوادي، اختصاصي التركيبات وزراعة الأسنان في مركز سلوادي بأبوظبي، مع اهتمام بزراعة الأسنان والرعاية الترميمية.',
    },
    'dr-nachiket-shah.html': {
      title: 'د. ناشيكيت شاه | اختصاصي أمراض اللثة وزراعة الأسنان في أبوظبي | سلوادي',
      description: 'تعرّف إلى د. ناشيكيت شاه، اختصاصي أمراض اللثة وزراعة الأسنان في مركز سلوادي بأبوظبي، واطّلع على معلومات الاستشارة.',
    },
    'dr-nasr-keshkiea.html': {
      title: 'د. نصر كشكية | طبيب أسنان عام في أبوظبي | مركز سلوادي',
      description: 'تعرّف إلى د. نصر كشكية، طبيب أسنان عام في مركز سلوادي بأبوظبي، واطّلع على مجالات الرعاية وتفاصيل الموعد.',
    },
    'dr-sara-ismail.html': {
      title: 'د. سارة إسماعيل | طبيبة أسنان عامة في أبوظبي | مركز سلوادي',
      description: 'تعرّف إلى د. سارة إسماعيل، طبيبة أسنان عامة في مركز سلوادي بأبوظبي، واطّلع على مجالات الرعاية وتفاصيل الموعد.',
    },
    'cosmetic-dentistry.html': {
      title: 'طب الأسنان التجميلي في أبوظبي | مركز سلوادي لطب الأسنان',
      description: 'استكشف طب الأسنان التجميلي في أبوظبي، بما في ذلك القشور والتبييض وتخطيط الابتسامة الترميمي بعد التقييم السريري في مركز سلوادي.',
    },
    'dental-implants.html': {
      title: 'زراعة الأسنان في أبوظبي | مركز سلوادي لطب الأسنان',
      description: 'هل تفكر في زراعة الأسنان في أبوظبي؟ تعرّف إلى التقييم والتخطيط الرقمي والرعاية الترميمية في مركز سلوادي.',
    },
    'emergency-dentist.html': {
      title: 'طبيب أسنان للحالات الطارئة في أبوظبي | مركز سلوادي',
      description: 'تحتاج إلى رعاية أسنان عاجلة في أبوظبي؟ اتصل بمركز سلوادي لمعرفة المواعيد المتاحة وتقييم ألم الأسنان أو كسرها وغيرها من الحالات العاجلة.',
    },
    'general-dentistry.html': {
      title: 'طب الأسنان العام في أبوظبي | مركز سلوادي لطب الأسنان',
      description: 'رعاية أسنان عامة في أبوظبي للفحوصات والحشوات والوقاية والمشكلات اليومية في مركز سلوادي ببرج بني ياس.',
    },
    'orthodontics.html': {
      title: 'تقويم الأسنان والصفافات في أبوظبي | مركز سلوادي',
      description: 'رعاية تقويم الأسنان في أبوظبي للأطفال واليافعين والكبار، بما في ذلك التقويم والصفافات الشفافة بعد تقييم الاختصاصي في مركز سلوادي.',
    },
  };

  function pageKey() {
    const locationObject = typeof window !== 'undefined' ? window.location : null;
    const pathname = String(locationObject?.pathname || '').replace(/\/+/g, '/');
    const cleanPath = pathname.replace(/\/$/, '');
    const lastSegment = cleanPath ? cleanPath.split('/').pop() : '';
    return /\.html?$/i.test(lastSegment) ? lastSegment : 'index.html';
  }

  function locationHref() {
    const locationObject = typeof window !== 'undefined' ? window.location : null;
    return String(locationObject?.href || locationObject?.pathname || 'https://silwadi.ae/');
  }

  function getRequestedLanguage() {
    const locationObject = typeof window !== 'undefined' ? window.location : null;
    const search = String(locationObject?.search || '');
    const match = search.match(/[?&]lang=(ar|en)(?:&|$)/i);
    return match ? match[1].toLowerCase() : null;
  }

  function pageUrlObject(value) {
    try {
      return new URL(value, locationHref());
    } catch (_) {
      return null;
    }
  }

  function isPageUrl(url) {
    return Boolean(url && (url.pathname === '/' || /\.html?$/i.test(url.pathname)));
  }

  function withLanguageQuery(href, language) {
    const value = String(href || '');
    if (!value || value.startsWith('#') || /^(?:mailto:|tel:|javascript:|data:|blob:)/i.test(value)) return value;
    const url = pageUrlObject(value);
    const base = pageUrlObject(locationHref());
    if (!url || !base || url.origin !== base.origin || !isPageUrl(url)) return value;

    const hashIndex = value.indexOf('#');
    const hash = hashIndex === -1 ? '' : value.slice(hashIndex);
    const beforeHash = hashIndex === -1 ? value : value.slice(0, hashIndex);
    const pathEnd = beforeHash.indexOf('?');
    const rawPath = pathEnd === -1 ? beforeHash : beforeHash.slice(0, pathEnd);
    const params = url.searchParams;
    params.delete('lang');
    if (language === 'ar') params.set('lang', 'ar');
    const query = params.toString();
    return `${rawPath}${query ? `?${query}` : ''}${hash}`;
  }

  function historyUrl(language) {
    const url = pageUrlObject(locationHref());
    if (!url || !isPageUrl(url)) return null;
    url.searchParams.delete('lang');
    if (language === 'ar') url.searchParams.set('lang', 'ar');
    return `${url.pathname}${url.search}${url.hash}`;
  }

  function updateCurrentUrl(language) {
    const target = historyUrl(language);
    const locationObject = typeof window !== 'undefined' ? window.location : null;
    const historyObject = typeof window !== 'undefined' ? window.history : null;
    if (!target || !locationObject || !historyObject || typeof historyObject.replaceState !== 'function') return;
    const current = `${locationObject.pathname || ''}${locationObject.search || ''}${locationObject.hash || ''}`;
    if (target !== current) historyObject.replaceState({}, '', target);
  }

  function decorateInternalLinks(language) {
    if (typeof document === 'undefined') return;
    document.querySelectorAll?.('a[href]').forEach(link => {
      const href = link.getAttribute?.('href');
      if (!href) return;
      const next = withLanguageQuery(href, language);
      if (next !== href) link.setAttribute('href', next);
    });
  }

  function metaContent(selector) {
    const element = document.querySelector?.(selector);
    if (!element) return null;
    return element.getAttribute?.('content') ?? element.content ?? null;
  }

  function setMetaContent(selector, value, name) {
    if (typeof document === 'undefined' || value == null) return;
    let element = document.querySelector?.(selector);
    if (!element && name && document.createElement && document.head?.appendChild) {
      element = document.createElement('meta');
      element.setAttribute('name', name);
      document.head.appendChild(element);
    }
    if (!element) return;
    if ('content' in element) element.content = value;
    element.setAttribute?.('content', value);
  }

  function setMetaProperty(property, value) {
    if (typeof document === 'undefined' || value == null) return;
    const selector = `meta[property="${property}"]`;
    let element = document.querySelector?.(selector);
    if (!element && document.createElement && document.head?.appendChild) {
      element = document.createElement('meta');
      element.setAttribute('property', property);
      document.head.appendChild(element);
    }
    if (!element) return;
    if ('content' in element) element.content = value;
    element.setAttribute?.('content', value);
  }

  function captureSeoOriginals() {
    if (typeof document === 'undefined') return;
    if (seoOriginals.title === null) seoOriginals.title = document.title || '';
    if (seoOriginals.description === null) seoOriginals.description = metaContent('meta[name="description"]') || '';
    if (seoOriginals.ogTitle === null) seoOriginals.ogTitle = metaContent('meta[property="og:title"]') || '';
    if (seoOriginals.ogDescription === null) seoOriginals.ogDescription = metaContent('meta[property="og:description"]') || '';
    if (seoOriginals.ogLocale === null) seoOriginals.ogLocale = metaContent('meta[property="og:locale"]') || 'en_AE';
    if (seoOriginals.ogLocaleAlternate === null) seoOriginals.ogLocaleAlternate = metaContent('meta[property="og:locale:alternate"]') || 'ar_AE';
  }

  function canonicalUrl() {
    const canonical = document.querySelector?.('link[rel="canonical"]');
    const href = canonical?.getAttribute?.('href') || '';
    const url = pageUrlObject(href || locationHref());
    if (!url) return '';
    url.search = '';
    url.hash = '';
    return url.href;
  }

  function upsertAlternate(hreflang, href) {
    if (typeof document === 'undefined' || !document.head?.appendChild) return;
    const selector = `link[rel="alternate"][hreflang="${hreflang}"]`;
    let link = document.querySelector?.(selector);
    if (!link && document.createElement) {
      link = document.createElement('link');
      link.setAttribute('rel', 'alternate');
      link.setAttribute('hreflang', hreflang);
      document.head.appendChild(link);
    }
    link?.setAttribute?.('href', href);
  }

  function updateLocalizedSeo(language) {
    if (typeof document === 'undefined') return;
    captureSeoOriginals();
    const cleanCanonical = canonicalUrl();
    const translation = arabicSeo[pageKey()];
    if (language === 'ar') {
      const title = translation?.title || translate(seoOriginals.title, 'ar');
      const description = translation?.description || translate(seoOriginals.description, 'ar');
      document.title = title || seoOriginals.title;
      setMetaContent('meta[name="description"]', description || seoOriginals.description);
      setMetaContent('meta[property="og:title"]', title || seoOriginals.ogTitle);
      setMetaContent('meta[property="og:description"]', description || seoOriginals.ogDescription);
      setMetaContent('meta[name="content-language"]', 'ar', 'content-language');
      setMetaProperty('og:locale', 'ar_AE');
      setMetaProperty('og:locale:alternate', 'en_AE');
    } else {
      document.title = seoOriginals.title || document.title;
      setMetaContent('meta[name="description"]', seoOriginals.description);
      setMetaContent('meta[property="og:title"]', seoOriginals.ogTitle);
      setMetaContent('meta[property="og:description"]', seoOriginals.ogDescription);
      setMetaContent('meta[name="content-language"]', 'en', 'content-language');
      setMetaProperty('og:locale', seoOriginals.ogLocale || 'en_AE');
      setMetaProperty('og:locale:alternate', seoOriginals.ogLocaleAlternate || 'ar_AE');
    }
    if (cleanCanonical) {
      upsertAlternate('en', cleanCanonical);
      upsertAlternate('ar', withLanguageQuery(cleanCanonical, 'ar'));
    }
  }

  function translate(value, language = currentLanguage) {
    const clean = normalize(value);
    if (language !== 'ar' || !clean) return clean;
    if (arabic[clean]) return arabic[clean];
    const caseInsensitiveKey = Object.keys(arabic).find(key => key.toLocaleLowerCase() === clean.toLocaleLowerCase());
    if (caseInsensitiveKey) return arabic[caseInsensitiveKey];
    const learnMoreMatch = clean.match(/^Learn More about (.+)$/i);
    if (learnMoreMatch) {
      const service = translate(learnMoreMatch[1], 'ar');
      return `تعرّف إلى ${service}`;
    }
    const countMatch = clean.match(/^(\d+) dentists & specialists$/);
    if (countMatch) return `${countMatch[1]} طبيباً واختصاصياً`;
    const clinicianMatch = clean.match(/^(\d+) clinicians?$/);
    if (clinicianMatch) return `${clinicianMatch[1]} من أفراد الفريق الطبي`;
    const doctorCaptionMatch = clean.match(/^(.+?) · Silwadi Dental Center, Abu Dhabi$/i);
    if (doctorCaptionMatch) {
      const name = translate(doctorCaptionMatch[1], 'ar');
      return `${name} · مركز سلوادي لطب الأسنان، أبوظبي`;
    }
    const doctorAppointmentMatch = clean.match(/^Contact reception to request (?:an appointment|a consultation) with (.+?)\. The team can (?:confirm availability and help route your enquiry|help with appointment availability and treatment enquiries)\.$/i);
    if (doctorAppointmentMatch) {
      const name = translate(doctorAppointmentMatch[1], 'ar');
      return `تواصل مع الاستقبال لطلب موعد مع ${name}. سيساعدك الفريق في التأكد من المواعيد المتاحة وتوجيه استفسارك.`;
    }
    return clean;
  }

  function translateTextNode(node, language) {
    if (!node || !textOriginals) return;
    if (!textOriginals.has(node)) textOriginals.set(node, node.nodeValue);
    const original = textOriginals.get(node);
    const clean = normalize(original);
    if (!clean) return;
    const replacement = translate(clean, language);
    if (language === 'en' || replacement === clean) {
      node.nodeValue = original;
      return;
    }
    const leading = original.match(/^\s*/)?.[0] || '';
    const trailing = original.match(/\s*$/)?.[0] || '';
    node.nodeValue = `${leading}${replacement}${trailing}`;
  }

  function translateAttribute(element, attribute, language) {
    if (!attributeOriginals) return;
    let originals = attributeOriginals.get(element);
    if (!originals) {
      originals = {};
      attributeOriginals.set(element, originals);
    }
    if (!(attribute in originals)) originals[attribute] = element.getAttribute(attribute);
    const original = originals[attribute];
    if (!original) return;
    element.setAttribute(attribute, language === 'ar' ? translate(original, 'ar') : original);
  }

  function applyLanguage(language) {
    currentLanguage = language === 'ar' ? 'ar' : 'en';
    if (typeof document === 'undefined') return currentLanguage;
    document.documentElement.setAttribute('lang', currentLanguage);
    document.documentElement.setAttribute('dir', currentLanguage === 'ar' ? 'rtl' : 'ltr');
    document.body?.classList?.toggle('language-ar', currentLanguage === 'ar');

    if (typeof document.createTreeWalker === 'function' && typeof NodeFilter !== 'undefined') {
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      let node = walker.nextNode();
      while (node) {
        const parent = node.parentElement;
        if (!parent || !['SCRIPT', 'STYLE', 'NOSCRIPT', 'CODE'].includes(parent.tagName)) {
          translateTextNode(node, currentLanguage);
        }
        node = walker.nextNode();
      }
    }

    document.querySelectorAll?.('[placeholder], [aria-label], [title], [alt]').forEach(element => {
      ['placeholder', 'aria-label', 'title', 'alt'].forEach(attribute => {
        if (element.hasAttribute(attribute)) translateAttribute(element, attribute, currentLanguage);
      });
    });

    updateLocalizedSeo(currentLanguage);
    updateCurrentUrl(currentLanguage);
    decorateInternalLinks(currentLanguage);

    if (languageButton) {
      languageButton.textContent = currentLanguage === 'ar' ? 'English' : 'عربي';
      languageButton.setAttribute('aria-label', currentLanguage === 'ar' ? 'Switch to English' : 'التبديل إلى العربية');
    }
    try { localStorage.setItem(STORAGE_KEY, currentLanguage); } catch (_) {}
    if (typeof document.dispatchEvent === 'function' && typeof CustomEvent === 'function') {
      document.dispatchEvent(new CustomEvent('silwadi:languagechange', { detail: { language: currentLanguage } }));
    }
    return currentLanguage;
  }

  function getLanguage() {
    return currentLanguage;
  }

  function init() {
    if (typeof document === 'undefined') return 'en';
    let saved = null;
    try { saved = localStorage.getItem(STORAGE_KEY); } catch (_) {}
    const requested = getRequestedLanguage();
    currentLanguage = requested || (saved === 'ar' ? 'ar' : 'en');
    const headerActions = document.querySelector('.header-actions');
    if (headerActions && !document.querySelector('[data-language-switch]')) {
      languageButton = document.createElement('button');
      languageButton.type = 'button';
      languageButton.className = 'language-switch';
      languageButton.setAttribute('data-language-switch', '');
      languageButton.addEventListener('click', () => applyLanguage(currentLanguage === 'ar' ? 'en' : 'ar'));
      headerActions.prepend(languageButton);
    }
    return applyLanguage(currentLanguage);
  }

  Object.assign(arabic, {"Serving Abu Dhabi families with care that feels personal.":"نخدم عائلات أبوظبي برعاية إنسانية تشعر معها بالاهتمام.","For more than four decades, Silwadi Dental Centre has welcomed Abu Dhabi families with clear advice, trusted expertise and thoughtful care at every visit.":"على مدى أكثر من أربعة عقود، رحّب مركز السلوادي لطب الأسنان بعائلات أبوظبي من خلال نصائح واضحة وخبرة موثوقة ورعاية مدروسة في كل زيارة."});
  Object.assign(arabic, {"Care for every smile in Abu Dhabi":"رعاية لكل ابتسامة في أبوظبي","Since 1980, our dentists have welcomed Abu Dhabi families with clear advice and thoughtful care.":"منذ عام 1980، يرحّب أطباؤنا بعائلات أبوظبي من خلال نصائح واضحة ورعاية مدروسة."});
  Object.assign(arabic, {"Our story":"قصتنا","A familiar name in Abu Dhabi dentistry.":"اسمٌ مألوف في طب الأسنان بأبوظبي.","Silwadi Dental Centre has cared for patients in Abu Dhabi since 1980. What began with Dr. Munir Silwadi continues today through a team of general dentists and specialists working together.":"يعتني مركز السلوادي لطب الأسنان بمرضى أبوظبي منذ عام 1980. وما بدأه الدكتور منير السلوادي يستمر اليوم من خلال فريق من أطباء الأسنان العامين والاختصاصيين الذين يعملون معاً.","We keep the experience simple: listen carefully, explain your options clearly and build a treatment plan around you.":"نحافظ على بساطة التجربة: نستمع باهتمام، ونشرح خياراتك بوضوح، ونضع خطة علاج تناسبك.","Learn about Dr. Munir Silwadi":"تعرّف إلى الدكتور منير السلوادي","Silwadi Dental Centre opens in Abu Dhabi.":"افتتاح مركز السلوادي لطب الأسنان في أبوظبي.","General dentists and specialists care for families across two locations.":"أطباء عامون واختصاصيون يعتنون بالعائلات في موقعين."});
  Object.assign(arabic, {"Everything your smile needs in one place":"كل ما تحتاجه ابتسامتك في مكان واحد","General dentistry and specialist care for children and adults, delivered by an experienced team.":"طب أسنان عام ومتخصص للأطفال والكبار، يقدمه فريق ذو خبرة."});
  Object.assign(arabic, {"Care for every smile in Abu Dhabi":"رعاية لكل ابتسامة في أبوظبي","From check-ups to specialist treatment, our team is here to make dental care feel simple.":"من الفحوصات الدورية إلى العلاجات المتخصصة، نحرص على أن تكون رعاية أسنانك سهلة وواضحة."});
  Object.assign(arabic, {
    "Care for every smile in": "رعاية لكل ابتسامة في",
    "Meet our doctors": "تعرّف إلى أطبائنا",
    "Serving Abu Dhabi": "نخدم أبوظبي",
    "One connected clinical team": "فريق سريري واحد متكامل",
    "2 locations": "فرعان",
    "A familiar name in": "اسم مألوف في",
    "dentistry.": "طب الأسنان.",
    "Today": "اليوم",
    "Care in practice": "الرعاية في الواقع",
    "A dedicated children’s zone helps young patients and families settle in from the moment they arrive.": "تساعد منطقة الأطفال المخصصة المرضى الصغار وعائلاتهم على الاستقرار والشعور بالراحة منذ لحظة الوصول.",
    "Explore children’s care": "استكشف رعاية الأطفال",
    "Plan your visit": "خطط لزيارتك",
    "See our services": "اطّلع على خدماتنا",
    "Where to find us": "أين تجدنا",
    "Two locations in": "فرعان في",
    "Building 117 C Floor, Sultan Bin Zayed The First St, W Corniche Road, Abu Dhabi.": "المبنى 117، الطابق C، شارع سلطان بن زايد الأول، طريق الكورنيش الغربي، أبوظبي.",
    "F14 & F15, Level 1, Al Raha Mall, Abu Dhabi.": "F14 وF15، الطابق الأول، الراحة مول، أبوظبي.",
    "Call reception or book a consultation online for help choosing the appropriate appointment.": "اتصل بالاستقبال أو احجز استشارة عبر الإنترنت لمساعدتك في اختيار الموعد المناسب.",
    "Silwadi Dental Centre": "مركز سلوادي لطب الأسنان",
    "Call, email or send a consultation request. If you are not sure who to book with, reception can guide you.": "اتصل أو أرسل بريداً إلكترونياً أو طلب استشارة. إذا لم تعرف الطبيب المناسب، يمكن للاستقبال إرشادك.",
    "One centre, clear next steps": "مركز واحد وخطوات واضحة",
    "Call, email or start with a general consultation enquiry. Reception can help direct your request.": "اتصل أو أرسل بريداً إلكترونياً أو ابدأ باستفسار عام عن الاستشارة. يساعدك الاستقبال في توجيه طلبك.",
    "If you already know the doctor or treatment you are enquiring about, include that when you contact us. If you are unsure, tell reception what you need help with and they can guide your enquiry to the appropriate clinician.": "إذا كنت تعرف الطبيب أو العلاج الذي تستفسر عنه، اذكره عند التواصل معنا. وإذا لم تكن متأكداً، أخبر الاستقبال بما تحتاج إليه ليقود استفسارك إلى الطبيب المناسب.",
    "01 · CALL": "01 · اتصال",
    "Best for appointment availability, urgent scheduling questions and direct assistance.": "مناسب لمعرفة المواعيد المتاحة والاستفسارات العاجلة والمساعدة المباشرة.",
    "Call +971 2 626 2042 →": "اتصل على ‎+971 2 626 2042 ←",
    "02 · WHATSAPP": "02 · واتساب",
    "Send your preferred date, contact number and a short note about what you need help with.": "أرسل التاريخ المفضل ورقم التواصل وملاحظة قصيرة عما تحتاج إليه.",
    "03 · ONLINE FORM": "03 · نموذج إلكتروني",
    "Complete the form and your request will be prepared for the appointments team.": "أكمل النموذج ليُرسل طلبك إلى فريق المواعيد.",
    "Complete the form →": "أكمل النموذج ←",
    "Bani Yas Tower · Abu Dhabi": "برج بني ياس · أبوظبي",
    "Serving Abu Dhabi.": "نخدم أبوظبي.",
    "Sun–Wed 09:00–21:00 · Thu & Sat 09:00–18:00 · Friday closed": "الأحد–الأربعاء 09:00–21:00 · الخميس والسبت 09:00–18:00 · الجمعة مغلق",
    "Available": "متاح",
    "Open in Google Maps →": "افتح في خرائط Google ←",
    "The centre accepts insurance and submits most claims electronically on behalf of patients. Coverage varies by provider and plan, so contact reception with your insurance details before your visit.": "يقبل المركز التأمين ويرسل معظم المطالبات إلكترونياً نيابة عن المرضى. تختلف التغطية حسب شركة التأمين والخطة، لذا تواصل مع الاستقبال بتفاصيل تأمينك قبل الزيارة.",
    "Al Raha Mall · now open": "الراحة مول · مفتوح الآن",
    "Second Abu Dhabi location": "فرع أبوظبي الثاني",
    "F14 & F15, Level 1, Al Raha Mall, Abu Dhabi, UAE.": "F14 وF15، الطابق الأول، الراحة مول، أبوظبي، الإمارات العربية المتحدة.",
    "Call +971 2 666 2408 →": "اتصل على ‎+971 2 666 2408 ←",
    "Not sure who to book?": "لست متأكداً أي طبيب تحجز معه؟",
    "Use the doctor directory or treatment directory, or contact reception and describe the reason for your visit.": "استخدم دليل الأطباء أو دليل العلاجات، أو تواصل مع الاستقبال واشرح سبب زيارتك.",
    "Ready to arrange your visit?": "هل أنت مستعد لترتيب زيارتك؟",
    "Choose the contact method that works best for you. Reception can help with appointment availability and route treatment enquiries appropriately.": "اختر طريقة التواصل الأنسب لك. يساعدك الاستقبال في معرفة المواعيد وتوجيه استفسارات العلاج إلى الطبيب المناسب.",
    "Email a Request": "أرسل طلباً بالبريد الإلكتروني",
    "Silwadi Dental Centre now welcomes patients at Bani Yas Tower and Al Raha Mall.": "يستقبل مركز سلوادي لطب الأسنان المرضى الآن في برج بني ياس والراحة مول.",
    "Open": "مفتوح",
    "F14 & F15, Level 1, Al Raha Mall, Channel St, Al Rahah, Abu Dhabi, UAE.": "F14 وF15، الطابق الأول، الراحة مول، شارع تشانل، الراحة، أبوظبي، الإمارات العربية المتحدة.",
    "Al Raha Mall, Level 1": "الراحة مول، الطابق الأول",
    "Call Al Raha": "اتصل بفرع الراحة",
    "Instagram": "إنستغرام",
    "09:00 AM to 09:00 PM": "09:00 ص إلى 09:00 م",
    "09:00 AM to 06:00 PM": "09:00 ص إلى 06:00 م",
    "Bani Yas Tower, Building 117 C Floor, Sultan Bin Zayed The First St, W Corniche Road, Abu Dhabi, UAE": "برج بني ياس، المبنى 117، الطابق C، شارع سلطان بن زايد الأول، طريق الكورنيش الغربي، أبوظبي، الإمارات العربية المتحدة",
    "Bani Yas Tower, Building 117 C Floor, Sultan Bin Zayed The First St, W Corniche Road, Abu Dhabi.": "برج بني ياس، المبنى 117، الطابق C، شارع سلطان بن زايد الأول، طريق الكورنيش الغربي، أبوظبي.",
    "© 2026 Dr. Munir Silwadi Dental Centre": "© 2026 مركز الدكتور منير السلوادي لطب الأسنان",
    "Our services": "خدماتنا",
    "Dental services for every smile in": "خدمات أسنان لكل ابتسامة في",
    "Aesthetic care with a restorative foundation.": "رعاية تجميلية تبدأ من أساس ترميمي سليم.",
    "Digital smile planning": "التخطيط الرقمي للابتسامة",
    "Examine": "افحص",
    "Oral Hygiene": "نظافة الفم",
    "Google": "Google",
    "Established": "تأسس",
    "Our team": "فريقنا",
    "Meet the team →": "تعرّف إلى الفريق ←",
    "Find a Doctor": "ابحث عن طبيب",
    "Meet the team": "تعرّف إلى الفريق",
    "Explore Services": "استكشف الخدمات",
    "Find the right care": "اعثر على الرعاية المناسبة",
    "Visit the centre": "زر المركز",
    "Call Us": "اتصل بنا",
    "Treatments": "العلاجات",
    "View all services": "عرض جميع الخدمات",
    "View all services →": "عرض جميع الخدمات ←",
    "Call or view urgent care →": "اتصل بنا أو اطّلع على الرعاية العاجلة ←",
    "Learn more about the centre": "اعرف المزيد عن المركز",
    "Specialist expertise. Personal care.": "خبرة تخصصية ورعاية شخصية.",
    "Meet some of our dentists and specialists, or browse the full team by specialty.": "تعرّف إلى عدد من أطبائنا واختصاصيينا، أو تصفّح الفريق كاملاً حسب التخصص.",
    "View medical team": "عرض الفريق الطبي",
    "Meet the full medical team": "تعرّف إلى الفريق الطبي كاملاً",
    "What patients say about Silwadi.": "ماذا يقول المرضى عن سلوادي؟",
    "Read all reviews →": "اقرأ جميع التقييمات ←",
    "Current location": "الفرع الحالي",
    "Call the centre": "اتصل بالمركز",
    "Ask for directions": "اطلب الاتجاهات",
    "Location details": "تفاصيل الموقع",
    "Not sure which dentist you need?": "لست متأكداً أي طبيب تحتاج؟",
    "Tell our team what you need help with and we can guide you toward the appropriate clinician.": "أخبر فريقنا بما تحتاج إليه وسنوجهك إلى الطبيب المناسب.",
    "Clinical base": "الموقع السريري",
    "CAD/CAM": "CAD/CAM",
    "Root canal care": "علاج الجذور",
    "Minimally invasive approach": "نهج قليل التدخل",
    "Gum health": "صحة اللثة",
    "Paris postgraduate training": "تدريب دراسات عليا في باريس",
    "Academic orthodontics": "خبرة أكاديمية في تقويم الأسنان",
    "Orthodontics & Braces": "تقويم الأسنان والتقويم الثابت",
    "25 years in GCC": "25 عاماً في دول الخليج",
    "Braces & aligners": "التقويم والصفافات",
    "Abu Dhabi practice since 2000": "ممارسة في أبوظبي منذ عام 2000",
    "Explore Dental Implants": "استكشف زراعة الأسنان",
    "Location & directions": "الموقع والاتجاهات",
  });

  Object.assign(arabic, {
    "Important notice": "تنبيه مهم",
    "To our valued patients, please beware of false online offers promising free treatments at Silwadi Dental Centre.": "مرضانا الكرام، يرجى الحذر من العروض الإلكترونية المضللة التي تعد بعلاجات مجانية في مركز السلوادي لطب الأسنان.",
    "Book your appointment": "احجز موعدك",
    "Share a few details and our appointments team will confirm availability with you.": "أدخل بعض التفاصيل وسيتواصل معك فريق المواعيد لتأكيد التوفر.",
    "Full name": "الاسم الكامل",
    "Mobile": "رقم الهاتف المحمول",
    "Treatment": "العلاج",
    "Preferred appointment date": "التاريخ المفضل للموعد",
    "Preferred appointment time": "الوقت المفضل للموعد",
    "Preferred clinic": "العيادة المفضلة",
    "Notes / other queries": "ملاحظات / استفسارات أخرى",
    "Please choose": "يرجى الاختيار",
    "General Dentistry": "طب الأسنان العام",
    "Preventive Dentistry": "طب الأسنان الوقائي",
    "Cosmetic Dentistry": "طب الأسنان التجميلي",
    "Dental Implants": "زراعة الأسنان",
    "Orthodontics": "تقويم الأسنان",
    "Periodontics": "علاج اللثة",
    "Endodontics": "علاج الجذور",
    "Paediatric Dentistry": "طب أسنان الأطفال",
    "Other / Not sure": "أخرى / لست متأكداً",
    "Bani Yas Tower": "برج بني ياس",
    "Al Raha Mall": "الراحة مول",
    "Send appointment request": "إرسال طلب موعد",
    "Your email app is opening with the appointment request.": "سيتم فتح تطبيق البريد الإلكتروني مع طلب الموعد."
  });

  Object.assign(arabic, {
    "Dental services for every smile in": "خدمات أسنان لكل ابتسامة في",
    "From preventive visits to specialist treatment, Silwadi Dental Center brings general dentists and specialists together across a broad range of dental care.": "من الزيارات الوقائية إلى العلاج التخصصي، يجمع مركز سلوادي لطب الأسنان أطباء عامين واختصاصيين لتقديم مجالات متنوعة من رعاية الأسنان.",
    "Start here": "ابدأ من هنا",
    "Start with what you need.": "ابدأ بما تحتاج إليه.",
    "Not sure which service fits? Begin with the reason you are visiting and follow the link that feels closest. Your dentist will confirm the right next step.": "لست متأكداً من الخدمة المناسبة؟ ابدأ بسبب زيارتك، وسيساعدك طبيب الأسنان في تحديد الخطوة التالية.",
    "For growing smiles": "لابتسامات صغيرة تكبر بصحة",
    "Children’s dental care": "رعاية أسنان الأطفال",
    "Gentle visits, prevention and restorative care for children.": "زيارات هادئة ورعاية وقائية وترميمية للأطفال.",
    "Restore confidence": "استعد راحتك",
    "Replace or repair teeth": "تعويض الأسنان أو ترميمها",
    "Implants, crowns, bridges and dentures planned around your bite.": "زراعة وتيجان وجسور وأطقم تُخطط بما يناسب إطباقك.",
    "Protect your smile": "احمِ ابتسامتك",
    "Prevention and hygiene": "الوقاية والعناية اليومية",
    "Examinations, hygiene guidance and early support for healthy gums.": "فحوصات وإرشادات للعناية اليومية ودعم مبكر لصحة اللثة.",
    "A clear place to begin.": "بداية واضحة لرعايتك.",
    "Browse the service areas below for a plain-language overview. Every card leads to the next useful step, and reception can help if you are unsure where to begin.": "تعرّف إلى مجالات الخدمة أدناه بلغة واضحة. كل بطاقة تقودك إلى الخطوة التالية، ويمكن للاستقبال مساعدتك إذا لم تعرف من أين تبدأ.",
    "focuses on planning and surgically placing dental implants—artificial tooth roots that support replacement teeth.": "يهتم بتخطيط زراعة الأسنان ووضعها جراحياً، وهي جذور صناعية تدعم الأسنان التعويضية.",
    "focuses on restoring or replacing teeth with crowns, bridges, veneers, dentures and implant-supported restorations, including full-mouth rehabilitation.": "يهتم بترميم الأسنان أو تعويضها بالتيجان والجسور والقشور والأطقم والتركيبات المدعومة بالزراعة، بما في ذلك إعادة تأهيل الفم بالكامل.",
    "Specialist gum care for periodontal disease and the supporting tissues around the teeth, including non-surgical and surgical treatment when indicated.": "رعاية تخصصية لأمراض اللثة والأنسجة الداعمة حول الأسنان، مع علاج غير جراحي أو جراحي عند الحاجة.",
    "Diagnosis and treatment of conditions affecting the dental pulp and root canal system, including root canal therapy and retreatment.": "تشخيص وعلاج الحالات التي تصيب لب السن وقنوات الجذر، بما في ذلك علاج الجذور وإعادة العلاج.",
    "Specialist orthodontic care for tooth alignment and bite correction using braces, aligners, retainers and other appliances where appropriate.": "رعاية تخصصية لتصحيح اصطفاف الأسنان والإطباق باستخدام التقويم والصفافات والمثبتات وغيرها عند ملاءمتها.",
    "Dental care for children from infancy through adolescence, including preventive care, fluoride, sealants and restorative treatment.": "رعاية أسنان الأطفال من مرحلة الرضاعة حتى المراهقة، وتشمل الوقاية والفلورايد والحشوات الوقائية والعلاج الترميمي.",
    "Aesthetic dental care including veneers, smile design and restorative options selected after a clinical assessment of the teeth and bite.": "رعاية تجميلية تشمل القشور وتصميم الابتسامة وخيارات ترميمية تُختار بعد تقييم الأسنان والإطباق.",
    "Professional whitening options for suitable patients, planned after an examination to assess the teeth, existing restorations and the cause of discoloration.": "خيارات تبييض احترافية للمرضى المناسبين، تُخطط بعد فحص الأسنان والتركيبات الموجودة وسبب تغير اللون.",
    "Dental laser techniques used for selected soft- and hard-tissue procedures when clinically appropriate.": "تقنيات الليزر المستخدمة في إجراءات مختارة للأنسجة الرخوة والصلبة عندما تكون مناسبة سريرياً.",
    "Routine examinations, professional hygiene guidance and preventive planning designed to protect teeth and gums and identify problems early.": "فحوصات دورية وإرشادات احترافية للعناية بالفم وتخطيط وقائي لحماية الأسنان واللثة واكتشاف المشكلات مبكراً.",
    "Not sure which service you need?": "لست متأكداً من الخدمة التي تحتاجها؟",
    "Tell reception what you would like help with and the team can guide your appointment enquiry.": "أخبر الاستقبال بما تحتاج إليه، وسيساعدك الفريق في توجيه طلب موعدك.",
    "Dental care": "رعاية الأسنان",
    "Explore Silwadi Dental Center’s dental service areas, or contact us if you are not sure where to start.": "استكشف مجالات رعاية الأسنان في مركز سلوادي، أو تواصل معنا إذا لم تعرف من أين تبدأ.",
    "10 service areas": "10 مجالات للرعاية",
    "General and specialist dental care across ten established service areas.": "رعاية أسنان عامة وتخصصية ضمن عشرة مجالات واضحة.",
    "Choose a service that matches your next step.": "اختر الخدمة التي تناسب خطوتك التالية.",
    "Start with the concern that brought you here. Each option opens a focused guide or takes you to the related service on our main services page.": "ابدأ من السبب الذي دفعك إلى زيارة الموقع. يفتح كل خيار دليلاً مختصراً أو ينقلك إلى الخدمة ذات الصلة.",
    "Restore and replace": "رمّم وعوّض",
    "Rebuild a comfortable bite.": "استعد إطباقاً مريحاً.",
    "Plans for missing, damaged or heavily worn teeth.": "خطط للأسنان المفقودة أو المتضررة أو شديدة التآكل.",
    "Implant planning and replacement teeth for suitable patients.": "تخطيط للزراعة وأسنان تعويضية للمرضى المناسبين.",
    "Crowns, bridges, dentures and other restorative options.": "تيجان وجسور وأطقم وخيارات ترميمية أخرى.",
    "Align and protect": "صحّح واحمِ",
    "Look after your foundations.": "اعتنِ بالأساس الذي يحمي ابتسامتك.",
    "Specialist care for alignment, gums and the tissues that support your teeth.": "رعاية تخصصية لاصطفاف الأسنان واللثة والأنسجة الداعمة.",
    "Braces, clear aligners and bite correction after assessment.": "تقويم وصفافات شفافة وتصحيح للإطباق بعد التقييم.",
    "Diagnosis and treatment for gums and supporting tissues.": "تشخيص وعلاج اللثة والأنسجة الداعمة.",
    "Family care": "رعاية لجميع أفراد الأسرة",
    "Support every stage of a smile.": "دعم كل مرحلة من مراحل الابتسامة.",
    "Gentle, practical care for children and treatment for tooth pain.": "رعاية هادئة وعملية للأطفال وعلاج لألم الأسنان.",
    "Root canal and pulp care when a tooth is painful or infected.": "علاج الجذور واللب عندما يكون السن مؤلماً أو مصاباً بالعدوى.",
    "Dental visits designed for children from infancy to adolescence.": "زيارات أسنان مناسبة للأطفال من الرضاعة حتى المراهقة.",
    "Smile and prevention": "الابتسامة والوقاية",
    "Feel good about your daily care.": "اجعل عنايتك اليومية أبسط.",
    "Evidence-led options to improve appearance and protect oral health.": "خيارات تستند إلى التقييم لتحسين المظهر وحماية صحة الفم.",
    "Veneers, whitening and restorative smile planning after review.": "قشور وتبييض وتخطيط ترميمي للابتسامة بعد المراجعة.",
    "Examinations and early support for healthier teeth and gums.": "فحوصات ودعم مبكر لأسنان ولثة أكثر صحة.",
    "Professional cleaning and guidance for an easier home routine.": "تنظيف احترافي وإرشادات لروتين منزلي أسهل.",
    "Laser-assisted techniques for selected procedures when suitable.": "تقنيات بمساعدة الليزر لإجراءات مختارة عند ملاءمتها.",
    "Need a little help?": "هل تحتاج إلى بعض المساعدة؟",
    "Tell us what is bothering you.": "أخبرنا ما الذي يزعجك.",
    "Reception can guide your enquiry to the right dentist or specialist. You do not need to know the treatment name before you contact us.": "يمكن للاستقبال توجيه استفسارك إلى طبيب الأسنان أو الاختصاصي المناسب. لا تحتاج إلى معرفة اسم العلاج قبل التواصل معنا.",
    "Talk to reception": "تحدث مع الاستقبال",
    "Emergency dental assessment is available during clinic hours. Call the centre for urgent scheduling or review our emergency guidance.": "يتوفر تقييم الأسنان العاجل خلال ساعات العمل. اتصل بالمركز لتحديد موعد عاجل أو اطّلع على إرشادات الحالات الطارئة.",
    "Emergency dental care →": "رعاية أسنان عاجلة ←",
    "Need guidance?": "هل تحتاج إلى توجيه؟",
    "Not sure which treatment applies?": "لست متأكداً من العلاج المناسب؟",
    "Our reception team can help direct your enquiry to the appropriate dentist or specialist.": "يمكن لفريق الاستقبال توجيه استفسارك إلى طبيب الأسنان أو الاختصاصي المناسب.",
    "Natural care, clear next steps.": "رعاية واضحة وخطوات بسيطة.",
    "Advanced dentistry.": "خبرة راسخة.",
    "Established trust.": "ثقة منذ عام 1980.",
    "Care for every smile in Abu Dhabi": "رعاية لكل ابتسامة في أبوظبي",
    "Since 1980, our dentists have welcomed Abu Dhabi families with clear advice and thoughtful care.": "منذ عام 1980، يرحّب أطباؤنا بعائلات أبوظبي بنصائح واضحة ورعاية مدروسة.",
    "Care that feels considered.": "رعاية تُقدّم باهتمام.",
    "A familiar name in Abu Dhabi dentistry.": "اسم يعرفه أهل أبوظبي في طب الأسنان.",
    "People of Determination": "أصحاب الهمم"
  });

  Object.assign(arabic, {
    "Open navigation": "فتح القائمة",
    "Mobile navigation": "القائمة المتنقلة",
    "Primary navigation": "التنقل الرئيسي",
    "Breadcrumb": "مسار التنقل",
    "Quick contact": "تواصل سريع",
    "Patient shortcuts": "اختصارات المرضى",
    "Patient review excerpts": "مقتطفات من تقييمات المرضى",
    "Selected members of the Silwadi dental team": "نماذج من فريق سلوادي لطب الأسنان",
    "Centre trust information": "معلومات عن المركز وثقة المرضى",
    "Established since 1980": "خبرة منذ عام 1980",
    "Profile highlights": "أبرز المعلومات",
    "Treatment overview": "نظرة عامة على العلاج",
    "Filter doctors by specialty": "تصفية الأطباء حسب التخصص",
    "Read Silwadi reviews on Google Maps": "اقرأ تقييمات سلوادي على خرائط Google",
    "Silwadi Dental Center home": "الصفحة الرئيسية لمركز سلوادي لطب الأسنان",
    "Chat with Silwadi Dental Center on WhatsApp": "تواصل مع مركز سلوادي لطب الأسنان عبر واتساب",
    "WhatsApp Silwadi Dental Center": "تواصل مع مركز سلوادي لطب الأسنان عبر واتساب",
    "Follow Silwadi Dental Center on Instagram": "تابع مركز سلوادي لطب الأسنان على Instagram",
    "Open patient review": "فتح تقييم المريض",
    "Close review": "إغلاق التقييم",
    "4.6 out of 5 stars": "4.6 من 5 نجوم",
    "5 out of 5 stars": "5 من 5 نجوم",
    "Choose a starting point": "اختر نقطة البداية",
    "Map showing Dr. Munir Silwadi Dental Centre at Al Raha Mall, Abu Dhabi": "خريطة توضح موقع مركز الدكتور منير السلوادي لطب الأسنان في الراحة مول بأبوظبي",
    "Map showing Dr. Munir Silwadi Dental Centre at Bani Yas Tower, Abu Dhabi": "خريطة توضح موقع مركز الدكتور منير السلوادي لطب الأسنان في برج بني ياس بأبوظبي",
    "Cosmetic dentistry": "طب الأسنان التجميلي",
    "Orthodontic care": "رعاية تقويم الأسنان",
    "Periodontal care": "رعاية اللثة",
    "Preventive dental care": "رعاية الأسنان الوقائية",
    "Prosthodontics and implantology": "تركيبات وزراعة الأسنان",
  });

  Object.assign(arabic, {
    "Since 1980, our dentists and specialists have cared for Abu Dhabi families with clear advice and a warm welcome.": "منذ عام 1980، يعتني أطباؤنا واختصاصيونا بعائلات أبوظبي من خلال نصائح واضحة وترحيب دافئ.",
    "Silwadi Dental Centre began serving patients in Abu Dhabi in 1980. Today, a multi-specialty, multidisciplinary team of general dentists and specialists works together across prosthodontics, implantology, orthodontics, endodontics and everyday dental care.": "بدأ مركز السلوادي لطب الأسنان خدمة المرضى في أبوظبي عام 1980. ويعمل اليوم فريق متعدد التخصصات من أطباء الأسنان العامين والاختصاصيين معاً في التركيبات والزراعة والتقويم وعلاج الجذور والرعاية اليومية.",
    "There is time for questions at every visit. We explain treatment in plain language, keep your comfort in mind and help you find the right next step.": "نخصص وقتاً لأسئلتك في كل زيارة. نشرح العلاج بلغة واضحة، ونضع راحتك في الاعتبار، ونساعدك في اختيار الخطوة التالية المناسبة.",
    "The people and place behind your care.": "الأشخاص والمكان وراء رعايتك.",
    "From the reception team to the clinical staff, our centre is built around clear conversations and a comfortable visit.": "من فريق الاستقبال إلى الطاقم السريري، صُمم مركزنا ليقدم حواراً واضحاً وزيارة مريحة.",
    "The Silwadi Dental Centre team in Abu Dhabi": "فريق مركز السلوادي لطب الأسنان في أبوظبي",
    "Silwadi Dental Centre clinical team in Abu Dhabi": "الفريق السريري في مركز السلوادي لطب الأسنان بأبوظبي",
    "Silwadi Dental Centre team meeting": "اجتماع فريق مركز السلوادي لطب الأسنان",
    "Silwadi Dental Centre clinicians at the Bani Yas clinic": "أطباء مركز السلوادي لطب الأسنان في عيادة بني ياس",
    "One team, working together.": "فريق واحد يعمل معاً.",
    "Care planned together.": "رعاية نخطط لها معاً.",
    "A familiar clinical team.": "فريق سريري مألوف.",
    "Start with the right conversation.": "ابدأ بالحوار المناسب.",
    "You do not need to know the treatment name before you call. Our directory can help you explore the team, and reception can guide your enquiry.": "لا تحتاج إلى معرفة اسم العلاج قبل الاتصال. يساعدك دليل الأطباء في استكشاف الفريق، ويمكن للاستقبال توجيه استفسارك.",
    "View profile": "عرض الملف",
    "A centre for real life.": "مركز يناسب حياتك اليومية.",
    "Thoughtful spaces, practical support and modern clinical tools help make each visit easier to understand.": "تساعد المساحات المدروسة والدعم العملي والتقنيات السريرية الحديثة على جعل كل زيارة أوضح.",
    "Support for every patient": "دعم لكل مريض",
    "Dedicated rooms and an accessible layout support People of Determination with dignity and comfort.": "تدعم الغرف المخصصة والتصميم الميسّر أصحاب الهمم بما يحفظ كرامتهم وراحتهم.",
    "Modern clinical tools": "تقنيات سريرية حديثة",
    "Digital X-rays, CAD/CAM, 3D printing, laser dentistry and intraoral imaging support careful treatment planning.": "تدعم الأشعة الرقمية وتقنيات CAD/CAM والطباعة ثلاثية الأبعاد وطب الأسنان بالليزر والتصوير داخل الفم تخطيط العلاج بعناية.",
    "Ready to meet the team?": "هل أنت مستعد للتعرف إلى الفريق؟",
    "Explore our dentists and specialists, or contact reception to talk through your next step.": "تعرّف إلى أطبائنا واختصاصيينا، أو تواصل مع الاستقبال لمناقشة خطوتك التالية.",
    "Talk to reception": "تحدث مع الاستقبال",
    "Your email app will open with the details you enter. We use them only to respond to this appointment enquiry. Please do not include sensitive medical information in the form.": "سيفتح تطبيق البريد الإلكتروني مع التفاصيل التي تدخلها. نستخدمها فقط للرد على استفسار الموعد. يرجى عدم إدخال معلومات طبية حساسة في النموذج.",
    "I agree that Silwadi may use these details to reply to my appointment enquiry.": "أوافق على استخدام سلوادي لهذه البيانات للرد على استفسار الموعد.",
  });

  // Treatment detail pages are intentionally written as complete, patient-facing
  // sentences. Keep their Arabic equivalents together so a visitor never lands
  // on a page with a translated breadcrumb but an English headline or paragraph.
  Object.assign(arabic, {
    "Implant dentistry": "زراعة الأسنان",
    "Dental Implants in": "زراعة الأسنان في",
    "Cosmetic Dentistry in": "طب الأسنان التجميلي في",
    "Thinking about changing the colour, shape or appearance of your smile? The first step is to understand the health of the teeth and which options are appropriate.": "هل تفكر في تغيير لون ابتسامتك أو شكلها أو مظهرها؟ تبدأ الخطوة الأولى بفهم صحة الأسنان والخيارات المناسبة لك.",
    "Emergency Dentist": "طبيب أسنان للحالات الطارئة",
    "Urgent dental care": "رعاية أسنان عاجلة",
    "Emergency Dentist in": "طبيب أسنان للحالات الطارئة في",
    "General Dentistry in": "طب الأسنان العام في",
    "Orthodontics in": "تقويم الأسنان في",
    "Meet Dr. Munir": "تعرّف إلى د. منير",
    "Bani Yas Tower, Abu Dhabi": "برج بني ياس، أبوظبي",
    "Next step": "الخطوة التالية",
    "Clinical assessment before treatment planning": "تقييم سريري قبل وضع خطة العلاج",
    "At a glance": "لمحة سريعة",
    "Location & directions →": "الموقع والاتجاهات ←",
    "Assessment before treatment": "تقييم قبل العلاج",
    "Digital planning where appropriate": "تخطيط رقمي عند الحاجة",
    "Specialist prosthodontic input": "إشراف اختصاصي التركيبات",
    "Implant care, planned around the restoration.": "رعاية زراعة تُخطط بما يناسب التركيبة.",
    "Whitening": "تبييض الأسنان",
    "Veneers and restorations": "القشور والترميمات",
    "Start with the health of the teeth": "ابدأ بصحة الأسنان",
    "Cosmetic dentistry should begin with a clinical assessment. The condition of the teeth and gums, the bite and any existing restorations can affect which aesthetic options make sense.": "يبدأ تجميل الأسنان بتقييم سريري. فقد تؤثر حالة الأسنان واللثة والإطباق والتركيبات الموجودة في الخيارات التجميلية المناسبة.",
    "Possible treatment options": "خيارات العلاج الممكنة",
    "Depending on the case, cosmetic planning may involve professional whitening, veneers, crowns or other restorative work. Digital smile planning may also be used to support communication about shape, proportion and restorative goals.": "بحسب الحالة، قد يشمل التخطيط التجميلي تبييضاً احترافياً أو قشوراً أو تيجاناً أو علاجاً ترميمياً آخر. وقد يُستخدم التخطيط الرقمي للابتسامة لتوضيح الشكل والتناسق وأهداف الترميم.",
    "Choosing the right approach": "اختيار النهج المناسب",
    "Treatment approach": "نهج العلاج",
    "Your next step": "خطوتك التالية",
    "Speak with the team": "تحدث مع فريقنا",
    "Assess": "قيّم",
    "Check oral health, existing restorations and the bite.": "افحص صحة الفم والتركيبات الموجودة والإطباق.",
    "Discuss": "ناقش",
    "Clarify what you would like to change and what is realistic.": "وضّح ما تود تغييره وما يمكن تحقيقه واقعياً.",
    "Plan": "خطط",
    "Select the restorative or aesthetic approach that fits the teeth.": "اختر النهج الترميمي أو التجميلي الذي يناسب أسنانك.",
    "Restorative and aesthetic care": "رعاية ترميمية وتجميلية",
    "Several clinicians’ public profiles include cosmetic or aesthetic restorative dentistry among their clinical interests. The appropriate dentist depends on the treatment being considered and the findings at assessment.": "تتضمن الملفات التعريفية المنشورة لعدد من أطبائنا الترميم التجميلي وتجميل الأسنان ضمن اهتماماتهم السريرية. ويعتمد اختيار الطبيب المناسب على العلاج المطلوب ونتائج التقييم.",
    "General Dentist · cosmetic & digital dentistry": "طبيب أسنان عام · تجميل الأسنان وطب الأسنان الرقمي",
    "General Dentist · cosmetic & restorative interests": "طبيب أسنان عام · اهتمامات تجميلية وترميمية",
    "General Dentist · aesthetic & restorative interests": "طبيب أسنان عام · اهتمامات تجميلية وترميمية",
    "Prosthodontics · aesthetic restorative care": "تركيبات الأسنان · رعاية ترميمية تجميلية",
    "Do I need an examination before whitening or veneers?": "هل أحتاج إلى فحص قبل التبييض أو القشور؟",
    "Yes. A dental assessment helps identify decay, gum problems, existing restorations or bite issues that may affect the plan.": "نعم. يساعد فحص الأسنان في اكتشاف التسوس ومشكلات اللثة والتركيبات الموجودة أو مشكلات الإطباق التي قد تؤثر في الخطة.",
    "Are veneers right for every cosmetic concern?": "هل تناسب القشور كل مشكلة تجميلية؟",
    "No. Veneers are one option. Whitening, restorative treatment or no treatment may be more appropriate depending on the teeth and your goals.": "لا. القشور خيار واحد فقط. وقد يكون التبييض أو العلاج الترميمي أو عدم التدخل أنسب، بحسب حالة الأسنان وأهدافك.",
    "Can I see the proposed changes before treatment?": "هل يمكنني رؤية التغييرات المقترحة قبل العلاج؟",
    "Digital smile planning may be used in selected cases to support discussion and visual communication before restorative treatment.": "قد يُستخدم التخطيط الرقمي للابتسامة في حالات مختارة لتوضيح النتيجة ومناقشتها قبل العلاج الترميمي.",
    "What are dental implants?": "ما هي زراعة الأسنان؟",
    "Missing a tooth or several teeth? Implant treatment starts with an assessment of your oral health, bone, bite and the restoration you may need.": "هل فقدت سناً أو عدة أسنان؟ يبدأ علاج الزراعة بتقييم صحة فمك والعظم والإطباق والتركيبة المناسبة لك.",
    "Dental implants can support a replacement tooth or an implant-supported restoration when a patient is clinically suitable. The restoration is planned around the missing tooth or teeth, the bite and the surrounding tissues.": "يمكن لزراعة الأسنان أن تدعم سناً بديلاً أو تركيبة مدعومة بالزراعة عندما يكون المريض مناسباً من الناحية السريرية. ويُخطط للتعويض وفق السن أو الأسنان المفقودة والإطباق والأنسجة المحيطة.",
    "Who may be suitable?": "من يناسبه العلاج؟",
    "Implant treatment is not the same for everyone. The dentist reviews oral health, available bone, gum condition and restorative needs before recommending an approach. Some patients may need another treatment first, or may be better suited to a different restorative option.": "لا يناسب علاج الزراعة الجميع بالطريقة نفسها. يراجع طبيب الأسنان صحة الفم والعظم المتاح وحالة اللثة والاحتياجات الترميمية قبل التوصية بالنهج المناسب. وقد يحتاج بعض المرضى إلى علاج آخر أولاً أو إلى خيار ترميمي مختلف.",
    "Clinical examination and diagnostic records where indicated.": "فحص سريري وسجلات تشخيصية عند الحاجة.",
    "Implant position, restoration and treatment sequence are reviewed.": "تُراجع موضع الزراعة والتركيبة وتسلسل العلاج.",
    "Restore": "عوّض",
    "The final restorative stage follows the appropriate clinical steps.": "تأتي المرحلة الترميمية النهائية بعد استكمال الخطوات السريرية المناسبة.",
    "Digital planning": "التخطيط الرقمي",
    "Digital and computer-guided workflows may be used in selected cases to support implant positioning and restorative planning. The technology used depends on the clinical situation rather than being required for every implant case.": "قد تُستخدم التقنيات الرقمية والتخطيط الموجّه بالحاسوب في حالات مختارة لدعم تحديد موضع الزراعة والتخطيط الترميمي. وتُختار التقنية وفق الحالة السريرية، ولا تكون ضرورية لكل حالة زراعة.",
    "Doctors for implant care": "أطباء زراعة الأسنان",
    "Implant care can involve restorative and periodontal input depending on the case. These public clinician profiles list implant dentistry among their clinical interests.": "قد تتطلب رعاية الزراعة مشاركة اختصاصي التركيبات أو اللثة بحسب الحالة. وتذكر هذه الملفات التعريفية المنشورة زراعة الأسنان ضمن الاهتمامات السريرية لأصحابها.",
    "View Dr. Munir’s profile →": "عرض ملف د. منير ←",
    "General Dentist · implant dentistry interest": "طبيب أسنان عام · اهتمام بزراعة الأسنان",
    "Dr. Fahed Khalil": "د. فهد أبي خليل",
    "Specialist Periodontics · implant dentistry interest": "اختصاصي أمراض اللثة · اهتمام بزراعة الأسنان",
    "Is everyone suitable for dental implants?": "هل يناسب علاج زراعة الأسنان الجميع؟",
    "No. Suitability depends on oral health, bone, gum condition, medical factors and the planned restoration.": "لا. تعتمد الملاءمة على صحة الفم والعظم وحالة اللثة والعوامل الطبية والتركيبة المخطط لها.",
    "Do all implant cases use guided surgery?": "هل تستخدم الجراحة الموجّهة في كل حالات الزراعة؟",
    "No. Digital or guided workflows may be used when they are clinically useful for the individual case.": "لا. قد تُستخدم التقنيات الرقمية أو الموجّهة عندما تكون مفيدة سريرياً للحالة الفردية.",
    "How do I know which implant restoration I need?": "كيف أعرف نوع التركيبة المناسبة للزراعة؟",
    "That is decided after assessment and restorative planning, based on the number and position of missing teeth and your clinical findings.": "يتحدد ذلك بعد التقييم والتخطيط الترميمي، وفق عدد الأسنان المفقودة ومواضعها ونتائج الفحص السريري.",
    "Dental pain or a broken tooth can be difficult to ignore. Call the centre first so we can check clinic availability and help direct the next step.": "قد يصعب تجاهل ألم الأسنان أو كسر السن. اتصل بالمركز أولاً لنتحقق من المواعيد المتاحة ونرشدك إلى الخطوة التالية.",
    "Call +971 2 626 2042": "اتصل على ‎+971 2 626 2042",
    "Urgent contact": "تواصل عاجل",
    "Clinic": "العيادة",
    "Call first for urgent dental concerns.": "اتصل أولاً عند وجود مشكلة أسنان عاجلة.",
    "Dental pain": "ألم الأسنان",
    "Broken teeth or lost restorations": "أسنان مكسورة أو تركيبات مفقودة",
    "Swelling or dental trauma": "تورم أو إصابة في الأسنان",
    "When to call for urgent dental care": "متى تتصل للحصول على رعاية أسنان عاجلة؟",
    "Urgent dental concerns can include severe tooth pain, a broken or chipped tooth, a lost filling or crown, dental swelling, or dental trauma. Call the centre so reception can check appointment availability and direct the concern appropriately.": "قد تشمل مشكلات الأسنان العاجلة ألماً شديداً أو سناً مكسوراً أو متشظياً أو حشوة أو تاجاً مفقوداً أو تورماً أو إصابة في الأسنان. اتصل بالمركز ليتحقق الاستقبال من توفر المواعيد ويوجهك إلى الرعاية المناسبة.",
    "When not to wait for a dental appointment": "متى لا تنتظر موعد الأسنان؟",
    "Seek emergency medical care if there is significant facial or neck swelling with difficulty breathing or swallowing, uncontrolled bleeding, loss of consciousness, or major facial trauma. These situations need urgent medical assessment rather than waiting for routine dental contact.": "اطلب الرعاية الطبية الطارئة إذا ظهر تورم كبير في الوجه أو الرقبة مع صعوبة في التنفس أو البلع، أو نزيف لا يتوقف، أو فقدان للوعي، أو إصابة شديدة في الوجه. تحتاج هذه الحالات إلى تقييم طبي عاجل ولا ينبغي انتظار موعد أسنان عادي.",
    "What happens when you call": "ماذا يحدث عند الاتصال؟",
    "Describe the problem": "صف المشكلة",
    "Tell reception what happened and the main symptoms.": "أخبر الاستقبال بما حدث والأعراض الأساسية.",
    "Urgent dental appointments depend on clinic hours and clinician availability.": "تعتمد المواعيد العاجلة على ساعات عمل العيادة وتوفر الطبيب.",
    "The dentist examines the problem before recommending treatment.": "يفحص طبيب الأسنان المشكلة قبل التوصية بالعلاج.",
    "Do I need an appointment for an urgent dental problem?": "هل أحتاج إلى موعد لمشكلة أسنان عاجلة؟",
    "Call the centre first. Availability depends on clinic hours and the clinicians working at that time.": "اتصل بالمركز أولاً. يعتمد توفر الموعد على ساعات العمل والأطباء الموجودين في ذلك الوقت.",
    "What if I have facial swelling?": "ماذا أفعل إذا كان لدي تورم في الوجه؟",
    "Dental swelling should be assessed promptly. If swelling affects breathing or swallowing, seek emergency medical care.": "يجب تقييم تورم الأسنان سريعاً. وإذا أثر التورم في التنفس أو البلع، فاطلب الرعاية الطبية الطارئة.",
    "Can you tell me the treatment before I arrive?": "هل يمكنكم تحديد العلاج قبل وصولي؟",
    "No. The dentist needs to assess the cause before recommending treatment.": "لا. يحتاج طبيب الأسنان إلى تقييم السبب قبل التوصية بالعلاج.",
    "A practical first point of care.": "بداية عملية للرعاية.",
    "Dental examinations": "فحوصات الأسنان",
    "Fillings and routine restorative care": "حشوات ورعاية ترميمية دورية",
    "Referral to specialists when needed": "إحالة إلى الاختصاصيين عند الحاجة",
    "What a general dentist can help with": "كيف يمكن لطبيب الأسنان العام مساعدتك؟",
    "For routine dental concerns, check-ups or a problem you are not sure how to classify, a general dentist is usually the best place to start.": "عند وجود مشكلة أسنان يومية أو رغبة في الفحص أو شك في نوع الحالة، يكون طبيب الأسنان العام غالباً أفضل نقطة للبدء.",
    "General dentistry covers routine examination, diagnosis, preventive care and common restorative needs. It is often the right starting point when you have a concern but do not yet know whether specialist care is needed.": "يشمل طب الأسنان العام الفحص الدوري والتشخيص والوقاية والاحتياجات الترميمية الشائعة. وغالباً ما يكون نقطة البداية المناسبة عندما تكون لديك مشكلة ولا تعرف بعد إن كنت تحتاج إلى رعاية تخصصية.",
    "Routine and restorative care": "رعاية دورية وترميمية",
    "Depending on clinical findings, care may include examinations, fillings, treatment of damaged teeth, preventive advice and hygiene support. More complex problems can be referred to the relevant specialist within the team.": "بحسب نتائج الفحص، قد تشمل الرعاية الفحوصات والحشوات وعلاج الأسنان المتضررة والنصائح الوقائية ودعم نظافة الفم. ويمكن إحالة الحالات الأكثر تعقيداً إلى الاختصاصي المناسب ضمن الفريق.",
    "A simple care pathway": "مسار رعاية بسيط",
    "Understand the concern and assess the teeth and gums.": "افهم المشكلة وقيّم الأسنان واللثة.",
    "Explain": "اشرح",
    "Discuss findings and the treatment options that apply.": "ناقش النتائج وخيارات العلاج المناسبة.",
    "Treat or refer": "عالج أو أحِل",
    "Provide general care or involve a specialist when needed.": "قدّم الرعاية العامة أو أشرك اختصاصياً عند الحاجة.",
    "Find a general dentist": "ابحث عن طبيب أسنان عام",
    "Our general dentists provide assessment, preventive and restorative care, with specialist referral available within the team when needed.": "يقدم أطباء الأسنان العامون لدينا التقييم والرعاية الوقائية والترميمية، مع إمكانية الإحالة إلى اختصاصي ضمن الفريق عند الحاجة.",
    "How often should I have a dental check-up?": "كم مرة ينبغي أن أجري فحصاً للأسنان؟",
    "The right interval depends on your oral health and risk factors. Your dentist can recommend a review schedule after examining you.": "يعتمد الفاصل المناسب على صحة فمك وعوامل الخطورة لديك. ويمكن لطبيبك اقتراح جدول للمراجعة بعد فحصك.",
    "Can a general dentist refer me to a specialist?": "هل يستطيع طبيب الأسنان العام إحالتي إلى اختصاصي؟",
    "Yes. If the problem needs specialist care, the dentist can direct you to the appropriate discipline.": "نعم. إذا احتاجت المشكلة إلى رعاية تخصصية، يوجهك الطبيب إلى الاختصاص المناسب.",
    "Do you provide preventive dental care?": "هل تقدمون رعاية أسنان وقائية؟",
    "Yes. Preventive planning and oral-hygiene support are part of general dental care, based on individual needs.": "نعم. يشكل التخطيط الوقائي ودعم نظافة الفم جزءاً من رعاية الأسنان العامة، وفق احتياجات كل شخص.",
    "Specialist orthodontic assessment.": "تقييم تخصصي لتقويم الأسنان.",
    "Fixed braces": "تقويم ثابت",
    "Clear aligners": "صفافات شفافة",
    "Bite and alignment planning": "تخطيط للإطباق واصطفاف الأسنان",
    "What orthodontic treatment addresses": "ما الذي يعالجه تقويم الأسنان؟",
    "Concerned about tooth alignment or your bite? Our orthodontic specialists assess the problem first, then discuss the treatment options that fit the case.": "هل يقلقك اصطفاف الأسنان أو الإطباق؟ يقيّم اختصاصيو التقويم المشكلة أولاً، ثم يناقشون خيارات العلاج المناسبة للحالة.",
    "Orthodontic care focuses on tooth alignment and the way the upper and lower teeth meet. A specialist assessment helps determine whether treatment is needed and which approach fits the case.": "تركز رعاية تقويم الأسنان على اصطفاف الأسنان وطريقة التقاء الأسنان العلوية والسفلية. ويساعد تقييم الاختصاصي في تحديد الحاجة إلى العلاج والنهج المناسب للحالة.",
    "Braces or clear aligners?": "تقويم ثابت أم صفافات شفافة؟",
    "The right appliance depends on the bite, tooth position, age and treatment goals. Options may include fixed braces, clear aligners such as Invisalign in selected cases, and retainers after active treatment. Not every option is suitable for every patient.": "يعتمد الجهاز المناسب على الإطباق وموضع الأسنان والعمر وأهداف العلاج. وقد تشمل الخيارات التقويم الثابت أو الصفافات الشفافة مثل Invisalign في حالات مختارة والمثبتات بعد العلاج الفعال. ولا يناسب كل خيار جميع المرضى.",
    "Review alignment, bite and records needed for diagnosis.": "راجع الاصطفاف والإطباق والسجلات اللازمة للتشخيص.",
    "Discuss the recommended appliance and treatment goals.": "ناقش الجهاز الموصى به وأهداف العلاج.",
    "Review": "راجع",
    "Regular appointments monitor movement and oral health.": "تتابع المواعيد المنتظمة حركة الأسنان وصحة الفم.",
    "Our orthodontic team": "فريق تقويم الأسنان",
    "Choose a profile to learn more about each orthodontist’s background and clinical interests.": "اختر ملفاً للتعرف إلى خبرة كل اختصاصي تقويم واهتماماته السريرية.",
    "Are braces the only option?": "هل التقويم هو الخيار الوحيد؟",
    "No. Depending on the case, options may include fixed braces or clear aligners. A specialist assessment determines what is appropriate.": "لا. قد تشمل الخيارات، بحسب الحالة، التقويم الثابت أو الصفافات الشفافة. ويحدد تقييم الاختصاصي ما يناسبك.",
    "Can adults have orthodontic treatment?": "هل يستطيع الكبار الخضوع لتقويم الأسنان؟",
    "Yes. Orthodontic treatment can be considered for adults as well as children and teenagers, depending on clinical findings.": "نعم. يمكن التفكير في تقويم الأسنان للكبار كما للأطفال واليافعين، بحسب نتائج الفحص السريري.",
    "Will I need retainers after treatment?": "هل سأحتاج إلى مثبتات بعد العلاج؟",
    "Retention is commonly part of orthodontic care. Your orthodontist will explain the retention plan that applies to your case.": "تُعد المثبتات جزءاً شائعاً من رعاية التقويم. وسيشرح لك اختصاصي التقويم خطة التثبيت المناسبة لحالتك.",
    "Call the centre or send a consultation request. Reception can help direct you to the appropriate dentist or specialist.": "اتصل بالمركز أو أرسل طلب استشارة. يمكن للاستقبال توجيهك إلى طبيب الأسنان أو الاختصاصي المناسب.",
    "Bani Yas Tower, Building 117 C Floor, W Corniche Road.": "برج بني ياس، المبنى 117، الطابق C، شارع سلطان بن زايد الأول، طريق الكورنيش الغربي.",
    "Treatment overview": "نظرة عامة على العلاج",
    "Talk to our team": "تحدث مع فريقنا",
  });

  Object.assign(arabic, {
    "Profile notes": "ملاحظات الملف",
    "Consultation": "الاستشارة",
    "Location & directions": "الموقع والاتجاهات",
    "Clinical focus": "مجالات الاهتمام السريري",
    "Related care": "الرعاية ذات الصلة",
    "General Dentistry →": "طب الأسنان العام ←",
    "Cosmetic Dentistry →": "طب الأسنان التجميلي ←",
    "Dental Implants →": "زراعة الأسنان ←",
    "Orthodontics & Braces →": "تقويم الأسنان ←",
    "View all treatments →": "عرض جميع العلاجات ←",
    "View treatments →": "عرض العلاجات ←",
    "View all doctors →": "عرض جميع الأطباء ←",
    "View profile →": "عرض الملف ←",
    "Explore Dental Implants →": "استكشف زراعة الأسنان ←",
    "Email the centre": "راسل المركز",
    "Established dental care in Abu Dhabi since 1980.": "رعاية أسنان راسخة في أبوظبي منذ عام 1980.",
    "Dr. Munir Silwadi Dental Centre": "مركز الدكتور منير السلوادي لطب الأسنان",
    "Bani Yas Tower, Building 117 C Floor": "برج بني ياس، المبنى 117، الطابق C",
    "Sultan Bin Zayed The First St, W Corniche Road, Abu Dhabi, UAE": "شارع سلطان بن زايد الأول، طريق الكورنيش الغربي، أبوظبي، الإمارات العربية المتحدة",
    "F14 & F15, Level 1, Al Raha Mall, Abu Dhabi, UAE": "F14 وF15، الطابق الأول، الراحة مول، أبوظبي، الإمارات العربية المتحدة",
    "Bani Yas Tower and Al Raha Mall, Abu Dhabi, UAE": "برج بني ياس والراحة مول، أبوظبي، الإمارات العربية المتحدة",
    "Both locations, Abu Dhabi": "كلا الفرعين في أبوظبي",
    "Al Raha Mall, Abu Dhabi": "الراحة مول، أبوظبي",
    "35 years+ experience": "خبرة تزيد على 35 عاماً",
    "Full-mouth rehabilitation": "إعادة تأهيل الفم بالكامل",
    "Root canal treatment": "علاج جذور الأسنان",
    "Conservative care": "علاج محافظ",
    "Diagnostic support": "دعم تشخيصي",
    "Complex restorative care": "رعاية ترميمية معقدة",
    "Maintenance": "المتابعة والمحافظة",
    "Orthodontic assessment": "تقييم تقويم الأسنان",
    "Specialist planning": "تخطيط تخصصي",
    "Academic experience": "خبرة أكاديمية",
    "Pediatric care": "رعاية الأطفال",
    "Family communication": "التواصل مع العائلة",
    "Braces": "تقويم الأسنان",
    "Lingual braces": "تقويم لساني",
    "Digital orthodontics": "تقويم رقمي",
    "Aligners": "صفافات شفافة",
    "Endodontic assessment": "تقييم علاج الجذور",
    "Tooth preservation": "الحفاظ على الأسنان الطبيعية",
    "Implantology": "زراعة الأسنان",
    "Implant dentistry interest": "اهتمام بزراعة الأسنان",
    "Digital Smile Design": "تصميم رقمي للابتسامة",
    "Crowns & restorative care": "التيجان والرعاية الترميمية",
    "CAD / CAM restorations": "ترميمات CAD/CAM",
    "Canadian Dental Board Certificate": "شهادة مجلس طب الأسنان الكندي",
    "Fellow, International College of Dentists": "زميل الكلية الدولية لأطباء الأسنان",
    "Fellow, Academy of Dentistry International": "زميل الأكاديمية الدولية لطب الأسنان",
    "CEREC Master and ISCD Certified International Trainer": "ماجستير CEREC ومدرب دولي معتمد من ISCD",
    "DOH licensed in prosthodontics and implantology": "مرخص من دائرة الصحة في التركيبات وزراعة الأسنان",
    "DHA licensed in prosthodontics and implantology": "مرخص من هيئة الصحة بدبي في التركيبات وزراعة الأسنان",
    "Treatment interests": "الاهتمامات العلاجية",
    "General Dentist": "طبيب أسنان عام",
    "Specialist Endodontics": "اختصاصي علاج الجذور",
    "Specialist Periodontics": "اختصاصي أمراض اللثة",
    "Consultant Orthodontics": "استشاري تقويم الأسنان",
    "Specialist Orthodontist": "اختصاصي تقويم الأسنان",
    "Pediatric Dentist": "اختصاصي طب أسنان الأطفال",
    "Periodontist & Implantologist": "اختصاصي أمراض اللثة وزراعة الأسنان",
    "Prosthodontist & Implantologist": "اختصاصي تركيبات وزراعة الأسنان",
    "Dr. Afnan Mashal is a general dentist whose current public centre profile records more than 35 years of dental experience and interests across restorative and aesthetic care.": "الدكتورة أفنان مشعل طبيبة أسنان عامة، ويسجل ملفها المنشور في المركز خبرة تزيد على 35 عاماً واهتماماً بالعلاج الترميمي والتجميلي.",
    "Prevention, diagnosis and general restorative treatment.": "الوقاية والتشخيص والعلاج الترميمي العام.",
    "Her public profile notes experience with CAD/CAM dental workflows.": "يذكر ملفها المنشور خبرتها في سير عمل طب الأسنان بتقنيات CAD/CAM.",
    "Smile makeovers, reshaping and anterior restorative work are listed among her interests.": "تشمل اهتماماتها تجميل الابتسامة وإعادة تشكيلها وترميم الأسنان الأمامية.",
    "Her profile also references full-mouth rehabilitation and dental prostheses.": "ويشير ملفها أيضاً إلى إعادة تأهيل الفم بالكامل وتركيبات الأسنان.",
    "The centre’s public profile records more than 35 years of experience and a broad GP scope including endodontic and prosthetic restorative care.": "يسجل الملف المنشور للمركز خبرة تزيد على 35 عاماً ونطاقاً واسعاً في طب الأسنان العام يشمل علاج الجذور والترميمات التعويضية.",
    "Dr. Ahmed El Shehri is a specialist endodontist focused on diagnosis and root canal care. His public centre profile describes a conservative, minimally invasive approach to endodontic treatment.": "الدكتور أحمد الشهري اختصاصي في علاج الجذور، يركز على التشخيص وعلاج قنوات الجذر. ويصف ملفه المنشور نهجاً محافظاً وقليل التدخل في علاج الجذور.",
    "Specialist assessment and non-surgical root canal care.": "تقييم تخصصي وعلاج غير جراحي لقنوات الجذر.",
    "A minimally invasive approach aimed at preserving natural tooth structure where clinically possible.": "نهج قليل التدخل يهدف إلى الحفاظ على بنية السن الطبيعية متى كان ذلك ممكناً سريرياً.",
    "His public profile references digital radiography and 3D imaging as part of endodontic assessment.": "يذكر ملفه المنشور التصوير الشعاعي الرقمي والتصوير ثلاثي الأبعاد ضمن تقييم علاج الجذور.",
    "His current centre profile emphasizes patient education, conservative treatment planning and the use of diagnostic imaging to support endodontic care.": "يركز ملفه الحالي في المركز على تثقيف المريض والتخطيط المحافظ للعلاج واستخدام التصوير التشخيصي لدعم علاج الجذور.",
    "Dr. Dana Awad is a dedicated General Dentist at Dr. Munir Silwadi Dental Centre, providing comprehensive dental care with a strong focus on preventive, restorative, and esthetic dentistry. She is committed to delivering evidence-based, patient-centered treatment while creating a comfortable and reassuring experience for every patient.": "الدكتورة دانا عوض طبيبة أسنان عامة في مركز الدكتور منير السلوادي لطب الأسنان، وتقدم رعاية شاملة مع تركيز على طب الأسنان الوقائي والترميمي والتجميلي. وهي حريصة على تقديم علاج يستند إلى الدليل ويتمحور حول المريض، مع توفير تجربة مريحة ومطمئنة لكل مريض.",
    "Dr. Ehab Hassouneh Bassam A is listed as a General Dentist at Dr. Munir Silwadi Dental Centre. The centre's updated medical team list confirms practice at Al Raha Mall.": "يُدرج الدكتور إيهاب حسونة بسام أ كطبيب أسنان عام في مركز الدكتور منير السلوادي لطب الأسنان. وتؤكد قائمة الفريق الطبي المحدثة في المركز ممارسته في الراحة مول.",
    "Assessment and management of common dental concerns.": "تقييم المشكلات السنية الشائعة وإدارتها.",
    "Routine examinations and preventive planning.": "فحوصات دورية وتخطيط وقائي.",
    "Restorative treatment based on clinical findings.": "علاج ترميمي يستند إلى نتائج الفحص السريري.",
    "This profile is intentionally limited to the doctor’s confirmed role and location from the centre’s current medical team list. Contact reception for appointment availability and further information.": "يقتصر هذا الملف على دور الطبيب وموقعه المؤكدين وفق قائمة الفريق الطبي الحالية في المركز. تواصل مع الاستقبال لمعرفة المواعيد المتاحة والمزيد من المعلومات.",
    "Dr. Fahed Abi Khalil is a specialist in periodontics. His public centre profile highlights periodontal care, implant dentistry and long-term continuing education.": "الدكتور فهد أبي خليل اختصاصي في أمراض اللثة. ويسلط ملفه المنشور في المركز الضوء على رعاية اللثة وزراعة الأسنان والتعليم المستمر.",
    "Assessment and treatment of gum health and the tissues supporting the teeth.": "تقييم صحة اللثة والأنسجة الداعمة للأسنان وعلاجها.",
    "Implant dentistry is listed as a particular clinical interest in his public profile.": "ترد زراعة الأسنان ضمن اهتماماته السريرية الخاصة في ملفه المنشور.",
    "Ongoing periodontal review and prevention are part of specialist gum care.": "تشكل المراجعة الدورية للثة والوقاية جزءاً من رعاية اللثة التخصصية.",
    "His public profile also records membership of the American Academy of Periodontology and Lebanese periodontal organisations.": "يسجل ملفه المنشور أيضاً عضويته في الأكاديمية الأمريكية لأمراض اللثة ومنظمات أمراض اللثة اللبنانية.",
    "Dr. Hani Hasbini is a consultant orthodontist with a long academic and clinical career spanning Lebanon, France and the UAE.": "الدكتور هاني حسبيني استشاري تقويم أسنان، وله مسيرة أكاديمية وسريرية طويلة في لبنان وفرنسا والإمارات.",
    "Consultant-led assessment of tooth alignment and bite relationships.": "تقييم بإشراف استشاري لاصطفاف الأسنان وعلاقات الإطباق.",
    "Orthodontic treatment planning across different ages and case types.": "تخطيط علاج تقويم الأسنان لمختلف الأعمار والحالات.",
    "His public profile records longstanding university teaching and postgraduate orthodontic involvement.": "يسجل ملفه المنشور خبرة طويلة في التدريس الجامعي والمشاركة في برامج تقويم الأسنان للدراسات العليا.",
    "His centre profile also records professional memberships across Lebanese, French, Arab, European and international orthodontic organisations.": "يسجل ملفه في المركز أيضاً عضوياته المهنية في منظمات تقويم الأسنان اللبنانية والفرنسية والعربية والأوروبية والدولية.",
    "Dr. Kashmira Pawar Jayprakash is listed as a Pediatric Dentist at Dr. Munir Silwadi Dental Centre. The centre’s updated medical team list confirms practice at Al Raha Mall.": "تُدرج الدكتورة كاشميرا باوار جايبراكاش كاختصاصية في طب أسنان الأطفال في مركز الدكتور منير السلوادي لطب الأسنان. وتؤكد قائمة الفريق الطبي المحدثة في المركز ممارستها في الراحة مول.",
    "Dr. Kashmira Pawar Jayprakash is listed as a Pediatric Dentist at Dr. Munir Silwadi Dental Centre. The centre's updated medical team list confirms practice at Al Raha Mall.": "تُدرج الدكتورة كاشميرا باوار جايبراكاش كاختصاصية في طب أسنان الأطفال في مركز الدكتور منير السلوادي لطب الأسنان. وتؤكد قائمة الفريق الطبي المحدثة في المركز ممارستها في الراحة مول.",
    "Dental assessment and care for children and adolescents.": "تقييم ورعاية أسنان الأطفال واليافعين.",
    "Age-appropriate preventive guidance and planning.": "إرشادات وتخطيط وقائيان يناسبان العمر.",
    "Clear explanations for children and their families.": "شرح واضح للأطفال وعائلاتهم.",
    "Dr. Krishnamurthy Balajee is a specialist orthodontist whose current public centre profile records 25 years of practice in the GCC and experience across braces, lingual orthodontics and clear aligners.": "الدكتور كريشنامورثي بالاجي اختصاصي تقويم أسنان، ويسجل ملفه المنشور الحالي في المركز خبرة 25 عاماً في دول الخليج وتجربة في التقويم الثابت واللساني والصفافات الشفافة.",
    "Fixed orthodontic options for children, teenagers and adults are included in his current profile.": "تشمل خبرته الحالية خيارات التقويم الثابت للأطفال واليافعين والكبار.",
    "Clear aligners are part of his stated orthodontic practice.": "تشكل الصفافات الشفافة جزءاً من ممارسته في تقويم الأسنان.",
    "His public profile records longstanding experience with lingual braces.": "يسجل ملفه المنشور خبرة طويلة في التقويم اللساني.",
    "Digital scanning and 3D diagnostic workflows are also described in his centre profile.": "ويصف ملفه في المركز أيضاً المسح الرقمي وسير العمل التشخيصي ثلاثي الأبعاد.",
    "25 years of orthodontic practice in the GCC, as stated in his current public profile": "25 عاماً من ممارسة تقويم الأسنان في دول الخليج، وفق ملفه المنشور الحالي",
    "Fellow, Pierre Fauchard Academy": "زميل أكاديمية بيير فوشار",
    "Active membership, European Society of Lingual Orthodontics (ESLO), as recorded by the centre": "عضوية فعالة في الجمعية الأوروبية للتقويم اللساني (ESLO)، وفق سجلات المركز",
    "His centre profile describes work across preventive, interceptive, teen and adult orthodontics using contemporary fixed and aligner systems.": "يصف ملفه في المركز خبرته في تقويم الأسنان الوقائي والاعتراضي وتقويم اليافعين والكبار باستخدام أنظمة التقويم والصفافات الحديثة.",
    "Dr. Lana Masoud is listed as a Endodontist at Dr. Munir Silwadi Dental Centre. The centre's updated medical team list confirms practice at Al Raha Mall.": "تُدرج الدكتورة لانا مسعود كاختصاصية في علاج الجذور في مركز الدكتور منير السلوادي لطب الأسنان. وتؤكد قائمة الفريق الطبي المحدثة في المركز ممارستها في الراحة مول.",
    "Diagnosis of conditions affecting the dental pulp and root canal system.": "تشخيص الحالات التي تصيب لب السن وقنوات الجذر.",
    "Root canal treatment planning based on clinical findings.": "تخطيط علاج الجذور استناداً إلى نتائج الفحص السريري.",
    "Care focused on preserving natural teeth where clinically appropriate.": "رعاية تركز على الحفاظ على الأسنان الطبيعية عندما يكون ذلك مناسباً سريرياً.",
    "Dr. Moammar Mohamed Rifai is a specialist orthodontist whose public profile records clinical practice in Abu Dhabi since 2000 and work with Silwadi Dental Center since 2011.": "الدكتور معمر محمد الرفاعي اختصاصي تقويم أسنان، ويسجل ملفه المنشور ممارسة سريرية في أبوظبي منذ عام 2000 وعمله مع مركز سلوادي لطب الأسنان منذ عام 2011.",
    "Assessment and treatment planning for alignment and bite correction.": "تقييم وتخطيط علاج اصطفاف الأسنان وتصحيح الإطباق.",
    "His public profile lists straight-wire, self-ligating and orthopaedic appliances among the techniques he uses.": "يذكر ملفه المنشور أجهزة السلك المستقيم والربط الذاتي والأجهزة التقويمية العظمية ضمن التقنيات التي يستخدمها.",
    "Clear aligner treatment is also listed among his orthodontic approaches.": "ويذكر الملف أيضاً علاج الصفافات الشفافة ضمن أساليبه في التقويم.",
    "His profile also records teaching at Beirut Arab University and lecturing at the Lebanese Dental Association congress.": "يسجل ملفه أيضاً التدريس في جامعة بيروت العربية وإلقاء المحاضرات في مؤتمر نقابة أطباء الأسنان اللبنانية.",
    "Dr. Moheb Silwadi is a general dentist whose public centre profile highlights cosmetic, restorative and implant dentistry, with a strong interest in digital workflows.": "الدكتور مهيب سلوادي طبيب أسنان عام، ويسلط ملفه المنشور في المركز الضوء على تجميل الأسنان والعلاج الترميمي وزراعة الأسنان، مع اهتمام واضح بالتقنيات الرقمية.",
    "Smile-focused restorative planning, veneers and cosmetic fillings.": "تخطيط ترميمي يركز على الابتسامة وقشور الأسنان والحشوات التجميلية.",
    "Digital Smile Design and computer-aided restorative workflows.": "التصميم الرقمي للابتسامة وسير العمل الترميمي بمساعدة الحاسوب.",
    "Dental implants and implant-supported restorative care are listed among his clinical interests.": "ترد زراعة الأسنان والرعاية الترميمية المدعومة بالزراعة ضمن اهتماماته السريرية.",
    "Crowns, partial crowns and broader general restorative treatment.": "تيجان وتيجان جزئية وعلاج ترميمي عام أوسع.",
    "His current public profile also lists certificates in cosmetic and computer-aided dentistry.": "يسجل ملفه المنشور الحالي أيضاً شهادات في تجميل الأسنان وطب الأسنان بمساعدة الحاسوب.",
    "Dr. Munir Silwadi's clinical work includes implantology, full-mouth rehabilitation and CAD/CAM aesthetic dentistry. His professional profile also includes international lecturing and CEREC training.": "يشمل عمل الدكتور منير سلوادي السريري زراعة الأسنان وإعادة تأهيل الفم بالكامل وطب الأسنان التجميلي بتقنيات CAD/CAM. ويتضمن ملفه المهني أيضاً محاضرات دولية وتدريباً على تقنية CEREC.",
    "Book a consultation with Dr. Munir Silwadi": "احجز استشارة مع د. منير سلوادي",
    "Selected areas highlighted in Dr. Silwadi's professional profile include implant and restorative treatment planning, complex rehabilitation and digital aesthetic workflows.": "تشمل المجالات التي يبرزها الملف المهني للدكتور سلوادي تخطيط علاج الزراعة والترميم وإعادة التأهيل المعقدة وسير العمل التجميلي الرقمي.",
    "Immediate implant and computer-guided implant workflows in selected cases.": "زراعة فورية وسير عمل موجّه بالحاسوب في حالات مختارة.",
    "Comprehensive restorative planning for complex prosthodontic cases.": "تخطيط ترميمي شامل لحالات التركيبات المعقدة.",
    "Digital workflows for selected crowns, veneers and aesthetic restorations.": "سير عمل رقمي لتيجان وقشور وترميمات تجميلية مختارة.",
    "Digital visual planning used to support restorative and aesthetic communication.": "تخطيط بصري رقمي لدعم التواصل حول الترميم والنتيجة التجميلية.",
    "Dr. Silwadi's published centre profile highlights immediate implants, All-on-4 / All-on-6 concepts, computer-guided implant treatment, full-mouth rehabilitation, CAD/CAM veneers and crowns, and digital smile design. Suitability for any treatment is determined after clinical assessment.": "يبرز ملف الدكتور سلوادي المنشور في المركز الزراعة الفورية ومفاهيم All-on-4 وAll-on-6 وعلاج الزراعة الموجّه بالحاسوب وإعادة تأهيل الفم بالكامل وقشور وتيجان CAD/CAM وتصميم الابتسامة الرقمي. وتُحدد ملاءمة أي علاج بعد التقييم السريري.",
    "Silwadi Dental Center's multidisciplinary team includes clinicians across orthodontics, periodontics, endodontics and general dentistry.": "يضم فريق مركز سلوادي متعدد التخصصات أطباء في تقويم الأسنان وأمراض اللثة وعلاج الجذور وطب الأسنان العام.",
    "Dr. Nachiket Shah is listed as a Periodontist & Implantologist at Dr. Munir Silwadi Dental Centre. The centre's updated medical team list confirms practice at Al Raha Mall.": "يُدرج الدكتور ناشيكيت شاه كاختصاصي في أمراض اللثة وزراعة الأسنان في مركز الدكتور منير السلوادي لطب الأسنان. وتؤكد قائمة الفريق الطبي المحدثة في المركز ممارسته في الراحة مول.",
    "Assessment and care for the gums and supporting tissues.": "تقييم اللثة والأنسجة الداعمة والعناية بها.",
    "Implant assessment and treatment planning for suitable patients.": "تقييم الزراعة وتخطيط العلاج للمرضى المناسبين.",
    "Ongoing periodontal review based on clinical needs.": "مراجعة دورية للثة وفق الاحتياجات السريرية.",
    "Dr. Nasr Keshkiea is listed as a General Dentist at Dr. Munir Silwadi Dental Centre. The centre's updated medical team list confirms practice at Bani Yas Tower.": "يُدرج الدكتور نصر كشكية كطبيب أسنان عام في مركز الدكتور منير السلوادي لطب الأسنان. وتؤكد قائمة الفريق الطبي المحدثة في المركز ممارسته في برج بني ياس.",
    "Dr. Sara Ismail is listed as a General Dentist at Dr. Munir Silwadi Dental Centre. The centre's updated medical team list confirms practice at Al Raha Mall.": "تُدرج الدكتورة سارة إسماعيل كطبيبة أسنان عامة في مركز الدكتور منير السلوادي لطب الأسنان. وتؤكد قائمة الفريق الطبي المحدثة في المركز ممارستها في الراحة مول.",
  });

  return { init, applyLanguage, getLanguage, getRequestedLanguage, translate, withLanguageQuery };
});
