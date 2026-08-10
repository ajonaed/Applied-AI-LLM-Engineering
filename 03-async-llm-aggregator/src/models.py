from dataclasses import dataclass


@dataclass(slots=True)
class ProviderResponse:
    provider: str
    text: str
    latency_seconds: float
    success: bool
    error: str | None = None
