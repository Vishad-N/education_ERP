class ProviderError(Exception):
    """Base error for provider adapter failures."""


class ProviderTimeout(ProviderError):
    """Raised when a fake or real provider call exceeds the allowed time."""


class ProviderValidationError(ProviderError):
    """Raised when provider input, signature or state is invalid."""


class ProviderReplayError(ProviderValidationError):
    """Raised when a webhook event was already processed."""

