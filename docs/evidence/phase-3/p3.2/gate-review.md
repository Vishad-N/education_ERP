# P3.2 Gate Review

Date: 2026-08-12

## Decision

`P3.2 - Student Identity and Documents` is not complete yet. Do not move to Phase 4.

The current P3.2 evidence proves the initial identity/document slice only:

- applicant-linked identity profile;
- consent, status history, category history and correction request;
- duplicate candidate without automatic merge;
- document type, requirement matrix, uploaded document and verification records;
- basic validation, permission and audit evidence.

## Missing From The P3.2 Exit Gate

The P3.2 exit gate requires student identity and document workflows to pass privacy, permission and audit tests. The following are still open:

- student-side profile issuance and immutable enrollment identity;
- guardian relationship workflow beyond standard Education guardian records;
- document replacement workflow;
- document expiry handling;
- scan-result adapter integration with fake ClamAV/R2 foundations;
- privacy masking and export controls;
- broader positive and negative role-permission tests;
- browser/Desk checks;
- migration tests;
- dedupe review and merge-request workflow without automatic merge.

## Current Roadmap State

The next executable step remains `P3.2 - Student Identity and Documents`.

`P3.2` can be marked complete only after the missing workflow, privacy, permission, audit and failure-path evidence is added.
