# P6.2 Initial Student Portal Slice

Date: 2026-08-13

## Scope

P6.2 now has a scoped read-only student/guardian portal snapshot. Access is represented by an expiring token whose SHA-256 hash is stored in `Student Portal Access`; the endpoint does not expose arbitrary Frappe list access.

## Implementation

- `Student Portal Access` binds one access token to one student, with status, expiry and last-use tracking.
- `get_student_portal_snapshot` returns the bound student's identity, generated fee dues, posted receipt records and student documents.
- `StudentPortal.vue` provides a mobile-first English/Hindi view at `/student-portal`.
- `download_student_receipt` verifies the receipt belongs to the scoped student and returns a generated PDF.
- `Student Portal Notice` provides published notices for students and guardians.
- `create_student_payment` creates a retry-safe fake-provider order only for a generated demand belonging to the scoped student.
- The view keeps the access token in the URL only for the initial handoff and then stores it locally for resume.

## Verification

Against the local `p21.localhost` site:

- Migration installed the new DocType successfully.
- Synthetic access `SPA-EDU-STU-2026-00002-00169` was created for `EDU-STU-2026-00002` with an expiry of `2027-01-01`.
- Snapshot proof returned student `EDU-STU-2026-00002`.
- Snapshot proof returned one generated demand for `850.0` and two posted receipts for `450.0` and `400.0`.
- Snapshot proof returned zero unrelated student documents.
- Snapshot proof returned the published synthetic notice `SPN-00170`.
- Receipt download returned HTTP 200 with `application/pdf` and a 17,315-byte response for a permitted receipt.
- First student payment initiation returned `SPPA-SFD-EDU-STU-2026-00002-EFP-P51-POLICY-2026.1-00109-00171` with provider order `order_000001`.
- Retrying the same payment key returned the same attempt and order with `idempotent: true`; no accounting capture was claimed.
- `npm.cmd run build` and the local `/student-portal` route/asset smoke checks passed after the frontend build.

## Remaining P6.2 work

- Profile refinement and real authentication/OTP/session integration.
- Real authentication/OTP/session integration and permission tests.
