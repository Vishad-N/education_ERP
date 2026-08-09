# Project Implementation Plan

> Status: Active execution plan
> Current completion: 0 percent functional implementation
> Current phase: Phase 1 - local platform bootstrap
> Current next step: P1.2 - generate `university_erp` through Bench
> Last updated: 2026-08-09

This file controls execution order for agents and engineers building the Education ERP from the pulled Frappe repositories into a production-ready product.

Do not skip phase gates. After every completed or blocked step, update this file with status, evidence links, owner, date and next executable step.

## Execution Rules

- Work only on the `Current next step` unless the step explicitly allows parallel work.
- Record every material decision as an ADR under `docs/adr/`.
- Keep upstream source clean. Do not edit `frappe`, `erpnext`, `education`, `crm` or `frappe_docker` directly for product customizations.
- Build product behavior in the custom app `university_erp`.
- Every feature must link to BRD IDs in `docs/requirements/traceability.md`.
- Purchases, production credentials, DNS changes, real SMS/email/payment traffic and production deployment require explicit user approval.
- No phase is complete without tests, permissions, audit behavior, failure-path coverage and evidence.

## Repository Baseline

The project expects the following repositories or source inputs to be available locally or referenced by pinned immutable SHAs:

| Source           | Purpose                              | Required state                                     |
| ---------------- | ------------------------------------ | -------------------------------------------------- |
| `frappe`         | Framework runtime                    | Exact v16 tag/SHA pinned                           |
| `erpnext`        | Accounting and core ERP              | Exact v16 tag/SHA pinned                           |
| `education`      | Education domain foundation          | Exact v16-compatible tag/SHA pinned                |
| `crm`            | Enquiry and counsellor CRM           | Exact v16-compatible tag/SHA pinned                |
| `frappe_docker`  | Docker build and runtime composition | Exact commit SHA pinned                            |
| `university_erp` | Custom project app                   | Generated through Bench and committed in this repo |

If these repositories were pulled outside this workspace, record their absolute paths and chosen SHAs in the phase evidence before bootstrapping.

## Phase Overview

| Phase    | Goal                                                                           | Exit result                                                      |
| -------- | ------------------------------------------------------------------------------ | ---------------------------------------------------------------- |
| Phase 0  | Confirm decisions, verify pulled repos, pin versions and freeze pilot scope    | Reproducible technical baseline is approved                      |
| Phase 1  | Bootstrap local Frappe stack and generate `university_erp`                     | Fresh site installs all apps successfully                        |
| Phase 2  | Prove compatibility, accounting, tenancy, storage and notification foundations | Architecture risks are proven with small working slices          |
| Phase 3  | Build core masters and student identity                                        | Pilot institution can configure academic and student foundations |
| Phase 4  | Build admissions, merit, seats and conversion                                  | Enquiry-to-student flow works end to end                         |
| Phase 5  | Build fees, payments, receipts and reconciliation                              | Fee-to-ERPNext-GL journey works end to end                       |
| Phase 6  | Build bilingual portal and low-literacy UX                                     | Guardian/applicant can complete core tasks on mobile             |
| Phase 7  | Harden security, privacy, testing and migration                                | Release candidate passes quality gates                           |
| Phase 8  | Prepare Hostinger production deployment                                        | Production-like staging is deployable, monitored and restorable  |
| Phase 9  | Pilot go-live and hypercare                                                    | First institution runs controlled production pilot               |
| Phase 10 | Scale to multi-institution rollout                                             | Repeatable pods, onboarding and operations are proven            |

## Phase 0 - Repository and Decision Bootstrap

### P0.1 - Verify Pulled Repositories and Pin Versions

Status: Complete

Owner: Engineering

Actions:

1. Locate local paths for `frappe`, `erpnext`, `education`, `crm` and `frappe_docker`.
2. Confirm each repository is on a v16-compatible branch/tag.
3. Record exact commit SHAs and remote URLs.
4. Create or update `apps.json` with pinned sources.
5. Create or update `docker/Dockerfile` to build from the pinned app manifest.
6. Record the result in `docs/adr/` or a release manifest.

Evidence required:

