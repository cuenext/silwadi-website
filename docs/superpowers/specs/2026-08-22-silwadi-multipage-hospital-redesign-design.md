# Silwadi Dental Center — Multi-Page Hospital-Style Redesign

Date: 2026-08-22
Status: Approved design, pending implementation plan

## 1. Objective

Transform the current single-page Silwadi Dental Center website into a professional multi-page healthcare website that feels like an established private hospital rather than a promotional landing page.

The approved visual direction is a hybrid of:
- hospital-level structure, clarity, and authority;
- premium private-clinic polish;
- restrained modern interactions;
- real people and clinical content over decorative UI effects.

The redesign must reduce crowding, remove the “AI landing page” feel, and give important information dedicated pages instead of placing everything on one long homepage.

## 2. Core Design Principles

1. **Calm, clinical, premium** — large areas of white, navy text, restrained teal accents.
2. **Content hierarchy first** — patients should immediately understand where to go next.
3. **Real healthcare institution feel** — thin dividers, disciplined spacing, subtle shadows, minimal gradients, almost no glassmorphism.
4. **Photography-led** — doctor and clinical photography should carry the visual identity.
5. **Smaller, more controlled typography** — avoid oversized SaaS-style headings.
6. **Minimal motion** — soft reveal transitions and restrained hover states only.
7. **Consultation-first CTA** — primary CTA is “Book a Consultation”.
8. **Multi-page SEO foundation** — important doctors and treatments get their own indexable pages.
9. **Mobile-first usability** — navigation, consultation actions, doctor directories, and treatment pages must remain easy to use on phone.
10. **Shared visual system** — all pages use the same header, footer, spacing, type scale, buttons, cards, and breadcrumb treatment.

## 3. Global Navigation

Primary navigation:
- Home
- Treatments
- Doctors
- About
- Digital Dentistry
- Locations
- Book a Consultation

Supporting contact actions may include:
- Call the Centre
- Email
- Location / directions

The header should be clean and hospital-like with a modest logo, strong alignment, minimal decoration, and a prominent consultation CTA.

## 4. Site Architecture

### Phase 1 pages

Build and fully style these first:

- `/index.html` — Home
- `/doctors.html` — Doctors directory
- `/doctors/dr-munir-silwadi.html` — Founder / doctor profile template
- `/treatments.html` — Treatment directory
- `/treatments/dental-implants.html` — Treatment detail template
- `/about.html` — About / history / philosophy
- `/digital-dentistry.html` — Technology and digital workflows
- `/locations.html` — Branch information
- `/contact.html` — Contact and consultation entry point

After these are proven, use the doctor-profile and treatment-detail templates for the remaining doctors and treatments.

## 5. Homepage

The homepage must be selective, calm, and significantly shorter than the current one.

### 5.1 Hero

White or very light background with restrained teal detail.

Left:
- Eyebrow: Dr. Munir Silwadi Dental Centre
- Headline: **Advanced dentistry. Established trust.**
- Short supporting copy focused on long-standing Abu Dhabi care, multidisciplinary expertise, and modern dentistry.
- Primary CTA: **Book a Consultation**
- Secondary CTA: **Find a Doctor**

Right:
- One strong real doctor / clinical image.
- No floating-pill clutter.
- At most one restrained trust/accreditation element if verified and visually useful.

### 5.2 Utility Bar

Compact hospital-style quick actions immediately under the hero:
- Find a Doctor
- Explore Treatments
- Insurance
- Locations
- Call Us

### 5.3 Treatment Preview

Show only four major pathways:
- Dental Implants
- Orthodontics
- Cosmetic & Restorative Dentistry
- General & Preventive Care

Each item includes a concise description and “View treatment”.

Finish with “View all treatments”.

### 5.4 Legacy / Trust

Quiet section led by:

**Serving Abu Dhabi since 1980**

Include a concise trust statement and a small number of verified factual stats. Avoid oversized decorative “1980” typography.

### 5.5 Featured Doctors

Show only four doctors on the homepage.

Required:
- Dr. Munir Silwadi first.
- Three additional doctors from the current roster.
- Clean portrait treatment.
- Name.
- Specialty.
- “View profile”.

No labels over faces or bodies.

Finish with “Meet the full medical team”.

