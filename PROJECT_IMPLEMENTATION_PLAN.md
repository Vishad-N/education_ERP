# Project Implementation Plan

> Status: Active execution plan
> Current completion: P7.2 complete for the local security/privacy gate; release-candidate security work remains deferred
> Current phase: Phase 7 - quality, security and migration
> Current next step: P8.1 - infrastructure and deployment automation
> Last updated: 2026-08-15

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

Status: Complete

Actions:

- Use Bench to create the Frappe app named `university_erp`.
- Commit generated app files including `hooks.py`, `modules.txt`, `patches.txt`, `pyproject.toml` and package metadata.
- Add domain package placeholders only when first implementation needs them.

Exit gate:

- `university_erp` installs on a clean site without manual patching.

### P1.3 - Bring Up Local Development Site

Status: Complete

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

Status: Complete

Actions:

- Run fresh install and migration tests with pinned SHAs.
- Validate basic Desk navigation for ERPNext, Education, CRM and custom app.
- Document known fit-gap items against the BRD.

Exit gate:

- No unresolved install or migration blocker remains.

### P2.2 - Accounting Proof

Status: Complete

Actions:

- Prove education fee demand to ERPNext invoice/payment entry/GL flow.
- Test partial payment, duplicate payment prevention, reversal and refund pattern.
- Record accounting ADR.

Exit gate:

- Finance path has a tested pattern before full fee development.

### P2.3 - Integration Foundation Proofs

Status: Complete

Actions:

- Implement fake adapters for Razorpay, MSG91, SMTP, R2 and ClamAV.
- Define provider ports and idempotency rules.
- Add webhook signature and replay validation structure.

Exit gate:

- Domain code can test provider success, failure, timeout and duplicate events without real providers.

## Phase 3 - Masters and Student Identity

### P3.1 - Institution and Academic Masters

Status: Complete

Build:

- Institution hierarchy and structure versioning.
- Academic sessions, calendars, programs, grades/classes, sections and subjects.
- Curriculum/version rules, intake, reservation and lock workflows.
- Timetable and faculty assignment foundations as required by pilot scope.

Exit gate:

- Pilot academic structure can be configured with permission and audit tests.

Progress:

- Custom DocTypes for institution hierarchy, structure versioning, academic session policy, academic calendar, program version/offering, class/section, curriculum, subject offering, intake/category capacity, faculty assignment and timetable foundations have been added under `university_erp`.
- `p21.localhost` migration passes with the completed P3.1 DocType set.
- A repeatable synthetic master-data proof creates and validates the full academic setup chain, permissions, timetable conflict rejection and audit Version evidence.
- Evidence: `docs/evidence/phase-3/p3.1/completion.md`.

### P3.2 - Student Identity and Documents

Status: Complete

Build:

- Student/applicant identity extensions.
- Guardian model, consent, category history, status history and corrections.
- Document requirement matrix, upload metadata, scan status, verification and replacement.
- Dedupe candidate detection without automatic merge.

Exit gate:

- Student identity and document workflows pass privacy, permission and audit tests.

Progress:

- Custom DocTypes for identity profile, guardian relationship, immutable identity issuance, consent, status/category history, correction request, duplicate candidate, document type, requirement matrix, student document, rejection reason, scan result, verification, replacement, expiry review, privacy export request and student data access audit have been added under `university_erp`.
- `p21.localhost` migration passes with the completed P3.2 DocType set.
- A repeatable synthetic proof creates and validates the applicant identity/document chain, guardian primary constraint, identity-number uniqueness, permissions, validation failures, scan, verification, replacement, expiry, privacy export and audit Version evidence.
- Evidence: `docs/evidence/phase-3/p3.2/initial-identity-document-slice.md`.
- Gate review: `docs/evidence/phase-3/p3.2/gate-review.md`.
- Completion evidence: `docs/evidence/phase-3/p3.2/completion.md`.

## Phase 4 - Admissions

### P4.1 - CRM Handoff and Application Forms

Status: Complete

Build:

- Frappe CRM lead/deal stages.
- Idempotent CRM-to-application handoff.
- Versioned dynamic application forms.
- Save/resume application workflow.

Exit gate:

- Enquiry can become one controlled application without duplicate records.

Progress:

