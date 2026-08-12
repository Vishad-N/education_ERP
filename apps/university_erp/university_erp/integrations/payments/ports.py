from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class PaymentOrderRequest:
    amount: int
    currency: str
    receipt: str
    notes: dict[str, str] | None = None


@dataclass(frozen=True)
class PaymentOrder:
    provider: str
    order_id: str
    amount: int
    currency: str
    status: str


@dataclass(frozen=True)
class PaymentRecord:
    provider: str
    payment_id: str
    order_id: str
    amount: int
    currency: str
    status: str


@dataclass(frozen=True)
class RefundRecord:
    provider: str
    refund_id: str
    payment_id: str
    amount: int
    status: str


@dataclass(frozen=True)
class SettlementRecord:
    provider: str
    settlement_id: str
    payment_ids: list[str]
    amount: int
    status: str


class PaymentGatewayAdapter(Protocol):
    def create_order(self, request: PaymentOrderRequest, *, idempotency_key: str) -> PaymentOrder: ...

    def fetch_payment(self, payment_id: str) -> PaymentRecord: ...

    def refund(self, payment_id: str, amount: int, *, idempotency_key: str) -> RefundRecord: ...

    def fetch_settlement(self, settlement_id: str) -> SettlementRecord: ...

