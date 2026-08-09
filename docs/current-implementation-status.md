# Current Implementation Status

## Purpose

This document distinguishes files that currently exist from capabilities that are actually implemented and verified. Agents must not treat scaffolding, empty directories, configuration examples, or installed JavaScript dependencies as completed product functionality.

## Current milestone

| Field | Current value |
|---|---|
| Product state | Pre-bootstrap engineering scaffold |
| Roadmap state | `S0.1` is the next governing execution step |
| Production readiness | Not production ready |
| Custom Frappe app | Directory skeleton exists; Bench-generated app is not complete |
| Business modules | Not implemented |
| Production infrastructure | Not provisioned |
| Real integrations | Not implemented or approved |
| Automated product tests | Not implemented |

## Existing repository assets

- Product, architecture, security, development, testing and operations documentation.
- Root tooling configuration and documentation formatting scripts.
- `apps.json` containing intended Frappe, ERPNext, Education, CRM and custom-app sources.
- Local-development `compose.yaml` with MariaDB, three Redis services, backend, WebSocket, scheduler and workers.
- Development Dockerfile and common Frappe site configuration.
- Bootstrap prerequisite, site initialization and repository verification scripts.
- `university_erp` folder structure, Python package metadata and Vue/Vite package metadata.
- Placeholder infrastructure, migration, operations, contract, E2E, performance and security folders.

## Known gaps that block `S1.1` completion

- `apps.json` contains `PIN_EXACT_SHA_BEFORE_RELEASE` values.
- `FRAPPE_DOCKER_REF` is not pinned.
- Dockerfile uses `frappe/bench:latest`, which is not an immutable production base.
- Docker build fetches branches/tags without verified source SHAs.
- The custom app has not been generated and installed through Bench; expected Frappe files such as `hooks.py` are absent.
- Local Compose is a development topology, not Hostinger production topology.
- Redis persistence, production secrets, TLS, proxy, health/readiness and backup behavior are not production configured.
- No Git-hosted CI workflow, SBOM, image signature, vulnerability policy or release manifest exists.
- No domain DocTypes, APIs, workflows, provider adapters, translations or business logic exist.
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

Follow `PROJECT_EXECUTION_ROADMAP.md` starting at `S0.1`. Resolve payment settlement ownership, SMS/DLT sender ownership, SMTP ownership and accountable finance/privacy decision-makers before completing infrastructure or integration implementation.

