# Production Deployment

Use the [Hostinger production platform](hostinger-production-platform.md) for the concrete self-managed VPS topology. The repository's local Compose file is not a production topology and must never be promoted directly to a public Hostinger host.

## Preconditions

- Release candidate digest, signature, SBOM and app SHA manifest are approved.
- UAT, finance reconciliation, security, migration, performance and restore gates pass.
- Target sites, deployment order, maintenance requirement, owners and communication are recorded.
- Current backups and site encryption keys are verified recoverable.
- Dashboards, alerts, incident channel and on-call coverage are active.

## Provisioning baseline

Provision network, load balancer/WAF, container runtime, MariaDB, Redis/Valkey, object storage, secret management, registry access, logs/metrics and backups through reviewed infrastructure code. Validate private networking, encryption, IAM, quotas, DNS/TLS and time synchronization before site creation.

## Site onboarding

1. Allocate site name, database/user, storage prefix, keys and backup policy.
2. Create the site through automation.
3. Install pinned applications in the tested order.
4. Apply institution-safe baseline configuration and roles.
5. Configure separate provider credentials and callback URLs.
6. Load approved masters/migration batches.
7. Run permission, accounting, messaging, file and backup smoke tests.
8. Register the site in fleet inventory and monitoring.

## Standard deployment procedure

1. Confirm release/change ticket and operator roles.
2. Freeze affected configuration/data imports and capture baseline metrics.
3. Verify backup and restore prerequisites.
4. Pull the approved digest to runtime nodes.
5. Enter maintenance mode if the migration is not backward-compatible.
6. Pause affected schedulers/consumers where required.
7. Run preflight and schema migrations by controlled site batch.
8. Deploy web, realtime, workers and scheduler with health/readiness checks.
9. Resume consumers/scheduler and exit maintenance mode.
10. Run technical and business smoke tests.
11. Reconcile queue, payment, fee/accounting and migration totals.
12. Observe the release for the defined soak period before closing.

## Smoke tests

- Anonymous/public and authenticated portal reachability.
- Staff login, role/campus scoping and a permission denial.
- Application draft/save and representative submission in safe test mode.
- Background job execution and scheduler heartbeat.
- Private file upload/access policy and scan integration.
- Payment sandbox/fake verification and idempotent webhook path.
- ERPNext accounting posting in approved non-live test context.
- SMS/email capture/test recipient path.
- Metrics, logs, traces, alerts and backup job visibility.

Do not create uncontrolled live financial or applicant records for smoke testing.

## Failed deployment decision

Stop and assess when migration fails, error rate/latency exceeds threshold, queue age grows without recovery, permission isolation fails, reconciliation differs, or data integrity is uncertain. Choose:

- complete/repair the forward migration;
- roll application services back when schema-compatible;
- restore to the approved point only with incident command, business impact and data-loss decision.

Record all commands/actions, times, actors and validation results.

## Cutover for first production launch

- Approve final migration delta and legacy-system freeze.
- Export, checksum, load and reconcile final data.
- Switch provider callbacks and verified DNS/TLS.
- Enable production schedulers, notifications and payment modes deliberately.
- Run role-based business validation with institution owners.
- Publish support contacts and begin hypercare.
- Monitor admission, payment, queue, database and error dashboards continuously during the agreed window.

## Hypercare exit

Exit after stable SLOs, no unresolved critical/high incidents, financial/seat/student reconciliation, successful backups, support handoff, known-issue acceptance and operations owner approval.
