# ADR-0008: Use Cloudflare R2 for private object storage

- Status: Accepted
- Date: 2026-08-02
- Related requirements: Student/applicant documents, receipts, exports and backups

## Decision

Use Cloudflare R2 through its S3-compatible API for private documents, generated receipts/reports/exports and approved backup objects. Isolate production institutions through per-site buckets or an equivalently approved credential boundary. Use short-lived authorized URLs; do not use public `r2.dev` delivery for production data.

## Consequences

- MariaDB stores ownership, checksum, scan, status and lifecycle metadata.
- Uploads remain quarantined until validation and ClamAV pass.
- R2 credentials are site/environment scoped and rotated.
- Retention, versioning, backup and cost controls require automation.

