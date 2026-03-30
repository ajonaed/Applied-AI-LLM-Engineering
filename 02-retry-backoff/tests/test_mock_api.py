import pytest
from src.api.mock_api import mock_llm_call, _attempt_tracker
from src.observability.metrics import shared_tracker

@pytest.fixture(autouse=True)
def cleanup():
    """Fixture to clear state between tests - prevents 'poisoned' data."""
    _attempt_tracker.clear()
    # Optional: Clear tracker latencies if needed
    shared_tracker.latencies = []
    yield


def test_mock_llm_call_success():
    """Verify happy path returns a dictionary."""
    result = mock_llm_call("test prompt")
    assert isinstance(result, dict)
    assert result["status"] == "success"
    assert "response" in result


def test_mock_llm_call_forced_failure():
    """Verify deterministic failure count triggers ConnectionError."""
    with pytest.raises(ConnectionError):
        mock_llm_call("fail me", mock_failure_count=7)
