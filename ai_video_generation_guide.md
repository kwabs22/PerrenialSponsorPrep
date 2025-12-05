# AI Video Generation Tools Guide

> Comprehensive guide to AI video generation including talking avatars, lip-sync, text-to-video, and image-to-video tools.

---

## Table of Contents

1. [Commercial Tools](#commercial-tools)
   - [Hedra](#hedra)
   - [Kling AI](#kling-ai)
   - [Other Commercial Options](#other-commercial-options)
2. [Open Source Alternatives](#open-source-alternatives)
   - [Text-to-Video Models](#text-to-video-models)
   - [Lip-Sync Models](#lip-sync-models)
   - [Image-to-Video Models](#image-to-video-models)
3. [Free Tier Options](#free-tier-options)
4. [Comparison Matrix](#comparison-matrix)
5. [Hardware Requirements](#hardware-requirements)
6. [Resources](#resources)

---

## Commercial Tools

### Hedra

**AI Studio for Video, Image, and Audio Generation**

[Website](https://www.hedra.com) | [Pricing](https://www.hedra.com/pricing)

Hedra provides an all-in-one AI studio supporting multiple models including Sora, Veo, Kling, Character-3, and various image generators. You're charged based on usage duration rather than fixed batches.

#### Pricing Tiers

| Plan | Price | Credits/Month | Generation Speed | Commercial Use |
|------|-------|---------------|------------------|:--------------:|
| **Free** | $0 | 300 | Slower | ❌ |
| **Basic** | $10/mo | 1,500 | Slower | ❌ |
| **Creator** | $30/mo | 5,400 | Faster | ✅ |
| **Professional** | $75/mo | 14,400 | Fastest | ✅ |
| **Enterprise** | Custom | Custom | Fastest | ✅ |

#### Key Features
- Multiple AI models in one platform
- Character-3 for talking avatars
- Pay-per-second pricing model
- Extra credits purchasable on paid plans

---

### Kling AI

**Professional AI Video Generation API**

[Website](https://klingai.com) | [Developer Pricing](https://klingai.com/global/dev/pricing)

Kling AI provides enterprise-grade video generation APIs including text-to-video, image-to-video, lip-sync, and virtual try-on capabilities.

#### API Pricing

| Service | Model | Duration | Credits | Cost (USD) |
|---------|-------|----------|---------|------------|
| **Video Gen** | V2-5-Turbo Standard | 5s | 1.5 | $0.21 |
| **Video Gen** | V2-5-Turbo Pro | 10s | 5 | $0.70 |
| **Video Gen** | V1 Standard | 5s | 1 | $0.14 |
| **Video Gen** | V1 Pro | 10s | 7 | $0.98 |
| **Lip-Sync** | Any | 5s | 0.5 | $0.07 |
| **Text-to-Image** | V2-1 | - | 4 | $0.014 |
| **Image-to-Image** | V2 | - | 8-16 | $0.028-0.056 |
| **Virtual Try-On** | V1/V1-5 | - | 1 | $0.07 |

#### Key Features
- High-quality video generation (up to 10s)
- Professional lip-sync at $0.07/5s
- Virtual try-on for e-commerce
- Volume-tiered discounts available
- Comprehensive API documentation

---

### Other Commercial Options

| Tool | Specialty | Free Tier | Paid From |
|------|-----------|-----------|-----------|
| **HeyGen** | Talking avatars | Limited | $29/mo |
| **Synthesia** | AI presenters | ❌ | $29/mo |
| **Runway** | Gen-3 video | 125 credits | $15/mo |
| **Pika** | Stylized video | Limited | $10/mo |
| **Luma AI** | Dream Machine | Limited | $29/mo |

---

## Open Source Alternatives

### Text-to-Video Models

#### HunyuanVideo (Tencent)
**Best for: Cinematic quality, high text-video alignment**

- **Parameters**: 13 billion
- **VRAM**: 24GB+ recommended
- **License**: Open source
- **Features**: 3D VAE for video compression, multimodal language models

```bash
# Install via Hugging Face
pip install diffusers transformers accelerate
```

#### Open Sora 2.0 (HPC-AI Tech)
**Best for: Unified text-to-video and image-to-video**

- **Parameters**: 11 billion
- **Resolution**: 256px or 768px
- **License**: Fully open source (code + checkpoints)
- **Features**: Flux text-to-image integration, ComfyUI compatible

```bash
# Clone and setup
git clone https://github.com/hpcaitech/Open-Sora
cd Open-Sora
pip install -e .
```

#### Wan 2.1/2.2 (Alibaba)
**Best for: Low VRAM, accessible hardware**

- **Parameters**: 1.3B (T2V model)
- **VRAM**: Only 8.19GB required
- **License**: Open source
- **Features**: Smooth transitions, natural motion, MoE architecture (2.2)

```bash
# Run via ComfyUI or Diffusers
pip install diffusers
# Model: wan-video/wan-2.1-t2v-480p
```

#### Mochi 1 (Genmo)
**Best for: Smooth motion, 30fps output**

- **Parameters**: 10 billion
- **VRAM**: ~60GB (single GPU)
- **License**: Apache 2.0
- **Resolution**: 480p (HD coming)
- **Duration**: Up to 5.4 seconds

```bash
git clone https://github.com/genmoai/mochi
cd mochi
pip install -e .

# Free playground: genmo.ai/play
```

#### CogVideoX (Tsinghua)
**Best for: Consumer GPUs, beginners**

- **Parameters**: 5B
- **VRAM**: 8-12GB
- **License**: Open source
- **Features**: Cinematic realism, educational demos

```bash
pip install diffusers
# Model: THUDM/CogVideoX-5b
```

#### SkyReels V1 (Community)
**Best for: Cinematic human characters**

- **Base**: HunyuanVideo fine-tune
- **Training**: 10M+ film/TV clips
- **Features**: 33 expressions, 400+ movements
- **License**: Fully open source

---

### Lip-Sync Models

#### Wav2Lip
**Industry standard for accurate lip sync**

- **Quality**: Best with DeepFaceLab combo
- **License**: Open source
- **Setup**: Technical (requires training)

```bash
git clone https://github.com/Rudrabha/Wav2Lip
cd Wav2Lip
pip install -r requirements.txt
```

#### SadTalker
**Best for: Animating still images from audio**

- **License**: Open source
- **Platforms**: Hugging Face Spaces, Google Colab
- **Cost**: Free

```bash
# Try on Hugging Face
# https://huggingface.co/spaces/vinthony/SadTalker
```

#### LatentSync (ByteDance)
**Best for: High-resolution lip sync**

- **Architecture**: Diffusion model
- **VRAM**: Low requirements
- **License**: Open source
- **Features**: Stable lip motion

```bash
git clone https://github.com/bytedance/LatentSync
```

#### MuseTalk (Tencent)
**Best for: Zero-shot multi-modal inputs**

- **License**: Open source
- **Access**: Free on Fal, Sieve, Replicate
- **Features**: Video + audio inputs

#### LivePortrait
**Best for: Generated avatars with identity retention**

- **License**: Open source
- **Quality**: Most realistic for generated faces

---

### Image-to-Video Models

#### Stable Video Diffusion (Stability AI)
**The foundational open model**

- **Versions**: SVD-14, SVD-25 (frames)
- **Frame Rate**: 3-30 fps configurable
- **Duration**: Up to 4 seconds
- **License**: Research (check commercial terms)

```bash
pip install diffusers
# Model: stabilityai/stable-video-diffusion-img2vid
```

#### AnimateDiff
**Best for: Animating existing images**

- **License**: Open source
- **Integration**: ComfyUI, Automatic1111
- **Features**: Style transfer, motion modules

---

## Free Tier Options

### Fully Free (Open Source)

| Tool | Type | VRAM Needed | Quality |
|------|------|-------------|---------|
| **Wan 2.1** | Text-to-Video | 8GB | High |
| **CogVideoX** | Text-to-Video | 8-12GB | High |
| **SadTalker** | Lip-Sync | 4-8GB | Good |
| **MuseTalk** | Lip-Sync | 8GB | High |
| **Wav2Lip** | Lip-Sync | 4GB | Best |
| **SVD** | Image-to-Video | 12GB | High |

### Free Tiers (Commercial)

| Tool | Free Allowance | Limitations |
|------|----------------|-------------|
| **Hedra** | 300 credits/mo | Non-commercial, slow |
| **A2E** | Unlimited | Watermarks |
| **Vidnoz** | Limited | Watermarks |
| **Veed.io** | Limited | Watermarks |
| **Magic Hour** | Trial credits | Limited duration |
| **Genmo** | Playground access | 480p only |

---

## Comparison Matrix

### By Use Case

| Use Case | Best Commercial | Best Open Source | Best Free |
|----------|-----------------|------------------|-----------|
| **Talking Avatars** | Hedra, HeyGen | SadTalker, MuseTalk | SadTalker |
| **Lip-Sync** | Kling ($0.07/5s) | Wav2Lip, LatentSync | Wav2Lip |
| **Text-to-Video** | Kling, Runway | HunyuanVideo, Wan 2.1 | Wan 2.1 |
| **Image-to-Video** | Kling | SVD, AnimateDiff | SVD |
| **Cinematic Quality** | Sora (via Hedra) | HunyuanVideo, SkyReels | Open Sora |
| **Virtual Try-On** | Kling | - | - |

### By Budget

| Budget | Recommended Stack |
|--------|-------------------|
| **$0** | Wan 2.1 + SadTalker + SVD |
| **< $30/mo** | Hedra Creator + local lip-sync |
| **< $100/mo** | Kling API + Hedra Pro |
| **Enterprise** | Kling Enterprise + Hedra Enterprise |

### By Hardware

| GPU VRAM | Compatible Models |
|----------|-------------------|
| **4-8GB** | Wav2Lip, SadTalker, Text2Video-Zero |
| **8-12GB** | Wan 2.1, CogVideoX, MuseTalk, LTXVideo |
| **16-24GB** | SVD, AnimateDiff, LatentSync |
| **24GB+** | HunyuanVideo, Open Sora, Mochi 1 |
| **Cloud** | All models via Replicate/Fal |

---

## Hardware Requirements

### Minimum Specs by Model

| Model | VRAM | RAM | Storage |
|-------|------|-----|---------|
| **Wan 2.1 T2V-1.3B** | 8.19GB | 16GB | 10GB |
| **CogVideoX-5B** | 12GB | 32GB | 20GB |
| **Stable Video Diffusion** | 12GB | 16GB | 15GB |
| **HunyuanVideo-13B** | 24GB+ | 64GB | 50GB |
| **Open Sora 2.0** | 24GB+ | 64GB | 50GB |
| **Mochi 1** | 60GB | 128GB | 100GB |

### Cloud Options

| Provider | GPU | Cost/hr | Best For |
|----------|-----|---------|----------|
| **Replicate** | Various | $0.001+/run | API access |
| **Fal.ai** | Various | Pay-per-use | Quick inference |
| **RunPod** | A100/H100 | $1-3/hr | Development |
| **Vast.ai** | Various | $0.20+/hr | Budget training |
| **Lambda Labs** | A100 | $1.10/hr | Production |

---

## Integration Examples

### Python: Text-to-Video with Wan 2.1

```python
from diffusers import WanPipeline
import torch

pipe = WanPipeline.from_pretrained(
    "wan-video/wan-2.1-t2v-480p",
    torch_dtype=torch.float16
)
pipe.to("cuda")

video = pipe(
    prompt="A astronaut riding a horse on Mars, cinematic",
    num_frames=24,
    guidance_scale=7.5
).frames[0]

# Save video
from diffusers.utils import export_to_video
export_to_video(video, "output.mp4", fps=8)
```

### Python: Lip-Sync with SadTalker

```python
# Using SadTalker API
import requests

response = requests.post(
    "https://api.sadtalker.com/generate",
    files={
        "image": open("avatar.png", "rb"),
        "audio": open("speech.mp3", "rb")
    }
)
video_url = response.json()["video_url"]
```

### ComfyUI Workflow

```json
{
  "nodes": [
    {"type": "WanTextToVideo", "prompt": "Your prompt here"},
    {"type": "VideoPreview"}
  ]
}
```

---

## Resources

### Official Links

**Commercial:**
- [Hedra](https://www.hedra.com) | [Pricing](https://www.hedra.com/pricing)
- [Kling AI](https://klingai.com) | [Dev Pricing](https://klingai.com/global/dev/pricing)
- [Runway](https://runwayml.com)
- [HeyGen](https://heygen.com)

**Open Source:**
- [HunyuanVideo](https://github.com/Tencent/HunyuanVideo)
- [Open Sora](https://github.com/hpcaitech/Open-Sora)
- [Mochi 1](https://github.com/genmoai/mochi)
- [CogVideoX](https://github.com/THUDM/CogVideo)
- [Wan Video](https://huggingface.co/wan-video)
- [SadTalker](https://github.com/OpenTalker/SadTalker)
- [Wav2Lip](https://github.com/Rudrabha/Wav2Lip)
- [LatentSync](https://github.com/bytedance/LatentSync)
- [MuseTalk](https://github.com/TMElyralab/MuseTalk)
- [Stable Video Diffusion](https://github.com/Stability-AI/generative-models)

### Tutorials & Guides
- [Pixazo: Best Open Source Video Models](https://www.pixazo.ai/blog/best-open-source-ai-video-generation-models)
- [Modal: Text-to-Video Guide](https://modal.com/blog/text-to-video-ai-article)
- [Hugging Face: Video Generation](https://huggingface.co/docs/diffusers/en/api/pipelines/text_to_video)

### Playgrounds (Free)
- [Genmo Playground](https://genmo.ai/play) - Mochi 1
- [Hugging Face Spaces](https://huggingface.co/spaces) - Various models
- [Replicate](https://replicate.com/collections/text-to-video) - API access
- [Fal.ai](https://fal.ai) - Quick inference

---

*Last updated: December 2025*
