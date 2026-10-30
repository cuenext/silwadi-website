/* Written five-star Google reviews verified on 30 October 2026.
 * Summaries faithfully paraphrase the available audited text; they are not verbatim quotes.
 * sourceAge records Google's relative age at audit time and must not be shown as a live date.
 */
(function () {
  "use strict";

  /**
   * @typedef {Object} ReviewRecord
   * @property {string} id Stable Google review ID, not a reviewer-name key.
   * @property {string} reviewer Reviewer spelling as shown by Google.
   * @property {"corniche"|"al-raha"} branch The listing on which the review was published.
   * @property {number} rating
   * @property {string} sourceAge Relative age captured at the audit.
   * @property {string} sourceUrl Google listing URL.
   * @property {{en: string, ar: string}} summary Concise bilingual paraphrases.
   */

  const CORNICHE_SOURCE_URL = "https://www.google.com/maps/place/?q=place_id:ChIJgb-kmGNmXj4R6fUFteS1G_U";
  const AL_RAHA_SOURCE_URL = "https://www.google.com/maps/place/Al+Raha+Branch+-+Dr.+Mohamed+Munir+Dental+Centre+-+LLC/@24.4388317,54.5744795,997m/data=!3m1!1e3!4m8!3m7!1s0x3e5e450061f92b85:0xb6d18f896de894bd!8m2!3d24.4388317!4d54.5744795!9m1!1b1";

  /** @type {ReadonlyArray<ReviewRecord>} */
  window.SILWADI_GOOGLE_REVIEWS = Object.freeze([
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2s4NGJWTnRhRkJqY2paaGMzcDNVRTF0YW14cVlXYxAB",
      "reviewer": "Antoni Yousef",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "8 months ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Welcoming reception, easy booking, and a clean, comfortable waiting area.",
        "ar": "استقبال ودود، وحجز سهل، ومنطقة انتظار نظيفة ومريحة."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT25WVE1YTkJTVk5wTFhOaVJXNW9SRzE2UVhkNlVFRRAB",
      "reviewer": "Fay Shaw",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "6 months ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Friendly, polite staff and professional dental care made the trip from Ajman worthwhile for implant treatment.",
        "ar": "طاقم ودود ومهذب ورعاية أسنان احترافية جعلت رحلة علاج الزراعة من عجمان تستحق العناء."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2xaSlRWRTJSSFV4YzBZM2NuVjFRM2cwU0hGUFgzYxAB",
      "reviewer": "Emily Campbell Scully",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "5 months ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Dr. Lujain made the check-up and cleaning reassuring, with friendly help from reception.",
        "ar": "جعلت د. لجين الفحص والتنظيف تجربة مطمئنة، مع مساعدة ودودة من الاستقبال."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUNPaWUtbzBnRRAB",
      "reviewer": "Waleed Humaid",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "4 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Professional doctors and nurses, careful precautions, and a Corniche setting.",
        "ar": "أطباء وممرضون محترفون، واهتمام بالإجراءات الوقائية، وموقع على الكورنيش."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2pGb1RGTllaMmxWVVdsRFprRmlNbXh5V21OVVEwRRAB",
      "reviewer": "Twana Karim",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Grateful to Dr. Hani Hasbini and the team for supportive orthodontic care and reassuring explanations.",
        "ar": "امتنان لد. هاني حسبيني والفريق على رعاية التقويم الداعمة والشرح المطمئن."
      }
    },
    {
      "id": "ChRDSUhNMG9nS0VJQ0FnSUNEajZVVxAB",
      "reviewer": "Joycefe Graciosa",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Thorough dental care and attention to detail made the journey from Dubai worthwhile.",
        "ar": "رعاية أسنان دقيقة واهتمام بالتفاصيل جعلا الرحلة من دبي تستحق العناء."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2pkYVVtOURkVXN4V2pWdmExTjBRbGxFWW5OWlZGRRAB",
      "reviewer": "Kari Felton",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "11 months ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Dr. Jamal Almarzooqi provided a professional, relaxing and painless cleaning experience.",
        "ar": "قدم د. جمال المرزوقي تنظيفاً احترافياً ومريحاً دون ألم."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VKYkMxZl9zMzdDM0pBEAE",
      "reviewer": "Omar Muflahi",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "A welcoming, friendly and professional reception team made the visit reassuring.",
        "ar": "جعل فريق الاستقبال الودود والمحترف الزيارة مريحة ومطمئنة."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2sxU1FVSkRSMmRFTm1oR1NHZE9Na1pIYVRZemJuYxAB",
      "reviewer": "Adela Askandar",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Dr. Krishna takes care to reduce discomfort from braces; the reviewer and their children are happy with treatment.",
        "ar": "يهتم د. كريشنا بتخفيف انزعاج التقويم، وصاحب التقييم وأطفاله راضون عن العلاج."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2s1NVlUSktTMko1UlVGaFkzcEtSWEZuZEVWdGVIYxAB",
      "reviewer": "el missouri Faiza",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Dr. Balajee reviews progress, answers questions, and tailors orthodontic care to the patient.",
        "ar": "يراجع د. بالاجي تقدم العلاج، ويجيب عن الأسئلة، ويخصص رعاية التقويم للمريض."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT20xS05WVmlXRFpTZVZSdVNqQndlV3R4Wm1sRWJtYxAB",
      "reviewer": "RachelT",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Dr. Munir arranged a prompt assessment after severe toothache and explained the CBCT scan findings.",
        "ar": "رتب د. منير تقييماً سريعاً بعد ألم شديد في الأسنان وشرح نتائج الأشعة المقطعية المخروطية."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2pWUmVEQmtiMGRmV2pGaVIyWm5jR1J5ZUY5bVNYYxAB",
      "reviewer": "Zainab Mansour",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "11 months ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "An excellent, comfortable and professional experience with self-ligating braces from Dr. Krishna.",
        "ar": "تجربة ممتازة ومريحة واحترافية مع التقويم ذاتي الربط لدى د. كريشنا."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT21nNFFXbEpRMFJYWkdGaVZ6UmhhVk13Y2xGdlZHYxAB",
      "reviewer": "Safeya Al Hameli",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "A patient of over ten years praises Dr. Munir's meticulous implant and crown work.",
        "ar": "مريض منذ أكثر من عشر سنوات يشيد بدقة عمل د. منير في الزراعة والتيجان."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VPeWlrSWJUckxiOUxnEAE",
      "reviewer": "Mohammed Mazrooei",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "High-quality dentistry, affordable prices, and professional, capable staff.",
        "ar": "علاج أسنان عالي الجودة وأسعار مناسبة وطاقم محترف وكفء."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUNUd1pPN1JBEAE",
      "reviewer": "joseph saoud",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Pleased with improvements in braces treatment under Dr. Krishna and the welcoming reception team.",
        "ar": "رضا عن التحسن في علاج التقويم لدى د. كريشنا وعن فريق الاستقبال الودود."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSURodHBDeXVnRRAB",
      "reviewer": "AREDEL JR_FAM",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "Edited 2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "A positive implant experience with Dr. Munir and his assistants, supported by accommodating staff.",
        "ar": "تجربة زراعة إيجابية مع د. منير ومساعديه، بدعم من طاقم متعاون."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUNPMmVfNEZnEAE",
      "reviewer": "Waleed Humaid",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "4 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Praises the spacious penthouse clinic and its long experience in Abu Dhabi.",
        "ar": "إشادة بالعيادة الواسعة في الطابق العلوي وخبرتها الطويلة في أبوظبي."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUNsaU11WExBEAE",
      "reviewer": "Ali Alomari",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Efficient appointments, responsive reception and follow-up, with a recommendation for Dr. Ahmed.",
        "ar": "مواعيد منظمة واستقبال متجاوب ومتابعة جيدة، مع توصية بد. أحمد."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJNms1THZyc1pPaFZ3EAE",
      "reviewer": "Ilm X",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Friendly staff, especially Mira, Alia, Len and rina at reception, during a visit with tooth pain and anxiety.",
        "ar": "طاقم ودود، خاصة ميرا وعليا ولين ورينا في الاستقبال، خلال زيارة رافقها ألم الأسنان والقلق."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUNwMTZUOWlBRRAB",
      "reviewer": "Hala Ahmadieh",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Happy with the daughter's braces results under Dr. Moammar and Dr. Rola's dental cleaning.",
        "ar": "رضا عن نتيجة تقويم الابنة لدى د. معمر وعن تنظيف الأسنان لدى د. رولا."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUNPbGVPb2NBEAE",
      "reviewer": "Panos Liatsis",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "4 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Excellent service, with thanks to Rina and Dr. Afnan for her kind, attentive dental care.",
        "ar": "خدمة ممتازة، مع الشكر لرينا ود. أفنان على رعايتها اللطيفة والمهتمة بالأسنان."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUNUM01mN1V3EAE",
      "reviewer": "Radhika C",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Consulted Dr. Krishna Balajee after Invisalign relapse following treatment at another clinic.",
        "ar": "استشارة د. كريشنا بالاجي بعد انتكاس علاج إنفزلاين الذي أُجري في عيادة أخرى."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUNoazh6dm5RRRAB",
      "reviewer": "Beth Marciniak",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "A nervous patient reports a quick, painless root canal with clear explanations from Dr. Ahmed.",
        "ar": "مريض قلق يصف علاج عصب سريعاً ودون ألم مع شرح واضح من د. أحمد."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUNsanZxNWlBRRAB",
      "reviewer": "Talal Al-Mukhalalati",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Over thirty years of excellent experiences with knowledgeable, friendly doctors and staff; recommends Dr. Muneer.",
        "ar": "أكثر من ثلاثين عاماً من التجارب الممتازة مع أطباء وطاقم ذوي معرفة وود، مع التوصية بد. منير."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUNQeXA2eDdRRRAB",
      "reviewer": "Hadil Saifi",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Professional care, punctual appointments and clear explanations, with thanks to Dr. Munir, Dr. Ahmad and Dr. Ibrahim.",
        "ar": "رعاية احترافية ومواعيد دقيقة وشرح واضح، مع الشكر لد. منير ود. أحمد ود. إبراهيم."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSURod19hU0JnEAE",
      "reviewer": "Rina de la Cruz",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Praises the dentists' expertise, compassion and care for patients.",
        "ar": "إشادة بخبرة أطباء الأسنان وتعاطفهم واهتمامهم بالمرضى."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSURPZ08tOXhRRRAB",
      "reviewer": "Deema Jayousi",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "4 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Consistently satisfying experiences with Dr. Silwdi's professional, skilled care.",
        "ar": "تجارب مرضية باستمرار مع رعاية د. سلوادي الاحترافية والمتقنة."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUN1NVlHRldREAE",
      "reviewer": "Salama Al Mazrouie",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "4 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "A patient of ten years recommends the clinic and Dr. Moheb for dental cleaning.",
        "ar": "مريض منذ عشر سنوات يوصي بالعيادة وبد. مهيب لتنظيف الأسنان."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSURKZ3Rfa3BRRRAB",
      "reviewer": "nicholas wyon",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "Edited 2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Pleased with the implant result; Dr. Fahed and the team guided the patient with minimal discomfort.",
        "ar": "رضا عن نتيجة الزراعة، مع إرشاد من د. فهد والفريق وانزعاج بسيط."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSURSaEp6R0hBEAE",
      "reviewer": "Shamsa",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Helpful reception and a friendly doctor who listened carefully and allowed time for concerns.",
        "ar": "استقبال متعاون وطبيبة ودودة استمعت باهتمام وخصصت وقتاً للمخاوف."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUQteW9uSnpRRRAB",
      "reviewer": "ghassan hassan",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Very satisfied with the treatment and experience provided by Dr. Munir Silwadi.",
        "ar": "رضا كبير عن العلاج والتجربة مع د. منير سلوادي."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUNseF9YNFJBEAE",
      "reviewer": "Alreem",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Dr. fahad made a feared wisdom-tooth removal easy, with no pain reported during or afterwards.",
        "ar": "جعل د. فهد خلع ضرس العقل الذي كان يثير الخوف سهلاً، دون ألم بحسب المريض أثناء الخلع أو بعده."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUMxdWNieUtBEAE",
      "reviewer": "alyaziaa",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Comfortable with the clinic since 1997 and pleased with Dr. Mohib's care.",
        "ar": "شعور بالراحة في العيادة منذ عام ١٩٩٧ ورضا عن رعاية د. مهيب."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUNPMjVIellREAE",
      "reviewer": "Caroline Saatdjian",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "4 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Good service from trustworthy doctors and welcoming, helpful staff.",
        "ar": "خدمة جيدة من أطباء جديرين بالثقة وطاقم ودود ومتعاون."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT25OQ09XZHlhblpFWkY5UVRXeFlUMXBaUVRSblRGRRAB",
      "reviewer": "Sahar Alsalman",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "6 months ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Professional work and friendly staff, especially Aliyah.",
        "ar": "عمل احترافي وطاقم ودود، وخاصة عليا."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSURWLS1HVThRRRAB",
      "reviewer": "Abu Abdullah",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Doctors clearly explained the problem and treatment options; pleasant staff helped the patient feel at ease.",
        "ar": "شرح الأطباء المشكلة وخيارات العلاج بوضوح، وساعد الطاقم اللطيف المريض على الشعور بالراحة."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUQ5MmN2ZmtRRRAB",
      "reviewer": "Bareaa Kadah",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Thanks Dr. Mineiro, the assistants, reception and administrative staff for the treatment.",
        "ar": "شكر لد. مينيرو والمساعدين وموظفي الاستقبال والإدارة على العلاج."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnTURBeDRlcjZ3RRAB",
      "reviewer": "Alastair Nicholson",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Friendly staff and dentist, with fast and efficient service at Al Raha Mall.",
        "ar": "طاقم وطبيب ودودون وخدمة سريعة وفعالة في الراحة مول."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSURCdXJfTXlBRRAB",
      "reviewer": "noora alkamali",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Professional service, especially from Dr. Moheb, and friendly help from Alya.",
        "ar": "خدمة احترافية، وخاصة من د. مهيب، ومساعدة ودودة من عليا."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSURacW9lYU9REAE",
      "reviewer": "MOHAMED Almansoori",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "A positive clinic experience with professional service from Alya and the team.",
        "ar": "تجربة إيجابية في العيادة وخدمة احترافية من عليا والفريق."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSURHaE9LazV3RRAB",
      "reviewer": "Houssam weiss",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "Edited 4 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Praises the doctors' professionalism and confidently recommends the clinic to friends.",
        "ar": "إشادة باحترافية الأطباء وتوصية بالعيادة للأصدقاء بثقة."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUNPdF8yYVNREAE",
      "reviewer": "Marie Ghastine",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "4 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Welcoming, helpful service from Rina at reception and a recommendation for Dr. Muneer.",
        "ar": "خدمة ودودة ومتعاونة من رينا في الاستقبال، مع توصية بد. منير."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSURoeHB2SnVRRRAB",
      "reviewer": "Yasser Sallam",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "A very good experience with a professional doctor, reception and cashier team.",
        "ar": "تجربة جيدة جداً مع طبيب وفريقي استقبال ومحاسبة محترفين."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSURCNXJfYTlBRRAB",
      "reviewer": "Issam Agha",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "A smooth visit from reception onward, with thanks to Dr. Ahmad for professional, caring treatment.",
        "ar": "زيارة سلسة بدءاً من الاستقبال، مع الشكر لد. أحمد على العلاج الاحترافي والمهتم."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSURCNHNQVm5nRRAB",
      "reviewer": "Fatheya R",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Appreciates the good service and professionalism of the clinic staff.",
        "ar": "تقدير للخدمة الجيدة واحترافية طاقم العيادة."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSURWZ1pIbEZ3EAE",
      "reviewer": "Muna Aldhuhoori",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "A smooth implant experience with Dr. Fahd.",
        "ar": "تجربة زراعة سلسة مع د. فهد."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUMxLXFMQ0ZBEAE",
      "reviewer": "Mubarak alketbi",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Considers it one of Abu Dhabi's best dental clinics.",
        "ar": "يعتبرها من أفضل عيادات الأسنان في أبوظبي."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VKYWM2Nl8yaHF2bTJ3RRAB",
      "reviewer": "Hidayah Al Zaabi",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "An excellent experience with Dr. Ahmed El Shehri.",
        "ar": "تجربة ممتازة مع د. أحمد الشهري."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnTURnMXNiNmdBRRAB",
      "reviewer": "Rasha Radi",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Praises Dr. Ehab's work during the visit.",
        "ar": "إشادة بعمل د. إيهاب خلال الزيارة."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUNsa2RpakNnEAE",
      "reviewer": "Mohamed Mabrouk",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Thanks the doctors, nurses and reception staff for excellent service.",
        "ar": "شكر للأطباء والممرضين وطاقم الاستقبال على الخدمة الممتازة."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2toTmVWZHFlV1J5TlhSdGFqbFZVVlJUZVdodUxYYxAB",
      "reviewer": "i ansari",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Very professional and kind.",
        "ar": "احترافية ولطف كبيران."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSURSMU03WEZREAE",
      "reviewer": "Dheyab BinHamoodah",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "A great dental clinic with a smooth experience.",
        "ar": "عيادة أسنان رائعة وتجربة سلسة."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUNPbzdEVVd3EAE",
      "reviewer": "Fahad SalZaabi",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "4 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Praises Dr. Muamer's work.",
        "ar": "إشادة بعمل د. معمر."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUQxeXZiNkxnEAE",
      "reviewer": "A. H",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Professional staff with extensive medical experience.",
        "ar": "طاقم محترف ذو خبرة طبية واسعة."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUNoeFB6U0V3EAE",
      "reviewer": "Khalifa Almheiri",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Excellent doctors and good service.",
        "ar": "أطباء ممتازون وخدمة جيدة."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSURMOXN6aE5nEAE",
      "reviewer": "Mariam Alhammadi",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Excellent doctors and nurses.",
        "ar": "أطباء وممرضون ممتازون."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUNaNUtDZUdREAE",
      "reviewer": "S. J. AL QUBAISI",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "Edited 2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Great communication and appointment scheduling.",
        "ar": "تواصل ممتاز وتنظيم جيد للمواعيد."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSURsZ05qNzN3RRAB",
      "reviewer": "Hessa Al Hashemi",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Excellent service and professional staff.",
        "ar": "خدمة ممتازة وطاقم محترف."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSURCbE9PcDN3RRAB",
      "reviewer": "Etienne Berchtold",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Very good, professional service.",
        "ar": "خدمة جيدة جداً واحترافية."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSURObU5DbTJnRRAB",
      "reviewer": "Hissa alkhaja",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "An excellent experience.",
        "ar": "تجربة ممتازة."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUNsaXU3dmNREAE",
      "reviewer": "Amr Mezian",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Considers the clinic the best.",
        "ar": "يعتبر العيادة الأفضل."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUNoa192aXN3RRAB",
      "reviewer": "Marwa Sammour",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Extremely neat work.",
        "ar": "عمل متقن للغاية."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUMxazRibm9RRRAB",
      "reviewer": "marchi 48",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Very professional staff.",
        "ar": "طاقم محترف جداً."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUR4dXJfaURREAE",
      "reviewer": "Ahmed Almehairi",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "An excellent dentist.",
        "ar": "طبيب أسنان ممتاز."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUMxOHJmZWtRRRAB",
      "reviewer": "Rana Al Mukhtar",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Praises the dentist as the best.",
        "ar": "إشادة بالطبيبة باعتبارها الأفضل."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUR4bXVEVXFnRRAB",
      "reviewer": "ayman yatim",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Great service.",
        "ar": "خدمة رائعة."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUNPbGFMdWtRRRAB",
      "reviewer": "Sadir P K",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "4 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Great doctors.",
        "ar": "أطباء رائعون."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUNPbGJMQmtRRRAB",
      "reviewer": "shafeeq koolikad",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "4 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Excellent doctors.",
        "ar": "أطباء ممتازون."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2s1eVNVUjFZak0xU20xWWJVZFdUSGRYUjFGR05GRRAB",
      "reviewer": "وليد ابوعبدو",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "7 hours ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "A painless extraction with Dr. Dana, with thanks to Amira, alia and the kind, professional team.",
        "ar": "خلع دون ألم لدى د. دانا، مع الشكر لأميرة وعليا والفريق اللطيف والمحترف."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2pCUFYzbGFkbFZ6YVRWaU9HOVNWV290WWpnNGFYYxAB",
      "reviewer": "Emirati Mother",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "a week ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Considers it the best dental clinic in Abu Dhabi.",
        "ar": "يعتبرها أفضل عيادة أسنان في أبوظبي."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2pOVVZsVlJhMkUwZW5NMFFsTlRZV3B6UkZkclJGRRAB",
      "reviewer": "Mz2006",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 weeks ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Dr. Dana's kind, attentive care made treatment comfortable and welcoming.",
        "ar": "جعلت رعاية د. دانا اللطيفة والمهتمة العلاج مريحاً وأشعرت المريض بالترحيب."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT25kM1ZFdDZZbTk2V1RVeU4wOVdibVF0ZDNSSGRFRRAB",
      "reviewer": "Ba Zim",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "a month ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Thanks Dr. Ahmed ELShehri for accepting an emergency case and providing root canal treatment.",
        "ar": "شكر لد. أحمد الشهري على استقبال حالة طارئة وتقديم علاج العصب."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2pNMk1tSjRUMjVCZEY5bmJGSlNTbVJZZURaSGRXYxAB",
      "reviewer": "Victoriya Davydova",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "5 months ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Very pleased with a professional cleaning by Dr. Lujain Masaab Abo Suleiman.",
        "ar": "رضا كبير عن تنظيف احترافي لدى د. لجين مصعب أبو سليمان."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUNwbWI3YnF3RRAB",
      "reviewer": "Anna Lona",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Praises Dr. Munir Al-Salwadi's work and respectful manner at the established Corniche clinic.",
        "ar": "إشادة بعمل د. منير السلوادي وتعامله المحترم في العيادة العريقة على الكورنيش."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2taNWJHWmlibGhqTWpoRFR6RmhUMVZPUTI1SlYxRRAB",
      "reviewer": "Sanaa Freihat",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "6 months ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Dr. Moheb Salwady's calm, patient manner made the dental experience comfortable.",
        "ar": "جعل أسلوب د. مهيب سلوادي الهادئ والصبور تجربة علاج الأسنان مريحة."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUNKNU9yUm53RRAB",
      "reviewer": "IZZA Bouziane BD",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Thanks Alia for her warm welcome and kindness, and describes trouble-free appointments.",
        "ar": "شكر لعليا على استقبالها الدافئ ولطفها، ووصف تجربة المواعيد بأنها خالية من المشكلات."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VLal92dEdvejhmNTZRRRAB",
      "reviewer": "Noura Alm",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Appreciates the clinic's continued efforts to excel.",
        "ar": "تقدير لجهود العيادة المستمرة للتميز."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT21STExVMVZjakpFVkRKd2VVVkVTazVCZFRKeGRWRRAB",
      "reviewer": "reem awny",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "10 months ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "An excellent implant experience with Dr. Fahd after initial hesitation and worry.",
        "ar": "تجربة زراعة ممتازة مع د. فهد بعد تردد وقلق في البداية."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2tzeFdFeERjbUV6V1RoRWN6aGhVVE5EZFhGd2FsRRAB",
      "reviewer": "Bakheeta zayed",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Praises Dr. Sarah's pediatric dental care and kind, respectful approach with children.",
        "ar": "إشادة برعاية د. سارة لأسنان الأطفال وتعاملها اللطيف والمحترم معهم."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUNsaDlEM09BEAE",
      "reviewer": "Ahmed Al khouri",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "A positive experience with root canal treatment, an implant and a filling, with thanks to Dr. Ahmed and the organized team.",
        "ar": "تجربة إيجابية مع علاج العصب والزراعة والحشو، مع الشكر لد. أحمد والفريق المنظم."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2tsMVNrMUtaVlY1VjNFd1VGUkpZMFJLTW5NMFNXYxAB",
      "reviewer": "Muna Alshuwaihi",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Aliya goes out of her way to arrange appointments and support patients through treatment.",
        "ar": "تبذل عليا جهداً لترتيب المواعيد ودعم المرضى طوال العلاج."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUNUcF82OHN3RRAB",
      "reviewer": "Husain ALJASMI",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "A well-equipped clinic with meticulous work and punctual appointments.",
        "ar": "عيادة مجهزة جيداً تتميز بدقة العمل والالتزام بالمواعيد."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VObWs0NURVeTZuTWxRRRAB",
      "reviewer": "Z R",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Praises Dr. Loujain's organized, gentle care and reports no pain during treatment.",
        "ar": "إشادة برعاية د. لجين المنظمة واللطيفة، مع عدم الشعور بالألم أثناء العلاج."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUNUOTdHNmhnRRAB",
      "reviewer": "Samira Ahmed",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Thanks Alia for her help, Dr. Moheb for his dedication, and Dr. Ahmed and Dr. Mounir.",
        "ar": "شكر لعليا على مساعدتها، ولد. مهيب على إخلاصه، ولد. أحمد ود. منير."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSURWc2NHOGtBRRAB",
      "reviewer": "Amal Shaker",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Skilled dentists and staff who treat patients politely and respectfully.",
        "ar": "أطباء أسنان ماهرون وطاقم يعامل المرضى بأدب واحترام."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSURkLVlqb2tRRRAB",
      "reviewer": "Latifa alobeidli",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "A patient of fourteen years praises the organized clinic and Dr. Afnan's precise, neat work.",
        "ar": "مريض منذ أربعة عشر عاماً يشيد بتنظيم العيادة ودقة عمل د. أفنان وإتقانه."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUNKMjhENW1RRRAB",
      "reviewer": "Moath Alsabty",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "Edited 3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "An excellent experience with Dr. Ahmed and Dr. Reem.",
        "ar": "تجربة ممتازة مع د. أحمد ود. ريم."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSURCMnZYRC1BRRAB",
      "reviewer": "Soheir El shall",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Praises Dr. Munir's experience and professionalism, and respectful service from Munjid and Alia.",
        "ar": "إشادة بخبرة د. منير واحترافيته، وبالتعامل المحترم من منجد وعليا."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUNod2Z2NnBRRRAB",
      "reviewer": "Mahra 11",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Thanks Dr. Munir for the mother's dental treatment and Dr. Reem for satisfying internal-whitening results.",
        "ar": "شكر لد. منير على علاج أسنان الأم ولد. ريم على نتائج التبييض الداخلي المرضية."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSURCcHVxZkFREAE",
      "reviewer": "abdullah nourallah",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Praises Dr. Muammar's experience and precision, Alia's helpful reception, and the cooperative team.",
        "ar": "إشادة بخبرة د. معمر ودقته، واستقبال عليا المتعاون، وتعاون الفريق."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUNRbWFuUDFBRRAB",
      "reviewer": "AHMAD ALSHAMSI",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "8 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "An excellent clinic for doctors, appointments and treatment.",
        "ar": "عيادة ممتازة من حيث الأطباء والمواعيد والعلاج."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2xwclZGOVlTME0yZGtSTlFuaG5NazlMYkV0MVgwRRAB",
      "reviewer": "Haila 22",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Thanks Dr. Afnan and Dr. Sarah for their expertise and excellent patient care.",
        "ar": "شكر لد. أفنان ود. سارة على خبرتهما ورعايتهما الممتازة للمرضى."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSURKZ01LLXRBRRAB",
      "reviewer": "Anissa Nagati",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Praises Dr. Munir's respectful, meticulous care and reports a painless experience.",
        "ar": "إشادة برعاية د. منير المحترمة والدقيقة، ووصف التجربة بأنها دون ألم."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUNBN0pPU253RRAB",
      "reviewer": "J.A.A Alhameli",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "9 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Praises the clinic and Dr. Munir's humility and attention to detail.",
        "ar": "إشادة بالعيادة وتواضع د. منير واهتمامه بالتفاصيل."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUMwbE5lTmhBRRAB",
      "reviewer": "علياء اليافعي",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "7 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Praises the team's humility and ethics, and Dr. Fahad's implant care.",
        "ar": "إشادة بتواضع الفريق وأخلاقه، وبرعاية د. فهد في زراعة الأسنان."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSURCNFBXOUhBEAE",
      "reviewer": "muneera alkharousi",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "A wonderful experience with professional reception, great nurses and excellent doctors.",
        "ar": "تجربة رائعة مع استقبال محترف وممرضين رائعين وأطباء ممتازين."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUNPMWE3T1BnEAE",
      "reviewer": "Marwan Abu hashish",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "4 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Over ten years of treatment with dedicated, skilled doctors.",
        "ar": "أكثر من عشر سنوات من العلاج مع أطباء مخلصين وماهرين."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSURoZzhQcHpnRRAB",
      "reviewer": "as00m as00m",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Praises the clinic and its excellent doctors.",
        "ar": "إشادة بالعيادة وأطبائها الممتازين."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUR4bXZ5dnVBRRAB",
      "reviewer": "Ali SM Almehairbi",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Excellent service and a warm reception during root canal treatment and front-tooth cleaning.",
        "ar": "خدمة ممتازة واستقبال رائع خلال علاج العصب وتنظيف سن أمامي."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUNCdjhiZm1BRRAB",
      "reviewer": "Ferial Karmy",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Praises the dental treatment and Dr. Amani's excellent care.",
        "ar": "إشادة بعلاج الأسنان ورعاية د. أماني الممتازة."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUNsdnRDdENnEAE",
      "reviewer": "S 7",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Professional doctors and staff who keep appointments on time.",
        "ar": "أطباء وطاقم محترفون يلتزمون بالمواعيد."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUNkN3JqR29nRRAB",
      "reviewer": "hamada Edris",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Thanks the skilled Dr. Reem and Mahmoud at reception.",
        "ar": "شكر لد. ريم الماهرة ولمحمود في الاستقبال."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnTURvLTctVzJBRRAB",
      "reviewer": "Moza Al Qubaisi",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Praises Dr. Sarah's work and excellent manner.",
        "ar": "إشادة بعمل د. سارة وتعامُلها الممتاز."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSURPMFBPMEd3EAE",
      "reviewer": "Huwaidi Hadi",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "4 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Praises the clinic and the skill and kindness of the staff, especially Dr. Muammar Al-Rifai.",
        "ar": "إشادة بالعيادة ومهارة الطاقم ولطفه، وخاصة د. معمر الرفاعي."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSURoeUxPWEJBEAE",
      "reviewer": "Aroob Ghaizan",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Thanks the team for excellent service and Dr. Afnan for meticulous work.",
        "ar": "شكر للفريق على الخدمة الممتازة ولد. أفنان على العمل الدقيق."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSURCdUstbkRBEAE",
      "reviewer": "Abdalla Alsuwaidi",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "Edited 2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Respectful service, attention to patient satisfaction, and precise work.",
        "ar": "تعامل محترم واهتمام برضا المريض وعمل دقيق."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSURodHRQNGVREAE",
      "reviewer": "المانيا المانيا",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Thanks everyone at the clinic, from Dr. Munir to reception.",
        "ar": "شكر للجميع في العيادة، من د. منير إلى موظفي الاستقبال."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUQxcFo3dTR3RRAB",
      "reviewer": "Fatima Juma",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Considers it one of the country's best dental treatment centres.",
        "ar": "يعتبره من أفضل مراكز علاج الأسنان في الدولة."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSURteDR1TTB3RRAB",
      "reviewer": "zubaida ahmed",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "4 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "A favourite dental centre in Abu Dhabi with professional doctors.",
        "ar": "مركز أسنان مفضل في أبوظبي بأطباء محترفين."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUNsM3Q2QTNnRRAB",
      "reviewer": "Mema A",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Thanks reception, nurses and doctors for excellent service and courtesy.",
        "ar": "شكر للاستقبال والممرضين والأطباء على الخدمة الممتازة وحسن التعامل."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUNPMWJyMmh3RRAB",
      "reviewer": "Marwani To",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "4 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "A wonderful, highly efficient team.",
        "ar": "فريق رائع وكفء جداً."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUQxX2ZmQmdRRRAB",
      "reviewer": "Mona Alobeidli_1",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "An excellent experience with Dr. Ahmed Farouk.",
        "ar": "تجربة ممتازة مع د. أحمد فاروق."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSURCeXBldi1BRRAB",
      "reviewer": "k m",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Praises Dr. Hasabini and the helpful reception staff.",
        "ar": "إشادة بد. حسبيني وموظفي الاستقبال المتعاونين."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUNsc3QyZVN3EAE",
      "reviewer": "نبنين نبينين",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "One of the best dental facilities the reviewer has visited.",
        "ar": "من أفضل مرافق علاج الأسنان التي زارها صاحب التقييم."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSURKc09tV1lnEAE",
      "reviewer": "سلطان الساعدي",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Considers it one of the best dental clinics and thanks the team.",
        "ar": "يعتبرها من أفضل عيادات الأسنان ويشكر الفريق."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUNocTgzWWlBRRAB",
      "reviewer": "om-salem Sem",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Special thanks to Dr. Muammar.",
        "ar": "شكر خاص لد. معمر."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUQ4bDlTd1hREAE",
      "reviewer": "مبارك المنصوري",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "6 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "One of the best clinics the reviewer has visited.",
        "ar": "من أفضل العيادات التي زارها صاحب التقييم."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUR4NnJfS1B3EAE",
      "reviewer": "Keokje Sweets",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Considers the dentist the best in Abu Dhabi.",
        "ar": "يعتبر طبيب الأسنان الأفضل في أبوظبي."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUNseDYtTHNnRRAB",
      "reviewer": "Abdulla Alabdouli",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Highly experienced doctors.",
        "ar": "أطباء ذوو خبرة واسعة."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUNseWFLUjZRRRAB",
      "reviewer": "H H",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Excellent.",
        "ar": "ممتاز."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUQ4Zzl5TFF3EAE",
      "reviewer": "anna lona",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "6 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Considers the dentist the best in Abu Dhabi.",
        "ar": "يعتبر طبيب الأسنان الأفضل في أبوظبي."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUR2ZzdUakF3EAE",
      "reviewer": "Sssa Almaz",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Excellent in every way.",
        "ar": "ممتاز من جميع النواحي."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUNvdzl5RnFBRRAB",
      "reviewer": "Moza Jassim",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "7 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Considers it one of Abu Dhabi's best clinics.",
        "ar": "يعتبرها من أفضل العيادات في أبوظبي."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUNBOUl2Q2VnEAE",
      "reviewer": "Khalfan Almehairbi",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "8 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Examination only.",
        "ar": "فحص فقط."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJQ0FnSUNsMDR5cjZBRRAB",
      "reviewer": "Mubarak640",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "2 years ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "Excellent service.",
        "ar": "خدمة ممتازة."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2s1Zk4wMDRNbGxSZGpockxXNUJia1l4Y2t0UFNXYxAB",
      "reviewer": "Sheikha Mubarak Rashed Almansouri",
      "branch": "corniche",
      "rating": 5,
      "sourceAge": "3 weeks ago",
      "sourceUrl": CORNICHE_SOURCE_URL,
      "summary": {
        "en": "An excellent experience with Dr. Mitra, praised for her kindness, understanding and clear treatment-plan explanations.",
        "ar": "تجربة ممتازة مع د. ميترا، مع الإشادة بلطفها وتفهمها وشرحها الواضح لخطة العلاج."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2xwSllUTXpUblU1YkVkRWVEZFZTM05pYkMwMWFXYxAB",
      "reviewer": "Michael Todd Currence",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "5 months ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Thanks MZoon, Shaina and Len for a warm welcome, and Dr. Nachiket for a quick, painless extraction.",
        "ar": "شكر لمزون وشاينا ولين على الترحيب الدافئ، ولد. ناتشيكيت على خلع سريع ودون ألم."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT21aWlZIbElSelZEYWpaM1dsQXhVVEpuVDIxdFYwRRAB",
      "reviewer": "جودي الجندي",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "4 months ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Friendly staff and Dr. Lujain's attention to comfort made this an excellent dental experience.",
        "ar": "جعل الطاقم الودود واهتمام د. لجين بالراحة تجربة الأسنان ممتازة."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2tVMGVISnFVMmcxZW1acWJWOWtTalp0VjA5bWMyYxAB",
      "reviewer": "Soha Shami",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "5 months ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Precise dental cleaning in a clean clinic, with little waiting and reasonable prices.",
        "ar": "تنظيف أسنان دقيق في عيادة نظيفة، مع انتظار قصير وأسعار مناسبة."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT25SYVlYa3hXSFZLY1RGS1VXbEtaVEpsTVdJME5HYxAB",
      "reviewer": "Aatikah Adam",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "5 months ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Dr. Krishna explained and supported every step of the son's braces treatment; the staff were consistently friendly.",
        "ar": "شرح د. كريشنا كل خطوة في تقويم الابن وقدم الدعم خلالها، وكان الطاقم ودوداً باستمرار."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2xKb2RETXhXVmgxVWpOdE0wWnpkMDl1U2xwTVFrRRAB",
      "reviewer": "Nada Elsokkary",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "6 months ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Dr. Ehab reassures a nervous patient by explaining treatment and checking comfort throughout.",
        "ar": "يطمئن د. إيهاب المريض القلق بشرح العلاج والاطمئنان إلى راحته طوال الوقت."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT21saFpreEpRVnA0VDJwbllXTktPRGRqTkVsMlJXYxAB",
      "reviewer": "Naila Rashed",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "2 months ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Comfortable treatment with Dr. Sara in a welcoming clinic with a friendly reception team.",
        "ar": "علاج مريح مع د. سارة في عيادة مرحبة وفريق استقبال ودود."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2pGbU9HTnNOaTFsWjFoU2FrcHRTamhGTldVNFMxRRAB",
      "reviewer": "Edwina G",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "3 months ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Thanks Dr. Hassouneh for his work and Len, Mzoon and Shaima for excellent customer service.",
        "ar": "شكر لد. حسونة على عمله، وللين ومزون وشيماء على خدمة العملاء الممتازة."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2xwdlpXZExObXd6TVROVVlXRXlTMHRHWW5oWVIzYxAB",
      "reviewer": "Louai Mohammad",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "6 months ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Satisfied with Dr. Krishna's Invisalign treatment plan and the professional, well-equipped clinic.",
        "ar": "رضا عن خطة علاج إنفزلاين لدى د. كريشنا وعن العيادة المجهزة جيداً وطاقمها المحترف."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT20xcU0weG5UREYzVDNsRFdUbE1SWGhsUTB0Qk5WRRAB",
      "reviewer": "Ronique Britz",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Dr. Ehab arranged a same-day Corniche referral to Dr. Munir for extraction; the caring team handled everything efficiently.",
        "ar": "رتب د. إيهاب إحالة في اليوم نفسه إلى د. منير في الكورنيش للخلع، وتعامل الفريق المهتم مع كل شيء بكفاءة."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT25ka1RWUk9PSFZmVFROcFRIbGhTRm80Y1ROM1JHYxAB",
      "reviewer": "Dr.Noushidha",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Dr. Kashmira gently reassured an anxious child, with supportive help from Ruby in a clean, child-friendly clinic.",
        "ar": "طمأنت د. كشميرا طفلاً قلقاً بلطف، بدعم من روبي في عيادة نظيفة ومناسبة للأطفال."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT25CWGRUTlVjMmRET1RKNFZHVnZjVE5SY0RoSWQxRRAB",
      "reviewer": "Iman Iman",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "4 months ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Dr. Lujain's gentle, kind and understanding care made the whole experience comfortable.",
        "ar": "جعلت رعاية د. لجين اللطيفة والمتفهمة التجربة مريحة طوال الوقت."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT21OWmJYcGFaV2RHWkhacVR6VlNUbDl5YTJWaVptYxAB",
      "reviewer": "Razan Awad",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Dr. Lujain provided gentle, thorough cleaning with attention to detail and patient comfort.",
        "ar": "قدمت د. لجين تنظيفاً لطيفاً ودقيقاً مع الاهتمام بالتفاصيل وراحة المريض."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2sxbFZsUjZkMjUzTTJOTldYVjJhMkZ1VlRrME5VRRAB",
      "reviewer": "Hamdan Alkatheeri",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "5 months ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Professional dental care and outstanding service from a welcoming, cooperative reception team.",
        "ar": "رعاية أسنان احترافية وخدمة مميزة من فريق استقبال مرحب ومتعاون."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT201ak1XWkdNa3BYZEhONFlXMDBlVkZQVTB0RlEwRRAB",
      "reviewer": "alaa al-habtari",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Dr. Ehab Bassam A. Hassouneh and the team provided attentive care and a comfortable, painless experience.",
        "ar": "قدم د. إيهاب بسام حسونة والفريق رعاية مهتمة وتجربة مريحة ودون ألم."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnTURBNV9Db1hBEAE",
      "reviewer": "Shades Beauty salon",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "Edited a year ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Dr. Kashmira explained the daughter's root canal and crown treatment patiently in a welcoming, child-friendly setting.",
        "ar": "شرحت د. كشميرا علاج عصب الابنة وتاج السن بصبر في أجواء مرحبة ومناسبة للأطفال."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2tscU5qQnZUMmgyV0hkT2REaDNaRVJqTTNwaU5sRRAB",
      "reviewer": "Kristy D",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "11 months ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Dr. Sara was kind and professional when repairing the edges of two front teeth with fillings.",
        "ar": "كانت د. سارة لطيفة ومحترفة عند ترميم حواف سنين أماميين بالحشوات."
      }
    },
    {
      "id": "ChdDSUhNMG9nS0VJM2g1WnVsOG9pZ3VRRRAB",
      "reviewer": "Yazeed Abed",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Two years of positive experiences with Dr. Krishna, including cleaning, fillings and Invisalign.",
        "ar": "عامان من التجارب الإيجابية مع د. كريشنا، شملت التنظيف والحشوات وإنفزلاين."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnTUNBbk5PV1lBEAE",
      "reviewer": "Jackie Wilson",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Dr. Ehab helped a nervous patient with sensitive teeth relax and experience treatment without pain.",
        "ar": "ساعد د. إيهاب مريضاً قلقاً ذا أسنان حساسة على الاسترخاء وتلقي العلاج دون ألم."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2tnelJXcElOVTVQYW1wMlpDMDFNa0ZMVGtSc1oyYxAB",
      "reviewer": "Jakob Serlier",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Pleased with Dr. Ehab's kind, professional care during cleaning and filling appointments.",
        "ar": "رضا عن رعاية د. إيهاب اللطيفة والاحترافية خلال مواعيد التنظيف والحشو."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2s0eVgyMVJaR3RQWHpCSUxXWjJkVkp0WjFGUFltYxAB",
      "reviewer": "E M",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "A calm clinic and attentive staff, with special thanks to Dr. Lujain Masaab.",
        "ar": "عيادة هادئة وطاقم مهتم، مع شكر خاص لد. لجين مصعب."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2xSYWFTMUlXa0ozWlVwTldUQlFNRE5UYW1KbmMxRRAB",
      "reviewer": "Ayesha Q",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Thanks Dr. Moheb for detailed explanations, precise work and professionalism.",
        "ar": "شكر لد. مهيب على الشرح المفصل والعمل الدقيق والاحترافية."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VQN0t1clBQZ2J5dlN3EAE",
      "reviewer": "Mahra Alm",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Dr. Krishna helped explain the problem and possible solutions, with high-quality service.",
        "ar": "ساعد د. كريشنا في شرح المشكلة والحلول الممكنة، مع خدمة عالية الجودة."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT25oemFrZE1aa05xWWpaR1RWUTFSRGx1ZUU5V1pHYxAB",
      "reviewer": "Mohsin Ali",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Praises the doctors and friendly staff.",
        "ar": "إشادة بالأطباء والطاقم الودود."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VNZkJ2TFBiaVlMa1NBEAE",
      "reviewer": "Nelly _dr",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "A very pleasant experience with Dr. Chuaeib's skilled, precise work.",
        "ar": "تجربة مريحة جداً مع عمل د. شعيب الماهر والدقيق."
      }
    },
    {
      "id": "ChZDSUhNMG9nS0VJQ0FnSUN2aWMtM0ZREAE",
      "reviewer": "Bilal Nabaa",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "A really pleasant experience.",
        "ar": "تجربة لطيفة جداً."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2kxd1pUTTVNM1J3UVZwb1VtUkljRkZzWjBGdmVFRRAB",
      "reviewer": "safia ahmed",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "a month ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Welcoming help from mzoon, len and shaima, gentle nurses, and clear, unhurried explanations from Dr. Kashmira.",
        "ar": "مساعدة مرحبة من مزون ولين وشيماء، وممرضون لطفاء، وشرح واضح دون استعجال من د. كشميرا."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT21STVRtNVhaazFWTkdKSldpMXBZbU5rTjFNdGFsRRAB",
      "reviewer": "Axel",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "2 months ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "A very friendly team; the doctor took time to explain options and answer every question.",
        "ar": "فريق ودود جداً؛ خصص الطبيب وقتاً لشرح الخيارات والإجابة عن جميع الأسئلة."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2pGVFFtaG1VVTh6YmpsV05tWnpkekEwYm1OYU1GRRAB",
      "reviewer": "Sanaa Freihat",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "6 months ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Dr. Moheb Salwady explained every step of a computer-aided filling and cleaning, with satisfying results.",
        "ar": "شرح د. مهيب سلوادي كل خطوة في حشوة بمساعدة الحاسوب وتنظيف الأسنان، مع نتائج مرضية."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2s1VVpUSjZOMVF6YzNsSFlsVjRPRE5pU2psWFkyYxAB",
      "reviewer": "Sana Samhouri",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "11 months ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Easy booking and a smooth, comfortable visit with clear explanations and painless treatment from Dr. Jamal.",
        "ar": "حجز سهل وزيارة سلسة ومريحة، مع شرح واضح وعلاج دون ألم لدى د. جمال."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT2pFM1lqaEdPVEV5ZERWRGFWSTRUMWxGWkU5TFgyYxAB",
      "reviewer": "Mohamed Almazrouei",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Thanks Dr. Muhib Al-Salwadi for precise, professional dental treatment and cleaning.",
        "ar": "شكر لد. مهيب السلوادي على علاج الأسنان وتنظيفها بدقة واحترافية."
      }
    },
    {
      "id": "Ci9DQUlRQUNvZENodHljRjlvT21GUlJYSktNMWhNY21ocGNUWmhUemhZT0hwM1duYxAB",
      "reviewer": "Nooraldeen Kasem",
      "branch": "al-raha",
      "rating": 5,
      "sourceAge": "a year ago",
      "sourceUrl": AL_RAHA_SOURCE_URL,
      "summary": {
        "en": "Praises Dr. Shoaib Sawali's gentle touch and excellent root canal filling work.",
        "ar": "إشادة بلمسة د. شعيب صوالي الخفيفة وعمله الممتاز في حشو العصب."
      }
    }
  ].map(function (review) {
    Object.freeze(review.summary);
    return Object.freeze(review);
  }));
})();
