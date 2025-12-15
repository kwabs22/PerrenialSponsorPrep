# Banana Serverless Inference

**Showcases:** Banana for serverless ML model deployment

## What it does
Deploy ML models as serverless APIs with Banana. Build once, deploy anywhere - perfect for image generation, LLMs, and custom models with auto-scaling.

## Latest Feature (December 2024)
- **Potassium Framework** - Easy model serving
- **Auto-scaling** - Scale to zero, scale to thousands
- **Custom Models** - Deploy any PyTorch/TF model
- **Streaming** - Real-time response streaming

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and add your API key:
   ```bash
   cp .env.example .env
   ```

3. Run the demo:
   ```bash
   python main.py
   ```

## API Reference
- [Banana Docs](https://docs.banana.dev/)
- [Potassium Framework](https://github.com/bananaml/potassium)
