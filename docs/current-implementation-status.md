# Current Implementation Status

## Purpose

This document distinguishes files that currently exist from capabilities that are actually implemented and verified. Agents must not treat scaffolding, empty directories, configuration examples, or installed JavaScript dependencies as completed product functionality.

## Current milestone

| Field | Current value |
|---|---|
| Product state | Phase 5 fee, payment, refund, settlement and GL reconciliation foundations completed locally |
| Roadmap state | `P6.1` applicant and guardian PWA is next under `PROJECT_IMPLEMENTATION_PLAN.md` |
| Production readiness | Not production ready |
| Upstream source repositories | Pulled into `apps/` at pinned commits for local reference and later Bench setup |
| Custom Frappe app | Generated app files exist and install on the local `erp.localhost` site |
| Business modules | P3.1 institution/academic foundations, P3.2 student identity/document foundations, Phase 4 admissions foundations through conversion and Phase 5 fee/accounting foundations are locally implemented and proven |
| Production infrastructure | Not provisioned |
| Real integrations | Not implemented or approved |
| Automated product tests | Not implemented |

## Existing repository assets

- Product, architecture, security, development, testing and operations documentation.
- Phase 0 source baseline manifest at `docs/releases/p0-source-baseline.md`.
- Phase 0 provider ownership ADR at `docs/adr/0012-institution-owned-provider-accounts.md`.
- Pilot scope baseline at `docs/requirements/pilot-scope.md`.
- Phase 1 repository-structure evidence at `docs/evidence/phase-1/p1.1/repository-structure-baseline.md`.
- Phase 1 custom app evidence at `docs/evidence/phase-1/p1.2/university-erp-generation.md`.
- Phase 1 local bootstrap evidence at `docs/evidence/phase-1/p1.3/local-bootstrap.md`.
- Phase 2.1 compatibility evidence at `docs/evidence/phase-2/p2.1/app-compatibility-proof.md`.
- Phase 2.2 accounting evidence at `docs/evidence/phase-2/p2.2/accounting-proof.md`.
- Accounting pattern ADR at `docs/adr/0013-fee-demand-sales-invoice-accounting-pattern.md`.
- Phase 2.3 integration foundation evidence at `docs/evidence/phase-2/p2.3/integration-foundation-proof.md`.
- Fake provider contract ADR at `docs/adr/0014-fake-provider-contract-foundation.md`.
- Phase 3.1 completion evidence at `docs/evidence/phase-3/p3.1/completion.md`.
- Phase 3.2 initial identity/document evidence at `docs/evidence/phase-3/p3.2/initial-identity-document-slice.md`.
- Phase 3.2 gate review at `docs/evidence/phase-3/p3.2/gate-review.md`.
- Phase 3.2 completion evidence at `docs/evidence/phase-3/p3.2/completion.md`.
- Phase 4.1 CRM handoff/application form evidence at `docs/evidence/phase-4/p4.1/completion.md`.
- Phase 4.2 eligibility/merit/seat evidence at `docs/evidence/phase-4/p4.2/completion.md`.
- Phase 4.3 admission confirmation/conversion evidence at `docs/evidence/phase-4/p4.3/completion.md`.
- Phase 5.1 fee policy/demand generation evidence at `docs/evidence/phase-5/p5.1/completion.md`.
- Phase 5.2 payment collection/receipt evidence at `docs/evidence/phase-5/p5.2/completion.md`.
- Phase 5.3 refund/settlement/GL reconciliation evidence at `docs/evidence/phase-5/p5.3/completion.md`.
- Root tooling configuration and documentation formatting scripts.
- `apps.json` containing intended Frappe, ERPNext, Education, CRM, Payments and custom-app sources.
- Local upstream source checkouts under `apps/`:
  - `apps/frappe` at `ba18090b141740e75d52aa97bfc525ff2f831f6c`
  - `apps/erpnext` at `054b20a2ae1bdea44694cca72d17412945171cab`
  - `apps/education` at `1c29e646bf943c2a5f696cb81cb48c8a072cbebc`
  - `apps/crm` at `bf1b7f07ac01b6ac435f25db7ccef6b52807720e`
  - `apps/payments` at `cca07d9f9392e2ea0e521c5975151db9e4b6c321`
  - `apps/frappe_docker` at `616ffd417797031f760e7a6c9669923a5febed66`
