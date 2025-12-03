"""
Shopify AI Product Descriptions
Showcases: Storefront API + AI
"""
import os
from dotenv import load_dotenv
import requests
from openai import OpenAI

load_dotenv()

SHOPIFY_STORE = os.getenv("SHOPIFY_STORE")
SHOPIFY_TOKEN = os.getenv("SHOPIFY_STOREFRONT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

def fetch_products(limit: int = 10):
    """Fetch products from Shopify Storefront API."""
    query = """
    query {
        products(first: %d) {
            edges {
                node {
                    id
                    title
                    description
                    productType
                    vendor
                    priceRange {
                        minVariantPrice {
                            amount
                            currencyCode
                        }
                    }
                    images(first: 1) {
                        edges {
                            node {
                                url
                            }
                        }
                    }
                }
            }
        }
    }
    """ % limit

    response = requests.post(
        f"https://{SHOPIFY_STORE}/api/2024-01/graphql.json",
        json={"query": query},
        headers={
            "X-Shopify-Storefront-Access-Token": SHOPIFY_TOKEN,
            "Content-Type": "application/json"
        }
    )

    data = response.json()
    products = []

    for edge in data.get("data", {}).get("products", {}).get("edges", []):
        node = edge["node"]
        products.append({
            "id": node["id"],
            "title": node["title"],
            "description": node["description"],
            "type": node["productType"],
            "vendor": node["vendor"],
            "price": node["priceRange"]["minVariantPrice"]["amount"]
        })

    return products

def generate_description(product: dict, style: str = "professional"):
    """Generate AI product description."""
    if not openai_client:
        return f"[AI Description for {product['title']}]"

    styles = {
        "professional": "Write a professional, benefit-focused product description",
        "casual": "Write a friendly, conversational product description",
        "luxury": "Write an elegant, premium product description",
        "technical": "Write a detailed, specification-focused description"
    }

    prompt = f"""
{styles.get(style, styles['professional'])} for the following product:

Title: {product['title']}
Type: {product.get('type', 'Product')}
Brand: {product.get('vendor', 'Unknown')}
Price: ${product.get('price', 'N/A')}

Current description: {product.get('description', 'None')}

Write 2-3 sentences that highlight benefits and encourage purchase.
"""

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )

    return response.choices[0].message.content

def main():
    print("=" * 50)
    print("Shopify AI Product Descriptions")
    print("=" * 50)

    if not SHOPIFY_STORE or not SHOPIFY_TOKEN:
        print("\nSetup required:")
        print("1. Create Shopify store or use dev store")
        print("2. Create Storefront API access token")
        print("3. Copy credentials to .env file")

        print("\n🛍️ Features demonstrated:")
        print("  - Storefront API product queries")
        print("  - AI description generation")
        print("  - Multiple writing styles")
        print("  - Bulk description updates")

        print("\n📝 Sample GraphQL Query:")
        print("""
query {
    products(first: 10) {
        edges {
            node {
                id
                title
                description
            }
        }
    }
}
        """)

        # Demo mode
        demo_products = [
            {"title": "Wireless Earbuds Pro", "type": "Electronics", "vendor": "TechBrand", "price": "99.99"},
            {"title": "Organic Cotton T-Shirt", "type": "Apparel", "vendor": "EcoWear", "price": "29.99"},
        ]

        print("\n🤖 Demo AI Descriptions:")
        for product in demo_products:
            print(f"\n📦 {product['title']}")
            desc = generate_description(product, "professional")
            print(f"   {desc}")

        return

    print(f"\nStore: {SHOPIFY_STORE}")

    # Fetch products
    print("\n📦 Fetching products...")
    products = fetch_products(5)

    if not products:
        print("No products found")
        return

    print(f"Found {len(products)} products")

    # Generate descriptions
    print("\n🤖 Generating AI descriptions...")
    for product in products[:3]:
        print(f"\n--- {product['title']} ---")
        print(f"Current: {product['description'][:100]}...")

        new_desc = generate_description(product, "professional")
        print(f"AI Generated: {new_desc}")

    print("\n💡 To update products:")
    print("   Use Admin API with productUpdate mutation")

if __name__ == "__main__":
    main()
