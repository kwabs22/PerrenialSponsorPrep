"""
Databricks Mosaic AI Demo
Showcases: Foundation models, vector search, model serving
"""

import os
from dotenv import load_dotenv
import json

load_dotenv()

DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")

# Initialize Databricks
databricks = None
try:
    from databricks.sdk import WorkspaceClient
    if DATABRICKS_HOST and DATABRICKS_TOKEN:
        databricks = WorkspaceClient(
            host=DATABRICKS_HOST,
            token=DATABRICKS_TOKEN
        )
        print("Databricks client initialized")
    else:
        print("Warning: Databricks credentials not set. Running in demo mode.")
except ImportError:
    print("databricks-sdk not installed. Running in demo mode.")

def foundation_model_demo():
    """Call foundation models via Model Serving"""
    print("\nFoundation Model Demo:")

    if databricks:
        # Call a served model
        response = databricks.serving_endpoints.query(
            name="databricks-llama-2-70b-chat",
            inputs={"prompt": "Explain data lakehouse in one sentence"}
        )
        print(f"  Response: {response.predictions[0]}")
    else:
        print("  [Demo] Foundation Model API:")
        print("    Endpoint: databricks-llama-2-70b-chat")
        print("    Response: 'A data lakehouse combines data lake and warehouse...'")

def vector_search_demo():
    """Demonstrate vector search"""
    print("\nVector Search Demo:")

    example = """
    -- Create vector search index
    CREATE VECTOR SEARCH INDEX product_index
    ON products (description_embedding)
    OPTIONS (
        index_type = 'DELTA_SYNC',
        pipeline_type = 'TRIGGERED'
    );

    -- Query similar items
    SELECT * FROM VECTOR_SEARCH(
        index_name => 'product_index',
        query_vector => embed('wireless headphones'),
        num_results => 5
    );
    """

    print("  SQL Example:")
    print(example)

    print("\n  Python SDK:")
    print("""
    from databricks.vector_search.client import VectorSearchClient

    client = VectorSearchClient()
    index = client.get_index("product_index")

    results = index.similarity_search(
        query_text="wireless headphones",
        columns=["name", "price"],
        num_results=5
    )
    """)

def model_serving_demo():
    """Deploy custom models"""
    print("\nModel Serving Demo:")

    if databricks:
        # List endpoints
        endpoints = databricks.serving_endpoints.list()
        print("  Existing endpoints:")
        for ep in endpoints:
            print(f"    - {ep.name}: {ep.state}")
    else:
        print("  [Demo] Create serving endpoint:")
        print("""
    config = EndpointCoreConfigInput(
        served_models=[
            ServedModelInput(
                model_name="my-model",
                model_version="1",
                workload_size="Small",
                scale_to_zero_enabled=True
            )
        ]
    )

    endpoint = w.serving_endpoints.create(
        name="my-model-endpoint",
        config=config
    )
        """)

def ai_gateway_demo():
    """Unified API for multiple LLM providers"""
    print("\nAI Gateway Demo:")

    print("  AI Gateway provides unified access to:")
    print("    - OpenAI (GPT-4, GPT-3.5)")
    print("    - Anthropic (Claude)")
    print("    - Meta (Llama)")
    print("    - Databricks Foundation Models")

    example = """
    # Route requests through AI Gateway
    from mlflow.deployments import get_deploy_client

    client = get_deploy_client("databricks")

    response = client.predict(
        endpoint="chat",
        inputs={
            "messages": [
                {"role": "user", "content": "Hello!"}
            ]
        }
    )
    """
    print(f"\n  Example:{example}")

def agent_framework_demo():
    """Build AI agents with Mosaic"""
    print("\nAgent Framework Demo:")

    example = '''
    from databricks.agents import Agent, Tool

    # Define tools
    @Tool
    def search_products(query: str) -> list:
        """Search product catalog"""
        return vector_search(query)

    @Tool
    def check_inventory(product_id: str) -> dict:
        """Check product availability"""
        return get_inventory(product_id)

    # Create agent
    agent = Agent(
        name="shopping-assistant",
        model="databricks-llama-2-70b-chat",
        tools=[search_products, check_inventory],
        system_prompt="You are a helpful shopping assistant."
    )

    # Run agent
    response = agent.chat("Find me wireless headphones under $100")
    '''

    print("  Agent Example:")
    print(example)

def feature_store_demo():
    """Feature engineering for ML"""
    print("\nFeature Store Demo:")

    print("  Feature Store enables:")
    print("    - Centralized feature management")
    print("    - Point-in-time lookups")
    print("    - Online/offline serving")
    print("    - Feature lineage tracking")

    example = """
    from databricks.feature_engineering import FeatureEngineeringClient

    fe = FeatureEngineeringClient()

    # Create feature table
    fe.create_table(
        name="user_features",
        primary_keys=["user_id"],
        df=features_df,
        description="User behavior features"
    )

    # Create training set
    training_set = fe.create_training_set(
        df=labels_df,
        feature_lookups=[
            FeatureLookup(
                table_name="user_features",
                lookup_key="user_id"
            )
        ]
    )
    """
    print(example)

def main():
    print("=" * 50)
    print("Databricks Mosaic AI Demo")
    print("=" * 50)

    if DATABRICKS_HOST:
        print(f"Host: {DATABRICKS_HOST}")
    else:
        print("Running in demo mode (no credentials)")

    print("\nAvailable demos:")
    print("  1. Foundation Models")
    print("  2. Vector Search")
    print("  3. Model Serving")
    print("  4. AI Gateway")
    print("  5. Agent Framework")
    print("  6. Feature Store")
    print("  7. Run all demos")

    choice = input("\nSelect demo (1-7): ").strip()

    if choice == "1":
        foundation_model_demo()
    elif choice == "2":
        vector_search_demo()
    elif choice == "3":
        model_serving_demo()
    elif choice == "4":
        ai_gateway_demo()
    elif choice == "5":
        agent_framework_demo()
    elif choice == "6":
        feature_store_demo()
    elif choice == "7":
        foundation_model_demo()
        vector_search_demo()
        ai_gateway_demo()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
