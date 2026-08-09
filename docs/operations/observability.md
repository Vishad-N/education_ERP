# Observability

## Objectives

Operators must detect customer impact, identify the affected site/workflow, correlate requests and jobs, reconcile critical business flows, and recover within SLOs without exposing PII.

## Telemetry standards

- Structured logs in UTC with event time, level, service, release/image, environment, site-safe identifier, correlation/request ID, job/event ID, operation and safe error code.
- Metrics use bounded-cardinality labels; never label with student/application IDs, emails, mobile numbers or raw URLs.
- Distributed traces cover web requests, domain commands, queues and approved provider calls where supported.
- Audit events are separate from diagnostic logs and follow stricter mutation/access controls.

## Golden signals

| Area | Signals |
|---|---|
| Web/API | Rate, P50/P95/P99 latency, error/timeout, saturation, status/error code |
| Database | Connections, CPU, memory, IOPS, slow queries, lock waits, replication lag |
| Queues | Depth, oldest age, enqueue/complete/fail/retry, worker heartbeat |
| Scheduler | Heartbeat, missed jobs, duration, duplicate/overlap prevention |
| Payments | Callback rate, signature failure, duplicate, verify/post lag, mismatch, settlement variance |
| Admissions | Submit failures, eligibility errors, seat contention, conversion failures |
| Fees | Demand/post failures, GL variance, overdue job lag, refund/reconcile failures |
| Notifications | Outbox age, send rate, provider failures, throttle, retry/dead-letter |
| Files | Upload/scan failures, quarantine age, unauthorized access denial |
| Fleet | Site health, image/schema drift, backup age, storage/quota use |

## SLOs and error budgets

Initial targets are defined in system architecture. Implement service-level indicators from user-visible outcomes, not only container uptime. Track monthly error budget and require reliability work or release controls when burn thresholds are exceeded.

## Alert policy

Page on actionable urgent conditions:

- sustained availability/error-budget burn;
- payment verification/posting failure or reconciliation mismatch;
- seat oversubscription/data-integrity invariant breach;
- database unavailability, severe lock/connection saturation or replication failure;
- queue oldest age beyond workflow SLO with no recovery;
- scheduler heartbeat absent;
- backup/PITR failure or restore prerequisite loss;
- suspected unauthorized access, secret exposure or malware control bypass;
- fleet deployment/schema drift.

Create tickets rather than pages for trends without immediate user/data impact. Every alert has owner, severity, threshold, runbook, deduplication and test evidence.

## Dashboards

- Executive service health and SLO/error budget.
- Admission peak: portal/API, application states, eligibility, merit/seat contention.
- Finance: payment intake, posting lag, duplicate/mismatch, settlement and GL reconciliation.
- Async: queues, workers, retries, scheduler, outbox/dead-letter.
- Data: MariaDB performance, locks, replication and storage.
- Site fleet: release/schema, quota, backups and per-site health.
- Security: auth anomalies, permission denials, WAF, webhook signature failures, sensitive exports.

## Logging restrictions

Never log passwords, tokens, cookies, full payment payloads, Aadhaar, unmasked identity values, private file content, full application bodies or database dumps. Sanitize provider errors and headers. Log identifiers only when operationally necessary and access-controlled.

## Release observability

Annotate deployments, migrations, feature-flag changes and provider configuration changes. Compare pre/post release rates, latency, errors, queue age, locks and business reconciliation. Keep a defined soak window and automatic/owner-driven rollback criteria.

## Retention and access

Set log, metric, trace, audit and security-event retention from approved operations/security policy. Restrict production telemetry access, audit sensitive searches/exports, and ensure deletion/archival does not break incident or regulatory obligations.

