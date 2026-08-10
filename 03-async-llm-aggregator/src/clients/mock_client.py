import asyncio


class MockCClient:
    def __init__(self, name: str, delay: float = 1.0):
        self.name = name
        self.delay = delay

    async def generate(self, prompt: str) -> str:
        await asyncio.sleep(self.delay)
        return f"{self.name} response to '{prompt}'"
