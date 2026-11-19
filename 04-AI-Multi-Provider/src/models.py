from dataclasses import dataclass


@dataclass(slots=True)
class ProviderResponse:
    provider: str
    text: str | None
    latency_seconds: float | None
    success: bool
    error: str | None = None
