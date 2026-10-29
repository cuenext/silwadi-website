/* Appointment drafts stay in page memory until explicit consent and submission to the clinic. */
globalThis.SilwadiBooking = (() => {
 const canon=q=>globalThis.SilwadiClinicText?.canonical(q)||String(q);
 const treatments=[['General Dentistry','طب الأسنان العام'],['Preventive Dentistry','طب الأسنان الوقائي'],['Cosmetic Dentistry','تجميل الأسنان'],['Dental Implants','زراعة الأسنان'],['Orthodontics','تقويم الأسنان'],['Periodontics','علاج اللثة'],['Endodontics','علاج العصب'],['Paediatric Dentistry','طب أسنان الأطفال'],['People of Determination Dental Care','رعاية أسنان أصحاب الهمم'],['Other / Not sure','غير ذلك / مب متأكد']];
 const clinics=[['Bani Yas Tower','برج بني ياس'],['Al Raha Mall','الراحة مول']];
 const times=Array.from({length:12},(_,i)=>String(i+9).padStart(2,'0')+':00');
 const doctors=[['Munir Silwadi','منير سلوادي'],['Moheb Silwadi','مهيب سلوادي'],['Ahmed El Shehri','أحمد الشهري'],['Hani Hasbini','هاني حسبيني'],['Dana Awad','دانا عوض'],['Afnan Mashal','أفنان مشعل'],['Lana Almasoud','لانا المسعود'],['Fahed Abi Khalil','فهد أبي خليل'],['Kashmira Pawar Jayprakash','كاشميرا باوار جايبراكاش'],['Krishnamurthy Balajee','كريشنامورثي بالاجي'],['Ehab Hassouneh','إيهاب حسونة'],['Sara Ismail','سارة إسماعيل'],['Nachiket Shah','ناشيكيت شاه'],['Nasr Keshkiea','نصر كشكية'],['Moammar Mohamed Rifai','معمر محمد الرفاعي']];
 function requestedDoctor(q){return String(q).normalize('NFKC').replace(/[\p{M}\p{Cf}]/gu,'').replace(/[أإآ]/g,'ا').trim().match(/\s+(?:with|مع|عند)\s+(?:(?:dr\.?|doctor|الدكتورة|الدكتور|دكتورة|دكتور)\s*)?([a-z\u0621-\u064a]+(?:[ -]+[a-z\u0621-\u064a]+){0,3})[؟?.!\s]*$/i);}
 function preferredDoctor(q){const m=requestedDoctor(canon(q));if(!m)return '';const parts=m[1].toLowerCase().split(/[ -]+/);const candidates=doctors.filter(d=>{const tokens=(d[0]+' '+d[1]).toLowerCase().replace(/[أإآ]/g,'ا').split(/[ -]+/);return parts.every(p=>tokens.includes(p));});return candidates.length===1?candidates[0][0]:'';}
 function intent(q){
  let s=canon(q).normalize('NFKC').replace(/[\p{M}\p{Cf}]/gu,'').replace(/[أإآ]/g,'ا').trim();
  if(/cancel|reschedul|pain|hurt|sw[ae]ll|bleed|breath|swallow|urgent|emergency|الغاء|الغي|تغيير|(?:^|\s)(?:الم|الالم)(?:\s|$)|يعور|وارم|ورم|نزيف|تنفس|ابلع|طوارئ/i.test(s))return false;
  const preferred=requestedDoctor(s);if(preferred)s=s.slice(0,preferred.index).trim();
  if(preferred&&preferredDoctor(q)&&/^(?:(?:i (?:wanna|want to|would like to)|please|can i)\s+)?book$/.test(s))return true;
  if(preferred&&preferredDoctor(q)&&/^(?:(?:ابغي|ابغى|ابي|ابا|اريد|ممكن)\s+)?(?:احجز|حجز)[؟?.!\s]*$/.test(s))return true;
  if(/^(?:can|could|may) i (?:have|get|request) (?:an? )?(?:appointment|visit)[?.!\s]*$/i.test(s))return true;
  return /^(?:(?:hi|hello|hey)[!,\s]*)?(?:(?:i (?:wanna|want to|would like to)|i'd like to|can i|can you help me|how (?:can|do) i|please)\s+)?(?:book|schedule|request)(?:\s+(?:me|an?|my|a dental|a dentist))?\s+(?:appointment|visit)(?:\s+(?:please|at silwadi|with you))?[?.!\s]*$/i.test(s)||/^i (?:want|need|would like) (?:an? )?appointment(?: please)?[?.!\s]*$/i.test(s)||/^(?:appointments?|booking)[?.!\s]*$/i.test(s)||/^(?:(?:هلا|مرحبا)[،\s]*)?(?:(?:ابغي|ابغى|ابي|ابا|اريد|ممكن|كيف اقدر)\s+)?(?:(?:احجز|اطلب|حجز)\s+)?موعد(?:\s+(?:عندكم|لو سمحت|في سلوادي))?[؟?.!\s]*$/.test(s);
 }
 function valid(step,d){
  if(step===0)return typeof d.name==='string'&&d.name.trim().length>=2&&d.name.length<=100;
  if(step===1)return /^[+\d ()-]{7,25}$/.test(d.mobile||'')&&(d.mobile.match(/\d/g)||[]).length>=7&&/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(d.email||'')&&d.email.length<=120;
  if(step===2)return treatments.some(x=>x[0]===d.treatment)&&clinics.some(x=>x[0]===d.clinic)&&(!d.doctor||doctors.some(x=>x[0]===d.doctor));
  if(step===3){if(!times.includes(d.time))return false;if(!d.date)return true;const parsed=new Date(d.date+'T12:00:00Z');return /^\d{4}-\d{2}-\d{2}$/.test(d.date)&&!Number.isNaN(parsed.valueOf())&&parsed.toISOString().slice(0,10)===d.date&&d.date>=new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Dubai',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());}
  return step===4&&d.consent===true&&typeof d.notes==='string'&&d.notes.length<=300;
 }
 function clarification(q){
  const s=String(q).normalize('NFKC').replace(/[\p{M}\p{Cf}]/gu,'').replace(/[أإآ]/g,'ا').trim();
  return /^(?:(?:i (?:wanna|want to|need to|would like to)|i'd like to|can i|please)\s+)?(?:book|bok|boook|booking)(?:\s+(?:please|an? appointment|an? apointment))?[?.!\s]*$/i.test(s)||/^(?:(?:ابغي|ابغى|ابي|ابا|اريد|ممكن)\s+)?(?:احجز|حجز)[؟?.!\s]*$/.test(s)?'booking':null;
 }
 function emergencyFailure(q){const s=String(q).normalize('NFKC').replace(/[\p{M}\p{Cf}]/gu,'').replace(/[أإآ]/g,'ا');return /breath|swallow|chok|throat.*clos|bleed|تنفس|اتنفس|اختنق|ابلع|بلع|نزيف|دم.*(?:يوقف|وقف)|نفسي.*(?:ضايق|ضيق|مب|مو)|حلق.*(?:مسكر|سكر|قفل)/i.test(s);}
 async function submit(d,language,sendRequest=fetch){
  if(![0,1,2,3,4].every(step=>valid(step,d)))throw new Error('invalid_booking');
  const payload={name:d.name.trim(),email:d.email.trim(),phone:d.mobile.trim(),treatment:d.treatment,clinic:d.clinic,date:d.date||'',time:d.time,notes:['Source: Silwadi AI website',d.doctor?'Preferred doctor: Dr. '+d.doctor:'',d.notes].filter(Boolean).join('\n'),language:language==='ar'?'ar':'en',website:'',consent:true};
  const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),20000);
  try{const response=await sendRequest('https://booking.silwadi.ae/booking-submit.php',{method:'POST',headers:{'Content-Type':'application/json'},credentials:'omit',referrerPolicy:'no-referrer',body:JSON.stringify(payload),signal:controller.signal});const result=await response.json();if(!response.ok||result.ok!==true){const error=new Error('booking_rejected');error.rejected=true;throw error;}return {ok:true};}finally{clearTimeout(timer);}
 }
 return {intent,preferredDoctor,doctors,clarification,emergencyFailure,valid,treatments,clinics,times,submit};
})();
