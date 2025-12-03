# Pinecone Semantic Search

**Showcases:** Serverless Indexes + Inference API

## What it does
A semantic search engine that finds relevant documents based on meaning, not just keywords. Uses Pinecone's serverless infrastructure for instant scaling and the new Inference API for automatic embeddings.

## Latest Feature (2024)
- **Serverless Indexes** - Auto-scaling with pay-per-use pricing
- **Inference API** - Generate embeddings directly in Pinecone
- No need for separate embedding model hosting
- Supports multiple embedding models
- Built-in metadata filtering

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and add your Pinecone API key:
   ```bash
   cp .env.example .env
   ```

3. Run the demo:
   ```bash
   python main.py
   ```

## How to Use
- Add documents to the search index
- Search using natural language queries
- Results are ranked by semantic similarity
- Filter by metadata for precise results

## API Reference
- [Pinecone Docs](https://docs.pinecone.io/)
- [Inference API](https://docs.pinecone.io/guides/inference/understanding-inference)
- [Release Notes](https://docs.pinecone.io/release-notes/2024)
