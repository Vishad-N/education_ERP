# Project Execution Roadmap

This file is the execution state machine for building the University ERP from documentation-only repository to production rollout. Every human or AI agent must read `AGENTS.md`, this file, and the linked specification for the current step before making changes.

## Current execution state

| Field | Value |
|---|---|
| Current phase | Phase 0 - decisions and pilot definition |
| Last completed step | None |
| Next executable step | `S0.1` Confirm unresolved commercial and compliance ownership |
| Current release target | Production-ready pilot for one township high school |
| Current repository state | Pre-bootstrap scaffold exists; exact pins, generated app, CI, tests, integrations, and production infrastructure are incomplete |
| Last updated | 2026-08-02; synchronized with the production documentation baseline |

Update this table whenever a step is completed or blocked. Do not mark a phase complete until its exit gate passes.

## Status convention

Use exactly one status for every step:

- `PENDING`: prerequisites are incomplete.
- `READY`: prerequisites are complete and work may begin.
- `IN_PROGRESS`: an owner is actively working on it.
- `BLOCKED`: progress requires a named decision, credential, approval, or external state change.
- `DONE`: artifacts and verification evidence satisfy the completion gate.

## Agent execution protocol

1. Select the `Next executable step` from the current-state table.
2. Confirm every prerequisite and read the linked specifications.
3. Change only that step and explicitly listed parallel work.
4. Preserve user changes and avoid unrelated refactors.
5. Add implementation, automated tests, documentation, and evidence together.
6. Run the step's verification commands/checks.
7. Record evidence under `docs/evidence/<release>/<step-id>/` when that directory becomes necessary.
8. Change the step to `DONE` only after its completion gate passes.
9. Update the current-state table to the next eligible step.
10. Stop at any approval boundary. Never purchase services, expose credentials, change production DNS, migrate real data, send real messages, collect real payments, or deploy production without explicit user authorization.

If a prerequisite is missing, mark the step `BLOCKED`, name the exact missing input, and continue only with independent work that is explicitly safe to parallelize.

## Confirmed product and platform decisions

| Decision | Baseline |
|---|---|
| Hosting | Hostinger self-managed VPS |
| Edge and DNS | Cloudflare |
| File/object storage | Cloudflare R2 through private S3-compatible access |
| Payments | Razorpay initially |
| SMS | MSG91 recommended, pending sender/DLT ownership decision |
| Email | Hostinger Business Email SMTP initially |
| Languages | English and Hindi initially |
| Tenancy | One Frappe site and database per independently governed institution |
| Initial scale target | 100 institutions through controlled rollout |
| Pilot | One small-township high school |
| UX priority | Guardian-first, mobile-first, extremely simple for low digital literacy |
| Backend | Python 3.14, Frappe v16, ERPNext v16, Education v16, CRM v1.x, MariaDB, Redis/Valkey |
| Frontend | Frappe Desk for staff; Vue 3, TypeScript, Frappe UI and Vite for public portal |
| Deployment | Pinned immutable Docker image based on official `frappe_docker` |

Read `docs/current-implementation-status.md` before execution. The presence of a folder, placeholder file, Docker Compose service, or document does not satisfy a roadmap completion gate; only the listed artifact and verification evidence does.

## Approval boundaries

Explicit user approval is required before:

- buying or resizing Hostinger VPS plans;
- creating or changing production Cloudflare DNS, WAF, R2, or access tokens;
- creating production Razorpay, MSG91, DLT, or SMTP credentials;
- sending messages to real recipients;
- processing real payments or refunds;
- importing identifiable student/applicant data;
- production cutover, rollback, restore, or deletion;
- changing approved accounting, retention, Aadhaar, consent, or legal policy.

Credentials must be supplied through approved secret/environment mechanisms, never committed to Git or pasted into documentation.

---

## Phase 0 - Decisions and pilot definition

### `S0.1` Confirm commercial and compliance ownership

- Status: `READY`
- Prerequisites: None
- Read: `AGENTS.md`, `docs/security/security-and-privacy.md`, ADR-0005
- Actions:
  - Decide whether every institution has its own Razorpay merchant account or whether an approved platform settlement model is required.
  - Decide whether each institution or the platform company owns DLT Principal Entity registration, sender headers, and templates.
  - Decide whether each institution receives independent Hostinger SMTP credentials/domain identity.
  - Name finance, privacy/security, and institutional approval owners.
