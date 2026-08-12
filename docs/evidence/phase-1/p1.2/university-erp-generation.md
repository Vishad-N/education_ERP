# P1.2 Evidence - `university_erp` App Generation

Date: 2026-08-09

Status: Complete

## Scope

`university_erp` is present as the custom Frappe application for project-owned domain logic. The app uses Frappe-compatible package metadata and the standard generated files required for installation on a site.

## Verified Artifacts

- `apps/university_erp/pyproject.toml`
- `apps/university_erp/university_erp/__init__.py`
- `apps/university_erp/university_erp/hooks.py`
- `apps/university_erp/university_erp/modules.txt`
- `apps/university_erp/university_erp/patches.txt`
- `apps/university_erp/university_erp/config/__init__.py`
- `apps/university_erp/university_erp/patches/__init__.py`
- `apps/university_erp/university_erp/templates/__init__.py`
- `apps/university_erp/university_erp/templates/pages/__init__.py`
- `apps/university_erp/university_erp/www/.gitkeep`
- `apps/university_erp/university_erp/university_erp/.frappe`

## Installation Result

The app was installed on the local `erp.localhost` site after registering it in Bench `sites/apps.txt` and installing the app package in editable mode.

Installed apps reported by `bench --site erp.localhost list-apps`:

```text
frappe         16.19.0 HEAD
erpnext        16.22.0 HEAD
payments       0.0.1   HEAD
education      16.0.1  HEAD
crm            1.72.0  HEAD
university_erp 0.0.0   UNVERSIONED
```

## Notes

- Upstream app source was not modified.
- `university_erp` is currently version `0.0.0`; Phase 2 should introduce release/version discipline before product feature work.
- The local app is tracked by the project repository instead of as a nested Git repository, so bootstrap uses `env/bin/pip install --editable apps/university_erp` rather than `bench setup requirements university_erp`.
