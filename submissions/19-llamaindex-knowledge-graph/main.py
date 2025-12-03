"""
LlamaIndex Knowledge Graph Builder
Showcases: Workflows + Property Graph Index
"""
import os
from dotenv import load_dotenv

load_dotenv()

# LlamaIndex imports
from llama_index.core import (
    Document,
    PropertyGraphIndex,
    Settings,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

def main():
    print("=" * 50)
    print("LlamaIndex Knowledge Graph Builder")
    print("=" * 50)

    # Configure LlamaIndex
    Settings.llm = OpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
    Settings.embed_model = OpenAIEmbedding(api_key=os.getenv("OPENAI_API_KEY"))

    # Sample documents about a tech company
    documents = [
        Document(text="""
            Acme Corp was founded in 2020 by Jane Smith and John Doe.
            The company is headquartered in San Francisco, California.
            Jane Smith serves as CEO while John Doe is the CTO.
        """),
        Document(text="""
            Acme Corp's main product is CloudSync, a cloud storage solution.
            CloudSync was launched in 2021 and has over 1 million users.
            The product competes with Dropbox and Google Drive.
        """),
        Document(text="""
            In 2023, Acme Corp acquired DataFlow Inc for $50 million.
            DataFlow specializes in data pipeline automation.
            This acquisition expanded Acme's enterprise offerings.
        """),
    ]

    print("\n📄 Processing documents...")

    # Build Property Graph Index
    # This extracts entities and relationships automatically
    index = PropertyGraphIndex.from_documents(
        documents,
        show_progress=True,
    )

    print("\n✅ Knowledge graph built!")
    print("\n🔍 Sample queries:")

    # Query the knowledge graph
    queries = [
        "Who founded Acme Corp?",
        "What products does Acme Corp have?",
        "What companies did Acme Corp acquire?",
    ]

    query_engine = index.as_query_engine(
        include_text=True,
        similarity_top_k=2,
    )

    for query in queries:
        print(f"\n❓ {query}")
        response = query_engine.query(query)
        print(f"💡 {response}")

    # Show graph structure
    print("\n📊 Graph Statistics:")
    print(f"  - Entities extracted: {len(index.property_graph_store.get_triplets())}")

    print("\n🔗 Sample Triplets (Entity-Relation-Entity):")
    triplets = index.property_graph_store.get_triplets()[:5]
    for subj, rel, obj in triplets:
        print(f"  [{subj}] --{rel}--> [{obj}]")

if __name__ == "__main__":
    main()
