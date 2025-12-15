"""
Datadog LLM Observability Demo
Showcases: APM tracing, LLM monitoring, custom metrics
"""

import os
from dotenv import load_dotenv
import time
import random

load_dotenv()

DD_API_KEY = os.getenv("DD_API_KEY")
DD_SITE = os.getenv("DD_SITE", "datadoghq.com")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Datadog tracing
try:
    from ddtrace import tracer, patch_all
    from ddtrace.llmobs import LLMObs

    if DD_API_KEY:
        patch_all()  # Auto-instrument common libraries
        print("Datadog tracing initialized")
    else:
        print("Warning: DD_API_KEY not set. Running in demo mode.")
        tracer = None
except ImportError:
    print("ddtrace not installed. Running in demo mode.")
    tracer = None

def simulate_llm_call(prompt: str, model: str = "gpt-4"):
    """Simulate an LLM API call with tracing"""

    # Simulated response data
    input_tokens = len(prompt.split()) * 2
    output_tokens = random.randint(50, 200)
    latency = random.uniform(0.5, 2.0)

    response = {
        "model": model,
        "content": f"This is a simulated response to: {prompt[:50]}...",
        "usage": {
            "prompt_tokens": input_tokens,
            "completion_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens
        },
        "latency_ms": latency * 1000
    }

    time.sleep(latency)  # Simulate API latency
    return response

def traced_llm_call(prompt: str, model: str = "gpt-4"):
    """LLM call with Datadog tracing"""

    if tracer:
        with tracer.trace("llm.completion", service="hackathon-llm") as span:
            span.set_tag("llm.model", model)
            span.set_tag("llm.prompt_length", len(prompt))

            response = simulate_llm_call(prompt, model)

            # Add LLM-specific tags
            span.set_tag("llm.input_tokens", response["usage"]["prompt_tokens"])
            span.set_tag("llm.output_tokens", response["usage"]["completion_tokens"])
            span.set_tag("llm.total_tokens", response["usage"]["total_tokens"])
            span.set_tag("llm.latency_ms", response["latency_ms"])

            return response
    else:
        return simulate_llm_call(prompt, model)

def rag_pipeline_demo():
    """Demonstrate a traced RAG pipeline"""
    print("\nRunning RAG Pipeline Demo...")

    if tracer:
        with tracer.trace("rag.pipeline", service="hackathon-rag") as parent:
            # Step 1: Embed query
            with tracer.trace("rag.embed_query") as span:
                span.set_tag("embedding.model", "text-embedding-3-small")
                time.sleep(0.1)
                print("  1. Query embedded")

            # Step 2: Vector search
            with tracer.trace("rag.vector_search") as span:
                span.set_tag("vector_db", "pinecone")
                span.set_tag("top_k", 5)
                time.sleep(0.2)
                print("  2. Vector search completed")

            # Step 3: LLM generation
            with tracer.trace("rag.generate") as span:
                response = simulate_llm_call("Answer based on context...", "gpt-4")
                span.set_tag("llm.model", "gpt-4")
                span.set_tag("llm.tokens", response["usage"]["total_tokens"])
                print("  3. Response generated")

            parent.set_tag("rag.total_steps", 3)
    else:
        print("  [Demo mode] Simulating RAG pipeline...")
        time.sleep(0.5)

    print("  Pipeline complete!")

def multi_model_comparison():
    """Compare multiple models with tracing"""
    print("\nMulti-Model Comparison...")

    models = ["gpt-4", "gpt-3.5-turbo", "claude-3-opus"]
    prompt = "Explain quantum computing in simple terms"

    results = []
    for model in models:
        response = traced_llm_call(prompt, model)
        results.append({
            "model": model,
            "tokens": response["usage"]["total_tokens"],
            "latency": response["latency_ms"]
        })
        print(f"  {model}: {response['usage']['total_tokens']} tokens, {response['latency_ms']:.0f}ms")

    return results

def error_tracking_demo():
    """Demonstrate error tracking"""
    print("\nError Tracking Demo...")

    if tracer:
        with tracer.trace("llm.completion", service="hackathon-llm") as span:
            span.set_tag("llm.model", "gpt-4")

            # Simulate an error
            span.set_tag("error", True)
            span.set_tag("error.type", "RateLimitError")
            span.set_tag("error.message", "Rate limit exceeded")

            print("  Error captured and sent to Datadog!")
    else:
        print("  [Demo mode] Would capture RateLimitError")

def main():
    print("=" * 50)
    print("Datadog LLM Observability Demo")
    print("=" * 50)

    if DD_API_KEY:
        print(f"Connected to Datadog ({DD_SITE})")
    else:
        print("Running in demo mode (no DD_API_KEY)")

    print("\nAvailable demos:")
    print("  1. Single LLM Call (with tracing)")
    print("  2. RAG Pipeline (multi-step)")
    print("  3. Multi-Model Comparison")
    print("  4. Error Tracking")
    print("  5. Run all demos")

    choice = input("\nSelect demo (1-5): ").strip()

    if choice == "1":
        response = traced_llm_call("What is the meaning of life?")
        print(f"\nResponse: {response['content']}")
        print(f"Tokens: {response['usage']['total_tokens']}")
    elif choice == "2":
        rag_pipeline_demo()
    elif choice == "3":
        multi_model_comparison()
    elif choice == "4":
        error_tracking_demo()
    elif choice == "5":
        traced_llm_call("Hello, world!")
        rag_pipeline_demo()
        multi_model_comparison()
        error_tracking_demo()
    else:
        print("Invalid choice")

    if DD_API_KEY:
        print("\nCheck your Datadog dashboard:")
        print(f"  https://app.{DD_SITE}/apm/traces")

if __name__ == "__main__":
    main()
