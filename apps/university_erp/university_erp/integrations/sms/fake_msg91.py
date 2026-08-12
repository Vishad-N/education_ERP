from __future__ import annotations

from dataclasses import dataclass

from university_erp.integrations.exceptions import ProviderTimeout, ProviderValidationError


@dataclass(frozen=True)
class SmsSendResult:
    provider: str
    message_id: str
    status: str


class FakeMsg91Adapter:
    provider = "fake_msg91"

    def __init__(self, *, mode: str = "success") -> None:
        self.mode = mode
        self.messages: list[dict] = []

    def send_sms(self, *, to: str, template_id: str, variables: dict[str, str]) -> SmsSendResult:
        if self.mode == "timeout":
            raise ProviderTimeout("Fake MSG91 timeout.")
        if self.mode == "failure":
            raise ProviderValidationError("Fake MSG91 failure.")
        message = {"to": to, "template_id": template_id, "variables": variables}
        self.messages.append(message)
        return SmsSendResult(provider=self.provider, message_id=f"sms_{len(self.messages):06d}", status="queued")

