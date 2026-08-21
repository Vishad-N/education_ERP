# Education ERP — User Guide, Admin Guide, and Demo Script

**Audience:** guardians, applicants, students, school staff, and demo presenters  
**Platform:** Frappe Desk (staff) + bilingual Vue portals (families)  
**Custom app:** `university_erp` on Frappe v16, ERPNext v16, Frappe Education, and Frappe CRM  
**Status:** staging-ready foundations. Human UAT and live providers are still deferred. The product is **not production-ready**.

This file is the single operating guide. It describes what is implemented today, who does each step, the exact record types involved, and a timed demo flow you can present without inventing screens that do not exist.

---

## 1. How to use this document

| You are… | Start at |
|---|---|
| A guardian or student | [Part A — User Guide](#part-a--user-guide) |
| School staff (admissions, academics, finance, registrar) | [Part B — Admin Guide](#part-b--admin-guide) |
| Presenting the product | [Part C — Demo Presentation Flow](#part-c--demo-presentation-flow) |
| Looking up a screen or DocType | [Part D — Feature catalogue](#part-d--feature-catalogue) |

Staff work in **Frappe Desk**. Families work in two public pages:

| Surface | Path | Who |
|---|---|---|
| Guardian admission portal | `/guardian-admission` | Parent/guardian applying for a child |
| Student / guardian portal | `/student-portal?access=<token>` | Enrolled student or guardian with a time-limited link |
| Staff Desk | `/login` then Desk search | Trained staff |

Staging example (Railway): `https://web-production-7580e.up.railway.app`. Local development typically uses `erp.localhost` or `p21.localhost`.

Do not put passwords in this guide. Desk credentials live in the operator secret store (`SITE_ADMIN_PASSWORD` / local `.env`). Never demonstrate production credentials on a projector.

---

## 2. What the product does

The Education ERP runs one connected admission-to-fee journey for an Indian school or college:

1. The institution configures its hierarchy, academic year, program, class, intake, fee policy, and published application form.
2. A guardian starts an application on a phone, in English or Hindi.
3. The system creates a CRM enquiry and a saveable draft.
4. The guardian uploads documents and starts the application fee.
5. Staff hand the enquiry to a Student Applicant, check eligibility, publish merit, and allocate seats without overselling capacity.
6. After documents and fees pass, staff confirm admission and convert the applicant into **exactly one** Student and **exactly one** Program Enrollment.
7. Finance generates a fee demand that posts a Sales Invoice in ERPNext, collects online or offline payment, issues a receipt, and can refund and reconcile to the General Ledger.
8. The family later opens a scoped student portal to see dues, receipts, documents, and notices.

ERPNext remains the accounting source of truth. Custom records hold education rules; they do not keep a second ledger.

### 2.1 Who uses it

| Persona | Typical tool | Main jobs |
|---|---|---|
| Guardian / applicant | `/guardian-admission` | Register, apply, upload, pay application fee, see status |
| Student / guardian (enrolled) | `/student-portal` | View dues, pay fees, download receipts, read notices |
| Institution Administrator | Desk | Institution tree, users, published structure |
| Academic Officer | Desk | Year, program, class, section, timetable, intake |
| Admissions Officer / counsellor | Desk + CRM | Enquiry, handoff, documents, eligibility |
| Merit Operator / Approver | Desk | Merit configuration, publish run, seat offers |
| Registrar | Desk | Confirmation, conversion, identity, corrections |
| Finance Officer / Cashier | Desk | Demands, collection, receipts, refunds, reconciliation |
| Auditor / System Manager | Desk | Audit, exports, roles, technical health |

### 2.2 What is in the current build vs later

**In the current build (can be shown in a demo):**

- Institution and academic masters, including timetable clash rejection
- Student identity, documents, consent, correction, duplicate review, privacy export request
- CRM lead → application handoff → Student Applicant
- Guardian PWA: bilingual steps, local autosave, server draft, document scan, application-fee order
- Eligibility, immutable merit, seat matrix, offers, waitlist, capacity lock
- Admission confirmation gates and idempotent student conversion
- Fee policy, demand + Sales Invoice, online/offline payment, receipt, refund, settlement import, GL check
- Student portal snapshot, receipt PDF, payment retry, fake OTP contract
- Role matrix, identifier masking, webhook replay rejection, correlation IDs

**Deferred (do not claim these in a live demo):**

- Real Razorpay / MSG91 / SMTP / Cloudflare R2 traffic
- Daily attendance, examinations, LMS, hostel, transport, library, HR
- Full Frappe Role Permission Manager sign-off and browser UAT
- Hindi human review and low-literacy usability sign-off
- Production DNS, signed image publish, production cutover

Payments and scans in staging use **fake adapters**. Money is not taken from a real bank account. OTP in the student portal is the local test code `246810`.

---

## 3. End-to-end product flow

This is the single story the product implements. Every later section is a zoom-in on one box.

```text
Institution + academic year + program + class + intake + fee policy
        │
        ▼
Published application form  ──►  Guardian portal  ──►  CRM Lead + Application Draft
        │                                                 │
        │                                                 ├─ upload documents (scan)
        │                                                 └─ application fee order (₹500)
        ▼
CRM Application Handoff  ──►  Student Applicant (submitted draft)
        │
        ▼
Eligibility Evaluation  ──►  Merit Run (immutable)  ──►  Seat Allocation Round
        │
        ▼
Seat Offer (Offered / Accepted / Waitlisted)
        │
        ▼
Admission Confirmation (document gate + fee gate)
        │
        ▼
Admission Student Conversion
        │
        ├─ Student
        ├─ Program Enrollment
        └─ Student Identity Issuance
                │
                ▼
Fee Policy ──► Student Fee Demand + Sales Invoice
                │
                ├─ Online payment (portal or Desk)
                ├─ Offline cashier payment
                ├─ Student Fee Payment + Payment Entry + receipt
                ├─ Refund + credit note (if approved)
                └─ Settlement import + GL reconciliation
                        │
                        ▼
Student Portal Access token  ──►  /student-portal (dues, receipts, documents, notices)
```

Hard rules that must never be broken in a demo or in production:

- Accepted seats cannot exceed the seat-matrix capacity.
- One provider payment maps to at most one posted accounting result.
- Conversion creates at most one Student and one enrollment.
- A published merit run cannot be cancelled or overwritten.
- Fee demand net amount must equal the submitted Sales Invoice.

---

# Part A — User Guide

This part is for families. Staff should still read it so they can help a guardian on a phone.

## A1. Guardian admission portal

**Open:** `/guardian-admission`  
**Languages:** English and हिन्दी (toggle in the header)  
**Device:** mobile-first. Works as a PWA (can be added to the home screen).  
**Network:** if the phone goes offline, the draft stays on the device. When the network returns, it syncs to the school.

### A1.1 Before you start

Have ready:

- Guardian 10-digit mobile number
- Guardian name and child name
- Child date of birth and home address
- Previous school name (if any)
- Birth certificate (PDF, JPG, or PNG, under 5 MB)
- Child photo (PDF, JPG, or PNG, under 5 MB)
- A way to pay the **₹500 application fee** (in staging this is a simulated payment)

The portal only appears if staff have published at least one **Admission Application Form Version**. If you see “No published admission form is available,” the school has not opened admissions yet.

### A1.2 The six steps

The left (or top) step list is the whole journey. You can go back to a finished step. You cannot skip ahead.

#### Step 1 — Register (mobile)

1. Enter a 10-digit mobile number.
2. Enter the guardian name.
3. Enter the child’s name.
4. Tap **Next**.

The first successful save creates:

- a **CRM Lead** (enquiry) for the child
- an **Admission Application Draft**
- a **resume token** stored only on this phone (the school stores a hash, not the raw token)

If you close the browser and come back on the same phone, the form reloads from local storage and resumes the same draft.

Validation: all three fields are required; mobile must be exactly 10 digits.

#### Step 2 — Class

1. Choose the class applying for: Class 6, 7, 8, or 9 (pilot list).
2. Optionally enter the previous school.
3. Tap **Next**.

#### Step 3 — Details

1. Enter date of birth.
2. Enter home address.
3. Tick the consent box: the school may check these details for admission.
4. Tap **Next**.

Validation: date of birth, address, and consent are required.

#### Step 4 — Documents

1. Upload **Birth certificate**.
2. Upload **Child photo**.
3. Wait until each file is accepted.

What happens in the background:

- the file is stored as a private object
- a malware scan runs (fake ClamAV in staging)
- only **Scan Passed** files unlock the next step
- PDF, JPG, and PNG only; maximum 5 MB

If upload fails, stay on this step and try again. Do not create a second application.

#### Step 5 — Application fee (currently no online pay)

Online payment is **off** until Razorpay is connected. The screen says the school can collect at the counter. Tap **Next**.

When a gateway is enabled later (`application_fee_mode=gateway`), this step will collect ₹500 online.

#### Step 6 — Status

You see a short summary:

- child name
- class
- documents complete / pending
- payment complete / pending

Message: the application is saved; the school will check details and update this page.

Tap **Finish**.

### A1.3 What the guardian does *not* do

The guardian portal does **not** currently:

- log in with a password or OTP (access is the phone + resume token)
- accept or reject a seat offer
- see merit rank
- pay tuition (that is the student portal after enrollment)
- switch between multiple children on one account (one draft per device session)

Staff complete eligibility, merit, offer, confirmation, and conversion in Desk.

### A1.4 If something goes wrong

| What you see | What to do |
|---|---|
| Offline banner | Keep filling. The phone copy is saved. Sync retries when online. |
| “Phone copy saved; school sync will retry” | Stay on the same phone. Do not start a new application. |
| Document rejected / scan failed | Upload a clearer PDF/JPG/PNG under 5 MB. |
| Payment started, not complete | Use **Check payment status**. Do not pay again. |
| Form will not go Next | Read the red error: missing mobile, consent, documents, or payment. |
| New phone / cleared browser | Ask the school to help. The resume token lived on the old phone. |

---

## A2. Student and guardian portal (after admission)

**Open:** `/student-portal?access=<access-token>`  
The school issues a time-limited **Student Portal Access** link. Bookmarking the URL on the same phone stores the token locally.

If the token is missing, expired, or revoked, the page says the link is invalid and you must request a new one.

### A2.1 What you see

| Section | Meaning |
|---|---|
| Student | Child name and student ID. Access expiry date. |
| Fee dues | Open **Student Fee Demand** rows in status `Generated`, with amount and due date. |
| Receipts | Posted **Student Fee Payment** rows. **Download** saves a PDF. |
| Notices | Published **Student Portal Notice** rows for All Students or Guardians. |
| Documents | Student documents with verification status and expiry (if any). |

Language toggle: English / हिन्दी.

### A2.2 Pay a due

1. On a due row, tap **Pay**.
2. The portal creates one provider order for that demand. Tapping again reuses the same order.
3. After the (staging) capture, staff-side accounting posts one **Payment Entry** and one **Student Fee Payment**.
4. Refresh or reopen the portal to see the new receipt.

If the invoice is already fully paid, the server refuses a second charge.

### A2.3 Download a receipt

Tap **Download** on a receipt. The PDF is generated only if that receipt belongs to the student on this access token. Another student’s receipt ID will be rejected.

### A2.4 OTP (staging only)

The API can issue a local OTP challenge. Delivery is **not** real SMS. The test code is `246810`. After five wrong attempts the challenge locks. Do not use this as a production login.

---

# Part B — Admin Guide

Staff work in Frappe Desk after `/login`. Use **Awesome Bar** (search at the top) to open any DocType by name, for example `Education Institution Node` or `Student Fee Demand`.

Do not give routine school staff the **System Manager** role. Use the baseline roles below.

## B1. Desk basics that apply everywhere

- **Save** stores a draft. **Submit** locks the business action (confirm, convert, post payment).
- Many masters use status: `Draft` → `Published` / `Approved` / `Active` → `Locked` / `Retired` / `Cancelled`.
- **Version** (track changes) is on for critical records. Do not hard-delete history.
- Never change a submitted financial document in place. Reverse with a credit note / refund.
- Never set a payment to Paid because a browser redirected to “success.” Confirm the provider event and the Payment Entry.
- Guest portal APIs are public but scoped by resume token or access token. Do not paste tokens into tickets or chat.

### B1.1 Baseline roles

| Role | May do | Must not do |
|---|---|---|
| Applicant / Guardian | Own portal draft, documents, dues, receipts | Any staff record or export |
| Admissions Officer | Enquiries, applications, documents, eligibility | Merit publish, refunds, concessions, role changes |
| Academic Officer | Academic masters, offerings, intake, sections | Financial posting, unmasked identity export |
| Finance Officer | Demands, invoices, payments, reconciliation | Unapproved refunds, write-offs, concessions |
| Registrar | Student identity, confirmation, conversion, corrections | Credential admin, unrestricted exports |
| Institution Administrator | Institution-scoped setup and users | Bypass audit or site isolation |
| System Manager | Technical configuration | Routine business approvals |

Site isolation is absolute: one institution = one Frappe site = one database.

### B1.2 Office buttons (click these; do not type Status)

Hard-refresh Desk after each deploy (`Ctrl+Shift+R`).

| Screen | Button |
|---|---|
| CRM Lead | **Create Application** |
| Admission Application Draft | **Create Application** |
| CRM Application Handoff | **Create Application** |
| Student Applicant | **Evaluate Eligibility**, **Admit Student** |
| Eligibility Evaluation | **Evaluate** |
| Merit Run | **Publish Merit**, **Allocate Seats** |
| Seat Allocation Round | **Allocate Seats** |
| Seat Offer | **Accept Seat**, **Confirm Admission** |
| Admission Confirmation | **Confirm Admission**, **Create Student** |
| Admission Student Conversion | **Create Student** |
| Student | **Issue Portal Link** |
| Student Document | **Verify** |
| Student Fee Demand | **Record Counter Payment** |

**Admit Student** on the applicant is the full remaining path without Razorpay.

### B1.3 Suggested Desk search list (pin these)

Institution: `Education Institution Node`, `Institution Structure Version`  
Academic: `Academic Year`, `Academic Term`, `Academic Session Policy`, `Academic Calendar`, `Program`, `Program Version`, `Program Offering`, `Class Offering`, `Academic Section`, `Curriculum Version`, `Subject Offering`, `Program Intake`, `Faculty Assignment`, `Timetable Slot`, `Timetable Entry`  
CRM / admissions: `CRM Lead`, `Admission Application Form Version`, `Admission Application Draft`, `CRM Application Handoff`, `Student Applicant`, `Eligibility Rule Set`, `Eligibility Evaluation`, `Merit Configuration`, `Merit Run`, `Admission Seat Matrix`, `Seat Allocation Round`, `Seat Offer`, `Admission Confirmation`, `Admission Student Conversion`  
Identity: `Student`, `Student Identity Profile`, `Student Identity Issuance`, `Guardian`, `Student Guardian Relationship`, `Communication Consent`, `Student Correction Request`, `Duplicate Candidate`  
Documents: `Student Document Type`, `Document Requirement Matrix`, `Student Document`, `Document Verification`, `Admission Application Document`  
Fees: `Education Fee Code`, `Education Fee Policy Version`, `Student Fee Demand`, `Student Fee Payment`, `Student Fee Refund`, `Fee General Ledger Reconciliation`, `Sales Invoice`, `Payment Entry`  
Portal: `Student Portal Access`, `Student Portal Notice`

---

## B2. Institution setup (do this first)

**Owner:** Institution Administrator  
**Records:** `Education Institution Node`, `Institution Structure Version`

### B2.1 Build the tree

Create nodes from the top down. The code is the document name (uppercased).

| Node type | Parent required? | Typical example |
|---|---|---|
| University | No (root only) | The school trust / university |
| Campus | University or higher group | Main campus |
| College | Campus (or higher group) | High school / college |
| Department | College | Science / Primary |

Rules:

- Only a University may have no parent.
- Parent must be a **group** node (`is_group`).
- Child type must sit below the parent (University → Campus → College → Department).
- `inactive_from` cannot be before `active_from`.
- Status: `Active`, `Inactive`, `Locked`.
- Link `company` (ERPNext Company) and currency on the node that owns accounting.

Do not delete a node that transactions already reference. Deactivate or lock it.

### B2.2 Publish a structure version

Create **Institution Structure Version** against the university node. Status: `Draft` → `Published`. This is the snapshot admissions and reporting should treat as the live hierarchy.

---

## B3. Academic year, calendar, program, class, intake

**Owner:** Academic Officer

Do this in order. Later admissions and fees depend on these names.

### B3.1 Year, term, policy, calendar

1. **Academic Year** (Education) — e.g. `2026-27`.
2. **Academic Term** under that year.
3. **Academic Session Policy** — `Draft` → `Published` → `Locked` when admissions start.
4. **Academic Calendar** linked to the year and institution node. Status: `Draft` / `Published` / `Locked` / `Cancelled`.
5. **Academic Calendar Day** rows: `Working`, `Holiday`, `Exam`, `Event`.

### B3.2 Program chain

Keep these separate. Do not clone a new Program every year.

```text
Program                  reusable identity (e.g. Class 6 / B.A.)
  → Program Version      published academic structure for a year
    → Curriculum Version + Curriculum Course rows
      (Core / Elective / Ability Enhancement / Skill Enhancement / Value Added)
  → Program Offering     that version offered on a campus for a session
    → Class Offering     the class instance
      → Academic Section section (e.g. 6-A) + optional class teacher
      → Subject Offering course taught in that class
```

Statuses you will use:

| Record | Statuses |
|---|---|
| Program Version | Draft / Published / Cancelled |
| Program Offering | Draft / Open / Locked / Closed |
| Class Offering | (configured per record; lock after timetable is live) |
| Academic Section | Active / Inactive / Locked |
| Subject Offering | Draft / Open / Locked / Closed |

A subject offering must be **Open** or **Locked** before you can timetable it.

### B3.3 Intake and reservation

1. Create **Student Category** values you will use (e.g. General).
2. Create **Program Intake** on the Program Offering.
3. Add **Category Intake** child rows. Category capacities **must sum to Total Capacity**.
4. Submit. Status becomes `Approved`. Cancel sets `Cancelled`. Later lock when the cycle must not change.

### B3.4 Faculty and timetable

1. Create an **Instructor**.
2. Create **Faculty Assignment** (Active) on a Subject Offering.
3. Create **Timetable Slot** (weekday + time).
4. Create **Timetable Entry** (code is the name) linking subject, section, slot, instructor, optional room.

Clash detection rejects:

- same section in the same slot
- same faculty in the same slot
- same room in the same slot

Cancelled entries are ignored. Use this in the demo to show the system blocking a double-book.

---

## B4. Open admissions (forms, CRM, handoff)

**Owners:** Institution Administrator (form), Admissions Officer / counsellor (enquiry)

### B4.1 Publish the application form

Create **Admission Application Form Version**:

- Program and Academic Year
- `form_schema` JSON (fields the portal/API may expose)
- Status **Published**

The guardian portal lists only Published forms. Retire old versions; do not edit a live published form in place if families already started drafts.

### B4.2 How an enquiry appears

Two equally valid paths:

**Path 1 — Guardian starts on the portal**  
`save_application_draft` creates CRM Lead + Admission Application Draft (`Draft`). Counsellor sees the lead in Frappe CRM / Desk.

**Path 2 — Counsellor captures a walk-in**  
Create **CRM Lead** in CRM (name, mobile, email, status). Then create the draft and handoff yourself.

CRM is for pre-application relationship only. It is not the permanent student master.

### B4.3 Review the draft

Open **Admission Application Draft**:

| Field | Meaning |
|---|---|
| Form Version | Published form used |
| CRM Lead | Enquiry |
| Status | Draft / Submitted / Abandoned |
| Draft Payload | JSON of guardian answers |
| Student Applicant | Filled after handoff |
| Resume Token Hash | Cannot be used to impersonate the family |

Also open **Admission Application Document** (scan status) and **Admission Payment Attempt** (`Pending` / `Paid`).

### B4.4 Handoff to Student Applicant

Create **CRM Application Handoff**:

- CRM Lead
- Program, Academic Year, Academic Term
- Form Version and Application Draft
- Handoff date

Submit. The system:

1. Creates or reuses **Student Applicant** (Education)
2. Marks the CRM Lead converted
3. Sets the draft to **Submitted** and stamps `submitted_on`
4. Sets handoff status to **Application Created**

Rules:

- One active handoff per CRM Lead
- Repeat submit is idempotent on the applicant email
- After submit, the guardian can no longer edit that draft

---

## B5. Documents and student identity

**Owners:** Document Verifier / Admissions Officer / Registrar

### B5.1 Configure what is required

1. **Student Document Type** (e.g. Birth certificate) — Active.
2. **Document Requirement Matrix** — program / category / Active.
3. **Document Rejection Reason** catalogue.

### B5.2 Student document lifecycle

```text
Uploaded → Scanning → Scan Passed / Scan Failed
                 → Pending Verification → Verified / Rejected / Expired / Replaced
```

Staff records:

| DocType | When to use |
|---|---|
| Student Document | The file metadata for an applicant or student |
| Document Scan Result | Passed / Failed scan evidence |
| Document Verification | Verified or Rejected + reason |
| Document Replacement Request | Draft → Approved / Rejected |
| Document Expiry Review | Open → Expired / Resolved |

Portal uploads during application land on **Admission Application Document**, not yet the permanent Student Document. After conversion, registrar/staff attach or migrate verified files onto the student.

Private files only. Do not email full documents.

### B5.3 Identity after the child exists as an applicant or student

| DocType | Purpose |
|---|---|
| Student Identity Profile | Canonical profile (Draft / Active / Locked / Merged / Cancelled) |
| Student Identity Issuance | Immutable student number + enrollment number (submit to Issue) |
| Student Guardian Relationship | Link to Education Guardian |
| Communication Consent | Channel consent history |
| Student Category History | Category changes with dates |
| Student Status Change | Lifecycle history |
| Student Correction Request | Draft → Approved / Rejected / Cancelled |
| Duplicate Candidate | Open → Confirmed Duplicate / Dismissed — **never silent merge** |
| Student Data Access Log | View / Export / Mask / Correction |
| Student Privacy Export Request | Draft → Approved / Rejected; default **masked** export |

Correction of issued IDs requires an approved correction request. Full Aadhaar must not be a default identifier; if collected under a lawful basis, mask it and keep it off lists, logs, and URLs.

---

## B6. Eligibility, merit, and seats

**Owners:** Admissions Officer (eligibility), Merit Operator / Approver (merit and seats)

### B6.1 Eligibility

1. Publish **Eligibility Rule Set** for the program/year. `rules_json` must include `minimum_score`.
2. Create **Eligibility Evaluation** for the Student Applicant:
   - score
   - result `Eligible` or `Ineligible`
   - `explanation_json` that includes `minimum_score` so the decision is explainable

The server recomputes the expected result from the published rules. A mismatched result is rejected. Only Published rule sets can be used.

### B6.2 Merit (immutable)

1. **Merit Configuration** — Active, with scoring / tie-breaker JSON.
2. **Merit Run** against that configuration, program, and year.
3. Add **Merit Entry** rows (applicant, category, scores, rank).
4. Submit the run. Status becomes **Published**. `published_on` is required.

You **cannot cancel** a published merit run. To correct it, create a new run and mark the old one **Superseded**. Regeneration is a new approved version, never an overwrite.

### B6.3 Seat matrix and offers

1. **Admission Seat Matrix** — Program Offering + Student Category + capacity. Status `Draft` / `Locked` / `Retired`.
2. **Seat Allocation Round** on a Published Merit Run. Publish the round (`Draft` / `Published` / `Closed`).
3. **Seat Offer** per applicant in that round:
   - `Offered` — issued
   - `Accepted` — requires `accepted_on`; capacity is locked with a row lock
   - `Waitlisted`
   - `Expired` / `Cancelled`

Rules:

- Offers require a **Published** allocation round
- One offer per applicant per round
- Submit of an **Accepted** offer fails if accepted count already equals capacity

This is the slide where you show “the system will not sell the 21st seat.”

---

## B7. Confirm admission and create the student

**Owner:** Registrar / Admission Approver

### B7.1 Admission Confirmation

Create **Admission Confirmation** on a **submitted Accepted** Seat Offer.

Before submit you must have:

- `document_gate_passed`
- `fee_gate_passed`
- `confirmed_on`

Status becomes `Confirmed`. Waitlisted offers are rejected. Missing gates are rejected.

### B7.2 Admission Student Conversion

Create **Admission Student Conversion** on that submitted confirmation. Set `conversion_date`. Submit.

The system will:

1. Create or reuse **Student** from the applicant
2. Create or reuse submitted **Program Enrollment**
3. Create or link **Student Identity Profile**
4. Issue **Student Identity Issuance** (student number + enrollment number)
5. Set Student Applicant `application_status` to `Admitted`
6. Set conversion status to `Converted`

Repeating conversion returns the same student and enrollment. A second active conversion for the same applicant is rejected.

After this, issue **Student Portal Access** (hash the raw token, store only the hash, set `expires_on`) and send the family `/student-portal?access=<raw-token>`.

---

## B8. Fees, collection, refunds, reconciliation

**Owner:** Finance Officer / Cashier / Finance Approver  
**Accounting truth:** ERPNext Sales Invoice, Payment Entry, credit note, General Ledger

### B8.1 Configure fee policy

1. **Fee Category** (Education) if needed.
2. **Education Fee Code** — Draft / Active / Retired.
3. **Education Fee Policy Version** — program, year, fee code, amounts. Publish it (`Draft` / `Published` / `Retired`).
4. **Education Fee Installment** child/related rows if the policy is split.
5. **Student Fee Adjustment** for Concession / Scholarship / Fine / Waiver (`Draft` / `Approved` / `Rejected`). Gross fee stays visible; net is derived.

Net formula enforced on the demand:

```text
net = gross − concession − scholarship + fine − waiver
```

Net cannot be negative. Generated demands must have a Sales Invoice whose grand total equals net.

### B8.2 Generate a demand

1. Ensure the student has a submitted Program Enrollment.
2. Create / generate **Student Fee Demand**:
   - student, enrollment, published policy
   - amounts and due date
   - linked submitted **Sales Invoice**
3. Submit. Status becomes `Generated`.

Do not mark a demand Generated without an invoice.

### B8.3 Collect payment

**Online (portal or Desk):**

1. Create a payment attempt (`Admission Payment Attempt` for application fee, `Student Portal Payment Attempt` or finance collection for tuition).
2. Verify the provider order / capture (fake Razorpay in staging).
3. Create and submit ERPNext **Payment Entry** against the Sales Invoice.
4. Create and submit **Student Fee Payment** (Online) with the same amount and Payment Entry.
5. Receipt number is issued (`FEE-REC-…` if not supplied).

**Offline (cashier):**

1. Collect cash/cheque/UPI at the counter.
2. Post Payment Entry.
3. Submit **Student Fee Payment** with `collection_type = Offline` and `approved_on` filled.

Duplicate `provider + provider_payment_id` is rejected. Browser “success” is not enough.

### B8.4 Refund

1. Create **Student Fee Refund** from the posted payment. Amount > 0.
2. Approve (`approved_on` required). Status `Approved`.
3. Post a return **Sales Invoice** (credit note) and a refund **Payment Entry** for the same amount.
4. Submit the refund. Status becomes `Posted`.

Duplicate provider refund IDs are rejected. Unapproved refunds cannot be posted.

### B8.5 Settlement and GL

1. **Payment Settlement Import** — Imported / Reconciled / Mismatch.
2. **Fee General Ledger Reconciliation** against the demand and Sales Invoice — Draft / Reconciled / Mismatch.

A mismatch must stay visible. Do not force Reconciled when totals disagree.

### B8.6 Application fee vs tuition fee

| Fee | Who pays | Record | Amount in current portal |
|---|---|---|---|
| Application fee | Guardian during apply | Admission Payment Attempt | ₹500 fixed |
| Tuition / school fee | Student portal or cashier | Student Fee Demand + Student Fee Payment | Policy net amount |

Application-fee attempts do not by themselves create the tuition Sales Invoice. Tuition starts after the student exists and finance generates a demand.

---

## B9. Notices, portal access, and helping a family

### B9.1 Notices

**Student Portal Notice**

- Title, message, published_on
- Audience: All Students / Guardians / Staff
- Status: Draft / Published / Archived
- Optional expires_on

Only Published notices for All Students or Guardians appear on `/student-portal`.

### B9.2 Issue or revoke portal access

1. Generate a high-entropy token (do not type a guessable ID).
2. Store **SHA-256 hash** in **Student Portal Access**. `status = Active`, set `expires_on`.
3. Send the family the raw token once, as a link.
4. To cut off access: set status `Revoked` or let it `Expired`.

`last_used_on` updates when the portal loads.

### B9.3 Assisted entry

If a guardian cannot complete the phone form, a counsellor may capture the CRM Lead and draft in Desk. Treat this as assisted entry: keep the guardian’s consent, do not invent documents, and do not mark fees paid without money.

---

## B10. Security, privacy, audit, migration

**Owner:** System Manager / Auditor / Institution Administrator

### B10.1 Daily security habits

- Named accounts, not shared `Administrator`, for school staff
- MFA for finance, merit approvers, auditors, and platform operators (production policy)
- Private files only for applicant/student documents
- Masked exports by default; unmasked export needs an approved **Student Privacy Export Request**
- Webhooks must verify signatures; replayed events are rejected
- Do not log passwords, OTPs, payment signatures, or full Aadhaar

### B10.2 What to show an auditor

- Frappe **Version** on tracked masters and identity
- **Student Data Access Log**
- Payment Provider Event (`Received` / `Processed` / `Duplicate` / `Rejected`)
- Submitted merit runs that cannot be cancelled
- Fee GL reconciliation Reconciled vs Mismatch

### B10.3 Trial migration (synthetic only)

Templates in `docs/operations/migration-templates/`:

- `students.csv`
- `guardians.csv`
- `fee_opening_balances.csv`

Validate with `scripts/migration/validate-trial-load.py`. Do not import identifiable student data without explicit authorization. Opening balances need finance sign-off before posting.

### B10.4 Health checks

```text
GET /api/method/university_erp.api.health.live
GET /api/method/university_erp.api.health.ready
```

Both should return HTTP 200 before a demo.

---

## B11. Recommended operating calendar (one admission cycle)

| When | Who | Action |
|---|---|---|
| T−6 weeks | Institution + Academic | Tree, year, program, class, sections, timetable |
| T−5 weeks | Academic | Intake approved and locked |
| T−4 weeks | Finance | Fee codes and published policy |
| T−3 weeks | Admissions | Publish form, eligibility rules, document matrix |
| T−2 weeks | Admissions | Counsellor training; portal smoke test |
| Cycle open | Guardians | Apply, upload, pay ₹500 |
| Daily | Admissions | Handoff, scrutiny, document verification |
| After close | Merit | Publish merit run; allocation rounds; offers |
| Offer window | Registrar + Finance | Gates, confirmation, conversion, portal links |
| After join | Finance | Generate demands; collect; reconcile |
| Monthly | Finance + Auditor | Settlement import, GL check, access-log sample |

---

# Part C — Demo Presentation Flow

Use this as a 25–35 minute stakeholder demo. One presenter drives the phone (or a narrow browser window). A second window stays on Desk. Use **synthetic** data only.

## C1. Goal of the demo

Leave the room believing three things:

1. A parent with a basic phone can start and finish an application without training.
2. Staff can take that enquiry all the way to a real student record without double-creating anyone.
3. Money is accounted for in ERPNext, including “do not pay twice.”

Do **not** claim live Razorpay, SMS, or production go-live. Say clearly: “This staging build uses safe fake payment and scan adapters so we can show the controls before real money moves.”

## C2. Prep (30 minutes before the room)

1. Confirm `/api/method/university_erp.api.health.ready` is 200.
2. Confirm a **Published** Admission Application Form Version exists.
3. Confirm Academic Year, Program, Program Offering, Class, Student Category, and Intake exist.
4. Confirm a Published Eligibility Rule Set, Merit Configuration, Seat Matrix (small capacity, e.g. 1 or 2), and Fee Policy exist — or be ready to show existing proof records.
5. Log into Desk as a named staff user (not root if you can avoid it).
6. Open a second browser profile or incognito for the guardian so cookies do not mix.
7. Narrow the guardian window to a phone width (~390px).
8. Clear the guardian profile’s `localStorage` if you need a clean “first time” story (`university_erp_guardian_application`).
9. Have a sample PDF and a JPG under 5 MB.
10. Write the student-portal URL pattern on a speaker note: `/student-portal?access=…`

If the site has existing proof data (`P3.1 Proof University`, `EDU-STU-2026-00002`, etc.), you may **fast-forward** staff setup and spend time on the live guardian + conversion + fee story.

## C3. Timed script

### Act 0 — Frame (2 minutes)

**Say:**  
“This is an Education ERP for a township high school that must also work for a university later. Families use a Hindi/English phone portal. Staff use Desk. Accounts use ERPNext so fees are not a spreadsheet.”

**Show:** one slide or the opening of this guide’s flow diagram. Then switch to the live site.

**Do not** tour every DocType.

---

### Act 1 — Guardian applies on a phone (8 minutes)

**URL:** `/guardian-admission`

| Minute | You do | You say |
|---|---|---|
| 0:00 | Toggle English → हिन्दी → English | “Same flow in both languages. Large targets, few fields.” |
| 0:30 | Register: mobile, guardian, child | “We start with mobile and names only. No password yet.” |
| 1:00 | Point at “Saved / Saved to school” | “The form autosaves on the phone and to the school.” |
| 1:15 | Class 6, previous school, Next | “Class list is the school’s published offering, not a free-text mess.” |
| 2:00 | DOB, address, consent | “Consent is a required gate, not a footer.” |
| 2:45 | Upload birth certificate + photo | “Private upload. File type and size checked. Scan must pass.” |
| 4:00 | Pay ₹500, then tap again | “Second tap does not create a second order. That is the duplicate-pay protection.” |
| 5:00 | Check payment status | “Families are told: if money is cut, check status, do not pay again.” |
| 6:00 | Status step | “The family is done. Rank, offer, and admission are school work.” |
| 6:30 | Optional: toggle airplane mode, type, go back online | “Offline draft survives a dropped village network.” |

**If payment stays Pending:** that is acceptable. Explain that capture is server-side and show the **Admission Payment Attempt** in Desk.

---

### Act 2 — Staff see the enquiry (4 minutes)

In Desk:

1. Awesome Bar → **CRM Lead** → open the child just created.
2. Open **Admission Application Draft** — status Draft, payload, linked lead.
3. Open **Admission Application Document** — Scan Passed.
4. Open **Admission Payment Attempt** — order id, status.

**Say:**  
“Nothing the parent typed is trapped in a WhatsApp chat. The counsellor already has an enquiry, a draft, documents, and a fee attempt.”

Then submit **CRM Application Handoff**.

**Show:** Student Applicant created; draft now **Submitted**; lead converted.

**Say:**  
“Handoff is idempotent. If the counsellor clicks twice, we do not create two applicants.”

---

### Act 3 — Eligibility, merit, seat (5 minutes)

Keep this tight. Prefer pre-seeded rules if the clock is short.

1. Open **Eligibility Evaluation** (or create one). Show Eligible + explanation JSON / minimum score.
2. Open a **Published Merit Run** and one **Merit Entry** (rank).
3. Attempt to cancel the merit run if you want the error: *published merit runs are immutable*.
4. Open **Admission Seat Matrix** (capacity 1 or 2).
5. Open **Seat Offer** Accepted. Mention waitlist as the other path.
6. Optional punch: try a second Accepted offer on a full matrix and show the capacity error.

**Say:**  
“Merit is a published snapshot. We never silently rewrite yesterday’s list. Seats cannot be oversold even if two clerks submit at once.”

---

### Act 4 — Confirmation and one student (4 minutes)

1. Open **Admission Confirmation**. Tick document gate + fee gate, set confirmed_on, Submit.
2. Open **Admission Student Conversion**, Submit.
3. Show **Student**, **Program Enrollment** (submitted), **Student Identity Issuance**.
4. Submit conversion again (or explain the proof): same student, same enrollment.

**Say:**  
“This is the permanent identity. Applicant becomes one student and one enrollment. That is what the rest of the school will use for fees and the student portal.”

---

### Act 5 — Fees that an accountant will trust (6 minutes)

1. Open **Education Fee Policy Version** (Published) and the amounts.
2. Open **Student Fee Demand** + linked **Sales Invoice** (submitted, totals match).
3. Show **Student Fee Payment** + **Payment Entry** (online and, if present, offline).
4. Show a receipt number.
5. Open **Student Fee Refund** path or an existing posted refund (credit note + refund Payment Entry).
6. Open **Fee General Ledger Reconciliation** — Reconciled. Mention Mismatch is a first-class status.

**Say:**  
“Education rules live in our app. The money lives in ERPNext. If settlement and the ledger disagree, the system keeps a mismatch instead of hiding it.”

---

### Act 6 — Student portal (4 minutes)

1. Issue or reuse **Student Portal Access**.
2. Open `/student-portal?access=…` on the phone window.
3. Show student name, dues, receipts, notices, documents.
4. Download a receipt PDF.
5. Tap Pay on a due (or show already Paid).
6. Toggle Hindi.

**Say:**  
“After admission the family does not need Desk. They get a time-limited link: dues, pay, receipt, notices. Access can be revoked.”

---

### Act 7 — Close (2 minutes)

Show this table on a slide or verbally:

| Question | Answer in this build |
|---|---|
| Can a low-literacy parent apply? | Yes — six steps, EN/HI, autosave |
| Can seats be oversold? | No — locked capacity |
| Can we rewrite merit? | No — new version only |
| Can we create two students? | No — idempotent conversion |
| Can we double-charge? | No — idempotency keys + unique provider payment |
| Is money in a real ledger? | Yes — Sales Invoice / Payment Entry / GL |
| Is this live production? | Not yet — staging, fake providers, UAT pending |

**Next ask:** authorize human UAT, then real sandbox credentials, then P9.1 pilot.

---

## C4. Demo variants

### C4.1 10-minute executive cut

1. Guardian register → documents → pay (3 min)
2. Handoff → Student Applicant (1 min)
3. Existing merit + accepted offer (1 min)
4. Existing Student + invoice + receipt (2 min)
5. Student portal receipt download (2 min)
6. Close lines (1 min)

### C4.2 45-minute operational workshop

Add after Act 3:

- Create a colliding **Timetable Entry** and show the clash error
- Open **Duplicate Candidate** and state that merge is never silent
- Open **Student Correction Request**
- Walk **Student Privacy Export Request** (masked vs privileged)
- Show `live` / `ready` health endpoints
- Walk the UAT script IDs `UAT-001`–`UAT-009` as a checklist, not a live execution

### C4.3 Things that will stall a room — avoid them

- Logging in as Administrator and wandering Awesome Bar
- Editing unpublished form JSON live
- Real card data or production DNS
- Claiming attendance, exams, or LMS
- Showing Aadhaar or unmasked exports
- Starting a second guardian application “to be safe”

---

## C5. Talking points by audience

| Audience | Emphasize | Skip |
|---|---|---|
| Principal / trustee | Guardian simplicity, one student identity, Hindi | DocType names |
| Admission clerk | CRM lead, draft, documents, handoff | GL theory |
| Accountant | Invoice = demand, Payment Entry, refund, mismatch | Portal CSS |
| IT | Site-per-institution, no core forks, fake-to-real adapters | Merit formula detail |
| Parent representative | Six steps, pay once, receipt PDF | Desk |

---

# Part D — Feature catalogue

Everything below exists as a custom DocType or portal/API behavior in `university_erp`, unless marked as an upstream Education / CRM / ERPNext record that this product reuses.

## D1. Institution and academic

| Feature | Record | What it does |
|---|---|---|
| Institution tree | Education Institution Node | University / Campus / College / Department nested set |
| Structure snapshot | Institution Structure Version | Draft / Published / Cancelled |
| Session rules | Academic Session Policy | Draft / Published / Locked / Cancelled |
| Calendar | Academic Calendar + Academic Calendar Day | Working / Holiday / Exam / Event |
| Program identity | Program (Education) | Reusable program |
| Versioned curriculum | Program Version, Curriculum Version, Curriculum Course | Published structure + course classification |
| Offering | Program Offering, Class Offering, Academic Section | Session-bound class/section |
| Subject | Subject Offering | Draft / Open / Locked / Closed |
| Intake | Program Intake, Category Intake | Category totals must equal capacity |
| Faculty | Faculty Assignment, Instructor (Education) | Active / Inactive |
| Timetable | Timetable Slot, Timetable Entry | Clash detection on section, faculty, room |

## D2. CRM and application

| Feature | Record / API | What it does |
|---|---|---|
| Enquiry | CRM Lead | Counsellor pipeline |
| Form version | Admission Application Form Version | Draft / Published / Retired |
| Guardian draft | Admission Application Draft + `save_application_draft` | Create/update, hashed resume token |
| Resume | `get_application_draft` | Load draft by token |
| Published forms | `get_application_context` | Portal bootstrap |
| Documents | Admission Application Document + `upload_application_document` | Private store + scan state |
| Application fee | Admission Payment Attempt + create/check/confirm APIs | ₹500, idempotent |
| Handoff | CRM Application Handoff | Lead → Student Applicant, submit draft |
| Applicant | Student Applicant (Education) | Official application record |

## D3. Eligibility, merit, seats, conversion

| Feature | Record | What it does |
|---|---|---|
| Rules | Eligibility Rule Set | Published JSON, minimum score |
| Decision | Eligibility Evaluation | Eligible / Ineligible + explanation |
| Scoring config | Merit Configuration | Draft / Active / Retired |
| Merit list | Merit Run, Merit Entry | Publish; cannot cancel |
| Capacity | Admission Seat Matrix | Draft / Locked / Retired |
| Round | Seat Allocation Round | Draft / Published / Closed |
| Offer | Seat Offer | Offered / Accepted / Waitlisted / Expired / Cancelled |
| Confirm | Admission Confirmation | Document + fee gates |
| Convert | Admission Student Conversion | One Student + one Program Enrollment + identity issuance |

## D4. Identity and documents

| Feature | Record | What it does |
|---|---|---|
| Profile | Student Identity Profile | Active identity |
| Numbers | Student Identity Issuance | Immutable student / enrollment numbers |
| Guardian link | Student Guardian Relationship, Guardian | Family link |
| Consent | Communication Consent | Channel consent |
| Histories | Student Category History, Student Status Change | Dated changes |
| Corrections | Student Correction Request | Approval workflow |
| Dedupe | Duplicate Candidate | Review only |
| Document types | Student Document Type, Document Requirement Matrix | What is required |
| Student files | Student Document, Document Scan Result, Document Verification | Scan + verify |
| Replace / expiry | Document Replacement Request, Document Expiry Review | Lifecycle |
| Privacy | Student Privacy Export Request, Student Data Access Log | Approval + audit |

## D5. Fees and accounting

| Feature | Record | What it does |
|---|---|---|
| Catalogue | Education Fee Code | Draft / Active / Retired |
| Policy | Education Fee Policy Version, Education Fee Installment | Published amounts / schedule |
| Adjustments | Student Fee Adjustment | Concession / Scholarship / Fine / Waiver |
| Demand | Student Fee Demand + Sales Invoice | Net must match invoice |
| Collection | Student Fee Payment + Payment Entry | Online / Offline, receipt |
| Portal pay | Student Portal Payment Attempt | Retry-safe tuition order |
| Events | Payment Provider Event | Order / capture / callback / refund |
| Refund | Student Fee Refund + credit note + refund PE | Approved then Posted |
| Settlement | Payment Settlement Import | Imported / Reconciled / Mismatch |
| GL | Fee General Ledger Reconciliation | Reconciled / Mismatch |

## D6. Portals and notices

| Feature | Where | What it does |
|---|---|---|
| Guardian PWA | `/guardian-admission` | Six-step EN/HI apply |
| Student PWA | `/student-portal` | Dues, pay, receipts, documents, notices |
| Access | Student Portal Access | Hashed token, expiry, revoke |
| OTP contract | Student Portal OTP Challenge | Fake local OTP, lock after 5 |
| Notices | Student Portal Notice | Published to families |
| Receipt PDF | `download_student_receipt` | Scoped to the token’s student |
| Health | `/api/method/university_erp.api.health.live` / `ready` | Staging/ops probe |

## D7. Integrations (adapters)

| Concern | Staging adapter | Production target (gated) |
|---|---|---|
| Payments | Fake Razorpay | Razorpay (institution-owned merchant) |
| SMS | Fake MSG91 | MSG91 after DLT / sender ownership |
| Email | Fake SMTP | Hostinger Business Email SMTP |
| Files | Fake R2 | Cloudflare R2 private bucket |
| Antivirus | Fake ClamAV | Approved scanner |

All adapters are behind ports so domain code does not hard-code a vendor.

## D8. Portal API cheat sheet

All under `/api/method/university_erp.api.portal.*` (guest, token-scoped).

| Method | Purpose |
|---|---|
| `get_application_context` | Published forms |
| `save_application_draft` | Create/update draft + CRM lead |
| `get_application_draft` | Resume |
| `upload_application_document` | Private upload + scan |
| `create_application_payment` | ₹500 order |
| `check_application_payment` | Status only |
| `confirm_application_payment` | Capture once |
| `get_student_portal_snapshot` | Student view |
| `download_student_receipt` | PDF |
| `create_student_payment` | Tuition order |
| `confirm_student_payment` | Capture + Payment Entry + receipt |
| `check_student_payment` | Status |
| `request_student_otp` / `verify_student_otp` | Fake OTP contract |

---

## E. Quick reference — statuses

| Record | Statuses |
|---|---|
| Education Institution Node | Active / Inactive / Locked |
| Institution Structure Version | Draft / Published / Cancelled |
| Academic Session Policy / Calendar | Draft / Published / Locked / Cancelled |
| Program Version | Draft / Published / Cancelled |
| Program Offering / Subject Offering | Draft / Open / Locked / Closed |
| Academic Section | Active / Inactive / Locked |
| Program Intake | Draft / Approved / Locked / Cancelled |
| Admission Application Form Version | Draft / Published / Retired |
| Admission Application Draft | Draft / Submitted / Abandoned |
| Admission Payment Attempt | Created / Pending / Paid / Failed / Cancelled |
| Admission Application Document | Uploaded / Scanning / Scan Passed / Scan Failed |
| CRM Application Handoff | Pending / Application Created / Failed |
| Eligibility Rule Set | Draft / Published / Retired |
| Eligibility Evaluation | Eligible / Ineligible |
| Merit Configuration | Draft / Active / Retired |
| Merit Run | Draft / Published / Superseded |
| Admission Seat Matrix | Draft / Locked / Retired |
| Seat Allocation Round | Draft / Published / Closed |
| Seat Offer | Offered / Accepted / Waitlisted / Expired / Cancelled |
| Admission Confirmation | Draft / Confirmed / Cancelled |
| Admission Student Conversion | Draft / Converted / Failed |
| Student Identity Profile | Draft / Active / Locked / Merged / Cancelled |
| Student Document verification | Pending Verification / Verified / Rejected / Expired / Replaced |
| Duplicate Candidate | Open / Confirmed Duplicate / Dismissed |
| Student Correction Request | Draft / Approved / Rejected / Cancelled |
| Education Fee Policy Version | Draft / Published / Retired |
| Student Fee Demand | Draft / Generated / Cancelled |
| Student Fee Payment | (submit sets Posted / receipt issued) |
| Student Fee Adjustment | Draft / Approved / Rejected |
| Student Fee Refund | Draft / Approved / Posted / Rejected |
| Payment Settlement Import | Imported / Reconciled / Mismatch |
| Fee General Ledger Reconciliation | Draft / Reconciled / Mismatch |
| Student Portal Access | Active / Revoked / Expired |
| Student Portal Notice | Draft / Published / Archived |
| Student Portal OTP Challenge | Pending / Verified / Expired / Locked |

---

## F. Honest limits for trainers

- Desk permissions on custom DocTypes are still primarily System Manager and Academics User in metadata. The role matrix is the target; full Role Permission Manager coverage is not signed off.
- There is no dedicated custom Workspace yet. Staff use Awesome Bar / module search.
- Guardian portal class list is hard-coded to Class 6–9 in the Vue app; live program offerings are not yet a dynamic dropdown.
- Application payment confirmation in the UI currently checks status; full browser-to-capture wiring is the fake-provider path, not Razorpay Checkout.js.
- Student portal Pay starts an order and polls status; a hosted checkout page is not implemented.
- Notifications are designed as an outbox; live SMS/email sending is not approved.
- Human UAT (`docs/quality/pilot-uat-script.md`) is still pending sign-off.

Train staff on the flows in this file, then execute UAT-001 through UAT-009 on synthetic data before any parent uses a real phone number.

---

## G. Related documents

| Document | Use |
|---|---|
| [Pilot scope](../requirements/pilot-scope.md) | What the first school is allowed to go live with |
| [UX and localization](ux-and-localization.md) | Language and low-literacy rules |
| [Role matrix](../security/role-matrix.md) | Permission boundaries |
| [Pilot UAT script](../quality/pilot-uat-script.md) | Formal test cases |
| [Marketing features](marketing-features.md) | External feature language |
| [Current implementation status](../current-implementation-status.md) | What is actually verified |
| [AGENTS.md](../../AGENTS.md) | Engineering contract |

---

*Guide version: 1.0 · Prepared 2026-08-17 · Matches implemented `university_erp` portals and DocTypes through Phase 8 staging.*