- Local-development `compose.yaml` with MariaDB, three Redis services, backend, WebSocket, scheduler and workers.
- Development Dockerfile and common Frappe site configuration.
- Bootstrap prerequisite, site initialization and repository verification scripts.
- `university_erp` folder structure, Frappe app metadata, Python package metadata and Vue/Vite package metadata.
- Local `erp.localhost` site with Frappe, ERPNext, Payments, Education, CRM and `university_erp` installed.
- Local `p21.localhost` compatibility site with the pinned app set installed and migrated.
- Local `p21.localhost` synthetic accounting proof data for `P2.2 Accounting Proof School`.
- Local fake provider adapters for Razorpay, MSG91, SMTP, R2 and ClamAV under `apps/university_erp/university_erp/integrations/`.
- Phase 3.1 custom DocTypes under `apps/university_erp/university_erp/university_erp/doctype/`.
- Local `p21.localhost` synthetic P3.1 master-data proof records for `P3.1 Proof University`, `P31 Proof Program`, `P31-OFFER-2026`, `P31-CLASS-2026`, `P31-A`, curriculum, subject offering, faculty assignment, timetable and related intake records.
- Phase 3.2 custom DocTypes under `apps/university_erp/university_erp/university_erp/doctype/`.
- Local `p21.localhost` synthetic P3.2 identity/document proof records for `EDU-APP-2026-00001`, `SIP-2026-00004`, `EDU-GRD-2026-00001`, `SII-2026-00026`, `P32-BIRTH`, `P32-BIRTH-GEN`, `SDOC-P32-BIRTH-00011`, `SDOC-P32-BIRTH-00027`, `SDOC-P32-BIRTH-00030` and related consent, correction, dedupe, verification, replacement, expiry and privacy records.
- Phase 4.1 custom DocTypes under `apps/university_erp/university_erp/university_erp/doctype/`.
- Local `p21.localhost` synthetic P4.1 proof records for `CRM-LEAD-2026-00013`, `AAF-P41-PILOT-2026.1`, `AAD-AAF-P41-PILOT-2026.1-00052`, `CAH-CRM-LEAD-2026-00013-00053` and `EDU-APP-2026-00002`.
- Phase 4.2 custom DocTypes under `apps/university_erp/university_erp/university_erp/doctype/`.
- Local `p21.localhost` synthetic P4.2 proof records for `ERS-P42-MIN-SCORE-2026.1`, `P42-MERIT-2026`, `MR-P42-MERIT-2026-00066`, `ASM-P31-OFFER-2026-P31 General`, `SAR-MR-P42-MERIT-2026-00066-1`, accepted and waitlisted seat offers.
- Phase 4.3 custom DocTypes under `apps/university_erp/university_erp/university_erp/doctype/`.
- Local `p21.localhost` synthetic P4.3 proof records for admission confirmation `AC-SO-SAR-MR-P42-MERIT-2026-00066-1-EDU-APP-2026-00002`, conversion `ASC-AC-SO-SAR-MR-P42-MERIT-2026-00066-1-EDU-APP-2026-00002`, Student `EDU-STU-2026-00002`, Program Enrollment `EDU-ENR-2026-00002` and identity issuance `SII-2026-00096`.
- Phase 5.1 custom DocTypes under `apps/university_erp/university_erp/university_erp/doctype/`.
- Local `p21.localhost` synthetic P5.1 proof records for fee category `P5.1 Tuition Fee`, fee code `P51-TUITION`, policy `EFP-P51-POLICY-2026.1`, installment `EFI-EFP-P51-POLICY-2026.1-1`, fee schedule `EDU-FSH-2026-00002`, Sales Invoice `ACC-SINV-2026-00003` and Student Fee Demand `SFD-EDU-STU-2026-00002-EFP-P51-POLICY-2026.1-00109`.
- Phase 5.2 custom DocTypes under `apps/university_erp/university_erp/university_erp/doctype/`.
- Local `p21.localhost` synthetic P5.2 proof records for provider order `order_000001`, online payment receipt `SFP-SFD-EDU-STU-2026-00002-EFP-P51-POLICY-2026.1-00109-00127`, online Payment Entry `ACC-PAY-2026-00004`, offline payment receipt `SFP-SFD-EDU-STU-2026-00002-EFP-P51-POLICY-2026.1-00109-00128` and offline Payment Entry `ACC-PAY-2026-00005`.
- Phase 5.3 custom DocTypes under `apps/university_erp/university_erp/university_erp/doctype/`.
- Local `p21.localhost` synthetic P5.3 proof records for Student Fee Refund `SFR-SFP-SFD-EDU-STU-2026-00002-EFP-P51-POLICY-2026.1-00109-00127-00149`, credit note `ACC-SINV-2026-00004`, refund Payment Entry `ACC-PAY-2026-00006`, settlement import `PSI-fake_razorpay-setl_p53_0001` and GL reconciliation `FGR-SFD-EDU-STU-2026-00002-EFP-P51-POLICY-2026.1-00109-00150`.
- Placeholder infrastructure, migration, operations, contract, E2E, performance and security folders.
- Previous local Docker Compose containers and network were removed on 2026-08-09; named project volumes were intentionally retained.

