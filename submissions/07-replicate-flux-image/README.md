# Replicate FLUX Image Generator

**Showcases:** FLUX LoRA Fine-tuning + Fast Inference

## What it does
A custom style image generator using FLUX - the latest state-of-the-art image model. Generate images in any style by leveraging FLUX's LoRA fine-tuning capabilities or use the base model for high-quality generations.

## Latest Feature (2024)
- **FLUX** - State-of-the-art image generation model
- **LoRA Fine-tuning** - Train FLUX on your own images with one API call
- Optimized fast inference (2-5 seconds per image)
- Open-source optimizations available
- Multiple model variants: FLUX.1 [schnell], [dev], [pro]

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and add your Replicate API token:
   ```bash
   cp .env.example .env
   ```

3. Run the image generator:
   ```bash
   python main.py "a futuristic city at sunset"
   ```

## How to Use
- Provide a text prompt describing the image you want
- Optionally specify aspect ratio, number of outputs, etc.
- Images are saved locally and URLs are displayed
- Use `--style` flag to apply custom LoRA styles

## API Reference
- [Replicate Docs](https://replicate.com/docs)
- [FLUX on Replicate](https://replicate.com/black-forest-labs/flux-schnell)
- [Changelog](https://replicate.com/changelog)
