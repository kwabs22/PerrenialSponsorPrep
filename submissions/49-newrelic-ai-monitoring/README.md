# New Relic AI Monitoring

**Showcases:** New Relic APM + AI Monitoring for ML applications

## What it does
Monitor AI/ML application performance with New Relic's AI Monitoring features. Track model inference latency, token usage, and error rates across your AI stack.

## Latest Feature (December 2024)
- **AI Monitoring** - Purpose-built dashboards for LLM apps
- **Model Performance** - Latency percentiles by model
- **Cost Tracking** - Token-based cost estimation
- **Error Analysis** - AI-powered error grouping

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and add your license key:
   ```bash
   cp .env.example .env
   ```

3. Run the demo:
   ```bash
   python main.py
   ```

## API Reference
- [New Relic Python Agent](https://docs.newrelic.com/docs/apm/agents/python-agent/)
- [AI Monitoring](https://docs.newrelic.com/docs/ai-monitoring/intro-to-ai-monitoring/)
