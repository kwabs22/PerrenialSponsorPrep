"""
New Relic AI Monitoring Demo
Showcases: APM, custom events, AI metrics
"""

import os
from dotenv import load_dotenv
import time
import random

load_dotenv()

NEW_RELIC_LICENSE_KEY = os.getenv("NEW_RELIC_LICENSE_KEY")

# Initialize New Relic
try:
    import newrelic.agent
    if NEW_RELIC_LICENSE_KEY:
        newrelic.agent.initialize()
        print("New Relic agent initialized")
    else:
        print("Warning: NEW_RELIC_LICENSE_KEY not set. Running in demo mode.")
except ImportError:
    print("newrelic not installed. Running in demo mode.")
    newrelic = None

def record_custom_event(event_type: str, params: dict):
    """Record a custom event to New Relic"""
    if newrelic and NEW_RELIC_LICENSE_KEY:
        app = newrelic.agent.application()
        newrelic.agent.record_custom_event(event_type, params, application=app)
    else:
        print(f"  [Demo] Would record: {event_type} = {params}")

def record_llm_metrics(model: str, input_tokens: int, output_tokens: int, latency_ms: float):
    """Record LLM-specific metrics"""
    record_custom_event("LLMInference", {
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "latency_ms": latency_ms,
        "estimated_cost": (input_tokens * 0.00001) + (output_tokens * 0.00003)
    })

def simulate_inference(prompt: str, model: str = "gpt-4"):
    """Simulate an LLM inference with metrics"""
    start = time.time()

    # Simulate processing
    input_tokens = len(prompt.split()) * 2
    output_tokens = random.randint(50, 200)
    time.sleep(random.uniform(0.3, 1.5))

    latency_ms = (time.time() - start) * 1000

    # Record metrics
    record_llm_metrics(model, input_tokens, output_tokens, latency_ms)

    return {
        "content": f"Response to: {prompt[:30]}...",
        "model": model,
        "tokens": input_tokens + output_tokens,
        "latency_ms": latency_ms
    }

def web_transaction_demo():
    """Simulate a web transaction with AI"""
    print("\nWeb Transaction Demo...")

    if newrelic and NEW_RELIC_LICENSE_KEY:
        @newrelic.agent.background_task(name='ai-chat-endpoint')
        def chat_endpoint():
            # Record the transaction
            newrelic.agent.add_custom_attribute('endpoint', '/api/chat')
            newrelic.agent.add_custom_attribute('user_id', 'demo-user-123')

            result = simulate_inference("What is machine learning?", "gpt-4")
            return result

        result = chat_endpoint()
    else:
        print("  [Demo mode] Simulating /api/chat endpoint")
        result = simulate_inference("What is machine learning?", "gpt-4")

    print(f"  Response generated: {result['tokens']} tokens in {result['latency_ms']:.0f}ms")

def batch_inference_demo():
    """Process multiple prompts with tracking"""
    print("\nBatch Inference Demo...")

    prompts = [
        "Explain quantum computing",
        "What is neural network?",
        "Define machine learning",
        "How does NLP work?",
        "What is deep learning?"
    ]

    models = ["gpt-4", "gpt-3.5-turbo", "claude-3-sonnet"]
    total_tokens = 0
    total_cost = 0

    for prompt in prompts:
        model = random.choice(models)
        result = simulate_inference(prompt, model)
        total_tokens += result["tokens"]
        total_cost += result["tokens"] * 0.00002
        print(f"  Processed: {prompt[:25]}... ({model})")

    print(f"\n  Total: {total_tokens} tokens, ${total_cost:.4f} estimated cost")

    # Record batch summary
    record_custom_event("BatchInference", {
        "batch_size": len(prompts),
        "total_tokens": total_tokens,
        "estimated_cost": total_cost
    })

def error_rate_demo():
    """Demonstrate error tracking"""
    print("\nError Rate Demo...")

    success_count = 0
    error_count = 0

    for i in range(10):
        if random.random() < 0.2:  # 20% error rate
            error_count += 1
            record_custom_event("LLMError", {
                "error_type": "RateLimitError",
                "model": "gpt-4",
                "retry_after": 60
            })
            print(f"  Request {i+1}: ERROR (rate limit)")
        else:
            success_count += 1
            simulate_inference(f"Test prompt {i}", "gpt-4")
            print(f"  Request {i+1}: SUCCESS")

    print(f"\n  Success rate: {success_count}/{success_count + error_count}")

def main():
    print("=" * 50)
    print("New Relic AI Monitoring Demo")
    print("=" * 50)

    if NEW_RELIC_LICENSE_KEY:
        print("Connected to New Relic")
    else:
        print("Running in demo mode (no license key)")

    print("\nAvailable demos:")
    print("  1. Single Inference")
    print("  2. Web Transaction")
    print("  3. Batch Inference")
    print("  4. Error Rate Tracking")
    print("  5. Run all demos")

    choice = input("\nSelect demo (1-5): ").strip()

    if choice == "1":
        result = simulate_inference("Hello, how are you?")
        print(f"\nResult: {result}")
    elif choice == "2":
        web_transaction_demo()
    elif choice == "3":
        batch_inference_demo()
    elif choice == "4":
        error_rate_demo()
    elif choice == "5":
        simulate_inference("Test prompt")
        web_transaction_demo()
        batch_inference_demo()
        error_rate_demo()
    else:
        print("Invalid choice")

    if NEW_RELIC_LICENSE_KEY:
        print("\nView metrics at: https://one.newrelic.com")

if __name__ == "__main__":
    main()
