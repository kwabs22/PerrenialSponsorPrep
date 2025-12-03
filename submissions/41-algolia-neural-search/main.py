"""
Algolia Neural Search
Showcases: NeuralSearch
"""
import os
from dotenv import load_dotenv
from algoliasearch.search.client import SearchClientSync

load_dotenv()

ALGOLIA_APP_ID = os.getenv("ALGOLIA_APP_ID")
ALGOLIA_API_KEY = os.getenv("ALGOLIA_API_KEY")
ALGOLIA_INDEX = os.getenv("ALGOLIA_INDEX", "products")

def get_algolia_client():
    """Initialize Algolia client."""
    return SearchClientSync(ALGOLIA_APP_ID, ALGOLIA_API_KEY)

def index_products(client, products: list):
    """Index products with NeuralSearch enabled."""
    client.save_objects(
        index_name=ALGOLIA_INDEX,
        objects=products
    )

    # Configure index for NeuralSearch
    client.set_settings(
        index_name=ALGOLIA_INDEX,
        index_settings={
            "searchableAttributes": ["name", "description", "category"],
            "attributesForFaceting": ["category", "brand"],
            # NeuralSearch settings
            "semanticSearch": {
                "enabled": True
            }
        }
    )

def neural_search(client, query: str, filters: str = None):
    """Perform NeuralSearch query."""
    search_params = {
        "query": query,
        "hitsPerPage": 10,
        # Enable semantic understanding
        "enableRules": True,
        "getRankingInfo": True
    }

    if filters:
        search_params["filters"] = filters

    response = client.search_single_index(
        index_name=ALGOLIA_INDEX,
        search_params=search_params
    )

    return response.hits

def main():
    print("=" * 50)
    print("Algolia Neural Search")
    print("=" * 50)

    if not ALGOLIA_APP_ID or not ALGOLIA_API_KEY:
        print("\nSetup required:")
        print("1. Create Algolia account at https://algolia.com")
        print("2. Create an application")
        print("3. Enable NeuralSearch in dashboard")
        print("4. Copy credentials to .env file")

        print("\n🔍 NeuralSearch Features:")
        print("  - Semantic understanding")
        print("  - Typo tolerance")
        print("  - Synonym expansion")
        print("  - Intent detection")

        print("\n📊 Example Queries:")
        queries = [
            ("laptop for coding", "Understands 'coding' means development"),
            ("comfortable shoes", "Semantic match for comfort features"),
            ("gift for mom", "Intent: gift + demographic"),
        ]

        for query, explanation in queries:
            print(f"\n  Query: '{query}'")
            print(f"  NeuralSearch: {explanation}")

        return

    client = get_algolia_client()
    print(f"\nApp ID: {ALGOLIA_APP_ID}")

    # Sample products
    products = [
        {
            "objectID": "1",
            "name": "MacBook Pro 16",
            "description": "Powerful laptop for developers and creatives",
            "category": "Electronics",
            "brand": "Apple",
            "price": 2499
        },
        {
            "objectID": "2",
            "name": "Ergonomic Office Chair",
            "description": "Comfortable seating for long work sessions",
            "category": "Furniture",
            "brand": "Herman Miller",
            "price": 899
        },
        {
            "objectID": "3",
            "name": "Noise-Canceling Headphones",
            "description": "Focus-enhancing audio for deep work",
            "category": "Electronics",
            "brand": "Sony",
            "price": 349
        }
    ]

    # Index products
    print("\n📦 Indexing products...")
    try:
        index_products(client, products)
        print(f"   Indexed {len(products)} products")
    except Exception as e:
        print(f"   Error: {e}")

    # Demo searches
    print("\n🔍 NeuralSearch Queries:")

    queries = [
        "computer for programming",
        "comfortable seating",
        "focus while working"
    ]

    for query in queries:
        print(f"\n  Query: '{query}'")
        try:
            results = neural_search(client, query)
            for hit in results[:2]:
                print(f"    - {hit.get('name')} (score: {hit.get('_rankingInfo', {}).get('nbTypos', 'N/A')})")
        except Exception as e:
            print(f"    Error: {e}")

    print("\n✅ NeuralSearch demo complete!")

if __name__ == "__main__":
    main()
