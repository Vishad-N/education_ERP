# Capacity and Scale Plan

## Planning assumptions

These values are estimates until pilot measurements replace them.

| Metric | Per small institution | At 100 institutions |
|---|---:|---:|
| Active students | 600-800 | 60,000-80,000 |
| Guardians | 900-1,200 | 90,000-120,000 |
| Staff accounts | 40-60 | 4,000-6,000 |
| Annual applications | 70-120 | 7,000-12,000 |
| Normal concurrent users | 5-15 | 500-1,000 across pods |
| Peak concurrent users | 15-30 | 1,000-1,500 across pods |
| Initial private objects | 5-10 GB | 500 GB-1 TB |
| Five-year object storage | 20-40 GB | 2-4 TB before retention refinement |

The initial scope excludes high-volume daily attendance, examinations, LMS content and video. Add their workload before bringing them into scope.

## Pilot sizing

Phase 0 pilot planning values:

| Metric | Pilot planning value | Owner/source | Review trigger |
|---|---:|---|---|
| Active students | 600-800 | Product baseline for small-township high school | Replace with pilot institution count before migration |
| Guardians | 900-1,200 | 1.5 guardians per student planning factor | Replace after admission/user data review |
| Staff accounts | 40-60 | Product baseline | Replace after role matrix approval |
| Annual applications | 70-120 | Product baseline | Replace before admission-cycle load test |
| Normal concurrent users | 5-15 | Engineering planning assumption | Validate in local/staging load test |
| Peak concurrent users | 15-30 | Engineering planning assumption | Validate before go-live |
| Initial private object storage | 5-10 GB | Document upload planning assumption | Replace after document matrix approval |
| Annual SMS volume | 5,000-15,000 | Notification planning assumption | Replace after template/trigger approval |
| Annual email volume | 3,000-10,000 | Notification planning assumption | Replace after template/trigger approval |
| Annual online payment transactions | 100-300 | Finance/admission planning assumption | Replace after fee policy approval |

Recommended production pilot:

- Hostinger KVM 8 application VPS: reverse proxy, Frappe web, WebSocket, scheduler and workers.
- Hostinger KVM 8 database VPS: MariaDB and Redis/Valkey with strict firewall and encrypted private connectivity.
- Cloudflare edge and private R2 storage.
- Off-host database/PITR and object backup.
- Central monitoring and alerting.

This is a baseline to load-test, not a guaranteed capacity statement.

## Pod model for growth

Target approximately 20-25 institution sites per measured production pod:

```text
Cloudflare edge
    -> Pod routing
        -> 2 application VPSs
        -> worker pools
        -> database primary
        -> optional tested replica/failover candidate
        -> Redis/Valkey
        -> independently recoverable site backups
```

Expected rollout topology:

| Wave | Institutions | Minimum topology evidence |
|---|---:|---|
| Pilot | 1 | Separate app/database nodes and restore proof |
| Wave 1 | 5 | Automated onboarding, quotas and support workflow |
| Wave 2 | 20 | First pod load and upgrade rehearsal |
| Wave 3 | 50 | Multiple pods and centralized fleet monitoring |
| Wave 4 | 100 | Four or more measured pods and DR review |

## Capacity triggers

Scale or rebalance before:

- sustained application or database CPU above 60-70 percent during normal load;
- memory pressure, swap use or repeated process restarts;
- disk, database or object quota above 70 percent;
- P95/P99 latency violates SLO under expected peak;
- payment or notification queue age breaches its SLO;
- database lock waits or connections approach safe limits;
- backup duration, restore duration or migration batch exceeds its window;
- one institution creates measurable noisy-neighbor impact;
- tested headroom falls below 40 percent before an admission/payment peak.

## Load-test profiles

At minimum test:

- guardian login, draft/save/resume and final application submission;
- concurrent final-seat acceptance;
- Razorpay webhook bursts with duplicates and out-of-order delivery;
- fee generation and large exports while normal Desk traffic continues;
- document upload/scan queues;
- SMS/email throttling and provider outage;
- multi-site migration batches and scheduler workload;
- pod-node loss and worker restart recovery.

Record dataset, image digest, site count, virtual users, traffic mix, P50/P95/P99, errors, queue age, database metrics, locks, resource use and recovery time.

## Cost-control mechanisms

- Per-site storage, export, notification and API quotas.
- Institution-level SMS/email usage reports and budgets.
- Async exports with expiration and R2 lifecycle policy.
- Archive policies for obsolete generated files.
- Scale pods from measured demand rather than provisioning all 100 institutions on day one.
