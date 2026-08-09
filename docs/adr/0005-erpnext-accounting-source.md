# ADR-0005: Use ERPNext as the accounting source of truth

- Status: Accepted
- Date: 2026-08-01
- Related requirements: `BRD-US-151..155`, `BRD-FEE-001..999`

## Context

Education fee rules need institution-specific configuration, but balances, receipts, refunds, settlements, and reconciliation must remain financially correct and auditable.

## Decision

Custom records own fee applicability, schedules, concessions, and operational status. Approved ERPNext accounting documents own receivables, payments, reversals, bank reconciliation, and General Ledger effects. No custom parallel ledger is permitted.

## Consequences

- Accounting design and chart-of-accounts mapping require finance approval.
- Every fee workflow includes GL reconciliation tests.
- Corrections use cancellation/reversal and replacement, not record mutation.
- Duplicate gateway events must not duplicate accounting postings.

