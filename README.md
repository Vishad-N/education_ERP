# University ERP

Production-oriented Education ERP for Indian institutions, beginning with a small-township high-school pilot and designed to grow to 100 independently governed institutions. It uses Frappe Framework v16, ERPNext v16, Frappe Education v16, Frappe CRM v1.x, and the custom `university_erp` application.

## Start here

1. Read [AGENTS.md](AGENTS.md) for product scope, non-negotiable decisions, and implementation rules.
2. Read the [project execution roadmap](PROJECT_EXECUTION_ROADMAP.md) and execute only its next eligible step.
3. Check the [current implementation status](docs/current-implementation-status.md) before assuming a component exists.
4. Read the [system architecture](docs/architecture/system-architecture.md) and [documentation index](docs/README.md).
5. Resolve open decisions using Architecture Decision Records before implementation diverges from the baseline.
6. Maintain story-to-test coverage in [requirements traceability](docs/requirements/traceability.md).
7. Follow the [repository structure](docs/architecture/repository-structure.md) when bootstrapping the Bench and custom app.

## Current status

Phases 0–8 staging gates are complete, with human UAT and production signatures deferred. The next step is **P9.1** controlled pilot launch in [PROJECT_IMPLEMENTATION_PLAN.md](PROJECT_IMPLEMENTATION_PLAN.md).

The product is **not production-ready**. A Railway staging stack is live for smoke checks. Real Razorpay, MSG91, SMTP, and Cloudflare R2 traffic remain blocked.

| Field | Value |
|---|---|
| Product state | Local domain foundations through Phase 7; Railway-first staging in progress |
| Next executable step | `P9.1` |
| Production readiness | Not production ready |
| Automated tests | 10 `university_erp` tests pass on `p21.localhost` |
| Live staging web | [https://web-production-7580e.up.railway.app](https://web-production-7580e.up.railway.app) |

## Live Railway staging

Railway project: `education-erp-backend` (environment `production`). Verified 2026-08-16.

| Service | State | Notes |
|---|---|---|
| `web` | Running | Public Desk/API and built portal assets |
| `mariadb` | Running | Persistent volume |
| `Redis` | Running | Shared cache/queue/realtime endpoint for staging |
| `bootstrap` (combined role) | Running | Constrained staging: scheduler plus all worker queues in one replica |

Dedicated `scheduler`, `websocket`, `worker-short`, `worker-long`, `migrate`, and `backup` services are not created. The Railway free plan is at its service cap. Use `combined` only until the plan is upgraded. Realtime still needs a dedicated WebSocket route.

### Health

```text
GET https://web-production-7580e.up.railway.app/api/method/university_erp.api.health.live
GET https://web-production-7580e.up.railway.app/api/method/university_erp.api.health.ready
```

Both return HTTP 200 when the site and MariaDB/Redis dependencies are up. `/login` also returns HTTP 200.

### Desk login

| Field | Value |
|---|---|
| URL | [https://web-production-7580e.up.railway.app/login](https://web-production-7580e.up.railway.app/login) |
| User ID | `Administrator` |

The Frappe System Manager account is always `Administrator`. The staging password is `SITE_ADMIN_PASSWORD` in the local gitignored file `secrets/railway-education-erp-backend.env`. Railway no longer stores that variable on `web` or `bootstrap` after the one-shot site create.

Do not commit passwords, encryption keys, or database credentials. Local Compose still uses the development defaults in `.env.example` (`Administrator` / `admin`); that is not the Railway password.

### Railway CLI

```text
railway --version    # 5.41.2 on the operator workstation
railway whoami
railway status
railway service list
```

Agent skills and remote Railway MCP are installed with `railway setup agent -y`. Restart the coding tool after that command so MCP registers.

## Delivery path

```text
Phase 0   ownership decisions, workload baseline, pilot scope, compliance
Phase 1   exact version pins, generated custom app, local compatibility proof
Phase 2   platform foundation, accounting, integrations, fake providers
Phase 3   institution, academic, student identity, documents
Phase 4   CRM handoff, eligibility, merit, seats, conversion
Phase 5   fees, payments, refunds, settlement, GL reconciliation
Phase 6   bilingual guardian and student portals
Phase 7   security, privacy, synthetic migration
Phase 8   Railway-first staging and portable production preparation
Phase 9   pilot go-live and hypercare
Phase 10  measured rollout toward 100 institutions
```

No phase is complete until its business rules, permissions, audit behavior, failure paths, migration impact, and acceptance evidence are complete.

## Remaining testing

Local automated coverage is the 10-test `university_erp` suite. Release-candidate work still open:

- P6.1 guardian PWA human checks in [docs/quality/human-testing-readme.md](docs/quality/human-testing-readme.md)
- Pilot UAT `UAT-001` through `UAT-009` in [docs/quality/pilot-uat-script.md](docs/quality/pilot-uat-script.md)
- Browser E2E, accessibility, and bilingual UI evidence
- CI integration of the custom-app suite
- Concurrent seat-acceptance and payment-webhook load tests
- Performance against the capacity profile
- Full Frappe role-permission matrix tests
- Dependency/container scans, image signing, and registry SBOM verification
- Independent penetration test
- Production-sized masked migration rehearsal and finance GL sign-off
- Staging restore test after backup/PITR automation
- Real provider sandbox tests (Razorpay, MSG91/DLT, SMTP, R2) after approved credentials
- Product, Institution, Finance, Security/Privacy, and Migration Operator signatures

## Core principles

- One Frappe site and database per independently governed institution.
- A modular monolith first; services are extracted only from measured scaling or security needs.
- ERPNext General Ledger is the financial source of truth.
- All business rules and permission checks are enforced server-side.
- Production releases are immutable, pinned, tested container images.
- External effects use idempotent APIs, background jobs, and a transactional outbox.
- Published and financial records are versioned or reversed, never silently overwritten.
- Applicant and guardian workflows are English/Hindi, mobile-first, low-bandwidth, and designed for very low digital literacy.