- `git rev-parse HEAD` for every upstream repository.
- `git remote -v` sanitized where needed.
- `apps.json` committed with immutable refs.
- `frappe_docker` SHA recorded.

Exit gate:

- No moving branches such as `main`, `develop` or `version-16` are used without a pinned SHA.

### P0.2 - Confirm Commercial and Compliance Ownership

Status: Complete

Owner: Product/Founder

Decisions to record:

- Razorpay: per-institution merchant accounts or approved platform settlement model.
- MSG91/DLT: platform-owned or institution-owned Principal Entity, headers and templates.
- Email: per-institution Hostinger SMTP/domain identity or shared sending domain.
- Named owners for finance, privacy/security, institution approvals and operations.

Evidence required:

- ADRs for payment, SMS/DLT and email ownership.
- Owners listed in production readiness documents.

Exit gate:

- No real payment, SMS, SMTP or production credential work starts before this is approved.

### P0.3 - Freeze Pilot Scope and Workload

Status: Complete

Owner: Product + Pilot Institution

Actions:

1. Confirm first pilot institution profile, classes, admissions workflow, fee types and documents.
2. Confirm expected users, students, applicants, files, payment volume and peak usage.
3. Confirm English/Hindi copy expectations and low-literacy UX constraints.
4. Identify missing high-school requirements such as attendance, exams, report cards or transport if needed for pilot acceptance.

Evidence required:

- Updated `docs/requirements/traceability.md`.
- Pilot workload added to capacity documents.
- Scope exclusions clearly documented.

Exit gate:

- Phase 1 engineering may begin when P0.1 is complete. Production integration work waits for P0.2.

## Phase 1 - Local Platform Bootstrap

### P1.1 - Create Product Repository Structure

Status: Complete

Actions:

- Add `.env.example`, `.editorconfig`, `.gitignore`, `apps.json`, `compose.yaml`, `docker/`, `scripts/`, `tests/`, `infrastructure/` and `apps/` if missing.
- Keep generated source and runtime data separate.
- Add safe local fake-provider configuration.

Exit gate:

- A new developer can identify all required setup files from this repo.

### P1.2 - Generate `university_erp` Through Bench

Status: Not started

Actions:

- Use Bench to create the Frappe app named `university_erp`.
- Commit generated app files including `hooks.py`, `modules.txt`, `patches.txt`, `pyproject.toml` and package metadata.
- Add domain package placeholders only when first implementation needs them.

Exit gate:

- `university_erp` installs on a clean site without manual patching.

### P1.3 - Bring Up Local Development Site

Status: Not started

Actions:

- Build the pinned Docker image.
- Start MariaDB, Redis/Valkey, Frappe web, socket, scheduler and workers.
- Create `erp.localhost` or equivalent dev site.
- Install apps in order: ERPNext, Education, CRM, `university_erp`.
- Add smoke tests for login, app installation, migrations and scheduler.

Exit gate:

- Fresh local bootstrap is repeatable from documented commands.

## Phase 2 - Compatibility and Foundation Proofs

### P2.1 - App Compatibility Proof

Status: Not started

Actions:

- Run fresh install and migration tests with pinned SHAs.
- Validate basic Desk navigation for ERPNext, Education, CRM and custom app.
- Document known fit-gap items against the BRD.

Exit gate:

- No unresolved install or migration blocker remains.

### P2.2 - Accounting Proof

Status: Not started

Actions:

- Prove education fee demand to ERPNext invoice/payment entry/GL flow.
- Test partial payment, duplicate payment prevention, reversal and refund pattern.
- Record accounting ADR.

Exit gate:

- Finance path has a tested pattern before full fee development.

### P2.3 - Integration Foundation Proofs

Status: Not started

Actions:

- Implement fake adapters for Razorpay, MSG91, SMTP, R2 and ClamAV.
- Define provider ports and idempotency rules.
- Add webhook signature and replay validation structure.

Exit gate:

- Domain code can test provider success, failure, timeout and duplicate events without real providers.

## Phase 3 - Masters and Student Identity

### P3.1 - Institution and Academic Masters

Status: Not started

Build:

- Institution hierarchy and structure versioning.
- Academic sessions, calendars, programs, grades/classes, sections and subjects.
- Curriculum/version rules, intake, reservation and lock workflows.
- Timetable and faculty assignment foundations as required by pilot scope.

