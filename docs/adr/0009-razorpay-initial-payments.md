# ADR-0009: Use Razorpay as the initial payment provider

- Status: Accepted with open settlement decision
- Date: 2026-08-02
- Related requirements: `BRD-US-151..155`, `BRD-FEE-001..999`

## Decision

Implement Razorpay behind a provider-neutral payment port for Orders, checkout, webhook verification, refunds and settlement reconciliation. Browser callbacks are never payment authority. Signed webhooks are processed idempotently and authoritative provider state is verified before posting ERPNext accounting.

## Open decision

Finance/legal owners must approve institution-owned merchant accounts or an appropriate platform marketplace/route settlement model. Independent-institution funds may not be centralized through an ordinary merchant account without approval.

## Consequences

- Provider event/payment/order/refund/settlement IDs require uniqueness.
- Payment, accounting-posting and settlement states are independently reconciled.
- Sandbox contract tests precede production credentials.

