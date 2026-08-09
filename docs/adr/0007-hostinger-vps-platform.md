# ADR-0007: Use Hostinger VPS for the initial production platform

- Status: Accepted
- Date: 2026-08-02
- Related requirements: Production deployment and 100-institution scaling

## Context

The product requires a cost-conscious self-hosted platform for the pilot and early rollout. Hostinger offers root-controlled KVM VPS resources, while the project accepts responsibility for operating the complete software stack.

## Decision

Use separate Hostinger application and database VPSs for the production pilot. Scale through independently recoverable pods of approximately 20-25 measured institution sites rather than one platform-wide server/database. Use Cloudflare at the public edge and encrypted private networking between VPS roles.

## Consequences

- The team owns OS, Docker, database, cache, network, backup, monitoring, security and incident operations.
- Local Compose cannot be promoted unchanged to production.
- High availability and database failover require explicit implementation and testing.
- Hostinger snapshots are supplementary, not the recovery strategy.

## Revisit triggers

Review when Hostinger constraints prevent required private networking, failover, RPO/RTO, observability, data residency or sustained capacity.

