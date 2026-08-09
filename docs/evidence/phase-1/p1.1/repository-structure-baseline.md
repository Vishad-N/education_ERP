# P1.1 Repository Structure Baseline

- Status: Complete
- Date: 2026-08-09
- Step: P1.1 - Create Product Repository Structure

## Required Root Assets

| Asset | Status | Notes |
|---|---|---|
| `.env.example` | Present | Safe local defaults and fake/local provider settings only. |
| `.editorconfig` | Present | Root editor conventions exist. |
| `.gitignore` | Present | Runtime data, secrets, dependencies, upstream checkouts, and Bench-local state are excluded. |
| `apps.json` | Present | Pinned source manifest exists from Phase 0. |
| `compose.yaml` | Present | Local development topology exists. |
| `docker/` | Present | Dockerfile, config, and entrypoint placeholder exist. |
| `scripts/` | Present | Bootstrap, CI, migration, and operations folders exist. |
| `tests/` | Present | Contract, E2E, performance, and security placeholders exist. |
| `infrastructure/` | Present | Development, staging, production, modules, monitoring, and policies placeholders exist. |
| `apps/` | Present | Upstream source checkouts and `university_erp` skeleton exist. |

## Source And Runtime Separation

- Product custom code belongs in `apps/university_erp`.
- Upstream source checkouts under `apps/frappe`, `apps/erpnext`, `apps/education`, `apps/crm`, `apps/payments`, and `apps/frappe_docker` are ignored by the product repository and must remain clean unless an ADR approves an upstream patch.
- Local Bench runtime output is ignored: `sites/`, `logs/`, `env/`, generated config/log files, local SQL backups, archives, and local secrets.
- Local fake/sandbox provider defaults are defined in `.env.example`; real provider credentials remain blocked by ADR-0012 and later explicit approval.

## Verification

Commands run from repository root:

```powershell
npm.cmd run check:repo
npm.cmd run lint:docs
docker compose config
```

All checks passed after the P1.1 update.
