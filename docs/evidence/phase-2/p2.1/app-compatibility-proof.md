# P2.1 Evidence - App Compatibility Proof

Date: 2026-08-10

Status: Complete

## Scope

This proof verified that the pinned Frappe v16 app set can install, migrate and serve basic staff-facing routes in the local Docker Compose environment without upstream source edits.

## Runtime State

Docker Compose services were running:

- `backend`
- `mariadb`
- `redis-cache`
- `redis-queue`
- `redis-socketio`
- `websocket`
- `scheduler`
- `worker-short`
- `worker-long`

MariaDB reported healthy through Docker Compose.

Repository foundation verification passed:

```text
npm.cmd run check:repo
Repository foundation check passed.
```

## Existing Site Migration

The existing Phase 1 site migrated successfully:

```text
docker compose exec backend bench --site erp.localhost migrate
Queued rebuilding of search index for erp.localhost
```

HTTP smoke test:

```text
GET http://erp.localhost:8000
StatusCode=200
```

## Fresh Compatibility Site

A fresh local site named `p21.localhost` was created using the pinned app set. Apps were installed in this order:

1. `erpnext`
2. `payments`
3. `education`
4. `crm`
5. `university_erp`

Fresh-site migration completed:

```text
docker compose exec backend bench --site p21.localhost migrate
Queued rebuilding of search index for p21.localhost
```

Installed apps on `p21.localhost`:

```text
frappe         16.19.0 HEAD
erpnext        16.22.0 HEAD
payments       0.0.1   HEAD
education      16.0.1  HEAD
crm            1.72.0  HEAD
university_erp 0.0.0   UNVERSIONED
```

Running app source SHAs in the bench:

```text
frappe     ba18090b141740e75d52aa97bfc525ff2f831f6c
erpnext    054b20a2ae1bdea44694cca72d17412945171cab
payments   cca07d9f9392e2ea0e521c5975151db9e4b6c321
education  1c29e646bf943c2a5f696cb81cb48c8a072cbebc
crm        bf1b7f07ac01b6ac435f25db7ccef6b52807720e
```

`university_erp` is installed from the local workspace and imported successfully:

```text
import university_erp
university_erp.__version__ == 0.0.0
```

HTTP smoke test:

```text
GET http://p21.localhost:8000
StatusCode=200
```

Authenticated Desk navigation smoke test after Administrator login:

```text
Login      200
Desk       200
Education  200
Accounting 200
CRM        200
```

Checked routes:

- `http://p21.localhost:8000/app`
- `http://p21.localhost:8000/app/education`
- `http://p21.localhost:8000/app/accounting`
- `http://p21.localhost:8000/crm`

## BRD Fit-Gap Summary

| Area | Base app fit | Gap requiring `university_erp` work |
|---|---|---|
| Institution hierarchy | Frappe and ERPNext provide company, address, roles and permissions foundations. | BRD needs university/campus/college/department hierarchy, structure versioning, lock rules and reporting descendants. |
| Academic masters | Education provides basic academic structures such as programs, courses and student lifecycle foundations. | BRD needs program versions, offerings, class/section model, CBCS/credits, NEP rules, intake/reservation, timetable clash detection and faculty workload controls. |
| CRM enquiry | CRM installs and serves its app route. | BRD needs controlled enquiry-to-application handoff, counsellor workflow mapping, idempotency and permission-safe reporting. |
| Student identity | Education provides student and applicant foundations. | BRD needs immutable identities, guardian-first profile extensions, dedupe candidates, category/status history, correction workflows, consent and privacy controls. |
| Documents | Frappe File provides private-file primitives. | BRD needs document requirement matrix, quarantine, malware scan status, verification/rejection/replacement states and signed access flow. |
| Admissions | Education provides starting points for applicant/admission records. | BRD needs dynamic application forms, eligibility engine, merit runs, seat matrix, waitlist, offer expiry and idempotent conversion. |
| Fees and accounting | ERPNext, Education and Payments install together. | BRD needs approved education fee demand pattern, invoice/payment/GL reconciliation, refunds, settlement, duplicate webhook safety and finance dashboards. |
| Notifications | Frappe has email/notification primitives. | BRD needs transactional outbox, template versioning, MSG91/SMTP adapters, consent, retries, throttling, dead-letter state and audit logs. |
| Portal UX | Frappe web and app routes serve successfully. | BRD needs Vue 3 bilingual low-literacy portal with save/resume, mobile-first forms, offline/retry behavior and accessibility evidence. |

## Known Follow-Ups

- The clean Docker image rebuild timeout from P1.3 remains a follow-up before production-style image evidence is accepted.
- No production credentials, live payment, live SMS/email, Cloudflare R2, production DNS or production deployment work was performed.
- No business-functional DocTypes or workflows were implemented in this step; Phase 2.1 only proves compatibility of the pinned app set.

## Gate Result

P2.1 exit gate passed. No unresolved install or migration blocker remains for the pinned app set in the local Docker Compose environment.
