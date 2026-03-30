# Applied AI LLM Engineering

### Resilient AI API Simulation: Retry, Backoff, and Observability

This project demonstrates a **production-style resilient API system for Python services** with built-in observability.

It simulates unreliable AI/LLM API calls, implements retry logic with exponential backoff and jitter, and records structured logs and latency metrics.

The system models real-world backend behavior under failure conditions and produces performance insights such as **average latency, min/max latency, total calls, and structured execution logs**.

---

# 🎯 Project Purpose

Modern AI systems must handle **failures, latency, and unpredictable external APIs**.

This project demonstrates how to build **resilient and observable systems** by combining:

- Retry mechanisms
- Fault injection (failures & timeouts)
- Structured logging
- Latency tracking

The goal is to simulate how real production AI services behave and how engineers design systems to handle them reliably.

---

# ✨ Features

• Retry decorator with exponential backoff  
• Jitter to prevent retry spikes  
• Exception-based failure handling  
• Structured JSON logging (production-style)  
• Latency tracking via decorators  
• Simulated API failures and timeouts  
• Execution summary with performance metrics  

---

# 🧠 Key Concepts Demonstrated

• Python decorators (`functools.wraps`)  
• Retry patterns (backoff + jitter)  
• Exception handling for resilience  
• Structured logging (JSON format)  
• Execution time measurement (`time.perf_counter`)  
• Modular backend architecture  
• Observability patterns used in production systems  

---

# 🏗 System Architecture
Prompts File
│
▼
main.py
│
▼
mock_api.py (Simulates unreliable AI / LLM API)
│
▼
retry decorator (handles failures)
│
▼
clock decorator (measures latency)
│
▼
LatencyTracker (metrics.py)
│
▼
writer.py
│
▼
Structured Logs + Output Files


---

# 📁 Project Structure
02-retry-observability/
│
├── main.py
├── README.md
├── requirements.txt
│
├── logs/
│ └── app.log
│
├── output/
│ └── output.txt
│
├── prompts/
│ └── prompts.txt
│
├── src/
│ ├── api/
│ │ └── mock_api.py
│ │
│ └── observability/
│ ├── decorators.py
│ ├── metrics.py
│ ├── writer.py
│ ├── logHelper.py
│ └── init.py
│
└── tests/


---


---

# ⚙️ How It Works

1. `mock_api.py` simulates an external AI/LLM API with:
   - random latency
   - injected failures (exceptions)

2. The `retry` decorator:
   - retries failed calls
   - applies exponential backoff
   - adds jitter to avoid retry storms

3. The `clock` decorator:
   - measures execution time
   - records latency metrics

4. `LatencyTracker` aggregates performance metrics.

5. `writer.py`:
   - logs structured JSON events
   - writes API responses and summaries

6. `main.py` orchestrates execution using prompts from `prompts/prompts.txt`.

---

# ▶️ Running the Project

Clone the repository and run:

```bash
pip install -r requirements.txt
python main.py ```

The program will:
• Read prompts from prompts/prompts.txt
• Simulate API calls with failures
• Retry failed requests automatically
• Log structured events in logs/app.log

📊 Example Log (Structured JSON)
{
  "timestamp": "2026-03-27T06:36:22.587994",
  "level": "INFO",
  "event": "latency_summary",
  "total_calls": 5,
  "avg_latency": 1.688,
  "max_latency": 1.901,
  "min_latency": 1.501
}

📈 Example Behavior
Calling mock_llm_call() with prompt: Explain decorators
Attempt 1 failed → retrying...
Attempt 2 failed → retrying...
Attempt 3 succeeded

Calling mock_llm_call() with prompt: What is RAG?
Success on first attempt

🔧 Technologies Used

Python 3
functools
time
random
logging
pathlib

🚀 Future Improvements

Possible extensions:

• Async API calls (asyncio)
• Circuit breaker pattern
• Integration with real LLM APIs
• Metrics export (Prometheus / Grafana)
• Distributed tracing

📚 Learning Roadmap

This project is part of a structured Applied AI Engineering path.

Phase 1 — Backend Foundations

• Observability
• Retry & fault tolerance
• Logging systems

Phase 2 — Applied AI Systems

• Embeddings
• Vector databases
• Retrieval pipelines

Phase 3 — AI System Design

• RAG architectures
• Agent workflows
• Tool usage

Phase 4 — Production AI

• Deployment
• Monitoring
• Scaling systems

👨‍💻 Author

Abdullah Jonaed

Software Engineer transitioning into Applied AI / LLM Engineering

📄 License

This project is licensed under the MIT License.