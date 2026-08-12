from __future__ import annotations

import hashlib
import hmac
import time
from dataclasses import dataclass

from university_erp.integrations.exceptions import ProviderReplayError, ProviderValidationError
from university_erp.integrations.idempotency import InMemoryIdempotencyStore


@dataclass(frozen=True)
class WebhookVerificationResult:
    event_id: str
    timestamp: int
    replay_key: str


class HmacWebhookVerifier:
    def __init__(
        self,
        *,
        secret: str,
        replay_store: InMemoryIdempotencyStore,
        tolerance_seconds: int = 300,
        now: int | None = None,
    ) -> None:
        self.secret = secret.encode("utf-8")
        self.replay_store = replay_store
        self.tolerance_seconds = tolerance_seconds
        self.now = now

    def sign(self, *, timestamp: int, body: bytes) -> str:
        payload = str(timestamp).encode("utf-8") + b"." + body
        return hmac.new(self.secret, payload, hashlib.sha256).hexdigest()

    def verify(self, *, event_id: str, timestamp: int, body: bytes, signature: str) -> WebhookVerificationResult:
        current = self.now if self.now is not None else int(time.time())
        if abs(current - timestamp) > self.tolerance_seconds:
            raise ProviderValidationError("Webhook timestamp is outside the replay tolerance.")

        expected = self.sign(timestamp=timestamp, body=body)
        if not hmac.compare_digest(expected, signature):
            raise ProviderValidationError("Webhook signature mismatch.")

        replay_key = f"webhook:{event_id}"
        if self.replay_store.seen(replay_key):
            raise ProviderReplayError(f"Webhook event already processed: {event_id}")

        self.replay_store.mark_seen(replay_key)
        return WebhookVerificationResult(event_id=event_id, timestamp=timestamp, replay_key=replay_key)

