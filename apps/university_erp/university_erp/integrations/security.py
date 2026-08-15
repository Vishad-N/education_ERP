from __future__ import annotations

import uuid
from datetime import datetime, timedelta


def new_correlation_id() -> str:
	return str(uuid.uuid4())


def mask_identifier(value: str | None, *, visible_suffix: int = 4) -> str | None:
	"""Return a non-sensitive display form for restricted identifiers."""
	if value is None:
		return None
	text = str(value).strip()
	if not text:
		return ""
	if visible_suffix < 0:
		raise ValueError("visible_suffix cannot be negative")
	if len(text) <= visible_suffix:
		return "*" * len(text)
	return "*" * (len(text) - visible_suffix) + text[-visible_suffix:]


def assert_export_allowed(*, status: str, masked: bool, is_privileged: bool) -> None:
	if status != "Approved":
		raise ValueError("Privacy export must be approved before download.")
	if not masked and not is_privileged:
		raise PermissionError("Unmasked privacy exports require a privileged role.")


def retention_expired(created_on: datetime, *, retention_days: int, now: datetime | None = None) -> bool:
	if retention_days < 1:
		raise ValueError("retention_days must be positive")
	return (now or datetime.utcnow()) >= created_on + timedelta(days=retention_days)


def audit_event(*, action: str, entity: str, actor: str, correlation_id: str | None = None) -> dict[str, str | None]:
	return {
		"action": action,
		"entity": entity,
		"actor": actor,
		"correlation_id": correlation_id or new_correlation_id(),
	}