- Custom DocTypes for versioned application forms, save/resume application drafts and CRM application handoff have been added under `university_erp`.
- `p21.localhost` migration passes with the P4.1 DocType set.
- A repeatable synthetic proof creates a CRM Lead, publishes a form version, saves/resumes a draft, creates one Student Applicant through an idempotent handoff, marks the CRM Lead converted and rejects invalid/duplicate handoff states.
- Evidence: `docs/evidence/phase-4/p4.1/completion.md`.

### P4.2 - Eligibility, Merit, Seats and Offers

Status: Complete

Build:

- Eligibility rule sets and explainable results.
- Merit configurations, immutable merit runs and tie-breakers.
- Seat matrix, allocation rounds, waitlist movement and offer expiry.
- Concurrency protection for final seat acceptance.

Exit gate:

- Concurrent acceptance cannot oversubscribe intake.

Progress:

- Custom DocTypes for eligibility rule sets/evaluations, merit configuration/run/entry, admission seat matrix, allocation round and seat offer have been added under `university_erp`.
- `p21.localhost` migration passes with the P4.2 DocType set.
- A repeatable synthetic proof validates explainable eligibility, published immutable merit, ranked entries, one accepted offer, one waitlisted offer, duplicate/invalid rejection and capacity protection that prevents a second accepted offer when the seat matrix is full.
- Evidence: `docs/evidence/phase-4/p4.2/completion.md`.

### P4.3 - Admission Confirmation and Conversion

Status: Complete

Build:

- Offer response and admission confirmation workflow.
- Required fee/document gates.
- Idempotent applicant-to-student conversion.
- Enrollment identity generation.

Exit gate:

- Repeated conversion returns the existing student instead of creating duplicates.

Progress:

- Custom DocTypes for admission confirmation and student conversion have been added under `university_erp`.
- `p21.localhost` migration passes with the P4.3 DocType set.
- A repeatable synthetic proof confirms an accepted seat offer after document/fee gates, converts the applicant into one standard Education Student, creates one submitted Program Enrollment, issues enrollment identity and rejects invalid or duplicate conversion paths.
- Evidence: `docs/evidence/phase-4/p4.3/completion.md`.

## Phase 5 - Fees, Payments and Reconciliation

### P5.1 - Fee Policy and Demand Generation

Status: Complete

Build:

- Fee groups, fee codes, policy versions, applicability and installment schedules.
- Demand generation linked to ERPNext accounting documents.
- Concession, scholarship, fine and waiver workflows.

Exit gate:

- Generated demands reconcile to expected fee policy totals.

Progress:

- Custom DocTypes for fee codes, fee policy versions, installments, student adjustments and student fee demands have been added under `university_erp`.
- A repeatable synthetic proof creates a published fee policy, approved concession/scholarship/fine/waiver adjustments, a submitted Education Fee Schedule Sales Invoice and a submitted Student Fee Demand.
- The generated demand reconciles to the published policy total and the submitted ERPNext Sales Invoice total.
- Invalid policy totals, negative adjustments, incorrect demand totals and invoice mismatch submissions are rejected.
- Evidence: `docs/evidence/phase-5/p5.1/completion.md`.

### P5.2 - Payment Collection and Receipts

Status: Complete

Build:

- Razorpay sandbox adapter.
- Offline payment workflow with maker-checker approval.
- Receipts, partial allocations and outstanding balances.
- Duplicate webhook and browser-callback safety.

Exit gate:

- One provider transaction creates at most one posted accounting result.

Progress:

- Custom DocTypes for provider events and student fee payment receipts have been added under `university_erp`.
- A repeatable synthetic proof creates a fake Razorpay order event, posts one online partial payment, replays duplicate webhook/browser callback paths and confirms the original ERPNext Payment Entry is reused.
- The proof also posts an approved offline receipt, rejects duplicate provider payment posting and rejects unapproved offline payment submission.
- Evidence: `docs/evidence/phase-5/p5.2/completion.md`.

### P5.3 - Refunds, Settlement and GL Reconciliation

Status: Complete

Build:

- Refund request/approval/posting.
- Settlement imports and mismatch handling.
- Finance dashboards and reconciliation reports.

Exit gate:

- Fee, payment, refund, settlement and GL reports reconcile.

Progress:

- Custom DocTypes for student fee refunds, payment settlement imports and fee general ledger reconciliation have been added under `university_erp`.
- A repeatable synthetic proof posts an approved partial refund through a submitted return Sales Invoice and ERPNext refund Payment Entry.
- The proof confirms refund idempotency, imports a reconciled fake-provider settlement, creates a balanced GL reconciliation record and rejects mismatch paths.
- Evidence: `docs/evidence/phase-5/p5.3/completion.md`.

