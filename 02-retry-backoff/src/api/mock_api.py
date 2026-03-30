import random
import time
from src.observability.decorators import clock, retry


_attempt_tracker = {}


@retry(
    max_attempts=3, base_delay=1
)  # Outer: Handles the logic of trying again [cite: 59]
@clock  # Inner: Measures the ACTUAL time of the call
def mock_llm_call(prompt: str, mock_failure_count=0) -> dict:
    # 1. Simulate the Network Wait (Always happens first)
    network_delay = random.uniform(0.3, 1.0)
    time.sleep(network_delay)

    # 2. Check for Deterministic Failures (Requirement: Week 2 Testing)
    if mock_failure_count > 0:
        _attempt_tracker[prompt] = _attempt_tracker.get(prompt, 0) + 1
        if _attempt_tracker[prompt] <= mock_failure_count:
            # Raising a specific retriable error
            raise ConnectionError(
                f"Deterministic Failure {_attempt_tracker[prompt]}/{mock_failure_count}"
            )

    # 3. Simulate Random Network Flakes
    if random.random() > 0.9:  # 10% chance of random failure
        raise RuntimeError("Mock API: Random Internal Server Error")

    # 4. Handle Timeouts (Must happen AFTER sleep to be recorded by @clock)
    generation_delay = random.uniform(0.5, 1.5)
    if network_delay + generation_delay > 2.0:  # Threshold of 2s
        time.sleep(0.5)  # Simulate the "hang" before it finally times out
        raise TimeoutError("Request Timed Out")

    # 5. Success Path
    time.sleep(generation_delay)
    return {
        "prompt": prompt,
        "status": "success",
        'response': 'This failure log is exactly what you need to see.',
        "latency": {
            "network": round(network_delay, 3),
            "gen": round(generation_delay, 3),
        },
    }
