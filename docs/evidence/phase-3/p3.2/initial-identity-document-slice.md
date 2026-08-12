# P3.2 Initial Identity and Document Slice

Date: 2026-08-12

Site: `p21.localhost`

## Scope Started

This evidence records the first executable slice of `P3.2 - Student Identity and Documents`.

Implemented in `university_erp`:

- `Student Identity Profile`
- `Communication Consent`
- `Student Status Change`
- `Student Category History`
- `Student Correction Request`
- `Duplicate Candidate`
- `Student Document Type`
- `Document Requirement Matrix`
- `Student Document`
- `Document Rejection Reason`
- `Document Verification`
- proof harness at `university_erp.domain.student_identity.identity_document_proof.run_identity_document_proof`

The custom records wrap standard Education `Student Applicant`, `Student`, `Student Category` and `Guardian` foundations instead of replacing upstream DocTypes.

## Verification Commands

```powershell
docker compose exec backend bash -lc "cd /home/frappe/frappe-bench && env/bin/python -m compileall -q apps/university_erp/university_erp/domain/student_identity apps/university_erp/university_erp/university_erp/doctype"
docker compose exec backend bench --site p21.localhost migrate
docker compose exec backend bench --site p21.localhost execute university_erp.domain.student_identity.identity_document_proof.run_identity_document_proof
```

The proof was run twice after migration to confirm repeatability.

## Proof Result

```json
{
  "doctype_count": 11,
  "permission_count": 22,
  "applicant": "EDU-APP-2026-00001",
  "identity_profile": "SIP-2026-00004",
  "candidate_profile": "SIP-2026-00005",
  "consent": "CC-SIP-2026-00004-00006",
  "status_change": "SSC-SIP-2026-00004-00007",
  "category_history": "SCH-SIP-2026-00004-00008",
  "correction_request": "SCR-SIP-2026-00004-00009",
  "duplicate_candidate": "DUP-SIP-2026-00004-00010",
  "document_type": "P32-BIRTH",
  "requirement": "P32-BIRTH-GEN",
  "rejection_reason": "P32-BLUR",
  "student_document": "SDOC-P32-BIRTH-00011",
  "verification": "DV-SDOC-P32-BIRTH-00011-00012",
  "document_status": "Verified",
  "validation_checks": {
    "blank_identity_rejected": true,
    "empty_consent_rejected": true,
    "self_duplicate_rejected": true,
    "scan_failed_without_reason_rejected": true
  },
  "audit_versions": 4
}
```

## Validation Covered

- Identity profiles require exactly one Student or Student Applicant link.
- Identity names, email and mobile values are normalized.
- Consent records require at least one allowed channel.
- Status and category history reject no-op changes.
- Correction requests become `Approved` on submit.
- Duplicate candidates are recorded without merging records and reject self-matches.
- Document requirements can be scoped to program/category.
- Student documents require Student or Student Applicant context.
- Scan-failed documents require a rejection reason.
- Document verification updates the linked student document.
- System Manager and Academics User permissions exist on the initial P3.2 DocTypes.
- Tracked identity records produce Frappe `Version` audit evidence when changed.

## Open P3.2 Work

This is not the P3.2 exit gate. Remaining work includes:

- student-side profile issuance and immutable enrollment identity;
- Guardian relationship workflow beyond standard Education guardian records;
- document replacement workflow and expiry handling;
- scan-result adapter integration with the fake ClamAV/R2 foundations;
- privacy masking/export controls;
- broader permission tests, negative role tests, browser/Desk checks and migration tests;
- dedupe review/merge request workflow without automatic merge.

## Status

`P3.2` is `In progress`. The initial identity/document slice is migrated and locally proven, but the full P3.2 completion gate has not passed.
