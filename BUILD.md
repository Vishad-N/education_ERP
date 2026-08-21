# BUILD.md — Remaining work to make this production-ready

**Purpose:** What is built today, what is missing for a real school, and the work still required before live admissions, live fees, and live messages.  
**Audience:** Founder, engineering, and the first pilot school.  
**Governing docs:** `AGENTS.md`, `PROJECT_IMPLEMENTATION_PLAN.md`, `docs/current-implementation-status.md`.  
**Current official next step:** `P9.1` controlled pilot launch — **blocked** until credentials, UAT, and a signed image are approved.  
**Status of this product:** Staging demo only. **Not production-ready.**

This file is the remaining-build contract. Do not treat a DocType, a Railway URL, or a marketing paragraph as a live school capability.

---

## 1. What “production-ready” means here

A real township high school can:

1. Open an admission cycle with their own classes, seats, documents, and fees.
2. Let guardians apply on a phone in English and Hindi without a technician.
3. Take a real ₹ application fee and later tuition through Razorpay (or an approved cashier path).
4. Store documents privately, scan them, and verify them.
5. Run eligibility, merit, seats, confirmation, and create **one** student / **one** enrolment.
6. Raise bills that match ERPNext, collect, receipt, refund, and reconcile.
7. Send SMS/email the school is legally allowed to send (DLT templates).
8. Restrict staff by role; keep an audit trail; restore from backup.

Until every item below is Done or explicitly deferred in writing, do not put real student data or real money on this system.

---

## 2. What is already built

### 2.1 Product foundations (custom app `university_erp`)

| Area | Built | Proven where |
|---|---|---|
| Institution / campus / class / intake / timetable clash | Yes | Local proofs |
| Identity, documents, consent, correction, duplicate candidate | Yes | Local proofs |
| CRM lead + versioned form + draft save/resume | Yes | Local + Railway after seed |
| Eligibility, immutable merit, seat matrix, offers | Yes | Local; Railway with staff forms |
| Confirmation + idempotent student conversion | Yes | Local; Railway if offer is Accepted+Submitted |
| Fee policy, demand, invoice, payment, refund, GL pattern | Yes | Local proofs |
| Guardian portal EN/HI six-step PWA | Yes | Railway (with known payment gap) |
| Student portal snapshot, receipt PDF, fake OTP | Yes | Local; Railway needs access token |
| Fake Razorpay / MSG91 / SMTP / R2 / ClamAV adapters | Yes | Local + Railway fake path |

### 2.2 Platform

- Frappe v16 + ERPNext + Education + CRM + Payments in one image.
- Railway staging: `web`, MariaDB, Redis, combined scheduler/worker.
- Health: `/api/method/university_erp.api.health.ready`.
- One site per institution (architecture decided; fleet automation not built).

### 2.3 Explicitly out of Phase 1 (do not build for first go-live)

LMS, exams, report cards, daily attendance, hostel, transport, library, HR/payroll, accreditation analytics.

---

## 3. Gaps found in live staging use

These blocked a real-looking demo. They will block a real school.

| Gap | What happens today | Remaining build |
|---|---|---|
| Application fee never completes | Waived on live staging (`application_fee.required=false`) | Optional Razorpay later via `application_fee_mode=gateway` |
| Upload looked “broken” | Draft save used a Lost CRM status (`New Lead` missing) | Use CRM status **New**; keep Open-status helper; do not depend on fake R2 for this bug |
| CRM board hides portal leads | Status `New Lead` is not a CRM column | Always create leads as **New**; optional CRM view for admissions |
| Handoff error “Student Applicant is required” | Staff set Status to Application Created before Submit | Validate only after submit (local fix not deployed); Desk UI should hide Status or keep it Pending |
| Confirm error “submitted accepted seat offer” | Staff submitted offer as **Offered** | Portal/Desk action **Accept offer**; do not require clerks to know DocType states |
| `/desk/crm-lead` “does not open” | Must be logged in; login lands on Education portal | Default staff home = Desk/admissions workspace |
| Class list is hard-coded 6–9 | Vue options, not live Program Offerings | Load published offerings from API |
| No staff workspace | Awesome Bar only | Role workspaces: Admissions, Registrar, Fees |
| Seed data was missing on Railway | Proof data lived only on `p21.localhost` | Repeatable demo/pilot seed in the image or a one-shot job |
| Local fixes not on Railway | Payment/handoff/lead-status patches sit in git | **Rebuild and deploy one image** before the next client demo |

