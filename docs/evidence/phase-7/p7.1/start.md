# P7.1 Test Suite and CI Start

Date: 2026-08-14

## Scope opened

P7.1 is now in progress. This first slice establishes executable automated coverage for the student portal access boundary and a repeatable CI entry point for repository validation, migration, and the custom-app test suite.

## Added artifacts

- `apps/university_erp/university_erp/tests/test_portal_api.py` verifies token hashing, invalid-token rejection, and the scoped snapshot contract when P6.2 synthetic proof data is loaded.
- `scripts/ci/run-app-tests.ps1` runs site migration and `bench run-tests --app university_erp` in the local Compose backend.
- `.github/workflows/ci.yml` runs documentation lint, repository policy checks, Compose validation, backend image build, migration and app tests.

## Verification

Repository-level execution completed locally:

- `npm.cmd run lint:docs`
- `npm.cmd run check:repo`
- `git diff --check`

The Docker-backed app-test job is defined but not claimed as passed in this evidence. A local elevated attempt was blocked by retained-volume database credentials and the transient container's missing editable app installation; the runner now bootstraps an ephemeral CI site and installs the custom app before testing. Browser E2E, permission matrix, migration upgrade, performance, security scan, SBOM and vulnerability gates remain open for the rest of P7.1.

## Next action

Extend the suite with permission and migration regression tests, then run the full Docker-backed test job and record its output before marking P7.1 complete.
