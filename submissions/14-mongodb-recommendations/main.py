"""
MongoDB Vector Search Recommendations
Showcases: Atlas Vector Search
"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def main():
    print("=" * 50)
    print("MongoDB Vector Search Recommendations")
    print("=" * 50)

    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client["hackathon"]
    products = db["products"]

    # Sample products with mock embeddings
    sample_products = [
        {"name": "Laptop", "category": "Electronics", "price": 999, "embedding": [0.1]*128},
        {"name": "Headphones", "category": "Electronics", "price": 199, "embedding": [0.2]*128},
        {"name": "Book", "category": "Books", "price": 29, "embedding": [0.3]*128},
    ]

    products.delete_many({})
    products.insert_many(sample_products)
    print(f"Inserted {len(sample_products)} products")

    # Vector search requires Atlas Search index - demo aggregation
    # In production, create a vector search index in Atlas UI
    pipeline = [
        {"$match": {"category": "Electronics"}},
        {"$sort": {"price": -1}},
        {"$limit": 2}
    ]

    results = list(products.aggregate(pipeline))
    print("\n🔍 Top Electronics:")
    for p in results:
        print(f"  - {p['name']}: ${p['price']}")

    print("\n💡 For vector search, create an Atlas Search index with type 'vectorSearch'")

if __name__ == "__main__":
    main()
