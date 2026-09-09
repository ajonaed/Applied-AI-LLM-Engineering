import asyncio
import time

import pytest

from src.aggregator import AsyncAggregator
from src.clients.mock_client import MockClient


@pytest.mark.asyncio
async def test_successful_results_are_retained_when_one_provider_fails():
    failing_client = MockClient(
        name="Failing Client",
        delay=0.05,
        should_fail=True,
    )

    successful_client = MockClient(
        name="Successful Client",
        delay=0.05,
    )

    aggregator = AsyncAggregator(
        clients=[failing_client, successful_client],
        timeout=1,
    )

    results = await aggregator.aggregate("test prompt")

    assert len(results) == 2

    assert results[0].provider == "Failing Client"
    assert results[0].success is False
    assert "simulated failure" in results[0].error

    assert results[1].provider == "Successful Client"
    assert results[1].success is True
    assert results[1].error is None
    assert results[1].text is not None


@pytest.mark.asyncio
async def test_slow_provider_times_out_but_fast_provider_succeeds():
    slow_client = MockClient(
        name="Slow Client",
        delay=1.0,
    )

    fast_client = MockClient(
        name="Fast Client",
        delay=0.05,
    )

    aggregator = AsyncAggregator(
        clients=[slow_client, fast_client],
        timeout=0.1,
    )

    results = await aggregator.aggregate("test prompt")

    slow_result = results[0]
    fast_result = results[1]

    assert slow_result.provider == "Slow Client"
    assert slow_result.success is False
    assert "timed out" in slow_result.error

    assert fast_result.provider == "Fast Client"
    assert fast_result.success is True


@pytest.mark.asyncio
async def test_aggregator_does_not_wait_for_full_slow_client_delay():
    slow_client = MockClient(
        name="Slow Client",
        delay=2.0,
    )

    aggregator = AsyncAggregator(
        clients=[slow_client],
        timeout=0.1,
    )

    start = time.perf_counter()

    results = await aggregator.aggregate("test prompt")

    elapsed = time.perf_counter() - start

    assert results[0].success is False
    assert "timed out" in results[0].error

    # The client wanted 2 seconds, but the gateway timeout is 0.1 seconds.
    # Give the test generous overhead so it is not timing-sensitive.
    assert elapsed < 0.5


@pytest.mark.asyncio
async def test_failure_information_identifies_provider_and_reason():
    client = MockClient(
        name="Broken Provider",
        delay=0.01,
        should_fail=True,
    )

    aggregator = AsyncAggregator(
        clients=[client],
        timeout=1,
    )

    results = await aggregator.aggregate("test prompt")

    result = results[0]

    assert result.provider == "Broken Provider"
    assert result.success is False
    assert result.error == "Broken Provider simulated failure"


@pytest.mark.asyncio
async def test_asyncio_timeout_raises_timeout_error():
    async def slow_operation():
        await asyncio.sleep(1)

    with pytest.raises(TimeoutError):
        async with asyncio.timeout(0.05):
            await slow_operation()
