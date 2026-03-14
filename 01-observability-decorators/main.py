from pathlib import Path

from src.observability.mock_api import mock_llm_call
from src.observability.decorators import tracker
from src.observability.writer import (
    write_latency_summary,
    mark_start_of_execution,
    write_api_output,
)


def main():
    base_dir = Path(__file__).resolve().parent

    prompt_file_path = base_dir / "prompts" / "prompts.txt"
    log_file_path = base_dir / "logs" / "log.log"
    output_file_path = base_dir / "output" / "output.txt"

    # Ensure output directories exist
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    output_file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(prompt_file_path, "r") as file:
        prompts = [line.strip() for line in file if line.strip()]

    print("*" * 10 + " New Execution started " + "*" * 10 + "\n")
    mark_start_of_execution(output_file_path)
    mark_start_of_execution(log_file_path)

    for prompt in prompts:
        try:
            print(f"Calling mock_llm_call() with prompt: {prompt}")
            result = mock_llm_call(prompt)
            response = result["response"]

            write_api_output(output_file_path, prompt, response)
            print("Response recorded in output.txt")

        except Exception as exc:
            print(f"Error processing prompt {prompt!r}: {exc}")

    latency_info = tracker.summary()
    write_latency_summary(log_file_path, latency_info)

    print("\n" + "*" * 10 + " Execution Completed " + "*" * 10 + "\n")


if __name__ == "__main__":
    main()
