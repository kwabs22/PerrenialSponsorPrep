"""
Mixpanel Event Analytics Demo
Showcases: Event tracking, user profiles, funnel analysis
"""

import os
from dotenv import load_dotenv
import time
import uuid
import json

load_dotenv()

MIXPANEL_TOKEN = os.getenv("MIXPANEL_TOKEN")

# Initialize Mixpanel
mp = None
try:
    from mixpanel import Mixpanel
    if MIXPANEL_TOKEN:
        mp = Mixpanel(MIXPANEL_TOKEN)
        print("Mixpanel initialized")
    else:
        print("Warning: MIXPANEL_TOKEN not set. Running in demo mode.")
except ImportError:
    print("mixpanel not installed. Running in demo mode.")

def track_event(distinct_id: str, event: str, properties: dict = None):
    """Track an event"""
    print(f"\nTrack: {event}")
    print(f"  User: {distinct_id}")
    if properties:
        print(f"  Properties: {json.dumps(properties, indent=4)}")

    if mp:
        mp.track(distinct_id, event, properties or {})
        print("  Sent to Mixpanel!")
    else:
        print("  [Demo] Would send event")

def set_user_profile(distinct_id: str, properties: dict):
    """Set user profile properties"""
    print(f"\nProfile Update: {distinct_id}")
    print(f"  Properties: {properties}")

    if mp:
        mp.people_set(distinct_id, properties)
        print("  Profile updated!")
    else:
        print("  [Demo] Would update profile")

def increment_property(distinct_id: str, prop: str, value: int = 1):
    """Increment a numeric property"""
    print(f"\nIncrement: {prop} by {value}")

    if mp:
        mp.people_increment(distinct_id, {prop: value})
        print("  Incremented!")
    else:
        print("  [Demo] Would increment property")

def user_journey_demo():
    """Demonstrate a complete user journey"""
    print("\nUser Journey Demo:")
    print("=" * 40)

    user_id = f"user-{uuid.uuid4().hex[:8]}"

    # Set initial profile
    set_user_profile(user_id, {
        "$email": f"{user_id}@demo.com",
        "$name": "Demo User",
        "$created": "2024-01-15T10:00:00",
        "plan": "free",
        "source": "organic"
    })

    # Track signup
    track_event(user_id, "Sign Up", {
        "signup_method": "email",
        "referrer": "google.com"
    })

    # Track onboarding steps
    for step in ["profile_completed", "first_project", "invite_sent"]:
        track_event(user_id, "Onboarding Step", {
            "step_name": step,
            "completed": True
        })
        time.sleep(0.1)

    # Track feature usage
    track_event(user_id, "Feature Used", {
        "feature_name": "ai_assistant",
        "duration_seconds": 45
    })

    # Increment usage counter
    increment_property(user_id, "features_used")
    increment_property(user_id, "total_sessions")

    print("\n  Journey complete!")

def funnel_demo():
    """Simulate funnel data"""
    print("\nFunnel Analysis Demo:")
    print("=" * 40)

    funnel_steps = [
        "Landing Page Viewed",
        "Signup Button Clicked",
        "Signup Form Submitted",
        "Email Verified",
        "First Action Completed"
    ]

    # Simulate 100 users going through funnel
    users = 100
    drop_rates = [0.3, 0.2, 0.15, 0.1]  # Drop rate at each step

    print("\n  Simulated Funnel:")
    print(f"  {'Step':<30} | Users | Conv%")
    print("  " + "-" * 50)

    for i, step in enumerate(funnel_steps):
        conv_pct = 100 * users / 100
        print(f"  {step:<30} | {users:>5} | {conv_pct:>4.0f}%")

        if i < len(drop_rates):
            users = int(users * (1 - drop_rates[i]))

    print("\n  Track these events to build funnels in Mixpanel!")

def cohort_demo():
    """Demonstrate cohort tracking"""
    print("\nCohort Analysis Demo:")
    print("=" * 40)

    cohorts = {
        "Jan 2024 Signups": {"signup_month": "2024-01", "count": 150},
        "Feb 2024 Signups": {"signup_month": "2024-02", "count": 180},
        "Mar 2024 Signups": {"signup_month": "2024-03", "count": 220},
    }

    print("\n  Sample Cohorts:")
    for name, data in cohorts.items():
        print(f"    {name}: {data['count']} users")

    print("\n  Retention (sample):")
    print("  Week    | Jan   | Feb   | Mar")
    print("  " + "-" * 35)
    print("  Week 0  | 100%  | 100%  | 100%")
    print("  Week 1  |  65%  |  68%  |  70%")
    print("  Week 2  |  45%  |  48%  |  52%")
    print("  Week 4  |  32%  |  35%  |  38%")

def ab_test_demo():
    """Track A/B test events"""
    print("\nA/B Test Tracking Demo:")
    print("=" * 40)

    # Assign users to variants
    variants = ["control", "variant_a", "variant_b"]

    for i in range(10):
        user_id = f"test-user-{i}"
        variant = variants[i % 3]

        # Track experiment exposure
        track_event(user_id, "$experiment_started", {
            "experiment_name": "new_checkout_flow",
            "variant": variant
        })

        # Simulate conversion
        if variant == "variant_b" or (variant == "control" and i % 3 == 0):
            track_event(user_id, "Checkout Completed", {
                "experiment": "new_checkout_flow",
                "variant": variant
            })

    print("\n  Experiment events tracked!")

def group_analytics_demo():
    """B2B group/account analytics"""
    print("\nGroup Analytics Demo (B2B):")
    print("=" * 40)

    if mp:
        # Set group profile
        mp.group_set("company", "acme-inc", {
            "name": "Acme Inc",
            "industry": "Technology",
            "plan": "enterprise",
            "employees": 500
        })

        # Track event for group
        mp.track("user-123", "Feature Used", {
            "$group_key": "company",
            "$group_id": "acme-inc",
            "feature": "advanced_reporting"
        })
        print("  Group analytics tracked!")
    else:
        print("  [Demo] Group analytics allows:")
        print("    - Track events at account level")
        print("    - Analyze B2B metrics")
        print("    - Account-based funnels")

def main():
    print("=" * 50)
    print("Mixpanel Analytics Demo")
    print("=" * 50)

    if MIXPANEL_TOKEN:
        print("Connected to Mixpanel")
    else:
        print("Running in demo mode (no token)")

    print("\nAvailable demos:")
    print("  1. Track Event")
    print("  2. User Journey")
    print("  3. Funnel Analysis")
    print("  4. Cohort Analysis")
    print("  5. A/B Test Tracking")
    print("  6. Group Analytics (B2B)")
    print("  7. Run all demos")

    choice = input("\nSelect demo (1-7): ").strip()

    if choice == "1":
        track_event("demo-user", "Demo Event", {"key": "value"})
    elif choice == "2":
        user_journey_demo()
    elif choice == "3":
        funnel_demo()
    elif choice == "4":
        cohort_demo()
    elif choice == "5":
        ab_test_demo()
    elif choice == "6":
        group_analytics_demo()
    elif choice == "7":
        user_journey_demo()
        funnel_demo()
        cohort_demo()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