## Phase 6 - Bilingual Low-Literacy Portal

### P6.1 - Applicant and Guardian PWA

Status: Complete with deferred human acceptance

Build:

- Vue 3, TypeScript, Frappe UI and Vite portal.
- Mobile-first registration, application, upload, payment and status tracking.
- English/Hindi switch on primary screens.
- Large touch targets, plain labels, icons with text and low-bandwidth states.

Exit gate:

- Guardian can complete the pilot application flow on a mobile device with minimal staff help.

Progress:

- Initial Vue 3, TypeScript and Vite portal scaffold has been added under `apps/university_erp/frontend`.
- A Frappe route at `/guardian-admission` serves the built portal assets from `university_erp/public/frontend`.
- The first mobile-first flow includes English/Hindi switching, local draft autosave, online/offline status, guardian registration, class selection, child details, document placeholders, payment safety text and status summary.
- Evidence: `docs/evidence/phase-6/p6.1/initial-portal-slice.md`.
- Portal autosave now persists and resumes an `Admission Application Draft` through a public API linked to a CRM Lead; the resume token is stored only as a hash. Evidence: `docs/evidence/phase-6/p6.1/portal-draft-api-proof.md`.
- Document uploads now have private quarantine metadata and fake ClamAV scan state; application-fee attempts now use durable retry keys, reuse the same fake Razorpay order and apply one idempotent capture callback. Evidence: `docs/evidence/phase-6/p6.1/upload-payment-integration-proof.md`.
- Final local flow validation blocks incomplete steps, prevents future-step skipping and passes route/asset smoke checks. Browser/mobile rendering and guardian usability acceptance are deferred to `docs/quality/human-testing-readme.md`. Evidence: `docs/evidence/phase-6/p6.1/acceptance-review.md`.

### P6.2 - Student and Guardian Portal

Status: Complete with deferred production integrations

Build:

- Fee dues, receipts, documents, profile, notices and language preference.
- Safe retry behavior for uploads and payments.

Progress:

- Added expiring, hashed `Student Portal Access` records and a scoped snapshot API for one student.
- Added the mobile-first English/Hindi `/student-portal` view for dues, receipts and documents.
- Added scoped receipt PDF download and published student/guardian notices.
- Added student-scoped, retry-safe payment order initiation for generated fee demands.
- Evidence: `docs/evidence/phase-6/p6.2/initial-student-portal-slice.md`.
- Added ERPNext payment capture/posting, duplicate callback idempotency, fake OTP verification and payment status polling. Evidence: `docs/evidence/phase-6/p6.2/completion.md`.

Exit gate:

- Student/guardian can view dues, pay, download receipt and check status.

## Phase 7 - Quality, Security and Migration

### P7.1 - Test Suite and CI

Status: Complete

Build:

- Unit, integration, permission, migration, API contract, E2E and smoke tests.
- CI workflow for install, migration, tests, lint, secret scan, image build and vulnerability scan.

Progress:

- Added portal API contract tests for token hashing, invalid-token rejection and scoped snapshot behavior.
- Added a Docker-backed local app-test runner for migration plus `bench run-tests --app university_erp`.
- Added the initial GitHub Actions workflow for repository checks, Compose validation, image build and app tests.
- Reconciled retained local MariaDB site-user host grants and passed `p21.localhost` migration.
- Passed 3 `university_erp` integration tests with 0 failures, repository checks, documentation lint and secret-pattern scan.
- Evidence: `docs/evidence/phase-7/p7.1/start.md`, `docs/evidence/phase-7/p7.1/completion.md`.

Exit gate:

- CI blocks broken install, failed migration, permission regressions and obvious secret leakage.

### P7.2 - Security and Privacy Hardening

Status: Complete

Build:

- Role matrix, MFA policy, private file access tests, export controls and audit events.
- Sensitive identifier masking and retention controls.
- Webhook validation and correlation IDs.

Progress:

- Added the baseline role matrix, identifier masking utility, webhook correlation IDs and private-object URL TTL tests.
- Added negative tests for webhook signature/replay failures and restricted file URL TTLs.
- Added export approval/privilege, retention expiry and audit correlation tests.
- Passed 8 custom-app tests with 0 failures plus repository, documentation and diff checks.
- Evidence: `docs/evidence/phase-7/p7.2/start.md`, `docs/evidence/phase-7/p7.2/completion.md`.