---

## 4. Remaining to build (real-school backlog)

Priority: **P0** blocks any live parent. **P1** blocks a safe pilot. **P2** blocks a comfortable school. **P3** is later.

### P0 — Make the live path work without a developer

Must ship and **deploy** before another client demo or any parent phone.

- [x] Deploy current `university_erp` to Railway web (waived fee live 2026-08-21, digest `sha256:193b6341…`).
- [x] Application fee waived by default (`application_fee_mode=waived`). Guardian can finish without Razorpay. Set `application_fee_mode=gateway` in site config when a real gateway is approved.
- [ ] When a school wants online pay: Razorpay order → checkout → **server webhook** → Paid. Never mark Paid from a browser redirect alone.
- [x] Visible errors on upload and draft save in the guardian portal.
- [x] Staff command buttons: **Create Application**, **Accept Seat**, **Confirm Admission**, **Create Student** (`university_erp.api.admissions`).
- [x] Office **Admit Student** on Student Applicant runs eligibility → merit → seat → confirm → student, counter fee demand, and a portal access link. No payment gateway.
- [ ] Dedicated school setup wizard UI (seed script still used for first masters).
- [x] Idempotency keys, offer dates, eligibility explanation, and conversion date generated by the system.

### P1 — Real integrations and money

- [ ] Institution-owned Razorpay (ADR-0012): order, capture, webhook HMAC, refund, settlement import.
- [ ] Cloudflare R2 private bucket, signed URLs, quarantine prefix (replace FakeR2).
- [ ] Malware scan on upload (replace Fake ClamAV).
- [ ] MSG91 + DLT PE/sender/templates (replace Fake MSG91).
- [ ] Hostinger SMTP with school From address, bounce handling (replace Fake SMTP).
- [ ] Notification outbox: after-commit events, retries, throttle, pause, audit (application received, offer, receipt).
- [x] Counter fee demand at conversion (no Sales Invoice until gateway). **Record Counter Payment** posts an offline receipt without Razorpay.
- [ ] Gateway path: demand → Sales Invoice → Razorpay/cashier → ERPNext Payment Entry.
- [ ] Duplicate payment / webhook replay tests on the deployed site.

### P1 — School operations UX

- [ ] Admissions workspace: today’s applications, document queue, eligibility, merit, seats.
- [ ] Registrar workspace: confirm, convert, identity, corrections.
- [ ] Fees workspace: demands, outstanding, receipts, refunds, mismatches.
- [ ] Offer accept/reject/expire from guardian portal (Desk **Accept Seat** works).
- [ ] Richer application status after submit (status page exists; live school updates still staff-side).
- [x] Student portal access issued at conversion and **Issue Portal Link** on Student.
- [ ] Hindi review by a native speaker; low-literacy pass on a cheap Android.
- [x] Dynamic program/class from published offerings.

### P1 — Permissions, privacy, audit

- [ ] Map role matrix to Frappe Role Permission Manager (Admissions, Academic, Finance, Registrar, Institution Admin). Named staff users; no shared Administrator for school work.
- [ ] MFA for finance, merit publish, refund, export.
- [ ] Private file ACL + time-limited URLs; no documents in email.
- [ ] Masked exports default; unmasked export needs approval.
- [ ] Maker-checker: intake change, merit publish, concession, refund, admission cancel.

### P1 — Hosting for a real school

Railway is **staging**. Production baseline is Hostinger VPS + Cloudflare (ADR). Remaining:

