# Patch 14 — Official Silwadi Content Alignment QA

Date: 2026-08-22

## Purpose

Patch 14 aligns the new `silwadi.ae` website with the factual service catalogue, patient-care positioning and operational information published on the existing official Silwadi Dental Centres website, while retaining the new site's cleaner clinical tone and design.

## Official source-of-truth pages reviewed

- Services: https://silwadidentalcentres.ae/services.php
- About: https://silwadidentalcentres.ae/about-us.php
- FAQ: https://silwadidentalcentres.ae/faq.php
- Contact: https://silwadidentalcentres.ae/contact-us.php
- Doctors: https://silwadidentalcentres.ae/doctors.php
- Dr. Munir Silwadi profile: https://silwadidentalcentres.ae/doctors-details/dr-mohamed-munir-juma-mousa.php

## Verified service catalogue

The public Treatments directory now presents exactly these ten official service lines, with two labels normalized for clear English presentation:

1. Implantology
2. Orthodontics
3. Periodontics
4. Pedodontics
5. Endodontics
6. Cosmetic Dentistry — official site label: “Cosmetics”
7. Preventive Treatments
8. Oral Hygiene
9. Laser Dentistry — official site label: “Laser”
10. Prosthodontics

Existing detailed pages remain available where useful for patients and SEO, but secondary procedures such as veneers, whitening and full-mouth rehabilitation are no longer presented as separate official Silwadi service departments.

## Supported secondary content

- Emergency dental care remains available as a secondary urgent-care route because the official site states that emergency services are available. It is not counted among the ten listed service lines.
- Digital Dentistry remains a clinical capability/technology page rather than an official service line. Dr. Munir Silwadi’s official profile supports CAD/CAM dentistry, intraoral scanning, computer-guided implant workflows, full-mouth rehabilitation and digital smile design.
- The unsupported homepage wording “Founder & specialist” was removed. Dr. Munir is presented using his supported specialist role.

## Values and operational facts aligned

Home and About now reflect the official site's patient-care themes:

- patient-centred care
- personalized treatment
- compassion and patient comfort
- patient education
- open communication
- comprehensive general and specialist dentistry

Contact and Locations now also expose verified operational facts from the official FAQ:

- insurance is accepted
- most insurance claims are submitted electronically on behalf of patients
- parking is available

The existing verified opening hours, phone, email, Bani Yas Tower address and Al Raha Mall “coming soon” status remain unchanged.

## Copy policy

The legacy site contains promotional wording such as “cutting-edge” and other superlative marketing language. Patch 14 deliberately does not import that wording. Facts and service scope are aligned to the official site while the new site keeps concise, medically responsible copy.

## TDD evidence

A Patch 14 content contract was added before implementation.

Initial RED run:

- 7 Patch 14 tests executed
- 6 failed for the identified mismatches
- 1 passed because Digital Dentistry was already correctly separated from the official service catalogue

The failing checks covered the official service list, homepage service labels, unverified founder wording, patient-care values, insurance claim handling and parking.

## Final clean verification

GitHub Actions ran against the clean Patch 14 HTML candidate:

- Python regression suite: **67/67 tests passed**
- JavaScript syntax: **PASS**
- SEO launch audit: **24 pages, 0 errors**
- Internal references: **876 local references, 0 broken**
- JSON-LD: **24 blocks, 0 errors**
- HTTP smoke: **29/29 returned 200**

A focused Lighthouse matrix covered the five changed public pages in mobile and desktop modes:

- Home
- Treatments
- About
- Contact
- Locations

Result: **10/10 Lighthouse jobs passed** the deterministic gate requiring Accessibility 100, Best Practices 100, SEO 100, passing color contrast and passing target-size audits when applicable.

As a representative result, Treatments mobile scored Performance 100 / Accessibility 100 / Best Practices 100 / SEO 100, with LCP 1.51 s and CLS 0.000 in the pre-launch CI run.

These Lighthouse results are pre-launch local-server measurements. Production Lighthouse/PageSpeed should still be rerun after public deployment because hosting, TLS, caching and network conditions can affect performance.
