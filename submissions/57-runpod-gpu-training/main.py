"""
RunPod GPU Training Demo
Showcases: Serverless endpoints, pod management, training jobs
"""

import os
from dotenv import load_dotenv
import time
import json

load_dotenv()

RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")

# Initialize RunPod
runpod = None
try:
    import runpod as rp
    if RUNPOD_API_KEY:
        rp.api_key = RUNPOD_API_KEY
        runpod = rp
        print("RunPod initialized")
    else:
        print("Warning: RUNPOD_API_KEY not set. Running in demo mode.")
except ImportError:
    print("runpod not installed. Running in demo mode.")

def list_available_gpus():
    """List available GPU types"""
    print("\nAvailable GPU Types:")

    if runpod:
        gpus = runpod.get_gpus()
        for gpu in gpus[:10]:
            print(f"  {gpu['id']}: ${gpu.get('securePrice', 'N/A')}/hr")
    else:
        # Demo data
        gpus = [
            {"name": "RTX 4090", "price": "$0.44/hr"},
            {"name": "A100 80GB", "price": "$1.89/hr"},
            {"name": "H100 80GB", "price": "$3.89/hr"},
            {"name": "RTX 3090", "price": "$0.29/hr"},
            {"name": "A40", "price": "$0.79/hr"},
        ]
        for gpu in gpus:
            print(f"  {gpu['name']}: {gpu['price']}")

def create_serverless_endpoint():
    """Create a serverless endpoint"""
    print("\nCreating Serverless Endpoint:")

    if runpod:
        # Create endpoint with a handler
        endpoint = runpod.create_endpoint(
            name="hackathon-demo",
            template_id="your-template-id",  # Pre-built template
            gpu_type_id="NVIDIA RTX 4090",
            min_workers=0,
            max_workers=3
        )
        print(f"  Endpoint created: {endpoint}")
    else:
        print("  [Demo] Would create serverless endpoint")
        print("  Config:")
        print("    - GPU: RTX 4090")
        print("    - Min workers: 0 (scale to zero)")
        print("    - Max workers: 3")

def run_serverless_inference(endpoint_id: str, inputs: dict):
    """Run inference on serverless endpoint"""
    print("\nServerless Inference:")

    if runpod:
        endpoint = runpod.Endpoint(endpoint_id)

        # Synchronous run
        result = endpoint.run_sync(inputs, timeout=60)
        print(f"  Result: {result}")
    else:
        print(f"  [Demo] Would call endpoint with: {inputs}")
        print("  Simulated response: {'output': 'Generated text...'}")

def async_inference_demo(endpoint_id: str):
    """Async inference with status polling"""
    print("\nAsync Inference Demo:")

    inputs = {"prompt": "Write a story about AI"}

    if runpod:
        endpoint = runpod.Endpoint(endpoint_id)

        # Start async job
        run = endpoint.run(inputs)
        print(f"  Job ID: {run.job_id}")

        # Poll status
        while True:
            status = run.status()
            print(f"  Status: {status}")
            if status in ["COMPLETED", "FAILED"]:
                break
            time.sleep(2)

        # Get output
        if status == "COMPLETED":
            output = run.output()
            print(f"  Output: {output}")
    else:
        print("  [Demo] Starting async job...")
        print("  Job ID: demo-job-123")
        for status in ["IN_QUEUE", "IN_PROGRESS", "COMPLETED"]:
            print(f"  Status: {status}")
            time.sleep(1)
        print("  Output: {'text': 'Once upon a time...'}")

def pod_management_demo():
    """Create and manage GPU pods"""
    print("\nPod Management Demo:")

    if runpod:
        # List existing pods
        pods = runpod.get_pods()
        print(f"  Existing pods: {len(pods)}")

        # Create a pod (commented to avoid costs)
        # pod = runpod.create_pod(
        #     name="hackathon-training",
        #     image_name="runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel",
        #     gpu_type_id="NVIDIA RTX 4090",
        #     volume_in_gb=50
        # )
        print("  [Would create pod with PyTorch 2.1 + CUDA 11.8]")
    else:
        print("  [Demo] Pod operations:")
        print("    - Create: runpod.create_pod(...)")
        print("    - List: runpod.get_pods()")
        print("    - Stop: runpod.stop_pod(pod_id)")
        print("    - Terminate: runpod.terminate_pod(pod_id)")

def handler_example():
    """Show RunPod handler example"""
    print("\nRunPod Handler Example:")
    print("-" * 40)

    code = '''
# handler.py - Deploy as serverless endpoint
import runpod
import torch
from transformers import pipeline

# Load model globally (persists between requests)
generator = None

def init():
    global generator
    generator = pipeline("text-generation", model="gpt2", device=0)

def handler(event):
    """Handle inference requests"""
    prompt = event["input"].get("prompt", "")
    max_length = event["input"].get("max_length", 100)

    output = generator(prompt, max_length=max_length)

    return {"output": output[0]["generated_text"]}

# Initialize on cold start
init()

# Start serverless handler
runpod.serverless.start({"handler": handler})
'''
    print(code)

def main():
    print("=" * 50)
    print("RunPod GPU Training Demo")
    print("=" * 50)

    if RUNPOD_API_KEY:
        print("API Key configured")
    else:
        print("Running in demo mode (no API key)")

    print("\nAvailable demos:")
    print("  1. List Available GPUs")
    print("  2. Serverless Endpoint Info")
    print("  3. Async Inference")
    print("  4. Pod Management")
    print("  5. Handler Example")
    print("  6. Run all demos")

    choice = input("\nSelect demo (1-6): ").strip()

    endpoint_id = os.getenv("RUNPOD_ENDPOINT_ID", "demo-endpoint")

    if choice == "1":
        list_available_gpus()
    elif choice == "2":
        create_serverless_endpoint()
    elif choice == "3":
        async_inference_demo(endpoint_id)
    elif choice == "4":
        pod_management_demo()
    elif choice == "5":
        handler_example()
    elif choice == "6":
        list_available_gpus()
        pod_management_demo()
        handler_example()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
