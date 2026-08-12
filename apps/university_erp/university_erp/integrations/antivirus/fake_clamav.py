from __future__ import annotations

from dataclasses import dataclass

from university_erp.integrations.exceptions import ProviderTimeout, ProviderValidationError


@dataclass(frozen=True)
class ScanResult:
    provider: str
    status: str
    signature: str | None = None


class FakeClamAvAdapter:
    provider = "fake_clamav"

    def __init__(self, *, mode: str = "success") -> None:
        self.mode = mode

    def scan(self, *, body: bytes) -> ScanResult:
        if self.mode == "timeout":
            raise ProviderTimeout("Fake ClamAV timeout.")
        if self.mode == "failure":
            raise ProviderValidationError("Fake ClamAV failure.")
        if b"EICAR" in body:
            return ScanResult(provider=self.provider, status="infected", signature="EICAR-Test-File")
        return ScanResult(provider=self.provider, status="clean")

