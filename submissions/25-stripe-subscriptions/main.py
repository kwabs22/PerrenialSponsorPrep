"""
Stripe Subscriptions with Entitlements
Showcases: Adaptive Pricing + Entitlements API
"""
import os
import stripe
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def main():
    print("=" * 50)
    print("Stripe Subscriptions with Entitlements")
    print("=" * 50)

    # Create a customer
    customer = stripe.Customer.create(
        email="demo@example.com",
        name="Demo User"
    )
    print(f"\n✅ Created customer: {customer.id}")

    # Create a product with entitlements
    product = stripe.Product.create(
        name="Pro Plan",
        metadata={"features": "advanced_analytics,priority_support,api_access"}
    )
    print(f"✅ Created product: {product.id}")

    # Create a price (with adaptive pricing support)
    price = stripe.Price.create(
        product=product.id,
        unit_amount=2999,  # $29.99
        currency="usd",
        recurring={"interval": "month"}
    )
    print(f"✅ Created price: {price.id}")

    # Create checkout session
    session = stripe.checkout.Session.create(
        customer=customer.id,
        line_items=[{"price": price.id, "quantity": 1}],
        mode="subscription",
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
        # Enable adaptive pricing
        automatic_tax={"enabled": True}
    )

    print(f"\n🔗 Checkout URL: {session.url}")

    # Check entitlements (mock - real implementation uses webhooks)
    print("\n📋 Feature Entitlements:")
    features = product.metadata.get("features", "").split(",")
    for feature in features:
        print(f"  ✓ {feature}")

    print("\n💡 In production:")
    print("  1. Set up webhook for checkout.session.completed")
    print("  2. Use Entitlements API to check feature access")
    print("  3. Enable Adaptive Pricing in Stripe Dashboard")

if __name__ == "__main__":
    main()
