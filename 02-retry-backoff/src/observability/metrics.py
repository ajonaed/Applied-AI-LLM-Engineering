import statistics
import threading


class LatencyTracker:
    def __init__(self):
        self.latencies = []
        self.lock = threading.Lock()

    def record(self, latency):
        with self.lock:
            self.latencies.append(latency)

    def _snapshot(self):
        with self.lock:
            return list(self.latencies)

    def total_calls(self):
        latencies = self._snapshot()
        return len(latencies)

    def average_latency(self):
        latencies = self._snapshot()
        return statistics.mean(latencies) if latencies else 0

    def max_latency(self):
        latencies = self._snapshot()
        return max(latencies) if latencies else 0

    def min_latency(self):
        latencies = self._snapshot()
        return min(latencies) if latencies else 0

    def p95_latency(self):
        latencies = self._snapshot()
        if len(latencies) < 2:
            return 0
        return statistics.quantiles(latencies, n=100)[94]

    def summary(self):
        latencies = self._snapshot()
        if not latencies:
            return {
                "total_calls": 0,
                "avg_latency": 0,
                "p95_latency": 0,
                "max_latency": 0,
                "min_latency": 0,
            }

        return {
            "total_calls": len(latencies),
            "avg_latency": round(statistics.mean(latencies), 3),
            "p95_latency": (
                round(statistics.quantiles(latencies, n=100)[94], 3)
                if len(latencies) >= 2
                else 0
            ),
            "max_latency": round(max(latencies), 3),
            "min_latency": round(min(latencies), 3),
        }
