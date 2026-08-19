import asyncio
import secrets
import string
import time

from src import models


class MockClient:
    def __init__(self, name: str, delay: float = 1.0, should_fail: bool = False):
        self.name = name
        self.delay = delay
        self.should_fail = should_fail

    async def generate(self, prompt: str) -> models.ProviderResponse:
        t0 = time.perf_counter()
        await asyncio.sleep(self.delay)

        if self.should_fail:
            raise RuntimeError(f"{self.name} simulated failure")

        res = self.__generate_string()
        t1 = time.perf_counter()
        return models.ProviderResponse(
            provider=self.name,
            text=res,
            latency_seconds=round(t1 - t0, 3),
            success=True,
            error=None,
        )

    def __generate_string(self):
        """Generates a cryptographically secure random alphanumeric string."""

        alphabet = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
        return "".join(secrets.choice(alphabet) for _ in range(25))
