"""
Replicate FLUX Image Generator
Showcases: FLUX LoRA Fine-tuning + Fast Inference
1-hour hackathon submission

This demo generates images using FLUX, the latest SOTA image model.
"""
import os
import sys
import argparse
import requests
from pathlib import Path
import replicate
from dotenv import load_dotenv

load_dotenv()

# FLUX model versions on Replicate
MODELS = {
    "schnell": "black-forest-labs/flux-schnell",  # Fast, 4 steps
    "dev": "black-forest-labs/flux-dev",          # Higher quality, more steps
    "pro": "black-forest-labs/flux-1.1-pro",      # Best quality
}


def generate_image(
    prompt: str,
    model: str = "schnell",
    aspect_ratio: str = "1:1",
    num_outputs: int = 1,
    seed: int = None
) -> list[str]:
    """
    Generate images using FLUX

    Args:
        prompt: Text description of the image
        model: Model variant (schnell, dev, pro)
        aspect_ratio: Image aspect ratio
        num_outputs: Number of images to generate
        seed: Random seed for reproducibility

    Returns:
        List of image URLs
    """
    model_id = MODELS.get(model, MODELS["schnell"])

    input_params = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "num_outputs": num_outputs,
        "output_format": "webp",
        "output_quality": 90,
    }

    if seed is not None:
        input_params["seed"] = seed

    # Run the model
    output = replicate.run(model_id, input=input_params)

    # Handle different output formats
    if isinstance(output, list):
        return [str(url) for url in output]
    return [str(output)]


def download_image(url: str, output_path: str) -> str:
    """Download an image from URL"""
    response = requests.get(url)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path


def main():
    print("=" * 50)
    print("Replicate FLUX Image Generator")
    print("Showcasing: FLUX LoRA + Fast Inference")
    print("=" * 50)

    # Check API token
    if not os.getenv("REPLICATE_API_TOKEN"):
        print("\nError: REPLICATE_API_TOKEN not found")
        print("Get your token from https://replicate.com/account/api-tokens")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Generate images with FLUX")
    parser.add_argument("prompt", nargs="?", help="Text prompt for image generation")
    parser.add_argument("--model", choices=["schnell", "dev", "pro"], default="schnell",
                       help="Model variant (default: schnell)")
    parser.add_argument("--aspect", default="1:1",
                       help="Aspect ratio (1:1, 16:9, 9:16, 4:3, 3:4)")
    parser.add_argument("--count", type=int, default=1,
                       help="Number of images to generate")
    parser.add_argument("--seed", type=int, help="Random seed")
    parser.add_argument("--save", action="store_true", help="Save images locally")
    parser.add_argument("--demo", action="store_true", help="Run demo mode")

    args = parser.parse_args()

    if args.demo or not args.prompt:
        demo_mode()
        return

    print(f"\nPrompt: {args.prompt}")
    print(f"Model: FLUX {args.model}")
    print(f"Aspect Ratio: {args.aspect}")
    print(f"Generating {args.count} image(s)...")
    print("-" * 50)

    try:
        urls = generate_image(
            prompt=args.prompt,
            model=args.model,
            aspect_ratio=args.aspect,
            num_outputs=args.count,
            seed=args.seed
        )

        print(f"\n✅ Generated {len(urls)} image(s)!")

        for i, url in enumerate(urls, 1):
            print(f"\n🖼️ Image {i}: {url}")

            if args.save:
                output_dir = Path("outputs")
                output_dir.mkdir(exist_ok=True)
                filename = f"flux_{i}.webp"
                filepath = output_dir / filename
                download_image(url, str(filepath))
                print(f"   Saved to: {filepath}")

    except Exception as e:
        print(f"\nError generating image: {e}")
        sys.exit(1)


def demo_mode():
    """Run demo with sample prompts"""
    print("\n📸 Demo Mode - FLUX Image Generation")
    print("-" * 50)

    demo_prompts = [
        "A serene Japanese garden with a koi pond, cherry blossoms falling, soft morning light",
        "Cyberpunk cityscape at night, neon signs, flying cars, rain-slicked streets",
        "A cozy coffee shop interior, warm lighting, books on shelves, steam rising from cups",
    ]

    print("\nSample prompts to try:")
    for i, prompt in enumerate(demo_prompts, 1):
        print(f"  {i}. {prompt}")

    print("\n" + "-" * 50)
    choice = input("Enter prompt number (1-3) or your own prompt: ").strip()

    if choice in ["1", "2", "3"]:
        prompt = demo_prompts[int(choice) - 1]
    elif choice:
        prompt = choice
    else:
        prompt = demo_prompts[0]

    print(f"\n🎨 Generating with FLUX schnell...")
    print(f"Prompt: {prompt}")

    try:
        urls = generate_image(prompt, model="schnell")

        print(f"\n✅ Image generated!")
        print(f"🖼️ URL: {urls[0]}")
        print("\nOpen the URL in your browser to view the image.")

        # Offer to save
        save = input("\nSave image locally? (y/n): ").strip().lower()
        if save == "y":
            output_dir = Path("outputs")
            output_dir.mkdir(exist_ok=True)
            filepath = output_dir / "demo_flux.webp"
            download_image(urls[0], str(filepath))
            print(f"Saved to: {filepath}")

    except Exception as e:
        print(f"\nError: {e}")

    # Interactive loop
    print("\n" + "-" * 50)
    print("Continue generating? (type 'quit' to exit)")

    while True:
        prompt = input("\nPrompt: ").strip()
        if not prompt or prompt.lower() == "quit":
            print("Goodbye!")
            break

        print("Generating...")
        try:
            urls = generate_image(prompt, model="schnell")
            print(f"✅ {urls[0]}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
