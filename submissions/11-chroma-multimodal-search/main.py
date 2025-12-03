"""
Chroma Multimodal Search
Showcases: Multi-modal Embeddings
"""
import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction

def main():
    print("=" * 50)
    print("Chroma Multimodal Search")
    print("=" * 50)

    # Initialize Chroma with multimodal embeddings
    client = chromadb.Client()
    embedding_fn = OpenCLIPEmbeddingFunction()

    collection = client.get_or_create_collection(
        name="multimodal_demo",
        embedding_function=embedding_fn,
        data_loader=chromadb.utils.data_loaders.ImageLoader()
    )

    # Add text documents
    collection.add(
        documents=[
            "A beautiful sunset over the ocean",
            "A cat sleeping on a couch",
            "Mountains covered in snow",
            "A busy city street at night",
        ],
        ids=["sunset", "cat", "mountains", "city"]
    )
    print("Added 4 text documents")

    # Search with text query
    query = "peaceful nature scene"
    results = collection.query(query_texts=[query], n_results=2)

    print(f"\n🔍 Query: '{query}'")
    print("Results:")
    for doc, id in zip(results["documents"][0], results["ids"][0]):
        print(f"  - [{id}] {doc}")

    # Note: For image search, use collection.add(images=[...])
    print("\n💡 Tip: Add images with collection.add(images=['path/to/image.jpg'])")

if __name__ == "__main__":
    main()
