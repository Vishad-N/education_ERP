# ADR-0004: Use one site per independent institution

- Status: Accepted
- Date: 2026-08-01
- Related requirements: `BRD-US-001..010`

## Context

Independent universities require separate governance, users, integrations, files, encryption keys, backups, accounting, and data lifecycle. Frappe sites already provide database-level isolation.

## Decision

Provision a separate Frappe site for each independently governed institution. Multiple campuses or colleges share a site only when academic masters, accounting, and reporting governance are shared. Do not add a universal `tenant_id` as a substitute for sites.

## Consequences

- Fleet provisioning, migration, monitoring, quota, and backup automation are required.
- Cross-institution reporting requires a separately approved, privacy-safe aggregation design.
- Site keys and backups are isolated and independently restorable.

