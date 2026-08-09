# Requirements Traceability

## Purpose

This file links each BRD capability to design ownership, implementation, verification, and acceptance evidence. It is updated continuously; it is not a one-time project artifact.

## Status model

`Clarification`, `Ready`, `In Progress`, `Implemented`, `Verified`, `Accepted`, or `Deferred`.

No requirement reaches `Ready` without measurable acceptance criteria. No requirement reaches `Verified` without test evidence. No Phase-1 requirement becomes `Deferred` without an approved change request.

## Coverage register

| Requirement IDs | Capability | Design owner | Primary specification | Minimum verification | Status |
|---|---|---|---|---|---|
| `BRD-US-001..010` | Institution hierarchy and governance | Institution | Database and security architecture | Hierarchy, history, lock, clone, permissions | Clarification |
| `BRD-US-011..020` | Academic session and calendar | Academic | Database architecture | Lifecycle, publish, copy, lock | Clarification |
| `BRD-US-021..030` | Programs and courses | Academic | Database architecture | Version, mapping, clone, deactivation | Clarification |
| `BRD-US-031..040` | CBCS and credit framework | Academic | Database architecture | Classification, baskets, credits, lock | Clarification |
| `BRD-US-041..050` | Intake and capacity | Academic/Admissions | System architecture | Concurrent capacity, approvals, utilization | Clarification |
| `BRD-US-051..058` | Reservation and category | Academic/Admissions | Security and database architecture | Effective rules, lock, propagation, audit | Clarification |
| `BRD-US-059..066` | NEP entry-exit rules | Academic | Database architecture | Version/effective date, lock, compliance | Clarification |
| `BRD-US-067..080` | Program governance and publishing | Academic | Engineering workflow | Approval, restore, publish, historical view | Clarification |
| `BRD-US-081..090` | Student identity and profile | Student Identity | Security and privacy | ID uniqueness, dedupe, critical edit audit | Clarification |
| `BRD-US-091..100` | Category, domicile, guardians, documents | Student Identity | Security and privacy | Eligibility/fee propagation, private upload | Clarification |
| `BRD-US-101..110` | Document and student status lifecycle | Student Identity | Security and database architecture | Scan/verify/reject, status transitions, audit | Clarification |
| `BRD-US-111..121` | Privacy and correction requests | Compliance/Identity | Security and privacy | Masking, access, correction approval, export | Clarification |
| `BRD-US-122..140` | Bulk, consent, login, retention | Identity/Compliance | Security and testing | Row validation, consent history, auth controls | Clarification |
| `BRD-US-141..150` | Application and eligibility | Admissions | API and database architecture | Form versions, explainable rules, override audit | Clarification |
| `BRD-US-151..155` | Application fee | Admissions/Fees | API and accounting ADR | Online/offline, receipt, duplicate, reconcile | Clarification |
| `BRD-US-156..160` | Merit processing | Admissions | System architecture | Determinism, tie-breakers, publish lock | Clarification |
| `BRD-US-161..169` | Offer, confirmation, conversion | Admissions/Identity | System architecture | Concurrent seat, cancellation, idempotent conversion | Clarification |
| `BRD-US-170..185` | Tracking, controls, analytics, exports | Admissions/Reporting | Security and testing | Workflow, approval, permission-safe reports | Clarification |
| `BRD-US-186..200` | Notification engine | Notifications | API and integrations | Consent, trigger, retry, throttle, pause, delivery | Clarification |
| `BRD-ACA-001` | Timetable and clash detection | Academic | Database architecture | Class/faculty/room clash and override | Clarification |
| `BRD-ACA-002` | Faculty assignment and workload | Academic | Database architecture | Effective assignment and workload limits | Clarification |
| `BRD-ACA-003` | Student promotion | Academic/Identity | Data migration and testing | Bulk validation, resume, history | Clarification |
| `BRD-FEE-001..999` | Detailed fee backlog | Fees/Finance | Accounting ADR and database architecture | Calculation, posting, payment, refund, reconcile | Clarification |

## Story-level record template

Create one row per story when it enters refinement:

| ID | Acceptance criteria | Design/API | Implementation | Automated tests | Manual/UAT evidence | Owner | Status |
|---|---|---|---|---|---|---|---|
| `BRD-US-NNN` | Given/when/then with thresholds | Link | Link/commit | Test IDs | Evidence link | Name/role | Ready |

## Required fee story groups

Assign stable `BRD-FEE-###` IDs during Sprint 0 for fee policy/versioning, applicability, demand generation, invoice posting, installments, fines, online/offline payments, partial allocation, excess/credit, concession, scholarship, tax, receipts, refunds, reversals, cancellation, chargeback, settlement, bank reconciliation, write-off, security deposit, migration, dashboards, permissions, audit, and failure recovery.

## Acceptance evidence

Evidence must identify release, site/data set, test identity, result, reviewer, and timestamp. Screenshots alone are insufficient for financial reconciliation, concurrency, permission, security, backup, restore, or performance acceptance.

