# Client demo — step by step (Railway staging)

Staging is prepared. A published Class 6 form exists. Use this as your speaker sheet.

**Do not put passwords on a slide.** Desk login is Administrator; the password is `SITE_ADMIN_PASSWORD` in your local file `secrets/railway-education-erp-backend.env`.

---

## 0. Open these two windows first

| Window | URL | How to set it |
|---|---|---|
| **Phone (parent)** | [https://web-production-7580e.up.railway.app/guardian-admission](https://web-production-7580e.up.railway.app/guardian-admission) | Incognito / a second browser profile. DevTools → device toolbar → **390px** width. In the console run: `localStorage.removeItem("university_erp_guardian_application")` then refresh. |
| **Office (you)** | [https://web-production-7580e.up.railway.app/login](https://web-production-7580e.up.railway.app/login) | Normal browser. Sign in as Administrator. |

Health check (optional, before the client sits down):

- [https://web-production-7580e.up.railway.app/api/method/university_erp.api.health.ready](https://web-production-7580e.up.railway.app/api/method/university_erp.api.health.ready) must show `"status":"ready"`.

Upload files (already in the repo, both under 5 MB):

- `scripts/demo/sample-birth-certificate.pdf`
- `scripts/demo/sample-child-photo.png`

Or use any PDF/JPG/PNG from your phone.

---

## 1. One-line opening (30 seconds)

> “I will show the same child twice: first as a parent on a phone, then as the school office. Apply → review → seat → student → fee.”

Do not start in Desk.

---

## 2. Parent applies (6 minutes)

**Link:** [Guardian admission](https://web-production-7580e.up.railway.app/guardian-admission)

| Step | What you do | What you say |
|---|---|---|
| Language | Toggle **हिन्दी** then back to **English** | “Same form in Hindi and English.” |
| Register | Mobile `9876543210`, guardian `Anita Sharma`, child `Rohan Sharma` → **Next** | “Only mobile and names to start. No training.” |
| Saved | Point at **Saved / Saved to school** | “If the network drops, the draft stays on the phone.” |
| Class | Class 6, previous school `Govt School` → **Next** | “They pick the class we opened.” |
| Details | DOB, address, tick consent → **Next** | “Consent is required, not hidden.” |
| Documents | Upload the PDF and the photo | “Private upload. Only PDF, JPG or PNG under 5 MB.” |
| Payment | **Pay ₹500**, then tap it again | “Second tap does not create a second order.” |
| Status | **Check payment status** if needed, then **Finish** | “The family is done. The school takes over.” |

If payment stays “started”, that is fine. Say: “Money is confirmed by the server, not by this button.” Continue to Desk.

---

## 3. School sees the same child (4 minutes)

Stay logged in. Use the Awesome Bar (search at the top) or these links.

**Enquiries (CRM)**  
[https://web-production-7580e.up.railway.app/app/crm-lead](https://web-production-7580e.up.railway.app/app/crm-lead)

Open the newest lead named **Rohan Sharma**.

**Application draft**  
[https://web-production-7580e.up.railway.app/app/admission-application-draft](https://web-production-7580e.up.railway.app/app/admission-application-draft)

Open the draft linked to that lead. Status should be **Draft**. Show the saved answers.

**Documents**  
[https://web-production-7580e.up.railway.app/app/admission-application-document](https://web-production-7580e.up.railway.app/app/admission-application-document)

Show **Scan Passed**.

**Application fee**  
[https://web-production-7580e.up.railway.app/app/admission-payment-attempt](https://web-production-7580e.up.railway.app/app/admission-payment-attempt)

Show the ₹500 attempt (**Pending** or **Paid**).

**Say:** “This did not stay in WhatsApp. Enquiry, form, papers and fee are already in the school system.”

### Turn enquiry into an official application

**Link:** [New CRM Application Handoff](https://web-production-7580e.up.railway.app/app/crm-application-handoff/new)

Fill:

- CRM Lead: the Rohan lead  
- Program: `Class 6`  
- Academic Year: `2026-27`  
- Academic Term: `2026-27 (Term 1)`  
- Form Version: `AAF-DEMO-C6-2026.1`  
- Application Draft: the draft you just opened  
- Handoff Date: today  

**Save**, then **Submit**.

Open the Student Applicant it created:  
[https://web-production-7580e.up.railway.app/app/student-applicant](https://web-production-7580e.up.railway.app/app/student-applicant)

**Say:** “If I submit this twice, the system still keeps one applicant.”

---

## 4. Eligibility, merit, seat (4 minutes)

You do not need to invent rules live. They are already published. Open them, then create the evaluation / offer for Rohan.

**Eligibility rule (already published)**  
[https://web-production-7580e.up.railway.app/app/eligibility-rule-set/ERS-DEMO-C6-2026.1](https://web-production-7580e.up.railway.app/app/eligibility-rule-set/ERS-DEMO-C6-2026.1)  
Rule: score **40 or more**.

**New evaluation**  
[https://web-production-7580e.up.railway.app/app/eligibility-evaluation/new](https://web-production-7580e.up.railway.app/app/eligibility-evaluation/new)

- Student Applicant: Rohan  
- Rule Set: `ERS-DEMO-C6-2026.1`  
- Score: `88`  
- Result: `Eligible`  
- Explanation JSON: `{"minimum_score":40,"score":88}`  

Save. **Say:** “The system checks the result against the published rule.”

**Merit configuration (already active)**  
[https://web-production-7580e.up.railway.app/app/merit-configuration/DEMO-MERIT-C6](https://web-production-7580e.up.railway.app/app/merit-configuration/DEMO-MERIT-C6)

**New merit run**  
[https://web-production-7580e.up.railway.app/app/merit-run/new](https://web-production-7580e.up.railway.app/app/merit-run/new)

- Configuration: `DEMO-MERIT-C6`  
- Program: `Class 6`  
- Academic Year: `2026-27`  
- Published On: now  
- Status: Draft  

Save. Add a **Merit Entry** (from the run, or [new merit entry](https://web-production-7580e.up.railway.app/app/merit-entry/new)): applicant Rohan, rank `1`, score `88`, category `General`.  
**Submit** the merit run.

**Say:** “After publish, this list cannot be silently rewritten.”

**Seat matrix (2 seats, already locked)**  
[https://web-production-7580e.up.railway.app/app/admission-seat-matrix/ASM-DEMO-C6-2026-General](https://web-production-7580e.up.railway.app/app/admission-seat-matrix/ASM-DEMO-C6-2026-General)

**New allocation round**  
[https://web-production-7580e.up.railway.app/app/seat-allocation-round/new](https://web-production-7580e.up.railway.app/app/seat-allocation-round/new)

- Merit Run: the run you submitted  
- Round Number: `1`  
- Status: Draft → Save → **Submit** (becomes Published)

**New seat offer**  
[https://web-production-7580e.up.railway.app/app/seat-offer/new](https://web-production-7580e.up.railway.app/app/seat-offer/new)

- Allocation Round: the round above  
- Seat Matrix: `ASM-DEMO-C6-2026-General`  
- Merit Entry: Rohan’s entry  
- Student Applicant: Rohan  
- Status: `Accepted`  
- Accepted On: today  

Save → **Submit**.

**Say:** “Only two seats. A third accept is blocked.”

---

## 5. Confirm admission and create the student (3 minutes)

**New confirmation**  
[https://web-production-7580e.up.railway.app/app/admission-confirmation/new](https://web-production-7580e.up.railway.app/app/admission-confirmation/new)

- Seat Offer: the accepted offer  
- Tick **Document Gate Passed**  
- Tick **Fee Gate Passed**  
- Confirmed On: today  

Save → **Submit**. Status becomes **Confirmed**.

**New conversion**  
[https://web-production-7580e.up.railway.app/app/admission-student-conversion/new](https://web-production-7580e.up.railway.app/app/admission-student-conversion/new)

- Admission Confirmation: the one you submitted  
- Conversion Date: today  

Save → **Submit**.

Then open:

- Student list: [https://web-production-7580e.up.railway.app/app/student](https://web-production-7580e.up.railway.app/app/student)  
- Program Enrollment: [https://web-production-7580e.up.railway.app/app/program-enrollment](https://web-production-7580e.up.railway.app/app/program-enrollment)

**Say:** “One child becomes one student and one enrolment. Running this again does not create a second child.”

---

## 6. Fees (3 minutes)

**Published fee policy (₹10,000)**  
[https://web-production-7580e.up.railway.app/app/education-fee-policy-version/EFP-DEMO-C6-2026.1](https://web-production-7580e.up.railway.app/app/education-fee-policy-version/EFP-DEMO-C6-2026.1)

For a live client meeting you can **show the policy** and say:

> “After the student exists, accounts raises a bill from this policy. That bill is also an invoice in the school ledger. Payment creates a receipt. A refund needs approval.”

If you have time and accounting accounts are set, create a **Student Fee Demand** from [new demand](https://web-production-7580e.up.railway.app/app/student-fee-demand/new) linked to a submitted Sales Invoice. If invoice setup is not ready, **do not improvise**. Stay on the published policy.

---

## 7. Student page (2 minutes)

After conversion, create access:

[New Student Portal Access](https://web-production-7580e.up.railway.app/app/student-portal-access/new)

- Student: Rohan  
- Token Hash: paste a SHA-256 hash of a secret you invented (the family gets the **raw** secret, not the hash)  
- Status: Active  
- Expires On: a date next month  

Family link:

[https://web-production-7580e.up.railway.app/student-portal?access=YOUR-RAW-TOKEN](https://web-production-7580e.up.railway.app/student-portal?access=YOUR-RAW-TOKEN)

If you skip creating a token, still open the empty page so they see the family UI:

[https://web-production-7580e.up.railway.app/student-portal](https://web-production-7580e.up.railway.app/student-portal)

Published notice already exists: `Welcome to Township High School`.

---

## 8. If time is short — 10-minute cut

1. Parent form (steps Register → Status).  
2. Desk: CRM Lead + draft + documents.  
3. Open these four prepared records only (do not create new ones):

| What | Link |
|---|---|
| School | [DEMO-SCHOOL](https://web-production-7580e.up.railway.app/app/education-institution-node/DEMO-SCHOOL) |
| Published form | [AAF-DEMO-C6-2026.1](https://web-production-7580e.up.railway.app/app/admission-application-form-version/AAF-DEMO-C6-2026.1) |
| Two seats | [ASM-DEMO-C6-2026-General](https://web-production-7580e.up.railway.app/app/admission-seat-matrix/ASM-DEMO-C6-2026-General) |
| Fee policy ₹10,000 | [EFP-DEMO-C6-2026.1](https://web-production-7580e.up.railway.app/app/education-fee-policy-version/EFP-DEMO-C6-2026.1) |

4. Close: “Parent finishes on the phone. School cannot oversell seats. Fees are a real bill, not a notebook.”

---

## Prepared records (already on Railway)

Use these if search is slow.

| Record | Name | Desk link |
|---|---|---|
| School | Township High School | [DEMO-SCHOOL](https://web-production-7580e.up.railway.app/app/education-institution-node/DEMO-SCHOOL) |
| Campus | Main Campus | [DEMO-CAMPUS](https://web-production-7580e.up.railway.app/app/education-institution-node/DEMO-CAMPUS) |
| Academic year | 2026-27 | [2026-27](https://web-production-7580e.up.railway.app/app/academic-year/2026-27) |
| Term | Term 1 | [2026-27 (Term 1)](https://web-production-7580e.up.railway.app/app/academic-term/2026-27%20(Term%201)) |
| Program | Class 6 | [Class 6](https://web-production-7580e.up.railway.app/app/program/Class%206) |
| Program version | PV-Class 6-2026 | [PV-Class 6-2026](https://web-production-7580e.up.railway.app/app/program-version/PV-Class%206-2026) |
| Offering | DEMO-C6-2026 | [DEMO-C6-2026](https://web-production-7580e.up.railway.app/app/program-offering/DEMO-C6-2026) |
| Class | Class 6 | [DEMO-C6-CLASS](https://web-production-7580e.up.railway.app/app/class-offering/DEMO-C6-CLASS) |
| Section | Section A | [DEMO-C6-A](https://web-production-7580e.up.railway.app/app/academic-section/DEMO-C6-A) |
| Category | General | [General](https://web-production-7580e.up.railway.app/app/student-category/General) |
| Intake (2 seats) | PI-DEMO-C6-2026-00003 | [PI-DEMO-C6-2026-00003](https://web-production-7580e.up.railway.app/app/program-intake/PI-DEMO-C6-2026-00003) |
| Published form | AAF-DEMO-C6-2026.1 | [AAF-DEMO-C6-2026.1](https://web-production-7580e.up.railway.app/app/admission-application-form-version/AAF-DEMO-C6-2026.1) |
| Eligibility | ERS-DEMO-C6-2026.1 | [ERS-DEMO-C6-2026.1](https://web-production-7580e.up.railway.app/app/eligibility-rule-set/ERS-DEMO-C6-2026.1) |
| Merit config | DEMO-MERIT-C6 | [DEMO-MERIT-C6](https://web-production-7580e.up.railway.app/app/merit-configuration/DEMO-MERIT-C6) |
| Seat matrix | ASM-DEMO-C6-2026-General | [ASM-DEMO-C6-2026-General](https://web-production-7580e.up.railway.app/app/admission-seat-matrix/ASM-DEMO-C6-2026-General) |
| Fee policy | EFP-DEMO-C6-2026.1 | [EFP-DEMO-C6-2026.1](https://web-production-7580e.up.railway.app/app/education-fee-policy-version/EFP-DEMO-C6-2026.1) |
| Notice | Welcome to Township High School | [Student Portal Notice list](https://web-production-7580e.up.railway.app/app/student-portal-notice) |

---

## What to tell the client at the end

> “This is a working staging school. Application fee is a test payment, not a live bank charge. Next step with you is your real classes, seats and fee heads, then a pilot with sandbox payments.”

Do not claim 100 schools, live Razorpay, or attendance/exams.

---

## If something is empty tomorrow

The site is slow under cold start. Refresh once. If the guardian page says no published form, run:

```text
C:\msys64\ucrt64\bin\python.exe scripts\demo\seed_railway_demo.py
```

That script is idempotent. It will not duplicate the school.
