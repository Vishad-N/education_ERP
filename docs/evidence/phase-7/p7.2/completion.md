# P7.2 Security and Privacy Completion

Date: 2026-08-14

## Completed local controls

- Baseline role matrix documented for portal, admissions, academic, finance, registrar, institution administration and system management roles.
- Restricted identifiers are masked by default.
- Privacy exports require approval; unmasked exports require a privileged role.
- Retention expiry calculation rejects invalid retention periods and is covered by tests.
- Provider webhook signatures use constant-time comparison, replay rejection and correlation IDs.
- Private document download URLs are limited to a maximum 900-second TTL.
- Audit event records carry actor, action, entity and correlation ID without sensitive payloads.

## Verification

- `bench --site p21.localhost run-tests --app university_erp`: 8 tests passed, 0 failures.
- `npm.cmd run check:repo`: passed.
- `npm.cmd run lint:docs`: passed.
- `git diff --check`: passed.

## Gate result

P7.2 is complete for the local application security/privacy gate. Production MFA enforcement, full Frappe role-permission integration tests, scheduled retention jobs, dependency/container vulnerability scans, penetration testing and human security review remain mandatory release-candidate work.

## Next step

Proceed to P7.3 Migration and UAT.
