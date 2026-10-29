(() => {
"use strict";
if (window.__SILWADI_ASSISTANT__) return;
window.__SILWADI_ASSISTANT__ = true;
const config = window.SILWADI_AI_CONFIG || {};
const script = document.currentScript;
const presentation=script?.dataset.presentation==="page"?"page":"widget";
const page=presentation==="page";
const base = new URL(script && script.src ? script.src : "/ai/preview/silwadi-ai-widget.js", location.href);
const icon = config.icon || new URL("assistant.svg", base).href;
const api = "https://booking.silwadi.ae/assistant-ask.php";
const dictionary = {
  en: {
    title:"Silwadi Assistant",sub:"Dental & clinic information",launcher:"Ask Silwadi",
    greeting:"How can we help?",intro:"Find a dentist, explore dental services, or plan your visit.",
    help:"General information, not diagnosis. OpenAI may process questions outside the UAE. Avoid personal details.",
    prompt:"Ask a general question…",book:"Request an appointment",more:"Read full question",less:"Show less",
    restart:"New conversation",close:"Close chat",privacy:"Privacy & safety",
    codeHelp:"This is an AI assistant for general dental and clinic information. General questions and recent conversation context may be processed by OpenAI outside the UAE. Processing is not UAE-only. store:false does not exclude all provider retention; standard safety monitoring may retain content for up to 30 days, subject to exceptions. See the full AI privacy notice below. It cannot diagnose, prescribe or confirm bookings. Do not share personal details or medical records. For personal concerns, contact reception or a dentist.",
    error:"I couldn't get an answer. If you have difficulty breathing or swallowing, or severe bleeding that will not stop, seek emergency medical help immediately. For swelling or rapidly worsening pain, seek urgent professional assessment. For other concerns, contact reception: Corniche +971 2 626 2042; Al Raha +971 2 666 2408.",copy:"Copy answer",copied:"Copied",
    common:"Popular questions",typing:"Preparing an answer",
    topics:[
      ["Find a dentist","Which Silwadi doctor provides root canal treatment?"],
      ["Clinic locations","Where are Silwadi's clinics in Abu Dhabi?"],
      ["Daily care tips","How can I keep my teeth clean?"],
      ["Appointments","How can I request an appointment?"]
    ]
  },
  ar: {
    title:"مساعد سلوادي",sub:"معلومات الأسنان والعيادة",launcher:"اسأل سلوادي",
    greeting:"كيف نقدر نساعدك؟",intro:"تعرف على أطبائنا وخدمات الأسنان وفروعنا في أبوظبي.",
    help:"معلومات عامة، مو تشخيص. OpenAI ممكن يعالج الأسئلة خارج الإمارات. لا تشارك بيانات شخصية.",
    prompt:"اكتب سؤالاً عاماً…",book:"طلب موعد",more:"عرض السؤال كاملاً",less:"عرض أقل",
    restart:"محادثة جديدة",close:"إغلاق المحادثة",privacy:"الخصوصية والسلامة",
    codeHelp:"هذا مساعد ذكي للمعلومات العامة عن الأسنان والعيادة. OpenAI ممكن يعالج الأسئلة العامة وسياق المحادثة الأخير خارج الإمارات. المعالجة مب محصورة في الإمارات. ممكن يحتفظ مزود الخدمة بالمحتوى لمراقبة السلامة لمدة تصل إلى 30 يوم، مع استثناءات. راجع إشعار الخصوصية الكامل أدناه. ما يقدر يشخّص أو يوصف دواء أو يثبت حجز. لا تشارك بيانات شخصية أو ملفات طبية. لأي موضوع شخصي، تواصل مع الاستقبال أو طبيب الأسنان.",
    error:"تعذّر الحصول على إجابة. إذا عندك صعوبة في التنفس أو البلع، أو نزيف شديد ما يوقف، اطلب المساعدة الطبية الطارئة فوراً. للانتفاخ أو الألم اللي يزيد بسرعة، اطلب تقييماً عاجلاً من مختص. لباقي الاستفسارات، تواصل مع الاستقبال: الكورنيش +971 2 626 2042؛ الراحة +971 2 666 2408.",copy:"نسخ الإجابة",copied:"تم النسخ",
    common:"أسئلة شائعة",typing:"جاري إعداد الرد",
    topics:[
      ["اختيار الطبيب","أي أخصائي في سلوادي يعالج عصب الأسنان؟"],
      ["فروع العيادة","وين فروع سلوادي في أبوظبي؟"],
      ["نصايح يومية","شو نصايحكم عشان احافظ على اسناني بشكل عام؟"],
      ["حجز موعد","كيف أقدر أطلب موعد عندكم؟"]
    ]
  }
};
const mount=document.createElement("div");
mount.id="silwadi-assistant-mount";
mount.dataset.presentation=presentation;
(page?document.getElementById("ai-app")||document.body:document.body).appendChild(mount);
const shadow=mount.attachShadow({mode:"open"});
const sheet=document.createElement("link");
sheet.rel="stylesheet";
sheet.href=new URL("silwadi-ai-widget.css?v=20261015-lang1",base).href;
shadow.appendChild(sheet);
if(page){const pageSheet=document.createElement("link");pageSheet.rel="stylesheet";pageSheet.href=new URL("../silwadi-ai-page.css?v=20261015-lang1",base).href;shadow.appendChild(pageSheet);dictionary.en.greeting="How can we help?";dictionary.ar.greeting="كيف نقدر نساعدك؟";dictionary.en.intro="Questions about a treatment, finding the right doctor, or visiting one of our clinics? Start here.";dictionary.ar.intro="عندك سؤال عن خدمات الأسنان، الأطباء أو زيارة أحد فروعنا؟ ابدأ هني.";dictionary.en.topics.push(["People of Determination","is there POD"]);dictionary.ar.topics.push(["أصحاب الهمم","عندكم POD؟"]);}
const markup=[
'<div class="sw-root">',
'<div class="sw-scrim" data-scrim></div>',
'<section class="sw-panel" id="sw-panel" role="dialog" aria-modal="false" aria-label="Silwadi Assistant" aria-hidden="true">',
'<header class="sw-head"><span class="sw-identity"><span class="sw-mark"><img data-mark alt=""></span><span class="sw-brand-copy"><strong data-title>Silwadi Assistant</strong><small data-sub>Dental & clinic information</small></span></span>',
'<span class="sw-tools"><button type="button" class="sw-small-button sw-language" data-language aria-label="Switch language">عربي</button>',
'<button type="button" class="sw-icon-button" data-new title="New conversation" aria-label="New conversation"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M12 5v14M5 12h14"/></svg></button>',
'<button type="button" class="sw-icon-button" data-close title="Close chat" aria-label="Close chat"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M5 5l14 14M19 5 5 19"/></svg></button></span></header>',
'<div class="sw-conversation" data-conversation><div class="sw-welcome" data-welcome>',
'<div class="sw-welcome-icon"><img data-mark alt=""></div><span class="sw-page-kicker" data-kicker hidden></span><'+(page?'h1':'h2')+' data-greeting>How can we help?</'+(page?'h1':'h2')+'><p data-intro>Find a dentist, explore dental services, or plan your visit.</p>',
'<div class="sw-quick-label" data-common>Popular questions</div><div class="sw-suggestions" data-suggestions></div></div>',
'<div class="sw-messages" data-messages role="log" aria-live="polite" aria-relevant="additions text"></div></div>',
'<div class="sw-footer"><form class="sw-composer" data-form>',
'<label for="sw-question" class="sw-sr-only">Ask Silwadi</label><textarea id="sw-question" data-question rows="1" maxlength="650" placeholder="Ask a general question…" autocomplete="off"></textarea>',
'<button class="sw-send" type="submit" data-send disabled aria-label="Send"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg></button></form>',
'<div class="sw-safety"><span class="sw-safety-sign" aria-hidden="true">i</span><span data-help></span></div>',
'<div class="sw-links"><a data-book href="https://silwadi.ae/contact.html#consultation-form" target="_blank" rel="noopener noreferrer"></a><button type="button" data-privacy>Privacy & testing</button></div>',
'<div class="sw-config" data-config hidden><p data-code-help></p><a href="/ai/privacy.html" target="_blank" rel="noopener noreferrer">AI privacy notice / خصوصية المساعد</a></div>',
'</div></section>',
'<div class="sw-launch-group"><span class="sw-tooltip" data-tooltip>Ask Silwadi</span><button class="sw-launcher" data-launch type="button" aria-haspopup="dialog" aria-controls="sw-panel" aria-expanded="false" aria-label="Open Silwadi Assistant"><img data-mark alt=""><span class="sw-launch-cross"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"><path d="M5 5l14 14M19 5 5 19"/></svg></span></button></div>',
'<div class="sw-sr-only" data-announcement role="status" aria-live="polite"></div></div>'
].join("");
const tpl=document.createElement("template");tpl.innerHTML=markup;shadow.appendChild(tpl.content.cloneNode(true));
const one=s=>shadow.querySelector(s);
const all=s=>Array.from(shadow.querySelectorAll(s));
all("[data-mark]").forEach(el=>{el.src=icon;});
const root=one(".sw-root"),panel=one(".sw-panel"),conversation=one("[data-conversation]");
const messages=one("[data-messages]"),welcome=one("[data-welcome]"),input=one("[data-question]");
const launch=one("[data-launch]"),send=one("[data-send]");
if(page){root.classList.add("sw-page");one(".sw-footer").prepend(one(".sw-tools"));panel.setAttribute("role","region");panel.removeAttribute("aria-modal");one("[data-kicker]").hidden=false;document.getElementById("clinic-faq-content")?.setAttribute("hidden","");const back=document.createElement("a");back.href="/";back.className="sw-page-nav";back.textContent="Clinic website ↗";one(".sw-tools").prepend(back);}
if(page){const browse=document.createElement("button");browse.type="button";browse.className="sw-page-nav sw-faq-browse";browse.dataset.faqBrowse="";browse.setAttribute("aria-expanded","false");browse.setAttribute("aria-controls","sw-faq-sidebar");browse.addEventListener("click",()=>{const open=!root.classList.contains("sw-faq-open");root.classList.toggle("sw-faq-open",open);browse.setAttribute("aria-expanded",String(open));if(open)one("[data-faq] summary")?.focus();});root.addEventListener("keydown",e=>{if(e.key==="Escape"){root.classList.remove("sw-faq-open");browse.setAttribute("aria-expanded","false");browse.focus();}});one(".sw-tools").prepend(browse);}
const prefersReduced=window.matchMedia("(prefers-reduced-motion: reduce)");
let language="en",opened=false,busy=false,abort=null,version=0,context=[];
let booking=null,bookingCard=null;
let clarification=null;
const bookingPolicy=window.SilwadiBooking;
function addChoices(row,ids,lang,token,bookingDoctor=""){
 const labels={booking:['Yes, book an appointment','هيه، حجز موعد'],other:['No, something else','لا، شي ثاني'],locations:['Clinic locations','فروع العيادة'],services:['Dental services','خدمات الأسنان']};
 const questions={locations:['Where are your clinics?','وين فروع سلوادي؟'],services:['What dental services do you offer?','شو خدمات الأسنان عندكم؟']};
 const box=document.createElement("div");box.className="sw-booking-actions";
 for(const id of ids){if(!labels[id])continue;const b=document.createElement("button");b.type="button";b.className="sw-choice";b.textContent=labels[id][lang==="ar"?1:0];
  b.addEventListener("click",()=>{if(token!==version||busy||booking)return;box.remove();clarification=null;if(id==="booking"){startBooking(lang,bookingPolicy.doctors.some(d=>d[0]===bookingDoctor)?bookingDoctor:"");return;}if(id==="other"){message("assistant",lang==="ar"?"تمام، شو تقصد؟":"Okay—what did you mean?",lang);input.focus();return;}ask(questions[id][lang==="ar"?1:0]);});box.appendChild(b);
 }row.querySelector(".sw-message-body").appendChild(box);scrollEnd();
}
function startBooking(lang=language,preferredDoctor=""){
 if(busy||booking)return;
 version++;clarification=null;
 context=[];languageUI(lang);booking={step:0,values:{doctor:preferredDoctor},lang};
 const doctorName=bookingPolicy.doctors?.find(d=>d[0]===preferredDoctor);
 const row=message("assistant",doctorName?(lang==="ar"?`أكيد! نقدر نجهز طلب موعد مع د. ${doctorName[1]}. الاستقبال يؤكد توفر الطبيب والموعد.`:`Sure! Let’s prepare an appointment request with Dr. ${doctorName[0]}. Reception will confirm the doctor’s availability and appointment.`):(lang==="ar"?"أكيد! خلنا نجهز طلب الموعد بخمس خطوات قصيرة.":"Sure! Let’s prepare your appointment request in five short steps."),lang);
 bookingCard=document.createElement("div");bookingCard.className="sw-booking";
 row.querySelector(".sw-message-body").appendChild(bookingCard);drawBooking();
}
function drawBooking(){
 const {step,values:d,lang}=booking,ar=lang==="ar";
 bookingCard.replaceChildren();bookingCard.dir=ar?"rtl":"ltr";
 const text=(tag,value)=>{const e=document.createElement(tag);e.textContent=value;bookingCard.appendChild(e);return e;};
 text("strong",ar?`الخطوة ${Math.min(step+1,5)} من 5`:`Step ${Math.min(step+1,5)} of 5`);
 text("p",ar?"بياناتك تنرسل لفريق المواعيد بعد موافقتك وعند الإرسال فقط، وما تنرسل للذكاء الاصطناعي.":"Your details are sent to the appointments team only when you submit. Booking details are not sent to the AI.");
 const f=document.createElement("form");f.className="sw-booking-form";bookingCard.appendChild(f);
 const fields=[];
 function field(key,en,arabic,type="text",options=null,required=true){
  const label=document.createElement("label");label.textContent=ar?arabic:en;
  const e=document.createElement(options?"select":type==="textarea"?"textarea":"input");
  e.name=key;e.setAttribute("aria-label",label.textContent);if(!options&&type!=="textarea")e.type=type;
  if(options){const blank=document.createElement("option");blank.value="";blank.textContent=ar?"اختر":"Please choose";e.appendChild(blank);for(const choice of options){const o=document.createElement("option");o.value=choice[0];o.textContent=ar?choice[1]:choice[0];e.appendChild(o);}}
  e.required=required;e.autocomplete="off";if(type==="checkbox")e.checked=!!d[key];else e.value=d[key]||"";
  if(!options&&type!=="checkbox")e.maxLength=key==="notes"?300:key==="name"?100:120;
  if(type==="date")e.min=new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Dubai',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
  const remember=()=>{d[key]=type==="checkbox"?e.checked:e.value.trim();};e.addEventListener("input",remember);e.addEventListener("change",remember);
  label.appendChild(e);f.appendChild(label);fields.push(e);
 }
 if(step===0)field("name","What’s your full name?","شو اسمك الكامل؟");
 if(step===1){field("mobile","Mobile number","رقم الموبايل","tel");field("email","Email address","البريد الإلكتروني","email");}
 if(step===2){field("treatment","Treatment / reason for visit","الخدمة / سبب الزيارة","text",bookingPolicy.treatments);field("clinic","Preferred clinic","الفرع المفضل","text",bookingPolicy.clinics);field("doctor","Preferred doctor (optional)","الطبيب المفضل (اختياري)","text",bookingPolicy.doctors,false);}
 if(step===3){field("date","Preferred date (optional)","التاريخ المفضل (اختياري)","date",null,false);field("time","Preferred time","الوقت المفضل","text",bookingPolicy.times.map(x=>[x,x]));text("p",ar?"الوقت تفضيل فقط؛ الاستقبال يؤكد التوفر وساعات الفرع.":"This is a preference; reception must confirm availability and branch hours.");}
 if(step===4){
  const dl=document.createElement("dl");f.appendChild(dl);
  for(const [key,en,arabic] of [["name","Name","الاسم"],["mobile","Mobile","الموبايل"],["email","Email","البريد"],["treatment","Treatment","الخدمة"],["clinic","Clinic","الفرع"],["doctor","Preferred doctor","الطبيب المفضل"],["date","Date","التاريخ"],["time","Time","الوقت"]]){
   const dt=document.createElement("dt"),dd=document.createElement("dd");dt.textContent=ar?arabic:en;
   const choice=[...bookingPolicy.treatments,...bookingPolicy.clinics,...bookingPolicy.doctors].find(x=>x[0]===d[key]);dd.textContent=ar&&choice?choice[1]:d[key]||(ar?"بدون تفضيل":"No preference");dl.append(dt,dd);
  }
  field("notes","Notes (optional; no medical details)","ملاحظات (اختياري، بدون تفاصيل طبية)","textarea",null,false);
  field("consent","I agree that Silwadi may use these details to reply to my appointment enquiry.","أوافق أن سلوادي تستخدم هالبيانات للرد على طلب الموعد.","checkbox");
 }
 const error=document.createElement("p");error.setAttribute("role","alert");error.className="sw-booking-error";f.appendChild(error);
 const actions=document.createElement("div");actions.className="sw-booking-actions";f.appendChild(actions);
 function capture(){for(const e of fields)d[e.name]=e.type==="checkbox"?e.checked:e.value.trim();}
 function button(label,action){const b=document.createElement("button");b.type="button";b.textContent=label;b.addEventListener("click",action);actions.appendChild(b);}
 if(step>0)button(ar?"رجوع":"Back",()=>{capture();booking.step--;drawBooking();});
 button(ar?"إلغاء":"Cancel",()=>{booking=null;bookingCard.remove();bookingCard=null;languageUI(language);resize();input.focus();});
 const next=document.createElement("button");next.type="submit";next.textContent=step===4?(ar?"إرسال طلب الموعد":"Send appointment request"):(ar?"التالي":"Continue");actions.appendChild(next);
 if(step===4&&booking.uncertain){next.disabled=true;error.textContent=ar?"نتيجة الإرسال السابق مب مؤكدة. تواصل مع الاستقبال قبل إرسال طلب ثاني.":"The previous submission outcome is unknown. Contact reception before sending another request.";}
 f.addEventListener("submit",async event=>{event.preventDefault();if(booking?.sending||(step===4&&booking?.uncertain))return;capture();if(!bookingPolicy.valid(step,d)){error.textContent=ar?"راجع البيانات المطلوبة وأدخلها بشكل صحيح.":"Please check the required details and enter valid values.";return;}
  if(step<4){booking.step++;drawBooking();return;}
  booking.sending=true;const controls=[...f.querySelectorAll('input,select,textarea,button'),one('[data-language]'),one('[data-new]')].filter(Boolean);controls.forEach(e=>e.disabled=true);next.textContent=ar?"جارٍ إرسال الطلب…":"Sending request…";error.textContent='';
  try{await bookingPolicy.submit(d,lang);}catch(failure){booking.sending=false;booking.uncertain=!failure.rejected;controls.forEach(e=>e.disabled=false);next.textContent=ar?"إرسال طلب الموعد":"Send appointment request";if(booking.uncertain)next.disabled=true;error.textContent=failure.rejected?(ar?"ما قدرنا نرسل الطلب. بياناتك بعدها موجودة؛ جرّب لاحقاً أو اتصل بالاستقبال.":"The request was not accepted. Your details are still here; try later or contact reception."):(ar?"ما قدرنا نتأكد إذا الطلب وصل. عشان ما يتكرر، تواصل مع الاستقبال قبل ما ترسل مرة ثانية.":"We couldn’t confirm whether the request arrived. To avoid duplicates, contact reception before submitting again.");return;}
  controls.forEach(e=>e.disabled=false);booking=null;bookingCard.replaceChildren();bookingCard.setAttribute('role','status');bookingCard.textContent=ar?"تم إرسال طلب الموعد لفريق المواعيد. الموعد مب مؤكد للحين؛ الاستقبال بيتواصل معك لتأكيد التوفر والطبيب والوقت.":"Your appointment request was sent to the appointments team. Your appointment is not confirmed yet; reception will contact you to confirm availability, doctor and time.";
  bookingCard=null;languageUI(language);resize();input.focus();scrollEnd();
 });
 input.readOnly=true;input.placeholder=ar?"أكمل الخطوة فوق":"Complete the step above";send.disabled=true;
 one("[data-help]").textContent=ar?"بيانات الحجز تنرسل لفريق المواعيد فقط بعد موافقتك، وما تنرسل للذكاء الاصطناعي.":"Booking details go to the appointments team only when you submit, never to the AI.";
 fields[0]?.focus({preventScroll:true});scrollEnd();
}
const t=k=>dictionary[language][k]||k;
const isArabic=q=>/[\u0600-\u06ff]/.test(String(q||""));
function renderFaq(){
 if(!page||!window.SilwadiFaq)return;
 let box=one("[data-faq]");if(!box){box=document.createElement("section");box.dataset.faq="";box.className="sw-faq";box.id="sw-faq-sidebar";box.setAttribute("aria-label","Frequently asked questions");panel.appendChild(box);}box.replaceChildren();
 const title=document.createElement("h2");title.textContent=language==="ar"?"الأسئلة الشائعة":"Frequently asked questions";box.appendChild(title);box.dir=language==="ar"?"rtl":"ltr";box.setAttribute("aria-label",title.textContent);const close=document.createElement("button");close.type="button";close.className="sw-faq-close";close.textContent="×";close.setAttribute("aria-label",language==="ar"?"إغلاق الأسئلة الشائعة":"Close FAQs");close.addEventListener("click",()=>{root.classList.remove("sw-faq-open");one("[data-faq-browse]").setAttribute("aria-expanded","false");one("[data-faq-browse]").focus();});box.appendChild(close);
 for(const [question,answer,followup,path] of window.SilwadiFaq[language]){const detail=document.createElement("details"),summary=document.createElement("summary"),body=document.createElement("p"),actions=document.createElement("div"),button=document.createElement("button"),link=document.createElement("a");summary.textContent=question;safeText(body,answer);button.type="button";button.className="sw-chip";button.textContent=language==="ar"?"اسأل عن هالموضوع":"Ask a follow-up";button.addEventListener("click",()=>{root.classList.remove("sw-faq-open");one("[data-faq-browse]").setAttribute("aria-expanded","false");ask(followup);});link.href=path;link.textContent=language==="ar"?"عرض التفاصيل ↗":"View details ↗";actions.append(button,link);detail.append(summary,body,actions);box.appendChild(detail);}
}
function renderChips(){
 const box=one("[data-suggestions]");box.replaceChildren();
 dictionary[language].topics.forEach(([name,question])=>{
  const b=document.createElement("button");b.type="button";b.className="sw-chip";b.textContent=name;
  b.addEventListener("click",()=>ask(question));box.appendChild(b);
 });
}
function languageUI(lang){
 language=lang;root.dataset.language=lang;if(page&&window.SilwadiSiteShell)window.SilwadiSiteShell(lang);
 one("[data-title]").textContent=t("title");
 one("[data-sub]").textContent=t("sub");
 one("[data-greeting]").textContent=t("greeting");
 if(page){one("[data-kicker]").textContent=lang==="ar"?"أسئلة الأسنان، بطريقة أبسط":"DENTAL QUESTIONS, SIMPLIFIED";one("a.sw-page-nav").textContent=lang==="ar"?"موقع العيادة ↗":"Clinic website ↗";}
 one("[data-intro]").textContent=t("intro");
 one("[data-common]").textContent=t("common");
 one("[data-tooltip]").textContent=t("launcher");
 one("[data-help]").textContent=t("help");
 one("[data-book]").textContent=t("book")+" ↗";
 one("[data-privacy]").textContent=t("privacy");
 one("[data-code-help]").textContent=t("codeHelp");
 one("button.sw-language").textContent=lang==="en"?"عربي":"EN";
 one("[data-new]").setAttribute("aria-label",t("restart"));
 one("[data-close]").setAttribute("aria-label",t("close"));
 input.placeholder=t("prompt");
 input.dir=isArabic(input.value)||lang==="ar"?"rtl":"ltr";
 one("[data-welcome]").dir=lang==="ar"?"rtl":"ltr";
 renderChips();renderFaq();if(page)one("[data-faq-browse]").textContent=lang==="ar"?"الأسئلة الشائعة":"Browse FAQs";
 if(booking){booking.lang=lang;drawBooking();}
}
function scrollEnd(){requestAnimationFrame(()=>{conversation.scrollTop=conversation.scrollHeight;});}
function resize(){input.style.height="auto";input.style.height=Math.min(input.scrollHeight,107)+"px";input.dir=isArabic(input.value)||language==="ar"?"rtl":"ltr";input.readOnly=busy||!!booking;send.disabled=busy||!!booking||!input.value.trim();}
function setBusy(val){busy=val;input.readOnly=val;send.disabled=val||!input.value.trim();all(".sw-chip,.sw-choice").forEach(x=>{x.disabled=val;});}
function safeText(parent,text){
 const source=String(text||"");let last=0;const regex=/(\+971(?:[\s-]*\d){8,12})/g;
 for(const m of source.matchAll(regex)){
  if(m.index>last)parent.appendChild(document.createTextNode(source.slice(last,m.index)));
  const isolated=document.createElement("bdi");isolated.dir="ltr";isolated.textContent=m[0];parent.appendChild(isolated);
  last=m.index+m[0].length;
 }if(last<source.length)parent.appendChild(document.createTextNode(source.slice(last)));
}
function inline(el,inputText){
 const source=String(inputText||"");let at=0;const regex=/(\*\*[^*\n]+\*\*|\[[^\]\n]{1,85}\]\(https:\/\/[^\s)]+\))/g;
 for(const m of source.matchAll(regex)){
  if(m.index>at)safeText(el,source.slice(at,m.index));
  const value=m[0];
  if(value.startsWith("**")){const b=document.createElement("strong");safeText(b,value.slice(2,-2));el.appendChild(b);}
  else{
   const parts=value.match(/^\[([^\]]+)\]\((https:\/\/[^\s)]+)\)$/);let trusted=false;
   if(parts){try{const u=new URL(parts[2]);trusted=u.protocol==="https:"&&!u.username&&!u.password&&["silwadi.ae","www.silwadi.ae","wa.me"].includes(u.hostname);}catch{}}
   if(trusted){const a=document.createElement("a");a.href=parts[2];a.target="_blank";a.rel="noopener noreferrer";a.textContent=parts[1];el.appendChild(a);}
   else safeText(el,value);
  }
  at=m.index+value.length;
 }
 if(at<source.length)safeText(el,source.slice(at));
}
function render(el,answer){
 let buf=[],list=null;const lines=String(answer||"").replace(/\r\n?/g,"\n").trim().split("\n");
 const flush=()=>{if(!buf.length)return;const p=document.createElement("p");inline(p,buf.join(" ").trim());el.appendChild(p);buf=[];};
 for(const s of lines){const line=s.trim();if(!line){flush();list=null;continue;}const bullet=line.match(/^[-•]\s+(.+)$/);
  if(bullet){flush();if(!list){list=document.createElement("ul");el.appendChild(list);}const li=document.createElement("li");inline(li,bullet[1]);list.appendChild(li);}
  else{list=null;buf.push(line);}
 }flush();
}
function iconMark(){const mark=document.createElement("span");mark.className="sw-avatar";mark.setAttribute("aria-hidden","true");
 const im=document.createElement("img");im.src=icon;im.alt="";mark.appendChild(im);return mark;
}
function message(role,text,messageLanguage,pending=false){
 welcome.hidden=true;
 const row=document.createElement("article");row.className="sw-message sw-"+role+(pending?" sw-pending":"");row.dir="ltr";
 const body=document.createElement("div");body.className="sw-message-body";
 if(role==="assistant"){row.appendChild(iconMark());const who=document.createElement("div");who.className="sw-who";who.textContent=messageLanguage==="ar"?"مساعد سلوادي":"Silwadi Assistant";body.appendChild(who);}
 const bubble=document.createElement("div");bubble.className="sw-bubble";bubble.dir=messageLanguage==="ar"?"rtl":"ltr";bubble.lang=messageLanguage;
 if(pending){bubble.innerHTML='<span class="sw-typing" aria-label="Loading"><i></i><i></i><i></i></span>';}
 else if(role==="user"){bubble.textContent=text;}
 else{render(bubble,text);}
 body.appendChild(bubble);
 if(role==="user"&&text.length>260){
  bubble.classList.add("sw-collapsed");
  const toggle=document.createElement("button");toggle.className="sw-show";toggle.type="button";toggle.textContent=messageLanguage==="ar"?dictionary.ar.more:dictionary.en.more;
  toggle.addEventListener("click",()=>{
   const collapsed=bubble.classList.toggle("sw-collapsed");
   toggle.textContent=messageLanguage==="ar"?(collapsed?dictionary.ar.more:dictionary.ar.less):(collapsed?dictionary.en.more:dictionary.en.less);
  });body.appendChild(toggle);
 }
 if(role==="assistant"&&!pending){
  const copy=document.createElement("button");copy.type="button";copy.className="sw-copy";
  copy.textContent=messageLanguage==="ar"?dictionary.ar.copy:dictionary.en.copy;
  copy.addEventListener("click",async()=>{try{await navigator.clipboard.writeText(text);copy.textContent=messageLanguage==="ar"?dictionary.ar.copied:dictionary.en.copied;}catch{}});
  body.appendChild(copy);
 }
 row.appendChild(body);messages.appendChild(row);scrollEnd();return row;
}
async function ask(value){
 const q=String(value||"").trim();if(!q||busy||booking)return;
 if(q.length>650){one("[data-announcement]").textContent=language==="ar"?"السؤال طويل جداً.":"Please shorten your question.";return;}
 if(clarification?.kind==="booking"){
  const s=q.toLowerCase().replace(/[!.؟?]/g,'').trim();
  if(/^(?:yes|yeah|yea|yep|sure|ok|okay|هيه|اي|ايه|نعم|تمام|اوكي)$/.test(s)){const lang=clarification.lang;clarification=null;version++;input.value="";startBooking(lang);return;}
  if(/^(?:no|nope|nah|لا)$/.test(s)){const lang=clarification.lang;clarification=null;version++;input.value="";message("assistant",lang==="ar"?"تمام، شو تقصد؟":"Okay—what did you mean?",lang);resize();return;}
 }
 clarification=null;
 if(bookingPolicy&&bookingPolicy.intent(q)){input.value="";startBooking(isArabic(q)?"ar":language,bookingPolicy.preferredDoctor(q));return;}
 if(bookingPolicy?.clarification(q)==="booking"){
  const lang=isArabic(q)?"ar":language;input.value="";message("user",q,lang);const token=++version;
  const row=message("assistant",lang==="ar"?"تقصد تحجز موعد عند سلوادي؟":"Did you mean book an appointment at Silwadi?",lang);
  clarification={kind:"booking",lang};addChoices(row,["booking","other"],lang,token);resize();return;
 }
 const ar=isArabic(q),ql=ar?"ar":"en";
 message("user",q,ql);
 input.value="";resize();
 const current=++version;const pending=message("assistant","",ql,true);
 setBusy(true);const controller=new AbortController();abort=controller;const timer=setTimeout(()=>controller.abort(),30000);
 try{
  const verification=await verifyRequest(controller.signal);
  const response=await fetch(api,{method:"POST",credentials:"omit",cache:"no-store",
   headers:{"Content-Type":"application/json","X-Silwadi-Token":verification.token,"X-Silwadi-Proof":String(verification.proof)},
   body:JSON.stringify({question:q,context}),signal:controller.signal});
  const data=await response.json().catch(()=>({}));
  if(current!==version)return;
  pending.remove();
  if(!response.ok||!["ai","reviewed","unavailable"].includes(data.mode)||typeof data.answer!=="string"||data.answer.length>2200)throw Error();
  const replyLanguage=data.language==="ar"?"ar":ql;
  const row=message("assistant",data.answer,replyLanguage);
  if(Array.isArray(data.choices))addChoices(row,data.choices.slice(0,3),replyLanguage,current,data.bookingDoctor);
  if(data.mode==="ai"||["clarification","services"].includes(data.category))context=[...context,{role:"user",content:q},{role:"assistant",content:data.answer}].slice(-4);
  else context=[];
 }catch{
  if(current!==version)return;
  const failedText=bookingPolicy?.emergencyFailure(q)?(ar?dictionary.ar.error:dictionary.en.error):(ar?"تعذّر الاتصال. جرّب مرة ثانية، أو تواصل مع استقبال سلوادي.":"I couldn’t connect. Please try again, or contact Silwadi reception.");
  pending.remove();message("assistant",failedText,ql);
 }finally{clearTimeout(timer);if(current===version){abort=null;setBusy(false);resize();}}
}
async function verifyRequest(signal){
 const r=await fetch('https://booking.silwadi.ae/assistant-challenge.php',{method:'POST',credentials:'omit',cache:'no-store',headers:{'Content-Type':'application/json'},body:'{}',signal});
 if(!r.ok)throw Error('verification_unavailable');const c=await r.json();if(typeof c.token!=='string'||c.token.length>600||c.difficulty!==3)throw Error('invalid_challenge');
 const encode=new TextEncoder();for(let proof=0;proof<=2000000;proof++){if(signal.aborted)throw Error('cancelled');const hash=new Uint8Array(await crypto.subtle.digest('SHA-256',encode.encode(c.token+':'+proof)));if(hash[0]===0&&hash[1]<16)return {token:c.token,proof};if(proof%100===0)await new Promise(resolve=>setTimeout(resolve,0));}throw Error('verification_failed');
}
function setOpen(open){
 if(page)open=true;
 opened=!!open;root.classList.toggle("sw-open",opened);panel.inert=!opened;
 panel.setAttribute("aria-hidden",String(!opened));launch.setAttribute("aria-expanded",String(opened));
 launch.setAttribute("aria-label",opened?t("close"):t("launcher"));
 if(opened){setTimeout(()=>input.focus({preventScroll:true}),window.matchMedia("(prefers-reduced-motion: reduce)").matches?0:180);scrollEnd();}
 else launch.focus({preventScroll:true});
}
function reset(){
 version++;if(abort)abort.abort();abort=null;context=[];clarification=null;booking=null;bookingCard=null;messages.replaceChildren();welcome.hidden=false;input.value="";setBusy(false);languageUI(language);resize();
}
launch.addEventListener("click",()=>setOpen(!opened));
one("[data-book]").addEventListener("click",event=>{if(!bookingPolicy)return;event.preventDefault();setOpen(true);startBooking();});
one("[data-close]").addEventListener("click",()=>setOpen(false));
one("[data-scrim]").addEventListener("click",()=>setOpen(false));
one("button.sw-language").addEventListener("click",()=>languageUI(language==="en"?"ar":"en"));
one("[data-new]").addEventListener("click",reset);
one("[data-privacy]").addEventListener("click",()=>{const box=one("[data-config]");box.hidden=!box.hidden;if(!box.hidden)scrollEnd();});
one("[data-form]").addEventListener("submit",event=>{event.preventDefault();ask(input.value);});
input.addEventListener("input",resize);
input.addEventListener("keydown",event=>{if(event.key==="Enter"&&!event.shiftKey&&!event.isComposing){event.preventDefault();ask(input.value);}});
document.addEventListener("keydown",event=>{if(event.key==="Escape"&&opened)setOpen(false);});
window.addEventListener("silwadi:assistant:open",()=>setOpen(true));
panel.inert=true;languageUI(page&&new URLSearchParams(location.search).get("lang")==="ar"?"ar":"en");resize();
if(page)setOpen(true);
})();
