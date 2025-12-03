"""
Weaviate AI Product Catalog
Showcases: Generative Search Modules
1-hour hackathon submission
"""
import os
import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.query import MetadataQuery
from dotenv import load_dotenv

load_dotenv()

def main():
    print("=" * 50)
    print("Weaviate AI Product Catalog")
    print("Showcasing: Generative Search")
    print("=" * 50)

    # Connect to Weaviate Cloud
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=os.getenv("WEAVIATE_URL"),
        auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WEAVIATE_API_KEY")),
        headers={"X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")}
    )

    try:
        # Create collection with generative module
        if not client.collections.exists("Product"):
            client.collections.create(
                name="Product",
                vectorizer_config=Configure.Vectorizer.text2vec_openai(),
                generative_config=Configure.Generative.openai(),
                properties=[
                    Property(name="name", data_type=DataType.TEXT),
                    Property(name="description", data_type=DataType.TEXT),
                    Property(name="category", data_type=DataType.TEXT),
                    Property(name="price", data_type=DataType.NUMBER),
                ]
            )
            print("Created Product collection")

        products = client.collections.get("Product")

        # Add sample products
        sample_products = [
            {"name": "Wireless Headphones", "description": "Premium noise-canceling headphones with 30-hour battery", "category": "Electronics", "price": 299.99},
            {"name": "Smart Watch", "description": "Fitness tracker with heart rate monitor and GPS", "category": "Electronics", "price": 199.99},
            {"name": "Laptop Stand", "description": "Ergonomic aluminum stand for better posture", "category": "Office", "price": 49.99},
            {"name": "Coffee Maker", "description": "Programmable drip coffee maker with thermal carafe", "category": "Kitchen", "price": 79.99},
        ]

        for product in sample_products:
            products.data.insert(product)
        print(f"Added {len(sample_products)} products")

        # Generative search demo
        print("\n🔍 Generative Search Demo")
        query = "I need something for working from home"

        response = products.generate.near_text(
            query=query,
            limit=2,
            grouped_task="Based on these products, recommend the best option for someone working from home and explain why."
        )

        print(f"\nQuery: {query}")
        print(f"\n💡 AI Recommendation:\n{response.generated}")

        for obj in response.objects:
            print(f"\n  - {obj.properties['name']}: ${obj.properties['price']}")

    finally:
        client.close()

if __name__ == "__main__":
    main()
