# Provider Integration Architecture

## Integration pattern

Domain modules depend on provider-neutral ports. Provider-specific SDKs, payloads, credentials and retry rules remain inside adapters.

```text
Domain service
    -> integration port
        -> fake/sandbox adapter
        -> Razorpay adapter
        -> MSG91 adapter
        -> Hostinger SMTP adapter
        -> Cloudflare R2 adapter
        -> ClamAV adapter
```

Every external operation has correlation, idempotency, timeout, retry, terminal failure and reconciliation behavior.

## Tenant credential model

Each institution must have separately controlled provider configuration where provider/legal models require it:

- Razorpay merchant/key/webhook secret and settlement identity;
- DLT Principal Entity, sender header, template IDs and MSG91 credentials;
- SMTP host, mailbox, DKIM/SPF/DMARC identity and daily quota;
- R2 bucket/token or approved isolated namespace;
- per-channel enablement, quotas and alert thresholds.

Secrets are encrypted or injected through protected environment/secret mechanisms. They never appear in Git, logs, screenshots, exports or general configuration fixtures.

## Razorpay

Required capabilities:

- create an Order from an approved fee/payment intent;
- launch checkout with amount/currency/order identity fixed server-side;
- validate checkout signature only as immediate UX input;
- process signed raw-body webhooks asynchronously;
- verify authoritative payment/refund state through the API;
- post ERPNext Payment Entry exactly once;
- support partial payments, refunds and failed refunds according to approved policy;
- import settlement data and reconcile to bank/GL;
- detect duplicate, replayed, missing, out-of-order and mismatched events.

Open decision: use institution-owned Razorpay accounts or an approved platform marketplace/route settlement model. Ordinary centralized collection for independent institutions is prohibited until finance/legal/accounting design is approved.

## MSG91 and DLT

Required capabilities:

- OTP and service/transactional SMS through approved routes;
- institution-specific DLT Principal Entity/header/template mapping;
- English and Hindi/Unicode template versions;
- delivery callbacks, normalized failure codes and retry policy;
- per-site/provider throttling and pause/resume;
- consent/preference checks where applicable;
- usage and cost reporting.

Open decision: whether the platform company or each institution owns DLT registrations. No real SMS delivery begins before PE, header and content templates are approved.

## Hostinger SMTP

Use authenticated SMTP rather than server-local mail. Initially prefer separate institution/domain mailboxes so identity, quotas and reputation are not shared invisibly.

Required controls:

- SPF, DKIM and DMARC;
- TLS, credential rotation and per-environment credentials;
- queued delivery, bounded retry and daily/rate throttling;
- bounce/failure tracking where available;
- no sensitive attachments unless explicitly approved;
- threshold for migration to a dedicated transactional provider.

Hostinger plan limits are treated as configuration and monitored rather than hard-coded.

## Cloudflare R2

- Use S3-compatible private API endpoints.
- Never use `r2.dev` as production document delivery.
- Scope tokens to required buckets and permissions.
- Use unique non-guessable object keys; never include Aadhaar, mobile or names in keys.
- Store site, owner, document type, checksum, scan state and lifecycle in MariaDB.
- Generate short-lived authorized URLs only after server-side permission checks.
- Enable versioning/backup/lifecycle according to approved retention.
- Separate production, non-production and backup buckets/credentials.

## ClamAV

Upload enters quarantine, then extension/MIME/signature/size validation and ClamAV scan. Scanner timeout/outage leaves the object quarantined. Only passed objects become available for business verification.

## Provider contract tests

Each adapter must pass deterministic tests for success, timeout, authentication failure, throttling, malformed payload, duplicate, replay, out-of-order event, unavailable provider, retry exhaustion and manual reconciliation. Sandbox test evidence is required before production credentials are enabled.

