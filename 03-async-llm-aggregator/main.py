from pathlib import Path

import asyncio
from src.observability.metrics import shared_tracker as tracker
from src.observability.writer import (
    log_generic_error,
    mark_start_of_execution,
    write_api_output,
    write_latency_summary,
)
from experiments.concurrent_tasks import provider_a, provider_b, provider_c


async def main():
    # base_dir = Path(__file__).resolve().parent

    # prompt_file_path = base_dir / "prompts" / "prompts.txt"

    # with open(prompt_file_path, "r") as file:
    #     prompts = [line.strip() for line in file if line.strip()]

    # print("*" * 10 + " New Execution started " + "*" * 10 + "\n")

    # mark_start_of_execution()

    # for prompt in prompts:
    #     try:
    #         result = mock_llm_call(
    #             prompt,
    #         )
    #         write_api_output(prompt, result["response"])
    #     except Exception as exc:
    #         # This ONLY runs if ALL retries failed
    #         log_generic_error({"e": exc, "prompt": prompt})
    #         write_api_output(prompt, "FAILED")

    # latency_info = tracker.summary()
    # write_latency_summary(latency_info)

    # print("\n" + "*" * 10 + " Execution Completed " + "*" * 10 + "\n")

    a, b, c = await asyncio.gather(provider_a(), provider_b(), provider_c())
    print(a, b, c)
    task_a = asyncio.create_task(provider_a())
    task_b = asyncio.create_task(provider_b())
    task_c = asyncio.create_task(provider_c())
    results_a = await task_a
    results_b = await task_b
    results_c = await task_c
    print(results_a, results_b, results_c)
    # results = await asyncio.gather(task_a, task_b, task_c)
    # print(results)
    



if __name__ == "__main__":
    asyncio.run(main())
