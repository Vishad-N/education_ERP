# P6.2 Completion Evidence

Date: 2026-08-14

## Implemented scope

- Expiring hashed student portal access.
- Scoped bilingual student/guardian snapshot for profile, dues, receipts, documents and notices.
- Token-scoped receipt PDF download.
- Retry-safe student payment order initiation.
- ERPNext `Payment Entry` and `Student Fee Payment` posting after provider capture.
- Duplicate capture callback idempotency.
- Local fake OTP challenge and verification contract.
- Payment status polling in the portal UI.

## Verification

- Snapshot returned student `EDU-STU-2026-00002`, one generated demand and two posted receipts.
- Receipt download returned HTTP 200, `application/pdf`, 17,315 bytes.
- Payment initiation retry reused the same `Student Portal Payment Attempt` and fake provider order.
- Positive capture proof posted `Payment Entry ACC-PAY-2026-00007` and `Student Fee Payment SFP-SFD-EDU-STU-2026-00002-EFP-P51-POLICY-2026.1-00180-00182`.
- Duplicate capture returned `idempotent: true` without a second accounting result.
- Fake OTP request returned challenge `SPO-00172`; verification returned `Verified`.
- `/student-portal` and its built asset returned HTTP 200.
- `npm.cmd run build`, documentation lint and repository checks passed.

## Deferred release work

- Replace fake OTP delivery with the approved SMS provider and real rate limits.
- Configure real payment provider callback credentials and reconciliation.
- Complete the deferred human/mobile/Hindi/usability checklist in `docs/quality/human-testing-readme.md`.
- Continue broader automated permission, security, migration and browser testing in Phase 7.