## Known gaps after local platform bootstrap completion

- Dockerfile uses a concrete `frappe/bench:v5.31.0` bootstrap tag, but the final production image digest/SBOM is not recorded yet.
- Clean rebuild of the updated Dockerfile exceeded local command timeouts after adding `university_erp`; this needs follow-up before accepting production-style image evidence.
- Local Compose is a development topology, not Hostinger production topology.
- Redis persistence, production secrets, TLS, proxy, health/readiness and backup behavior are not production configured.
- No Git-hosted CI workflow, SBOM, image signature, vulnerability policy or release manifest exists.
- P3.1 institution and academic master foundations are implemented locally, but browser/Desk workflow tests, CI integration, production approval workflows, translations and broader reports remain later-phase work.
- P3.2 student identity/document foundations are implemented locally, but browser/Desk workflow tests, CI integration, translations, production-scale migration tests and real provider-backed document storage/scanning remain later-phase work.
- P4.1 CRM handoff/application form foundations are implemented locally, but browser/portal workflow tests, public API methods, localization and CI integration remain later-phase work.
- P4.2 eligibility/merit/seat foundations are implemented locally, but browser/portal workflow tests, public API methods, localization, CI integration and production concurrency load tests remain later-phase work.
- P4.3 admission confirmation/conversion foundations are implemented locally, but browser/portal workflow tests, public API methods, localization and CI integration remain later-phase work.
- P5.1 fee policy/demand generation foundations are implemented locally, but browser/Desk workflow tests, public API methods, CI integration, broader fee story IDs and production-scale financial reconciliation tests remain later-phase work.
- P5.2 payment collection/receipt foundations are implemented locally, but real Razorpay sandbox credentials, browser payment pages, public callback APIs, CI integration, provider settlement reconciliation and production financial controls remain later-phase work.
- P5.3 refund, settlement and GL reconciliation foundations are implemented locally, but full finance dashboards, browser/Desk workflow tests, CI integration, production bank statement imports and real provider settlements remain later-phase work.
- No automated unit, integration, permission, migration, browser, performance or security tests exist.
- No infrastructure-as-code or production monitoring implementation exists.
- No production Razorpay, MSG91/DLT, Hostinger SMTP or Cloudflare R2 configuration is approved.

## Interpretation rules for agents

- Empty folders represent intended ownership, not completed modules.
- A dependency in `package.json` represents an intended tool, not a verified integration.
- A Compose service represents local orchestration, not production availability.
- Example/default passwords are local-development values only.
- A roadmap step becomes `DONE` only when its artifacts and verification gate pass.
- Do not advance the execution roadmap merely because a file or folder already has the expected name.

## Immediate next action

Continue `PROJECT_IMPLEMENTATION_PLAN.md` at `P6.1`. The next work is the applicant and guardian PWA. Live credentials, production infrastructure, real provider traffic and production deployment remain blocked until explicit approval at later phases.
