# OpenAI Realtime Voice Assistant

**Showcases:** OpenAI Realtime API (gpt-4o-realtime-preview) with new voices

## What it does
A voice-controlled assistant that uses OpenAI's new Realtime API for low-latency, real-time audio conversations. Speak to the assistant and get instant voice responses using the latest voices (alloy, ash, ballad, coral, echo, sage, shimmer, verse).

## Latest Feature (December 2024)
- **gpt-4o-realtime-preview** model with WebSocket-based real-time audio
- New voices: alloy, ash, ballad, coral, echo, sage, shimmer, verse
- Prompt caching support for faster responses
- Rate limits now based on RPM/TPM instead of connections

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and add your OpenAI API key:
   ```bash
   cp .env.example .env
   ```

3. Run the assistant:
   ```bash
   python main.py
   ```

## How to Use
- The script connects to OpenAI's Realtime API via WebSocket
- Speak into your microphone when prompted
- The assistant responds with voice using the selected voice model
- Press Ctrl+C to exit

## API Reference
- [OpenAI Realtime API Docs](https://platform.openai.com/docs/guides/realtime)
- [Changelog](https://platform.openai.com/docs/changelog)
