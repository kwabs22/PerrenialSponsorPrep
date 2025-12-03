"""
Anthropic Computer Use Demo
Showcases: Claude Computer Use API (Public Beta)
1-hour hackathon submission

This demo analyzes screenshots and suggests computer actions using Claude's
new Computer Use capability.
"""
import os
import sys
import base64
import json
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


def encode_image(image_path: str) -> tuple[str, str]:
    """Encode image to base64 and detect media type"""
    path = Path(image_path)
    suffix = path.suffix.lower()

    media_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp"
    }

    media_type = media_types.get(suffix, "image/png")

    with open(path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    return image_data, media_type


def analyze_screenshot(image_path: str, task: str = None) -> dict:
    """
    Analyze a screenshot using Claude's Computer Use capability

    Args:
        image_path: Path to the screenshot
        task: Optional task description (e.g., "Find the search button")

    Returns:
        Analysis results with suggested actions
    """
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    image_data, media_type = encode_image(image_path)

    # Default task if none provided
    if not task:
        task = "Analyze this screenshot and tell me what you see. Suggest the most useful action I could take."

    # Use computer_use_2024_10_22 beta for computer use capability
    response = client.beta.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        betas=["computer-use-2024-10-22"],
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": f"""You are a computer use assistant. Analyze this screenshot and help the user.

Task: {task}

Please provide:
1. A brief description of what you see on screen
2. The main interactive elements you can identify
3. A suggested action with specific coordinates or element names

Format your suggested action as JSON:
{{
    "action_type": "click" | "type" | "scroll" | "none",
    "target": "description of what to interact with",
    "coordinates": {{"x": number, "y": number}} (if applicable),
    "text": "text to type" (if action_type is "type"),
    "reasoning": "why this action would be helpful"
}}
"""
                    }
                ],
            }
        ],
    )

    return {
        "analysis": response.content[0].text,
        "model": response.model,
        "usage": {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens
        }
    }


def main():
    print("=" * 50)
    print("Anthropic Computer Use Demo")
    print("Showcasing: Claude Computer Use API (Public Beta)")
    print("=" * 50)

    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("\nError: ANTHROPIC_API_KEY not found in environment")
        print("Please set up your .env file with your API key")
        sys.exit(1)

    # Get image path from arguments or use demo
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        task = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        # Demo mode - create a simple test
        print("\nUsage: python main.py <screenshot.png> [task]")
        print("\nExample:")
        print('  python main.py desktop.png "Find the Chrome browser icon"')
        print("\nRunning demo with placeholder...")

        # Create a demo without an image
        demo_analysis()
        return

    # Check if file exists
    if not Path(image_path).exists():
        print(f"\nError: File not found: {image_path}")
        sys.exit(1)

    print(f"\nAnalyzing: {image_path}")
    if task:
        print(f"Task: {task}")
    print("-" * 50)

    try:
        result = analyze_screenshot(image_path, task)

        print("\n[Analysis Result]")
        print(result["analysis"])
        print(f"\n[Model: {result['model']}]")
        print(f"[Tokens: {result['usage']['input_tokens']} in / {result['usage']['output_tokens']} out]")

    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure you have access to the Computer Use beta.")


def demo_analysis():
    """Run a demo analysis without an actual screenshot"""
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    print("\n[Demo Mode - Text-based analysis]")
    print("-" * 50)

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": """Imagine you're analyzing a screenshot of a typical desktop with:
- A web browser open to a search engine
- Some desktop icons on the left
- A taskbar at the bottom

What action would you suggest to help someone who wants to search for "hackathon projects"?

Provide your response as a JSON action:
{
    "action_type": "click" | "type",
    "target": "element description",
    "coordinates": {"x": number, "y": number},
    "text": "text to type" (if applicable),
    "reasoning": "why this action"
}"""
            }
        ],
    )

    print(response.content[0].text)
    print(f"\n[Model: {response.model}]")


if __name__ == "__main__":
    main()
