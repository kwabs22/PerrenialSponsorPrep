# DuckDB In-Browser Analytics

**Showcases:** DuckDB WASM for in-browser SQL analytics

## What it does
Run powerful SQL analytics directly in the browser with DuckDB's WebAssembly build. Process CSV, Parquet, and JSON files locally without a server - perfect for data exploration tools.

## Latest Feature (December 2024)
- **WASM Build** - Full SQL engine in browser
- **Extensions** - JSON, Parquet, spatial support
- **Arrow Integration** - Zero-copy data exchange
- **httpfs** - Query remote files directly

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the demo:
   ```bash
   python main.py
   ```

## API Reference
- [DuckDB Docs](https://duckdb.org/docs/)
- [DuckDB WASM](https://duckdb.org/docs/api/wasm/overview.html)
