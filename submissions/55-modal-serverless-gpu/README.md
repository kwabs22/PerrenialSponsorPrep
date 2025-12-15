# Modal Serverless GPU

**Showcases:** Modal for serverless GPU compute and ML pipelines

## What it does
Run GPU-accelerated code without managing infrastructure. Modal handles container building, scaling, and GPU allocation automatically - perfect for ML inference, training, and batch processing.

## Latest Feature (December 2024)
- **Instant Cold Starts** - Sub-second container startup
- **A100/H100 Support** - Latest NVIDIA GPUs
- **Volume Caching** - Persistent storage for models
- **Web Endpoints** - Deploy APIs instantly

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Authenticate with Modal:
   ```bash
   modal token new
   ```

3. Run the demo:
   ```bash
   modal run main.py
   ```

## API Reference
- [Modal Docs](https://modal.com/docs)
- [GPU Guide](https://modal.com/docs/guide/gpu)
