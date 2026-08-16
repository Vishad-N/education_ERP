# Education ERP - Feature Overview

This document summarizes the key capabilities of the Education ERP in client-friendly language. It is intended for marketing, demos, proposals and stakeholder briefings.

## Product Positioning

Education ERP is a modern, institution-ready platform for schools, colleges and universities that need to manage admissions, student records, fees, documents and compliance in one connected system.

The platform is built on Frappe, ERPNext, Frappe Education and a custom `university_erp` application. It combines proven ERP foundations with education-specific workflows for Indian institutions, including guardian-first admissions, bilingual portal experiences and finance-grade fee reconciliation.

## Key Benefits

- One connected system for admissions, student identity, academic setup and fees.
- Mobile-first applicant and guardian portal designed for low digital literacy users.
- English and Hindi support for pilot-facing portal workflows.
- Strong fee and accounting foundation using ERPNext as the financial source of truth.
- Safe online payment handling with duplicate retry protection.
- Document upload, scan-state tracking and verification workflow foundations.
- Role-based access for admissions, academics, finance, registrar, institution administration and system management.
- Audit-friendly records for sensitive actions and compliance workflows.
- Migration templates and reconciliation process for onboarding existing institution data.
- Multi-institution architecture using one Frappe site per independent institution.

## Applicant And Guardian Portal

The applicant and guardian portal is designed for families who may be using a mobile phone, unstable internet connection or limited digital support.

Features include:

- Mobile-first application flow.
- Guardian registration using basic contact details.
- Applicant/child information capture.
- Step-by-step admission journey.
- English and Hindi language switching.
- Local draft autosave.
- Offline draft recovery foundation.
- Server-side draft save and resume.
- Document upload flow for admission documents.
- Document scan-status integration.
- Application fee payment initiation.
- Safe retry messaging to avoid duplicate payments.
- Final application status view.

The portal is intended to reduce staff dependency during admissions and make the first interaction easier for guardians.

## Student And Guardian Portal

The student/guardian portal provides a scoped view of student-facing information.

Features include:

- Secure token-based portal access foundation.
- Student and guardian profile snapshot.
- Outstanding dues view.
- Receipt list.
- Receipt PDF download.
- Document status view.
- Notices and announcements view.
- Student fee payment initiation.
- Payment status polling.
- Duplicate payment callback protection.
- Bilingual portal view foundation.

## Admissions Management

The admissions foundation supports the journey from enquiry to confirmed admission.

Features include:

- CRM lead to application handoff.
- Versioned admission application forms.
- Save/resume application drafts.
- Student applicant creation.
- Explainable eligibility evaluation.
- Published eligibility rule sets.
- Merit configuration.
- Immutable merit runs.
- Ranked merit entries.
- Seat matrix and category capacity foundations.
- Seat allocation rounds.
- Accepted and waitlisted seat offers.
- Offer capacity protection.
- Admission confirmation workflow.
- Applicant-to-student conversion.
- One student and one enrollment identity per accepted applicant.

## Academic And Institution Setup

The platform includes foundational academic and institution configuration for the pilot journey.

Features include:

- Institution hierarchy for university, campus, college and department structures.
- Institution structure versioning.
- Academic year and term setup.
- Academic session policy.
- Academic calendar.
- Program versioning.
- Program offerings.
- Class offerings.
- Academic sections.
- Curriculum versions.
- Curriculum course rows.
- Subject offerings.
- Intake and category capacity records.
- Faculty assignment.
- Timetable slots and entries.
- Timetable conflict rejection foundation.

These capabilities provide the structure required before admissions and fee assignment can work correctly.

## Student Identity And Documents

The student identity foundation is designed to protect long-term institutional records.

Features include:

- Applicant identity foundation.
- Student identity profile.
- Guardian relationship records.
- Communication consent records.
- Student status history.
- Student category history.
- Correction request workflow foundation.
- Duplicate candidate review.
- Immutable identity issuance.
- Student document records.
- Document requirement matrix.
- Document scan result records.
- Document verification workflow foundation.
- Document replacement request.
- Document expiry review.
- Privacy export request.
- Student data access audit.

## Fees, Payments And Accounting

The fee system is designed around ERPNext accounting so that finance records remain reconcilable.

Features include:

