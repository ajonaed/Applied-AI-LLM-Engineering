# from .logHelper import AppLogger
from src.observability.writer import (
    write_from_decorator_clock,
    write_form_decorator_retry,
)
import random
from typing import Callable, Any
import functools
import time
import logging
# from src.observability.metrics import LatencyTracker  # Your LatencyTracker instance
from src.observability.logHelper import AppLogger
from .metrics import shared_tracker as tracker

# Standard practice: Use a dedicated logger for instrumentation
logger = AppLogger.get_logger("logs/app.log")


def clock(func):
    """
    Instrumentation decorator that records execution time and success/failure.
    Preserves metadata using functools.wraps.
    """

    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.perf_counter()

        # Format arguments for logging (careful with large LLM prompts)
        arg_str = ", ".join(
            [repr(arg) for arg in args] + [f"{k}={v!r}" for k, v in kwargs.items()]
        )

        try:
            # Execute the actual function
            result = func(*args, **kwargs)

            # Record Success Metrics
            elapsed = time.perf_counter() - t0
            tracker.record(elapsed)  #

            logger.info(
                "Execution Success",
                extra={
                    "event": "llm_call_success",
                    "function": func.__name__,
                    "elapsed_time": f"{elapsed:.4f}s",
                    "params": arg_str[:100],  # Truncate for log readability
                },
            )
            return result

        except Exception as e:
            # Record Failure Metrics (Crucial for Week 2)
            elapsed = time.perf_counter() - t0
            # We still record the time spent during a failure/timeout
            tracker.record(elapsed)

            logger.error(
                "Execution Failed",
                extra={
                    "event": "llm_call_failure",
                    "function": func.__name__,
                    "elapsed_time": f"{elapsed:.4f}s",
                    "error_type": type(e).__name__,
                    "error_msg": str(e),
                },
            )
            # Re-raise so the @retry decorator can see the error [cite: 59, 60]
            raise

    return clocked


def retry(max_attempts, base_delay=1):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = base_delay
            last_exception = None

            for i in range(max_attempts):
                try:
                    return func(*args, **kwargs)

                except Exception as e:
                    last_exception = e

                    # Check if last attempt
                    if i == max_attempts - 1:
                        break

                    # Add jitter (0 to 50% of delay)
                    jitter = random.uniform(0, delay * 0.5)
                    sleep_time = delay + jitter

                    # Inside your retry decorator's except block:
                    logger.warning(
                        "Retry attempt",
                        extra={
                            "event": "retry_attempt",
                            "attempt": i + 1,
                            "next_delay": round(sleep_time, 2),
                            "error": str(e),
                        },
                    )

                    time.sleep(sleep_time)

                    # Exponential backoff
                    delay *= 2

            raise last_exception

        return wrapper

    return decorator
