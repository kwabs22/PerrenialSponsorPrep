# GitHub Free Tools: Complete Guide

> Everything GitHub offers for free - from AI to hosting to security. Updated December 2025.

---

## Table of Contents

1. [Quick Reference Card](#quick-reference-card)
2. [AI & Copilot](#ai--copilot)
3. [Development Environment](#development-environment)
4. [CI/CD & Automation](#cicd--automation)
5. [Hosting & Deployment](#hosting--deployment)
6. [Security Features](#security-features)
7. [Collaboration Tools](#collaboration-tools)
8. [Package & Container Registry](#package--container-registry)
9. [AI Models Playground](#ai-models-playground)
10. [Student & Education](#student--education)
11. [Comparison: Free vs Pro vs Team](#comparison-free-vs-pro-vs-team)
12. [Resources](#resources)

---

## Quick Reference Card

### Free Plan Limits at a Glance

| Feature | Free Tier Limit |
|---------|-----------------|
| **Public Repos** | Unlimited |
| **Private Repos** | Unlimited |
| **Collaborators** | Unlimited |
| **Actions (Public)** | Unlimited minutes |
| **Actions (Private)** | 2,000 min/month |
| **Packages Storage** | 500 MB |
| **Codespaces** | 120 core-hours/month |
| **Codespaces Storage** | 15 GB/month |
| **Pages Bandwidth** | 100 GB/month |
| **Pages Site Size** | 1 GB max |
| **Copilot Completions** | 2,000/month |
| **Copilot Chat** | 50 messages/month |
| **LFS Storage** | 1 GB |
| **LFS Bandwidth** | 1 GB/month |

---

## AI & Copilot

### GitHub Copilot Free

[Copilot](https://github.com/features/copilot) | [Plans](https://github.com/features/copilot/plans)

Available to everyone with a GitHub account - no trial, no credit card.

| Feature | Free | Pro ($10/mo) |
|---------|------|--------------|
| Code completions | 2,000/month | Unlimited |
| Chat messages | 50/month | Unlimited |
| Models | GPT-4o, Claude 3.5 Sonnet | All models |
| Multi-file editing | ❌ | ✅ |
| Copilot Extensions | ❌ | ✅ |

**Available in:**
- VS Code (native)
- JetBrains IDEs
- Neovim
- Visual Studio
- GitHub.com (web)
- GitHub Mobile

### Copilot Features (Free Tier)

```
✅ Code completions (2,000/month)
✅ Inline chat (50/month)
✅ Model selection (GPT-4o or Claude 3.5)
✅ Code explanations
✅ Test generation suggestions
✅ Documentation assistance
❌ Agent mode
❌ Multi-file editing
❌ Copilot Extensions marketplace
```

---

## Development Environment

### GitHub Codespaces

[Codespaces](https://github.com/features/codespaces) | [Docs](https://docs.github.com/en/codespaces)

Full VS Code environment in the cloud, accessible from any browser.

#### Free Allowance (Personal Accounts)

| Resource | Free Limit |
|----------|------------|
| Core hours | 120/month (60 hrs on 2-core) |
| Storage | 15 GB/month |

#### Machine Types

| Cores | RAM | Free Hours/Month |
|-------|-----|------------------|
| 2 | 8 GB | 60 hours |
| 4 | 16 GB | 30 hours |
| 8 | 32 GB | 15 hours |
| 16 | 64 GB | 7.5 hours |

#### Features
- Pre-configured dev containers
- Dotfiles support
- Port forwarding
- VS Code extensions
- Terminal access
- GPU support (paid)

### GitHub CLI

[CLI](https://cli.github.com/) | [Manual](https://cli.github.com/manual/)

**Completely free** - manage GitHub from your terminal.

```bash
# Install
brew install gh        # macOS
winget install gh      # Windows
sudo apt install gh    # Ubuntu

# Common commands
gh repo clone owner/repo
gh pr create
gh issue list
gh workflow run
gh codespace create
gh copilot explain "code"
gh copilot suggest "task"
```

### GitHub Desktop

[Desktop](https://desktop.github.com/) | [Docs](https://docs.github.com/en/desktop)

**Completely free** GUI for Git.

- Visual commit history
- Branch management
- Drag-and-drop cherry-pick
- Stash changes
- Resolve merge conflicts
- Syntax-highlighted diffs

### GitHub Mobile

[iOS](https://apps.apple.com/app/github/id1477376905) | [Android](https://play.google.com/store/apps/details?id=com.github.android)

**Completely free** mobile app.

- Review and merge PRs
- Manage issues
- Browse code
- Push notifications
- Markdown support
- Dark mode

---

## CI/CD & Automation

### GitHub Actions

[Actions](https://github.com/features/actions) | [Marketplace](https://github.com/marketplace?type=actions)

#### Free Limits

| Repository Type | Minutes/Month | Storage |
|-----------------|---------------|---------|
| Public | **Unlimited** | 500 MB |
| Private | 2,000 | 500 MB |

#### Runner Multipliers (Private Repos)

| OS | Multiplier |
|----|------------|
| Linux | 1x |
| Windows | 2x |
| macOS | 10x |

*Example: 2,000 Linux mins = 1,000 Windows mins = 200 macOS mins*

#### Free Features

```yaml
# Example: Free CI/CD workflow
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest  # Free for public repos
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm test
```

### Dependabot

[Dependabot](https://docs.github.com/en/code-security/dependabot)

**Completely free** automated dependency updates.

- Security updates (automatic PRs)
- Version updates (scheduled)
- Grouped updates
- Custom schedules
- Ignore rules

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
```

---

## Hosting & Deployment

### GitHub Pages

[Pages](https://pages.github.com/) | [Docs](https://docs.github.com/en/pages)

**Free static site hosting** directly from your repo.

#### Limits

| Resource | Limit |
|----------|-------|
| Site size | 1 GB |
| Bandwidth | 100 GB/month |
| Builds | 10/hour |
| Build timeout | 10 minutes |

#### Features

```
✅ Custom domains (free)
✅ HTTPS/SSL (automatic)
✅ Jekyll integration
✅ GitHub Actions deployment
✅ Branch/folder source
❌ Server-side code
❌ Database connections
```

#### Availability

| Account Type | Public Repos | Private Repos |
|--------------|--------------|---------------|
| Free | ✅ | ❌ |
| Pro | ✅ | ✅ |
| Team | ✅ | ✅ |

### GitHub Releases

[Releases](https://docs.github.com/en/repositories/releasing-projects-on-github)

**Free** software distribution.

- Binary attachments (up to 2 GB each)
- Release notes (auto-generated)
- Pre-release tags
- Download counts
- Permanent URLs

---

## Security Features

### Free for All Repositories

| Feature | Public | Private |
|---------|--------|---------|
| Dependency graph | ✅ | ✅ |
| Dependabot alerts | ✅ | ✅ |
| Dependabot security updates | ✅ | ✅ |
| Security advisories | ✅ | ✅ |
| Secret scanning (push protection) | ✅ | ❌* |

*Available with GitHub Advanced Security (paid)

### Free for Public Repositories Only

| Feature | Description |
|---------|-------------|
| **Code scanning** | Find vulnerabilities with CodeQL |
| **Secret scanning** | Detect leaked credentials |
| **Dependency review** | Block vulnerable dependencies |

### Push Protection for Users

**Free for everyone** - automatically blocks you from pushing secrets to public repos, regardless of repo settings.

### Paid Security Features

| Product | Price | Features |
|---------|-------|----------|
| Secret Protection | $19/user/mo | Push protection, AI detection, alerts |
| Code Security | $30/user/mo | CodeQL, Copilot Autofix, campaigns |

---

## Collaboration Tools

### GitHub Issues

[Issues](https://github.com/features/issues)

**Completely free** issue tracking.

- Labels and milestones
- Assignees
- Templates
- Task lists
- Linked PRs
- Timeline
- Reactions

### GitHub Projects

[Projects](https://github.com/features/issues)

**Free** project management boards.

| Feature | Free | Team |
|---------|------|------|
| Public projects | Unlimited | Unlimited |
| Private projects | Limited | Unlimited |
| Custom fields | ✅ | ✅ |
| Workflows/Automation | ✅ | ✅ |
| Insights | Basic | Advanced |

### GitHub Discussions

[Discussions](https://docs.github.com/en/discussions)

**Free** community forums for your repo.

- Categories
- Polls
- Announcements
- Q&A with accepted answers
- Upvoting
- Threaded conversations

### Wikis

**Free** documentation per repository.

- Markdown support
- Sidebar navigation
- Git-backed (clone locally)
- Access control
- Edit history

### Gists

[Gist](https://gist.github.com/)

**Free** code snippet sharing.

- Public or secret
- Versioned
- Forkable
- Embeddable
- Comments

---

## Package & Container Registry

### GitHub Packages

[Packages](https://github.com/features/packages)

Host your packages alongside your code.

#### Free Limits

| Resource | Public Repos | Private Repos |
|----------|--------------|---------------|
| Storage | Unlimited | 500 MB |
| Transfer | Unlimited | 1 GB/month |

#### Supported Registries

| Registry | URL |
|----------|-----|
| npm | `npm.pkg.github.com` |
| Maven | `maven.pkg.github.com` |
| Gradle | `maven.pkg.github.com` |
| NuGet | `nuget.pkg.github.com` |
| RubyGems | `rubygems.pkg.github.com` |
| Docker/OCI | `ghcr.io` |

### GitHub Container Registry (ghcr.io)

**Free** Docker image hosting.

```bash
# Push image
docker tag myimage ghcr.io/username/myimage:latest
docker push ghcr.io/username/myimage:latest

# Pull image (public)
docker pull ghcr.io/username/myimage:latest
```

---

## AI Models Playground

### GitHub Models

[Models Marketplace](https://github.com/marketplace/models)

**Free** AI playground for testing LLMs.

#### Available Models

| Provider | Models |
|----------|--------|
| OpenAI | GPT-4o, GPT-4o-mini |
| Meta | Llama 3.1, Llama 3.3 |
| Microsoft | Phi-3, Phi-3.5 |
| Mistral | Mistral Large 2 |
| Cohere | Command R+ |

#### Rate Limits (Free)

| Model Tier | Requests/Min | Requests/Day | Tokens (In/Out) |
|------------|--------------|--------------|-----------------|
| Low | 15 | 150 | 8K/4K |
| High | 10 | 50 | 8K/4K |

#### Features

- Interactive playground
- API access (OpenAI-compatible format)
- Codespaces integration
- Sample code
- No data sharing with model providers

```python
# Use GitHub Models API
from openai import OpenAI

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"]
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

---

## Student & Education

### GitHub Student Developer Pack

[Student Pack](https://education.github.com/pack)

**Free** premium tools for verified students.

#### Included Benefits

| Tool | Value | Duration |
|------|-------|----------|
| GitHub Pro | $4/mo | While student |
| Copilot Pro | $10/mo | While student |
| Codespaces | Extra hours | While student |
| JetBrains IDEs | $200+/yr | While student |
| DigitalOcean | $200 credit | 1 year |
| Azure | $100 credit | 1 year |
| Namecheap | Free .me domain | 1 year |
| And 100+ more... | Various | Various |

### GitHub Classroom

[Classroom](https://classroom.github.com/)

**Free** for educators.

- Assignment distribution
- Starter code templates
- Auto-grading with Actions
- Plagiarism detection
- Roster management

### GitHub Campus Program

[Campus](https://education.github.com/schools)

**Free** for educational institutions.

- Enterprise features for free
- Unlimited private repos
- Advanced security
- GitHub Actions minutes

---

## Comparison: Free vs Pro vs Team

### Personal Plans

| Feature | Free | Pro ($4/mo) |
|---------|------|-------------|
| Public repos | Unlimited | Unlimited |
| Private repos | Unlimited | Unlimited |
| Collaborators | Unlimited | Unlimited |
| Actions minutes | 2,000 | 3,000 |
| Packages storage | 500 MB | 2 GB |
| Codespaces hours | 120 core-hr | 180 core-hr |
| Pages (private repos) | ❌ | ✅ |
| Protected branches | ❌ | ✅ |
| Multiple reviewers | ❌ | ✅ |
| Wiki (private repos) | ❌ | ✅ |
| Insights | Basic | Full |

### Organization Plans

| Feature | Free | Team ($4/user/mo) |
|---------|------|-------------------|
| Public repos | Unlimited | Unlimited |
| Private repos | Unlimited | Unlimited |
| Actions minutes | 2,000 | 3,000 |
| Packages storage | 500 MB | 2 GB |
| Required reviewers | ❌ | ✅ |
| Code owners | ❌ | ✅ |
| Draft PRs | ❌ | ✅ |
| Branch protection rules | Basic | Advanced |
| Security features | Basic | Advanced |

---

## Resources

### Official Documentation
- [GitHub Docs](https://docs.github.com/)
- [GitHub Pricing](https://github.com/pricing)
- [GitHub Pricing Calculator](https://github.com/pricing/calculator)
- [GitHub Features](https://github.com/features)
- [GitHub Changelog](https://github.blog/changelog/)

### Free Tier Specific
- [GitHub's Plans](https://docs.github.com/en/get-started/learning-about-github/githubs-plans)
- [Actions Billing](https://docs.github.com/en/billing/managing-billing-for-github-actions)
- [Codespaces Billing](https://docs.github.com/en/billing/managing-billing-for-github-codespaces)
- [Pages Limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)
- [Packages Billing](https://docs.github.com/en/billing/managing-billing-for-github-packages)

### Security
- [Security Features](https://docs.github.com/en/code-security/getting-started/github-security-features)
- [About Advanced Security](https://docs.github.com/en/get-started/learning-about-github/about-github-advanced-security)
- [Dependabot](https://docs.github.com/en/code-security/dependabot)

### Tools
- [GitHub CLI](https://cli.github.com/)
- [GitHub Desktop](https://desktop.github.com/)
- [GitHub Mobile](https://github.com/mobile)
- [GitHub Models](https://github.com/marketplace/models)

### Education
- [GitHub Education](https://education.github.com/)
- [Student Developer Pack](https://education.github.com/pack)
- [GitHub Classroom](https://classroom.github.com/)

### AI Documentation Standard
- [llms.txt - Machine-Readable Docs](https://huggingface.co/changelog/docs-llms-txt) - Standard for AI-accessible documentation

---

## Tips for Maximizing Free Tier

### Actions Minutes

1. **Use public repos** for open-source projects (unlimited minutes)
2. **Cache dependencies** to reduce build time
3. **Use self-hosted runners** (free, unlimited)
4. **Cancel redundant workflows** with concurrency groups
5. **Use Linux runners** (1x multiplier vs 10x for macOS)

### Codespaces Hours

1. **Stop codespaces** when not in use
2. **Use 2-core machines** when possible
3. **Set auto-suspend timeout** (default: 30 min)
4. **Delete unused codespaces**

### Storage

1. **Use Git LFS** for large files
2. **Prune old packages** regularly
3. **Clean up releases** you don't need
4. **Use `.gitignore`** properly

---

*Last updated: December 2025*
