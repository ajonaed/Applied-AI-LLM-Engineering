from datetime import datetime
from pathlib import Path

from .logHelper import AppLogger

base_dir = Path(__file__).resolve().parent.parent.parent
print(base_dir)
log_file_path = base_dir / "logs" / "app.log"
output_file_path = base_dir / "output" / "output.txt"

log_file_path.parent.mkdir(parents=True, exist_ok=True)
output_file_path.parent.mkdir(parents=True, exist_ok=True)


def mark_start_of_execution():
    with open(log_file_path, "a") as file:
        file.write(
            "\n\n"
            + "*" * 10
            + " New Execution : "
            + str(datetime.now())
            + " "
            + "*" * 10
            + "\n\n"
        )
    with open(output_file_path, "a") as file:
        file.write(
            "\n\n"
            + "*" * 10
            + " New Execution : "
            + str(datetime.now())
            + " "
            + "*" * 10
            + "\n\n"
        )


def write_api_output(prompt, resObject, time_elapsed):
    with open(output_file_path, "a") as file:
        file.write("\nAggregation Results")
        file.write("=" * 60)

        for result in resObject:
            file.write(f"\nProvider : {result.provider}\n")

            if result.success:
                file.write("Status   : SUCCESS\n")
                file.write(f"Latency  : {result.latency_seconds:.2f} seconds\n")
                file.write(f"Response : {result.text}\n")

            else:
                file.write("Status   : FAILED\n")
                file.write(f"Error    : {result.error}\n")

        file.write("\n" + "=" * 60)
        file.write("Aggregation completed.\n")
        file.write(f"Total time taken: {time_elapsed:.2f} seconds\n")


def write_latency_summary(data: dict):
    logger = AppLogger.get_logger(str(log_file_path))

    logger.info(
        "latency_summary",
        extra={
            "extra_data": {
                "event": "latency_summary",
                "total_calls": data["total_calls"],
                "avg_latency": data["avg_latency"],
                "max_latency": data["max_latency"],
                "min_latency": data["min_latency"],
            }
        },
    )


def write_from_decorator_clock(data: dict):
    logger = AppLogger.get_logger(str(log_file_path))
    logger.info(
        "Total Execution Time",
        extra={
            "extra_data": {
                "event": "LLM Execution Duration",
                "elapsed_time": data["elapsed_time"],
                "function_name": data["function_name"],
                "prompt": data["prompt"],
            }
        },
    )


def write_form_decorator_retry(data: dict):
    pass


def log_generic_error(data: dict):
    logger = AppLogger.get_logger(str(log_file_path))
    thread_name = data.get("thread", "UnknownThread")
    prompt_val = data.get("prompt", "N/A")
    logger.error(
        "Terminal Execution Failure",
        extra={
            "extra_data": {
                "event": "error",
                "exception": str(data["e"]),
                "thread": thread_name,
                "prompt": prompt_val,
            }
        },
    )
