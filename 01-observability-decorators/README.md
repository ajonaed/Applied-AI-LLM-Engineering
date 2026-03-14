# Execution-Time Logging Decorator & API Latency Tracker

This project demonstrates a simple **observability utility for Python services** using decorators.
It instruments function execution, measures latency, and records performance metrics for simulated API calls.

The system simulates external AI/LLM requests, records execution time, and produces summary statistics such as average latency and p95 latency.

---

## 🎯 Project Purpose

Modern backend and AI systems require **observability** to monitor performance and diagnose issues.

This project demonstrates:

* Function instrumentation using decorators
* Latency tracking and metrics aggregation
* Structured logging of API responses
* Separation of concerns across modules

---

## 🧠 Key Concepts Demonstrated

* Python decorators (`functools.wraps`)
* Execution time measurement (`time.perf_counter`)
* Thread-safe metrics collection
* Modular project architecture
* File-based logging
* Basic observability design patterns

---

## 📁 Project Structure

```
01-observability-decorators/
│
├── main.py
├── README.md
│
├── logs/
│   └── log.log
│
├── output/
│   └── output.txt
│
├── prompts/
│   └── prompts.txt
│
├── src/
│   └── observability/
│       ├── decorators.py
│       ├── metrics.py
│       ├── mock_api.py
│       ├── writer.py
│       └── __init__.py
│
└── tests/
```

---

## ⚙️ How It Works

1. `mock_api.py` simulates an external AI/LLM API call with random latency.
2. The `clock` decorator measures execution time of the function.
3. Latency is recorded by `LatencyTracker` in `metrics.py`.
4. `writer.py` records responses and latency summaries to files.
5. `main.py` orchestrates execution using prompts from a file.

---

## ▶️ Running the Project

From the project directory:

```bash
python main.py
```

The program will:

* Read prompts from `prompts/prompts.txt`
* Simulate API calls
* Record responses in `output/output.txt`
* Log latency metrics in `logs/log.log`

---

## 📊 Example Console Output

```
********** New Execution started **********

Calling mock_llm_call() with prompt: Explain decorators
[1.2034s] mock_llm_call('Explain decorators')

Calling mock_llm_call() with prompt: What is RAG?
[0.9832s] mock_llm_call('What is RAG?')

********** Execution Completed **********
```

---

## 📈 Example Latency Summary

```
Latency Summary
-------------------------------
total_calls: 5
avg_latency: 1.204 seconds
p95_latency: 1.982 seconds
max_latency: 2.110 seconds
min_latency: 0.823 seconds
```

---

## 🔧 Technologies Used

* Python 3
* `functools`
* `statistics`
* `threading`
* `pathlib`
* `lorem_text` (for mock response generation)

---

## 🚀 Future Improvements

Possible extensions of this project:

* JSON structured logging
* Async instrumentation (`asyncio`)
* Retry decorator with exponential backoff
* API integration with FastAPI
* Prometheus metrics exporter
* Distributed tracing support

---

## 👤 Author

Abdullah Jonaed
Software Engineer transitioning into Applied AI / LLM Engineering

---

## 📄 License

This project is licensed under the MIT License.
