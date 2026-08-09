# Low-Literacy UX and Localization

## Product audience

The pilot serves a small-township high school where many guardians may have limited formal education, limited English, entry-level Android devices and unreliable mobile data. The guardian portal must be understandable without training or technical vocabulary.

## Experience principles

- Guardian-first rather than institution-structure-first.
- One clear task per screen.
- Three to five active fields at a time where practical.
- Large touch targets and readable text.
- Icons always accompanied by text.
- English/Hindi switch visible on every primary page.
- Autosave after meaningful progress and explicit saved status.
- Resume after session expiry, device change or network interruption.
- Prefer selections, examples and defaults over free typing.
- Explain exactly what happened and what to do next.
- Never use color alone to communicate status.
- Never show internal DocType, workflow, accounting or provider terminology.

## Primary guardian journeys

1. Register or sign in with mobile OTP.
2. Add/select a child.
3. Choose admission class/program.
4. Complete a short staged application.
5. Photograph/upload required documents.
6. Review a simple summary.
7. Pay application/admission/education fee.
8. Understand pending, successful or failed payment status.
9. Track application/offer/admission state.
10. Download or print application, offer, receipt and fee statement.

One guardian account must support multiple children and preserve institution separation.

## Bilingual implementation

- Store stable translation keys, not duplicated hard-coded strings.
- Use Unicode throughout database, API, templates, SMS/email and PDFs.
- Translate navigation, fields, help, errors, notifications and receipts consistently.
- Have local Hindi speakers review terminology; machine translation is not acceptance.
- Preserve names and identifiers exactly as entered while translating surrounding labels.
- Design for Hindi strings that may be longer than English.
- Format Indian currency, dates, mobile numbers and academic years consistently.

## Content style

Use direct, respectful instructions:

```text
Avoid: Authentication failed.
Use: We could not verify this mobile number. Request a new code.

Avoid: Payment reconciliation pending.
Use: Your payment is being checked. Do not pay again. We will update this page shortly.
```

Hindi messages must convey the same action and safety information, especially for payments and deadlines.

## Forms and documents

- Show why sensitive information is needed.
- Use camera upload with crop/compression guidance and progress.
- Show the uploaded image before confirmation.
- Keep failed uploads resumable.
- Clearly separate mandatory and optional documents.
- Allow authorized school staff to assist through an audited assisted-entry workflow.
- Generate printable bilingual summaries and receipts.

## Accessibility and low bandwidth

- Target WCAG 2.2 AA behaviors where applicable.
- Keyboard access, visible focus, screen-reader labels and sufficient contrast.
- Avoid decorative animation and heavy media.
- Lazy-load noncritical assets and compress uploads before transfer where safe.
- Preserve entered state when requests time out.
- Provide a plain retry action without duplicate submission/payment.
- Test on entry-level Android devices and slow mobile networks.

## Usability acceptance

Test prototypes and release candidates with at least 8-12 representative guardians/staff from the pilot community.

Pass when:

- at least 80 percent complete the primary journey without direct instruction;
- no participant loses entered data;
- payment status and the risk of paying twice are understood;
- required documents and next steps are understood;
- English/Hindi switching preserves progress;
- no critical accessibility or mobile-layout defect remains;
- observed problems are recorded and resolved or formally accepted.

## Staff interfaces

Frappe Desk remains appropriate for trained staff, but role workspaces must expose only frequent tasks, use school terminology and avoid overwhelming dashboards. High-risk actions require clear impact summaries, confirmation and maker-checker approval.

