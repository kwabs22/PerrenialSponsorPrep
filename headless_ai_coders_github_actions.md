# Headless AI Coders + GitHub Actions: 10 Options Guide

> Comprehensive guide to integrating AI coding agents into your CI/CD pipelines for automated code review, PR generation, and development workflows.

---

## Table of Contents

1. [Overview & Comparison Matrix](#overview--comparison-matrix)
2. [Option 1: Claude Code Action](#option-1-claude-code-action)
3. [Option 2: Gemini CLI GitHub Actions](#option-2-gemini-cli-github-actions)
4. [Option 3: OpenAI Codex Action](#option-3-openai-codex-action)
5. [Option 4: Cursor CLI](#option-4-cursor-cli)
6. [Option 5: GitHub Copilot Coding Agent](#option-5-github-copilot-coding-agent)
7. [Option 6: Amazon Q Developer](#option-6-amazon-q-developer)
8. [Option 7: Qodo Merge / PR-Agent](#option-7-qodo-merge--pr-agent)
9. [Option 8: CodeRabbit](#option-8-coderabbit)
10. [Option 9: Sourcery AI](#option-9-sourcery-ai)
11. [Option 10: Sweep AI](#option-10-sweep-ai)
12. [Option 11: OpenAI Apps SDK + MCP](#option-11-openai-apps-sdk--mcp)
13. [Use Case Recommendations](#use-case-recommendations)
14. [Security Best Practices](#security-best-practices)

---

## Overview & Comparison Matrix

| Tool | Provider | Type | Pricing | Best For | Setup Time |
|------|----------|------|---------|----------|------------|
| **Claude Code** | Anthropic | Full agent | API usage | Complex multi-file changes | 10 min |
| **Gemini CLI** | Google | Full agent | Free | Large context, enterprise | 15 min |
| **Codex CLI** | OpenAI | Full agent | API usage | Auto-fix CI failures | 10 min |
| **Cursor CLI** | Cursor | Full agent | Subscription | PR reviews, IDE companion | 30 min |
| **Copilot Agent** | GitHub | Native agent | Pro+/Enterprise | Issue-to-PR automation | 5 min |
| **Amazon Q** | AWS | Full agent | Free tier | AWS ecosystem, Java migration | 20 min |
| **Qodo Merge** | Qodo | PR reviewer | Free OSS | Multi-model, self-hosted | 10 min |
| **CodeRabbit** | CodeRabbit | PR reviewer | Free OSS | Detailed line comments | 5 min |
| **Sourcery** | Sourcery | PR reviewer | Free OSS | Python/JS/TS focus | 5 min |
| **Sweep AI** | Sweep | Issue-to-PR | Free OSS | Issue automation | 10 min |

### Capability Matrix

| Tool | Code Gen | Code Review | Auto-fix | @mention | Self-hosted |
|------|:--------:|:-----------:|:--------:|:--------:|:-----------:|
| Claude Code | ✅ | ✅ | ✅ | ✅ | ❌ |
| Gemini CLI | ✅ | ✅ | ✅ | ✅ | ❌ |
| Codex CLI | ✅ | ✅ | ✅ | ❌ | ❌ |
| Cursor CLI | ✅ | ✅ | ✅ | ❌ | ❌ |
| Copilot Agent | ✅ | ✅ | ✅ | ✅ | ❌ |
| Amazon Q | ✅ | ✅ | ✅ | ✅ | ❌ |
| Qodo Merge | ❌ | ✅ | ✅ | ✅ | ✅ |
| CodeRabbit | ❌ | ✅ | ❌ | ✅ | ❌ |
| Sourcery | ❌ | ✅ | ❌ | ❌ | ✅ |
| Sweep AI | ✅ | ❌ | ❌ | ✅ | ✅ |

---

## Option 1: Claude Code Action

**Official Action:** `anthropics/claude-code-action`

### Overview
Anthropic's official GitHub Action brings Claude Code's agentic capabilities to your CI/CD. It can answer questions, implement features, and create PRs - all triggered by @claude mentions or automated workflows.

### Quick Setup (Recommended)
```bash
# In your terminal with Claude Code installed
claude /install-github-app
```
This guides you through setting up the GitHub app and required secrets.

### Manual Workflow Setup

```yaml
# .github/workflows/claude-code.yml
name: Claude Code Agent

on:
  issue_comment:
    types: [created]
  issues:
    types: [opened, assigned]
  pull_request_review_comment:
    types: [created]

jobs:
  claude-agent:
    if: |
      contains(github.event.comment.body, '@claude') ||
      contains(github.event.issue.assignees.*.login, 'claude')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          # Or use Bedrock:
          # use_bedrock: true
          # aws_access_key_id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          # aws_secret_access_key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          # aws_region: us-east-1
```

### Headless Mode for Automation

```yaml
# .github/workflows/claude-headless.yml
name: Claude Headless Tasks

on:
  schedule:
    - cron: '0 0 * * *'  # Daily
  workflow_dispatch:
    inputs:
      prompt:
        description: 'Task for Claude'
        required: true

jobs:
  run-claude:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Run Claude Headless
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude -p "${{ github.event.inputs.prompt || 'Update copyright headers to 2025' }}" \
            --allowedTools Edit,View,Bash \
            --output-format json
```

### Key Features
- **Agentic subagents**: Spawns specialized agents for complex tasks
- **MCP support**: Extend capabilities with Model Context Protocol
- **Multi-provider**: Works with Anthropic API, AWS Bedrock, Google Vertex, Azure
- **Progress tracking**: Visual indicators in GitHub comments

### Authentication Options
```yaml
# Anthropic Direct
anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}

# AWS Bedrock
use_bedrock: true
aws_access_key_id: ${{ secrets.AWS_ACCESS_KEY_ID }}
aws_secret_access_key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

# Google Vertex AI
use_vertex: true
gcp_project_id: your-project
gcp_region: us-central1
```

### Resources
- [GitHub Action](https://github.com/anthropics/claude-code-action)
- [Claude Code Docs](https://code.claude.com/docs/en/github-actions)
- [Headless Mode Guide](https://code.claude.com/docs/en/headless)
- [Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Ultimate Claude Code Guide (Hidden Tricks)](https://dev.to/holasoymalva/the-ultimate-claude-code-guide-every-hidden-trick-hack-and-power-feature-you-need-to-know-2l45)

---

## Option 2: Gemini CLI GitHub Actions

**Official Action:** `google-github-actions/run-gemini-cli`

### Overview
Google's Gemini CLI brings 1M+ token context to GitHub Actions - perfect for large codebases and complex refactoring. Free to use with excellent enterprise security features.

### Quick Setup

```yaml
# .github/workflows/gemini-cli.yml
name: Gemini CLI Agent

on:
  issues:
    types: [opened, labeled]
  issue_comment:
    types: [created]
  pull_request:
    types: [opened, synchronize]

jobs:
  gemini-agent:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: actions/checkout@v4

      - uses: google-github-actions/run-gemini-cli@v1
        with:
          gemini_api_key: ${{ secrets.GEMINI_API_KEY }}
          # Optional: Use Workload Identity Federation for enterprise
          # workload_identity_provider: 'projects/PROJECT/locations/global/workloadIdentityPools/POOL/providers/PROVIDER'
```

### On-Demand Collaboration

Mention `@gemini-cli` in any issue or PR comment:
```
@gemini-cli /review
@gemini-cli write tests for this bug
@gemini-cli implement the changes suggested above
```

### Automated Issue Triage

```yaml
# .github/workflows/gemini-triage.yml
name: Gemini Issue Triage

on:
  issues:
    types: [opened]

jobs:
  triage:
    runs-on: ubuntu-latest
    steps:
      - uses: google-github-actions/run-gemini-cli@v1
        with:
          gemini_api_key: ${{ secrets.GEMINI_API_KEY }}
          prompt: |
            Analyze this issue and:
            1. Suggest appropriate labels
            2. Estimate complexity (low/medium/high)
            3. Identify related files that may need changes
          output_format: json
```

### Project-Specific Context

Create `GEMINI.md` in your repository root:
```markdown
# Project Context for Gemini

## Architecture
- Frontend: React + TypeScript
- Backend: Python FastAPI
- Database: PostgreSQL

## Coding Standards
- Use functional components with hooks
- All API endpoints must have OpenAPI docs
- Tests required for new features

## Important Files
- src/api/routes.py - API endpoints
- src/components/ - React components
```

### Security Features
- **Command allowlisting**: Explicitly approve shell commands
- **Workload Identity Federation**: Short-lived tokens for enterprise
- **OpenTelemetry integration**: Stream logs to your observability platform
- **Custom agent identity**: Precise permission control

### Resources
- [GitHub Action](https://github.com/google-github-actions/run-gemini-cli)
- [Gemini CLI Repo](https://github.com/google-gemini/gemini-cli)
- [Google Blog Announcement](https://blog.google/technology/developers/introducing-gemini-cli-github-actions/)

---

## Option 3: OpenAI Codex Action

**Official Action:** `openai/codex-action`

### Overview
OpenAI's Codex CLI, powered by the codex-1 model (optimized o3), excels at autonomous coding with self-healing capabilities. The official GitHub Action provides tight security controls.

### Quick Setup

```yaml
# .github/workflows/codex.yml
name: Codex Agent

on:
  pull_request:
    types: [opened, synchronize]
  workflow_dispatch:
    inputs:
      prompt:
        description: 'Task for Codex'
        required: true

jobs:
  codex-review:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    steps:
      - uses: actions/checkout@v4

      - uses: openai/codex-action@v1
        with:
          openai_api_key: ${{ secrets.OPENAI_API_KEY }}
          prompt: "Review this PR for bugs and security issues"
          # Safety mode: drop-sudo (default), read-only, or none
          safety: drop-sudo
```

### Auto-Fix CI Failures

```yaml
# .github/workflows/codex-autofix.yml
name: Codex Auto-Fix

on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]

jobs:
  autofix:
    if: ${{ github.event.workflow_run.conclusion == 'failure' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: openai/codex-action@v1
        with:
          openai_api_key: ${{ secrets.OPENAI_API_KEY }}
          prompt-file: .github/codex/prompts/fix-ci.md
          codex-args: '["--full-auto"]'
          safety: drop-sudo
```

Create `.github/codex/prompts/fix-ci.md`:
```markdown
The CI build failed. Please:
1. Analyze the error logs
2. Identify the root cause
3. Apply minimal fixes
4. Run tests to verify
5. Create a PR with the fix
```

### Safety Strategies

| Strategy | Description | Best For |
|----------|-------------|----------|
| `drop-sudo` | Removes sudo access (default) | GitHub-hosted runners |
| `read-only` | Filesystem is read-only | Audit/review only |
| `none` | Full access | Self-hosted secure runners |

### Configuration Options

```yaml
- uses: openai/codex-action@v1
  with:
    openai_api_key: ${{ secrets.OPENAI_API_KEY }}
    # Inline prompt or file
    prompt: "Your task here"
    prompt-file: .github/codex/prompts/task.md
    # Extra CLI arguments (JSON array or shell string)
    codex-args: '["--full-auto", "--model", "codex-1"]'
    # Safety mode
    safety: drop-sudo
```

### Resources
- [GitHub Action](https://github.com/openai/codex-action)
- [Auto-fix CI Guide](https://cookbook.openai.com/examples/codex/autofix-github-actions)
- [Codex SDK Docs](https://developers.openai.com/codex/sdk/)

---

## Option 4: Cursor CLI

**Documentation:** [cursor.com/docs/cli/github-actions](https://cursor.com/docs/cli/github-actions)

### Overview
Cursor CLI brings the popular AI IDE's capabilities to your terminal and CI/CD pipelines. Ideal for teams already using Cursor who want automated PR reviews.

### Setup

```yaml
# .github/workflows/cursor-review.yml
name: Cursor PR Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install Cursor CLI
        run: |
          curl -fsSL https://cursor.com/install-cli.sh | bash
          echo "$HOME/.cursor/bin" >> $GITHUB_PATH

      - name: Run Cursor Review
        env:
          CURSOR_API_KEY: ${{ secrets.CURSOR_API_KEY }}
        run: |
          # Get diff
          git diff origin/main...HEAD > pr.diff

          # Run review
          cursor-cli review --diff pr.diff --output github-comments
```

### Permission Configuration

Create `.cursor/permissions.yaml`:
```yaml
allow:
  - read: "**/*.md"
  - read: "**/*.ts"
  - write: "docs/**"
  - shell: "npm test"
  - shell: "npm run lint"

deny:
  - shell: "git *"
  - write: ".env*"
  - write: "*.key"
```

### Autonomy Levels

```yaml
# Conservative - requires approval for each action
cursor-cli agent --autonomy conservative

# Balanced - auto-approve safe operations
cursor-cli agent --autonomy balanced

# Full - complete control (use with caution)
cursor-cli agent --autonomy full
```

### Resources
- [Official Docs](https://docs.cursor.com/en/cli/github-actions)
- [Cursor Website](https://cursor.com/)

---

## Option 5: GitHub Copilot Coding Agent

**Built into GitHub** - Available for Copilot Pro+ and Enterprise

### Overview
GitHub's native AI agent runs in GitHub Actions, implementing features and fixing bugs when you assign issues to Copilot. The most seamlessly integrated option.

### Setup

1. Enable Copilot coding agent in your organization settings
2. Assign issues to `@copilot` or use VS Code integration

```yaml
# Issues assigned to Copilot automatically trigger the agent
# No workflow file needed - it's built into GitHub!
```

### Manual Trigger via API

```yaml
# .github/workflows/copilot-trigger.yml
name: Trigger Copilot Agent

on:
  issues:
    types: [labeled]

jobs:
  assign-to-copilot:
    if: contains(github.event.issue.labels.*.name, 'copilot')
    runs-on: ubuntu-latest
    steps:
      - name: Assign to Copilot
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.issues.addAssignees({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              assignees: ['copilot']
            });
```

### How It Works

1. Assign a GitHub issue to Copilot
2. Copilot spins up a secure dev environment via GitHub Actions
3. Agent analyzes codebase, makes changes, pushes commits
4. Creates a draft PR for your review
5. You review, request changes, or merge

### Key Features
- **Native integration**: No external setup needed
- **Branch protections apply**: Existing security policies enforced
- **Human approval required**: CI/CD only runs after PR approval
- **VS Code integration**: Start tasks from your IDE

### AgentHQ (November 2025)
Create custom agents for:
- Issue triage and documentation
- Testing automation
- Deployment workflows

### Pricing
- Included in Copilot Pro+ and Enterprise
- Uses premium requests (1 per model request)

### Resources
- [Copilot Coding Agent Docs](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent)
- [GitHub Blog Announcement](https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/)

---

## Option 6: Amazon Q Developer

**AWS Integration** - Preview on GitHub

### Overview
Amazon Q Developer brings AWS's AI coding capabilities to GitHub, excelling at automated feature development, code reviews, and Java modernization.

### Setup

```yaml
# .github/workflows/amazon-q.yml
name: Amazon Q Developer

on:
  issues:
    types: [labeled]
  pull_request:
    types: [opened, synchronize]

jobs:
  q-developer:
    if: contains(github.event.issue.labels.*.name, 'amazon-q')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Install Amazon Q CLI
        run: |
          curl -fsSL https://d2eo22ngex1n9g.cloudfront.net/Documentation/CLI/q-cli.sh | bash

      - name: Run Q Developer
        run: |
          q /dev --issue "${{ github.event.issue.number }}"
```

### Automated Code Review

```yaml
# .github/workflows/q-review.yml
name: Amazon Q Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Run Q Review
        run: |
          q review --pr ${{ github.event.pull_request.number }}
```

### Feature Development Flow

1. Add `amazon-q` label to an issue
2. Q Developer analyzes the codebase
3. Generates code with full context
4. Creates a PR with changes
5. Posts progress updates as comments

### Key Features
- **Java modernization**: Excellent for legacy Java migration
- **Security scanning**: Automatic vulnerability detection
- **AWS integration**: Native support for AWS services
- **Terraform generation**: IaC in minutes

### Resources
- [AWS Blog](https://aws.amazon.com/blogs/aws/amazon-q-developer-in-github-now-in-preview-with-code-generation-review-and-legacy-transformation-capabilities/)
- [Community Guide](https://community.aws/content/2uN0wiRmSJ0A1Crs110ZGCVOsoi/automated-task-development-with-amazon-q-and-github-actions)

---

## Option 7: Qodo Merge / PR-Agent

**Open Source:** `qodo-ai/pr-agent`

### Overview
The most flexible option - supports multiple LLMs (GPT, Claude, Gemini, local models), multiple git providers, and can be self-hosted. Free for open source.

### Quick Setup (GitHub Action)

```yaml
# .github/workflows/pr-agent.yml
name: PR-Agent

on:
  pull_request:
    types: [opened, reopened, ready_for_review]
  issue_comment:
    types: [created]

jobs:
  pr-agent:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: qodo-ai/pr-agent@main
        env:
          OPENAI_KEY: ${{ secrets.OPENAI_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          # Auto-run on new PRs
          github_action_config.auto_review: "true"
          github_action_config.auto_describe: "true"
          github_action_config.auto_improve: "true"
```

### Multi-Model Configuration

```yaml
# Using Claude
- uses: qodo-ai/pr-agent@main
  env:
    ANTHROPIC.KEY: ${{ secrets.ANTHROPIC_API_KEY }}
    config.model: "anthropic/claude-3-opus-20240229"
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

# Using Gemini
- uses: qodo-ai/pr-agent@main
  env:
    GOOGLE_AI_STUDIO.GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
    config.model: "gemini/gemini-1.5-flash"
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

# Using Local Ollama
- uses: qodo-ai/pr-agent@main
  env:
    OLLAMA.API_BASE: "http://localhost:11434"
    config.model: "ollama/codellama"
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Available Commands

| Command | Description |
|---------|-------------|
| `/review` | Full code review with suggestions |
| `/describe` | Auto-generate PR description |
| `/improve` | Suggest code improvements |
| `/ask <question>` | Ask about the PR |
| `/update_changelog` | Update CHANGELOG.md |
| `/add_docs` | Generate documentation |

### Self-Hosted Deployment

```yaml
# docker-compose.yml
version: '3.8'
services:
  pr-agent:
    image: codiumai/pr-agent:latest
    environment:
      - OPENAI_KEY=${OPENAI_API_KEY}
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    ports:
      - "3000:3000"
```

### Resources
- [GitHub Repo](https://github.com/qodo-ai/pr-agent)
- [Documentation](https://qodo-merge-docs.qodo.ai/)
- [Qodo Merge (Hosted)](https://www.qodo.ai/products/qodo-merge/)

---

## Option 8: CodeRabbit

**GitHub App + Action:** `coderabbitai/ai-pr-reviewer`

### Overview
CodeRabbit provides detailed, line-by-line code reviews with learning capabilities. Free for open source, with incremental reviews on each commit.

### Quick Setup (GitHub App - Recommended)

1. Install from [GitHub Marketplace](https://github.com/apps/coderabbitai)
2. Add `.github/coderabbit.yaml` for configuration:

```yaml
# .github/coderabbit.yaml
language: en
reviews:
  profile: assertive  # chill, assertive, or thorough
  path_instructions:
    - path: "**/*.test.*"
      instructions: "Focus on test coverage and edge cases"
    - path: "src/api/**"
      instructions: "Check for security vulnerabilities"
  auto_review:
    enabled: true
    ignore_title_keywords:
      - "WIP"
      - "DO NOT MERGE"
chat:
  auto_reply: true
```

### GitHub Action Setup

```yaml
# .github/workflows/coderabbit.yml
name: CodeRabbit Review

on:
  pull_request:
    types: [opened, synchronize]
  pull_request_review_comment:
    types: [created]

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: coderabbitai/ai-pr-reviewer@latest
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        with:
          debug: false
          review_simple_changes: false
          review_comment_lgtm: false
```

### Key Features
- **Incremental reviews**: Reviews each commit, not just the final diff
- **Learning**: Improves based on your feedback
- **PR visualization**: Code flow diagrams
- **Issue validation**: Verifies linked issues
- **Chat interface**: Ask questions about the PR

### Benchmarks
- 74% faster first feedback (42 min → 11 min)
- 31% fewer formatting comments after deployment

### Resources
- [GitHub App](https://github.com/apps/coderabbitai)
- [Action Repo](https://github.com/coderabbitai/ai-pr-reviewer)
- [Documentation](https://docs.coderabbit.ai/)

---

## Option 9: Sourcery AI

**GitHub App:** `sourcery-ai` | **Action:** Available

### Overview
Sourcery specializes in code quality with deep static analysis for Python, JavaScript, and TypeScript. Uses both OpenAI and Anthropic for reviews.

### Quick Setup (GitHub App)

1. Install from [GitHub Marketplace](https://github.com/marketplace/sourcery-ai)
2. Automatic reviews on all PRs

### Configuration

Create `.sourcery.yaml` in your repository:

```yaml
# .sourcery.yaml
refactor:
  skip:
    - tests/*
    - docs/*

rule_settings:
  enable:
    - default
    - google-python-style

metrics:
  quality_threshold: 25.0

review:
  request_changes_on_quality_below: 20.0
```

### GitHub Action (Alternative)

```yaml
# .github/workflows/sourcery.yml
name: Sourcery Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  sourcery:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Sourcery Review
        uses: sourcery-ai/sourcery-action@v1
        with:
          token: ${{ secrets.SOURCERY_TOKEN }}
```

### Key Features
- **Static analysis**: Deep refactoring suggestions
- **30+ languages**: General reviews for all languages
- **Python/JS/TS focus**: Most detailed for these languages
- **IDE integration**: Review before committing
- **No code storage**: Code not retained or used for training

### Pricing
- **Free**: Public repos / open source
- **Pro**: $12/month for private repos
- **Enterprise**: Self-hosted option available

### Resources
- [GitHub Marketplace](https://github.com/marketplace/sourcery-ai)
- [Documentation](https://sourcery.ai/)

---

## Option 10: Sweep AI

**GitHub App:** `sweep-ai` | **Repo:** `sweepai/sweep`

### Overview
Sweep turns GitHub issues into pull requests automatically. Ideal for bug fixes, small features, and repetitive tasks. Now also available as a JetBrains plugin.

### Quick Setup

1. Install from [GitHub Apps](https://github.com/apps/sweep-ai)
2. Create issues with "Sweep:" prefix

### Usage

Create an issue:
```markdown
Title: Sweep: Add input validation to user registration

Body:
Add validation for:
- Email format
- Password strength (min 8 chars, 1 number, 1 special)
- Username uniqueness check

Files to modify:
- src/auth/register.py
- src/validators/user.py
```

Sweep will:
1. Analyze your codebase
2. Plan the changes
3. Create a PR with the implementation
4. Run your test suite

### Self-Hosted Deployment

```yaml
# docker-compose.yml
version: '3.8'
services:
  sweep:
    image: sweepai/sweep:latest
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GITHUB_APP_ID=${GITHUB_APP_ID}
      - GITHUB_APP_PRIVATE_KEY=${GITHUB_APP_PRIVATE_KEY}
    ports:
      - "8080:8080"
```

### Configuration

Create `sweep.yaml` in your repository:

```yaml
# sweep.yaml
branch: main
blocked_dirs:
  - node_modules
  - .git
  - dist
draft: false
description: |
  Sweep is an AI junior developer.
  Repository: Python FastAPI backend with React frontend.
```

### Key Features
- **Issue-to-PR**: Complete end-to-end automation
- **Follow-up comments**: Iterate via issue comments
- **Self-hosted option**: Full control over your data
- **Multi-language**: Python, JS/TS, Java, Go, C#, C++, Rust

### Resources
- [GitHub App](https://github.com/apps/sweep-ai)
- [Documentation](https://docs.sweep.dev/)
- [GitHub Repo](https://github.com/sweepai/sweep)

---

## Option 11: OpenAI Apps SDK + MCP

**Build custom ChatGPT integrations with MCP connectors**

### Overview

The OpenAI Apps SDK lets developers create custom apps that run inside ChatGPT, extending it with MCP (Model Context Protocol) connectors for both read and write operations. Available since October 2025.

### Key Features

- **Developer Mode**: Full MCP client support for read/write operations
- **Custom UI Components**: Build React components that render in ChatGPT
- **Tool Execution**: Call external APIs, update databases, trigger workflows
- **OAuth Support**: Secure authentication for third-party services

### Availability

| Plan | Access |
|------|--------|
| Pro | ✅ |
| Plus | ✅ |
| Business | ✅ |
| Enterprise | ✅ |
| Education | ✅ |

### Enable Developer Mode

1. **Admin Setup**: Workspace Settings → Permissions & Roles → Developer mode
2. **User Setup**: Settings → Connectors → Advanced → Developer Mode
3. **Add MCP Server**: Register your server URL (HTTPS required)

### Building an MCP Server

```typescript
// Basic MCP server structure
import { createServer } from '@modelcontextprotocol/sdk';

const server = createServer({
  tools: {
    'create-issue': {
      description: 'Create a GitHub issue',
      parameters: {
        title: { type: 'string' },
        body: { type: 'string' }
      },
      handler: async ({ title, body }) => {
        // Create issue via GitHub API
        return { success: true, issueNumber: 123 };
      }
    }
  }
});

server.listen(3000);
```

### Building Custom UI Components

```typescript
// React component for ChatGPT
import { useOpenAiGlobal, useWidgetState } from '@openai/apps-sdk';

export function IssueCard() {
  const { theme, locale } = useOpenAiGlobal();
  const [state, setState] = useWidgetState({ selected: null });

  const handleCreateIssue = async () => {
    const result = await window.openai.callTool('create-issue', {
      title: 'Bug fix needed',
      body: 'Description here'
    });
    setState({ selected: result.issueNumber });
  };

  return (
    <div className={theme === 'dark' ? 'dark' : 'light'}>
      <button onClick={handleCreateIssue}>Create Issue</button>
    </div>
  );
}
```

### Core APIs

| API | Purpose |
|-----|---------|
| `callTool()` | Execute MCP tool |
| `sendFollowUpMessage()` | Insert messages into conversation |
| `requestDisplayMode()` | Switch layouts (inline/PIP/fullscreen) |
| `setWidgetState()` | Persist state across sessions |
| `requestClose()` | Close widget |
| `openExternal()` | Navigate to external URLs |

### Security Notes

- Write operations show confirmation modal before execution
- Use OAuth for secure third-party authentication
- Sanitize inputs to prevent prompt injection
- HTTPS required for all connections

### Development Setup

```bash
# 1. Create MCP server
npm init -y
npm install @modelcontextprotocol/sdk

# 2. Tunnel localhost (for development)
npx ngrok http 3000

# 3. Add connector in ChatGPT
# Settings → Connectors → Add → Use ngrok URL
```

### Resources
- [Apps SDK Overview](https://openai.com/index/introducing-apps-in-chatgpt/)
- [Build with Apps SDK](https://help.openai.com/en/articles/12515353-build-with-the-apps-sdk)
- [Developer Mode & MCP](https://help.openai.com/en/articles/12584461-developer-mode-apps-and-full-mcp-connectors-in-chatgpt-beta)
- [ChatGPT UI Components](https://developers.openai.com/apps-sdk/build/chatgpt-ui)
- [Build MCP Server](https://developers.openai.com/apps-sdk/build/mcp-server/)
- [Example Apps](https://github.com/openai/openai-apps-sdk-examples)

---

## Use Case Recommendations

### By Task Type

| Task | Recommended Tools |
|------|-------------------|
| **PR Code Review** | CodeRabbit, Sourcery, Qodo Merge |
| **Issue → PR Automation** | Copilot Agent, Sweep, Amazon Q |
| **Auto-fix CI Failures** | Codex CLI, Claude Code |
| **Large Codebase Refactoring** | Gemini CLI (1M+ context), Claude Code |
| **Security Review** | Amazon Q, CodeRabbit |
| **Documentation Generation** | Claude Code, Gemini CLI |
| **Test Generation** | Copilot Agent, Qodo Merge |

### By Team Size

| Team | Recommended Setup |
|------|-------------------|
| **Solo / OSS** | CodeRabbit (free) + Sweep |
| **Small Team (2-10)** | Qodo Merge + Claude Code |
| **Enterprise** | Copilot Agent + Gemini CLI |
| **AWS-heavy** | Amazon Q Developer |
| **Privacy-focused** | Qodo Merge (self-hosted) + local LLMs |

### By Budget

| Budget | Recommended Tools |
|--------|-------------------|
| **$0** | CodeRabbit, Sourcery, Qodo Merge (all free for OSS) |
| **Low** | Gemini CLI (free) + CodeRabbit |
| **Medium** | Claude Code + Qodo Merge Pro |
| **Enterprise** | Copilot Enterprise + Amazon Q |

---

## Security Best Practices

### 1. Secret Management

```yaml
# Always use GitHub Secrets
env:
  API_KEY: ${{ secrets.API_KEY }}  # ✅ Good

# Never hardcode
env:
  API_KEY: "sk-abc123..."  # ❌ Bad
```

### 2. Minimal Permissions

```yaml
permissions:
  contents: read      # Only what's needed
  pull-requests: write
  # Don't use: permissions: write-all
```

### 3. Restrict Triggers

```yaml
# Require approval for fork PRs
on:
  pull_request_target:  # More secure than pull_request for forks
    types: [opened, synchronize]

jobs:
  review:
    # Require manual approval
    environment: production
```

### 4. Prompt Injection Prevention

```yaml
# Sanitize inputs from untrusted sources
- name: Sanitize PR Title
  run: |
    # Don't directly use PR titles/bodies in prompts
    SAFE_TITLE=$(echo "${{ github.event.pull_request.title }}" | tr -d '`$')
```

### 5. Command Allowlisting (Gemini/Codex)

```yaml
# Explicitly allow only safe commands
- uses: google-github-actions/run-gemini-cli@v1
  with:
    allowed_commands: |
      npm test
      npm run lint
      npm run build
```

### 6. Audit Logging

```yaml
# Enable verbose logging for security review
- uses: anthropics/claude-code-action@v1
  with:
    debug: true
    log_level: verbose
```

---

## Quick Start Checklist

- [ ] Choose tool based on use case and budget
- [ ] Set up API keys as GitHub Secrets
- [ ] Create workflow file in `.github/workflows/`
- [ ] Configure tool-specific settings (`.yaml` files)
- [ ] Test on a non-critical PR first
- [ ] Review security permissions
- [ ] Monitor costs and usage
- [ ] Iterate on prompts/configuration

---

## Resources

### Official Documentation
- [Claude Code Action](https://github.com/anthropics/claude-code-action)
- [Gemini CLI Action](https://github.com/google-github-actions/run-gemini-cli)
- [OpenAI Codex Action](https://github.com/openai/codex-action)
- [Cursor CLI Docs](https://cursor.com/docs/cli/github-actions)
- [Copilot Coding Agent](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent)
- [Amazon Q Developer](https://aws.amazon.com/q/developer/)
- [Qodo Merge / PR-Agent](https://github.com/qodo-ai/pr-agent)
- [CodeRabbit](https://docs.coderabbit.ai/)
- [Sourcery AI](https://sourcery.ai/)
- [Sweep AI](https://docs.sweep.dev/)

### Community Guides
- [Skywork AI Guides](https://skywork.ai/blog/)
- [DevToolsAcademy State of AI Code Review 2025](https://www.devtoolsacademy.com/blog/state-of-ai-code-review-tools-2025/)
- [Ultimate Claude Code Guide (Hidden Tricks)](https://dev.to/holasoymalva/the-ultimate-claude-code-guide-every-hidden-trick-hack-and-power-feature-you-need-to-know-2l45)

### AI-Friendly Documentation
- [llms.txt - Machine-Readable Docs](https://huggingface.co/changelog/docs-llms-txt) - Standard for AI agent documentation consumption
- [Hugging Face Docs (Markdown)](https://huggingface.co/docs/hub/llms.txt) - Access HF docs in LLM-optimized format

---

*Last updated: December 2025*
