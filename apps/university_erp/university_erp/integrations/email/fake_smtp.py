from __future__ import annotations

from dataclasses import dataclass

from university_erp.integrations.exceptions import ProviderTimeout, ProviderValidationError


@dataclass(frozen=True)
class EmailSendResult:
    provider: str
    message_id: str
    status: str


class FakeSmtpAdapter:
    provider = "fake_smtp"

    def __init__(self, *, mode: str = "success") -> None:
        self.mode = mode
        self.messages: list[dict] = []

    def send_email(self, *, to: str, subject: str, body: str) -> EmailSendResult:
        if self.mode == "timeout":
            raise ProviderTimeout("Fake SMTP timeout.")
        if self.mode == "failure":
            raise ProviderValidationError("Fake SMTP failure.")
        message = {"to": to, "subject": subject, "body": body}
        self.messages.append(message)
        return EmailSendResult(provider=self.provider, message_id=f"email_{len(self.messages):06d}", status="queued")

