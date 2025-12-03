"""
OpenAI Realtime Voice Assistant
Showcases: Realtime API (gpt-4o-realtime-preview) with new voices
1-hour hackathon submission

This demo uses the OpenAI Realtime API for low-latency voice conversations.
"""
import os
import json
import asyncio
import base64
import pyaudio
import websockets
from dotenv import load_dotenv

load_dotenv()

# Audio configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 24000  # OpenAI Realtime API uses 24kHz

# Available voices in the new Realtime API
VOICES = ["alloy", "ash", "ballad", "coral", "echo", "sage", "shimmer", "verse"]


class RealtimeVoiceAssistant:
    def __init__(self, voice="alloy"):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")

        self.voice = voice if voice in VOICES else "alloy"
        self.ws_url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview"
        self.audio = pyaudio.PyAudio()

    async def connect(self):
        """Connect to the Realtime API WebSocket"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "OpenAI-Beta": "realtime=v1"
        }

        print(f"Connecting to OpenAI Realtime API with voice: {self.voice}")

        async with websockets.connect(self.ws_url, extra_headers=headers) as ws:
            # Configure the session
            await ws.send(json.dumps({
                "type": "session.update",
                "session": {
                    "modalities": ["text", "audio"],
                    "voice": self.voice,
                    "instructions": "You are a helpful voice assistant. Keep responses concise and natural.",
                    "input_audio_format": "pcm16",
                    "output_audio_format": "pcm16",
                    "turn_detection": {
                        "type": "server_vad",
                        "threshold": 0.5,
                        "prefix_padding_ms": 300,
                        "silence_duration_ms": 500
                    }
                }
            }))

            print("Connected! Speak into your microphone...")
            print("Press Ctrl+C to exit\n")

            # Run send and receive tasks concurrently
            await asyncio.gather(
                self._send_audio(ws),
                self._receive_responses(ws)
            )

    async def _send_audio(self, ws):
        """Capture and send audio from microphone"""
        stream = self.audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )

        try:
            while True:
                data = stream.read(CHUNK, exception_on_overflow=False)
                audio_b64 = base64.b64encode(data).decode()

                await ws.send(json.dumps({
                    "type": "input_audio_buffer.append",
                    "audio": audio_b64
                }))

                await asyncio.sleep(0.01)  # Small delay to prevent flooding
        finally:
            stream.stop_stream()
            stream.close()

    async def _receive_responses(self, ws):
        """Receive and play audio responses"""
        output_stream = self.audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            output=True,
            frames_per_buffer=CHUNK
        )

        try:
            async for message in ws:
                event = json.loads(message)
                event_type = event.get("type", "")

                if event_type == "response.audio.delta":
                    # Play received audio
                    audio_data = base64.b64decode(event["delta"])
                    output_stream.write(audio_data)

                elif event_type == "response.audio_transcript.delta":
                    # Print transcript as it comes in
                    print(f"Assistant: {event.get('delta', '')}", end="", flush=True)

                elif event_type == "response.audio_transcript.done":
                    print()  # New line after transcript

                elif event_type == "input_audio_buffer.speech_started":
                    print("You: [speaking...]")

                elif event_type == "error":
                    print(f"Error: {event.get('error', {}).get('message', 'Unknown error')}")
        finally:
            output_stream.stop_stream()
            output_stream.close()

    def cleanup(self):
        """Clean up audio resources"""
        self.audio.terminate()


async def main():
    print("=" * 50)
    print("OpenAI Realtime Voice Assistant")
    print("Showcasing: gpt-4o-realtime-preview with new voices")
    print("=" * 50)
    print(f"\nAvailable voices: {', '.join(VOICES)}")

    # Use coral voice (one of the new voices)
    assistant = RealtimeVoiceAssistant(voice="coral")

    try:
        await assistant.connect()
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: Make sure you have access to the Realtime API.")
        print("You may need to join the waitlist at platform.openai.com")
    finally:
        assistant.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
