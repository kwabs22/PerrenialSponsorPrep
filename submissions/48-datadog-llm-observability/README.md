# Datadog LLM Observability

**Showcases:** Datadog APM + LLM Observability for AI applications

## What it does
Monitor your LLM-powered applications with Datadog's specialized AI observability features. Track token usage, latency, errors, and costs across OpenAI, Anthropic, and other LLM providers.

## Latest Feature (December 2024)
- **LLM Observability** - Purpose-built monitoring for AI apps
- **Token Tracking** - Input/output token counts and costs
- **Prompt/Response Logging** - Full conversation capture
- **Model Performance** - Latency and error rate by model

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and add your keys:
   ```bash
   cp .env.example .env
   ```

3. Run the demo:
   ```bash
   python main.py
   ```

## API Reference
- [Datadog LLM Observability](https://docs.datadoghq.com/llm_observability/)
- [ddtrace Python](https://docs.datadoghq.com/tracing/trace_collection/dd_libraries/python/)
