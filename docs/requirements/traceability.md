# Requirements Traceability

## Purpose

This file links each BRD capability to design ownership, implementation, verification, and acceptance evidence. It is updated continuously; it is not a one-time project artifact.

## Status model

`Clarification`, `Ready`, `In Progress`, `Implemented`, `Verified`, `Accepted`, or `Deferred`.

No requirement reaches `Ready` without measurable acceptance criteria. No requirement reaches `Verified` without test evidence. No Phase-1 requirement becomes `Deferred` without an approved change request.

## Coverage register

Phase 0 pilot scope baseline: [pilot-scope.md](pilot-scope.md).

P3.1 institution and academic master completion evidence: [completion.md](../evidence/phase-3/p3.1/completion.md).

P3.2 completion evidence: [completion.md](../evidence/phase-3/p3.2/completion.md).

P4.1 CRM handoff/application form evidence: [completion.md](../evidence/phase-4/p4.1/completion.md).

P4.2 eligibility/merit/seat evidence: [completion.md](../evidence/phase-4/p4.2/completion.md).

P4.3 admission confirmation/conversion evidence: [completion.md](../evidence/phase-4/p4.3/completion.md).

P5.1 fee policy/demand generation evidence: [completion.md](../evidence/phase-5/p5.1/completion.md).

P5.2 payment collection/receipt evidence: [completion.md](../evidence/phase-5/p5.2/completion.md).

P5.3 refund/settlement/GL reconciliation evidence: [completion.md](../evidence/phase-5/p5.3/completion.md).

P6.1 initial portal slice evidence: [initial-portal-slice.md](../evidence/phase-6/p6.1/initial-portal-slice.md).
P6.1 portal draft API evidence: [portal-draft-api-proof.md](../evidence/phase-6/p6.1/portal-draft-api-proof.md).
P6.1 upload/payment evidence: [upload-payment-integration-proof.md](../evidence/phase-6/p6.1/upload-payment-integration-proof.md).

P7.1 automated test and CI evidence: [completion.md](../evidence/phase-7/p7.1/completion.md).

P7.2 security and privacy evidence: [completion.md](../evidence/phase-7/p7.2/completion.md), [start.md](../evidence/phase-7/p7.2/start.md) and [role-matrix.md](../security/role-matrix.md).

P7.3 migration and UAT evidence: [completion.md](../evidence/phase-7/p7.3/completion.md), [reconciliation.md](../evidence/phase-7/p7.3/reconciliation.md), [migration templates](../operations/migration-templates/README.md) and [pilot UAT script](../quality/pilot-uat-script.md). Human execution/signatures are deferred in [human-testing-readme.md](../quality/human-testing-readme.md) and remain mandatory before production.

P8.1 infrastructure automation is in progress: [start.md](../evidence/phase-8/p8.1/start.md) and [ADR-0015](../adr/0015-portable-staging-runtime.md). Railway is the first staging target; Hostinger and AWS portability artifacts use the same immutable-image runtime contract.
P6.1 acceptance evidence: [acceptance-review.md](../evidence/phase-6/p6.1/acceptance-review.md).
P6.1 deferred human acceptance checklist: [human-testing-readme.md](../quality/human-testing-readme.md).
P6.2 initial student portal evidence: [initial-student-portal-slice.md](../evidence/phase-6/p6.2/initial-student-portal-slice.md).
P6.2 completion evidence: [completion.md](../evidence/phase-6/p6.2/completion.md).