Exit gate:

- No unaccepted critical/high security findings remain.

### P7.3 - Migration and UAT

Status: Complete with deferred human UAT

Build:

- Migration templates and trial-load scripts.
- Count, reference and finance reconciliation reports.
- UAT scripts for pilot users.

Progress:

- Added no-write CSV trial-load validation for students, guardians and opening fee balances.
- Added synthetic migration templates with duplicate, reference and financial amount checks.
- Added role-based pilot UAT script covering academic, admissions, finance, identity, portal, security and reconciliation journeys.
- Synthetic templates validated successfully: 3 files, 1 row each, INR 1,000.00 opening balance, no errors.
- Added checksum-backed count, reference and finance reconciliation with no exceptions.
- Human UAT and production-sized rehearsal are recorded as mandatory pre-production checks.
- Evidence: `docs/evidence/phase-7/p7.3/start.md`, `docs/evidence/phase-7/p7.3/reconciliation.md`, `docs/evidence/phase-7/p7.3/completion.md`.

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

Current next step: P8.1 - infrastructure and deployment automation.

Blocked by:

- Production credentials and live provider setup remain blocked until explicit user approval at the relevant later phase.
- Named individual go-live owners remain pending before production readiness, but Phase 0 role ownership is recorded.

Allowed parallel work:

- Resolve the clean Docker image rebuild timeout recorded in P1.3 evidence.
- Prepare local-only fake provider interfaces required by P2.3.

Not allowed yet:

- Real Razorpay, MSG91, Hostinger SMTP, Cloudflare R2 or production DNS setup.
- Production deployment.
- Unpinned upstream app/image builds.

## Execution Log

