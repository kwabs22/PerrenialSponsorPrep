# Honeycomb Distributed Tracing

**Showcases:** Honeycomb OpenTelemetry + BubbleUp Analysis

## What it does
Implement distributed tracing for microservices with Honeycomb's powerful query and analysis capabilities. Uses OpenTelemetry for instrumentation and Honeycomb's BubbleUp for automatic anomaly detection.

## Latest Feature (December 2024)
- **BubbleUp Analysis** - Automatic anomaly detection
- **OpenTelemetry Native** - First-class OTel support
- **SLO Management** - Service level objective tracking
- **Query Builder** - Powerful trace exploration

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and add your API key:
   ```bash
   cp .env.example .env
   ```

3. Run the demo:
   ```bash
   python main.py
   ```

## API Reference
- [Honeycomb Python](https://docs.honeycomb.io/send-data/python/)
- [OpenTelemetry Python](https://opentelemetry-python.readthedocs.io/)
