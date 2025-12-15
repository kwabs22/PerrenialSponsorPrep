"""
Modal Serverless GPU Demo
Showcases: GPU functions, web endpoints, model caching
"""

import os

# Check if running in Modal or locally
try:
    import modal
    IN_MODAL = True
except ImportError:
    IN_MODAL = False
    print("modal not installed. Showing demo structure.")

if IN_MODAL:
    # Create Modal app
    app = modal.App("hackathon-demo")

    # Define image with ML dependencies
    ml_image = modal.Image.debian_slim().pip_install(
        "torch",
        "transformers",
        "accelerate"
    )

    # Volume for model caching
    model_cache = modal.Volume.from_name("model-cache", create_if_missing=True)

    @app.function(gpu="T4", image=ml_image, volumes={"/cache": model_cache})
    def gpu_inference(prompt: str, model_name: str = "gpt2"):
        """Run inference on GPU"""
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        # Check GPU
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Running on: {device}")

        # Load model (cached in volume)
        cache_dir = "/cache/models"
        tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            cache_dir=cache_dir,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32
        ).to(device)

        # Generate
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        outputs = model.generate(**inputs, max_new_tokens=100)
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return {
            "prompt": prompt,
            "response": result,
            "device": device,
            "model": model_name
        }

    @app.function(gpu="T4", image=ml_image)
    def batch_inference(prompts: list):
        """Process multiple prompts in parallel"""
        results = []
        for prompt in prompts:
            result = gpu_inference.local(prompt)
            results.append(result)
        return results

    @app.function()
    def cpu_task(data: dict):
        """CPU-only processing task"""
        import time
        time.sleep(1)  # Simulate processing
        return {"processed": data, "status": "complete"}

    @app.local_entrypoint()
    def main():
        """Entry point when running `modal run`"""
        print("=" * 50)
        print("Modal Serverless GPU Demo")
        print("=" * 50)

        # Single inference
        print("\n1. GPU Inference:")
        result = gpu_inference.remote("The future of AI is")
        print(f"   Prompt: {result['prompt']}")
        print(f"   Response: {result['response'][:200]}...")
        print(f"   Device: {result['device']}")

        # Batch processing
        print("\n2. Batch Processing:")
        prompts = [
            "Machine learning is",
            "Python programming",
            "The best way to learn"
        ]
        results = batch_inference.remote(prompts)
        for r in results:
            print(f"   - {r['prompt']}: {r['response'][:50]}...")

        # CPU task
        print("\n3. CPU Task:")
        result = cpu_task.remote({"key": "value"})
        print(f"   Result: {result}")

        print("\nDemo complete!")

    # Web endpoint
    @app.function()
    @modal.web_endpoint()
    def api_endpoint(prompt: str = "Hello"):
        """HTTP endpoint for inference"""
        result = gpu_inference.remote(prompt)
        return {"result": result}

else:
    # Demo mode when Modal not installed
    def main():
        print("=" * 50)
        print("Modal Serverless GPU Demo (Preview)")
        print("=" * 50)

        print("""
Modal allows you to run GPU code without infrastructure:

1. Define functions with @app.function(gpu="T4")
2. Run remotely with function.remote()
3. Deploy web endpoints with @modal.web_endpoint()

Example:

    @app.function(gpu="A100", image=ml_image)
    def train_model(data):
        # This runs on an A100 GPU in the cloud
        model = load_model()
        model.train(data)
        return model

    # Call from anywhere
    result = train_model.remote(my_data)

Install Modal to try:
    pip install modal
    modal token new
    modal run main.py
        """)

if __name__ == "__main__":
    main()
