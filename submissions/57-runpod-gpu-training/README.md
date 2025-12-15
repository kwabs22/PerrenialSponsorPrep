# RunPod GPU Training

**Showcases:** RunPod Serverless for ML training and inference

## What it does
Access affordable GPU compute for training and inference. RunPod offers community cloud GPUs, serverless endpoints, and persistent storage - ideal for fine-tuning and batch processing.

## Latest Feature (December 2024)
- **Serverless GPU** - Pay per second compute
- **H100 Access** - Latest NVIDIA hardware
- **Template Marketplace** - Pre-built environments
- **Network Volumes** - Shared persistent storage

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
- [RunPod Docs](https://docs.runpod.io/)
- [Serverless API](https://docs.runpod.io/serverless/overview)
