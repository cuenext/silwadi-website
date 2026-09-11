(() => {
  'use strict';

  const root = document.querySelector('[data-ai-assistant]');
  if (!root) return;

  const form = root.querySelector('[data-ai-form]');
  const input = root.querySelector('[data-ai-input]');
  const submit = root.querySelector('[data-ai-submit]');
  const count = root.querySelector('[data-ai-count]');
  const status = root.querySelector('[data-ai-status]');
  const answer = root.querySelector('[data-ai-answer]');
  const contacts = root.querySelector('[data-ai-contact-actions]');
  const suggestions = root.querySelectorAll('[data-ai-suggestion]');

  const MAX_QUESTION_LENGTH = 500;
  const REQUEST_TIMEOUT_MS = 12000;
  const REVIEW_CLINIC_URL = '../ai/clinic-knowledge-v1.json';
  const REVIEW_DENTAL_URL = '../ai/dental-guidance-v1.json';
  const REVIEW_MODE = 'review-demo';
  const PEDIATRIC_DOCTOR = 'Dr. Kashmira Pawar Jayprakash';
  const PEDIATRIC_ROLE = 'Specialist Pediatric Dentist';
  let activeController = null;
  let reviewDataPromise = null;

  const containsArabic = (value) => /[\u0600-\u06FF]/.test(value || '');

  const urgentPatterns = [
    /can't breathe|cannot breathe|difficulty breathing|trouble breathing/i,
    /can't swallow|cannot swallow|difficulty swallowing|trouble swallowing/i,
    /uncontrolled bleeding|bleeding won't stop|bleeding will not stop/i,
    /severe (face|facial) swelling|rapid(ly)? worsening (face|facial) swelling/i,
    /serious (dental|facial) trauma|major (dental|facial) trauma|knocked out tooth.*(heavy|uncontrolled) bleeding/i,
    /صعوبة.{0,20}التنفس|لا أستطيع.{0,20}التنفس|مش قادر.{0,20}اتنفس/i,
    /صعوبة.{0,20}البلع|لا أستطيع.{0,20}البلع|مش قادر.{0,20}ابلع/i,
    /نزيف.{0,30}(لا يتوقف|ما بيوقف|مستمر بشدة|شديد)/i,
    /تورم.{0,30}(شديد|كبير|يزداد بسرعة)/i,
    /إصابة.{0,25}(خطيرة|شديدة)|حادث.{0,25}(قوي|شديد)/i
  ];

  const medicationPatterns = [
    /what dose|which dose|how many mg|how much .*mg|dose of/i,
    /should i take|can i take|which antibiotic|prescribe|medication dose/i,
    /stop (my|the) medication|change (my|the) medication/i,
    /جرعة|كم.{0,20}(ملغ|مليغرام)|أي.{0,20}مضاد|اي.{0,20}مضاد/i,
    /(آخذ|اخذ|أخذ).{0,30}(دواء|مضاد)|أوقف.{0,20}(دواء|العلاج)|أغير.{0,20}(دواء|العلاج)/i
  ];

  const liveConfirmationPatterns = [
    /how much|what(?:'s| is) the price|price of|cost of|fee for/i,
    /covered by|does .*insurance cover|does .*daman cover|insurance coverage/i,
    /available (today|tomorrow|on|at)|free (today|tomorrow|on|at)|appointment slot|doctor schedule/i,
    /كم السعر|ما السعر|سعر.{0,20}(العلاج|التقويم|الزراعة)|التكلفة/i,
    /يغطي.{0,30}(التأمين|ضمان)|تأمين.{0,30}يغطي/i,
    /موعد.{0,30}(اليوم|بكرة|غداً|غدا)|متاح.{0,30}(اليوم|بكرة|غداً|غدا)|جدول.{0,20}الدكتور/i
  ];

  const arabicGuidance = {
    'bleeding-gums': 'قد يحدث نزيف اللثة عند تهيج أو التهاب اللثة، وغالباً حول مناطق تراكم البلاك. يساعد التنظيف اللطيف والجيد بالفرشاة وبين الأسنان، لكن النزيف المستمر أو المتكرر يحتاج تقييماً لدى طبيب الأسنان لأن أسبابه قد تكون متعددة.',
    'root-canal': 'يُستخدم علاج العصب لمعالجة داخل السن عندما يكون لب السن ملتهباً أو مصاباً أو غير سليم. تتم إزالة النسيج المتأثر وتنظيف القنوات وإغلاقها، ويحدد طبيب الأسنان بعد الفحص والصور اللازمة ما إذا كان العلاج مناسباً.',
    'dental-x-rays': 'تساعد أشعة الأسنان في إظهار مناطق لا يمكن رؤيتها بالفحص السريري وحده، مثل التسوس بين الأسنان ومستوى العظم وبعض الالتهابات والأسنان النامية. يحدد طبيب الأسنان الحاجة إلى الأشعة ونوعها حسب الحالة.',
    'first-child-dental-visit': 'يُنصح عادةً بأن تكون الزيارة الأولى للطفل مع ظهور أول سن، وبحد أقصى قرب عمر سنة. يمكن أن تشمل الزيارة فحصاً لطيفاً وإرشادات للتنظيف والغذاء.',
    'fluoride-toothpaste-children': 'يساعد معجون الأسنان بالفلورايد على حماية مينا الأسنان من التسوس. يجب استخدام كمية مناسبة لعمر الطفل مع إشراف أحد الوالدين أو مقدم الرعاية حتى يستطيع الطفل تنظيف أسنانه جيداً بنفسه.',
    'crowns': 'يغطي تاج الأسنان السن ويحميه عندما يحتاج إلى دعم أو ترميم أكبر من الحشوة وحدها. يحتاج طبيب الأسنان إلى فحص السن لتحديد ما إذا كان التاج أو خيار ترميم آخر مناسباً.',
    'whitening': 'يهدف تبييض الأسنان الاحترافي إلى تفتيح لون الأسنان الطبيعية. تختلف النتائج، كما أن الحشوات والتيجان والقشور لا تبيض بالطريقة نفسها، لذلك يساعد الفحص في تحديد ما إذا كان التبييض مناسباً.',
    'dental-implants': 'زرعة الأسنان هي بديل لجذر السن يوضع في عظم الفك لدعم تاج أو جسر أو ترميم آخر. الملاءمة تعتمد على الفم والعظم واللثة والتاريخ الطبي ومنطقة العلاج، وتحتاج إلى تقييم وفحوص مناسبة.',
    'brushing-and-interdental-cleaning': 'بالنسبة لمعظم الأشخاص، تنظيف الأسنان مرتين يومياً بمعجون أسنان يحتوي على الفلورايد هو روتين عملي. كما يساعد تنظيف ما بين الأسنان بالخيط أو الفرش البينية أو وسيلة مناسبة أخرى على إزالة البلاك من المناطق التي قد لا تصل إليها الفرشاة.'
  };

  function languageFor(value) {
    return containsArabic(value) ? 'ar' : 'en';
  }

  function setDirection(language) {
    const direction = language === 'ar' ? 'rtl' : 'ltr';
    answer.dir = direction;
    answer.lang = language;
    status.dir = direction;
    status.lang = language;
  }

  function setBusy(isBusy, language) {
    submit.disabled = isBusy;
    input.disabled = isBusy;
    status.dataset.busy = isBusy ? 'true' : 'false';
    if (isBusy) {
      status.textContent = language === 'ar'
        ? 'جارٍ التحقق من معلومات سلوادي…'
        : 'Checking Silwadi information…';
    }
  }

  function clearResult() {
    answer.hidden = true;
    answer.textContent = '';
    contacts.hidden = true;
    status.textContent = '';
    status.dataset.busy = 'false';
  }

  function showAnswer(text, language, mode = 'general', reviewDemo = false) {
    setDirection(language);
    answer.hidden = false;
    answer.textContent = String(text || '').slice(0, 1600);
    status.textContent = reviewDemo
      ? (language === 'ar'
        ? 'وضع مراجعة خاص — إجابة آمنة من معلومات سلوادي المعتمدة، قبل تفعيل اتصال الذكاء الاصطناعي.'
        : 'Private review mode — safe answer from approved Silwadi information before the AI connection is activated.')
      : '';
    status.dataset.busy = 'false';
    contacts.hidden = !['fallback', 'urgent', 'unsafe'].includes(mode);
  }

  function showFallback(language, reason = 'unknown', reviewDemo = false) {
    const connectionMissing = reason === 'endpoint';
    setDirection(language);
    answer.hidden = false;
    answer.textContent = language === 'ar'
      ? (connectionMissing
        ? 'نسخة المراجعة جاهزة، لكن اتصال الذكاء الاصطناعي لم يتم تفعيله بعد. يمكن لفريق الاستقبال مساعدتك الآن.'
        : 'لا أملك معلومات موثقة كافية للإجابة بدقة. يمكن لفريق الاستقبال تأكيد ذلك لك.')
      : (connectionMissing
        ? 'The review interface is ready, but the AI test connection has not been activated yet. Reception can help you in the meantime.'
        : "I don’t have enough verified information to answer that accurately. Reception can confirm this for you.");
    status.textContent = reviewDemo
      ? (language === 'ar' ? 'وضع مراجعة خاص — لم يتم تفعيل اتصال الذكاء الاصطناعي بعد.' : 'Private review mode — AI connection not activated yet.')
      : '';
    status.dataset.busy = 'false';
    contacts.hidden = false;
  }

  function updateCount() {
    const length = input.value.length;
    count.textContent = `${length} / ${MAX_QUESTION_LENGTH}`;
  }

  async function loadReviewData() {
    if (!reviewDataPromise) {
      reviewDataPromise = Promise.all([
        fetch(REVIEW_CLINIC_URL, { cache: 'no-store', credentials: 'omit' }).then((response) => {
          if (!response.ok) throw new Error('Clinic review data unavailable');
          return response.json();
        }),
        fetch(REVIEW_DENTAL_URL, { cache: 'no-store', credentials: 'omit' }).then((response) => {
          if (!response.ok) throw new Error('Dental review data unavailable');
          return response.json();
        })
      ]).then(([clinic, dental]) => ({ clinic, dental }));
    }
    return reviewDataPromise;
  }

  function matchesAny(question, patterns) {
    return patterns.some((pattern) => pattern.test(question));
  }

  function guidanceFor(dental, topic, language) {
    const item = (dental.guidance || []).find((entry) => entry.topic === topic);
    if (!item) return '';
    if (language === 'ar') return arabicGuidance[topic] || '';
    return item.approvedSummary || '';
  }

  function childDentistQuestion(question) {
    return /child|children|kid|pediatric|paediatric|pedodont/i.test(question)
      || /الأطفال|اطفال|طفل|أسنان الأطفال|اسنان الأطفال/i.test(question);
  }

  function founderQuestion(question) {
    return /who.{0,20}(founded|founded the|started|established).{0,30}(silwadi|clinic|centre|center)|who.{0,10}is.{0,10}(the )?founder|founder of/i.test(question)
      || /من.{0,15}(أسس|اسس|مؤسس).{0,25}(سلوادي|العيادة|المركز)|من هو.{0,15}المؤسس|مين.{0,15}(أسس|اسس|المؤسس)/i.test(question);
  }

  function establishedQuestion(question) {
    return /when.{0,20}(silwadi|clinic|centre|center).{0,20}(start|open|founded|established)|when was.{0,20}(silwadi|clinic|centre|center)|since when|what year.{0,20}(silwadi|clinic)/i.test(question)
      || /متى.{0,20}(تأسس|تاسس|افتتح).{0,20}(سلوادي|المركز|العيادة)|منذ متى|أي سنة.{0,20}(تأسس|تاسس|افتتح)/i.test(question);
  }

  function locationsQuestion(question) {
    const asksLocation = /how many.{0,15}(locations|branches)|where are.{0,15}(your )?(locations|branches)|what.{0,10}(locations|branches)|where is silwadi/i.test(question);
    const asksLocationAr = /كم.{0,15}(فرع|فروع)|وين.{0,15}(الفروع|فروعكم|سلوادي)|أين.{0,15}(الفروع|فروعكم|سلوادي)|ما هي.{0,15}(الفروع|المواقع)/i.test(question);
    return asksLocation || asksLocationAr;
  }

  function contactQuestion(question) {
    return /what(?:'s| is).{0,15}(your )?(email|phone|number)|how (?:can|do) i contact|contact (?:you|silwadi)|email address|phone number/i.test(question)
      || /كيف.{0,15}(أتواصل|اتواصل)|رقم.{0,15}(الهاتف|التلفون|سلوادي)|إيميل|ايميل|البريد الإلكتروني|البريد الالكتروني/i.test(question);
  }

  function branchHoursQuestion(question) {
    const asksHours = /hours|opening|open|close|closing/i.test(question)
      || /ساعات|اوقات|أوقات|دوام|يفتح|يغلق|مفتوح/i.test(question);
    if (!asksHours) return '';
    if (/al\s*raha|raha/i.test(question) || /الراحة|الراحه/i.test(question)) return 'al-raha';
    if (/bani\s*yas|corniche/i.test(question) || /بني ياس|الكورنيش/i.test(question)) return 'bani-yas';
    return '';
  }

  function localizeHours(hours, language) {
    if (language !== 'ar') return hours;
    return String(hours || '')
      .replace('Sat–Thu', 'السبت–الخميس')
      .replace('Sun–Wed', 'الأحد–الأربعاء')
      .replace('Thu & Sat', 'الخميس والسبت')
      .replace('Fri closed', 'الجمعة مغلق');
  }

  function rootCanalTopic(question) {
    return /root canal|endodont/i.test(question) || /علاج العصب|سحب العصب|عصب الأسنان|عصب الاسنان|اندودونت/i.test(question);
  }

  function personalRootCanalQuestion(question) {
    if (!rootCanalTopic(question)) return false;
    return /do i need|do we need|does my tooth need|should i (?:get|have|do)|need a root canal|is a root canal necessary|would i need/i.test(question)
      || /هل أحتاج|هل احتاج|هل لازم|هل يجب|بحتاج|محتاج.{0,15}(علاج|سحب).{0,10}العصب|لازم.{0,15}(علاج|سحب).{0,10}العصب/i.test(question);
  }

  function rootCanalServiceQuestion(question) {
    if (!rootCanalTopic(question)) return false;
    return /do you (?:offer|provide|have|do)|does silwadi (?:offer|provide|have|do)|can i (?:get|do|have).{0,20}root canal.{0,20}(at|with|in) silwadi|root canal treatment.{0,15}(available|offered)/i.test(question)
      || /هل.{0,15}(توفرون|تقدمون|عندكم).{0,20}(علاج|سحب).{0,10}العصب|هل سلوادي.{0,15}(يوفر|يقدم).{0,20}(علاج|سحب).{0,10}العصب/i.test(question);
  }

  function bleedingGumsQuestion(question) {
    return /gums?.{0,20}bleed|bleeding gums?|gum bleeding/i.test(question)
      || /نزيف.{0,15}اللثة|اللثة.{0,15}تنزف|لثت(?:ي|ك)?.{0,15}تنزف|نزيف اللثة/i.test(question);
  }

  function topicFromQuestion(question) {
    if (bleedingGumsQuestion(question)) return 'bleeding-gums';
    if (rootCanalTopic(question)) return 'root-canal';
    if (/x-?ray|radiograph/i.test(question) || /أشعة|اشعة/i.test(question)) return 'dental-x-rays';
    if (/first.{0,15}(dental|dentist).{0,15}(visit|child)|first.{0,15}visit.{0,15}child/i.test(question) || /أول.{0,15}زيارة.{0,15}(طفل|للطفل)/i.test(question)) return 'first-child-dental-visit';
    if (/fluoride.{0,20}(child|kid)|toothpaste.{0,20}(child|kid)/i.test(question) || /فلورايد.{0,20}(طفل|الأطفال)|معجون.{0,20}(طفل|الأطفال)/i.test(question)) return 'fluoride-toothpaste-children';
    if (/crown/i.test(question) || /تاج|تلبيسة|تلبيسه/i.test(question)) return 'crowns';
    if (/whiten/i.test(question) || /تبييض/i.test(question)) return 'whitening';
    if (/implant/i.test(question) || /زراعة|زرعة|زرعه/i.test(question)) return 'dental-implants';
    if (/brush|floss|interdental/i.test(question) || /فرشاة|تفريش|خيط الأسنان|خيط الاسنان/i.test(question)) return 'brushing-and-interdental-cleaning';
    return '';
  }

  function endodontistQuestion(question) {
    const asksWho = /who.{0,20}(does|treats|handles|performs)|which.{0,15}(doctor|dentist)|root canal doctor|endodontist/i.test(question)
      || /مين.{0,20}(يعمل|يعالج|يسوي)|أي.{0,15}(دكتور|طبيب)|طبيب.{0,10}العصب|أخصائي.{0,10}العصب|اخصائي.{0,10}العصب/i.test(question);
    return asksWho && rootCanalTopic(question);
  }

  function doctorBranchLabel(branches) {
    return (branches || []).map((branch) => branch === 'al-raha' ? 'Al Raha Mall' : branch === 'bani-yas' ? 'Bani Yas Tower' : branch).join(' and ');
  }

  async function runReviewFallback(question, language) {
    root.dataset.aiMode = REVIEW_MODE;

    if (matchesAny(question, urgentPatterns)) {
      return {
        mode: 'urgent',
        answer: language === 'ar'
          ? 'هذه الأعراض قد تحتاج تقييماً عاجلاً. إذا كان هناك صعوبة في التنفس أو البلع، نزيف لا يتوقف، تورم شديد أو سريع، أو إصابة خطيرة، اطلب الرعاية الطبية العاجلة أو الطوارئ فوراً ولا تعتمد على إجابة عبر الإنترنت.'
          : 'These symptoms may need urgent assessment. If there is difficulty breathing or swallowing, uncontrolled bleeding, severe or rapidly worsening swelling, or serious trauma, seek urgent/emergency medical care promptly rather than relying on an online answer.'
      };
    }

    if (matchesAny(question, medicationPatterns)) {
      return {
        mode: 'unsafe',
        answer: language === 'ar'
          ? 'أستطيع تقديم معلومات عامة عن الأسنان، لكن لا يمكنني وصف دواء أو مضاد حيوي، تحديد جرعة، أو إخبارك بإيقاف أو تغيير دواء موصوف لك. تواصل مع طبيبك أو فريق الاستقبال للحصول على إرشاد مناسب.'
          : 'I can provide general dental information, but I can’t prescribe medication or antibiotics, give a dose, or tell you to stop or change prescribed medication. Please contact your dentist/prescriber or reception for appropriate advice.'
      };
    }

    if (matchesAny(question, liveConfirmationPatterns)) {
      return {
        mode: 'fallback',
        answer: language === 'ar'
          ? 'الأسعار، تغطية التأمين، المواعيد المتاحة وجداول الأطباء تحتاج تأكيداً مباشراً من فريق الاستقبال. استخدم واتساب أو الاتصال أو البريد الإلكتروني أو طلب موعد أدناه.'
          : 'Prices, insurance coverage, live appointment availability and doctor schedules need direct confirmation from reception. Please use WhatsApp, Call, Email or Book Appointment below.'
      };
    }

    const { clinic, dental } = await loadReviewData();

    if (founderQuestion(question)) {
      const founder = clinic.history && clinic.history.founder;
      if (!founder) return { mode: 'fallback', answer: '' };
      return {
        mode: 'clinic',
        answer: language === 'ar'
          ? `مؤسس مركز سلوادي لطب الأسنان هو د. منير سلوادي. بدأ المركز خدمة المرضى في أبوظبي عام ${clinic.history.established || clinic.established || 1980}.`
          : `${founder} is the founder of Silwadi Dental Centre. The centre has served Abu Dhabi since ${clinic.history.established || clinic.established || 1980}.`
      };
    }

    if (establishedQuestion(question)) {
      const year = (clinic.history && clinic.history.established) || clinic.established;
      if (!year) return { mode: 'fallback', answer: '' };
      return {
        mode: 'clinic',
        answer: language === 'ar'
          ? `تأسس مركز سلوادي لطب الأسنان في أبوظبي عام ${year}.`
          : `Silwadi Dental Centre was established in Abu Dhabi in ${year}.`
      };
    }

    if (locationsQuestion(question)) {
      const branches = Object.values(clinic.branches || {});
      if (!branches.length) return { mode: 'fallback', answer: '' };
      const names = branches.map((branch) => branch.displayName).join(' and ');
      return {
        mode: 'clinic',
        answer: language === 'ar'
          ? `لدى سلوادي فرعان في أبوظبي: بني ياس تاور والراحة مول.`
          : `Silwadi has ${branches.length} Abu Dhabi locations: ${names}.`
      };
    }

    if (contactQuestion(question)) {
      const baniYas = clinic.branches && clinic.branches['bani-yas'];
      const alRaha = clinic.branches && clinic.branches['al-raha'];
      return {
        mode: 'clinic',
        answer: language === 'ar'
          ? `يمكنك التواصل مع سلوادي على ${clinic.contact.email}. هاتف بني ياس: ${baniYas.phone}، وهاتف الراحة مول: ${alRaha.phone}.`
          : `You can contact Silwadi at ${clinic.contact.email}. Bani Yas Tower: ${baniYas.phone}. Al Raha Mall: ${alRaha.phone}.`
      };
    }

    const branchKey = branchHoursQuestion(question);
    if (branchKey) {
      const branch = clinic.branches && clinic.branches[branchKey];
      if (!branch || !branch.hours) return { mode: 'fallback', answer: '' };
      return {
        mode: 'clinic',
        answer: language === 'ar'
          ? `ساعات فرع ${branchKey === 'al-raha' ? 'الراحة مول' : 'بني ياس تاور'} المعتمدة حالياً: ${localizeHours(branch.hours, 'ar')}.`
          : `${branch.displayName} opening hours are ${branch.hours}.`
      };
    }

    if (childDentistQuestion(question)) {
      const doctor = (clinic.doctors || []).find((item) => item.name === PEDIATRIC_DOCTOR && item.role === PEDIATRIC_ROLE);
      if (!doctor) return { mode: 'fallback', answer: '' };
      return {
        mode: 'clinic',
        answer: language === 'ar'
          ? 'تُدرج سلوادي د. كاشميرا باوار جايبراكاش كأخصائية أسنان أطفال في فرع الراحة مول. يمكن لفريق الاستقبال تأكيد الموعد المتاح.'
          : `${doctor.name} is listed by Silwadi as a ${doctor.role} at Al Raha Mall. Reception can confirm current appointment availability.`
      };
    }

    if (personalRootCanalQuestion(question)) {
      const education = guidanceFor(dental, 'root-canal', language);
      return {
        mode: 'general',
        answer: language === 'ar'
          ? `لا يمكن تحديد ما إذا كنت تحتاج علاج عصب من خلال الدردشة فقط؛ يحتاج ذلك إلى فحص لدى طبيب الأسنان وقد تحتاج أشعة. ${education}`
          : `Whether you need a root canal can only be decided after a dental examination and any necessary X-rays. ${education}`
      };
    }

    if (endodontistQuestion(question)) {
      const doctors = (clinic.doctors || []).filter((item) => /Endodontist/i.test(item.role || ''));
      if (!doctors.length) return { mode: 'fallback', answer: '' };
      const english = doctors.map((doctor) => `${doctor.name} (${doctorBranchLabel(doctor.branches)})`).join('; ');
      return {
        mode: 'clinic',
        answer: language === 'ar'
          ? 'أخصائيو علاج العصب المدرجون لدى سلوادي هم د. أحمد الشهري في بني ياس تاور ود. لانا مسعود في الراحة مول. المواعيد الحالية يؤكدها فريق الاستقبال.'
          : `Silwadi's listed Specialist Endodontists are ${english}. Reception can confirm current appointment availability.`
      };
    }

    if (rootCanalServiceQuestion(question)) {
      const offered = (clinic.services || []).includes('Endodontics');
      if (!offered) return { mode: 'fallback', answer: '' };
      const education = guidanceFor(dental, 'root-canal', language);
      return {
        mode: 'clinic',
        answer: language === 'ar'
          ? `نعم. تقدم سلوادي علاج جذور الأسنان (علاج العصب/Endodontics). ${education}`
          : `Yes. Silwadi offers Endodontics, including root canal treatment. ${education}`
      };
    }

    const topic = topicFromQuestion(question);
    if (topic) {
      const education = guidanceFor(dental, topic, language);
      if (education) return { mode: 'general', answer: education };
    }

    return { mode: 'fallback', answer: '' };
  }

  async function askQuestion(question) {
    const trimmed = String(question || '').trim();
    const language = languageFor(trimmed);
    setDirection(language);

    if (!trimmed) {
      clearResult();
      status.textContent = language === 'ar' ? 'اكتب سؤالك أولاً.' : 'Please type your question first.';
      input.focus();
      return;
    }

    if (trimmed.length > MAX_QUESTION_LENGTH) {
      clearResult();
      status.textContent = language === 'ar'
        ? 'يرجى اختصار سؤالك إلى 500 حرف أو أقل.'
        : 'Please keep your question to 500 characters or fewer.';
      return;
    }

    const endpoint = String(root.dataset.aiEndpoint || '').trim();
    if (!endpoint) {
      clearResult();
      setBusy(true, language);
      try {
        const result = await runReviewFallback(trimmed, language);
        if (!result.answer) {
          showFallback(language, 'unknown', true);
        } else {
          showAnswer(result.answer, language, result.mode, true);
        }
      } catch (error) {
        showFallback(language, 'endpoint', true);
      } finally {
        submit.disabled = false;
        input.disabled = false;
        status.dataset.busy = 'false';
      }
      return;
    }

    root.dataset.aiMode = 'secure-endpoint';
    if (activeController) activeController.abort();
    activeController = new AbortController();
    const controller = activeController;
    const timeout = window.setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

    clearResult();
    setBusy(true, language);

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: trimmed }),
        signal: controller.signal,
        credentials: 'omit',
        cache: 'no-store',
        referrerPolicy: 'strict-origin-when-cross-origin'
      });

      if (!response.ok) throw new Error(`Silwadi AI request failed: ${response.status}`);

      const payload = await response.json();
      const mode = ['clinic', 'general', 'fallback', 'urgent', 'unsafe'].includes(payload.mode)
        ? payload.mode
        : 'fallback';
      const responseLanguage = payload.language === 'ar' ? 'ar' : (payload.language === 'en' ? 'en' : language);
      const responseText = typeof payload.answer === 'string' ? payload.answer.trim() : '';

      if (!responseText) {
        showFallback(responseLanguage);
        return;
      }

      showAnswer(responseText, responseLanguage, mode);
    } catch (error) {
      if (controller.signal.aborted) {
        status.textContent = language === 'ar'
          ? 'استغرق الرد وقتاً أطول من المتوقع.'
          : 'The answer took longer than expected.';
      }
      showFallback(language);
    } finally {
      window.clearTimeout(timeout);
      if (activeController === controller) activeController = null;
      submit.disabled = false;
      input.disabled = false;
      status.dataset.busy = 'false';
    }
  }

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    askQuestion(input.value);
  });

  suggestions.forEach((button) => {
    button.addEventListener('click', () => {
      const question = button.dataset.aiSuggestion || button.textContent || '';
      input.value = question.slice(0, MAX_QUESTION_LENGTH);
      updateCount();
      askQuestion(input.value);
    });
  });

  input.addEventListener('input', updateCount);
  updateCount();
})();
