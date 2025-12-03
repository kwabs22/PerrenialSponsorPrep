# Free/Low-Cost Hackathon Ideas

> Reusable ideas for hackathons when sponsors don't provide API credits.

---

## Cost-Free Tech Stack Components

### Free LLM Options
| Option | Cost | Notes |
|--------|------|-------|
| **Ollama + Llama 3.2** | $0 | Local, no API key needed |
| **HuggingFace Inference** | $0 | Free tier available |
| **Groq** | $0 | Generous free tier, fast inference |
| **Google AI Studio** | $0 | Free Gemini API access |
| **Mistral (Le Chat)** | $0 | Free tier available |

### Free Database/Vector Options
| Option | Cost | Notes |
|--------|------|-------|
| **Chroma** | $0 | Local, in-memory |
| **Neon** | $0 | 512MB free tier |
| **Supabase** | $0 | 500MB + pgvector |
| **PlanetScale** | $0 | 5GB free tier |
| **Cloudflare D1** | $0 | 5GB free tier |

### Free Hosting/Deployment
| Option | Cost | Notes |
|--------|------|-------|
| **Cloudflare Workers** | $0 | 100K requests/day |
| **Vercel** | $0 | Hobby tier |
| **Streamlit Cloud** | $0 | Public apps free |
| **HuggingFace Spaces** | $0 | Gradio/Streamlit hosting |
| **GitHub Pages** | $0 | Static sites |

### Free Auth
| Option | Cost | Notes |
|--------|------|-------|
| **Clerk** | $0 | 10K MAUs free |
| **Supabase Auth** | $0 | Included in free tier |
| **Auth0** | $0 | 7K MAUs free |

---

## Ready-to-Use Project Ideas

### 1. IRC-to-AI Bridge (Resurrection Theme)
**Concept:** Bring IRC back from the dead with modern AI

**Free Stack:**
- `04-meta-llama-ollama` - Local LLM (Llama 3.2)
- `13-neon-mcp` - Database (free tier)
- `31-discord-faq-bot` - Bot framework reference

**Why it works:** Nostalgia + modern AI = memorable demo

---

### 2. Universal Hackathon Starter Kit (Skeleton Crew Theme)
**Concept:** Reusable template for any hackathon

**Free Stack:**
- `24-clerk-reverification` - Auth (free tier)
- `22-streamlit-dashboard` - UI (Streamlit Cloud free)
- `46-cloudflare-edge-notes` - Backend (Workers free tier)

**Why it works:** Meta-submission that helps the community

---

### 3. Spooky Code Reviewer (Costume Contest Theme)
**Concept:** Horror-themed code analysis with dramatic UI

**Free Stack:**
- `36-github-dependabot` - GitHub API (free)
- `37-docker-scout` - Security scanning (free tier)
- HuggingFace free models for analysis

**Why it works:** Polished UI + theme = memorable presentation

---

### 4. Edge + Vector Hybrid Search (Frankenstein Theme)
**Concept:** Combine edge computing with vector search

**Free Stack:**
- `46-cloudflare-edge-notes` - Edge backend (free)
- `11-chroma-multimodal` - Local vector DB (free)
- `27-gradio-ssr` - UI (HuggingFace Spaces free)

**Why it works:** Novel architecture, impressive technical demo

---

### 5. Local Document Q&A (General Purpose)
**Concept:** Chat with your documents, fully local

**Free Stack:**
- `04-meta-llama-ollama` - Local LLM
- `11-chroma-multimodal` - Local embeddings
- `22-streamlit-dashboard` - Simple UI

**Why it works:** Privacy-focused, no API costs ever

---

### 6. Multi-Provider Fallback Chat (Frankenstein Theme)
**Concept:** Chat that falls back through free tiers

**Free Stack:**
- Groq (primary) → HuggingFace (fallback) → Ollama (offline)
- `22-streamlit-dashboard` - UI
- `12-supabase-edge-cron` - Message storage

**Why it works:** Clever use of multiple free tiers

---

## Expensive APIs to Avoid (Without Credits)

| API | Cost | Alternative |
|-----|------|-------------|
| OpenAI Realtime | ~$0.06/min | Groq + TTS |
| Anthropic Computer Use | ~$0.01/action | Screenshot + local LLM |
| GPT-4o | ~$0.01/1K tokens | Llama 3.2 70B via Groq |
| Claude 3.5 Sonnet | ~$0.01/1K tokens | Mistral Large free tier |

---

## Hackathon Categories This Covers

These ideas map to common hackathon themes:

| Theme | Best Idea |
|-------|-----------|
| **Resurrection** | IRC-to-AI Bridge |
| **Frankenstein** | Edge + Vector Hybrid, Multi-Provider Fallback |
| **Skeleton Crew** | Universal Starter Kit |
| **Costume Contest** | Spooky Code Reviewer |
| **AI/ML** | Local Document Q&A |
| **Developer Tools** | Spooky Code Reviewer, Starter Kit |
| **Open Innovation** | Any of the above |

---

## Tips for Zero-Budget Hackathons

1. **Stack free tiers** - Combine Groq + Supabase + Vercel for full stack at $0
2. **Go local** - Ollama + Chroma means no API keys needed
3. **Use HuggingFace Spaces** - Free GPU for Gradio apps
4. **Leverage GitHub Actions** - Free CI/CD for demos
5. **Static + Edge** - Cloudflare Pages + Workers = fast & free

---

*Created: December 2025*
*For use with: submissions/ templates in this repo*
