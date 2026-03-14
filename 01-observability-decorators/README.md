
# Applied AI LLM Engineering

### Python Observability Toolkit: Execution-Time Decorators & API Latency Tracking

This project demonstrates a **production-style observability utility for Python services** using decorators.

It instruments function execution, measures latency, and records performance metrics for simulated API / LLM calls.

The system simulates external AI requests, records execution time, and produces summary statistics such as **average latency, p95 latency, min/max latency, and total call count**.

---

# 🎯 Project Purpose

Modern backend and AI systems require **observability** to monitor performance, detect bottlenecks, and diagnose failures.

This project demonstrates how to implement **lightweight observability tooling** in Python using clean architecture and modular design.

The project simulates AI/LLM API calls and collects performance metrics similar to what real production systems use.

---

# ✨ Features

• Function latency tracking via decorators
• Thread-safe latency aggregation
• Modular observability architecture
• File-based response logging
• Simulated LLM API calls for testing
• Execution summary with p95 latency metrics

---

# 🧠 Key Concepts Demonstrated

• Python decorators (`functools.wraps`)
• Execution time measurement (`time.perf_counter`)
• Thread-safe metrics collection (`threading.Lock`)
• Modular backend architecture
• File-based logging and output persistence
• Basic observability design patterns used in real services

---


# 🏗 System Architecture

```
Prompts File
      │
      ▼
   main.py
      │
      ▼
  mock_api.py
      │
      ▼
 clock decorator
      │
      ▼
 LatencyTracker
   (metrics.py)
      │
      ▼
    writer.py
      │
      ▼
Logs + Output Files
```
---

# 📁 Project Structure

```
01-observability-decorators/
│
├── main.py
├── README.md
├── requirements.txt
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

# ⚙️ How It Works

1. `mock_api.py` simulates an external AI/LLM API call with random latency.

2. The `clock` decorator measures execution time of each function call.

3. Latency values are recorded by the **LatencyTracker** class in `metrics.py`.

4. `writer.py` writes responses and metrics summaries to files.

5. `main.py` orchestrates execution using prompts loaded from `prompts/prompts.txt`.

---

# ▶️ Running the Project

Clone the repository and run the project:

```bash
pip install -r requirements.txt
python main.py
```

The program will:

• Read prompts from `prompts/prompts.txt`
• Simulate API calls
• Record responses in `output/output.txt`
• Log latency metrics in `logs/log.log`

---

# 📊 Example Console Output

```
********** New Execution started **********

Calling mock_llm_call() with prompt: Explain decorators
[1.2034s] mock_llm_call('Explain decorators')

Calling mock_llm_call() with prompt: What is RAG?
[0.9832s] mock_llm_call('What is RAG?')

********** Execution Completed **********
```

---

# 📈 Example Latency Summary

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

# 🔧 Technologies Used

Python 3
functools
statistics
threading
pathlib
lorem_text (mock response generation)

---

# 🚀 Future Improvements

Possible extensions of this project:

• JSON structured logging
• Async instrumentation using `asyncio`
• Retry decorator with exponential backoff
• FastAPI integration for AI services
• Prometheus metrics exporter
• Distributed tracing support

---

# 📚 Learning Roadmap

This project is part of a larger **Applied AI Engineering learning path**.

### Phase 1 — Python & Backend Foundations

• Observability decorators
• Retry logic & error handling
• Async API aggregation
• FastAPI services

### Phase 2 — Applied ML & NLP

• Embeddings & semantic search
• Vector databases
• Retrieval pipelines

### Phase 3 — AI Systems Engineering

• RAG architectures
• Tool-calling agents
• Memory systems
• Multi-agent workflows

### Phase 4 — Production AI Systems

• Deployment
• Monitoring
• Performance optimization
• System design

---

# 👨‍💻 Author

**Abdullah Jonaed**

Software Engineer transitioning into **Applied AI / LLM Engineering**

---

# 📄 License

This project is licensed under the **MIT License**.

