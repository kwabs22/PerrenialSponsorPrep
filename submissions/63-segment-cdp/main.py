"""
Segment Customer Data Platform Demo
Showcases: Event tracking, identify, group, page tracking
"""

import os
from dotenv import load_dotenv
import time
import uuid

load_dotenv()

SEGMENT_WRITE_KEY = os.getenv("SEGMENT_WRITE_KEY")

# Initialize Segment
analytics = None
try:
    import segment.analytics as segment_analytics
    if SEGMENT_WRITE_KEY:
        segment_analytics.write_key = SEGMENT_WRITE_KEY
        analytics = segment_analytics
        print("Segment initialized")
    else:
        print("Warning: SEGMENT_WRITE_KEY not set. Running in demo mode.")
except ImportError:
    print("segment-analytics-python not installed. Running in demo mode.")

def identify_user(user_id: str, traits: dict):
    """Identify a user with traits"""
    print(f"\nIdentify: {user_id}")
    print(f"  Traits: {traits}")

    if analytics:
        analytics.identify(user_id, traits)
        print("  Sent to Segment!")
    else:
        print("  [Demo] Would send identify call")

def track_event(user_id: str, event: str, properties: dict = None):
    """Track a custom event"""
    print(f"\nTrack: {event}")
    print(f"  User: {user_id}")
    print(f"  Properties: {properties}")

    if analytics:
        analytics.track(user_id, event, properties or {})
        print("  Sent to Segment!")
    else:
        print("  [Demo] Would send track call")

def page_view(user_id: str, name: str, properties: dict = None):
    """Track a page view"""
    print(f"\nPage: {name}")

    if analytics:
        analytics.page(user_id, name=name, properties=properties or {})
        print("  Sent to Segment!")
    else:
        print("  [Demo] Would send page call")

def group_user(user_id: str, group_id: str, traits: dict):
    """Associate user with a group/company"""
    print(f"\nGroup: {group_id}")
    print(f"  Traits: {traits}")

    if analytics:
        analytics.group(user_id, group_id, traits)
        print("  Sent to Segment!")
    else:
        print("  [Demo] Would send group call")

def ecommerce_demo():
    """Demonstrate e-commerce tracking"""
    print("\nE-commerce Funnel Demo:")
    print("=" * 40)

    user_id = f"user-{uuid.uuid4().hex[:8]}"

    # Identify
    identify_user(user_id, {
        "email": f"{user_id}@demo.com",
        "name": "Demo User",
        "plan": "free"
    })

    # Product viewed
    track_event(user_id, "Product Viewed", {
        "product_id": "SKU-123",
        "name": "Wireless Headphones",
        "price": 79.99,
        "category": "Electronics"
    })

    # Added to cart
    track_event(user_id, "Product Added", {
        "product_id": "SKU-123",
        "quantity": 1,
        "cart_id": "cart-456"
    })

    # Checkout started
    track_event(user_id, "Checkout Started", {
        "cart_id": "cart-456",
        "products": [{"product_id": "SKU-123", "quantity": 1}],
        "total": 79.99
    })

    # Order completed
    track_event(user_id, "Order Completed", {
        "order_id": "order-789",
        "total": 79.99,
        "currency": "USD",
        "products": [{"product_id": "SKU-123", "quantity": 1, "price": 79.99}]
    })

    print("\n  Full funnel tracked!")

def saas_demo():
    """Demonstrate SaaS event tracking"""
    print("\nSaaS Product Demo:")
    print("=" * 40)

    user_id = f"user-{uuid.uuid4().hex[:8]}"

    # Sign up
    identify_user(user_id, {
        "email": f"{user_id}@company.com",
        "created_at": "2024-01-15",
        "plan": "free"
    })

    track_event(user_id, "Signed Up", {
        "signup_method": "google_oauth"
    })

    # Associate with company
    group_user(user_id, "company-abc", {
        "name": "Acme Inc",
        "industry": "Technology",
        "employees": 50
    })

    # Feature usage
    track_event(user_id, "Feature Used", {
        "feature": "ai_assistant",
        "usage_count": 1
    })

    # Upgrade
    track_event(user_id, "Plan Upgraded", {
        "previous_plan": "free",
        "new_plan": "pro",
        "mrr": 49.00
    })

    print("\n  SaaS journey tracked!")

def batch_tracking_demo():
    """Batch multiple events"""
    print("\nBatch Tracking Demo:")

    events = [
        ("Button Clicked", {"button_name": "cta_signup"}),
        ("Form Submitted", {"form_name": "contact"}),
        ("Video Played", {"video_id": "intro", "duration": 120}),
    ]

    user_id = "batch-demo-user"

    for event, props in events:
        track_event(user_id, event, props)
        time.sleep(0.1)

    if analytics:
        analytics.flush()
        print("\n  All events flushed!")

def destinations_info():
    """Information about destinations"""
    print("\nSegment Destinations:")
    print("-" * 40)

    print("""
Popular destinations you can send data to:

Analytics:
  - Google Analytics 4
  - Mixpanel
  - Amplitude
  - PostHog

Marketing:
  - HubSpot
  - Mailchimp
  - Braze
  - Customer.io

Data Warehouses:
  - Snowflake
  - BigQuery
  - Redshift
  - Databricks

Advertising:
  - Facebook Ads
  - Google Ads
  - LinkedIn Ads

All destinations receive the same events through
a single integration!
    """)

def main():
    print("=" * 50)
    print("Segment CDP Demo")
    print("=" * 50)

    if SEGMENT_WRITE_KEY:
        print("Connected to Segment")
    else:
        print("Running in demo mode (no write key)")

    print("\nAvailable demos:")
    print("  1. Identify User")
    print("  2. Track Event")
    print("  3. E-commerce Funnel")
    print("  4. SaaS Journey")
    print("  5. Batch Tracking")
    print("  6. Destinations Info")
    print("  7. Run all demos")

    choice = input("\nSelect demo (1-7): ").strip()

    if choice == "1":
        identify_user("demo-user", {"email": "demo@test.com", "name": "Demo"})
    elif choice == "2":
        track_event("demo-user", "Demo Event", {"key": "value"})
    elif choice == "3":
        ecommerce_demo()
    elif choice == "4":
        saas_demo()
    elif choice == "5":
        batch_tracking_demo()
    elif choice == "6":
        destinations_info()
    elif choice == "7":
        ecommerce_demo()
        saas_demo()
        destinations_info()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
