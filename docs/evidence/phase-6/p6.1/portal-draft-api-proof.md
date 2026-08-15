# P6.1 Portal Draft API Proof

Date: 2026-08-13

## Scope

The guardian portal now persists its autosave draft through the custom app's public portal API. The API uses the existing admissions model and does not expose the stored resume token.

## Verification

Against `http://p21.localhost:8000`:

1. Published form context returned `AAF-P41-PILOT-2026.1`.
2. A guardian payload created draft `AAD-AAF-P41-PILOT-2026.1-00166`.
3. Resume returned the same draft and the persisted payload.
4. A second save with the same resume token returned the same draft and updated the payload without creating a duplicate.
5. The response returned the token only to the caller; the DocType stores `resume_token_hash`.
6. `npm.cmd run build` passed and emitted the deterministic portal assets.

## Remaining P6.1 gate work

- Real document upload and scan-status integration.
- Payment initiation and safe callback/retry integration using the existing fake provider contracts.
- Frappe UI dependency integration where the portal requires shared Frappe components.
- Browser/mobile visual and interaction verification. The configured browser connection was unavailable during this run.
- Hindi terminology review and guardian usability acceptance.