- Artifacts: new ADRs or approved entries in `docs/requirements/traceability.md`
- Completion gate: ownership and settlement responsibility are unambiguous and approved.
- Next: `S0.2`

### `S0.2` Establish workload and capacity assumptions

- Status: `PENDING`
- Prerequisites: `S0.1`
- Actions:
  - Record pilot students, guardians, staff, annual applicants, documents, peak concurrent users, messages, email, and payment volumes.
  - Record planning values for 5, 20, 50, and 100 institutions.
  - Define storage growth, database growth, queue throughput, and rollout triggers.
- Artifacts: `docs/architecture/capacity-plan.md` and load-test profiles
- Completion gate: capacity assumptions have an owner, source, safety margin, and review date.
- Next: `S0.3`

### `S0.3` Freeze pilot scope and acceptance criteria

- Status: `PENDING`
- Prerequisites: `S0.1`
- Actions:
  - Define the pilot's exact institution, academic, admissions, fee, notification, document, reporting, and migration scope.
  - Record explicitly deferred school features such as attendance and examinations.
  - Convert missing fee, timetable, faculty, promotion, document, and school-specific requirements into stable IDs.
  - Define English/Hindi terminology and acceptance owners.
- Artifacts: updated traceability matrix and pilot acceptance specification
- Completion gate: every pilot capability is testable and every deferred item is explicit.
- Next: `G0`

### `G0` Decision gate

- Status: `PENDING`
- Pass when: `S0.1`, `S0.2`, and `S0.3` are `DONE`.
- Next: `S1.1`

---

## Phase 1 - Executable repository and open-source stack

### `S1.1` Create repository foundations

- Status: `PENDING`
- Prerequisites: `G0`
- Actions:
  - Create `.gitignore`, `.editorconfig`, `.env.example`, `apps.json`, `compose.yaml`, Docker files, scripts, CI folders, and test folders according to `docs/architecture/repository-structure.md`.
  - Pin all source repositories by exact tag/SHA.
  - Add secret scanning and pre-commit checks.
- Completion gate: repository structure matches documentation and contains no secrets.
- Next: `S1.2`

### `S1.2` Build the local container platform

- Status: `PENDING`
- Prerequisites: `S1.1`
- Read: `docs/development/local-development.md`
- Actions:
  - Build the custom `frappe_docker` image.
  - Start MariaDB, Redis/Valkey, backend, frontend, WebSocket, scheduler, and workers.
  - Install Frappe, ERPNext, Education, and CRM using pinned versions.
- Completion gate: the stack starts reproducibly on a clean machine and health checks pass.
- Next: `S1.3`

### `S1.3` Create `university_erp`

- Status: `PENDING`
- Prerequisites: `S1.2`
- Actions:
  - Generate the Frappe custom app and domain module skeleton.
  - Install it on a development site.
  - Add app metadata, hooks, versioning, test base, and module ownership.
- Completion gate: fresh site installation and migration succeed with no upstream modifications.
- Next: `S1.4`

### `S1.4` Establish CI and supply-chain controls

- Status: `PENDING`
- Prerequisites: `S1.3`
- Read: `docs/operations/ci-cd.md`
- Actions:
  - Add formatting, lint, unit, integration, migration, secret, dependency, and container scans.
  - Build an immutable image and record app SHAs and SBOM.
- Completion gate: pull-request and release pipelines pass from a clean checkout.
- Next: `S1.5`

### `S1.5` Create deterministic synthetic data

- Status: `PENDING`
- Prerequisites: `S1.3`
- Actions:
  - Seed a fictional high school, roles, grades/classes/sections, guardians, students, fee structures, applicants, and provider outcomes.
  - Ensure all sample identities are visibly synthetic.
- Completion gate: seed is repeatable and safe for tests/screenshots.
- Next: `G1`

### `G1` Platform gate

- Status: `PENDING`
- Pass when: clean bootstrap, custom app installation, CI, image build, and seed creation pass.
- Next: `S2.1`

---

## Phase 2 - Compatibility and risk proofs

### `S2.1` Prove standard-app extension

- Status: `PENDING`
- Prerequisites: `G1`
- Actions: extend representative Student and Program behavior through hooks/classes without core edits.
- Gate: extension, permission, migration, and upgrade tests pass.
- Next: `S2.2`

### `S2.2` Prove accounting flow

- Status: `PENDING`
- Prerequisites: `S2.1`, approved accounting ownership
- Actions: fee demand -> Sales Invoice -> Razorpay sandbox order -> verified webhook -> Payment Entry -> GL reconciliation.
- Gate: duplicate/out-of-order webhook and refund tests cannot duplicate or corrupt accounting.
- Next: `S2.3`

