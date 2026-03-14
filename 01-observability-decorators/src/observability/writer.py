def mark_start_of_execution(file_path):
    with open(file_path, "a") as file:
        file.write("\n\n" + "*" * 10 + " New Execution " + "*" * 10 + "\n\n")


def write_latency_summary(file_path, data):
    with open(file_path, "a") as file:
        file.write("*" * 30 + " Latency Summary " + "*" * 30 + "\n")
        for key, value in data.items():
            if key == "total_calls":
                file.write(f"{key}: {value}\n")
            else:
                file.write(f"{key}: {value} seconds\n")
        file.write("*" * 30 + " End Latency Summary " + "*" * 27 + "\n\n")


def write_api_output(file_path, prompt, response):
    with open(file_path, "a") as file:
        file.write("*" * 40 + "\n")
        file.write(f"Calling mock_llm_call() with prompt: {prompt}\n")
        file.write("*" * 40 + "\n")
        file.write(f"Response: {response}\n")
        file.write("*" * 40 + "\n\n")
