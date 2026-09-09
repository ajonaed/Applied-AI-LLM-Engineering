import asyncio

from src.models import ProviderResponse
from src.utils.retry import retry_async


class AsyncAggregator:
    def __init__(
        self,
        clients,
        timeout=3,
        max_attempts=3,
        base_delay=1.0,
        jitter=0.0,
    ):
        self.clients = clients
        self.timeout = timeout

        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.jitter = jitter

    async def aggregate(self, prompt):

        tasks = [
            asyncio.wait_for(
                retry_async(
                    client.generate,
                    prompt,
                    max_attempts=self.max_attempts,
                    base_delay=self.base_delay,
                    jitter=self.jitter,
                    operation_name=client.name,
                ),
                timeout=self.timeout,
            )
            for client in self.clients
        ]

        response_list = await asyncio.gather(
            *tasks,
            return_exceptions=True,
        )

        final_results = []

        for client, result in zip(
            self.clients,
            response_list,
        ):
            if isinstance(result, TimeoutError):
                final_results.append(
                    ProviderResponse(
                        provider=client.name,
                        text=None,
                        latency_seconds=None,
                        success=False,
                        error=(f"{client.name} timed out after {self.timeout} seconds"),
                    )
                )

            elif isinstance(result, Exception):
                final_results.append(
                    ProviderResponse(
                        provider=client.name,
                        text=None,
                        latency_seconds=None,
                        success=False,
                        error=str(result),
                    )
                )

            else:
                final_results.append(result)

        return final_results