- [ ] One signed image digest; same digest in staging then production.
- [ ] Dedicated web, websocket, short worker, long worker, scheduler (not combined replica).
- [ ] TLS, WAF, rate limits on login, OTP, upload, pay.
- [ ] Secrets in a manager; rotate staging admin password; no secrets in git.
- [ ] Off-host encrypted backup + PITR; monthly restore evidence; site encryption key backed up.
- [ ] Health, queue, backup, payment-webhook, and 5xx alerts.

### P2 — Data, testing, go-live

- [ ] School master-data load: classes, seats, fee heads, users, Hindi labels.
- [ ] Migration rehearsal with masked data; finance sign-off on opening balances.
- [ ] Browser E2E: apply → handoff → merit → accept → confirm → student → pay tuition.
- [ ] Concurrent seat-accept and duplicate-webhook tests.
- [ ] Penetration test; no unaccepted high findings.
- [ ] UAT signed: product, institution, finance, security, operations (`UAT-001`–`UAT-009`).
- [ ] Training + support contacts + known-limitations sheet for the school.

### P3 — After first school is stable

- [ ] Site provisioning for the next institution.
- [ ] 20–25 sites per measured pod.
- [ ] Do not start LMS/exams/attendance unless a change request moves them into scope.

---

## 5. Suggested build sequence

Do not skip. Fake adapters stay until the named owner supplies credentials.

```text
1. Deploy current patches to Railway (P0)
2. Staff command UI + payment complete on staging (P0)
3. Human UAT on staging with synthetic data
4. Razorpay sandbox + R2 + SMTP sandbox (P1) — needs user approval
5. MSG91/DLT after PE/sender ownership (P1)
6. Hostinger production image, same digest as staging (P1)
7. Restore drill + permission tests + load smoke (P2)
8. P9.1: one school, controlled parents, hypercare
```

Each step needs: tests, evidence under `docs/evidence/`, and a rollback note. No live SMS, live cards, or identifiable students without explicit user approval (`AGENTS.md` approval boundary).

---

## 6. Definition of Done for production

A school is allowed live only if:

- [ ] One image digest is signed and matches staging and production
- [ ] Guardian can finish apply → documents → **real or sandbox** pay without Desk help
- [ ] Staff can admit without typing Status or idempotency keys
- [ ] Seat accept cannot exceed capacity under two concurrent clerks
- [ ] Conversion cannot create a second student
- [ ] Fee totals equal ERPNext GL for a sample of students
- [ ] Documents are private and scanned
- [ ] SMS/email use approved templates only
- [ ] Backup restore was demonstrated in the last 30 days
- [ ] UAT signatures exist
- [ ] Phase 2 modules are not shown as available

---

## 7. Owners and blockers

| Need | Owner | Blocks |
|---|---|---|
| Razorpay merchant, settlement, refunds | Institution finance | Live fees |
| DLT PE, sender, templates | Institution / platform (ADR-0012) | Live SMS |
| SMTP domain / From identity | Institution | Live email |
| Cloudflare DNS, WAF, R2 | Operations | Files + public hostname |
| Hostinger VPS | Operations | Production hosting |
| Named UAT signers | Institution | P9.1 |
| Aadhaar / retention legal answers | Institution legal | Identity fields |

Engineering can finish P0 and most P1 UX/permissions without those credentials. Engineering cannot finish live pay/SMS/files without them.

---

## 8. Related files

| File | Use |
|---|---|
| `docs/current-implementation-status.md` | What exists vs what is proven |
| `PROJECT_IMPLEMENTATION_PLAN.md` | Official phase steps (next: P9.1) |
| `docs/operations/production-readiness-checklist.md` | Sign-off checklist |
| `docs/quality/pilot-uat-script.md` | UAT-001–009 |
| `docs/product/CLIENT_DEMO_WALKTHROUGH.md` | Staging demo only |
| `docs/adr/0012-institution-owned-provider-accounts.md` | Who owns Razorpay/DLT/SMTP |

---

*Written 2026-08-19. Update this file when a P0/P1 item is deployed and evidenced, not when a DocType is merely added.*
