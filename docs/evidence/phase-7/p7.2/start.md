# P7.2 Security and Privacy Start

Date: 2026-08-14

## Initial slice

- Added reusable correlation IDs for verified provider webhooks.
- Added restricted-identifier masking utility.
- Preserved constant-time HMAC verification and replay rejection.
- Added private-object signed URL TTL negative coverage.
- Added the baseline role matrix at `docs/security/role-matrix.md`.
- Added automated tests for masking, webhook signature/replay behavior, private-object URL limits, export approval/privilege, retention expiry and audit correlation.

## Verification

The initial security test slice passed through the Docker-backed Frappe test command: 8 `university_erp` tests passed with 0 failures. Full MFA enforcement, Frappe permission matrix integration, production retention jobs, dependency/container scans and human security review remain open.

## Next action

Wire correlation IDs into provider request/audit logs and add negative Frappe permission tests for private documents and restricted student fields.
