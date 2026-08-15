# P7.3 Migration and UAT Start

Date: 2026-08-14

## Initial slice

- Added a no-write CSV trial-load validator with schema, duplicate, reference and opening-balance checks.
- Added masked/synthetic migration templates for students, guardians and finance opening balances.
- Added a role-based pilot UAT script covering academic, admissions, finance, identity, portal, security and reconciliation journeys.

## Verification

The validator was run in the backend container before any import and passed:

- 3 template files validated;
- 1 student, 1 guardian and 1 opening-balance row;
- INR 1,000.00 opening-balance total;
- no duplicate, reference or amount errors.

Its synthetic templates are the only data supplied in this repository; no real student data is imported.

Full isolated-site trial load, source-to-target count/reference reconciliation, finance sign-off and human UAT signatures remain open.

## Next action

Run the validator against the supplied templates, then add isolated-site reconciliation output and signed UAT evidence after approved testers execute the script.
