import asyncio
import random
import time
from pathlib import Path

from src.observability.logHelper import AppLogger
from src.observability.metrics import shared_tracker
from src.utils.exceptions import TransientProviderError

base_dir = Path(__file__).resolve().parent.parent.parent
log_file_path = base_dir / "logs" / "app.log"
# output_file_path = base_dir / "output" / "output.txt"

log_file_path.parent.mkdir(parents=True, exist_ok=True)
logger = AppLogger.get_logger(str(log_file_path))


async def retry_async(
    operation,
    *args,
    max_attempts=3,
    base_delay=1.0,
    jitter=0.0,
    operation_name=None,
):
    """
    Retry an async operation when it raises TransientProviderError.

    Args:
        operation: Async callable to execute.
        *args: Arguments passed to the async callable.
        max_attempts: Maximum number of total attempts.
        base_delay: Initial backoff delay in seconds.
        jitter: Maximum random delay added to the backoff.
        operation_name: Name used in log messages.

    Returns:
        Result returned by the async operation.

    Raises:
        TransientProviderError:
            Re-raised when all attempts are exhausted.
    """

    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    if base_delay < 0:
        raise ValueError("base_delay cannot be negative")

    if jitter < 0:
        raise ValueError("jitter cannot be negative")

    name = operation_name or getattr(
        operation,
        "__name__",
        "operation",
    )

    for attempt in range(1, max_attempts + 1):
        start = time.perf_counter()

        try:
            result = await operation(*args)

        except TransientProviderError as exc:
            if attempt == max_attempts:
                logger.error(
                    "%s failed after %s attempts: %s",
                    name,
                    max_attempts,
                    exc,
                    extra={
                        "event": "provider_retry_exhausted",
                        "provider": name,
                        "attempt": attempt,
                        "max_attempts": max_attempts,
                        "status": "failed",
                        "error": str(exc),
                    },
                )
                raise

            delay = base_delay * (2 ** (attempt - 1))

            if jitter > 0:
                delay += random.uniform(0, jitter)

            logger.warning(
                "%s failed on attempt %s/%s: %s. Retrying in %.2f seconds.",
                name,
                attempt,
                max_attempts,
                exc,
                delay,
                extra={
                    "event": "provider_retry",
                    "provider": name,
                    "attempt": attempt,
                    "max_attempts": max_attempts,
                    "status": "retrying",
                    "error": str(exc),
                    "retry_delay_seconds": round(delay, 3),
                },
            )

        else:
            logger.info(
                "%s succeeded on attempt %s/%s",
                name,
                attempt,
                max_attempts,
                extra={
                    "event": "provider_attempt",
                    "provider": name,
                    "attempt": attempt,
                    "max_attempts": max_attempts,
                    "status": "success",
                },
            )

            return result

        finally:
            latency = time.perf_counter() - start
            shared_tracker.record(latency)

        await asyncio.sleep(delay)
