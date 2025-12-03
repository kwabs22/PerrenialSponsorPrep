"""
Qdrant Hybrid Search
Showcases: Sparse Vectors + Hybrid Search
"""
import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, SparseVectorParams, SparseIndexParams
from qdrant_client.models import PointStruct, SparseVector, NamedVector, NamedSparseVector
from dotenv import load_dotenv

load_dotenv()

def main():
    print("=" * 50)
    print("Qdrant Hybrid Search Demo")
    print("=" * 50)

    client = QdrantClient(
        url=os.getenv("QDRANT_URL", "http://localhost:6333"),
        api_key=os.getenv("QDRANT_API_KEY")
    )

    collection_name = "hybrid_demo"

    # Create collection with both dense and sparse vectors
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config={
            "dense": VectorParams(size=384, distance=Distance.COSINE)
        },
        sparse_vectors_config={
            "sparse": SparseVectorParams(index=SparseIndexParams())
        }
    )

    # Sample documents with mock embeddings
    docs = [
        "Machine learning algorithms transform data into predictions",
        "Python programming language is popular for data science",
        "Climate change affects weather patterns globally",
    ]

    # Insert with hybrid vectors (simplified demo with mock embeddings)
    points = []
    for i, doc in enumerate(docs):
        # Mock dense embedding (in production, use a real model)
        dense_vector = [0.1] * 384
        # Mock sparse vector from word indices
        words = doc.lower().split()
        sparse_indices = [hash(w) % 10000 for w in words]
        sparse_values = [1.0] * len(words)

        points.append(PointStruct(
            id=i,
            vector={
                "dense": dense_vector,
                "sparse": SparseVector(indices=sparse_indices, values=sparse_values)
            },
            payload={"text": doc}
        ))

    client.upsert(collection_name=collection_name, points=points)
    print(f"Indexed {len(docs)} documents with hybrid vectors")

    # Hybrid search demo
    query = "machine learning"
    print(f"\n🔍 Hybrid search: '{query}'")

    # In production, generate real query embeddings
    query_dense = [0.1] * 384
    query_words = query.lower().split()
    query_sparse = SparseVector(
        indices=[hash(w) % 10000 for w in query_words],
        values=[1.0] * len(query_words)
    )

    results = client.query_points(
        collection_name=collection_name,
        prefetch=[
            {"query": query_dense, "using": "dense", "limit": 10},
            {"query": query_sparse, "using": "sparse", "limit": 10}
        ],
        query={"fusion": "rrf"},  # Reciprocal Rank Fusion
        limit=3
    )

    print("\nResults (RRF fusion):")
    for point in results.points:
        print(f"  - {point.payload['text'][:60]}...")

if __name__ == "__main__":
    main()
