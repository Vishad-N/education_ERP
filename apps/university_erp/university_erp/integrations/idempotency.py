from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class InMemoryIdempotencyStore:
    """Local proof store; production must use database uniqueness."""

    values: dict[str, Any] = field(default_factory=dict)

    def get(self, key: str) -> Any | None:
        return self.values.get(key)

    def setdefault(self, key: str, value: Any) -> tuple[Any, bool]:
        if key in self.values:
            return self.values[key], False
        self.values[key] = value
        return value, True

    def seen(self, key: str) -> bool:
        return key in self.values

    def mark_seen(self, key: str) -> None:
        self.values[key] = True

