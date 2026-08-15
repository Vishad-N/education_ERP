# ADR-0015: Use Railway for staging with a portable container runtime

- Status: Accepted for Phase 8 staging
- Date: 2026-08-15
- Related requirements: Deployment portability, staging, restore rehearsal, pilot readiness

## Context

ADR-0007 selected Hostinger VPS for the initial production platform. The project now requires Railway as the first staging environment while retaining deployment readiness for Hostinger VPS and AWS. Frappe requires separate HTTP, realtime, scheduler and worker processes plus MariaDB and Redis/Valkey connectivity.

Railway maps Compose services to separate project services and supports service-specific configuration as code. AWS ECS and Hostinger Compose use different orchestration formats but can run the same immutable image and role commands.

## Decision

Use Railway for the first production-like staging deployment. Keep Hostinger VPS as the current production baseline until a later approved ADR changes it. Maintain AWS ECS/Fargate as a portable alternative.

Build one immutable application image. Select runtime behavior with these explicit roles:

- `web`;
- `websocket`;
- `scheduler`;
- `worker-short`;
- `worker-long`;
- `migrate`.

Generate non-secret Frappe routing configuration and secret-backed site configuration at container start from environment variables. Store authoritative databases, queues, files, encryption keys and backups outside ephemeral container filesystems.

## Consequences

- Railway staging requires multiple services, private MariaDB-compatible and Redis/Valkey endpoints, managed variables and a controlled one-shot migration job.
- The web service binds to the platform `PORT` and exposes a database/cache readiness probe.
- Railway staging does not replace Cloudflare, Hostinger, R2, backup or production acceptance requirements.
- Hostinger Compose and AWS ECS templates use the same image and startup contract, reducing provider lock-in.
- No production service, DNS, credential or paid resource is created by repository configuration alone.

## Revisit triggers

Revisit before production if Railway becomes the proposed production platform, if shared-file requirements cannot be satisfied through private object storage, or if measured cost, availability, data residency or operational limits fail the pilot requirements.
