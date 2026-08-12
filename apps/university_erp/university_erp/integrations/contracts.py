from __future__ import annotations

from university_erp.integrations.antivirus.fake_clamav import FakeClamAvAdapter
from university_erp.integrations.email.fake_smtp import FakeSmtpAdapter
from university_erp.integrations.exceptions import ProviderReplayError, ProviderTimeout, ProviderValidationError
from university_erp.integrations.payments.fake_razorpay import FakeRazorpayAdapter
from university_erp.integrations.payments.ports import PaymentOrderRequest
from university_erp.integrations.sms.fake_msg91 import FakeMsg91Adapter
from university_erp.integrations.storage.fake_r2 import FakeR2Adapter


def run_integration_foundation_proof() -> dict:
    payment = _prove_payments()
    messaging = _prove_messaging()
    storage = _prove_storage()
    antivirus = _prove_antivirus()
    failures = _prove_failure_modes()

    result = {
        "payment": payment,
        "messaging": messaging,
        "storage": storage,
        "antivirus": antivirus,
        "failures": failures,
    }
    _assert_result(result)
    return result


def _prove_payments() -> dict:
    adapter = FakeRazorpayAdapter()
    request = PaymentOrderRequest(amount=100000, currency="INR", receipt="P2.3-RECEIPT")
    order = adapter.create_order(request, idempotency_key="fee-demand-1")
    duplicate_order = adapter.create_order(request, idempotency_key="fee-demand-1")
    payment = adapter.capture_payment(order.order_id)
    body, headers = adapter.make_webhook(event_id="evt_payment_captured_1", payment_id=payment.payment_id)
    verified = adapter.verify_webhook(body=body, headers=headers)

    replay_rejected = False
    try:
        adapter.verify_webhook(body=body, headers=headers)
    except ProviderReplayError:
        replay_rejected = True

    bad_signature_rejected = False
    bad_headers = dict(headers)
    bad_headers["x-provider-event-id"] = "evt_bad_signature"
    bad_headers["x-provider-signature"] = "bad"
    try:
        adapter.verify_webhook(body=body, headers=bad_headers)
    except ProviderValidationError:
        bad_signature_rejected = True

    refund = adapter.refund(payment.payment_id, 100000, idempotency_key="refund-1")
    duplicate_refund = adapter.refund(payment.payment_id, 100000, idempotency_key="refund-1")
    settlement = adapter.fetch_settlement("setl_000001")

    return {
        "order_id": order.order_id,
        "duplicate_order_reused_existing": order == duplicate_order,
        "payment_id": payment.payment_id,
        "webhook_replay_key": verified.replay_key,
        "webhook_replay_rejected": replay_rejected,
        "bad_signature_rejected": bad_signature_rejected,
        "refund_id": refund.refund_id,
        "duplicate_refund_reused_existing": refund == duplicate_refund,
        "settlement_id": settlement.settlement_id,
        "settlement_amount": settlement.amount,
    }


def _prove_messaging() -> dict:
    sms = FakeMsg91Adapter()
    email = FakeSmtpAdapter()
    sms_result = sms.send_sms(to="+919999999999", template_id="P2_3_TEMPLATE", variables={"name": "Proof"})
    email_result = email.send_email(to="guardian@example.invalid", subject="P2.3 Proof", body="Synthetic proof")
    return {
        "sms_provider": sms_result.provider,
        "sms_status": sms_result.status,
        "email_provider": email_result.provider,
        "email_status": email_result.status,
    }


def _prove_storage() -> dict:
    storage = FakeR2Adapter()
    stored = storage.put_private_object(
        key="p21.localhost/documents/proof.txt",
        body=b"P2.3 private object",
        content_type="text/plain",
    )
    url = storage.signed_download_url(key=stored.key, expires_in_seconds=300)
    storage.delete_object(key=stored.key)
    return {
        "provider": stored.provider,
        "status": stored.status,
        "size": stored.size,
        "checksum_sha256": stored.checksum_sha256,
        "signed_url_is_short_lived": "expires=300" in url,
        "deleted": stored.key not in storage.objects,
    }


def _prove_antivirus() -> dict:
    scanner = FakeClamAvAdapter()
    clean = scanner.scan(body=b"normal file")
    infected = scanner.scan(body=b"EICAR test marker")
    return {
        "clean_status": clean.status,
        "infected_status": infected.status,
        "infected_signature": infected.signature,
    }


def _prove_failure_modes() -> dict:
    checks = {}
    for name, call in {
        "razorpay_timeout": lambda: FakeRazorpayAdapter(mode="timeout").create_order(
            PaymentOrderRequest(amount=1, currency="INR", receipt="timeout"),
            idempotency_key="timeout",
        ),
        "msg91_failure": lambda: FakeMsg91Adapter(mode="failure").send_sms(
            to="+919999999999",
            template_id="FAIL",
            variables={},
        ),
        "smtp_timeout": lambda: FakeSmtpAdapter(mode="timeout").send_email(
            to="x@example.invalid",
            subject="Timeout",
            body="Timeout",
        ),
        "r2_failure": lambda: FakeR2Adapter(mode="failure").put_private_object(
            key="site/file.txt",
            body=b"x",
            content_type="text/plain",
        ),
        "clamav_timeout": lambda: FakeClamAvAdapter(mode="timeout").scan(body=b"x"),
    }.items():
        try:
            call()
            checks[name] = "not_raised"
        except (ProviderTimeout, ProviderValidationError):
            checks[name] = "raised"
    return checks


def _assert_result(result: dict) -> None:
    payment = result["payment"]
    if not payment["duplicate_order_reused_existing"]:
        raise AssertionError("Duplicate payment order did not reuse existing result.")
    if not payment["webhook_replay_rejected"]:
        raise AssertionError("Duplicate webhook replay was not rejected.")
    if not payment["bad_signature_rejected"]:
        raise AssertionError("Bad webhook signature was not rejected.")
    if not payment["duplicate_refund_reused_existing"]:
        raise AssertionError("Duplicate refund did not reuse existing result.")
    if result["storage"]["status"] != "quarantined" or not result["storage"]["deleted"]:
        raise AssertionError("Storage quarantine/delete contract failed.")
    if result["antivirus"]["clean_status"] != "clean" or result["antivirus"]["infected_status"] != "infected":
        raise AssertionError("Antivirus scan contract failed.")
    if any(status != "raised" for status in result["failures"].values()):
        raise AssertionError("Failure/timeout modes were not observable.")
