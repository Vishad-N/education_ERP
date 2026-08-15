# P6.1 Upload and Payment Retry Proof

Date: 2026-08-13

## Scope

The guardian portal now has server-side document quarantine/scan state and application-fee order creation with safe retries.

## Implementation

- `Admission Application Document` stores the draft link, private object key, checksum, file metadata, scan provider and scan state.
- `Admission Payment Attempt` stores the draft link, fixed pilot fee, provider order, status and unique retry key.
- `university_erp.api.portal.upload_application_document` validates PDF/JPG/PNG content, enforces a 5 MB limit, writes through the fake R2 contract, scans through fake ClamAV and records the result.
- `university_erp.api.portal.create_application_payment` creates a fake Razorpay order for INR 500 and returns the existing attempt for a duplicate idempotency key.
- `DocumentUpload.vue` and `App.vue` connect file selection and payment retry controls to these endpoints.

## Verification

Against `http://p21.localhost:8000` after `bench --site p21.localhost migrate`:

- First document upload returned `AADOC-AAD-AAF-P41-PILOT-2026.1-00166-00167` with `Scan Passed`.
- Retrying the same upload key returned the same document with `idempotent: true`.
- First payment attempt returned `APA-AAD-AAF-P41-PILOT-2026.1-00166-00168` and provider order `order_000001`.
- Retrying the same payment key returned the same attempt and provider order with `idempotent: true`.
- The first verified capture callback transitioned the attempt to `Paid` with provider payment `pay_000001`.
- Replaying the capture callback returned `idempotent: true` and did not create a second payment result.
- Payment status polling returned the persisted `Paid` state and provider payment ID.
- `npm.cmd run build` passed after the frontend integration.

## Remaining P6.1 gate work

- Browser/mobile visual verification, Hindi terminology review and guardian usability acceptance remain open.
