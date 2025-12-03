"""
Pinecone Semantic Search
Showcases: Serverless Indexes + Inference API
1-hour hackathon submission

This demo uses Pinecone's Inference API for automatic embeddings.
"""
import os
import sys
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

INDEX_NAME = "hackathon-search"
EMBED_MODEL = "multilingual-e5-large"  # Pinecone hosted embedding model


def setup_pinecone():
    """Initialize Pinecone client"""
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise ValueError("PINECONE_API_KEY not found in environment")

    return Pinecone(api_key=api_key)


def create_index_if_needed(pc: Pinecone):
    """Create serverless index if it doesn't exist"""
    existing = pc.list_indexes().names()

    if INDEX_NAME not in existing:
        print(f"Creating serverless index: {INDEX_NAME}")
        pc.create_index(
            name=INDEX_NAME,
            dimension=1024,  # e5-large dimension
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        print("Index created!")
    else:
        print(f"Using existing index: {INDEX_NAME}")

    return pc.Index(INDEX_NAME)


def embed_text(pc: Pinecone, texts: list[str]) -> list[list[float]]:
    """Generate embeddings using Pinecone Inference API"""
    embeddings = pc.inference.embed(
        model=EMBED_MODEL,
        inputs=texts,
        parameters={"input_type": "passage"}
    )
    return [e["values"] for e in embeddings]


def embed_query(pc: Pinecone, query: str) -> list[float]:
    """Generate query embedding"""
    embeddings = pc.inference.embed(
        model=EMBED_MODEL,
        inputs=[query],
        parameters={"input_type": "query"}
    )
    return embeddings[0]["values"]


def add_documents(pc: Pinecone, index, documents: list[dict]):
    """Add documents to the index"""
    # Extract texts and metadata
    texts = [doc["text"] for doc in documents]
    ids = [doc.get("id", str(i)) for i, doc in enumerate(documents)]

    # Generate embeddings using Inference API
    print("Generating embeddings...")
    embeddings = embed_text(pc, texts)

    # Prepare vectors with metadata
    vectors = []
    for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
        metadata = {k: v for k, v in doc.items() if k not in ["id", "text"]}
        metadata["text"] = doc["text"][:1000]  # Store truncated text
        vectors.append({
            "id": ids[i],
            "values": embedding,
            "metadata": metadata
        })

    # Upsert to index
    index.upsert(vectors=vectors)
    print(f"Added {len(documents)} documents to index")


def search(pc: Pinecone, index, query: str, top_k: int = 5, filter: dict = None):
    """Search for similar documents"""
    query_embedding = embed_query(pc, query)

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        filter=filter
    )

    return results.matches


def main():
    print("=" * 50)
    print("Pinecone Semantic Search")
    print("Showcasing: Serverless + Inference API")
    print("=" * 50)

    try:
        pc = setup_pinecone()
        index = create_index_if_needed(pc)
    except ValueError as e:
        print(f"\nError: {e}")
        print("Get your API key from https://app.pinecone.io/")
        sys.exit(1)

    # Sample documents
    documents = [
        {"id": "1", "text": "Machine learning is transforming how we analyze data and make predictions.", "category": "tech"},
        {"id": "2", "text": "Python is the most popular programming language for data science.", "category": "tech"},
        {"id": "3", "text": "Climate change is causing more extreme weather events worldwide.", "category": "environment"},
        {"id": "4", "text": "Renewable energy sources like solar and wind are growing rapidly.", "category": "environment"},
        {"id": "5", "text": "The stock market showed strong gains in technology sectors this quarter.", "category": "finance"},
        {"id": "6", "text": "Cryptocurrency adoption continues to grow among institutional investors.", "category": "finance"},
        {"id": "7", "text": "Remote work has become the new normal for many tech companies.", "category": "work"},
        {"id": "8", "text": "Artificial intelligence is being used to improve healthcare diagnostics.", "category": "health"},
    ]

    print("\nAdding sample documents...")
    add_documents(pc, index, documents)

    print("\n" + "-" * 50)
    print("Demo: Semantic Search")
    print("-" * 50)

    # Demo searches
    demo_queries = [
        ("What are the trends in AI?", None),
        ("Tell me about global warming", None),
        ("Investment opportunities", {"category": "finance"}),
    ]

    for query, filter in demo_queries:
        print(f"\n🔍 Query: {query}")
        if filter:
            print(f"   Filter: {filter}")

        results = search(pc, index, query, top_k=3, filter=filter)

        print("Results:")
        for i, match in enumerate(results, 1):
            print(f"  {i}. (score: {match.score:.3f}) {match.metadata.get('text', '')[:80]}...")

    # Interactive mode
    print("\n" + "-" * 50)
    print("Interactive Search (type 'quit' to exit)")
    print("-" * 50)

    while True:
        query = input("\nSearch: ").strip()
        if not query or query.lower() == "quit":
            break

        results = search(pc, index, query, top_k=3)

        print("\nResults:")
        for i, match in enumerate(results, 1):
            print(f"  {i}. [{match.metadata.get('category', 'unknown')}] "
                  f"(score: {match.score:.3f})")
            print(f"     {match.metadata.get('text', '')[:100]}...")

    print("\nGoodbye!")


if __name__ == "__main__":
    main()
