"""
Meta Llama Local Document Q&A
Showcases: Llama 3.2 with local inference via Ollama
1-hour hackathon submission

This demo runs Llama 3.2 locally for document Q&A without API calls.
"""
import os
import sys
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv()

# Ollama API endpoint (runs locally)
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL_NAME = os.getenv("LLAMA_MODEL", "llama3.2")


def check_ollama():
    """Check if Ollama is running"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False


def check_model_available():
    """Check if the Llama model is available"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return any(MODEL_NAME in m.get("name", "") for m in models)
    except:
        pass
    return False


def load_document(file_path: str) -> str:
    """Load a text document"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Document not found: {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def query_llama(prompt: str, context: str = "") -> str:
    """Query Llama 3.2 via Ollama"""

    system_prompt = """You are a helpful document assistant. Answer questions based on the provided document context.
If the answer isn't in the document, say so. Be concise and accurate."""

    if context:
        full_prompt = f"""Document Context:
{context}

Question: {prompt}

Answer based on the document above:"""
    else:
        full_prompt = prompt

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": MODEL_NAME,
            "prompt": full_prompt,
            "system": system_prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 500
            }
        },
        timeout=120
    )

    if response.status_code == 200:
        return response.json().get("response", "No response generated")
    else:
        raise Exception(f"Ollama error: {response.text}")


def interactive_qa(document_content: str):
    """Run interactive Q&A session"""
    print("\nDocument loaded! Ask questions about it.")
    print("Type 'quit' to exit, 'summary' for a document summary")
    print("-" * 50)

    while True:
        try:
            question = input("\nYour question: ").strip()

            if not question:
                continue

            if question.lower() == "quit":
                print("Goodbye!")
                break

            if question.lower() == "summary":
                question = "Please provide a brief summary of this document."

            print("\nLlama 3.2 is thinking...")
            answer = query_llama(question, document_content[:4000])  # Limit context size
            print(f"\nAnswer: {answer}")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")


def main():
    print("=" * 50)
    print("Meta Llama Local Document Q&A")
    print("Showcasing: Llama 3.2 with local inference")
    print("=" * 50)

    # Check Ollama is running
    if not check_ollama():
        print("\nError: Ollama is not running!")
        print("Please install and start Ollama:")
        print("  1. Download from https://ollama.ai")
        print("  2. Run: ollama serve")
        print(f"  3. Pull model: ollama pull {MODEL_NAME}")
        sys.exit(1)

    print(f"\nOllama is running at {OLLAMA_URL}")

    # Check model is available
    if not check_model_available():
        print(f"\nModel '{MODEL_NAME}' not found!")
        print(f"Please pull it: ollama pull {MODEL_NAME}")
        sys.exit(1)

    print(f"Model '{MODEL_NAME}' is ready!")

    # Load document if provided
    if len(sys.argv) > 1:
        doc_path = sys.argv[1]
        try:
            document = load_document(doc_path)
            print(f"\nLoaded document: {doc_path}")
            print(f"Document length: {len(document)} characters")
            interactive_qa(document)
        except FileNotFoundError as e:
            print(f"\nError: {e}")
            sys.exit(1)
    else:
        # Demo mode without document
        print("\nNo document provided - running in chat mode")
        print("Usage: python main.py <document.txt>")
        print("\nYou can still chat with Llama 3.2 directly.")
        print("Type 'quit' to exit")
        print("-" * 50)

        while True:
            try:
                prompt = input("\nYou: ").strip()
                if not prompt:
                    continue
                if prompt.lower() == "quit":
                    break

                print("\nLlama 3.2 is thinking...")
                response = query_llama(prompt)
                print(f"\nLlama: {response}")

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")


if __name__ == "__main__":
    main()
