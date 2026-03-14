import functools
import time

from src.observability.metrics import LatencyTracker

tracker = LatencyTracker()


def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.perf_counter()
        name = func.__name__

        arg_list = [repr(arg) for arg in args]
        arg_list.extend(f"{k}={v!r}" for k, v in kwargs.items())
        arg_str = ", ".join(arg_list)

        try:
            result = func(*args, **kwargs)
            return result
        finally:
            elapsed = time.perf_counter() - t0
            tracker.record(elapsed)
            print(f"[{elapsed:0.4f}s] {name}({arg_str})")

    return clocked
