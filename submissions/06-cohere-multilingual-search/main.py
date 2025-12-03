"""
Cohere Multilingual Document Search
Showcases: Command R+ with Multilingual RAG
1-hour hackathon submission

This demo uses Cohere's multilingual embeddings for cross-language search.
"""
import os
import sys
import cohere
import numpy as np
from dotenv import load_dotenv

load_dotenv()


class MultilingualSearch:
    def __init__(self):
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY not found in environment")

        self.client = cohere.ClientV2(api_key)
        self.documents = []
        self.embeddings = []

    def add_documents(self, documents: list[dict]):
        """
        Add documents to the search index

        Each document should have:
        - text: The content
        - language: The language code (optional)
        - title: A title (optional)
        """
        self.documents.extend(documents)

        # Generate embeddings for all documents
        texts = [doc["text"] for doc in documents]

        response = self.client.embed(
            texts=texts,
            model="embed-multilingual-v3.0",
            input_type="search_document",
            embedding_types=["float"]
        )

        new_embeddings = response.embeddings.float_
        self.embeddings.extend(new_embeddings)

        print(f"Added {len(documents)} documents to index")

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        """Search for relevant documents using the query"""
        # Embed the query
        response = self.client.embed(
            texts=[query],
            model="embed-multilingual-v3.0",
            input_type="search_query",
            embedding_types=["float"]
        )

        query_embedding = np.array(response.embeddings.float_[0])

        # Calculate cosine similarity
        similarities = []
        for i, doc_embedding in enumerate(self.embeddings):
            doc_emb = np.array(doc_embedding)
            similarity = np.dot(query_embedding, doc_emb) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc_emb)
            )
            similarities.append((i, similarity))

        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Return top results
        results = []
        for idx, score in similarities[:top_k]:
            results.append({
                **self.documents[idx],
                "score": float(score)
            })

        return results

    def rerank(self, query: str, documents: list[dict], top_k: int = 3) -> list[dict]:
        """Rerank documents for better relevance"""
        doc_texts = [doc["text"] for doc in documents]

        response = self.client.rerank(
            query=query,
            documents=doc_texts,
            model="rerank-multilingual-v3.0",
            top_n=top_k
        )

        reranked = []
        for result in response.results:
            doc = documents[result.index].copy()
            doc["relevance_score"] = result.relevance_score
            reranked.append(doc)

        return reranked

    def answer(self, query: str, documents: list[dict] = None) -> str:
        """Generate an answer using Command R+ with RAG"""
        if documents is None:
            # Search for relevant documents
            documents = self.search(query, top_k=5)

        # Format documents for RAG
        formatted_docs = [
            {"data": {"text": doc["text"], "title": doc.get("title", f"Document {i+1}")}}
            for i, doc in enumerate(documents)
        ]

        response = self.client.chat(
            model="command-r-plus",
            messages=[{"role": "user", "content": query}],
            documents=formatted_docs
        )

        answer = response.message.content[0].text

        # Add citations if available
        if response.message.citations:
            answer += "\n\nSources:"
            for citation in response.message.citations:
                answer += f"\n- {citation.sources[0].document['title'] if citation.sources else 'Unknown'}"

        return answer


def main():
    print("=" * 50)
    print("Cohere Multilingual Document Search")
    print("Showcasing: Command R+ with Multilingual RAG")
    print("=" * 50)

    try:
        search = MultilingualSearch()
    except ValueError as e:
        print(f"\nError: {e}")
        print("Get your API key from https://dashboard.cohere.com/")
        sys.exit(1)

    # Add sample multilingual documents
    sample_docs = [
        {
            "text": "Artificial intelligence is transforming how we work and live. Machine learning models can now understand and generate human language with remarkable accuracy.",
            "title": "AI Overview (English)",
            "language": "en"
        },
        {
            "text": "La inteligencia artificial está transformando nuestra forma de trabajar y vivir. Los modelos de aprendizaje automático ahora pueden entender y generar lenguaje humano con una precisión notable.",
            "title": "Visión General de IA (Spanish)",
            "language": "es"
        },
        {
            "text": "人工知能は私たちの働き方や生活を変革しています。機械学習モデルは今や、驚くべき精度で人間の言語を理解し生成することができます。",
            "title": "AI概要 (Japanese)",
            "language": "ja"
        },
        {
            "text": "L'intelligence artificielle transforme notre façon de travailler et de vivre. Les modèles d'apprentissage automatique peuvent désormais comprendre et générer le langage humain avec une précision remarquable.",
            "title": "Aperçu de l'IA (French)",
            "language": "fr"
        },
        {
            "text": "Climate change is one of the most pressing challenges of our time. Rising temperatures are causing more extreme weather events worldwide.",
            "title": "Climate Change (English)",
            "language": "en"
        },
        {
            "text": "气候变化是我们这个时代最紧迫的挑战之一。气温上升正在导致全球更多极端天气事件。",
            "title": "气候变化 (Chinese)",
            "language": "zh"
        }
    ]

    print("\nLoading multilingual documents...")
    search.add_documents(sample_docs)
    print(f"Languages: English, Spanish, Japanese, French, Chinese")

    print("\n" + "-" * 50)
    print("Demo: Cross-language search")
    print("-" * 50)

    # Demo queries in different languages
    demo_queries = [
        ("What is AI?", "English query about AI"),
        ("¿Cómo funciona la inteligencia artificial?", "Spanish query about AI"),
        ("気候変動について", "Japanese query about climate"),
        ("Tell me about global warming", "English query about climate"),
    ]

    for query, description in demo_queries:
        print(f"\n🔍 Query ({description}): {query}")

        results = search.search(query, top_k=2)

        print("Results:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. [{result.get('language', '?')}] {result['title']} (score: {result['score']:.3f})")

    # Generate an answer
    print("\n" + "-" * 50)
    print("Demo: RAG Answer Generation")
    print("-" * 50)

    rag_query = "What are the main topics discussed in these documents?"
    print(f"\n❓ Question: {rag_query}")
    print("\n💬 Answer (Command R+):")

    answer = search.answer(rag_query)
    print(answer)

    # Interactive mode
    print("\n" + "-" * 50)
    print("Interactive Mode (type 'quit' to exit)")
    print("-" * 50)

    while True:
        try:
            query = input("\nYour query: ").strip()
            if not query:
                continue
            if query.lower() == "quit":
                break

            print("\n🔍 Searching...")
            results = search.search(query, top_k=3)

            print("\nTop Results:")
            for i, result in enumerate(results, 1):
                print(f"  {i}. {result['title']} (score: {result['score']:.3f})")
                print(f"     {result['text'][:100]}...")

            print("\n💬 Generating answer...")
            answer = search.answer(query, results)
            print(f"\nAnswer: {answer}")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break


if __name__ == "__main__":
    main()