- Education fee codes.
- Fee policy versions.
- Fee installments.
- Fee demand generation.
- Concession, scholarship, fine and waiver calculation foundation.
- ERPNext Sales Invoice integration.
- Student Fee Demand records.
- Online payment attempt records.
- Offline approved payment foundation.
- Receipt number generation.
- ERPNext Payment Entry posting.
- Duplicate payment event protection.
- Refund request foundation.
- Credit note creation.
- Refund Payment Entry posting.
- Provider settlement import foundation.
- Fee general ledger reconciliation records.
- Mismatch rejection for settlement and GL reconciliation.

## Integrations Foundation

The platform includes fake provider adapters that allow the team to test provider behavior safely before real credentials are approved.

Current integration foundations include:

- Fake Razorpay adapter for payment order, capture, refund and settlement behavior.
- Fake MSG91 adapter for SMS delivery testing.
- Fake SMTP adapter for email testing.
- Fake R2 adapter for private object storage testing.
- Fake ClamAV adapter for clean and infected document scan states.
- Webhook signature verification foundation.
- Replay protection foundation.
- Idempotency key support for retry-safe operations.
- Timeout and provider failure handling foundations.

Real production integrations are intentionally gated until provider ownership, credentials and release approvals are complete.

## Security And Privacy

The system includes early security and privacy controls for a safer pilot foundation.

Features include:

- Role matrix for major operational roles.
- Permission metadata on custom DocTypes.
- Restricted identifier masking foundation.
- Privacy export approval requirement.
- Privileged unmasked export control.
- Private document URL time limit foundation.
- Webhook signature verification.
- Webhook replay rejection.
- Correlation IDs for important events.
- Sanitized audit events.
- Retention expiry calculation validation.
- Repository secret-pattern checks.

## Migration And UAT Readiness

The project includes migration and testing assets for moving toward pilot readiness.

Features include:

- CSV templates for students.
- CSV templates for guardians.
- CSV templates for fee opening balances.
- No-write migration validator.
- Required-column checks.
- Duplicate source ID checks.
- Reference validation.
- Monetary value validation.
- Immutable checksum evidence.
- Count reconciliation process.
- Reference reconciliation process.
- Fee opening balance reconciliation process.
- Pilot UAT script with nine role-based scenarios.
- Pre-production human testing checklist.
- Testing-team CSV with expected results and blank result columns.

## Deployment And Scaling Direction

The architecture is designed for controlled growth.

Deployment and scaling features include:

- One Frappe site per independent institution.
- Shared immutable application image direction.
- Railway-first staging artifacts.
- Portable Docker Compose production baseline for Hostinger or similar VPS hosting.
- AWS ECS/Fargate baseline for future portability.
- Role-based container entrypoint for web, WebSocket, scheduler and workers.
- Database/cache readiness probes.
- Health check foundations.
- Managed environment variable templates.
- Queue separation for short and long workers.

## Current Readiness Statement

The application has a strong verified local foundation and is ready to continue pre-production testing. It is not yet production-ready.

Before pilot go-live or real provider traffic, the project still requires:

- Completed P6.1 applicant/guardian human testing.
- Published admission form seed data on Railway/pre-production.
- Full Hindi review and correction of any untranslated portal text.
- Real phone document upload testing.
- Payment retry and callback testing in sandbox/pre-production.
- Named pilot UAT execution.
- Production-sized masked migration rehearsal.
- Finance reconciliation sign-off.
- Security/privacy sign-off.
- Production provider credentials and callback configuration.
- Backup, restore, monitoring and release-readiness evidence.

## Ideal Demo Story

For a client demo, present the product journey in this order:

1. Configure institution and academic structure.
2. Publish admission form and program offering.
3. Guardian applies from mobile portal.
4. Documents are uploaded and scanned.
5. Eligibility and merit are reviewed.
6. Seat offer is issued.
7. Admission is confirmed.
8. Applicant becomes a student.
9. Fee demand and invoice are generated.
10. Payment is collected and receipted.
11. Finance reconciles payment, refund, settlement and GL.
12. Student/guardian views dues, receipts and documents from the portal.

## Marketing Message

Education ERP helps institutions move from fragmented admission files, manual fee tracking and disconnected student records to a structured digital platform with admissions, identity, fees, documents and audit controls working together.

It is built for real institutional operations, not just form collection: every major workflow is designed to connect back to permissions, audit history, accounting reconciliation and future production deployment controls.
