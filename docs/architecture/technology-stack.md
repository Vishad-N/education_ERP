# Technology Stack

## Selected stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend language | Python 3.14 | Frappe controllers, services, policies, jobs and integrations |
| Application framework | Frappe Framework v16 | DocTypes, ORM, permissions, workflows, APIs, queues and Desk |
| Accounting | ERPNext v16 | Receivables, payments, refunds, reconciliation and General Ledger |
| Education foundation | Frappe Education v16 | Student, applicant, program, course and enrollment foundations |
| CRM | Frappe CRM v1.x | Enquiries, counsellor pipeline and application handoff |
| Custom application | `university_erp` | Product-specific institution, academic, admission, fee and compliance domains |
| Staff frontend | Frappe Desk | Administrative forms, workflows, reports and approvals |
| Public frontend | Vue 3, TypeScript, Frappe UI and Vite | Applicant, guardian and student bilingual PWA |
| Database | MariaDB 11.8 | Authoritative site-local transactional storage |
| Cache and queues | Redis/Valkey | Cache, Frappe jobs and realtime coordination |
| Realtime | Frappe Socket.IO | Approved user-facing state updates |
| Edge | Cloudflare | DNS, TLS, CDN, WAF, DDoS and rate controls |
| Object storage | Cloudflare R2 | Private documents, receipts, exports and backup objects |
| Payments | Razorpay | Orders, checkout, webhooks, refunds and settlements |
| SMS/OTP | MSG91 | DLT-aware transactional SMS, OTP and delivery status |
| Email | Hostinger Business Email SMTP | Initial institution email delivery |
| Malware scanning | ClamAV | Quarantine scan before verification/access |
| Containers | Docker and official `frappe_docker` patterns | Reproducible local and immutable production releases |
| Metrics | Prometheus | Application, queue, database and infrastructure metrics |
| Dashboards/alerts | Grafana | SLO, business and operations dashboards |
| Logs | Loki | Central structured diagnostic logs |
| Availability | Uptime Kuma | External endpoint and certificate monitoring |
| Testing | Frappe test framework plus Playwright | Domain, integration, permission and browser journeys |
| Infrastructure | Reviewed automation/IaC | Repeatable Hostinger pod, Cloudflare and monitoring setup |

## Frontend policy

Use Frappe Desk for staff administration. Do not rebuild generic administrative CRUD, lists, permissions or workflows in a separate SPA.

Use the Vue/TypeScript PWA for applicants, guardians and students because these users require a simpler mobile-first experience than Desk. The PWA delegates all authorization, validation, eligibility, fees, seats and payment decisions to Frappe APIs.

Do not add React, Next.js, a Node.js business backend, GraphQL or native mobile apps in Phase 1 without an ADR.

## Backend policy

Business logic remains in the `university_erp` modular monolith. Provider SDKs remain in integration adapters. ERPNext remains the accounting authority. Microservices, Kafka, OpenSearch and a separate analytics warehouse are deferred until measured needs satisfy extraction criteria.

## Version and supply-chain policy

- Pin every application, base image and build tool by approved tag and immutable digest/SHA.
- Do not release from moving branches or `latest` images.
- Generate an SBOM and provenance for each image.
- Scan dependencies, source, secrets, containers and infrastructure configuration.
- Promote one signed image digest through UAT, staging and production.

## Environment usage

| Environment | Providers | Data |
|---|---|---|
| Local | Fake payments/SMS/scanner, Mailpit, local object storage | Synthetic only |
| CI | Deterministic fake adapters | Ephemeral synthetic |
| Development | Sandbox/fake providers | Synthetic |
| UAT | Sandbox providers and approved test recipients | Synthetic or masked |
| Staging | Production-like restricted integrations | Masked production-sized data |
| Production | Razorpay, MSG91/DLT, Hostinger SMTP, R2 | Real institution data |