| Requirement IDs | Capability | Design owner | Primary specification | Minimum verification | Status |
|---|---|---|---|---|---|
| `BRD-US-001..010` | Institution hierarchy and governance | Institution | Database architecture; P3.1 completion evidence | Hierarchy, history, lock, clone, permissions | Verified |
| `BRD-US-011..020` | Academic session and calendar | Academic | Database architecture; P3.1 completion evidence | Lifecycle, publish, copy, lock | Verified |
| `BRD-US-021..030` | Programs and courses | Academic | Database architecture; P3.1 completion evidence | Version, mapping, clone, deactivation | Verified |
| `BRD-US-031..040` | CBCS and credit framework | Academic | Database architecture; P3.1 completion evidence | Classification, baskets, credits, lock | Verified |
| `BRD-US-041..050` | Intake and capacity | Academic/Admissions | System architecture; P3.1 completion evidence | Concurrent capacity, approvals, utilization | Verified |
| `BRD-US-051..058` | Reservation and category | Academic/Admissions | Security and database architecture; P3.1 completion evidence | Effective rules, lock, propagation, audit | Verified |
| `BRD-US-059..066` | NEP entry-exit rules | Academic | Database architecture | Version/effective date, lock, compliance | Clarification |
| `BRD-US-067..080` | Program governance and publishing | Academic | Engineering workflow | Approval, restore, publish, historical view | Clarification |
| `BRD-US-081..090` | Student identity and profile | Student Identity | Security and privacy; P3.2 completion evidence | ID uniqueness, dedupe, critical edit audit | Verified |
| `BRD-US-091..100` | Category, domicile, guardians, documents | Student Identity | Security and privacy; P3.2 completion evidence | Eligibility/fee propagation, private upload | Verified |
| `BRD-US-101..110` | Document and student status lifecycle | Student Identity | Security and database architecture; P3.2 completion evidence | Scan/verify/reject, status transitions, audit | Verified |
| `BRD-US-111..121` | Privacy and correction requests | Compliance/Identity | Security and privacy; P3.2 completion evidence | Masking, access, correction approval, export | Verified |
| `BRD-US-122..140` | Bulk, consent, login, retention | Identity/Compliance | Security and testing | Row validation, consent history, auth controls | Clarification |
| `BRD-US-141..150` | Application and eligibility | Admissions | API and database architecture; P4.1 and P4.2 completion evidence | Form versions, explainable rules, override audit | Verified |
| `BRD-US-151..155` | Application fee | Admissions/Fees | API, accounting ADR and P5.2 completion evidence | Online/offline, receipt, duplicate, reconcile | In Progress |
| `BRD-US-156..160` | Merit processing | Admissions | System architecture; P4.2 completion evidence | Determinism, tie-breakers, publish lock | Verified |
| `BRD-US-161..169` | Offer, confirmation, conversion | Admissions/Identity | System architecture; P4.2 and P4.3 completion evidence | Concurrent seat, cancellation, idempotent conversion | Verified |
| `BRD-US-170..185` | Tracking, controls, analytics, exports | Admissions/Reporting | Security and testing | Workflow, approval, permission-safe reports | Clarification |
| `BRD-US-186..200` | Notification engine | Notifications | API and integrations | Consent, trigger, retry, throttle, pause, delivery | Clarification |
| `BRD-ACA-001` | Timetable and clash detection | Academic | Database architecture; P3.1 completion evidence | Class/faculty/room clash and override | Verified |
| `BRD-ACA-002` | Faculty assignment and workload | Academic | Database architecture; P3.1 completion evidence | Effective assignment and workload limits | Verified |
| `BRD-ACA-003` | Student promotion | Academic/Identity | Data migration and testing | Bulk validation, resume, history | Clarification |
| `BRD-FEE-001..999` | Detailed fee backlog | Fees/Finance | Accounting ADR, database architecture and P5.1/P5.2/P5.3 completion evidence | Calculation, posting, payment, refund, reconcile | In Progress |

## Story-level record template

Create one row per story when it enters refinement:

| ID | Acceptance criteria | Design/API | Implementation | Automated tests | Manual/UAT evidence | Owner | Status |
|---|---|---|---|---|---|---|---|
| `BRD-US-NNN` | Given/when/then with thresholds | Link | Link/commit | Test IDs | Evidence link | Name/role | Ready |

## Required fee story groups

Assign stable `BRD-FEE-###` IDs during Sprint 0 for fee policy/versioning, applicability, demand generation, invoice posting, installments, fines, online/offline payments, partial allocation, excess/credit, concession, scholarship, tax, receipts, refunds, reversals, cancellation, chargeback, settlement, bank reconciliation, write-off, security deposit, migration, dashboards, permissions, audit, and failure recovery.

## Acceptance evidence

Evidence must identify release, site/data set, test identity, result, reviewer, and timestamp. Screenshots alone are insufficient for financial reconciliation, concurrency, permission, security, backup, restore, or performance acceptance.
