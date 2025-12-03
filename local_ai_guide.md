# Local AI Use Cases Guide

> Everything you can do with AI locally, offline, without API costs.

---

## Quick Summary: What Can Run Locally?

| Capability | Best Local Tool | Hardware Needed | Quality vs API |
|------------|-----------------|-----------------|----------------|
| **Chat/Text Generation** | Ollama + Llama 3.2 | 8GB RAM min | 85-95% of GPT-4 |
| **Code Completion** | Ollama + CodeLlama/Codestral | 16GB RAM | 80-90% of Copilot |
| **Image Generation** | ComfyUI + FLUX | 12GB VRAM | Equal to Midjourney |
| **Speech-to-Text** | Whisper | 8GB RAM | Equal to API |
| **Text-to-Speech** | Piper/Coqui | 4GB RAM | 70-85% of ElevenLabs |
| **Embeddings/RAG** | Sentence Transformers | 8GB RAM | Equal to API |
| **OCR** | Surya/PaddleOCR | 8GB RAM | Better than Tesseract |
| **Vision/Multimodal** | LLaVA via Ollama | 16GB RAM | 70-80% of GPT-4V |

---

## 1. Local LLMs (Text Generation)

### Tools to Run LLMs

| Tool | Best For | Platform | GUI |
|------|----------|----------|-----|
| [**Ollama**](https://ollama.com) | Developers, CLI | Win/Mac/Linux | No |
| [**LM Studio**](https://lmstudio.ai) | Beginners | Win/Mac/Linux | Yes |
| [**Jan**](https://jan.ai) | Chat interface | Win/Mac/Linux | Yes |
| [**LocalAI**](https://localai.io) | API compatibility | Docker | No |
| [**vLLM**](https://github.com/vllm-project/vllm) | Production/Scale | Linux | No |

### Best Models (December 2025)

| Model | Size | RAM Needed | Best For |
|-------|------|------------|----------|
| **Llama 3.2 3B** | 2GB | 8GB | Quick tasks, mobile |
| **Llama 3.2 8B** | 5GB | 16GB | General purpose |
| **Llama 3.2 70B** | 40GB | 64GB | Best quality |
| **Mistral 7B** | 4GB | 12GB | Fast, accurate |
| **CodeLlama 34B** | 20GB | 32GB | Complex coding |
| **Dolphin 3.0 8B** | 5GB | 16GB | Uncensored, function calling |
| **DeepSeek-R1** | Varies | 16GB+ | Reasoning tasks |
| **Gemma 3** | 2-9GB | 8-16GB | Google's open model |
| **EXAONE Deep** | 2-20GB | 8-32GB | Math/coding |

### Getting Started with Ollama

```bash
# Install (one command)
curl -fsSL https://ollama.com/install.sh | sh  # Linux/Mac
# Windows: Download from ollama.com

# Run a model
ollama run llama3.2

# Run with specific size
ollama run llama3.2:70b

# List available models
ollama list

# Use as API (OpenAI compatible!)
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3.2", "messages": [{"role": "user", "content": "Hello!"}]}'
```

### Use Cases for Local LLMs

1. **Code completion** - Use CodeLlama or Codestral
2. **Document Q&A** - Combine with RAG (see section 6)
3. **Writing assistance** - Drafting, editing, summarizing
4. **Data analysis** - Process CSV/JSON locally
5. **Translation** - Many models support 90+ languages
6. **Function calling** - Dolphin 3.0 supports tool use
7. **Offline chatbot** - No internet required
8. **Private data processing** - Medical, legal, financial docs

---

## 2. Local Image Generation

### Tools

| Tool | Best For | Complexity |
|------|----------|------------|
| [**ComfyUI**](https://github.com/comfyanonymous/ComfyUI) | Power users, workflows | High |
| [**Stable Diffusion WebUI**](https://github.com/AUTOMATIC1111/stable-diffusion-webui) | General use | Medium |
| [**Fooocus**](https://github.com/lllyasviel/Fooocus) | Beginners | Low |
| [**InvokeAI**](https://github.com/invoke-ai/InvokeAI) | Artists | Medium |

### Models

| Model | VRAM | Quality | Speed |
|-------|------|---------|-------|
| **FLUX.1 Dev** | 12GB+ | Best | Slow |
| **FLUX.2** | 12GB+ | Best (4MP) | Medium |
| **SDXL** | 8GB | Great | Medium |
| **SD 3.5** | 8GB | Great | Fast |
| **SD 1.5** | 4GB | Good | Very Fast |

### Use Cases

1. **Art generation** - Illustrations, concept art
2. **Product mockups** - E-commerce images
3. **Logos and icons** - With ControlNet for precision
4. **Photo editing** - Inpainting, outpainting
5. **Style transfer** - Apply artistic styles
6. **LoRA training** - Custom subjects/styles with your photos
7. **Batch generation** - Generate 1000s of images overnight
8. **Video frames** - AnimateDiff for animation

### Hardware Reality Check

```
GPU VRAM → What you can run:
4GB  → SD 1.5 only
6GB  → SD 1.5, some SDXL (slow)
8GB  → SDXL comfortably
12GB → FLUX, all models
24GB → Everything, large batches
```

---

## 3. Local Speech-to-Text (Whisper)

### Desktop Apps

| App | Platform | Cost | Notes |
|-----|----------|------|-------|
| [**WhisperUI**](https://whisperui.com) | Win/Mac | Freemium | Best GUI |
| [**Whisper Notes**](https://whispernotes.app) | Mac/iOS | $4.99 | Apple optimized |
| [**WhisperO**](https://whispero.my) | Windows | Free | Simple |
| [**WizWhisp**](https://apps.microsoft.com/detail/9pgq3h6jxl4c) | Windows | Free | Microsoft Store |

### Developer Options

```bash
# Python library
pip install openai-whisper

# Basic transcription
whisper audio.mp3 --model medium

# With GPU acceleration
whisper audio.mp3 --model large-v3 --device cuda

# Faster alternative (10x speed)
pip install faster-whisper
```

### Model Sizes

| Model | Size | RAM | Accuracy | Speed |
|-------|------|-----|----------|-------|
| tiny | 75MB | 1GB | 70% | Very fast |
| base | 150MB | 1GB | 75% | Fast |
| small | 500MB | 2GB | 80% | Medium |
| medium | 1.5GB | 5GB | 85% | Slow |
| large-v3 | 3GB | 10GB | 95%+ | Very slow |
| large-v3-turbo | 1.5GB | 5GB | 93% | Fast |

### Use Cases

1. **Meeting transcription** - Record and transcribe locally
2. **Podcast processing** - Transcribe for show notes
3. **Video subtitles** - Generate SRT files
4. **Voice notes** - Quick speech-to-text
5. **Interview transcription** - Keep recordings private
6. **Real-time dictation** - With streaming models
7. **Multi-language** - 90+ languages supported

---

## 4. Local Text-to-Speech

### Tools

| Tool | Quality | Speed | Languages |
|------|---------|-------|-----------|
| [**Piper**](https://github.com/rhasspy/piper) | Good | Very Fast | 30+ |
| [**Coqui TTS**](https://github.com/idiap/coqui-ai-TTS) | Excellent | Medium | 17+ |
| [**Kokoro**](https://github.com/remsky/Kokoro-FastAPI) | Good | Fast | English |
| [**StyleTTS2**](https://github.com/yl4579/StyleTTS2) | Excellent | Slow | English |
| [**OpenTTS**](https://github.com/synesthesiam/opentts) | Varies | Fast | Multi-engine |

### Coqui TTS Example

```python
from TTS.api import TTS

# Initialize
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")

# Generate speech
tts.tts_to_file(text="Hello world!", file_path="output.wav")

# Voice cloning (XTTS)
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
tts.tts_to_file(
    text="Hello!",
    file_path="output.wav",
    speaker_wav="my_voice.wav",  # 6+ seconds of your voice
    language="en"
)
```

### Use Cases

1. **Audiobook generation** - Convert books to audio
2. **Voice assistants** - Offline smart home
3. **Accessibility** - Screen readers
4. **Video narration** - Generate voiceovers
5. **Voice cloning** - Clone voices with 6s of audio
6. **Game dialogue** - Generate NPC voices
7. **Language learning** - Pronunciation examples

---

## 5. Local OCR (Document Processing)

### Tools (Better than Tesseract)

| Tool | Best For | Languages | Accuracy |
|------|----------|-----------|----------|
| [**Surya**](https://github.com/VikParuchuri/surya) | Modern docs | 90+ | Excellent |
| [**PaddleOCR**](https://github.com/PaddlePaddle/PaddleOCR) | Multi-language | 80+ | Excellent |
| [**EasyOCR**](https://github.com/JaidedAI/EasyOCR) | Simple integration | 80+ | Good |
| [**DocTR**](https://github.com/mindee/doctr) | PDFs | Multi | Excellent |
| [**Marker**](https://github.com/VikParuchuri/marker) | PDF→Markdown | Multi | Excellent |

### Surya Example

```python
from surya.ocr import run_ocr
from surya.model.detection import segformer
from surya.model.recognition.model import load_model

# Load models
det_model = segformer.load_model()
rec_model = load_model()

# Run OCR
results = run_ocr(
    images=["document.png"],
    det_model=det_model,
    rec_model=rec_model,
    languages=["en"]
)

for page in results:
    for line in page.text_lines:
        print(line.text)
```

### Use Cases

1. **Document digitization** - Scan and extract text
2. **Receipt processing** - Extract purchase data
3. **PDF extraction** - Convert PDFs to text/markdown
4. **Historical documents** - Kraken for old texts
5. **Handwriting recognition** - With specialized models
6. **Form processing** - Extract structured data
7. **Book scanning** - Digitize personal library

---

## 6. Local Embeddings & RAG

### Embedding Models

| Model | Size | Quality | Speed |
|-------|------|---------|-------|
| **all-MiniLM-L6-v2** | 80MB | Good | Very Fast |
| **all-mpnet-base-v2** | 420MB | Better | Fast |
| **bge-large-en** | 1.3GB | Excellent | Medium |
| **EmbeddingGemma** | 308MB | Excellent | Fast |
| **nomic-embed-text** | 550MB | Excellent | Fast |

### Vector Databases (Local)

| Database | Best For | Notes |
|----------|----------|-------|
| [**Chroma**](https://www.trychroma.com/) | Prototyping | Python-native, simple |
| [**LanceDB**](https://lancedb.com/) | Production | Embedded, fast |
| [**Qdrant**](https://qdrant.tech/) | Scale | Docker, feature-rich |
| [**FAISS**](https://github.com/facebookresearch/faiss) | Performance | Meta's library |

### Complete Local RAG Example

```python
from sentence_transformers import SentenceTransformer
import chromadb

# 1. Load embedding model (downloads once, then offline)
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Create local vector database
client = chromadb.Client()
collection = client.create_collection("my_docs")

# 3. Add documents
docs = ["Paris is the capital of France", "Tokyo is in Japan"]
embeddings = embedder.encode(docs).tolist()
collection.add(
    documents=docs,
    embeddings=embeddings,
    ids=["doc1", "doc2"]
)

# 4. Query
query_embedding = embedder.encode(["What is the capital of France?"]).tolist()
results = collection.query(query_embeddings=query_embedding, n_results=1)
print(results['documents'])  # [['Paris is the capital of France']]

# 5. Feed to local LLM via Ollama
import requests
context = results['documents'][0][0]
response = requests.post('http://localhost:11434/api/generate', json={
    "model": "llama3.2",
    "prompt": f"Context: {context}\n\nQuestion: What is the capital of France?"
})
```

### Use Cases

1. **Document Q&A** - Chat with your PDFs
2. **Code search** - Semantic search over codebase
3. **Knowledge base** - Personal wiki with AI
4. **Research assistant** - Query academic papers
5. **Customer support** - Offline FAQ bot
6. **Legal document search** - Confidential data stays local
7. **Medical records** - HIPAA-compliant processing

---

## 7. Local Vision/Multimodal

### Models via Ollama

```bash
# LLaVA - Vision + Language
ollama run llava

# Ask about an image
ollama run llava "What's in this image?" --image photo.jpg

# Bakllava - Better vision
ollama run bakllava
```

### Use Cases

1. **Image captioning** - Describe photos
2. **Visual Q&A** - Ask questions about images
3. **Document understanding** - Analyze charts/graphs
4. **Accessibility** - Describe images for blind users
5. **Content moderation** - Classify image content
6. **Screenshot analysis** - Extract info from UI

---

## 8. Hardware Recommendations

### Minimum Viable Setup

| Component | Spec | Cost |
|-----------|------|------|
| CPU | Any modern (2020+) | - |
| RAM | 16GB | ~$50 |
| GPU | None (CPU inference) | $0 |
| Storage | 50GB free | - |

**Can run:** Llama 3.2 3B, Whisper small, SD 1.5 (slow)

### Recommended Setup

| Component | Spec | Cost |
|-----------|------|------|
| CPU | Ryzen 7 / i7 | ~$300 |
| RAM | 32GB | ~$100 |
| GPU | RTX 3060 12GB | ~$250 |
| Storage | 500GB SSD | ~$50 |

**Can run:** Llama 3.2 8B, Whisper large, SDXL, FLUX

### Power User Setup

| Component | Spec | Cost |
|-----------|------|------|
| CPU | Ryzen 9 / i9 | ~$500 |
| RAM | 64GB+ | ~$200 |
| GPU | RTX 4090 24GB | ~$1600 |
| Storage | 2TB NVMe | ~$150 |

**Can run:** Llama 70B, everything at full speed

### Apple Silicon

| Chip | Unified Memory | Can Run |
|------|----------------|---------|
| M1 | 8-16GB | Small models |
| M2 | 8-24GB | Medium models |
| M3 | 8-128GB | Large models (Pro/Max) |
| M4 | 16-128GB | Everything (Pro/Max) |

Apple Silicon is excellent for local AI due to unified memory architecture.

---

## 9. Comparison: Local vs API

| Factor | Local | API |
|--------|-------|-----|
| **Cost** | One-time hardware | Per-token/request |
| **Privacy** | Complete | Data sent to servers |
| **Speed** | Depends on hardware | Usually faster |
| **Quality** | 70-95% of best APIs | Best available |
| **Offline** | Yes | No |
| **Customization** | Full (fine-tuning) | Limited |
| **Rate limits** | None | Yes |
| **Setup** | More complex | Simple |

### When to Use Local

- Processing sensitive/private data
- High volume (would cost $$$$ via API)
- Offline requirements
- Custom fine-tuning needed
- Learning/experimentation
- Predictable costs

### When to Use API

- Need absolute best quality
- Low volume/occasional use
- Limited hardware
- Rapid prototyping
- Production with SLA needs

---

## 10. Quick Start Recipes

### Recipe 1: Offline Chatbot

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Run chat
ollama run llama3.2
```

### Recipe 2: Document Q&A

```bash
pip install sentence-transformers chromadb ollama
```
Then use the RAG example from Section 6.

### Recipe 3: Voice Transcription

```bash
pip install faster-whisper
faster-whisper audio.mp3 --model large-v3
```

### Recipe 4: Image Generation

1. Install [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
2. Download SDXL or FLUX model
3. Generate images via node workflow

### Recipe 5: Complete Offline Assistant

Combine:
- Whisper (speech→text)
- Ollama (process text)
- Piper (text→speech)
- Chroma (memory/RAG)

---

## Resources

### Documentation
- [Ollama Library](https://ollama.com/library)
- [HuggingFace Models](https://huggingface.co/models)
- [ComfyUI Docs](https://comfyui.org)

### Guides
- [Local LLM Hosting Comparison](https://www.glukhov.org/post/2025/11/hosting-llms-ollama-localai-jan-lmstudio-vllm-comparison/)
- [Best Ollama Models 2025](https://collabnix.com/best-ollama-models-in-2025-complete-performance-comparison/)
- [Open Source OCR Comparison](https://modal.com/blog/8-top-open-source-ocr-models-compared)
- [Open Source TTS Tools](https://www.lemonfox.ai/blog/open-source-text-to-speech)

### Communities
- r/LocalLLaMA (Reddit)
- r/StableDiffusion (Reddit)
- Ollama Discord
- ComfyUI Discord

---

*Created: December 2025*
*Focus: Practical local AI without API costs*
