# ADR-0009: Use Razorpay as the initial payment provider

- Status: Accepted; ownership resolved by ADR-0012
- Date: 2026-08-02
- Related requirements: `BRD-US-151..155`, `BRD-FEE-001..999`

## Decision

Implement Razorpay behind a provider-neutral payment port for Orders, checkout, webhook verification, refunds and settlement reconciliation. Browser callbacks are never payment authority. Signed webhooks are processed idempotently and authoritative provider state is verified before posting ERPNext accounting.

## Ownership decision

ADR-0012 resolves the Phase 0 ownership model: production Razorpay merchant accounts are institution-owned by default. A platform settlement model requires a later legal/finance ADR before use.

## Consequences

- Provider event/payment/order/refund/settlement IDs require uniqueness.
- Payment, accounting-posting and settlement states are independently reconciled.
- Sandbox contract tests precede production credentials.
