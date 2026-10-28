import test from 'node:test';
import assert from 'node:assert/strict';
import { accreditationAnswer } from '../ai/server/accreditations.mjs';

const source = 'https://silwadi.ae/about.html#accreditations-heading';

function reviewed(question, language = 'en') {
  const result = accreditationAnswer(question, language);
  assert.ok(result, `Expected an accreditation answer for: ${question}`);
  assert.equal(result.language, language);
  assert.equal(result.mode, 'reviewed');
  assert.equal(result.category, 'clarification');
  assert.equal(typeof result.answer, 'string');
  assert.ok(result.answer.includes(source), 'The answer must cite the published accreditation section');
  return result.answer;
}

test('the screenshot question returns the published scores and facility mapping', () => {
  const answer = reviewed('whats the accreditations');
  assert.match(answer, /Department of Health/);
  assert.match(answer, /JAWDA[^\n]*99\.55%[^\n]*GRADE A/);
  assert.match(answer, /ADHICS[^\n]*98%[^\n]*GRADE A/);
  assert.match(answer, /Dr\. Munir Silwadi Dental Centre[^\n]*MF368[^\n]*Corniche/);
  assert.match(answer, /Dr\. Mohamed Munir Dental Centre[^\n]*MF7451[^\n]*Al Raha Mall/);
  assert.match(answer, /ISO 9001:2015/);
  assert.doesNotMatch(answer, /don't have verified|reception can confirm/i);
});

test('certification wording reaches the same published overview', () => {
  const answer = reviewed('What certifications does Silwadi have?');
  assert.match(answer, /99\.55%/);
  assert.match(answer, /98%/);
  assert.match(answer, /ISO 9001:2015/);
});

test('JAWDA questions return only its authority, score and grade', () => {
  const answer = reviewed('What is your JAWDA score?');
  assert.match(answer, /Department of Health[^\n]*JAWDA[^\n]*99\.55%[^\n]*GRADE A/);
  assert.doesNotMatch(answer, /ADHICS|ISO|MF368|MF7451|2026/);
});

test('a branch-specific JAWDA question does not assign the score to that branch', () => {
  const answer = reviewed('What is Al Raha Mall JAWDA score?');
  assert.match(answer, /99\.55%/);
  assert.match(answer, /accreditation page does not specify a branch for this JAWDA score/i);
  assert.doesNotMatch(answer, /MF7451|MF368|ADHICS|ISO/);
});

test('ADHICS questions return its score for both named facilities', () => {
  const answer = reviewed('What is the ADHICS score?');
  assert.match(answer, /Department of Health[^\n]*ADHICS[^\n]*98%[^\n]*GRADE A/);
  assert.match(answer, /Dr\. Munir Silwadi Dental Centre[^\n]*MF368[^\n]*Corniche/);
  assert.match(answer, /Dr\. Mohamed Munir Dental Centre[^\n]*MF7451[^\n]*Al Raha Mall/);
  assert.doesNotMatch(answer, /JAWDA|99\.55|ISO/);
});

for (const query of ['What is Corniche ADHICS score?', 'ADHICS for MF368', 'ADHICS for Dr. Munir Silwadi Dental Centre']) {
  test(`${query} uses only the Corniche facility`, () => {
    const answer = reviewed(query);
    assert.match(answer, /98%[^\n]*GRADE A/);
    assert.match(answer, /MF368[^\n]*Corniche/);
    assert.doesNotMatch(answer, /MF7451|Al Raha|JAWDA|ISO/);
  });
}

for (const query of ['ADHICS score at Al Raha Mall?', 'ADHICS for MF7451', 'ADHICS for Dr. Mohamed Munir Dental Centre']) {
  test(`${query} uses only the Al Raha facility`, () => {
    const answer = reviewed(query);
    assert.match(answer, /98%[^\n]*GRADE A/);
    assert.match(answer, /MF7451[^\n]*Al Raha Mall/);
    assert.doesNotMatch(answer, /MF368|Corniche|JAWDA|ISO/);
  });
}

test('a branch accreditation overview includes only that facility and no branch JAWDA claim', () => {
  const answer = reviewed('What accreditations does Al Raha Mall have?');
  assert.match(answer, /Dr\. Mohamed Munir Dental Centre[^\n]*MF7451[^\n]*Al Raha Mall/);
  assert.match(answer, /ADHICS[^\n]*98%[^\n]*GRADE A/);
  assert.match(answer, /ISO 9001:2015/);
  assert.doesNotMatch(answer, /MF368|Corniche|JAWDA|99\.55%/);
});

for (const [question, language, facilityId, otherId] of [
  ['What certifications does Dr. Munir Silwadi Dental Centre have?', 'en', 'MF368', 'MF7451'],
  ['What accreditations does Dr. Mohamed Munir Dental Centre have?', 'en', 'MF7451', 'MF368'],
  ['ما شهادات مركز الدكتور محمد منير لطب الأسنان؟', 'ar', 'MF7451', 'MF368'],
]) {
  test(`a legal facility name keeps facility accreditation handling: ${question}`, () => {
    const answer = reviewed(question, language);
    assert.ok(answer.includes(facilityId));
    assert.ok(!answer.includes(otherId));
    assert.match(answer, /ADHICS[^\n]*98%/);
    assert.match(answer, /ISO 9001:2015/);
  });
}

test('ISO questions return the exact supported standard without unrelated scores', () => {
  const answer = reviewed('Are you ISO9001:2015 certified?');
  assert.match(answer, /ISO 9001:2015/);
  assert.match(answer, /MF368/);
  assert.match(answer, /MF7451/);
  assert.doesNotMatch(answer, /JAWDA|ADHICS|99\.55%|98%|GRADE A/);
});

test('a branch ISO question returns only that facility', () => {
  const answer = reviewed('ISO certificate for Corniche');
  assert.match(answer, /ISO 9001:2015/);
  assert.match(answer, /MF368[^\n]*Corniche/);
  assert.doesNotMatch(answer, /MF7451|Al Raha|JAWDA|ADHICS/);
});

test('Arabic accreditation wording returns a fully Arabic overview with readable scores', () => {
  const answer = reviewed('ما هي اعتمادات المركز؟', 'ar');
  assert.match(answer, /دائرة الصحة/);
  assert.match(answer, /JAWDA[^\n]*99\.55%[^\n]*الدرجة A/);
  assert.match(answer, /ADHICS[^\n]*98%[^\n]*الدرجة A/);
  assert.match(answer, /MF368[^\n]*الكورنيش/);
  assert.match(answer, /MF7451[^\n]*الراحة مول/);
  assert.match(answer, /ISO 9001:2015/);
  assert.doesNotMatch(answer, /Department of Health|Dr\.|Corniche|Al Raha/);
});

test('Arabic JAWDA wording handles diacritics and returns only the JAWDA fact', () => {
  const answer = reviewed('ما نتيجة جَوْدَة؟', 'ar');
  assert.match(answer, /دائرة الصحة[^\n]*JAWDA[^\n]*99\.55%[^\n]*الدرجة A/);
  assert.doesNotMatch(answer, /ADHICS|ISO|MF368|MF7451/);
});

test('Arabic ADHICS wording scopes the score to Al Raha Mall', () => {
  const answer = reviewed('كم نتيجة أدهيكس في الراحة مول؟', 'ar');
  assert.match(answer, /دائرة الصحة[^\n]*ADHICS[^\n]*98%[^\n]*الدرجة A/);
  assert.match(answer, /MF7451[^\n]*الراحة مول/);
  assert.doesNotMatch(answer, /MF368|الكورنيش|JAWDA|ISO/);
});

test('Arabic ISO spelling and numerals identify the supported standard', () => {
  const answer = reviewed('شهادة الآيزو ٩٠٠١:٢٠١٥ للكورنيش', 'ar');
  assert.match(answer, /ISO 9001:2015/);
  assert.match(answer, /MF368[^\n]*الكورنيش/);
  assert.doesNotMatch(answer, /MF7451|JAWDA|ADHICS/);
});

test('a question naming two supported standards includes only those standards', () => {
  const answer = reviewed('JAWDA and ADHICS scores?');
  assert.match(answer, /99\.55%/);
  assert.match(answer, /98%/);
  assert.doesNotMatch(answer, /ISO/);
});

for (const question of [
  'Are you JCI accredited?',
  'What is your Joint Commission International certification?',
  'JCI and ADHICS accreditation?',
  'Do you have ISO27001?',
  'ISO/IEC 27001 certification?',
  'ISO certification 27001?',
  'ISO 27001:2022 certification?',
  'Are you ISO9001:2020 certified?',
  'Are you ISO 9001 2020 certified?',
  'Is your ISO 9001-2020 certificate valid?',
  'شهادة ايزو ٢٧٠٠١',
  'هل لديكم شهادة الآيزو ٩٠٠١:٢٠٢٠؟',
]) {
  test(`an unsupported explicit certificate falls through: ${question}`, () => {
    assert.equal(accreditationAnswer(question, /[\u0600-\u06ff]/.test(question) ? 'ar' : 'en'), null);
  });
}

for (const question of [
  '',
  'Where are your clinics?',
  'Who is Dr. Munir?',
  'How much is a root canal?',
  'What is the quality of my filling?',
  'كيف أحجز موعداً؟',
]) {
  test(`an unrelated question keeps existing handling: ${question || '(empty)'}`, () => {
    assert.equal(accreditationAnswer(question, 'en'), null);
  });
}

for (const [question, language] of [
  ['Can I get a sick leave certificate after my visit?', 'en'],
  ['Can you issue a medical certificate?', 'en'],
  ['Is Dr. Moammar board certified?', 'en'],
  ['What certificates does Dr. Munir hold?', 'en'],
  ['What are your doctors’ certifications?', 'en'],
  ['هل يمكن إصدار شهادة إجازة مرضية بعد الزيارة؟', 'ar'],
  ['هل تعطون شهادة طبية؟', 'ar'],
  ['هل الدكتور معمر حاصل على البورد؟', 'ar'],
  ['هل الدكتور معمر حاصل على شهادة البورد؟', 'ar'],
  ['ما شهادات الدكتور منير؟', 'ar'],
]) {
  test(`patient paperwork or individual credentials keep existing handling: ${question}`, () => {
    assert.equal(accreditationAnswer(question, language), null);
  });
}
