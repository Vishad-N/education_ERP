# ADR-0002: Keep product behavior in a custom app

- Status: Accepted
- Date: 2026-08-01
- Related requirements: All custom and extended Phase-1 requirements

## Context

Routine edits to upstream applications create upgrade conflicts, untracked behavior, and security maintenance risk.

## Decision

Implement institution-specific DocTypes, services, hooks, workflows, reports, APIs, patches, integrations, and portal extensions in `university_erp`. Do not edit Frappe, ERPNext, Education, or CRM source for convenience.

An upstream fork requires a separate ADR, verified defect, upstream issue or PR, minimal patch, regression test, and exit plan.

## Consequences

- Fit-gap analysis precedes customization.
- Extension hooks are preferred over class replacement.
- Upgrade testing can treat upstream applications as pinned immutable dependencies.

