const services=[
["Dental Implants","Implant placement, guided planning and implant-supported restorative solutions.","Implant care"],
["Orthodontics","Braces, aligners and orthodontic appliances for alignment and bite correction.","Orthodontic care"],
["Endodontics","Specialist root canal diagnosis and treatment focused on preserving natural teeth.","Root canal care"],
["Cosmetic Dentistry","Smile design, veneers, whitening and aesthetic restorative treatment planning.","Smile aesthetics"],
["Periodontics","Diagnosis and treatment of gum health and the supporting tissues around teeth.","Gum care"],
["Pediatric Dentistry","Preventive and restorative care designed around a comfortable experience for children.","Children's dentistry"],
["Prosthodontics","Crowns, bridges, veneers, dentures and complex restorative rehabilitation.","Restorative care"],
["Preventive Care","Routine examinations, hygiene, cleanings and preventive treatment planning.","Routine care"]
];
const doctors=[
["Dr. Munir Silwadi","Specialist Prosthodontist & Implantologist","dr-munir-silwadi.png",40],
["Dr. Moheb Silwadi","General Dentist","dr-moheb-silwadi.png",39],
["Dr. Hani Hasbini","Consultant Orthodontics","dr-hani-hasbini.png",38],
["Dr. Moammer Rifai","Specialist Orthodontics","dr-moammer-rifai.png",39],
["Dr. Ahmed El Shehri","Specialist Endodontics","dr-ahmed-el-shehri.png",38],
["Dr. Fahed Khalil","Specialist Periodontics","dr-fahed-khalil.png",40],
["Dr. Mohammed Abualkas","General Dentist","dr-mohammed-abualkas.png",39],
["Dr. Reem Alshaer","General Dentist","dr-reem-alshaer.png",38],
["Dr. Afnan Mashal","General Dentist","dr-afnan-mashal.png",39],
["Dr. Hawra'a Al Ameri","Specialist Periodontist","dr-hawraa-al-ameri.png",38],
["Dr. Ibrahem Abu Shanab","General Dentist","dr-ibrahem-abu-shanab.png",39],
["Dr. Krishnamurthy Katta Balajee","Specialist Orthodontist","dr-krishnamurthy-katta-balajee.png",40]
];
const treatmentNames=["Implantology","Orthodontics","Periodontics","Pediatric Dentistry","Endodontics","Cosmetic Dentistry","Preventive Care","Laser Dentistry","Prosthodontics"];
document.getElementById("serviceGrid").innerHTML=services.map((s,i)=>`<article class="service-card reveal"><span class="service-index">${String(i+1).padStart(2,"0")}</span><div><h3>${s[0]}</h3><p>${s[1]}</p><div class="service-footer"><span>${s[2]}</span><div class="service-arrow">↗</div></div></div></article>`).join("");
document.getElementById("teamGrid").innerHTML=doctors.map(d=>`<article class="doctor-card reveal"><div class="doctor-photo-wrap" style="--doctor-focus:${d[3]}%"><img src="assets/doctors/${d[2]}" alt="${d[0]}" class="doctor-photo" loading="lazy"></div><div class="doctor-copy"><h3>${d[0]}</h3><p>${d[1]}</p></div></article>`).join("");
const track=treatmentNames.map(x=>`<span>${x} <b>✦</b></span>`).join("");
document.getElementById("marqueeTrack").innerHTML=track+track;

// Consultation-first calls to action.
document.querySelectorAll("[data-book]").forEach(btn=>{
  btn.textContent="Book a Consultation";
});
const bookingTitle=document.getElementById("bookingTitle");
if(bookingTitle) bookingTitle.textContent="Book a consultation.";
const bookingEyebrow=document.querySelector("#bookingModal .eyebrow");
if(bookingEyebrow) bookingEyebrow.textContent="Consultations";
const bookingCopy=document.querySelector("#bookingModal .modal-card>p");
if(bookingCopy) bookingCopy.textContent="Choose the easiest way to reach the centre. Our team can help match you with the appropriate dentist or specialist.";
const emailOption=[...document.querySelectorAll(".booking-option")].find(a=>a.href.startsWith("mailto:"));
if(emailOption){
  emailOption.href="mailto:info@silwadidentalcentres.ae?subject=Consultation%20Request";
  const strong=emailOption.querySelector("strong");
  const small=emailOption.querySelector("small");
  if(strong) strong.textContent="Request a consultation";
  if(small) small.textContent="Send your preferred date, treatment concern and contact number.";
}
const bookSection=document.querySelector(".book");
if(bookSection){
  const label=bookSection.querySelector(".eyebrow");
  const title=bookSection.querySelector("h2");
  const copy=bookSection.querySelector("p");
  if(label) label.textContent="Consultations";
  if(title) title.textContent="Ready to speak with the right dentist?";
  if(copy) copy.textContent="Book a consultation and our team can help match you with the appropriate dentist or specialist for your concerns and treatment goals.";
}

const header=document.getElementById("siteHeader");
window.addEventListener("scroll",()=>header.classList.toggle("scrolled",window.scrollY>18),{passive:true});
const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add("visible");observer.unobserve(entry.target)}}),{threshold:.08});
document.querySelectorAll(".reveal").forEach(el=>observer.observe(el));
document.querySelectorAll(".faq-q").forEach(btn=>btn.addEventListener("click",()=>btn.parentElement.classList.toggle("open")));

const menuBtn=document.querySelector(".mobile-btn"),menu=document.getElementById("mobileNav"),modal=document.getElementById("bookingModal");
function closeMenu(){menu.classList.remove("open");document.body.classList.remove("menu-open");menuBtn.setAttribute("aria-expanded","false")}
menuBtn.addEventListener("click",()=>{const open=!menu.classList.contains("open");menu.classList.toggle("open",open);document.body.classList.toggle("menu-open",open);menuBtn.setAttribute("aria-expanded",String(open))});
menu.querySelectorAll("a").forEach(a=>a.addEventListener("click",closeMenu));
function openBooking(){closeMenu();modal.classList.add("open");document.body.classList.add("modal-open")}
function closeBooking(){modal.classList.remove("open");document.body.classList.remove("modal-open")}
document.querySelectorAll("[data-book]").forEach(btn=>btn.addEventListener("click",openBooking));
document.querySelector(".modal-close").addEventListener("click",closeBooking);
modal.addEventListener("click",e=>{if(e.target===modal)closeBooking()});
document.addEventListener("keydown",e=>{if(e.key==="Escape"){closeBooking();closeMenu()}});
