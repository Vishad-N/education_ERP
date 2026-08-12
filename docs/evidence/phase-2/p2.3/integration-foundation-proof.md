# P2.3 Evidence - Integration Foundation Proofs

Date: 2026-08-10

Status: Complete

## Scope

This proof added local-only fake provider adapters for Razorpay, MSG91, SMTP, R2 and ClamAV. It also added shared idempotency, webhook signature and replay validation structures.

No production credentials, live providers, live payments, live SMS/email, Cloudflare R2 buckets or production DNS were used.

## Implemented Modules

```text
apps/university_erp/university_erp/integrations/exceptions.py
apps/university_erp/university_erp/integrations/idempotency.py
apps/university_erp/university_erp/integrations/webhooks.py
apps/university_erp/university_erp/integrations/payments/ports.py
apps/university_erp/university_erp/integrations/payments/fake_razorpay.py
apps/university_erp/university_erp/integrations/sms/fake_msg91.py
apps/university_erp/university_erp/integrations/email/fake_smtp.py
apps/university_erp/university_erp/integrations/storage/fake_r2.py
apps/university_erp/university_erp/integrations/antivirus/fake_clamav.py
apps/university_erp/university_erp/integrations/contracts.py
```

## Verification Commands

```powershell
docker compose exec backend bash -lc "cd /home/frappe/frappe-bench && env/bin/python -m compileall -q apps/university_erp/university_erp/integrations"
docker compose exec backend bench --site p21.localhost execute university_erp.integrations.contracts.run_integration_foundation_proof
```

## Contract Result

```json
{
  "payment": {
    "order_id": "order_000001",
    "duplicate_order_reused_existing": true,
    "payment_id": "pay_000001",
    "webhook_replay_key": "webhook:evt_payment_captured_1",
    "webhook_replay_rejected": true,
    "bad_signature_rejected": true,
    "refund_id": "rfnd_000001",
    "duplicate_refund_reused_existing": true,
    "settlement_id": "setl_000001",
    "settlement_amount": 100000
  },
  "messaging": {
    "sms_provider": "fake_msg91",
    "sms_status": "queued",
    "email_provider": "fake_smtp",
    "email_status": "queued"
  },
  "storage": {
    "provider": "fake_r2",
    "status": "quarantined",
    "size": 19,
    "checksum_sha256": "386698bf7f05739934006e75ac048de25d388392a8268d649eb99f3730c383bf",
    "signed_url_is_short_lived": true,
    "deleted": true
  },
  "antivirus": {
    "clean_status": "clean",
    "infected_status": "infected",
    "infected_signature": "EICAR-Test-File"
  },
  "failures": {
    "razorpay_timeout": "raised",
    "msg91_failure": "raised",
    "smtp_timeout": "raised",
    "r2_failure": "raised",
    "clamav_timeout": "raised"
  }
}
```

## Assertions Covered

- Domain code can create a fake Razorpay order without network calls.
- Reusing the same payment idempotency key returns the original order.
- Fake payment capture and settlement records are fetchable.
- HMAC webhook signature verification accepts valid payloads.
- Duplicate webhook replay is rejected.
- Bad webhook signature is rejected.
- Reusing the same refund idempotency key returns the original refund.
- Fake MSG91 and SMTP adapters return queued delivery results.
- Fake R2 stores private objects in quarantined state, generates short-lived signed URLs and deletes objects.
- Fake ClamAV returns clean and infected scan states.
- Provider failure and timeout paths raise explicit exceptions.

## Known Follow-Ups

- Replace in-memory idempotency/replay stores with database-backed unique records before production.
- Add transactional outbox and provider transaction DocTypes in later shared-platform work.
- Implement real/sandbox Razorpay, MSG91, SMTP, R2 and ClamAV adapters behind the same ports.
- Add provider-specific contract tests when credentials and sandbox endpoints are approved.

## Gate Result

P2.3 exit gate passed. Domain code can now test provider success, failure, timeout and duplicate-event behavior without real providers.
