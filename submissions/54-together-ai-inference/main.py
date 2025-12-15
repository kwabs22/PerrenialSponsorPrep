"""
Together AI Inference Demo
Showcases: Multi-model inference, embeddings, function calling
"""

import os
from dotenv import load_dotenv
import json

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Initialize Together client
client = None
try:
    from together import Together
    if TOGETHER_API_KEY:
        client = Together(api_key=TOGETHER_API_KEY)
        print("Together AI client initialized")
    else:
        print("Warning: TOGETHER_API_KEY not set. Running in demo mode.")
except ImportError:
    print("together not installed. Running in demo mode.")

# Popular models
MODELS = {
    "llama-3.1-70b": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
    "llama-3.1-8b": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
    "mixtral-8x7b": "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "qwen-72b": "Qwen/Qwen2.5-72B-Instruct-Turbo",
    "codellama-34b": "codellama/CodeLlama-34b-Instruct-hf"
}

EMBEDDING_MODEL = "togethercomputer/m2-bert-80M-8k-retrieval"

def chat_completion(prompt: str, model: str = "llama-3.1-8b", system: str = None):
    """Chat completion with any model"""
    model_id = MODELS.get(model, model)

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    if client:
        response = client.chat.completions.create(
            model=model_id,
            messages=messages,
            max_tokens=1024
        )
        return {
            "content": response.choices[0].message.content,
            "model": model_id,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens
            }
        }
    else:
        return {
            "content": f"[Demo] Response from {model}: {prompt[:50]}...",
            "model": model_id,
            "usage": {"prompt_tokens": 50, "completion_tokens": 100}
        }

def get_embeddings(texts: list):
    """Get text embeddings"""
    if client:
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=texts
        )
        return [e.embedding for e in response.data]
    else:
        # Demo: return fake embeddings
        import random
        return [[random.random() for _ in range(768)] for _ in texts]

def function_calling_demo():
    """Demonstrate function calling with open models"""
    print("\nFunction Calling Demo:")

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get the current weather in a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "City name"},
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                    },
                    "required": ["location"]
                }
            }
        }
    ]

    messages = [{"role": "user", "content": "What's the weather in San Francisco?"}]

    if client:
        response = client.chat.completions.create(
            model=MODELS["llama-3.1-70b"],
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        if response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            print(f"  Function: {tool_call.function.name}")
            print(f"  Arguments: {tool_call.function.arguments}")
        else:
            print(f"  Response: {response.choices[0].message.content}")
    else:
        print("  [Demo] Would call get_weather({\"location\": \"San Francisco\"})")

def model_comparison():
    """Compare responses across models"""
    print("\nModel Comparison:")
    print("=" * 60)

    prompt = "Explain machine learning in one sentence."

    for name, model_id in list(MODELS.items())[:3]:
        result = chat_completion(prompt, name)
        print(f"\n{name}:")
        print(f"  {result['content'][:200]}...")

def code_generation_demo():
    """Code generation with CodeLlama"""
    print("\nCode Generation Demo:")

    prompt = """Write a Python function that implements binary search.
Include type hints and a docstring."""

    result = chat_completion(
        prompt,
        model="codellama-34b",
        system="You are an expert Python programmer. Write clean, efficient code."
    )

    print(result["content"])

def embedding_demo():
    """Demonstrate embeddings for similarity search"""
    print("\nEmbedding Demo:")

    texts = [
        "Machine learning is a subset of AI",
        "Deep learning uses neural networks",
        "The weather is sunny today",
        "Python is a programming language"
    ]

    embeddings = get_embeddings(texts)

    print(f"  Generated {len(embeddings)} embeddings")
    print(f"  Dimension: {len(embeddings[0])}")

    # Simple similarity (dot product of first two)
    if embeddings:
        similarity = sum(a * b for a, b in zip(embeddings[0], embeddings[1]))
        print(f"\n  Similarity between text 1 and 2: {similarity:.4f}")
        print("  (Higher = more similar)")

def streaming_demo():
    """Streaming response demo"""
    print("\nStreaming Demo:")
    print("-" * 40)

    if client:
        stream = client.chat.completions.create(
            model=MODELS["llama-3.1-8b"],
            messages=[{"role": "user", "content": "Write a haiku about AI"}],
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
        print("\n")
    else:
        print("[Demo] Streaming response would appear here...")

def main():
    print("=" * 50)
    print("Together AI Inference Demo")
    print("=" * 50)

    if client:
        print("Connected to Together AI")
    else:
        print("Running in demo mode")

    print("\nAvailable demos:")
    print("  1. Chat Completion")
    print("  2. Model Comparison")
    print("  3. Function Calling")
    print("  4. Code Generation")
    print("  5. Embeddings")
    print("  6. Streaming")

    choice = input("\nSelect demo (1-6): ").strip()

    if choice == "1":
        result = chat_completion("What is Together AI?")
        print(f"\nResponse: {result['content']}")
    elif choice == "2":
        model_comparison()
    elif choice == "3":
        function_calling_demo()
    elif choice == "4":
        code_generation_demo()
    elif choice == "5":
        embedding_demo()
    elif choice == "6":
        streaming_demo()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
