# Autonomous "Fire-and-Forget" AI Coding Agents

> Message an agent, it wakes up, works autonomously, delivers results, and goes dormant.

---

## Table of Contents

1. [Overview & Comparison](#overview--comparison)
2. [Devin AI](#1-devin-ai)
3. [OpenHands (All Hands AI)](#2-openhands-all-hands-ai)
4. [Factory Droids](#3-factory-droids)
5. [Cosine Genie](#4-cosine-genie)
6. [SWE-agent](#5-swe-agent)
7. [Potpie AI](#6-potpie-ai)
8. [Bolt.diy](#7-boltdiy)
9. [Choosing the Right Agent](#choosing-the-right-agent)
10. [Integration Patterns](#integration-patterns)

---

## Overview & Comparison

These agents differ from CI/CD-triggered tools - you **message them directly** (Slack, API, web UI) and they autonomously complete tasks.

### Quick Comparison

| Agent | Pricing | Self-Hosted | Slack | API | Best For |
|-------|---------|:-----------:|:-----:|:---:|----------|
| **Devin** | $20-500/mo | ❌ | ✅ | ✅ (Team+) | Full autonomous dev |
| **OpenHands** | Free OSS | ✅ | ❌ | ✅ | Privacy, local control |
| **Factory Droids** | Enterprise | ❌ | ✅ | ✅ | Enterprise SDLC |
| **Cosine Genie** | Contact | ❌ | ❌ | ✅ | Complex codebases |
| **SWE-agent** | Free OSS | ✅ | ❌ | ✅ | Research, GitHub issues |
| **Potpie** | Freemium | ✅ | ✅ | ✅ | Custom agents, Slack |
| **Bolt.diy** | Free OSS | ✅ | ❌ | ❌ | Full-stack web apps |

### Benchmark Scores (SWE-Bench)

| Agent | SWE-Bench Verified | Notes |
|-------|-------------------|-------|
| Factory Droid | 58.75% | #1 on Terminal-Bench |
| Cosine Genie | 72% (SWE-Lancer) | Proprietary Genie 2 model |
| OpenHands | 37.2% | Open-weights 32B model |
| SWE-agent | 18% (Lite) | GPT-4 Turbo |
| Devin | ~14% | Original benchmark |

---

## 1. Devin AI

**The original autonomous AI software engineer**

### Overview

Devin is Cognition's autonomous coding agent - give it a task and it independently plans, codes, debugs, and delivers working software. It maintains its own dev environment with shell, browser, and editor.

### Pricing

| Plan | Price | ACUs | API Access |
|------|-------|------|------------|
| **Core** | $20/month | 50 | ❌ |
| **Team** | $500/month | 250 | ✅ |
| **Enterprise** | Custom | Custom | ✅ |

**ACU (Agent Compute Unit)**: Measures work complexity - planning, debugging, code execution, browser actions. Only consumed when actively working.

### How It Works

1. **Assign a task** via Slack, web UI, or API
2. **Devin plans** - breaks down the problem
3. **Devin executes** - writes code, runs tests, debugs
4. **Devin delivers** - creates PR or deploys

### Slack Integration

```
@devin Build a REST API for user authentication with JWT tokens.
Use FastAPI and PostgreSQL. Include tests.
```

Devin will:
- Set up the project structure
- Write the authentication logic
- Create database models
- Write and run tests
- Open a PR with the changes

### API Access (Team/Enterprise)

```python
import requests

response = requests.post(
    "https://api.devin.ai/v1/sessions",
    headers={"Authorization": f"Bearer {DEVIN_API_KEY}"},
    json={
        "prompt": "Fix the authentication bug in issue #123",
        "repository": "myorg/myrepo"
    }
)

session_id = response.json()["session_id"]

# Check status
status = requests.get(
    f"https://api.devin.ai/v1/sessions/{session_id}",
    headers={"Authorization": f"Bearer {DEVIN_API_KEY}"}
)
```

### Key Features

- **Persistent memory**: Remembers context across sessions
- **Full dev environment**: Shell, browser, code editor
- **Jira/Linear integration**: Works from tickets
- **Real-time collaboration**: Watch Devin work, intervene if needed

### Best For

- Teams wanting a managed autonomous agent
- Companies without resources to self-host
- Non-critical feature development and bug fixes

### Resources

- [Devin Website](https://devin.ai)
- [Pricing](https://devin.ai/pricing/)
- [TechCrunch on Devin 2.0](https://techcrunch.com/2025/04/03/devin-the-viral-coding-ai-agent-gets-a-new-pay-as-you-go-plan/)

---

## 2. OpenHands (All Hands AI)

**Open-source autonomous coding agent - run anywhere**

### Overview

OpenHands is the open standard for autonomous software development. Fully MIT-licensed, model-agnostic, and deployable in your own cloud or on-premises. Recently raised $18.8M Series A.

### Pricing

| Option | Price | Notes |
|--------|-------|-------|
| **Open Source** | Free | Self-hosted, MIT license |
| **OpenHands Cloud** | Usage-based | Managed hosting |
| **Enterprise** | Custom | Self-hosted in your VPC |

### Deployment Options

#### Local (Docker)

```bash
# Quick start
docker run -it --rm \
  -p 3000:3000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e LLM_API_KEY=$OPENAI_API_KEY \
  -e LLM_MODEL=claude-3-5-sonnet-20241022 \
  ghcr.io/openhands/openhands:latest
```

#### Local with AMD Hardware

```bash
# Run with local Ollama
docker run -it --rm \
  -p 3000:3000 \
  -e LLM_API_KEY=ollama \
  -e LLM_MODEL=ollama/codellama:34b \
  -e OLLAMA_API_BASE=http://host.docker.internal:11434 \
  ghcr.io/openhands/openhands:latest
```

#### Kubernetes (Enterprise)

```yaml
# helm values.yaml
openhands:
  replicas: 3
  model:
    provider: anthropic
    name: claude-3-5-sonnet-20241022
  sandbox:
    type: kubernetes
    namespace: openhands-sandboxes
```

### Python SDK

```python
from openhands import Agent, Sandbox

# Create a sandboxed environment
sandbox = Sandbox()

# Initialize agent with your preferred model
agent = Agent(
    model="claude-3-5-sonnet-20241022",
    sandbox=sandbox
)

# Give it a task
result = agent.run("""
Fix the bug in authentication.py where
users can't reset their passwords.
Repository: /workspace/myproject
""")

print(result.summary)
print(result.files_changed)
```

### CLI Mode (Headless)

```bash
# Run from terminal
openhands-cli --task "Implement the feature described in issue #42" \
  --repo /path/to/repo \
  --model claude-3-5-sonnet-20241022

# Headless automation
openhands-cli --task "Update all dependencies and fix breaking changes" \
  --repo . \
  --auto-commit \
  --output json
```

### Key Features

- **Model agnostic**: GPT-4, Claude, Gemini, local LLMs
- **Docker sandboxes**: Secure, isolated execution
- **Full tool access**: Shell, browser, file system, APIs
- **GitHub/GitLab integration**: Direct repo access
- **OpenHands LM**: Their own 32B open-weights model

### Best For

- **Privacy-conscious teams**: Keep code on-premises
- **Cost optimization**: Use local/cheaper models
- **Customization**: Modify agent behavior
- **Research**: Academic and experimental use

### Resources

- [OpenHands Website](https://openhands.dev/)
- [GitHub Repo](https://github.com/OpenHands/OpenHands)
- [Documentation](https://docs.openhands.dev/)
- [All Hands AI](https://www.all-hands.dev/)

---

## 3. Factory Droids

**Enterprise-grade autonomous software development**

### Overview

Factory's Droids are production-ready AI agents that handle the entire SDLC - from feature development to incident response. #1 on Terminal-Bench with 58.75%.

### Pricing

Enterprise pricing - contact sales. Customers include NVIDIA, MongoDB, Zapier, Ernst & Young, Bayer.

### Integration Points

Factory Droids work where you work:

| Interface | Description |
|-----------|-------------|
| **Slack** | @droid commands in channels |
| **Linear/Jira** | Assign tickets directly |
| **IDE** | VS Code, JetBrains, Vim |
| **Terminal** | CLI for developers |
| **API** | Custom integrations |

### Slack Usage

```
@droid Build the user dashboard feature from ticket LIN-234

@droid Review PR #89 for security issues

@droid Why is the checkout flow failing in production?
```

### Key Capabilities

| Capability | Description |
|------------|-------------|
| **Feature Development** | Build production-ready features from specs |
| **Code Review** | Automated review with context awareness |
| **Refactoring** | Large-scale codebase migrations |
| **Incident Response** | Diagnose and fix production issues |
| **Documentation** | Generate and update docs |
| **Codebase Q&A** | Answer questions about your code |

### Memory System

Droids have org and user-level memory:
- **Decisions**: Remembers architectural choices
- **Documentation**: Indexes your docs and runbooks
- **Patterns**: Learns your coding standards
- **Context**: Carries context across sessions

### Results (Customer Reported)

| Metric | Improvement |
|--------|-------------|
| Feature delivery | 31x faster |
| Migration time | 96.1% reduction |
| On-call resolution | 95.8% faster |

### Best For

- **Large enterprises**: Complex codebases, compliance needs
- **Teams using Linear/Jira**: Deep ticket integration
- **Incident response**: Production debugging
- **Multi-repo organizations**: Cross-codebase understanding

### Resources

- [Factory Website](https://factory.ai/)
- [Droids Product](https://factory.ai/news/factory-is-ga)
- [Terminal-Bench Results](https://factory.ai/news/terminal-bench)

---

## 4. Cosine Genie

**Proprietary model, highest benchmark scores**

### Overview

Cosine's Genie is powered by Genie 2, a proprietary model built specifically for complex coding tasks. Achieves 72% on SWE-Lancer benchmark, outperforming OpenAI and Anthropic models.

### Pricing

Contact for pricing. Platform access with dedicated support.

### How It Works

Unlike sandboxed browser solutions, Cosine CLI runs in your **actual environment**:
- Access local files
- Run builds and tests
- Use project-specific tools
- Full Git integration

### CLI Usage

```bash
# Install
npm install -g @cosine/cli

# Authenticate
cosine auth login

# Run a task
cosine run "Implement the search feature from the PRD in docs/search.md"

# Fix a bug
cosine fix "Users are seeing 500 errors on the checkout page"

# Review code
cosine review --pr 123
```

### Multi-Agent Mode

Genie Multi-agent decomposes your backlog into logical subtasks:

```bash
# Process entire sprint backlog
cosine backlog --sprint "Sprint 24" --parallel 5
```

Genie will:
1. Parse all tickets in the sprint
2. Decompose into subtasks
3. Assign agents to each subtask
4. Coordinate and merge results
5. Create PRs for review

### Key Features

- **50+ languages**: Not limited to Python/JS
- **Genie 2 model**: Purpose-built for coding
- **No sandbox**: Runs in your real environment
- **Multi-agent**: Parallel task processing
- **Autonomous validation**: Tests before submitting

### Genie 3 (Coming)

Training on rich sandbox environments with full tool access:
- Compilers and debuggers
- Documentation access
- Internet resources
- Trial-and-error learning

### Best For

- **Complex codebases**: Enterprise-scale projects
- **High accuracy needs**: Mission-critical code
- **Multi-language teams**: Diverse tech stacks
- **Backlog processing**: Sprint automation

### Resources

- [Cosine Website](https://cosine.sh)
- [Genie Product](https://cosine.sh/product)
- [Genie 2 Announcement](https://cosine.sh/blog/genie-autonomous-software-engineer)

---

## 5. SWE-agent

**Open-source research agent from Princeton**

### Overview

SWE-agent is an academic project that takes GitHub issues and autonomously fixes them. Great for research, experimentation, and learning how AI agents work.

### Pricing

Free and open-source (MIT license)

### Installation

```bash
# Clone the repo
git clone https://github.com/SWE-agent/SWE-agent.git
cd SWE-agent

# Install dependencies
pip install -e .

# Set up API keys
export OPENAI_API_KEY=your-key
# or
export ANTHROPIC_API_KEY=your-key
```

### Usage

#### Fix a GitHub Issue

```bash
python run.py \
  --model_name claude-3-5-sonnet-20241022 \
  --data_path issue.json \
  --repo_path /path/to/repo \
  --config_file config/default.yaml
```

#### Issue JSON Format

```json
{
  "instance_id": "myorg__myrepo__123",
  "repo": "myorg/myrepo",
  "base_commit": "abc123",
  "problem_statement": "Users can't log in with OAuth",
  "hints_text": "Check the callback URL configuration"
}
```

### Agent-Computer Interface (ACI)

SWE-agent uses a custom interface optimized for LLMs:

```python
# Custom commands available to the agent
open <file>           # Open file in editor
goto <line>           # Jump to line number
scroll_down           # Scroll down in file
scroll_up             # Scroll up in file
create <file>         # Create new file
edit <start>:<end>    # Edit lines
submit                # Submit the solution
```

### Key Features

- **Model agnostic**: GPT-4, Claude, open models
- **GitHub integration**: Direct issue processing
- **Cybersecurity mode**: EnIGMA for CTF challenges
- **Benchmarked**: Standard SWE-Bench evaluation
- **Research-friendly**: Well-documented for academic use

### EnIGMA Mode (Cybersecurity)

```bash
python run.py \
  --model_name gpt-4 \
  --ctf_mode \
  --challenge_path /path/to/ctf/challenge
```

### Best For

- **Researchers**: Understanding AI agent behavior
- **Experimenters**: Testing different models/prompts
- **Learning**: How autonomous agents work
- **Hackathons**: Quick issue-to-PR automation

### Resources

- [GitHub Repo](https://github.com/SWE-agent/SWE-agent)
- [Paper (arXiv)](https://arxiv.org/abs/2405.15793)
- [SWE-Bench](https://swe-bench.github.io/)

---

## 6. Potpie AI

**Custom agents for your codebase + Slack**

### Overview

Potpie lets you build custom AI agents tailored to your specific codebase. It builds a knowledge graph of your code for deep understanding, then lets you interact via Slack, VS Code, or API.

### Pricing

| Plan | Price | Notes |
|------|-------|-------|
| **Free** | $0 | Limited usage |
| **Pro** | $29/month | More capacity |
| **Team** | $99/month | Team features |
| **Enterprise** | Custom | Self-hosted |

### Slack Integration Setup

1. Install Potpie Slack App (2 minutes)
2. Connect your repositories
3. Start chatting with your agents

```
@potpie debug Why is the payment processing failing?

@potpie generate Add rate limiting to the API endpoints

@potpie review Check PR #45 for security issues
```

### Pre-built Agents

| Agent | Purpose |
|-------|---------|
| **Debugging Agent** | Analyzes stacktraces, provides fix steps |
| **Code Generation Agent** | New features, refactoring |
| **Code Review Agent** | PR reviews with codebase context |
| **Onboarding Agent** | Explains codebase to new devs |
| **Q&A Agent** | Answers questions about code |

### Custom Agent Creation

```python
from potpie import Agent, KnowledgeGraph

# Build knowledge graph from your repo
kg = KnowledgeGraph.from_repo("/path/to/repo")

# Create custom agent
agent = Agent(
    name="API Expert",
    knowledge_graph=kg,
    system_prompt="""
    You are an expert on our REST API.
    Help developers understand endpoints,
    debug issues, and suggest improvements.
    """,
    tools=["code_search", "file_read", "web_access"]
)

# Deploy to Slack
agent.deploy_to_slack(
    workspace="mycompany",
    channel="#api-help"
)
```

### VS Code Extension

```
1. Install "Potpie" from VS Code marketplace
2. Authenticate with Potpie
3. Use Command Palette: "Potpie: Ask Agent"
4. Or use inline comments: // @potpie explain this
```

### Key Features

- **Knowledge graph**: Deep codebase understanding
- **Custom agents**: Build purpose-specific helpers
- **Slack native**: 2-minute setup
- **Multi-model**: OpenAI, Claude, Gemini
- **Web access**: Pull context from URLs

### Best For

- **Teams on Slack**: Native integration
- **Custom workflows**: Build specialized agents
- **Onboarding**: Help new developers
- **Support teams**: Answer codebase questions

### Resources

- [Potpie Website](https://potpie.ai)
- [GitHub Repo](https://github.com/potpie-ai/potpie)
- [Documentation](https://docs.potpie.ai/)
- [Slack Integration Docs](https://docs.potpie.ai/extensions/slack)

---

## 7. Bolt.diy

**Self-hosted AI web app builder**

### Overview

Bolt.diy is an open-source, self-hostable version of bolt.new. Give it a prompt, it builds full-stack web applications in your browser. Great for prototyping and learning.

### Pricing

Free and open-source (MIT license for core, WebContainers requires commercial license for production)

### Quick Start (Docker)

```bash
# Clone
git clone https://github.com/stackblitz-labs/bolt.diy.git
cd bolt.diy

# Configure
cp .env.example .env
# Edit .env with your API keys

# Run
docker-compose up -d

# Access at http://localhost:3000
```

### Supported Models

Configure in `.env`:

```bash
# OpenAI
OPENAI_API_KEY=sk-...

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Google
GOOGLE_GENERATIVE_AI_API_KEY=...

# Local (Ollama)
OLLAMA_API_BASE=http://localhost:11434

# And 15+ more providers
```

### Usage

1. **Describe your app**: "Build a todo app with user authentication"
2. **Watch it build**: Real-time code generation
3. **Iterate**: "Add a dark mode toggle"
4. **Deploy**: Direct to Netlify, Vercel, or GitHub Pages

### Key Features

| Feature | Description |
|---------|-------------|
| **19+ LLMs** | OpenAI, Claude, Gemini, Ollama, etc. |
| **Integrated terminal** | See command output |
| **Version control** | Revert to earlier versions |
| **Image prompts** | Attach screenshots for context |
| **Supabase integration** | Database management |
| **Expo support** | React Native apps |
| **Diff view** | See AI changes |

### Self-Hosting Options

| Platform | Notes |
|----------|-------|
| **Docker** | docker-compose up |
| **Railway** | One-click deploy |
| **Easypanel** | Managed hosting |
| **VPS** | Full control |

### Configuration

```yaml
# docker-compose.yml
version: '3.8'
services:
  bolt:
    build: .
    ports:
      - "3000:3000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ./projects:/app/projects
```

### Best For

- **Prototyping**: Quick app scaffolding
- **Learning**: See how apps are built
- **Privacy**: Keep code on your infrastructure
- **Experimentation**: Try different models

### Resources

- [GitHub Repo](https://github.com/stackblitz-labs/bolt.diy)
- [Railway Deploy](https://railway.com/deploy/boltdiy)
- [Bolt.new (hosted)](https://bolt.new)

---

## Choosing the Right Agent

### By Use Case

| Use Case | Recommended |
|----------|-------------|
| **Quick prototypes** | Bolt.diy, Devin Core |
| **Enterprise development** | Factory Droids, Cosine |
| **Privacy-first** | OpenHands (self-hosted) |
| **Slack-native team** | Potpie, Factory, Devin |
| **Research/learning** | SWE-agent, OpenHands |
| **Complex codebases** | Cosine Genie, Factory |
| **Budget-conscious** | OpenHands, SWE-agent |

### By Budget

| Budget | Options |
|--------|---------|
| **$0** | OpenHands, SWE-agent, Bolt.diy |
| **$20-100/mo** | Devin Core, Potpie Pro |
| **$500+/mo** | Devin Team, Potpie Team |
| **Enterprise** | Factory, Cosine, OpenHands Enterprise |

### By Team Size

| Team | Recommended |
|------|-------------|
| **Solo** | Devin Core, Bolt.diy |
| **Small (2-10)** | Potpie, OpenHands |
| **Medium (10-50)** | Devin Team, Cosine |
| **Enterprise (50+)** | Factory Droids |

### By Integration Needs

| Need | Best Options |
|------|--------------|
| **Slack** | Potpie, Factory, Devin |
| **Linear/Jira** | Factory, Devin |
| **GitHub/GitLab** | All options |
| **Custom API** | OpenHands, Devin Team |
| **VS Code** | Potpie, Cosine |
| **Self-hosted** | OpenHands, Bolt.diy, Potpie |

---

## Integration Patterns

### Pattern 1: Slack Bot Trigger

```mermaid
User -> Slack: @agent fix bug #123
Slack -> Agent API: POST /tasks
Agent -> GitHub: Clone repo
Agent -> Agent: Plan & execute
Agent -> GitHub: Create PR
Agent -> Slack: "PR #456 ready for review"
```

### Pattern 2: Ticket Automation

```yaml
# Linear/Jira webhook -> Agent
1. Issue created with "ai-ready" label
2. Webhook fires to agent API
3. Agent clones repo, analyzes issue
4. Agent implements solution
5. Agent creates PR, links to issue
6. Agent comments on issue with status
```

### Pattern 3: Scheduled Tasks

```python
# Cron-triggered maintenance
import schedule
from openhands import Agent

def nightly_maintenance():
    agent = Agent(model="claude-3-5-sonnet")

    # Update dependencies
    agent.run("Update all npm dependencies, fix any breaking changes")

    # Clean up code
    agent.run("Remove unused imports and dead code")

    # Update docs
    agent.run("Ensure all public functions have docstrings")

schedule.every().day.at("02:00").do(nightly_maintenance)
```

### Pattern 4: API Gateway

```python
# FastAPI wrapper for agent access
from fastapi import FastAPI, BackgroundTasks
from openhands import Agent

app = FastAPI()
agent = Agent(model="claude-3-5-sonnet")

@app.post("/tasks")
async def create_task(prompt: str, repo: str, background_tasks: BackgroundTasks):
    task_id = generate_id()
    background_tasks.add_task(run_agent, task_id, prompt, repo)
    return {"task_id": task_id, "status": "started"}

@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    return get_task_status(task_id)

async def run_agent(task_id: str, prompt: str, repo: str):
    result = agent.run(prompt, repo=repo)
    save_result(task_id, result)
```

---

## Summary Comparison Table

| Agent | Autonomy | Setup | Cost | Best Feature |
|-------|----------|-------|------|--------------|
| **Devin** | Full | Easy | $$$ | Persistent memory |
| **OpenHands** | Full | Medium | Free | Self-hosted, open |
| **Factory** | Full | Enterprise | $$$$ | SDLC coverage |
| **Cosine** | Full | Medium | $$$ | Benchmark leader |
| **SWE-agent** | Full | Technical | Free | Research-grade |
| **Potpie** | Guided | Easy | $ | Custom agents |
| **Bolt.diy** | Guided | Easy | Free | Web app builder |

---

## Resources

### Official Sites
- [Devin](https://devin.ai)
- [OpenHands](https://openhands.dev)
- [Factory](https://factory.ai)
- [Cosine](https://cosine.sh)
- [SWE-agent](https://github.com/SWE-agent/SWE-agent)
- [Potpie](https://potpie.ai)
- [Bolt.diy](https://github.com/stackblitz-labs/bolt.diy)

### Benchmarks
- [SWE-Bench](https://swe-bench.github.io/)
- [Terminal-Bench](https://factory.ai/news/terminal-bench)
- [SWE-Lancer](https://cosine.sh/blog/genie-autonomous-software-engineer)

---

*Last updated: December 2025*
