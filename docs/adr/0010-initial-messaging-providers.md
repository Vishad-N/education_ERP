# ADR-0010: Use MSG91 and Hostinger SMTP initially

- Status: Accepted with open DLT ownership decision
- Date: 2026-08-02
- Related requirements: `BRD-US-186..200`

## Decision

Use MSG91 for initial OTP/transactional SMS and Hostinger Business Email authenticated SMTP for initial email delivery. Both are adapters behind the notification outbox. Configure credentials, identities, templates, quotas and throttles per institution where required.

## Open decision

Approve whether the platform company or each institution owns DLT Principal Entity registration, sender headers and content templates. No real SMS begins before the approved DLT model is operational.

## Consequences

- English/Hindi template versions and delivery status are audited.
- SPF, DKIM and DMARC are required for email domains.
- SMTP daily/rate limits are monitored and trigger migration to a dedicated provider when insufficient.
- Provider outage cannot roll back the source business transaction.

