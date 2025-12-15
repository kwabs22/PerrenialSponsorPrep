"""
Grafana Cloud Metrics Demo
Showcases: Prometheus metrics, remote write, custom dashboards
"""

import os
from dotenv import load_dotenv
import time
import random
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

load_dotenv()

GRAFANA_USER = os.getenv("GRAFANA_USER")
GRAFANA_API_KEY = os.getenv("GRAFANA_API_KEY")
GRAFANA_PUSH_URL = os.getenv("GRAFANA_PUSH_URL")

# Initialize Prometheus client
try:
    from prometheus_client import Counter, Histogram, Gauge, generate_latest, REGISTRY
    from prometheus_client import push_to_gateway, CONTENT_TYPE_LATEST

    # Define metrics
    REQUEST_COUNT = Counter(
        'hackathon_requests_total',
        'Total HTTP requests',
        ['method', 'endpoint', 'status']
    )

    REQUEST_LATENCY = Histogram(
        'hackathon_request_latency_seconds',
        'Request latency in seconds',
        ['endpoint'],
        buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
    )

    ACTIVE_USERS = Gauge(
        'hackathon_active_users',
        'Number of active users'
    )

    LLM_TOKENS = Counter(
        'hackathon_llm_tokens_total',
        'Total LLM tokens used',
        ['model', 'type']
    )

    MODEL_LATENCY = Histogram(
        'hackathon_model_latency_seconds',
        'ML model inference latency',
        ['model']
    )

    print("Prometheus metrics initialized")
except ImportError:
    print("prometheus_client not installed. Running in demo mode.")
    REQUEST_COUNT = None

def record_request(method: str, endpoint: str, status: int, latency: float):
    """Record an HTTP request metric"""
    if REQUEST_COUNT:
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=str(status)).inc()
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)
    print(f"  Recorded: {method} {endpoint} -> {status} ({latency:.3f}s)")

def record_llm_usage(model: str, input_tokens: int, output_tokens: int, latency: float):
    """Record LLM usage metrics"""
    if LLM_TOKENS:
        LLM_TOKENS.labels(model=model, type="input").inc(input_tokens)
        LLM_TOKENS.labels(model=model, type="output").inc(output_tokens)
        MODEL_LATENCY.labels(model=model).observe(latency)
    print(f"  LLM: {model} - {input_tokens}+{output_tokens} tokens ({latency:.3f}s)")

def simulate_traffic():
    """Simulate realistic traffic patterns"""
    print("\nSimulating Traffic...")

    endpoints = ["/api/chat", "/api/search", "/api/recommend", "/api/analyze"]
    models = ["gpt-4", "gpt-3.5-turbo", "claude-3"]

    for i in range(20):
        # Simulate HTTP request
        endpoint = random.choice(endpoints)
        latency = random.uniform(0.1, 2.0)
        status = random.choices([200, 200, 200, 400, 500], weights=[85, 5, 5, 3, 2])[0]
        record_request("POST", endpoint, status, latency)

        # Simulate LLM call for some requests
        if endpoint == "/api/chat" and status == 200:
            model = random.choice(models)
            record_llm_usage(
                model,
                random.randint(50, 200),
                random.randint(100, 500),
                random.uniform(0.5, 3.0)
            )

        time.sleep(0.1)

    print(f"\n  Generated 20 request metrics!")

def update_active_users():
    """Simulate active user gauge"""
    print("\nUpdating Active Users Gauge...")

    for i in range(10):
        users = random.randint(10, 100)
        if ACTIVE_USERS:
            ACTIVE_USERS.set(users)
        print(f"  Active users: {users}")
        time.sleep(0.5)

def start_metrics_server(port: int = 8000):
    """Start a Prometheus metrics endpoint"""

    class MetricsHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/metrics":
                self.send_response(200)
                self.send_header("Content-Type", CONTENT_TYPE_LATEST)
                self.end_headers()
                self.wfile.write(generate_latest(REGISTRY))
            else:
                self.send_response(404)
                self.end_headers()

        def log_message(self, format, *args):
            pass  # Suppress logging

    server = HTTPServer(("", port), MetricsHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"\nMetrics server running at http://localhost:{port}/metrics")
    return server

def show_current_metrics():
    """Display current metric values"""
    print("\nCurrent Metrics:")
    if REQUEST_COUNT:
        print(generate_latest(REGISTRY).decode())
    else:
        print("  [Demo mode] No metrics collected")

def main():
    print("=" * 50)
    print("Grafana Cloud Metrics Demo")
    print("=" * 50)

    if GRAFANA_USER and GRAFANA_API_KEY:
        print(f"Grafana User: {GRAFANA_USER}")
    else:
        print("Running in demo mode (no Grafana credentials)")

    print("\nAvailable demos:")
    print("  1. Simulate Traffic (20 requests)")
    print("  2. Update Active Users Gauge")
    print("  3. Start Metrics Server (:8000)")
    print("  4. Show Current Metrics")
    print("  5. Run all demos")

    choice = input("\nSelect demo (1-5): ").strip()

    if choice == "1":
        simulate_traffic()
    elif choice == "2":
        update_active_users()
    elif choice == "3":
        start_metrics_server()
        print("\nPress Enter to stop...")
        input()
    elif choice == "4":
        show_current_metrics()
    elif choice == "5":
        simulate_traffic()
        update_active_users()
        show_current_metrics()
    else:
        print("Invalid choice")

    if GRAFANA_PUSH_URL:
        print(f"\nPush metrics to: {GRAFANA_PUSH_URL}")
    print("\nTo visualize in Grafana:")
    print("  1. Go to https://grafana.com/products/cloud/")
    print("  2. Import dashboard or create custom panels")
    print("  3. Query metrics like: hackathon_requests_total")

if __name__ == "__main__":
    main()
