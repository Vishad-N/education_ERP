# P6.1 Initial Portal Slice - Applicant and Guardian PWA

Date: 2026-08-13

Site: `p21.localhost`

Status: In progress

## Scope Added

- Added a Vue 3 and TypeScript guardian admission portal under `apps/university_erp/frontend`.
- Added Vite configuration that builds into `apps/university_erp/university_erp/public/frontend`.
- Added a Frappe web route at `/guardian-admission`.
- Added PWA manifest and service worker assets.
- Added English/Hindi language switching for the primary application flow.
- Added mobile-first screens for guardian registration, class selection, child details, document upload placeholders, payment status safety text and application status.
- Added local draft autosave with online/offline status messaging.

## Verification Commands

```powershell
npm.cmd run build
docker compose exec backend bench --site p21.localhost clear-cache
```

The frontend build passed from `apps/university_erp` and emitted:

- `university_erp/public/frontend/assets/index.js`
- `university_erp/public/frontend/assets/index.css`
- `university_erp/public/frontend/manifest.webmanifest`
- `university_erp/public/frontend/service-worker.js`

The local route and assets returned HTTP 200:

```text
http://p21.localhost:8000/guardian-admission
http://p21.localhost:8000/assets/university_erp/frontend/assets/index.js
http://p21.localhost:8000/assets/university_erp/frontend/assets/index.css
```

## Known Follow-Up

`bench build --app university_erp` linked app assets successfully, then failed while running the app build command inside the Linux container because the current `node_modules` tree was installed on Windows and is missing Rollup's Linux optional native package. The already-built assets are served after the link step, but the container build path needs a Linux dependency install or clean container-side install before P6.1 can be treated as complete.

## Exit Gate Status

Not complete. The implementation is an initial working slice; the P6.1 exit gate still requires validated guardian mobile flow completion with minimal staff help, real portal/API integration, browser/mobile visual verification, and Frappe UI dependency integration.
