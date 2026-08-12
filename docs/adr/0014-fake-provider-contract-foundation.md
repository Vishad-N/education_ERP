# ADR-0014: Use Fake Provider Adapters for Integration Contract Proofs

- Status: Accepted for Phase 2 proof
- Date: 2026-08-10
- Decision owners: Engineering
- Related requirements: `BRD-US-151..155`, `BRD-US-186..200`, `BRD-FEE-001..999`

## Context

P2.3 requires domain code to test provider success, failure, timeout and duplicate events without real providers. ADR-0009, ADR-0010 and ADR-0012 also block live Razorpay, MSG91, SMTP and production-provider setup until explicit later approval.

## Decision

Add provider-neutral integration foundations under `university_erp.integrations`:

- fake Razorpay adapter for orders, payments, refunds, settlements and signed webhook verification;
- fake MSG91 adapter for SMS send results;
- fake SMTP adapter for email send results;
- fake R2 adapter for private-object quarantine, signed URL and delete behavior;
- fake ClamAV adapter for clean/infected scan results;
- shared provider exceptions;
- in-memory idempotency and replay stores for local proof work;
- HMAC webhook verifier with timestamp tolerance, signature comparison and replay rejection.

These fakes are local contract tools only. Production implementation must replace in-memory stores with database-backed idempotency, transactional outbox records and durable provider transaction records.

## Consequences

- Domain code can be developed and tested without external network calls or credentials.
- Failure and timeout states are observable and deterministic.
- Duplicate order/refund/webhook behavior can be tested before production provider code exists.
- The fakes do not prove provider-specific Razorpay, MSG91, SMTP, R2 or ClamAV API compatibility.

## Validation

P2.3 evidence: `docs/evidence/phase-2/p2.3/integration-foundation-proof.md`.

The local proof confirmed:

- duplicate payment order idempotency;
- webhook HMAC signature verification;
- duplicate webhook replay rejection;
- bad-signature rejection;
- duplicate refund idempotency;
- SMS and email queued responses;
- R2-style private object quarantine, short-lived signed URL and delete behavior;
- clean and infected antivirus scan states;
- explicit timeout/failure exceptions for all fake providers.

## Revisit Triggers

- P2.3 fakes are promoted beyond local testing.
- Production provider adapters are implemented.
- Durable outbox/provider transaction DocTypes are added.
- Provider-specific webhook signature, timestamp or event-ID semantics differ from the fake contract.
