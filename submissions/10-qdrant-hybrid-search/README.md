# Qdrant Hybrid Search

**Showcases:** Sparse Vectors + Hybrid Search

## What it does
Combines keyword search (BM25) with semantic search for the best of both worlds. Find documents by exact terms AND meaning.

## Latest Feature (2024)
- **Sparse Vectors** - BM25-style keyword matching
- **Hybrid Search** - Combine sparse + dense vectors
- Fusion algorithms for optimal ranking

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env
python main.py
```
