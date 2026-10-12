(() => {
"use strict";
if (window.__SILWADI_ASSISTANT__) return;
window.__SILWADI_ASSISTANT__ = true;
const config = window.SILWADI_AI_CONFIG || {};
const script = document.currentScript;
const base = new URL(script && script.src ? script.src : "/ai/preview/silwadi-ai-widget.js", location.href);
const icon = config.icon || new URL("../../favicon.svg", base).href;
const api = config.endpoint || "/api/silwadi-widget";
const memoryKey = "silwadi_review_code";
const dictionary = {
  en: {
    title:"Silwadi Assistant",sub:"Dental & clinic information",launcher:"Ask Silwadi",
    greeting:"How can we help?",intro:"Find a dentist, explore dental services, or plan your visit.",
    help:"General information only. Not a diagnosis. Please don't share personal medical details.",
    prompt:"Ask a general question…",book:"Request an appointment",more:"Read full question",less:"Show less",
    restart:"New conversation",close:"Close chat",privacy:"Privacy & testing",
    code:"Review code (optional)",codeHelp:"Enables live AI wording tests on general topics only.",codeSave:"Enable testing",
    codeSaved:"Code saved for this tab.",codeError:"Please check the code.",
    error:"I couldn't get an answer. Reception can help you directly.",copy:"Copy answer",copied:"Copied",
    common:"Popular questions",typing:"Preparing an answer",
    topics:[
      ["Find a dentist","Which Silwadi doctor provides root canal treatment?"],
      ["Clinic locations","Where are Silwadi's clinics in Abu Dhabi?"],
      ["Treatments","Which dental services do you provide?"],
      ["Appointments","How can I request an appointment?"]
    ]
  },
  ar: {
    title:"مساعد سلوادي",sub:"معلومات الأسنان والعيادة",launcher:"اسأل سلوادي",
    greeting:"كيف نقدر نساعدك؟",intro:"تعرف على أطبائنا وخدمات الأسنان وفروعنا في أبوظبي.",
    help:"معلومات عامة فقط، وليست تشخيصاً. لا تشارك معلوماتك الصحية الشخصية.",
    prompt:"اكتب سؤالاً عاماً…",book:"طلب موعد",more:"عرض السؤال كاملاً",less:"عرض أقل",
    restart:"محادثة جديدة",close:"إغلاق المحادثة",privacy:"الخصوصية والتجربة",
    code:"رمز المراجعة (اختياري)",codeHelp:"لتجربة الصياغة الذكية للأسئلة العامة فقط.",codeSave:"تفعيل التجربة",
    codeSaved:"تم حفظ الرمز لهذه الجلسة.",codeError:"تأكد من الرمز.",
    error:"تعذّر الحصول على إجابة. تواصل مع الاستقبال للمساعدة.",copy:"نسخ الإجابة",copied:"تم النسخ",
    common:"أسئلة شائعة",typing:"جاري إعداد الرد",
    topics:[
      ["اختيار الطبيب","أي أخصائي في سلوادي يعالج عصب الأسنان؟"],
      ["فروع العيادة","وين فروع سلوادي في أبوظبي؟"],
      ["العلاجات","شو علاجات الأسنان اللي تقدمونها؟"],
      ["حجز موعد","كيف أقدر أطلب موعد عندكم؟"]
    ]
  }
};
const mount=document.createElement("div");
mount.id="silwadi-assistant-mount";
document.body.appendChild(mount);
const shadow=mount.attachShadow({mode:"open"});
const sheet=document.createElement("link");
sheet.rel="stylesheet";
sheet.href=new URL("silwadi-ai-widget.css?v=20261012a",base).href;
shadow.appendChild(sheet);
const markup=[
'<div class="sw-root">',
'<div class="sw-scrim" data-scrim></div>',
'<section class="sw-panel" id="sw-panel" role="dialog" aria-modal="false" aria-label="Silwadi Assistant" aria-hidden="true">',
'<header class="sw-head"><span class="sw-identity"><span class="sw-mark"><img data-mark alt=""></span><span class="sw-brand-copy"><strong data-title>Silwadi Assistant</strong><small data-sub>Dental & clinic information</small></span></span>',
'<span class="sw-tools"><button type="button" class="sw-small-button sw-language" data-language aria-label="Switch language">عربي</button>',
'<button type="button" class="sw-icon-button" data-new title="New conversation" aria-label="New conversation"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M12 5v14M5 12h14"/></svg></button>',
'<button type="button" class="sw-icon-button" data-close title="Close chat" aria-label="Close chat"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M5 5l14 14M19 5 5 19"/></svg></button></span></header>',
'<div class="sw-conversation" data-conversation><div class="sw-welcome" data-welcome>',
'<div class="sw-welcome-icon"><img data-mark alt=""></div><h2 data-greeting>How can we help?</h2><p data-intro>Find a dentist, explore dental services, or plan your visit.</p>',
'<div class="sw-quick-label" data-common>Popular questions</div><div class="sw-suggestions" data-suggestions></div></div>',
'<div class="sw-messages" data-messages role="log" aria-live="polite" aria-relevant="additions text"></div></div>',
'<div class="sw-footer"><form class="sw-composer" data-form>',
'<label for="sw-question" class="sw-sr-only">Ask Silwadi</label><textarea id="sw-question" data-question rows="1" maxlength="650" placeholder="Ask a general question…" autocomplete="off"></textarea>',
'<button class="sw-send" type="submit" data-send disabled aria-label="Send"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg></button></form>',
'<div class="sw-safety"><span class="sw-safety-sign" aria-hidden="true">i</span><span data-help></span></div>',
'<div class="sw-links"><a data-book href="https://silwadi.ae/contact.html#consultation-form" target="_blank" rel="noopener noreferrer"></a><button type="button" data-privacy>Privacy & testing</button></div>',
'<div class="sw-config" data-config hidden><p data-code-help></p>',
'<form data-code-form><label data-code-label for="sw-code">Review code (optional)</label><div class="sw-config-input"><input data-code id="sw-code" type="password" autocomplete="off"><button data-code-submit type="submit">Enable testing</button></div></form><p data-code-status role="status"></p></div>',
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
const prefersReduced=window.matchMedia("(prefers-reduced-motion: reduce)");
let language="en",opened=false,busy=false,abort=null,version=0,reviewCode="";
try{reviewCode=sessionStorage.getItem(memoryKey)||"";}catch{}
const t=k=>dictionary[language][k]||k;
const isArabic=q=>/[\u0600-\u06ff]/.test(String(q||""));
function renderChips(){
 const box=one("[data-suggestions]");box.replaceChildren();
 dictionary[language].topics.forEach(([name,question])=>{
  const b=document.createElement("button");b.type="button";b.className="sw-chip";b.textContent=name;
  b.addEventListener("click",()=>ask(question));box.appendChild(b);
 });
}
function languageUI(lang){
 language=lang;root.dataset.language=lang;
 one("[data-title]").textContent=t("title");
 one("[data-sub]").textContent=t("sub");
 one("[data-greeting]").textContent=t("greeting");
 one("[data-intro]").textContent=t("intro");
 one("[data-common]").textContent=t("common");
 one("[data-tooltip]").textContent=t("launcher");
 one("[data-help]").textContent=t("help");
 one("[data-book]").textContent=t("book")+" ↗";
 one("[data-privacy]").textContent=t("privacy");
 one("[data-code-help]").textContent=t("codeHelp");
 one("[data-code-label]").textContent=t("code");
 one("[data-code-submit]").textContent=t("codeSave");
 one("[data-language]").textContent=lang==="en"?"عربي":"EN";
 one("[data-new]").setAttribute("aria-label",t("restart"));
 one("[data-close]").setAttribute("aria-label",t("close"));
 input.placeholder=t("prompt");
 input.dir=isArabic(input.value)||lang==="ar"?"rtl":"ltr";
 one("[data-welcome]").dir=lang==="ar"?"rtl":"ltr";
 renderChips();
}
function scrollEnd(){requestAnimationFrame(()=>{conversation.scrollTop=conversation.scrollHeight;});}
function resize(){input.style.height="auto";input.style.height=Math.min(input.scrollHeight,107)+"px";input.dir=isArabic(input.value)||language==="ar"?"rtl":"ltr";send.disabled=busy||!input.value.trim();}
function setBusy(val){busy=val;input.readOnly=val;send.disabled=val||!input.value.trim();all(".sw-chip").forEach(x=>{x.disabled=val;});}
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
const danger=/(?:can(?:not|'t) breathe|difficulty breathing|difficulty swallowing|can't swallow|uncontrolled bleeding|نزيف ما يوقف|صعوبة في التنفس|صعوبة في البلع|ما اقدر اتنفس)/i;
const identifying=/(?:[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}|(?:\+?\d[\s.()\-]?){10,}|emirates id|رقم الهوية|رقم جوازي|رقم الملف)/i;
const personal=/(?:\b(?:my tooth|my teeth|my gums|i have|i take|i am taking|i'm taking|my child|my mother|my father|i've had)\b|عندي|صار لي|أخذ دواء|اخذ دواء|آخذ|مركّب دعامة|مركب دعامة|ضرسي يعورني|سني يعورني|اللثة عندي)/i;
function safety(q){
 const ar=isArabic(q);
 if(identifying.test(q))return ar?"لحماية خصوصيتك، لا تشارك بياناتك الشخصية أو ملفاتك الطبية هنا. تواصل مع الاستقبال عبر القنوات الرسمية.":"To protect your privacy, please don't enter contact details, identifiers or medical records. Contact reception privately.";
 if(danger.test(q))return ar?"صعوبة التنفس أو البلع أو النزيف الشديد الذي لا يتوقف قد تكون حالة طارئة. اطلب المساعدة الطبية الطارئة فوراً.":"Difficulty breathing or swallowing, or severe uncontrolled bleeding, may be an emergency. Seek emergency care immediately.";
 if(personal.test(q))return ar?"ما أقدر أشخّص حالتك أو أقيّم تاريخك الطبي في المحادثة. تواصل مع استقبال سلوادي لحجز تقييم عند طبيب الأسنان. إذا عندك انتفاخ شديد أو حرارة أو ألم يزداد بسرعة، اطلب تقييماً عاجلاً.":"I can help with general dental information, but can't assess personal symptoms or medical history here. Contact Silwadi reception for a dental assessment. Seek urgent care for significant swelling, fever or quickly worsening pain.";
 return "";
}
async function ask(value){
 const q=String(value||"").trim();if(!q||busy)return;
 if(q.length>650){one("[data-announcement]").textContent=language==="ar"?"السؤال طويل جداً.":"Please shorten your question.";return;}
 const ar=isArabic(q),ql=ar?"ar":"en";
 message("user",q,ql);
 input.value="";resize();
 const safe=safety(q);if(safe){message("assistant",safe,ql);return;}
 const current=++version;const pending=message("assistant","",ql,true);
 setBusy(true);abort=new AbortController();const timer=setTimeout(()=>abort.abort(),23000);
 try{
  const response=await fetch(api,{method:"POST",credentials:"omit",cache:"no-store",
   headers:{"Content-Type":"application/json",...(reviewCode?{"X-Silwadi-Review-Code":reviewCode}:{})},
   body:JSON.stringify({question:q}),signal:abort.signal});
  const data=await response.json().catch(()=>({}));
  if(current!==version)return;
  pending.remove();
  if(!response.ok||typeof data.answer!=="string")throw Error();
  message("assistant",data.answer,data.language==="ar"?"ar":ql);
 }catch{
  if(current!==version)return;
  pending.remove();message("assistant",ar?dictionary.ar.error:dictionary.en.error,ql);
 }finally{clearTimeout(timer);if(current===version){abort=null;setBusy(false);resize();}}
}
function setOpen(open){
 opened=!!open;root.classList.toggle("sw-open",opened);panel.inert=!opened;
 panel.setAttribute("aria-hidden",String(!opened));launch.setAttribute("aria-expanded",String(opened));
 launch.setAttribute("aria-label",opened?t("close"):t("launcher"));
 if(opened){setTimeout(()=>input.focus({preventScroll:true}),window.matchMedia("(prefers-reduced-motion: reduce)").matches?0:180);scrollEnd();}
 else launch.focus({preventScroll:true});
}
function reset(){
 version++;if(abort)abort.abort();abort=null;messages.replaceChildren();welcome.hidden=false;input.value="";setBusy(false);resize();
}
launch.addEventListener("click",()=>setOpen(!opened));
one("[data-close]").addEventListener("click",()=>setOpen(false));
one("[data-scrim]").addEventListener("click",()=>setOpen(false));
one("[data-language]").addEventListener("click",()=>languageUI(language==="en"?"ar":"en"));
one("[data-new]").addEventListener("click",reset);
one("[data-privacy]").addEventListener("click",()=>{const box=one("[data-config]");box.hidden=!box.hidden;if(!box.hidden)scrollEnd();});
one("[data-code-form]").addEventListener("submit",event=>{event.preventDefault();
 const value=one("[data-code]").value.trim();
 if(value.length<15){one("[data-code-status]").textContent=t("codeError");return;}
 reviewCode=value;try{sessionStorage.setItem(memoryKey,value);}catch{}
 one("[data-code-status]").textContent=t("codeSaved");one("[data-code]").value="";
});
one("[data-form]").addEventListener("submit",event=>{event.preventDefault();ask(input.value);});
input.addEventListener("input",resize);
input.addEventListener("keydown",event=>{if(event.key==="Enter"&&!event.shiftKey&&!event.isComposing){event.preventDefault();ask(input.value);}});
document.addEventListener("keydown",event=>{if(event.key==="Escape"&&opened)setOpen(false);});
window.addEventListener("silwadi:assistant:open",()=>setOpen(true));
panel.inert=true;languageUI("en");resize();
})();