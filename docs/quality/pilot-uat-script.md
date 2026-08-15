# Pilot UAT Script

Use only with synthetic data or an approved masked pilot dataset. Record tester, date, site, role, expected result, actual result and defect ID for every case.

| ID | Role | Scenario | Expected result |
|---|---|---|---|
| UAT-001 | Institution Administrator | Configure institution and campus scope | Records save only within the permitted site/scope |
| UAT-002 | Academic Officer | Publish a program offering and intake | Published version is visible to admissions; locked versions cannot be edited |
| UAT-003 | Admissions Officer | Create application, validate documents and review eligibility | Required documents and explainable eligibility state are enforced |
| UAT-004 | Finance Officer | Generate demand, record partial payment and reconcile | Invoice, payment, receipt and outstanding balance agree |
| UAT-005 | Registrar | Convert accepted applicant | Exactly one Student and enrollment identity are created |
| UAT-006 | Applicant/Guardian | Save draft, upload document and resume | Draft is recoverable; private document reaches scan state |
| UAT-007 | Student/Guardian | View dues, download receipt and start payment | Access is student-scoped and duplicate payment retry is safe |
| UAT-008 | System Manager | Review audit event and restricted export request | Actor, action, entity and correlation ID are present; unapproved export is blocked |
| UAT-009 | Finance approver | Reconcile migration opening balances | Source totals, target totals and GL totals match or exceptions are signed |

## Sign-off

- Product owner: pending
- Institution owner: pending
- Finance owner: pending
- Security/privacy owner: pending
- Migration operator: pending
