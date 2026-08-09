# Production Runbooks

## Common incident procedure

1. Acknowledge and assign incident commander, operations lead, domain lead and communications owner.
2. Record start time, affected sites/workflows, release, symptoms and correlation IDs.
3. Contain impact without destroying evidence or creating untracked data changes.
4. Diagnose through dashboards, structured logs, traces, queue/job state and reconciliation.
5. Recover using approved commands/workflows and verify business invariants.
6. Communicate status at severity-appropriate intervals.
7. Close only after monitoring and reconciliation remain stable.
8. Produce corrective actions for material incidents.

Never paste secrets or sensitive student/payment payloads into incident channels.

## Web/API error-rate or latency incident

- Confirm edge, load balancer, web replicas, database, Redis and provider dependencies.
- Compare with deployment/config annotations and isolate affected sites/routes.
- Scale stateless replicas only if saturation is proven; scaling does not fix lock/query/provider failures.
- Apply safe rate limits or temporarily disable expensive exports/bulk operations if approved.
- Verify recovery through user-visible SLI, not container health alone.

## Queue backlog or worker failure

- Identify queue, oldest age, failing job type, retry pattern and worker heartbeat.
- Pause a poison job/event class if it blocks progress; preserve payload identity for replay.
- Restore workers or scale based on throughput and downstream quotas.
- Do not bulk-requeue without proving idempotency and provider/accounting safety.
- Reconcile completed, failed, duplicated and dead-lettered business outcomes.

## Scheduler not running or running twice

- Check scheduler heartbeat, leader configuration, site enablement and recent deployment.
- Stop duplicate scheduler instances before replaying missed schedules.
- Determine the exact missed time window and job set.
- Replay idempotent jobs in bounded batches; manually review fines, offer expiry and financial jobs.
- Verify no duplicate assessments/notifications/accounting results.

## Payment webhook or reconciliation incident

- Preserve provider event/order/payment/settlement identities and signature result.
- Distinguish provider state, ERP operational payment state and ERPNext posting state.
- Continue acknowledging valid duplicate callbacks according to provider contract.
- Verify authoritative provider state through the approved adapter.
- Replay through idempotent processing; never mark success from browser redirect or manual field edit.
- Reconcile amount, currency, student/demand, Payment Entry, invoice and settlement before closure.

## Seat allocation or admission invariant incident

- Freeze affected offer acceptance/allocation commands, not unrelated reads.
- Capture seat matrix version, allocations, offers, cancellations and concurrent request IDs.
- Do not delete or overwrite published merit/allocation records.
- Determine authoritative capacity and impacted applicants with product/legal owner.
- Apply approved compensating workflow and communicate through controlled channels.
- Add a concurrency/regression test before re-enabling.

## Database saturation, lock or failover

- Confirm connection, CPU, memory, IOPS, lock waits, slow query and replication metrics.
- Stop or throttle known bulk/report workloads if safe.
- Do not kill transactions without identifying business impact.
- Follow managed failover or restore procedure; verify application connection behavior.
- Reconcile in-flight seat, payment, conversion and fee transactions after recovery.

## Private file or malware-control incident

- Revoke exposed URLs/access and quarantine affected objects.
- Disable unsafe upload/download path while preserving evidence.
- Identify access events, users, sites and scan state without redistributing content.
- Rotate credentials if storage access may be compromised.
- Rescan/revalidate and restore access only after security approval.

## Suspected credential or data exposure

- Activate security incident process and restrict access.
- Revoke sessions/tokens and rotate affected credentials/keys in dependency order.
- Preserve audit, edge, authentication, export and object-access evidence.
- Determine scope, data classes, actions and legal/contract notification obligations.
- Reconcile unauthorized changes and monitor recurrence.

## Bad deployment or migration

- Stop subsequent site batches and annotate the incident.
- Keep maintenance/consumer pause state consistent with the failure mode.
- Assess schema compatibility and whether new-version writes occurred.
- Choose forward-fix, compatible app rollback or approved restore.
- Run migration, permission, queue and financial reconciliation before traffic resumes.

