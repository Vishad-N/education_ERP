# Pilot Scope Baseline

- Status: Phase 0 baseline
- Date: 2026-08-09
- Pilot type: small-township high school
- Languages: English and Hindi
- Primary users: guardians, applicants/students, admission staff, accounts staff, academic administrators, system administrators

## In scope for pilot

- Institution, campus/school, academic session, class/grade, section, subject, and intake setup.
- Applicant enquiry capture and counsellor/admission follow-up using Frappe CRM foundations.
- Guardian-first application flow with save/resume.
- Applicant/student identity, guardian records, category/status history, correction workflow, and duplicate-candidate detection.
- Document requirement matrix, private upload metadata, scan status, verification, rejection, and replacement workflow.
- Eligibility, scrutiny, merit, seat offer, waitlist, admission confirmation, and idempotent student conversion.
- Day-1 fee setup, demand generation, installments, concession/scholarship/fine workflow, online/offline collection, receipts, refunds, settlement import, and ERPNext GL reconciliation pattern.
- Event-driven SMS/email notifications through an outbox using fake/sandbox adapters until live credentials are approved.
- Permission, audit, export, and reporting controls for all in-scope workflows.
- Mobile-first bilingual portal for registration, application, document upload, payment status, receipts, and application/admission status.

## Explicitly deferred unless approved later

- Full LMS/course content delivery.
- Full examination/evaluation/report-card engine.
- Daily attendance.
- Hostel, transport, library, HR/payroll, and accreditation analytics.
- Production DNS, live payment processing, real SMS/email traffic, and migration of identifiable student data.

## Planning workload

Initial planning values are documented in `docs/architecture/capacity-plan.md`. These values are assumptions for engineering and load-test profiles, not contractual capacity guarantees. They must be replaced with measured pilot data before production scale decisions.

## Acceptance baseline

Pilot acceptance requires:

- every in-scope requirement linked to BRD IDs in `docs/requirements/traceability.md`;
- automated tests for business rules, permissions, audit behavior, and failure paths;
- finance reconciliation evidence against ERPNext accounting documents;
- English/Hindi UX review and low-literacy usability evidence;
- signed approval from product, institution, finance, security/privacy, engineering, and operations owners before go-live.