### `S2.3` Prove Cloudflare R2 file flow

- Status: `PENDING`
- Prerequisites: `S2.1`, non-production R2 credentials
- Actions: private upload, signature/MIME/size checks, quarantine, malware scan, authorized signed download, deletion/version test.
- Gate: unauthorized and unscanned access fails; audit trail is complete.
- Next: `S2.4`

### `S2.4` Prove bilingual portal integration

- Status: `PENDING`
- Prerequisites: `S2.1`
- Actions: Vue/TypeScript/Frappe UI form with English/Hindi switch, autosave, resume, validation, and versioned API submission.
- Gate: mobile, permission, session, accessibility, and network-retry tests pass.
- Next: `S2.5`

### `S2.5` Prove transactional notifications

- Status: `PENDING`
- Prerequisites: `S2.1`
- Actions: domain transaction -> outbox -> worker -> fake/approved MSG91 and SMTP adapters -> delivery status.
- Gate: rollback sends nothing; duplicate event sends once; retries and dead-letter state are observable.
- Next: `G2`

### `G2` Compatibility gate

- Status: `PENDING`
- Pass when: all five proofs pass and architecture changes are recorded in ADRs.
- Next: `S3.1`

---

## Phase 3 - Low-literacy UX and design system

### `S3.1` Research pilot users

- Status: `PENDING`
- Prerequisites: `G0`
- Actions: observe/interview 8-12 guardians and staff; document devices, literacy, language, network, payment, and assistance needs.
- Gate: personas and top failure risks are evidence-based.
- Next: `S3.2`

### `S3.2` Build and test the bilingual prototype

- Status: `PENDING`
- Prerequisites: `S3.1`, may run parallel with Phase 2
- Actions: prototype registration, application, document upload, payment status, receipt, and help flows.
- Gate: at least 80% of representative users complete primary tasks without direct instruction; no data loss or payment misunderstanding.
- Next: `S3.3`

### `S3.3` Freeze the portal design system

- Status: `PENDING`
- Prerequisites: `S3.2`
- Actions: define typography, spacing, components, form patterns, simple English/Hindi content, error messages, loading/offline states, and accessibility rules.
- Gate: product, UX, Hindi reviewer, and accessibility review approve.
- Next: `G3`

### `G3` UX gate

- Status: `PENDING`
- Pass when: tested prototype and design system are approved.
- Next: `S4.1`

---

## Phase 4 - Domain, data, security, and integration contracts

### `S4.1` Finalize domain model and state machines

- Status: `PENDING`
- Prerequisites: `G0`, `G2`
- Actions: finalize DocTypes, ownership, relationships, versions, uniqueness, locks, transitions, indexes, and retention hooks.
- Gate: architecture/domain review passes; no ambiguous status or ownership remains.
- Next: `S4.2`

### `S4.2` Finalize role and permission matrix

- Status: `PENDING`
- Prerequisites: `S4.1`
- Actions: define site, institution/campus, role, record, field, workflow, report, export, file, and privileged-service access.
- Gate: positive and negative test cases exist for every role.
- Next: `S4.3`

### `S4.3` Finalize API, event, and provider contracts

- Status: `PENDING`
- Prerequisites: `S4.1`
- Actions: version APIs/events, define error/idempotency contracts, Razorpay/MSG91/SMTP/R2 adapters, rate limits, and reconciliation.
- Gate: contract tests and failure behavior are specified.
- Next: `S4.4`

### `S4.4` Threat model and privacy design

- Status: `PENDING`
- Prerequisites: `S4.1`, `S4.2`, `S4.3`
- Actions: map trust boundaries, data classes, threats, consent, audit, secrets, document security, and incident controls.
- Gate: no unmitigated critical/high design risk.
- Next: `G4`

### `G4` Design gate

- Status: `PENDING`
- Pass when: domain, permission, contract, threat, finance, and migration foundations are approved.
- Next: `S5.1`

---

## Phase 5 - Shared platform capabilities

Execute in this order unless a step explicitly permits parallel work.

