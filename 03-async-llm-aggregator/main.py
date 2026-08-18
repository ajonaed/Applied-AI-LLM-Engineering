import asyncio
import time

from src.aggregator import AsyncAggregator
from src.clients.mock_client import MockClient
from src.clients.ollama_client import OllamaClient


async def main():

    client_1 = MockClient(name="Client 1", delay=2.0)
    client_2 = MockClient(name="Client 2", delay=1.5)

    ollama_client_1 = OllamaClient()
    # result_1 = await ollama_client_1.generate("What is Applied AI vs Agentic AI?")

    ollama_client_2 = OllamaClient()
    # result_2 = await ollama_client_2.generate(
    #     "Which has better job prospects, Applied AI or Agentic AI?"
    # )

    start = time.perf_counter()
    print("Starting aggregation...")
    aggregator = AsyncAggregator(
        clients=[client_1, client_2, ollama_client_1, ollama_client_2]
    )
    aggregator_results = await aggregator.aggregate(
        "I am a software engineer, should I continue Applied AI or Agentic AI?"
    )
    print("Results:", aggregator_results)
    print("Aggregation completed.")
    end = time.perf_counter()
    print(f"Total time taken: {end - start:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
