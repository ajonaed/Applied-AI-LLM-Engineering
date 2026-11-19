import pytest
from src.clients.mock_client import MockClient
from src.utils.exceptions import TransientProviderError
from src.utils.retry import retry_async


@pytest.mark.asyncio
async def test_retry_recovers_after_transient_failures():
    client = MockClient(
        name="Retry Client",
        delay=0.01,
        failures_before_success=2,
    )

    result = await retry_async(
        client.generate,
        "test prompt",
        max_attempts=3,
        base_delay=0.01,
    )

    assert result.success is True
    assert client.attempt_count == 3


@pytest.mark.asyncio
async def test_retry_exhausts_all_attempts():
    client = MockClient(
        name="Retry Client",
        delay=0.01,
        failures_before_success=10,
    )

    with pytest.raises(TransientProviderError):
        await retry_async(
            client.generate,
            "test prompt",
            max_attempts=3,
            base_delay=0.01,
        )

    assert client.attempt_count == 3


@pytest.mark.asyncio
async def test_non_transient_error_is_not_retried():
    client = MockClient(
        name="Permanent Failure",
        delay=0.01,
        should_fail=True,
    )

    with pytest.raises(RuntimeError):
        await retry_async(
            client.generate,
            "test prompt",
            max_attempts=3,
            base_delay=0.01,
        )

    assert client.attempt_count == 1
