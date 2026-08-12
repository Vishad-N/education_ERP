from __future__ import annotations

import hashlib
from dataclasses import dataclass

from university_erp.integrations.exceptions import ProviderTimeout, ProviderValidationError


@dataclass(frozen=True)
class StoredObject:
    provider: str
    key: str
    checksum_sha256: str
    size: int
    status: str


class FakeR2Adapter:
    provider = "fake_r2"

    def __init__(self, *, mode: str = "success") -> None:
        self.mode = mode
        self.objects: dict[str, bytes] = {}

    def put_private_object(self, *, key: str, body: bytes, content_type: str) -> StoredObject:
        self._guard_mode()
        if not key or not body or "/" not in key:
            raise ProviderValidationError("Invalid private object key or body.")
        self.objects[key] = body
        return StoredObject(
            provider=self.provider,
            key=key,
            checksum_sha256=hashlib.sha256(body).hexdigest(),
            size=len(body),
            status="quarantined",
        )

    def signed_download_url(self, *, key: str, expires_in_seconds: int) -> str:
        self._guard_mode()
        if key not in self.objects:
            raise ProviderValidationError(f"Unknown private object: {key}")
        if expires_in_seconds <= 0 or expires_in_seconds > 900:
            raise ProviderValidationError("Signed URL TTL must be between 1 and 900 seconds.")
        return f"https://fake-r2.local/{key}?expires={expires_in_seconds}"

    def delete_object(self, *, key: str) -> None:
        self._guard_mode()
        self.objects.pop(key, None)

    def _guard_mode(self) -> None:
        if self.mode == "timeout":
            raise ProviderTimeout("Fake R2 timeout.")
        if self.mode == "failure":
            raise ProviderValidationError("Fake R2 failure.")

