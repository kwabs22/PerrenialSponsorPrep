"""
Haystack Document Pipeline
Showcases: Pipeline as Code + Haystack 2.0
"""
import os
from dotenv import load_dotenv

load_dotenv()

from haystack import Pipeline, Document
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.writers import DocumentWriter
from haystack.components.embedders import (
    SentenceTransformersTextEmbedder,
    SentenceTransformersDocumentEmbedder,
)
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders import PromptBuilder

def main():
    print("=" * 50)
    print("Haystack Document Pipeline")
    print("=" * 50)

    # Initialize document store
    document_store = InMemoryDocumentStore()

    # Sample documents
    documents = [
        Document(content="Python is a programming language known for its simplicity and readability."),
        Document(content="Machine learning is a subset of AI that enables systems to learn from data."),
        Document(content="Haystack is an open-source framework for building NLP applications."),
        Document(content="RAG combines retrieval with generation for more accurate AI responses."),
        Document(content="Vector databases store embeddings for efficient similarity search."),
    ]

    print("\n📄 Building indexing pipeline...")

    # === INDEXING PIPELINE ===
    indexing_pipeline = Pipeline()
    indexing_pipeline.add_component(
        "embedder",
        SentenceTransformersDocumentEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
    )
    indexing_pipeline.add_component(
        "writer",
        DocumentWriter(document_store=document_store)
    )
    indexing_pipeline.connect("embedder", "writer")

    # Run indexing
    indexing_pipeline.run({"embedder": {"documents": documents}})
    print(f"✅ Indexed {len(documents)} documents")

    # === RAG PIPELINE ===
    print("\n🔧 Building RAG pipeline...")

    prompt_template = """
    Answer the question based on the provided context.

    Context:
    {% for doc in documents %}
    - {{ doc.content }}
    {% endfor %}

    Question: {{ question }}

    Answer:
    """

    rag_pipeline = Pipeline()
    rag_pipeline.add_component(
        "text_embedder",
        SentenceTransformersTextEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
    )
    rag_pipeline.add_component(
        "retriever",
        InMemoryEmbeddingRetriever(document_store=document_store, top_k=3)
    )
    rag_pipeline.add_component(
        "prompt_builder",
        PromptBuilder(template=prompt_template)
    )
    rag_pipeline.add_component(
        "generator",
        OpenAIGenerator(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
    )

    # Connect components
    rag_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
    rag_pipeline.connect("retriever.documents", "prompt_builder.documents")
    rag_pipeline.connect("prompt_builder", "generator")

    print("✅ RAG pipeline ready!")

    # Test queries
    queries = [
        "What is Haystack?",
        "How does RAG work?",
        "What are vector databases used for?",
    ]

    print("\n🔍 Running queries...")
    print("-" * 50)

    for query in queries:
        print(f"\n❓ {query}")

        result = rag_pipeline.run({
            "text_embedder": {"text": query},
            "prompt_builder": {"question": query},
        })

        answer = result["generator"]["replies"][0]
        print(f"💡 {answer}")

    # Show pipeline structure
    print("\n" + "=" * 50)
    print("📊 Pipeline Structure:")
    print("  Indexing: embedder → writer → document_store")
    print("  RAG: text_embedder → retriever → prompt_builder → generator")

if __name__ == "__main__":
    main()
