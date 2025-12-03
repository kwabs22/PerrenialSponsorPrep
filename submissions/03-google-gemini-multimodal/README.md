# Google Gemini 2.0 Multimodal Chat

**Showcases:** Gemini 2.0 Flash + Multimodal Live API

## What it does
A multimodal chat application that uses Google's new Gemini 2.0 Flash model to analyze images, answer questions about them, and engage in natural conversation. Demonstrates the enhanced multimodal reasoning capabilities.

## Latest Feature (December 2024)
- **Gemini 2.0 Flash** - Most capable model yet, built for the agentic era
- **Multimodal Live API** - Real-time audio/video streaming input
- Enhanced capabilities: multimodal reasoning, long context, complex instruction following
- Native tool use and compositional function-calling
- Built on Google's 6th-generation Trillium TPUs

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and add your Google AI API key:
   ```bash
   cp .env.example .env
   ```

3. Run the chat:
   ```bash
   python main.py
   ```

## How to Use
- Start the application and type messages or image paths
- Use `image: path/to/image.jpg` to add an image to analyze
- Ask questions about the image or have a general conversation
- Type `quit` to exit

## API Reference
- [Gemini API Docs](https://ai.google.dev/gemini-api/docs)
- [Changelog](https://ai.google.dev/gemini-api/docs/changelog)
