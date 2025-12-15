# Sentry Error Tracking with AI Analysis

**Showcases:** Sentry SDK + AI-powered error grouping and analysis

## What it does
A Python application demonstrating Sentry's error tracking capabilities with AI-assisted error analysis. Captures exceptions, performance data, and uses Sentry's AI features to group and analyze errors intelligently.

## Latest Feature (December 2024)
- **AI Error Analysis** - Automatic root cause analysis
- **Issue Grouping** - AI-powered similar error detection
- **Performance Monitoring** - Transaction tracing
- **Session Replay** - (Web SDK) Visual error reproduction

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and add your Sentry DSN:
   ```bash
   cp .env.example .env
   ```

3. Run the demo:
   ```bash
   python main.py
   ```

## How to Use
- The script demonstrates various error types and how Sentry captures them
- View errors in your Sentry dashboard with AI-generated summaries
- Performance transactions show up in the Performance tab

## API Reference
- [Sentry Python SDK](https://docs.sentry.io/platforms/python/)
- [Sentry AI Features](https://docs.sentry.io/product/issues/issue-details/ai-suggested-fix/)
