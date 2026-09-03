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
  };

  const normalize = value => String(value ?? '').replace(/\s+/g, ' ').trim();

  function translate(value, language = currentLanguage) {
    const clean = normalize(value);
    if (language !== 'ar' || !clean) return clean;
    if (arabic[clean]) return arabic[clean];
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

    document.querySelectorAll?.('[placeholder], [aria-label], [title]').forEach(element => {
      ['placeholder', 'aria-label', 'title'].forEach(attribute => {
        if (element.hasAttribute(attribute)) translateAttribute(element, attribute, currentLanguage);
      });
    });

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
    currentLanguage = saved === 'ar' ? 'ar' : 'en';
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

  return { init, applyLanguage, getLanguage, translate };
});
