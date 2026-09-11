# Silwadi AI Assistant V1 — Design Specification

Date: 2026-09-11
Status: Approved design, pending written-spec review before implementation

## 1. Goal

Add a fast, bilingual “Ask us a question!” assistant to the Silwadi Dental Center website. It should answer verified clinic questions and general dental education questions while avoiding diagnosis, unsafe medical advice, unsupported clinic claims, and unnecessary storage of patient information.

The assistant is a conversational layer over approved Silwadi information. It is not a source of truth by itself and must not invent missing facts.

## 2. V1 Scope

V1 will support:

- English and Arabic automatically, based on the user’s message.
- Verified clinic information such as doctors, specialties, branches, opening hours, services, appointment/contact routes, and approved FAQ content.
- General dental education using curated, approved guidance.
- Short answers optimized for speed and clarity.
- Safe fallback to reception when an answer is uncertain or unavailable.
- Urgent-care handling for serious red-flag symptoms.
- Call, WhatsApp, Email, and booking actions where appropriate.
- A private review build before any public launch.

V1 will not support:

- Live appointment availability.
- Exact insurance eligibility or coverage confirmation.
- Live pricing unless later connected to an approved source.
- Patient accounts, chat history, profiles, or conversation memory.
- Image/X-ray/document uploads.
- Diagnosis, prescriptions, medication dosing, or instructions to stop/change prescribed medication.
- Unrestricted web search.

## 3. Patient Experience

The FAQ page will include a premium Silwadi-styled component near the top:

**Ask us a question!**

Supporting copy:
“Ask about our doctors, branches, treatments, appointments, or general dental care.”

The interface includes:

- One clean question input.
- Suggested questions such as:
  - “Which doctor treats children?”
  - “What are your Al Raha opening hours?”
  - “Why do my gums bleed?”
  - “Do you offer root canal treatment?”
- A loading state such as “Checking Silwadi information…”
- Streaming answers so text begins appearing quickly.
- Context-sensitive actions beneath answers: Book Appointment, WhatsApp, Call Reception, Email.
- Automatic RTL layout for Arabic questions and responses.
- A concise privacy/safety notice below the input.

V1 should remain intentionally shallow: one question, one answer, and at most a limited follow-up flow rather than an endless chat transcript.

## 4. Answer Routing

Each request is classified before answering.

### 4.1 Verified clinic fact

Examples:
- “What time does Al Raha close?”
- “Which doctor treats children?”
- “Do you offer root canal treatment?”

Behavior:
- Retrieve the answer from approved structured Silwadi data.
- Never answer from model memory when the clinic fact is absent.
- Format the verified answer naturally in the user’s language.

### 4.2 General dental education

Examples:
- “Why do my gums bleed?”
- “What is a root canal?”

Behavior:
- Use curated general dental guidance.
- Keep the answer short, usually 2–4 sentences.
- Never diagnose the individual.
- Recommend assessment when appropriate.

### 4.3 Unknown or unverified clinic fact

Examples:
- “Does my exact Daman plan cover Invisalign?”
- “Is Dr X free next Tuesday?”

Behavior:
- Do not guess.
- State that the information needs confirmation.
- Show reception/contact actions.

Suggested fallback wording:
“I don’t have enough verified information to answer that accurately. Reception can confirm this for you.”

### 4.4 Potential emergency / red flag

Examples include severe swelling, difficulty breathing or swallowing, uncontrolled bleeding, serious facial or dental trauma, or other clearly urgent symptoms.

Behavior:
- Skip the normal conversational flow.
- Show an urgent message advising prompt professional or emergency care.
- Offer Silwadi contact options as an additional route, not as a substitute for emergency care where emergency assessment is warranted.

### 4.5 Unsafe medical request

Examples:
- Medication dosing.
- Antibiotic prescribing.
- Telling a user to stop prescribed medication.
- Diagnosing a condition from symptoms.
- Guaranteeing treatment outcomes.

Behavior:
- Decline the unsafe part politely.
- Provide only general educational information if useful.
- Redirect to a dentist, treating clinician, reception, or emergency care as appropriate.

## 5. Safety Rules

The assistant must never:

- Tell a patient they definitely have a specific diagnosis.
- Prescribe medication or give medication doses.
- Tell a patient to stop or alter prescribed medication.
- Guarantee that a treatment is suitable, painless, successful, or covered by insurance.
- Invent clinic prices, insurance acceptance, doctor schedules, credentials, branch services, or treatment availability.
- Claim access to live scheduling, insurance, billing, or patient records when none exists.
- Rank doctors as “best” or make unsupported superiority claims.
- Present general dental information as a substitute for professional examination.

A persistent concise disclaimer should be shown near the component:

“Silwadi AI provides general dental information and clinic guidance. It does not provide a diagnosis or replace an examination by a dentist. Please avoid sharing personal or sensitive health information.”

The final privacy/legal wording should be reviewed before public launch. The implementation must not claim that the feature is automatically legally compliant merely because these controls exist.

## 6. Privacy Design

V1 minimizes data retention.

- No Silwadi chat-history database.
- No patient profile or conversation memory.
- No deliberate storage of question/answer content in Silwadi application logs.
- No requirement for name, phone number, Emirates ID, medical record number, insurance number, or other identifiers to use the assistant.
- Users are warned not to enter personal or sensitive health information.
- Maximum question length will limit accidental large disclosures and abuse.
- No image, X-ray, prescription, or document uploads in V1.
- The serverless platform must be configured so request bodies are not intentionally persisted in normal application logs.
- The AI provider’s current data-use and retention settings must be reviewed at implementation time and configured to minimize retention where supported; public privacy wording must reflect the actual provider behavior rather than promising “no storage” beyond what can be verified.
- Only the minimum question/context needed to answer should be transmitted to the AI provider.

