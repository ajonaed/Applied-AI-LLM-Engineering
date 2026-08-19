import asyncio
import time

from src.aggregator import AsyncAggregator
from src.clients.mock_client import MockClient
from src.clients.ollama_client import OllamaClient


async def main():

    client_1 = MockClient(name="Slow Client", delay=3.0, should_fail=True)
    client_2 = MockClient(name="Slow Client", delay=26.0, should_fail=False)
    client_3 = MockClient(name="Client 2", delay=1.5)

    ollama_client_1 = OllamaClient()
    # result_1 = await ollama_client_1.generate("What is Applied AI vs Agentic AI?")

    # ollama_client_2 = OllamaClient()
    # result_2 = await ollama_client_2.generate(
    #     "Which has better job prospects, Applied AI or Agentic AI?"
    # )

    start = time.perf_counter()
    print("Starting aggregation...")
    aggregator = AsyncAggregator(
        clients=[client_1, client_2, client_3, ollama_client_1]
    )
    aggregator_results = await aggregator.aggregate(
        "I am a software engineer, should I continue Applied AI or Agentic AI?"
    )
    # print("Results:", aggregator_results)
    print("\nAggregation Results")
    print("=" * 60)

    for result in aggregator_results:
        print(f"\nProvider : {result.provider}")
        print(f"Status   : {'SUCCESS' if result.success else 'FAILED'}")

        if result.latency_seconds is not None:
            print(f"Latency  : {result.latency_seconds:.2f} seconds")

        if result.success:
            preview = result.text[:200]

            if len(result.text) > 200:
                preview += "..."

            print(f"Response : {preview}")
        else:
            print(f"Error    : {result.error}")

    print("\n" + "=" * 60)
    print("Aggregation completed.")
    end = time.perf_counter()
    print(f"Total time taken: {end - start:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