### 5.6 Digital Dentistry Preview

One editorial horizontal feature rather than a grid of generic cards.

Highlight selected workflows such as:
- CAD/CAM dentistry
- guided implant planning
- digital smile planning

Finish with “Explore our technology”.

### 5.7 Locations

Two clean branch blocks:
- Bani Yas Tower — current location
- Al Raha Mall — clearly marked as coming soon unless status changes before launch

### 5.8 Final Consultation CTA

Dark navy closing section:

**Not sure which dentist you need?**

Supporting copy: the team can guide the patient to the appropriate clinician.

Actions:
- Book a Consultation
- Call the Centre

## 6. Doctors Directory

Path: `/doctors.html`

Purpose: make the medical team feel like a hospital consultant directory rather than a card wall.

### 6.1 Directory controls

- Search doctors by name.
- Filter by specialty.

Initial filter set:
- All
- Prosthodontics
- Orthodontics
- Periodontics
- Endodontics
- General Dentistry

### 6.2 Doctor listing

Desktop: cleaner horizontal or editorial profile cards.

Each item contains:
- portrait;
- doctor name;
- specialty;
- short clinical focus when verified;
- “View profile”.

Mobile: stack naturally while preserving portrait quality and readable hierarchy.

## 7. Doctor Profile Template

Example: `/doctors/dr-munir-silwadi.html`

Sections:
1. Breadcrumbs.
2. Professional portrait.
3. Doctor name and exact specialty.
4. Primary CTA: “Book a Consultation”.
5. Clinical interests / focus.
6. Qualifications / credentials.
7. Treatments provided.
8. Location / branch information where appropriate.
9. Related doctors.

For doctor-specific CTA copy, use:
**Book a consultation with Dr. [Name]**

Only verified public profile information should be shown.

## 8. Treatments Directory

Path: `/treatments.html`

Treatments are grouped rather than shown as one repetitive card wall.

### 8.1 Implant & Restorative
- Dental Implants
- Prosthodontics
- Full-Mouth Rehabilitation
- Crowns & Bridges

### 8.2 Smile & Aesthetic
- Cosmetic Dentistry
- Veneers
- Whitening
- Digital Smile Design

### 8.3 Specialist Dentistry
- Orthodontics
- Endodontics
- Periodontics
- Pediatric Dentistry

### 8.4 Routine Care
- General Dentistry
- Preventive Care
- Oral Hygiene

Only publish treatment names/details that are confirmed by current clinic information before launch.

## 9. Treatment Detail Template

Example: `/treatments/dental-implants.html`

Structure:
1. Breadcrumbs.
2. Clean treatment hero.
3. What the treatment is.
4. Who it may be suitable for.
5. Treatment approach / journey.
6. Relevant technology.
7. Doctors who provide the treatment.
8. FAQ.
9. Primary CTA: Book a Consultation.

Treatment copy must avoid overpromising and remain clinically responsible.

## 10. About Page

Path: `/about.html`

Purpose: move history and institutional story off the homepage.

Content areas:
- centre history since 1980;
- clinical philosophy;
- continuity of care;
- multidisciplinary model;
- founder story / Dr. Munir spotlight;
- how the centre combines established experience with modern dentistry.

Tone: institutional, human, concise.

## 11. Digital Dentistry Page

Path: `/digital-dentistry.html`

Purpose: present technology as part of clinical workflow rather than as marketing decoration.

Potential sections:
- CAD/CAM dentistry;
- intraoral scanning;
- guided implant planning;
- digital smile planning;
- other verified digital workflows.

Each technology section should explain:
- what it is;
- where it may be used;
- how it supports planning, communication, or treatment delivery.

Avoid unsupported claims of superior outcomes.

## 12. Locations Page

Path: `/locations.html`

Each location block contains:
- branch name;
- current status;
- full address;
- phone;
- hours;
- directions CTA;
- parking information when verified;
- insurance information when verified;
- consultation CTA.

Current known locations for the design:
- Bani Yas Tower
- Al Raha Mall — coming soon unless current status is updated before launch

## 13. Contact Page

Path: `/contact.html`

Purpose: create a clear institutional contact destination.

Include:
- Book a Consultation entry point;
- phone;
- email;
- location links;
- opening hours;
- insurance enquiry guidance;
- branch selection if needed.

