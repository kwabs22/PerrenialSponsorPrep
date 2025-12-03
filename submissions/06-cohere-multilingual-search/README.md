# Cohere Multilingual Document Search

**Showcases:** Command R+ with Multilingual RAG

## What it does
A multilingual document search system that can find and answer questions about documents in any language. Uses Cohere's multilingual embeddings and Command R+ for accurate retrieval across 100+ languages.

## Latest Feature (2024)
- **Command R+** - Advanced RAG-optimized model
- **Embed v3** - Multilingual embeddings supporting 100+ languages
- **Rerank** - Improve search relevance with neural reranking
- Built-in citation support for verifiable answers
- Optimized for enterprise RAG workloads

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and add your Cohere API key:
   ```bash
   cp .env.example .env
   ```

3. Run the search demo:
   ```bash
   python main.py
   ```

## How to Use
- Add documents in any language to the system
- Search using queries in any language
- The system finds relevant documents regardless of language
- Get answers with citations pointing to source documents

## API Reference
- [Cohere API Docs](https://docs.cohere.com/)
- [Embed v3 Docs](https://docs.cohere.com/docs/multilingual-language-models)
- [Changelog](https://docs.cohere.com/changelog)
