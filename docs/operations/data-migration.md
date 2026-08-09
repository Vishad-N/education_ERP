# Data Migration

## Scope

Migration covers institution/academic masters, applicants, students, guardians, categories, documents, admissions, opening fee balances, payments and reference mappings approved for the pilot. Historical depth and source systems remain `TBD` until discovery.

## Principles

- Preserve source identifiers and lineage.
- Transform through reviewed mappings, never ad hoc production edits.
- Use staged validation and idempotent/resumable loads.
- Reject/quarantine invalid rows with explicit reason; do not silently coerce.
- Reconcile business counts, relationships and financial totals before acceptance.
- Mask production-derived data in non-production environments.

## Migration stages

1. Inventory source systems, owners, formats, volumes, quality and extraction limits.
2. Define target ownership, field mapping, code crosswalks, defaults and transformations.
3. Profile duplicates, invalid dates/codes, missing references and financial discrepancies.
4. Cleanse at source where possible and approve residual transformation rules.
5. Load into staging tables/files with checksums and batch identity.
6. Validate schema, required fields, references, uniqueness, permissions and business rules.
7. Dry-run into an isolated site; produce row-level and aggregate results.
8. Reconcile and obtain domain/finance sign-off.
9. Repeat production-sized rehearsal and measure cutover duration.
10. Execute delta/final cutover, reconcile, archive evidence and enable operations.

## Load order

```text
Institution and accounting foundations
-> academic sessions, programs, curriculum, class/section, intake
-> users/roles and reference masters
-> applicants and student identities/guardians/categories
-> documents and verification metadata
-> applications, offers, admissions and enrollments
-> fee policies/demands and approved opening receivables
-> payments/allocations and reconciliation
-> audit/source cross-reference records
```

## Controls

- Each batch has immutable source checksum, mapping version, target site, started/completed time and operator.
- Use stable external/source IDs for idempotent upsert decisions.
- Duplicate identity resolution is reviewed; migration never silently merges.
- Sensitive files are private, scanned and access-controlled.
- Financial opening balances require finance-approved accounting entries and GL reconciliation.
- Migration users are temporary, least-privileged and disabled after cutover.

## Reconciliation

At minimum compare:

- record counts by source/type/status/session/program/category;
- rejected and transformed rows by reason;
- source-to-target key coverage and orphan references;
- student ID/enrollment uniqueness and duplicate candidates;
- application/admission/enrollment lifecycle totals;
- document count, checksum and scan/verification state;
- fee demand, invoice, payment, refund and outstanding totals;
- ERPNext control accounts and General Ledger balances;
- representative role/permission access.

## Cutover

Approve source freeze and delta window, final extraction/checksum, target maintenance state, provider callback handling, load order, reconciliation owners, rollback/forward-fix criteria and communication. Legacy systems become read-only according to approved retention rather than being immediately destroyed.

## Acceptance

Migration is accepted only with signed domain and finance reconciliation, documented exceptions, permission/privacy verification, measured duration within cutover window, and a recoverable pre-cutover backup.

