"""
Honeycomb Distributed Tracing Demo
Showcases: OpenTelemetry, spans, BubbleUp-ready attributes
"""

import os
from dotenv import load_dotenv
import time
import random

load_dotenv()

HONEYCOMB_API_KEY = os.getenv("HONEYCOMB_API_KEY")
SERVICE_NAME = os.getenv("SERVICE_NAME", "hackathon-demo")

# Initialize OpenTelemetry with Honeycomb exporter
tracer = None
try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.resources import Resource

    if HONEYCOMB_API_KEY:
        resource = Resource.create({"service.name": SERVICE_NAME})
        provider = TracerProvider(resource=resource)

        exporter = OTLPSpanExporter(
            endpoint="https://api.honeycomb.io/v1/traces",
            headers={"x-honeycomb-team": HONEYCOMB_API_KEY}
        )
        provider.add_span_processor(BatchSpanProcessor(exporter))
        trace.set_tracer_provider(provider)
        tracer = trace.get_tracer(__name__)
        print("Honeycomb tracing initialized")
    else:
        print("Warning: HONEYCOMB_API_KEY not set. Running in demo mode.")
except ImportError:
    print("OpenTelemetry not installed. Running in demo mode.")

def simulate_span(name: str, attributes: dict = None, duration_range=(0.1, 0.5)):
    """Simulate a traced operation"""
    duration = random.uniform(*duration_range)
    time.sleep(duration)
    return duration * 1000  # Return ms

def api_gateway_handler(request_path: str, user_id: str):
    """Simulate API gateway with tracing"""
    if tracer:
        with tracer.start_as_current_span("api.gateway") as span:
            span.set_attribute("http.path", request_path)
            span.set_attribute("user.id", user_id)
            span.set_attribute("http.method", "POST")

            # Auth check
            with tracer.start_as_current_span("auth.validate") as auth_span:
                auth_span.set_attribute("auth.type", "jwt")
                simulate_span("auth", duration_range=(0.05, 0.1))
                auth_span.set_attribute("auth.success", True)

            # Route to service
            result = recommendation_service(user_id)

            span.set_attribute("http.status_code", 200)
            return result
    else:
        print(f"  [Demo] api.gateway: {request_path}")
        simulate_span("auth")
        return recommendation_service(user_id)

def recommendation_service(user_id: str):
    """Simulate recommendation microservice"""
    if tracer:
        with tracer.start_as_current_span("recommendation.generate") as span:
            span.set_attribute("user.id", user_id)

            # Fetch user preferences
            with tracer.start_as_current_span("db.query") as db_span:
                db_span.set_attribute("db.system", "postgresql")
                db_span.set_attribute("db.operation", "SELECT")
                db_span.set_attribute("db.table", "user_preferences")
                duration = simulate_span("db", duration_range=(0.1, 0.3))
                db_span.set_attribute("db.duration_ms", duration)

            # Call ML model
            with tracer.start_as_current_span("ml.inference") as ml_span:
                ml_span.set_attribute("ml.model", "recommendation-v2")
                ml_span.set_attribute("ml.model_version", "2.1.0")
                duration = simulate_span("ml", duration_range=(0.2, 0.8))
                ml_span.set_attribute("ml.duration_ms", duration)
                ml_span.set_attribute("ml.items_scored", random.randint(100, 500))

            # Cache results
            with tracer.start_as_current_span("cache.write") as cache_span:
                cache_span.set_attribute("cache.type", "redis")
                cache_span.set_attribute("cache.key", f"recs:{user_id}")
                simulate_span("cache", duration_range=(0.01, 0.05))

            recommendations = [f"item-{i}" for i in random.sample(range(1000), 5)]
            span.set_attribute("recommendations.count", len(recommendations))
            return recommendations
    else:
        print("  [Demo] recommendation.generate")
        simulate_span("db")
        simulate_span("ml", duration_range=(0.2, 0.8))
        return ["item-1", "item-2", "item-3"]

def simulate_error_scenario():
    """Simulate an error for BubbleUp analysis"""
    if tracer:
        with tracer.start_as_current_span("api.request") as span:
            span.set_attribute("http.path", "/api/checkout")
            span.set_attribute("user.tier", "premium")

            # Simulate slow database
            with tracer.start_as_current_span("db.query") as db_span:
                db_span.set_attribute("db.system", "postgresql")
                # Artificially slow - will show up in BubbleUp
                duration = simulate_span("slow_db", duration_range=(2.0, 3.0))
                db_span.set_attribute("db.duration_ms", duration)
                db_span.set_attribute("db.slow_query", True)

            span.set_attribute("error", True)
            span.set_attribute("error.type", "TimeoutError")
            print("  Error scenario traced - check BubbleUp for analysis!")
    else:
        print("  [Demo] Would trace error scenario")

def load_test_demo():
    """Generate multiple traces for analysis"""
    print("\nGenerating load test traces...")

    users = ["user-1", "user-2", "user-3", "user-4", "user-5"]
    paths = ["/api/home", "/api/search", "/api/product", "/api/cart"]

    for i in range(10):
        user = random.choice(users)
        path = random.choice(paths)
        api_gateway_handler(path, user)
        print(f"  Request {i+1}: {path} (user: {user})")

    print("\n  10 traces generated!")

def main():
    print("=" * 50)
    print("Honeycomb Distributed Tracing Demo")
    print("=" * 50)

    if HONEYCOMB_API_KEY:
        print(f"Service: {SERVICE_NAME}")
    else:
        print("Running in demo mode (no API key)")

    print("\nAvailable demos:")
    print("  1. Single Request Trace")
    print("  2. Error Scenario (BubbleUp)")
    print("  3. Load Test (10 requests)")
    print("  4. Run all demos")

    choice = input("\nSelect demo (1-4): ").strip()

    if choice == "1":
        result = api_gateway_handler("/api/recommendations", "user-123")
        print(f"\nRecommendations: {result}")
    elif choice == "2":
        simulate_error_scenario()
    elif choice == "3":
        load_test_demo()
    elif choice == "4":
        api_gateway_handler("/api/test", "user-1")
        simulate_error_scenario()
        load_test_demo()
    else:
        print("Invalid choice")

    if HONEYCOMB_API_KEY:
        print("\nView traces at: https://ui.honeycomb.io")

if __name__ == "__main__":
    main()
