import asyncio

from .models import ProviderResponse


class AsyncAggregator:
    def __init__(self, clients, timeout=20):
        self.clients = clients
        self.timeout = timeout
        self.results = []

    async def aggregate(self, prompt):
        # """Version 1: Using asyncio.create_task() to create tasks and then gather results"""
        # # 1. Schedule each client's generate() as a running background task on the event loop
        # # tasks = [asyncio.create_task(client.generate(query)) for client in self.clients]
        # # results = await asyncio.gather(*tasks)

        # """Version 2: Using asyncio.gather() directly without creating tasks"""

        # tasks = asyncio.wait_for(
        #     (client.generate(prompt) for client in self.clients), timeout=self.timeout
        # )
        # tasks = []
        # for client in self.clients:
        #     tasks.append(
        #         asyncio.wait_for(client.generate(prompt), timeout=self.timeout)
        #     )
        tasks = [
            asyncio.wait_for(
                client.generate(prompt),
                timeout=self.timeout,
            )
            for client in self.clients
        ]
        response_list = await asyncio.gather(*tasks, return_exceptions=True)

        # """ Version 3: With error handling """
        # # coroutines = [client.generate(query) for client in self.clients]
        for client, result in zip(self.clients, response_list):
            if isinstance(result, TimeoutError):
                self.results.append(
                    ProviderResponse(
                        provider=client.name,
                        text=None,
                        latency_seconds=None,
                        success=False,
                        error=f"{client.name} timed out after {self.timeout} seconds",
                    )
                )
            elif isinstance(result, Exception):
                self.results.append(
                    ProviderResponse(
                        provider=client.name,
                        text=None,
                        latency_seconds=None,
                        success=False,
                        error=str(result),
                    )
                )
            else:
                self.results.append(result)
        # # results = await asyncio.gather(*coroutines)
        return self.results
