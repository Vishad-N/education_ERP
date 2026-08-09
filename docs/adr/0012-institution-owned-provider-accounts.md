# ADR-0012: Institution-owned provider accounts for money, SMS, and email identity

- Status: Accepted
- Date: 2026-08-09
- Related requirements: `BRD-US-151..155`, `BRD-US-186..200`, `BRD-FEE-001..999`
- Supersedes open ownership questions in: ADR-0009, ADR-0010

## Context

The product serves independently governed institutions with one Frappe site and database per institution. Payments, statutory messaging identity, and sender reputation have legal, financial, and operational consequences. Phase 0 requires an unambiguous ownership model before real provider credentials or production traffic are configured.

## Decision

Use institution-owned production accounts and sender identities by default:

- Razorpay merchant account: owned by the institution receiving funds.
- MSG91/DLT Principal Entity, sender headers, and approved templates: owned by the institution unless a later legal ADR approves a platform-owned model for a specific rollout.
- Hostinger SMTP/domain identity: owned or formally authorized by the institution's domain owner.
- Cloudflare R2 buckets and application infrastructure may be operated by the platform for the institution, but institution data remains institution-scoped and access-controlled per site.

The project founder is the interim accountable owner for Phase 0 documentation. Before production launch, named people must be recorded for:

- institution approval owner;
- finance owner;
- security/privacy owner;
- operations owner;
- engineering release owner.

## Consequences

- No production Razorpay, MSG91, DLT, SMTP, Cloudflare, or DNS setup starts without explicit user approval and institution authorization.
- Settlement, refunds, chargebacks, tax documents, and bank reconciliation remain institution-specific.
- SMS templates and sender headers are approved per institution before live SMS.
- Email sender domains require SPF, DKIM, DMARC, bounce handling, and per-institution throttling.
- Sandbox and fake providers remain the only allowed development defaults until production credentials are approved.
