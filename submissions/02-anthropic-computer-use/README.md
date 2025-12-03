# Anthropic Computer Use Demo

**Showcases:** Claude Computer Use API (Public Beta)

## What it does
A screenshot analyzer that uses Claude's new Computer Use capability to understand what's on screen and suggest actions. Upload a screenshot and get intelligent suggestions for what to click, type, or do next.

## Latest Feature (October 2024)
- **Computer Use API** in public beta - Claude can see screens and suggest mouse/keyboard actions
- Works with Claude 3.5 Sonnet
- Supports screenshot analysis, cursor positioning, button clicking, and text typing
- First frontier AI model to offer this capability

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and add your Anthropic API key:
   ```bash
   cp .env.example .env
   ```

3. Run the analyzer:
   ```bash
   python main.py screenshot.png
   ```

## How to Use
- Take a screenshot of any application or webpage
- Run the script with the screenshot path as argument
- Claude will analyze the screen and suggest what actions to take
- Actions include: click coordinates, type text, scroll, etc.

## API Reference
- [Anthropic Computer Use Docs](https://docs.anthropic.com/en/docs/build-with-claude/computer-use)
- [Release Notes](https://docs.anthropic.com/en/release-notes/overview)
