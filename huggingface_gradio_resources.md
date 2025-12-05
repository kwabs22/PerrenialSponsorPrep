# Hugging Face & Gradio Resources Guide

> Comprehensive guide to Hugging Face Spaces, models, papers, and Gradio for building AI demos and applications.

---

## Table of Contents

1. [Hugging Face Overview](#hugging-face-overview)
2. [Featured Spaces](#featured-spaces)
3. [Spaces by Category](#spaces-by-category)
4. [Models & Papers](#models--papers)
5. [Learning Resources](#learning-resources)
6. [Gradio Documentation](#gradio-documentation)
7. [Gradio Guides](#gradio-guides)
8. [MCP Integration](#mcp-integration)
9. [Deployment & Integration](#deployment--integration)
10. [Community](#community)

---

## Hugging Face Overview

### What is Hugging Face?

Hugging Face is the AI community's home for:
- **Models**: 500K+ pre-trained models
- **Datasets**: 100K+ datasets
- **Spaces**: Free GPU-powered AI demos
- **Papers**: Daily ML research papers

### Key Resources

| Resource | URL | Description |
|----------|-----|-------------|
| Hub | [huggingface.co](https://huggingface.co) | Main platform |
| Spaces | [huggingface.co/spaces](https://huggingface.co/spaces) | AI demo apps |
| Models | [huggingface.co/models](https://huggingface.co/models) | Pre-trained models |
| Datasets | [huggingface.co/datasets](https://huggingface.co/datasets) | ML datasets |
| Papers | [huggingface.co/papers](https://huggingface.co/papers) | Daily papers |
| Forum | [discuss.huggingface.co](https://discuss.huggingface.co/) | Community discussions |
| llms.txt | [huggingface.co/changelog/docs-llms-txt](https://huggingface.co/changelog/docs-llms-txt) | AI-readable docs |

---

## Featured Spaces

### Computer Vision

#### Depth Estimation
| Space | Description | Link |
|-------|-------------|------|
| **Depth Anything 3** | State-of-the-art monocular depth estimation | [depth-anything/depth-anything-3](https://huggingface.co/spaces/depth-anything/depth-anything-3) |

#### Pose Estimation
| Space | Description | Link |
|-------|-------------|------|
| **ViTPose Transformers** | Human pose estimation with Vision Transformers | [hysts/ViTPose-transformers](https://huggingface.co/spaces/hysts/ViTPose-transformers) |

#### Segmentation
| Space | Description | Link |
|-------|-------------|------|
| **SAM3** | Segment Anything Model 3 | [akhaliq/sam3](https://huggingface.co/spaces/akhaliq/sam3) |
| **SAM3 Video** | Video segmentation with SAM3 | [merve/SAM3-video-segmentation](https://huggingface.co/spaces/merve/SAM3-video-segmentation) |

#### 3D & Geometry
| Space | Description | Link |
|-------|-------------|------|
| **VGGT** | Visual Geometry Grounded Transformer (Facebook) | [facebook/vggt](https://huggingface.co/spaces/facebook/vggt) |

### Video Generation

| Space | Description | Link |
|-------|-------------|------|
| **Wan 2.2 on AMD** | Video generation running on AMD hardware | [amd/wan2.2onAMD](https://huggingface.co/spaces/amd/wan2.2onAMD) |
| **Dream Wan 2.2 Faster Pro** | Optimized Wan 2.2 video generation | [dream2589632147/Dream-wan2-2-faster-Pro](https://huggingface.co/spaces/dream2589632147/Dream-wan2-2-faster-Pro) |

### Image Generation

| Space | Description | Link |
|-------|-------------|------|
| **SimpleVectorFlux** | Vector-style image generation with Flux | [renderartist/simplevectorflux](https://huggingface.co/renderartist/simplevectorflux) |

### Language Models

| Space | Description | Link |
|-------|-------------|------|
| **GPT OSS 120B Chatbot** | Open-source 120B parameter chatbot on AMD | [amd/gpt-oss-120b-chatbot](https://huggingface.co/spaces/amd/gpt-oss-120b-chatbot) |

### Creative & Games

| Space | Description | Link |
|-------|-------------|------|
| **3D Game Maker** | AI-powered 3D game creation | [Mi6paulino/3D-Game-Maker](https://huggingface.co/spaces/Mi6paulino/3D-Game-Maker) |

### Finance

| Space | Description | Link |
|-------|-------------|------|
| **Trading Analyst** | AI trading analysis tool | [dami1996/trading-analyst](https://huggingface.co/spaces/dami1996/trading-analyst) |

---

## Spaces by Category

### Browse All Categories

| Category | Link | Use Cases |
|----------|------|-----------|
| **Object Detection** | [spaces?category=object-detection](https://huggingface.co/spaces?category=object-detection) | YOLO, DETR, security, inventory |
| **Speech Synthesis** | [spaces?category=speech-synthesis](https://huggingface.co/spaces?category=speech-synthesis) | TTS, voice cloning, audiobooks |
| **Document Analysis** | [spaces?category=document-analysis](https://huggingface.co/spaces?category=document-analysis) | OCR, PDF parsing, invoices |
| **Financial Analysis** | [spaces?category=financial-analysis](https://huggingface.co/spaces?category=financial-analysis) | Stock prediction, sentiment |
| **Sentiment Analysis** | [spaces?category=sentiment-analysis](https://huggingface.co/spaces?category=sentiment-analysis) | Reviews, social media |
| **Visual QA** | [spaces?category=visual-qa](https://huggingface.co/spaces?category=visual-qa) | Image understanding, VQA |
| **Image Captioning** | [spaces?category=image-captioning](https://huggingface.co/spaces?category=image-captioning) | Alt text, descriptions |
| **Pose Estimation** | [spaces?category=pose-estimation](https://huggingface.co/spaces?category=pose-estimation) | Body tracking, fitness |
| **Face Recognition** | [spaces?category=face-recognition](https://huggingface.co/spaces?category=face-recognition) | Identity, verification |
| **Style Transfer** | [spaces?category=style-transfer](https://huggingface.co/spaces?category=style-transfer) | Art styles, filters |
| **Recommendation Systems** | [spaces?category=recommendation-systems](https://huggingface.co/spaces?category=recommendation-systems) | Products, content |
| **Dataset Creation** | [spaces?category=dataset-creation](https://huggingface.co/spaces?category=dataset-creation) | Labeling, annotation |

### Category Quick Reference

```
Vision:
├── Object Detection    → Security, retail, autonomous
├── Pose Estimation     → Fitness, gaming, AR
├── Face Recognition    → Auth, tagging, analysis
├── Style Transfer      → Art, filters, creative
├── Image Captioning    → Accessibility, search
└── Visual QA           → Multimodal understanding

NLP:
├── Sentiment Analysis  → Reviews, social, support
├── Document Analysis   → PDF, OCR, extraction
└── Financial Analysis  → Trading, reports, risk

Audio:
└── Speech Synthesis    → TTS, voices, accessibility

Data:
├── Dataset Creation    → Annotation, labeling
└── Recommendations     → E-commerce, content
```

---

## Models & Papers

### Notable Researchers

| Profile | Focus | Link |
|---------|-------|------|
| **akhaliq** | AI/ML demos, daily papers | [huggingface.co/akhaliq](https://huggingface.co/akhaliq) |

### Featured Papers

| Paper | Topic | Link |
|-------|-------|------|
| **2511.04217** | Research paper | [papers/2511.04217](https://huggingface.co/papers/2511.04217) |

### Daily Papers

Browse the latest ML research papers at [huggingface.co/papers](https://huggingface.co/papers)

---

## Learning Resources

### Smol Course - Train Small Language Models

A complete course on training efficient language models.

| Resource | Description | Link |
|----------|-------------|------|
| **Course Overview** | Introduction to smol models | [learn/smol-course/unit0/1](https://huggingface.co/learn/smol-course/unit0/1) |
| **Training Playbook** | Interactive training guide | [HuggingFaceTB/smol-training-playbook](https://huggingface.co/spaces/HuggingFaceTB/smol-training-playbook#introduction) |

### Course Topics

```
Unit 0: Introduction
├── What are Small Language Models?
├── Why train small models?
└── Hardware requirements

Unit 1: Data Preparation
├── Dataset selection
├── Tokenization
└── Data cleaning

Unit 2: Training
├── Fine-tuning strategies
├── LoRA/QLoRA
└── Distributed training

Unit 3: Evaluation
├── Benchmarks
├── Human evaluation
└── Deployment
```

### LeRobot - Robotics & Embodied AI

[github.com/huggingface/lerobot](https://github.com/huggingface/lerobot)

Open-source robotics library from Hugging Face:
- Robot learning algorithms
- Simulation environments
- Real robot integration
- Imitation learning
- Reinforcement learning

```bash
# Install LeRobot
pip install lerobot

# Quick start
from lerobot import Robot
robot = Robot("pusht")
robot.train()
```

---

## Gradio Documentation

### Core Documentation

| Doc | Description | Link |
|-----|-------------|------|
| **Walkthrough** | Complete Gradio tutorial | [docs/gradio/walkthrough](https://www.gradio.app/docs/gradio/walkthrough) |
| **HTML Component** | Embed custom HTML | [docs/gradio/html](https://www.gradio.app/docs/gradio/html) |
| **Dataset Component** | Display datasets in UI | [docs/gradio/dataset](https://www.gradio.app/docs/gradio/dataset) |

### Custom Components

Build your own Gradio components:

| Resource | Link |
|----------|------|
| **Component Gallery** | [custom-components/gallery](https://www.gradio.app/custom-components/gallery) |

```python
# Example: Custom component
import gradio as gr

with gr.Blocks() as demo:
    gr.HTML("<h1>Custom HTML</h1>")
    gr.Dataset(
        components=[gr.Textbox()],
        samples=[["Sample 1"], ["Sample 2"]]
    )

demo.launch()
```

---

## Gradio Guides

### Getting Started

| Guide | Description | Link |
|-------|-------------|------|
| **Gradio 6 Migration** | Upgrade to Gradio 6 | [gradio-6-migration-guide](https://www.gradio.app/guides/gradio-6-migration-guide) |

### AI & ML Applications

| Guide | Description | Link |
|-------|-------------|------|
| **LLM Agents** | Build LLM-powered apps | [gradio-and-llm-agents](https://www.gradio.app/guides/gradio-and-llm-agents) |
| **Real-time Speech** | Speech recognition apps | [real-time-speech-recognition](https://www.gradio.app/guides/real-time-speech-recognition) |
| **Named Entity Recognition** | NER interfaces | [named-entity-recognition](https://www.gradio.app/guides/named-entity-recognition) |
| **3D Model Component** | Display 3D models | [how-to-use-3D-model-component](https://www.gradio.app/guides/how-to-use-3D-model-component) |
| **GAN Friends** | Create images with GANs | [create-your-own-friends-with-a-gan](https://www.gradio.app/guides/create-your-own-friends-with-a-gan) |

### Integrations

| Guide | Description | Link |
|-------|-------------|------|
| **Hugging Face Integration** | Connect to HF Hub | [using-hugging-face-integrations](https://www.gradio.app/guides/using-hugging-face-integrations) |
| **FastAPI Integration** | Use with FastAPI | [fastapi-app-with-the-gradio-client](https://www.gradio.app/guides/fastapi-app-with-the-gradio-client) |
| **Discord Bot** | Create Discord bots | [creating-a-discord-bot-from-a-gradio-app](https://www.gradio.app/guides/creating-a-discord-bot-from-a-gradio-app) |

### Dashboards & Data

| Guide | Description | Link |
|-------|-------------|------|
| **Supabase Dashboard** | Real-time Supabase data | [creating-a-dashboard-from-supabase-data](https://www.gradio.app/guides/creating-a-dashboard-from-supabase-data) |
| **Google Sheets Dashboard** | Live Google Sheets | [creating-a-realtime-dashboard-from-google-sheets](https://www.gradio.app/guides/creating-a-realtime-dashboard-from-google-sheets) |

### Deployment

| Guide | Description | Link |
|-------|-------------|------|
| **Share Links** | Understanding Gradio sharing | [understanding-gradio-share-links](https://www.gradio.app/guides/understanding-gradio-share-links) |
| **Deploy with Modal** | Serverless deployment | [deploying-gradio-with-modal](https://www.gradio.app/guides/deploying-gradio-with-modal) |
| **Background Tasks** | Async task processing | [running-background-tasks](https://www.gradio.app/guides/running-background-tasks) |

---

## MCP Integration

### Model Context Protocol with Gradio

Gradio now supports MCP (Model Context Protocol) for AI agent integration.

| Guide | Description | Link |
|-------|-------------|------|
| **Building MCP Server** | Create MCP servers with Gradio | [building-mcp-server-with-gradio](https://www.gradio.app/guides/building-mcp-server-with-gradio) |
| **Building MCP Client** | Create MCP clients | [building-an-mcp-client-with-gradio](https://www.gradio.app/guides/building-an-mcp-client-with-gradio) |
| **File Upload MCP** | File handling with MCP | [file-upload-mcp](https://www.gradio.app/guides/file-upload-mcp) |
| **Using Docs MCP** | Documentation access via MCP | [using-docs-mcp](https://www.gradio.app/guides/using-docs-mcp) |

### MCP Server Example

```python
import gradio as gr
from gradio.mcp import MCPServer

def process_image(image):
    # Your AI processing here
    return result

# Create Gradio interface
demo = gr.Interface(
    fn=process_image,
    inputs=gr.Image(),
    outputs=gr.Image()
)

# Expose as MCP server
mcp_server = MCPServer(demo)
mcp_server.launch()
```

### MCP Client Example

```python
import gradio as gr
from gradio.mcp import MCPClient

# Connect to MCP server
client = MCPClient("http://localhost:7860")

# Call tools
result = client.call_tool("process_image", {"image": image_data})
```

### Use Cases

| Use Case | Description |
|----------|-------------|
| **Claude Code + Gradio** | Expose Gradio apps as tools for Claude |
| **ChatGPT + Gradio** | Connect Gradio to ChatGPT via MCP |
| **Agent Workflows** | Chain multiple Gradio apps |
| **File Processing** | Handle uploads in agent pipelines |

---

## Deployment & Integration

### Hugging Face Spaces Deployment

```python
# app.py - Deploy to HF Spaces
import gradio as gr

def greet(name):
    return f"Hello, {name}!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")
demo.launch()
```

```yaml
# README.md header for Spaces
---
title: My App
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
---
```

### Modal Deployment

```python
# Deploy to Modal (serverless)
import modal
import gradio as gr

app = modal.App("gradio-app")

@app.function(gpu="T4")
def inference(text):
    # Your model inference
    return result

@app.local_entrypoint()
def main():
    demo = gr.Interface(fn=inference, inputs="text", outputs="text")
    demo.launch()
```

### FastAPI Integration

```python
from fastapi import FastAPI
import gradio as gr

app = FastAPI()

# Your FastAPI routes
@app.get("/api/health")
def health():
    return {"status": "ok"}

# Gradio app
demo = gr.Interface(fn=lambda x: x, inputs="text", outputs="text")
app = gr.mount_gradio_app(app, demo, path="/gradio")
```

### Discord Bot

```python
import gradio as gr
import discord

# Create Gradio interface
demo = gr.Interface(fn=my_function, inputs="text", outputs="text")

# Create Discord bot that uses Gradio
client = gr.deploy_discord(demo, token="YOUR_BOT_TOKEN")
```

---

## Community

### Discussion Forum

[discuss.huggingface.co](https://discuss.huggingface.co/)

| Category | Topics |
|----------|--------|
| **Beginners** | Getting started, tutorials |
| **Transformers** | Model usage, fine-tuning |
| **Diffusers** | Image generation |
| **Datasets** | Data loading, processing |
| **Spaces** | Deployment, Gradio |
| **Research** | Papers, experiments |

### Notable Contributors

| User | Focus | Profile |
|------|-------|---------|
| **akhaliq** | Daily papers, demos | [huggingface.co/akhaliq](https://huggingface.co/akhaliq) |

### Getting Help

1. **Documentation**: [huggingface.co/docs](https://huggingface.co/docs)
2. **Forum**: [discuss.huggingface.co](https://discuss.huggingface.co/)
3. **Discord**: [Hugging Face Discord](https://discord.gg/huggingface)
4. **GitHub**: [github.com/huggingface](https://github.com/huggingface)

---

## Quick Start Templates

### Basic Gradio App

```python
import gradio as gr

def process(input_text):
    return f"Processed: {input_text}"

demo = gr.Interface(
    fn=process,
    inputs=gr.Textbox(label="Input"),
    outputs=gr.Textbox(label="Output"),
    title="My AI App"
)

demo.launch()
```

### Image Processing App

```python
import gradio as gr
from transformers import pipeline

# Load model from HF Hub
pipe = pipeline("image-classification")

def classify(image):
    return pipe(image)

demo = gr.Interface(
    fn=classify,
    inputs=gr.Image(type="pil"),
    outputs=gr.Label(num_top_classes=5),
    examples=["cat.jpg", "dog.jpg"]
)

demo.launch()
```

### Chat Interface

```python
import gradio as gr

def chat(message, history):
    # Your LLM logic here
    return f"You said: {message}"

demo = gr.ChatInterface(
    fn=chat,
    title="AI Chatbot",
    examples=["Hello!", "What can you do?"]
)

demo.launch()
```

### Multi-Modal App

```python
import gradio as gr

with gr.Blocks() as demo:
    gr.Markdown("# Multi-Modal AI App")

    with gr.Tab("Text"):
        text_input = gr.Textbox()
        text_output = gr.Textbox()
        text_btn = gr.Button("Process Text")

    with gr.Tab("Image"):
        image_input = gr.Image()
        image_output = gr.Image()
        image_btn = gr.Button("Process Image")

    with gr.Tab("Audio"):
        audio_input = gr.Audio()
        audio_output = gr.Audio()
        audio_btn = gr.Button("Process Audio")

demo.launch()
```

---

## Resource Summary

### Hugging Face Links

| Category | Links |
|----------|-------|
| **Community** | [akhaliq](https://huggingface.co/akhaliq), [Forum](https://discuss.huggingface.co/) |
| **Vision** | [Depth Anything 3](https://huggingface.co/spaces/depth-anything/depth-anything-3), [ViTPose](https://huggingface.co/spaces/hysts/ViTPose-transformers), [SAM3](https://huggingface.co/spaces/akhaliq/sam3), [VGGT](https://huggingface.co/spaces/facebook/vggt) |
| **Video** | [Wan 2.2 AMD](https://huggingface.co/spaces/amd/wan2.2onAMD), [Dream Wan](https://huggingface.co/spaces/dream2589632147/Dream-wan2-2-faster-Pro) |
| **LLMs** | [GPT OSS 120B](https://huggingface.co/spaces/amd/gpt-oss-120b-chatbot) |
| **Creative** | [3D Game Maker](https://huggingface.co/spaces/Mi6paulino/3D-Game-Maker), [SimpleVectorFlux](https://huggingface.co/renderartist/simplevectorflux) |
| **Finance** | [Trading Analyst](https://huggingface.co/spaces/dami1996/trading-analyst) |
| **Learning** | [Smol Course](https://huggingface.co/learn/smol-course/unit0/1), [Training Playbook](https://huggingface.co/spaces/HuggingFaceTB/smol-training-playbook) |
| **Robotics** | [LeRobot](https://github.com/huggingface/lerobot) |

### Gradio Links

| Category | Links |
|----------|-------|
| **Docs** | [Walkthrough](https://www.gradio.app/docs/gradio/walkthrough), [HTML](https://www.gradio.app/docs/gradio/html), [Dataset](https://www.gradio.app/docs/gradio/dataset) |
| **Components** | [Gallery](https://www.gradio.app/custom-components/gallery) |
| **MCP** | [Server](https://www.gradio.app/guides/building-mcp-server-with-gradio), [Client](https://www.gradio.app/guides/building-an-mcp-client-with-gradio), [File Upload](https://www.gradio.app/guides/file-upload-mcp), [Docs](https://www.gradio.app/guides/using-docs-mcp) |
| **AI Apps** | [LLM Agents](https://www.gradio.app/guides/gradio-and-llm-agents), [Speech](https://www.gradio.app/guides/real-time-speech-recognition), [3D Models](https://www.gradio.app/guides/how-to-use-3D-model-component) |
| **Integration** | [Discord](https://www.gradio.app/guides/creating-a-discord-bot-from-a-gradio-app), [FastAPI](https://www.gradio.app/guides/fastapi-app-with-the-gradio-client), [HF](https://www.gradio.app/guides/using-hugging-face-integrations) |
| **Dashboards** | [Supabase](https://www.gradio.app/guides/creating-a-dashboard-from-supabase-data), [Google Sheets](https://www.gradio.app/guides/creating-a-realtime-dashboard-from-google-sheets) |
| **Deploy** | [Share Links](https://www.gradio.app/guides/understanding-gradio-share-links), [Modal](https://www.gradio.app/guides/deploying-gradio-with-modal), [Background Tasks](https://www.gradio.app/guides/running-background-tasks) |

---

*Last updated: December 2025*
