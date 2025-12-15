"""
Sentry Error Tracking Demo
Showcases: Error capture, performance monitoring, and AI analysis
"""

import os
import sentry_sdk
from sentry_sdk import capture_exception, capture_message, set_tag, set_user
from dotenv import load_dotenv
import time
import random

load_dotenv()

SENTRY_DSN = os.getenv("SENTRY_DSN")

def init_sentry():
    """Initialize Sentry with recommended settings"""
    if not SENTRY_DSN:
        print("Warning: SENTRY_DSN not set. Running in demo mode.")
        return False

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        # Performance monitoring
        traces_sample_rate=1.0,
        # Session tracking
        auto_session_tracking=True,
        # Environment
        environment="development",
        release="hackathon-demo@1.0.0",
        # AI-powered features enabled by default
    )
    return True

def simulate_user_context():
    """Set user context for error tracking"""
    set_user({
        "id": "user-123",
        "email": "demo@hackathon.com",
        "username": "hackathon_user"
    })
    set_tag("feature", "error-demo")

def divide_by_zero():
    """Simulate a division error"""
    return 1 / 0

def key_error_demo():
    """Simulate a key error"""
    data = {"name": "hackathon"}
    return data["missing_key"]

def api_error_demo():
    """Simulate an API error with context"""
    set_tag("api_endpoint", "/users")
    set_tag("http_method", "GET")
    raise ConnectionError("Failed to connect to external API")

def performance_transaction():
    """Demonstrate performance monitoring"""
    with sentry_sdk.start_transaction(op="task", name="process_data") as transaction:
        # Simulate database query
        with transaction.start_child(op="db.query", description="SELECT * FROM users"):
            time.sleep(random.uniform(0.1, 0.3))

        # Simulate external API call
        with transaction.start_child(op="http.client", description="GET /api/data"):
            time.sleep(random.uniform(0.2, 0.5))

        # Simulate data processing
        with transaction.start_child(op="process", description="transform_data"):
            time.sleep(random.uniform(0.05, 0.15))

    print("Performance transaction recorded!")

def breadcrumb_demo():
    """Show breadcrumbs leading up to an error"""
    sentry_sdk.add_breadcrumb(
        category="auth",
        message="User logged in",
        level="info"
    )
    sentry_sdk.add_breadcrumb(
        category="navigation",
        message="User visited /dashboard",
        level="info"
    )
    sentry_sdk.add_breadcrumb(
        category="action",
        message="User clicked 'Process Data'",
        level="info"
    )
    # Now trigger an error - breadcrumbs will be attached
    raise ValueError("Data processing failed after user action")

def main():
    print("=" * 50)
    print("Sentry Error Tracking Demo")
    print("=" * 50)

    initialized = init_sentry()
    simulate_user_context()

    demos = [
        ("Division by Zero", divide_by_zero),
        ("Key Error", key_error_demo),
        ("API Connection Error", api_error_demo),
        ("Breadcrumb Trail", breadcrumb_demo),
    ]

    print("\nAvailable demos:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"  {i}. {name}")
    print(f"  {len(demos) + 1}. Performance Transaction (no error)")
    print(f"  {len(demos) + 2}. Run all demos")

    choice = input("\nSelect demo (1-6): ").strip()

    try:
        choice = int(choice)
        if choice == len(demos) + 1:
            performance_transaction()
        elif choice == len(demos) + 2:
            # Run all
            performance_transaction()
            for name, func in demos:
                try:
                    print(f"\nRunning: {name}")
                    func()
                except Exception as e:
                    capture_exception(e)
                    print(f"  Captured: {type(e).__name__}: {e}")
        elif 1 <= choice <= len(demos):
            name, func = demos[choice - 1]
            print(f"\nRunning: {name}")
            func()
        else:
            print("Invalid choice")
    except ValueError:
        print("Please enter a number")
    except Exception as e:
        capture_exception(e)
        print(f"\nError captured and sent to Sentry!")
        print(f"  Type: {type(e).__name__}")
        print(f"  Message: {e}")
        if initialized:
            print("\nCheck your Sentry dashboard for AI-analyzed error details.")

if __name__ == "__main__":
    main()
