from src.observability.writer import write_latency_summary
from pathlib import Path

data = {
    "total_calls": 5,
    "avg_latency": 3.222,
    "max_latency": 4.882,
    "min_latency": 1.407,
}

base_dir = Path(__file__).resolve().parent
log_file_path = base_dir / "logs" / "log.log"

write_latency_summary(log_file_path, data)
