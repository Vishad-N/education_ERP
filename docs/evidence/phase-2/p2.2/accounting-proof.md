# P2.2 Evidence - Accounting Proof

Date: 2026-08-10

Status: Complete

## Scope

This proof verified a local, synthetic fee-to-accounting path using the pinned Frappe, ERPNext, Education, Payments, CRM and `university_erp` app set on `p21.localhost`.

No production credentials, live Razorpay calls, live payments or real refunds were used.

## Implemented Proof Harness

Proof function:

```text
university_erp.domain.fees.accounting_proof.run_accounting_proof
```

Local file:

```text
apps/university_erp/university_erp/domain/fees/accounting_proof.py
```

## Flow Verified

```text
Education Fee Structure
  -> Education Fee Schedule
  -> ERPNext Sales Invoice
  -> local provider-event surrogate
  -> ERPNext Payment Entry
  -> ERPNext credit note
  -> ERPNext refund Payment Entry
  -> ERPNext GL Entry reconciliation
```

The provider-event surrogate stores a synthetic external event ID in `Payment Entry.reference_no` and checks for an existing submitted `Payment Entry` before creating a new one. This proves the idempotent posting pattern locally. A production provider transaction DocType with database-level uniqueness is still required before real Razorpay traffic.

## Command

```powershell
docker compose exec backend bench --site p21.localhost execute university_erp.domain.fees.accounting_proof.run_accounting_proof
```

## Result

```json
{
  "site": "p21.localhost",
  "company": "P2.2 Accounting Proof School",
  "student": "EDU-STU-2026-00001",
  "fee_schedule": "EDU-FSH-2026-00001",
  "sales_invoice": "ACC-SINV-2026-00001",
  "sales_invoice_grand_total": 1000.0,
  "sales_invoice_outstanding_after_payments": 0.0,
  "first_payment_entry": "ACC-PAY-2026-00001",
  "duplicate_payment_entry": "ACC-PAY-2026-00001",
  "duplicate_payment_reused_existing": true,
  "second_payment_entry": "ACC-PAY-2026-00002",
  "credit_note": "ACC-SINV-2026-00002",
  "credit_note_grand_total": -1000.0,
  "refund_payment_entry": "ACC-PAY-2026-00003",
  "duplicate_refund_entry": "ACC-PAY-2026-00003",
  "duplicate_refund_reused_existing": true,
  "payment_entries_for_first_event": 1,
  "payment_entries_for_refund_event": 1,
  "gl_balance_by_account": [
    {
      "account": "Cash - P22",
      "debit": 1000.0,
      "credit": 1000.0,
      "net": 0.0
    },
    {
      "account": "Debtors - P22",
      "debit": 2000.0,
      "credit": 2000.0,
      "net": 0.0
    },
    {
      "account": "Sales - P22",
      "debit": 1000.0,
      "credit": 1000.0,
      "net": 0.0
    }
  ]
}
```

## Assertions Covered

- Fee demand creates an ERPNext receivable through `Sales Invoice`.
- INR 400 partial payment posts as one submitted `Payment Entry`.
- Replaying the same synthetic provider payment event returns the original `Payment Entry`.
- INR 600 final payment settles the original invoice.
- Credit note reverses the fee income/receivable.
- Refund payment posts through ERPNext `Payment Entry`.
- Replaying the same synthetic refund event returns the original refund `Payment Entry`.
- GL entries for the proof vouchers balance by account and in total.

## Known Follow-Ups

- Replace the `Payment Entry.reference_no` surrogate with a dedicated provider transaction DocType that has database-level uniqueness for provider, event ID, payment ID, order ID and refund ID.
- Implement fake/sandbox Razorpay adapter contracts in P2.3 before any production credential work.
- Define settlement import, chargeback, concession, scholarship, fine, write-off and security-deposit accounting treatment with finance approval.
- Add browser/API and permission tests when the fee workflow moves from proof harness to product DocTypes.

## Gate Result

P2.2 exit gate passed for the local proof. Duplicate payment/refund events did not duplicate accounting postings, refund used ERPNext credit-note and Payment Entry behavior, and the proof vouchers reconciled to ERPNext General Ledger.
