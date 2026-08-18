import asyncio


class AsyncAggregator:
    def __init__(self, clients):
        self.clients = clients

    async def aggregate(self, prompt):
        # """Version 1: Using asyncio.create_task() to create tasks and then gather results"""
        # # 1. Schedule each client's generate() as a running background task on the event loop
        # # tasks = [asyncio.create_task(client.generate(query)) for client in self.clients]
        # # results = await asyncio.gather(*tasks)

        # """Version 2: Using asyncio.gather() directly without creating tasks"""
        results = await asyncio.gather(
            *(client.generate(prompt) for client in self.clients)
        )

        # """ Version 3: With error handling """
        # # coroutines = [client.generate(query) for client in self.clients]

        # # results = await asyncio.gather(*coroutines)
        return results
