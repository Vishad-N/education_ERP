# ADR-0003: Use a modular monolith first

- Status: Accepted
- Date: 2026-08-01
- Related requirements: All Phase-1 requirements

## Context

Admissions, seats, identity, fees, and accounting contain transactions that require strong consistency. Frappe is already a monolithic application platform with queues and extension points.

## Decision

Implement clear domain modules in `university_erp` and deploy them together. Scale stateless replicas, workers, queues, indexes, and sites before extracting services.

Extraction requires measured independent scale above an order of magnitude, a separate security/failure boundary, a different runtime, or multi-product reuse. The extracted capability must own its data and provide versioned idempotent contracts and reconciliation.

## Consequences

- Cross-domain writes use named service commands.
- Internal module boundaries are reviewed even though deployment is shared.
- Distributed transactions are avoided in Phase 1.