Phase 1 consultation request can continue to use direct phone/email actions unless a real backend/form workflow is later approved.

## 14. Shared Components

Reusable site-wide components:
- top utility strip where useful;
- main hospital-style header;
- mobile navigation;
- breadcrumb component;
- page intro / hero component;
- consultation CTA component;
- doctor preview/profile component;
- treatment preview/list component;
- location block;
- footer;
- mobile consultation action bar if it remains visually restrained.

The current dynamic JavaScript rendering for essential doctor/treatment content should be reduced. Important indexable content should live directly in page HTML where practical.

## 15. Visual System

### Palette
- Primary navy based on current Silwadi direction.
- Teal / aqua as controlled accents.
- White and very pale cool neutral backgrounds.
- Dark neutral body text.
- Avoid excessive gradients.

### Typography
- Professional sans-serif system or carefully selected web-safe / externally hosted family.
- Smaller, more editorial heading scale than the current landing-page version.
- Strong hierarchy without dramatic oversized display text.

### Cards / Surfaces
- Thin borders.
- Subtle shadows only when needed.
- Moderate corner radii.
- No glassmorphism-heavy surfaces.

### Doctor Photography
- Consistent portrait treatment.
- Faces framed naturally.
- No specialty badges placed over the person.
- Use real supplied clinic portraits.

### Motion
- Soft fade / translate reveals.
- Restrained card hover states.
- No floating decorative UI or continuous motion except where truly useful.

## 16. Consultation Experience

Primary wording across the website:
**Book a Consultation**

Doctor-specific wording:
**Book a consultation with Dr. [Name]**

The consultation entry point should remain highly visible without making every section feel like an advertisement.

## 17. Responsive Behaviour

Desktop:
- strong horizontal layouts;
- balanced white space;
- hospital-like navigation;
- editorial doctor/treatment layouts.

Tablet:
- reduce columns progressively;
- preserve generous spacing and touch targets.

Mobile:
- compact header;
- clear mobile navigation;
- no overcrowded grids;
- doctor directory stacks cleanly;
- optional bottom consultation bar if it does not obscure content;
- all phone, email, and location actions remain directly tappable.

## 18. Accessibility & Semantics

Implementation should include:
- meaningful heading hierarchy;
- descriptive image alt text;
- keyboard-accessible navigation and dialogs;
- visible focus states;
- semantic links/buttons;
- adequate colour contrast;
- reduced-motion consideration;
- clear form labels if forms are introduced later.

## 19. SEO Foundation

Each page should have:
- unique title;
- unique meta description;
- canonical-ready URL structure;
- one clear H1;
- crawlable doctor/treatment content;
- internal links between doctors, treatments, locations, and consultation pages;
- Open Graph metadata where useful.

Future additions can include structured data for LocalBusiness / Dentist / Physician-style entities only after content and implementation are validated.

## 20. Content Safety / Verification

Before public launch, verify:
- doctor specialties and credentials;
- branch status;
- hours;
- phone and email;
- insurance claims;
- technology availability;
- treatment scope;
- any regulatory/accreditation language.

Do not invent medical claims, awards, accreditations, affiliations, patient outcomes, or treatment guarantees.

## 21. Implementation Strategy

Phase 1 should establish the visual system and page templates first rather than mass-producing every profile and treatment page.

Recommended order:
1. Shared CSS / layout / navigation system.
2. New homepage.
3. Doctors directory.
4. Dr. Munir profile template.
5. Treatments directory.
6. Dental implants treatment template.
7. About.
8. Digital Dentistry.
9. Locations.
10. Contact.
11. Responsive polish and accessibility pass.
12. Duplicate approved templates for remaining doctors/treatments in later patches.

This protects consistency and avoids generating many mediocre pages before the underlying system is proven.

## 22. Definition of Success

The redesign is successful when:
- the homepage feels calm rather than crowded;
- users can reach doctors, treatments, locations, and consultation actions within one or two clicks;
- the visual identity feels like an established healthcare institution rather than a generic marketing template;
- doctor imagery feels natural and professional;
- mobile use is clean and fast;
- important content is separated into meaningful pages;
- the design retains Silwadi’s existing navy/teal identity without looking dated;
- the site is structured so future SEO and content expansion are straightforward.
