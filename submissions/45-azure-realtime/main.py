"""
Azure OpenAI Realtime Voice Translation
Showcases: gpt-4o-realtime + Voice Translation
"""
import os
import asyncio
import json
from dotenv import load_dotenv

load_dotenv()

# Check for required packages
try:
    import websockets
    HAS_WEBSOCKETS = True
except ImportError:
    HAS_WEBSOCKETS = False

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-realtime-preview")

class AzureRealtimeTranslator:
    """Real-time voice translator using Azure OpenAI."""

    def __init__(self, source_lang: str = "en", target_lang: str = "es"):
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.ws_url = f"{AZURE_OPENAI_ENDPOINT.replace('https', 'wss')}/openai/realtime?api-version=2024-10-01-preview&deployment={AZURE_OPENAI_DEPLOYMENT}"

    async def connect(self):
        """Connect to Azure OpenAI Realtime API."""
        headers = {
            "api-key": AZURE_OPENAI_KEY
        }

        async with websockets.connect(self.ws_url, extra_headers=headers) as ws:
            # Configure session for translation
            await ws.send(json.dumps({
                "type": "session.update",
                "session": {
                    "modalities": ["text", "audio"],
                    "instructions": f"""You are a real-time translator.
                    Listen to speech in {self.source_lang} and translate to {self.target_lang}.
                    Respond with the translation in audio form.
                    Maintain natural speech patterns and tone.""",
                    "voice": "alloy",
                    "input_audio_format": "pcm16",
                    "output_audio_format": "pcm16",
                    "turn_detection": {
                        "type": "server_vad",
                        "threshold": 0.5
                    }
                }
            }))

            print("Connected to Azure OpenAI Realtime")

            # Handle messages
            async for message in ws:
                data = json.loads(message)
                await self.handle_message(data)

    async def handle_message(self, data: dict):
        """Handle incoming messages."""
        msg_type = data.get("type", "")

        if msg_type == "session.created":
            print("Session ready for translation")

        elif msg_type == "response.audio.delta":
            # Audio translation chunk received
            print("Received translated audio chunk")

        elif msg_type == "response.audio_transcript.delta":
            # Text of translation
            text = data.get("delta", "")
            print(f"Translation: {text}", end="", flush=True)

        elif msg_type == "response.done":
            print("\n[Translation complete]")

        elif msg_type == "error":
            print(f"Error: {data.get('error', {}).get('message', 'Unknown')}")

    async def translate_text(self, text: str):
        """Translate text (for demo without audio)."""
        headers = {"api-key": AZURE_OPENAI_KEY}

        async with websockets.connect(self.ws_url, extra_headers=headers) as ws:
            # Configure session
            await ws.send(json.dumps({
                "type": "session.update",
                "session": {
                    "modalities": ["text"],
                    "instructions": f"Translate from {self.source_lang} to {self.target_lang}."
                }
            }))

            # Send text
            await ws.send(json.dumps({
                "type": "conversation.item.create",
                "item": {
                    "type": "message",
                    "role": "user",
                    "content": [{"type": "input_text", "text": text}]
                }
            }))

            await ws.send(json.dumps({"type": "response.create"}))

            # Get response
            async for message in ws:
                data = json.loads(message)
                if data.get("type") == "response.text.delta":
                    print(data.get("delta", ""), end="", flush=True)
                elif data.get("type") == "response.done":
                    break

def main():
    print("=" * 50)
    print("Azure OpenAI Realtime Voice Translation")
    print("=" * 50)

    if not HAS_WEBSOCKETS:
        print("\nInstall: pip install websockets")
        return

    if not AZURE_OPENAI_ENDPOINT or not AZURE_OPENAI_KEY:
        print("\nSetup required:")
        print("1. Create Azure OpenAI resource")
        print("2. Deploy gpt-4o-realtime-preview model")
        print("3. Get endpoint and API key")
        print("4. Copy credentials to .env file")

        print("\n🎙️ Realtime Features:")
        print("  - Low-latency voice I/O")
        print("  - Server-side VAD")
        print("  - Multiple voices")
        print("  - Streaming responses")

        print("\n🌍 Translation Demo:")
        translations = [
            ("Hello, how are you?", "¡Hola, ¿cómo estás?"),
            ("The weather is nice today", "El clima está agradable hoy"),
            ("Thank you very much", "Muchas gracias"),
        ]

        print("\n  English → Spanish:")
        for en, es in translations:
            print(f"  '{en}' → '{es}'")

        print("\n💡 Voice Translation Flow:")
        print("""
1. User speaks in English
2. Audio streamed to Azure OpenAI
3. gpt-4o-realtime processes speech
4. Generates Spanish translation
5. Returns translated audio in real-time
        """)
        return

    print(f"\nEndpoint: {AZURE_OPENAI_ENDPOINT}")
    print(f"Deployment: {AZURE_OPENAI_DEPLOYMENT}")

    # Create translator
    translator = AzureRealtimeTranslator(
        source_lang="English",
        target_lang="Spanish"
    )

    print("\n🌍 Starting real-time translator...")
    print("   (Press Ctrl+C to stop)")

    try:
        asyncio.run(translator.connect())
    except KeyboardInterrupt:
        print("\n\nTranslator stopped")
    except Exception as e:
        print(f"\nConnection error: {e}")
        print("Make sure gpt-4o-realtime-preview is deployed")

if __name__ == "__main__":
    main()
