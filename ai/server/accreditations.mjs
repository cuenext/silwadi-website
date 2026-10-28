const SOURCE = 'https://silwadi.ae/about.html#accreditations-heading';

const FACILITIES = [
  {
    id: 'MF368',
    en: 'Dr. Munir Silwadi Dental Centre (MF368 · Corniche)',
    ar: 'مركز الدكتور منير سلوادي لطب الأسنان (MF368 · الكورنيش)',
    matches: /\bmf368\b|\bcorniche\b|\bbani\s*yas\b|\bmunir\s+silwadi\s+dental\s+cent(?:re|er)s?\b|كورنيش|بني ياس|منير سلوادي/,
  },
  {
    id: 'MF7451',
    en: 'Dr. Mohamed Munir Dental Centre (MF7451 · Al Raha Mall)',
    ar: 'مركز الدكتور محمد منير لطب الأسنان (MF7451 · الراحة مول)',
    matches: /\bmf7451\b|\braha\b|\bmohamed\s+munir\s+dental\s+cent(?:re|er)s?\b|الراح[ةه]|محمد منير/,
  },
];

function normalize(question) {
  return String(question || '').normalize('NFKC').toLowerCase()
    .replace(/[\u0610-\u061a\u064b-\u065f\u0670\u06d6-\u06ed]/g, '')
    .replace(/[أإآٱ]/g, 'ا')
    .replace(/[٠-٩]/g, digit => String(digit.charCodeAt(0) - 0x660))
    .replace(/[۰-۹]/g, digit => String(digit.charCodeAt(0) - 0x6f0));
}

export function accreditationAnswer(question, language) {
  const q = normalize(question);
  const jawda = /\bjawda\b|(?:نتيج[ةه]|درج[ةه]|معيار)\s+(?:ال)?جود[ةه]|^(?:ال)?جود[ةه][؟?!.\s]*$/.test(q);
  const adhics = /\badhics\b|ادهي?كس|ادهكس/.test(q);
  const iso = /\biso(?=\b|\d)|ايزو/.test(q);
  const overview = /\baccredit(?:ation|ations|ed)\b|\bcertif(?:ication|ications|icate|icates|ied)\b|اعتماد|اعتمادات|شهاد[ةه]|شهادات/.test(q);
  if (!jawda && !adhics && !iso && !overview) return null;

  // Patient documents and individual qualifications use the existing assistant routes.
  if (/\bsick[\s-]*leave\b|\bmedical[\s-]+certificat|اجاز[ةه].{0,15}مرضي|شهاد[ةه].{0,15}(?:مرضي|طبي)/.test(q)) return null;
  if (/\bboard[\s-]*certif|البورد/.test(q)) return null;
  const legalFacility = /\b(?:munir\s+silwadi|mohamed\s+munir)\s+dental\s+cent(?:re|er)s?\b|مركز.{0,20}(?:منير سلوادي|محمد منير).{0,20}طب الاسنان/.test(q);
  if (!jawda && !adhics && !iso && !legalFacility
    && /\b(?:dr|doctors?|dentists?|specialists?)\b|دكتور|اطباء|طبيب|اخصائي/.test(q)) return null;

  // Only the published ISO standard is approved; other named standards fall through.
  if (/\bjci\b|\bjcaho\b|joint commission|اللجن[ةه] الدولي[ةه] المشترك[ةه]/.test(q)) return null;
  if (iso) {
    if (/\biso\s*\/\s*iec\b/.test(q)) return null;
    for (const match of q.matchAll(/(?:\biso|ايزو)(?:\s+(?:certification|certificate|standard))?\s*[-:]?\s*(\d+)(?:(?:\s*[:/\-]\s*|\s+)(\d{4}))?/g)) {
      if (match[1] !== '9001' || (match[2] && match[2] !== '2015')) return null;
    }
  }

  const ar = language === 'ar';
  const scoped = FACILITIES.filter(facility => facility.matches.test(q));
  const facilities = scoped.length ? scoped : FACILITIES;
  const names = facilities.map(facility => facility[ar ? 'ar' : 'en']);
  const specific = jawda || adhics || iso;
  const parts = [];

  if (jawda || (!specific && !scoped.length)) {
    parts.push(ar
      ? 'دائرة الصحة — نتيجة جودة JAWDA: 99.55% — الدرجة A.'
      : 'Department of Health — JAWDA Quality Score: 99.55% — GRADE A.');
    if (scoped.length) parts.push(ar
      ? 'صفحة الاعتمادات لا تحدد فرعاً لهذه النتيجة من جودة JAWDA.'
      : 'The accreditation page does not specify a branch for this JAWDA score.');
  }

  if (adhics || !specific) {
    parts.push(ar
      ? 'دائرة الصحة — نتيجة ADHICS: 98% — الدرجة A، للمنشآت التالية:'
      : 'Department of Health — ADHICS Score: 98% — GRADE A, for:');
    parts.push(...names);
  }

  if (iso || !specific) {
    if (adhics || !specific) {
      parts.push(ar
        ? 'شهادة ISO 9001:2015 منشورة أيضاً لهذه المنشآت.'
        : 'ISO 9001:2015 certification is also listed for these facilities.');
    } else {
      parts.push(ar
        ? 'شهادة ISO 9001:2015 منشورة للمنشآت التالية:'
        : 'ISO 9001:2015 certification is listed for:');
      parts.push(...names);
    }
  }

  parts.push(`[${ar ? 'عرض الاعتمادات' : 'View accreditations'}](${SOURCE})`);
  return { language, mode: 'reviewed', category: 'clarification', answer: parts.join('\n\n') };
}