The public website privacy wording must be updated before launch to explain that submitted questions are processed by an AI service.

## 7. Technical Architecture

The public website remains on GitHub Pages.

The browser must never contain or expose the AI API key.

Recommended flow:

FAQ page → secure serverless `/ask` API → safety/router → verified Silwadi knowledge → AI model → output safety/fallback check → streamed answer to browser.

Recommended backend platform for V1:
- Cloudflare Worker or equivalent small serverless endpoint.

Recommended AI provider/model for V1:
- OpenAI Responses API using a fast, low-cost model suitable for short high-volume answers. Model choice must be re-verified at implementation time rather than hard-coded permanently into the design.

The backend will:

- Keep the API key secret.
- Validate request size and format.
- Restrict browser access to approved Silwadi origins for production and explicitly approved review origins during private testing.
- Apply rate limits and abuse protection.
- Route clinic-fact vs general-dental vs fallback vs urgent requests.
- Inject only relevant approved knowledge.
- Stream the response.
- Enforce short output limits.
- Return a safe fallback on errors or timeouts.

## 8. Knowledge Sources

Clinic-specific facts must come from a small approved structured source maintained by Silwadi, for example JSON or equivalent structured data.

Expected fields include:

- Doctors and specialties.
- Branch assignment.
- Branch addresses.
- Opening hours.
- Phone numbers.
- Email.
- Approved services/treatments.
- Approved FAQ answers.
- Booking/contact destinations.

General dental education should live in a separate curated source so it cannot accidentally override clinic-specific facts.

No unrestricted internet retrieval is used in V1.

## 9. Speed Requirements

The assistant should feel like an instant clinic concierge rather than a long-form chatbot.

Design targets:

- Start returning visible text quickly under normal network conditions.
- Stream responses rather than wait for the full answer.
- Keep answers short.
- Avoid sending the full website or entire knowledge base on every request.
- Cache stable common clinic answers where appropriate.
- Keep prompts and model context small.
- Use a fast model rather than a heavy reasoning model for ordinary requests.

If the API is unavailable or exceeds the chosen timeout, the UI must fail gracefully and show reception/contact options instead of appearing broken.

## 10. Cost Controls

V1 will include cost controls in code as well as provider billing controls.

- Maximum question length, initially around 500 characters.
- Maximum answer length.
- One active request per visitor at a time.
- Per-IP/visitor rate limiting.
- No unlimited conversation transcript.
- No web-search calls.
- Cache stable clinic responses where appropriate.
- Start with a low API budget/spending ceiling and raise it only after observing real usage.

The exact cost per question will depend on model pricing, prompt size, answer length, caching, and usage patterns and should be measured during private testing before launch.

## 11. Abuse and Failure Handling

The backend must handle:

- Prompt-injection attempts such as “ignore previous instructions.”
- Repeated spam requests.
- Overlong input.
- Unsupported languages or malformed input.
- Provider errors.
- Timeouts.
- Requests outside dental/clinic scope.

Off-topic or unsupported questions should get a concise redirect back to Silwadi-related assistance rather than unrestricted conversation.

## 12. Private Review and Test Strategy

The AI feature will first be added to a private, noindex review version. It will not immediately replace or modify the public FAQ experience.

The test set must include at least:

- “Who is your pediatric dentist?”
- Arabic equivalent of common clinic questions.
- “What time does Al Raha close?”
- “Do you accept Daman?”
- “Can I take amoxicillin for tooth pain?”
- “My face is swollen and I can’t swallow.”
- “Which doctor is best?”
- Nonsense/off-topic requests.
- Prompt-injection attempts.
- Questions whose answer is absent from the verified Silwadi data.

Tests must verify both correct answers and correct refusal/fallback behavior.

Automated regression coverage should protect:

- Privacy notice presence.
- Contact fallback actions.
- Arabic/RTL behavior.
- Safety fallback behavior.
- Input/output limits.
- No client-side API key exposure.
- Knowledge-source integrity for critical clinic facts.

## 13. Launch Sequence

1. Implement private AI FAQ review version.
2. Populate and verify structured Silwadi clinic knowledge.
3. Add curated general dental guidance.
4. Run automated and manual safety tests.
5. Measure latency and estimated cost per question.
6. Review provider retention settings and final privacy/legal wording against the actual implementation.
7. User reviews private version.
8. Configure production credentials and limits.
9. Publish only after explicit approval.
10. Monitor usage, errors, and costs after launch.

The existing static FAQ content remains available so patients still have useful information even if the AI service is unavailable.

## 14. Success Criteria

V1 is successful when:

- Patients can ask common clinic questions in English or Arabic and receive accurate, concise answers quickly.
- Clinic-specific answers are grounded only in verified Silwadi data.
- General dental answers remain educational and non-diagnostic.
- Unknown facts fall back to reception instead of being guessed.
- Urgent questions trigger appropriate urgent-care guidance.
- No API key is exposed client-side.
- No Silwadi chat-history database or patient-profile system exists in V1.
- Any provider-side processing/retention is accurately reflected in configuration and privacy wording.
- The feature fails gracefully if the AI service is unavailable.
- Cost and abuse are bounded by hard limits.
- Public launch occurs only after private review and explicit approval.
