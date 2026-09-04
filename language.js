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

  return { init, applyLanguage, getLanguage, getRequestedLanguage, translate, withLanguageQuery };
});
