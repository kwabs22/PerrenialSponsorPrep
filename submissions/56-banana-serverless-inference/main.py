"""
Banana Serverless Inference Demo
Showcases: Model deployment, API calls, async processing
"""

import os
from dotenv import load_dotenv
import time
import json

load_dotenv()

BANANA_API_KEY = os.getenv("BANANA_API_KEY")
BANANA_MODEL_KEY = os.getenv("BANANA_MODEL_KEY")

# Initialize Banana client
banana = None
try:
    import banana_dev as banana_sdk
    if BANANA_API_KEY:
        banana = banana_sdk
        print("Banana SDK initialized")
    else:
        print("Warning: BANANA_API_KEY not set. Running in demo mode.")
except ImportError:
    print("banana-dev not installed. Running in demo mode.")

def run_inference(model_key: str, inputs: dict):
    """Run inference on a Banana model"""
    if banana and BANANA_API_KEY:
        out = banana.run(BANANA_API_KEY, model_key, inputs)
        return out
    else:
        # Demo response
        return {
            "id": "demo-123",
            "message": "Demo mode - would call Banana API",
            "created": int(time.time()),
            "modelOutputs": [{"output": f"Processed: {inputs}"}]
        }

def start_async(model_key: str, inputs: dict):
    """Start async inference"""
    if banana and BANANA_API_KEY:
        result = banana.start(BANANA_API_KEY, model_key, inputs)
        return result
    else:
        return {"callID": "demo-async-123"}

def check_async(call_id: str):
    """Check async job status"""
    if banana and BANANA_API_KEY:
        result = banana.check(BANANA_API_KEY, call_id)
        return result
    else:
        return {
            "id": call_id,
            "status": "completed",
            "modelOutputs": [{"output": "Demo async result"}]
        }

def image_generation_demo():
    """Demo: Generate an image with a deployed model"""
    print("\nImage Generation Demo:")

    inputs = {
        "prompt": "A futuristic city at sunset, cyberpunk style",
        "negative_prompt": "blurry, low quality",
        "num_inference_steps": 30,
        "guidance_scale": 7.5
    }

    print(f"  Prompt: {inputs['prompt']}")

    # Use a placeholder model key for demo
    model_key = BANANA_MODEL_KEY or "sdxl-demo"
    result = run_inference(model_key, inputs)

    print(f"  Result: {json.dumps(result, indent=2)[:200]}...")

def text_generation_demo():
    """Demo: Run a text generation model"""
    print("\nText Generation Demo:")

    inputs = {
        "prompt": "Explain quantum computing in simple terms:",
        "max_tokens": 200,
        "temperature": 0.7
    }

    print(f"  Prompt: {inputs['prompt']}")

    model_key = BANANA_MODEL_KEY or "llama-demo"
    result = run_inference(model_key, inputs)

    print(f"  Result: {json.dumps(result, indent=2)[:300]}...")

def async_workflow_demo():
    """Demo: Async job processing"""
    print("\nAsync Workflow Demo:")

    # Start job
    inputs = {"data": "process this"}
    print("  Starting async job...")

    result = start_async(BANANA_MODEL_KEY or "demo", inputs)
    call_id = result.get("callID", "demo-123")
    print(f"  Call ID: {call_id}")

    # Poll for completion
    print("  Checking status...")
    for i in range(3):
        time.sleep(1)
        status = check_async(call_id)
        print(f"    Attempt {i+1}: {status.get('status', 'pending')}")
        if status.get("status") == "completed":
            break

    print(f"  Final result: {status}")

def potassium_example():
    """Show Potassium framework example"""
    print("\nPotassium Framework Example:")
    print("-" * 40)

    code = '''
# app.py - Deploy this to Banana
from potassium import Potassium, Request, Response
import torch
from transformers import pipeline

app = Potassium("my-model")

@app.init
def init():
    """Load model on cold start"""
    model = pipeline("text-generation", model="gpt2")
    return {"model": model}

@app.handler()
def handler(context: dict, request: Request) -> Response:
    """Handle inference requests"""
    model = context["model"]
    prompt = request.json.get("prompt", "")

    output = model(prompt, max_length=100)

    return Response(json={"output": output}, status=200)

if __name__ == "__main__":
    app.serve()
'''
    print(code)

def main():
    print("=" * 50)
    print("Banana Serverless Inference Demo")
    print("=" * 50)

    if BANANA_API_KEY:
        print(f"API Key configured")
    else:
        print("Running in demo mode (no API key)")

    print("\nAvailable demos:")
    print("  1. Image Generation")
    print("  2. Text Generation")
    print("  3. Async Workflow")
    print("  4. Potassium Example")
    print("  5. Run all demos")

    choice = input("\nSelect demo (1-5): ").strip()

    if choice == "1":
        image_generation_demo()
    elif choice == "2":
        text_generation_demo()
    elif choice == "3":
        async_workflow_demo()
    elif choice == "4":
        potassium_example()
    elif choice == "5":
        image_generation_demo()
        text_generation_demo()
        async_workflow_demo()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
