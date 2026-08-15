# P7.1 Test Suite and CI Completion

Date: 2026-08-14

## Database credential repair

The retained local MariaDB volume contained site users restricted to an old backend container IP. The local users for `p21.localhost` and `erp.localhost` were granted access from the Compose network while retaining their existing passwords and database ownership. No application data or named volumes were deleted.

## Verification passed

- `p21.localhost` migration completed successfully.
- `bench --site p21.localhost run-tests --app university_erp` passed: 3 integration tests, 0 failures.
- `npm.cmd run lint:docs` passed.
- `npm.cmd run check:repo` passed, including the repository secret-pattern scan.
- `git diff --check` passed.
- The CI workflow and bootstrap-capable app-test runner are present at `.github/workflows/ci.yml` and `scripts/ci/run-app-tests.ps1`.

## Gate result

P7.1 is complete for the local repository gate. Browser E2E, accessibility, performance, vulnerability scanning, SBOM/signing and production-provider verification remain later release-candidate work.

## Next step

Proceed to P7.2 Security and Privacy Hardening.
