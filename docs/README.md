# Engineering Documentation Index

`AGENTS.md` is the governing product and engineering contract. Documents in this directory explain how to implement and operate that contract. If they conflict, follow the authority order in `AGENTS.md` and create an ADR or requirement clarification.

## Architecture

| Document | Purpose |
|---|---|
| [System architecture](architecture/system-architecture.md) | Context, containers, modules, data flows, invariants, scaling boundaries |
| [Deployment architecture](architecture/deployment-architecture.md) | Production topology, tenancy, HA, capacity, rollout, environments |
| [Technology stack](architecture/technology-stack.md) | Selected frontend, backend, data, provider, and operations technologies |
| [Capacity plan](architecture/capacity-plan.md) | Initial 100-institution workload model, pod sizing, and scale triggers |
| [Database architecture](architecture/database-architecture.md) | Data ownership, entities, constraints, transactions, indexes, retention |
| [Repository structure](architecture/repository-structure.md) | Target folders, module boundaries, generated files, import rules |
| [Architecture decisions](adr/README.md) | ADR process, index, and templates |

## Product and delivery

| Document | Purpose |
|---|---|
| [Project implementation plan](../PROJECT_IMPLEMENTATION_PLAN.md) | Active execution plan; Phase 6.1 applicant and guardian PWA is next |
| [Project execution roadmap](../PROJECT_EXECUTION_ROADMAP.md) | Current step, prerequisites, completion gates, next-step state machine |
| [Current implementation status](current-implementation-status.md) | Honest inventory of scaffolded, missing, and production-blocking components |
| [Phase 0 source baseline](releases/p0-source-baseline.md) | Pinned upstream repositories, Docker build refs, and local cleanup evidence |
| [P1.1 repository-structure evidence](evidence/phase-1/p1.1/repository-structure-baseline.md) | Product repository layout, source/runtime separation, and local fake-provider baseline |
| [P2.1 app compatibility evidence](evidence/phase-2/p2.1/app-compatibility-proof.md) | Fresh install, migration, app version, import, HTTP, and Desk route compatibility proof |
| [P2.2 accounting evidence](evidence/phase-2/p2.2/accounting-proof.md) | Education fee schedule to ERPNext Sales Invoice, Payment Entry, refund, and GL reconciliation proof |
| [P2.3 integration foundation evidence](evidence/phase-2/p2.3/integration-foundation-proof.md) | Fake Razorpay, MSG91, SMTP, R2, and ClamAV adapter contract proof |
| [P3.1 completion evidence](evidence/phase-3/p3.1/completion.md) | Completed institution and academic master foundation proof with permissions, timetable conflict, and audit evidence |
| [P3.2 initial identity/document evidence](evidence/phase-3/p3.2/initial-identity-document-slice.md) | Initial student identity and document DocTypes, migration, and synthetic proof |
| [P3.2 gate review](evidence/phase-3/p3.2/gate-review.md) | Historical review from before P3.2 completion |
| [P3.2 completion evidence](evidence/phase-3/p3.2/completion.md) | Completed student identity and document foundation proof with guardian, issuance, scan, replacement, expiry, privacy, permission and audit evidence |
| [P4.1 completion evidence](evidence/phase-4/p4.1/completion.md) | Completed CRM handoff and versioned application form proof with idempotency, save/resume, duplicate rejection, permission and audit evidence |
| [P4.2 completion evidence](evidence/phase-4/p4.2/completion.md) | Completed eligibility, merit, seat matrix, allocation and offer proof with capacity protection, permission and audit evidence |
| [P4.3 completion evidence](evidence/phase-4/p4.3/completion.md) | Completed admission confirmation and conversion proof with required gates, one Student, one enrollment, identity issuance, permission and audit evidence |
| [P5.1 completion evidence](evidence/phase-5/p5.1/completion.md) | Completed fee policy and demand generation proof with policy math, adjustments, submitted Sales Invoice, generated demand, permission and audit evidence |
| [P5.2 completion evidence](evidence/phase-5/p5.2/completion.md) | Completed payment collection and receipt proof with fake provider order, online and offline payments, duplicate callback safety, permission and audit evidence |
| [P5.3 completion evidence](evidence/phase-5/p5.3/completion.md) | Completed refund, settlement and GL reconciliation proof with credit note, refund Payment Entry, settlement import, mismatch rejection, permission and audit evidence |
| [Pilot scope baseline](requirements/pilot-scope.md) | Phase 0 pilot scope, deferrals, workload reference, and acceptance baseline |
| [UX and localization](product/ux-and-localization.md) | Low-literacy, guardian-first, English/Hindi product requirements |
| [Requirements traceability](requirements/traceability.md) | BRD-to-design-to-test coverage and evidence |
| [Phase-1 delivery plan](requirements/phase-1-delivery-plan.md) | Workstreams, dependencies, gates, deliverables |
| [Development setup](development/local-development.md) | Reproducible local environment and app bootstrap |
| [Coding and workflow](development/engineering-workflow.md) | Branching, migrations, review, Definition of Done |
| [API and integrations](development/api-and-integrations.md) | API conventions, events, webhooks, provider adapters |
| [Provider architecture](integrations/provider-architecture.md) | Razorpay, MSG91, Hostinger SMTP, R2, and malware-scanning contracts |
| [Testing strategy](quality/testing-strategy.md) | Test pyramid, critical scenarios, performance and security gates |
| [Security and privacy](security/security-and-privacy.md) | Threat controls, access model, PII, secrets, audit, compliance |

## Production and operations

| Document | Purpose |
|---|---|
| [CI/CD](operations/ci-cd.md) | Build, test, scan, promote, deploy, rollback controls |
| [Production deployment](operations/production-deployment.md) | Provisioning, release procedure, smoke tests, rollback/forward-fix |
| [Hostinger production platform](operations/hostinger-production-platform.md) | VPS topology, hardening, pod rollout, and Hostinger-specific controls |
| [Observability](operations/observability.md) | Logs, metrics, traces, dashboards, SLOs, alerting |
| [Backup and disaster recovery](operations/backup-and-dr.md) | Backup scope, retention, PITR, restore, DR exercises |
| [Runbooks](operations/runbooks.md) | Incident procedures for common production failures |
| [Data migration](operations/data-migration.md) | Source assessment, mapping, trial loads, reconciliation, cutover |
| [Production readiness](operations/production-readiness-checklist.md) | Final go-live evidence and approvals |

## Documentation rules

- Link every material design choice to an ADR.
- Link every feature specification and test to BRD IDs.
- Use explicit owners, states, thresholds, and failure behavior.
- Do not put secrets, real student data, or production credentials in documentation.
- Update documents in the same pull request as the behavior they describe.
- Review links and stale `TBD` values before each release candidate.
