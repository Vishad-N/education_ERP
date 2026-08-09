# Production Readiness Checklist

Every checked item links to evidence, owner, release/image digest and approval date. `Not applicable` requires a recorded reason and approver.

## Product and requirements

- [ ] All Phase-1 requirements are Ready/Implemented/Verified/Accepted as required by release scope.
- [ ] Missing fee and academic stories have approved acceptance criteria.
- [ ] End-to-end UAT is signed by institution owners.
- [ ] Phase-2 capabilities are not accidentally exposed as supported.
- [ ] Training, support contacts and known limitations are approved.

## Architecture and data

- [ ] ADRs and system/database/deployment specifications match implementation.
- [ ] No untracked upstream core changes exist.
- [ ] Exact app SHAs, image digest, SBOM and schema version are recorded.
- [ ] Tenancy/site isolation and campus/record permissions pass.
- [ ] Concurrency invariants for seats, payments and conversion pass.
- [ ] Migration trial and final reconciliation are signed.

## Finance

- [ ] Fee policy, rounding, tax, chart-of-accounts and posting design are approved.
- [ ] Demand/invoice/payment/refund/outstanding totals reconcile to ERPNext GL.
- [ ] Duplicate, timeout, mismatch, partial, refund, reversal and settlement cases pass.
- [ ] Offline payment controls, receipts and maker-checker approvals pass.
- [ ] Finance dashboards/reports match approved source documents.

## Security and privacy

- [ ] Threat model, data classification and permission matrix are current.
- [ ] MFA and least privilege are active for privileged users/services.
- [ ] Private file, malware scan, masking, export and consent controls pass.
- [ ] Secrets are production-specific, managed and rotated.
- [ ] Scans/penetration test have no unaccepted critical/high findings.
- [ ] Incident contacts, evidence preservation and notification path are active.

## Reliability and performance

- [ ] SLOs, workload profile and capacity/headroom are validated.
- [ ] Load, contention, queue backlog and provider-outage tests pass.
- [ ] Health/readiness, autoscale/manual scale and scheduler leader controls pass.
- [ ] Backup, PITR prerequisites and monthly restore evidence are current.
- [ ] RPO/RTO and DR exercise pass.

## Delivery and operations

- [ ] CI/CD gates, signature/provenance and environment promotion pass.
- [ ] Production-sized migration/deployment rehearsal fits the window.
- [ ] Dashboards, alerts, logs, traces and audit retention are active.
- [ ] Runbooks are tested and on-call/escalation is staffed.
- [ ] Rollback/forward-fix criteria and release communication are approved.
- [ ] Hypercare staffing, duration, exit criteria and handoff are defined.

## Go-live approval

| Role | Name | Decision | Date | Evidence/conditions |
|---|---|---|---|---|
| Product owner | TBD | Pending | TBD | |
| Institution owner | TBD | Pending | TBD | |
| Finance owner | TBD | Pending | TBD | |
| Security/privacy owner | TBD | Pending | TBD | |
| Engineering owner | TBD | Pending | TBD | |
| Operations owner | TBD | Pending | TBD | |

