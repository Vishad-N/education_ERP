# P8 Staging Release Manifest

- Status: Staging accepted; not a production release
- Date: 2026-08-17
- Site: `web-production-7580e.up.railway.app`
- Railway project: `education-erp-backend` (`6d24ea5d-99d4-4614-b608-569be198e321`)
- Environment: `production` (Railway environment name; this is staging)

## Application SHAs

| Component | Tag / ref | SHA |
|---|---|---|
| Frappe | v16.19.0 | `ba18090b141740e75d52aa97bfc525ff2f831f6c` |
| ERPNext | v16.22.0 | `054b20a2ae1bdea44694cca72d17412945171cab` |
| Education | version-16 pin | `1c29e646bf943c2a5f696cb81cb48c8a072cbebc` |
| CRM | v1.72.0 | `bf1b7f07ac01b6ac435f25db7ccef6b52807720e` |
| Payments | version-16 pin | `cca07d9f9392e2ea0e521c5975151db9e4b6c321` |
| frappe_docker reference | pin | `616ffd417797031f760e7a6c9669923a5febed66` |
| Bench image | `frappe/bench:v5.31.0` | `sha256:e44c7454500296940d26ef45eefff8fc295b9d9aacaac4e5714e8be01c326ee8` |
| university_erp | 0.0.0 | repository tree at commit `cede62abe47887b5ad68845bd18815f071760cbb` plus uncommitted P8 files recorded in evidence |

## Runtime image digests

| Service | Role | Deployment | Digest |
|---|---|---|---|
| `web` | HTTP/API | `b757b47a-bd87-4f7a-be60-ec370b3df517` | `sha256:9e67b33f90b77701b1aa6d9d3641f960f39afe0d155ff244d1281db14047eb85` |
| `bootstrap` | combined scheduler + all queues | `71c6041d-f258-4317-8a16-6df0f94b4840` | `sha256:43f711b403e4358254994c200147b72d16459c4f57f45c13516039d24ee7c506` |
| `mariadb` | MariaDB 11.8 | `5cf9aec7-7baf-4486-9fe1-7a66a86b3268` | vendor image `mariadb:11.8` |
| `Redis` | cache/queue/realtime | `3af6f5db-ec0e-449b-b7fe-76d4f6833abc` | vendor image `redis:8.2` |

The two application digests are not identical. Staging accepted a combined worker image after the web image because the Railway free plan cannot add more services. Production must publish one digest and run every role from it.

## Schema

| Field | Value |
|---|---|
| Site name | `web-production-7580e.up.railway.app` |
| Database | `education_erp_staging` |
| `university_erp` patches.txt | empty pre and post model-sync lists |
| Schema source | Frappe migrate from the pinned apps plus generated custom DocTypes |

## SBOM

Source-component SBOM: `docs/releases/p8-source.cdx.json`.

This is a CycloneDX inventory of pinned application sources. It is not a signed container SBOM from a registry. Registry publication and image signing remain a Phase 9 production item.

## Health

```text
GET https://web-production-7580e.up.railway.app/api/method/university_erp.api.health.live
GET https://web-production-7580e.up.railway.app/api/method/university_erp.api.health.ready
```

Both must return HTTP 200.

## Deferred from this manifest

- Human UAT
- Real Razorpay, MSG91, SMTP, and R2 credentials
- Cloudflare DNS cutover
- Dedicated WebSocket, migrate, and backup services
- Off-host PITR
- Production owner signatures
