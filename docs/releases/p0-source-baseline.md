# Phase 0 Source Baseline

- Status: Approved for local bootstrap
- Date: 2026-08-09
- Scope: Phase 0 repository verification and immutable source pinning

## Local source checkouts

| Source | Local path | Remote URL | Checked-out ref | Commit SHA | Compatibility basis |
|---|---|---|---|---|---|
| Frappe Framework | `apps/frappe` | `https://github.com/frappe/frappe.git` | detached HEAD from `v16.19.0` | `ba18090b141740e75d52aa97bfc525ff2f831f6c` | Frappe v16 baseline |
| ERPNext | `apps/erpnext` | `https://github.com/frappe/erpnext.git` | detached HEAD from `v16.22.0` | `054b20a2ae1bdea44694cca72d17412945171cab` | ERPNext v16 baseline |
| Frappe Education | `apps/education` | `https://github.com/frappe/education.git` | detached HEAD from `version-16` lineage | `1c29e646bf943c2a5f696cb81cb48c8a072cbebc` | Education v16-compatible branch |
| Frappe CRM | `apps/crm` | `https://github.com/frappe/crm.git` | detached HEAD from `v1.72.0` | `bf1b7f07ac01b6ac435f25db7ccef6b52807720e` | CRM v1 release compatible with Frappe v16 target |
| Frappe Payments | `apps/payments` | `https://github.com/frappe/payments.git` | detached HEAD from `version-16` lineage | `cca07d9f9392e2ea0e521c5975151db9e4b6c321` | Payments app for ERPNext payment integration |
| Frappe Docker | `apps/frappe_docker` | `https://github.com/frappe/frappe_docker.git` | detached HEAD | `616ffd417797031f760e7a6c9669923a5febed66` | Docker composition/build reference |

## Container build baseline

| Input | Value | Notes |
|---|---|---|
| Bench bootstrap image | `frappe/bench:v5.31.0` | Concrete Docker Hub tag selected for Phase 0; production release must later record image digest/SBOM. |
| Frappe app installation | `v16.19.0` verified as `ba18090b141740e75d52aa97bfc525ff2f831f6c` | Dockerfile checks the installed SHA. |
| ERPNext app installation | `054b20a2ae1bdea44694cca72d17412945171cab` | Dockerfile checks out the exact SHA. |
| Education app installation | `1c29e646bf943c2a5f696cb81cb48c8a072cbebc` | Dockerfile checks out the exact SHA. |
| CRM app installation | `v1.72.0` verified as `bf1b7f07ac01b6ac435f25db7ccef6b52807720e` | Dockerfile checks the installed SHA. |
| Payments app installation | `cca07d9f9392e2ea0e521c5975151db9e4b6c321` | Dockerfile checks out the exact SHA. |

## Verification commands

Run from the repository root:

```powershell
$repos = "frappe","erpnext","education","crm","payments","frappe_docker"
foreach ($repo in $repos) {
  $path = Resolve-Path "apps/$repo"
  git -c safe.directory=$path -C $path remote -v
  git -c safe.directory=$path -C $path rev-parse HEAD
}
npm.cmd run check:repo
```

## Build input rule

`apps.json`, `.env.example`, `compose.yaml`, and `docker/Dockerfile` must use these exact refs or exact successor refs recorded in a later manifest. Development may inspect upstream source locally, but product changes must remain in `apps/university_erp` unless an ADR approves an upstream defect patch.

## Docker cleanup state

Previous local Compose containers and the `education-erp_default` network were removed on 2026-08-09. Named Docker volumes were intentionally retained:

- `education-erp_mariadb-data`
- `education-erp_redis-cache-data`
- `education-erp_redis-queue-data`
- `education-erp_redis-socketio-data`
- `education-erp_sites-data`
