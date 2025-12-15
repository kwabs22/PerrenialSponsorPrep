# Snowflake Cortex AI

**Showcases:** Snowflake Cortex for AI/ML in the data warehouse

## What it does
Run AI/ML models directly in Snowflake with Cortex. Use built-in LLMs, embeddings, and ML functions without moving data - perfect for secure enterprise AI.

## Latest Feature (December 2024)
- **Cortex LLM Functions** - GPT-4, Claude, Llama in SQL
- **Cortex Search** - Semantic search on warehouse data
- **Cortex Analyst** - Natural language to SQL
- **ML Functions** - Forecasting, anomaly detection

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and add credentials:
   ```bash
   cp .env.example .env
   ```

3. Run the demo:
   ```bash
   python main.py
   ```

## API Reference
- [Snowflake Cortex](https://docs.snowflake.com/en/guides-overview-ai-features)
- [Python Connector](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector)
