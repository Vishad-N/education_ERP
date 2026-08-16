# Hypercare Plan

This is the staging-to-pilot hypercare plan. It does not start production support hours.

## Window

| Field | Staging value | Pilot value |
|---|---|---|
| Duration | While P8 staging is the live target | 14 days after first real-data go-live |
| Hours | Best-effort by the current operator | Named on-call before first applicant traffic |
| Exit | P8.2 artifacts accepted and next phase opened | Pilot owner signs P9.2 |

Human UAT, real payments, real SMS/email, and production MFA remain outside this window.

## Watch list

Check at least once per working day:

- `GET /api/method/university_erp.api.health.live` and `.ready`
- Railway replica count: `web` = 1, combined worker = 1, MariaDB = 1, Redis = 1
- Combined-service logs for repeated job failures
- Disk use on the MariaDB volume
- Newest backup/restore evidence age

Use `deploy/monitoring/uptime-probes.example.yaml` and `deploy/monitoring/alert-rules.example.yaml` until an external monitor is approved.

## Severity

| Severity | Meaning | Response |
|---|---|---|
| 1 | Site down, data loss, seat oversubscription, duplicate posting | Page operator, freeze writes, follow runbooks |
| 2 | Ready failing, worker down, backup stale | Same day fix or documented workaround |
| 3 | Cosmetic, deferred UAT, missing translation | Track for the next release |

## Exit criteria

Leave staging hypercare when:

- Health probes stay green for 24 hours after the last P8 change
- Isolated restore evidence exists
- Release manifest and rollback criteria are recorded
- Remaining production items are listed as Phase 9 blockers, not silent gaps

Leave pilot hypercare only after the P9.2 owner signature.
