from __future__ import annotations

import json

from university_erp.integrations.exceptions import ProviderTimeout, ProviderValidationError
from university_erp.integrations.idempotency import InMemoryIdempotencyStore
from university_erp.integrations.payments.ports import (
    PaymentOrder,
    PaymentOrderRequest,
    PaymentRecord,
    RefundRecord,
    SettlementRecord,
)
from university_erp.integrations.webhooks import HmacWebhookVerifier, WebhookVerificationResult


class FakeRazorpayAdapter:
    provider = "fake_razorpay"

    def __init__(self, *, secret: str = "local-secret", mode: str = "success") -> None:
        self.mode = mode
        self.idempotency = InMemoryIdempotencyStore()
        self.replays = InMemoryIdempotencyStore()
        self.verifier = HmacWebhookVerifier(secret=secret, replay_store=self.replays, now=1_800_000_000)
        self.orders: dict[str, PaymentOrder] = {}
        self.payments: dict[str, PaymentRecord] = {}
        self.refunds: dict[str, RefundRecord] = {}
        self.settlements: dict[str, SettlementRecord] = {}

    def create_order(self, request: PaymentOrderRequest, *, idempotency_key: str) -> PaymentOrder:
        self._guard_mode()
        existing = self.idempotency.get(f"order:{idempotency_key}")
        if existing:
            return existing

        order = PaymentOrder(
            provider=self.provider,
            order_id=f"order_{len(self.orders) + 1:06d}",
            amount=request.amount,
            currency=request.currency,
            status="created",
        )
        self.orders[order.order_id] = order
        self.idempotency.setdefault(f"order:{idempotency_key}", order)
        return order

    def capture_payment(self, order_id: str) -> PaymentRecord:
        self._guard_mode()
        order = self.orders[order_id]
        payment = PaymentRecord(
            provider=self.provider,
            payment_id=f"pay_{len(self.payments) + 1:06d}",
            order_id=order.order_id,
            amount=order.amount,
            currency=order.currency,
            status="captured",
        )
        self.payments[payment.payment_id] = payment
        return payment

    def fetch_payment(self, payment_id: str) -> PaymentRecord:
        self._guard_mode()
        return self.payments[payment_id]

    def refund(self, payment_id: str, amount: int, *, idempotency_key: str) -> RefundRecord:
        self._guard_mode()
        existing = self.idempotency.get(f"refund:{idempotency_key}")
        if existing:
            return existing

        if payment_id not in self.payments:
            raise ProviderValidationError(f"Unknown payment: {payment_id}")

        refund = RefundRecord(
            provider=self.provider,
            refund_id=f"rfnd_{len(self.refunds) + 1:06d}",
            payment_id=payment_id,
            amount=amount,
            status="processed",
        )
        self.refunds[refund.refund_id] = refund
        self.idempotency.setdefault(f"refund:{idempotency_key}", refund)
        return refund

    def fetch_settlement(self, settlement_id: str) -> SettlementRecord:
        self._guard_mode()
        if settlement_id not in self.settlements:
            payment_ids = list(self.payments)
            amount = sum(payment.amount for payment in self.payments.values())
            self.settlements[settlement_id] = SettlementRecord(
                provider=self.provider,
                settlement_id=settlement_id,
                payment_ids=payment_ids,
                amount=amount,
                status="settled",
            )
        return self.settlements[settlement_id]

    def make_webhook(self, *, event_id: str, payment_id: str, timestamp: int = 1_800_000_000) -> tuple[bytes, dict[str, str]]:
        body = json.dumps(
            {"event_id": event_id, "type": "payment.captured", "payment_id": payment_id},
            sort_keys=True,
        ).encode("utf-8")
        signature = self.verifier.sign(timestamp=timestamp, body=body)
        return body, {"x-provider-event-id": event_id, "x-provider-timestamp": str(timestamp), "x-provider-signature": signature}

    def verify_webhook(self, *, body: bytes, headers: dict[str, str]) -> WebhookVerificationResult:
        return self.verifier.verify(
            event_id=headers["x-provider-event-id"],
            timestamp=int(headers["x-provider-timestamp"]),
            body=body,
            signature=headers["x-provider-signature"],
        )

    def _guard_mode(self) -> None:
        if self.mode == "timeout":
            raise ProviderTimeout("Fake Razorpay timeout.")
        if self.mode == "failure":
            raise ProviderValidationError("Fake Razorpay failure.")

