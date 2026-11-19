import asyncio
import time

from src.aggregator import AsyncAggregator
from src.clients.mock_client import MockClient
from src.clients.ollama_client import OllamaClient
from src.observability.metrics import shared_tracker
from src.observability.writer import (
    mark_start_of_execution,
    write_api_output,
    write_latency_summary,
)


async def main():
    # logging.basicConfig(
    #     level=logging.INFO,
    #     format="%(asctime)s | %(levelname)s | %(message)s",
    # )
    shared_tracker.reset()

    mark_start_of_execution()
    retry_client = MockClient(
        name="Retry Client",
        delay=1.2,
        failures_before_success=2,
    )

    permanent_failure_client = MockClient(
        name="Permanent Failure Client",
        delay=2.2,
        should_fail=True,
    )

    normal_client = MockClient(
        name="Normal Client",
        delay=1.5,
    )
    ollama_client = OllamaClient()

    clients = [
        retry_client,
        permanent_failure_client,
        normal_client,
        ollama_client,
    ]

    aggregator = AsyncAggregator(
        clients=clients,
        timeout=10,
        max_attempts=3,
        base_delay=0.5,
        jitter=0.25,
    )

    start = time.perf_counter()

    print("\nStarting aggregation...\n")

    results = await aggregator.aggregate("Should I continue learning Applied AI?")

    elapsed = time.perf_counter() - start
    write_api_output("Should I continue learning Applied AI?", results, elapsed)
    latency_summary = shared_tracker.summary()

    write_latency_summary(latency_summary)

    print("\nAggregation complete.\n")


if __name__ == "__main__":
    asyncio.run(main())
