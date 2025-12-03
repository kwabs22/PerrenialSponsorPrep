"""
Google Cloud Vertex AI Chatbot
Showcases: Vertex AI + Gemini 2.0
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Check for Google Cloud SDK
try:
    import vertexai
    from vertexai.generative_models import GenerativeModel, Part
    HAS_VERTEXAI = True
except ImportError:
    HAS_VERTEXAI = False

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

def initialize_vertex():
    """Initialize Vertex AI."""
    vertexai.init(project=PROJECT_ID, location=LOCATION)

def create_chatbot():
    """Create Gemini chatbot with grounding."""
    model = GenerativeModel(
        "gemini-2.0-flash-exp",
        system_instruction="""You are a helpful enterprise assistant.
        Provide accurate, professional responses.
        When uncertain, acknowledge limitations."""
    )
    return model.start_chat()

def chat_with_grounding(chat, message: str, use_grounding: bool = True):
    """Send message with optional Google Search grounding."""
    if use_grounding:
        # Enable grounding with Google Search
        response = chat.send_message(
            message,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 1024,
            },
            # Grounding configuration
            tools=[{
                "google_search_retrieval": {
                    "dynamic_retrieval_config": {
                        "mode": "MODE_DYNAMIC",
                        "dynamic_threshold": 0.3
                    }
                }
            }]
        )
    else:
        response = chat.send_message(message)

    return response.text

def analyze_document(file_path: str, question: str):
    """Analyze document with Gemini."""
    model = GenerativeModel("gemini-2.0-flash-exp")

    # For demo, use text content
    with open(file_path, 'r') as f:
        content = f.read()

    prompt = f"""Analyze this document and answer the question.

Document:
{content[:5000]}

Question: {question}"""

    response = model.generate_content(prompt)
    return response.text

def main():
    print("=" * 50)
    print("Google Cloud Vertex AI Chatbot")
    print("=" * 50)

    if not HAS_VERTEXAI:
        print("\nInstall: pip install google-cloud-aiplatform")
        return

    if not PROJECT_ID:
        print("\nSetup required:")
        print("1. Create Google Cloud project")
        print("2. Enable Vertex AI API")
        print("3. Set up authentication (gcloud auth)")
        print("4. Copy project ID to .env file")

        print("\n🤖 Vertex AI + Gemini 2.0 Features:")
        print("  - Multimodal understanding")
        print("  - Google Search grounding")
        print("  - Long context (1M+ tokens)")
        print("  - Enterprise security")

        print("\n💬 Demo Conversation:")
        demo_messages = [
            ("User", "What are the latest AI trends?"),
            ("Gemini", "[Grounded response with Google Search results]"),
            ("User", "Explain quantum computing"),
            ("Gemini", "[Detailed explanation with citations]"),
        ]
        for role, msg in demo_messages:
            print(f"  {role}: {msg}")

        print("\n📊 Grounding Example:")
        print("""
# Enable Google Search grounding
response = chat.send_message(
    "What's the current stock price of GOOGL?",
    tools=[{
        "google_search_retrieval": {
            "dynamic_retrieval_config": {
                "mode": "MODE_DYNAMIC"
            }
        }
    }]
)
# Response includes real-time data from search
        """)
        return

    print(f"\nProject: {PROJECT_ID}")
    print(f"Location: {LOCATION}")

    # Initialize
    initialize_vertex()
    print("\n✅ Vertex AI initialized")

    # Create chatbot
    print("\n💬 Starting chatbot...")
    chat = create_chatbot()

    # Demo conversation
    messages = [
        "Hello! What can you help me with?",
        "What are the key features of Gemini 2.0?",
        "How does grounding improve responses?",
    ]

    for msg in messages:
        print(f"\n👤 User: {msg}")
        try:
            response = chat_with_grounding(chat, msg, use_grounding=False)
            print(f"🤖 Gemini: {response[:300]}...")
        except Exception as e:
            print(f"   Error: {e}")

    print("\n✅ Chatbot demo complete!")

if __name__ == "__main__":
    main()
