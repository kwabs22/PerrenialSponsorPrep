# Grafana Cloud Metrics

**Showcases:** Grafana Cloud Free Tier + Prometheus Metrics

## What it does
Push custom application metrics to Grafana Cloud and visualize them with pre-built dashboards. Perfect for monitoring hackathon projects in real-time.

## Latest Feature (December 2024)
- **Grafana Cloud Free** - 10K metrics, 50GB logs free
- **Prometheus Remote Write** - Easy metric ingestion
- **Dashboard Templates** - Pre-built visualizations
- **Alerting** - Threshold-based notifications

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and add your credentials:
   ```bash
   cp .env.example .env
   ```

3. Run the demo:
   ```bash
   python main.py
   ```

## API Reference
- [Grafana Cloud](https://grafana.com/docs/grafana-cloud/)
- [Prometheus Python Client](https://prometheus.github.io/client_python/)
