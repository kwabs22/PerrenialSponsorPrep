"""
Google Gemini 2.0 Multimodal Chat
Showcases: Gemini 2.0 Flash + Multimodal capabilities
1-hour hackathon submission

This demo uses Gemini 2.0 Flash for multimodal conversations with images.
"""
import os
import sys
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


def setup_gemini():
    """Configure the Gemini API"""
    api_key = os.getenv("GOOGLE_AI_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_AI_API_KEY not found in environment")

    genai.configure(api_key=api_key)

    # Use Gemini 2.0 Flash - the latest model
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config={
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        },
        system_instruction="""You are a helpful multimodal assistant powered by Gemini 2.0 Flash.
You can analyze images, answer questions, and have natural conversations.
When analyzing images, be detailed and helpful. Point out interesting details."""
    )

    return model


def load_image(image_path: str):
    """Load an image file for Gemini"""
    path = Path(image_path)
    if not path.exists():
        return None

    # Upload the file to Gemini
    return genai.upload_file(path)


def chat_with_gemini(model, chat, user_input: str, image_path: str = None):
    """Send a message to Gemini and get a response"""
    content = []

    # Add image if provided
    if image_path:
        image = load_image(image_path)
        if image:
            content.append(image)
            print(f"[Image loaded: {image_path}]")
        else:
            print(f"[Warning: Could not load image: {image_path}]")

    # Add text
    content.append(user_input)

    # Send message and get response
    response = chat.send_message(content)

    return response.text


def main():
    print("=" * 50)
    print("Google Gemini 2.0 Multimodal Chat")
    print("Showcasing: Gemini 2.0 Flash + Multimodal")
    print("=" * 50)

    try:
        model = setup_gemini()
        chat = model.start_chat(history=[])
        print("\nGemini 2.0 Flash ready!")
        print("\nCommands:")
        print("  - Type a message to chat")
        print("  - Type 'image: path/to/file.jpg' to analyze an image")
        print("  - Type 'quit' to exit")
        print("-" * 50)

    except Exception as e:
        print(f"\nError setting up Gemini: {e}")
        print("Make sure you have a valid GOOGLE_AI_API_KEY")
        sys.exit(1)

    # Chat loop
    while True:
        try:
            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "quit":
                print("Goodbye!")
                break

            # Check for image command
            image_path = None
            if user_input.lower().startswith("image:"):
                parts = user_input.split(":", 1)
                if len(parts) > 1:
                    image_path = parts[1].strip()
                    user_input = input("Question about image (or press Enter for analysis): ").strip()
                    if not user_input:
                        user_input = "Please analyze this image in detail. What do you see?"

            # Get response
            response = chat_with_gemini(model, chat, user_input, image_path)
            print(f"\nGemini: {response}")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Try again or type 'quit' to exit")


def demo_mode():
    """Run a quick demo without user interaction"""
    print("\n[Demo Mode]")
    print("-" * 50)

    model = setup_gemini()

    # Simple text demo
    response = model.generate_content(
        "What are 3 creative ways to use Gemini 2.0's multimodal capabilities in a hackathon project?"
    )

    print("Demo Question: Creative hackathon uses for Gemini 2.0 multimodal?")
    print(f"\nGemini: {response.text}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        try:
            demo_mode()
        except Exception as e:
            print(f"Demo error: {e}")
    else:
        main()
