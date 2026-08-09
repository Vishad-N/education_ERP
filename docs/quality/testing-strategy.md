# Testing Strategy

## Quality model

Tests prove business correctness, authorization, auditability, financial reconciliation, reliability and operability. A passing happy-path UI test is not sufficient.

The pilot release also requires usability evidence from representative low-literacy guardians in both English and Hindi. Test on low-cost Android devices, constrained bandwidth, interrupted sessions, large text settings, and assisted/offline-to-online school workflows.

## Test layers

| Layer | Scope | Typical owner |
|---|---|---|
| Pure unit | Eligibility, fee, merit, credit, reservation and transition policies | Domain engineers |
| DocType/service integration | Validation, permissions, transactions, hooks, accounting side effects | Domain engineers |
| API/contract | Auth, validation, errors, idempotency, provider contracts | API/integration engineers |
| Browser E2E | Applicant, staff, finance and student journeys | QA/product engineering |
| Migration | Fresh install, supported upgrades, data backfill and reconciliation | Domain/platform |
| Performance | Peak application, payment webhook, bulk jobs, reports | Performance/platform |
| Security | Permissions, tenant/site isolation, OWASP paths, files, secrets | Security/QA |
| Resilience | Retry, duplicate, timeout, worker loss, provider outage, restore | Platform/domain |

Performance and fleet tests must model the [capacity plan](../architecture/capacity-plan.md), including admission/payment peaks, noisy-neighbor behavior within a 20-25-site pod, and staged growth to 100 institutions.

## Critical scenario matrix

### Admissions

- Simultaneous acceptance for the final available seat cannot oversubscribe capacity.
- Merit rerun with identical inputs/rules produces identical output.
- Published merit is immutable and regeneration requires approval.
- Eligibility override records maker/checker, reason and before/after result.
- Repeated conversion returns the same Student/enrollment result.
- Waitlist movement, offer expiry, cancellation and vacancy preserve seat accounting.

### Fees and payments

- Fee applicability and rounding are deterministic for category/program/session/date.
- Demand and invoice totals reconcile by student, fee code, currency and period.
- Duplicate or out-of-order webhooks post at most one accounting result.
- Partial, installment, excess, refund, reversal and chargeback paths reconcile to GL.
- Scheduled fines are idempotent and respect approved grace/holiday rules.
- Settlement import identifies missing, duplicate and amount-mismatched transactions.

### Identity and documents

- Student IDs/enrollment numbers remain unique under concurrent creation.
- Dedupe suggests candidates but never silently merges.
- Critical edits and merge/correction workflows enforce approval and audit.
- Sensitive fields are masked and excluded from unauthorized lists, exports and logs.
- Private/quarantined files cannot be accessed before scan and authorization.

### Notifications

- Source transaction rollback produces no delivered notification.
- Consent, event disablement, throttling, pause, retry and dead-letter behavior work.
- Duplicate events do not send duplicate messages unless an approved resend is requested.

## Permission testing

Use positive and negative tests for every role across institution/campus, record ownership, field permission level, workflow state and portal/Desk/API channel. Include direct URL/API attempts, exports, reports, attachments and background jobs. Test privileged services separately and prove their scope is bounded.

## Performance profile

Finalize volumes in Sprint 0. Initial test scenarios must include:

- public application browsing and save/resume during admission peak;
- concurrent final submission and application-fee callbacks;
- final-seat acceptance contention;
- bulk merit and fee generation while normal Desk reads/writes continue;
- payment webhook bursts with duplicates;
- notification backlog and provider throttling;
- permission-safe report and export load;
- multi-site migration batches.

Pass criteria use SLOs, error rate, database/queue saturation, lock waits, memory, worker age and recovery time. Averages do not replace P95/P99 evidence.

## Security testing

- Static analysis, dependency/container scanning and secret scanning on every change.
- Authentication, session, CSRF, access-control and rate-limit tests.
- OWASP injection, XSS, SSRF, unsafe upload, path and deserialization checks.
- Webhook signature/replay and idempotency tests.
- Tenant/site and campus-scope isolation tests.
- Independent penetration test before production pilot and after material boundary changes.

## Test data

Use deterministic synthetic factories. Cover all roles, categories, campuses, lifecycle states, payment outcomes, dates, currencies and edge cases. Production data is prohibited unless formally approved and masked. Test clocks/timezones explicitly around deadlines and scheduled jobs.

## CI gates

- Pull request: lint/static, unit, changed-domain integration, migration smoke, secret/SAST scans.
- Main/release: full integration, API contracts, fresh install, supported upgrade, container scan.
- Release candidate: E2E, accessibility, performance, resilience, restore, security and UAT evidence.

Quarantined/flaky tests require an owner, issue, reason, risk approval and removal date; they cannot silently reduce a release gate.

## Evidence and defect policy

Record test release/image, site/data profile, scenario, result, timings, logs/metrics links and reviewer. Severity 1/2 defects block production. Lower severities require explicit product/risk acceptance and a target release.
