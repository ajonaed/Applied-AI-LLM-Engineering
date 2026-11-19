import asyncio
import secrets
import string
import time

from src.models import ProviderResponse
from src.utils.exceptions import TransientProviderError


class MockClient:
    def __init__(
        self,
        name: str,
        delay: float = 1.0,
        should_fail: bool = False,
        failures_before_success: int = 0,
    ):
        self.name = name
        self.delay = delay
        self.should_fail = should_fail
        self.failures_before_success = failures_before_success
        self.attempt_count = 0

    async def generate(self, prompt: str) -> ProviderResponse:
        self.attempt_count += 1

        start = time.perf_counter()

        await asyncio.sleep(self.delay)

        if self.should_fail:
            raise RuntimeError(f"{self.name} simulated permanent failure")

        if self.attempt_count <= self.failures_before_success:
            raise TransientProviderError(f"{self.name} temporary failure")

        text = self._generate_string()

        latency = time.perf_counter() - start

        return ProviderResponse(
            provider=self.name,
            text=text,
            latency_seconds=round(latency, 3),
            success=True,
            error=None,
        )

    def _generate_string(self) -> str:
        alphabet = string.ascii_letters + string.digits

        return "".join(secrets.choice(alphabet) for _ in range(25))
