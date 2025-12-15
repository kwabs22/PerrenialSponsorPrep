"""
PostHog Product Analytics Demo
Showcases: Events, feature flags, user identification
"""

import os
from dotenv import load_dotenv
import time
import random
import uuid

load_dotenv()

POSTHOG_API_KEY = os.getenv("POSTHOG_API_KEY")
POSTHOG_HOST = os.getenv("POSTHOG_HOST", "https://app.posthog.com")

# Initialize PostHog
posthog = None
try:
    import posthog as ph
    if POSTHOG_API_KEY:
        ph.api_key = POSTHOG_API_KEY
        ph.host = POSTHOG_HOST
        posthog = ph
        print("PostHog initialized")
    else:
        print("Warning: POSTHOG_API_KEY not set. Running in demo mode.")
except ImportError:
    print("posthog not installed. Running in demo mode.")

def capture_event(distinct_id: str, event: str, properties: dict = None):
    """Capture an analytics event"""
    if posthog:
        posthog.capture(distinct_id, event, properties or {})
    print(f"  Event: {event} (user: {distinct_id})")
    if properties:
        for k, v in properties.items():
            print(f"    {k}: {v}")

def identify_user(distinct_id: str, properties: dict):
    """Identify a user with properties"""
    if posthog:
        posthog.identify(distinct_id, properties)
    print(f"  Identified user: {distinct_id}")
    for k, v in properties.items():
        print(f"    {k}: {v}")

def check_feature_flag(distinct_id: str, flag_key: str) -> bool:
    """Check if a feature flag is enabled"""
    if posthog:
        enabled = posthog.feature_enabled(flag_key, distinct_id)
    else:
        # Demo mode: randomly enable
        enabled = random.choice([True, False])

    print(f"  Feature '{flag_key}': {'ENABLED' if enabled else 'DISABLED'} for {distinct_id}")
    return enabled

def simulate_user_journey():
    """Simulate a complete user journey"""
    print("\nSimulating User Journey...")

    user_id = f"user-{uuid.uuid4().hex[:8]}"

    # Identify the user
    identify_user(user_id, {
        "email": f"{user_id}@demo.com",
        "name": "Demo User",
        "plan": random.choice(["free", "pro", "enterprise"]),
        "signed_up": "2024-01-15"
    })

    # Page views
    pages = ["/", "/features", "/pricing", "/signup"]
    for page in pages:
        capture_event(user_id, "$pageview", {
            "$current_url": f"https://app.example.com{page}",
            "referrer": "google.com" if page == "/" else None
        })
        time.sleep(0.1)

    # Sign up
    capture_event(user_id, "user_signed_up", {
        "signup_method": random.choice(["google", "email", "github"]),
        "referral_code": "HACKATHON2024" if random.random() > 0.5 else None
    })

    # Feature usage
    capture_event(user_id, "feature_used", {
        "feature_name": "ai_chat",
        "tokens_used": random.randint(100, 1000),
        "model": "gpt-4"
    })

    print(f"\n  Journey complete for {user_id}!")

def feature_flag_demo():
    """Demonstrate feature flags for A/B testing"""
    print("\nFeature Flag Demo (A/B Test)...")

    flag_key = "new-checkout-flow"
    users = [f"user-{i}" for i in range(10)]

    group_a = []
    group_b = []

    for user_id in users:
        if check_feature_flag(user_id, flag_key):
            group_b.append(user_id)
            capture_event(user_id, "checkout_started", {"variant": "new"})
        else:
            group_a.append(user_id)
            capture_event(user_id, "checkout_started", {"variant": "control"})

    print(f"\n  Control (A): {len(group_a)} users")
    print(f"  Variant (B): {len(group_b)} users")

def funnel_analysis_demo():
    """Generate events for funnel analysis"""
    print("\nFunnel Analysis Demo...")

    funnel_steps = [
        ("page_viewed", {"page": "landing"}),
        ("signup_clicked", {}),
        ("form_started", {}),
        ("form_completed", {}),
        ("onboarding_started", {}),
        ("first_action_completed", {})
    ]

    users = [f"user-{i}" for i in range(20)]

    for step_idx, (event, props) in enumerate(funnel_steps):
        # Simulate drop-off at each step
        drop_rate = 0.2 + (step_idx * 0.05)
        remaining_users = [u for u in users if random.random() > drop_rate]

        for user_id in remaining_users:
            capture_event(user_id, event, props)

        users = remaining_users
        print(f"  Step {step_idx + 1}: {event} - {len(users)} users")

    print(f"\n  Funnel complete! {len(users)} users completed all steps.")

def cohort_demo():
    """Demonstrate cohort properties"""
    print("\nCohort Demo...")

    cohorts = {
        "power_users": {"actions_per_day": ">10", "days_active": ">7"},
        "churned": {"last_seen": ">30 days ago"},
        "enterprise": {"plan": "enterprise", "seats": ">5"}
    }

    for cohort_name, criteria in cohorts.items():
        user_id = f"cohort-demo-{cohort_name}"
        identify_user(user_id, {
            "cohort": cohort_name,
            **criteria
        })

def main():
    print("=" * 50)
    print("PostHog Product Analytics Demo")
    print("=" * 50)

    if POSTHOG_API_KEY:
        print(f"Connected to: {POSTHOG_HOST}")
    else:
        print("Running in demo mode (no API key)")

    print("\nAvailable demos:")
    print("  1. User Journey Simulation")
    print("  2. Feature Flags (A/B Test)")
    print("  3. Funnel Analysis")
    print("  4. Cohort Properties")
    print("  5. Run all demos")

    choice = input("\nSelect demo (1-5): ").strip()

    if choice == "1":
        simulate_user_journey()
    elif choice == "2":
        feature_flag_demo()
    elif choice == "3":
        funnel_analysis_demo()
    elif choice == "4":
        cohort_demo()
    elif choice == "5":
        simulate_user_journey()
        feature_flag_demo()
        funnel_analysis_demo()
        cohort_demo()
    else:
        print("Invalid choice")

    # Flush events
    if posthog:
        posthog.flush()
        print("\nEvents flushed to PostHog!")
        print(f"View at: {POSTHOG_HOST}/events")

if __name__ == "__main__":
    main()
