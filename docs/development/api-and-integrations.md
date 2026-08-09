# API and Integration Standards

Provider-specific contracts, ownership decisions, and failure behavior for Razorpay, MSG91, Hostinger SMTP, Cloudflare R2, and malware scanning are defined in the [provider architecture](../integrations/provider-architecture.md).

## API surface

Use standard Frappe resource APIs for straightforward permission-safe CRUD. Use explicit whitelisted methods under `university_erp.api.v1` for domain commands, multi-record transactions, calculations, provider callbacks, and stable external contracts.

## HTTP conventions

- HTTPS only outside local development.
- JSON uses UTF-8 and ISO 8601 timestamps with timezone.
- API paths are versioned, for example `/api/method/university_erp.api.v1.admissions.accept_offer`.
- Commands use POST; reads use GET unless payload sensitivity/size requires an approved alternative.
- List APIs require bounded pagination, deterministic ordering and permission-safe filters.
- Return stable machine codes plus safe user messages; never expose stack traces.
- Propagate or create a correlation/request ID.
- Require idempotency keys for retried commands, payment operations and inbound webhooks.

## Error contract

```json
{
  "error": {
    "code": "SEAT_CAPACITY_EXHAUSTED",
    "message": "The selected seat is no longer available.",
    "correlation_id": "req_...",
    "details": []
  }
}
```

Do not include secrets, raw provider payloads, SQL, internal paths, or sensitive identity values.

## Authentication and authorization

- Browser sessions use Frappe CSRF/session controls.
- External server integrations use scoped OAuth or API credentials with rotation and expiry.
- Every endpoint checks role, site, institution/campus, document, field and workflow authorization server-side.
- Service identities receive least privilege and separate credentials per environment/provider.
- Rate limits differ for public forms, authenticated users, exports, logins and webhooks.

## Domain event envelope

```json
{
  "event_id": "uuid",
  "event_type": "admission.offer_accepted.v1",
  "occurred_at": "2026-08-01T10:00:00+05:30",
  "site": "institution-site-id",
  "aggregate_type": "Seat Offer",
  "aggregate_id": "opaque-id",
  "aggregate_version": 4,
  "correlation_id": "uuid",
  "causation_id": "uuid",
  "actor_id": "opaque-user-id",
  "payload": {}
}
```

Events are past-tense facts. Consumers deduplicate by `event_id`; schemas are versioned and backward-compatible within a major version. Payloads include only data needed by consumers.

## Webhook intake

1. Validate provider route, TLS, signature and timestamp/replay window.
2. Persist sanitized raw-event metadata and provider event identity.
3. Return the provider-required acknowledgement quickly.
4. Process asynchronously with idempotency and bounded retries.
5. Fetch/verify authoritative provider state when payment semantics require it.
6. Post business/accounting result exactly once.
7. Record attempts, terminal outcome and reconciliation state.

Client redirects never prove payment success.

## Payment adapters

Normalize provider behavior behind an interface for request creation, status verification, refund, webhook verification and settlement import. Store provider transaction/order/refund/settlement IDs with unique constraints. Separate payment state from accounting posting state and reconcile both.

Test success, decline, abandonment, timeout, duplicate webhook, out-of-order webhook, amount/currency mismatch, replay, partial payment, refund, failed refund, chargeback and settlement discrepancy.

## Messaging adapters

- Render a versioned template with approved variables.
- Enforce consent, event enablement, quiet hours and channel preference.
- Queue through the outbox; apply provider and site throttles.
- Record attempt, provider message ID, status, failure category and retry time.
- Use exponential backoff with jitter and a terminal dead-letter/manual review state.
- Never place unnecessary PII, credentials or sensitive attachments in messages.

## File and malware integration

Uploads enter private quarantine. Validate extension, declared MIME, detected signature and size; scan before business verification; expose only short-lived authorized access. Scan timeout or scanner outage leaves the file quarantined, never implicitly clean.

## Contract governance

Maintain contract tests for every provider and public integration. Provider SDK/version changes require sandbox verification. Breaking API/event changes require a new major contract version, migration window, consumer inventory and deprecation date.