| Date       | Step         | Status      | Evidence                                                                                                           | Notes                                                                                                                                                                                                                                                      |
| ---------- | ------------ | ----------- | ------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-08-09 | Plan created | Complete    | `PROJECT_IMPLEMENTATION_PLAN.md`                                                                                   | Initial local execution plan added after Frappe repositories were reported as pulled.                                                                                                                                                                      |
| 2026-08-09 | P0.1         | Complete    | `docs/releases/p0-source-baseline.md`, `apps.json`, `docker/Dockerfile`, `.env.example`, `compose.yaml`            | Upstream source paths, remotes, SHAs, Docker build refs and local cleanup state recorded.                                                                                                                                                                  |
| 2026-08-09 | P0.2         | Complete    | `docs/adr/0012-institution-owned-provider-accounts.md`, `docs/operations/production-readiness-checklist.md`        | Institution-owned provider account model approved for Phase 0 baseline; real credentials still require explicit later approval.                                                                                                                            |
| 2026-08-09 | P0.3         | Complete    | `docs/requirements/pilot-scope.md`, `docs/architecture/capacity-plan.md`, `docs/requirements/traceability.md`      | Pilot scope, deferrals, bilingual UX baseline and workload assumptions recorded.                                                                                                                                                                           |
| 2026-08-09 | P1.1         | Complete    | `docs/evidence/phase-1/p1.1/repository-structure-baseline.md`, `.gitignore`, `.env.example`, `compose.yaml`        | Product repository structure, source/runtime separation, and fake-provider local defaults verified.                                                                                                                                                        |
| 2026-08-09 | P1.2         | Complete    | `docs/evidence/phase-1/p1.2/university-erp-generation.md`, `apps/university_erp`                                   | Custom Frappe app files are present and installable without upstream source modification.                                                                                                                                                                  |
| 2026-08-09 | P1.3         | Complete    | `docs/evidence/phase-1/p1.3/local-bootstrap.md`, `compose.yaml`, `scripts/bootstrap/init-site.sh`                  | Local site installs all apps and responds on `erp.localhost:8000`; clean Docker image rebuild still needs follow-up confirmation.                                                                                                                          |
| 2026-08-10 | P2.1         | Complete    | `docs/evidence/phase-2/p2.1/app-compatibility-proof.md`                                                            | Fresh `p21.localhost` install, migration, app version, import, HTTP and authenticated Desk route checks passed for the pinned app set.                                                                                                                     |
| 2026-08-10 | P2.2         | Complete    | `docs/evidence/phase-2/p2.2/accounting-proof.md`, `docs/adr/0013-fee-demand-sales-invoice-accounting-pattern.md`   | Education fee schedule to ERPNext Sales Invoice, partial payments, duplicate event reuse, credit note refund and GL reconciliation proof passed locally.                                                                                                   |
| 2026-08-10 | P2.3         | Complete    | `docs/evidence/phase-2/p2.3/integration-foundation-proof.md`, `docs/adr/0014-fake-provider-contract-foundation.md` | Fake Razorpay, MSG91, SMTP, R2 and ClamAV adapters with idempotency, HMAC webhook verification, replay rejection, failure and timeout contract checks passed locally.                                                                                      |
| 2026-08-12 | P3.1         | In progress | `docs/evidence/phase-3/p3.1/initial-master-schema.md`                                                              | Initial institution and academic master DocTypes were added to `university_erp`, migrated on `p21.localhost`, and proven with a repeatable synthetic master-data chain. Full P3.1 permission, audit, curriculum, timetable and faculty scope remains open. |
| 2026-08-12 | P3.1         | Complete    | `docs/evidence/phase-3/p3.1/completion.md`                                                                         | Completed P3.1 DocTypes migrated on `p21.localhost`; repeatable proof passed for full academic setup chain, permissions, timetable conflict rejection and audit Version evidence.                                                                          |
| 2026-08-12 | P3.2         | In progress | `docs/evidence/phase-3/p3.2/initial-identity-document-slice.md`                                                    | Initial identity/document DocTypes migrated on `p21.localhost`; repeatable proof passed for applicant identity, consent, history, correction, dedupe candidate, document requirement, verification, permissions and audit evidence.                        |
| 2026-08-12 | P3.2         | In progress | `docs/evidence/phase-3/p3.2/gate-review.md`                                                                        | Gate review confirmed P3.2 is not complete yet; Phase 4 must not start until guardian workflow, immutable identity issuance, replacement/expiry, scan integration, privacy controls and broader permission/audit evidence are complete.                    |
| 2026-08-12 | P3.2         | Complete    | `docs/evidence/phase-3/p3.2/completion.md`                                                                         | Completed P3.2 DocTypes migrated on `p21.localhost`; repeatable proof passed for identity, guardian, issuance, consent, history, correction, dedupe, document scan, verification, replacement, expiry, privacy export, permissions and audit evidence.     |
| 2026-08-13 | P4.1         | Complete    | `docs/evidence/phase-4/p4.1/completion.md`                                                                         | Completed CRM handoff and versioned application form slice; repeatable proof passed for CRM Lead conversion, save/resume draft, one Student Applicant creation, duplicate prevention, permissions and audit evidence.                                      |
| 2026-08-13 | P4.2         | Complete    | `docs/evidence/phase-4/p4.2/completion.md`                                                                         | Completed eligibility, merit, seat matrix, allocation and offer slice; repeatable proof passed for explainable eligibility, immutable merit, ranking, waitlist, accepted-offer capacity protection, permissions and audit evidence.                        |
| 2026-08-13 | P4.3         | Complete    | `docs/evidence/phase-4/p4.3/completion.md`                                                                         | Completed admission confirmation and conversion slice; repeatable proof passed for accepted-offer gates, one Student, one Program Enrollment, enrollment identity issuance, duplicate rejection, permissions and audit evidence.                           |
| 2026-08-13 | P5.1         | Complete    | `docs/evidence/phase-5/p5.1/completion.md`                                                                         | Completed fee policy and demand generation slice; repeatable proof passed for policy math, installment, adjustments, submitted Sales Invoice, generated Student Fee Demand, idempotency, invalid-record rejection, permissions and audit evidence.         |
| 2026-08-13 | P5.2         | Complete    | `docs/evidence/phase-5/p5.2/completion.md`                                                                         | Completed payment collection and receipt slice; repeatable proof passed for fake provider order, online partial payment, duplicate webhook/browser callback reuse, offline approved payment, receipts, permissions and audit evidence.                     |
| 2026-08-13 | P5.3         | Complete    | `docs/evidence/phase-5/p5.3/completion.md`                                                                         | Completed refund, settlement and GL reconciliation slice; repeatable proof passed for approved partial refund, credit note, refund Payment Entry, settlement import, GL balance, mismatch rejection, permissions and audit evidence.                       |
