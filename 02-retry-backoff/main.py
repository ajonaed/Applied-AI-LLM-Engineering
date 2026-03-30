from pathlib import Path

from src.api.mock_api import mock_llm_call
from src.observability.metrics import shared_tracker as tracker
from src.observability.writer import (
    write_latency_summary,
    mark_start_of_execution,
    log_generic_error,
    write_api_output,
)


def main():
    base_dir = Path(__file__).resolve().parent

    prompt_file_path = base_dir / "prompts" / "prompts.txt"

    with open(prompt_file_path, "r") as file:
        prompts = [line.strip() for line in file if line.strip()]

    print("*" * 10 + " New Execution started " + "*" * 10 + "\n")

    mark_start_of_execution()

    for prompt in prompts:
        try:
            
            mock_llm_call(prompt)
            write_api_output(prompt, "Success")
        except Exception as exc:
            # This ONLY runs if ALL retries failed
            log_generic_error({"e": exc, "prompt": prompt})
            write_api_output(prompt, "FAILED")

    latency_info = tracker.summary()
    write_latency_summary(latency_info)

    print("\n" + "*" * 10 + " Execution Completed " + "*" * 10 + "\n")


if __name__ == "__main__":
    main()
