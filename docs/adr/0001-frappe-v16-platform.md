# ADR-0001: Use Frappe v16 as the platform baseline

- Status: Accepted
- Date: 2026-08-01
- Related requirements: All Phase-1 requirements

## Context

The product needs metadata-driven records, workflows, permissions, portals, APIs, queues, audit history, and an accounting platform. Frappe, ERPNext, Education, and CRM provide these foundations.

## Decision

Use compatible, exact releases or SHAs from the Frappe v16 ecosystem. Validate the complete application matrix before promotion. Use the dependency versions from the tested official production image.

## Consequences

- Teams must use Frappe conventions and supported extension hooks.
- Patch upgrades require matrix regression and migration rehearsal.
- Moving branches are prohibited in deployed images.
- Unsupported plugins or version combinations block release until proven compatible.

## Revisit triggers

Review when v16 support nears its end, a critical requirement cannot be implemented safely, or a later supported line passes full compatibility and migration tests.