Exit gate:

- Pilot academic structure can be configured with permission and audit tests.

### P3.2 - Student Identity and Documents

Status: Not started

Build:

- Student/applicant identity extensions.
- Guardian model, consent, category history, status history and corrections.
- Document requirement matrix, upload metadata, scan status, verification and replacement.
- Dedupe candidate detection without automatic merge.

Exit gate:

- Student identity and document workflows pass privacy, permission and audit tests.

## Phase 4 - Admissions

### P4.1 - CRM Handoff and Application Forms

Status: Not started

Build:

- Frappe CRM lead/deal stages.
- Idempotent CRM-to-application handoff.
- Versioned dynamic application forms.
- Save/resume application workflow.

Exit gate:

- Enquiry can become one controlled application without duplicate records.

### P4.2 - Eligibility, Merit, Seats and Offers

Status: Not started

Build:

- Eligibility rule sets and explainable results.
- Merit configurations, immutable merit runs and tie-breakers.
- Seat matrix, allocation rounds, waitlist movement and offer expiry.
- Concurrency protection for final seat acceptance.

Exit gate:

- Concurrent acceptance cannot oversubscribe intake.

### P4.3 - Admission Confirmation and Conversion

Status: Not started

Build:

- Offer response and admission confirmation workflow.
- Required fee/document gates.
- Idempotent applicant-to-student conversion.
- Enrollment identity generation.

Exit gate:

- Repeated conversion returns the existing student instead of creating duplicates.

## Phase 5 - Fees, Payments and Reconciliation

### P5.1 - Fee Policy and Demand Generation

Status: Not started

Build:

- Fee groups, fee codes, policy versions, applicability and installment schedules.
- Demand generation linked to ERPNext accounting documents.
- Concession, scholarship, fine and waiver workflows.

Exit gate:

- Generated demands reconcile to expected fee policy totals.

### P5.2 - Payment Collection and Receipts

Status: Not started

Build:

- Razorpay sandbox adapter.
- Offline payment workflow with maker-checker approval.
- Receipts, partial allocations and outstanding balances.
- Duplicate webhook and browser-callback safety.

Exit gate:

- One provider transaction creates at most one posted accounting result.

### P5.3 - Refunds, Settlement and GL Reconciliation

Status: Not started

Build:

- Refund request/approval/posting.
- Settlement imports and mismatch handling.
- Finance dashboards and reconciliation reports.

Exit gate:

- Fee, payment, refund, settlement and GL reports reconcile.

## Phase 6 - Bilingual Low-Literacy Portal

### P6.1 - Applicant and Guardian PWA

Status: Not started

Build:

- Vue 3, TypeScript, Frappe UI and Vite portal.
- Mobile-first registration, application, upload, payment and status tracking.
- English/Hindi switch on primary screens.
- Large touch targets, plain labels, icons with text and low-bandwidth states.

Exit gate:

- Guardian can complete the pilot application flow on a mobile device with minimal staff help.

### P6.2 - Student and Guardian Portal

Status: Not started

Build:

- Fee dues, receipts, documents, profile, notices and language preference.
- Safe retry behavior for uploads and payments.

Exit gate:

- Student/guardian can view dues, pay, download receipt and check status.

## Phase 7 - Quality, Security and Migration

### P7.1 - Test Suite and CI

Status: Not started

Build:

- Unit, integration, permission, migration, API contract, E2E and smoke tests.
- CI workflow for install, migration, tests, lint, secret scan, image build and vulnerability scan.

Exit gate:

- CI blocks broken install, failed migration, permission regressions and obvious secret leakage.

### P7.2 - Security and Privacy Hardening

Status: Not started

Build:

- Role matrix, MFA policy, private file access tests, export controls and audit events.
- Sensitive identifier masking and retention controls.
- Webhook validation and correlation IDs.

Exit gate:

- No unaccepted critical/high security findings remain.

### P7.3 - Migration and UAT

Status: Not started

Build:

- Migration templates and trial-load scripts.
- Count, reference and finance reconciliation reports.
- UAT scripts for pilot users.

Exit gate:

- UAT, migration trial and reconciliation are signed.

## Phase 8 - Hostinger Production Preparation

### P8.1 - Infrastructure and Deployment Automation

Status: Not started

Build:

- Hostinger VPS deployment scripts for app and database nodes.
- Cloudflare DNS/TLS/WAF baseline.
- Cloudflare R2 private bucket configuration.
- MariaDB backup/PITR and restore automation.
- Prometheus, Grafana, Loki and Uptime Kuma monitoring.

Exit gate:

- Production-like staging deploys from an immutable image and restores successfully.

### P8.2 - Release and Operations Readiness

Status: Not started

Build:

- Runbooks, alert rules, rollback/forward-fix criteria and hypercare plan.
- Release manifest with app SHAs, image digest, schema version and SBOM.

Exit gate:

- Production readiness checklist is signed by required owners.

## Phase 9 - Pilot Go-Live

### P9.1 - Controlled Pilot Launch

Status: Not started

Actions:

- Provision pilot site and integrations using approved credentials.
- Load approved master data and migration data.
- Run smoke tests, payment tests, notification tests and restore checks.
- Open access in controlled batches.

Exit gate:

- Pilot operations run without unresolved Severity 1/2 defects.

### P9.2 - Hypercare and Stabilization

Status: Not started

Actions:

- Monitor daily admissions, payments, notifications, errors, queue age and support issues.
- Fix defects through reviewed releases.
- Update docs, training and runbooks from real pilot findings.

Exit gate:

- Pilot owner signs acceptance and rollout readiness decision.

## Phase 10 - Multi-Institution Scale

### P10.1 - Fleet Provisioning

Status: Not started

Build:

- Site provisioning automation.
- Per-site quotas, backup state, integration health and schema drift inventory.
- Repeatable institution onboarding checklist.

Exit gate:

- New institution site can be provisioned, tested and backed up repeatably.

### P10.2 - Pod Scaling

Status: Not started

Build:

- 20 to 25-site pod model on measured capacity.
- Central observability, backup verification and incident process.
- Staggered upgrades and migration windows.

Exit gate:

- Rollout can progress toward 100 institutions without shared-database tenancy risk.

## Current Execution State

Current next step: P1.2 - generate `university_erp` through Bench.

Blocked by:

- Production credentials and live provider setup remain blocked until explicit user approval at the relevant later phase.
- Named individual go-live owners remain pending before production readiness, but Phase 0 role ownership is recorded.

Allowed parallel work:

- Clean up local repository structure for Phase 1.
- Prepare local-only fake provider interfaces.

Not allowed yet:

- Real Razorpay, MSG91, Hostinger SMTP, Cloudflare R2 or production DNS setup.
- Production deployment.
- Unpinned upstream app/image builds.

## Execution Log

| Date       | Step         | Status   | Evidence                                                                                                      | Notes                                                                                                                           |
| ---------- | ------------ | -------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| 2026-08-09 | Plan created | Complete | `PROJECT_IMPLEMENTATION_PLAN.md`                                                                              | Initial local execution plan added after Frappe repositories were reported as pulled.                                           |
| 2026-08-09 | P0.1         | Complete | `docs/releases/p0-source-baseline.md`, `apps.json`, `docker/Dockerfile`, `.env.example`, `compose.yaml`       | Upstream source paths, remotes, SHAs, Docker build refs and local cleanup state recorded.                                       |
| 2026-08-09 | P0.2         | Complete | `docs/adr/0012-institution-owned-provider-accounts.md`, `docs/operations/production-readiness-checklist.md`   | Institution-owned provider account model approved for Phase 0 baseline; real credentials still require explicit later approval. |
| 2026-08-09 | P0.3         | Complete | `docs/requirements/pilot-scope.md`, `docs/architecture/capacity-plan.md`, `docs/requirements/traceability.md` | Pilot scope, deferrals, bilingual UX baseline and workload assumptions recorded.                                                |
| 2026-08-09 | P1.1         | Complete | `docs/evidence/phase-1/p1.1/repository-structure-baseline.md`, `.gitignore`, `.env.example`, `compose.yaml`   | Product repository structure, source/runtime separation, and fake-provider local defaults verified.                             |
