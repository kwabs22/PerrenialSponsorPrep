# Mistral AI Code Review Bot

**Showcases:** Codestral + Function Calling

## What it does
An AI-powered code review bot that analyzes your code and provides suggestions for improvements. Uses Mistral's Codestral model (specialized for code) with function calling to provide structured, actionable feedback.

## Latest Feature (2024)
- **Codestral** - Mistral's code-specialized model with 32K context
- **Function Calling** - Structured outputs for consistent review format
- Fill-in-the-middle (FIM) capability for code completion
- Supports 80+ programming languages
- Fast inference optimized for developer workflows

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and add your Mistral API key:
   ```bash
   cp .env.example .env
   ```

3. Run the code reviewer:
   ```bash
   python main.py your_code.py
   ```

## How to Use
- Provide a code file as input
- The bot analyzes the code using Codestral
- Get structured feedback: issues, suggestions, and improved code
- Works with Python, JavaScript, TypeScript, and 80+ other languages

## API Reference
- [Mistral API Docs](https://docs.mistral.ai/)
- [Codestral Docs](https://docs.mistral.ai/capabilities/code_generation/)
- [Changelog](https://docs.mistral.ai/getting-started/changelog)
