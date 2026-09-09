import time

import httpx

from src.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from src.models import ProviderResponse
from src.utils.exceptions import (
    ClientTimeoutError,
    ModelNotFoundError,
    ProviderConnectionError,
    ProviderServerError,
    RateLimitExceededError,
)


class OllamaClient:
    def __init__(
        self,
        base_url=OLLAMA_BASE_URL,
        model=OLLAMA_MODEL,
        timeout=15.0,
    ):
        self.name = "Ollama client"
        self.base_url = base_url
        self.timeout = timeout
        self.model = model

    async def generate(self, prompt: str) -> ProviderResponse:
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        start = time.perf_counter()

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    url,
                    json=payload,
                )

        except httpx.ConnectError as exc:
            raise ProviderConnectionError(
                f"{self.name} connection failed: {exc}"
            ) from exc

        except (
            httpx.ReadTimeout,
            httpx.WriteTimeout,
            httpx.PoolTimeout,
        ) as exc:
            raise ClientTimeoutError(f"{self.name} request timed out") from exc

        if response.status_code == 404:
            raise ModelNotFoundError(f"Model '{self.model}' was not found")

        if response.status_code == 429:
            raise RateLimitExceededError(f"{self.name} rate limit exceeded")

        if response.status_code >= 500:
            raise ProviderServerError(
                f"{self.name} server returned HTTP {response.status_code}"
            )

        response.raise_for_status()

        latency = time.perf_counter() - start

        data = response.json()

        return ProviderResponse(
            provider=self.name,
            text=data["response"],
            latency_seconds=latency,
            success=True,
            error=None,
        )
