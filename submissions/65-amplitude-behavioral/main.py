"""
Amplitude Behavioral Analytics Demo
Showcases: Event tracking, user properties, revenue tracking
"""

import os
from dotenv import load_dotenv
import time
import uuid

load_dotenv()

AMPLITUDE_API_KEY = os.getenv("AMPLITUDE_API_KEY")

# Initialize Amplitude
amplitude = None
try:
    from amplitude import Amplitude, BaseEvent, Identify, Revenue, EventOptions
    if AMPLITUDE_API_KEY:
        amplitude = Amplitude(AMPLITUDE_API_KEY)
        print("Amplitude initialized")
    else:
        print("Warning: AMPLITUDE_API_KEY not set. Running in demo mode.")
except ImportError:
    print("amplitude-analytics not installed. Running in demo mode.")

def track_event(user_id: str, event_type: str, event_properties: dict = None):
    """Track an event"""
    print(f"\nTrack: {event_type}")
    print(f"  User: {user_id}")
    if event_properties:
        print(f"  Properties: {event_properties}")

    if amplitude:
        event = BaseEvent(
            event_type=event_type,
            user_id=user_id,
            event_properties=event_properties or {}
        )
        amplitude.track(event)
        print("  Sent to Amplitude!")
    else:
        print("  [Demo] Would send event")

def identify_user(user_id: str, user_properties: dict):
    """Set user properties"""
    print(f"\nIdentify: {user_id}")
    print(f"  Properties: {user_properties}")

    if amplitude:
        identify = Identify()
        for key, value in user_properties.items():
            identify.set(key, value)

        amplitude.identify(identify, EventOptions(user_id=user_id))
        print("  User identified!")
    else:
        print("  [Demo] Would identify user")

def track_revenue(user_id: str, product_id: str, price: float, quantity: int = 1):
    """Track revenue event"""
    print(f"\nRevenue: ${price * quantity:.2f}")
    print(f"  Product: {product_id}")

    if amplitude:
        revenue = Revenue(
            product_id=product_id,
            price=price,
            quantity=quantity
        )
        amplitude.revenue(revenue, EventOptions(user_id=user_id))
        print("  Revenue tracked!")
    else:
        print("  [Demo] Would track revenue")

def user_journey_demo():
    """Complete user journey tracking"""
    print("\nUser Journey Demo:")
    print("=" * 40)

    user_id = f"user-{uuid.uuid4().hex[:8]}"
    session_id = int(time.time() * 1000)

    # Identify user
    identify_user(user_id, {
        "email": f"{user_id}@demo.com",
        "plan": "free",
        "signup_date": "2024-01-15"
    })

    # Page views
    pages = ["home", "features", "pricing"]
    for page in pages:
        track_event(user_id, "Page Viewed", {
            "page_name": page,
            "session_id": session_id
        })
        time.sleep(0.1)

    # Sign up
    track_event(user_id, "Sign Up Completed", {
        "signup_method": "google",
        "session_id": session_id
    })

    # Feature usage
    track_event(user_id, "Feature Used", {
        "feature_name": "dashboard",
        "duration_ms": 45000
    })

    print("\n  Journey tracked!")

def ecommerce_demo():
    """E-commerce tracking"""
    print("\nE-commerce Demo:")
    print("=" * 40)

    user_id = "ecommerce-demo-user"

    # Product viewed
    track_event(user_id, "Product Viewed", {
        "product_id": "SKU-001",
        "product_name": "Wireless Headphones",
        "category": "Electronics",
        "price": 79.99
    })

    # Added to cart
    track_event(user_id, "Add to Cart", {
        "product_id": "SKU-001",
        "quantity": 1,
        "cart_value": 79.99
    })

    # Checkout
    track_event(user_id, "Checkout Started", {
        "cart_size": 1,
        "cart_value": 79.99
    })

    # Purchase
    track_revenue(user_id, "SKU-001", 79.99, 1)

    track_event(user_id, "Purchase Completed", {
        "order_id": "ORD-12345",
        "total": 79.99,
        "items": 1
    })

    print("\n  E-commerce funnel tracked!")

def experiment_demo():
    """A/B test tracking"""
    print("\nExperiment Demo:")
    print("=" * 40)

    experiment_name = "new_onboarding_flow"
    variants = ["control", "variant_1", "variant_2"]

    # Assign users to variants
    for i in range(9):
        user_id = f"exp-user-{i}"
        variant = variants[i % 3]

        # Track exposure
        track_event(user_id, "$exposure", {
            "experiment": experiment_name,
            "variant": variant
        })

        # Track conversion
        if variant != "control" or i % 2 == 0:
            track_event(user_id, "Onboarding Completed", {
                "experiment": experiment_name,
                "variant": variant
            })

    print("\n  Experiment data tracked!")

def group_demo():
    """Group analytics for B2B"""
    print("\nGroup Analytics Demo:")
    print("=" * 40)

    if amplitude:
        # Set group
        identify = Identify()
        identify.set("company_id", "acme-inc")
        identify.set("company_name", "Acme Inc")
        identify.set("plan", "enterprise")

        amplitude.identify(identify, EventOptions(user_id="user-123"))

        # Track with group
        event = BaseEvent(
            event_type="Feature Used",
            user_id="user-123",
            event_properties={"feature": "advanced_analytics"},
            groups={"company": "acme-inc"}
        )
        amplitude.track(event)
        print("  Group event tracked!")
    else:
        print("  [Demo] Group analytics allows:")
        print("    - Account-level tracking")
        print("    - B2B metrics")
        print("    - Company-based cohorts")

def retention_info():
    """Information about retention analysis"""
    print("\nRetention Analysis:")
    print("=" * 40)

    print("""
Amplitude automatically calculates retention:

Retention Types:
  - N-Day: Users who return on day N
  - Unbounded: Users who return on or after day N
  - Bracket: Users who return within a range

Sample Retention Curve:
  Day 0:  100% (baseline)
  Day 1:   45%
  Day 7:   28%
  Day 14:  22%
  Day 30:  15%

Track these events for retention:
  1. "Sign Up" - Starting event
  2. "App Opened" / "Session Start" - Return event

Amplitude builds the curve automatically!
    """)

def main():
    print("=" * 50)
    print("Amplitude Behavioral Analytics Demo")
    print("=" * 50)

    if AMPLITUDE_API_KEY:
        print("Connected to Amplitude")
    else:
        print("Running in demo mode (no API key)")

    print("\nAvailable demos:")
    print("  1. Track Event")
    print("  2. User Journey")
    print("  3. E-commerce Tracking")
    print("  4. Experiment Tracking")
    print("  5. Group Analytics")
    print("  6. Retention Info")
    print("  7. Run all demos")

    choice = input("\nSelect demo (1-7): ").strip()

    if choice == "1":
        track_event("demo-user", "Demo Event", {"key": "value"})
    elif choice == "2":
        user_journey_demo()
    elif choice == "3":
        ecommerce_demo()
    elif choice == "4":
        experiment_demo()
    elif choice == "5":
        group_demo()
    elif choice == "6":
        retention_info()
    elif choice == "7":
        user_journey_demo()
        ecommerce_demo()
        retention_info()
    else:
        print("Invalid choice")

    # Flush events
    if amplitude:
        amplitude.flush()

if __name__ == "__main__":
    main()
