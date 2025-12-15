"""
Groq Ultra-Fast Inference Demo
Showcases: LPU speed, streaming, JSON mode
"""

import os
from dotenv import load_dotenv
import time
import json

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = None
try:
    from groq import Groq
    if GROQ_API_KEY:
        client = Groq(api_key=GROQ_API_KEY)
        print("Groq client initialized")
    else:
        print("Warning: GROQ_API_KEY not set. Running in demo mode.")
except ImportError:
    print("groq not installed. Running in demo mode.")

# Available models
MODELS = {
    "llama-3.2-90b": "llama-3.2-90b-vision-preview",
    "llama-3.1-70b": "llama-3.1-70b-versatile",
    "llama-3.1-8b": "llama-3.1-8b-instant",
    "mixtral-8x7b": "mixtral-8x7b-32768",
    "gemma-7b": "gemma2-9b-it"
}

def chat_completion(prompt: str, model: str = "llama-3.1-8b", temperature: float = 0.7):
    """Basic chat completion with speed tracking"""
    model_id = MODELS.get(model, model)

    if client:
        start = time.time()
        response = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=1024
        )
        elapsed = time.time() - start

        content = response.choices[0].message.content
        tokens = response.usage.total_tokens
        tps = tokens / elapsed if elapsed > 0 else 0

        return {
            "content": content,
            "model": model_id,
            "tokens": tokens,
            "time_s": elapsed,
            "tokens_per_second": tps
        }
    else:
        # Demo mode
        return {
            "content": f"[Demo] Response to: {prompt[:50]}...",
            "model": model_id,
            "tokens": 150,
            "time_s": 0.15,
            "tokens_per_second": 1000  # Simulated Groq speed
        }

def streaming_demo(prompt: str, model: str = "llama-3.1-8b"):
    """Demonstrate streaming responses"""
    model_id = MODELS.get(model, model)

    print(f"\nStreaming from {model}:")
    print("-" * 40)

    if client:
        start = time.time()
        stream = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )

        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                full_response += content

        elapsed = time.time() - start
        print(f"\n\n[Completed in {elapsed:.2f}s]")
    else:
        # Demo mode
        demo_response = "This is a simulated streaming response from Groq's LPU. The actual response would stream at incredible speeds - often exceeding 500 tokens per second!"
        for char in demo_response:
            print(char, end="", flush=True)
            time.sleep(0.01)
        print("\n\n[Demo mode - actual Groq is much faster!]")

def json_mode_demo():
    """Demonstrate structured JSON output"""
    print("\nJSON Mode Demo:")

    prompt = """Analyze this product review and return JSON:
    "This laptop is amazing! Great battery life and super fast. A bit pricey though."

    Return: {"sentiment": "positive/negative/mixed", "pros": [...], "cons": [...], "score": 1-10}"""

    if client:
        response = client.chat.completions.create(
            model=MODELS["llama-3.1-8b"],
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)
        print(json.dumps(result, indent=2))
    else:
        # Demo response
        result = {
            "sentiment": "mixed",
            "pros": ["great battery life", "super fast"],
            "cons": ["pricey"],
            "score": 8
        }
        print(json.dumps(result, indent=2))

def speed_benchmark():
    """Compare inference speed across models"""
    print("\nSpeed Benchmark:")
    print("=" * 50)

    prompt = "Explain quantum computing in exactly 3 sentences."

    for name, model_id in MODELS.items():
        result = chat_completion(prompt, name)
        print(f"{name:20} | {result['tokens']:4} tokens | {result['time_s']:.2f}s | {result['tokens_per_second']:.0f} tok/s")

def conversation_demo():
    """Multi-turn conversation"""
    print("\nConversation Demo:")
    print("Type 'quit' to exit\n")

    messages = []
    model = "llama-3.1-8b"

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'quit':
            break

        messages.append({"role": "user", "content": user_input})

        if client:
            start = time.time()
            response = client.chat.completions.create(
                model=MODELS[model],
                messages=messages
            )
            elapsed = time.time() - start

            assistant_msg = response.choices[0].message.content
            messages.append({"role": "assistant", "content": assistant_msg})

            print(f"\nGroq ({elapsed:.2f}s): {assistant_msg}\n")
        else:
            print(f"\n[Demo] Assistant: I understand you said '{user_input}'\n")

def main():
    print("=" * 50)
    print("Groq Ultra-Fast Inference Demo")
    print("=" * 50)

    if client:
        print("Connected to Groq API")
    else:
        print("Running in demo mode")

    print("\nAvailable demos:")
    print("  1. Single Completion (with speed)")
    print("  2. Streaming Response")
    print("  3. JSON Mode")
    print("  4. Speed Benchmark (all models)")
    print("  5. Conversation Mode")

    choice = input("\nSelect demo (1-5): ").strip()

    if choice == "1":
        result = chat_completion("What makes Groq's LPU faster than GPUs?")
        print(f"\nResponse: {result['content']}")
        print(f"\nSpeed: {result['tokens_per_second']:.0f} tokens/second")
    elif choice == "2":
        streaming_demo("Write a short poem about speed and technology")
    elif choice == "3":
        json_mode_demo()
    elif choice == "4":
        speed_benchmark()
    elif choice == "5":
        conversation_demo()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