| Step | Status | Capability | Prerequisite | Completion gate | Next |
|---|---|---|---|---|---|
| `S5.1` | PENDING | Audit events and correlation IDs | `G4` | Sensitive actions produce immutable, sanitized audit evidence | `S5.2` |
| `S5.2` | PENDING | Transactional outbox and idempotent jobs | `S5.1` | retry/duplicate/rollback tests pass | `S5.3` |
| `S5.3` | PENDING | Provider adapter framework | `S5.2` | fake R2/Razorpay/MSG91/SMTP adapters pass contracts | `S5.4` |
| `S5.4` | PENDING | Private file/quarantine/scan service | `S5.3` | authorization and malware failure tests pass | `S5.5` |
| `S5.5` | PENDING | Bilingual portal shell and auth | `G3`, `S5.1` | OTP/session, language, accessibility, mobile tests pass | `S5.6` |
| `S5.6` | PENDING | Bulk-job and export framework | `S5.2` | resumable row-level processing and private exports pass | `G5` |

### `G5` Shared-platform gate

- Status: `PENDING`
- Pass when: shared controls are reusable, tested, documented, and observable.
- Next: `S6.1`

---

## Phase 6 - Phase 1A masters and identity

| Step | Status | Capability | Required outcome | Next |
|---|---|---|---|---|
| `S6.1` | PENDING | Institution hierarchy | active/inactive history, reporting scope, locks, clone | `S6.2` |
| `S6.2` | PENDING | Academic calendar and offering | year/term, grade/program, class, section, publish/version | `S6.3` |
| `S6.3` | PENDING | Curriculum, timetable and capacity | subject, faculty, clash/workload, intake/reservation | `S6.4` |
| `S6.4` | PENDING | Applicant/student identity | IDs, guardians, dedupe, status, corrections, consent | `S6.5` |
| `S6.5` | PENDING | Fee masters | fee codes/groups, applicability, installments, accounting mapping | `G6` |

Every step requires unit, integration, permission, audit, migration, and report tests.

### `G6` Phase 1A gate

- Status: `PENDING`
- Pass when: the pilot institution can configure a complete academic offering, student identity, and fee policy without direct database changes.
- Next: `S7.1`

---

## Phase 7 - Phase 1B vertical business journey

| Step | Status | Capability | Required outcome | Next |
|---|---|---|---|---|
| `S7.1` | PENDING | Application portal | register, draft, save/resume, program choice, submit | `S7.2` |
| `S7.2` | PENDING | Eligibility and scrutiny | explainable rules, documents, controlled override | `S7.3` |
| `S7.3` | PENDING | Application fee | Razorpay/offline, receipt, duplicate safety, reconcile | `S7.4` |
| `S7.4` | PENDING | Merit and seat allocation | deterministic merit, capacity, waitlist, offer expiry | `S7.5` |
| `S7.5` | PENDING | Confirmation and conversion | acceptance/cancellation, one Student/enrollment | `S7.6` |
| `S7.6` | PENDING | Day-1 fees and payments | demand, invoice, installment, partial, fine, concession | `S7.7` |
| `S7.7` | PENDING | Refund and reconciliation | reversal, refund, settlement, bank/GL reconciliation | `S7.8` |
| `S7.8` | PENDING | Notifications and dashboards | consent, SMS/email, retries, reports, exports | `G7` |

### `G7` Functional gate

- Status: `PENDING`
- Pass when: the complete application-to-student-to-fee-to-GL journey passes automated tests and product/finance demonstration.
- Next: `S8.1`

---

## Phase 8 - Quality, migration, and production hardening

| Step | Status | Work | Completion gate | Next |
|---|---|---|---|---|
| `S8.1` | PENDING | Full regression and browser E2E | all critical journeys and both languages pass | `S8.2` |
| `S8.2` | PENDING | Accessibility and low-bandwidth testing | approved usability/performance budgets pass | `S8.3` |
| `S8.3` | PENDING | Concurrency and performance | seat/payment/idempotency and SLO load profile pass | `S8.4` |
| `S8.4` | PENDING | Security and penetration testing | no unaccepted critical/high findings | `S8.5` |
| `S8.5` | PENDING | Migration rehearsal | counts, references, documents, fees and GL reconcile | `S8.6` |
| `S8.6` | PENDING | Backup/restore and DR exercise | RPO 15 minutes and RTO 2 hours demonstrated | `G8` |

### `G8` Release-candidate gate

- Status: `PENDING`
- Pass when: quality, security, migration, reconciliation, backup, restore, and operations evidence is approved.
- Next: `S9.1`

---

## Phase 9 - Hostinger production platform

### `S9.1` Provision pilot infrastructure

