"""
def mock_llm_call(prompt: str) -> dict:
    #Simulate an external AI API call.
    delay = random.uniform(0.5, 2.5)
    time.sleep(delay)

    if random.random() < 0.2:
        raise RuntimeError("Mock API request failed")

    return {
        "prompt": prompt,
        "response": f"Mock AI response for: {prompt}",
        "status": "success",
    }
"""

import random
import time
from src.observability.decorators import clock
from lorem_text import lorem


def generate_response(prompt: str) -> str:
    ratio = 3
    target_char_count = len(prompt) * ratio

    filler_pool = lorem.words(20)
    generated_text = filler_pool[:target_char_count]
    return generated_text


@clock
def mock_llm_call(prompt: str) -> dict:
    """Simulate an external AI API call with random latency."""
    network_delay = random.uniform(0.3, 1.0)
    generation_delay = random.uniform(0.5, 1.5)

    time.sleep(network_delay)
    response = generate_response(prompt)
    time.sleep(generation_delay)
    return {
        "prompt": prompt,
        "response": response,
        "network_delay": round(network_delay, 3),
        "generation_delay": round(generation_delay, 3),
        "status": "success",
    }
