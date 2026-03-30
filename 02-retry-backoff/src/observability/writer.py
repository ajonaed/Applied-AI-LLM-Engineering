from .logHelper import AppLogger
from pathlib import Path
import time
from datetime import datetime

base_dir = Path(__file__).resolve().parent.parent.parent
print(base_dir)
log_file_path = base_dir / "logs" / "app.log"
output_file_path = base_dir / "output" / "output.txt"

log_file_path.parent.mkdir(parents=True, exist_ok=True)
output_file_path.parent.mkdir(parents=True, exist_ok=True)


def mark_start_of_execution():
    #     with open(log_file_path, "a") as file:
    #         file.write(
    #             "\n\n"
    #             + "*" * 10
    #             + " New Execution : "
    #             + str(datetime.now())
    #             + " "
    #             + "*" * 10
    #             + "\n\n"
    #         )
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


def write_api_output(prompt, response):
    print(prompt, response)
    with open(output_file_path, "a") as file:
        file.write("*" * 40 + "\n")
        file.write(f"Calling mock_llm_call() with prompt: {prompt}\n")
        file.write("*" * 40 + "\n")
        file.write(f"Response: {response}\n")
        file.write("*" * 40 + "\n\n")


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

    logger.error(
        "error_event",
        extra={
            "extra_data": {
                "event": "error",
                "exception": str(data["e"]),
                "thread": data["thread"],
                "prompt": data["prompt"],
            }
        },
    )
