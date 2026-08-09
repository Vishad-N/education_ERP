# ADR-0006: Promote immutable container releases

- Status: Accepted
- Date: 2026-08-01
- Related requirements: Platform and production readiness

## Context

Interactive production updates make rollback, provenance, testing, and multi-site consistency unreliable.

## Decision

Build a signed image from pinned application SHAs using the approved `frappe_docker` baseline. Generate an SBOM, scan it, and promote the same digest across environments. Production containers never run interactive `bench get-app`, `git pull`, or source edits.

## Consequences

- Configuration and secrets are injected at runtime.
- Database migrations are versioned and rehearsed before deployment.
- Releases can be identified by image digest and application manifest.
- Application rollback is allowed only when schema compatibility is proven.

