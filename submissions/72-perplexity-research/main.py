"""Perplexity Sonar API Demo"""
import os, requests
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("PERPLEXITY_API_KEY")

def search_query(query: str):
    if not API_KEY:
        print(f"[Demo] Would search: {query}")
        return {"answer": "Demo response with citations", "citations": ["https://example.com"]}

    response = requests.post(
        "https://api.perplexity.ai/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [{"role": "user", "content": query}]
        }
    )
    return response.json()

def main():
    print("=" * 50)
    print("Perplexity Research Demo")
    print("=" * 50)
    query = input("\nEnter research query: ") or "What are the latest AI developments?"
    result = search_query(query)
    print(f"\nResult: {result}")

if __name__ == "__main__":
    main()
