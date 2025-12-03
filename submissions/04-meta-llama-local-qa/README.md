# Meta Llama Local Document Q&A

**Showcases:** Llama 3.2 with llama-stack

## What it does
A local document Q&A system that uses Meta's Llama 3.2 model to answer questions about your documents. Runs entirely on your machine with no API calls needed - perfect for privacy-sensitive use cases.

## Latest Feature (2024)
- **Llama 3.2** - Latest Llama model with improved performance
- **llama-stack** - Official Meta framework for building Llama apps
- Available in 1B, 3B, 11B, and 90B parameter sizes
- Supports text and multimodal inputs (11B+ versions)
- Runs locally via Ollama or llama.cpp

## Setup

1. Install Ollama from https://ollama.ai

2. Pull the Llama 3.2 model:
   ```bash
   ollama pull llama3.2
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Q&A system:
   ```bash
   python main.py document.txt
   ```

## How to Use
- Provide a text document as input
- Ask questions about the document content
- Get answers powered by Llama 3.2 running locally
- No internet connection required after model download

## API Reference
- [Llama Models](https://github.com/meta-llama/llama-models)
- [Llama Stack](https://github.com/meta-llama/llama-stack)
- [Ollama Docs](https://ollama.ai/library/llama3.2)
