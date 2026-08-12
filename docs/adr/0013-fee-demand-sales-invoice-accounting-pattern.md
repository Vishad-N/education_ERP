# ADR-0013: Use Sales Invoice Pattern for Education Fee Demands

- Status: Accepted for Phase 2 proof
- Date: 2026-08-10
- Decision owners: Engineering; finance owner approval still required before production fee rollout
- Related requirements: `BRD-US-151..155`, `BRD-FEE-001..999`

## Context

ADR-0005 requires ERPNext to remain the accounting source of truth. P2.2 needed a working local proof that education fee demand can become a receivable, accept partial payment, reject duplicate provider events, support refund accounting and reconcile to General Ledger without a parallel custom ledger.

The installed Education app has a `Fee Schedule` path that maps fee components into ERPNext `Sales Invoice` documents. ERPNext already owns `Sales Invoice`, `Payment Entry`, credit-note and `GL Entry` posting behavior.

## Decision

Use this accounting pattern:

```text
Fee policy and assignment in university_erp
  -> Education Fee Schedule / Fee Structure bridge where semantics fit
  -> ERPNext Sales Invoice as the student receivable
  -> provider-verified idempotent payment event
  -> ERPNext Payment Entry
  -> ERPNext credit note for approved refunds/reversals
  -> ERPNext refund Payment Entry
  -> ERPNext GL Entry and reconciliation reports
```

The Phase 2 proof used a local provider-event surrogate: the external provider event ID was stored on `Payment Entry.reference_no`, and duplicate events reused the existing submitted `Payment Entry`. Production implementation must replace this surrogate with a dedicated provider transaction/outbox model that enforces uniqueness at the database level before any accounting document is submitted.

## Consequences

- Fee receivables, collections and refunds remain visible in ERPNext accounting.
- Partial payment and refund behavior can use ERPNext validation and GL posting.
- `Payment Entry.reference_no` is not sufficient as the final production idempotency control.
- Full Razorpay order/webhook/refund/settlement contracts remain to be implemented behind the provider adapter.
- The final chart of accounts, fee income classification, tax treatment, scholarship/concession accounting and refund approval policy need finance sign-off.

## Validation

P2.2 local proof evidence: `docs/evidence/phase-2/p2.2/accounting-proof.md`.

Validation completed on `p21.localhost`:

- Education `Fee Schedule` generated submitted ERPNext `Sales Invoice`.
- Partial payment of INR 400 posted through `Payment Entry`.
- Duplicate payment event reused the same submitted `Payment Entry`.
- Final payment of INR 600 settled the original invoice.
- Standalone credit note reversed the fee receivable/income.
- Refund `Payment Entry` paid the credit note.
- Duplicate refund event reused the same submitted `Payment Entry`.
- GL entries balanced to zero net across Cash, Debtors and Sales for the proof vouchers.

## Revisit Triggers

- Finance rejects Sales Invoice as the receivable document for education fees.
- Fee requirements need multi-company, tax, scholarship funding, security deposit or write-off treatment that cannot be represented cleanly with the current pattern.
- Razorpay settlement, chargeback or refund behavior requires a different document relationship.
- ERPNext or Education v16 changes the Fee Schedule to Sales Invoice mapping.
