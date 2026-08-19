import time

import httpx

from src import models
from src.config import OLLAMA_BASE_URL, OLLAMA_MODEL


class OllamaClient:
    def __init__(self, base_url=OLLAMA_BASE_URL, model=OLLAMA_MODEL, name="Ollama"):
        self.base_url = base_url
        self.model = model
        self.name = name

    async def generate(self, prompt):
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        start = time.perf_counter()

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=payload)

        latency = time.perf_counter() - start

        response.raise_for_status()

        data = response.json()

        return models.ProviderResponse(
            provider="Ollama",
            text=data["response"],
            latency_seconds=latency,
            success=True,
        )