- Status: `PENDING`
- Prerequisites: `G8`, explicit purchase approval
- Actions: provision separate application and database Hostinger VPSs, private encrypted networking, firewall, SSH, time sync, and least privilege.
- Gate: hardened baseline and network tests pass.
- Next: `S9.2`

### `S9.2` Configure Cloudflare and R2

- Status: `PENDING`
- Prerequisites: `S9.1`, explicit Cloudflare approval
- Actions: DNS/TLS/WAF/rate limits, private per-site R2 bucket/credentials, lifecycle, CORS, backup bucket.
- Gate: public edge and private-file tests pass; `r2.dev` is not used for production.
- Next: `S9.3`

### `S9.3` Deploy observability and backups

- Status: `PENDING`
- Prerequisites: `S9.1`
- Actions: Prometheus, Grafana, Loki, Uptime Kuma, alerts, MariaDB backups/PITR, R2 backup/versioning, restore automation.
- Gate: alerts fire and restore evidence is current.
- Next: `S9.4`

### `S9.4` Configure production integrations

- Status: `PENDING`
- Prerequisites: `S9.2`, approved production credentials
- Actions: Razorpay webhook/signing, MSG91/DLT, Hostinger SMTP/SPF/DKIM/DMARC, R2, credential rotation and test recipients.
- Gate: controlled production-mode tests pass without uncontrolled real messages/payments.
- Next: `G9`

### `G9` Infrastructure gate

- Status: `PENDING`
- Pass when: production platform is hardened, observable, recoverable, and integration-ready.
- Next: `S10.1`

---

## Phase 10 - Pilot migration, UAT, and launch

| Step | Status | Work | Completion gate | Next |
|---|---|---|---|---|
| `S10.1` | PENDING | Pilot data mapping and cleansing | approved mappings, rejects, ownership, privacy | `S10.2` |
| `S10.2` | PENDING | Production-sized trial migration | duration and reconciliation fit cutover | `S10.3` |
| `S10.3` | PENDING | Staff training and bilingual UAT | signed institution, product, finance acceptance | `S10.4` |
| `S10.4` | PENDING | Production readiness review | checklist approved by all owners | `S10.5` |
| `S10.5` | PENDING | Final cutover and smoke tests | explicit deployment approval; all smoke/reconcile checks pass | `S10.6` |
| `S10.6` | PENDING | Two-week hypercare | stable SLOs, backups, support, finance and incident review | `G10` |

### `G10` Pilot acceptance gate

- Status: `PENDING`
- Pass when: pilot is stable, accepted, financially reconciled, recoverable, and handed to operations.
- Next: `S11.1`

---

## Phase 11 - Controlled rollout to 100 institutions

Never advance a wave only because the calendar says so. Advance after capacity, support, backup, upgrade, finance, and incident gates pass.

| Step | Status | Target | Required gate | Next |
|---|---|---:|---|---|
| `S11.1` | PENDING | 5 institutions | pilot lessons closed; onboarding automation proven | `S11.2` |
| `S11.2` | PENDING | 20 institutions | first production pod capacity and upgrade test pass | `S11.3` |
| `S11.3` | PENDING | 50 institutions | multiple pods, fleet inventory, quotas and support scale pass | `S11.4` |
| `S11.4` | PENDING | 100 institutions | pod isolation, DR, security, finance and operations review pass | `G11` |

Target pod size is approximately 20-25 institution sites, adjusted by measured workload. Do not place all 100 institutions on one VPS or one database server.

### `G11` Scale acceptance gate

- Status: `PENDING`
- Pass when: 100-institution operations meet SLO, isolation, reconciliation, backup, support, security, and upgrade requirements.

---

## Global Definition of Done

No step is `DONE` unless:

- linked requirements and acceptance criteria are satisfied;
- business, permission, audit, failure, migration, and security behavior is tested;
- financial changes reconcile to ERPNext General Ledger;
- API/event/schema compatibility and deployment impact are documented;
- logs and metrics are useful and contain no secrets/unnecessary PII;
- changed documentation and operational runbooks are accurate;
- required specialist and user approvals are recorded;
- unresolved risks have an owner and formal acceptance.

## Execution log

Append concise entries after completed or blocked steps:

| Date | Step | Result | Evidence | Next step |
|---|---|---|---|---|
| 2026-08-02 | Roadmap created | Execution has not started | This document | `S0.1` |
| 2026-08-02 | Documentation synchronized | Hostinger/R2/Razorpay/messaging/UX/capacity baseline recorded; implementation remains unstarted | `docs/README.md`, ADR-0007 through ADR-0011 | `S0.1` |
